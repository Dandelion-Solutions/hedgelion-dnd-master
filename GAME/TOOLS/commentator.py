"""Self-contained, read-only Commentator projection and pre-materialization filter."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy

from GAME.TOOLS.story import StoryContractError, validate_story_projection


class CommentatorContractError(ValueError):
    """Raised for malformed self-contained Commentator control material."""


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CommentatorContractError(f"{label} must be a nonempty string")
    return value


def _story_ids(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise CommentatorContractError("story_ids must be an array")
    ids = [_nonempty_string(item, "story_id") for item in value]
    if len(ids) != len(set(ids)):
        raise CommentatorContractError("story_ids must be unique")
    return ids


def build_commentator_control_projection(value: object) -> dict[str, object]:
    """Build derived control data; it is not a second knowledge or ACL authority."""

    if not isinstance(value, Mapping):
        raise CommentatorContractError("Commentator controls must be an object")
    controls: dict[str, dict[str, list[str]]] = {}
    for player_id, raw_control in value.items():
        player = _nonempty_string(player_id, "player_id")
        if not isinstance(raw_control, Mapping) or set(raw_control) != {"story_ids"}:
            raise CommentatorContractError("each Commentator control must contain story_ids")
        controls[player] = {"story_ids": _story_ids(raw_control["story_ids"])}
    return {"schema_version": 1, "controls": controls}


def _validate_control_projection(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping) or set(value) != {"schema_version", "controls"}:
        raise CommentatorContractError("invalid Commentator control projection")
    version = value["schema_version"]
    if version != 1 or isinstance(version, bool):
        raise CommentatorContractError("unsupported Commentator control schema_version")
    controls = value["controls"]
    if not isinstance(controls, Mapping):
        raise CommentatorContractError("Commentator controls must be an object")
    return build_commentator_control_projection(controls)


def build_commentator_snapshot(projections: object, control: object) -> dict[str, object]:
    """Create a finite imported corpus and its derived eligibility-control projection."""

    if not isinstance(projections, Sequence) or isinstance(projections, str):
        raise CommentatorContractError("Story projections must be an array")
    try:
        records = [validate_story_projection(record, layer="EVENTS") for record in projections]
    except StoryContractError as exc:
        raise CommentatorContractError(str(exc)) from exc
    ids = [record["story_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise CommentatorContractError("Commentator Story identities must be unique")
    validated_control = _validate_control_projection(control)
    return {"schema_version": 1, "records": deepcopy(records), "control": validated_control}


def filter_commentator_request(snapshot: object, player_id: object) -> list[dict[str, object]]:
    """Filter IDs and bodies before a Commentator request sees any protected material."""

    if not isinstance(snapshot, Mapping) or set(snapshot) != {"schema_version", "records", "control"}:
        raise CommentatorContractError("invalid Commentator snapshot")
    if snapshot["schema_version"] != 1 or isinstance(snapshot["schema_version"], bool):
        raise CommentatorContractError("unsupported Commentator snapshot schema_version")
    player = _nonempty_string(player_id, "player_id")
    control = _validate_control_projection(snapshot["control"])
    raw_player_control = control["controls"].get(player)
    if not isinstance(raw_player_control, Mapping):
        return []
    allowed = set(_story_ids(raw_player_control.get("story_ids")))
    records = snapshot["records"]
    if not isinstance(records, Sequence) or isinstance(records, str):
        raise CommentatorContractError("invalid Commentator record corpus")
    try:
        validated_records = [validate_story_projection(record, layer="EVENTS") for record in records]
    except StoryContractError as exc:
        raise CommentatorContractError(str(exc)) from exc
    return deepcopy(
        [
            record
            for record in validated_records
            if record["story_id"] in allowed and player in record["availability"]["visible_to"]
        ]
    )
