"""Owner-local deterministic execution for one accepted runtime command.

This module deliberately keeps execution evidence in memory.  Durability,
publication, recovery-source selection and campaign storage remain owned by
their later Wave-02 tasks.  The in-memory store supplies the atomic boundary
needed to make duplicate delivery safe while this owner builds one committed
segment.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from typing import Final, Protocol


# framework_module_version: 1.0.5
FRAMEWORK_MODULE_VERSION: Final = "1.0.5"
_DIGEST_GENERATION: Final = 1
_ID_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_EVENT_KIND_PATTERN: Final = re.compile(r"^event\.[a-z][a-z0-9_.]*$")
_SHA256_PATTERN: Final = re.compile(r"^[a-f0-9]{64}$")
_EXECUTION_STATES: Final = frozenset(
    {
        "PENDING",
        "RUNNING",
        "AWAITING_CHOICE",
        "AWAITING_REACTION",
        "HYDRATION_REQUIRED",
        "PUBLISH_REQUIRED",
        "COMPLETED",
        "REJECTED",
        "ABORTED",
        "FAILED",
    }
)
_ROLL_FIELDS: Final = frozenset(
    {"roll_id", "request_id", "expression", "raw_values", "source_kind", "provenance_ref"}
)
_ROLL_SOURCES: Final = frozenset({"rng.system", "rng.player", "rng.external"})
_ACCEPTED_INPUT_FIELDS: Final = frozenset(
    {
        "command_kind",
        "catalog_context_fingerprint",
        "invocation_facts",
        "action_request",
        "interpreter_result",
        "interpreter_result_fingerprint_generation",
        "interpreter_result_fingerprint",
        "catalog_context",
        "candidate_binding",
    }
)
_RUNTIME_COMMAND_INPUT_DOMAIN: Final = b"HDM_RUNTIME_COMMAND_INPUT/2\n"
_FORBIDDEN_RESOLUTION_FIELDS: Final = frozenset(
    {
        "world_state",
        "world_state_snapshot",
        "procedure_resources",
        "resource_state_copy",
        "prospective_deltas",
        "mechanical_context",
        "temporal_agenda",
        "condition_index",
        "committed_receipt_refs",
        "receipt_ref",
    }
)
_FORBIDDEN_CONTINUATION_FIELDS: Final = frozenset(
    {
        "procedure_resources",
        "resource_state_copy",
        "mechanical_context",
        "temporal_agenda",
        "prospective_deltas",
        "condition_index",
        "committed_receipt_refs",
        "receipt_ref",
    }
)
_FORBIDDEN_PROCEDURE_FIELDS: Final = frozenset(
    {
        "world_state",
        "world_state_snapshot",
        "prospective_deltas",
        "mechanical_context",
        "temporal_agenda",
        "condition_index",
    }
)
_PROCEDURE_SCHEMA_VERSION: Final = 2
_PROCEDURE_LIFECYCLES: Final = frozenset({"ACTIVE", "TERMINAL"})


class ExecutionContractError(ValueError):
    """Raised when an execution input or owner-local state is malformed."""


class ExecutionConflict(ExecutionContractError):
    """Raised when an accepted command is delivered with conflicting inputs."""

    failure_code: str

    def __init__(
        self,
        message: str,
        *,
        failure_code: str = "failure.idempotency_conflict",
    ) -> None:
        super().__init__(message)
        self.failure_code = failure_code


class RngProvider(Protocol):
    """The narrow provider contract needed to capture one fixed roll value."""

    def draw(self, request: Mapping[str, object]) -> Mapping[str, object]:
        """Return one typed roll result for the supplied request."""


class FixedRng:
    """Small deterministic RNG fixture/provider whose values are consumed once."""

    __slots__ = ("_values", "_cursor", "draw_count")

    def __init__(self, values: Sequence[int]) -> None:
        if not values:
            raise ValueError("fixed RNG requires at least one value")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
            raise ValueError("fixed RNG values must be integers")
        self._values = tuple(values)
        self._cursor = 0
        self.draw_count = 0

    def draw(self, request: Mapping[str, object]) -> Mapping[str, object]:
        """Consume and return the next fixed value as a ``roll-result`` value."""
        if self._cursor >= len(self._values):
            raise ExecutionContractError("fixed RNG has no remaining value")
        value = self._values[self._cursor]
        self._cursor += 1
        self.draw_count += 1
        return {
            "roll_id": _require_id(request.get("roll_id"), "roll request roll_id"),
            "request_id": _require_id(request.get("request_id"), "roll request request_id"),
            "expression": _require_string(request.get("expression"), "roll request expression"),
            "raw_values": [value],
            "source_kind": _require_roll_source(request.get("source_kind")),
            "provenance_ref": _require_string(
                request.get("provenance_ref"), "roll request provenance_ref"
            ),
        }

    def _checkpoint(self) -> tuple[int, int]:
        return self._cursor, self.draw_count

    def _restore(self, checkpoint: tuple[int, int]) -> None:
        self._cursor, self.draw_count = checkpoint


@dataclass(frozen=True, slots=True)
class _StoredExecution:
    execution_owner_id: str
    segment_id: str
    command_id: str
    input_fingerprint: str
    execution_fingerprint: str
    result: dict[str, object]


class ExecutionStore:
    """Atomic owner-local accepted-execution store used for duplicate delivery."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._entries: dict[tuple[str, str], _StoredExecution] = {}
        self._command_fingerprints: dict[str, str] = {}

    def lookup(self, execution_owner_id: str, segment_id: str | None = None) -> dict[str, object] | None:
        """Return an isolated copy of a committed result, if present."""
        with self._lock:
            if segment_id is not None:
                entry = self._entries.get((execution_owner_id, segment_id))
            else:
                matches = [
                    entry
                    for entry in self._entries.values()
                    if entry.command_id == execution_owner_id
                ]
                if len(matches) > 1:
                    raise ExecutionContractError(
                        "command has multiple execution segments; owner and segment are required"
                    )
                entry = matches[0] if matches else None
            return None if entry is None else deepcopy(entry.result)

    def commit(
        self,
        execution_owner_id: str,
        segment_id: str,
        command_id: str,
        input_fingerprint: str,
        execution_fingerprint: str,
        result: Mapping[str, object],
    ) -> dict[str, object]:
        """Commit one result or return the exact prior result for a duplicate."""
        with self._lock:
            prior_fingerprint = self._command_fingerprints.get(command_id)
            if prior_fingerprint is not None and prior_fingerprint != input_fingerprint:
                raise ExecutionConflict("accepted command was replayed with conflicting input fingerprint")
            existing = self._entries.get((execution_owner_id, segment_id))
            if existing is not None:
                if (
                    existing.input_fingerprint != input_fingerprint
                    or existing.execution_fingerprint != execution_fingerprint
                ):
                    raise ExecutionConflict("accepted command was replayed with conflicting input")
                return deepcopy(existing.result)
            stored = deepcopy(dict(result))
            self._command_fingerprints[command_id] = input_fingerprint
            self._entries[(execution_owner_id, segment_id)] = _StoredExecution(
                execution_owner_id=execution_owner_id,
                segment_id=segment_id,
                command_id=command_id,
                input_fingerprint=input_fingerprint,
                execution_fingerprint=execution_fingerprint,
                result=stored,
            )
            return deepcopy(stored)


