import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))

from apply_documentation_corpus_migration import apply_migration


class DocumentationCorpusMigrationApplyTests(unittest.TestCase):
    def test_applies_verified_repairs_moves_and_bounded_extraction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            specs = root / "DEV/docs/superpowers/specs"
            research = root / "DEV/docs/superpowers/research"
            design = root / "DEV/docs/superpowers/design"
            arch = root / "DEV/ARCHITECTURE"
            specs.mkdir(parents=True)
            research.mkdir(parents=True)
            design.mkdir(parents=True)
            arch.mkdir(parents=True)

            (specs / "move.md").write_text("payload\n", encoding="utf-8")
            (specs / "keep.md").write_text(
                "Derivation: `move.md`\n",
                encoding="utf-8",
            )
            (arch / "INDEX.md").write_text(
                "Owner: `DEV/docs/superpowers/specs/move.md`\n",
                encoding="utf-8",
            )
            (research / "mixed.md").write_text(
                "# Intro\n\n# 3. Current first-party ChatGPT evidence\n\n## H1\nFact one.\n\n## H8\nFact eight.\n\n# 4. Preliminary assurance disposition matrix\n\nDo not extract.\n",
                encoding="utf-8",
            )

            migration = {
                "rows": [
                    {
                        "source_id": "S-001",
                        "old_path": "DEV/docs/superpowers/specs/move.md",
                        "destination_path": "DEV/docs/superpowers/design/move.md",
                        "action": "MOVE",
                    },
                    {
                        "source_id": "S-002",
                        "old_path": "DEV/docs/superpowers/specs/keep.md",
                        "destination_path": "DEV/docs/superpowers/specs/keep.md",
                        "action": "RETAIN",
                    },
                    {
                        "source_id": "R-015",
                        "old_path": "DEV/docs/superpowers/research/mixed.md",
                        "destination_path": "DEV/docs/superpowers/design/mixed.md",
                        "action": "MOVE",
                    },
                ],
                "extractions": [
                    {
                        "source_id": "R-015",
                        "source_path": "DEV/docs/superpowers/research/mixed.md",
                        "destination_path": "DEV/docs/superpowers/research/extracted.md",
                    }
                ],
            }
            repairs = [
                {
                    "source_path": "DEV/ARCHITECTURE/INDEX.md",
                    "line": 1,
                    "old_literal": "DEV/docs/superpowers/specs/move.md",
                    "new_literal": "DEV/docs/superpowers/design/move.md",
                },
                {
                    "source_path": "DEV/docs/superpowers/specs/keep.md",
                    "line": 1,
                    "old_literal": "move.md",
                    "new_literal": "../design/move.md",
                },
            ]

            result = apply_migration(root, migration=migration, repairs=repairs)

            self.assertEqual(result["move_count"], 2)
            self.assertEqual(result["repair_count"], 2)
            self.assertEqual(result["extraction_count"], 1)
            self.assertFalse((specs / "move.md").exists())
            self.assertFalse((research / "mixed.md").exists())
            self.assertEqual((design / "move.md").read_text(encoding="utf-8"), "payload\n")
            self.assertIn("../design/move.md", (specs / "keep.md").read_text(encoding="utf-8"))
            self.assertIn("DEV/docs/superpowers/design/move.md", (arch / "INDEX.md").read_text(encoding="utf-8"))
            self.assertTrue((design / "mixed.md").exists())

            extracted = (research / "extracted.md").read_text(encoding="utf-8")
            self.assertIn("CURRENT_AUTHORITY: NONE — EVIDENCE ONLY", extracted)
            self.assertIn("SPLIT_FROM: `DEV/docs/superpowers/research/mixed.md`", extracted)
            self.assertIn("# 3. Current first-party ChatGPT evidence", extracted)
            self.assertIn("## H1", extracted)
            self.assertIn("## H8", extracted)
            self.assertNotIn("# 4. Preliminary assurance disposition matrix", extracted)
            self.assertNotIn("Do not extract.", extracted)

    def test_repair_mismatch_fails_before_any_move(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "DEV/docs/superpowers/specs/move.md"
            source.parent.mkdir(parents=True)
            source.write_text("payload\n", encoding="utf-8")
            consumer = root / "consumer.md"
            consumer.write_text("different\n", encoding="utf-8")

            migration = {
                "rows": [
                    {
                        "source_id": "S-001",
                        "old_path": "DEV/docs/superpowers/specs/move.md",
                        "destination_path": "DEV/docs/superpowers/design/move.md",
                        "action": "MOVE",
                    }
                ],
                "extractions": [],
            }
            repairs = [
                {
                    "source_path": "consumer.md",
                    "line": 1,
                    "old_literal": "missing.md",
                    "new_literal": "new.md",
                }
            ]

            with self.assertRaises(ValueError):
                apply_migration(root, migration=migration, repairs=repairs)

            self.assertTrue(source.exists())
            self.assertFalse((root / "DEV/docs/superpowers/design/move.md").exists())


if __name__ == "__main__":
    unittest.main()
