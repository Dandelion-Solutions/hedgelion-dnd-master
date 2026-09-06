from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "DEV" / "docs" / "superpowers" / "specs"
AMENDMENT = SPECS / "2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md"
WP20 = SPECS / "2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md"


def _is_ancestor(ancestor: str, descendant: str, parent_of: dict[str, str | None]) -> bool:
    current: str | None = descendant
    seen: set[str] = set()
    while current is not None and current not in seen:
        if current == ancestor:
            return True
        seen.add(current)
        current = parent_of.get(current)
    return False


def _non_force_fast_forward_allowed(
    current_ref: str,
    candidate: str,
    parent_of: dict[str, str | None],
) -> bool:
    return _is_ancestor(current_ref, candidate, parent_of)


def _ambiguous_disposition(
    intended: str,
    current: str,
    parent_of: dict[str, str | None],
    *,
    current_closure_compatible: bool,
) -> str:
    if current == intended:
        return "CURRENT_CLOSURE_REQUIRED"
    if _is_ancestor(intended, current, parent_of):
        return (
            "LINEAGE_AND_CURRENT_CLOSURE_ACCEPTABLE"
            if current_closure_compatible
            else "REVALIDATION_REQUIRED"
        )
    return "NO_SUCCESS_INFERENCE"


class PublicationRefFenceContractTests(unittest.TestCase):
    def test_existing_ref_accepts_only_fast_forward_candidate(self):
        parents = {"H": None, "C": "H"}
        self.assertTrue(_non_force_fast_forward_allowed("H", "C", parents))

    def test_intervening_writer_rejects_stale_sibling(self):
        parents = {"H": None, "A": "H", "C": "H"}
        self.assertFalse(_non_force_fast_forward_allowed("A", "C", parents))

    def test_further_descendant_does_not_make_stale_sibling_valid(self):
        parents = {"H": None, "A": "H", "D": "A", "C": "H"}
        self.assertFalse(_non_force_fast_forward_allowed("D", "C", parents))

    def test_ambiguous_descendant_requires_current_closure_not_exact_ref_equality(self):
        parents = {"H": None, "C": "H", "D": "C"}
        self.assertEqual(
            _ambiguous_disposition(
                "C", "D", parents, current_closure_compatible=True
            ),
            "LINEAGE_AND_CURRENT_CLOSURE_ACCEPTABLE",
        )
        self.assertEqual(
            _ambiguous_disposition(
                "C", "D", parents, current_closure_compatible=False
            ),
            "REVALIDATION_REQUIRED",
        )

    def test_ambiguous_lineage_excluding_intended_gives_no_success_inference(self):
        parents = {"H": None, "A": "H", "C": "H"}
        self.assertEqual(
            _ambiguous_disposition(
                "C", "A", parents, current_closure_compatible=True
            ),
            "NO_SUCCESS_INFERENCE",
        )

    def test_rewind_is_not_an_admitted_non_force_movement(self):
        parents = {"H": None, "A": "H", "D": "A"}
        self.assertFalse(_non_force_fast_forward_allowed("D", "H", parents))
        self.assertFalse(_non_force_fast_forward_allowed("D", "A", parents))

    def test_repair_amendment_names_all_supported_ref_movement_classes(self):
        src = AMENDMENT.read_text(encoding="utf-8")
        for case_id in ("PCR-A1", "PCR-A2", "PCR-A3", "PCR-A4", "PCR-A5", "PCR-A6", "PCR-A7"):
            self.assertIn(case_id, src)
        self.assertIn("create-if-absent", src)
        self.assertIn("force=false", src)
        self.assertIn("NON_MONOTONIC_HISTORY", src)
        self.assertIn("C proven reachable ancestor of D", src)
        self.assertIn("current D supplies compatible current required closure", src)
        self.assertIn("does **not** expose a separate expected-old/current-ref SHA argument", src)

    def test_wp20_ambiguity_contract_preserves_lineage_current_closure(self):
        src = WP20.read_text(encoding="utf-8")
        self.assertIn("FINAL SENIOR REVIEW PASS", src)
        self.assertIn("C proven reachable ancestor of D", src)
        self.assertIn("compatible current required closure", src)
        self.assertNotIn("ref proves another current successor/head -> rejected/stale", src)


if __name__ == "__main__":
    unittest.main()
