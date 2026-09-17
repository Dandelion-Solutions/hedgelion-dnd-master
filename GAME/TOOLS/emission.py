"""Protected player-visible emission for validated Narrator output only."""

from __future__ import annotations

from typing import Any

try:
    from .turn_runtime import ExecutionHandoff
except ImportError:  # Direct GAME/TOOLS test imports use the module directory on sys.path.
    from turn_runtime import ExecutionHandoff


INSTRUCTION_OWNER = "AI_REASONING"
FORBIDDEN_VISIBLE_KEYS = frozenset({"context_trace", "tool_payload", "hidden_reasoning", "raw_bundle", "draft"})


class EmissionContractError(ValueError):
    """A value attempted to bypass protected Narrator emission."""


def validate_narration_result(result: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict) or not isinstance(bundle, dict):
        raise EmissionContractError("result and bundle must be objects")
    if result.get("kind") != "narration_result" or FORBIDDEN_VISIBLE_KEYS.intersection(result):
        raise EmissionContractError("only clean narration_result values are eligible")
    if (
        any(
            not isinstance(result.get(name), str) or not result[name]
            for name in ("recipient_id", "bundle_id", "prose")
        )
        or not isinstance(result.get("disclosure_refs"), list)
        or any(
            not isinstance(reference, str) or not reference
            for reference in result["disclosure_refs"]
        )
    ):
        raise EmissionContractError("narration result is incomplete")
    if result["bundle_id"] != bundle.get("bundle_id") or result["recipient_id"] != bundle.get("recipient_id"):
        raise EmissionContractError("narration recipient or bundle basis is invalid")
    allowed = bundle.get("disclosure_refs")
    if not isinstance(allowed, list) or not set(result["disclosure_refs"]).issubset(allowed):
        raise EmissionContractError("narration disclosure is not recipient-eligible")
    return result


def commit_visible_payload(
    result: dict[str, Any],
    bundle: dict[str, Any],
    instruction_owner: str,
    *,
    envelope: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Project validated Narrator content to the sole ordinary visible surface."""
    if instruction_owner != INSTRUCTION_OWNER:
        raise EmissionContractError("unowned ordinary emission")
    valid = validate_narration_result(result, bundle)
    payload = {
        "recipient_id": valid["recipient_id"],
        "prose": valid["prose"],
        "disclosure_refs": list(valid["disclosure_refs"]),
    }
    if envelope is None:
        raise EmissionContractError("protected emission envelope is required")
    if not isinstance(envelope, dict):
        raise EmissionContractError("emission envelope must be an object")
    accepted_results = envelope.get("accepted_results")
    phase_bindings = envelope.get("phase_bindings")
    narrator_binding = phase_bindings.get("NARRATOR") if isinstance(phase_bindings, dict) else None
    if not isinstance(accepted_results, dict) or not isinstance(narrator_binding, dict):
        raise EmissionContractError("emission envelope is missing the bound Narrator phase")
    allowed_results = narrator_binding.get("allowed_results")
    if not isinstance(allowed_results, list) or "narration_result" not in allowed_results:
        raise EmissionContractError("emission envelope does not admit Narrator results")
    if narrator_binding.get("bundle_id") != valid["bundle_id"]:
        raise EmissionContractError("emission envelope Narrator bundle is invalid")
    if narrator_binding.get("recipient_id") != valid["recipient_id"]:
        raise EmissionContractError("emission envelope Narrator recipient is invalid")
    if accepted_results.get("NARRATOR") != valid:
        raise EmissionContractError("narration result was not accepted by the Narrator phase")
    allowed_handoffs = narrator_binding.get("allowed_handoffs", [])
    if not isinstance(allowed_handoffs, list):
        raise EmissionContractError("emission envelope has invalid handoff scope")
    if "execution_result" in allowed_handoffs:
        accepted_handoffs = envelope.get("accepted_handoffs")
        narrator_handoffs = accepted_handoffs.get("NARRATOR") if isinstance(accepted_handoffs, dict) else None
        if not isinstance(narrator_handoffs, list) or not any(
            isinstance(handoff, ExecutionHandoff)
            and handoff.turn_id == envelope.get("turn_id")
            and handoff.recipient_role == "NARRATOR"
            and handoff.bundle_id == valid["bundle_id"]
            and handoff.recipient_id == valid["recipient_id"]
            for handoff in narrator_handoffs
        ):
            raise EmissionContractError("owner-verified execution handoff is required before emission")
    if "remaining_narrator_capacity" not in envelope or "emitted_payload" not in envelope:
        raise EmissionContractError("emission envelope is missing protected capacity state")
    if envelope["emitted_payload"] is not None:
        raise EmissionContractError("ordinary visible emission is already committed")
    remaining = envelope.get("remaining_narrator_capacity")
    if isinstance(remaining, bool) or not isinstance(remaining, int) or remaining < 0:
        raise EmissionContractError("emission envelope has invalid protected capacity")
    required_capacity = len(valid["prose"].encode("utf-8"))
    if required_capacity > remaining:
        raise EmissionContractError("narration exceeds protected capacity")
    envelope["remaining_narrator_capacity"] = remaining - required_capacity
    envelope["emitted_payload"] = dict(payload)
    return payload
