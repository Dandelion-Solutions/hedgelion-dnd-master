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


class CatalogDefinitionBindingContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.structures = load_json(CATALOG / "entity-structures.json")
        cls.schema = load_json(SCHEMAS / "entity-structures.schema.json")

    def test_entity_structures_schema_accepts_current_machine_catalog(self):
        Draft202012Validator(self.schema).validate(self.structures)

    def test_every_world_kind_declares_definition_binding_mode(self):
        for kind, spec in self.structures["world_records"].items():
            with self.subTest(kind=kind):
                self.assertIn("definition_binding", spec)
                self.assertIn(spec["definition_binding"]["mode"], {"forbidden", "optional", "required"})

    def test_allowed_definition_kinds_are_registered(self):
        registered = set(self.core["registries"]["content_definition_kinds"])
        for world_kind, spec in self.structures["world_records"].items():
            binding = spec["definition_binding"]
            allowed = set(binding.get("allowed_definition_kinds", []))
            with self.subTest(world_kind=world_kind):
                if binding["mode"] == "forbidden":
                    self.assertEqual(allowed, set())
                else:
                    self.assertTrue(allowed)
                    self.assertTrue(allowed <= registered)

    def test_core_world_definition_compatibilities_are_explicit(self):
        expected = {
            "world.actor": ("optional", {"definition.actor_archetype"}),
            "world.asset": ("optional", {"definition.asset"}),
            "world.location": ("optional", {"definition.location_archetype"}),
            "world.organization": ("optional", {"definition.organization_archetype"}),
            "world.contract": ("optional", {"definition.contract_template"}),
            "world.mission": ("optional", {"definition.mission_template"}),
            "world.hazard": ("optional", {"definition.hazard"}),
            "world.effect": ("required", {"definition.effect", "definition.condition"}),
        }
        for world_kind, (mode, allowed) in expected.items():
            binding = self.structures["world_records"][world_kind]["definition_binding"]
            with self.subTest(world_kind=world_kind):
                self.assertEqual(binding["mode"], mode)
                self.assertEqual(set(binding["allowed_definition_kinds"]), allowed)

    def test_world_kinds_without_reusable_identity_forbid_definition_id(self):
        allowed_kinds = {
            "world.actor", "world.asset", "world.location", "world.organization",
            "world.contract", "world.mission", "world.hazard", "world.effect",
        }
        for world_kind, spec in self.structures["world_records"].items():
            if world_kind in allowed_kinds:
                continue
            with self.subTest(world_kind=world_kind):
                self.assertEqual(spec["definition_binding"], {"mode": "forbidden"})


if __name__ == "__main__":
    unittest.main()
