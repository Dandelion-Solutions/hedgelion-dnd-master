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


def action_command():
    return {
        "interaction_id": "turn-000042",
        "intent_plan_id": "turn-000042-plan",
        "clause_id": "c1",
        "command_kind": "action",
        "catalog_context_fingerprint": "sha256:catalog-context-A",
        "input_fingerprint": "sha256:command-input-A",
        "disposition": "command.accepted",
        "invocation_facts": [],
        "action_request": {
            "activity_id": "activity.attack.basic",
            "actor_id": "actor-0001",
            "target_ids": ["actor-0002"],
        },
        "root_resolution_id": "resolution-0000001",
        "pending_child_invocations": [],
    }


def transition_command(disposition="command.accepted"):
    return {
        "interaction_id": "turn-1",
        "intent_plan_id": "turn-1-plan",
        "clause_id": "c1",
        "command_kind": "transition",
        "catalog_context_fingerprint": "ctx",
        "input_fingerprint": "fp",
        "disposition": disposition,
        "invocation_facts": [],
        "transition_request": {
            "transition_kind": "transition.location_change",
            "payload": {"target_id": "actor-1", "destination_id": "location-2"},
        },
        "pending_child_invocations": [],
    }


def committed_transition_segment(pending=None):
    return {
        "segment_sequence": 1,
        "commit_state": "committed",
        "resulting_execution_state": "COMPLETED",
        "event_ids": ["event-00000001"],
        "pending_child_invocations": list(pending or []),
        "receipt_exports": {},
        "affected_revision_refs": ["actor-1@2"],
    }


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

    def test_action_command_links_normalized_request_and_resolution(self):
        value = action_command()
        validate("runtime-command-state.schema.json", value)
        missing_request = dict(value)
        missing_request.pop("action_request")
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", missing_request)

    def test_command_closes_only_without_pending_children(self):
        settled = dict(action_command(), disposition="command.settled")
        settled["pending_child_invocations"] = [{
            "firing_key": "f1", "root_command_id": "turn-000042-cmd-01",
            "activity_id": "activity.followup", "trigger_ref": "event-00000001",
            "reason": "mandatory_followup",
        }]
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", settled)

    def test_action_and_transition_paths_do_not_collapse(self):
        action = action_command()
        invalid_action = dict(action, transition_request={
            "transition_kind": "transition.location_change",
            "payload": {"target_id": "actor-1", "destination_id": "location-2"},
        })
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", invalid_action)

        transition = transition_command()
        validate("runtime-command-state.schema.json", transition)
        invalid_transition = dict(transition, resolution_cursor="effect")
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", invalid_transition)

    def test_settled_direct_transition_keeps_committed_segment_evidence_on_command(self):
        transition = transition_command("command.settled")
        transition["direct_transition_segments"] = [committed_transition_segment()]
        validate("runtime-command-state.schema.json", transition)

    def test_post_commit_direct_transition_with_pending_child_keeps_segment_evidence(self):
        pending = {
            "firing_key": "event-00000001:binding-1",
            "root_command_id": "turn-1-cmd-01",
            "activity_id": "activity.followup",
            "trigger_ref": "event-00000001",
            "reason": "mandatory_followup",
        }
        transition = transition_command()
        transition["pending_child_invocations"] = [pending]
        with self.assertRaises(ValidationError):
            validate("runtime-command-state.schema.json", transition)

        transition["direct_transition_segments"] = [committed_transition_segment([pending])]
        validate("runtime-command-state.schema.json", transition)


if __name__ == "__main__":
    unittest.main()
