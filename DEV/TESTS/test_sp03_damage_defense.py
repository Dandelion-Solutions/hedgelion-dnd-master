"""Bounded source-compiled conformance for typed damage defense."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)
DAMAGE_INPUT_SYMBOLS = (
    "compiled.damage_full",
    "compiled.damage_half",
    "compiled.damage_bypassed",
    "compiled.damage_wrong_type",
    "compiled.damage_wrong_origin",
    "compiled.damage_mixed",
    "compiled.damage_group_peer",
    "compiled.damage_group_unbound",
    "compiled.damage_mixed_permuted",
    "compiled.damage_bypass_partition",
    "compiled.damage_origin_partition",
)
DAMAGE_INSTANCE_KEYS = (
    "damage.instance.primary",
    "damage.instance.primary",
    "damage.instance.bypassed",
    "damage.instance.wrong_type",
    "damage.instance.wrong_origin",
    "damage.instance.mixed",
    "damage.instance.secondary",
    "damage.instance.tertiary",
    "damage.instance.mixed_permuted",
    "damage.instance.bypass_partition",
    "damage.instance.origin_partition",
)
DAMAGE_GROUP_KEYS = (
    "damage.group.conformance",
    None,
    None,
    None,
    None,
    None,
    "damage.group.conformance",
    None,
    "damage.group.conformance",
    None,
    None,
)
DAMAGE_SOURCE_DEFINITION_KINDS = {
    "effect.sp03.damage.resistance": "definition.effect",
    "effect.sp03.damage.resistance_duplicate": "definition.effect",
    "effect.sp03.damage.vulnerability": "definition.effect",
    "effect.sp03.damage.vulnerability_duplicate": "definition.effect",
    "effect.sp03.damage.immunity": "definition.effect",
    "effect.sp03.damage.adjustment": "definition.effect",
    "effect.sp03.damage.resistance_wrong_type": "definition.effect",
    "effect.sp03.damage.resistance_wrong_origin": "definition.effect",
    "effect.sp03.damage.resistance_bypass": "definition.effect",
    "effect.sp03.damage.false_predicate": "definition.effect",
    "effect.sp03.damage.resistance_other_origin": "definition.effect",
    "asset.sp03.damage.resistance": "definition.asset",
}


def _damage_declaration() -> dict[str, object]:
    return {
        "roles": {"actor": "world.actor", "target": "world.actor"},
        "symbols": {},
        "profiles": [],
        "calculation_policies": [],
        "damage_input_bindings": [
            {
                "binding_id": "damage_input.primary",
                "consumer_id": "activity.conformance.compiler.step.2",
                "profile_id": "calculation.damage_defense_srd521",
                "profile_generation": 1,
                "selector_id": "damage.received",
                "components_symbol_id": "compiled.damage_full",
                "source_role": "actor",
                "recipient_role": "target",
                "instance_key": "damage.instance.primary",
                "simultaneous_group_key": "damage.group.conformance",
                "component_annotations": [
                    {
                        "source_component_ordinal": 0,
                        "origin_id": "origin.sp03.spell",
                        "bypass_ids": [],
                    }
                ],
            }
        ],
    }


def _schema_registry() -> Registry:
    registry = Registry()
    for path in (ROOT / "DEV/SCHEMAS").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            registry = registry.with_resource(
                schema["$id"], Resource.from_contents(schema)
            )
    return registry


def _damage_recipe(
    policy_indices: tuple[int, ...] | None = None,
) -> dict[str, object]:
    activity_id = "activity.conformance.damage"
    consumer_ids = tuple(
        f"{activity_id}.step.{index}" for index in range(len(DAMAGE_INPUT_SYMBOLS))
    )
    selected_consumer_ids = tuple(
        consumer_ids[index]
        for index in (
            tuple(range(len(consumer_ids)))
            if policy_indices is None
            else policy_indices
        )
    )
    return {
        "id": activity_id,
        "kind": "definition.activity",
        "data": {
            "family_id": "activity.spell_attack",
            "profile_bindings": [
                {
                    "consumer_id": consumer_id,
                    "profile_id": "calculation.damage_defense_srd521",
                    "profile_generation": 1,
                }
                for consumer_id in selected_consumer_ids
            ],
            "steps": [
                {
                    "op": "op.apply_damage",
                    "args": {
                        "target_role": "target",
                        "components": symbol_id,
                    },
                }
                for symbol_id in DAMAGE_INPUT_SYMBOLS
            ],
        },
    }


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _install_damage_compiler_source(
    source_root: Path,
    installed_template: Path,
    destination: Path,
    *,
    mutation: str | None = None,
    policy_indices: tuple[int, ...] | None = None,
) -> Path:
    import shutil

    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as policy_tests

    catalog_tests._stage_clean_source_tree(source_root)
    activity_id = "activity.conformance.damage"
    consumer_ids = tuple(
        f"{activity_id}.step.{index}" for index in range(len(DAMAGE_INPUT_SYMBOLS))
    )
    selected_indices = (
        tuple(range(len(consumer_ids))) if policy_indices is None else policy_indices
    )
    selected_consumer_ids = tuple(consumer_ids[index] for index in selected_indices)
    profile_id = "calculation.damage_defense_srd521"
    operation_ids = (
        "rule.add_flat",
        "rule.resistance",
        "rule.vulnerability",
        "rule.immunity",
    )
    contribution_types = {
        "rule.add_flat": "ADJUSTMENT",
        "rule.resistance": "RESISTANCE",
        "rule.vulnerability": "VULNERABILITY",
        "rule.immunity": "IMMUNITY",
    }

    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    apply_damage_path = primitive_root / "op.apply_damage.json"
    apply_damage = json.loads(apply_damage_path.read_text(encoding="utf-8"))
    declaration = apply_damage["contract"].setdefault("compiler_declarations", {})
    components_by_symbol = {
        "compiled.damage_full": [{"amount": 7, "damage_type_ref": "damage.fire"}],
        "compiled.damage_bypassed": [{"amount": 7, "damage_type_ref": "damage.fire"}],
        "compiled.damage_wrong_type": [{"amount": 7, "damage_type_ref": "damage.cold"}],
        "compiled.damage_wrong_origin": [
            {"amount": 7, "damage_type_ref": "damage.fire"}
        ],
        "compiled.damage_mixed": [
            {"amount": 7, "damage_type_ref": "damage.fire"},
            {"amount": 4, "damage_type_ref": "damage.cold"},
        ],
        "compiled.damage_mixed_permuted": [
            {"amount": 4, "damage_type_ref": "damage.cold"},
            {"amount": 7, "damage_type_ref": "damage.fire"},
        ],
        "compiled.damage_group_peer": [{"amount": 7, "damage_type_ref": "damage.fire"}],
        "compiled.damage_group_unbound": [
            {"amount": 7, "damage_type_ref": "damage.fire"}
        ],
        "compiled.damage_bypass_partition": [
            {"amount": 7, "damage_type_ref": "damage.fire"},
            {"amount": 7, "damage_type_ref": "damage.fire"},
        ],
        "compiled.damage_origin_partition": [
            {"amount": 7, "damage_type_ref": "damage.fire"},
            {"amount": 7, "damage_type_ref": "damage.fire"},
        ],
    }
    annotations_by_symbol = {
        "compiled.damage_full": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_half": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_bypassed": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": ["bypass.fire"],
            }
        ],
        "compiled.damage_wrong_type": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_wrong_origin": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.other",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_mixed": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
            {
                "source_component_ordinal": 1,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
        ],
        "compiled.damage_group_peer": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_group_unbound": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ],
        "compiled.damage_mixed_permuted": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
            {
                "source_component_ordinal": 1,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
        ],
        "compiled.damage_bypass_partition": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
            {
                "source_component_ordinal": 1,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": ["bypass.fire"],
            },
        ],
        "compiled.damage_origin_partition": [
            {
                "source_component_ordinal": 0,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            },
            {
                "source_component_ordinal": 1,
                "origin_id": "origin.sp03.other",
                "bypass_ids": [],
            },
        ],
    }
    if mutation == "boolean_component_amount":
        components_by_symbol["compiled.damage_full"][0]["amount"] = True
    elif mutation == "float_component_amount":
        components_by_symbol["compiled.damage_full"][0]["amount"] = 7.0
    elif mutation == "rich_component_symbol":
        components_by_symbol["compiled.damage_full"] = [
            {
                "amount": 7,
                "damage_type_id": "damage.fire",
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
        ]
    elif mutation == "unknown_component_member":
        components_by_symbol["compiled.damage_full"][0]["amount_source"] = "caller"
    elif mutation == "legacy_source_ref":
        components_by_symbol["compiled.damage_full"][0]["source_ref"] = "source.unbound"
    elif mutation == "duplicate_equivalent_components":
        components_by_symbol["compiled.damage_full"] = [
            copy.deepcopy(components_by_symbol["compiled.damage_full"][0]),
            copy.deepcopy(components_by_symbol["compiled.damage_full"][0]),
        ]
        duplicate_annotations = [
            {
                "source_component_ordinal": index,
                "origin_id": "origin.sp03.spell",
                "bypass_ids": [],
            }
            for index in (0, 1)
        ]
        annotations_by_symbol["compiled.damage_full"] = duplicate_annotations
        annotations_by_symbol["compiled.damage_half"] = copy.deepcopy(
            duplicate_annotations
        )
    symbol_occurrences = {
        "compiled.damage_full": [
            consumer_ids[0],
            consumer_ids[1],
            consumer_ids[6],
            consumer_ids[7],
        ],
        "compiled.damage_half": [consumer_ids[1]],
        **{
            symbol_id: [consumer_ids[index]]
            for index, symbol_id in enumerate(DAMAGE_INPUT_SYMBOLS)
            if symbol_id not in {"compiled.damage_full", "compiled.damage_half"}
        },
    }
    symbols: dict[str, object] = {}
    for symbol_id in DAMAGE_INPUT_SYMBOLS:
        if symbol_id == "compiled.damage_half":
            symbols[symbol_id] = {
                "value_kind": "damage_components",
                "cardinality": "single",
                "template": {
                    "kind": "HALF_DAMAGE_FLOOR_MIN_ZERO",
                    "source_symbol": "compiled.damage_full",
                    "input_contract": "SAME_FIXED_FULL_DAMAGE_RESULT",
                },
                "dependencies": ["compiled.damage_full"],
                "reads": [],
                "permitted_occurrence_ids": symbol_occurrences[symbol_id],
            }
        else:
            symbols[symbol_id] = {
                "value_kind": "damage_components",
                "cardinality": "single",
                "value": components_by_symbol[symbol_id],
                "dependencies": [],
                "reads": [],
                "permitted_occurrence_ids": symbol_occurrences[symbol_id],
            }
    if mutation == "rich_half_dependency":
        rich_dependency_id = "compiled.damage_full_rich"
        symbols[rich_dependency_id] = {
            "value_kind": "damage_components",
            "cardinality": "single",
            "value": [
                {
                    "amount": 7,
                    "damage_type_id": "damage.fire",
                    "origin_id": "origin.sp03.spell",
                    "bypass_ids": [],
                }
            ],
            "dependencies": [],
            "reads": [],
            "permitted_occurrence_ids": [consumer_ids[1]],
        }
        symbols["compiled.damage_half"]["template"]["source_symbol"] = (
            rich_dependency_id
        )
        symbols["compiled.damage_half"]["dependencies"] = [rich_dependency_id]
    declaration[activity_id] = {
        "roles": {"actor": "world.actor", "target": "world.actor"},
        "symbols": symbols,
        "profiles": [
            {
                "consumer_id": consumer_id,
                "profile_id": profile_id,
                "profile_generation": 1,
            }
            for consumer_id in selected_consumer_ids
        ],
        "calculation_policies": [
            {
                "consumer_id": consumer_id,
                "profile_id": profile_id,
                "profile_generation": 1,
                "reads": ["selector:damage.received"],
                "selector_operation_pairs": [
                    {
                        "selector_id": "damage.received",
                        "operation_ids": list(operation_ids),
                    }
                ],
                "context_fact_bindings": [],
                "native_role_bindings": [
                    {
                        "read_ref": "selector:damage.received",
                        "role_names": ["target"],
                    }
                ],
            }
            for consumer_id in selected_consumer_ids
        ],
        "damage_input_bindings": [
            {
                "binding_id": f"damage_input.{source_index}",
                "consumer_id": consumer_id,
                "profile_id": profile_id,
                "profile_generation": 1,
                "selector_id": "damage.received",
                "components_symbol_id": DAMAGE_INPUT_SYMBOLS[source_index],
                "component_annotations": annotations_by_symbol[
                    DAMAGE_INPUT_SYMBOLS[source_index]
                ],
                "source_role": "actor",
                "recipient_role": "target",
                "instance_key": DAMAGE_INSTANCE_KEYS[source_index],
                "simultaneous_group_key": DAMAGE_GROUP_KEYS[source_index],
            }
            for consumer_id, source_index in zip(
                selected_consumer_ids, selected_indices, strict=True
            )
        ],
    }
    if mutation == "wrong_recipient_role":
        declaration[activity_id]["damage_input_bindings"][0]["recipient_role"] = "actor"
    elif mutation == "wrong_components_symbol":
        declaration[activity_id]["damage_input_bindings"][0]["components_symbol_id"] = (
            "compiled.damage_unbound"
        )
    elif mutation == "wrong_half_dependency":
        declaration[activity_id]["symbols"]["compiled.damage_half"]["template"][
            "source_symbol"
        ] = "compiled.damage_unbound"
        declaration[activity_id]["symbols"]["compiled.damage_half"]["dependencies"] = [
            "compiled.damage_unbound"
        ]
    elif mutation == "binding_only":
        orphan_binding = copy.deepcopy(
            declaration[activity_id]["damage_input_bindings"][0]
        )
        orphan_binding.update(
            {
                "binding_id": "damage_input.unselected_sibling",
                "consumer_id": consumer_ids[1],
                "components_symbol_id": DAMAGE_INPUT_SYMBOLS[1],
                "component_annotations": annotations_by_symbol[DAMAGE_INPUT_SYMBOLS[1]],
            }
        )
        declaration[activity_id]["damage_input_bindings"].append(orphan_binding)
    elif mutation == "policy_only":
        declaration[activity_id]["damage_input_bindings"] = []
    elif mutation == "unbound_sibling":
        declaration[activity_id]["damage_input_bindings"] = [
            binding
            for binding in declaration[activity_id]["damage_input_bindings"]
            if binding["consumer_id"] != consumer_ids[1]
        ]
    elif mutation == "foreign_occurrence":
        declaration[activity_id]["damage_input_bindings"][0]["consumer_id"] = (
            "activity.foreign.damage.step.0"
        )
    elif mutation == "wrong_profile":
        declaration[activity_id]["damage_input_bindings"][0]["profile_id"] = (
            "calculation.roll_advantage_srd521"
        )
    elif mutation == "wrong_annotation_ordinal":
        declaration[activity_id]["damage_input_bindings"][0]["component_annotations"][
            0
        ]["source_component_ordinal"] = 1
    apply_damage_path.write_text(
        json.dumps(apply_damage, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    mechanical_path = source_root / "DEV/CATALOG/mechanical-surfaces.json"
    mechanical = json.loads(mechanical_path.read_text(encoding="utf-8"))
    selector = mechanical["selectors"]["damage.received"]
    selector.update(
        {
            "allowed_operations": list(operation_ids),
            "operation_contracts": {
                operation_id: {
                    "value_kind": "damage_defense",
                    "normalization": "SOURCE_DEFINED_ORDER",
                    "damage_contribution_type": contribution_types[operation_id],
                    "constraints": ["damage_type_origin_bypass_order_and_rounding"],
                    "calculation_policy_id": profile_id,
                    "calculation_policy_generation": 1,
                }
                for operation_id in operation_ids
            },
            "contribution_type": "damage_defense",
            "result_type": "damage_result",
            "combination_policy": "damage_defense_source_ordered_v1",
            "calculation_policy_id": profile_id,
            "calculation_policy_generation": 1,
            "allowed_input_classes": ["ENGINE_STATE"],
            "permitted_context_fact_ids": [],
            "static_dependencies": [],
        }
    )
    _write_json(mechanical_path, mechanical)

    selector_ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
    )
    selector_ledger = json.loads(selector_ledger_path.read_text(encoding="utf-8"))
    damage_selector = next(
        row for row in selector_ledger["entries"] if row["id"] == "damage.received"
    )
    if activity_id not in damage_selector["consumer_or_dependency"]:
        damage_selector["consumer_or_dependency"] += f"; {activity_id}"
    _write_json(selector_ledger_path, selector_ledger)

    operation_ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_operations.json"
    )
    operation_ledger = json.loads(operation_ledger_path.read_text(encoding="utf-8"))
    for operation_id in operation_ids:
        row = next(
            item for item in operation_ledger["entries"] if item["id"] == operation_id
        )
        if operation_id in {"rule.resistance", "rule.vulnerability"}:
            row.update(
                {
                    "realization_state": "COMPLETE",
                    "downstream_owner": None,
                    "admission_disposition": "ACTIVE_ADMITTED",
                    "evidence_class": "ISOLATED_CONFORMANCE_ONLY",
                    "evidence_citation": (
                        "SP03 exact damage.received pair in isolated source only"
                    ),
                    "consumer_or_dependency": (
                        "activity.conformance.damage damage.received only in isolated source"
                    ),
                    "activation_trigger": (
                        "ISOLATED_SP03_SOURCE_COMPILER_CONFORMANCE_ONLY"
                    ),
                }
            )
        elif activity_id not in row["consumer_or_dependency"]:
            row["consumer_or_dependency"] += f"; {activity_id} isolated conformance"
    operation_ledger["registry_census"]["admitted"] += 2
    operation_ledger["registry_census"]["dormant_nonselectable"] -= 2
    _write_json(operation_ledger_path, operation_ledger)

    package_seed_path = (
        source_root
        / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
    )
    package_seed = json.loads(package_seed_path.read_text(encoding="utf-8"))
    support = package_seed["support_definitions"]
    effect_template = next(
        row for row in support if row["id"] == "effect.innate_sorcery"
    )
    asset_template = next(row for row in support if row["id"] == "asset.arcane_focus")
    matching = {"damage_type_ids": ["damage.fire"], "origin_ids": ["origin.sp03.spell"]}
    effect_rule_values = {
        "effect.sp03.damage.resistance": (
            "rule.resistance",
            {**matching, "bypass_id": "bypass.fire"},
        ),
        "effect.sp03.damage.resistance_duplicate": (
            "rule.resistance",
            {**matching, "bypass_id": "bypass.fire"},
        ),
        "effect.sp03.damage.vulnerability": (
            "rule.vulnerability",
            {**matching, "bypass_id": "bypass.vulnerability"},
        ),
        "effect.sp03.damage.vulnerability_duplicate": (
            "rule.vulnerability",
            {**matching, "bypass_id": "bypass.vulnerability"},
        ),
        "effect.sp03.damage.immunity": (
            "rule.immunity",
            {**matching, "bypass_id": "bypass.immunity"},
        ),
        "effect.sp03.damage.adjustment": (
            "rule.add_flat",
            {**matching, "bypass_id": "bypass.adjustment", "amount": -1},
        ),
        "effect.sp03.damage.resistance_wrong_type": (
            "rule.resistance",
            {
                "damage_type_ids": ["damage.cold"],
                "origin_ids": ["origin.sp03.spell"],
                "bypass_id": "bypass.cold",
            },
        ),
        "effect.sp03.damage.resistance_wrong_origin": (
            "rule.resistance",
            {
                "damage_type_ids": ["damage.fire"],
                "origin_ids": ["origin.sp03.other"],
                "bypass_id": "bypass.other_origin",
            },
        ),
        "effect.sp03.damage.resistance_bypass": (
            "rule.resistance",
            {**matching, "bypass_id": "bypass.fire"},
        ),
        "effect.sp03.damage.false_predicate": (
            "rule.resistance",
            {**matching, "bypass_id": "bypass.false_predicate"},
        ),
        "effect.sp03.damage.resistance_other_origin": (
            "rule.resistance",
            {
                "damage_type_ids": ["damage.fire"],
                "origin_ids": ["origin.sp03.other"],
                "bypass_id": "bypass.other_origin",
            },
        ),
    }
    for definition_id, (operation_id, value) in effect_rule_values.items():
        effect_definition = copy.deepcopy(effect_template)
        effect_definition["id"] = definition_id
        rule_element = {
            "selector": "damage.received",
            "operation_id": operation_id,
            "value": value,
        }
        if definition_id == "effect.sp03.damage.false_predicate":
            rule_element["predicate"] = {
                "compare": {
                    "left": 1,
                    "operator": "eq",
                    "right": 0,
                }
            }
        effect_definition["data"]["rule_elements"] = [rule_element]
        support.append(effect_definition)
    if mutation in {
        "boolean_adjustment_amount",
        "float_adjustment_amount",
        "unknown_adjustment_member",
        "unpaired_damage_operation",
        "rule_element_gate",
        "rule_element_priority",
        "rule_element_stacking_key",
    }:
        adjustment_source = next(
            row for row in support if row["id"] == "effect.sp03.damage.adjustment"
        )
        adjustment_element = adjustment_source["data"]["rule_elements"][0]
        adjustment_value = adjustment_element["value"]
        if mutation == "boolean_adjustment_amount":
            adjustment_value["amount"] = True
        elif mutation == "float_adjustment_amount":
            adjustment_value["amount"] = 1.0
        elif mutation == "unknown_adjustment_member":
            adjustment_value["arbitrary"] = "not permitted"
        elif mutation == "unpaired_damage_operation":
            adjustment_element["operation_id"] = "rule.grant_disadvantage"
        elif mutation == "rule_element_gate":
            adjustment_element["gate"] = {"resource_ref": "resource.unsupported"}
        elif mutation == "rule_element_priority":
            adjustment_element["priority"] = 1
        elif mutation == "rule_element_stacking_key":
            adjustment_element["stacking_key"] = "stack.unsupported"
    asset_definition = copy.deepcopy(asset_template)
    asset_definition["id"] = "asset.sp03.damage.resistance"
    asset_definition["data"]["rule_elements"] = [
        {
            "selector": "damage.received",
            "operation_id": "rule.resistance",
            "value": {**matching, "bypass_id": "bypass.fire"},
        }
    ]
    support.append(asset_definition)
    _write_json(package_seed_path, package_seed)

    runtime_root = policy_tests._installed_source_compiler_fixture(
        source_root, installed_template, destination
    )
    runtime_seed = (
        runtime_root
        / "RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
    )
    shutil.copy2(package_seed_path, runtime_seed)
    return runtime_root


def _damage_compiler_runtime(
    source_root: Path,
    installed_template: Path,
    destination: Path,
    *,
    mutation: str | None = None,
    policy_indices: tuple[int, ...] | None = None,
) -> Path:
    import yaml

    from GAME.TOOLS import ruleset_package

    runtime_root = _install_damage_compiler_source(
        source_root,
        installed_template,
        destination,
        mutation=mutation,
        policy_indices=policy_indices,
    )
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
    marker_path = runtime_root / "RUNTIME_PACKAGE.yaml"
    marker = yaml.safe_load(marker_path.read_text(encoding="utf-8"))
    marker["ruleset_set_sha256"] = lock["ruleset_set_sha256"]
    marker["resolved_ruleset_lock"] = lock
    marker_path.write_text(yaml.safe_dump(marker, sort_keys=False), encoding="utf-8")
    return runtime_root


def test_compiler_declaration_closes_damage_input_to_exact_consumer_and_source() -> (
    None
):
    schema = json.loads(
        (ROOT / "DEV/SCHEMAS/activity-compiler-declaration.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema, registry=_schema_registry()).validate(
        _damage_declaration()
    )


def test_damage_input_binding_schema_rejects_generic_or_foreign_authority() -> None:
    schema = json.loads(
        (ROOT / "DEV/SCHEMAS/activity-compiler-declaration.schema.json").read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(schema, registry=_schema_registry())
    invalid_mutations = (
        lambda binding: binding.update(untyped_arguments={"amount": 7}),
        lambda binding: binding.update(profile_id="calculation.roll_advantage_srd521"),
        lambda binding: binding.update(profile_generation=True),
        lambda binding: binding.update(components_symbol_id="caller.damage"),
        lambda binding: binding.update(source_role="source role"),
        lambda binding: binding.update(simultaneous_group_key=7),
    )
    for mutate in invalid_mutations:
        declaration = _damage_declaration()
        mutate(declaration["damage_input_bindings"][0])
        assert not validator.is_valid(declaration)

    declaration = _damage_declaration()
    declaration["damage_input_bindings"][0]["unowned_member"] = True
    assert not validator.is_valid(declaration)


def test_generic_damage_components_remains_legacy_only() -> None:
    from GAME.TOOLS import structural_contracts

    legacy = [{"amount": 7, "damage_type_ref": "damage.fire"}]
    rich = [
        {
            "amount": 7,
            "damage_type_id": "damage.fire",
            "origin_id": "origin.sp03.spell",
            "bypass_ids": [],
        }
    ]
    with pytest.raises(structural_contracts.StructuralContractError):
        structural_contracts.validate_contract(
            "typed_export_value",
            {"value_kind": "damage_components", "value": rich},
        )
    structural_contracts.validate_contract(
        "typed_export_value", {"value_kind": "damage_components", "value": legacy}
    )
    with pytest.raises(structural_contracts.StructuralContractError):
        structural_contracts.validate_contract(
            "arguments:op.apply_damage",
            {"target_role": "target", "components": rich},
        )
    structural_contracts.validate_contract(
        "arguments:op.apply_damage",
        {"target_role": "target", "components": legacy},
    )


def test_installed_compiler_retains_exact_damage_symbol_consumer_and_roles(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
    )
    script = (
        catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
        + r"""
