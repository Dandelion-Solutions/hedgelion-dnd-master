from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ASSET_NAME = "hedgelion-dnd-master-runtime-v0.8.zip"


class ReleaseIntegrationTests(unittest.TestCase):
    def test_canonical_entry_point_builds_reproducible_flat_runtime_and_generator_smoke(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hdm-release-integration-") as td:
            temp_root = Path(td)
            out_a = temp_root / "build-a"
            out_b = temp_root / "build-b"
            extracted = temp_root / "runtime"
            campaign = temp_root / "campaign"

            command = [
                str(REPO_ROOT / "DEV" / "TOOLS" / "run_release_build"),
                "--tag",
                "v0.8",
            ]

            first = subprocess.run(
                [*command, "--output", str(out_a)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr or first.stdout)

            second = subprocess.run(
                [*command, "--output", str(out_b)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr or second.stdout)

            zip_a = out_a / ASSET_NAME
            zip_b = out_b / ASSET_NAME
            sha_a = zip_a.with_suffix(zip_a.suffix + ".sha256")
            sha_b = zip_b.with_suffix(zip_b.suffix + ".sha256")

            self.assertTrue(zip_a.is_file())
            self.assertTrue(zip_b.is_file())
            self.assertEqual(zip_a.read_bytes(), zip_b.read_bytes())
            self.assertEqual(sha_a.read_text(encoding="utf-8"), sha_b.read_text(encoding="utf-8"))

            with zipfile.ZipFile(zip_a) as archive:
                names = archive.namelist()
                self.assertIn("ENGINE_VERSION.yaml", names)
                self.assertIn("TOOLS/init_campaign.py", names)
                self.assertTrue(any(name.startswith("CORE/") for name in names))
                self.assertTrue(any(name.startswith("INSTALL/") for name in names))
                self.assertFalse(any(name.startswith("GAME/") for name in names))
                self.assertFalse(any(name.startswith("DEV/") for name in names))
                self.assertNotIn("AGENTS.md", names)
                archive.extractall(extracted)

            generator = extracted / "TOOLS" / "init_campaign.py"
            generated = subprocess.run(
                [
                    sys.executable,
                    str(generator),
                    "--output",
                    str(campaign),
                    "--campaign-id",
                    "camp-release-smoke",
                    "--branch",
                    "campaign/20990101",
                    "--engine-tag",
                    "dev-v0.8",
                    "--created-at",
                    "2099-01-01T00:00:00+00:00",
                    "--creator-github-login",
                    "audit-user",
                    "--mode",
                    "singleplayer",
                    "--source-root",
                    str(extracted),
                ],
                cwd=extracted,
                capture_output=True,
                text=True,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr or generated.stdout)
            self.assertTrue((campaign / "MANIFEST.yaml").is_file())
            self.assertTrue((campaign / "CAMPAIGN_CARD.yaml").is_file())
            self.assertTrue((campaign / "README.md").is_file())
            self.assertFalse((campaign / "CAMPAIGN" / "MANIFEST.yaml").exists())
            self.assertFalse((campaign / "DND_STORAGE.yaml").exists())


if __name__ == "__main__":
    unittest.main()
