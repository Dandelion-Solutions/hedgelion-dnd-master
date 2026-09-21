"""Owner-local admission for bounded human collaboration.

The module consumes accepted Interaction/IntentPlan nominations and reloads
their native sources before choosing a coordination family.  The exact-load
boundary supplies records only; all identity, linkage, currentness and
participant checks remain here or with the existing access-control owner.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
import json
import re
from typing import Final, TypeAlias

from .access_control import (
    AccessControlContractError,
    PlayerLoader,
    PlayerRecord,
    PlayerResolution,
    PrincipalPlayerRoute,
    VerifiedPrincipal,
    authorize_operation,
    resolve_player,
    resolve_principal,
)
from .native_storage import FAMILY_ROOTS, NativeStorageError, validate_loaded_identity


# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"
COLLABORATION_SCHEMA_VERSION: Final[int] = 1
COLLABORATION_KIND: Final[str] = "runtime.collaboration_obligation"

_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_REVISION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$"
)
_SEMANTIC_CLASSES: Final[frozenset[str]] = frozenset(
    {"OOC_COORDINATION", "DIEGETIC_COMMUNICATION", "ACTIONABLE_INTENT", "CONTROL_SIGNAL"}
)
_ORDERED_OWNER_NAMES: Final[frozenset[str]] = frozenset(
    {
        "Procedure",
        "Continuation",
        "Choice",
        "Reaction",
        "runtime.procedure",
        "runtime.continuation",
    }
)
_REQUEST_FIELDS: Final[frozenset[str]] = frozenset(
    {"interaction_id", "intent_plan_id", "clause_id", "obligation_id", "generation"}
)


class CollaborationContractError(ValueError):
    """Raised when collaboration admission evidence is malformed or stale."""

    failure_code: str

    def __init__(self, message: str, *, failure_code: str = "collaboration.contract_invalid") -> None:
        super().__init__(message)
        self.failure_code = failure_code


class CoordinationFamily(StrEnum):
    """The closed coordination-family vocabulary."""

    INDEPENDENT_IMMEDIATE = "INDEPENDENT_IMMEDIATE"
    AGENCY_DEPENDENT_COLLECTIVE = "AGENCY_DEPENDENT_COLLECTIVE"
    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"


class CollaborationLifecycle(StrEnum):
    """Base obligation lifecycle; later W04 rows own its transitions."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RESOLVED = "RESOLVED"
    OBSOLETE = "OBSOLETE"


ExactLoadResult: TypeAlias = Mapping[str, object] | bytes | bytearray | None
ExactLoadTransport: TypeAlias = Callable[[str, tuple[str, ...]], ExactLoadResult]