from GAME.TOOLS import activity_contracts as contracts
from GAME.TOOLS import calculation
from GAME.TOOLS import mechanical_context
consumer = "activity.conformance.damage.step.0"
assert len(compiled.damage_input_bindings) == 11
assert all(
    type(binding) is contracts.CompiledDamageInputBinding
    for binding in compiled.damage_input_bindings
)
binding = compiled.damage_input_bindings[0]
assert binding.consumer_id == consumer
assert binding.profile_id == "calculation.damage_defense_srd521"
assert binding.selector_id == "damage.received"
assert binding.components_symbol_id == "compiled.damage_full"
assert binding.source_role == "actor" and binding.recipient_role == "target"
assert binding.instance_key == "damage.instance.primary"
assert binding.simultaneous_group_key == "damage.group.conformance"
assert compiled.instructions[0].primitive_id == "op.apply_damage"
assert compiled.instructions[0].arguments["components"] == {
    "symbol_ref": "compiled.damage_full",
    "value_kind": "damage_components",
}
half_binding = compiled.damage_input_bindings[1]
assert half_binding.consumer_id == "activity.conformance.damage.step.1"
assert half_binding.components_symbol_id == "compiled.damage_half"
assert half_binding.simultaneous_group_key is None
assert compiled.instructions[1].arguments["components"] == {
    "symbol_ref": "compiled.damage_half",
    "value_kind": "damage_components",
}
component = compiled.symbol_contracts["compiled.damage_full"]["value"][0]
assert dict(component) == {"amount": 7, "damage_type_ref": "damage.fire"}
assert tuple(
    (
        annotation.source_component_ordinal,
        annotation.origin_id,
        annotation.bypass_ids,
    )
    for annotation in binding.component_annotations
) == ((0, "origin.sp03.spell", ()),)
assert calculation._damage_input_binding_wire(binding)["component_annotations"] == [
    {
        "source_component_ordinal": 0,
        "origin_id": "origin.sp03.spell",
        "bypass_ids": [],
    }
]
assert tuple(
    (
        annotation.source_component_ordinal,
        annotation.origin_id,
        annotation.bypass_ids,
    )
    for annotation in half_binding.component_annotations
) == ((0, "origin.sp03.spell", ()),)
assert compiled.symbol_contracts["compiled.damage_half"]["template"] == {
    "kind": "HALF_DAMAGE_FLOOR_MIN_ZERO",
    "source_symbol": "compiled.damage_full",
    "input_contract": "SAME_FIXED_FULL_DAMAGE_RESULT",
}
policy = next(
    item
    for item in compiled.calculation_policy_bindings
    if item.binding.consumer_id == consumer
)
operation_contract = policy.selector_contracts["damage.received"]["operation_contracts"]["rule.add_flat"]
invalid_values = (
    {"amount": True, "damage_type_ids": ["damage.fire"], "origin_ids": ["origin.sp03.spell"], "bypass_id": "bypass.adjustment"},
    {"amount": 1.0, "damage_type_ids": ["damage.fire"], "origin_ids": ["origin.sp03.spell"], "bypass_id": "bypass.adjustment"},
    {"amount": 1, "damage_type_ids": ["damage.fire"], "origin_ids": ["origin.sp03.spell"], "bypass_id": "bypass.adjustment", "unknown": True},
)
rejected_values = 0
for invalid_value in invalid_values:
    try:
        mechanical_context._closed_operation_value("rule.add_flat", operation_contract, invalid_value)
    except mechanical_context.MechanicalContextError:
        rejected_values += 1
