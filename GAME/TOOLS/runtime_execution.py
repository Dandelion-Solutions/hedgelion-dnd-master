"""Typed acceptance and verification for authoritative ``runtime.command`` records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from .catalog_runtime import (
    BoundCatalogContext,
    CatalogBindingError,
    bind_executable_catalog,
    canonical_json,
    sha256,
    validate_executable_binding,
)
from .native_storage import (
    IdentityMismatch,
    NativeStorageError,
    route_native_record,
    validate_loaded_identity,
)
from .policy_basis import (
    AcceptedAdjudicationBasis,
    PinnedCampaign,
    PolicyBasisResolutionError,
    is_accepted_basis_issued,
    validate_adjudicated_input_surface,
    validate_frozen_adjudication_basis,
    validate_policy_applicability_witnesses,
)

# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.5"
RUNTIME_COMMAND_SCHEMA_VERSION: Final = 3
INTERPRETER_RESULT_FINGERPRINT_GENERATION: Final = 1
RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION: Final = 2
INTERPRETER_RESULT_FIELDS: Final = frozenset(
    {"kind", "purpose", "bundle_id", "source_generation", "intent"}
)
COMMAND_PROPOSAL_FIELDS: Final = frozenset(
    {
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "action_request",
        "root_resolution_id",
    }
)
COMMAND_STATE_FIELDS: Final = frozenset(
    {
        "schema_version",
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "command_kind",
        "catalog_context_fingerprint",
        "input_fingerprint_generation",
        "input_fingerprint",
        "disposition",
        "invocation_facts",
        "action_request",
        "root_resolution_id",
        "pending_child_invocations",
        "interpreter_result",
        "interpreter_result_fingerprint_generation",
        "interpreter_result_fingerprint",
        "catalog_context",
        "candidate_binding",
    }
)
ACCEPTED_INPUT_FIELDS: Final = frozenset(
    {
        "command_kind",
        "catalog_context_fingerprint",
        "invocation_facts",
        "action_request",
        "interpreter_result",
        "interpreter_result_fingerprint_generation",
        "interpreter_result_fingerprint",
        "catalog_context",
        "candidate_binding",
    }
)
_INTERPRETER_RESULT_DOMAIN: Final = b"HDM_INTERPRETER_RESULT/1\n"
_RUNTIME_COMMAND_INPUT_DOMAIN: Final = b"HDM_RUNTIME_COMMAND_INPUT/2\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")


class CommandAcceptanceError(ValueError):
    """Raised when a command is not a valid accepted ``runtime.command`` record."""


class NativeOrderingError(ValueError):
    """Raised when a native ordered-owner proof cannot be established."""


class NativeOrderingStatus(StrEnum):
    """Ephemeral native ordered-owner result status."""

    RULE_OWNED_ORDERED = "RULE_OWNED_ORDERED"
    NO_ORDERED_OWNER = "NO_ORDERED_OWNER"


@dataclass(frozen=True, slots=True)
class NativeOrderingEvidence:
    """Derived evidence for one exact current Step-3 ordered offer."""

    status: NativeOrderingStatus
    campaign_id: str
    source_scope: str
    source_key: str
    source_revision: str
    resolution_id: str
    continuation_id: str
    continuation_generation: int
    offer_kind: str
    offer_id: str
    responder_id: str
    procedure_id: str | None = None


@dataclass(frozen=True, slots=True)
class NativeOrderingNoOwner:
    """Ephemeral negative result when no exact Resolution reference is requested."""

    status: NativeOrderingStatus
    campaign_id: str
    route: str = "runtime_execution"


class CatalogGap:
    """Typed non-acceptance evidence for an unavailable catalog candidate."""

    __slots__ = ("gap_report",)

    def __init__(self, gap_report: Mapping[str, object]) -> None:
        self.gap_report = MappingProxyType(dict(gap_report))


_ORDERING_FAMILIES: Final[frozenset[str]] = frozenset(
    {"runtime.resolution", "runtime.continuation", "runtime.procedure"}
)
_ORDERING_REQUEST_FIELDS: Final[frozenset[str]] = frozenset({"resolution_id"})
_CHOICE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "kind",
        "offer_id",
        "parent_resolution_id",
        "continuation_generation",
        "responder_id",
        "option_ids",
    }
)
_REACTION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "kind",
        "offer_id",
        "parent_resolution_id",
        "continuation_generation",
        "responder_id",
        "candidate_activity_ids",
    }
)


def _ordering_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise NativeOrderingError(f"{label} must be a nonempty string")
    return value


def _ordering_record(
    repository: object, campaign_pin: PinnedCampaign, family: str, record_id: str
) -> Mapping[str, object]:
    if family not in _ORDERING_FAMILIES:
        raise NativeOrderingError("native ordering family is not admitted")
    try:
        route = route_native_record(family, (record_id,))
        payload = repository.read_exact_path(campaign_pin, route.relative_path)
        if not isinstance(payload, Mapping):
            raise NativeOrderingError(f"exact {family} record is not an object")
        validate_loaded_identity(family, (record_id,), payload)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        if isinstance(exc, NativeOrderingError):
            raise
        if isinstance(exc, (IdentityMismatch, NativeStorageError)):
            raise NativeOrderingError(f"exact {family} identity is stale or foreign") from exc
        raise NativeOrderingError(f"exact {family} owner read failed") from exc
    if payload.get("campaign_id") not in {None, campaign_pin.campaign_id}:
        raise NativeOrderingError(f"exact {family} belongs to another campaign")
    record_revision = payload.get("revision")
    if record_revision is not None and record_revision != campaign_pin.revision:
        raise NativeOrderingError(f"exact {family} record is stale")
    return payload


def _pending_offer(
    response: object,
    *,
    resolution_id: str,
    continuation_generation: int,
) -> tuple[str, str, str]:
    offer = response if isinstance(response, Mapping) else None
    if offer is None or set(offer) not in {_CHOICE_FIELDS, _REACTION_FIELDS}:
        raise NativeOrderingError("continuation pending response is not a valid ChoiceRequest or ReactionOffer")
    kind = offer.get("kind")
    expected_fields = _CHOICE_FIELDS if kind == "choice" else _REACTION_FIELDS if kind == "reaction" else None
    if expected_fields is None or set(offer) != expected_fields:
        raise NativeOrderingError("continuation pending response kind is not admitted")
    offer_id = _ordering_text(offer.get("offer_id"), "pending offer id")
    if offer.get("parent_resolution_id") != resolution_id:
        raise NativeOrderingError("pending offer does not belong to the current resolution")
    if offer.get("continuation_generation") != continuation_generation:
        raise NativeOrderingError("pending offer generation differs from the current continuation")
    responder_id = _ordering_text(offer.get("responder_id"), "pending responder id")
    item_field = "option_ids" if kind == "choice" else "candidate_activity_ids"
    item_ids = offer.get(item_field)
    if (
        not isinstance(item_ids, Sequence)
        or isinstance(item_ids, (str, bytes))
        or not item_ids
        or any(not isinstance(item, str) or not item for item in item_ids)
        or len(item_ids) != len(set(item_ids))
    ):
        raise NativeOrderingError("pending offer candidates are invalid")
    return str(kind), offer_id, responder_id


def _validate_linked_procedure(
    repository: object,
    campaign_pin: PinnedCampaign,
    resolution: Mapping[str, object],
    continuation: Mapping[str, object],
    procedure_id: object,
) -> str:
    procedure_ref = _ordering_text(procedure_id, "linked procedure id")
    continuation_procedure = continuation.get("procedure_id")
    if continuation_procedure != procedure_ref:
        raise NativeOrderingError("resolution and continuation procedure linkage differs")
    procedure = _ordering_record(repository, campaign_pin, "runtime.procedure", procedure_ref)
    declared_procedure_id = procedure.get("procedure_id", procedure.get("id"))
    if declared_procedure_id != procedure_ref:
        raise NativeOrderingError("linked procedure identity differs from its native route")
    state = procedure.get("state")
    if state is not None and not isinstance(state, Mapping):
        raise NativeOrderingError("linked procedure state is malformed")
    procedure_state = state if isinstance(state, Mapping) else procedure
    if procedure_state.get("schema_version") != 2 or procedure_state.get("lifecycle") != "ACTIVE":
        raise NativeOrderingError("linked procedure is not current schema v2 ACTIVE")
    for field, expected in (
        ("resolution_id", resolution.get("id")),
        ("continuation_id", continuation.get("id")),
    ):
        declared = procedure.get(field, procedure_state.get(field))
        if declared is not None and declared != expected:
            raise NativeOrderingError("linked procedure identity is inconsistent")
    return procedure_ref


def resolve_native_ordering_evidence(
    request: object,
    *,
    repository: object,
    campaign_pin: PinnedCampaign,
    selected_live: object,
) -> NativeOrderingEvidence | NativeOrderingNoOwner:
    """Produce the sole generation-1 ``RULE_OWNED_ORDERED`` evidence.

    The caller supplies only an exact Resolution reference.  Continuation,
    Procedure, status, pending offer and family values are loaded from their
    current owner records and are never accepted as caller evidence.
    """
    del selected_live
    if isinstance(request, Mapping) and "resolution_id" not in request:
        return NativeOrderingNoOwner(
            status=NativeOrderingStatus.NO_ORDERED_OWNER,
            campaign_id=campaign_pin.campaign_id,
        )
    if not isinstance(request, Mapping) or set(request) != _ORDERING_REQUEST_FIELDS:
        raise NativeOrderingError("native ordering request must contain only resolution_id")
    resolution_id = _ordering_text(request.get("resolution_id"), "resolution id")
    resolution = _ordering_record(repository, campaign_pin, "runtime.resolution", resolution_id)
    declared_resolution_id = resolution.get("resolution_id", resolution.get("id"))
    if declared_resolution_id != resolution_id:
        raise NativeOrderingError("resolution identity differs from requested identity")
    status = resolution.get("status")
    if status not in {"AWAITING_CHOICE", "AWAITING_REACTION"}:
        raise NativeOrderingError("resolution is not awaiting an owner response")
    continuation_id = _ordering_text(resolution.get("continuation_id"), "resolution continuation id")
    continuation = _ordering_record(
        repository, campaign_pin, "runtime.continuation", continuation_id
    )
    if continuation.get("resolution_id") != resolution_id:
        raise NativeOrderingError("continuation does not belong to the current resolution")
    generation = continuation.get("generation")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        raise NativeOrderingError("continuation generation is invalid")
    expected_generation = resolution.get("continuation_generation")
    if expected_generation is not None and expected_generation != generation:
        raise NativeOrderingError("resolution continuation generation is stale")
    offer_kind, offer_id, responder_id = _pending_offer(
        continuation.get("pending_response"),
        resolution_id=resolution_id,
        continuation_generation=generation,
    )
    if (status == "AWAITING_CHOICE" and offer_kind != "choice") or (
        status == "AWAITING_REACTION" and offer_kind != "reaction"
    ):
        raise NativeOrderingError("resolution status does not match pending offer kind")
    resolution_procedure = resolution.get("procedure_id")
    continuation_procedure = continuation.get("procedure_id")
    if (resolution_procedure is None) != (continuation_procedure is None):
        raise NativeOrderingError("resolution and continuation procedure linkage is incomplete")
    procedure_id = None
    if resolution_procedure is not None:
        procedure_id = _validate_linked_procedure(
            repository,
            campaign_pin,
            resolution,
            continuation,
            resolution_procedure,
        )
    return NativeOrderingEvidence(
        status=NativeOrderingStatus.RULE_OWNED_ORDERED,
        campaign_id=campaign_pin.campaign_id,
        source_scope="campaign",
        source_key=f"runtime.resolution/{resolution_id}",
        source_revision=campaign_pin.revision,
        resolution_id=resolution_id,
        continuation_id=continuation_id,
        continuation_generation=generation,
        offer_kind=offer_kind,
        offer_id=offer_id,
        responder_id=responder_id,
        procedure_id=procedure_id,
    )


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_thaw(item) for item in value]
    return value


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CommandAcceptanceError(f"{label} must be an object")
    return value


def _require_exact_fields(
    value: object, fields: frozenset[str], label: str
) -> Mapping[str, object]:
    mapping = _require_mapping(value, label)
    if set(mapping) != fields:
        raise CommandAcceptanceError(f"{label} has unexpected or missing fields")
    return mapping


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CommandAcceptanceError(f"{label} must be a nonempty string")
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in _SHA256_HEX for char in value):
        raise CommandAcceptanceError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _typed_interpreter_result(value: object) -> dict[str, str]:
    raw_result = _require_exact_fields(value, INTERPRETER_RESULT_FIELDS, "interpreter result")
    result = {
        field: _require_nonempty_string(raw_result[field], f"interpreter result {field}")
        for field in INTERPRETER_RESULT_FIELDS
    }
    if result["kind"] != "interpreter_result":
        raise CommandAcceptanceError("interpreter result kind is not interpreter_result")
    return result


def _candidate_identity(value: object) -> tuple[str, str]:
    candidate = _require_exact_fields(value, frozenset({"definition_id", "kind"}), "candidate")
    return (
        _require_nonempty_string(candidate["definition_id"], "candidate definition_id"),
        _require_nonempty_string(candidate["kind"], "candidate kind"),
    )


def _typed_command_proposal(value: object, candidate_id: str) -> dict[str, object]:
    proposal = _require_exact_fields(value, COMMAND_PROPOSAL_FIELDS, "command proposal")
    normalized = {
        field: _require_nonempty_string(proposal[field], f"command proposal {field}")
        for field in (
            "command_id",
            "interaction_id",
            "intent_plan_id",
            "clause_id",
            "root_resolution_id",
        )
    }
    action_request = _require_mapping(proposal["action_request"], "command proposal action_request")
    allowed_action_fields = {"activity_id", "actor_id", "source_id", "target_ids", "parameter_bindings"}
    if set(action_request) - allowed_action_fields or not {"activity_id", "actor_id"}.issubset(
        action_request
    ):
        raise CommandAcceptanceError("command proposal action_request has unexpected or missing fields")
    activity_id = _require_nonempty_string(action_request["activity_id"], "action_request activity_id")
    if activity_id != candidate_id:
        raise CommandAcceptanceError("action_request activity_id differs from candidate")
    if "parameter_bindings" in action_request:
        try:
            parameter_bindings, _facts, _refs = validate_frozen_adjudication_basis(
                action_request["parameter_bindings"], []
            )
        except PolicyBasisResolutionError as exc:
            raise CommandAcceptanceError(str(exc)) from exc
        normalized_action_request = _thaw(action_request)
        if not isinstance(normalized_action_request, dict):
            raise CommandAcceptanceError("action_request must be an object")
        normalized_action_request["parameter_bindings"] = parameter_bindings
        normalized["action_request"] = normalized_action_request
    else:
        normalized["action_request"] = _thaw(action_request)
    return normalized


def _interpreter_result_fingerprint(interpreter_result: Mapping[str, str]) -> str:
    return sha256(_INTERPRETER_RESULT_DOMAIN + canonical_json(dict(interpreter_result)))


def _input_fingerprint(command: Mapping[str, object]) -> str:
    material = {
        key: _thaw(command[key])
        for key in ACCEPTED_INPUT_FIELDS
    }
    return sha256(_RUNTIME_COMMAND_INPUT_DOMAIN + canonical_json(material))


def _require_admitted_context(context: object) -> BoundCatalogContext:
    if not isinstance(context, BoundCatalogContext) or not context._is_admitted():
        raise CommandAcceptanceError("catalog context must be an admitted bound context")
    return context


def accept_command(
    interpreter_result: object,
    context: BoundCatalogContext,
    candidate: object,
    command_proposal: object,
    *,
    adjudication_basis: AcceptedAdjudicationBasis | None = None,
) -> dict[str, object] | CatalogGap:
    """Return a schema-shaped accepted command or typed catalog-gap evidence."""

    typed_result = _typed_interpreter_result(interpreter_result)
    admitted_context = _require_admitted_context(context)
    candidate_id, _candidate_kind = _candidate_identity(candidate)
    proposal = _typed_command_proposal(command_proposal, candidate_id)
    action_request = _require_mapping(proposal["action_request"], "accepted action_request")
    if adjudication_basis is not None:
        if not is_accepted_basis_issued(adjudication_basis):
            raise CommandAcceptanceError("adjudication basis must be resolver-produced evidence")
        expected_bindings = adjudication_basis.runtime_parameter_bindings()
        actual_bindings = action_request.get("parameter_bindings", {})
        if actual_bindings != expected_bindings:
            raise CommandAcceptanceError("accepted adjudication parameters differ from verified basis")
        invocation_facts = adjudication_basis.runtime_invocation_facts()
    else:
        invocation_facts = []
        if any(
            isinstance(binding, Mapping)
            and binding.get("source_class") == "INVOCATION_ADJUDICATED"
            for binding in action_request.get("parameter_bindings", {}).values()
        ):
            raise CommandAcceptanceError("adjudicated parameters require a verified policy basis")
    try:
        normalized_parameters, normalized_facts = validate_adjudicated_input_surface(
            str(action_request["activity_id"]),
            action_request.get("parameter_bindings", {}),
            invocation_facts,
        )
        if adjudication_basis is not None:
            validate_policy_applicability_witnesses(
                adjudication_basis.verified_policies,
                str(action_request["activity_id"]),
                admitted_context,
            )
    except PolicyBasisResolutionError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if adjudication_basis is not None and normalized_parameters != expected_bindings:
        raise CommandAcceptanceError("accepted adjudication parameters differ from verified basis")
    invocation_facts = normalized_facts
    try:
        catalog_result = bind_executable_catalog(admitted_context, candidate)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if catalog_result["status"] == "gap":
        return CatalogGap(_require_mapping(catalog_result["gap_report"], "catalog gap report"))

    binding = _require_mapping(catalog_result["binding"], "catalog binding")
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    command: dict[str, object] = {
        "schema_version": RUNTIME_COMMAND_SCHEMA_VERSION,
        **proposal,
        "command_kind": "action",
        "catalog_context_fingerprint": admitted_context.fingerprint,
        "input_fingerprint_generation": RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION,
        "input_fingerprint": "",
        "disposition": "command.accepted",
        "invocation_facts": invocation_facts,
        "pending_child_invocations": [],
        "interpreter_result": typed_result,
        "interpreter_result_fingerprint_generation": INTERPRETER_RESULT_FINGERPRINT_GENERATION,
        "interpreter_result_fingerprint": _interpreter_result_fingerprint(typed_result),
        "catalog_context": admitted_context.to_dict(),
        "candidate_binding": _thaw(binding),
    }
    command["input_fingerprint"] = _input_fingerprint(command)
    return command


def validate_execution_proposal(
    accepted_command: object,
    context: BoundCatalogContext,
    candidate: object,
) -> None:
    """Verify a serialized command's exact basis and recomputed acceptance fingerprints."""

    command = _require_exact_fields(accepted_command, COMMAND_STATE_FIELDS, "accepted command")
    admitted_context = _require_admitted_context(context)
    if command["schema_version"] != RUNTIME_COMMAND_SCHEMA_VERSION:
        raise CommandAcceptanceError("unsupported runtime command schema version")
    for field in ("command_id", "interaction_id", "intent_plan_id", "clause_id", "root_resolution_id"):
        _require_nonempty_string(command[field], f"accepted command {field}")
    if command["command_kind"] != "action" or command["disposition"] not in {
        "command.accepted",
        "command.settled",
    }:
        raise CommandAcceptanceError("accepted command has an unsupported disposition")
    if not isinstance(command["invocation_facts"], list):
        raise CommandAcceptanceError("accepted command invocation facts must be an array")
    action_request = _require_mapping(command["action_request"], "accepted command action_request")
    try:
        parameters, facts = validate_adjudicated_input_surface(
            _require_nonempty_string(action_request.get("activity_id"), "action_request activity_id"),
            action_request.get("parameter_bindings", {}),
            command["invocation_facts"],
        )
    except PolicyBasisResolutionError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if parameters != action_request.get("parameter_bindings", {}) or facts != command["invocation_facts"]:
        raise CommandAcceptanceError("accepted adjudication input differs from its normalized basis")
    if not isinstance(command["pending_child_invocations"], list):
        raise CommandAcceptanceError("accepted command pending child invocations must be an array")
    if command["disposition"] == "command.settled" and command["pending_child_invocations"]:
        raise CommandAcceptanceError("settled command retains pending child invocations")
    if command["input_fingerprint_generation"] != RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION:
        raise CommandAcceptanceError("unsupported command input fingerprint generation")
    if command["interpreter_result_fingerprint_generation"] != INTERPRETER_RESULT_FINGERPRINT_GENERATION:
        raise CommandAcceptanceError("unsupported interpreter result fingerprint generation")
    interpreter_result = _typed_interpreter_result(command["interpreter_result"])
    if command["interpreter_result_fingerprint"] != _interpreter_result_fingerprint(interpreter_result):
        raise CommandAcceptanceError("interpreter result fingerprint differs from accepted result")
    if command["catalog_context_fingerprint"] != admitted_context.fingerprint:
        raise CommandAcceptanceError("stale catalog context")
    if command["catalog_context"] != admitted_context.to_dict():
        raise CommandAcceptanceError("catalog context differs from accepted basis")
    binding = _require_mapping(command["candidate_binding"], "accepted command catalog binding")
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    candidate_id, candidate_kind = _candidate_identity(candidate)
    if candidate_id != binding["definition_id"] or candidate_kind != binding["kind"]:
        raise CommandAcceptanceError("candidate differs from accepted binding")
    _typed_command_proposal(
        {
            key: command[key]
            for key in COMMAND_PROPOSAL_FIELDS
        },
        candidate_id,
    )
    _require_sha256(command["input_fingerprint"], "accepted command input fingerprint")
    if command["input_fingerprint"] != _input_fingerprint(command):
        raise CommandAcceptanceError("input fingerprint differs from accepted command")
