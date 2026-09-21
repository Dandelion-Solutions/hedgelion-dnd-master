import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from GAME.TOOLS import history as history_module


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

import context_runtime
from context_budget import ContextBudgetError, allocate, estimate_size
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    build_live_ref,
    build_live_route,
    derive_live_epoch_id,
)


def candidate(candidate_id, *, channel="EXPLICIT_REF", required=False, rank=0, size=10, eligible=None, current=None, depends_on=()):
    dependencies = [{"relation": "requires", "candidate_id": item} for item in depends_on]
    result = {
        "candidate_id": candidate_id,
        "channel": channel,
        "required": required,
        "rank": rank,
        "dependencies": dependencies,
        "owner_family": "world.scene",
        "owner_identity": [candidate_id],
        "payload": {"ref": candidate_id, "text": "x" * size},
    }
    if eligible is not None:
        result["eligible"] = eligible
    if current is not None:
        result["current"] = current
    return result


def request(**values):
    values.setdefault("profile_id", "profile.narration")
    values.setdefault("role", "NARRATOR")
    values.setdefault("purpose", "narrate")
    values.setdefault("subject_id", "actor.context")
    values.setdefault("recipient_id", "player-1")
    values.setdefault("campaign_id", "campaign-context")
    values.setdefault("allowed_channels", ["EXPLICIT_REF"])
    values.setdefault("max_candidates", 5)
    values.setdefault("required_ids", [])
    values.setdefault("allowed_relations", ["requires"])
    values.setdefault("budget", 1000)
    return values


def budget_for(*items):
    runtime = native_runtime_for(items)
    total = 0
    for item in items:
        admitted = runtime.resolve_candidate_basis(request(), item)
        total += estimate_size(admitted["payload"])
    return total


class RepositoryFixture:
    def __init__(self):
        self.revision = "a" * 40
        self.tree_sha = "b" * 40
        self.records = {}
        self.reads = []

    def pin_campaign(self, campaign_id):
        return PinnedCampaign(campaign_id, self.revision, self.tree_sha)

    def read_exact_path(self, pinned, path):
        self.reads.append((pinned, path))
        return self.records[path]

    def add_record(self, family, identity, record):
        self.records[route_native_record(family, identity).relative_path] = record


class SelectedLiveReader:
    def __init__(self, projection):
        self.projection = projection
        self.calls = []

    def read_selected_live_source(self, route, source):
        self.calls.append((route, source))
        return self.projection


def live_fixture():
    claims = (LiveClaim.exact_owner("world.actor", "actor.context"),)
    scene_id = "scene-context"
    epoch_id = derive_live_epoch_id("campaign-context", scene_id, "0" * 40, claims)
    source = LiveEnvelope(
        campaign_id="campaign-context",
        scene_id=scene_id,
        epoch_id=epoch_id,
        source_ref=build_live_ref("campaign-context", scene_id, epoch_id),
        source_revision="c" * 40,
        claims=claims,
        opening_campaign_revision="0" * 40,
    )
    route = build_live_route(source.campaign_id, (source,))
    projection = {
        "source_key": list(source.source_key),
        "source_ref": source.source_ref,
        "source_revision": source.source_revision,
        "source_native_ids": list(source.source_native_ids),
        "material": {"scene": source.scene_id},
    }
    return route, source, projection


def bound_request(**values):
    request = {
        "profile_id": "profile.narration",
        "role": "NARRATOR",
        "purpose": "narrate",
        "subject_id": "actor.context",
        "recipient_id": "player-1",
        "campaign_id": "campaign-context",
        "allowed_channels": ["EXPLICIT_REF"],
        "max_candidates": 5,
        "required_ids": [],
        "allowed_relations": [],
        "budget": 1000,
    }
    request.update(values)
    return request


def owner_candidate(candidate_id, family, identity, *, channel="EXPLICIT_REF", **values):
    result = {
        "candidate_id": candidate_id,
        "channel": channel,
        "owner_family": family,
        "owner_identity": list(identity),
        "payload": {"caller": "untrusted"},
    }
    result.update(values)
    return result


