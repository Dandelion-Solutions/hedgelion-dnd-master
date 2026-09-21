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

from .live_state import LiveRouting, select_live_source
from .policy_basis import PinnedCampaign

if TYPE_CHECKING:
    from .policy_basis import RepositoryPort


# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"
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


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class NativeHistoryCurrentness:
    """Ephemeral source basis issued by the bound native-history route."""

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
            raise HistoryContractError("unsupported native history contract generation")
        _history_origin(self.origin)
        _git_revision(self.source_revision, "native history source revision")
        if self.lower_exclusive is not None:
            _positive_int(self.lower_exclusive, "lower-exclusive evt ordinal")
        if self.upper is not None:
            _positive_int(self.upper, "upper evt ordinal")
            if self.upper <= (self.lower_exclusive or 0):
                raise HistoryContractError("native history interval is empty or reversed")
        if not isinstance(self.accepted_event_fingerprints, Mapping):
            raise HistoryContractError("native event fingerprints must be an object")
        fingerprints: dict[str, str] = {}
        for event_id, fingerprint in self.accepted_event_fingerprints.items():
            _nonempty_string(event_id, "accepted native event identity")
            if not isinstance(fingerprint, str) or re.fullmatch(r"[a-f0-9]{64}", fingerprint) is None:
                raise HistoryContractError("native event fingerprint must be SHA-256")
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
            "lower_exclusive": _cursor_text(self.lower_exclusive),
            "upper": _cursor_text(self.upper),
            "accepted_event_fingerprints": dict(self.accepted_event_fingerprints),
        }


_OWNER_ISSUED_CURRENTNESS: dict[int, weakref.ReferenceType[NativeHistoryCurrentness]] = {}


def _mark_owner_issued_currentness(value: NativeHistoryCurrentness) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeHistoryCurrentness]) -> None:
        if _OWNER_ISSUED_CURRENTNESS.get(value_id) is reference:
            _OWNER_ISSUED_CURRENTNESS.pop(value_id, None)

    _OWNER_ISSUED_CURRENTNESS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_currentness(value: object) -> bool:
    reference = _OWNER_ISSUED_CURRENTNESS.get(id(value))
    return isinstance(value, NativeHistoryCurrentness) and reference is not None and reference() is value


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class NativeSemanticEvent:
    """Accepted SemanticEvent evidence bound to one exact source window."""

    event: Mapping[str, object]
    currentness: NativeHistoryCurrentness

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("accepted semantic events must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_currentness(self.currentness):
            raise HistoryContractError("accepted event requires service-issued currentness")
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
        """The native evt enrollment ordinal, not fictional chronology."""

        return self.semantic_order

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
                "provenance_refs": list(self.event["provenance_refs"]),
            },
        }


_OWNER_ISSUED_EVENTS: dict[int, weakref.ReferenceType[NativeSemanticEvent]] = {}


def _mark_owner_issued_event(value: NativeSemanticEvent) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeSemanticEvent]) -> None:
        if _OWNER_ISSUED_EVENTS.get(value_id) is reference:
            _OWNER_ISSUED_EVENTS.pop(value_id, None)

    _OWNER_ISSUED_EVENTS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_event(value: object) -> bool:
    reference = _OWNER_ISSUED_EVENTS.get(id(value))
    return isinstance(value, NativeSemanticEvent) and reference is not None and reference() is value


@dataclass(frozen=True, slots=True, init=False, weakref_slot=True)
class NativeHistoryPublication:
    """Ephemeral accepted history over one validated evt source window."""

    currentness: NativeHistoryCurrentness
    events: tuple[NativeSemanticEvent, ...]

    def __init__(self, **_values: object) -> None:
        raise HistoryContractError("native history publications must be service-issued")

    def __post_init__(self) -> None:
        if not _is_owner_issued_currentness(self.currentness):
            raise HistoryContractError("publication requires service-issued currentness")
        events = tuple(self.events)
        if any(not _is_owner_issued_event(event) for event in events):
            raise HistoryContractError("publication requires service-issued events")
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


_OWNER_ISSUED_PUBLICATIONS: dict[int, weakref.ReferenceType[NativeHistoryPublication]] = {}


def _mark_owner_issued_publication(value: NativeHistoryPublication) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[NativeHistoryPublication]) -> None:
        if _OWNER_ISSUED_PUBLICATIONS.get(value_id) is reference:
            _OWNER_ISSUED_PUBLICATIONS.pop(value_id, None)

    _OWNER_ISSUED_PUBLICATIONS[value_id] = weakref.ref(value, remove)


def _is_owner_issued_publication(value: object) -> bool:
    reference = _OWNER_ISSUED_PUBLICATIONS.get(id(value))
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


def append_semantic_event(history: object, event: object) -> NativeHistoryPublication:
    """Append only service-issued event evidence to an owner-issued publication."""

    if not _is_owner_issued_publication(history):
        raise HistoryContractError("native history append requires an owner-issued publication")
    if not _is_owner_issued_event(event):
        raise HistoryContractError("native history append requires an owner-issued event")
    if event.currentness != history.currentness:
        raise HistoryContractError("native history event currentness differs")
    if history.events and event.admission_ordinal <= history.events[-1].admission_ordinal:
        raise HistoryContractError("native history admission ordinal must advance")
    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", history.currentness)
    object.__setattr__(publication, "events", (*history.events, event))
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_publication(publication)
    return publication


