from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEV = ROOT / "DEV"
LEDGER = DEV / "PRODUCT_OWNER_INPUT.md"
PROGRESS = DEV / "CURRENT_PROGRESS.md"
CREATOR_DECISION = (
    DEV
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-09-06-hdm-creator-login-continuity-owner-decision.md"
)


def _closed_wps(progress: str) -> set[int]:
    return {
        int(match.group(1))
        for match in re.finditer(r"(?m)^WP(\d+)_CLOSED:\s*YES\s*$", progress)
    }


def _active_pending_closed_routes(ledger: str, progress: str) -> list[str]:
    closed = _closed_wps(progress)
    bad: list[str] = []
    for line in ledger.splitlines():
        if not line.startswith("|"):
            continue
        if "ACTIVE" not in line and "PENDING" not in line:
            continue
        for match in re.finditer(r"\bWP-(\d+)\b", line):
            if int(match.group(1)) in closed and "DISTINCT OPEN ROUTE" not in line:
                bad.append(line)
    return bad


def _verbatim_block_after(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    first = text.index("```", start) + 3
    end = text.index("```", first)
    return text[first:end].strip("\n")


class ProductOwnerRoutingConsistencyTests(unittest.TestCase):
    def test_active_or_pending_route_does_not_target_closed_wp_without_explicit_distinct_route(self):
        ledger = LEDGER.read_text(encoding="utf-8")
        progress = PROGRESS.read_text(encoding="utf-8")
        self.assertEqual(_active_pending_closed_routes(ledger, progress), [])

    def test_completed_repair_is_not_projected_as_still_in_progress(self):
        ledger = LEDGER.read_text(encoding="utf-8")
        progress = PROGRESS.read_text(encoding="utf-8")
        if "WHOLE_PROJECT_AUDIT_REPAIR_COMPLETE: YES" in progress:
            self.assertNotIn(
                "WHOLE_PROJECT_AUDIT_REPAIR: EXECUTION / VERIFICATION IN PROGRESS",
                ledger,
            )
            self.assertIn("WHOLE_PROJECT_AUDIT_REPAIR: COMPLETE", ledger)

    def test_po004_is_closed_against_final_wp20_architecture(self):
        src = LEDGER.read_text(encoding="utf-8")
        self.assertIn("| `PO-004` | COMPATIBILITY POLICY | INCORPORATED |", src)
        self.assertIn("WP-20 final Senior PASS", src)
        self.assertNotIn("WP-20 STEP-1 CONSUMER ACTIVE/PENDING", src)

    def test_creator_login_decision_is_captured_verbatim_in_ledger(self):
        ledger = LEDGER.read_text(encoding="utf-8")
        decision = CREATOR_DECISION.read_text(encoding="utf-8")
        decision_block = _verbatim_block_after(
            decision, "## Product Owner input — VERBATIM / IMMUTABLE"
        )
        self.assertIn(decision_block, ledger)
        self.assertIn("## PO-005 — Creator-login continuity and takeover prevention", ledger)
        self.assertIn("2026-09-06-hdm-creator-login-continuity-owner-decision.md", ledger)

    def test_creator_login_decision_remains_fail_closed_and_not_reopened(self):
        src = LEDGER.read_text(encoding="utf-8")
        self.assertIn("PO-005: INCORPORATED", src)
        self.assertIn("AUTOMATIC LOGIN-RENAME CONTINUITY: NOT SUPPORTED", src)
        self.assertIn("NEEDS_PO: NONE", src)


if __name__ == "__main__":
    unittest.main()
