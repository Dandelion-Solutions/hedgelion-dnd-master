import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SURFACES = ROOT / "DEV" / "CATALOG" / "mechanical-surfaces.json"


class Step2ConditionApplicabilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SURFACES.open("r", encoding="utf-8") as handle:
            cls.surfaces = json.load(handle)

    def test_condition_applicability_has_only_proven_immunity_operation(self):
        selector = self.surfaces["selectors"]["condition.applicability"]
        self.assertEqual(selector["allowed_operations"], ["rule.immunity"])
        self.assertEqual(
            selector["operation_contracts"],
            {"rule.immunity": {"fixed_value": True}},
        )


if __name__ == "__main__":
    unittest.main()
