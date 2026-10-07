"""Closed source/compiler carriers for the bounded SP03 policy slice."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

from GAME.TOOLS import activity_contracts, activity_runtime

pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
CALCULATION_PROFILES = (
    "calculation.roll_advantage_srd521",
    "calculation.damage_defense_srd521",
    "calculation.armor_class_srd521",
    "calculation.capability_projection_srd521",
)
CAST_PROFILES = (
    "execution.spell_cast.srd521",
    "execution.spell_cast.ritual",
    "execution.spell_cast.long",
    "execution.spell_cast.invalid_target",
    "execution.spell_cast.countered",
)
FIXTURE_ACTIVITY_ID = "activity.test.sp03_carriers"
FIXTURE_CONSUMER_ID = f"{FIXTURE_ACTIVITY_ID}.step.0"
FIXTURE_SELECTOR_ID = "selector.test.sp03_roll"
FIXTURE_OPERATION_ID = "operation.test.sp03_pair"


def _schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _accepts(schema: dict[str, Any], reference: str, value: object) -> bool:
    definition_name = reference.removeprefix("#/$defs/")
    validation_root = {
        "$schema": schema["$schema"],
        "$defs": schema.get("$defs", {}),
        "allOf": [schema["$defs"][definition_name]],
    }
    return Draft202012Validator(validation_root).is_valid(value)


def _mechanical_policy_contract(
    profile_id: str,
    *,
    static_dependencies: tuple[str, ...] = (),
    fact_ids: tuple[str, ...] = (),
    input_classes: tuple[str, ...] = ("ENGINE_STATE",),
    subject_kinds: tuple[str, ...] = ("world.actor",),
    dependency_kinds: tuple[str, ...] = ("accessor",),
) -> dict[str, object]:
    contribution, result, combination, operation_kind, normalization, constraint = {
        CALCULATION_PROFILES[0]: (
            "roll_modifier",
            "roll_modifier_set",
            "roll_advantage_cancellation_v1",
            "roll_modifier",
            "CANCEL_APPLICABLE_OPPOSITES",
            "stable_raw_dice_identity_and_contribution_provenance",
        ),
        CALCULATION_PROFILES[1]: (
            "damage_defense",
            "damage_result",
            "damage_defense_source_ordered_v1",
            "damage_defense",
            "SOURCE_DEFINED_ORDER",
            "damage_type_origin_bypass_order_and_rounding",
        ),
        CALCULATION_PROFILES[2]: (
            "armor_class_base",
            "integer",
            "armor_class_nonadditive_base_v1",
            "armor_class_base",
            "SELECT_ONE_LEGAL_BASE",
            "eligible_nonadditive_ac_base",
        ),
        CALCULATION_PROFILES[3]: (
            "capability_projection",
            "capability_projection",
            "capability_native_projection_v1",
            "capability_change",
            "NATIVE_GRANTS_AND_RESTRICTIONS",
            "native_role_form_equipment_movement_sense_projection",
        ),
    }[profile_id]
    return {
        "calculation_policy_id": profile_id,
        "calculation_policy_generation": 1,
        "allowed_operations": [FIXTURE_OPERATION_ID],
        "operation_contracts": {
            FIXTURE_OPERATION_ID: {
                "value_kind": operation_kind,
                "normalization": normalization,
                "constraints": [constraint],
                "calculation_policy_id": profile_id,
                "calculation_policy_generation": 1,
            }
        },
        "contribution_type": contribution,
        "result_type": result,
        "result_constraints": {},
        "subject_kinds": list(subject_kinds),
        "binding_kinds": ["subject", "activity_definition"],
        "allowed_dependency_kinds": list(dependency_kinds),
        "allowed_input_classes": list(input_classes),
        "permitted_context_fact_ids": list(fact_ids),
        "static_dependencies": list(static_dependencies),
        "combination_policy": combination,
        "resolution_owner": "SELECTOR_METADATA",
        "trace_policy": "RETAIN_ACCEPTED_REJECTED_PROVENANCE",
    }


def _policy_binding(
    profile_id: str = CALCULATION_PROFILES[0],
    *,
    consumer_id: str = FIXTURE_CONSUMER_ID,
    selector_id: str = FIXTURE_SELECTOR_ID,
    operation_ids: tuple[str, ...] = (FIXTURE_OPERATION_ID,),
    reads: tuple[str, ...] | None = None,
    fact_bindings: tuple[dict[str, object], ...] = (),
    native_roles: tuple[dict[str, object], ...] | None = None,
) -> dict[str, object]:
    policy_reads = (f"selector:{selector_id}",) if reads is None else reads
    role_bindings = (
        ({"read_ref": f"selector:{selector_id}", "role_names": ["actor"]},)
        if native_roles is None
        else native_roles
    )
    return {
        "consumer_id": consumer_id,
        "profile_id": profile_id,
        "profile_generation": 1,
        "reads": list(policy_reads),
        "selector_operation_pairs": [
            {"selector_id": selector_id, "operation_ids": list(operation_ids)}
        ],
        "context_fact_bindings": list(fact_bindings),
        "native_role_bindings": list(role_bindings),
    }


def _accessor_contract(
    accessor_id: str,
    *,
    consumer_refs: tuple[str, ...],
    dependencies: tuple[str, ...] = (),
    subject_kinds: tuple[str, ...] = ("world.actor",),
    value_type: str = "integer",
    source_class: str = "DIRECT_AUTHORITY",
) -> dict[str, object]:
    return {
        "source_class": source_class,
        "value_type": value_type,
        "subject_kinds": list(subject_kinds),
        "dependencies": list(dependencies),
        "disposition": "ACTIVE_ADMITTED",
        "input_class": "ENGINE_STATE",
        "argument_kinds": ["subject"],
        "implicit_binding_kinds": [],
        "missing_policy": "TYPED_HYDRATION_REQUIRED",
        "permitted_consumer_kinds": ["mechanical_predicate", "accessor", "derived"],
        "state_view_policy": "COMMITTED_OR_PROSPECTIVE_PINNED",
        "cache_policy": "VIEW_BINDING_CATALOG_REVISION_KEYED",
        "activation_trigger": "S6D-08_VALUED_CONDITION_AGGREGATION",
        "permitted_consumer_ids": list(consumer_refs),
    }


def _derived_node_contract(
    *,
    dependencies: tuple[str, ...] = (),
    consumer_refs: tuple[str, ...] = (),
    fact_ids: tuple[str, ...] = (),
    input_classes: tuple[str, ...] = ("ENGINE_STATE",),
) -> dict[str, object]:
    return {
        "allowed_dependency_kinds": ["selector", "accessor", "derived"],
        "allowed_input_classes": list(input_classes),
        "dependencies": list(dependencies),
        "disposition": "ACTIVE_INTERNAL",
        "result_role": "effect_member_set",
        "permitted_consumer_ids": list(consumer_refs),
        "permitted_context_fact_ids": list(fact_ids),
        "state_view_policy": "COMMITTED_OR_PROSPECTIVE_PINNED",
        "missing_policy": "PROPAGATE_TYPED_INPUT_FAILURE",
        "cache_policy": "DISPOSABLE_VIEW_BINDING_CATALOG_REVISION_KEYED",
    }


def _fact_contract(consumer_id: str) -> dict[str, object]:
    return {
        "disposition": "ACTIVE_ADMITTED",
        "source_class": "INVOCATION_ADJUDICATED",
        "value_type": "boolean",
        "producer": "HOST_LLM_BOUNDARY",
        "acceptance_authority": "ACTIVITY_INVOCATION_VALIDATOR",
        "occurrence_scope": "ACTIVITY_RESOLUTION_GENERATION",
        "provenance_policy": "STABLE_REF_AND_FINGERPRINT_REQUIRED",
        "missing_policy": "TYPED_MISSING_INPUT",
        "permitted_consumer_ids": [consumer_id],
        "retention_policy": "FIXED_CAUSAL_INPUT_WHILE_ACCEPTED_WORK_LIVE",
        "portable_realization_owner": "https://hedgelion.invalid/schemas/invocation-fact.schema.json",
        "activation_trigger": "SATISFIED_BY_S6D_09_EXACT_SPATIAL_CONSUMERS",
        "binding_policy": "EXACT_COMPILED_CONSUMER_ROLES",
        "optional_boundary_context": "ONLY_WHEN_INVOCATION_ARISES_FROM_BOUNDARY",
    }


def _compiler_inputs(
    profile_id: str = CALCULATION_PROFILES[0],
    *,
    activity_id: str = FIXTURE_ACTIVITY_ID,
    selector_contracts: dict[str, dict[str, object]] | None = None,
    accessor_contracts: dict[str, dict[str, object]] | None = None,
    derived_contracts: dict[str, dict[str, object]] | None = None,
    fact_contracts: dict[str, dict[str, object]] | None = None,
    role_contracts: dict[str, dict[str, object]] | None = None,
) -> tuple[
    dict[str, object],
    dict[str, object],
    dict[tuple[str, str], dict[str, str]],
    dict[str, dict[str, object]],
]:
    selectors = selector_contracts or {
        FIXTURE_SELECTOR_ID: _mechanical_policy_contract(profile_id)
    }
    accessors = accessor_contracts or {}
    derived_nodes = derived_contracts or {}
    context_facts = fact_contracts or {}
    role_map = role_contracts or {
        "actor": {"family_key": "world.actor", "required": True}
    }
    operations = {
        operation_id
        for selector in selectors.values()
        for operation_id in selector["allowed_operations"]
    }
    core: dict[str, object] = {
        "registries": {
            "rule_selectors": list(selectors),
            "rule_operations": sorted(operations),
        }
    }
    ledger_rows: dict[tuple[str, str], dict[str, str]] = {}
    for selector_id, selector in selectors.items():
        ledger_rows[("rule_selectors", selector_id)] = {
            "admission_disposition": "ACTIVE_ADMITTED",
            "realization_state": "COMPLETE",
            "consumer_or_dependency": activity_id,
        }
        for operation_id in selector["allowed_operations"]:
            ledger_rows[("rule_operations", operation_id)] = {
                "admission_disposition": "ACTIVE_ADMITTED",
                "realization_state": "COMPLETE",
            }
    for accessor_id in accessors:
        ledger_rows[("mechanical_accessors", accessor_id)] = {
            "admission_disposition": "ACTIVE_ADMITTED",
            "realization_state": "COMPLETE",
        }
    mechanical: dict[str, object] = {
        "selectors": selectors,
        "accessors": accessors,
        "derived_nodes": derived_nodes,
        "context_facts": context_facts,
    }
    return mechanical, core, ledger_rows, role_map


def _transitive_policy_fixture(
    *,
    current_consumer_refs: tuple[str, ...] | None = None,
    bloodied_consumer_refs: tuple[str, ...] | None = None,
    bloodied_dependencies: tuple[str, ...] = (
        "accessor:accessor.test.current",
        "accessor:accessor.test.maximum",
        "selector:selector.test.maximum",
    ),
) -> tuple[
    dict[str, object],
    dict[str, object],
    dict[str, object],
    dict[tuple[str, str], dict[str, str]],
    dict[str, dict[str, object]],
    activity_contracts.ProfileBinding,
]:
    fact_id = "fiction.test.allowed"
    activity_id = FIXTURE_ACTIVITY_ID
    selector = _mechanical_policy_contract(
        CALCULATION_PROFILES[0],
        static_dependencies=(
            "accessor:accessor.test.bloodied",
            "derived:derived.test.availability",
        ),
        fact_ids=(fact_id,),
        input_classes=("ENGINE_STATE", "INVOCATION_ADJUDICATED"),
        dependency_kinds=("accessor", "derived"),
    )
    dependency_selector = _mechanical_policy_contract(
        CALCULATION_PROFILES[2], dependency_kinds=("accessor", "derived")
    )
    accessors = {
        "accessor.test.bloodied": _accessor_contract(
            "accessor.test.bloodied",
            consumer_refs=(f"selector:{FIXTURE_SELECTOR_ID}",),
            dependencies=bloodied_dependencies,
            value_type="boolean",
            source_class="DERIVED_MECHANICAL",
        ),
        "accessor.test.current": _accessor_contract(
            "accessor.test.current",
            consumer_refs=(
                (f"activity:{activity_id}",)
                if current_consumer_refs is None
                else current_consumer_refs
            )
            + ("accessor:accessor.test.bloodied",),
        ),
        "accessor.test.maximum": _accessor_contract(
            "accessor.test.maximum",
            consumer_refs=("accessor:accessor.test.bloodied",),
        ),
    }
    derived_nodes = {
        "derived.test.availability": _derived_node_contract(
            consumer_refs=(f"selector:{FIXTURE_SELECTOR_ID}",)
        )
    }
    selectors = {
        FIXTURE_SELECTOR_ID: selector,
        "selector.test.maximum": dependency_selector,
    }
    context_facts = {fact_id: _fact_contract(activity_id)}
    mechanical, core, ledger_rows, roles = _compiler_inputs(
        CALCULATION_PROFILES[0],
        activity_id=activity_id,
        selector_contracts=selectors,
        accessor_contracts=accessors,
        derived_contracts=derived_nodes,
        fact_contracts=context_facts,
    )
    reads = (
        f"selector:{FIXTURE_SELECTOR_ID}",
        "accessor:accessor.test.current",
        f"fact:{fact_id}",
    )
    binding = _policy_binding(
        CALCULATION_PROFILES[0],
        consumer_id=FIXTURE_CONSUMER_ID,
        selector_id=FIXTURE_SELECTOR_ID,
        reads=reads,
        fact_bindings=(
            {"consumer_ref": f"selector:{FIXTURE_SELECTOR_ID}", "fact_ids": [fact_id]},
        ),
        native_roles=(
            {"read_ref": f"selector:{FIXTURE_SELECTOR_ID}", "role_names": ["actor"]},
            {"read_ref": "accessor:accessor.test.current", "role_names": ["actor"]},
        ),
    )
    profile_binding = activity_contracts.ProfileBinding(
        FIXTURE_CONSUMER_ID, CALCULATION_PROFILES[0], 1
    )
    return binding, mechanical, core, ledger_rows, roles, profile_binding


def _compile_transitive_fixture(
    binding: dict[str, object],
    mechanical: dict[str, object],
    core: dict[str, object],
    ledger_rows: dict[tuple[str, str], dict[str, str]],
    roles: dict[str, dict[str, object]],
    profile_binding: activity_contracts.ProfileBinding,
) -> tuple[activity_contracts.CompiledCalculationPolicy, ...]:
    compile_bindings = _compiler_policy_closure_api()
    return compile_bindings(
        (binding,),
        consumer_id=FIXTURE_CONSUMER_ID,
        activity_id=FIXTURE_ACTIVITY_ID,
        profile_bindings=(profile_binding,),
        mechanical=mechanical,
        core=core,
        ledger_rows=ledger_rows,
        role_contracts=roles,
    )


def _compiler_policy_closure_api():
    from inspect import signature

    compile_bindings = getattr(
        activity_runtime, "_compile_calculation_policy_bindings", None
    )
    assert callable(compile_bindings), "policy compiler closure binding is missing"
    required_parameters = {
        "mechanical",
        "core",
        "ledger_rows",
        "role_contracts",
    }
    assert required_parameters <= set(signature(compile_bindings).parameters), (
        "policy compiler must receive exact mechanical graph, admission and roles"
    )
    return compile_bindings


def _append_once(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _sp03_policy_row(consumer_id: str) -> dict[str, object]:
    return {
        "consumer_id": consumer_id,
        "profile_id": CALCULATION_PROFILES[0],
        "profile_generation": 1,
        "reads": [
            "selector:check.roll",
            "accessor:health.current",
            "fact:fiction.target_reachable",
        ],
        "selector_operation_pairs": [
            {"selector_id": "check.roll", "operation_ids": ["rule.add_flat"]}
        ],
        "context_fact_bindings": [
            {
                "consumer_ref": "selector:check.roll",
                "fact_ids": ["fiction.target_reachable"],
            }
        ],
        "native_role_bindings": [
            {"read_ref": "selector:check.roll", "role_names": ["actor"]},
            {"read_ref": "accessor:health.current", "role_names": ["actor"]},
        ],
    }


def _prepare_sp03_source_tree(source_root: Path, mutation: str | None = None) -> None:
    activity_id = "activity.conformance.compiler"
    outer_consumer = f"{activity_id}.step.0"
    nested_consumer = f"{activity_id}.step.1.steps.step.0"
    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    for path in sorted(primitive_root.glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        if row["contract"]["selection_state"] == "ACTIVE_ADMITTED":
            row["contract"].setdefault("compiler_declarations", {})[activity_id] = {
                "roles": {
                    "actor": "world.actor",
                    "target": "world.actor",
                    "asset_owner": "world.asset",
                },
                "symbols": {},
                "profiles": [],
            }
            path.write_text(json.dumps(row), encoding="utf-8")

    roll_path = primitive_root / "op.roll.json"
    roll = json.loads(roll_path.read_text(encoding="utf-8"))
    declaration = roll["contract"]["compiler_declarations"][activity_id]
    declaration["symbols"] = {}
    declaration["calculation_policies"] = [
        _sp03_policy_row(outer_consumer),
        _sp03_policy_row(nested_consumer),
    ]
    declaration["cast_profiles"] = [
        {
            "consumer_id": nested_consumer,
            "profile_id": CAST_PROFILES[0],
            "profile_generation": 1,
        }
    ]
    roll_path.write_text(json.dumps(roll), encoding="utf-8")

    loop_path = primitive_root / "op.for_each_target.json"
    loop = json.loads(loop_path.read_text(encoding="utf-8"))
    loop_declaration = loop["contract"]["compiler_declarations"][activity_id]
    loop_declaration["symbols"] = {
        "compiled.targets": {
            "value_kind": "entity_ref",
            "cardinality": "many",
            "value": ["actor.test.target"],
            "dependencies": [],
            "reads": [],
            "permitted_occurrence_ids": [f"{activity_id}.step.1"],
        },
    }
    loop_path.write_text(json.dumps(loop), encoding="utf-8")

    mechanical_path = source_root / "DEV/CATALOG/mechanical-surfaces.json"
    mechanical = json.loads(mechanical_path.read_text(encoding="utf-8"))
    selector = mechanical["selectors"]["check.roll"]
    selector.update(
        {
            "contribution_type": "roll_modifier",
            "result_type": "roll_modifier_set",
            "allowed_dependency_kinds": ["accessor", "derived"],
            "allowed_input_classes": ["ENGINE_STATE", "INVOCATION_ADJUDICATED"],
            "permitted_context_fact_ids": ["fiction.target_reachable"],
            "static_dependencies": [
                "accessor:health.bloodied",
                "derived:effect_availability",
            ],
            "combination_policy": "roll_advantage_cancellation_v1",
            "calculation_policy_id": CALCULATION_PROFILES[0],
            "calculation_policy_generation": 1,
        }
    )
    operation = selector["operation_contracts"]["rule.add_flat"]
    operation.update(
        {
            "value_kind": "roll_modifier",
            "normalization": "CANCEL_APPLICABLE_OPPOSITES",
            "constraints": ["stable_raw_dice_identity_and_contribution_provenance"],
            "calculation_policy_id": CALCULATION_PROFILES[0],
            "calculation_policy_generation": 1,
        }
    )
    for consumer_ref in (
        "selector:check.roll",
        "activity:activity.conformance.compiler",
    ):
        _append_once(
            mechanical["accessors"]["health.bloodied"]["permitted_consumer_ids"],
            consumer_ref,
        )
    _append_once(
        mechanical["accessors"]["health.current"]["permitted_consumer_ids"],
        "activity:activity.conformance.compiler",
    )
    _append_once(
        mechanical["derived_nodes"]["effect_availability"]["permitted_consumer_ids"],
        "selector:check.roll",
    )
    _append_once(
        mechanical["context_facts"]["fiction.target_reachable"][
            "permitted_consumer_ids"
        ],
        activity_id,
    )
    mechanical_path.write_text(json.dumps(mechanical), encoding="utf-8")

    ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
    )
    selector_ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    for entry in selector_ledger["entries"]:
        if (
            entry["id"] in {"check.roll", "damage.received"}
            and activity_id not in entry["consumer_or_dependency"]
        ):
            entry["consumer_or_dependency"] += f"; {activity_id}"
    ledger_path.write_text(json.dumps(selector_ledger), encoding="utf-8")

    if mutation == "missing_dependency":
        selector["static_dependencies"].append("accessor:health.missing")
    elif mutation == "cycle":
        mechanical["accessors"]["health.bloodied"]["dependencies"].append(
            "selector:check.roll"
        )
    elif mutation == "unauthorized_transitive":
        mechanical["accessors"]["health.bloodied"]["permitted_consumer_ids"] = [
            "accessor:accessor.test.unrelated"
        ]
    elif mutation == "incompatible_subject":
        mechanical["accessors"]["health.bloodied"]["subject_kinds"] = ["world.asset"]
    elif mutation == "incompatible_binding":
        selector["binding_kinds"] = ["ability_definition"]
    elif mutation in {"bare_accessor", "foreign_accessor"}:
        permission = (
            activity_id
            if mutation == "bare_accessor"
            else "activity:activity.test.foreign"
        )
        mechanical["accessors"]["health.current"]["permitted_consumer_ids"] = [
            "accessor:health.bloodied",
            permission,
        ]
    elif mutation == "wrong_accessor_consumer_kind":
        mechanical["accessors"]["health.current"]["permitted_consumer_ids"] = [
            "accessor:health.bloodied",
            f"predicate:{activity_id}",
        ]
    elif mutation == "unpaired_foreign_fact":
        selector["allowed_input_classes"] = ["ENGINE_STATE"]
        selector["permitted_context_fact_ids"] = []
        foreign_selector = mechanical["selectors"]["damage.received"]
        foreign_selector["allowed_input_classes"] = [
            "ENGINE_STATE",
            "INVOCATION_ADJUDICATED",
        ]
        foreign_selector["permitted_context_fact_ids"] = ["fiction.target_reachable"]
        for policy in declaration["calculation_policies"]:
            policy["reads"].append("selector:damage.received")
            policy["context_fact_bindings"] = [
                {
                    "consumer_ref": "selector:damage.received",
                    "fact_ids": ["fiction.target_reachable"],
                }
            ]
            policy["native_role_bindings"].append(
                {"read_ref": "selector:damage.received", "role_names": ["actor"]}
            )
        for symbol in declaration["symbols"].values():
            symbol["reads"].append("selector:damage.received")
    elif mutation == "orphan_policy_occurrence":
        declaration["calculation_policies"][0]["consumer_id"] = f"{activity_id}.step.99"
        declaration["profiles"].append(
            {
                "consumer_id": outer_consumer,
                "profile_id": CALCULATION_PROFILES[0],
                "profile_generation": 1,
            }
        )
    elif mutation == "duplicate_policy":
        declaration["calculation_policies"].append(
            json.loads(json.dumps(declaration["calculation_policies"][0]))
        )
    elif mutation == "generation_mismatch":
        declaration["calculation_policies"][0]["profile_generation"] = 2
    elif mutation == "pair_mismatch":
        declaration["calculation_policies"][0]["selector_operation_pairs"][0][
            "operation_ids"
        ] = ["rule.immunity"]
    elif mutation == "profile_mismatch":
        selector.update(
            {
                "contribution_type": "damage_defense",
                "result_type": "damage_result",
                "allowed_input_classes": ["ENGINE_STATE"],
                "permitted_context_fact_ids": [],
                "static_dependencies": [],
                "combination_policy": "damage_defense_source_ordered_v1",
                "calculation_policy_id": CALCULATION_PROFILES[1],
            }
        )
        operation.update(
            {
                "value_kind": "damage_defense",
                "normalization": "SOURCE_DEFINED_ORDER",
                "constraints": ["damage_type_origin_bypass_order_and_rounding"],
                "calculation_policy_id": CALCULATION_PROFILES[1],
            }
        )
    mechanical_path.write_text(json.dumps(mechanical), encoding="utf-8")
    roll_path.write_text(json.dumps(roll), encoding="utf-8")


def _installed_source_compiler_fixture(
    source_root: Path,
    installed_template: Path,
    destination: Path,
) -> Path:
    from DEV.TOOLS import validate_ruleset_package_closure as package_closure
    from GAME.TOOLS import ruleset_package

    package_id = "hdm.rules.dnd2024-srd52-core"
    package_root = source_root / "GAME/RULES/packages" / package_id
    manifest = ruleset_package.load_json_bytes(
        (package_root / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [package_root],
        root_package_ids=[package_id],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    engine_version = manifest["engine_requirement"]["engine_version"]
    ruleset_set_sha256 = lock["ruleset_set_sha256"]
    compiler_sha256 = package_closure.write_activity_compiler_contracts_projection(
        source_root,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )
    projection_path = source_root / "GAME/TOOLS/activity_compiler_contracts.json"
    projection_bytes = projection_path.read_bytes()
    assert package_closure.sha256(projection_bytes) == compiler_sha256
    inventory = package_closure.derive_engine_contract_inventory(
        source_root,
        engine_version=engine_version,
        ruleset_set_sha256=ruleset_set_sha256,
    )

    shutil.copytree(installed_template, destination)
    installed_projection = destination / "TOOLS/activity_compiler_contracts.json"
    installed_projection.write_bytes(projection_bytes)
    package_marker = destination / "RUNTIME_PACKAGE.yaml"
    marker = yaml.safe_load(package_marker.read_text(encoding="utf-8"))
    marker["activity_compiler_contracts_sha256"] = compiler_sha256
    marker["ruleset_engine_contract_inventory"] = inventory
    marker["ruleset_conformance_attestation"]["engine_contract_inventory_sha256"] = (
        inventory["inventory_sha256"]
    )
    package_marker.write_text(yaml.safe_dump(marker, sort_keys=False), encoding="utf-8")
    return destination


def _source_compiler_recipe() -> dict[str, object]:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    recipe = catalog_tests._nested_recipe()
    activity_id = str(recipe["id"])
    root_consumer = f"{activity_id}.step.0"
    nested_consumer = f"{activity_id}.step.1.steps.step.0"
    recipe["data"]["steps"][1]["args"]["targets"] = "compiled.targets"
    recipe["data"]["profile_bindings"] = [
        {
            "consumer_id": root_consumer,
            "profile_id": CALCULATION_PROFILES[0],
            "profile_generation": 1,
        },
        {
            "consumer_id": nested_consumer,
            "profile_id": CALCULATION_PROFILES[0],
            "profile_generation": 1,
        },
        {
            "consumer_id": nested_consumer,
            "profile_id": CAST_PROFILES[0],
            "profile_generation": 1,
        },
    ]
    return recipe


def _source_compiler_runtime(
    source_root: Path,
    installed_template: Path,
    destination: Path,
    *,
    mutation: str | None = None,
) -> Path:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    catalog_tests._stage_clean_source_tree(source_root)
    _prepare_sp03_source_tree(source_root, mutation)
    return _installed_source_compiler_fixture(
        source_root, installed_template, destination
    )


def test_authenticated_source_declarations_compile_nested_policy_and_cast_carriers(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root = _source_compiler_runtime(
        tmp_path / "source",
        conformance_runtime_root,
        tmp_path / "runtime",
    )
    recipe = _source_compiler_recipe()
    script = (
        catalog_tests._RECIPE_PROBE
        + """
