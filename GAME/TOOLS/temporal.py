"""Owner-local temporal predicate and derived Agenda primitives.

These helpers evaluate only caller-supplied native-owner state and typed
chronology evidence.  They never discover roots, advance an owner, or establish
an accepted execution consequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


_DISPOSITIONS = frozenset({"NOT_DUE", "DUE", "INDETERMINATE"})
_OCCURRENCE_STATES = frozenset({"ARMED", "CLAIMED", "CLOSED"})
_DEPENDENCY_KINDS = frozenset({
    "METRIC_POSITION",
    "BOUNDARY_OCCURRENCE",
    "EVENT_OR_SIGNAL",
    "RELATION_EVIDENCE",
    "OWNER_LOCAL_TEMPORAL_STATE",
})


class TemporalContractError(ValueError):
    """Raised when a caller provides incomplete or non-owner-local temporal data."""


@dataclass(frozen=True)
class TemporalEvaluation:
    disposition: str


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TemporalContractError(f"{label} must be an object")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TemporalContractError(f"{label} must be a non-empty string")
    return value


def _require_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TemporalContractError(f"{label} must be an integer")
    return value


def _validate_binding(binding: Mapping[str, Any]) -> str:
    basis_id = _require_string(binding.get("basis_id"), "binding.basis_id")
    if basis_id == "temporal.metric_deadline":
        _reject_unknown_fields(binding, {"basis_id", "context_id", "anchor_value", "deadline_value", "unit_id"})
        _require_string(binding.get("context_id"), "binding.context_id")
        anchor = _require_integer(binding.get("anchor_value"), "binding.anchor_value")
        deadline = _require_integer(binding.get("deadline_value"), "binding.deadline_value")
        _require_string(binding.get("unit_id"), "binding.unit_id")
        if anchor < 0 or deadline < anchor:
            raise TemporalContractError("metric deadline must not precede its anchor")
    elif basis_id == "temporal.procedure_boundary":
        _reject_unknown_fields(binding, {"basis_id", "boundary_id", "procedure_id", "anchor_id", "subject_id", "offset"})
        for field in ("boundary_id", "procedure_id", "anchor_id"):
            _require_string(binding.get(field), f"binding.{field}")
    elif basis_id == "temporal.semantic_boundary":
        _reject_unknown_fields(binding, {"basis_id", "boundary_id", "anchor_id", "subject_id", "scope_id"})
        for field in ("boundary_id", "anchor_id"):
            _require_string(binding.get(field), f"binding.{field}")
    else:
        raise TemporalContractError(f"unsupported temporal basis: {basis_id}")
    return basis_id


def _reject_unknown_fields(value: Mapping[str, Any], allowed: set[str]) -> None:
    unexpected = set(value).difference(allowed)
    if unexpected:
        raise TemporalContractError(f"unsupported binding field: {sorted(unexpected)[0]}")


def _metric_disposition(position: Mapping[str, Any], deadline: int) -> str:
    kind = _require_string(position.get("kind"), "position.kind")
    if kind == "EXACT":
        value = _require_integer(position.get("value"), "position.value")
        return "DUE" if value >= deadline else "NOT_DUE"
    if kind == "BOUNDED":
        lower = _require_integer(position.get("lower"), "position.lower")
        upper = _require_integer(position.get("upper"), "position.upper")
        if lower > upper:
            raise TemporalContractError("bounded position lower exceeds upper")
        if upper < deadline:
            return "NOT_DUE"
        if lower >= deadline:
            return "DUE"
        return "INDETERMINATE"
    if kind == "UNKNOWN":
        return "INDETERMINATE"
    raise TemporalContractError(f"unsupported position kind: {kind}")


def evaluate_temporal_binding(binding: Mapping[str, Any], evidence: Mapping[str, Any]) -> TemporalEvaluation:
    """Evaluate one owner-local binding from its named provider evidence only."""
    checked_binding = _require_mapping(binding, "binding")
    checked_evidence = _require_mapping(evidence, "evidence")
    basis_id = _validate_binding(checked_binding)
    if basis_id == "temporal.metric_deadline":
        provider_id = _require_string(checked_evidence.get("provider_id"), "evidence.provider_id")
        if provider_id != checked_binding["context_id"]:
            raise TemporalContractError("provider does not match the binding context")
        position = _require_mapping(checked_evidence.get("position"), "evidence.position")
        return TemporalEvaluation(_metric_disposition(position, checked_binding["deadline_value"]))

    boundary_status = checked_evidence.get("boundary_status")
    if not isinstance(boundary_status, Mapping):
        return TemporalEvaluation("INDETERMINATE")
    status = boundary_status.get(checked_binding["boundary_id"])
    if status is None:
        return TemporalEvaluation("INDETERMINATE")
    if status not in _DISPOSITIONS:
        raise TemporalContractError("boundary status is not a temporal disposition")
    return TemporalEvaluation(status)


def validate_current_state_replacement(
    current_state: Mapping[str, Any], replacement: Mapping[str, Any]
) -> dict[str, int | str]:
    """Validate one exact successor without granting CURRENT a chronology frontier."""
    current = _require_mapping(current_state, "current state")
    proposed = _require_mapping(replacement, "replacement current state")
    for value, label in ((current, "current state"), (proposed, "replacement current state")):
        if "chronology_frontier" in value or "world_time" in value:
            raise TemporalContractError(f"{label} cannot carry a global chronology frontier")
    current_revision = _require_integer(current.get("state_revision"), "current state.state_revision")
    replacement_revision = _require_integer(proposed.get("state_revision"), "replacement state_revision")
    if replacement_revision != current_revision + 1:
        raise TemporalContractError("replacement must carry exactly the next revision")
    anchors = proposed.get("chronology_anchor_ids")
    if not isinstance(anchors, Sequence) or isinstance(anchors, (str, bytes)):
        raise TemporalContractError("replacement requires chronology anchor evidence")
    normalized_anchors = tuple(_require_string(anchor, "chronology anchor") for anchor in anchors)
    if len(normalized_anchors) != len(set(normalized_anchors)):
        raise TemporalContractError("replacement has duplicate chronology anchors")
    return {"status": "ACCEPTED", "state_revision": replacement_revision}


def derive_temporal_dependency_keys(root: Mapping[str, Any]) -> tuple[str, ...]:
    """Return the complete declared re-evaluation keys for one armed occurrence."""
    checked_root = _require_mapping(root, "temporal root")
    _require_string(checked_root.get("root_ref"), "root_ref")
    _require_string(checked_root.get("occurrence_id"), "occurrence_id")
    _require_string(checked_root.get("binding_id"), "binding_id")
    state = _require_string(checked_root.get("occurrence_state"), "occurrence_state")
    if state not in _OCCURRENCE_STATES:
        raise TemporalContractError("unknown occurrence state")
    _validate_binding(_require_mapping(checked_root.get("binding"), "binding"))
    keys = checked_root.get("dependency_keys")
    if not isinstance(keys, Sequence) or isinstance(keys, (str, bytes)):
        raise TemporalContractError("dependency keys must be an array")
    normalized = tuple(sorted(_require_string(key, "dependency key") for key in keys))
    if state == "ARMED" and not normalized:
        raise TemporalContractError("armed occurrence requires dependency keys")
    if len(normalized) != len(set(normalized)):
        raise TemporalContractError("duplicate dependency key")
    for key in normalized:
        kind, separator, target = key.partition(":")
        if separator != ":" or kind not in _DEPENDENCY_KINDS or not target:
            raise TemporalContractError("dependency key is not typed")
    return normalized


def materialize_due_occurrence(root: Mapping[str, Any], evaluation: TemporalEvaluation) -> dict[str, str]:
    """Produce a prospective candidate; accepted execution owns any later mutation."""
    if not isinstance(evaluation, TemporalEvaluation):
        raise TemporalContractError("evaluation must be a TemporalEvaluation")
    checked_root = _require_mapping(root, "temporal root")
    derive_temporal_dependency_keys(checked_root)
    if checked_root["occurrence_state"] != "ARMED":
        raise TemporalContractError("occurrence is not armed")
    if evaluation.disposition != "DUE":
        raise TemporalContractError("occurrence is not due")
    return {
        "status": "CANDIDATE",
        "root_ref": checked_root["root_ref"],
        "occurrence_id": checked_root["occurrence_id"],
    }


def rebuild_temporal_agenda(roots: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], ...]:
    """Rebuild derived Agenda entries from explicit roots, never by broad discovery."""
    seen: set[tuple[str, str]] = set()
    entries: list[dict[str, Any]] = []
    for root in roots:
        checked_root = _require_mapping(root, "temporal root")
        root_ref = _require_string(checked_root.get("root_ref"), "root_ref")
        occurrence_id = _require_string(checked_root.get("occurrence_id"), "occurrence_id")
        identity = (root_ref, occurrence_id)
        if identity in seen:
            raise TemporalContractError("duplicate native occurrence")
        seen.add(identity)
        keys = derive_temporal_dependency_keys(checked_root)
        if checked_root["occurrence_state"] == "ARMED":
            entries.append({
                "root_ref": root_ref,
                "occurrence_id": occurrence_id,
                "binding_id": checked_root["binding_id"],
                "dependency_keys": list(keys),
            })
    return tuple(sorted(entries, key=lambda entry: (entry["root_ref"], entry["occurrence_id"])))
