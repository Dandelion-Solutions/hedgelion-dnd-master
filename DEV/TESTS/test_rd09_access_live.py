"""Principal-to-PLAYER routing and fail-closed authorization witnesses."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, RefResolver

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
from GAME.TOOLS.live_state import (
    LiveClaim,
    LiveClaimAdmission,
    LiveContractError,
    LiveEnvelope,
    LiveLifecycle,
    LivePublicationStatus,
    build_live_route,
    classify_cas_result,
    close_live_source,
    freeze_live_attempt,
    lookup_write_authority,
    reconcile_indeterminate,
    select_live_source,
    validate_exact_source,
)


ROOT = Path(__file__).resolve().parents[2]
ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
LIVE_ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/LIVE_ROUTING.yaml"


LIVE_H0 = "0" * 40
LIVE_H1 = "1" * 40
LIVE_H2 = "2" * 40


def _live_source(
    *,
    revision: str = LIVE_H0,
    status: LiveLifecycle = LiveLifecycle.ACTIVE,
    claims: tuple[LiveClaim, ...] | None = None,
) -> LiveEnvelope:
    return LiveEnvelope(
        campaign_id="campaign-frostfall",
        scene_id="scene-market",
        epoch_id="epoch-1",
        source_ref="live/campaign-frostfall/scene-market/epoch-1",
        source_revision=revision,
        claims=claims
        if claims is not None
        else (LiveClaim.exact_owner("world.actor", "actor-1"),),
        status=status,
    )


def _live_route(source: LiveEnvelope | None = None):
    selected = _live_source() if source is None else source
    return build_live_route(selected.campaign_id, (selected,))


def _accepted_ack(attempt: object) -> dict[str, object]:
    return {
        "accepted": True,
        "source_key": attempt.source_key,  # type: ignore[attr-defined]
        "target_ref": attempt.target_ref,  # type: ignore[attr-defined]
        "expected_source_revision": attempt.expected_source_revision,  # type: ignore[attr-defined]
        "new_source_revision": attempt.proposed_source_revision,  # type: ignore[attr-defined]
        "selected_route": attempt.selected_route.as_mapping(),  # type: ignore[attr-defined]
        "successor": attempt.successor_route.as_mapping(),  # type: ignore[attr-defined]
    }


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


class LiveEnvelopeClaimTests(unittest.TestCase):
    def test_live_machine_schemas_and_blank_route_are_present_and_strict(self) -> None:
        schema_dir = ROOT / "DEV/SCHEMAS"
        claim_schema = json.loads(
            (schema_dir / "live-claim.schema.json").read_text(encoding="utf-8")
        )
        route_schema = json.loads(
            (schema_dir / "live-routing.schema.json").read_text(encoding="utf-8")
        )
        publication_schema = json.loads(
            (schema_dir / "live-publication-attempt.schema.json").read_text(encoding="utf-8")
        )
        for schema in (claim_schema, route_schema, publication_schema):
            Draft202012Validator.check_schema(schema)

        route = build_live_route("campaign-frostfall", (_live_source(),))
        route_validator = Draft202012Validator(
            route_schema,
            resolver=RefResolver.from_schema(
                route_schema,
                store={claim_schema["$id"]: claim_schema},
            ),
        )
        self.assertFalse(list(route_validator.iter_errors(route.as_mapping())))
        source = _live_source()
        publication = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
        )
        publication_validator = Draft202012Validator(
            publication_schema,
            resolver=RefResolver.from_schema(
                publication_schema,
                store={
                    claim_schema["$id"]: claim_schema,
                    route_schema["$id"]: route_schema,
                },
            ),
        )
        self.assertFalse(list(publication_validator.iter_errors(publication.as_mapping())))
        self.assertIn("kind: runtime.live_routing", LIVE_ROUTE_TEMPLATE.read_text(encoding="utf-8"))
        self.assertIn("entries: []", LIVE_ROUTE_TEMPLATE.read_text(encoding="utf-8"))

    def test_live_source_key_is_exact_campaign_scene_epoch_tuple(self) -> None:
        source = _live_source()

        self.assertEqual(
            source.source_key,
            ("campaign-frostfall", "scene-market", "epoch-1"),
        )
        self.assertEqual(source.claims[0].as_mapping(), {
            "claim_type": "EXACT_OWNER",
            "native_family": "world.actor",
            "native_identity": "actor-1",
        })

    def test_claim_grammar_is_typed_and_closed(self) -> None:
        admission = LiveClaimAdmission(creation_families=frozenset({"world.asset"}))
        self.assertEqual(
            LiveClaim.epoch_local_creation("world.asset", admission=admission).as_mapping(),
            {
                "claim_type": "EPOCH_LOCAL_CREATION",
                "native_family": "world.asset",
            },
        )
        self.assertEqual(
            LiveClaim.owner_defined_partition(
                "scene",
                "scene-market",
                admission=LiveClaimAdmission(
                    owner_defined_partitions=frozenset({("scene", "scene-market")})
                ),
            ).as_mapping(),
            {
                "claim_type": "OWNER_DEFINED_PARTITION",
                "partition_type": "scene",
                "partition_key": "scene-market",
            },
        )
        with self.assertRaisesRegex(LiveContractError, "typed|wildcard|claim"):
            LiveClaim.from_mapping({
                "claim_type": "PATH_GLOB",
                "path": "WORLD/**",
            })

    def test_creation_and_partition_claims_require_owner_admission(self) -> None:
        with self.assertRaisesRegex(LiveContractError, "admitted|creation|partition"):
            LiveClaim.epoch_local_creation("world.unknown")

        with self.assertRaisesRegex(LiveContractError, "admitted|owner|partition"):
            LiveClaim.owner_defined_partition("arbitrary", "unowned")

    def test_schema_and_python_reject_illegal_claim_companion_fields(self) -> None:
        schema = json.loads(
            (ROOT / "DEV/SCHEMAS/live-claim.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        invalid_claims = (
            {
                "claim_type": "EXACT_OWNER",
                "native_family": "world.actor",
                "native_identity": "actor-1",
                "partition_key": "scene-market",
            },
            {
                "claim_type": "EPOCH_LOCAL_CREATION",
                "native_family": "world.actor",
                "partition_key": "scene-market",
            },
            {
                "claim_type": "OWNER_DEFINED_PARTITION",
                "partition_type": "scene",
                "partition_key": "scene-market",
                "native_identity": "actor-1",
            },
        )

        for claim in invalid_claims:
            self.assertTrue(list(validator.iter_errors(claim)))
            with self.assertRaises(LiveContractError):
                LiveClaim.from_mapping(claim)

    def test_campaign_and_access_authority_cannot_be_live_claimed(self) -> None:
        for factory in (
            lambda: LiveClaim.exact_owner("world.player", "player-1"),
            lambda: LiveClaim.epoch_local_creation("runtime.session"),
        ):
            with self.assertRaisesRegex(LiveContractError, "claim|authority|admitted"):
                factory()

    def test_selected_claims_are_unique_and_do_not_expand_by_reference(self) -> None:
        with self.assertRaisesRegex(LiveContractError, "duplicate|overlap"):
            _live_source(
                claims=(
                    LiveClaim.exact_owner("world.actor", "actor-1"),
                    LiveClaim.exact_owner("world.actor", "actor-1"),
                )
            )

        source = _live_source(
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),)
        )
        self.assertFalse(source.claims_contain("world.asset", "asset-1"))

    def test_selected_partition_claims_cannot_overlap_across_route_entries(self) -> None:
        admission = LiveClaimAdmission(
            owner_defined_partitions=frozenset(
                {("scene", "scene-market"), ("scene", "scene-market-2")}
            )
        )
        first = _live_source(
            claims=(
                LiveClaim.owner_defined_partition(
                    "scene", "scene-market", admission=admission
                ),
            )
        )
        second = LiveEnvelope(
            campaign_id=first.campaign_id,
            scene_id="scene-other",
            epoch_id=first.epoch_id,
            source_ref="live/campaign-frostfall/scene-other/epoch-1",
            source_revision=LIVE_H1,
            claims=(
                LiveClaim.owner_defined_partition(
                    "scene", "scene-market-2", admission=admission
                ),
            ),
        )

        with self.assertRaisesRegex(LiveContractError, "overlap"):
            build_live_route("campaign-frostfall", (first, second))

    def test_prepared_source_is_not_selected_without_exact_route_entry(self) -> None:
        prepared = _live_source(revision=LIVE_H1)
        route = build_live_route("campaign-frostfall", ())

        self.assertIsNone(select_live_source(route, prepared.source_key))
        self.assertEqual(
            lookup_write_authority("world.actor", "actor-1", route),
            "CAMPAIGN",
        )


class LiveCurrentnessTests(unittest.TestCase):
    def test_selected_source_requires_exact_source_revision(self) -> None:
        selected = _live_source()
        self.assertTrue(validate_exact_source(selected, selected))
        self.assertFalse(validate_exact_source(selected, _live_source(revision=LIVE_H1)))

    def test_source_ref_and_key_are_part_of_exact_currentness(self) -> None:
        selected = _live_source()
        wrong_ref = LiveEnvelope(
            campaign_id=selected.campaign_id,
            scene_id=selected.scene_id,
            epoch_id=selected.epoch_id,
            source_ref="live/other-source",
            source_revision=selected.source_revision,
            claims=selected.claims,
        )
        wrong_key = LiveEnvelope(
            campaign_id=selected.campaign_id,
            scene_id="scene-other",
            epoch_id=selected.epoch_id,
            source_ref=selected.source_ref,
            source_revision=selected.source_revision,
            claims=selected.claims,
        )

        self.assertFalse(validate_exact_source(selected, wrong_ref))
        self.assertFalse(validate_exact_source(selected, wrong_key))

    def test_newest_timestamp_and_commit_existence_do_not_fallback_to_authority(self) -> None:
        selected = _live_source()
        latest_looking = {
            "campaign_id": selected.campaign_id,
            "scene_id": selected.scene_id,
            "epoch_id": selected.epoch_id,
            "source_ref": selected.source_ref,
            "source_revision": LIVE_H1,
            "timestamp": "9999-12-31T23:59:59Z",
            "commit_exists": True,
        }

        self.assertFalse(validate_exact_source(selected, latest_looking))
        self.assertIsNone(select_live_source(latest_looking, selected.source_key))

    def test_parallel_candidate_loses_against_the_accepted_exact_predecessor(self) -> None:
        selected = _live_source()
        route = _live_route(selected)
        first = freeze_live_attempt(
            selected, route=route, proposed_source_revision=LIVE_H1
        )
        second = freeze_live_attempt(
            selected, route=route, proposed_source_revision=LIVE_H2
        )

        accepted = classify_cas_result(first, _accepted_ack(first))
        stale = classify_cas_result(
            second,
            {
                "accepted": False,
                "source_key": selected.source_key,
                "expected_source_revision": LIVE_H0,
                "current_source_revision": LIVE_H1,
                "reason": "stale_predecessor",
            },
        )

        self.assertEqual(accepted.status, LivePublicationStatus.ACCEPTED)
        self.assertEqual(stale.status, LivePublicationStatus.REJECTED_STALE)

    def test_non_monotonic_source_transition_is_rejected(self) -> None:
        selected = _live_source()

        with self.assertRaisesRegex(LiveContractError, "monotonic|predecessor|revision"):
            freeze_live_attempt(
                selected, route=_live_route(selected), proposed_source_revision=LIVE_H0
            )


class LivePublicationTests(unittest.TestCase):
    def test_freeze_requires_exact_selected_route_evidence(self) -> None:
        source = _live_source()
        route = build_live_route("campaign-frostfall", ())

        with self.assertRaisesRegex(LiveContractError, "route|selected|current"):
            freeze_live_attempt(
                source,
                route=route,
                proposed_source_revision=LIVE_H1,
            )

    def test_frozen_attempt_binds_selected_source_and_is_immutable(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            transition_kind="MUTATION",
        )

        self.assertEqual(attempt.source_key, source.source_key)
        self.assertEqual(attempt.expected_source_revision, LIVE_H0)
        self.assertEqual(attempt.proposed_source_revision, LIVE_H1)
        with self.assertRaises(AttributeError):
            attempt.expected_source_revision = LIVE_H2  # type: ignore[misc]

    def test_ambiguous_acknowledgement_is_not_success(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source, route=_live_route(source), proposed_source_revision=LIVE_H1
        )

        result = classify_cas_result(attempt, None)

        self.assertEqual(result.status, LivePublicationStatus.INDETERMINATE)
        self.assertFalse(result.authoritative)

    def test_accepted_acknowledgement_requires_complete_selected_successor_closure(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source, route=_live_route(source), proposed_source_revision=LIVE_H1
        )

        result = classify_cas_result(
            attempt,
            {
                "accepted": True,
                "source_key": attempt.source_key,
                "target_ref": attempt.target_ref,
                "expected_source_revision": attempt.expected_source_revision,
                "new_source_revision": attempt.proposed_source_revision,
            },
        )

        self.assertNotEqual(result.status, LivePublicationStatus.ACCEPTED)

    def test_indeterminate_ack_requires_exact_current_source_reconciliation(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source, route=_live_route(source), proposed_source_revision=LIVE_H1
        )

        accepted = reconcile_indeterminate(attempt, _live_source(revision=LIVE_H1))
        unresolved = reconcile_indeterminate(attempt, _live_source(revision=LIVE_H0))
        rejected = reconcile_indeterminate(attempt, _live_source(revision=LIVE_H2))

        self.assertEqual(accepted.status, LivePublicationStatus.ACCEPTED)
        self.assertTrue(accepted.authoritative)
        self.assertEqual(unresolved.status, LivePublicationStatus.INDETERMINATE)
        self.assertEqual(rejected.status, LivePublicationStatus.REJECTED_STALE)

    def test_reconciliation_requires_complete_successor_source_evidence(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source, route=_live_route(source), proposed_source_revision=LIVE_H1
        )
        changed_claims = _live_source(
            revision=LIVE_H1,
            claims=(LiveClaim.exact_owner("world.actor", "actor-2"),),
        )

        result = reconcile_indeterminate(attempt, changed_claims)

        self.assertNotEqual(result.status, LivePublicationStatus.ACCEPTED)

    def test_successful_local_write_without_selected_source_ack_is_not_authority(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source, route=_live_route(source), proposed_source_revision=LIVE_H1
        )

        result = classify_cas_result(
            attempt,
            {"local_write_succeeded": True, "new_source_revision": LIVE_H1},
        )

        self.assertEqual(result.status, LivePublicationStatus.INDETERMINATE)
        self.assertFalse(result.authoritative)


class LiveLifecycleTests(unittest.TestCase):
    def test_active_source_closes_only_from_its_exact_current_revision(self) -> None:
        source = _live_source()

        closed = close_live_source(
            source,
            expected_source_revision=LIVE_H0,
            closed_source_revision=LIVE_H1,
        )

        self.assertEqual(closed.status, LiveLifecycle.CLOSED)
        self.assertFalse(closed.ordinary_writes_allowed)
        self.assertTrue(
            validate_exact_source(
                closed,
                _live_source(revision=LIVE_H1, status=LiveLifecycle.CLOSED),
            )
        )

    def test_closed_source_never_reopens_or_accepts_ordinary_writes(self) -> None:
        closed = _live_source(revision=LIVE_H1, status=LiveLifecycle.CLOSED)

        with self.assertRaisesRegex(LiveContractError, "closed|reopen|ordinary"):
            freeze_live_attempt(
                closed, route=_live_route(closed), proposed_source_revision=LIVE_H2
            )
        with self.assertRaisesRegex(LiveContractError, "reopen|monotonic"):
            close_live_source(
                closed,
                expected_source_revision=LIVE_H1,
                closed_source_revision=LIVE_H2,
            )

    def test_closed_unabsorbed_remains_current_truth_without_write_authority(self) -> None:
        closed = _live_source(revision=LIVE_H1, status=LiveLifecycle.CLOSED_UNABSORBED)
        route = build_live_route("campaign-frostfall", (closed,))

        selected = select_live_source(route, closed.source_key)

        self.assertEqual(selected, closed)
        self.assertEqual(
            lookup_write_authority("world.actor", "actor-1", route),
            "INTEGRITY_CONFLICT",
        )

    def test_selected_closed_source_never_falls_back_to_campaign_authority(self) -> None:
        closed = _live_source(revision=LIVE_H1, status=LiveLifecycle.CLOSED)
        route = build_live_route("campaign-frostfall", (closed,))

        self.assertEqual(
            lookup_write_authority("world.actor", "actor-1", route),
            "INTEGRITY_CONFLICT",
        )

    def test_absorbed_source_is_not_selected_as_current_truth(self) -> None:
        absorbed = _live_source(revision=LIVE_H1, status=LiveLifecycle.ABSORBED)
        route = build_live_route("campaign-frostfall", (absorbed,))

        self.assertIsNone(select_live_source(route, absorbed.source_key))


if __name__ == "__main__":
    unittest.main()
