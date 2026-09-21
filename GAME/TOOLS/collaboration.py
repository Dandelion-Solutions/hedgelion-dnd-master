"""Native-owner-first collaboration admission.

Collaboration does not mint an opportunity, participant authority or currentness
token.  It reloads the accepted ``runtime.interaction`` and ``runtime.intent_plan``
through the host-injected repository capability, validates the embedded clause,
revalidates the current PLAYER/native basis, and returns one ephemeral derived
admission.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from .access_control import (
    AccessControlContractError,
    PlayerRecord,
    resolve_player,
)
from .native_storage import (
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .policy_basis import PinnedCampaign, RepositoryPort

# framework_module_version: 1.0.3
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.3"
COLLABORATION_SCHEMA_VERSION: Final[int] = 1

_ID_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_SEMANTIC_CLASSES: Final = frozenset(
    {"OOC_COORDINATION", "DIEGETIC_COMMUNICATION", "ACTIONABLE_INTENT", "CONTROL_SIGNAL"}
)
_DEPENDENCY_CLASSES: Final = frozenset(
    {
        "JOINT_VOLUNTARY_ACTION",
        "SHARED_DECISION_OR_NEGOTIATION",
        "SHARED_SCARCE_RESOURCE_CHOICE",
        "SCENE_CHRONOLOGY_CONVERGENCE",
        "PC_CONSEQUENCE_DECISION",
    }
)
_CLAUSE_FIELDS: Final = frozenset(
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
        "native_basis_refs",
    }
)


class CollaborationAdmissionError(ValueError):
    """Raised when native collaboration admission cannot be proved."""

    failure_code: str

    def __init__(self, message: str, *, failure_code: str = "collaboration.admission_invalid") -> None:
        super().__init__(message)
        self.failure_code = failure_code


class CoordinationFamily(StrEnum):
    """Closed derived coordination-family result."""

    INDEPENDENT_IMMEDIATE = "INDEPENDENT_IMMEDIATE"
    AGENCY_DEPENDENT_COLLECTIVE = "AGENCY_DEPENDENT_COLLECTIVE"
    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"


class DependencyClass(StrEnum):
    """The finite generation-1 material dependency vocabulary."""

    JOINT_VOLUNTARY_ACTION = "JOINT_VOLUNTARY_ACTION"
    SHARED_DECISION_OR_NEGOTIATION = "SHARED_DECISION_OR_NEGOTIATION"
    SHARED_SCARCE_RESOURCE_CHOICE = "SHARED_SCARCE_RESOURCE_CHOICE"
    SCENE_CHRONOLOGY_CONVERGENCE = "SCENE_CHRONOLOGY_CONVERGENCE"
    PC_CONSEQUENCE_DECISION = "PC_CONSEQUENCE_DECISION"


@dataclass(frozen=True, slots=True)
class _DependencyBasisRule:
    """Closed native basis owner for one ruled dependency class."""

    family: str
    scope_key: str


_DEPENDENCY_BASIS_RULES: Final[dict[DependencyClass, _DependencyBasisRule]] = {
    DependencyClass.JOINT_VOLUNTARY_ACTION: _DependencyBasisRule("world.scene", "scene_id"),
    DependencyClass.SHARED_DECISION_OR_NEGOTIATION: _DependencyBasisRule("world.scene", "scene_id"),
    DependencyClass.SHARED_SCARCE_RESOURCE_CHOICE: _DependencyBasisRule("world.asset", "asset_id"),
    DependencyClass.SCENE_CHRONOLOGY_CONVERGENCE: _DependencyBasisRule("world.scene", "scene_id"),
    DependencyClass.PC_CONSEQUENCE_DECISION: _DependencyBasisRule("world.actor", "actor_id"),
}
_ORDERED_OWNER_FAMILIES: Final = frozenset({"runtime.procedure", "runtime.continuation"})
_NATIVE_BASIS_FAMILIES: Final = frozenset(
    {rule.family for rule in _DEPENDENCY_BASIS_RULES.values()} | set(_ORDERED_OWNER_FAMILIES)
)
_COLLABORATION_READ_FAMILIES: Final = _NATIVE_BASIS_FAMILIES | frozenset(
    {"runtime.interaction", "runtime.intent_plan", "world.player"}
)


def _id(value: object, label: str) -> str:
    if not isinstance(value, str) or _ID_PATTERN.fullmatch(value) is None:
        raise CollaborationAdmissionError(f"{label} must be a native identifier")
    return value


def _nonempty(value: object, label: str) -> str:
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
        _id(self.player_id, "required contributor player_id")
        if self.pc_id is not None:
            _id(self.pc_id, "required contributor pc_id")

    def to_mapping(self) -> dict[str, str]:
        value = {"player_id": self.player_id}
        if self.pc_id is not None:
            value["pc_id"] = self.pc_id
        return value


@dataclass(frozen=True, slots=True)
class NativeBasisRef:
    """One explicit WP-11 known-ID native basis reference."""

    family: str
    record_id: str
    revision: str | None = None

    def __post_init__(self) -> None:
        if self.family not in _NATIVE_BASIS_FAMILIES:
            raise CollaborationAdmissionError("native basis family is not admitted for collaboration")
        _id(self.record_id, "native basis id")
        if self.revision is not None:
            _nonempty(self.revision, "native basis revision")

    @property
    def id(self) -> str:
        """Expose the owner identity using the schema's compact ``id`` spelling."""

        return self.record_id

    def to_mapping(self) -> dict[str, str]:
        value = {"family": self.family, "id": self.record_id}
        if self.revision is not None:
            value["revision"] = self.revision
        return value