def execute_segment(
    accepted_command: Mapping[str, object],
    resolution: Mapping[str, object],
    *,
    target_segment_id: str | None = None,
    rng: RngProvider | None = None,
    roll_request: Mapping[str, object] | None = None,
    event_kind: str = "event.execution.committed",
    event_payload: Mapping[str, object] | None = None,
    procedure_state: Mapping[str, object] | None = None,
    continuation_state: Mapping[str, object] | None = None,
    expected_continuation_generation: int | None = None,
    store: ExecutionStore,
) -> dict[str, object]:
    """Execute one accepted input into one deterministic committed segment.

    All evidence is constructed before the owner-local store mutation.  A
    duplicate owner/segment delivery therefore returns the committed result without drawing
    RNG, allocating another segment/event identity, or mutating caller input.

    When ``target_segment_id`` is provided, this is an exact replay of an
    already committed segment; otherwise the resolution's next segment is
    advanced.
    """
    command_id, input_fingerprint, root_resolution_id = _accepted_identity(accepted_command)
    checked_resolution = _mapping_copy(resolution, "resolution")
    _reject_fields(checked_resolution, _FORBIDDEN_RESOLUTION_FIELDS, "resolution")
    resolution_id = _require_id(
        checked_resolution.get("resolution_id", root_resolution_id), "resolution resolution_id"
    )
    _validate_invocation_binding(accepted_command, checked_resolution, resolution_id, root_resolution_id)
    replay_target = _optional_id(target_segment_id, "target_segment_id")
    sequence = (
        _segment_sequence(checked_resolution)
        if replay_target is None
        else _target_segment_sequence(resolution_id, replay_target)
    )
    status = checked_resolution.get("status", "COMPLETED")
    if not isinstance(status, str):
        raise ExecutionContractError("resolution status must be a string")
    if status not in _EXECUTION_STATES:
        raise ExecutionContractError("resolution status is not a supported execution state")
    checked_event_kind = _event_kind(event_kind)
    payload = _mapping_copy({} if event_payload is None else event_payload, "event payload")
    exports = _scalar_exports(payload)
    procedure = _mapping_copy(procedure_state, "procedure state") if procedure_state is not None else None
    continuation = (
        _mapping_copy(continuation_state, "continuation state")
        if continuation_state is not None
        else None
    )
    if continuation is not None:
        _reject_fields(continuation, _FORBIDDEN_CONTINUATION_FIELDS, "continuation state")
    _validate_continuation_generation(continuation, expected_continuation_generation)
    procedure_id = _optional_id(checked_resolution.get("procedure_id"), "resolution procedure_id")
    _validate_procedure_binding(checked_resolution, procedure)
    _validate_continuation_binding(
        checked_resolution,
        continuation,
        command_id,
        resolution_id,
    )
    targeted_existing = (
        store.lookup(resolution_id, replay_target) if replay_target is not None else None
    )
    if replay_target is not None and targeted_existing is None:
        raise ExecutionConflict("target segment is not a committed execution")
    stored_roll = (
        _roll_result(_require_mapping(targeted_existing["roll_result"], "stored roll result"))
        if targeted_existing is not None and "roll_result" in targeted_existing
        else None
    )
    if roll_request is not None:
        checked_roll_request = _roll_request(resolution_id, roll_request)
    elif stored_roll is not None:
        checked_roll_request = _roll_request_from_result(stored_roll)
    elif rng is not None:
        checked_roll_request = _roll_request(resolution_id, None)
    else:
        checked_roll_request = None
    fixed_roll = stored_roll if replay_target is not None else _existing_roll_result(
        checked_resolution, checked_roll_request
    )
    if replay_target is not None and stored_roll is not None:
        supplied_roll = _existing_roll_result(
            checked_resolution, _roll_request_from_result(stored_roll)
        )
        if supplied_roll is not None and supplied_roll != stored_roll:
            raise ExecutionConflict("accepted command was replayed with conflicting fixed RNG")
    execution_fingerprint = _digest(
        {
            "generation": _DIGEST_GENERATION,
            "command_id": command_id,
            "input_fingerprint": input_fingerprint,
            "resolution": _execution_resolution_basis(checked_resolution),
            "event_kind": checked_event_kind,
            "event_payload": payload,
            "procedure_state": procedure,
            "continuation_state": _continuation_execution_basis(continuation),
            "expected_continuation_generation": expected_continuation_generation,
            "roll_request": checked_roll_request,
            "segment_id": f"{resolution_id}:segment:{sequence}",
        }
    )
    segment_id = f"{resolution_id}:segment:{sequence}"
    existing = targeted_existing if replay_target is not None else store.lookup(resolution_id, segment_id)
    if existing is not None:
        prior_roll = existing.get("roll_result")
        if fixed_roll is not None and prior_roll is not None and fixed_roll != prior_roll:
            raise ExecutionConflict("accepted command was replayed with conflicting fixed RNG")
        return store.commit(
            resolution_id,
            segment_id,
            command_id,
            input_fingerprint,
            execution_fingerprint,
            existing,
        )

    checkpoint = rng._checkpoint() if isinstance(rng, FixedRng) else None
    try:
        roll_result = fixed_roll
        if roll_result is None and rng is not None:
            if checked_roll_request is None:
                raise ExecutionContractError("RNG execution requires a typed roll request")
            roll_result = _roll_result(rng.draw(checked_roll_request))
        event_ordinal = 1
        event_id = f"{segment_id}:event:{event_ordinal}"
        event: dict[str, object] = {
            "segment_id": segment_id,
            "event_ordinal": event_ordinal,
            "event_kind": checked_event_kind,
            "root_command_id": command_id,
            "causal_ref": resolution_id,
            "payload": deepcopy(payload),
        }
        if procedure_id is not None:
            event["procedure_id"] = procedure_id
        segment: dict[str, object] = {
            "segment_id": segment_id,
            "segment_sequence": sequence,
            "commit_state": "committed",
            "resulting_execution_state": status,
            "event_ids": [event_id],
            "pending_child_invocations": [],
            "receipt_exports": exports,
            "affected_revision_refs": [],
        }
        receipt: dict[str, object] = {
            "execution_owner_id": resolution_id,
            "segment_refs": [segment_id],
            "status": status,
            "event_ids": [event_id],
            "exports": exports,
            "pending_child_refs": [],
        }
        result: dict[str, object] = {
            "accepted_command_id": command_id,
            "accepted_input_fingerprint": input_fingerprint,
            "execution_owner_id": resolution_id,
            "resolution_id": resolution_id,
            "status": status,
            "segment": segment,
            "event": event,
            "event_id": event_id,
            "receipt": receipt,
        }
        if roll_result is not None:
            result["roll_result"] = roll_result
        if procedure is not None:
            result["procedure_state"] = procedure
        if continuation is not None:
            result["continuation_state"] = _continuation_with_segment(
                continuation, segment, roll_result
            )
        result["resolution"] = _resolution_with_segment(
            checked_resolution, segment, roll_result
        )
        return store.commit(
            resolution_id,
            segment_id,
            command_id,
            input_fingerprint,
            execution_fingerprint,
            result,
        )
    except Exception:
        if isinstance(rng, FixedRng) and checkpoint is not None:
            rng._restore(checkpoint)
        raise


