import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG_VERSION = "2.0.0"


class R27WP03CatalogConformanceTests(unittest.TestCase):
    def load_json(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_catalog_generation_is_coherent(self):
        versions = {
            self.load_json("DEV/CATALOG/core-catalog.json")["catalog_version"],
            self.load_json("DEV/CATALOG/entity-structures.json")["catalog_version"],
            self.load_json("DEV/CATALOG/identifier-policies.json")["catalog_version"],
            self.load_json("DEV/CATALOG/mechanical-surfaces.json")["catalog_version"],
        }
        self.assertEqual(versions, {CATALOG_VERSION})

    def test_accepted_record_classes_replace_stale_generic_owners(self):
        core = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        self.assertNotIn("world.relationship", core["world_record_kinds"])
        self.assertIn("runtime.disclosure", core["runtime_record_kinds"])
        self.assertIn("runtime.collaboration_obligation", core["runtime_record_kinds"])
        self.assertNotIn("transition.relationship_change", core["transition_kinds"])
        self.assertNotIn("event.relationship.changed", core["event_kinds"])

    def test_step4_information_vocabulary_is_explicit(self):
        r = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        self.assertEqual(
            r["truth_statuses"],
            ["truth.undetermined", "truth.established", "truth.disproven"],
        )
        self.assertEqual(
            r["lore_record_statuses"],
            ["lore_record.active", "lore_record.superseded"],
        )
        self.assertEqual(
            r["epistemic_stances"],
            [
                "epistemic.aware",
                "epistemic.known",
                "epistemic.believed",
                "epistemic.suspected",
                "epistemic.rejected",
            ],
        )
        self.assertEqual(
            r["disclosure_aspects"],
            ["disclosure.statement", "disclosure.objective_status"],
        )
        self.assertNotIn("knowledge_modes", r)

    def test_step5_durability_and_publication_are_not_old_intrinsic_classes(self):
        r = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        self.assertNotIn("canonicality_classes", r)
        self.assertNotIn("durability_classes", r)
        self.assertNotIn("publication_states", r)
        self.assertEqual(
            r["semantic_survival_states"],
            ["survival.ephemeral", "survival.established"],
        )
        self.assertEqual(
            r["current_durability_states"],
            ["durability.durable", "durability.volatile_dirty"],
        )
        self.assertEqual(
            r["durability_obligation_kinds"],
            ["durability.may_defer", "durability.must_be_durable_before"],
        )
        self.assertEqual(
            r["repository_ref_outcomes"],
            [
                "repository_ref.confirmed_accepted",
                "repository_ref.confirmed_rejected",
                "repository_ref.indeterminate",
            ],
        )

    def test_round2_closed_vocabulary_is_registered_without_new_authority(self):
        r = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        expected = {
            "actor_continuity_lifetimes": {
                "actor_continuity.foundation",
                "actor_continuity.durable_evolving",
                "actor_continuity.transient_private",
            },
            "actor_cognition_purposes": {
                "cognition.react",
                "cognition.reflect",
                "cognition.plan",
                "cognition.reconsider",
                "cognition.relationship_update",
            },
            "actor_relationship_facets": {
                "relationship.trust",
                "relationship.affinity",
                "relationship.fear",
                "relationship.respect",
                "relationship.hostility",
                "relationship.felt_obligation",
            },
            "logical_roles": {
                "role.interpreter",
                "role.dramaturg",
                "role.actor",
                "role.narrator",
                "role.chronicler",
                "role.commentator",
            },
            "context_discovery_channels": {
                "context.current_scope",
                "context.scene_manifest",
                "context.explicit_ref",
                "context.active_dependency",
                "context.live_current",
                "context.index_lookup",
                "context.history_hint",
            },
            "context_representation_classes": {
                "context.exact",
                "context.full_structured",
                "context.compact_structured",
                "context.summary",
                "context.reference_only",
            },
            "context_assembly_outcomes": {
                "context.assembled",
                "context.assembled_degraded",
                "context.unsatisfiable",
            },
            "story_service_outcomes": {
                "story_service.no_backlog",
                "story_service.service",
                "story_service.defer",
            },
            "collaboration_coordination_families": {
                "collaboration.independent_immediate",
                "collaboration.agency_dependent_collective",
                "collaboration.rule_owned_ordered",
            },
            "input_semantic_classes": {
                "input.ooc_coordination",
                "input.diegetic_communication",
                "input.actionable_intent",
                "input.control_signal",
            },
            "collaboration_states": {
                "collaboration.open",
                "collaboration.closed",
                "collaboration.resolved",
                "collaboration.obsolete",
            },
            "planning_entry_classes": {
                "planning.source_anchored_constraint",
                "planning.provisional_dramaturgic_direction",
            },
        }
        for registry, values in expected.items():
            self.assertEqual(set(r[registry]), values)

    def test_later_typed_handoffs_are_protocol_values_not_records(self):
        r = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        protocol = set(r["protocol_value_kinds"])
        required = {
            "value.epistemic_delta",
            "value.role_context_request",
            "value.context_need_profile",
            "value.role_context_bundle",
            "value.context_trace",
            "value.context_budget_envelope",
            "value.turn_envelope",
            "value.interpreter_result",
            "value.preparation_draft",
            "value.actor_proposal",
            "value.story_projection_draft",
            "value.narration_result",
            "value.story_service_decision",
        }
        self.assertTrue(required <= protocol)
        records = set(r["runtime_record_kinds"]) | set(r["world_record_kinds"])
        self.assertTrue(required.isdisjoint(records))

    def test_lore_and_knowledge_inventory_follow_step4(self):
        structures = self.load_json("DEV/CATALOG/entity-structures.json")
        world = structures["world_records"]
        self.assertNotIn("world.relationship", world)
        self.assertEqual(
            world["world.knowledge"]["required"],
            ["knower_id", "fact_id", "stance"],
        )
        self.assertIn("supporting_source_refs", world["world.knowledge"]["expected"])
        self.assertEqual(
            world["world.lore_fact"]["required"],
            ["statement", "truth_status", "record_status"],
        )

    def test_relation_owner_identifiers_are_semantic_composite_keys(self):
        policies = self.load_json("DEV/CATALOG/identifier-policies.json")
        self.assertNotIn("world.relationship", policies["world"])
        self.assertEqual(
            policies["world"]["world.knowledge"],
            {
                "strategy": "composite_key",
                "fields": ["knower_id", "fact_id"],
                "scope": "campaign",
            },
        )
        self.assertEqual(
            policies["runtime"]["runtime.disclosure"],
            {
                "strategy": "composite_key",
                "fields": ["player_id", "fact_id"],
                "scope": "campaign",
            },
        )
        self.assertIn("runtime.collaboration_obligation", policies["runtime"])


if __name__ == "__main__":
    unittest.main()