@dataclass(frozen=True, slots=True)
class CoordinationAdmission:
    """Ephemeral collaboration result derived after complete revalidation."""

    campaign_id: str
    campaign_revision: str
    interaction_id: str
    intent_plan_id: str
    clause_id: str
    semantic_class: str | None
    normalized_semantics: Mapping[str, object]
    dependency_class: DependencyClass | None
    purpose: str | None
    dependency_scope: Mapping[str, object]
    required_contributors: tuple[ContributorRef, ...]
    native_basis_refs: tuple[NativeBasisRef, ...]
    family: CoordinationFamily
    ordered_owner_family: str | None = None

    def __post_init__(self) -> None:
        _id(self.campaign_id, "admission campaign_id")
        _nonempty(self.campaign_revision, "admission campaign revision")
        _id(self.interaction_id, "admission interaction_id")
        _id(self.intent_plan_id, "admission intent_plan_id")
        _id(self.clause_id, "admission clause_id")
        if self.semantic_class is not None and self.semantic_class not in _SEMANTIC_CLASSES:
            raise CollaborationAdmissionError("admission semantic class is not registered")
        if self.dependency_class is not None and self.dependency_class.value not in _DEPENDENCY_CLASSES:
            raise CollaborationAdmissionError("admission dependency class is not registered")
        object.__setattr__(self, "normalized_semantics", MappingProxyType(dict(_freeze(self.normalized_semantics))))
        object.__setattr__(self, "dependency_scope", MappingProxyType(dict(_freeze(self.dependency_scope))))

    @property
    def opportunity_identity(self) -> tuple[str, str]:
        return self.interaction_id, self.clause_id


@dataclass(frozen=True, slots=True)
class CollaborationObligation:
    """Derived durable-owner record for one admitted collective generation."""

    obligation_id: str
    generation: int
    campaign_id: str
    interaction_id: str
    intent_plan_id: str
    clause_id: str
    dependency_class: DependencyClass
    purpose: str
    dependency_scope: Mapping[str, object]
    native_basis_refs: tuple[NativeBasisRef, ...]
    required_contributors: tuple[ContributorRef, ...]
    coordination_family: CoordinationFamily = CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
    lifecycle: str = "OPEN"
    optional_contributors: tuple[ContributorRef, ...] = ()
    accepted_input_uses: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        _id(self.obligation_id, "obligation_id")
        if isinstance(self.generation, bool) or not isinstance(self.generation, int) or self.generation < 1:
            raise CollaborationAdmissionError("obligation generation must be a positive integer")
        if self.coordination_family is not CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE:
            raise CollaborationAdmissionError("only collective admissions create obligations")
        if self.lifecycle not in {"OPEN", "CLOSED", "RESOLVED", "OBSOLETE"}:
            raise CollaborationAdmissionError("obligation lifecycle is not registered")

    def to_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_SCHEMA_VERSION,
            "kind": "runtime.collaboration_obligation",
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "lifecycle": self.lifecycle,
            "coordination_family": self.coordination_family.value,
            "campaign_id": self.campaign_id,
            "interaction_id": self.interaction_id,
            "intent_plan_id": self.intent_plan_id,
            "clause_id": self.clause_id,
            "dependency_class": self.dependency_class.value,
            "purpose": self.purpose,
            "dependency_scope": _thaw(self.dependency_scope),
            "native_basis_refs": [ref.to_mapping() for ref in self.native_basis_refs],
            "required_contributors": [ref.to_mapping() for ref in self.required_contributors],
            "optional_contributors": [ref.to_mapping() for ref in self.optional_contributors],
            "accepted_input_uses": [
                {"interaction_id": interaction_id, "clause_id": clause_id}
                for interaction_id, clause_id in self.accepted_input_uses
            ],
        }


