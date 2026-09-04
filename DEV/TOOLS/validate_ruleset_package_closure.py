#!/usr/bin/env python3
"""S6D-11 build/conformance orchestration over the shipped GAME contract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from GAME.TOOLS.ruleset_package import *  # re-export the shipped pure contract
    from GAME.TOOLS.ruleset_package import _validated_engine_contract_entries
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from GAME.TOOLS.ruleset_package import *
    from GAME.TOOLS.ruleset_package import _validated_engine_contract_entries

try:
    from DEV.TOOLS.catalog_admission import load_catalog_admission_ledger
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from catalog_admission import load_catalog_admission_ledger


# Symbolic member path for the catalog-admission-ledger engine-contract member. It is
# not read as a literal file: derive_engine_contract_inventory() recognizes this exact
# string and resolves it through the canonical loader/assembler instead, since the
# ledger is physically a manifest + per-registry-family shards, not one file.
CATALOG_ADMISSION_LEDGER_MEMBER_PATH = "DEV/CATALOG/catalog-admission-ledger.json"

ENGINE_CONTRACT_SOURCE_GROUPS = {
    "catalog_admission": (("catalog_admission_ledger", CATALOG_ADMISSION_LEDGER_MEMBER_PATH),),
    "mechanical_surface": (
        ("core_catalog","DEV/CATALOG/core-catalog.json"),
        ("mechanical_surfaces","DEV/CATALOG/mechanical-surfaces.json"),
    ),
    "primitive": (("activity_primitive_contracts","DEV/CATALOG/activity-primitive-contracts.json"),),
    "portable_value": (
        ("portable_value_contracts","DEV/CATALOG/portable-value-contracts.json"),
        ("portable_value_routes","DEV/CATALOG/portable-value-routes.json"),
    ),
    "schema_contract": (
        ("ruleset_package_manifest_schema","DEV/SCHEMAS/ruleset-package-manifest.schema.json"),
        ("resolved_ruleset_lock_schema","DEV/SCHEMAS/resolved-ruleset-lock.schema.json"),
        ("ruleset_set_compatibility_result_schema","DEV/SCHEMAS/ruleset-set-compatibility-result.schema.json"),
        ("runtime_resolution_state_schema","DEV/SCHEMAS/runtime-resolution-state.schema.json"),
        ("runtime_continuation_state_schema","DEV/SCHEMAS/runtime-continuation-state.schema.json"),
    ),
}

REGISTERED_VALIDATORS = {
    "DEV/TOOLS/validate_character_mvp_seed.py": ("character_seed_closure", "DEV/TESTS/test_s6d_07_character_mvp_seed.py"),
    "DEV/TOOLS/validate_health_effects_recovery_seed.py": ("health_effect_recovery_closure", "DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py"),
    "DEV/TOOLS/validate_domain_rules_coverage.py": ("domain_rules_coverage_closure", "DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py"),
    "DEV/TOOLS/validate_house_rules_mechanical_boundary.py": ("house_rules_boundary_closure", "DEV/TESTS/test_s6d_10_house_rules_boundary_contract.py"),
}
TRANSITIONAL_KEYS = frozenset({
    "character-capabilities.content_file",
    "character-capabilities.content_sha256",
    "character-capabilities.content_files[].sha256",
    "character-capabilities.content_set_sha256",
    "ready-pc.package_content_set_sha256",
    "s6d08.aggregate-content-set-test",
    "s6d09.package_binding.content_set_sha256",
    "s6d10.identity_bound_package_candidate.content_set_sha256",
    "runtime-package.missing-resolved-lock",
    "campaign-and-execution.missing-ruleset-set-projection",
})
CURRENT_IDENTITY_LITERAL_CARRIERS = (
    "DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py",
    "DEV/TESTS/test_s6d_11_ruleset_package_closure.py",
)


def current_identity_projection_mismatches(repo_root: Path) -> list[str]:
    """Compare current identity projections with one fresh canonical reconstruction."""
    repo_root = Path(repo_root).resolve()
    package = repo_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
    manifest = load_json_bytes((package / "ruleset-package-manifest.json").read_bytes())
    lock, snapshots = build_resolved_lock(
        [package], root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    snapshot = snapshots[manifest["package_id"]]
    package_hash = snapshot.content_sha256
    set_hash = lock["ruleset_set_sha256"]
    mismatches: list[str] = []
    closure = load_json_bytes((repo_root / "DEV/CATALOG/ruleset-package-closure.json").read_bytes())
    if closure.get("derived_current_identity") != {
        "authority": "DERIVED_NONAUTHORITATIVE_VERIFICATION_EVIDENCE",
        "package_content_sha256": package_hash, "ruleset_set_sha256": set_hash,
    }:
        mismatches.append("DEV/CATALOG/ruleset-package-closure.json")
    binding = load_json_bytes((repo_root / "DEV/CATALOG/domain-rules-coverage-binding.json").read_bytes())
    expected_binding = {
        "profile_id": "gameplay_spine.mvp.v1", "package_id": manifest["package_id"],
        "package_version": manifest["package_version"], "catalog_generation": manifest["catalog_generation"],
        "gameplay_spine_member": "gameplay-spine-seed.json", "package_content_sha256": package_hash,
        "ruleset_set_sha256": set_hash,
    }
    if binding != expected_binding or "gameplay-spine-seed.json" not in {row["path"] for row in snapshot.members}:
        mismatches.append("DEV/CATALOG/domain-rules-coverage-binding.json")
    actors = load_json_bytes((repo_root / "DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json").read_bytes())
    if any(row.get("ruleset_set_sha256") != set_hash for row in actors.get("readiness_evidence", {}).values()):
        mismatches.append("DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json")
    boundary = load_json_bytes((repo_root / "DEV/CATALOG/house-rules-mechanical-boundary.json").read_bytes())
    identity = boundary.get("resolved_ruleset_identity", {})
    if (identity.get("package_id"), identity.get("package_version"), identity.get("catalog_generation"), identity.get("ruleset_set_sha256")) != (manifest["package_id"], manifest["package_version"], manifest["catalog_generation"], set_hash):
        mismatches.append("DEV/CATALOG/house-rules-mechanical-boundary.json")
    for rel in CURRENT_IDENTITY_LITERAL_CARRIERS:
        text = (repo_root / rel).read_text(encoding="utf-8")
        if set_hash not in text or package_hash not in text and rel.endswith("test_s6d_11_ruleset_package_closure.py"):
            mismatches.append(rel)
    return sorted(mismatches)


def derive_engine_contract_inventory(
    repo_root: Path, *, engine_version: str, ruleset_set_sha256: str,
    source_groups: dict[str, tuple[tuple[str, str], ...]] | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    source_groups = ENGINE_CONTRACT_SOURCE_GROUPS if source_groups is None else source_groups
    if set(source_groups) != REQUIRED_ENGINE_CONTRACT_FAMILIES:
        raise RulesetContractError("unreconstructable_context", "engine contract family registry differs")
    items: list[dict[str, str]] = []
    for family, members in sorted(source_groups.items()):
        payloads: dict[str, Any] = {}
        member_ids = [member_id for member_id, _rel in members]
        if len(member_ids) != len(set(member_ids)):
            raise RulesetContractError("unreconstructable_context", f"duplicate stable member ID in {family}")
        for member_id, rel in members:
            if rel == CATALOG_ADMISSION_LEDGER_MEMBER_PATH:
                try:
                    payloads[member_id] = load_catalog_admission_ledger(repo_root)
                except ValueError as exc:
                    raise RulesetContractError("unreconstructable_context", str(exc)) from exc
                continue
            path = repo_root / rel
            if not path.is_file():
                raise RulesetContractError("unreconstructable_context", f"missing active owner artifact: {rel}")
            payloads[member_id] = load_json_bytes(path.read_bytes())
        items.append({
            "family": family,
            "contract_id": f"engine_contract.{family}.v1",
            "semantic_sha256": sha256(ENTRY_DOMAIN + canonical_json(payloads)),
        })
    core = {
        "inventory_schema_version": 1,
        "engine_version": engine_version,
        "ruleset_set_sha256": ruleset_set_sha256,
        "items": sorted(items, key=lambda row: row["family"]),
    }
    result = dict(core)
    result["inventory_sha256"] = sha256(INVENTORY_DOMAIN + canonical_json(core))
    _validated_engine_contract_entries(
        result, engine_version=engine_version, ruleset_set_sha256=ruleset_set_sha256
    )
    return result


def validate_registered_package_suite(repo_root: Path) -> list[dict[str, str]]:
    repo_root = Path(repo_root).resolve()
    ledger_path = repo_root / "DEV/CATALOG/ruleset-package-closure.json"
    ledger = load_json_bytes(ledger_path.read_bytes())
    rows = ledger.get("registered_package_validators")
    if (
        not isinstance(rows, list) or len(rows) != len(REGISTERED_VALIDATORS)
        or any(
            not isinstance(row, dict)
            or set(row) != {"validator_id", "path", "test_path", "scope", "stage"}
            or row.get("stage") != "BUILD_AND_CONFORMANCE"
            or not isinstance(row.get("scope"), str) or not row["scope"]
            for row in rows
        )
    ):
        raise RulesetContractError("unreconstructable_context", "validator registry missing")
    observed = {row.get("path"): (row.get("validator_id"), row.get("test_path")) for row in rows if isinstance(row, dict)}
    if observed != REGISTERED_VALIDATORS:
        raise RulesetContractError("unreconstructable_context", "validator registry is incomplete, stale or ambiguous")
    results: list[dict[str, str]] = []
    for validator_path, (validator_id, test_path) in sorted(REGISTERED_VALIDATORS.items()):
        if not (repo_root / validator_path).is_file() or not (repo_root / test_path).is_file():
            raise RulesetContractError("unreconstructable_context", f"missing validator or test: {validator_path}")
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "DEV/TESTS", "-p", Path(test_path).name, "-q"],
            cwd=repo_root, text=True, capture_output=True, check=False,
        )
        if completed.returncode:
            detail = (completed.stderr or completed.stdout).strip()
            raise RulesetContractError("unreconstructable_context", f"{validator_path} failed: {detail}")
        results.append({"validator_id": validator_id, "result": "PASS"})
    return results


def validate_transitional_identity_census(repo_root: Path, ledger: dict[str, Any] | None = None) -> None:
    repo_root = Path(repo_root).resolve()
    if ledger is None:
        ledger = load_json_bytes((repo_root / "DEV/CATALOG/ruleset-package-closure.json").read_bytes())
    rows = ledger.get("transitional_package_identity")
    if not isinstance(rows, list) or len(rows) != len(TRANSITIONAL_KEYS):
        raise RulesetContractError("unreconstructable_context", "transitional identity census incomplete")
    expected_fields = {
        "key", "carrier_paths", "field_paths", "producer_derivation",
        "current_authority_use", "consumer_paths", "disposition",
        "canonical_replacement", "positive_proof", "negative_proof",
    }
    keys = {row.get("key") for row in rows if isinstance(row, dict)}
    if keys != TRANSITIONAL_KEYS or any(set(row) != expected_fields for row in rows):
        raise RulesetContractError("unreconstructable_context", "transitional identity row differs")
    for row in rows:
        for rel in row["carrier_paths"] + row["consumer_paths"]:
            if not (repo_root / rel).is_file():
                raise RulesetContractError("unreconstructable_context", f"orphan transitional path: {rel}")
    forbidden = (
        '"content_set_sha256":', "'content_set_sha256':",
        '["content_set_sha256"]', '.get("content_set_sha256")',
        "package_content_set_sha256", "identity_bound_package_candidate",
    )
    excluded = {
        (repo_root / "DEV/CATALOG/ruleset-package-closure.json").resolve(),
        (repo_root / "DEV/TESTS/test_s6d_11_ruleset_package_closure.py").resolve(),
        (repo_root / "DEV/TOOLS/validate_ruleset_package_closure.py").resolve(),
    }
    for path in repo_root.rglob("*"):
        if not path.is_file() or path.resolve() in excluded or path.suffix.lower() not in {".json", ".py", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            raise RulesetContractError("unreconstructable_context", f"parallel transitional identity carrier: {path.relative_to(repo_root)}")


def validate_integrated_ruleset_package(
    repo_root: Path,
    *,
    root_package_ids: list[str],
    engine_version: str,
    catalog_generation: str,
) -> tuple[dict[str, Any], dict[str, PackageSnapshot], dict[str, Any], list[dict[str, str]]]:
    repo_root = Path(repo_root).resolve()
    package_dirs = [repo_root / "GAME/RULES/packages" / package_id for package_id in root_package_ids]
    lock, snapshots = build_resolved_lock(
        package_dirs,
        root_package_ids=root_package_ids,
        engine_version=engine_version,
        catalog_generation=catalog_generation,
    )
    engine_inventory = derive_engine_contract_inventory(
        repo_root, engine_version=engine_version,
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )
    validate_transitional_identity_census(repo_root)
    validator_results = validate_registered_package_suite(repo_root)
    return lock, snapshots, engine_inventory, validator_results
