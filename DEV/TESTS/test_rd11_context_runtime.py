import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from GAME.TOOLS.collaboration import (
    CollaborationObligation,
    ContributorRef,
    DependencyClass,
    NativeBasisRef,
)
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    LiveRouting,
    build_live_ref,
    derive_live_epoch_id,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign
from GAME.TOOLS.runtime_host import compose_runtime_host

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "GAME" / "TOOLS"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(TOOLS))

from context_budget import ContextBudgetError, allocate, estimate_size

from GAME.TOOLS import context_runtime


def candidate(
    candidate_id,
    *,
    channel="EXPLICIT_REF",
    required=False,
    rank=0,
    size=10,
    eligible=None,
    current=None,
    depends_on=(),
):
    dependencies = [
        {"relation": "requires", "candidate_id": item} for item in depends_on
    ]
    result = {
        "candidate_id": candidate_id,
        "channel": channel,
        "required": required,
        "role": "NARRATOR",
        "purpose": "narrate",
        "subject_id": "actor.context",
        "recipient_id": "player-1",
        "rank": rank,
        "owner_family": "world.scene",
        "owner_identity": [candidate_id],
        "dependencies": dependencies,
        "payload": {
            "kind": "world.scene",
            "id": candidate_id,
            "state": {"ref": candidate_id, "text": "x" * size},
        },
    }
    if eligible is not None:
        result["eligible"] = eligible
    if current is not None:
        result["current"] = current
    return result


def request(**values):
    result = {
        "profile_id": "profile.narration",
        "role": "NARRATOR",
        "purpose": "narrate",
        "subject_id": "actor.context",
        "recipient_id": "player-1",
        "campaign_id": "campaign-context",
        "allowed_channels": ["EXPLICIT_REF"],
        "max_candidates": 5,
        "required_ids": [],
        "allowed_relations": ["requires"],
        "budget": 1000,
    }
    result.update(values)
    return result


def budget_for(*items):
    return sum(estimate_size(item["payload"]) for item in items)


def native_history_window(*, source_revision, event_id="event-1"):
    event = {
        "schema_version": 1,
        "event_id": event_id,
        "semantic_order": 1,
        "kind": "event.context",
        "provenance_refs": ["resolution.context"],
        "semantic_delta": {"state": "native"},
    }
    return {
        "schema_version": 1,
        "source_domain": "campaign.semantic_events@S",
        "semantic_contract_generation": 1,
        "campaign_id": "campaign-context",
        "origin": "LOCAL",
        "lane": "evt",
        "source_revision": source_revision,
        "lower_exclusive": None,
        "upper": "evt:1",
        "enumeration_representation": "runtime.semantic_event.evt.v1",
        "owner_contracts": [{"family": "runtime.semantic_event", "schema_version": 1}],
        "entries": [
            {
                "candidate_id": json.dumps([event_id], separators=(",", ":")),
                "ordinal": 1,
                "event": event,
            }
        ],
        "interval_complete": True,
    }


class RuntimeRepository:
    def __init__(self, campaign_id="campaign-context"):
        self.campaign_id = campaign_id
        self.records = {}
        self.read_paths = []
        self.pin_calls = []

    def pin_campaign(self, campaign_id):
        self.pin_calls.append(campaign_id)
        ordinal = len(self.pin_calls)
        return PinnedCampaign(
            campaign_id=self.campaign_id,
            revision=f"{ordinal:040x}",
            tree_sha=f"{ordinal + 100:040x}",
        )

    def read_exact_path(self, pinned, path):
        self.read_paths.append(path)
        return self.records[path]

    def read_exact_campaign_ref(self, campaign_id):
        return {}

    def read_exact_commit(self, campaign_ref, revision):
        return {}

    def compare_ancestry(self, repository_ref, ancestor_revision, descendant_revision):
        return {"relation": "EQUAL"}

    def read_authenticated_commit_author(self, campaign_ref, revision):
        return {}

    def add_record(self, family, identity, record):
        self.records[route_native_record(family, identity).relative_path] = record


class RuntimeLiveTransport:
    def __init__(self, campaign_id="campaign-context"):
        self.campaign_id = campaign_id

    def read_selected_live(self, campaign_id, pinned):
        return LiveRouting(campaign_id=self.campaign_id, entries=())


