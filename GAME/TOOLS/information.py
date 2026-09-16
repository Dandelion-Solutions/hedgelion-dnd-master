#!/usr/bin/env python3
"""Owner-native normalization for HDM lore, knowledge, disclosure, and messages.

This module validates only the typed input supplied by its caller.  It does not
discover evidence, infer knowledge from visibility, or read caches/indexes.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from typing import Final


TRUTH_STATUSES: Final = frozenset(
    {"truth.undetermined", "truth.established", "truth.disproven"}
)
LORE_RECORD_STATUSES: Final = frozenset({"lore_record.active", "lore_record.superseded"})
EPISTEMIC_STANCES: Final = frozenset(
    {
        "epistemic.aware",
        "epistemic.known",
        "epistemic.believed",
        "epistemic.suspected",
        "epistemic.rejected",
    }
)
DISCLOSURE_ASPECTS: Final = frozenset(
    {"disclosure.statement", "disclosure.objective_status"}
)


class InformationContractError(ValueError):
    """Raised when caller-supplied information violates a native contract."""


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise InformationContractError(f"{label} must be an object")
    return value


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise InformationContractError(f"{label} must be a nonempty string")
    return value


def _optional_nonempty_string(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, label)


def _accepted_source_refs(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise InformationContractError("supporting_source_refs must be an array")
    source_refs = [_require_nonempty_string(source_ref, "source reference") for source_ref in value]
    if not source_refs:
        raise InformationContractError("knowledge requires accepted native evidence")
    if len(source_refs) != len(set(source_refs)):
        raise InformationContractError("supporting_source_refs are ambiguous")
    return source_refs


def _validate_source_evidence(
    source_refs: list[str], source_evidence: object, knower_id: str
) -> None:
    if not isinstance(source_evidence, Sequence) or isinstance(source_evidence, str):
        raise InformationContractError("knowledge requires accepted native evidence")
    evidence_by_ref: dict[str, Mapping[str, object]] = {}
    for raw_evidence in source_evidence:
        evidence = _require_mapping(raw_evidence, "source evidence")
        ref = _require_nonempty_string(evidence.get("ref"), "source evidence ref")
        if ref in evidence_by_ref:
            raise InformationContractError("source_evidence is ambiguous")
        current = evidence.get("current")
        if not isinstance(current, bool):
            raise InformationContractError("source evidence currentness must be boolean")
        if evidence.get("accepted") is not True:
            raise InformationContractError("knowledge requires accepted native evidence")
        authorized_knowers = evidence.get("authorized_knower_ids")
        if not isinstance(authorized_knowers, Sequence) or isinstance(authorized_knowers, str):
            raise InformationContractError("authorized_knower_ids must be an array")
        evidence_by_ref[ref] = evidence
    for source_ref in source_refs:
        evidence = evidence_by_ref.get(source_ref)
        if evidence is None:
            raise InformationContractError("knowledge evidence is missing")
        if evidence["current"] is not True:
            raise InformationContractError("knowledge evidence is stale")
        authorized_knowers = evidence["authorized_knower_ids"]
        if knower_id not in authorized_knowers:
            raise InformationContractError("knowledge evidence is unauthorized")


def _validate_disclosure_source_evidence(source_refs: list[str], source_evidence: object) -> None:
    if not isinstance(source_evidence, Sequence) or isinstance(source_evidence, str):
        raise InformationContractError("disclosure requires accepted native evidence")
    evidence_by_ref: dict[str, Mapping[str, object]] = {}
    for raw_evidence in source_evidence:
        evidence = _require_mapping(raw_evidence, "disclosure source evidence")
        ref = _require_nonempty_string(evidence.get("ref"), "disclosure source evidence ref")
        if ref in evidence_by_ref:
            raise InformationContractError("disclosure source evidence is ambiguous")
        if evidence.get("accepted") is not True or evidence.get("current") is not True:
            raise InformationContractError("disclosure requires accepted native evidence")
        evidence_by_ref[ref] = evidence
    if any(source_ref not in evidence_by_ref for source_ref in source_refs):
        raise InformationContractError("disclosure requires accepted native evidence")


def _validated_fact(value: object) -> dict[str, object]:
    fact = _require_mapping(value, "fact")
    fact_id = _require_nonempty_string(fact.get("fact_id"), "fact_id")
    statement = _require_nonempty_string(fact.get("statement"), "statement")
    truth_status = _require_nonempty_string(fact.get("truth_status"), "truth_status")
    record_status = _require_nonempty_string(fact.get("record_status"), "record_status")
    if truth_status not in TRUTH_STATUSES:
        raise InformationContractError("unsupported truth_status")
    if record_status not in LORE_RECORD_STATUSES:
        raise InformationContractError("unsupported record_status")
    provenance_refs = fact.get("provenance_refs", [])
    if not isinstance(provenance_refs, Sequence) or isinstance(provenance_refs, str):
        raise InformationContractError("provenance_refs must be an array")
    normalized_provenance = [
        _require_nonempty_string(reference, "provenance reference") for reference in provenance_refs
    ]
    if len(normalized_provenance) != len(set(normalized_provenance)):
        raise InformationContractError("provenance_refs are ambiguous")
    last_transition = _optional_nonempty_string(
        fact.get("last_truth_transition_ref"), "last_truth_transition_ref"
    )
    result: dict[str, object] = {
        "fact_id": fact_id,
        "statement": statement,
        "truth_status": truth_status,
        "record_status": record_status,
        "provenance_refs": normalized_provenance,
    }
    if last_transition is not None:
        result["last_truth_transition_ref"] = last_transition
    return result


def validate_knowledge_transition(value: object) -> dict[str, object]:
    """Validate one current `(knower_id, fact_id)` epistemic relation."""

    knowledge = _require_mapping(value, "knowledge")
    knower_id = _require_nonempty_string(knowledge.get("knower_id"), "knower_id")
    fact_id = _require_nonempty_string(knowledge.get("fact_id"), "fact_id")
    stance = _require_nonempty_string(knowledge.get("stance"), "stance")
    if stance not in EPISTEMIC_STANCES:
        raise InformationContractError("unsupported epistemic stance")
    source_refs = _accepted_source_refs(knowledge.get("supporting_source_refs"))
    _validate_source_evidence(source_refs, knowledge.get("source_evidence"), knower_id)
    result: dict[str, object] = {
        "knower_id": knower_id,
        "fact_id": fact_id,
        "stance": stance,
        "supporting_source_refs": source_refs,
    }
    last_changed = _optional_nonempty_string(
        knowledge.get("last_changed_event_id"), "last_changed_event_id"
    )
    if last_changed is not None:
        result["last_changed_event_id"] = last_changed
    if "confidence" in knowledge:
        confidence = knowledge["confidence"]
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            raise InformationContractError("confidence must be a number")
        result["confidence"] = confidence
    return result


def normalize_embedded_epistemic_input(value: object) -> dict[str, object]:
    """Normalize an explicit legacy evidence input without making it an owner.

    Legacy visibility, cache, and narration fields are intentionally not accepted
    as epistemic evidence.  Callers must supply accepted native evidence refs.
    """

    embedded = _require_mapping(value, "embedded epistemic input")
    forbidden = {"visibility", "visible_to", "cache_ref", "narration", "knowledge"}
    if forbidden.intersection(embedded):
        raise InformationContractError("embedded visibility is not accepted native evidence")
    return validate_knowledge_transition(embedded)


def _normalize_emission(value: object) -> dict[str, object]:
    emission = _require_mapping(value, "emission")
    recipient_player_id = _require_nonempty_string(
        emission.get("recipient_player_id"), "recipient_player_id"
    )
    message_id = _require_nonempty_string(emission.get("message_id"), "message_id")
    interaction_id = _require_nonempty_string(emission.get("interaction_id"), "interaction_id")
    text = _require_nonempty_string(emission.get("text"), "text")
    disclosure_refs = emission.get("disclosure_refs", [])
    if not isinstance(disclosure_refs, Sequence) or isinstance(disclosure_refs, str):
        raise InformationContractError("disclosure_refs must be an array")

    statement_exposed = False
    truth_transition_ref: str | None = None
    disclosure_evidence: list[tuple[str, str, str, str | None]] = []
    fact_ids: list[str] = []
    for raw_ref in disclosure_refs:
        disclosure_ref = _require_mapping(raw_ref, "disclosure reference")
        ref_recipient = disclosure_ref.get("player_id", recipient_player_id)
        if ref_recipient != recipient_player_id:
            raise InformationContractError("disclosure recipient does not match message recipient")
        fact_id = _require_nonempty_string(disclosure_ref.get("fact_id"), "disclosure fact_id")
        aspect = _require_nonempty_string(disclosure_ref.get("aspect"), "disclosure aspect")
        if aspect not in DISCLOSURE_ASPECTS:
            raise InformationContractError("unsupported disclosure aspect")
        source_ref = _require_nonempty_string(disclosure_ref.get("source_ref"), "disclosure source_ref")
        disclosure_transition: str | None = None
        if aspect == "disclosure.objective_status":
            disclosure_transition = _require_nonempty_string(
                disclosure_ref.get("truth_transition_ref"), "truth_transition_ref"
            )
            if truth_transition_ref is not None and truth_transition_ref != disclosure_transition:
                raise InformationContractError("disclosure truth-transition evidence is ambiguous")
            truth_transition_ref = disclosure_transition
        else:
            statement_exposed = True
        fact_ids.append(fact_id)
        disclosure_evidence.append((fact_id, aspect, source_ref, disclosure_transition))

    if len(set(fact_ids)) > 1:
        raise InformationContractError("one disclosure relation must have one fact_id")
    if len(disclosure_evidence) != len(set(disclosure_evidence)):
        raise InformationContractError("disclosure source evidence is ambiguous")
    _validate_disclosure_source_evidence(
        list(dict.fromkeys(reference[2] for reference in disclosure_evidence)),
        emission.get("source_evidence"),
    )

    message = {
        "message_id": message_id,
        "interaction_id": interaction_id,
        "direction": "outbound",
        "recipient_player_id": recipient_player_id,
        "payload_state": "message.exact_retained",
        "content_digest": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "exact_text": text,
    }
    if not fact_ids:
        return {"message": message}
    disclosure: dict[str, object] = {
        "player_id": recipient_player_id,
        "fact_id": fact_ids[0],
        "statement_exposed": statement_exposed,
        "source_refs": list(dict.fromkeys(reference[2] for reference in disclosure_evidence)),
        "last_disclosed_interaction_id": interaction_id,
        "message_id": message_id,
    }
    if truth_transition_ref is not None:
        disclosure["latest_exposed_truth_transition_ref"] = truth_transition_ref
    return {"message": message, "disclosure": disclosure}


def normalize_live_material_evidence(value: object) -> dict[str, object]:
    """Normalize one recipient-bound outbound closure without LIVE state joining."""

    return _normalize_emission(value)


def normalize_information_evidence(value: object) -> dict[str, object]:
    """Validate a bounded native information closure supplied by an owner."""

    evidence = _require_mapping(value, "information evidence")
    fact = _validated_fact(evidence.get("fact"))
    knowledge = validate_knowledge_transition(evidence.get("knowledge"))
    if knowledge["fact_id"] != fact["fact_id"]:
        raise InformationContractError("knowledge fact_id does not match native lore fact")
    emission = _normalize_emission(evidence.get("emission"))
    disclosure = emission.get("disclosure")
    if disclosure is not None and disclosure["fact_id"] != fact["fact_id"]:
        raise InformationContractError("disclosure fact_id does not match native lore fact")
    return {"lore_fact": fact, "knowledge": knowledge, **emission}
