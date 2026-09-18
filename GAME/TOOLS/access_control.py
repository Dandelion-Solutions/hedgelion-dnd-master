"""Bounded authenticated-principal to PLAYER authorization routing.

The principal route is a derived lookup aid, not an identity or authorization
owner.  A route nominates candidate PLAYER IDs; every candidate is reloaded
from the exact current PLAYER owner before an operation can be authorized.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final, TypeAlias


AccountId: TypeAlias = str

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
        return cls(
            player_id=player_id,
            stable_account_id=stable_account_id,
            login=login,
            status=status,
            deactivated_by=raw_deactivated_by,
            mechanical_override_policy=mechanical_override_policy,
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
        if creator_login == resolved_principal.login:
            return AuthorizationDecision(authorized=True, player_id=resolution.player.player_id)
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
