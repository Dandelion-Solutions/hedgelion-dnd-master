from __future__ import annotations

from copy import deepcopy
import unittest

from jsonschema import Draft202012Validator, ValidationError

from DEV.TESTS.test_rd15_catalog_runtime import _bind_context, _schema_registry
from GAME.TOOLS.catalog_runtime import BoundCatalogContext
from GAME.TOOLS.runtime_execution import (
    CatalogGap,
    CommandAcceptanceError,
    accept_command,
    validate_execution_proposal,
)
from GAME.TOOLS.mechanics import (
    ExecutionConflict,
    ExecutionContractError,
    ExecutionStore,
    FixedRng,
    close_resolution,
    execute_segment,
    resolve_mechanic,
    resume_accepted_execution,
)


def _interpreter_result() -> dict[str, str]:
    return {
        "kind": "interpreter_result",
        "purpose": "interpret",
        "bundle_id": "bundle-1",
        "source_generation": "frontier-7",
        "intent": "make a check",
    }


def _candidate() -> dict[str, str]:
    return {"definition_id": "activity.check.generic", "kind": "definition.activity"}


def _proposal(activity_id: str = "activity.check.generic") -> dict[str, object]:
    return {
        "command_id": "turn-1-cmd-01",
        "interaction_id": "turn-1",
        "intent_plan_id": "turn-1-plan",
        "clause_id": "c1",
        "action_request": {
            "activity_id": activity_id,
            "actor_id": "actor-1",
            "target_ids": ["actor-2"],
        },
        "root_resolution_id": "resolution-1",
    }


def _pending_child_invocation() -> dict[str, str]:
    return {
        "firing_key": "event-1:binding-1",
        "root_command_id": "turn-1-cmd-01",
        "activity_id": "activity.followup",
        "trigger_ref": "event-1",
        "reason": "mandatory_followup",
    }


class AcceptedIdentityTests(unittest.TestCase):
    def test_accepted_command_pins_the_exact_interpreter_result_context_and_candidate(self) -> None:
        interpreter_result = _interpreter_result()
        context = _bind_context()

        accepted = accept_command(interpreter_result, context, _candidate(), _proposal())

        self.assertNotIsInstance(accepted, CatalogGap)
        self.assertEqual(accepted["interpreter_result"], interpreter_result)
        self.assertEqual(
            accepted["catalog_context"]["catalog_context_fingerprint"], context.fingerprint
        )
        self.assertEqual(accepted["candidate_binding"]["definition_id"], "activity.check.generic")
        self.assertEqual(accepted["schema_version"], 2)
        self.assertEqual(accepted["input_fingerprint_generation"], 2)
        self.assertRegex(accepted["input_fingerprint"], r"^[a-f0-9]{64}$")
        registry, schemas = _schema_registry()
        Draft202012Validator(
            schemas["runtime-command-state.schema.json"], registry=registry
        ).validate(accepted)

    def test_forged_public_context_cannot_be_used_for_acceptance(self) -> None:
        admitted = _bind_context()
        forged = BoundCatalogContext(
            admitted.basis, admitted.definition_dependencies, admitted.fingerprint
        )

        with self.assertRaisesRegex(CommandAcceptanceError, "admitted"):
            accept_command(_interpreter_result(), forged, _candidate(), _proposal())


class ProposalValidationTests(unittest.TestCase):
    def test_unavailable_candidate_is_typed_gap_evidence_not_an_accepted_command(self) -> None:
        result = accept_command(
            _interpreter_result(),
            _bind_context(),
            {"definition_id": "activity.unknown", "kind": "definition.activity"},
            _proposal("activity.unknown"),
        )

        self.assertIsInstance(result, CatalogGap)
        self.assertEqual(result.gap_report["reason"], "definition_not_found")