def _pin_campaign(repository: RepositoryPort, campaign_id: str) -> PinnedCampaign:
    _id(campaign_id, "campaign_id")
    try:
        pinned = repository.pin_campaign(campaign_id)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError("trusted campaign pin is unavailable") from exc
    if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
        raise CollaborationAdmissionError("repository did not return the exact campaign pin")
    return pinned


def _read_native(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    family: str,
    record_id: str,
) -> Mapping[str, object]:
    if family not in _COLLABORATION_READ_FAMILIES:
        raise CollaborationAdmissionError("native basis family is not admitted for collaboration")
    _id(record_id, f"{family} id")
    path = route_native_record(family, (record_id,)).relative_path
    try:
        raw = repository.read_exact_path(pinned, path)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError(f"exact {family} load failed") from exc
    payload = _mapping(raw, f"exact {family} record")
    try:
        validate_loaded_identity(family, (record_id,), payload)
    except (IdentityMismatch, NativeStorageError) as exc:
        raise CollaborationAdmissionError(f"exact {family} identity is stale or foreign") from exc
    if payload.get("campaign_id") not in {None, pinned.campaign_id}:
        raise CollaborationAdmissionError(f"exact {family} belongs to another campaign")
    return payload


def _load_interaction(
    repository: RepositoryPort, pinned: PinnedCampaign, interaction_id: str
) -> Mapping[str, object]:
    interaction = _read_native(repository, pinned, "runtime.interaction", interaction_id)
    declared_id = interaction.get("interaction_id", interaction.get("id"))
    if declared_id is not None and declared_id != interaction_id:
        raise CollaborationAdmissionError("interaction identity differs from requested identity")
    if interaction.get("campaign_id") != pinned.campaign_id:
        raise CollaborationAdmissionError("interaction belongs to another campaign")
    for field in ("session_id", "player_id", "input_message_id", "intent_plan_id"):
        _id(interaction.get(field), f"interaction {field}")
    return interaction


def _load_intent_plan(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    intent_plan_id: str,
    interaction_id: str,
) -> Mapping[str, object]:
    plan = _read_native(repository, pinned, "runtime.intent_plan", intent_plan_id)
    declared_id = plan.get("intent_plan_id", plan.get("id"))
    if declared_id is not None and declared_id != intent_plan_id:
        raise CollaborationAdmissionError("intent plan identity differs from interaction route")
    if plan.get("interaction_id") != interaction_id:
        raise CollaborationAdmissionError("intent plan is not owned by the interaction")
    return plan


def _load_clause(plan: Mapping[str, object], clause_id: str) -> Mapping[str, object]:
    raw_clauses = _sequence(plan.get("clauses"), "intent plan clauses")
    matches = [
        clause
        for clause in raw_clauses
        if isinstance(clause, Mapping) and clause.get("clause_id") == clause_id
    ]
    if len(matches) != 1:
        raise CollaborationAdmissionError("intent clause identity is missing or ambiguous")
    clause = matches[0]
    unexpected = set(clause) - _CLAUSE_FIELDS
    if unexpected:
        raise CollaborationAdmissionError("intent clause contains an unsupported field")
    if clause.get("execution_state") not in {
        "intent.pending",
        "intent.ready",
        "intent.executed",
        "intent.skipped_due_to_prior_result",
        "intent.failed",
    }:
        raise CollaborationAdmissionError("intent clause execution state is not registered")
    if clause.get("mapping_outcome") not in {
        "exact",
        "composed",
        "narrative_only",
        "clarification_required",
        "unsupported",
    }:
        raise CollaborationAdmissionError("intent clause mapping outcome is not registered")
    return clause


def _parse_contributors(value: object) -> tuple[ContributorRef, ...]:
    refs: list[ContributorRef] = []
    seen: set[tuple[str, str | None]] = set()
    for raw in _sequence(value, "required contributors"):
        contributor = _mapping(raw, "required contributor")
        if set(contributor) - {"player_id", "pc_id"} or "player_id" not in contributor:
            raise CollaborationAdmissionError("required contributor has unsupported or missing fields")
        ref = ContributorRef(
            player_id=_id(contributor["player_id"], "required contributor player_id"),
            pc_id=None
            if contributor.get("pc_id") is None
            else _id(contributor["pc_id"], "required contributor pc_id"),
        )
        if (ref.player_id, ref.pc_id) in seen:
            raise CollaborationAdmissionError("required contributors must be unique")
        seen.add((ref.player_id, ref.pc_id))
        refs.append(ref)
    return tuple(refs)


