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
from GAME.TOOLS.access_control import (
    PlayerRecord,
    PlayerResolution,
    VerifiedPrincipal,
    build_principal_player_route,
    resolve_player,
)
from GAME.TOOLS.information import extract_material_live_information
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveEnvelope,
    build_live_ref,
    build_live_route,
    derive_live_epoch_id,
)


def candidate(candidate_id, *, channel="EXPLICIT_REF", required=False, rank=0, size=10, eligible=None, current=None, depends_on=()):
    dependencies = [{"relation": "requires", "candidate_id": item} for item in depends_on]
    result = {"candidate_id": candidate_id, "channel": channel, "required": required, "rank": rank, "dependencies": dependencies, "payload": {"ref": candidate_id, "text": "x" * size}}
    if eligible is not None:
        result["eligible"] = eligible
    if current is not None:
        result["current"] = current
    return result


def make_request(**values):
    values.setdefault("profile_id", "profile.narration")
    values.setdefault("allowed_relations", ["requires"])
    values.setdefault("role_id", "role.narrator")
    values.setdefault("purpose", "context-test")
    values.setdefault("recipient_id", "player-1")
    return values


def budget_for(*items):
    total = 0
    for item in items:
        try:
            payload = context_runtime.resolve_candidate_basis(
                item,
                owner_input=owner_input(item["candidate_id"]),
                request=make_request(),
            )["payload"]
        except context_runtime.ContextContractError:
            payload = item["payload"]
        total += estimate_size(payload)
    return total


def owner_input(candidate_id, *, recipient="player-1", player_status="active"):
    claims = (LiveClaim.exact_owner("world.actor", "actor.context"),)
    scene_id = f"scene-{candidate_id}"
    epoch_id = derive_live_epoch_id(
        "campaign-context", scene_id, "0" * 40, claims
    )
    source = LiveEnvelope(
        campaign_id="campaign-context",
        scene_id=scene_id,
        epoch_id=epoch_id,
        source_ref=build_live_ref("campaign-context", scene_id, epoch_id),
        source_revision="a" * 40,
        claims=claims,
        opening_campaign_revision="0" * 40,
    )
    projection = {
        "source_key": list(source.source_key),
        "source_ref": source.source_ref,
        "source_revision": source.source_revision,
        "source_native_ids": list(source.source_native_ids),
        "information_candidates": [
            {
                "recipient_player_id": recipient,
                "evidence": {
                    "fact": {
                        "fact_id": candidate_id,
                        "statement": f"Native {candidate_id}.",
                        "truth_status": "truth.established",
                        "record_status": "lore_record.active",
                        "provenance_refs": [f"source.{candidate_id}"],
                    },
                    "knowledge": {
                        "knower_id": "actor.context",
                        "fact_id": candidate_id,
                        "stance": "epistemic.known",
                        "supporting_source_refs": [f"source.{candidate_id}"],
                        "source_evidence": [
                            {
                                "ref": f"source.{candidate_id}",
                                "accepted": True,
                                "current": True,
                                "authorized_knower_ids": ["actor.context"],
                            }
                        ],
                    },
                    "emission": {
                        "message_id": f"message.{candidate_id}",
                        "interaction_id": f"interaction.{candidate_id}",
                        "recipient_player_id": recipient,
                        "text": f"Native {candidate_id}.",
                        "source_evidence": [
                            {
                                "ref": f"source.{candidate_id}",
                                "accepted": True,
                                "current": True,
                                "fact_id": candidate_id,
                            }
                        ],
                        "disclosure_refs": [
                            {
                                "fact_id": candidate_id,
                                "aspect": "disclosure.statement",
                                "source_ref": f"source.{candidate_id}",
                            }
                        ],
                    },
                },
            }
        ],
    }
    live_route = build_live_route(source.campaign_id, (source,))
    principal = VerifiedPrincipal(stable_account_id="context-account", login="context")
    player_route = build_principal_player_route(
        source.campaign_id,
        (
            PlayerRecord(
                player_id=recipient,
                stable_account_id=principal.stable_account_id,
                login="context",
                status=player_status,
                deactivated_by=None if player_status == "active" else "self",
            ),
        ),
    )
    resolution = resolve_player(
        principal,
        player_route,
        lambda player_id: PlayerRecord(
            player_id=player_id,
            stable_account_id=principal.stable_account_id,
            login="context",
            status=player_status,
            deactivated_by=None if player_status == "active" else "self",
        ),
        campaign_id=source.campaign_id,
    )
    [information_candidate] = extract_material_live_information(
        live_route,
        source,
        projection,
        recipient_player_id=recipient,
    )
    return context_runtime.ContextOwnerInput(
        candidate_id=candidate_id,
        live_route=live_route,
        live_source=source,
        live_projection=projection,
        information_candidate=information_candidate,
        player_resolution=resolution,
    )


