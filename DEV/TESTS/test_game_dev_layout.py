from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class GameDevLayoutTests(unittest.TestCase):
    def test_old_root_ownership_paths_are_absent(self):
        forbidden = {
            "CORE", "RULES", "SCHEMA", "CAMPAIGN", "TEMPLATE", "MIGRATIONS", "INSTALL",
            "TOOLS", "ARCHITECTURE", "TESTS", "RELEASE", "CATALOG", "SCHEMAS", "docs",
            "ENGINE_VERSION.yaml",
        }
        self.assertEqual([name for name in sorted(forbidden) if (ROOT / name).exists()], [])

    def test_runtime_marker_is_unique(self):
        self.assertEqual(list(ROOT.rglob("ENGINE_VERSION.yaml")), [ROOT / "GAME/ENGINE_VERSION.yaml"])

    def test_superpowers_paths_are_dev_only(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("DEV/docs/superpowers/specs/", agents)
        self.assertIn("DEV/docs/superpowers/plans/", agents)
        self.assertFalse((ROOT / "docs").exists())

    def test_deprecated_manifest_stub_is_absent(self):
        self.assertFalse((ROOT / "GAME/TEMPLATE/CAMPAIGN_MANIFEST.yaml").exists())


if __name__ == "__main__":
    unittest.main()
