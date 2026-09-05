from __future__ import annotations

import importlib.util
import shutil
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


def run_git(root: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return cp.stdout.strip()


def init_fixture_repo(root: Path, release_status: str) -> str:
    run_git(root, "init")
    run_git(root, "config", "user.name", "HDM Test")
    run_git(root, "config", "user.email", "hdm-test@example.invalid")
    game = root / "GAME"
    dev = root / "DEV"
    shutil.copytree(ROOT / "GAME", game)
    for name in ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(ROOT / name, root / name)
    shutil.copytree(ROOT / "LICENSES", root / "LICENSES")
    (dev / "CATALOG").mkdir(parents=True)
    shutil.copytree(ROOT / "DEV" / "CATALOG", dev / "CATALOG", dirs_exist_ok=True)
    (dev / "SCHEMAS").mkdir(parents=True)
    shutil.copytree(ROOT / "DEV" / "SCHEMAS", dev / "SCHEMAS", dirs_exist_ok=True)
    shutil.copytree(ROOT / "DEV" / "TOOLS", dev / "TOOLS", dirs_exist_ok=True)
    shutil.copytree(ROOT / "DEV" / "ARCHITECTURE", dev / "ARCHITECTURE", dirs_exist_ok=True)
    for relative in (
        "DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md",
        "DEV/docs/superpowers/design/2026-08-27-s6d-09-domain-rules-coverage-matrix-owner-decision.md",
        "DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json",
        "DEV/TESTS/test_release_builder.py",
        "DEV/TESTS/test_s6d_07_character_mvp_seed.py",
        "DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py",
        "DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py",
        "DEV/TESTS/test_s6d_10_house_rules_boundary_contract.py",
        "DEV/TESTS/test_step3_execution_owner_contract.py",
        "DEV/TESTS/test_step3_resume_ordering_contract.py",
    ):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    shared = (
        "engine_version: 1.0-alpha\n"
        f"release_status: {release_status}\n"
        "repository: Dandelion-Solutions/hedgelion-dnd-master\n"
        "engine_owner_login: dkolyada\n"
        "rules_baseline: D&D 2024 / SRD 5.2.1\n"
        "campaign_contract_generation: 2\n"
        "campaign_update:\n"
        "  compatibility: maintenance_required\n"
        "recommended_tag: v1.0-alpha\n"
    )
    (game / "ENGINE_VERSION.yaml").write_text(shared, encoding="utf-8")
    (dev / "ENGINE_DEVELOPMENT.yaml").write_text(
        shared + "runtime_scope_revision: 3\n",
        encoding="utf-8",
    )
    (root / "tracked.txt").write_text("clean\n", encoding="utf-8")
    run_git(root, "add", ".")
    run_git(root, "commit", "-m", "fixture")
    return run_git(root, "rev-parse", "HEAD")


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

        meta = module.build_runtime_package_metadata(ROOT, "v1.0-alpha", tag_mode=False)

        self.assertEqual(meta["schema_version"], 3)
        self.assertEqual(meta["engine_version"], "1.0-alpha")
        self.assertEqual(meta["package_id"], "dev-v1.0-alpha")
        self.assertEqual(meta["source_state"], "clean_head")
        self.assertEqual(meta["source_ref"], "HEAD")
        self.assertEqual(meta["source_commit_sha"], expected_head)
        self.assertEqual(meta["ruleset_set_digest_generation"], 1)

    def test_tagged_metadata_records_exact_tagged_commit(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            expected_head = init_fixture_repo(root, "ready-for-tag")
            run_git(root, "tag", "v1.0-alpha")

            meta = module.build_runtime_package_metadata(root, "v1.0-alpha", tag_mode=True)

        self.assertEqual(meta["schema_version"], 3)
        self.assertEqual(meta["engine_version"], "1.0-alpha")
        self.assertEqual(meta["package_id"], "v1.0-alpha")
        self.assertEqual(meta["source_state"], "tagged")
        self.assertEqual(meta["source_ref"], "v1.0-alpha")
        self.assertEqual(meta["source_commit_sha"], expected_head)
        self.assertEqual(meta["ruleset_set_digest_generation"], 1)

    def test_dirty_worktree_does_not_falsely_claim_head_provenance(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init_fixture_repo(root, "development")
            (root / "tracked.txt").write_text("dirty\n", encoding="utf-8")

            meta = module.build_runtime_package_metadata(root, "v1.0-alpha", tag_mode=False)

        self.assertEqual(meta["schema_version"], 3)
        self.assertEqual(meta["engine_version"], "1.0-alpha")
        self.assertEqual(meta["package_id"], "dev-v1.0-alpha")
        self.assertEqual(meta["source_state"], "dirty_worktree")
        self.assertIsNone(meta["source_ref"])
        self.assertIsNone(meta["source_commit_sha"])
        self.assertEqual(meta["ruleset_set_digest_generation"], 1)

    def test_built_zip_contains_one_generated_root_provenance_member(self):
        module = load_module()
        self.assertFalse((ROOT / "GAME" / "RUNTIME_PACKAGE.yaml").exists())

        with tempfile.TemporaryDirectory() as td:
            runtime_zip = module.build_runtime_zip(ROOT, Path(td), "v1.0-alpha")
            with zipfile.ZipFile(runtime_zip) as zf:
                names = zf.namelist()
                self.assertEqual(names.count("RUNTIME_PACKAGE.yaml"), 1)
                self.assertNotIn("GAME/RUNTIME_PACKAGE.yaml", names)
                meta = yaml.safe_load(zf.read("RUNTIME_PACKAGE.yaml"))

        self.assertEqual(meta["schema_version"], 3)
        self.assertEqual(meta["engine_version"], "1.0-alpha")
        self.assertEqual(meta["package_id"], "dev-v1.0-alpha")
        self.assertIn(meta["source_state"], {"tagged", "clean_head", "dirty_worktree", "non_git"})
        self.assertIn("source_ref", meta)
        self.assertIn("source_commit_sha", meta)
        self.assertEqual(meta["ruleset_set_digest_generation"], 1)


if __name__ == "__main__":
    unittest.main()
