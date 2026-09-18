"""Principal-to-PLAYER routing and fail-closed authorization witnesses."""

from __future__ import annotations

import base64
import hashlib
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
    FRAMEWORK_MODULE_VERSION,
    LiveClaim,
    LiveContractError,
    LiveEnvelope,
    LiveLifecycle,
    LivePublicationStatus,
    LiveRouting,
    LIVE_CLAIM_SCHEMA_VERSION,
    LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION,
    LIVE_ROUTING_SCHEMA_VERSION,
    SOURCE_NATIVE_CURSOR_MAX,
    SOURCE_NATIVE_LIVE_ENCODING,
    SourceNativeCursor,
    SourceNativeCreation,
    SourceNativeAllocationError,
    advance_source_native_cursor,
    allocate_source_native_creations,
    build_live_route,
    build_live_ref,
    classify_cas_result,
    close_live_source,
    derive_live_epoch_id,
    encode_live_campaign_route_token,
    encode_live_scene_route_token,
    encode_source_native_live_id,
    freeze_live_attempt,
    lookup_write_authority,
    normalize_source_native_creations,
    parse_source_native_live_id,
    reconcile_indeterminate,
    select_live_source,
    validate_live_route_identity,
    validate_exact_source,
)


ROOT = Path(__file__).resolve().parents[2]
ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
LIVE_ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/LIVE_ROUTING.yaml"


LIVE_H0 = "0" * 40
LIVE_H1 = "1" * 40
LIVE_H2 = "2" * 40
SOURCE_NATIVE_POLICY = {
    "world": {
        "world.actor": {
            "strategy": "sequential",
            "prefix": "actor",
            "live_birth": {
                "disposition": "source_native_live",
                "encoding": "framed_base32hex_v1",
            },
        },
        "world.asset": {
            "strategy": "sequential",
            "prefix": "asset",
            "live_birth": {
                "disposition": "source_native_live",
                "encoding": "framed_base32hex_v1",
            },
        },
    },
    "runtime": {
        "runtime.message": {
            "strategy": "sequential",
            "prefix": "message",
            "live_birth": {
                "disposition": "source_native_live",
                "encoding": "framed_base32hex_v1",
            },
        },
    },
}
PRE_T03_LIVE_SCENE_SCHEMA_SHA256 = (
    "0e5cceac5b29d1bcad1fcfe5779905092402d1c8b00d9c3d04157a822ceb5638"
)


