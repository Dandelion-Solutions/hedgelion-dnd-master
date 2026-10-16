"""Typed acceptance and verification for authoritative ``runtime.command`` records."""

from __future__ import annotations

import math
import re
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
from .current_owner import CurrentOwnerObservation, CurrentOwnerStatus, NativeOwnerRef
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
from .structural_contracts import StructuralContractError, validate_contract

# framework_module_version: 1.0.11
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.11"
RUNTIME_COMMAND_SCHEMA_VERSION: Final = 4
INTERPRETER_RESULT_FINGERPRINT_GENERATION: Final = 1
RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION: Final = 3
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
_INTERPRETER_RESULT_DOMAIN: Final = b"HDM_INTERPRETER_RESULT/1\n"
_RUNTIME_COMMAND_INPUT_DOMAIN: Final = b"HDM_RUNTIME_COMMAND_INPUT/3\n"
RESUME_INPUT_FINGERPRINT_GENERATION: Final = 1
_ACCEPTED_RESUME_INPUT_DOMAIN: Final = b"HDM_ACCEPTED_RESUME_INPUT/1\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")


class CommandAcceptanceError(ValueError):
    """Raised when a command is not a valid accepted ``runtime.command`` record."""


def input_native_state(owner: Mapping[str, object], kind: str) -> Mapping[str, object]:
    """Read envelope identity first; flattened projections never override state.

    This is source grammar, not external authentication or native acceptance.
    """
    if not isinstance(owner, Mapping) or owner.get("kind") != kind:
        raise CommandAcceptanceError("input native envelope kind differs")
    identity = owner.get("id")
    if not isinstance(identity, str) or re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", identity) is None:
        raise CommandAcceptanceError("input native envelope identity is invalid")
    state = owner.get("state")
    if not isinstance(state, Mapping):
        raise CommandAcceptanceError("input native envelope state is missing")
    if "campaign_id" in owner:
        _input_id(owner["campaign_id"])
    if set(owner) - {"kind", "id", "state", "revision", "campaign_id", "interaction_id", "intent_plan_id", "message_id"} - set(state):
        raise CommandAcceptanceError("input native envelope has an undeclared private/authority field")
    for field, value in state.items():
        if field in owner and canonical_json(owner[field]) != canonical_json(value):
            raise CommandAcceptanceError("input flattened alias differs from native state")
    identity_field = {
        "runtime.interaction": "interaction_id", "runtime.message": "message_id",
        "runtime.intent_plan": "intent_plan_id",
    }.get(kind)
    if identity_field in owner and owner[identity_field] != identity:
        raise CommandAcceptanceError("input flattened identity differs from native envelope")
    if identity_field in state and state[identity_field] != identity:
        raise CommandAcceptanceError("input state identity differs from native envelope")
    if kind == "runtime.interaction":
        for field in ("intent_plan_id", "message_id"):
            if field in owner and field not in state:
                raise CommandAcceptanceError("input flattened alias has no lawful native phase field")
    return state


def _input_closed(value: object, required: set[str], optional: set[str] | None = None) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not required.issubset(value) or set(value) - required - (optional or set()):
        raise CommandAcceptanceError("input object has missing or forbidden fields")
    if any(item is None for item in value.values()):
        raise CommandAcceptanceError("input optional fields must be absent, not null")
    return value


def _input_wire(name: str, value: object) -> None:
    try:
        validate_contract(name, value)
    except StructuralContractError as exc:
        raise CommandAcceptanceError(f"input {name} shape is invalid: {exc}") from exc