class AcceptedExecutionCatalogBasisTests(unittest.TestCase):
    def test_proposal_rejects_context_or_candidate_selected_after_acceptance(self) -> None:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        self.assertNotIsInstance(accepted, CatalogGap)

        with self.assertRaisesRegex(CommandAcceptanceError, "stale catalog context"):
            validate_execution_proposal(accepted, _bind_context(_request_with_frontier_revision(5)), _candidate())
        with self.assertRaisesRegex(CommandAcceptanceError, "candidate differs from accepted binding"):
            validate_execution_proposal(
                accepted,
                _bind_context(),
                {"definition_id": "activity.unknown", "kind": "definition.activity"},
            )

    def test_forged_command_fingerprint_cannot_reach_execution(self) -> None:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        self.assertNotIsInstance(accepted, CatalogGap)
        forged = dict(accepted)
        forged["input_fingerprint"] = "0" * 64

        with self.assertRaisesRegex(CommandAcceptanceError, "input fingerprint"):
            validate_execution_proposal(forged, _bind_context(), _candidate())

    def test_settled_command_retains_exact_accepted_basis(self) -> None:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        self.assertNotIsInstance(accepted, CatalogGap)
        settled = dict(accepted, disposition="command.settled")

        registry, schemas = _schema_registry()
        Draft202012Validator(
            schemas["runtime-command-state.schema.json"], registry=registry
        ).validate(settled)
        validate_execution_proposal(settled, _bind_context(), _candidate())
        for field in (
            "catalog_context",
            "candidate_binding",
            "interpreter_result",
            "interpreter_result_fingerprint_generation",
            "interpreter_result_fingerprint",
        ):
            self.assertEqual(settled[field], accepted[field])

        for field in (
            "catalog_context",
            "candidate_binding",
            "interpreter_result",
            "interpreter_result_fingerprint_generation",
            "interpreter_result_fingerprint",
        ):
            discarded_basis = dict(settled)
            discarded_basis.pop(field)
            with self.subTest(discarded_field=field), self.assertRaises(ValidationError):
                Draft202012Validator(
                    schemas["runtime-command-state.schema.json"], registry=registry
                ).validate(discarded_basis)

    def test_accepted_input_fingerprint_ignores_lifecycle_and_rejects_accepted_input_tampering(self) -> None:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        self.assertNotIsInstance(accepted, CatalogGap)

        with_pending_child = dict(accepted, pending_child_invocations=[_pending_child_invocation()])
        validate_execution_proposal(with_pending_child, _bind_context(), _candidate())
        self.assertEqual(with_pending_child["input_fingerprint"], accepted["input_fingerprint"])

        settled = dict(accepted, disposition="command.settled")
        validate_execution_proposal(settled, _bind_context(), _candidate())
        self.assertEqual(settled["input_fingerprint"], accepted["input_fingerprint"])

        tampered = dict(accepted)
        tampered["action_request"] = dict(accepted["action_request"], actor_id="actor-3")
        with self.assertRaisesRegex(CommandAcceptanceError, "input fingerprint"):
            validate_execution_proposal(tampered, _bind_context(), _candidate())


