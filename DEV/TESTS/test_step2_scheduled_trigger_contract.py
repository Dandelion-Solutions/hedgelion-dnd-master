import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
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


class Step2ScheduledTriggerContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()
        cls.definition_validator = Draft202012Validator(
            cls.schemas["catalog-definition.schema.json"],
            registry=cls.registry,
        )
        cls.world_validator = Draft202012Validator(
            cls.schemas["world-record.schema.json"],
            registry=cls.registry,
        )
        cls.entity_structures = load_json(CATALOG / "entity-structures.json")
        cls.core = load_json(CATALOG / "core-catalog.json")

    def periodic_effect_definition(self, after=None):
        if after is None:
            after = {"kind_id": "duration.metric", "amount": 24, "unit_id": "unit.hour"}
        return {
            "id": "effect.periodic_disease",
            "kind": "definition.effect",
            "name": {"en": "Periodic Disease"},
            "data": {
                "duration": {"kind_id": "duration.metric", "amount": 3, "unit_id": "unit.day"},
                "scheduled_triggers": {
                    "daily_save": {
                        "after": after,
                        "activity_id": "srd.activity.disease_save",
                    }
                },
            },
        }

    def active_effect(self):
        return {
            "id": "effect-00001",
            "kind": "world.effect",
            "definition_id": "effect.periodic_disease",
            "state": {
                "target_id": "actor-00001",
                "temporal_binding": {
                    "basis_id": "temporal.metric_deadline",
                    "context_id": "scene-00001",
                    "anchor_value": 0,
                    "deadline_value": 72,
                    "unit_id": "unit.hour",
                },
                "scheduled_trigger_state": {
                    "daily_save": {
                        "basis_id": "temporal.metric_deadline",
                        "context_id": "scene-00001",
                        "anchor_value": 0,
                        "deadline_value": 24,
                        "unit_id": "unit.hour",
                    }
                },
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        }

    def test_definition_accepts_stable_owner_local_metric_trigger(self):
        self.definition_validator.validate(self.periodic_effect_definition())

    def test_scheduled_trigger_delay_is_metric_not_duplicate_boundary_encoding(self):
        with self.assertRaises(ValidationError):
            self.definition_validator.validate(self.periodic_effect_definition({
                "kind_id": "duration.boundary",
                "boundary_id": "boundary.dawn",
            }))

    def test_active_effect_can_own_intrinsic_lifetime_and_independent_next_due_binding(self):
        self.world_validator.validate(self.active_effect())

    def test_terminal_effect_cannot_keep_armed_scheduled_trigger_state(self):
        record = self.active_effect()
        record["state"]["lifecycle"] = {
            "state_id": "effect_lifecycle.terminal",
            "terminal_reason_id": "effect_end.removed",
        }
        with self.assertRaises(ValidationError):
            self.world_validator.validate(record)

    def test_inventory_exposes_owner_local_state_without_global_scheduler_kind(self):
        definition = self.entity_structures["definitions"]["definition.effect"]
        world_effect = self.entity_structures["world_records"]["world.effect"]
        self.assertIn("scheduled_triggers", set(definition["expected"]))
        self.assertIn("scheduled_trigger_state", set(world_effect["expected"]))
        self.assertNotIn("runtime.scheduled_job", self.core["registries"]["runtime_record_kinds"])
        self.assertNotIn("world.scheduled_job", self.core["registries"]["world_record_kinds"])


if __name__ == "__main__":
    unittest.main()
