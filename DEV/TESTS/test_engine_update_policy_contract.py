from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "GAME" / "CORE" / "ENGINE_UPDATES.md"


class EngineUpdatePolicyContractTests(unittest.TestCase):
    def test_semantic_version_prompt_is_creator_controlled_and_ephemeral(self):
        src = POLICY.read_text(encoding="utf-8")
        self.assertIn("campaign creator", src.lower())
        self.assertIn("Update now", src)
        self.assertIn("Remind later", src)
        self.assertIn("Do not remind about this version", src)
        self.assertIn("24 hours", src)
        self.assertIn("(campaign_identity, target_engine_version)", src)
        self.assertIn("ephemeral", src.lower())
        self.assertIn("MUST NOT be written to campaign Git", src)
        self.assertIn("storage owner", src.lower())

    def test_same_version_descendant_refresh_is_silent_and_does_not_force_manifest_commit(self):
        src = POLICY.read_text(encoding="utf-8")
        self.assertIn("same-version", src.lower())
        self.assertIn("one bounded server-side compare", src)
        self.assertIn("RUNTIME_PACKAGE.source_commit_sha", src)
        self.assertIn("silently prefer", src.lower())
        self.assertIn("ancestor", src.lower())
        self.assertIn("downgrade", src.lower())
        self.assertIn("diverged", src.lower())
        self.assertIn("MUST NOT create a standalone", src)
        self.assertIn("non-creator", src.lower())

    def test_storage_baseline_and_campaign_engine_authority_are_independent(self):
        src = POLICY.read_text(encoding="utf-8")
        self.assertIn("DND_STORAGE.engine.baseline", src)
        self.assertIn("MANIFEST.engine.current", src)
        self.assertIn("independent", src.lower())
        self.assertNotIn("Only authenticated storage owner may change storage baseline metadata or perform normal campaign engine maintenance", src)


if __name__ == "__main__":
    unittest.main()
