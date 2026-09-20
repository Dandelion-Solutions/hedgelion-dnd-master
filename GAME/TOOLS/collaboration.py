"""Owner-local coordination admission for scoped human collaboration.

This module owns only the admission boundary for a durable collaboration
obligation.  Native currentness, ordering and participant authority are
supplied as owner-issued evidence; caller-shaped family, contributor and
currentness fields are never treated as authority.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
import re
from typing import Final, NoReturn

from .access_control import (
    AccessControlContractError,
    PlayerLoader,
    VerifiedPrincipal,
    authorize_operation,
    resolve_player,
    resolve_principal,
)


# framework_module_version: 1.0.2
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.2"
COLLABORATION_SCHEMA_VERSION: Final[int] = 1
COLLABORATION_KIND: Final[str] = "runtime.collaboration_obligation"

_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_REVISION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$"
)
_NATIVE_ORDER_OWNERS: Final[frozenset[str]] = frozenset(
    {
        "Procedure",
        "Continuation",
        "Choice",
        "Reaction",
        "runtime.procedure",
        "runtime.continuation",
        "value.choice_request",
        "value.reaction_offer",
    }
)

_PARTICIPANT_ISSUER: Final[object] = object()
_BASIS_ISSUER: Final[object] = object()


class CollaborationContractError(ValueError):
    """Raised when collaboration admission evidence is malformed or stale."""

    failure_code: str

    def __init__(self, message: str, *, failure_code: str = "collaboration.contract_invalid") -> None:
        super().__init__(message)
        self.failure_code = failure_code


class CoordinationFamily(StrEnum):
    """Closed coordination-family classification."""

    INDEPENDENT_IMMEDIATE = "INDEPENDENT_IMMEDIATE"
    AGENCY_DEPENDENT_COLLECTIVE = "AGENCY_DEPENDENT_COLLECTIVE"
    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"


class CollaborationLifecycle(StrEnum):
    """Base obligation lifecycle; later tasks own transitions beyond OPEN."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RESOLVED = "RESOLVED"
    OBSOLETE = "OBSOLETE"


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


def _participant_sequence(value: object, label: str) -> tuple[ParticipantAuthority, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise CollaborationContractError(f"{label} must be an explicit participant sequence")
    participants = tuple(value)
    if any(
        not isinstance(participant, ParticipantAuthority)
        or not _is_owner_issued_participant(participant)
        for participant in participants
    ):
        raise CollaborationContractError(
            f"{label} requires exact participant authority from the access owner",
            failure_code="collaboration.participant_authority_required",
        )
    identities = tuple(participant.reference for participant in participants)
    if len(identities) != len(set(identities)):
        raise CollaborationContractError(f"{label} must contain unique participants")
    return tuple(sorted(participants, key=lambda item: item.reference))


@dataclass(frozen=True, slots=True)
class ParticipantRef:
    """Persistent participant reference derived from exact access evidence."""

    player_id: str
    pc_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "player_id", _string(self.player_id, "participant player_id", pattern=_ID_PATTERN))
        if self.pc_id is not None:
            object.__setattr__(self, "pc_id", _string(self.pc_id, "participant pc_id", pattern=_ID_PATTERN))

    @property
    def reference(self) -> tuple[str, str]:
        return self.player_id, self.pc_id or ""

    def as_mapping(self) -> dict[str, str]:
        result = {"player_id": self.player_id}
        if self.pc_id is not None:
            result["pc_id"] = self.pc_id
        return result


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ParticipantAuthority:
    """Opaque current principal/PLAYER/controlled-PC authority result.

    The access owner issues this value through ``resolve_participant_authority``.
    A caller-provided player ID, login or PC ID cannot construct an admitted
    authority value by shape alone.
    """

    stable_account_id: str
    player_id: str
    controlled_pc_id: str | None = None
    _issuer: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._issuer is not _PARTICIPANT_ISSUER:
            raise CollaborationContractError(
                "participant authority must be issued by the access owner",
                failure_code="collaboration.participant_authority_required",
            )
        object.__setattr__(self, "stable_account_id", _string(self.stable_account_id, "stable_account_id"))
        object.__setattr__(self, "player_id", _string(self.player_id, "participant player_id", pattern=_ID_PATTERN))
        if self.controlled_pc_id is not None:
            object.__setattr__(
                self,
                "controlled_pc_id",
                _string(self.controlled_pc_id, "controlled_pc_id", pattern=_ID_PATTERN),
            )

    @property
    def reference(self) -> tuple[str, str]:
        return self.player_id, self.controlled_pc_id or ""

    def to_participant_ref(self) -> ParticipantRef:
        return ParticipantRef(self.player_id, self.controlled_pc_id)


