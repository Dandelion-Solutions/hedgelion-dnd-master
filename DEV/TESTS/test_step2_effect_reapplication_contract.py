import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_registry():
    registry = Registry()
    schemas = {}
    for path in SCHEMAS.glob("*.schema.json"):
        schema = load_json(path)
        schemas[path.name] = schema
        schema_id = schema.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry, schemas


class Step2EffectReapplicationContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()
        cls.core = load_json(CATALOG / "core-catalog.json")

    def test_reapplication_separates_matching_from_action(self):
        registries = self.core["registries"]
        self.assertEqual(
            set(registries["effect_reapplication_match_policies"]),
            {
                "effect_reapplication_match.target_family",
                "effect_reapplication_match.target_family_source",
            },
        )
        self.assertEqual(
            set(registries["effect_reapplication_actions"]),
            {"effect_reapplication.refresh", "effect_reapplication.replace"},
        )
        self.assertNotIn("effect_reapplication_policies", registries)

    def test_effect_definition_accepts_typed_match_and_action(self):
        validator = Draft202012Validator(
            self.schemas["catalog-definition.schema.json"],
            registry=self.registry,
        )
        validator.validate({
            "id": "effect.example_refresh",
            "kind": "definition.effect",
            "name": {"en": "Example Refresh"},
            "data": {
                "reapplication": {
                    "match_policy_id": "effect_reapplication_match.target_family_source",
                    "action_id": "effect_reapplication.refresh",
                }
            },
        })

    def test_old_single_reapplication_policy_field_is_rejected(self):
        validator = Draft202012Validator(
            self.schemas["catalog-definition.schema.json"],
            registry=self.registry,
        )
        with self.assertRaises(ValidationError):
            validator.validate({
                "id": "effect.old_shape",
                "kind": "definition.effect",
                "name": {"en": "Old Shape"},
                "data": {"reapplication_policy_id": "effect_reapplication.refresh"},
            })


if __name__ == "__main__":
    unittest.main()
