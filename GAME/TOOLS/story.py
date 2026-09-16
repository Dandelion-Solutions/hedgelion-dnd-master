"""Bounded noncanonical Story projection helpers over native semantic history."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path

from GAME.TOOLS.history import HistoryContractError, validate_semantic_event_draft, validate_t0_basis


STORY_ROOT = "STORY"
_STORY_ID = re.compile(r"^(?P<prefix>[TEMN])(?P<sequence>[0-9]{6,})$")
_PREFIX_LAYERS = {"T": "TRANSCRIPT", "E": "EVENTS", "M": "MECHANICS", "N": "NARRATIVE"}


class StoryContractError(ValueError):
    """Raised when an owner-local Story projection violates its boundary."""


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise StoryContractError(f"{label} must be an object")
    return value


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StoryContractError(f"{label} must be a nonempty string")
    return value


def _unique_strings(value: object, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise StoryContractError(f"{label} must be an array")
    items = [_nonempty_string(item, label) for item in value]
    if not items or len(items) != len(set(items)):
        raise StoryContractError(f"{label} must be nonempty and unique")
    return items


def select_story_root(value: object) -> str:
    """Select the accepted static root without consulting deferred manifest routing."""

    if value != STORY_ROOT:
        raise StoryContractError("only the accepted STORY root is selectable")
    return STORY_ROOT


def _story_layer(story_id: object) -> tuple[str, int]:
    if not isinstance(story_id, str):
        raise StoryContractError("story_id must be a string")
    match = _STORY_ID.fullmatch(story_id)
    if match is None:
        raise StoryContractError("story_id must have a known prefix and canonical decimal sequence")
    sequence = int(match["sequence"])
    if sequence < 1:
        raise StoryContractError("story_id sequence must be positive")
    return _PREFIX_LAYERS[match["prefix"]], sequence


def story_record_path(story_root: object, story_id: object) -> Path:
    """Derive the fixed bounded route; physical placement is not Story authority."""

    root = select_story_root(story_root)
    layer, sequence = _story_layer(story_id)
    return Path(root) / layer / f"{sequence // 1000:03d}" / f"{story_id}.yaml"


def validate_story_projection(value: object, *, layer: str) -> dict[str, object]:
    """Validate one EVENTS owner-local projection with Story-local T0 support."""

    if layer != "EVENTS":
        raise StoryContractError("owner-local projection currently supports EVENTS only")
    projection = _mapping(value, "Story projection")
    expected = {"schema_version", "story_id", "content", "sources", "t0_basis", "availability"}
    if set(projection) != expected:
        raise StoryContractError("Story projection has unsupported or missing fields")
    actual_layer, _ = _story_layer(projection["story_id"])
    if actual_layer != layer:
        raise StoryContractError("Story identity prefix does not match projection layer")
    content = _mapping(projection["content"], "Story content")
    if set(content) != {"body"}:
        raise StoryContractError("Story content must contain only body in this owner-local shape")
    availability = _mapping(projection["availability"], "Story availability")
    if set(availability) != {"visible_to"}:
        raise StoryContractError("Story availability must contain only visible_to")
    visible_to = _unique_strings(availability["visible_to"], "visible_to")
    try:
        basis = validate_t0_basis(projection["t0_basis"])
    except HistoryContractError as exc:
        raise StoryContractError(str(exc)) from exc
    sources = _unique_strings(projection["sources"], "sources")
    if basis["event_id"] not in sources:
        raise StoryContractError("Story-local T0 basis must name an event source")
    version = projection["schema_version"]
    if version != 1 or isinstance(version, bool):
        raise StoryContractError("unsupported schema_version")
    return {
        "schema_version": version,
        "story_id": projection["story_id"],
        "content": {"body": _nonempty_string(content["body"], "Story body")},
        "sources": sources,
        "t0_basis": basis,
        "availability": {"visible_to": visible_to},
    }


def build_story_source_bundle(events: object, *, layer: str) -> dict[str, object]:
    """Build a caller-supplied finite source bundle; no scan or source mutation occurs."""

    if layer != "EVENTS":
        raise StoryContractError("owner-local source bundles currently support EVENTS only")
    if not isinstance(events, Sequence) or isinstance(events, str):
        raise StoryContractError("events must be an array")
    try:
        normalized = [validate_semantic_event_draft(event) for event in events]
    except HistoryContractError as exc:
        raise StoryContractError(str(exc)) from exc
    ids = [event["event_id"] for event in normalized]
    if len(ids) != len(set(ids)):
        raise StoryContractError("source bundle event identities must be unique")
    return {"layer": layer, "events": normalized}


def project_story_window(bundle: object, projections: object) -> list[dict[str, object]]:
    """Validate a finite EVENTS projection window without changing native history."""

    source_bundle = _mapping(bundle, "Story source bundle")
    if set(source_bundle) != {"layer", "events"} or source_bundle["layer"] != "EVENTS":
        raise StoryContractError("invalid EVENTS Story source bundle")
    if not isinstance(projections, Sequence) or isinstance(projections, str):
        raise StoryContractError("projections must be an array")
    event_ids = {event["event_id"] for event in source_bundle["events"]}
    validated = [validate_story_projection(projection, layer="EVENTS") for projection in projections]
    for projection in validated:
        if not set(projection["sources"]).issubset(event_ids):
            raise StoryContractError("Story projection must use only its bounded native sources")
    return deepcopy(validated)