def _input_text(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise CommandAcceptanceError("input field must be nonempty text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise CommandAcceptanceError("input text has invalid Unicode") from exc
    return value


def _input_id(value: object) -> str:
    text = _input_text(value)
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", text) is None:
        raise CommandAcceptanceError("input field must be a native ID")
    return text


def _input_integer(value: object, minimum: int = 1, exact: int | None = None) -> int:
    if type(value) is not int or value < minimum or exact is not None and value != exact:
        raise CommandAcceptanceError("input generation/revision is unsupported")
    return value


def _input_digest(value: object) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise CommandAcceptanceError("input content digest is malformed")
    return value


def _input_campaign_projection(owner: Mapping[str, object], campaign_id: str) -> None:
    if "campaign_id" in owner and _input_id(owner["campaign_id"]) != _input_id(campaign_id):
        raise CommandAcceptanceError("input envelope campaign projection differs from selected campaign")


def validate_input_resolution(
    *, resolution_id: str, resolution: Mapping[str, object],
) -> Mapping[str, object]:
    """Validate the native response owner before consuming its retained state."""
    _input_id(resolution_id)
    try:
        validate_loaded_identity("runtime.resolution", (resolution_id,), resolution)
    except NativeStorageError as exc:
        raise CommandAcceptanceError("input Resolution native identity differs from route") from exc
    state = resolution.get("state", resolution)
    if not isinstance(state, Mapping):
        raise CommandAcceptanceError("input Resolution state is malformed")
    _input_integer(state.get("schema_version"), exact=1)
    for carrier in (resolution, state):
        if "resolution_id" in carrier and _input_id(carrier["resolution_id"]) != resolution_id:
            raise CommandAcceptanceError("input Resolution identity projection differs")
    for field, value in state.items():
        if field in resolution and canonical_json(resolution[field]) != canonical_json(value):
            raise CommandAcceptanceError("input Resolution flattened projection differs from state")
    return state


def validate_input_interaction(*, campaign_id: str, interaction: Mapping[str, object]) -> Mapping[str, object]:
    """Validate the own-I variant without claiming I's historical authority.

    Root/promise admission can validate I and route its dependencies; full source
    closure additionally requires exact M/P/segment reads via validate_input_closure.
    """
    state = input_native_state(interaction, "runtime.interaction")
    _input_wire("runtime-interaction-state", state)
    _input_closed(state, {"schema_version", "campaign_id", "session_id", "input_message_id",
                          "input_kind", "accepted_input_basis"},
                  {"player_id", "intent_plan_id", "response_message_id", "response_target",
                   "response_selection", "planning_phase", "accepted_resume_ref", "details",
                   "host_invocation_ref", "authenticated_principal_ref"})
    _input_integer(state["schema_version"], exact=1)
    if state["campaign_id"] != _input_id(campaign_id):
        raise CommandAcceptanceError("input belongs to another campaign")
    for field in ("session_id", "input_message_id", "intent_plan_id", "response_message_id", "player_id"):
        if field in state:
            _input_id(state[field])
    basis = _input_closed(state["accepted_input_basis"], {
        "basis_generation", "repository_identity", "adapter_profile_id", "adapter_profile_generation",
        "accepted_exchange_key", "host_invocation_ref", "principal", "representation", "authority_at_acceptance",
    })
    for field in ("basis_generation", "adapter_profile_generation"):
        _input_integer(basis[field], exact=1)
    for field in ("repository_identity", "adapter_profile_id", "accepted_exchange_key", "host_invocation_ref"):
        _input_text(basis[field])
    principal = _input_closed(basis["principal"], {"provider", "stable_account_id", "login_at_acceptance"})
    if principal["provider"] != "github":
        raise CommandAcceptanceError("input principal provider is unsupported")
    _input_text(principal["stable_account_id"])
    _input_text(principal["login_at_acceptance"])
    representation = _input_closed(basis["representation"], {"kind", "digest_generation", "content_digest"})
    if representation["kind"] != "accepted_text":
        raise CommandAcceptanceError("input representation is unsupported")
    _input_integer(representation["digest_generation"], exact=1)
    _input_digest(representation["content_digest"])
    authority = basis["authority_at_acceptance"]
    if not isinstance(authority, Mapping):
        raise CommandAcceptanceError("input authority shape is missing")
    if authority.get("kind") == "multiplayer":
        _input_closed(authority, {"kind", "player_id", "accepted_subject_ids", "campaign_authority_revision",
                                  "player_revision", "route_evidence_revision"})
        if state.get("player_id") != _input_id(authority["player_id"]):
            raise CommandAcceptanceError("input Player projection differs")
        _input_integer(authority["player_revision"], minimum=0)
        for field in ("campaign_authority_revision", "route_evidence_revision"):
            _input_text(authority[field])
    elif authority.get("kind") == "creator_singleplayer":
        _input_closed(authority, {"kind", "creator_history", "accepted_subject_ids"})
        if "player_id" in state:
            raise CommandAcceptanceError("creator input forbids Player")
        history = _input_closed(authority["creator_history"], {"author_login", "initialization_revision", "parent_revision"})
        for item in history.values():
            _input_text(item)
        if history["author_login"] != principal["login_at_acceptance"]:
            raise CommandAcceptanceError("creator historical login differs")
    else:
        raise CommandAcceptanceError("input authority variant is unsupported")
    subjects = authority["accepted_subject_ids"]
    if not isinstance(subjects, (list, tuple)):
        raise CommandAcceptanceError("input subjects must be an array")
    checked = [_input_id(item) for item in subjects]
    if checked != sorted(set(checked)):
        raise CommandAcceptanceError("input subjects must be sorted unique")
    if "host_invocation_ref" in state and state["host_invocation_ref"] != basis["host_invocation_ref"]:
        raise CommandAcceptanceError("input invocation alias differs")
    # Legacy free-form principal strings cannot express this closed principal.
    if "authenticated_principal_ref" in state:
        raise CommandAcceptanceError("legacy principal string is not an input basis projection")
    kind = state["input_kind"]
    if kind == "intent":
        if "intent_plan_id" not in state or set(state) & {"response_target", "response_selection", "planning_phase", "accepted_resume_ref"}:
            raise CommandAcceptanceError("intent phase requires P and forbids response fields")
    elif kind in {"response", "response_and_intent"}:
        target = _input_closed(state.get("response_target"), {"root_command_id", "resolution_id", "continuation_id",
            "continuation_generation", "offer_kind", "offer_id", "responder_id"})
        for field in ("root_command_id", "resolution_id", "continuation_id", "offer_id", "responder_id"):
            _input_id(target[field])
        _input_integer(target["continuation_generation"])
        if target["offer_kind"] == "choice":
            selection = _input_closed(state.get("response_selection"), {"kind", "option_id"})
            _input_id(selection["option_id"])
        elif target["offer_kind"] == "reaction":
            selection = _input_closed(state.get("response_selection"), {"kind", "activity_id"})
            _input_id(selection["activity_id"])
        else:
            raise CommandAcceptanceError("input offer kind is unsupported")
        if selection["kind"] != target["offer_kind"]:
            raise CommandAcceptanceError("input selection kind differs from target")
        if target["responder_id"] not in checked:
            raise CommandAcceptanceError("input historical subject set omits responder")
        if kind == "response":
            if set(state) & {"intent_plan_id", "planning_phase"}:
                raise CommandAcceptanceError("pure response forbids Plan/phase")
        else:
            phase = state.get("planning_phase")
            links = set(state) & {"intent_plan_id", "accepted_resume_ref"}
            expected = {"awaiting_response": set(), "ready_to_plan": {"accepted_resume_ref"},
                        "materialized": {"intent_plan_id", "accepted_resume_ref"}}
            if not isinstance(phase, str) or phase not in expected or links != expected[phase]:
                raise CommandAcceptanceError("mixed input phase links are incomplete or forbidden")
        if "accepted_resume_ref" in state:
            reference = _input_closed(state["accepted_resume_ref"], {"resolution_id", "segment_id"})
            for item in reference.values():
                _input_id(item)
            if reference["resolution_id"] != target["resolution_id"]:
                raise CommandAcceptanceError("input resume Resolution differs from target")
    else:
        raise CommandAcceptanceError("input kind is unsupported")
    if "details" in state and not isinstance(state["details"], Mapping):
        raise CommandAcceptanceError("input details must be an object")
    return state


def _validate_input_message(*, campaign_id: str, interaction: Mapping[str, object],
                            state: Mapping[str, object], message: Mapping[str, object]) -> Mapping[str, object]:
    """Validate I/M representation independently of later P/response progression."""
    message_state = input_native_state(message, "runtime.message")
    _input_campaign_projection(message, campaign_id)
    _input_wire("runtime-message-state", message_state)
    _input_closed(message_state, {"schema_version", "message_id", "interaction_id", "direction",
        "input_basis_generation", "representation_kind", "payload_state", "content_digest"},
        {"exact_text", "source_domain_ref", "semantic_event_refs"})
    for field in ("schema_version", "input_basis_generation"):
        _input_integer(message_state[field], exact=1)
    if (message["id"] != state["input_message_id"] or message_state["message_id"] != message["id"]
            or message_state["interaction_id"] != interaction["id"]):
        raise CommandAcceptanceError("input I/M reciprocal identity differs")
    if message_state["direction"] != "inbound" or message_state["representation_kind"] != "accepted_text":
        raise CommandAcceptanceError("input Message must be inbound accepted text")
    basis = state["accepted_input_basis"]
    digest = basis["representation"]["content_digest"]
    if _input_digest(message_state["content_digest"]) != digest:
        raise CommandAcceptanceError("input I/M content digest differs")
    payload_state = message_state["payload_state"]
    if payload_state == "message.exact_retained":
        text = _input_text(message_state.get("exact_text"))
        if sha256(text.encode("utf-8")) != digest:
            raise CommandAcceptanceError("input retained content digest differs")
    elif payload_state == "message.compacted":
        if "exact_text" in message_state:
            raise CommandAcceptanceError("input compacted content forbids exact_text")
    else:
        raise CommandAcceptanceError("input Message payload state is unsupported")
    for field in ("source_domain_ref",):
        if field in message_state:
            _input_id(message_state[field])
    if "semantic_event_refs" in message_state:
        refs = message_state["semantic_event_refs"]
        if not isinstance(refs, (tuple, list)) or len(refs) != len({_input_id(item) for item in refs}):
            raise CommandAcceptanceError("input semantic refs are malformed or duplicate")
    return message_state


def resume_input_fingerprint(*, interaction: Mapping[str, object], message: Mapping[str, object]) -> str:
    """Codec1 over fixed accepted response input, not an acceptance/consume proof.

    Phase, P/C/K and new outputs are deliberately excluded. The complete native
    I/M types and representation are checked before canonical serialization.
    """
    native = input_native_state(interaction, "runtime.interaction")
    state = validate_input_interaction(campaign_id=native.get("campaign_id"), interaction=interaction)
    if state["input_kind"] not in {"response", "response_and_intent"}:
        raise CommandAcceptanceError("resume fingerprint requires response input")
    _validate_input_message(campaign_id=state["campaign_id"], interaction=interaction, state=state, message=message)
    material = {"response_interaction_id": interaction["id"], "response_message_id": message["id"],
                "input_kind": state["input_kind"], "accepted_input_basis": _thaw(state["accepted_input_basis"]),
                "target": _thaw(state["response_target"]), "selection": _thaw(state["response_selection"])}
    try:
        return sha256(_ACCEPTED_RESUME_INPUT_DOMAIN + canonical_json(material))
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CommandAcceptanceError("resume input is not canonical JSON/UTF-8") from exc


def validate_input_closure(*, campaign_id: str, interaction: Mapping[str, object],
                           message: Mapping[str, object], plan: Mapping[str, object] | None,
                           accepted_response_segment: Mapping[str, object] | None) -> None:
    """Validate deterministic native source closure, never authenticated authority.

    A structurally matching retained marker is necessary, not proof of a native
    consume edge. Protected acceptance must separately establish native issuance.
    """
    state = validate_input_interaction(campaign_id=campaign_id, interaction=interaction)
    message_state = _validate_input_message(campaign_id=campaign_id, interaction=interaction,
                                           state=state, message=message)
    payload_state = message_state["payload_state"]
    if payload_state == "message.compacted":
        # normalized_semantics is an open object, not an admitted sufficient
        # content representation. No wrapper/key/value heuristic can certify it.
        # Until an actual content-bearing natural survivor is observed through
        # its owner, this input reader must retain exact M rather than guess.
        raise CommandAcceptanceError("compacted input requires admitted content-bearing survivor evidence")
    reference = state.get("accepted_resume_ref")
    if reference is None:
        if accepted_response_segment is not None:
            raise CommandAcceptanceError("input has no accepted response segment locator")
    else:
        segment = accepted_response_segment
        if not isinstance(segment, Mapping) or segment.get("segment_id") != reference["segment_id"]:
            raise CommandAcceptanceError("input exact accepted response segment is missing")
        _input_wire("execution-segment", segment)
        sequence = _input_integer(segment.get("segment_sequence"))
        if reference["segment_id"] != f'{reference["resolution_id"]}:segment:{sequence}' or segment.get("commit_state") != "committed":
            raise CommandAcceptanceError("input response segment identity/commit differs")
        marker = _input_closed(segment.get("accepted_resume_input"), {"schema_version", "resume_fingerprint_generation",
            "resume_fingerprint", "response_interaction_id", "response_message_id", "target", "selection"})
        for field in ("schema_version", "resume_fingerprint_generation"):
            _input_integer(marker[field], exact=1)
        for field in ("response_interaction_id", "response_message_id"):
            _input_id(marker[field])
        # Reuse the input owner's complete closed types before exact comparison;
        # Python mapping equality alone equates True/1 and 1.0/1.
        _input_wire("https://hedgelion.invalid/schemas/runtime-interaction-state.schema.json#/$defs/target", marker["target"])
        _input_wire("https://hedgelion.invalid/schemas/runtime-interaction-state.schema.json#/$defs/selection", marker["selection"])
        _input_integer(marker["target"]["continuation_generation"])
        if (marker["response_interaction_id"] != interaction["id"] or marker["response_message_id"] != message["id"]
                or canonical_json(marker["target"]) != canonical_json(state["response_target"])
                or canonical_json(marker["selection"]) != canonical_json(state["response_selection"])):
            raise CommandAcceptanceError("input response marker source links differ")
        if _input_digest(marker["resume_fingerprint"]) != resume_input_fingerprint(interaction=interaction, message=message):
            raise CommandAcceptanceError("input response marker fingerprint differs")
    if "intent_plan_id" not in state:
        if plan is not None:
            raise CommandAcceptanceError("input phase forbids Plan")
        return
    if plan is None:
        raise CommandAcceptanceError("input required Plan is missing")
    _input_campaign_projection(plan, campaign_id)
    plan_state = validate_input_plan(plan)
    _input_closed(plan_state, {"schema_version", "interaction_id", "clauses"}, {"details"})
    _input_integer(plan_state["schema_version"], exact=1)
    if plan["id"] != state["intent_plan_id"] or plan_state["interaction_id"] != interaction["id"]:
        raise CommandAcceptanceError("input Plan reciprocity differs")
    clauses = plan_state["clauses"]
    if not isinstance(clauses, (tuple, list)) or not clauses:
        raise CommandAcceptanceError("input Plan clauses are missing")
    ids: set[str] = set()
    for order, clause in enumerate(clauses, 1):
        if not isinstance(clause, Mapping):
            raise CommandAcceptanceError("input clause must be an object")
        _input_integer(clause.get("schema_version"), exact=1)
        clause_id = _input_id(clause.get("clause_id"))
        if clause_id in ids or _input_integer(clause.get("order")) != order:
            raise CommandAcceptanceError("input clause IDs/order are duplicate or noncanonical")
        if "guard" in clause:
            guard = clause["guard"]
            if not isinstance(guard, Mapping) or guard.get("prior_clause_id") not in ids:
                raise CommandAcceptanceError("input clause guard must name an earlier clause")
        ids.add(clause_id)
        if "command_id" in clause:
            _input_id(clause["command_id"])
        if state["input_kind"] == "response_and_intent" and order == 1:
            _input_closed(clause, {"schema_version", "clause_kind", "clause_id", "order", "mapping_outcome",
                                    "execution_state", "accepted_resume_ref"})
            if (clause["clause_kind"] != "solicited_response" or clause_id != "clause.response"
                    or clause["mapping_outcome"] != "exact" or clause["execution_state"] != "intent.executed"
                    or canonical_json(clause["accepted_resume_ref"]) != canonical_json(reference)):
                raise CommandAcceptanceError("input mixed response clause differs")
        else:
            if clause.get("clause_kind") != "intent" or "accepted_resume_ref" in clause:
                raise CommandAcceptanceError("input ordinary clause must be intent")
            if state["input_kind"] == "response_and_intent" and clause_id != f"clause.intent.{order - 1}":
                raise CommandAcceptanceError("input mixed extra clause ID differs")
            if state["input_kind"] == "response_and_intent" and not (
                clause.get("normalized_semantics") or clause.get("material_exact_text_refs")
            ):
                raise CommandAcceptanceError("input mixed extra clause has no retained material meaning")
    if state["input_kind"] == "response_and_intent" and len(clauses) < 2:
        raise CommandAcceptanceError("input mixed Plan needs real extra meaning")


def validate_input_plan(plan: Mapping[str, object]) -> Mapping[str, object]:
    """Validate complete owner-local units before a Plan becomes a routing root."""
    state = input_native_state(plan, "runtime.intent_plan")
    _input_wire("runtime-intent-plan-state", state)
    _input_id(state["interaction_id"])
    seen: set[str] = set()
    for order, clause in enumerate(state["clauses"], 1):
        identity = _input_id(clause["clause_id"])
        if identity in seen or _input_integer(clause["order"]) != order:
            raise CommandAcceptanceError("input Plan has duplicate/noncanonical units")
        if "guard" in clause and clause["guard"]["prior_clause_id"] not in seen:
            raise CommandAcceptanceError("input Plan guard does not name an earlier unit")
        if "command_id" in clause:
            _input_id(clause["command_id"])
            if clause["mapping_outcome"] not in {"exact", "composed"} or (
                "dependency_kind" in clause and clause["execution_state"] == "intent.pending"
            ):
                raise CommandAcceptanceError("input nonexecutable/held clause cannot own a command")
        seen.add(identity)
    return state


def accepted_input_origin(
    *, campaign_id: str, interaction: Mapping[str, object],
    message: Mapping[str, object], plan: Mapping[str, object], clause_id: str,
    accepted_response_segment: Mapping[str, object] | None = None,
) -> Mapping[str, object]:
    """Derive historical provenance from exact native sources, not a shadow DTO.

    This pure validator does not issue authentication or current write authority.
    """
    validate_input_closure(
        campaign_id=campaign_id, interaction=interaction, message=message,
        plan=plan, accepted_response_segment=accepted_response_segment,
    )
    state = input_native_state(interaction, "runtime.interaction")
    if state["input_kind"] not in {"intent", "response_and_intent"}:
        raise CommandAcceptanceError("pure response cannot anchor an ordinary command")
    if state["input_kind"] == "response_and_intent" and state["planning_phase"] != "materialized":
        raise CommandAcceptanceError("mixed command requires materialized native input")
    clauses = input_native_state(plan, "runtime.intent_plan")["clauses"]
    matches = [clause for clause in clauses if clause["clause_id"] == clause_id]
    if len(matches) != 1 or matches[0]["clause_kind"] != "intent":
        raise CommandAcceptanceError("command requires exactly one genuine intent clause")
    clause = matches[0]
    if clause.get("collaboration_semantic_class") in {"OOC_COORDINATION", "DIEGETIC_COMMUNICATION", "CONTROL_SIGNAL"}:
        raise CommandAcceptanceError("nonexecuting material unit cannot anchor a command")
    if clause["mapping_outcome"] not in {"exact", "composed"} or (
        "dependency_kind" in clause and clause["execution_state"] == "intent.pending"
    ):
        raise CommandAcceptanceError("nonexecutable or held clause cannot anchor a command")
    origin = {
        "interaction_id": interaction["id"], "intent_plan_id": plan["id"],
        "clause_id": clause_id, "input_kind": state["input_kind"],
        "accepted_input_basis": _thaw(state["accepted_input_basis"]),
    }
    if state["input_kind"] == "response_and_intent":
        origin["accepted_resume_ref"] = _thaw(state["accepted_resume_ref"])
    return origin


def command_input_fingerprint(command: Mapping[str, object], *, origin: Mapping[str, object]) -> str:
    """Codec3 over the complete validated variant and native-source origin.

    This exact-identity calculation is not an issuer. Native origin/current
    authority must be validated independently even if a plain hash is recomputed.
    """
    kind = command.get("command_kind")
    variants = {
        "action": {"action_request", "interpreter_result", "interpreter_result_fingerprint_generation",
            "interpreter_result_fingerprint", "candidate_binding"},
        "transition": {"transition_request", "transition_binding"},
    }
    if not isinstance(kind, str) or kind not in variants:
        raise CommandAcceptanceError("command kind is unsupported")
    forbidden = variants["transition" if kind == "action" else "action"]
    if set(command) & forbidden:
        raise CommandAcceptanceError("command has fields forbidden for its variant")
    if kind == "transition" and "root_resolution_id" in command:
        raise CommandAcceptanceError("direct command cannot manufacture a root Resolution")
    if kind == "action" and set(command) & {"direct_transition_segments", "direct_transition_receipt"}:
        raise CommandAcceptanceError("action cannot own direct segments/receipt")
    required = {"command_kind", "catalog_context_fingerprint", "catalog_context", "invocation_facts"} | variants[kind]
    if not required <= set(command):
        raise CommandAcceptanceError("command is missing immutable input material")
    origin_fields = {"interaction_id", "intent_plan_id", "clause_id", "input_kind", "accepted_input_basis"}
    if origin.get("input_kind") == "response_and_intent":
        origin_fields.add("accepted_resume_ref")
    elif origin.get("input_kind") != "intent":
        raise CommandAcceptanceError("command origin must be intent or materialized mixed input")
    _input_closed(origin, origin_fields)
    for field in ("interaction_id", "intent_plan_id", "clause_id"):
        _input_id(origin[field])
        if field in command and command[field] != origin[field]:
            raise CommandAcceptanceError("command identity differs from native input origin")
    material = {key: _thaw(command[key]) for key in required}
    material["accepted_input_origin"] = _thaw(origin)
    try:
        return sha256(_RUNTIME_COMMAND_INPUT_DOMAIN + canonical_json(material))
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CommandAcceptanceError("command input is not canonical JSON/UTF-8") from exc


def input_source_owner_refs(
    command: Mapping[str, object], observation: CurrentOwnerObservation, *,
    authority_sources: Mapping[str, object],
) -> frozenset[NativeOwnerRef]:
    """Derive infrastructure refs, without granting any MechanicalContext read.

    Each independent consumer recomputes this set from native I and the verified
    current account nomination; no asserted union or session-record lease is an
    authority source. Effects/Assets remain their own complete membership join.
    """
    interaction_ref = NativeOwnerRef("runtime.interaction", (command["interaction_id"],))
    read = observation.require(interaction_ref)
    if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
        raise CommandAcceptanceError("required native input source is unavailable")
    state = input_native_state(read.payload, "runtime.interaction")
    refs = {interaction_ref, NativeOwnerRef("runtime.message", (state["input_message_id"],)),
        NativeOwnerRef("runtime.intent_plan", (command["intent_plan_id"],))}
    reference = state.get("accepted_resume_ref")
    if isinstance(reference, Mapping):
        refs.add(NativeOwnerRef("runtime.resolution", (reference["resolution_id"],)))
    if authority_sources["mode"] == "multiplayer":
        for entry in authority_sources["route"]["entries"]:
            refs.update(NativeOwnerRef("world.player", (identity,)) for identity in entry["candidate_player_ids"])
    if command.get("command_kind", "action") == "transition":
        refs.update(direct_input_contract(command)[1])
    else:
        request = _require_mapping(command.get("action_request"), "action request")
        refs.add(NativeOwnerRef("world.actor", (_input_id(request.get("actor_id")),)))
    return frozenset(refs)


def direct_input_contract(command: Mapping[str, object], context: BoundCatalogContext | None = None
                          ) -> tuple[str, frozenset[NativeOwnerRef]]:
    """Resolve a finite native profile from the installed inventory, never an Activity.

    The source-owned payload schema and profile must agree exactly. These reads
    prepare a native edge; they neither apply a mutation nor certify its result.
    """
    from .catalog_runtime import load_activity_compiler_contract_source

    try:
        source = load_activity_compiler_contract_source()
        if context is not None and (not context._is_admitted()
                or not source.inventory_matches(_thaw(context.basis["engine_contract_inventory"]))):
            raise CommandAcceptanceError("direct profile inventory differs from admitted context")
        members = source.compiler_contracts["families"]["schema_contract"]
        request = _require_exact_fields(command.get("transition_request"),
            frozenset({"transition_kind", "payload"}), "transition request")
        binding = _require_exact_fields(command.get("transition_binding"),
            frozenset({"profile_id", "profile_generation", "payload_schema_id", "payload_schema_version"}),
            "transition binding")
        for field in ("profile_generation", "payload_schema_version"):
            _input_integer(binding[field], exact=1)
        payload = _require_mapping(request["payload"], "native transition payload")
        matches = [profile for profile in members["gameplay_spine_seed"]["transition_profiles"]
            if profile["profile_id"] == binding["profile_id"]]
        if len(matches) != 1:
            raise CommandAcceptanceError("direct native profile is unavailable or ambiguous")
        profile = matches[0]
        if (profile["transition_kind"] != request["transition_kind"]
                or payload.get("profile_id") != profile["profile_id"]
                or payload.get("transition_kind") != request["transition_kind"]
                or binding["payload_schema_id"] != profile["request_schema"]):
            raise CommandAcceptanceError("direct payload/kind/schema differs from admitted native profile")
        schema = members["gameplay_spine_transition_request_schema"]
        schema_id, fragment = profile["request_schema"].split("#", 1)
        if schema_id != schema["$id"] or not fragment.startswith("/$defs/"):
            raise CommandAcceptanceError("native payload schema is not an admitted inventory member")
        # The installed structural validator consumes this same exact DEV schema.
        _input_wire(profile["request_schema"], payload)
        refs: set[NativeOwnerRef] = set()
        if profile["profile_id"] in {"location_change.procedure_movement", "location_change.outside_procedure"}:
            subject = _input_id(payload["actor_id"])
            refs.update({NativeOwnerRef("world.actor", (subject,)),
                NativeOwnerRef("world.location", (_input_id(payload["destination_location_id"]),))})
            if "procedure_id" in payload:
                refs.add(NativeOwnerRef("runtime.procedure", (_input_id(payload["procedure_id"]),)))
        elif profile["profile_id"] == "asset.equip":
            subject = _input_id(payload["owner_actor_id"])
            refs.update({NativeOwnerRef("world.actor", (subject,)),
                NativeOwnerRef("world.asset", (_input_id(payload["asset_id"]),))})
        elif profile["profile_id"] == "asset.transfer":
            # A non-Actor placement has no voluntary controller mapping in this
            # finite profile. Do not infer an actor from an arbitrary container.
            subject = _input_id(payload["from_placement"].get("owner_actor_id"))
            refs.update({NativeOwnerRef("world.actor", (subject,)),
                NativeOwnerRef("world.asset", (_input_id(payload["asset_id"]),))})
            for placement in (payload["from_placement"], payload["to_placement"]):
                for field, family in (("owner_actor_id", "world.actor"),
                                      ("container_asset_id", "world.asset"), ("location_id", "world.location")):
                    if field in placement:
                        refs.add(NativeOwnerRef(family, (_input_id(placement[field]),)))
        else:
            raise CommandAcceptanceError("profile has no admitted direct transition/control mapping")
        return subject, frozenset(refs)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, CommandAcceptanceError):
            raise
        raise CommandAcceptanceError("admitted native transition contract is unavailable") from exc


def validate_direct_input_sources(command: Mapping[str, object], observation: CurrentOwnerObservation) -> str:
    """Check selected native identities/revisions without accepting native effects."""
    subject, refs = direct_input_contract(command)
    payload = command["transition_request"]["payload"]
    revision_fields = {"world.actor": "actor_revision", "world.asset": "asset_revision",
        "runtime.procedure": "procedure_revision", "world.location": "destination_location_revision"}
    for ref in refs:
        read = observation.require(ref)
        if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
            raise CommandAcceptanceError("direct native source is unavailable")
        native = read.payload
        if native.get("kind") != ref.family_key or native.get("id") != ref.identity[0]:
            raise CommandAcceptanceError("direct native source envelope differs")
        field = revision_fields[ref.family_key]
        identity_field = {"world.actor": "actor_id", "world.asset": "asset_id",
            "runtime.procedure": "procedure_id", "world.location": "destination_location_id"}[ref.family_key]
        if payload.get(identity_field) == ref.identity[0] and field in payload:
            revision = native.get("state_revision", native.get("revision"))
            _input_integer(revision, minimum=0)
            if revision != payload[field]:
                raise CommandAcceptanceError("REVALIDATION_REQUIRED: direct native revision differs")
        if ref.family_key == "world.asset" and ref.identity[0] == payload.get("asset_id"):
            state = _require_mapping(native.get("state"), "native Asset state")
            if state.get("owner_actor_id") != subject:
                raise CommandAcceptanceError("direct Asset source has no exact controlled owner")
    return subject


def execution_identity(
    command: Mapping[str, object], *, execution_owner_kind: str,
    execution_owner_id: str, segment: Mapping[str, object],
) -> Mapping[str, object]:
    """Project an actual K/R owner edge without inventing a Resolution or event.

    Native R/root/child reciprocity and eventless profile eligibility are checked
    by the owning acceptance boundary, never inferred from this projection/hash.
    """
    command_id = _input_id(command.get("command_id"))
    if type(command.get("input_fingerprint_generation")) is not int or command["input_fingerprint_generation"] != 3:
        raise CommandAcceptanceError("execution identity requires command input generation3")
    fingerprint = _input_digest(command.get("input_fingerprint"))
    owner_id = _input_id(execution_owner_id)
    kind = command.get("command_kind")
    if kind == "transition":
        if execution_owner_kind != "runtime.command" or owner_id != command_id or "root_resolution_id" in command:
            raise CommandAcceptanceError("direct execution owner must be the actual command")
        if "accepted_resume_input" in segment:
            raise CommandAcceptanceError("direct command cannot own a solicited response marker")
    elif kind == "action":
        _input_id(command.get("root_resolution_id"))
        if execution_owner_kind != "runtime.resolution":
            raise CommandAcceptanceError("action execution owner must be a real Resolution")
    else:
        raise CommandAcceptanceError("execution command kind is unsupported")
    sequence = _input_integer(segment.get("segment_sequence"))
    segment_id = _input_id(segment.get("segment_id"))
    if segment_id != f"{owner_id}:segment:{sequence}":
        raise CommandAcceptanceError("execution segment identity differs from native owner")
    events = segment.get("event_ids")
    if not isinstance(events, (list, tuple)):
        raise CommandAcceptanceError("execution event_ids must be an exact native set")
    event_ids = [_input_id(event_id) for event_id in events]
    if len(event_ids) != len(set(event_ids)):
        raise CommandAcceptanceError("execution event_ids are duplicate")
    return {"identity_generation": 1, "command_id": command_id,
        "input_fingerprint_generation": 3, "input_fingerprint": fingerprint,
        "execution_owner_kind": execution_owner_kind, "execution_owner_id": owner_id,
        "segment_id": segment_id, "event_ids": event_ids}


def _validate_retained_segments(*, owner_kind: str, owner_id: str,
        state: Mapping[str, object], segments: object) -> dict[str, Mapping[str, object]]:
    """One relational segment/frontier validator for native reads and receipts."""
    if not isinstance(segments, (list, tuple)):
        raise CommandAcceptanceError("execution owner segments are malformed")
    by_id: dict[str, Mapping[str, object]] = {}
    previous_sequence = 0
    for embedded in segments:
        _input_wire("execution-segment", embedded)
        if "accepted_resume_input" in embedded:
            if owner_kind != "runtime.resolution":
                raise CommandAcceptanceError("only a real Resolution can retain a response marker")
            _validate_resume_marker_shape(embedded)
            if embedded["accepted_resume_input"]["target"]["root_command_id"] != state["root_command_id"]:
                raise CommandAcceptanceError("response marker root differs from native Resolution")
        _input_integer(embedded.get("schema_version"), exact=1)
        sequence = _input_integer(embedded.get("segment_sequence"))
        expected_id = f"{owner_id}:segment:{sequence}"
        if (sequence <= previous_sequence or embedded["segment_id"] != expected_id
                or owner_kind == "runtime.command" and sequence != previous_sequence + 1):
            raise CommandAcceptanceError("native owner segment identity/order differs")
        previous_sequence = sequence
        previous_ordinal = 0
        for event_id in embedded["event_ids"]:
            prefix = expected_id + ":event:"
            suffix = event_id.removeprefix(prefix)
            if (not event_id.startswith(prefix) or not suffix.isascii() or not suffix.isdecimal()
                    or str(int(suffix)) != suffix or int(suffix) <= previous_ordinal):
                raise CommandAcceptanceError("native segment event identity/order differs")
            previous_ordinal = int(suffix)
        by_id[expected_id] = embedded
    if owner_kind == "runtime.resolution" and state["next_segment_sequence"] <= previous_sequence:
        raise CommandAcceptanceError("Resolution next segment does not follow its committed closure")
    return by_id


def validate_retained_resolution(*, resolution_id: str,
        resolution: Mapping[str, object]) -> Mapping[str, object]:
    """Complete native R grammar and intrinsic relations, never native issue."""
    native = validate_input_resolution(resolution_id=resolution_id, resolution=resolution)
    state = {key: value for key, value in native.items()
             if key not in {"kind", "id", "campaign_id", "revision", "state_revision", "resolution_id"}}
    _input_wire("runtime-resolution-state", state)
    _ordering_resolution_schema(state)
    _validate_retained_segments(owner_kind="runtime.resolution", owner_id=resolution_id,
        state=state, segments=state["segments"])
    if state["status"] in {"AWAITING_CHOICE", "AWAITING_REACTION"} and "continuation_id" not in state:
        raise CommandAcceptanceError("suspended native Resolution requires its current Continuation")
    declared = {child["child_resolution_id"] for segment in state["segments"]
                for child in segment["pending_child_invocations"] if "child_resolution_id" in child}
    if not declared <= set(state["child_resolution_ids"]):
        raise CommandAcceptanceError("native Resolution omits a declared child forward link")
    return state


def _validate_execution_owner_edge(*, owner_kind: str, owner_id: str,
        owner: Mapping[str, object], segment: Mapping[str, object], receipt: Mapping[str, object]) -> Mapping[str, object]:
    """Validate one retained native edge and its cumulative receipt membership."""
    _input_wire("execution-segment", segment)
    _input_integer(segment.get("schema_version"), exact=1)
    _input_wire("resolution-receipt", receipt)
    if owner_kind == "runtime.resolution":
        if "kind" in owner or "state" in owner or "id" in owner:
            state = validate_retained_resolution(resolution_id=owner_id, resolution=owner)
        else:
            state = validate_retained_resolution(resolution_id=owner_id,
                resolution={"kind": owner_kind, "id": owner_id, "state": owner})
        segments = state["segments"]
    elif owner_kind == "runtime.command":
        _input_wire("runtime-command-state", owner)
        if owner.get("command_id") != owner_id or owner.get("command_kind") != "transition":
            raise CommandAcceptanceError("direct edge has a foreign native command owner")
        state = owner
        segments = owner.get("direct_transition_segments", ())
        if canonical_json(_thaw(owner.get("direct_transition_receipt"))) != canonical_json(_thaw(receipt)):
            raise CommandAcceptanceError("direct receipt differs from its actual native command")
    else:
        raise CommandAcceptanceError("execution owner kind is unsupported")
    if not segments:
        raise CommandAcceptanceError("execution owner has no committed segments")
    by_id = _validate_retained_segments(owner_kind=owner_kind, owner_id=owner_id, state=state, segments=segments)
    selected = by_id.get(segment["segment_id"])
    if selected is None or canonical_json(_thaw(selected)) != canonical_json(_thaw(segment)):
        raise CommandAcceptanceError("selected segment differs from its actual native owner embedding")
    refs = receipt["segment_refs"]
    if (receipt["execution_owner_id"] != owner_id or segment["segment_id"] not in refs
            or any(ref not in by_id for ref in refs)
            or list(refs) != [ref for ref in by_id if ref in refs]):
        raise CommandAcceptanceError("native receipt owner/segment closure differs")
    covered = [by_id[ref] for ref in refs]
    expected_events = [event_id for item in covered for event_id in item["event_ids"]]
    if (list(receipt["event_ids"]) != expected_events
            or receipt["status"] != covered[-1]["resulting_execution_state"]
            or canonical_json(_thaw(receipt["exports"])) != canonical_json(_thaw(covered[-1]["receipt_exports"]))):
        raise CommandAcceptanceError("native receipt result/event/export evidence differs")
    child_refs = {ref for item in covered for child in item["pending_child_invocations"]
        for ref in (child["firing_key"], child.get("child_resolution_id")) if ref is not None}
    if not set(receipt["pending_child_refs"]) <= child_refs:
        raise CommandAcceptanceError("native receipt has a foreign pending child")
    return state


def _validate_action_resolution_binding(command: Mapping[str, object], owner_id: str,
                                        resolution: Mapping[str, object]) -> None:
    if resolution.get("root_command_id") != command["command_id"]:
        raise CommandAcceptanceError("execution Resolution has a foreign root command")
    if owner_id == command.get("root_resolution_id"):
        if resolution.get("initiating_command_id") != command["command_id"]:
            raise CommandAcceptanceError("root Resolution lacks reciprocal command identity")
        request = command["action_request"]
        for field, default in (("activity_id", None), ("actor_id", None), ("source_id", None),
                               ("target_ids", []), ("parameter_bindings", {})):
            if canonical_json(_thaw(resolution.get(field, default))) != canonical_json(_thaw(request.get(field, default))):
                raise CommandAcceptanceError("root Resolution differs from its accepted action request")
    else:
        matches = [child for child in command["pending_child_invocations"] if child.get("child_resolution_id") == owner_id]
        if (len(matches) != 1 or "initiating_command_id" in resolution
                or matches[0]["firing_key"] != resolution.get("causal_invocation_key")
                or matches[0]["activity_id"] != resolution["activity_id"]
                or matches[0]["root_command_id"] != command["command_id"]
                or "procedure_id" in matches[0] and matches[0]["procedure_id"] != resolution.get("procedure_id")):
            raise CommandAcceptanceError("child Resolution lacks its exact native command invocation mapping")
    lock = command["catalog_context"]["basis"]["ruleset_lock"]
    if (resolution["catalog_context_fingerprint_generation"] != command["catalog_context"]["catalog_context_fingerprint_generation"]
            or resolution["catalog_context_fingerprint"] != command["catalog_context_fingerprint"]
            or resolution["ruleset_set_digest_generation"] != lock["ruleset_set_digest_generation"]
            or resolution["ruleset_set_sha256"] != lock["ruleset_set_sha256"]
            or owner_id == command["root_resolution_id"] and resolution["invocation_facts"] != command["invocation_facts"]):
        raise CommandAcceptanceError("Resolution accepted catalog/fact basis differs")


def execution_result_identity(command: Mapping[str, object], result: Mapping[str, object]) -> Mapping[str, object]:
    """Check the serialized native edge's reciprocal evidence and project it once."""
    _input_wire("runtime-command-state", command)
    _input_integer(command.get("schema_version"), exact=4)
    _input_integer(command.get("input_fingerprint_generation"), exact=3)
    kind = command.get("command_kind")
    owner_kind = "runtime.command" if kind == "transition" else "runtime.resolution"
    owner_id = _input_id(result.get("execution_owner_id"))
    segment = _require_mapping(result.get("segment"), "execution segment")
    receipt = _require_mapping(result.get("receipt"), "execution receipt")
    identity = execution_identity(command, execution_owner_kind=owner_kind,
        execution_owner_id=owner_id, segment=segment)
    if (result.get("accepted_command_id") != identity["command_id"]
            or result.get("accepted_input_fingerprint") != identity["input_fingerprint"]):
        raise CommandAcceptanceError("execution differs from accepted command identity")
    if kind == "action":
        if result.get("resolution_id") != owner_id:
            raise CommandAcceptanceError("action result has no actual Resolution identity")
        resolution = _validate_execution_owner_edge(owner_kind=owner_kind, owner_id=owner_id,
            owner=_require_mapping(result.get("resolution"), "execution Resolution"), segment=segment, receipt=receipt)
        _validate_action_resolution_binding(command, owner_id, resolution)
        if result.get("status") != resolution["status"]:
            raise CommandAcceptanceError("execution result status differs from its current Resolution")
    elif kind == "transition":
        if "resolution_id" in result or "resolution" in result:
            raise CommandAcceptanceError("direct result forbids a synthetic Resolution identity")
        _validate_execution_owner_edge(owner_kind=owner_kind, owner_id=owner_id,
            owner=command, segment=segment, receipt=receipt)
        if result.get("status") != receipt["status"]:
            raise CommandAcceptanceError("direct result status differs from its native receipt")
    receipt_events = receipt.get("event_ids", ())
    if (receipt.get("execution_owner_id") != owner_id
            or segment["segment_id"] not in receipt.get("segment_refs", ())
            or not isinstance(receipt_events, (list, tuple))
            or len(set(receipt_events)) != len(receipt_events)
            or not set(identity["event_ids"]) <= set(receipt_events)):
        raise CommandAcceptanceError("native receipt differs from execution owner/segment/events")
    if "execution_identity" in result and canonical_json(_thaw(result["execution_identity"])) != canonical_json(identity):
        raise CommandAcceptanceError("execution identity projection differs from native edge")
    event_ids = identity["event_ids"]
    events = result["events"] if "events" in result else ([result["event"]] if "event" in result else [])
    if not isinstance(events, (list, tuple)) or len(events) != len(event_ids):
        raise CommandAcceptanceError("execution event evidence differs from native segment")
    # Every supplied carrier participates. Exact canonical equality also rejects
    # Python-equal aliases such as bool/int or int/float before schema validation.
    # The existing loop then validates both equal carriers as the same sole event.
    if "event" in result and (len(events) != 1 or not isinstance(result["event"], Mapping)
            or canonical_json(_thaw(result["event"])) != canonical_json(_thaw(events[0]))):
        raise CommandAcceptanceError("singular event differs from the sole plural event")
    previous_ordinal = 0
    for event_id, event in zip(event_ids, events):
        if not isinstance(event, Mapping):
            raise CommandAcceptanceError("native event evidence is not an object")
        if "event_id" in event and event["event_id"] != event_id:
            raise CommandAcceptanceError("native event alias differs from its exact identity")
        event_state = event.get("state", event)
        if not isinstance(event_state, Mapping):
            raise CommandAcceptanceError("native event state is not an object")
        if "kind" in event or "id" in event:
            try:
                validate_loaded_identity("runtime.mechanical_event", (event_id,), event)
            except NativeStorageError as exc:
                raise CommandAcceptanceError("native event envelope differs from its exact identity") from exc
        if event_state is not event:
            for field in event_state:
                if field in event and canonical_json(_thaw(event[field])) != canonical_json(_thaw(event_state[field])):
                    raise CommandAcceptanceError("native event flattened alias differs")
        excluded = {"event_id"} if event_state is not event else {"event_id", "kind", "id", "campaign_id", "revision", "state_revision"}
        _input_wire("runtime-mechanical-event-state", {key: value for key, value in event_state.items() if key not in excluded})
        event = event_state
        if (not isinstance(event, Mapping)
                or type(event.get("event_ordinal")) is not int
                or event["event_ordinal"] <= previous_ordinal
                or event_id != f'{segment["segment_id"]}:event:{event["event_ordinal"]}'
                or event.get("segment_id") != segment["segment_id"]
                or event.get("root_command_id") != identity["command_id"] or event.get("causal_ref") != owner_id
                or event.get("event_id", event_id) != event_id):
            raise CommandAcceptanceError("native event identity/causal linkage differs")
        previous_ordinal = event["event_ordinal"]
    if "event_id" in result and (len(event_ids) != 1 or result["event_id"] != event_ids[0]):
        raise CommandAcceptanceError("singular event alias differs from native event set")
    return identity


def command_policy_basis(command: Mapping[str, object]) -> Mapping[str, object]:
    """Closed variant projection of already accepted policies, never re-resolution."""
    if command.get("command_kind") == "action":
        request = _require_mapping(command.get("action_request"), "accepted action request")
        parameters = request.get("parameter_bindings", {})
        variant = {"action_request": _thaw(request)}
    elif command.get("command_kind") == "transition":
        parameters = {}
        variant = {key: _thaw(command[key]) for key in ("transition_request", "transition_binding")}
    else:
        raise CommandAcceptanceError("policy command variant is unsupported")
    try:
        _parameters, facts, refs = validate_frozen_adjudication_basis(parameters, command["invocation_facts"])
    except (KeyError, TypeError, ValueError) as exc:
        raise CommandAcceptanceError("accepted policy basis is incomplete") from exc
    return {**variant, "invocation_facts": _thaw(facts), "policy_refs": list(refs)}


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
_ORDERING_OWNER_REQUIRED_FIELDS: Final[dict[str, frozenset[str]]] = {
    "runtime.resolution": frozenset(
        {
            "root_command_id",
            "activity_id",
            "actor_id",
            "ruleset_set_digest_generation",
            "ruleset_set_sha256",
            "catalog_context_fingerprint_generation",
            "catalog_context_fingerprint",
            "status",
            "next_segment_sequence",
            "invocation_facts",
            "fixed_rng_results",
            "prior_step_exports",
            "child_resolution_ids",
            "segments",
        }
    ),
    "runtime.continuation": frozenset(
        {
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
    ),
    "runtime.procedure": frozenset(
        {"schema_version", "lifecycle", "participant_resources"}
    ),
}
_RESOLUTION_BASIS_FIELDS: Final[frozenset[str]] = frozenset(
    {"initiating_command_id", "causal_invocation_key"}
)
_ORDERING_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_ORDERING_SHA256_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-f0-9]{64}$")
_ORDERING_POLICY_REF_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$"
)
_ORDERING_EXECUTION_STATES: Final[frozenset[str]] = frozenset(
    {
        "PENDING",
        "RUNNING",
        "AWAITING_CHOICE",
        "AWAITING_REACTION",
        "HYDRATION_REQUIRED",
        "PUBLISH_REQUIRED",
        "COMPLETED",
        "REJECTED",
        "ABORTED",
        "FAILED",
    }
)
_ORDERING_FAILURE_CODES: Final[frozenset[str]] = frozenset(
    {
        "failure.idempotency_conflict",
        "failure.hydration_required",
        "failure.missing_reference",
        "failure.catalog_context_incompatible",
        "failure.continuation_conflict",
        "failure.continuation_stale",
        "failure.dependency_cycle",
        "failure.transition_requires_procedure",
        "failure.order_adjudication_required",
        "failure.execution_limit",
        "failure.invocation_fact_missing",
        "failure.invocation_fact_unauthorized",
        "failure.adjudication_input_missing",
        "failure.adjudication_input_unauthorized",
        "failure.adjudication_input_invalid",
        "failure.adjudication_context_stale",
        "failure.policy_conflict",
        "failure.policy_realization_gap",
    }
)
_ORDERING_ENVELOPE_FIELDS: Final[frozenset[str]] = frozenset(
    {"kind", "id", "campaign_id", "revision"}
)
_ORDERING_RESOLUTION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "root_command_id",
        "initiating_command_id",
        "causal_invocation_key",
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "procedure_id",
        "status",
        "failure_code",
        "cursor",
        "safe_recompute_phase",
        "next_segment_sequence",
        "invocation_facts",
        "fixed_rng_results",
        "prior_step_exports",
        "child_resolution_ids",
        "segments",
        "continuation_id",
        "trace_id",
        "details",
    }
)
_ORDERING_CONTINUATION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "generation",
        "root_command_id",
        "resolution_id",
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "procedure_id",
        "execution_cursor",
        "safe_recompute_phase",
        "invocation_facts",
        "fixed_rng_results",
        "prior_step_exports",
        "committed_segment_refs",
        "dependency_frontier_refs",
        "expected_child_resolution_ids",
        "future_rng_frontier",
        "pending_response",
        "unconsumed_advancement",
        "details",
    }
)


