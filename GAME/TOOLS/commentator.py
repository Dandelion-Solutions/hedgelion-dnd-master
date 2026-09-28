"""Self-contained, read-only Commentator projection and pre-materialization filter."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Final

from GAME.TOOLS.story import StoryContractError, validate_story_projection

_CONTROL_SCHEMA_VERSION: Final = 2
_SNAPSHOT_SCHEMA_VERSION: Final = 2
_CONTEXT_PROFILE_ID: Final = "profile.commentator_control"
_CONTEXT_EVIDENCE_FAMILIES: Final[frozenset[str]] = frozenset(
    {"world.player", "world.knowledge", "runtime.disclosure", "world.lore_fact"}
)
_ANCHOR_FAMILIES: Final[frozenset[str]] = frozenset(
    {"world.knowledge", "world.lore_fact"}
)
_EPISTEMIC_STANCES: Final[frozenset[str]] = frozenset(
    {
        "epistemic.aware",
        "epistemic.known",
        "epistemic.believed",
        "epistemic.suspected",
        "epistemic.rejected",
    }
)
_OBJECTIVE_TRUTH_STATUSES: Final[frozenset[str]] = frozenset(
    {"truth.undetermined", "truth.established", "truth.disproven"}
)


class CommentatorContractError(ValueError):
    """Raised for malformed self-contained Commentator control material."""


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CommentatorContractError(f"{label} must be a nonempty string")
    return value


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CommentatorContractError(f"{label} must be an object")
    return value


def _string_array(
    value: object, label: str, *, expected_length: int | None = None
) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise CommentatorContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if len(items) != len(set(items)):
        raise CommentatorContractError(f"{label} must be unique")
    if expected_length is not None and len(items) != expected_length:
        raise CommentatorContractError(
            f"{label} must contain exactly {expected_length} item(s)"
        )
    return items


def _validate_owner_evidence(
    family: object, identity_value: object, payload_value: object
) -> dict[str, object]:
    owner_family = _nonempty_string(family, "owner_family")
    if owner_family not in _CONTEXT_EVIDENCE_FAMILIES:
        raise CommentatorContractError("Context evidence family is not admitted")
    identity_length = 1 if owner_family in {"world.player", "world.lore_fact"} else 2
    identity = _string_array(
        identity_value, "owner_identity", expected_length=identity_length
    )
    payload = _mapping(payload_value, "native owner payload")

    if owner_family == "world.player":
        player_id = identity[0]
        controlled_pc_ids = _string_array(
            payload.get("controlled_pc_ids"), "controlled_pc_ids"
        )
        if (
            payload.get("id") != player_id
            or payload.get("player_id") != player_id
            or payload.get("status") != "active"
        ):
            raise CommentatorContractError(
                "PLAYER evidence does not match its exact active identity"
            )
        normalized_payload = deepcopy(dict(payload))
        normalized_payload["controlled_pc_ids"] = controlled_pc_ids
    elif owner_family == "world.knowledge":
        stance = payload.get("stance")
        if (
            payload.get("knower_id") != identity[0]
            or payload.get("fact_id") != identity[1]
            or not isinstance(stance, str)
            or stance not in _EPISTEMIC_STANCES
        ):
            raise CommentatorContractError(
                "knowledge evidence does not match its exact owner identity"
            )
        normalized_payload = deepcopy(dict(payload))
    elif owner_family == "runtime.disclosure":
        if (
            payload.get("player_id") != identity[0]
            or payload.get("fact_id") != identity[1]
            or not isinstance(payload.get("statement_exposed"), bool)
        ):
            raise CommentatorContractError(
                "disclosure evidence does not match its exact owner identity"
            )
        normalized_payload = deepcopy(dict(payload))
    else:
        state = payload.get("state")
        if payload.get("id") != identity[0] or (
            isinstance(state, Mapping)
            and state.get("fact_id") not in (None, identity[0])
        ):
            raise CommentatorContractError(
                "lore-fact evidence does not match its exact owner identity"
            )
        normalized_payload = deepcopy(dict(payload))

    return {
        "owner_family": owner_family,
        "owner_identity": identity,
        "payload": normalized_payload,
    }


def _evidence_key(evidence: Mapping[str, object]) -> tuple[str, tuple[str, ...]]:
    identity = evidence["owner_identity"]
    assert isinstance(identity, list)
    return str(evidence["owner_family"]), tuple(identity)


def _validate_control_projection(value: object) -> dict[str, object]:
    projection = _mapping(value, "Commentator control projection")
    allowed_fields = {
        "schema_version",
        "reader_id",
        "player_id",
        "selected_pc_id",
        "evidence",
    }
    required_fields = {"schema_version", "reader_id", "evidence"}
    if not required_fields.issubset(projection) or set(projection) - allowed_fields:
        raise CommentatorContractError("invalid Commentator control projection fields")
    version = projection["schema_version"]
    if (
        not isinstance(version, int)
        or isinstance(version, bool)
        or version != _CONTROL_SCHEMA_VERSION
    ):
        raise CommentatorContractError("unsupported Commentator control schema_version")
    reader_id = _nonempty_string(projection["reader_id"], "reader_id")
    player_id = projection.get("player_id")
    if player_id is not None:
        player_id = _nonempty_string(player_id, "player_id")
        if reader_id != player_id:
            raise CommentatorContractError(
                "PLAYER control must match the Commentator recipient"
            )
    selected_pc_id = projection.get("selected_pc_id")
    if selected_pc_id is not None:
        selected_pc_id = _nonempty_string(selected_pc_id, "selected_pc_id")
        if player_id is None:
            raise CommentatorContractError(
                "selected PC requires current PLAYER evidence"
            )

    raw_evidence = projection["evidence"]
    if not isinstance(raw_evidence, Sequence) or isinstance(raw_evidence, (str, bytes)):
        raise CommentatorContractError("Commentator control evidence must be an array")
    evidence: list[dict[str, object]] = []
    for raw_item in raw_evidence:
        item = _mapping(raw_item, "Commentator native evidence")
        if set(item) != {"owner_family", "owner_identity", "payload"}:
            raise CommentatorContractError(
                "Commentator native evidence fields are not strict"
            )
        evidence.append(
            _validate_owner_evidence(
                item["owner_family"], item["owner_identity"], item["payload"]
            )
        )
    evidence_keys = [_evidence_key(item) for item in evidence]
    if len(evidence_keys) != len(set(evidence_keys)):
        raise CommentatorContractError("duplicate Commentator native owner evidence")

    player_records = [
        item for item in evidence if item["owner_family"] == "world.player"
    ]
    if player_id is None:
        if player_records or any(
            item["owner_family"] in {"runtime.disclosure", "world.knowledge"}
            for item in evidence
        ):
            raise CommentatorContractError(
                "protected control evidence requires current PLAYER scope"
            )
    elif len(player_records) != 1 or _evidence_key(player_records[0]) != (
        "world.player",
        (player_id,),
    ):
        raise CommentatorContractError(
            "control evidence lacks the exact current PLAYER"
        )

    player_payload = player_records[0]["payload"] if player_records else None
    controlled_pc_ids: list[str] = []
    if isinstance(player_payload, Mapping):
        controlled_pc_ids = _string_array(
            player_payload.get("controlled_pc_ids"), "controlled_pc_ids"
        )
    if selected_pc_id is not None and selected_pc_id not in controlled_pc_ids:
        raise CommentatorContractError(
            "selected PC is not controlled by the current PLAYER"
        )
    for item in evidence:
        family = item["owner_family"]
        identity = item["owner_identity"]
        assert isinstance(identity, list)
        if family == "runtime.disclosure" and identity[0] != player_id:
            raise CommentatorContractError(
                "disclosure evidence belongs to another PLAYER"
            )
        if family == "world.knowledge" and (
            selected_pc_id is None or identity[0] != selected_pc_id
        ):
            raise CommentatorContractError(
                "knowledge evidence is outside the selected-PC perspective"
            )

    result: dict[str, object] = {
        "schema_version": _CONTROL_SCHEMA_VERSION,
        "reader_id": reader_id,
        "evidence": evidence,
    }
    if player_id is not None:
        result["player_id"] = player_id
    if selected_pc_id is not None:
        result["selected_pc_id"] = selected_pc_id
    return result


def _control_projection_from_context(
    value: object, *, selected_pc_id: object | None
) -> dict[str, object]:
    result = _mapping(value, "profile.commentator_control result")
    if set(result) != {"outcome", "bundle", "trace"}:
        raise CommentatorContractError(
            "Commentator control result fields are not strict"
        )
    outcome = result["outcome"]
    if not isinstance(outcome, str) or outcome not in {
        "ASSEMBLED",
        "ASSEMBLED_DEGRADED",
    }:
        raise CommentatorContractError("Commentator control evidence is not assembled")
    _mapping(result["trace"], "Commentator control trace")
    bundle = _mapping(result["bundle"], "Commentator control bundle")
    expected_bundle_fields = {
        "profile_id",
        "role",
        "purpose",
        "subject_id",
        "source_frontier",
        "recipient_id",
        "required",
        "optional",
        "retrospective_projection",
    }
    if set(bundle) != expected_bundle_fields:
        raise CommentatorContractError(
            "Commentator control bundle fields are not strict"
        )
    if (
        bundle["profile_id"] != _CONTEXT_PROFILE_ID
        or bundle["role"] != "COMMENTATOR"
        or bundle["purpose"] != "control"
        or bundle["retrospective_projection"] is not False
    ):
        raise CommentatorContractError(
            "Context evidence is not from the registered Commentator control profile"
        )
    _nonempty_string(bundle["subject_id"], "subject_id")
    source_frontier = bundle["source_frontier"]
    if not isinstance(source_frontier, str):
        raise CommentatorContractError("source_frontier must be a string")
    if source_frontier:
        _nonempty_string(source_frontier, "source_frontier")
    recipient_id = _nonempty_string(bundle["recipient_id"], "recipient_id")

    candidates: list[object] = []
    for field in ("required", "optional"):
        raw_candidates = bundle[field]
        if not isinstance(raw_candidates, Sequence) or isinstance(
            raw_candidates, (str, bytes)
        ):
            raise CommentatorContractError(f"Context {field} evidence must be an array")
        candidates.extend(raw_candidates)

    native_evidence: list[dict[str, object]] = []
    candidate_ids: set[str] = set()
    for raw_candidate in candidates:
        candidate = _mapping(raw_candidate, "Context owner evidence")
        if set(candidate) != {
            "candidate_id",
            "owner_family",
            "owner_identity",
            "payload",
        }:
            raise CommentatorContractError(
                "Context owner evidence fields are not strict"
            )
        candidate_id = _nonempty_string(candidate["candidate_id"], "candidate_id")
        if candidate_id in candidate_ids:
            raise CommentatorContractError(
                "Context candidate identities must be unique"
            )
        candidate_ids.add(candidate_id)
        native_evidence.append(
            _validate_owner_evidence(
                candidate["owner_family"],
                candidate["owner_identity"],
                candidate["payload"],
            )
        )

    native_keys = [_evidence_key(item) for item in native_evidence]
    if len(native_keys) != len(set(native_keys)):
        raise CommentatorContractError(
            "Context evidence repeats a native owner identity"
        )
    player_records = [
        item for item in native_evidence if item["owner_family"] == "world.player"
    ]
    if len(player_records) > 1:
        raise CommentatorContractError(
            "Commentator control must have at most one PLAYER"
        )
    player_id: str | None = None
    if player_records:
        player_id = _evidence_key(player_records[0])[1][0]
        if player_id != recipient_id:
            raise CommentatorContractError(
                "current PLAYER evidence differs from the profile recipient"
            )
    selected = (
        None
        if selected_pc_id is None
        else _nonempty_string(selected_pc_id, "selected_pc_id")
    )
    return _validate_control_projection(
        {
            "schema_version": _CONTROL_SCHEMA_VERSION,
            "reader_id": recipient_id,
            "player_id": player_id,
            "selected_pc_id": selected,
            "evidence": native_evidence,
        }
    )


def build_commentator_control_projection(
    value: object, *, selected_pc_id: object | None = None
) -> dict[str, object]:
    """Build derived control data from exact-current registered Context evidence.

    Story IDs and visibility lists are not control inputs. Story-local T0
    `(owner_family, factor_id)` values nominate exact anchors; this projection
    retains only the P0 owner evidence needed to evaluate those anchors.
    """

    return _control_projection_from_context(value, selected_pc_id=selected_pc_id)


def _validate_snapshot(value: object) -> dict[str, object]:
    snapshot = _mapping(value, "Commentator snapshot")
    if set(snapshot) != {"schema_version", "records", "control"}:
        raise CommentatorContractError("invalid Commentator snapshot")
    version = snapshot["schema_version"]
    if (
        not isinstance(version, int)
        or isinstance(version, bool)
        or version != _SNAPSHOT_SCHEMA_VERSION
    ):
        raise CommentatorContractError(
            "unsupported Commentator snapshot schema_version"
        )
    records = snapshot["records"]
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise CommentatorContractError("invalid Commentator record corpus")
    try:
        validated_records = [
            validate_story_projection(record, layer="EVENTS") for record in records
        ]
    except StoryContractError as exc:
        raise CommentatorContractError(str(exc)) from exc
    ids = [record["story_id"] for record in validated_records]
    if len(ids) != len(set(ids)):
        raise CommentatorContractError("Commentator Story identities must be unique")
    return {
        "schema_version": version,
        "records": validated_records,
        "control": _validate_control_projection(snapshot["control"]),
    }


def build_commentator_snapshot(
    projections: object, control: object
) -> dict[str, object]:
    """Create a finite Story corpus and a separate derived control basis."""

    if not isinstance(projections, Sequence) or isinstance(projections, (str, bytes)):
        raise CommentatorContractError("Story projections must be an array")
    try:
        records = [
            validate_story_projection(record, layer="EVENTS") for record in projections
        ]
    except StoryContractError as exc:
        raise CommentatorContractError(str(exc)) from exc
    ids = [record["story_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise CommentatorContractError("Commentator Story identities must be unique")
    validated_control = _validate_control_projection(control)
    return {
        "schema_version": _SNAPSHOT_SCHEMA_VERSION,
        "records": deepcopy(records),
        "control": validated_control,
    }


def refresh_commentator_control(
    snapshot: object,
    current_context_evidence: object,
    *,
    selected_pc_id: object | None = None,
) -> dict[str, object]:
    """Refresh only the independently current control basis, retaining Story bytes."""

    current = _validate_snapshot(snapshot)
    control = build_commentator_control_projection(
        current_context_evidence, selected_pc_id=selected_pc_id
    )
    return build_commentator_snapshot(current["records"], control)


def _evidence_index(
    control: Mapping[str, object],
) -> dict[tuple[str, tuple[str, ...]], Mapping[str, object]]:
    raw_evidence = control["evidence"]
    assert isinstance(raw_evidence, list)
    return {
        _evidence_key(item): item for item in raw_evidence if isinstance(item, Mapping)
    }


def _lore_anchor_value_matches(
    value: object, evidence: Mapping[str, object] | None
) -> bool:
    payload = evidence.get("payload") if evidence is not None else None
    state = payload.get("state") if isinstance(payload, Mapping) else None
    if not isinstance(state, Mapping):
        return False
    statement = state.get("statement")
    truth_status = state.get("truth_status")
    current_transition = state.get("last_truth_transition_ref")
    if isinstance(value, str):
        if value in _OBJECTIVE_TRUTH_STATUSES:
            return value == truth_status
        return value == statement
    if not isinstance(value, Mapping) or set(value) - {
        "statement",
        "truth_status",
        "truth_transition_ref",
        "last_truth_transition_ref",
        "latest_exposed_truth_transition_ref",
    }:
        return False

    matched = False
    if "statement" in value:
        if not isinstance(value["statement"], str) or value["statement"] != statement:
            return False
        matched = True
    if "truth_status" in value:
        if (
            not isinstance(value["truth_status"], str)
            or value["truth_status"] not in _OBJECTIVE_TRUTH_STATUSES
            or value["truth_status"] != truth_status
        ):
            return False
        matched = True
    for field in (
        "truth_transition_ref",
        "last_truth_transition_ref",
        "latest_exposed_truth_transition_ref",
    ):
        if field in value:
            if (
                not isinstance(value[field], str)
                or not value[field]
                or value[field] != current_transition
            ):
                return False
            matched = True
    return matched


def _knowledge_anchor_value_supported(
    value: object, lore_fact: Mapping[str, object] | None
) -> bool:
    if isinstance(value, str) and value in _EPISTEMIC_STANCES:
        return True
    if isinstance(value, Mapping) and set(value) == {"stance"}:
        stance = value["stance"]
        return isinstance(stance, str) and stance in _EPISTEMIC_STANCES
    return _lore_anchor_value_matches(value, lore_fact)


def _requires_statement_disclosure(owner_family: object, value: object) -> bool:
    objective_fields = {
        "truth_status",
        "truth_transition_ref",
        "last_truth_transition_ref",
        "latest_exposed_truth_transition_ref",
    }
    if isinstance(value, str):
        return value not in _OBJECTIVE_TRUTH_STATUSES
    if isinstance(value, Mapping):
        return "statement" in value or not bool(objective_fields.intersection(value))
    return owner_family in _ANCHOR_FAMILIES


def _record_is_eligible(
    record: Mapping[str, object],
    control: Mapping[str, object],
    *,
    player_matches: bool,
) -> bool:
    basis = record["t0_basis"]
    assert isinstance(basis, Mapping)
    factors = basis["factors"]
    assert isinstance(factors, list)
    protected = [
        factor
        for factor in factors
        if isinstance(factor, Mapping)
        and factor.get("availability_classification") == "PROTECTED"
    ]
    if not protected:
        return True
    if not player_matches:
        return False

    evidence = _evidence_index(control)
    player_id = control.get("player_id")
    selected_pc_id = control.get("selected_pc_id")
    for factor in protected:
        owner_family = factor.get("owner_family")
        fact_id = factor.get("factor_id")
        if owner_family not in _ANCHOR_FAMILIES or not isinstance(fact_id, str):
            return False
        anchor = (owner_family, (fact_id,))
        lore_fact = evidence.get(("world.lore_fact", (fact_id,)))
        if owner_family == "world.lore_fact" and anchor not in evidence:
            return False

        value = factor.get("t0_value")
        if owner_family == "world.lore_fact" and not _lore_anchor_value_matches(
            value, lore_fact
        ):
            return False
        if owner_family == "world.knowledge" and not _knowledge_anchor_value_supported(
            value, lore_fact
        ):
            return False
        value_truth_status = (
            value.get("truth_status") if isinstance(value, Mapping) else None
        )
        requires_objective_status = (
            isinstance(value, str) and value in _OBJECTIVE_TRUTH_STATUSES
        ) or (
            isinstance(value, Mapping)
            and (
                isinstance(value_truth_status, str)
                and value_truth_status in _OBJECTIVE_TRUTH_STATUSES
                or any(
                    field in value
                    for field in (
                        "truth_transition_ref",
                        "last_truth_transition_ref",
                        "latest_exposed_truth_transition_ref",
                    )
                )
            )
        )

        disclosure = (
            evidence.get(("runtime.disclosure", (player_id, fact_id)))
            if isinstance(player_id, str)
            else None
        )
        disclosure_payload = (
            disclosure.get("payload") if disclosure is not None else None
        )
        if requires_objective_status:
            lore_payload = lore_fact.get("payload") if lore_fact is not None else None
            lore_state = (
                lore_payload.get("state") if isinstance(lore_payload, Mapping) else None
            )
            current_transition = (
                lore_state.get("last_truth_transition_ref")
                if isinstance(lore_state, Mapping)
                else None
            )
            objective_status_disclosed = (
                isinstance(current_transition, str)
                and bool(current_transition)
                and isinstance(disclosure_payload, Mapping)
                and disclosure_payload.get("latest_exposed_truth_transition_ref")
                == current_transition
            )
        else:
            objective_status_disclosed = True
        statement_disclosed = (
            isinstance(disclosure_payload, Mapping)
            and disclosure_payload.get("statement_exposed") is True
        )
        disclosed = (not requires_objective_status or objective_status_disclosed) and (
            not _requires_statement_disclosure(owner_family, value)
            or statement_disclosed
        )
        knowledge = (
            evidence.get(("world.knowledge", (selected_pc_id, fact_id)))
            if isinstance(selected_pc_id, str)
            else None
        )
        knowledge_payload = knowledge.get("payload") if knowledge is not None else None
        known = (
            isinstance(knowledge_payload, Mapping)
            and knowledge_payload.get("stance") == "epistemic.known"
        )
        if not (disclosed or known):
            return False
    return True


def filter_commentator_request(
    snapshot: object, player_id: object | None
) -> list[dict[str, object]]:
    """Filter protected Story/T0 units and all their metadata before materialization."""

    current = _validate_snapshot(snapshot)
    control = current["control"]
    assert isinstance(control, Mapping)
    if player_id is None:
        requested_player: str | None = None
    else:
        requested_player = _nonempty_string(player_id, "player_id")
    bound_player = control.get("player_id")
    player_matches = requested_player == bound_player and bound_player is not None
    records = current["records"]
    assert isinstance(records, list)
    return deepcopy(
        [
            record
            for record in records
            if _record_is_eligible(record, control, player_matches=player_matches)
        ]
    )