class RuntimeLiveSourceTransport(RuntimeLiveTransport):
    def __init__(self, campaign_id="campaign-context"):
        super().__init__(campaign_id)
        claims = (LiveClaim.exact_owner("world.scene", "live-scene"),)
        opening_revision = "0" * 40
        epoch_id = derive_live_epoch_id(
            campaign_id, "scene-live", opening_revision, claims
        )
        self.source = LiveEnvelope(
            campaign_id=campaign_id,
            scene_id="scene-live",
            epoch_id=epoch_id,
            source_ref=build_live_ref(campaign_id, "scene-live", epoch_id),
            source_revision="1" * 40,
            claims=claims,
            opening_campaign_revision=opening_revision,
        )
        self.route = LiveRouting(campaign_id=campaign_id, entries=(self.source,))

    def read_selected_live(self, campaign_id, pinned):
        return self.route

    def read_selected_live_source(self, route, source):
        return source.as_mapping()


class MismatchedRuntimeLiveSourceTransport(RuntimeLiveSourceTransport):
    def __init__(self, mismatch):
        super().__init__()
        self.mismatch = mismatch

    def read_selected_live_source(self, route, source):
        result = source.as_mapping()
        if self.mismatch == "source_revision":
            result["source_revision"] = "2" * 40
        elif self.mismatch == "source_ref":
            result["source_ref"] = result["source_ref"] + "/altered"
        elif self.mismatch == "status":
            result["status"] = "CLOSED"
        elif self.mismatch == "opening_campaign_revision":
            result["opening_campaign_revision"] = "1" * 40
        elif self.mismatch == "claims":
            result["claims"] = [
                {
                    "schema_version": 2,
                    "claim_type": "EXACT_OWNER",
                    "native_family": "world.actor",
                    "native_identity": "actor-1",
                }
            ]
        else:
            raise AssertionError(f"unknown LIVE mismatch: {self.mismatch}")
        return result


class TwoSourceSubstitutionRuntimeLiveSourceTransport(RuntimeLiveSourceTransport):
    def __init__(self):
        super().__init__()
        claims = (LiveClaim.exact_owner("world.scene", "live-scene-b"),)
        opening_revision = "0" * 40
        epoch_id = derive_live_epoch_id(
            self.campaign_id, "scene-live-b", opening_revision, claims
        )
        self.substitute = LiveEnvelope(
            campaign_id=self.campaign_id,
            scene_id="scene-live-b",
            epoch_id=epoch_id,
            source_ref=build_live_ref(self.campaign_id, "scene-live-b", epoch_id),
            source_revision="2" * 40,
            claims=claims,
            opening_campaign_revision=opening_revision,
        )
        self.route = LiveRouting(
            campaign_id=self.campaign_id,
            entries=(self.source, self.substitute),
        )

    def read_selected_live_source(self, route, source):
        if source.source_key == self.source.source_key:
            return self.substitute.as_mapping()
        return source.as_mapping()


def host_for(items):
    repository = RuntimeRepository()
    repository.records["LOG/SEMANTIC_EVENTS"] = native_history_window(
        source_revision=f"{1:040x}"
    )
    for item in items:
        family = item.get("owner_family", "world.scene")
        identity = tuple(item.get("owner_identity", [item["candidate_id"]]))
        if family == "world.scene":
            repository.add_record(family, identity, item["payload"])
    return compose_runtime_host("campaign-context", repository, RuntimeLiveTransport())


def assemble_via_host(request_value, items):
    return host_for(items).context.assemble(request_value, items)


