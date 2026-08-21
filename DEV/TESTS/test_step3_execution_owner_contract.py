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

    def test_resolution_and_continuation_reference_but_do_not_copy_procedure_state(self):
        resolution = {
            "root_command_id": "turn-000042-cmd-01",
            "initiating_command_id": "turn-000042-cmd-01",
            "activity_id": "activity.attack.basic",
            "catalog_context_fingerprint": "ctx",
            "procedure_id": "procedure-000001",
            "status": "AWAITING_REACTION",
            "next_segment_sequence": 2,
            "invocation_facts": [],
            "fixed_rng_results": [17],
            "prior_step_exports": {"attack_roll": 17},
            "child_resolution_ids": [],
        }
        validate("runtime-resolution-state.schema.json", resolution)
        continuation = {
            "generation": 1,
            "root_command_id": "turn-000042-cmd-01",
            "resolution_id": "resolution-0000001",
            "catalog_context_fingerprint": "ctx",
            "procedure_id": "procedure-000001",
            "safe_recompute_phase": "determine",
            "invocation_facts": [],
            "fixed_rng_results": [17],
            "prior_step_exports": {"attack_roll": 17},
            "committed_receipt_refs": ["resolution-0000001:segment:1"],
            "dependency_frontier_refs": ["actor-0001@12"],
            "expected_child_resolution_ids": [],
            "future_rng_frontier": "rng:42",
        }
        validate("runtime-continuation-state.schema.json", continuation)
        for schema_name, base in (
            ("runtime-resolution-state.schema.json", resolution),
            ("runtime-continuation-state.schema.json", continuation),
        ):
            for forbidden in ("procedure_resources", "resource_state_copy"):
                invalid = dict(base)
                invalid[forbidden] = {}
                with self.assertRaises(ValidationError):
                    validate(schema_name, invalid)

    def test_continuation_rejects_derived_cache_authority(self):
        base = {
            "generation": 1, "root_command_id": "cmd", "resolution_id": "resolution-1",
            "catalog_context_fingerprint": "ctx", "safe_recompute_phase": "effect",
            "invocation_facts": [], "fixed_rng_results": [], "prior_step_exports": {},
            "committed_receipt_refs": [], "dependency_frontier_refs": [],
            "expected_child_resolution_ids": [], "future_rng_frontier": "rng:0",
        }
        for forbidden in ("mechanical_context", "temporal_agenda", "prospective_deltas", "condition_index"):
            invalid = dict(base)
            invalid[forbidden] = {}
            with self.assertRaises(ValidationError):
                validate("runtime-continuation-state.schema.json", invalid)

    def test_child_resolution_without_initiating_command_needs_causal_key(self):
        child = {
            "root_command_id": "cmd", "activity_id": "activity.followup",
            "catalog_context_fingerprint": "ctx", "status": "PENDING",
            "next_segment_sequence": 1, "invocation_facts": [],
            "fixed_rng_results": [], "prior_step_exports": {}, "child_resolution_ids": [],
            "causal_invocation_key": "event-1:binding-1",
        }
        validate("runtime-resolution-state.schema.json", child)
        child.pop("causal_invocation_key")
        with self.assertRaises(ValidationError):
            validate("runtime-resolution-state.schema.json", child)


if __name__ == "__main__":
    unittest.main()
