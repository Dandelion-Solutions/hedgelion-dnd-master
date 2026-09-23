"""Owner-local collaboration admission over exact native records.

The collaboration owner derives a bounded family from accepted
``Interaction``/``IntentPlan``/``IntentClause`` data and fresh native
revalidation.  It never accepts a caller-selected family, currentness flag,
participant authority, Procedure body or Continuation body.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, replace
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from .access_control import AccessControlContractError, PlayerRecord, resolve_player
from .durability import route_serialized_operation
from .native_storage import (
    FAMILY_ROOTS,
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .publication import PublicationOutcome, PublicationStatus
from .runtime_execution import (
    NativeOrderingError,
    resolve_native_ordering_evidence,
)

if TYPE_CHECKING:
    from .runtime_host import RuntimeHost, _OperationBasis


# framework_module_version: 1.0.14
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.14"
COLLABORATION_SCHEMA_VERSION: Final[int] = 3
COLLABORATION_FRONTIER_SCHEMA_VERSION: Final[int] = 1
COLLABORATION_CLOSED_BASIS_SCHEMA_VERSION: Final[int] = 1
COLLABORATION_HANDOFF_SCHEMA_VERSION: Final[int] = 1
COLLABORATION_CATCH_UP_SCHEMA_VERSION: Final[int] = 2
COLLABORATION_INPUT_FINGERPRINT_GENERATION: Final[int] = 1

_CLOSED_INPUT_FINGERPRINT_DOMAIN: Final[bytes] = (
    b"hdm:collaboration:closed-input-set:fingerprint:v1\0"
)

_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_SEMANTIC_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "OOC_COORDINATION",
        "DIEGETIC_COMMUNICATION",
        "ACTIONABLE_INTENT",
        "CONTROL_SIGNAL",
    }
)
_DEPENDENCY_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "JOINT_VOLUNTARY_ACTION",
        "SHARED_DECISION_OR_NEGOTIATION",
        "SHARED_SCARCE_RESOURCE_CHOICE",
        "SCENE_CHRONOLOGY_CONVERGENCE",
        "PC_CONSEQUENCE_DECISION",
    }
)
_CLAUSE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "clause_id",
        "order",
        "mapping_outcome",
        "execution_state",
        "guard",
        "command_id",
        "details",
        "collaboration_semantic_class",
        "normalized_semantics",
        "material_exact_text_refs",
        "dependency_kind",
        "purpose",
        "dependency_scope",
        "required_contributors",
        "optional_contributors",
        "native_basis_refs",
        "ordering_resolution_id",
    }
)
_DEPENDENCY_BASIS_RULES: Final[dict[str, tuple[str, str]]] = {
    "JOINT_VOLUNTARY_ACTION": ("world.scene", "scene_id"),
    "SHARED_DECISION_OR_NEGOTIATION": ("world.scene", "scene_id"),
    "SHARED_SCARCE_RESOURCE_CHOICE": ("world.asset", "asset_id"),
    "SCENE_CHRONOLOGY_CONVERGENCE": ("world.scene", "scene_id"),
    "PC_CONSEQUENCE_DECISION": ("world.actor", "actor_id"),
}
_COLLABORATION_READ_FAMILIES: Final[frozenset[str]] = frozenset(
    {
        "runtime.interaction",
        "runtime.intent_plan",
        "world.player",
        "world.scene",
        "world.asset",
        "world.actor",
    }
)


class CollaborationAdmissionError(ValueError):
    """Raised when a collaboration family cannot be proved fail-closed."""

    failure_code: str

    def __init__(
        self,
        message: str,
        *,
        failure_code: str = "collaboration.admission_invalid",
    ) -> None:
        super().__init__(message)
        self.failure_code = failure_code


class CoordinationFamily(StrEnum):
    """Closed derived collaboration-family result."""

    INDEPENDENT_IMMEDIATE = "INDEPENDENT_IMMEDIATE"
    AGENCY_DEPENDENT_COLLECTIVE = "AGENCY_DEPENDENT_COLLECTIVE"
    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"


class DependencyClass(StrEnum):
    """Finite generation-1 material dependency vocabulary."""

    JOINT_VOLUNTARY_ACTION = "JOINT_VOLUNTARY_ACTION"
    SHARED_DECISION_OR_NEGOTIATION = "SHARED_DECISION_OR_NEGOTIATION"
    SHARED_SCARCE_RESOURCE_CHOICE = "SHARED_SCARCE_RESOURCE_CHOICE"
    SCENE_CHRONOLOGY_CONVERGENCE = "SCENE_CHRONOLOGY_CONVERGENCE"
    PC_CONSEQUENCE_DECISION = "PC_CONSEQUENCE_DECISION"


def _id(value: object, label: str) -> str:
    if not isinstance(value, str) or _ID_PATTERN.fullmatch(value) is None:
        raise CollaborationAdmissionError(f"{label} must be a native identifier")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CollaborationAdmissionError(f"{label} must be a nonempty string")
    return value


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CollaborationAdmissionError(f"{label} must be an object")
    return value


def _sequence(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise CollaborationAdmissionError(f"{label} must be an array")
    return value


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class ContributorRef:
    """A required PLAYER and optional currently controlled PC reference."""

    player_id: str
    pc_id: str | None = None

    def __post_init__(self) -> None:
        _id(self.player_id, "contributor player_id")
        if self.pc_id is not None:
            _id(self.pc_id, "contributor pc_id")

    def to_mapping(self) -> dict[str, str]:
        value = {"player_id": self.player_id}
        if self.pc_id is not None:
            value["pc_id"] = self.pc_id
        return value


@dataclass(frozen=True, slots=True)
class NativeBasisRef:
    """One finite known-ID dependency-owner reference."""

    family: str
    record_id: str
    revision: str | None = None

    def __post_init__(self) -> None:
        if self.family not in FAMILY_ROOTS:
            raise CollaborationAdmissionError(
                "native basis family is not a known owner"
            )
        _id(self.record_id, "native basis id")
        if self.revision is not None:
            _text(self.revision, "native basis revision")

    @property
    def id(self) -> str:
        return self.record_id

    def to_mapping(self) -> dict[str, str]:
        value = {"family": self.family, "id": self.record_id}
        if self.revision is not None:
            value["revision"] = self.revision
        return value


def _canonical_input_associations(
    accepted_input_uses: Sequence[tuple[str, str]],
    accepted_input_contributors: Sequence[tuple[tuple[str, str], ContributorRef]],
) -> tuple[dict[str, str], ...]:
    contributor_by_identity = dict(accepted_input_contributors)
    use_identities = set(accepted_input_uses)
    if use_identities != set(contributor_by_identity):
        raise CollaborationAdmissionError(
            "closed input uses and contributors must correlate"
        )
    canonical: list[dict[str, str]] = []
    for interaction_id, clause_id in use_identities:
        contributor = contributor_by_identity[(interaction_id, clause_id)]
        entry = {
            "interaction_id": interaction_id,
            "clause_id": clause_id,
            "player_id": contributor.player_id,
        }
        if contributor.pc_id is not None:
            entry["pc_id"] = contributor.pc_id
        canonical.append(entry)
    return tuple(
        sorted(
            canonical,
            key=lambda entry: tuple(
                entry.get(field, "")
                for field in ("interaction_id", "clause_id", "player_id", "pc_id")
            ),
        )
    )


def _closed_input_set_fingerprint(
    accepted_input_uses: Sequence[tuple[str, str]],
    accepted_input_contributors: Sequence[tuple[tuple[str, str], ContributorRef]],
) -> str:
    canonical = _canonical_input_associations(
        accepted_input_uses, accepted_input_contributors
    )
    encoded = json.dumps(
        {
            "generation": COLLABORATION_INPUT_FINGERPRINT_GENERATION,
            "inputs": canonical,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(_CLOSED_INPUT_FINGERPRINT_DOMAIN + encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class CollaborationClosedBasis:
    """Immutable order-independent basis frozen by explicit collection close."""

    campaign_id: str
    obligation_id: str
    generation: int
    closed_input_set_fingerprint: str
    accepted_input_uses: tuple[tuple[str, str], ...]
    accepted_input_contributors: tuple[tuple[tuple[str, str], ContributorRef], ...]

    def __post_init__(self) -> None:
        _id(self.campaign_id, "closed basis campaign_id")
        _id(self.obligation_id, "closed basis obligation_id")
        if (
            isinstance(self.generation, bool)
            or not isinstance(self.generation, int)
            or self.generation < 1
        ):
            raise CollaborationAdmissionError(
                "closed basis generation must be positive"
            )
        if (
            not isinstance(self.closed_input_set_fingerprint, str)
            or re.fullmatch(r"[a-f0-9]{64}", self.closed_input_set_fingerprint) is None
        ):
            raise CollaborationAdmissionError(
                "closed input set fingerprint must be a SHA-256 digest"
            )
        if (
            not isinstance(self.accepted_input_uses, tuple)
            or not self.accepted_input_uses
        ):
            raise CollaborationAdmissionError("closed basis input uses are required")
        normalized_uses = tuple(
            sorted(
                (
                    _id(identity[0], "closed input interaction_id"),
                    _id(identity[1], "closed input clause_id"),
                )
                for identity in self.accepted_input_uses
            )
        )
        if len(normalized_uses) != len(set(normalized_uses)):
            raise CollaborationAdmissionError(
                "closed basis input identities are duplicate"
            )
        if not isinstance(self.accepted_input_contributors, tuple):
            raise CollaborationAdmissionError(
                "closed basis input contributors are required"
            )
        normalized_contributors = tuple(
            sorted(
                (
                    (
                        _id(identity[0], "closed contributor interaction_id"),
                        _id(identity[1], "closed contributor clause_id"),
                    ),
                    contributor,
                )
                for identity, contributor in self.accepted_input_contributors
            )
        )
        if any(
            not isinstance(contributor, ContributorRef)
            for _, contributor in normalized_contributors
        ):
            raise CollaborationAdmissionError("closed basis contributors must be typed")
        if len(normalized_contributors) != len(
            {identity for identity, _ in normalized_contributors}
        ):
            raise CollaborationAdmissionError(
                "closed basis contributor identities are duplicate"
            )
        expected = _closed_input_set_fingerprint(
            normalized_uses, normalized_contributors
        )
        if self.closed_input_set_fingerprint != expected:
            raise CollaborationAdmissionError(
                "closed input set fingerprint does not match frozen inputs"
            )
        if set(normalized_uses) != {
            identity for identity, _ in normalized_contributors
        }:
            raise CollaborationAdmissionError(
                "closed basis input uses and contributors must correlate"
            )
        object.__setattr__(self, "accepted_input_uses", normalized_uses)
        object.__setattr__(self, "accepted_input_contributors", normalized_contributors)

    @classmethod
    def from_obligation(
        cls, obligation: CollaborationObligation
    ) -> CollaborationClosedBasis:
        if not isinstance(obligation, CollaborationObligation):
            raise CollaborationAdmissionError("owner-derived obligation is required")
        if obligation.closed_input_set_fingerprint is None:
            raise CollaborationAdmissionError("obligation has no closed input basis")
        return cls(
            campaign_id=obligation.campaign_id,
            obligation_id=obligation.obligation_id,
            generation=obligation.generation,
            closed_input_set_fingerprint=obligation.closed_input_set_fingerprint,
            accepted_input_uses=obligation.accepted_input_uses,
            accepted_input_contributors=obligation.accepted_input_contributors,
        )

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_CLOSED_BASIS_SCHEMA_VERSION,
            "kind": "runtime.collaboration_closed_basis",
            "campaign_id": self.campaign_id,
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "closed_input_set_fingerprint": self.closed_input_set_fingerprint,
            "accepted_input_uses": [
                {"interaction_id": interaction_id, "clause_id": clause_id}
                for interaction_id, clause_id in self.accepted_input_uses
            ],
            "accepted_input_contributors": [
                {
                    "interaction_id": interaction_id,
                    "clause_id": clause_id,
                    **contributor.to_mapping(),
                }
                for (
                    interaction_id,
                    clause_id,
                ), contributor in self.accepted_input_contributors
            ],
        }

    @classmethod
    def from_mapping(cls, value: object) -> CollaborationClosedBasis:
        if not isinstance(value, Mapping):
            raise CollaborationAdmissionError(
                "serialized closed basis must be an object"
            )
        expected = {
            "schema_version",
            "kind",
            "campaign_id",
            "obligation_id",
            "generation",
            "closed_input_set_fingerprint",
            "accepted_input_uses",
            "accepted_input_contributors",
        }
        if set(value) != expected:
            raise CollaborationAdmissionError(
                "serialized closed basis fields are not strict"
            )
        if (
            value["schema_version"] != COLLABORATION_CLOSED_BASIS_SCHEMA_VERSION
            or value["kind"] != "runtime.collaboration_closed_basis"
        ):
            raise CollaborationAdmissionError(
                "unsupported collaboration closed basis schema"
            )
        raw_uses = _sequence(value["accepted_input_uses"], "closed basis input uses")
        uses: list[tuple[str, str]] = []
        for raw_use in raw_uses:
            use = _mapping(raw_use, "closed basis input use")
            if set(use) != {"interaction_id", "clause_id"}:
                raise CollaborationAdmissionError(
                    "closed basis input use fields are not strict"
                )
            uses.append(
                (
                    _id(use["interaction_id"], "closed basis interaction_id"),
                    _id(use["clause_id"], "closed basis clause_id"),
                )
            )
        raw_contributors = _sequence(
            value["accepted_input_contributors"],
            "closed basis input contributors",
        )
        contributors: list[tuple[tuple[str, str], ContributorRef]] = []
        for raw_entry in raw_contributors:
            entry = _mapping(raw_entry, "closed basis input contributor")
            if set(entry) - {
                "interaction_id",
                "clause_id",
                "player_id",
                "pc_id",
            } or not {"interaction_id", "clause_id", "player_id"}.issubset(entry):
                raise CollaborationAdmissionError(
                    "closed basis contributor fields are not strict"
                )
            identity = (
                _id(entry["interaction_id"], "closed contributor interaction_id"),
                _id(entry["clause_id"], "closed contributor clause_id"),
            )
            contributors.append(
                (
                    identity,
                    ContributorRef(
                        _id(entry["player_id"], "closed contributor player_id"),
                        None
                        if entry.get("pc_id") is None
                        else _id(entry["pc_id"], "closed contributor pc_id"),
                    ),
                )
            )
        return cls(
            campaign_id=_id(value["campaign_id"], "closed basis campaign_id"),
            obligation_id=_id(value["obligation_id"], "closed basis obligation_id"),
            generation=value["generation"],  # type: ignore[arg-type]
            closed_input_set_fingerprint=_text(
                value["closed_input_set_fingerprint"],
                "closed input set fingerprint",
            ),
            accepted_input_uses=tuple(uses),
            accepted_input_contributors=tuple(contributors),
        )


class HandoffDisposition(StrEnum):
    """Finite next-owner choices for a frozen collaboration collection."""

    RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH = "RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH"
    CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT = "CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT"
    HAND_TO_EXISTING_NATIVE_OWNER = "HAND_TO_EXISTING_NATIVE_OWNER"
    CLARIFICATION_OR_UNSUPPORTED = "CLARIFICATION_OR_UNSUPPORTED"


@dataclass(frozen=True, slots=True)
class CollaborationHandoffEntry:
    """One frozen input mapped to an existing owner without a command ID."""

    interaction_id: str
    clause_id: str
    semantic_class: str
    disposition: HandoffDisposition
    execution_state: str | None

    def __post_init__(self) -> None:
        _id(self.interaction_id, "handoff interaction_id")
        _id(self.clause_id, "handoff clause_id")
        if self.semantic_class not in _SEMANTIC_CLASSES:
            raise CollaborationAdmissionError(
                "handoff semantic class is not registered"
            )
        if not isinstance(self.disposition, HandoffDisposition):
            raise CollaborationAdmissionError("handoff disposition is not registered")
        if self.execution_state is not None and self.execution_state not in {
            "intent.pending",
            "intent.ready",
            "intent.executed",
            "intent.skipped_due_to_prior_result",
            "intent.failed",
        }:
            raise CollaborationAdmissionError(
                "handoff execution state is not registered"
            )
        if (
            self.disposition
            is HandoffDisposition.RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
            and self.execution_state != "intent.ready"
        ):
            raise CollaborationAdmissionError(
                "released actionable handoff must be intent.ready"
            )

    @property
    def input_identity(self) -> tuple[str, str]:
        return self.interaction_id, self.clause_id

    @property
    def command_id(self) -> None:
        """Handoff evidence never allocates or carries a RuntimeCommand ID."""
        return None

    def to_mapping(self) -> dict[str, object]:
        value: dict[str, object] = {
            "interaction_id": self.interaction_id,
            "clause_id": self.clause_id,
            "semantic_class": self.semantic_class,
            "disposition": self.disposition.value,
        }
        if self.execution_state is not None:
            value["execution_state"] = self.execution_state
        return value


@dataclass(frozen=True, slots=True)
class CollaborationHandoff:
    """Ephemeral deterministic handoff from CLOSED collection to native owners."""

    basis: CollaborationClosedBasis
    entries: tuple[CollaborationHandoffEntry, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.basis, CollaborationClosedBasis):
            raise CollaborationAdmissionError("handoff closed basis is required")
        if not isinstance(self.entries, tuple) or not self.entries:
            raise CollaborationAdmissionError("handoff entries are required")
        if any(
            not isinstance(entry, CollaborationHandoffEntry) for entry in self.entries
        ):
            raise CollaborationAdmissionError("handoff entries must be typed")
        identities = tuple(entry.input_identity for entry in self.entries)
        if len(identities) != len(set(identities)):
            raise CollaborationAdmissionError("handoff input identities are duplicate")
        if set(identities) != set(self.basis.accepted_input_uses):
            raise CollaborationAdmissionError(
                "handoff entries must cover the closed input set"
            )
        if identities != tuple(sorted(identities)):
            raise CollaborationAdmissionError(
                "handoff entries must use deterministic input order"
            )

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_HANDOFF_SCHEMA_VERSION,
            "kind": "runtime.collaboration_handoff",
            "source_lifecycle": "CLOSED",
            "target_lifecycle": "RESOLVED",
            "closed_basis": self.basis.to_mapping(),
            "entries": [entry.to_mapping() for entry in self.entries],
        }

    @classmethod
    def from_mapping(cls, value: object) -> CollaborationHandoff:
        if not isinstance(value, Mapping):
            raise CollaborationAdmissionError("serialized handoff must be an object")
        expected = {
            "schema_version",
            "kind",
            "source_lifecycle",
            "target_lifecycle",
            "closed_basis",
            "entries",
        }
        if set(value) != expected:
            raise CollaborationAdmissionError(
                "serialized handoff fields are not strict"
            )
        if (
            value["schema_version"] != COLLABORATION_HANDOFF_SCHEMA_VERSION
            or value["kind"] != "runtime.collaboration_handoff"
            or value["source_lifecycle"] != "CLOSED"
            or value["target_lifecycle"] != "RESOLVED"
        ):
            raise CollaborationAdmissionError(
                "unsupported collaboration handoff schema"
            )
        raw_entries = _sequence(value["entries"], "handoff entries")
        entries: list[CollaborationHandoffEntry] = []
        for raw_entry in raw_entries:
            entry = _mapping(raw_entry, "handoff entry")
            if set(entry) - {
                "interaction_id",
                "clause_id",
                "semantic_class",
                "disposition",
                "execution_state",
            } or not {
                "interaction_id",
                "clause_id",
                "semantic_class",
                "disposition",
            }.issubset(entry):
                raise CollaborationAdmissionError("handoff entry fields are not strict")
            try:
                disposition = HandoffDisposition(entry["disposition"])
            except (TypeError, ValueError) as exc:
                raise CollaborationAdmissionError(
                    "handoff disposition is not registered"
                ) from exc
            entries.append(
                CollaborationHandoffEntry(
                    interaction_id=_id(
                        entry["interaction_id"], "handoff interaction_id"
                    ),
                    clause_id=_id(entry["clause_id"], "handoff clause_id"),
                    semantic_class=_text(
                        entry["semantic_class"], "handoff semantic class"
                    ),
                    disposition=disposition,
                    execution_state=(
                        None
                        if entry.get("execution_state") is None
                        else _text(entry["execution_state"], "handoff execution state")
                    ),
                )
            )
        return cls(
            basis=CollaborationClosedBasis.from_mapping(value["closed_basis"]),
            entries=tuple(entries),
        )


@dataclass(frozen=True, slots=True)
class CoordinationAdmission:
    """Ephemeral family evidence derived after complete revalidation."""

    campaign_id: str
    campaign_revision: str
    interaction_id: str
    initiating_player_id: str
    intent_plan_id: str
    clause_id: str
    semantic_class: str | None
    normalized_semantics: Mapping[str, object]
    dependency_class: DependencyClass | None
    purpose: str | None
    dependency_scope: Mapping[str, object]
    required_contributors: tuple[ContributorRef, ...]
    optional_contributors: tuple[ContributorRef, ...]
    native_basis_refs: tuple[NativeBasisRef, ...]
    family: CoordinationFamily
    ordered_evidence: object | None = None

    def __post_init__(self) -> None:
        _id(self.campaign_id, "admission campaign_id")
        _text(self.campaign_revision, "admission campaign revision")
        _id(self.interaction_id, "admission interaction_id")
        _id(self.initiating_player_id, "admission initiating player_id")
        _id(self.intent_plan_id, "admission intent_plan_id")
        _id(self.clause_id, "admission clause_id")
        if (
            self.semantic_class is not None
            and self.semantic_class not in _SEMANTIC_CLASSES
        ):
            raise CollaborationAdmissionError(
                "admission semantic class is not registered"
            )
        object.__setattr__(
            self,
            "normalized_semantics",
            MappingProxyType(dict(_freeze(self.normalized_semantics))),
        )
        object.__setattr__(
            self,
            "dependency_scope",
            MappingProxyType(dict(_freeze(self.dependency_scope))),
        )

    @property
    def opportunity_identity(self) -> tuple[str, str]:
        return self.interaction_id, self.clause_id


@dataclass(frozen=True, slots=True)
class CollaborationObligation:
    """Derived durable-owner shape for one collective generation."""

    obligation_id: str
    generation: int
    campaign_id: str
    interaction_id: str
    intent_plan_id: str
    clause_id: str
    semantic_class: str
    dependency_class: DependencyClass
    purpose: str
    dependency_scope: Mapping[str, object]
    native_basis_refs: tuple[NativeBasisRef, ...]
    required_contributors: tuple[ContributorRef, ...]
    coordination_family: CoordinationFamily = (
        CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
    )
    lifecycle: str = "OPEN"
    optional_contributors: tuple[ContributorRef, ...] = ()
    accepted_input_uses: tuple[tuple[str, str], ...] = ()
    accepted_input_contributors: tuple[tuple[tuple[str, str], ContributorRef], ...] = ()
    predecessor_generation: int | None = None
    closed_input_set_fingerprint: str | None = None

    def __post_init__(self) -> None:
        _id(self.obligation_id, "obligation_id")
        if (
            isinstance(self.generation, bool)
            or not isinstance(self.generation, int)
            or self.generation < 1
        ):
            raise CollaborationAdmissionError("obligation generation must be positive")
        if (
            self.coordination_family
            is not CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
        ):
            raise CollaborationAdmissionError(
                "only collective admissions create obligations"
            )
        if (
            not isinstance(self.semantic_class, str)
            or self.semantic_class not in _SEMANTIC_CLASSES
        ):
            raise CollaborationAdmissionError(
                "obligation semantic class is not registered"
            )
        if not isinstance(self.dependency_class, DependencyClass):
            raise CollaborationAdmissionError(
                "obligation dependency class is not registered"
            )
        _id(self.campaign_id, "obligation campaign_id")
        _id(self.interaction_id, "obligation interaction_id")
        _id(self.intent_plan_id, "obligation intent_plan_id")
        _id(self.clause_id, "obligation clause_id")
        _text(self.purpose, "obligation purpose")
        if not isinstance(self.dependency_scope, Mapping):
            raise CollaborationAdmissionError(
                "obligation dependency scope must be an object"
            )
        if not self.dependency_scope:
            raise CollaborationAdmissionError(
                "obligation dependency scope must not be empty"
            )
        if not isinstance(self.native_basis_refs, tuple) or not self.native_basis_refs:
            raise CollaborationAdmissionError(
                "obligation native basis refs are required"
            )
        basis_identities: set[tuple[str, str]] = set()
        for ref in self.native_basis_refs:
            if not isinstance(ref, NativeBasisRef):
                raise CollaborationAdmissionError(
                    "obligation native basis refs must be typed"
                )
            identity = (ref.family, ref.record_id)
            if identity in basis_identities:
                raise CollaborationAdmissionError(
                    "obligation native basis refs must be unique"
                )
            basis_identities.add(identity)
        if (
            not isinstance(self.required_contributors, tuple)
            or not self.required_contributors
        ):
            raise CollaborationAdmissionError(
                "obligation required contributors are required"
            )
        required_identities: set[tuple[str, str | None]] = set()
        for contributor in self.required_contributors:
            if not isinstance(contributor, ContributorRef):
                raise CollaborationAdmissionError(
                    "obligation contributors must be typed"
                )
            identity = (contributor.player_id, contributor.pc_id)
            if identity in required_identities:
                raise CollaborationAdmissionError(
                    "obligation required contributors must be unique"
                )
            required_identities.add(identity)
        if not isinstance(self.optional_contributors, tuple):
            raise CollaborationAdmissionError(
                "obligation optional contributors must be an array"
            )
        optional_identities: set[tuple[str, str | None]] = set()
        for contributor in self.optional_contributors:
            if not isinstance(contributor, ContributorRef):
                raise CollaborationAdmissionError(
                    "obligation contributors must be typed"
                )
            identity = (contributor.player_id, contributor.pc_id)
            if identity in optional_identities:
                raise CollaborationAdmissionError(
                    "obligation optional contributors must be unique"
                )
            optional_identities.add(identity)
        if {player_id for player_id, _ in required_identities}.intersection(
            player_id for player_id, _ in optional_identities
        ):
            raise CollaborationAdmissionError(
                "obligation contributors cannot be both required and optional"
            )
        if not isinstance(self.lifecycle, str) or self.lifecycle not in {
            "OPEN",
            "CLOSED",
            "RESOLVED",
            "OBSOLETE",
        }:
            raise CollaborationAdmissionError("obligation lifecycle is not registered")
        if self.closed_input_set_fingerprint is not None and (
            not isinstance(self.closed_input_set_fingerprint, str)
            or re.fullmatch(r"[a-f0-9]{64}", self.closed_input_set_fingerprint) is None
        ):
            raise CollaborationAdmissionError(
                "closed input set fingerprint must be a SHA-256 digest"
            )
        if self.lifecycle == "OPEN" and self.closed_input_set_fingerprint is not None:
            raise CollaborationAdmissionError(
                "open obligation cannot retain a closed input fingerprint"
            )
        if self.lifecycle in {"CLOSED", "RESOLVED"} and (
            self.closed_input_set_fingerprint is None
        ):
            raise CollaborationAdmissionError(
                "closed or resolved obligation requires a closed input fingerprint"
            )
        if self.generation == 1 and self.predecessor_generation is not None:
            raise CollaborationAdmissionError(
                "initial obligation cannot have a predecessor generation"
            )
        if self.generation > 1 and self.predecessor_generation is None:
            raise CollaborationAdmissionError(
                "successor obligation requires a predecessor generation"
            )
        if self.predecessor_generation is not None and (
            isinstance(self.predecessor_generation, bool)
            or not isinstance(self.predecessor_generation, int)
            or self.predecessor_generation != self.generation - 1
        ):
            raise CollaborationAdmissionError(
                "successor predecessor generation must be adjacent"
            )
        if (
            not isinstance(self.accepted_input_uses, tuple)
            or not self.accepted_input_uses
        ):
            raise CollaborationAdmissionError(
                "obligation accepted input uses are required"
            )
        use_identities: set[tuple[str, str]] = set()
        for identity in self.accepted_input_uses:
            if (
                not isinstance(identity, tuple)
                or len(identity) != 2
                or any(not isinstance(item, str) for item in identity)
            ):
                raise CollaborationAdmissionError(
                    "accepted input identity is malformed"
                )
            normalized_identity = (
                _id(identity[0], "accepted input interaction_id"),
                _id(identity[1], "accepted input clause_id"),
            )
            if normalized_identity in use_identities:
                raise CollaborationAdmissionError(
                    "accepted input identity is duplicate"
                )
            use_identities.add(normalized_identity)
        if (
            not isinstance(self.accepted_input_contributors, tuple)
            or not self.accepted_input_contributors
        ):
            raise CollaborationAdmissionError(
                "accepted input contributors are required"
            )
        contributor_identities: set[tuple[str, str]] = set()
        for entry in self.accepted_input_contributors:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise CollaborationAdmissionError(
                    "accepted input contributor entry is malformed"
                )
            identity, contributor = entry
            if (
                not isinstance(identity, tuple)
                or len(identity) != 2
                or any(not isinstance(item, str) for item in identity)
                or not isinstance(contributor, ContributorRef)
            ):
                raise CollaborationAdmissionError(
                    "accepted input contributor identity is malformed"
                )
            normalized_identity = (
                _id(identity[0], "accepted input contributor interaction_id"),
                _id(identity[1], "accepted input contributor clause_id"),
            )
            if normalized_identity in contributor_identities:
                raise CollaborationAdmissionError(
                    "accepted input contributor identity is duplicate"
                )
            contributor_identities.add(normalized_identity)
        if contributor_identities != use_identities:
            raise CollaborationAdmissionError(
                "accepted input uses and contributors must correlate"
            )

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_SCHEMA_VERSION,
            "kind": "runtime.collaboration_obligation",
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "predecessor_generation": self.predecessor_generation,
            "lifecycle": self.lifecycle,
            "coordination_family": self.coordination_family.value,
            "campaign_id": self.campaign_id,
            "interaction_id": self.interaction_id,
            "intent_plan_id": self.intent_plan_id,
            "clause_id": self.clause_id,
            "collaboration_semantic_class": self.semantic_class,
            "dependency_class": self.dependency_class.value,
            "purpose": self.purpose,
            "dependency_scope": _thaw(self.dependency_scope),
            "native_basis_refs": [ref.to_mapping() for ref in self.native_basis_refs],
            "required_contributors": [
                ref.to_mapping() for ref in self.required_contributors
            ],
            "optional_contributors": [
                ref.to_mapping() for ref in self.optional_contributors
            ],
            "accepted_input_uses": [
                {"interaction_id": interaction_id, "clause_id": clause_id}
                for interaction_id, clause_id in self.accepted_input_uses
            ],
            "accepted_input_contributors": [
                {
                    "interaction_id": interaction_id,
                    "clause_id": clause_id,
                    **contributor.to_mapping(),
                }
                for (
                    interaction_id,
                    clause_id,
                ), contributor in self.accepted_input_contributors
            ],
            "closed_input_set_fingerprint": self.closed_input_set_fingerprint,
        }

    @property
    def closed_basis(self) -> CollaborationClosedBasis:
        """Return the immutable basis produced for a CLOSED/RESOLVED state."""
        return CollaborationClosedBasis.from_obligation(self)

    @classmethod
    def from_mapping(
        cls,
        value: object,
        *,
        host: RuntimeHost,
        basis: _OperationBasis | None = None,
    ) -> CollaborationObligation:
        """Load one persisted obligation only after strict native revalidation."""
        if not isinstance(value, Mapping):
            raise CollaborationAdmissionError("serialized obligation must be an object")
        expected = {
            "schema_version",
            "kind",
            "obligation_id",
            "generation",
            "predecessor_generation",
            "lifecycle",
            "coordination_family",
            "campaign_id",
            "interaction_id",
            "intent_plan_id",
            "clause_id",
            "collaboration_semantic_class",
            "dependency_class",
            "purpose",
            "dependency_scope",
            "native_basis_refs",
            "required_contributors",
            "optional_contributors",
            "accepted_input_uses",
            "accepted_input_contributors",
            "closed_input_set_fingerprint",
        }
        if set(value) != expected:
            raise CollaborationAdmissionError(
                "serialized obligation fields are not strict"
            )
        if (
            value["schema_version"] != COLLABORATION_SCHEMA_VERSION
            or value["kind"] != "runtime.collaboration_obligation"
        ):
            raise CollaborationAdmissionError(
                "unsupported collaboration obligation schema"
            )
        raw_uses = _sequence(value["accepted_input_uses"], "accepted input uses")
        uses: list[tuple[str, str]] = []
        for raw_use in raw_uses:
            use = _mapping(raw_use, "accepted input use")
            if set(use) != {"interaction_id", "clause_id"}:
                raise CollaborationAdmissionError(
                    "accepted input use fields are not strict"
                )
            uses.append(
                (
                    _id(use["interaction_id"], "accepted input interaction_id"),
                    _id(use["clause_id"], "accepted input clause_id"),
                )
            )
        raw_contributors = _sequence(
            value["accepted_input_contributors"],
            "accepted input contributors",
        )
        contributors: list[tuple[tuple[str, str], ContributorRef]] = []
        for raw_entry in raw_contributors:
            entry = _mapping(raw_entry, "accepted input contributor")
            if set(entry) - {
                "interaction_id",
                "clause_id",
                "player_id",
                "pc_id",
            } or not {
                "interaction_id",
                "clause_id",
                "player_id",
            }.issubset(entry):
                raise CollaborationAdmissionError(
                    "accepted input contributor fields are not strict"
                )
            identity = (
                _id(
                    entry["interaction_id"], "accepted input contributor interaction_id"
                ),
                _id(entry["clause_id"], "accepted input contributor clause_id"),
            )
            contributors.append(
                (
                    identity,
                    ContributorRef(
                        _id(entry["player_id"], "accepted input contributor player_id"),
                        None
                        if entry.get("pc_id") is None
                        else _id(entry["pc_id"], "accepted input contributor pc_id"),
                    ),
                )
            )
        try:
            coordination_family = CoordinationFamily(value["coordination_family"])
            dependency_class = DependencyClass(value["dependency_class"])
        except (TypeError, ValueError) as exc:
            raise CollaborationAdmissionError(
                "serialized obligation class is not registered"
            ) from exc
        obligation = cls(
            obligation_id=_id(value["obligation_id"], "obligation_id"),
            generation=value["generation"],  # type: ignore[arg-type]
            predecessor_generation=value["predecessor_generation"],  # type: ignore[arg-type]
            lifecycle=value["lifecycle"],  # type: ignore[arg-type]
            coordination_family=coordination_family,
            campaign_id=_id(value["campaign_id"], "obligation campaign_id"),
            interaction_id=_id(value["interaction_id"], "obligation interaction_id"),
            intent_plan_id=_id(value["intent_plan_id"], "obligation intent_plan_id"),
            clause_id=_id(value["clause_id"], "obligation clause_id"),
            semantic_class=value["collaboration_semantic_class"],  # type: ignore[arg-type]
            dependency_class=dependency_class,
            purpose=_text(value["purpose"], "obligation purpose"),
            dependency_scope=_mapping(value["dependency_scope"], "dependency scope"),
            native_basis_refs=_parse_basis_refs(value["native_basis_refs"]),
            required_contributors=_parse_contributors(value["required_contributors"]),
            optional_contributors=_parse_contributors(value["optional_contributors"]),
            accepted_input_uses=tuple(uses),
            accepted_input_contributors=tuple(contributors),
            closed_input_set_fingerprint=(
                None
                if value["closed_input_set_fingerprint"] is None
                else _text(
                    value["closed_input_set_fingerprint"],
                    "closed input set fingerprint",
                )
            ),
        )
        if obligation.lifecycle in {"CLOSED", "RESOLVED"} or (
            obligation.lifecycle == "OBSOLETE"
            and obligation.closed_input_set_fingerprint is not None
        ):
            CollaborationClosedBasis.from_obligation(obligation)
        _validate_persisted_input_owners(obligation, host, basis=basis)
        return obligation


@dataclass(frozen=True, slots=True)
class CollaborationFrontier:
    """One scope-local safe prefix and its still-open required inputs.

    ``safe_prefix_refs`` are owner-native evidence references.  They are the
    same evidence boundary for semantic progress and visible consequence;
    this value object deliberately has no transport order, clock, CAS order,
    chronology or campaign-global frontier field.
    """

    obligation_id: str
    generation: int
    campaign_id: str
    dependency_scope: Mapping[str, object]
    safe_prefix_refs: tuple[NativeBasisRef, ...]
    pending_required_contributors: tuple[ContributorRef, ...]

    def __post_init__(self) -> None:
        _id(self.obligation_id, "frontier obligation_id")
        if (
            isinstance(self.generation, bool)
            or not isinstance(self.generation, int)
            or self.generation < 1
        ):
            raise CollaborationAdmissionError("frontier generation must be positive")
        _id(self.campaign_id, "frontier campaign_id")
        if not isinstance(self.dependency_scope, Mapping) or not self.dependency_scope:
            raise CollaborationAdmissionError(
                "frontier dependency scope must not be empty"
            )
        object.__setattr__(
            self,
            "dependency_scope",
            MappingProxyType(dict(_freeze(self.dependency_scope))),
        )
        if not isinstance(self.safe_prefix_refs, tuple) or not self.safe_prefix_refs:
            raise CollaborationAdmissionError("frontier owner evidence is required")
        if any(
            not isinstance(ref, NativeBasisRef) or ref.revision is None
            for ref in self.safe_prefix_refs
        ):
            raise CollaborationAdmissionError(
                "frontier owner evidence must carry current revisions"
            )
        if len(set(self.safe_prefix_refs)) != len(self.safe_prefix_refs):
            raise CollaborationAdmissionError("frontier owner evidence must be unique")
        if not isinstance(self.pending_required_contributors, tuple):
            raise CollaborationAdmissionError(
                "frontier pending contributors must be an array"
            )
        if any(
            not isinstance(contributor, ContributorRef)
            for contributor in self.pending_required_contributors
        ):
            raise CollaborationAdmissionError(
                "frontier pending contributors must be typed"
            )
        identities = [
            (contributor.player_id, contributor.pc_id)
            for contributor in self.pending_required_contributors
        ]
        if len(identities) != len(set(identities)):
            raise CollaborationAdmissionError(
                "frontier pending contributors must be unique"
            )

    def to_mapping(self) -> dict[str, object]:
        """Return the strict owner-local frontier projection."""
        return {
            "schema_version": COLLABORATION_FRONTIER_SCHEMA_VERSION,
            "kind": "runtime.collaboration_frontier",
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "campaign_id": self.campaign_id,
            "dependency_scope": _thaw(self.dependency_scope),
            "safe_prefix_refs": [ref.to_mapping() for ref in self.safe_prefix_refs],
            "pending_required_contributors": [
                contributor.to_mapping()
                for contributor in self.pending_required_contributors
            ],
        }

    @classmethod
    def from_mapping(cls, value: object) -> CollaborationFrontier:
        """Load a strict frontier projection without accepting technical order."""
        if not isinstance(value, Mapping):
            raise CollaborationAdmissionError("serialized frontier must be an object")
        expected = {
            "schema_version",
            "kind",
            "obligation_id",
            "generation",
            "campaign_id",
            "dependency_scope",
            "safe_prefix_refs",
            "pending_required_contributors",
        }
        if set(value) != expected:
            raise CollaborationAdmissionError(
                "serialized frontier fields are not strict"
            )
        if (
            value["schema_version"] != COLLABORATION_FRONTIER_SCHEMA_VERSION
            or value["kind"] != "runtime.collaboration_frontier"
        ):
            raise CollaborationAdmissionError(
                "unsupported collaboration frontier schema"
            )
        return cls(
            obligation_id=_id(value["obligation_id"], "frontier obligation_id"),
            generation=value["generation"],  # type: ignore[arg-type]
            campaign_id=_id(value["campaign_id"], "frontier campaign_id"),
            dependency_scope=_mapping(value["dependency_scope"], "frontier scope"),
            safe_prefix_refs=_parse_frontier_basis_refs(value["safe_prefix_refs"]),
            pending_required_contributors=_parse_frontier_contributors(
                value["pending_required_contributors"]
            ),
        )


@dataclass(frozen=True, slots=True)
class CollaborationRouteRef:
    """A non-authorizing exact obligation/generation routing reference."""

    obligation_id: str
    generation: int

    def __post_init__(self) -> None:
        _id(self.obligation_id, "route obligation_id")
        if isinstance(self.generation, bool) or not isinstance(self.generation, int):
            raise CollaborationAdmissionError("route generation must be an integer")
        if self.generation < 1:
            raise CollaborationAdmissionError("route generation must be positive")

    def to_mapping(self) -> dict[str, object]:
        return {
            "obligation_id": self.obligation_id,
            "generation": self.generation,
        }


@dataclass(frozen=True, slots=True)
class PlayerRouteCompanion:
    """Completeness-protected PLAYER routing projection, never authorization."""

    campaign_id: str
    player_id: str
    collaboration_route_refs: tuple[CollaborationRouteRef, ...]
    complete: bool = True

    def __post_init__(self) -> None:
        _id(self.campaign_id, "route companion campaign_id")
        _id(self.player_id, "route companion player_id")
        if self.complete is not True:
            raise CollaborationAdmissionError(
                "PLAYER collaboration route companion must be complete"
            )
        if any(
            not isinstance(ref, CollaborationRouteRef)
            for ref in self.collaboration_route_refs
        ):
            raise CollaborationAdmissionError("route companion refs must be typed")
        identities = [
            (ref.obligation_id, ref.generation) for ref in self.collaboration_route_refs
        ]
        if len(identities) != len(set(identities)):
            raise CollaborationAdmissionError("route companion refs must be unique")

    def to_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "player_id": self.player_id,
            "complete": True,
            "collaboration_route_refs": [
                ref.to_mapping() for ref in self.collaboration_route_refs
            ],
        }


@dataclass(frozen=True, slots=True)
class CollaborationCatchUpEntry:
    """Recipient-safe summary for one current obligation route reference.

    The entry deliberately carries no accepted input identity, semantic body,
    participant list, native basis or planning material.  Those owners remain
    independently responsible for deciding whether any such content is
    eligible for a recipient.
    """

    obligation_id: str
    generation: int
    lifecycle: str
    participant_role: str
    own_pc_ids: tuple[str, ...] = ()
    contribution_status: str = "PENDING"

    def __post_init__(self) -> None:
        _id(self.obligation_id, "catch-up obligation_id")
        if isinstance(self.generation, bool) or not isinstance(self.generation, int):
            raise CollaborationAdmissionError("catch-up generation must be an integer")
        if self.generation < 1:
            raise CollaborationAdmissionError("catch-up generation must be positive")
        if self.lifecycle not in {"OPEN", "CLOSED"}:
            raise CollaborationAdmissionError("catch-up lifecycle is not unresolved")
        if self.participant_role not in {"ORIGINATING", "REQUIRED", "OPTIONAL"}:
            raise CollaborationAdmissionError(
                "catch-up participant role is not registered"
            )
        if not isinstance(self.own_pc_ids, tuple):
            raise CollaborationAdmissionError("catch-up PC references must be an array")
        normalized_pc_ids = tuple(
            _id(pc_id, "catch-up own pc_id") for pc_id in self.own_pc_ids
        )
        if len(normalized_pc_ids) != len(set(normalized_pc_ids)):
            raise CollaborationAdmissionError("catch-up PC references must be unique")
        object.__setattr__(self, "own_pc_ids", normalized_pc_ids)
        if self.contribution_status not in {"PENDING", "RECEIVED", "NOT_REQUIRED"}:
            raise CollaborationAdmissionError(
                "catch-up contribution status is not registered"
            )
        if (
            self.participant_role == "OPTIONAL"
            and self.contribution_status == "PENDING"
        ):
            raise CollaborationAdmissionError(
                "optional catch-up contribution cannot be pending"
            )

    def to_mapping(self) -> dict[str, object]:
        return {
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "lifecycle": self.lifecycle,
            "participant_role": self.participant_role,
            "own_pc_ids": list(self.own_pc_ids),
            "contribution_status": self.contribution_status,
        }


@dataclass(frozen=True, slots=True)
class CollaborationCatchUp:
    """Ephemeral recipient projection prepared after current route admission."""

    campaign_id: str
    campaign_revision: str
    player_id: str
    controlled_pc_ids: tuple[str, ...]
    live_source_keys: tuple[tuple[str, str, str], ...]
    obligations: tuple[CollaborationCatchUpEntry, ...]
    cursor_hint: str | None = None

    def __post_init__(self) -> None:
        _id(self.campaign_id, "catch-up campaign_id")
        _text(self.campaign_revision, "catch-up campaign revision")
        _id(self.player_id, "catch-up player_id")
        if not isinstance(self.controlled_pc_ids, tuple):
            raise CollaborationAdmissionError(
                "catch-up controlled PC references must be an array"
            )
        controlled_pc_ids = tuple(
            _id(pc_id, "catch-up controlled pc_id") for pc_id in self.controlled_pc_ids
        )
        if len(controlled_pc_ids) != len(set(controlled_pc_ids)):
            raise CollaborationAdmissionError(
                "catch-up controlled PC references must be unique"
            )
        object.__setattr__(self, "controlled_pc_ids", controlled_pc_ids)
        if not isinstance(self.live_source_keys, tuple):
            raise CollaborationAdmissionError(
                "catch-up LIVE source keys must be an array"
            )
        normalized_sources: list[tuple[str, str, str]] = []
        for source_key in self.live_source_keys:
            if (
                not isinstance(source_key, tuple)
                or len(source_key) != 3
                or any(not isinstance(part, str) or not part for part in source_key)
            ):
                raise CollaborationAdmissionError("catch-up LIVE source key is invalid")
            normalized_sources.append(source_key)
        if len(normalized_sources) != len(set(normalized_sources)):
            raise CollaborationAdmissionError(
                "catch-up LIVE source keys must be unique"
            )
        object.__setattr__(self, "live_source_keys", tuple(sorted(normalized_sources)))
        if not isinstance(self.obligations, tuple) or any(
            not isinstance(entry, CollaborationCatchUpEntry)
            for entry in self.obligations
        ):
            raise CollaborationAdmissionError("catch-up obligations must be typed")
        identities = [
            (entry.obligation_id, entry.generation) for entry in self.obligations
        ]
        if len(identities) != len(set(identities)):
            raise CollaborationAdmissionError("catch-up obligations must be unique")
        object.__setattr__(
            self,
            "obligations",
            tuple(
                sorted(
                    self.obligations,
                    key=lambda entry: (entry.obligation_id, entry.generation),
                )
            ),
        )
        if self.cursor_hint is not None:
            _text(self.cursor_hint, "catch-up cursor hint")

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_CATCH_UP_SCHEMA_VERSION,
            "kind": "runtime.collaboration_catch_up",
            "campaign_id": self.campaign_id,
            "campaign_revision": self.campaign_revision,
            "player_id": self.player_id,
            "controlled_pc_ids": list(self.controlled_pc_ids),
            "live_source_keys": [
                list(source_key) for source_key in self.live_source_keys
            ],
            "obligations": [entry.to_mapping() for entry in self.obligations],
            "cursor_hint": self.cursor_hint,
        }


def _read_native(
    host: RuntimeHost,
    basis: _OperationBasis,
    family: str,
    record_id: str,
) -> Mapping[str, object]:
    if family not in _COLLABORATION_READ_FAMILIES:
        raise CollaborationAdmissionError(
            "native family is not admitted for collaboration"
        )
    _id(record_id, f"{family} id")
    try:
        route = route_native_record(family, (record_id,))
        raw = host._repository.read_exact_path(
            basis.pinned_campaign, route.relative_path
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(f"exact {family} load failed") from exc
    payload = _mapping(raw, f"exact {family} record")
    try:
        validate_loaded_identity(family, (record_id,), payload)
    except (IdentityMismatch, NativeStorageError) as exc:
        raise CollaborationAdmissionError(
            f"exact {family} identity is stale or foreign"
        ) from exc
    if payload.get("campaign_id") not in {None, basis.pinned_campaign.campaign_id}:
        raise CollaborationAdmissionError(f"exact {family} belongs to another campaign")
    return payload


def _load_interaction(
    host: RuntimeHost, basis: _OperationBasis, interaction_id: str
) -> Mapping[str, object]:
    interaction = _read_native(host, basis, "runtime.interaction", interaction_id)
    declared_id = interaction.get("interaction_id", interaction.get("id"))
    if declared_id is not None and declared_id != interaction_id:
        raise CollaborationAdmissionError(
            "interaction identity differs from requested identity"
        )
    if interaction.get("campaign_id") != basis.pinned_campaign.campaign_id:
        raise CollaborationAdmissionError("interaction belongs to another campaign")
    for field in ("session_id", "player_id", "input_message_id", "intent_plan_id"):
        _id(interaction.get(field), f"interaction {field}")
    return interaction


def _load_plan(
    host: RuntimeHost,
    basis: _OperationBasis,
    intent_plan_id: str,
    interaction_id: str,
) -> Mapping[str, object]:
    plan = _read_native(host, basis, "runtime.intent_plan", intent_plan_id)
    declared_id = plan.get("intent_plan_id", plan.get("id"))
    if declared_id is not None and declared_id != intent_plan_id:
        raise CollaborationAdmissionError(
            "intent plan identity differs from interaction route"
        )
    if plan.get("interaction_id") != interaction_id:
        raise CollaborationAdmissionError("intent plan is not owned by the interaction")
    return plan


def _load_clause(plan: Mapping[str, object], clause_id: str) -> Mapping[str, object]:
    clauses = _sequence(plan.get("clauses"), "intent plan clauses")
    matches = [
        clause
        for clause in clauses
        if isinstance(clause, Mapping) and clause.get("clause_id") == clause_id
    ]
    if len(matches) != 1:
        raise CollaborationAdmissionError(
            "intent clause identity is missing or ambiguous"
        )
    clause = matches[0]
    if set(clause) - _CLAUSE_FIELDS:
        raise CollaborationAdmissionError(
            "intent clause contains an unsupported authority field"
        )
    if clause.get("execution_state") not in {
        "intent.pending",
        "intent.ready",
        "intent.executed",
        "intent.skipped_due_to_prior_result",
        "intent.failed",
    }:
        raise CollaborationAdmissionError(
            "intent clause execution state is not registered"
        )
    if clause.get("mapping_outcome") not in {
        "exact",
        "composed",
        "narrative_only",
        "clarification_required",
        "unsupported",
    }:
        raise CollaborationAdmissionError(
            "intent clause mapping outcome is not registered"
        )
    return clause


def _parse_contributors(value: object) -> tuple[ContributorRef, ...]:
    result: list[ContributorRef] = []
    seen: set[tuple[str, str | None]] = set()
    for raw in _sequence(value, "required contributors"):
        contributor = _mapping(raw, "required contributor")
        if set(contributor) - {"player_id", "pc_id"} or "player_id" not in contributor:
            raise CollaborationAdmissionError(
                "required contributor has unsupported fields"
            )
        ref = ContributorRef(
            _id(contributor["player_id"], "required contributor player_id"),
            None
            if contributor.get("pc_id") is None
            else _id(contributor["pc_id"], "required contributor pc_id"),
        )
        if (ref.player_id, ref.pc_id) in seen:
            raise CollaborationAdmissionError("required contributors must be unique")
        seen.add((ref.player_id, ref.pc_id))
        result.append(ref)
    return tuple(result)


def _parse_basis_refs(value: object) -> tuple[NativeBasisRef, ...]:
    result: list[NativeBasisRef] = []
    seen: set[tuple[str, str]] = set()
    for raw in _sequence(value, "native basis refs"):
        basis = _mapping(raw, "native basis ref")
        if set(basis) - {"family", "id", "revision"} or not {"family", "id"}.issubset(
            basis
        ):
            raise CollaborationAdmissionError(
                "native basis ref has unsupported or missing fields"
            )
        ref = NativeBasisRef(
            _text(basis["family"], "native basis family"),
            _id(basis["id"], "native basis id"),
            None
            if basis.get("revision") is None
            else _text(basis["revision"], "native basis revision"),
        )
        if (ref.family, ref.record_id) in seen:
            raise CollaborationAdmissionError("native basis refs must be unique")
        seen.add((ref.family, ref.record_id))
        result.append(ref)
    if not result:
        raise CollaborationAdmissionError("positive dependency requires a native basis")
    return tuple(result)


def _parse_frontier_basis_refs(value: object) -> tuple[NativeBasisRef, ...]:
    refs = _parse_basis_refs(value)
    if any(ref.revision is None for ref in refs):
        raise CollaborationAdmissionError(
            "frontier owner evidence must carry current revisions"
        )
    return refs


def _parse_frontier_contributors(value: object) -> tuple[ContributorRef, ...]:
    return _parse_contributors(value)


def _validate_basis_shape(
    dependency: DependencyClass,
    scope: Mapping[str, object],
    basis_refs: tuple[NativeBasisRef, ...],
) -> None:
    if len(basis_refs) != 1:
        raise CollaborationAdmissionError(
            "dependency requires exactly one native basis owner"
        )
    basis = basis_refs[0]
    expected_family, scope_key = _DEPENDENCY_BASIS_RULES[dependency.value]
    if basis.family != expected_family:
        raise CollaborationAdmissionError(
            "native basis family is irrelevant to dependency class"
        )
    if basis.revision is None:
        raise CollaborationAdmissionError(
            "native basis revision is required for currentness"
        )
    if scope.get(scope_key) != basis.record_id:
        raise CollaborationAdmissionError(
            f"native basis id must match dependency scope {scope_key}"
        )


def _validate_clause_semantics(
    clause: Mapping[str, object],
) -> tuple[
    str | None,
    Mapping[str, object],
    DependencyClass | None,
    str | None,
    Mapping[str, object],
    tuple[ContributorRef, ...],
    tuple[ContributorRef, ...],
    tuple[NativeBasisRef, ...],
    str | None,
]:
    semantic_class = clause.get("collaboration_semantic_class")
    if semantic_class is not None and semantic_class not in _SEMANTIC_CLASSES:
        raise CollaborationAdmissionError(
            "intent clause semantic class is not registered"
        )
    normalized = _mapping(
        clause.get("normalized_semantics", {}), "normalized semantics"
    )
    raw_dependency = clause.get("dependency_kind")
    dependency = (
        None
        if raw_dependency is None
        else DependencyClass(str(raw_dependency))
        if raw_dependency in _DEPENDENCY_CLASSES
        else None
    )
    if raw_dependency is not None and dependency is None:
        raise CollaborationAdmissionError(
            "intent clause dependency class is not registered"
        )
    if semantic_class is not None and not normalized:
        raise CollaborationAdmissionError(
            "collaboration clause normalized semantics must not be empty"
        )
    purpose = clause.get("purpose")
    if purpose is not None:
        purpose = _text(purpose, "intent clause purpose")
    scope = _mapping(clause.get("dependency_scope", {}), "dependency scope")
    ordering_ref = clause.get("ordering_resolution_id")
    if ordering_ref is not None:
        ordering_ref = _id(ordering_ref, "ordering resolution id")
    if dependency is None:
        if (
            clause.get("required_contributors") is not None
            or clause.get("optional_contributors") is not None
            or clause.get("native_basis_refs") is not None
            or purpose is not None
            or scope
        ):
            raise CollaborationAdmissionError(
                "dependency fields require a registered dependency class"
            )
        if semantic_class == "ACTIONABLE_INTENT" and ordering_ref is None:
            raise CollaborationAdmissionError(
                "actionable collaboration intent lacks a dependency or ordering ref"
            )
        return semantic_class, normalized, None, None, scope, (), (), (), ordering_ref
    if semantic_class is None:
        raise CollaborationAdmissionError(
            "dependency class requires an accepted semantic class"
        )
    if purpose is None or not scope:
        raise CollaborationAdmissionError(
            "positive dependency requires bounded purpose and scope"
        )
    contributors = _parse_contributors(clause.get("required_contributors"))
    if not contributors:
        raise CollaborationAdmissionError(
            "positive dependency requires required contributors"
        )
    basis_refs = _parse_basis_refs(clause.get("native_basis_refs"))
    optional = _parse_contributors(
        clause.get("optional_contributors", ()),
    )
    if {ref.player_id for ref in contributors}.intersection(
        ref.player_id for ref in optional
    ):
        raise CollaborationAdmissionError(
            "contributors cannot be both required and optional"
        )
    _validate_basis_shape(dependency, scope, basis_refs)
    if (
        semantic_class == "ACTIONABLE_INTENT"
        and clause.get("execution_state") != "intent.pending"
    ):
        raise CollaborationAdmissionError(
            "collaboration-held actionable intent must remain pending"
        )
    if clause.get("command_id") is not None:
        raise CollaborationAdmissionError(
            "collaboration-held intent cannot already have a command"
        )
    return (
        semantic_class,
        normalized,
        dependency,
        purpose,
        scope,
        contributors,
        optional,
        basis_refs,
        ordering_ref,
    )


def _load_current_player(
    host: RuntimeHost,
    basis: _OperationBasis,
    principal: object,
    player_route: object,
    expected_player_id: str,
) -> PlayerRecord:
    def load_exact(candidate_id: str) -> Mapping[str, object]:
        return _read_native(host, basis, "world.player", candidate_id)

    try:
        resolution = resolve_player(
            principal,
            player_route,
            load_exact,
            campaign_id=basis.pinned_campaign.campaign_id,
        )
    except (
        AccessControlContractError,
        CollaborationAdmissionError,
        TypeError,
        ValueError,
    ) as exc:
        raise CollaborationAdmissionError(
            "current principal-to-PLAYER resolution failed"
        ) from exc
    if resolution.status != "AUTHORIZED_PLAYER" or resolution.player is None:
        raise CollaborationAdmissionError(
            "current principal does not own an active PLAYER"
        )
    if resolution.player.player_id != expected_player_id:
        raise CollaborationAdmissionError(
            "interaction PLAYER differs from current principal PLAYER"
        )
    return resolution.player


def _validate_required_player(
    host: RuntimeHost, basis: _OperationBasis, ref: ContributorRef
) -> None:
    try:
        player = PlayerRecord.from_mapping(
            _read_native(host, basis, "world.player", ref.player_id)
        )
    except (
        AccessControlContractError,
        CollaborationAdmissionError,
        TypeError,
        ValueError,
    ) as exc:
        raise CollaborationAdmissionError(
            "required contributor PLAYER is not current"
        ) from exc
    if player.status != "active":
        raise CollaborationAdmissionError("required contributor PLAYER is not active")
    if ref.pc_id is not None and ref.pc_id not in player.controlled_pc_ids:
        raise CollaborationAdmissionError(
            "required contributor PC is not currently controlled"
        )


def _revalidate_host_basis(host: RuntimeHost, basis: _OperationBasis) -> None:
    try:
        current_basis = host._begin_operation()
    except (AttributeError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "runtime host basis could not be revalidated"
        ) from exc
    if current_basis != basis:
        raise CollaborationAdmissionError(
            "runtime host campaign basis changed during admission"
        )


def _operation_basis(
    host: RuntimeHost, basis: _OperationBasis | None
) -> _OperationBasis:
    """Use one caller-prepared host basis throughout a publication preparation."""
    if basis is None:
        try:
            basis = host._begin_operation()
        except (AttributeError, TypeError, ValueError) as exc:
            raise CollaborationAdmissionError("bound runtime host is required") from exc
    if not hasattr(basis, "pinned_campaign") or not hasattr(basis, "selected_live"):
        raise CollaborationAdmissionError("host operation basis is not owner-typed")
    if basis.host_token is not host._basis_token:
        raise CollaborationAdmissionError(
            "host operation basis belongs to another runtime host"
        )
    if basis.pinned_campaign.campaign_id != host.campaign_id:
        raise CollaborationAdmissionError(
            "host operation basis belongs to another campaign"
        )
    return basis


def _revalidate_frontier_basis(
    obligation: CollaborationObligation, host: RuntimeHost
) -> tuple[NativeBasisRef, ...]:
    """Read the obligation's bounded native basis through the bound host.

    A frontier is safe only when the exact owner records still carry the
    revisions admitted for this obligation.  The caller cannot replay a
    previously observed basis or supply a replacement scope.  The host basis
    is checked again after the exact reads so a ref move during this operation
    also fails closed.
    """
    try:
        basis = host._begin_operation()
    except (AttributeError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "runtime host is required for frontier currentness"
        ) from exc
    if basis.pinned_campaign.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "frontier obligation belongs to another campaign"
        )
    try:
        _validate_basis_shape(
            obligation.dependency_class,
            obligation.dependency_scope,
            obligation.native_basis_refs,
        )
    except (CollaborationAdmissionError, KeyError) as exc:
        raise CollaborationAdmissionError(
            "frontier obligation basis is invalid"
        ) from exc

    current: list[NativeBasisRef] = []
    for ref in obligation.native_basis_refs:
        owner = _read_native(host, basis, ref.family, ref.record_id)
        if owner.get("revision") != ref.revision:
            raise CollaborationAdmissionError("frontier native basis is not current")
        current.append(NativeBasisRef(ref.family, ref.record_id, ref.revision))
    _revalidate_host_basis(host, basis)
    return _canonical_frontier_refs(current, "current frontier basis")


def _validate_persisted_input_owners(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> None:
    """Prove each persisted input identity against its native Interaction owner."""
    basis = _operation_basis(host, basis)
    if basis.pinned_campaign.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "serialized obligation belongs to another campaign"
        )
    originating_identity = (obligation.interaction_id, obligation.clause_id)
    permitted_contributors = (
        obligation.required_contributors + obligation.optional_contributors
    )
    for (
        interaction_id,
        clause_id,
    ), contributor in obligation.accepted_input_contributors:
        identity = (interaction_id, clause_id)
        interaction = _load_interaction(host, basis, interaction_id)
        if interaction.get("player_id") != contributor.player_id:
            raise CollaborationAdmissionError(
                "accepted input contributor does not match native Interaction owner"
            )
        if identity == originating_identity:
            if contributor.pc_id is not None:
                raise CollaborationAdmissionError(
                    "originating input cannot add a PC association"
                )
            _validate_required_player(host, basis, contributor)
        else:
            participant = next(
                (
                    ref
                    for ref in permitted_contributors
                    if ref.player_id == contributor.player_id
                ),
                None,
            )
            if participant is None:
                raise CollaborationAdmissionError(
                    "persisted input contributor is not a current obligation holder"
                )
            if participant != contributor:
                raise CollaborationAdmissionError(
                    "persisted input contributor does not match holder PC association"
                )
            _validate_required_player(host, basis, participant)
        plan = _load_plan(
            host,
            basis,
            _id(interaction["intent_plan_id"], "input intent_plan_id"),
            interaction_id,
        )
        clause = _load_clause(plan, clause_id)
        if clause.get("collaboration_semantic_class") != obligation.semantic_class:
            raise CollaborationAdmissionError(
                "accepted input semantic class does not match obligation"
            )
    _revalidate_host_basis(host, basis)


def classify_coordination_dependency(
    host: RuntimeHost,
    interaction_id: str,
    clause_id: str,
    *,
    principal: object,
    player_route: object,
) -> CoordinationAdmission:
    """Derive one family through the bound RuntimeHost owner-reader path."""
    _id(interaction_id, "interaction_id")
    _id(clause_id, "clause_id")
    try:
        basis = host._begin_operation()
    except (AttributeError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError("bound runtime host is required") from exc
    interaction = _load_interaction(host, basis, interaction_id)
    intent_plan_id = _id(interaction["intent_plan_id"], "interaction intent_plan_id")
    plan = _load_plan(host, basis, intent_plan_id, interaction_id)
    clause = _load_clause(plan, clause_id)
    (
        semantic_class,
        normalized,
        dependency,
        purpose,
        scope,
        required,
        optional,
        basis_refs,
        ordering_ref,
    ) = _validate_clause_semantics(clause)
    current_player = _load_current_player(
        host,
        basis,
        principal,
        player_route,
        _id(interaction["player_id"], "interaction player_id"),
    )
    del current_player
    for ref in basis_refs:
        owner = _read_native(host, basis, ref.family, ref.record_id)
        if ref.revision is None or owner.get("revision") != ref.revision:
            raise CollaborationAdmissionError("native basis revision is stale")
    for ref in required:
        _validate_required_player(host, basis, ref)

    ordered_evidence = None
    if ordering_ref is not None:
        try:
            _revalidate_host_basis(host, basis)
            ordered_evidence = resolve_native_ordering_evidence(
                {"resolution_id": ordering_ref},
                repository=host._repository,
                campaign_pin=basis.pinned_campaign,
                selected_live=basis.selected_live,
            )
        except CollaborationAdmissionError:
            raise
        except (NativeOrderingError, AttributeError, TypeError, ValueError) as exc:
            raise CollaborationAdmissionError(
                "ordered owner evidence is invalid"
            ) from exc
        if (
            getattr(getattr(ordered_evidence, "status", None), "value", None)
            != "RULE_OWNED_ORDERED"
        ):
            raise CollaborationAdmissionError("ordered owner evidence is unavailable")
        family = CoordinationFamily.RULE_OWNED_ORDERED
    elif dependency is None:
        family = CoordinationFamily.INDEPENDENT_IMMEDIATE
    else:
        family = CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
    return CoordinationAdmission(
        campaign_id=basis.pinned_campaign.campaign_id,
        campaign_revision=basis.pinned_campaign.revision,
        interaction_id=interaction_id,
        initiating_player_id=_id(interaction["player_id"], "interaction player_id"),
        intent_plan_id=intent_plan_id,
        clause_id=clause_id,
        semantic_class=semantic_class,
        normalized_semantics=normalized,
        dependency_class=dependency,
        purpose=purpose,
        dependency_scope=scope,
        required_contributors=required,
        optional_contributors=optional,
        native_basis_refs=basis_refs,
        family=family,
        ordered_evidence=ordered_evidence,
    )


def open_or_successor_obligation(
    admission: CoordinationAdmission,
    *,
    obligation_id: str | None = None,
    generation: int = 1,
    predecessor: CollaborationObligation | None = None,
) -> CollaborationObligation | None:
    """Create durable collection state only for a derived collective family."""
    if not isinstance(admission, CoordinationAdmission):
        raise CollaborationAdmissionError(
            "owner-derived coordination admission is required"
        )
    if admission.family is not CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE:
        return None
    if admission.dependency_class is None or admission.purpose is None:
        raise CollaborationAdmissionError("collective admission is incomplete")
    if obligation_id is None:
        obligation_id = (
            f"collaboration:{admission.interaction_id}:{admission.clause_id}"
        )
    if generation != 1 and predecessor is None:
        raise CollaborationAdmissionError(
            "non-initial generation requires an explicit predecessor"
        )
    if predecessor is not None:
        if not isinstance(predecessor, CollaborationObligation):
            raise CollaborationAdmissionError("successor predecessor is invalid")
        if obligation_id != predecessor.obligation_id:
            raise CollaborationAdmissionError(
                "successor must retain the obligation lineage identity"
            )
        if generation != predecessor.generation + 1:
            raise CollaborationAdmissionError(
                "successor generation must immediately follow its predecessor"
            )
        if (
            admission.campaign_id != predecessor.campaign_id
            or admission.interaction_id != predecessor.interaction_id
            or admission.intent_plan_id != predecessor.intent_plan_id
            or admission.clause_id != predecessor.clause_id
        ):
            raise CollaborationAdmissionError(
                "successor admission does not belong to the obligation lineage"
            )
        if predecessor.lifecycle in {"RESOLVED", "OBSOLETE"}:
            raise CollaborationAdmissionError(
                "terminal obligation cannot create a successor generation"
            )
    return CollaborationObligation(
        obligation_id=obligation_id,
        generation=generation,
        campaign_id=admission.campaign_id,
        interaction_id=admission.interaction_id,
        intent_plan_id=admission.intent_plan_id,
        clause_id=admission.clause_id,
        semantic_class=admission.semantic_class,
        dependency_class=admission.dependency_class,
        purpose=admission.purpose,
        dependency_scope=admission.dependency_scope,
        native_basis_refs=admission.native_basis_refs,
        required_contributors=admission.required_contributors,
        optional_contributors=admission.optional_contributors,
        accepted_input_uses=(admission.opportunity_identity,),
        accepted_input_contributors=(
            (
                admission.opportunity_identity,
                ContributorRef(admission.initiating_player_id),
            ),
        ),
        predecessor_generation=None if predecessor is None else predecessor.generation,
    )


def associate_input(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    interaction_id: str,
    clause_id: str,
    *,
    principal: object,
    player_route: object,
    generation: int | None = None,
) -> CollaborationObligation:
    """Associate one current accepted clause by reference only.

    The Interaction/IntentPlan owner remains the source of semantic content.  This
    operation carries only its exact identity and the revalidated PLAYER holder;
    it never copies message or clause bodies into the obligation.
    """
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    identity = (
        _id(interaction_id, "input interaction_id"),
        _id(clause_id, "input clause_id"),
    )
    try:
        basis = _operation_basis(host, None)
    except (AttributeError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError("bound runtime host is required") from exc
    _obligation_basis, current = _read_current_obligation(
        obligation.obligation_id, host, basis=basis
    )
    if current.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "input obligation belongs to another campaign"
        )
    if current.generation != obligation.generation:
        raise CollaborationAdmissionError(
            "input targets a non-current collaboration generation"
        )
    if generation is not None and generation != current.generation:
        raise CollaborationAdmissionError(
            "input targets a stale collaboration generation"
        )
    if current.lifecycle != "OPEN":
        raise CollaborationAdmissionError("only an open obligation accepts input")
    _revalidate_obligation_native_basis(current, host, basis=basis)
    current_player, current_route_refs = _resolve_join_player(
        host,
        basis,
        principal=principal,
        player_route=player_route,
    )
    if (current.obligation_id, current.generation) not in current_route_refs:
        raise CollaborationAdmissionError(
            "current PLAYER collaboration route does not carry the obligation"
        )
    interaction = _load_interaction(host, basis, interaction_id)
    plan = _load_plan(
        host,
        basis,
        _id(interaction["intent_plan_id"], "input intent_plan_id"),
        interaction_id,
    )
    clause = _load_clause(plan, clause_id)
    if interaction.get("player_id") != current_player.player_id:
        raise CollaborationAdmissionError(
            "input Interaction is not owned by the current PLAYER"
        )
    permitted = current.required_contributors + current.optional_contributors
    participant = next(
        (ref for ref in permitted if ref.player_id == current_player.player_id),
        None,
    )
    if participant is None:
        raise CollaborationAdmissionError("current PLAYER is not a contributor")
    if (
        participant.pc_id is not None
        and participant.pc_id not in current_player.controlled_pc_ids
    ):
        raise CollaborationAdmissionError("current PLAYER does not control required PC")
    input_semantic_class = clause.get("collaboration_semantic_class")
    if input_semantic_class not in _SEMANTIC_CLASSES:
        raise CollaborationAdmissionError(
            "collaboration input semantic class is required"
        )
    if input_semantic_class != current.semantic_class:
        raise CollaborationAdmissionError(
            "collaboration input semantic class is incompatible with obligation"
        )
    if identity in current.accepted_input_uses:
        existing_contributor = dict(current.accepted_input_contributors)[identity]
        if existing_contributor != participant:
            raise CollaborationAdmissionError(
                "accepted input contributor does not match current PLAYER"
            )
        return current
    uses = current.accepted_input_uses + (identity,)
    contributors = current.accepted_input_contributors + ((identity, participant),)
    return replace(
        current,
        accepted_input_uses=uses,
        accepted_input_contributors=contributors,
    )


def _revalidate_obligation_native_basis(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> None:
    """Revalidate an obligation's finite native basis without scanning."""
    basis = _operation_basis(host, basis)
    if basis.pinned_campaign.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "collaboration obligation belongs to another campaign"
        )
    try:
        _validate_basis_shape(
            obligation.dependency_class,
            obligation.dependency_scope,
            obligation.native_basis_refs,
        )
    except (CollaborationAdmissionError, KeyError) as exc:
        raise CollaborationAdmissionError(
            "collaboration obligation basis is invalid"
        ) from exc
    for ref in obligation.native_basis_refs:
        owner = _read_native(host, basis, ref.family, ref.record_id)
        if owner.get("revision") != ref.revision:
            raise CollaborationAdmissionError(
                "collaboration native basis is not current"
            )
    _revalidate_host_basis(host, basis)


