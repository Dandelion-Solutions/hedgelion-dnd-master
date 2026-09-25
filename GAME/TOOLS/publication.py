"""Bounded campaign publication freeze, plan and outcome contracts.

The module prepares one campaign-domain tree/ref closure.  It does not perform
network I/O, create a journal, retry a write blindly, or own any campaign
currentness, policy, lifecycle, or storage metadata.
"""

from __future__ import annotations

import hashlib
import json
import re
import weakref
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, StrEnum
from types import MappingProxyType
from typing import Final

from .durability import (
    ExecutionDurabilityJoin,
    RoutedSerializedOperation,
    _policy_refs,
    is_execution_durability_join,
)
from .policy_basis import AuthenticatedPrincipalEvidence, PinnedCampaign
from .recovery_roots import (
    OperationalRootDelta,
    validate_operational_root_delta,
)

# framework_module_version: 1.0.6
FRAMEWORK_MODULE_VERSION: Final = "1.0.6"
OPERATIONAL_ROOT_MEMBERSHIP_PATH: Final = "STATE/RUNTIME/RECOVERY_ROOTS/ROUTING.yaml"
_SHA40_OR_64: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_SHA256: Final = re.compile(r"^[a-f0-9]{64}$")
_ID: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_IMMUTABLE_CAMPAIGN_PATHS: Final = frozenset({"MANIFEST.yaml", "CAMPAIGN_CARD.yaml"})
_STORAGE_PATH_MARKERS: Final = frozenset({"DND_STORAGE.yaml", "DND_STORAGE"})


class PublicationContractError(ValueError):
    """Raised when a publication attempt cannot be frozen safely."""


class PublicationStatus(str, Enum):
    ACCEPTED = "CONFIRMED_ACCEPTED"
    REJECTED = "CONFIRMED_REJECTED"
    CONFLICT = "CONFLICT"
    INDETERMINATE = "INDETERMINATE"


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PublicationContractError(f"{label} must be a nonempty string")
    return value


def _machine_id(value: object, label: str) -> str:
    result = _nonempty(value, label)
    if _ID.fullmatch(result) is None:
        raise PublicationContractError(f"{label} must be a machine identifier")
    return result


def _revision(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA40_OR_64.fullmatch(value) is None:
        raise PublicationContractError(f"{label} must be a lowercase Git revision")
    return value


def _sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise PublicationContractError(f"{label} must be a SHA-256 digest")
    return value


def _json_copy(value: object, label: str) -> object:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if value != value or value in {float("inf"), float("-inf")}:
            raise PublicationContractError(f"{label} must not contain a non-finite number")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise PublicationContractError(f"{label} keys must be strings")
        return {key: _json_copy(item, f"{label}.{key}") for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_copy(item, f"{label}[{index}]") for index, item in enumerate(value)]
    raise PublicationContractError(f"{label} must contain JSON-compatible values")


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_thaw(item) for item in value]
    return value