def resolve_mechanic(
    accepted_command: Mapping[str, object],
    resolution: Mapping[str, object],
    *,
    rng: RngProvider | None = None,
    roll_request: Mapping[str, object] | None = None,
    event_kind: str = "event.execution.committed",
    event_payload: Mapping[str, object] | None = None,
    procedure_state: Mapping[str, object] | None = None,
    continuation_state: Mapping[str, object] | None = None,
    expected_continuation_generation: int | None = None,
    store: ExecutionStore,
) -> dict[str, object]:
    """Resolve one accepted mechanic through the deterministic segment owner."""
    return execute_segment(
        accepted_command,
        resolution,
        rng=rng,
        roll_request=roll_request,
        event_kind=event_kind,
        event_payload=event_payload,
        procedure_state=procedure_state,
        continuation_state=continuation_state,
        expected_continuation_generation=expected_continuation_generation,
        store=store,
    )


def resume_accepted_execution(
    accepted_command: Mapping[str, object],
    resolution: Mapping[str, object],
    *,
    target_segment_id: str | None = None,
    rng: RngProvider | None = None,
    roll_request: Mapping[str, object] | None = None,
    event_kind: str = "event.execution.committed",
    event_payload: Mapping[str, object] | None = None,
    procedure_state: Mapping[str, object] | None = None,
    continuation_state: Mapping[str, object] | None = None,
    expected_continuation_generation: int | None = None,
    store: ExecutionStore,
) -> dict[str, object]:
    """Resume or replay an accepted execution through its owner boundary.

    ``target_segment_id`` selects an existing committed segment for exact
    recovery.  Omitting it advances to the resolution's next segment.
    """
    return execute_segment(
        accepted_command,
        resolution,
        target_segment_id=target_segment_id,
        rng=rng,
        roll_request=roll_request,
        event_kind=event_kind,
        event_payload=event_payload,
        procedure_state=procedure_state,
        continuation_state=continuation_state,
        expected_continuation_generation=expected_continuation_generation,
        store=store,
    )


