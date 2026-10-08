"""Finite, non-activating SP03 Armor Class policy contracts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
AC_POLICY_ID = "calculation.armor_class_srd521"
AC_ACTIVITY_ID = "activity.conformance.ac"
AC_CONSUMER_ID = f"{AC_ACTIVITY_ID}.step.1"


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _schema_registry() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = _schema(path.name)
        identifier = schema.get("$id")
        if isinstance(identifier, str):
            registry = registry.with_resource(
                identifier, Resource.from_contents(schema)
            )
    return registry


def _accepts(schema: dict[str, object], definition_name: str, value: object) -> bool:
    validation_root = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "allOf": [schema["$defs"][definition_name]],
    }
    return Draft202012Validator(validation_root, registry=_schema_registry()).is_valid(
        value
    )


def _ac_policy_binding() -> dict[str, object]:
    return {
        "consumer_id": AC_CONSUMER_ID,
        "profile_id": AC_POLICY_ID,
        "profile_generation": 1,
        "reads": ["selector:defense.armor_class"],
        "selector_operation_pairs": [
            {
                "selector_id": "defense.armor_class",
                "operation_ids": ["rule.add_flat", "rule.override"],
            }
        ],
        "context_fact_bindings": [],
        "native_role_bindings": [
            {
                "read_ref": "selector:defense.armor_class",
                "role_names": ["target"],
            }
        ],
        "native_base_descriptor": {
            "kind": "ACTOR_DEXTERITY_BASE",
            "ability_id": "ability.dexterity",
            "subject_role": "target",
        },
    }


def _ac_activity_record() -> dict[str, object]:
    return {
        "id": AC_ACTIVITY_ID,
        "kind": "definition.activity",
        "name": {"en": "SP03 AC preparation conformance"},
        "data": {
            "family_id": "activity.attack",
            "profile_bindings": [
                {
                    "consumer_id": AC_CONSUMER_ID,
                    "profile_id": AC_POLICY_ID,
                    "profile_generation": 1,
                }
            ],
            "steps": [
                {
                    "op": "op.roll",
                    "args": {
                        "request": {
                            "roll_id": "roll.sp03.ac.conformance",
                            "expression": "1d20",
                            "purpose_id": "roll.attack",
                            "roller_role": "actor",
                        }
                    },
                    "export": "attack_roll",
                },
                {
                    "op": "op.resolve_attack",
                    "args": {
                        "roll": "attack_roll.result",
                        "threshold": "selector.defense.armor_class",
                    },
                },
            ],
        },
    }


def _ac_source_definitions(
    modifier_order: tuple[int, int] = (2, 3),
    mage_armor_predicate_false: bool = False,
    mage_armor_as_flat: bool = False,
    shield_arbitration_policy_id: str | None = None,
    duplicate_shield_ac_elements: bool = False,
    shield_definition_kind: str = "definition.effect",
    unsupported_modifier_member: str | None = None,
    duplicate_mage_armor_ac_elements: bool = False,
    archetype_feature_ids: tuple[str, ...] | None = None,
) -> list[dict[str, object]]:
    mage_armor_element: dict[str, object] = {
        "selector": "defense.armor_class",
        "operation_id": "rule.add_flat" if mage_armor_as_flat else "rule.override",
        "value": 13 if mage_armor_as_flat else {"base_kind": "MAGE_ARMOR_13_PLUS_DEX"},
    }
    if mage_armor_predicate_false and not mage_armor_as_flat:
        mage_armor_element["predicate"] = {
            "compare": {"left": 1, "operator": "eq", "right": 2}
        }
    mage_armor_elements = [mage_armor_element]
    if duplicate_mage_armor_ac_elements:
        mage_armor_elements.append(dict(mage_armor_element))
    shield_ac_elements = [
        {
            "selector": "defense.armor_class",
            "operation_id": "rule.add_flat",
            "value": 5,
        }
    ]
    if duplicate_shield_ac_elements:
        shield_ac_elements.append(
            {
                "selector": "defense.armor_class",
                "operation_id": "rule.add_flat",
                "value": 5,
            }
        )
    shield_data: dict[str, object] = {"rule_elements": shield_ac_elements}
    if shield_arbitration_policy_id is not None:
        shield_data["arbitration_policy_id"] = shield_arbitration_policy_id
    shield_definition: dict[str, object] = {
        "id": "effect.spell.shield",
        "kind": shield_definition_kind,
        "name": {"en": "Shield"},
        "data": shield_data,
    }
    if shield_definition_kind == "definition.asset":
        shield_definition["facets"] = ["asset.shield"]
    attuned_asset_rule_elements = [
        {
            "selector": "defense.armor_class",
            "operation_id": "rule.add_flat",
            "value": 2,
        }
    ]
    modifier_elements = [
        {
            "selector": "defense.armor_class",
            "operation_id": "rule.add_flat",
            "value": value,
        }
        for value in modifier_order
    ]
    if unsupported_modifier_member is not None:
        unsupported_value: object = (
            {"resource_ref": "resource.unknown"}
            if unsupported_modifier_member == "gate"
            else 1
            if unsupported_modifier_member == "priority"
            else "stack.ac"
        )
        for element in modifier_elements:
            element[unsupported_modifier_member] = unsupported_value
    archetype_data: dict[str, object] = {
        "abilities": {"ability.dexterity": 15},
    }
    if archetype_feature_ids is not None:
        archetype_data["feature_ids"] = list(archetype_feature_ids)
    return [
        {
            "id": "actor_archetype.sp03.ac",
            "kind": "definition.actor_archetype",
            "name": {"en": "SP03 AC conformance archetype"},
            "data": archetype_data,
        },
        {
            "id": "effect.spell.mage_armor",
            "kind": "definition.effect",
            "name": {"en": "Mage Armor"},
            "data": {"rule_elements": mage_armor_elements},
        },
        {
            "id": "effect.sp03.ac.support",
            "kind": "definition.effect",
            "name": {"en": "AC support parent"},
            "data": {"rule_elements": []},
        },
        shield_definition,
        {
            "id": "effect.sp03.ac.modifier_pair",
            "kind": "definition.effect",
            "name": {"en": "AC modifier permutation conformance"},
            "data": {"rule_elements": modifier_elements},
        },
        {
            "id": "effect.lookalike.mage_armor",
            "kind": "definition.effect",
            "name": {"en": "Mage Armor"},
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.override",
                        "value": {"base_kind": "MAGE_ARMOR_13_PLUS_DEX"},
                    }
                ]
            },
        },
        {
            "id": "effect.sp03.dexterity_change",
            "kind": "definition.effect",
            "name": {"en": "Unresolved ability-changing effect"},
            "data": {
                "rule_elements": [
                    {
                        "selector": "ability.score",
                        "operation_id": "rule.add_flat",
                        "value": 2,
                    }
                ]
            },
        },
        {
            "id": "asset.sp03.ac.armor",
            "kind": "definition.asset",
            "name": {"en": "Conformance armor"},
            "facets": ["asset.armor"],
            "data": {},
        },
        {
            "id": "asset.sp03.ac.wearable",
            "kind": "definition.asset",
            "name": {"en": "Conformance wearable"},
            "facets": ["asset.wearable"],
            "data": {},
        },
        {
            "id": "asset.sp03.ac.unclassified",
            "kind": "definition.asset",
            "name": {"en": "Unclassified worn asset"},
            "data": {},
        },
        {
            "id": "asset.sp03.ac.shield",
            "kind": "definition.asset",
            "name": {"en": "Conformance held shield"},
            "facets": ["asset.shield"],
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.add_flat",
                        "value": 2,
                    }
                ]
            },
        },
        {
            "id": "asset.sp03.ac.attuned_shield",
            "kind": "definition.asset",
            "name": {"en": "Conformance required-attunement shield"},
            "facets": ["asset.shield"],
            "data": {
                "attunement": {"required": True},
                "rule_elements": attuned_asset_rule_elements,
            },
        },
        {
            "id": "asset.sp03.ac.class_limited_shield",
            "kind": "definition.asset",
            "name": {"en": "Conformance class-limited shield"},
            "facets": ["asset.shield"],
            "data": {
                "attunement": {
                    "required": True,
                    "allowed_class_ids": ["class.test"],
                },
                "rule_elements": attuned_asset_rule_elements,
            },
        },
    ]


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _install_ac_compiler_runtime(
    source_root: Path, installed_template: Path, destination: Path
) -> Path:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as carrier_tests

    catalog_tests._stage_clean_source_tree(source_root)
    primitive_root = source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
    for primitive_id in ("op.roll", "op.resolve_attack"):
        path = primitive_root / f"{primitive_id}.json"
        row = json.loads(path.read_text(encoding="utf-8"))
        contract = row["contract"]
        consumers = contract["exact_seed_consumer_ids"]
        if AC_ACTIVITY_ID not in consumers:
            consumers.append(AC_ACTIVITY_ID)
        declarations = contract.setdefault("compiler_declarations", {})
        declaration: dict[str, object] = {
            "roles": {"actor": "world.actor", "target": "world.actor"},
            "symbols": {},
            "profiles": [],
        }
        if primitive_id == "op.resolve_attack":
            declaration["calculation_policies"] = [_ac_policy_binding()]
        declarations[AC_ACTIVITY_ID] = declaration
        _write_json(path, row)

    selector_ledger_path = (
        source_root
        / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
    )
    ledger = json.loads(selector_ledger_path.read_text(encoding="utf-8"))
    for selector_id in ("attack.roll", "defense.armor_class"):
        selector = next(row for row in ledger["entries"] if row["id"] == selector_id)
        if AC_ACTIVITY_ID not in selector["consumer_or_dependency"]:
            selector["consumer_or_dependency"] += (
                f"; {AC_ACTIVITY_ID} isolated conformance"
            )
    _write_json(selector_ledger_path, ledger)

    return carrier_tests._installed_source_compiler_fixture(
        source_root, installed_template, destination
    )


def test_ac_selector_contract_separates_registered_flat_from_conformance_base() -> None:
    schema = _schema("mechanical-surfaces.schema.json")
    selector = {
        "allowed_operations": ["rule.add_flat", "rule.override"],
        "operation_contracts": {
            "rule.add_flat": {
                "value_kind": "numeric_scalar",
                "normalization": "SUM",
                "constraints": ["finite_integer"],
                "calculation_policy_id": AC_POLICY_ID,
                "calculation_policy_generation": 1,
            },
            "rule.override": {
                "value_kind": "armor_class_base",
                "normalization": "SELECT_ONE_LEGAL_BASE",
                "constraints": ["eligible_nonadditive_ac_base"],
                "calculation_policy_id": AC_POLICY_ID,
                "calculation_policy_generation": 1,
            },
        },
        "contribution_type": "armor_class",
        "result_type": "integer",
        "result_constraints": {},
        "subject_kinds": ["world.actor"],
        "binding_kinds": ["subject"],
        "allowed_dependency_kinds": [],
        "allowed_input_classes": ["ENGINE_STATE"],
        "permitted_context_fact_ids": [],
        "static_dependencies": [],
        "combination_policy": "armor_class_nonadditive_base_v1",
        "calculation_policy_id": AC_POLICY_ID,
        "calculation_policy_generation": 1,
        "resolution_owner": "SELECTOR_METADATA",
        "trace_policy": "RETAIN_ACCEPTED_REJECTED_PROVENANCE",
    }

    assert _accepts(schema, "selectorMetadata", selector)

    repurposed_flat = json.loads(json.dumps(selector))
    repurposed_flat["operation_contracts"]["rule.add_flat"].update(
        {
            "value_kind": "armor_class_base",
            "normalization": "SELECT_ONE_LEGAL_BASE",
            "constraints": ["eligible_nonadditive_ac_base"],
        }
    )
    assert not _accepts(schema, "selectorMetadata", repurposed_flat)

    unbound_armor_class = json.loads(
        json.dumps(
            _schema("../CATALOG/mechanical-surfaces.json")["selectors"][
                "defense.armor_class"
            ]
        )
    )
    unbound_armor_class["contribution_type"] = "armor_class"
    assert not _accepts(schema, "selectorMetadata", unbound_armor_class)


def test_ac_native_base_descriptor_is_closed_and_dexterity_specific() -> None:
    values = _schema("spell-native-profile-values.schema.json")
    binding = {
        "consumer_id": "activity.attack.ranged_weapon.step.2",
        "profile_id": AC_POLICY_ID,
        "profile_generation": 1,
        "reads": ["selector:defense.armor_class"],
        "selector_operation_pairs": [
            {
                "selector_id": "defense.armor_class",
                "operation_ids": ["rule.add_flat", "rule.override"],
            }
        ],
        "context_fact_bindings": [],
        "native_role_bindings": [
            {
                "read_ref": "selector:defense.armor_class",
                "role_names": ["target"],
            }
        ],
        "native_base_descriptor": {
            "kind": "ACTOR_DEXTERITY_BASE",
            "ability_id": "ability.dexterity",
            "subject_role": "target",
        },
    }

    assert _accepts(values, "calculationPolicyBinding", binding)

    alias = json.loads(json.dumps(binding))
    alias["native_base_descriptor"]["ability_id"] = "dex"
    assert not _accepts(values, "calculationPolicyBinding", alias)

    generic_path = json.loads(json.dumps(binding))
    generic_path["native_base_descriptor"]["property_path"] = "state.dex"
    assert not _accepts(values, "calculationPolicyBinding", generic_path)


def test_ac_base_value_has_only_the_mage_armor_candidate_discriminator() -> None:
    values = _schema("spell-native-profile-values.schema.json")
    base_schema = values["$defs"].get("armorClassBaseValue")
    assert isinstance(base_schema, dict), "AC base value contract is missing"
    validator = Draft202012Validator(
        {"$schema": values["$schema"], "$defs": values["$defs"], **base_schema},
        registry=_schema_registry(),
    )

    assert validator.is_valid({"base_kind": "MAGE_ARMOR_13_PLUS_DEX"})
    assert not validator.is_valid(
        {"base_kind": "MAGE_ARMOR_13_PLUS_DEX", "ability_id": "ability.dexterity"}
    )
    assert not validator.is_valid({"base_kind": "ARBITRARY_OVERRIDE", "value": 13})


def test_ac_result_schema_separates_candidate_math_from_selected_ac() -> None:
    values = _schema("spell-native-profile-values.schema.json")
    result_schema = values["$defs"].get("armorClassPolicyResult")
    assert isinstance(result_schema, dict), "AC policy result contract is missing"
    assert "CHOICE_REQUIRED" in result_schema["properties"]["selection_status"]["enum"]
    assert "selected_ac" in result_schema["properties"]


def test_compiler_materializes_only_the_exact_dormant_ac_override_pair() -> None:
    from DEV.TOOLS.catalog_admission import load_catalog_admission_ledger
    from GAME.TOOLS import activity_contracts, activity_runtime

    core = _schema("../CATALOG/core-catalog.json")
    mechanical = _schema("../CATALOG/mechanical-surfaces.json")
    ledger = load_catalog_admission_ledger(ROOT)
    ledger_rows = {
        (entry["registry_family"], entry["id"]): entry for entry in ledger["entries"]
    }
    consumer_id = "activity.attack.ranged_weapon.step.2"
    activity_id = "activity.attack.ranged_weapon"
    binding = {
        "consumer_id": consumer_id,
        "profile_id": AC_POLICY_ID,
        "profile_generation": 1,
        "reads": ["selector:defense.armor_class"],
        "selector_operation_pairs": [
            {
                "selector_id": "defense.armor_class",
                "operation_ids": ["rule.add_flat", "rule.override"],
            }
        ],
        "context_fact_bindings": [],
        "native_role_bindings": [
            {
                "read_ref": "selector:defense.armor_class",
                "role_names": ["target"],
            }
        ],
        "native_base_descriptor": {
            "kind": "ACTOR_DEXTERITY_BASE",
            "ability_id": "ability.dexterity",
            "subject_role": "target",
        },
    }
    role_contracts = {
        "actor": {
            "family_key": "world.actor",
            "required": True,
        },
        "target": {
            "family_key": "world.actor",
            "required": True,
        },
    }

    def compile_policy(
        source_definitions: dict[str, dict[str, object]],
    ) -> tuple[activity_contracts.CompiledCalculationPolicy, ...]:
        return activity_runtime._compile_calculation_policy_bindings(
            (binding,),
            consumer_id=consumer_id,
            activity_id=activity_id,
            profile_bindings=(
                activity_contracts.ProfileBinding(consumer_id, AC_POLICY_ID, 1),
            ),
            mechanical=mechanical,
            core=core,
            ledger_rows=ledger_rows,
            role_contracts=role_contracts,
            source_definitions=source_definitions,
        )

    compiled = compile_policy({})

    assert len(compiled) == 1
    assert compiled[0].binding.selector_operation_pairs == (
        activity_contracts.SelectorOperationPair(
            "defense.armor_class", ("rule.add_flat", "rule.override")
        ),
    )
    assert compiled[0].binding.native_base_descriptor.ability_id == "ability.dexterity"
    assert compiled[0].selector_contracts["defense.armor_class"][
        "allowed_operations"
    ] == ("rule.add_flat", "rule.override")
    override = ledger_rows[("rule_operations", "rule.override")]
    assert override["admission_disposition"] == "DORMANT_NONSELECTABLE"

    invalid_source = {
        "effect.invalid.ac_base": {
            "id": "effect.invalid.ac_base",
            "kind": "definition.effect",
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.override",
                        "value": {
                            "base_kind": "MAGE_ARMOR_13_PLUS_DEX",
                            "value": 13,
                        },
                    }
                ]
            },
        }
    }
    with pytest.raises(
        activity_runtime.ActivityNotSelectable,
        match="not the Mage Armor discriminator",
    ):
        compile_policy(invalid_source)

    mage_armor_flat_source = {
        "effect.spell.mage_armor": {
            "id": "effect.spell.mage_armor",
            "kind": "definition.effect",
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.add_flat",
                        "value": 13,
                    }
                ]
            },
        }
    }
    with pytest.raises(
        activity_runtime.ActivityNotSelectable,
        match="Mage Armor source is base-only",
    ):
        compile_policy(mage_armor_flat_source)

    shield_rule = {
        "selector": "defense.armor_class",
        "operation_id": "rule.add_flat",
        "value": 5,
    }
    duplicate_shield_source = {
        "effect.spell.shield": {
            "id": "effect.spell.shield",
            "kind": "definition.effect",
            "data": {"rule_elements": [shield_rule, dict(shield_rule)]},
        }
    }
    with pytest.raises(
        activity_runtime.ActivityNotSelectable,
        match="Shield source requires exactly one AC flat",
    ):
        compile_policy(duplicate_shield_source)

    retyped_shield_source = {
        "effect.spell.shield": {
            "id": "effect.spell.shield",
            "kind": "definition.asset",
            "facets": ["asset.shield"],
            "data": {"rule_elements": [shield_rule]},
        }
    }
    with pytest.raises(
        activity_runtime.ActivityNotSelectable,
        match="Shield source must be an Effect definition",
    ):
        compile_policy(retyped_shield_source)


def test_mechanical_context_accepts_only_the_mage_armor_base_discriminator() -> None:
    from GAME.TOOLS.mechanical_context import (
        MechanicalContextError,
        _closed_operation_value,
    )

    operation = {
        "value_kind": "armor_class_base",
        "normalization": "SELECT_ONE_LEGAL_BASE",
        "constraints": ["eligible_nonadditive_ac_base"],
        "calculation_policy_id": AC_POLICY_ID,
        "calculation_policy_generation": 1,
    }

    assert _closed_operation_value(
        "rule.override", operation, {"base_kind": "MAGE_ARMOR_13_PLUS_DEX"}
    ) == {"base_kind": "MAGE_ARMOR_13_PLUS_DEX"}
    with pytest.raises(MechanicalContextError):
        _closed_operation_value(
            "rule.override",
            operation,
            {"base_kind": "MAGE_ARMOR_13_PLUS_DEX", "value": 13},
        )
    with pytest.raises(MechanicalContextError):
        _closed_operation_value(
            "rule.override", operation, {"base_kind": "ARBITRARY_OVERRIDE"}
        )
    with pytest.raises(MechanicalContextError):
        _closed_operation_value(
            "rule.override",
            operation,
            {"base_kind": "MAGE_ARMOR_13_PLUS_DEX", "ability_id": "ability.dexterity"},
        )


@pytest.mark.parametrize("unsupported_member", ("gate", "priority", "stacking_key"))
def test_ac_cold_source_validation_rejects_unowned_rule_element_members(
    unsupported_member: str,
) -> None:
    from GAME.TOOLS.activity_runtime import (
        ActivityNotSelectable,
        _validate_typed_ac_policy_source_values,
    )

    unsupported_value: object = (
        {"resource_ref": "resource.unknown"}
        if unsupported_member == "gate"
        else 1
        if unsupported_member == "priority"
        else "stack.ac"
    )
    source_definitions = {
        "effect.ac.unsafe": {
            "id": "effect.ac.unsafe",
            "kind": "definition.effect",
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.add_flat",
                        "value": 2,
                        unsupported_member: unsupported_value,
                    }
                ]
            },
        }
    }
    with pytest.raises(ActivityNotSelectable, match="unsupported source members"):
        _validate_typed_ac_policy_source_values(source_definitions)


def test_ac_cold_source_rejects_exact_shield_definition_retyped_as_asset() -> None:
    from GAME.TOOLS.activity_runtime import (
        ActivityNotSelectable,
        _validate_typed_ac_policy_source_values,
    )

    source_definitions = {
        "effect.spell.shield": {
            "id": "effect.spell.shield",
            "kind": "definition.asset",
            "facets": ["asset.shield"],
            "data": {
                "rule_elements": [
                    {
                        "selector": "defense.armor_class",
                        "operation_id": "rule.add_flat",
                        "value": 5,
                    }
                ]
            },
        }
    }
    with pytest.raises(
        ActivityNotSelectable,
        match="Shield source must be an Effect definition",
    ):
        _validate_typed_ac_policy_source_values(source_definitions)


def test_ac_cold_source_rejects_duplicate_mage_armor_base_elements() -> None:
    from GAME.TOOLS.activity_runtime import (
        ActivityNotSelectable,
        _validate_typed_ac_policy_source_values,
    )

    element = {
        "selector": "defense.armor_class",
        "operation_id": "rule.override",
        "value": {"base_kind": "MAGE_ARMOR_13_PLUS_DEX"},
    }
    source_definitions = {
        "effect.spell.mage_armor": {
            "id": "effect.spell.mage_armor",
            "kind": "definition.effect",
            "data": {"rule_elements": [element, dict(element)]},
        }
    }
    with pytest.raises(
        ActivityNotSelectable,
        match="Mage Armor source requires exactly one AC base Rule Element",
    ):
        _validate_typed_ac_policy_source_values(source_definitions)


def test_ruling_keeps_registry_dormant_set_unpromoted() -> None:
    core = _schema("../CATALOG/core-catalog.json")
    assert "rule.override" in core["registries"]["rule_operations"]


def _ac_root_probe_script(
    compiler_probe: str, *, bypass_cold_source_validation: bool = False
) -> str:
    prepared_probe = compiler_probe.replace("TOOLS.", "GAME.TOOLS.")
    if bypass_cold_source_validation:
        marker = "import GAME.TOOLS.activity_runtime as runtime"
        assert marker in prepared_probe
        prepared_probe = prepared_probe.replace(
            marker,
            marker
            + "\nruntime._validate_typed_ac_policy_source_values = "
            + "lambda _source_definitions: None",
            1,
        )
    return (
        prepared_probe
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
    _asset,
    _effect,
    _write_routed,
)
from DEV.TESTS.test_w05_t06_p0_actor_producer import _selected_host
from GAME.TOOLS import activity_contracts as contracts
from GAME.TOOLS import calculation
from GAME.TOOLS import mechanical_context
from GAME.TOOLS.hot_store import NativeHotStore
from GAME.TOOLS.runtime_execution import accept_command

case = json.loads(sys.argv[4])
extra_records = records[1:]
target_id = "actor.ac.subject"
archetype_id = "actor_archetype.sp03.ac"

def _actor(actor_id, abilities):
    record = _actor_record()
    record["id"] = actor_id
    record["definition_id"] = case.get("subject_definition_id", archetype_id) if actor_id == target_id else archetype_id
    state = record["state"]
    state.pop("embodiment", None)
    if abilities is None:
        state.pop("abilities", None)
    else:
        state["abilities"] = abilities
    if case.get("build"):
        state["build"] = {"class_progression": [{"class_id": "class.test", "level": 1}]}
    if case.get("embodiment"):
        state.pop("continuity", None)
        state.pop("build", None)
        state["embodiment"] = {
            "profile_id": "actor.embodiment.body",
            "principal_subject_id": "actor.principal",
            "relation_effect_id": "effect.relation",
            "construction_basis_ref": "basis.construction",
        }
    return record

actor = _actor(ACTOR_ID, case.get("caster_abilities", {"ability.dexterity": {"base": 20}}))
target = _actor(target_id, case.get("subject_abilities", {"ability.dexterity": {"base": 16}}))

with tempfile.TemporaryDirectory(prefix="sp03-ac-policy-") as temporary:
    repository = GitCampaignRepository(Path(temporary) / "campaign.git")
    repository.write("MANIFEST.yaml", {"campaign_id": CAMPAIGN_ID})
    repository.write("WORLD/EFFECTS/INDEX.yaml", {"entries": []})
    repository.write("WORLD/ITEMS/INDEX.yaml", {"entries": []})
    _write_routed(repository, "world.actor", actor)
    _write_routed(repository, "world.actor", target)

    effect_specs = {
        "mage_armor": {
            "effect_id": "effect.application.mage_armor",
            "definition_id": "effect.spell.mage_armor",
            "rules_origin_id": "source.spell.mage_armor",
            "source_id": ACTOR_ID,
        },
        "mage_armor_false": {
            "effect_id": "effect.application.mage_armor_false",
            "definition_id": "effect.spell.mage_armor",
            "rules_origin_id": "source.spell.mage_armor",
            "source_id": ACTOR_ID,
        },
        "support_parent": {
            "effect_id": "effect.application.ac.support_parent",
            "definition_id": "effect.sp03.ac.support",
            "rules_origin_id": "source.conformance.ac.support",
            "source_id": ACTOR_ID,
        },
        "shield": {
            "effect_id": "effect.application.shield",
            "definition_id": "effect.spell.shield",
            "rules_origin_id": "source.spell.shield",
            "source_id": target_id,
        },
        "modifier_pair": {
            "effect_id": "effect.application.ac_modifier_pair",
            "definition_id": "effect.sp03.ac.modifier_pair",
            "rules_origin_id": "source.conformance.ac.modifiers",
            "source_id": target_id,
        },
        "mage_armor_lookalike": {
            "effect_id": "effect.application.lookalike",
            "definition_id": "effect.lookalike.mage_armor",
            "rules_origin_id": "source.spell.lookalike",
            "source_id": ACTOR_ID,
        },
        "ability_change": {
            "effect_id": "effect.application.dexterity_change",
            "definition_id": "effect.sp03.dexterity_change",
            "rules_origin_id": "source.spell.dexterity_change",
            "source_id": ACTOR_ID,
        },
    }
    for effect_entry in case.get("effects", []):
        effect_name = effect_entry if isinstance(effect_entry, str) else effect_entry["name"]
        spec = effect_specs[effect_name]
        effect_id = (
            spec["effect_id"]
            if isinstance(effect_entry, str)
            else effect_entry.get("effect_id", spec["effect_id"])
        )
        effect_target = (
            target_id
            if isinstance(effect_entry, str)
            else effect_entry.get("target_id", target_id)
        )
        effect = _effect(effect_id, effect_target)
        effect["definition_id"] = spec["definition_id"]
        effect["state"]["source_id"] = (
            spec["source_id"]
            if isinstance(effect_entry, str)
            else effect_entry.get("source_id", spec["source_id"])
        )
        effect["state"]["rules_origin_id"] = (
            spec["rules_origin_id"]
            if isinstance(effect_entry, str)
            else effect_entry.get("rules_origin_id", spec["rules_origin_id"])
        )
        if isinstance(effect_entry, dict) and "support_effect_id" in effect_entry:
            effect["state"]["support_effect_id"] = effect_entry["support_effect_id"]
        if isinstance(effect_entry, dict) and effect_entry.get("omit_rules_origin_id") is True:
            effect["state"].pop("rules_origin_id", None)
        _write_routed(repository, "world.effect", effect)

    for asset in case.get("assets", []):
        record = _asset(
            asset["asset_id"],
            owner=target_id,
            equipment=asset.get("equipment_mode"),
        )
        record["definition_id"] = asset["definition_id"]
        if "attuned_actor_id" in asset:
            record["state"]["attuned_actor_id"] = asset["attuned_actor_id"]
        _write_routed(repository, "world.asset", record)

    repository.commit("seed source-bound AC preparation inputs")
    revision_before = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
    proposal = _proposal(compiled.activity_id)
    proposal["action_request"]["actor_id"] = ACTOR_ID
    proposal["action_request"]["target_ids"] = [target_id]
    accepted = accept_command(
        _interpreter_result(),
        catalog.catalog_context,
        {"definition_id": compiled.activity_id, "kind": "definition.activity"},
        proposal,
    )
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
    repository.commit("seed accepted AC preparation root")
    revision_before_calculation = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()

    with NativeHotStore(":memory:") as store:
        host, _source = _selected_host(store, repository=repository)
        context = None
        try:
            context = host._current_owner._prepare_root_context(
                catalog,
                compiled,
                command_id=accepted["command_id"],
                consumer_id=identity + ".step.1",
            )
        except contracts.NativePreparationHold as hold:
            evidence = {"status": "HOLD", "hold_status": hold.operation_status}
        if context is not None:
            assert contracts._preparation_context_is_issued(context)
            if case.get("change_target_after_issue"):
                target["state"]["abilities"] = {"ability.dexterity": {"base": 8}}
                _write_routed(repository, "world.actor", target)
                repository.commit("change AC target after issued read context")
            if case.get("raw_only"):
                try:
                    raw = mechanical_context.evaluate_selector(
                        compiled,
                        "defense.armor_class",
                        consumer_id=context.consumer_id,
                        observation=context.observation,
                        role_bindings=context.role_bindings,
                        accepted_command=context.accepted_command,
                    )
                except contracts.NativePreparationHold as hold:
                    evidence = {"status": "HOLD", "hold_status": hold.operation_status}
                except mechanical_context.MechanicalContextError as error:
                    evidence = {"status": "MECHANICAL_CONTEXT_ERROR", "error": str(error)}
                else:
                    evidence = {"status": "RAW", "raw_selector": contracts._thaw(raw)}
            else:
                try:
                    result = calculation.calculate_selector(context, "defense.armor_class")
                except contracts.NativePreparationHold as hold:
                    evidence = {"status": "HOLD", "hold_status": hold.operation_status}
                except (calculation.CalculationError, mechanical_context.MechanicalContextError) as error:
                    evidence = {"status": "CALCULATION_ERROR", "error": str(error)}
                else:
                    evidence = {"status": "OK", "result": contracts._thaw(result)}

    revision_after_calculation = repository._git("rev-parse", "HEAD").stdout.decode("ascii").strip()
    print(json.dumps({
        **evidence,
        "role_bindings": {} if context is None else {
            role: {"family_key": owner.family_key, "identity": list(owner.identity)}
            for role, owner in context.role_bindings.items()
        },
        "revision_before_calculation": revision_before_calculation,
        "revision_after_calculation": revision_after_calculation,
        "fixed_rng_results": [] if context is None else list(context.resolution.get("fixed_rng_results", [])),
        "accepted_fact_refs": [] if context is None else list(context.accepted_fact_refs),
        "source_execution_ref": {"command_id": accepted["command_id"], "resolution_id": accepted["root_resolution_id"]},
        "context_issued": context is not None and contracts._preparation_context_is_issued(context),
    }, sort_keys=True))
"""
    )


