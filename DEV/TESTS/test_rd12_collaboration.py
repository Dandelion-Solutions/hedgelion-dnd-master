"""W04.T01A collaboration admission over accepted Interaction/IntentPlan owners."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS.access_control import (
    PlayerRecord,
    VerifiedPrincipal,
    build_principal_player_route,
)
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
            "state": {"name": "Market morning"},
            "campaign_id": CAMPAIGN_ID,
            "revision": CAMPAIGN_REVISION,
        }
        asset_path = route_native_record("world.asset", ("asset-market-goods",)).relative_path
        self.records[asset_path] = {
            "kind": "world.asset",
            "id": "asset-market-goods",
            "state": {"quantity": 1},
            "campaign_id": CAMPAIGN_ID,
            "revision": CAMPAIGN_REVISION,
        }
        actor_path = route_native_record("world.actor", ("actor-pc-bob",)).relative_path
        self.records[actor_path] = {
            "kind": "world.actor",
            "id": "actor-pc-bob",
            "state": {"name": {"en": "Bob"}},
            "campaign_id": CAMPAIGN_ID,
            "revision": CAMPAIGN_REVISION,
        }

    def add_native_owner(self, family: str, record_id: str, value: dict[str, object]) -> None:
        self.records[route_native_record(family, (record_id,)).relative_path] = value


def _collective_clause(
    *, dependency_kind: str = DependencyClass.JOINT_VOLUNTARY_ACTION.value
) -> dict[str, object]:
    dependency = DependencyClass(dependency_kind)
    basis = {
        DependencyClass.JOINT_VOLUNTARY_ACTION: ("world.scene", "scene-market", "scene_id"),
        DependencyClass.SHARED_DECISION_OR_NEGOTIATION: ("world.scene", "scene-market", "scene_id"),
        DependencyClass.SHARED_SCARCE_RESOURCE_CHOICE: ("world.asset", "asset-market-goods", "asset_id"),
        DependencyClass.SCENE_CHRONOLOGY_CONVERGENCE: ("world.scene", "scene-market", "scene_id"),
        DependencyClass.PC_CONSEQUENCE_DECISION: ("world.actor", "actor-pc-bob", "actor_id"),
    }[dependency]
    return {
        "clause_id": "clause-1",
        "order": 1,
        "mapping_outcome": "exact",
        "execution_state": "intent.pending",
        "collaboration_semantic_class": "ACTIONABLE_INTENT",
        "normalized_semantics": {"action": "enter", "target": "market"},
        "dependency_kind": dependency_kind,
        "purpose": "joint-entry",
        "dependency_scope": {basis[2]: basis[1]},
        "required_contributors": [{"player_id": "player-bob", "pc_id": "pc-bob"}],
        "native_basis_refs": [{"family": basis[0], "id": basis[1], "revision": CAMPAIGN_REVISION}],
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


def _valid_combat_procedure_state(*, lifecycle: str = "ACTIVE") -> dict[str, object]:
    state: dict[str, object] = {
        "schema_version": 2,
        "procedure_kind": "procedure.combat_minimal",
        "lifecycle": lifecycle,
        "lifecycle_state": "terminated" if lifecycle == "TERMINAL" else "between_turns",
        "participant_ids": ["actor-pc-alice", "actor-pc-bob"],
        "initiative_order": ["actor-pc-alice", "actor-pc-bob"],
        "round_number": 1,
        "round_advance_pending": False,
        "active_turn_index": 0,
        "participant_resources": {
            "actor-pc-alice": {
                "resource.action_budget": {"capacity": 1, "spent": 0},
                "resource.movement_budget": {"capacity": 30, "spent": 0},
            },
            "actor-pc-bob": {
                "resource.action_budget": {"capacity": 1, "spent": 0},
                "resource.movement_budget": {"capacity": 30, "spent": 0},
            },
        },
    }
    Draft202012Validator(_schema("combat-minimal-procedure-state.schema.json"), registry=_registry()).validate(state)
    return state


def _valid_continuation_record(
    *,
    pending_response: dict[str, object] | None = None,
    unconsumed_advancement: dict[str, object] | None = None,
) -> dict[str, object]:
    record: dict[str, object] = {
        "kind": "runtime.continuation",
        "id": "continuation-1",
        "revision": CAMPAIGN_REVISION,
        "generation": 1,
        "root_command_id": "command-1",
        "resolution_id": "resolution-1",
        "activity_id": "activity.attack.basic",
        "actor_id": "actor-pc-bob",
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": "c" * 64,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": "catalog-context-1",
        "execution_cursor": "step.attack.resolve",
        "safe_recompute_phase": "determine",
        "invocation_facts": [],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "committed_segment_refs": ["segment-1"],
        "dependency_frontier_refs": ["frontier-1"],
        "expected_child_resolution_ids": [],
        "future_rng_frontier": "rng-frontier-1",
    }
    if pending_response is not None:
        record["pending_response"] = pending_response
    if unconsumed_advancement is not None:
        record["unconsumed_advancement"] = unconsumed_advancement
    state = {key: value for key, value in record.items() if key not in {"kind", "id", "revision"}}
    Draft202012Validator(_schema("runtime-continuation-state.schema.json"), registry=_registry()).validate(state)
    return record


def _choice_response() -> dict[str, object]:
    return {
        "kind": "choice",
        "offer_id": "choice-1",
        "parent_resolution_id": "resolution-1",
        "continuation_generation": 1,
        "responder_id": "actor-pc-bob",
        "option_ids": ["option.left", "option.right"],
    }


def _reaction_response() -> dict[str, object]:
    return {
        "kind": "reaction",
        "offer_id": "reaction-1",
        "parent_resolution_id": "resolution-1",
        "continuation_generation": 1,
        "responder_id": "actor-pc-bob",
        "candidate_activity_ids": ["activity.shield"],
    }


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

    def test_each_ruled_dependency_class_rejects_an_irrelevant_basis_family(self) -> None:
        wrong_family = {
            DependencyClass.JOINT_VOLUNTARY_ACTION: ("world.asset", "asset-market-goods"),
            DependencyClass.SHARED_DECISION_OR_NEGOTIATION: ("world.asset", "asset-market-goods"),
            DependencyClass.SHARED_SCARCE_RESOURCE_CHOICE: ("world.scene", "scene-market"),
            DependencyClass.SCENE_CHRONOLOGY_CONVERGENCE: ("world.asset", "asset-market-goods"),
            DependencyClass.PC_CONSEQUENCE_DECISION: ("world.scene", "scene-market"),
        }
        for dependency_kind, (family, record_id) in wrong_family.items():
            with self.subTest(dependency_kind=dependency_kind):
                clause = _collective_clause(dependency_kind=dependency_kind)
                clause["native_basis_refs"] = [
                    {"family": family, "id": record_id, "revision": CAMPAIGN_REVISION}
                ]
                with self.assertRaisesRegex(CollaborationAdmissionError, "basis family"):
                    _classify(FakeRepository(clause=clause))

    def test_unknown_or_caller_selected_dependency_family_fails_closed(self) -> None:
        unknown_clause = _collective_clause()
        unknown_clause["dependency_kind"] = "OWNER_DEFINED"
        unknown = FakeRepository(clause=unknown_clause)
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
        clause["native_basis_refs"] = [
            {"family": "runtime.procedure", "id": "procedure-1", "revision": CAMPAIGN_REVISION}
        ]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.procedure",
            "procedure-1",
            {
                "kind": "runtime.procedure",
                "id": "procedure-1",
                "revision": CAMPAIGN_REVISION,
                "state": _valid_combat_procedure_state(),
                "campaign_id": CAMPAIGN_ID,
            },
        )
        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)
        self.assertIsNone(open_or_successor_obligation(admission))

    def test_pending_continuation_choice_is_the_order_owner(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.continuation",
            "continuation-1",
            {
                **_valid_continuation_record(pending_response=_choice_response()),
            },
        )

        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)

    def test_terminal_or_no_pending_nominated_order_owner_fails_closed(self) -> None:
        cases: tuple[tuple[str, dict[str, object]], ...] = (
            ("runtime.procedure", {"state": _valid_combat_procedure_state(lifecycle="TERMINAL")}),
            ("runtime.procedure", {"state": {"lifecycle": "ACTIVE"}}),
            ("runtime.continuation", {"generation": 1}),
        )
        for index, (family, state) in enumerate(cases):
            with self.subTest(case=index):
                clause = _collective_clause()
                record_id = f"ordered-owner-{index}"
                clause["native_basis_refs"] = [
                    {"family": family, "id": record_id, "revision": CAMPAIGN_REVISION}
                ]
                repository = FakeRepository(clause=clause)
                record = {"kind": family, "id": record_id, "revision": CAMPAIGN_REVISION, **state}
                repository.add_native_owner(family, record_id, record)

                with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
                    _classify(repository)

    def test_truthy_unknown_procedure_marker_fails_closed(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.procedure", "id": "procedure-1", "revision": CAMPAIGN_REVISION}
        ]
        state = _valid_combat_procedure_state()
        state["pending_choice"] = "choice-1"
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.procedure",
            "procedure-1",
            {"kind": "runtime.procedure", "id": "procedure-1", "revision": CAMPAIGN_REVISION, "state": state},
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_malformed_continuation_response_fails_closed(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        record = _valid_continuation_record()
        record["pending_response"] = {"kind": "choice", "option_ids": ["option.left"]}
        repository = FakeRepository(clause=clause)
        repository.add_native_owner("runtime.continuation", "continuation-1", record)

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_complete_continuation_without_pending_resume_fails_closed(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner("runtime.continuation", "continuation-1", _valid_continuation_record())

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_schema_invalid_procedure_lifecycle_fails_closed(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.procedure", "id": "procedure-1", "revision": CAMPAIGN_REVISION}
        ]
        state = _valid_combat_procedure_state()
        state["lifecycle_state"] = "not-a-procedure-phase"
        with self.assertRaises(ValidationError):
            Draft202012Validator(
                _schema("combat-minimal-procedure-state.schema.json"), registry=_registry()
            ).validate(state)
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.procedure",
            "procedure-1",
            {"kind": "runtime.procedure", "id": "procedure-1", "revision": CAMPAIGN_REVISION, "state": state},
        )

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_schema_invalid_continuation_nested_fact_fails_closed(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        record = _valid_continuation_record(pending_response=_choice_response())
        record["invocation_facts"] = [{}]
        state = {key: value for key, value in record.items() if key not in {"kind", "id", "revision"}}
        with self.assertRaises(ValidationError):
            Draft202012Validator(_schema("runtime-continuation-state.schema.json"), registry=_registry()).validate(state)
        repository = FakeRepository(clause=clause)
        repository.add_native_owner("runtime.continuation", "continuation-1", record)

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_owner_rejects_unadmitted_continuation_parameter_binding_before_order(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        record = _valid_continuation_record(pending_response=_choice_response())
        record["parameter_bindings"] = {
            "dc": {
                "source_class": "INVOCATION_ADJUDICATED",
                "value": 31,
                "provenance_ref": "turn-1:fact:1",
                "eligibility_basis_fingerprint": "eligibility-1",
                "rules_context_fingerprint": "rules-1",
                "policy_basis_refs": [],
            }
        }
        state = {key: value for key, value in record.items() if key not in {"kind", "id", "revision"}}
        Draft202012Validator(_schema("runtime-continuation-state.schema.json"), registry=_registry()).validate(state)
        repository = FakeRepository(clause=clause)
        repository.add_native_owner("runtime.continuation", "continuation-1", record)

        with self.assertRaisesRegex(CollaborationAdmissionError, "ordered owner"):
            _classify(repository)

    def test_pending_continuation_reaction_is_the_order_owner(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.continuation",
            "continuation-1",
            _valid_continuation_record(pending_response=_reaction_response()),
        )

        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)

    def test_unconsumed_continuation_advancement_is_the_resume_owner(self) -> None:
        clause = _collective_clause()
        clause["native_basis_refs"] = [
            {"family": "runtime.continuation", "id": "continuation-1", "revision": CAMPAIGN_REVISION}
        ]
        repository = FakeRepository(clause=clause)
        repository.add_native_owner(
            "runtime.continuation",
            "continuation-1",
            _valid_continuation_record(
                unconsumed_advancement={
                    "amount": 1,
                    "unit_id": "unit.hour",
                    "context_id": "world-context-1",
                }
            ),
        )

        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.RULE_OWNED_ORDERED)

    def test_scene_pending_marker_does_not_become_a_rule_owned_order(self) -> None:
        repository = FakeRepository()
        scene_path = route_native_record("world.scene", ("scene-market",)).relative_path
        scene = repository.records[scene_path]
        assert isinstance(scene, dict)
        scene["state"] = {"name": "Market morning", "pending_choice": "choice-1"}

        admission = _classify(repository)

        self.assertEqual(admission.family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE)


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

    def test_each_ruled_dependency_class_requires_a_current_basis_revision(self) -> None:
        for dependency_kind in DependencyClass:
            with self.subTest(dependency_kind=dependency_kind):
                clause = _collective_clause(dependency_kind=dependency_kind)
                basis = clause["native_basis_refs"]
                assert isinstance(basis, list)
                assert isinstance(basis[0], dict)
                basis[0].pop("revision")
                with self.assertRaisesRegex(CollaborationAdmissionError, "revision"):
                    _classify(FakeRepository(clause=clause))

    def test_stale_native_basis_revision_fails_closed(self) -> None:
        for dependency_kind in DependencyClass:
            with self.subTest(dependency_kind=dependency_kind):
                clause = _collective_clause(dependency_kind=dependency_kind)
                basis = clause["native_basis_refs"]
                assert isinstance(basis, list)
                assert isinstance(basis[0], dict)
                basis[0]["revision"] = "stale"

                with self.assertRaisesRegex(CollaborationAdmissionError, "stale"):
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
            "native_basis_refs": [
                {"family": "world.scene", "id": "scene-market", "revision": CAMPAIGN_REVISION}
            ],
            "required_contributors": [{"player_id": "player-bob", "pc_id": "pc-bob"}],
            "optional_contributors": [],
            "accepted_input_uses": [],
        }
        Draft202012Validator(
            _schema("runtime-collaboration-obligation-state.schema.json"), registry=_registry()
        ).validate(value)

    def test_native_basis_schema_requires_revision_evidence(self) -> None:
        clause = _collective_clause()
        basis = clause["native_basis_refs"]
        assert isinstance(basis, list)
        assert isinstance(basis[0], dict)
        basis[0].pop("revision")

        with self.assertRaises(ValidationError):
            Draft202012Validator(_schema("intent-clause.schema.json"), registry=_registry()).validate(clause)


if __name__ == "__main__":
    unittest.main()