def _read_current_obligation_state(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> tuple[int, str]:
    """Read the exact current obligation owner before using a caller object.

    ``CollaborationObligation`` uses ``obligation_id`` as its native identity,
    unlike the generic ``id`` field used by most runtime records.  Keep this
    owner-specific route local rather than teaching a second identity rule to a
    shared storage helper.  The caller-held value is only a candidate; current
    generation and lifecycle come from this exact owner read.
    """
    try:
        basis = _operation_basis(host, basis)
        route = route_native_record(
            "runtime.collaboration_obligation", (obligation.obligation_id,)
        )
        raw = host._repository.read_exact_path(
            basis.pinned_campaign, route.relative_path
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "current collaboration obligation owner is unavailable"
        ) from exc
    current = _mapping(raw, "current collaboration obligation")
    if (
        current.get("schema_version") != COLLABORATION_SCHEMA_VERSION
        or current.get("kind") != "runtime.collaboration_obligation"
    ):
        raise CollaborationAdmissionError(
            "current collaboration obligation owner schema is unsupported"
        )
    if current.get("obligation_id") != obligation.obligation_id:
        raise CollaborationAdmissionError(
            "current collaboration obligation identity differs from the request"
        )
    if current.get("campaign_id") != basis.pinned_campaign.campaign_id:
        raise CollaborationAdmissionError(
            "current collaboration obligation belongs to another campaign"
        )
    generation = current.get("generation")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
        raise CollaborationAdmissionError(
            "current collaboration obligation generation is invalid"
        )
    lifecycle = current.get("lifecycle")
    if not isinstance(lifecycle, str) or lifecycle not in {
        "OPEN",
        "CLOSED",
        "RESOLVED",
        "OBSOLETE",
    }:
        raise CollaborationAdmissionError(
            "current collaboration obligation lifecycle is invalid"
        )
    _revalidate_host_basis(host, basis)
    return generation, lifecycle


def _read_current_obligation(
    obligation_id: str,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> tuple[_OperationBasis, CollaborationObligation]:
    """Load one obligation through its exact native route for recovery/closure."""
    _id(obligation_id, "current collaboration obligation_id")
    try:
        basis = _operation_basis(host, basis)
        route = route_native_record(
            "runtime.collaboration_obligation", (obligation_id,)
        )
        raw = host._repository.read_exact_path(
            basis.pinned_campaign, route.relative_path
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "current collaboration obligation owner is unavailable"
        ) from exc
    current = _mapping(raw, "current collaboration obligation")
    if current.get("kind") != "runtime.collaboration_obligation":
        raise CollaborationAdmissionError(
            "current collaboration obligation owner schema is unsupported"
        )
    if current.get("obligation_id") != obligation_id:
        raise CollaborationAdmissionError(
            "current collaboration obligation identity differs from the request"
        )
    if current.get("campaign_id") != basis.pinned_campaign.campaign_id:
        raise CollaborationAdmissionError(
            "current collaboration obligation belongs to another campaign"
        )
    obligation = CollaborationObligation.from_mapping(current, host=host, basis=basis)
    _revalidate_host_basis(host, basis)
    return basis, obligation


def recover_obligation(
    host: RuntimeHost, obligation_id: str
) -> CollaborationObligation:
    """Recover exactly one persisted collaboration obligation by known ID."""
    _basis, obligation = _read_current_obligation(obligation_id, host)
    return obligation


def _obligation_route(obligation: CollaborationObligation):
    """Build the W02 route carrier without creating a collaboration publisher."""
    return route_serialized_operation(
        "runtime.collaboration_obligation",
        obligation.obligation_id,
        obligation.to_mapping(),
    )


def _publish_obligation_delta(
    host: RuntimeHost,
    obligation: CollaborationObligation,
    path_operations: Mapping[str, object | None],
    *,
    reason: str,
    basis: _OperationBasis | None = None,
) -> PublicationOutcome:
    """Submit one collaboration delta through RuntimeHost's W02 service."""
    try:
        outcome = host.publication.publish_owner_delta(
            routed_operation=_obligation_route(obligation),
            path_operations=path_operations,
            owner_generations={
                "runtime.collaboration_obligation": obligation.generation
            },
            publication_reason=reason,
            basis=basis,
        )
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "collaboration publication failed closed"
        ) from exc
    if not isinstance(outcome, PublicationOutcome):
        raise CollaborationAdmissionError(
            "collaboration publication result is not W02 owner-typed"
        )
    if outcome.status is not PublicationStatus.ACCEPTED:
        raise CollaborationAdmissionError(
            "collaboration publication was not confirmed accepted"
        )
    return outcome


def _player_route_refs(
    player: Mapping[str, object], label: str
) -> list[tuple[str, int]]:
    raw_refs = player.get("collaboration_route_refs", ())
    if not isinstance(raw_refs, Sequence) or isinstance(raw_refs, (str, bytes)):
        raise CollaborationAdmissionError(f"{label} route companion is malformed")
    refs: list[tuple[str, int]] = []
    for raw_ref in raw_refs:
        ref = _mapping(raw_ref, f"{label} route reference")
        if set(ref) != {"obligation_id", "generation"}:
            raise CollaborationAdmissionError(
                f"{label} route reference fields are not strict"
            )
        ref_id = _id(ref["obligation_id"], f"{label} obligation_id")
        generation = ref["generation"]
        if (
            isinstance(generation, bool)
            or not isinstance(generation, int)
            or generation < 1
        ):
            raise CollaborationAdmissionError(f"{label} route generation is invalid")
        refs.append((ref_id, generation))
    if len(refs) != len(set(refs)):
        raise CollaborationAdmissionError(f"{label} route references are duplicate")
    return refs


def _player_with_route_ref(
    player: Mapping[str, object], obligation: CollaborationObligation
) -> dict[str, object]:
    result = deepcopy(dict(player))
    refs = set(_player_route_refs(player, "PLAYER"))
    refs.add((obligation.obligation_id, obligation.generation))
    result["collaboration_route_refs"] = [
        {"obligation_id": ref_id, "generation": generation}
        for ref_id, generation in sorted(refs)
    ]
    return result


def _player_without_route_ref(
    player: Mapping[str, object], obligation: CollaborationObligation
) -> dict[str, object]:
    result = deepcopy(dict(player))
    refs = set(_player_route_refs(player, "PLAYER"))
    refs.discard((obligation.obligation_id, obligation.generation))
    result["collaboration_route_refs"] = [
        {"obligation_id": ref_id, "generation": generation}
        for ref_id, generation in sorted(refs)
    ]
    return result


def _route_companion_operations(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    *,
    retain: bool,
    basis: _OperationBasis | None = None,
) -> dict[str, object]:
    if basis is None:
        try:
            basis = host._begin_operation()
        except (AttributeError, TypeError, ValueError) as exc:
            raise CollaborationAdmissionError(
                "runtime host is required for route-companion publication"
            ) from exc
    operations: dict[str, object] = {}
    for player_id in _prior_route_holder_ids(obligation):
        player = _read_native(host, basis, "world.player", player_id)
        value = (
            _player_with_route_ref(player, obligation)
            if retain
            else _player_without_route_ref(player, obligation)
        )
        operations[route_native_record("world.player", (player_id,)).relative_path] = (
            value
        )
    _revalidate_host_basis(host, basis)
    return operations


def _closed_publication_operations(
    closed: CollaborationObligation,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> dict[str, object | None]:
    operations: dict[str, object | None] = {
        route_native_record(
            "runtime.collaboration_obligation", (closed.obligation_id,)
        ).relative_path: closed.to_mapping()
    }
    operations.update(
        _route_companion_operations(closed, host, retain=True, basis=basis)
    )
    return operations


def publish_closed(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    generation: int | None = None,
) -> CollaborationObligation:
    """Persist OPEN -> CLOSED through one W02 campaign publication attempt."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    basis, current = _read_current_obligation(obligation.obligation_id, host)
    if current.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "collaboration obligation belongs to another campaign"
        )
    if current.generation != obligation.generation:
        raise CollaborationAdmissionError(
            "close publication targets a stale generation"
        )
    if generation is not None and generation != current.generation:
        raise CollaborationAdmissionError(
            "close publication targets a stale generation"
        )
    if current.lifecycle in {"CLOSED", "RESOLVED"}:
        candidate_fingerprint = _closed_input_set_fingerprint(
            obligation.accepted_input_uses,
            obligation.accepted_input_contributors,
        )
        if current.closed_input_set_fingerprint != candidate_fingerprint:
            raise CollaborationAdmissionError(
                "close publication targets a different input fingerprint"
            )
        if (
            obligation.closed_input_set_fingerprint is not None
            and current.closed_input_set_fingerprint
            != obligation.closed_input_set_fingerprint
        ):
            raise CollaborationAdmissionError(
                "close publication targets a different input fingerprint"
            )
        return current
    if current.lifecycle != "OPEN":
        raise CollaborationAdmissionError(
            "only an open collaboration obligation can be durably closed"
        )
    closed = close_obligation(
        current, host=host, generation=current.generation, basis=basis
    )
    _publish_obligation_delta(
        host,
        closed,
        _closed_publication_operations(closed, host, basis=basis),
        reason="collaboration-close",
        basis=basis,
    )
    return closed


def _load_obligation_clause(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    interaction_id: str,
    clause_id: str,
    *,
    basis: _OperationBasis | None = None,
) -> Mapping[str, object]:
    basis = _operation_basis(host, basis)
    interaction = _load_interaction(host, basis, interaction_id)
    plan = _load_plan(
        host,
        basis,
        _id(interaction["intent_plan_id"], "handoff intent_plan_id"),
        interaction_id,
    )
    clause = _load_clause(plan, clause_id)
    if interaction.get("campaign_id") != obligation.campaign_id:
        raise CollaborationAdmissionError("handoff input belongs to another campaign")
    _revalidate_host_basis(host, basis)
    return clause


def close_obligation(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    generation: int | None = None,
    basis: _OperationBasis | None = None,
) -> CollaborationObligation:
    """Freeze one current complete collection without handing it to execution."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    basis = _operation_basis(host, basis)
    current_generation, current_lifecycle = _read_current_obligation_state(
        obligation, host, basis=basis
    )
    if current_generation != obligation.generation:
        raise CollaborationAdmissionError(
            "close targets a non-current collaboration generation"
        )
    if generation is not None and generation != current_generation:
        raise CollaborationAdmissionError(
            "close targets a stale collaboration generation"
        )
    if current_lifecycle != obligation.lifecycle:
        raise CollaborationAdmissionError(
            "close targets a stale collaboration lifecycle"
        )
    if obligation.lifecycle in {"CLOSED", "RESOLVED"}:
        return obligation
    if obligation.lifecycle != "OPEN":
        raise CollaborationAdmissionError("only an open obligation can close")
    _revalidate_obligation_native_basis(obligation, host, basis=basis)
    _validate_persisted_input_owners(obligation, host, basis=basis)
    pending = _pending_required_contributors(obligation)
    if pending:
        raise CollaborationAdmissionError(
            "required collaboration inputs remain unsatisfied"
        )
    clause = _load_obligation_clause(
        obligation,
        host,
        obligation.interaction_id,
        obligation.clause_id,
        basis=basis,
    )
    if clause.get("ordering_resolution_id") is not None:
        raise CollaborationAdmissionError(
            "native ordered owner took over before collaboration close"
        )
    if obligation.semantic_class == "ACTIONABLE_INTENT" and (
        clause.get("execution_state") != "intent.pending"
        or clause.get("command_id") is not None
    ):
        raise CollaborationAdmissionError(
            "collaboration-held actionable clause is no longer pre-command"
        )
    final_generation, final_lifecycle = _read_current_obligation_state(
        obligation, host, basis=basis
    )
    if final_generation != obligation.generation or final_lifecycle != "OPEN":
        raise CollaborationAdmissionError(
            "collaboration generation changed during close"
        )
    fingerprint = _closed_input_set_fingerprint(
        obligation.accepted_input_uses,
        obligation.accepted_input_contributors,
    )
    return replace(
        obligation,
        lifecycle="CLOSED",
        closed_input_set_fingerprint=fingerprint,
    )


def _handoff_disposition(
    obligation: CollaborationObligation,
    identity: tuple[str, str],
    clause: Mapping[str, object],
) -> tuple[HandoffDisposition, str | None]:
    if identity == (obligation.interaction_id, obligation.clause_id):
        if obligation.semantic_class == "ACTIONABLE_INTENT":
            if (
                clause.get("execution_state") != "intent.pending"
                or clause.get("command_id") is not None
            ):
                raise CollaborationAdmissionError(
                    "held actionable clause must remain pre-command until handoff"
                )
            return (
                HandoffDisposition.RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH,
                "intent.ready",
            )
        return (
            HandoffDisposition.CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT,
            str(clause.get("execution_state")),
        )
    if clause.get("ordering_resolution_id") is not None:
        return (
            HandoffDisposition.HAND_TO_EXISTING_NATIVE_OWNER,
            str(clause.get("execution_state")),
        )
    if clause.get("mapping_outcome") in {"clarification_required", "unsupported"}:
        return HandoffDisposition.CLARIFICATION_OR_UNSUPPORTED, str(
            clause.get("execution_state")
        )
    return HandoffDisposition.CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT, str(
        clause.get("execution_state")
    )


def build_handoff(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    basis: _OperationBasis | None = None,
) -> CollaborationHandoff:
    """Build deterministic ephemeral handoff evidence for a CLOSED collection."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    basis = _operation_basis(host, basis)
    current_generation, current_lifecycle = _read_current_obligation_state(
        obligation, host, basis=basis
    )
    if current_generation != obligation.generation:
        raise CollaborationAdmissionError(
            "handoff targets a non-current collaboration generation"
        )
    if current_lifecycle != obligation.lifecycle:
        raise CollaborationAdmissionError(
            "handoff targets a stale collaboration lifecycle"
        )
    if obligation.lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "collaboration handoff requires a CLOSED obligation"
        )
    closed_basis = obligation.closed_basis
    _revalidate_obligation_native_basis(obligation, host, basis=basis)
    _validate_persisted_input_owners(obligation, host, basis=basis)
    entries: list[CollaborationHandoffEntry] = []
    for identity in closed_basis.accepted_input_uses:
        clause = _load_obligation_clause(obligation, host, *identity, basis=basis)
        disposition, execution_state = _handoff_disposition(
            obligation, identity, clause
        )
        entries.append(
            CollaborationHandoffEntry(
                interaction_id=identity[0],
                clause_id=identity[1],
                semantic_class=_text(
                    clause.get("collaboration_semantic_class"),
                    "handoff semantic class",
                ),
                disposition=disposition,
                execution_state=execution_state,
            )
        )
    final_generation, final_lifecycle = _read_current_obligation_state(
        obligation, host, basis=basis
    )
    if final_generation != obligation.generation or final_lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "collaboration generation changed during handoff"
        )
    return CollaborationHandoff(basis=closed_basis, entries=tuple(entries))


def apply_handoff(
    obligation: CollaborationObligation,
    handoff: CollaborationHandoff,
    *,
    host: RuntimeHost,
) -> CollaborationObligation:
    """Validate a handoff without claiming T02B's publication closure."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    if not isinstance(handoff, CollaborationHandoff):
        raise CollaborationAdmissionError("typed collaboration handoff is required")
    current_generation, current_lifecycle = _read_current_obligation_state(
        obligation, host
    )
    if current_generation != obligation.generation:
        raise CollaborationAdmissionError(
            "handoff targets a non-current collaboration generation"
        )
    if obligation.lifecycle == "RESOLVED":
        if current_lifecycle != "RESOLVED":
            raise CollaborationAdmissionError(
                "handoff targets a stale collaboration lifecycle"
            )
        return obligation
    if obligation.lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "collaboration handoff requires a CLOSED obligation"
        )
    if current_lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "handoff targets a stale collaboration lifecycle"
        )
    if handoff.basis != obligation.closed_basis:
        raise CollaborationAdmissionError(
            "handoff basis differs from the closed collaboration collection"
        )
    expected = build_handoff(obligation, host=host)
    if handoff != expected:
        raise CollaborationAdmissionError(
            "handoff does not match current native owner classification"
        )
    for entry in handoff.entries:
        if (
            entry.disposition
            is not HandoffDisposition.RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
        ):
            continue
        clause = _load_obligation_clause(
            obligation, host, entry.interaction_id, entry.clause_id
        )
        if clause.get("execution_state") == "intent.pending":
            # T02A has no campaign publication writer.  Keep the collection
            # CLOSED until T02B atomically updates the native IntentClause and
            # the obligation/routing closure together.
            return obligation
        if clause.get("execution_state") != entry.execution_state:
            raise CollaborationAdmissionError(
                "native actionable clause handoff state is invalid"
            )
        if clause.get("command_id") is not None:
            raise CollaborationAdmissionError(
                "native actionable clause handoff cannot carry a command"
            )
    final_generation, final_lifecycle = _read_current_obligation_state(obligation, host)
    if final_generation != obligation.generation or final_lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "collaboration generation changed during handoff application"
        )
    # T02A is read-only with respect to campaign-native owners.  Even when a
    # caller presents a clause that already looks ready, only T02B's atomic
    # publication closure may pair that owner transition with RESOLVED.
    return obligation