def _run_ac_case(runtime_root: Path, case: dict[str, object]) -> dict[str, object]:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_selector_dag as selector_tests

    effect_names = case.get("effects", [])
    mage_armor_predicate_false = any(
        effect == "mage_armor_false"
        or isinstance(effect, dict)
        and effect.get("name") == "mage_armor_false"
        for effect in effect_names
    )
    result = selector_tests._game_runtime_probe(
        runtime_root,
        _ac_root_probe_script(
            catalog_tests._RECIPE_PROBE,
            bypass_cold_source_validation=bool(
                case.get("bypass_cold_source_validation", False)
            ),
        ),
        json.dumps(_ac_activity_record()),
        json.dumps({}),
        json.dumps(
            _ac_source_definitions(
                tuple(case.get("modifier_order", (2, 3))),
                mage_armor_predicate_false,
                bool(case.get("mage_armor_as_flat", False)),
                (
                    case.get("shield_arbitration_policy_id")
                    if isinstance(case.get("shield_arbitration_policy_id"), str)
                    else None
                ),
                bool(case.get("duplicate_shield_ac_elements", False)),
                (
                    case.get("shield_definition_kind", "definition.effect")
                    if isinstance(
                        case.get("shield_definition_kind", "definition.effect"), str
                    )
                    else "definition.effect"
                ),
                (
                    case.get("unsupported_modifier_member")
                    if isinstance(case.get("unsupported_modifier_member"), str)
                    else None
                ),
                bool(case.get("duplicate_mage_armor_ac_elements", False)),
                (
                    tuple(case["subject_archetype_feature_ids"])
                    if isinstance(case.get("subject_archetype_feature_ids"), list)
                    else None
                ),
            )
        ),
        json.dumps(case),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


@pytest.fixture(scope="module")
def ac_conformance_runtime(
    conformance_runtime_root: Path, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    source_parent = tmp_path_factory.mktemp("sp03-ac-source-")
    install_parent = tmp_path_factory.mktemp("sp03-ac-runtime-")
    return _install_ac_compiler_runtime(
        source_parent / "source",
        conformance_runtime_root,
        install_parent / "GAME",
    )


def test_issued_ac_calculation_uses_target_dex_and_keeps_multiple_bases_unselected(
    ac_conformance_runtime: Path,
) -> None:
    default_case = _run_ac_case(
        ac_conformance_runtime,
        {
            "caster_abilities": {"ability.dexterity": {"base": 20}},
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": [],
            "assets": [],
        },
    )
    assert default_case["status"] == "OK", default_case
    assert default_case["context_issued"] is True
    assert default_case["role_bindings"]["target"]["identity"] == ["actor.ac.subject"]
    native_ability_basis = default_case["result"]["native_base_inputs"][
        "native_ability_basis"
    ]
    assert native_ability_basis["resolved_score"] == 16
    assert native_ability_basis["dexterity_modifier"] == 3
    assert default_case["result"]["trace"]["base_candidates"][0]["base_value"] == 13
    assert default_case["result"]["selection_status"] == "SELECTED_SOLE_LEGAL_BASE"
    assert default_case["result"]["selected_ac"] == 13
    assert default_case["result"]["context_facts"] == []
    assert default_case["result"]["rng_draw_count"] == 0
    assert default_case["fixed_rng_results"] == []
    assert (
        default_case["revision_before_calculation"]
        == default_case["revision_after_calculation"]
    )

    held_case = _run_ac_case(
        ac_conformance_runtime,
        {
            "caster_abilities": {"ability.dexterity": {"base": 20}},
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor", "shield"],
            "assets": [],
        },
    )
    assert held_case["status"] == "OK", held_case
    held_result = held_case["result"]
    candidates = held_result["trace"]["base_candidates"]
    assert [(row["base_kind"], row["base_value"]) for row in candidates] == [
        ("MAGE_ARMOR_13_PLUS_DEX", 16),
        ("UNARMORED_10_PLUS_DEX", 13),
    ]
    assert held_result["modifier_total"] == 5
    assert held_result["selection_status"] == "CHOICE_REQUIRED"
    assert "selected_ac" not in held_result


def test_ac_native_dexterity_precedence_adjustment_and_floor(
    ac_conformance_runtime: Path,
) -> None:
    cases = (
        (
            {
                "caster_abilities": {"ability.dexterity": {"base": 20}},
                "subject_abilities": {"ability.dexterity": {"base": 17}},
            },
            "ACTOR_STATE",
            17,
            3,
            13,
        ),
        (
            {
                "subject_abilities": {"ability.dexterity": {"base": 9}},
            },
            "ACTOR_STATE",
            9,
            -1,
            9,
        ),
        (
            {
                "subject_abilities": {"ability.dexterity": {"adjustment": 1}},
            },
            "ACTOR_ARCHETYPE",
            16,
            3,
            13,
        ),
        (
            {"subject_abilities": None},
            "ACTOR_ARCHETYPE",
            15,
            2,
            12,
        ),
    )
    for case, base_source, score, modifier, expected_ac in cases:
        evidence = _run_ac_case(ac_conformance_runtime, case)
        assert evidence["status"] == "OK", evidence
        result = evidence["result"]
        ability = result["native_base_inputs"]["native_ability_basis"]
        assert ability["base_source"] == base_source
        assert ability["resolved_score"] == score
        assert ability["dexterity_modifier"] == modifier
        assert result["selection_status"] == "SELECTED_SOLE_LEGAL_BASE"
        assert result["selected_ac"] == expected_ac
        assert evidence["fixed_rng_results"] == []
        assert (
            evidence["revision_before_calculation"]
            == evidence["revision_after_calculation"]
        )


def test_ac_source_and_worn_armor_gates_do_not_use_names_or_carried_armor(
    ac_conformance_runtime: Path,
) -> None:
    lookalike = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor_lookalike"],
        },
    )
    assert lookalike["status"] == "OK", lookalike
    assert lookalike["result"]["selection_status"] == "SELECTED_SOLE_LEGAL_BASE"
    assert [
        row["base_kind"] for row in lookalike["result"]["trace"]["base_candidates"]
    ] == ["UNARMORED_10_PLUS_DEX"]
    assert lookalike["result"]["trace"]["base_contributions"][0][
        "rejection_reasons"
    ] == ["SOURCE_NOT_ELIGIBLE"]

    false_predicate = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor_false"],
        },
    )
    assert false_predicate["status"] == "OK", false_predicate
    assert false_predicate["result"]["selection_status"] == "SELECTED_SOLE_LEGAL_BASE"
    assert false_predicate["result"]["trace"]["base_contributions"][0][
        "rejection_reasons"
    ] == ["PREDICATE_FALSE"]

    wrong_target = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": [{"name": "mage_armor", "target_id": "actor.sp03"}],
        },
    )
    assert wrong_target["status"] == "OK", wrong_target
    assert [
        row["base_kind"] for row in wrong_target["result"]["trace"]["base_candidates"]
    ] == ["UNARMORED_10_PLUS_DEX"]

    worn_armor = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor"],
            "assets": [
                {
                    "asset_id": "asset.target.armor",
                    "definition_id": "asset.sp03.ac.armor",
                    "equipment_mode": "worn",
                }
            ],
        },
    )
    assert worn_armor["status"] == "HOLD"
    assert worn_armor["hold_status"] == "AUTHORITY_UNAVAILABLE"

    carried_armor = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor"],
            "assets": [
                {
                    "asset_id": "asset.target.carried_armor",
                    "definition_id": "asset.sp03.ac.armor",
                    "equipment_mode": None,
                }
            ],
        },
    )
    assert carried_armor["status"] == "OK", carried_armor
    assert carried_armor["result"]["selection_status"] == "CHOICE_REQUIRED"
    assert "selected_ac" not in carried_armor["result"]

    worn_nonarmor = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor"],
            "assets": [
                {
                    "asset_id": "asset.target.wearable",
                    "definition_id": "asset.sp03.ac.wearable",
                    "equipment_mode": "worn",
                }
            ],
        },
    )
    assert worn_nonarmor["status"] == "OK", worn_nonarmor
    assert worn_nonarmor["result"]["selection_status"] == "CHOICE_REQUIRED"


