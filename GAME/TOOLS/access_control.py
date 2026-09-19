"""Bounded authenticated-principal to PLAYER authorization routing.

The principal route is a derived lookup aid, not an identity or authorization
owner.  A route nominates candidate PLAYER IDs; every candidate is reloaded
from the exact current PLAYER owner before an operation can be authorized.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final, TypeAlias


AccountId: TypeAlias = str

# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.1"
ROUTE_SCHEMA_VERSION: Final = 1
ROUTE_KIND: Final = "runtime.principal_player_routing"
_RESOLUTION_TOKEN: Final = object()


class AccessControlContractError(ValueError):
    """Raised when an owner contract or typed identity is malformed."""

    failure_code: str

    def __init__(self, message: str, *, failure_code: str = "access.contract_invalid") -> None:
        super().__init__(message)
        self.failure_code = failure_code


class AuthorizationFailureCode(StrEnum):
    """Typed fail-closed outcomes for principal/PLAYER authorization."""

    PRINCIPAL_UNVERIFIED = "principal.unverified"
    ROUTE_ABSENT = "principal_player_route.absent"
    ROUTE_INCOMPLETE = "principal_player_route.incomplete"
    ROUTE_SCOPE_REQUIRED = "principal_player_route.scope_required"
    ROUTE_SCOPE_MISMATCH = "principal_player_route.scope_mismatch"
    STALE_CANDIDATE = "principal_player_route.stale_candidate"
    PLAYER_RECORD_INVALID = "player.record_invalid"
    AMBIGUOUS_BINDING = "player.binding_ambiguous"
    PLAYER_INACTIVE = "player.inactive"
    REJOIN_REQUIRES_CREATOR = "player.rejoin_requires_creator"
    POLICY_GRANT_REQUIRED = "policy.mechanical_override_grant_required"
    CURRENTNESS_CONFLICT = "access.currentness_conflict"
    TRANSITION_INVALID = "access.transition_invalid"
    CREATOR_UNCERTAIN = "creator.uncertain"
    OPERATION_UNSUPPORTED = "operation.unsupported"


def _account_id(value: object, label: str) -> AccountId:
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise AccessControlContractError(f"{label} must be a verified stable account ID")
    normalized = str(value)
    if not normalized:
        raise AccessControlContractError(f"{label} must be a nonempty verified stable account ID")
    return normalized


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise AccessControlContractError(f"{label} must be a nonempty string")
    return value


def _string_tuple(value: object, label: str, *, nonempty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise AccessControlContractError(f"{label} must be an array")
    result = tuple(_nonempty(item, f"{label} item") for item in value)
    if nonempty and not result:
        raise AccessControlContractError(f"{label} must not be empty")
    if len(result) != len(set(result)):
        raise AccessControlContractError(f"{label} must be unique")
    return result


@dataclass(frozen=True, slots=True)
class VerifiedPrincipal:
    """Current verified GitHub evidence, with stable ID separate from login."""

    stable_account_id: AccountId
    login: str
    provider: str = "github"
    verified: bool = True

    def __post_init__(self) -> None:
        account_id = _account_id(self.stable_account_id, "stable_account_id")
        login = _nonempty(self.login, "login")
        if self.provider != "github":
            raise AccessControlContractError("principal provider is not the admitted GitHub provider")
        if type(self.verified) is not bool or not self.verified:
            raise AccessControlContractError(
                "trustworthy current stable principal evidence is required",
                failure_code=AuthorizationFailureCode.PRINCIPAL_UNVERIFIED,
            )
        object.__setattr__(self, "stable_account_id", account_id)
        object.__setattr__(self, "login", login)


def resolve_principal(value: VerifiedPrincipal | Mapping[str, object]) -> VerifiedPrincipal:
    """Resolve only explicit verified stable GitHub principal evidence.

    Login, email and caller-provided PLAYER identifiers are deliberately not
    accepted as substitutes for the stable account ID.
    """

    if isinstance(value, VerifiedPrincipal):
        return value
    if not isinstance(value, Mapping):
        raise AccessControlContractError("verified principal evidence is required")
    if "email" in value:
        raise AccessControlContractError("email is not principal or invitation authority")
    allowed = {"provider", "stable_account_id", "login", "verified"}
    unknown = set(value) - allowed
    if unknown:
        raise AccessControlContractError("principal evidence contains unsupported authority fields")
    return VerifiedPrincipal(
        stable_account_id=_account_id(value.get("stable_account_id"), "stable_account_id"),
        login=_nonempty(value.get("login"), "login"),
        provider=_nonempty(value.get("provider", "github"), "provider"),
        verified=_verified_flag(value.get("verified", True)),
    )


def _verified_flag(value: object) -> bool:
    if type(value) is not bool:
        raise AccessControlContractError("principal verified flag must be boolean")
    return value


@dataclass(frozen=True, slots=True)
class PlayerRecord:
    """The exact current PLAYER fields needed for this route revalidation."""

    player_id: str
    stable_account_id: AccountId
    login: str | None
    status: str
    deactivated_by: str | None
    mechanical_override_policy: bool = False
    controlled_pc_ids: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> PlayerRecord:
        player_id = _nonempty(value.get("player_id"), "PLAYER player_id")
        status = value.get("status")
        if status not in {"active", "inactive"}:
            raise AccessControlContractError("PLAYER status is not admitted")
        raw_binding = value.get("github_binding")
        if not isinstance(raw_binding, Mapping):
            raise AccessControlContractError("PLAYER github_binding is required")
        stable_account_id = _account_id(raw_binding.get("user_id"), "PLAYER github_binding.user_id")
        raw_login = raw_binding.get("login")
        login = None if raw_login is None else _nonempty(raw_login, "PLAYER github_binding.login")
        raw_deactivated_by = value.get("deactivated_by")
        if raw_deactivated_by not in {None, "self", "creator"}:
            raise AccessControlContractError("PLAYER deactivated_by is not admitted")
        raw_policy_authority = value.get("policy_authority")
        if raw_policy_authority is None:
            mechanical_override_policy = False
        elif not isinstance(raw_policy_authority, Mapping):
            raise AccessControlContractError("PLAYER policy_authority is not admitted")
        else:
            raw_grant = raw_policy_authority.get("mechanical_override_policy", False)
            if raw_grant is None:
                mechanical_override_policy = False
            elif type(raw_grant) is not bool:
                raise AccessControlContractError(
                    "PLAYER mechanical_override_policy must be boolean or null"
                )
            else:
                mechanical_override_policy = raw_grant
        raw_controlled_pc_ids = value.get("controlled_pc_ids", ())
        controlled_pc_ids = _string_tuple(
            raw_controlled_pc_ids,
            "PLAYER controlled_pc_ids",
            nonempty=False,
        )
        return cls(
            player_id=player_id,
            stable_account_id=stable_account_id,
            login=login,
            status=status,
            deactivated_by=raw_deactivated_by,
            mechanical_override_policy=mechanical_override_policy,
            controlled_pc_ids=controlled_pc_ids,
        )


PlayerLoader: TypeAlias = Callable[[str], Mapping[str, object] | PlayerRecord | None]


@dataclass(frozen=True, slots=True)
class RouteEntry:
    """One derived stable-account-to-candidate-PLAYER route entry."""

    stable_account_id: AccountId
    candidate_player_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "stable_account_id",
            _account_id(self.stable_account_id, "route stable_account_id"),
        )
        candidates = _string_tuple(self.candidate_player_ids, "route candidate_player_ids")
        object.__setattr__(self, "candidate_player_ids", candidates)


@dataclass(frozen=True, slots=True)
class PrincipalPlayerRoute:
    """Completeness-protected derived route companion for one campaign."""

    campaign_id: str
    entries: tuple[RouteEntry, ...]
    complete: bool = True

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "route campaign_id")
        if type(self.complete) is not bool or not self.complete:
            raise AccessControlContractError(
                "principal PLAYER route must be complete",
                failure_code=AuthorizationFailureCode.ROUTE_INCOMPLETE,
            )
        seen_accounts: set[str] = set()
        seen_players: set[str] = set()
        for entry in self.entries:
            if not isinstance(entry, RouteEntry):
                raise AccessControlContractError("principal PLAYER route entries must be typed")
            if entry.stable_account_id in seen_accounts:
                raise AccessControlContractError("route stable account IDs must be unique")
            seen_accounts.add(entry.stable_account_id)
            overlap = seen_players.intersection(entry.candidate_player_ids)
            if overlap:
                raise AccessControlContractError("route candidate PLAYER IDs must be unique")
            seen_players.update(entry.candidate_player_ids)

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> PrincipalPlayerRoute:
        if not isinstance(value, Mapping):
            raise AccessControlContractError("principal PLAYER route must be an object")
        expected = {"schema_version", "kind", "campaign_id", "complete", "entries"}
        if set(value) != expected:
            raise AccessControlContractError("principal PLAYER route has unexpected or missing fields")
        if value["schema_version"] != ROUTE_SCHEMA_VERSION:
            raise AccessControlContractError("unsupported principal PLAYER route schema")
        if value["kind"] != ROUTE_KIND:
            raise AccessControlContractError("principal PLAYER route kind is not admitted")
        raw_entries = value["entries"]
        if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
            raise AccessControlContractError("principal PLAYER route entries must be an array")
        entries: list[RouteEntry] = []
        for raw_entry in raw_entries:
            if not isinstance(raw_entry, Mapping):
                raise AccessControlContractError("principal PLAYER route entry must be an object")
            if set(raw_entry) != {"stable_account_id", "candidate_player_ids"}:
                raise AccessControlContractError("principal PLAYER route entry has unexpected fields")
            entries.append(
                RouteEntry(
                    stable_account_id=_account_id(
                        raw_entry["stable_account_id"], "route stable_account_id"
                    ),
                    candidate_player_ids=_string_tuple(
                        raw_entry["candidate_player_ids"], "route candidate_player_ids"
                    ),
                )
            )
        return cls(
            campaign_id=_nonempty(value["campaign_id"], "route campaign_id"),
            entries=tuple(entries),
            complete=value["complete"],  # type: ignore[arg-type]
        )

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": ROUTE_SCHEMA_VERSION,
            "kind": ROUTE_KIND,
            "campaign_id": self.campaign_id,
            "complete": True,
            "entries": [
                {
                    "stable_account_id": entry.stable_account_id,
                    "candidate_player_ids": list(entry.candidate_player_ids),
                }
                for entry in self.entries
            ],
        }

    def for_account(self, stable_account_id: AccountId) -> RouteEntry | None:
        account_id = _account_id(stable_account_id, "principal stable_account_id")
        return next(
            (entry for entry in self.entries if entry.stable_account_id == account_id),
            None,
        )


def build_principal_player_route(
    campaign_id: str,
    players: Sequence[PlayerRecord | Mapping[str, object]],
) -> PrincipalPlayerRoute:
    """Derive a complete route from an explicit current PLAYER owner result.

    This builder accepts only the bounded PLAYER set supplied by the native
    owner.  It does not discover records, consult a generic PLAYER index or
    authorize from the derived companion itself.  Duplicate bindings remain represented
    as multiple candidates so a later authorization read fails closed rather
    than selecting a first match.
    """

    by_account: dict[AccountId, list[str]] = {}
    player_accounts: dict[str, AccountId] = {}
    for raw_player in players:
        player = raw_player if isinstance(raw_player, PlayerRecord) else PlayerRecord.from_mapping(raw_player)
        previous_account = player_accounts.get(player.player_id)
        if previous_account is not None and previous_account != player.stable_account_id:
            raise AccessControlContractError("PLAYER identity appears under multiple stable accounts")
        player_accounts[player.player_id] = player.stable_account_id
        by_account.setdefault(player.stable_account_id, []).append(player.player_id)
    entries = tuple(
        RouteEntry(account_id, tuple(sorted(candidate_ids)))
        for account_id, candidate_ids in sorted(by_account.items())
    )
    return PrincipalPlayerRoute(campaign_id=campaign_id, entries=entries)


@dataclass(frozen=True, slots=True)
class PlayerResolution:
    """Exact PLAYER reload result, including a typed non-authorizing outcome."""

    status: str
    player: PlayerRecord | None = None
    failure_code: AuthorizationFailureCode | None = None
    principal_account_id: AccountId | None = None
    _issuer: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        valid_statuses = {"AUTHORIZED_PLAYER", "INACTIVE_REJOIN_CANDIDATE", "FAIL_CLOSED"}
        if self.status not in valid_statuses:
            raise AccessControlContractError("PLAYER resolution status is not admitted")
        if self.status == "FAIL_CLOSED":
            if self.player is not None or self.failure_code is None:
                raise AccessControlContractError("fail-closed PLAYER resolution is incomplete")
        elif self.player is None or self.failure_code is not None:
            raise AccessControlContractError("successful PLAYER resolution is incomplete")

    @property
    def player_id(self) -> str | None:
        return None if self.player is None else self.player.player_id


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    """Typed authorized PLAYER or fail-closed operation result."""

    authorized: bool
    player_id: str | None = None
    failure_code: AuthorizationFailureCode | None = None

    def __post_init__(self) -> None:
        if type(self.authorized) is not bool:
            raise AccessControlContractError("authorization decision must be boolean")
        if self.authorized and self.failure_code is not None:
            raise AccessControlContractError("authorized result cannot carry a failure")
        if not self.authorized and self.failure_code is None:
            raise AccessControlContractError("fail-closed result requires a typed failure")

    @property
    def status(self) -> str:
        return "AUTHORIZED" if self.authorized else "FAIL_CLOSED"


def _fail(code: AuthorizationFailureCode) -> AuthorizationDecision:
    return AuthorizationDecision(authorized=False, failure_code=code)


def resolve_player(
    principal: VerifiedPrincipal | Mapping[str, object],
    route: PrincipalPlayerRoute | Mapping[str, object] | None,
    load_exact_player: PlayerLoader,
    *,
    campaign_id: str | None = None,
) -> PlayerResolution:
    """Resolve candidates from the route and revalidate every exact PLAYER body.

    The loader is called only for candidate IDs named by the route.  A missing,
    stale or malformed candidate invalidates the route; no index or repository
    scan is permitted as a fallback.
    """

    resolved_principal = resolve_principal(principal)
    if route is None:
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=AuthorizationFailureCode.ROUTE_ABSENT,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    try:
        resolved_route = (
            route
            if isinstance(route, PrincipalPlayerRoute)
            else PrincipalPlayerRoute.from_mapping(route)
        )
    except AccessControlContractError as error:
        failure_code = (
            AuthorizationFailureCode.ROUTE_INCOMPLETE
            if error.failure_code == AuthorizationFailureCode.ROUTE_INCOMPLETE
            else AuthorizationFailureCode.PLAYER_RECORD_INVALID
        )
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=failure_code,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    if not isinstance(campaign_id, str) or not campaign_id:
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=AuthorizationFailureCode.ROUTE_SCOPE_REQUIRED,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    if resolved_route.campaign_id != campaign_id:
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=AuthorizationFailureCode.ROUTE_SCOPE_MISMATCH,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    if not callable(load_exact_player):
        raise AccessControlContractError("exact PLAYER loader is required")
    entry = resolved_route.for_account(resolved_principal.stable_account_id)
    if entry is None:
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=AuthorizationFailureCode.ROUTE_ABSENT,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )

    matching: list[PlayerRecord] = []
    for candidate_id in entry.candidate_player_ids:
        try:
            raw_player = load_exact_player(candidate_id)
        except (AccessControlContractError, KeyError, OSError, TypeError):
            raw_player = None
        if raw_player is None:
            return PlayerResolution(
                status="FAIL_CLOSED",
                failure_code=AuthorizationFailureCode.STALE_CANDIDATE,
                principal_account_id=resolved_principal.stable_account_id,
                _issuer=_RESOLUTION_TOKEN,
            )
        try:
            player = (
                raw_player
                if isinstance(raw_player, PlayerRecord)
                else PlayerRecord.from_mapping(raw_player)
            )
        except (AccessControlContractError, AttributeError, TypeError):
            return PlayerResolution(
                status="FAIL_CLOSED",
                failure_code=AuthorizationFailureCode.PLAYER_RECORD_INVALID,
                principal_account_id=resolved_principal.stable_account_id,
                _issuer=_RESOLUTION_TOKEN,
            )
        if (
            player.player_id != candidate_id
            or player.stable_account_id != resolved_principal.stable_account_id
        ):
            return PlayerResolution(
                status="FAIL_CLOSED",
                failure_code=AuthorizationFailureCode.STALE_CANDIDATE,
                principal_account_id=resolved_principal.stable_account_id,
                _issuer=_RESOLUTION_TOKEN,
            )
        matching.append(player)

    if len(matching) != 1:
        return PlayerResolution(
            status="FAIL_CLOSED",
            failure_code=AuthorizationFailureCode.AMBIGUOUS_BINDING,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    player = matching[0]
    if player.status == "active":
        return PlayerResolution(
            status="AUTHORIZED_PLAYER",
            player=player,
            principal_account_id=resolved_principal.stable_account_id,
            _issuer=_RESOLUTION_TOKEN,
        )
    return PlayerResolution(
        status="INACTIVE_REJOIN_CANDIDATE",
        player=player,
        principal_account_id=resolved_principal.stable_account_id,
        _issuer=_RESOLUTION_TOKEN,
    )


def authorize_operation(
    principal: VerifiedPrincipal | Mapping[str, object],
    resolution: PlayerResolution | None = None,
    *,
    operation: str,
    creator_login: str | None = None,
) -> AuthorizationDecision:
    """Apply operation-specific authorization after principal/PLAYER routing."""

    resolved_principal = resolve_principal(principal)
    if operation in {"creator_write", "creator_only"}:
        if creator_login is None or creator_login != resolved_principal.login:
            return _fail(AuthorizationFailureCode.CREATOR_UNCERTAIN)
        return AuthorizationDecision(authorized=True, player_id=None)

    if resolution is None:
        return _fail(AuthorizationFailureCode.ROUTE_ABSENT)
    if (
        resolution._issuer is not _RESOLUTION_TOKEN
        or resolution.principal_account_id != resolved_principal.stable_account_id
    ):
        return _fail(AuthorizationFailureCode.PLAYER_RECORD_INVALID)
    if resolution.failure_code is not None:
        return _fail(resolution.failure_code)
    if resolution.player is None:
        return _fail(AuthorizationFailureCode.PLAYER_RECORD_INVALID)
    if operation == "mechanical_override_policy":
        if resolution.player.status != "active":
            return _fail(AuthorizationFailureCode.PLAYER_INACTIVE)
        if creator_login is not None:
            return _fail(AuthorizationFailureCode.CREATOR_UNCERTAIN)
        if resolution.player.mechanical_override_policy:
            return AuthorizationDecision(authorized=True, player_id=resolution.player.player_id)
        return _fail(AuthorizationFailureCode.POLICY_GRANT_REQUIRED)
    if operation in {"rejoin", "reactivate"}:
        if resolution.player.status == "active":
            return AuthorizationDecision(authorized=True, player_id=resolution.player.player_id)
        if resolution.player.deactivated_by == "self":
            return AuthorizationDecision(authorized=True, player_id=resolution.player.player_id)
        return _fail(AuthorizationFailureCode.REJOIN_REQUIRES_CREATOR)
    if operation not in {"gameplay", "write", "interpretive_policy", "mechanical_override_policy"}:
        return _fail(AuthorizationFailureCode.OPERATION_UNSUPPORTED)
    if resolution.player.status != "active":
        return _fail(AuthorizationFailureCode.PLAYER_INACTIVE)
    return AuthorizationDecision(authorized=True, player_id=resolution.player.player_id)


class AdditiveAuthorizationDecision(StrEnum):
    """Whether an additive access change can preserve selected LIVE sources."""

    NO_LIVE_ROLLOVER = "NO_LIVE_ROLLOVER"
    LIVE_TRANSITION_REQUIRED = "LIVE_TRANSITION_REQUIRED"


class AccessTransitionKind(StrEnum):
    """Closed set of campaign access mutations owned by this module."""

    DEACTIVATE_SELF = "DEACTIVATE_SELF"
    DEACTIVATE_CREATOR = "DEACTIVATE_CREATOR"
    REACTIVATE = "REACTIVATE"
    GRANT_MECHANICAL_OVERRIDE = "GRANT_MECHANICAL_OVERRIDE"
    REVOKE_MECHANICAL_OVERRIDE = "REVOKE_MECHANICAL_OVERRIDE"
    MODE_CHANGE = "MODE_CHANGE"
    JOIN_POLICY_CHANGE = "JOIN_POLICY_CHANGE"
    MODE_AND_JOIN_POLICY_CHANGE = "MODE_AND_JOIN_POLICY_CHANGE"


LiveSourceKeyValue: TypeAlias = tuple[str, str, str]


def _transition_source_key(value: object, label: str = "LIVE source key") -> LiveSourceKeyValue:
    """Normalize one exact semantic source key without accepting route names."""

    if hasattr(value, "source_key"):
        value = getattr(value, "source_key")
    if isinstance(value, Mapping):
        value = value.get("source_key")
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise AccessControlContractError(
            f"{label} must be (campaign_id, scene_id, epoch_id)",
            failure_code=AuthorizationFailureCode.TRANSITION_INVALID,
        )
    return tuple(_nonempty(item, f"{label} component") for item in value)  # type: ignore[return-value]


def _transition_source_keys(value: object) -> tuple[LiveSourceKeyValue, ...]:
    if value is None:
        return ()
    if hasattr(value, "source_key") or isinstance(value, Mapping):
        raw_items: Sequence[object] = (value,)
    elif (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
        and len(value) == 3
        and all(isinstance(item, str) for item in value)
    ):
        raw_items = (value,)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        raw_items = value
    else:
        raise AccessControlContractError("LIVE source keys must be a bounded sequence")
    normalized = tuple(_transition_source_key(item) for item in raw_items)
    if len(normalized) != len(set(normalized)):
        raise AccessControlContractError("LIVE source keys must be unique")
    return normalized


def _mapping_copy(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, Mapping):
        raise AccessControlContractError(f"{label} must be an object")
    return deepcopy(dict(value))


def _revision_value(value: object, label: str) -> str:
    return _nonempty(value, label)


@dataclass(frozen=True, slots=True)
class CampaignAccessState:
    """Exact campaign-domain access/configuration evidence for one revision."""

    campaign_id: str
    revision: str
    mode: str
    join_policy: str
    player_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "campaign_id")
        _revision_value(self.revision, "campaign revision")
        if self.mode not in {"singleplayer", "multiplayer"}:
            raise AccessControlContractError("campaign mode is not admitted")
        if self.join_policy not in {"invite_only", "open_contributors"}:
            raise AccessControlContractError("campaign join policy is not admitted")
        object.__setattr__(
            self,
            "player_ids",
            _string_tuple(self.player_ids, "campaign player_ids", nonempty=False),
        )

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, object],
        *,
        revision: str | None = None,
    ) -> CampaignAccessState:
        raw = _mapping_copy(value, "campaign access state")
        campaign_id = _nonempty(raw.get("campaign_id"), "campaign_id")
        raw_revision = raw.get("revision", raw.get("campaign_revision", raw.get("current_revision")))
        if revision is not None:
            raw_revision = revision
        if raw_revision is None:
            raise AccessControlContractError("exact current campaign revision is required")
        mode = raw.get("mode")
        if mode not in {"singleplayer", "multiplayer"}:
            raise AccessControlContractError("campaign mode is not admitted")
        players = raw.get("players")
        if players is not None and not isinstance(players, Mapping):
            raise AccessControlContractError("campaign players access state must be an object")
        join_policy = raw.get("join_policy")
        if join_policy is None and isinstance(players, Mapping):
            join_policy = players.get("join_policy")
        if join_policy is None:
            join_policy = "invite_only"
        raw_player_ids = raw.get("player_ids")
        if raw_player_ids is None and isinstance(players, Mapping):
            raw_player_ids = players.get("player_ids", ())
        if raw_player_ids is None:
            raw_player_ids = ()
        return cls(
            campaign_id=campaign_id,
            revision=_revision_value(raw_revision, "campaign revision"),
            mode=mode,  # type: ignore[arg-type]
            join_policy=join_policy,  # type: ignore[arg-type]
            player_ids=_string_tuple(raw_player_ids, "campaign player_ids", nonempty=False),
        )

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "revision": self.revision,
            "mode": self.mode,
            "players": {
                "join_policy": self.join_policy,
                "player_ids": list(self.player_ids),
            },
        }


def _campaign_state(
    value: CampaignAccessState | Mapping[str, object],
    *,
    revision: str | None = None,
) -> CampaignAccessState:
    if isinstance(value, CampaignAccessState):
        if revision is None or value.revision == revision:
            return value
        return CampaignAccessState(
            campaign_id=value.campaign_id,
            revision=revision,
            mode=value.mode,
            join_policy=value.join_policy,
            player_ids=value.player_ids,
        )
    return CampaignAccessState.from_mapping(value, revision=revision)


def _campaign_transition_mapping(
    value: CampaignAccessState | Mapping[str, object],
    state: CampaignAccessState,
) -> dict[str, object]:
    """Retain unrelated campaign fields while replacing only access/currentness data."""

    raw = (
        value.as_mapping()
        if isinstance(value, CampaignAccessState)
        else _mapping_copy(value, "campaign access state")
    )
    raw["campaign_id"] = state.campaign_id
    if "campaign_revision" in raw:
        raw["campaign_revision"] = state.revision
    elif "current_revision" in raw and "revision" not in raw:
        raw["current_revision"] = state.revision
    else:
        raw["revision"] = state.revision
    raw["mode"] = state.mode
    players = raw.get("players")
    if not isinstance(players, Mapping):
        players = {}
    else:
        players = deepcopy(dict(players))
    players["join_policy"] = state.join_policy
    players["player_ids"] = list(state.player_ids)
    raw["players"] = players
    return raw


@dataclass(frozen=True, slots=True)
class AccessConsumerImpact:
    """Complete bounded consumer set for one campaign access closure."""

    live_source_keys: tuple[LiveSourceKeyValue, ...] = ()
    collaboration_keys: tuple[str, ...] = ()
    planning_catchup_keys: tuple[str, ...] = ()
    publication_consumers: tuple[str, ...] = ()
    complete: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "live_source_keys", _transition_source_keys(self.live_source_keys))
        for field_name in (
            "collaboration_keys",
            "planning_catchup_keys",
            "publication_consumers",
        ):
            value = _string_tuple(getattr(self, field_name), field_name, nonempty=False)
            object.__setattr__(self, field_name, value)
        if type(self.complete) is not bool or not self.complete:
            raise AccessControlContractError("access transition impact must be complete")

    def as_mapping(self) -> dict[str, object]:
        return {
            "live_source_keys": [list(key) for key in self.live_source_keys],
            "collaboration_keys": list(self.collaboration_keys),
            "planning_catchup_keys": list(self.planning_catchup_keys),
            "publication_consumers": list(self.publication_consumers),
            "complete": True,
        }


def _player_state(value: PlayerRecord | Mapping[str, object], label: str) -> tuple[PlayerRecord, dict[str, object]]:
    raw = (
        {
            "player_id": value.player_id,
            "status": value.status,
            "deactivated_by": value.deactivated_by,
            "github_binding": {
                "user_id": value.stable_account_id,
                "login": value.login,
            },
            "controlled_pc_ids": list(value.controlled_pc_ids),
            "policy_authority": {
                "mechanical_override_policy": value.mechanical_override_policy,
            },
        }
        if isinstance(value, PlayerRecord)
        else _mapping_copy(value, label)
    )
    try:
        return PlayerRecord.from_mapping(raw), raw
    except (AccessControlContractError, TypeError, AttributeError) as error:
        raise AccessControlContractError(
            f"{label} is not an exact current PLAYER record",
            failure_code=AuthorizationFailureCode.PLAYER_RECORD_INVALID,
        ) from error


def _player_semantics(record: PlayerRecord) -> tuple[object, ...]:
    return (
        record.player_id,
        record.stable_account_id,
        record.login,
        record.mechanical_override_policy,
        record.controlled_pc_ids,
    )


def _history_projection(value: Mapping[str, object]) -> dict[str, object]:
    keys = (
        "history",
        "historical_results",
        "accepted_results",
        "accepted_resolution_ids",
        "provenance",
        "provenance_refs",
    )
    return {key: deepcopy(value[key]) for key in keys if key in value}


def _history_ids(value: Mapping[str, object]) -> tuple[str, ...]:
    for key in ("historical_result_ids", "accepted_resolution_ids", "history"):
        raw = value.get(key)
        if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
            if all(isinstance(item, str) and item for item in raw):
                return tuple(raw)
    return ()


def _require_exact_resolution(
    resolution: PlayerResolution | None,
    current: PlayerRecord,
) -> None:
    if not isinstance(resolution, PlayerResolution) or resolution._issuer is not _RESOLUTION_TOKEN:
        raise AccessControlContractError(
            "access mutation requires W03.T01 owner-issued PLAYER resolution",
            failure_code=AuthorizationFailureCode.PLAYER_RECORD_INVALID,
        )
    if resolution.failure_code is not None or resolution.player is None:
        raise AccessControlContractError(
            "access mutation requires a resolved exact current PLAYER",
            failure_code=resolution.failure_code or AuthorizationFailureCode.PLAYER_RECORD_INVALID,
        )
    if _player_semantics(resolution.player) != _player_semantics(current):
        raise AccessControlContractError(
            "PLAYER mutation predecessor differs from exact W03.T01 resolution",
            failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
        )


def _require_creator(
    principal: VerifiedPrincipal | Mapping[str, object],
    creator_login: str | None,
) -> VerifiedPrincipal:
    resolved = resolve_principal(principal)
    decision = authorize_operation(resolved, operation="creator_only", creator_login=creator_login)
    if not decision.authorized:
        raise AccessControlContractError(
            "creator authority is uncertain; mutation fails closed",
            failure_code=decision.failure_code or AuthorizationFailureCode.CREATOR_UNCERTAIN,
        )
    return resolved


def _impact(
    campaign: CampaignAccessState,
    *,
    player_ids: Sequence[str],
    source_keys: Sequence[LiveSourceKeyValue],
    publication_paths: Sequence[str],
) -> AccessConsumerImpact:
    ids = tuple(dict.fromkeys(_nonempty(item, "impact player_id") for item in player_ids))
    collaboration = tuple(
        dict.fromkeys(
            (f"campaign:{campaign.campaign_id}", *(f"player:{item}" for item in ids))
        )
    )
    planning = tuple(dict.fromkeys(f"player:{item}" for item in ids))
    return AccessConsumerImpact(
        live_source_keys=tuple(source_keys),
        collaboration_keys=collaboration,
        planning_catchup_keys=planning,
        publication_consumers=tuple(
            dict.fromkeys(
                (
                    *publication_paths,
                    "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml",
                )
            )
        ),
    )


def _additive_assessment(
    evidence: Mapping[str, object] | None,
    *,
    has_live_sources: bool,
) -> tuple[AdditiveAuthorizationDecision, tuple[str, ...]]:
    if evidence is None:
        if not has_live_sources:
            return AdditiveAuthorizationDecision.NO_LIVE_ROLLOVER, ()
        return (
            AdditiveAuthorizationDecision.LIVE_TRANSITION_REQUIRED,
            (
                "immutable_claim_sets_unchanged",
                "existing_writer_authorization_unchanged",
                "no_affected_controlled_pc_transfer",
                "no_selected_source_revoked_or_invalidated",
                "new_player_gains_no_live_write_without_reacquiring_obligations",
                "campaign_change_preserves_selected_live_routing_currentness",
            ),
        )
    decision = classify_additive_authorization_change(**dict(evidence))
    names = (
        "immutable_claim_sets_unchanged",
        "existing_writer_authorization_unchanged",
        "no_affected_controlled_pc_transfer",
        "no_selected_source_revoked_or_invalidated",
        "new_player_gains_no_live_write_without_reacquiring_obligations",
        "campaign_change_preserves_selected_live_routing_currentness",
    )
    failed = tuple(name for name in names if evidence.get(name) is not True)
    return decision, failed


def classify_additive_authorization_change(
    immutable_claim_sets_unchanged: bool = False,
    existing_writer_authorization_unchanged: bool = False,
    no_affected_controlled_pc_transfer: bool = False,
    no_selected_source_revoked_or_invalidated: bool = False,
    new_player_gains_no_live_write_without_reacquiring_obligations: bool = False,
    campaign_change_preserves_selected_live_routing_currentness: bool = False,
    **aliases: object,
) -> AdditiveAuthorizationDecision:
    """Apply the six exact current-owner predicates for additive activation.

    Missing or malformed evidence is deliberately equivalent to false.  The
    function is a classifier only; a LIVE transition is separately frozen and
    published through the exact-source CAS owner.
    """

    if isinstance(immutable_claim_sets_unchanged, Mapping):
        supplied = dict(immutable_claim_sets_unchanged)
        immutable_claim_sets_unchanged = supplied.pop("immutable_claim_sets_unchanged", False)  # type: ignore[assignment]
        aliases = supplied | aliases
    alias_names = {
        "immutable_claims_unchanged": "immutable_claim_sets_unchanged",
        "claims_unchanged": "immutable_claim_sets_unchanged",
        "existing_writers_unchanged": "existing_writer_authorization_unchanged",
        "no_controlled_pc_transfer": "no_affected_controlled_pc_transfer",
        "no_source_revocation": "no_selected_source_revoked_or_invalidated",
        "no_selected_source_revoked": "no_selected_source_revoked_or_invalidated",
        "new_player_requires_obligation_reacquisition": (
            "new_player_gains_no_live_write_without_reacquiring_obligations"
        ),
        "new_player_no_live_write_without_obligations": (
            "new_player_gains_no_live_write_without_reacquiring_obligations"
        ),
        "selected_live_routing_unchanged": "campaign_change_preserves_selected_live_routing_currentness",
        "selected_live_routing_currentness_unchanged": "campaign_change_preserves_selected_live_routing_currentness",
    }
    values = {
        "immutable_claim_sets_unchanged": immutable_claim_sets_unchanged,
        "existing_writer_authorization_unchanged": existing_writer_authorization_unchanged,
        "no_affected_controlled_pc_transfer": no_affected_controlled_pc_transfer,
        "no_selected_source_revoked_or_invalidated": no_selected_source_revoked_or_invalidated,
        "new_player_gains_no_live_write_without_reacquiring_obligations": (
            new_player_gains_no_live_write_without_reacquiring_obligations
        ),
        "campaign_change_preserves_selected_live_routing_currentness": (
            campaign_change_preserves_selected_live_routing_currentness
        ),
    }
    for alias, canonical in aliases.items():
        if alias not in alias_names:
            raise AccessControlContractError(f"unsupported additive authorization predicate: {alias}")
        canonical_value = aliases[alias]
        if type(canonical_value) is not bool:
            raise AccessControlContractError(f"additive predicate {alias} must be boolean")
        values[alias_names[alias]] = canonical_value
    if not all(type(value) is bool and value for value in values.values()):
        return AdditiveAuthorizationDecision.LIVE_TRANSITION_REQUIRED
    return AdditiveAuthorizationDecision.NO_LIVE_ROLLOVER


@dataclass(frozen=True, slots=True)
class FrozenAccessPolicyTransition:
    """Immutable campaign access mutation and its bounded after-authority impact."""

    transition_kind: AccessTransitionKind | str
    campaign_id: str
    expected_campaign_revision: str
    proposed_campaign_revision: str
    current_campaign: Mapping[str, object]
    proposed_campaign: Mapping[str, object]
    current_player: Mapping[str, object] | None
    proposed_player: Mapping[str, object] | None
    impact: AccessConsumerImpact
    live_rollover: AdditiveAuthorizationDecision
    failed_additive_predicates: tuple[str, ...] = ()
    historical_result_ids: tuple[str, ...] = ()
    historical_results_rewritten: bool = False
    rejoin_preserves_player_identity: bool = False
    existing_player_bindings_preserved: bool = True
    prospective: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "campaign_id", _nonempty(self.campaign_id, "campaign_id"))
        _revision_value(self.expected_campaign_revision, "expected campaign revision")
        _revision_value(self.proposed_campaign_revision, "proposed campaign revision")
        if self.expected_campaign_revision == self.proposed_campaign_revision:
            raise AccessControlContractError("access mutation must advance campaign currentness")
        if not isinstance(self.impact, AccessConsumerImpact) or not self.impact.complete:
            raise AccessControlContractError("access mutation impact is incomplete")
        object.__setattr__(self, "current_campaign", _mapping_copy(self.current_campaign, "current campaign"))
        object.__setattr__(self, "proposed_campaign", _mapping_copy(self.proposed_campaign, "proposed campaign"))
        for field_name in ("current_player", "proposed_player"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _mapping_copy(value, field_name))
        object.__setattr__(self, "historical_result_ids", _string_tuple(self.historical_result_ids, "historical_result_ids", nonempty=False))
        object.__setattr__(self, "failed_additive_predicates", _string_tuple(self.failed_additive_predicates, "failed_additive_predicates", nonempty=False))
        if type(self.historical_results_rewritten) is not bool or self.historical_results_rewritten:
            raise AccessControlContractError("access transitions cannot rewrite accepted history")
        if type(self.prospective) is not bool or not self.prospective:
            raise AccessControlContractError("access policy changes are prospective")

    @property
    def player_id(self) -> str | None:
        if self.current_player is None:
            return None
        return self.current_player.get("player_id")  # type: ignore[return-value]

    @property
    def preserved_controlled_pc_ids(self) -> tuple[str, ...]:
        if self.current_player is None:
            return ()
        raw = self.current_player.get("controlled_pc_ids", ())
        return _string_tuple(raw, "controlled_pc_ids", nonempty=False)

    def as_mapping(self) -> dict[str, object]:
        return {
            "transition_kind": str(self.transition_kind),
            "campaign_id": self.campaign_id,
            "expected_campaign_revision": self.expected_campaign_revision,
            "proposed_campaign_revision": self.proposed_campaign_revision,
            "current_campaign": deepcopy(dict(self.current_campaign)),
            "proposed_campaign": deepcopy(dict(self.proposed_campaign)),
            "current_player": None if self.current_player is None else deepcopy(dict(self.current_player)),
            "proposed_player": None if self.proposed_player is None else deepcopy(dict(self.proposed_player)),
            "impact": self.impact.as_mapping(),
            "live_rollover": str(self.live_rollover),
            "failed_additive_predicates": list(self.failed_additive_predicates),
            "historical_result_ids": list(self.historical_result_ids),
            "historical_results_rewritten": False,
            "rejoin_preserves_player_identity": self.rejoin_preserves_player_identity,
            "existing_player_bindings_preserved": self.existing_player_bindings_preserved,
            "prospective": True,
        }

    @property
    def after_authority_view(self) -> dict[str, object]:
        """The deterministic campaign-closure view used by publication/recovery."""

        return {
            "campaign": deepcopy(dict(self.proposed_campaign)),
            "player": None if self.proposed_player is None else deepcopy(dict(self.proposed_player)),
            "impact": self.impact.as_mapping(),
            "live_rollover": str(self.live_rollover),
            "historical_results_rewritten": False,
        }

    def recover_after_authority(
        self,
        campaign: CampaignAccessState | Mapping[str, object],
        player: PlayerRecord | Mapping[str, object] | None = None,
    ) -> dict[str, object]:
        """Reproduce the same after-view from one exact published campaign read."""

        observed_campaign = _campaign_state(campaign)
        expected_campaign = _campaign_state(self.proposed_campaign)
        if observed_campaign != expected_campaign:
            raise AccessControlContractError(
                "recovered campaign does not match the frozen after-authority view",
                failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
            )
        if self.proposed_player is not None:
            if player is None:
                raise AccessControlContractError("recovery requires the exact published PLAYER record")
            observed_player, observed_raw = _player_state(player, "recovered PLAYER")
            expected_player, expected_raw = _player_state(self.proposed_player, "proposed PLAYER")
            if (
                _player_semantics(observed_player) != _player_semantics(expected_player)
                or _history_projection(observed_raw) != _history_projection(expected_raw)
            ):
                raise AccessControlContractError(
                    "recovered PLAYER does not match the frozen after-authority view",
                    failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
                )
        return self.after_authority_view


def _freeze_player_access_transition(
    principal: VerifiedPrincipal | Mapping[str, object],
    resolution: PlayerResolution | None,
    *,
    operation: str,
    current_player: PlayerRecord | Mapping[str, object],
    proposed_player: PlayerRecord | Mapping[str, object],
    current_campaign: CampaignAccessState | Mapping[str, object],
    proposed_campaign: CampaignAccessState | Mapping[str, object],
    creator_login: str | None,
    expected_campaign_revision: str | None,
    proposed_campaign_revision: str | None,
    live_source_keys: object,
    additive_evidence: Mapping[str, object] | None,
    historical_result_ids: Sequence[str],
) -> FrozenAccessPolicyTransition:
    normalized_operation = operation.strip().lower().replace("-", "_")
    operation_aliases = {
        "deactivate": "deactivate_self",
        "remove_self": "deactivate_self",
        "remove_creator": "deactivate_creator",
        "activate": "reactivate",
        "rejoin": "reactivate",
        "grant": "grant_mechanical_override",
        "revoke": "revoke_mechanical_override",
    }
    normalized_operation = operation_aliases.get(normalized_operation, normalized_operation)
    allowed_operations = {
        "deactivate_self",
        "deactivate_creator",
        "reactivate",
        "grant_mechanical_override",
        "revoke_mechanical_override",
    }
    if normalized_operation not in allowed_operations:
        raise AccessControlContractError(
            "unsupported PLAYER access transition",
            failure_code=AuthorizationFailureCode.OPERATION_UNSUPPORTED,
        )

    resolved_principal = resolve_principal(principal)
    before, before_raw = _player_state(current_player, "current PLAYER")
    after, after_raw = _player_state(proposed_player, "proposed PLAYER")
    _require_exact_resolution(resolution, before)
    if before.player_id != after.player_id or before.stable_account_id != after.stable_account_id:
        raise AccessControlContractError("PLAYER identity and binding are immutable in an access transition")
    if _history_projection(before_raw) != _history_projection(after_raw):
        raise AccessControlContractError("accepted PLAYER history/provenance cannot be rewritten")
    if normalized_operation == "deactivate_self":
        decision = authorize_operation(resolved_principal, resolution, operation="gameplay")
        if not decision.authorized or before.stable_account_id != resolved_principal.stable_account_id:
            raise AccessControlContractError(
                "self deactivation requires the exact active PLAYER authority",
                failure_code=decision.failure_code or AuthorizationFailureCode.PLAYER_RECORD_INVALID,
            )
        if (before.status, after.status, after.deactivated_by) != ("active", "inactive", "self"):
            raise AccessControlContractError("self deactivation has an invalid status transition")
    elif normalized_operation == "deactivate_creator":
        _require_creator(resolved_principal, creator_login)
        if before.stable_account_id == resolved_principal.stable_account_id:
            raise AccessControlContractError("creator cannot deactivate their own PLAYER binding")
        if (before.status, after.status, after.deactivated_by) != ("active", "inactive", "creator"):
            raise AccessControlContractError("creator deactivation has an invalid status transition")
    elif normalized_operation == "reactivate":
        if before.status != "inactive" or after.status != "active" or after.deactivated_by is not None:
            raise AccessControlContractError("reactivation must be inactive -> active and clear deactivated_by")
        if before.deactivated_by == "self":
            decision = authorize_operation(resolved_principal, resolution, operation="rejoin")
            if (
                not decision.authorized
                or before.stable_account_id != resolved_principal.stable_account_id
            ):
                _require_creator(resolved_principal, creator_login)
        else:
            _require_creator(resolved_principal, creator_login)
    else:
        _require_creator(resolved_principal, creator_login)
        if before.status != after.status or before.deactivated_by != after.deactivated_by:
            raise AccessControlContractError("policy grant/revocation cannot change membership status")
        if normalized_operation == "grant_mechanical_override":
            if before.mechanical_override_policy or not after.mechanical_override_policy:
                raise AccessControlContractError("mechanical override grant must be false -> true")
        elif not before.mechanical_override_policy or after.mechanical_override_policy:
            raise AccessControlContractError("mechanical override revocation must be true -> false")
    if before.controlled_pc_ids != after.controlled_pc_ids:
        raise AccessControlContractError("access transition cannot transfer controlled PCs")
    if normalized_operation in {"deactivate_self", "deactivate_creator", "reactivate"}:
        if before.mechanical_override_policy != after.mechanical_override_policy:
            raise AccessControlContractError("membership transition cannot change policy grant")

    expected = expected_campaign_revision
    proposed = proposed_campaign_revision
    before_campaign = _campaign_state(current_campaign, revision=expected)
    after_campaign = _campaign_state(proposed_campaign, revision=proposed)
    if before_campaign.campaign_id != after_campaign.campaign_id:
        raise AccessControlContractError("campaign identity is immutable")
    if (
        before_campaign.mode,
        before_campaign.join_policy,
        before_campaign.player_ids,
    ) != (
        after_campaign.mode,
        after_campaign.join_policy,
        after_campaign.player_ids,
    ):
        raise AccessControlContractError("PLAYER mutation cannot change campaign access policy")
    source_keys = _transition_source_keys(live_source_keys)
    decision, failed = _additive_assessment(
        additive_evidence,
        has_live_sources=bool(source_keys),
    )
    if normalized_operation in {"deactivate_self", "deactivate_creator", "revoke_mechanical_override"} and source_keys:
        decision = AdditiveAuthorizationDecision.LIVE_TRANSITION_REQUIRED
        failed = failed or ("access_revocation_requires_source_freeze",)
    impact = _impact(
        before_campaign,
        player_ids=(before.player_id,),
        source_keys=source_keys,
        publication_paths=(f"WORLD/PLAYERS/{before.player_id}.yaml",),
    )
    ids = tuple(historical_result_ids) if historical_result_ids else _history_ids(before_raw)
    return FrozenAccessPolicyTransition(
        transition_kind=AccessTransitionKind({
            "deactivate_self": AccessTransitionKind.DEACTIVATE_SELF,
            "deactivate_creator": AccessTransitionKind.DEACTIVATE_CREATOR,
            "reactivate": AccessTransitionKind.REACTIVATE,
            "grant_mechanical_override": AccessTransitionKind.GRANT_MECHANICAL_OVERRIDE,
            "revoke_mechanical_override": AccessTransitionKind.REVOKE_MECHANICAL_OVERRIDE,
        }[normalized_operation]),
        campaign_id=before_campaign.campaign_id,
        expected_campaign_revision=before_campaign.revision,
        proposed_campaign_revision=after_campaign.revision,
        current_campaign=_campaign_transition_mapping(current_campaign, before_campaign),
        proposed_campaign=_campaign_transition_mapping(proposed_campaign, after_campaign),
        current_player=before_raw,
        proposed_player=after_raw,
        impact=impact,
        live_rollover=decision,
        failed_additive_predicates=failed,
        historical_result_ids=ids,
        rejoin_preserves_player_identity=normalized_operation == "reactivate",
    )


def freeze_player_access_transition(
    principal: VerifiedPrincipal | Mapping[str, object],
    resolution: PlayerResolution | None = None,
    *,
    operation: str,
    current_player: PlayerRecord | Mapping[str, object],
    proposed_player: PlayerRecord | Mapping[str, object],
    current_campaign: CampaignAccessState | Mapping[str, object],
    proposed_campaign: CampaignAccessState | Mapping[str, object],
    creator_login: str | None = None,
    expected_campaign_revision: str | None = None,
    proposed_campaign_revision: str | None = None,
    current_campaign_revision: str | None = None,
    next_campaign_revision: str | None = None,
    live_source_keys: object = (),
    live_sources: object | None = None,
    additive_evidence: Mapping[str, object] | None = None,
    historical_result_ids: Sequence[str] = (),
) -> FrozenAccessPolicyTransition:
    """Freeze one exact current PLAYER mutation; publication is separate."""

    if live_sources is not None:
        live_source_keys = live_sources
    if expected_campaign_revision is None:
        expected_campaign_revision = current_campaign_revision
    if proposed_campaign_revision is None:
        proposed_campaign_revision = next_campaign_revision
    return _freeze_player_access_transition(
        principal,
        resolution,
        operation=operation,
        current_player=current_player,
        proposed_player=proposed_player,
        current_campaign=current_campaign,
        proposed_campaign=proposed_campaign,
        creator_login=creator_login,
        expected_campaign_revision=expected_campaign_revision,
        proposed_campaign_revision=proposed_campaign_revision,
        live_source_keys=live_source_keys,
        additive_evidence=additive_evidence,
        historical_result_ids=historical_result_ids,
    )


def freeze_access_policy_transition(
    principal: VerifiedPrincipal | Mapping[str, object],
    resolution: PlayerResolution | None = None,
    *,
    current_campaign: CampaignAccessState | Mapping[str, object],
    proposed_campaign: CampaignAccessState | Mapping[str, object],
    creator_login: str | None = None,
    expected_campaign_revision: str | None = None,
    proposed_campaign_revision: str | None = None,
    current_campaign_revision: str | None = None,
    next_campaign_revision: str | None = None,
    current_player: PlayerRecord | Mapping[str, object] | None = None,
    proposed_player: PlayerRecord | Mapping[str, object] | None = None,
    operation: str | None = None,
    live_source_keys: object = (),
    live_sources: object | None = None,
    additive_evidence: Mapping[str, object] | None = None,
    historical_result_ids: Sequence[str] = (),
) -> FrozenAccessPolicyTransition:
    """Freeze creator-owned campaign policy or PLAYER grant transitions."""

    if live_sources is not None:
        live_source_keys = live_sources
    if expected_campaign_revision is None:
        expected_campaign_revision = current_campaign_revision
    if proposed_campaign_revision is None:
        proposed_campaign_revision = next_campaign_revision
    if current_player is not None or proposed_player is not None:
        if current_player is None or proposed_player is None:
            raise AccessControlContractError("PLAYER policy transition requires both exact states")
        if operation is None:
            before, _ = _player_state(current_player, "current PLAYER")
            after, _ = _player_state(proposed_player, "proposed PLAYER")
            operation = (
                "grant_mechanical_override"
                if not before.mechanical_override_policy and after.mechanical_override_policy
                else "revoke_mechanical_override"
            )
        return _freeze_player_access_transition(
            principal,
            resolution,
            operation=operation,
            current_player=current_player,
            proposed_player=proposed_player,
            current_campaign=current_campaign,
            proposed_campaign=proposed_campaign,
            creator_login=creator_login,
            expected_campaign_revision=expected_campaign_revision,
            proposed_campaign_revision=proposed_campaign_revision,
            live_source_keys=live_source_keys,
            additive_evidence=additive_evidence,
            historical_result_ids=historical_result_ids,
        )

    resolved_principal = _require_creator(principal, creator_login)
    before = _campaign_state(current_campaign, revision=expected_campaign_revision)
    after = _campaign_state(proposed_campaign, revision=proposed_campaign_revision)
    if before.campaign_id != after.campaign_id:
        raise AccessControlContractError("campaign identity is immutable")
    if before.player_ids != after.player_ids:
        raise AccessControlContractError("join-policy mutation cannot revoke or create PLAYER bindings")
    mode_changed = before.mode != after.mode
    join_changed = before.join_policy != after.join_policy
    if not mode_changed and not join_changed:
        raise AccessControlContractError("campaign access policy transition has no admitted mutation")
    kind = (
        AccessTransitionKind.MODE_AND_JOIN_POLICY_CHANGE
        if mode_changed and join_changed
        else AccessTransitionKind.MODE_CHANGE
        if mode_changed
        else AccessTransitionKind.JOIN_POLICY_CHANGE
    )
    source_keys = _transition_source_keys(live_source_keys)
    decision, failed = _additive_assessment(additive_evidence, has_live_sources=bool(source_keys))
    impact = _impact(
        before,
        player_ids=before.player_ids,
        source_keys=source_keys,
        publication_paths=("MANIFEST.yaml", "CONFIG.yaml"),
    )
    _ = resolved_principal
    return FrozenAccessPolicyTransition(
        transition_kind=kind,
        campaign_id=before.campaign_id,
        expected_campaign_revision=before.revision,
        proposed_campaign_revision=after.revision,
        current_campaign=_campaign_transition_mapping(current_campaign, before),
        proposed_campaign=_campaign_transition_mapping(proposed_campaign, after),
        current_player=None,
        proposed_player=None,
        impact=impact,
        live_rollover=decision,
        failed_additive_predicates=failed,
        existing_player_bindings_preserved=True,
    )


def publish_access_policy_transition(
    transition: FrozenAccessPolicyTransition,
    *,
    current_campaign_revision: str,
    current_campaign: CampaignAccessState | Mapping[str, object] | None = None,
    current_player: PlayerRecord | Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Authorize one campaign closure after exact currentness revalidation.

    The function returns a publication candidate; the native campaign writer
    remains the only physical publisher.
    """

    if not isinstance(transition, FrozenAccessPolicyTransition):
        raise AccessControlContractError("access publication requires a typed frozen transition")
    if current_campaign_revision != transition.expected_campaign_revision:
        raise AccessControlContractError(
            "access publication predecessor is stale",
            failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
        )
    if current_campaign is not None:
        observed_campaign = _campaign_state(current_campaign, revision=current_campaign_revision)
        expected_campaign = _campaign_state(transition.current_campaign)
        if observed_campaign != expected_campaign:
            raise AccessControlContractError(
                "access publication campaign evidence is stale",
                failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
            )
    if transition.current_player is not None:
        if current_player is None:
            raise AccessControlContractError("access publication requires exact current PLAYER evidence")
        observed_player, observed_raw = _player_state(current_player, "current PLAYER")
        expected_player, expected_raw = _player_state(transition.current_player, "frozen PLAYER")
        if (
            _player_semantics(observed_player) != _player_semantics(expected_player)
            or _history_projection(observed_raw) != _history_projection(expected_raw)
        ):
            raise AccessControlContractError(
                "access publication PLAYER evidence is stale",
                failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
            )
    return transition.after_authority_view


