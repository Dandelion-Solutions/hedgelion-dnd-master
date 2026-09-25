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
from typing import Final, NoReturn, Protocol

from .durability import RoutedSerializedOperation
from .live_state import (
    LIVE_NATIVE_STATE_PACK_SCHEMA_VERSION,
    LiveEnvelope,
    LiveNativeStatePack,
    LiveRouting,
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
    reconcile_indeterminate_publication,
)

# framework_module_version: 1.0.9
FRAMEWORK_MODULE_VERSION: Final[str] = "1.0.9"

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

    def create_commit(self, parent_sha: str, tree_sha: str, target_ref: str) -> object:
        """Create one single-parent commit and return its exact identity."""

    def update_ref(
        self, target_ref: str, new_commit_sha: str, force: bool = False
    ) -> object:
        """Request one non-force authority-changing ref transition."""


class RuntimeHostError(ValueError):
    """Raised when a campaign-bound runtime operation cannot be admitted."""


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
        selected = self._index_entries(index, lower, max_items)
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
    ) -> EvtSourceWindow:
        lower = self._validate_window_request(lower_exclusive_ordinal, max_items)
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
        if len(matches) != 1:
            raise RuntimeHostError("selected LIVE source is missing or ambiguous")
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
        value: Mapping[str, object], lower: int | None, max_items: int
    ) -> list[tuple[int, str, str]]:
        if value.get("schema_version") != 1 or value.get("entity_type") != "EVENT":
            raise RuntimeHostError(
                "LOCAL evt enrollment/index is not the accepted event index"
            )
        raw_entries = value.get("entries")
        if not isinstance(raw_entries, Sequence) or isinstance(
            raw_entries, (str, bytes)
        ):
            raise RuntimeHostError("LOCAL evt enrollment/index entries are not bounded")
        if value.get("complete") is not True or "upper_ordinal" not in value:
            raise RuntimeHostError(
                "LOCAL evt enrollment/index does not prove completeness"
            )
        upper_ordinal = value["upper_ordinal"]
        if upper_ordinal is not None and (
            type(upper_ordinal) is not int or upper_ordinal < 1
        ):
            raise RuntimeHostError("LOCAL evt enrollment/index upper basis is invalid")
        expected_length = 0 if upper_ordinal is None else upper_ordinal
        if expected_length != len(raw_entries):
            raise RuntimeHostError(
                "LOCAL evt index upper basis differs from enrollment"
            )
        start = lower or 0
        if start > expected_length:
            raise RuntimeHostError(
                "LOCAL evt lower cursor exceeds the complete upper basis"
            )
        stop = min(expected_length, start + max_items)
        if start == expected_length and start > 0:
            raise RuntimeHostError(
                "LOCAL evt source has no new interval after the cursor"
            )
        result: list[tuple[int, str, str]] = []
        for index in range(start, stop):
            raw = raw_entries[index]
            if not isinstance(raw, Mapping):
                raise RuntimeHostError("LOCAL evt enrollment entry is not typed")
            event_id = raw.get("event_id", raw.get("id"))
            if not isinstance(event_id, str) or not event_id:
                raise RuntimeHostError(
                    "LOCAL evt enrollment entry has no event identity"
                )
            ordinal = raw.get("ordinal")
            if type(ordinal) is not int or ordinal != index + 1:
                raise RuntimeHostError(
                    "LOCAL evt enrollment interval is not contiguous"
                )
            path = raw.get("path")
            expected_path = route_native_record(
                "runtime.semantic_event", (event_id,)
            ).relative_path
            if path is not None and path != expected_path:
                raise RuntimeHostError(
                    "LOCAL evt enrollment path is not the known-ID route"
                )
            result.append((ordinal, event_id, expected_path))
        if len({event_id for _ordinal, event_id, _path in result}) != len(result):
            raise RuntimeHostError("LOCAL evt enrollment identities are not unique")
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
        )


class HistoryService(_BoundService):
    """Fixed route to native history; it is a sibling of ContextService."""

    __slots__ = ()

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
        "_basis_token",
        "_campaign_id",
        "_context",
        "_history",
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
    ) -> None:
        campaign_id = _require_nonempty_campaign_id(selected_campaign_id)
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
        object.__setattr__(self, "_campaign_id", campaign_id)
        object.__setattr__(self, "_basis_token", object())
        object.__setattr__(self, "_repository", authenticated_repository_port)
        object.__setattr__(self, "_live_transport", selected_live_transport)
        object.__setattr__(
            self, "_publication_transport", campaign_publication_transport
        )
        object.__setattr__(self, "_context", ContextService(self))
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


def compose_runtime_host(
    selected_campaign_id: str,
    authenticated_repository_port: RepositoryPort,
    selected_live_transport: SelectedLiveTransport,
    campaign_publication_transport: CampaignPublicationTransport | None = None,
) -> RuntimeHost:
    """Compose one immutable, campaign-bound ephemeral runtime root."""

    return RuntimeHost(
        selected_campaign_id,
        authenticated_repository_port,
        selected_live_transport,
        campaign_publication_transport,
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