def _ordering_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise NativeOrderingError(f"{label} must be a nonempty string")
    return value


def _ordering_id(value: object, label: str) -> str:
    result = _ordering_text(value, label)
    if _ORDERING_ID_PATTERN.fullmatch(result) is None:
        raise NativeOrderingError(f"{label} must be a machine identifier")
    return result


def _ordering_integer(value: object, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise NativeOrderingError(f"{label} must be an integer >= {minimum}")
    return value


def _ordering_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise NativeOrderingError(f"{label} must be an object with string keys")
    return value


def _ordering_array(value: object, label: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise NativeOrderingError(f"{label} must be an array")
    return value


def _ordering_scalar(value: object, label: str) -> None:
    if value is None or not isinstance(value, (str, int, float, bool)):
        raise NativeOrderingError(f"{label} must be a scalar")
    if isinstance(value, float) and not math.isfinite(value):
        raise NativeOrderingError(f"{label} must be a finite scalar")


def _ordering_sha256(value: object, label: str) -> str:
    result = _ordering_text(value, label)
    if _ORDERING_SHA256_PATTERN.fullmatch(result) is None:
        raise NativeOrderingError(f"{label} must be a lower-case SHA-256 digest")
    return result


def _ordering_unique_strings(
    value: object, label: str, *, machine_ids: bool = False, minimum: int = 0
) -> None:
    values = _ordering_array(value, label)
    if len(values) < minimum:
        raise NativeOrderingError(f"{label} must contain at least {minimum} item(s)")
    normalized: list[str] = []
    for item in values:
        normalized.append(
            _ordering_id(item, label) if machine_ids else _ordering_text(item, label)
        )
    if len(normalized) != len(set(normalized)):
        raise NativeOrderingError(f"{label} must contain unique items")


def _ordering_scalar_object(value: object, label: str) -> None:
    mapping = _ordering_mapping(value, label)
    for key, item in mapping.items():
        _ordering_text(key, f"{label} key")
        _ordering_scalar(item, f"{label} value")


def _ordering_policy_refs(value: object, label: str) -> None:
    refs = _ordering_array(value, label)
    normalized: list[str] = []
    for ref in refs:
        text = _ordering_text(ref, f"{label} item")
        if _ORDERING_POLICY_REF_PATTERN.fullmatch(text) is None:
            raise NativeOrderingError(f"{label} contains an invalid policy reference")
        normalized.append(text)
    if len(normalized) != len(set(normalized)):
        raise NativeOrderingError(f"{label} must contain unique items")


def _ordering_parameter_binding(value: object, label: str) -> None:
    if isinstance(value, (str, int, float, bool)):
        _ordering_scalar(value, label)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        values = list(value)
        if not values:
            raise NativeOrderingError(f"{label} array must not be empty")
        for item in values:
            _ordering_scalar(item, f"{label} array item")
        return
    binding = _ordering_mapping(value, label)
    allowed = {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
        "candidate_set_fingerprint",
    }
    if set(binding) - allowed or not {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }.issubset(binding):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    if binding["source_class"] != "INVOCATION_ADJUDICATED":
        raise NativeOrderingError(f"{label} has an unsupported source class")
    _ordering_scalar(binding["value"], f"{label} value")
    for field in (
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "candidate_set_fingerprint",
    ):
        if field in binding:
            _ordering_text(binding[field], f"{label} {field}")
    _ordering_policy_refs(binding["policy_basis_refs"], f"{label} policy_basis_refs")


def _ordering_parameter_bindings(value: object, label: str) -> None:
    bindings = _ordering_mapping(value, label)
    for key, item in bindings.items():
        _ordering_id(key, f"{label} key")
        _ordering_parameter_binding(item, f"{label} {key}")


def _ordering_invocation_fact(value: object, label: str) -> None:
    fact = _ordering_mapping(value, label)
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
    if set(fact) != required:
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    _ordering_id(fact["fact_id"], f"{label} fact_id")
    if type(fact["value"]) is not bool:
        raise NativeOrderingError(f"{label} value must be boolean")
    if fact["provenance_class"] != "INVOCATION_ADJUDICATED":
        raise NativeOrderingError(f"{label} provenance class is unsupported")
    _ordering_text(fact["provenance_ref"], f"{label} provenance_ref")
    _ordering_id(fact["consumer_id"], f"{label} consumer_id")
    _ordering_sha256(fact["binding_fingerprint"], f"{label} binding_fingerprint")
    _ordering_sha256(
        fact["rules_context_fingerprint"], f"{label} rules_context_fingerprint"
    )
    _ordering_policy_refs(fact["policy_basis_refs"], f"{label} policy_basis_refs")


def _ordering_roll_result(value: object, label: str) -> None:
    result = _ordering_mapping(value, label)
    required = {
        "roll_id",
        "request_id",
        "expression",
        "raw_values",
        "source_kind",
        "provenance_ref",
    }
    if set(result) != required:
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    _ordering_id(result["roll_id"], f"{label} roll_id")
    _ordering_id(result["request_id"], f"{label} request_id")
    _ordering_text(result["expression"], f"{label} expression")
    values = _ordering_array(result["raw_values"], f"{label} raw_values")
    if not values or any(type(item) is not int for item in values):
        raise NativeOrderingError(f"{label} raw_values must contain integers")
    if result["source_kind"] not in {"rng.system", "rng.player", "rng.external"}:
        raise NativeOrderingError(f"{label} source_kind is unsupported")
    _ordering_text(result["provenance_ref"], f"{label} provenance_ref")


def _ordering_pending_child(value: object, label: str) -> None:
    child = _ordering_mapping(value, label)
    required = {"firing_key", "root_command_id", "activity_id", "trigger_ref", "reason"}
    allowed = required | {"procedure_id", "child_resolution_id"}
    if set(child) - allowed or not required.issubset(child):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    for field in ("firing_key", "root_command_id", "trigger_ref"):
        _ordering_text(child[field], f"{label} {field}")
    _ordering_id(child["activity_id"], f"{label} activity_id")
    for field in ("procedure_id", "child_resolution_id"):
        if field in child:
            _ordering_text(child[field], f"{label} {field}")
    if child["reason"] not in {"mandatory_followup", "execution_limit"}:
        raise NativeOrderingError(f"{label} reason is unsupported")


def _validate_resume_marker_shape(segment: Mapping[str, object]) -> None:
    """Validate a retained R marker's closed types, never its native issuance."""
    marker = segment["accepted_resume_input"]
    _input_wire("https://hedgelion.invalid/schemas/execution-segment.schema.json#/$defs/acceptedResumeInput", marker)
    for field in ("schema_version", "resume_fingerprint_generation"):
        _input_integer(marker[field], exact=1)
    _input_integer(marker["target"]["continuation_generation"])
    sequence = _input_integer(segment["segment_sequence"])
    if segment["segment_id"] != f'{marker["target"]["resolution_id"]}:segment:{sequence}':
        raise CommandAcceptanceError("response marker is not embedded under its exact Resolution")


def _ordering_segment(value: object, label: str) -> None:
    segment = _ordering_mapping(value, label)
    required = {
        "schema_version",
        "segment_id",
        "segment_sequence",
        "commit_state",
        "resulting_execution_state",
        "event_ids",
        "pending_child_invocations",
        "receipt_exports",
        "affected_revision_refs",
    }
    allowed = required | {"continuation_id", "accepted_resume_input"}
    if set(segment) - allowed or not required.issubset(segment):
        raise NativeOrderingError(f"{label} has unexpected or missing fields")
    if type(segment["schema_version"]) is not int or segment["schema_version"] != 1:
        raise NativeOrderingError(f"{label} schema_version must be exactly 1")
    _ordering_id(segment["segment_id"], f"{label} segment_id")
    _ordering_integer(
        segment["segment_sequence"], f"{label} segment_sequence", minimum=1
    )
    if segment["commit_state"] != "committed":
        raise NativeOrderingError(f"{label} commit_state is unsupported")
    if segment["resulting_execution_state"] not in _ORDERING_EXECUTION_STATES:
        raise NativeOrderingError(f"{label} resulting_execution_state is unsupported")
    _ordering_unique_strings(segment["event_ids"], f"{label} event_ids")
    children = _ordering_array(
        segment["pending_child_invocations"], f"{label} pending_child_invocations"
    )
    for index, child in enumerate(children):
        _ordering_pending_child(child, f"{label} pending_child_invocations[{index}]")
    receipt_exports = _ordering_mapping(
        segment["receipt_exports"], f"{label} receipt_exports"
    )
    for key, item in receipt_exports.items():
        _ordering_id(key, f"{label} receipt export key")
        _ordering_scalar(item, f"{label} receipt export value")
    _ordering_unique_strings(
        segment["affected_revision_refs"], f"{label} affected_revision_refs"
    )
    if "continuation_id" in segment:
        _ordering_text(segment["continuation_id"], f"{label} continuation_id")
    if "accepted_resume_input" in segment:
        try:
            _validate_resume_marker_shape(segment)
        except CommandAcceptanceError as exc:
            raise NativeOrderingError(f"{label} retained response marker is invalid: {exc}") from exc


def _ordering_pending_response_schema(value: object, label: str) -> None:
    offer = _ordering_mapping(value, label)
    kind = offer.get("kind")
    fields = (
        _CHOICE_FIELDS
        if kind == "choice"
        else _REACTION_FIELDS
        if kind == "reaction"
        else None
    )
    if fields is None or set(offer) != fields:
        raise NativeOrderingError(
            f"{label} is not a valid ChoiceRequest or ReactionOffer"
        )
    _ordering_text(offer["offer_id"], f"{label} offer_id")
    _ordering_text(offer["parent_resolution_id"], f"{label} parent_resolution_id")
    _ordering_integer(
        offer["continuation_generation"], f"{label} continuation_generation", minimum=1
    )
    _ordering_text(offer["responder_id"], f"{label} responder_id")
    item_field = "option_ids" if kind == "choice" else "candidate_activity_ids"
    _ordering_unique_strings(offer[item_field], f"{label} {item_field}", minimum=1)


def _ordering_resolution_schema(payload: Mapping[str, object]) -> None:
    if type(payload.get("schema_version")) is not int or payload["schema_version"] != 1:
        raise NativeOrderingError("resolution schema_version must be exactly 1")
    for field in (
        "root_command_id",
        "initiating_command_id",
        "causal_invocation_key",
        "cursor",
        "safe_recompute_phase",
        "trace_id",
    ):
        if field in payload:
            _ordering_text(payload[field], f"resolution {field}")
    for field in ("activity_id", "actor_id", "source_id"):
        if field in payload:
            _ordering_id(payload[field], f"resolution {field}")
    for field in ("continuation_id", "procedure_id"):
        if field in payload:
            _ordering_text(payload[field], f"resolution {field}")
    if "target_ids" in payload:
        _ordering_unique_strings(
            payload["target_ids"], "resolution target_ids", machine_ids=True
        )
    if "parameter_bindings" in payload:
        _ordering_parameter_bindings(
            payload["parameter_bindings"], "resolution parameter_bindings"
        )
    for field in (
        "catalog_context_fingerprint_generation",
        "ruleset_set_digest_generation",
    ):
        if type(payload[field]) is not int or payload[field] != 1:
            raise NativeOrderingError(f"resolution {field} must be exactly 1")
    _ordering_text(
        payload["catalog_context_fingerprint"], "resolution catalog_context_fingerprint"
    )
    _ordering_sha256(payload["ruleset_set_sha256"], "resolution ruleset_set_sha256")
    if payload["status"] not in _ORDERING_EXECUTION_STATES:
        raise NativeOrderingError("resolution status is unsupported")
    if (
        "failure_code" in payload
        and payload["failure_code"] not in _ORDERING_FAILURE_CODES
    ):
        raise NativeOrderingError("resolution failure_code is unsupported")
    if (
        payload["status"] in {"HYDRATION_REQUIRED", "REJECTED", "FAILED"}
        and "failure_code" not in payload
    ):
        raise NativeOrderingError("resolution failure_code is required for its status")
    if "failure_code" in payload and payload["status"] not in {
        "HYDRATION_REQUIRED",
        "REJECTED",
        "ABORTED",
        "FAILED",
    }:
        raise NativeOrderingError("resolution failure_code conflicts with its status")
    _ordering_integer(
        payload["next_segment_sequence"], "resolution next_segment_sequence", minimum=1
    )
    facts = _ordering_array(payload["invocation_facts"], "resolution invocation_facts")
    for index, fact in enumerate(facts):
        _ordering_invocation_fact(fact, f"resolution invocation_facts[{index}]")
    rolls = _ordering_array(
        payload["fixed_rng_results"], "resolution fixed_rng_results"
    )
    for index, roll in enumerate(rolls):
        _ordering_roll_result(roll, f"resolution fixed_rng_results[{index}]")
    _ordering_scalar_object(
        payload["prior_step_exports"], "resolution prior_step_exports"
    )
    _ordering_unique_strings(
        payload["child_resolution_ids"], "resolution child_resolution_ids"
    )
    segments = _ordering_array(payload["segments"], "resolution segments")
    for index, segment in enumerate(segments):
        _ordering_segment(segment, f"resolution segments[{index}]")
        if ("accepted_resume_input" in segment
                and segment["accepted_resume_input"]["target"]["root_command_id"] != payload["root_command_id"]):
            raise NativeOrderingError("retained response marker has a foreign root command")
    if "details" in payload:
        _ordering_mapping(payload["details"], "resolution details")


def _ordering_continuation_schema(payload: Mapping[str, object]) -> None:
    _ordering_integer(payload["generation"], "continuation generation", minimum=1)
    for field in (
        "root_command_id",
        "resolution_id",
        "execution_cursor",
        "safe_recompute_phase",
        "future_rng_frontier",
    ):
        _ordering_text(payload[field], f"continuation {field}")
    if "procedure_id" in payload:
        _ordering_text(payload["procedure_id"], "continuation procedure_id")
    for field in ("activity_id", "actor_id", "source_id"):
        if field in payload:
            _ordering_id(payload[field], f"continuation {field}")
    if "target_ids" in payload:
        _ordering_unique_strings(
            payload["target_ids"], "continuation target_ids", machine_ids=True
        )
    if "parameter_bindings" in payload:
        _ordering_parameter_bindings(
            payload["parameter_bindings"], "continuation parameter_bindings"
        )
    for field in (
        "catalog_context_fingerprint_generation",
        "ruleset_set_digest_generation",
    ):
        if type(payload[field]) is not int or payload[field] != 1:
            raise NativeOrderingError(f"continuation {field} must be exactly 1")
    _ordering_text(
        payload["catalog_context_fingerprint"],
        "continuation catalog_context_fingerprint",
    )
    _ordering_sha256(payload["ruleset_set_sha256"], "continuation ruleset_set_sha256")
    for field in ("invocation_facts", "fixed_rng_results"):
        values = _ordering_array(payload[field], f"continuation {field}")
        validator = (
            _ordering_invocation_fact
            if field == "invocation_facts"
            else _ordering_roll_result
        )
        for index, item in enumerate(values):
            validator(item, f"continuation {field}[{index}]")
    _ordering_scalar_object(
        payload["prior_step_exports"], "continuation prior_step_exports"
    )
    for field in (
        "committed_segment_refs",
        "dependency_frontier_refs",
        "expected_child_resolution_ids",
    ):
        _ordering_unique_strings(payload[field], f"continuation {field}")
    if "pending_response" in payload:
        _ordering_pending_response_schema(
            payload["pending_response"], "continuation pending_response"
        )
    if "unconsumed_advancement" in payload:
        advancement = _ordering_mapping(
            payload["unconsumed_advancement"], "continuation unconsumed_advancement"
        )
        if set(advancement) != {"amount", "unit_id", "context_id"}:
            raise NativeOrderingError(
                "continuation unconsumed_advancement has unexpected or missing fields"
            )
        _ordering_integer(
            advancement["amount"], "continuation advancement amount", minimum=1
        )
        if advancement["unit_id"] not in {
            "unit.second",
            "unit.minute",
            "unit.hour",
            "unit.day",
        }:
            raise NativeOrderingError("continuation advancement unit_id is unsupported")
        _ordering_text(advancement["context_id"], "continuation advancement context_id")
    if "details" in payload:
        _ordering_mapping(payload["details"], "continuation details")


def _validate_ordering_owner_schema(family: str, payload: Mapping[str, object]) -> None:
    missing = _ORDERING_OWNER_REQUIRED_FIELDS[family].difference(payload)
    if missing:
        raise NativeOrderingError(
            f"exact {family} record is missing required owner-schema fields"
        )
    if family == "runtime.resolution" and not _RESOLUTION_BASIS_FIELDS.intersection(
        payload
    ):
        raise NativeOrderingError(
            "exact runtime.resolution record is missing command or invocation basis"
        )
    allowed = _ORDERING_ENVELOPE_FIELDS.copy()
    if family == "runtime.resolution":
        allowed |= _ORDERING_RESOLUTION_FIELDS
    elif family == "runtime.continuation":
        allowed |= _ORDERING_CONTINUATION_FIELDS
    else:
        return
    unexpected = set(payload) - allowed
    if unexpected:
        raise NativeOrderingError(
            f"exact {family} record has unsupported owner-schema fields"
        )
    if family == "runtime.resolution":
        _ordering_resolution_schema(payload)
    else:
        _ordering_continuation_schema(payload)


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
            raise NativeOrderingError(
                f"exact {family} identity is stale or foreign"
            ) from exc
        raise NativeOrderingError(f"exact {family} owner read failed") from exc
    if payload.get("campaign_id") not in {None, campaign_pin.campaign_id}:
        raise NativeOrderingError(f"exact {family} belongs to another campaign")
    record_revision = payload.get("revision")
    if record_revision is not None and record_revision != campaign_pin.revision:
        raise NativeOrderingError(f"exact {family} record is stale")
    if family == "runtime.resolution" and "state" in payload:
        # The native envelope is authoritative; normalize only after checking
        # every duplicated projection. This is the same W07 source, not a second
        # ordering owner or a fallback to a stale flattened representation.
        try:
            state = validate_input_resolution(resolution_id=record_id, resolution=payload)
        except CommandAcceptanceError as exc:
            raise NativeOrderingError("native Resolution envelope/state is inconsistent") from exc
        payload = {**{key: payload[key] for key in _ORDERING_ENVELOPE_FIELDS if key in payload},
                   **{key: value for key, value in state.items() if key != "resolution_id"}}
    _validate_ordering_owner_schema(family, payload)
    return payload


def _pending_offer(
    response: object,
    *,
    resolution_id: str,
    continuation_generation: int,
) -> tuple[str, str, str]:
    offer = response if isinstance(response, Mapping) else None
    if offer is None or set(offer) not in {_CHOICE_FIELDS, _REACTION_FIELDS}:
        raise NativeOrderingError(
            "continuation pending response is not a valid ChoiceRequest or ReactionOffer"
        )
    kind = offer.get("kind")
    expected_fields = (
        _CHOICE_FIELDS
        if kind == "choice"
        else _REACTION_FIELDS
        if kind == "reaction"
        else None
    )
    if expected_fields is None or set(offer) != expected_fields:
        raise NativeOrderingError("continuation pending response kind is not admitted")
    offer_id = _ordering_text(offer.get("offer_id"), "pending offer id")
    if offer.get("parent_resolution_id") != resolution_id:
        raise NativeOrderingError(
            "pending offer does not belong to the current resolution"
        )
    if offer.get("continuation_generation") != continuation_generation:
        raise NativeOrderingError(
            "pending offer generation differs from the current continuation"
        )
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
        raise NativeOrderingError(
            "resolution and continuation procedure linkage differs"
        )
    procedure = _ordering_record(
        repository, campaign_pin, "runtime.procedure", procedure_ref
    )
    declared_procedure_id = procedure.get("procedure_id", procedure.get("id"))
    if declared_procedure_id != procedure_ref:
        raise NativeOrderingError(
            "linked procedure identity differs from its native route"
        )
    state = procedure.get("state")
    if state is not None and not isinstance(state, Mapping):
        raise NativeOrderingError("linked procedure state is malformed")
    procedure_state = state if isinstance(state, Mapping) else procedure
    if (
        procedure_state.get("schema_version") != 2
        or procedure_state.get("lifecycle") != "ACTIVE"
    ):
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
        raise NativeOrderingError(
            "native ordering request must contain only resolution_id"
        )
    resolution_id = _ordering_text(request.get("resolution_id"), "resolution id")
    resolution = _ordering_record(
        repository, campaign_pin, "runtime.resolution", resolution_id
    )
    declared_resolution_id = resolution.get("resolution_id", resolution.get("id"))
    if declared_resolution_id != resolution_id:
        raise NativeOrderingError("resolution identity differs from requested identity")
    status = resolution.get("status")
    if status not in {"AWAITING_CHOICE", "AWAITING_REACTION"}:
        raise NativeOrderingError("resolution is not awaiting an owner response")
    continuation_id = _ordering_text(
        resolution.get("continuation_id"), "resolution continuation id"
    )
    continuation = _ordering_record(
        repository, campaign_pin, "runtime.continuation", continuation_id
    )
    if continuation.get("resolution_id") != resolution_id:
        raise NativeOrderingError(
            "continuation does not belong to the current resolution"
        )
    generation = continuation.get("generation")
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation < 1
    ):
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
        raise NativeOrderingError(
            "resolution and continuation procedure linkage is incomplete"
        )
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
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(char not in _SHA256_HEX for char in value)
    ):
        raise CommandAcceptanceError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _typed_interpreter_result(value: object) -> dict[str, str]:
    raw_result = _require_exact_fields(
        value, INTERPRETER_RESULT_FIELDS, "interpreter result"
    )
    result = {
        field: _require_nonempty_string(
            raw_result[field], f"interpreter result {field}"
        )
        for field in INTERPRETER_RESULT_FIELDS
    }
    if result["kind"] != "interpreter_result":
        raise CommandAcceptanceError(
            "interpreter result kind is not interpreter_result"
        )
    return result


