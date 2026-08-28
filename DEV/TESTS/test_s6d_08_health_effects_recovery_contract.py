import json
import unittest
from pathlib import Path

from DEV.TOOLS.validate_character_mvp_seed import CanonicalSchemaValidator, SchemaViolation

from DEV.TOOLS.validate_health_effects_recovery_seed import (
    apply_damage,
    apply_healing,
    apply_maximum_change,
    apply_death_save,
    recover_stable_actor,
    apply_boundary,
    validate_actor_health,
    validate_resource_instances,
    validate_seed_schema,
    validate_actor_and_effect_outputs,
    apply_effect,
    expire_effect,
    terminate_support_tree,
    reconstruct_derived_state,
)
from DEV.TOOLS.validate_ruleset_package_closure import build_resolved_lock


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "GAME" / "RULES" / "packages" / "hdm.rules.dnd2024-srd52-core"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class S6D08HealthEffectsRecoveryContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seed = load(PACKAGE / "character-mvp-seed.json")
        cls.contract = load(PACKAGE / "health-effects-recovery-seed.json")
        cls.actor_schema = load(ROOT / "DEV" / "SCHEMAS" / "world-actor-state.schema.json")
        cls.contract_schema = load(ROOT / "DEV" / "SCHEMAS" / "health-effects-recovery-seed.schema.json")
        cls.capabilities = load(PACKAGE / "character-capabilities.json")

    def test_hp_is_actor_intrinsic_not_generic_resource(self):
        support = {row["id"]: row for row in self.seed["support_definitions"]}
        self.assertNotIn("resource.hit_points", support)
        self.assertNotIn("resource.hit_points", self.seed["external_dependency_ids"])
        self.assertEqual(self.contract["authority"]["hp"], "ACTOR_STATE_HP")
        self.assertEqual(self.contract["authority"]["condition_aggregate"], "DERIVED_FROM_APPLICABLE_EFFECTS")

    def test_materialized_hp_requires_current_and_maximum_base(self):
        hp = self.actor_schema["$defs"]["hp"]
        self.assertEqual(set(hp["required"]), {"current", "maximum_base"})
        self.assertIn("life_state_policy_id", self.actor_schema["dependentRequired"]["hp"])

    def test_character_like_lifestate_transition_table_is_exact(self):
        transitions = self.contract["life_state_policy"]["transitions"]
        by_id = {row["transition_id"]: row for row in transitions}
        self.assertEqual(by_id["damage_to_zero"]["to"], "life.dying")
        self.assertEqual(by_id["healing_from_zero"]["to"], "life.active")
        self.assertEqual(by_id["third_death_save_success"]["to"], "life.stable")
        self.assertEqual(by_id["third_death_save_failure"]["to"], "life.dead")
        self.assertEqual(by_id["healing_from_zero"]["progress"], "CLEAR")
        self.assertIn("instant_death_massive_damage", by_id)
        self.assertIn("damage_at_zero", by_id)
        self.assertIn("death_save_natural_1", by_id)
        self.assertIn("death_save_natural_20", by_id)

    def test_damage_consumes_temporary_hp_before_current_hp(self):
        damage = self.contract["health_operations"]["damage"]
        self.assertEqual(damage["order"], ["hp.temporary", "hp.current"])
        self.assertEqual(damage["floor"], 0)
        self.assertEqual(damage["lifestate"], "POLICY_IN_SAME_EXECUTION_SEGMENT")

    def test_s6d07_resource_recovery_is_exact_and_owner_local(self):
        responders = {
            (row["resource_id"], row["boundary_id"]): row
            for row in self.contract["mechanical_recovery"]["resource_responders"]
        }
        self.assertEqual(responders[("resource.second_wind", "boundary.short_rest_complete")]["operation_id"], "resource_recovery.restore_amount")
        self.assertEqual(responders[("resource.second_wind", "boundary.short_rest_complete")]["amount"], 1)
        self.assertEqual(responders[("resource.second_wind", "boundary.long_rest_complete")]["operation_id"], "resource_recovery.restore_to_capacity")
        self.assertEqual(responders[("resource.action_surge", "boundary.short_rest_complete")]["owner"], "ACTOR_RESOURCE_STATE")
        self.assertEqual(responders[("resource.innate_sorcery", "boundary.long_rest_complete")]["owner"], "ACTOR_RESOURCE_STATE")
        self.assertEqual(responders[("resource.spell_slot.level_1", "boundary.long_rest_complete")]["owner"], "ACTOR_RESOURCE_STATE")
        self.assertEqual(self.contract["mechanical_recovery"]["rest_policy_authority"], "QUALIFY_AND_EMIT_COMPLETION_BOUNDARY_ONLY")

    def test_action_surge_entitlement_remains_procedure_state(self):
        self.assertEqual(self.contract["procedure_state"]["action_surge_entitlement"]["owner"], "RUNTIME_PROCEDURE_PARTICIPANT_RESOURCE")
        self.assertEqual(self.contract["procedure_state"]["action_surge_entitlement"]["expiry"], "boundary.turn_end")
        self.assertFalse(self.contract["procedure_state"]["action_surge_entitlement"]["persist_on_actor"])

    def test_effect_and_condition_owners_do_not_duplicate(self):
        effect = self.contract["effect_cases"]["effect.innate_sorcery"]
        self.assertEqual(effect["instance_owner"], "WORLD_EFFECT")
        self.assertEqual(effect["duration_owner"], "WORLD_EFFECT_TEMPORAL_BINDING")
        self.assertEqual(effect["due_index"], "DERIVED_DISPOSABLE_TEMPORAL_AGENDA")
        self.assertEqual(effect["reapplication"], "REPLACE_SAME_TARGET_SOURCE_DEFINITION_KEY")
        self.assertEqual(self.contract["condition_cases"]["condition.unconscious"]["storage"], "NO_ACTOR_CONDITION_LIST")
        self.assertEqual(self.contract["condition_cases"]["condition.exhaustion"]["selection_state"], "CONFORMANCE_ONLY_NONSELECTABLE")

    def test_periodic_trigger_and_generic_concentration_stay_nonselectable(self):
        negative = self.contract["negative_space"]
        self.assertEqual(negative["periodic_effect_content"], "ABSENT_NONSELECTABLE")
        self.assertEqual(negative["generic_concentration_content"], "CONFORMANCE_ONLY_NONSELECTABLE")
        self.assertEqual(negative["new_primitive_activation"], "NONE")

    def test_boundary_retry_and_durability_recovery_are_explicit(self):
        boundary = self.contract["boundary_execution"]
        self.assertEqual(boundary["idempotency_key"], ["occurrence_key", "responder_owner_id"])
        self.assertEqual(boundary["phase_order"], ["DISCOVER", "PROSPECTIVE_CLOSURE", "ATOMIC_COMMIT", "EVENT_AND_RECEIPT"])
        self.assertEqual(self.contract["durability_recovery"]["agenda"], "REBUILD_FROM_OWNER_BINDINGS")
        self.assertEqual(self.contract["durability_recovery"]["condition_aggregate"], "RECOMPUTE")
        self.assertEqual(self.contract["durability_recovery"]["missing_required_evidence"], "FAIL_CLOSED")

    def test_no_scheduler_queue_or_campaign_scan_authority(self):
        forbidden = set(self.contract["forbidden_authorities"])
        self.assertEqual(forbidden, {
            "BACKGROUND_SCHEDULER",
            "GLOBAL_EVENT_QUEUE",
            "CAMPAIGN_WIDE_BOUNDARY_SCAN",
            "REST_POLICY_CROSS_DOMAIN_MUTATION",
            "GENERIC_STATE_DELTA_OWNER",
            "MUTABLE_CONDITION_AGGREGATE",
        })

    def test_machine_seed_has_strict_schema_and_no_extra_fields(self):
        validate_seed_schema(self.contract, self.contract_schema)
        invalid = json.loads(json.dumps(self.contract))
        invalid["unexpected"] = True
        with self.assertRaises(ValueError):
            validate_seed_schema(invalid, self.contract_schema)

        mutations = []
        for path, replacement in (
            (("authority", "effect"), "ACTOR_STATE_EFFECTS"),
            (("life_state_policy", "transitions", 1, "from"), "life.active_or_dying"),
            (("life_state_policy", "stable_recovery", "rng"), "REROLL_1D4_HOURS"),
            (("effect_cases", "effect.innate_sorcery", "instance_owner"), "ACTOR_STATE"),
            (("mechanical_recovery", "resource_responders", 0, "owner"), "REST_POLICY"),
        ):
            value = json.loads(json.dumps(self.contract))
            cursor = value
            for token in path[:-1]:
                cursor = cursor[token]
            cursor[path[-1]] = replacement
            mutations.append(value)
        for invalid in mutations:
            with self.assertRaises(ValueError):
                validate_seed_schema(invalid, self.contract_schema)

    def test_canonical_schema_examples_are_valid(self):
        validator = CanonicalSchemaValidator(ROOT / "DEV" / "SCHEMAS")
        for schema_name in ("world-actor-state.schema.json", "world-effect-state.schema.json"):
            schema = load(ROOT / "DEV" / "SCHEMAS" / schema_name)
            for example in schema.get("examples", []):
                validator.validate(example, schema)

    def test_package_identity_binds_exact_closed_content_set(self):
        lock, _ = build_resolved_lock([PACKAGE], root_package_ids=["hdm.rules.dnd2024-srd52-core"], engine_version="1.0-alpha", catalog_generation="2.0.0")
        self.assertEqual(lock["ruleset_set_sha256"], "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143")
        self.assertIn("health-effects-recovery-seed.json", {row["path"] for row in lock["packages"][0]["members"]})
        self.assertFalse({"content_files", "content_set_sha256"}.intersection(self.capabilities))

    def test_policy_validator_rejects_missing_or_contradictory_health(self):
        valid = {"hp": {"current": 6, "maximum_base": 6, "temporary": 0}, "life_state_id": "life.active", "life_state_policy_id": "life_policy.dnd2024.character_like"}
        validate_actor_health(valid)
        for invalid in (
            {"hp": {"current": 6, "maximum_base": 6}, "life_state_id": "life.active"},
            {"hp": {"current": 0, "maximum_base": 6}, "life_state_id": "life.active", "life_state_policy_id": "life_policy.dnd2024.character_like"},
            {"hp": {"current": 1, "maximum_base": 6}, "life_state_id": "life.dying", "life_state_policy_id": "life_policy.dnd2024.character_like", "life_state_progress": {"death_saves": {"successes": 0, "failures": 0}}},
            {"hp": {"current": 1, "maximum_base": 6}, "life_state_id": "life.dead", "life_state_policy_id": "life_policy.dnd2024.character_like"},
        ):
            with self.assertRaises(ValueError):
                validate_actor_health(invalid)

    def test_damage_and_healing_reference_transitions_are_atomic_and_idempotent(self):
        actor = {"id": "actor.a", "hp": {"current": 8, "maximum_base": 8, "temporary": 3}, "life_state_id": "life.active", "life_state_policy_id": "life_policy.dnd2024.character_like"}
        receipts = {}
        first = apply_damage(actor, 5, "damage.1", receipts)
        retry = apply_damage(actor, 5, "damage.1", receipts)
        self.assertIs(first, retry)
        self.assertEqual(first["actor"]["hp"], {"current": 6, "maximum_base": 8, "temporary": 0})
        dying = apply_damage(first["actor"], 6, "damage.2", receipts)["actor"]
        self.assertEqual(dying["life_state_id"], "life.dying")
        dying_result = apply_damage(first["actor"], 6, "damage.2b", {})
        dying = dying_result["actor"]
        self.assertNotIn("effect_changes", dying)
        self.assertEqual(dying_result["world_effect_changes"]["create"][0]["definition_id"], "condition.unconscious")
        healed_result = apply_healing(dying, 2, "heal.1", receipts)
        healed = healed_result["actor"]
        self.assertEqual((healed["hp"]["current"], healed["life_state_id"]), (2, "life.active"))
        self.assertEqual(healed_result["world_effect_changes"]["terminate"], ["effect:life_state_unconscious:actor.a"])
        validate_actor_and_effect_outputs(dying_result, ROOT / "DEV" / "SCHEMAS")
        malformed = json.loads(json.dumps(dying_result))
        malformed["world_effect_changes"]["create"][0]["state"]["target_id"] = "not a valid id"
        with self.assertRaises(ValueError):
            validate_actor_and_effect_outputs(malformed, ROOT / "DEV" / "SCHEMAS")
        illegal_actor = json.loads(json.dumps(dying_result))
        illegal_actor["actor"]["effect_changes"] = {}
        with self.assertRaises(ValueError):
            validate_actor_and_effect_outputs(illegal_actor, ROOT / "DEV" / "SCHEMAS")

    def test_instant_death_and_damage_at_zero(self):
        actor = {"id": "actor.a", "hp": {"current": 4, "maximum_base": 8}, "life_state_id": "life.active", "life_state_policy_id": "life_policy.dnd2024.character_like"}
        dead = apply_damage(actor, 12, "damage.massive", {})["actor"]
        self.assertEqual(dead["life_state_id"], "life.dead")
        dying = apply_damage(actor, 4, "damage.zero", {})["actor"]
        once = apply_damage(dying, 1, "damage.at_zero.1", {})["actor"]
        self.assertEqual(once["life_state_progress"]["death_saves"]["failures"], 1)
        critical = apply_damage(once, 1, "damage.at_zero.critical", {}, critical=True)["actor"]
        self.assertEqual(critical["life_state_id"], "life.dead")
        massive_at_zero = apply_damage(dying, 8, "damage.at_zero.massive", {})["actor"]
        self.assertEqual(massive_at_zero["life_state_id"], "life.dead")
        stable = json.loads(json.dumps(dying))
        stable["life_state_id"] = "life.stable"
        stable["life_state_progress"] = {"recovery_binding": {"basis_id": "temporal.metric_deadline", "context_id": "scene.a", "anchor_value": 0, "deadline_value": 1, "unit_id": "unit.hour"}}
        stable_hit = apply_damage(stable, 1, "damage.stable", {})["actor"]
        self.assertEqual(stable_hit["life_state_id"], "life.dying")
        self.assertEqual(stable_hit["life_state_progress"]["death_saves"]["failures"], 1)
        stable_critical = apply_damage(stable, 1, "damage.stable.critical", {}, critical=True)["actor"]
        self.assertEqual(stable_critical["life_state_progress"]["death_saves"]["failures"], 2)
        stable_massive = apply_damage(stable, 8, "damage.stable.massive", {})["actor"]
        self.assertEqual(stable_massive["life_state_id"], "life.dead")

    def test_death_save_natural_results_and_stable_recovery_retry(self):
        dying = {"id": "actor.a", "hp": {"current": 0, "maximum_base": 8}, "life_state_id": "life.dying", "life_state_policy_id": "life_policy.dnd2024.character_like", "life_state_progress": {"death_saves": {"successes": 1, "failures": 0}}}
        self.assertEqual(apply_death_save(dying, 1, "save.1", {})["actor"]["life_state_progress"]["death_saves"]["failures"], 2)
        active = apply_death_save(dying, 20, "save.20", {})["actor"]
        self.assertEqual((active["hp"]["current"], active["life_state_id"]), (1, "life.active"))
        stable_result = apply_death_save(apply_death_save(dying, 12, "save.2", {})["actor"], 12, "save.3", {})
        stable = stable_result["actor"]
        self.assertEqual(stable["life_state_id"], "life.stable")
        self.assertEqual(stable_result["receipt"]["fixed_rng"], {"die": "1d4", "result": 1})
        receipts = {}
        recovered = recover_stable_actor(stable, "stable.due", receipts)
        self.assertIs(recovered, recover_stable_actor(stable, "stable.due", receipts))
        self.assertEqual((recovered["actor"]["hp"]["current"], recovered["actor"]["life_state_id"]), (1, "life.active"))

    def test_maximum_change_and_integer_resource_invariants(self):
        actor = {"id": "actor.a", "hp": {"current": 8, "maximum_base": 8, "temporary": 4}, "life_state_id": "life.active", "life_state_policy_id": "life_policy.dnd2024.character_like"}
        reduced = apply_maximum_change(actor, -5, "max.1", {})["actor"]
        self.assertEqual(reduced["hp"], {"current": 3, "maximum_base": 8, "maximum_adjustment": -5, "temporary": 4})
        dead = apply_maximum_change(reduced, -3, "max.2", {})["actor"]
        self.assertEqual(dead["life_state_id"], "life.dead")
        validate_resource_instances({"resource.second_wind": {"current": 1}}, {"resource.second_wind": {"lifetime_owner": "actor", "capacity": 1}})
        for state in ({"current": 1.5}, {"current": 2}, {"current": -1}):
            with self.assertRaises(ValueError):
                validate_resource_instances({"resource.second_wind": state}, {"resource.second_wind": {"lifetime_owner": "actor", "capacity": 1}})

    def test_boundary_reference_execution_deduplicates_and_fails_closed(self):
        resources = {"resource.second_wind": {"current": 0}, "resource.innate_sorcery": {"current": 0}}
        capacities = {"resource.second_wind": 1, "resource.innate_sorcery": 2}
        receipts = {}
        short = apply_boundary(resources, capacities, "boundary.short_rest_complete", "rest:1", "actor.a", self.contract, receipts)
        self.assertIs(short, apply_boundary(resources, capacities, "boundary.short_rest_complete", "rest:1", "actor.a", self.contract, receipts))
        self.assertEqual(short["resources"]["resource.second_wind"]["current"], 1)
        self.assertEqual(short["resources"]["resource.innate_sorcery"]["current"], 0)
        with self.assertRaises(ValueError):
            apply_boundary(resources, capacities, "boundary.unknown", "bad:1", "actor.a", self.contract, {})

    def test_effect_replace_expiry_and_support_loss_are_idempotent(self):
        effects = {}
        receipts = {}
        first = apply_effect(effects, "effect.innate_sorcery", "actor.a", "actor.a", "effect.1", receipts)
        self.assertIs(first, apply_effect(effects, "effect.innate_sorcery", "actor.a", "actor.a", "effect.1", receipts))
        replaced = apply_effect(first["effects"], "effect.innate_sorcery", "actor.a", "actor.a", "effect.2", receipts)
        self.assertEqual(set(replaced["effects"]), {"effect.1", "effect.2"})
        self.assertEqual(replaced["effects"]["effect.1"]["state"]["lifecycle"]["terminal_reason_id"], "effect_end.replaced")
        self.assertEqual(replaced["effects"]["effect.2"]["definition_id"], "effect.innate_sorcery")
        self.assertNotIn("definition_id", replaced["effects"]["effect.2"]["state"])
        self.assertNotIn("instance_key", replaced["effects"]["effect.2"]["state"])
        expired = expire_effect(replaced["effects"], "effect.2", "expiry.1", receipts)
        self.assertEqual(expired["effects"]["effect.2"]["state"]["lifecycle"]["terminal_reason_id"], "effect_end.expired")
        support = {
            "effect.root": {"id": "effect.root", "kind": "world.effect", "definition_id": "condition.unconscious", "state": {"target_id": "actor.a", "lifecycle": {"state_id": "effect_lifecycle.active"}}},
            "effect.child": {"id": "effect.child", "kind": "world.effect", "definition_id": "condition.unconscious", "state": {"target_id": "actor.a", "support_effect_id": "effect.root", "lifecycle": {"state_id": "effect_lifecycle.active"}}},
        }
        ended = terminate_support_tree(support, "effect.root", "support.1", {})
        self.assertEqual(ended["effects"]["effect.child"]["state"]["lifecycle"]["terminal_reason_id"], "effect_end.support_lost")

        validator = CanonicalSchemaValidator(ROOT / "DEV" / "SCHEMAS")
        world_schema = validator.schemas["https://hedgelion.invalid/schemas/world-record.schema.json"]
        for result in (first, replaced, expired, ended):
            for effect_id, record in result["effects"].items():
                self.assertEqual(record["id"], effect_id)
                validator.validate(record, world_schema)
        legacy_flat = {"definition_id": "effect.innate_sorcery", "instance_key": ["actor.a", "actor.a", "effect.innate_sorcery"], "target_id": "actor.a", "lifecycle": {"state_id": "effect_lifecycle.active"}}
        with self.assertRaises(SchemaViolation):
            validator.validate(legacy_flat, world_schema)

    def test_recovery_rebuilds_derivatives_and_fails_on_missing_binding(self):
        effects = {
            "effect.1": {
                "id": "effect.1",
                "kind": "world.effect",
                "definition_id": "effect.innate_sorcery",
                "state": {
                    "target_id": "actor.a",
                    "temporal_binding": {"basis_id": "temporal.metric_deadline", "context_id": "scene.a", "anchor_value": 0, "deadline_value": 60, "unit_id": "unit.second"},
                    "lifecycle": {"state_id": "effect_lifecycle.active"},
                },
            }
        }
        rebuilt = reconstruct_derived_state(effects)
        self.assertEqual(rebuilt["agenda"], [("effect.1", 60)])
        self.assertEqual(rebuilt["conditions"], {})
        invalid = json.loads(json.dumps(effects))
        del invalid["effect.1"]["state"]["temporal_binding"]
        with self.assertRaises(ValueError):
            reconstruct_derived_state(invalid, required_timed_definition_ids={"effect.innate_sorcery"})

    def test_exact_life_state_inventory_includes_stable_at_zero(self):
        transitions = {row["transition_id"]: row for row in self.contract["life_state_policy"]["transitions"]}
        self.assertEqual(transitions["damage_at_zero"]["from"], "life.dying_or_stable")
        self.assertEqual(transitions["instant_death_massive_damage"]["from"], "life.active_or_dying_or_stable")


if __name__ == "__main__":
    unittest.main()
