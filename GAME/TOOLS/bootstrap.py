"""Typed campaign selection, identity and initial-publication contracts.

Initial publication remains a bootstrap-specific operation over the same
authenticated deployment adapter used for bounded campaign discovery.
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Mapping
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, Literal, Protocol, cast

from .durability import DurabilityPromiseResult, RoutedSerializedOperation
from .policy_basis import AuthenticatedPrincipalEvidence
from .publication import PublicationOutcome, PublicationStatus

if TYPE_CHECKING:
    from .access_control import PrincipalPlayerRoute, VerifiedPrincipal
    from .collaboration import CollaborationCatchUp
    from .hot_store import HotOwnerStorePort
    from .policy_basis import RepositoryPort
    from .runtime_host import (
        CampaignPublicationTransport,
        RuntimeHost,
        SelectedLiveTransport,
    )

# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.5"

_SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CAMPAIGN_ID_RE = re.compile(r"^campaign\.[0-9a-f]{32}$")
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


@dataclass(frozen=True, slots=True)
class InitialCampaignRefState:
    """Exact target campaign ref state at one bounded read point."""

    status: Literal["ABSENT", "PRESENT"]
    head_sha: str | None = None

    def __post_init__(self) -> None:
        if self.status == "ABSENT":
            if self.head_sha is not None:
                raise BootstrapContractError("absent campaign ref cannot carry a HEAD")
            return
        if self.status == "PRESENT":
            if not isinstance(self.head_sha, str) or not _SHA1_RE.fullmatch(
                self.head_sha
            ):
                raise BootstrapContractError(
                    "present campaign ref requires an exact lowercase HEAD"
                )
            return
        raise BootstrapContractError("initial campaign ref status is not admitted")

    @classmethod
    def absent(cls) -> InitialCampaignRefState:
        return cls(status="ABSENT")

    @classmethod
    def present(cls, head_sha: str) -> InitialCampaignRefState:
        return cls(status="PRESENT", head_sha=head_sha)


class BootstrapPublicationCapability(Protocol):
    """Narrow pre-campaign publication view on the discovery deployment adapter."""

    def repository_identity(self) -> str:
        """Return the exact repository identity bound to this adapter."""

    def resolve_authenticated_storage_principal(
        self, storage_repository: str, pinned_storage_head: str
    ) -> AuthenticatedPrincipalEvidence:
        """Resolve the authenticated principal for this exact storage basis."""

    def read_ref_state(self, target_campaign_ref: str) -> InitialCampaignRefState:
        """Return exact ABSENT/PRESENT evidence for one target ref."""

    def create_tree_from_scratch(
        self, exact_generated_files: Mapping[str, bytes]
    ) -> object:
        """Create one tree from exactly these files, with no base tree."""

    def create_single_parent_commit(
        self, parent_sha: str, tree_sha: str, target_ref: str
    ) -> object:
        """Create one initialization commit with exactly the supplied parent."""

    def create_ref_if_absent(
        self, target_campaign_ref: str, exact_commit_sha: str
    ) -> PublicationOutcome:
        """Atomically create only an absent ref and return a W02 outcome."""

    def read_exact_commit(
        self, target_campaign_ref: str, exact_commit_sha: str
    ) -> Mapping[str, object]:
        """Return exact revision/tree/parents and the complete path-to-bytes map."""


class BootstrapDeploymentProvider(
    CampaignDiscoveryProvider, BootstrapPublicationCapability, Protocol
):
    """One authenticated deployment adapter for discovery and initial creation."""


@dataclass(frozen=True, slots=True)
class InitialCampaignPublicationResult:
    """W02-compatible initial-publication outcome plus its frozen retry identity."""

    attempt: FrozenInitialCampaignPublication
    outcome: PublicationOutcome


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


@dataclass(frozen=True, slots=True)
class FrozenInitialCampaignPublication:
    """One immutable bootstrap identity plus its exact generated file map."""

    bootstrap_result: BootstrapResult
    generated_files: Mapping[str, bytes]
    generated_files_fingerprint: tuple[tuple[str, bytes], ...] = ()
    tree_sha: str | None = None
    initialization_commit_sha: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.bootstrap_result, BootstrapResult):
            raise BootstrapContractError("frozen bootstrap result is required")
        result = self.bootstrap_result
        if (
            not isinstance(result.selection, CampaignSelection)
            or result.selection.kind != "new"
        ):
            raise BootstrapContractError(
                "initial publication requires the frozen New Game identity"
            )
        if not isinstance(result.creator, CreatorIdentity):
            raise BootstrapContractError("frozen creator identity is required")
        if not isinstance(result.campaign_id, str) or not _CAMPAIGN_ID_RE.fullmatch(
            result.campaign_id
        ):
            raise BootstrapContractError("frozen campaign ID is not canonical")
        _validate_creation_input(
            storage_repository=result.storage_repository,
            pinned_storage_head=result.pinned_storage_head,
            mode=result.mode,
            campaign_branch=result.campaign_branch,
            created_at=result.created_at,
            engine_version=result.engine_version,
            package_id=result.package_id,
            source_commit_sha=result.source_commit_sha,
            package_sha256=result.package_sha256,
            ruleset_set_sha256=result.ruleset_set_sha256,
            ruleset_set_digest_generation=result.ruleset_set_digest_generation,
        )
        if not isinstance(self.generated_files, Mapping) or not self.generated_files:
            raise BootstrapContractError(
                "initial publication requires a complete generated file map"
            )

        files: dict[str, bytes] = {}
        for raw_path, content in self.generated_files.items():
            if (
                not isinstance(raw_path, str)
                or not raw_path
                or raw_path.startswith("/")
                or "\\" in raw_path
                or "\x00" in raw_path
                or any(part in {"", ".", ".."} for part in raw_path.split("/"))
            ):
                raise BootstrapContractError(
                    "generated campaign file path must be normalized"
                )
            # README.md is valid campaign scaffold content. Because publication
            # builds only this exact map from scratch, no storage-root README is
            # inherited; explicit storage markers remain forbidden.
            if raw_path in {"DND_STORAGE.yaml", "DND_STORAGE"} or raw_path.startswith(
                "DND_STORAGE/"
            ):
                raise BootstrapContractError(
                    "generated campaign tree cannot include storage-root files"
                )
            if not isinstance(content, bytes):
                raise BootstrapContractError(
                    "generated campaign file content must be exact bytes"
                )
            files[raw_path] = content

        fingerprint = tuple(sorted(files.items()))
        if self.generated_files_fingerprint not in ((), fingerprint):
            raise BootstrapContractError(
                "generated campaign file fingerprint differs from its exact files"
            )
        if self.tree_sha is not None and (
            not isinstance(self.tree_sha, str) or not _SHA1_RE.fullmatch(self.tree_sha)
        ):
            raise BootstrapContractError("prepared campaign tree must be an exact SHA")
        if self.initialization_commit_sha is not None and (
            not isinstance(self.initialization_commit_sha, str)
            or not _SHA1_RE.fullmatch(self.initialization_commit_sha)
        ):
            raise BootstrapContractError("initialization commit must be an exact SHA")
        if (self.tree_sha is None) != (self.initialization_commit_sha is None):
            raise BootstrapContractError(
                "prepared tree and initialization commit must be frozen together"
            )
        object.__setattr__(self, "generated_files", MappingProxyType(files))
        object.__setattr__(self, "generated_files_fingerprint", fingerprint)


def freeze_initial_campaign_publication(
    bootstrap_result: BootstrapResult,
    generated_files: Mapping[str, bytes],
) -> FrozenInitialCampaignPublication:
    """Freeze one New Game identity and the exact complete generated file map."""

    return FrozenInitialCampaignPublication(
        bootstrap_result=bootstrap_result,
        generated_files=generated_files,
    )


def publish_initial_campaign(
    deployment: BootstrapDeploymentProvider,
    attempt: FrozenInitialCampaignPublication,
) -> InitialCampaignPublicationResult:
    """Publish one from-scratch initialization through a create-if-absent ref."""

    if not isinstance(attempt, FrozenInitialCampaignPublication):
        raise BootstrapContractError("frozen initial campaign attempt is required")
    if not _has_initial_publication_capability(deployment):
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="INITIAL_PUBLICATION_CAPABILITY_UNAVAILABLE",
        )

    identity = attempt.bootstrap_result
    try:
        repository_identity = deployment.repository_identity()
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="STORAGE_REPOSITORY_IDENTITY_UNAVAILABLE",
        )
    if (
        not isinstance(repository_identity, str)
        or repository_identity != identity.storage_repository
    ):
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="STORAGE_REPOSITORY_IDENTITY_MISMATCH",
        )

    try:
        principal = deployment.resolve_authenticated_storage_principal(
            identity.storage_repository, identity.pinned_storage_head
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="AUTHENTICATED_STORAGE_PRINCIPAL_UNAVAILABLE",
        )
    if (
        not isinstance(principal, AuthenticatedPrincipalEvidence)
        or principal.principal_id != identity.creator.stable_github_user_id
    ):
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="AUTHENTICATED_STORAGE_PRINCIPAL_MISMATCH",
        )

    try:
        ref_state = deployment.read_ref_state(identity.campaign_branch)
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="INITIAL_TARGET_REF_EVIDENCE_UNAVAILABLE",
        )
    if not isinstance(ref_state, InitialCampaignRefState):
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="INITIAL_TARGET_REF_EVIDENCE_INVALID",
        )
    if ref_state.status == "PRESENT":
        return _adopt_existing_initial_campaign(deployment, attempt, ref_state)

    resuming_prepared_commit = attempt.initialization_commit_sha is not None
    tree_sha = attempt.tree_sha
    if tree_sha is None:
        try:
            tree_sha = _initial_revision(
                deployment.create_tree_from_scratch(attempt.generated_files),
                "created campaign tree",
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError):
            return _initial_publication_result(
                attempt,
                PublicationStatus.REJECTED,
                cause="INITIAL_TREE_PREPARATION_FAILED",
            )

    commit_sha = attempt.initialization_commit_sha
    if commit_sha is None:
        try:
            commit_sha = _initial_revision(
                deployment.create_single_parent_commit(
                    identity.pinned_storage_head,
                    tree_sha,
                    identity.campaign_branch,
                ),
                "initialization commit",
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError):
            return _initial_publication_result(
                attempt,
                PublicationStatus.REJECTED,
                cause="INITIAL_COMMIT_PREPARATION_FAILED",
            )
    if tree_sha is None or commit_sha is None:
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="INITIAL_PREPARATION_IDENTITY_UNAVAILABLE",
        )
    prepared = (
        attempt
        if resuming_prepared_commit
        else replace(
            attempt,
            tree_sha=tree_sha,
            initialization_commit_sha=commit_sha,
        )
    )

    intended_commit_sha = commit_sha
    if resuming_prepared_commit:
        evidence = _read_initial_commit_evidence(
            deployment, prepared, intended_commit_sha
        )
        matches = (
            None
            if evidence is None
            else _initial_commit_match(evidence, prepared, intended_commit_sha)
        )
        if matches is not True:
            return _initial_publication_result(
                prepared,
                PublicationStatus.CONFLICT
                if matches is False
                else PublicationStatus.REJECTED,
                cause="PREPARED_INITIALIZATION_NOT_PROVEN",
                intended_commit_sha=intended_commit_sha,
            )

    try:
        outcome = deployment.create_ref_if_absent(
            identity.campaign_branch, intended_commit_sha
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        outcome = PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended_commit_sha,
            None,
            "INITIAL_REF_CREATE_RESULT_UNAVAILABLE",
            True,
        )

    classified = _initial_ref_outcome(outcome, intended_commit_sha)
    if classified.status is PublicationStatus.INDETERMINATE:
        return _reconcile_initial_publication(deployment, prepared, intended_commit_sha)
    return InitialCampaignPublicationResult(prepared, classified)


def _has_initial_publication_capability(value: object) -> bool:
    required = (
        "list_campaign_refs",
        "read_campaign_file",
        "repository_identity",
        "resolve_authenticated_storage_principal",
        "read_ref_state",
        "create_tree_from_scratch",
        "create_single_parent_commit",
        "create_ref_if_absent",
        "read_exact_commit",
    )
    return all(callable(getattr(value, name, None)) for name in required)


def _initial_revision(value: object, label: str) -> str:
    if isinstance(value, Mapping):
        value = value.get("sha", value.get("tree_sha", value.get("commit_sha")))
    if not isinstance(value, str) or not _SHA1_RE.fullmatch(value):
        raise BootstrapContractError(f"{label} must be an exact lowercase SHA")
    return value


def _initial_publication_result(
    attempt: FrozenInitialCampaignPublication,
    status: PublicationStatus,
    *,
    cause: str,
    intended_commit_sha: str | None = None,
    observed_head_sha: str | None = None,
    dispatched: bool = False,
) -> InitialCampaignPublicationResult:
    return InitialCampaignPublicationResult(
        attempt,
        PublicationOutcome(
            status,
            intended_commit_sha,
            observed_head_sha,
            cause,
            dispatched,
        ),
    )


def _initial_ref_outcome(value: object, intended_commit_sha: str) -> PublicationOutcome:
    if not isinstance(value, PublicationOutcome):
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended_commit_sha,
            None,
            "INITIAL_REF_CREATE_OUTCOME_INVALID",
            True,
        )
    if (
        not isinstance(value.status, PublicationStatus)
        or type(value.dispatched) is not bool
        or not isinstance(value.cause, str)
        or not value.cause
        or type(value.retry_with_force) is not bool
    ):
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended_commit_sha,
            None,
            "INITIAL_REF_CREATE_OUTCOME_INVALID",
            True,
        )
    if value.observed_head_sha is not None:
        try:
            _initial_revision(value.observed_head_sha, "observed campaign HEAD")
        except BootstrapContractError:
            return PublicationOutcome(
                PublicationStatus.INDETERMINATE,
                intended_commit_sha,
                None,
                "INITIAL_REF_CREATE_OUTCOME_INVALID",
                value.dispatched,
            )
    if value.intended_commit_sha != intended_commit_sha:
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended_commit_sha,
            value.observed_head_sha,
            "INITIAL_REF_CREATE_OUTCOME_MISMATCH",
            value.dispatched,
        )
    if value.retry_with_force:
        return PublicationOutcome(
            PublicationStatus.CONFLICT,
            intended_commit_sha,
            value.observed_head_sha,
            "FORCE_RETRY_FORBIDDEN",
            value.dispatched,
            retry_with_force=False,
        )
    if value.status is PublicationStatus.ACCEPTED and (
        value.dispatched is not True or value.observed_head_sha != intended_commit_sha
    ):
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended_commit_sha,
            value.observed_head_sha,
            "INITIAL_REF_ACCEPTANCE_EVIDENCE_INCOMPLETE",
            value.dispatched,
        )
    return value


def _read_initial_commit_evidence(
    deployment: BootstrapPublicationCapability,
    attempt: FrozenInitialCampaignPublication,
    commit_sha: str,
) -> Mapping[str, object] | None:
    try:
        evidence = deployment.read_exact_commit(
            attempt.bootstrap_result.campaign_branch, commit_sha
        )
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return None
    return evidence if isinstance(evidence, Mapping) else None


def _initial_commit_match(
    evidence: Mapping[str, object],
    attempt: FrozenInitialCampaignPublication,
    commit_sha: str,
) -> bool | None:
    """Return exact match, contradiction, or insufficient read evidence."""

    if evidence.get("revision") != commit_sha:
        return None
    tree_sha = evidence.get("tree_sha")
    if not isinstance(tree_sha, str) or not _SHA1_RE.fullmatch(tree_sha):
        return None
    if attempt.tree_sha is not None and tree_sha != attempt.tree_sha:
        return False
    parents = evidence.get("parents")
    if not isinstance(parents, (list, tuple)):
        return None
    if len(parents) != 1:
        return False
    if parents[0] != attempt.bootstrap_result.pinned_storage_head:
        return False
    files = evidence.get("files")
    if not isinstance(files, Mapping):
        return None
    if any(
        not isinstance(path, str) or not isinstance(content, bytes)
        for path, content in files.items()
    ):
        return None
    return dict(files) == dict(attempt.generated_files)


def _adopt_existing_initial_campaign(
    deployment: BootstrapPublicationCapability,
    attempt: FrozenInitialCampaignPublication,
    ref_state: InitialCampaignRefState,
) -> InitialCampaignPublicationResult:
    head_sha = ref_state.head_sha
    if head_sha is None:
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="PRESENT_INITIAL_TARGET_HEAD_UNAVAILABLE",
        )
    if (
        attempt.initialization_commit_sha is not None
        and head_sha != attempt.initialization_commit_sha
    ):
        return _initial_publication_result(
            attempt,
            PublicationStatus.CONFLICT,
            cause="EXISTING_TARGET_IS_DIFFERENT_INITIALIZATION",
            intended_commit_sha=attempt.initialization_commit_sha,
            observed_head_sha=head_sha,
        )

    evidence = _read_initial_commit_evidence(deployment, attempt, head_sha)
    if evidence is None:
        return _initial_publication_result(
            attempt,
            PublicationStatus.CONFLICT,
            cause="EXISTING_TARGET_INITIALIZATION_NOT_PROVEN",
            intended_commit_sha=attempt.initialization_commit_sha,
            observed_head_sha=head_sha,
        )
    matches = _initial_commit_match(evidence, attempt, head_sha)
    if matches is not True:
        return _initial_publication_result(
            attempt,
            PublicationStatus.CONFLICT,
            cause="EXISTING_TARGET_INITIALIZATION_NOT_PROVEN",
            intended_commit_sha=attempt.initialization_commit_sha,
            observed_head_sha=head_sha,
        )

    tree_sha = evidence["tree_sha"]
    adopted = replace(
        attempt,
        tree_sha=tree_sha,
        initialization_commit_sha=head_sha,
    )
    return _initial_publication_result(
        adopted,
        PublicationStatus.ACCEPTED,
        cause="RECONCILED_CURRENT_CLOSURE",
        intended_commit_sha=head_sha,
        observed_head_sha=head_sha,
        dispatched=False,
    )


def _reconcile_initial_publication(
    deployment: BootstrapPublicationCapability,
    attempt: FrozenInitialCampaignPublication,
    intended_commit_sha: str,
) -> InitialCampaignPublicationResult:
    try:
        ref_state = deployment.read_ref_state(attempt.bootstrap_result.campaign_branch)
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="INITIAL_REF_RECONCILIATION_UNAVAILABLE",
            intended_commit_sha=intended_commit_sha,
            dispatched=False,
        )
    if not isinstance(ref_state, InitialCampaignRefState):
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="INITIAL_REF_RECONCILIATION_INVALID",
            intended_commit_sha=intended_commit_sha,
            dispatched=False,
        )
    if ref_state.status == "ABSENT":
        return _initial_publication_result(
            attempt,
            PublicationStatus.REJECTED,
            cause="CONFIRMED_NOT_PUBLISHED",
            intended_commit_sha=intended_commit_sha,
            dispatched=False,
        )
    head_sha = ref_state.head_sha
    if head_sha != intended_commit_sha:
        return _initial_publication_result(
            attempt,
            PublicationStatus.CONFLICT,
            cause="INITIAL_REF_POINTS_ELSEWHERE",
            intended_commit_sha=intended_commit_sha,
            observed_head_sha=head_sha,
            dispatched=False,
        )

    evidence = _read_initial_commit_evidence(deployment, attempt, head_sha)
    if evidence is None:
        return _initial_publication_result(
            attempt,
            PublicationStatus.INDETERMINATE,
            cause="INITIAL_COMMIT_RECONCILIATION_UNAVAILABLE",
            intended_commit_sha=intended_commit_sha,
            observed_head_sha=head_sha,
            dispatched=False,
        )
    matches = _initial_commit_match(evidence, attempt, head_sha)
    if matches is not True:
        return _initial_publication_result(
            attempt,
            PublicationStatus.CONFLICT
            if matches is False
            else PublicationStatus.INDETERMINATE,
            cause="INITIAL_COMMIT_RECONCILIATION_MISMATCH",
            intended_commit_sha=intended_commit_sha,
            observed_head_sha=head_sha,
            dispatched=False,
        )
    return _initial_publication_result(
        attempt,
        PublicationStatus.ACCEPTED,
        cause="RECONCILED_CURRENT_CLOSURE",
        intended_commit_sha=intended_commit_sha,
        observed_head_sha=head_sha,
        dispatched=False,
    )


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


def resolve_current_creator_authority(
    host: RuntimeHost,
    principal: Mapping[str, object] | object,
) -> CreatorAuthority:
    """Use current owner-issued first-initialization evidence; uncertainty is read-only."""

    from .access_control import authorize_operation, resolve_principal
    from .history import (
        FirstInitializationHistoryEvidence,
        HistoryObservationStatus,
    )

    current = resolve_principal(principal)
    try:
        campaign_id = host.campaign_id
        observe = host.history.observe_first_initialization_history
        if not isinstance(campaign_id, str) or not campaign_id or not callable(observe):
            return "read_only"
        observation = observe()
    except (AttributeError, KeyError, OSError, TypeError, ValueError):
        return "read_only"

    evidence = getattr(observation, "evidence", None)
    if (
        getattr(observation, "status", None) is not HistoryObservationStatus.AVAILABLE
        or not isinstance(evidence, FirstInitializationHistoryEvidence)
        or evidence.campaign_id != campaign_id
    ):
        return "read_only"
    decision = authorize_operation(
        current,
        operation="creator_only",
        creator_provenance=evidence,
        campaign_id=campaign_id,
    )
    return "creator" if decision.authorized else "read_only"


def invitation_login_for_display(login: object) -> str:
    """Retain the user-supplied invitee login as display text, never identity proof."""

    if (
        not isinstance(login, str)
        or not login
        or login != login.strip()
        or "@" in login
    ):
        raise BootstrapContractError("invitation requires a GitHub login, not an email")
    return login


def prepare_multiplayer_join(
    host: RuntimeHost,
    *,
    principal: VerifiedPrincipal | Mapping[str, object],
    player_route: PrincipalPlayerRoute | Mapping[str, object],
    cursor_hint: str | None = None,
) -> CollaborationCatchUp:
    """Route join through verified principal and Collaboration's current-owner reload."""

    from .access_control import resolve_principal
    from .collaboration import join_participant

    current_principal = resolve_principal(principal)
    return join_participant(
        host,
        principal=current_principal,
        player_route=player_route,
        cursor_hint=cursor_hint,
    )


