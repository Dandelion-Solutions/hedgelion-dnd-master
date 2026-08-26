import json
import hashlib
import unittest
from pathlib import Path
from DEV.TOOLS.validate_character_mvp_seed import advance_fighter_to_level_2, create_innate_sorcery_effect_candidate, evaluate_ready_pc, resolve_package, validate_primitive_argument


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "GAME" / "RULES" / "packages" / "hdm.rules.dnd2024-srd52-core"


class CharacterMvpSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PACKAGE / "character-capabilities.json").read_text(encoding="utf-8"))
        cls.seed = json.loads((PACKAGE / "character-mvp-seed.json").read_text(encoding="utf-8"))
        cls.primitive_catalog = json.loads(
            (ROOT / "DEV" / "CATALOG" / "activity-primitive-contracts.json").read_text(encoding="utf-8")
        )
        cls.actors = json.loads(
            (ROOT / "DEV" / "TESTS" / "fixtures" / "s6d-07-character-mvp-actors.json").read_text(encoding="utf-8")
        )
        cls.resolved = resolve_package(PACKAGE, cls.primitive_catalog)

    def test_capability_claim_is_bounded_and_honest(self):
        self.assertEqual(self.manifest["package_id"], "hdm.rules.dnd2024-srd52-core")
        content = (PACKAGE / self.manifest["content_file"]).read_bytes()
        self.assertEqual(hashlib.sha256(content).hexdigest(), self.manifest["content_sha256"])
        self.assertEqual(self.manifest["profile_id"], "character.mvp_vertical_slice.v1")
        self.assertFalse(self.manifest["full_srd_character_corpus"])
        self.assertEqual(self.manifest["unsupported_content_policy"], "ABSENT_NONSELECTABLE")
        self.assertEqual(self.manifest["supported_class_levels"], {"class.fighter": [1, 2], "class.sorcerer": [1]})

    def test_exact_definition_inventory_and_reference_closure(self):
        definitions = self.seed["definitions"]
        ids = [item["id"] for item in definitions]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 24)
        realized_dependencies = (
            {item["id"] for item in self.seed["support_definitions"]}
            | {item["id"] for item in self.seed["activity_definitions"]}
            | set(self.seed["value_registrations"])
        )
        self.assertEqual(set(self.seed["external_dependency_ids"]), realized_dependencies)
        admitted = set(ids) | realized_dependencies
        for item in definitions:
            for ref in item.get("references", []):
                self.assertIn(ref, admitted, f"unresolved reference {ref} from {item['id']}")

    def test_real_material_and_defaulted_choices_are_both_present(self):
        slots = [slot for item in self.seed["definitions"] for slot in item.get("choice_slots", [])]
        policies = {slot["decision_policy"] for slot in slots}
        self.assertIn("choice.player_or_delegated", policies)
        self.assertIn("choice.deterministic_default", policies)
        for slot in slots:
            self.assertLessEqual(slot["minimum"], slot["maximum"])
            option_ids = [option["option_id"] for option in slot["options"]]
            self.assertEqual(len(option_ids), len(set(option_ids)))
            self.assertTrue(set(slot.get("default_option_ids", [])).issubset(option_ids))

    def test_ready_pc_is_dependency_closure_not_questionnaire_completion(self):
        readiness = self.seed["ready_pc"]
        self.assertTrue(readiness["provisional_gameplay_before_ready_pc"])
        self.assertEqual(readiness["open_material_initial_choice"], "BLOCKING")
        self.assertEqual(readiness["future_advancement_choice"], "NONBLOCKING_UNTIL_BOUNDARY")
        self.assertNotIn("all_profile_fields_answered", readiness["required_evidence"])

    def test_only_necessity_challenged_primitives_are_activated(self):
        expected = {"op.select_targets", "op.roll", "op.resolve_attack", "op.resolve_save", "op.apply_damage", "op.apply_healing", "op.consume_resource", "op.for_each_target", "op.resolve_check", "op.create_effect", "op.emit_fact"}
        active_rows = [row for row in self.primitive_catalog["contracts"] if row["selection_state"] == "ACTIVE_ADMITTED"]
        actual = {row["primitive_id"] for row in active_rows}
        self.assertEqual(actual, expected)
        consumers = {ref for item in self.seed["definitions"] for ref in item.get("primitive_dependencies", [])}
        self.assertTrue(consumers.issubset(actual))
        for row in active_rows:
            self.assertEqual(row["realization_state"], "COMPLETE")
            matrix = self.primitive_catalog["primitive_validation_matrix"][row["primitive_id"]]
            expected_segment = "CHILD_STEPS_DEFINE_SEGMENTS" if row["execution_kind"] == "COMPILER_FORM" else "ONE_SEGMENT"
            self.assertEqual(matrix["segment_semantics"], expected_segment)

    def test_every_referenced_activity_is_real_and_compiles_against_base_contract(self):
        activities = {item["id"]: item for item in self.seed["activity_definitions"]}
        referenced = {
            ref for item in self.seed["definitions"]
            for ref in item.get("references", []) if ref.startswith("activity.")
        }
        self.assertEqual(set(activities), referenced)
        contracts = {row["primitive_id"]: row for row in self.primitive_catalog["contracts"]}
        for activity in activities.values():
            self.assertEqual(activity["kind"], "definition.activity")
            self.assertTrue(activity["data"]["family_id"].startswith("activity."))
            self.assertTrue(activity["data"]["steps"])
            for step in activity["data"]["steps"]:
                contract = contracts[step["op"]]
                self.assertEqual(contract["realization_state"], "COMPLETE")
                self.assertEqual(contract["selection_state"], "ACTIVE_ADMITTED")
                self.assertFalse(set(step.get("args", {})) - set(contract["arguments"]))
                required = {name for name, spec in contract["arguments"].items() if spec["required"]}
                self.assertTrue(required.issubset(step.get("args", {})))
        actual_consumers = {}
        def walk(steps, activity_id):
            for step in steps:
                actual_consumers.setdefault(step["op"], set()).add(activity_id)
                if step["op"] == "op.for_each_target":
                    self.assertTrue(step["args"]["steps"])
                    walk(step["args"]["steps"], activity_id)
        for activity_id, activity in activities.items():
            walk(activity["data"]["steps"], activity_id)
        for primitive_id, consumer_ids in actual_consumers.items():
            self.assertEqual(set(contracts[primitive_id]["exact_seed_consumer_ids"]), consumer_ids)

    def test_advancement_proof_is_bounded_and_reconstructable(self):
        proof = self.seed["advancement_proof"]
        self.assertEqual((proof["class_id"], proof["from_level"], proof["to_level"]), ("class.fighter", 1, 2))
        self.assertEqual(proof["publication"], "ATOMIC_IDEMPOTENT_ACTOR_RECONSTRUCTION")
        self.assertFalse(proof["reopens_initial_choices"])

    def test_actor_fixtures_use_sparse_owner_relative_bindings(self):
        for name in ("fighter_ready", "fighter_unresolved_style", "sorcerer_ready"):
            actor = self.actors[name]
            self.assertIn("class_progression", actor["build"])
            self.assertNotIn("flattened_sheet", actor)
            for binding in actor["build"].get("choice_bindings", {}).values():
                self.assertTrue(binding["selected_option_ids"])
                self.assertTrue(binding["selection_basis"].startswith("choice_basis."))

    def test_readiness_returns_exact_blocker_and_preserves_provisional_play(self):
        self.assertTrue(evaluate_ready_pc(self.actors["fighter_ready"], self.resolved, self.actors["readiness_evidence"]["fighter"])["ready"])
        self.assertTrue(evaluate_ready_pc(self.actors["sorcerer_ready"], self.resolved, self.actors["readiness_evidence"]["sorcerer"])["ready"])
        result = evaluate_ready_pc(self.actors["fighter_unresolved_style"], self.resolved, self.actors["readiness_evidence"]["fighter"])
        self.assertFalse(result["ready"])
        self.assertIn("advancement.fighter.level_1.style", result["blockers"])
        self.assertTrue(self.seed["ready_pc"]["provisional_gameplay_before_ready_pc"])

    def test_advancement_trace_has_existing_owner_boundaries_and_retry_evidence(self):
        receipts = {}
        trace = advance_fighter_to_level_2(
            self.actors["fighter_ready"], "command.advance.mvp-archer.level-2",
            "actor.mvp-archer:class.fighter:1:2", receipts,
        )
        retry = advance_fighter_to_level_2(
            self.actors["fighter_ready"], "command.advance.mvp-archer.level-2",
            "actor.mvp-archer:class.fighter:1:2", receipts,
        )
        self.assertIs(trace, retry)
        self.assertEqual(trace["after_actor"]["build"]["class_progression"][0]["level"], 2)
        self.assertEqual(trace["execution_segment"]["disposition"], "COMMITTED")
        self.assertEqual(trace["mechanical_event"]["kind"], "event.character.advanced")
        self.assertEqual(trace["receipt"]["outcome"], "COMPLETED")
        self.assertIsNone(trace["continuation"])
        self.assertEqual(trace["after_actor"]["build"]["choice_bindings"], self.actors["fighter_ready"]["build"]["choice_bindings"])

    def test_spell_binding_mismatch_blocks_ready_pc(self):
        actor = json.loads(json.dumps(self.actors["sorcerer_ready"]))
        actor["build"]["spellcasting"]["known_spell_ids"] = ["spell.fire_bolt"]
        result = evaluate_ready_pc(actor, self.resolved, self.actors["readiness_evidence"]["sorcerer"])
        self.assertFalse(result["ready"])
        self.assertIn("spell_selection_binding_mismatch", result["blockers"])

    def test_missing_transitive_readiness_evidence_blocks(self):
        result = evaluate_ready_pc(self.actors["sorcerer_ready"], self.resolved, {"owned_asset_definition_ids": []})
        self.assertFalse(result["ready"])
        self.assertIn("owned_assets", result["blockers"])
        self.assertIn("admitted_spell_activities", result["blockers"])

    def test_unbound_or_forged_readiness_attestation_blocks(self):
        evidence = json.loads(json.dumps(self.actors["readiness_evidence"]["fighter"]))
        evidence["actor_state_revision"] = 999
        evidence["selector_results"]["defense.armor_class"] = 30
        result = evaluate_ready_pc(self.actors["fighter_ready"], self.resolved, evidence)
        self.assertFalse(result["ready"])
        self.assertIn("readiness_actor_identity_or_revision", result["blockers"])
        self.assertIn("derived_defense", result["blockers"])

    def test_action_surge_and_innate_sorcery_have_typed_owner_contracts(self):
        activities = {item["id"]: item["data"] for item in self.seed["activity_definitions"]}
        surge = activities["activity.feature.action_surge"]
        self.assertEqual([step["op"] for step in surge["steps"]], ["op.consume_resource", "op.emit_fact"])
        entitlement = surge["steps"][1]["args"]
        self.assertEqual(entitlement["scope"], "CURRENT_TURN")
        self.assertEqual(entitlement["consumption"], "NEXT_ELIGIBLE_ACTIVATION")
        self.assertEqual(entitlement["excluded_activity_family_ids"], ["activity.magic"])
        effect = self.resolved["resolved_catalog"]["effect.innate_sorcery"]["data"]
        self.assertEqual(effect["reapplication"]["match_policy_id"], "effect_reapplication_match.target_family_source")
        self.assertEqual(effect["reapplication"]["action_id"], "effect_reapplication.replace")
        self.assertEqual(effect["details"]["cleanup"], "TEMPORAL_AGENDA_EMITS_IDEMPOTENT_EXPIRY_TRANSITION")

    def test_innate_sorcery_effect_contract_rejects_identity_role_and_duration_drift(self):
        invalid = [
            ("effect_definition_ref", "effect.some_other_effect"),
            ("target_role", "target"),
            ("source_role", "source"),
            ("duration", {"kind_id": "duration.metric", "amount": 2, "unit_id": "unit.minute"}),
        ]
        for argument_name, value in invalid:
            with self.assertRaises(ValueError):
                validate_primitive_argument(self.primitive_catalog, "op.create_effect", argument_name, value)

    def test_innate_sorcery_effect_identity_and_retry_are_stable(self):
        recovered = {}
        first = create_innate_sorcery_effect_candidate("actor.mvp-innate-mage", "resolution.innate-1", "scene.mvp", recovered)
        retry = create_innate_sorcery_effect_candidate("actor.mvp-innate-mage", "resolution.innate-1", "scene.mvp", recovered)
        replacement = create_innate_sorcery_effect_candidate("actor.mvp-innate-mage", "resolution.innate-2", "scene.mvp", recovered)
        self.assertIs(first, retry)
        self.assertEqual(first["instance_key"], replacement["instance_key"])
        self.assertEqual(first["temporal_binding"]["duration"], {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.minute"})
        self.assertEqual(replacement["reapplication"], "ATOMIC_REPLACE_SAME_INSTANCE_KEY")


if __name__ == "__main__":
    unittest.main()
