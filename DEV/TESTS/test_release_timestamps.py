from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "DEV" / "TOOLS" / "release_builder.py"


def load_module():
    spec = importlib.util.spec_from_file_location("release_builder_timestamp_tests", MOD)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str, env: dict[str, str] | None = None) -> str:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    cp = subprocess.run(
        ["git", *args],
        cwd=root,
        env=merged_env,
        check=True,
        capture_output=True,
        text=True,
    )
    return cp.stdout.strip()


class ReleaseTimestampTests(unittest.TestCase):
    def _repo_with_two_commits(self, td: str) -> Path:
        root = Path(td)
        git(root, "init")
        git(root, "config", "user.name", "HDM Test")
        git(root, "config", "user.email", "hdm-test@example.invalid")

        (root / "payload.txt").write_text("one\n", encoding="utf-8")
        git(root, "add", "payload.txt")
        first_env = {
            "GIT_AUTHOR_DATE": "2026-08-18T09:11:12+02:00",
            "GIT_COMMITTER_DATE": "2026-08-18T09:11:12+02:00",
        }
        git(root, "commit", "-m", "first", env=first_env)
        git(root, "tag", "v9.9")

        (root / "payload.txt").write_text("two\n", encoding="utf-8")
        git(root, "add", "payload.txt")
        second_env = {
            "GIT_AUTHOR_DATE": "2026-08-18T10:22:24+02:00",
            "GIT_COMMITTER_DATE": "2026-08-18T10:22:24+02:00",
        }
        git(root, "commit", "-m", "second", env=second_env)
        return root

    def test_existing_tag_uses_date_of_commit_pointed_to_by_tag(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = self._repo_with_two_commits(td)
            observed = module.resolve_archive_datetime(root, "v9.9")
            self.assertEqual(observed, datetime.fromisoformat("2026-08-18T09:11:12+02:00"))

    def test_missing_tag_uses_head_commit_date(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = self._repo_with_two_commits(td)
            observed = module.resolve_archive_datetime(root, "v10.0")
            self.assertEqual(observed, datetime.fromisoformat("2026-08-18T10:22:24+02:00"))

    def test_one_second_commit_time_change_changes_zip_metadata_bytes(self):
        module = load_module()
        first = datetime.fromisoformat("2026-08-18T10:22:12+02:00")
        second = datetime.fromisoformat("2026-08-18T10:22:13+02:00")

        first_dos, first_extra = module._zip_timestamp_fields(first)
        second_dos, second_extra = module._zip_timestamp_fields(second)

        # Classic ZIP/DOS time truncates to two-second precision, so the visible
        # compatibility field can be identical while the standard extended mtime
        # still makes the archive metadata (and therefore SHA) different.
        self.assertEqual(first_dos, second_dos)
        self.assertNotEqual(first_extra, second_extra)


if __name__ == "__main__":
    unittest.main()