def _serialized_operation_digest(value: object) -> str:
    copied = _json_copy(value, "serialized operation")
    encoded = json.dumps(copied, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _path(value: object) -> str:
    result = _nonempty(value, "publication path")
    if result.startswith("/") or "//" in result or any(part in {"", ".", ".."} for part in result.split("/")):
        raise PublicationContractError("publication path is not normalized")
    return result


def _require_execution_join_for_route(
    routed_operation: RoutedSerializedOperation,
    execution_durability_join: ExecutionDurabilityJoin | None,
) -> None:
    if routed_operation.owner_kind == "runtime.command" and execution_durability_join is None:
        raise PublicationContractError("runtime.command publication requires an execution/durability join")


@dataclass(frozen=True, slots=True)
class CampaignIdentity:
    campaign_id: str
    campaign_name: str | None
    branch: str
    created_at: str

    def __post_init__(self) -> None:
        _machine_id(self.campaign_id, "campaign identity campaign_id")
        _nonempty(self.branch, "campaign identity branch")
        _nonempty(self.created_at, "campaign identity created_at")


@dataclass(frozen=True, slots=True)
class AcceptedExecutionIdentity:
    command_id: str
    input_fingerprint: str
    resolution_id: str
    segment_id: str
    event_id: str

    def __post_init__(self) -> None:
        _machine_id(self.command_id, "accepted command_id")
        _sha256(self.input_fingerprint, "accepted input_fingerprint")
        _machine_id(self.resolution_id, "accepted resolution_id")
        _nonempty(self.segment_id, "accepted segment_id")
        _nonempty(self.event_id, "accepted event_id")


@dataclass(frozen=True, slots=True)
class CommitAncestryEvidence:
    """Typed repository evidence that one exact commit is an ancestor of another."""

    ancestor_sha: str
    descendant_sha: str
    relation: str = "ANCESTOR"

    def __post_init__(self) -> None:
        _revision(self.ancestor_sha, "ancestry ancestor")
        _revision(self.descendant_sha, "ancestry descendant")
        if self.ancestor_sha == self.descendant_sha:
            raise PublicationContractError("ancestry evidence must contain distinct commits")
        if self.relation != "ANCESTOR":
            raise PublicationContractError("unsupported commit ancestry relation")


@dataclass(frozen=True, slots=True)
class PublicationCurrentClosureEvidence:
    """Typed bounded diff evidence returned by the authoritative current-source read."""

    base_revision: str
    head_sha: str
    tree_sha: str
    operation_digests: Mapping[str, str]

    def __post_init__(self) -> None:
        _revision(self.base_revision, "closure base revision")
        _revision(self.head_sha, "closure head")
        _revision(self.tree_sha, "closure tree")
        normalized: dict[str, str] = {}
        for path, digest in self.operation_digests.items():
            normalized[_path(path)] = _sha256(digest, "closure operation digest")
        if not normalized:
            raise PublicationContractError("current closure operation evidence is required")
        object.__setattr__(self, "operation_digests", MappingProxyType(normalized))

    def to_dict(self) -> dict[str, object]:
        return {
            "base_revision": self.base_revision,
            "head_sha": self.head_sha,
            "tree_sha": self.tree_sha,
            "operation_digests": dict(self.operation_digests),
        }


@dataclass(frozen=True, slots=True)
class FrozenCampaignPublicationAttempt:
    """Immutable pre-mutation campaign publication evidence."""

    repository_id: str
    target_ref: str
    campaign_id: str
    acting_principal: AuthenticatedPrincipalEvidence
    pinned_head_sha: str
    base_tree_sha: str
    campaign_identity: CampaignIdentity
    path_operations: Mapping[str, object | None]
    deleted_paths: tuple[str, ...]
    owner_generations: Mapping[str, int]
    accepted_identity: AcceptedExecutionIdentity | None
    fixed_rng_values: tuple[int, ...]
    catalog_basis: Mapping[str, object]
    policy_basis: Mapping[str, object]
    procedure_before: Mapping[str, object] | None
    procedure_after: Mapping[str, object] | None
    root_delta: OperationalRootDelta | None
    root_membership_before: Mapping[str, object] | None
    currentness_evidence: PinnedCampaign
    publication_reason: str
    execution_durability_join: ExecutionDurabilityJoin | None
    routed_operation: RoutedSerializedOperation
    native_domains: tuple[str, ...] = ("campaign",)

    def __post_init__(self) -> None:
        _nonempty(self.repository_id, "repository identity")
        _nonempty(self.target_ref, "target campaign ref")
        _machine_id(self.campaign_id, "campaign_id")
        _revision(self.pinned_head_sha, "pinned_head_sha")
        _revision(self.base_tree_sha, "base_tree_sha")
        if not isinstance(self.acting_principal, AuthenticatedPrincipalEvidence):
            raise PublicationContractError("Access-owner-typed acting principal evidence is required")
        if not isinstance(self.currentness_evidence, PinnedCampaign):
            raise PublicationContractError("currentness evidence must be owner-typed")
        if self.currentness_evidence.campaign_id != self.campaign_id:
            raise PublicationContractError("currentness evidence campaign differs from publication")
        if self.currentness_evidence.revision != self.pinned_head_sha:
            raise PublicationContractError("currentness evidence does not bind pinned head")
        if self.currentness_evidence.tree_sha != self.base_tree_sha:
            raise PublicationContractError("currentness evidence does not bind pinned tree")
        if not isinstance(self.routed_operation, RoutedSerializedOperation):
            raise PublicationContractError("owner-routed serialized operation is required")
        _require_execution_join_for_route(self.routed_operation, self.execution_durability_join)
        if self.execution_durability_join is not None:
            if not is_execution_durability_join(self.execution_durability_join):
                raise PublicationContractError("owner-issued execution/durability join is invalid")
            if self.execution_durability_join.routed_operation != self.routed_operation:
                raise PublicationContractError("execution/durability route differs from publication route")
            if self.execution_durability_join.campaign_id != self.campaign_id:
                raise PublicationContractError("execution/durability join campaign differs from publication")
        operations = {
            _path(path): _json_copy(value, f"path operation {path}")
            for path, value in self.path_operations.items()
        }
        object.__setattr__(self, "path_operations", _freeze(operations))
        object.__setattr__(self, "deleted_paths", tuple(sorted(self.deleted_paths)))
        generations: dict[str, int] = {}
        for key, value in self.owner_generations.items():
            _nonempty(key, "owner generation key")
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise PublicationContractError("owner generation must be a non-negative integer")
            generations[key] = value
        object.__setattr__(self, "owner_generations", MappingProxyType(generations))
        catalog = _json_copy(self.catalog_basis, "catalog basis")
        policy = _json_copy(self.policy_basis, "policy basis")
        if not isinstance(catalog, dict) or not isinstance(policy, dict):
            raise PublicationContractError("catalog and policy bases must be objects")
        if isinstance(policy.get("policy_refs"), list):
            policy["policy_refs"] = tuple(policy["policy_refs"])
        object.__setattr__(self, "catalog_basis", _freeze(catalog))
        object.__setattr__(self, "policy_basis", _freeze(policy))
        if self.procedure_before is not None:
            object.__setattr__(self, "procedure_before", _freeze(_json_copy(self.procedure_before, "procedure_before")))
        if self.procedure_after is not None:
            object.__setattr__(self, "procedure_after", _freeze(_json_copy(self.procedure_after, "procedure_after")))
        if self.root_membership_before is not None:
            object.__setattr__(self, "root_membership_before", _freeze(_json_copy(self.root_membership_before, "root_membership_before")))
        if any(isinstance(value, bool) or not isinstance(value, int) for value in self.fixed_rng_values):
            raise PublicationContractError("fixed RNG evidence must contain integers")
        _nonempty(self.publication_reason, "publication reason")
        if self.native_domains != ("campaign",):
            raise PublicationContractError("campaign attempt may contain only the campaign domain")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 2,
            "repository_id": self.repository_id,
            "target_ref": self.target_ref,
            "campaign_id": self.campaign_id,
            "acting_principal": {
                "principal_id": self.acting_principal.principal_id,
                "evidence_type": "authenticated_access_owner",
            },
            "pinned_head_sha": self.pinned_head_sha,
            "base_tree_sha": self.base_tree_sha,
            "campaign_identity": {
                "campaign_id": self.campaign_identity.campaign_id,
                "campaign_name": self.campaign_identity.campaign_name,
                "branch": self.campaign_identity.branch,
                "created_at": self.campaign_identity.created_at,
            },
            "path_operations": _thaw(self.path_operations),
            "deleted_paths": list(self.deleted_paths),
            "owner_generations": _thaw(self.owner_generations),
            "accepted_identity": None
            if self.accepted_identity is None
            else {
                "command_id": self.accepted_identity.command_id,
                "input_fingerprint": self.accepted_identity.input_fingerprint,
                "resolution_id": self.accepted_identity.resolution_id,
                "segment_id": self.accepted_identity.segment_id,
                "event_id": self.accepted_identity.event_id,
            },
            "fixed_rng_values": list(self.fixed_rng_values),
            "catalog_basis": _thaw(self.catalog_basis),
            "policy_basis": _thaw(self.policy_basis),
            "procedure_before": _thaw(self.procedure_before),
            "procedure_after": _thaw(self.procedure_after),
            "root_delta": None if self.root_delta is None else self.root_delta.to_dict(),
            "root_membership_before": _thaw(self.root_membership_before),
            "currentness_evidence": {
                "campaign_id": self.currentness_evidence.campaign_id,
                "revision": self.currentness_evidence.revision,
                "tree_sha": self.currentness_evidence.tree_sha,
            },
            "publication_reason": self.publication_reason,
            "execution_durability_join": None
            if self.execution_durability_join is None
            else self.execution_durability_join.to_dict(),
            "routed_operation": self.routed_operation.to_dict(),
            "native_domains": list(self.native_domains),
        }

    def publication_closure_digest(self, intended_commit_sha: str) -> str:
        """Digest the exact bounded commit closure for authoritative reconciliation."""

        intended = _revision(intended_commit_sha, "intended commit")
        material = {
            "parent_sha": self.pinned_head_sha,
            "base_tree_sha": self.base_tree_sha,
            "commit_sha": intended,
            "path_operations": _thaw(self.path_operations),
        }
        encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        return hashlib.sha256(encoded).hexdigest()

    def publication_operation_digests(self) -> dict[str, str]:
        """Return per-path digests used by an authoritative descendant-closure read."""

        return {
            path: _serialized_operation_digest(value)
            for path, value in self.path_operations.items()
        }


