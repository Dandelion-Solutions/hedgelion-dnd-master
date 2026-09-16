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
FORBIDDEN_HANDOFF_KEYS = frozenset({"raw_bundle", "context_trace", "hidden_reasoning", "role_frame", "tool_payload"})
FALLBACKS = frozenset({"BLOCKED", "DEGRADED", "CLARIFICATION", "DETERMINISTIC_PATH"})


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
    }


def bind_phase(
    envelope: dict[str, Any], role: str, purpose: str, profile_id: str, bundle_id: str, allowed_results: tuple[str, ...],
) -> dict[str, Any]:
    """Bind one registered role to its independently assembled context basis."""
    if role not in PHASE_RESULT_KINDS:
        raise TurnContractError("unregistered role")
    for label, value in (("purpose", purpose), ("profile_id", profile_id), ("bundle_id", bundle_id)):
        _nonempty_string(value, label)
    if not isinstance(allowed_results, tuple) or any(not isinstance(item, str) or not item for item in allowed_results):
        raise TurnContractError("allowed_results must be a tuple of nonempty strings")
    binding = {
        "purpose": purpose,
        "profile_id": profile_id,
        "bundle_id": bundle_id,
        "allowed_results": list(allowed_results),
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
    bindings = envelope.get("phase_bindings", {})
    matching_roles = [role for role, allowed in PHASE_RESULT_KINDS.items() if kind in allowed and role in bindings]
    if len(matching_roles) != 1:
        raise TurnContractError("result kind is not accepted by exactly one bound phase")
    role = matching_roles[0]
    binding = bindings[role]
    if result.get("purpose") != binding["purpose"]:
        raise TurnContractError("result purpose does not match phase binding")
    if result.get("source_generation") != envelope.get("accepted_frontier"):
        raise TurnContractError("result source_generation does not match accepted frontier")
    accepted = dict(result)
    envelope["accepted_results"][role] = accepted
    return accepted


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


def select_fallback(outcome: str, registered_fallbacks: tuple[str, ...]) -> str:
    """Choose exactly one registered finite fallback for a terminal assembly outcome."""
    if outcome != "UNSATISFIABLE":
        raise TurnContractError("fallback selection requires UNSATISFIABLE")
    if not registered_fallbacks or any(item not in FALLBACKS for item in registered_fallbacks):
        raise TurnContractError("no registered finite fallback")
    return registered_fallbacks[0]