def close_resolution(
    execution: Mapping[str, object],
    *,
    status: str = "COMPLETED",
    store: ExecutionStore | None = None,
) -> dict[str, object]:
    """Close committed execution evidence without changing its identities."""
    if not isinstance(status, str) or status not in _EXECUTION_STATES:
        raise ExecutionContractError("resolution close status is not supported")
    if store is None:
        raise ExecutionContractError("closing requires stored committed execution evidence")
    result = _mapping_copy(execution, "execution result")
    segment = _mapping_copy(result.get("segment"), "execution segment")
    segment_id = _require_id(segment.get("segment_id"), "execution segment segment_id")
    execution_owner_id = _require_id(
        result.get("execution_owner_id", result.get("resolution_id")),
        "execution execution_owner_id",
    )
    stored = store.lookup(execution_owner_id, segment_id)
    if stored is None:
        raise ExecutionContractError("closing requires stored committed execution evidence")
    if _evidence_without_close_state(result) != _evidence_without_close_state(stored):
        raise ExecutionConflict("closing requires the stored committed evidence")

    closed = deepcopy(stored)
    closed["status"] = status
    closed_resolution = _mapping_copy(closed.get("resolution"), "stored execution resolution")
    closed_resolution["status"] = status
    closed["resolution"] = closed_resolution
    return closed


