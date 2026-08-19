import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_registry():
    registry = Registry()
    schemas = {}
    for path in SCHEMAS.glob("*.schema.json"):
        schema = load_json(path)
        schemas[path.name] = schema
        schema_id = schema.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry, schemas


class Step2ConditionBoundaryResponseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()
        cls.core = load_json(CATALOG / "core-catalog.json")

    def test_exhaustion_can_own_long_rest_remove_one_response(self):
        self.assertEqual(
            self.core["registries"]["condition_boundary_response_operations"],
            ["condition_response.remove_count"],
        )
        validator = Draft202012Validator(
            self.schemas["catalog-definition.schema.json"],
            registry=self.registry,
        )
        validator.validate({
            "id": "condition.exhaustion",
            "kind": "definition.condition",
            "name": {"en": "Exhaustion"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.cumulative_units",
                "value_constraints": {"minimum": 0, "maximum": 6},
                "automatic_boundary_responses": [{
                    "boundary_id": "boundary.long_rest_complete",
                    "operation_id": "condition_response.remove_count",
                    "count": 1,
                }],
            },
        })


if __name__ == "__main__":
    unittest.main()