@dataclass(frozen=True, slots=True)
class MultiLiveClosePlan:
    """One independently CAS-fenced source inside a multi-LIVE transition."""

    source_key: LiveSourceKeyValue
    source: object
    expected_source_revision: str
    proposed_source_revision: str
    attempt: object | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_key", _transition_source_key(self.source_key))
        _revision_value(self.expected_source_revision, "expected LIVE source revision")
        _revision_value(self.proposed_source_revision, "proposed LIVE source revision")


@dataclass(frozen=True, slots=True)
class FrozenMultiLiveForwardPlan:
    """Ephemeral exact-source freeze plan; it is not a distributed transaction."""

    campaign_id: str
    expected_campaign_revision: str
    proposed_campaign_revision: str
    selected_route: object
    sources: tuple[MultiLiveClosePlan, ...]
    accepted_history_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "multi-LIVE campaign_id")
        _revision_value(self.expected_campaign_revision, "expected campaign revision")
        _revision_value(self.proposed_campaign_revision, "proposed campaign revision")
        if self.expected_campaign_revision == self.proposed_campaign_revision:
            raise AccessControlContractError("multi-LIVE forward plan must advance campaign currentness")
        if not self.sources:
            raise AccessControlContractError("multi-LIVE forward plan requires at least one source")
        keys = tuple(item.source_key for item in self.sources)
        if len(keys) != len(set(keys)):
            raise AccessControlContractError("multi-LIVE source keys must be unique")
        object.__setattr__(self, "accepted_history_refs", _string_tuple(self.accepted_history_refs, "accepted_history_refs", nonempty=False))

    @property
    def attempts(self) -> tuple[object, ...]:
        return tuple(item.attempt for item in self.sources if item.attempt is not None)

    @property
    def source_keys(self) -> tuple[LiveSourceKeyValue, ...]:
        return tuple(item.source_key for item in self.sources)

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "expected_campaign_revision": self.expected_campaign_revision,
            "proposed_campaign_revision": self.proposed_campaign_revision,
            "source_keys": [list(key) for key in self.source_keys],
            "accepted_history_refs": list(self.accepted_history_refs),
        }