@dataclass(frozen=True, slots=True)
class FrozenCampaignPublicationRecoveryBasis:
    """Ephemeral W02 basis for revalidating an already-published owner delta."""

    repository_id: str
    target_ref: str
    campaign_id: str
    pinned_head_sha: str
    base_tree_sha: str
    intended_commit_sha: str
    campaign_identity: CampaignIdentity
    path_operations: Mapping[str, object | None]
    owner_generations: Mapping[str, int]
    routed_operation: RoutedSerializedOperation
    publication_reason: str

    def __post_init__(self) -> None:
        _nonempty(self.repository_id, "repository identity")
        _nonempty(self.target_ref, "target campaign ref")
        _machine_id(self.campaign_id, "campaign_id")
        _revision(self.pinned_head_sha, "pinned_head_sha")
        _revision(self.base_tree_sha, "base_tree_sha")
        _revision(self.intended_commit_sha, "intended commit")
        if self.pinned_head_sha == self.intended_commit_sha:
            raise PublicationContractError(
                "revalidated publication commit must differ from its predecessor"
            )
        if not isinstance(self.campaign_identity, CampaignIdentity):
            raise PublicationContractError(
                "recovery basis campaign identity is not typed"
            )
        if (
            self.campaign_identity.campaign_id != self.campaign_id
            or self.campaign_identity.branch != self.target_ref
        ):
            raise PublicationContractError(
                "recovery basis campaign identity differs from its bound ref"
            )
        if not isinstance(self.routed_operation, RoutedSerializedOperation):
            raise PublicationContractError(
                "owner-routed serialized operation is required"
            )
        _require_execution_join_for_route(self.routed_operation, None)
        if not isinstance(self.path_operations, Mapping) or not self.path_operations:
            raise PublicationContractError(
                "recovery basis requires a nonempty path delta"
            )
        operations: dict[str, object | None] = {}
        for raw_path, value in self.path_operations.items():
            path = _path(raw_path)
            if path in _STORAGE_PATH_MARKERS or path.startswith("DND_STORAGE/"):
                raise PublicationContractError(
                    "storage metadata is a separate native transaction"
                )
            if path == "LIVE_STATE.yaml" or path.startswith("LIVE/"):
                raise PublicationContractError(
                    "live state is a separate native transaction"
                )
            operations[path] = _json_copy(value, f"path operation {path}")

        manifest_operation = operations.get("MANIFEST.yaml")
        card_operation = operations.get("CAMPAIGN_CARD.yaml")
        identity = self.campaign_identity
        if "MANIFEST.yaml" in operations:
            if not isinstance(manifest_operation, Mapping):
                raise PublicationContractError(
                    "MANIFEST.yaml must retain canonical identity fields"
                )
            for field in ("campaign_id", "branch", "created_at"):
                if manifest_operation.get(field) != getattr(identity, field):
                    raise PublicationContractError(
                        "canonical campaign identity is immutable"
                    )
        if "CAMPAIGN_CARD.yaml" in operations and (
            not isinstance(card_operation, Mapping)
            or card_operation.get("campaign_id") != self.campaign_id
            or "campaign_name" not in card_operation
        ):
            raise PublicationContractError("campaign card identity is immutable")
        resulting_manifest_name = (
            manifest_operation.get("campaign_name", identity.campaign_name)
            if isinstance(manifest_operation, Mapping)
            else identity.campaign_name
        )
        resulting_card_name = (
            card_operation.get("campaign_name", identity.campaign_name)
            if isinstance(card_operation, Mapping)
            else identity.campaign_name
        )
        if resulting_manifest_name != resulting_card_name:
            raise PublicationContractError(
                "campaign name projection differs in recovery operation set"
            )
        if operations.get(self.routed_operation.relative_path) != _thaw(
            self.routed_operation.payload
        ):
            raise PublicationContractError(
                "owner-routed serialized operation is missing or mismatched"
            )
        object.__setattr__(self, "path_operations", _freeze(operations))

        if not isinstance(self.owner_generations, Mapping):
            raise PublicationContractError("owner generations must be a mapping")
        generations: dict[str, int] = {}
        for owner, generation in self.owner_generations.items():
            generations[_nonempty(owner, "owner generation key")] = generation
            if (
                isinstance(generation, bool)
                or not isinstance(generation, int)
                or generation < 0
            ):
                raise PublicationContractError(
                    "owner generation must be a non-negative integer"
                )
        object.__setattr__(self, "owner_generations", MappingProxyType(generations))
        _nonempty(self.publication_reason, "publication reason")

    def publication_operation_digests(self) -> dict[str, str]:
        """Return exact per-path after-image digests for this recovery basis."""

        return {
            path: _serialized_operation_digest(value)
            for path, value in self.path_operations.items()
        }


def _campaign_identity(
    campaign_id: str,
    manifest: Mapping[str, object],
    campaign_card: Mapping[str, object],
) -> CampaignIdentity:
    if manifest.get("campaign_id") != campaign_id or campaign_card.get("campaign_id") != campaign_id:
        raise PublicationContractError("campaign identity is not canonical")
    if manifest.get("campaign_name") != campaign_card.get("campaign_name"):
        raise PublicationContractError("campaign name projection differs from manifest")
    campaign_name = manifest.get("campaign_name")
    if campaign_name is not None and not isinstance(campaign_name, str):
        raise PublicationContractError("campaign name must be text or null")
    branch = _nonempty(manifest.get("branch"), "manifest branch")
    created_at = _nonempty(manifest.get("created_at"), "manifest created_at")
    return CampaignIdentity(
        campaign_id=campaign_id,
        campaign_name=campaign_name,
        branch=branch,
        created_at=created_at,
    )