assert rejected_values == len(invalid_values)
print(json.dumps({"binding": binding.binding_id, "consumer": binding.consumer_id, "rejected_values": rejected_values}))
"""
    )
    result = selector_tests._game_runtime_probe(
        runtime_root, script, json.dumps(_damage_recipe()), "{}"
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "binding": "damage_input.0",
        "consumer": "activity.conformance.damage.step.0",
        "rejected_values": 3,
    }


@pytest.mark.parametrize(
    ("mutation", "policy_indices", "diagnostic"),
    (
        ("boolean_component_amount", None, "typed_export_value is not admitted"),
        ("float_component_amount", None, "typed_export_value is not admitted"),
        ("unknown_component_member", None, "typed_export_value is not admitted"),
        (
            "legacy_source_ref",
            None,
            "legacy damage source_ref has no selected damage-binding mapping",
        ),
        ("wrong_recipient_role", None, "damage recipient role differs"),
        (
            "wrong_components_symbol",
            None,
            "differs from its compiled components symbol",
        ),
        ("wrong_half_dependency", None, "compiled.damage_unbound"),
        (
            "binding_only",
            (0,),
            "damage policy consumers need one exact source input binding each",
        ),
        (
            "policy_only",
            (0,),
            "damage policy consumers need one exact source input binding each",
        ),
        (
            "unbound_sibling",
            (0, 1),
            "damage policy consumers need one exact source input binding each",
        ),
        ("foreign_occurrence", None, "damage input binding is duplicated, foreign"),
        ("wrong_profile", None, "activity-compiler-declaration is not admitted"),
        (
            "wrong_annotation_ordinal",
            None,
            "damage annotations do not bind each source component exactly once",
        ),
        ("rich_component_symbol", (), "typed_export_value is not admitted"),
        ("rich_half_dependency", (1,), "typed_export_value is not admitted"),
        ("boolean_adjustment_amount", None, "damage Rule Element value is not closed"),
        ("float_adjustment_amount", None, "damage Rule Element value is not closed"),
        ("unknown_adjustment_member", None, "damage Rule Element value is not closed"),
        ("unpaired_damage_operation", None, "damage source has an unpaired operation"),
        ("rule_element_gate", None, "damage Rule Element has unsupported members"),
        ("rule_element_priority", None, "damage Rule Element has unsupported members"),
        (
            "rule_element_stacking_key",
            None,
            "damage Rule Element has unsupported members",
        ),
    ),
)
def test_installed_compiler_cold_rejects_damage_source_and_binding_mutations(
    installed_runtime_root: Path,
    tmp_path: Path,
    mutation: str,
    policy_indices: tuple[int, ...] | None,
    diagnostic: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
        mutation=mutation,
        policy_indices=policy_indices,
    )
    result = selector_tests._game_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS."),
        json.dumps(_damage_recipe(policy_indices=policy_indices)),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
    )
    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_damage_compiler_rejects_amount_supplied_as_direct_activity_argument(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
        policy_indices=(),
    )
    recipe = _damage_recipe(policy_indices=())
    recipe["data"]["steps"][0]["args"]["components"] = [
        {
            "amount": 99,
            "damage_type_id": "damage.fire",
            "origin_id": "origin.caller",
            "bypass_ids": [],
        }
    ]
    result = selector_tests._game_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS."),
        json.dumps(recipe),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
    )
    assert result.returncode != 0
    assert "closed union does not match" in result.stderr


@pytest.mark.parametrize(
    ("policy_index", "duplicate_source_symbol"),
    ((0, "compiled.damage_full"), (1, "compiled.damage_full")),
    ids=("literal", "dependent-half-template"),
)
def test_compiler_rejects_ambiguous_same_type_components_before_rounding(
    installed_runtime_root: Path,
    tmp_path: Path,
    policy_index: int,
    duplicate_source_symbol: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
        mutation="duplicate_equivalent_components",
        policy_indices=(policy_index,),
    )
    recipe = _damage_recipe(policy_indices=(policy_index,))
    result = selector_tests._game_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS."),
        json.dumps(recipe),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
    )
    assert result.returncode != 0
    assert "ambiguous repeated same-type/origin/bypass" in result.stderr
    assert duplicate_source_symbol in result.stderr


def test_issued_compiled_literal_damage_input_produces_preparation_only_result(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
    )
    compiler_probe = catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
    script = (
        compiler_probe
        + r"""
