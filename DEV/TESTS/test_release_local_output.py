import importlib.machinery
import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / 'DEV' / 'TOOLS' / 'run_release_build'


def load_launcher():
    loader = importlib.machinery.SourceFileLoader('run_release_build_test_module', str(LAUNCHER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ReleaseLocalOutputTests(unittest.TestCase):
    def test_launcher_defaults_output_to_repo_builds(self):
        module = load_launcher()
        captured = {}

        def fake_run(cmd, cwd):
            captured['cmd'] = cmd
            captured['cwd'] = cwd
            return SimpleNamespace(returncode=0)

        with (
            mock.patch.object(module, 'ensure_environment', return_value=Path(sys.executable)),
            mock.patch.object(module.subprocess, 'run', side_effect=fake_run),
            mock.patch.object(sys, 'argv', ['run_release_build', '--tag', 'v0.8']),
        ):
            try:
                rc = module.main()
            except SystemExit as exc:
                self.fail(f'launcher should accept omitted --output, exited {exc.code}')

        self.assertEqual(rc, 0)
        output_index = captured['cmd'].index('--output') + 1
        self.assertEqual(Path(captured['cmd'][output_index]), ROOT / 'builds')
        self.assertEqual(captured['cwd'], ROOT)

    def test_builds_directory_is_ignored_and_old_output_name_is_not(self):
        ignored = (ROOT / '.gitignore').read_text(encoding='utf-8').splitlines()
        self.assertIn('builds/', ignored)
        self.assertNotIn('.hdm-release/', ignored)


if __name__ == '__main__':
    unittest.main()