def prepare_multiplayer_rejoin(
    host: RuntimeHost,
    *,
    principal: VerifiedPrincipal | Mapping[str, object],
    player_route: PrincipalPlayerRoute | Mapping[str, object],
    cursor_hint: str | None = None,
) -> CollaborationCatchUp:
    """Route rejoin through the same stable principal and exact current PLAYER owner."""

    from .access_control import resolve_principal
    from .collaboration import rejoin_participant

    current_principal = resolve_principal(principal)
    return rejoin_participant(
        host,
        principal=current_principal,
        player_route=player_route,
        cursor_hint=cursor_hint,
    )


def compose_selected_runtime_host(
    selection: CampaignSelection,
    authenticated_repository_port: RepositoryPort,
    selected_live_transport: SelectedLiveTransport,
    campaign_publication_transport: CampaignPublicationTransport,
    *,
    hot_owner_store: HotOwnerStorePort,
    initial_publication: InitialCampaignPublicationResult | None = None,
) -> RuntimeHost:
    """Compose one host only after an explicit existing selection or accepted creation."""

    current_selection = require_campaign_selection(selection)
    if current_selection.kind == "existing":
        if current_selection.campaign_id is None or initial_publication is not None:
            raise BootstrapContractError(
                "existing selection has inconsistent creation evidence"
            )
        campaign_id = current_selection.campaign_id
    else:
        if not isinstance(initial_publication, InitialCampaignPublicationResult):
            raise BootstrapContractError(
                "New Game requires confirmed initial campaign publication before host composition"
            )
        creation = initial_publication.attempt.bootstrap_result
        outcome = initial_publication.outcome
        if (
            creation.selection != current_selection
            or outcome.status is not PublicationStatus.ACCEPTED
            or outcome.acknowledged is not True
            or outcome.observed_head_sha != outcome.intended_commit_sha
        ):
            raise BootstrapContractError(
                "New Game host composition requires confirmed matching publication"
            )
        campaign_id = creation.campaign_id

    if campaign_publication_transport is None:
        raise BootstrapContractError(
            "selected gameplay RuntimeHost requires campaign publication capability"
        )
    if hot_owner_store is None:
        raise BootstrapContractError(
            "selected gameplay RuntimeHost requires infrastructure HOT capability"
        )
    from .runtime_host import compose_runtime_host

    return compose_runtime_host(
        campaign_id,
        authenticated_repository_port,
        selected_live_transport,
        campaign_publication_transport,
        hot_owner_store=hot_owner_store,
    )


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