def _accepted_identity(value: Mapping[str, object]) -> tuple[str, str, str]:
    command = _require_mapping(value, "accepted command")
    command_id = _require_id(command.get("command_id"), "accepted command command_id")
    fingerprint = command.get("input_fingerprint")
    if not isinstance(fingerprint, str) or _SHA256_PATTERN.fullmatch(fingerprint) is None:
        raise ExecutionContractError("accepted command input_fingerprint must be a SHA-256 digest")
    if not _ACCEPTED_INPUT_FIELDS.issubset(command):
        raise ExecutionContractError("accepted command is missing input fingerprint basis")
    expected_fingerprint = _accepted_input_fingerprint(command)
    if fingerprint != expected_fingerprint:
        raise ExecutionConflict("accepted command input fingerprint differs from basis")
    if command.get("disposition") not in {"command.accepted", "command.settled"}:
        raise ExecutionContractError("accepted command has no executable disposition")
    action_request = _require_mapping(command.get("action_request"), "accepted command action_request")
    _require_id(action_request.get("activity_id"), "accepted command action_request activity_id")
    _require_id(action_request.get("actor_id"), "accepted command action_request actor_id")
    root_resolution_id = _require_id(
        command.get("root_resolution_id"), "accepted command root_resolution_id"
    )
    return command_id, fingerprint, root_resolution_id


def _validate_invocation_binding(
    accepted_command: Mapping[str, object],
    resolution: Mapping[str, object],
    resolution_id: str,
    root_resolution_id: str,
) -> None:
    command_id = _require_id(accepted_command.get("command_id"), "accepted command command_id")
    root_command_id = _require_id(resolution.get("root_command_id"), "resolution root_command_id")
    if root_command_id != command_id:
        raise ExecutionConflict("resolution root_command_id differs from accepted command")
    initiating_command_id = _optional_id(
        resolution.get("initiating_command_id"), "resolution initiating_command_id"
    )
    action_request = _require_mapping(accepted_command.get("action_request"), "accepted command action_request")
    if resolution_id != root_resolution_id:
        if resolution.get("causal_invocation_key") is None:
            raise ExecutionConflict("child resolution requires causal_invocation_key")
        _require_string(resolution["causal_invocation_key"], "resolution causal_invocation_key")
        if initiating_command_id is not None and initiating_command_id != command_id:
            raise ExecutionConflict("child resolution initiating_command_id differs from root command")
    elif initiating_command_id != command_id:
        raise ExecutionConflict("resolution initiating_command_id differs from accepted command")
    for field in ("activity_id", "actor_id"):
        resolved = _require_id(resolution.get(field), f"resolution {field}")
        accepted = _require_id(action_request.get(field), f"accepted command action_request {field}")
        if resolution_id == root_resolution_id and resolved != accepted:
            raise ExecutionConflict(f"resolution {field} differs from accepted input")


def _validate_procedure_binding(
    resolution: Mapping[str, object], procedure: Mapping[str, object] | None
) -> None:
    if procedure is None:
        return
    _reject_fields(procedure, _FORBIDDEN_PROCEDURE_FIELDS, "procedure state")
    resolution_procedure_id = _optional_id(
        resolution.get("procedure_id"), "resolution procedure_id"
    )
    procedure_procedure_id = _optional_id(procedure.get("procedure_id"), "procedure state procedure_id")
    if procedure_procedure_id is not None and procedure_procedure_id != resolution_procedure_id:
        raise ExecutionConflict("procedure state procedure_id differs from resolution procedure_id")
    if procedure.get("schema_version") != _PROCEDURE_SCHEMA_VERSION:
        raise ExecutionContractError("procedure schema_version must be 2")
    lifecycle = procedure.get("lifecycle")
    if lifecycle not in _PROCEDURE_LIFECYCLES:
        raise ExecutionContractError("procedure schema lifecycle must be ACTIVE or TERMINAL")
    lifecycle_state = procedure.get("lifecycle_state")
    if lifecycle == "TERMINAL" and lifecycle_state != "terminated":
        raise ExecutionContractError("terminal procedure schema requires terminated phase")
    if lifecycle == "ACTIVE" and lifecycle_state == "terminated":
        raise ExecutionContractError("active procedure schema cannot use terminated phase")


