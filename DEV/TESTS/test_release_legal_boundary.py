from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "DEV" / "TOOLS" / "release_builder.py"


def load_module():
    spec = importlib.util.spec_from_file_location("release_builder", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["release_builder"] = module
    spec.loader.exec_module(module)
    return module


def write_minimal_repo(root: Path) -> None:
    game = root / "GAME"
    dev = root / "DEV"
    game.mkdir()
    dev.mkdir()
    manifest = (
        "engine_version: 0.8\n"
        "release_status: development\n"
        "repository: Dandelion-Solutions/hedgelion-dnd-master\n"
        "engine_owner_login: dkolyada\n"
        "rules_baseline: D&D 2024 / SRD 5.2.1\n"
        "schema_version: 2\n"
        "campaign_update:\n  compatibility: maintenance_required\n"
        "recommended_tag: v0.8\n"
    )
    (game / "ENGINE_VERSION.yaml").write_text(manifest, encoding="utf-8")
    (dev / "ENGINE_DEVELOPMENT.yaml").write_text(
        manifest + "runtime_scope_revision: 3\n", encoding="utf-8"
    )
    for directory in ("CORE", "INSTALL", "RULES", "SCHEMA", "CAMPAIGN", "TOOLS", "TEMPLATE", "MIGRATIONS"):
        (game / directory).mkdir()
    (game / "INSTALL" / "PROJECT_INSTRUCTIONS.txt").write_text("hello\n", encoding="utf-8")
    (game / "INSTALL" / "README.md").write_text("```text\nhello\n```\n", encoding="utf-8")
    (game / "CAMPAIGN" / "README.md").write_text("campaign\n", encoding="utf-8")
    (game / "TEMPLATE" / "STORAGE_README.md").write_text("storage\n", encoding="utf-8")

    for base in (root, game):
        (base / "LICENSE").write_text("license\n", encoding="utf-8")
        (base / "NOTICE").write_text("notice\n", encoding="utf-8")
        (base / "THIRD_PARTY_NOTICES.md").write_text("third-party\n", encoding="utf-8")
        (base / "LICENSES").mkdir()
        (base / "LICENSES" / "SRD-5.2.1-ATTRIBUTION.md").write_text(
            "attribution\n", encoding="utf-8"
        )


class ReleaseLegalBoundaryTests(unittest.TestCase):
    def test_runtime_build_rejects_drift_from_canonical_legal_files(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_minimal_repo(root)
            (root / "GAME" / "NOTICE").write_text("stale notice\n", encoding="utf-8")

            with self.assertRaises(module.BuildError):
                module.build_runtime_zip(root, root / ".hdm-release", "v0.8")


if __name__ == "__main__":
    unittest.main()
