import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
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


class Step2ResourceStorageContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()
        cls.validator = Draft202012Validator(
            cls.schemas["catalog-definition.schema.json"],
            registry=cls.registry,
        )

    def definition(self, lifetime_owner, state_model, recovery=None):
        data = {
            "mechanic_id": "resource.bounded_pool",
            "lifetime_owner": lifetime_owner,
            "state_model": state_model,
        }
        if recovery is not None:
            data["recovery"] = recovery
        return {
            "id": "resource.example",
            "kind": "definition.resource",
            "name": {"en": "Example Resource"},
            "data": data,
        }

    def test_persistent_actor_and_asset_resources_use_current_state(self):
        self.validator.validate(self.definition("actor", "current"))
        self.validator.validate(self.definition("asset", "current"))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("actor", "spent"))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("asset", "spent"))

    def test_procedure_resources_use_spent_state(self):
        self.validator.validate(self.definition("procedure", "spent"))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("procedure", "current"))

    def test_recovery_operations_match_storage_model(self):
        self.validator.validate(self.definition("procedure", "spent", [{
            "boundary_id": "boundary.turn_start",
            "operation_id": "resource_recovery.reset_spent",
        }]))
        self.validator.validate(self.definition("actor", "current", [{
            "boundary_id": "boundary.long_rest_complete",
            "operation_id": "resource_recovery.restore_to_capacity",
        }]))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("actor", "current", [{
                "boundary_id": "boundary.long_rest_complete",
                "operation_id": "resource_recovery.reset_spent",
            }]))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("procedure", "spent", [{
                "boundary_id": "boundary.turn_start",
                "operation_id": "resource_recovery.restore_to_capacity",
            }]))

    def test_after_recovery_is_metric_only_not_a_second_boundary_encoding(self):
        self.validator.validate(self.definition("actor", "current", [{
            "after": {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.hour"},
            "operation_id": "resource_recovery.restore_amount",
            "amount": 1,
        }]))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("actor", "current", [{
                "after": {
                    "kind_id": "duration.boundary",
                    "boundary_id": "boundary.long_rest_complete",
                },
                "operation_id": "resource_recovery.restore_to_capacity",
            }]))
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("actor", "current", [{
                "after": {"kind_id": "duration.permanent"},
                "operation_id": "resource_recovery.restore_to_capacity",
            }]))

    def test_current_resource_has_at_most_one_metric_delay_recovery_policy(self):
        one_metric_plus_boundaries = [
            {
                "after": {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.hour"},
                "operation_id": "resource_recovery.restore_amount",
                "amount": 1,
            },
            {
                "boundary_id": "boundary.long_rest_complete",
                "operation_id": "resource_recovery.restore_to_capacity",
            },
        ]
        self.validator.validate(self.definition("actor", "current", one_metric_plus_boundaries))

        two_metric = [
            {
                "after": {"kind_id": "duration.metric", "amount": 1, "unit_id": "unit.hour"},
                "operation_id": "resource_recovery.restore_amount",
                "amount": 1,
            },
            {
                "after": {"kind_id": "duration.metric", "amount": 8, "unit_id": "unit.hour"},
                "operation_id": "resource_recovery.restore_to_capacity",
            },
        ]
        with self.assertRaises(ValidationError):
            self.validator.validate(self.definition("asset", "current", two_metric))


if __name__ == "__main__":
    unittest.main()
