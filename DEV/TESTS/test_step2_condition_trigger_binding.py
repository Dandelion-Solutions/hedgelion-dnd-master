import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
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


class Step2ConditionTriggerBindingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()

    def test_per_effective_application_trigger_can_bind_condition_source_and_target(self):
        validator = Draft202012Validator(
            self.schemas["catalog-definition.schema.json"],
            registry=self.registry,
        )
        validator.validate({
            "id": "condition.example_relational",
            "kind": "definition.condition",
            "name": {"en": "Example Relational Condition"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.presence",
                "intrinsic_mechanics": [{
                    "scope_id": "condition_rule_scope.per_effective_application",
                    "trigger_binding": {
                        "on": "signal.effect.end",
                        "activity_id": "activity.example_followup",
                        "mode": "schedule",
                        "actor": "condition.source",
                        "targets": "condition.target"
                    }
                }]
            }
        })


if __name__ == "__main__":
    unittest.main()
