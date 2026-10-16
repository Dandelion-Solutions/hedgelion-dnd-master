"""Campaign-bound runtime composition for the deterministic GAME engine.

The deployment host supplies the authenticated repository capability and the
selected-LIVE reader exactly once at this infrastructure boundary.  Gameplay
services receive only domain requests and candidate data; they never receive a
transport, repository, route resolver or replaceable sibling service.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import weakref
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, NoReturn, Protocol

from .current_owner import (
    CurrentOwnerObservation,
    CurrentOwnerReadSession,
    CurrentOwnerStatus,
    NativeOwnerRef,
)
from .durability import RoutedSerializedOperation
from .hot_store import (
    HotOwnerStorePort,
    NativeHotStore,
    OwnerDocument,
    StaleOwnerGeneration,
)
from .live_state import (
    LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
    WriteAuthority,
    lookup_write_authority,
    select_live_source,
    validate_live_route_completeness,
)
from .native_storage import route_native_record
from .policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign, RepositoryPort
from .publication import (
    CommitAncestryEvidence,
    FrozenCampaignPublicationAttempt,
    PublicationContractError,
    PublicationCurrentClosureEvidence,
    PublicationOutcome,
    PublicationStatus,
    _issue_owner_issued_accepted_publication,
    build_connector_git_plan,
    classify_ref_transition,
    freeze_campaign_publication_attempt,
    freeze_campaign_publication_recovery_basis,
    reconcile_indeterminate_publication,
)

if TYPE_CHECKING:
    from .access_control import PlayerRecord
    from .activity_contracts import (
        AcceptedAdjudicationBasis,
        AdmittedActivityCatalog,
        CompiledActivity,
        NativePreparationContext,
    )
    from .history import (
        HistoryDiscoveryRequest,
        HistoryDiscoveryResult,
        NativeHistoryCandidate,
        NativeSemanticEvent,
    )

# framework_module_version: 1.0.20
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.20"

_REPOSITORY_OPERATIONS: Final[tuple[str, ...]] = (
    "pin_campaign",
    "read_exact_path",
    "read_exact_campaign_ref",
    "read_exact_commit",
    "compare_ancestry",
    "read_authenticated_commit_author",
)
_LIVE_OPERATION: Final[str] = "read_selected_live"
_NATIVE_ORDERING_ROUTE: Final[str] = "runtime_execution"
_PUBLICATION_OPERATIONS: Final[tuple[str, ...]] = (
    "repository_identity",
    "resolve_authenticated_acting_principal",
    "read_ref",
    "create_tree",
    "create_commit",
    "update_ref",
)
_REVISION: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_LIVE_ORIGIN: Final = re.compile(r"^LIVE:[A-Za-z0-9_.:-]+$")
_MAX_EVT_WINDOW_ITEMS: Final[int] = 1000
_EVENT_INDEX_PATH: Final[str] = "INDEX/EVENT_INDEX.yaml"


class SelectedLiveTransport(Protocol):
    """Selected-LIVE source reader supplied by the deployment host."""

    def read_selected_live(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> LiveRouting | None:
        """Return the exact selected route for the current campaign pin."""


class CampaignPublicationTransport(Protocol):
    """Connector Git-data capability bound to the selected campaign repository."""

    def repository_identity(self) -> str:
        """Return the selected repository identity."""

    def resolve_authenticated_acting_principal(
        self, campaign_id: str, pinned_campaign: PinnedCampaign
    ) -> AuthenticatedPrincipalEvidence:
        """Return authenticated application principal evidence for publication."""

    def read_ref(self, target_ref: str) -> object:
        """Read exact current target-ref/head evidence."""

    def create_tree(
        self, base_tree_sha: str, path_operations: Mapping[str, object | None]
    ) -> object:
        """Create one base-tree-derived tree and return its exact identity."""

    def measure_path_operations(
        self, path_operations: Mapping[str, object | None]
    ) -> Mapping[str, int]:
        """Measure exact UTF-8 file bytes with the same serializer as create_tree.

        This method must be deterministic and side-effect-free. Its result names
        every supplied path; a deletion (None) has size zero. The adapter must use
        the exact serializer that its create_tree implementation uses, not an
        estimate or a second representation.
        """

    def create_commit(self, parent_sha: str, tree_sha: str, target_ref: str) -> object:
        """Create one single-parent commit and return its exact identity."""

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        """Request one non-force authority-changing ref transition."""


class RuntimeHostError(ValueError):
    """Raised when a campaign-bound runtime operation cannot be admitted."""


class InputAuthorityUnavailable(RuntimeHostError):
    """Existing scoped hold before protected preparation, costs or RNG."""

    status = "AUTHORITY_UNAVAILABLE"


class AcceptedInputCapability(Protocol):
    """Constructor-bound infrastructure contract, not deployed issuer proof."""

    adapter_profile_id: str
    adapter_profile_generation: int

    def lookup_exchange(
        self, *, repository_identity: str, campaign_id: str,
        adapter_profile_id: str, adapter_profile_generation: int,
        accepted_exchange_key: str,
    ) -> str | None: ...

    def accepted_representation(
        self, *, repository_identity: str, campaign_id: str,
        adapter_profile_id: str, adapter_profile_generation: int,
        accepted_exchange_key: str, host_invocation_ref: str,
    ) -> tuple[object, str]: ...

    def current_principal(self, *, repository_identity: str, campaign_id: str) -> object: ...


class _PublicationRevalidationFailure(Exception):
    """Internal fail-closed result for bounded W02 repository proof."""

    def __init__(
        self,
        status: PublicationStatus,
        cause: str,
        observed_head_sha: str | None,
    ) -> None:
        super().__init__(cause)
        self.status = status
        self.cause = cause
        self.observed_head_sha = observed_head_sha


class NativeOrderingStatus(StrEnum):
    """Bounded result when no native ordered owner is currently admitted."""

    NO_ORDERED_OWNER = "NO_ORDERED_OWNER"


@dataclass(frozen=True, slots=True)
class NativeOrderingResult:
    """Ephemeral result of the fixed native-ordering dispatch route."""

    status: NativeOrderingStatus
    campaign_id: str
    route: str = _NATIVE_ORDERING_ROUTE


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeHostError(f"{label} must be a nonempty string")
    return value


def _revision(value: object, label: str) -> str:
    result = _nonempty_string(value, label)
    if _REVISION.fullmatch(result) is None:
        raise RuntimeHostError(f"{label} must be an exact lowercase Git revision")
    return result


def _json_copy(value: object, label: str) -> object:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RuntimeHostError(f"{label} must not contain a non-finite number")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise RuntimeHostError(f"{label} keys must be strings")
        return {key: _json_copy(item, f"{label}.{key}") for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [
            _json_copy(item, f"{label}[{index}]") for index, item in enumerate(value)
        ]
    raise RuntimeHostError(f"{label} must contain JSON-compatible values")


def _freeze_json(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_json(item) for key, item in value.items()}
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze_json(item) for item in value)
    return value


def _operation_digest(value: object) -> str:
    copied = _json_copy(value, "publication operation")
    encoded = json.dumps(
        copied, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_revalidation_commit(
    repository: RepositoryPort,
    target_ref: str,
    revision: str,
    *,
    observed_head_sha: str | None,
) -> tuple[Mapping[str, object], str]:
    try:
        value = repository.read_exact_commit(target_ref, revision)
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "EXACT_COMMIT_EVIDENCE_UNAVAILABLE",
            observed_head_sha,
        ) from exc
    if not isinstance(value, Mapping) or value.get("revision") != revision:
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "EXACT_COMMIT_IDENTITY_UNAVAILABLE",
            observed_head_sha,
        )
    for field in ("ref", "campaign_ref"):
        if field in value and value[field] != target_ref:
            raise _PublicationRevalidationFailure(
                PublicationStatus.INDETERMINATE,
                "EXACT_COMMIT_REF_MISMATCH",
                observed_head_sha,
            )
    tree_sha = value.get("tree_sha")
    if not isinstance(tree_sha, str) or _REVISION.fullmatch(tree_sha) is None:
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "EXACT_COMMIT_TREE_UNAVAILABLE",
            observed_head_sha,
        )
    return value, tree_sha


def _require_direct_single_parent(
    commit: Mapping[str, object],
    predecessor_sha: str,
    *,
    observed_head_sha: str | None,
) -> None:
    parent_fields: list[tuple[str, str]] = []
    for field in ("parents", "parent_revisions"):
        if field not in commit:
            continue
        raw_parents = commit[field]
        if not isinstance(raw_parents, Sequence) or isinstance(
            raw_parents, (str, bytes, bytearray)
        ):
            raise _PublicationRevalidationFailure(
                PublicationStatus.INDETERMINATE,
                "COMMIT_PARENT_EVIDENCE_AMBIGUOUS",
                observed_head_sha,
            )
        if len(raw_parents) != 1:
            raise _PublicationRevalidationFailure(
                PublicationStatus.CONFLICT,
                "INTENDED_COMMIT_IS_NOT_SINGLE_PARENT",
                observed_head_sha,
            )
        parent = raw_parents[0]
        if not isinstance(parent, str) or _REVISION.fullmatch(parent) is None:
            raise _PublicationRevalidationFailure(
                PublicationStatus.INDETERMINATE,
                "COMMIT_PARENT_EVIDENCE_AMBIGUOUS",
                observed_head_sha,
            )
        parent_fields.append((field, parent))
    if "parent_revision" in commit:
        parent = commit["parent_revision"]
        if not isinstance(parent, str) or _REVISION.fullmatch(parent) is None:
            raise _PublicationRevalidationFailure(
                PublicationStatus.INDETERMINATE,
                "COMMIT_PARENT_EVIDENCE_AMBIGUOUS",
                observed_head_sha,
            )
        parent_fields.append(("parent_revision", parent))
    if not parent_fields:
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "COMMIT_PARENT_EVIDENCE_UNAVAILABLE",
            observed_head_sha,
        )
    if any(parent != predecessor_sha for _field, parent in parent_fields):
        raise _PublicationRevalidationFailure(
            PublicationStatus.CONFLICT,
            "INTENDED_COMMIT_IS_NOT_DIRECT_CHILD",
            observed_head_sha,
        )


def _exact_changed_paths(
    commit: Mapping[str, object], *, observed_head_sha: str | None
) -> frozenset[str]:
    raw_paths = commit.get("changed_paths")
    if not isinstance(raw_paths, Sequence) or isinstance(
        raw_paths, (str, bytes, bytearray)
    ):
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "COMMIT_CHANGED_PATH_EVIDENCE_UNAVAILABLE",
            observed_head_sha,
        )
    paths: list[str] = []
    for path in raw_paths:
        if not isinstance(path, str) or not path:
            raise _PublicationRevalidationFailure(
                PublicationStatus.INDETERMINATE,
                "COMMIT_CHANGED_PATH_EVIDENCE_AMBIGUOUS",
                observed_head_sha,
            )
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "COMMIT_CHANGED_PATH_EVIDENCE_AMBIGUOUS",
            observed_head_sha,
        )
    return frozenset(paths)


def _read_revalidation_path(
    repository: RepositoryPort,
    pinned: PinnedCampaign,
    path: str,
    *,
    observed_head_sha: str | None,
) -> object:
    try:
        return repository.read_exact_path(pinned, path)
    except KeyError:
        return None
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise _PublicationRevalidationFailure(
            PublicationStatus.INDETERMINATE,
            "EXACT_PATH_EVIDENCE_UNAVAILABLE",
            observed_head_sha,
        ) from exc


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvtSourceWindow:
    """Raw bounded evt-lane source evidence; History owns semantic validation."""

    campaign_id: str
    origin: str
    source_ref: str
    source_revision: str
    lane: str
    lower_exclusive_ordinal: int | None
    upper_ordinal: int | None
    interval_complete_through_upper: bool
    entries: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        _nonempty_string(self.campaign_id, "evt source campaign_id")
        if self.origin != "LOCAL" and _LIVE_ORIGIN.fullmatch(self.origin) is None:
            raise RuntimeHostError(
                "evt source origin is not LOCAL or a selected LIVE origin"
            )
        _nonempty_string(self.source_ref, "evt source_ref")
        _revision(self.source_revision, "evt source_revision")
        if self.lane != "evt":
            raise RuntimeHostError("evt source window lane must be evt")
        lower = self.lower_exclusive_ordinal
        if lower is not None and (type(lower) is not int or lower < 0):
            raise RuntimeHostError(
                "evt lower-exclusive ordinal must be null or non-negative"
            )
        upper = self.upper_ordinal
        if upper is not None and (type(upper) is not int or upper < 1):
            raise RuntimeHostError("evt upper ordinal must be null or positive")
        if self.interval_complete_through_upper is not True:
            raise RuntimeHostError("evt source window must prove interval completeness")
        copied_entries: list[Mapping[str, object]] = []
        expected_ordinal = (lower or 0) + 1
        raw_entries = tuple(self.entries)
        if upper is None and raw_entries:
            raise RuntimeHostError("empty evt upper basis cannot carry entries")
        if upper is not None and upper <= (lower or 0):
            raise RuntimeHostError("evt source interval is empty or reversed")
        for raw_entry in raw_entries:
            if not isinstance(raw_entry, Mapping) or set(raw_entry) != {
                "ordinal",
                "event_id",
                "event_record",
            }:
                raise RuntimeHostError("evt source entry fields are not strict")
            ordinal = raw_entry["ordinal"]
            if type(ordinal) is not int or ordinal != expected_ordinal:
                raise RuntimeHostError("evt source interval is not contiguous")
            event_id = _nonempty_string(raw_entry["event_id"], "evt event_id")
            record = raw_entry["event_record"]
            if not isinstance(record, Mapping) or record.get("event_id") != event_id:
                raise RuntimeHostError("evt source event record identity differs")
            copied_entries.append(
                _freeze_json(_json_copy(raw_entry, "evt source entry"))
            )  # type: ignore[arg-type]
            expected_ordinal += 1
        if upper is not None and expected_ordinal - 1 != upper:
            raise RuntimeHostError("evt source window does not prove its upper basis")
        object.__setattr__(self, "entries", tuple(copied_entries))

    def to_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "origin": self.origin,
            "source_ref": self.source_ref,
            "source_revision": self.source_revision,
            "lane": self.lane,
            "lower_exclusive_ordinal": self.lower_exclusive_ordinal,
            "upper_ordinal": self.upper_ordinal,
            "interval_complete_through_upper": True,
            "entries": [
                _json_copy(entry, "evt source entry") for entry in self.entries
            ],
        }


_EVT_SOURCE_WINDOW_ISSUANCE: dict[
    int, tuple[weakref.ReferenceType[EvtSourceWindow], object]
] = {}


def _mark_adapter_issued_evt_window(value: EvtSourceWindow, host_token: object) -> None:
    value_id = id(value)

    def remove(reference: weakref.ReferenceType[EvtSourceWindow]) -> None:
        entry = _EVT_SOURCE_WINDOW_ISSUANCE.get(value_id)
        if entry is not None and entry[0] is reference:
            _EVT_SOURCE_WINDOW_ISSUANCE.pop(value_id, None)

    _EVT_SOURCE_WINDOW_ISSUANCE[value_id] = (weakref.ref(value, remove), host_token)


def _is_adapter_issued_evt_window(
    value: object, *, host_token: object | None = None
) -> bool:
    entry = _EVT_SOURCE_WINDOW_ISSUANCE.get(id(value))
    return (
        isinstance(value, EvtSourceWindow)
        and entry is not None
        and entry[0]() is value
        and (host_token is None or entry[1] is host_token)
    )


def _issue_evt_source_window(
    *, host_token: object, **values: object
) -> EvtSourceWindow:
    """Create and mark one raw window from the bound source adapter."""
    try:
        window = EvtSourceWindow(**values)  # type: ignore[arg-type]
    except (TypeError, RuntimeHostError) as exc:
        raise RuntimeHostError(
            "evt source adapter produced an invalid raw window"
        ) from exc
    _mark_adapter_issued_evt_window(window, host_token)
    return window


@dataclass(frozen=True, slots=True)
class _OperationBasis:
    """Fresh source basis for one host operation."""

    pinned_campaign: PinnedCampaign
    selected_live: LiveRouting | None
    host_token: object


@dataclass(slots=True)
class _InputSourceOperation:
    """One actual Host/session lifecycle; never a serialized authority verdict."""

    host: RuntimeHost
    basis: _OperationBasis
    session: CurrentOwnerReadSession | None = None
    authority_sources: Mapping[str, object] | None = None
    session_configuration: tuple[object, ...] | None = None

    @property
    def host_token(self) -> object:
        return self.basis.host_token


def _require_nonempty_campaign_id(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeHostError("selected campaign identity is required")
    return value


def _require_operations(value: object, operations: tuple[str, ...], label: str) -> None:
    for operation in operations:
        if not callable(getattr(value, operation, None)):
            raise RuntimeHostError(f"{label} is missing required operation {operation}")


def _validate_pinned_campaign(
    value: object, expected_campaign_id: str
) -> PinnedCampaign:
    if not isinstance(value, PinnedCampaign):
        raise RuntimeHostError("repository did not return an owner-typed campaign pin")
    if value.campaign_id != expected_campaign_id:
        raise RuntimeHostError("repository pin belongs to another campaign")
    return value


def _validate_selected_live(
    value: object, expected_campaign_id: str
) -> LiveRouting | None:
    if value is None:
        return None
    if not isinstance(value, LiveRouting):
        raise RuntimeHostError(
            "selected-LIVE transport did not return an owner-typed route"
        )
    if value.campaign_id != expected_campaign_id:
        raise RuntimeHostError("selected-LIVE route belongs to another campaign")
    try:
        validate_live_route_completeness(value)
    except ValueError as exc:
        raise RuntimeHostError(
            "selected-LIVE route is not current and complete"
        ) from exc
    return value


class _BoundService:
    """Immutable handle to the one composition root that owns the service."""

    __slots__ = ("_host",)

    def __init__(self, host: RuntimeHost) -> None:
        object.__setattr__(self, "_host", host)

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise AttributeError(f"bound service attribute {name!r} is immutable")

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError(f"bound service attribute {name!r} cannot be deleted")


class CampaignPublicationService(_BoundService):
    """Fixed campaign publication route over the W02 publication owner."""

    __slots__ = ()

    def publish_owner_delta(
        self,
        *,
        routed_operation: RoutedSerializedOperation,
        path_operations: Mapping[str, object | None],
        owner_generations: Mapping[str, int],
        publication_reason: str,
        basis: _OperationBasis | None = None,
    ) -> PublicationOutcome:
        """Publish one owner-local delta without owning its semantic result."""

        transport = self._host._publication_transport
        if transport is None:
            raise RuntimeHostError("campaign publication capability is unavailable")
        if not isinstance(routed_operation, RoutedSerializedOperation):
            raise RuntimeHostError("owner-routed serialized operation is required")
        if not isinstance(path_operations, Mapping):
            raise RuntimeHostError("publication path operations must be an object")

        if basis is None:
            operation_basis = self._host._begin_operation()
        elif not isinstance(basis, _OperationBasis):
            raise RuntimeHostError("publication basis is not host-typed")
        else:
            operation_basis = basis
        if operation_basis.host_token is not self._host._basis_token:
            raise RuntimeHostError("publication basis belongs to another runtime host")
        if operation_basis.pinned_campaign.campaign_id != self._host._campaign_id:
            raise RuntimeHostError("publication basis belongs to another campaign")
        if routed_operation.owner_kind == "runtime.semantic_event":
            # Campaign-native event publication only. Existing LIVE absorption
            # closures retain their native owner-derived companion unchanged;
            # source-local -> campaign ordinal reconciliation is a held arm.
            path_operations = self._prepare_event_index_companion(
                operation_basis.pinned_campaign, path_operations
            )
        manifest = self._read_exact_path(
            operation_basis.pinned_campaign, "MANIFEST.yaml"
        )
        campaign_card = self._read_exact_path(
            operation_basis.pinned_campaign, "CAMPAIGN_CARD.yaml"
        )
        target_ref = manifest.get("branch") if isinstance(manifest, Mapping) else None
        if not isinstance(target_ref, str) or not target_ref:
            raise RuntimeHostError("campaign manifest has no canonical target ref")
        repository_id = _validate_transport_repository_identity(
            self._host._repository, transport
        )
        principal = self._resolve_principal(transport, operation_basis.pinned_campaign)
        try:
            attempt = freeze_campaign_publication_attempt(
                repository_id=repository_id,
                target_ref=target_ref,
                campaign_id=self._host._campaign_id,
                acting_principal=principal,
                pinned_head_sha=operation_basis.pinned_campaign.revision,
                base_tree_sha=operation_basis.pinned_campaign.tree_sha,
                manifest=manifest,
                campaign_card=campaign_card,
                path_operations=path_operations,
                owner_generations=owner_generations,
                currentness_evidence=operation_basis.pinned_campaign,
                routed_operation=routed_operation,
                publication_reason=publication_reason,
            )
            plan = build_connector_git_plan(attempt)
        except (PublicationContractError, TypeError, ValueError) as exc:
            raise RuntimeHostError("campaign publication attempt is invalid") from exc

        tree_sha = self._exact_revision(
            transport.create_tree(plan.base_tree_sha, plan.path_operations),
            "created tree",
        )
        current_ref = self._read_ref(transport, target_ref)
        if current_ref != attempt.pinned_head_sha:
            return PublicationOutcome(
                PublicationStatus.CONFLICT,
                None,
                current_ref,
                "STALE_OR_NON_FAST_FORWARD",
                dispatched=False,
            )
        commit_sha = self._exact_revision(
            transport.create_commit(plan.commit_parent_sha, tree_sha, target_ref),
            "created commit",
        )
        try:
            raw_response = transport.update_ref(target_ref, commit_sha, force=False)
            outcome = classify_ref_transition(
                raw_response, intended_commit_sha=commit_sha
            )
        except (PublicationContractError, TypeError, ValueError) as exc:
            raise RuntimeHostError(
                "campaign ref transition response is invalid"
            ) from exc
        if outcome.status is PublicationStatus.INDETERMINATE:
            return self._reconcile_indeterminate(attempt, transport, commit_sha)
        if outcome.status is PublicationStatus.ACCEPTED:
            try:
                _issue_owner_issued_accepted_publication(
                    outcome,
                    attempt,
                    intended_commit_sha=commit_sha,
                )
            except PublicationContractError as exc:
                raise RuntimeHostError(
                    "confirmed campaign publication lacks valid W02 acceptance evidence"
                ) from exc
        return outcome

    def _prepare_event_index_companion(
        self,
        pinned: PinnedCampaign,
        operations: Mapping[str, object | None],
    ) -> Mapping[str, object | None]:
        """Join serialized native events to the existing W02 closure, not acceptance."""
        from .history import (
            _semantic_event_fingerprint,
            event_index_after_image,
            validate_event_index,
            validate_semantic_event_draft,
        )
        from .native_storage import FAMILY_ROOTS

        prefix = FAMILY_ROOTS["runtime.semantic_event"] + "/RECORDS/"
        event_operations = {
            path: value for path, value in operations.items()
            if isinstance(path, str) and path.startswith(prefix)
        }
        if not event_operations:
            return operations
        try:
            records = []
            for path, value in event_operations.items():
                event = validate_semantic_event_draft(value)
                expected = route_native_record(
                    "runtime.semantic_event", (event["event_id"],)
                ).relative_path
                if path != expected:
                    raise RuntimeHostError("event publication path differs from native identity")
                records.append(event)
            index = self._read_exact_path(pinned, _EVENT_INDEX_PATH)
            checked = validate_event_index(index)
            existing = {entry["event_id"]: entry for entry in checked["entries"]}
            after_image = _json_copy(index, "event index")
            changed = False
            # This is the existing campaign admission ordinal, never ID order or
            # fictional chronology. LIVE absorption has a separate held arm.
            for event in sorted(records, key=lambda record: record["semantic_order"]):
                enrolled = existing.get(event["event_id"])
                if enrolled is None:
                    after_image = event_index_after_image(after_image, event)
                    changed = True
                else:
                    path = route_native_record(
                        "runtime.semantic_event", (event["event_id"],)
                    ).relative_path
                    exact = self._read_exact_path(pinned, path)
                    exact_event = validate_semantic_event_draft(exact)
                    # Existing exact events may anchor another owner's W02 edge.
                    if (
                        _semantic_event_fingerprint(event)
                        != _semantic_event_fingerprint(exact_event)
                        or enrolled["source_origin"] != "LOCAL"
                        or "native_source_binding" in enrolled
                        or event["semantic_order"] != enrolled["admission_ordinal"]
                        or event["semantic_delta"].get("discovery_refs", [])
                        != enrolled.get("discovery_refs", [])
                    ):
                        raise RuntimeHostError("existing event differs from exact native evidence")
            if (
                _EVENT_INDEX_PATH in operations
                and _json_copy(operations[_EVENT_INDEX_PATH], "event index") != after_image
            ):
                raise RuntimeHostError("event-index companion differs from native derivation")
            return dict(operations) | {_EVENT_INDEX_PATH: after_image} if changed else operations
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeHostError("event publication enrollment is invalid") from exc

    def measure_path_operations(
        self, path_operations: Mapping[str, object | None]
    ) -> Mapping[str, int]:
        """Return exact adapter-serialized UTF-8 byte lengths without publication."""

        transport = self._host._publication_transport
        if transport is None:
            raise RuntimeHostError("campaign publication capability is unavailable")
        if not isinstance(path_operations, Mapping):
            raise RuntimeHostError("measurement path operations must be an object")
        try:
            copied = _json_copy(path_operations, "measurement path operations")
        except (TypeError, ValueError) as exc:
            raise RuntimeHostError("measurement path operations are invalid") from exc
        if not isinstance(copied, dict):
            raise RuntimeHostError("measurement path operations must be an object")
        if any(not isinstance(path, str) or not path for path in copied):
            raise RuntimeHostError("measurement path operation paths must be nonempty")
        measurement = getattr(transport, "measure_path_operations", None)
        if not callable(measurement):
            raise RuntimeHostError(
                "exact campaign path measurement capability is unavailable"
            )
        frozen_operations = MappingProxyType(
            {path: _freeze_json(value) for path, value in copied.items()}
        )
        try:
            measured = measurement(frozen_operations)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("exact campaign path measurement failed") from exc
        if not isinstance(measured, Mapping) or set(measured) != set(copied):
            raise RuntimeHostError(
                "path measurement must return every exact operation path"
            )
        sizes: dict[str, int] = {}
        for path, size in measured.items():
            if not isinstance(path, str) or type(size) is not int or size < 0:
                raise RuntimeHostError(
                    "path measurements must be non-negative integer byte counts"
                )
            if copied[path] is None and size != 0:
                raise RuntimeHostError("deleted path measurements must be zero")
            sizes[path] = size
        return MappingProxyType(sizes)

    def revalidate_published_owner_delta(
        self,
        *,
        routed_operation: RoutedSerializedOperation,
        path_operations: Mapping[str, object | None],
        owner_generations: Mapping[str, int],
        publication_reason: str,
        expected_pinned_head_sha: str,
        intended_commit_sha: str,
    ) -> PublicationOutcome:
        """Re-prove an existing H -> C publication from current repository authority.

        This recovery path performs exact read-side validation only. It does not
        reconstruct the historical acting principal or issue a repository write.
        """

        transport = self._host._publication_transport
        if transport is None:
            raise RuntimeHostError("campaign publication capability is unavailable")
        if not isinstance(routed_operation, RoutedSerializedOperation):
            raise RuntimeHostError("owner-routed serialized operation is required")
        if routed_operation.owner_kind == "runtime.command":
            raise RuntimeHostError(
                "runtime.command recovery requires an unavailable execution/durability join"
            )
        if not isinstance(path_operations, Mapping) or not path_operations:
            raise RuntimeHostError("revalidation path operations must be nonempty")
        try:
            predecessor = _revision(expected_pinned_head_sha, "expected predecessor")
            intended = _revision(intended_commit_sha, "intended commit")
            reason = _nonempty_string(publication_reason, "publication reason")
            routed_payload = _json_copy(
                routed_operation.payload, "owner-routed publication operation"
            )
            supplied_route_payload = _json_copy(
                path_operations.get(routed_operation.relative_path),
                "owner-routed path operation",
            )
        except (RuntimeHostError, TypeError, ValueError) as exc:
            raise RuntimeHostError(
                "post-publication recovery inputs are invalid"
            ) from exc
        if predecessor == intended:
            raise RuntimeHostError("intended commit must differ from its predecessor")
        if supplied_route_payload != routed_payload:
            raise RuntimeHostError(
                "owner-routed operation is missing or mismatched in the complete write set"
            )
        if not isinstance(owner_generations, Mapping):
            raise RuntimeHostError("owner generations must be a mapping")
        for owner, generation in owner_generations.items():
            if not isinstance(owner, str) or not owner:
                raise RuntimeHostError("owner generation key must be nonempty")
            if (
                isinstance(generation, bool)
                or not isinstance(generation, int)
                or generation < 0
            ):
                raise RuntimeHostError(
                    "owner generation must be a non-negative integer"
                )

        observed_head: str | None = None
        try:
            repository = self._host._repository
            pinned_value = repository.pin_campaign(self._host._campaign_id)
            pinned_current = _validate_pinned_campaign(
                pinned_value, self._host._campaign_id
            )
            observed_head = pinned_current.revision
            current_manifest = self._read_exact_path(pinned_current, "MANIFEST.yaml")
            current_card = self._read_exact_path(pinned_current, "CAMPAIGN_CARD.yaml")
            if (
                current_manifest.get("campaign_id") != self._host._campaign_id
                or current_card.get("campaign_id") != self._host._campaign_id
                or current_card.get("campaign_name")
                != current_manifest.get("campaign_name")
            ):
                raise _PublicationRevalidationFailure(
                    PublicationStatus.CONFLICT,
                    "CURRENT_CAMPAIGN_IDENTITY_MISMATCH",
                    observed_head,
                )
            target_ref = current_manifest.get("branch")
            if not isinstance(target_ref, str) or not target_ref:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.INDETERMINATE,
                    "CURRENT_CAMPAIGN_REF_UNAVAILABLE",
                    observed_head,
                )
            repository_id = _validate_transport_repository_identity(
                repository, transport
            )
            if self._read_ref(transport, target_ref) != observed_head:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.INDETERMINATE,
                    "CURRENT_REF_AND_REPOSITORY_PIN_DIVERGED",
                    observed_head,
                )

            _predecessor_commit, predecessor_tree = _read_revalidation_commit(
                repository,
                target_ref,
                predecessor,
                observed_head_sha=observed_head,
            )
            predecessor_pin = PinnedCampaign(
                self._host._campaign_id, predecessor, predecessor_tree
            )
            predecessor_manifest = self._read_exact_path(
                predecessor_pin, "MANIFEST.yaml"
            )
            predecessor_card = self._read_exact_path(
                predecessor_pin, "CAMPAIGN_CARD.yaml"
            )
            if current_manifest.get("created_at") != predecessor_manifest.get(
                "created_at"
            ):
                raise _PublicationRevalidationFailure(
                    PublicationStatus.CONFLICT,
                    "CAMPAIGN_CREATION_IDENTITY_CHANGED",
                    observed_head,
                )
            recovery_path_operations = path_operations
            if routed_operation.owner_kind == "runtime.semantic_event":
                try:
                    recovery_path_operations = self._prepare_event_index_companion(
                        predecessor_pin, path_operations
                    )
                except RuntimeHostError as exc:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.CONFLICT,
                        "RECOVERY_EVENT_INDEX_COMPANION_INVALID",
                        observed_head,
                    ) from exc
            try:
                recovery_basis = freeze_campaign_publication_recovery_basis(
                    repository_id=repository_id,
                    target_ref=target_ref,
                    campaign_id=self._host._campaign_id,
                    pinned_head_sha=predecessor,
                    base_tree_sha=predecessor_tree,
                    intended_commit_sha=intended,
                    manifest=predecessor_manifest,
                    campaign_card=predecessor_card,
                    path_operations=recovery_path_operations,
                    owner_generations=owner_generations,
                    routed_operation=routed_operation,
                    publication_reason=reason,
                )
            except (PublicationContractError, TypeError, ValueError) as exc:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.CONFLICT,
                    "RECOVERY_OPERATION_SET_INVALID_AT_PREDECESSOR",
                    observed_head,
                ) from exc

            intended_commit, intended_tree = _read_revalidation_commit(
                repository,
                target_ref,
                intended,
                observed_head_sha=observed_head,
            )
            if intended_tree == predecessor_tree:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.CONFLICT,
                    "INTENDED_COMMIT_HAS_NO_TREE_DELTA",
                    observed_head,
                )
            _require_direct_single_parent(
                intended_commit,
                predecessor,
                observed_head_sha=observed_head,
            )
            changed_paths = _exact_changed_paths(
                intended_commit, observed_head_sha=observed_head
            )
            expected_digests = recovery_basis.publication_operation_digests()
            if changed_paths != frozenset(expected_digests):
                raise _PublicationRevalidationFailure(
                    PublicationStatus.CONFLICT,
                    "INTENDED_COMMIT_CHANGED_PATH_SET_MISMATCH",
                    observed_head,
                )

            for path, expected_digest in expected_digests.items():
                base_value = _read_revalidation_path(
                    repository,
                    predecessor_pin,
                    path,
                    observed_head_sha=observed_head,
                )
                if _operation_digest(base_value) == expected_digest:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.CONFLICT,
                        "RECOVERY_OPERATION_IS_NOOP_AT_PREDECESSOR",
                        observed_head,
                    )

            intended_pin = PinnedCampaign(
                self._host._campaign_id, intended, intended_tree
            )
            for path, expected_digest in expected_digests.items():
                intended_value = _read_revalidation_path(
                    repository,
                    intended_pin,
                    path,
                    observed_head_sha=observed_head,
                )
                if _operation_digest(intended_value) != expected_digest:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.CONFLICT,
                        "INTENDED_COMMIT_OPERATION_CLOSURE_MISMATCH",
                        observed_head,
                    )

            if observed_head == intended:
                if pinned_current.tree_sha != intended_tree:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.INDETERMINATE,
                        "CURRENT_COMMIT_TREE_MISMATCH",
                        observed_head,
                    )
                ancestry = None
                cause = "RECONCILED_CURRENT_CLOSURE"
                evidence_kind_head = intended
            else:
                current_commit, current_tree = _read_revalidation_commit(
                    repository,
                    target_ref,
                    observed_head,
                    observed_head_sha=observed_head,
                )
                del current_commit
                if current_tree != pinned_current.tree_sha:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.INDETERMINATE,
                        "CURRENT_COMMIT_TREE_MISMATCH",
                        observed_head,
                    )
                try:
                    ancestry_value = repository.compare_ancestry(
                        target_ref, intended, observed_head
                    )
                except (
                    AttributeError,
                    KeyError,
                    OSError,
                    TypeError,
                    ValueError,
                ) as exc:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.INDETERMINATE,
                        "CURRENT_LINEAGE_EVIDENCE_UNAVAILABLE",
                        observed_head,
                    ) from exc
                if not isinstance(ancestry_value, Mapping):
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.INDETERMINATE,
                        "CURRENT_LINEAGE_EVIDENCE_AMBIGUOUS",
                        observed_head,
                    )
                relation = ancestry_value.get("relation")
                if relation == "NOT_ANCESTOR" or relation == "EQUAL":
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.CONFLICT,
                        "INTENDED_COMMIT_NOT_IN_CURRENT_LINEAGE",
                        observed_head,
                    )
                if relation != "ANCESTOR":
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.INDETERMINATE,
                        "CURRENT_LINEAGE_EVIDENCE_AMBIGUOUS",
                        observed_head,
                    )
                ancestry = CommitAncestryEvidence(
                    ancestor_sha=intended, descendant_sha=observed_head
                )
                cause = "RECONCILED_ANCESTOR_CURRENT_CLOSURE"
                evidence_kind_head = observed_head

            closure_digests: dict[str, str] = {}
            for path, expected_digest in expected_digests.items():
                current_value = _read_revalidation_path(
                    repository,
                    pinned_current,
                    path,
                    observed_head_sha=observed_head,
                )
                actual_digest = _operation_digest(current_value)
                if actual_digest != expected_digest:
                    raise _PublicationRevalidationFailure(
                        PublicationStatus.CONFLICT,
                        "CURRENT_OPERATION_CLOSURE_MISMATCH",
                        observed_head,
                    )
                closure_digests[path] = actual_digest

            if self._read_ref(transport, target_ref) != observed_head:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.INDETERMINATE,
                    "CURRENT_REF_MOVED_DURING_REVALIDATION",
                    observed_head,
                )
            closure = PublicationCurrentClosureEvidence(
                base_revision=predecessor,
                head_sha=evidence_kind_head,
                tree_sha=pinned_current.tree_sha,
                operation_digests=closure_digests,
            )
            outcome = PublicationOutcome(
                PublicationStatus.ACCEPTED,
                intended,
                observed_head,
                cause,
                dispatched=False,
            )
            try:
                _issue_owner_issued_accepted_publication(
                    outcome,
                    recovery_basis,
                    intended_commit_sha=intended,
                    current_closure=closure,
                    ancestry=ancestry,
                )
            except PublicationContractError as exc:
                raise _PublicationRevalidationFailure(
                    PublicationStatus.INDETERMINATE,
                    "W02_RECOVERY_EVIDENCE_ISSUANCE_FAILED",
                    observed_head,
                ) from exc
            return outcome
        except _PublicationRevalidationFailure as exc:
            return PublicationOutcome(
                exc.status,
                intended,
                exc.observed_head_sha,
                exc.cause,
                dispatched=False,
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError):
            return PublicationOutcome(
                PublicationStatus.INDETERMINATE,
                intended,
                observed_head,
                "POSTPUBLICATION_REVALIDATION_INSUFFICIENT",
                dispatched=False,
            )

    def _read_exact_path(
        self, pinned: PinnedCampaign, path: str
    ) -> Mapping[str, object]:
        try:
            value = self._host._repository.read_exact_path(pinned, path)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError(
                f"exact campaign publication read failed for {path}"
            ) from exc
        if not isinstance(value, Mapping):
            raise RuntimeHostError(
                f"exact campaign publication path is not an object: {path}"
            )
        return value

    @staticmethod
    def _resolve_principal(
        transport: CampaignPublicationTransport, pinned: PinnedCampaign
    ) -> AuthenticatedPrincipalEvidence:
        try:
            principal = transport.resolve_authenticated_acting_principal(
                pinned.campaign_id, pinned
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError(
                "authenticated publication principal is unavailable"
            ) from exc
        if not isinstance(principal, AuthenticatedPrincipalEvidence):
            raise RuntimeHostError("publication principal is not owner-typed")
        return principal

    @staticmethod
    def _exact_revision(value: object, label: str) -> str:
        if isinstance(value, Mapping):
            value = value.get("sha", value.get("tree_sha", value.get("commit_sha")))
        return _revision(value, label)

    @staticmethod
    def _read_ref(transport: CampaignPublicationTransport, target_ref: str) -> str:
        try:
            value = transport.read_ref(target_ref)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("campaign target ref read failed") from exc
        if not isinstance(value, Mapping):
            raise RuntimeHostError("campaign target ref evidence is not typed")
        return _revision(value.get("head_sha"), "campaign target ref head")

    def _reconcile_indeterminate(
        self,
        attempt: FrozenCampaignPublicationAttempt,
        transport: CampaignPublicationTransport,
        intended_commit_sha: str,
    ) -> PublicationOutcome:
        current_evidence: Mapping[str, object] | None = None

        def read_current() -> Mapping[str, object]:
            nonlocal current_evidence
            try:
                observed = self._read_ref(transport, attempt.target_ref)
                commit_evidence = self._host._repository.read_exact_commit(
                    attempt.target_ref, observed
                )
                if not isinstance(commit_evidence, Mapping):
                    return {}
                pinned = self._host._repository.pin_campaign(self._host._campaign_id)
                if not isinstance(pinned, PinnedCampaign):
                    return {}
                if (
                    pinned.campaign_id != self._host._campaign_id
                    or pinned.revision != observed
                ):
                    return {}
                operation_digests: dict[str, str] = {}
                for path in attempt.path_operations:
                    try:
                        value = self._host._repository.read_exact_path(pinned, path)
                    except KeyError:
                        value = None
                    operation_digests[path] = _operation_digest(value)
                closure = PublicationCurrentClosureEvidence(
                    base_revision=attempt.pinned_head_sha,
                    head_sha=observed,
                    tree_sha=pinned.tree_sha,
                    operation_digests=operation_digests,
                )
                evidence: dict[str, object] = {"closure": closure}
                if observed != intended_commit_sha:
                    ancestry_value = self._host._repository.compare_ancestry(
                        attempt.target_ref, intended_commit_sha, observed
                    )
                    if (
                        isinstance(ancestry_value, Mapping)
                        and ancestry_value.get("relation") == "ANCESTOR"
                    ):
                        evidence["ancestry"] = CommitAncestryEvidence(
                            ancestor_sha=intended_commit_sha,
                            descendant_sha=observed,
                        )
                current_evidence = evidence
                return evidence
            except (
                AttributeError,
                KeyError,
                OSError,
                TypeError,
                ValueError,
                PublicationContractError,
            ):
                return {}

        try:
            outcome = reconcile_indeterminate_publication(
                attempt,
                read_current,
                intended_commit_sha=intended_commit_sha,
            )
        except (PublicationContractError, TypeError, ValueError) as exc:
            raise RuntimeHostError(
                "indeterminate publication reconciliation failed"
            ) from exc
        if outcome.status is PublicationStatus.ACCEPTED:
            closure = (
                None if current_evidence is None else current_evidence.get("closure")
            )
            ancestry = (
                None if current_evidence is None else current_evidence.get("ancestry")
            )
            try:
                _issue_owner_issued_accepted_publication(
                    outcome,
                    attempt,
                    intended_commit_sha=intended_commit_sha,
                    current_closure=closure,
                    ancestry=ancestry,
                )
            except PublicationContractError as exc:
                raise RuntimeHostError(
                    "reconciled campaign publication lacks valid W02 acceptance evidence"
                ) from exc
        return outcome


class SemanticEventSourceAdapter(_BoundService):
    """Bound raw evt-source enumeration; native History remains authoritative."""

    __slots__ = ()

    def read_local_evt_window(
        self,
        *,
        lower_exclusive_ordinal: int | None,
        max_items: int,
        _basis: _OperationBasis | None = None,
    ) -> EvtSourceWindow:
        lower = self._validate_window_request(lower_exclusive_ordinal, max_items)
        basis = self._operation_basis(_basis)
        manifest = self._read_exact_path(basis.pinned_campaign, "MANIFEST.yaml")
        branch = manifest.get("branch")
        if not isinstance(branch, str) or not branch:
            raise RuntimeHostError("LOCAL evt source has no exact campaign ref")
        index = self._read_exact_path(basis.pinned_campaign, _EVENT_INDEX_PATH)
        selected = self._index_entries(index, lower, max_items, source_origin="LOCAL")
        entries: list[Mapping[str, object]] = []
        for ordinal, event_id, path in selected:
            record = self._read_exact_path(basis.pinned_campaign, path)
            if record.get("event_id") != event_id:
                raise RuntimeHostError(
                    "LOCAL evt record identity differs from enrollment"
                )
            entries.append(
                {"ordinal": ordinal, "event_id": event_id, "event_record": record}
            )
        upper = selected[-1][0] if selected else None
        return _issue_evt_source_window(
            host_token=self._host._basis_token,
            campaign_id=self._host._campaign_id,
            origin="LOCAL",
            source_ref=branch,
            source_revision=basis.pinned_campaign.revision,
            lane="evt",
            lower_exclusive_ordinal=lower,
            upper_ordinal=upper,
            interval_complete_through_upper=True,
            entries=tuple(entries),
        )

    def read_selected_live_evt_window(
        self,
        *,
        origin: str,
        lower_exclusive_ordinal: int | None,
        max_items: int,
        _basis: _OperationBasis | None = None,
        require_complete_source: bool = False,
    ) -> EvtSourceWindow:
        lower = self._validate_window_request(lower_exclusive_ordinal, max_items)
        if type(require_complete_source) is not bool:
            raise RuntimeHostError("complete-source requirement must be boolean")
        if require_complete_source and (lower is not None or max_items != 1000):
            raise RuntimeHostError(
                "complete LIVE metadata revalidation requires the full finite window"
            )
        if _LIVE_ORIGIN.fullmatch(origin) is None:
            raise RuntimeHostError("selected LIVE evt origin is invalid")
        basis = self._operation_basis(_basis)
        routing = basis.selected_live
        if routing is None or not routing.complete:
            raise RuntimeHostError("selected LIVE routing is unavailable")
        epoch_id = origin.removeprefix("LIVE:")
        matches = tuple(
            entry for entry in routing.entries if entry.epoch_id == epoch_id
        )
        if len(matches) > 1:
            raise RuntimeHostError("selected LIVE source is ambiguous")
        if not matches:
            from .history import validate_event_index, validate_semantic_event_draft

            index = self._read_exact_path(basis.pinned_campaign, _EVENT_INDEX_PATH)
            try:
                checked = validate_event_index(index)
            except (TypeError, ValueError) as exc:
                raise RuntimeHostError("absorbed LIVE event index is invalid") from exc
            anchored = tuple(
                entry
                for entry in checked["entries"]
                if entry["source_origin"] == origin
            )
            if not anchored:
                raise RuntimeHostError(
                    "selected LIVE source has no positively anchored absorbed history"
                )
            binding = anchored[0]["native_source_binding"]
            if binding["source_key"][0] != self._host._campaign_id:
                raise RuntimeHostError(
                    "absorbed LIVE source binding belongs to another campaign"
                )
            selected = self._index_entries(
                checked, lower, max_items, source_origin=origin
            )
            entries: list[Mapping[str, object]] = []
            entry_by_ordinal = {entry["admission_ordinal"]: entry for entry in anchored}
            for ordinal, event_id, path in selected:
                record = validate_semantic_event_draft(
                    self._read_exact_path(basis.pinned_campaign, path)
                )
                index_entry = entry_by_ordinal[ordinal]
                if (
                    record["event_id"] != event_id
                    or record["semantic_order"] != ordinal
                    or record["semantic_delta"].get("discovery_refs", [])
                    != index_entry.get("discovery_refs", [])
                ):
                    raise RuntimeHostError(
                        "absorbed LIVE event differs from its exact source anchor"
                    )
                entries.append(
                    {"ordinal": ordinal, "event_id": event_id, "event_record": record}
                )
            upper = selected[-1][0] if selected else None
            return _issue_evt_source_window(
                host_token=self._host._basis_token,
                campaign_id=self._host._campaign_id,
                origin=origin,
                source_ref=binding["source_ref"],
                source_revision=binding["source_revision"],
                lane="evt",
                lower_exclusive_ordinal=lower,
                upper_ordinal=upper,
                interval_complete_through_upper=True,
                entries=tuple(entries),
            )
        source = select_live_source(routing, matches[0].source_key)
        if source is None or source.epoch_id != epoch_id:
            raise RuntimeHostError("selected LIVE source is not current")
        reader = getattr(self._host._live_transport, "read_selected_live_source", None)
        if not callable(reader):
            raise RuntimeHostError(
                "selected LIVE source-domain read capability is unavailable"
            )
        try:
            packed = reader(routing, source)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("selected LIVE source-domain read failed") from exc
        if require_complete_source:
            if isinstance(packed, LiveNativeStatePack):
                owner_states: object = packed.native_owner_states
            elif isinstance(packed, Mapping):
                owner_states = packed.get("native_owner_states")
            else:
                owner_states = None
            event_state = (
                owner_states.get("runtime.semantic_event")
                if isinstance(owner_states, Mapping)
                else None
            )
            if (
                not isinstance(event_state, Mapping)
                or type(event_state.get("upper_ordinal")) is not int
                or event_state["upper_ordinal"] > 1000
            ):
                raise RuntimeHostError(
                    "selected LIVE exact metadata exceeds the finite source bound"
                )
        selected = self._live_entries(packed, source, lower, max_items)
        entries = tuple(
            {"ordinal": ordinal, "event_id": event_id, "event_record": record}
            for ordinal, event_id, record in selected
        )
        upper = selected[-1][0] if selected else None
        return _issue_evt_source_window(
            host_token=self._host._basis_token,
            campaign_id=self._host._campaign_id,
            origin=origin,
            source_ref=source.source_ref,
            source_revision=source.source_revision,
            lane="evt",
            lower_exclusive_ordinal=lower,
            upper_ordinal=upper,
            interval_complete_through_upper=True,
            entries=entries,
        )

    def _operation_basis(self, value: _OperationBasis | None) -> _OperationBasis:
        if value is None:
            return self._host._begin_operation()
        if (
            not isinstance(value, _OperationBasis)
            or value.host_token is not self._host._basis_token
            or value.pinned_campaign.campaign_id != self._host._campaign_id
        ):
            raise RuntimeHostError("evt source basis belongs to another runtime host")
        return value

    def _read_exact_path(
        self, pinned: PinnedCampaign, path: str
    ) -> Mapping[str, object]:
        try:
            value = self._host._repository.read_exact_path(pinned, path)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError(f"exact evt source read failed for {path}") from exc
        if not isinstance(value, Mapping):
            raise RuntimeHostError(f"exact evt source path is not an object: {path}")
        return value

    @staticmethod
    def _validate_window_request(lower: int | None, max_items: int) -> int | None:
        if lower is not None and (type(lower) is not int or lower < 0):
            raise RuntimeHostError(
                "evt lower-exclusive ordinal must be null or non-negative"
            )
        if type(max_items) is not int or not 1 <= max_items <= _MAX_EVT_WINDOW_ITEMS:
            raise RuntimeHostError(
                "evt max_items is outside the bounded resource limit"
            )
        return lower

    @staticmethod
    def _index_entries(
        value: Mapping[str, object],
        lower: int | None,
        max_items: int,
        *,
        source_origin: str = "LOCAL",
    ) -> list[tuple[int, str, str]]:
        from .history import validate_event_index

        try:
            checked = validate_event_index(value)
        except (TypeError, ValueError) as exc:
            raise RuntimeHostError("evt enrollment/index is invalid") from exc
        if source_origin != "LOCAL" and _LIVE_ORIGIN.fullmatch(source_origin) is None:
            raise RuntimeHostError("evt source origin is not admitted")
        lane_entries = [
            entry
            for entry in checked["entries"]
            if entry["source_origin"] == source_origin
        ]
        expected_length = len(lane_entries)
        start = lower or 0
        if start > expected_length:
            raise RuntimeHostError(
                "evt source-local lower cursor exceeds the complete upper basis"
            )
        stop = min(expected_length, start + max_items)
        if start == expected_length and start > 0:
            raise RuntimeHostError(
                "evt source has no new interval after the source-local cursor"
            )
        result: list[tuple[int, str, str]] = []
        for raw in lane_entries[start:stop]:
            event_id = raw["event_id"]
            ordinal = raw["admission_ordinal"]
            path = raw["path"]
            expected_path = route_native_record(
                "runtime.semantic_event", (event_id,)
            ).relative_path
            if path != expected_path:
                raise RuntimeHostError("evt enrollment path is not the known-ID route")
            result.append((ordinal, event_id, expected_path))
        if len({event_id for _ordinal, event_id, _path in result}) != len(result):
            raise RuntimeHostError("evt source-local event identities are not unique")
        return result

    @classmethod
    def _live_entries(
        cls,
        value: object,
        source: LiveEnvelope,
        lower: int | None,
        max_items: int,
    ) -> list[tuple[int, str, Mapping[str, object]]]:
        if isinstance(value, LiveNativeStatePack):
            if (
                value.source_key != source.source_key
                or value.source_revision != source.source_revision
            ):
                raise RuntimeHostError("selected LIVE packed source is stale")
            owner_states: object = value.native_owner_states
        elif isinstance(value, Mapping):
            if (
                value.get("schema_version") != LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION
                or value.get("kind") != "runtime.live_native_state_pack"
            ):
                raise RuntimeHostError(
                    "selected LIVE source pack schema is unsupported"
                )
            raw_source_key = value.get("source_key")
            if (
                not isinstance(raw_source_key, Sequence)
                or isinstance(raw_source_key, (str, bytes))
                or tuple(raw_source_key) != source.source_key
            ):
                raise RuntimeHostError("selected LIVE packed source identity differs")
            if value.get("source_revision") != source.source_revision:
                raise RuntimeHostError("selected LIVE source revision is stale")
            owner_states = value.get("native_owner_states")
        else:
            raise RuntimeHostError("selected LIVE source evidence is not a typed pack")
        if not isinstance(owner_states, Mapping):
            raise RuntimeHostError("selected LIVE native owner evidence is missing")
        event_state = owner_states.get("runtime.semantic_event")
        if (
            not isinstance(event_state, Mapping)
            or event_state.get("complete") is not True
        ):
            raise RuntimeHostError("selected LIVE evt enrollment is incomplete")
        raw_entries = event_state.get("entries")
        if not isinstance(raw_entries, Sequence) or isinstance(
            raw_entries, (str, bytes)
        ):
            raise RuntimeHostError("selected LIVE evt enrollment entries are missing")
        upper_ordinal = event_state.get("upper_ordinal")
        if type(upper_ordinal) is not int or upper_ordinal < 0:
            raise RuntimeHostError("selected LIVE evt upper basis is invalid")
        if upper_ordinal != len(raw_entries):
            raise RuntimeHostError(
                "selected LIVE evt upper basis differs from enrollment"
            )
        start = lower or 0
        if start > upper_ordinal:
            raise RuntimeHostError("selected LIVE evt cursor exceeds its upper basis")
        stop = min(upper_ordinal, start + max_items)
        if start == upper_ordinal and start > 0:
            raise RuntimeHostError("selected LIVE evt source has no new interval")
        result: list[tuple[int, str, Mapping[str, object]]] = []
        for index in range(start, stop):
            raw = raw_entries[index]
            if not isinstance(raw, Mapping):
                raise RuntimeHostError(
                    "selected LIVE evt enrollment entry is not typed"
                )
            ordinal = raw.get("ordinal")
            event_id = raw.get("event_id")
            record = raw.get("event_record")
            if type(ordinal) is not int or ordinal != index + 1:
                raise RuntimeHostError(
                    "selected LIVE evt enrollment interval is not contiguous"
                )
            if not isinstance(event_id, str) or not event_id:
                raise RuntimeHostError(
                    "selected LIVE evt enrollment identity is invalid"
                )
            if not isinstance(record, Mapping) or record.get("event_id") != event_id:
                raise RuntimeHostError("selected LIVE evt record identity differs")
            result.append((ordinal, event_id, deepcopy(dict(record))))
        if len({event_id for _ordinal, event_id, _record in result}) != len(result):
            raise RuntimeHostError(
                "selected LIVE evt enrollment identities are not unique"
            )
        return result


class ContextService(_BoundService):
    """Fixed route to the owner-native ephemeral Context Runtime."""

    __slots__ = ()

    def assemble(
        self,
        request: dict[str, object],
        candidates: list[dict[str, object]],
    ) -> dict[str, object]:
        basis = self._host._begin_operation()
        try:
            from . import context_runtime
        except ModuleNotFoundError as exc:
            raise RuntimeHostError("Context Runtime owner is unavailable") from exc
        return context_runtime._assemble_bound_context(
            request,
            candidates,
            repository=self._host._repository,
            pinned_campaign=basis.pinned_campaign,
            selected_live=basis.selected_live,
            selected_live_reader=self._host._live_transport,
            current_owner_session=self._host._current_owner.begin(basis),
        )


class ActorContinuityEstablishmentStatus(StrEnum):
    ESTABLISHED = "ESTABLISHED"
    NO_CHANGE = "NO_CHANGE"
    UNSUPPORTED = "UNSUPPORTED"
    REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"


@dataclass(frozen=True, slots=True)
class ActorContinuityEstablishmentResult:
    status: ActorContinuityEstablishmentStatus
    owner_ref: NativeOwnerRef | None = None
    before_state_revision: int | None = None
    after_state_revision: int | None = None


class CurrentOwnerView(_BoundService):
    """Fixed operation-scoped read route over exact source and admitted HOT."""

    __slots__ = ()

    def _input_session_configuration(self, operation: _InputSourceOperation) -> tuple[object, ...]:
        """Snapshot only the issued data plane, not the expanding semantic union."""
        session = operation.session
        pin = session._pinned_campaign
        live = session._selected_live
        return (id(session), id(operation.basis), session._campaign_id, id(session.operation_token),
            id(pin), pin.campaign_id, pin.revision, pin.tree_sha, id(live),
            None if live is None else _operation_digest(live.as_mapping()),
            id(session._hot_store), id(session._reader), id(session._source_basis_reader), id(session._live_reader),
            id(self._host._repository), id(self._host._live_transport), id(self._host._hot_store),
            id(self._host._accepted_input_capability))

    def _observe_command_input(
        self, command: Mapping[str, object], *,
        required_owner_refs: tuple[NativeOwnerRef, ...] = (),
        current_authority: bool = True,
    ) -> CurrentOwnerObservation:
        """Read-only TC/native-source preparation, never native input issue.

        The optional adapter is fixed at infrastructure composition. Every union
        expansion re-reads the full accumulated set through the existing P0 owner
        session, including admitted HOT and exact selected LIVE sources.
        ``current_authority=False`` requests historical source/read validation
        only. It never issues a permission bit: protected command acceptance and
        preparation independently require fresh current control again.
        """
        if type(current_authority) is not bool:
            raise RuntimeHostError("input validation purpose must be explicit")
        if self._host._accepted_input_capability is None:
            raise InputAuthorityUnavailable("accepted-input issuer is unavailable")
        operation = _InputSourceOperation(self._host, self._host._begin_operation())
        session = CurrentOwnerReadSession(
            campaign_id=self._host._campaign_id, operation_token=operation,
            pinned_campaign=operation.basis.pinned_campaign, selected_live=operation.basis.selected_live,
            hot_store=self._host._hot_store, reader=self._host._read_current_owner_path,
            source_basis_reader=self._host._read_current_owner_basis,
            live_reader=self._host._read_current_owner_live,
        )
        operation.session = session
        operation.session_configuration = self._input_session_configuration(operation)
        try:
            interaction_ref = NativeOwnerRef("runtime.interaction", (command["interaction_id"],))
            observation = session.require((interaction_ref, *required_owner_refs))
            interaction = self._input_payload(observation, interaction_ref)
            # Lookup the accepted mapping before consulting the acting principal.
            principal = self._input_adapter_principal(interaction)
            authority = self._input_current_authority_sources(operation, principal)
            operation.authority_sources = _freeze_json(authority)
            refs = self._input_required_refs(command, observation, authority)
            observation = session.require(tuple(refs))
            self._validate_input_player_route(observation, authority)
            # The mixed marker belongs to its exact native R, not a copied DTO.
            self._input_origin(command, observation)
            if current_authority:
                self._input_current_control(command, observation, principal, authority)
            self._validate_command_input_observation(observation, command, current_authority=current_authority)
            return observation
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            if isinstance(exc, RuntimeHostError):
                raise
            raise InputAuthorityUnavailable("native input source/authority closure is unavailable") from exc

    def _observe_retained_resolution_sources(self, session: CurrentOwnerReadSession,
            observation: CurrentOwnerObservation, roots: Mapping[str, str]) -> tuple[CurrentOwnerObservation, set[NativeOwnerRef]]:
        """Read only the existing finite R/child/suspension/event source graph."""
        from .recovery import _validate_event_identity
        from .recovery_roots import _validate_native_owner
        from .runtime_execution import (
            _pending_offer,
            _validate_action_resolution_binding,
            _validate_ordering_owner_schema,
            native_command_state,
            resume_input_fingerprint,
            validate_input_interaction,
            validate_retained_resolution,
        )
        from .structural_contracts import validate_contract

        def payload(ref: NativeOwnerRef) -> Mapping[str, object]:
            native = self._input_payload(observation, ref)
            if native.get("campaign_id", self._host._campaign_id) != self._host._campaign_id:
                raise RuntimeHostError("retained execution source campaign differs")
            if isinstance(native.get("state"), Mapping):
                for key, value in native["state"].items():
                    if key in native and _operation_digest(value) != _operation_digest(native[key]):
                        raise RuntimeHostError("retained execution envelope/state projections conflict")
            return native

        def expand(refs: set[NativeOwnerRef]) -> None:
            nonlocal observation
            prior = observation
            observation = session.require(tuple(refs))
            if any(observation.require(ref) != prior.require(ref) for ref in prior.key_union):
                raise RuntimeHostError("REVALIDATION_REQUIRED: retained execution closure moved")

        refs = set(observation.key_union)
        expected_roots = dict(roots)
        refs.update(NativeOwnerRef("runtime.resolution", (identity,)) for identity in roots)
        refs.update(NativeOwnerRef("runtime.command", (identity,)) for identity in roots.values())
        expand(refs)
        checked: set[NativeOwnerRef] = set()
        causes: dict[str, list[Mapping[str, object]]] = {}
        states: dict[str, Mapping[str, object]] = {}
        continuations: dict[str, str] = {}
        events: dict[str, tuple[str, Mapping[str, object]]] = {}
        while True:
            pending = [identity for identity in expected_roots
                       if NativeOwnerRef("runtime.resolution", (identity,)) not in checked]
            if not pending:
                break
            for identity in pending:
                ref = NativeOwnerRef("runtime.resolution", (identity,))
                state = validate_retained_resolution(resolution_id=identity, resolution=payload(ref))
                if state["status"] == "COMPLETED" and not state["segments"]:
                    raise RuntimeHostError("completed retained Resolution lacks its native result segment")
                if state["root_command_id"] != expected_roots[identity]:
                    raise RuntimeHostError("retained Resolution has a foreign root command")
                if identity in roots:
                    command_id = expected_roots[identity]
                    command = native_command_state(payload(NativeOwnerRef("runtime.command", (command_id,))),
                        command_id=command_id, campaign_id=self._host._campaign_id)
                    if command["command_kind"] == "action":
                        _validate_action_resolution_binding(command, identity, state)
                if identity not in roots:
                    matches = [cause for cause in causes.get(identity, ())
                        if cause["firing_key"] == state.get("causal_invocation_key")
                        and cause["activity_id"] == state["activity_id"]
                        and cause["root_command_id"] == state["root_command_id"]
                        and ("procedure_id" not in cause or cause["procedure_id"] == state.get("procedure_id"))]
                    if len(matches) != 1 or "initiating_command_id" in state:
                        raise RuntimeHostError("retained child lacks its exact fixed native cause")
                states[identity] = state
                for child_id in state["child_resolution_ids"]:
                    if child_id in expected_roots:
                        raise RuntimeHostError("retained child owner is cyclic or multiply linked")
                    expected_roots[child_id] = state["root_command_id"]
                    refs.add(NativeOwnerRef("runtime.resolution", (child_id,)))
                    causes[child_id] = [cause for segment in state["segments"]
                        for cause in segment["pending_child_invocations"]
                        if cause.get("child_resolution_id", child_id) == child_id]
                if "continuation_id" in state:
                    continuation_id = state["continuation_id"]
                    if continuation_id in continuations:
                        raise RuntimeHostError("current Continuation has multiple native owners")
                    continuations[continuation_id] = identity
                    refs.add(NativeOwnerRef("runtime.continuation", (continuation_id,)))
                if "procedure_id" in state:
                    refs.add(NativeOwnerRef("runtime.procedure", (state["procedure_id"],)))
                for segment in state["segments"]:
                    for event_id in segment["event_ids"]:
                        if event_id in events:
                            raise RuntimeHostError("retained event ownership is ambiguous")
                        events[event_id] = identity, segment
                        refs.add(NativeOwnerRef("runtime.mechanical_event", (event_id,)))
                checked.add(ref)
            expand(refs)
        # An old segment's output Continuation is a required forward link unless
        # the native R retains its later consuming edge AND the exact I/M source
        # proves that consume. A matching marker in isolation is insufficient.
        retired_outputs = []
        for identity, state in states.items():
            for segment in state["segments"]:
                output = segment.get("continuation_id")
                if output is None or output == state.get("continuation_id"):
                    continue
                consumers = [later for later in state["segments"]
                    if later["segment_sequence"] > segment["segment_sequence"]
                    and later.get("accepted_resume_input", {}).get("target", {}).get("continuation_id") == output]
                if len(consumers) != 1:
                    raise RuntimeHostError("old Continuation forward link lacks an actual retained consume")
                consume = consumers[0]
                marker = consume["accepted_resume_input"]
                refs.add(NativeOwnerRef("runtime.interaction", (marker["response_interaction_id"],)))
                refs.add(NativeOwnerRef("runtime.message", (marker["response_message_id"],)))
                retired_outputs.append((identity, consume))
        if retired_outputs:
            expand(refs)
        for identity, consume in retired_outputs:
            marker = consume["accepted_resume_input"]
            interaction = payload(NativeOwnerRef("runtime.interaction", (marker["response_interaction_id"],)))
            message = payload(NativeOwnerRef("runtime.message", (marker["response_message_id"],)))
            source = validate_input_interaction(campaign_id=self._host._campaign_id, interaction=interaction)
            if (source.get("accepted_resume_ref") != {"resolution_id": identity, "segment_id": consume["segment_id"]}
                    or _operation_digest(source.get("response_target")) != _operation_digest(marker["target"])
                    or _operation_digest(source.get("response_selection")) != _operation_digest(marker["selection"])
                    or message.get("state", message).get("payload_state") != "message.exact_retained"
                    or resume_input_fingerprint(interaction=interaction, message=message) != marker["resume_fingerprint"]):
                raise RuntimeHostError("old Continuation consume lacks its fixed native I/M provenance")
        for identity, parent_id in continuations.items():
            native = payload(NativeOwnerRef("runtime.continuation", (identity,)))
            if "state" in native:
                native = {**native["state"], **{key: native[key] for key in
                    ("kind", "id", "campaign_id", "revision") if key in native}}
            _validate_ordering_owner_schema("runtime.continuation", native)
            parent = states[parent_id]
            if (native["resolution_id"] != parent_id or native["root_command_id"] != parent["root_command_id"]
                    or native.get("procedure_id") != parent.get("procedure_id")
                    or not set(native["expected_child_resolution_ids"]) <= set(parent["child_resolution_ids"])):
                raise RuntimeHostError("current Continuation/parent forward links differ")
            if parent["status"] in {"AWAITING_CHOICE", "AWAITING_REACTION"}:
                kind, _offer, _responder = _pending_offer(native.get("pending_response"),
                    resolution_id=parent_id, continuation_generation=native["generation"])
                if kind != ("choice" if parent["status"] == "AWAITING_CHOICE" else "reaction"):
                    raise RuntimeHostError("current suspension/offer kinds differ")
        for identity, state in states.items():
            if "procedure_id" in state:
                _validate_native_owner("runtime.procedure", payload(NativeOwnerRef("runtime.procedure", (state["procedure_id"],))))
        for event_id, (identity, segment) in events.items():
            native = payload(NativeOwnerRef("runtime.mechanical_event", (event_id,)))
            event = native.get("state", native)
            wire = event if "state" in native else {key: value for key, value in event.items()
                if key not in {"kind", "id", "campaign_id", "revision", "event_id"}}
            validate_contract("runtime-mechanical-event-state", wire)
            _validate_event_identity({"event_id": event_id}, identity, segment, segment["segment_id"], event)
            if event["root_command_id"] != states[identity]["root_command_id"] or event["causal_ref"] != identity:
                raise RuntimeHostError("retained event native cause differs")
        return observation, checked

    def _observe_collaboration_input(
        self, interaction_id: str, clause_id: str, *, principal: object,
        player_route: object,
    ) -> tuple[CurrentOwnerObservation, PlayerRecord]:
        """Observe a voluntary clause use without manufacturing an executable K.

        Public account/route arguments are nominations only. The constructor-bound
        adapter, native campaign route and every nominated Player supply authority.
        This source conformance operation neither associates nor publishes input.
        """
        from .access_control import (
            PrincipalPlayerRoute,
            authorize_operation,
            resolve_player,
            resolve_principal,
        )
        from .runtime_execution import (
            native_command_state,
            validate_input_closure,
            validate_input_interaction,
            validate_retained_resolution,
        )

        if self._host._accepted_input_capability is None:
            raise InputAuthorityUnavailable("accepted-input issuer is unavailable")
        operation = _InputSourceOperation(self._host, self._host._begin_operation())
        session = self.begin(operation.basis)
        try:
            interaction_ref = NativeOwnerRef("runtime.interaction", (interaction_id,))
            observation = session.require((interaction_ref,))
            interaction = self._input_payload(observation, interaction_ref)
            acting = self._input_adapter_principal(interaction)
            authority = self._input_current_authority_sources(operation, acting)
            nominated = resolve_principal(principal)
            if nominated != acting:
                raise InputAuthorityUnavailable("caller principal differs from trusted current principal")
            if authority["mode"] != "multiplayer":
                # The collaboration contributor contract requires an actual Player;
                # creator input remains valid, but cannot fabricate participation.
                raise InputAuthorityUnavailable("collaboration requires current multiplayer participation")
            route = player_route if isinstance(player_route, PrincipalPlayerRoute) else PrincipalPlayerRoute.from_mapping(player_route)
            if _operation_digest(route.as_mapping()) != _operation_digest(authority["route"]):
                raise InputAuthorityUnavailable("caller route differs from complete native account route")
            state = validate_input_interaction(campaign_id=self._host._campaign_id, interaction=interaction)
            if "intent_plan_id" not in state:
                raise InputAuthorityUnavailable("input has no materialized collaboration clause")
            refs = {interaction_ref,
                NativeOwnerRef("runtime.message", (state["input_message_id"],)),
                NativeOwnerRef("runtime.intent_plan", (state["intent_plan_id"],))}
            for entry in authority["route"]["entries"]:
                refs.update(NativeOwnerRef("world.player", (identity,)) for identity in entry["candidate_player_ids"])
            reference = state.get("accepted_resume_ref")
            if reference is not None:
                refs.add(NativeOwnerRef("runtime.resolution", (reference["resolution_id"],)))
            observation = session.require(tuple(refs))
            if reference is not None:
                observation, _checked = self._observe_retained_resolution_sources(session, observation,
                    {reference["resolution_id"]: state["response_target"]["root_command_id"]})
                root_id = state["response_target"]["root_command_id"]
                root = native_command_state(self._input_payload(observation, NativeOwnerRef("runtime.command", (root_id,))),
                    command_id=root_id, campaign_id=self._host._campaign_id)
                if root["command_kind"] != "action":
                    raise InputAuthorityUnavailable("response native action mapping is unavailable")
            interaction = self._input_payload(observation, interaction_ref)
            state = validate_input_interaction(campaign_id=self._host._campaign_id, interaction=interaction)
            message = self._input_payload(observation, NativeOwnerRef("runtime.message", (state["input_message_id"],)))
            plan = self._input_payload(observation, NativeOwnerRef("runtime.intent_plan", (state["intent_plan_id"],)))
            segment = None
            if reference is not None:
                resolution = self._input_payload(observation, NativeOwnerRef("runtime.resolution", (reference["resolution_id"],)))
                native = validate_retained_resolution(resolution_id=reference["resolution_id"], resolution=resolution)
                if native.get("root_command_id") != state["response_target"]["root_command_id"]:
                    raise InputAuthorityUnavailable("mixed response root differs")
                matches = [item for item in native.get("segments", ()) if item.get("segment_id") == reference["segment_id"]]
                if len(matches) != 1:
                    raise InputAuthorityUnavailable("mixed response marker is missing or ambiguous")
                segment = matches[0]
            validate_input_closure(campaign_id=self._host._campaign_id, interaction=interaction,
                message=message, plan=plan, accepted_response_segment=segment)
            clauses = plan["state"]["clauses"]
            matches = [clause for clause in clauses if clause["clause_id"] == clause_id]
            if len(matches) != 1 or matches[0]["clause_kind"] != "intent":
                raise InputAuthorityUnavailable("solicited response is not collaboration consent")
            clause = matches[0]
            if not clause.get("normalized_semantics") and not clause.get("material_exact_text_refs"):
                raise InputAuthorityUnavailable("collaboration clause has no retained material meaning")
            self._validate_input_player_route(observation, authority)
            resolution = resolve_player(acting, authority["route"],
                lambda identity: self._input_player_state(observation, identity), campaign_id=self._host._campaign_id)
            decision = authorize_operation(acting, resolution, operation="gameplay", campaign_id=self._host._campaign_id)
            if not decision.authorized or resolution.player is None:
                raise InputAuthorityUnavailable("active current Player purpose is not authorized")
            if (acting.stable_account_id != state["accepted_input_basis"]["principal"]["stable_account_id"]
                    or resolution.player.player_id != state.get("player_id")):
                raise InputAuthorityUnavailable("current PLAYER executor has no native voluntary-input mapping")
            fresh_acting = self._input_adapter_principal(interaction)
            fresh_authority = self._input_current_authority_sources(operation, fresh_acting)
            if (acting != fresh_acting or _operation_digest(authority) != _operation_digest(fresh_authority)
                    or not session.revalidate(observation)):
                raise InputAuthorityUnavailable("REVALIDATION_REQUIRED: collaboration input source moved")
            return observation, resolution.player
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            if isinstance(exc, RuntimeHostError):
                raise
            raise InputAuthorityUnavailable("native collaboration input authority is unavailable") from exc

    def _validate_input_handoff_sources(self, promise: object) -> None:
        """Validate an already-retained same-domain closure, without issuing it.

        Positive root membership plus exact forward native links protect the
        finite input closure. A complete-page flag is never negative proof.
        Cross-source cleanup protection is not established by a read session;
        absent an admitted protection/freeze reader that case holds explicitly.
        """
        from .current_owner import CurrentOwnerSource
        from .durability import is_authorized_handoff_promise
        from .recovery import (
            _hydrate_execution_result,
            _hydrate_input_root_closure,
            _root_mappings,
        )
        from .runtime_execution import (
            _validate_action_resolution_binding,
            accepted_input_origin,
            command_input_fingerprint,
            execution_result_identity,
            input_native_state,
            native_command_state,
            validate_input_interaction,
            validate_retained_resolution,
        )

        if not is_authorized_handoff_promise(promise) or promise.campaign_id != self._host._campaign_id:
            raise RuntimeHostError("input handoff promise differs from selected campaign")
        basis = self._host._begin_operation()
        session = self.begin(basis)

        def expand(refs: set[NativeOwnerRef]) -> CurrentOwnerObservation:
            prior = session.observation
            fresh = session.require(tuple(refs))
            if prior is not None and any(fresh.require(ref) != prior.require(ref) for ref in prior.key_union):
                raise RuntimeHostError("REVALIDATION_REQUIRED: input closure moved during discovery")
            return fresh

        root_path = "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"
        try:
            page = self._host._repository.read_exact_path(basis.pinned_campaign, root_path)
            if (not isinstance(page, Mapping) or type(page.get("schema_version")) is not int
                    or set(page) != {"schema_version", "campaign_id", "complete", "roots"}):
                raise RuntimeHostError("input protection root page is not a strict native carrier")
            roots = _root_mappings(page, self._host._campaign_id)
            owner_ref = NativeOwnerRef(promise.owner_kind, (promise.owner_id,))
            observation = expand({owner_ref})
            owner = self._input_payload(observation, owner_ref)
            if not promise.validate(campaign_id=promise.campaign_id, owner_kind=promise.owner_kind,
                                    owner_id=promise.owner_id, native_owner=owner):
                raise RuntimeHostError("input handoff promise no longer matches selected native owner")
            refs = {owner_ref}
            if promise.owner_kind == "runtime.intent_plan":
                plan_state = input_native_state(owner, "runtime.intent_plan")
                interaction_ref = NativeOwnerRef("runtime.interaction", (plan_state["interaction_id"],))
                refs.add(interaction_ref)
                observation = expand(refs)
                interaction = self._input_payload(observation, interaction_ref)
            else:
                interaction_ref = owner_ref
                interaction = owner
            state = validate_input_interaction(campaign_id=promise.campaign_id, interaction=interaction)
            if state["accepted_input_basis"]["repository_identity"] != self._host._repository.repository_identity():
                raise RuntimeHostError("retained input belongs to a different repository")
            refs.add(NativeOwnerRef("runtime.message", (state["input_message_id"],)))
            if "intent_plan_id" in state:
                refs.add(NativeOwnerRef("runtime.intent_plan", (state["intent_plan_id"],)))
            target = state.get("response_target")
            if target is not None:
                refs.add(NativeOwnerRef("runtime.resolution", (target["resolution_id"],)))
                refs.add(NativeOwnerRef("runtime.command", (target["root_command_id"],)))
                if "accepted_resume_ref" not in state:
                    refs.add(NativeOwnerRef("runtime.continuation", (target["continuation_id"],)))
            observation = expand(refs)
            plan = None
            native_basis_revisions: dict[NativeOwnerRef, str] = {}
            extra_ordering_refs: set[NativeOwnerRef] = set()
            extra_clauses: dict[str, Mapping[str, object]] = {}
            if "intent_plan_id" in state:
                plan = self._input_payload(observation, NativeOwnerRef("runtime.intent_plan", (state["intent_plan_id"],)))
                for clause in input_native_state(plan, "runtime.intent_plan")["clauses"]:
                    if "command_id" in clause:
                        refs.add(NativeOwnerRef("runtime.command", (clause["command_id"],)))
                        extra_clauses[clause["command_id"]] = clause
                    for dependency in clause.get("native_basis_refs", ()):
                        dependency_ref = NativeOwnerRef(dependency["family"], (dependency["id"],))
                        if "revision" not in dependency:
                            raise RuntimeHostError("input native-basis source revision is unavailable")
                        if (dependency_ref in native_basis_revisions
                                and native_basis_revisions[dependency_ref] != dependency["revision"]):
                            raise RuntimeHostError("input native-basis source revisions conflict")
                        native_basis_revisions[dependency_ref] = dependency["revision"]
                        refs.add(dependency_ref)
                    if "ordering_resolution_id" in clause:
                        extra_ordering_refs.add(NativeOwnerRef("runtime.resolution", (clause["ordering_resolution_id"],)))
                observation = expand(refs)
                for clause in input_native_state(plan, "runtime.intent_plan")["clauses"]:
                    if clause.get("material_exact_text_refs"):
                        raise RuntimeHostError("input exact natural-owner protection reader is unavailable")
            # Each populated extra K has its own execution owner. It never
            # inherits the earlier response root's result or protection proof.
            resolution_roots = {} if target is None else {target["resolution_id"]: target["root_command_id"]}
            extra_commands: dict[str, Mapping[str, object]] = {}
            direct_children: dict[str, Mapping[str, object]] = {}
            for identity in extra_clauses:
                command = native_command_state(self._input_payload(observation,
                    NativeOwnerRef("runtime.command", (identity,))), command_id=identity, campaign_id=promise.campaign_id)
                extra_commands[identity] = command
                if command["command_kind"] == "action":
                    resolution_roots[command["root_resolution_id"]] = identity
                else:
                    for segment in command.get("direct_transition_segments", ()):
                        if "continuation_id" in segment:
                            raise RuntimeHostError("direct segment Continuation source contract is unavailable")
                        refs.update(NativeOwnerRef("runtime.mechanical_event", (event_id,)) for event_id in segment["event_ids"])
                    invocations = list(command["pending_child_invocations"]) + [child
                        for segment in command.get("direct_transition_segments", ()) for child in segment["pending_child_invocations"]]
                    for child in invocations:
                        if "child_resolution_id" not in child:
                            raise RuntimeHostError("direct child requires its bounded native result mapping")
                        child_id = child["child_resolution_id"]
                        if child_id in direct_children and direct_children[child_id] != child:
                            raise RuntimeHostError("direct child native cause is ambiguous")
                        direct_children[child_id] = child
                        resolution_roots[child_id] = identity
            observation = expand(refs)
            observation, checked_resolutions = self._observe_retained_resolution_sources(session, observation, resolution_roots)
            refs.update(observation.key_union)
            action_children = {child["child_resolution_id"]: command for command in extra_commands.values()
                if command["command_kind"] == "action" for child in command["pending_child_invocations"]
                if "child_resolution_id" in child}
            remaining_children = {identity: command["command_id"] for identity, command in action_children.items()
                if NativeOwnerRef("runtime.resolution", (identity,)) not in checked_resolutions}
            if remaining_children:
                observation, checked_children = self._observe_retained_resolution_sources(session, observation, remaining_children)
                checked_resolutions.update(checked_children)
                refs.update(observation.key_union)
            for identity, command in action_children.items():
                if identity == command["root_resolution_id"]:
                    raise RuntimeHostError("action mandatory child cannot be its root Resolution")
                _validate_action_resolution_binding(command, identity, validate_retained_resolution(resolution_id=identity,
                    resolution=self._input_payload(observation, NativeOwnerRef("runtime.resolution", (identity,)))))
            for command in extra_commands.values():
                from .recovery import _validate_catalog_closure

                if not callable(getattr(self._host._repository, "resolve_recovery_catalog_context", None)):
                    raise RuntimeHostError("extra command accepted interpretation source is unavailable")
                bound = self._observe_command_input(command, required_owner_refs=tuple(refs), current_authority=False)
                if any(bound.require(ref) != observation.require(ref) for ref in observation.key_union):
                    raise RuntimeHostError("REVALIDATION_REQUIRED: extra command interpretation sources moved")
                refs.update(bound.key_union)
                observation = expand(refs)
                _validate_catalog_closure(self._host._repository, basis.pinned_campaign, command,
                    command["catalog_context"], input_observation=bound)
            # The response root cannot route extra units. A retained I or the
            # exact complete same-I P is the bounded survivor for *all* units,
            # including nonexecutables/held clauses with no K or native use yet.
            protected = {(root["owner_kind"], root["owner_id"]) for root in roots}
            if (("runtime.interaction", interaction["id"]) not in protected
                    and (plan is None or ("runtime.intent_plan", plan["id"]) not in protected)):
                raise RuntimeHostError("input lacks retained I/complete same-I Plan root protection")
            if ("runtime.interaction", interaction["id"]) not in protected:
                from .recovery_roots import validate_unresolved_input_owner

                validate_unresolved_input_owner(promise.campaign_id, "runtime.intent_plan", plan)
            records = {}
            if extra_ordering_refs - checked_resolutions:
                raise RuntimeHostError("input additional ordering protection closure is unavailable")
            for ref in observation.key_union:
                read = observation.require(ref)
                payload = self._input_payload(observation, ref)
                if isinstance(payload.get("state"), Mapping):
                    for field, value in payload["state"].items():
                        if field in payload and _operation_digest(payload[field]) != _operation_digest(value):
                            raise RuntimeHostError("input retained envelope/state projections conflict")
                if payload.get("campaign_id", promise.campaign_id) != promise.campaign_id:
                    raise RuntimeHostError("input retained dependency belongs to another campaign")
                if ref in native_basis_revisions and payload.get("revision") != native_basis_revisions[ref]:
                    raise RuntimeHostError("input native-basis source revision differs")
                if (read.source is not CurrentOwnerSource.PINNED_CAMPAIGN
                        or read.source_basis != basis.pinned_campaign.revision):
                    raise RuntimeHostError("input cross-source protection/freeze is unavailable")
                records[route_native_record(ref.family_key, ref.identity).relative_path] = payload
            # Use the existing cold reader on the observed union, never reload a
            # missing selected owner from older campaign bytes or a transcript.
            class ObservedSources:
                def read_exact_path(self, pin: object, path: str) -> object:
                    if pin != basis.pinned_campaign:
                        raise RuntimeHostError("input retention source pin differs")
                    native = records[path]
                    if native.get("kind") == "runtime.mechanical_event" and "state" in native:
                        return {**native["state"], "kind": native["kind"], "id": native["id"]}
                    return native

            _hydrate_input_root_closure(ObservedSources(), basis.pinned_campaign,
                self._input_payload(observation, owner_ref))
            for identity, command in extra_commands.items():
                prior_segment = None
                if "accepted_resume_ref" in state:
                    reference = state["accepted_resume_ref"]
                    prior = validate_retained_resolution(resolution_id=reference["resolution_id"],
                        resolution=self._input_payload(observation, NativeOwnerRef("runtime.resolution", (reference["resolution_id"],))))
                    prior_segment = next(segment for segment in prior["segments"] if segment["segment_id"] == reference["segment_id"])
                origin = accepted_input_origin(campaign_id=promise.campaign_id, interaction=interaction,
                    message=self._input_payload(observation, NativeOwnerRef("runtime.message", (state["input_message_id"],))),
                    plan=plan, clause_id=command["clause_id"], accepted_response_segment=prior_segment)
                if command["input_fingerprint"] != command_input_fingerprint(command, origin=origin):
                    raise RuntimeHostError("retained extra command interpretation/origin fingerprint differs")
                resolution = None
                if command["command_kind"] == "action":
                    resolution = validate_retained_resolution(resolution_id=command["root_resolution_id"],
                        resolution=self._input_payload(observation, NativeOwnerRef("runtime.resolution", (command["root_resolution_id"],))))
                    _validate_action_resolution_binding(command, command["root_resolution_id"], resolution)
                    if not resolution["segments"]:
                        raise RuntimeHostError("extra action native result closure is unavailable")
                result = _hydrate_execution_result(ObservedSources(), basis.pinned_campaign, command, resolution)
                if result is not None:
                    execution_result_identity(command, result)
                clause = extra_clauses[identity]
                if clause["execution_state"] == "intent.executed" and (command["disposition"] != "command.settled"
                        or result is None or result["status"] != "COMPLETED"):
                    raise RuntimeHostError("executed extra unit lacks actual completed native closure")
                if command["disposition"] == "command.settled" and (result is None
                        or result["status"] not in {"COMPLETED", "REJECTED", "ABORTED", "FAILED"}
                        or command["pending_child_invocations"]):
                    raise RuntimeHostError("settled extra command lacks terminal native closure")
                if command["disposition"] == "command.settled":
                    native_descendants = [validate_retained_resolution(resolution_id=ref.identity[0],
                        resolution=self._input_payload(observation, ref)) for ref in checked_resolutions]
                    fixed_child_causes = {descendant.get("causal_invocation_key") for descendant in native_descendants
                        if descendant["root_command_id"] == identity}
                    for ref in checked_resolutions:
                        descendant = validate_retained_resolution(resolution_id=ref.identity[0],
                            resolution=self._input_payload(observation, ref))
                        if descendant["root_command_id"] == identity and descendant["status"] not in {
                                "COMPLETED", "REJECTED", "ABORTED", "FAILED"}:
                            raise RuntimeHostError("settled extra command retains unfinished native descendants")
                        if descendant["root_command_id"] == identity and any(
                                child["firing_key"] not in fixed_child_causes for segment in descendant["segments"]
                                for child in segment["pending_child_invocations"]):
                            raise RuntimeHostError("settled extra command has an undiscovered mandatory native result")
            for child_id, cause in direct_children.items():
                child = validate_retained_resolution(resolution_id=child_id,
                    resolution=self._input_payload(observation, NativeOwnerRef("runtime.resolution", (child_id,))))
                if ("initiating_command_id" in child or child.get("causal_invocation_key") != cause["firing_key"]
                        or child["activity_id"] != cause["activity_id"] or child["root_command_id"] != cause["root_command_id"]):
                    raise RuntimeHostError("direct mandatory child lacks its exact native cause")
            for ref in observation.key_union:
                if ref.family_key == "runtime.command":
                    command = native_command_state(self._input_payload(observation, ref),
                        command_id=ref.identity[0], campaign_id=promise.campaign_id)
                    if target is not None and ref.identity[0] == target["root_command_id"]:
                        if command["command_kind"] != "action":
                            raise RuntimeHostError("response native action mapping is unavailable")
                        _validate_action_resolution_binding(command, target["resolution_id"], validate_retained_resolution(
                            resolution_id=target["resolution_id"], resolution=self._input_payload(observation,
                                NativeOwnerRef("runtime.resolution", (target["resolution_id"],)))))
            if not promise.validate(campaign_id=promise.campaign_id, owner_kind=promise.owner_kind,
                                    owner_id=promise.owner_id,
                                    native_owner=self._input_payload(observation, owner_ref)):
                raise RuntimeHostError("REVALIDATION_REQUIRED: input promise owner moved")
            if (not session.revalidate(observation)
                    or _operation_digest(page) != _operation_digest(
                        self._host._repository.read_exact_path(basis.pinned_campaign, root_path))):
                raise RuntimeHostError("REVALIDATION_REQUIRED: input retention sources moved")
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            if isinstance(exc, RuntimeHostError):
                raise
            raise RuntimeHostError("input retained content/protection closure is unavailable") from exc

    @staticmethod
    def _input_payload(observation: CurrentOwnerObservation, ref: NativeOwnerRef) -> Mapping[str, object]:
        read = observation.require(ref)
        if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
            raise InputAuthorityUnavailable(f"exact input source unavailable: {ref.family_key}/{ref.identity}")
        return read.payload

    def _input_adapter_principal(self, interaction: Mapping[str, object]) -> object:
        from .access_control import resolve_principal
        from .runtime_execution import validate_input_interaction

        adapter = self._host._accepted_input_capability
        if adapter is None:
            raise InputAuthorityUnavailable("accepted-input issuer is unavailable")
        state = validate_input_interaction(campaign_id=self._host._campaign_id, interaction=interaction)
        basis = state["accepted_input_basis"]
        repository_identity = self._host._repository.repository_identity()
        if (basis["repository_identity"] != repository_identity
                or basis["adapter_profile_id"] != adapter.adapter_profile_id
                or basis["adapter_profile_generation"] != adapter.adapter_profile_generation):
            raise InputAuthorityUnavailable("input repository/profile differs from trusted composition")
        key = {
            "repository_identity": repository_identity, "campaign_id": self._host._campaign_id,
            "adapter_profile_id": adapter.adapter_profile_id,
            "adapter_profile_generation": adapter.adapter_profile_generation,
            "accepted_exchange_key": basis["accepted_exchange_key"],
        }
        if adapter.lookup_exchange(**key) != interaction["id"]:
            raise InputAuthorityUnavailable("input exchange mapping is missing or conflicts")
        accepted_principal, text = adapter.accepted_representation(**key, host_invocation_ref=basis["host_invocation_ref"])
        accepted_principal = resolve_principal(accepted_principal)
        historical = basis["principal"]
        if (accepted_principal.provider != historical["provider"]
                or accepted_principal.stable_account_id != historical["stable_account_id"]
                or accepted_principal.login != historical["login_at_acceptance"]):
            raise InputAuthorityUnavailable("accepted account/representation mapping conflicts with native input")
        if not isinstance(text, str) or not text or hashlib.sha256(text.encode("utf-8")).hexdigest() != basis["representation"]["content_digest"]:
            raise InputAuthorityUnavailable("accepted representation/invocation differs from native input")
        return resolve_principal(adapter.current_principal(
            repository_identity=repository_identity, campaign_id=self._host._campaign_id,
        ))

    def _input_current_authority_sources(self, operation: _InputSourceOperation, principal: object) -> dict[str, object]:
        from .access_control import PrincipalPlayerRoute

        pin = self._host._begin_operation().pinned_campaign
        manifest = self._host._repository.read_exact_path(pin, "MANIFEST.yaml")
        if not isinstance(manifest, Mapping) or manifest.get("campaign_id") != self._host._campaign_id:
            raise InputAuthorityUnavailable("current campaign access source is missing or foreign")
        mode = manifest.get("mode")
        if mode == "singleplayer":
            return {"campaign_id": self._host._campaign_id, "mode": mode}
        if mode != "multiplayer":
            raise InputAuthorityUnavailable("current campaign access mode is unavailable")
        raw = self._host._repository.read_exact_path(pin, "STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml")
        if not isinstance(raw, Mapping) or type(raw.get("schema_version")) is not int:
            raise InputAuthorityUnavailable("complete current account route is unavailable")
        route = PrincipalPlayerRoute.from_mapping(raw)
        if route.campaign_id != self._host._campaign_id:
            raise InputAuthorityUnavailable("current account route has foreign campaign scope")
        players = manifest.get("players")
        ids = players.get("player_ids") if isinstance(players, Mapping) else None
        if (not isinstance(ids, (list, tuple)) or any(not isinstance(item, str) or not item for item in ids)
                or len(ids) != len(set(ids))):
            raise InputAuthorityUnavailable("campaign PLAYER membership is incomplete")
        nominated = {identity for entry in route.entries for identity in entry.candidate_player_ids}
        if nominated != set(ids):
            raise InputAuthorityUnavailable("account route omits or invents a campaign PLAYER")
        entry = route.for_account(principal.stable_account_id)
        if entry is None:
            raise InputAuthorityUnavailable("current principal has no native account route")
        # Preserve every finite nomination until exact bodies prove the complete
        # account association. The executor helper alone performs reduction.
        return {"campaign_id": self._host._campaign_id, "mode": mode,
            "route": route.as_mapping()}

    def _input_player_state(self, observation: CurrentOwnerObservation, player_id: str) -> Mapping[str, object]:
        from .runtime_execution import _input_wire

        owner = self._input_payload(observation, NativeOwnerRef("world.player", (player_id,)))
        if (owner.get("kind") != "world.player" or owner.get("id") != player_id
                or type(owner.get("schema_version")) is not int or owner["schema_version"] != 2
                or owner.get("campaign_id", self._host._campaign_id) != self._host._campaign_id):
            raise InputAuthorityUnavailable("native Player envelope is invalid")
        native = owner.get("state")
        _input_wire("world-player-state", native)
        if native["player_id"] != player_id:
            raise InputAuthorityUnavailable("native Player state/envelope identity differs")
        for field in native:
            if field in owner and _operation_digest(owner[field]) != _operation_digest(native[field]):
                raise InputAuthorityUnavailable("native Player flattened alias differs")
        return native

    def _validate_input_player_route(self, observation: CurrentOwnerObservation, authority: Mapping[str, object]) -> None:
        from .access_control import PlayerRecord, PrincipalPlayerRoute

        if authority["mode"] == "singleplayer":
            return
        route = PrincipalPlayerRoute.from_mapping(authority["route"])
        for entry in route.entries:
            for player_id in entry.candidate_player_ids:
                player = PlayerRecord.from_mapping(self._input_player_state(observation, player_id))
                if player.stable_account_id != entry.stable_account_id:
                    raise InputAuthorityUnavailable("complete account route differs from native Player binding")

    def _input_required_refs(
        self, command: Mapping[str, object], observation: CurrentOwnerObservation,
        authority: Mapping[str, object],
    ) -> set[NativeOwnerRef]:
        from .runtime_execution import input_source_owner_refs

        return set(input_source_owner_refs(command, observation, authority_sources=authority))

    @staticmethod
    def _input_command_subject(command: Mapping[str, object]) -> str:
        request = command.get("action_request")
        if command.get("command_kind") == "transition":
            from .runtime_execution import direct_input_contract

            return direct_input_contract(command)[0]
        if command.get("command_kind", "action") != "action" or not isinstance(request, Mapping):
            raise InputAuthorityUnavailable("command has no admitted source/control profile")
        return _nonempty_string(request.get("actor_id"), "command controlled subject")

    def _input_origin(self, command: Mapping[str, object], observation: CurrentOwnerObservation) -> Mapping[str, object]:
        from .runtime_execution import (
            accepted_input_origin,
            input_native_state,
            validate_input_resolution,
        )

        interaction = self._input_payload(observation, NativeOwnerRef("runtime.interaction", (command["interaction_id"],)))
        state = input_native_state(interaction, "runtime.interaction")
        message = self._input_payload(observation, NativeOwnerRef("runtime.message", (state["input_message_id"],)))
        plan = self._input_payload(observation, NativeOwnerRef("runtime.intent_plan", (command["intent_plan_id"],)))
        reference = state.get("accepted_resume_ref")
        segment = None
        if isinstance(reference, Mapping):
            owner = self._input_payload(observation, NativeOwnerRef("runtime.resolution", (reference["resolution_id"],)))
            native = validate_input_resolution(resolution_id=reference["resolution_id"], resolution=owner)
            if "campaign_id" in owner and owner["campaign_id"] != self._host._campaign_id:
                raise InputAuthorityUnavailable("mixed prior response has a foreign campaign projection")
            if native.get("root_command_id") != state["response_target"]["root_command_id"]:
                raise InputAuthorityUnavailable("mixed prior response has a foreign root")
            matches = [item for item in native.get("segments", ()) if isinstance(item, Mapping) and item.get("segment_id") == reference["segment_id"]]
            if len(matches) != 1:
                raise InputAuthorityUnavailable("mixed prior response marker is missing or ambiguous")
            segment = matches[0]
        origin = accepted_input_origin(campaign_id=self._host._campaign_id, interaction=interaction,
            message=message, plan=plan, clause_id=command["clause_id"], accepted_response_segment=segment)
        clauses = input_native_state(plan, "runtime.intent_plan")["clauses"]
        clause = next(item for item in clauses if item["clause_id"] == command["clause_id"])
        if "command_id" in clause and clause["command_id"] != command["command_id"]:
            raise InputAuthorityUnavailable("native clause/command reciprocity differs")
        return origin

    def _input_current_control(self, command, observation, principal, authority) -> None:
        from .access_control import authorize_operation, resolve_player
        from .runtime_execution import input_native_state

        interaction = self._input_payload(observation, NativeOwnerRef("runtime.interaction", (command["interaction_id"],)))
        state = input_native_state(interaction, "runtime.interaction")
        origin = state["accepted_input_basis"]
        if principal.stable_account_id != origin["principal"]["stable_account_id"]:
            raise InputAuthorityUnavailable("current executor has no native voluntary-input mapping")
        subject = self._input_command_subject(command)
        if state["input_kind"] == "intent" and subject not in origin["authority_at_acceptance"]["accepted_subject_ids"]:
            raise InputAuthorityUnavailable("historical input did not authorize the command subject")
        if authority["mode"] == "singleplayer":
            history_observation = self._host.history.observe_first_initialization_history()
            evidence = history_observation.evidence
            decision = authorize_operation(principal, operation="creator_write", creator_provenance=evidence,
                campaign_id=self._host._campaign_id)
            if not decision.authorized:
                raise InputAuthorityUnavailable("creator.uncertain")
            historical = origin["authority_at_acceptance"]
            if historical["kind"] == "creator_singleplayer":
                actual = {"author_login": evidence.author_login,
                    "initialization_revision": evidence.initialization_revision,
                    "parent_revision": evidence.parent_revision}
                if _operation_digest(actual) != _operation_digest(historical["creator_history"]):
                    raise InputAuthorityUnavailable("creator historical initialization source differs")
            return

        def load_player(player_id):
            return self._input_player_state(observation, player_id)

        resolution = resolve_player(principal, authority["route"], load_player, campaign_id=self._host._campaign_id)
        decision = authorize_operation(principal, resolution, operation="gameplay", campaign_id=self._host._campaign_id)
        if not decision.authorized or resolution.player is None or subject not in resolution.player.controlled_pc_ids:
            raise InputAuthorityUnavailable("current Player purpose/control is not authorized")

    def _validate_command_input_observation(
        self, observation: CurrentOwnerObservation, command: Mapping[str, object],
        *, current_authority: bool = True,
    ) -> Mapping[str, object]:
        if type(current_authority) is not bool:
            raise RuntimeHostError("input validation purpose must be explicit")
        try:
            operation = observation.operation_token
            if (type(observation) is not CurrentOwnerObservation or type(operation) is not _InputSourceOperation
                    or operation.host is not self._host or operation.host_token is not self._host._basis_token
                    or type(operation.session) is not CurrentOwnerReadSession
                    or operation.session.observation is not observation
                    or operation.session.operation_token is not operation
                    or getattr(operation.session._reader, "__self__", None) is not self._host
                    or getattr(operation.session._reader, "__func__", None) is not RuntimeHost._read_current_owner_path
                    or getattr(operation.session._source_basis_reader, "__self__", None) is not self._host
                    or getattr(operation.session._source_basis_reader, "__func__", None) is not RuntimeHost._read_current_owner_basis
                    or getattr(operation.session._live_reader, "__self__", None) is not self._host
                    or getattr(operation.session._live_reader, "__func__", None) is not RuntimeHost._read_current_owner_live
                    or operation.session._hot_store is not self._host._hot_store
                    or operation.session._pinned_campaign is not operation.basis.pinned_campaign
                    or operation.session._selected_live is not operation.basis.selected_live
                    or self._input_session_configuration(operation) != operation.session_configuration):
                raise InputAuthorityUnavailable("input observation is not this Host's exact current source session")
            session = operation.session
            if not session.revalidate(observation):
                raise InputAuthorityUnavailable("REVALIDATION_REQUIRED: input owner source moved")
            interaction = self._input_payload(observation, NativeOwnerRef("runtime.interaction", (command["interaction_id"],)))
            principal = self._input_adapter_principal(interaction)
            authority = self._input_current_authority_sources(operation, principal)
            if _operation_digest(authority) != _operation_digest(operation.authority_sources):
                raise InputAuthorityUnavailable("REVALIDATION_REQUIRED: current authority source moved")
            if not self._input_required_refs(command, observation, authority) <= set(observation.key_union):
                raise InputAuthorityUnavailable("input observation omits required native source owners")
            self._validate_input_player_route(observation, authority)
            origin = self._input_origin(command, observation)
            if current_authority and command.get("command_kind") == "transition":
                from .runtime_execution import validate_direct_input_sources

                validate_direct_input_sources(command, observation)
            if current_authority:
                self._input_current_control(command, observation, principal, authority)
            if not session.revalidate(observation):
                raise InputAuthorityUnavailable("REVALIDATION_REQUIRED: input source changed during authority validation")
            return origin
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            if isinstance(exc, RuntimeHostError):
                raise
            raise InputAuthorityUnavailable("native input source/authority revalidation failed") from exc

    def begin(self, basis: _OperationBasis) -> CurrentOwnerReadSession:
        operation = self._host._operation_basis(basis)
        return CurrentOwnerReadSession(
            campaign_id=self._host._campaign_id,
            operation_token=operation,
            pinned_campaign=operation.pinned_campaign,
            selected_live=operation.selected_live,
            hot_store=self._host._hot_store,
            reader=self._host._read_current_owner_path,
            source_basis_reader=self._host._read_current_owner_basis,
            live_reader=self._host._read_current_owner_live,
        )

    def _prepare_root_context(
        self,
        catalog: AdmittedActivityCatalog,
        compiled: CompiledActivity,
        *,
        command_id: str,
        consumer_id: str,
        adjudication_basis: AcceptedAdjudicationBasis | None = None,
    ) -> NativePreparationContext:
        """Issue one read-only preparation from the exact accepted native root."""
        from . import activity_contracts as contracts
        from . import mechanical_context
        from .policy_basis import PolicyBasisResolutionError
        from .runtime_execution import (
            CommandAcceptanceError,
            validate_execution_proposal,
        )

        if not isinstance(command_id, str) or not command_id:
            raise RuntimeHostError("root preparation requires a command identity")
        if (
            type(catalog) is not contracts.AdmittedActivityCatalog
            or not contracts._compiler_value_is_issued(catalog, kind="catalog")
            or type(compiled) is not contracts.CompiledActivity
            or not contracts._compiler_value_is_issued(
                compiled, kind="compiled", parent=catalog.catalog_context
            )
            or catalog.compiled_activities.get(compiled.activity_id) is not compiled
        ):
            raise RuntimeHostError(
                "root preparation requires exact compiler-issued catalog handles"
            )
        try:
            mechanical_context._instruction(compiled, consumer_id)
        except mechanical_context.MechanicalContextError as error:
            raise RuntimeHostError("root preparation consumer is not compiler-issued") from error

        placeholder = contracts.ExecutionRef(command_id, command_id)
        operation = self._host._begin_operation()
        session = self.begin(operation)
        command_ref = NativeOwnerRef("runtime.command", (command_id,))
        command_read = session.read(command_ref)
        if command_read.status is not CurrentOwnerStatus.RESOLVED:
            status = (
                "REVALIDATION_REQUIRED"
                if command_read.status is CurrentOwnerStatus.REVALIDATION_REQUIRED
                else "AUTHORITY_UNAVAILABLE"
            )
            raise contracts.NativePreparationHold(status, placeholder, ())
        command_payload = command_read.payload
        if not isinstance(command_payload, Mapping):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", placeholder, ()
            )
        try:
            accepted_command = contracts._preparation_owner_state(
                command_payload,
                family="runtime.command",
                owner_id=command_id,
                campaign_id=self._host._campaign_id,
            )
            contracts._wire_contract("runtime-command-state", accepted_command)
        except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", placeholder, ()
            ) from error
        root_resolution_id = accepted_command.get("root_resolution_id")
        if not isinstance(root_resolution_id, str) or not root_resolution_id:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", placeholder, ()
            )
        execution_ref = contracts.ExecutionRef(command_id, root_resolution_id)
        request = accepted_command.get("action_request")
        if (
            accepted_command.get("command_kind") != "action"
            or accepted_command.get("disposition") != "command.accepted"
            or accepted_command.get("pending_child_invocations")
            or not isinstance(request, Mapping)
            or request.get("activity_id") != compiled.activity_id
            or request.get("source_id") is not None
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            )
        if adjudication_basis is None:
            if request.get("parameter_bindings", {}) or accepted_command.get(
                "invocation_facts"
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", execution_ref, ()
                )
            accepted_adjudication = ()
            policy_refs: tuple[str, ...] = ()
        else:
            if not contracts.is_accepted_basis_issued(adjudication_basis):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", execution_ref, ()
                )
            try:
                contracts.validate_policy_applicability_witnesses(
                    adjudication_basis.verified_policies,
                    compiled.activity_id,
                    catalog.catalog_context,
                )
            except PolicyBasisResolutionError as error:
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", execution_ref, ()
                ) from error
            if (
                adjudication_basis.runtime_parameter_bindings()
                != request.get("parameter_bindings", {})
                or contracts._thaw(adjudication_basis.runtime_invocation_facts())
                != contracts._thaw(accepted_command.get("invocation_facts", []))
            ):
                raise contracts.NativePreparationHold(
                    "AUTHORITY_UNAVAILABLE", execution_ref, ()
                )
            accepted_adjudication = (adjudication_basis,)
            policy_refs = tuple(
                sorted(
                    {
                        policy.policy_id
                        for policy in adjudication_basis.verified_policies
                    }
                )
            )
        accepted_facts = accepted_command.get("invocation_facts", [])
        if not isinstance(accepted_facts, (list, tuple)):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            )
        accepted_fact_refs = tuple(
            sorted(
                {
                    fact["fact_id"]
                    for fact in accepted_facts
                    if isinstance(fact, Mapping)
                    and isinstance(fact.get("fact_id"), str)
                }
            )
        )
        try:
            role_bindings = contracts._derive_root_role_bindings(
                compiled, accepted_command
            )
        except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            ) from error

        resolution_ref = NativeOwnerRef(
            "runtime.resolution", (root_resolution_id,)
        )
        try:
            observation = self._observe_command_input(accepted_command,
                required_owner_refs=(command_ref, resolution_ref, *role_bindings.values()))
            session = observation.operation_token.session
            validate_execution_proposal(accepted_command, catalog.catalog_context,
                {"definition_id": compiled.activity_id, "kind": "definition.activity"},
                input_observation=observation)
        except (RuntimeHostError, CommandAcceptanceError, KeyError, TypeError, ValueError) as error:
            raise contracts.NativePreparationHold("AUTHORITY_UNAVAILABLE", execution_ref, ()) from error
        for owner_ref in observation.key_union:
            read = observation.require(owner_ref)
            if read.status is not CurrentOwnerStatus.RESOLVED or read.payload is None:
                status = (
                    "REVALIDATION_REQUIRED"
                    if read.status is CurrentOwnerStatus.REVALIDATION_REQUIRED
                    else "AUTHORITY_UNAVAILABLE"
                )
                raise contracts.NativePreparationHold(status, execution_ref, ())
        command_read = observation.require(command_ref)
        resolution_read = observation.require(resolution_ref)
        if (
            command_read.payload is None
            or command_read.payload.get("kind") != "runtime.command"
            or command_read.payload.get("command_id") != command_id
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            )
        try:
            final_command_state = contracts._preparation_owner_state(
                command_read.payload,
                family="runtime.command",
                owner_id=command_id,
                campaign_id=self._host._campaign_id,
            )
        except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            ) from error
        if final_command_state != contracts._thaw(accepted_command):
            raise contracts.NativePreparationHold(
                "REVALIDATION_REQUIRED", execution_ref, ()
            )
        try:
            resolution = contracts._preparation_owner_state(
                resolution_read.payload,
                family="runtime.resolution",
                owner_id=root_resolution_id,
                campaign_id=self._host._campaign_id,
            )
            contracts._wire_contract("runtime-resolution-state", resolution)
        except (contracts.ActivityContractError, KeyError, TypeError, ValueError) as error:
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            ) from error

        if (
            resolution.get("root_command_id") != command_id
            or resolution.get("initiating_command_id") != command_id
            or resolution.get("activity_id") != compiled.activity_id
            or resolution.get("actor_id") != request.get("actor_id")
            or resolution.get("target_ids", []) != request.get("target_ids", [])
            or resolution.get("parameter_bindings", {})
            != request.get("parameter_bindings", {})
            or resolution.get("invocation_facts", []) != accepted_facts
            or resolution.get("ruleset_set_digest_generation")
            != compiled.ruleset_set_digest_generation
            or resolution.get("ruleset_set_sha256") != compiled.ruleset_set_sha256
            or resolution.get("catalog_context_fingerprint_generation")
            != compiled.catalog_context_fingerprint_generation
            or resolution.get("catalog_context_fingerprint")
            != compiled.catalog_context_fingerprint
            or resolution.get("status") != "RUNNING"
            or resolution.get("next_segment_sequence") != 1
            or resolution.get("segments")
            or resolution.get("fixed_rng_results")
            or resolution.get("prior_step_exports")
            or resolution.get("child_resolution_ids")
            or resolution.get("causal_invocation_key") is not None
            or resolution.get("procedure_id") is not None
            or resolution.get("continuation_id") is not None
            or resolution.get("trace_id") is not None
            or resolution.get("stochastic_state") is not None
            or resolution.get("reconciliation_state") is not None
        ):
            raise contracts.NativePreparationHold(
                "AUTHORITY_UNAVAILABLE", execution_ref, ()
            )

        context = contracts.NativePreparationContext(
            catalog=catalog,
            compiled=compiled,
            consumer_id=consumer_id,
            occurrence_id=contracts._root_preparation_occurrence_id(
                root_resolution_id, consumer_id
            ),
            execution_ref=execution_ref,
            observation=observation,
            owner_session=session,
            role_bindings=role_bindings,
            accepted_command=accepted_command,
            resolution=resolution,
            accepted_fact_refs=accepted_fact_refs,
            accepted_adjudication=accepted_adjudication,
            policy_refs=policy_refs,
            fixed_roll_refs=(),
            prospective_owner_documents=(),
            allocation_handles=(),
            _builder_token=session.operation_token,
            _issue_seal=contracts._CONTRACT_SEAL,
        )
        contracts._register_preparation_context(context, issuer=self)
        return context


class ActorContinuityService(_BoundService):
    """One trusted ACTOR-phase join for native NPC self-state reconsideration."""

    __slots__ = ()

    def establish_from_phase(
        self, envelope: object, phase_result: object
    ) -> ActorContinuityEstablishmentResult:
        from . import actor_continuity, turn_runtime

        actor_id = (
            phase_result.subject_id
            if type(phase_result) is turn_runtime.AcceptedPhaseResult
            else None
        )
        try:
            owner_ref = (
                NativeOwnerRef("world.actor", (actor_id,))
                if isinstance(actor_id, str) and actor_id
                else None
            )
        except ValueError:
            owner_ref = None
        try:
            basis, accepted_payload = turn_runtime.require_current_actor_phase_result(
                envelope,
                phase_result,
                context_service=self._host._context,
            )
        except (TypeError, ValueError, KeyError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
            )
        if (
            owner_ref is None
            or basis.subject_id != actor_id
            or basis.role != "ACTOR"
            or basis.purpose != "assess"
            or basis.profile_id != "profile.actor"
            or basis.source_frontier != envelope.get("accepted_frontier")
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )

        try:
            operation = self._host._begin_operation()
        except RuntimeHostError:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )
        if (
            operation.pinned_campaign.campaign_id != self._host._campaign_id
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )
        try:
            live_authority = lookup_write_authority(
                "world.actor", actor_id, operation.selected_live
            )
        except (TypeError, ValueError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )
        if live_authority is WriteAuthority.LIVE:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED, owner_ref
            )
        if live_authority is WriteAuthority.INTEGRITY_CONFLICT:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )

        session = self._host._current_owner.begin(operation)
        try:
            observation = session.require((owner_ref,))
            current_read = observation.require(owner_ref)
        except (TypeError, ValueError, RuntimeHostError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )
        if (
            current_read.status is not CurrentOwnerStatus.RESOLVED
            or current_read.payload is None
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )

        actor_record = deepcopy(dict(current_read.payload))
        try:
            native_actor = actor_continuity.validate_actor_source(actor_record)
        except (TypeError, ValueError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED, owner_ref
            )
        before_revision = native_actor["state_revision"]
        if (
            actor_record.get("schema_version") != 2
            or actor_record.get("id") != actor_id
            or current_read.generation != before_revision
            or current_read.source_basis is None
            or current_read.predecessor_fingerprint is None
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )

        basis_actor = _actor_from_context_basis(basis.bundle, actor_id)
        if basis_actor is None or basis_actor != actor_record:
            consumed = self._host._hot_store._lookup_actor_phase_consumption(
                self._host._campaign_id,
                "world.actor",
                (actor_id,),
                phase_result,
                self._host._basis_token,
            )
            if consumed is not None:
                prior_result, prior_fingerprint = consumed
                if (
                    current_read.fingerprint == prior_fingerprint
                    and session.revalidate(observation)
                ):
                    return prior_result  # type: ignore[return-value]
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )

        consumed = self._host._hot_store._lookup_actor_phase_consumption(
            self._host._campaign_id,
            "world.actor",
            (actor_id,),
            phase_result,
            self._host._basis_token,
        )
        if consumed is not None:
            prior_result, prior_fingerprint = consumed
            if (
                current_read.fingerprint == prior_fingerprint
                and session.revalidate(observation)
            ):
                return prior_result  # type: ignore[return-value]
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )

        roles = native_actor["state"].get("roles", [])
        if (
            not isinstance(roles, Sequence)
            or isinstance(roles, (str, bytes))
            or "actor.nonplayer_character" not in roles
            or "actor.player_character" in roles
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )

        proposal = _parse_actor_reconsideration(accepted_payload.get("proposal"))
        if proposal is None:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )
        evolving = native_actor["state"].get("continuity", {}).get("evolving", {})
        cues = (
            evolving.get("reconsideration_cues")
            if isinstance(evolving, Mapping)
            else None
        )
        if (
            not isinstance(cues, Sequence)
            or isinstance(cues, (str, bytes))
            or not any(proposal["reconsideration_cue"] == cue for cue in cues)
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )

        delta = proposal["delta"]
        if delta is not None and not _bounded_actor_reconsideration_delta(
            delta, actor_id, before_revision
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )
        if not session.revalidate(observation):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )

        try:
            latest_operation = self._host._begin_operation()
            latest_authority = lookup_write_authority(
                "world.actor", actor_id, latest_operation.selected_live
            )
        except (RuntimeHostError, TypeError, ValueError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )
        if latest_authority is WriteAuthority.LIVE:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )
        if latest_authority is WriteAuthority.INTEGRITY_CONFLICT:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )
        latest_session = self._host._current_owner.begin(latest_operation)
        try:
            latest_observation = latest_session.require((owner_ref,))
            latest_read = latest_observation.require(owner_ref)
        except (TypeError, ValueError, RuntimeHostError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )
        if (
            latest_read.status is not CurrentOwnerStatus.RESOLVED
            or latest_read.payload != actor_record
            or latest_read.generation != current_read.generation
            or latest_read.predecessor_fingerprint
            != current_read.predecessor_fingerprint
            or not latest_session.revalidate(latest_observation)
        ):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )

        # This legacy evidence mapping is deterministic and private to the native
        # owner join; phase sealing alone never sets its acceptance flags.
        source_evidence = [
            {
                "ref": actor_id,
                "accepted": True,
                "current": True,
                "authorized_actor_ids": [actor_id],
            }
        ]
        try:
            assessment = actor_continuity.assess_actor(
                {
                    "actor": actor_record,
                    "purpose": "assessment.reconsider",
                    "source_evidence": source_evidence,
                    "delta": delta,
                }
            )
            if assessment["disposition"] == "assessment.no_change":
                result = _actor_establishment_result(
                    ActorContinuityEstablishmentStatus.NO_CHANGE,
                    owner_ref,
                    before_revision,
                    before_revision,
                )
                try:
                    self._host._hot_store._consume_actor_no_change(
                        campaign_id=self._host._campaign_id,
                        identity=(actor_id,),
                        expected_snapshot=observation._hot_snapshot,
                        phase_result=phase_result,
                        host_token=self._host._basis_token,
                        result=result,
                        source_fingerprint=current_read.fingerprint,
                    )
                except StaleOwnerGeneration:
                    return _actor_establishment_result(
                        ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                        owner_ref,
                        before_revision,
                    )
                return result
            after_image = actor_continuity.apply_actor_delta(
                actor_record, delta, source_evidence
            )
        except (TypeError, ValueError):
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.UNSUPPORTED,
                owner_ref,
                before_revision,
            )

        if after_image["state"] == native_actor["state"]:
            result = _actor_establishment_result(
                ActorContinuityEstablishmentStatus.NO_CHANGE,
                owner_ref,
                before_revision,
                before_revision,
            )
            try:
                self._host._hot_store._consume_actor_no_change(
                    campaign_id=self._host._campaign_id,
                    identity=(actor_id,),
                    expected_snapshot=observation._hot_snapshot,
                    phase_result=phase_result,
                    host_token=self._host._basis_token,
                    result=result,
                    source_fingerprint=current_read.fingerprint,
                )
            except StaleOwnerGeneration:
                return _actor_establishment_result(
                    ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                    owner_ref,
                    before_revision,
                )
            return result

        after_revision = after_image["state_revision"]
        result = _actor_establishment_result(
            ActorContinuityEstablishmentStatus.ESTABLISHED,
            owner_ref,
            before_revision,
            after_revision,
        )
        document = OwnerDocument(
            campaign_id=self._host._campaign_id,
            family_key="world.actor",
            identity=(actor_id,),
            payload=after_image,
            source_basis=current_read.source_basis,
            generation=after_revision,
        )
        try:
            self._host._hot_store._establish_actor_owner(
                document,
                observation._hot_snapshot,
                phase_result=phase_result,
                host_token=self._host._basis_token,
                establishment_result=result,
                source_fingerprint=current_read.predecessor_fingerprint,
            )
        except StaleOwnerGeneration:
            return _actor_establishment_result(
                ActorContinuityEstablishmentStatus.REVALIDATION_REQUIRED,
                owner_ref,
                before_revision,
            )
        return result


def _actor_establishment_result(
    status: ActorContinuityEstablishmentStatus,
    owner_ref: NativeOwnerRef | None,
    before_revision: int | None = None,
    after_revision: int | None = None,
) -> ActorContinuityEstablishmentResult:
    return ActorContinuityEstablishmentResult(
        status=status,
        owner_ref=owner_ref,
        before_state_revision=before_revision,
        after_state_revision=after_revision,
    )


def _actor_from_context_basis(
    bundle: Mapping[str, object], actor_id: str
) -> dict[str, object] | None:
    if any(
        bundle.get(field) != expected
        for field, expected in (
            ("role", "ACTOR"),
            ("purpose", "assess"),
            ("profile_id", "profile.actor"),
            ("subject_id", actor_id),
        )
    ):
        return None
    candidates: list[Mapping[str, object]] = []
    for section in ("required", "optional"):
        rows = bundle.get(section)
        if rows is None:
            continue
        if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
            return None
        candidates.extend(row for row in rows if isinstance(row, Mapping))
    matches = [
        candidate
        for candidate in candidates
        if candidate.get("owner_family") == "world.actor"
        and candidate.get("owner_identity") == [actor_id]
    ]
    if len(matches) != 1 or not isinstance(matches[0].get("payload"), Mapping):
        return None
    return deepcopy(dict(matches[0]["payload"]))


def _parse_actor_reconsideration(value: object) -> dict[str, object] | None:
    if not isinstance(value, str):
        return None

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, item in pairs:
            if key in result:
                raise ValueError("Actor reconsideration proposal contains duplicate keys")
            result[key] = item
        return result

    try:
        proposal = json.loads(value, object_pairs_hook=unique_object)
    except (json.JSONDecodeError, TypeError, ValueError):
        return None
    if (
        not isinstance(proposal, dict)
        or set(proposal) != {"assessment_purpose", "reconsideration_cue", "delta"}
        or proposal.get("assessment_purpose") != "assessment.reconsider"
        or not isinstance(proposal.get("reconsideration_cue"), Mapping)
    ):
        return None
    delta = proposal.get("delta")
    if delta is not None and not isinstance(delta, Mapping):
        return None
    return {
        "assessment_purpose": "assessment.reconsider",
        "reconsideration_cue": deepcopy(dict(proposal["reconsideration_cue"])),
        "delta": deepcopy(dict(delta)) if isinstance(delta, Mapping) else None,
    }


def _bounded_actor_reconsideration_delta(
    value: Mapping[str, object], actor_id: str, state_revision: int
) -> bool:
    if set(value) != {
        "actor_id",
        "expected_state_revision",
        "purpose",
        "source_refs",
        "changes",
    }:
        return False
    if (
        value.get("actor_id") != actor_id
        or type(value.get("expected_state_revision")) is not int
        or value.get("expected_state_revision") != state_revision
        or value.get("purpose") != "assessment.reconsider"
        or value.get("source_refs") != [actor_id]
    ):
        return False
    changes = value.get("changes")
    if not isinstance(changes, Mapping) or set(changes) != {"continuity"}:
        return False
    continuity = changes.get("continuity")
    if not isinstance(continuity, Mapping) or set(continuity) != {"evolving"}:
        return False
    evolving = continuity.get("evolving")
    return isinstance(evolving, Mapping) and bool(evolving)


class HistoryService(_BoundService):
    """Fixed route to native history; it is a sibling of ContextService."""

    __slots__ = ()

    def discover(self, request: HistoryDiscoveryRequest) -> HistoryDiscoveryResult:
        """Bounded campaign/LIVE preparation; HOT producer dependency remains held."""
        from .history import _discover_bound_history

        return _discover_bound_history(self._host, request)

    def read_candidate(
        self, result: HistoryDiscoveryResult, candidate: NativeHistoryCandidate
    ) -> NativeSemanticEvent:
        """Exact native evidence only from this Host's retained shortlist."""
        from .history import _read_discovery_candidate

        return _read_discovery_candidate(self._host, result, candidate)

    def read(self, *, origin: str = "LOCAL") -> object:
        """Read a bounded native evt window through this host's fresh basis."""

        basis = self._host._begin_operation()
        return self._read_from_basis(basis, origin=origin)

    def _read_from_basis(
        self, basis: _OperationBasis, *, origin: str = "LOCAL"
    ) -> object:
        from .history import _read_bound_native_history

        return _read_bound_native_history(
            source_adapter=self._host._semantic_events,
            basis=basis,
            origin=origin,
        )

    def recover(self, *, origin: str = "LOCAL") -> object:
        """Recover by re-reading the same bound native source route."""

        return self.read(origin=origin)

    def observe_first_initialization_history(self):
        self._host._begin_operation()
        from .history import observe_first_initialization_history

        return observe_first_initialization_history(
            self._host._repository, self._host._campaign_id
        )