def _resolution_publication_operations(
    current: CollaborationObligation,
    handoff: CollaborationHandoff,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> tuple[CollaborationObligation, dict[str, object | None]]:
    basis = _operation_basis(host, basis)
    expected = build_handoff(current, host=host, basis=basis)
    if handoff != expected:
        raise CollaborationAdmissionError(
            "handoff does not match current native collaboration owner"
        )
    interaction = _load_interaction(host, basis, current.interaction_id)
    plan_id = _id(interaction["intent_plan_id"], "collaboration intent_plan_id")
    plan = _load_plan(host, basis, plan_id, current.interaction_id)
    clauses = list(_sequence(plan.get("clauses"), "intent plan clauses"))
    target_identity = (current.interaction_id, current.clause_id)
    indexes = [
        index
        for index, raw_clause in enumerate(clauses)
        if isinstance(raw_clause, Mapping)
        and raw_clause.get("clause_id") == current.clause_id
    ]
    if len(indexes) != 1:
        raise CollaborationAdmissionError(
            "collaboration IntentClause identity is missing or ambiguous"
        )
    target_index = indexes[0]
    target_clause = _mapping(clauses[target_index], "collaboration IntentClause")
    should_release = any(
        entry.input_identity == target_identity
        and entry.disposition
        is HandoffDisposition.RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
        for entry in handoff.entries
    )
    transitioned_plan = deepcopy(dict(plan))
    if should_release:
        if target_clause.get("execution_state") != "intent.pending":
            raise CollaborationAdmissionError(
                "collaboration IntentClause is not pending for native release"
            )
        if target_clause.get("command_id") is not None:
            raise CollaborationAdmissionError(
                "collaboration IntentClause already has a command"
            )
        transitioned_clause = deepcopy(dict(target_clause))
        transitioned_clause["execution_state"] = "intent.ready"
        clauses[target_index] = transitioned_clause
        transitioned_plan["clauses"] = clauses
    if should_release:
        operations: dict[str, object | None] = {
            route_native_record(
                "runtime.intent_plan", (plan_id,)
            ).relative_path: transitioned_plan
        }
    else:
        operations = {}
    resolved = replace(current, lifecycle="RESOLVED")
    operations.update(
        {
            route_native_record(
                "runtime.collaboration_obligation", (current.obligation_id,)
            ).relative_path: resolved.to_mapping(),
        }
    )
    operations.update(
        _route_companion_operations(current, host, retain=False, basis=basis)
    )
    _revalidate_host_basis(host, basis)
    return resolved, operations


def _validate_resolved_waiting_state(
    current: CollaborationObligation,
    handoff: CollaborationHandoff,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> None:
    basis = _operation_basis(host, basis)
    if handoff.basis != current.closed_basis:
        raise CollaborationAdmissionError(
            "resolved collaboration handoff basis differs from current owner"
        )
    interaction = _load_interaction(host, basis, current.interaction_id)
    plan = _load_plan(
        host,
        basis,
        _id(interaction["intent_plan_id"], "resolved intent_plan_id"),
        current.interaction_id,
    )
    clause = _load_clause(plan, current.clause_id)
    if current.semantic_class == "ACTIONABLE_INTENT" and (
        clause.get("execution_state") != "intent.ready"
        or clause.get("command_id") is not None
    ):
        raise CollaborationAdmissionError(
            "resolved collaboration IntentClause is not native-ready"
        )
    for player_id in _prior_route_holder_ids(current):
        player = _read_native(host, basis, "world.player", player_id)
        if (current.obligation_id, current.generation) in set(
            _player_route_refs(player, "PLAYER")
        ):
            raise CollaborationAdmissionError(
                "resolved collaboration route companion was not removed"
            )
    _revalidate_host_basis(host, basis)


def resolve_waiting(
    obligation: CollaborationObligation,
    handoff: CollaborationHandoff,
    *,
    host: RuntimeHost,
) -> CollaborationObligation:
    """Persist CLOSED -> RESOLVED as one same-campaign owner closure."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    if not isinstance(handoff, CollaborationHandoff):
        raise CollaborationAdmissionError("typed collaboration handoff is required")
    basis, current = _read_current_obligation(obligation.obligation_id, host)
    if current.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "collaboration obligation belongs to another campaign"
        )
    if current.generation != obligation.generation:
        raise CollaborationAdmissionError(
            "resolve targets a stale collaboration generation"
        )
    if current.lifecycle == "RESOLVED" and obligation.lifecycle == "CLOSED":
        if (
            current.closed_input_set_fingerprint
            != obligation.closed_input_set_fingerprint
        ):
            raise CollaborationAdmissionError(
                "resolve targets a different input fingerprint"
            )
        _validate_resolved_waiting_state(current, handoff, host, basis=basis)
        return current
    if current.lifecycle != obligation.lifecycle:
        raise CollaborationAdmissionError(
            "resolve targets a stale collaboration lifecycle"
        )
    if current.closed_input_set_fingerprint != obligation.closed_input_set_fingerprint:
        raise CollaborationAdmissionError(
            "resolve targets a different input fingerprint"
        )
    if current.lifecycle == "RESOLVED":
        _validate_resolved_waiting_state(current, handoff, host, basis=basis)
        return current
    if current.lifecycle == "OBSOLETE":
        raise CollaborationAdmissionError(
            "obsolete collaboration obligation cannot resolve"
        )
    if current.lifecycle != "CLOSED":
        raise CollaborationAdmissionError(
            "collaboration resolution requires a CLOSED obligation"
        )
    resolved, operations = _resolution_publication_operations(
        current, handoff, host, basis=basis
    )
    _publish_obligation_delta(
        host,
        resolved,
        operations,
        reason="collaboration-resolve",
        basis=basis,
    )
    return resolved


def obsolete_generation(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    generation: int | None = None,
) -> CollaborationObligation:
    """Persist OPEN/CLOSED -> OBSOLETE with exact route-companion removal."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    basis, current = _read_current_obligation(obligation.obligation_id, host)
    if current.campaign_id != obligation.campaign_id:
        raise CollaborationAdmissionError(
            "collaboration obligation belongs to another campaign"
        )
    if current.generation != obligation.generation:
        raise CollaborationAdmissionError(
            "obsolete transition targets a stale collaboration generation"
        )
    if generation is not None and generation != current.generation:
        raise CollaborationAdmissionError(
            "obsolete transition targets a stale collaboration generation"
        )
    if current.lifecycle == "OBSOLETE":
        if (
            current.closed_input_set_fingerprint
            != obligation.closed_input_set_fingerprint
        ):
            raise CollaborationAdmissionError(
                "obsolete transition targets a different input fingerprint"
            )
        _validate_terminal_route_removal(current, host, basis=basis)
        return current
    if current.lifecycle == "RESOLVED":
        raise CollaborationAdmissionError(
            "resolved collaboration obligation cannot become obsolete"
        )
    if current.lifecycle not in {"OPEN", "CLOSED"}:
        raise CollaborationAdmissionError(
            "only an open or closed collaboration obligation can become obsolete"
        )
    _validate_persisted_input_owners(current, host, basis=basis)
    if current.lifecycle == "CLOSED":
        CollaborationClosedBasis.from_obligation(current)
    obsolete = replace(current, lifecycle="OBSOLETE")
    operations: dict[str, object | None] = {
        route_native_record(
            "runtime.collaboration_obligation", (obsolete.obligation_id,)
        ).relative_path: obsolete.to_mapping()
    }
    operations.update(
        _route_companion_operations(obsolete, host, retain=False, basis=basis)
    )
    _publish_obligation_delta(
        host,
        obsolete,
        operations,
        reason="collaboration-obsolete",
        basis=basis,
    )
    return obsolete


def _validate_terminal_route_removal(
    obligation: CollaborationObligation,
    host: RuntimeHost,
    *,
    basis: _OperationBasis | None = None,
) -> None:
    basis = _operation_basis(host, basis)
    for player_id in _prior_route_holder_ids(obligation):
        player = _read_native(host, basis, "world.player", player_id)
        if (obligation.obligation_id, obligation.generation) in set(
            _player_route_refs(player, "PLAYER")
        ):
            raise CollaborationAdmissionError(
                "terminal collaboration route companion was not removed"
            )
    _revalidate_host_basis(host, basis)


# Name aliases keep the owner vocabulary explicit at call sites without adding
# another lifecycle or execution authority.
close_collaboration = close_obligation
handoff_collaboration = build_handoff
complete_collaboration_handoff = apply_handoff
ClosedCollectionBasis = CollaborationClosedBasis
resolve_collaboration_waiting = resolve_waiting
obsolete_collaboration = obsolete_generation


def required_route_holders(obligation: CollaborationObligation) -> tuple[str, ...]:
    """Return bounded current PLAYER identities that must recover an obligation."""
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    if obligation.lifecycle in {"RESOLVED", "OBSOLETE"}:
        return ()
    return _prior_route_holder_ids(obligation)


def _prior_route_holder_ids(
    obligation: CollaborationObligation,
) -> tuple[str, ...]:
    """Retain the former bounded holder set for terminal route cleanup."""
    holders = {ref.player_id for ref in obligation.required_contributors}
    holders.update(
        contributor.player_id
        for _, contributor in obligation.accepted_input_contributors
    )
    return tuple(sorted(holders))


def reconcile_player_route_companions(
    obligation: CollaborationObligation,
) -> tuple[PlayerRouteCompanion, ...]:
    """Build every bounded PLAYER companion for one obligation closure.

    Terminal generations retain the former holder set only to emit explicit
    route-ref removals.  No companion field is an authorization or currentness
    verdict; consumers must dereference the obligation and revalidate owners.
    """
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    holder_ids = _prior_route_holder_ids(obligation)
    refs = (
        ()
        if obligation.lifecycle in {"RESOLVED", "OBSOLETE"}
        else (CollaborationRouteRef(obligation.obligation_id, obligation.generation),)
    )
    return tuple(
        PlayerRouteCompanion(obligation.campaign_id, player_id, refs)
        for player_id in holder_ids
    )


def _canonical_frontier_refs(
    refs: Sequence[NativeBasisRef], label: str
) -> tuple[NativeBasisRef, ...]:
    if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes)):
        raise CollaborationAdmissionError(f"{label} must be an array")
    typed = tuple(refs)
    if not typed or any(
        not isinstance(ref, NativeBasisRef) or ref.revision is None for ref in typed
    ):
        raise CollaborationAdmissionError(
            f"{label} must contain current owner evidence"
        )
    if len(set(typed)) != len(typed):
        raise CollaborationAdmissionError(f"{label} must be unique")
    return tuple(
        sorted(
            typed,
            key=lambda ref: (ref.family, ref.record_id, ref.revision or ""),
        )
    )


