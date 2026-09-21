"""W04.T01A coordination admission and exact participant authority tests."""

from __future__ import annotations

from copy import deepcopy
from importlib.util import find_spec
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, ValidationError

from GAME.TOOLS.access_control import (
    PlayerRecord,
    build_principal_player_route,
)
from GAME.TOOLS.collaboration import (
    CollaborationAdmissionRequest,
    CollaborationContractError,
    CoordinationFamily,
    classify_coordination_dependency,
    open_or_successor_obligation,
    resolve_participant_authority,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"


class ExactLoadTransport:
    """Test-only exact native-record transport; it returns records only."""

    def __init__(self, records: dict[tuple[str, str], dict[str, object]]) -> None:
        self.records = records
        self.calls: list[tuple[str, tuple[str, ...]]] = []

    def load_exact(self, family_key: str, identity: tuple[str, ...]) -> dict[str, object] | None:
        self.calls.append((family_key, identity))
        record = self.records.get((family_key, identity[0]))
        return None if record is None else deepcopy(record)


def _player(
    player_id: str,
    account_id: str,
    login: str,
    *,
    pc_ids: tuple[str, ...] = (),
    status: str = "active",
) -> PlayerRecord:
    return PlayerRecord(
        player_id=player_id,
        stable_account_id=account_id,
        login=login,
        status=status,
        deactivated_by=None if status == "active" else "creator",
        controlled_pc_ids=pc_ids,
    )


def _transport(
    *,
    candidate_players: tuple[str, ...] = ("player-alice", "player-bob"),
    required_players: tuple[str, ...] = ("player-alice", "player-bob"),
    positive_dependency: bool = True,
    can_change_result: bool = True,
    opportunity_status: str = "OPEN",
    ordered_owner: str | None = None,
) -> ExactLoadTransport:
    players = {
        "player-alice": {
            "kind": "world.player",
            "id": "player-alice",
            "player_id": "player-alice",
            "status": "active",
            "github_binding": {"user_id": 42, "login": "alice"},
            "controlled_pc_ids": ["pc-alice"],
        },
        "player-bob": {
            "kind": "world.player",
            "id": "player-bob",
            "player_id": "player-bob",
            "status": "active",
            "github_binding": {"user_id": 43, "login": "bob"},
            "controlled_pc_ids": ["pc-bob"],
        },
    }
    required_refs = [
        {"player_id": player_id, "pc_id": f"pc-{player_id.removeprefix('player-')}"}
        for player_id in required_players
    ]
    records: dict[tuple[str, str], dict[str, object]] = {
        ("runtime.interaction", "interaction-1"): {
            "kind": "runtime.interaction",
            "interaction_id": "interaction-1",
            "campaign_id": "campaign-frostfall",
            "session_id": "session-1",
            "player_id": "player-alice",
            "input_message_id": "message-1",
            "intent_plan_id": "plan-1",
            "state_revision": "interaction-rev-1",
        },
        ("runtime.intent_plan", "plan-1"): {
            "kind": "runtime.intent_plan",
            "intent_plan_id": "plan-1",
            "interaction_id": "interaction-1",
            "campaign_id": "campaign-frostfall",
            "state_revision": "plan-rev-1",
            "clauses": [
                {
                    "clause_id": "clause-1",
                    "order": 1,
                    "mapping_outcome": "exact",
                    "execution_state": "intent.pending",
                    "collaboration_semantic_class": "ACTIONABLE_INTENT",
                    "normalized_semantics": {"action": "enter"},
                    "coordination_candidate": {
                        "native_owner_kind": "world.scene",
                        "native_owner_id": "scene-market",
                        "opportunity_id": "opportunity-entry",
                        "purpose": "joint-entry",
                        "dependency_scope": "scene:market",
                        "participant_player_ids": list(candidate_players),
                    },
                }
            ],
        },
        ("world.scene", "scene-market"): {
            "kind": "world.scene",
            "id": "scene-market",
            "schema_version": 2,
            "state_revision": "scene-rev-1",
            "state": {
                "status": "active",
                "coordination_opportunities": [
                    {
                        "opportunity_id": "opportunity-entry",
                        "status": opportunity_status,
                        "purpose": "joint-entry",
                        "dependency_scope": "scene:market",
                        "positive_material_dependency": positive_dependency,
                        "input_can_change_result": can_change_result,
                        "independently_durable": True,
                        "required_participants": required_refs,
                        **({"native_order_owner": ordered_owner} if ordered_owner else {}),
                    }
                ],
            },
        },
        **{("world.player", player_id): record for player_id, record in players.items()},
    }
    return ExactLoadTransport(records)


def _request(**overrides: object) -> CollaborationAdmissionRequest:
    values: dict[str, object] = {
        "interaction_id": "interaction-1",
        "intent_plan_id": "plan-1",
        "clause_id": "clause-1",
        "obligation_id": "obligation-1",
    }
    values.update(overrides)
    return CollaborationAdmissionRequest(**values)


def _principal_and_route() -> tuple[dict[str, object], object, PlayerRecord]:
    player = _player("player-alice", "42", "alice", pc_ids=("pc-alice",))
    route = build_principal_player_route("campaign-frostfall", (player,))
    principal = {
        "provider": "github",
        "stable_account_id": "42",
        "login": "alice",
        "verified": True,
    }
    return principal, route, player


def _admit(
    request: CollaborationAdmissionRequest | dict[str, object] | None = None,
    *,
    transport: ExactLoadTransport | None = None,
):
    principal, route, player = _principal_and_route()
    selected_transport = _transport() if transport is None else transport
    return open_or_successor_obligation(
        _request() if request is None else request,
        principal=principal,
        player_route=route,
        load_exact_player=lambda player_id: player if player_id == player.player_id else None,
        exact_load=selected_transport.load_exact,
        campaign_id="campaign-frostfall",
    )


class CollaborationAdmissionTests(unittest.TestCase):
    def test_collaboration_owner_module_exists(self) -> None:
        self.assertIsNotNone(find_spec("GAME.TOOLS.collaboration"))

    def test_positive_current_dependency_admits_collective_family(self) -> None:
        result = _admit()
        self.assertEqual(result.family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE)
        self.assertIsNotNone(result.obligation)
        assert result.obligation is not None
        self.assertEqual(
            tuple(item.player_id for item in result.obligation.required_contributors),
            ("player-alice", "player-bob"),
        )

    def test_caller_cannot_select_family_or_required_contributors(self) -> None:
        with self.assertRaises(CollaborationContractError):
            _admit(
                {
                    "interaction_id": "interaction-1",
                    "intent_plan_id": "plan-1",
                    "clause_id": "clause-1",
                    "obligation_id": "obligation-1",
                    "coordination_family": "INDEPENDENT_IMMEDIATE",
                    "required_contributors": ["player-alice"],
                }
            )

    def test_independence_does_not_create_an_obligation(self) -> None:
        result = _admit(transport=_transport(positive_dependency=False))
        self.assertEqual(result.family, CoordinationFamily.INDEPENDENT_IMMEDIATE)
        self.assertIsNone(result.obligation)

    def test_unproven_independence_is_not_collective(self) -> None:
        result = _admit(transport=_transport(can_change_result=False))
        self.assertEqual(result.family, CoordinationFamily.INDEPENDENT_IMMEDIATE)
        self.assertIsNone(result.obligation)

    def test_native_order_owner_wins_over_generic_collaboration(self) -> None:
        result = _admit(transport=_transport(ordered_owner="Choice"))
        self.assertEqual(result.family, CoordinationFamily.RULE_OWNED_ORDERED)
        self.assertIsNone(result.obligation)

    def test_classification_reloads_native_sources_before_returning_family(self) -> None:
        transport = _transport()
        family = classify_coordination_dependency(
            _request(),
            principal={
                "provider": "github",
                "stable_account_id": "42",
                "login": "alice",
                "verified": True,
            },
            player_route=build_principal_player_route(
                "campaign-frostfall",
                (_player("player-alice", "42", "alice", pc_ids=("pc-alice",)),),
            ),
            load_exact_player=lambda player_id: _player(
                "player-alice", "42", "alice", pc_ids=("pc-alice",)
            )
            if player_id == "player-alice"
            else None,
            exact_load=transport,
            campaign_id="campaign-frostfall",
        )
        self.assertEqual(family, CoordinationFamily.AGENCY_DEPENDENT_COLLECTIVE)
        self.assertIn(("runtime.interaction", ("interaction-1",)), transport.calls)
        self.assertIn(("runtime.intent_plan", ("plan-1",)), transport.calls)
        self.assertIn(("world.scene", ("scene-market",)), transport.calls)

    def test_admitted_obligation_serializes_to_its_persistent_schema(self) -> None:
        result = _admit()
        assert result.obligation is not None
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(result.obligation.as_mapping())

    def test_stale_native_opportunity_fails_closed(self) -> None:
        with self.assertRaises(CollaborationContractError):
            _admit(transport=_transport(opportunity_status="STALE"))

    def test_exact_load_transport_cannot_supply_semantic_verdict(self) -> None:
        transport = _transport()
        transport.records[("world.scene", "scene-market")] = {
            "kind": "world.scene",
            "id": "scene-market",
            "current": True,
            "eligible": True,
            "coordination_family": "AGENCY_DEPENDENT_COLLECTIVE",
        }
        with self.assertRaises(CollaborationContractError):
            _admit(transport=transport)

    def test_candidate_is_revalidated_against_loaded_intent_and_opportunity(self) -> None:
        transport = _transport(candidate_players=("player-alice",))
        with self.assertRaises(CollaborationContractError):
            _admit(transport=transport)

    def test_caller_selected_family_in_a_candidate_is_rejected(self) -> None:
        transport = _transport()
        clause = transport.records[("runtime.intent_plan", "plan-1")]["clauses"][0]
        assert isinstance(clause, dict)
        candidate = clause["coordination_candidate"]
        assert isinstance(candidate, dict)
        candidate["coordination_family"] = "INDEPENDENT_IMMEDIATE"
        with self.assertRaises(CollaborationContractError):
            _admit(transport=transport)

    def test_mechanical_contribution_is_not_collaboration_admission(self) -> None:
        transport = _transport()
        clause = transport.records[("runtime.intent_plan", "plan-1")]["clauses"][0]
        assert isinstance(clause, dict)
        clause["normalized_semantics"] = {"value_kind": "value.contribution"}
        with self.assertRaises(CollaborationContractError):
            _admit(transport=transport)


class ParticipantAuthorityTests(unittest.TestCase):
    def test_login_alone_cannot_authorize_participant(self) -> None:
        _principal, route, player = _principal_and_route()
        with self.assertRaises(CollaborationContractError):
            resolve_participant_authority(
                {"login": "alice"},
                route,
                lambda player_id: player if player_id == player.player_id else None,
                campaign_id="campaign-frostfall",
            )

    def test_exact_current_player_and_controlled_pc_are_required(self) -> None:
        principal, route, player = _principal_and_route()
        resolution = resolve_participant_authority(
            principal,
            route,
            lambda player_id: player if player_id == player.player_id else None,
            campaign_id="campaign-frostfall",
            controlled_pc_id="pc-alice",
        )
        self.assertEqual(resolution.player_id, "player-alice")
        with self.assertRaises(CollaborationContractError):
            resolve_participant_authority(
                principal,
                route,
                lambda player_id: player if player_id == player.player_id else None,
                campaign_id="campaign-frostfall",
                controlled_pc_id="pc-other",
            )

    def test_stale_or_foreign_player_route_fails_closed(self) -> None:
        principal, route, player = _principal_and_route()
        foreign = _player("player-foreign", "99", "foreign", pc_ids=("pc-foreign",))
        with self.assertRaises(CollaborationContractError):
            resolve_participant_authority(
                principal,
                route,
                lambda _player_id: foreign,
                campaign_id="campaign-frostfall",
            )


class CollaborationSchemaTests(unittest.TestCase):
    def test_base_obligation_schema_accepts_admitted_shape(self) -> None:
        schema = json.loads(
            (SCHEMAS / "runtime-collaboration-obligation-state.schema.json").read_text(
                encoding="utf-8"
            )
        )
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
            "decision_opportunity_ref": "opportunity-entry",
            "currentness_basis": {
                "source_ref": "scene:market",
                "source_revision": "scene-rev-1",
                "opportunity_ref": "opportunity-entry",
            },
            "required_contributors": [{"player_id": "player-alice", "pc_id": "pc-alice"}],
            "optional_contributors": [],
            "accepted_input_uses": [],
            "safe_frontier_refs": [],
        }
        Draft202012Validator(schema).validate(value)

    def test_intent_clause_collaboration_fields_require_typed_semantics(self) -> None:
        schema = json.loads((SCHEMAS / "intent-clause.schema.json").read_text(encoding="utf-8"))
        valid = {
            "clause_id": "clause-1",
            "order": 1,
            "mapping_outcome": "exact",
            "execution_state": "intent.pending",
            "collaboration_semantic_class": "ACTIONABLE_INTENT",
            "normalized_semantics": {"action": "enter"},
            "material_exact_text_refs": [{"message_id": "message-1"}],
        }
        Draft202012Validator(schema).validate(valid)
        invalid = dict(valid)
        invalid.pop("normalized_semantics")
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(invalid)


if __name__ == "__main__":
    unittest.main()