def freeze_campaign_publication_recovery_basis(
    *,
    repository_id: str,
    target_ref: str,
    campaign_id: str,
    pinned_head_sha: str,
    base_tree_sha: str,
    intended_commit_sha: str,
    manifest: Mapping[str, object],
    campaign_card: Mapping[str, object],
    path_operations: Mapping[str, object | None],
    owner_generations: Mapping[str, int],
    routed_operation: RoutedSerializedOperation,
    publication_reason: str,
) -> FrozenCampaignPublicationRecoveryBasis:
    """Freeze read-only recovery inputs against the exact H campaign basis."""

    if not isinstance(manifest, Mapping) or not isinstance(campaign_card, Mapping):
        raise PublicationContractError(
            "recovery predecessor manifest and campaign card are required"
        )
    identity = _campaign_identity(campaign_id, manifest, campaign_card)
    if identity.branch != target_ref:
        raise PublicationContractError(
            "target ref differs from canonical predecessor campaign branch"
        )
    return FrozenCampaignPublicationRecoveryBasis(
        repository_id=repository_id,
        target_ref=target_ref,
        campaign_id=campaign_id,
        pinned_head_sha=pinned_head_sha,
        base_tree_sha=base_tree_sha,
        intended_commit_sha=intended_commit_sha,
        campaign_identity=identity,
        path_operations=path_operations,
        owner_generations=owner_generations,
        routed_operation=routed_operation,
        publication_reason=publication_reason,
    )


def _accepted_identity(
    accepted_command: Mapping[str, object] | None,
    execution: Mapping[str, object] | None,
) -> tuple[AcceptedExecutionIdentity | None, tuple[int, ...], Mapping[str, object]]:
    if accepted_command is None and execution is None:
        return None, (), {}
    if not isinstance(accepted_command, Mapping) or not isinstance(execution, Mapping):
        raise PublicationContractError("accepted command and execution must join together")
    command_id = _machine_id(accepted_command.get("command_id"), "accepted command_id")
    input_fingerprint = _sha256(accepted_command.get("input_fingerprint"), "accepted input_fingerprint")
    if execution.get("accepted_command_id") != command_id or execution.get("accepted_input_fingerprint") != input_fingerprint:
        raise PublicationContractError("execution and accepted identity differ")
    resolution_id = _machine_id(execution.get("resolution_id"), "execution resolution_id")
    segment = execution.get("segment")
    event = execution.get("event")
    if not isinstance(segment, Mapping) or not isinstance(event, Mapping):
        raise PublicationContractError("execution segment and event evidence are required")
    segment_id = _nonempty(segment.get("segment_id"), "execution segment_id")
    event_id = _nonempty(execution.get("event_id"), "execution event_id")
    roll = execution.get("roll_result")
    values: tuple[int, ...] = ()
    if isinstance(roll, Mapping):
        raw_values = roll.get("raw_values", ())
        if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)):
            raise PublicationContractError("fixed RNG evidence is malformed")
        values = tuple(raw_values)
        if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
            raise PublicationContractError("fixed RNG evidence must contain integers")
    catalog = accepted_command.get("catalog_context")
    if not isinstance(catalog, Mapping):
        raise PublicationContractError("accepted catalog basis is required")
    return (
        AcceptedExecutionIdentity(command_id, input_fingerprint, resolution_id, segment_id, event_id),
        values,
        dict(catalog),
    )


def _root_page_after(
    before: Mapping[str, object], delta: OperationalRootDelta
) -> dict[str, object]:
    if before.get("schema_version") != 1 or before.get("complete") is not True:
        raise PublicationContractError("root membership must be a complete native routing page")
    if before.get("campaign_id") != delta.campaign_id:
        raise PublicationContractError("root membership campaign differs from publication")
    roots = before.get("roots")
    if not isinstance(roots, list):
        raise PublicationContractError("root membership roots must be an array")
    expected = (delta.root.owner_kind, delta.root.owner_id)
    copied = [deepcopy(root) for root in roots]
    matches = [
        root
        for root in copied
        if isinstance(root, Mapping)
        and root.get("owner_kind") == expected[0]
        and root.get("owner_id") == expected[1]
    ]
    if delta.action == "REMOVE":
        if len(matches) != 1:
            raise PublicationContractError("root removal lacks current membership evidence")
        copied = [
            root
            for root in copied
            if not (
                isinstance(root, Mapping)
                and root.get("owner_kind") == expected[0]
                and root.get("owner_id") == expected[1]
            )
        ]
    elif delta.action == "ENROLL":
        if matches:
            raise PublicationContractError("root enrollment is not a membership mutation")
        copied.append(delta.root.to_dict())
    elif delta.action != "NOOP":
        raise PublicationContractError("unsupported root membership delta")
    copied.sort(key=lambda root: (str(root.get("owner_kind")), str(root.get("owner_id"))))
    return {
        "schema_version": 1,
        "campaign_id": delta.campaign_id,
        "complete": True,
        "roots": copied,
    }


