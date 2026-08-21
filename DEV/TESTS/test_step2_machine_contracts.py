import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class Step2MachineContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.surfaces = load_json(CATALOG / "mechanical-surfaces.json")
        cls.surface_schema = load_json(SCHEMAS / "mechanical-surfaces.schema.json")
        cls.entity_structures = load_json(CATALOG / "entity-structures.json")

    def test_mechanical_surfaces_validate_against_schema(self):
        Draft202012Validator.check_schema(self.surface_schema)
        Draft202012Validator(self.surface_schema).validate(self.surfaces)

    def test_accessor_registry_matches_structured_metadata(self):
        registry = set(self.core["registries"]["mechanical_accessors"])
        metadata = set(self.surfaces["accessors"])
        self.assertEqual(registry, metadata)

    def test_surface_selectors_and_operations_are_registered(self):
        selectors = set(self.core["registries"]["rule_selectors"])
        operations = set(self.core["registries"]["rule_operations"])
        for selector_id, metadata in self.surfaces["selectors"].items():
            self.assertIn(selector_id, selectors)
            self.assertLessEqual(set(metadata["allowed_operations"]), operations)

    def test_removed_step2_authorities_are_not_registered(self):
        registries = self.core["registries"]
        self.assertNotIn("resource.health", registries["resource_mechanics"])
        self.assertNotIn("resource.temporary_health", registries["resource_mechanics"])
        self.assertNotIn("effect.stacks", registries["rule_selectors"])
        self.assertNotIn("duration.concentration", registries["duration_modes"])
        self.assertNotIn("recovery_triggers", registries)
        self.assertNotIn("stacking_behaviors", registries)

    def test_condition_axes_are_independent_closed_registries(self):
        registries = self.core["registries"]
        self.assertEqual(
            set(registries["condition_aggregation_policies"]),
            {"condition_aggregation.presence", "condition_aggregation.cumulative_units"},
        )
        self.assertEqual(
            set(registries["condition_rule_scopes"]),
            {
                "condition_rule_scope.aggregate_once",
                "condition_rule_scope.per_effective_application",
            },
        )

    def test_world_effect_inventory_has_one_target_and_no_stack_authority(self):
        effect = self.entity_structures["world_records"]["world.effect"]
        self.assertEqual(effect["required"], ["target_id", "lifecycle"])
        self.assertEqual(effect["definition_binding"]["mode"], "required")
        self.assertEqual(
            set(effect["definition_binding"]["allowed_definition_kinds"]),
            {"definition.effect", "definition.condition"},
        )
        fields = set(effect["required"]) | set(effect["expected"])
        self.assertNotIn("target_ids", fields)
        self.assertNotIn("stacks", fields)
        self.assertNotIn("status", fields)
        self.assertIn("support_effect_id", fields)
        self.assertIn("temporal_binding", fields)

    def test_condition_definition_has_direct_aggregation_authority(self):
        condition = self.entity_structures["definitions"]["definition.condition"]
        self.assertEqual(condition["required"], ["aggregation_policy_id"])
        fields = set(condition["required"]) | set(condition["expected"])
        self.assertNotIn("effect_ids", fields)
        self.assertIn("intrinsic_mechanics", fields)

    def test_rest_policy_does_not_own_recovery_steps(self):
        rest = self.entity_structures["definitions"]["definition.rest_policy"]
        fields = set(rest["required"]) | set(rest["expected"])
        self.assertNotIn("recovery_steps", fields)
        self.assertIn("completion_boundary_id", fields)


if __name__ == "__main__":
    unittest.main()
