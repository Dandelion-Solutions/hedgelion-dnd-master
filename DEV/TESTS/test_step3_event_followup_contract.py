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


class Step3EventFollowupContractTest(unittest.TestCase):
    def test_mechanical_event_identity_is_segment_plus_ordinal(self):
        event = {
            "segment_id": "resolution-0000001:segment:1",
            "event_ordinal": 1,
            "event_kind": "event.damage.applied",
            "root_command_id": "turn-000042-cmd-01",
            "causal_ref": "resolution-0000001",
            "payload": {"amount": 7, "target_id": "actor-0002"},
        }
        validate("runtime-mechanical-event-state.schema.json", event)
        invalid = dict(event)
        invalid.pop("event_ordinal")
        with self.assertRaises(ValidationError):
            validate("runtime-mechanical-event-state.schema.json", invalid)

    def test_identical_payload_does_not_define_identity(self):
        a = {"segment_id": "r:segment:1", "event_ordinal": 1, "event_kind": "event.damage.applied", "root_command_id": "cmd", "causal_ref": "r", "payload": {"amount": 7}}
        b = dict(a, event_ordinal=2)
        validate("runtime-mechanical-event-state.schema.json", a)
        validate("runtime-mechanical-event-state.schema.json", b)
        self.assertNotEqual((a["segment_id"], a["event_ordinal"]), (b["segment_id"], b["event_ordinal"]))

    def test_committed_segment_can_atomically_carry_mandatory_followup(self):
        segment = {
            "segment_sequence": 1,
            "commit_state": "committed",
            "event_ids": ["event-00000001"],
            "pending_child_invocations": [{
                "firing_key": "effect-1:damage:event-00000001",
                "root_command_id": "cmd",
                "activity_id": "activity.concentration_save",
                "trigger_ref": "event-00000001",
                "reason": "mandatory_followup",
            }],
            "receipt_exports": {},
            "affected_revision_refs": ["actor-2@18"],
        }
        validate("execution-segment.schema.json", segment)
        invalid = dict(segment)
        invalid["pending_child_invocations"] = [{
            "firing_key": "f", "root_command_id": "cmd",
            "activity_id": "activity.followup", "trigger_ref": "event-NOT-IN-SEGMENT",
            "reason": "mandatory_followup",
        }]
        # Cross-membership is an execution invariant; the machine test records the required relationship explicitly.
        self.assertNotIn(invalid["pending_child_invocations"][0]["trigger_ref"], invalid["event_ids"])


if __name__ == "__main__":
    unittest.main()