def _read_bound_native_history(
    repository: RepositoryPort,
    *,
    campaign_id: str,
    campaign_pin: PinnedCampaign,
    current_routing: LiveRouting | None,
    selected_live_reader: object,
    origin: str,
) -> NativeHistoryPublication:
    """Read one bounded evt window through the RuntimeHost-owned capabilities."""

    campaign = _nonempty_string(campaign_id, "native history campaign_id")
    if campaign_pin.campaign_id != campaign:
        raise HistoryContractError("native history campaign pin belongs to another campaign")
    checked_origin = _history_origin(origin)
    if checked_origin == "LOCAL":
        try:
            raw_window = repository.read_exact_path(campaign_pin, _SEMANTIC_EVENT_PATH)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise HistoryContractError("campaign semantic-event window is unavailable") from exc
        expected_revision = campaign_pin.revision
    else:
        if not isinstance(current_routing, LiveRouting):
            raise HistoryContractError("selected LIVE source routing is unavailable")
        if current_routing.campaign_id != campaign or not current_routing.complete:
            raise HistoryContractError("selected LIVE source routing is stale")
        epoch_id = checked_origin.removeprefix("LIVE:")
        matches = tuple(entry for entry in current_routing.entries if entry.epoch_id == epoch_id)
        if len(matches) != 1:
            raise HistoryContractError("selected LIVE source is missing or ambiguous")
        source = select_live_source(current_routing, matches[0].source_key)
        if source is None or source.epoch_id != epoch_id:
            raise HistoryContractError("selected LIVE source is not current")
        reader = getattr(selected_live_reader, "read_selected_live_source", None)
        if not callable(reader):
            raise HistoryContractError("selected LIVE source read capability is unavailable")
        try:
            raw_window = reader(current_routing, source)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise HistoryContractError("selected LIVE semantic-event window is unavailable") from exc
        expected_revision = source.source_revision
    return _issue_native_history_publication(
        raw_window,
        campaign_id=campaign,
        origin=checked_origin,
        expected_revision=expected_revision,
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
    events = tuple(entry["event"] for entry in window["entries"])
    fingerprints = {
        event["event_id"]: _semantic_event_fingerprint(event) for event in events
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
    _mark_owner_issued_currentness(currentness)

    accepted_events: list[NativeSemanticEvent] = []
    for event in events:
        accepted = object.__new__(NativeSemanticEvent)
        object.__setattr__(accepted, "event", _freeze_history_value(event))
        object.__setattr__(accepted, "currentness", currentness)
        NativeSemanticEvent.__post_init__(accepted)
        _mark_owner_issued_event(accepted)
        accepted_events.append(accepted)

    publication = object.__new__(NativeHistoryPublication)
    object.__setattr__(publication, "currentness", currentness)
    object.__setattr__(publication, "events", tuple(accepted_events))
    NativeHistoryPublication.__post_init__(publication)
    _mark_owner_issued_publication(publication)
    return publication


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
        raise HistoryContractError("unsupported native history contract generation")
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
    raw_entries = window["entries"]
    if upper is None:
        if lower is not None or raw_entries not in ([], ()):
            raise HistoryContractError("empty native history window has an invalid basis")
        return {"lower_exclusive": None, "upper": None, "entries": []}
    lower_value = lower or 0
    if upper <= lower_value:
        raise HistoryContractError("native history source interval is empty or reversed")
    if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
        raise HistoryContractError("native history source entries must be an array")

    entries: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for offset, raw_entry in enumerate(raw_entries, start=1):
        entry = _mapping(raw_entry, "native history source entry")
        if set(entry) != {"candidate_id", "ordinal", "event"}:
            raise HistoryContractError("native history source entry fields are not strict")
        ordinal = _positive_int(entry["ordinal"], "native history admission ordinal")
        if ordinal != lower_value + offset or ordinal > upper:
            raise HistoryContractError("native history evt interval is not contiguous")
        normalized = validate_semantic_event_draft(entry["event"])
        if normalized["semantic_order"] != ordinal:
            raise HistoryContractError("semantic event order is not its evt admission ordinal")
        candidate_id = entry["candidate_id"]
        if candidate_id != _candidate_id(normalized["event_id"]):
            raise HistoryContractError("native history candidate identity does not bind event")
        if candidate_id in seen_ids:
            raise HistoryContractError("native history candidate identity is duplicated")
        seen_ids.add(candidate_id)
        entries.append({"candidate_id": candidate_id, "ordinal": ordinal, "event": normalized})
    if not entries or entries[-1]["ordinal"] != upper:
        raise HistoryContractError("native history source window does not prove its upper basis")
    return {"lower_exclusive": lower, "upper": upper, "entries": entries}


def _validate_owner_contracts(value: object) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 1:
        raise HistoryContractError("native history owner contracts must name one exact owner")
    contract = _mapping(value[0], "native history owner contract")
    if set(contract) != {"family", "schema_version"}:
        raise HistoryContractError("native history owner contract fields are not strict")
    if contract["family"] != "runtime.semantic_event" or contract["schema_version"] != 1:
        raise HistoryContractError("native history owner contract is unsupported")


def _validate_native_event_sequence(
    events: Sequence[NativeSemanticEvent], currentness: NativeHistoryCurrentness
) -> None:
    seen_ids: set[str] = set()
    previous: int | None = None
    for event in events:
        if not _is_owner_issued_event(event) or event.currentness != currentness:
            raise HistoryContractError("native history sequence contains foreign event evidence")
        if event.event_id in seen_ids:
            raise HistoryContractError("native history event identity is duplicated")
        if previous is not None and event.admission_ordinal <= previous:
            raise HistoryContractError("native history admission ordinals are not increasing")
        seen_ids.add(event.event_id)
        previous = event.admission_ordinal


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


def _cursor_text(value: int | None) -> str | None:
    return None if value is None else f"evt:{value}"


def _candidate_id(event_id: str) -> str:
    return json.dumps([event_id], ensure_ascii=False, separators=(",", ":"))


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