@dataclass(frozen=True, slots=True)
class MultiLiveFreezeProgress:
    """Owner evidence accumulated without rolling back accepted source closes."""

    plan: FrozenMultiLiveForwardPlan
    status: str
    final_sources: tuple[object, ...]
    outcomes: tuple[tuple[LiveSourceKeyValue, str], ...]

    @property
    def ready_to_publish(self) -> bool:
        return self.status == "READY_TO_PUBLISH"

    @property
    def closed_source_keys(self) -> tuple[LiveSourceKeyValue, ...]:
        return tuple(key for key, outcome in self.outcomes if outcome == "CONFIRMED_CLOSED")

    def outcome_for(self, source_key: Sequence[str]) -> str:
        key = _transition_source_key(source_key)
        for candidate, outcome in self.outcomes:
            if candidate == key:
                return outcome
        raise KeyError(key)


@dataclass(frozen=True, slots=True)
class ForwardTransitionPublication:
    """Pure after-authority campaign view after all source closes are proven."""

    campaign_state: Mapping[str, object]
    route: object
    accepted_history_refs: tuple[str, ...]
    rollback_allowed: bool = False
    chronology_order: None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "campaign_state", _mapping_copy(self.campaign_state, "published campaign state"))
        object.__setattr__(self, "accepted_history_refs", _string_tuple(self.accepted_history_refs, "accepted_history_refs", nonempty=False))
        if self.rollback_allowed:
            raise AccessControlContractError("forward transition cannot enable rollback")
        if self.chronology_order is not None:
            raise AccessControlContractError("CAS order cannot become fictional chronology")


