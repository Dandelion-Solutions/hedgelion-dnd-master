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
ACTOR_STATE_FIELDS = frozenset(
    {
        "name",
        "concept",
        "roles",
        "location_id",
        "build",
        "abilities",
        "hp",
        "life_state_id",
        "life_state_policy_id",
        "life_state_progress",
        "resources",
        "continuity",
        "details",
    }
)
FOUNDATION_FIELDS = frozenset({"values", "temperament", "identity"})
EVOLVING_STATEMENT_FIELDS = frozenset(
    {"long_term_goal", "current_objective", "next_intention"}
)
EVOLVING_STATEMENT_SET_FIELDS = frozenset(
    {"material_commitments", "reconsideration_cues"}
)
RELATIONSHIP_FACETS = frozenset(
    {"trust", "affinity", "fear", "respect", "hostility", "felt_obligation"}
)
RELATIONSHIP_LEVELS = frozenset({"low", "moderate", "high"})


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


def _id_set(value: object, label: str, *, allow_empty: bool) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise ActorContinuityError(f"{label} must be an array")
    identifiers = [_id(item, label) for item in value]
    if not allow_empty and not identifiers:
        raise ActorContinuityError(f"{label} must not be empty")
    if len(identifiers) != len(set(identifiers)):
        raise ActorContinuityError(f"{label} is ambiguous")
    return identifiers


def _statement(value: object, label: str) -> dict[str, object]:
    statement = _mapping(value, label)
    if set(statement) - {"statement", "source_refs"}:
        raise ActorContinuityError(f"{label} contains an unsupported field")
    text = statement.get("statement")
    if not isinstance(text, str) or not text:
        raise ActorContinuityError(f"{label} statement must be a nonempty string")
    result: dict[str, object] = {"statement": text}
    if "source_refs" in statement:
        result["source_refs"] = _id_set(
            statement["source_refs"], f"{label} source_refs", allow_empty=True
        )
    return result


def _statement_set(value: object, label: str) -> list[dict[str, object]]:
    if not isinstance(value, Sequence) or isinstance(value, str) or not value:
        raise ActorContinuityError(f"{label} must be a nonempty array")
    return [_statement(item, label) for item in value]


def _foundation(value: object) -> dict[str, object]:
    foundation = _mapping(value, "foundation continuity")
    if not foundation or set(foundation) - FOUNDATION_FIELDS:
        raise ActorContinuityError("foundation continuity contains an unsupported field")
    return {field: _statement_set(content, f"foundation {field}") for field, content in foundation.items()}


def _evolving(value: object) -> dict[str, object]:
    evolving = _mapping(value, "evolving continuity")
    allowed = EVOLVING_STATEMENT_FIELDS | EVOLVING_STATEMENT_SET_FIELDS
    if not evolving or set(evolving) - allowed:
        raise ActorContinuityError("evolving continuity contains an unsupported field")
    result: dict[str, object] = {}
    for field, content in evolving.items():
        if field in EVOLVING_STATEMENT_FIELDS:
            result[field] = _statement(content, f"evolving {field}")
        else:
            result[field] = _statement_set(content, f"evolving {field}")
    return result


def _relationships(value: object) -> dict[str, object]:
    relationships = _mapping(value, "relationship continuity")
    if not relationships:
        raise ActorContinuityError("relationship continuity must not be empty")
    normalized: dict[str, object] = {}
    for target_id, raw_view in relationships.items():
        _id(target_id, "relationship target id")
        view = _mapping(raw_view, "relationship view")
        if set(view) - {"facets", "basis_refs", "last_changed_event_id"} or "facets" not in view:
            raise ActorContinuityError("relationship view contains an unsupported field")
        facets = _mapping(view["facets"], "relationship facets")
        if not facets or set(facets) - RELATIONSHIP_FACETS:
            raise ActorContinuityError("relationship facets contain an unsupported field")
        if any(level not in RELATIONSHIP_LEVELS for level in facets.values()):
            raise ActorContinuityError("relationship facet has an unsupported value")
        normalized_view: dict[str, object] = {"facets": dict(facets)}
        if "basis_refs" in view:
            normalized_view["basis_refs"] = _id_set(
                view["basis_refs"], "relationship basis_refs", allow_empty=True
            )
        if "last_changed_event_id" in view:
            normalized_view["last_changed_event_id"] = _id(
                view["last_changed_event_id"], "relationship last_changed_event_id"
            )
        normalized[target_id] = normalized_view
    return normalized


