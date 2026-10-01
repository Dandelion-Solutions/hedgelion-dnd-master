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

    def test_current_state_v3_retires_frontier_and_defers_old_scaffold(self):
        schema = self.read("GAME/SCHEMA/current_state.schema.yaml")
        template = self.read("GAME/CAMPAIGN/STATE/CURRENT.yaml")
        cursor = self.read(
            "DEV/docs/superpowers/plans/implementation-wave-05-machine-bootstrap-integration-execution-status.md"
        )

        self.assertIn("schema_version: 3", schema)
        self.assertNotIn("frontier:", schema)
        self.assertNotIn("player_character_ids", schema)
        self.assertNotIn("path:", schema)

        # CURRENT remains the old blank scaffold until W05.T05; it is not a
        # valid current_state-v3 instance during that interval.
        self.assertIn("schema_version: 2", template)
        self.assertIn("frontier:", template)
        self.assertIn(
            "CURRENT_SCAFFOLD_ALIGNMENT: DEFERRED_TO_W05_T05", cursor
        )
        self.assertIn("CURRENT.yaml -> schema_version 3", cursor)
        self.assertIn("remove world_time.frontier", cursor)

    def test_campaign_allocator_remains_distinct_identity_owner(self):
        policies = self.read("DEV/CATALOG/identifier-policies.json")
        self.assertIn('"id": "campaign-allocator"', policies)
        self.assertIn('"runtime.id_allocator"', policies)
        contracts = self.read("DEV/ARCHITECTURE/CATALOG_CONTRACTS.md")
        self.assertIn("not silently reused", contracts.lower())


if __name__ == "__main__":
    unittest.main()
