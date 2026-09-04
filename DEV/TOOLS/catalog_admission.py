"""Canonical loader/assembler for the semantically partitioned catalog-admission ledger.

`DEV/CATALOG/catalog-admission-ledger.json` was one physical monolith. It is now
physically realized as `DEV/CATALOG/catalog-admission-ledger/manifest.json` plus one
`DEV/CATALOG/catalog-admission-ledger/families/<registry_family>.json` shard per
registry family, while remaining one logical ledger contract. This module is the
single canonical assembler: consumers must call `load_catalog_admission_ledger`
rather than reading manifest/shard files directly.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

LEDGER_DIR_RELATIVE = "DEV/CATALOG/catalog-admission-ledger"
MANIFEST_RELATIVE = f"{LEDGER_DIR_RELATIVE}/manifest.json"
FAMILIES_DIR_RELATIVE = f"{LEDGER_DIR_RELATIVE}/families"
CORE_CATALOG_RELATIVE = "DEV/CATALOG/core-catalog.json"

MANIFEST_KEYS = {
    "schema_name", "schema_version", "catalog_generation", "source_registry",
    "decision_owner", "laws", "ruleset_package_admission", "retired_reference_audit",
    "family_shards",
}
FAMILY_SHARD_KEYS = {"registry_family", "registry_census", "family_policy", "entries"}
CENSUS_ARITHMETIC_FIELDS = ("admitted", "embedded_nonowner", "dormant_nonselectable", "stale_remove")
DISPOSITION_TO_CENSUS_FIELD = {
    "ACTIVE_ADMITTED": "admitted",
    "EMBEDDED_NONOWNER": "embedded_nonowner",
    "DORMANT_NONSELECTABLE": "dormant_nonselectable",
    "STALE_REMOVE": "stale_remove",
}


class CatalogAdmissionLedgerError(ValueError):
    """Raised when the physical manifest/shard set cannot be assembled fail-closed."""


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_catalog_admission_ledger(repo_root: Path) -> dict[str, Any]:
    """Load the manifest and every declared family shard and assemble the logical ledger.

    The returned object has the same shape as the retired
    `DEV/CATALOG/catalog-admission-ledger.json` monolith: the same top-level keys,
    with `registry_census` (list), `family_policies` (dict) and `entries` (list)
    reconstructed from the family shards. `entries` order is grouped by family in
    manifest order; the original monolith interleaved entries across families, so
    ordering is not itself semantic and callers must not rely on it.
    """
    repo_root = Path(repo_root).resolve()
    manifest_path = repo_root / MANIFEST_RELATIVE
    if not manifest_path.is_file():
        raise CatalogAdmissionLedgerError(f"missing catalog-admission-ledger manifest: {manifest_path}")
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        raise CatalogAdmissionLedgerError("catalog-admission-ledger manifest keys are not exact")

    family_shards = manifest["family_shards"]
    if not isinstance(family_shards, list) or not family_shards or not all(isinstance(f, str) and f for f in family_shards):
        raise CatalogAdmissionLedgerError("manifest family_shards must be a non-empty ordered list of family names")
    if len(set(family_shards)) != len(family_shards):
        raise CatalogAdmissionLedgerError("manifest declares a duplicate family shard")

    families_dir = repo_root / FAMILIES_DIR_RELATIVE
    declared_files = {f"{family}.json" for family in family_shards}
    actual_files = {p.name for p in families_dir.glob("*.json")} if families_dir.is_dir() else set()
    missing = declared_files - actual_files
    if missing:
        raise CatalogAdmissionLedgerError(f"missing declared family shard file(s): {sorted(missing)}")
    undeclared = actual_files - declared_files
    if undeclared:
        raise CatalogAdmissionLedgerError(f"undeclared family shard file(s) present: {sorted(undeclared)}")

    registry_census: list[dict[str, Any]] = []
    family_policies: dict[str, Any] = {}
    entries: list[dict[str, Any]] = []
    seen_ids: set[tuple[str, str]] = set()

    for family in family_shards:
        shard_path = families_dir / f"{family}.json"
        shard = _load_json(shard_path)
        if not isinstance(shard, dict) or set(shard) != FAMILY_SHARD_KEYS:
            raise CatalogAdmissionLedgerError(f"family shard keys are not exact: {shard_path}")
        if shard["registry_family"] != family:
            raise CatalogAdmissionLedgerError(
                f"shard file name does not match its declared registry_family: {shard_path}"
            )
        census = shard["registry_census"]
        if not isinstance(census, dict) or census.get("registry_family") != family:
            raise CatalogAdmissionLedgerError(f"census registry_family mismatch in {shard_path}")

        shard_entries = shard["entries"]
        if not isinstance(shard_entries, list):
            raise CatalogAdmissionLedgerError(f"entries must be a list in {shard_path}")
        disposition_counts = {field: 0 for field in CENSUS_ARITHMETIC_FIELDS}
        for entry in shard_entries:
            family_of_entry = entry.get("registry_family")
            if family_of_entry != family:
                raise CatalogAdmissionLedgerError(
                    f"entry {entry.get('id')!r} declares registry_family {family_of_entry!r} "
                    f"but is contained in shard {family!r}"
                )
            key = (family_of_entry, entry.get("id"))
            if key in seen_ids:
                raise CatalogAdmissionLedgerError(f"duplicate entry ID across shards: {key}")
            seen_ids.add(key)
            census_field = DISPOSITION_TO_CENSUS_FIELD.get(entry.get("admission_disposition"))
            if census_field is not None:
                disposition_counts[census_field] += 1
            entries.append(entry)

        if census.get("count") != len(shard_entries):
            raise CatalogAdmissionLedgerError(f"census count mismatch for family {family!r}")
        for field in CENSUS_ARITHMETIC_FIELDS:
            if census.get(field) != disposition_counts[field]:
                raise CatalogAdmissionLedgerError(f"census {field!r} mismatch for family {family!r}")

        registry_census.append(census)
        family_policies[family] = shard["family_policy"]

    core_catalog_path = repo_root / CORE_CATALOG_RELATIVE
    if not core_catalog_path.is_file():
        raise CatalogAdmissionLedgerError(f"missing source registry: {core_catalog_path}")
    core_catalog = _load_json(core_catalog_path)
    core_families = set(core_catalog.get("registries", {}))
    if core_families != set(family_shards):
        raise CatalogAdmissionLedgerError(
            "family shard inventory does not match DEV/CATALOG/core-catalog.json registries"
        )

    ledger = {key: value for key, value in manifest.items() if key != "family_shards"}
    ledger["registry_census"] = registry_census
    ledger["family_policies"] = family_policies
    ledger["entries"] = entries
    return ledger
