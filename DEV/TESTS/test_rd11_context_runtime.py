import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

import context_runtime
from context_budget import ContextBudgetError, allocate, estimate_size


def candidate(candidate_id, *, channel="EXPLICIT_REF", required=False, rank=0, size=10, eligible=True, current=True, depends_on=()):
    dependencies = [{"relation": "requires", "candidate_id": item} for item in depends_on]
    return {"candidate_id": candidate_id, "channel": channel, "required": required, "rank": rank, "eligible": eligible, "current": current, "dependencies": dependencies, "payload": {"ref": candidate_id, "text": "x" * size}}


def request(**values):
    values.setdefault("allowed_relations", ["requires"])
    return values


def budget_for(*items):
    return sum(estimate_size(item["payload"]) for item in items)


class ContextDiscoveryTests(unittest.TestCase):
    def test_duplicate_candidate_identity_is_rejected_not_silently_overwritten(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 2}
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.discover_candidates(request, [candidate("same"), candidate("same")])
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
    def test_unregistered_dependency_relation_is_rejected(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "allowed_relations": [] , "budget": 25}
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.assemble_context(request, [candidate("root", depends_on=("secret",))])
    def test_required_dependency_closure_precedes_optional_allocation(self):
        root, dependency, optional = candidate("root", required=True, size=10, depends_on=("dependency",)), candidate("dependency", required=True, size=10), candidate("optional", rank=99, size=10)
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "allowed_relations": ["requires"], "budget": budget_for(root, dependency) + 1}
        result = context_runtime.assemble_context(request, [root, dependency, optional])
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["dependency", "root"])

    def test_missing_required_closure_is_terminal_unsatisfiable(self):
        root = candidate("root", required=True, depends_on=("missing",))
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "allowed_relations": ["requires"], "budget": budget_for(root)}
        result = context_runtime.assemble_context(request, [root])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_ineligible_required_closure_is_terminal_unsatisfiable(self):
        required = candidate("required", eligible=False)
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["required"], "allowed_relations": [], "budget": budget_for(required)}
        result = context_runtime.assemble_context(request, [required])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")

    def test_relation_bearing_profile_requires_admitted_typed_relations(self):
        root = candidate("root", depends_on=("dependency",))
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["root"], "budget": budget_for(root)}
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.assemble_context(request, [root])


class ContextAllocationTests(unittest.TestCase):
    def test_declared_negative_size_cannot_bypass_actual_allocation(self):
        with self.assertRaises(ContextBudgetError):
            allocate([], [{"candidate_id": "bad", "size": -100}], 0)
    def test_central_estimator_counts_utf8_when_no_owner_size_is_declared(self):
        self.assertEqual(estimate_size("ё"), 4)

    def test_required_floor_cannot_be_evicted_by_optional_material(self):
        optional, required = candidate("optional", rank=100, size=10), candidate("required", required=True, size=10)
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": ["required"], "allowed_relations": [], "budget": budget_for(required)}
        result = context_runtime.assemble_context(request, [optional, required])
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["required"])
        self.assertEqual(result["bundle"]["optional"], [])


class OptionalRankingTests(unittest.TestCase):
    def test_optional_ranking_is_deterministic_within_remaining_budget(self):
        a, b, c = candidate("a", rank=2), candidate("b", rank=2), candidate("c", rank=1)
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 5, "required_ids": [], "allowed_relations": [], "budget": budget_for(a, b)}
        result = context_runtime.assemble_context(request, [b, a, c])
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["optional"]], ["a", "b"])


class RetrospectiveContextTests(unittest.TestCase):
    def test_retrospective_payload_is_explicitly_a_projection(self):
        item = candidate("story-1", channel="HISTORY_HINT")
        request = {"profile_id": "profile.commentator", "allowed_channels": ["HISTORY_HINT"], "max_candidates": 2, "required_ids": [], "allowed_relations": [], "budget": budget_for(item), "retrospective": True}
        result = context_runtime.assemble_context(request, [item])
        self.assertTrue(result["bundle"]["retrospective_projection"])
        self.assertNotIn("gameplay_truth", result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
    def test_trace_is_diagnostic_and_does_not_include_payload(self):
        item = candidate("a")
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 2, "required_ids": [], "allowed_relations": [], "budget": budget_for(item)}
        result = context_runtime.assemble_context(request, [item])
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
        profile_schema = json.loads((SCHEMAS / "context-need-profile.schema.json").read_text(encoding="utf-8"))
        self.assertIn("allowed_relations", profile_schema["required"])
        Draft202012Validator(profile_schema).validate({"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 1, "required_ids": [], "allowed_relations": ["requires"], "budget": 10})
        with self.assertRaises(ValidationError):
            Draft202012Validator(profile_schema).validate({"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 1, "required_ids": [], "allowed_relations": [1], "budget": 10})


if __name__ == "__main__":
    unittest.main()
