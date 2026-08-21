import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProjectMapRetrospectiveHotfixTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_retired_secret_index_is_absent_from_new_campaign_template(self):
        self.assertFalse((ROOT / "GAME/CAMPAIGN/INDEX/SECRET_INDEX.yaml").exists())

    def test_checkpoint_docs_distinguish_pointer_descriptor_and_recovery_boundary(self):
        session = self.read("GAME/CORE/SESSION.md")
        storage = self.read("GAME/CORE/STORAGE.md")
        maintenance = self.read("DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md")

        self.assertNotIn("Checkpoints are sparse recovery frontiers", session)
        self.assertNotIn("Checkpoints are recovery frontiers", storage)
        self.assertNotIn("latest-checkpoint pointer/frontier", maintenance)
        self.assertIn("MANIFEST.last_checkpoint_id", maintenance)
        self.assertIn("recovery descriptor", maintenance)

    def test_maintenance_commands_use_current_connector_transport_contract(self):
        maintenance = self.read("DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md")
        lowered = maintenance.lower()

        self.assertNotIn("native_git", maintenance)
        self.assertNotIn("connector_fallback", maintenance)
        self.assertNotIn("probe native git", lowered)
        self.assertIn("Connector", maintenance)
        self.assertIn("PERSISTENCE.md", maintenance)

    def test_maintenance_contract_does_not_revive_retired_chapter_authority(self):
        maintenance = self.read("DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md")
        self.assertNotIn("chapter entry", maintenance.lower())

    def test_maintenance_turn_counter_wording_does_not_claim_all_runtime_state(self):
        maintenance = self.read("DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md")
        self.assertNotIn("Runtime state stores one counter only", maintenance)
        self.assertIn("turn-number bookkeeping", maintenance)


if __name__ == "__main__":
    unittest.main()
