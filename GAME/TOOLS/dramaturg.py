"""Noncanonical bounded Dramaturg horizon validation, admission, and safe rebase."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy


class DramaturgContractError(ValueError):
    """Raised when prospective planning is treated as authority or is stale."""


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise DramaturgContractError(f"{label} must be a nonempty string")
    return value


def _source_basis(value: object) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise DramaturgContractError("source_basis must be an array")
    basis = [_nonempty_string(item, "source basis") for item in value]
    if not basis or len(basis) != len(set(basis)):
        raise DramaturgContractError("source_basis must be nonempty and unique")
    return basis


def validate_dramaturg_horizon(value: object) -> dict[str, object]:
    """Validate prospective planning without admitting future facts or canonical state."""

    if not isinstance(value, Mapping):
        raise DramaturgContractError("Dramaturg horizon must be an object")
    expected = {"schema_version", "scope_id", "generation", "source_basis", "entries"}
    if set(value) != expected:
        raise DramaturgContractError("Dramaturg horizon has unsupported or missing fields")
    generation = value["generation"]
    version = value["schema_version"]
    if version != 1 or isinstance(version, bool):
        raise DramaturgContractError("unsupported schema_version")
    if not isinstance(generation, int) or isinstance(generation, bool) or generation < 1:
        raise DramaturgContractError("generation must be a positive integer")
    entries = value["entries"]
    if not isinstance(entries, Sequence) or isinstance(entries, str):
        raise DramaturgContractError("entries must be an array")
    normalized_entries: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {"kind", "text"}:
            raise DramaturgContractError("Dramaturg entry has unsupported or missing fields")
        kind = _nonempty_string(entry["kind"], "Dramaturg entry kind")
        if kind not in {"SOURCE_ANCHORED_CONSTRAINT", "PROVISIONAL_DRAMATURGIC_DIRECTION"}:
            raise DramaturgContractError("unsupported Dramaturg entry kind")
        normalized_entries.append({"kind": kind, "text": _nonempty_string(entry["text"], "Dramaturg entry text")})
    return {
        "schema_version": version,
        "scope_id": _nonempty_string(value["scope_id"], "scope_id"),
        "generation": generation,
        "source_basis": _source_basis(value["source_basis"]),
        "entries": normalized_entries,
    }


def admit_dramaturg_horizon(value: object, *, mode: str) -> dict[str, object]:
    """Admit only the retained multiplayer planning family, never single-player bytes."""

    if mode != "multiplayer":
        raise DramaturgContractError("retained Dramaturg horizons require multiplayer mode")
    return validate_dramaturg_horizon(value)


def rebase_dramaturg_horizon(value: object, *, current_source_basis: object) -> dict[str, object]:
    """Keep only an exact compatible native basis; no text merge or authority override."""

    horizon = validate_dramaturg_horizon(value)
    current = _source_basis(current_source_basis)
    if horizon["source_basis"] != current:
        raise DramaturgContractError("stale Dramaturg horizon requires discard or explicit reprepare")
    return deepcopy(horizon)
