import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))

from audit_documentation_corpus_references import build_reference_report, build_target_manifest


class DocumentationCorpusReferenceAuditTests(unittest.TestCase):
    def test_scans_every_utf8_file_for_full_relative_and_bare_corpus_references(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            specs = root / "DEV/docs/superpowers/specs"
            research = root / "DEV/docs/superpowers/research"
            specs.mkdir(parents=True)
            research.mkdir(parents=True)
            (specs / "alpha-spec.md").write_text("alpha\n", encoding="utf-8")
            (research / "beta-research.md").write_text("beta\n", encoding="utf-8")

            docs = root / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text(
                "full DEV/docs/superpowers/specs/alpha-spec.md\n"
                "relative ../research/beta-research.md\n"
                "bare alpha-spec.md\n",
                encoding="utf-8",
            )
            (docs / "binary.bin").write_bytes(b"\xff\xfe\x00\x01")

            report = build_reference_report(root)

            self.assertEqual(report["target_count"], 2)
            self.assertEqual(report["ambiguous_target_basenames"], {})
            self.assertEqual(report["binary_or_non_utf8_files"], ["docs/binary.bin"])
            refs = [
                (row["source_path"], row["line"], row["target_path"], row["matched_basename"])
                for row in report["references"]
            ]
            self.assertEqual(
                refs,
                [
                    ("docs/guide.md", 1, "DEV/docs/superpowers/specs/alpha-spec.md", "alpha-spec.md"),
                    ("docs/guide.md", 2, "DEV/docs/superpowers/research/beta-research.md", "beta-research.md"),
                    ("docs/guide.md", 3, "DEV/docs/superpowers/specs/alpha-spec.md", "alpha-spec.md"),
                ],
            )

    def test_reports_ambiguous_basenames_instead_of_guessing_target_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            specs = root / "DEV/docs/superpowers/specs"
            research = root / "DEV/docs/superpowers/research"
            specs.mkdir(parents=True)
            research.mkdir(parents=True)
            (specs / "same.md").write_text("spec\n", encoding="utf-8")
            (research / "same.md").write_text("research\n", encoding="utf-8")
            (root / "consumer.txt").write_text("same.md\n", encoding="utf-8")

            report = build_reference_report(root)

            self.assertEqual(
                report["ambiguous_target_basenames"],
                {
                    "same.md": [
                        "DEV/docs/superpowers/research/same.md",
                        "DEV/docs/superpowers/specs/same.md",
                    ]
                },
            )
            self.assertEqual(report["references"], [])

    def test_report_is_json_serializable_and_deterministically_sorted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            specs = root / "DEV/docs/superpowers/specs"
            specs.mkdir(parents=True)
            (specs / "zeta.md").write_text("zeta\n", encoding="utf-8")
            (specs / "alpha.md").write_text("alpha\n", encoding="utf-8")
            (root / "b.txt").write_text("zeta.md\n", encoding="utf-8")
            (root / "a.txt").write_text("alpha.md\n", encoding="utf-8")

            report = build_reference_report(root)
            json.dumps(report, sort_keys=True)

            self.assertEqual(
                [row["target_path"] for row in report["targets"]],
                [
                    "DEV/docs/superpowers/specs/alpha.md",
                    "DEV/docs/superpowers/specs/zeta.md",
                ],
            )
            self.assertEqual(
                [(row["source_path"], row["line"]) for row in report["references"]],
                [("a.txt", 1), ("b.txt", 1)],
            )

    def test_git_worktree_scans_only_tracked_branch_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            specs = root / "DEV/docs/superpowers/specs"
            specs.mkdir(parents=True)
            target = specs / "tracked-spec.md"
            target.write_text("target\n", encoding="utf-8")
            tracked = root / "tracked-consumer.md"
            tracked.write_text("tracked-spec.md\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "DEV/docs/superpowers/specs/tracked-spec.md", "tracked-consumer.md"],
                cwd=root,
                check=True,
            )

            untracked = root / "untracked-consumer.md"
            untracked.write_text("tracked-spec.md\n", encoding="utf-8")

            report = build_reference_report(root)

            self.assertEqual(report["scan_source"], "git_ls_files")
            self.assertEqual(report["tracked_file_count"], 2)
            self.assertEqual(
                [(row["source_path"], row["line"]) for row in report["references"]],
                [("tracked-consumer.md", 1)],
            )

    def test_frozen_target_manifest_still_finds_old_references_after_target_moves(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            specs = root / "DEV/docs/superpowers/specs"
            specs.mkdir(parents=True)
            target = specs / "old-spec.md"
            target.write_text("target\n", encoding="utf-8")
            consumer = root / "consumer.md"
            consumer.write_text("DEV/docs/superpowers/specs/old-spec.md\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)

            manifest = build_target_manifest(root)
            self.assertEqual(manifest["target_count"], 1)

            design = root / "DEV/docs/superpowers/design"
            design.mkdir(parents=True)
            subprocess.run(
                [
                    "git",
                    "mv",
                    "DEV/docs/superpowers/specs/old-spec.md",
                    "DEV/docs/superpowers/design/old-spec.md",
                ],
                cwd=root,
                check=True,
            )

            report = build_reference_report(root, targets=manifest["targets"])

            self.assertEqual(report["target_count"], 1)
            self.assertEqual(
                [(row["source_path"], row["target_path"]) for row in report["references"]],
                [("consumer.md", "DEV/docs/superpowers/specs/old-spec.md")],
            )


if __name__ == "__main__":
    unittest.main()
