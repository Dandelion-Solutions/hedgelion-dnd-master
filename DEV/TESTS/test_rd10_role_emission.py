import json
import pickle
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from GAME.TOOLS.live_state import LiveRouting
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.runtime_host import compose_runtime_host

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

import emission
import turn_runtime


class _ContextRepository:
    def __init__(self):
        self.pin_calls = []

    def pin_campaign(self, campaign_id):
        self.pin_calls.append(campaign_id)
        ordinal = len(self.pin_calls)
        return PinnedCampaign(
            campaign_id=campaign_id,
            revision=f"{ordinal:040x}",
            tree_sha=f"{ordinal + 100:040x}",
        )

    def read_exact_path(self, pinned, path):
        raise AssertionError(f"unexpected Context source read: {path}")

    def read_exact_campaign_ref(self, campaign_id):
        return {}

    def read_exact_commit(self, campaign_ref, revision):
        return {}

    def compare_ancestry(self, repository_ref, ancestor_revision, descendant_revision):
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(self, campaign_ref, revision):
        return {}


class _ContextLiveTransport:
    def __init__(self):
        self.calls = 0

    def read_selected_live(self, campaign_id, pinned_campaign):
        self.calls += 1
        return LiveRouting(campaign_id=campaign_id, entries=())


class _CountingContextService:
    def __init__(self, context_service):
        self.context_service = context_service
        self.calls = []

    def assemble(self, request, candidates):
        self.calls.append((request, candidates))
        return self.context_service.assemble(request, candidates)


class _StructuralTestContextAssembler:
    """Trusted harness capability; intentionally not a RuntimeHost service."""

    def __init__(self):
        self.calls = 0

    def assemble(self, request, candidates):
        self.calls += 1
        return {
            "outcome": "ASSEMBLED",
            "bundle": {
                "profile_id": request["profile_id"],
                "role": request["role"],
                "purpose": request["purpose"],
                "subject_id": request["subject_id"],
                "recipient_id": request["recipient_id"],
                "source_frontier": request["source_frontier"],
                "required": [],
                "optional": [],
                "retrospective_projection": False,
            },
            "trace": {"diagnostic": "not phase evidence"},
        }


def _context_service():
    repository = _ContextRepository()
    live_transport = _ContextLiveTransport()
    host = compose_runtime_host("campaign-1", repository, live_transport)
    return _CountingContextService(host.context), repository, live_transport


def _context_request(role, purpose, profile_id, subject_id, recipient_id="player-1"):
    return {
        "profile_id": profile_id,
        "role": role,
        "purpose": purpose,
        "subject_id": subject_id,
        "recipient_id": recipient_id,
        "campaign_id": "campaign-1",
        "allowed_channels": ["CURRENT_SCOPE"],
        "max_candidates": 10,
        "required_ids": [],
        "allowed_relations": ["requires"],
        "budget": 10000,
        "source_frontier": "frontier-7",
        "retrospective": False,
    }


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


def _bind_phase(
    envelope: dict[str, object],
    role: str,
    purpose: str,
    profile_id: str,
    allowed_results: tuple[str, ...],
    *,
    subject_id: str | None = None,
    recipient_id: str = "player-1",
    allowed_handoffs: tuple[str, ...] = (),
    allowed_prior_results: tuple[str, ...] = (),
    context_service: _CountingContextService | None = None,
) -> dict[str, object]:
    actual_subject = "player-1" if subject_id is None else subject_id
    actual_context_service = context_service or _context_service()[0]
    request = _context_request(role, purpose, profile_id, actual_subject, recipient_id)
    return turn_runtime.bind_phase_from_context(
        envelope,
        role,
        purpose,
        profile_id,
        actual_context_service,
        request,
        [],
        allowed_results,
        subject_id=subject_id,
        recipient_id=recipient_id,
        allowed_handoffs=allowed_handoffs,
        allowed_prior_results=allowed_prior_results,
    )