import copy
import json
import tempfile
from pathlib import Path

from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
from DEV.TESTS.test_sp03_native_membership import (
    ACTOR_ID,
    CAMPAIGN_ID,
    GitCampaignRepository,
    _actor_record,
    _write_routed,
)
from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
from GAME.TOOLS import activity_contracts as contracts
from GAME.TOOLS import calculation
from GAME.TOOLS.hot_store import NativeHotStore
from GAME.TOOLS.runtime_execution import accept_command

proposal = _proposal(compiled.activity_id)
proposal["action_request"]["actor_id"] = ACTOR_ID
proposal["action_request"]["target_ids"] = ["actor.target"]
accepted = accept_command(
    _interpreter_result(),
    catalog.catalog_context,
    {"definition_id": compiled.activity_id, "kind": "definition.activity"},
    proposal,
)

with tempfile.TemporaryDirectory(prefix="sp03-damage-input-") as temporary:
    repository = GitCampaignRepository(Path(temporary) / "campaign.git")
    repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
    repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
    repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
    _write_routed(repository, "world.actor", _actor_record())
    target = copy.deepcopy(_actor_record())
    target["id"] = "actor.target"
    _write_routed(repository, "world.actor", target)
    repository.commit("seed bounded damage preparation source")

    resolution = {
        "root_command_id": accepted["command_id"],
        "initiating_command_id": accepted["command_id"],
        "activity_id": compiled.activity_id,
        "actor_id": ACTOR_ID,
        "target_ids": accepted["action_request"]["target_ids"],
        "parameter_bindings": accepted["action_request"].get("parameter_bindings", {}),
        "ruleset_set_digest_generation": 1,
        "ruleset_set_sha256": compiled.ruleset_set_sha256,
        "catalog_context_fingerprint_generation": 1,
        "catalog_context_fingerprint": catalog.catalog_context.fingerprint,
        "status": "RUNNING",
        "next_segment_sequence": 1,
        "invocation_facts": [],
        "fixed_rng_results": [],
        "prior_step_exports": {},
        "child_resolution_ids": [],
        "segments": [],
    }
    _write_routed(
        repository,
        "runtime.command",
        {"kind": "runtime.command", "id": accepted["command_id"], **accepted},
    )
    _write_routed(
        repository,
        "runtime.resolution",
        {
            "kind": "runtime.resolution",
            "id": accepted["root_resolution_id"],
            "campaign_id": CAMPAIGN_ID,
            **resolution,
        },
    )
    repository.commit("seed authentic accepted root for preparation only")
    revision_before = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()

    with NativeHotStore(":memory:") as store:
        host, _source = _selected_host(store, repository=repository)
        try:
            context = host._current_owner._prepare_root_context(
                catalog,
                compiled,
                command_id=accepted["command_id"],
                consumer_id="activity.conformance.damage.step.0",
            )
            assert contracts._preparation_context_is_issued(context)
            full = calculation.calculate_selector(context, "damage.received")
            half_context = host._current_owner._prepare_root_context(
                catalog,
                compiled,
                command_id=accepted["command_id"],
                consumer_id="activity.conformance.damage.step.1",
            )
            assert contracts._preparation_context_is_issued(half_context)
            half = calculation.calculate_selector(
                half_context, "damage.received"
            )
        except calculation.CalculationError as error:
            evidence = {"status": "UNREALIZED", "error": str(error)}
        else:
            evidence = {"status": "OK", "full": full, "half": half}

    revision_after = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
    print(json.dumps({**evidence, "revision_before": revision_before, "revision_after": revision_after}, sort_keys=True))