def _nonnegative_integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ActorContinuityError(f"{label} must be a nonnegative integer")
    return value


def _localized_text(value: object) -> dict[str, object]:
    text = _mapping(value, "actor name")
    if not 1 <= len(text) <= 4:
        raise ActorContinuityError("actor name must contain one to four translations")
    normalized: dict[str, object] = {}
    for locale, content in text.items():
        if not isinstance(locale, str) or re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", locale) is None:
            raise ActorContinuityError("actor name locale is invalid")
        if not isinstance(content, str) or not content:
            raise ActorContinuityError("actor name value must be a nonempty string")
        normalized[locale] = content
    return normalized


def _build(value: object) -> dict[str, object]:
    build = _mapping(value, "actor build")
    allowed = {"species_id", "background_id", "class_progression", "choice_bindings", "spellcasting"}
    if set(build) - allowed or "class_progression" not in build:
        raise ActorContinuityError("actor build contains an unsupported field")
    progression = build["class_progression"]
    if not isinstance(progression, Sequence) or isinstance(progression, str) or not progression:
        raise ActorContinuityError("actor build class_progression must be a nonempty array")
    normalized_progression: list[dict[str, object]] = []
    for entry in progression:
        item = _mapping(entry, "actor build class progression entry")
        if set(item) - {"class_id", "level", "subclass_id"} or {"class_id", "level"} - set(item):
            raise ActorContinuityError("actor build class progression contains an unsupported field")
        normalized_entry: dict[str, object] = {
            "class_id": _id(item["class_id"], "actor build class_id"),
            "level": _nonnegative_integer(item["level"], "actor build level"),
        }
        if normalized_entry["level"] < 1:
            raise ActorContinuityError("actor build level must be positive")
        if "subclass_id" in item:
            normalized_entry["subclass_id"] = _id(item["subclass_id"], "actor build subclass_id")
        normalized_progression.append(normalized_entry)
    result: dict[str, object] = {"class_progression": normalized_progression}
    for field in ("species_id", "background_id"):
        if field in build:
            result[field] = _id(build[field], f"actor build {field}")
    if "choice_bindings" in build:
        bindings = _mapping(build["choice_bindings"], "actor build choice_bindings")
        if not bindings:
            raise ActorContinuityError("actor build choice_bindings must not be empty")
        normalized_bindings: dict[str, object] = {}
        allowed_bases = {
            "choice_basis.player_explicit",
            "choice_basis.rules_inheritance",
            "choice_basis.concept_inference",
            "choice_basis.campaign_default",
            "choice_basis.delegated_default",
        }
        for choice_id, raw_binding in bindings.items():
            binding = _mapping(raw_binding, "actor build choice binding")
            if set(binding) - {"selected_option_ids", "selection_basis", "basis_ref"} or "selected_option_ids" not in binding:
                raise ActorContinuityError("actor build choice binding contains an unsupported field")
            normalized_binding: dict[str, object] = {
                "selected_option_ids": _id_set(
                    binding["selected_option_ids"], "actor build selected_option_ids", allow_empty=True
                )
            }
            if "selection_basis" in binding:
                if (
                    not isinstance(binding["selection_basis"], str)
                    or binding["selection_basis"] not in allowed_bases
                ):
                    raise ActorContinuityError("actor build selection_basis is unsupported")
                normalized_binding["selection_basis"] = binding["selection_basis"]
            if "basis_ref" in binding:
                if not isinstance(binding["basis_ref"], str) or not binding["basis_ref"]:
                    raise ActorContinuityError("actor build basis_ref must be a nonempty string")
                normalized_binding["basis_ref"] = binding["basis_ref"]
            normalized_bindings[_id(choice_id, "actor build choice id")] = normalized_binding
        result["choice_bindings"] = normalized_bindings
    if "spellcasting" in build:
        spellcasting = _mapping(build["spellcasting"], "actor build spellcasting")
        allowed_spells = {"known_spell_ids", "prepared_spell_ids", "spellbook_spell_ids"}
        if not spellcasting or set(spellcasting) - allowed_spells:
            raise ActorContinuityError("actor build spellcasting contains an unsupported field")
        result["spellcasting"] = {
            field: _id_set(content, f"actor build {field}", allow_empty=True)
            for field, content in spellcasting.items()
        }
    return result


