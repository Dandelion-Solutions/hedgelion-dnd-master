#!/usr/bin/env python3
"""S6D-11 build/conformance orchestration over the shipped GAME contract."""

from __future__ import annotations

import re
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

try:
    from DEV.TOOLS.activity_primitive_contracts import load_activity_primitive_contracts
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from activity_primitive_contracts import load_activity_primitive_contracts


# Symbolic member paths. Neither is read as a literal file: derive_engine_contract_inventory()
# recognizes these exact strings and resolves each through its canonical loader/assembler
# instead, since both are physically a manifest plus shards, not one file.
CATALOG_ADMISSION_LEDGER_MEMBER_PATH = "DEV/CATALOG/catalog-admission-ledger.json"
ACTIVITY_PRIMITIVE_CONTRACTS_MEMBER_PATH = (
    "DEV/CATALOG/activity-primitive-contracts.json"
)

ENGINE_CONTRACT_SOURCE_GROUPS = {
    "catalog_admission": (
        ("catalog_admission_ledger", CATALOG_ADMISSION_LEDGER_MEMBER_PATH),
    ),
    "mechanical_surface": (
        ("core_catalog", "DEV/CATALOG/core-catalog.json"),
        ("mechanical_surfaces", "DEV/CATALOG/mechanical-surfaces.json"),
    ),
    "primitive": (
        ("activity_primitive_contracts", ACTIVITY_PRIMITIVE_CONTRACTS_MEMBER_PATH),
    ),
    "portable_value": (
        ("portable_value_contracts", "DEV/CATALOG/portable-value-contracts.json"),
        ("portable_value_routes", "DEV/CATALOG/portable-value-routes.json"),
    ),
    "schema_contract": (
        (
            "ruleset_package_manifest_schema",
            "DEV/SCHEMAS/ruleset-package-manifest.schema.json",
        ),
        (
            "resolved_ruleset_lock_schema",
            "DEV/SCHEMAS/resolved-ruleset-lock.schema.json",
        ),
        (
            "ruleset_set_compatibility_result_schema",
            "DEV/SCHEMAS/ruleset-set-compatibility-result.schema.json",
        ),
        (
            "runtime_resolution_state_schema",
            "DEV/SCHEMAS/runtime-resolution-state.schema.json",
        ),
        (
            "runtime_continuation_state_schema",
            "DEV/SCHEMAS/runtime-continuation-state.schema.json",
        ),
    ),
}

REGISTERED_VALIDATORS = {
    "DEV/TOOLS/validate_character_mvp_seed.py": (
        "character_seed_closure",
        "DEV/TESTS/test_s6d_07_character_mvp_seed.py",
    ),
    "DEV/TOOLS/validate_health_effects_recovery_seed.py": (
        "health_effect_recovery_closure",
        "DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py",
    ),
    "DEV/TOOLS/validate_domain_rules_coverage.py": (
        "domain_rules_coverage_closure",
        "DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py",
    ),
    "DEV/TOOLS/validate_house_rules_mechanical_boundary.py": (
        "house_rules_boundary_closure",
        "DEV/TESTS/test_s6d_10_house_rules_boundary_contract.py",
    ),
}
TRANSITIONAL_KEYS = frozenset(
    {
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
    }
)
CURRENT_IDENTITY_LITERAL_CARRIERS = (
    "DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py",
    "DEV/TESTS/test_s6d_11_ruleset_package_closure.py",
)

ACTIVITY_COMPILER_CONTRACTS_RELATIVE = "GAME/TOOLS/activity_compiler_contracts.json"
ACTIVITY_COMPILER_CONTRACTS_SCHEMA_VERSION = 1
_SOURCE_PATH = re.compile(r"DEV/[A-Za-z0-9_./#:-]+")
_LEDGER_PROVENANCE_FIELDS = frozenset(
    {
        "evidence_citation",
        "semantic_owner",
        "downstream_owner",
        "decision_owner",
        "owner",
    }
)
_LEDGER_TOP_LEVEL_PROVENANCE_FIELDS = frozenset({"decision_owner", "source_registry"})


