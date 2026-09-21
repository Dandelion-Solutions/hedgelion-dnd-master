"""W04.T01A collaboration admission over accepted Interaction/IntentPlan owners."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from GAME.TOOLS.access_control import PlayerRecord, VerifiedPrincipal, build_principal_player_route
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionError,
    CoordinationFamily,
    DependencyClass,
    classify_coordination_dependency,
    open_or_successor_obligation,
)
from GAME.TOOLS.native_storage import route_native_record
from GAME.TOOLS.policy_basis import PinnedCampaign


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
CAMPAIGN_ID = "campaign-frostfall"
CAMPAIGN_REVISION = "a" * 40
TREE_SHA = "b" * 40


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in document:
            registry = registry.with_resource(document["$id"], Resource.from_contents(document))
    return registry


class FakeRepository:
    """Host-injected exact-read capability used by the admission integration tests."""

    def __init__(self, *, clause: dict[str, object] | None = None) -> None:
        self.reads: list[str] = []
        self.records: dict[str, object] = {}
        self._install_records(clause or _collective_clause())

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if campaign_id != CAMPAIGN_ID:
            raise KeyError(campaign_id)
        return PinnedCampaign(campaign_id=campaign_id, revision=CAMPAIGN_REVISION, tree_sha=TREE_SHA)

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        if pinned.campaign_id != CAMPAIGN_ID or pinned.revision != CAMPAIGN_REVISION:
            raise KeyError("stale pin")
        self.reads.append(path)
        return copy.deepcopy(self.records[path])

    def _install_records(self, clause: dict[str, object]) -> None:
        interaction_path = route_native_record("runtime.interaction", ("interaction-1",)).relative_path
        plan_path = route_native_record("runtime.intent_plan", ("plan-1",)).relative_path
        self.records[interaction_path] = {
            "kind": "runtime.interaction",
            "id": "interaction-1",
            "campaign_id": CAMPAIGN_ID,
            "session_id": "session-1",
            "player_id": "player-alice",
            "input_message_id": "message-1",
            "intent_plan_id": "plan-1",
        }
        self.records[plan_path] = {
            "kind": "runtime.intent_plan",
            "id": "plan-1",
            "interaction_id": "interaction-1",
            "clauses": [clause],
        }
        for player_id, account_id, login, pc_id in (
            ("player-alice", "42", "alice", "pc-alice"),
            ("player-bob", "43", "bob", "pc-bob"),
        ):
            path = route_native_record("world.player", (player_id,)).relative_path
            self.records[path] = {
                "kind": "world.player",
                "id": player_id,
                "player_id": player_id,
                "state": {},
                "campaign_id": CAMPAIGN_ID,
                "github_binding": {"user_id": account_id, "login": login},
                "status": "active",
                "deactivated_by": None,
                "controlled_pc_ids": [pc_id],
            }
        scene_path = route_native_record("world.scene", ("scene-market",)).relative_path
        self.records[scene_path] = {
            "kind": "world.scene",
            "id": "scene-market",
            "state": {"scene_id": "scene-market"},
            "campaign_id": CAMPAIGN_ID,
            "revision": CAMPAIGN_REVISION,
        }

    def add_native_owner(self, family: str, record_id: str, value: dict[str, object]) -> None:
        self.records[route_native_record(family, (record_id,)).relative_path] = value


def _collective_clause(
    *, dependency_kind: str = DependencyClass.JOINT_VOLUNTARY_ACTION.value
) -> dict[str, object]:
    return {
        "clause_id": "clause-1",
        "order": 1,
        "mapping_outcome": "exact",
        "execution_state": "intent.pending",
        "collaboration_semantic_class": "ACTIONABLE_INTENT",
        "normalized_semantics": {"action": "enter", "target": "market"},
        "dependency_kind": dependency_kind,
        "purpose": "joint-entry",
        "dependency_scope": {"scene_id": "scene-market"},
        "required_contributors": [{"player_id": "player-bob", "pc_id": "pc-bob"}],
        "native_basis_refs": [{"family": "world.scene", "id": "scene-market"}],
    }


def _route() -> object:
    return build_principal_player_route(
        CAMPAIGN_ID,
        (
            PlayerRecord(
                player_id="player-alice",
                stable_account_id="42",
                login="alice",
                status="active",
                deactivated_by=None,
                controlled_pc_ids=("pc-alice",),
            ),
            PlayerRecord(
                player_id="player-bob",
                stable_account_id="43",
                login="bob",
                status="active",
                deactivated_by=None,
                controlled_pc_ids=("pc-bob",),
            ),
        ),
    )


def _principal() -> VerifiedPrincipal:
    return VerifiedPrincipal(stable_account_id="42", login="alice")


def _classify(repository: FakeRepository) -> object:
    return classify_coordination_dependency(
        repository,
        CAMPAIGN_ID,
        "interaction-1",
        "clause-1",
        principal=_principal(),
        player_route=_route(),
    )


class CoordinationAdmissionTests(unittest.TestCase):
    def test_admission_identity_is_the_revalidated_interaction_and_clause(self) -> None:
        admission = _classify(FakeRepository())

        self.assertEqual(admission.family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE)
        self.assertEqual(admission.opportunity_identity, ("interaction-1", "clause-1"))
        self.assertEqual(admission.intent_plan_id, "plan-1")
        self.assertEqual(admission.required_contributors[0].player_id, "player-bob")
        self.assertEqual(admission.required_contributors[0].pc_id, "pc-bob")

        obligation = open_or_successor_obligation(admission, obligation_id="obligation-1")
        assert obligation is not None
        Draft202012Validator(
            _schema("runtime-collaboration-obligation-state.schema.json"), registry=_registry()
        ).validate(obligation.to_mapping())

    def test_each_ruled_dependency_class_is_finite_and_admitted(self) -> None:
        for dependency_kind in DependencyClass:
            with self.subTest(dependency_kind=dependency_kind):
                admission = _classify(FakeRepository(clause=_collective_clause(dependency_kind=dependency_kind)))
                self.assertEqual(admission.dependency_class, dependency_kind)
                self.assertEqual(admission.family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE)

    def test_unknown_or_caller_selected_dependency_family_fails_closed(self) -> None:
        unknown = FakeRepository(clause=_collective_clause(dependency_kind="OWNER_DEFINED"))
        with self.assertRaisesRegex(CollaborationAdmissionError, "dependency class"):
            _classify(unknown)

        caller_selected = _collective_clause()
        caller_selected["coordination_family"] = "INDEPENDENT_IMMEDIATE"
        with self.assertRaisesRegex(CollaborationAdmissionError, "unsupported.*field"):
            _classify(FakeRepository(clause=caller_selected))

    def test_independent_clause_derives_no_collective_obligation(self) -> None:
        clause = {
            "clause_id": "clause-1",
            "order": 1,
            "mapping_outcome": "narrative_only",
            "execution_state": "intent.ready",
            "collaboration_semantic_class": "DIEGETIC_COMMUNICATION",
            "normalized_semantics": {"speech": "hello"},
        }
        admission = _classify(FakeRepository(clause=clause))

        self.assertEqual(admission.family, CoordinationFamily.INDEPENDENT_IMMEDIATE)
        self.assertIsNone(open_or_successor_obligation(admission))

    def test_native_order_owner_wins_without_generic_collaboration(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [{"family": "runtime.procedure", "id": "procedure-1"}]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.procedure",
            "procedure-1",
            {
                "kind": "runtime.procedure",
                "id": "procedure-1",
                "state": {"lifecycle": "ACTIVE", "pending_choice": "choice-1"},
                "campaign_id": CAMPAIGN_ID,
            },
        )
        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)
        self.assertIsNone(open_or_successor_obligation(admission))


class NativeRevalidationTests(unittest.TestCase):
    def test_login_only_cannot_authorize_the_interaction_player(self) -> None:
        with self.assertRaises(CollaborationAdmissionError):
            classify_coordination_dependency(
                FakeRepository(),
                CAMPAIGN_ID,
                "interaction-1",
                "clause-1",
                principal={"login": "alice"},
                player_route=_route(),
            )

    def test_stale_plan_or_clause_identity_cannot_be_substituted(self) -> None:
        repository = FakeRepository()
        plan_path = route_native_record("runtime.intent_plan", ("plan-1",)).relative_path
        plan = repository.records[plan_path]
        assert isinstance(plan, dict)
        plan["interaction_id"] = "interaction-other"

        with self.assertRaisesRegex(CollaborationAdmissionError, "interaction"):
            _classify(repository)

    def test_required_contributor_is_reloaded_and_controlled_by_current_player(self) -> None:
        repository = FakeRepository()
        player_path = route_native_record("world.player", ("player-bob",)).relative_path
        player = repository.records[player_path]
        assert isinstance(player, dict)
        player["controlled_pc_ids"] = ["pc-other"]

        with self.assertRaisesRegex(CollaborationAdmissionError, "control"):
            _classify(repository)

    def test_missing_native_basis_cannot_create_collective_admission(self) -> None:
        clause = _collective_clause()
        clause.pop("native_basis_refs")
        with self.assertRaisesRegex(CollaborationAdmissionError, "native basis"):
            _classify(FakeRepository(clause=clause))

    def test_unenveloped_native_body_is_not_an_exact_owner_load(self) -> None:
        repository = FakeRepository()
        interaction_path = route_native_record("runtime.interaction", ("interaction-1",)).relative_path
        interaction = repository.records[interaction_path]
        assert isinstance(interaction, dict)
        interaction.pop("kind")
        interaction.pop("id")

        with self.assertRaisesRegex(CollaborationAdmissionError, "identity"):
            _classify(repository)

    def test_caller_boolean_currentness_and_required_contributors_are_not_authority(self) -> None:
        clause = _collective_clause()
        clause["is_current"] = True
        clause["positive_material_dependency"] = True
        clause["required_contributors"] = [{"player_id": "player-alice"}]
        with self.assertRaisesRegex(CollaborationAdmissionError, "unsupported.*field"):
            _classify(FakeRepository(clause=clause))


class CollaborationSchemaTests(unittest.TestCase):
    def test_intent_clause_schema_accepts_only_bounded_interpreted_fields(self) -> None:
        clause = _collective_clause()
        Draft202012Validator(_schema("intent-clause.schema.json"), registry=_registry()).validate(clause)

    def test_obligation_schema_accepts_only_the_derived_collective_owner_shape(self) -> None:
        value = {
            "schema_version": 1,
            "kind": "runtime.collaboration_obligation",
            "obligation_id": "obligation-1",
            "generation": 1,
            "lifecycle": "OPEN",
            "coordination_family": "AGENCY_DEPENDENT_COLLECTIVE",
            "campaign_id": CAMPAIGN_ID,
            "interaction_id": "interaction-1",
            "intent_plan_id": "plan-1",
            "clause_id": "clause-1",
            "dependency_class": "JOINT_VOLUNTARY_ACTION",
            "purpose": "joint-entry",
            "dependency_scope": {"scene_id": "scene-market"},
            "native_basis_refs": [{"family": "world.scene", "id": "scene-market"}],
            "required_contributors": [{"player_id": "player-bob", "pc_id": "pc-bob"}],
            "optional_contributors": [],
            "accepted_input_uses": [],
        }
        Draft202012Validator(
            _schema("runtime-collaboration-obligation-state.schema.json"), registry=_registry()
        ).validate(value)


if __name__ == "__main__":
    unittest.main()
