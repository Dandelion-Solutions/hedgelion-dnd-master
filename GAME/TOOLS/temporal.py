"""Owner-local temporal predicate and derived Agenda primitives.

These helpers evaluate only caller-supplied native-owner state and typed
chronology evidence.  They never discover roots, advance an owner, or establish
an accepted execution consequence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


# framework_module_version: 1.0.1
FRAMEWORK_MODULE_VERSION = "1.0.1"


_DISPOSITIONS = frozenset({"NOT_DUE", "DUE", "INDETERMINATE"})
_OCCURRENCE_STATES = frozenset({"ARMED", "CLAIMED", "CLOSED"})
_DEPENDENCY_KINDS = frozenset({
    "METRIC_POSITION",
    "BOUNDARY_OCCURRENCE",
    "EVENT_OR_SIGNAL",
    "RELATION_EVIDENCE",
    "OWNER_LOCAL_TEMPORAL_STATE",
})
_MACHINE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_REVISION = re.compile(r"^(?:[a-f0-9]{40}(?:[a-f0-9]{24})?|[A-Za-z][A-Za-z0-9_.:-]*)$")
_ROUTE_SCOPES = frozenset({"CAMPAIGN", "LIVE"})


class TemporalContractError(ValueError):
    """Raised when a caller provides incomplete or non-owner-local temporal data."""


@dataclass(frozen=True)
class TemporalEvaluation:
    disposition: str


@dataclass(frozen=True, slots=True)
class TemporalRouteEntry:
    """Typed retrieval evidence for one native temporal occurrence.

    The entry deliberately carries identity, binding and dependency references
    only.  It never carries current owner state, chronology values or a due
    result, so moving it between campaign and LIVE cannot create a second
    temporal authority.
    """

    campaign_id: str
    source_scope: str
    source_revision: str
    root_ref: str
    occurrence_id: str
    binding_id: str
    occurrence_state: str
    dependency_keys: tuple[str, ...]
    source_key: tuple[str, str, str] | None = None

    def __post_init__(self) -> None:
        campaign_id = _require_string(self.campaign_id, "route campaign_id")
        scope = _route_scope(self.source_scope)
        revision = _route_revision(self.source_revision)
        root_ref = _require_string(self.root_ref, "route root_ref")
        occurrence_id = _require_string(self.occurrence_id, "route occurrence_id")
        binding_id = _require_string(self.binding_id, "route binding_id")
        state = _require_string(self.occurrence_state, "route occurrence_state")
        if state not in _OCCURRENCE_STATES:
            raise TemporalContractError("route occurrence_state is unknown")
        keys = tuple(_require_string(key, "route dependency key") for key in self.dependency_keys)
        if state == "ARMED" and not keys:
            raise TemporalContractError("armed temporal route entry requires dependency keys")
        if len(keys) != len(set(keys)):
            raise TemporalContractError("route dependency keys must be unique")
        for key in keys:
            kind, separator, target = key.partition(":")
            if separator != ":" or kind not in _DEPENDENCY_KINDS or not target:
                raise TemporalContractError("route dependency key is not typed")
        source_key = _route_source_key(self.source_key, campaign_id, scope)
        object.__setattr__(self, "campaign_id", campaign_id)
        object.__setattr__(self, "source_scope", scope)
        object.__setattr__(self, "source_revision", revision)
        object.__setattr__(self, "root_ref", root_ref)
        object.__setattr__(self, "occurrence_id", occurrence_id)
        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "occurrence_state", state)
        object.__setattr__(self, "dependency_keys", tuple(sorted(keys)))
        object.__setattr__(self, "source_key", source_key)

    def as_mapping(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "source_scope": self.source_scope,
            "source_revision": self.source_revision,
            "source_key": list(self.source_key) if self.source_key is not None else None,
            "root_ref": self.root_ref,
            "occurrence_id": self.occurrence_id,
            "binding_id": self.binding_id,
            "occurrence_state": self.occurrence_state,
            "dependency_keys": list(self.dependency_keys),
        }


@dataclass(frozen=True, slots=True)
class TemporalRoute:
    """Complete ephemeral routing evidence for one exact native source."""

    campaign_id: str
    source_scope: str
    source_revision: str
    entries: tuple[TemporalRouteEntry, ...]
    source_key: tuple[str, str, str] | None = None
    complete: bool = True

    def __post_init__(self) -> None:
        campaign_id = _require_string(self.campaign_id, "temporal route campaign_id")
        scope = _route_scope(self.source_scope)
        revision = _route_revision(self.source_revision)
        if self.complete is not True:
            raise TemporalContractError("temporal route must be complete")
        source_key = _route_source_key(self.source_key, campaign_id, scope)
        entries = tuple(self.entries)
        if any(not isinstance(entry, TemporalRouteEntry) for entry in entries):
            raise TemporalContractError("temporal route entries must be typed")
        identities: set[tuple[str, str]] = set()
        for entry in entries:
            if (
                entry.campaign_id != campaign_id
                or entry.source_scope != scope
                or entry.source_revision != revision
                or entry.source_key != source_key
            ):
                raise TemporalContractError("temporal route entry campaign/source differs from route")
            identity = (entry.root_ref, entry.occurrence_id)
            if identity in identities:
                raise TemporalContractError("temporal route contains duplicate occurrence")
            identities.add(identity)
        object.__setattr__(self, "campaign_id", campaign_id)
        object.__setattr__(self, "source_scope", scope)
        object.__setattr__(self, "source_revision", revision)
        object.__setattr__(self, "entries", entries)
        object.__setattr__(self, "source_key", source_key)

    def as_mapping(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "kind": "runtime.temporal_routing",
            "campaign_id": self.campaign_id,
            "source_scope": self.source_scope,
            "source_revision": self.source_revision,
            "source_key": list(self.source_key) if self.source_key is not None else None,
            "complete": True,
            "entries": [entry.as_mapping() for entry in self.entries],
        }

    @classmethod
    def from_mapping(cls, value: object) -> "TemporalRoute":
        if not isinstance(value, Mapping):
            raise TemporalContractError("temporal route must be an object")
        expected = {
            "schema_version",
            "kind",
            "campaign_id",
            "source_scope",
            "source_revision",
            "source_key",
            "complete",
            "entries",
        }
        if set(value) != expected:
            raise TemporalContractError("temporal route fields are not strict")
        if value["schema_version"] != 1 or value["kind"] != "runtime.temporal_routing":
            raise TemporalContractError("unsupported temporal route")
        raw_entries = value["entries"]
        if not isinstance(raw_entries, Sequence) or isinstance(raw_entries, (str, bytes)):
            raise TemporalContractError("temporal route entries must be an array")
        campaign_id = _require_string(value["campaign_id"], "temporal route campaign_id")
        entries = tuple(_route_entry_from_mapping(item) for item in raw_entries)
        return cls(
            campaign_id=campaign_id,
            source_scope=value["source_scope"],  # type: ignore[arg-type]
            source_revision=value["source_revision"],  # type: ignore[arg-type]
            source_key=value["source_key"],  # type: ignore[arg-type]
            complete=value["complete"],  # type: ignore[arg-type]
            entries=entries,
        )


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TemporalContractError(f"{label} must be an object")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise TemporalContractError(f"{label} must be a non-empty string")
    return value


def _route_scope(value: Any) -> str:
    scope = _require_string(value, "temporal route source_scope").upper()
    if scope not in _ROUTE_SCOPES:
        raise TemporalContractError("temporal route source_scope is not admitted")
    return scope


def _route_revision(value: Any) -> str:
    revision = _require_string(value, "temporal route source_revision")
    if _REVISION.fullmatch(revision) is None:
        raise TemporalContractError("temporal route source_revision is not exact")
    return revision


def _route_source_key(
    value: Any,
    campaign_id: str,
    scope: str,
) -> tuple[str, str, str] | None:
    if scope == "CAMPAIGN":
        if value is not None:
            raise TemporalContractError("campaign temporal route cannot carry a LIVE source key")
        return None
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise TemporalContractError("LIVE temporal route requires an exact source key")
    key = tuple(_require_string(item, "temporal route source key") for item in value)
    if key[0] != campaign_id:
        raise TemporalContractError("temporal route source key belongs to another campaign")
    return key  # type: ignore[return-value]


def _route_entry_from_mapping(value: object) -> TemporalRouteEntry:
    if isinstance(value, TemporalRouteEntry):
        return value
    if not isinstance(value, Mapping):
        raise TemporalContractError("temporal route entry must be an object")
    expected = {
        "campaign_id",
        "source_scope",
        "source_revision",
        "source_key",
        "root_ref",
        "occurrence_id",
        "binding_id",
        "occurrence_state",
        "dependency_keys",
    }
    if set(value) != expected:
        raise TemporalContractError("temporal route entry fields are not strict")
    keys = value["dependency_keys"]
    if not isinstance(keys, Sequence) or isinstance(keys, (str, bytes)):
        raise TemporalContractError("temporal route dependency_keys must be an array")
    return TemporalRouteEntry(
        campaign_id=value["campaign_id"],  # type: ignore[arg-type]
        source_scope=value["source_scope"],  # type: ignore[arg-type]
        source_revision=value["source_revision"],  # type: ignore[arg-type]
        source_key=value["source_key"],  # type: ignore[arg-type]
        root_ref=value["root_ref"],  # type: ignore[arg-type]
        occurrence_id=value["occurrence_id"],  # type: ignore[arg-type]
        binding_id=value["binding_id"],  # type: ignore[arg-type]
        occurrence_state=value["occurrence_state"],  # type: ignore[arg-type]
        dependency_keys=tuple(keys),
    )


def _require_machine_id(value: Any, label: str) -> str:
    result = _require_string(value, label)
    if _MACHINE_ID.fullmatch(result) is None:
        raise TemporalContractError(f"{label} must be a machine ID")
    return result


def _require_integer(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TemporalContractError(f"{label} must be an integer")
    return value


def _validate_binding(binding: Mapping[str, Any]) -> str:
    basis_id = _require_string(binding.get("basis_id"), "binding.basis_id")
    if basis_id == "temporal.metric_deadline":
        _require_exact_fields(binding, {"basis_id", "context_id", "anchor_value", "deadline_value", "unit_id"})
        _require_machine_id(binding["context_id"], "binding.context_id")
        _require_nonnegative_integer(binding["anchor_value"], "binding.anchor_value")
        _require_nonnegative_integer(binding["deadline_value"], "binding.deadline_value")
        _require_machine_id(binding["unit_id"], "binding.unit_id")
    elif basis_id == "temporal.procedure_boundary":
        _require_exact_fields(
            binding,
            {"basis_id", "boundary_id", "procedure_id", "anchor_id"},
            {"subject_id", "offset"},
        )
        for field in ("boundary_id", "procedure_id", "anchor_id"):
            _require_machine_id(binding[field], f"binding.{field}")
        if "subject_id" in binding:
            _require_machine_id(binding["subject_id"], "binding.subject_id")
        if "offset" in binding:
            offset = _require_integer(binding["offset"], "binding.offset")
            if offset < 1:
                raise TemporalContractError("binding.offset must be positive")
    elif basis_id == "temporal.semantic_boundary":
        _require_exact_fields(
            binding,
            {"basis_id", "boundary_id", "anchor_id"},
            {"subject_id", "scope_id"},
        )
        for field in ("boundary_id", "anchor_id"):
            _require_machine_id(binding[field], f"binding.{field}")
        for field in ("subject_id", "scope_id"):
            if field in binding:
                _require_machine_id(binding[field], f"binding.{field}")
    else:
        raise TemporalContractError(f"unsupported temporal basis: {basis_id}")
    return basis_id


def _require_nonnegative_integer(value: Any, label: str) -> int:
    result = _require_integer(value, label)
    if result < 0:
        raise TemporalContractError(f"{label} must be non-negative")
    return result


def _require_exact_fields(
    value: Mapping[str, Any], required: set[str], optional: set[str] | None = None
) -> None:
    allowed = required | (optional or set())
    unexpected = set(value).difference(allowed)
    if unexpected:
        raise TemporalContractError(f"unsupported binding field: {sorted(unexpected)[0]}")
    missing = required.difference(value)
    if missing:
        raise TemporalContractError(f"missing binding field: {sorted(missing)[0]}")


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


def validate_chronology_relation_evidence(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one typed sparse chronology relation without inventing a clock."""
    relation = _require_mapping(evidence, "chronology relation")
    relation_type = _require_string(relation.get("relation_type"), "relation_type")
    if relation_type == "CAUSES":
        _require_relation_fields(relation, {"relation_type", "cause_anchor_id", "effect_anchor_id", "scope_id"})
        for field in ("cause_anchor_id", "effect_anchor_id", "scope_id"):
            _require_machine_id(relation[field], field)
    elif relation_type == "PRECEDES":
        _require_relation_fields(
            relation,
            {"relation_type", "predecessor_anchor_id", "successor_anchor_id", "order_domain_id", "scope_id"},
        )
        for field in ("predecessor_anchor_id", "successor_anchor_id", "order_domain_id", "scope_id"):
            _require_machine_id(relation[field], field)
    elif relation_type == "SAME_COORDINATE":
        _require_relation_fields(
            relation,
            {"relation_type", "first_anchor_id", "second_anchor_id", "provider_scope_id", "context_id", "coordinate"},
        )
        for field in ("first_anchor_id", "second_anchor_id", "provider_scope_id", "context_id"):
            _require_machine_id(relation[field], field)
        _validate_coordinate(_require_mapping(relation["coordinate"], "coordinate"))
    elif relation_type == "ELAPSED":
        _require_relation_fields(
            relation,
            {"relation_type", "start_anchor_id", "end_anchor_id", "provider_scope_id", "context_id", "elapsed"},
        )
        for field in ("start_anchor_id", "end_anchor_id", "provider_scope_id", "context_id"):
            _require_machine_id(relation[field], field)
        _validate_interval(_require_mapping(relation["elapsed"], "elapsed"))
    else:
        raise TemporalContractError(f"unsupported chronology relation: {relation_type}")
    return dict(relation)


