import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
ARCH = ROOT / "DEV" / "ARCHITECTURE"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class Step4StoryRetirementContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.structures = load_json(CATALOG / "entity-structures.json")
        cls.identifiers = load_json(CATALOG / "identifier-policies.json")
        cls.surfaces = load_json(CATALOG / "mechanical-surfaces.json")
        cls.inventory = (ARCH / "CATALOG_INVENTORY.md").read_text(encoding="utf-8")
        cls.contracts = (ARCH / "CATALOG_CONTRACTS.md").read_text(encoding="utf-8")
        cls.entity_doc = (ARCH / "ENTITY_STRUCTURES.md").read_text(encoding="utf-8")

    def test_catalog_generation_preserves_step4_closed_vocabulary_baseline(self):
        generations = {
            self.core["catalog_generation"],
            self.structures["catalog_generation"],
            self.identifiers["catalog_generation"],
            self.surfaces["catalog_generation"],
        }
        self.assertEqual(generations, {2})

    def test_world_record_machine_surfaces_remain_coherent(self):
        registered = set(self.core["registries"]["world_record_kinds"])
        self.assertEqual(registered, set(self.structures["world_records"]))
        self.assertEqual(registered, set(self.identifiers["world"]))

    def test_world_chapter_is_not_a_world_record(self):
        self.assertNotIn(
            "world.chapter",
            self.core["registries"]["world_record_kinds"],
        )
        self.assertNotIn("world.chapter", self.structures["world_records"])
        self.assertNotIn("world.chapter", self.identifiers["world"])

    def test_chapter_append_transition_and_event_are_retired(self):
        registries = self.core["registries"]
        self.assertNotIn("transition.chapter_append", registries["transition_kinds"])
        self.assertNotIn("event.chapter.appended", registries["event_kinds"])

    def test_current_normative_docs_have_no_world_chapter_authority(self):
        for text in (self.inventory, self.contracts, self.entity_doc):
            self.assertNotIn("world.chapter", text)
        self.assertIn("Story", self.inventory)
        self.assertIn("narrative", self.inventory.lower())
        self.assertIn("index", self.inventory.lower())


if __name__ == "__main__":
    unittest.main()
