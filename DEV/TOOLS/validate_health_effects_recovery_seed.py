"""S6D-08 fail-closed reference validator; conformance aid, not production runtime."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from DEV.TOOLS.validate_character_mvp_seed import CanonicalSchemaValidator, SchemaViolation


def _effective_maximum(actor):
    hp = actor["hp"]
    return max(0, hp["maximum_base"] + hp.get("maximum_adjustment", 0))


def validate_actor_health(actor):
    hp = actor.get("hp")
    if hp is None:
        return True
    if "life_state_id" not in actor or "life_state_policy_id" not in actor:
        raise ValueError("material health requires LifeState and policy")
    if actor["life_state_policy_id"] != "life_policy.dnd2024.character_like":
        raise ValueError("unsupported LifeState policy")
    maximum = _effective_maximum(actor)
    current = hp.get("current")
    if not isinstance(current, int) or isinstance(current, bool) or current < 0 or current > maximum:
        raise ValueError("current HP outside pinned maximum")
    temporary = hp.get("temporary", 0)
    if not isinstance(temporary, int) or isinstance(temporary, bool) or temporary < 0:
        raise ValueError("invalid temporary HP")
    state = actor["life_state_id"]
    progress = actor.get("life_state_progress")
    if state == "life.active" and current == 0:
        raise ValueError("active character-like Actor cannot have zero HP")
    if state in {"life.dying", "life.stable", "life.dead"} and current != 0:
        raise ValueError("non-active character-like Actor requires zero HP")
    if state == "life.dying":
        saves = (progress or {}).get("death_saves")
        if not saves or any(not isinstance(saves.get(k), int) or not 0 <= saves[k] <= 2 for k in ("successes", "failures")):
            raise ValueError("dying requires bounded death-save progress")
    elif state == "life.stable":
        if not (progress or {}).get("recovery_binding"):
            raise ValueError("stable requires recovery binding")
    elif progress is not None:
        raise ValueError("active/dead cannot carry LifeState progress")
    return True


def validate_resource_instances(instances, definitions):
    for resource_id, state in instances.items():
        definition = definitions.get(resource_id)
        if not definition or definition.get("lifetime_owner") != "actor":
            raise ValueError("Actor ResourceState lacks matching Actor-owned definition")
        current = state.get("current")
        capacity = definition.get("capacity")
        if not isinstance(current, int) or isinstance(current, bool) or current < 0:
            raise ValueError("supported resource current must be nonnegative integer")
        if not isinstance(capacity, int) or current > capacity:
            raise ValueError("resource current exceeds pinned capacity")
    return True


def _receipt(actor, key, kind, world_effect_changes=None):
    result = {"actor": actor, "execution_segment": {"disposition": "COMMITTED"}, "mechanical_event": {"kind": kind}, "receipt": {"outcome": "COMPLETED", "idempotency_key": key}}
    if world_effect_changes:
        result["world_effect_changes"] = world_effect_changes
    return result


def _dedupe(key, receipts, producer):
    if key in receipts:
        return receipts[key]
    value = producer()
    receipts[key] = value
    return value


def _unconscious_changes(actor, present):
    effect_id = f"effect:life_state_unconscious:{actor['id']}"
    if not present:
        return {"create": [], "terminate": [effect_id]}
    return {
        "create": [{
            "id": effect_id,
            "kind": "world.effect",
            "definition_id": "condition.unconscious",
            "state": {
                "target_id": actor["id"],
                "rules_origin_id": actor["life_state_policy_id"],
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }],
        "terminate": [],
    }


def apply_damage(actor, amount, key, receipts, critical=False):
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("damage must be nonnegative integer")
    def produce():
        result = deepcopy(actor)
        world_effect_changes = None
        hp = result["hp"]
        remaining = amount
        temporary = hp.get("temporary", 0)
        used = min(temporary, remaining)
        hp["temporary"] = temporary - used
        remaining -= used
        state = result["life_state_id"]
        if hp["current"] == 0 and state in {"life.dying", "life.stable"} and remaining:
            if remaining >= _effective_maximum(result):
                result["life_state_id"] = "life.dead"
                result.pop("life_state_progress", None)
                world_effect_changes = _unconscious_changes(result, False)
            else:
                prior_failures = result.get("life_state_progress", {}).get("death_saves", {}).get("failures", 0)
                failures = prior_failures + (2 if critical else 1)
                if failures >= 3:
                    result["life_state_id"] = "life.dead"
                    result.pop("life_state_progress", None)
                    world_effect_changes = _unconscious_changes(result, False)
                else:
                    result["life_state_id"] = "life.dying"
                    result["life_state_progress"] = {"death_saves": {"successes": 0, "failures": failures}}
                    world_effect_changes = _unconscious_changes(result, True)
        else:
            before = hp["current"]
            hp["current"] = max(0, before - remaining)
            remainder_at_zero = max(0, remaining - before)
            if hp["current"] == 0:
                if remainder_at_zero >= _effective_maximum(result):
                    result["life_state_id"] = "life.dead"
                    result.pop("life_state_progress", None)
                    world_effect_changes = _unconscious_changes(result, False)
                else:
                    result["life_state_id"] = "life.dying"
                    result["life_state_progress"] = {"death_saves": {"successes": 0, "failures": 0}}
                    world_effect_changes = _unconscious_changes(result, True)
        validate_actor_health(result)
        return _receipt(result, key, "event.health.damage_applied", world_effect_changes)
    return _dedupe(key, receipts, produce)


def apply_healing(actor, amount, key, receipts):
    if not isinstance(amount, int) or amount < 0:
        raise ValueError("healing must be nonnegative integer")
    def produce():
        result = deepcopy(actor)
        world_effect_changes = None
        result["hp"]["current"] = min(_effective_maximum(result), result["hp"]["current"] + amount)
        if result["hp"]["current"] > 0 and result["life_state_id"] in {"life.dying", "life.stable"}:
            result["life_state_id"] = "life.active"
            result.pop("life_state_progress", None)
            world_effect_changes = _unconscious_changes(result, False)
        validate_actor_health(result)
        return _receipt(result, key, "event.health.healing_applied", world_effect_changes)
    return _dedupe(key, receipts, produce)


def apply_maximum_change(actor, adjustment_delta, key, receipts):
    def produce():
        result = deepcopy(actor)
        world_effect_changes = None
        hp = result["hp"]
        hp["maximum_adjustment"] = hp.get("maximum_adjustment", 0) + adjustment_delta
        maximum = _effective_maximum(result)
        hp["current"] = min(hp["current"], maximum)
        if maximum == 0:
            result["life_state_id"] = "life.dead"
            result.pop("life_state_progress", None)
            world_effect_changes = _unconscious_changes(result, False)
        validate_actor_health(result)
        return _receipt(result, key, "event.health.maximum_changed", world_effect_changes)
    return _dedupe(key, receipts, produce)


def apply_death_save(actor, natural_roll, key, receipts, fixed_recovery_roll=1, chronology_id="chronology.local", anchor=0):
    if not isinstance(natural_roll, int) or not 1 <= natural_roll <= 20:
        raise ValueError("death save requires fixed natural d20 result")
    def produce():
        result = deepcopy(actor)
        world_effect_changes = None
        if result["life_state_id"] != "life.dying":
            raise ValueError("death save requires dying Actor")
        saves = result["life_state_progress"]["death_saves"]
        if natural_roll == 20:
            result["hp"]["current"] = 1
            result["life_state_id"] = "life.active"
            result.pop("life_state_progress", None)
            world_effect_changes = _unconscious_changes(result, False)
        else:
            name, delta = ("failures", 2) if natural_roll == 1 else (("successes", 1) if natural_roll >= 10 else ("failures", 1))
            total = saves[name] + delta
            if total >= 3:
                if name == "failures":
                    result["life_state_id"] = "life.dead"
                    result.pop("life_state_progress", None)
                    world_effect_changes = _unconscious_changes(result, False)
                else:
                    if not 1 <= fixed_recovery_roll <= 4:
                        raise ValueError("fixed stable recovery roll must be d4")
                    result["life_state_id"] = "life.stable"
                    result["life_state_progress"] = {"recovery_binding": {"basis_id": "temporal.metric_deadline", "context_id": chronology_id, "anchor_value": anchor, "deadline_value": anchor + fixed_recovery_roll, "unit_id": "unit.hour"}}
            else:
                saves[name] = total
        validate_actor_health(result)
        receipt = _receipt(result, key, "event.life_state.death_save_resolved", world_effect_changes)
        if result["life_state_id"] == "life.stable":
            receipt["receipt"]["fixed_rng"] = {"die": "1d4", "result": fixed_recovery_roll}
        return receipt
    return _dedupe(key, receipts, produce)


def recover_stable_actor(actor, key, receipts):
    def produce():
        result = deepcopy(actor)
        if result["life_state_id"] != "life.stable":
            raise ValueError("stable recovery requires stable Actor")
        result["hp"]["current"] = 1
        result["life_state_id"] = "life.active"
        result.pop("life_state_progress", None)
        world_effect_changes = _unconscious_changes(result, False)
        validate_actor_health(result)
        return _receipt(result, key, "event.life_state.stable_recovered", world_effect_changes)
    return _dedupe(key, receipts, produce)


def apply_boundary(resources, capacities, boundary_id, occurrence_key, owner_id, contract, receipts):
    valid_boundaries = {row["boundary_id"] for row in contract["mechanical_recovery"]["resource_responders"]}
    if boundary_id not in valid_boundaries:
        raise ValueError("unknown or unsupported boundary")
    key = (occurrence_key, owner_id)
    def produce():
        result = deepcopy(resources)
        for row in contract["mechanical_recovery"]["resource_responders"]:
            if row["boundary_id"] == boundary_id and row["resource_id"] in result:
                if row["operation_id"] == "resource_recovery.restore_to_capacity":
                    result[row["resource_id"]]["current"] = capacities[row["resource_id"]]
                elif row["operation_id"] == "resource_recovery.restore_amount":
                    result[row["resource_id"]]["current"] = min(
                        capacities[row["resource_id"]],
                        result[row["resource_id"]]["current"] + row["amount"],
                    )
                else:
                    raise ValueError("unsupported recovery operation")
        return {"resources": result, "mechanical_event": {"kind": "event.boundary.owner_responses_committed"}, "receipt": {"outcome": "COMPLETED", "idempotency_key": list(key)}}
    return _dedupe(key, receipts, produce)


def validate_package_content_set(package_dir, capability):
    expected_paths = ["character-mvp-seed.json", "health-effects-recovery-seed.json"]
    rows = capability.get("content_files")
    if not isinstance(rows, list) or [row.get("path") for row in rows] != expected_paths:
        raise ValueError("package content file set mismatch")
    digest_lines = []
    for row in rows:
        path = package_dir / row["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != row.get("sha256"):
            raise ValueError("package member digest mismatch")
        digest_lines.append(f"{row['path']}\0{actual}\n")
    aggregate = hashlib.sha256("".join(digest_lines).encode("utf-8")).hexdigest()
    if aggregate != capability.get("content_set_sha256"):
        raise ValueError("package aggregate content identity mismatch")
    return True


def validate_seed_schema(value, schema):
    validator = CanonicalSchemaValidator(Path(__file__).resolve().parents[1] / "SCHEMAS")
    try:
        validator.validate(value, schema)
    except SchemaViolation as error:
        raise ValueError("health/effects/recovery seed schema violation") from error
    exact_digest = schema.get("x-hdm-exact-instance-sha256")
    actual_digest = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if not exact_digest or actual_digest != exact_digest:
        raise ValueError("health/effects/recovery exact machine contract mismatch")
    transition_ids = {row["transition_id"] for row in value["life_state_policy"]["transitions"]}
    expected = {"damage_to_zero", "instant_death_massive_damage", "damage_at_zero", "healing_from_zero", "death_save_natural_1", "death_save_natural_20", "third_death_save_success", "third_death_save_failure"}
    if transition_ids != expected:
        raise ValueError("LifeState transition inventory mismatch")
    return True


def validate_actor_and_effect_outputs(output, schema_dir):
    validator = CanonicalSchemaValidator(Path(schema_dir))
    world_schema_id = "https://hedgelion.invalid/schemas/world-record.schema.json"
    if world_schema_id not in validator.schemas:
        raise ValueError("canonical world-record schema unavailable")
    world_schema = validator.schemas[world_schema_id]
    actor = output["actor"]
    if "id" not in actor:
        raise ValueError("Actor identity missing")
    actor_record = {"id": actor["id"], "kind": "world.actor", "state": {key: value for key, value in actor.items() if key != "id"}}
    try:
        validator.validate(actor_record, world_schema)
        for record in output.get("world_effect_changes", {}).get("create", []):
            validator.validate(record, world_schema)
        for effect_id in output.get("world_effect_changes", {}).get("terminate", []):
            validator.validate(effect_id, {"$ref": "#/$defs/machineId"}, world_schema)
    except (SchemaViolation, KeyError) as error:
        raise ValueError("canonical Actor/Effect schema validation failed") from error
    validate_actor_health(actor)
    return True


def apply_effect(effects, definition_id, target_id, source_id, key, receipts):
    def produce():
        result = deepcopy(effects)
        validate_world_effect_records(result)
        if key in result:
            raise ValueError("new Effect envelope identity already exists")
        for record in result.values():
            state = record["state"]
            if (
                record["definition_id"] == definition_id
                and state["target_id"] == target_id
                and state.get("source_id") == source_id
                and state["lifecycle"]["state_id"] == "effect_lifecycle.active"
            ):
                state["lifecycle"] = {"state_id": "effect_lifecycle.terminal", "terminal_reason_id": "effect_end.replaced"}
                state.pop("temporal_binding", None)
        result[key] = {
            "id": key,
            "kind": "world.effect",
            "definition_id": definition_id,
            "state": {
                "target_id": target_id,
                "source_id": source_id,
                "temporal_binding": {"basis_id": "temporal.metric_deadline", "context_id": "chronology.local", "anchor_value": 0, "deadline_value": 60, "unit_id": "unit.second"},
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }
        validate_world_effect_records(result)
        return {"effects": result, "mechanical_event": {"kind": "event.effect.applied"}, "receipt": {"outcome": "COMPLETED", "idempotency_key": key}}
    return _dedupe(key, receipts, produce)


def expire_effect(effects, effect_id, key, receipts):
    def produce():
        validate_world_effect_records(effects)
        if effect_id not in effects:
            raise ValueError("unknown Effect owner")
        result = deepcopy(effects)
        state = result[effect_id]["state"]
        if state["lifecycle"]["state_id"] != "effect_lifecycle.active":
            raise ValueError("Effect is not active")
        state["lifecycle"] = {"state_id": "effect_lifecycle.terminal", "terminal_reason_id": "effect_end.expired"}
        state.pop("temporal_binding", None)
        validate_world_effect_records(result)
        return {"effects": result, "mechanical_event": {"kind": "event.effect.expired"}, "receipt": {"outcome": "COMPLETED", "idempotency_key": key}}
    return _dedupe(key, receipts, produce)


def terminate_support_tree(effects, root_id, key, receipts):
    def produce():
        validate_world_effect_records(effects)
        if root_id not in effects:
            raise ValueError("unknown support root")
        result = deepcopy(effects)
        result[root_id]["state"]["lifecycle"] = {"state_id": "effect_lifecycle.terminal", "terminal_reason_id": "effect_end.removed"}
        changed = {root_id}
        while True:
            next_ids = [effect_id for effect_id, effect in result.items() if effect["state"].get("support_effect_id") in changed and effect["state"]["lifecycle"]["state_id"] == "effect_lifecycle.active"]
            if not next_ids:
                break
            changed = set(next_ids)
            for effect_id in next_ids:
                result[effect_id]["state"]["lifecycle"] = {"state_id": "effect_lifecycle.terminal", "terminal_reason_id": "effect_end.support_lost"}
        validate_world_effect_records(result)
        return {"effects": result, "mechanical_event": {"kind": "event.effect.support_tree_ended"}, "receipt": {"outcome": "COMPLETED", "idempotency_key": key}}
    return _dedupe(key, receipts, produce)


def reconstruct_derived_state(effects, required_timed_definition_ids=None):
    validate_world_effect_records(effects)
    required = set(required_timed_definition_ids or ())
    agenda = []
    condition_sources = {}
    for effect_id, record in effects.items():
        effect = record["state"]
        if effect["lifecycle"]["state_id"] != "effect_lifecycle.active":
            continue
        binding = effect.get("temporal_binding")
        if record["definition_id"] in required and not binding:
            raise ValueError("required active temporal binding missing")
        if binding and binding.get("basis_id") == "temporal.metric_deadline":
            agenda.append((effect_id, binding["deadline_value"]))
        definition_id = record["definition_id"]
        if definition_id.startswith("condition."):
            condition_sources.setdefault(definition_id, []).append(effect_id)
    return {"agenda": sorted(agenda), "conditions": {key: sorted(value) for key, value in condition_sources.items()}}


def validate_world_effect_records(effects, schema_dir=None):
    validator = CanonicalSchemaValidator(Path(schema_dir or Path(__file__).resolve().parents[1] / "SCHEMAS"))
    world_schema = validator.schemas.get("https://hedgelion.invalid/schemas/world-record.schema.json")
    if world_schema is None:
        raise ValueError("canonical world-record schema unavailable")
    try:
        for effect_id, record in effects.items():
            if record.get("id") != effect_id or record.get("kind") != "world.effect":
                raise ValueError("Effect collection key/envelope identity mismatch")
            validator.validate(record, world_schema)
    except SchemaViolation as error:
        raise ValueError("canonical world.effect record validation failed") from error
    return True

