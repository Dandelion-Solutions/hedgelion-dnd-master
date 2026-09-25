"""Owner-native semantic history and retained event-time decision basis."""

from __future__ import annotations

import hashlib
import json
import re
import weakref
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .policy_basis import RepositoryPort


_GIT_REVISION: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_GIT_REF: Final = re.compile(r"^refs/heads/[^\s/]+(?:/[^\s/]+)*$")
_CAMPAIGN_REF: Final = re.compile(r"^refs/heads/campaign/[^\s/]+$")
_LIVE_ORIGIN: Final = re.compile(r"^LIVE:[A-Za-z0-9_.:-]+$")
_HISTORY_SOURCE_DOMAIN: Final[str] = "campaign.semantic_events@S"
_HISTORY_LANE: Final[str] = "evt"
_HISTORY_CONTRACT_GENERATION: Final[int] = 1
T0_BASIS_SCHEMA_VERSION: Final[int] = 2
T0_AVAILABILITY_CLASSIFICATIONS: Final[frozenset[str]] = frozenset(
    {"PUBLIC", "PROTECTED"}
)
_T0_FACTOR_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "owner_family",
        "factor_id",
        "t0_value",
        "provenance_refs",
        "availability_classification",
    }
)
_NATIVE_HISTORY_KIND: Final[str] = "runtime.native_history"
_MISSING_HOST_TOKEN: Final[object] = object()

# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.5"


class HistoryContractError(ValueError):
    """Raised when a caller supplies invalid native history material."""


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeHistoryCurrentness:
    """Ephemeral currentness issued from one exact adapter source window."""

    campaign_id: str
    source_domain: str
    lane: str
    semantic_contract_generation: int
    origin: str
    source_ref: str
    source_revision: str
    lower_exclusive_ordinal: int | None
    upper_ordinal: int | None
    accepted_event_fingerprints: Mapping[str, str]

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native history currentness must be service-issued")

    def __post_init__(self) -> None:
        _nonempty_string(self.campaign_id, "native history campaign_id")
        if self.source_domain != _HISTORY_SOURCE_DOMAIN:
            raise HistoryContractError("native history source domain is not admitted")
        if self.lane != _HISTORY_LANE:
            raise HistoryContractError("native history lane is not admitted")
        if self.semantic_contract_generation != _HISTORY_CONTRACT_GENERATION:
            raise HistoryContractError("unsupported native history contract generation")
        _history_origin(self.origin)
        _history_source_ref(self.source_ref)
        _git_revision(self.source_revision, "native history source revision")
        lower = self.lower_exclusive_ordinal
        if lower is not None and (type(lower) is not int or lower < 0):
            raise HistoryContractError(
                "lower-exclusive evt ordinal must be null or non-negative"
            )
        upper = self.upper_ordinal
        if upper is not None and (type(upper) is not int or upper < 1):
            raise HistoryContractError("upper evt ordinal must be null or positive")
        if upper is not None and upper <= (lower or 0):
            raise HistoryContractError("native history interval is empty or reversed")
        if not isinstance(self.accepted_event_fingerprints, Mapping):
            raise HistoryContractError(
                "native history event fingerprints must be an object"
            )
        fingerprints: dict[str, str] = {}
        for event_id, fingerprint in self.accepted_event_fingerprints.items():
            _nonempty_string(event_id, "accepted native event identity")
            if (
                not isinstance(fingerprint, str)
                or re.fullmatch(r"[a-f0-9]{64}", fingerprint) is None
            ):
                raise HistoryContractError(
                    "native history event fingerprint must be SHA-256"
                )
            fingerprints[event_id] = fingerprint
        object.__setattr__(
            self, "accepted_event_fingerprints", MappingProxyType(fingerprints)
        )

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "campaign_id": self.campaign_id,
            "source_domain": self.source_domain,
            "lane": self.lane,
            "semantic_contract_generation": self.semantic_contract_generation,
            "origin": self.origin,
            "source_ref": self.source_ref,
            "source_revision": self.source_revision,
            "lower_exclusive_ordinal": self.lower_exclusive_ordinal,
            "upper_ordinal": self.upper_ordinal,
            "accepted_event_fingerprints": dict(self.accepted_event_fingerprints),
        }


_OWNER_ISSUED_HISTORY_CURRENTNESS: dict[
    int, weakref.ReferenceType[NativeHistoryCurrentness]
] = {}