def _string(value: object, label: str, *, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value:
        raise CollaborationContractError(f"{label} must be a nonempty string")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise CollaborationContractError(f"{label} is not a native identifier")
    return value


def _boolean(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise CollaborationContractError(f"{label} must be boolean")
    return value


def _sequence(value: object, label: str) -> tuple[object, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise CollaborationContractError(f"{label} must be an array")
    return tuple(value)


def _revision(value: object, label: str) -> str:
    return _string(value, label, pattern=_REVISION_PATTERN)


@dataclass(frozen=True, slots=True)
class CollaborationAdmissionRequest:
    """Known IDs nominated by one accepted Interaction/IntentPlan.

    The request deliberately contains no family, contributor, currentness or
    eligibility field.  Those values are discovered from the reloaded native
    records below.
    """

    interaction_id: str
    intent_plan_id: str
    clause_id: str
    obligation_id: str
    generation: int = 1

    def __post_init__(self) -> None:
        for field_name in ("interaction_id", "intent_plan_id", "clause_id", "obligation_id"):
            object.__setattr__(
                self,
                field_name,
                _string(getattr(self, field_name), field_name, pattern=_ID_PATTERN),
            )
        if isinstance(self.generation, bool) or not isinstance(self.generation, int) or self.generation < 1:
            raise CollaborationContractError("generation must be a positive integer")

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> CollaborationAdmissionRequest:
        if not isinstance(value, Mapping):
            raise CollaborationContractError("collaboration admission request must be an object")
        if set(value) - _REQUEST_FIELDS:
            raise CollaborationContractError(
                "caller cannot select family, contributors, currentness or eligibility",
                failure_code="collaboration.caller_authority_fields",
            )
        missing = _REQUEST_FIELDS - {"generation"} - set(value)
        if missing:
            raise CollaborationContractError("collaboration admission request is incomplete")
        return cls(
            interaction_id=value["interaction_id"],  # type: ignore[arg-type]
            intent_plan_id=value["intent_plan_id"],  # type: ignore[arg-type]
            clause_id=value["clause_id"],  # type: ignore[arg-type]
            obligation_id=value["obligation_id"],  # type: ignore[arg-type]
            generation=value.get("generation", 1),  # type: ignore[arg-type]
        )


@dataclass(frozen=True, slots=True)
class ParticipantRef:
    """Exact PLAYER/controlled-PC reference copied from a native owner."""

    player_id: str
    pc_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "player_id",
            _string(self.player_id, "participant player_id", pattern=_ID_PATTERN),
        )
        if self.pc_id is not None:
            object.__setattr__(self, "pc_id", _string(self.pc_id, "participant pc_id", pattern=_ID_PATTERN))

    @property
    def identity(self) -> tuple[str, str]:
        return self.player_id, self.pc_id or ""

    def as_mapping(self) -> dict[str, str]:
        value = {"player_id": self.player_id}
        if self.pc_id is not None:
            value["pc_id"] = self.pc_id
        return value


@dataclass(frozen=True, slots=True)
class CollaborationObligation:
    """The bounded collection owner created after native admission."""

    obligation_id: str
    generation: int
    lifecycle: CollaborationLifecycle
    purpose: str
    dependency_scope: str
    decision_opportunity_ref: str
    campaign_id: str
    source_ref: str
    source_revision: str
    required_contributors: tuple[ParticipantRef, ...]
    optional_contributors: tuple[ParticipantRef, ...] = ()
    accepted_input_uses: tuple[tuple[str, str], ...] = ()
    safe_frontier_refs: tuple[str, ...] = ()

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": COLLABORATION_SCHEMA_VERSION,
            "kind": COLLABORATION_KIND,
            "obligation_id": self.obligation_id,
            "generation": self.generation,
            "lifecycle": self.lifecycle.value,
            "coordination_family": CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE.value,
            "campaign_id": self.campaign_id,
            "purpose": self.purpose,
            "dependency_scope": self.dependency_scope,
            "decision_opportunity_ref": self.decision_opportunity_ref,
            "currentness_basis": {
                "source_ref": self.source_ref,
                "source_revision": self.source_revision,
                "opportunity_ref": self.decision_opportunity_ref,
            },
            "required_contributors": [item.as_mapping() for item in self.required_contributors],
            "optional_contributors": [item.as_mapping() for item in self.optional_contributors],
            "accepted_input_uses": [
                {"interaction_id": interaction_id, "clause_id": clause_id}
                for interaction_id, clause_id in self.accepted_input_uses
            ],
            "safe_frontier_refs": list(self.safe_frontier_refs),
        }


@dataclass(frozen=True, slots=True)
class CollaborationMutation:
    """Admission result; non-collective families contain no obligation."""

    family: CoordinationFamily
    disposition: str
    obligation: CollaborationObligation | None = None
    native_order_owner: str | None = None


@dataclass(frozen=True, slots=True)
class _NativeAdmissionEvidence:
    campaign_id: str
    source_ref: str
    source_revision: str
    opportunity_ref: str
    purpose: str
    dependency_scope: str
    positive_material_dependency: bool
    input_can_change_result: bool
    independently_durable: bool
    required_contributors: tuple[ParticipantRef, ...]
    optional_contributors: tuple[ParticipantRef, ...]
    native_order_owner: str | None


def resolve_participant_authority(
    principal: VerifiedPrincipal | Mapping[str, object],
    route: PrincipalPlayerRoute | Mapping[str, object] | None,
    load_exact_player: PlayerLoader,
    *,
    campaign_id: str,
    controlled_pc_id: str | None = None,
) -> PlayerResolution:
    """Consume W03's owner-issued PLAYER resolution without minting a bridge."""

    try:
        resolved_principal = resolve_principal(principal)
        resolution = resolve_player(
            resolved_principal,
            route,
            load_exact_player,
            campaign_id=campaign_id,
        )
        decision = authorize_operation(
            resolved_principal,
            resolution,
            operation="gameplay",
            campaign_id=campaign_id,
        )
    except (AccessControlContractError, TypeError, ValueError) as error:
        raise CollaborationContractError(
            "trusted current participant authority is required",
            failure_code="collaboration.participant_authority_required",
        ) from error
    if not decision.authorized or resolution.player is None:
        raise CollaborationContractError(
            "participant is not currently authorized for gameplay",
            failure_code="collaboration.participant_not_authorized",
        )
    if controlled_pc_id is not None:
        pc_id = _string(controlled_pc_id, "controlled_pc_id", pattern=_ID_PATTERN)
        if pc_id not in resolution.player.controlled_pc_ids:
            raise CollaborationContractError(
                "participant does not currently control the requested PC",
                failure_code="collaboration.controlled_pc_not_authorized",
            )
    return resolution


def _call_exact_load(
    exact_load: ExactLoadTransport | object,
    family_key: str,
    identity: tuple[str, ...],
) -> Mapping[str, object]:
    loader = getattr(exact_load, "load_exact", None)
    if loader is None:
        loader = exact_load
    if not callable(loader):
        raise CollaborationContractError("exact native-record transport is required")
    try:
        raw = loader(family_key, identity)
    except (KeyError, OSError, TypeError, ValueError) as error:
        raise CollaborationContractError(
            f"exact native load failed for {family_key}",
            failure_code="collaboration.native_load_failed",
        ) from error
    if raw is None:
        raise CollaborationContractError(
            f"exact native record is missing for {family_key}:{identity[0]}",
            failure_code="collaboration.native_record_missing",
        )
    if isinstance(raw, (bytes, bytearray)):
        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CollaborationContractError(
                "exact native bytes are not a supported JSON record",
                failure_code="collaboration.native_record_invalid",
            ) from error
        raw = decoded
    if not isinstance(raw, Mapping):
        raise CollaborationContractError(
            "exact native transport returned a non-record value",
            failure_code="collaboration.native_record_invalid",
        )
    return raw


def _validate_identity(family_key: str, identity: tuple[str, ...], record: Mapping[str, object]) -> None:
    if family_key not in FAMILY_ROOTS:
        raise CollaborationContractError(
            f"native family has no admitted exact route: {family_key}",
            failure_code="collaboration.native_route_missing",
        )
    try:
        validate_loaded_identity(family_key, identity, record)
    except NativeStorageError as error:
        raise CollaborationContractError(
            f"native record identity is not current for {family_key}:{identity[0]}",
            failure_code="collaboration.native_identity_invalid",
        ) from error


def _record_kind(record: Mapping[str, object], family_key: str) -> None:
    kind = record.get("kind")
    if kind is not None and kind != family_key:
        raise CollaborationContractError("native record kind does not match its route")


def _record_revision(record: Mapping[str, object], label: str) -> str:
    for field_name in ("state_revision", "source_revision", "revision"):
        if field_name in record:
            return _revision(record[field_name], f"{label} {field_name}")
    raise CollaborationContractError(
        f"{label} has no owner revision",
        failure_code="collaboration.currentness_required",
    )


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CollaborationContractError(f"{label} must be an object")
    return value


def _participant_ref(value: object, label: str) -> ParticipantRef:
    raw = _mapping(value, label)
    allowed = {"player_id", "pc_id"}
    if set(raw) - allowed or "player_id" not in raw:
        raise CollaborationContractError(f"{label} has unexpected or missing fields")
    pc_id = raw.get("pc_id")
    if pc_id is not None and not isinstance(pc_id, str):
        raise CollaborationContractError(f"{label} pc_id must be a string or null")
    return ParticipantRef(
        player_id=_string(raw["player_id"], f"{label} player_id", pattern=_ID_PATTERN),
        pc_id=pc_id,
    )


def _participant_refs(value: object, label: str) -> tuple[ParticipantRef, ...]:
    result = tuple(_participant_ref(item, f"{label} item") for item in _sequence(value, label))
    identities = tuple(item.identity for item in result)
    if len(identities) != len(set(identities)):
        raise CollaborationContractError(f"{label} must contain unique participant references")
    return tuple(sorted(result, key=lambda item: item.identity))


def _load_player(
    exact_load: ExactLoadTransport | object,
    participant: ParticipantRef,
) -> PlayerRecord:
    record = _call_exact_load(exact_load, "world.player", (participant.player_id,))
    _record_kind(record, "world.player")
    if record.get("id", record.get("player_id")) != participant.player_id:
        raise CollaborationContractError(
            "exact PLAYER identity does not match the requested participant",
            failure_code="collaboration.native_identity_invalid",
        )
    try:
        player = PlayerRecord.from_mapping(record)
    except (AccessControlContractError, TypeError, ValueError) as error:
        raise CollaborationContractError(
            "exact PLAYER record is invalid",
            failure_code="collaboration.participant_authority_required",
        ) from error
    if player.status != "active":
        raise CollaborationContractError(
            "required participant PLAYER is not active",
            failure_code="collaboration.participant_not_authorized",
        )
    if participant.pc_id is not None and participant.pc_id not in player.controlled_pc_ids:
        raise CollaborationContractError(
            "required participant does not control the native PC",
            failure_code="collaboration.controlled_pc_not_authorized",
        )
    return player


def _candidate_from_clause(clause: Mapping[str, object]) -> Mapping[str, object]:
    semantic_class = clause.get("collaboration_semantic_class")
    if semantic_class not in _SEMANTIC_CLASSES:
        raise CollaborationContractError(
            "collaboration clause has no admitted semantic class",
            failure_code="collaboration.intent_clause_invalid",
        )
    normalized = clause.get("normalized_semantics")
    if not isinstance(normalized, Mapping) or not normalized:
        raise CollaborationContractError(
            "collaboration clause has no normalized semantics",
            failure_code="collaboration.intent_clause_invalid",
        )
    if normalized.get("value_kind") == "value.contribution":
        raise CollaborationContractError(
            "mechanical value.contribution is not human collaboration input",
            failure_code="collaboration.mechanical_contribution_rejected",
        )
    candidate = _mapping(clause.get("coordination_candidate"), "coordination candidate")
    required = {
        "native_owner_kind",
        "native_owner_id",
        "opportunity_id",
        "purpose",
        "dependency_scope",
        "participant_player_ids",
    }
    if set(candidate) - required or required - set(candidate):
        raise CollaborationContractError("coordination candidate has unexpected or missing fields")
    return candidate


def _prepare_admission(
    request: CollaborationAdmissionRequest | Mapping[str, object],
    *,
    principal: VerifiedPrincipal | Mapping[str, object],
    player_route: PrincipalPlayerRoute | Mapping[str, object] | None,
    load_exact_player: PlayerLoader,
    exact_load: ExactLoadTransport | object,
    campaign_id: str,
) -> _NativeAdmissionEvidence:
    admission_request = (
        request
        if isinstance(request, CollaborationAdmissionRequest)
        else CollaborationAdmissionRequest.from_mapping(request)
    )
    _string(campaign_id, "campaign_id", pattern=_ID_PATTERN)

    interaction = _call_exact_load(exact_load, "runtime.interaction", (admission_request.interaction_id,))
    _record_kind(interaction, "runtime.interaction")
    interaction_id = interaction.get("interaction_id", interaction.get("id"))
    if interaction_id != admission_request.interaction_id:
        raise CollaborationContractError("Interaction identity is stale or foreign")
    if interaction.get("campaign_id") != campaign_id:
        raise CollaborationContractError("Interaction campaign scope is stale or foreign")
    if interaction.get("intent_plan_id") != admission_request.intent_plan_id:
        raise CollaborationContractError("Interaction does not name the requested IntentPlan")
    _record_revision(interaction, "Interaction")

    intent_plan = _call_exact_load(exact_load, "runtime.intent_plan", (admission_request.intent_plan_id,))
    _record_kind(intent_plan, "runtime.intent_plan")
    intent_plan_id = intent_plan.get("intent_plan_id", intent_plan.get("id"))
    if intent_plan_id != admission_request.intent_plan_id:
        raise CollaborationContractError("IntentPlan identity is stale or foreign")
    if intent_plan.get("interaction_id") != admission_request.interaction_id:
        raise CollaborationContractError("IntentPlan does not belong to the requested Interaction")
    if intent_plan.get("campaign_id", campaign_id) != campaign_id:
        raise CollaborationContractError("IntentPlan campaign scope is stale or foreign")
    _record_revision(intent_plan, "IntentPlan")
    clauses = _sequence(intent_plan.get("clauses"), "IntentPlan clauses")
    clauses_by_id = {}
    for raw_clause in clauses:
        clause_value = _mapping(raw_clause, "IntentClause")
        clause_id = _string(clause_value.get("clause_id"), "clause_id", pattern=_ID_PATTERN)
        if clause_id in clauses_by_id:
            raise CollaborationContractError("IntentPlan contains duplicate clause IDs")
        clauses_by_id[clause_id] = clause_value
    clause = clauses_by_id.get(admission_request.clause_id)
    if clause is None:
        raise CollaborationContractError("requested IntentClause is not in the current IntentPlan")
    candidate = _candidate_from_clause(clause)
    candidate_player_ids = tuple(
        _string(item, "candidate participant player_id", pattern=_ID_PATTERN)
        for item in _sequence(candidate["participant_player_ids"], "candidate participant_player_ids")
    )
    if not candidate_player_ids or len(candidate_player_ids) != len(set(candidate_player_ids)):
        raise CollaborationContractError("coordination candidate participant IDs must be unique")

    native_owner_kind = _string(candidate["native_owner_kind"], "native owner kind")
    native_owner_id = _string(candidate["native_owner_id"], "native owner ID", pattern=_ID_PATTERN)
    opportunity_id = _string(candidate["opportunity_id"], "opportunity ID", pattern=_ID_PATTERN)
    purpose = _string(candidate["purpose"], "candidate purpose")
    dependency_scope = _string(candidate["dependency_scope"], "candidate dependency scope")

    resolved_principal = resolve_principal(principal)
    resolution = resolve_participant_authority(
        resolved_principal,
        player_route,
        load_exact_player,
        campaign_id=campaign_id,
    )
    if interaction.get("player_id") != resolution.player_id:
        raise CollaborationContractError("Interaction PLAYER is not the current authenticated PLAYER")
    if resolution.player_id not in candidate_player_ids:
        raise CollaborationContractError("current authenticated PLAYER is outside the nominated scope")

    native_owner = _call_exact_load(exact_load, native_owner_kind, (native_owner_id,))
    _record_kind(native_owner, native_owner_kind)
    _validate_identity(native_owner_kind, (native_owner_id,), native_owner)
    source_revision = _record_revision(native_owner, "native opportunity owner")
    state = native_owner.get("state", native_owner)
    state_mapping = _mapping(state, "native opportunity owner state")
    opportunity_values = _sequence(
        state_mapping.get("coordination_opportunities"),
        "native coordination opportunities",
    )
    opportunity: Mapping[str, object] | None = None
    for raw_opportunity in opportunity_values:
        item = _mapping(raw_opportunity, "native coordination opportunity")
        if item.get("opportunity_id") == opportunity_id:
            opportunity = item
            break
    if opportunity is None:
        raise CollaborationContractError("native decision opportunity is absent or stale")
    if opportunity.get("status") != "OPEN":
        raise CollaborationContractError(
            "native decision opportunity is not current",
            failure_code="collaboration.currentness_required",
        )
    if opportunity.get("purpose") != purpose or opportunity.get("dependency_scope") != dependency_scope:
        raise CollaborationContractError("native opportunity does not match the accepted candidate")
    positive_dependency = _boolean(
        opportunity.get("positive_material_dependency"),
        "native positive_material_dependency",
    )
    input_can_change_result = _boolean(
        opportunity.get("input_can_change_result"),
        "native input_can_change_result",
    )
    independently_durable = _boolean(
        opportunity.get("independently_durable"),
        "native independently_durable",
    )
    native_order_owner = opportunity.get("native_order_owner")
    if native_order_owner is not None:
        native_order_owner = _string(native_order_owner, "native order owner")
        if native_order_owner not in _ORDERED_OWNER_NAMES:
            raise CollaborationContractError("native order owner is not admitted")
    if native_owner_kind in {"runtime.procedure", "runtime.continuation"}:
        native_order_owner = native_owner_kind
    required = _participant_refs(opportunity.get("required_participants"), "native required participants")
    optional = _participant_refs(
        opportunity.get("optional_participants", ()),
        "native optional participants",
    )
    if not required:
        raise CollaborationContractError("native opportunity has no exact required participant authority")
    candidate_set = set(candidate_player_ids)
    if any(item.player_id not in candidate_set for item in required):
        raise CollaborationContractError("accepted candidate does not cover the native required participants")
    if set(item.identity for item in required).intersection(item.identity for item in optional):
        raise CollaborationContractError("native required and optional participants overlap")
    for participant in (*required, *optional):
        _load_player(exact_load, participant)
    return _NativeAdmissionEvidence(
        campaign_id=campaign_id,
        source_ref=f"{native_owner_kind}:{native_owner_id}",
        source_revision=source_revision,
        opportunity_ref=opportunity_id,
        purpose=purpose,
        dependency_scope=dependency_scope,
        positive_material_dependency=positive_dependency,
        input_can_change_result=input_can_change_result,
        independently_durable=independently_durable,
        required_contributors=required,
        optional_contributors=optional,
        native_order_owner=native_order_owner,
    )


def classify_coordination_dependency(
    request: CollaborationAdmissionRequest | Mapping[str, object],
    *,
    principal: VerifiedPrincipal | Mapping[str, object],
    player_route: PrincipalPlayerRoute | Mapping[str, object] | None,
    load_exact_player: PlayerLoader,
    exact_load: ExactLoadTransport | object,
    campaign_id: str,
) -> CoordinationFamily:
    """Choose a family from revalidated native evidence, never caller fields."""

    evidence = _prepare_admission(
        request,
        principal=principal,
        player_route=player_route,
        load_exact_player=load_exact_player,
        exact_load=exact_load,
        campaign_id=campaign_id,
    )
    if evidence.native_order_owner is not None:
        return CoordinationFamily.RULE_OWNED_ORDERED
    if not evidence.positive_material_dependency or not evidence.input_can_change_result:
        return CoordinationFamily.INDEPENDENT_IMMEDIATE
    return CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE


def open_or_successor_obligation(
    request: CollaborationAdmissionRequest | Mapping[str, object],
    *,
    principal: VerifiedPrincipal | Mapping[str, object],
    player_route: PrincipalPlayerRoute | Mapping[str, object] | None,
    load_exact_player: PlayerLoader,
    exact_load: ExactLoadTransport | object,
    campaign_id: str,
) -> CollaborationMutation:
    """Admit one base OPEN obligation after exact native revalidation."""

    admission_request = (
        request
        if isinstance(request, CollaborationAdmissionRequest)
        else CollaborationAdmissionRequest.from_mapping(request)
    )
    evidence = _prepare_admission(
        admission_request,
        principal=principal,
        player_route=player_route,
        load_exact_player=load_exact_player,
        exact_load=exact_load,
        campaign_id=campaign_id,
    )
    if evidence.native_order_owner is not None:
        return CollaborationMutation(
            CoordinationFamily.RULE_OWNED_ORDERED,
            "NATIVE_OWNER_REQUIRED",
            native_order_owner=evidence.native_order_owner,
        )
    if not evidence.positive_material_dependency or not evidence.input_can_change_result:
        return CollaborationMutation(
            CoordinationFamily.INDEPENDENT_IMMEDIATE,
            "INDEPENDENT_NO_OBLIGATION",
        )
    if not evidence.independently_durable:
        return CollaborationMutation(
            CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE,
            "EPHEMERAL_COORDINATION",
        )
    obligation = CollaborationObligation(
        obligation_id=admission_request.obligation_id,
        generation=admission_request.generation,
        lifecycle=CollaborationLifecycle.OPEN,
        purpose=evidence.purpose,
        dependency_scope=evidence.dependency_scope,
        decision_opportunity_ref=evidence.opportunity_ref,
        campaign_id=evidence.campaign_id,
        source_ref=evidence.source_ref,
        source_revision=evidence.source_revision,
        required_contributors=evidence.required_contributors,
        optional_contributors=evidence.optional_contributors,
    )
    return CollaborationMutation(
        CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE,
        "COLLECTIVE_ADMITTED",
        obligation=obligation,
    )


__all__ = [
    "COLLABORATION_KIND",
    "COLLABORATION_SCHEMA_VERSION",
    "FRAMEWORK_MODULE_VERSION",
    "CollaborationAdmissionRequest",
    "CollaborationContractError",
    "CollaborationLifecycle",
    "CollaborationMutation",
    "CollaborationObligation",
    "CoordinationFamily",
    "ExactLoadResult",
    "ExactLoadTransport",
    "ParticipantRef",
    "classify_coordination_dependency",
    "open_or_successor_obligation",
    "resolve_participant_authority",
]
