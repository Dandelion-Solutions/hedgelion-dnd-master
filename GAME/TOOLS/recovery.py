"""Bounded current-source recovery and maintenance contracts.

Recovery follows owner-native currentness routes.  It never promotes a
checkpoint, session record, local HOT projection, or historical observation to
current authority.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import re
from typing import Final, Protocol

from .catalog_runtime import BoundCatalogContext, CatalogBindingError
from .native_storage import NativeStorageError, route_native_record
from .policy_basis import PinnedCampaign, PolicyBasisResolutionError, validate_frozen_adjudication_basis
from .recovery_roots import derive_operational_root_delta
from .runtime_execution import CommandAcceptanceError, validate_execution_proposal


# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final = "1.0.5"
_REVISION = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_NATIVE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


class RecoveryFailureCode(str, Enum):
    MISSING = "MISSING"
    STALE = "STALE"
    CORRUPT = "CORRUPT"
    INCOMPLETE = "INCOMPLETE"
    AMBIGUOUS = "AMBIGUOUS"


class RecoveryDisposition(str, Enum):
    READY = "READY"
    RETRY = "RETRY"
    BLOCKED = "BLOCKED"


class RecoverySourceError(ValueError):
    """A current-source selection cannot establish a typed recovery basis."""

    def __init__(self, message: str, *, code: RecoveryFailureCode) -> None:
        super().__init__(message)
        self.code = code


class RecoveryFailure(RecoverySourceError):
    """Typed failure for an invalid recovered native owner or accepted basis."""


class CheckpointDescriptorError(RecoveryFailure):
    """A checkpoint descriptor is malformed, stale, or incorrectly associated."""


class RecoveryRepository(Protocol):
    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        """Pin the selected campaign through its currentness owner."""

    def select_current_native_sources(
        self, pinned: PinnedCampaign
    ) -> Iterable["CurrentNativeSource"]:
        """Return the explicit owner-native current source set."""


@dataclass(frozen=True, slots=True)
class CurrentNativeSource:
    """One exact current source selected by an owning routing contract."""

    campaign_id: str
    domain: str
    source_id: str
    revision: str
    relative_path: str

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "source campaign_id")
        _nonempty(self.domain, "source domain")
        _nonempty(self.source_id, "source identity")
        _revision(self.revision, "source revision")
        _safe_path(self.relative_path)

    @property
    def identity(self) -> tuple[str, str, str]:
        return self.domain, self.source_id, self.revision

    def to_dict(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "domain": self.domain,
            "source_id": self.source_id,
            "revision": self.revision,
            "relative_path": self.relative_path,
        }


@dataclass(frozen=True, slots=True)
class CheckpointDescriptor:
    """Narrow immutable checkpoint identity/provenance descriptor."""

    schema_version: int
    id: str
    campaign_id: str
    created_at: str | None = None
    state: Mapping[str, object] | None = None
    engine: Mapping[str, object] | None = None
    ruleset: Mapping[str, object] | None = None
    schema_data_version: int | None = None

    def __post_init__(self) -> None:
        if self.schema_version != 4:
            raise CheckpointDescriptorError(
                "unsupported checkpoint descriptor schema",
                code=RecoveryFailureCode.CORRUPT,
            )
        _nonempty(self.id, "checkpoint id")
        _nonempty(self.campaign_id, "checkpoint campaign_id")


@dataclass(frozen=True, slots=True)
class RecoveredExecution:
    """Accepted execution evidence returned without replay or reallocation."""

    command_id: str
    input_fingerprint: str
    resolution_id: str
    segment_id: str
    event_id: str
    fixed_rng_values: tuple[int, ...]
    catalog_basis: Mapping[str, object]
    policy_basis: Mapping[str, object]
    accepted_command: Mapping[str, object]
    execution: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class RecoveryResult:
    disposition: RecoveryDisposition
    campaign: PinnedCampaign
    sources: tuple[CurrentNativeSource, ...]
    roots: tuple[Mapping[str, object], ...]
    hydrated_owners: tuple[Mapping[str, object], ...]
    checkpoint: CheckpointDescriptor | None = None
    hot_authoritative: bool = False
    hot_rebuilt: bool = True
    reason_code: RecoveryFailureCode | None = None
    affected_scopes: tuple[str, ...] = ()
    diagnostic_evidence: Mapping[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "disposition": self.disposition.value,
            "reason_code": self.reason_code.value if self.reason_code is not None else None,
            "affected_scopes": list(self.affected_scopes),
            "diagnostic_evidence": deepcopy(dict(self.diagnostic_evidence or {})),
            "sources": [source.to_dict() for source in self.sources],
            "operational_root_count": len(self.hydrated_owners),
            "hot_authoritative": self.hot_authoritative,
            "ephemeral": True,
        }


@dataclass(frozen=True, slots=True)
class HistoricalRepairCandidate:
    """Validated historical evidence kept outside ordinary current recovery."""

    campaign_id: str
    operation_id: str
    historical_revision: str
    source_paths: tuple[str, ...]
    evidence: Mapping[str, object]

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "repair campaign_id")
        _nonempty(self.operation_id, "repair operation_id")
        _revision(self.historical_revision, "repair historical revision")
        if not self.source_paths or len(set(self.source_paths)) != len(self.source_paths):
            raise RecoveryFailure("repair source paths are incomplete", code=RecoveryFailureCode.INCOMPLETE)
        for path in self.source_paths:
            _safe_path(path)
        if not isinstance(self.evidence, Mapping) or not self.evidence:
            raise RecoveryFailure("repair evidence is incomplete", code=RecoveryFailureCode.INCOMPLETE)

    def to_dict(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "operation_id": self.operation_id,
            "historical_revision": self.historical_revision,
            "source_paths": list(self.source_paths),
            "evidence": deepcopy(dict(self.evidence)),
            "current_authority": False,
        }


@dataclass(frozen=True, slots=True)
class MaintenanceAudit:
    """Narrow support audit evidence; never a recovery or currentness owner."""

    campaign_id: str
    audit_id: str
    operation: str
    scope: str
    outcome: str
    observed_basis: Mapping[str, object]

    def __post_init__(self) -> None:
        _nonempty(self.campaign_id, "audit campaign_id")
        if not re.fullmatch(r"audit-[0-9]{4,}", self.audit_id):
            raise RecoveryFailure("audit identity is not campaign-native", code=RecoveryFailureCode.CORRUPT)
        _nonempty(self.operation, "audit operation")
        _nonempty(self.scope, "audit scope")
        if self.outcome not in {"CONFIRMED", "UNAVAILABLE", "REJECTED", "INDETERMINATE"}:
            raise RecoveryFailure("audit outcome is unsupported", code=RecoveryFailureCode.CORRUPT)
        if not isinstance(self.observed_basis, Mapping) or not self.observed_basis:
            raise RecoveryFailure("audit observed basis is required", code=RecoveryFailureCode.INCOMPLETE)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "kind": "runtime.maintenance_audit",
            "campaign_id": self.campaign_id,
            "audit_id": self.audit_id,
            "operation": self.operation,
            "scope": self.scope,
            "outcome": self.outcome,
            "observed_basis": deepcopy(dict(self.observed_basis)),
            "authority": "SUPPORT_AUDIT_ONLY",
        }


def export_checkpoint_diagnostics(
    checkpoint: object | None,
    *,
    campaign_id: str,
    selected_id: str | None = None,
    observed_revision: str | None = None,
) -> Mapping[str, object]:
    """Export descriptor evidence without hydrating HOT or moving authority."""

    _nonempty(campaign_id, "campaign_id")
    if checkpoint is not None and not isinstance(checkpoint, Mapping):
        repository = checkpoint
        try:
            pinned = repository.pin_campaign(campaign_id)  # type: ignore[attr-defined]
            if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
                raise RecoveryFailure(
                    "checkpoint diagnostic pin is corrupt", code=RecoveryFailureCode.CORRUPT
                )
            reader = repository.read_exact_path  # type: ignore[attr-defined]
            manifest = _mapping_or_failure(reader(pinned, "MANIFEST.yaml"), "campaign manifest")
        except (AttributeError, KeyError, OSError, TypeError) as exc:
            raise RecoveryFailure(
                "checkpoint diagnostic source is missing", code=RecoveryFailureCode.MISSING
            ) from exc
        pointer = manifest.get("last_checkpoint_id")
        if pointer is None:
            return {
                "schema_version": 1,
                "campaign_id": campaign_id,
                "observed_revision": pinned.revision,
                "status": "NO_CHECKPOINT",
                "authoritative": False,
                "ephemeral": True,
            }
        if not isinstance(pointer, str) or not pointer:
            raise RecoveryFailure(
                "checkpoint pointer is corrupt", code=RecoveryFailureCode.CORRUPT
            )
        try:
            checkpoint = reader(
                pinned, route_native_record("runtime.checkpoint", (pointer,)).relative_path
            )
        except (AttributeError, KeyError, OSError, TypeError) as exc:
            raise RecoveryFailure(
                "checkpoint descriptor is missing", code=RecoveryFailureCode.MISSING
            ) from exc
        selected_id = pointer
        observed_revision = pinned.revision
    if checkpoint is None:
        return {
            "schema_version": 1,
            "campaign_id": campaign_id,
            "status": "NO_CHECKPOINT",
            "authoritative": False,
            "ephemeral": True,
        }
    descriptor = validate_checkpoint_descriptor(checkpoint, campaign_id=campaign_id, selected_id=selected_id)  # type: ignore[arg-type]
    result: dict[str, object] = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "checkpoint_id": descriptor.id,
        "status": "VALID",
        "authoritative": False,
        "ephemeral": True,
    }
    if observed_revision is not None:
        result["observed_revision"] = _revision(observed_revision, "observed revision")
    return result


def reset_last_checkpoint_reference(
    manifest: Mapping[str, object], *, selected_checkpoint_id: str
) -> dict[str, object]:
    """Return a pointer-only maintenance projection after exact selection proof."""

    value = _mapping_or_failure(manifest, "campaign manifest")
    selected = value.get("last_checkpoint_id")
    if selected is None:
        return deepcopy(dict(value))
    if selected != selected_checkpoint_id:
        raise RecoveryFailure(
            "last checkpoint pointer moved during maintenance",
            code=RecoveryFailureCode.STALE,
        )
    result = deepcopy(dict(value))
    result["last_checkpoint_id"] = None
    return result


def validate_repair_candidate(
    candidate: object,
    *,
    campaign_id: str,
    historical_revision: str | None = None,
) -> HistoricalRepairCandidate:
    """Validate a complete historical composition without making it current."""

    value = _mapping_or_failure(candidate, "historical repair candidate")
    expected = {
        "schema_version",
        "campaign_id",
        "operation_id",
        "historical_revision",
        "source_paths",
        "evidence",
    }
    if set(value) != expected or value.get("schema_version") != 1:
        raise RecoveryFailure("repair candidate shape is unsupported", code=RecoveryFailureCode.CORRUPT)
    if value.get("campaign_id") != campaign_id:
        raise RecoveryFailure("repair candidate belongs to another campaign", code=RecoveryFailureCode.AMBIGUOUS)
    revision = _revision(value.get("historical_revision"), "repair historical revision")
    if historical_revision is not None and revision != historical_revision:
        raise RecoveryFailure("repair candidate revision is stale", code=RecoveryFailureCode.STALE)
    paths = value.get("source_paths")
    if not isinstance(paths, Sequence) or isinstance(paths, (str, bytes)):
        raise RecoveryFailure("repair source paths are incomplete", code=RecoveryFailureCode.INCOMPLETE)
    source_paths = tuple(_safe_path(path) for path in paths)
    return HistoricalRepairCandidate(
        campaign_id=campaign_id,
        operation_id=_nonempty(value.get("operation_id"), "repair operation_id"),
        historical_revision=revision,
        source_paths=source_paths,
        evidence=_mapping_or_failure(value.get("evidence"), "repair evidence"),
    )


def promote_historical_repair(
    candidate: HistoricalRepairCandidate,
    *,
    current_revision: str,
    authorized: bool,
    publication: object | None = None,
) -> Mapping[str, object]:
    """Prepare only a forward promotion; never rewind a current ref locally."""

    if not isinstance(candidate, HistoricalRepairCandidate):
        raise RecoveryFailure("repair promotion requires validated candidate", code=RecoveryFailureCode.CORRUPT)
    _revision(current_revision, "current revision")
    if not authorized:
        raise RecoveryFailure(
            "repair promotion requires application authorization",
            code=RecoveryFailureCode.INCOMPLETE,
        )
    if candidate.historical_revision == current_revision:
        raise RecoveryFailure("historical repair is not a distinct forward promotion", code=RecoveryFailureCode.STALE)
    if publication is not None and not callable(publication):
        raise RecoveryFailure("repair promotion publication boundary is invalid", code=RecoveryFailureCode.CORRUPT)
    result: dict[str, object] = {
        "operation_id": candidate.operation_id,
        "campaign_id": candidate.campaign_id,
        "historical_revision": candidate.historical_revision,
        "current_basis_revision": current_revision,
        "status": "FORWARD_PUBLICATION_REQUIRED",
        "ref_rewind": False,
        "current_authority": False,
    }
    if publication is not None:
        result["publication_plan"] = publication(candidate)
    return result


def record_maintenance_audit(
    *,
    campaign_id: str,
    audit_id: str,
    operation: str,
    scope: str,
    outcome: str,
    observed_basis: Mapping[str, object],
) -> MaintenanceAudit:
    """Build one idempotent-support audit record without granting authority."""

    return MaintenanceAudit(
        campaign_id=campaign_id,
        audit_id=audit_id,
        operation=operation,
        scope=scope,
        outcome=outcome,
        observed_basis=deepcopy(dict(observed_basis)),
    )


def validate_checkpoint_descriptor(
    value: object,
    *,
    campaign_id: str,
    selected_id: str | None = None,
) -> CheckpointDescriptor:
    """Validate optional descriptor metadata without making it a source selector."""

    if not isinstance(value, Mapping):
        raise CheckpointDescriptorError(
            "checkpoint descriptor is not an object", code=RecoveryFailureCode.CORRUPT
        )
    retired = {"valid_through_event_id", "expected_commit_sha", "world_time"}
    if retired.intersection(value):
        raise CheckpointDescriptorError(
            "checkpoint contains retired recovery authority", code=RecoveryFailureCode.CORRUPT
        )
    allowed = {
        "schema_version",
        "id",
        "campaign_id",
        "created_at",
        "state",
        "engine",
        "ruleset",
        "schema_data_version",
    }
    if set(value) - allowed:
        raise CheckpointDescriptorError(
            "checkpoint descriptor has unsupported fields", code=RecoveryFailureCode.CORRUPT
        )
    if value.get("campaign_id") != campaign_id:
        raise CheckpointDescriptorError(
            "checkpoint descriptor belongs to another campaign", code=RecoveryFailureCode.AMBIGUOUS
        )
    descriptor_id = value.get("id")
    if not isinstance(descriptor_id, str) or not descriptor_id:
        raise CheckpointDescriptorError(
            "checkpoint descriptor has no identity", code=RecoveryFailureCode.CORRUPT
        )
    if selected_id is not None and descriptor_id != selected_id:
        raise CheckpointDescriptorError(
            "checkpoint descriptor is stale for the selected pointer", code=RecoveryFailureCode.STALE
        )
    schema_version = value.get("schema_version")
    if schema_version != 4:
        raise CheckpointDescriptorError(
            "unsupported checkpoint descriptor schema", code=RecoveryFailureCode.CORRUPT
        )
    for field in ("state", "engine", "ruleset"):
        field_value = value.get(field)
        if field_value is not None and not isinstance(field_value, Mapping):
            raise CheckpointDescriptorError(
                f"checkpoint {field} must be an object", code=RecoveryFailureCode.CORRUPT
            )
    created_at = value.get("created_at")
    if created_at is not None and not isinstance(created_at, str):
        raise CheckpointDescriptorError(
            "checkpoint created_at must be text", code=RecoveryFailureCode.CORRUPT
        )
    schema_data_version = value.get("schema_data_version")
    if schema_data_version is not None and (
        isinstance(schema_data_version, bool) or not isinstance(schema_data_version, int)
    ):
        raise CheckpointDescriptorError(
            "checkpoint schema_data_version must be an integer", code=RecoveryFailureCode.CORRUPT
        )
    return CheckpointDescriptor(
        schema_version=4,
        id=descriptor_id,
        campaign_id=campaign_id,
        created_at=created_at,
        state=deepcopy(value.get("state")) if isinstance(value.get("state"), Mapping) else None,
        engine=deepcopy(value.get("engine")) if isinstance(value.get("engine"), Mapping) else None,
        ruleset=deepcopy(value.get("ruleset")) if isinstance(value.get("ruleset"), Mapping) else None,
        schema_data_version=schema_data_version,
    )


def validate_recovered_basis(
    accepted_command: object,
    execution: object,
    *,
    catalog_basis: Mapping[str, object],
    policy_basis: Mapping[str, object],
    resolution: object | None = None,
) -> RecoveredExecution:
    """Validate accepted execution evidence exactly as persisted by publication."""

    command = _mapping_or_failure(accepted_command, "accepted command")
    result = _mapping_or_failure(execution, "execution evidence")
    command_id = _string_or_failure(command.get("command_id"), "command_id")
    fingerprint = _digest_or_failure(command.get("input_fingerprint"), "input_fingerprint")
    if result.get("accepted_command_id") != command_id or result.get("accepted_input_fingerprint") != fingerprint:
        raise RecoveryFailure("accepted execution identity differs", code=RecoveryFailureCode.CORRUPT)
    resolution_id = _string_or_failure(result.get("resolution_id"), "resolution_id")
    segment = _mapping_or_failure(result.get("segment"), "execution segment")
    segment_id = _string_or_failure(segment.get("segment_id"), "segment_id")
    event = _mapping_or_failure(result.get("event"), "execution event")
    _validate_event_identity(result, resolution_id, segment, segment_id, event)
    event_id = _string_or_failure(result.get("event_id"), "event_id")
    roll = result.get("roll_result", {})
    if not isinstance(roll, Mapping):
        raise RecoveryFailure("fixed RNG evidence is malformed", code=RecoveryFailureCode.CORRUPT)
    raw_values = roll.get("raw_values", ())
    if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)):
        raise RecoveryFailure("fixed RNG evidence is malformed", code=RecoveryFailureCode.CORRUPT)
    fixed_values = tuple(raw_values)
    if any(isinstance(value, bool) or not isinstance(value, int) for value in fixed_values):
        raise RecoveryFailure("fixed RNG evidence is malformed", code=RecoveryFailureCode.CORRUPT)
    if roll:
        _validate_roll_identity(roll)
    if resolution is not None:
        _validate_resolution_closure(resolution, resolution_id, command_id, segment, roll)
    accepted_catalog = _mapping_or_failure(command.get("catalog_context"), "catalog basis")
    supplied_catalog = _mapping_or_failure(catalog_basis, "catalog basis")
    if dict(accepted_catalog) != dict(supplied_catalog):
        raise RecoveryFailure("catalog basis differs from accepted execution", code=RecoveryFailureCode.STALE)
    supplied_policy = _mapping_or_failure(policy_basis, "policy basis")
    action_request = _mapping_or_failure(command.get("action_request"), "accepted action_request")
    invocation_facts = command.get("invocation_facts")
    try:
        normalized_parameters, normalized_facts, frozen_refs = validate_frozen_adjudication_basis(
            action_request.get("parameter_bindings", {}), invocation_facts
        )
    except PolicyBasisResolutionError as exc:
        raise RecoveryFailure("frozen adjudication basis is invalid", code=RecoveryFailureCode.CORRUPT) from exc
    if normalized_parameters != action_request.get("parameter_bindings", {}) or normalized_facts != invocation_facts:
        raise RecoveryFailure("accepted adjudication basis is not normalized", code=RecoveryFailureCode.CORRUPT)
    refs = _accepted_policy_refs(command)
    if refs != frozen_refs:
        raise RecoveryFailure("accepted policy references differ from frozen inputs", code=RecoveryFailureCode.CORRUPT)
    supplied_refs = supplied_policy.get("policy_refs")
    if not isinstance(supplied_refs, Sequence) or isinstance(supplied_refs, (str, bytes)):
        raise RecoveryFailure("accepted policy basis is incomplete", code=RecoveryFailureCode.INCOMPLETE)
    typed_supplied_refs = tuple(sorted(_string_or_failure(ref, "policy reference") for ref in supplied_refs))
    if typed_supplied_refs != refs:
        raise RecoveryFailure("policy basis differs from accepted execution", code=RecoveryFailureCode.STALE)
    if refs:
        supplied_action = _mapping_or_failure(supplied_policy.get("action_request"), "policy basis action_request")
        supplied_facts = supplied_policy.get("invocation_facts")
        if dict(supplied_action) != dict(action_request) or supplied_facts != invocation_facts:
            raise RecoveryFailure("policy basis inputs differ from accepted execution", code=RecoveryFailureCode.CORRUPT)
    source_revision = supplied_policy.get("source_revision")
    if refs and (not isinstance(source_revision, str) or any(not ref.endswith("@" + source_revision) for ref in refs)):
        raise RecoveryFailure("accepted policy basis is stale", code=RecoveryFailureCode.STALE)
    return RecoveredExecution(
        command_id=command_id,
        input_fingerprint=fingerprint,
        resolution_id=resolution_id,
        segment_id=segment_id,
        event_id=event_id,
        fixed_rng_values=fixed_values,
        catalog_basis=deepcopy(dict(accepted_catalog)),
        policy_basis=deepcopy(dict(supplied_policy)),
        accepted_command=deepcopy(dict(command)),
        execution=deepcopy(dict(result)),
    )


def hydrate_operational_roots(
    repository: object,
    pinned: PinnedCampaign,
    page: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    """Hydrate every root in one complete routing page by exact native route."""

    roots = _root_mappings(page, pinned.campaign_id)
    reader = getattr(repository, "read_exact_path", None)
    if not callable(reader):
        raise RecoveryFailure("native root reader is unavailable", code=RecoveryFailureCode.MISSING)
    hydrated: list[Mapping[str, object]] = []
    for root in roots:
        route = root["route"]
        path = route["relative_path"]
        try:
            owner = reader(pinned, path)
        except (AttributeError, KeyError, OSError, TypeError) as exc:
            raise RecoveryFailure("required operational root is missing", code=RecoveryFailureCode.MISSING) from exc
        owner_map = _mapping_or_failure(owner, "operational root owner")
        _validate_root_owner(pinned.campaign_id, root, owner_map)
        hydrated.append(deepcopy(dict(owner_map)))
    return tuple(hydrated)


def recover_current_runtime(
    repository: object,
    campaign_id: str,
    *,
    checkpoint: Mapping[str, object] | None = None,
    hot_state: Mapping[str, object] | None = None,
) -> RecoveryResult:
    """Recover the selected current native source set without replay or scans."""

    try:
        pinned = repository.pin_campaign(campaign_id)  # type: ignore[attr-defined]
    except (AttributeError, KeyError, OSError, TypeError) as exc:
        raise RecoverySourceError("selected campaign source is missing", code=RecoveryFailureCode.MISSING) from exc
    if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
        raise RecoverySourceError("selected campaign pin is corrupt", code=RecoveryFailureCode.CORRUPT)
    sources = _select_sources_from_pin(repository, pinned)
    for source in sources:
        if source.domain == "campaign":
            reader = getattr(repository, "read_exact_path", None)
            if not callable(reader):
                raise RecoverySourceError("campaign source reader is missing", code=RecoveryFailureCode.MISSING)
            try:
                reader(pinned, source.relative_path)
            except (AttributeError, KeyError, OSError, TypeError) as exc:
                raise RecoverySourceError("campaign current source is missing", code=RecoveryFailureCode.MISSING) from exc
        else:
            reader = getattr(repository, "read_current_native_source", None)
            if not callable(reader):
                raise RecoverySourceError("selected native source is missing", code=RecoveryFailureCode.MISSING)
            try:
                reader(source)
            except (AttributeError, KeyError, OSError, TypeError) as exc:
                raise RecoverySourceError("selected native source is missing", code=RecoveryFailureCode.MISSING) from exc
    root_reader = getattr(repository, "read_exact_path", None)
    if not callable(root_reader):
        raise RecoveryFailure("operational-root route is missing", code=RecoveryFailureCode.MISSING)
    try:
        page = root_reader(pinned, "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml")
    except (AttributeError, KeyError, OSError, TypeError) as exc:
        raise RecoveryFailure("operational-root route is missing", code=RecoveryFailureCode.MISSING) from exc
    hydrated = hydrate_operational_roots(repository, pinned, _mapping_or_failure(page, "root routing page"))
    _validate_recovered_root_closures(repository, pinned, hydrated)
    checkpoint_descriptor = None
    if checkpoint is not None:
        try:
            checkpoint_descriptor = validate_checkpoint_descriptor(checkpoint, campaign_id=campaign_id)
        except CheckpointDescriptorError:
            # Optional checkpoint defects remain facility-scoped; current roots win.
            checkpoint_descriptor = None
    del hot_state
    return RecoveryResult(
        disposition=RecoveryDisposition.READY,
        campaign=pinned,
        sources=sources,
        roots=tuple(_root_mappings(page, campaign_id)),
        hydrated_owners=hydrated,
        checkpoint=checkpoint_descriptor,
        hot_authoritative=False,
        hot_rebuilt=True,
    )


def select_current_native_sources(
    repository: RecoveryRepository,
    campaign_id: str,
    *,
    checkpoint_hint: Mapping[str, object] | None = None,
) -> tuple[CurrentNativeSource, ...]:
    """Select exact current sources from the native route, never from hints.

    ``checkpoint_hint`` is deliberately accepted only as an explicitly
    non-authoritative input so callers cannot accidentally make it the source
    selector.  The route owner remains the sole selector for this attempt.
    """

    del checkpoint_hint
    try:
        pinned = repository.pin_campaign(campaign_id)
    except (AttributeError, KeyError, OSError, TypeError) as exc:
        raise RecoverySourceError(
            "selected campaign current source is missing",
            code=RecoveryFailureCode.MISSING,
        ) from exc
    if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
        raise RecoverySourceError(
            "repository did not return a trusted exact campaign pin",
            code=RecoveryFailureCode.CORRUPT,
        )
    return _select_sources_from_pin(repository, pinned)


def _select_sources_from_pin(
    repository: object, pinned: PinnedCampaign
) -> tuple[CurrentNativeSource, ...]:
    selector = getattr(repository, "select_current_native_sources", None)
    if not callable(selector):
        raise RecoverySourceError(
            "owner-native current source route is unavailable",
            code=RecoveryFailureCode.INCOMPLETE,
        )
    try:
        raw_sources = selector(pinned)
    except (AttributeError, KeyError, OSError, TypeError) as exc:
        raise RecoverySourceError(
            "owner-native current source route is unavailable",
            code=RecoveryFailureCode.MISSING,
        ) from exc
    if raw_sources is None or callable(raw_sources) or isinstance(raw_sources, (str, bytes, Mapping)):
        raise RecoverySourceError(
            "current source route is not an explicit native enumeration",
            code=RecoveryFailureCode.CORRUPT,
        )
    try:
        sources = tuple(raw_sources)
    except TypeError as exc:
        raise RecoverySourceError(
            "current source route is not iterable",
            code=RecoveryFailureCode.CORRUPT,
        ) from exc
    if not sources:
        raise RecoverySourceError(
            "current source route is incomplete",
            code=RecoveryFailureCode.INCOMPLETE,
        )
    validated: list[CurrentNativeSource] = []
    seen: set[tuple[str, str]] = set()
    for source in sources:
        if not isinstance(source, CurrentNativeSource):
            raise RecoverySourceError(
                "current source route contains untyped evidence",
                code=RecoveryFailureCode.CORRUPT,
            )
        if source.campaign_id != pinned.campaign_id:
            raise RecoverySourceError(
                "current source identity belongs to another campaign",
                code=RecoveryFailureCode.AMBIGUOUS,
            )
        key = source.domain, source.source_id
        if key in seen:
            raise RecoverySourceError(
                "current source route selects one owner more than once",
                code=RecoveryFailureCode.AMBIGUOUS,
            )
        seen.add(key)
        if source.domain == "campaign" and source.revision != pinned.revision:
            raise RecoverySourceError(
                "campaign current source is stale relative to the pinned campaign",
                code=RecoveryFailureCode.STALE,
            )
        validated.append(source)
    return tuple(validated)


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RecoverySourceError(f"{label} must be a nonempty string", code=RecoveryFailureCode.CORRUPT)
    return value


def _revision(value: object, label: str) -> str:
    if not isinstance(value, str) or _REVISION.fullmatch(value) is None:
        raise RecoverySourceError(f"{label} must be an exact lowercase revision", code=RecoveryFailureCode.CORRUPT)
    return value


def _safe_path(value: object) -> str:
    path = _nonempty(value, "source route")
    if path.startswith("/") or "//" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        raise RecoverySourceError("source route is not normalized", code=RecoveryFailureCode.CORRUPT)
    return path


def _mapping_or_failure(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise RecoveryFailure(f"{label} must be an object", code=RecoveryFailureCode.CORRUPT)
    return value


def _string_or_failure(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RecoveryFailure(f"{label} must be nonempty text", code=RecoveryFailureCode.CORRUPT)
    return value


def _digest_or_failure(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise RecoveryFailure(f"{label} must be a SHA-256 digest", code=RecoveryFailureCode.CORRUPT)
    return value


def _accepted_policy_refs(command: Mapping[str, object]) -> tuple[str, ...]:
    refs: set[str] = set()
    action = command.get("action_request")
    if action is not None and not isinstance(action, Mapping):
        raise RecoveryFailure("action request is malformed", code=RecoveryFailureCode.CORRUPT)
    if isinstance(action, Mapping):
        bindings = action.get("parameter_bindings")
        if bindings is not None and not isinstance(bindings, Mapping):
            raise RecoveryFailure("parameter bindings are malformed", code=RecoveryFailureCode.CORRUPT)
        if isinstance(bindings, Mapping):
            for binding in bindings.values():
                if not isinstance(binding, Mapping):
                    raise RecoveryFailure("parameter binding is malformed", code=RecoveryFailureCode.CORRUPT)
                values = binding.get("policy_basis_refs", ())
                if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
                    raise RecoveryFailure("policy basis references are malformed", code=RecoveryFailureCode.CORRUPT)
                refs.update(_string_or_failure(value, "policy reference") for value in values)
    facts = command.get("invocation_facts", ())
    if not isinstance(facts, Sequence) or isinstance(facts, (str, bytes)):
        raise RecoveryFailure("invocation facts are malformed", code=RecoveryFailureCode.CORRUPT)
    if isinstance(facts, Sequence) and not isinstance(facts, (str, bytes)):
        for fact in facts:
            if not isinstance(fact, Mapping):
                raise RecoveryFailure("invocation fact is malformed", code=RecoveryFailureCode.CORRUPT)
            values = fact.get("policy_basis_refs", ())
            if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
                raise RecoveryFailure("policy basis references are malformed", code=RecoveryFailureCode.CORRUPT)
            refs.update(_string_or_failure(value, "policy reference") for value in values)
    return tuple(sorted(refs))


def _root_mappings(page: Mapping[str, object], campaign_id: str) -> tuple[Mapping[str, object], ...]:
    if page.get("schema_version") != 1 or page.get("campaign_id") != campaign_id:
        raise RecoveryFailure("operational-root page is corrupt", code=RecoveryFailureCode.CORRUPT)
    if page.get("complete") is not True:
        raise RecoveryFailure("operational-root page is incomplete", code=RecoveryFailureCode.INCOMPLETE)
    raw_roots = page.get("roots")
    if not isinstance(raw_roots, list):
        raise RecoveryFailure("operational-root page has no root array", code=RecoveryFailureCode.CORRUPT)
    result: list[Mapping[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for raw_root in raw_roots:
        root = _mapping_or_failure(raw_root, "operational root")
        owner_kind = _string_or_failure(root.get("owner_kind"), "root owner_kind")
        owner_id = _string_or_failure(root.get("owner_id"), "root owner_id")
        route = _mapping_or_failure(root.get("route"), "root route")
        if route.get("family_key") != owner_kind or route.get("identity") != [owner_id]:
            raise RecoveryFailure("operational-root route identity differs", code=RecoveryFailureCode.CORRUPT)
        try:
            expected_path = route_native_record(owner_kind, (owner_id,)).relative_path
        except NativeStorageError as exc:
            raise RecoveryFailure(
                "operational-root owner kind is not a native storage family",
                code=RecoveryFailureCode.CORRUPT,
            ) from exc
        if route.get("relative_path") != expected_path:
            raise RecoveryFailure("operational-root route is not native", code=RecoveryFailureCode.CORRUPT)
        key = owner_kind, owner_id
        if key in seen:
            raise RecoveryFailure("operational-root page is ambiguous", code=RecoveryFailureCode.AMBIGUOUS)
        seen.add(key)
        result.append(root)
    return tuple(result)


def _validate_recovered_root_closures(
    repository: object,
    pinned: PinnedCampaign,
    owners: Sequence[Mapping[str, object]],
) -> None:
    for owner in owners:
        if not _is_runtime_command_owner(owner):
            continue
        accepted_command = owner
        command_id = _string_or_failure(accepted_command.get("command_id"), "accepted command_id")
        raw_resolution_id = accepted_command.get("root_resolution_id")
        if raw_resolution_id is None:
            raise RecoveryFailure(
                "accepted command root resolution identity is missing",
                code=RecoveryFailureCode.INCOMPLETE,
            )
        resolution_id = _string_or_failure(raw_resolution_id, "accepted command root_resolution_id")
        resolution = _read_pinned_native_record(
            repository,
            pinned,
            "runtime.resolution",
            (resolution_id,),
            "runtime resolution",
        )
        execution = _hydrate_execution_result(repository, pinned, accepted_command, resolution)
        catalog_basis = _mapping_or_failure(accepted_command.get("catalog_context"), "catalog basis")
        policy_basis = _recovered_policy_basis(repository, pinned, accepted_command)
        recovered = validate_recovered_basis(
            accepted_command,
            execution,
            catalog_basis=catalog_basis,
            policy_basis=policy_basis,
            resolution=resolution,
        )
        if recovered.command_id != command_id:
            raise RecoveryFailure(
                "runtime command closure identity differs from native owner",
                code=RecoveryFailureCode.CORRUPT,
            )
        _validate_catalog_closure(repository, pinned, accepted_command, catalog_basis)


def _is_runtime_command_owner(owner: Mapping[str, object]) -> bool:
    declared_kind = owner.get("kind")
    if declared_kind is not None:
        return declared_kind == "runtime.command"
    return "command_id" in owner and "root_resolution_id" in owner


def _read_pinned_native_record(
    repository: object,
    pinned: PinnedCampaign,
    family_key: str,
    identity: tuple[str, ...],
    label: str,
) -> Mapping[str, object]:
    reader = getattr(repository, "read_exact_path", None)
    if not callable(reader):
        raise RecoveryFailure(f"{label} reader is unavailable", code=RecoveryFailureCode.MISSING)
    try:
        route = route_native_record(family_key, identity)
        payload = reader(pinned, route.relative_path)
    except (AttributeError, KeyError, OSError, TypeError, NativeStorageError) as exc:
        raise RecoveryFailure(f"{label} is missing", code=RecoveryFailureCode.MISSING) from exc
    value = _mapping_or_failure(payload, label)
    _validate_pinned_native_identity(family_key, identity, value)
    return value


def _validate_pinned_native_identity(
    family_key: str, identity: tuple[str, ...], payload: Mapping[str, object]
) -> None:
    declared_kind = payload.get("kind")
    if declared_kind is not None and declared_kind != family_key:
        raise RecoveryFailure(
            "native owner kind differs from its exact route", code=RecoveryFailureCode.CORRUPT
        )
    owner_id = identity[0]
    if family_key == "runtime.command" and payload.get("command_id") != owner_id:
        raise RecoveryFailure(
            "runtime command identity differs from its exact route",
            code=RecoveryFailureCode.CORRUPT,
        )
    if family_key == "runtime.resolution_trace" and payload.get("resolution_id") != owner_id:
        raise RecoveryFailure(
            "resolution trace identity differs from its exact route",
            code=RecoveryFailureCode.CORRUPT,
        )
    if family_key == "runtime.mechanical_event":
        declared_id = payload.get("event_id")
        if declared_id is not None and declared_id != owner_id:
            raise RecoveryFailure(
                "mechanical event identity differs from its exact route",
                code=RecoveryFailureCode.CORRUPT,
            )
    if family_key == "runtime.resolution":
        declared_id = payload.get("resolution_id")
        if declared_id is not None and declared_id != owner_id:
            raise RecoveryFailure(
                "resolution identity differs from its exact route", code=RecoveryFailureCode.CORRUPT
            )


def _hydrate_execution_result(
    repository: object,
    pinned: PinnedCampaign,
    accepted_command: Mapping[str, object],
    resolution: Mapping[str, object],
) -> dict[str, object]:
    command_id = _string_or_failure(accepted_command.get("command_id"), "accepted command_id")
    input_fingerprint = _digest_or_failure(
        accepted_command.get("input_fingerprint"), "accepted input_fingerprint"
    )
    resolution_id = _string_or_failure(
        accepted_command.get("root_resolution_id"), "accepted command root_resolution_id"
    )
    root_command_id = resolution.get("root_command_id")
    if root_command_id is None:
        raise RecoveryFailure(
            "resolution root command identity is missing", code=RecoveryFailureCode.INCOMPLETE
        )
    if root_command_id != command_id:
        raise RecoveryFailure(
            "resolution root command differs from accepted command",
            code=RecoveryFailureCode.CORRUPT,
        )
    segments = resolution.get("segments")
    if not isinstance(segments, list) or not segments:
        raise RecoveryFailure(
            "resolution has no committed execution segments", code=RecoveryFailureCode.INCOMPLETE
        )
    fixed_results = _validate_fixed_rng_results(
        resolution.get("fixed_rng_results", []), "resolution fixed RNG result"
    )

    hydrated_segments: list[Mapping[str, object]] = []
    events_by_id: dict[str, Mapping[str, object]] = {}
    seen_sequences: set[int] = set()
    for raw_segment in segments:
        segment = _mapping_or_failure(raw_segment, "resolution execution segment")
        segment_id = _string_or_failure(segment.get("segment_id"), "segment_id")
        match = re.fullmatch(re.escape(resolution_id) + r":segment:(\d+)", segment_id)
        if match is None:
            raise RecoveryFailure("resolution segment identity is arbitrary", code=RecoveryFailureCode.CORRUPT)
        sequence = int(match.group(1))
        if segment.get("segment_sequence") != sequence or sequence in seen_sequences:
            raise RecoveryFailure(
                "resolution segment sequence is inconsistent", code=RecoveryFailureCode.CORRUPT
            )
        seen_sequences.add(sequence)
        event_ids = segment.get("event_ids")
        if not isinstance(event_ids, list) or not event_ids:
            raise RecoveryFailure(
                "resolution segment event membership is incomplete",
                code=RecoveryFailureCode.INCOMPLETE,
            )
        for raw_event_id in event_ids:
            event_id = _string_or_failure(raw_event_id, "event_id")
            event = _read_pinned_native_record(
                repository,
                pinned,
                "runtime.mechanical_event",
                (event_id,),
                "runtime mechanical event",
            )
            event_copy = deepcopy(dict(event))
            event_copy["event_id"] = event_id
            _validate_event_route_identity(event_copy, resolution_id, command_id, segment_id)
            if event_id in events_by_id:
                raise RecoveryFailure(
                    "resolution event membership is ambiguous", code=RecoveryFailureCode.AMBIGUOUS
                )
            events_by_id[event_id] = event_copy
        hydrated_segments.append(segment)

    selected_segment = max(hydrated_segments, key=lambda item: int(item["segment_sequence"]))
    selected_event_id = _string_or_failure(selected_segment["event_ids"][-1], "event_id")
    result: dict[str, object] = {
        "accepted_command_id": command_id,
        "accepted_input_fingerprint": input_fingerprint,
        "execution_owner_id": resolution_id,
        "resolution_id": resolution_id,
        "status": selected_segment.get("resulting_execution_state", resolution.get("status", "COMPLETED")),
        "segment": deepcopy(dict(selected_segment)),
        "event": deepcopy(dict(events_by_id[selected_event_id])),
        "event_id": selected_event_id,
    }
    if fixed_results:
        result["roll_result"] = deepcopy(dict(fixed_results[-1]))
    return result


def _validate_event_route_identity(
    event: Mapping[str, object], resolution_id: str, command_id: str, segment_id: str
) -> None:
    event_id = _string_or_failure(event.get("event_id"), "event_id")
    match = re.fullmatch(re.escape(segment_id) + r":event:(\d+)", event_id)
    if match is None:
        raise RecoveryFailure("event identity is not derived from its segment", code=RecoveryFailureCode.CORRUPT)
    ordinal = int(match.group(1))
    if event.get("segment_id") != segment_id or event.get("event_ordinal") != ordinal:
        raise RecoveryFailure("event identity differs from its native route", code=RecoveryFailureCode.CORRUPT)
    if event.get("root_command_id") != command_id or event.get("causal_ref") != resolution_id:
        raise RecoveryFailure(
            "event causal identity differs from accepted execution", code=RecoveryFailureCode.CORRUPT
        )


def _validate_catalog_closure(
    repository: object,
    pinned: PinnedCampaign,
    accepted_command: Mapping[str, object],
    catalog_basis: Mapping[str, object],
) -> None:
    resolver = getattr(repository, "resolve_recovery_catalog_context", None)
    if callable(resolver):
        try:
            resolved = resolver(pinned, accepted_command, catalog_basis)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            raise RecoveryFailure(
                "accepted catalog basis could not be reconstructed", code=RecoveryFailureCode.INCOMPLETE
            ) from exc
        if not isinstance(resolved, tuple) or len(resolved) != 2:
            raise RecoveryFailure(
                "catalog recovery validator did not return typed context and candidate",
                code=RecoveryFailureCode.CORRUPT,
            )
        context, candidate = resolved
        if not isinstance(context, BoundCatalogContext):
            raise RecoveryFailure(
                "catalog recovery validator returned untyped context",
                code=RecoveryFailureCode.CORRUPT,
            )
        try:
            validate_execution_proposal(accepted_command, context, candidate)
        except (CatalogBindingError, CommandAcceptanceError, TypeError, ValueError) as exc:
            raise RecoveryFailure(
                "accepted catalog basis failed owner validation", code=RecoveryFailureCode.STALE
            ) from exc
        return
    raise RecoveryFailure(
        "accepted catalog basis lacks an owner validation boundary",
        code=RecoveryFailureCode.INCOMPLETE,
    )


def _recovered_policy_basis(
    repository: object,
    pinned: PinnedCampaign,
    accepted_command: Mapping[str, object],
) -> Mapping[str, object]:
    refs = _accepted_policy_refs(accepted_command)
    basis: dict[str, object] = {
        "policy_refs": list(refs),
        "action_request": deepcopy(_mapping_or_failure(accepted_command.get("action_request"), "action_request")),
        "invocation_facts": deepcopy(accepted_command.get("invocation_facts", [])),
    }
    if not refs:
        return basis
    resolver = getattr(repository, "resolve_recovery_policy_basis", None)
    if not callable(resolver):
        raise RecoveryFailure(
            "accepted policy basis lacks an owner validation boundary",
            code=RecoveryFailureCode.INCOMPLETE,
        )
    try:
        resolved = resolver(pinned, accepted_command, tuple(refs))
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
        raise RecoveryFailure(
            "accepted policy basis could not be reconstructed", code=RecoveryFailureCode.INCOMPLETE
        ) from exc
    if not isinstance(resolved, Mapping):
        raise RecoveryFailure(
            "policy recovery validator returned untyped evidence", code=RecoveryFailureCode.CORRUPT
        )
    basis.update(deepcopy(dict(resolved)))
    return basis


def _validate_event_identity(
    result: Mapping[str, object],
    resolution_id: str,
    segment: Mapping[str, object],
    segment_id: str,
    event: Mapping[str, object],
) -> None:
    match = re.fullmatch(re.escape(resolution_id) + r":segment:(\d+)", segment_id)
    if match is None:
        raise RecoveryFailure("execution segment identity is arbitrary", code=RecoveryFailureCode.CORRUPT)
    sequence = int(match.group(1))
    if segment.get("segment_sequence") != sequence:
        raise RecoveryFailure("execution segment sequence differs from identity", code=RecoveryFailureCode.CORRUPT)
    event_id = _string_or_failure(result.get("event_id"), "event_id")
    event_match = re.fullmatch(re.escape(segment_id) + r":event:(\d+)", event_id)
    if event_match is None:
        raise RecoveryFailure("execution event identity is arbitrary", code=RecoveryFailureCode.CORRUPT)
    event_ordinal = int(event_match.group(1))
    if event.get("event_id") is not None and event.get("event_id") != event_id:
        raise RecoveryFailure("execution event ID differs from derived identity", code=RecoveryFailureCode.CORRUPT)
    if event.get("segment_id") != segment_id or event.get("event_ordinal") != event_ordinal:
        raise RecoveryFailure("execution event identity is arbitrary", code=RecoveryFailureCode.CORRUPT)
    event_ids = segment.get("event_ids")
    if event_ids is not None:
        if not isinstance(event_ids, list) or event_id not in event_ids:
            raise RecoveryFailure("execution segment event membership is corrupt", code=RecoveryFailureCode.CORRUPT)
    elif event_ordinal != 1:
        raise RecoveryFailure("execution event ordinal is not owner-derived", code=RecoveryFailureCode.CORRUPT)


def _validate_roll_identity(roll: Mapping[str, object]) -> None:
    expected = {"roll_id", "request_id", "expression", "raw_values", "source_kind", "provenance_ref"}
    if set(roll) != expected:
        raise RecoveryFailure("fixed RNG evidence is malformed", code=RecoveryFailureCode.CORRUPT)
    for field in ("roll_id", "request_id"):
        value = _string_or_failure(roll.get(field), field)
        if _NATIVE_ID.fullmatch(value) is None:
            raise RecoveryFailure(
                f"{field} is not a valid native identifier", code=RecoveryFailureCode.CORRUPT
            )
    _string_or_failure(roll.get("expression"), "roll expression")
    raw_values = roll.get("raw_values")
    if (
        not isinstance(raw_values, Sequence)
        or isinstance(raw_values, (str, bytes))
        or not raw_values
        or any(isinstance(value, bool) or not isinstance(value, int) for value in raw_values)
    ):
        raise RecoveryFailure("fixed RNG raw values are malformed", code=RecoveryFailureCode.CORRUPT)
    if roll.get("source_kind") not in {"rng.system", "rng.player", "rng.external"}:
        raise RecoveryFailure("fixed RNG source kind is unsupported", code=RecoveryFailureCode.CORRUPT)
    _string_or_failure(roll.get("provenance_ref"), "RNG provenance reference")


def _validate_fixed_rng_results(value: object, label: str) -> list[Mapping[str, object]]:
    if not isinstance(value, list):
        raise RecoveryFailure("resolution fixed RNG evidence is malformed", code=RecoveryFailureCode.CORRUPT)
    validated: list[Mapping[str, object]] = []
    seen_request_ids: set[str] = set()
    for raw_roll in value:
        roll = _mapping_or_failure(raw_roll, label)
        _validate_roll_identity(roll)
        request_id = _string_or_failure(roll.get("request_id"), "request_id")
        if request_id in seen_request_ids:
            raise RecoveryFailure(
                "fixed RNG request ID is duplicated", code=RecoveryFailureCode.AMBIGUOUS
            )
        seen_request_ids.add(request_id)
        validated.append(roll)
    return validated


def _validate_resolution_closure(
    resolution: object,
    resolution_id: str,
    command_id: str,
    segment: Mapping[str, object],
    roll: Mapping[str, object],
) -> None:
    value = _mapping_or_failure(resolution, "resolution closure")
    if value.get("resolution_id") is not None and value.get("resolution_id") != resolution_id:
        raise RecoveryFailure("resolution identity differs from execution", code=RecoveryFailureCode.CORRUPT)
    if "root_command_id" not in value:
        raise RecoveryFailure("resolution root command is missing", code=RecoveryFailureCode.INCOMPLETE)
    if value.get("root_command_id") != command_id:
        raise RecoveryFailure("resolution root command differs from accepted command", code=RecoveryFailureCode.CORRUPT)
    segments = value.get("segments")
    if not isinstance(segments, list) or not any(item == segment for item in segments):
        raise RecoveryFailure("resolution closure does not contain execution segment", code=RecoveryFailureCode.INCOMPLETE)
    fixed = value.get("fixed_rng_results")
    if fixed is not None:
        validated_fixed = _validate_fixed_rng_results(fixed, "resolution fixed RNG result")
        if roll and not any(item == roll for item in validated_fixed):
            raise RecoveryFailure("resolution closure does not contain fixed RNG evidence", code=RecoveryFailureCode.INCOMPLETE)
    elif roll:
        raise RecoveryFailure("resolution closure does not contain fixed RNG evidence", code=RecoveryFailureCode.INCOMPLETE)


def _validate_root_owner(
    campaign_id: str, root: Mapping[str, object], owner: Mapping[str, object]
) -> None:
    owner_kind = str(root["owner_kind"])
    owner_id = str(root["owner_id"])
    declared_kind = owner.get("kind")
    if declared_kind != owner_kind and not (
        declared_kind is None and owner_kind == "runtime.command"
    ):
        raise RecoveryFailure("root owner kind differs from route", code=RecoveryFailureCode.CORRUPT)
    try:
        delta = derive_operational_root_delta(
            campaign_id, owner_kind, owner, existing_roots=(root,)
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise RecoveryFailure(
            "operational root owner state is not valid native evidence",
            code=RecoveryFailureCode.CORRUPT,
        ) from exc
    if delta.root.owner_id != owner_id:
        raise RecoveryFailure("root owner identity differs from route", code=RecoveryFailureCode.CORRUPT)
    if delta.action == "REMOVE":
        raise RecoveryFailure("operational root owner is terminal", code=RecoveryFailureCode.STALE)
