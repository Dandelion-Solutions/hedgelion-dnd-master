"""Principal-to-PLAYER routing and fail-closed authorization witnesses."""

from __future__ import annotations

from pathlib import Path
import unittest

from GAME.TOOLS.access_control import (
    AccessControlContractError,
    AuthorizationFailureCode,
    PlayerRecord,
    PlayerResolution,
    PrincipalPlayerRoute,
    RouteEntry,
    VerifiedPrincipal,
    authorize_operation,
    build_principal_player_route,
    resolve_player,
    resolve_principal,
)


ROOT = Path(__file__).resolve().parents[2]
ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"


def _principal(*, account_id: object = "42", login: str = "lina") -> VerifiedPrincipal:
    return resolve_principal(
        {
            "provider": "github",
            "stable_account_id": account_id,
            "login": login,
            "verified": True,
        }
    )


def _route(*, candidates: tuple[str, ...] = ("player-1",)) -> PrincipalPlayerRoute:
    return PrincipalPlayerRoute(
        campaign_id="campaign-frostfall",
        entries=(RouteEntry(stable_account_id="42", candidate_player_ids=candidates),),
    )


def _player(
    player_id: str = "player-1",
    *,
    account_id: object = "42",
    login: str = "lina",
    status: str = "active",
    deactivated_by: str | None = None,
    mechanical_override_policy: bool | None = None,
) -> dict[str, object]:
    player: dict[str, object] = {
        "player_id": player_id,
        "status": status,
        "deactivated_by": deactivated_by,
        "github_binding": {"user_id": account_id, "login": login},
        "controlled_pc_ids": ["pc-1"],
    }
    if mechanical_override_policy is not None:
        player["policy_authority"] = {
            "mechanical_override_policy": mechanical_override_policy
        }
    return player


class PrincipalAuthorizationTests(unittest.TestCase):
    def test_verified_stable_account_id_routes_to_exact_active_player(self) -> None:
        reads: list[str] = []

        def load_exact(player_id: str) -> dict[str, object]:
            reads.append(player_id)
            return _player(player_id)

        principal = _principal()
        resolution = resolve_player(
            principal, _route(), load_exact, campaign_id="campaign-frostfall"
        )
        decision = authorize_operation(principal, resolution, operation="gameplay")

        self.assertTrue(decision.authorized)
        self.assertEqual(decision.player_id, "player-1")
        self.assertEqual(resolution.status, "AUTHORIZED_PLAYER")
        self.assertEqual(reads, ["player-1"])

    def test_stale_route_candidate_is_typed_failure_without_fallback_scan(self) -> None:
        reads: list[str] = []

        def load_exact(player_id: str) -> None:
            reads.append(player_id)
            return None

        resolution = resolve_player(
            _principal(), _route(), load_exact, campaign_id="campaign-frostfall"
        )
        decision = authorize_operation(_principal(), resolution, operation="gameplay")

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.STALE_CANDIDATE)
        self.assertEqual(reads, ["player-1"])

    def test_duplicate_binding_is_ambiguous_and_never_first_match(self) -> None:
        reads: list[str] = []

        def load_exact(player_id: str) -> dict[str, object]:
            reads.append(player_id)
            return _player(player_id)

        route = _route(candidates=("player-1", "player-2"))
        resolution = resolve_player(
            _principal(), route, load_exact, campaign_id="campaign-frostfall"
        )
        decision = authorize_operation(_principal(), resolution, operation="gameplay")

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.AMBIGUOUS_BINDING)
        self.assertEqual(reads, ["player-1", "player-2"])

    def test_inactive_binding_is_routable_for_self_rejoin_but_not_gameplay(self) -> None:
        resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id, status="inactive", deactivated_by="self"),
            campaign_id="campaign-frostfall",
        )

        self.assertEqual(resolution.status, "INACTIVE_REJOIN_CANDIDATE")
        self.assertFalse(
            authorize_operation(_principal(), resolution, operation="gameplay").authorized
        )
        rejoin = authorize_operation(_principal(), resolution, operation="rejoin")
        self.assertTrue(rejoin.authorized)
        self.assertEqual(rejoin.player_id, "player-1")

    def test_login_only_impersonation_cannot_select_a_player(self) -> None:
        principal = _principal(account_id="attacker-99", login="lina")
        resolution = resolve_player(
            principal,
            _route(),
            lambda _player_id: _player(),
            campaign_id="campaign-frostfall",
        )
        decision = authorize_operation(principal, resolution, operation="gameplay")

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.ROUTE_ABSENT)

    def test_creator_uncertainty_fails_closed_and_stable_id_is_not_a_substitute(self) -> None:
        principal = _principal()
        resolution = resolve_player(
            principal,
            _route(),
            lambda player_id: _player(player_id),
            campaign_id="campaign-frostfall",
        )

        missing = authorize_operation(
            principal, resolution, operation="creator_write", creator_login=None
        )
        renamed = authorize_operation(
            principal, resolution, operation="creator_write", creator_login="lina-renamed"
        )

        self.assertFalse(missing.authorized)
        self.assertEqual(missing.failure_code, AuthorizationFailureCode.CREATOR_UNCERTAIN)
        self.assertFalse(renamed.authorized)
        self.assertEqual(renamed.failure_code, AuthorizationFailureCode.CREATOR_UNCERTAIN)

    def test_absent_route_is_typed_fail_closed_result_without_player_read(self) -> None:
        reads: list[str] = []
        resolution = resolve_player(
            _principal(),
            None,
            lambda player_id: reads.append(player_id),
        )
        decision = authorize_operation(_principal(), resolution, operation="gameplay")

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.ROUTE_ABSENT)
        self.assertEqual(reads, [])

    def test_forged_player_resolution_cannot_bypass_the_route_reload(self) -> None:
        forged = PlayerResolution(
            status="AUTHORIZED_PLAYER",
            player=PlayerRecord(
                player_id="player-1",
                stable_account_id="42",
                login="lina",
                status="active",
                deactivated_by=None,
            ),
        )

        decision = authorize_operation(_principal(), forged, operation="gameplay")

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.PLAYER_RECORD_INVALID)

    def test_resolution_for_one_principal_cannot_be_reused_by_another(self) -> None:
        resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id),
            campaign_id="campaign-frostfall",
        )

        decision = authorize_operation(
            _principal(account_id="attacker-99"), resolution, operation="gameplay"
        )

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.PLAYER_RECORD_INVALID)

    def test_mechanical_override_requires_existing_owner_grant(self) -> None:
        resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id),
            campaign_id="campaign-frostfall",
        )
        denied = authorize_operation(
            _principal(), resolution, operation="mechanical_override_policy"
        )

        granted_resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id, mechanical_override_policy=True),
            campaign_id="campaign-frostfall",
        )
        granted = authorize_operation(
            _principal(), granted_resolution, operation="mechanical_override_policy"
        )

        self.assertFalse(denied.authorized)
        self.assertEqual(denied.failure_code, "policy.mechanical_override_grant_required")
        self.assertTrue(granted.authorized)

    def test_caller_supplied_creator_login_cannot_self_claim_mechanical_override(self) -> None:
        resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id),
            campaign_id="campaign-frostfall",
        )

        decision = authorize_operation(
            _principal(),
            resolution,
            operation="mechanical_override_policy",
            creator_login="lina",
        )

        self.assertFalse(decision.authorized)
        self.assertEqual(decision.failure_code, AuthorizationFailureCode.CREATOR_UNCERTAIN)

    def test_ordinary_authorization_requires_campaign_scope_evidence(self) -> None:
        resolution = resolve_player(_principal(), _route(), lambda player_id: _player(player_id))

        self.assertEqual(resolution.failure_code, "principal_player_route.scope_required")

    def test_incomplete_route_returns_typed_fail_closed_result(self) -> None:
        incomplete = _route().as_mapping() | {"complete": False}
        try:
            resolution = resolve_player(
                _principal(),
                incomplete,
                lambda player_id: _player(player_id),
                campaign_id="campaign-frostfall",
            )
        except AccessControlContractError as error:
            self.fail(f"incomplete route raised instead of returning typed failure: {error!r}")

        self.assertEqual(resolution.failure_code, "principal_player_route.incomplete")