def _require_relation_fields(value: Mapping[str, Any], required: set[str]) -> None:
    unexpected = set(value).difference(required)
    if unexpected:
        raise TemporalContractError(f"unsupported chronology relation field: {sorted(unexpected)[0]}")
    missing = required.difference(value)
    if missing:
        raise TemporalContractError(f"missing chronology relation field: {sorted(missing)[0]}")


def _validate_coordinate(coordinate: Mapping[str, Any]) -> None:
    kind = _require_string(coordinate.get("kind"), "coordinate.kind")
    if kind == "EXACT":
        _require_relation_fields(coordinate, {"kind", "value", "unit_id"})
        _require_integer(coordinate["value"], "coordinate.value")
    elif kind == "BOUNDED":
        _require_relation_fields(coordinate, {"kind", "lower", "upper", "unit_id"})
        _validate_ordered_integer_range(coordinate["lower"], coordinate["upper"], "coordinate")
    else:
        raise TemporalContractError(f"unsupported coordinate kind: {kind}")
    _require_machine_id(coordinate["unit_id"], "coordinate.unit_id")


def _validate_interval(interval: Mapping[str, Any]) -> None:
    _require_relation_fields(interval, {"lower", "upper", "unit_id"})
    _validate_nonnegative_integer_range(interval["lower"], interval["upper"], "elapsed")
    _require_machine_id(interval["unit_id"], "elapsed.unit_id")


