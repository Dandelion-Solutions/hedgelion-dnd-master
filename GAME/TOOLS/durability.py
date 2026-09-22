"""Ephemeral durability promises and owner-local publication evidence.

This module composes already-admitted native durability owners.  It does not
persist a promise, create a campaign-wide frontier, or resolve policy,
catalog, lifecycle, or currentness on behalf of their owners.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import weakref
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from .native_storage import route_native_record

# framework_module_version: 1.0.3
FRAMEWORK_MODULE_VERSION: Final = "1.0.3"
_SHA256: Final = re.compile(r"^[a-f0-9]{64}$")
_ID: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_PROMISE_STATUSES: Final = frozenset(
    {"READY", "NO_WRITE_NEEDED", "REVALIDATION_REQUIRED"}
)
_NATIVE_STATUSES: Final = frozenset(
    {
        "CONFIRMED_ACCEPTED",
        "NO_WRITE_NEEDED",
        "CONFIRMED_REJECTED",
        "CONFLICT",
        "INDETERMINATE",
    }
)


class DurabilityContractError(ValueError):
    """Raised when a durability boundary lacks typed owner evidence."""


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise DurabilityContractError(f"{label} must be a nonempty string")
    return value


def _machine_id(value: object, label: str) -> str:
    result = _nonempty(value, label)
    if _ID.fullmatch(result) is None:
        raise DurabilityContractError(f"{label} must be a machine identifier")
    return result


def _sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise DurabilityContractError(f"{label} must be a SHA-256 digest")
    return value


def _json_copy(value: object, label: str) -> object:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DurabilityContractError(f"{label} must not contain a non-finite number")
        return value
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise DurabilityContractError(f"{label} keys must be strings")
        return {key: _json_copy(item, f"{label}.{key}") for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_copy(item, f"{label}[{index}]") for index, item in enumerate(value)]
    raise DurabilityContractError(f"{label} must contain JSON-compatible values")


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


def _sorted_unique(values: Sequence[object], label: str) -> tuple[str, ...]:
    result = tuple(_nonempty(value, f"{label} item") for value in values)
    if len(result) != len(set(result)):
        raise DurabilityContractError(f"{label} must be unique")
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class DurabilityEvaluation:
    """Operation-local evaluation of one requested durability boundary."""

    campaign_id: str
    scope: str
    dirty_roots: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    currentness_evidence: Mapping[str, object] | None
    status: str
    ephemeral: bool = True

    def __post_init__(self) -> None:
        _machine_id(self.campaign_id, "campaign_id")
        _nonempty(self.scope, "durability scope")
        if self.status not in _PROMISE_STATUSES:
            raise DurabilityContractError("unsupported durability evaluation status")
        if self.ephemeral is not True:
            raise DurabilityContractError("durability evaluation must remain ephemeral")
        if self.currentness_evidence is not None:
            evidence = _json_copy(self.currentness_evidence, "currentness_evidence")
            if not isinstance(evidence, dict) or not evidence:
                raise DurabilityContractError("currentness evidence must be a non-empty object")
            object.__setattr__(self, "currentness_evidence", _freeze(evidence))
        object.__setattr__(self, "dirty_roots", _sorted_unique(self.dirty_roots, "dirty_roots"))
        object.__setattr__(
            self,
            "required_dependencies",
            _sorted_unique(self.required_dependencies, "required_dependencies"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "campaign_id": self.campaign_id,
            "scope": self.scope,
            "status": self.status,
            "dirty_roots": list(self.dirty_roots),
            "required_dependencies": list(self.required_dependencies),
            "currentness_evidence": _thaw(self.currentness_evidence),
            "ephemeral": self.ephemeral,
        }


def evaluate_durability(
    *,
    campaign_id: str,
    scope: str,
    dirty_roots: Sequence[str],
    required_dependencies: Sequence[str] = (),
    currentness_evidence: Mapping[str, object] | None,
) -> DurabilityEvaluation:
    """Evaluate one bounded scope without scanning or inventing a frontier."""

    if currentness_evidence is None:
        status = "REVALIDATION_REQUIRED"
    elif dirty_roots:
        status = "READY"
    else:
        status = "NO_WRITE_NEEDED"
    return DurabilityEvaluation(
        campaign_id=campaign_id,
        scope=scope,
        dirty_roots=tuple(dirty_roots),
        required_dependencies=tuple(required_dependencies),
        currentness_evidence=currentness_evidence,
        status=status,
    )


@dataclass(frozen=True, slots=True)
class DurabilityPromise:
    """Frozen local SAVE/handoff promise; never a persistent journal record."""

    campaign_id: str
    scope: str
    required_roots: tuple[str, ...]
    required_dependencies: tuple[str, ...]
    owner_generations: Mapping[str, int]
    currentness_evidence: Mapping[str, object]
    ephemeral: bool = True

    def __post_init__(self) -> None:
        _machine_id(self.campaign_id, "campaign_id")
        _nonempty(self.scope, "promise scope")
        if self.ephemeral is not True:
            raise DurabilityContractError("durability promise must remain ephemeral")
        object.__setattr__(self, "required_roots", _sorted_unique(self.required_roots, "required_roots"))
        object.__setattr__(
            self,
            "required_dependencies",
            _sorted_unique(self.required_dependencies, "required_dependencies"),
        )
        generations: dict[str, int] = {}
        for key, value in self.owner_generations.items():
            _nonempty(key, "owner generation key")
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise DurabilityContractError("owner generation must be a non-negative integer")
            generations[key] = value
        object.__setattr__(self, "owner_generations", MappingProxyType(generations))
        evidence = _json_copy(self.currentness_evidence, "currentness_evidence")
        if not isinstance(evidence, dict) or not evidence:
            raise DurabilityContractError("promise currentness evidence is required")
        object.__setattr__(self, "currentness_evidence", _freeze(evidence))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "campaign_id": self.campaign_id,
            "scope": self.scope,
            "required_roots": list(self.required_roots),
            "required_dependencies": list(self.required_dependencies),
            "owner_generations": _thaw(self.owner_generations),
            "currentness_evidence": _thaw(self.currentness_evidence),
            "ephemeral": self.ephemeral,
        }


def freeze_save_promise(
    evaluation: DurabilityEvaluation,
    *,
    owner_generations: Mapping[str, int],
) -> DurabilityPromise:
    """Freeze one evaluated scope and its exact native generations."""

    if not isinstance(evaluation, DurabilityEvaluation):
        raise DurabilityContractError("typed durability evaluation is required")
    if evaluation.status == "REVALIDATION_REQUIRED" or evaluation.currentness_evidence is None:
        raise DurabilityContractError("save promise requires operation-current evidence")
    return DurabilityPromise(
        campaign_id=evaluation.campaign_id,
        scope=evaluation.scope,
        required_roots=evaluation.dirty_roots,
        required_dependencies=evaluation.required_dependencies,
        owner_generations=owner_generations,
        currentness_evidence=evaluation.currentness_evidence,
    )


@dataclass(frozen=True, slots=True)
class NativeDurabilityResult:
    """Result from one already-admitted native durability domain."""

    domain: str
    status: str

    def __post_init__(self) -> None:
        _nonempty(self.domain, "native durability domain")
        if self.status not in _NATIVE_STATUSES:
            raise DurabilityContractError("unsupported native durability status")


@dataclass(frozen=True, slots=True)
class DurabilityPromiseResult:
    """Overall promise result preserving native partial/ambiguous outcomes."""

    promise: DurabilityPromise
    status: str
    acknowledged: bool
    native_results: tuple[NativeDurabilityResult, ...]
    currentness_evidence: Mapping[str, object]

    def __post_init__(self) -> None:
        if self.status not in {"CONFIRMED_ACCEPTED", "CONFIRMED_REJECTED", "CONFLICT", "INDETERMINATE"}:
            raise DurabilityContractError("unsupported overall durability result")
        if self.acknowledged is not (self.status == "CONFIRMED_ACCEPTED"):
            raise DurabilityContractError("durability acknowledgement does not match result")
        evidence = _json_copy(self.currentness_evidence, "currentness_evidence")
        if not isinstance(evidence, dict) or not evidence:
            raise DurabilityContractError("completion requires currentness evidence")
        object.__setattr__(self, "currentness_evidence", _freeze(evidence))

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "campaign_id": self.promise.campaign_id,
            "scope": self.promise.scope,
            "status": self.status,
            "acknowledged": self.acknowledged,
            "required_roots": list(self.promise.required_roots),
            "required_dependencies": list(self.promise.required_dependencies),
            "native_results": [
                {"domain": result.domain, "status": result.status}
                for result in self.native_results
            ],
            "currentness_evidence": _thaw(self.currentness_evidence),
            "ephemeral": self.promise.ephemeral,
        }


def complete_save_promise(
    promise: DurabilityPromise,
    native_results: Sequence[NativeDurabilityResult],
    *,
    currentness_evidence: Mapping[str, object],
) -> DurabilityPromiseResult:
    """Compose native results; only complete current closure can acknowledge SAVE."""

    if not isinstance(promise, DurabilityPromise):
        raise DurabilityContractError("typed durability promise is required")
    evidence = _json_copy(currentness_evidence, "currentness_evidence")
    if not isinstance(evidence, dict) or not evidence:
        raise DurabilityContractError("completion requires currentness evidence")
    results = tuple(native_results)
    if any(not isinstance(result, NativeDurabilityResult) for result in results):
        raise DurabilityContractError("native durability results must be typed")
    statuses = {result.status for result in results}
    if "INDETERMINATE" in statuses:
        status = "INDETERMINATE"
    elif "CONFLICT" in statuses:
        status = "CONFLICT"
    elif statuses.intersection({"CONFIRMED_REJECTED"}):
        status = "CONFIRMED_REJECTED"
    elif statuses and statuses.issubset({"CONFIRMED_ACCEPTED", "NO_WRITE_NEEDED"}):
        status = "CONFIRMED_ACCEPTED"
    else:
        status = "CONFIRMED_REJECTED"
    return DurabilityPromiseResult(promise, status, status == "CONFIRMED_ACCEPTED", results, evidence)


@dataclass(frozen=True, slots=True)
class RoutedSerializedOperation:
    """Owner-routed serialized bytes admitted to one native record route."""

    owner_kind: str
    owner_id: str
    relative_path: str
    payload: Mapping[str, object]

    def __post_init__(self) -> None:
        _nonempty(self.owner_kind, "operation owner kind")
        _machine_id(self.owner_id, "operation owner id")
        expected_path = route_native_record(self.owner_kind, (self.owner_id,)).relative_path
        if self.relative_path != expected_path:
            raise DurabilityContractError("serialized operation route differs from native owner")
        copied = _json_copy(self.payload, "serialized operation payload")
        if not isinstance(copied, dict):
            raise DurabilityContractError("serialized operation payload must be an object")
        declared_kind = copied.get("kind")
        if declared_kind is not None and declared_kind != self.owner_kind:
            raise DurabilityContractError("serialized operation owner kind differs from payload")
        identity_field = {
            "runtime.command": "command_id",
            "runtime.interaction": "input_message_id",
            "runtime.intent_plan": "intent_plan_id",
            "runtime.collaboration_obligation": "obligation_id",
        }.get(self.owner_kind, "id")
        if copied.get(identity_field, copied.get("id")) != self.owner_id:
            raise DurabilityContractError("serialized operation owner identity differs from payload")
        object.__setattr__(self, "payload", _freeze(copied))

    def to_dict(self) -> dict[str, object]:
        return {
            "owner_kind": self.owner_kind,
            "owner_id": self.owner_id,
            "relative_path": self.relative_path,
            "payload": _thaw(self.payload),
        }


def route_serialized_operation(
    owner_kind: str, owner_id: str, payload: Mapping[str, object]
) -> RoutedSerializedOperation:
    """Derive the native route before a serialized owner operation is published."""

    route = route_native_record(owner_kind, (owner_id,))
    return RoutedSerializedOperation(owner_kind, owner_id, route.relative_path, payload)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class ExecutionDurabilityJoin:
    """Durability evidence joined to one accepted execution identity."""

    campaign_id: str
    command_id: str
    input_fingerprint: str
    resolution_id: str
    segment_id: str
    event_id: str
    fixed_rng_values: tuple[int, ...]
    catalog_basis: Mapping[str, object]
    policy_basis_refs: tuple[str, ...]
    accepted_command: Mapping[str, object]
    execution: Mapping[str, object]
    routed_operation: RoutedSerializedOperation
    policy_basis: Mapping[str, object]

    def __init__(self, **_values: object) -> None:
        raise DurabilityContractError("execution/durability joins must be owner-issued")

    def __post_init__(self) -> None:
        _machine_id(self.campaign_id, "campaign_id")
        _machine_id(self.command_id, "command_id")
        _sha256(self.input_fingerprint, "input_fingerprint")
        _machine_id(self.resolution_id, "resolution_id")
        _nonempty(self.segment_id, "segment_id")
        _nonempty(self.event_id, "event_id")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in self.fixed_rng_values):
            raise DurabilityContractError("fixed RNG values must remain typed integers")
        basis = _json_copy(self.catalog_basis, "catalog_basis")
        if not isinstance(basis, dict):
            raise DurabilityContractError("catalog basis must be an object")
        object.__setattr__(self, "catalog_basis", _freeze(basis))
        object.__setattr__(self, "policy_basis_refs", _sorted_unique(self.policy_basis_refs, "policy_basis_refs"))
        accepted = _json_copy(self.accepted_command, "accepted command")
        execution = _json_copy(self.execution, "execution evidence")
        if not isinstance(accepted, dict) or not isinstance(execution, dict):
            raise DurabilityContractError("execution/durability join requires serialized owner evidence")
        if not isinstance(self.routed_operation, RoutedSerializedOperation):
            raise DurabilityContractError("execution/durability join requires an owner-routed operation")
        if self.routed_operation.owner_kind != "runtime.command":
            raise DurabilityContractError("execution/durability operation must route a RuntimeCommand")
        if self.routed_operation.owner_id != self.command_id:
            raise DurabilityContractError("execution/durability route identity differs from command identity")
        if _thaw(self.routed_operation.payload) != accepted:
            raise DurabilityContractError("execution/durability route payload differs from accepted command")
        basis = _json_copy(self.policy_basis, "policy basis")
        if not isinstance(basis, dict):
            raise DurabilityContractError("execution/durability policy basis must be an object")
        if tuple(basis.get("policy_refs", ())) != self.policy_basis_refs:
            raise DurabilityContractError("execution/durability policy refs differ from accepted basis")
        object.__setattr__(self, "accepted_command", _freeze(accepted))
        object.__setattr__(self, "execution", _freeze(execution))
        object.__setattr__(self, "policy_basis", _freeze(basis))

    def to_dict(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "command_id": self.command_id,
            "input_fingerprint": self.input_fingerprint,
            "resolution_id": self.resolution_id,
            "segment_id": self.segment_id,
            "event_id": self.event_id,
            "fixed_rng_values": list(self.fixed_rng_values),
            "catalog_basis": _thaw(self.catalog_basis),
            "policy_basis_refs": list(self.policy_basis_refs),
            "accepted_command": _thaw(self.accepted_command),
            "execution": _thaw(self.execution),
            "routed_operation": self.routed_operation.to_dict(),
            "policy_basis": _thaw(self.policy_basis),
        }


def _policy_refs(command: Mapping[str, object]) -> tuple[str, ...]:
    refs: set[str] = set()
    action_request = command.get("action_request")
    if isinstance(action_request, Mapping):
        bindings = action_request.get("parameter_bindings")
        if isinstance(bindings, Mapping):
            values = bindings.values()
            for binding in values:
                if isinstance(binding, Mapping):
                    raw_refs = binding.get("policy_basis_refs", ())
                    if isinstance(raw_refs, Sequence) and not isinstance(raw_refs, (str, bytes)):
                        refs.update(_nonempty(value, "policy basis reference") for value in raw_refs)
    facts = command.get("invocation_facts", ())
    if isinstance(facts, Sequence) and not isinstance(facts, (str, bytes)):
        for fact in facts:
            if isinstance(fact, Mapping):
                raw_refs = fact.get("policy_basis_refs", ())
                if isinstance(raw_refs, Sequence) and not isinstance(raw_refs, (str, bytes)):
                    refs.update(_nonempty(value, "policy basis reference") for value in raw_refs)
    return tuple(sorted(refs))


_ISSUED_EXECUTION_JOINS: weakref.WeakValueDictionary[int, ExecutionDurabilityJoin] = weakref.WeakValueDictionary()


def join_execution_durability(
    accepted_command: Mapping[str, object],
    execution: Mapping[str, object],
    promise: DurabilityPromise,
    *,
    routed_operation: RoutedSerializedOperation,
) -> ExecutionDurabilityJoin:
    """Join execution output without rerunning mechanics or resolving policy."""

    if not isinstance(promise, DurabilityPromise):
        raise DurabilityContractError("typed durability promise is required")
    if not isinstance(routed_operation, RoutedSerializedOperation):
        raise DurabilityContractError("owner-routed serialized operation is required")
    if not isinstance(accepted_command, Mapping) or not isinstance(execution, Mapping):
        raise DurabilityContractError("accepted command and execution must be serialized objects")
    command_id = _machine_id(accepted_command.get("command_id"), "accepted command_id")
    fingerprint = _sha256(accepted_command.get("input_fingerprint"), "accepted input_fingerprint")
    if execution.get("accepted_command_id") != command_id:
        raise DurabilityContractError("execution and accepted identity differ")
    if execution.get("accepted_input_fingerprint") != fingerprint:
        raise DurabilityContractError("execution and accepted input fingerprint differ")
    resolution_id = _machine_id(execution.get("resolution_id"), "execution resolution_id")
    segment = execution.get("segment")
    event = execution.get("event")
    if not isinstance(segment, Mapping) or not isinstance(event, Mapping):
        raise DurabilityContractError("execution segment and event evidence are required")
    segment_id = _nonempty(segment.get("segment_id"), "execution segment_id")
    event_id = _nonempty(execution.get("event_id"), "execution event_id")
    roll = execution.get("roll_result")
    fixed_values: tuple[int, ...] = ()
    if isinstance(roll, Mapping):
        raw_values = roll.get("raw_values", ())
        if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)):
            raise DurabilityContractError("fixed RNG evidence must contain raw_values")
        fixed_values = tuple(
            value
            for value in raw_values
            if not isinstance(value, bool) and isinstance(value, int)
        )
        if len(fixed_values) != len(raw_values):
            raise DurabilityContractError("fixed RNG evidence contains a non-integer value")
    catalog = accepted_command.get("catalog_context")
    if not isinstance(catalog, Mapping):
        raise DurabilityContractError("accepted catalog basis is required")
    catalog_basis = dict(catalog)
    if catalog_basis.get("catalog_generation") != 2:
        raise DurabilityContractError("accepted catalog basis is not the pinned generation")
    policy_refs = _policy_refs(accepted_command)
    accepted_copy = _json_copy(accepted_command, "accepted command")
    execution_copy = _json_copy(execution, "execution evidence")
    if not isinstance(accepted_copy, dict) or not isinstance(execution_copy, dict):
        raise DurabilityContractError("accepted command and execution must be serialized objects")
    basis = {
        "policy_refs": list(policy_refs),
        "action_request": _json_copy(accepted_command.get("action_request", {}), "action request"),
        "invocation_facts": _json_copy(accepted_command.get("invocation_facts", []), "invocation facts"),
    }
    join = object.__new__(ExecutionDurabilityJoin)
    for field, value in {
        "campaign_id": promise.campaign_id,
        "command_id": command_id,
        "input_fingerprint": fingerprint,
        "resolution_id": resolution_id,
        "segment_id": segment_id,
        "event_id": event_id,
        "fixed_rng_values": fixed_values,
        "catalog_basis": catalog_basis,
        "policy_basis_refs": policy_refs,
        "accepted_command": accepted_copy,
        "execution": execution_copy,
        "routed_operation": routed_operation,
        "policy_basis": basis,
    }.items():
        object.__setattr__(join, field, value)
    ExecutionDurabilityJoin.__post_init__(join)
    _ISSUED_EXECUTION_JOINS[id(join)] = join
    return join


def is_execution_durability_join(value: object) -> bool:
    return (
        isinstance(value, ExecutionDurabilityJoin)
        and _ISSUED_EXECUTION_JOINS.get(id(value)) is value
    )


@dataclass(frozen=True, slots=True)
class DurabilityProjection:
    durable: Mapping[str, int]
    dirty: Mapping[str, int]


def project_durable_generations(
    *, current: Mapping[str, int], published: Mapping[str, int]
) -> DurabilityProjection:
    """Adopt exactly published generations and preserve newer local generations."""

    current_copy = dict(current)
    published_copy = dict(published)
    dirty = {
        key: generation
        for key, generation in current_copy.items()
        if key not in published_copy or generation != published_copy[key]
    }
    return DurabilityProjection(durable=published_copy, dirty=dirty)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class DurabilityHandoffPromise:
    """Opaque owner-issued boundary for an unresolved interaction/intent plan."""

    campaign_id: str
    owner_kind: str
    owner_id: str
    scope: str
    owner_state_fingerprint: str
    ephemeral: bool = True

    def __init__(self, **_values: object) -> None:
        raise DurabilityContractError("handoff promises must be owner-issued")

    def validate(
        self,
        *,
        campaign_id: str,
        owner_kind: str,
        owner_id: str,
        native_owner: Mapping[str, object],
    ) -> bool:
        return (
            is_authorized_handoff_promise(self)
            and self.campaign_id == campaign_id
            and self.owner_kind == owner_kind
            and self.owner_id == owner_id
            and _native_owner_fingerprint(native_owner) == self.owner_state_fingerprint
        )


_ISSUED_HANDOFF_PROMISES: weakref.WeakSet[DurabilityHandoffPromise] = weakref.WeakSet()


def _native_owner_fingerprint(owner: Mapping[str, object]) -> str:
    encoded = json.dumps(
        _json_copy(owner, "native owner"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _handoff_owner_id(owner_kind: str, owner: Mapping[str, object]) -> str:
    if owner_kind == "runtime.interaction":
        return _machine_id(owner.get("input_message_id"), "interaction input_message_id")
    if owner_kind == "runtime.intent_plan":
        return _machine_id(owner.get("intent_plan_id", owner.get("id")), "intent plan id")
    raise DurabilityContractError("handoff promise owner kind is not unresolved input")


def issue_durability_handoff_promise(
    *,
    campaign_id: str,
    owner_kind: str,
    native_owner: Mapping[str, object],
    scope: str,
) -> DurabilityHandoffPromise:
    """Issue the only accepted promise boundary for unresolved input roots."""

    campaign = _machine_id(campaign_id, "campaign_id")
    if not isinstance(native_owner, Mapping):
        raise DurabilityContractError("native unresolved owner must be an object")
    if native_owner.get("kind") != owner_kind:
        raise DurabilityContractError("handoff owner kind differs from native owner")
    try:
        from .recovery_roots import validate_unresolved_input_owner

        owner_id = validate_unresolved_input_owner(campaign, owner_kind, native_owner)
    except (ImportError, ValueError) as exc:
        raise DurabilityContractError(f"native owner is not an admitted unresolved owner: {exc}") from exc
    _nonempty(scope, "handoff promise scope")
    promise = object.__new__(DurabilityHandoffPromise)
    for field, value in {
        "campaign_id": campaign,
        "owner_kind": owner_kind,
        "owner_id": owner_id,
        "scope": scope,
        "owner_state_fingerprint": _native_owner_fingerprint(native_owner),
        "ephemeral": True,
    }.items():
        object.__setattr__(promise, field, value)
    _ISSUED_HANDOFF_PROMISES.add(promise)
    return promise


def is_authorized_handoff_promise(value: object) -> bool:
    return isinstance(value, DurabilityHandoffPromise) and value in _ISSUED_HANDOFF_PROMISES