def _transition_mapping_lookup(value: object, source: MultiLiveClosePlan, index: int) -> object | None:
    if value is None:
        return None
    if isinstance(value, Mapping):
        for key in (source.source_key, source.source_key[2], getattr(source.source, "source_ref", None), index):
            try:
                if key in value:
                    return value[key]
            except TypeError:
                continue
        return None
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return value[index] if index < len(value) else None
    raise AccessControlContractError("multi-LIVE evidence must be keyed by exact source")


def _live_modules() -> tuple[object, ...]:
    from .live_state import (
        LiveContractError,
        LiveEnvelope,
        LiveLifecycle,
        LivePublicationResult,
        LivePublicationStatus,
        LiveRouting,
        build_live_route,
        classify_cas_result,
        freeze_live_attempt,
        mark_closed_unabsorbed,
        reconcile_indeterminate,
        select_live_source,
        validate_live_route_completeness,
    )

    return (
        LiveContractError,
        LiveEnvelope,
        LiveLifecycle,
        LivePublicationResult,
        LivePublicationStatus,
        LiveRouting,
        build_live_route,
        classify_cas_result,
        freeze_live_attempt,
        mark_closed_unabsorbed,
        reconcile_indeterminate,
        select_live_source,
        validate_live_route_completeness,
    )