class NativeOrderingService(_BoundService):
    """Fixed route to the Step-3 runtime-execution ordered-owner producer."""

    __slots__ = ()

    def resolve(self, request: object) -> NativeOrderingResult | object:
        basis = self._host._begin_operation()
        try:
            from . import runtime_execution
        except ModuleNotFoundError as exc:
            raise RuntimeHostError("runtime execution owner is unavailable") from exc

        resolver = getattr(runtime_execution, "resolve_native_ordering_evidence", None)
        if not callable(resolver):
            return NativeOrderingResult(
                status=NativeOrderingStatus.NO_ORDERED_OWNER,
                campaign_id=basis.pinned_campaign.campaign_id,
            )
        return resolver(
            request,
            repository=self._host._repository,
            campaign_pin=basis.pinned_campaign,
            selected_live=basis.selected_live,
        )


class RuntimeHost:
    """Ephemeral root for exactly one selected campaign.

    Construction is an infrastructure operation.  Once constructed, every
    normal attribute assignment and deletion is rejected; callers cannot
    replace the repository, selected-LIVE transport or sibling services.
    """

    __slots__ = (
        "_accepted_input_capability",
        "_actor_continuity",
        "_basis_token",
        "_campaign_id",
        "_context",
        "_current_owner",
        "_history",
        "_hot_store",
        "_live_transport",
        "_native_ordering",
        "_publication",
        "_publication_transport",
        "_repository",
        "_semantic_events",
    )

    def __init__(
        self,
        selected_campaign_id: str,
        authenticated_repository_port: RepositoryPort,
        selected_live_transport: SelectedLiveTransport,
        campaign_publication_transport: CampaignPublicationTransport | None = None,
        hot_owner_store: HotOwnerStorePort | None = None,
        *,
        accepted_input_capability: AcceptedInputCapability | None = None,
    ) -> None:
        campaign_id = _require_nonempty_campaign_id(selected_campaign_id)
        if accepted_input_capability is not None:
            _require_operations(accepted_input_capability,
                ("lookup_exchange", "accepted_representation", "current_principal"),
                "accepted-input infrastructure capability")
            _nonempty_string(accepted_input_capability.adapter_profile_id, "input adapter profile")
            if type(accepted_input_capability.adapter_profile_generation) is not int or accepted_input_capability.adapter_profile_generation < 1:
                raise RuntimeHostError("input adapter profile generation is invalid")
        object.__setattr__(self, "_accepted_input_capability", accepted_input_capability)
        _require_operations(
            authenticated_repository_port,
            _REPOSITORY_OPERATIONS,
            "authenticated RepositoryPort",
        )
        _require_operations(
            selected_live_transport, (_LIVE_OPERATION,), "selected-LIVE transport"
        )
        if campaign_publication_transport is not None:
            _require_operations(
                campaign_publication_transport,
                _PUBLICATION_OPERATIONS,
                "campaign publication transport",
            )
            _validate_transport_repository_identity(
                authenticated_repository_port, campaign_publication_transport
            )
        hot_store = NativeHotStore(":memory:") if hot_owner_store is None else hot_owner_store
        _require_operations(
            hot_store,
            (
                "read_admitted_snapshot",
                "_lookup_actor_phase_consumption",
                "_establish_actor_owner",
                "_consume_actor_no_change",
            ),
            "infrastructure HOT owner store",
        )
        object.__setattr__(self, "_campaign_id", campaign_id)
        object.__setattr__(self, "_basis_token", object())
        object.__setattr__(self, "_repository", authenticated_repository_port)
        object.__setattr__(self, "_live_transport", selected_live_transport)
        object.__setattr__(self, "_hot_store", hot_store)
        object.__setattr__(
            self, "_publication_transport", campaign_publication_transport
        )
        object.__setattr__(self, "_context", ContextService(self))
        object.__setattr__(self, "_current_owner", CurrentOwnerView(self))
        object.__setattr__(self, "_actor_continuity", ActorContinuityService(self))
        object.__setattr__(self, "_history", HistoryService(self))
        object.__setattr__(self, "_native_ordering", NativeOrderingService(self))
        object.__setattr__(self, "_publication", CampaignPublicationService(self))
        object.__setattr__(self, "_semantic_events", SemanticEventSourceAdapter(self))

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise AttributeError(f"runtime host binding {name!r} is immutable")

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError(f"runtime host binding {name!r} cannot be deleted")

    def __reduce__(self) -> NoReturn:
        raise TypeError("RuntimeHost is ephemeral and cannot be serialized")

    def __reduce_ex__(self, protocol: int) -> NoReturn:
        raise TypeError("RuntimeHost is ephemeral and cannot be serialized")

    @property
    def campaign_id(self) -> str:
        return self._campaign_id

    @property
    def context(self) -> ContextService:
        return self._context

    @property
    def actor_continuity(self) -> ActorContinuityService:
        return self._actor_continuity

    @property
    def history(self) -> HistoryService:
        return self._history

    @property
    def native_ordering(self) -> NativeOrderingService:
        return self._native_ordering

    @property
    def publication(self) -> CampaignPublicationService:
        return self._publication

    @property
    def semantic_events(self) -> SemanticEventSourceAdapter:
        return self._semantic_events

    def _begin_operation(self) -> _OperationBasis:
        try:
            pinned = self._repository.pin_campaign(self._campaign_id)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("campaign pinning failed") from exc
        pinned_campaign = _validate_pinned_campaign(pinned, self._campaign_id)
        try:
            selected_live = self._live_transport.read_selected_live(
                self._campaign_id, pinned_campaign
            )
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("selected-LIVE currentness read failed") from exc
        return _OperationBasis(
            pinned_campaign=pinned_campaign,
            selected_live=_validate_selected_live(selected_live, self._campaign_id),
            host_token=self._basis_token,
        )

    def _operation_basis(self, value: _OperationBasis | None) -> _OperationBasis:
        if value is None:
            return self._begin_operation()
        if (
            not isinstance(value, _OperationBasis)
            or value.host_token is not self._basis_token
            or value.pinned_campaign.campaign_id != self._campaign_id
        ):
            raise RuntimeHostError("operation basis belongs to another runtime host")
        return value

    def _read_current_owner_path(
        self, pinned: PinnedCampaign, path: str
    ) -> object:
        try:
            return self._repository.read_exact_path(pinned, path)
        except KeyError:
            raise
        except (AttributeError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError(f"exact current-owner read failed for {path}") from exc

    def _read_current_owner_basis(
        self, pinned_campaign: PinnedCampaign
    ) -> tuple[PinnedCampaign, LiveRouting | None]:
        if pinned_campaign.campaign_id != self._campaign_id:
            raise RuntimeHostError("current-owner basis belongs to another campaign")
        operation = self._begin_operation()
        return operation.pinned_campaign, operation.selected_live

    def _read_current_owner_live(
        self, routing: LiveRouting, source: LiveEnvelope
    ) -> object:
        reader = getattr(self._live_transport, "read_selected_live_source", None)
        if not callable(reader):
            raise RuntimeHostError("selected LIVE native-owner read capability is unavailable")
        try:
            return reader(routing, source)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RuntimeHostError("selected LIVE native-owner read failed") from exc


def compose_runtime_host(
    selected_campaign_id: str,
    authenticated_repository_port: RepositoryPort,
    selected_live_transport: SelectedLiveTransport,
    campaign_publication_transport: CampaignPublicationTransport | None = None,
    hot_owner_store: HotOwnerStorePort | None = None,
    *,
    accepted_input_capability: AcceptedInputCapability | None = None,
) -> RuntimeHost:
    """Compose one immutable, campaign-bound ephemeral runtime root."""

    return RuntimeHost(
        selected_campaign_id,
        authenticated_repository_port,
        selected_live_transport,
        campaign_publication_transport,
        hot_owner_store,
        accepted_input_capability=accepted_input_capability,
    )


def _validate_transport_repository_identity(
    repository: object, transport: CampaignPublicationTransport
) -> str:
    try:
        write_identity = transport.repository_identity()
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise RuntimeHostError(
            "campaign publication repository identity is unavailable"
        ) from exc
    _nonempty_string(write_identity, "campaign publication repository identity")
    read_identity = getattr(repository, "repository_identity", None)
    if not callable(read_identity):
        raise RuntimeHostError("campaign read repository identity is unavailable")
    try:
        read_value = read_identity()
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise RuntimeHostError(
            "campaign read repository identity is unavailable"
        ) from exc
    if not isinstance(read_value, str) or read_value != write_identity:
        raise RuntimeHostError("campaign read/write repository identities differ")
    return write_identity
