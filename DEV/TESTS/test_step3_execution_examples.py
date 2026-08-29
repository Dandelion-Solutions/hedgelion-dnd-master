import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
WP05_TEST = ROOT / "DEV" / "TESTS" / "test_r2_7_wp05_execution_conformance.py"


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
        "request_id": "roll.attack.1",
        "provenance_ref": "rng:fixture",
    }


def action_command(disposition="command.accepted"):
    return {
        "interaction_id": "turn-1",
        "intent_plan_id": "turn-1-plan",
        "clause_id": "c1",
        "command_kind": "action",
        "catalog_context_fingerprint": "ctx",
        "input_fingerprint": "fp",
        "disposition": disposition,
        "invocation_facts": [],
        "action_request": {
            "activity_id": "activity.attack.basic",
            "actor_id": "actor-1",
            "target_ids": ["actor-2"],
        },
        "root_resolution_id": "resolution-1",
        "pending_child_invocations": [],
    }


def resolution(status="COMPLETED"):
    return {
        "root_command_id": "turn-1-cmd-01",
        "initiating_command_id": "turn-1-cmd-01",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-1",
        "target_ids": ["actor-2"],
        "catalog_context_fingerprint": "ctx",
        "ruleset_set_sha256": "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143",
        "status": status,
        "next_segment_sequence": 2,
        "invocation_facts": [],
        "fixed_rng_results": [roll()],
        "prior_step_exports": {"hit": True},
        "child_resolution_ids": [],
        "segments": [{
            "segment_sequence": 1,
            "commit_state": "committed",
            "resulting_execution_state": status,
            "event_ids": ["event-1"],
            "pending_child_invocations": [],
            "receipt_exports": {"hit": True},
            "affected_revision_refs": ["actor-2@5"],
        }],
    }


def continuation():
    return {
        "generation": 1,
        "root_command_id": "cmd",
        "resolution_id": "resolution-1",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-1",
        "target_ids": ["actor-2"],
        "catalog_context_fingerprint": "ctx",
        "ruleset_set_sha256": "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143",
        "procedure_id": "procedure-1",
        "execution_cursor": "step.attack.resolve",
        "safe_recompute_phase": "determine",
        "invocation_facts": [],
        "fixed_rng_results": [roll()],
        "prior_step_exports": {"attack_roll": 17},
        "committed_segment_refs": ["resolution-1:segment:1"],
        "dependency_frontier_refs": ["actor-1@4"],
        "expected_child_resolution_ids": [],
        "future_rng_frontier": "rng:2",
    }