def freeze_multi_live_forward_plan(
    route: object | None = None,
    *,
    live_route: object | None = None,
    expected_campaign_revision: str | None = None,
    proposed_campaign_revision: str | None = None,
    current_campaign_revision: str | None = None,
    next_campaign_revision: str | None = None,
    proposed_source_revisions: Mapping[object, str] | Sequence[str] | None = None,
    source_revisions: Mapping[object, str] | Sequence[str] | None = None,
    accepted_history_refs: Sequence[str] = (),
) -> FrozenMultiLiveForwardPlan:
    """Pin exact campaign/LIVE inputs and create one CAS attempt per source."""

    if route is None:
        route = live_route
    if expected_campaign_revision is None:
        expected_campaign_revision = current_campaign_revision
    if proposed_campaign_revision is None:
        proposed_campaign_revision = next_campaign_revision
    (
        live_error,
        live_envelope,
        live_lifecycle,
        _live_publication_result,
        _live_publication_status,
        live_routing,
        _build_live_route,
        _classify_cas_result,
        freeze_live_attempt,
        _mark_closed_unabsorbed,
        _reconcile_indeterminate,
        _select_live_source,
        validate_live_route_completeness,
    ) = _live_modules()
    if not isinstance(route, live_routing) or not route.complete:
        raise AccessControlContractError("multi-LIVE forward plan requires a complete exact route")
    validate_live_route_completeness(route)
    expected = _revision_value(expected_campaign_revision, "expected campaign revision")
    proposed = _revision_value(proposed_campaign_revision, "proposed campaign revision")
    if expected == proposed:
        raise AccessControlContractError("multi-LIVE forward plan must advance campaign currentness")
    revisions = proposed_source_revisions if proposed_source_revisions is not None else source_revisions
    if revisions is None:
        raise AccessControlContractError("each selected LIVE source needs an exact proposed revision")
    sources: list[MultiLiveClosePlan] = []
    for index, source in enumerate(route.entries):
        proposed_source_revision = _transition_mapping_lookup(
            revisions,
            MultiLiveClosePlan(
                source_key=source.source_key,
                source=source,
                expected_source_revision=source.source_revision,
                proposed_source_revision=source.source_revision,
                attempt=None,
            ),
            index,
        )
        if proposed_source_revision is None:
            raise AccessControlContractError("multi-LIVE proposed revisions are incomplete")
        proposed_source_revision = _revision_value(
            proposed_source_revision,
            "proposed LIVE source revision",
        )
        if source.status is live_lifecycle.ACTIVE:
            try:
                attempt = freeze_live_attempt(
                    source,
                    route=route,
                    proposed_source_revision=proposed_source_revision,
                    transition_kind="CLOSE",
                )
            except (live_error, TypeError, ValueError) as error:
                raise AccessControlContractError(
                    "multi-LIVE source close cannot be frozen from exact current route",
                    failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
                ) from error
        elif source.status in {live_lifecycle.CLOSED, live_lifecycle.CLOSED_UNABSORBED}:
            if proposed_source_revision != source.source_revision:
                raise AccessControlContractError(
                    "already closed LIVE source cannot be reopened or advanced by this plan"
                )
            attempt = None
        else:
            raise AccessControlContractError("absorbed LIVE source cannot be selected for forward freeze")
        sources.append(
            MultiLiveClosePlan(
                source_key=source.source_key,
                source=source,
                expected_source_revision=source.source_revision,
                proposed_source_revision=proposed_source_revision,
                attempt=attempt,
            )
        )
    return FrozenMultiLiveForwardPlan(
        campaign_id=route.campaign_id,
        expected_campaign_revision=expected,
        proposed_campaign_revision=proposed,
        selected_route=route,
        sources=tuple(sources),
        accepted_history_refs=tuple(accepted_history_refs),
    )


