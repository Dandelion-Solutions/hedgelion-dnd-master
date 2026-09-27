"""Protected player-visible emission for validated Narrator output only."""

from __future__ import annotations

from typing import Any

try:
    from .turn_runtime import (
        RESULT_REQUIRED_FIELDS,
        AcceptedContextBasis,
        ExecutionHandoff,
        TurnContractError,
        current_phase_context_basis,
        current_resolved_response_language,
        is_internal_narration_text,
    )
except ImportError:  # Direct GAME/TOOLS test imports use the module directory on sys.path.
    from turn_runtime import (
        RESULT_REQUIRED_FIELDS,
        AcceptedContextBasis,
        ExecutionHandoff,
        TurnContractError,
        current_phase_context_basis,
        current_resolved_response_language,
        is_internal_narration_text,
    )


INSTRUCTION_OWNER = "AI_REASONING"
FORBIDDEN_VISIBLE_KEYS = frozenset({"context_trace", "tool_payload", "hidden_reasoning", "raw_bundle", "draft"})
_INFORMATION_FAMILIES = frozenset(
    {"information", "world.information", "world.lore_fact"}
)
_KNOWLEDGE_FAMILIES = frozenset({"knowledge", "world.knowledge"})
_DISCLOSURE_FAMILIES = frozenset({"disclosure", "runtime.disclosure"})


class EmissionContractError(ValueError):
    """A value attempted to bypass protected Narrator emission."""


def _validate_narration_shape(result: dict[str, Any], bundle: dict[str, Any]) -> None:
    if not isinstance(result, dict) or not isinstance(bundle, dict):
        raise EmissionContractError("result and bundle must be objects")
    if result.get("kind") != "narration_result" or FORBIDDEN_VISIBLE_KEYS.intersection(
        result
    ):
        raise EmissionContractError("only clean narration_result values are eligible")
    if (
        any(
            not isinstance(result.get(name), str) or not result[name]
            for name in ("recipient_id", "bundle_id", "response_language", "prose")
        )
        or not isinstance(result.get("disclosure_refs"), list)
        or any(
            not isinstance(reference, str) or not reference
            for reference in result["disclosure_refs"]
        )
    ):
        raise EmissionContractError("narration result is incomplete")
    if set(result) != RESULT_REQUIRED_FIELDS["narration_result"]:
        raise EmissionContractError("only clean narration_result values are eligible")
    if is_internal_narration_text(result["prose"]):
        raise EmissionContractError(
            "internal role, status, or fallback token is not narration"
        )
    if result["bundle_id"] != bundle.get("bundle_id") or result[
        "recipient_id"
    ] != bundle.get("recipient_id"):
        raise EmissionContractError("narration recipient or bundle basis is invalid")


def _eligible_context_disclosure_refs(
    basis: AcceptedContextBasis,
) -> frozenset[str]:
    """Project fact refs only from native information packets in this basis."""
    bundle = basis.bundle
    eligible: set[str] = set()
    for field in ("required", "optional"):
        packets = bundle.get(field)
        if not isinstance(packets, list):
            raise EmissionContractError(
                "accepted Context candidate packets are invalid"
            )
        for packet in packets:
            if not isinstance(packet, dict):
                raise EmissionContractError("accepted Context candidate is invalid")
            family = packet.get("owner_family")
            if not isinstance(family, str) or family not in (
                _INFORMATION_FAMILIES | _KNOWLEDGE_FAMILIES | _DISCLOSURE_FAMILIES
            ):
                continue
            payload = packet.get("payload")
            identity = packet.get("owner_identity")
            if not isinstance(payload, dict) or not isinstance(identity, list):
                continue
            fact_id = payload.get("fact_id")
            if not isinstance(fact_id, str) or not fact_id:
                continue
            if family in _INFORMATION_FAMILIES:
                identity_matches = identity == [fact_id]
            elif family in _KNOWLEDGE_FAMILIES:
                identity_matches = (
                    identity == [basis.subject_id, fact_id]
                    and payload.get("knower_id") == basis.subject_id
                )
            else:
                identity_matches = (
                    identity == [basis.recipient_id, fact_id]
                    and payload.get("player_id") == basis.recipient_id
                )
            if identity_matches:
                eligible.add(fact_id)
    return frozenset(eligible)


def validate_narration_result(
    result: dict[str, Any],
    bundle: dict[str, Any],
    *,
    eligible_disclosure_refs: frozenset[str],
) -> dict[str, Any]:
    _validate_narration_shape(result, bundle)
    if not set(result["disclosure_refs"]).issubset(eligible_disclosure_refs):
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
    _validate_narration_shape(result, bundle)
    if envelope is None:
        raise EmissionContractError("protected emission envelope is required")
    if not isinstance(envelope, dict):
        raise EmissionContractError("emission envelope must be an object")
    accepted_results = envelope.get("accepted_results")
    phase_bindings = envelope.get("phase_bindings")
    narrator_binding = phase_bindings.get("NARRATOR") if isinstance(phase_bindings, dict) else None
    if not isinstance(accepted_results, dict) or not isinstance(narrator_binding, dict):
        raise EmissionContractError("emission envelope is missing the bound Narrator phase")
    try:
        response_language = current_resolved_response_language(
            envelope, narrator_binding
        )
    except TurnContractError as exc:
        raise EmissionContractError(
            f"Narrator response language basis is invalid: {exc}"
        ) from exc
    try:
        context_basis = current_phase_context_basis(envelope, "NARRATOR")
    except TurnContractError as exc:
        raise EmissionContractError(
            f"accepted Narrator Context basis is invalid: {exc}"
        ) from exc
    if (
        bundle.get("bundle_id") != context_basis.bundle_id
        or bundle.get("recipient_id") != context_basis.recipient_id
    ):
        raise EmissionContractError("narration recipient or bundle basis is invalid")
    valid = validate_narration_result(
        result,
        bundle,
        eligible_disclosure_refs=_eligible_context_disclosure_refs(context_basis),
    )
    payload = {
        "recipient_id": valid["recipient_id"],
        "response_language": valid["response_language"],
        "prose": valid["prose"],
        "disclosure_refs": list(valid["disclosure_refs"]),
    }
    if valid["response_language"] != response_language:
        raise EmissionContractError(
            "narration response language differs from the current Narrator basis"
        )
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
