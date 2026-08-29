import importlib.util
import shutil
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
    shutil.copytree(ROOT / 'GAME', game)
    shutil.copytree(ROOT / 'DEV' / 'CATALOG', dev / 'CATALOG')
    shutil.copytree(ROOT / 'DEV' / 'SCHEMAS', dev / 'SCHEMAS')
    shutil.copytree(ROOT / 'DEV' / 'TOOLS', dev / 'TOOLS')
    shutil.copytree(ROOT / 'DEV' / 'ARCHITECTURE', dev / 'ARCHITECTURE')
    owner = ROOT / 'DEV' / 'docs' / 'superpowers' / 'specs' / '2026-08-27-s6d-09-domain-rules-coverage-matrix-owner-decision.md'
    owner_target = dev / 'docs' / 'superpowers' / 'specs' / owner.name
    owner_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(owner, owner_target)
    for relative in (
        'DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md',
        'DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md',
        'DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md',
        'DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json',
        'DEV/TESTS/test_release_builder.py',
        'DEV/TESTS/test_s6d_07_character_mvp_seed.py',
        'DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py',
        'DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py',
        'DEV/TESTS/test_s6d_10_house_rules_boundary_contract.py',
        'DEV/TESTS/test_step3_execution_owner_contract.py',
        'DEV/TESTS/test_step3_resume_ordering_contract.py',
    ):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    shutil.copy2(ROOT / 'DEV' / 'ENGINE_DEVELOPMENT.yaml', dev / 'ENGINE_DEVELOPMENT.yaml')
    for name in ('LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md'):
        shutil.copy2(ROOT / name, root / name)
    shutil.copytree(ROOT / 'LICENSES', root / 'LICENSES')


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

            runtime_zip = module.build_runtime_zip(root, root / 'builds', 'v1.0-alpha')
            with zipfile.ZipFile(runtime_zip) as zf:
                names = set(zf.namelist())

            self.assertIn('future-root-file.dat', names)
            self.assertIn('FUTURE_AREA/nested.txt', names)


if __name__ == '__main__':
    unittest.main()