def _live_source(
    *,
    revision: str = LIVE_H0,
    status: LiveLifecycle = LiveLifecycle.ACTIVE,
    claims: tuple[LiveClaim, ...] | None = None,
    next_source_native_creation_ordinal: int = 1,
    source_native_ids: tuple[str, ...] = (),
) -> LiveEnvelope:
    selected_claims = claims if claims is not None else (
        LiveClaim.exact_owner("world.actor", "actor-1"),
    )
    opening_revision = LIVE_H0
    epoch_id = derive_live_epoch_id(
        "campaign-frostfall", "scene-market", opening_revision, selected_claims
    )
    return LiveEnvelope(
        campaign_id="campaign-frostfall",
        scene_id="scene-market",
        epoch_id=epoch_id,
        opening_campaign_revision=opening_revision,
        source_ref=build_live_ref("campaign-frostfall", "scene-market", epoch_id),
        source_revision=revision,
        claims=selected_claims,
        status=status,
        next_source_native_creation_ordinal=next_source_native_creation_ordinal,
        source_native_ids=source_native_ids,
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
        self.assertIn("schema_version: 4", LIVE_ROUTE_TEMPLATE.read_text(encoding="utf-8"))
        self.assertIn("entries: []", LIVE_ROUTE_TEMPLATE.read_text(encoding="utf-8"))

    def test_live_source_key_is_exact_campaign_scene_epoch_tuple(self) -> None:
        source = _live_source()

        self.assertEqual(
            source.source_key,
            ("campaign-frostfall", "scene-market", source.epoch_id),
        )
        self.assertEqual(source.claims[0].as_mapping(), {
            "schema_version": 2,
            "claim_type": "EXACT_OWNER",
            "native_family": "world.actor",
            "native_identity": "actor-1",
        })

    def test_claim_grammar_is_typed_and_closed(self) -> None:
        self.assertEqual(
            LiveClaim.exact_owner("world.actor", "actor-1").as_mapping(),
            {
                "schema_version": 2,
                "claim_type": "EXACT_OWNER",
                "native_family": "world.actor",
                "native_identity": "actor-1",
            },
        )
        for factory in (
            lambda: LiveClaim.epoch_local_creation("world.asset"),
            lambda: LiveClaim.owner_defined_partition("scene", "scene-market"),
        ):
            with self.assertRaisesRegex(LiveContractError, "owner-backed|non-exact"):
                factory()
        with self.assertRaisesRegex(LiveContractError, "typed|wildcard|claim"):
            LiveClaim.from_mapping({
                "claim_type": "PATH_GLOB",
                "path": "WORLD/**",
            })

    def test_creation_and_partition_claims_require_owner_admission(self) -> None:
        with self.assertRaisesRegex(
            LiveContractError, "admitted|creation|partition|owner-backed|non-exact"
        ):
            LiveClaim.epoch_local_creation("world.unknown")

        with self.assertRaisesRegex(
            LiveContractError, "admitted|owner|partition|owner-backed|non-exact"
        ):
            LiveClaim.owner_defined_partition("arbitrary", "unowned")

    def test_non_exact_claims_have_no_current_owner_backed_contract(self) -> None:
        with self.assertRaisesRegex(LiveContractError, "owner-backed|non-exact"):
            LiveClaim.epoch_local_creation("world.asset")
        with self.assertRaisesRegex(LiveContractError, "owner-backed|non-exact"):
            LiveClaim.owner_defined_partition("scene", "scene-market")

    def test_schema_and_python_fail_closed_together_for_unadmitted_creation_claim(self) -> None:
        schema = json.loads(
            (ROOT / "DEV/SCHEMAS/live-claim.schema.json").read_text(encoding="utf-8")
        )
        claim = {
            "claim_type": "EPOCH_LOCAL_CREATION",
            "native_family": "world.asset",
        }

        self.assertFalse(Draft202012Validator(schema).is_valid(claim))
        with self.assertRaises(LiveContractError):
            LiveClaim.from_mapping(claim)

    def test_live_schema_versions_match_material_claim_language(self) -> None:
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

        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.5")
        self.assertEqual(LIVE_CLAIM_SCHEMA_VERSION, 2)
        self.assertEqual(LIVE_ROUTING_SCHEMA_VERSION, 4)
        self.assertEqual(LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION, 5)
        self.assertEqual(claim_schema["properties"]["schema_version"]["const"], 2)
        self.assertEqual(route_schema["properties"]["schema_version"]["const"], 4)
        self.assertEqual(publication_schema["properties"]["schema_version"]["const"], 5)

    def test_w03_does_not_edit_wave05_retained_live_scene_schema(self) -> None:
        retained_schema = ROOT / "GAME/SCHEMA/live_scene.schema.yaml"

        self.assertEqual(
            hashlib.sha256(retained_schema.read_bytes()).hexdigest(),
            PRE_T03_LIVE_SCENE_SCHEMA_SHA256,
        )

    def test_schema_and_python_reject_illegal_claim_companion_fields(self) -> None:
        schema = json.loads(
            (ROOT / "DEV/SCHEMAS/live-claim.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        invalid_claims = (
            {
                "schema_version": 2,
                "claim_type": "EXACT_OWNER",
                "native_family": "world.actor",
                "native_identity": "actor-1",
                "partition_key": "scene-market",
            },
            {
                "schema_version": 2,
                "claim_type": "EPOCH_LOCAL_CREATION",
                "native_family": "world.actor",
                "partition_key": "scene-market",
            },
            {
                "schema_version": 2,
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
        with self.assertRaisesRegex(LiveContractError, "owner-backed|non-exact"):
            LiveClaim.owner_defined_partition("scene", "scene-market")

    def test_selected_creation_family_claims_cannot_overlap_across_route_entries(self) -> None:
        with self.assertRaisesRegex(LiveContractError, "owner-backed|non-exact"):
            LiveClaim.epoch_local_creation("world.asset")

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
            opening_campaign_revision=selected.opening_campaign_revision,
            source_ref="live/other-source",
            source_revision=selected.source_revision,
            claims=selected.claims,
        )
        wrong_key = LiveEnvelope(
            campaign_id=selected.campaign_id,
            scene_id="scene-other",
            epoch_id=selected.epoch_id,
            opening_campaign_revision=selected.opening_campaign_revision,
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


def _frame_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return len(encoded).to_bytes(4, "big") + encoded


def _reference_claim_frame(claim: LiveClaim) -> bytes:
    if claim.claim_type != "EXACT_OWNER":
        raise AssertionError("the T03 reference fixture intentionally uses exact-owner claims")
    identity = (claim.native_identity or "").encode("utf-8")
    return (
        b"\x01"
        + _frame_string(claim.native_family or "")
        + len((identity,)).to_bytes(4, "big")
        + len(identity).to_bytes(4, "big")
        + identity
    )


def _reference_epoch_id(
    campaign_id: str,
    scene_id: str,
    opening_campaign_revision: str,
    claims: tuple[LiveClaim, ...],
) -> str:
    claim_frames = tuple(sorted(_reference_claim_frame(claim) for claim in claims))
    frame = (
        b"HDM-LIVE-EPOCH-ID-V1\x00"
        + _frame_string(campaign_id)
        + _frame_string(scene_id)
        + _frame_string(opening_campaign_revision)
        + len(claim_frames).to_bytes(4, "big")
        + b"".join(len(frame).to_bytes(4, "big") + frame for frame in claim_frames)
    )
    return "e1-" + hashlib.sha256(frame).hexdigest()


class LiveCampaignRouteIdentityTests(unittest.TestCase):
    def test_campaign_route_token_uses_full_domain_separated_utf8_digest(self) -> None:
        campaign_id = "Кампания/../α:live1:"
        expected = "c1-" + hashlib.sha256(
            b"HDM-LIVE-CAMPAIGN-ROUTE-V1\x00" + _frame_string(campaign_id)
        ).hexdigest()

        token = encode_live_campaign_route_token(campaign_id)

        self.assertEqual(token, expected)
        self.assertRegex(token, r"^c1-[0-9a-f]{64}$")
        self.assertEqual(len(token.removeprefix("c1-")), 64)
        self.assertNotIn("Кампания", token)
        self.assertNotIn("/", token)

    def test_delimiter_like_and_near_collision_campaign_ids_are_distinct_routes(self) -> None:
        first = encode_live_campaign_route_token("campaign/a:b")
        second = encode_live_campaign_route_token("campaign/a: b")
        third = encode_live_campaign_route_token("campaign/a:b\x00")

        self.assertEqual(len({first, second, third}), 3)

    def test_physical_token_does_not_replace_semantic_campaign_identity(self) -> None:
        campaign_id = "campaign/semantic"
        token = encode_live_campaign_route_token(campaign_id)

        self.assertNotEqual(token, campaign_id)
        self.assertEqual(
            build_live_ref(campaign_id, "scene/semantic", "e1-" + "a" * 64).split("/")[1],
            token,
        )


class LiveEpochRouteIdentityTests(unittest.TestCase):
    def test_epoch_id_matches_exact_full_basis_framing_and_is_order_insensitive(self) -> None:
        claims = (
            LiveClaim.exact_owner("world.actor", "actor-2"),
            LiveClaim.exact_owner("world.actor", "actor-1"),
        )
        expected = _reference_epoch_id(
            "campaign/α", "scene:live1:market", "f" * 40, claims
        )

        epoch_id = derive_live_epoch_id(
            "campaign/α", "scene:live1:market", "f" * 40, claims
        )
        reordered = derive_live_epoch_id(
            "campaign/α", "scene:live1:market", "f" * 40, tuple(reversed(claims))
        )

        self.assertEqual(epoch_id, expected)
        self.assertEqual(epoch_id, reordered)
        self.assertRegex(epoch_id, r"^e1-[0-9a-f]{64}$")

    def test_epoch_id_changes_for_each_semantic_opening_basis_component(self) -> None:
        claim = LiveClaim.exact_owner("world.actor", "actor-1")
        base = derive_live_epoch_id("campaign-1", "scene-1", "a" * 40, (claim,))

        self.assertNotEqual(
            base, derive_live_epoch_id("campaign-2", "scene-1", "a" * 40, (claim,))
        )
        self.assertNotEqual(
            base, derive_live_epoch_id("campaign-1", "scene-2", "a" * 40, (claim,))
        )
        self.assertNotEqual(
            base, derive_live_epoch_id("campaign-1", "scene-1", "b" * 40, (claim,))
        )
        self.assertNotEqual(
            base,
            derive_live_epoch_id(
                "campaign-1",
                "scene-1",
                "a" * 40,
                (LiveClaim.exact_owner("world.actor", "actor-2"),),
            ),
        )

    def test_duplicate_claim_frames_and_wrong_epoch_version_fail_closed(self) -> None:
        claim = LiveClaim.exact_owner("world.actor", "actor-1")

        with self.assertRaisesRegex(LiveContractError, "duplicate|claim"):
            derive_live_epoch_id("campaign-1", "scene-1", "a" * 40, (claim, claim))
        with self.assertRaisesRegex(LiveContractError, "epoch|version|e1"):
            build_live_ref("campaign-1", "scene-1", "e0-" + "a" * 64)

    def test_scene_route_token_and_live_ref_use_safe_versioned_components(self) -> None:
        scene_id = "scene/market:α"
        scene_token = encode_live_scene_route_token(scene_id)
        epoch_id = "e1-" + "b" * 64

        self.assertRegex(scene_token, r"^s1-[0-9a-f]{64}$")
        self.assertEqual(
            build_live_ref("campaign/market", scene_id, epoch_id),
            "live/"
            + encode_live_campaign_route_token("campaign/market")
            + "/"
            + scene_token
            + "/"
            + epoch_id
            + "/LIVE/LIVE_STATE.yaml",
        )
        self.assertNotIn(scene_id, build_live_ref("campaign/market", scene_id, epoch_id))


class SceneLiveRouteProjectionTests(unittest.TestCase):
    def _source(self) -> LiveEnvelope:
        claims = (LiveClaim.exact_owner("world.actor", "actor-1"),)
        opening_revision = "a" * 40
        epoch_id = derive_live_epoch_id("campaign-1", "scene-1", opening_revision, claims)
        physical_ref = build_live_ref("campaign-1", "scene-1", epoch_id)
        return LiveEnvelope(
            campaign_id="campaign-1",
            scene_id="scene-1",
            epoch_id=epoch_id,
            opening_campaign_revision=opening_revision,
            source_ref=physical_ref,
            source_revision="b" * 40,
            claims=claims,
        )

    def test_route_load_revalidates_body_tuple_and_opening_basis(self) -> None:
        source = self._source()
        route = build_live_route(source.campaign_id, (source,))

        validate_live_route_identity(route, source.as_mapping(), source.source_ref)

        wrong_body = source.as_mapping() | {"scene_id": "scene-other"}
        with self.assertRaisesRegex(LiveContractError, "identity|tuple|scene"):
            validate_live_route_identity(route, wrong_body, source.source_ref)

    def test_route_token_equality_cannot_override_wrong_body_or_version(self) -> None:
        source = self._source()
        route = build_live_route(source.campaign_id, (source,))
        wrong_campaign_body = source.as_mapping() | {"campaign_id": "campaign-other"}
        wrong_version_ref = source.source_ref.replace("/c1-", "/c0-", 1)

        with self.assertRaisesRegex(LiveContractError, "identity|campaign"):
            validate_live_route_identity(route, wrong_campaign_body, source.source_ref)
        with self.assertRaisesRegex(LiveContractError, "route|version|physical"):
            validate_live_route_identity(route, source.as_mapping(), wrong_version_ref)

    def test_route_mapping_load_rejects_a_body_tuple_alias(self) -> None:
        source = self._source()
        raw_route = build_live_route(source.campaign_id, (source,)).as_mapping()
        raw_route["entries"] = [source.as_mapping() | {"epoch_id": "e1-" + "c" * 64}]

        with self.assertRaisesRegex(LiveContractError, "identity|basis|route"):
            LiveRouting.from_mapping(raw_route)

    def test_semantic_source_key_is_stable_when_physical_route_is_derived(self) -> None:
        source = self._source()

        self.assertEqual(source.source_key, ("campaign-1", "scene-1", source.epoch_id))
        self.assertNotIn(source.campaign_id, source.source_ref)
        self.assertNotIn(source.scene_id, source.source_ref)


class SourceNativeIdentityTests(unittest.TestCase):
    def test_source_native_identity_is_bound_to_the_exact_live_source_key(self) -> None:
        source_key = ("campaign/α", "scene:market", "e1-" + "a" * 64)

        native_id = encode_source_native_live_id(
            source_key,
            "world.actor",
            1,
            SOURCE_NATIVE_POLICY,
        )
        parsed = parse_source_native_live_id(native_id, SOURCE_NATIVE_POLICY)

        self.assertEqual(parsed.live_source_key, source_key)
        self.assertEqual(parsed.native_family, "world.actor")
        self.assertEqual(parsed.source_local_creation_ordinal, 1)
        self.assertEqual(parsed.encoding, SOURCE_NATIVE_LIVE_ENCODING)

    def test_transport_revision_wall_clock_and_host_do_not_enter_identity(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "b" * 64)

        first = encode_source_native_live_id(
            source_key,
            "world.actor",
            4,
            SOURCE_NATIVE_POLICY,
        )
        second = encode_source_native_live_id(
            source_key,
            "world.actor",
            4,
            SOURCE_NATIVE_POLICY,
        )

        self.assertEqual(first, second)
        self.assertNotIn(LIVE_H0, first)
        self.assertNotIn("2026-09-18", first)

    def test_identity_components_are_injective_for_accepted_coordinates(self) -> None:
        base = ("campaign-1", "scene-1", "e1-" + "c" * 64)
        values = {
            encode_source_native_live_id(base, "world.actor", 1, SOURCE_NATIVE_POLICY),
            encode_source_native_live_id(("campaign-2", *base[1:]), "world.actor", 1, SOURCE_NATIVE_POLICY),
            encode_source_native_live_id(base, "world.asset", 1, SOURCE_NATIVE_POLICY),
            encode_source_native_live_id(base, "world.actor", 2, SOURCE_NATIVE_POLICY),
        }

        self.assertEqual(len(values), 4)


class SourceNativeLiveIdEncodingTests(unittest.TestCase):
    def test_known_vector_uses_domain_framing_and_unpadded_lowercase_base32hex(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "d" * 64)
        frame = (
            b"HDM-LIVE-ID-V1\x00"
            + _frame_string(source_key[0])
            + _frame_string(source_key[1])
            + _frame_string(source_key[2])
            + _frame_string("world.actor")
            + (1).to_bytes(8, "big")
        )
        expected = "actor:live1:" + base64.b32hexencode(frame).decode("ascii").rstrip("=").lower()

        self.assertEqual(
            encode_source_native_live_id(source_key, "world.actor", 1, SOURCE_NATIVE_POLICY),
            expected,
        )

    def test_malformed_padding_version_and_family_prefix_fail_closed(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "e" * 64)
        native_id = encode_source_native_live_id(
            source_key,
            "world.actor",
            1,
            SOURCE_NATIVE_POLICY,
        )

        for invalid in (
            native_id + "=",
            native_id.replace(":live1:", ":live0:", 1),
            native_id.replace("actor:live1:", "asset:live1:", 1),
            native_id.upper(),
        ):
            with self.assertRaisesRegex(LiveContractError, "identity|encoding|ID|base32"):
                parse_source_native_live_id(invalid, SOURCE_NATIVE_POLICY)

    def test_missing_or_non_source_native_policy_cannot_allocate(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "f" * 64)
        missing = {"world": {"world.actor": {"prefix": "actor"}}}

        with self.assertRaisesRegex(LiveContractError, "policy|source_native_live|encoding|disposition"):
            encode_source_native_live_id(source_key, "world.actor", 1, missing)


class SourceNativeCreationOrderingTests(unittest.TestCase):
    def test_normalization_sorts_by_native_family_utf8_bytes_then_owner_local_index(self) -> None:
        creations = (
            SourceNativeCreation("world.asset", 2),
            SourceNativeCreation("world.actor", 9),
            SourceNativeCreation("world.actor", 1),
        )

        normalized = normalize_source_native_creations(tuple(reversed(creations)))

        self.assertEqual(
            [(item.native_family, item.owner_local_index) for item in normalized],
            [("world.actor", 1), ("world.actor", 9), ("world.asset", 2)],
        )

    def test_duplicate_owner_local_index_within_one_native_family_fails(self) -> None:
        with self.assertRaisesRegex(LiveContractError, "duplicate|owner-local|index"):
            normalize_source_native_creations(
                (
                    SourceNativeCreation("world.actor", 1),
                    SourceNativeCreation("world.actor", 1),
                )
            )

    def test_reordered_inputs_receive_the_same_slots_ordinals_and_ids(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "1" * 64)
        creations = (
            SourceNativeCreation("world.asset", 2),
            SourceNativeCreation("world.actor", 1),
        )

        first = allocate_source_native_creations(
            source_key, creations, SourceNativeCursor(1), SOURCE_NATIVE_POLICY
        )
        second = allocate_source_native_creations(
            source_key, tuple(reversed(creations)), SourceNativeCursor(1), SOURCE_NATIVE_POLICY
        )

        self.assertEqual(first, second)
        self.assertEqual([item.creation_slot_index for item in first], [0, 1])
        self.assertEqual(
            [item.source_local_creation_ordinal for item in first],
            [1, 2],
        )


class LiveSourceCreationCursorTests(unittest.TestCase):
    def test_cursor_is_uint64_and_starts_at_one(self) -> None:
        cursor = SourceNativeCursor()

        self.assertEqual(cursor.next_ordinal, 1)
        self.assertEqual(cursor.value, 1)
        with self.assertRaisesRegex(SourceNativeAllocationError, "uint64|cursor"):
            SourceNativeCursor(SOURCE_NATIVE_CURSOR_MAX + 1)

    def test_accepted_exact_source_cas_advances_cursor_once_for_the_batch(self) -> None:
        source = _live_source()
        route = _live_route(source)
        attempt = freeze_live_attempt(
            source,
            route=route,
            proposed_source_revision=LIVE_H1,
            source_native_creations=(
                SourceNativeCreation("world.actor", 1),
                SourceNativeCreation("world.asset", 1),
            ),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        result = classify_cas_result(attempt, _accepted_ack(attempt) | {
            "source_native_allocations": [
                allocation.as_mapping() for allocation in attempt.source_native_allocations
            ],
            "expected_next_source_native_creation_ordinal": 1,
            "proposed_next_source_native_creation_ordinal": 3,
        })

        self.assertEqual(result.status, LivePublicationStatus.ACCEPTED)
        self.assertEqual(advance_source_native_cursor(SourceNativeCursor(1), result), SourceNativeCursor(3))

    def test_cursor_exhaustion_fails_without_reuse_or_wrap(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "2" * 64)

        with self.assertRaisesRegex(SourceNativeAllocationError, "overflow|exhaust"):
            allocate_source_native_creations(
                source_key,
                (
                    SourceNativeCreation("world.actor", 1),
                    SourceNativeCreation("world.actor", 2),
                ),
                SourceNativeCursor(SOURCE_NATIVE_CURSOR_MAX),
                SOURCE_NATIVE_POLICY,
            )

    def test_rejected_or_indeterminate_cas_does_not_advance_cursor(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        stale = classify_cas_result(
            attempt,
            {
                "accepted": False,
                "source_key": source.source_key,
                "current_source_revision": LIVE_H1,
            },
        )
        indeterminate = classify_cas_result(attempt, None)

        self.assertEqual(advance_source_native_cursor(SourceNativeCursor(1), stale), SourceNativeCursor(1))
        self.assertEqual(
            advance_source_native_cursor(SourceNativeCursor(1), indeterminate),
            SourceNativeCursor(1),
        )


class SourceNativeAmbiguousPublicationTests(unittest.TestCase):
    def test_indeterminate_ack_reconciles_original_allocations_before_reallocation(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        successor = attempt.successor_route.entries[0]

        result = reconcile_indeterminate(attempt, successor)

        self.assertEqual(result.status, LivePublicationStatus.ACCEPTED)
        self.assertEqual(result.source_native_allocations, attempt.source_native_allocations)
        self.assertEqual(result.proposed_next_source_native_creation_ordinal, 2)

    def test_accepted_response_loss_preserves_frozen_ids_and_cursor(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        result = reconcile_indeterminate(attempt, attempt.successor_route.entries[0])

        self.assertEqual(result.source_native_ids, tuple(item.native_id for item in attempt.source_native_allocations))
        self.assertEqual(advance_source_native_cursor(SourceNativeCursor(1), result), SourceNativeCursor(2))

    def test_unresolved_acknowledgement_cannot_allocate_a_second_identity(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )

        result = reconcile_indeterminate(attempt, _live_source(revision=LIVE_H0))

        self.assertEqual(result.status, LivePublicationStatus.INDETERMINATE)
        self.assertEqual(result.source_native_allocations, ())
        self.assertEqual(advance_source_native_cursor(SourceNativeCursor(1), result), SourceNativeCursor(1))


if __name__ == "__main__":
    unittest.main()
