from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "TOOLS"
sys.path.insert(0, str(TOOLS))

from verify_documentation_corpus_migration_candidate import (
    _append_derived_path_repairs,
    _assert_no_stale_full_or_short_references,
    _is_historical_exception,
    _tracked_files,
)


class DocumentationCorpusCandidateVerifierTests(unittest.TestCase):
    def test_only_part13_reference_to_research_destination_is_historical_exception(self):
        source = "DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-13.md"
        self.assertTrue(
            _is_historical_exception(
                source,
                "DEV/docs/superpowers/research/example-evidence.md",
            )
        )
        self.assertFalse(
            _is_historical_exception(
                source,
                "DEV/docs/superpowers/design/example-record.md",
            )
        )
        self.assertFalse(
            _is_historical_exception(
                "DEV/docs/superpowers/design/other.md",
                "DEV/docs/superpowers/research/example-evidence.md",
            )
        )

    def test_release_fixture_derived_owner_destination_is_repaired_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fixture = root / "DEV/TESTS/test_release_game_passthrough.py"
            fixture.parent.mkdir(parents=True)
            fixture.write_text(
                "owner = ROOT / 'DEV' / 'docs' / 'superpowers' / 'design' / 'owner.md'\n"
                "owner_target = dev / 'docs' / 'superpowers' / 'specs' / owner.name\n",
                encoding="utf-8",
            )
            repairs = []
            _append_derived_path_repairs(root, repairs)

            self.assertEqual(len(repairs), 1)
            self.assertEqual(
                repairs[0],
                {
                    "source_path": "DEV/TESTS/test_release_game_passthrough.py",
                    "line": 2,
                    "old_literal": "owner_target = dev / 'docs' / 'superpowers' / 'specs' / owner.name",
                    "new_literal": "owner_target = dev / 'docs' / 'superpowers' / 'design' / owner.name",
                },
            )

    def test_release_fixture_derived_owner_destination_fails_closed_if_not_unique(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fixture = root / "DEV/TESTS/test_release_game_passthrough.py"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("# no derived owner target\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                _append_derived_path_repairs(root, [])

    def test_tracked_files_excludes_temporary_dcr_orchestration(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(
                ["git", "init", "-q"],
                cwd=root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            paths = [
                ".github/workflows/dcr-migration-candidate.yml",
                ".github/workflows/dcr-reference-audit.yml",
                "DEV/TOOLS/verify_documentation_corpus_migration_candidate.py",
                "DEV/TESTS/test_documentation_corpus_candidate_verifier.py",
                "DEV/ARCHITECTURE/keep.md",
            ]
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(relative + "\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "."],
                cwd=root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            observed = [path.relative_to(root).as_posix() for path in _tracked_files(root)]
            self.assertEqual(observed, ["DEV/ARCHITECTURE/keep.md"])

    def test_r015_extraction_split_from_old_path_is_frozen_provenance_exception(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = "DEV/docs/superpowers/research/2026-08-24-chatgpt-plus-host-evidence.md"
            old_path = "DEV/docs/superpowers/research/2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md"
            source = root / source_path
            source.parent.mkdir(parents=True)
            source.write_text(f"SPLIT_FROM: `{old_path}`\n", encoding="utf-8")
            migration = {
                "rows": [
                    {
                        "old_path": old_path,
                        "destination_path": "DEV/docs/superpowers/design/2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md",
                        "action": "MOVE",
                    }
                ]
            }
            report = {
                "references": [
                    {
                        "source_path": source_path,
                        "line": 1,
                        "target_path": old_path,
                        "matched_basename": Path(old_path).name,
                    }
                ]
            }
            _assert_no_stale_full_or_short_references(root, migration, report)

    def test_other_old_full_path_still_fails_frozen_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = "DEV/ARCHITECTURE/example.md"
            old_path = "DEV/docs/superpowers/specs/example-owner.md"
            source = root / source_path
            source.parent.mkdir(parents=True)
            source.write_text(f"live route: {old_path}\n", encoding="utf-8")
            migration = {
                "rows": [
                    {
                        "old_path": old_path,
                        "destination_path": "DEV/docs/superpowers/design/example-owner.md",
                        "action": "MOVE",
                    }
                ]
            }
            report = {
                "references": [
                    {
                        "source_path": source_path,
                        "line": 1,
                        "target_path": old_path,
                        "matched_basename": Path(old_path).name,
                    }
                ]
            }
            with self.assertRaises(RuntimeError):
                _assert_no_stale_full_or_short_references(root, migration, report)


if __name__ == "__main__":
    unittest.main()