def _pending_required_contributors(
    obligation: CollaborationObligation,
) -> tuple[ContributorRef, ...]:
    accepted = {
        (contributor.player_id, contributor.pc_id)
        for _, contributor in obligation.accepted_input_contributors
    }
    pending = tuple(
        contributor
        for contributor in obligation.required_contributors
        if (contributor.player_id, contributor.pc_id) not in accepted
    )
    return tuple(sorted(pending, key=lambda ref: (ref.player_id, ref.pc_id or "")))


def compute_maximal_safe_frontier(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    safe_prefix_refs: Sequence[NativeBasisRef] | None = None,
    current_basis_refs: Sequence[NativeBasisRef] | None = None,
    pending_required_contributors: Sequence[ContributorRef] | None = None,
) -> CollaborationFrontier:
    """Compute the latest safe owner-evidence boundary for one obligation.

    This is a scope-local projection.  It does not close an obligation, infer
    chronology from technical order, or use timeout/presence/silence as a
    substitute for a required contribution.  The legacy projection arguments
    are accepted only for call-site compatibility and are deliberately ignored;
    current basis and pending contributors are derived below from owner state.
    """
    if not isinstance(obligation, CollaborationObligation):
        raise CollaborationAdmissionError("owner-derived obligation is required")
    if obligation.lifecycle != "OPEN":
        raise CollaborationAdmissionError(
            "maximal safe frontier requires an open obligation"
        )
    del safe_prefix_refs, current_basis_refs, pending_required_contributors
    safe = _revalidate_frontier_basis(obligation, host)
    pending = _pending_required_contributors(obligation)
    return CollaborationFrontier(
        obligation_id=obligation.obligation_id,
        generation=obligation.generation,
        campaign_id=obligation.campaign_id,
        dependency_scope=obligation.dependency_scope,
        safe_prefix_refs=safe,
        pending_required_contributors=pending,
    )