def _validate_continuation_binding(
    resolution: Mapping[str, object],
    continuation: Mapping[str, object] | None,
    command_id: str,
    resolution_id: str,
) -> None:
    if continuation is None:
        return
    required = (
        "root_command_id",
        "resolution_id",
        "activity_id",
        "actor_id",
        "execution_cursor",
        "safe_recompute_phase",
    )
    for field in required:
        if field not in continuation:
            raise ExecutionContractError(f"continuation state is missing {field}")
    if _require_id(continuation["root_command_id"], "continuation root_command_id") != command_id:
        raise ExecutionConflict("continuation root_command_id differs from accepted command")
    if _require_id(continuation["resolution_id"], "continuation resolution_id") != resolution_id:
        raise ExecutionConflict("continuation resolution_id differs from resolution")
    for field in ("activity_id", "actor_id"):
        continuation_value = _require_id(continuation[field], f"continuation {field}")
        resolution_value = _require_id(resolution.get(field), f"resolution {field}")
        if continuation_value != resolution_value:
            raise ExecutionConflict(f"continuation {field} differs from resolution")
    for field in ("execution_cursor", "safe_recompute_phase"):
        continuation_value = _require_string(continuation[field], f"continuation {field}")
        if field in resolution:
            resolution_value = _require_string(resolution[field], f"resolution {field}")
            if continuation_value != resolution_value:
                raise ExecutionConflict(f"continuation {field} differs from resolution")
    continuation_procedure_id = _optional_id(
        continuation.get("procedure_id"), "continuation procedure_id"
    )
    resolution_procedure_id = _optional_id(
        resolution.get("procedure_id"), "resolution procedure_id"
    )
    if continuation_procedure_id != resolution_procedure_id:
        raise ExecutionConflict("continuation procedure_id differs from resolution")


def _evidence_without_close_state(result: Mapping[str, object]) -> dict[str, object]:
    evidence = deepcopy(dict(result))
    evidence.pop("status", None)
    segment = evidence.get("segment")
    if isinstance(segment, Mapping):
        segment_copy = deepcopy(dict(segment))
        segment_copy.pop("resulting_execution_state", None)
        evidence["segment"] = segment_copy
    receipt = evidence.get("receipt")
    if isinstance(receipt, Mapping):
        receipt_copy = deepcopy(dict(receipt))
        receipt_copy.pop("status", None)
        evidence["receipt"] = receipt_copy
    resolution = evidence.get("resolution")
    if isinstance(resolution, Mapping):
        resolution_copy = deepcopy(dict(resolution))
        resolution_copy.pop("status", None)
        segments = resolution_copy.get("segments")
        if isinstance(segments, Sequence) and not isinstance(segments, (str, bytes)):
            normalized_segments: list[object] = []
            for item in segments:
                if isinstance(item, Mapping):
                    segment_copy = deepcopy(dict(item))
                    segment_copy.pop("resulting_execution_state", None)
                    normalized_segments.append(segment_copy)
                else:
                    normalized_segments.append(deepcopy(item))
            resolution_copy["segments"] = normalized_segments
        evidence["resolution"] = resolution_copy
    return evidence


def _reject_fields(value: Mapping[str, object], forbidden: frozenset[str], label: str) -> None:
    unexpected = sorted(set(value).intersection(forbidden))
    if unexpected:
        raise ExecutionContractError(f"{label} contains forbidden field {unexpected[0]}")


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ExecutionContractError(f"{label} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise ExecutionContractError(f"{label} keys must be strings")
    return value


def _mapping_copy(value: object, label: str) -> dict[str, object]:
    mapping = _require_mapping(value, label)
    return {key: _json_copy(item, f"{label}.{key}") for key, item in mapping.items()}


def _json_copy(value: object, label: str) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (value != value or value in {float("inf"), float("-inf")}):
            raise ExecutionContractError(f"{label} must not contain a non-finite number")
        return value
    if isinstance(value, Mapping):
        return _mapping_copy(value, label)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_copy(item, f"{label}[{index}]") for index, item in enumerate(value)]
    raise ExecutionContractError(f"{label} must contain JSON-compatible values")


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ExecutionContractError(f"{label} must be a nonempty string")
    return value


def _require_id(value: object, label: str) -> str:
    result = _require_string(value, label)
    if _ID_PATTERN.fullmatch(result) is None:
        raise ExecutionContractError(f"{label} must be a machine ID")
    return result


def _optional_id(value: object, label: str) -> str | None:
    return None if value is None else _require_id(value, label)