def _validate_ordered_integer_range(lower: Any, upper: Any, label: str) -> None:
    checked_lower = _require_integer(lower, f"{label}.lower")
    checked_upper = _require_integer(upper, f"{label}.upper")
    if checked_lower > checked_upper:
        raise TemporalContractError(f"{label}.lower must not exceed {label}.upper")


def _validate_nonnegative_integer_range(lower: Any, upper: Any, label: str) -> None:
    checked_lower = _require_nonnegative_integer(lower, f"{label}.lower")
    checked_upper = _require_nonnegative_integer(upper, f"{label}.upper")
    if checked_lower > checked_upper:
        raise TemporalContractError(f"{label}.lower must not exceed {label}.upper")


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


def derive_temporal_route_entry(
    root: Mapping[str, Any],
    *,
    campaign_id: str,
    source_scope: str,
    source_revision: str,
    source_key: Sequence[str] | None = None,
) -> TemporalRouteEntry:
    """Derive routing evidence from one explicit native temporal owner.

    The complete owner binding is validated at derivation time, then only its
    stable retrieval identity and dependency references are retained in the
    route.  This prevents a route companion from becoming a copy of current
    owner state or chronology authority.
    """

    checked_root = _require_mapping(root, "temporal root")
    checked_campaign = _require_string(campaign_id, "campaign_id")
    scope = _route_scope(source_scope)
    revision = _route_revision(source_revision)
    _validate_binding(_require_mapping(checked_root.get("binding"), "temporal root.binding"))
    dependencies = derive_temporal_dependency_keys(checked_root)
    root_campaign = checked_root.get("campaign_id")
    if root_campaign is not None and root_campaign != checked_campaign:
        raise TemporalContractError("temporal owner belongs to another campaign")
    return TemporalRouteEntry(
        campaign_id=checked_campaign,
        source_scope=scope,
        source_revision=revision,
        source_key=source_key,
        root_ref=_require_string(checked_root.get("root_ref"), "root_ref"),
        occurrence_id=_require_string(checked_root.get("occurrence_id"), "occurrence_id"),
        binding_id=_require_string(checked_root.get("binding_id"), "binding_id"),
        occurrence_state=_require_string(checked_root.get("occurrence_state"), "occurrence_state"),
        dependency_keys=dependencies,
    )