def _mark_owner_issued_currentness(value: NativeHistoryCurrentness) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeHistoryCurrentness]) -> None:
        if _OWNER_ISSUED_HISTORY_CURRENTNESS.get(value_id) is reference:
            _OWNER_ISSUED_HISTORY_CURRENTNESS.pop(value_id, None)

    _OWNER_ISSUED_HISTORY_CURRENTNESS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_currentness(value: object) -> bool:
    reference = _OWNER_ISSUED_HISTORY_CURRENTNESS.get(id(value))
    return (
        isinstance(value, NativeHistoryCurrentness)
        and reference is not None
        and reference() is value
    )


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeSemanticEvent:
    """Ephemeral event evidence bound to one exact native source window."""

    event: Mapping[str, object]
    currentness: NativeHistoryCurrentness
    admission_ordinal: int

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native semantic events must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_currentness(self.currentness):
            raise HistoryContractError(
                "native event requires service-issued currentness"
            )
        normalized = validate_semantic_event_draft(self.event)
        if type(self.admission_ordinal) is not int or self.admission_ordinal < 1:
            raise HistoryContractError(
                "native event admission ordinal must be positive"
            )
        if normalized["semantic_order"] != self.admission_ordinal:
            raise HistoryContractError(
                "generation-1 semantic_order must equal evt admission ordinal"
            )
        expected = self.currentness.accepted_event_fingerprints.get(
            normalized["event_id"]
        )
        if expected != _semantic_event_fingerprint(normalized):
            raise HistoryContractError(
                "native event is not bound to the exact source window"
            )
        object.__setattr__(self, "event", _freeze_history_value(normalized))

    @property
    def event_id(self) -> str:
        return _nonempty_string(self.event["event_id"], "native event_id")

    @property
    def semantic_order(self) -> int:
        return _positive_int(self.event["semantic_order"], "native semantic_order")

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
    def source_ref(self) -> str:
        return self.currentness.source_ref

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
                "source_ref": self.source_ref,
                "source_revision": self.source_revision,
                "event_id": self.event_id,
                "admission_ordinal": self.admission_ordinal,
                "provenance_refs": list(self.event["provenance_refs"]),
            },
        }


_OWNER_ISSUED_NATIVE_EVENTS: dict[int, weakref.ReferenceType[NativeSemanticEvent]] = {}


def _mark_owner_issued_event(value: NativeSemanticEvent) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeSemanticEvent]) -> None:
        if _OWNER_ISSUED_NATIVE_EVENTS.get(value_id) is reference:
            _OWNER_ISSUED_NATIVE_EVENTS.pop(value_id, None)

    _OWNER_ISSUED_NATIVE_EVENTS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_event(value: object) -> bool:
    reference = _OWNER_ISSUED_NATIVE_EVENTS.get(id(value))
    return (
        isinstance(value, NativeSemanticEvent)
        and reference is not None
        and reference() is value
    )


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class NativeHistoryPublication:
    """Ephemeral native history issued from one validated evt window."""

    currentness: NativeHistoryCurrentness
    events: tuple[NativeSemanticEvent, ...]

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native history publications must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_currentness(self.currentness):
            raise HistoryContractError(
                "native publication requires service-issued currentness"
            )
        events = tuple(self.events)
        if any(not _is_owner_issued_event(event) for event in events):
            raise HistoryContractError(
                "native publication requires service-issued events"
            )
        if any(event.currentness is not self.currentness for event in events):
            raise HistoryContractError(
                "native publication events have foreign currentness"
            )
        event_ids = {event.event_id for event in events}
        if event_ids != set(self.currentness.accepted_event_fingerprints):
            raise HistoryContractError(
                "native publication does not cover its exact source window"
            )
        expected_ordinal = (self.currentness.lower_exclusive_ordinal or 0) + 1
        for event in events:
            if event.admission_ordinal != expected_ordinal:
                raise HistoryContractError(
                    "native publication evt interval is not contiguous"
                )
            expected_ordinal += 1
        upper = self.currentness.upper_ordinal
        if upper is None:
            if events:
                raise HistoryContractError(
                    "empty native publication has event evidence"
                )
        elif expected_ordinal - 1 != upper:
            raise HistoryContractError(
                "native publication does not prove its upper basis"
            )
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
    def source_ref(self) -> str:
        return self.currentness.source_ref

    @property
    def source_revision(self) -> str:
        return self.currentness.source_revision

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "kind": _NATIVE_HISTORY_KIND,
            **self.currentness.as_mapping(),
            "events": [event.as_envelope() for event in self.events],
        }