root_consumer = identity + ".step.0"
nested_consumer = identity + ".step.1.steps.step.0"
policies = {item.binding.consumer_id: item for item in compiled.calculation_policy_bindings}
assert set(policies) == {root_consumer, nested_consumer}
assert all(item.binding.profile_id == "calculation.roll_advantage_srd521" for item in policies.values())
for item in policies.values():
    assert set(item.selector_contracts) == {"check.roll", "health.maximum"}
    assert set(item.accessor_contracts) == {"health.bloodied", "health.current", "health.maximum"}
    assert set(item.derived_node_contracts) == {"effect_availability"}
    assert set(item.context_fact_contracts) == {"fiction.target_reachable"}
    assert item.role_contracts["actor"]["family_key"] == "world.actor"
inner = compiled.instructions[1].children[0]
assert set(inner.read_contract_refs) >= {
    "selector:check.roll", "accessor:health.current", "fact:fiction.target_reachable",
    "accessor:health.bloodied", "accessor:health.maximum", "selector:health.maximum",
    "derived:effect_availability",
}
assert tuple(item.consumer_id for item in compiled.cast_profile_bindings) == (nested_consumer,)
record["data"]["profile_bindings"].clear()
assert policies[root_consumer].binding.consumer_id == root_consumer
assert policies[nested_consumer].context_fact_contracts["fiction.target_reachable"]["disposition"] == "ACTIVE_ADMITTED"
print(json.dumps({"policy_consumers": sorted(policies), "inner_reads": list(inner.read_contract_refs),
                  "cast_consumers": [item.consumer_id for item in compiled.cast_profile_bindings]}))
