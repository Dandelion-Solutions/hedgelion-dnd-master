from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "GAME"


class MultiRuntimeBootstrapContractTests(unittest.TestCase):
    def test_project_instructions_allow_multiple_runtime_zips_and_lazy_extraction(self):
        src = (GAME / "INSTALL" / "PROJECT_INSTRUCTIONS.txt").read_text(encoding="utf-8")
        self.assertNotIn("Ensure exactly one D&D Master runtime release ZIP", src)
        self.assertIn("multiple", src.lower())
        self.assertIn("hedgelion-dnd-master-runtime-v<version>.zip", src)
        self.assertIn("RUNTIME_PACKAGE.yaml", src)
        self.assertIn("must not eagerly extract", src.lower())
        self.assertIn("silently re-extract", src.lower())

    def test_install_bootstrap_binds_one_isolated_current_runtime_root(self):
        src = (GAME / "INSTALL" / "00_DND_BOOTSTRAP.md").read_text(encoding="utf-8")
        self.assertIn("current_runtime_root", src)
        self.assertIn("<version>/<package_sha256>", src)
        self.assertIn("RUNTIME_PACKAGE.yaml", src)
        self.assertIn("silently re-extract", src.lower())
        self.assertIn("MUST NOT globally search", src)

    def test_core_bootstrap_keeps_sibling_runtime_caches_inert(self):
        src = (GAME / "CORE" / "BOOTSTRAP_RUNTIME.md").read_text(encoding="utf-8")
        self.assertIn("current_runtime_root", src)
        self.assertIn("Sibling cached engine versions are inert", src)
        self.assertIn("RUNTIME_PACKAGE.yaml", src)
        self.assertIn("package_sha256", src)
        self.assertIn("silently re-extract", src.lower())

    def test_tagged_runtime_is_published_independent_of_release_status(self):
        install = (GAME / "INSTALL" / "00_DND_BOOTSTRAP.md").read_text(encoding="utf-8")
        core = (GAME / "CORE" / "BOOTSTRAP_RUNTIME.md").read_text(encoding="utf-8")

        for src in (install, core):
            self.assertIn("RUNTIME_PACKAGE.source_state: tagged", src)
            self.assertIn("regardless of `ENGINE_VERSION.release_status`", src)
            self.assertIn("dev-v<ENGINE_VERSION.engine_version>", src)
            self.assertNotIn("For `ENGINE_VERSION.release_status: development`:", src)


if __name__ == "__main__":
    unittest.main()
