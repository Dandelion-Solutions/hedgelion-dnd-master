import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def load(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def registry():
    result = Registry()
    for path in SCHEMAS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in data:
            result = result.with_resource(data["$id"], Resource.from_contents(data))
    return result


def validate(name, value):
    Draft202012Validator(load(name), registry=registry()).validate(value)


def roll(value=17):
    return {
        "roll_id": "roll.attack.1",
        "expression": "1d20",
        "raw_values": [value],
        "source_kind": "rng.system",
    }


def resolution():
    return {
        "root_command_id": "turn-000042-cmd-01",
        "initiating_command_id": "turn-000042-cmd-01",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-0001",
        "target_ids": ["actor-0002"],
        "catalog_context_fingerprint": "ctx",
        "procedure_id": "procedure-000001",
        "status": "AWAITING_REACTION",
        "next_segment_sequence": 2,
        "invocation_facts": [],
        "fixed_rng_results": [roll()],
        "prior_step_exports": {"attack_roll": 17},
        "child_resolution_ids": [],
        "segments": [{
            "segment_sequence": 1,
            "commit_state": "committed",
            "event_ids": ["event-00000001"],
            "pending_child_invocations": [],
            "receipt_exports": {"attack_roll": 17},
            "affected_revision_refs": [],
        }],
    }


def continuation():
    return {
        "generation": 1,
        "root_command_id": "turn-000042-cmd-01",
        "resolution_id": "resolution-0000001",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-0001",
        "target_ids": ["actor-0002"],
        "catalog_context_fingerprint": "ctx",
        "procedure_id": "procedure-000001",
        "execution_cursor": "step.attack.resolve",
        "safe_recompute_phase": "determine",
        "invocation_facts": [],
        "fixed_rng_results": [roll()],
        "prior_step_exports": {"attack_roll": 17},
        "committed_segment_refs": ["resolution-0000001:segment:1"],
        "dependency_frontier_refs": ["actor-0001@12"],
        "expected_child_resolution_ids": [],
        "future_rng_frontier": "rng:42",
    }


class Step3ExecutionOwnerContractTest(unittest.TestCase):
    def test_procedure_is_sole_spent_resource_owner(self):
        value = {
            "participant_resources": {
                "actor-0001": {
                    "resource.action": {"spent": 1},
                    "resource.reaction": {"spent": 0},
                }
            }
        }
        validate("runtime-procedure-state.schema.json", value)
        invalid = {
            "participant_resources": {
                "actor-0001": {"resource.action": {"spent": 1, "capacity": 2}}
            }
        }
        with self.assertRaises(ValidationError):
            validate("runtime-procedure-state.schema.json", invalid)

    def test_resolution_owns_bindings_segments_and_fixed_rng_without_copying_procedure_state(self):
        value = resolution()
        validate("runtime-resolution-state.schema.json", value)
        for forbidden in ("procedure_resources", "resource_state_copy"):
            invalid = dict(value)
            invalid[forbidden] = {}
            with self.assertRaises(ValidationError):
                validate("runtime-resolution-state.schema.json", invalid)

    def test_continuation_references_committed_segments_and_copies_no_procedure_or_derived_state(self):
        value = continuation()
        validate("runtime-continuation-state.schema.json", value)
        self.assertNotIn("committed_receipt_refs", value)
        for forbidden in (
            "procedure_resources", "resource_state_copy", "mechanical_context",
            "temporal_agenda", "prospective_deltas", "condition_index",
        ):
            invalid = dict(value)
            invalid[forbidden] = {}
            with self.assertRaises(ValidationError):
                validate("runtime-continuation-state.schema.json", invalid)

    def test_child_resolution_without_initiating_command_needs_causal_key(self):
        child = {
            "root_command_id": "cmd",
            "activity_id": "activity.followup",
            "actor_id": "actor-0001",
            "catalog_context_fingerprint": "ctx",
            "status": "PENDING",
            "next_segment_sequence": 1,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
            "causal_invocation_key": "event-1:binding-1",
        }
        validate("runtime-resolution-state.schema.json", child)
        child.pop("causal_invocation_key")
        with self.assertRaises(ValidationError):
            validate("runtime-resolution-state.schema.json", child)

    def test_fixed_rng_result_identity_is_not_an_untyped_scalar(self):
        value = resolution()
        value["fixed_rng_results"] = [17]
        with self.assertRaises(ValidationError):
            validate("runtime-resolution-state.schema.json", value)


if __name__ == "__main__":
    unittest.main()
