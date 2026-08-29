from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "TOOLS"
sys.path.insert(0, str(TOOLS))

from verify_documentation_corpus_migration_candidate import _is_historical_exception


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


if __name__ == "__main__":
    unittest.main()
