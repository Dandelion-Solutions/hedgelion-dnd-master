"""Structural Step-2 schema examples. These tests do not grant selector/operation selectability; catalog-aware legality is owned by the resolved mechanical surfaces."""

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


class Step2MechanicalExamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.schemas = build_registry()

    def validator(self, schema_name):
        return Draft202012Validator(self.schemas[schema_name], registry=self.registry)

    def validate_definition(self, definition):
        self.validator("catalog-definition.schema.json").validate(definition)

    def test_presence_condition_can_emit_aggregate_once_rule(self):
        self.validate_definition({
            "id": "condition.poisoned",
            "kind": "definition.condition",
            "name": {"en": "Poisoned"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.presence",
                "intrinsic_mechanics": [{
                    "scope_id": "condition_rule_scope.aggregate_once",
                    "rule_element": {
                        "operation_id": "rule.grant_disadvantage",
                        "selector": "attack.roll",
                        "value": True,
                    },
                }],
            },
        })

    def test_presence_condition_can_bind_rule_per_effective_application(self):
        self.validate_definition({
            "id": "condition.frightened",
            "kind": "definition.condition",
            "name": {"en": "Frightened"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.presence",
                "intrinsic_mechanics": [{
                    "scope_id": "condition_rule_scope.per_effective_application",
                    "rule_element": {
                        "operation_id": "rule.restrict_activity",
                        "selector": "activity.availability",
                        "value": {"relative_to": "condition_source"},
                    },
                }],
            },
        })

    def test_one_condition_can_mix_intrinsic_rule_scopes(self):
        self.validate_definition({
            "id": "condition.grappled",
            "kind": "definition.condition",
            "name": {"en": "Grappled"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.presence",
                "intrinsic_mechanics": [
                    {
                        "scope_id": "condition_rule_scope.aggregate_once",
                        "rule_element": {
                            "operation_id": "rule.override",
                            "selector": "movement.speed",
                            "value": 0,
                        },
                    },
                    {
                        "scope_id": "condition_rule_scope.per_effective_application",
                        "rule_element": {
                            "operation_id": "rule.restrict_activity",
                            "selector": "activity.availability",
                            "value": {"relative_to": "condition_source"},
                        },
                    },
                ],
            },
        })

    def test_exhaustion_uses_cumulative_units_without_stack_field(self):
        self.validate_definition({
            "id": "condition.exhaustion",
            "kind": "definition.condition",
            "name": {"en": "Exhaustion"},
            "data": {
                "aggregation_policy_id": "condition_aggregation.cumulative_units",
                "value_constraints": {"minimum": 0, "maximum": 6},
                "intrinsic_mechanics": [
                    {
                        "scope_id": "condition_rule_scope.per_effective_application",
                        "rule_element": {
                            "operation_id": "rule.add_flat",
                            "selector": "test.roll",
                            "value": -2,
                        },
                    },
                    {
                        "scope_id": "condition_rule_scope.per_effective_application",
                        "rule_element": {
                            "operation_id": "rule.add_flat",
                            "selector": "movement.speed",
                            "value": -5,
                        },
                    },
                ],
            },
        })

    def test_effect_definition_rejects_generic_stacking(self):
        with self.assertRaises(ValidationError):
            self.validate_definition({
                "id": "effect.example",
                "kind": "definition.effect",
                "name": {"en": "Example"},
                "data": {"stacking": "stack.stack"},
            })

    def test_rest_policy_rejects_recovery_steps(self):
        with self.assertRaises(ValidationError):
            self.validate_definition({
                "id": "rest.long",
                "kind": "definition.rest_policy",
                "name": {"en": "Long Rest"},
                "data": {
                    "duration": {"kind_id": "duration.metric", "amount": 8, "unit_id": "unit.hour"},
                    "completion_boundary_id": "boundary.long_rest_complete",
                    "recovery_steps": [],
                },
            })

    def test_typed_accessor_predicate_accepts_condition_read_and_rejects_old_ref(self):
        validator = self.validator("mechanical-predicate.schema.json")
        validator.validate({
            "compare": {
                "left": {
                    "accessor_id": "condition.present",
                    "subject": "target",
                    "condition_id": "condition.poisoned",
                },
                "operator": "eq",
                "right": True,
            }
        })
        with self.assertRaises(ValidationError):
            validator.validate({
                "compare": {
                    "left": {"ref": "target.conditions.poisoned"},
                    "operator": "eq",
                    "right": True,
                }
            })

    def test_world_effect_is_single_target_and_can_own_temporal_binding(self):
        validator = self.validator("world-record.schema.json")
        validator.validate({
            "id": "effect-00001",
            "kind": "world.effect",
            "definition_id": "condition.frightened",
            "state": {
                "target_id": "actor-00001",
                "source_id": "actor-00002",
                "temporal_binding": {
                    "basis_id": "temporal.procedure_boundary",
                    "boundary_id": "boundary.turn_end",
                    "procedure_id": "encounter-00001",
                    "anchor_id": "turn-00017",
                    "subject_id": "actor-00001",
                },
                "lifecycle": {"state_id": "effect_lifecycle.active"},
            },
        })
        with self.assertRaises(ValidationError):
            validator.validate({
                "id": "effect-00002",
                "kind": "world.effect",
                "definition_id": "condition.poisoned",
                "state": {
                    "target_ids": ["actor-00001", "actor-00002"],
                    "status": "active",
                    "stacks": 2,
                },
            })

    def test_world_effect_terminal_reason_is_registered(self):
        validator = self.validator("world-record.schema.json")
        validator.validate({
            "id": "effect-00003",
            "kind": "world.effect",
            "definition_id": "condition.poisoned",
            "state": {
                "target_id": "actor-00001",
                "lifecycle": {
                    "state_id": "effect_lifecycle.terminal",
                    "terminal_reason_id": "effect_end.removed",
                },
            },
        })
        with self.assertRaises(ValidationError):
            validator.validate({
                "id": "effect-00004",
                "kind": "world.effect",
                "definition_id": "condition.poisoned",
                "state": {
                    "target_id": "actor-00001",
                    "lifecycle": {
                        "state_id": "effect_lifecycle.terminal",
                        "terminal_reason_id": "effect_end.llm_invented",
                    },
                },
            })

    def test_lifestate_progress_is_state_local(self):
        validator = self.validator("world-actor-state.schema.json")
        validator.validate({
            "name": {"en": "Aria"},
            "hp": {"current": 0, "maximum_base": 18},
            "life_state_id": "life.dying",
            "life_state_progress": {"death_saves": {"successes": 2, "failures": 1}},
        })
        validator.validate({
            "name": {"en": "Aria"},
            "hp": {"current": 0, "maximum_base": 18},
            "life_state_id": "life.stable",
            "life_state_progress": {
                "recovery_binding": {
                    "basis_id": "temporal.metric_deadline",
                    "context_id": "scene-00001",
                    "anchor_value": 10,
                    "deadline_value": 20,
                    "unit_id": "unit.minute",
                }
            },
        })
        with self.assertRaises(ValidationError):
            validator.validate({
                "name": {"en": "Aria"},
                "life_state_id": "life.active",
                "life_state_progress": {"death_saves": {"successes": 0, "failures": 0}},
            })


if __name__ == "__main__":
    unittest.main()