def build_join_frontier(
    obligation: CollaborationObligation,
    *,
    host: RuntimeHost,
    current_basis_refs: Sequence[NativeBasisRef] | None = None,
) -> CollaborationFrontier:
    """Build one current, scope-local frontier for a participant join.

    Joining does not merge unrelated obligations or create a global current
    frontier.  The exact owner basis is rechecked by
    :func:`compute_maximal_safe_frontier`.
    """
    return compute_maximal_safe_frontier(
        obligation,
        host=host,
        current_basis_refs=current_basis_refs,
    )


def validate_visible_consequence(
    frontier: CollaborationFrontier,
    *,
    obligation: CollaborationObligation,
    host: RuntimeHost,
    evidence_refs: Sequence[NativeBasisRef],
) -> None:
    """Require visible evidence to match a freshly recomputed safe frontier."""
    if not isinstance(frontier, CollaborationFrontier):
        raise CollaborationAdmissionError("collaboration frontier is required")
    authoritative = compute_maximal_safe_frontier(obligation, host=host)
    if frontier != authoritative:
        raise CollaborationAdmissionError(
            "visible consequence requires an authoritative current frontier"
        )
    visible = _canonical_frontier_refs(evidence_refs, "visible consequence evidence")
    if visible != authoritative.safe_prefix_refs:
        raise CollaborationAdmissionError(
            "visible consequence crosses the collaboration safe frontier"
        )


