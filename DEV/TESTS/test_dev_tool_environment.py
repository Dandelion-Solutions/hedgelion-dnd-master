from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "DEV/TOOLS/dev_tool_environment.py"


def load_module():
    spec = importlib.util.spec_from_file_location("dev_tool_environment", MODULE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DevToolEnvironmentTests(unittest.TestCase):
    def _requirements(self, root: Path, text: str = "jsonschema==4.26.0\nPyYAML==6.0.3\n") -> Path:
        path = root / "DEV/TOOLS/requirements-dev-tools.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_fingerprint_depends_on_requirements_bytes_and_python_minor(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            req = self._requirements(Path(td))
            a = m.compute_fingerprint(req, (3, 13))
            req.write_text("jsonschema==4.26.0\nPyYAML==6.0.4\n", encoding="utf-8")
            b = m.compute_fingerprint(req, (3, 13))
            c = m.compute_fingerprint(req, (3, 14))
            self.assertNotEqual(a, b)
            self.assertNotEqual(b, c)

    def test_warm_cache_skips_builder_and_pip(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            req = self._requirements(root)
            cache = root / ".hdm-devtools"
            venv_dir = cache / "venv"
            py = m.venv_python_path(venv_dir)
            py.parent.mkdir(parents=True)
            py.write_text("#!/bin/sh\n", encoding="utf-8")
            py.chmod(0o755)
            cache.mkdir(exist_ok=True)
            expected = m.compute_fingerprint(req, (3, 13))
            (cache / "fingerprint.json").write_text(json.dumps(expected), encoding="utf-8")
            builder = mock.Mock()
            runner = mock.Mock()
            self.assertEqual(
                m.ensure_environment(root, python_version=(3, 13), builder_factory=builder, runner=runner),
                py,
            )
            builder.assert_not_called()
            runner.assert_not_called()

    def test_missing_requirements_is_preparation_error(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(m.PreparationError):
                m.ensure_environment(Path(td), python_version=(3, 13))


if __name__ == "__main__":
    unittest.main()
