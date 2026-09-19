"""Principal-to-PLAYER routing and fail-closed authorization witnesses."""

from __future__ import annotations

import base64
import ast
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, RefResolver, ValidationError
import GAME.TOOLS.recovery_roots as recovery_roots_module
import GAME.TOOLS.access_control as access_control_module

from GAME.TOOLS.access_control import (
    AccessControlContractError,
    AdditiveAuthorizationDecision,
    AuthorizationFailureCode,
    FirstInitializationProvenance,
    PlayerRecord,
    PlayerResolution,
    PrincipalPlayerRoute,
    RouteEntry,
    VerifiedPrincipal,
    authorize_operation,
    build_principal_player_route,
    classify_additive_authorization_change,
    freeze_access_policy_transition,
    freeze_multi_live_forward_plan,
    freeze_player_access_transition,
    advance_multi_live_freeze,
    publish_access_policy_transition,
    publish_forward_transition,
    resolve_player,
    resolve_principal,
)
from GAME.TOOLS.history import HistoryContractError, _issue_verified_first_initialization_history
from GAME.TOOLS.live_state import (
    FRAMEWORK_MODULE_VERSION,
    LiveClaim,
    LiveContractError,
    LiveEnvelope,
    LiveLifecycle,
    LivePublicationResult,
    LivePublicationStatus,
    LiveRouting,
    LiveAbsorptionStatus,
    LiveAbsorptionPublication,
    FrozenCampaignAbsorption,
    LiveNativeStatePack,
    LIVE_ABSORPTION_ATTEMPT_SCHEMA_VERSION,
    LIVE_CLAIM_SCHEMA_VERSION,
    LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION,
    LIVE_OPENING_PREPARATION_SCHEMA_VERSION,
    LIVE_OPENING_SEED_SCHEMA_VERSION,
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
    build_live_opening_seed,
    classify_cas_result,
    classify_campaign_absorption,
    close_live_source,
    derive_live_epoch_id,
    encode_live_campaign_route_token,
    encode_live_scene_route_token,
    encode_source_native_live_id,
    freeze_live_attempt,
    freeze_campaign_absorption,
    handoff_temporal_route_to_campaign,
    handoff_temporal_route_to_live,
    handoff_operational_roots_to_campaign,
    lookup_write_authority,
    normalize_source_native_creations,
    parse_source_native_live_id,
    pack_live_native_state,
    prepare_live_opening,
    publish_live_opening,
    recover_closed_unabsorbed,
    reconcile_indeterminate,
    select_live_source,
    validate_live_route_identity,
    validate_live_route_completeness,
    validate_exact_source,
    absorb_live_state,
    mark_closed_unabsorbed,
    unpack_live_native_state,
)
from GAME.TOOLS.recovery_roots import (
    OperationalRootError,
    OperationalRoot,
    OperationalRootHandoff,
    OperationalRootPage,
    OPERATIONAL_ROOT_HANDOFF_SCHEMA_VERSION,
    derive_operational_root_delta,
    enumerate_operational_root_page,
    handoff_operational_roots_to_live,
)
from GAME.TOOLS.temporal import (
    derive_temporal_route_entry,
    enumerate_temporal_native_owners,
    rebuild_temporal_agenda_from_route,
    reconcile_temporal_route_membership,
)
from GAME.TOOLS.native_storage import route_native_record


ROOT = Path(__file__).resolve().parents[2]
ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml"
LIVE_ROUTE_TEMPLATE = ROOT / "GAME/CAMPAIGN/STATE/RUNTIME/LIVE_ROUTING.yaml"


LIVE_H0 = "0" * 40
LIVE_H1 = "1" * 40
LIVE_H2 = "2" * 40
LIVE_H3 = "3" * 40
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


def _empty_live_route() -> LiveRouting:
    return build_live_route("campaign-frostfall", ())


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