def freeze_campaign_publication_attempt(
    *,
    repository_id: str,
    target_ref: str,
    campaign_id: str,
    acting_principal: AuthenticatedPrincipalEvidence,
    pinned_head_sha: str,
    base_tree_sha: str,
    manifest: Mapping[str, object],
    campaign_card: Mapping[str, object],
    path_operations: Mapping[str, object | None],
    owner_generations: Mapping[str, int],
    currentness_evidence: PinnedCampaign | None = None,
    execution_durability_join: ExecutionDurabilityJoin | None = None,
    routed_operation: RoutedSerializedOperation | None = None,
    accepted_command: Mapping[str, object] | None = None,
    execution: Mapping[str, object] | None = None,
    policy_basis: Mapping[str, object] | None = None,
    catalog_basis: Mapping[str, object] | None = None,
    procedure_before: Mapping[str, object] | None = None,
    procedure_after: Mapping[str, object] | None = None,
    root_delta: OperationalRootDelta | None = None,
    root_membership_before: Mapping[str, object] | None = None,
    publication_reason: str = "durability",
) -> FrozenCampaignPublicationAttempt:
    """Freeze all campaign writes and their exact parent/currentness evidence."""

    if currentness_evidence is None:
        raise PublicationContractError("captured currentness evidence is required")
    if not isinstance(routed_operation, RoutedSerializedOperation):
        raise PublicationContractError("owner-routed serialized operation is required")
    _require_execution_join_for_route(routed_operation, execution_durability_join)
    if execution_durability_join is not None:
        if not isinstance(execution_durability_join, ExecutionDurabilityJoin) or not is_execution_durability_join(
            execution_durability_join
        ):
            raise PublicationContractError("owner-issued execution/durability join is invalid")
        if execution_durability_join.routed_operation != routed_operation:
            raise PublicationContractError("execution/durability route differs from publication route")
        if accepted_command is None:
            accepted_command = _thaw(execution_durability_join.accepted_command)
        if execution is None:
            execution = _thaw(execution_durability_join.execution)
        if accepted_command != _thaw(execution_durability_join.accepted_command):
            raise PublicationContractError("accepted command differs from typed execution/durability join")
        if execution != _thaw(execution_durability_join.execution):
            raise PublicationContractError("execution evidence differs from typed execution/durability join")
    elif accepted_command is not None or execution is not None:
        raise PublicationContractError("execution-backed publication requires an execution/durability join")
    identity = _campaign_identity(campaign_id, manifest, campaign_card)
    if identity.branch != target_ref:
        raise PublicationContractError("target ref differs from canonical campaign branch")
    _nonempty(publication_reason, "publication reason")
    operations = {path: value for path, value in path_operations.items()}
    for path, value in operations.items():
        normalized = _path(path)
        if normalized in _STORAGE_PATH_MARKERS or normalized.startswith("DND_STORAGE/"):
            raise PublicationContractError("storage metadata is a separate native transaction")
        if normalized == "LIVE_STATE.yaml" or normalized.startswith("LIVE/"):
            raise PublicationContractError("live state is a separate native transaction")
        if normalized in _IMMUTABLE_CAMPAIGN_PATHS and value is None:
            raise PublicationContractError("canonical campaign identity records cannot be deleted")
        if normalized in _IMMUTABLE_CAMPAIGN_PATHS and isinstance(value, Mapping):
            if value.get("campaign_id") != campaign_id:
                raise PublicationContractError("campaign identity is immutable")
    manifest_operation = operations.get("MANIFEST.yaml")
    card_operation = operations.get("CAMPAIGN_CARD.yaml")
    if manifest_operation is not None:
        if not isinstance(manifest_operation, Mapping):
            raise PublicationContractError("MANIFEST.yaml must retain canonical identity fields")
        for field in ("campaign_id", "branch", "created_at"):
            if manifest_operation.get(field) != getattr(identity, field):
                raise PublicationContractError("canonical campaign identity is immutable")
    if card_operation is not None:
        if not isinstance(card_operation, Mapping) or card_operation.get("campaign_id") != campaign_id:
            raise PublicationContractError("canonical campaign identity is immutable")
        if "campaign_name" not in card_operation:
            raise PublicationContractError("campaign card must retain synchronized campaign name")
    if isinstance(manifest_operation, Mapping) or isinstance(card_operation, Mapping):
        resulting_manifest_name = (
            manifest_operation.get("campaign_name", manifest.get("campaign_name"))
            if isinstance(manifest_operation, Mapping)
            else manifest.get("campaign_name")
        )
        resulting_card_name = (
            card_operation.get("campaign_name", campaign_card.get("campaign_name"))
            if isinstance(card_operation, Mapping)
            else campaign_card.get("campaign_name")
        )
        if resulting_manifest_name != resulting_card_name:
            raise PublicationContractError("campaign name projection differs in publication delta")
    if root_delta is not None:
        if not isinstance(root_delta, OperationalRootDelta):
            raise PublicationContractError("root delta must be owner-derived typed evidence")
        if procedure_after is None or procedure_before is None or root_membership_before is None:
            raise PublicationContractError("procedure/root publication closure is incomplete")
        before_state = procedure_before.get("state")
        after_state = procedure_after.get("state")
        if not isinstance(before_state, Mapping) or not isinstance(after_state, Mapping):
            raise PublicationContractError("procedure transition lacks native state")
        if root_delta.action == "REMOVE":
            if before_state.get("lifecycle") != "ACTIVE" or after_state.get("lifecycle") != "TERMINAL":
                raise PublicationContractError("root removal requires ACTIVE to TERMINAL procedure transition")
            if procedure_before.get("id") != procedure_after.get("id"):
                raise PublicationContractError("procedure transition changes native identity")
        try:
            validate_operational_root_delta(root_delta, native_owner=procedure_after)
        except ValueError as exc:
            raise PublicationContractError("root delta lacks native lifecycle evidence") from exc
        owner_path = root_delta.root.relative_path
        procedure_payload = deepcopy(dict(procedure_after))
        if owner_path in operations and operations[owner_path] != procedure_payload:
            raise PublicationContractError("procedure owner has duplicate publication writer")
        operations[owner_path] = procedure_payload
        if root_delta.action != "NOOP":
            root_after = _root_page_after(root_membership_before, root_delta)
            if OPERATIONAL_ROOT_MEMBERSHIP_PATH in operations:
                raise PublicationContractError("root membership has duplicate publication writer")
            operations[OPERATIONAL_ROOT_MEMBERSHIP_PATH] = root_after
    operation_payload = _thaw(routed_operation.payload)
    if operations.get(routed_operation.relative_path) != operation_payload:
        raise PublicationContractError("owner-routed serialized operation is missing or mismatched")
    accepted_identity, fixed_rng_values, accepted_catalog = _accepted_identity(accepted_command, execution)
    joined_catalog = (
        _thaw(execution_durability_join.catalog_basis)
        if execution_durability_join is not None
        else {}
    )
    catalog = dict(catalog_basis or accepted_catalog or joined_catalog)
    if accepted_catalog and catalog != accepted_catalog:
        raise PublicationContractError("catalog basis differs from accepted execution")
    policy = dict(
        policy_basis
        or (
            _thaw(execution_durability_join.policy_basis)
            if execution_durability_join is not None
            else {}
        )
    )
    if execution_durability_join is not None:
        expected_join_policy = _thaw(execution_durability_join.policy_basis)
        for field in ("policy_refs", "action_request", "invocation_facts"):
            if field in policy and policy[field] != expected_join_policy[field]:
                raise PublicationContractError("policy basis differs from typed execution/durability join")
            policy[field] = expected_join_policy[field]
    if accepted_command is not None:
        expected_refs = _policy_refs(accepted_command)
        supplied_refs = policy.get("policy_refs", expected_refs)
        if isinstance(supplied_refs, Sequence) and not isinstance(supplied_refs, (str, bytes)):
            if tuple(sorted(supplied_refs)) != tuple(sorted(expected_refs)):
                raise PublicationContractError("policy basis differs from accepted execution")
            policy["policy_refs"] = tuple(sorted(supplied_refs))
    deleted = tuple(sorted(path for path, value in operations.items() if value is None))
    return FrozenCampaignPublicationAttempt(
        repository_id=repository_id,
        target_ref=target_ref,
        campaign_id=campaign_id,
        acting_principal=acting_principal,
        pinned_head_sha=pinned_head_sha,
        base_tree_sha=base_tree_sha,
        campaign_identity=identity,
        path_operations=operations,
        deleted_paths=deleted,
        owner_generations=owner_generations,
        accepted_identity=accepted_identity,
        fixed_rng_values=fixed_rng_values,
        catalog_basis=catalog,
        policy_basis=policy,
        procedure_before=procedure_before,
        procedure_after=procedure_after,
        root_delta=root_delta,
        root_membership_before=root_membership_before,
        currentness_evidence=currentness_evidence,
        publication_reason=publication_reason,
        execution_durability_join=execution_durability_join,
        routed_operation=routed_operation,
    )


