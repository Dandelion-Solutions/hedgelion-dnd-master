import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

import emission
import turn_runtime


class TurnEnvelopeContainmentTests(unittest.TestCase):
    def test_turn_rejects_noninteger_protected_capacity(self):
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.start_turn("turn-1", "frontier-7", "120")

    def test_envelope_is_transient_control_and_has_no_world_authority(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        self.assertEqual(envelope["turn_id"], "turn-1")
        self.assertEqual(envelope["accepted_frontier"], "frontier-7")
        self.assertNotIn("world_state", envelope)
        self.assertNotIn("story_coverage", envelope)


class TypedHandoffTests(unittest.TestCase):
    def test_bound_phase_advances_only_as_transient_control(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ())
        self.assertEqual(turn_runtime.advance_phase(envelope, "INTERPRETER"), "INTERPRETER")

    def test_phase_accepts_only_its_registered_minimum_result_family(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ())
        accepted = turn_runtime.accept_phase_result(
            envelope,
            {"kind": "interpreter_result", "purpose": "interpret", "source_generation": "frontier-7", "intent": "move"},
        )
        self.assertEqual(accepted["kind"], "interpreter_result")
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.accept_phase_result(envelope, {"kind": "narration_result", "prose": "leak"})

    def test_raw_bundle_trace_and_hidden_reasoning_cannot_cross_phase_boundary(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "ACTOR", "assess", "profile.actor", "bundle-2", ())
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.accept_phase_result(
                envelope,
                {"kind": "actor_proposal", "purpose": "assess", "source_generation": "frontier-7", "raw_bundle": {}},
            )


class ProtectedCapacityTests(unittest.TestCase):
    def test_auxiliary_work_cannot_consume_protected_narrator_capacity(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 20)
        self.assertEqual(turn_runtime.reserve_auxiliary_capacity(envelope, 21), 0)
        self.assertEqual(envelope["protected_narrator_capacity"], 20)


class ProtectedEmissionTests(unittest.TestCase):
    def test_only_validated_recipient_scoped_narration_can_be_visible(self):
        result = {"kind": "narration_result", "recipient_id": "player-1", "bundle_id": "bundle-1", "prose": "You hear a bell.", "disclosure_refs": ["fact.bell"]}
        payload = emission.commit_visible_payload(result, {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": ["fact.bell"]}, "AI_REASONING")
        self.assertEqual(payload, {"recipient_id": "player-1", "prose": "You hear a bell.", "disclosure_refs": ["fact.bell"]})

    def test_trace_tool_and_unowned_emission_are_rejected(self):
        result = {"kind": "narration_result", "recipient_id": "player-1", "bundle_id": "bundle-1", "prose": "safe", "disclosure_refs": []}
        with self.assertRaises(emission.EmissionContractError):
            emission.commit_visible_payload({**result, "context_trace": {}}, {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []}, "AI_REASONING")
        with self.assertRaises(emission.EmissionContractError):
            emission.commit_visible_payload(result, {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []}, "PLAY_POLICY")


class AuxiliaryFallbackTests(unittest.TestCase):
    def test_registered_fallback_is_one_finite_terminal_choice(self):
        fallback = turn_runtime.select_fallback("UNSATISFIABLE", ("BLOCKED", "DEGRADED"))
        self.assertEqual(fallback, "BLOCKED")
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.select_fallback("UNSATISFIABLE", ())


class InstructionOwnerTests(unittest.TestCase):
    def test_instruction_owner_is_explicit_and_schema_examples_are_strict(self):
        self.assertEqual(emission.INSTRUCTION_OWNER, "AI_REASONING")
        for name in (
            "turn-envelope.schema.json", "interpreter-result.schema.json", "preparation-draft.schema.json",
            "actor-proposal.schema.json", "story-projection-draft.schema.json", "narration-result.schema.json",
        ):
            schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            for example in schema["examples"]:
                Draft202012Validator(schema).validate(example)


if __name__ == "__main__":
    unittest.main()
