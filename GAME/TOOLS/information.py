#!/usr/bin/env python3
"""Owner-native normalization for HDM lore, knowledge, disclosure, and messages.

This module validates only the typed input supplied by its caller.  It does not
discover evidence, infer knowledge from visibility, or read caches/indexes.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .live_state import LiveEnvelope


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
NATIVE_ID_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


class InformationContractError(ValueError):
    """Raised when caller-supplied information violates a native contract."""


def _live_source_key(value: object, label: str) -> tuple[str, str, str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise InformationContractError(f"{label} must be (campaign_id, scene_id, epoch_id)")
    if len(value) != 3 or any(not isinstance(item, str) or not item for item in value):
        raise InformationContractError(f"{label} must contain three nonempty source IDs")
    return value[0], value[1], value[2]  # type: ignore[return-value]


def _live_source_native_ids(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise InformationContractError(f"{label} must be an array")
    result = tuple(_require_native_id(item, f"{label} item") for item in value)
    if len(result) != len(set(result)):
        raise InformationContractError(f"{label} must contain unique IDs")
    return result


@dataclass(frozen=True, slots=True)
class LiveInformationCandidate:
    """Ephemeral, source-bound request data for native-owner normalization.

    Candidate fields are untrusted transport data.  Normalization re-runs the
    canonical exact-current extraction and never treats candidate evidence as
    authoritative.
    """

    source_key: tuple[str, str, str]
    source_ref: str
    source_revision: str
    source_native_ids: tuple[str, ...]
    recipient_player_id: str
    evidence: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_key",
            _live_source_key(self.source_key, "candidate source_key"),
        )
        object.__setattr__(
            self,
            "source_ref",
            _require_nonempty_string(self.source_ref, "candidate source_ref"),
        )
        object.__setattr__(
            self,
            "source_revision",
            _require_nonempty_string(self.source_revision, "candidate source_revision"),
        )
        object.__setattr__(
            self,
            "source_native_ids",
            _live_source_native_ids(self.source_native_ids, "candidate source_native_ids"),
        )
        object.__setattr__(
            self,
            "recipient_player_id",
            _require_native_id(self.recipient_player_id, "candidate recipient_player_id"),
        )
        evidence = _require_mapping(self.evidence, "candidate evidence")
        object.__setattr__(self, "evidence", deepcopy(dict(evidence)))

    def as_mapping(self) -> dict[str, object]:
        return {
            "source_key": list(self.source_key),
            "source_ref": self.source_ref,
            "source_revision": self.source_revision,
            "source_native_ids": list(self.source_native_ids),
            "recipient_player_id": self.recipient_player_id,
            "evidence": deepcopy(dict(self.evidence)),
        }


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise InformationContractError(f"{label} must be an object")
    return value


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise InformationContractError(f"{label} must be a nonempty string")
    return value


def _require_native_id(value: object, label: str) -> str:
    identifier = _require_nonempty_string(value, label)
    if NATIVE_ID_PATTERN.fullmatch(identifier) is None:
        raise InformationContractError(f"{label} must be a schema-compatible native id")
    return identifier


def _optional_native_id(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _require_native_id(value, label)


def _accepted_source_refs(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise InformationContractError("supporting_source_refs must be an array")
    source_refs = [_require_native_id(source_ref, "source reference") for source_ref in value]
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


def _validate_disclosure_source_evidence(
    source_refs: list[str], source_evidence: object
) -> dict[str, Mapping[str, object]]:
    if not isinstance(source_evidence, Sequence) or isinstance(source_evidence, str):
        raise InformationContractError("disclosure requires accepted native evidence")
    evidence_by_ref: dict[str, Mapping[str, object]] = {}
    for raw_evidence in source_evidence:
        evidence = _require_mapping(raw_evidence, "disclosure source evidence")
        ref = _require_native_id(evidence.get("ref"), "disclosure source evidence ref")
        if ref in evidence_by_ref:
            raise InformationContractError("disclosure source evidence is ambiguous")
        if evidence.get("accepted") is not True or evidence.get("current") is not True:
            raise InformationContractError("disclosure requires accepted native evidence")
        evidence_by_ref[ref] = evidence
    if any(source_ref not in evidence_by_ref for source_ref in source_refs):
        raise InformationContractError("disclosure requires accepted native evidence")
    return evidence_by_ref


def _validated_fact(value: object) -> dict[str, object]:
    fact = _require_mapping(value, "fact")
    fact_id = _require_native_id(fact.get("fact_id"), "fact_id")
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
        _require_native_id(reference, "provenance reference") for reference in provenance_refs
    ]
    if len(normalized_provenance) != len(set(normalized_provenance)):
        raise InformationContractError("provenance_refs are ambiguous")
    last_transition = _optional_native_id(
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
    knower_id = _require_native_id(knowledge.get("knower_id"), "knower_id")
    fact_id = _require_native_id(knowledge.get("fact_id"), "fact_id")
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
    last_changed = _optional_native_id(
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
    recipient_player_id = _require_native_id(
        emission.get("recipient_player_id"), "recipient_player_id"
    )
    message_id = _require_native_id(emission.get("message_id"), "message_id")
    interaction_id = _require_native_id(emission.get("interaction_id"), "interaction_id")
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
        fact_id = _require_native_id(disclosure_ref.get("fact_id"), "disclosure fact_id")
        aspect = _require_nonempty_string(disclosure_ref.get("aspect"), "disclosure aspect")
        if aspect not in DISCLOSURE_ASPECTS:
            raise InformationContractError("unsupported disclosure aspect")
        source_ref = _require_native_id(disclosure_ref.get("source_ref"), "disclosure source_ref")
        disclosure_transition: str | None = None
        if aspect == "disclosure.objective_status":
            disclosure_transition = _require_native_id(
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
    evidence_by_ref = _validate_disclosure_source_evidence(
        list(dict.fromkeys(reference[2] for reference in disclosure_evidence)),
        emission.get("source_evidence"),
    )
    for fact_id, aspect, source_ref, disclosure_transition in disclosure_evidence:
        if aspect != "disclosure.objective_status":
            continue
        evidence = evidence_by_ref[source_ref]
        evidence_fact_id = _require_native_id(
            evidence.get("fact_id"), "truth-transition evidence fact_id"
        )
        evidence_transition = _require_native_id(
            evidence.get("truth_transition_ref"), "truth-transition evidence ref"
        )
        if evidence_fact_id != fact_id or evidence_transition != disclosure_transition:
            raise InformationContractError(
                "truth-transition evidence does not bind to the disclosed fact"
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


def _selected_live_source(selected_route: object, value: object) -> LiveEnvelope:
    """Require one owner-typed source selected by the complete LIVE route."""

    from .live_state import LiveEnvelope, LiveLifecycle
    from .live_state import LiveContractError, require_selected_live_source

    if not isinstance(value, LiveEnvelope):
        raise InformationContractError("LIVE information requires the exact selected source")
    try:
        selected = require_selected_live_source(selected_route, value)
    except LiveContractError as error:
        raise InformationContractError(str(error)) from error
    if selected.status is LiveLifecycle.ABSORBED:
        raise InformationContractError("absorbed LIVE source is not current information authority")
    return selected


def _projection_candidates(projection: Mapping[str, object]) -> object:
    direct = projection.get("information_candidates")
    if direct is not None:
        return direct
    material = projection.get("material")
    if isinstance(material, Mapping) and "information_candidates" in material:
        return material["information_candidates"]
    raise InformationContractError(
        "LIVE projection requires owner-local information_candidates; no legacy fallback"
    )


def extract_material_live_information(
    selected_route: object,
    live_source: object,
    projection: object,
    *,
    recipient_player_id: str,
) -> tuple[LiveInformationCandidate, ...]:
    """Extract candidates from one source selected by an exact LIVE route.

    LIVE physical fields are evidence/input only.  This function does not infer
    knowledge from visibility or emit any native owner record; the returned
    candidates must pass through :func:`apply_normalization_candidates_under_native_owners`.
    """

    source = _selected_live_source(selected_route, live_source)
    recipient = _require_native_id(recipient_player_id, "recipient_player_id")
    raw_projection = _require_mapping(projection, "LIVE information projection")
    forbidden_projection_fields = {
        "epoch_id",
        "live_branch",
        "live_head_sha",
        "revision",
        "base_campaign_sha",
        "known_by_pc_ids",
        "perceived_by_pc_ids",
        "visible_to",
        "authority",
    }
    if forbidden_projection_fields.intersection(raw_projection):
        raise InformationContractError(
            "legacy LIVE projection fields cannot become information authority"
        )
    required_fields = {
        "source_key",
        "source_ref",
        "source_revision",
        "source_native_ids",
    }
    missing = required_fields.difference(raw_projection)
    if missing:
        raise InformationContractError(
            "LIVE information projection is missing exact current fields: "
            + ", ".join(sorted(missing))
        )
    if _live_source_key(raw_projection["source_key"], "projection source_key") != source.source_key:
        raise InformationContractError("LIVE information projection is stale or bound to another source")
    if raw_projection["source_ref"] != source.source_ref:
        raise InformationContractError("LIVE information projection source_ref is not current")
    if raw_projection["source_revision"] != source.source_revision:
        raise InformationContractError("LIVE information projection source_revision is stale")
    if _live_source_native_ids(
        raw_projection["source_native_ids"], "projection source_native_ids"
    ) != source.source_native_ids:
        raise InformationContractError("LIVE information projection source-native history is stale")

    raw_candidates = _projection_candidates(raw_projection)
    if not isinstance(raw_candidates, Sequence) or isinstance(raw_candidates, (str, bytes)):
        raise InformationContractError("information_candidates must be an array")

    result: list[LiveInformationCandidate] = []
    for raw_candidate in raw_candidates:
        candidate = _require_mapping(raw_candidate, "LIVE information candidate")
        if set(candidate) == {"recipient_player_id", "evidence"}:
            evidence = candidate["evidence"]
        else:
            allowed_direct = {"recipient_player_id", "fact", "knowledge", "emission"}
            if set(candidate).issubset(allowed_direct) and "recipient_player_id" in candidate:
                evidence = {key: value for key, value in candidate.items() if key != "recipient_player_id"}
            else:
                raise InformationContractError(
                    "LIVE information candidate must use the native evidence shape"
                )
        candidate_recipient = _require_native_id(
            candidate.get("recipient_player_id"), "candidate recipient_player_id"
        )
        if candidate_recipient != recipient:
            raise InformationContractError("LIVE information candidate recipient leakage")
        native_evidence = _require_mapping(evidence, "LIVE information candidate evidence")
        if {
            "known_by_pc_ids",
            "perceived_by_pc_ids",
            "visibility",
            "visible_to",
            "cache_ref",
            "narration",
            "live_facts",
            "observable_events",
        }.intersection(native_evidence):
            raise InformationContractError(
                "legacy visibility/perception fields are not accepted native evidence"
            )
        emission = _require_mapping(native_evidence.get("emission"), "candidate emission")
        if emission.get("recipient_player_id") != recipient:
            raise InformationContractError("LIVE information emission recipient leakage")
        candidate_value = LiveInformationCandidate(
            source_key=source.source_key,
            source_ref=source.source_ref,
            source_revision=source.source_revision,
            source_native_ids=source.source_native_ids,
            recipient_player_id=recipient,
            evidence=native_evidence,
        )
        result.append(candidate_value)
    return tuple(result)


def apply_normalization_candidates_under_native_owners(
    candidates: object,
    selected_route: object,
    current_source: object,
    projection: object,
    *,
    recipient_player_id: str | None = None,
) -> tuple[dict[str, object], ...]:
    """Normalize exact-route LIVE information through native owners.

    Candidate values are untrusted request/comparison data only.  The canonical
    exact-current extraction is re-run from the owner-supplied projection and
    only that fresh evidence reaches the native information normalizers.  The
    operation is deliberately ephemeral: it returns native-owner inputs and
    never writes, merges, or promotes LIVE physical projections into authority.
    """

    source = _selected_live_source(selected_route, current_source)
    if not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes)):
        raise InformationContractError("normalization candidates must be a typed array")
    expected_recipient = (
        _require_native_id(recipient_player_id, "recipient_player_id")
        if recipient_player_id is not None
        else None
    )
    if expected_recipient is None:
        raise InformationContractError(
            "normalization requires an explicit recipient for owner-side LIVE extraction"
        )

    requested_candidates: list[LiveInformationCandidate] = []
    for candidate in candidates:
        if not isinstance(candidate, LiveInformationCandidate):
            raise InformationContractError(
                "normalization candidates must be typed request data"
            )
        if (
            candidate.source_key != source.source_key
            or candidate.source_ref != source.source_ref
            or candidate.source_revision != source.source_revision
            or candidate.source_native_ids != source.source_native_ids
        ):
            raise InformationContractError("normalization candidate is stale for current LIVE source")
        if candidate.recipient_player_id != expected_recipient:
            raise InformationContractError("normalization candidate recipient leakage")
        requested_candidates.append(candidate)

    extracted_candidates = extract_material_live_information(
        selected_route,
        current_source,
        projection,
        recipient_player_id=expected_recipient,
    )
    if len(requested_candidates) != len(extracted_candidates):
        raise InformationContractError(
            "normalization candidate request does not match fresh LIVE extraction"
        )

    normalized: list[dict[str, object]] = []
    seen_relations: set[tuple[str, str, str]] = set()
    for candidate in extracted_candidates:
        result = normalize_information_evidence(candidate.evidence)
        message_recipient = result["message"]["recipient_player_id"]
        if message_recipient != candidate.recipient_player_id:
            raise InformationContractError("normalized message recipient does not match candidate")
        relation = (
            result["knowledge"]["knower_id"],
            result["knowledge"]["fact_id"],
            message_recipient,
        )
        if relation in seen_relations:
            raise InformationContractError("normalization candidates contain an ambiguous native relation")
        seen_relations.add(relation)
        normalized.append(result)
    return tuple(normalized)