def current_identity_projection_mismatches(repo_root: Path) -> list[str]:
    """Compare current identity projections with one fresh canonical reconstruction."""
    repo_root = Path(repo_root).resolve()
    package = repo_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
    manifest = load_json_bytes((package / "ruleset-package-manifest.json").read_bytes())
    lock, snapshots = build_resolved_lock(
        [package],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    snapshot = snapshots[manifest["package_id"]]
    package_hash = snapshot.content_sha256
    set_hash = lock["ruleset_set_sha256"]
    mismatches: list[str] = []
    closure = load_json_bytes(
        (repo_root / "DEV/CATALOG/ruleset-package-closure.json").read_bytes()
    )
    if closure.get("derived_current_identity") != {
        "authority": "DERIVED_NONAUTHORITATIVE_VERIFICATION_EVIDENCE",
        "package_content_sha256": package_hash,
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "ruleset_set_sha256": set_hash,
    }:
        mismatches.append("DEV/CATALOG/ruleset-package-closure.json")
    binding = load_json_bytes(
        (repo_root / "DEV/CATALOG/domain-rules-coverage-binding.json").read_bytes()
    )
    expected_binding = {
        "profile_id": "gameplay_spine.mvp.v1",
        "package_id": manifest["package_id"],
        "package_revision": manifest["package_revision"],
        "compatibility_family": manifest["compatibility_family"],
        "compatibility_generation": manifest["compatibility_generation"],
        "catalog_generation": manifest["catalog_generation"],
        "gameplay_spine_member": "gameplay-spine-seed.json",
        "package_content_sha256": package_hash,
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "ruleset_set_sha256": set_hash,
    }
    if binding != expected_binding or "gameplay-spine-seed.json" not in {
        row["path"] for row in snapshot.members
    }:
        mismatches.append("DEV/CATALOG/domain-rules-coverage-binding.json")
    actors = load_json_bytes(
        (repo_root / "DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json").read_bytes()
    )
    if any(
        row.get("ruleset_set_digest_generation") != RULESET_SET_DIGEST_GENERATION
        or row.get("ruleset_set_sha256") != set_hash
        for row in actors.get("readiness_evidence", {}).values()
    ):
        mismatches.append("DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json")
    boundary = load_json_bytes(
        (repo_root / "DEV/CATALOG/house-rules-mechanical-boundary.json").read_bytes()
    )
    identity = boundary.get("resolved_ruleset_identity", {})
    expected_identity = {
        "package_id": manifest["package_id"],
        "package_revision": manifest["package_revision"],
        "compatibility_family": manifest["compatibility_family"],
        "compatibility_generation": manifest["compatibility_generation"],
        "catalog_generation": manifest["catalog_generation"],
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "ruleset_set_sha256": set_hash,
        "runtime_selection_state": "ACTIVE_VERIFIED_MACHINE_CONTRACT",
    }
    if identity != expected_identity:
        mismatches.append("DEV/CATALOG/house-rules-mechanical-boundary.json")
    for rel in CURRENT_IDENTITY_LITERAL_CARRIERS:
        text = (repo_root / rel).read_text(encoding="utf-8")
        if set_hash not in text or (
            package_hash not in text
            and rel.endswith("test_s6d_11_ruleset_package_closure.py")
        ):
            mismatches.append(rel)
    return sorted(mismatches)


def _assemble_engine_contract_payloads(
    repo_root: Path,
    source_groups: dict[str, tuple[tuple[str, str], ...]] | None = None,
) -> dict[str, dict[str, Any]]:
    repo_root = Path(repo_root).resolve()
    source_groups = (
        ENGINE_CONTRACT_SOURCE_GROUPS if source_groups is None else source_groups
    )
    if set(source_groups) != REQUIRED_ENGINE_CONTRACT_FAMILIES:
        raise RulesetContractError(
            "unreconstructable_context", "engine contract family registry differs"
        )
    family_payloads: dict[str, dict[str, Any]] = {}
    for family, members in sorted(source_groups.items()):
        payloads: dict[str, Any] = {}
        member_ids = [member_id for member_id, _rel in members]
        if len(member_ids) != len(set(member_ids)):
            raise RulesetContractError(
                "unreconstructable_context", f"duplicate stable member ID in {family}"
            )
        for member_id, rel in members:
            if rel == CATALOG_ADMISSION_LEDGER_MEMBER_PATH:
                try:
                    payloads[member_id] = load_catalog_admission_ledger(repo_root)
                except ValueError as exc:
                    raise RulesetContractError(
                        "unreconstructable_context", str(exc)
                    ) from exc
                continue
            if rel == ACTIVITY_PRIMITIVE_CONTRACTS_MEMBER_PATH:
                try:
                    payloads[member_id] = load_activity_primitive_contracts(repo_root)
                except ValueError as exc:
                    raise RulesetContractError(
                        "unreconstructable_context", str(exc)
                    ) from exc
                continue
            path = repo_root / rel
            if not path.is_file():
                raise RulesetContractError(
                    "unreconstructable_context", f"missing active owner artifact: {rel}"
                )
            payloads[member_id] = load_json_bytes(path.read_bytes())
        family_payloads[family] = payloads
    return family_payloads


def _inventory_from_engine_contract_payloads(
    family_payloads: dict[str, dict[str, Any]],
    *,
    engine_version: str,
    ruleset_set_sha256: str,
) -> dict[str, Any]:
    if set(family_payloads) != REQUIRED_ENGINE_CONTRACT_FAMILIES:
        raise RulesetContractError(
            "unreconstructable_context", "engine contract family registry differs"
        )
    items = [
        {
            "family": family,
            "contract_id": f"engine_contract.{family}.v1",
            "semantic_sha256": sha256(
                ENTRY_DOMAIN + canonical_json(family_payloads[family])
            ),
        }
        for family in sorted(family_payloads)
    ]
    core = {
        "inventory_schema_version": 2,
        "engine_version": engine_version,
        "ruleset_set_digest_generation": RULESET_SET_DIGEST_GENERATION,
        "ruleset_set_sha256": ruleset_set_sha256,
        "items": sorted(items, key=lambda row: row["family"]),
    }
    result = dict(core)
    result["inventory_sha256"] = sha256(INVENTORY_DOMAIN + canonical_json(core))
    _validated_engine_contract_entries(
        result, engine_version=engine_version, ruleset_set_sha256=ruleset_set_sha256
    )
    return result


def _path_neutral_compiler_value(value: Any, *, field_name: str = "") -> Any:
    if isinstance(value, dict):
        return {
            key: _path_neutral_compiler_value(item, field_name=key)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [
            _path_neutral_compiler_value(item, field_name=field_name) for item in value
        ]
    if isinstance(value, str):
        if field_name in {"schema_ref", "portable_realization_owner"}:
            prefix, separator, fragment = value.partition("#")
            if prefix.startswith("DEV/SCHEMAS/"):
                schema_id = f"https://hedgelion.invalid/schemas/{Path(prefix).name}"
                return schema_id + (f"#{fragment}" if separator else "")
        return _SOURCE_PATH.sub("source-owner", value)
    return value


def _project_engine_contract_member(
    family: str, member_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Remove documentary owner paths without dropping executable contract data."""
    projected = _path_neutral_compiler_value(payload)
    if family == "catalog_admission" and member_id == "catalog_admission_ledger":
        projected = {
            key: value
            for key, value in projected.items()
            if key not in _LEDGER_TOP_LEVEL_PROVENANCE_FIELDS
        }

        entries = projected.get("entries")
        if isinstance(entries, list):
            projected["entries"] = [
                {
                    key: value
                    for key, value in entry.items()
                    if key not in _LEDGER_PROVENANCE_FIELDS
                }
                for entry in entries
            ]
    elif family == "primitive" and member_id == "activity_primitive_contracts":
        projected.pop("owner", None)
        value_contracts = projected.get("value_contracts")
        if isinstance(value_contracts, dict):
            projected["value_contracts"] = {
                value_id: {
                    key: value for key, value in contract.items() if key != "owner"
                }
                for value_id, contract in value_contracts.items()
            }
    elif family == "portable_value":
        projected.pop("owner", None)
    return projected


def derive_activity_compiler_contracts(
    repo_root: Path,
    *,
    engine_version: str,
    ruleset_set_sha256: str,
) -> dict[str, Any]:
    """Derive the path-neutral runtime compiler view from canonical DEV owners.

    Family identities are computed over the original assembled owner payloads,
    before projection sanitization. The projection is never hashed as a substitute
    for an existing engine-contract family.
    """
    family_payloads = _assemble_engine_contract_payloads(repo_root)
    inventory = _inventory_from_engine_contract_payloads(
        family_payloads,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )
    result = {
        "schema_version": ACTIVITY_COMPILER_CONTRACTS_SCHEMA_VERSION,
        "source_identity": {
            "inventory_schema_version": inventory["inventory_schema_version"],
            "engine_version": inventory["engine_version"],
            "ruleset_set_digest_generation": inventory["ruleset_set_digest_generation"],
            "ruleset_set_sha256": inventory["ruleset_set_sha256"],
            "inventory_sha256": inventory["inventory_sha256"],
            "families": [
                {
                    "family": item["family"],
                    "contract_id": item["contract_id"],
                    "source_semantic_sha256": item["semantic_sha256"],
                }
                for item in inventory["items"]
            ],
        },
        "families": {
            family: {
                member_id: _project_engine_contract_member(family, member_id, payload)
                for member_id, payload in family_payloads[family].items()
            }
            for family in sorted(family_payloads)
        },
    }
    # This is a typed producer projection, not a second MechanicalContext DAG.
    # Gameplay-spine's exact generic definitions and the domain-resolution owner
    # (validate_domain_rules_coverage.py:169-190) explicitly supply d20 + native
    # ability basis + proficiency, with adjudicated DC 1..30. No other legacy
    # alias receives arithmetic by resemblance or name.
    seed_path = repo_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json"
    seed = load_json_bytes(seed_path.read_bytes())
    definitions = {record["id"]: record for record in seed["activity_definitions"]}
    primitives = result["families"]["primitive"]["activity_primitive_contracts"]["contracts"]
    roll = next(row for row in primitives if row["primitive_id"] == "op.roll")
    declarations = roll.setdefault("compiler_declarations", {})
    for family in ("check", "save"):
        activity_id = f"activity.{family}.generic"
        data = definitions[activity_id]["data"]
        parameters = data["parameters"]
        symbol_id = f"compiled.generic_{family}_roll"
        if (data["steps"][0] != {"op": "op.roll", "args": {"request": symbol_id}, "export": f"{family}_roll"}
            or parameters["ability_id"]["source_class"] != "ENGINE_BOUND"
            or parameters["ability_id"]["value_type"] != "machine_id"
            or parameters["dc"] != {"source_class": "INVOCATION_ADJUDICATED", "value_type": "integer", "cardinality": "single", "required": True, "minimum": 1, "maximum": 30}):
            raise RulesetContractError("unreconstructable_context", f"generic producer source contract changed: {activity_id}")
        template = {"kind": "D20_ABILITY_BASIS", "modifier_basis": "AUTHORITATIVE_ABILITY_AND_PROFICIENCY",
                    "ability_parameter": "ability_id", "purpose_id": f"roll.{family}", "roller_role": "actor"}
        if family == "check":
            template["proficiency_parameter"] = "proficiency_id"
        if activity_id in declarations:
            raise RulesetContractError("unreconstructable_context", f"duplicate generic producer authority: {activity_id}")
        declarations[activity_id] = {"roles": {"actor": "world.actor"}, "profiles": [], "symbols": {
            symbol_id: {"value_kind": "roll_request", "cardinality": "single", "template": template,
                "dependencies": [], "reads": [f"selector:{family}.roll"],
                "permitted_occurrence_ids": [f"{activity_id}.step.0"]}}}
    character = load_json_bytes((repo_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json").read_bytes())
    tactical = next(record for record in character["activity_definitions"] if record["id"] == "activity.feature.tactical_mind")
    expected_details = {"invocation_gate": "PRIOR_ABILITY_CHECK_FAILED", "request_binding": "D10_WITH_PRIOR_CHECK_TOTAL_AS_FIXED_MODIFIER", "consume_policy": "ONLY_IF_AUGMENTED_RESULT_SUCCEEDS", "failed_augmented_result": "NO_RESOURCE_CONSUMPTION_AND_ORIGINAL_FAILURE_STANDS"}
    tactical_data = tactical["data"]
    if (tactical_data["details"] != expected_details or tactical_data["steps"][0]["args"] != {"request": "compiled.d10_plus_prior_check_total"}
        or tactical_data["steps"][1]["args"]["threshold"] != "invocation.prior_check_dc"
        or tactical_data["steps"][2]["when"] != {"result": "augmented_check.outcome", "in": ["success"]}):
        raise RulesetContractError("unreconstructable_context", "Tactical Mind producer source contract changed")
    if tactical["id"] in declarations:
        raise RulesetContractError("unreconstructable_context", "duplicate Tactical Mind producer authority")
    declarations[tactical["id"]] = {"roles": {"actor": "world.actor"}, "profiles": [],
        "parameters": {"prior_check_dc": {"source_class": "ENGINE_BOUND", "value_type": "integer", "cardinality": "single", "required": True}},
        "symbols": {"compiled.d10_plus_prior_check_total": {"value_kind": "roll_request", "cardinality": "single",
            "template": {"kind": "D10_FIXED_FAILED_CHECK", "modifier_basis": "FIXED_PRIOR_TOTAL",
                "prior_result_source": "ACCEPTED_FAILED_ABILITY_CHECK", "original_dc_parameter": "prior_check_dc", "roller_role": "actor"},
            "dependencies": [], "reads": [], "permitted_occurrence_ids": [tactical["id"] + ".step.0"]}}}
    burning = next(record for record in character["activity_definitions"] if record["id"] == "activity.spell.burning_hands")
    burning_data = burning["data"]
    per_target = burning_data["steps"][2]["args"]["steps"]
    if (burning_data["details"]["save_damage_policy"] != "HALF_ON_SUCCESS_FLOOR_MIN_ZERO"
        or per_target[2]["args"]["components"] != "compiled.full_fire_damage"
        or per_target[3]["args"]["components"] != "compiled.half_fire_damage_floor"):
        raise RulesetContractError("unreconstructable_context", "half-damage producer source contract changed")
    damage = next(row for row in primitives if row["primitive_id"] == "op.apply_damage")
    if burning["id"] in damage.get("compiler_declarations", {}):
        raise RulesetContractError("unreconstructable_context", "duplicate half-damage producer authority")
    damage.setdefault("compiler_declarations", {})[burning["id"]] = {"roles": {}, "profiles": [], "symbols": {
        "compiled.half_fire_damage_floor": {"value_kind": "damage_components", "cardinality": "single",
            "template": {"kind": "HALF_DAMAGE_FLOOR_MIN_ZERO", "source_symbol": "compiled.full_fire_damage", "input_contract": "SAME_FIXED_FULL_DAMAGE_RESULT"},
            "dependencies": ["compiled.full_fire_damage"], "reads": [],
            "permitted_occurrence_ids": [burning["id"] + ".step.2.steps.step.3"]}}}
    return result


def _activity_compiler_contracts_bytes(
    repo_root: Path,
    *,
    engine_version: str,
    ruleset_set_sha256: str,
) -> bytes:
    projection = derive_activity_compiler_contracts(
        repo_root,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )
    return canonical_json(projection) + b"\n"


def write_activity_compiler_contracts_projection(
    repo_root: Path,
    *,
    engine_version: str,
    ruleset_set_sha256: str,
) -> str:
    """Regenerate the derived GAME view from its canonical DEV owners."""
    repo_root = Path(repo_root).resolve()
    target = repo_root / ACTIVITY_COMPILER_CONTRACTS_RELATIVE
    if target.is_symlink() or not target.parent.is_dir():
        raise RulesetContractError(
            "unreconstructable_context",
            "compiler projection destination is not a regular path",
        )
    raw = _activity_compiler_contracts_bytes(
        repo_root,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(target)
    return sha256(raw)


def validate_activity_compiler_contracts_projection(
    repo_root: Path,
    *,
    engine_version: str,
    ruleset_set_sha256: str,
) -> tuple[dict[str, Any], str]:
    """Require exact installed bytes generated from original canonical families."""
    repo_root = Path(repo_root).resolve()
    target = repo_root / ACTIVITY_COMPILER_CONTRACTS_RELATIVE
    try:
        actual = target.read_bytes()
    except OSError as exc:
        raise RulesetContractError(
            "unreconstructable_context",
            "installed Activity compiler contracts projection is unavailable",
        ) from exc
    expected = _activity_compiler_contracts_bytes(
        repo_root,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )
    if actual != expected:
        raise RulesetContractError(
            "unreconstructable_context",
            "installed Activity compiler contracts projection differs from canonical source",
        )
    return (
        load_json_bytes(actual, failure_reason="unreconstructable_context"),
        sha256(actual),
    )


def derive_engine_contract_inventory(
    repo_root: Path,
    *,
    engine_version: str,
    ruleset_set_sha256: str,
    source_groups: dict[str, tuple[tuple[str, str], ...]] | None = None,
) -> dict[str, Any]:
    family_payloads = _assemble_engine_contract_payloads(repo_root, source_groups)
    return _inventory_from_engine_contract_payloads(
        family_payloads,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )


def validate_registered_package_suite(repo_root: Path) -> list[dict[str, str]]:
    repo_root = Path(repo_root).resolve()
    ledger_path = repo_root / "DEV/CATALOG/ruleset-package-closure.json"
    ledger = load_json_bytes(ledger_path.read_bytes())
    rows = ledger.get("registered_package_validators")
    if (
        not isinstance(rows, list)
        or len(rows) != len(REGISTERED_VALIDATORS)
        or any(
            not isinstance(row, dict)
            or set(row) != {"validator_id", "path", "test_path", "scope", "stage"}
            or row.get("stage") != "BUILD_AND_CONFORMANCE"
            or not isinstance(row.get("scope"), str)
            or not row["scope"]
            for row in rows
        )
    ):
        raise RulesetContractError(
            "unreconstructable_context", "validator registry missing"
        )
    observed = {
        row.get("path"): (row.get("validator_id"), row.get("test_path"))
        for row in rows
        if isinstance(row, dict)
    }
    if observed != REGISTERED_VALIDATORS:
        raise RulesetContractError(
            "unreconstructable_context",
            "validator registry is incomplete, stale or ambiguous",
        )
    results: list[dict[str, str]] = []
    for validator_path, (validator_id, test_path) in sorted(
        REGISTERED_VALIDATORS.items()
    ):
        if (
            not (repo_root / validator_path).is_file()
            or not (repo_root / test_path).is_file()
        ):
            raise RulesetContractError(
                "unreconstructable_context",
                f"missing validator or test: {validator_path}",
            )
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "DEV/TESTS",
                "-p",
                Path(test_path).name,
                "-q",
            ],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            detail = (completed.stderr or completed.stdout).strip()
            raise RulesetContractError(
                "unreconstructable_context", f"{validator_path} failed: {detail}"
            )
        results.append({"validator_id": validator_id, "result": "PASS"})
    return results


def validate_transitional_identity_census(
    repo_root: Path, ledger: dict[str, Any] | None = None
) -> None:
    repo_root = Path(repo_root).resolve()
    if ledger is None:
        ledger = load_json_bytes(
            (repo_root / "DEV/CATALOG/ruleset-package-closure.json").read_bytes()
        )
    rows = ledger.get("transitional_package_identity")
    if not isinstance(rows, list) or len(rows) != len(TRANSITIONAL_KEYS):
        raise RulesetContractError(
            "unreconstructable_context", "transitional identity census incomplete"
        )
    expected_fields = {
        "key",
        "carrier_paths",
        "field_paths",
        "producer_derivation",
        "current_authority_use",
        "consumer_paths",
        "disposition",
        "canonical_replacement",
        "positive_proof",
        "negative_proof",
    }
    keys = {row.get("key") for row in rows if isinstance(row, dict)}
    if keys != TRANSITIONAL_KEYS or any(set(row) != expected_fields for row in rows):
        raise RulesetContractError(
            "unreconstructable_context", "transitional identity row differs"
        )
    for row in rows:
        for rel in row["carrier_paths"] + row["consumer_paths"]:
            if not (repo_root / rel).is_file():
                raise RulesetContractError(
                    "unreconstructable_context", f"orphan transitional path: {rel}"
                )
    forbidden = (
        '"content_set_sha256":',
        "'content_set_sha256':",
        '["content_set_sha256"]',
        '.get("content_set_sha256")',
        "package_content_set_sha256",
        "identity_bound_package_candidate",
    )
    excluded = {
        (repo_root / "DEV/CATALOG/ruleset-package-closure.json").resolve(),
        (repo_root / "DEV/TESTS/test_s6d_11_ruleset_package_closure.py").resolve(),
        (repo_root / "DEV/TOOLS/validate_ruleset_package_closure.py").resolve(),
    }
    for path in repo_root.rglob("*"):
        if (
            not path.is_file()
            or path.resolve() in excluded
            or path.suffix.lower() not in {".json", ".py", ".yaml", ".yml"}
        ):
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            raise RulesetContractError(
                "unreconstructable_context",
                f"parallel transitional identity carrier: {path.relative_to(repo_root)}",
            )


def validate_integrated_ruleset_package(
    repo_root: Path,
    *,
    root_package_ids: list[str],
    engine_version: str,
    catalog_generation: int,
) -> tuple[
    dict[str, Any], dict[str, PackageSnapshot], dict[str, Any], list[dict[str, str]]
]:
    repo_root = Path(repo_root).resolve()
    package_dirs = [
        repo_root / "GAME/RULES/packages" / package_id
        for package_id in root_package_ids
    ]
    lock, snapshots = build_resolved_lock(
        package_dirs,
        root_package_ids=root_package_ids,
        engine_version=engine_version,
        catalog_generation=catalog_generation,
    )
    engine_inventory = derive_engine_contract_inventory(
        repo_root,
        engine_version=engine_version,
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )
    validate_activity_compiler_contracts_projection(
        repo_root,
        engine_version=engine_version,
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )
    validate_transitional_identity_census(repo_root)
    validator_results = validate_registered_package_suite(repo_root)
    return lock, snapshots, engine_inventory, validator_results
