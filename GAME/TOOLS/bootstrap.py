"""Typed pre-materialization campaign selection and identity contracts.

This module intentionally prepares no scaffold bytes and performs no repository
mutation.  Wave 05 owns generator invocation, publication and installation.
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Literal, Protocol, cast

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CAMPAIGN_BRANCH_RE = re.compile(r"^campaign/\d{8}(?:-(?:0[2-9]|[1-9]\d+))?$")
MAX_CAMPAIGN_REFS_PER_PAGE: int = 20

SelectionKind = Literal["existing", "new"]
CreatorAuthority = Literal["creator", "read_only"]
CampaignMode = Literal["singleplayer", "multiplayer"]
CampaignStatus = Literal["initializing", "active", "paused", "completed", "archived"]
CampaignProjectionSource = Literal["card", "manifest"]
CampaignDiscoveryInabilityReason = Literal[
    "provider_limited",
    "continuation_unavailable",
    "continuation_did_not_advance",
    "page_limit_exceeded",
    "duplicate_campaign_ref",
    "ambiguous_campaign_id",
    "invalid_campaign_metadata",
    "exact_campaign_not_found",
    "selector_mismatch",
    "invalid_provider_page",
]

_DISCOVERY_INABILITY_REASONS = frozenset(
    {
        "provider_limited",
        "continuation_unavailable",
        "continuation_did_not_advance",
        "page_limit_exceeded",
        "duplicate_campaign_ref",
        "ambiguous_campaign_id",
        "invalid_campaign_metadata",
        "exact_campaign_not_found",
        "selector_mismatch",
        "invalid_provider_page",
    }
)


class BootstrapContractError(ValueError):
    """Raised when a bounded bootstrap input cannot establish trusted identity."""


@dataclass(frozen=True, slots=True)
class CampaignRef:
    """Exact campaign ref supplied by the repository transport."""

    branch: str

    def __post_init__(self) -> None:
        if not isinstance(self.branch, str) or not _CAMPAIGN_BRANCH_RE.fullmatch(
            self.branch
        ):
            raise BootstrapContractError(
                "campaign ref must be a campaign/YYYYMMDD[-NN] branch"
            )


@dataclass(frozen=True, slots=True)
class CampaignDiscoveryInability:
    """Typed reason a finite candidate page cannot be completed or routed."""

    reason: CampaignDiscoveryInabilityReason

    def __post_init__(self) -> None:
        if (
            not isinstance(self.reason, str)
            or self.reason not in _DISCOVERY_INABILITY_REASONS
        ):
            raise BootstrapContractError(
                "campaign discovery inability reason is not admitted"
            )


@dataclass(frozen=True, slots=True)
class CampaignRefPage:
    """One provider-bounded ref page; continuation is returned, never auto-drained."""

    references: tuple[CampaignRef, ...]
    more_available: bool
    continuation: str | None = None
    inability: CampaignDiscoveryInability | None = None


@dataclass(frozen=True, slots=True)
class CampaignMenuProjection:
    """Non-authoritative fields sufficient to present one campaign menu row."""

    campaign_id: str
    campaign_name: str | None
    mode: CampaignMode
    status: CampaignStatus
    engine_version: str | None
    current_location: str | None
    creator_github_login: str | None
    join_policy: Literal["invite_only", "open_contributors"] | None
    participant_github_logins: tuple[str, ...]
    source: CampaignProjectionSource


@dataclass(frozen=True, slots=True)
class CampaignCandidate:
    """A branch plus display projection; it grants no selection or access authority."""

    branch: str
    projection: CampaignMenuProjection


@dataclass(frozen=True, slots=True)
class CampaignDiscoveryPage:
    """At most one finite page of menu candidates and its explicit next action."""

    candidates: tuple[CampaignCandidate, ...]
    continuation: str | None
    inability: CampaignDiscoveryInability | None = None


class CampaignDiscoveryProvider(Protocol):
    """Minimum provider operations required by bounded campaign discovery."""

    def list_campaign_refs(
        self, *, continuation: str | None, limit: int
    ) -> CampaignRefPage: ...

    def read_campaign_file(
        self, *, ref: CampaignRef, path: Literal["CAMPAIGN_CARD.yaml", "MANIFEST.yaml"]
    ) -> Mapping[str, object] | None: ...


class _ExactCampaignRefResolver(Protocol):
    """Optional direct-routing capability for an explicit campaign ID."""

    def resolve_campaign_ref(self, *, campaign_id: str) -> CampaignRef | None: ...


@dataclass(frozen=True, slots=True)
class CampaignSelection:
    """An explicit current-chat choice; discovery candidates never populate it."""

    kind: SelectionKind
    campaign_id: str | None

    def __post_init__(self) -> None:
        if self.kind not in {"existing", "new"}:
            raise BootstrapContractError("campaign selection kind is not admitted")
        if self.kind == "existing" and not self.campaign_id:
            raise BootstrapContractError(
                "existing campaign selection requires a campaign_id"
            )
        if self.kind == "new" and self.campaign_id is not None:
            raise BootstrapContractError(
                "new campaign selection cannot carry a campaign_id"
            )

    @classmethod
    def existing(cls, campaign_id: str) -> CampaignSelection:
        return cls(kind="existing", campaign_id=campaign_id)

    @classmethod
    def new(cls) -> CampaignSelection:
        return cls(kind="new", campaign_id=None)

    def as_dict(self) -> dict[str, str | None]:
        return {"kind": self.kind, "campaign_id": self.campaign_id}


@dataclass(frozen=True, slots=True)
class CreatorIdentity:
    """Current trustworthy principal evidence with durable and display identities apart."""

    stable_github_user_id: str
    login: str

    def __post_init__(self) -> None:
        if not self.stable_github_user_id:
            raise BootstrapContractError("stable GitHub user ID is required")
        if not self.login:
            raise BootstrapContractError("current GitHub login is required")


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    """Frozen identity envelope produced after an explicit New Game selection."""

    selection: CampaignSelection
    storage_repository: str
    pinned_storage_head: str
    creator: CreatorIdentity
    mode: Literal["singleplayer", "multiplayer"]
    campaign_id: str
    campaign_branch: str
    created_at: str
    engine_version: str
    package_id: str
    source_commit_sha: str | None
    package_sha256: str
    ruleset_set_sha256: str
    ruleset_set_digest_generation: int

    def as_dict(self) -> dict[str, object]:
        return {
            "selection": self.selection.as_dict(),
            "storage_repository": self.storage_repository,
            "pinned_storage_head": self.pinned_storage_head,
            "creator": asdict(self.creator),
            "mode": self.mode,
            "campaign_id": self.campaign_id,
            "campaign_branch": self.campaign_branch,
            "created_at": self.created_at,
            "engine_version": self.engine_version,
            "package_id": self.package_id,
            "source_commit_sha": self.source_commit_sha,
            "package_sha256": self.package_sha256,
            "ruleset_set_sha256": self.ruleset_set_sha256,
            "ruleset_set_digest_generation": self.ruleset_set_digest_generation,
        }


def require_campaign_selection(
    selection: CampaignSelection | None,
) -> CampaignSelection:
    """Reject absent/ambiguous selection rather than infer a campaign from discovery."""

    if selection is None:
        raise BootstrapContractError("explicit campaign selection is required")
    return selection


def discover_campaign_page(
    provider: CampaignDiscoveryProvider,
    *,
    continuation: str | None = None,
    selection: CampaignSelection | None = None,
) -> CampaignDiscoveryPage:
    """Produce one bounded display page or directly route an explicit existing selection.

    Candidate cards and minimal manifest fallback fields are menu projections only.
    The returned page never manufactures or changes a CampaignSelection.
    """

    if selection is not None:
        selected = require_campaign_selection(selection)
        if selected.kind != "existing":
            raise BootstrapContractError(
                "campaign discovery direct routing requires an existing selection"
            )
        campaign_id = selected.campaign_id
        if campaign_id is None:
            raise BootstrapContractError(
                "existing campaign selection requires a campaign_id"
            )
        if not callable(getattr(provider, "resolve_campaign_ref", None)):
            return CampaignDiscoveryPage(
                candidates=(),
                continuation=None,
                inability=CampaignDiscoveryInability(reason="provider_limited"),
            )
        resolver = cast(_ExactCampaignRefResolver, provider)
        ref = resolver.resolve_campaign_ref(campaign_id=campaign_id)
        if ref is None:
            return CampaignDiscoveryPage(
                candidates=(),
                continuation=None,
                inability=CampaignDiscoveryInability(reason="exact_campaign_not_found"),
            )
        if not isinstance(ref, CampaignRef):
            return CampaignDiscoveryPage(
                candidates=(),
                continuation=None,
                inability=CampaignDiscoveryInability(reason="invalid_provider_page"),
            )
        return _hydrate_campaign_refs(
            provider,
            (ref,),
            more_available=False,
            continuation=None,
            requested_continuation=None,
            expected_campaign_id=campaign_id,
        )

    provider_page = provider.list_campaign_refs(
        continuation=continuation,
        limit=MAX_CAMPAIGN_REFS_PER_PAGE,
    )
    if not isinstance(provider_page, CampaignRefPage):
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="invalid_provider_page"),
        )
    if provider_page.inability is not None:
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=provider_page.inability,
        )
    if (
        not isinstance(provider_page.references, tuple)
        or type(provider_page.more_available) is not bool
        or (
            provider_page.continuation is not None
            and not isinstance(provider_page.continuation, str)
        )
        or any(not isinstance(ref, CampaignRef) for ref in provider_page.references)
    ):
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="invalid_provider_page"),
        )
    if len(provider_page.references) > MAX_CAMPAIGN_REFS_PER_PAGE:
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="page_limit_exceeded"),
        )
    if not provider_page.more_available and provider_page.continuation is not None:
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="invalid_provider_page"),
        )
    return _hydrate_campaign_refs(
        provider,
        provider_page.references,
        more_available=provider_page.more_available,
        continuation=provider_page.continuation,
        requested_continuation=continuation,
        expected_campaign_id=None,
    )


def _hydrate_campaign_refs(
    provider: CampaignDiscoveryProvider,
    refs: tuple[CampaignRef, ...],
    *,
    more_available: bool,
    continuation: str | None,
    requested_continuation: str | None,
    expected_campaign_id: str | None,
) -> CampaignDiscoveryPage:
    branches = tuple(ref.branch for ref in refs)
    if len(set(branches)) != len(branches):
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="duplicate_campaign_ref"),
        )
    if more_available and not continuation:
        inability = CampaignDiscoveryInability(reason="continuation_unavailable")
    elif more_available and continuation == requested_continuation:
        return CampaignDiscoveryPage(
            candidates=(),
            continuation=None,
            inability=CampaignDiscoveryInability(reason="continuation_did_not_advance"),
        )
    else:
        inability = None

    candidates: list[CampaignCandidate] = []
    seen_campaign_ids: set[str] = set()
    for ref in refs:
        projection = _read_campaign_menu_projection(provider, ref)
        if projection is None:
            return CampaignDiscoveryPage(
                candidates=tuple(candidates),
                continuation=continuation if more_available else None,
                inability=CampaignDiscoveryInability(
                    reason="invalid_campaign_metadata"
                ),
            )
        if (
            expected_campaign_id is not None
            and projection.campaign_id != expected_campaign_id
        ):
            return CampaignDiscoveryPage(
                candidates=(),
                continuation=None,
                inability=CampaignDiscoveryInability(reason="selector_mismatch"),
            )
        if projection.campaign_id in seen_campaign_ids:
            return CampaignDiscoveryPage(
                candidates=(),
                continuation=None,
                inability=CampaignDiscoveryInability(reason="ambiguous_campaign_id"),
            )
        seen_campaign_ids.add(projection.campaign_id)
        candidates.append(CampaignCandidate(branch=ref.branch, projection=projection))

    return CampaignDiscoveryPage(
        candidates=tuple(candidates),
        continuation=continuation if more_available else None,
        inability=inability,
    )


def _read_campaign_menu_projection(
    provider: CampaignDiscoveryProvider, ref: CampaignRef
) -> CampaignMenuProjection | None:
    card = provider.read_campaign_file(ref=ref, path="CAMPAIGN_CARD.yaml")
    projection = _campaign_card_projection(card)
    if projection is not None:
        return projection
    manifest = provider.read_campaign_file(ref=ref, path="MANIFEST.yaml")
    return _minimal_manifest_projection(ref, manifest)


def _campaign_card_projection(
    value: Mapping[str, object] | None,
) -> CampaignMenuProjection | None:
    if not isinstance(value, Mapping):
        return None
    campaign_id = value.get("campaign_id")
    mode = _campaign_mode(value.get("mode"))
    status = _campaign_status(value.get("status"))
    engine_version = value.get("engine_version")
    if (
        type(value.get("schema_version")) is not int
        or value.get("schema_version") != 1
        or not isinstance(campaign_id, str)
        or not campaign_id
        or mode is None
        or status is None
        or not isinstance(engine_version, str)
    ):
        return None
    for field in (
        "campaign_name",
        "status_note",
        "current_location",
        "creator_github_login",
    ):
        if field in value and not _optional_text(value[field]):
            return None

    join_policy: Literal["invite_only", "open_contributors"] | None = None
    participant_logins: tuple[str, ...] = ()
    protagonist = value.get("protagonist")
    multiplayer = value.get("multiplayer")
    if mode == "singleplayer":
        if not isinstance(protagonist, Mapping) or multiplayer is not None:
            return None
        if any(
            field in protagonist and not _optional_text(protagonist[field])
            for field in ("name", "role_race")
        ):
            return None
    else:
        if protagonist is not None or not isinstance(multiplayer, Mapping):
            return None
        join_policy = _join_policy(multiplayer.get("join_policy"))
        raw_logins = multiplayer.get("participant_github_logins")
        if join_policy is None or not isinstance(raw_logins, list):
            return None
        if any(not isinstance(login, str) for login in raw_logins):
            return None
        participant_logins = tuple(raw_logins)

    return CampaignMenuProjection(
        campaign_id=campaign_id,
        campaign_name=_text_or_none(value.get("campaign_name")),
        mode=mode,
        status=status,
        engine_version=engine_version,
        current_location=_text_or_none(value.get("current_location")),
        creator_github_login=_text_or_none(value.get("creator_github_login")),
        join_policy=join_policy,
        participant_github_logins=participant_logins,
        source="card",
    )


def _minimal_manifest_projection(
    ref: CampaignRef, value: Mapping[str, object] | None
) -> CampaignMenuProjection | None:
    if not isinstance(value, Mapping):
        return None
    campaign_id = value.get("campaign_id")
    mode = _campaign_mode(value.get("mode"))
    status = _campaign_status(value.get("status"))
    campaign_name = value.get("campaign_name")
    if (
        type(value.get("schema_version")) is not int
        or value.get("schema_version") != 4
        or value.get("branch") != ref.branch
        or not isinstance(campaign_id, str)
        or not campaign_id
        or mode is None
        or status is None
        or not _optional_text(campaign_name)
    ):
        return None
    join_policy: Literal["invite_only", "open_contributors"] | None = None
    players = value.get("players")
    if isinstance(players, Mapping):
        join_policy = _join_policy(players.get("join_policy"))
    return CampaignMenuProjection(
        campaign_id=campaign_id,
        campaign_name=_text_or_none(campaign_name),
        mode=mode,
        status=status,
        engine_version=None,
        current_location=None,
        creator_github_login=None,
        join_policy=join_policy,
        participant_github_logins=(),
        source="manifest",
    )


def _optional_text(value: object) -> bool:
    return value is None or isinstance(value, str)


def _campaign_mode(value: object) -> CampaignMode | None:
    if value == "singleplayer":
        return "singleplayer"
    if value == "multiplayer":
        return "multiplayer"
    return None


def _campaign_status(value: object) -> CampaignStatus | None:
    if value == "initializing":
        return "initializing"
    if value == "active":
        return "active"
    if value == "paused":
        return "paused"
    if value == "completed":
        return "completed"
    if value == "archived":
        return "archived"
    return None


def _join_policy(value: object) -> Literal["invite_only", "open_contributors"] | None:
    if value == "invite_only":
        return "invite_only"
    if value == "open_contributors":
        return "open_contributors"
    return None


def _text_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


def authorize_creator(
    *, creator_login: str | None, current_principal: CreatorIdentity
) -> CreatorAuthority:
    """Resolve creator-only authority from immutable creator-login provenance alone."""

    if creator_login is not None and creator_login == current_principal.login:
        return "creator"
    return "read_only"


def create_bootstrap_result(
    *,
    selection: CampaignSelection,
    storage_repository: str,
    pinned_storage_head: str,
    creator: CreatorIdentity,
    mode: Literal["singleplayer", "multiplayer"],
    campaign_branch: str,
    created_at: str,
    engine_version: str,
    package_id: str,
    source_commit_sha: str | None,
    package_sha256: str,
    ruleset_set_sha256: str,
    ruleset_set_digest_generation: int,
) -> BootstrapResult:
    """Freeze creation identity before a generator or dependent campaign root can exist."""

    require_campaign_selection(selection)
    if selection.kind != "new":
        raise BootstrapContractError("creation requires an explicit New Game selection")
    _validate_creation_input(
        storage_repository=storage_repository,
        pinned_storage_head=pinned_storage_head,
        mode=mode,
        campaign_branch=campaign_branch,
        created_at=created_at,
        engine_version=engine_version,
        package_id=package_id,
        source_commit_sha=source_commit_sha,
        package_sha256=package_sha256,
        ruleset_set_sha256=ruleset_set_sha256,
        ruleset_set_digest_generation=ruleset_set_digest_generation,
    )
    return BootstrapResult(
        selection=selection,
        storage_repository=storage_repository,
        pinned_storage_head=pinned_storage_head,
        creator=creator,
        mode=mode,
        campaign_id=f"campaign.{uuid.uuid4().hex}",
        campaign_branch=campaign_branch,
        created_at=created_at,
        engine_version=engine_version,
        package_id=package_id,
        source_commit_sha=source_commit_sha,
        package_sha256=package_sha256.lower(),
        ruleset_set_sha256=ruleset_set_sha256.lower(),
        ruleset_set_digest_generation=ruleset_set_digest_generation,
    )


def build_scaffold_input(result: BootstrapResult) -> dict[str, object]:
    """Return the complete bounded input contract for the later scaffold generator."""

    return {
        "campaign_id": result.campaign_id,
        "campaign_branch": result.campaign_branch,
        "created_at": result.created_at,
        "creator_github_login": result.creator.login,
        "mode": result.mode,
        "engine_version": result.engine_version,
        "package_id": result.package_id,
        "source_commit_sha": result.source_commit_sha,
        "package_sha256": result.package_sha256,
        "ruleset_set_sha256": result.ruleset_set_sha256,
        "ruleset_set_digest_generation": result.ruleset_set_digest_generation,
    }


def _validate_creation_input(
    *,
    storage_repository: str,
    pinned_storage_head: str,
    mode: str,
    campaign_branch: str,
    created_at: str,
    engine_version: str,
    package_id: str,
    source_commit_sha: str | None,
    package_sha256: str,
    ruleset_set_sha256: str,
    ruleset_set_digest_generation: int,
) -> None:
    if not storage_repository:
        raise BootstrapContractError("storage repository identity is required")
    if not _SHA1_RE.fullmatch(pinned_storage_head):
        raise BootstrapContractError(
            "pinned storage HEAD must be a lowercase 40-character SHA"
        )
    if mode not in {"singleplayer", "multiplayer"}:
        raise BootstrapContractError("mode is not admitted")
    if not _CAMPAIGN_BRANCH_RE.fullmatch(campaign_branch):
        raise BootstrapContractError(
            "campaign branch must be a neutral campaign/YYYYMMDD[-NN] branch"
        )
    try:
        created_at_value = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BootstrapContractError(
            "created_at must be an ISO-8601 timestamp"
        ) from exc
    if "T" not in created_at or created_at_value.tzinfo is None:
        raise BootstrapContractError(
            "created_at must be a timezone-qualified ISO-8601 timestamp"
        )
    if not engine_version or not package_id:
        raise BootstrapContractError("exact engine version and package ID are required")
    if source_commit_sha is not None and not _SHA1_RE.fullmatch(source_commit_sha):
        raise BootstrapContractError(
            "source commit SHA must be null or a lowercase 40-character SHA"
        )
    if not _SHA256_RE.fullmatch(package_sha256):
        raise BootstrapContractError(
            "package SHA-256 must be a lowercase 64-character SHA"
        )
    if not _SHA256_RE.fullmatch(ruleset_set_sha256):
        raise BootstrapContractError(
            "ruleset-set SHA-256 must be a lowercase 64-character SHA"
        )
    if (
        type(ruleset_set_digest_generation) is not int
        or ruleset_set_digest_generation != 1
    ):
        raise BootstrapContractError("ruleset-set digest generation must be 1")
