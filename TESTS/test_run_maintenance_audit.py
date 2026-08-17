from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "TOOLS" / "run_maintenance_audit"


def load_launcher():
    name = "hdm_run_maintenance_audit"
    sys.modules.pop(name, None)
    loader = importlib.machinery.SourceFileLoader(name, str(LAUNCHER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class MaintenanceAuditLauncherCoreTests(unittest.TestCase):
    def test_fingerprint_changes_with_requirements_bytes_and_python_version(self):
        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            req = Path(td) / "requirements-maintenance.txt"
            req.write_bytes(b"jsonschema==4.26.0\n")
            a = m.compute_fingerprint(req, (3, 13))
            req.write_bytes(b"jsonschema==4.27.0\n")
            b = m.compute_fingerprint(req, (3, 13))
            c = m.compute_fingerprint(req, (3, 14))
            self.assertNotEqual(a, b)
            self.assertNotEqual(b, c)
            self.assertEqual(a["python"], "3.13")

    def test_cache_is_current_requires_executable_python_and_exact_fingerprint(self):
        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            venv_dir = base / "venv"
            py = m.venv_python_path(venv_dir)
            py.parent.mkdir(parents=True)
            py.write_text("#!/bin/sh\n", encoding="utf-8")
            py.chmod(0o755)
            fp = base / "fingerprint.json"
            expected = {"requirements_sha256": "abc", "python": "3.13"}
            fp.write_text(json.dumps(expected), encoding="utf-8")
            self.assertTrue(m.cache_is_current(venv_dir, fp, expected))
            self.assertFalse(m.cache_is_current(venv_dir, fp, {**expected, "python": "3.14"}))
            py.chmod(0o644)
            if sys.platform != "win32":
                self.assertFalse(m.cache_is_current(venv_dir, fp, expected))


class MaintenanceAuditLauncherLifecycleTests(unittest.TestCase):
    def _write_requirements(self, root: Path, text: str = "jsonschema==4.26.0\n") -> Path:
        tools = root / "TOOLS"
        tools.mkdir(parents=True, exist_ok=True)
        req = tools / "requirements-maintenance.txt"
        req.write_text(text, encoding="utf-8")
        return req

    def _fake_builder(self, m, created):
        class FakeBuilder:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

            def create(self, path):
                created.append(Path(path))
                py = m.venv_python_path(Path(path))
                py.parent.mkdir(parents=True, exist_ok=True)
                py.write_text("#!/bin/sh\n", encoding="utf-8")
                py.chmod(0o755)

        return FakeBuilder

    def test_warm_cache_skips_builder_and_pip(self):
        from unittest import mock

        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            req = self._write_requirements(root)
            cache = root / ".hdm-maintenance"
            venv_dir = cache / "venv"
            py = m.venv_python_path(venv_dir)
            py.parent.mkdir(parents=True)
            py.write_text("#!/bin/sh\n", encoding="utf-8")
            py.chmod(0o755)
            expected = m.compute_fingerprint(req, (3, 13))
            cache.mkdir(exist_ok=True)
            (cache / "fingerprint.json").write_text(json.dumps(expected), encoding="utf-8")
            builder = mock.Mock()
            runner = mock.Mock()

            result = m.ensure_environment(
                root,
                python_version=(3, 13),
                builder_factory=builder,
                runner=runner,
            )

            self.assertEqual(result, py)
            builder.assert_not_called()
            runner.assert_not_called()

    def test_requirements_change_rebuilds_and_installs_tools_requirements(self):
        from unittest import mock

        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            req = self._write_requirements(root)
            cache = root / ".hdm-maintenance"
            cache.mkdir()
            (cache / "fingerprint.json").write_text(
                json.dumps({"requirements_sha256": "old", "python": "3.13"}),
                encoding="utf-8",
            )
            created = []
            runner = mock.Mock(return_value=mock.Mock(returncode=0))

            py = m.ensure_environment(
                root,
                python_version=(3, 13),
                builder_factory=self._fake_builder(m, created),
                runner=runner,
            )

            self.assertEqual(created, [root / ".hdm-maintenance" / "venv"])
            runner.assert_called_once()
            args, kwargs = runner.call_args
            self.assertEqual(args[0], [str(py), "-m", "pip", "install", "-r", str(req)])
            self.assertEqual(kwargs["cwd"], root)
            self.assertEqual(kwargs["env"]["PIP_DISABLE_PIP_VERSION_CHECK"], "1")
            self.assertEqual(kwargs["env"]["PIP_NO_INPUT"], "1")
            self.assertEqual(kwargs["env"]["PIP_RETRIES"], "1")
            self.assertEqual(kwargs["env"]["PIP_CACHE_DIR"], str(root / ".hdm-maintenance" / "pip-cache"))
            self.assertEqual(
                json.loads((cache / "fingerprint.json").read_text()),
                m.compute_fingerprint(req, (3, 13)),
            )

    def test_python_minor_change_invalidates_cache(self):
        from unittest import mock

        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            req = self._write_requirements(root)
            cache = root / ".hdm-maintenance"
            venv_dir = cache / "venv"
            py = m.venv_python_path(venv_dir)
            py.parent.mkdir(parents=True)
            py.write_text("#!/bin/sh\n", encoding="utf-8")
            py.chmod(0o755)
            cache.mkdir(exist_ok=True)
            old = m.compute_fingerprint(req, (3, 13))
            (cache / "fingerprint.json").write_text(json.dumps(old), encoding="utf-8")
            created = []
            runner = mock.Mock(return_value=mock.Mock(returncode=0))

            m.ensure_environment(
                root,
                python_version=(3, 14),
                builder_factory=self._fake_builder(m, created),
                runner=runner,
            )

            self.assertEqual(created, [venv_dir])
            self.assertEqual(
                json.loads((cache / "fingerprint.json").read_text()),
                m.compute_fingerprint(req, (3, 14)),
            )

    def test_pip_failure_leaves_no_success_fingerprint(self):
        from unittest import mock

        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_requirements(root)
            created = []
            runner = mock.Mock(return_value=mock.Mock(returncode=7))

            with self.assertRaises(m.PreparationError) as cm:
                m.ensure_environment(
                    root,
                    python_version=(3, 13),
                    builder_factory=self._fake_builder(m, created),
                    runner=runner,
                )

            self.assertEqual(cm.exception.exit_code, 7)
            self.assertFalse((root / ".hdm-maintenance" / "fingerprint.json").exists())

    def test_run_audit_propagates_exit_code(self):
        from unittest import mock

        m = load_launcher()
        runner = mock.Mock(return_value=mock.Mock(returncode=11))
        py = Path("/tmp/fake-python")

        rc = m.run_audit(py, runner=runner)

        self.assertEqual(rc, 11)
        runner.assert_called_once_with([str(py), str(m.AUDIT)], cwd=m.ROOT)


class MaintenanceAuditLauncherCliTests(unittest.TestCase):
    def test_missing_requirements_is_preparation_error(self):
        m = load_launcher()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(m.PreparationError) as cm:
                m.ensure_environment(root, python_version=(3, 13))
            self.assertIn("TOOLS/requirements-maintenance.txt", str(cm.exception))

    def test_main_reports_preparation_error_and_skips_audit(self):
        import contextlib
        import io
        from unittest import mock

        m = load_launcher()
        err = io.StringIO()
        with mock.patch.object(
            m,
            "ensure_environment",
            side_effect=m.PreparationError("maintenance dependency installation failed (exit 7)", 7),
        ), mock.patch.object(m, "run_audit") as run_audit, contextlib.redirect_stderr(err):
            rc = m.main()

        self.assertEqual(rc, 7)
        self.assertIn("ERROR: maintenance environment preparation failed:", err.getvalue())
        self.assertIn("maintenance dependency installation failed (exit 7)", err.getvalue())
        run_audit.assert_not_called()

    def test_main_runs_audit_after_environment_is_ready(self):
        from unittest import mock

        m = load_launcher()
        py = Path("/tmp/maintenance-python")
        with mock.patch.object(m, "ensure_environment", return_value=py) as ensure, mock.patch.object(
            m, "run_audit", return_value=9
        ) as run_audit:
            rc = m.main()

        self.assertEqual(rc, 9)
        ensure.assert_called_once_with(m.ROOT)
        run_audit.assert_called_once_with(py)


if __name__ == "__main__":
    unittest.main()