@dataclass(frozen=True, slots=True)
class SaveExitResult:
    """Ephemeral PO-002 result; it changes chat selection, not campaign lifecycle."""

    durability_result: DurabilityPromiseResult
    selection: CampaignSelection | None
    session_context: object | None
    saved: bool
    return_to_selection: bool

    def __post_init__(self) -> None:
        if not isinstance(self.durability_result, DurabilityPromiseResult):
            raise BootstrapContractError("typed durability result is required")
        if type(self.saved) is not bool or type(self.return_to_selection) is not bool:
            raise BootstrapContractError("save/exit result flags must be boolean")
        if self.saved is not self.return_to_selection:
            raise BootstrapContractError("save/exit selection result is inconsistent")
        if self.saved:
            if self.selection is not None or self.session_context is not None:
                raise BootstrapContractError(
                    "confirmed save/exit must clear selection and session context"
                )
        elif (
            not isinstance(self.selection, CampaignSelection)
            or self.session_context is None
        ):
            raise BootstrapContractError(
                "unconfirmed save/exit must retain selection and session context"
            )


def compose_save_exit(
    selection: CampaignSelection,
    durability_result: DurabilityPromiseResult,
    *,
    session_context: object,
) -> SaveExitResult:
    """Return to campaign selection only after the typed required save is accepted."""

    current_selection = require_campaign_selection(selection)
    if current_selection.kind != "existing" or current_selection.campaign_id is None:
        raise BootstrapContractError(
            "save/exit requires an explicitly selected campaign"
        )
    if not isinstance(durability_result, DurabilityPromiseResult):
        raise BootstrapContractError("typed durability result is required")
    if durability_result.promise.campaign_id != current_selection.campaign_id:
        raise BootstrapContractError("save result belongs to another selected campaign")
    if durability_result.promise.scope != "SAVE_ALL_DIRTY":
        raise BootstrapContractError("save/exit requires the SAVE_ALL_DIRTY boundary")
    if session_context is None:
        raise BootstrapContractError(
            "recovery-safe selected session context is required"
        )

    saved = (
        durability_result.status == "CONFIRMED_ACCEPTED"
        and durability_result.acknowledged is True
    )
    return SaveExitResult(
        durability_result=durability_result,
        selection=None if saved else current_selection,
        session_context=None if saved else session_context,
        saved=saved,
        return_to_selection=saved,
    )


