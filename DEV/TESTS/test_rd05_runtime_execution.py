from __future__ import annotations

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


def _request_with_frontier_revision(revision: int) -> dict[str, object]:
    from DEV.TESTS.test_rd15_catalog_runtime import _request

    return _request(frontier_revision=revision)


if __name__ == "__main__":
    unittest.main()
