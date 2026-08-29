import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))

from build_documentation_corpus_migration_map import build_migration_map


class DocumentationCorpusMigrationMapTests(unittest.TestCase):
    def test_latest_specs_census_occurrence_wins_and_research_split_is_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            design = root / "DEV/docs/superpowers/design"
            design.mkdir(parents=True)

            (design / "2026-08-29-documentation-corpus-refactor-census.md").write_text(
                "### R-001 — `keep.md`\n"
                "- **FINAL_DESTINATION_FILES:** same research artifact.\n\n"
                "### R-002 — `move.md`\n"
                "- **FINAL_DESTINATION_FILES:** corresponding `design/` path.\n\n"
                "### R-003 — `split.md`\n"
                "- **FINAL_DESTINATION_FILES:** `design/split.md`; new `research/extracted.md`.\n",
                encoding="utf-8",
            )
            (design / "2026-08-29-documentation-corpus-refactor-specs-census-part-01.md").write_text(
                "## S-001 — `pending.md`\n"
                "- **FINAL_DESTINATION_FILES:** `PENDING_FINAL_SUPERSESSION_CHECK`; remain in `specs/` meanwhile.\n\n"
                "## S-002 — `evidence.md`\n"
                "- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/research/evidence.md`.\n\n"
                "## S-003 — `law.md`\n"
                "- **FINAL_DESTINATION_FILES:** unchanged `DEV/docs/superpowers/specs/law.md`.\n",
                encoding="utf-8",
            )
            (design / "2026-08-29-documentation-corpus-refactor-specs-census-part-61.md").write_text(
                "## S-001 — `pending.md`\n"
                "- **FINAL DESTINATION:** `DEV/docs/superpowers/design/pending.md`.\n",
                encoding="utf-8",
            )

            targets = [
                {"target_path": "DEV/docs/superpowers/research/keep.md", "basename": "keep.md"},
                {"target_path": "DEV/docs/superpowers/research/move.md", "basename": "move.md"},
                {"target_path": "DEV/docs/superpowers/research/split.md", "basename": "split.md"},
                {"target_path": "DEV/docs/superpowers/specs/pending.md", "basename": "pending.md"},
                {"target_path": "DEV/docs/superpowers/specs/evidence.md", "basename": "evidence.md"},
                {"target_path": "DEV/docs/superpowers/specs/law.md", "basename": "law.md"},
            ]

            result = build_migration_map(root, targets=targets)
            rows = {row["old_path"]: row for row in result["rows"]}

            self.assertEqual(rows["DEV/docs/superpowers/research/keep.md"]["action"], "RETAIN")
            self.assertEqual(
                rows["DEV/docs/superpowers/research/move.md"]["destination_path"],
                "DEV/docs/superpowers/design/move.md",
            )
            self.assertEqual(
                rows["DEV/docs/superpowers/research/split.md"]["destination_path"],
                "DEV/docs/superpowers/design/split.md",
            )
            self.assertEqual(
                rows["DEV/docs/superpowers/specs/pending.md"]["destination_path"],
                "DEV/docs/superpowers/design/pending.md",
            )
            self.assertEqual(
                rows["DEV/docs/superpowers/specs/evidence.md"]["destination_path"],
                "DEV/docs/superpowers/research/evidence.md",
            )
            self.assertEqual(rows["DEV/docs/superpowers/specs/law.md"]["action"], "RETAIN")
            self.assertEqual(
                result["extractions"],
                [
                    {
                        "source_id": "R-003",
                        "source_path": "DEV/docs/superpowers/research/split.md",
                        "destination_path": "DEV/docs/superpowers/research/extracted.md",
                    }
                ],
            )
            self.assertEqual(result["unresolved_targets"], [])

    def test_missing_census_disposition_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            design = root / "DEV/docs/superpowers/design"
            design.mkdir(parents=True)
            (design / "2026-08-29-documentation-corpus-refactor-census.md").write_text(
                "### R-001 — `known.md`\n- **FINAL_DESTINATION_FILES:** same research artifact.\n",
                encoding="utf-8",
            )
            targets = [
                {"target_path": "DEV/docs/superpowers/research/known.md", "basename": "known.md"},
                {"target_path": "DEV/docs/superpowers/specs/missing.md", "basename": "missing.md"},
            ]

            result = build_migration_map(root, targets=targets)

            self.assertEqual(result["unresolved_targets"], ["DEV/docs/superpowers/specs/missing.md"])


if __name__ == "__main__":
    unittest.main()
