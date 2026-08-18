from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
ASSET_NAME = "hedgelion-dnd-master-runtime-v0.8.zip"


def git_commit_datetime(revision: str) -> datetime:
    cp = subprocess.run(
        ["git", "show", "-s", "--format=%cI", revision],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return datetime.fromisoformat(cp.stdout.strip())


class ReleaseIntegrationTests(unittest.TestCase):
    def test_canonical_entry_point_builds_reproducible_flat_runtime_and_generator_smoke(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hdm-release-integration-") as td:
            temp_root = Path(td)
            out_a = temp_root / "build-a"
            out_b = temp_root / "build-b"
            extracted = temp_root / "runtime"
            campaign = temp_root / "campaign"

            command = [
                sys.executable,
                str(REPO_ROOT / "DEV" / "TOOLS" / "run_release_build.py"),
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
            package_sha256 = hashlib.sha256(zip_a.read_bytes()).hexdigest()

            expected_dt = git_commit_datetime("HEAD")
            expected_zip_time = (
                expected_dt.year,
                expected_dt.month,
                expected_dt.day,
                expected_dt.hour,
                expected_dt.minute,
                expected_dt.second - (expected_dt.second % 2),
            )

            with zipfile.ZipFile(zip_a) as archive:
                names = archive.namelist()
                self.assertIn("ENGINE_VERSION.yaml", names)
                self.assertIn("RUNTIME_PACKAGE.yaml", names)
                self.assertIn("TOOLS/init_campaign.py", names)
                self.assertTrue(any(name.startswith("CORE/") for name in names))
                self.assertTrue(any(name.startswith("INSTALL/") for name in names))
                self.assertFalse(any(name.startswith("GAME/") for name in names))
                self.assertFalse(any(name.startswith("DEV/") for name in names))
                self.assertNotIn("AGENTS.md", names)
                file_times = {info.date_time for info in archive.infolist() if not info.is_dir()}
                self.assertEqual(file_times, {expected_zip_time})
                package_meta = yaml.safe_load(archive.read("RUNTIME_PACKAGE.yaml"))
                archive.extractall(extracted)

            generator = extracted / "TOOLS" / "init_campaign.py"
            generator_args = [
                sys.executable,
                str(generator),
                "--output",
                str(campaign),
                "--campaign-id",
                "camp-release-smoke",
                "--branch",
                "campaign/20990101",
                "--engine-version",
                str(package_meta["engine_version"]),
                "--package-id",
                str(package_meta["package_id"]),
                "--package-sha256",
                package_sha256,
                "--created-at",
                "2099-01-01T00:00:00+00:00",
                "--creator-github-login",
                "audit-user",
                "--mode",
                "singleplayer",
                "--source-root",
                str(extracted),
            ]
            if package_meta.get("source_commit_sha"):
                generator_args.extend(["--source-commit-sha", str(package_meta["source_commit_sha"])])
            generated = subprocess.run(
                generator_args,
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
            manifest = yaml.safe_load((campaign / "MANIFEST.yaml").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 3)
            self.assertEqual(manifest["engine"]["current"]["package_sha256"], package_sha256)
            self.assertEqual(manifest["engine"]["current"]["package_id"], package_meta["package_id"])


if __name__ == "__main__":
    unittest.main()