@dataclass(frozen=True, slots=True)
class ConnectorOperation:
    kind: str
    payload: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ConnectorGitPlan:
    parent_sha: str
    base_tree_sha: str
    commit_parent_sha: str
    path_operations: Mapping[str, object | None]
    operations: tuple[ConnectorOperation, ...]
    force: bool
    confirmation_reads: int
    requires_currentness_probe: bool


def build_connector_git_plan(attempt: FrozenCampaignPublicationAttempt) -> ConnectorGitPlan:
    """Build exactly one base-tree/tree/commit/non-force-ref operation envelope."""

    if not isinstance(attempt, FrozenCampaignPublicationAttempt):
        raise PublicationContractError("immutable campaign publication attempt is required")
    if not attempt.path_operations:
        raise PublicationContractError("empty normalized campaign delta requires no publication")
    for path in attempt.path_operations:
        if path in _STORAGE_PATH_MARKERS or path.startswith("DND_STORAGE/"):
            raise PublicationContractError("storage metadata cannot join campaign publication")
    operations = (
        ConnectorOperation("create_tree", {"base_tree_sha": attempt.base_tree_sha}),
        ConnectorOperation(
            "read_ref", {"ref": attempt.target_ref, "expected_head": attempt.pinned_head_sha}
        ),
        ConnectorOperation("create_commit", {"parent": attempt.pinned_head_sha}),
        ConnectorOperation("update_ref", {"force": False, "ref": attempt.target_ref}),
    )
    return ConnectorGitPlan(
        parent_sha=attempt.pinned_head_sha,
        base_tree_sha=attempt.base_tree_sha,
        commit_parent_sha=attempt.pinned_head_sha,
        path_operations=attempt.path_operations,
        operations=operations,
        force=False,
        confirmation_reads=0,
        requires_currentness_probe=True,
    )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class PublicationOutcome:
    status: PublicationStatus
    intended_commit_sha: str | None
    observed_head_sha: str | None
    cause: str
    dispatched: bool
    retry_with_force: bool = False

    @property
    def acknowledged(self) -> bool:
        return self.status is PublicationStatus.ACCEPTED

    @property
    def kind(self) -> str:
        return self.status.name.lower()

    @property
    def requires_repin(self) -> bool:
        return self.status is PublicationStatus.CONFLICT

    @property
    def can_reexecute(self) -> bool:
        return False

    def acknowledge(self) -> bool:
        if self.status is not PublicationStatus.ACCEPTED:
            raise PublicationContractError(
                "indeterminate/rejected publication cannot be acknowledged as saved"
            )
        return True


class PublicationAcceptanceKind(StrEnum):
    """W02-owned proof route that supports one accepted publication outcome."""

    CONFIRMED_REF = "CONFIRMED_REF"
    RECONCILED_CURRENT_CLOSURE = "RECONCILED_CURRENT_CLOSURE"
    RECONCILED_ANCESTOR_CURRENT_CLOSURE = "RECONCILED_ANCESTOR_CURRENT_CLOSURE"


@dataclass(frozen=True, slots=True)
class PublicationAcceptanceEvidence:
    """Ephemeral W02 proof bound to one frozen attempt and exact outcome instance."""

    kind: PublicationAcceptanceKind
    attempt: FrozenCampaignPublicationAttempt | FrozenCampaignPublicationRecoveryBasis
    intended_commit_sha: str
    observed_head_sha: str
    current_closure: PublicationCurrentClosureEvidence | None
    ancestry: CommitAncestryEvidence | None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, PublicationAcceptanceKind):
            raise PublicationContractError(
                "publication acceptance proof kind is invalid"
            )
        if not isinstance(
            self.attempt,
            (FrozenCampaignPublicationAttempt, FrozenCampaignPublicationRecoveryBasis),
        ):
            raise PublicationContractError(
                "publication acceptance basis is not W02-typed"
            )
        _revision(self.intended_commit_sha, "acceptance intended commit")
        _revision(self.observed_head_sha, "acceptance observed head")
        if self.current_closure is not None and not isinstance(
            self.current_closure, PublicationCurrentClosureEvidence
        ):
            raise PublicationContractError(
                "publication current closure proof is not typed"
            )
        if self.ancestry is not None and not isinstance(
            self.ancestry, CommitAncestryEvidence
        ):
            raise PublicationContractError("publication ancestry proof is not typed")


_OWNER_ISSUED_PUBLICATION_ACCEPTANCES: dict[
    int,
    tuple[weakref.ReferenceType[PublicationOutcome], PublicationAcceptanceEvidence],
] = {}


