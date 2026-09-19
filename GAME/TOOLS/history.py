"""Owner-native semantic history and retained event-time decision basis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
import re
from typing import Final
import weakref


_GIT_REVISION = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_FIRST_INITIALIZATION_OWNER_TOKEN: Final = object()


class HistoryContractError(ValueError):
    """Raised when a caller supplies invalid native history material."""


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

    @classmethod
    def _from_owner(
        cls,
        *,
        owner_token: object,
        campaign_id: str,
        author_login: str,
        initialization_revision: str,
        parent_revision: str,
    ) -> FirstInitializationHistoryEvidence:
        if owner_token is not _FIRST_INITIALIZATION_OWNER_TOKEN:
            raise HistoryContractError("first-initialization evidence requires the native history owner")
        _nonempty_string(campaign_id, "creator provenance campaign_id")
        _nonempty_string(author_login, "creator provenance author_login")
        _git_revision(initialization_revision, "creator initialization revision")
        _git_revision(parent_revision, "creator initialization parent revision")
        if initialization_revision == parent_revision:
            raise HistoryContractError("creator initialization commit must advance its parent")
        instance = object.__new__(cls)
        object.__setattr__(instance, "campaign_id", campaign_id)
        object.__setattr__(instance, "author_login", author_login)
        object.__setattr__(instance, "initialization_revision", initialization_revision)
        object.__setattr__(instance, "parent_revision", parent_revision)
        object.__setattr__(instance, "first_campaign_specific_commit", True)
        _mark_owner_issued_first_initialization_history(instance)
        return instance

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "author_login": self.author_login,
            "initialization_revision": self.initialization_revision,
            "parent_revision": self.parent_revision,
            "first_campaign_specific_commit": True,
        }


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


def _issue_verified_first_initialization_history(
    *,
    campaign_id: str,
    author_login: str,
    initialization_revision: str,
    parent_revision: str,
) -> FirstInitializationHistoryEvidence:
    """Internal native-history-owner seam used by the verified history adapter."""

    return FirstInitializationHistoryEvidence._from_owner(
        owner_token=_FIRST_INITIALIZATION_OWNER_TOKEN,
        campaign_id=campaign_id,
        author_login=author_login,
        initialization_revision=initialization_revision,
        parent_revision=parent_revision,
    )


def _git_revision(value: object, label: str) -> str:
    if not isinstance(value, str) or _GIT_REVISION.fullmatch(value) is None:
        raise HistoryContractError(f"{label} must be an exact lowercase Git revision")
    return value


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