def native_runtime_for(items):
    repository = RepositoryFixture()
    for item in items:
        family = item.get("owner_family", "world.scene")
        identity = tuple(item.get("owner_identity", (item["candidate_id"],)))
        if family == "world.scene":
            repository.add_record(
                family,
                identity,
                {
                    "kind": family,
                    "id": identity[0],
                    "state": {"ref": identity[0], "text": "native"},
                },
            )
    return context_runtime._compose_context_runtime(repository)


class ContextDiscoveryTests(unittest.TestCase):
    def test_duplicate_candidate_identity_is_rejected_not_silently_overwritten(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 2}
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.discover_candidates(request, [candidate("same"), candidate("same")])
    def test_discovery_uses_only_registered_bounded_channels(self):
        request = {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 1}
        found = context_runtime.discover_candidates(request, [candidate("b", channel="HISTORY_HINT"), candidate("a")])
        self.assertEqual([item["candidate_id"] for item in found], ["a"])


class HostBoundContextContractTests(unittest.TestCase):
    def test_context_runtime_is_bound_to_the_trusted_repository_owner(self):
        runtime = context_runtime._compose_context_runtime(RepositoryFixture())
        self.assertIsInstance(runtime, context_runtime.BoundContextRuntime)

    def test_registered_role_purpose_subject_recipient_bindings_are_finite(self):
        runtime = context_runtime._compose_context_runtime(RepositoryFixture())
        bindings = (
            ("profile.intent", "INTERPRETER", "interpret"),
            ("profile.dramaturgy", "DRAMATURG", "prepare"),
            ("profile.actor", "ACTOR", "assess"),
            ("profile.story", "CHRONICLER", "chronicle"),
            ("profile.narration", "NARRATOR", "narrate"),
        )
        for profile_id, role, purpose in bindings:
            with self.subTest(role=role):
                result = runtime.assemble(
                    bound_request(
                        profile_id=profile_id,
                        role=role,
                        purpose=purpose,
                    ),
                    [],
                )
                self.assertEqual(result["outcome"], "ASSEMBLED")
                self.assertEqual(result["bundle"]["role"], role)
                self.assertEqual(result["bundle"]["subject_id"], "actor.context")
                self.assertEqual(result["bundle"]["recipient_id"], "player-1")

    def test_unregistered_profile_or_role_cannot_widen_binding(self):
        runtime = context_runtime._compose_context_runtime(RepositoryFixture())
        with self.assertRaises(context_runtime.ContextContractError):
            runtime.assemble(bound_request(profile_id="profile.custom"), [])
        with self.assertRaises(context_runtime.ContextContractError):
            runtime.assemble(bound_request(role="NARRATOR", purpose="planning"), [])

    def test_public_resolution_rejects_caller_pinned_campaign_substitution(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.scene",
            ("scene-1",),
            {"kind": "world.scene", "id": "scene-1", "state": {"name": "Native scene"}},
        )
        runtime = context_runtime._compose_context_runtime(repository)
        stale_pin = PinnedCampaign("campaign-context", "c" * 40, "d" * 40)

        with self.assertRaises(context_runtime.ContextContractError):
            runtime.resolve_candidate_basis(
                bound_request(),
                owner_candidate("scene-1", "world.scene", ("scene-1",)),
                pinned=stale_pin,
            )
        self.assertEqual(repository.reads, [])

    def test_context_schema_and_runtime_share_the_finite_request_contract(self):
        schema = json.loads((SCHEMAS / "context-need-profile.schema.json").read_text(encoding="utf-8"))
        profile_ids = set(schema["properties"]["profile_id"]["enum"])
        self.assertEqual(profile_ids, set(context_runtime.REGISTERED_PROFILE_IDS))
        Draft202012Validator(schema).validate(bound_request())

        for invalid in (
            {key: value for key, value in bound_request().items() if key != "recipient_id"},
            {**bound_request(), "profile_id": "profile.custom"},
            {**bound_request(), "profile_id": "profile.actor", "role": "NARRATOR"},
            {**bound_request(), "semantic_resolver": "caller"},
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema).validate(invalid)
                with self.assertRaises(context_runtime.ContextContractError):
                    context_runtime._compose_context_runtime(RepositoryFixture()).assemble(invalid, [])

    def test_context_uses_the_existing_private_live_contract_not_a_public_reader(self):
        self.assertNotIn("SelectedLiveReadCapability", vars(context_runtime))
        self.assertNotIn("PinnedCampaign", vars(context_runtime))
        self.assertNotIn("bind_context_runtime", vars(context_runtime))
        self.assertIs(
            context_runtime._SelectedLiveReadCapability,
            history_module._SelectedLiveReadCapability,
        )

    def test_context_host_composition_rejects_a_forged_live_reader(self):
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime._compose_context_runtime(
                RepositoryFixture(),
                live_route=None,
                selected_live_reader=object(),
            )

    def test_context_runtime_module_revision_is_current(self):
        self.assertEqual(context_runtime.FRAMEWORK_MODULE_VERSION, "1.0.6")

    def test_campaign_record_is_reloaded_from_pinned_repository_not_candidate_payload(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.scene",
            ("scene-1",),
            {
                "kind": "world.scene",
                "id": "scene-1",
                "state": {"name": "Native scene"},
            },
        )
        runtime = context_runtime._compose_context_runtime(repository)
        result = runtime.assemble(
            bound_request(),
            [owner_candidate("scene-1", "world.scene", ("scene-1",))],
        )
        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(result["bundle"]["optional"][0]["payload"]["state"]["name"], "Native scene")
        self.assertNotIn("caller", result["bundle"]["optional"][0]["payload"])
        self.assertNotIn("current", result["bundle"]["optional"][0])
        self.assertNotIn("eligible", result["bundle"]["optional"][0])
        self.assertEqual(len(repository.reads), 1)

    def test_caller_flags_and_semantic_loader_fields_are_not_authority(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.scene",
            ("scene-1",),
            {"kind": "world.scene", "id": "scene-1", "state": {"name": "Native scene"}},
        )
        runtime = context_runtime._compose_context_runtime(repository)
        forged = owner_candidate(
            "scene-1",
            "world.scene",
            ("scene-1",),
            current=True,
            eligible=True,
            exact_load=lambda *_args: None,
            validator=lambda *_args: True,
            resolver=lambda *_args: True,
        )
        with self.assertRaises(context_runtime.ContextContractError):
            runtime.resolve_candidate_basis(bound_request(), forged)

    def test_unsupported_family_is_degraded_for_optional_and_terminal_for_required(self):
        runtime = context_runtime._compose_context_runtime(RepositoryFixture())
        optional = owner_candidate("mystery-1", "runtime.mystery", ("mystery-1",))
        optional_result = runtime.assemble(bound_request(), [optional])
        self.assertEqual(optional_result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional_result["bundle"]["optional"], [])
        required_result = runtime.assemble(
            bound_request(required_ids=["mystery-1"]),
            [optional],
        )
        self.assertEqual(required_result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(required_result["bundle"])

    def test_live_candidate_uses_only_the_bound_read_capability_and_route(self):
        route, source, projection = live_fixture()
        reader = SelectedLiveReader(projection)
        runtime = context_runtime._compose_context_runtime(
            RepositoryFixture(),
            live_route=route,
            selected_live_reader=reader,
        )
        result = runtime.assemble(
            bound_request(allowed_channels=["LIVE_CURRENT"]),
            [
                owner_candidate(
                    "live-scene",
                    "LIVE",
                    source.source_key,
                    channel="LIVE_CURRENT",
                    source_key=list(source.source_key),
                )
            ],
        )
        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(len(reader.calls), 1)
        self.assertEqual(result["bundle"]["optional"][0]["payload"], projection)

    def test_fixed_dispatch_revalidates_player_knowledge_and_disclosure_owners(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.player",
            ("player-1",),
            {
                "kind": "world.player",
                "id": "player-1",
                "state": {},
                "player_id": "player-1",
                "github_binding": {"user_id": "account-1", "login": "player"},
                "status": "active",
                "deactivated_by": None,
                "controlled_pc_ids": [],
            },
        )
        repository.add_record(
            "world.knowledge",
            ("actor.context", "fact-1"),
            {
                "kind": "world.knowledge",
                "knower_id": "actor.context",
                "fact_id": "fact-1",
                "state": {"stance": "known"},
            },
        )
        repository.add_record(
            "runtime.disclosure",
            ("player-1", "fact-1"),
            {
                "kind": "runtime.disclosure",
                "player_id": "player-1",
                "fact_id": "fact-1",
                "message_id": "message-1",
            },
        )
        candidates = [
            owner_candidate("player-1", "world.player", ("player-1",), channel="CURRENT_SCOPE"),
            owner_candidate("fact-1", "world.knowledge", ("actor.context", "fact-1")),
            owner_candidate("disclosure-1", "runtime.disclosure", ("player-1", "fact-1")),
        ]
        result = context_runtime._compose_context_runtime(repository).assemble(
            bound_request(allowed_channels=["CURRENT_SCOPE", "EXPLICIT_REF"]),
            candidates,
        )
        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(
            [item["candidate_id"] for item in result["bundle"]["optional"]],
            ["disclosure-1", "fact-1", "player-1"],
        )

    def test_player_and_knowledge_recipient_or_subject_mismatch_fail_closed(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.player",
            ("other-player",),
            {
                "kind": "world.player",
                "id": "other-player",
                "state": {},
                "player_id": "other-player",
                "github_binding": {"user_id": "account-2", "login": "other"},
                "status": "active",
                "deactivated_by": None,
                "controlled_pc_ids": [],
            },
        )
        repository.add_record(
            "world.knowledge",
            ("actor.other", "fact-2"),
            {
                "kind": "world.knowledge",
                "knower_id": "actor.other",
                "fact_id": "fact-2",
                "state": {"stance": "known"},
            },
        )
        candidates = [
            owner_candidate("other-player", "world.player", ("other-player",)),
            owner_candidate("fact-2", "world.knowledge", ("actor.other", "fact-2")),
        ]
        result = context_runtime._compose_context_runtime(repository).assemble(
            bound_request(), candidates
        )
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(result["bundle"]["optional"], [])

    def test_information_owner_recipient_binding_blocks_private_native_material(self):
        repository = RepositoryFixture()
        repository.add_record(
            "world.lore_fact",
            ("fact-private",),
            {
                "kind": "world.lore_fact",
                "id": "fact-private",
                "state": {"statement": "private"},
                "recipient_player_id": "other-player",
            },
        )
        result = context_runtime._compose_context_runtime(repository).assemble(
            bound_request(),
            [owner_candidate("fact-private", "information", ("fact-private",))],
        )
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(result["bundle"]["optional"], [])


class ContextEligibilityTests(unittest.TestCase):
    def test_ineligible_or_stale_candidate_is_not_role_evidence(self):
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("secret", eligible=False))
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("stale", current=False))


