from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "DEV" / "TOOLS" / "release_builder.py"


def load_module():
    spec = importlib.util.spec_from_file_location("runtime_package_provenance_tests", MOD)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RuntimePackageProvenanceTests(unittest.TestCase):
    def test_clean_checkout_metadata_records_exact_head(self):
        module = load_module()
        expected_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        meta = module.build_runtime_package_metadata(ROOT, "v0.8", tag_mode=False)

        self.assertEqual(meta["schema_version"], 1)
        self.assertEqual(meta["engine_version"], "0.8")
        self.assertEqual(meta["package_id"], "dev-v0.8")
        self.assertEqual(meta["source_state"], "clean_head")
        self.assertEqual(meta["source_ref"], "HEAD")
        self.assertEqual(meta["source_commit_sha"], expected_head)

    def test_built_zip_contains_one_generated_root_provenance_member(self):
        module = load_module()
        self.assertFalse((ROOT / "GAME" / "RUNTIME_PACKAGE.yaml").exists())

        with tempfile.TemporaryDirectory() as td:
            runtime_zip = module.build_runtime_zip(ROOT, Path(td), "v0.8")
            with zipfile.ZipFile(runtime_zip) as zf:
                names = zf.namelist()
                self.assertEqual(names.count("RUNTIME_PACKAGE.yaml"), 1)
                self.assertNotIn("GAME/RUNTIME_PACKAGE.yaml", names)
                meta = yaml.safe_load(zf.read("RUNTIME_PACKAGE.yaml"))

        self.assertEqual(meta["schema_version"], 1)
        self.assertEqual(meta["engine_version"], "0.8")
        self.assertEqual(meta["package_id"], "dev-v0.8")
        self.assertIn(meta["source_state"], {"tagged", "clean_head", "dirty_worktree", "non_git"})
        self.assertIn("source_ref", meta)
        self.assertIn("source_commit_sha", meta)


if __name__ == "__main__":
    unittest.main()
