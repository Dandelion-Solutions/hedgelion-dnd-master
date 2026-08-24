import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


class R27WP05ExecutionConformanceTests(unittest.TestCase):
    WP05_SCHEMAS = (
        "action-request.schema.json",
        "transition-request.schema.json",
        "roll-result.schema.json",
        "choice-request.schema.json",
        "reaction-offer.schema.json",
        "runtime-interaction-state.schema.json",
        "runtime-intent-plan-state.schema.json",
        "runtime-command-state.schema.json",
        "runtime-procedure-state.schema.json",
        "runtime-resolution-state.schema.json",
        "runtime-continuation-state.schema.json",
        "runtime-mechanical-event-state.schema.json",
        "runtime-resolution-trace-state.schema.json",
        "execution-segment.schema.json",
        "pending-child-invocation.schema.json",
        "resolution-receipt.schema.json",
        "boundary-occurrence.schema.json",
        "invocation-fact.schema.json",
        "intent-clause.schema.json",
    )

    def load(self, name):
        return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))

    def registry(self):
        result = Registry()
        for path in SCHEMAS.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if "$id" in data:
                result = result.with_resource(data["$id"], Resource.from_contents(data))
        return result

    def test_independent_step3_owners_have_machine_schemas(self):
        for name in (
            "runtime-interaction-state.schema.json",
            "runtime-intent-plan-state.schema.json",
            "runtime-command-state.schema.json",
            "runtime-procedure-state.schema.json",
            "runtime-resolution-state.schema.json",
            "runtime-continuation-state.schema.json",
            "runtime-mechanical-event-state.schema.json",
            "runtime-resolution-trace-state.schema.json",
        ):
            self.assertTrue((SCHEMAS / name).is_file(), name)

    def test_wp05_schema_examples_are_draft_2020_12_valid(self):
        registry = self.registry()
        for name in self.WP05_SCHEMAS:
            schema = self.load(name)
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema, registry=registry)
            for index, example in enumerate(schema.get("examples", [])):
                with self.subTest(schema=name, example=index):
                    validator.validate(example)

    def test_action_and_transition_requests_are_embedded_protocol_schemas(self):
        for name in ("action-request.schema.json", "transition-request.schema.json"):
            self.assertTrue((SCHEMAS / name).is_file(), name)
        command = self.load("runtime-command-state.schema.json")
        props = command["properties"]
        self.assertIn("action_request", props)
        self.assertIn("transition_request", props)
        self.assertNotIn("receipt_ref", props)

    def test_resolution_owns_concrete_invocation_bindings_and_committed_segments(self):
        resolution = self.load("runtime-resolution-state.schema.json")
        props = resolution["properties"]
        for required in ("activity_id", "actor_id", "segments"):
            self.assertIn(required, props)
        for optional in ("source_id", "target_ids", "parameter_bindings"):
            self.assertIn(optional, props)
        self.assertEqual(
            props["segments"]["items"]["$ref"],
            "https://hedgelion.invalid/schemas/execution-segment.schema.json",
        )
        for duplicate in ("procedure_resources", "resource_state_copy", "world_state"):
            self.assertNotIn(duplicate, props)

    def test_segment_contains_complete_minimum_receipt_evidence(self):
        segment = self.load("execution-segment.schema.json")
        required = set(segment["required"])
        self.assertTrue({
            "segment_sequence",
            "commit_state",
            "resulting_execution_state",
            "event_ids",
            "pending_child_invocations",
            "receipt_exports",
            "affected_revision_refs",
        } <= required)
        self.assertNotIn("world_state", segment["properties"])

    def test_direct_transition_segments_live_on_command_owner(self):
        command = self.load("runtime-command-state.schema.json")
        props = command["properties"]
        self.assertIn("direct_transition_segments", props)
        self.assertEqual(
            props["direct_transition_segments"]["items"]["$ref"],
            "https://hedgelion.invalid/schemas/execution-segment.schema.json",
        )

    def test_continuation_carries_portable_invocation_inputs_but_no_receipt_record_refs(self):
        continuation = self.load("runtime-continuation-state.schema.json")
        props = continuation["properties"]
        for required in ("activity_id", "actor_id", "execution_cursor", "committed_segment_refs"):
            self.assertIn(required, props)
        for optional in ("source_id", "target_ids", "parameter_bindings"):
            self.assertIn(optional, props)
        self.assertNotIn("committed_receipt_refs", props)
        self.assertNotIn("receipt_ref", props)

    def test_pending_choice_and_reaction_are_registered_portable_value_schemas(self):
        self.assertTrue((SCHEMAS / "choice-request.schema.json").is_file())
        self.assertTrue((SCHEMAS / "reaction-offer.schema.json").is_file())
        continuation = self.load("runtime-continuation-state.schema.json")
        refs = {
            branch["$ref"]
            for branch in continuation["properties"]["pending_response"]["oneOf"]
        }
        self.assertEqual(refs, {
            "https://hedgelion.invalid/schemas/choice-request.schema.json",
            "https://hedgelion.invalid/schemas/reaction-offer.schema.json",
        })

    def test_fixed_rng_is_typed_and_reusable_across_resolution_and_continuation(self):
        self.assertTrue((SCHEMAS / "roll-result.schema.json").is_file())
        for owner_name in (
            "runtime-resolution-state.schema.json",
            "runtime-continuation-state.schema.json",
        ):
            owner = self.load(owner_name)
            self.assertEqual(
                owner["properties"]["fixed_rng_results"]["items"]["$ref"],
                "https://hedgelion.invalid/schemas/roll-result.schema.json",
            )

    def test_embedded_receipt_and_segment_do_not_become_runtime_record_classes(self):
        catalog = json.loads((ROOT / "DEV" / "CATALOG" / "core-catalog.json").read_text(encoding="utf-8"))
        kinds = set(catalog["registries"]["runtime_record_kinds"])
        self.assertNotIn("runtime.execution_segment", kinds)
        self.assertNotIn("runtime.receipt", kinds)
        protocol = set(catalog["registries"]["protocol_value_kinds"])
        self.assertIn("value.execution_segment", protocol)
        self.assertIn("value.resolution_receipt", protocol)
        self.assertNotIn("value.runtime_command", protocol)

    def test_interaction_state_links_input_auth_context_and_plan_without_world_mutation(self):
        interaction = self.load("runtime-interaction-state.schema.json")
        props = interaction["properties"]
        for name in ("campaign_id", "session_id", "player_id", "input_message_id", "intent_plan_id"):
            self.assertIn(name, props)
        for forbidden in ("world_delta", "rng_state", "procedure_resources", "state_patch"):
            self.assertNotIn(forbidden, props)

    def test_resolution_trace_is_diagnostic_not_current_state_authority(self):
        trace = self.load("runtime-resolution-trace-state.schema.json")
        props = trace["properties"]
        self.assertIn("resolution_id", props)
        self.assertIn("entries", props)
        serialized = json.dumps(trace)
        for forbidden in ("world_state_snapshot", "procedure_resources", "authoritative_state"):
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
