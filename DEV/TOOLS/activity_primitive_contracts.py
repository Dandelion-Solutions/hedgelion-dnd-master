"""Canonical loader/assembler for the semantically partitioned Activity primitive contracts.

`DEV/CATALOG/activity-primitive-contracts.json` was one physical monolith. It is now
physically realized as `DEV/CATALOG/activity-primitive-contracts/manifest.json` plus
`DEV/CATALOG/activity-primitive-contracts/shared/value_contracts.json`,
`DEV/CATALOG/activity-primitive-contracts/shared/read_contracts.json` and one
`DEV/CATALOG/activity-primitive-contracts/primitives/<primitive_id>.json` shard per
registered `op.*` primitive (`contracts[primitive_id]` and
`primitive_validation_matrix[primitive_id]` colocated as one semantic unit), while
remaining one logical Activity primitive contract. This module is the single
canonical assembler: consumers must call `load_activity_primitive_contracts` rather
than reading manifest/shard files directly.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TOPOLOGY_DIR_RELATIVE = "DEV/CATALOG/activity-primitive-contracts"
MANIFEST_RELATIVE = f"{TOPOLOGY_DIR_RELATIVE}/manifest.json"
VALUE_CONTRACTS_RELATIVE = f"{TOPOLOGY_DIR_RELATIVE}/shared/value_contracts.json"
READ_CONTRACTS_RELATIVE = f"{TOPOLOGY_DIR_RELATIVE}/shared/read_contracts.json"
PRIMITIVES_DIR_RELATIVE = f"{TOPOLOGY_DIR_RELATIVE}/primitives"
CORE_CATALOG_RELATIVE = "DEV/CATALOG/core-catalog.json"

MANIFEST_KEYS = {"schema_name", "schema_version", "catalog_generation", "owner", "laws", "primitive_shards"}
PRIMITIVE_SHARD_KEYS = {"primitive_id", "contract", "validation_matrix"}


class ActivityPrimitiveContractsError(ValueError):
    """Raised when the physical manifest/shard set cannot be assembled fail-closed."""


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_activity_primitive_contracts(repo_root: Path) -> dict[str, Any]:
    """Load the manifest, shared vocabularies and every declared primitive shard and
    assemble the logical Activity primitive contract.

    The returned object has the same shape as the retired
    `DEV/CATALOG/activity-primitive-contracts.json` monolith: the same top-level
    keys, with `contracts` (list, in exact manifest-declared order) and
    `primitive_validation_matrix` (dict) reconstructed from the primitive shards.
    Manifest-declared order reproduces the original monolith's `contracts` array
    order exactly, because array order is semantic for the S6D-11 engine-contract
    hash; callers must not reorder it.
    """
    repo_root = Path(repo_root).resolve()
    manifest_path = repo_root / MANIFEST_RELATIVE
    if not manifest_path.is_file():
        raise ActivityPrimitiveContractsError(f"missing activity-primitive-contracts manifest: {manifest_path}")
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        raise ActivityPrimitiveContractsError("activity-primitive-contracts manifest keys are not exact")

    primitive_shards = manifest["primitive_shards"]
    if not isinstance(primitive_shards, list) or not primitive_shards or not all(
        isinstance(p, str) and p for p in primitive_shards
    ):
        raise ActivityPrimitiveContractsError("manifest primitive_shards must be a non-empty ordered list of primitive IDs")
    if len(set(primitive_shards)) != len(primitive_shards):
        raise ActivityPrimitiveContractsError("manifest declares a duplicate primitive shard")

    primitives_dir = repo_root / PRIMITIVES_DIR_RELATIVE
    declared_files = {f"{pid}.json" for pid in primitive_shards}
    actual_files = {p.name for p in primitives_dir.glob("*.json")} if primitives_dir.is_dir() else set()
    missing = declared_files - actual_files
    if missing:
        raise ActivityPrimitiveContractsError(f"missing declared primitive shard file(s): {sorted(missing)}")
    undeclared = actual_files - declared_files
    if undeclared:
        raise ActivityPrimitiveContractsError(f"undeclared primitive shard file(s) present: {sorted(undeclared)}")

    value_contracts_path = repo_root / VALUE_CONTRACTS_RELATIVE
    read_contracts_path = repo_root / READ_CONTRACTS_RELATIVE
    if not value_contracts_path.is_file():
        raise ActivityPrimitiveContractsError(f"missing shared value contracts: {value_contracts_path}")
    if not read_contracts_path.is_file():
        raise ActivityPrimitiveContractsError(f"missing shared read contracts: {read_contracts_path}")
    value_contracts = _load_json(value_contracts_path)
    read_contracts = _load_json(read_contracts_path)
    if not isinstance(value_contracts, dict) or not value_contracts:
        raise ActivityPrimitiveContractsError("shared value_contracts must be a non-empty object")
    if not isinstance(read_contracts, dict) or not read_contracts:
        raise ActivityPrimitiveContractsError("shared read_contracts must be a non-empty object")

    contracts: list[dict[str, Any]] = []
    primitive_validation_matrix: dict[str, Any] = {}
    seen_ids: set[str] = set()

    for pid in primitive_shards:
        shard_path = primitives_dir / f"{pid}.json"
        shard = _load_json(shard_path)
        if not isinstance(shard, dict) or set(shard) != PRIMITIVE_SHARD_KEYS:
            raise ActivityPrimitiveContractsError(f"primitive shard keys are not exact: {shard_path}")
        if shard["primitive_id"] != pid:
            raise ActivityPrimitiveContractsError(
                f"shard file name does not match its declared primitive_id: {shard_path}"
            )
        contract = shard["contract"]
        matrix = shard["validation_matrix"]
        if not isinstance(contract, dict) or contract.get("primitive_id") != pid:
            raise ActivityPrimitiveContractsError(f"contract primitive_id mismatch in {shard_path}")
        if pid in seen_ids:
            raise ActivityPrimitiveContractsError(f"duplicate primitive identity: {pid}")
        seen_ids.add(pid)
        contracts.append(contract)
        primitive_validation_matrix[pid] = matrix

    core_catalog_path = repo_root / CORE_CATALOG_RELATIVE
    if not core_catalog_path.is_file():
        raise ActivityPrimitiveContractsError(f"missing source registry: {core_catalog_path}")
    core_catalog = _load_json(core_catalog_path)
    core_primitives = set(core_catalog.get("registries", {}).get("activity_primitives", []))
    assembled_ids = {c["primitive_id"] for c in contracts}
    if not (core_primitives == set(primitive_shards) == assembled_ids == set(primitive_validation_matrix)):
        raise ActivityPrimitiveContractsError(
            "primitive inventory mismatch across DEV/CATALOG/core-catalog.json, the "
            "manifest, assembled contracts and assembled primitive_validation_matrix"
        )

    result = {key: value for key, value in manifest.items() if key != "primitive_shards"}
    result["value_contracts"] = value_contracts
    result["read_contracts"] = read_contracts
    result["primitive_validation_matrix"] = primitive_validation_matrix
    result["contracts"] = contracts
    return result