def _bind_narrator(
    envelope: dict[str, object],
    *,
    allowed_handoffs: tuple[str, ...] = ("execution_result",),
    allowed_prior_results: tuple[str, ...] = (),
    context_service: _CountingContextService | None = None,
) -> dict[str, object]:
    return _bind_phase(
        envelope,
        "NARRATOR",
        "narrate",
        "profile.narration",
        ("narration_result",),
        subject_id="player-1",
        allowed_handoffs=allowed_handoffs,
        allowed_prior_results=allowed_prior_results,
        context_service=context_service,
    )


def _narration_result(
    envelope: dict[str, object] | None = None, prose: str = "safe"
) -> dict[str, object]:
    binding = (
        envelope["phase_bindings"]["NARRATOR"]
        if envelope is not None
        else {"bundle_id": "unbound-bundle", "recipient_id": "player-1"}
    )
    return {
        "kind": "narration_result",
        "purpose": "narrate",
        "source_generation": "frontier-7",
        "recipient_id": binding["recipient_id"],
        "bundle_id": binding["bundle_id"],
        "prose": prose,
        "disclosure_refs": [],
    }


def _emission_bundle(
    envelope: dict[str, object], disclosure_refs: list[str] | None = None
) -> dict[str, object]:
    binding = envelope["phase_bindings"]["NARRATOR"]
    return {
        "bundle_id": binding["bundle_id"],
        "recipient_id": binding["recipient_id"],
        "disclosure_refs": [] if disclosure_refs is None else disclosure_refs,
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
    def test_context_binding_mints_basis_from_one_injected_host_assembly(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, repository, live_transport = _context_service()
        request = _context_request(
            "INTERPRETER", "interpret", "profile.intent", "player-1"
        )

        binding = turn_runtime.bind_phase_from_context(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            context_service,
            request,
            [],
            ("interpreter_result",),
        )

        basis = binding["context_basis"]
        self.assertIsInstance(basis, turn_runtime.AcceptedContextBasis)
        self.assertEqual(basis.turn_id, "turn-1")
        self.assertEqual(basis.role, "INTERPRETER")
        self.assertEqual(basis.purpose, "interpret")
        self.assertEqual(basis.profile_id, "profile.intent")
        self.assertEqual(basis.subject_id, "player-1")
        self.assertEqual(basis.recipient_id, "player-1")
        self.assertEqual(basis.source_frontier, "frontier-7")
        self.assertEqual(basis.bundle["role"], "INTERPRETER")
        self.assertNotIn("trace", basis.bundle)
        self.assertNotEqual(basis.bundle_id, "bundle-1")
        self.assertEqual(len(context_service.calls), 1)
        self.assertEqual(repository.pin_calls, ["campaign-1"])
        self.assertEqual(live_transport.calls, 1)

        structural_assembler = _StructuralTestContextAssembler()
        data_plane_replacement = _StructuralTestContextAssembler()
        untrusted_envelope = turn_runtime.start_turn("turn-2", "frontier-7", 120)
        untrusted_envelope["context_service"] = data_plane_replacement
        untrusted_envelope["context_assembler"] = data_plane_replacement
        untrusted_request = _context_request(
            "INTERPRETER", "interpret", "profile.intent", "player-1"
        )
        untrusted_request["context_service"] = data_plane_replacement
        untrusted_request["context_assembler"] = data_plane_replacement
        untrusted_candidates = [
            {
                "candidate_id": "candidate-1",
                "context_service": data_plane_replacement,
                "context_assembler": data_plane_replacement,
            }
        ]

        turn_runtime.bind_phase_from_context(
            untrusted_envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            structural_assembler,
            untrusted_request,
            untrusted_candidates,
            ("interpreter_result",),
            subject_id="player-1",
            recipient_id="player-1",
        )

        self.assertEqual(structural_assembler.calls, 1)
        self.assertEqual(data_plane_replacement.calls, 0)

    def test_accepted_context_and_result_controls_are_not_serializable(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        binding = _bind_phase(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "interpreter_result",
                "purpose": "interpret",
                "bundle_id": binding["bundle_id"],
                "source_generation": "frontier-7",
                "intent": "move",
            },
        )
        accepted_result = binding["accepted_phase_result"]

        for control in (binding["context_basis"], accepted_result):
            with (
                self.subTest(control=type(control).__name__),
                self.assertRaisesRegex(TypeError, "transient"),
            ):
                pickle.dumps(control)

    def test_actor_context_profile_keeps_its_registered_purpose(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        request = _context_request("ACTOR", "reflect", "profile.actor", "actor-1")

        with self.assertRaisesRegex(ValueError, "registered profile"):
            turn_runtime.bind_phase_from_context(
                envelope,
                "ACTOR",
                "reflect",
                "profile.actor",
                context_service,
                request,
                [],
                ("actor_proposal",),
                subject_id="actor-1",
            )
        self.assertEqual(len(context_service.calls), 1)
        self.assertEqual(envelope["phase_bindings"], {})

    def test_actor_result_cannot_escape_its_bound_subject_or_purpose(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        binding = _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-1",
        )

        for result_overrides, error in (
            ({"purpose": "reflect"}, "purpose"),
            ({"subject_id": "actor-2"}, "subject_id"),
        ):
            result = {
                "kind": "actor_proposal",
                "purpose": "assess",
                "bundle_id": binding["bundle_id"],
                "source_generation": "frontier-7",
                "subject_id": "actor-1",
                "proposal": "withdraw",
            }
            result.update(result_overrides)
            with (
                self.subTest(error=error),
                self.assertRaisesRegex(turn_runtime.TurnContractError, error),
            ):
                turn_runtime.accept_phase_result(envelope, result)

    def test_context_request_scope_mismatches_fail_before_assembly(self):
        mismatches = (
            ("role", "ACTOR"),
            ("purpose", "prepare"),
            ("profile_id", "profile.dramaturgy"),
            ("subject_id", "actor-1"),
            ("recipient_id", "player-2"),
            ("source_frontier", "frontier-stale"),
        )
        for field, wrong_value in mismatches:
            with self.subTest(field=field):
                envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
                context_service, _, _ = _context_service()
                request = _context_request(
                    "INTERPRETER", "interpret", "profile.intent", "player-1"
                )
                request[field] = wrong_value
                with self.assertRaises(turn_runtime.TurnContractError):
                    turn_runtime.bind_phase_from_context(
                        envelope,
                        "INTERPRETER",
                        "interpret",
                        "profile.intent",
                        context_service,
                        request,
                        [],
                        ("interpreter_result",),
                        subject_id="player-1",
                        recipient_id="player-1",
                    )
                self.assertEqual(context_service.calls, [])

    def test_context_basis_cannot_cross_turns_with_matching_identifiers(self):
        first_envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        binding = _bind_phase(
            first_envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
        )
        second_envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "not current"):
            turn_runtime.bind_phase(
                second_envelope,
                "INTERPRETER",
                "interpret",
                "profile.intent",
                binding["context_basis"],
                ("interpreter_result",),
                subject_id="player-1",
                recipient_id="player-1",
            )

    def test_context_basis_cannot_be_rebound_after_its_phase_is_replaced(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        first_binding = _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-1",
        )
        _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-2",
        )

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "already bound"):
            turn_runtime.bind_phase(
                envelope,
                "ACTOR",
                "assess",
                "profile.actor",
                first_binding["context_basis"],
                ("actor_proposal",),
                subject_id="actor-1",
                recipient_id="player-1",
            )

    def test_matching_bundle_id_does_not_accept_a_shaped_context_basis(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        envelope["accepted_context_bases"] = {
            "INTERPRETER": {
                "kind": "role_context_basis",
                "bundle_id": "bundle-1",
                "profile_id": "profile.intent",
                "role": "INTERPRETER",
                "purpose": "interpret",
                "source_frontier": "frontier-7",
                "recipient_id": "player-1",
                "required": [{"payload": {"private_context": "forged"}}],
            }
        }

        for caller_value in (
            "bundle-1",
            envelope["accepted_context_bases"]["INTERPRETER"],
        ):
            with (
                self.subTest(caller_value=type(caller_value).__name__),
                self.assertRaisesRegex(
                    turn_runtime.TurnContractError, "accepted Context basis"
                ),
            ):
                turn_runtime.bind_phase(
                    envelope,
                    "INTERPRETER",
                    "interpret",
                    "profile.intent",
                    caller_value,
                    ("interpreter_result",),
                )

    def test_result_requires_its_exact_accepted_context_token(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        envelope["phase_bindings"]["INTERPRETER"] = {
            "role": "INTERPRETER",
            "purpose": "interpret",
            "profile_id": "profile.intent",
            "bundle_id": "bundle-1",
            "context_basis": {
                "kind": "role_context_basis",
                "bundle_id": "bundle-1",
                "profile_id": "profile.intent",
                "role": "INTERPRETER",
                "purpose": "interpret",
                "source_frontier": "frontier-7",
                "recipient_id": "player-1",
            },
            "subject_id": "player-1",
            "recipient_id": "player-1",
            "source_frontier": "frontier-7",
            "assembly_ordinal": 1,
            "allowed_results": ["interpreter_result"],
            "allowed_handoffs": [],
        }

        with self.assertRaisesRegex(
            turn_runtime.TurnContractError, "accepted Context basis"
        ):
            turn_runtime.accept_phase_result(
                envelope,
                {
                    "kind": "interpreter_result",
                    "purpose": "interpret",
                    "bundle_id": "bundle-1",
                    "source_generation": "frontier-7",
                    "intent": "move",
                },
            )

        injected_assembler = _StructuralTestContextAssembler()
        data_plane_replacement = _StructuralTestContextAssembler()
        bound_envelope = turn_runtime.start_turn("turn-2", "frontier-7", 120)
        binding = turn_runtime.bind_phase_from_context(
            bound_envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            injected_assembler,
            _context_request(
                "INTERPRETER", "interpret", "profile.intent", "player-1"
            ),
            [],
            ("interpreter_result",),
            subject_id="player-1",
            recipient_id="player-1",
        )
        untrusted_model_result = {
            "kind": "interpreter_result",
            "purpose": "interpret",
            "bundle_id": binding["bundle_id"],
            "source_generation": "frontier-7",
            "intent": "move",
            "context_assembler": data_plane_replacement,
        }
        with self.assertRaisesRegex(
            turn_runtime.TurnContractError, "registered schema contract"
        ):
            turn_runtime.accept_phase_result(bound_envelope, untrusted_model_result)

        valid_result = dict(untrusted_model_result)
        del valid_result["context_assembler"]
        turn_runtime.accept_phase_result(bound_envelope, valid_result)
        binding["accepted_phase_result"] = {
            **valid_result,
            "context_service": data_plane_replacement,
        }
        narrator_request = _context_request(
            "NARRATOR", "narrate", "profile.narration", "player-1"
        )
        with self.assertRaisesRegex(
            turn_runtime.TurnContractError, "prior result is absent or ambiguous"
        ):
            turn_runtime.bind_phase_from_context(
                bound_envelope,
                "NARRATOR",
                "narrate",
                "profile.narration",
                injected_assembler,
                narrator_request,
                [],
                ("narration_result",),
                subject_id="player-1",
                recipient_id="player-1",
                allowed_handoffs=("execution_result",),
                allowed_prior_results=("interpreter_result",),
            )
        self.assertEqual(injected_assembler.calls, 2)
        self.assertEqual(data_plane_replacement.calls, 0)

    def test_actor_phase_requires_subject_bound_context(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "subject"):
            turn_runtime.bind_phase_from_context(
                envelope,
                "ACTOR",
                "assess",
                "profile.actor",
                _context_service()[0],
                _context_request("ACTOR", "assess", "profile.actor", "actor-1"),
                [],
                ("actor_proposal",),
            )

    def test_actor_prior_result_cannot_cross_subject_scope(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        actor_binding = _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-1",
            context_service=context_service,
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "actor_proposal",
                "purpose": "assess",
                "bundle_id": actor_binding["bundle_id"],
                "source_generation": "frontier-7",
                "subject_id": "actor-1",
                "proposal": "withdraw",
            },
        )

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "subject"):
            _bind_phase(
                envelope,
                "ACTOR",
                "assess",
                "profile.actor",
                ("actor_proposal",),
                subject_id="actor-2",
                allowed_prior_results=("actor_proposal",),
                context_service=context_service,
            )

    def test_only_explicit_minimum_typed_prior_results_cross_phases(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        interpreter_binding = _bind_phase(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
            context_service=context_service,
        )
        interpreter_result = {
            "kind": "interpreter_result",
            "purpose": "interpret",
            "bundle_id": interpreter_binding["bundle_id"],
            "source_generation": "frontier-7",
            "intent": "move",
        }
        turn_runtime.accept_phase_result(envelope, interpreter_result)
        preparation_binding = _bind_phase(
            envelope,
            "DRAMATURG",
            "prepare",
            "profile.dramaturgy",
            ("preparation_draft",),
            context_service=context_service,
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "preparation_draft",
                "purpose": "prepare",
                "bundle_id": preparation_binding["bundle_id"],
                "source_generation": "frontier-7",
                "pressures": ["storm"],
            },
        )

        narrator_binding = _bind_narrator(
            envelope,
            allowed_prior_results=("interpreter_result",),
            context_service=context_service,
        )

        self.assertEqual(len(narrator_binding["prior_results"]), 1)
        prior = narrator_binding["prior_results"][0]
        self.assertIsInstance(prior, turn_runtime.AcceptedPhaseResult)
        self.assertEqual(prior.to_dict(), interpreter_result)
        self.assertNotIn(
            "preparation_draft",
            {item.kind for item in narrator_binding["prior_results"]},
        )

    def test_chronicler_story_result_never_crosses_within_the_same_turn(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        chronicler = _bind_phase(
            envelope,
            "CHRONICLER",
            "chronicle",
            "profile.story",
            ("story_projection_draft",),
            subject_id="campaign-1",
            context_service=context_service,
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "story_projection_draft",
                "purpose": "chronicle",
                "bundle_id": chronicler["bundle_id"],
                "source_generation": "frontier-7",
                "source_refs": ["event-1"],
            },
        )

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "same-envelope"):
            _bind_narrator(
                envelope,
                allowed_prior_results=("story_projection_draft",),
                context_service=context_service,
            )

    def test_narrator_rebind_after_chronicler_requires_a_new_context_assembly(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        narrator_before = _bind_narrator(envelope, context_service=context_service)
        chronicler = _bind_phase(
            envelope,
            "CHRONICLER",
            "chronicle",
            "profile.story",
            ("story_projection_draft",),
            subject_id="campaign-1",
            context_service=context_service,
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "story_projection_draft",
                "purpose": "chronicle",
                "bundle_id": chronicler["bundle_id"],
                "source_generation": "frontier-7",
                "source_refs": ["event-1"],
            },
        )
        turn_runtime.advance_phase(envelope, "CHRONICLER")

        with self.assertRaisesRegex(
            turn_runtime.TurnContractError, "fresh Context rebind"
        ):
            turn_runtime.accept_phase_result(envelope, _narration_result(envelope))

        narrator_after = _bind_narrator(envelope, context_service=context_service)
        self.assertGreater(
            narrator_after["assembly_ordinal"], chronicler["assembly_ordinal"]
        )
        self.assertNotEqual(narrator_after["bundle_id"], narrator_before["bundle_id"])
        self.assertEqual(len(context_service.calls), 3)
        turn_runtime.accept_phase_result(envelope, _narration_result(envelope))

    def test_fresh_narrator_rebind_reuses_accepted_execution_without_conflicting_handoff(
        self,
    ):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        context_service, _, _ = _context_service()
        narrator_before = _bind_narrator(envelope, context_service=context_service)
        execution = _execution_result()
        first_handoff = turn_runtime.accept_execution_handoff(
            envelope, "NARRATOR", execution
        )
        chronicler = _bind_phase(
            envelope,
            "CHRONICLER",
            "chronicle",
            "profile.story",
            ("story_projection_draft",),
            subject_id="campaign-1",
            context_service=context_service,
        )
        turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "story_projection_draft",
                "purpose": "chronicle",
                "bundle_id": chronicler["bundle_id"],
                "source_generation": "frontier-7",
                "source_refs": ["event-1"],
            },
        )
        turn_runtime.advance_phase(envelope, "CHRONICLER")
        narrator_after = _bind_narrator(envelope, context_service=context_service)

        rebound_handoff = turn_runtime.accept_execution_handoff(
            envelope, "NARRATOR", execution
        )

        self.assertNotEqual(narrator_before["bundle_id"], narrator_after["bundle_id"])
        self.assertEqual(
            first_handoff["accepted_command_id"], rebound_handoff["accepted_command_id"]
        )
        self.assertEqual(rebound_handoff["bundle_id"], narrator_after["bundle_id"])
        self.assertEqual(len(envelope["accepted_handoffs"]["NARRATOR"]), 1)

    def test_narrator_binding_cannot_omit_execution_handoff_requirement(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)

        with self.assertRaisesRegex(turn_runtime.TurnContractError, "requires"):
            turn_runtime.bind_phase_from_context(
                envelope,
                "NARRATOR",
                "narrate",
                "profile.narration",
                _context_service()[0],
                _context_request(
                    "NARRATOR", "narrate", "profile.narration", "player-1"
                ),
                [],
                ("narration_result",),
                subject_id="player-1",
                recipient_id="player-1",
            )

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

        narration = _narration_result(envelope, "The check succeeds.")
        turn_runtime.accept_phase_result(envelope, narration)
        payload = emission.commit_visible_payload(
            narration,
            _emission_bundle(envelope),
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
            _bind_phase(
                envelope,
                "INTERPRETER",
                "interpret",
                "profile.intent",
                ("actor_proposal",),
            )

    def test_bound_phase_advances_only_as_transient_control(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_phase(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
        )
        self.assertEqual(turn_runtime.advance_phase(envelope, "INTERPRETER"), "INTERPRETER")

    def test_phase_accepts_only_its_registered_minimum_result_family(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        binding = _bind_phase(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
        )
        accepted = turn_runtime.accept_phase_result(
            envelope,
            {
                "kind": "interpreter_result",
                "purpose": "interpret",
                "bundle_id": binding["bundle_id"],
                "source_generation": "frontier-7",
                "intent": "move",
            },
        )
        self.assertEqual(accepted["kind"], "interpreter_result")
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.accept_phase_result(envelope, {"kind": "narration_result", "prose": "leak"})

    def test_untyped_result_kind_is_rejected_as_a_contract_error(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_phase(
            envelope,
            "INTERPRETER",
            "interpret",
            "profile.intent",
            ("interpreter_result",),
        )
        with self.assertRaisesRegex(turn_runtime.TurnContractError, "registered result"):
            turn_runtime.accept_phase_result(envelope, {"kind": [], "payload": "not typed"})

    def test_raw_bundle_trace_and_hidden_reasoning_cannot_cross_phase_boundary(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-1",
        )
        with self.assertRaises(turn_runtime.TurnContractError):
            turn_runtime.accept_phase_result(
                envelope,
                {"kind": "actor_proposal", "purpose": "assess", "source_generation": "frontier-7", "raw_bundle": {}},
            )

    def test_trace_and_private_diagnostics_are_rejected_from_phase_results(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        binding = _bind_phase(
            envelope,
            "ACTOR",
            "assess",
            "profile.actor",
            ("actor_proposal",),
            subject_id="actor-1",
        )
        for private_field in ("trace", "private_diagnostics", "private_context"):
            result = {
                "kind": "actor_proposal",
                "purpose": "assess",
                "bundle_id": binding["bundle_id"],
                "source_generation": "frontier-7",
                "subject_id": "actor-1",
                "proposal": "withdraw",
                private_field: {"secret": True},
            }
            with (
                self.subTest(private_field=private_field),
                self.assertRaisesRegex(
                    turn_runtime.TurnContractError, "protected private material"
                ),
            ):
                turn_runtime.accept_phase_result(envelope, result)


class ProtectedCapacityTests(unittest.TestCase):
    def test_auxiliary_work_cannot_consume_protected_narrator_capacity(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 20)
        self.assertEqual(turn_runtime.reserve_auxiliary_capacity(envelope, 21), 0)
        self.assertEqual(envelope["protected_narrator_capacity"], 20)


class ProtectedEmissionTests(unittest.TestCase):
    def test_forged_execution_handoff_dict_cannot_unlock_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        result = _narration_result(envelope)
        turn_runtime.accept_phase_result(envelope, result)
        envelope["accepted_handoffs"]["NARRATOR"] = [
            {
                "kind": "execution_result",
                "accepted_command_id": "turn-1-cmd-01",
                "accepted_input_fingerprint": "a" * 64,
                "execution_owner_id": "resolution-1",
                "resolution_id": "resolution-1",
                "status": "COMPLETED",
                "segment_id": "resolution-1:segment:1",
                "event_id": "event-1",
            }
        ]

        with self.assertRaisesRegex(emission.EmissionContractError, "owner-verified"):
            emission.commit_visible_payload(
                result,
                _emission_bundle(envelope),
                "AI_REASONING",
                envelope=envelope,
            )

    def test_untyped_execution_handoff_string_cannot_unlock_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        result = _narration_result(envelope)
        turn_runtime.accept_phase_result(envelope, result)
        envelope["accepted_handoffs"]["NARRATOR"] = ["execution-result"]

        with self.assertRaisesRegex(emission.EmissionContractError, "owner-verified"):
            emission.commit_visible_payload(
                result,
                _emission_bundle(envelope),
                "AI_REASONING",
                envelope=envelope,
            )

    def test_visible_emission_requires_the_protected_envelope(self):
        result = {
            "kind": "narration_result",
            "purpose": "narrate",
            "source_generation": "frontier-7",
            "recipient_id": "player-1",
            "bundle_id": "unbound-bundle",
            "prose": "safe",
            "disclosure_refs": [],
        }

        with self.assertRaisesRegex(emission.EmissionContractError, "envelope"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": "unbound-bundle", "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
            )

    def test_untyped_narration_fields_are_rejected_before_emission(self):
        result = _narration_result()
        result["prose"] = 17

        with self.assertRaisesRegex(emission.EmissionContractError, "incomplete"):
            emission.commit_visible_payload(
                result,
                {"bundle_id": result["bundle_id"], "recipient_id": "player-1", "disclosure_refs": []},
                "AI_REASONING",
                envelope=turn_runtime.start_turn("turn-1", "frontier-7", 120),
            )

    def test_over_capacity_narration_is_rejected_without_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 4)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        turn_runtime.accept_execution_handoff(envelope, "NARRATOR", _execution_result())
        result = _narration_result(envelope, "too long")
        turn_runtime.accept_phase_result(envelope, result)

        with self.assertRaisesRegex(emission.EmissionContractError, "capacity"):
            emission.commit_visible_payload(
                result,
                _emission_bundle(envelope),
                "AI_REASONING",
                envelope=envelope,
            )

        self.assertIsNone(envelope["emitted_payload"])

    def test_execution_handoff_is_required_before_mechanics_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        result = _narration_result(envelope, "mechanics are missing")
        turn_runtime.accept_phase_result(envelope, result)

        with self.assertRaisesRegex(emission.EmissionContractError, "execution handoff"):
            emission.commit_visible_payload(
                result,
                _emission_bundle(envelope),
                "AI_REASONING",
                envelope=envelope,
            )

    def test_only_one_enveloped_visible_result_can_be_committed(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        turn_runtime.accept_execution_handoff(envelope, "NARRATOR", _execution_result())
        result = _narration_result(envelope)
        turn_runtime.accept_phase_result(envelope, result)
        bundle = _emission_bundle(envelope)
        emission.commit_visible_payload(result, bundle, "AI_REASONING", envelope=envelope)

        with self.assertRaisesRegex(emission.EmissionContractError, "already committed"):
            emission.commit_visible_payload(result, bundle, "AI_REASONING", envelope=envelope)

    def test_only_validated_recipient_scoped_narration_can_be_visible(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        result = _narration_result(envelope, "You hear a bell.")
        result["disclosure_refs"] = ["fact.bell"]
        turn_runtime.accept_execution_handoff(envelope, "NARRATOR", _execution_result())
        turn_runtime.accept_phase_result(envelope, result)
        payload = emission.commit_visible_payload(
            result,
            _emission_bundle(envelope, ["fact.bell"]),
            "AI_REASONING",
            envelope=envelope,
        )
        self.assertEqual(payload, {"recipient_id": "player-1", "prose": "You hear a bell.", "disclosure_refs": ["fact.bell"]})

    def test_trace_tool_and_unowned_emission_are_rejected(self):
        result = {
            "kind": "narration_result",
            "purpose": "narrate",
            "source_generation": "frontier-7",
            "recipient_id": "player-1",
            "bundle_id": "unbound-bundle",
            "prose": "safe",
            "disclosure_refs": [],
        }
        with self.assertRaises(emission.EmissionContractError):
            emission.commit_visible_payload({**result, "context_trace": {}}, {"bundle_id": "unbound-bundle", "recipient_id": "player-1", "disclosure_refs": []}, "AI_REASONING")
        with self.assertRaises(emission.EmissionContractError):
            emission.commit_visible_payload(result, {"bundle_id": "unbound-bundle", "recipient_id": "player-1", "disclosure_refs": []}, "PLAY_POLICY")


class AuxiliaryFallbackTests(unittest.TestCase):
    def test_auxiliary_fallback_stays_outside_protected_execution_emission(self):
        envelope = turn_runtime.start_turn("turn-1", "frontier-7", 120)
        _bind_narrator(envelope, allowed_handoffs=("execution_result",))
        turn_runtime.accept_execution_handoff(envelope, "NARRATOR", _execution_result())
        original_handoff = envelope["accepted_handoffs"]["NARRATOR"][0].to_dict()
        original_capacity = envelope["remaining_narrator_capacity"]
        fallback = turn_runtime.select_fallback("UNSATISFIABLE", ("BLOCKED", "DEGRADED"))

        self.assertEqual(turn_runtime.reserve_auxiliary_capacity(envelope, 10_000), 0)
        self.assertEqual(fallback, "BLOCKED")
        self.assertEqual(envelope["remaining_narrator_capacity"], original_capacity)
        self.assertEqual(envelope["accepted_handoffs"]["NARRATOR"][0].to_dict(), original_handoff)
        for private_key in ("event", "resolution", "context_trace", "hidden_reasoning"):
            self.assertNotIn(private_key, original_handoff)

        narration = _narration_result(envelope, "The deterministic result stands.")
        turn_runtime.accept_phase_result(envelope, narration)
        bundle = _emission_bundle(envelope)
        emission.commit_visible_payload(narration, bundle, "AI_REASONING", envelope=envelope)
        with self.assertRaisesRegex(emission.EmissionContractError, "already committed"):
            emission.commit_visible_payload(narration, bundle, "AI_REASONING", envelope=envelope)

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
