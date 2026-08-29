from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "TOOLS"
sys.path.insert(0, str(TOOLS))

from verify_documentation_corpus_migration_candidate import (
    _append_derived_path_repairs,
    _is_historical_exception,
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


if __name__ == "__main__":
    unittest.main()
