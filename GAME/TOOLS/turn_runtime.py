"""Transient typed controls for one logical HDM turn."""

from __future__ import annotations

from typing import Any


PHASE_RESULT_KINDS = {
    "INTERPRETER": {"interpreter_result"},
    "DRAMATURG": {"preparation_draft"},
    "ACTOR": {"actor_proposal"},
    "CHRONICLER": {"story_projection_draft"},
    "NARRATOR": {"narration_result"},
}
RESULT_REQUIRED_FIELDS = {
    "interpreter_result": frozenset({"kind", "purpose", "bundle_id", "source_generation", "intent"}),
    "preparation_draft": frozenset({"kind", "purpose", "bundle_id", "source_generation", "pressures"}),
    "actor_proposal": frozenset({"kind", "purpose", "bundle_id", "source_generation", "subject_id", "proposal"}),
    "story_projection_draft": frozenset({"kind", "purpose", "bundle_id", "source_generation", "source_refs"}),
    "narration_result": frozenset({"kind", "bundle_id", "recipient_id", "prose", "disclosure_refs"}),
}
EXECUTION_HANDOFF_KIND = "execution_result"
EXECUTION_HANDOFF_REQUIRED_FIELDS = frozenset(
    {
        "kind",
        "accepted_command_id",
        "accepted_input_fingerprint",
        "execution_owner_id",
        "resolution_id",
        "status",
        "segment_id",
        "event_id",
    }
)
FORBIDDEN_HANDOFF_KEYS = frozenset({"raw_bundle", "context_trace", "hidden_reasoning", "role_frame", "tool_payload"})
FALLBACKS = frozenset({"BLOCKED", "DEGRADED", "CLARIFICATION", "DETERMINISTIC_PATH"})
EXECUTION_STATES = frozenset(
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
SHA256_HEX = frozenset("0123456789abcdef")


class TurnContractError(ValueError):
    """A transient turn control contract was not satisfied."""


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TurnContractError(f"{label} must be a nonempty string")
    return value


def start_turn(turn_id: str, accepted_frontier: str, protected_narrator_capacity: int) -> dict[str, Any]:
    """Start a control-only envelope; it deliberately carries no gameplay state."""
    _nonempty_string(turn_id, "turn_id")
    _nonempty_string(accepted_frontier, "accepted_frontier")
    if (
        isinstance(protected_narrator_capacity, bool)
        or not isinstance(protected_narrator_capacity, int)
        or protected_narrator_capacity < 0
    ):
        raise TurnContractError("protected_narrator_capacity must be a nonnegative integer")
    return {
        "turn_id": turn_id,
        "accepted_frontier": accepted_frontier,
        "protected_narrator_capacity": protected_narrator_capacity,
        "auxiliary_capacity": 0,
        "phase_bindings": {},
        "accepted_results": {},
        "accepted_handoffs": {},
        "remaining_narrator_capacity": protected_narrator_capacity,
        "emitted_payload": None,
    }


def bind_phase(
    envelope: dict[str, Any], role: str, purpose: str, profile_id: str, bundle_id: str, allowed_results: tuple[str, ...],
    *, subject_id: str | None = None, recipient_id: str | None = None,
    allowed_handoffs: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Bind one registered role to its independently assembled context basis."""
    if role not in PHASE_RESULT_KINDS:
        raise TurnContractError("unregistered role")
    for label, value in (("purpose", purpose), ("profile_id", profile_id), ("bundle_id", bundle_id)):
        _nonempty_string(value, label)
    if (
        not isinstance(allowed_results, tuple)
        or not allowed_results
        or any(not isinstance(item, str) or item not in PHASE_RESULT_KINDS[role] for item in allowed_results)
    ):
        raise TurnContractError("allowed_results must be registered for the bound phase")
    if not isinstance(allowed_handoffs, tuple) or any(
        item != EXECUTION_HANDOFF_KIND for item in allowed_handoffs
    ):
        raise TurnContractError("allowed_handoffs must be registered typed handoffs")
    for label, value in (("subject_id", subject_id), ("recipient_id", recipient_id)):
        if value is not None:
            _nonempty_string(value, label)
    binding = {
        "purpose": purpose,
        "profile_id": profile_id,
        "bundle_id": bundle_id,
        "allowed_results": list(allowed_results),
        "subject_id": subject_id,
        "recipient_id": recipient_id,
        "allowed_handoffs": list(allowed_handoffs),
    }
    envelope["phase_bindings"][role] = binding
    return binding


def accept_phase_result(envelope: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Accept the minimum registered result; raw role-private material never crosses."""
    if not isinstance(result, dict):
        raise TurnContractError("result must be an object")
    if FORBIDDEN_HANDOFF_KEYS.intersection(result):
        raise TurnContractError("result contains protected private material")
    kind = result.get("kind")
    if not isinstance(kind, str):
        raise TurnContractError("result kind must be a registered result string")
    required_fields = RESULT_REQUIRED_FIELDS.get(kind)
    if required_fields is None or set(result) != required_fields:
        raise TurnContractError("result does not satisfy its registered schema contract")
    bindings = envelope.get("phase_bindings", {})
    matching_roles = [role for role, allowed in PHASE_RESULT_KINDS.items() if kind in allowed and role in bindings]
    if len(matching_roles) != 1:
        raise TurnContractError("result kind is not accepted by exactly one bound phase")
    role = matching_roles[0]
    binding = bindings[role]
    if kind not in binding["allowed_results"]:
        raise TurnContractError("result kind is outside the bound allowed-results scope")
    if "purpose" in required_fields and result.get("purpose") != binding["purpose"]:
        raise TurnContractError("result purpose does not match phase binding")
    if result.get("bundle_id") != binding["bundle_id"]:
        raise TurnContractError("result bundle_id does not match phase binding")
    for field in ("subject_id", "recipient_id"):
        if binding[field] is not None and result.get(field) != binding[field]:
            raise TurnContractError(f"result {field} does not match phase binding")
    if "source_generation" in required_fields and result.get("source_generation") != envelope.get("accepted_frontier"):
        raise TurnContractError("result source_generation does not match accepted frontier")
    accepted = dict(result)
    envelope["accepted_results"][role] = accepted
    return accepted


def accept_execution_handoff(
    envelope: dict[str, Any], recipient_role: str, execution_result: object
) -> dict[str, Any]:
    """Project committed mechanics into one registered, recipient-scoped handoff."""
    bindings = envelope.get("phase_bindings", {})
    binding = bindings.get(recipient_role)
    if not isinstance(binding, dict):
        raise TurnContractError("recipient phase is not bound")
    if EXECUTION_HANDOFF_KIND not in binding.get("allowed_handoffs", []):
        raise TurnContractError("execution result is outside the bound handoff scope")
    handoff = _execution_handoff(execution_result)
    accepted_handoffs = envelope.setdefault("accepted_handoffs", {})
    prior = accepted_handoffs.setdefault(recipient_role, [])
    for existing in prior:
        if existing["accepted_command_id"] == handoff["accepted_command_id"]:
            if existing != handoff:
                raise TurnContractError("execution handoff conflicts with an accepted result")
            return dict(existing)
    prior.append(dict(handoff))
    return dict(handoff)


def advance_phase(envelope: dict[str, Any], role: str) -> str:
    """Record that a bound phase completed without inventing durable lifecycle state."""
    if role not in envelope.get("phase_bindings", {}):
        raise TurnContractError("phase is not bound")
    return role


def reserve_auxiliary_capacity(envelope: dict[str, Any], requested: int) -> int:
    """Reserve only spare capacity; protected Narrator capacity is never spendable."""
    if isinstance(requested, bool) or not isinstance(requested, int) or requested < 0:
        raise TurnContractError("requested capacity must be a nonnegative integer")
    # This owner receives a protected reservation, not a total host envelope.
    # No separately admitted spare capacity exists at this boundary.
    return 0


def _execution_handoff(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        raise TurnContractError("execution result must be a typed object")
    if FORBIDDEN_HANDOFF_KEYS.intersection(value):
        raise TurnContractError("execution result contains protected diagnostic material")
    segment = value.get("segment")
    event = value.get("event")
    if not isinstance(segment, dict) or not isinstance(event, dict):
        raise TurnContractError("execution result is missing committed segment evidence")
    command_id = _nonempty_string(value.get("accepted_command_id"), "accepted_command_id")
    input_fingerprint = _nonempty_string(
        value.get("accepted_input_fingerprint"), "accepted_input_fingerprint"
    )
    if len(input_fingerprint) != 64 or any(char not in SHA256_HEX for char in input_fingerprint):
        raise TurnContractError("accepted_input_fingerprint must be a SHA-256 fingerprint")
    execution_owner_id = _nonempty_string(value.get("execution_owner_id"), "execution_owner_id")
    resolution_id = _nonempty_string(value.get("resolution_id"), "resolution_id")
    status = _nonempty_string(value.get("status"), "status")
    if status not in EXECUTION_STATES:
        raise TurnContractError("execution result status is not registered")
    segment_id = _nonempty_string(segment.get("segment_id"), "segment_id")
    event_id = _nonempty_string(value.get("event_id"), "event_id")
    event_ids = segment.get("event_ids")
    if not isinstance(event_ids, list) or event_id not in event_ids:
        raise TurnContractError("execution event is not committed by its segment")
    if event.get("segment_id") != segment_id or event.get("root_command_id") != command_id:
        raise TurnContractError("execution event evidence is not bound to the accepted command")
    return {
        "kind": EXECUTION_HANDOFF_KIND,
        "accepted_command_id": command_id,
        "accepted_input_fingerprint": input_fingerprint,
        "execution_owner_id": execution_owner_id,
        "resolution_id": resolution_id,
        "status": status,
        "segment_id": segment_id,
        "event_id": event_id,
    }


def select_fallback(outcome: str, registered_fallbacks: tuple[str, ...]) -> str:
    """Choose exactly one registered finite fallback for a terminal assembly outcome."""
    if outcome != "UNSATISFIABLE":
        raise TurnContractError("fallback selection requires UNSATISFIABLE")
    if not registered_fallbacks or any(item not in FALLBACKS for item in registered_fallbacks):
        raise TurnContractError("no registered finite fallback")
    return registered_fallbacks[0]