def _abilities(value: object) -> dict[str, object]:
    abilities = _mapping(value, "actor abilities")
    normalized: dict[str, object] = {}
    for ability_id, raw_components in abilities.items():
        components = _mapping(raw_components, "actor ability components")
        if not components or set(components) - {"base", "adjustment"}:
            raise ActorContinuityError("actor ability components contain an unsupported field")
        normalized_components: dict[str, object] = {}
        for field, component in components.items():
            if not isinstance(component, int) or isinstance(component, bool):
                raise ActorContinuityError(f"actor ability {field} must be an integer")
            if field == "base" and component < 0:
                raise ActorContinuityError("actor ability base must be nonnegative")
            normalized_components[field] = component
        normalized[_id(ability_id, "actor ability id")] = normalized_components
    return normalized


def _hp(value: object) -> dict[str, object]:
    hp = _mapping(value, "actor hp")
    if set(hp) - {"current", "maximum_base", "maximum_adjustment", "temporary"} or {"current", "maximum_base"} - set(hp):
        raise ActorContinuityError("actor hp contains an unsupported field")
    result: dict[str, object] = {}
    for field, amount in hp.items():
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ActorContinuityError(f"actor hp {field} must be an integer")
        if field != "maximum_adjustment" and amount < 0:
            raise ActorContinuityError(f"actor hp {field} must be nonnegative")
        result[field] = amount
    return result


def _temporal_binding(value: object, label: str) -> dict[str, object]:
    binding = _mapping(value, label)
    basis = binding.get("basis_id")
    variants = {
        "temporal.metric_deadline": ({"basis_id", "context_id", "anchor_value", "deadline_value", "unit_id"}, {"context_id", "unit_id"}, {"anchor_value", "deadline_value"}),
        "temporal.procedure_boundary": ({"basis_id", "boundary_id", "procedure_id", "anchor_id", "subject_id", "offset"}, {"boundary_id", "procedure_id", "anchor_id", "subject_id"}, {"offset"}),
        "temporal.semantic_boundary": ({"basis_id", "boundary_id", "anchor_id", "subject_id", "scope_id"}, {"boundary_id", "anchor_id", "subject_id", "scope_id"}, set()),
    }
    if not isinstance(basis, str) or basis not in variants:
        raise ActorContinuityError(f"{label} basis_id is unsupported")
    allowed, id_fields, integer_fields = variants[basis]
    required = {
        "temporal.metric_deadline": {"basis_id", "context_id", "anchor_value", "deadline_value", "unit_id"},
        "temporal.procedure_boundary": {"basis_id", "boundary_id", "procedure_id", "anchor_id"},
        "temporal.semantic_boundary": {"basis_id", "boundary_id", "anchor_id"},
    }[basis]
    if set(binding) - allowed or required - set(binding):
        raise ActorContinuityError(f"{label} contains an unsupported field")
    result: dict[str, object] = {"basis_id": basis}
    for field, item in binding.items():
        if field == "basis_id":
            continue
        if field in id_fields:
            result[field] = _id(item, f"{label} {field}")
        elif field in integer_fields:
            minimum = 1 if field == "offset" else 0
            amount = _nonnegative_integer(item, f"{label} {field}")
            if amount < minimum:
                raise ActorContinuityError(f"{label} offset must be positive")
            result[field] = amount
    return result


