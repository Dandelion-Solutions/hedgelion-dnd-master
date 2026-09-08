from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "GAME" / "CORE"
DEV = ROOT / "DEV"


class DurabilityRiskContractTests(unittest.TestCase):
    RETIRED_EXACT_TIMER_TOKENS = (
        "one-hour",
        "one hour",
        "hourly",
        "durable_frontier_time",
        ">= 1 hour",
        "one-hour ceiling",
        "hourly ceiling",
    )

    ACTIVE_SURFACES = (
        CORE / "DURABILITY_GUARD.md",
        CORE / "SESSION.md",
        CORE / "STORAGE.md",
        CORE / "RUNTIME.md",
        CORE / "PERSISTENCE.md",
        CORE / "CAMPAIGN_SETUP.md",
        DEV / "RELEASE" / "CHECKLIST.md",
    )

    def test_retired_exact_timer_is_absent_from_active_surfaces(self):
        leaks: list[str] = []
        for path in self.ACTIVE_SURFACES:
            src = path.read_text(encoding="utf-8").lower()
            for token in self.RETIRED_EXACT_TIMER_TOKENS:
                if token in src:
                    leaks.append(f"{path.relative_to(ROOT).as_posix()}: {token}")
        self.assertEqual(leaks, [], "retired exact durability timer leaked into active runtime/release contracts")

    def test_guard_owns_normal_elevated_danger_as_loss_protection_not_hard(self):
        src = (CORE / "DURABILITY_GUARD.md").read_text(encoding="utf-8")
        self.assertIn("NORMAL\nELEVATED\nDANGER", src)
        self.assertIn("operability/loss-protection trajectory", src)
        self.assertIn("one owner-valid bounded preservation/recovery attempt", src)
        self.assertIn("DANGER alone MUST NOT", src)
        self.assertIn("create `MUST_BE_DURABLE_BEFORE(edge)` as a correctness law", src)
        self.assertIn("automatic retry", src)
        self.assertIn("background scheduler/worker/heartbeat/polling loop", src)

    def test_clean_state_never_creates_heartbeat_or_noop_persistence(self):
        src = (CORE / "DURABILITY_GUARD.md").read_text(encoding="utf-8")
        self.assertIn("### No heartbeat commits", src)
        self.assertIn("no dirty canonical/current state", src.lower())
        self.assertIn("MUST NOT create an empty/no-op commit", src)

    def test_advisory_host_pressure_alone_cannot_create_gameplay_danger(self):
        guard = (CORE / "DURABILITY_GUARD.md").read_text(encoding="utf-8")
        runtime = (CORE / "RUNTIME.md").read_text(encoding="utf-8")
        session = (CORE / "SESSION.md").read_text(encoding="utf-8")
        for src in (guard, runtime, session):
            self.assertIn("alone", src.lower())
            self.assertIn("gameplay-affecting DANGER", src)
        self.assertIn("owner-valid still-relevant unpublished-state/loss-exposure evidence", guard)

    def test_persistence_transports_danger_attempt_without_creating_policy_or_retry(self):
        src = (CORE / "PERSISTENCE.md").read_text(encoding="utf-8")
        self.assertIn("one bounded preservation/recovery attempt", src)
        self.assertIn("does not promote DANGER to correctness HARD", src)
        self.assertIn("does not", src.lower())
        self.assertIn("automatically retry", src)

    def test_storage_no_longer_requires_timer_only_frontier_state(self):
        src = (CORE / "STORAGE.md").read_text(encoding="utf-8")
        self.assertIn("without a synthetic global durability timer/frontier", src)
        self.assertIn("NORMAL / ELEVATED / DANGER", src)

    def test_release_checklist_tracks_current_durability_contract(self):
        src = (DEV / "RELEASE" / "CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("NORMAL / ELEVATED / DANGER", src)
        self.assertIn("one owner-valid bounded preservation/recovery attempt", src)
        self.assertIn("does not create correctness HARD", src)
        self.assertIn("Clean state never creates", src)


if __name__ == "__main__":
    unittest.main()