def _validate_acceptance_proof(
    outcome: PublicationOutcome, evidence: PublicationAcceptanceEvidence
) -> None:
    """Validate cause/proof correspondence against one immutable W02 attempt."""

    if outcome.status is not PublicationStatus.ACCEPTED:
        raise PublicationContractError("publication outcome is not accepted")
    attempt = evidence.attempt
    intended = _revision(outcome.intended_commit_sha, "publication intended commit")
    observed = _revision(outcome.observed_head_sha, "publication observed head")
    if (
        evidence.intended_commit_sha != intended
        or evidence.observed_head_sha != observed
    ):
        raise PublicationContractError("publication outcome SHA differs from its proof")

    expected_digests = attempt.publication_operation_digests()
    if (
        isinstance(attempt, FrozenCampaignPublicationRecoveryBasis)
        and attempt.intended_commit_sha != intended
    ):
        raise PublicationContractError(
            "recovery outcome differs from its nominated intended commit"
        )
    closure = evidence.current_closure
    ancestry = evidence.ancestry
    if evidence.kind is PublicationAcceptanceKind.CONFIRMED_REF:
        if (
            not isinstance(attempt, FrozenCampaignPublicationAttempt)
            or outcome.cause != "CONFIRMED_ACCEPTED"
            or outcome.dispatched is not True
            or intended != observed
            or closure is not None
            or ancestry is not None
        ):
            raise PublicationContractError(
                "confirmed-ref publication proof does not match result"
            )
        return

    if (
        outcome.dispatched is not False
        or closure is None
        or closure.base_revision != attempt.pinned_head_sha
        or closure.head_sha != observed
    ):
        raise PublicationContractError(
            "publication current-closure proof does not bind attempt"
        )
    closure_digests = dict(closure.operation_digests)
    if any(
        closure_digests.get(path) != digest for path, digest in expected_digests.items()
    ):
        raise PublicationContractError(
            "publication current closure omits or changes an attempted operation"
        )

    if evidence.kind is PublicationAcceptanceKind.RECONCILED_CURRENT_CLOSURE:
        if (
            outcome.cause != "RECONCILED_CURRENT_CLOSURE"
            or intended != observed
            or ancestry is not None
            or set(closure_digests) != set(expected_digests)
        ):
            raise PublicationContractError(
                "current-closure publication proof does not match result"
            )
        return

    if evidence.kind is PublicationAcceptanceKind.RECONCILED_ANCESTOR_CURRENT_CLOSURE:
        if (
            outcome.cause != "RECONCILED_ANCESTOR_CURRENT_CLOSURE"
            or intended == observed
            or not isinstance(ancestry, CommitAncestryEvidence)
            or ancestry.ancestor_sha != intended
            or ancestry.descendant_sha != observed
        ):
            raise PublicationContractError(
                "ancestor publication proof does not bind exact commits"
            )
        return

    raise PublicationContractError("unsupported publication acceptance proof kind")


def _issue_owner_issued_accepted_publication(
    outcome: PublicationOutcome,
    attempt: FrozenCampaignPublicationAttempt | FrozenCampaignPublicationRecoveryBasis,
    *,
    intended_commit_sha: str,
    current_closure: PublicationCurrentClosureEvidence | None = None,
    ancestry: CommitAncestryEvidence | None = None,
) -> PublicationAcceptanceEvidence:
    """Privately bind trusted CampaignPublicationService proof to one result object."""

    if not isinstance(outcome, PublicationOutcome):
        raise PublicationContractError("campaign publication result is not typed")
    if not isinstance(
        attempt,
        (FrozenCampaignPublicationAttempt, FrozenCampaignPublicationRecoveryBasis),
    ):
        raise PublicationContractError("campaign publication basis is not W02-typed")
    intended = _revision(intended_commit_sha, "service intended commit")
    if outcome.intended_commit_sha != intended:
        raise PublicationContractError("service result differs from its created commit")
    if (
        isinstance(attempt, FrozenCampaignPublicationRecoveryBasis)
        and attempt.intended_commit_sha != intended
    ):
        raise PublicationContractError(
            "recovery basis differs from its intended commit"
        )
    if outcome.cause == "CONFIRMED_ACCEPTED":
        kind = PublicationAcceptanceKind.CONFIRMED_REF
    elif outcome.cause == "RECONCILED_CURRENT_CLOSURE":
        kind = PublicationAcceptanceKind.RECONCILED_CURRENT_CLOSURE
    elif outcome.cause == "RECONCILED_ANCESTOR_CURRENT_CLOSURE":
        kind = PublicationAcceptanceKind.RECONCILED_ANCESTOR_CURRENT_CLOSURE
    else:
        raise PublicationContractError(
            "accepted publication cause has no W02 proof kind"
        )
    evidence = PublicationAcceptanceEvidence(
        kind=kind,
        attempt=attempt,
        intended_commit_sha=intended,
        observed_head_sha=_revision(outcome.observed_head_sha, "service observed head"),
        current_closure=current_closure,
        ancestry=ancestry,
    )
    _validate_acceptance_proof(outcome, evidence)

    outcome_id = id(outcome)

    def remove(reference: weakref.ReferenceType[PublicationOutcome]) -> None:
        registered = _OWNER_ISSUED_PUBLICATION_ACCEPTANCES.get(outcome_id)
        if registered is not None and registered[0] is reference:
            _OWNER_ISSUED_PUBLICATION_ACCEPTANCES.pop(outcome_id, None)

    _OWNER_ISSUED_PUBLICATION_ACCEPTANCES[outcome_id] = (
        weakref.ref(outcome, remove),
        evidence,
    )
    return evidence


def validate_owner_issued_accepted_publication(
    outcome: PublicationOutcome,
    *,
    campaign_id: str,
    expected_pinned_head_sha: str,
    required_operation_digests: Mapping[str, str] | None = None,
) -> PublicationAcceptanceEvidence:
    """Return W02 evidence only for the exact accepted result the owner issued."""

    if not isinstance(outcome, PublicationOutcome):
        raise PublicationContractError("publication result is not typed")
    registered = _OWNER_ISSUED_PUBLICATION_ACCEPTANCES.get(id(outcome))
    if registered is None or registered[0]() is not outcome:
        raise PublicationContractError(
            "publication result has no W02 owner-issued evidence"
        )
    evidence = registered[1]
    _validate_acceptance_proof(outcome, evidence)
    if evidence.attempt.campaign_id != _machine_id(
        campaign_id, "expected publication campaign"
    ):
        raise PublicationContractError(
            "publication evidence belongs to another campaign"
        )
    if evidence.attempt.pinned_head_sha != _revision(
        expected_pinned_head_sha, "expected pinned publication head"
    ):
        raise PublicationContractError(
            "publication evidence has another predecessor head"
        )
    if required_operation_digests is not None:
        if not isinstance(required_operation_digests, Mapping):
            raise PublicationContractError(
                "required publication operation subset must be a mapping"
            )
        attempted_digests = evidence.attempt.publication_operation_digests()
        for path, digest in required_operation_digests.items():
            normalized_path = _path(path)
            normalized_digest = _sha256(digest, "required operation digest")
            if attempted_digests.get(normalized_path) != normalized_digest:
                raise PublicationContractError(
                    "required operation digest is not an exact subset of the W02 attempt"
                )
    return evidence


