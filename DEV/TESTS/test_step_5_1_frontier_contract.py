import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Step51FrontierContractTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_current_state_does_not_persist_global_last_event_cursor(self):
        schema = self.read("GAME/SCHEMA/current_state.schema.yaml")
        template = self.read("GAME/CAMPAIGN/STATE/CURRENT.yaml")
        self.assertNotIn("last_event_id", schema)
        self.assertNotIn("last_event_id", template)

    def test_current_state_keeps_chronology_frontier_for_step_5_9(self):
        schema = self.read("GAME/SCHEMA/current_state.schema.yaml")
        template = self.read("GAME/CAMPAIGN/STATE/CURRENT.yaml")
        self.assertIn("world_time:", schema)
        self.assertIn("frontier:", schema)
        self.assertIn("world_time:", template)
        self.assertIn("frontier:", template)

    def test_campaign_allocator_remains_distinct_identity_owner(self):
        contracts = self.read("DEV/ARCHITECTURE/CATALOG_CONTRACTS.md")
        self.assertIn("campaign-allocator", contracts)
        self.assertIn("last_allocated", contracts)
        self.assertIn("Concurrent writers allocate against their pinned frontier", contracts)
        self.assertIn("Published IDs are never changed or reused", contracts)


if __name__ == "__main__":
    unittest.main()