_OWNER_ISSUED_HISTORY_PUBLICATIONS: dict[
    int, weakref.ReferenceType[NativeHistoryPublication]
] = {}


def _mark_owner_issued_publication(value: NativeHistoryPublication) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeHistoryPublication]) -> None:
        if _OWNER_ISSUED_HISTORY_PUBLICATIONS.get(value_id) is reference:
            _OWNER_ISSUED_HISTORY_PUBLICATIONS.pop(value_id, None)

    _OWNER_ISSUED_HISTORY_PUBLICATIONS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_publication(value: object) -> bool:
    reference = _OWNER_ISSUED_HISTORY_PUBLICATIONS.get(id(value))
    return (
        isinstance(value, NativeHistoryPublication)
        and reference is not None
        and reference() is value
    )


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
                raise HistoryContractError(
                    "available history observation requires owner-issued evidence"
                )
        elif self.evidence is not None:
            raise HistoryContractError(
                "failed history observation cannot carry creator evidence"
            )
        if not isinstance(self.reason, str) or not self.reason:
            raise HistoryContractError(
                "history observation requires a failure or source reason"
            )


_OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY: dict[
    int, weakref.ReferenceType[FirstInitializationHistoryEvidence]
] = {}


def _mark_owner_issued_first_initialization_history(
    evidence: FirstInitializationHistoryEvidence,
) -> None:
    evidence_id = id(evidence)

    def remove(
        reference: weakref.ReferenceType[FirstInitializationHistoryEvidence],
    ) -> None:
        if _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY.get(evidence_id) is reference:
            _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY.pop(evidence_id, None)

    _OWNER_ISSUED_FIRST_INITIALIZATION_HISTORY[evidence_id] = weakref.ref(
        evidence, remove
    )


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
            ref["campaign_ref"],
            ref["initialization_revision"],
            ref["campaign_head_revision"],
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"bounded ancestry evidence is unavailable: {exc}")
    try:
        default_relation = _ancestry_relation(
            default_relation_value, "default ancestry"
        )
        campaign_relation = _ancestry_relation(
            campaign_relation_value, "campaign ancestry"
        )
    except HistoryContractError as exc:
        return _ambiguous(f"bounded ancestry evidence is ambiguous: {exc}")
    if default_relation != "EQUAL":
        return _ambiguous("initialization parent is not the exact storage default HEAD")
    if campaign_relation not in {"EQUAL", "ANCESTOR"}:
        return _ambiguous(
            "initialization commit is not a bounded ancestor of campaign HEAD"
        )

    try:
        author_value = repository.read_authenticated_commit_author(
            ref["campaign_ref"], ref["initialization_revision"]
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        return _unavailable(f"authenticated commit author is unavailable: {exc}")
    try:
        author_login = _authenticated_per_user_login(author_value)
    except HistoryContractError as exc:
        return _unavailable(
            f"authenticated per-user commit authorship is unavailable: {exc}"
        )

    evidence = object.__new__(FirstInitializationHistoryEvidence)
    object.__setattr__(evidence, "campaign_id", campaign_id)
    object.__setattr__(evidence, "author_login", author_login)
    object.__setattr__(
        evidence, "initialization_revision", ref["initialization_revision"]
    )
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


def _read_bound_native_history(
    *,
    source_adapter: object,
    basis: object,
    origin: str,
    lower_exclusive_ordinal: int | None = None,
    max_items: int = 1000,
) -> NativeHistoryPublication:
    """Validate and issue history from this RuntimeHost's bound adapter output."""
    checked_origin = _history_origin(origin)
    try:
        from .runtime_host import (
            SemanticEventSourceAdapter,
            _is_adapter_issued_evt_window,
            _OperationBasis,
        )
    except ImportError as exc:  # pragma: no cover - package wiring failure
        raise HistoryContractError(
            "RuntimeHost evt source adapter is unavailable"
        ) from exc
    if not isinstance(source_adapter, SemanticEventSourceAdapter):
        raise HistoryContractError(
            "native history requires the bound RuntimeHost adapter"
        )
    if not isinstance(basis, _OperationBasis):
        raise HistoryContractError(
            "native history requires the exact RuntimeHost basis"
        )
    host = source_adapter._host
    if host._basis_token is not basis.host_token:
        raise HistoryContractError(
            "native history adapter and basis belong to different hosts"
        )
    try:
        if checked_origin == "LOCAL":
            raw_window = source_adapter.read_local_evt_window(
                lower_exclusive_ordinal=lower_exclusive_ordinal,
                max_items=max_items,
                _basis=basis,
            )
        else:
            raw_window = source_adapter.read_selected_live_evt_window(
                origin=checked_origin,
                lower_exclusive_ordinal=lower_exclusive_ordinal,
                max_items=max_items,
                _basis=basis,
            )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise HistoryContractError(
            "bound native history evt window is unavailable"
        ) from exc
    if not _is_adapter_issued_evt_window(raw_window, host_token=basis.host_token):
        raise HistoryContractError("RuntimeHost did not issue the native evt window")

    if checked_origin == "LOCAL":
        expected_source_ref = raw_window.source_ref
        expected_source_revision = basis.pinned_campaign.revision
    else:
        routing = basis.selected_live
        if routing is None or not routing.complete:
            raise HistoryContractError(
                "selected LIVE route is unavailable or incomplete"
            )
        epoch_id = checked_origin.removeprefix("LIVE:")
        matches = tuple(
            entry for entry in routing.entries if entry.epoch_id == epoch_id
        )
        if len(matches) != 1:
            raise HistoryContractError("selected LIVE origin is missing or ambiguous")
        from .live_state import select_live_source

        source = select_live_source(routing, matches[0].source_key)
        if source is None or source.epoch_id != epoch_id:
            raise HistoryContractError("selected LIVE source is no longer current")
        expected_source_ref = source.source_ref
        expected_source_revision = source.source_revision

    return _issue_native_history_from_window(
        raw_window,
        campaign_id=basis.pinned_campaign.campaign_id,
        expected_origin=checked_origin,
        expected_source_ref=expected_source_ref,
        expected_source_revision=expected_source_revision,
        _expected_host_token=basis.host_token,
    )


def read_native_history_window(
    host: object,
    *,
    origin: str = "LOCAL",
    lower_exclusive_ordinal: int | None = None,
    max_items: int = 1000,
    _basis: object | None = None,
) -> NativeHistoryPublication:
    """Read one bounded, owner-issued native history interval through RuntimeHost."""
    try:
        from .runtime_host import RuntimeHost, _OperationBasis
    except ImportError as exc:  # pragma: no cover - package wiring failure
        raise HistoryContractError("RuntimeHost history route is unavailable") from exc
    if not isinstance(host, RuntimeHost):
        raise HistoryContractError("native history requires a bound RuntimeHost")
    if _basis is None:
        basis = host._begin_operation()
    elif isinstance(_basis, _OperationBasis):
        basis = _basis
    else:
        raise HistoryContractError("native history basis is not owner-typed")
    if basis.host_token is not host._basis_token:
        raise HistoryContractError("native history basis belongs to another host")
    return _read_bound_native_history(
        source_adapter=host.semantic_events,
        basis=basis,
        origin=origin,
        lower_exclusive_ordinal=lower_exclusive_ordinal,
        max_items=max_items,
    )


def _issue_native_history_from_window(
    source_window: object,
    *,
    campaign_id: str,
    expected_origin: str,
    expected_source_ref: str,
    expected_source_revision: str,
    _expected_host_token: object = _MISSING_HOST_TOKEN,
) -> NativeHistoryPublication:
    """Issue native history only from one RuntimeHost adapter evt window.

    The RuntimeHost ``SemanticEventSourceAdapter`` is the sole producer of the
    accepted raw window. This internal boundary is not a gameplay API and does
    not accept a repository, LIVE transport, aggregate log or adapter override.
    """

    try:
        from .runtime_host import EvtSourceWindow, _is_adapter_issued_evt_window
    except ImportError as exc:  # pragma: no cover - package wiring failure
        raise HistoryContractError(
            "RuntimeHost evt source adapter is unavailable"
        ) from exc
    if _expected_host_token is _MISSING_HOST_TOKEN or _expected_host_token is None:
        raise HistoryContractError(
            "native history requires its bound RuntimeHost token"
        )
    if not isinstance(
        source_window, EvtSourceWindow
    ) or not _is_adapter_issued_evt_window(
        source_window, host_token=_expected_host_token
    ):
        raise HistoryContractError(
            "native history requires an adapter-issued evt window"
        )

    campaign = _nonempty_string(campaign_id, "native history campaign_id")
    origin = _history_origin(expected_origin)
    source_ref = _history_source_ref(expected_source_ref)
    source_revision = _git_revision(
        expected_source_revision, "native history source revision"
    )
    if source_window.campaign_id != campaign:
        raise HistoryContractError("native history window belongs to another campaign")
    if source_window.origin != origin:
        raise HistoryContractError(
            "native history window origin differs from selected source"
        )
    if source_window.source_ref != source_ref:
        raise HistoryContractError(
            "native history window ref differs from selected source"
        )
    if source_window.source_revision != source_revision:
        raise HistoryContractError("native history window revision is stale")
    if source_window.lane != _HISTORY_LANE:
        raise HistoryContractError("native history window lane is not evt")
    if source_window.interval_complete_through_upper is not True:
        raise HistoryContractError("native history window does not prove completeness")

    lower = source_window.lower_exclusive_ordinal
    upper = source_window.upper_ordinal
    if lower is not None and (type(lower) is not int or lower < 0):
        raise HistoryContractError("native history lower ordinal is invalid")
    if upper is not None and (type(upper) is not int or upper < 1):
        raise HistoryContractError("native history upper ordinal is invalid")
    if upper is not None and upper <= (lower or 0):
        raise HistoryContractError("native history interval is empty or reversed")

    raw_entries = tuple(source_window.entries)
    if upper is None:
        if lower is not None or raw_entries:
            raise HistoryContractError(
                "empty native history window has an invalid basis"
            )
        normalized_events: list[tuple[int, dict[str, object]]] = []
    else:
        normalized_events = []
        expected_ordinal = (lower or 0) + 1
        seen_event_ids: set[str] = set()
        for raw_entry in raw_entries:
            if not isinstance(raw_entry, Mapping) or set(raw_entry) != {
                "ordinal",
                "event_id",
                "event_record",
            }:
                raise HistoryContractError(
                    "native history evt entry fields are not strict"
                )
            ordinal = raw_entry["ordinal"]
            if type(ordinal) is not int or ordinal != expected_ordinal:
                raise HistoryContractError(
                    "native history evt interval is not contiguous"
                )
            event_id = _nonempty_string(
                raw_entry["event_id"], "native history event_id"
            )
            if event_id in seen_event_ids:
                raise HistoryContractError(
                    "native history event identity is duplicated"
                )
            record = raw_entry["event_record"]
            if not isinstance(record, Mapping) or record.get("event_id") != event_id:
                raise HistoryContractError(
                    "native history event identity differs from record"
                )
            normalized = validate_semantic_event_draft(record)
            if normalized["semantic_order"] != ordinal:
                raise HistoryContractError(
                    "generation-1 semantic_order must equal evt admission ordinal"
                )
            seen_event_ids.add(event_id)
            normalized_events.append((ordinal, normalized))
            expected_ordinal += 1
        if not normalized_events or normalized_events[-1][0] != upper:
            raise HistoryContractError(
                "native history window does not prove its upper basis"
            )

    currentness = _issue_history_currentness(
        campaign_id=campaign,
        origin=origin,
        source_ref=source_ref,
        source_revision=source_revision,
        lower_exclusive_ordinal=lower,
        upper_ordinal=upper,
        events=[event for _ordinal, event in normalized_events],
    )
    events = tuple(
        _issue_native_event(event, currentness=currentness, admission_ordinal=ordinal)
        for ordinal, event in normalized_events
    )
    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", currentness)
    object.__setattr__(publication, "events", events)
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_publication(publication)
    return publication


def recover_native_history(
    value: object,
    *,
    currentness: NativeHistoryCurrentness,
) -> NativeHistoryPublication:
    """Recover an ephemeral publication only against its exact currentness."""

    if not _is_owner_issued_currentness(currentness):
        raise HistoryContractError(
            "native history recovery requires owner-issued currentness"
        )
    if _is_owner_issued_publication(value):
        if value.currentness is not currentness:
            raise HistoryContractError("native history recovery currentness differs")
        return value
    envelope = _mapping(value, "native history recovery")
    expected_fields = {
        "schema_version",
        "kind",
        "campaign_id",
        "source_domain",
        "lane",
        "semantic_contract_generation",
        "origin",
        "source_ref",
        "source_revision",
        "lower_exclusive_ordinal",
        "upper_ordinal",
        "accepted_event_fingerprints",
        "events",
    }
    if set(envelope) != expected_fields:
        raise HistoryContractError("native history recovery fields are not strict")
    if envelope["schema_version"] != 1 or envelope["kind"] != _NATIVE_HISTORY_KIND:
        raise HistoryContractError("unsupported native history recovery envelope")
    if envelope["campaign_id"] != currentness.campaign_id:
        raise HistoryContractError("native history recovery campaign differs")
    current_mapping = currentness.as_mapping()
    for field_name in current_mapping:
        if envelope[field_name] != current_mapping[field_name]:
            raise HistoryContractError("native history recovery currentness differs")

    raw_events = envelope["events"]
    if not isinstance(raw_events, Sequence) or isinstance(raw_events, (str, bytes)):
        raise HistoryContractError("native history recovery events must be an array")
    recovered: list[NativeSemanticEvent] = []
    for raw_item in raw_events:
        item = _mapping(raw_item, "native history event envelope")
        if set(item) != {"event", "provenance"}:
            raise HistoryContractError(
                "native history event envelope fields are not strict"
            )
        event = validate_semantic_event_draft(item["event"])
        provenance = _mapping(item["provenance"], "native history event provenance")
        expected_provenance = {
            "campaign_id",
            "source_domain",
            "lane",
            "semantic_contract_generation",
            "origin",
            "source_ref",
            "source_revision",
            "event_id",
            "admission_ordinal",
            "provenance_refs",
        }
        if set(provenance) != expected_provenance:
            raise HistoryContractError(
                "native history provenance fields are not strict"
            )
        if (
            provenance["campaign_id"] != currentness.campaign_id
            or provenance["source_domain"] != currentness.source_domain
            or provenance["lane"] != currentness.lane
            or provenance["semantic_contract_generation"]
            != currentness.semantic_contract_generation
            or provenance["origin"] != currentness.origin
            or provenance["source_ref"] != currentness.source_ref
            or provenance["source_revision"] != currentness.source_revision
            or provenance["event_id"] != event["event_id"]
            or provenance["provenance_refs"] != event["provenance_refs"]
        ):
            raise HistoryContractError(
                "native history provenance does not bind its event"
            )
        admission_ordinal = provenance["admission_ordinal"]
        recovered.append(
            _issue_native_event(
                event,
                currentness=currentness,
                admission_ordinal=admission_ordinal,
            )
        )

    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", currentness)
    object.__setattr__(publication, "events", tuple(recovered))
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_publication(publication)
    return publication


def validate_native_history(
    value: object,
    *,
    currentness: NativeHistoryCurrentness,
) -> NativeHistoryPublication:
    """Validate one recovered native-history publication envelope."""

    return recover_native_history(value, currentness=currentness)


def _issue_history_currentness(
    *,
    campaign_id: str,
    origin: str,
    source_ref: str,
    source_revision: str,
    lower_exclusive_ordinal: int | None,
    upper_ordinal: int | None,
    events: Sequence[Mapping[str, object]],
) -> NativeHistoryCurrentness:
    fingerprints: dict[str, str] = {}
    for event in events:
        normalized = validate_semantic_event_draft(event)
        event_id = normalized["event_id"]
        if event_id in fingerprints:
            raise HistoryContractError("native history event identities must be unique")
        fingerprints[event_id] = _semantic_event_fingerprint(normalized)
    currentness = object.__new__(NativeHistoryCurrentness)
    for field_name, field_value in {
        "campaign_id": campaign_id,
        "source_domain": _HISTORY_SOURCE_DOMAIN,
        "lane": _HISTORY_LANE,
        "semantic_contract_generation": _HISTORY_CONTRACT_GENERATION,
        "origin": origin,
        "source_ref": source_ref,
        "source_revision": source_revision,
        "lower_exclusive_ordinal": lower_exclusive_ordinal,
        "upper_ordinal": upper_ordinal,
        "accepted_event_fingerprints": fingerprints,
    }.items():
        object.__setattr__(currentness, field_name, field_value)
    NativeHistoryCurrentness.__post_init__(currentness)
    _mark_owner_issued_currentness(currentness)
    return currentness


def _issue_native_event(
    event: Mapping[str, object],
    *,
    currentness: NativeHistoryCurrentness,
    admission_ordinal: object,
) -> NativeSemanticEvent:
    accepted = object.__new__(NativeSemanticEvent)
    object.__setattr__(accepted, "event", event)
    object.__setattr__(accepted, "currentness", currentness)
    object.__setattr__(accepted, "admission_ordinal", admission_ordinal)
    NativeSemanticEvent.__post_init__(accepted)
    _mark_owner_issued_event(accepted)
    return accepted


def _history_origin(value: object) -> str:
    origin = _nonempty_string(value, "native history origin")
    if origin != "LOCAL" and _LIVE_ORIGIN.fullmatch(origin) is None:
        raise HistoryContractError(
            "native history origin must be LOCAL or a selected LIVE origin"
        )
    return origin


def _history_source_ref(value: object) -> str:
    source_ref = _nonempty_string(value, "native history source ref")
    if any(character.isspace() for character in source_ref):
        raise HistoryContractError(
            "native history source ref must not contain whitespace"
        )
    return source_ref


def _freeze_history_value(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_history_value(item) for key, item in value.items()}
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze_history_value(item) for item in value)
    return value