def advance_multi_live_freeze(
    plan: FrozenMultiLiveForwardPlan,
    acknowledgements: Mapping[object, object] | Sequence[object] | None = None,
    *,
    cas_results: Mapping[object, object] | Sequence[object] | None = None,
    current_sources: Mapping[object, object] | Sequence[object] | None = None,
    exact_sources: Mapping[object, object] | Sequence[object] | None = None,
) -> MultiLiveFreezeProgress:
    """Accumulate independent source CAS outcomes; never undo a confirmed close."""

    if not isinstance(plan, FrozenMultiLiveForwardPlan):
        raise AccessControlContractError("multi-LIVE freeze progress requires a typed plan")
    if acknowledgements is None:
        acknowledgements = cas_results
    if exact_sources is not None:
        current_sources = exact_sources
    (
        live_error,
        live_envelope,
        live_lifecycle,
        live_publication_result,
        live_publication_status,
        _live_routing,
        _build_live_route,
        classify_cas_result,
        _freeze_live_attempt,
        mark_closed_unabsorbed,
        reconcile_indeterminate,
        _select_live_source,
        _validate_live_route_completeness,
    ) = _live_modules()
    final_sources: list[object] = []
    outcomes: list[tuple[LiveSourceKeyValue, str]] = []
    for index, source_plan in enumerate(plan.sources):
        source = source_plan.source
        if source_plan.attempt is None:
            if source.status is live_lifecycle.CLOSED:
                final_source = mark_closed_unabsorbed(source)
            elif source.status is live_lifecycle.CLOSED_UNABSORBED:
                final_source = source
            else:
                raise AccessControlContractError("closed-source plan has invalid LIVE lifecycle")
            final_sources.append(final_source)
            outcomes.append((source_plan.source_key, "CONFIRMED_CLOSED"))
            continue
        acknowledgement = _transition_mapping_lookup(acknowledgements, source_plan, index)
        if isinstance(acknowledgement, live_publication_result):
            if acknowledgement.attempt is not source_plan.attempt:
                raise AccessControlContractError("LIVE CAS result is bound to another frozen attempt")
            result = acknowledgement
        else:
            result = classify_cas_result(source_plan.attempt, acknowledgement)
        if result.status is live_publication_status.ACCEPTED and result.accepted_source is not None:
            final_sources.append(mark_closed_unabsorbed(result.accepted_source))
            outcomes.append((source_plan.source_key, "CONFIRMED_CLOSED"))
            continue
        if result.status is live_publication_status.INDETERMINATE:
            current = _transition_mapping_lookup(current_sources, source_plan, index)
            if current is not None:
                if not isinstance(current, live_envelope):
                    try:
                        current = live_envelope.from_mapping(current)
                    except (live_error, TypeError, ValueError) as error:
                        raise AccessControlContractError(
                            "indeterminate LIVE result requires exact typed source evidence"
                        ) from error
                if current.status is live_lifecycle.CLOSED_UNABSORBED:
                    if (
                        current.source_key == source_plan.source_key
                        and current.source_revision == source_plan.proposed_source_revision
                    ):
                        final_sources.append(current)
                        outcomes.append((source_plan.source_key, "CONFIRMED_CLOSED"))
                        continue
                reconciled = reconcile_indeterminate(source_plan.attempt, current)
                if reconciled.status is live_publication_status.ACCEPTED and reconciled.accepted_source is not None:
                    final_sources.append(mark_closed_unabsorbed(reconciled.accepted_source))
                    outcomes.append((source_plan.source_key, "CONFIRMED_CLOSED"))
                    continue
                result = reconciled
            outcomes.append((source_plan.source_key, "INDETERMINATE"))
            continue
        if result.status is live_publication_status.REJECTED_STALE:
            outcomes.append((source_plan.source_key, "REJECTED_STALE"))
        else:
            outcomes.append((source_plan.source_key, "REJECTED"))
    outcome_values = tuple(outcome for _, outcome in outcomes)
    if all(value == "CONFIRMED_CLOSED" for value in outcome_values):
        status = "READY_TO_PUBLISH"
    elif "REJECTED_STALE" in outcome_values:
        status = "REJECTED_STALE"
    elif "REJECTED" in outcome_values:
        status = "REJECTED"
    else:
        status = "INDETERMINATE"
    return MultiLiveFreezeProgress(
        plan=plan,
        status=status,
        final_sources=tuple(final_sources),
        outcomes=tuple(outcomes),
    )


