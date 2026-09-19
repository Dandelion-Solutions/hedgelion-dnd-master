"""Owner-native semantic history and retained event-time decision basis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
import re
from typing import TYPE_CHECKING, Final
import weakref

if TYPE_CHECKING:
    from .policy_basis import RepositoryPort


_GIT_REVISION: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_GIT_REF: Final = re.compile(r"^refs/heads/[^\s/]+(?:/[^\s/]+)*$")
_CAMPAIGN_REF: Final = re.compile(r"^refs/heads/campaign/[^\s/]+$")


class HistoryContractError(ValueError):
    """Raised when a caller supplies invalid native history material."""


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


def append_semantic_event(history: object, event: object) -> list[dict[str, object]]:
    """Return a new native-history sequence; projections never enter this path."""

    if not isinstance(history, Sequence) or isinstance(history, str):
        raise HistoryContractError("history must be an array")
    normalized = [validate_semantic_event_draft(item) for item in history]
    candidate = validate_semantic_event_draft(event)
    if candidate["event_id"] in {item["event_id"] for item in normalized}:
        raise HistoryContractError("semantic event identity is already accepted")
    if candidate["semantic_order"] in {item["semantic_order"] for item in normalized}:
        raise HistoryContractError("semantic order is already accepted")
    return [*normalized, candidate]
