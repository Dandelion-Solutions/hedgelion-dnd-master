import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

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


class RuntimeRepository:
    def __init__(self, campaign_id="campaign-context"):
        self.campaign_id = campaign_id
        self.records = {}
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
        self.assertEqual(host.context.assemble(bound_request(), [valid])["outcome"], "ASSEMBLED")

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
        self.assertEqual(context_runtime.FRAMEWORK_MODULE_VERSION, "1.0.4")


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
    def test_declared_negative_size_cannot_bypass_actual_allocation(self):
        with self.assertRaises(ContextBudgetError):
            allocate([], [{"candidate_id": "bad", "size": -100}], 0)

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
    def test_retrospective_payload_is_explicitly_a_projection(self):
        item = candidate("story-1", channel="HISTORY_HINT")
        request_value = request(
            profile_id="profile.story",
            role="CHRONICLER",
            purpose="chronicle",
            allowed_channels=["HISTORY_HINT"],
            required_ids=[],
            allowed_relations=[],
            budget=budget_for(item),
            retrospective=True,
        )
        result = assemble_via_host(request_value, [item])
        self.assertTrue(result["bundle"]["retrospective_projection"])
        self.assertNotIn("gameplay_truth", result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
