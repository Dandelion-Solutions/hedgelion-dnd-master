#!/usr/bin/env python3
"""Exact, caller-supplied catalog-context binding for HDM execution.

This module neither discovers catalog content nor supplies a default context. A
consumer must bind an exact resolved ruleset lock, definition frontier, and
definition dependencies before it can use an interpreter candidate.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from .ruleset_package import (
    PackageSnapshot,
    RULESET_SET_DIGEST_GENERATION,
    RulesetContractError,
    canonical_json,
    sha256,
    validate_resolved_lock,
)


CATALOG_CONTEXT_FINGERPRINT_GENERATION: Final = 1
CATALOG_CONTEXT_DOMAIN: Final = b"HDM_CATALOG_CONTEXT/1\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")


class CatalogBindingError(ValueError):
    """Raised when an exact catalog context or executable binding is invalid."""


@dataclass(frozen=True)
class BoundCatalogContext:
    """One immutable logical context with reconstructive input evidence."""

    basis: Mapping[str, object]
    definition_dependencies: tuple[Mapping[str, str], ...]
    fingerprint: str

    def to_dict(self) -> dict[str, object]:
        """Return a serializable carrier without exposing mutable internal state."""

        return {
            "basis": _thaw(self.basis),
            "definition_dependencies": [dict(row) for row in self.definition_dependencies],
            "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
            "catalog_context_fingerprint": self.fingerprint,
        }


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_thaw(item) for item in value]
    return value


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise CatalogBindingError(f"{label} must be an object")
    return value


def _require_exact_keys(
    value: object, expected: set[str], label: str, *, optional: set[str] | None = None
) -> Mapping[str, object]:
    mapping = _require_mapping(value, label)
    allowed = expected | (optional or set())
    if set(mapping) - allowed or not expected.issubset(mapping):
        raise CatalogBindingError(f"{label} has unexpected or missing fields")
    return mapping


def _require_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or not value[0].isalpha() or not all(
        character.isalnum() or character in "_.:-" for character in value
    ):
        raise CatalogBindingError(f"{label} must be a native identifier")
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in _SHA256_HEX for character in value
    ):
        raise CatalogBindingError(f"{label} must be a lower-case SHA-256 digest")
    return value


def _require_revision(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise CatalogBindingError(f"{label} must be a non-negative integer")
    return value


def _normalize_frontier(value: object, label: str) -> dict[str, object]:
    frontier = _require_exact_keys(
        value, {"frontier_id", "state_revision", "definition_ids"}, label
    )
    definition_ids = frontier["definition_ids"]
    if not isinstance(definition_ids, Sequence) or isinstance(definition_ids, str):
        raise CatalogBindingError(f"{label}.definition_ids must be an array")
    normalized_ids = [_require_id(item, f"{label}.definition_id") for item in definition_ids]
    if len(normalized_ids) != len(set(normalized_ids)):
        raise CatalogBindingError(f"{label}.definition_ids are ambiguous")
    return {
        "frontier_id": _require_id(frontier["frontier_id"], f"{label}.frontier_id"),
        "state_revision": _require_revision(frontier["state_revision"], f"{label}.state_revision"),
        "definition_ids": sorted(normalized_ids),
    }


def _normalize_basis(value: object) -> dict[str, object]:
    basis = _require_exact_keys(
        value,
        {
            "catalog_generation",
            "engine_contract_inventory_sha256",
            "ruleset_lock",
            "campaign_definition_frontier",
        },
        "catalog context basis",
        optional={"session_overlay_frontier"},
    )
    catalog_generation = _require_revision(basis["catalog_generation"], "catalog_generation")
    if catalog_generation < 1:
        raise CatalogBindingError("catalog_generation must be positive")
    lock = copy.deepcopy(_require_mapping(basis["ruleset_lock"], "ruleset_lock"))
    try:
        validated_lock = validate_resolved_lock(lock)
    except RulesetContractError as exc:
        raise CatalogBindingError(f"ruleset_lock is not reconstructive: {exc.detail}") from exc
    if validated_lock["ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION:
        raise CatalogBindingError("unsupported ruleset set digest generation")
    package_ids: set[str] = set()
    for package in validated_lock["packages"]:
        package_id = package["package_id"]
        if package_id in package_ids:
            raise CatalogBindingError("ruleset_lock package identities are ambiguous")
        package_ids.add(package_id)
        if package["catalog_generation"] != catalog_generation:
            raise CatalogBindingError("ruleset_lock has a mixed catalog generation")
    normalized: dict[str, object] = {
        "catalog_generation": catalog_generation,
        "engine_contract_inventory_sha256": _require_sha256(
            basis["engine_contract_inventory_sha256"], "engine_contract_inventory_sha256"
        ),
        "ruleset_lock": validated_lock,
        "campaign_definition_frontier": _normalize_frontier(
            basis["campaign_definition_frontier"], "campaign_definition_frontier"
        ),
    }
    if "session_overlay_frontier" in basis:
        normalized["session_overlay_frontier"] = _normalize_frontier(
            basis["session_overlay_frontier"], "session_overlay_frontier"
        )
    return normalized


def _normalize_dependencies(
    value: object,
    basis: Mapping[str, object],
    package_snapshots: Mapping[str, PackageSnapshot],
) -> tuple[dict[str, str], ...]:
    if not isinstance(value, Sequence) or isinstance(value, str) or not value:
        raise CatalogBindingError("definition_dependencies must be a nonempty array")
    packages = {
        row["package_id"]: row
        for row in basis["ruleset_lock"]["packages"]
    }
    if set(package_snapshots) != set(packages):
        raise CatalogBindingError("package snapshot evidence is incomplete or ambiguous")
    for package_id, lock_package in packages.items():
        snapshot = package_snapshots[package_id]
        if not isinstance(snapshot, PackageSnapshot):
            raise CatalogBindingError("package snapshot evidence has an invalid source")
        if (
            snapshot.manifest.get("package_id") != package_id
            or snapshot.content_sha256 != lock_package["content_sha256"]
            or set(snapshot.manifest.get("owned_namespaces", ()))
            != set(lock_package["owned_namespaces"])
        ):
            raise CatalogBindingError("package snapshot evidence does not match ruleset_lock")
    frontier_ids = set(basis["campaign_definition_frontier"]["definition_ids"])
    session_frontier = basis.get("session_overlay_frontier")
    if session_frontier is not None:
        frontier_ids.update(session_frontier["definition_ids"])
    dependencies: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for value_row in value:
        row = _require_exact_keys(
            value_row,
            {"definition_id", "kind", "package_id", "package_content_sha256"},
            "catalog definition dependency",
        )
        definition_id = _require_id(row["definition_id"], "definition_id")
        kind = _require_id(row["kind"], "kind")
        package_id = _require_id(row["package_id"], "package_id")
        content_sha256 = _require_sha256(
            row["package_content_sha256"], "package_content_sha256"
        )
        if definition_id in seen_ids:
            raise CatalogBindingError("definition_dependencies contain duplicate definition_id")
        lock_package = packages.get(package_id)
        if lock_package is None or lock_package["content_sha256"] != content_sha256:
            raise CatalogBindingError("definition dependency is not pinned by ruleset_lock")
        namespace = f"{definition_id.partition('.')[0]}.*"
        if namespace not in lock_package["owned_namespaces"]:
            raise CatalogBindingError("definition dependency namespace is not owned by its source")
        if definition_id not in frontier_ids:
            raise CatalogBindingError("definition dependency is outside the current frontier")
        snapshot = package_snapshots[package_id]
        matching_entries = [
            entry
            for entry_key, entry in snapshot.semantic_entries.items()
            if entry_key.endswith(f"|id:{definition_id}")
        ]
        if len(matching_entries) != 1:
            raise CatalogBindingError("definition dependency is absent or ambiguous in source evidence")
        if matching_entries[0].get("kind") != kind:
            raise CatalogBindingError("definition dependency kind differs from source evidence")
        seen_ids.add(definition_id)
        dependencies.append(
            {
                "definition_id": definition_id,
                "kind": kind,
                "package_id": package_id,
                "package_content_sha256": content_sha256,
            }
        )
    return tuple(sorted(dependencies, key=lambda row: row["definition_id"]))


def bind_catalog_context(
    value: object, *, package_snapshots: Mapping[str, PackageSnapshot]
) -> BoundCatalogContext:
    """Bind exact reconstruction inputs; this function never chooses a default."""

    request = _require_exact_keys(
        value, {"basis", "definition_dependencies"}, "catalog binding request"
    )
    basis = _normalize_basis(request["basis"])
    dependencies = _normalize_dependencies(
        request["definition_dependencies"], basis, package_snapshots
    )
    fingerprint_payload = {
        "basis": basis,
        "definition_dependencies": list(dependencies),
    }
    fingerprint = sha256(CATALOG_CONTEXT_DOMAIN + canonical_json(fingerprint_payload))
    frozen_basis = _freeze(basis)
    frozen_dependencies = _freeze(dependencies)
    if not isinstance(frozen_basis, Mapping) or not isinstance(frozen_dependencies, tuple):
        raise AssertionError("catalog context freezing changed the expected carrier shape")
    return BoundCatalogContext(frozen_basis, frozen_dependencies, fingerprint)


def _candidate(value: object) -> tuple[str, str]:
    candidate = _require_exact_keys(value, {"definition_id", "kind"}, "candidate")
    return (
        _require_id(candidate["definition_id"], "candidate definition_id"),
        _require_id(candidate["kind"], "candidate kind"),
    )


def _find_dependency(
    context: BoundCatalogContext, definition_id: str
) -> dict[str, str] | None:
    return next(
        (
            row
            for row in context.definition_dependencies
            if row["definition_id"] == definition_id
        ),
        None,
    )


def bind_interpreter_candidate(
    context: BoundCatalogContext, candidate: object
) -> dict[str, object]:
    """Pin one exact interpreter candidate to its already-bound catalog context."""

    definition_id, kind = _candidate(candidate)
    dependency = _find_dependency(context, definition_id)
    if dependency is None:
        raise CatalogBindingError("definition_not_found")
    if dependency["kind"] != kind:
        raise CatalogBindingError("definition_kind_mismatch")
    lock = context.basis["ruleset_lock"]
    return {
        "definition_id": definition_id,
        "kind": kind,
        "source_package_id": dependency["package_id"],
        "source_package_content_sha256": dependency["package_content_sha256"],
        "catalog_generation": context.basis["catalog_generation"],
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
        "catalog_context_fingerprint": context.fingerprint,
    }


def validate_executable_binding(
    context: BoundCatalogContext, binding: object
) -> None:
    """Reject bindings that were selected under another or forged context."""

    value = _require_exact_keys(
        binding,
        {
            "definition_id",
            "kind",
            "source_package_id",
            "source_package_content_sha256",
            "catalog_generation",
            "ruleset_set_digest_generation",
            "ruleset_set_sha256",
            "catalog_context_fingerprint_generation",
            "catalog_context_fingerprint",
        },
        "executable binding",
    )
    if (
        value["catalog_context_fingerprint_generation"]
        != CATALOG_CONTEXT_FINGERPRINT_GENERATION
        or value["catalog_context_fingerprint"] != context.fingerprint
    ):
        raise CatalogBindingError("stale catalog context")
    lock = context.basis["ruleset_lock"]
    if (
        value["catalog_generation"] != context.basis["catalog_generation"]
        or value["ruleset_set_digest_generation"] != lock["ruleset_set_digest_generation"]
        or value["ruleset_set_sha256"] != lock["ruleset_set_sha256"]
    ):
        raise CatalogBindingError("stale catalog context")
    definition_id, kind = _candidate(
        {"definition_id": value["definition_id"], "kind": value["kind"]}
    )
    dependency = _find_dependency(context, definition_id)
    if dependency is None or dependency["kind"] != kind:
        raise CatalogBindingError("binding definition is no longer pinned")
    if (
        value["source_package_id"] != dependency["package_id"]
        or value["source_package_content_sha256"] != dependency["package_content_sha256"]
    ):
        raise CatalogBindingError("binding source does not match the pinned definition")


def bind_executable_catalog(
    context: BoundCatalogContext, candidate: object
) -> dict[str, object]:
    """Return either an exact executable binding or typed unsupported-gap evidence."""

    try:
        return {"status": "bound", "binding": bind_interpreter_candidate(context, candidate)}
    except CatalogBindingError as exc:
        if str(exc) not in {"definition_not_found", "definition_kind_mismatch"}:
            raise
        definition_id, kind = _candidate(candidate)
        lock = context.basis["ruleset_lock"]
        return {
            "status": "gap",
            "gap_report": {
                "requested_identity": {"definition_id": definition_id, "kind": kind},
                "context_basis": _thaw(context.basis),
                "catalog_generation": context.basis["catalog_generation"],
                "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
                "ruleset_set_sha256": lock["ruleset_set_sha256"],
                "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
                "catalog_context_fingerprint": context.fingerprint,
                "reason": str(exc),
            },
        }