def _thaw_history_value(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_history_value(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_thaw_history_value(item) for item in value]
    return value


def _semantic_event_fingerprint(event: Mapping[str, object]) -> str:
    try:
        encoded = json.dumps(
            _thaw_history_value(event),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise HistoryContractError(
            "native semantic event is not JSON-serializable"
        ) from exc
    return hashlib.sha256(encoded).hexdigest()


def _unavailable(reason: str) -> FirstInitializationHistoryObservation:
    return FirstInitializationHistoryObservation(
        HistoryObservationStatus.UNAVAILABLE, reason=reason
    )


def _ambiguous(reason: str) -> FirstInitializationHistoryObservation:
    return FirstInitializationHistoryObservation(
        HistoryObservationStatus.AMBIGUOUS, reason=reason
    )


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
        raise HistoryContractError(
            "campaign ref observation has unsupported or missing fields"
        )
    observed_campaign_id = _nonempty_string(
        raw["campaign_id"], "campaign ref campaign_id"
    )
    if observed_campaign_id != campaign_id:
        raise HistoryContractError("campaign ref belongs to another campaign")
    campaign_ref = _ref(raw["campaign_ref"], "campaign ref", campaign=True)
    default_ref = _ref(raw["default_ref"], "storage default ref", campaign=False)
    if default_ref.startswith("refs/heads/campaign/"):
        raise HistoryContractError("storage default ref cannot be a campaign ref")
    return {
        "campaign_ref": campaign_ref,
        "campaign_head_revision": _revision(
            raw["campaign_head_revision"], "campaign HEAD"
        ),
        "default_ref": default_ref,
        "default_head_revision": _revision(
            raw["default_head_revision"], "storage default HEAD"
        ),
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
    if (
        _nonempty_string(raw["campaign_id"], "initialization campaign_id")
        != campaign_id
    ):
        raise HistoryContractError("initialization commit belongs to another campaign")
    if (
        _revision(raw["revision"], "initialization commit revision")
        != initialization_revision
    ):
        raise HistoryContractError(
            "initialization commit revision does not match campaign ref"
        )
    if type(raw["campaign_specific"]) is not bool or not raw["campaign_specific"]:
        raise HistoryContractError("initialization commit is not campaign-specific")
    parent_revision = _revision(
        raw["parent_revision"], "initialization parent revision"
    )
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
        raise HistoryContractError(
            "authenticated commit author has unsupported or missing fields"
        )
    author = _mapping(raw["author"], "authenticated commit author identity")
    if set(author) != {"login"}:
        raise HistoryContractError(
            "authenticated commit author identity has unsupported fields"
        )
    if type(raw["authenticated"]) is not bool or not raw["authenticated"]:
        raise HistoryContractError("commit author authentication is not trustworthy")
    if type(raw["per_user"]) is not bool or not raw["per_user"]:
        raise HistoryContractError(
            "commit author is not meaningful per-user authorship"
        )
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


def _t0_schema_version(value: object) -> int:
    if type(value) is not int or value != T0_BASIS_SCHEMA_VERSION:
        raise HistoryContractError("unsupported T0 basis schema_version")
    return T0_BASIS_SCHEMA_VERSION


def _unique_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise HistoryContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if not items or len(items) != len(set(items)):
        raise HistoryContractError(f"{label} must be nonempty and unique")
    return items


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
    semantic_delta = _thaw_history_value(event["semantic_delta"])
    if not isinstance(semantic_delta, dict):
        raise HistoryContractError("semantic_delta must be a JSON object")
    normalized = {
        "schema_version": _schema_version(event["schema_version"]),
        "event_id": _nonempty_string(event["event_id"], "event_id"),
        "semantic_order": _positive_int(event["semantic_order"], "semantic_order"),
        "kind": _nonempty_string(event["kind"], "kind"),
        "provenance_refs": _unique_strings(event["provenance_refs"], "provenance_refs"),
        "semantic_delta": semantic_delta,
    }
    extract_t0_basis_from_semantic_event(normalized)
    return normalized


def extract_t0_basis_from_semantic_event(
    value: object,
) -> dict[str, object] | None:
    """Return the bounded T0 basis embedded in this exact accepted event, if present."""
    event = _mapping(value, "semantic event")
    event_id = _nonempty_string(event.get("event_id"), "event_id")
    semantic_delta = _mapping(event.get("semantic_delta"), "semantic_delta")
    if "actor_decision_basis" not in semantic_delta:
        return None
    raw_basis = semantic_delta["actor_decision_basis"]
    basis = validate_t0_basis(raw_basis)
    if basis["event_id"] != event_id:
        raise HistoryContractError(
            "retained T0 basis must bind its containing native SemanticEvent"
        )
    return basis


def validate_t0_basis(value: object) -> dict[str, object]:
    """Validate bounded retained T0 factors without reading mutable T1 state."""

    basis = _mapping(value, "T0 basis")
    if set(basis) != {"schema_version", "event_id", "actor_id", "factors"}:
        raise HistoryContractError("T0 basis has unsupported or missing fields")
    raw_factors = basis["factors"]
    if (
        not isinstance(raw_factors, Sequence)
        or isinstance(raw_factors, str)
        or not raw_factors
    ):
        raise HistoryContractError("T0 factors must be a nonempty array")
    factors: list[dict[str, object]] = []
    factor_ids: set[str] = set()
    for raw_factor in raw_factors:
        factor = _mapping(raw_factor, "T0 factor")
        if set(factor) != _T0_FACTOR_FIELDS:
            raise HistoryContractError("T0 factor has unsupported or missing fields")
        factor_id = _nonempty_string(factor["factor_id"], "factor_id")
        if factor_id in factor_ids:
            raise HistoryContractError("T0 factor identities must be unique")
        factor_ids.add(factor_id)
        availability_classification = factor["availability_classification"]
        if (
            not isinstance(availability_classification, str)
            or availability_classification not in T0_AVAILABILITY_CLASSIFICATIONS
        ):
            raise HistoryContractError(
                "T0 factor availability_classification is unsupported"
            )
        factors.append(
            {
                "owner_family": _nonempty_string(
                    factor["owner_family"], "owner_family"
                ),
                "factor_id": factor_id,
                "t0_value": deepcopy(factor["t0_value"]),
                "provenance_refs": _unique_strings(
                    factor["provenance_refs"], "provenance_refs"
                ),
                "availability_classification": availability_classification,
            }
        )
    return {
        "schema_version": _t0_schema_version(basis["schema_version"]),
        "event_id": _nonempty_string(basis["event_id"], "event_id"),
        "actor_id": _nonempty_string(basis["actor_id"], "actor_id"),
        "factors": factors,
    }


def build_t0_basis(event: object, basis: object) -> dict[str, object]:
    """Copy only the T0 basis admitted inside its accepted native SemanticEvent."""

    event_value = validate_semantic_event_draft(event)
    basis_value = validate_t0_basis(basis)
    owner_basis = extract_t0_basis_from_semantic_event(event_value)
    if owner_basis is None:
        raise HistoryContractError(
            "native SemanticEvent does not contain a retained T0 decision basis"
        )
    if basis_value != owner_basis:
        raise HistoryContractError(
            "T0 basis differs from the containing native SemanticEvent evidence"
        )
    return basis_value


def append_semantic_event(history: object, event: object) -> list[dict[str, object]]:
    """Reject the former caller-shaped draft append path.

    Accepted history is issued only through the bound RuntimeHost History route.
    Keeping this name as a fail-closed compatibility surface prevents Story,
    narration, or another caller from silently becoming a native-history writer.
    """

    del history, event
    raise HistoryContractError(
        "caller-shaped semantic events cannot mint native history; use a bound evt window"
    )
