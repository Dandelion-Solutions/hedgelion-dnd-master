import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
CATALOG_GENERATION = 2
WORLD_RECORD_FAMILIES = {
    "world.actor",
    "world.actor_group",
    "world.asset",
    "world.location",
    "world.connection",
    "world.zone",
    "world.organization",
    "world.contract",
    "world.mission",
    "world.scene",
    "world.encounter",
    "world.hazard",
    "world.effect",
    "world.lore_fact",
    "world.knowledge",
    "world.thread",
    "world.player",
}
RUNTIME_RECORD_FAMILIES = {
    "runtime.session",
    "runtime.message",
    "runtime.interaction",
    "runtime.procedure",
    "runtime.intent_plan",
    "runtime.command",
    "runtime.resolution",
    "runtime.continuation",
    "runtime.mechanical_event",
    "runtime.semantic_event",
    "runtime.resolution_trace",
    "runtime.disclosure",
    "runtime.collaboration_obligation",
    "runtime.checkpoint",
    "runtime.id_allocator",
    "runtime.maintenance_audit",
    "runtime.catalog_gap_report",
}


class R27WP03CatalogConformanceTests(unittest.TestCase):
    def load_json(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_catalog_generation_is_coherent(self):
        generations = {
            self.load_json("DEV/CATALOG/core-catalog.json")["catalog_generation"],
            self.load_json("DEV/CATALOG/entity-structures.json")["catalog_generation"],
            self.load_json("DEV/CATALOG/identifier-policies.json")["catalog_generation"],
            self.load_json("DEV/CATALOG/mechanical-surfaces.json")["catalog_generation"],
        }
        self.assertEqual(generations, {CATALOG_GENERATION})

    def test_exact_world_and_runtime_record_censuses_remain_closed(self):
        registries = self.load_json("DEV/CATALOG/core-catalog.json")["registries"]
        self.assertEqual(set(registries["world_record_kinds"]), WORLD_RECORD_FAMILIES)
        self.assertEqual(
            set(registries["runtime_record_kinds"]), RUNTIME_RECORD_FAMILIES
        )
        self.assertEqual(len(registries["world_record_kinds"]), 17)
        self.assertEqual(len(registries["runtime_record_kinds"]), 17)
        self.assertNotIn("world.faction", registries["world_record_kinds"])
        self.assertIn("organization.faction", registries["organization_facets"])

    def test_world_admission_shard_matches_the_final_core_registry(self):
        core_world = set(
            self.load_json("DEV/CATALOG/core-catalog.json")["registries"][
                "world_record_kinds"
            ]
        )
        shard = self.load_json(
            "DEV/CATALOG/catalog-admission-ledger/families/world_record_kinds.json"
        )
        census = shard["registry_census"]
        admitted_ids = {
            entry["id"]
            for entry in shard["entries"]
            if entry["admission_disposition"] == "ACTIVE_ADMITTED"
        }
        self.assertEqual(shard["registry_family"], "world_record_kinds")
        self.assertEqual(census["count"], len(WORLD_RECORD_FAMILIES))
        self.assertEqual(census["admitted"], len(WORLD_RECORD_FAMILIES))
        self.assertEqual(admitted_ids, core_world)
        self.assertEqual({entry["id"] for entry in shard["entries"]}, core_world)

    def test_identifier_policy_schema_v3_matches_the_exact_w03_live_birth_table(self):
        from GAME.TOOLS.live_state import (
            LIVE_BIRTH_ADMISSION_TABLE,
            SOURCE_NATIVE_LIVE_ENCODING,
        )

        policies = self.load_json("DEV/CATALOG/identifier-policies.json")
        schema = self.load_json("DEV/SCHEMAS/identifier-policies.schema.json")
        Draft202012Validator(schema).validate(policies)

        self.assertEqual(policies["catalog_generation"], CATALOG_GENERATION)
        self.assertEqual(policies["schema_version"], 3)
        self.assertEqual(schema["properties"]["schema_version"]["const"], 3)
        all_policies = {**policies["world"], **policies["runtime"]}
        self.assertEqual(set(all_policies), set(LIVE_BIRTH_ADMISSION_TABLE))
        self.assertEqual(
            set(all_policies), WORLD_RECORD_FAMILIES | RUNTIME_RECORD_FAMILIES
        )
        self.assertEqual(len(all_policies), 34)
        for family, policy in all_policies.items():
            with self.subTest(family=family):
                self.assertEqual(
                    policy["live_birth"], LIVE_BIRTH_ADMISSION_TABLE[family]
                )
        self.assertEqual(SOURCE_NATIVE_LIVE_ENCODING, "framed_base32hex_v1")

    def test_shared_entity_structure_joins_owner_binding_inputs_once(self):
        structures = self.load_json("DEV/CATALOG/entity-structures.json")
        shared_world = structures["world_records"]
        self.assertEqual(set(shared_world), WORLD_RECORD_FAMILIES)
        self.assertEqual(
            shared_world["world.thread"]["definition_binding"], {"mode": "forbidden"}
        )
        self.assertEqual(
            shared_world["world.player"]["definition_binding"], {"mode": "forbidden"}
        )
        for family, spec in shared_world.items():
            with self.subTest(family=family):
                self.assertIn(
                    spec["definition_binding"]["mode"],
                    {"forbidden", "optional", "required"},
                )
                if spec["definition_binding"]["mode"] == "forbidden":
                    self.assertEqual(spec["definition_binding"], {"mode": "forbidden"})

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
                "live_birth": "OWNER_EQUIVALENT",
            },
        )
        self.assertEqual(
            policies["runtime"]["runtime.disclosure"],
            {
                "strategy": "composite_key",
                "fields": ["player_id", "fact_id"],
                "scope": "campaign",
                "live_birth": "OWNER_EQUIVALENT",
            },
        )
        self.assertIn("runtime.collaboration_obligation", policies["runtime"])


if __name__ == "__main__":
    unittest.main()
