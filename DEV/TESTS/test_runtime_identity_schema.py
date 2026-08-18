from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class RuntimeIdentitySchemaTests(unittest.TestCase):
    def test_campaign_template_uses_created_with_and_current_runtime_identity(self):
        manifest = yaml.safe_load((ROOT / "GAME" / "CAMPAIGN" / "MANIFEST.yaml").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 3)
        engine = manifest["engine"]
        self.assertEqual(set(engine), {"created_with", "current", "update_policy"})
        self.assertEqual(
            set(engine["created_with"]),
            {"version", "package_id", "source_commit_sha"},
        )
        self.assertEqual(
            set(engine["current"]),
            {"version", "package_id", "source_commit_sha", "package_sha256", "adopted_at"},
        )
        for legacy in ("base_tag", "base_sha", "integrated_tag", "integrated_main_sha"):
            self.assertNotIn(legacy, engine)

    def test_storage_schema_v3_uses_portable_baseline_object(self):
        schema = yaml.safe_load((ROOT / "GAME" / "SCHEMA" / "dnd_storage.schema.yaml").read_text(encoding="utf-8"))
        self.assertEqual(schema["schema_version"], 3)
        baseline = schema["fields"]["engine"]["baseline"]
        self.assertEqual(
            set(baseline),
            {"version", "package_id", "source_commit_sha", "package_sha256", "adopted_at"},
        )
        self.assertNotIn("baseline_version", schema["fields"]["engine"])

    def test_campaign_generator_emits_new_runtime_identity_only(self):
        generator = ROOT / "GAME" / "TOOLS" / "init_campaign.py"
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign"
            cp = subprocess.run(
                [
                    sys.executable,
                    str(generator),
                    "--output",
                    str(output),
                    "--campaign-id",
                    "camp-runtime-schema",
                    "--branch",
                    "campaign/20990102",
                    "--engine-version",
                    "0.8",
                    "--package-id",
                    "dev-v0.8",
                    "--source-commit-sha",
                    "a" * 40,
                    "--package-sha256",
                    "b" * 64,
                    "--created-at",
                    "2099-01-02T00:00:00+00:00",
                    "--creator-github-login",
                    "audit-user",
                    "--source-root",
                    str(ROOT / "GAME"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(cp.returncode, 0, cp.stderr or cp.stdout)
            manifest = yaml.safe_load((output / "MANIFEST.yaml").read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema_version"], 3)
        self.assertEqual(
            manifest["engine"]["created_with"],
            {
                "version": "0.8",
                "package_id": "dev-v0.8",
                "source_commit_sha": "a" * 40,
            },
        )
        self.assertEqual(
            manifest["engine"]["current"],
            {
                "version": "0.8",
                "package_id": "dev-v0.8",
                "source_commit_sha": "a" * 40,
                "package_sha256": "b" * 64,
                "adopted_at": "2099-01-02T00:00:00+00:00",
            },
        )
        self.assertEqual(manifest["engine"]["update_policy"], "ask")
        for legacy in ("base_tag", "base_sha", "integrated_tag", "integrated_main_sha"):
            self.assertNotIn(legacy, manifest["engine"])


if __name__ == "__main__":
    unittest.main()