class PrincipalPlayerRouteCompanionTests(unittest.TestCase):
    def test_route_builder_preserves_duplicate_bindings_as_candidates(self) -> None:
        route = build_principal_player_route(
            "campaign-frostfall",
            (
                _player("player-2"),
                _player("player-1"),
                _player("player-other", account_id="99"),
            ),
        )

        self.assertEqual(route.entries[0].stable_account_id, "42")
        self.assertEqual(route.entries[0].candidate_player_ids, ("player-1", "player-2"))
        self.assertEqual(route.entries[1].stable_account_id, "99")

    def test_cross_campaign_route_is_fail_closed_when_scope_is_revalidated(self) -> None:
        resolution = resolve_player(
            _principal(),
            _route(),
            lambda player_id: _player(player_id),
            campaign_id="campaign-other",
        )

        self.assertEqual(resolution.failure_code, AuthorizationFailureCode.ROUTE_SCOPE_MISMATCH)

    def test_route_companion_is_complete_and_serializes_candidates_only(self) -> None:
        route = _route(candidates=("player-1", "player-2"))

        self.assertTrue(route.complete)
        self.assertEqual(
            route.as_mapping(),
            {
                "schema_version": 1,
                "kind": "runtime.principal_player_routing",
                "campaign_id": "campaign-frostfall",
                "complete": True,
                "entries": [
                    {
                        "stable_account_id": "42",
                        "candidate_player_ids": ["player-1", "player-2"],
                    }
                ],
            },
        )

    def test_route_companion_rejects_incomplete_or_duplicate_entries(self) -> None:
        base = _route().as_mapping()
        with self.assertRaisesRegex(AccessControlContractError, "complete"):
            PrincipalPlayerRoute.from_mapping(base | {"complete": False})

        duplicate = base | {
            "entries": [
                base["entries"][0],
                {"stable_account_id": "42", "candidate_player_ids": ["player-2"]},
            ]
        }
        with self.assertRaisesRegex(AccessControlContractError, "unique"):
            PrincipalPlayerRoute.from_mapping(duplicate)

    def test_blank_campaign_template_is_present_and_does_not_authorize_by_itself(self) -> None:
        content = ROUTE_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("kind: runtime.principal_player_routing", content)
        self.assertIn("complete: true", content)
        self.assertIn("entries: []", content)

        template = PrincipalPlayerRoute.from_mapping(
            {
                "schema_version": 1,
                "kind": "runtime.principal_player_routing",
                "campaign_id": "campaign-frostfall",
                "complete": True,
                "entries": [],
            }
        )
        result = resolve_player(
            _principal(),
            template,
            lambda _player_id: _player(),
            campaign_id="campaign-frostfall",
        )
        self.assertEqual(result.failure_code, AuthorizationFailureCode.ROUTE_ABSENT)


if __name__ == "__main__":
    unittest.main()
