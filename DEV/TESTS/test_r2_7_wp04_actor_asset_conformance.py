import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class R27WP04ActorAssetConformanceTests(unittest.TestCase):
    def load_json(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_actor_state_has_one_typed_non_epistemic_continuity_owner(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        props = actor["properties"]
        self.assertIn("continuity", props)
        for duplicate in ("knowledge", "beliefs", "suspicions", "inventory", "conditions", "active_effects"):
            self.assertNotIn(duplicate, props)

        continuity = actor["$defs"]["continuity"]
        self.assertFalse(continuity["additionalProperties"])
        self.assertEqual(set(continuity["properties"]), {"foundation", "evolving", "relationships"})
        self.assertNotIn("transient_private", continuity["properties"])

    def test_actor_continuity_is_sparse_and_does_not_store_hidden_reasoning(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        evolving = actor["$defs"]["evolvingContinuity"]
        self.assertEqual(
            set(evolving["properties"]),
            {
                "long_term_goal",
                "current_objective",
                "next_intention",
                "material_commitments",
                "reconsideration_cues",
            },
        )
        serialized = json.dumps(actor)
        for forbidden in ("chain_of_thought", "reasoning_trace", "plan_graph", "strategy_dag"):
            self.assertNotIn(forbidden, serialized)

    def test_directed_relationships_are_source_actor_local_sparse_views(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        view = actor["$defs"]["relationshipView"]
        facets = view["properties"]["facets"]
        self.assertEqual(
            set(facets["properties"]),
            {"trust", "affinity", "fear", "respect", "hostility", "felt_obligation"},
        )
        self.assertTrue(facets["minProperties"] >= 1)
        self.assertFalse(facets["additionalProperties"])
        self.assertEqual(actor["$defs"]["relationshipLevel"]["enum"], ["low", "moderate", "high"])

    def test_actor_machine_inventory_exposes_continuity_but_no_generic_relationship_record(self):
        structures = self.load_json("DEV/CATALOG/entity-structures.json")
        actor = structures["world_records"]["world.actor"]
        self.assertIn("continuity", actor["expected"])
        self.assertNotIn("world.relationship", structures["world_records"])

    def test_provisional_actor_does_not_require_name_and_has_typed_concept_anchor(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        self.assertNotIn("name", actor.get("required", []))
        self.assertIn("concept", actor["properties"])

        structures = self.load_json("DEV/CATALOG/entity-structures.json")
        inventory = structures["world_records"]["world.actor"]
        self.assertNotIn("name", inventory["required"])
        self.assertIn("name", inventory["expected"])
        self.assertIn("concept", inventory["expected"])

    def test_actor_build_stores_only_instance_owned_reconstruction_choices(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        build = actor["$defs"]["build"]
        self.assertEqual(
            set(build["properties"]),
            {"species_id", "background_id", "class_progression", "choice_bindings", "spellcasting"},
        )
        self.assertIn("class_progression", build["required"])
        self.assertNotIn("level", build["properties"])
        self.assertNotIn("class_id", build["properties"])
        self.assertNotIn("subclass_id", build["properties"])

        progression = actor["$defs"]["classProgression"]
        self.assertTrue(progression["minItems"] >= 1)
        entry = actor["$defs"]["classProgressionEntry"]
        self.assertEqual(set(entry["required"]), {"class_id", "level"})

        spellcasting = actor["$defs"]["spellcastingState"]
        self.assertEqual(
            set(spellcasting["properties"]),
            {"known_spell_ids", "prepared_spell_ids", "spellbook_spell_ids"},
        )
        serialized = json.dumps(build)
        for derived in ("armor_class", "attack_bonus", "save_bonus", "proficiency_bonus", "derived"):
            self.assertNotIn(derived, serialized)

    def test_campaign_actor_name_does_not_require_an_english_translation(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        text = actor["$defs"]["localizedText"]
        self.assertNotIn("required", text)
        self.assertEqual(text["minProperties"], 1)

    def test_asset_state_keeps_single_placement_and_no_epistemic_aliases(self):
        asset = self.load_json("DEV/SCHEMAS/world-asset-state.schema.json")
        props = asset["properties"]
        for stale in ("identified_by_pc_ids", "secret_ids", "inventory", "contents", "legal_owner_id"):
            self.assertNotIn(stale, props)
        for placement in ("owner_actor_id", "container_asset_id", "location_id"):
            self.assertIn(placement, props)
        self.assertIn("resources", props)
        self.assertIn("durability", props)

    def test_hp_resource_effect_authority_separation_is_preserved(self):
        actor = self.load_json("DEV/SCHEMAS/world-actor-state.schema.json")
        hp = actor["$defs"]["hp"]["properties"]
        self.assertEqual(set(hp), {"current", "maximum_base", "maximum_adjustment", "temporary"})
        resource = actor["$defs"]["resourceState"]["properties"]
        self.assertNotIn("hp", resource)
        self.assertNotIn("temporary_hp", resource)

        effect = self.load_json("DEV/SCHEMAS/world-effect-state.schema.json")
        effect_props = effect["properties"]
        for duplicate in ("condition_present", "condition_value", "remaining_duration", "winner", "shadow_state"):
            self.assertNotIn(duplicate, effect_props)


if __name__ == "__main__":
    unittest.main()