def _candidate_identity(value: object) -> tuple[str, str]:
    candidate = _require_exact_fields(
        value, frozenset({"definition_id", "kind"}), "candidate"
    )
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
    action_request = _require_mapping(
        proposal["action_request"], "command proposal action_request"
    )
    allowed_action_fields = {
        "activity_id",
        "actor_id",
        "source_id",
        "target_ids",
        "parameter_bindings",
    }
    if set(action_request) - allowed_action_fields or not {
        "activity_id",
        "actor_id",
    }.issubset(action_request):
        raise CommandAcceptanceError(
            "command proposal action_request has unexpected or missing fields"
        )
    activity_id = _require_nonempty_string(
        action_request["activity_id"], "action_request activity_id"
    )
    if activity_id != candidate_id:
        raise CommandAcceptanceError(
            "action_request activity_id differs from candidate"
        )
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


def _bound_input_origin(command: Mapping[str, object], observation: CurrentOwnerObservation,
                        *, current_authority: bool = True) -> Mapping[str, object]:
    """Check the real composition/source session; no flag or seal grants auth."""
    from .runtime_host import RuntimeHost, RuntimeHostError, _InputSourceOperation

    if type(observation) is not CurrentOwnerObservation:
        raise CommandAcceptanceError("input observation must come from the bound Host source session")
    operation = observation.operation_token
    if type(operation) is not _InputSourceOperation or type(operation.host) is not RuntimeHost:
        raise CommandAcceptanceError("input observation is not a bound Host input operation")
    try:
        return operation.host._current_owner._validate_command_input_observation(
            observation, command, current_authority=current_authority)
    except RuntimeHostError as exc:
        raise CommandAcceptanceError(str(exc)) from exc


