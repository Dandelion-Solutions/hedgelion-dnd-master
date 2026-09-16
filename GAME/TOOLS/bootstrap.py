"""Typed pre-materialization campaign selection and identity contracts.

This module intentionally prepares no scaffold bytes and performs no repository
mutation.  Wave 05 owns generator invocation, publication and installation.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Literal


_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CAMPAIGN_BRANCH_RE = re.compile(r"^campaign/\d{8}(?:-(?:0[2-9]|[1-9]\d+))?$")

SelectionKind = Literal["existing", "new"]
CreatorAuthority = Literal["creator", "read_only"]


class BootstrapContractError(ValueError):
    """Raised when a bounded bootstrap input cannot establish trusted identity."""


@dataclass(frozen=True, slots=True)
class CampaignSelection:
    """An explicit current-chat choice; discovery candidates never populate it."""

    kind: SelectionKind
    campaign_id: str | None

    def __post_init__(self) -> None:
        if self.kind not in {"existing", "new"}:
            raise BootstrapContractError("campaign selection kind is not admitted")
        if self.kind == "existing" and not self.campaign_id:
            raise BootstrapContractError("existing campaign selection requires a campaign_id")
        if self.kind == "new" and self.campaign_id is not None:
            raise BootstrapContractError("new campaign selection cannot carry a campaign_id")

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


def require_campaign_selection(selection: CampaignSelection | None) -> CampaignSelection:
    """Reject absent/ambiguous selection rather than infer a campaign from discovery."""

    if selection is None:
        raise BootstrapContractError("explicit campaign selection is required")
    return selection


def authorize_creator(*, creator_login: str | None, current_principal: CreatorIdentity) -> CreatorAuthority:
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
        raise BootstrapContractError("pinned storage HEAD must be a lowercase 40-character SHA")
    if mode not in {"singleplayer", "multiplayer"}:
        raise BootstrapContractError("mode is not admitted")
    if not _CAMPAIGN_BRANCH_RE.fullmatch(campaign_branch):
        raise BootstrapContractError("campaign branch must be a neutral campaign/YYYYMMDD[-NN] branch")
    try:
        created_at_value = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BootstrapContractError("created_at must be an ISO-8601 timestamp") from exc
    if "T" not in created_at or created_at_value.tzinfo is None:
        raise BootstrapContractError("created_at must be a timezone-qualified ISO-8601 timestamp")
    if not engine_version or not package_id:
        raise BootstrapContractError("exact engine version and package ID are required")
    if source_commit_sha is not None and not _SHA1_RE.fullmatch(source_commit_sha):
        raise BootstrapContractError("source commit SHA must be null or a lowercase 40-character SHA")
    if not _SHA256_RE.fullmatch(package_sha256):
        raise BootstrapContractError("package SHA-256 must be a lowercase 64-character SHA")
    if not _SHA256_RE.fullmatch(ruleset_set_sha256):
        raise BootstrapContractError("ruleset-set SHA-256 must be a lowercase 64-character SHA")
    if ruleset_set_digest_generation != 1:
        raise BootstrapContractError("ruleset-set digest generation must be 1")