def _segment_sequence(resolution: Mapping[str, object]) -> int:
    segments = resolution.get("segments", [])
    if not isinstance(segments, Sequence) or isinstance(segments, (str, bytes)):
        raise ExecutionContractError("resolution segments must be an array")
    value = resolution.get("next_segment_sequence")
    if value is None:
        return len(segments) + 1
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ExecutionContractError("resolution next_segment_sequence must be positive")
    existing_sequences = [
        segment.get("segment_sequence")
        for segment in segments
        if isinstance(segment, Mapping) and isinstance(segment.get("segment_sequence"), int)
    ]
    if existing_sequences and value <= max(existing_sequences):
        raise ExecutionContractError("resolution next_segment_sequence reuses a committed segment")
    return value


def _target_segment_sequence(resolution_id: str, target_segment_id: str) -> int:
    prefix = f"{resolution_id}:segment:"
    if not target_segment_id.startswith(prefix):
        raise ExecutionContractError("target segment does not belong to the resolution")
    suffix = target_segment_id[len(prefix) :]
    if not suffix.isdigit() or int(suffix) < 1:
        raise ExecutionContractError("target segment must identify a positive segment sequence")
    return int(suffix)


def _event_kind(value: object) -> str:
    result = _require_string(value, "event_kind")
    if _EVENT_KIND_PATTERN.fullmatch(result) is None:
        raise ExecutionContractError("event_kind must be a typed event ID")
    return result


def _roll_request(
    resolution_id: str, value: Mapping[str, object] | None
) -> dict[str, object]:
    if value is None:
        roll_id = f"{resolution_id}:roll:1"
        return {
            "roll_id": roll_id,
            "request_id": roll_id,
            "expression": "fixed",
            "source_kind": "rng.system",
            "provenance_ref": f"{resolution_id}:rng:1",
        }
    request = _mapping_copy(value, "roll request")
    expected = {"roll_id", "request_id", "expression", "source_kind", "provenance_ref"}
    if set(request) != expected:
        raise ExecutionContractError("roll request has unexpected or missing fields")
    _require_id(request["roll_id"], "roll request roll_id")
    _require_id(request["request_id"], "roll request request_id")
    _require_string(request["expression"], "roll request expression")
    _require_roll_source(request["source_kind"])
    _require_string(request["provenance_ref"], "roll request provenance_ref")
    return request


def _require_roll_source(value: object) -> str:
    result = _require_string(value, "roll source_kind")
    if result not in _ROLL_SOURCES:
        raise ExecutionContractError("roll source_kind is unsupported")
    return result


def _roll_result(value: Mapping[str, object]) -> dict[str, object]:
    result = _mapping_copy(value, "roll result")
    if set(result) != _ROLL_FIELDS:
        raise ExecutionContractError("roll result has unexpected or missing fields")
    _require_id(result["roll_id"], "roll result roll_id")
    _require_id(result["request_id"], "roll result request_id")
    _require_string(result["expression"], "roll result expression")
    raw_values = result["raw_values"]
    if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)) or not raw_values:
        raise ExecutionContractError("roll result raw_values must be a nonempty array")
    if any(isinstance(item, bool) or not isinstance(item, int) for item in raw_values):
        raise ExecutionContractError("roll result raw_values must contain integers")
    _require_roll_source(result["source_kind"])
    _require_string(result["provenance_ref"], "roll result provenance_ref")
    return result


def _scalar_exports(payload: Mapping[str, object]) -> dict[str, object]:
    for key, value in payload.items():
        _require_id(key, "receipt export key")
        if value is None or not isinstance(value, (str, int, float, bool)):
            raise ExecutionContractError("receipt exports must contain scalar values")
        if isinstance(value, float) and (value != value or value in {float("inf"), float("-inf")}):
            raise ExecutionContractError("receipt exports must contain finite scalar values")
    return deepcopy(dict(payload))


def _continuation_with_segment(
    continuation: Mapping[str, object],
    segment: Mapping[str, object],
    roll_result: Mapping[str, object] | None,
) -> dict[str, object]:
    result = _mapping_copy(continuation, "continuation state")
    refs = result.get("committed_segment_refs", [])
    if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes)):
        raise ExecutionContractError("continuation committed_segment_refs must be an array")
    segment_id = _require_id(segment.get("segment_id"), "execution segment segment_id")
    committed_refs = list(refs)
    if segment_id not in committed_refs:
        committed_refs.append(segment_id)
    result["committed_segment_refs"] = committed_refs
    if roll_result is not None:
        fixed_results = result.get("fixed_rng_results", [])
        if not isinstance(fixed_results, Sequence) or isinstance(fixed_results, (str, bytes)):
            raise ExecutionContractError("continuation fixed_rng_results must be an array")
        request_id = roll_result["request_id"]
        if not any(
            isinstance(item, Mapping) and item.get("request_id") == request_id
            for item in fixed_results
        ):
            result["fixed_rng_results"] = [*deepcopy(list(fixed_results)), deepcopy(dict(roll_result))]
    generation = result.get("generation")
    if generation is not None:
        if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
            raise ExecutionContractError("continuation generation must be a positive integer")
        result["generation"] = generation + 1
    return result