def _creator_provenance(
    *, campaign_id: str = "campaign-frostfall", author_login: str = "creator"
) -> FirstInitializationProvenance:
    return _issue_verified_first_initialization_history(
        campaign_id=campaign_id,
        author_login=author_login,
        initialization_revision=LIVE_H0,
        parent_revision=LIVE_H3,
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

        self.assertEqual(FRAMEWORK_MODULE_VERSION, "1.0.18")
        self.assertEqual(LIVE_CLAIM_SCHEMA_VERSION, 2)
        self.assertEqual(LIVE_ROUTING_SCHEMA_VERSION, 4)
        self.assertEqual(LIVE_PUBLICATION_ATTEMPT_SCHEMA_VERSION, 5)
        self.assertEqual(LIVE_OPENING_PREPARATION_SCHEMA_VERSION, 1)
        self.assertEqual(LIVE_OPENING_SEED_SCHEMA_VERSION, 2)
        self.assertEqual(LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION, 2)
        self.assertEqual(LIVE_ABSORPTION_ATTEMPT_SCHEMA_VERSION, 1)
        self.assertEqual(claim_schema["properties"]["schema_version"]["const"], 2)
        self.assertEqual(route_schema["properties"]["schema_version"]["const"], 4)
        self.assertEqual(publication_schema["properties"]["schema_version"]["const"], 5)

    def test_each_w03_opening_and_absorption_contract_has_its_own_schema_owner(self) -> None:
        schema_dir = ROOT / "DEV/SCHEMAS"
        contracts = (
            ("live-opening-preparation.schema.json", LIVE_OPENING_PREPARATION_SCHEMA_VERSION),
            ("live-opening-seed.schema.json", LIVE_OPENING_SEED_SCHEMA_VERSION),
            ("live-native-state-pack.schema.json", LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION),
            ("live-absorption-attempt.schema.json", LIVE_ABSORPTION_ATTEMPT_SCHEMA_VERSION),
        )

        for filename, expected_version in contracts:
            schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.assertEqual(schema["properties"]["schema_version"]["const"], expected_version)

    def test_w03_serialized_contracts_validate_their_runtime_mappings(self) -> None:
        schema_dir = ROOT / "DEV/SCHEMAS"
        filenames = (
            "live-claim.schema.json",
            "live-routing.schema.json",
            "live-opening-preparation.schema.json",
            "live-opening-seed.schema.json",
            "live-native-state-pack.schema.json",
            "live-absorption-attempt.schema.json",
        )
        schemas = {
            filename: json.loads((schema_dir / filename).read_text(encoding="utf-8"))
            for filename in filenames
        }
        store = {schema["$id"]: schema for schema in schemas.values()}

        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        seed = build_live_opening_seed(
            preparation,
            native_owner_states=_opening_native_states(),
            provenance={},
            privacy={},
            chronology={},
            unresolved_work={},
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        packed = pack_live_native_state(
            closed,
            native_owner_states=_opening_native_states(),
            provenance={},
            privacy={},
            chronology={},
            unresolved_work={},
        )
        route = build_live_route("campaign-frostfall", (closed,))
        attempt = freeze_campaign_absorption(
            closed,
            route=route,
            packed_state=packed,
            campaign_state={},
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        mappings = {
            "live-opening-preparation.schema.json": preparation.as_mapping(),
            "live-opening-seed.schema.json": seed.as_mapping(),
            "live-native-state-pack.schema.json": packed.as_mapping(),
            "live-absorption-attempt.schema.json": attempt.as_mapping(),
        }
        for filename, mapping in mappings.items():
            validator = Draft202012Validator(
                schemas[filename],
                resolver=RefResolver.from_schema(schemas[filename], store=store),
            )
            self.assertFalse(list(validator.iter_errors(mapping)), filename)

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

    def test_closed_live_birth_table_rejects_owner_equivalent_and_forbidden_families(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "f" * 64)
        forged_policy = {
            "world": {
                "world.knowledge": {
                    "prefix": "knowledge",
                    "live_birth": {
                        "disposition": "source_native_live",
                        "encoding": SOURCE_NATIVE_LIVE_ENCODING,
                    },
                },
                "world.player": {
                    "prefix": "player",
                    "live_birth": {
                        "disposition": "source_native_live",
                        "encoding": SOURCE_NATIVE_LIVE_ENCODING,
                    },
                },
            },
            "runtime": {
                "runtime.session": {
                    "prefix": "session",
                    "live_birth": {
                        "disposition": "source_native_live",
                        "encoding": SOURCE_NATIVE_LIVE_ENCODING,
                    },
                },
            },
        }

        for family in ("world.knowledge", "world.player", "runtime.session"):
            with self.subTest(family=family):
                with self.assertRaisesRegex(LiveContractError, "admitted|disposition|source-native|LIVE"):
                    encode_source_native_live_id(source_key, family, 1, forged_policy)

    def test_source_native_policy_requires_an_exact_family_row(self) -> None:
        source_key = ("campaign-1", "scene-1", "e1-" + "f" * 64)
        domain_fallback = {
            "prefix": "actor",
            "live_birth": {
                "disposition": "source_native_live",
                "encoding": SOURCE_NATIVE_LIVE_ENCODING,
            },
        }

        with self.assertRaisesRegex(LiveContractError, "policy|family|exact"):
            encode_source_native_live_id(source_key, "world.actor", 1, domain_fallback)


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
        self.assertEqual(result.accepted_source, attempt.successor_route.entries[0])
        self.assertEqual(advance_source_native_cursor(SourceNativeCursor(1), result), SourceNativeCursor(3))

    def test_cursor_advance_requires_the_exact_envelope_accepted_by_cas(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        forged = LivePublicationResult(
            status=LivePublicationStatus.ACCEPTED,
            source_key=attempt.source_key,
            authoritative=True,
            observed_source_revision=attempt.successor_route.entries[0].source_revision,
            source_native_allocations=attempt.source_native_allocations,
            expected_next_source_native_creation_ordinal=1,
            proposed_next_source_native_creation_ordinal=2,
        )

        with self.assertRaisesRegex(SourceNativeAllocationError, "envelope|source|accepted"):
            advance_source_native_cursor(SourceNativeCursor(1), forged)
        with self.assertRaisesRegex(SourceNativeAllocationError, "envelope|source|accepted"):
            advance_source_native_cursor(
                SourceNativeCursor(1),
                forged,
                attempt.successor_route.entries[0],
            )

    def test_cursor_advance_rejects_forged_matching_envelope_result(self) -> None:
        source = _live_source()
        attempt = freeze_live_attempt(
            source,
            route=_live_route(source),
            proposed_source_revision=LIVE_H1,
            source_native_creations=(SourceNativeCreation("world.actor", 1),),
            source_native_cursor=SourceNativeCursor(1),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        accepted = classify_cas_result(
            attempt,
            _accepted_ack(attempt)
            | {
                "source_native_allocations": [
                    allocation.as_mapping()
                    for allocation in attempt.source_native_allocations
                ],
                "expected_next_source_native_creation_ordinal": 1,
                "proposed_next_source_native_creation_ordinal": 2,
            },
        )
        forged = LivePublicationResult(
            status=accepted.status,
            source_key=accepted.source_key,
            authoritative=accepted.authoritative,
            observed_source_revision=accepted.observed_source_revision,
            source_native_allocations=accepted.source_native_allocations,
            expected_next_source_native_creation_ordinal=(
                accepted.expected_next_source_native_creation_ordinal
            ),
            proposed_next_source_native_creation_ordinal=(
                accepted.proposed_next_source_native_creation_ordinal
            ),
            accepted_source=accepted.accepted_source,
        )

        with self.assertRaisesRegex(SourceNativeAllocationError, "owner|issued|CAS|accepted"):
            advance_source_native_cursor(
                SourceNativeCursor(1), forged, accepted.accepted_source
            )

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


class SourceNativeHistoryValidationTests(unittest.TestCase):
    def test_persisted_history_accepts_the_exact_family_policy_prefix(self) -> None:
        source = _live_source()
        native_id = encode_source_native_live_id(
            source.source_key,
            "world.actor",
            1,
            SOURCE_NATIVE_POLICY,
        )

        loaded = LiveEnvelope.from_mapping(
            source.as_mapping()
            | {
                "next_source_native_creation_ordinal": 2,
                "source_native_ids": [native_id],
            },
            identifier_policy=SOURCE_NATIVE_POLICY,
        )

        self.assertEqual(loaded.source_native_ids, (native_id,))

    def test_live_envelope_rejects_a_framed_id_for_another_source(self) -> None:
        source = _live_source()
        foreign_id = encode_source_native_live_id(
            ("campaign-other", source.scene_id, source.epoch_id),
            "world.actor",
            1,
            SOURCE_NATIVE_POLICY,
        )

        with self.assertRaisesRegex(LiveContractError, "source|identity|history"):
            _live_source(next_source_native_creation_ordinal=2, source_native_ids=(foreign_id,))

    def test_live_envelope_requires_contiguous_source_native_history(self) -> None:
        source_key = _live_source().source_key
        first = encode_source_native_live_id(source_key, "world.actor", 1, SOURCE_NATIVE_POLICY)
        third = encode_source_native_live_id(source_key, "world.asset", 3, SOURCE_NATIVE_POLICY)

        with self.assertRaisesRegex(LiveContractError, "contiguous|ordinal|history"):
            _live_source(
                next_source_native_creation_ordinal=4,
                source_native_ids=(first, third),
            )

    def test_persisted_history_rejects_a_reprefixed_id_for_the_same_family(self) -> None:
        source = _live_source()
        renamed_policy = {
            "world": {
                "world.actor": {
                    **SOURCE_NATIVE_POLICY["world"]["world.actor"],
                    "prefix": "renamed-actor",
                }
            }
        }
        re_prefixed_id = encode_source_native_live_id(
            source.source_key,
            "world.actor",
            1,
            renamed_policy,
        )

        with self.assertRaisesRegex(LiveContractError, "prefix|policy|history"):
            LiveEnvelope.from_mapping(
                source.as_mapping()
                | {
                    "next_source_native_creation_ordinal": 2,
                    "source_native_ids": [re_prefixed_id],
                },
                identifier_policy=SOURCE_NATIVE_POLICY,
            )


def _opening_native_states() -> dict[str, object]:
    return {
        "world.actor": {
            "kind": "world.actor",
            "id": "actor-1",
            "state": {"hp": 10, "status": "ready"},
        },
        "runtime.procedure": {
            "kind": "runtime.procedure",
            "id": "procedure-1",
            "revision": 1,
            "state": {
                "schema_version": 2,
                "lifecycle": "ACTIVE",
                "lifecycle_state": "running",
                "participant_resources": {"actor-1": {"action": 1}},
            },
        },
    }


def _opening_seed(preparation: object, source: LiveEnvelope | None = None) -> LiveNativeStatePack:
    if source is not None:
        return pack_live_native_state(
            source,
            native_owner_states=_opening_native_states(),
            provenance={"opening_revision": LIVE_H0, "refs": ["event:opening"]},
            privacy={"knowledge": {"actor-1": ["fact:market"]}, "disclosure": []},
            chronology={"anchors": ["anchor:opening"], "relations": []},
            unresolved_work={"runtime.continuation": [{"id": "continuation-1"}]},
        )
    seed = build_live_opening_seed(
        preparation,
        native_owner_states=_opening_native_states(),
        provenance={"opening_revision": LIVE_H0, "refs": ["event:opening"]},
        privacy={"knowledge": {"actor-1": ["fact:market"]}, "disclosure": []},
        chronology={"anchors": ["anchor:opening"], "relations": []},
        unresolved_work={"runtime.continuation": [{"id": "continuation-1"}]},
    )
    return pack_live_native_state(seed)


def _accepted_absorption_publication(source: LiveEnvelope) -> LiveAbsorptionPublication:
    source = replace(source, status=LiveLifecycle.CLOSED)
    preparation = prepare_live_opening(
        source.campaign_id,
        source.scene_id,
        opening_campaign_revision=LIVE_H0,
        claims=source.claims,
        source_revision=LIVE_H0,
    )
    packed = _opening_seed(preparation, source)
    route = _live_route(source)
    attempt = freeze_campaign_absorption(
        source,
        route=route,
        packed_state=packed,
        campaign_state={"native_owner_states": {}},
        expected_campaign_revision=LIVE_H0,
        proposed_campaign_revision=LIVE_H2,
    )
    return classify_campaign_absorption(
        attempt,
        {
            "accepted": True,
            "source_key": source.source_key,
            "source_revision": source.source_revision,
            "expected_campaign_revision": LIVE_H0,
            "new_campaign_revision": LIVE_H2,
            "candidate_state_digest": attempt.candidate_state_digest,
            "selected_route": attempt.selected_route.as_mapping(),
            "successor_route": attempt.successor_route.as_mapping(),
        },
    )


class LiveOpeningPreparationTests(unittest.TestCase):
    def test_opening_preparation_requires_an_explicit_source_revision(self) -> None:
        with self.assertRaises(TypeError):
            prepare_live_opening(
                "campaign-frostfall",
                "scene-market",
                opening_campaign_revision=LIVE_H0,
                claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            )

    def test_opening_preparation_is_repeatable_and_not_selected_authority(self) -> None:
        claims = (LiveClaim.exact_owner("world.actor", "actor-1"),)

        first = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=claims,
            source_revision="prepared-opening",
        )
        second = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=claims,
            source_revision="prepared-opening",
        )

        self.assertEqual(first, second)
        self.assertIsNone(select_live_source(build_live_route("campaign-frostfall", ()), first.source_key))
        self.assertEqual(first.source.status, LiveLifecycle.ACTIVE)

    def test_opening_seed_requires_complete_explicit_native_inputs(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision="prepared-opening",
        )

        with self.assertRaisesRegex(LiveContractError, "provenance|privacy|chronology|unresolved"):
            build_live_opening_seed(
                preparation,
                native_owner_states=_opening_native_states(),
                provenance={"opening_revision": LIVE_H0},
                privacy={},
                chronology={},
                unresolved_work=None,
            )


class LiveOpeningSeedTests(unittest.TestCase):
    def test_exact_cas_publication_is_required_before_opening_route_adoption(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        source = preparation.source
        route = build_live_route("campaign-frostfall", (source,))
        attempt = freeze_live_attempt(source, route=route, proposed_source_revision=LIVE_H1)

        rejected = classify_cas_result(
            attempt,
            {
                "accepted": False,
                "source_key": source.source_key,
                "current_source_revision": LIVE_H1,
            },
        )
        self.assertEqual(rejected.status, LivePublicationStatus.REJECTED_STALE)
        with self.assertRaisesRegex(LiveContractError, "accepted|publication|opening"):
            publish_live_opening(preparation, rejected)

        accepted = classify_cas_result(attempt, _accepted_ack(attempt))
        published = publish_live_opening(preparation, accepted)
        self.assertEqual(published.source_revision, LIVE_H1)
        self.assertEqual(published.source_key, source.source_key)

    def test_forged_matching_cas_result_cannot_publish_a_prepared_opening(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        source = preparation.source
        attempt = freeze_live_attempt(
            source,
            route=build_live_route("campaign-frostfall", (source,)),
            proposed_source_revision=LIVE_H1,
        )
        accepted = classify_cas_result(attempt, _accepted_ack(attempt))
        forged = LivePublicationResult(
            status=accepted.status,
            source_key=accepted.source_key,
            authoritative=accepted.authoritative,
            observed_source_revision=accepted.observed_source_revision,
            accepted_source=accepted.accepted_source,
        )

        with self.assertRaisesRegex(LiveContractError, "owner|issued|CAS"):
            publish_live_opening(preparation, forged)

    def test_opening_publication_requires_the_exact_prepared_predecessor(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        foreign_predecessor = LiveEnvelope(
            campaign_id=preparation.source.campaign_id,
            scene_id=preparation.source.scene_id,
            epoch_id=preparation.source.epoch_id,
            source_ref=preparation.source.source_ref,
            source_revision=LIVE_H2,
            claims=preparation.source.claims,
            status=LiveLifecycle.ACTIVE,
            opening_campaign_revision=preparation.source.opening_campaign_revision,
        )
        foreign_attempt = freeze_live_attempt(
            foreign_predecessor,
            route=build_live_route("campaign-frostfall", (foreign_predecessor,)),
            proposed_source_revision=LIVE_H3,
        )
        accepted = classify_cas_result(foreign_attempt, _accepted_ack(foreign_attempt))

        with self.assertRaisesRegex(LiveContractError, "predecessor|prepared|source"):
            publish_live_opening(preparation, accepted)


class LiveRoutingCompletenessTests(unittest.TestCase):
    def test_complete_route_requires_every_expected_body_and_rejects_stale_extra_member(self) -> None:
        source = _live_source()
        other = _live_source(claims=(LiveClaim.exact_owner("world.asset", "asset-1"),))

        route = build_live_route(
            "campaign-frostfall",
            (source,),
            expected_source_keys=(source.source_key,),
        )
        validate_live_route_completeness(route, (source.source_key,))

        with self.assertRaisesRegex(LiveContractError, "complete|missing|expected"):
            build_live_route(
                "campaign-frostfall",
                (source,),
                expected_source_keys=(source.source_key, other.source_key),
            )

        absorbed = _live_source(
            revision=LIVE_H1,
            status=LiveLifecycle.ABSORBED,
            claims=(LiveClaim.exact_owner("world.asset", "asset-1"),),
        )
        with self.assertRaisesRegex(LiveContractError, "stale|absorbed|complete"):
            validate_live_route_completeness(
                build_live_route("campaign-frostfall", (source, absorbed)),
                (source.source_key,),
            )


class LiveNativeStatePackingTests(unittest.TestCase):
    def test_packing_and_unpacking_are_lossless_across_owner_and_crosscutting_inputs(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        seed = build_live_opening_seed(
            preparation,
            native_owner_states=_opening_native_states(),
            provenance={"opening_revision": LIVE_H0, "refs": ["event:opening"]},
            privacy={"knowledge": {"actor-1": ["fact:market"]}, "disclosure": []},
            chronology={"anchors": ["anchor:opening"], "relations": []},
            unresolved_work={"runtime.continuation": [{"id": "continuation-1"}]},
        )

        packed = pack_live_native_state(seed)

        self.assertEqual(
            unpack_live_native_state(packed),
            {
                "source_key": preparation.source.source_key,
                "source_revision": LIVE_H0,
                "next_source_native_creation_ordinal": 1,
                "source_native_ids": (),
                "native_owner_states": _opening_native_states(),
                "provenance": {"opening_revision": LIVE_H0, "refs": ["event:opening"]},
                "privacy": {"knowledge": {"actor-1": ["fact:market"]}, "disclosure": []},
                "chronology": {"anchors": ["anchor:opening"], "relations": []},
                "unresolved_work": {"runtime.continuation": [{"id": "continuation-1"}]},
            },
        )

    def test_packing_preserves_exact_source_native_ids_and_cursor_history(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
            source_native_creations=(SourceNativeCreation("world.asset", 7),),
            identifier_policy=SOURCE_NATIVE_POLICY,
        )
        packed = _opening_seed(preparation)

        unpacked = unpack_live_native_state(packed)

        self.assertEqual(unpacked["source_key"], preparation.source.source_key)
        self.assertEqual(unpacked["source_revision"], LIVE_H0)
        self.assertEqual(unpacked["next_source_native_creation_ordinal"], 2)
        self.assertEqual(unpacked["source_native_ids"], preparation.source.source_native_ids)

    def test_partial_pack_is_rejected_instead_of_inventing_owner_defaults(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        with self.assertRaisesRegex(LiveContractError, "privacy|chronology|unresolved"):
            pack_live_native_state(
                preparation.source,
                native_owner_states=_opening_native_states(),
                provenance={"opening_revision": LIVE_H0},
            )


class LiveAbsorptionMaterializationTests(unittest.TestCase):
    def test_absorption_rejects_a_successor_route_with_wrong_membership(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        route = build_live_route("campaign-frostfall", (closed,))
        packed = _opening_seed(preparation, closed)
        candidate = freeze_campaign_absorption(
            closed,
            route=route,
            packed_state=packed,
            campaign_state={"native_owner_states": {}},
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        wrong_successor = build_live_route("campaign-frostfall", (closed,))

        with self.assertRaisesRegex(LiveContractError, "route|member|closure"):
            FrozenCampaignAbsorption(
                selected_route=candidate.selected_route,
                source_key=candidate.source_key,
                source_revision=candidate.source_revision,
                expected_campaign_revision=candidate.expected_campaign_revision,
                proposed_campaign_revision=candidate.proposed_campaign_revision,
                packed_state=candidate.packed_state,
                candidate_state=candidate.candidate_state,
                successor_route=wrong_successor,
            )

    def test_absorption_preserves_identity_provenance_privacy_chronology_and_is_idempotent(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        source = preparation.source
        closed = close_live_source(
            source,
            expected_source_revision=LIVE_H0,
            closed_source_revision=LIVE_H1,
        )
        closed_unabsorbed = mark_closed_unabsorbed(closed)
        route = build_live_route("campaign-frostfall", (closed_unabsorbed,))
        packed = _opening_seed(preparation, closed_unabsorbed)
        campaign_state = {
            "native_owner_states": {},
            "provenance": {},
            "privacy": {},
            "chronology": {},
            "unresolved_work": {},
        }
        attempt = freeze_campaign_absorption(
            closed_unabsorbed,
            route=route,
            packed_state=packed,
            campaign_state=campaign_state,
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        incomplete_ack = {
            "accepted": True,
            "source_key": closed_unabsorbed.source_key,
            "source_revision": LIVE_H1,
            "expected_campaign_revision": LIVE_H0,
            "new_campaign_revision": LIVE_H2,
            "candidate_state_digest": attempt.candidate_state_digest,
            "successor_route": attempt.successor_route.as_mapping(),
        }
        self.assertEqual(
            classify_campaign_absorption(attempt, incomplete_ack).status,
            LiveAbsorptionStatus.INDETERMINATE,
        )
        publication = classify_campaign_absorption(
            attempt,
            {
                "accepted": True,
                "source_key": closed_unabsorbed.source_key,
                "source_revision": LIVE_H1,
                 "expected_campaign_revision": LIVE_H0,
                 "new_campaign_revision": LIVE_H2,
                 "candidate_state_digest": attempt.candidate_state_digest,
                 "selected_route": attempt.selected_route.as_mapping(),
                 "successor_route": attempt.successor_route.as_mapping(),
             },
         )
        first = absorb_live_state(
            closed_unabsorbed,
            packed,
            campaign_state,
            route=route,
            publication=publication,
        )
        second = absorb_live_state(
            first.source,
            packed,
            first.campaign_state,
            route=first.route,
            publication=publication,
        )

        self.assertEqual(first.status, LiveAbsorptionStatus.ACCEPTED)
        self.assertEqual(first.source.status, LiveLifecycle.ABSORBED)
        self.assertEqual(first.campaign_state, second.campaign_state)
        self.assertEqual(first.campaign_state["native_owner_states"], packed.native_owner_states)
        self.assertEqual(first.campaign_state["provenance"], packed.provenance)
        self.assertEqual(first.campaign_state["privacy"], packed.privacy)
        self.assertEqual(first.campaign_state["chronology"], packed.chronology)
        self.assertEqual(first.campaign_state["unresolved_work"], packed.unresolved_work)

        forged = LiveAbsorptionPublication(
            status=publication.status,
            source_key=publication.source_key,
            source_revision=publication.source_revision,
            authoritative=publication.authoritative,
            candidate_state=publication.candidate_state,
            successor_route=publication.successor_route,
            attempt=publication.attempt,
        )
        with self.assertRaisesRegex(LiveContractError, "owner|issued|CAS"):
            absorb_live_state(
                closed_unabsorbed,
                packed,
                campaign_state,
                route=route,
                publication=forged,
            )

        foreign_closed = close_live_source(
            source,
            expected_source_revision=LIVE_H0,
            closed_source_revision=LIVE_H2,
        )
        foreign_closed_unabsorbed = mark_closed_unabsorbed(foreign_closed)
        foreign_route = build_live_route("campaign-frostfall", (foreign_closed_unabsorbed,))
        foreign_packed = _opening_seed(preparation, foreign_closed_unabsorbed)
        foreign_attempt = freeze_campaign_absorption(
            foreign_closed_unabsorbed,
            route=foreign_route,
            packed_state=foreign_packed,
            campaign_state=campaign_state,
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        foreign_publication = classify_campaign_absorption(
            foreign_attempt,
            {
                "accepted": True,
                "source_key": foreign_closed.source_key,
                "source_revision": LIVE_H2,
                "expected_campaign_revision": LIVE_H0,
                "new_campaign_revision": LIVE_H2,
                "candidate_state_digest": foreign_attempt.candidate_state_digest,
                "selected_route": foreign_attempt.selected_route.as_mapping(),
                "successor_route": foreign_attempt.successor_route.as_mapping(),
            },
        )
        with self.assertRaisesRegex(LiveContractError, "exact|source|bound"):
            absorb_live_state(
                closed_unabsorbed,
                packed,
                campaign_state,
                route=route,
                publication=foreign_publication,
            )

    def test_absorption_retry_requires_the_stored_accepted_campaign_and_route_closure(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        route = build_live_route("campaign-frostfall", (closed,))
        packed = _opening_seed(preparation, closed)
        campaign_state = {"native_owner_states": {}}
        attempt = freeze_campaign_absorption(
            closed,
            route=route,
            packed_state=packed,
            campaign_state=campaign_state,
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        publication = classify_campaign_absorption(
            attempt,
            {
                "accepted": True,
                "source_key": closed.source_key,
                "source_revision": LIVE_H1,
                "expected_campaign_revision": LIVE_H0,
                "new_campaign_revision": LIVE_H2,
                "candidate_state_digest": attempt.candidate_state_digest,
                "selected_route": attempt.selected_route.as_mapping(),
                "successor_route": attempt.successor_route.as_mapping(),
            },
        )
        first = absorb_live_state(
            closed,
            packed,
            campaign_state,
            route=route,
            publication=publication,
        )
        tampered_state = deepcopy(dict(first.campaign_state))
        tampered_state["live_routing"] = route.as_mapping()

        with self.assertRaisesRegex(LiveContractError, "stored|closure|route|accepted"):
            absorb_live_state(
                first.source,
                packed,
                tampered_state,
                route=first.route,
                publication=publication,
            )

    def test_absorption_rejects_pack_with_different_source_native_history(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        route = build_live_route("campaign-frostfall", (closed,))
        wrong_id = encode_source_native_live_id(
            closed.source_key,
            "world.actor",
            1,
            SOURCE_NATIVE_POLICY,
        )
        wrong_pack = LiveNativeStatePack(
            source_key=closed.source_key,
            source_revision=closed.source_revision,
            next_source_native_creation_ordinal=2,
            source_native_ids=(wrong_id,),
            native_owner_states=_opening_native_states(),
            provenance={},
            privacy={},
            chronology={},
            unresolved_work={},
        )

        with self.assertRaisesRegex(LiveContractError, "history|native|exact"):
            freeze_campaign_absorption(
                closed,
                route=route,
                packed_state=wrong_pack,
                campaign_state={"native_owner_states": {}},
                expected_campaign_revision=LIVE_H0,
                proposed_campaign_revision=LIVE_H2,
            )

    def test_failed_or_indeterminate_campaign_publication_keeps_closed_unabsorbed_recovery_truth(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        route = build_live_route("campaign-frostfall", (closed,))
        packed = _opening_seed(preparation, closed)
        pending = absorb_live_state(
            closed,
            packed,
            {"native_owner_states": {}},
            route=route,
            publication=None,
        )

        self.assertEqual(pending.status, LiveAbsorptionStatus.CLOSED_UNABSORBED)
        self.assertEqual(recover_closed_unabsorbed(pending.route, closed.source_key), closed)
        self.assertEqual(pending.campaign_state, {"native_owner_states": {}})


def _temporal_root() -> dict[str, object]:
    return {
        "root_ref": "world.thread:THREAD_market_siege",
        "occurrence_id": "occurrence:market-siege:1",
        "binding_id": "temporal-binding:market-siege:1",
        "occurrence_state": "ARMED",
        "binding": {
            "basis_id": "temporal.metric_deadline",
            "context_id": "scene:market",
            "anchor_value": 12,
            "deadline_value": 15,
            "unit_id": "unit.day",
        },
        "dependency_keys": ["METRIC_POSITION:scene:market"],
    }


def _temporal_route(entry: object, *, scope: str, revision: str, source_key: object = None) -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "runtime.temporal_routing",
        "campaign_id": "campaign-frostfall",
        "source_scope": scope,
        "source_revision": revision,
        "source_key": list(source_key) if source_key is not None else None,
        "complete": True,
        "entries": [entry],
    }


def _temporal_native_enumeration(
    root: dict[str, object], *, scope: str, revision: str, source_key: object = None
):
    entry = derive_temporal_route_entry(
        root,
        campaign_id="campaign-frostfall",
        source_scope=scope,
        source_revision=revision,
        source_key=source_key,
    )
    return enumerate_temporal_native_owners(
        (entry,),
        campaign_id="campaign-frostfall",
        source_scope=scope,
        source_revision=revision,
        source_key=source_key,
    )


class LiveTemporalRoutingHandoffTests(unittest.TestCase):
    def test_closed_unabsorbed_cannot_return_to_campaign_from_caller_ack(self) -> None:
        root = _temporal_root()
        entry = derive_temporal_route_entry(
            root,
            campaign_id="campaign-frostfall",
            source_scope="LIVE",
            source_revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        route = _temporal_route(
            entry,
            scope="LIVE",
            revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        closed_unabsorbed = mark_closed_unabsorbed(
            close_live_source(
                _live_source(revision=LIVE_H0),
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )

        with self.assertRaisesRegex(LiveContractError, "ABSORBED|absorption"):
            handoff_temporal_route_to_campaign(
                route,
                live_source=closed_unabsorbed,
                live_route=_live_route(closed_unabsorbed),
                campaign_revision=LIVE_H2,
                absorption_evidence=True,
                native_enumeration=_temporal_native_enumeration(
                    root,
                    scope="LIVE",
                    revision=LIVE_H1,
                    source_key=closed_unabsorbed.source_key,
                ),
            )

    def test_temporal_campaign_return_requires_owner_issued_accepted_absorption(self) -> None:
        preparation = prepare_live_opening(
            "campaign-frostfall",
            "scene-market",
            opening_campaign_revision=LIVE_H0,
            claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
            source_revision=LIVE_H0,
        )
        closed = mark_closed_unabsorbed(
            close_live_source(
                preparation.source,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        route = _live_route(closed)
        packed = _opening_seed(preparation, closed)
        attempt = freeze_campaign_absorption(
            closed,
            route=route,
            packed_state=packed,
            campaign_state={"native_owner_states": {}},
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        publication = classify_campaign_absorption(
            attempt,
            {
                "accepted": True,
                "source_key": closed.source_key,
                "source_revision": LIVE_H1,
                "expected_campaign_revision": LIVE_H0,
                "new_campaign_revision": LIVE_H2,
                "candidate_state_digest": attempt.candidate_state_digest,
                "selected_route": attempt.selected_route.as_mapping(),
                "successor_route": attempt.successor_route.as_mapping(),
            },
        )
        absorbed = replace(closed, status=LiveLifecycle.ABSORBED)
        entry = derive_temporal_route_entry(
            _temporal_root(),
            campaign_id="campaign-frostfall",
            source_scope="LIVE",
            source_revision=LIVE_H1,
            source_key=closed.source_key,
        )

        returned = handoff_temporal_route_to_campaign(
            _temporal_route(entry, scope="LIVE", revision=LIVE_H1, source_key=closed.source_key),
            live_source=absorbed,
            live_route=route,
            campaign_revision=LIVE_H2,
            absorption_evidence=publication,
            native_enumeration=_temporal_native_enumeration(
                _temporal_root(),
                scope="LIVE",
                revision=LIVE_H1,
                source_key=closed.source_key,
            ),
        )

        self.assertEqual(returned.source_scope, "CAMPAIGN")

    def test_temporal_handoff_requires_the_exact_native_owner_set(self) -> None:
        root = _temporal_root()
        entry = derive_temporal_route_entry(
            root,
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision=LIVE_H0,
        )
        campaign_route = _temporal_route(entry, scope="CAMPAIGN", revision=LIVE_H0)
        active = _live_source(revision=LIVE_H0)

        with self.assertRaisesRegex((LiveContractError, ValueError), "complete|native|root"):
            handoff_temporal_route_to_live(
                campaign_route,
                campaign_revision=LIVE_H0,
                live_source=active,
                live_route=_live_route(active),
                native_enumeration=enumerate_temporal_native_owners(
                    (),
                    campaign_id="campaign-frostfall",
                    source_scope="CAMPAIGN",
                    source_revision=LIVE_H0,
                ),
            )

    def test_campaign_to_live_and_live_to_campaign_preserve_temporal_identity(self) -> None:
        root = _temporal_root()
        entry = derive_temporal_route_entry(
            root,
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision=LIVE_H0,
        )
        campaign_route = _temporal_route(entry, scope="CAMPAIGN", revision=LIVE_H0)
        active = _live_source(revision=LIVE_H0)

        live_route = handoff_temporal_route_to_live(
            campaign_route,
            campaign_revision=LIVE_H0,
            live_source=active,
            live_route=_live_route(active),
            native_enumeration=_temporal_native_enumeration(
                root,
                scope="CAMPAIGN",
                revision=LIVE_H0,
            ),
        )
        live_retry = handoff_temporal_route_to_live(
            live_route,
            campaign_revision=LIVE_H0,
            live_source=active,
            live_route=_live_route(active),
            native_enumeration=_temporal_native_enumeration(
                root,
                scope="LIVE",
                revision=LIVE_H0,
                source_key=active.source_key,
            ),
        )
        self.assertEqual(live_retry, live_route)
        closed = mark_closed_unabsorbed(
            close_live_source(
                active,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        absorbed = replace(closed, status=LiveLifecycle.ABSORBED)
        current_live_route = reconcile_temporal_route_membership(
            live_route,
            expected_source_scope="LIVE",
            expected_source_revision=LIVE_H0,
            expected_source_key=active.source_key,
            target_source_scope="LIVE",
            target_source_revision=LIVE_H1,
            target_source_key=closed.source_key,
            native_enumeration=_temporal_native_enumeration(
                root,
                scope="LIVE",
                revision=LIVE_H0,
                source_key=active.source_key,
            ),
        )
        packed = _opening_seed(
            prepare_live_opening(
                "campaign-frostfall",
                "scene-market",
                opening_campaign_revision=LIVE_H0,
                claims=(LiveClaim.exact_owner("world.actor", "actor-1"),),
                source_revision=LIVE_H0,
            ),
            closed,
        )
        absorption_attempt = freeze_campaign_absorption(
            closed,
            route=_live_route(closed),
            packed_state=packed,
            campaign_state={"native_owner_states": {}},
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H2,
        )
        absorption_publication = classify_campaign_absorption(
            absorption_attempt,
            {
                "accepted": True,
                "source_key": closed.source_key,
                "source_revision": LIVE_H1,
                "expected_campaign_revision": LIVE_H0,
                "new_campaign_revision": LIVE_H2,
                "candidate_state_digest": absorption_attempt.candidate_state_digest,
                "selected_route": absorption_attempt.selected_route.as_mapping(),
                "successor_route": absorption_attempt.successor_route.as_mapping(),
            },
        )
        campaign_again = handoff_temporal_route_to_campaign(
            current_live_route,
            live_source=absorbed,
            live_route=_live_route(closed),
            campaign_revision=LIVE_H2,
            absorption_evidence=absorption_publication,
            native_enumeration=_temporal_native_enumeration(
                root,
                scope="LIVE",
                revision=LIVE_H1,
                source_key=closed.source_key,
            ),
        )
        campaign_retry = handoff_temporal_route_to_campaign(
            campaign_again,
            live_source=absorbed,
            live_route=_live_route(closed),
            campaign_revision=LIVE_H2,
            absorption_evidence=absorption_publication,
            native_enumeration=_temporal_native_enumeration(
                root,
                scope="CAMPAIGN",
                revision=LIVE_H2,
            ),
        )
        self.assertEqual(campaign_retry, campaign_again)

        original = live_route.entries[0]
        returned = campaign_again.entries[0]
        self.assertEqual(returned.root_ref, original.root_ref)
        self.assertEqual(returned.occurrence_id, original.occurrence_id)
        self.assertEqual(returned.binding_id, original.binding_id)
        self.assertEqual(returned.dependency_keys, original.dependency_keys)
        self.assertEqual(campaign_again.source_scope, "CAMPAIGN")
        self.assertEqual(campaign_again.source_revision, LIVE_H2)
        self.assertIsNone(campaign_again.source_key)

    def test_temporal_handoff_rejects_foreign_campaign_and_stale_source(self) -> None:
        entry = derive_temporal_route_entry(
            _temporal_root(),
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision=LIVE_H0,
        )
        route = _temporal_route(entry, scope="CAMPAIGN", revision=LIVE_H0)
        active = _live_source(revision=LIVE_H1)

        with self.assertRaisesRegex((LiveContractError, ValueError), "campaign|revision|source"):
            handoff_temporal_route_to_live(
                route,
                campaign_revision=LIVE_H1,
                live_source=active,
                live_route=_live_route(active),
                native_enumeration=_temporal_native_enumeration(
                    _temporal_root(),
                    scope="CAMPAIGN",
                    revision=LIVE_H0,
                ),
            )

        foreign_entry = derive_temporal_route_entry(
            _temporal_root(),
            campaign_id="campaign-other",
            source_scope="CAMPAIGN",
            source_revision=LIVE_H0,
        )
        with self.assertRaisesRegex(ValueError, "campaign"):
            reconcile_temporal_route_membership(
                _temporal_route(foreign_entry, scope="CAMPAIGN", revision=LIVE_H0),
                expected_source_scope="CAMPAIGN",
                expected_source_revision=LIVE_H0,
                target_source_scope="LIVE",
                target_source_revision=LIVE_H1,
                target_source_key=active.source_key,
                native_enumeration=_temporal_native_enumeration(
                    _temporal_root(),
                    scope="CAMPAIGN",
                    revision=LIVE_H0,
                ),
            )

    def test_interrupted_handoff_retries_from_exact_live_route_and_rebuilds_agenda(self) -> None:
        entry = derive_temporal_route_entry(
            _temporal_root(),
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision=LIVE_H0,
        )
        live = reconcile_temporal_route_membership(
            _temporal_route(entry, scope="CAMPAIGN", revision=LIVE_H0),
            expected_source_scope="CAMPAIGN",
            expected_source_revision=LIVE_H0,
            target_source_scope="LIVE",
            target_source_revision=LIVE_H1,
            target_source_key=_live_source(revision=LIVE_H1).source_key,
            native_enumeration=_temporal_native_enumeration(
                _temporal_root(),
                scope="CAMPAIGN",
                revision=LIVE_H0,
            ),
        )
        retry = reconcile_temporal_route_membership(
            live,
            expected_source_scope="LIVE",
            expected_source_revision=LIVE_H1,
            expected_source_key=live.source_key,
            target_source_scope="LIVE",
            target_source_revision=LIVE_H1,
            target_source_key=live.source_key,
            native_enumeration=_temporal_native_enumeration(
                _temporal_root(),
                scope="LIVE",
                revision=LIVE_H1,
                source_key=live.source_key,
            ),
        )

        self.assertEqual(retry, live)
        agenda = rebuild_temporal_agenda_from_route(retry)
        self.assertEqual(agenda[0]["root_ref"], "world.thread:THREAD_market_siege")
        self.assertEqual(agenda[0]["occurrence_id"], "occurrence:market-siege:1")

    def test_terminal_temporal_owner_is_removed_only_by_explicit_exact_identity(self) -> None:
        armed_entry = derive_temporal_route_entry(
            _temporal_root(),
            campaign_id="campaign-frostfall",
            source_scope="LIVE",
            source_revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        armed_route = _temporal_route(
            armed_entry,
            scope="LIVE",
            revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        with self.assertRaisesRegex(ValueError, "terminal"):
            reconcile_temporal_route_membership(
                armed_route,
                expected_source_scope="LIVE",
                expected_source_revision=LIVE_H1,
                expected_source_key=armed_route["source_key"],
                target_source_scope="CAMPAIGN",
                target_source_revision=LIVE_H2,
                terminal_root_refs=("world.thread:THREAD_market_siege",),
                native_enumeration=_temporal_native_enumeration(
                    _temporal_root(),
                    scope="LIVE",
                    revision=LIVE_H1,
                    source_key=armed_route["source_key"],
                ),
            )

        closed_root = dict(_temporal_root(), occurrence_state="CLOSED")
        entry = derive_temporal_route_entry(
            closed_root,
            campaign_id="campaign-frostfall",
            source_scope="LIVE",
            source_revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        route = _temporal_route(
            entry,
            scope="LIVE",
            revision=LIVE_H1,
            source_key=_live_source(revision=LIVE_H1).source_key,
        )
        forged_entry = replace(entry)
        with self.assertRaisesRegex(ValueError, "owner-issued|proof"):
            reconcile_temporal_route_membership(
                route,
                expected_source_scope="LIVE",
                expected_source_revision=LIVE_H1,
                expected_source_key=route["source_key"],
                target_source_scope="CAMPAIGN",
                target_source_revision=LIVE_H2,
                terminal_root_refs=("world.thread:THREAD_market_siege",),
                terminal_owner_entries=(forged_entry,),
                native_enumeration=_temporal_native_enumeration(
                    closed_root,
                    scope="LIVE",
                    revision=LIVE_H1,
                    source_key=route["source_key"],
                ),
            )
        terminal = reconcile_temporal_route_membership(
            route,
            expected_source_scope="LIVE",
            expected_source_revision=LIVE_H1,
            expected_source_key=route["source_key"],
            target_source_scope="CAMPAIGN",
            target_source_revision=LIVE_H2,
            terminal_root_refs=("world.thread:THREAD_market_siege",),
            terminal_owner_entries=(entry,),
            native_enumeration=_temporal_native_enumeration(
                closed_root,
                scope="LIVE",
                revision=LIVE_H1,
                source_key=route["source_key"],
            ),
        )

        self.assertEqual(terminal.entries, ())


class LiveOperationalRootHandoffTests(unittest.TestCase):
    def _recover(
        self,
        page: OperationalRootHandoff,
        source: LiveEnvelope,
        *,
        absorption_evidence: object | None = None,
        campaign_revision: str = LIVE_H2,
        terminal_owner_keys: tuple[tuple[str, str] | tuple[str, str, str], ...] = (),
        terminal_native_owners: dict[
            tuple[str, str] | tuple[str, str, str], object
        ]
        | None = None,
        superseded_owner_keys: tuple[tuple[str, str] | tuple[str, str, str], ...] = (),
        superseded_native_deltas: dict[
            tuple[str, str] | tuple[str, str, str], object
        ]
        | None = None,
    ) -> object:
        closed_source = replace(source, status=LiveLifecycle.CLOSED)
        absorbed_source = replace(source, status=LiveLifecycle.ABSORBED)
        return handoff_operational_roots_to_campaign(
            page,
            live_source=absorbed_source,
            live_route=_live_route(closed_source),
            campaign_revision=campaign_revision,
            absorption_evidence=(
                _accepted_absorption_publication(source)
                if absorption_evidence is None
                else absorption_evidence
            ),
            terminal_owner_keys=terminal_owner_keys,
            terminal_native_owners=terminal_native_owners,
            superseded_owner_keys=superseded_owner_keys,
            superseded_native_deltas=superseded_native_deltas,
        )

    def _page(self) -> OperationalRootPage:
        root = OperationalRoot(
            "campaign-frostfall",
            "runtime.command",
            "command-000001",
            route_native_record("runtime.command", ("command-000001",)).relative_path,
        )
        return OperationalRootPage("campaign-frostfall", (root,), complete=True)

    def test_serialized_handoff_has_a_distinct_strict_contract(self) -> None:
        source = _live_source(revision=LIVE_H1)
        handoff = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        mapping = handoff.to_dict()
        schema = json.loads(
            (ROOT / "DEV/SCHEMAS/operational-root-handoff.schema.json").read_text(encoding="utf-8")
        )

        Draft202012Validator(schema).validate(mapping)
        self.assertEqual(OperationalRootHandoff.from_mapping(mapping), handoff)
        invalid = dict(mapping)
        del invalid["kind"]
        with self.assertRaisesRegex(ValueError, "fields|unsupported"):
            OperationalRootHandoff.from_mapping(invalid)

    def test_absorption_evidence_has_no_neutral_issuer(self) -> None:
        self.assertFalse((ROOT / "GAME/TOOLS/handoff_evidence.py").exists())
        tree = ast.parse(
            (ROOT / "GAME/TOOLS/recovery_roots.py").read_text(encoding="utf-8")
        )
        neutral_imports = [
            node
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "handoff_evidence"
        ]
        self.assertEqual(neutral_imports, [])

    def test_root_recovery_requires_the_live_owner_absorption_transport(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        with self.assertRaisesRegex(ValueError, "producer|transport|absorption"):
            self._recover(live_page, source, absorption_evidence=object())

    def _assert_no_recovery_roots_live_campaign_entry(
        self,
        candidate: object,
        source: LiveEnvelope,
    ) -> None:
        for name in (
            "recover_operational_roots_to_campaign",
            "_recover_operational_roots_to_campaign",
            "_reconcile_operational_root_handoff",
            ):
            with self.subTest(candidate=candidate, name=name):
                self.assertFalse(callable(getattr(recovery_roots_module, name, None)))
        with self.assertRaisesRegex(OperationalRootError, "CAMPAIGN|scope|stale|typed"):
            handoff_operational_roots_to_live(
                candidate,  # type: ignore[arg-type]
                campaign_id="campaign-frostfall",
                campaign_revision=LIVE_H0,
                live_source_key=source.source_key,
                live_source_revision=source.source_revision,
            )

    def test_direct_live_handoff_has_no_recovery_roots_entry(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        self.assertFalse(hasattr(recovery_roots_module, "AcceptedAbsorptionEvidenceTransport"))
        self._assert_no_recovery_roots_live_campaign_entry(live_page, source)

    def test_reconstructed_live_handoff_has_no_recovery_roots_entry(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_handoff = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        reconstructed = OperationalRootHandoff.from_mapping(live_handoff.to_dict())
        self._assert_no_recovery_roots_live_campaign_entry(reconstructed, source)

    def test_repeated_live_handoff_mapping_has_no_recovery_roots_entry(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_handoff = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        mapping = live_handoff.to_dict()
        self._assert_no_recovery_roots_live_campaign_entry(mapping, source)
        self._assert_no_recovery_roots_live_campaign_entry(mapping, source)

    def test_root_recovery_rejects_forged_evidence_and_arbitrary_validator(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        publication = _accepted_absorption_publication(source)
        forged_evidence = LiveAbsorptionPublication(
            status=publication.status,
            source_key=publication.source_key,
            source_revision=publication.source_revision,
            authoritative=publication.authoritative,
            candidate_state=publication.candidate_state,
            successor_route=publication.successor_route,
            attempt=publication.attempt,
        )

        class ForgedValidator:
            def __call__(
                self,
                _evidence: object,
                *,
                source_key: tuple[str, str, str],
                source_revision: str,
            ) -> None:
                return None

        class ForgedEvidence:
            def validate_for_operational_root_recovery(
                self,
                *,
                source_key: tuple[str, str, str],
                source_revision: str,
            ) -> "ForgedEvidence":
                return self

        with self.assertRaisesRegex(ValueError, "producer|owner|evidence|transport|typed"):
            self._recover(live_page, source, absorption_evidence=forged_evidence)
        with self.assertRaises(TypeError):
            handoff_operational_roots_to_campaign(
                live_page,
                live_source=replace(source, status=LiveLifecycle.ABSORBED),
                live_route=_live_route(replace(source, status=LiveLifecycle.CLOSED)),
                campaign_revision=LIVE_H2,
                absorption_evidence=publication,
                absorption_evidence_validator=ForgedValidator(),  # type: ignore[call-arg]
            )
        with self.assertRaisesRegex(ValueError, "producer|owner|evidence|transport|typed"):
            self._recover(live_page, source, absorption_evidence=ForgedEvidence())
        with self.assertRaisesRegex(ValueError, "producer|owner|evidence|transport|typed"):
            self._recover(live_page, source, absorption_evidence=ForgedValidator())

    def test_operational_root_handoff_schema_matches_runtime_scope_and_source_key_grammar(self) -> None:
        source = _live_source(revision=LIVE_H1)
        handoff = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        mapping = handoff.to_dict()
        schema = json.loads(
            (ROOT / "DEV/SCHEMAS/operational-root-handoff.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(OPERATIONAL_ROOT_HANDOFF_SCHEMA_VERSION, 2)
        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)
        self.assertIn("campaign_id", schema["properties"]["source_key"]["description"])
        validator = Draft202012Validator(schema)

        for invalid in (
            mapping | {"source_scope": "CAMPAIGN"},
            mapping | {"source_scope": "LIVE", "source_key": None},
            mapping | {"source_revision": "not a source revision"},
        ):
            with self.assertRaises(ValidationError):
                validator.validate(invalid)

        foreign_campaign = mapping | {
            "source_key": ["campaign-other", "scene-market", "epoch-1"]
        }
        validator.validate(foreign_campaign)
        with self.assertRaisesRegex(ValueError, "another campaign"):
            OperationalRootHandoff.from_mapping(foreign_campaign)

        with self.assertRaisesRegex(ValueError, "source key"):
            OperationalRootHandoff(
                campaign_id="campaign-frostfall",
                source_scope="CAMPAIGN",
                source_revision=LIVE_H0,
                source_key=source.source_key,
                roots=handoff.roots,
            )

    def test_recovery_roots_does_not_depend_directly_on_live_state(self) -> None:
        tree = ast.parse(
            (ROOT / "GAME/TOOLS/recovery_roots.py").read_text(encoding="utf-8")
        )
        direct_live_imports = [
            node
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module == "live_state"
        ]
        self.assertEqual(direct_live_imports, [])

    def test_campaign_to_live_and_live_to_campaign_preserve_root_identity(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        campaign_page = self._recover(live_page, source)
        campaign_retry = self._recover(campaign_page, source)

        self.assertEqual(live_page.source_scope, "LIVE")
        self.assertEqual(live_page.source_key, source.source_key)
        self.assertEqual(campaign_page.source_scope, "CAMPAIGN")
        self.assertEqual(campaign_page.source_revision, LIVE_H2)
        self.assertEqual(campaign_page.roots[0].key, self._page().roots[0].key)
        self.assertEqual(campaign_retry, campaign_page)

    def test_root_handoff_rejects_foreign_campaign_stale_source_and_interrupted_absorption(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        with self.assertRaisesRegex(ValueError, "campaign"):
            foreign_epoch = derive_live_epoch_id(
                "campaign-other", source.scene_id, source.opening_campaign_revision, source.claims
            )
            foreign_source = replace(
                source,
                campaign_id="campaign-other",
                epoch_id=foreign_epoch,
                source_ref=build_live_ref("campaign-other", source.scene_id, foreign_epoch),
            )
            self._recover(live_page, foreign_source)

        with self.assertRaisesRegex(ValueError, "source|revision"):
            self._recover(live_page, _live_source(revision=LIVE_H2))

        with self.assertRaisesRegex(ValueError, "ABSORBED|absorption"):
            handoff_operational_roots_to_campaign(
                live_page,
                live_source=replace(source, status=LiveLifecycle.CLOSED_UNABSORBED),
                live_route=_live_route(replace(source, status=LiveLifecycle.CLOSED)),
                campaign_revision=LIVE_H2,
                absorption_evidence=_accepted_absorption_publication(source),
            )

    def test_owner_handoff_rejects_caller_absorption_acknowledgement(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )

        with self.assertRaises(TypeError):
            handoff_operational_roots_to_campaign(
                live_page,
                live_source=replace(source, status=LiveLifecycle.ABSORBED),
                live_route=_live_route(replace(source, status=LiveLifecycle.CLOSED)),
                campaign_revision=LIVE_H2,
                absorption_evidence=_accepted_absorption_publication(source),
                absorption_acknowledged=True,
            )

    def test_root_recovery_rejects_caller_native_mapping_as_terminal_proof(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        root_key = live_page.roots[0].key
        terminal_owner = {
            "kind": "runtime.command",
            "command_id": "command-000001",
            "disposition": "command.settled",
            "pending_child_invocations": [],
        }

        with self.assertRaisesRegex(ValueError, "owner-issued|proof|delta"):
            self._recover(
                live_page,
                source,
                terminal_owner_keys=(root_key,),
                terminal_native_owners={root_key: terminal_owner},
            )

    def test_terminal_and_superseded_roots_are_not_reintroduced(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        root_key = live_page.roots[0].key
        terminal_owner = {
            "kind": "runtime.command",
            "command_id": "command-000001",
            "disposition": "command.settled",
            "pending_child_invocations": [],
        }
        replacement_delta = derive_operational_root_delta(
            "campaign-frostfall",
            "runtime.command",
            terminal_owner,
            existing_roots=(live_page.roots[0],),
        )
        terminal = self._recover(
            live_page,
            source,
            superseded_owner_keys=(root_key,),
            superseded_native_deltas={root_key: replacement_delta},
        )

        self.assertEqual(terminal.roots, ())

    def test_terminal_root_removal_requires_exact_native_terminal_evidence(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        root_key = live_page.roots[0].key
        terminal_owner = {
            "kind": "runtime.command",
            "command_id": "command-000001",
            "disposition": "command.settled",
            "pending_child_invocations": [],
        }
        terminal_delta = derive_operational_root_delta(
            "campaign-frostfall",
            "runtime.command",
            terminal_owner,
            existing_roots=(live_page.roots[0],),
        )
        with self.assertRaisesRegex(ValueError, "native"):
            self._recover(live_page, source, terminal_owner_keys=(root_key,))

        terminal = self._recover(
            live_page,
            source,
            terminal_owner_keys=(root_key,),
            terminal_native_owners={root_key: terminal_delta},
        )

        self.assertEqual(terminal.roots, ())

    def test_superseded_root_rejects_owner_issued_noop_or_enrollment_delta(self) -> None:
        source = _live_source(revision=LIVE_H1)
        live_page = handoff_operational_roots_to_live(
            self._page(),
            campaign_id="campaign-frostfall",
            campaign_revision=LIVE_H0,
            live_source_key=source.source_key,
            live_source_revision=source.source_revision,
        )
        root_key = live_page.roots[0].key
        active_owner = {
            "kind": "runtime.command",
            "command_id": "command-000001",
            "disposition": "command.accepted",
            "pending_child_invocations": [{"firing_key": "event-1:binding-1"}],
        }
        noop_delta = derive_operational_root_delta(
            "campaign-frostfall",
            "runtime.command",
            active_owner,
            existing_roots=(live_page.roots[0],),
        )
        enrollment_delta = derive_operational_root_delta(
            "campaign-frostfall",
            "runtime.command",
            active_owner,
        )
        self.assertEqual(noop_delta.action, "NOOP")
        self.assertEqual(enrollment_delta.action, "ENROLL")

        for delta in (noop_delta, enrollment_delta):
            with self.assertRaisesRegex(ValueError, "removal|replacement|delta"):
                self._recover(
                    live_page,
                    source,
                    superseded_owner_keys=(root_key,),
                    superseded_native_deltas={root_key: delta},
                )


class PlayerAccessTransitionTests(unittest.TestCase):
    def _campaign(self, *, revision: str = LIVE_H0, join_policy: str = "invite_only") -> dict[str, object]:
        return {
            "campaign_id": "campaign-frostfall",
            "revision": revision,
            "mode": "multiplayer",
            "players": {
                "join_policy": join_policy,
                "player_ids": ["player-1", "player-2"],
            },
        }

    def test_creator_provenance_has_no_public_caller_mint_factory(self) -> None:
        self.assertIsNone(getattr(access_control_module, "issue_first_initialization_provenance", None))

    def test_creator_provenance_cannot_be_forged_by_constructing_public_type(self) -> None:
        with self.assertRaises(HistoryContractError):
            FirstInitializationProvenance(
                campaign_id="campaign-frostfall",
                author_login="creator",
                initialization_revision=LIVE_H0,
                parent_revision=LIVE_H3,
            )

    def _resolved(self, principal: VerifiedPrincipal, player: Mapping[str, object]) -> PlayerResolution:
        return resolve_player(
            principal,
            _route(candidates=(str(player["player_id"]),)),
            lambda _player_id: player,
            campaign_id="campaign-frostfall",
        )

    def test_self_deactivation_is_exact_current_and_has_bounded_consumer_impact(self) -> None:
        principal = _principal()
        current = _player("player-1") | {
            "controlled_pc_ids": ["pc-1"],
            "history": ["resolution-1"],
        }
        after = current | {"status": "inactive", "deactivated_by": "self"}
        resolution = self._resolved(principal, current)
        route = _live_route()

        transition = freeze_player_access_transition(
            principal,
            resolution,
            operation="deactivate_self",
            current_player=current,
            proposed_player=after,
            current_campaign=self._campaign(),
            proposed_campaign=self._campaign(revision=LIVE_H1),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=route,
            live_source_keys=route.entries[0].source_key,
        )

        self.assertEqual(transition.player_id, "player-1")
        self.assertTrue(transition.impact.complete)
        self.assertEqual(
            transition.impact.live_source_keys,
            (route.entries[0].source_key,),
        )
        self.assertIn("player:player-1", transition.impact.collaboration_keys)
        self.assertIn("player:player-1", transition.impact.planning_catchup_keys)
        self.assertFalse(transition.historical_results_rewritten)

    def test_rejoin_reuses_identity_and_preserves_pc_and_history(self) -> None:
        principal = _principal()
        current = _player("player-1", status="inactive", deactivated_by="self") | {
            "controlled_pc_ids": ["pc-1"],
            "history": ["resolution-1"],
            "provenance": {"joined_event_id": "event-1"},
        }
        after = current | {"status": "active", "deactivated_by": None}
        resolution = self._resolved(principal, current)

        transition = freeze_player_access_transition(
            principal,
            resolution,
            operation="reactivate",
            current_player=current,
            proposed_player=after,
            current_campaign=self._campaign(),
            proposed_campaign=self._campaign(revision=LIVE_H1),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        self.assertTrue(transition.rejoin_preserves_player_identity)
        self.assertEqual(transition.player_id, "player-1")
        self.assertEqual(transition.preserved_controlled_pc_ids, ("pc-1",))
        self.assertEqual(transition.historical_result_ids, ("resolution-1",))

    def test_creator_grant_and_revoke_are_prospective_and_do_not_rewrite_history(self) -> None:
        creator = _principal(account_id="99", login="creator")
        target = _player("player-1", mechanical_override_policy=True) | {
            "history": ["resolution-1", "resolution-2"],
        }
        revoked = target | {
            "policy_authority": {"mechanical_override_policy": False},
        }
        target_resolution = self._resolved(_principal(), target)

        transition = freeze_player_access_transition(
            creator,
            target_resolution,
            operation="revoke_mechanical_override",
            current_player=target,
            proposed_player=revoked,
            current_campaign=self._campaign(),
            proposed_campaign=self._campaign(revision=LIVE_H1),
            creator_provenance=_creator_provenance(),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
            historical_result_ids=("resolution-1", "resolution-2"),
        )

        self.assertTrue(transition.prospective)
        self.assertFalse(transition.historical_results_rewritten)
        self.assertEqual(transition.historical_result_ids, ("resolution-1", "resolution-2"))

    def test_creator_only_join_policy_change_keeps_existing_bindings(self) -> None:
        creator = _principal(account_id="99", login="creator")
        transition = freeze_access_policy_transition(
            creator,
            current_campaign=self._campaign(),
            proposed_campaign=self._campaign(
                revision=LIVE_H1,
                join_policy="open_contributors",
            ),
            creator_provenance=_creator_provenance(),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        self.assertEqual(transition.transition_kind, "JOIN_POLICY_CHANGE")
        self.assertEqual(transition.impact.live_source_keys, ())
        self.assertIn("campaign:campaign-frostfall", transition.impact.collaboration_keys)
        self.assertTrue(transition.existing_player_bindings_preserved)

    def test_access_publication_and_recovery_share_one_after_authority_view(self) -> None:
        creator = _principal(account_id="99", login="creator")
        current = self._campaign() | {
            "metadata": {"display_name": "Frostfall", "region": "north"},
        }
        proposed = self._campaign(revision=LIVE_H1, join_policy="open_contributors") | {
            "metadata": {"display_name": "Frostfall", "region": "north"},
        }
        transition = freeze_access_policy_transition(
            creator,
            current_campaign=current,
            proposed_campaign=proposed,
            creator_provenance=_creator_provenance(),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        published = publish_access_policy_transition(
            transition,
            current_campaign_revision=LIVE_H0,
            current_campaign=current,
        )
        recovered = transition.recover_after_authority(proposed)

        self.assertEqual(published, recovered)
        self.assertEqual(
            published["campaign"]["metadata"],
            {"display_name": "Frostfall", "region": "north"},
        )
        with self.assertRaisesRegex(AccessControlContractError, "stale"):
            publish_access_policy_transition(
                transition,
                current_campaign_revision=LIVE_H1,
                current_campaign=current,
            )

    def test_access_publication_rejects_same_revision_unrelated_campaign_body_drift(self) -> None:
        creator = _principal(account_id="99", login="creator")
        current = self._campaign() | {"metadata": {"display_name": "Frostfall"}}
        proposed = self._campaign(revision=LIVE_H1, join_policy="open_contributors") | {
            "metadata": {"display_name": "Frostfall"},
        }
        transition = freeze_access_policy_transition(
            creator,
            current_campaign=current,
            proposed_campaign=proposed,
            creator_provenance=_creator_provenance(),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        with self.assertRaisesRegex(AccessControlContractError, "stale|currentness|body"):
            publish_access_policy_transition(
                transition,
                current_campaign_revision=LIVE_H0,
                current_campaign=current | {"metadata": {"display_name": "Drifted"}},
            )

    def test_access_recovery_rejects_same_revision_unrelated_campaign_body_drift(self) -> None:
        creator = _principal(account_id="99", login="creator")
        current = self._campaign() | {"metadata": {"display_name": "Frostfall"}}
        proposed = self._campaign(revision=LIVE_H1, join_policy="open_contributors") | {
            "metadata": {"display_name": "Frostfall"},
        }
        transition = freeze_access_policy_transition(
            creator,
            current_campaign=current,
            proposed_campaign=proposed,
            creator_provenance=_creator_provenance(),
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        with self.assertRaisesRegex(AccessControlContractError, "match|currentness|body"):
            transition.recover_after_authority(
                proposed | {"metadata": {"display_name": "Drifted"}},
            )

    def test_creator_uncertainty_fails_closed_for_campaign_policy_mutation(self) -> None:
        with self.assertRaises(AccessControlContractError) as context:
            freeze_access_policy_transition(
                _principal(),
                current_campaign=self._campaign(),
                proposed_campaign=self._campaign(
                    revision=LIVE_H1,
                    join_policy="open_contributors",
                ),
                creator_login="renamed-login",
                expected_campaign_revision=LIVE_H0,
                proposed_campaign_revision=LIVE_H1,
            )

        self.assertEqual(context.exception.failure_code, AuthorizationFailureCode.CREATOR_UNCERTAIN)

    def test_caller_creator_login_is_not_creator_provenance(self) -> None:
        with self.assertRaises(AccessControlContractError) as context:
            freeze_access_policy_transition(
                _principal(account_id="99", login="creator"),
                current_campaign=self._campaign(),
                proposed_campaign=self._campaign(
                    revision=LIVE_H1,
                    join_policy="open_contributors",
                ),
                creator_login="creator",
                expected_campaign_revision=LIVE_H0,
                proposed_campaign_revision=LIVE_H1,
            )

        self.assertEqual(context.exception.failure_code, AuthorizationFailureCode.CREATOR_UNCERTAIN)

    def test_owner_issued_first_initialization_provenance_authorizes_creator_transition(self) -> None:
        provenance = _issue_verified_first_initialization_history(
            campaign_id="campaign-frostfall",
            author_login="creator",
            initialization_revision=LIVE_H0,
            parent_revision=LIVE_H3,
        )
        transition = freeze_access_policy_transition(
            _principal(account_id="99", login="creator"),
            current_campaign=self._campaign(),
            proposed_campaign=self._campaign(
                revision=LIVE_H1,
                join_policy="open_contributors",
            ),
            creator_provenance=provenance,
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H1,
            live_route=_empty_live_route(),
        )

        self.assertEqual(transition.transition_kind, "JOIN_POLICY_CHANGE")

    def test_expected_campaign_revision_must_match_loaded_campaign_body(self) -> None:
        with self.assertRaisesRegex(AccessControlContractError, "revision|currentness") as context:
            freeze_access_policy_transition(
                _principal(account_id="99", login="creator"),
                current_campaign=self._campaign(revision=LIVE_H1),
                proposed_campaign=self._campaign(
                    revision=LIVE_H2,
                    join_policy="open_contributors",
                ),
                creator_provenance=_creator_provenance(),
                expected_campaign_revision=LIVE_H0,
                proposed_campaign_revision=LIVE_H2,
            )

        self.assertEqual(context.exception.failure_code, AuthorizationFailureCode.CURRENTNESS_CONFLICT)

    def test_player_transition_requires_exact_current_live_route_evidence(self) -> None:
        principal = _principal()
        current = _player("player-1")
        resolution = self._resolved(principal, current)

        with self.assertRaisesRegex(AccessControlContractError, "route|source|evidence"):
            freeze_player_access_transition(
                principal,
                resolution,
                operation="deactivate_self",
                current_player=current,
                proposed_player=current | {"status": "inactive", "deactivated_by": "self"},
                current_campaign=self._campaign(),
                proposed_campaign=self._campaign(revision=LIVE_H1),
                expected_campaign_revision=LIVE_H0,
                proposed_campaign_revision=LIVE_H1,
                live_source_keys=("campaign-frostfall", "scene-market", "e1-" + "a" * 64),
            )


class LiveAdditiveAuthorizationTests(unittest.TestCase):
    def _all_true(self) -> dict[str, bool]:
        return {
            "immutable_claim_sets_unchanged": True,
            "existing_writer_authorization_unchanged": True,
            "no_affected_controlled_pc_transfer": True,
            "no_selected_source_revoked_or_invalidated": True,
            "new_player_gains_no_live_write_without_reacquiring_obligations": True,
            "campaign_change_preserves_selected_live_routing_currentness": True,
        }

    def test_all_six_current_owner_predicates_allow_no_live_rollover(self) -> None:
        self.assertEqual(
            classify_additive_authorization_change(
                current_player=_player(),
                proposed_player=_player(),
                current_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "multiplayer",
                },
                proposed_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H1,
                    "mode": "multiplayer",
                },
                current_live_route=_empty_live_route(),
                proposed_live_route=_empty_live_route(),
            ),
            AdditiveAuthorizationDecision.NO_LIVE_ROLLOVER,
        )

    def test_missing_or_false_predicate_requires_live_transition(self) -> None:
        self.assertEqual(
            classify_additive_authorization_change(
                current_player=_player(),
                proposed_player=_player() | {"controlled_pc_ids": ["pc-2"]},
                current_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "multiplayer",
                },
                proposed_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H1,
                    "mode": "multiplayer",
                },
                current_live_route=_empty_live_route(),
                proposed_live_route=_empty_live_route(),
            ),
            AdditiveAuthorizationDecision.LIVE_TRANSITION_REQUIRED,
        )

    def test_caller_predicate_assertions_without_owner_evidence_fail_closed(self) -> None:
        self.assertEqual(
            classify_additive_authorization_change(**self._all_true()),
            AdditiveAuthorizationDecision.LIVE_TRANSITION_REQUIRED,
        )


class MultiLiveForwardTransitionTests(unittest.TestCase):
    def test_access_control_repair_advances_runtime_module_version(self) -> None:
        self.assertEqual(access_control_module.FRAMEWORK_MODULE_VERSION, "1.0.4")

    def _source(self, scene_id: str, actor_id: str, revision: str = LIVE_H0) -> LiveEnvelope:
        claims = (LiveClaim.exact_owner("world.actor", actor_id),)
        epoch_id = derive_live_epoch_id("campaign-frostfall", scene_id, LIVE_H0, claims)
        return LiveEnvelope(
            campaign_id="campaign-frostfall",
            scene_id=scene_id,
            epoch_id=epoch_id,
            opening_campaign_revision=LIVE_H0,
            source_ref=build_live_ref("campaign-frostfall", scene_id, epoch_id),
            source_revision=revision,
            claims=claims,
        )

    def test_multi_live_plan_binds_expected_campaign_revision_to_loaded_body(self) -> None:
        source = self._source("scene-a", "actor-a")
        route = build_live_route("campaign-frostfall", (source,))
        with self.assertRaisesRegex(AccessControlContractError, "revision|currentness"):
            try:
                freeze_multi_live_forward_plan(
                    route,
                    current_campaign={
                        "campaign_id": "campaign-frostfall",
                        "revision": LIVE_H1,
                        "mode": "multiplayer",
                    },
                    expected_campaign_revision=LIVE_H0,
                    proposed_campaign_revision=LIVE_H3,
                    proposed_source_revisions={source.source_key: LIVE_H2},
                )
            except TypeError as error:
                raise AssertionError("multi-LIVE plan lacks campaign-body currentness binding") from error

    def test_each_live_source_closes_by_own_cas_before_campaign_forward_publication(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
            accepted_history_refs=("resolution-1",),
        )

        progress = advance_multi_live_freeze(
            plan,
            acknowledgements={
                source_a.source_key: _accepted_ack(plan.attempts[0]),
                source_b.source_key: _accepted_ack(plan.attempts[1]),
            },
        )
        published = publish_forward_transition(
            plan,
            progress,
            current_campaign_revision=LIVE_H0,
            campaign_state={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
        )

        self.assertTrue(progress.ready_to_publish)
        self.assertEqual(published.campaign_state["revision"], LIVE_H3)
        self.assertTrue(
            all(source.status is LiveLifecycle.CLOSED_UNABSORBED for source in published.route.entries)
        )
        self.assertEqual(published.accepted_history_refs, ("resolution-1",))
        self.assertFalse(published.rollback_allowed)
        self.assertIsNone(published.chronology_order)

    def test_forward_publication_requires_exact_frozen_campaign_body(self) -> None:
        source = self._source("scene-a", "actor-a")
        plan = freeze_multi_live_forward_plan(
            build_live_route("campaign-frostfall", (source,)),
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source.source_key: LIVE_H1},
        )
        progress = advance_multi_live_freeze(
            plan,
            acknowledgements={source.source_key: _accepted_ack(plan.attempts[0])},
        )

        with self.assertRaisesRegex(AccessControlContractError, "campaign|body|currentness"):
            publish_forward_transition(
                plan,
                progress,
                current_campaign_revision=LIVE_H0,
                campaign_state={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "singleplayer",
                },
            )

    def test_forward_publication_rejects_unmodeled_frozen_campaign_body_field(self) -> None:
        source = self._source("scene-a", "actor-a")
        plan = freeze_multi_live_forward_plan(
            build_live_route("campaign-frostfall", (source,)),
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
                "metadata": {"display_name": "Frostfall"},
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source.source_key: LIVE_H1},
        )
        progress = advance_multi_live_freeze(
            plan,
            acknowledgements={source.source_key: _accepted_ack(plan.attempts[0])},
        )

        with self.assertRaisesRegex(AccessControlContractError, "campaign|body|currentness"):
            publish_forward_transition(
                plan,
                progress,
                current_campaign_revision=LIVE_H0,
                campaign_state={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "multiplayer",
                },
            )

    def test_closed_a_and_stale_b_block_campaign_transition_without_rollback(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
        )
        progress = advance_multi_live_freeze(
            plan,
            acknowledgements={
                source_a.source_key: _accepted_ack(plan.attempts[0]),
                source_b.source_key: {
                    "accepted": False,
                    "source_key": source_b.source_key,
                    "current_source_revision": LIVE_H3,
                    "reason": "stale_predecessor",
                },
            },
        )

        self.assertFalse(progress.ready_to_publish)
        self.assertEqual(progress.status, "REJECTED_STALE")
        with self.assertRaisesRegex(AccessControlContractError, "final|source|freeze"):
            publish_forward_transition(
                plan,
                progress,
                current_campaign_revision=LIVE_H0,
                campaign_state={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "multiplayer",
                },
            )

    def test_indeterminate_source_is_resolved_only_by_exact_source_read(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
        )
        progress = advance_multi_live_freeze(
            plan,
            acknowledgements={
                source_a.source_key: _accepted_ack(plan.attempts[0]),
                source_b.source_key: None,
            },
            current_sources={source_b.source_key: source_b},
        )

        self.assertFalse(progress.ready_to_publish)
        self.assertEqual(progress.status, "INDETERMINATE")

    def test_forged_typed_cas_result_is_not_live_owner_evidence(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
        )
        forged = LivePublicationResult(
            status=LivePublicationStatus.ACCEPTED,
            source_key=source_a.source_key,
            authoritative=True,
            observed_source_revision=LIVE_H1,
            accepted_source=plan.attempts[0].successor_route.entries[0],
            attempt=plan.attempts[0],
        )

        with self.assertRaisesRegex(AccessControlContractError, "owner-issued"):
            advance_multi_live_freeze(
                plan,
                acknowledgements={
                    source_a.source_key: forged,
                    source_b.source_key: _accepted_ack(plan.attempts[1]),
                },
            )

    def test_partial_recovery_preserves_a_closed_unabsorbed_when_b_is_stale(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
        )
        closed_a = mark_closed_unabsorbed(
            close_live_source(
                source_a,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        stale_b = replace(source_b, source_revision=LIVE_H3)
        current_route = build_live_route("campaign-frostfall", (closed_a, stale_b))
        recover = getattr(access_control_module, "recover_multi_live_forward_plan", None)
        self.assertIsNotNone(recover)
        progress = recover(
            plan,
            current_route=current_route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
        )

        self.assertEqual(progress.outcome_for(source_a.source_key), "CONFIRMED_CLOSED")
        self.assertEqual(progress.outcome_for(source_b.source_key), "REJECTED_STALE")
        self.assertEqual(progress.final_sources[0].status, LiveLifecycle.CLOSED_UNABSORBED)
        self.assertFalse(progress.ready_to_publish)

    def test_partial_recovery_preserves_a_closed_unabsorbed_when_b_is_indeterminate(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a, source_b))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1, source_b.source_key: LIVE_H2},
        )
        closed_a = mark_closed_unabsorbed(
            close_live_source(
                source_a,
                expected_source_revision=LIVE_H0,
                closed_source_revision=LIVE_H1,
            )
        )
        current_route = build_live_route("campaign-frostfall", (closed_a, source_b))
        recover = getattr(access_control_module, "recover_multi_live_forward_plan", None)
        self.assertIsNotNone(recover)
        progress = recover(
            plan,
            current_route=current_route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
        )

        self.assertEqual(progress.outcome_for(source_a.source_key), "CONFIRMED_CLOSED")
        self.assertEqual(progress.outcome_for(source_b.source_key), "INDETERMINATE")
        self.assertEqual(progress.final_sources[0].status, LiveLifecycle.CLOSED_UNABSORBED)
        self.assertFalse(progress.ready_to_publish)

    def test_partial_recovery_rejects_campaign_body_that_differs_from_frozen_cas_basis(self) -> None:
        source = self._source("scene-a", "actor-a")
        route = build_live_route("campaign-frostfall", (source,))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source.source_key: LIVE_H1},
        )
        recover = getattr(access_control_module, "recover_multi_live_forward_plan", None)
        self.assertIsNotNone(recover)
        with self.assertRaisesRegex(AccessControlContractError, "campaign|currentness|body"):
            recover(
                plan,
                current_route=route,
                current_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "singleplayer",
                },
            )

    def test_partial_recovery_rejects_route_membership_that_differs_from_frozen_route(self) -> None:
        source_a = self._source("scene-a", "actor-a")
        source_b = self._source("scene-b", "actor-b")
        route = build_live_route("campaign-frostfall", (source_a,))
        plan = freeze_multi_live_forward_plan(
            route,
            current_campaign={
                "campaign_id": "campaign-frostfall",
                "revision": LIVE_H0,
                "mode": "multiplayer",
            },
            expected_campaign_revision=LIVE_H0,
            proposed_campaign_revision=LIVE_H3,
            proposed_source_revisions={source_a.source_key: LIVE_H1},
        )
        recover = getattr(access_control_module, "recover_multi_live_forward_plan", None)
        self.assertIsNotNone(recover)
        with self.assertRaisesRegex(AccessControlContractError, "route|source|currentness"):
            recover(
                plan,
                current_route=build_live_route("campaign-frostfall", (source_a, source_b)),
                current_campaign={
                    "campaign_id": "campaign-frostfall",
                    "revision": LIVE_H0,
                    "mode": "multiplayer",
                },
            )


if __name__ == "__main__":
    unittest.main()
