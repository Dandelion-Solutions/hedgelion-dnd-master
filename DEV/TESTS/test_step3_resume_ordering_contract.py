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


def base_continuation():
    return {
        "generation": 2,
        "root_command_id": "cmd",
        "resolution_id": "resolution-1",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-1",
        "target_ids": ["actor-2"],
        "catalog_context_fingerprint": "ctx",
        "execution_cursor": "step.attack.resolve",
        "safe_recompute_phase": "determine",
        "invocation_facts": [],
        "fixed_rng_results": [{
            "roll_id": "roll.attack.1",
            "expression": "1d20",
            "raw_values": [17],
            "source_kind": "rng.system",
        }],
        "prior_step_exports": {},
        "committed_segment_refs": ["resolution-1:segment:1"],
        "dependency_frontier_refs": ["actor-1@2"],
        "expected_child_resolution_ids": [],
        "future_rng_frontier": "rng:4",
    }


class Step3ResumeOrderingContractTest(unittest.TestCase):
    def test_reaction_offer_is_bounded_and_identified(self):
        value = base_continuation()
        value["pending_response"] = {
            "kind": "reaction",
            "offer_id": "offer-7",
            "responder_id": "actor-2",
            "candidate_activity_ids": ["activity.shield"],
        }
        validate("runtime-continuation-state.schema.json", value)
        invalid = base_continuation()
        invalid["pending_response"] = {
            "kind": "reaction", "offer_id": "offer-7", "responder_id": "actor-2",
            "candidate_activity_ids": [],
        }
        with self.assertRaises(ValidationError):
            validate("runtime-continuation-state.schema.json", invalid)

    def test_choice_offer_is_bounded(self):
        value = base_continuation()
        value["pending_response"] = {
            "kind": "choice", "offer_id": "choice-1", "responder_id": "actor-1",
            "option_ids": ["option.a", "option.b"],
        }
        validate("runtime-continuation-state.schema.json", value)

    def test_unconsumed_advancement_is_positive_and_explicit(self):
        value = base_continuation()
        value["unconsumed_advancement"] = {"amount": 10, "unit_id": "unit.minute", "context_id": "scene-1"}
        validate("runtime-continuation-state.schema.json", value)
        invalid = dict(value)
        invalid["unconsumed_advancement"] = {"amount": -1, "unit_id": "unit.minute", "context_id": "scene-1"}
        with self.assertRaises(ValidationError):
            validate("runtime-continuation-state.schema.json", invalid)

    def test_resume_keeps_fixed_rng_and_rejects_old_prospective_state(self):
        value = base_continuation()
        validate("runtime-continuation-state.schema.json", value)
        invalid = dict(value, prospective_delta={"hp": -3})
        with self.assertRaises(ValidationError):
            validate("runtime-continuation-state.schema.json", invalid)

    def test_failure_code_cannot_masquerade_as_completed_receipt(self):
        invalid = {
            "execution_owner_id": "resolution-1", "segment_refs": [], "status": "COMPLETED",
            "event_ids": [], "exports": {}, "pending_child_refs": [],
            "failure_code": "failure.order_adjudication_required",
        }
        with self.assertRaises(ValidationError):
            validate("resolution-receipt.schema.json", invalid)
        valid = dict(invalid, status="FAILED")
        validate("resolution-receipt.schema.json", valid)


if __name__ == "__main__":
    unittest.main()
