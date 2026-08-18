from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "GAME"
DEV = ROOT / "DEV"


class MultiRuntimeReleaseConsistencyTests(unittest.TestCase):
    def test_generated_provenance_is_artifact_only_not_tracked_game_source(self):
        checklist = (DEV / "RELEASE" / "CHECKLIST.md").read_text(encoding="utf-8")
        self.assertFalse((GAME / "RUNTIME_PACKAGE.yaml").exists())
        self.assertIn("generated `RUNTIME_PACKAGE.yaml`", checklist)
        self.assertIn("in-memory ZIP entry", checklist)
        self.assertIn("all valid files under `GAME/` plus exactly one", checklist)

    def test_release_checklist_covers_multi_runtime_and_portable_identity(self):
        checklist = (DEV / "RELEASE" / "CHECKLIST.md").read_text(encoding="utf-8")
        for token in (
            "multiple runtime ZIPs",
            "current_runtime_root",
            "DND_STORAGE.engine.baseline",
            "MANIFEST.engine.current",
            "same-version",
            "campaign creator",
            "one-hour",
            "heartbeat",
            "continuation frame",
        ):
            self.assertIn(token, checklist)

    def test_new_campaign_template_and_storage_schema_are_both_v3(self):
        manifest = yaml.safe_load((GAME / "CAMPAIGN" / "MANIFEST.yaml").read_text(encoding="utf-8"))
        storage_schema = yaml.safe_load((GAME / "SCHEMA" / "dnd_storage.schema.yaml").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 3)
        self.assertEqual(storage_schema["schema_version"], 3)
        self.assertIn("current", manifest["engine"])
        self.assertIn("baseline", storage_schema["fields"]["engine"])

    def test_root_readme_is_not_part_of_automatic_multi_runtime_implementation(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Root README editorial contract", agents)
        self.assertIn("explicitly asks for, or explicitly approves", agents)


if __name__ == "__main__":
    unittest.main()
