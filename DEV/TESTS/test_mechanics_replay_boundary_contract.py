from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "GAME" / "CORE"
TESTS = ROOT / "DEV" / "TESTS"


class MechanicsReplayBoundaryContractTests(unittest.TestCase):
    def test_missing_trace_alone_does_not_authorize_replay(self):
        src = (CORE / "MECHANICS_INTEGRITY.md").read_text(encoding="utf-8")
        self.assertIn("trace **alone does not prove that accepted mechanics never existed**", src)
        self.assertIn("does not invalidate an already accepted mechanical consequence", src)
        self.assertNotIn(
            "If the runtime discovers that an uncertain narrated outcome was produced without a valid resolution trace",
            src,
        )

    def test_accepted_mechanics_rng_ids_and_consequences_survive_downstream_failure(self):
        src = (CORE / "MECHANICS_INTEGRITY.md").read_text(encoding="utf-8")
        for token in (
            "accepted mechanics/RNG/stable IDs/consequences",
            "do NOT replay or re-resolve the accepted action",
            "do NOT reroll or replace accepted RNG",
            "do NOT reallocate or replace accepted stable IDs",
            "do NOT rewrite accepted consequences",
        ):
            self.assertIn(token, src)

    def test_fresh_rng_is_limited_to_genuinely_unsupported_preacceptance_correction(self):
        src = (CORE / "MECHANICS_INTEGRITY.md").read_text(encoding="utf-8")
        self.assertIn("genuinely mechanically unsupported", src)
        self.assertIn("no valid accepted mechanics/RNG consequence ever existed", src)
        self.assertIn("fresh legitimate RNG", src)
        self.assertIn("repair/persist only canon that was based on genuinely unsupported mechanics", src)

    def test_regression_cases_cover_trace_loss_after_accepted_resolution(self):
        src = (TESTS / "MECHANICS_INTEGRITY_CASES.md").read_text(encoding="utf-8")
        self.assertIn("accepted mechanics/RNG consequence already exists", src)
        self.assertIn("missing/corrupt/unavailable downstream trace alone", src)
        self.assertIn("NO replay / reroll / reallocation", src)


if __name__ == "__main__":
    unittest.main()