"""
    )
    result = selector_tests._game_runtime_probe(
        runtime_root, script, json.dumps(_damage_recipe()), "{}"
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["status"] == "OK", evidence
    for result in (evidence["full"], evidence["half"]):
        assert result["selector_id"] == "damage.received"
        assert result["rng_draw_count"] == 0
        assert result["fixed_roll_refs"] == []
    assert evidence["full"]["total_damage"] == 7
    assert evidence["full"]["component_results"][0]["received_amount"] == 7
    assert evidence["half"]["total_damage"] == 3
    assert evidence["half"]["component_results"][0]["received_amount"] == 3
    assert evidence["full"]["amount_basis"]["kind"] == "SOURCE_LITERAL"
    assert evidence["half"]["amount_basis"]["kind"] == "HALF_DAMAGE_FLOOR_MIN_ZERO"
    assert evidence["full"]["logical_identity"]["consumer_id"].endswith("step.0")
    assert evidence["half"]["logical_identity"]["consumer_id"].endswith("step.1")
    assert (
        evidence["full"]["logical_identity"]["instance_key"]
        == (evidence["half"]["logical_identity"]["instance_key"])
    )
    assert evidence["full"]["logical_identity"]["simultaneous_group_key"] == (
        "damage.group.conformance"
    )
    assert evidence["half"]["logical_identity"]["simultaneous_group_key"] is None
    assert "damage_instance_id" not in evidence["full"]
    assert evidence["revision_before"] == evidence["revision_after"]


def _damage_cases_script(compiler_probe: str) -> str:
    return (
        compiler_probe
        + r"""
import copy
import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

from DEV.TESTS.test_rd05_runtime_execution import _interpreter_result, _proposal
from DEV.TESTS.test_sp03_native_membership import (
    ACTOR_ID,
    CAMPAIGN_ID,
    GitCampaignRepository,
    _actor_record,
    _asset,
    _effect,
    _write_routed,
)
from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
from GAME.TOOLS import activity_contracts as contracts
from GAME.TOOLS import calculation
from GAME.TOOLS.hot_store import NativeHotStore
from GAME.TOOLS.runtime_execution import accept_command

cases = json.loads(sys.argv[4])
# The caller's original Activity object is no longer an input authority after
# compilation; the sealed compiled symbol and argument remain source-exact.
record["data"]["steps"][0]["args"]["components"] = "compiled.damage_bypassed"
assert compiled.instructions[0].arguments["components"]["symbol_ref"] == "compiled.damage_full"
assert compiled.symbol_contracts["compiled.damage_full"]["value"][0]["amount"] == 7
try:
    compiled.symbol_contracts["compiled.damage_full"]["value"][0]["amount"] = 99
except TypeError:
    pass
else:
    raise AssertionError("compiled damage literal is not frozen")