def _parse_basis_refs(value: object) -> tuple[NativeBasisRef, ...]:
    refs: list[NativeBasisRef] = []
    seen: set[tuple[str, str]] = set()
    for raw in _sequence(value, "native basis refs"):
        basis = _mapping(raw, "native basis ref")
        if set(basis) - {"family", "id", "revision"} or not {"family", "id"}.issubset(basis):
            raise CollaborationAdmissionError("native basis ref has unsupported or missing fields")
        ref = NativeBasisRef(
            family=_nonempty(basis["family"], "native basis family"),
            record_id=_id(basis["id"], "native basis id"),
            revision=None if basis.get("revision") is None else _nonempty(basis["revision"], "native basis revision"),
        )
        if (ref.family, ref.record_id) in seen:
            raise CollaborationAdmissionError("native basis refs must be unique")
        seen.add((ref.family, ref.record_id))
        refs.append(ref)
    if not refs:
        raise CollaborationAdmissionError("positive dependency requires an explicit native basis")
    return tuple(refs)


def _validate_dependency_basis_shape(
    dependency: DependencyClass,
    dependency_scope: Mapping[str, object],
    basis_refs: tuple[NativeBasisRef, ...],
) -> None:
    rule = _DEPENDENCY_BASIS_RULES[dependency]
    if len(basis_refs) != 1:
        raise CollaborationAdmissionError("dependency requires exactly one native basis owner")
    basis = basis_refs[0]
    if basis.revision is None:
        raise CollaborationAdmissionError("native basis revision is required for currentness")
    if basis.family in _ORDERED_OWNER_FAMILIES:
        return
    if basis.family != rule.family:
        raise CollaborationAdmissionError(
            f"native basis family is not admitted for dependency class {dependency.value}"
        )
    if dependency_scope.get(rule.scope_key) != basis.record_id:
        raise CollaborationAdmissionError(
            f"native basis id must match dependency scope {rule.scope_key}"
        )


def _validate_dependency_basis_owner(
    dependency: DependencyClass,
    dependency_scope: Mapping[str, object],
    basis: NativeBasisRef,
    owner: Mapping[str, object],
) -> None:
    rule = _DEPENDENCY_BASIS_RULES[dependency]
    if basis.revision is None or owner.get("revision") != basis.revision:
        raise CollaborationAdmissionError("native basis revision is stale")
    if basis.family in _ORDERED_OWNER_FAMILIES:
        return
    if basis.family != rule.family or dependency_scope.get(rule.scope_key) != basis.record_id:
        raise CollaborationAdmissionError("native basis owner is irrelevant to the dependency class")
    if not isinstance(owner.get("state"), Mapping):
        raise CollaborationAdmissionError("native basis owner state is incomplete")


def _validate_clause_semantics(
    clause: Mapping[str, object],
) -> tuple[str | None, Mapping[str, object], DependencyClass | None, str | None, Mapping[str, object], tuple[ContributorRef, ...], tuple[NativeBasisRef, ...]]:
    semantic_class = clause.get("collaboration_semantic_class")
    if semantic_class is not None and semantic_class not in _SEMANTIC_CLASSES:
        raise CollaborationAdmissionError("intent clause semantic class is not registered")
    normalized = _mapping(clause.get("normalized_semantics", {}), "normalized semantics")
    raw_dependency = clause.get("dependency_kind")
    dependency: DependencyClass | None
    if raw_dependency is None:
        dependency = None
    elif raw_dependency not in _DEPENDENCY_CLASSES:
        raise CollaborationAdmissionError("intent clause dependency class is not registered")
    else:
        dependency = DependencyClass(raw_dependency)
    purpose = clause.get("purpose")
    if purpose is not None:
        purpose = _nonempty(purpose, "intent clause purpose")
    scope = _mapping(clause.get("dependency_scope", {}), "dependency scope")
    raw_contributors = clause.get("required_contributors")
    raw_basis = clause.get("native_basis_refs")
    if dependency is None:
        if raw_contributors is not None or raw_basis is not None or purpose is not None or scope:
            raise CollaborationAdmissionError("dependency fields require a registered dependency class")
        return semantic_class, normalized, None, None, scope, (), ()
    if semantic_class is None:
        raise CollaborationAdmissionError("dependency class requires an accepted semantic class")
    if purpose is None or not scope:
        raise CollaborationAdmissionError("positive dependency requires bounded purpose and scope")
    contributors = _parse_contributors(raw_contributors)
    if not contributors:
        raise CollaborationAdmissionError("positive dependency requires required contributors")
    basis_refs = _parse_basis_refs(raw_basis)
    if semantic_class == "ACTIONABLE_INTENT" and clause.get("execution_state") != "intent.pending":
        raise CollaborationAdmissionError("collaboration-held actionable intent must remain pending")
    if clause.get("command_id") is not None:
        raise CollaborationAdmissionError("collaboration-held intent cannot already have a command")
    _validate_dependency_basis_shape(dependency, scope, basis_refs)
    return semantic_class, normalized, dependency, purpose, scope, contributors, basis_refs


