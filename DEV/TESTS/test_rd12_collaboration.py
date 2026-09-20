"""W04.T01A collaboration-family admission and participant-authority tests."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource
import yaml
import GAME.TOOLS.collaboration as collaboration_module

from GAME.TOOLS.access_control import (
    PlayerRecord,
    build_principal_player_route,
)
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionRequest,
    CollaborationContractError,
    CoordinationFamily,
    NativeCoordinationBasis,
    classify_coordination_dependency,
    _owner_issue_native_coordination_basis,
    open_or_successor_obligation,
    resolve_participant_authority,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.json"):
        document = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in document:
            registry = registry.with_resource(
                document["$id"], Resource.from_contents(document)
            )
    return registry


def _validate(name: str, value: object) -> None:
    Draft202012Validator(_schema(name), registry=_registry()).validate(value)


def _authority(*, player_id: str = "player-alice", pc_id: str = "pc-alice"):
    player = PlayerRecord(
        player_id=player_id,
        stable_account_id="42",
        login="alice",
        status="active",
        deactivated_by=None,
        controlled_pc_ids=(pc_id,),
    )
    route = build_principal_player_route("campaign-frostfall", (player,))
    return resolve_participant_authority(
        {
            "provider": "github",
            "stable_account_id": "42",
            "login": "alice",
            "verified": True,
        },
        route,
        lambda candidate_id: player if candidate_id == player_id else None,
        campaign_id="campaign-frostfall",
        controlled_pc_id=pc_id,
    )


def _basis(
    *,
    purpose: str = "joint-entry",
    dependency_scope: str = "scene:market",
    positive_dependency: bool = True,
    input_can_change_result: bool = True,
    opportunity_current: bool = True,
    independently_durable: bool = True,
    native_order_owner: str | None = None,
    participants: tuple[object, ...] | None = None,
) -> NativeCoordinationBasis:
    return _owner_issue_native_coordination_basis(
        campaign_id="campaign-frostfall",
        source_ref="scene:market",
        source_revision="a" * 40,
        opportunity_ref="decision:market-entry",
        purpose=purpose,
        dependency_scope=dependency_scope,
        positive_material_dependency=positive_dependency,
        input_can_change_result=input_can_change_result,
        opportunity_current=opportunity_current,
        independently_durable=independently_durable,
        native_order_owner=native_order_owner,
        required_participants=participants or (_authority(),),
    )


class CoordinationAdmissionTests(unittest.TestCase):
    def test_family_is_derived_from_native_evidence_not_a_caller_selector(self):
        self.assertEqual(
            classify_coordination_dependency(_basis()),
            CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE,
        )
        with self.assertRaises(CollaborationContractError):
            CollaborationAdmissionRequest.from_mapping(
                {
                    "obligation_id": "obligation-1",
                    "purpose": "joint-entry",
                    "dependency_scope": "scene:market",
                    "decision_opportunity_ref": "decision:market-entry",
                    "coordination_family": "INDEPENDENT_IMMEDIATE",
                }
            )

    def test_independent_input_creates_no_obligation(self):
        mutation = open_or_successor_obligation(
            CollaborationAdmissionRequest(
                obligation_id="obligation-independent",
                purpose="observe",
                dependency_scope="scene:market",
                decision_opportunity_ref="decision:market-entry",
            ),
            _basis(purpose="observe", positive_dependency=False),
        )
        self.assertEqual(mutation.family, CoordinationFamily.INDEPENDENT_IMMEDIATE)
        self.assertIsNone(mutation.obligation)

    def test_native_order_owners_exclude_generic_collaboration(self):
        for owner in ("Procedure", "Continuation", "Choice", "Reaction"):
            with self.subTest(owner=owner):
                basis = _basis(
                    purpose="native-choice",
                    dependency_scope="native:1",
                    native_order_owner=owner,
                )
                self.assertEqual(
                    classify_coordination_dependency(basis),
                    CoordinationFamily.RULE_OWNED_ORDERED,
                )
                mutation = open_or_successor_obligation(
                    CollaborationAdmissionRequest(
                        obligation_id=f"obligation-{owner.lower()}",
                        purpose="native-choice",
                        dependency_scope="native:1",
                        decision_opportunity_ref="decision:market-entry",
                    ),
                    basis,
                )
                self.assertIsNone(mutation.obligation)
                self.assertEqual(mutation.disposition, "NATIVE_OWNER_REQUIRED")

    def test_presence_or_possible_interest_does_not_create_a_dependency(self):
        mutation = open_or_successor_obligation(
            CollaborationAdmissionRequest(
                obligation_id="obligation-possible",
                purpose="possible-interest",
                dependency_scope="scene:market",
                decision_opportunity_ref="decision:market-entry",
            ),
            _basis(
                purpose="possible-interest",
                positive_dependency=False,
                input_can_change_result=False,
            ),
        )
        self.assertEqual(mutation.family, CoordinationFamily.INDEPENDENT_IMMEDIATE)
        self.assertIsNone(mutation.obligation)

    def test_mechanical_value_contribution_is_not_collaboration_input(self):
        with self.assertRaises(CollaborationContractError):
            collaboration_module.issue_native_coordination_basis(
                campaign_id="campaign-frostfall",
                source_ref="scene:market",
                source_revision="a" * 40,
                opportunity_ref="decision:market-entry",
                positive_material_dependency=True,
                input_can_change_result=True,
                opportunity_current=True,
                independently_durable=True,
                required_participants=(_authority(),),
                semantic_value_kind="value.contribution",
            )


class ParticipantAuthorityTests(unittest.TestCase):
    def test_public_basis_factory_cannot_mint_coordination_authority(self):
        with self.assertRaises(CollaborationContractError):
            collaboration_module.issue_native_coordination_basis(
                campaign_id="campaign-frostfall",
                source_ref="scene:market",
                source_revision="a" * 40,
                opportunity_ref="decision:market-entry",
                positive_material_dependency=True,
                input_can_change_result=True,
                opportunity_current=True,
                independently_durable=True,
                required_participants=(_authority(),),
            )

        class ForgedBasis(NativeCoordinationBasis):
            def __post_init__(self) -> None:
                pass

        forged = ForgedBasis(
            campaign_id="campaign-frostfall",
            source_ref="scene:market",
            source_revision="a" * 40,
            opportunity_ref="decision:market-entry",
            positive_material_dependency=True,
            input_can_change_result=True,
            opportunity_current=True,
            independently_durable=True,
            required_participants=(_authority(),),
            purpose="joint-entry",
            dependency_scope="scene:market",
        )
        with self.assertRaises(CollaborationContractError):
            open_or_successor_obligation(
                CollaborationAdmissionRequest(
                    obligation_id="obligation-subclass",
                    purpose="joint-entry",
                    dependency_scope="scene:market",
                    decision_opportunity_ref="decision:market-entry",
                ),
                forged,
            )

    def test_request_opportunity_must_match_native_opportunity(self):
        for purpose, dependency_scope, opportunity_ref in (
            ("forged-purpose", "scene:market", "decision:market-entry"),
            ("joint-entry", "scene:forged", "decision:market-entry"),
            ("joint-entry", "scene:market", "decision:forged"),
        ):
            with self.subTest(purpose=purpose, dependency_scope=dependency_scope, opportunity_ref=opportunity_ref):
                with self.assertRaises(CollaborationContractError):
                    open_or_successor_obligation(
                        CollaborationAdmissionRequest(
                            obligation_id="obligation-mismatch",
                            purpose=purpose,
                            dependency_scope=dependency_scope,
                            decision_opportunity_ref=opportunity_ref,
                        ),
                        _basis(),
                    )

    def test_login_only_does_not_admit_participant_authority(self):
        player = PlayerRecord(
            player_id="player-alice",
            stable_account_id="42",
            login="alice",
            status="active",
            deactivated_by=None,
            controlled_pc_ids=("pc-alice",),
        )
        route = build_principal_player_route("campaign-frostfall", (player,))
        with self.assertRaises(CollaborationContractError):
            resolve_participant_authority(
                {"login": "alice"},
                route,
                lambda _candidate_id: player,
                campaign_id="campaign-frostfall",
                controlled_pc_id="pc-alice",
            )

    def test_caller_cannot_select_required_contributors_or_currentness(self):
        with self.assertRaises(CollaborationContractError):
            CollaborationAdmissionRequest.from_mapping(
                {
                    "obligation_id": "obligation-1",
                    "purpose": "joint-entry",
                    "dependency_scope": "scene:market",
                    "decision_opportunity_ref": "decision:market-entry",
                    "required_contributors": ["player-attacker"],
                }
            )
        with self.assertRaises(CollaborationContractError):
            open_or_successor_obligation(
                CollaborationAdmissionRequest(
                    obligation_id="obligation-stale",
                    purpose="joint-entry",
                    dependency_scope="scene:market",
                    decision_opportunity_ref="decision:market-entry",
                ),
                {"current": True},
            )

        with self.assertRaises(CollaborationContractError):
            NativeCoordinationBasis(
                campaign_id="campaign-frostfall",
                source_ref="scene:market",
                source_revision="a" * 40,
                opportunity_ref="decision:market-entry",
                positive_material_dependency=True,
                input_can_change_result=True,
                opportunity_current=True,
                independently_durable=True,
                required_participants=(),
            )

    def test_non_current_native_opportunity_fails_closed(self):
        with self.assertRaises(CollaborationContractError):
            open_or_successor_obligation(
                CollaborationAdmissionRequest(
                    obligation_id="obligation-stale",
                    purpose="joint-entry",
                    dependency_scope="scene:market",
                    decision_opportunity_ref="decision:market-entry",
                ),
                _basis(opportunity_current=False),
            )

    def test_required_participants_are_exact_owner_issued_refs(self):
        mutation = open_or_successor_obligation(
            CollaborationAdmissionRequest(
                obligation_id="obligation-exact",
                purpose="joint-entry",
                dependency_scope="scene:market",
                decision_opportunity_ref="decision:market-entry",
            ),
            _basis(),
        )
        assert mutation.obligation is not None
        self.assertEqual(
            mutation.obligation.required_contributors[0].player_id,
            "player-alice",
        )
        self.assertEqual(mutation.obligation.required_contributors[0].pc_id, "pc-alice")


class CollaborationSchemaTests(unittest.TestCase):
    def test_game_schema_matches_dev_contributor_cardinality_and_uniqueness(self):
        schema = yaml.safe_load(
            (ROOT / "GAME" / "SCHEMA" / "collaboration_obligation.schema.yaml").read_text(
                encoding="utf-8"
            )
        )
        required = schema["fields"]["required_contributors"]
        optional = schema["fields"]["optional_contributors"]
        self.assertEqual(required, {
            "type": "array",
            "item": "participant_ref",
            "min_items": 1,
            "unique_items": True,
        })
        self.assertEqual(optional, {
            "type": "array",
            "item": "participant_ref",
            "unique_items": True,
        })

    def test_base_obligation_schema_accepts_owner_shape(self):
        _validate(
            "runtime-collaboration-obligation-state.schema.json",
            {
                "schema_version": 1,
                "kind": "runtime.collaboration_obligation",
                "obligation_id": "obligation-1",
                "generation": 1,
                "lifecycle": "OPEN",
                "coordination_family": "AGENCY_DEPENDENT_COLLECTIVE",
                "campaign_id": "campaign-frostfall",
                "purpose": "joint-entry",
                "dependency_scope": "scene:market",
                "decision_opportunity_ref": "decision:market-entry",
                "currentness_basis": {
                    "source_ref": "scene:market",
                    "source_revision": "a" * 40,
                    "opportunity_ref": "decision:market-entry",
                },
                "required_contributors": [{"player_id": "player-alice", "pc_id": "pc-alice"}],
                "optional_contributors": [{"player_id": "player-bob", "pc_id": None}],
                "accepted_input_uses": [],
                "safe_frontier_refs": [],
                "execution_anchor_clause_ref": None,
                "closed_input_set_fingerprint": None,
            },
        )

    def test_obligation_schema_rejects_mechanical_contribution_vocabulary(self):
        value = {
            "schema_version": 1,
            "kind": "runtime.collaboration_obligation",
            "obligation_id": "obligation-1",
            "generation": 1,
            "lifecycle": "OPEN",
            "coordination_family": "AGENCY_DEPENDENT_COLLECTIVE",
            "campaign_id": "campaign-frostfall",
            "purpose": "joint-entry",
            "dependency_scope": "scene:market",
            "decision_opportunity_ref": "decision:market-entry",
            "currentness_basis": {
                "source_ref": "scene:market",
                "source_revision": "a" * 40,
                "opportunity_ref": "decision:market-entry",
            },
            "required_contributors": [{"player_id": "player-alice"}],
            "optional_contributors": [],
            "accepted_input_uses": [],
            "safe_frontier_refs": [],
            "value.contribution": {},
        }
        with self.assertRaises(ValidationError):
            _validate("runtime-collaboration-obligation-state.schema.json", value)

    def test_intent_clause_accepts_bounded_collaboration_semantics(self):
        _validate(
            "intent-clause.schema.json",
            {
                "clause_id": "clause-1",
                "order": 1,
                "mapping_outcome": "exact",
                "execution_state": "intent.pending",
                "collaboration_semantic_class": "ACTIONABLE_INTENT",
                "normalized_semantics": {"action": "enter", "target": "market"},
                "material_exact_text_refs": [{"message_id": "message-1"}],
            },
        )

    def test_intent_clause_rejects_unknown_collaboration_class(self):
        with self.assertRaises(ValidationError):
            _validate(
                "intent-clause.schema.json",
                {
                    "clause_id": "clause-1",
                    "order": 1,
                    "mapping_outcome": "exact",
                    "execution_state": "intent.pending",
                    "collaboration_semantic_class": "value.contribution",
                    "normalized_semantics": {"amount": 1},
                },
            )


if __name__ == "__main__":
    unittest.main()
