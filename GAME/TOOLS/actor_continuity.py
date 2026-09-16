#!/usr/bin/env python3
"""Deterministic validation and application of source-Actor continuity deltas."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
import re


NATIVE_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
ASSESSMENT_PURPOSES = frozenset(
    {
        "assessment.react",
        "assessment.reflect",
        "assessment.plan",
        "assessment.reconsider",
        "assessment.relationship_update",
    }
)
ACTOR_STATE_ALIASES = frozenset(
    {"knowledge", "beliefs", "suspicions", "inventory", "conditions", "active_effects"}
)
CONTINUITY_FIELDS = frozenset({"foundation", "evolving", "relationships"})


class ActorContinuityError(ValueError):
    """Raised when a proposed Actor-continuity operation crosses an owner boundary."""


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ActorContinuityError(f"{label} must be an object")
    return value


def _id(value: object, label: str) -> str:
    if not isinstance(value, str) or NATIVE_ID_PATTERN.fullmatch(value) is None:
        raise ActorContinuityError(f"{label} must be a native id")
    return value


def _revision(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ActorContinuityError(f"{label} must be a nonnegative integer")
    return value


def validate_actor_source(value: object) -> dict[str, object]:
    """Return the bounded native Actor source required by continuity operations."""

    actor = _mapping(value, "actor")
    if actor.get("kind") != "world.actor":
        raise ActorContinuityError("continuity requires a world.actor native source")
    if actor.get("provisional") is True:
        raise ActorContinuityError("provisional actor cannot become native continuity authority")

    actor_id = _id(actor.get("id"), "actor id")
    state_revision = _revision(actor.get("state_revision"), "actor state_revision")
    state = _mapping(actor.get("state"), "actor state")
    aliases = ACTOR_STATE_ALIASES.intersection(state)
    if aliases:
        raise ActorContinuityError("native Actor continuity cannot mutate legacy authority aliases")
    return {
        "id": actor_id,
        "kind": "world.actor",
        "state_revision": state_revision,
        "state": deepcopy(dict(state)),
    }


def _validated_evidence(value: object, actor_id: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ActorContinuityError("source_evidence must be an array")
    refs: list[str] = []
    for raw_evidence in value:
        evidence = _mapping(raw_evidence, "source evidence")
        ref = _id(evidence.get("ref"), "source evidence ref")
        if evidence.get("accepted") is not True:
            raise ActorContinuityError("source evidence is not accepted")
        if evidence.get("current") is not True:
            raise ActorContinuityError("source evidence is stale")
        authorized = evidence.get("authorized_actor_ids")
        if not isinstance(authorized, Sequence) or isinstance(authorized, str):
            raise ActorContinuityError("source evidence authorization is missing")
        if actor_id not in authorized:
            raise ActorContinuityError("source evidence is unauthorized")
        refs.append(ref)
    if not refs or len(refs) != len(set(refs)):
        raise ActorContinuityError("source evidence is missing or ambiguous")
    return refs


def _validated_continuity(value: object, *, foundation_transition: object = None) -> dict[str, object]:
    continuity = _mapping(value, "continuity changes")
    fields = set(continuity)
    if not fields or not fields.issubset(CONTINUITY_FIELDS):
        raise ActorContinuityError("changes must remain within native Actor continuity")
    if "foundation" in fields and foundation_transition != "foundation.explicit":
        raise ActorContinuityError("foundation changes require an explicit foundation transition")
    for field, content in continuity.items():
        if not isinstance(content, Mapping) or not content:
            raise ActorContinuityError(f"continuity {field} must be a nonempty object")
    return deepcopy(dict(continuity))


def validate_actor_delta(
    value: object, actor: object, source_evidence: object
) -> dict[str, object]:
    """Validate one bounded, evidence-backed Actor continuity delta."""

    native_actor = validate_actor_source(actor)
    delta = _mapping(value, "actor delta")
    actor_id = _id(delta.get("actor_id"), "delta actor_id")
    if actor_id != native_actor["id"]:
        raise ActorContinuityError("delta actor identity conflicts with native Actor source")
    expected_revision = _revision(
        delta.get("expected_state_revision"), "expected_state_revision"
    )
    if expected_revision != native_actor["state_revision"]:
        raise ActorContinuityError("actor delta is stale")
    purpose = delta.get("purpose")
    if purpose not in ASSESSMENT_PURPOSES:
        raise ActorContinuityError("unsupported assessment purpose")
    source_refs = delta.get("source_refs")
    if not isinstance(source_refs, Sequence) or isinstance(source_refs, str):
        raise ActorContinuityError("source_refs must be an array")
    normalized_refs = [_id(ref, "source ref") for ref in source_refs]
    accepted_refs = _validated_evidence(source_evidence, actor_id)
    if not normalized_refs or len(normalized_refs) != len(set(normalized_refs)):
        raise ActorContinuityError("source_refs are missing or ambiguous")
    if set(normalized_refs) != set(accepted_refs):
        raise ActorContinuityError("delta source refs do not match accepted evidence")
    raw_changes = _mapping(delta.get("changes"), "actor delta changes")
    if set(raw_changes) != {"continuity"}:
        raise ActorContinuityError("changes must remain within native Actor continuity")
    continuity = _validated_continuity(
        raw_changes["continuity"], foundation_transition=delta.get("foundation_transition")
    )
    result: dict[str, object] = {
        "actor_id": actor_id,
        "expected_state_revision": expected_revision,
        "purpose": purpose,
        "source_refs": normalized_refs,
        "changes": {"continuity": continuity},
    }
    if "foundation" in continuity:
        result["foundation_transition"] = "foundation.explicit"
    return result


def assess_actor(value: object) -> dict[str, object]:
    """Assess one native Actor and return a deterministic acceptance carrier."""

    request = _mapping(value, "actor assessment request")
    actor = validate_actor_source(request.get("actor"))
    purpose = request.get("purpose")
    if purpose not in ASSESSMENT_PURPOSES:
        raise ActorContinuityError("unsupported assessment purpose")
    source_refs = _validated_evidence(request.get("source_evidence"), actor["id"])
    if request.get("delta") is None:
        return {
            "actor_id": actor["id"],
            "expected_state_revision": actor["state_revision"],
            "purpose": purpose,
            "disposition": "assessment.no_change",
            "source_refs": source_refs,
        }
    delta = validate_actor_delta(request.get("delta"), actor, request.get("source_evidence"))
    if delta["purpose"] != purpose:
        raise ActorContinuityError("assessment purpose conflicts with delta purpose")
    return {
        "actor_id": actor["id"],
        "expected_state_revision": actor["state_revision"],
        "purpose": purpose,
        "disposition": "assessment.delta",
        "source_refs": delta["source_refs"],
        "delta": delta,
    }


def _merge_mapping(base: dict[str, object], change: Mapping[str, object]) -> dict[str, object]:
    merged = deepcopy(base)
    for key, value in change.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, Mapping):
            merged[key] = _merge_mapping(existing, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def apply_actor_delta(
    actor: object, delta: object, source_evidence: object
) -> dict[str, object]:
    """Apply an accepted continuity-only delta to its exact native Actor revision."""

    native_actor = validate_actor_source(actor)
    normalized_delta = validate_actor_delta(delta, native_actor, source_evidence)
    state = deepcopy(native_actor["state"])
    roles = state.get("roles", [])
    if (
        isinstance(roles, Sequence)
        and not isinstance(roles, str)
        and "actor.player_character" in roles
    ):
        raise ActorContinuityError(
            "continuity assessment cannot author player-controlled Actor state"
        )
    continuity = state.get("continuity", {})
    if not isinstance(continuity, dict):
        raise ActorContinuityError("actor continuity state must be an object")
    state["continuity"] = _merge_mapping(continuity, normalized_delta["changes"]["continuity"])
    return {
        "id": native_actor["id"],
        "kind": "world.actor",
        "state_revision": native_actor["state_revision"] + 1,
        "state": state,
    }