def bound_request(**values):
    result = {
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
    result.update(values)
    return result


def owner_candidate(candidate_id, family="world.scene", identity=None, **values):
    result = {
        "candidate_id": candidate_id,
        "channel": "EXPLICIT_REF",
        "role": "NARRATOR",
        "purpose": "narrate",
        "subject_id": "actor.context",
        "recipient_id": "player-1",
        "owner_family": family,
        "owner_identity": list(identity or (candidate_id,)),
        "dependencies": [],
        "rank": 0,
        "payload": {"forged": True},
    }
    result.update(values)
    return result


def collaboration_obligation_mapping(
    *, lifecycle="OPEN", purpose="joint-entry", dependency_scope=None
):
    obligation = CollaborationObligation(
        obligation_id="obligation-1",
        generation=1,
        campaign_id="campaign-context",
        interaction_id="interaction-own",
        intent_plan_id="plan-1",
        clause_id="clause-own",
        semantic_class="ACTIONABLE_INTENT",
        dependency_class=DependencyClass.JOINT_VOLUNTARY_ACTION,
        purpose=purpose,
        dependency_scope=(
            {"scene_id": "scene-1"} if dependency_scope is None else dependency_scope
        ),
        native_basis_refs=(NativeBasisRef("world.scene", "scene-1", "a" * 40),),
        required_contributors=(
            ContributorRef("player-1", "pc-1"),
            ContributorRef("player-2", "pc-2"),
        ),
        lifecycle=lifecycle,
        accepted_input_uses=(
            ("interaction-own", "clause-own"),
            ("interaction-other", "clause-other"),
        ),
        accepted_input_contributors=(
            (
                ("interaction-own", "clause-own"),
                ContributorRef("player-1", "pc-1"),
            ),
            (
                ("interaction-other", "clause-other"),
                ContributorRef("player-2", "pc-2"),
            ),
        ),
        closed_input_set_fingerprint=("b" * 64 if lifecycle == "CLOSED" else None),
    )
    return obligation.to_mapping()


def context_player_record(*, status="active", collaboration_route_refs=None):
    return {
        "kind": "world.player",
        "id": "player-1",
        "player_id": "player-1",
        "campaign_id": "campaign-context",
        "state": {},
        "github_binding": {"user_id": "42", "login": "alice"},
        "status": status,
        "deactivated_by": None,
        "controlled_pc_ids": ["pc-1"],
        "collaboration_route_refs": list(collaboration_route_refs or ()),
    }


def collaboration_candidate(**values):
    candidate_values = {
        "generation": 1,
        "source_frontier": "frontier-1",
        "payload": {
            "lifecycle": "OPEN",
            "private_context": "stale-other-player-private-text",
            "accepted_input_contributors": ["player-2"],
        },
    }
    candidate_values.update(values)
    return owner_candidate(
        "obligation-1",
        "runtime.collaboration_obligation",
        ("obligation-1",),
        channel="ACTIVE_DEPENDENCY",
        **candidate_values,
    )


def collaboration_request(**values):
    request_values = {
        "allowed_channels": ["ACTIVE_DEPENDENCY"],
        "required_ids": ["obligation-1"],
        "allowed_relations": [],
        "source_frontier": "frontier-1",
    }
    request_values.update(values)
    return request(**request_values)


class ContextRuntimeHostTests(unittest.TestCase):
    def _host(self):
        repository = RuntimeRepository()
        repository.add_record(
            "world.scene",
            ("scene-1",),
            {"kind": "world.scene", "id": "scene-1", "state": {"name": "Native"}},
        )
        return compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        ), repository

    def test_context_reloads_native_owner_before_using_candidate(self):
        host, _repository = self._host()

        result = host.context.assemble(
            bound_request(),
            [owner_candidate("scene-1")],
        )

        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(
            result["bundle"]["optional"][0]["payload"]["state"]["name"],
            "Native",
        )

    def test_forged_current_and_eligible_flags_cannot_admit_required_material(self):
        host, _repository = self._host()
        candidate = owner_candidate("scene-1", current=True, eligible=True)

        optional = host.context.assemble(bound_request(), [candidate])
        required = host.context.assemble(
            bound_request(required_ids=["scene-1"]), [candidate]
        )

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_live_candidate_uses_exact_selected_source_body(self):
        repository = RuntimeRepository()
        live = RuntimeLiveSourceTransport()
        host = compose_runtime_host("campaign-context", repository, live)
        candidate = owner_candidate(
            "live-1",
            "LIVE",
            ("campaign-context", "scene-live", live.source.epoch_id),
            channel="LIVE_CURRENT",
            source_key=list(live.source.source_key),
        )

        result = host.context.assemble(
            bound_request(
                allowed_channels=["LIVE_CURRENT"],
                max_candidates=1,
                required_ids=["live-1"],
            ),
            [candidate],
        )

        self.assertEqual(result["outcome"], "ASSEMBLED")
        self.assertEqual(
            result["bundle"]["required"][0]["payload"]["source_ref"],
            live.source.source_ref,
        )

    def test_registered_campaign_family_requires_complete_scope_binding(self):
        host, _repository = self._host()
        expected = {
            "role": "NARRATOR",
            "purpose": "narrate",
            "subject_id": "actor.context",
            "recipient_id": "player-1",
        }

        valid = owner_candidate("scene-1", **expected)
        self.assertEqual(
            host.context.assemble(bound_request(), [valid])["outcome"], "ASSEMBLED"
        )

        for field, expected_value in expected.items():
            with self.subTest(binding=field, state="missing"):
                missing = dict(valid)
                missing.pop(field)
                optional = host.context.assemble(bound_request(), [missing])
                required = host.context.assemble(
                    bound_request(required_ids=["scene-1"]), [missing]
                )
                self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
                self.assertEqual(optional["bundle"]["optional"], [])
                self.assertEqual(required["outcome"], "UNSATISFIABLE")

            with self.subTest(binding=field, state="wrong"):
                wrong = dict(valid)
                wrong[field] = expected_value + "-wrong"
                optional = host.context.assemble(bound_request(), [wrong])
                required = host.context.assemble(
                    bound_request(required_ids=["scene-1"]), [wrong]
                )
                self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
                self.assertEqual(optional["bundle"]["optional"], [])
                self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_catalog_family_without_registered_resolver_is_not_eligible(self):
        repository = RuntimeRepository()
        repository.add_record(
            "runtime.interaction",
            ("interaction-1",),
            {"kind": "runtime.interaction", "id": "interaction-1"},
        )
        host = compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        )
        item = owner_candidate("interaction-1", "runtime.interaction")

        optional = host.context.assemble(bound_request(), [item])
        required = host.context.assemble(
            bound_request(required_ids=["interaction-1"]), [item]
        )
        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_live_reader_mismatch_degrades_optional_and_blocks_required(self):
        candidate = owner_candidate(
            "live-1",
            "LIVE",
            ("campaign-context", "scene-live", "placeholder"),
            channel="LIVE_CURRENT",
        )
        for mismatch in (
            "source_revision",
            "source_ref",
            "status",
            "opening_campaign_revision",
            "claims",
        ):
            with self.subTest(mismatch=mismatch):
                live = MismatchedRuntimeLiveSourceTransport(mismatch)
                candidate["owner_identity"] = [
                    "campaign-context",
                    "scene-live",
                    live.source.epoch_id,
                ]
                candidate["source_key"] = list(live.source.source_key)
                host = compose_runtime_host(
                    "campaign-context", RuntimeRepository(), live
                )
                optional = host.context.assemble(
                    bound_request(allowed_channels=["LIVE_CURRENT"]), [candidate]
                )
                required = host.context.assemble(
                    bound_request(
                        allowed_channels=["LIVE_CURRENT"], required_ids=["live-1"]
                    ),
                    [candidate],
                )
                self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
                self.assertEqual(optional["bundle"]["optional"], [])
                self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_live_reader_cannot_substitute_another_selected_source(self):
        repository = RuntimeRepository()
        live = TwoSourceSubstitutionRuntimeLiveSourceTransport()
        host = compose_runtime_host("campaign-context", repository, live)
        candidate = owner_candidate(
            "live-a",
            "LIVE",
            ("campaign-context", "scene-live", live.source.epoch_id),
            channel="LIVE_CURRENT",
            source_key=list(live.source.source_key),
        )

        optional = host.context.assemble(
            bound_request(allowed_channels=["LIVE_CURRENT"]), [candidate]
        )
        required = host.context.assemble(
            bound_request(allowed_channels=["LIVE_CURRENT"], required_ids=["live-a"]),
            [candidate],
        )

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_wrong_registered_role_purpose_and_unknown_profile_fail_closed(self):
        host, _repository = self._host()

        for request_value in (
            bound_request(role="ACTOR"),
            bound_request(purpose="assess"),
            bound_request(profile_id="profile.unknown"),
        ):
            with (
                self.subTest(request=request_value),
                self.assertRaises(context_runtime.ContextContractError),
            ):
                host.context.assemble(request_value, [])

    def test_unsupported_family_is_degraded_or_terminal(self):
        host, _repository = self._host()
        candidate = owner_candidate("mystery-1", "runtime.mystery", ("mystery-1",))

        optional = host.context.assemble(bound_request(), [candidate])
        required = host.context.assemble(
            bound_request(required_ids=["mystery-1"]), [candidate]
        )

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_context_schema_and_module_contract_are_registered(self):
        schema = json.loads(
            (SCHEMAS / "context-need-profile.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator(schema).validate(bound_request())
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(
                {key: value for key, value in bound_request().items() if key != "role"}
            )
        self.assertEqual(context_runtime.FRAMEWORK_MODULE_VERSION, "1.0.8")


class ContextDiscoveryTests(unittest.TestCase):
    def test_duplicate_candidate_identity_is_rejected_not_silently_overwritten(self):
        request = {
            "profile_id": "profile.narration",
            "allowed_channels": ["EXPLICIT_REF"],
            "max_candidates": 2,
        }
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.discover_candidates(
                request, [candidate("same"), candidate("same")]
            )

    def test_discovery_uses_only_registered_bounded_channels(self):
        request = {
            "profile_id": "profile.narration",
            "allowed_channels": ["EXPLICIT_REF"],
            "max_candidates": 1,
        }
        found = context_runtime.discover_candidates(
            request, [candidate("b", channel="HISTORY_HINT"), candidate("a")]
        )
        self.assertEqual([item["candidate_id"] for item in found], ["a"])


class ContextEligibilityTests(unittest.TestCase):
    def test_ineligible_or_stale_candidate_is_not_role_evidence(self):
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("secret", eligible=False))
        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.resolve_candidate_basis(candidate("stale", current=False))


class RequiredPacketClosureTests(unittest.TestCase):
    def test_unsatisfiable_closure_terminates_before_optional_owner_reads(self):
        repository = RuntimeRepository()
        root = candidate("root", depends_on=("missing",))
        optional = candidate("optional")
        for item in (root, optional):
            repository.add_record(
                "world.scene", (item["candidate_id"],), item["payload"]
            )
        host = compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        )

        result = host.context.assemble(
            request(
                required_ids=["root"],
                allowed_relations=["requires"],
            ),
            [root, optional],
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertNotIn(
            route_native_record("world.scene", ("optional",)).relative_path,
            repository.read_paths,
        )

    def test_unregistered_dependency_relation_is_rejected(self):
        request_value = request(
            required_ids=["root"], allowed_relations=[], budget=1000
        )
        with self.assertRaises(context_runtime.ContextContractError):
            assemble_via_host(
                request_value, [candidate("root", depends_on=("secret",))]
            )

    def test_required_dependency_closure_precedes_optional_allocation(self):
        root, dependency, optional = (
            candidate("root", required=True, size=10, depends_on=("dependency",)),
            candidate("dependency", required=True, size=10),
            candidate("optional", rank=99, size=10),
        )
        request_value = request(
            required_ids=["root"],
            allowed_relations=["requires"],
            budget=budget_for(root, dependency) + 1,
        )
        result = assemble_via_host(request_value, [root, dependency, optional])
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(
            [item["candidate_id"] for item in result["bundle"]["required"]],
            ["dependency", "root"],
        )

    def test_missing_required_closure_is_terminal_unsatisfiable(self):
        root = candidate("root", required=True, depends_on=("missing",))
        request_value = request(
            required_ids=["root"],
            allowed_relations=["requires"],
            budget=budget_for(root),
        )
        result = assemble_via_host(request_value, [root])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_ineligible_required_closure_is_terminal_unsatisfiable(self):
        required = candidate("required", eligible=False)
        request_value = request(
            required_ids=["required"], allowed_relations=[], budget=budget_for(required)
        )
        result = assemble_via_host(request_value, [required])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")

    def test_relation_bearing_profile_requires_admitted_typed_relations(self):
        root = candidate("root", depends_on=("dependency",))
        request_value = request(
            required_ids=["root"], allowed_relations=[], budget=budget_for(root)
        )
        with self.assertRaises(context_runtime.ContextContractError):
            assemble_via_host(request_value, [root])


class ContextAllocationTests(unittest.TestCase):
    def test_bound_context_rejects_caller_supplied_size(self):
        item = candidate("sized")
        item["size"] = 1
        optional = assemble_via_host(request(), [item])
        required = assemble_via_host(request(required_ids=["sized"]), [item])

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_declared_negative_size_cannot_bypass_actual_allocation(self):
        with self.assertRaises(ContextBudgetError):
            allocate([], [{"candidate_id": "bad", "size": -100}], 0)

    def test_direct_allocator_rejects_malformed_rank(self):
        with self.assertRaises(ContextBudgetError):
            allocate(
                [],
                [{"candidate_id": "bad", "payload": {}, "rank": "highest"}],
                100,
            )

    def test_central_estimator_counts_utf8_when_no_owner_size_is_declared(self):
        self.assertEqual(estimate_size("ё"), 4)

    def test_required_floor_cannot_be_evicted_by_optional_material(self):
        optional, required = (
            candidate("optional", rank=100, size=10),
            candidate("required", required=True, size=10),
        )
        request_value = request(
            required_ids=["required"], allowed_relations=[], budget=budget_for(required)
        )
        result = assemble_via_host(request_value, [optional, required])
        self.assertEqual(
            [item["candidate_id"] for item in result["bundle"]["required"]],
            ["required"],
        )
        self.assertEqual(result["bundle"]["optional"], [])


class OptionalRankingTests(unittest.TestCase):
    def test_optional_rank_must_be_an_integer(self):
        item = candidate("malformed-rank")
        item["rank"] = "highest"

        result = assemble_via_host(request(), [item])

        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(result["bundle"]["optional"], [])
        self.assertEqual(result["trace"]["excluded_ids"], ["malformed-rank"])

    def test_optional_ranking_is_deterministic_within_remaining_budget(self):
        a, b, c = candidate("a", rank=2), candidate("b", rank=2), candidate("c", rank=1)
        request_value = request(
            required_ids=[], allowed_relations=[], budget=budget_for(a, b)
        )
        result = assemble_via_host(request_value, [b, a, c])
        self.assertEqual(
            [item["candidate_id"] for item in result["bundle"]["optional"]], ["a", "b"]
        )


class RetrospectiveContextTests(unittest.TestCase):
    def test_retrospective_is_terminal_without_calling_history_route(self):
        repository = RuntimeRepository()
        repository.records["LOG/SEMANTIC_EVENTS"] = native_history_window(
            source_revision=f"{1:040x}"
        )
        host = compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        )
        item = owner_candidate(
            "event-1",
            "runtime.semantic_event",
            ("event-1",),
            channel="HISTORY_HINT",
            role="CHRONICLER",
            purpose="chronicle",
        )

        result = host.context.assemble(
            request(
                profile_id="profile.story",
                role="CHRONICLER",
                purpose="chronicle",
                allowed_channels=["HISTORY_HINT"],
                required_ids=["event-1"],
                retrospective=True,
            ),
            [item],
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])
        self.assertEqual(repository.read_paths, [])

    def test_stale_or_unavailable_retrospective_native_evidence_is_terminal(self):
        for state in ("stale", "unavailable"):
            with self.subTest(state=state):
                repository = RuntimeRepository()
                if state == "stale":
                    repository.records["LOG/SEMANTIC_EVENTS"] = native_history_window(
                        source_revision="f" * 40
                    )
                host = compose_runtime_host(
                    "campaign-context", repository, RuntimeLiveTransport()
                )
                item = owner_candidate(
                    "event-1",
                    "runtime.semantic_event",
                    ("event-1",),
                    channel="HISTORY_HINT",
                    role="CHRONICLER",
                    purpose="chronicle",
                )

                result = host.context.assemble(
                    request(
                        profile_id="profile.story",
                        role="CHRONICLER",
                        purpose="chronicle",
                        allowed_channels=["HISTORY_HINT"],
                        required_ids=["event-1"],
                        retrospective=True,
                    ),
                    [item],
                )

                self.assertEqual(result["outcome"], "UNSATISFIABLE")
                self.assertIsNone(result["bundle"])
                self.assertEqual(repository.read_paths, [])

    def test_owner_payload_estimation_failure_degrades_optional_and_terminalizes_required(
        self,
    ):
        repository = RuntimeRepository()
        malformed_payload = {
            "kind": "world.scene",
            "id": "malformed",
            "state": {"not_json": object()},
        }
        repository.add_record("world.scene", ("malformed",), malformed_payload)
        host = compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        )
        item = owner_candidate("malformed")

        optional = host.context.assemble(request(), [item])
        required = host.context.assemble(request(required_ids=["malformed"]), [item])

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")
        self.assertIsNone(required["bundle"])

    def test_retrospective_projection_is_unavailable_until_native_route_is_admitted(
        self,
    ):
        item = owner_candidate(
            "event-1",
            "runtime.semantic_event",
            ("event-1",),
            channel="HISTORY_HINT",
            role="CHRONICLER",
            purpose="chronicle",
        )
        request_value = request(
            profile_id="profile.story",
            role="CHRONICLER",
            purpose="chronicle",
            allowed_channels=["HISTORY_HINT"],
            required_ids=["event-1"],
            allowed_relations=[],
            budget=1000,
            retrospective=True,
        )
        result = assemble_via_host(request_value, [item])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
    def test_native_private_routing_payload_is_not_role_evidence(self):
        repository = RuntimeRepository()
        repository.add_record(
            "world.scene",
            ("private-scene",),
            {
                "kind": "world.scene",
                "id": "private-scene",
                "state": {"name": "Native"},
                "routing": {"private": "operator-only"},
            },
        )
        host = compose_runtime_host(
            "campaign-context", repository, RuntimeLiveTransport()
        )
        item = owner_candidate("private-scene")

        optional = host.context.assemble(request(), [item])
        required = host.context.assemble(
            request(required_ids=["private-scene"]), [item]
        )

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_context_trace_carrier_is_not_role_evidence(self):
        item = candidate("trace-carrier")
        item["context_trace"] = {"private": "routing-only"}

        optional = assemble_via_host(request(), [item])
        required = assemble_via_host(request(required_ids=["trace-carrier"]), [item])

        self.assertEqual(optional["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual(optional["bundle"]["optional"], [])
        self.assertEqual(required["outcome"], "UNSATISFIABLE")

    def test_trace_is_diagnostic_and_does_not_include_payload(self):
        item = candidate("a")
        request_value = request(
            required_ids=[], allowed_relations=[], budget=budget_for(item)
        )
        result = assemble_via_host(request_value, [item])
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
            context_runtime.scoped_context_join(
                bundle,
                {
                    "profile_id": "profile.actor",
                    "source_frontier": "frontier-1",
                    "recipient_id": "player-1",
                },
            )

    def test_frontier_mismatch_is_rejected(self):
        bundle = {
            "profile_id": "profile.narration",
            "role": "NARRATOR",
            "purpose": "narrate",
            "subject_id": "actor.context",
            "source_frontier": "frontier-1",
            "recipient_id": "player-1",
        }

        with self.assertRaises(context_runtime.ContextContractError):
            context_runtime.scoped_context_join(
                bundle, bundle | {"source_frontier": "frontier-stale"}
            )

    def test_context_schemas_are_strict_and_examples_validate(self):
        for name in ("context-need-profile.schema.json", "context-trace.schema.json"):
            schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            for example in schema["examples"]:
                Draft202012Validator(schema).validate(example)
        profile_schema = json.loads(
            (SCHEMAS / "context-need-profile.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("allowed_relations", profile_schema["required"])
        Draft202012Validator(profile_schema).validate(
            request(
                max_candidates=1,
                required_ids=[],
                allowed_relations=["requires"],
                budget=10,
            )
        )
        with self.assertRaises(ValidationError):
            Draft202012Validator(profile_schema).validate(
                {
                    **request(
                        max_candidates=1,
                        required_ids=[],
                        allowed_relations=["requires"],
                        budget=10,
                    ),
                    "allowed_relations": [1],
                }
            )


class CollaborationContextJoinTests(unittest.TestCase):
    def _host(
        self,
        *,
        lifecycle="OPEN",
        player_status="active",
        route=True,
        purpose="joint-entry",
        dependency_scope=None,
    ):
        repository = RuntimeRepository()
        route_refs = (
            [{"obligation_id": "obligation-1", "generation": 1}] if route else []
        )
        repository.add_record(
            "world.player",
            ("player-1",),
            context_player_record(
                status=player_status,
                collaboration_route_refs=route_refs,
            ),
        )
        repository.add_record(
            "runtime.collaboration_obligation",
            ("obligation-1",),
            collaboration_obligation_mapping(
                lifecycle=lifecycle,
                purpose=purpose,
                dependency_scope=dependency_scope,
            ),
        )
        return (
            compose_runtime_host(
                "campaign-context", repository, RuntimeLiveTransport()
            ),
            repository,
        )

    def test_current_obligation_join_projects_only_the_recipient_safe_summary(self):
        host, repository = self._host(
            purpose="joint-entry at cobalt-archive-17",
            dependency_scope={
                "scene_id": "scene-1",
                "annotation": "cobalt-archive-17",
            },
        )
        candidate_value = collaboration_candidate()

        result = host.context.assemble(collaboration_request(), [candidate_value])

        self.assertEqual(result["outcome"], "ASSEMBLED")
        summary = result["bundle"]["required"][0]["payload"]
        self.assertEqual(summary["obligation_id"], "obligation-1")
        self.assertEqual(summary["generation"], 1)
        self.assertEqual(summary["lifecycle"], "OPEN")
        self.assertNotIn("purpose", summary)
        self.assertNotIn("dependency_scope", summary)
        self.assertEqual(
            summary["recipient_requirement"],
            {
                "player_id": "player-1",
                "required": True,
                "input_status": "RECEIVED",
            },
        )
        bundle_text = json.dumps(result["bundle"], sort_keys=True)
        for private_value in (
            "player-2",
            "interaction-other",
            "clause-other",
            "stale-other-player-private-text",
            "cobalt-archive-17",
        ):
            self.assertNotIn(private_value, bundle_text)
        self.assertIn(
            route_native_record("world.player", ("player-1",)).relative_path,
            repository.read_paths,
        )
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation", ("obligation-1",)
            ).relative_path,
            repository.read_paths,
        )

    def test_retrospective_context_revalidates_current_obsolete_obligation(self):
        host, repository = self._host(lifecycle="OBSOLETE", route=True)
        candidate_value = collaboration_candidate()

        result = host.context.assemble(
            collaboration_request(retrospective=True), [candidate_value]
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])
        self.assertIn(
            route_native_record("world.player", ("player-1",)).relative_path,
            repository.read_paths,
        )
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation", ("obligation-1",)
            ).relative_path,
            repository.read_paths,
        )
        result_text = json.dumps(result, sort_keys=True)
        self.assertNotIn("stale-other-player-private-text", result_text)

    def test_unhashable_current_obligation_lifecycle_fails_closed(self):
        host, repository = self._host()
        obligation_path = route_native_record(
            "runtime.collaboration_obligation", ("obligation-1",)
        ).relative_path
        repository.records[obligation_path] = {
            **repository.records[obligation_path],
            "lifecycle": [],
        }

        result = host.context.assemble(
            collaboration_request(), [collaboration_candidate()]
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_access_change_removed_route_ref_rejects_open_obligation(self):
        host, repository = self._host(lifecycle="OPEN", route=False)

        result = host.context.assemble(
            collaboration_request(), [collaboration_candidate()]
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])
        self.assertIn(
            route_native_record("world.player", ("player-1",)).relative_path,
            repository.read_paths,
        )
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation", ("obligation-1",)
            ).relative_path,
            repository.read_paths,
        )

    def test_candidate_owner_generation_mismatch_is_rejected(self):
        host, repository = self._host()

        result = host.context.assemble(
            collaboration_request(),
            [collaboration_candidate(generation=2)],
        )

        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])
        self.assertIn(
            route_native_record("world.player", ("player-1",)).relative_path,
            repository.read_paths,
        )
        self.assertIn(
            route_native_record(
                "runtime.collaboration_obligation", ("obligation-1",)
            ).relative_path,
            repository.read_paths,
        )

    def test_scope_and_frontier_mismatch_cannot_admit_obligation(self):
        mismatches = (
            (
                collaboration_candidate(recipient_id="player-2"),
                collaboration_request(),
            ),
            (
                collaboration_candidate(role="ACTOR", purpose="assess"),
                collaboration_request(),
            ),
            (
                collaboration_candidate(source_frontier="frontier-stale"),
                collaboration_request(),
            ),
        )
        for candidate_value, request_value in mismatches:
            with self.subTest(candidate=candidate_value, request=request_value):
                host, _repository = self._host()
                result = host.context.assemble(request_value, [candidate_value])
                self.assertEqual(result["outcome"], "UNSATISFIABLE")
                self.assertIsNone(result["bundle"])


if __name__ == "__main__":
    unittest.main()