def publish_forward_transition(
    plan: FrozenMultiLiveForwardPlan,
    progress: MultiLiveFreezeProgress,
    *,
    current_campaign_revision: str | None = None,
    campaign_revision: str | None = None,
    campaign_state: Mapping[str, object] | None = None,
    campaign_after: Mapping[str, object] | None = None,
    campaign_acknowledgement: Mapping[str, object] | None = None,
) -> ForwardTransitionPublication:
    """Build the campaign after-view only after every exact source is closed."""

    if not isinstance(plan, FrozenMultiLiveForwardPlan) or progress.plan is not plan:
        raise AccessControlContractError("forward publication requires the same frozen plan and progress")
    if not progress.ready_to_publish:
        raise AccessControlContractError("forward publication requires every exact LIVE source final revision")
    if campaign_state is None:
        campaign_state = campaign_after
    observed_campaign_revision = current_campaign_revision or campaign_revision
    if observed_campaign_revision is None and campaign_state is not None:
        observed_campaign_revision = campaign_state.get(
            "revision",
            campaign_state.get("campaign_revision", campaign_state.get("current_revision")),
        )  # type: ignore[assignment]
    if observed_campaign_revision != plan.expected_campaign_revision:
        raise AccessControlContractError(
            "campaign forward transition has stale currentness",
            failure_code=AuthorizationFailureCode.CURRENTNESS_CONFLICT,
        )
    if campaign_acknowledgement is not None:
        if campaign_acknowledgement.get("accepted") is not True:
            raise AccessControlContractError("campaign forward transition was not accepted")
        if campaign_acknowledgement.get("expected_campaign_revision") not in {
            None,
            plan.expected_campaign_revision,
        }:
            raise AccessControlContractError("campaign acknowledgement predecessor is stale")
        if campaign_acknowledgement.get("new_campaign_revision") not in {
            None,
            plan.proposed_campaign_revision,
        }:
            raise AccessControlContractError("campaign acknowledgement successor is mismatched")
    (
        _live_error,
        _live_envelope,
        _live_lifecycle,
        _live_publication_result,
        _live_publication_status,
        _live_routing,
        build_live_route,
        _classify_cas_result,
        _freeze_live_attempt,
        _mark_closed_unabsorbed,
        _reconcile_indeterminate,
        _select_live_source,
        _validate_live_route_completeness,
    ) = _live_modules()
    final_by_key = {
        source.source_key: source for source in progress.final_sources
    }
    successor_entries = tuple(
        final_by_key[source.source_key]
        for source in plan.sources
        if source.source_key in final_by_key
    )
    if len(successor_entries) != len(plan.sources):
        raise AccessControlContractError("forward publication lacks a final source for every selected LIVE scope")
    successor_route = build_live_route(plan.campaign_id, successor_entries)
    result_state = (
        _mapping_copy(campaign_state, "campaign state")
        if campaign_state is not None
        else {"campaign_id": plan.campaign_id}
    )
    if result_state.get("campaign_id", plan.campaign_id) != plan.campaign_id:
        raise AccessControlContractError("campaign forward publication crosses campaign scope")
    result_state["revision"] = plan.proposed_campaign_revision
    result_state["live_routing"] = successor_route.as_mapping()
    result_state["access_transition"] = "FORWARD_SOURCE_FREEZE_COMPLETE"
    return ForwardTransitionPublication(
        campaign_state=result_state,
        route=successor_route,
        accepted_history_refs=plan.accepted_history_refs,
    )
