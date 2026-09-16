#!/usr/bin/env python3
"""Exact, caller-supplied catalog-context binding for HDM execution.

This module neither discovers catalog content nor supplies a default context. A
consumer must bind an exact resolved ruleset lock, definition frontier,
definition dependencies, and admitted immutable engine/campaign/session source
evidence before it can use an interpreter candidate.
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
    _validated_engine_contract_entries,
    build_resolved_lock,
    canonical_json,
    sha256,
    validate_resolved_lock,
)


CATALOG_CONTEXT_FINGERPRINT_GENERATION: Final = 1
CATALOG_CONTEXT_DOMAIN: Final = b"HDM_CATALOG_CONTEXT/1\n"
NATURAL_OWNER_EVIDENCE_DOMAIN: Final = b"HDM_CATALOG_NATURAL_OWNER_EVIDENCE/1\n"
_SHA256_HEX: Final = frozenset("0123456789abcdef")
_NATURAL_OWNER_SCOPES: Final = {
    "campaign": "campaign.definition_frontier",
    "session": "session.overlay_frontier",
}
_NATURAL_OWNER_ROUTE_PREFIXES: Final = {
    "campaign": "campaign/definitions/",
    "session": "session/overlays/",
}


class CatalogBindingError(ValueError):
    """Raised when an exact catalog context or executable binding is invalid."""


@dataclass(frozen=True)
class BoundCatalogContext:
    """One immutable logical context with reconstructive input evidence."""

    basis: Mapping[str, object]
    definition_dependencies: tuple[Mapping[str, object], ...]
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
            "engine_version",
            "engine_contract_inventory_sha256",
            "engine_contract_inventory",
            "ruleset_lock",
            "campaign_definition_frontier",
            "natural_owner_evidence",
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
    engine_version = _require_nonempty_string(basis["engine_version"], "engine_version")
    inventory = copy.deepcopy(
        _require_mapping(basis["engine_contract_inventory"], "engine_contract_inventory")
    )
    inventory_sha256 = _require_sha256(
        basis["engine_contract_inventory_sha256"], "engine_contract_inventory_sha256"
    )
    if inventory.get("inventory_sha256") != inventory_sha256:
        raise CatalogBindingError("engine contract inventory digest does not match its basis")
    try:
        _validated_engine_contract_entries(
            inventory,
            engine_version=engine_version,
            ruleset_set_sha256=validated_lock["ruleset_set_sha256"],
            ruleset_set_digest_generation=validated_lock["ruleset_set_digest_generation"],
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"engine contract inventory is not admitted evidence: {exc.detail}"
        ) from exc
    normalized: dict[str, object] = {
        "catalog_generation": catalog_generation,
        "engine_version": engine_version,
        "engine_contract_inventory_sha256": inventory_sha256,
        "engine_contract_inventory": inventory,
        "ruleset_lock": validated_lock,
        "campaign_definition_frontier": _normalize_frontier(
            basis["campaign_definition_frontier"], "campaign_definition_frontier"
        ),
        "natural_owner_evidence": _normalize_natural_owner_evidence(
            basis["natural_owner_evidence"]
        ),
    }
    if "session_overlay_frontier" in basis:
        normalized["session_overlay_frontier"] = _normalize_frontier(
            basis["session_overlay_frontier"], "session_overlay_frontier"
        )
    return normalized


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CatalogBindingError(f"{label} must be a nonempty string")
    return value


def _require_route(value: object, label: str) -> str:
    route = _require_nonempty_string(value, label)
    components = route.split("/")
    if any(not component or component.casefold() == "latest" for component in components):
        raise CatalogBindingError(
            f"{label} must be an exact route, not an ambient/latest selector"
        )
    return route


def _require_canonical_natural_owner_route(
    value: object, *, owner_domain: str, definition_id: str
) -> str:
    route = _require_route(value, "natural owner route")
    expected = f"{_NATURAL_OWNER_ROUTE_PREFIXES[owner_domain]}{definition_id}.json"
    if route != expected:
        raise CatalogBindingError("natural owner route is not canonical")
    return route


def _normalize_natural_owner_evidence(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise CatalogBindingError("natural_owner_evidence must be an array")
    evidence_rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for raw_row in value:
        row = _require_exact_keys(
            raw_row,
            {
                "definition_id",
                "kind",
                "owner_domain",
                "scope",
                "route",
                "pinned_revision",
                "content_sha256",
            },
            "natural owner evidence",
        )
        definition_id = _require_id(row["definition_id"], "natural owner definition_id")
        owner_domain = _require_nonempty_string(row["owner_domain"], "owner_domain")
        scope = _require_nonempty_string(row["scope"], "scope")
        if _NATURAL_OWNER_SCOPES.get(owner_domain) != scope:
            raise CatalogBindingError("natural owner domain and scope do not match")
        if definition_id in seen_ids:
            raise CatalogBindingError("natural owner evidence is ambiguous")
        seen_ids.add(definition_id)
        evidence_rows.append(
            {
                "definition_id": definition_id,
                "kind": _require_id(row["kind"], "natural owner kind"),
                "owner_domain": owner_domain,
                "scope": scope,
                "route": _require_canonical_natural_owner_route(
                    row["route"], owner_domain=owner_domain, definition_id=definition_id
                ),
                "pinned_revision": _require_revision(
                    row["pinned_revision"], "natural owner pinned_revision"
                ),
                "content_sha256": _require_sha256(
                    row["content_sha256"], "natural owner content_sha256"
                ),
            }
        )
    return tuple(sorted(evidence_rows, key=lambda row: str(row["definition_id"])))


def _validate_admitted_source_evidence(
    basis: Mapping[str, object],
    *,
    engine_contract_inventory_source: object,
    natural_owner_sources: object,
) -> None:
    source_inventory = copy.deepcopy(
        _require_mapping(engine_contract_inventory_source, "engine contract inventory source")
    )
    try:
        _validated_engine_contract_entries(
            source_inventory,
            engine_version=str(basis["engine_version"]),
            ruleset_set_sha256=str(basis["ruleset_lock"]["ruleset_set_sha256"]),
            ruleset_set_digest_generation=int(
                basis["ruleset_lock"]["ruleset_set_digest_generation"]
            ),
        )
    except (RulesetContractError, KeyError, TypeError, ValueError) as exc:
        detail = exc.detail if isinstance(exc, RulesetContractError) else str(exc)
        raise CatalogBindingError(
            f"engine contract inventory source is not admitted evidence: {detail}"
        ) from exc
    if source_inventory != basis["engine_contract_inventory"]:
        raise CatalogBindingError("engine contract inventory differs from admitted source evidence")

    sources = _require_mapping(natural_owner_sources, "natural owner sources")
    evidence_by_domain = {
        owner_domain: tuple(
            row
            for row in basis["natural_owner_evidence"]
            if row["owner_domain"] == owner_domain
        )
        for owner_domain in _NATURAL_OWNER_SCOPES
    }
    expected_domains = {
        owner_domain for owner_domain, rows in evidence_by_domain.items() if rows
    }
    if set(sources) != expected_domains:
        raise CatalogBindingError("natural owner sources do not match admitted owner domains")
    for owner_domain in sorted(expected_domains):
        source = _require_exact_keys(
            sources[owner_domain],
            {"selected_frontier", "members", "immutable_member_bytes"},
            "natural owner source",
        )
        frontier_key = (
            "campaign_definition_frontier"
            if owner_domain == "campaign"
            else "session_overlay_frontier"
        )
        if frontier_key not in basis:
            raise CatalogBindingError("natural owner source has no selected context frontier")
        selected_frontier = _normalize_frontier(
            source["selected_frontier"], f"{owner_domain} source selected_frontier"
        )
        if selected_frontier != basis[frontier_key]:
            raise CatalogBindingError("natural owner selected frontier differs from context basis")
        admitted_members = _normalize_natural_owner_evidence(source["members"])
        if any(row["owner_domain"] != owner_domain for row in admitted_members):
            raise CatalogBindingError("natural owner source member has the wrong domain")
        if admitted_members != evidence_by_domain[owner_domain]:
            raise CatalogBindingError("natural owner evidence differs from admitted source membership")
        if not {
            str(row["definition_id"]) for row in admitted_members
        }.issubset(set(selected_frontier["definition_ids"])):
            raise CatalogBindingError("natural owner member is absent from its selected frontier")
        immutable_member_bytes = _require_mapping(
            source["immutable_member_bytes"], "natural owner immutable member bytes"
        )
        expected_routes = {str(row["route"]) for row in admitted_members}
        if set(immutable_member_bytes) != expected_routes:
            raise CatalogBindingError("natural owner immutable member bytes are incomplete")
        for row in admitted_members:
            raw_content = immutable_member_bytes[row["route"]]
            if not isinstance(raw_content, bytes):
                raise CatalogBindingError("natural owner immutable member content must be bytes")
            if sha256(raw_content) != row["content_sha256"]:
                raise CatalogBindingError(
                    "natural owner content digest differs from immutable owner bytes"
                )


def _rebuild_definition_sources(
    basis: Mapping[str, object], package_snapshots: Mapping[str, PackageSnapshot]
) -> dict[str, dict[str, str]]:
    packages = {
        row["package_id"]: row
        for row in basis["ruleset_lock"]["packages"]
    }
    if set(package_snapshots) != set(packages):
        raise CatalogBindingError("package snapshot evidence is incomplete or ambiguous")
    source_dirs = []
    for snapshot in package_snapshots.values():
        if not isinstance(snapshot, PackageSnapshot):
            raise CatalogBindingError("package snapshot evidence has an invalid source")
        source_dirs.append(snapshot.package_dir)
    try:
        rebuilt_lock, rebuilt_snapshots = build_resolved_lock(
            source_dirs,
            root_package_ids=basis["ruleset_lock"]["root_package_ids"],
            engine_version=basis["engine_version"],
            catalog_generation=basis["catalog_generation"],
        )
    except RulesetContractError as exc:
        raise CatalogBindingError(
            f"package snapshot source cannot rebuild an admitted lock: {exc.detail}"
        ) from exc
    if rebuilt_lock != basis["ruleset_lock"]:
        raise CatalogBindingError("rebuilt admitted lock does not match ruleset_lock")

    definitions: dict[str, dict[str, str]] = {}
    for package_id, rebuilt in rebuilt_snapshots.items():
        lock_package = packages[package_id]
        for entry_key, entry in rebuilt.semantic_entries.items():
            _prefix, marker, definition_id = entry_key.rpartition("|id:")
            kind = entry.get("kind")
            if not marker or not isinstance(kind, str) or not kind.startswith("definition."):
                continue
            namespace = f"{definition_id.partition('.')[0]}.*"
            if namespace not in lock_package["owned_namespaces"]:
                raise CatalogBindingError("source definition is outside its package namespace")
            if definition_id in definitions:
                raise CatalogBindingError("cross-source definition collision")
            definitions[definition_id] = {
                "package_id": package_id,
                "kind": kind,
                "package_content_sha256": rebuilt.content_sha256,
            }
    return definitions


def _normalize_dependencies(
    value: object,
    basis: Mapping[str, object],
    package_snapshots: Mapping[str, PackageSnapshot],
) -> tuple[dict[str, str], ...]:
    if not isinstance(value, Sequence) or isinstance(value, str) or not value:
        raise CatalogBindingError("definition_dependencies must be a nonempty array")
    source_definitions = _rebuild_definition_sources(basis, package_snapshots)
    natural_evidence = {
        str(row["definition_id"]): row for row in basis["natural_owner_evidence"]
    }
    dependencies: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for value_row in value:
        row = _require_mapping(value_row, "catalog definition dependency")
        source_type = _require_nonempty_string(
            row.get("source_type"), "dependency source_type"
        )
        if source_type == "ruleset_package":
            row = _require_exact_keys(
                row,
                {
                    "source_type",
                    "definition_id",
                    "kind",
                    "package_id",
                    "package_content_sha256",
                },
                "ruleset package definition dependency",
            )
            definition_id = _require_id(row["definition_id"], "definition_id")
            kind = _require_id(row["kind"], "kind")
            if definition_id in seen_ids:
                raise CatalogBindingError("definition_dependencies contain duplicate definition_id")
            package_id = _require_id(row["package_id"], "package_id")
            content_sha256 = _require_sha256(
                row["package_content_sha256"], "package_content_sha256"
            )
            source_definition = source_definitions.get(definition_id)
            if source_definition is None:
                raise CatalogBindingError(
                    "definition dependency is absent from rebuilt source evidence"
                )
            if (
                source_definition["package_id"] != package_id
                or source_definition["package_content_sha256"] != content_sha256
            ):
                raise CatalogBindingError(
                    "definition dependency source does not match rebuilt evidence"
                )
            if source_definition["kind"] != kind:
                raise CatalogBindingError("definition dependency kind differs from rebuilt evidence")
            normalized_dependency: dict[str, object] = {
                "source_type": source_type,
                "definition_id": definition_id,
                "kind": kind,
                "package_id": package_id,
                "package_content_sha256": content_sha256,
            }
        elif source_type == "natural_owner":
            row = _require_exact_keys(
                row,
                {
                    "source_type",
                    "definition_id",
                    "kind",
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                    "evidence_sha256",
                },
                "natural owner definition dependency",
            )
            definition_id = _require_id(row["definition_id"], "definition_id")
            kind = _require_id(row["kind"], "kind")
            if definition_id in seen_ids:
                raise CatalogBindingError("definition_dependencies contain duplicate definition_id")
            if definition_id in source_definitions:
                raise CatalogBindingError(
                    "natural owner definition collides with a package definition"
                )
            evidence = natural_evidence.get(definition_id)
            if evidence is None:
                raise CatalogBindingError("natural owner evidence is missing")
            expected = {
                key: evidence[key]
                for key in (
                    "definition_id",
                    "kind",
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                )
            }
            actual = {key: row[key] for key in expected}
            if actual != expected:
                raise CatalogBindingError("natural owner dependency does not match pinned evidence")
            evidence_sha256 = _require_sha256(row["evidence_sha256"], "evidence_sha256")
            if evidence_sha256 != sha256(
                NATURAL_OWNER_EVIDENCE_DOMAIN + canonical_json(evidence)
            ):
                raise CatalogBindingError("natural owner evidence digest mismatch")
            normalized_dependency = {
                "source_type": source_type,
                **expected,
                "evidence_sha256": evidence_sha256,
            }
        else:
            raise CatalogBindingError("unsupported dependency source_type")
        seen_ids.add(definition_id)
        dependencies.append(normalized_dependency)
    return tuple(sorted(dependencies, key=lambda row: row["definition_id"]))


def bind_catalog_context(
    value: object,
    *,
    package_snapshots: Mapping[str, PackageSnapshot],
    engine_contract_inventory_source: object,
    natural_owner_sources: object,
) -> BoundCatalogContext:
    """Bind exact reconstruction inputs; this function never chooses a default."""

    request = _require_exact_keys(
        value, {"basis", "definition_dependencies"}, "catalog binding request"
    )
    basis = _normalize_basis(request["basis"])
    _validate_admitted_source_evidence(
        basis,
        engine_contract_inventory_source=engine_contract_inventory_source,
        natural_owner_sources=natural_owner_sources,
    )
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
) -> Mapping[str, object] | None:
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
    binding: dict[str, object] = {
        "definition_id": definition_id,
        "kind": kind,
        "source_type": dependency["source_type"],
        "catalog_generation": context.basis["catalog_generation"],
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "catalog_context_fingerprint_generation": CATALOG_CONTEXT_FINGERPRINT_GENERATION,
        "catalog_context_fingerprint": context.fingerprint,
    }
    if dependency["source_type"] == "ruleset_package":
        binding.update(
            {
                "source_package_id": dependency["package_id"],
                "source_package_content_sha256": dependency["package_content_sha256"],
            }
        )
    else:
        binding.update(
            {
                key: dependency[key]
                for key in (
                    "owner_domain",
                    "scope",
                    "route",
                    "pinned_revision",
                    "evidence_sha256",
                )
            }
        )
    return binding


def validate_executable_binding(
    context: BoundCatalogContext, binding: object
) -> None:
    """Reject bindings that were selected under another or forged context."""

    raw_binding = _require_mapping(binding, "executable binding")
    source_type = _require_nonempty_string(raw_binding.get("source_type"), "source_type")
    common_fields = {
        "definition_id",
        "kind",
        "source_type",
        "catalog_generation",
        "ruleset_set_digest_generation",
        "ruleset_set_sha256",
        "catalog_context_fingerprint_generation",
        "catalog_context_fingerprint",
    }
    if source_type == "ruleset_package":
        value = _require_exact_keys(
            raw_binding,
            common_fields | {"source_package_id", "source_package_content_sha256"},
            "ruleset package executable binding",
        )
    elif source_type == "natural_owner":
        value = _require_exact_keys(
            raw_binding,
            common_fields
            | {"owner_domain", "scope", "route", "pinned_revision", "evidence_sha256"},
            "natural owner executable binding",
        )
    else:
        raise CatalogBindingError("unsupported binding source_type")
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
    if value["source_type"] != dependency["source_type"]:
        raise CatalogBindingError("binding source does not match the pinned definition")
    if value["source_type"] == "ruleset_package":
        source_fields = ("package_id", "package_content_sha256")
        binding_fields = ("source_package_id", "source_package_content_sha256")
    else:
        source_fields = ("owner_domain", "scope", "route", "pinned_revision", "evidence_sha256")
        binding_fields = source_fields
    if any(
        value[binding_key] != dependency[source_key]
        for binding_key, source_key in zip(binding_fields, source_fields, strict=True)
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