"""
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root, script, json.dumps(recipe), "{}"
    )
    assert result.returncode == 0, result.stderr or result.stdout
    evidence = json.loads(result.stdout)
    assert evidence["policy_consumers"] == [
        "activity.conformance.compiler.step.0",
        "activity.conformance.compiler.step.1.steps.step.0",
    ]
    assert "derived:effect_availability" in evidence["inner_reads"]
    assert evidence["cast_consumers"] == [
        "activity.conformance.compiler.step.1.steps.step.0"
    ]


@pytest.mark.parametrize(
    ("mutation", "diagnostic"),
    [
        ("bare_accessor", "string shape"),
        ("foreign_accessor", "unauthorized"),
        ("wrong_accessor_consumer_kind", "unauthorized"),
        ("missing_dependency", "unproven dependency"),
        ("cycle", "dependency cycle"),
        ("unauthorized_transitive", "unauthorized accessor edge"),
        ("incompatible_subject", "subject"),
        ("incompatible_binding", "subject"),
        ("unpaired_foreign_fact", "paired policy root"),
        ("orphan_policy_occurrence", "not retained by its exact compiled occurrence"),
        ("duplicate_policy", "duplicate array member"),
        ("generation_mismatch", "profile occurrence/generation is not admitted"),
        ("pair_mismatch", "unadmitted selector operation"),
        ("profile_mismatch", "foreign policy profile"),
        ("missing_profile_edge", "no exact profile binding"),
    ],
)
def test_authenticated_source_compiler_rejects_policy_closure_faults(
    conformance_runtime_root: Path,
    tmp_path: Path,
    mutation: str,
    diagnostic: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root = _source_compiler_runtime(
        tmp_path / "source",
        conformance_runtime_root,
        tmp_path / "runtime",
        mutation=mutation,
    )
    recipe = _source_compiler_recipe()
    if mutation == "missing_profile_edge":
        root_consumer = f"{recipe['id']}.step.0"
        recipe["data"]["profile_bindings"] = [
            binding
            for binding in recipe["data"]["profile_bindings"]
            if not (
                binding["consumer_id"] == root_consumer
                and binding["profile_id"] == CALCULATION_PROFILES[0]
            )
        ]
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        "{}",
    )
    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_schema_carries_four_finite_policy_profiles_and_no_open_payload_bag() -> None:
    profile_values = _schema("spell-native-profile-values.schema.json")
    mechanical = _schema("mechanical-surfaces.schema.json")
    compiler = _schema("activity-compiler-declaration.schema.json")

    assert "calculationPolicyBinding" in profile_values["$defs"]
    assert "castProfileBinding" in profile_values["$defs"]
    assert "castPreflightInput" in profile_values["$defs"]
    assert "contextFactBinding" in profile_values["$defs"]
    assert "nativeRoleBinding" in profile_values["$defs"]
    assert "calculation_policies" in compiler["properties"]
    assert "cast_profiles" in compiler["properties"]
    calculation_schema = profile_values["$defs"]["calculationPolicyBinding"]
    assert calculation_schema["properties"]["profile_id"]["$ref"].endswith(
        "#/$defs/calculationPolicyId"
    )
    assert set(profile_values["$defs"]["calculationPolicyId"]["enum"]) == set(
        CALCULATION_PROFILES
    )
    binding = _policy_binding()
    assert _accepts(
        profile_values,
        "#/$defs/calculationPolicyBinding",
        binding,
    )
    assert not _accepts(
        profile_values,
        "#/$defs/calculationPolicyBinding",
        {**binding, "permitted_context_fact_ids": ["fiction.anything"]},
    )
    assert not _accepts(
        profile_values,
        "#/$defs/calculationPolicyBinding",
        {**binding, "arguments": {"caller_selected_base": 13}},
    )

    selector_schema = mechanical["$defs"]["selectorMetadata"]
    assert "calculation_policy_id" in selector_schema["properties"]
    operation_schema = mechanical["$defs"]["operationContract"]
    assert "calculation_policy_id" in operation_schema["properties"]
    assert compiler["properties"]["calculation_policies"]["items"]["$ref"].endswith(
        "#/$defs/calculationPolicyBinding"
    )
    declaration = {
        "roles": {},
        "symbols": {},
        "profiles": [],
        "calculation_policies": [binding],
        "cast_profiles": [
            {
                "consumer_id": FIXTURE_CONSUMER_ID,
                "profile_id": CAST_PROFILES[0],
                "profile_generation": 1,
            }
        ],
    }
    activity_contracts._wire_contract("activity-compiler-declaration", declaration)
    with pytest.raises(activity_contracts.ActivityContractError):
        activity_contracts._wire_contract(
            "activity-compiler-declaration",
            {
                **declaration,
                "cast_profiles": [{**declaration["cast_profiles"][0], "open_args": {}}],
            },
        )


@pytest.mark.parametrize("profile_id", CALCULATION_PROFILES, ids=CALCULATION_PROFILES)
def test_each_selected_policy_has_a_closed_pair_contract(profile_id: str) -> None:
    schema = _schema("mechanical-surfaces.schema.json")
    metadata = _mechanical_policy_contract(profile_id)
    assert "calculation_policy_id" in schema["$defs"]["selectorMetadata"]["properties"]
    assert _accepts(schema, "#/$defs/selectorMetadata", metadata)
    unknown_pair = json.loads(json.dumps(metadata))
    unknown_pair["operation_contracts"][FIXTURE_OPERATION_ID]["untyped_arguments"] = {}
    assert not _accepts(schema, "#/$defs/selectorMetadata", unknown_pair)
    mismatched_profile = json.loads(json.dumps(metadata))
    mismatched_profile["combination_policy"] = "integer_additive_v1"
    assert not _accepts(schema, "#/$defs/selectorMetadata", mismatched_profile)


def test_cast_preflight_wire_contract_keeps_principal_origin_source_and_payer_distinct() -> (
    None
):
    values = _schema("spell-native-profile-values.schema.json")
    assert "castPreflightInput" in values["$defs"]
    cast_input = {
        "consumer_id": FIXTURE_CONSUMER_ID,
        "subject_binding": {
            "principal_subject_id": "actor.test.principal",
            "physical_actor_id": "actor.test.body",
            "binding_generation": 1,
        },
        "source_actor_id": "actor.test.source",
        "origin_subject_id": "actor.test.origin",
        "cost_payer_actor_id": "actor.test.payer",
        "acquisition_binding_ref": "acquisition.test.sp03",
        "component_owner_refs": [
            {"family_key": "world.asset", "identity": ["asset.test.focus"]}
        ],
        "target_bindings": [
            {
                "principal_subject_id": "actor.test.target",
                "physical_actor_id": "actor.test.target",
                "binding_generation": 1,
            }
        ],
        "slot_resource_definition_id": "resource.test.spell_slot",
    }
    assert _accepts(values, "#/$defs/castPreflightInput", cast_input)
    assert not _accepts(
        values,
        "#/$defs/castPreflightInput",
        {**cast_input, "remaining_slots": 1},
    )
    assert set(CAST_PROFILES) == set(values["$defs"]["castProfileId"]["enum"])


def test_compiler_retains_only_exact_permitted_policy_reads_and_occurrences() -> None:
    compile_bindings = getattr(
        activity_runtime, "_compile_calculation_policy_bindings", None
    )
    assert callable(compile_bindings), (
        "compiler must retain selected policy contracts in the exact consumer read plan"
    )
    from inspect import signature

    assert {"mechanical", "core", "ledger_rows", "role_contracts"} <= set(
        signature(compile_bindings).parameters
    )

    consumer_id = FIXTURE_CONSUMER_ID
    profile_id = CALCULATION_PROFILES[0]
    mechanical, core, ledger_rows, roles = _compiler_inputs(profile_id)
    profile_binding = activity_contracts.ProfileBinding(consumer_id, profile_id, 1)
    compiled = compile_bindings(
        (_policy_binding(profile_id, consumer_id=consumer_id),),
        consumer_id=consumer_id,
        activity_id=FIXTURE_ACTIVITY_ID,
        profile_bindings=(profile_binding,),
        mechanical=mechanical,
        core=core,
        ledger_rows=ledger_rows,
        role_contracts=roles,
    )

    assert len(compiled) == 1
    assert compiled[0].binding.consumer_id == consumer_id
    assert compiled[0].binding.profile_id == profile_id
    assert compiled[0].binding.selector_operation_pairs == (
        activity_contracts.SelectorOperationPair(
            FIXTURE_SELECTOR_ID, (FIXTURE_OPERATION_ID,)
        ),
    )
    retained_selector = compiled[0].selector_contracts[FIXTURE_SELECTOR_ID]
    assert retained_selector["calculation_policy_id"] == profile_id
    assert retained_selector["calculation_policy_generation"] == 1
    assert retained_selector["allowed_operations"] == (FIXTURE_OPERATION_ID,)
    assert retained_selector["static_dependencies"] == ()
    assert retained_selector["permitted_context_fact_ids"] == ()
    with pytest.raises(activity_runtime.ActivityRuntimeError, match="profile binding"):
        compile_bindings(
            (_policy_binding(profile_id, consumer_id=consumer_id),),
            consumer_id=consumer_id,
            activity_id=FIXTURE_ACTIVITY_ID,
            profile_bindings=(),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            role_contracts=roles,
        )
    with pytest.raises(
        activity_runtime.ActivityRuntimeError, match="array cardinality"
    ):
        compile_bindings(
            (_policy_binding(profile_id, consumer_id=consumer_id, native_roles=()),),
            consumer_id=consumer_id,
            activity_id=FIXTURE_ACTIVITY_ID,
            profile_bindings=(profile_binding,),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            role_contracts=roles,
        )
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="unadmitted selector operation"
    ):
        compile_bindings(
            (
                _policy_binding(
                    profile_id,
                    consumer_id=consumer_id,
                    operation_ids=("operation.not_in_fixture_contract",),
                ),
            ),
            consumer_id=consumer_id,
            activity_id=FIXTURE_ACTIVITY_ID,
            profile_bindings=(profile_binding,),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            role_contracts=roles,
        )
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="fact is unregistered"
    ):
        missing_fact_binding = _policy_binding(
            profile_id,
            consumer_id=consumer_id,
            reads=(f"selector:{FIXTURE_SELECTOR_ID}", "fact:fact.test.unadmitted"),
            fact_bindings=(
                {
                    "consumer_ref": f"selector:{FIXTURE_SELECTOR_ID}",
                    "fact_ids": ["fact.test.unadmitted"],
                },
            ),
        )
        compile_bindings(
            (missing_fact_binding,),
            consumer_id=consumer_id,
            activity_id=FIXTURE_ACTIVITY_ID,
            profile_bindings=(profile_binding,),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            role_contracts=roles,
        )


def test_compiler_retains_transitive_source_closure_and_exact_fact_path() -> None:
    binding, mechanical, core, ledger_rows, roles, profile_binding = (
        _transitive_policy_fixture()
    )
    compiled = _compile_transitive_fixture(
        binding, mechanical, core, ledger_rows, roles, profile_binding
    )
    assert len(compiled) == 1
    closure = compiled[0]
    assert closure.dependency_read_refs == (
        "accessor:accessor.test.bloodied",
        "accessor:accessor.test.maximum",
        "derived:derived.test.availability",
        "selector:selector.test.maximum",
    )
    assert set(closure.selector_contracts) == {
        FIXTURE_SELECTOR_ID,
        "selector.test.maximum",
    }
    assert set(closure.accessor_contracts) == {
        "accessor.test.bloodied",
        "accessor.test.current",
        "accessor.test.maximum",
    }
    assert set(closure.derived_node_contracts) == {"derived.test.availability"}
    assert set(closure.context_fact_contracts) == {"fiction.test.allowed"}
    assert closure.role_contracts == {
        "actor": {"family_key": "world.actor", "required": True}
    }
    retained_consumers = closure.accessor_contracts["accessor.test.current"][
        "permitted_consumer_ids"
    ]
    mechanical["accessors"]["accessor.test.current"]["permitted_consumer_ids"].append(
        "activity:activity.test.foreign"
    )
    assert (
        closure.accessor_contracts["accessor.test.current"]["permitted_consumer_ids"]
        == retained_consumers
    )
    with pytest.raises(TypeError):
        closure.accessor_contracts["accessor.test.current"]["source_class"] = "FORGED"


def test_accessor_consumer_permission_uses_only_owner_prefixed_reference() -> None:
    binding, mechanical, core, ledger_rows, roles, profile_binding = (
        _transitive_policy_fixture()
    )
    compiled = _compile_transitive_fixture(
        binding, mechanical, core, ledger_rows, roles, profile_binding
    )
    assert "accessor.test.current" in compiled[0].accessor_contracts

    binding, mechanical, core, ledger_rows, roles, profile_binding = (
        _transitive_policy_fixture(current_consumer_refs=(FIXTURE_ACTIVITY_ID,))
    )
    with pytest.raises(activity_runtime.ActivityRuntimeError, match="string shape"):
        _compile_transitive_fixture(
            binding, mechanical, core, ledger_rows, roles, profile_binding
        )

    for consumer_refs in (("activity:activity.test.other",), ()):
        binding, mechanical, core, ledger_rows, roles, profile_binding = (
            _transitive_policy_fixture(current_consumer_refs=consumer_refs)
        )
        with pytest.raises(
            activity_runtime.ActivityNotSelectable, match="unauthorized"
        ):
            _compile_transitive_fixture(
                binding, mechanical, core, ledger_rows, roles, profile_binding
            )


def test_compiler_rejects_missing_cyclic_unauthorized_and_incompatible_closure_edges() -> (
    None
):
    cases = (
        (
            lambda binding, mechanical: mechanical["accessors"][
                "accessor.test.bloodied"
            ].__setitem__("dependencies", ["accessor:accessor.test.missing"]),
            "unproven dependency",
        ),
        (
            lambda binding, mechanical: mechanical["accessors"][
                "accessor.test.bloodied"
            ].__setitem__("dependencies", [f"selector:{FIXTURE_SELECTOR_ID}"]),
            "dependency cycle",
        ),
        (
            lambda binding, mechanical: mechanical["accessors"][
                "accessor.test.bloodied"
            ].__setitem__("permitted_consumer_ids", ["accessor:accessor.test.other"]),
            "unauthorized accessor edge",
        ),
        (
            lambda binding, mechanical: mechanical["accessors"][
                "accessor.test.bloodied"
            ].__setitem__("subject_kinds", ["world.asset"]),
            "subject",
        ),
        (
            lambda binding, mechanical: mechanical["selectors"][
                FIXTURE_SELECTOR_ID
            ].__setitem__("binding_kinds", ["ability_definition"]),
            "subject",
        ),
    )
    for mutate, diagnostic in cases:
        binding, mechanical, core, ledger_rows, roles, profile_binding = (
            _transitive_policy_fixture()
        )
        mutate(binding, mechanical)
        with pytest.raises(activity_runtime.ActivityNotSelectable, match=diagnostic):
            _compile_transitive_fixture(
                binding, mechanical, core, ledger_rows, roles, profile_binding
            )
    binding, mechanical, core, ledger_rows, roles, profile_binding = (
        _transitive_policy_fixture()
    )
    binding["context_fact_bindings"] = [
        {
            "consumer_ref": "derived:derived.test.availability",
            "fact_ids": ["fiction.test.allowed"],
        }
    ]
    mechanical["derived_nodes"]["derived.test.availability"][
        "permitted_context_fact_ids"
    ] = []
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="exact path allowlist"
    ):
        _compile_transitive_fixture(
            binding, mechanical, core, ledger_rows, roles, profile_binding
        )


def test_unpaired_foreign_selector_cannot_lend_fact_permission() -> None:
    binding, mechanical, core, ledger_rows, roles, profile_binding = (
        _transitive_policy_fixture()
    )
    foreign_selector_id = "selector.test.foreign_damage"
    fact_id = "fiction.test.allowed"
    foreign = _mechanical_policy_contract(
        CALCULATION_PROFILES[1],
        fact_ids=(fact_id,),
        input_classes=("ENGINE_STATE", "INVOCATION_ADJUDICATED"),
    )
    mechanical["selectors"][foreign_selector_id] = foreign
    core["registries"]["rule_selectors"].append(foreign_selector_id)
    ledger_rows[("rule_selectors", foreign_selector_id)] = {
        "admission_disposition": "ACTIVE_ADMITTED",
        "realization_state": "COMPLETE",
        "consumer_or_dependency": FIXTURE_ACTIVITY_ID,
    }
    binding["reads"].append(f"selector:{foreign_selector_id}")
    binding["native_role_bindings"].append(
        {"read_ref": f"selector:{foreign_selector_id}", "role_names": ["actor"]}
    )
    binding["context_fact_bindings"] = [
        {"consumer_ref": f"selector:{foreign_selector_id}", "fact_ids": [fact_id]}
    ]
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="paired policy root"
    ):
        _compile_transitive_fixture(
            binding, mechanical, core, ledger_rows, roles, profile_binding
        )


def test_compiled_activity_has_distinct_calculation_and_cast_profile_carriers() -> None:
    from dataclasses import fields

    compiled_fields = {
        field.name for field in fields(activity_contracts.CompiledActivity)
    }
    assert "calculation_policy_bindings" in compiled_fields
    assert "cast_profile_bindings" in compiled_fields
    preflight = activity_contracts.CastPreflightInput(
        consumer_id=FIXTURE_CONSUMER_ID,
        subject_binding=activity_contracts.SubjectBinding(
            "actor.test.principal", "actor.test.body", 1
        ),
        source_actor_id="actor.test.source",
        origin_subject_id="actor.test.origin",
        cost_payer_actor_id="actor.test.payer",
        acquisition_binding_ref="acquisition.test.sp03",
        component_owner_refs=(
            activity_contracts.NativeOwnerRef("world.asset", ("asset.test.focus",)),
        ),
        target_bindings=(
            activity_contracts.SubjectBinding(
                "actor.test.target", "actor.test.target", 1
            ),
        ),
    )
    assert preflight.origin_subject_id != preflight.cost_payer_actor_id
    cast_binding = activity_contracts.CastProfileBinding(
        FIXTURE_CONSUMER_ID, CAST_PROFILES[0], 1
    )
    assert cast_binding.profile_id == CAST_PROFILES[0]
    with pytest.raises(activity_contracts.ActivityContractError):
        activity_contracts.CastProfileBinding(
            FIXTURE_CONSUMER_ID, CALCULATION_PROFILES[0], 1
        )


def test_cast_profile_source_binding_is_occurrence_exact() -> None:
    compile_cast_bindings = getattr(
        activity_runtime, "_compile_cast_profile_bindings", None
    )
    assert callable(compile_cast_bindings), (
        "compiler must retain exact common-cast source bindings"
    )
    consumer_id = FIXTURE_CONSUMER_ID
    raw = {
        "consumer_id": consumer_id,
        "profile_id": CAST_PROFILES[0],
        "profile_generation": 1,
    }
    binding = activity_contracts.ProfileBinding(consumer_id, CAST_PROFILES[0], 1)
    compiled = compile_cast_bindings(
        (raw,), profile_bindings=(binding,), occurrence_ids=(consumer_id,)
    )
    assert compiled == (
        activity_contracts.CastProfileBinding(consumer_id, CAST_PROFILES[0], 1),
    )
    assert (
        compile_cast_bindings(
            (), profile_bindings=(binding,), occurrence_ids=(consumer_id,)
        )
        == compiled
    )
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="foreign instruction"
    ):
        compile_cast_bindings((raw,), profile_bindings=(binding,), occurrence_ids=())
    with pytest.raises(
        activity_runtime.ActivityNotSelectable, match="exact Activity profile"
    ):
        compile_cast_bindings(
            (raw,), profile_bindings=(), occurrence_ids=(consumer_id,)
        )
