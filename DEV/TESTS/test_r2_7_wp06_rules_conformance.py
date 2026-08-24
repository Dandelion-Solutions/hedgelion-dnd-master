import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class R27WP06RulesConformanceTests(unittest.TestCase):
    def registry(self):
        result = Registry()
        for path in SCHEMAS.glob("*.json"):
            data = load(path)
            if "$id" in data:
                result = result.with_resource(data["$id"], Resource.from_contents(data))
        return result

    def test_every_registered_rule_selector_has_structured_metadata(self):
        core = load(CATALOG / "core-catalog.json")
        surfaces = load(CATALOG / "mechanical-surfaces.json")
        self.assertEqual(
            set(core["registries"]["rule_selectors"]),
            set(surfaces["selectors"]),
        )

    def test_mechanical_surfaces_validate_after_full_selector_closure(self):
        schema = load(SCHEMAS / "mechanical-surfaces.schema.json")
        data = load(CATALOG / "mechanical-surfaces.json")
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(data)

    def test_character_build_definitions_have_strict_data_schemas(self):
        catalog_schema = load(SCHEMAS / "catalog-definition.schema.json")
        serialized = json.dumps(catalog_schema)
        expected = {
            "definition.species": "species-definition-data.schema.json",
            "definition.background": "background-definition-data.schema.json",
            "definition.class": "class-definition-data.schema.json",
            "definition.subclass": "subclass-definition-data.schema.json",
            "definition.advancement": "advancement-definition-data.schema.json",
            "definition.feat": "feat-definition-data.schema.json",
            "definition.feature": "feature-definition-data.schema.json",
            "definition.spell": "spell-definition-data.schema.json",
        }
        for kind, filename in expected.items():
            self.assertIn(kind, serialized)
            self.assertIn(filename, serialized)
            self.assertTrue((SCHEMAS / filename).is_file(), filename)

    def test_build_choice_slots_are_stable_and_actor_bindings_reference_option_ids(self):
        self.assertTrue((SCHEMAS / "build-choice-slot.schema.json").is_file())
        actor = load(SCHEMAS / "world-actor-state.schema.json")
        binding = actor["$defs"]["choiceBinding"]
        self.assertEqual(binding["required"], ["selected_option_ids"])
        selected = binding["properties"]["selected_option_ids"]
        self.assertTrue(selected["uniqueItems"])
        self.assertEqual(
            actor["$defs"]["choiceBindings"]["additionalProperties"]["$ref"],
            "#/$defs/choiceBinding",
        )

    def test_advancement_levels_own_stable_choice_slots(self):
        advancement = load(SCHEMAS / "advancement-definition-data.schema.json")
        self.assertIn("levels", advancement["required"])
        level = advancement["$defs"]["levelEntry"]
        self.assertIn("level", level["required"])
        self.assertEqual(
            level["properties"]["choice_slots"]["items"]["$ref"],
            "https://hedgelion.invalid/schemas/build-choice-slot.schema.json",
        )

    def test_activity_uses_typed_parameter_target_and_cost_contracts(self):
        activity = load(SCHEMAS / "activity-definition-data.schema.json")
        props = activity["properties"]
        self.assertEqual(
            props["parameters"]["additionalProperties"]["$ref"],
            "https://hedgelion.invalid/schemas/activity-parameter-spec.schema.json",
        )
        self.assertEqual(
            props["targeting"]["$ref"],
            "https://hedgelion.invalid/schemas/target-spec.schema.json",
        )
        self.assertEqual(
            props["costs"]["items"]["$ref"],
            "https://hedgelion.invalid/schemas/cost-spec.schema.json",
        )

    def test_adjudicated_activity_parameters_are_explicit_and_not_engine_state_aliases(self):
        parameter = load(SCHEMAS / "activity-parameter-spec.schema.json")
        source_classes = set(parameter["properties"]["source_class"]["enum"])
        self.assertIn("INVOCATION_ADJUDICATED", source_classes)
        self.assertIn("PLAYER_CHOICE", source_classes)
        self.assertIn("ENGINE_BOUND", source_classes)
        self.assertNotIn("DIRECT_AUTHORITY", source_classes)

    def test_target_area_cost_roll_values_have_embedded_schemas(self):
        for name in (
            "target-spec.schema.json",
            "area-spec.schema.json",
            "cost-spec.schema.json",
            "roll-request.schema.json",
        ):
            self.assertTrue((SCHEMAS / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
