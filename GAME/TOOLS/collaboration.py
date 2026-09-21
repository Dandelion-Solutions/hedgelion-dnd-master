"""Owner-local collaboration admission over exact native records.

The collaboration owner derives a bounded family from accepted
``Interaction``/``IntentPlan``/``IntentClause`` data and fresh native
revalidation.  It never accepts a caller-selected family, currentness flag,
participant authority, Procedure body or Continuation body.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final

from .access_control import AccessControlContractError, PlayerRecord, resolve_player
from .native_storage import (
    FAMILY_ROOTS,
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .runtime_execution import (
    NativeOrderingError,
    resolve_native_ordering_evidence,
)

if TYPE_CHECKING:
    from .runtime_host import RuntimeHost, _OperationBasis


# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.2"
COLLABORATION_SCHEMA_VERSION: Final[int] = 1

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


@dataclass(frozen=True, slots=True)
class CoordinationAdmission:
    """Ephemeral family evidence derived after complete revalidation."""

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
    ordered_evidence: object | None = None

    def __post_init__(self) -> None:
        _id(self.campaign_id, "admission campaign_id")
        _text(self.campaign_revision, "admission campaign revision")
        _id(self.interaction_id, "admission interaction_id")
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
        return semantic_class, normalized, None, None, scope, (), (), ordering_ref
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
        ordered_evidence=ordered_evidence,
    )


def open_or_successor_obligation(
    admission: CoordinationAdmission,
    *,
    obligation_id: str | None = None,
    generation: int = 1,
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
        accepted_input_uses=(admission.opportunity_identity,),
    )
