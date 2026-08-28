import importlib.util
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
import yaml
from GAME.TOOLS.ruleset_package import INVENTORY_DOMAIN, canonical_json, sha256, compile_conformance_attestation

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'DEV' / 'TOOLS' / 'release_builder.py'


def load_module():
    spec = importlib.util.spec_from_file_location('release_builder', MOD)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules['release_builder'] = module
    spec.loader.exec_module(module)
    return module


def write_ruleset_package(root: Path, engine_version: str, *, flattened: bool = False):
    package = root / ("RULES" if flattened else "GAME/RULES") / "packages" / "hdm.rules.dnd2024-srd52-core"
    package.mkdir(parents=True, exist_ok=True)
    (package / "character-capabilities.json").write_text('{"identity_source":"ruleset-package-manifest.json","profile_id":"test.profile"}\n', encoding="utf-8")
    (package / "gameplay.json").write_text('{"activity_definitions":[]}\n', encoding="utf-8")
    manifest = {
        "manifest_schema_version": 1, "package_id": "hdm.rules.dnd2024-srd52-core", "package_version": "0.1.0-mvp",
        "compatibility_id": "hdm.rules.dnd2024-srd52.v1", "engine_requirement": {"engine_version": engine_version},
        "catalog_generation": "2.0.0", "owned_namespaces": ["activity.*"], "dependencies": [],
        "content_files": ["ruleset-package-manifest.json", "character-capabilities.json", "gameplay.json"],
    }
    (package / "ruleset-package-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return package


def engine_inventory(m, engine_version, ruleset_set_sha256):
    core = {
        "inventory_schema_version":1,
        "engine_version":engine_version,
        "ruleset_set_sha256":ruleset_set_sha256,
        "items":[
            {"family":family,"contract_id":f"engine_contract.{family}.v1","semantic_sha256":"a"*64}
            for family in sorted(m.REQUIRED_ENGINE_CONTRACT_FAMILIES)
        ],
    }
    return {**core, "inventory_sha256":sha256(INVENTORY_DOMAIN + canonical_json(core))}


def validator_results():
    return [
        {"validator_id":validator_id,"result":"PASS"}
        for validator_id in sorted({
            "character_seed_closure","health_effect_recovery_closure",
            "domain_rules_coverage_closure","house_rules_boundary_closure",
        })
    ]


class ReleaseBuilderContractTests(unittest.TestCase):
    def test_output_inside_game_is_rejected(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            game = root / 'GAME'
            game.mkdir()
            with self.assertRaises(m.BuildError):
                m.validate_output_dir(root, game / 'dist')

    def test_game_manifest_rejects_development_revision_fields(self):
        m = load_module()
        data = {
            'engine_version': 0.8,
            'release_status': 'development',
            'repository': 'Dandelion-Solutions/hedgelion-dnd-master',
            'engine_owner_login': 'dkolyada',
            'rules_baseline': 'D&D 2024 / SRD 5.2.1',
            'schema_version': 2,
            'campaign_update': {'compatibility': 'maintenance_required'},
            'recommended_tag': 'v0.8',
            'runtime_scope_revision': 3,
        }
        with self.assertRaises(m.BuildError):
            m.validate_game_manifest_shape(data)

    def test_runtime_asset_name_is_derived_from_validated_tag(self):
        m = load_module()
        self.assertEqual(m.runtime_asset_name('v0.8'), 'hedgelion-dnd-master-runtime-v0.8.zip')

    def test_runtime_asset_name_rejects_non_version_tag(self):
        m = load_module()
        with self.assertRaises(m.BuildError):
            m.runtime_asset_name('vbanana')

    def test_source_archive_shape_is_rejected(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            wrapper = root / 'Dandelion-Solutions-hedgelion-dnd-master-deadbeef'
            (wrapper / 'GAME' / 'CORE').mkdir(parents=True)
            (wrapper / 'GAME' / 'ENGINE_VERSION.yaml').write_text('engine_version: 0.8\n')
            with self.assertRaises(m.BuildError):
                m.validate_extracted_package_root(root)

    def test_package_root_shape_accepts_flattened_game_contents(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for d in ('CORE', 'INSTALL', 'RULES', 'SCHEMA', 'CAMPAIGN', 'TEMPLATE', 'MIGRATIONS', 'TOOLS'):
                (root / d).mkdir()
            (root / 'ENGINE_VERSION.yaml').write_text('engine_version: 0.8\n')
            package = write_ruleset_package(root, "0.8", flattened=True)
            lock, _ = m.build_resolved_lock([package], root_package_ids=["hdm.rules.dnd2024-srd52-core"], engine_version="0.8", catalog_generation="2.0.0")
            inventory = engine_inventory(m,'0.8',lock['ruleset_set_sha256'])
            attestation = compile_conformance_attestation(inventory,validator_results(),lock=lock,engine_version='0.8')
            metadata = {'schema_version':2,'engine_version':'0.8','package_id':'dev-v0.8','source_state':'non_git','source_ref':None,'source_commit_sha':None,'ruleset_set_sha256':lock['ruleset_set_sha256'],'resolved_ruleset_lock':lock,'ruleset_engine_contract_inventory':inventory,'ruleset_conformance_attestation':attestation}
            (root / 'RUNTIME_PACKAGE.yaml').write_text(yaml.safe_dump(metadata, sort_keys=False), encoding='utf-8')
            self.assertEqual(m.validate_extracted_package_root(root), root)
            self.assertFalse((root / 'DEV').exists())
            (package / 'gameplay.json').write_text('{"activity_definitions":[{"id":"activity.tampered"}]}\n', encoding='utf-8')
            with self.assertRaises(m.BuildError):
                m.validate_extracted_package_root(root)


class ReleaseBuilderZipTests(unittest.TestCase):
    def _write_manifest_pair(self, root: Path, status: str = 'development'):
        dev = root / 'DEV'
        game = root / 'GAME'
        dev.mkdir(parents=True, exist_ok=True)
        game.mkdir(parents=True, exist_ok=True)
        shared = (
            'engine_version: 0.8\n'
            f'release_status: {status}\n'
            'repository: Dandelion-Solutions/hedgelion-dnd-master\n'
            'engine_owner_login: dkolyada\n'
            'rules_baseline: D&D 2024 / SRD 5.2.1\n'
            'schema_version: 2\n'
            'campaign_update:\n  compatibility: maintenance_required\n'
            'recommended_tag: v0.8\n'
        )
        (game / 'ENGINE_VERSION.yaml').write_text(shared, encoding='utf-8')
        (dev / 'ENGINE_DEVELOPMENT.yaml').write_text(shared + 'runtime_scope_revision: 3\n', encoding='utf-8')
        for d in ('CORE','INSTALL','RULES','SCHEMA','CAMPAIGN','TOOLS','TEMPLATE','MIGRATIONS'):
            (game / d).mkdir()
        write_ruleset_package(root, "0.8")
        (game / 'CORE' / 'x.md').write_text('x\n', encoding='utf-8')
        (game / 'INSTALL' / 'PROJECT_INSTRUCTIONS.txt').write_text('hello\n', encoding='utf-8')
        (game / 'INSTALL' / 'README.md').write_text('```text\nhello\n```\n', encoding='utf-8')
        (game / 'CAMPAIGN' / 'README.md').write_text('campaign\n', encoding='utf-8')
        (game / 'TEMPLATE' / 'STORAGE_README.md').write_text('storage\n', encoding='utf-8')

    def test_manifest_pair_rejects_shared_field_drift(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_manifest_pair(root)
            p = root / 'GAME' / 'ENGINE_VERSION.yaml'
            p.write_text(p.read_text().replace('v0.8', 'v0.9'), encoding='utf-8')
            with self.assertRaises(m.BuildError):
                m.load_and_validate_manifests(root)

    def test_tag_mode_allows_development_status(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_manifest_pair(root, status='development')
            m.load_and_validate_manifests(root, intended_tag='v0.8', tag_mode=True)

    def test_manifest_validation_is_not_hardcoded_to_v0_8(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_manifest_pair(root, status='development')
            for rel in ('GAME/ENGINE_VERSION.yaml', 'DEV/ENGINE_DEVELOPMENT.yaml'):
                p = root / rel
                p.write_text(p.read_text(encoding='utf-8').replace('0.8', '0.9'), encoding='utf-8')
            m.load_and_validate_manifests(root, intended_tag='v0.9', tag_mode=True)

    def test_build_zip_flattens_game_and_is_reproducible(self):
        import hashlib
        import zipfile
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_manifest_pair(root)
            out = root / '.hdm-release'
            package = root / 'GAME/RULES/packages/hdm.rules.dnd2024-srd52-core'
            lock, snapshots = m.build_resolved_lock([package], root_package_ids=['hdm.rules.dnd2024-srd52-core'], engine_version='0.8', catalog_generation='2.0.0')
            inventory = engine_inventory(m,'0.8',lock['ruleset_set_sha256'])
            integrated = (lock, snapshots, inventory, validator_results())
            with mock.patch.object(m, 'validate_integrated_ruleset_package', return_value=integrated):
                a = m.build_runtime_zip(root, out, 'v0.8')
            first = a.read_bytes()
            a.unlink()
            with mock.patch.object(m, 'validate_integrated_ruleset_package', return_value=integrated):
                b = m.build_runtime_zip(root, out, 'v0.8')
            second = b.read_bytes()
            self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())
            with zipfile.ZipFile(b) as zf:
                names = zf.namelist()
            self.assertIn('ENGINE_VERSION.yaml', names)
            self.assertIn('RUNTIME_PACKAGE.yaml', names)
            self.assertIn('CORE/x.md', names)
            self.assertNotIn('GAME/ENGINE_VERSION.yaml', names)
            self.assertFalse(any(n.startswith('DEV/') for n in names))


class ReleaseBuilderSafetyTests(unittest.TestCase):
    def _root(self, td: str) -> Path:
        root = Path(td)
        game = root / 'GAME'
        dev = root / 'DEV'
        game.mkdir(); dev.mkdir()
        manifest = (
            'engine_version: 0.8\nrelease_status: development\n'
            'repository: Dandelion-Solutions/hedgelion-dnd-master\n'
            'engine_owner_login: dkolyada\n'
            'rules_baseline: D&D 2024 / SRD 5.2.1\nschema_version: 2\n'
            'campaign_update:\n  compatibility: maintenance_required\nrecommended_tag: v0.8\n'
        )
        (game/'ENGINE_VERSION.yaml').write_text(manifest)
        (dev/'ENGINE_DEVELOPMENT.yaml').write_text(manifest+'runtime_scope_revision: 3\n')
        for d in ('CORE','INSTALL','RULES','SCHEMA','CAMPAIGN','TOOLS','TEMPLATE','MIGRATIONS'):
            (game/d).mkdir()
        (game/'INSTALL'/'PROJECT_INSTRUCTIONS.txt').write_text('hello\n')
        (game/'INSTALL'/'README.md').write_text('```text\nhello\n```\n')
        (game/'CAMPAIGN'/'README.md').write_text('campaign\n')
        (game/'TEMPLATE'/'STORAGE_README.md').write_text('storage\n')
        return root

    def test_build_rejects_zip_junk_inside_game(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = self._root(td)
            (root/'GAME'/'old.zip').write_bytes(b'x')
            with self.assertRaises(m.BuildError):
                m.build_runtime_zip(root, root/'.hdm-release', 'v0.8')

    def test_destination_readme_must_not_reference_game_prefix(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = self._root(td)
            p = root/'GAME'/'TEMPLATE'/'STORAGE_README.md'
            p.write_text('[bad](GAME/CORE/RUNTIME.md)\n')
            with self.assertRaises(m.BuildError):
                m.validate_destination_markdown(p, destination_root_files={'README.md'}, destination_rel='README.md')

    def test_project_instructions_parity_detects_drift(self):
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = self._root(td)
            inst = root/'GAME'/'INSTALL'
            canonical = 'alpha\nbeta\n'
            (inst/'PROJECT_INSTRUCTIONS.txt').write_text(canonical)
            (inst/'README.md').write_text('before\n```text\nalpha\ngamma\n```\nafter\n')
            with self.assertRaises(m.BuildError):
                m.validate_project_instructions_parity(inst)


class ReleaseBuilderCliTests(unittest.TestCase):
    def test_main_prints_machine_readable_result(self):
        import contextlib, io
        m = load_module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            game = root/'GAME'; dev=root/'DEV'
            game.mkdir(); dev.mkdir()
            manifest = (
                'engine_version: 0.8\nrelease_status: development\n'
                'repository: Dandelion-Solutions/hedgelion-dnd-master\nengine_owner_login: dkolyada\n'
                'rules_baseline: D&D 2024 / SRD 5.2.1\nschema_version: 2\n'
                'campaign_update:\n  compatibility: maintenance_required\nrecommended_tag: v0.8\n'
            )
            (game/'ENGINE_VERSION.yaml').write_text(manifest)
            (dev/'ENGINE_DEVELOPMENT.yaml').write_text(manifest+'runtime_scope_revision: 3\n')
            for d in ('CORE','INSTALL','RULES','SCHEMA','CAMPAIGN','TOOLS','TEMPLATE','MIGRATIONS'):
                (game/d).mkdir()
            (game/'INSTALL'/'PROJECT_INSTRUCTIONS.txt').write_text('hello\n')
            (game/'INSTALL'/'README.md').write_text('```text\nhello\n```\n')
            (game/'CAMPAIGN'/'README.md').write_text('campaign\n')
            (game/'TEMPLATE'/'STORAGE_README.md').write_text('storage\n')
            out = root/'.hdm-release'
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc=m.main(['--repo-root',str(root),'--tag','v0.8','--output',str(out)])
            self.assertEqual(rc,0)
            payload=__import__('json').loads(buf.getvalue())
            self.assertEqual(payload['asset_name'],'hedgelion-dnd-master-runtime-v0.8.zip')
            self.assertTrue(Path(payload['runtime_zip']).is_file())
            self.assertTrue(Path(payload['sha256_file']).is_file())


class ReleaseLineageTests(unittest.TestCase):
    def test_tag_mode_requires_git_checkout_for_lineage_validation(self):
        m=load_module()
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            game=root/'GAME'; dev=root/'DEV'; game.mkdir(); dev.mkdir()
            manifest=(
                'engine_version: 0.8\nrelease_status: development\n'
                'repository: Dandelion-Solutions/hedgelion-dnd-master\nengine_owner_login: dkolyada\n'
                'rules_baseline: D&D 2024 / SRD 5.2.1\nschema_version: 2\n'
                'campaign_update:\n  compatibility: maintenance_required\nrecommended_tag: v0.8\n'
            )
            (game/'ENGINE_VERSION.yaml').write_text(manifest)
            (dev/'ENGINE_DEVELOPMENT.yaml').write_text(manifest+'runtime_scope_revision: 3\n')
            with self.assertRaises(m.BuildError):
                m.validate_tag_lineage(root)


class ReleaseBuilderIntegratedValidationTests(unittest.TestCase):
    def _fixture(self, td: str) -> Path:
        root=Path(td); game=root/'GAME'; dev=root/'DEV'; game.mkdir(); dev.mkdir()
        manifest=(
            'engine_version: 0.8\nrelease_status: development\n'
            'repository: Dandelion-Solutions/hedgelion-dnd-master\nengine_owner_login: dkolyada\n'
            'rules_baseline: D&D 2024 / SRD 5.2.1\nschema_version: 2\n'
            'campaign_update:\n  compatibility: maintenance_required\nrecommended_tag: v0.8\n'
        )
        (game/'ENGINE_VERSION.yaml').write_text(manifest)
        (dev/'ENGINE_DEVELOPMENT.yaml').write_text(manifest+'runtime_scope_revision: 3\n')
        for d in ('CORE','INSTALL','RULES','SCHEMA','CAMPAIGN','TOOLS','TEMPLATE','MIGRATIONS'):
            (game/d).mkdir()
        canonical='hello\n'
        (game/'INSTALL'/'PROJECT_INSTRUCTIONS.txt').write_text(canonical)
        (game/'INSTALL'/'README.md').write_text('```text\nhello\n```\n')
        (game/'CAMPAIGN'/'README.md').write_text('campaign\n')
        (game/'TEMPLATE'/'STORAGE_README.md').write_text('storage\n')
        return root

    def test_build_runs_package_link_validation(self):
        m=load_module()
        with tempfile.TemporaryDirectory() as td:
            root=self._fixture(td)
            (root/'GAME'/'CORE'/'broken.md').write_text('[missing](NOPE.md)\n')
            with self.assertRaises(m.BuildError):
                m.build_runtime_zip(root, root/'.hdm-release', 'v0.8')


if __name__ == '__main__':
    unittest.main()