class _MeasuredCampaignPublication(Protocol):
    """The existing RuntimeHost publication service used by T06 product paths."""

    def measure_path_operations(
        self, path_operations: Mapping[str, object | None]
    ) -> Mapping[str, int]: ...

    def publish_owner_delta(
        self,
        *,
        routed_operation: RoutedSerializedOperation,
        path_operations: Mapping[str, object | None],
        owner_generations: Mapping[str, int],
        publication_reason: str,
        basis: object | None = None,
    ) -> PublicationOutcome: ...


class _CampaignPublicationHost(Protocol):
    """One already-composed, immutable campaign-bound RuntimeHost."""

    publication: _MeasuredCampaignPublication


def publish_measured_owner_delta(
    host: _CampaignPublicationHost,
    *,
    routed_operation: RoutedSerializedOperation,
    path_operations: Mapping[str, object | None],
    owner_generations: Mapping[str, int],
    publication_reason: str,
    basis: object | None = None,
) -> tuple[Mapping[str, int], PublicationOutcome]:
    """Measure exact adapter bytes before delegating one existing host write.

    The same operation mapping is passed to measurement and publication. This
    wrapper neither serializes campaign data nor owns publication authority.
    """

    if not isinstance(routed_operation, RoutedSerializedOperation):
        raise BootstrapContractError("owner-routed serialized operation is required")
    if not isinstance(path_operations, Mapping) or not path_operations:
        raise BootstrapContractError("size-governed path operations are required")
    if any(not isinstance(path, str) or not path for path in path_operations):
        raise BootstrapContractError("size-governed paths must be nonempty strings")
    if not isinstance(owner_generations, Mapping):
        raise BootstrapContractError("owner generations must be an object")
    if not isinstance(publication_reason, str) or not publication_reason:
        raise BootstrapContractError("publication reason is required")

    publication = host.publication
    measure = getattr(publication, "measure_path_operations", None)
    writer = getattr(publication, "publish_owner_delta", None)
    if not callable(measure) or not callable(writer):
        raise BootstrapContractError(
            "exact measured publication capability is required"
        )
    try:
        measured = measure(path_operations)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise BootstrapContractError("exact path measurement failed closed") from exc
    if not isinstance(measured, Mapping) or set(measured) != set(path_operations):
        raise BootstrapContractError("exact measurement must cover every write path")
    sizes: dict[str, int] = {}
    for path, size in measured.items():
        if not isinstance(path, str) or type(size) is not int or size < 0:
            raise BootstrapContractError("exact path measurements must be byte counts")
        if path_operations[path] is None and size != 0:
            raise BootstrapContractError("deleted path measurement must be zero")
        sizes[path] = size

    outcome = writer(
        routed_operation=routed_operation,
        path_operations=path_operations,
        owner_generations=owner_generations,
        publication_reason=publication_reason,
        basis=basis,
    )
    if not isinstance(outcome, PublicationOutcome):
        raise BootstrapContractError("host publication outcome is not typed")
    return MappingProxyType(sizes), outcome