def native_command_state(
    owner: Mapping[str, object], *, command_id: str, campaign_id: str,
) -> Mapping[str, object]:
    """Envelope-first command source parsing, including exact flattened aliases."""
    if (owner.get("kind") != "runtime.command" or owner.get("id") != command_id
            or owner.get("campaign_id", campaign_id) != campaign_id):
        raise CommandAcceptanceError("native command envelope is foreign or incomplete")
    if "state" in owner:
        state = _require_mapping(owner["state"], "native command state")
        for field, value in state.items():
            if field in owner and canonical_json(owner[field]) != canonical_json(value):
                raise CommandAcceptanceError("native command flattened alias differs")
    else:
        state = {key: value for key, value in owner.items()
            if key not in {"kind", "id", "campaign_id", "revision", "state_revision"}}
    if state.get("command_id") != command_id:
        raise CommandAcceptanceError("native command state identity differs from its envelope")
    _input_integer(state.get("schema_version"), exact=4)
    _input_integer(state.get("input_fingerprint_generation"), exact=3)
    _input_wire("runtime-command-state", state)
    return state


def _validate_native_command_projection(command: Mapping[str, object], observation: CurrentOwnerObservation) -> None:
    try:
        read = observation.require(NativeOwnerRef("runtime.command", (command["command_id"],)))
        if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
            raise CommandAcceptanceError("native accepted command source is unavailable")
        campaign_id = observation.operation_token.host._campaign_id
        native = native_command_state(read.payload, command_id=command["command_id"], campaign_id=campaign_id)
        if canonical_json(_thaw(native)) != canonical_json(_thaw(command)):
            raise CommandAcceptanceError("execution proposal differs from the actual native accepted command")
        plan_read = observation.require(NativeOwnerRef("runtime.intent_plan", (command["intent_plan_id"],)))
        clauses = input_native_state(plan_read.payload, "runtime.intent_plan")["clauses"]
        matches = [clause for clause in clauses if clause["clause_id"] == command["clause_id"]]
        if len(matches) != 1 or matches[0].get("command_id") != command["command_id"]:
            raise CommandAcceptanceError("native accepted command lacks reciprocal clause linkage")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, CommandAcceptanceError):
            raise
        raise CommandAcceptanceError("native accepted command/Plan source closure is incomplete") from exc


