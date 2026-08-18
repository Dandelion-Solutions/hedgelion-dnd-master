import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / 'DEV' / 'TOOLS' / 'run_release_build.py'
LEGACY_LAUNCHER = ROOT / 'DEV' / 'TOOLS' / 'run_release_build'


def load_launcher():
    spec = importlib.util.spec_from_file_location('run_release_build_test_module', LAUNCHER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ReleaseLocalOutputTests(unittest.TestCase):
    def test_canonical_launcher_is_python_file_and_legacy_name_is_absent(self):
        self.assertTrue(LAUNCHER.is_file())
        self.assertFalse(LEGACY_LAUNCHER.exists())

    def test_launcher_defaults_output_to_repo_builds_and_allows_omitted_tag(self):
        module = load_launcher()
        captured = {}

        def fake_run(cmd, cwd):
            captured['cmd'] = cmd
            captured['cwd'] = cwd
            return SimpleNamespace(returncode=0)

        with (
            mock.patch.object(module, 'ensure_environment', return_value=Path(sys.executable)),
            mock.patch.object(module.subprocess, 'run', side_effect=fake_run),
            mock.patch.object(sys, 'argv', ['run_release_build.py']),
        ):
            try:
                rc = module.main()
            except SystemExit as exc:
                self.fail(f'launcher should accept omitted --tag/--output, exited {exc.code}')

        self.assertEqual(rc, 0)
        output_index = captured['cmd'].index('--output') + 1
        self.assertEqual(Path(captured['cmd'][output_index]), ROOT / 'builds')
        self.assertNotIn('--tag', captured['cmd'])
        self.assertEqual(captured['cwd'], ROOT)

    def test_launcher_forwards_explicit_tag(self):
        module = load_launcher()
        captured = {}

        def fake_run(cmd, cwd):
            captured['cmd'] = cmd
            return SimpleNamespace(returncode=0)

        with (
            mock.patch.object(module, 'ensure_environment', return_value=Path(sys.executable)),
            mock.patch.object(module.subprocess, 'run', side_effect=fake_run),
            mock.patch.object(sys, 'argv', ['run_release_build.py', '--tag', 'v0.8']),
        ):
            rc = module.main()

        self.assertEqual(rc, 0)
        tag_index = captured['cmd'].index('--tag') + 1
        self.assertEqual(captured['cmd'][tag_index], 'v0.8')

    def test_current_and_legacy_local_release_directories_are_ignored(self):
        ignored = (ROOT / '.gitignore').read_text(encoding='utf-8').splitlines()
        self.assertIn('builds/', ignored)
        self.assertIn('.hdm-release/', ignored)


if __name__ == '__main__':
    unittest.main()