def _life_progress(value: object, life_state_id: object) -> dict[str, object]:
    progress = _mapping(value, "actor life_progress")
    if life_state_id == "life.dying":
        if set(progress) != {"death_saves"}:
            raise ActorContinuityError("actor life_progress contains an unsupported field")
        saves = _mapping(progress["death_saves"], "actor death_saves")
        if set(saves) != {"successes", "failures"}:
            raise ActorContinuityError("actor death_saves contains an unsupported field")
        normalized_saves = {
            field: _nonnegative_integer(amount, f"actor death_saves {field}")
            for field, amount in saves.items()
        }
        if any(amount > 2 for amount in normalized_saves.values()):
            raise ActorContinuityError("actor death_saves values must not exceed two")
        return {"death_saves": normalized_saves}
    if life_state_id == "life.stable":
        if set(progress) != {"recovery_binding"}:
            raise ActorContinuityError("actor life_progress contains an unsupported field")
        return {
            "recovery_binding": _temporal_binding(
                progress["recovery_binding"], "actor recovery_binding"
            )
        }
    raise ActorContinuityError("actor life_progress is not allowed for this life state")


def _resources(value: object) -> dict[str, object]:
    resources = _mapping(value, "actor resources")
    normalized: dict[str, object] = {}
    for resource_id, raw_pool in resources.items():
        pool = _mapping(raw_pool, "actor resource pool")
        if set(pool) - {"current", "recovery_binding"} or "current" not in pool:
            raise ActorContinuityError("actor resource pool contains an unsupported field")
        normalized_pool: dict[str, object] = {
            "current": _nonnegative_integer(pool["current"], "actor resource current")
        }
        if "recovery_binding" in pool:
            normalized_pool["recovery_binding"] = _temporal_binding(
                pool["recovery_binding"], "actor resource recovery_binding"
            )
        normalized[_id(resource_id, "actor resource id")] = normalized_pool
    return normalized


def validate_actor_source(value: object) -> dict[str, object]:
    """Return the bounded native Actor source required by continuity operations."""

    actor = _mapping(value, "actor")
    if actor.get("kind") != "world.actor":
        raise ActorContinuityError("continuity requires a world.actor native source")
    if set(actor) - {"id", "kind", "state_revision", "state", "provisional"}:
        raise ActorContinuityError("actor contains an unsupported field")
    if actor.get("provisional") is True:
        raise ActorContinuityError("provisional actor cannot become native continuity authority")

    actor_id = _id(actor.get("id"), "actor id")
    state_revision = _revision(actor.get("state_revision"), "actor state_revision")
    state = _validated_actor_state(actor.get("state"))
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


def _validated_continuity(
    value: object,
    *,
    foundation_transition: object = None,
    require_foundation_transition: bool = False,
) -> dict[str, object]:
    continuity = _mapping(value, "continuity changes")
    fields = set(continuity)
    if not fields or not fields.issubset(CONTINUITY_FIELDS):
        raise ActorContinuityError("changes must remain within native Actor continuity")
    if (
        require_foundation_transition
        and "foundation" in fields
        and foundation_transition != "foundation.explicit"
    ):
        raise ActorContinuityError("foundation changes require an explicit foundation transition")
    normalized: dict[str, object] = {}
    if "foundation" in continuity:
        normalized["foundation"] = _foundation(continuity["foundation"])
    if "evolving" in continuity:
        normalized["evolving"] = _evolving(continuity["evolving"])
    if "relationships" in continuity:
        normalized["relationships"] = _relationships(continuity["relationships"])
    return normalized


def validate_actor_continuity(value: object) -> dict[str, object]:
    """Validate the complete native Actor continuity contract."""

    return _validated_continuity(value)