class DeterministicExecutionTests(unittest.TestCase):
    def _accepted(self) -> dict[str, object]:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate(), _proposal())
        self.assertNotIsInstance(accepted, CatalogGap)
        return accepted

    def _resolution(self, **overrides: object) -> dict[str, object]:
        value: dict[str, object] = {
            "resolution_id": "resolution-1",
            "root_command_id": "turn-1-cmd-01",
            "initiating_command_id": "turn-1-cmd-01",
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "procedure_id": "procedure-1",
            "execution_cursor": "step.check.resolve",
            "safe_recompute_phase": "determine",
        }
        value.update(overrides)
        return value

    def test_retry_reuses_fixed_rng_and_event_identity(self) -> None:
        accepted = self._accepted()
        resolution = self._resolution()
        store = ExecutionStore()
        first_rng = FixedRng([17])
        first = execute_segment(
            accepted,
            resolution,
            rng=first_rng,
            event_kind="event.check.resolved",
            event_payload={"result": 17},
            store=store,
        )

        retry_rng = FixedRng([3])
        retry = execute_segment(
            accepted,
            resolution,
            rng=retry_rng,
            event_kind="event.check.resolved",
            event_payload={"result": 17},
            store=store,
        )

        self.assertEqual(first, retry)
        self.assertEqual(first["roll_result"]["raw_values"], [17])
        self.assertEqual(first["event"]["segment_id"], first["segment"]["segment_id"])
        self.assertEqual(first["event"]["event_ordinal"], 1)
        self.assertEqual(first_rng.draw_count, 1)
        self.assertEqual(retry_rng.draw_count, 0)
        registry, schemas = _schema_registry()
        for schema_name, value in (
            ("execution-segment.schema.json", first["segment"]),
            ("runtime-mechanical-event-state.schema.json", first["event"]),
            ("resolution-receipt.schema.json", first["receipt"]),
        ):
            with self.subTest(schema=schema_name):
                Draft202012Validator(schemas[schema_name], registry=registry).validate(value)

    def test_procedure_and_continuation_temporal_state_is_preserved_exactly(self) -> None:
        accepted = self._accepted()
        procedure = {
            "procedure_kind": "procedure.combat_minimal",
            "lifecycle_state": "turn_active",
            "participant_ids": ["actor-1"],
            "initiative_order": ["actor-1"],
            "round_number": 2,
            "round_advance_pending": False,
            "active_turn_index": 0,
            "participant_resources": {"actor-1": {"resource.action_budget": {"spent": 1}}},
        }
        continuation = {
            "generation": 2,
            "root_command_id": accepted["command_id"],
            "resolution_id": "resolution-1",
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "procedure_id": "procedure-1",
            "execution_cursor": "step.check.resolve",
            "safe_recompute_phase": "determine",
            "committed_segment_refs": [],
            "fixed_rng_results": [],
        }
        result = execute_segment(
            accepted,
            self._resolution(status="AWAITING_REACTION", next_segment_sequence=2),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            procedure_state=procedure,
            continuation_state=continuation,
            store=ExecutionStore(),
        )

        self.assertEqual(result["procedure_state"], procedure)
        self.assertEqual(
            result["continuation_state"]["committed_segment_refs"],
            ["resolution-1:segment:2"],
        )
        self.assertEqual(
            result["continuation_state"]["fixed_rng_results"][0]["raw_values"],
            [17],
        )
        self.assertEqual(result["continuation_state"]["generation"], 3)
        self.assertEqual(procedure["round_number"], 2)
        self.assertEqual(continuation["committed_segment_refs"], [])

    def test_stale_continuation_generation_fails_closed_before_execution(self) -> None:
        accepted = self._accepted()
        continuation = {
            "generation": 1,
            "committed_segment_refs": [],
            "fixed_rng_results": [],
        }
        rng = FixedRng([17])

        with self.assertRaisesRegex(ExecutionConflict, "stale continuation"):
            execute_segment(
                accepted,
                self._resolution(),
                rng=rng,
                event_payload={"result": 17},
                continuation_state=continuation,
                expected_continuation_generation=2,
                store=ExecutionStore(),
            )

        self.assertEqual(rng.draw_count, 0)

    def test_tampered_accepted_input_is_rejected_before_mechanics(self) -> None:
        accepted = self._accepted()
        forged = dict(accepted)
        forged["action_request"] = dict(accepted["action_request"], actor_id="actor-9")
        rng = FixedRng([17])

        with self.assertRaisesRegex(ExecutionContractError, "input fingerprint"):
            execute_segment(
                forged,
                self._resolution(),
                rng=rng,
                event_payload={"result": 17},
                store=ExecutionStore(),
            )

        self.assertEqual(rng.draw_count, 0)

    def test_same_command_identity_with_a_different_fingerprint_is_rejected(self) -> None:
        accepted = self._accepted()
        forged = dict(accepted, input_fingerprint="0" * 64)

        with self.assertRaisesRegex(ExecutionConflict, "input fingerprint"):
            execute_segment(
                forged,
                self._resolution(),
                event_payload={"result": 17},
                store=ExecutionStore(),
            )

    def test_lost_acknowledgement_retry_returns_the_existing_committed_result(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        execute_segment(
            accepted,
            self._resolution(),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )

        recovered = resume_accepted_execution(
            accepted,
            self._resolution(),
            rng=FixedRng([2]),
            event_payload={"result": 17},
            store=store,
        )

        self.assertEqual(recovered["event_id"], "resolution-1:segment:1:event:1")
        self.assertEqual(recovered["roll_result"]["raw_values"], [17])

    def test_conflicting_replay_payload_fails_closed_without_new_event(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        first = execute_segment(
            accepted,
            self._resolution(),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )

        with self.assertRaisesRegex(ExecutionConflict, "conflicting input"):
            execute_segment(
                accepted,
                self._resolution(),
                rng=FixedRng([3]),
                event_payload={"result": 3},
                store=store,
            )

        committed = store.lookup(accepted["command_id"])
        self.assertEqual(committed["event_id"], first["event_id"])
        self.assertEqual(committed["roll_result"]["raw_values"], [17])

    def test_recovery_replay_reuses_fixed_rng_and_segment_identity(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        first = resolve_mechanic(
            accepted,
            self._resolution(),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )
        retry_rng = FixedRng([19])

        replay = resume_accepted_execution(
            accepted,
            self._resolution(),
            rng=retry_rng,
            event_payload={"result": 17},
            store=store,
        )

        self.assertEqual(replay["segment"]["segment_id"], first["segment"]["segment_id"])
        self.assertEqual(replay["event"]["event_ordinal"], 1)
        self.assertEqual(replay["roll_result"], first["roll_result"])
        self.assertEqual(retry_rng.draw_count, 0)

    def test_existing_fixed_roll_is_reused_without_a_new_rng_draw(self) -> None:
        accepted = self._accepted()
        roll = {
            "roll_id": "resolution-1:roll:1",
            "request_id": "resolution-1:roll:1",
            "expression": "fixed",
            "raw_values": [17],
            "source_kind": "rng.system",
            "provenance_ref": "resolution-1:rng:1",
        }
        rng = FixedRng([3])

        result = execute_segment(
            accepted,
            self._resolution(fixed_rng_results=[roll]),
            rng=rng,
            event_payload={"result": 17},
            store=ExecutionStore(),
        )

        self.assertEqual(result["roll_result"], roll)
        self.assertEqual(rng.draw_count, 0)

    def test_retry_accepts_resolution_with_its_committed_evidence(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        first = execute_segment(
            accepted,
            self._resolution(),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )

        retry = execute_segment(
            accepted,
            first["resolution"],
            rng=FixedRng([3]),
            event_payload={"result": 17},
            store=store,
        )

        self.assertEqual(retry, first)

    def test_later_segment_under_one_root_command_gets_its_own_idempotency_slot(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        first = execute_segment(
            accepted,
            self._resolution(next_segment_sequence=1, segments=[]),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )
        second_resolution = deepcopy(first["resolution"])
        second_resolution["next_segment_sequence"] = 2
        second_roll_request = {
            "roll_id": "resolution-1:roll:2",
            "request_id": "resolution-1:roll:2",
            "expression": "fixed",
            "source_kind": "rng.system",
            "provenance_ref": "resolution-1:rng:2",
        }

        second = execute_segment(
            accepted,
            second_resolution,
            rng=FixedRng([19]),
            roll_request=second_roll_request,
            event_payload={"result": 19},
            store=store,
        )

        self.assertEqual(second["segment"]["segment_id"], "resolution-1:segment:2")
        self.assertNotEqual(first["event_id"], second["event_id"])
        self.assertEqual(len(second["resolution"]["segments"]), 2)
        self.assertEqual(
            store.lookup("resolution-1", "resolution-1:segment:1")["event_id"], first["event_id"]
        )
        self.assertEqual(
            store.lookup("resolution-1", "resolution-1:segment:2")["event_id"], second["event_id"]
        )

        replay_rng = FixedRng([23])
        replay = resume_accepted_execution(
            accepted,
            second["resolution"],
            rng=replay_rng,
            event_payload={"result": 19},
            store=store,
        )

        self.assertEqual(replay, second)
        self.assertEqual(replay["segment"]["segment_id"], "resolution-1:segment:2")
        self.assertEqual(replay["roll_result"]["raw_values"], [19])
        self.assertEqual(replay_rng.draw_count, 0)

    def test_child_resolution_under_one_root_command_has_a_distinct_owner_slot(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        child_resolution = self._resolution(
            resolution_id="resolution-child",
            activity_id="activity.followup",
            actor_id="actor-2",
            initiating_command_id=None,
            causal_invocation_key="resolution-1:segment:1:event:1",
        )
        child_resolution.pop("initiating_command_id")

        child = execute_segment(
            accepted,
            child_resolution,
            event_payload={"followup": True},
            store=store,
        )

        self.assertEqual(child["resolution_id"], "resolution-child")
        self.assertEqual(child["event"]["root_command_id"], accepted["command_id"])
        self.assertEqual(
            store.lookup("resolution-child", "resolution-child:segment:1")["event_id"],
            child["event_id"],
        )

    def test_close_requires_stored_result_and_rejects_tampered_evidence(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        committed = execute_segment(
            accepted,
            self._resolution(status="RUNNING"),
            event_payload={"result": 17},
            store=store,
        )
        with self.assertRaisesRegex(ExecutionContractError, "stored"):
            close_resolution(committed)
        for field_path in ("segment", "event", "receipt"):
            tampered = deepcopy(committed)
            if field_path == "segment":
                tampered["segment"]["event_ids"] = []
            elif field_path == "event":
                tampered["event"]["payload"]["result"] = 99
            else:
                tampered["receipt"]["event_ids"] = []
            with self.subTest(field=field_path), self.assertRaisesRegex(
                ExecutionConflict, "stored committed evidence"
            ):
                close_resolution(tampered, store=store)

        closed = close_resolution(committed, store=store)
        stored = store.lookup("resolution-1", "resolution-1:segment:1")
        self.assertEqual(closed["segment"], committed["segment"])
        self.assertEqual(closed["event"], committed["event"])
        self.assertEqual(closed["receipt"], committed["receipt"])
        self.assertEqual(stored["segment"], committed["segment"])
        self.assertEqual(stored["event"], committed["event"])
        self.assertEqual(stored["receipt"], committed["receipt"])
        stored["event"]["payload"]["result"] = 99
        self.assertEqual(
            store.lookup("resolution-1", "resolution-1:segment:1")["event"]["payload"]["result"],
            17,
        )

    def test_mismatched_root_binding_fails_before_rng_or_store_mutation(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        rng = FixedRng([17])

        with self.assertRaisesRegex(ExecutionConflict, "root_command_id"):
            execute_segment(
                accepted,
                self._resolution(root_command_id="other-command"),
                rng=rng,
                event_payload={"result": 17},
                store=store,
            )

        self.assertEqual(rng.draw_count, 0)
        self.assertIsNone(store.lookup("resolution-1", "resolution-1:segment:1"))

    def test_mismatched_procedure_binding_fails_before_rng_or_store_mutation(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        rng = FixedRng([17])

        with self.assertRaisesRegex(ExecutionConflict, "procedure_id"):
            execute_segment(
                accepted,
                self._resolution(),
                rng=rng,
                procedure_state={"procedure_id": "procedure-other"},
                event_payload={"result": 17},
                store=store,
            )

        self.assertEqual(rng.draw_count, 0)
        self.assertIsNone(store.lookup("resolution-1", "resolution-1:segment:1"))

    def test_mismatched_continuation_binding_fails_before_rng_or_store_mutation(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        rng = FixedRng([17])
        continuation = {
            "generation": 1,
            "root_command_id": "other-command",
            "resolution_id": "resolution-1",
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "procedure_id": "procedure-1",
            "execution_cursor": "step.check.resolve",
            "safe_recompute_phase": "determine",
            "committed_segment_refs": [],
            "fixed_rng_results": [],
        }

        with self.assertRaisesRegex(ExecutionConflict, "continuation root_command_id"):
            execute_segment(
                accepted,
                self._resolution(),
                rng=rng,
                continuation_state=continuation,
                event_payload={"result": 17},
                store=store,
            )

        self.assertEqual(rng.draw_count, 0)
        self.assertIsNone(store.lookup("resolution-1", "resolution-1:segment:1"))

    def test_replay_with_conflicting_fixed_rng_fails_without_reroll(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        first = execute_segment(
            accepted,
            self._resolution(),
            rng=FixedRng([17]),
            event_payload={"result": 17},
            store=store,
        )
        conflicting_resolution = dict(first["resolution"])
        conflicting_resolution["fixed_rng_results"] = [
            dict(first["roll_result"], raw_values=[18])
        ]
        retry_rng = FixedRng([3])

        with self.assertRaisesRegex(ExecutionConflict, "conflicting fixed RNG"):
            execute_segment(
                accepted,
                conflicting_resolution,
                rng=retry_rng,
                event_payload={"result": 17},
                store=store,
            )

        self.assertEqual(retry_rng.draw_count, 0)

    def test_invalid_downstream_payload_does_not_commit_or_consume_fixed_rng(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        rng = FixedRng([17])

        with self.assertRaises(ExecutionContractError):
            execute_segment(
                accepted,
                self._resolution(),
                rng=rng,
                event_payload={"result": {"nested": True}},
                store=store,
            )

        self.assertIsNone(store.lookup(accepted["command_id"]))
        self.assertEqual(rng.draw_count, 0)

    def test_close_resolution_preserves_segment_and_event_identity(self) -> None:
        accepted = self._accepted()
        store = ExecutionStore()
        running = execute_segment(
            accepted,
            self._resolution(status="RUNNING"),
            event_payload={"progress": True},
            store=store,
        )

        closed = close_resolution(running, store=store)

        self.assertEqual(closed["status"], "COMPLETED")
        self.assertEqual(closed["segment"]["segment_id"], running["segment"]["segment_id"])
        self.assertEqual(closed["event_id"], running["event_id"])
        self.assertEqual(closed["resolution"]["status"], "COMPLETED")
        self.assertEqual(closed["resolution"]["segments"][-1]["resulting_execution_state"], "RUNNING")
        self.assertEqual(
            store.lookup(accepted["root_resolution_id"], running["segment"]["segment_id"])["status"],
            "RUNNING",
        )

    def test_full_resolution_and_continuation_outputs_match_owner_schemas(self) -> None:
        accepted = self._accepted()
        resolution = {
            "root_command_id": accepted["command_id"],
            "initiating_command_id": accepted["command_id"],
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "ctx",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": "0700d3ccf367ade9ff56f620c4330bd5b4544fb9e22031f9d1eac3718a88ef2d",
            "procedure_id": "procedure-1",
            "status": "COMPLETED",
            "next_segment_sequence": 1,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        continuation = {
            "generation": 1,
            "root_command_id": accepted["command_id"],
            "resolution_id": "resolution-1",
            "activity_id": "activity.check.generic",
            "actor_id": "actor-1",
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": "ctx",
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": "0700d3ccf367ade9ff56f620c4330bd5b4544fb9e22031f9d1eac3718a88ef2d",
            "procedure_id": "procedure-1",
            "execution_cursor": "step.check.resolve",
            "safe_recompute_phase": "determine",
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "committed_segment_refs": [],
            "dependency_frontier_refs": [],
            "expected_child_resolution_ids": [],
            "future_rng_frontier": "rng:1",
        }
        result = execute_segment(
            accepted,
            resolution,
            rng=FixedRng([17]),
            event_payload={"result": 17},
            continuation_state=continuation,
            store=ExecutionStore(),
        )

        registry, schemas = _schema_registry()
        for schema_name, value in (
            ("runtime-resolution-state.schema.json", result["resolution"]),
            ("runtime-continuation-state.schema.json", result["continuation_state"]),
        ):
            with self.subTest(schema=schema_name):
                Draft202012Validator(schemas[schema_name], registry=registry).validate(value)


def _request_with_frontier_revision(revision: int) -> dict[str, object]:
    from DEV.TESTS.test_rd15_catalog_runtime import _request

    return _request(frontier_revision=revision)


if __name__ == "__main__":
    unittest.main()