def owner_inputs_for(*items):
    return tuple(owner_input(item["candidate_id"]) for item in items)


class OwnerRoutedContextAdmissionTests(unittest.TestCase):
    def test_context_assembly_requires_registered_scope(self):
        with self.assertRaisesRegex(context_runtime.ContextContractError, "role, purpose and recipient"):
            context_runtime.assemble_context(
                {"profile_id": "profile.narration", "allowed_channels": ["EXPLICIT_REF"], "max_candidates": 1, "required_ids": [], "allowed_relations": [], "budget": 10},
                [],
            )

    def test_caller_flags_cannot_admit_without_native_owner_basis(self):
        item = candidate("forged", eligible=True, current=True)
        with self.assertRaisesRegex(context_runtime.ContextContractError, "owner"):
            context_runtime.resolve_candidate_basis(item, request=make_request())

    def test_registered_profile_rejects_caller_role_or_purpose(self):
        item = candidate("wrong-scope")
        with self.assertRaisesRegex(context_runtime.ContextContractError, "registered"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=owner_input("wrong-scope"),
                request=make_request(role_id="role.actor"),
            )

    def test_complete_native_owner_basis_admits_post_resolution_flags(self):
        item = candidate("native")
        item["payload"] = {"forged": "caller material"}
        admitted = context_runtime.resolve_candidate_basis(
            item,
            owner_input=owner_input("native"),
            request=make_request(),
        )
        self.assertTrue(admitted["current"])
        self.assertTrue(admitted["eligible"])
        self.assertEqual(admitted["candidate_id"], "native")
        self.assertEqual(admitted["payload"]["lore_fact"]["fact_id"], "native")
        self.assertNotIn("forged", admitted["payload"])

    def test_caller_cannot_widen_registered_profile_limits(self):
        item = candidate("widened")
        with self.assertRaisesRegex(context_runtime.ContextContractError, "registered profile"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=owner_input("widened"),
                request=make_request(allowed_channels=["UNREGISTERED_CHANNEL"]),
            )

    def test_stale_live_source_cannot_admit_a_candidate(self):
        item = candidate("stale-live")
        basis = owner_input("stale-live")
        stale_source = LiveEnvelope(
            campaign_id=basis.live_source.campaign_id,
            scene_id=basis.live_source.scene_id,
            epoch_id=basis.live_source.epoch_id,
            source_ref=basis.live_source.source_ref,
            source_revision="b" * 40,
            claims=basis.live_source.claims,
            opening_campaign_revision=basis.live_source.opening_campaign_revision,
        )
        forged = context_runtime.ContextOwnerInput(
            candidate_id=basis.candidate_id,
            live_route=basis.live_route,
            live_source=stale_source,
            live_projection=basis.live_projection,
            information_candidate=basis.information_candidate,
            player_resolution=basis.player_resolution,
        )
        with self.assertRaisesRegex(context_runtime.ContextContractError, "stale|current"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=forged,
                request=make_request(),
            )

    def test_forged_player_resolution_cannot_admit_a_candidate(self):
        item = candidate("stale-player")
        basis = owner_input("stale-player")
        forged = context_runtime.ContextOwnerInput(
            candidate_id=basis.candidate_id,
            live_route=basis.live_route,
            live_source=basis.live_source,
            live_projection=basis.live_projection,
            information_candidate=basis.information_candidate,
            player_resolution=PlayerResolution(
                status="AUTHORIZED_PLAYER",
                player=PlayerRecord(
                    player_id="player-1",
                    stable_account_id="context-account",
                    login="context",
                    status="active",
                    deactivated_by=None,
                ),
            ),
        )
        with self.assertRaisesRegex(context_runtime.ContextContractError, "owner-issued"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=forged,
                request=make_request(),
            )

    def test_inactive_player_resolution_cannot_admit_a_candidate(self):
        item = candidate("inactive-player")
        with self.assertRaisesRegex(context_runtime.ContextContractError, "PLAYER resolution"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=owner_input("inactive-player", player_status="inactive"),
                request=make_request(),
            )

    def test_physical_co_presence_does_not_widen_recipient_scope(self):
        item = candidate("private")
        with self.assertRaisesRegex(context_runtime.ContextContractError, "recipient|PLAYER"):
            context_runtime.resolve_candidate_basis(
                item,
                owner_input=owner_input("private", recipient="player-1"),
                request=make_request(recipient_id="player-2"),
            )

    def test_index_scene_cache_presence_without_owner_route_fails_closed(self):
        item = candidate("routing-only", channel="INDEX_LOOKUP")
        item.update({"scene_present": True, "index_present": True, "cache_present": True})
        with self.assertRaisesRegex(context_runtime.ContextContractError, "owner"):
            context_runtime.resolve_candidate_basis(item, request=make_request())

    def test_required_candidate_without_exact_owner_route_is_terminal(self):
        item = candidate("unrouted")
        result = context_runtime.assemble_context(
            make_request(
                allowed_channels=["EXPLICIT_REF"],
                max_candidates=1,
                required_ids=["unrouted"],
                allowed_relations=[],
                budget=100,
            ),
            [item],
        )
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_mapping_or_subclass_owner_carrier_cannot_mint_admission(self):
        item = candidate("carrier")
        basis = owner_input("carrier")

        class ForgedOwnerInput(context_runtime.ContextOwnerInput):
            pass

        for forged in (
            {"candidate_id": "carrier", "current": True, "eligible": True},
            ForgedOwnerInput(
                candidate_id=basis.candidate_id,
                live_route=basis.live_route,
                live_source=basis.live_source,
                live_projection=basis.live_projection,
                information_candidate=basis.information_candidate,
                player_resolution=basis.player_resolution,
            ),
        ):
            with self.subTest(type=type(forged).__name__):
                with self.assertRaisesRegex(context_runtime.ContextContractError, "owner input"):
                    context_runtime.resolve_candidate_basis(
                        item,
                        owner_input=forged,
                        request=make_request(),
                    )


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
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=["root"], allowed_relations=[], budget=25)
        with self.assertRaises(context_runtime.ContextContractError):
            root = candidate("root", depends_on=("secret",))
            context_runtime.assemble_context(request, [root], owner_inputs=owner_inputs_for(root))
    def test_required_dependency_closure_precedes_optional_allocation(self):
        root, dependency, optional = candidate("root", required=True, size=10, depends_on=("dependency",)), candidate("dependency", required=True, size=10), candidate("optional", rank=99, size=10)
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=["root"], allowed_relations=["requires"], budget=budget_for(root, dependency) + 1)
        result = context_runtime.assemble_context(request, [root, dependency, optional], owner_inputs=owner_inputs_for(root, dependency, optional))
        self.assertEqual(result["outcome"], "ASSEMBLED_DEGRADED")
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["dependency", "root"])

    def test_missing_required_closure_is_terminal_unsatisfiable(self):
        root = candidate("root", required=True, depends_on=("missing",))
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=["root"], allowed_relations=["requires"], budget=budget_for(root))
        result = context_runtime.assemble_context(request, [root])
        self.assertEqual(result["outcome"], "UNSATISFIABLE")
        self.assertIsNone(result["bundle"])

    def test_ineligible_required_closure_is_terminal_unsatisfiable(self):
        required = candidate("required", eligible=False)
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=["required"], allowed_relations=[], budget=budget_for(required))
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
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=["required"], allowed_relations=[], budget=budget_for(required))
        result = context_runtime.assemble_context(request, [optional, required], owner_inputs=owner_inputs_for(optional, required))
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["required"]], ["required"])
        self.assertEqual(result["bundle"]["optional"], [])