@pytest.mark.parametrize(
    "effects",
    (
        pytest.param(
            [
                {
                    "name": "mage_armor",
                    "effect_id": "effect.application.mage_armor.first",
                },
                {
                    "name": "mage_armor",
                    "effect_id": "effect.application.mage_armor.second",
                },
            ],
            id="first-then-second",
        ),
        pytest.param(
            [
                {
                    "name": "mage_armor",
                    "effect_id": "effect.application.mage_armor.second",
                },
                {
                    "name": "mage_armor",
                    "effect_id": "effect.application.mage_armor.first",
                },
            ],
            id="second-then-first",
        ),
    ),
)
def test_ac_holds_multiple_mage_armor_applications_without_arbitration(
    ac_conformance_runtime: Path,
    effects: list[dict[str, str]],
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": effects,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_calculation_holds_duplicate_mage_armor_elements_after_cold_bypass(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor"],
            "duplicate_mage_armor_ac_elements": True,
            "bypass_cold_source_validation": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_native_actor_base_does_not_bypass_unproved_build_grants(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "build": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


@pytest.mark.parametrize(
    "subject_abilities",
    (
        pytest.param({"ability.dexterity": {"base": 16}}, id="actor-base"),
        pytest.param(None, id="archetype-base"),
    ),
)
def test_ac_native_base_holds_unproved_archetype_feature_grants(
    ac_conformance_runtime: Path,
    subject_abilities: dict[str, dict[str, int]] | None,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": subject_abilities,
            "subject_archetype_feature_ids": ["feature.ac.unresolved"],
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


@pytest.mark.parametrize(
    "mage_armor_effects",
    (
        pytest.param(
            [
                {
                    "name": "mage_armor",
                    "support_effect_id": "effect.application.ac.support_parent",
                },
                {"name": "support_parent", "target_id": "actor.sp03"},
            ],
            id="active-support-parent",
        ),
        pytest.param(
            [{"name": "mage_armor", "omit_rules_origin_id": True}],
            id="missing-rule-origin",
        ),
        pytest.param(
            [{"name": "mage_armor", "rules_origin_id": "source.spell.other"}],
            id="inconsistent-rule-origin",
        ),
    ),
)
def test_ac_holds_potential_mage_armor_with_unproved_support_or_provenance(
    ac_conformance_runtime: Path,
    mage_armor_effects: list[dict[str, object]],
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": mage_armor_effects,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_false_mage_armor_predicate_remains_rejected_with_unproved_support(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": [
                {
                    "name": "mage_armor_false",
                    "support_effect_id": "effect.application.ac.support_parent",
                },
                {"name": "support_parent", "target_id": "actor.sp03"},
            ],
        },
    )
    assert evidence["status"] == "OK", evidence
    assert evidence["result"]["selection_status"] == "SELECTED_SOLE_LEGAL_BASE"
    assert (
        evidence["result"]["trace"]["base_contributions"][0]["rejection_reasons"][0]
        == "PREDICATE_FALSE"
    )


def test_ac_flat_modifiers_sum_without_selecting_or_adding_bases(
    ac_conformance_runtime: Path,
) -> None:
    case = {
        "subject_abilities": {"ability.dexterity": {"base": 16}},
        "effects": ["shield"],
        "assets": [
            {
                "asset_id": "asset.target.shield",
                "definition_id": "asset.sp03.ac.shield",
                "equipment_mode": "held",
            }
        ],
    }
    evidence = _run_ac_case(ac_conformance_runtime, case)
    assert evidence["status"] == "OK", evidence
    result = evidence["result"]
    assert result["trace"]["base_candidates"][0]["base_value"] == 13
    assert result["modifier_total"] == 7
    assert result["selected_ac"] == 20
    assert [row["value"] for row in result["trace"]["modifier_contributions"]] == [2, 5]

    permuted = _run_ac_case(
        ac_conformance_runtime,
        {
            **case,
            "effects": list(reversed(case["effects"])),
            "assets": list(reversed(case["assets"])),
        },
    )
    assert permuted["status"] == "OK", permuted
    permuted_result = permuted["result"]
    assert permuted_result["modifier_total"] == result["modifier_total"]
    assert permuted_result["selected_ac"] == result["selected_ac"]
    assert [
        (row["source_owner_ref"]["family_key"], row["value"])
        for row in permuted_result["trace"]["modifier_contributions"]
    ] == [
        (row["source_owner_ref"]["family_key"], row["value"])
        for row in result["trace"]["modifier_contributions"]
    ]


def test_ac_unproved_build_dynamic_ability_and_stale_context_hold(
    ac_conformance_runtime: Path,
) -> None:
    cases = (
        {"subject_abilities": None, "subject_definition_id": "actor_archetype.missing"},
        {"subject_abilities": {"ability.dexterity": {"base": True}}},
        {"subject_abilities": {"dex": {"base": 16}}},
        {"subject_abilities": None, "build": True},
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["ability_change"],
        },
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "change_target_after_issue": True,
        },
    )
    for case in cases:
        evidence = _run_ac_case(ac_conformance_runtime, case)
        assert evidence["status"] in {"HOLD", "CALCULATION_ERROR"}, evidence
        assert evidence.get("result") is None


