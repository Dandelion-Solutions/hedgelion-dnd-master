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


class DestinationTemplateBoundaryTests(unittest.TestCase):
    def test_plain_text_source_path_must_not_leak_into_destination_template(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "STORAGE_README.md"
            source.write_text(
                "Internal source is GAME/TEMPLATE/STORAGE_README.md\n",
                encoding="utf-8",
            )
            with self.assertRaises(module.BuildError):
                module.validate_destination_markdown(
                    source,
                    destination_root_files={"README.md", "DND_STORAGE.yaml"},
                    destination_rel="README.md",
                )


if __name__ == "__main__":
    unittest.main()