def _resolve_join_player(
    host: RuntimeHost,
    basis: _OperationBasis,
    *,
    principal: object,
    player_route: object,
) -> tuple[PlayerRecord, tuple[tuple[str, int], ...]]:
    """Resolve one active PLAYER and its exact native collaboration route refs."""

    try:
        resolution = resolve_player(
            principal,
            player_route,
            lambda candidate_id: _read_native(
                host, basis, "world.player", candidate_id
            ),
            campaign_id=basis.pinned_campaign.campaign_id,
        )
    except (
        AccessControlContractError,
        CollaborationAdmissionError,
        TypeError,
        ValueError,
    ) as exc:
        raise CollaborationAdmissionError(
            "current join PLAYER binding could not be resolved"
        ) from exc
    if resolution.status != "AUTHORIZED_PLAYER" or resolution.player is None:
        raise CollaborationAdmissionError(
            "join/rejoin requires an active current PLAYER binding"
        )
    player_id = resolution.player.player_id
    raw_player = _read_native(host, basis, "world.player", player_id)
    try:
        exact_player = PlayerRecord.from_mapping(raw_player)
    except (AccessControlContractError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(
            "current join PLAYER record is invalid"
        ) from exc
    if exact_player != resolution.player:
        raise CollaborationAdmissionError(
            "current join PLAYER binding changed during resolution"
        )
    return exact_player, tuple(_player_route_refs(raw_player, "current PLAYER"))


def _recipient_catch_up_entry(
    obligation: CollaborationObligation,
    *,
    player: PlayerRecord,
) -> CollaborationCatchUpEntry:
    required = tuple(
        ref
        for ref in obligation.required_contributors
        if ref.player_id == player.player_id
    )
    optional = tuple(
        ref
        for ref in obligation.optional_contributors
        if ref.player_id == player.player_id
    )
    accepted = tuple(
        contributor
        for _identity, contributor in obligation.accepted_input_contributors
        if contributor.player_id == player.player_id
    )
    if required:
        role = "REQUIRED"
        own_refs = required
    elif optional:
        role = "OPTIONAL"
        own_refs = optional
    elif accepted:
        role = "ORIGINATING"
        own_refs = accepted
    else:
        raise CollaborationAdmissionError(
            "current route obligation does not belong to the recipient"
        )
    own_pc_ids = tuple(sorted({ref.pc_id for ref in own_refs if ref.pc_id is not None}))
    if any(pc_id not in player.controlled_pc_ids for pc_id in own_pc_ids):
        raise CollaborationAdmissionError(
            "recipient no longer controls an obligation PC"
        )
    if accepted:
        contribution_status = "RECEIVED"
    elif role == "REQUIRED":
        contribution_status = "PENDING"
    else:
        contribution_status = "NOT_REQUIRED"
    return CollaborationCatchUpEntry(
        obligation_id=obligation.obligation_id,
        generation=obligation.generation,
        lifecycle=obligation.lifecycle,
        participant_role=role,
        own_pc_ids=own_pc_ids,
        contribution_status=contribution_status,
    )


def join_participant(
    host: RuntimeHost,
    *,
    principal: object,
    player_route: object,
    cursor_hint: str | None = None,
) -> CollaborationCatchUp:
    """Prepare bounded join/rejoin catch-up before any mutable gameplay input.

    The current W03 principal/PLAYER route and RuntimeHost campaign/LIVE basis
    are acquired first.  The PLAYER's exact native collaboration route refs
    then bound the only obligation IDs read.  This function produces an
    ephemeral projection; it does not authorize input, persist a cursor or
    assert that a human consumed the result.
    """

    basis = _operation_basis(host, None)
    player, route_refs = _resolve_join_player(
        host,
        basis,
        principal=principal,
        player_route=player_route,
    )
    entries: list[CollaborationCatchUpEntry] = []
    for obligation_id, route_generation in sorted(route_refs):
        _obligation_basis, obligation = _read_current_obligation(
            obligation_id, host, basis=basis
        )
        if obligation.generation != route_generation:
            raise CollaborationAdmissionError(
                "current PLAYER collaboration route points to a stale generation"
            )
        if obligation.lifecycle not in {"OPEN", "CLOSED"}:
            raise CollaborationAdmissionError(
                "current PLAYER collaboration route points to a terminal obligation"
            )
        _revalidate_obligation_native_basis(obligation, host, basis=basis)
        entries.append(_recipient_catch_up_entry(obligation, player=player))

    current_player, current_refs = _resolve_join_player(
        host,
        basis,
        principal=principal,
        player_route=player_route,
    )
    if current_player != player or current_refs != route_refs:
        raise CollaborationAdmissionError(
            "current PLAYER binding or collaboration route changed during catch-up"
        )
    _revalidate_host_basis(host, basis)
    return CollaborationCatchUp(
        campaign_id=basis.pinned_campaign.campaign_id,
        campaign_revision=basis.pinned_campaign.revision,
        player_id=player.player_id,
        controlled_pc_ids=player.controlled_pc_ids,
        live_source_keys=tuple(
            entry.source_key
            for entry in (basis.selected_live.entries if basis.selected_live else ())
        ),
        obligations=tuple(entries),
        cursor_hint=cursor_hint,
    )


def rejoin_participant(
    host: RuntimeHost,
    *,
    principal: object,
    player_route: object,
    cursor_hint: str | None = None,
) -> CollaborationCatchUp:
    """Use the same currentness-safe recipient projection for a rejoin."""

    return join_participant(
        host,
        principal=principal,
        player_route=player_route,
        cursor_hint=cursor_hint,
    )


build_recipient_catch_up = join_participant
