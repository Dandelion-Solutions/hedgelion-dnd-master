"""Owner-native semantic history and retained event-time decision basis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
import re
import sys
from types import MappingProxyType
from typing import TYPE_CHECKING, Final
import weakref

from .live_state import (
    LiveEnvelope,
    LiveRouting,
    _SelectedLiveReadCapability,
    _is_owner_issued_selected_live_read_capability,
    select_live_source,
)
from .policy_basis import PinnedCampaign

if TYPE_CHECKING:
    from .policy_basis import RepositoryPort


# framework_module_version: 1.0.9
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.9"
_GIT_REVISION: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_GIT_REF: Final = re.compile(r"^refs/heads/[^\s/]+(?:/[^\s/]+)*$")
_CAMPAIGN_REF: Final = re.compile(r"^refs/heads/campaign/[^\s/]+$")
_LIVE_ORIGIN: Final = re.compile(r"^LIVE:[A-Za-z0-9_.:-]+$")
_CURSOR: Final = re.compile(r"^evt:([1-9][0-9]*)$")
_SOURCE_DOMAIN: Final = "campaign.semantic_events@S"
_SOURCE_LANE: Final = "evt"
_SEMANTIC_CONTRACT_GENERATION: Final = 1
_SOURCE_WINDOW_SCHEMA_VERSION: Final = 1
_SEMANTIC_EVENT_PATH: Final = "LOG/SEMANTIC_EVENTS"
_NATIVE_HISTORY_KIND: Final = "runtime.native_history"


class HistoryContractError(ValueError):
    """Raised when a caller supplies invalid native history material."""


class _EvtLaneEnrollmentWindowAdapter:
    """Read one exact Step-5.10 evt window without issuing history evidence."""

    def __init__(
        self,
        repository: RepositoryPort,
        current_routing: LiveRouting | None,
        selected_live_reader: _SelectedLiveReadCapability | None,
    ) -> None:
        self._repository = repository
        self._current_routing = current_routing
        self._selected_live_reader = selected_live_reader

    def read_window(self, campaign_id: str, origin: str) -> tuple[object, str]:
        if origin == "LOCAL":
            pinned = self._pin_campaign(campaign_id)
            try:
                raw_window = self._repository.read_exact_path(pinned, _SEMANTIC_EVENT_PATH)
            except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
                raise HistoryContractError("campaign semantic-event window is unavailable") from exc
            return raw_window, pinned.revision

        if _LIVE_ORIGIN.fullmatch(origin) is None:
            raise HistoryContractError("native history origin is not admitted")
        route = self._current_routing
        reader = self._selected_live_reader
        if route is None or reader is None:
            raise HistoryContractError("selected LIVE source read capability is unavailable")
        source = _select_live_origin(route, campaign_id, origin)
        try:
            raw_window = reader.read_selected_live_source(route, source)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise HistoryContractError("selected LIVE semantic-event window is unavailable") from exc
        return raw_window, source.source_revision

    def _pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        try:
            pinned = self._repository.pin_campaign(campaign_id)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise HistoryContractError("exact campaign currentness is unavailable") from exc
        if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
            raise HistoryContractError("repository did not return the exact campaign pin")
        return pinned


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class BoundNativeHistoryRuntime:
    """Native-history service bound once by the trusted host composition root."""

    _window_adapter: _EvtLaneEnrollmentWindowAdapter

    def __init__(self, host_runtime: object) -> None:
        try:
            from .context_runtime import BoundContextRuntime
        except ImportError as exc:  # pragma: no cover - direct-path focused imports.
            raise HistoryContractError("native history host composition is unavailable") from exc
        context_runtime_types: tuple[type[object], ...] = (BoundContextRuntime,)
        direct_context_module = sys.modules.get("context_runtime")
        direct_context_type = getattr(direct_context_module, "BoundContextRuntime", None)
        if isinstance(direct_context_type, type) and direct_context_type is not BoundContextRuntime:
            context_runtime_types += (direct_context_type,)
        if not isinstance(host_runtime, context_runtime_types):
            raise HistoryContractError("native history runtime must be host-bound")
        try:
            repository = host_runtime._repository
            current_routing = host_runtime._live_route
            selected_live_reader = host_runtime._selected_live_reader
        except AttributeError as exc:
            raise HistoryContractError("native history host capabilities are unavailable") from exc
        if not hasattr(repository, "pin_campaign") or not hasattr(repository, "read_exact_path"):
            raise HistoryContractError("native history requires the trusted RepositoryPort")
        if current_routing is not None and not isinstance(current_routing, LiveRouting):
            raise HistoryContractError("native history current routing must be owner-typed")
        if selected_live_reader is not None and not _is_owner_issued_selected_live_read_capability(
            selected_live_reader
        ):
            raise HistoryContractError("native history LIVE reader must be owner-issued")
        if selected_live_reader is not None and current_routing is None:
            raise HistoryContractError("native history LIVE reader requires its selected route")
        object.__setattr__(
            self,
            "_window_adapter",
            _EvtLaneEnrollmentWindowAdapter(
                repository,
                current_routing,
                selected_live_reader,
            ),
        )

    def read(
        self,
        campaign_id: str,
        *,
        origin: str = "LOCAL",
    ) -> NativeHistoryPublication:
        """Read and validate one bounded native evt window from bound capabilities."""

        try:
            adapter = self._window_adapter
        except AttributeError as exc:
            raise HistoryContractError("native history runtime must be host-composed") from exc
        if not isinstance(adapter, _EvtLaneEnrollmentWindowAdapter):
            raise HistoryContractError("native history runtime must be host-composed")
        campaign = _nonempty_string(campaign_id, "native history campaign_id")
        checked_origin = _history_origin(origin)
        raw_window, expected_revision = adapter.read_window(campaign, checked_origin)
        return _issue_native_history_publication(
            raw_window,
            campaign_id=campaign,
            origin=checked_origin,
            expected_revision=expected_revision,
        )

    def recover(self, campaign_id: str, *, origin: str = "LOCAL") -> NativeHistoryPublication:
        """Recover only by re-reading the bound exact source window."""

        return self.read(campaign_id, origin=origin)


def read_native_history(
    runtime: BoundNativeHistoryRuntime,
    campaign_id: str,
    *,
    origin: str = "LOCAL",
) -> NativeHistoryPublication:
    """Read native history only through a host-bound runtime service."""

    if not isinstance(runtime, BoundNativeHistoryRuntime):
        raise HistoryContractError("native history requires a host-composed runtime")
    return runtime.read(campaign_id, origin=origin)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeHistoryCurrentness:
    """Ephemeral source/currentness basis issued by the bound history service."""

    campaign_id: str
    source_domain: str
    lane: str
    semantic_contract_generation: int
    origin: str
    source_revision: str
    lower_exclusive: int | None
    upper: int | None
    accepted_event_fingerprints: Mapping[str, str]

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native history currentness must be service-issued")

    def __post_init__(self) -> None:
        _nonempty_string(self.campaign_id, "native history campaign_id")
        if self.source_domain != _SOURCE_DOMAIN or self.lane != _SOURCE_LANE:
            raise HistoryContractError("native history source domain/lane is not admitted")
        if self.semantic_contract_generation != _SEMANTIC_CONTRACT_GENERATION:
            raise HistoryContractError("unsupported semantic history contract generation")
        _history_origin(self.origin)
        _git_revision(self.source_revision, "native history source_revision")
        if self.lower_exclusive is not None:
            _positive_int(self.lower_exclusive, "native history lower-exclusive ordinal")
        if self.upper is not None:
            _positive_int(self.upper, "native history upper ordinal")
        if self.upper is not None and self.upper <= (self.lower_exclusive or 0):
            raise HistoryContractError("native history interval is empty or reversed")
        if not isinstance(self.accepted_event_fingerprints, Mapping):
            raise HistoryContractError("accepted native event fingerprints must be an object")
        fingerprints: dict[str, str] = {}
        for event_id, fingerprint in self.accepted_event_fingerprints.items():
            _nonempty_string(event_id, "accepted native event identity")
            if not isinstance(fingerprint, str) or re.fullmatch(r"[a-f0-9]{64}", fingerprint) is None:
                raise HistoryContractError("accepted native event fingerprint must be SHA-256")
            fingerprints[event_id] = fingerprint
        object.__setattr__(self, "accepted_event_fingerprints", MappingProxyType(fingerprints))

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": _SOURCE_WINDOW_SCHEMA_VERSION,
            "campaign_id": self.campaign_id,
            "source_domain": self.source_domain,
            "lane": self.lane,
            "semantic_contract_generation": self.semantic_contract_generation,
            "origin": self.origin,
            "source_revision": self.source_revision,
            "lower_exclusive": (
                f"evt:{self.lower_exclusive}" if self.lower_exclusive is not None else None
            ),
            "upper": f"evt:{self.upper}" if self.upper is not None else None,
            "accepted_event_fingerprints": dict(self.accepted_event_fingerprints),
        }


_OWNER_ISSUED_HISTORY_CURRENTNESS: dict[
    int, weakref.ReferenceType[NativeHistoryCurrentness]
] = {}


def _mark_owner_issued_history_currentness(currentness: NativeHistoryCurrentness) -> None:
    currentness_id = id(currentness)

    def remove(reference: weakref.ReferenceType[NativeHistoryCurrentness]) -> None:
        if _OWNER_ISSUED_HISTORY_CURRENTNESS.get(currentness_id) is reference:
            _OWNER_ISSUED_HISTORY_CURRENTNESS.pop(currentness_id, None)

    _OWNER_ISSUED_HISTORY_CURRENTNESS[currentness_id] = weakref.ref(currentness, remove)


def _is_owner_issued_history_currentness(value: object) -> bool:
    reference = _OWNER_ISSUED_HISTORY_CURRENTNESS.get(id(value))
    return isinstance(value, NativeHistoryCurrentness) and reference is not None and reference() is value


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeSemanticEvent:
    """Ephemeral accepted SemanticEvent evidence bound to one source window."""

    event: Mapping[str, object]
    currentness: NativeHistoryCurrentness

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("accepted semantic events must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_history_currentness(self.currentness):
            raise HistoryContractError("accepted semantic event requires service-issued currentness")
        normalized = validate_semantic_event_draft(self.event)
        expected = self.currentness.accepted_event_fingerprints.get(normalized["event_id"])
        if expected != _semantic_event_fingerprint(normalized):
            raise HistoryContractError("semantic event is not bound to the exact source window")
        object.__setattr__(self, "event", _freeze_history_value(normalized))

    @property
    def event_id(self) -> str:
        return _nonempty_string(self.event["event_id"], "event_id")

    @property
    def candidate_id(self) -> str:
        return _candidate_id(self.event_id)

    @property
    def semantic_order(self) -> int:
        return _positive_int(self.event["semantic_order"], "semantic_order")

    @property
    def admission_ordinal(self) -> int:
        """The native evt admission ordinal, not chronology or causal order."""

        return self.semantic_order

    @property
    def provenance_refs(self) -> tuple[str, ...]:
        raw = self.event["provenance_refs"]
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            raise HistoryContractError("provenance_refs must be an array")
        return tuple(_nonempty_string(item, "provenance reference") for item in raw)

    @property
    def campaign_id(self) -> str:
        return self.currentness.campaign_id

    @property
    def source_domain(self) -> str:
        return self.currentness.source_domain

    @property
    def lane(self) -> str:
        return self.currentness.lane

    @property
    def origin(self) -> str:
        return self.currentness.origin

    @property
    def source_revision(self) -> str:
        return self.currentness.source_revision

    def __getitem__(self, key: str) -> object:
        return self.event[key]

    def as_mapping(self) -> dict[str, object]:
        return _thaw_history_value(self.event)

    def as_envelope(self) -> dict[str, object]:
        return {
            "event": self.as_mapping(),
            "provenance": {
                "campaign_id": self.campaign_id,
                "source_domain": self.source_domain,
                "lane": self.lane,
                "semantic_contract_generation": self.currentness.semantic_contract_generation,
                "origin": self.origin,
                "source_revision": self.source_revision,
                "event_id": self.event_id,
                "candidate_id": self.candidate_id,
                "admission_ordinal": self.admission_ordinal,
                "provenance_refs": list(self.provenance_refs),
            },
        }


_OWNER_ISSUED_NATIVE_EVENTS: dict[int, weakref.ReferenceType[NativeSemanticEvent]] = {}


def _mark_owner_issued_native_event(event: NativeSemanticEvent) -> None:
    event_id = id(event)

    def remove(reference: weakref.ReferenceType[NativeSemanticEvent]) -> None:
        if _OWNER_ISSUED_NATIVE_EVENTS.get(event_id) is reference:
            _OWNER_ISSUED_NATIVE_EVENTS.pop(event_id, None)

    _OWNER_ISSUED_NATIVE_EVENTS[event_id] = weakref.ref(event, remove)


def _is_owner_issued_native_event(value: object) -> bool:
    reference = _OWNER_ISSUED_NATIVE_EVENTS.get(id(value))
    return isinstance(value, NativeSemanticEvent) and reference is not None and reference() is value


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeHistoryPublication:
    """Ephemeral accepted history evidence over one validated source window."""

    currentness: NativeHistoryCurrentness
    events: tuple[NativeSemanticEvent, ...]

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native history publications must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_history_currentness(self.currentness):
            raise HistoryContractError("native history publication requires service-issued currentness")
        events = tuple(self.events)
        if any(not _is_owner_issued_native_event(event) for event in events):
            raise HistoryContractError("native history publication requires service-issued events")
        _validate_native_event_sequence(events, self.currentness)
        object.__setattr__(self, "events", events)

    @property
    def campaign_id(self) -> str:
        return self.currentness.campaign_id

    @property
    def source_domain(self) -> str:
        return self.currentness.source_domain

    @property
    def lane(self) -> str:
        return self.currentness.lane

    @property
    def semantic_contract_generation(self) -> int:
        return self.currentness.semantic_contract_generation

    @property
    def origin(self) -> str:
        return self.currentness.origin

    @property
    def source_revision(self) -> str:
        return self.currentness.source_revision

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": _SOURCE_WINDOW_SCHEMA_VERSION,
            "kind": _NATIVE_HISTORY_KIND,
            **self.currentness.as_mapping(),
            "events": [event.as_envelope() for event in self.events],
        }


_OWNER_ISSUED_HISTORY_PUBLICATIONS: dict[
    int, weakref.ReferenceType[NativeHistoryPublication]
] = {}


def _mark_owner_issued_history_publication(publication: NativeHistoryPublication) -> None:
    publication_id = id(publication)

    def remove(reference: weakref.ReferenceType[NativeHistoryPublication]) -> None:
        if _OWNER_ISSUED_HISTORY_PUBLICATIONS.get(publication_id) is reference:
            _OWNER_ISSUED_HISTORY_PUBLICATIONS.pop(publication_id, None)

    _OWNER_ISSUED_HISTORY_PUBLICATIONS[publication_id] = weakref.ref(publication, remove)


def _is_owner_issued_history_publication(value: object) -> bool:
    reference = _OWNER_ISSUED_HISTORY_PUBLICATIONS.get(id(value))
    return (
        isinstance(value, NativeHistoryPublication)
        and reference is not None
        and reference() is value
    )


def _issue_native_history_publication(
    raw_window: object,
    *,
    campaign_id: str,
    origin: str,
    expected_revision: str,
) -> NativeHistoryPublication:
    window = _validate_source_window(
        raw_window,
        campaign_id=campaign_id,
        origin=origin,
        expected_revision=expected_revision,
    )
    normalized_events = tuple(entry["event"] for entry in window["entries"])
    fingerprints = {
        event["event_id"]: _semantic_event_fingerprint(event) for event in normalized_events
    }
    currentness = object.__new__(NativeHistoryCurrentness)
    for name, value in {
        "campaign_id": campaign_id,
        "source_domain": _SOURCE_DOMAIN,
        "lane": _SOURCE_LANE,
        "semantic_contract_generation": _SEMANTIC_CONTRACT_GENERATION,
        "origin": origin,
        "source_revision": expected_revision,
        "lower_exclusive": window["lower_exclusive"],
        "upper": window["upper"],
        "accepted_event_fingerprints": fingerprints,
    }.items():
        object.__setattr__(currentness, name, value)
    NativeHistoryCurrentness.__post_init__(currentness)
    _mark_owner_issued_history_currentness(currentness)

    events: list[NativeSemanticEvent] = []
    for event in normalized_events:
        accepted = object.__new__(NativeSemanticEvent)
        object.__setattr__(accepted, "event", _freeze_history_value(event))
        object.__setattr__(accepted, "currentness", currentness)
        NativeSemanticEvent.__post_init__(accepted)
        _mark_owner_issued_native_event(accepted)
        events.append(accepted)

    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", currentness)
    object.__setattr__(publication, "events", tuple(events))
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_history_publication(publication)
    return publication


def append_semantic_event(
    history: NativeHistoryPublication,
    event: NativeSemanticEvent,
) -> NativeHistoryPublication:
    """Append only service-issued event evidence to an owner-issued publication."""

    if not _is_owner_issued_history_publication(history):
        raise HistoryContractError("native history append requires an owner-issued publication")
    if not _is_owner_issued_native_event(event):
        raise HistoryContractError("native history append requires an owner-issued event")
    if event.currentness != history.currentness:
        raise HistoryContractError("native history event currentness differs")
    if event.semantic_order <= history.events[-1].semantic_order:
        raise HistoryContractError("native history admission ordinal must advance")
    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", history.currentness)
    object.__setattr__(publication, "events", (*history.events, event))
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_history_publication(publication)
    return publication


def recover_native_history(
    runtime: BoundNativeHistoryRuntime | object,
    campaign_id: str | None = None,
    *,
    origin: str = "LOCAL",
) -> NativeHistoryPublication:
    """Recover by bounded re-read through the bound runtime, never caller bytes."""

    if not isinstance(runtime, BoundNativeHistoryRuntime) or campaign_id is None:
        raise HistoryContractError("native history recovery requires a host-composed runtime")
    return runtime.recover(campaign_id, origin=origin)


def validate_native_history(value: object) -> NativeHistoryPublication:
    """Validate only an already-issued ephemeral publication object."""

    if not _is_owner_issued_history_publication(value):
        raise HistoryContractError("native history validation requires service-issued evidence")
    return value


class HistoryObservationStatus(StrEnum):
    """Epistemic result of one bounded native-history observation."""

    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class FirstInitializationHistoryEvidence:
    """Verified creator evidence issued only by the native history owner."""

    campaign_id: str
    author_login: str
    initialization_revision: str
    parent_revision: str
    first_campaign_specific_commit: bool = True

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError(
            "first-initialization evidence must be issued by the native history owner"
        )

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "author_login": self.author_login,
            "initialization_revision": self.initialization_revision,
            "parent_revision": self.parent_revision,
            "first_campaign_specific_commit": True,
        }


@dataclass(frozen=True, slots=True)
class FirstInitializationHistoryObservation:
    """Bounded owner result used to admit creator authorization."""

    status: HistoryObservationStatus
    evidence: FirstInitializationHistoryEvidence | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.status, HistoryObservationStatus):
            raise HistoryContractError("history observation status must be owner-typed")
        if self.status is HistoryObservationStatus.AVAILABLE:
            if not _is_owner_issued_first_initialization_history(self.evidence):
                raise HistoryContractError("available history observation requires owner-issued evidence")
        elif self.evidence is not None:
            raise HistoryContractError("failed history observation cannot carry creator evidence")
        if not isinstance(self.reason, str) or not self.reason:
            raise HistoryContractError("history observation requires a failure or source reason")


_OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY: dict[
    int, weakref.ReferenceType[FirstInitializationHistoryEvidence]
] = {}


def _mark_owner_issued_first_initialization_history(
    evidence: FirstInitializationHistoryEvidence,
) -> None:
    evidence_id = id(evidence)

    def remove(reference: weakref.ReferenceType[FirstInitializationHistoryEvidence]) -> None:
        if _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY.get(evidence_id) is reference:
            _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY.pop(evidence_id, None)

    _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY[evidence_id] = weakref.ref(evidence, remove)


def _is_owner_issued_first_initialization_history(value: object) -> bool:
    if not isinstance(value, FirstInitializationHistoryEvidence):
        return False
    reference = _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY.get(id(value))
    return reference is not None and reference() is value


def observe_first_initialization_history(
    repository: RepositoryPort,
    campaign_id: str,
) -> FirstInitializationHistoryObservation:
    """Derive creator evidence from one bounded authenticated repository observation.

    The repository owner supplies only exact-ref/commit reads, bounded ancestry
    relations and authenticated per-user author evidence.  No caller fields,
    validator, callback or alternate port can issue or replace the result.
    """

    if not isinstance(campaign_id, str) or not campaign_id:
        return _unavailable("campaign identity is unavailable")

    try:
        ref_value = repository.read_exact_campaign_ref(campaign_id)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"exact campaign ref is unavailable: {exc}")
    try:
        ref = _campaign_ref_observation(ref_value, campaign_id)
    except HistoryContractError as exc:
        return _ambiguous(f"exact campaign ref is ambiguous: {exc}")

    try:
        commit_value = repository.read_exact_commit(
            ref["campaign_ref"], ref["initialization_revision"]
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"initialization commit is unavailable: {exc}")
    try:
        commit = _initialization_commit_observation(
            commit_value,
            campaign_id=campaign_id,
            initialization_revision=ref["initialization_revision"],
        )
    except HistoryContractError as exc:
        return _ambiguous(f"initialization commit is ambiguous: {exc}")

    try:
        default_relation_value = repository.compare_ancestry(
            ref["default_ref"], ref["default_head_revision"], commit["parent_revision"]
        )
        campaign_relation_value = repository.compare_ancestry(
            ref["campaign_ref"], ref["initialization_revision"], ref["campaign_head_revision"]
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"bounded ancestry evidence is unavailable: {exc}")
    try:
        default_relation = _ancestry_relation(default_relation_value, "default ancestry")
        campaign_relation = _ancestry_relation(campaign_relation_value, "campaign ancestry")
    except HistoryContractError as exc:
        return _ambiguous(f"bounded ancestry evidence is ambiguous: {exc}")
    if default_relation != "EQUAL":
        return _ambiguous("initialization parent is not the exact storage default HEAD")
    if campaign_relation not in {"EQUAL", "ANCESTOR"}:
        return _ambiguous("initialization commit is not a bounded ancestor of campaign HEAD")

    try:
        author_value = repository.read_authenticated_commit_author(
            ref["campaign_ref"], ref["initialization_revision"]
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"authenticated commit author is unavailable: {exc}")
    try:
        author_login = _authenticated_per_user_login(author_value)
    except HistoryContractError as exc:
        return _unavailable(f"authenticated per-user commit authorship is unavailable: {exc}")

    evidence = object.__new__(FirstInitializationHistoryEvidence)
    object.__setattr__(evidence, "campaign_id", campaign_id)
    object.__setattr__(evidence, "author_login", author_login)
    object.__setattr__(evidence, "initialization_revision", ref["initialization_revision"])
    object.__setattr__(evidence, "parent_revision", commit["parent_revision"])
    object.__setattr__(evidence, "first_campaign_specific_commit", True)
    _mark_owner_issued_first_initialization_history(evidence)
    return FirstInitializationHistoryObservation(
        HistoryObservationStatus.AVAILABLE,
        evidence=evidence,
        reason="authenticated first campaign-specific initialization commit",
    )


def resolve_creator_provenance(
    repository: RepositoryPort,
    campaign_id: str,
) -> FirstInitializationHistoryObservation:
    """Resolve creator evidence through the native history owner for access control."""

    return observe_first_initialization_history(repository, campaign_id)


def _unavailable(reason: str) -> FirstInitializationHistoryObservation:
    return FirstInitializationHistoryObservation(HistoryObservationStatus.UNAVAILABLE, reason=reason)


def _ambiguous(reason: str) -> FirstInitializationHistoryObservation:
    return FirstInitializationHistoryObservation(HistoryObservationStatus.AMBIGUOUS, reason=reason)


def _campaign_ref_observation(value: object, campaign_id: str) -> dict[str, str]:
    raw = _mapping(value, "campaign ref observation")
    expected = {
        "campaign_id",
        "campaign_ref",
        "campaign_head_revision",
        "default_ref",
        "default_head_revision",
        "initialization_revision",
    }
    if set(raw) != expected:
        raise HistoryContractError("campaign ref observation has unsupported or missing fields")
    observed_campaign_id = _nonempty_string(raw["campaign_id"], "campaign ref campaign_id")
    if observed_campaign_id != campaign_id:
        raise HistoryContractError("campaign ref belongs to another campaign")
    campaign_ref = _ref(raw["campaign_ref"], "campaign ref", campaign=True)
    default_ref = _ref(raw["default_ref"], "storage default ref", campaign=False)
    if default_ref.startswith("refs/heads/campaign/"):
        raise HistoryContractError("storage default ref cannot be a campaign ref")
    return {
        "campaign_ref": campaign_ref,
        "campaign_head_revision": _revision(raw["campaign_head_revision"], "campaign HEAD"),
        "default_ref": default_ref,
        "default_head_revision": _revision(raw["default_head_revision"], "storage default HEAD"),
        "initialization_revision": _revision(
            raw["initialization_revision"], "initialization revision"
        ),
    }


def _initialization_commit_observation(
    value: object,
    *,
    campaign_id: str,
    initialization_revision: str,
) -> dict[str, str]:
    raw = _mapping(value, "initialization commit observation")
    expected = {"campaign_id", "revision", "parent_revision", "campaign_specific"}
    if set(raw) != expected:
        raise HistoryContractError(
            "initialization commit observation has unsupported or missing fields"
        )
    if _nonempty_string(raw["campaign_id"], "initialization campaign_id") != campaign_id:
        raise HistoryContractError("initialization commit belongs to another campaign")
    if _revision(raw["revision"], "initialization commit revision") != initialization_revision:
        raise HistoryContractError("initialization commit revision does not match campaign ref")
    if type(raw["campaign_specific"]) is not bool or not raw["campaign_specific"]:
        raise HistoryContractError("initialization commit is not campaign-specific")
    parent_revision = _revision(raw["parent_revision"], "initialization parent revision")
    if parent_revision == initialization_revision:
        raise HistoryContractError("initialization commit must advance its parent")
    return {"parent_revision": parent_revision}


def _ancestry_relation(value: object, label: str) -> str:
    raw = _mapping(value, label)
    if set(raw) != {"relation"}:
        raise HistoryContractError(f"{label} has unsupported or missing fields")
    relation = raw["relation"]
    if relation not in {"EQUAL", "ANCESTOR", "NOT_ANCESTOR"}:
        raise HistoryContractError(f"{label} is not a bounded exact relation")
    return relation


def _authenticated_per_user_login(value: object) -> str:
    raw = _mapping(value, "authenticated commit author")
    expected = {"author", "authenticated", "per_user"}
    if set(raw) != expected:
        raise HistoryContractError("authenticated commit author has unsupported or missing fields")
    author = _mapping(raw["author"], "authenticated commit author identity")
    if set(author) != {"login"}:
        raise HistoryContractError("authenticated commit author identity has unsupported fields")
    if type(raw["authenticated"]) is not bool or not raw["authenticated"]:
        raise HistoryContractError("commit author authentication is not trustworthy")
    if type(raw["per_user"]) is not bool or not raw["per_user"]:
        raise HistoryContractError("commit author is not meaningful per-user authorship")
    return _nonempty_string(author["login"], "commit author.login")


def _ref(value: object, label: str, *, campaign: bool) -> str:
    if not isinstance(value, str) or (not _GIT_REF.fullmatch(value)):
        raise HistoryContractError(f"{label} must be an exact Git ref")
    if campaign and _CAMPAIGN_REF.fullmatch(value) is None:
        raise HistoryContractError(f"{label} must be an exact campaign ref")
    return value


def _git_revision(value: object, label: str) -> str:
    if not isinstance(value, str) or _GIT_REVISION.fullmatch(value) is None:
        raise HistoryContractError(f"{label} must be an exact lowercase Git revision")
    return value


def _revision(value: object, label: str) -> str:
    return _git_revision(value, label)


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise HistoryContractError(f"{label} must be an object")
    return value


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise HistoryContractError(f"{label} must be a nonempty string")
    return value


def _positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise HistoryContractError(f"{label} must be a positive integer")
    return value


def _schema_version(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value != 1:
        raise HistoryContractError("unsupported schema_version")
    return 1


def _unique_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise HistoryContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if not items or len(items) != len(set(items)):
        raise HistoryContractError(f"{label} must be nonempty and unique")
    return items


def _history_origin(value: object) -> str:
    origin = _nonempty_string(value, "native history origin")
    if origin != "LOCAL" and _LIVE_ORIGIN.fullmatch(origin) is None:
        raise HistoryContractError("native history origin must be LOCAL or a selected LIVE epoch")
    return origin


def _cursor(value: object, label: str, *, allow_none: bool = False) -> int | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str):
        raise HistoryContractError(f"{label} must be an evt cursor")
    match = _CURSOR.fullmatch(value)
    if match is None:
        raise HistoryContractError(f"{label} must be an unpadded positive evt cursor")
    return int(match.group(1))


def _candidate_id(event_id: str) -> str:
    try:
        return json.dumps([event_id], ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise HistoryContractError("semantic event identity is not canonical") from exc


def _semantic_event_fingerprint(event: Mapping[str, object]) -> str:
    try:
        encoded = json.dumps(
            _thaw_history_value(event),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise HistoryContractError("semantic event is not JSON-serializable") from exc
    return hashlib.sha256(encoded).hexdigest()


def _freeze_history_value(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_history_value(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze_history_value(item) for item in value)
    return value


def _thaw_history_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_history_value(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_thaw_history_value(item) for item in value]
    return value


def _select_live_origin(
    route: LiveRouting | None,
    campaign_id: str,
    origin: str,
) -> LiveEnvelope:
    if not isinstance(route, LiveRouting) or not route.complete or route.campaign_id != campaign_id:
        raise HistoryContractError("current LIVE routing is unavailable or stale")
    epoch_id = origin.removeprefix("LIVE:")
    matches = tuple(entry for entry in route.entries if entry.epoch_id == epoch_id)
    if len(matches) != 1:
        raise HistoryContractError("selected LIVE origin is missing or ambiguous")
    selected = select_live_source(route, matches[0].source_key)
    if selected is None or selected.epoch_id != epoch_id:
        raise HistoryContractError("selected LIVE origin is not current")
    return selected


def _validate_source_window(
    value: object,
    *,
    campaign_id: str,
    origin: str,
    expected_revision: str,
) -> dict[str, object]:
    window = _mapping(value, "native history source window")
    expected_fields = {
        "schema_version",
        "source_domain",
        "semantic_contract_generation",
        "campaign_id",
        "origin",
        "lane",
        "source_revision",
        "lower_exclusive",
        "upper",
        "enumeration_representation",
        "owner_contracts",
        "entries",
        "interval_complete",
    }
    if set(window) != expected_fields:
        raise HistoryContractError("native history source window fields are not strict")
    if window["schema_version"] != _SOURCE_WINDOW_SCHEMA_VERSION:
        raise HistoryContractError("unsupported native history source-window schema")
    if window["source_domain"] != _SOURCE_DOMAIN or window["lane"] != _SOURCE_LANE:
        raise HistoryContractError("native history source domain/lane differs")
    if window["semantic_contract_generation"] != _SEMANTIC_CONTRACT_GENERATION:
        raise HistoryContractError("unsupported native history semantic contract generation")
    if window["campaign_id"] != campaign_id or window["origin"] != origin:
        raise HistoryContractError("native history source identity or origin differs")
    source_revision = _git_revision(window["source_revision"], "native history source revision")
    if source_revision != expected_revision:
        raise HistoryContractError("native history source revision is stale")
    _nonempty_string(window["enumeration_representation"], "enumeration representation")
    _validate_owner_contracts(window["owner_contracts"])
    if window["interval_complete"] is not True:
        raise HistoryContractError("native history source interval is incomplete")
    lower = _cursor(window["lower_exclusive"], "lower-exclusive evt cursor", allow_none=True)
    upper = _cursor(window["upper"], "upper evt cursor", allow_none=True)
    if upper is None:
        if lower is not None or window["entries"] not in ([], ()):
            raise HistoryContractError("nonempty native history window requires an upper basis")
        return {"lower_exclusive": None, "upper": None, "entries": []}
    if lower is None:
        lower_value = 0
    else:
        lower_value = lower
    if upper <= lower_value:
        raise HistoryContractError("native history source interval is empty or reversed")
    raw_entries = window["entries"]
    if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
        raise HistoryContractError("native history source entries must be an array")

    entries: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    seen_ordinals: set[int] = set()
    for offset, raw_entry in enumerate(raw_entries, start=1):
        entry = _mapping(raw_entry, "native history source entry")
        if set(entry) != {"candidate_id", "ordinal", "event"}:
            raise HistoryContractError("native history source entry fields are not strict")
        ordinal = _positive_int(entry["ordinal"], "native history admission ordinal")
        if ordinal != lower_value + offset or ordinal > upper:
            raise HistoryContractError("native history evt interval is not contiguous")
        if ordinal in seen_ordinals:
            raise HistoryContractError("native history admission ordinal is duplicated")
        event = _mapping(entry["event"], "native history source event")
        normalized = validate_semantic_event_draft(event)
        if normalized["semantic_order"] != ordinal:
            raise HistoryContractError("semantic event order is not its evt admission ordinal")
        candidate_id = entry["candidate_id"]
        if candidate_id != _candidate_id(normalized["event_id"]):
            raise HistoryContractError("native history candidate identity does not bind event")
        if candidate_id in seen_ids:
            raise HistoryContractError("native history candidate identity is duplicated")
        seen_ids.add(candidate_id)
        seen_ordinals.add(ordinal)
        entries.append({"candidate_id": candidate_id, "ordinal": ordinal, "event": normalized})
    if not entries or entries[-1]["ordinal"] != upper:
        raise HistoryContractError("native history source window does not prove its upper basis")
    return {
        "lower_exclusive": lower,
        "upper": upper,
        "entries": entries,
    }


def _validate_owner_contracts(value: object) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 1:
        raise HistoryContractError("native history owner contracts must name one exact owner")
    contract = _mapping(value[0], "native history owner contract")
    if set(contract) != {"family", "schema_version"}:
        raise HistoryContractError("native history owner contract fields are not strict")
    if contract["family"] != "runtime.semantic_event" or contract["schema_version"] != 1:
        raise HistoryContractError("native history owner contract is unsupported")


def _validate_native_event_sequence(
    events: Sequence[NativeSemanticEvent],
    currentness: NativeHistoryCurrentness,
) -> None:
    previous: int | None = None
    seen_ids: set[str] = set()
    for event in events:
        if not _is_owner_issued_native_event(event) or event.currentness != currentness:
            raise HistoryContractError("native history sequence contains foreign event evidence")
        if event.event_id in seen_ids:
            raise HistoryContractError("native history event identity is duplicated")
        if previous is not None and event.admission_ordinal <= previous:
            raise HistoryContractError("native history admission ordinals are not increasing")
        seen_ids.add(event.event_id)
        previous = event.admission_ordinal


def validate_semantic_event_draft(value: object) -> dict[str, object]:
    """Validate the compact accepted semantic event that owns history meaning."""

    event = _mapping(value, "semantic event")
    expected = {
        "schema_version",
        "event_id",
        "semantic_order",
        "kind",
        "provenance_refs",
        "semantic_delta",
    }
    if set(event) != expected:
        raise HistoryContractError("semantic event has unsupported or missing fields")
    if not isinstance(event["semantic_delta"], Mapping):
        raise HistoryContractError("semantic_delta must be an object")
    return {
        "schema_version": _schema_version(event["schema_version"]),
        "event_id": _nonempty_string(event["event_id"], "event_id"),
        "semantic_order": _positive_int(event["semantic_order"], "semantic_order"),
        "kind": _nonempty_string(event["kind"], "kind"),
        "provenance_refs": _unique_strings(event["provenance_refs"], "provenance_refs"),
        "semantic_delta": deepcopy(dict(event["semantic_delta"])),
    }


def validate_t0_basis(value: object) -> dict[str, object]:
    """Validate bounded retained T0 factors without reading mutable T1 state."""

    basis = _mapping(value, "T0 basis")
    if set(basis) != {"schema_version", "event_id", "actor_id", "factors"}:
        raise HistoryContractError("T0 basis has unsupported or missing fields")
    raw_factors = basis["factors"]
    if not isinstance(raw_factors, Sequence) or isinstance(raw_factors, str) or not raw_factors:
        raise HistoryContractError("T0 factors must be a nonempty array")
    factors: list[dict[str, object]] = []
    factor_ids: set[str] = set()
    for raw_factor in raw_factors:
        factor = _mapping(raw_factor, "T0 factor")
        if set(factor) != {"owner_family", "factor_id", "t0_value", "provenance_refs"}:
            raise HistoryContractError("T0 factor has unsupported or missing fields")
        factor_id = _nonempty_string(factor["factor_id"], "factor_id")
        if factor_id in factor_ids:
            raise HistoryContractError("T0 factor identities must be unique")
        factor_ids.add(factor_id)
        factors.append(
            {
                "owner_family": _nonempty_string(factor["owner_family"], "owner_family"),
                "factor_id": factor_id,
                "t0_value": deepcopy(factor["t0_value"]),
                "provenance_refs": _unique_strings(factor["provenance_refs"], "provenance_refs"),
            }
        )
    return {
        "schema_version": _schema_version(basis["schema_version"]),
        "event_id": _nonempty_string(basis["event_id"], "event_id"),
        "actor_id": _nonempty_string(basis["actor_id"], "actor_id"),
        "factors": factors,
    }


def build_t0_basis(event: object, basis: object) -> dict[str, object]:
    """Bind retained factors to their accepted native SemanticEvent."""

    event_value = validate_semantic_event_draft(event)
    basis_value = validate_t0_basis(basis)
    if basis_value["event_id"] != event_value["event_id"]:
        raise HistoryContractError("T0 basis must bind its accepted semantic event")
    return basis_value
