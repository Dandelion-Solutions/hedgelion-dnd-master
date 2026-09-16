"""Protected player-visible emission for validated Narrator output only."""

from __future__ import annotations

from typing import Any


INSTRUCTION_OWNER = "AI_REASONING"
FORBIDDEN_VISIBLE_KEYS = frozenset({"context_trace", "tool_payload", "hidden_reasoning", "raw_bundle", "draft"})


class EmissionContractError(ValueError):
    """A value attempted to bypass protected Narrator emission."""


def validate_narration_result(result: dict[str, Any], bundle: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict) or not isinstance(bundle, dict):
        raise EmissionContractError("result and bundle must be objects")
    if result.get("kind") != "narration_result" or FORBIDDEN_VISIBLE_KEYS.intersection(result):
        raise EmissionContractError("only clean narration_result values are eligible")
    required = ("recipient_id", "bundle_id", "prose", "disclosure_refs")
    if any(not result.get(name) for name in required[:3]) or not isinstance(result.get("disclosure_refs"), list):
        raise EmissionContractError("narration result is incomplete")
    if result["bundle_id"] != bundle.get("bundle_id") or result["recipient_id"] != bundle.get("recipient_id"):
        raise EmissionContractError("narration recipient or bundle basis is invalid")
    allowed = bundle.get("disclosure_refs")
    if not isinstance(allowed, list) or not set(result["disclosure_refs"]).issubset(allowed):
        raise EmissionContractError("narration disclosure is not recipient-eligible")
    return result


def commit_visible_payload(result: dict[str, Any], bundle: dict[str, Any], instruction_owner: str) -> dict[str, Any]:
    """Project validated Narrator content to the sole ordinary visible surface."""
    if instruction_owner != INSTRUCTION_OWNER:
        raise EmissionContractError("unowned ordinary emission")
    valid = validate_narration_result(result, bundle)
    return {
        "recipient_id": valid["recipient_id"],
        "prose": valid["prose"],
        "disclosure_refs": list(valid["disclosure_refs"]),
    }