def test_ac_base_choice_has_no_caller_choice_or_order_fallback(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor", "shield"],
        },
    )
    assert evidence["status"] == "OK", evidence
    result = evidence["result"]
    assert result["selection_status"] == "CHOICE_REQUIRED"
    assert result["modifier_total"] == 5
    assert {row["base_value"] for row in result["trace"]["base_candidates"]} == {13, 16}
    assert "selected_ac" not in result
    assert "selected_base_kind" not in result
    assert evidence["context_issued"] is True
    assert evidence["fixed_rng_results"] == []
    assert evidence["accepted_fact_refs"] == []


def test_ac_duplicate_shields_require_existing_effect_arbitration(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "shield_arbitration_policy_id": "effect_arbitration.potency_then_recency",
            "effects": [
                {"name": "shield"},
                {"name": "shield", "effect_id": "effect.application.shield.second"},
            ],
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_duplicate_shields_without_arbitration_declaration_hold(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": [
                {"name": "shield"},
                {"name": "shield", "effect_id": "effect.application.shield.second"},
            ],
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_duplicate_shield_elements_in_one_application_hold(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["shield"],
            "duplicate_shield_ac_elements": True,
            "bypass_cold_source_validation": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_exact_shield_definition_retyped_as_asset_holds(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "shield_definition_kind": "definition.asset",
            "assets": [
                {
                    "asset_id": "asset.target.retyped_shield",
                    "definition_id": "effect.spell.shield",
                    "equipment_mode": "held",
                }
            ],
            "bypass_cold_source_validation": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_ac_unproved_effect_arbitration_holds_even_for_one_shield(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "shield_arbitration_policy_id": "effect_arbitration.unproved",
            "effects": ["shield"],
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_single_unarbitrated_shield_selects_default_ac_18(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["shield"],
        },
    )
    assert evidence["status"] == "OK", evidence
    assert evidence["result"]["modifier_total"] == 5
    assert evidence["result"]["selected_ac"] == 18


def test_required_asset_attunement_controls_ac_modifier_eligibility(
    ac_conformance_runtime: Path,
) -> None:
    cases = (
        ({}, "SOURCE_NOT_ELIGIBLE", 13),
        ({"attuned_actor_id": "actor.sp03"}, "SOURCE_NOT_ELIGIBLE", 13),
        ({"attuned_actor_id": "actor.ac.subject"}, None, 15),
    )
    for asset_state, rejection, selected_ac in cases:
        evidence = _run_ac_case(
            ac_conformance_runtime,
            {
                "subject_abilities": {"ability.dexterity": {"base": 16}},
                "assets": [
                    {
                        "asset_id": "asset.target.attuned_shield",
                        "definition_id": "asset.sp03.ac.attuned_shield",
                        "equipment_mode": "held",
                        **asset_state,
                    }
                ],
            },
        )
        assert evidence["status"] == "OK", evidence
        result = evidence["result"]
        assert result["selected_ac"] == selected_ac
        assert result["modifier_total"] == (0 if rejection else 2)
        if rejection:
            assert result["trace"]["modifier_contributions"][0][
                "rejection_reasons"
            ] == [rejection]

    unproved_prerequisite = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "assets": [
                {
                    "asset_id": "asset.target.class_limited_shield",
                    "definition_id": "asset.sp03.ac.class_limited_shield",
                    "equipment_mode": "held",
                    "attuned_actor_id": "actor.ac.subject",
                }
            ],
        },
    )
    assert unproved_prerequisite["status"] == "HOLD", unproved_prerequisite
    assert unproved_prerequisite["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in unproved_prerequisite


def test_mage_armor_flat_source_is_rejected_and_consumption_holds(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["mage_armor"],
            "mage_armor_as_flat": True,
            "bypass_cold_source_validation": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


@pytest.mark.parametrize("unsupported_member", ("gate", "priority", "stacking_key"))
def test_ac_consumption_holds_unmodeled_rule_element_members(
    ac_conformance_runtime: Path,
    unsupported_member: str,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["modifier_pair"],
            "unsupported_modifier_member": unsupported_member,
            "bypass_cold_source_validation": True,
        },
    )
    assert evidence["status"] == "HOLD", evidence
    assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"
    assert "result" not in evidence


def test_mechanical_context_retains_source_bound_dex_and_equipment_inputs(
    ac_conformance_runtime: Path,
) -> None:
    evidence = _run_ac_case(
        ac_conformance_runtime,
        {
            "raw_only": True,
            "caster_abilities": {"ability.dexterity": {"base": 20}},
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": [],
            "assets": [],
        },
    )
    assert evidence["status"] == "RAW", evidence
    raw_selector = evidence["raw_selector"]["selector_result"]
    native_base = raw_selector["native_base_inputs"]["native_ability_basis"]
    assert native_base["subject_owner_ref"]["identity"] == ["actor.ac.subject"]
    assert native_base["ability_id"] == "ability.dexterity"
    assert native_base["base_score"] == 16
    assert native_base["dexterity_modifier"] == 3
    assert raw_selector["native_base_inputs"]["equipment_membership"]["assets"] == []


def test_ac_unresolved_native_dex_and_dynamic_sources_hold(
    ac_conformance_runtime: Path,
) -> None:
    cases = (
        {"subject_abilities": {"dex": {"base": 16}}},
        {"subject_abilities": {"ability.dexterity": {"base": True}}},
        {"subject_abilities": None, "subject_definition_id": "actor_archetype.missing"},
        {"subject_abilities": None, "build": True},
        {"subject_abilities": {"ability.dexterity": {"base": 16}}, "embodiment": True},
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "effects": ["ability_change"],
        },
    )
    for case in cases:
        evidence = _run_ac_case(ac_conformance_runtime, case)
        assert evidence["status"] == "HOLD", evidence
        assert evidence["hold_status"] == "AUTHORITY_UNAVAILABLE"


def test_ac_shield_modifiers_are_additive_permutation_invariant_and_separate_from_base(
    ac_conformance_runtime: Path,
) -> None:
    case = {
        "subject_abilities": {"ability.dexterity": {"base": 16}},
        "effects": ["shield", "modifier_pair"],
        "assets": [],
    }
    first = _run_ac_case(ac_conformance_runtime, case)
    assert first["status"] == "OK", first
    result = first["result"]
    assert result["trace"]["base_candidates"][0]["base_value"] == 13
    assert result["modifier_total"] == 10
    assert result["selected_ac"] == 23
    assert sorted(
        row["value"] for row in result["trace"]["modifier_contributions"]
    ) == [2, 3, 5]

    reversed_inputs = _run_ac_case(
        ac_conformance_runtime,
        {
            **case,
            "effects": list(reversed(case["effects"])),
            "modifier_order": (3, 2),
        },
    )
    assert reversed_inputs["status"] == "OK", reversed_inputs
    reversed_result = reversed_inputs["result"]
    assert reversed_result["modifier_total"] == result["modifier_total"]
    assert reversed_result["selected_ac"] == result["selected_ac"]
    assert sorted(
        row["value"] for row in reversed_result["trace"]["modifier_contributions"]
    ) == [2, 3, 5]

    held_asset = _run_ac_case(
        ac_conformance_runtime,
        {
            "subject_abilities": {"ability.dexterity": {"base": 16}},
            "assets": [
                {
                    "asset_id": "asset.target.shield",
                    "definition_id": "asset.sp03.ac.shield",
                    "equipment_mode": "held",
                }
            ],
        },
    )
    assert held_asset["status"] == "OK", held_asset
    assert held_asset["result"]["modifier_total"] == 2
    assert held_asset["result"]["selected_ac"] == 15