class OptionalRankingTests(unittest.TestCase):
    def test_optional_ranking_is_deterministic_within_remaining_budget(self):
        a, b, c = candidate("a", rank=2), candidate("b", rank=2), candidate("c", rank=1)
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=5, required_ids=[], allowed_relations=[], budget=budget_for(a, b))
        result = context_runtime.assemble_context(request, [b, a, c], owner_inputs=owner_inputs_for(a, b, c))
        self.assertEqual([item["candidate_id"] for item in result["bundle"]["optional"]], ["a", "b"])


class RetrospectiveContextTests(unittest.TestCase):
    def test_retrospective_payload_is_explicitly_a_projection(self):
        item = candidate("story-1", channel="HISTORY_HINT")
        request = make_request(profile_id="profile.commentator", allowed_channels=["HISTORY_HINT"], max_candidates=2, required_ids=[], allowed_relations=[], budget=budget_for(item), retrospective=True, role_id="role.commentator", purpose="commentary")
        result = context_runtime.assemble_context(request, [item], owner_inputs=owner_inputs_for(item))
        self.assertTrue(result["bundle"]["retrospective_projection"])
        self.assertNotIn("gameplay_truth", result["bundle"])


class ContextResultTraceTests(unittest.TestCase):
    def test_trace_is_diagnostic_and_does_not_include_payload(self):
        item = candidate("a")
        request = make_request(profile_id="profile.narration", allowed_channels=["EXPLICIT_REF"], max_candidates=2, required_ids=[], allowed_relations=[], budget=budget_for(item))
        result = context_runtime.assemble_context(request, [item], owner_inputs=owner_inputs_for(item))
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
