import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = REPO_ROOT / "DEV" / "CATALOG" / "catalog-admission-ledger.json"
PLANNING_CLASSES_PATH = REPO_ROOT / "DEV" / "CATALOG" / "planning-entry-classes.json"

OWNER_CHAIN = (
    "DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md + "
    "DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md"
)
PLANNING_IDS = [
    "planning.source_anchored_constraint",
    "planning.provisional_dramaturgic_direction",
]


class WP18FinalSeniorRecoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.planning_classes = json.loads(PLANNING_CLASSES_PATH.read_text(encoding="utf-8"))

    def test_planning_entry_class_vocabulary_is_unchanged(self):
        self.assertEqual(self.planning_classes["values"], PLANNING_IDS)

    def test_planning_entry_family_uses_current_owner_chain(self):
        policy = self.ledger["family_policies"]["planning_entry_classes"]
        self.assertEqual(policy["semantic_owner"], OWNER_CHAIN)
        self.assertEqual(policy["default_downstream_owner"], OWNER_CHAIN)

    def test_planning_entries_use_current_owner_chain(self):
        entries = {
            entry["id"]: entry
            for entry in self.ledger["entries"]
            if entry.get("registry_family") == "planning_entry_classes"
        }
        self.assertEqual(list(entries), PLANNING_IDS)

        for planning_id in PLANNING_IDS:
            entry = entries[planning_id]
            self.assertEqual(entry["semantic_owner"], OWNER_CHAIN)
            self.assertEqual(entry["downstream_owner"], OWNER_CHAIN)
            self.assertEqual(
                entry["evidence_citation"],
                f"{OWNER_CHAIN}; exact closed enum member: {planning_id}",
            )


if __name__ == "__main__":
    unittest.main()