def classify_ref_transition(
    response: Mapping[str, object], *, intended_commit_sha: str
) -> PublicationOutcome:
    """Classify the final authority-changing ref response without retrying it."""

    if not isinstance(response, Mapping):
        raise PublicationContractError("ref transition response must be typed evidence")
    intended = _revision(intended_commit_sha, "intended commit")
    dispatched = response.get("dispatched") is True
    raw_status = str(response.get("status", "")).lower()
    observed = response.get("head_sha")
    observed_sha = None if observed is None else _revision(observed, "observed head")
    if raw_status in {"accepted", "confirmed_accepted", "ok", "success"}:
        if observed_sha is not None and observed_sha != intended:
            return PublicationOutcome(PublicationStatus.INDETERMINATE, intended, observed_sha, "accepted_identity_mismatch", dispatched)
        return PublicationOutcome(PublicationStatus.ACCEPTED, intended, observed_sha or intended, "CONFIRMED_ACCEPTED", dispatched)
    if raw_status in {"indeterminate", "unknown", "timeout", "transport_unknown"}:
        return PublicationOutcome(PublicationStatus.INDETERMINATE, intended, observed_sha, "INDETERMINATE", dispatched)
    if raw_status in {"rejected", "failed", "error"}:
        reason = str(response.get("reason", "")).lower().replace("-", "_")
        if reason in {"non_fast_forward", "nonfastforward", "stale", "ref_moved", "head_moved"}:
            return PublicationOutcome(PublicationStatus.CONFLICT, intended, observed_sha, "STALE_OR_NON_FAST_FORWARD", dispatched)
        if reason in {"authorization", "unauthorized", "forbidden"}:
            cause = "AUTHORIZATION_REJECTED"
        elif reason in {"configuration", "rule", "invalid"}:
            cause = "CONFIGURATION_OR_RULE_REJECTED"
        elif reason in {"capability", "infrastructure", "network"}:
            cause = "CAPABILITY_OR_INFRASTRUCTURE_REJECTED"
        else:
            cause = "UNCLASSIFIED_CONFIRMED_REJECTION"
        return PublicationOutcome(PublicationStatus.REJECTED, intended, observed_sha, cause, dispatched)
    raise PublicationContractError("ref transition response has no typed outcome")


RefTransitionOutcome = PublicationOutcome
CampaignPublicationOutcome = PublicationOutcome
CampaignPublicationAttempt = FrozenCampaignPublicationAttempt
CampaignPublicationPlan = ConnectorGitPlan


def reconcile_indeterminate_publication(
    attempt: FrozenCampaignPublicationAttempt,
    read_current: Callable[[], Mapping[str, object]],
    *,
    intended_commit_sha: str | None = None,
) -> PublicationOutcome:
    """Read current authority once and reconcile; never dispatch a second write."""

    if not isinstance(attempt, FrozenCampaignPublicationAttempt):
        raise PublicationContractError("immutable campaign publication attempt is required")
    if intended_commit_sha is None:
        raise PublicationContractError("indeterminate reconciliation requires an intended commit")
    intended = _revision(intended_commit_sha, "intended commit")
    if not callable(read_current):
        raise PublicationContractError("indeterminate reconciliation requires authoritative read")
    evidence = read_current()
    if not isinstance(evidence, Mapping):
        raise PublicationContractError("currentness reconciliation evidence must be typed")
    if any(
        field in evidence
        for field in ("current_closure_compatible", "lineage_contains_intended", "head_is_intended")
    ):
        raise PublicationContractError("reconciliation cannot consume caller boolean authority")
    closure = evidence.get("closure")
    if not isinstance(closure, PublicationCurrentClosureEvidence):
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended,
            None,
            "BOUNDED_RECONCILIATION_INSUFFICIENT",
            dispatched=False,
        )
    observed = closure.head_sha
    if closure.base_revision != attempt.pinned_head_sha:
        return PublicationOutcome(
            PublicationStatus.CONFLICT,
            intended,
            observed,
            "CURRENT_CLOSURE_REQUIRES_REPIN",
            dispatched=False,
        )
    expected_digests = attempt.publication_operation_digests()
    overlapping = set(expected_digests).intersection(closure.operation_digests)
    if any(expected_digests[path] != closure.operation_digests[path] for path in overlapping):
        return PublicationOutcome(
            PublicationStatus.CONFLICT,
            intended,
            observed,
            "CURRENT_CLOSURE_REQUIRES_REPIN",
            dispatched=False,
        )
    if set(overlapping) != set(expected_digests):
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended,
            observed,
            "BOUNDED_RECONCILIATION_INSUFFICIENT",
            dispatched=False,
        )
    if observed == intended and set(closure.operation_digests) != set(expected_digests):
        return PublicationOutcome(
            PublicationStatus.CONFLICT,
            intended,
            observed,
            "CURRENT_CLOSURE_REQUIRES_REPIN",
            dispatched=False,
        )
    if observed != intended:
        ancestry = evidence.get("ancestry")
        if not isinstance(ancestry, CommitAncestryEvidence):
            return PublicationOutcome(
                PublicationStatus.INDETERMINATE,
                intended,
                observed,
                "BOUNDED_RECONCILIATION_INSUFFICIENT",
                dispatched=False,
            )
        if ancestry.ancestor_sha != intended or ancestry.descendant_sha != observed:
            return PublicationOutcome(
                PublicationStatus.CONFLICT,
                intended,
                observed,
                "ANCESTRY_EVIDENCE_INCOMPATIBLE",
                dispatched=False,
            )
    if observed == intended:
        return PublicationOutcome(
            PublicationStatus.ACCEPTED,
            intended,
            observed,
            "RECONCILED_CURRENT_CLOSURE",
            dispatched=False,
        )
    if not closure.operation_digests:
        return PublicationOutcome(
            PublicationStatus.INDETERMINATE,
            intended,
            observed,
            "BOUNDED_RECONCILIATION_INSUFFICIENT",
            dispatched=False,
        )
    return PublicationOutcome(
        PublicationStatus.ACCEPTED,
        intended,
        observed,
        "RECONCILED_ANCESTOR_CURRENT_CLOSURE",
        dispatched=False,
    )


def reconcile_non_fast_forward_publication(
    attempt: FrozenCampaignPublicationAttempt,
    read_current: Callable[[], Mapping[str, object]],
    *,
    intended_commit_sha: str,
) -> PublicationOutcome:
    """Reconcile a stale parent through bounded reads before any rebuild."""

    return reconcile_indeterminate_publication(
        attempt, read_current, intended_commit_sha=intended_commit_sha
    )
