from __future__ import annotations

import unittest

from DEV.TESTS.test_rd15_catalog_runtime import _bind_context
from GAME.TOOLS.runtime_execution import (
    AcceptedRuntimeCommand,
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


class AcceptedIdentityTests(unittest.TestCase):
    def test_accepted_command_pins_the_exact_interpreter_result_context_and_candidate(self) -> None:
        interpreter_result = _interpreter_result()
        context = _bind_context()

        accepted = accept_command(interpreter_result, context, _candidate())

        self.assertIsInstance(accepted, AcceptedRuntimeCommand)
        self.assertEqual(accepted.interpreter_result, interpreter_result)
        self.assertEqual(accepted.catalog_context["catalog_context_fingerprint"], context.fingerprint)
        self.assertEqual(accepted.candidate_binding["definition_id"], "activity.check.generic")
        self.assertRegex(accepted.input_fingerprint, r"^[a-f0-9]{64}$")


class ProposalValidationTests(unittest.TestCase):
    def test_unavailable_candidate_is_typed_gap_evidence_not_an_accepted_command(self) -> None:
        result = accept_command(
            _interpreter_result(),
            _bind_context(),
            {"definition_id": "activity.unknown", "kind": "definition.activity"},
        )

        self.assertIsInstance(result, CatalogGap)
        self.assertEqual(result.gap_report["reason"], "definition_not_found")
        self.assertNotIsInstance(result, AcceptedRuntimeCommand)


class AcceptedExecutionCatalogBasisTests(unittest.TestCase):
    def test_proposal_rejects_context_or_candidate_selected_after_acceptance(self) -> None:
        accepted = accept_command(_interpreter_result(), _bind_context(), _candidate())
        self.assertIsInstance(accepted, AcceptedRuntimeCommand)

        with self.assertRaisesRegex(CommandAcceptanceError, "stale catalog context"):
            validate_execution_proposal(accepted, _bind_context(_request_with_frontier_revision(5)), _candidate())
        with self.assertRaisesRegex(CommandAcceptanceError, "candidate differs from accepted binding"):
            validate_execution_proposal(
                accepted,
                _bind_context(),
                {"definition_id": "activity.unknown", "kind": "definition.activity"},
            )


def _request_with_frontier_revision(revision: int) -> dict[str, object]:
    from DEV.TESTS.test_rd15_catalog_runtime import _request

    return _request(frontier_revision=revision)


if __name__ == "__main__":
    unittest.main()
