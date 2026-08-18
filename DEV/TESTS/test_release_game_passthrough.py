import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / 'DEV' / 'TOOLS' / 'release_builder.py'


def load_builder():
    spec = importlib.util.spec_from_file_location('release_builder_passthrough_test', BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_fixture(root: Path) -> None:
    game = root / 'GAME'
    dev = root / 'DEV'
    game.mkdir()
    dev.mkdir()
    manifest = (
        'engine_version: 0.8\n'
        'release_status: development\n'
        'repository: Dandelion-Solutions/hedgelion-dnd-master\n'
        'engine_owner_login: dkolyada\n'
        'rules_baseline: D&D 2024 / SRD 5.2.1\n'
        'schema_version: 2\n'
        'campaign_update:\n  compatibility: maintenance_required\n'
        'recommended_tag: v0.8\n'
    )
    (game / 'ENGINE_VERSION.yaml').write_text(manifest, encoding='utf-8')
    (dev / 'ENGINE_DEVELOPMENT.yaml').write_text(
        manifest + 'runtime_scope_revision: 3\n', encoding='utf-8'
    )
    for dirname in ('CORE', 'INSTALL', 'RULES', 'SCHEMA', 'CAMPAIGN', 'TEMPLATE', 'MIGRATIONS', 'TOOLS'):
        (game / dirname).mkdir()
    (game / 'INSTALL' / 'PROJECT_INSTRUCTIONS.txt').write_text('hello\n', encoding='utf-8')
    (game / 'INSTALL' / 'README.md').write_text('```text\nhello\n```\n', encoding='utf-8')
    (game / 'CAMPAIGN' / 'README.md').write_text('campaign\n', encoding='utf-8')
    (game / 'TEMPLATE' / 'STORAGE_README.md').write_text('storage\n', encoding='utf-8')


class ReleaseGamePassthroughTests(unittest.TestCase):
    def test_new_game_root_file_and_directory_are_automatically_archived(self):
        module = load_builder()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root)
            game = root / 'GAME'
            (game / 'future-root-file.dat').write_bytes(b'root')
            (game / 'FUTURE_AREA').mkdir()
            (game / 'FUTURE_AREA' / 'nested.txt').write_text('nested\n', encoding='utf-8')

            runtime_zip = module.build_runtime_zip(root, root / 'builds', 'v0.8')
            with zipfile.ZipFile(runtime_zip) as zf:
                names = set(zf.namelist())

            self.assertIn('future-root-file.dat', names)
            self.assertIn('FUTURE_AREA/nested.txt', names)


if __name__ == '__main__':
    unittest.main()
