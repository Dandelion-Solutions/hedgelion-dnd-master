import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
RULESET_SET_SHA256 = "0700d3ccf367ade9ff56f620c4330bd5b4544fb9e22031f9d1eac3718a88ef2d"


def load(name: str):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def registry():
    result = Registry()
    for path in SCHEMAS.glob("*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            result = result.with_resource(schema["$id"], Resource.from_contents(schema))
    return result


def validate(name: str, value):
    Draft202012Validator(load(name), registry=registry()).validate(value)


class HouseRulesAdjudicatedInputContractTests(unittest.TestCase):
    def test_boolean_context_fact_channel_stays_boolean_only(self):
        surfaces = json.loads((CATALOG / "mechanical-surfaces.json").read_text(encoding="utf-8"))
        for metadata in surfaces["context_facts"].values():
            self.assertEqual(metadata["source_class"], "INVOCATION_ADJUDICATED")
            self.assertEqual(metadata["value_type"], "boolean")

    def test_adjudicated_activity_parameter_declarations_are_bounded(self):
        valid = (
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "boolean", "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "integer", "minimum": 1, "maximum": 30, "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "number", "allowed_values": [0.5, 1, 2], "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "machine_id", "allowed_values": ["approach.careful", "approach.fast"], "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "machine_id", "allowed_definition_kinds": ["definition.activity"], "cardinality": "single", "required": True},
        )
        for value in valid:
            validate("activity-parameter-spec.schema.json", value)

        invalid = (
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "string", "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "integer", "minimum": 1, "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "number", "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "machine_id", "cardinality": "single", "required": True},
            {"source_class": "INVOCATION_ADJUDICATED", "value_type": "boolean", "cardinality": "many"},
        )
        for value in invalid:
            with self.assertRaises(ValidationError, msg=value):
                validate("activity-parameter-spec.schema.json", value)

    def adjudicated_binding(self):
        return {
            "source_class": "INVOCATION_ADJUDICATED",
            "value": 15,
            "provenance_ref": "interaction-000001:adjudication:dc",
            "eligibility_basis_fingerprint": "sha256:eligibility-A",
            "rules_context_fingerprint": "sha256:rules-A",
            "policy_basis_refs": ["house-rule.social-leverage@0123456789abcdef0123456789abcdef01234567"],
        }

    def test_action_request_accepts_provenanced_adjudicated_binding(self):
        validate(
            "action-request.schema.json",
            {
                "activity_id": "activity.test.generic",
                "actor_id": "actor-0001",
                "parameter_bindings": {"dc": self.adjudicated_binding()},
            },
        )

    def test_resolution_and_continuation_preserve_same_adjudicated_binding_shape(self):
        binding = self.adjudicated_binding()
        resolution = {
            "root_command_id": "cmd-1",
            "initiating_command_id": "cmd-1",
            "activity_id": "activity.test.generic",
            "actor_id": "actor-0001",
            "parameter_bindings": {"dc": binding},
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "ctx",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": RULESET_SET_SHA256,
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        validate("runtime-resolution-state.schema.json", resolution)

        continuation = {
            "generation": 1,
            "root_command_id": "cmd-1",
            "resolution_id": "resolution-1",
            "activity_id": "activity.test.generic",
            "actor_id": "actor-0001",
            "parameter_bindings": {"dc": binding},
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "ctx",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": RULESET_SET_SHA256,
            "execution_cursor": "step.test.resolve",
            "safe_recompute_phase": "determine",
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "committed_segment_refs": [],
            "dependency_frontier_refs": [],
            "expected_child_resolution_ids": [],
            "future_rng_frontier": "rng:1",
        }
        validate("runtime-continuation-state.schema.json", continuation)
        self.assertEqual(
            resolution["parameter_bindings"]["dc"],
            continuation["parameter_bindings"]["dc"],
        )

    def test_house_rules_adjudication_failures_are_closed_and_typed(self):
        required = {
            "failure.adjudication_input_missing",
            "failure.adjudication_input_unauthorized",
            "failure.adjudication_input_invalid",
            "failure.adjudication_context_stale",
            "failure.policy_conflict",
            "failure.policy_realization_gap",
        }
        resolution_codes = set(load("runtime-resolution-state.schema.json")["$defs"]["failureCode"]["enum"])
        receipt_codes = set(load("resolution-receipt.schema.json")["$defs"]["failureCode"]["enum"])
        self.assertTrue(required <= resolution_codes)
        self.assertTrue(required <= receipt_codes)


if __name__ == "__main__":
    unittest.main()
