import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load_json(name: str):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def registry():
    result = Registry()
    for path in SCHEMAS.glob("*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            result = result.with_resource(schema["$id"], Resource.from_contents(schema))
    return result


def validate(name: str, value):
    Draft202012Validator(load_json(name), registry=registry()).validate(value)


class Step3ExecutionValueSchemasTest(unittest.TestCase):
    def test_invocation_fact_requires_explicit_boolean_value(self):
        valid = {
            "fact_id": "fiction.target_visible",
            "value": False,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "interaction-000001:fact:1",
        }
        validate("invocation-fact.schema.json", valid)
        for invalid in (
            {"fact_id": "fiction.target_visible", "provenance_class": "INVOCATION_ADJUDICATED", "provenance_ref": "x"},
            {"fact_id": "fiction.target_visible", "value": None, "provenance_class": "INVOCATION_ADJUDICATED", "provenance_ref": "x"},
        ):
            with self.assertRaises(ValidationError):
                validate("invocation-fact.schema.json", invalid)

    def test_intent_guard_is_one_bounded_forward_reference(self):
        valid = {
            "clause_id": "clause-02",
            "order": 2,
            "mapping_outcome": "exact",
            "execution_state": "intent.ready",
            "guard": {
                "prior_clause_id": "clause-01",
                "source": "status",
                "operator": "eq",
                "literal": "intent.executed",
            },
        }
        validate("intent-clause.schema.json", valid)
        invalid = dict(valid)
        invalid["guard"] = {
            "prior_clause_ids": ["clause-01", "clause-00"],
            "expression": "a && b",
        }
        with self.assertRaises(ValidationError):
            validate("intent-clause.schema.json", invalid)

    def test_execution_segment_is_receipt_not_world_snapshot(self):
        valid = {
            "segment_sequence": 1,
            "commit_state": "committed",
            "event_ids": ["event-00000001"],
            "pending_child_invocations": [],
            "receipt_exports": {"hit": True},
            "affected_revision_refs": ["actor-0001@43"],
        }
        validate("execution-segment.schema.json", valid)
        invalid = dict(valid)
        invalid["world_state"] = {"actor-0001": {"hp": 3}}
        with self.assertRaises(ValidationError):
            validate("execution-segment.schema.json", invalid)

    def test_pending_child_requires_stable_causal_identity(self):
        valid = {
            "firing_key": "effect-000001:damage:event-00000001",
            "root_command_id": "turn-000042-cmd-01",
            "activity_id": "activity.concentration_save",
            "trigger_ref": "event-00000001",
            "reason": "mandatory_followup",
        }
        validate("pending-child-invocation.schema.json", valid)
        invalid = {"activity_id": "activity.concentration_save"}
        with self.assertRaises(ValidationError):
            validate("pending-child-invocation.schema.json", invalid)

    def test_boundary_occurrence_and_receipt_are_closed_values(self):
        validate(
            "boundary-occurrence.schema.json",
            {
                "boundary_id": "boundary.turn_end",
                "producer_id": "procedure-000001",
                "scope_subject_id": "actor-0001",
                "occurrence_key": "procedure-000001:turn:actor-0001:7:end",
                "causal_position": "resolution-0000001:segment:2",
            },
        )
        validate(
            "resolution-receipt.schema.json",
            {
                "execution_owner_id": "resolution-0000001",
                "segment_refs": ["resolution-0000001:segment:1"],
                "status": "COMPLETED",
                "event_ids": ["event-00000001"],
                "exports": {"hit": True},
                "pending_child_refs": [],
            },
        )


if __name__ == "__main__":
    unittest.main()