class Step3ExecutionExamplesTest(unittest.TestCase):
    def test_A_ordinary_action_is_representable_without_workflow_class(self):
        validate("runtime-command-state.schema.json", action_command("command.settled"))
        validate("runtime-resolution-state.schema.json", resolution())

    def test_B_reaction_suspension_has_bounded_offer_and_fixed_roll(self):
        value = continuation()
        value["pending_response"] = {
            "kind": "reaction",
            "offer_id": "offer-1",
            "parent_resolution_id": "resolution-1",
            "continuation_generation": 1,
            "responder_id": "actor-2",
            "candidate_activity_ids": ["activity.shield"],
        }
        validate("runtime-continuation-state.schema.json", value)

    def test_C_post_commit_followup_is_in_committed_segment_contract(self):
        validate("execution-segment.schema.json", {
            "segment_sequence": 1,
            "commit_state": "committed",
            "resulting_execution_state": "COMPLETED",
            "event_ids": ["event-1"],
            "pending_child_invocations": [{
                "firing_key": "event-1:binding-1",
                "root_command_id": "cmd",
                "activity_id": "activity.concentration_save",
                "trigger_ref": "event-1",
                "reason": "mandatory_followup",
            }],
            "receipt_exports": {},
            "affected_revision_refs": ["actor-1@3"],
        })

    def test_D_intent_plan_represents_partial_completion(self):
        validate("runtime-intent-plan-state.schema.json", {
            "interaction_id": "turn-1",
            "clauses": [
                {"clause_id": "c1", "order": 1, "mapping_outcome": "exact", "execution_state": "intent.executed"},
                {"clause_id": "c2", "order": 2, "mapping_outcome": "exact", "execution_state": "intent.executed"},
                {"clause_id": "c3", "order": 3, "mapping_outcome": "exact", "execution_state": "intent.failed"},
            ],
        })

    def test_E_direct_transition_is_distinct_from_activity_resolution(self):
        validate("runtime-command-state.schema.json", {
            "interaction_id": "turn-1",
            "intent_plan_id": "turn-1-plan",
            "clause_id": "c1",
            "command_kind": "transition",
            "catalog_context_fingerprint": "ctx",
            "input_fingerprint": "fp",
            "disposition": "command.settled",
            "invocation_facts": [],
            "transition_request": {
                "transition_kind": "transition.location_change",
                "payload": {"target_id": "actor-1", "destination_id": "location-2"},
            },
            "direct_transition_segments": [{
                "segment_sequence": 1,
                "commit_state": "committed",
                "resulting_execution_state": "COMPLETED",
                "event_ids": ["event-2"],
                "pending_child_invocations": [],
                "receipt_exports": {},
                "affected_revision_refs": ["actor-1@6"],
            }],
            "direct_transition_receipt": {
                "execution_owner_id": "turn-1-cmd-01",
                "segment_refs": ["turn-1-cmd-01:segment:1"],
                "status": "COMPLETED",
                "event_ids": ["event-2"],
                "exports": {},
                "pending_child_refs": [],
            },
            "pending_child_invocations": [],
        })

    def test_F_ambiguous_target_can_remain_clarification_without_command(self):
        validate("intent-clause.schema.json", {
            "clause_id": "c1",
            "order": 1,
            "mapping_outcome": "clarification_required",
            "execution_state": "intent.pending",
        })

    def test_G_retry_identity_has_stable_accepted_fingerprint_fields(self):
        command = action_command()
        validate("runtime-command-state.schema.json", command)
        self.assertEqual(
            (command["catalog_context_fingerprint"], command["input_fingerprint"]),
            ("ctx", "fp"),
        )

    def test_H_suspended_portable_closure_uses_sources_not_caches(self):
        value = continuation()
        value["generation"] = 3
        value["safe_recompute_phase"] = "effect"
        value["expected_child_resolution_ids"] = ["resolution-2"]
        validate("runtime-continuation-state.schema.json", value)
        for forbidden in (
            "mechanical_context", "temporal_agenda", "procedure_resources",
            "prospective_deltas", "committed_receipt_refs",
        ):
            self.assertNotIn(forbidden, value)

    def test_I_boundary_occurrence_has_stable_identity(self):
        validate("boundary-occurrence.schema.json", {
            "boundary_id": "boundary.turn_end",
            "producer_id": "procedure-1",
            "scope_subject_id": "actor-1",
            "occurrence_key": "procedure-1:turn:7:end",
            "causal_position": "resolution-1:segment:2",
        })

    def test_J_scheduled_due_child_uses_stable_firing_key(self):
        validate("pending-child-invocation.schema.json", {
            "firing_key": "effect-1:daily_save:due-3",
            "root_command_id": "cmd",
            "activity_id": "activity.daily_save",
            "trigger_ref": "due-3",
            "child_resolution_id": "resolution-4",
            "reason": "mandatory_followup",
        })

    def test_K_reaction_child_shares_procedure_by_reference_only(self):
        validate("runtime-procedure-state.schema.json", {
            "participant_resources": {"actor-2": {"resource.reaction": {"spent": 1}}}
        })
        child = {
            "root_command_id": "cmd",
            "causal_invocation_key": "offer-1:activity.shield",
            "activity_id": "activity.shield",
            "actor_id": "actor-2",
            "catalog_context_fingerprint": "ctx",
            "ruleset_set_sha256": "fa0a0794e75a9e0a4343b6394f9d52677e123cd3f01d9b380dd0481bba8fa143",
            "procedure_id": "procedure-1",
            "status": "COMPLETED",
            "next_segment_sequence": 2,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        validate("runtime-resolution-state.schema.json", child)
        self.assertNotIn("procedure_resources", child)

    def test_L_incompatible_catalog_context_is_typed_failure(self):
        validate("resolution-receipt.schema.json", {
            "execution_owner_id": "resolution-1",
            "segment_refs": [],
            "status": "FAILED",
            "event_ids": [],
            "exports": {},
            "pending_child_refs": [],
            "failure_code": "failure.catalog_context_incompatible",
        })

    def test_M_execution_limit_preserves_pending_child_and_open_root(self):
        value = action_command()
        value["pending_child_invocations"] = [{
            "firing_key": "f-limit",
            "root_command_id": "turn-1-cmd-01",
            "activity_id": "activity.followup",
            "trigger_ref": "event-8",
            "reason": "execution_limit",
        }]
        validate("runtime-command-state.schema.json", value)

    def test_N_effect_recency_survives_without_trace_body(self):
        effect = {
            "target_id": "actor-1",
            "application_order_key": 3,
            "lifecycle": {"state_id": "effect_lifecycle.active"},
        }
        validate("world-effect-state.schema.json", effect)
        self.assertNotIn("trace", effect)
        self.assertNotIn("created_at", effect)

    def test_wp05_expanded_schema_family_is_owned_by_r27_conformance(self):
        src = WP05_TEST.read_text(encoding="utf-8")
        for name in (
            "action-request.schema.json",
            "transition-request.schema.json",
            "roll-result.schema.json",
            "choice-request.schema.json",
            "reaction-offer.schema.json",
            "runtime-interaction-state.schema.json",
            "runtime-command-state.schema.json",
            "runtime-resolution-state.schema.json",
            "runtime-continuation-state.schema.json",
            "runtime-resolution-trace-state.schema.json",
            "execution-segment.schema.json",
            "resolution-receipt.schema.json",
        ):
            self.assertIn(name, src)


if __name__ == "__main__":
    unittest.main()
