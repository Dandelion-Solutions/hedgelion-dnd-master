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


def _execution_result() -> dict[str, object]:
    return {
        "accepted_command_id": "turn-1-cmd-01",
        "accepted_input_fingerprint": "a" * 64,
        "execution_owner_id": "resolution-1",
        "resolution_id": "resolution-1",
        "status": "COMPLETED",
        "segment": {"segment_id": "resolution-1:segment:1", "event_ids": ["event-1"]},
        "event_id": "event-1",
        "event": {"segment_id": "resolution-1:segment:1", "root_command_id": "turn-1-cmd-01"},
    }


def _bind_narrator(envelope: dict[str, object], *, allowed_handoffs: tuple[str, ...] = ()) -> None:
    turn_runtime.bind_phase(
        envelope,
        "NARRATOR",
        "narrate",
        "profile.narration",
        "bundle-1",
        ("narration_result",),
        recipient_id="player-1",
        allowed_handoffs=allowed_handoffs,
    )


def _narration_result(prose: str = "safe") -> dict[str, object]:
    return {
        "kind": "narration_result",
        "recipient_id": "player-1",
        "bundle_id": "bundle-1",
        "prose": prose,
        "disclosure_refs": [],
    }


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
    def test_accepted_execution_enters_narrator_before_visible_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        execution = _execution_result()

        handoff = turn_runtime.accept_execution_handoff(envelope, "NARRATOR", execution)

        self.assertEqual(handoff["kind"], "execution_result")
        self.assertEqual(handoff["accepted_command_id"], "turn-1-cmd-01")
        self.assertEqual(handoff["event_id"], execution["event_id"])
        self.assertNotIn("event", handoff)
        self.assertNotIn("resolution", handoff)

        narration = _narration_result("The check succeeds.")
        turn_runtime.accept_phase_result(envelope, narration)
        payload = emission.commit_visible_payload(
            narration,
            {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []},
            "AI_REASONING",
            envelope=envelope,
        )
        self.assertEqual(payload["prose"], "The check succeeds.")

    def test_execution_handoff_rejects_untyped_or_diagnostic_transport(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        with self.assertRaisesRegex(turn_runtime.TurnContractError, "typed object"):
            turn_runtime.accept_execution_handoff(envelope, "NARRATOR", "execution-result")

        diagnostic = {
            "accepted_command_id": "command-1",
            "accepted_input_fingerprint": "a" * 64,
            "execution_owner_id": "resolution-1",
            "resolution_id": "resolution-1",
            "status": "COMPLETED",
            "segment": {"segment_id": "resolution-1:segment:1", "event_ids": ["event-1"]},
            "event_id": "event-1",
            "event": {
                "segment_id": "resolution-1:segment:1",
                "root_command_id": "command-1",
            },
            "context_trace": {"private": True},
        }
        with self.assertRaisesRegex(turn_runtime.TurnContractError, "diagnostic"):
            turn_runtime.accept_execution_handoff(envelope, "NARRATOR", diagnostic)

        invalid_fingerprint = _execution_result()
        invalid_fingerprint["accepted_input_fingerprint"] = "not-a-fingerprint"
        with self.assertRaisesRegex(turn_runtime.TurnContractError, "fingerprint"):
            turn_runtime.accept_execution_handoff(envelope, "NARRATOR", invalid_fingerprint)

    def test_phase_rejects_result_outside_registered_result_and_binding_scope(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ("actor_proposal",))
    def test_bound_phase_advances_only_as_transient_control(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ("interpreter_result",))
        self.assertEqual(turn_runtime.advance_phase(envelope, "INTERPRETER"), "INTERPRETER")

    def test_phase_accepts_only_its_registered_minimum_result_family(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ("interpreter_result",))
        accepted = turn_runtime.accept_phase_result(
            envelope,
            {"kind": "interpreter_result", "purpose": "interpret", "bundle_id": "bundle-1", "source_generation": "frontier-7", "intent": "move"},
        )
        self.assertEqual(accepted["kind"], "interpreter_result")
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.accept_phase_result(envelope, {"kind": "narration_result", "prose": "leak"})

    def test_untyped_result_kind_is_rejected_as_a_contract_error(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "INTERPRETER", "interpret", "profile.intent", "bundle-1", ("interpreter_result",))
        with self.assertRaisesRegex(turn_runtime.TurnContractError, "registered result"):
            turn_runtime.accept_phase_result(envelope, {"kind": [], "payload": "not typed"})

    def test_raw_bundle_trace_and_hidden_reasoning_cannot_cross_phase_boundary(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        turn_runtime.bind_phase(envelope, "ACTOR", "assess", "profile.actor", "bundle-2", ("actor_proposal",))
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
    def test_visible_emission_requires_the_protected_envelope(self):
        result = {
            "kind": "narration_result",
            "recipient_id": "player-1",
            "bundle_id": "bundle-1",
            "prose": "safe",
            "disclosure_refs": [],
        }

        with self.assertRaisesRegex(emission.EmissionContractError, "envelope"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
            )

    def test_untyped_narration_fields_are_rejected_before_emission(self):
        result = _narration_result()
        result["prose"] = 17

        with self.assertRaisesRegex(emission.EmissionContractError, "incomplete"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
                envelope=turn_runtime.start_turn("turn-1", "frontier-7", 120),
            )

    def test_over_capacity_narration_is_rejected_without_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 4)
        _bind_narrator(envelope)
        result = _narration_result("too long")
        turn_runtime.accept_phase_result(envelope, result)

        with self.assertRaisesRegex(emission.EmissionContractError, "capacity"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
                envelope=envelope,
            )

        self.assertIsNone(envelope["emitted_payload"])

    def test_execution_handoff_is_required_before_mechanics_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        result = _narration_result("mechanics are missing")
        turn_runtime.accept_phase_result(envelope, result)

        with self.assertRaisesRegex(emission.EmissionContractError, "execution handoff"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
                envelope=envelope,
            )

    def test_only_one_enveloped_visible_result_can_be_committed(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope)
        result = _narration_result()
        turn_runtime.accept_phase_result(envelope, result)
        bundle = {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": []}
        emission.commit_visible_payload(result, bundle, "AI_REASONING", envelope=envelope)

        with self.assertRaisesRegex(emission.EmissionContractError, "already committed"):
            emission.commit_visible_payload(result, bundle, "AI_REASONING", envelope=envelope)

    def test_only_validated_recipient_scoped_narration_can_be_visible(self):
        result = _narration_result("You hear a bell.")
        result["disclosure_refs"] = ["fact.bell"]
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope)
        turn_runtime.accept_phase_result(envelope, result)
        payload = emission.commit_visible_payload(
            result,
            {"bundle_id": "bundle-1", "recipient_id": "player-1", "disclosure_refs": ["fact.bell"]},
            "AI_REASONING",
            envelope=envelope,
        )
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
