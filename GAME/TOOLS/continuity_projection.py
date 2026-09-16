#!/usr/bin/env python3
"""Derived-only continuity projection admission for one exact native Actor source."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy

from GAME.TOOLS.actor_continuity import (
    ActorContinuityError,
    NATIVE_ID_PATTERN,
    validate_actor_source,
)


class ContinuityProjectionError(ValueError):
    """Raised when a continuity projection attempts to replace native Actor state."""


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ContinuityProjectionError(f"{label} must be an object")
    return value


def _source_refs(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ContinuityProjectionError("source_refs must be an array")
    refs = list(value)
    if not refs or not all(
        isinstance(ref, str) and NATIVE_ID_PATTERN.fullmatch(ref) is not None for ref in refs
    ):
        raise ContinuityProjectionError("source_refs must contain native ids")
    if len(refs) != len(set(refs)):
        raise ContinuityProjectionError("source_refs are ambiguous")
    return refs


def _id(value: object, label: str) -> str:
    if not isinstance(value, str) or NATIVE_ID_PATTERN.fullmatch(value) is None:
        raise ContinuityProjectionError(f"{label} must be a native id")
    return value


def _revision(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContinuityProjectionError(f"{label} must be a nonnegative integer")
    return value


def _retained_value_subset(candidate: object, source: object) -> bool:
    if isinstance(candidate, Mapping):
        return (
            isinstance(source, Mapping)
            and bool(candidate)
            and all(
                key in source and _retained_value_subset(value, source[key])
                for key, value in candidate.items()
            )
        )
    if isinstance(candidate, list):
        return isinstance(source, list) and bool(candidate) and all(
            any(candidate_item == source_item for source_item in source)
            for candidate_item in candidate
        )
    return candidate == source


def _validated_source_bundle(value: object) -> dict[str, object]:
    bundle = _mapping(value, "continuity source bundle")
    if set(bundle) != {"actor_id", "state_revision", "source_refs", "continuity"}:
        raise ContinuityProjectionError("continuity source bundle contains an unsupported field")
    continuity = _mapping(bundle["continuity"], "native continuity")
    if not continuity:
        raise ContinuityProjectionError("native continuity must not be empty")
    return {
        "actor_id": _id(bundle["actor_id"], "source bundle actor_id"),
        "state_revision": _revision(bundle["state_revision"], "source bundle state_revision"),
        "source_refs": _source_refs(bundle["source_refs"]),
        "continuity": deepcopy(dict(continuity)),
    }


def build_continuity_source_bundle(actor: object, source_evidence: object) -> dict[str, object]:
    """Create a bounded projection source bundle from one non-provisional native Actor."""

    try:
        native_actor = validate_actor_source(actor)
    except ActorContinuityError as error:
        raise ContinuityProjectionError(str(error)) from error
    if not isinstance(source_evidence, Sequence) or isinstance(source_evidence, str):
        raise ContinuityProjectionError("source_evidence must be an array")
    refs: list[str] = []
    for raw_evidence in source_evidence:
        evidence = _mapping(raw_evidence, "source evidence")
        ref = evidence.get("ref")
        authorized = evidence.get("authorized_actor_ids")
        if (
            not isinstance(ref, str)
            or evidence.get("accepted") is not True
            or evidence.get("current") is not True
            or not isinstance(authorized, Sequence)
            or isinstance(authorized, str)
            or native_actor["id"] not in authorized
        ):
            raise ContinuityProjectionError("projection source evidence is not current native evidence")
        refs.append(_id(ref, "projection source evidence ref"))
    if not refs or len(refs) != len(set(refs)):
        raise ContinuityProjectionError("projection source evidence is missing or ambiguous")
    continuity = native_actor["state"].get("continuity", {})
    if not isinstance(continuity, Mapping):
        raise ContinuityProjectionError("native actor continuity must be an object")
    return {
        "actor_id": native_actor["id"],
        "state_revision": native_actor["state_revision"],
        "source_refs": refs,
        "continuity": deepcopy(dict(continuity)),
    }


def validate_continuity_projection(
    candidate: object, source_bundle: object
) -> dict[str, object]:
    """Validate a derived projection without admitting a writable replacement authority."""

    projection = _mapping(candidate, "continuity projection candidate")
    bundle = _validated_source_bundle(source_bundle)
    if set(projection) != {
        "actor_id",
        "expected_state_revision",
        "source_refs",
        "projection_kind",
        "continuity",
    }:
        raise ContinuityProjectionError("continuity projection contains an unsupported field")
    if projection.get("projection_kind") != "continuity.derived":
        raise ContinuityProjectionError("continuity projection must be explicitly derived")
    if _id(projection.get("actor_id"), "projection actor_id") != bundle["actor_id"]:
        raise ContinuityProjectionError("projection actor identity conflicts with source bundle")
    if _revision(
        projection.get("expected_state_revision"), "projection expected_state_revision"
    ) != bundle["state_revision"]:
        raise ContinuityProjectionError("continuity projection is stale")
    refs = _source_refs(projection.get("source_refs"))
    if set(refs) != set(_source_refs(bundle.get("source_refs"))):
        raise ContinuityProjectionError("projection source refs do not match native bundle")
    continuity = _mapping(projection.get("continuity"), "projection continuity")
    forbidden = {"knowledge", "beliefs", "suspicions", "inventory", "conditions", "active_effects"}
    if forbidden.intersection(continuity):
        raise ContinuityProjectionError("continuity projection cannot contain knowledge or other native authority")
    if not _retained_value_subset(continuity, bundle["continuity"]):
        raise ContinuityProjectionError("continuity projection diverges from native source continuity")
    return {
        "actor_id": projection["actor_id"],
        "expected_state_revision": projection["expected_state_revision"],
        "source_refs": refs,
        "projection_kind": "continuity.derived",
        "continuity": deepcopy(dict(continuity)),
    }


def classify_projection_compatibility(
    projection: object, source_bundle: object
) -> str:
    """Classify a projection only against the exact current source bundle supplied."""

    try:
        validate_continuity_projection(projection, source_bundle)
    except ContinuityProjectionError as error:
        if "stale" in str(error):
            return "stale"
        return "incompatible"
    return "compatible"