def _require_admitted_context(context: object) -> BoundCatalogContext:
    if not isinstance(context, BoundCatalogContext) or not context._is_admitted():
        raise CommandAcceptanceError(
            "catalog context must be an admitted bound context"
        )
    return context


def accept_command(
    interpreter_result: object,
    context: BoundCatalogContext,
    candidate: object,
    command_proposal: object,
    *,
    input_observation: CurrentOwnerObservation,
    adjudication_basis: AcceptedAdjudicationBasis | None = None,
) -> dict[str, object] | CatalogGap:
    """Return a schema-shaped accepted command or typed catalog-gap evidence."""

    origin = _bound_input_origin(_require_mapping(command_proposal, "command proposal"), input_observation)
    if command_proposal.get("command_kind") == "transition":
        if interpreter_result is not None or candidate is not None or adjudication_basis is not None:
            raise CommandAcceptanceError("direct transition forbids action interpreter/candidate/adjudication")
        admitted_context = _require_admitted_context(context)
        proposal = _require_exact_fields(command_proposal, frozenset({
            "command_id", "interaction_id", "intent_plan_id", "clause_id", "command_kind",
            "transition_request", "transition_binding"}), "direct command proposal")
        direct_input_contract(proposal, admitted_context)
        command = {**_thaw(proposal), "schema_version": RUNTIME_COMMAND_SCHEMA_VERSION,
            "catalog_context_fingerprint": admitted_context.fingerprint,
            "catalog_context": admitted_context.to_dict(),
            "input_fingerprint_generation": RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION,
            "disposition": "command.accepted", "invocation_facts": [], "pending_child_invocations": []}
        command["input_fingerprint"] = command_input_fingerprint(command, origin=origin)
        _input_wire("runtime-command-state", command)
        return command
    typed_result = _typed_interpreter_result(interpreter_result)
    admitted_context = _require_admitted_context(context)
    candidate_id, _candidate_kind = _candidate_identity(candidate)
    proposal = _typed_command_proposal(command_proposal, candidate_id)
    action_request = _require_mapping(
        proposal["action_request"], "accepted action_request"
    )
    if adjudication_basis is not None:
        if not is_accepted_basis_issued(adjudication_basis):
            raise CommandAcceptanceError(
                "adjudication basis must be resolver-produced evidence"
            )
        expected_bindings = adjudication_basis.runtime_parameter_bindings()
        actual_bindings = action_request.get("parameter_bindings", {})
        if actual_bindings != expected_bindings:
            raise CommandAcceptanceError(
                "accepted adjudication parameters differ from verified basis"
            )
        invocation_facts = adjudication_basis.runtime_invocation_facts()
    else:
        invocation_facts = []
        if any(
            isinstance(binding, Mapping)
            and binding.get("source_class") == "INVOCATION_ADJUDICATED"
            for binding in action_request.get("parameter_bindings", {}).values()
        ):
            raise CommandAcceptanceError(
                "adjudicated parameters require a verified policy basis"
            )
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
        raise CommandAcceptanceError(
            "accepted adjudication parameters differ from verified basis"
        )
    invocation_facts = normalized_facts
    try:
        catalog_result = bind_executable_catalog(admitted_context, candidate)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if catalog_result["status"] == "gap":
        return CatalogGap(
            _require_mapping(catalog_result["gap_report"], "catalog gap report")
        )

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
    command["input_fingerprint"] = command_input_fingerprint(command, origin=origin)
    return command