class RequiredPacketClosureTests(unittest.TestCase):
    def test_unregistered_dependency_relation_is_rejected(self):
        root = candidate("root", depends_on=("secret",))
        request_value = request(profile_id="profile.narration", required_ids=["root"], allowed_relations=[], budget=1000)
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.assemble_context(request_value, [root], runtime=native_runtime_for([root]))
    def test_required_dependency_closure_precedes_optional_allocation(self):
        root, dependency, optional = candidate("root", required=True, size=10, depends_on=("dependency",)), candidate("dependency", required=True, size=10), candidate("optional", rank=99, size=10)
        request_value = request(profile_id="profile.narration", required_ids=["root"], allowed_relations=["requires"], budget=budget_for(root, dependency) + 1)
        result = context_runtime.assemble_context(request_value, [root, dependency, optional], runtime=native_runtime_for([root, dependency, optional]))
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["dependency", "root"])

    def test_missing_required_closure_is_terminal_unsatisfiable(self):
        root = candidate("root", required=True, depends_on=("missing",))
        request_value = request(profile_id="profile.narration", required_ids=["root"], allowed_relations=["requires"], budget=budget_for(root))
        result = context_runtime.assemble_context(request_value, [root], runtime=native_runtime_for([root]))
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_ineligible_required_closure_is_terminal_unsatisfiable(self):
        required = candidate("required", eligible=False)
        request_value = request(profile_id="profile.narration", required_ids=["required"], allowed_relations=[], budget=1000)
        result = context_runtime.assemble_context(request_value, [required], runtime=native_runtime_for([required]))
        self.assertEqual(result["outcome"], "UNSATISFIABLE")

    def test_relation_bearing_profile_requires_admitted_typed_relations(self):
        root = candidate("root", depends_on=("dependency",))
        request_value = request(profile_id="profile.narration", required_ids=["root"], allowed_relations=[], budget=1000)
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.assemble_context(request_value, [root], runtime=native_runtime_for([root]))


