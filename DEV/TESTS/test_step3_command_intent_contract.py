import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def schema(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def registry():
    result = Registry()
    for path in SCHEMAS.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in data:
            result = result.with_resource(data["$id"], Resource.from_contents(data))
    return result


def validate(name, value):
    Draft202012Validator(schema(name), registry=registry()).validate(value)


class Step3CommandIntentContractTest(unittest.TestCase):
    def test_intent_plan_allows_partial_completion_without_transaction_authority(self):
        value = {
            "interaction_id": "turn-000042",
            "clauses": [
                {"clause_id": "c1", "order": 1, "mapping_outcome": "exact", "execution_state": "intent.executed"},
                {"clause_id": "c2", "order": 2, "mapping_outcome": "exact", "execution_state": "intent.executed"},
                {"clause_id": "c3", "order": 3, "mapping_outcome": "exact", "execution_state": "intent.failed"},
            ],
        }
        validate("runtime-intent-plan-state.schema.json", value)
        for forbidden in ("world_delta", "rng_state", "procedure_resources", "transaction_state"):
            invalid = dict(value)
            invalid[forbidden] = {}
            with self.assertRaises(ValidationError):
                validate("runtime-intent-plan-state.schema.json", invalid)

    def test_action_command_links_resolution_and_closes_only_without_pending_children(self):
        value = {
            "interaction_id": "turn-000042",
            "intent_plan_id": "turn-000042-plan",
            "clause_id": "c1",
            "command_kind": "action",
            "catalog_context_fingerprint": "sha256:catalog-context-A",
            "input_fingerprint": "sha256:command-input-A",
            "disposition": "command.accepted",
            "invocation_facts": [],
            "root_resolution_id": "resolution-0000001",
            "pending_child_invocations": [],
        }
        validate("runtime-command-state.schema.json", value)
        settled = dict(value, disposition="command.settled")
        settled["pending_child_invocations"] = [{
            "firing_key": "f1", "root_command_id": "turn-000042-cmd-01",
            "activity_id": "activity.followup", "trigger_ref": "event-00000001",
            "reason": "mandatory_followup",
        }]
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", settled)

    def test_action_and_transition_paths_do_not_collapse(self):
        action = {
            "interaction_id": "turn-1", "intent_plan_id": "turn-1-plan", "clause_id": "c1",
            "command_kind": "action", "catalog_context_fingerprint": "ctx", "input_fingerprint": "fp",
            "disposition": "command.accepted", "invocation_facts": [], "root_resolution_id": "resolution-1",
            "pending_child_invocations": [],
        }
        invalid_action = dict(action, transition_request={"transition_kind": "transition.location_change"})
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", invalid_action)
        transition = dict(action)
        transition.pop("root_resolution_id")
        transition["command_kind"] = "transition"
        transition["transition_request"] = {"transition_kind": "transition.location_change", "payload": {"target_id": "actor-1", "destination_id": "location-2"}}
        validate("runtime-command-state.schema.json", transition)
        invalid_transition = dict(transition, resolution_cursor="effect")
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", invalid_transition)


if __name__ == "__main__":
    unittest.main()