def validate_execution_proposal(
    accepted_command: object,
    context: BoundCatalogContext,
    candidate: object,
    *,
    input_observation: CurrentOwnerObservation,
) -> None:
    """Validate a prospective protected edge with fresh source/control authority."""
    _validate_execution_proposal(accepted_command, context, candidate,
        input_observation=input_observation, current_authority=True)


def _validate_execution_proposal(
    accepted_command: object,
    context: BoundCatalogContext,
    candidate: object,
    *,
    input_observation: CurrentOwnerObservation,
    current_authority: bool,
) -> None:
    """Verify a serialized command's exact basis and recomputed acceptance fingerprints."""

    raw = _require_mapping(accepted_command, "accepted command")
    if raw.get("command_kind") == "transition":
        command = raw
        _input_wire("runtime-command-state", command)
        origin = _bound_input_origin(command, input_observation, current_authority=current_authority)
        _validate_native_command_projection(command, input_observation)
        admitted_context = _require_admitted_context(context)
        if candidate is not None:
            raise CommandAcceptanceError("direct transition forbids an action candidate")
        direct_input_contract(command, admitted_context)
        if (command["catalog_context"] != admitted_context.to_dict()
                or command["catalog_context_fingerprint"] != admitted_context.fingerprint):
            raise CommandAcceptanceError("direct context differs from admitted basis")
        if command["invocation_facts"]:
            raise CommandAcceptanceError("native direct profile admits no invocation facts")
        if command["input_fingerprint"] != command_input_fingerprint(command, origin=origin):
            raise CommandAcceptanceError("input fingerprint differs from accepted direct command")
        if command["disposition"] == "command.settled" and not command.get("direct_transition_receipt"):
            raise CommandAcceptanceError("settled direct command has no native result receipt")
        return
    command = _require_exact_fields(
        accepted_command, COMMAND_STATE_FIELDS, "accepted command"
    )
    origin = _bound_input_origin(command, input_observation, current_authority=current_authority)
    _validate_native_command_projection(command, input_observation)
    admitted_context = _require_admitted_context(context)
    if command["schema_version"] != RUNTIME_COMMAND_SCHEMA_VERSION:
        raise CommandAcceptanceError("unsupported runtime command schema version")
    for field in (
        "command_id",
        "interaction_id",
        "intent_plan_id",
        "clause_id",
        "root_resolution_id",
    ):
        _require_nonempty_string(command[field], f"accepted command {field}")
    if command["command_kind"] != "action" or command["disposition"] not in {
        "command.accepted",
        "command.settled",
    }:
        raise CommandAcceptanceError("accepted command has an unsupported disposition")
    if not isinstance(command["invocation_facts"], list):
        raise CommandAcceptanceError(
            "accepted command invocation facts must be an array"
        )
    action_request = _require_mapping(
        command["action_request"], "accepted command action_request"
    )
    try:
        parameters, facts = validate_adjudicated_input_surface(
            _require_nonempty_string(
                action_request.get("activity_id"), "action_request activity_id"
            ),
            action_request.get("parameter_bindings", {}),
            command["invocation_facts"],
        )
    except PolicyBasisResolutionError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    if (
        parameters != action_request.get("parameter_bindings", {})
        or facts != command["invocation_facts"]
    ):
        raise CommandAcceptanceError(
            "accepted adjudication input differs from its normalized basis"
        )
    if not isinstance(command["pending_child_invocations"], list):
        raise CommandAcceptanceError(
            "accepted command pending child invocations must be an array"
        )
    if (
        command["disposition"] == "command.settled"
        and command["pending_child_invocations"]
    ):
        raise CommandAcceptanceError(
            "settled command retains pending child invocations"
        )
    if (
        command["input_fingerprint_generation"]
        != RUNTIME_COMMAND_INPUT_FINGERPRINT_GENERATION
    ):
        raise CommandAcceptanceError("unsupported command input fingerprint generation")
    if (
        command["interpreter_result_fingerprint_generation"]
        != INTERPRETER_RESULT_FINGERPRINT_GENERATION
    ):
        raise CommandAcceptanceError(
            "unsupported interpreter result fingerprint generation"
        )
    interpreter_result = _typed_interpreter_result(command["interpreter_result"])
    if command["interpreter_result_fingerprint"] != _interpreter_result_fingerprint(
        interpreter_result
    ):
        raise CommandAcceptanceError(
            "interpreter result fingerprint differs from accepted result"
        )
    if command["catalog_context_fingerprint"] != admitted_context.fingerprint:
        raise CommandAcceptanceError("stale catalog context")
    if command["catalog_context"] != admitted_context.to_dict():
        raise CommandAcceptanceError("catalog context differs from accepted basis")
    binding = _require_mapping(
        command["candidate_binding"], "accepted command catalog binding"
    )
    try:
        validate_executable_binding(admitted_context, binding)
    except CatalogBindingError as exc:
        raise CommandAcceptanceError(str(exc)) from exc
    candidate_id, candidate_kind = _candidate_identity(candidate)
    if candidate_id != binding["definition_id"] or candidate_kind != binding["kind"]:
        raise CommandAcceptanceError("candidate differs from accepted binding")
    _typed_command_proposal(
        {key: command[key] for key in COMMAND_PROPOSAL_FIELDS},
        candidate_id,
    )
    _require_sha256(command["input_fingerprint"], "accepted command input fingerprint")
    if command["input_fingerprint"] != command_input_fingerprint(command, origin=origin):
        raise CommandAcceptanceError("input fingerprint differs from accepted command")