class ContextAllocationTests(unittest.TestCase):
    def test_declared_negative_size_cannot_bypass_actual_allocation(self):
        with self.assertRaises(ContextBudgetError):
            allocate([], [{"candidate_id": "bad", "size": -100}], 0)
    def test_central_estimator_counts_utf8_when_no_owner_size_is_declared(self):
        self.assertEqual(estimate_size("ё"), 4)

    def test_required_floor_cannot_be_evicted_by_optional_material(self):
        optional, required = candidate("optional", rank=100, size=10), candidate("required", required=True, size=10)
        request_value = request(profile_id="profile.narration", required_ids=["required"], allowed_relations=[], budget=budget_for(required))
        result = context_runtime.assemble_context(request_value, [optional, required], runtime=native_runtime_for([optional, required]))
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["required"])
        self.assertEqual(result["bundle"]["optional"], [])


class OptionalRankingTests(unittest.TestCase):
    def test_optional_ranking_is_deterministic_within_remaining_budget(self):
        a, b, c = candidate("a", rank=2), candidate("b", rank=2), candidate("c", rank=1)
        request_value = request(profile_id="profile.narration", required_ids=[], allowed_relations=[], budget=budget_for(a, b))
        result = context_runtime.assemble_context(request_value, [b, a, c], runtime=native_runtime_for([a, b, c]))
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["optional"]], ["a", "b"])


