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


class Step3ExecutionCatalogContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = load_json(CATALOG / "core-catalog.json")
        cls.schema = load_json(SCHEMAS / "core-catalog.schema.json")

    def test_step3_closed_vocabulary_is_registered(self):
        registries = self.core["registries"]
        self.assertEqual(
            registries["command_dispositions"],
            ["command.accepted", "command.settled"],
        )
        required_failures = {
            "failure.idempotency_conflict",
            "failure.hydration_required",
            "failure.missing_reference",
            "failure.catalog_context_incompatible",
            "failure.continuation_conflict",
            "failure.continuation_stale",
            "failure.dependency_cycle",
            "failure.transition_requires_procedure",
            "failure.order_adjudication_required",
            "failure.execution_limit",
            "failure.invocation_fact_missing",
            "failure.invocation_fact_unauthorized",
        }
        self.assertTrue(required_failures <= set(registries["execution_failure_codes"]))
        for kind in (
            "value.execution_segment",
            "value.pending_child_invocation",
            "value.invocation_fact",
            "value.boundary_occurrence",
        ):
            self.assertIn(kind, registries["protocol_value_kinds"])
        self.assertNotIn("runtime.execution_segment", registries["runtime_record_kinds"])
        self.assertNotIn("runtime.resolution_chain", registries["runtime_record_kinds"])

    def test_catalogs_move_as_one_version(self):
        versions = {
            load_json(CATALOG / name)["catalog_version"]
            for name in (
                "core-catalog.json",
                "entity-structures.json",
                "mechanical-surfaces.json",
                "identifier-policies.json",
            )
        }
        self.assertEqual(len(versions), 1)
        version = next(iter(versions))
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (1, 4, 0))

    def test_core_catalog_schema_accepts_updated_catalog(self):
        Draft202012Validator(self.schema).validate(self.core)


if __name__ == "__main__":
    unittest.main()
