from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "GAME" / "CORE"


class HourlyDurabilityContractTests(unittest.TestCase):
    def test_dirty_hot_or_soft_state_forces_boundary_at_one_hour(self):
        src = (CORE / "DURABILITY_GUARD.md").read_text(encoding="utf-8")
        self.assertIn("one-hour dirty durability ceiling", src.lower())
        self.assertIn("dirty_hot_or_soft", src)
        self.assertIn("now - durable_frontier_time >= 1 hour", src)
        self.assertIn("forced durability boundary", src.lower())
        self.assertIn("additive", src.lower())

    def test_clean_state_never_creates_hourly_heartbeat_commit(self):
        src = (CORE / "DURABILITY_GUARD.md").read_text(encoding="utf-8")
        self.assertIn("no heartbeat commits", src.lower())
        self.assertIn("no dirty canonical/current state", src.lower())
        self.assertIn("MUST NOT create an empty/no-op commit", src)

    def test_inactive_chat_rechecks_on_next_interaction_not_in_background(self):
        src = (CORE / "SESSION.md").read_text(encoding="utf-8")
        self.assertIn("after a long inactive gap", src.lower())
        self.assertIn("next user interaction", src.lower())
        self.assertIn("before applying a new gameplay action", src.lower())
        self.assertIn("does not run in the background", src.lower())

    def test_lost_ephemeral_dirty_state_is_not_reinvented(self):
        src = (CORE / "RUNTIME.md").read_text(encoding="utf-8")
        self.assertIn("lost ephemeral dirty state", src.lower())
        self.assertIn("recover only from the latest durable campaign frontier", src.lower())
        self.assertIn("must not invent unpublished canon", src.lower())

    def test_persistence_transport_does_not_create_separate_hourly_policy(self):
        src = (CORE / "PERSISTENCE.md").read_text(encoding="utf-8")
        self.assertIn("one-hour boundary", src.lower())
        self.assertIn("DURABILITY_GUARD.md", src)
        self.assertIn("does not create or reinterpret", src.lower())


if __name__ == "__main__":
    unittest.main()
