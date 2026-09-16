import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

import context_runtime
from context_budget import estimate_size


def candidate(candidate_id, *, channel="EXPLICIT_REF", required=False, rank=0, size=10, eligible=True, current=True, depends_on=()):
    return {"candidate_id": candidate_id, "channel": channel, "required": required, "rank": rank, "size": size, "eligible": eligible, "current": current, "depends_on": list(depends_on), "payload": {"ref": candidate_id}}


class ContextDiscoveryTests(unittest.TestCase):
    def test_discovery_uses_only_registered_bounded_channels(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 1}
        found = context_runtime.discover_candidates(request, [candidate("b", channel="HISTORY_HINT"), candidate("a")])
        self.assertEqual([item["candidate_id"] for item in found], ["a"])


class ContextEligibilityTests(unittest.TestCase):
    def test_ineligible_or_stale_candidate_is_not_role_evidence(self):
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("secret", eligible=False))
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("stale", current=False))


class RequiredPacketClosureTests(unittest.TestCase):
    def test_required_dependency_closure_precedes_optional_allocation(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "budget": 25}
        result = context_runtime.assemble_context(request, [candidate("root", required=True, size=10, depends_on=("dependency",)), candidate("dependency", required=True, size=10), candidate("optional", rank=99, size=10)])
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["dependency", "root"])

    def test_missing_required_closure_is_terminal_unsatisfiable(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "budget": 25}
        result = context_runtime.assemble_context(request, [candidate("root", required=True, depends_on=("missing",))])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")


class ContextAllocationTests(unittest.TestCase):
    def test_central_estimator_counts_utf8_when_no_owner_size_is_declared(self):
        self.assertEqual(estimate_size("ё"), 4)

    def test_required_floor_cannot_be_evicted_by_optional_material(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["required"], "budget": 10}
        result = context_runtime.assemble_context(request, [candidate("optional", rank=100, size=10), candidate("required", required=True, size=10)])
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["required"])
        self.assertEqual(result["bundle"]["optional"], [])


class OptionalRankingTests(unittest.TestCase):
    def test_optional_ranking_is_deterministic_within_remaining_budget(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": [], "budget": 20}
        result = context_runtime.assemble_context(request, [candidate("b", rank=2), candidate("a", rank=2), candidate("c", rank=1)])
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["optional"]], ["a", "b"])


class RetrospectiveContextTests(unittest.TestCase):
    def test_retrospective_payload_is_explicitly_a_projection(self):
        request = {"profile_id": "profile.commentator", "allowed_channels": ["HISTORY_HINT"], "max_candidates": 2, "required_ids": [], "budget": 10, "retrospective": True}
        result = context_runtime.assemble_context(request, [candidate("story-1", channel="HISTORY_HINT")])
        self.assertTrue(result["bundle"]["retrospective_projection"])
        self.assertNotIn("gameplay_truth", result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
    def test_trace_is_diagnostic_and_does_not_include_payload(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 2, "required_ids": [], "budget": 10}
        result = context_runtime.assemble_context(request, [candidate("a")])
        self.assertEqual(result["trace"]["included_ids"], ["a"])
        self.assertNotIn("payload", json.dumps(result["trace"]))


class ScopedContextJoinTests(unittest.TestCase):
    def test_scoped_join_rejects_different_request_basis(self):
        bundle = {"profile_id": "profile.narration", "source_frontier": "frontier-1", "recipient_id": "player-1"}
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.scoped_context_join(bundle, {"profile_id": "profile.actor", "source_frontier": "frontier-1", "recipient_id": "player-1"})

    def test_context_schemas_are_strict_and_examples_validate(self):
        for name in ("context-need-profile.schema.json", "context-trace.schema.json"):
            schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            for example in schema["examples"]:
                Draft202012Validator(schema).validate(example)


if __name__ == "__main__":
    unittest.main()
