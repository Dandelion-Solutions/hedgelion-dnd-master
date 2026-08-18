from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "GAME" / "CORE"


class MaintenanceContinuationContractTests(unittest.TestCase):
    def test_session_captures_ephemeral_maintenance_continuation_frame(self):
        src = (CORE / "SESSION.md").read_text(encoding="utf-8")
        self.assertIn("maintenance continuation frame", src.lower())
        self.assertIn("last meaningful player action", src.lower())
        self.assertIn("last meaningful Master/NPC", src)
        self.assertIn("unresolved decision point", src.lower())
        self.assertIn("current-chat working state", src.lower())
        self.assertIn("not automatically campaign canon", src.lower())

    def test_successful_maintenance_returns_to_same_gameplay_point(self):
        src = (CORE / "ENGINE_UPDATES.md").read_text(encoding="utf-8")
        self.assertIn("transparent pause", src.lower())
        self.assertIn("return to the same unresolved gameplay point", src.lower())
        self.assertIn("must not end the player-facing response with only", src.lower())
        self.assertIn("who last said/did what", src.lower())

    def test_resume_uses_exact_dialogue_only_when_evidence_supports_it(self):
        src = (CORE / "SESSION.md").read_text(encoding="utf-8")
        self.assertIn("exact previous utterance", src.lower())
        self.assertIn("current chat context", src.lower())
        self.assertIn("durable semantic summary", src.lower())
        self.assertIn("never fabricate an exact quote", src.lower())

    def test_runtime_switch_does_not_advance_fictional_time(self):
        src = (CORE / "RUNTIME.md").read_text(encoding="utf-8")
        self.assertIn("maintenance itself does not advance fictional time", src.lower())
        self.assertIn("continuation frame", src.lower())


if __name__ == "__main__":
    unittest.main()