proposal = _proposal(compiled.activity_id)
proposal["action_request"]["actor_id"] = ACTOR_ID
proposal["action_request"]["target_ids"] = ["actor.target"]
accepted = accept_command(
    _interpreter_result(),
    catalog.catalog_context,
    {"definition_id": compiled.activity_id, "kind": "definition.activity"},
    proposal,
)

def run_case(case):
    with tempfile.TemporaryDirectory(prefix="sp03-damage-defense-") as temporary:
        repository = GitCampaignRepository(Path(temporary) / "campaign.git")
        repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
        repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
        repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
        _write_routed(repository, "world.actor", _actor_record())
        target = copy.deepcopy(_actor_record())
        target["id"] = "actor.target"
        _write_routed(repository, "world.actor", target)
        for index, definition_id in enumerate(case["effects"]):
            effect = _effect(f"effect.damage.case.{index}", "actor.target")
            effect["definition_id"] = definition_id
            effect["state"]["source_id"] = ACTOR_ID
            _write_routed(repository, "world.effect", effect)
        for index, definition_id in enumerate(case["assets"]):
            asset = _asset(
                f"asset.damage.case.{index}",
                owner="actor.target",
                equipment=case.get("asset_equipment", "worn"),
            )
            asset["definition_id"] = definition_id
            _write_routed(repository, "world.asset", asset)
        repository.commit("seed source-backed damage defense membership")

        resolution = {
            "root_command_id": accepted["command_id"],
            "initiating_command_id": accepted["command_id"],
            "activity_id": compiled.activity_id,
            "actor_id": ACTOR_ID,
            "target_ids": accepted["action_request"]["target_ids"],
            "parameter_bindings": accepted["action_request"].get("parameter_bindings", {}),
            "ruleset_set_digest_generation": 1,
            "ruleset_set_sha256": compiled.ruleset_set_sha256,
            "catalog_context_fingerprint_generation": 1,
            "catalog_context_fingerprint": catalog.catalog_context.fingerprint,
            "status": "RUNNING",
            "next_segment_sequence": 1,
            "invocation_facts": [],
            "fixed_rng_results": [],
            "prior_step_exports": {},
            "child_resolution_ids": [],
            "segments": [],
        }
        _write_routed(
            repository,
            "runtime.command",
            {"kind": "runtime.command", "id": accepted["command_id"], **accepted},
        )
        _write_routed(
            repository,
            "runtime.resolution",
            {
                "kind": "runtime.resolution",
                "id": accepted["root_resolution_id"],
                "campaign_id": CAMPAIGN_ID,
                **resolution,
            },
        )
        repository.commit("seed authentic accepted root for preparation only")
        revision_before = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
        revision_after_change = revision_before
        if "consumer_indices" in case:
            grouped_results = []
            with NativeHotStore(":memory:") as store:
                host, _source = _selected_host(store, repository=repository)
                for consumer_index in case["consumer_indices"]:
                    context = host._current_owner._prepare_root_context(
                        catalog,
                        compiled,
                        command_id=accepted["command_id"],
                        consumer_id=f"{compiled.activity_id}.step.{consumer_index}",
                    )
                    if not contracts._preparation_context_is_issued(context):
                        raise AssertionError("grouped damage context was not issued")
                    grouped_results.append(
                        calculation.calculate_selector(context, "damage.received")
                    )
            revision_after = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
            return {
                "status": "OK",
                "results": grouped_results,
                "revision_before": revision_before,
                "revision_after_change": revision_after_change,
                "revision_after": revision_after,
            }
        consumer_id = f"{compiled.activity_id}.step.{case['consumer_index']}"

        with NativeHotStore(":memory:") as store:
            host, _source = _selected_host(store, repository=repository)
            context = host._current_owner._prepare_root_context(
                catalog,
                compiled,
                command_id=accepted["command_id"],
                consumer_id=consumer_id,
            )
            if not contracts._preparation_context_is_issued(context):
                raise AssertionError("damage calculation context was not issued")
            runtime_partition_status = None
            if case.get("runtime_partition_probe"):
                damage_binding = calculation._issued_damage_input_binding(context)
                full_components, _amount_basis = calculation._source_damage_components(
                    context, damage_binding
                )
                try:
                    calculation._validate_damage_components(
                        context, tuple(full_components) + tuple(full_components)
                    )
                except contracts.NativePreparationHold as hold:
                    runtime_partition_status = hold.operation_status
                else:
                    runtime_partition_status = "AMBIGUOUS_PARTITION_ACCEPTED"
            if (
                context.fixed_roll_refs
                or context.resolution.get("fixed_rng_results")
                or context.prospective_owner_documents
                or context.allocation_handles
            ):
                raise AssertionError("damage preparation unexpectedly has native work authority")
            original_evaluator = None
            if case.get("inject"):
                from GAME.TOOLS import mechanical_context

                original_evaluator = mechanical_context.evaluate_selector

                def inject_malformed_damage_source(*args, **kwargs):
                    raw = copy.deepcopy(original_evaluator(*args, **kwargs))
                    row = raw["selector_result"]["raw_contributions"][0]
                    injection = case["inject"]
                    if injection == "boolean_adjustment":
                        row["value"]["amount"] = True
                        row["rule_element"]["value"]["amount"] = True
                    elif injection == "float_adjustment":
                        row["value"]["amount"] = 1.0
                        row["rule_element"]["value"]["amount"] = 1.0
                    elif injection == "gate":
                        row["rule_element"]["gate"] = {
                            "resource_ref": "resource.unsupported"
                        }
                    elif injection == "priority":
                        row["rule_element"]["priority"] = 1
                    elif injection == "stacking_key":
                        row["rule_element"]["stacking_key"] = "stack.unsupported"
                    else:
                        raise AssertionError(f"unknown test injection: {injection}")
                    return raw

                mechanical_context.evaluate_selector = inject_malformed_damage_source
            forgery_cases = []
            if case.get("forgery"):
                from GAME.TOOLS import mechanical_context

                original_evaluator = mechanical_context.evaluate_selector
                evaluator_calls = []

                def forbidden_evaluator(*args, **kwargs):
                    evaluator_calls.append(True)
                    raise AssertionError("counterfeit damage context reached reads")

                mechanical_context.evaluate_selector = forbidden_evaluator
                forged_contexts = [("copy", copy.copy(context))]
                rebound_roles = dict(context.role_bindings)
                rebound_roles["target"] = rebound_roles["actor"]
                try:
                    forged_contexts.append(
                        ("role-rebind", replace(context, role_bindings=rebound_roles))
                    )
                except contracts.ActivityContractError:
                    forgery_cases.append("role-rebind-constructor-rejected")
                rejected_forgery_count = 0
                try:
                    for forgery_name, counterfeit in forged_contexts:
                        if contracts._preparation_context_is_issued(counterfeit):
                            raise AssertionError("counterfeit damage context retained issuance")
                        try:
                            calculation.calculate_selector(counterfeit, "damage.received")
                        except calculation.CalculationError:
                            rejected_forgery_count += 1
                            forgery_cases.append(f"{forgery_name}-rejected")
                finally:
                    mechanical_context.evaluate_selector = original_evaluator
                    original_evaluator = None
                if evaluator_calls or rejected_forgery_count != len(forged_contexts):
                    raise AssertionError("damage context forgery crossed into native reads")
            try:
                if case.get("change_membership_after_issue"):
                    changed_effect = _effect(
                        "effect.sp03.damage.currentness", "actor.target"
                    )
                    changed_effect["definition_id"] = "effect.sp03.damage.resistance"
                    changed_effect["state"]["source_id"] = ACTOR_ID
                    _write_routed(repository, "world.effect", changed_effect)
                    repository.commit("change recipient defense membership after issue")
                    revision_after_change = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
                    try:
                        calculation.calculate_selector(context, "damage.received")
                    except contracts.NativePreparationHold as hold:
                        stale_status = hold.operation_status
                    else:
                        stale_status = "STALE_CONTEXT_USED"
                    fresh_context = host._current_owner._prepare_root_context(
                        catalog,
                        compiled,
                        command_id=accepted["command_id"],
                        consumer_id=consumer_id,
                    )
                    result = calculation.calculate_selector(
                        fresh_context, "damage.received"
                    )
                    outcome = {
                        "status": "CURRENTNESS_CHECKED",
                        "stale_status": stale_status,
                        "result": result,
                        "runtime_partition_status": runtime_partition_status,
                        "forge_rejections": rejected_forgery_count
                        if case.get("forgery")
                        else 0,
                        "forgery_cases": forgery_cases,
                    }
                else:
                    result = calculation.calculate_selector(context, "damage.received")
                    outcome = {
                        "status": "OK",
                        "result": result,
                        "runtime_partition_status": runtime_partition_status,
                        "forge_rejections": rejected_forgery_count
                        if case.get("forgery")
                        else 0,
                        "forgery_cases": forgery_cases,
                    }
            except contracts.NativePreparationHold as hold:
                outcome = {"status": hold.operation_status}
            except calculation.CalculationError as error:
                outcome = {"status": "CALCULATION_ERROR", "error": str(error)}
            finally:
                if original_evaluator is not None:
                    mechanical_context.evaluate_selector = original_evaluator

        revision_after = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
        return {
            **outcome,
            "revision_before": revision_before,
            "revision_after_change": revision_after_change,
            "revision_after": revision_after,
        }

