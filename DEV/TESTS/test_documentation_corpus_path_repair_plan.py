import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))

from plan_documentation_corpus_path_repairs import build_path_repair_plan


class DocumentationCorpusPathRepairPlanTests(unittest.TestCase):
    def test_classifies_full_short_and_basename_only_occurrences_without_double_counting(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "docs").mkdir()
            (root / "docs/full.md").write_text(
                "DEV/docs/superpowers/specs/moved.md\n",
                encoding="utf-8",
            )
            (root / "docs/short.md").write_text(
                "../specs/moved.md\n",
                encoding="utf-8",
            )
            (root / "docs/bare.md").write_text(
                "moved.md\n",
                encoding="utf-8",
            )
            (root / "docs/retained.md").write_text(
                "DEV/docs/superpowers/specs/keep.md\n",
                encoding="utf-8",
            )

            migration = {
                "rows": [
                    {
                        "source_id": "S-001",
                        "old_path": "DEV/docs/superpowers/specs/moved.md",
                        "destination_path": "DEV/docs/superpowers/design/moved.md",
                        "action": "MOVE",
                    },
                    {
                        "source_id": "S-002",
                        "old_path": "DEV/docs/superpowers/specs/keep.md",
                        "destination_path": "DEV/docs/superpowers/specs/keep.md",
                        "action": "RETAIN",
                    },
                ]
            }
            repository_files = [
                root / "docs/bare.md",
                root / "docs/full.md",
                root / "docs/retained.md",
                root / "docs/short.md",
            ]

            plan = build_path_repair_plan(root, migration, repository_files=repository_files)

            self.assertEqual(plan["counts"]["full_old_path_occurrences"], 1)
            self.assertEqual(plan["counts"]["short_old_root_occurrences"], 1)
            self.assertEqual(plan["counts"]["basename_only_occurrences"], 1)
            self.assertEqual(plan["counts"]["mechanical_repair_occurrences"], 2)
            self.assertEqual(plan["counts"]["mechanical_repair_source_files"], 2)
            self.assertEqual(
                [(row["source_path"], row["kind"], row["old_literal"], row["new_literal"]) for row in plan["mechanical_repairs"]],
                [
                    (
                        "docs/full.md",
                        "FULL_OLD_PATH",
                        "DEV/docs/superpowers/specs/moved.md",
                        "DEV/docs/superpowers/design/moved.md",
                    ),
                    ("docs/short.md", "SHORT_OLD_ROOT_PATH", "specs/moved.md", "design/moved.md"),
                ],
            )
            self.assertEqual(
                [(row["source_path"], row["line"], row["target_path"]) for row in plan["basename_only_review"]],
                [("docs/bare.md", 1, "DEV/docs/superpowers/specs/moved.md")],
            )

    def test_non_utf8_files_are_reported_and_not_guessed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            binary = root / "binary.bin"
            binary.write_bytes(b"\xff\xfe")
            migration = {
                "rows": [
                    {
                        "source_id": "S-001",
                        "old_path": "DEV/docs/superpowers/specs/moved.md",
                        "destination_path": "DEV/docs/superpowers/design/moved.md",
                        "action": "MOVE",
                    }
                ]
            }

            plan = build_path_repair_plan(root, migration, repository_files=[binary])

            self.assertEqual(plan["non_utf8_files"], ["binary.bin"])
            self.assertEqual(plan["mechanical_repairs"], [])
            self.assertEqual(plan["basename_only_review"], [])


if __name__ == "__main__":
    unittest.main()
