import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from catalog_admission import load_catalog_admission_ledger  # noqa: E402

CATALOG = ROOT / "DEV" / "CATALOG"
REQUIRED = {"attack.roll", "save.roll", "check.roll", "defense.armor_class", "damage.received", "healing.received", "spell.dc"}
REQUIRED_OPERATIONS = {"rule.grant_advantage"}


class MvpSelectorActivationTests(unittest.TestCase):
    def test_mvp_primitive_selector_dependencies_are_complete_and_admitted(self):
        surfaces = json.loads((CATALOG / "mechanical-surfaces.json").read_text(encoding="utf-8"))
        ledger = load_catalog_admission_ledger(ROOT)
        selectors = surfaces["selectors"]
        self.assertLessEqual(REQUIRED, set(selectors))
        for selector_id in REQUIRED:
            row = selectors[selector_id]
            self.assertEqual(row["resolution_owner"], "SELECTOR_METADATA")
            self.assertEqual(row["allowed_input_classes"], ["ENGINE_STATE"])
            self.assertEqual(row["trace_policy"], "RETAIN_ACCEPTED_REJECTED_PROVENANCE")
        admissions = {row["id"]: row for row in ledger["entries"] if row["id"] in REQUIRED}
        self.assertEqual(set(admissions), REQUIRED)
        for row in admissions.values():
            self.assertEqual(row["realization_state"], "COMPLETE")
            self.assertEqual(row["admission_disposition"], "ACTIVE_ADMITTED")
            self.assertEqual(row["downstream_owner"], "S6D-07")
        operation_admissions = {row["id"]: row for row in ledger["entries"] if row["id"] in REQUIRED_OPERATIONS}
        self.assertEqual(set(operation_admissions), REQUIRED_OPERATIONS)
        for row in operation_admissions.values():
            self.assertEqual(row["realization_state"], "COMPLETE")
            self.assertEqual(row["admission_disposition"], "ACTIVE_ADMITTED")
            self.assertEqual(row["downstream_owner"], "S6D-07")
        self.assertIn("rule.grant_advantage", selectors["attack.roll"]["allowed_operations"])
        self.assertIs(selectors["attack.roll"]["operation_contracts"]["rule.grant_advantage"]["fixed_value"], True)


if __name__ == "__main__":
    unittest.main()