evidence = {case["name"]: run_case(case) for case in cases}
print(json.dumps(evidence, sort_keys=True))
"""
    )


def test_damage_defense_goldens_order_duplicates_and_source_matching(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
    )
    cases = [
        {"name": "none", "consumer_index": 0, "effects": [], "assets": []},
        {
            "name": "resistance",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.resistance"],
            "assets": [],
        },
        {
            "name": "vulnerability",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.vulnerability"],
            "assets": [],
        },
        {
            "name": "immunity",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.immunity"],
            "assets": [],
        },
        {
            "name": "both",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.vulnerability",
            ],
            "assets": [],
        },
        {
            "name": "both_permuted",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.vulnerability",
                "effect.sp03.damage.resistance",
            ],
            "assets": [],
        },
        {
            "name": "ordered_adjustment",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.adjustment",
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.vulnerability",
            ],
            "assets": [],
        },
        {
            "name": "duplicate_defenses",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.resistance_duplicate",
            ],
            "assets": ["asset.sp03.damage.resistance"],
        },
        {
            "name": "duplicate_defenses_permuted",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.resistance_duplicate",
                "effect.sp03.damage.resistance",
            ],
            "assets": ["asset.sp03.damage.resistance"],
        },
        {
            "name": "duplicate_vulnerabilities",
            "consumer_index": 0,
            "effects": [
                "effect.sp03.damage.vulnerability",
                "effect.sp03.damage.vulnerability_duplicate",
            ],
            "assets": [],
        },
        {
            "name": "asset_resistance",
            "consumer_index": 0,
            "effects": [],
            "assets": ["asset.sp03.damage.resistance"],
        },
        {
            "name": "ineligible_asset_resistance",
            "consumer_index": 0,
            "effects": [],
            "assets": ["asset.sp03.damage.resistance"],
            "asset_equipment": None,
        },
        {
            "name": "false_predicate",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.false_predicate"],
            "assets": [],
        },
        {
            "name": "bypassed",
            "consumer_index": 2,
            "effects": ["effect.sp03.damage.resistance_bypass"],
            "assets": [],
        },
        {
            "name": "wrong_type",
            "consumer_index": 3,
            "effects": ["effect.sp03.damage.resistance"],
            "assets": [],
        },
        {
            "name": "wrong_origin",
            "consumer_index": 4,
            "effects": ["effect.sp03.damage.resistance"],
            "assets": [],
        },
        {
            "name": "mixed_components",
            "consumer_index": 5,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.vulnerability",
            ],
            "assets": [],
        },
        {
            "name": "mixed_components_permuted",
            "consumer_index": 8,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.vulnerability",
            ],
            "assets": [],
        },
        {
            "name": "bypass_qualifier_partition",
            "consumer_index": 9,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.resistance_bypass",
            ],
            "assets": [],
        },
        {
            "name": "origin_qualifier_partition",
            "consumer_index": 10,
            "effects": [
                "effect.sp03.damage.resistance",
                "effect.sp03.damage.resistance_other_origin",
            ],
            "assets": [],
        },
        {"name": "group_peer", "consumer_index": 6, "effects": [], "assets": []},
        {"name": "group_unbound", "consumer_index": 7, "effects": [], "assets": []},
        {
            "name": "same_root_group_pair",
            "consumer_indices": [0, 6],
            "effects": [],
            "assets": [],
        },
    ]
    result = selector_tests._game_runtime_probe(
        runtime_root,
        _damage_cases_script(
            catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
        ),
        json.dumps(_damage_recipe()),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
        "[]",
        json.dumps(cases),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert {name: row["status"] for name, row in evidence.items()} == {
        case["name"]: "OK" for case in cases
    }
    assert {
        name: row["revision_before"] == row["revision_after"]
        for name, row in evidence.items()
    } == {case["name"]: True for case in cases}

    raw_input = evidence["none"]["result"]["components"][0]
    assert raw_input == {
        "amount": 7,
        "damage_type_id": "damage.fire",
        "origin_id": "origin.sp03.spell",
        "bypass_ids": [],
    }
    assert evidence["none"]["result"]["input_roles"] == {
        "source_role": "actor",
        "source_owner_ref": {
            "family_key": "world.actor",
            "identity": ["actor.sp03"],
        },
        "recipient_role": "target",
        "recipient_owner_ref": {
            "family_key": "world.actor",
            "identity": ["actor.target"],
        },
    }
    assert "cause" not in evidence["none"]["result"]
    assert "damage_instance_id" not in evidence["none"]["result"]
    assert len(evidence["none"]["result"]["source_evidence"]["source_tree_sha"]) == 40

    def total(name: str) -> int:
        return evidence[name]["result"]["total_damage"]

    assert (
        total("none"),
        total("resistance"),
        total("vulnerability"),
        total("immunity"),
    ) == (
        7,
        3,
        14,
        0,
    )
    assert total("both") == 6
    assert total("both_permuted") == 6
    assert total("ordered_adjustment") == 6
    assert [
        stage["output_amount"]
        for stage in evidence["ordered_adjustment"]["result"]["component_results"][0][
            "stages"
        ]
    ] == [6, 3, 6, 6]
    assert total("duplicate_defenses") == 3
    assert total("duplicate_defenses_permuted") == 3
    assert total("duplicate_vulnerabilities") == 14
    duplicate_trace = evidence["duplicate_defenses"]["result"]["trace"]["contributions"]
    assert sum(row["disposition"] == "APPLIED" for row in duplicate_trace) == 1
    assert (
        sum(row["disposition"] == "COALESCED_DUPLICATE" for row in duplicate_trace) == 2
    )
    permuted_duplicate_trace = evidence["duplicate_defenses_permuted"]["result"][
        "trace"
    ]["contributions"]
    assert sum(row["disposition"] == "APPLIED" for row in permuted_duplicate_trace) == 1
    assert (
        sum(
            row["disposition"] == "COALESCED_DUPLICATE"
            for row in permuted_duplicate_trace
        )
        == 2
    )
    vulnerability_trace = evidence["duplicate_vulnerabilities"]["result"]["trace"][
        "contributions"
    ]
    assert sum(row["disposition"] == "APPLIED" for row in vulnerability_trace) == 1
    assert (
        sum(row["disposition"] == "COALESCED_DUPLICATE" for row in vulnerability_trace)
        == 1
    )
    asset_trace = evidence["asset_resistance"]["result"]["trace"]["contributions"]
    assert len(asset_trace) == 1
    assert asset_trace[0]["source_owner_ref"]["family_key"] == "world.asset"
    assert total("asset_resistance") == 3
    target_effect = evidence["resistance"]["result"]["source_evidence"][
        "native_membership"
    ]["effects"][0]
    assert target_effect["target_id"] == "actor.target"
    assert target_effect["lifecycle"] == "effect_lifecycle.active"
    assert target_effect["is_target_local"] is True
    native_asset = evidence["asset_resistance"]["result"]["source_evidence"][
        "native_membership"
    ]["assets"][0]
    assert native_asset["equipment_mode"] == "worn"
    assert native_asset["accessible"] is True
    assert total("ineligible_asset_resistance") == 7
    ineligible_asset_trace = evidence["ineligible_asset_resistance"]["result"]["trace"][
        "contributions"
    ][0]
    assert ineligible_asset_trace["source_eligibility"] == "INELIGIBLE"
    assert "SOURCE_NOT_ELIGIBLE" in ineligible_asset_trace["rejection_reasons"]
    assert total("false_predicate") == 7
    false_predicate_trace = evidence["false_predicate"]["result"]["trace"][
        "contributions"
    ][0]
    assert false_predicate_trace["predicate_state"] == "FALSE"
    assert false_predicate_trace["disposition"] == "REJECTED"
    assert false_predicate_trace["predicate"] == {
        "compare": {"left": 1, "operator": "eq", "right": 0}
    }
    assert "PREDICATE_FALSE" in false_predicate_trace["rejection_reasons"]
    assert total("bypassed") == 7
    assert evidence["bypassed"]["result"]["components"][0]["bypass_ids"] == [
        "bypass.fire"
    ]
    assert (
        evidence["bypassed"]["result"]["trace"]["contributions"][0]["disposition"]
        == "BYPASSED"
    )
    assert (
        "BYPASSED_BY_COMPONENT"
        in evidence["bypassed"]["result"]["trace"]["contributions"][0][
            "rejection_reasons"
        ]
    )
    assert total("wrong_type") == 7
    assert (
        "DAMAGE_TYPE_MISMATCH"
        in evidence["wrong_type"]["result"]["trace"]["contributions"][0][
            "rejection_reasons"
        ]
    )
    assert total("wrong_origin") == 7
    assert (
        "ORIGIN_MISMATCH"
        in evidence["wrong_origin"]["result"]["trace"]["contributions"][0][
            "rejection_reasons"
        ]
    )
    assert total("mixed_components") == 10
    mixed = evidence["mixed_components"]["result"]["component_results"]
    assert [item["received_amount"] for item in mixed] == [6, 4]
    mixed_permuted = evidence["mixed_components_permuted"]["result"][
        "component_results"
    ]
    assert [item["received_amount"] for item in mixed_permuted] == [4, 6]
    assert evidence["mixed_components_permuted"]["result"]["total_damage"] == 10
    bypass_partition = evidence["bypass_qualifier_partition"]["result"]
    assert bypass_partition["total_damage"] == 10
    assert [
        item["received_amount"] for item in bypass_partition["component_results"]
    ] == [
        3,
        7,
    ]
    bypassed_rows = [
        row
        for row in bypass_partition["trace"]["contributions"]
        if row["component_index"] == 1
    ]
    assert len(bypassed_rows) == 2
    assert all(row["disposition"] == "BYPASSED" for row in bypassed_rows)
    assert all(
        "BYPASSED_BY_COMPONENT" in row["rejection_reasons"] for row in bypassed_rows
    )
    origin_partition = evidence["origin_qualifier_partition"]["result"]
    assert origin_partition["total_damage"] == 6
    assert [
        item["received_amount"] for item in origin_partition["component_results"]
    ] == [
        3,
        3,
    ]
    first_identity = evidence["none"]["result"]["logical_identity"]
    peer_identity = evidence["group_peer"]["result"]["logical_identity"]
    unbound_identity = evidence["group_unbound"]["result"]["logical_identity"]
    assert first_identity["instance_key"] != peer_identity["instance_key"]
    assert (
        first_identity["simultaneous_group_key"]
        == peer_identity["simultaneous_group_key"]
    )
    assert unbound_identity["simultaneous_group_key"] is None
    same_root_group_results = evidence["same_root_group_pair"]["results"]
    assert len(same_root_group_results) == 2
    assert [result["total_damage"] for result in same_root_group_results] == [7, 7]
    same_root_identities = [
        result["logical_identity"] for result in same_root_group_results
    ]
    assert (
        same_root_identities[0]["execution_ref"]
        == same_root_identities[1]["execution_ref"]
    )
    assert (
        same_root_identities[0]["simultaneous_group_key"]
        == (same_root_identities[1]["simultaneous_group_key"])
        == "damage.group.conformance"
    )
    assert (
        same_root_identities[0]["instance_key"]
        != same_root_identities[1]["instance_key"]
    )
    assert (
        same_root_identities[0]["consumer_id"] != same_root_identities[1]["consumer_id"]
    )


def test_damage_consumer_rejects_or_holds_unsupported_runtime_rule_values(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
    )
    cases = [
        {
            "name": "boolean_adjustment",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.adjustment"],
            "assets": [],
            "inject": "boolean_adjustment",
        },
        {
            "name": "float_adjustment",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.adjustment"],
            "assets": [],
            "inject": "float_adjustment",
        },
        {
            "name": "gate",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.adjustment"],
            "assets": [],
            "inject": "gate",
        },
        {
            "name": "priority",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.adjustment"],
            "assets": [],
            "inject": "priority",
        },
        {
            "name": "stacking_key",
            "consumer_index": 0,
            "effects": ["effect.sp03.damage.adjustment"],
            "assets": [],
            "inject": "stacking_key",
        },
    ]
    result = selector_tests._game_runtime_probe(
        runtime_root,
        _damage_cases_script(
            catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
        ),
        json.dumps(_damage_recipe()),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
        "[]",
        json.dumps(cases),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["boolean_adjustment"]["status"] == "CALCULATION_ERROR"
    assert "value is not closed" in evidence["boolean_adjustment"]["error"]
    assert evidence["float_adjustment"]["status"] == "CALCULATION_ERROR"
    assert "value is not closed" in evidence["float_adjustment"]["error"]
    assert evidence["gate"]["status"] == "AUTHORITY_UNAVAILABLE"
    for unsupported in ("priority", "stacking_key"):
        assert evidence[unsupported]["status"] == "AUTHORITY_UNAVAILABLE"


def test_damage_context_copy_rebinding_and_membership_currentness_are_enforced(
    installed_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    installed_parent = tmp_path / "installed"
    installed_parent.mkdir()
    runtime_root = _damage_compiler_runtime(
        tmp_path / "source",
        installed_runtime_root,
        installed_parent / "GAME",
    )
    cases = [
        {
            "name": "forgery",
            "consumer_index": 0,
            "effects": [],
            "assets": [],
            "forgery": True,
        },
        {
            "name": "runtime_partition",
            "consumer_index": 0,
            "effects": [],
            "assets": [],
            "runtime_partition_probe": True,
        },
        {
            "name": "membership_changed_after_issue",
            "consumer_index": 0,
            "effects": [],
            "assets": [],
            "change_membership_after_issue": True,
        },
    ]
    result = selector_tests._game_runtime_probe(
        runtime_root,
        _damage_cases_script(
            catalog_tests._RECIPE_PROBE.replace("TOOLS.", "GAME.TOOLS.")
        ),
        json.dumps(_damage_recipe()),
        json.dumps(DAMAGE_SOURCE_DEFINITION_KINDS),
        "[]",
        json.dumps(cases),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["forgery"]["status"] == "OK"
    assert evidence["forgery"]["forge_rejections"] >= 1
    assert "copy-rejected" in evidence["forgery"]["forgery_cases"]
    assert (
        "role-rebind-rejected" in evidence["forgery"]["forgery_cases"]
        or "role-rebind-constructor-rejected" in evidence["forgery"]["forgery_cases"]
    )
    assert evidence["runtime_partition"]["status"] == "OK"
    assert evidence["runtime_partition"]["runtime_partition_status"] == (
        "AUTHORITY_UNAVAILABLE"
    )
    changed = evidence["membership_changed_after_issue"]
    assert changed["status"] == "CURRENTNESS_CHECKED"
    assert changed["stale_status"] == "REVALIDATION_REQUIRED"
    assert changed["result"]["total_damage"] == 3
    assert (
        changed["result"]["source_evidence"]["source_revision"]
        == (changed["revision_after_change"])
    )
    assert changed["result"]["source_evidence"]["native_membership"]["effect_ids"] == [
        "effect.sp03.damage.currentness"
    ]