def _validated_actor_state(value: object) -> dict[str, object]:
    state = _mapping(value, "actor state")
    unsupported = set(state) - ACTOR_STATE_FIELDS
    if unsupported:
        raise ActorContinuityError("actor state contains an unsupported field")
    aliases = ACTOR_STATE_ALIASES.intersection(state)
    if aliases:
        raise ActorContinuityError("native Actor continuity cannot mutate legacy authority aliases")
    normalized = deepcopy(dict(state))
    if "name" in state:
        normalized["name"] = _localized_text(state["name"])
    if "roles" in state:
        normalized["roles"] = _id_set(state["roles"], "actor roles", allow_empty=True)
    if "location_id" in state:
        normalized["location_id"] = _id(state["location_id"], "actor location_id")
    if "concept" in state and (not isinstance(state["concept"], str) or not state["concept"]):
        raise ActorContinuityError("actor concept must be a nonempty string")
    if "build" in state:
        normalized["build"] = _build(state["build"])
    if "abilities" in state:
        normalized["abilities"] = _abilities(state["abilities"])
    if "hp" in state:
        normalized["hp"] = _hp(state["hp"])
    if "life_state_id" in state:
        if (
            not isinstance(state["life_state_id"], str)
            or state["life_state_id"] not in {"life.active", "life.dying", "life.stable", "life.dead"}
        ):
            raise ActorContinuityError("actor life_state_id is unsupported")
    if "life_state_policy_id" in state:
        if not isinstance(state["life_state_policy_id"], str) or state[
            "life_state_policy_id"
        ] not in {"life_policy.dnd2024.character_like", "life_policy.dnd2024.monster_default"}:
            raise ActorContinuityError("actor life_state_policy_id is unsupported")
    if "life_state_progress" in state:
        if "life_state_id" not in state:
            raise ActorContinuityError("actor life_state_progress requires life_state_id")
        normalized["life_state_progress"] = _life_progress(
            state["life_state_progress"], state["life_state_id"]
        )
    if "resources" in state:
        normalized["resources"] = _resources(state["resources"])
    if "hp" in state and not {"life_state_id", "life_state_policy_id"}.issubset(state):
        raise ActorContinuityError(
            "actor hp requires life_state_id and life_state_policy_id"
        )
    if "life_state_id" in state and "life_state_policy_id" not in state:
        raise ActorContinuityError("actor life_state_id requires life_state_policy_id")
    if "life_state_progress" in state and not {"life_state_id", "life_state_policy_id"}.issubset(state):
        raise ActorContinuityError(
            "actor life_state_progress requires life_state_id and life_state_policy_id"
        )
    if state.get("life_state_id") == "life.dying" and "life_state_progress" not in state:
        raise ActorContinuityError("actor life.dying requires life_state_progress")
    if state.get("life_state_id") == "life.stable" and "life_state_progress" not in state:
        raise ActorContinuityError("actor life.stable requires life_state_progress")
    if state.get("life_state_id") in {"life.active", "life.dead"} and "life_state_progress" in state:
        raise ActorContinuityError("actor life_state_progress is not allowed for this life state")
    if "details" in state:
        normalized["details"] = deepcopy(dict(_mapping(state["details"], "actor details")))
    if "continuity" in state:
        normalized["continuity"] = _validated_continuity(state["continuity"])
    return normalized


def validate_actor_delta(
    value: object, actor: object, source_evidence: object
) -> dict[str, object]:
    """Validate one bounded, evidence-backed Actor continuity delta."""

    native_actor = validate_actor_source(actor)
    delta = _mapping(value, "actor delta")
    if set(delta) - {
        "actor_id",
        "expected_state_revision",
        "purpose",
        "source_refs",
        "foundation_transition",
        "changes",
    }:
        raise ActorContinuityError("actor delta contains an unsupported field")
    if (
        "foundation_transition" in delta
        and delta["foundation_transition"] != "foundation.explicit"
    ):
        raise ActorContinuityError("foundation_transition must equal foundation.explicit")
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
        raw_changes["continuity"],
        foundation_transition=delta.get("foundation_transition"),
        require_foundation_transition=True,
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
    state = _validated_actor_state(state)
    return {
        "id": native_actor["id"],
        "kind": "world.actor",
        "state_revision": native_actor["state_revision"] + 1,
        "state": state,
    }