def _validate_continuation_generation(
    continuation: Mapping[str, object] | None,
    expected_generation: int | None,
) -> None:
    expected = expected_generation
    if expected is None:
        if continuation is not None and "generation" in continuation:
            generation = continuation["generation"]
            if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
                raise ExecutionContractError("continuation generation must be a positive integer")
        return
    if isinstance(expected, bool) or not isinstance(expected, int) or expected < 1:
        raise ExecutionContractError("resolution continuation_generation must be positive")
    if continuation is None:
        raise ExecutionConflict(
            "stale continuation: expected generation is missing",
            failure_code="failure.continuation_stale",
        )
    generation = continuation.get("generation")
    if generation != expected:
        raise ExecutionConflict(
            "stale continuation generation",
            failure_code="failure.continuation_stale",
        )


def _continuation_execution_basis(
    continuation: Mapping[str, object] | None,
) -> dict[str, object] | None:
    if continuation is None:
        return None
    return {
        key: deepcopy(continuation[key])
        for key in (
            "root_command_id",
            "resolution_id",
            "activity_id",
            "actor_id",
            "procedure_id",
            "execution_cursor",
            "safe_recompute_phase",
        )
        if key in continuation
    }


def _resolution_with_segment(
    resolution: Mapping[str, object], segment: Mapping[str, object], roll_result: Mapping[str, object] | None
) -> dict[str, object]:
    result = _mapping_copy(resolution, "resolution")
    segments = result.get("segments", [])
    if not isinstance(segments, Sequence) or isinstance(segments, (str, bytes)):
        raise ExecutionContractError("resolution segments must be an array")
    result["segments"] = [deepcopy(item) for item in segments] + [deepcopy(dict(segment))]
    result["next_segment_sequence"] = int(segment["segment_sequence"]) + 1
    if roll_result is not None:
        fixed_results = result.get("fixed_rng_results", [])
        if not isinstance(fixed_results, Sequence) or isinstance(fixed_results, (str, bytes)):
            raise ExecutionContractError("resolution fixed_rng_results must be an array")
        if not any(
            isinstance(item, Mapping) and item.get("request_id") == roll_result["request_id"]
            for item in fixed_results
        ):
            result["fixed_rng_results"] = [
                *deepcopy(list(fixed_results)),
                deepcopy(dict(roll_result)),
            ]
    return result


def _execution_resolution_basis(resolution: Mapping[str, object]) -> dict[str, object]:
    return {
        key: deepcopy(resolution[key])
        for key in (
            "resolution_id",
            "activity_id",
            "actor_id",
            "source_id",
            "target_ids",
            "parameter_bindings",
            "procedure_id",
            "cursor",
            "execution_cursor",
            "safe_recompute_phase",
        )
        if key in resolution
    }


def _roll_request_from_result(result: Mapping[str, object]) -> dict[str, object]:
    return {
        key: result[key]
        for key in ("roll_id", "request_id", "expression", "source_kind", "provenance_ref")
    }


def _existing_roll_result(
    resolution: Mapping[str, object], request: Mapping[str, object] | None
) -> dict[str, object] | None:
    if request is None:
        return None
    fixed_results = resolution.get("fixed_rng_results", [])
    if not isinstance(fixed_results, Sequence) or isinstance(fixed_results, (str, bytes)):
        raise ExecutionContractError("resolution fixed_rng_results must be an array")
    for value in fixed_results:
        candidate = _roll_result(_require_mapping(value, "resolution fixed RNG result"))
        if candidate["request_id"] == request["request_id"]:
            return candidate
    return None


def _accepted_input_fingerprint(command: Mapping[str, object]) -> str:
    material = {key: _json_copy(command[key], f"accepted command {key}") for key in _ACCEPTED_INPUT_FIELDS}
    encoded = json.dumps(
        material, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(_RUNTIME_COMMAND_INPUT_DOMAIN + encoded).hexdigest()


def _digest(value: Mapping[str, object]) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