def _coerce_temporal_route(value: TemporalRoute | Mapping[str, Any]) -> TemporalRoute:
    if isinstance(value, TemporalRoute):
        return value
    return TemporalRoute.from_mapping(value)


def resolve_temporal_dependency_dependents(
    route: TemporalRoute | Mapping[str, Any],
    dependency_key: str,
    *,
    campaign_id: str | None = None,
) -> tuple[TemporalRouteEntry, ...]:
    """Resolve only the entries named by one typed dependency key."""

    resolved = _coerce_temporal_route(route)
    if campaign_id is not None and resolved.campaign_id != _require_string(campaign_id, "campaign_id"):
        raise TemporalContractError("temporal route belongs to another campaign")
    key = _require_string(dependency_key, "dependency_key")
    kind, separator, target = key.partition(":")
    if separator != ":" or kind not in _DEPENDENCY_KINDS or not target:
        raise TemporalContractError("dependency key is not typed")
    return tuple(entry for entry in resolved.entries if key in entry.dependency_keys)


def reconcile_temporal_route_membership(
    route: TemporalRoute | Mapping[str, Any],
    *,
    expected_source_scope: str,
    expected_source_revision: str,
    target_source_scope: str,
    target_source_revision: str,
    expected_source_key: Sequence[str] | None = None,
    target_source_key: Sequence[str] | None = None,
    campaign_id: str | None = None,
    terminal_root_refs: Sequence[str] = (),
    superseded_root_refs: Sequence[str] = (),
) -> TemporalRoute:
    """Move complete temporal routing membership across one exact source edge.

    Both the predecessor and successor source identities are explicit.  The
    operation is idempotent when the route already describes the requested
    successor, which makes an interrupted handoff retryable without scanning
    owners or inventing chronology.
    """

    current = _coerce_temporal_route(route)
    if campaign_id is not None and current.campaign_id != _require_string(campaign_id, "campaign_id"):
        raise TemporalContractError("temporal route belongs to another campaign")
    expected_scope = _route_scope(expected_source_scope)
    target_scope = _route_scope(target_source_scope)
    expected_revision = _route_revision(expected_source_revision)
    target_revision = _route_revision(target_source_revision)
    normalized_expected_key = _route_source_key(expected_source_key, current.campaign_id, expected_scope)
    normalized_target_key = _route_source_key(target_source_key, current.campaign_id, target_scope)
    if current.source_scope != expected_scope or current.source_revision != expected_revision:
        raise TemporalContractError("temporal route predecessor source/revision is stale")
    if current.source_key != normalized_expected_key:
        raise TemporalContractError("temporal route predecessor source differs")

    terminal = {_require_string(value, "terminal root_ref") for value in terminal_root_refs}
    superseded = {_require_string(value, "superseded root_ref") for value in superseded_root_refs}
    if terminal.intersection(superseded):
        raise TemporalContractError("terminal and superseded temporal roots overlap")
    known = {entry.root_ref for entry in current.entries}
    unknown = (terminal | superseded).difference(known)
    if unknown and not (
        current.source_scope == target_scope
        and current.source_revision == target_revision
        and current.source_key == normalized_target_key
    ):
        raise TemporalContractError("temporal root removal is not bound to the exact route")
    terminal_entries = tuple(entry for entry in current.entries if entry.root_ref in terminal)
    if any(entry.occurrence_state != "CLOSED" for entry in terminal_entries):
        raise TemporalContractError("terminal temporal roots require CLOSED owner state")

    moved = tuple(
        TemporalRouteEntry(
            campaign_id=entry.campaign_id,
            source_scope=target_scope,
            source_revision=target_revision,
            source_key=normalized_target_key,
            root_ref=entry.root_ref,
            occurrence_id=entry.occurrence_id,
            binding_id=entry.binding_id,
            occurrence_state=entry.occurrence_state,
            dependency_keys=entry.dependency_keys,
        )
        for entry in current.entries
        if entry.root_ref not in terminal and entry.root_ref not in superseded
    )
    return TemporalRoute(
        campaign_id=current.campaign_id,
        source_scope=target_scope,
        source_revision=target_revision,
        source_key=normalized_target_key,
        entries=moved,
        complete=True,
    )


def rebuild_temporal_agenda_from_route(
    route: TemporalRoute | Mapping[str, Any],
    *,
    campaign_id: str | None = None,
) -> tuple[dict[str, Any], ...]:
    """Rebuild disposable Agenda entries from complete route evidence."""

    resolved = _coerce_temporal_route(route)
    if campaign_id is not None and resolved.campaign_id != _require_string(campaign_id, "campaign_id"):
        raise TemporalContractError("temporal route belongs to another campaign")
    entries: list[dict[str, Any]] = []
    for entry in resolved.entries:
        if entry.occurrence_state == "ARMED":
            entries.append(
                {
                    "root_ref": entry.root_ref,
                    "occurrence_id": entry.occurrence_id,
                    "binding_id": entry.binding_id,
                    "dependency_keys": list(entry.dependency_keys),
                }
            )
    return tuple(sorted(entries, key=lambda item: (item["root_ref"], item["occurrence_id"])))