class RetrospectiveContextTests(unittest.TestCase):
    def test_retrospective_payload_is_explicitly_a_projection(self):
        item = candidate("story-1", channel="HISTORY_HINT")
        request_value = request(profile_id="profile.story", role="CHRONICLER", purpose="chronicle", allowed_channels=["HISTORY_HINT"], max_candidates=2, required_ids=[], allowed_relations=[], budget=budget_for(item), retrospective=True)
        result = context_runtime.assemble_context(request_value, [item], runtime=native_runtime_for([item]))
        self.assertTrue(result["bundle"]["retrospective_projection"])
        self.assertNotIn("gameplay_truth", result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
    def test_trace_is_diagnostic_and_does_not_include_payload(self):
        item = candidate("a")
        request_value = request(profile_id="profile.narration", required_ids=[], allowed_relations=[], budget=budget_for(item))
        result = context_runtime.assemble_context(request_value, [item], runtime=native_runtime_for([item]))
        self.assertEqual(result["trace"]["included_ids"], ["a"])
        self.assertNotIn("payload", json.dumps(result["trace"]))


class ScopedContextJoinTests(unittest.TestCase):
    def test_scoped_join_rejects_different_request_basis(self):
        bundle = {
            "profile_id": "profile.narration",
            "role": "NARRATOR",
            "purpose": "narrate",
            "subject_id": "actor.context",
            "source_frontier": "frontier-1",
            "recipient_id": "player-1",
        }
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.scoped_context_join(bundle, {**bundle, "profile_id": "profile.actor"})

    def test_context_schemas_are_strict_and_examples_validate(self):
        for name in ("context-need-profile.schema.json", "context-trace.schema.json"):
            schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            for example in schema["examples"]:
                Draft202012Validator(schema).validate(example)
        profile_schema = json.loads((SCHEMAS / "context-need-profile.schema.json").read_text(encoding="utf-8"))
        self.assertIn("allowed_relations", profile_schema["required"])
        Draft202012Validator(profile_schema).validate(
            bound_request(max_candidates=1, required_ids=[], allowed_relations=["requires"], budget=10)
        )
        with self.assertRaises(ValidationError):
            Draft202012Validator(profile_schema).validate(
                {**bound_request(max_candidates=1, required_ids=[], allowed_relations=["requires"], budget=10), "allowed_relations": [1]}
            )


if __name__ == "__main__":
    unittest.main()
