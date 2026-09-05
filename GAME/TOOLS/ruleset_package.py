#!/usr/bin/env python3
"""Bounded S6D-11 ruleset package builder/loader/compatibility reference.

Shipped bounded ruleset manifest, lock and compatibility contract. It reads only
explicit package bytes and caller-supplied generated provenance; never DEV sources.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


PACKAGE_SNAPSHOT_DIGEST_GENERATION = 1
RULESET_SET_DIGEST_GENERATION = 1
SEMANTIC_ENTRY_DIGEST_GENERATION = 1
COMPATIBILITY_EVIDENCE_DIGEST_GENERATION = 1
ENGINE_CONTRACT_INVENTORY_DIGEST_GENERATION = 1
CONFORMANCE_ATTESTATION_DIGEST_GENERATION = 1

PACKAGE_DOMAIN = b"HDM_RULESET_PACKAGE_SNAPSHOT/1\n"
SET_DOMAIN = b"HDM_RESOLVED_RULESET_SET/1\n"
ENTRY_DOMAIN = b"HDM_RULESET_SEMANTIC_ENTRY/1\n"
EVIDENCE_DOMAIN = b"HDM_RULESET_COMPATIBILITY_EVIDENCE/1\n"
INVENTORY_DOMAIN = b"HDM_RULESET_ENGINE_CONTRACT_INVENTORY/1\n"
ATTESTATION_DOMAIN = b"HDM_RULESET_CONFORMANCE_ATTESTATION/1\n"
MANIFEST_NAME = "ruleset-package-manifest.json"

LOAD_FAILURE_REASONS = (
    "invalid_manifest", "content_mismatch", "missing_dependency",
    "ambiguous_dependency", "dependency_cycle", "package_id_ambiguity",
    "namespace_conflict", "engine_incompatibility", "catalog_incompatibility",
    "resolved_set_mismatch", "unreconstructable_context",
)
REQUIRED_ENGINE_CONTRACT_FAMILIES = frozenset({
    "catalog_admission", "mechanical_surface", "primitive",
    "portable_value", "schema_contract",
})
COMPATIBILITY_REASON_CODES = frozenset({
    "PACKAGE_REMOVED", "DEPENDENCY_CHANGED", "NAMESPACE_OWNERSHIP_CHANGED",
    "ENTRY_REMOVED", "ENTRY_KIND_CHANGED", "ENTRY_SEMANTICS_CHANGED",
    "EVIDENCE_MISSING", "ACCEPTED_DEPENDENCY_INVALIDATED",
})
REQUIRED_VALIDATOR_IDS = frozenset({
    "character_seed_closure", "health_effect_recovery_closure",
    "domain_rules_coverage_closure", "house_rules_boundary_closure",
})


class RulesetContractError(ValueError):
    def __init__(self, reason: str, detail: str):
        if reason not in LOAD_FAILURE_REASONS:
            raise ValueError(f"unknown ruleset failure reason: {reason}")
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason}: {detail}")


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise RulesetContractError("invalid_manifest", f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json_bytes(raw: bytes, *, failure_reason: str = "content_mismatch") -> Any:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_object)
    except RulesetContractError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RulesetContractError(failure_reason, f"invalid UTF-8 JSON: {exc}") from exc


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise RulesetContractError("content_mismatch", f"non-canonical JSON value: {exc}") from exc


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _valid_digest(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def _require_exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        actual = sorted(value) if isinstance(value, dict) else type(value).__name__
        raise RulesetContractError("invalid_manifest", f"{label} keys {actual!r}; expected {sorted(expected)!r}")
    return value


def _valid_id(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and value[0].isalpha() and all(ch.isalnum() or ch in "_.:-" for ch in value)


def _normalize_member_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise RulesetContractError("invalid_manifest", f"invalid content path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or path.as_posix() != value:
        raise RulesetContractError("invalid_manifest", f"non-normalized content path: {value!r}")
    return value


def validate_manifest(value: Any, *, engine_version: str, catalog_generation: int) -> dict[str, Any]:
    expected = {
        "manifest_schema_version", "package_id", "package_revision",
        "compatibility_family", "compatibility_generation", "engine_requirement",
        "catalog_generation", "owned_namespaces", "dependencies", "content_files",
    }
    manifest = _require_exact_keys(value, expected, "manifest")
    if manifest["manifest_schema_version"] != 2:
        raise RulesetContractError("invalid_manifest", "unsupported manifest_schema_version")
    for key in ("package_id", "compatibility_family"):
        if not _valid_id(manifest[key]):
            raise RulesetContractError("invalid_manifest", f"invalid {key}")
    if not isinstance(manifest["package_revision"], int) or isinstance(manifest["package_revision"], bool) or manifest["package_revision"] < 1:
        raise RulesetContractError("invalid_manifest", "invalid package_revision")
    if not isinstance(manifest["compatibility_generation"], int) or isinstance(manifest["compatibility_generation"], bool) or manifest["compatibility_generation"] < 1:
        raise RulesetContractError("invalid_manifest", "invalid compatibility_generation")
    req = _require_exact_keys(manifest["engine_requirement"], {"engine_version"}, "engine_requirement")
    if req["engine_version"] != engine_version:
        raise RulesetContractError("engine_incompatibility", f"requires {req['engine_version']!r}, engine is {engine_version!r}")
    if not isinstance(catalog_generation, int) or isinstance(catalog_generation, bool):
        raise RulesetContractError("catalog_incompatibility", "caller catalog_generation must be integer")
    if manifest["catalog_generation"] != catalog_generation:
        raise RulesetContractError("catalog_incompatibility", "catalog_generation mismatch")
    claims = manifest["owned_namespaces"]
    if not isinstance(claims, list) or not claims or len(claims) != len(set(claims)) or any(not isinstance(x, str) or not x.endswith(".*") for x in claims):
        raise RulesetContractError("invalid_manifest", "owned_namespaces must be unique prefix.* strings")
    dependencies = manifest["dependencies"]
    if not isinstance(dependencies, list):
        raise RulesetContractError("invalid_manifest", "dependencies must be an array")
    seen_dep: set[str] = set()
    for dep in dependencies:
        dep = _require_exact_keys(dep, {"package_id", "content_sha256"}, "dependency")
        if not _valid_id(dep["package_id"]) or not _valid_digest(dep["content_sha256"]):
            raise RulesetContractError("invalid_manifest", "invalid dependency identity")
        if dep["package_id"] in seen_dep:
            raise RulesetContractError("ambiguous_dependency", f"duplicate dependency {dep['package_id']}")
        seen_dep.add(dep["package_id"])
    members = manifest["content_files"]
    if not isinstance(members, list) or not members:
        raise RulesetContractError("invalid_manifest", "content_files must be nonempty")
    normalized = [_normalize_member_path(x) for x in members]
    if len(normalized) != len(set(normalized)):
        raise RulesetContractError("invalid_manifest", "duplicate content file")
    if len(normalized) != len({item.casefold() for item in normalized}):
        raise RulesetContractError("invalid_manifest", "case-fold-colliding content file")
    if MANIFEST_NAME not in normalized:
        raise RulesetContractError("invalid_manifest", "manifest must include itself in content_files")
    forbidden = {"content_sha256", "content_set_sha256", "sha256", "package_version", "compatibility_id"}
    if forbidden.intersection(manifest):
        raise RulesetContractError("invalid_manifest", "manifest may not carry obsolete or snapshot/member digest authority")
    return manifest


@dataclass(frozen=True)
class PackageSnapshot:
    package_dir: Path
    manifest: dict[str, Any]
    content_sha256: str
    members: tuple[dict[str, str], ...]
    semantic_entries: dict[str, dict[str, str]]


def _entry_hash(value: Any) -> str:
    return sha256(ENTRY_DOMAIN + canonical_json(value))


def _stable_row_key(row: dict[str, Any], index: int) -> str | None:
    del index
    for key in ("id", "policy_id", "transition_id", "route_id", "edge_key", "key", "name"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return f"{key}:{value}"
    return None


def semantic_entries(package_id: str, path: str, value: Any) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    if path == "character-capabilities.json" and isinstance(value, dict):
        for field, item in sorted(value.items()):
            if isinstance(item, list):
                for element in item:
                    key = f"{package_id}|capability|{field}|{canonical_json(element).decode('utf-8')}"
                    entries[key] = {"kind": f"capability.{field}", "semantic_sha256": _entry_hash(element)}
            elif isinstance(item, dict):
                for subkey, subvalue in sorted(item.items()):
                    key = f"{package_id}|capability|{field}|{subkey}"
                    entries[key] = {"kind": f"capability.{field}", "semantic_sha256": _entry_hash(subvalue)}
            else:
                key = f"{package_id}|capability|{field}"
                entries[key] = {"kind": f"capability.{field}", "semantic_sha256": _entry_hash(item)}
        return entries
    if not isinstance(value, dict):
        key = f"{package_id}|file|{path}"
        return {key: {"kind": "file", "semantic_sha256": _entry_hash(value)}}
    for collection, content in sorted(value.items()):
        if isinstance(content, list):
            stable = True
            staged: list[tuple[str, Any]] = []
            for index, row in enumerate(content):
                if not isinstance(row, dict):
                    stable = False
                    break
                row_key = _stable_row_key(row, index)
                if row_key is None:
                    stable = False
                    break
                staged.append((row_key, row))
            if stable:
                for row_key, row in staged:
                    kind = row.get("kind", collection)
                    key = f"{package_id}|{collection}|{row_key}"
                    if key in entries:
                        raise RulesetContractError("unreconstructable_context", f"duplicate semantic entry {key}")
                    entries[key] = {"kind": str(kind), "semantic_sha256": _entry_hash(row)}
            else:
                key = f"{package_id}|collection|{path}|{collection}"
                entries[key] = {"kind": f"collection.{collection}", "semantic_sha256": _entry_hash(content)}
        else:
            key = f"{package_id}|field|{path}|{collection}"
            entries[key] = {"kind": f"field.{collection}", "semantic_sha256": _entry_hash(content)}
    return entries


def build_snapshot(package_dir: Path, *, engine_version: str, catalog_generation: int) -> PackageSnapshot:
    package_dir = Path(package_dir).resolve()
    manifest_path = package_dir / MANIFEST_NAME
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise RulesetContractError("invalid_manifest", f"missing or symlink manifest: {manifest_path}")
    manifest_raw = manifest_path.read_bytes()
    manifest = validate_manifest(
        load_json_bytes(manifest_raw, failure_reason="invalid_manifest"),
        engine_version=engine_version,
        catalog_generation=catalog_generation,
    )
    members: list[dict[str, str]] = []
    entries: dict[str, dict[str, str]] = {}
    for rel in sorted(manifest["content_files"]):
        target = package_dir / PurePosixPath(rel)
        if not target.is_file() or target.is_symlink() or package_dir not in target.resolve().parents:
            raise RulesetContractError("content_mismatch", f"missing, escaping or symlink content member: {rel}")
        raw = target.read_bytes()
        members.append({"path": rel, "sha256": sha256(raw)})
        if rel != MANIFEST_NAME and rel.endswith(".json"):
            payload = load_json_bytes(raw)
            for key, item in semantic_entries(manifest["package_id"], rel, payload).items():
                if key in entries:
                    raise RulesetContractError("unreconstructable_context", f"duplicate semantic key: {key}")
                entries[key] = item
    digest = sha256(PACKAGE_DOMAIN + canonical_json({"content_files": members}))
    return PackageSnapshot(package_dir, manifest, digest, tuple(members), entries)


def _detect_cycle(graph: dict[str, list[str]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise RulesetContractError("dependency_cycle", f"cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)


def build_resolved_lock(
    package_dirs: Iterable[Path], *, root_package_ids: Iterable[str],
    engine_version: str, catalog_generation: int,
) -> tuple[dict[str, Any], dict[str, PackageSnapshot]]:
    snapshots: dict[str, PackageSnapshot] = {}
    for package_dir in package_dirs:
        snap = build_snapshot(package_dir, engine_version=engine_version, catalog_generation=catalog_generation)
        package_id = snap.manifest["package_id"]
        if package_id in snapshots:
            raise RulesetContractError("package_id_ambiguity", f"duplicate package_id {package_id}")
        snapshots[package_id] = snap
    roots = sorted(set(root_package_ids))
    if not roots or any(root not in snapshots for root in roots):
        raise RulesetContractError("missing_dependency", "root package missing")
    graph: dict[str, list[str]] = {}
    for package_id, snap in snapshots.items():
        graph[package_id] = []
        for dep in snap.manifest["dependencies"]:
            target = snapshots.get(dep["package_id"])
            if target is None:
                raise RulesetContractError("missing_dependency", dep["package_id"])
            if target.content_sha256 != dep["content_sha256"]:
                raise RulesetContractError("missing_dependency", f"wrong snapshot for {dep['package_id']}")
            graph[package_id].append(dep["package_id"])
    _detect_cycle(graph)
    closure: set[str] = set()
    pending = list(roots)
    while pending:
        node = pending.pop()
        if node in closure:
            continue
        closure.add(node)
        pending.extend(graph[node])
    if closure != set(snapshots):
        raise RulesetContractError("ambiguous_dependency", "explicit package roots include unreachable snapshots")
    claims: dict[str, str] = {}
    definition_ids: dict[str, str] = {}
    for package_id in sorted(closure):
        snap = snapshots[package_id]
        for claim in snap.manifest["owned_namespaces"]:
            owner = claims.get(claim)
            if owner is not None and owner != package_id:
                raise RulesetContractError("namespace_conflict", f"{claim}: {owner} vs {package_id}")
            claims[claim] = package_id
        for key in snap.semantic_entries:
            parts = key.split("|")
            if len(parts) >= 3 and parts[1] not in ("capability", "field", "collection", "file"):
                semantic_id = parts[-1].split(":", 1)[-1]
                prior = definition_ids.get(semantic_id)
                if prior is not None and prior != package_id:
                    raise RulesetContractError("namespace_conflict", f"duplicate definition {semantic_id}")
                definition_ids[semantic_id] = package_id
                if "." in semantic_id:
                    namespace_claim = semantic_id.split(".", 1)[0] + ".*"
                    if namespace_claim not in snap.manifest["owned_namespaces"]:
                        raise RulesetContractError("namespace_conflict", f"{semantic_id} is not covered by a namespace owned by {package_id}")
    packages: list[dict[str, Any]] = []
    for package_id in sorted(closure):
        snap = snapshots[package_id]
        packages.append({
            "package_id": package_id,
            "package_revision": snap.manifest["package_revision"],
            "compatibility_family": snap.manifest["compatibility_family"],
            "compatibility_generation": snap.manifest["compatibility_generation"],
            "content_sha256": snap.content_sha256,
            "catalog_generation": snap.manifest["catalog_generation"],
            "owned_namespaces": sorted(snap.manifest["owned_namespaces"]),
            "dependencies": sorted(snap.manifest["dependencies"], key=lambda row: row["package_id"]),
            "members": list(snap.members),
        })
    core = {
        "lock_schema_version": 2,
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "root_package_ids": roots,
        "packages": packages,
    }
    lock = dict(core)
    lock["ruleset_set_sha256"] = sha256(SET_DOMAIN + canonical_json(core))
    return lock, snapshots


def validate_resolved_lock(value: Any) -> dict[str, Any]:
    expected = {"lock_schema_version", "ruleset_set_digest_generation", "root_package_ids", "packages", "ruleset_set_sha256"}
    lock = _require_exact_keys(value, expected, "resolved ruleset lock")
    if lock["lock_schema_version"] != 2 or lock["ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION:
        raise RulesetContractError("resolved_set_mismatch", "unsupported ruleset lock/digest generation")
    if not isinstance(lock["root_package_ids"], list) or not isinstance(lock["packages"], list):
        raise RulesetContractError("resolved_set_mismatch", "invalid resolved ruleset lock collections")
    for row in lock["packages"]:
        row = _require_exact_keys(row, {
            "package_id", "package_revision", "compatibility_family", "compatibility_generation",
            "content_sha256", "catalog_generation", "owned_namespaces", "dependencies", "members",
        }, "resolved package row")
        if not _valid_id(row["package_id"]) or not _valid_id(row["compatibility_family"]):
            raise RulesetContractError("resolved_set_mismatch", "invalid resolved package identity")
        if not isinstance(row["package_revision"], int) or isinstance(row["package_revision"], bool) or row["package_revision"] < 1:
            raise RulesetContractError("resolved_set_mismatch", "invalid package_revision")
        if not isinstance(row["compatibility_generation"], int) or isinstance(row["compatibility_generation"], bool) or row["compatibility_generation"] < 1:
            raise RulesetContractError("resolved_set_mismatch", "invalid compatibility_generation")
        if not isinstance(row["catalog_generation"], int) or isinstance(row["catalog_generation"], bool) or row["catalog_generation"] < 1:
            raise RulesetContractError("resolved_set_mismatch", "invalid catalog_generation")
        if not _valid_digest(row["content_sha256"]):
            raise RulesetContractError("resolved_set_mismatch", "invalid content_sha256")
    core = {key: lock[key] for key in ("lock_schema_version", "ruleset_set_digest_generation", "root_package_ids", "packages")}
    expected_digest = sha256(SET_DOMAIN + canonical_json(core))
    if not _valid_digest(lock["ruleset_set_sha256"]) or lock["ruleset_set_sha256"] != expected_digest:
        raise RulesetContractError("resolved_set_mismatch", "ruleset set digest mismatch")
    return lock


def _validated_engine_contract_entries(
    inventory: dict[str, Any], *, engine_version: str, ruleset_set_sha256: str,
    ruleset_set_digest_generation: int = RULESET_SET_DIGEST_GENERATION,
) -> dict[str, dict[str, str]]:
    if not isinstance(inventory, dict) or set(inventory) != {
        "inventory_schema_version", "engine_version", "ruleset_set_digest_generation",
        "ruleset_set_sha256", "items", "inventory_sha256",
    }:
        raise RulesetContractError("unreconstructable_context", "invalid engine contract inventory shape")
    items = inventory["items"]
    if (
        inventory["inventory_schema_version"] != 2
        or inventory["engine_version"] != engine_version
        or inventory["ruleset_set_digest_generation"] != ruleset_set_digest_generation
        or inventory["ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION
        or inventory["ruleset_set_sha256"] != ruleset_set_sha256
        or not isinstance(items, list)
    ):
        raise RulesetContractError("unreconstructable_context", "stale engine contract inventory")
    sources = {row.get("family"): row for row in items if isinstance(row, dict)}
    if len(sources) != len(items) or set(sources) != REQUIRED_ENGINE_CONTRACT_FAMILIES:
        raise RulesetContractError("unreconstructable_context", "engine contract families differ")
    entries: dict[str, dict[str, str]] = {}
    for family, row in sorted(sources.items()):
        if set(row) != {"family", "contract_id", "semantic_sha256"}:
            raise RulesetContractError("unreconstructable_context", f"invalid {family} contract evidence")
        digest = row["semantic_sha256"]
        if row["contract_id"] != f"engine_contract.{family}.v1" or not _valid_digest(digest):
            raise RulesetContractError("unreconstructable_context", f"stale {family} contract evidence")
        entries[row["contract_id"]] = {"kind": f"engine_contract.{family}", "semantic_sha256": digest}
    core = {key: inventory[key] for key in (
        "inventory_schema_version", "engine_version", "ruleset_set_digest_generation", "ruleset_set_sha256", "items"
    )}
    if not _valid_digest(inventory["inventory_sha256"]) or inventory["inventory_sha256"] != sha256(INVENTORY_DOMAIN + canonical_json(core)):
        raise RulesetContractError("unreconstructable_context", "engine contract inventory digest mismatch")
    return entries


def compare_resolved_sets(
    adopted_lock: dict[str, Any], adopted_snapshots: dict[str, PackageSnapshot],
    adopted_engine_contract_inventory: dict[str, Any], candidate_lock: dict[str, Any],
    candidate_snapshots: dict[str, PackageSnapshot], candidate_engine_contract_inventory: dict[str, Any],
    *, engine_version: str, dependency_frontier: dict[str, Any],
) -> dict[str, Any]:
    validate_resolved_lock(adopted_lock)
    validate_resolved_lock(candidate_lock)
    reasons: list[dict[str, str]] = []
    try:
        adopted_engine_entries = _validated_engine_contract_entries(
            adopted_engine_contract_inventory, engine_version=engine_version,
            ruleset_set_sha256=adopted_lock["ruleset_set_sha256"],
            ruleset_set_digest_generation=adopted_lock["ruleset_set_digest_generation"],
        )
    except (RulesetContractError, TypeError):
        adopted_engine_entries = {}
        reasons.append({"code":"EVIDENCE_MISSING","key":"adopted.engine_contract_families","detail":"adopted closed engine-contract inventory is incomplete"})
    try:
        candidate_engine_entries = _validated_engine_contract_entries(
            candidate_engine_contract_inventory, engine_version=engine_version,
            ruleset_set_sha256=candidate_lock["ruleset_set_sha256"],
            ruleset_set_digest_generation=candidate_lock["ruleset_set_digest_generation"],
        )
    except (RulesetContractError, TypeError):
        candidate_engine_entries = {}
        reasons.append({"code":"EVIDENCE_MISSING","key":"candidate.engine_contract_families","detail":"candidate closed engine-contract inventory is incomplete"})
    if reasons:
        adopted_engine_entries = {}
        candidate_engine_entries = {}
    adopted_entries = combined_semantic_entries(adopted_snapshots, adopted_engine_entries)
    candidate_entries = combined_semantic_entries(candidate_snapshots, candidate_engine_entries)
    frontier_valid = False
    if isinstance(dependency_frontier, dict) and set(dependency_frontier) == {"owner", "state_revision", "required_entry_keys"}:
        required_keys = dependency_frontier["required_entry_keys"]
        frontier_valid = (
            isinstance(dependency_frontier["owner"], str)
            and isinstance(dependency_frontier["state_revision"], int)
            and not isinstance(dependency_frontier["state_revision"], bool)
            and isinstance(required_keys, list)
            and len(required_keys) == len(set(required_keys))
            and all(isinstance(key, str) and key for key in required_keys)
        )
    else:
        required_keys = []
    if not frontier_valid:
        reasons.append({"code":"EVIDENCE_MISSING","key":"campaign.dependency_frontier","detail":"durable-state and accepted-work dependency frontier is incomplete"})
    evidence = {"adopted": adopted_entries, "candidate": candidate_entries, "dependency_frontier": dependency_frontier}
    evidence_digest = sha256(EVIDENCE_DOMAIN + canonical_json(evidence))
    adopted_packages = {row["package_id"]: row for row in adopted_lock.get("packages", [])}
    candidate_packages = {row["package_id"]: row for row in candidate_lock.get("packages", [])}
    for package_id, old in sorted(adopted_packages.items()):
        new = candidate_packages.get(package_id)
        if new is None:
            reasons.append({"code": "PACKAGE_REMOVED", "key": package_id, "detail": "adopted package absent from candidate"})
            continue
        if (
            old.get("compatibility_family") != new.get("compatibility_family")
            or old.get("compatibility_generation") != new.get("compatibility_generation")
            or old.get("catalog_generation") != new.get("catalog_generation")
        ):
            reasons.append({"code": "DEPENDENCY_CHANGED", "key": package_id, "detail": "compatibility/catalog line changed"})
        if old.get("owned_namespaces") != new.get("owned_namespaces"):
            reasons.append({"code": "NAMESPACE_OWNERSHIP_CHANGED", "key": package_id, "detail": "owned namespace claims changed"})
        old_dependencies = {(row.get("package_id"), row.get("content_sha256")) for row in old.get("dependencies", [])}
        new_dependencies = {(row.get("package_id"), row.get("content_sha256")) for row in new.get("dependencies", [])}
        if not old_dependencies.issubset(new_dependencies):
            reasons.append({"code": "DEPENDENCY_CHANGED", "key": package_id, "detail": "an adopted exact dependency was removed or replaced"})
    for key, old in sorted(adopted_entries.items()):
        new = candidate_entries.get(key)
        if new is None:
            reasons.append({"code": "ENTRY_REMOVED", "key": key, "detail": "adopted semantic/active-contract entry absent"})
        elif old.get("kind") != new.get("kind"):
            reasons.append({"code": "ENTRY_KIND_CHANGED", "key": key, "detail": "existing entry kind changed"})
        elif old.get("semantic_sha256") != new.get("semantic_sha256"):
            reasons.append({"code": "ENTRY_SEMANTICS_CHANGED", "key": key, "detail": "existing entry canonical semantics changed"})
    for key in required_keys:
        if key not in adopted_entries:
            reasons.append({"code": "EVIDENCE_MISSING", "key": key, "detail": "durable owner named an entry absent from the adopted evidence"})
        elif key not in candidate_entries:
            reasons.append({"code": "ACCEPTED_DEPENDENCY_INVALIDATED", "key": key, "detail": "candidate omits durable-state or accepted-work dependency"})
    if reasons:
        result = "BLOCKED_INSUFFICIENT_EVIDENCE" if all(row["code"] == "EVIDENCE_MISSING" for row in reasons) else "BLOCKED_INCOMPATIBLE"
    else:
        result = "COMPATIBLE_ADDITIVE"
    result_row = {
        "comparison_schema_version": 2,
        "adopted_ruleset_set_digest_generation": adopted_lock["ruleset_set_digest_generation"],
        "adopted_ruleset_set_sha256": adopted_lock["ruleset_set_sha256"],
        "candidate_ruleset_set_digest_generation": candidate_lock["ruleset_set_digest_generation"],
        "candidate_ruleset_set_sha256": candidate_lock["ruleset_set_sha256"],
        "evidence_inventory_sha256": evidence_digest,
        "result": result,
        "reasons": reasons,
    }
    validate_compatibility_result(result_row)
    return result_row


def validate_compatibility_result(value: Any) -> None:
    expected = {
        "comparison_schema_version", "adopted_ruleset_set_digest_generation", "adopted_ruleset_set_sha256",
        "candidate_ruleset_set_digest_generation", "candidate_ruleset_set_sha256",
        "evidence_inventory_sha256", "result", "reasons",
    }
    if not isinstance(value, dict) or set(value) != expected or value["comparison_schema_version"] != 2:
        raise RulesetContractError("unreconstructable_context", "invalid compatibility result shape")
    if value["adopted_ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION or value["candidate_ruleset_set_digest_generation"] != RULESET_SET_DIGEST_GENERATION:
        raise RulesetContractError("unreconstructable_context", "unsupported ruleset set digest generation")
    for field in ("adopted_ruleset_set_sha256", "candidate_ruleset_set_sha256", "evidence_inventory_sha256"):
        if not _valid_digest(value[field]):
            raise RulesetContractError("unreconstructable_context", f"invalid compatibility digest: {field}")
    reasons = value["reasons"]
    if not isinstance(reasons, list) or any(
        not isinstance(row, dict) or set(row) != {"code", "key", "detail"}
        or row["code"] not in COMPATIBILITY_REASON_CODES
        or not isinstance(row["key"], str) or not row["key"]
        or not isinstance(row["detail"], str) or not row["detail"]
        for row in reasons
    ):
        raise RulesetContractError("unreconstructable_context", "invalid compatibility reason")
    result = value["result"]
    if result == "COMPATIBLE_ADDITIVE":
        valid = not reasons
    elif result == "BLOCKED_INSUFFICIENT_EVIDENCE":
        valid = bool(reasons) and all(row["code"] == "EVIDENCE_MISSING" for row in reasons)
    elif result == "BLOCKED_INCOMPATIBLE":
        valid = bool(reasons) and any(row["code"] != "EVIDENCE_MISSING" for row in reasons)
    else:
        valid = False
    if not valid:
        raise RulesetContractError("unreconstructable_context", "compatibility result/reasons mismatch")


def compile_conformance_attestation(
    inventory: dict[str, Any], validator_results: list[dict[str, str]], *,
    lock: dict[str, Any], engine_version: str,
) -> dict[str, Any]:
    validate_resolved_lock(lock)
    _validated_engine_contract_entries(
        inventory, engine_version=engine_version,
        ruleset_set_sha256=lock["ruleset_set_sha256"],
        ruleset_set_digest_generation=lock["ruleset_set_digest_generation"],
    )
    observed = {row.get("validator_id") for row in validator_results if isinstance(row, dict)}
    if (
        len(validator_results) != len(REQUIRED_VALIDATOR_IDS)
        or observed != REQUIRED_VALIDATOR_IDS
        or any(set(row) != {"validator_id", "result"} or row["result"] != "PASS" for row in validator_results)
    ):
        raise RulesetContractError("unreconstructable_context", "integrated validator results incomplete")
    core = {
        "attestation_schema_version": 2,
        "validator_suite_id": "ruleset.integrated_closure.v1",
        "engine_version": engine_version,
        "ruleset_set_digest_generation": lock["ruleset_set_digest_generation"],
        "ruleset_set_sha256": lock["ruleset_set_sha256"],
        "engine_contract_inventory_sha256": inventory["inventory_sha256"],
        "validator_results": sorted(validator_results, key=lambda row: row["validator_id"]),
    }
    result = dict(core)
    result["attestation_sha256"] = sha256(ATTESTATION_DOMAIN + canonical_json(core))
    return result


def validate_runtime_conformance_evidence(
    inventory: dict[str, Any], attestation: dict[str, Any], *,
    lock: dict[str, Any], engine_version: str,
) -> None:
    validate_resolved_lock(lock)
    _validated_engine_contract_entries(
        inventory, engine_version=engine_version,
        ruleset_set_sha256=lock["ruleset_set_sha256"],
        ruleset_set_digest_generation=lock["ruleset_set_digest_generation"],
    )
    if not isinstance(attestation, dict) or set(attestation) != {
        "attestation_schema_version", "validator_suite_id", "engine_version",
        "ruleset_set_digest_generation", "ruleset_set_sha256", "engine_contract_inventory_sha256",
        "validator_results", "attestation_sha256",
    }:
        raise RulesetContractError("unreconstructable_context", "invalid conformance attestation shape")
    expected = compile_conformance_attestation(
        inventory, attestation["validator_results"], lock=lock, engine_version=engine_version
    )
    if attestation != expected:
        raise RulesetContractError("unreconstructable_context", "conformance attestation binding mismatch")


def combined_semantic_entries(
    snapshots: dict[str, PackageSnapshot],
    active_contract_entries: dict[str, dict[str, str]] | None = None,
) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for package_id in sorted(snapshots):
        for key, value in snapshots[package_id].semantic_entries.items():
            if key in out:
                raise RulesetContractError("unreconstructable_context", f"duplicate combined entry {key}")
            out[key] = value
    for key, value in sorted((active_contract_entries or {}).items()):
        full_key = f"ENGINE_ACTIVE_CONTRACT|{key}"
        if full_key in out:
            raise RulesetContractError("unreconstructable_context", f"duplicate active contract entry {key}")
        out[full_key] = value
    return out
