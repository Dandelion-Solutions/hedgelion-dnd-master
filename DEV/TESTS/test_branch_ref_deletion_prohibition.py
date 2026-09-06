from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNER_DECISION = (
    ROOT
    / "DEV"
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md"
)
AGENTS = ROOT / "AGENTS.md"
PERSISTENCE = ROOT / "GAME" / "CORE" / "PERSISTENCE.md"
LIVE_SCENE = ROOT / "GAME" / "CORE" / "LIVE_SCENE.md"
PO_LEDGER = ROOT / "DEV" / "PRODUCT_OWNER_INPUT.md"


class BranchRefDeletionProhibitionTests(unittest.TestCase):
    def test_canonical_owner_prohibits_branch_ref_deletion(self):
        src = OWNER_DECISION.read_text(encoding="utf-8")
        self.assertIn("HDM NEVER DELETES A BRANCH OR REF", src)
        self.assertIn("There is no HDM `delete branch` / `delete ref` operation", src)
        self.assertIn("LAW 5.13-71     superseded", src)
        self.assertIn("SD-6 live-ref deletion capability` is superseded", src)

    def test_dev_and_runtime_core_project_the_absolute_prohibition(self):
        agents = AGENTS.read_text(encoding="utf-8")
        persistence = PERSISTENCE.read_text(encoding="utf-8")
        live_scene = LIVE_SCENE.read_text(encoding="utf-8")
        ledger = PO_LEDGER.read_text(encoding="utf-8")

        self.assertIn("Branch/ref deletion is **prohibited absolutely**", agents)
        self.assertNotIn(
            "If the connected GitHub interface does not expose remote ref deletion",
            agents,
        )
        self.assertIn("## Branch/ref deletion prohibition", persistence)
        self.assertIn("Never invoke a branch/ref-delete operation", persistence)
        self.assertIn("## Retained live-branch policy", live_scene)
        self.assertIn("Never delete a live branch/ref", live_scene)
        self.assertNotIn(
            "may be deleted/cleaned up when ref deletion is available", live_scene
        )
        self.assertIn("## PO-006 — Branch/ref deletion prohibition", ledger)
        self.assertIn("BRANCH/REF DELETION: PROHIBITED", ledger)

    def test_executable_hdm_surfaces_contain_no_branch_delete_invocation(self):
        patterns = {
            "delete_ref_call": re.compile(r"\bdelete_ref\s*\("),
            "delete_branch_call": re.compile(r"\bdelete_branch\s*\("),
            "git_push_delete": re.compile(r"git\s+push\b[^\n]*--delete"),
            "git_branch_delete": re.compile(r"git\s+branch\s+-(?:d|D)\b"),
        }

        candidates: list[Path] = []
        candidates.extend((ROOT / "GAME").rglob("*.py"))
        candidates.extend((ROOT / "DEV" / "TOOLS").rglob("*.py"))
        workflow_root = ROOT / ".github" / "workflows"
        if workflow_root.exists():
            candidates.extend(workflow_root.glob("*.yml"))
            candidates.extend(workflow_root.glob("*.yaml"))

        violations: list[str] = []
        for path in sorted(set(candidates)):
            text = path.read_text(encoding="utf-8")
            for name, pattern in patterns.items():
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)}: {name}")

        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