def _load_current_player(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    principal: object,
    player_route: object,
    expected_player_id: str,
) -> PlayerRecord:
    def load_exact(candidate_id: str) -> Mapping[str, object] | PlayerRecord | None:
        payload = _read_native(repository, pinned, "world.player", candidate_id)
        return payload

    try:
        resolution = resolve_player(
            principal,
            player_route,
            load_exact,
            campaign_id=pinned.campaign_id,
        )
    except (AccessControlContractError, CollaborationAdmissionError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError("current principal-to-PLAYER resolution failed") from exc
    if resolution.status != "AUTHORIZED_PLAYER" or resolution.player is None:
        raise CollaborationAdmissionError("current principal does not own an active PLAYER")
    if resolution.player.player_id != expected_player_id:
        raise CollaborationAdmissionError("interaction PLAYER differs from current principal PLAYER")
    return resolution.player


def _validate_required_player(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    ref: ContributorRef,
) -> None:
    try:
        player = PlayerRecord.from_mapping(_read_native(repository, pinned, "world.player", ref.player_id))
    except (AccessControlContractError, CollaborationAdmissionError, TypeError, ValueError) as exc:
        raise CollaborationAdmissionError("required contributor PLAYER is not current") from exc
    if player.status != "active":
        raise CollaborationAdmissionError("required contributor PLAYER is not active")
    if ref.pc_id is not None and ref.pc_id not in player.controlled_pc_ids:
        raise CollaborationAdmissionError("required contributor PC is not currently controlled")


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _is_positive_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _is_nonnegative_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_unique_identifier_array(value: object, *, minimum: int = 0) -> bool:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return False
    values = tuple(value)
    if len(values) < minimum or not all(_id_is_valid(item) for item in values):
        return False
    return len(values) == len(set(values))


def _is_unique_string_array(value: object, *, minimum: int = 0) -> bool:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return False
    values = tuple(value)
    if len(values) < minimum or not all(_is_nonempty_string(item) for item in values):
        return False
    return len(values) == len(set(values))


def _id_is_valid(value: object) -> bool:
    return isinstance(value, str) and _ID_PATTERN.fullmatch(value) is not None


def _is_scalar(value: object) -> bool:
    return isinstance(value, (str, int, float, bool)) and not (
        isinstance(value, float) and not math.isfinite(value)
    )


def _validate_policy_basis_refs(value: object) -> bool:
    pattern = r"^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$"
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return False
    values = tuple(value)
    if not all(isinstance(item, str) and re.fullmatch(pattern, item) is not None for item in values):
        return False
    return len(values) == len(set(values))


def _validate_adjudicated_binding(value: object) -> bool:
    if _is_scalar(value):
        return True
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return bool(value) and all(_is_scalar(item) for item in value)
    if not isinstance(value, Mapping):
        return False
    required = {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }
    allowed = required | {"candidate_set_fingerprint"}
    if set(value) - allowed or not required.issubset(value):
        return False
    return (
        value.get("source_class") == "INVOCATION_ADJUDICATED"
        and _is_scalar(value.get("value"))
        and _is_nonempty_string(value.get("provenance_ref"))
        and _is_nonempty_string(value.get("eligibility_basis_fingerprint"))
        and _is_nonempty_string(value.get("rules_context_fingerprint"))
        and _validate_policy_basis_refs(value.get("policy_basis_refs"))
        and (
            "candidate_set_fingerprint" not in value
            or _is_nonempty_string(value["candidate_set_fingerprint"])
        )
    )


def _validate_invocation_fact(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    required = {
        "fact_id",
        "value",
        "provenance_class",
        "provenance_ref",
        "consumer_id",
        "binding_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }
    if set(value) != required:
        return False
    return (
        _id_is_valid(value.get("fact_id"))
        and type(value.get("value")) is bool
        and value.get("provenance_class") == "INVOCATION_ADJUDICATED"
        and _is_nonempty_string(value.get("provenance_ref"))
        and _id_is_valid(value.get("consumer_id"))
        and isinstance(value.get("binding_fingerprint"), str)
        and re.fullmatch(r"[a-f0-9]{64}", value["binding_fingerprint"]) is not None
        and isinstance(value.get("rules_context_fingerprint"), str)
        and re.fullmatch(r"[a-f0-9]{64}", value["rules_context_fingerprint"]) is not None
        and _validate_policy_basis_refs(value.get("policy_basis_refs"))
    )


def _validate_roll_result(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    required = {"roll_id", "request_id", "expression", "raw_values", "source_kind", "provenance_ref"}
    if set(value) != required:
        return False
    raw_values = value.get("raw_values")
    return (
        _id_is_valid(value.get("roll_id"))
        and _id_is_valid(value.get("request_id"))
        and _is_nonempty_string(value.get("expression"))
        and isinstance(raw_values, Sequence)
        and not isinstance(raw_values, (str, bytes))
        and bool(raw_values)
        and all(_is_nonnegative_integer(item) or (isinstance(item, int) and item < 0) for item in raw_values)
        and value.get("source_kind") in {"rng.system", "rng.player", "rng.external"}
        and _is_nonempty_string(value.get("provenance_ref"))
    )


def _validate_spent_resources(value: object, *, minimum: int) -> bool:
    if not isinstance(value, Mapping) or len(value) < minimum:
        return False
    for participant_id, resources in value.items():
        if not _is_nonempty_string(participant_id) or not isinstance(resources, Mapping):
            return False
        for resource_id, spent_state in resources.items():
            if not _is_nonempty_string(resource_id) or not isinstance(spent_state, Mapping):
                return False
            if set(spent_state) != {"spent"} or not _is_nonnegative_integer(spent_state.get("spent")):
                return False
    return True


def _validate_budget_resources(value: object) -> bool:
    if not isinstance(value, Mapping) or not value:
        return False
    required = {"resource.action_budget", "resource.movement_budget"}
    for participant_id, resources in value.items():
        if not _is_nonempty_string(participant_id) or not isinstance(resources, Mapping):
            return False
        if set(resources) != required:
            return False
        for budget in resources.values():
            if not isinstance(budget, Mapping) or set(budget) != {"capacity", "spent"}:
                return False
            if not all(_is_nonnegative_integer(budget.get(key)) for key in ("capacity", "spent")):
                return False
    return True


def _validate_procedure_state(value: object) -> tuple[bool, bool]:
    if not isinstance(value, Mapping):
        return False, False
    procedure_kind = value.get("procedure_kind")
    if procedure_kind == "procedure.combat_minimal":
        allowed = {
            "schema_version",
            "procedure_kind",
            "lifecycle",
            "lifecycle_state",
            "participant_ids",
            "initiative_order",
            "round_number",
            "round_advance_pending",
            "active_turn_index",
            "participant_resources",
            "world_context_id",
        }
        required = allowed - {"world_context_id"}
        if set(value) - allowed or not required.issubset(value):
            return False, False
        lifecycle = value.get("lifecycle")
        lifecycle_state = value.get("lifecycle_state")
        if value.get("schema_version") != 2 or lifecycle not in {"ACTIVE", "TERMINAL"}:
            return False, False
        if lifecycle_state not in {"between_turns", "turn_active", "terminated"}:
            return False, False
        if lifecycle == "TERMINAL" and lifecycle_state != "terminated":
            return False, False
        if lifecycle == "ACTIVE" and lifecycle_state == "terminated":
            return False, False
        if not _is_unique_string_array(value.get("participant_ids"), minimum=1):
            return False, False
        if not _is_unique_string_array(value.get("initiative_order"), minimum=1):
            return False, False
        if not _is_positive_integer(value.get("round_number")):
            return False, False
        if type(value.get("round_advance_pending")) is not bool:
            return False, False
        active_turn_index = value.get("active_turn_index")
        if (
            not _is_nonnegative_integer(active_turn_index)
            or active_turn_index >= len(value["initiative_order"])
        ):
            return False, False
        if not _validate_budget_resources(value.get("participant_resources")):
            return False, False
        if "world_context_id" in value and not _is_nonempty_string(value["world_context_id"]):
            return False, False
        return True, lifecycle == "ACTIVE"

    allowed = {"schema_version", "lifecycle", "participant_resources", "world_context_id", "details"}
    required = {"schema_version", "lifecycle", "participant_resources"}
    if set(value) - allowed or not required.issubset(value):
        return False, False
    if value.get("schema_version") != 2 or value.get("lifecycle") not in {"ACTIVE", "TERMINAL"}:
        return False, False
    if not _validate_spent_resources(value.get("participant_resources"), minimum=0):
        return False, False
    if "world_context_id" in value and not _is_nonempty_string(value["world_context_id"]):
        return False, False
    if "details" in value and not isinstance(value["details"], Mapping):
        return False, False
    return True, False


def _validate_pending_response(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    kind = value.get("kind")
    if kind == "choice":
        required = {
            "kind",
            "offer_id",
            "parent_resolution_id",
            "continuation_generation",
            "responder_id",
            "option_ids",
        }
        if set(value) != required:
            return False
        return (
            _is_nonempty_string(value.get("offer_id"))
            and _is_nonempty_string(value.get("parent_resolution_id"))
            and _is_positive_integer(value.get("continuation_generation"))
            and _is_nonempty_string(value.get("responder_id"))
            and _is_unique_string_array(value.get("option_ids"), minimum=1)
        )
    if kind == "reaction":
        required = {
            "kind",
            "offer_id",
            "parent_resolution_id",
            "continuation_generation",
            "responder_id",
            "candidate_activity_ids",
        }
        if set(value) != required:
            return False
        return (
            _is_nonempty_string(value.get("offer_id"))
            and _is_nonempty_string(value.get("parent_resolution_id"))
            and _is_positive_integer(value.get("continuation_generation"))
            and _is_nonempty_string(value.get("responder_id"))
            and _is_unique_string_array(value.get("candidate_activity_ids"), minimum=1)
        )
    return False


def _validate_continuation_record(owner: Mapping[str, object]) -> tuple[bool, bool]:
    required = {
        "generation",
        "root_command_id",
        "resolution_id",
        "activity_id",
        "actor_id",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
        "execution_cursor",
        "safe_recompute_phase",
        "invocation_facts",
        "fixed_rng_results",
        "prior_step_exports",
        "committed_segment_refs",
        "dependency_frontier_refs",
        "expected_child_resolution_ids",
        "future_rng_frontier",
    }
    optional = {
        "source_id",
        "target_ids",
        "parameter_bindings",
        "procedure_id",
        "pending_response",
        "unconsumed_advancement",
        "details",
    }
    envelope = {"kind", "id", "revision", "campaign_id"}
    if set(owner) - required - optional - envelope or not required.issubset(owner):
        return False, False
    if owner.get("kind") != "runtime.continuation" or not _id_is_valid(owner.get("id")):
        return False, False
    if not _is_nonempty_string(owner.get("revision")):
        return False, False
    if "campaign_id" in owner and not _is_nonempty_string(owner["campaign_id"]):
        return False, False
    if not _is_positive_integer(owner.get("generation")):
        return False, False
    if not all(_is_nonempty_string(owner.get(key)) for key in ("root_command_id", "resolution_id")):
        return False, False
    if not all(_id_is_valid(owner.get(key)) for key in ("activity_id", "actor_id")):
        return False, False
    if owner.get("ruleset_set_digest_generation") != 1:
        return False, False
    ruleset_sha = owner.get("ruleset_set_sha256")
    if not isinstance(ruleset_sha, str) or re.fullmatch(r"[a-f0-9]{64}", ruleset_sha) is None:
        return False, False
    if owner.get("catalog_context_fingerprint_generation") != 1:
        return False, False
    if not all(
        _is_nonempty_string(owner.get(key))
        for key in ("catalog_context_fingerprint", "execution_cursor", "safe_recompute_phase", "future_rng_frontier")
    ):
        return False, False
    invocation_facts = owner.get("invocation_facts")
    fixed_rng_results = owner.get("fixed_rng_results")
    if not isinstance(invocation_facts, list) or not all(_validate_invocation_fact(item) for item in invocation_facts):
        return False, False
    if not isinstance(fixed_rng_results, list) or not all(_validate_roll_result(item) for item in fixed_rng_results):
        return False, False
    if not isinstance(owner.get("prior_step_exports"), Mapping):
        return False, False
    if not all(_is_scalar(value) for value in owner["prior_step_exports"].values()):
        return False, False
    if not all(_is_unique_string_array(owner.get(key)) for key in ("committed_segment_refs", "dependency_frontier_refs", "expected_child_resolution_ids")):
        return False, False
    if "source_id" in owner and not _id_is_valid(owner["source_id"]):
        return False, False
    if "target_ids" in owner and not _is_unique_identifier_array(owner["target_ids"]):
        return False, False
    if "parameter_bindings" in owner:
        parameter_bindings = owner["parameter_bindings"]
        if not isinstance(parameter_bindings, Mapping):
            return False, False
        if not all(
            _id_is_valid(key) and _validate_adjudicated_binding(value)
            for key, value in parameter_bindings.items()
        ):
            return False, False
    if "procedure_id" in owner and not _is_nonempty_string(owner["procedure_id"]):
        return False, False
    if "details" in owner and not isinstance(owner["details"], Mapping):
        return False, False
    has_pending_response = "pending_response" in owner
    if has_pending_response and not _validate_pending_response(owner["pending_response"]):
        return False, False
    has_unconsumed_advancement = "unconsumed_advancement" in owner
    if has_unconsumed_advancement:
        advancement = owner["unconsumed_advancement"]
        if not isinstance(advancement, Mapping) or set(advancement) != {"amount", "unit_id", "context_id"}:
            return False, False
        if not _is_positive_integer(advancement.get("amount")):
            return False, False
        if advancement.get("unit_id") not in {"unit.second", "unit.minute", "unit.hour", "unit.day"}:
            return False, False
        if not _is_nonempty_string(advancement.get("context_id")):
            return False, False
    return True, has_pending_response or has_unconsumed_advancement


def _ordered_owner(refs: Sequence[NativeBasisRef], owners: Sequence[Mapping[str, object]]) -> str | None:
    for ref, owner in zip(refs, owners):
        if ref.family == "runtime.procedure":
            valid, ordered = _validate_procedure_state(owner.get("state"))
        elif ref.family == "runtime.continuation":
            valid, ordered = _validate_continuation_record(owner)
        else:
            continue
        if not valid:
            raise CollaborationAdmissionError("nominated native ordered owner is rejected by its owner schema")
        if ordered:
            return ref.family
        raise CollaborationAdmissionError("nominated native ordered owner has no active ordering evidence")
    return None


def classify_coordination_dependency(
    repository: RepositoryPort,
    campaign_id: str,
    interaction_id: str,
    clause_id: str,
    *,
    principal: object,
    player_route: object,
) -> CoordinationAdmission:
    """Derive one finite collaboration admission from exact native owners.

    The caller supplies only the authenticated principal and the bounded W03
    route companion.  Family, dependency class, required contributors and
    currentness are read from/revalidated against native owner records.
    """

    _id(interaction_id, "interaction_id")
    _id(clause_id, "clause_id")
    pinned = _pin_campaign(repository, campaign_id)
    interaction = _load_interaction(repository, pinned, interaction_id)
    intent_plan_id = _id(interaction["intent_plan_id"], "interaction intent_plan_id")
    plan = _load_intent_plan(repository, pinned, intent_plan_id, interaction_id)
    clause = _load_clause(plan, clause_id)
    (
        semantic_class,
        normalized,
        dependency,
        purpose,
        scope,
        required,
        basis_refs,
    ) = _validate_clause_semantics(clause)
    current_player = _load_current_player(
        repository,
        pinned,
        principal,
        player_route,
        _id(interaction["player_id"], "interaction player_id"),
    )
    del current_player

    basis_owners = tuple(_read_native(repository, pinned, ref.family, ref.record_id) for ref in basis_refs)
    if dependency is not None:
        for ref, owner in zip(basis_refs, basis_owners):
            _validate_dependency_basis_owner(dependency, scope, ref, owner)
        for ref in required:
            _validate_required_player(repository, pinned, ref)
    ordered_owner = _ordered_owner(basis_refs, basis_owners)
    if ordered_owner is not None:
        family = CoordinationFamily.RULE_OWNED_ORDERED
    elif dependency is None:
        family = CoordinationFamily.INDEPENDENT_IMMEDIATE
    else:
        family = CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE
    return CoordinationAdmission(
        campaign_id=pinned.campaign_id,
        campaign_revision=pinned.revision,
        interaction_id=interaction_id,
        intent_plan_id=intent_plan_id,
        clause_id=clause_id,
        semantic_class=semantic_class,
        normalized_semantics=normalized,
        dependency_class=dependency,
        purpose=purpose,
        dependency_scope=scope,
        required_contributors=required,
        native_basis_refs=basis_refs,
        family=family,
        ordered_owner_family=ordered_owner,
    )


def open_or_successor_obligation(
    admission: CoordinationAdmission,
    *,
    obligation_id: str | None = None,
    generation: int = 1,
) -> CollaborationObligation | None:
    """Create the durable collaboration owner only for a derived collective result."""

    if not isinstance(admission, CoordinationAdmission):
        raise CollaborationAdmissionError("owner-derived coordination admission is required")
    if admission.family is not CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE:
        return None
    if admission.dependency_class is None or admission.purpose is None:
        raise CollaborationAdmissionError("collective admission is incomplete")
    if obligation_id is None:
        # The durable owner identity is deterministic lineage metadata derived
        # from the accepted opportunity; it is not a caller-issued token.
        obligation_id = f"collaboration:{admission.interaction_id}:{admission.clause_id}"
    return CollaborationObligation(
        obligation_id=obligation_id,
        generation=generation,
        campaign_id=admission.campaign_id,
        interaction_id=admission.interaction_id,
        intent_plan_id=admission.intent_plan_id,
        clause_id=admission.clause_id,
        dependency_class=admission.dependency_class,
        purpose=admission.purpose,
        dependency_scope=admission.dependency_scope,
        native_basis_refs=admission.native_basis_refs,
        required_contributors=admission.required_contributors,
    )
