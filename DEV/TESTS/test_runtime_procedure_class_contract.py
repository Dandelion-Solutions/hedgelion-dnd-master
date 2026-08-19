import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class RuntimeProcedureClassContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.policies = load_json(CATALOG / "identifier-policies.json")
        cls.policy_schema = load_json(SCHEMAS / "identifier-policies.schema.json")

    def test_procedure_is_independent_runtime_record_not_world_or_protocol_kind(self):
        registries = self.core["registries"]
        self.assertIn("runtime.procedure", registries["runtime_record_kinds"])
        self.assertNotIn("world.procedure", registries["world_record_kinds"])
        self.assertNotIn("value.procedure", registries["protocol_value_kinds"])

    def test_procedure_has_campaign_stable_operational_identity(self):
        policy = self.policies["runtime"]["runtime.procedure"]
        self.assertEqual(policy["strategy"], "sequential")
        self.assertEqual(policy["prefix"], "procedure")
        self.assertEqual(policy["scope"], "campaign")
        self.assertGreaterEqual(policy["minimum_width"], 6)

    def test_identifier_policy_schema_accepts_runtime_procedure(self):
        Draft202012Validator(self.policy_schema).validate(self.policies)
        runtime_schema = self.policy_schema["properties"]["runtime"]
        self.assertIn("runtime.procedure", runtime_schema["required"])
        self.assertIn("runtime.procedure", runtime_schema["properties"])


if __name__ == "__main__":
    unittest.main()