def _is_owner_issued_participant(value: object) -> bool:
    return isinstance(value, ParticipantAuthority) and value._issuer is _PARTICIPANT_ISSUER


def resolve_participant_authority(
    principal: VerifiedPrincipal | Mapping[str, object],
    route: object,
    load_exact_player: PlayerLoader,
    *,
    campaign_id: str,
    controlled_pc_id: str | None = None,
) -> ParticipantAuthority:
    """Resolve one exact participant through the existing access-control owner."""

    try:
        resolved_principal = resolve_principal(principal)
        resolution = resolve_player(
            resolved_principal,
            route,  # type: ignore[arg-type]
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
        try:
            requested_pc_id = _string(controlled_pc_id, "controlled_pc_id", pattern=_ID_PATTERN)
        except CollaborationContractError as error:
            raise CollaborationContractError(
                "controlled PC authority is malformed",
                failure_code="collaboration.controlled_pc_invalid",
            ) from error
        if requested_pc_id not in resolution.player.controlled_pc_ids:
            raise CollaborationContractError(
                "participant does not currently control the requested PC",
                failure_code="collaboration.controlled_pc_not_authorized",
            )
    else:
        requested_pc_id = None
    return ParticipantAuthority(
        stable_account_id=resolved_principal.stable_account_id,
        player_id=resolution.player.player_id,
        controlled_pc_id=requested_pc_id,
        _issuer=_PARTICIPANT_ISSUER,
    )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class NativeCoordinationBasis:
    """Owner-issued current dependency evidence used for family admission."""

    campaign_id: str
    source_ref: str
    source_revision: str
    opportunity_ref: str
    positive_material_dependency: bool
    input_can_change_result: bool
    opportunity_current: bool
    independently_durable: bool
    required_participants: tuple[ParticipantAuthority, ...]
    purpose: str = ""
    dependency_scope: str = ""
    optional_participants: tuple[ParticipantAuthority, ...] = ()
    native_order_owner: str | None = None
    semantic_value_kind: str | None = None
    _issuer: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._issuer is not _BASIS_ISSUER:
            raise CollaborationContractError(
                "coordination basis must be issued by a native owner",
                failure_code="collaboration.native_basis_required",
            )
        object.__setattr__(self, "campaign_id", _string(self.campaign_id, "basis campaign_id", pattern=_ID_PATTERN))
        object.__setattr__(self, "source_ref", _string(self.source_ref, "basis source_ref"))
        object.__setattr__(
            self,
            "source_revision",
            _string(self.source_revision, "basis source_revision", pattern=_REVISION_PATTERN),
        )
        object.__setattr__(self, "opportunity_ref", _string(self.opportunity_ref, "basis opportunity_ref"))
        object.__setattr__(self, "purpose", _string(self.purpose, "basis purpose"))
        object.__setattr__(self, "dependency_scope", _string(self.dependency_scope, "basis dependency_scope"))
        for field_name in (
            "positive_material_dependency",
            "input_can_change_result",
            "opportunity_current",
            "independently_durable",
        ):
            _boolean(getattr(self, field_name), f"basis {field_name}")
        object.__setattr__(
            self,
            "required_participants",
            _participant_sequence(self.required_participants, "required_participants"),
        )
        object.__setattr__(
            self,
            "optional_participants",
            _participant_sequence(self.optional_participants, "optional_participants"),
        )
        required_refs = {participant.reference for participant in self.required_participants}
        optional_refs = {participant.reference for participant in self.optional_participants}
        if required_refs.intersection(optional_refs):
            raise CollaborationContractError("required and optional participants must be disjoint")
        if self.native_order_owner is not None:
            owner = _string(self.native_order_owner, "native_order_owner")
            if owner not in _NATIVE_ORDER_OWNERS:
                raise CollaborationContractError("native order owner is not admitted")
            object.__setattr__(self, "native_order_owner", owner)
        if self.semantic_value_kind == "value.contribution":
            raise CollaborationContractError(
                "mechanical value.contribution is not human collaboration input",
                failure_code="collaboration.mechanical_contribution_rejected",
            )

    @property
    def current(self) -> bool:
        """Compatibility alias; currentness still comes from this owner-issued basis."""

        return self.opportunity_current


def issue_native_coordination_basis(
    *_args: object,
    **_kwargs: object,
) -> NoReturn:
    """Reject the former public evidence-minting surface.

    Native currentness/dependency owners must use their private owner-native
    handoff; a public constructor-like helper cannot mint collaboration
    authority from shaped caller input.
    """

    raise CollaborationContractError(
        "native coordination evidence issuance is not public",
        failure_code="collaboration.native_basis_not_public",
    )


def _owner_issue_native_coordination_basis(
    *,
    campaign_id: str,
    source_ref: str,
    source_revision: str,
    opportunity_ref: str,
    purpose: str,
    dependency_scope: str,
    positive_material_dependency: bool,
    input_can_change_result: bool,
    opportunity_current: bool,
    independently_durable: bool,
    required_participants: Sequence[ParticipantAuthority],
    optional_participants: Sequence[ParticipantAuthority] = (),
    native_order_owner: str | None = None,
    semantic_value_kind: str | None = None,
) -> NativeCoordinationBasis:
    """Internal native-owner handoff used until the producing owner is wired."""

    return NativeCoordinationBasis(
        campaign_id=campaign_id,
        source_ref=source_ref,
        source_revision=source_revision,
        opportunity_ref=opportunity_ref,
        purpose=purpose,
        dependency_scope=dependency_scope,
        positive_material_dependency=positive_material_dependency,
        input_can_change_result=input_can_change_result,
        opportunity_current=opportunity_current,
        independently_durable=independently_durable,
        required_participants=tuple(required_participants),
        optional_participants=tuple(optional_participants),
        native_order_owner=native_order_owner,
        semantic_value_kind=semantic_value_kind,
        _issuer=_BASIS_ISSUER,
    )


def _is_owner_issued_basis(value: object) -> bool:
    return type(value) is NativeCoordinationBasis and value._issuer is _BASIS_ISSUER


def classify_coordination_dependency(basis: NativeCoordinationBasis) -> CoordinationFamily:
    """Derive the family from owner evidence; never accept a requested family."""

    if not _is_owner_issued_basis(basis):
        raise CollaborationContractError(
            "coordination family requires native-owner evidence",
            failure_code="collaboration.native_basis_required",
        )
    if basis.native_order_owner is not None:
        return CoordinationFamily.RULE_OWNED_ORDERED
    if not basis.positive_material_dependency or not basis.input_can_change_result:
        return CoordinationFamily.INDEPENDENT_IMMEDIATE
    if not basis.opportunity_current:
        return CoordinationFamily.INDEPENDENT_IMMEDIATE
    return CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE


@dataclass(frozen=True, slots=True)
class CollaborationAdmissionRequest:
    """Caller request containing identity/purpose only, never authority."""

    obligation_id: str
    purpose: str
    dependency_scope: str
    decision_opportunity_ref: str
    generation: int = 1

    def __post_init__(self) -> None:
        for field_name in (
            "obligation_id",
        ):
            object.__setattr__(
                self,
                field_name,
                _string(getattr(self, field_name), field_name, pattern=_ID_PATTERN),
            )
        for field_name in ("purpose", "dependency_scope", "decision_opportunity_ref"):
            object.__setattr__(self, field_name, _string(getattr(self, field_name), field_name))
        if isinstance(self.generation, bool) or not isinstance(self.generation, int) or self.generation < 1:
            raise CollaborationContractError("generation must be a positive integer")

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> CollaborationAdmissionRequest:
        if not isinstance(value, Mapping):
            raise CollaborationContractError("collaboration request must be an object")
        allowed = {
            "obligation_id",
            "purpose",
            "dependency_scope",
            "decision_opportunity_ref",
            "generation",
        }
        unknown = set(value) - allowed
        if unknown:
            raise CollaborationContractError(
                "caller cannot select coordination family, contributors or currentness",
                failure_code="collaboration.caller_authority_fields",
            )
        required = {"obligation_id", "purpose", "dependency_scope", "decision_opportunity_ref"}
        if required - set(value):
            raise CollaborationContractError("collaboration request is incomplete")
        return cls(
            obligation_id=value["obligation_id"],  # type: ignore[arg-type]
            purpose=value["purpose"],  # type: ignore[arg-type]
            dependency_scope=value["dependency_scope"],  # type: ignore[arg-type]
            decision_opportunity_ref=value["decision_opportunity_ref"],  # type: ignore[arg-type]
            generation=value.get("generation", 1),  # type: ignore[arg-type]
        )


@dataclass(frozen=True, slots=True)
class CollaborationObligation:
    """Persistent collection owner state created only for durable collective work."""

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
    optional_contributors: tuple[ParticipantRef, ...]
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
    """Admission result; non-collective families never contain an obligation."""

    family: CoordinationFamily
    disposition: str
    obligation: CollaborationObligation | None = None
    native_order_owner: str | None = None


def open_or_successor_obligation(
    request: CollaborationAdmissionRequest | Mapping[str, object],
    current_basis: NativeCoordinationBasis,
) -> CollaborationMutation:
    """Admit a base obligation only after family and exact authority checks."""

    admission_request = (
        request
        if isinstance(request, CollaborationAdmissionRequest)
        else CollaborationAdmissionRequest.from_mapping(request)
    )
    if not _is_owner_issued_basis(current_basis):
        raise CollaborationContractError(
            "currentness must come from the native owner",
            failure_code="collaboration.native_basis_required",
        )
    if (
        admission_request.purpose != current_basis.purpose
        or admission_request.dependency_scope != current_basis.dependency_scope
        or admission_request.decision_opportunity_ref != current_basis.opportunity_ref
    ):
        raise CollaborationContractError(
            "admission request does not match the native dependency opportunity",
            failure_code="collaboration.native_basis_mismatch",
        )
    if current_basis.campaign_id == "":  # pragma: no cover - constructor prevents this
        raise CollaborationContractError("current campaign basis is missing")
    if not current_basis.opportunity_current:
        raise CollaborationContractError(
            "current collaboration opportunity is not proven",
            failure_code="collaboration.currentness_required",
        )
    family = classify_coordination_dependency(current_basis)
    if family is CoordinationFamily.INDEPENDENT_IMMEDIATE:
        return CollaborationMutation(family, "INDEPENDENT_NO_OBLIGATION")
    if family is CoordinationFamily.RULE_OWNED_ORDERED:
        return CollaborationMutation(
            family,
            "NATIVE_OWNER_REQUIRED",
            native_order_owner=current_basis.native_order_owner,
        )
    if not current_basis.independently_durable:
        return CollaborationMutation(family, "EPHEMERAL_COORDINATION")
    if not current_basis.required_participants:
        raise CollaborationContractError(
            "durable collective admission requires exact required participants",
            failure_code="collaboration.participant_authority_required",
        )
    required = tuple(participant.to_participant_ref() for participant in current_basis.required_participants)
    optional = tuple(participant.to_participant_ref() for participant in current_basis.optional_participants)
    obligation = CollaborationObligation(
        obligation_id=admission_request.obligation_id,
        generation=admission_request.generation,
        lifecycle=CollaborationLifecycle.OPEN,
        purpose=admission_request.purpose,
        dependency_scope=admission_request.dependency_scope,
        decision_opportunity_ref=admission_request.decision_opportunity_ref,
        campaign_id=current_basis.campaign_id,
        source_ref=current_basis.source_ref,
        source_revision=current_basis.source_revision,
        required_contributors=required,
        optional_contributors=optional,
    )
    return CollaborationMutation(family, "COLLECTIVE_ADMITTED", obligation=obligation)


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
    "NativeCoordinationBasis",
    "ParticipantAuthority",
    "ParticipantRef",
    "classify_coordination_dependency",
    "open_or_successor_obligation",
    "resolve_participant_authority",
]
