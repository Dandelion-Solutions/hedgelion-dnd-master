import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
INVENTORY = ROOT / "DEV" / "ARCHITECTURE" / "CATALOG_INVENTORY.md"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class Step4StoryRetirementContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.structures = load_json(CATALOG / "entity-structures.json")
        cls.identifiers = load_json(CATALOG / "identifier-policies.json")
        cls.inventory = INVENTORY.read_text(encoding="utf-8")

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

    def test_normative_inventory_does_not_classify_chapter_as_world_authority(self):
        self.assertNotIn("| `world.chapter` |", self.inventory)
        self.assertIn("STORY/NARRATIVE", self.inventory)
        self.assertIn("chapter", self.inventory.lower())
        self.assertIn("index", self.inventory.lower())


if __name__ == "__main__":
    unittest.main()
