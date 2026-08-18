from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPDATES = ROOT / "GAME" / "CORE" / "ENGINE_UPDATES.md"
BOOT = ROOT / "GAME" / "INSTALL" / "00_DND_BOOTSTRAP.md"


class EngineMismatchRecoveryContractTests(unittest.TestCase):
    def test_available_current_version_package_is_used_without_player_cache_prompt(self):
        src = UPDATES.read_text(encoding="utf-8")
        self.assertIn("Required current-version package is available", src)
        self.assertIn("reuse or silently re-extract", src.lower())
        self.assertIn("no player prompt", src.lower())

    def test_non_creator_missing_current_version_package_is_told_to_add_matching_zip_only(self):
        src = UPDATES.read_text(encoding="utf-8")
        self.assertIn("Required current-version package is absent; user is not campaign creator", src)
        self.assertIn("add the matching `hedgelion-dnd-master-runtime-v<version>.zip`", src.lower())
        self.assertIn("MUST NOT offer semantic-version migration", src)

    def test_creator_missing_old_package_gets_restore_or_update_choices(self):
        src = UPDATES.read_text(encoding="utf-8")
        self.assertIn("Required current-version package is absent; user is campaign creator", src)
        self.assertIn("Restore/add the campaign's current runtime version", src)
        self.assertIn("Update the campaign to an available newer semantic version", src)
        self.assertIn("preferred when one Project intentionally contains campaigns on different engine versions", src)

    def test_bootstrap_forbids_bare_terminal_refusal_when_recovery_exists(self):
        src = BOOT.read_text(encoding="utf-8")
        self.assertIn("MUST NOT end at a bare", src)
        self.assertIn("valid restore/update path", src)


if __name__ == "__main__":
    unittest.main()
