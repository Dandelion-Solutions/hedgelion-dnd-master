"""Finite Sorcerer source bindings and source-basis result contracts."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource

from GAME.TOOLS import activity_contracts as contracts

pytest_plugins = ("DEV.TESTS.test_local_spell_catalog",)

ROOT = Path(__file__).resolve().parents[2]
PROFILE_SCHEMA = ROOT / "DEV/SCHEMAS/spell-native-profile-values.schema.json"
COMPILER_SCHEMA = ROOT / "DEV/SCHEMAS/activity-compiler-declaration.schema.json"

CLASS_REF = {"definition_id": "class.sorcerer", "kind": "definition.class"}
ADVANCEMENT_REF = {
    "definition_id": "advancement.sorcerer.mvp_1",
    "kind": "definition.advancement",
}
SPELLCASTING_FEATURE_REF = {
    "definition_id": "feature.sorcerer.spellcasting",
    "kind": "definition.feature",
}
INNATE_SORCERY_FEATURE_REF = {
    "definition_id": "feature.sorcerer.innate_sorcery",
    "kind": "definition.feature",
}
INNATE_SORCERY_EFFECT_REF = {
    "definition_id": "effect.innate_sorcery",
    "kind": "definition.effect",
}
MAGIC_MISSILE_REF = {
    "definition_id": "spell.magic_missile",
    "kind": "definition.spell",
}
MAGIC_MISSILE_ACTIVITY_REF = {
    "definition_id": "activity.spell.magic_missile",
    "kind": "definition.activity",
}

CANTRIP_SLOT_ID = "advancement.sorcerer.level_1.cantrips"
PREPARED_SLOT_ID = "advancement.sorcerer.level_1.prepared_spells"
CANTRIP_IDS = (
    "spell.acid_splash",
    "spell.fire_bolt",
    "spell.poison_spray",
    "spell.thunderclap",
)
LEVEL1_IDS = ("spell.burning_hands", "spell.magic_missile")
KNOWN_IDS = tuple(sorted((*CANTRIP_IDS, *LEVEL1_IDS)))


def _seed_source_records(seed: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        record["id"]: record
        for group in ("definitions", "support_definitions", "activity_definitions")
        for record in seed.get(group, ())
    }


def _reference_closure(
    records: dict[str, dict[str, Any]], roots: tuple[str, ...]
) -> tuple[str, ...]:
    visited: set[str] = set()
    pending = list(roots)
    while pending:
        identity = pending.pop()
        if identity in visited:
            continue
        record = records.get(identity)
        visited.add(identity)
        if record is None:
            continue
        kind = record.get("kind")
        data = record.get("data", {})
        for reference in record.get("references", ()):
            if reference in records or str(reference).startswith(
                ("definition.", "activity.")
            ):
                pending.append(reference)
        if kind == "definition.class" and isinstance(data, dict):
            advancement_id = data.get("advancement_id")
            if isinstance(advancement_id, str):
                pending.append(advancement_id)
        elif kind == "definition.advancement":
            if isinstance(data, dict):
                for level in data.get("levels", ()):
                    if isinstance(level, dict):
                        pending.extend(level.get("automatic_grant_definition_ids", ()))
            for slot in record.get("choice_slots", ()):
                if not isinstance(slot, dict):
                    continue
                for option in slot.get("options", ()):
                    if not isinstance(option, dict):
                        continue
                    pending.extend(option.get("grant_definition_ids", ()))
                    pending.extend(
                        asset.get("definition_id")
                        for asset in option.get("starting_assets", ())
                        if isinstance(asset, dict)
                    )
        elif kind in {"definition.feature", "definition.spell"} and isinstance(
            data, dict
        ):
            for member in ("activity_ids", "resource_ids", "effect_ids"):
                if isinstance(data.get(member, ()), (list, tuple)):
                    pending.extend(data.get(member, ()))
    return tuple(sorted(visited))


_SEED_PATH = (
    ROOT / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
)
_BASE_SEED = json.loads(_SEED_PATH.read_text(encoding="utf-8"))
_BASE_SOURCE_RECORDS = _seed_source_records(_BASE_SEED)
SPELL_REFS = tuple(
    {"definition_id": spell_id, "kind": "definition.spell"} for spell_id in KNOWN_IDS
)
ACTIVITY_IDS = tuple(
    sorted(
        activity_id
        for spell_id in KNOWN_IDS
        for activity_id in _BASE_SOURCE_RECORDS[spell_id]["data"]["activity_ids"]
    )
)


def _activity_primitive_ids(value: object) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        operation_id = value.get("op")
        if isinstance(operation_id, str):
            result.add(operation_id)
        for child in value.values():
            if isinstance(child, (dict, list, tuple)):
                result.update(_activity_primitive_ids(child))
    elif isinstance(value, (list, tuple)):
        for child in value:
            result.update(_activity_primitive_ids(child))
    return result


DEFINITION_REFS = tuple(
    {
        "definition_id": identity,
        "kind": str(_BASE_SOURCE_RECORDS[identity]["kind"]),
    }
    for identity in _reference_closure(
        _BASE_SOURCE_RECORDS, ("class.sorcerer", "spell.magic_missile")
    )
)
ALL_SOURCE_ACTIVITY_IDS = tuple(
    reference["definition_id"]
    for reference in DEFINITION_REFS
    if reference["kind"] == "definition.activity"
)
SOURCE_ACTIVITY_PRIMITIVE_IDS = {
    activity_id: tuple(
        sorted(
            _activity_primitive_ids(_BASE_SOURCE_RECORDS[activity_id]["data"]["steps"])
        )
    )
    for activity_id in ALL_SOURCE_ACTIVITY_IDS
}
ACTIVITY_REFS = tuple(
    reference
    for reference in DEFINITION_REFS
    if reference["kind"] == "definition.activity"
)
DEFINITION_DEPENDENCIES = [
    f"bound_definition:{reference['definition_id']}" for reference in DEFINITION_REFS
]
SOURCE_ROOT_DEPENDENCIES = [
    "bound_definition:class.sorcerer",
    "bound_definition:spell.magic_missile",
]
FACET_KEYS = (
    "class_progression",
    "acquisition",
    "source_spell",
    "source_mode",
    "activity_closure",
    "source_ability",
    "proficiency",
    "base_spell_values",
    "final_modifier_closure",
    "movement",
    "senses",
    "anatomy",
    "equipment",
    "form",
)


def _schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _capability_binding() -> dict[str, object]:
    return {
        "consumer_id": "activity.conformance.compiler.step.0",
        "profile_id": "calculation.capability_projection_srd521",
        "profile_generation": 1,
        "source_variant": "SORCERER_1",
        "source_definition_refs": list(copy.deepcopy(DEFINITION_REFS)),
        "source_spell_id": "spell.magic_missile",
        "choice_slots": [
            {"slot_id": CANTRIP_SLOT_ID, "minimum": 4, "maximum": 4},
            {"slot_id": PREPARED_SLOT_ID, "minimum": 2, "maximum": 2},
        ],
        "source_ability_id": "ability.charisma",
        "native_role_bindings": [
            {
                "read_ref": "bound_definition:class.sorcerer",
                "role_names": ["actor"],
            }
        ],
        "dependency_refs": list(SOURCE_ROOT_DEPENDENCIES),
        "context_fact_ids": [],
        "evaluated_facets": [
            "source_class",
            "acquisition",
            "source_ability",
            "proficiency",
        ],
    }


def _cast_binding() -> dict[str, object]:
    return {
        "consumer_id": "activity.conformance.compiler.step.0",
        "profile_id": "execution.spell_cast.srd521",
        "profile_generation": 1,
        "source_variant": "SORCERER_1",
        "source_definition_refs": list(copy.deepcopy(DEFINITION_REFS)),
        "source_spell_id": "spell.magic_missile",
        "choice_slots": [
            {"slot_id": CANTRIP_SLOT_ID, "minimum": 4, "maximum": 4},
            {"slot_id": PREPARED_SLOT_ID, "minimum": 2, "maximum": 2},
        ],
        "source_ability_id": "ability.charisma",
        "native_role_bindings": [
            {
                "read_ref": "bound_definition:class.sorcerer",
                "role_names": ["actor"],
            }
        ],
        "dependency_refs": list(SOURCE_ROOT_DEPENDENCIES),
        "context_fact_ids": [],
        "evaluated_facets": [
            "source_spell",
            "activity_closure",
            "source_ability",
            "proficiency",
        ],
    }


def _source_basis_result(
    *,
    score: int = 16,
    adjustment: int = 0,
    source_spell_id: str = "spell.magic_missile",
    source_spell_level: int | None = None,
    acquisition_evidence: bool = True,
    ability_evidence: bool = True,
    source_disposition: str | None = None,
    additional_source_definition_refs: tuple[dict[str, str], ...] = (),
    consumer_id: str = "activity.conformance.compiler.step.0",
    activity_id: str = "activity.conformance.compiler",
) -> dict[str, object]:
    cantrips = list(CANTRIP_IDS)
    level1 = list(LEVEL1_IDS)
    known = sorted((*cantrips, *level1))
    if source_spell_level is None:
        source_spell_level = _BASE_SOURCE_RECORDS.get(
            source_spell_id, {"data": {"level": 1}}
        )["data"]["level"]
    selected_cantrip = source_spell_level == 0 and source_spell_id in cantrips
    selected_prepared = source_spell_level == 1 and source_spell_id in level1
    if source_disposition is None:
        if not acquisition_evidence:
            source_disposition = "NOT_EVALUATED"
        elif selected_cantrip:
            source_disposition = "SELECTED_KNOWN_CANTRIP"
        elif selected_prepared:
            source_disposition = "SELECTED_PREPARED_LEVEL1"
        elif source_spell_level > 1:
            source_disposition = "PROHIBITED"
        else:
            source_disposition = "UNAVAILABLE"
    ability_modifier = (score - 10) // 2
    facets = {facet: "NOT_EVALUATED" for facet in FACET_KEYS}
    facets["source_mode"] = "NOT_EVALUATED"
    activity_closure_ids: list[str] = []
    acquisition = None
    if acquisition_evidence:
        facets["class_progression"] = "RESOLVED"
        facets["acquisition"] = "RESOLVED"
        facets["activity_closure"] = "RESOLVED"
        activity_closure_ids = list(ACTIVITY_IDS)
        facets["source_spell"] = {
            "SELECTED_KNOWN_CANTRIP": "RESOLVED",
            "SELECTED_PREPARED_LEVEL1": "RESOLVED",
            "UNAVAILABLE": "UNAVAILABLE",
            "PROHIBITED": "PROHIBITED",
            "NOT_EVALUATED": "NOT_EVALUATED",
        }[source_disposition]
        acquisition = {
            "class_progression": [{"class_id": "class.sorcerer", "level": 1}],
            "advancement_id": "advancement.sorcerer.mvp_1",
            "spellcasting_feature_id": "feature.sorcerer.spellcasting",
            "cantrip_choice_slot_id": CANTRIP_SLOT_ID,
            "cantrip_spell_ids": cantrips,
            "cantrip_option_ids": [f"option.{spell_id}" for spell_id in cantrips],
            "prepared_choice_slot_id": PREPARED_SLOT_ID,
            "level1_spell_ids": level1,
            "prepared_option_ids": [f"option.{spell_id}" for spell_id in level1],
            "known_spell_ids": known,
            "prepared_spell_ids": sorted(level1),
        }
        if ability_evidence:
            for facet in ("source_ability", "proficiency", "base_spell_values"):
                facets[facet] = "RESOLVED"
    source_spell_ref = {
        "definition_id": source_spell_id,
        "kind": "definition.spell",
    }
    definition_refs = sorted(
        [
            *copy.deepcopy(DEFINITION_REFS),
            *(
                []
                if source_spell_id
                in {reference["definition_id"] for reference in SPELL_REFS}
                else [source_spell_ref]
            ),
            *copy.deepcopy(additional_source_definition_refs),
        ],
        key=lambda reference: reference["definition_id"],
    )
    read_refs = sorted(
        [
            *(
                f"bound_definition:{reference['definition_id']}"
                for reference in definition_refs
            ),
        ]
    )
    source_actor_ref = {
        "family_key": "world.actor",
        "identity": ["actor.sorcerer"],
    }
    return {
        "consumer_id": consumer_id,
        "profile_id": "calculation.capability_projection_srd521",
        "profile_generation": 1,
        "activity_id": activity_id,
        "source_actor_ref": source_actor_ref,
        "source_spell_id": source_spell_id,
        "source_spell_level": source_spell_level,
        "mode_id": None,
        "activity_closure_ids": activity_closure_ids,
        "source_definition_refs": definition_refs,
        "read_refs": read_refs,
        "context_facts": [],
        "source_disposition": source_disposition,
        "acquisition": acquisition,
        "ability_basis": (
            {
                "ability_id": "ability.charisma",
                "base_source": "ACTOR",
                "base_source_ref": {
                    "kind": "ACTOR",
                    "source_actor_ref": source_actor_ref,
                },
                "base_score": score - adjustment,
                "adjustment": adjustment,
                "score": score,
                "modifier": ability_modifier,
                "proficiency_bonus": 2,
                "base_spell_save_dc": 8 + ability_modifier + 2,
                "base_spell_attack_bonus": ability_modifier + 2,
                "modifier_source_definition_ids": ["effect.innate_sorcery"],
            }
            if acquisition_evidence and ability_evidence
            else None
        ),
        "facets": facets,
    }


def test_source_binding_schemas_are_finite_and_wired_into_compiler_declarations() -> (
    None
):
    profile_schema = _schema(PROFILE_SCHEMA)
    compiler_schema = _schema(COMPILER_SCHEMA)
    definitions = profile_schema["$defs"]

    assert "capabilitySourceBinding" in definitions
    assert "castSourceBinding" in definitions
    assert "sourceBasisResult" in definitions
    assert "capability_sources" in compiler_schema["properties"]
    assert "cast_sources" in compiler_schema["properties"]

    for name, value in (
        ("capabilitySourceBinding", _capability_binding()),
        ("castSourceBinding", _cast_binding()),
    ):
        root = {
            "$schema": profile_schema["$schema"],
            "$defs": definitions,
            "allOf": [definitions[name]],
        }
        Draft202012Validator(root).validate(value)

    declaration = {
        "roles": {"actor": "world.actor"},
        "symbols": {},
        "profiles": [],
        "capability_sources": [_capability_binding()],
        "cast_sources": [_cast_binding()],
    }
    registry = Registry().with_resource(
        profile_schema["$id"], Resource.from_contents(profile_schema)
    )
    Draft202012Validator(compiler_schema, registry=registry).validate(declaration)
    with pytest.raises(ValidationError):
        Draft202012Validator(compiler_schema, registry=registry).validate(
            {**declaration, "cast_sources": [{**_cast_binding(), "arguments": {}}]}
        )


def test_spell_source_modes_are_optional_closed_exact_route_rows() -> None:
    spell_schema = _schema(ROOT / "DEV/SCHEMAS/spell-definition-data.schema.json")
    value = {
        "level": 1,
        "school_id": "school.evocation",
        "activity_ids": ["activity.spell.magic_missile"],
        "source_modes": [
            {
                "mode_id": "mode.magic_missile.ordinary",
                "activity_id": "activity.spell.magic_missile",
            }
        ],
    }

    Draft202012Validator(spell_schema).validate(value)
    Draft202012Validator(spell_schema).validate(
        {key: item for key, item in value.items() if key != "source_modes"}
    )

    invalid = copy.deepcopy(value)
    invalid["source_modes"][0]["fallback_activity_id"] = "activity.spell.fire_bolt"
    with pytest.raises(ValidationError):
        Draft202012Validator(spell_schema).validate(invalid)
    with pytest.raises(ValidationError):
        Draft202012Validator(spell_schema).validate({**value, "source_modes": []})

    from DEV.TOOLS import build_activity_contract_shapes as shape_builder

    projection = shape_builder.build_projection(ROOT)
    source_schema_id = (
        "https://hedgelion.invalid/schemas/spell-definition-data.schema.json"
    )
    assert source_schema_id in projection["schemas"]
    assert projection["named"]["source_mode"] == {
        "$ref": source_schema_id + "#/$defs/sourceMode"
    }


def test_source_basis_validator_accepts_only_sorcerer1_base_values_and_explicit_unknown_facets() -> (
    None
):
    result = contracts.SourceBasisResult(_source_basis_result(score=16))
    assert isinstance(result, contracts.SourceBasisResult)
    assert result.value["ability_basis"]["base_spell_save_dc"] == 13
    assert result.value["ability_basis"]["base_spell_attack_bonus"] == 5
    assert result.value["ability_basis"]["modifier_source_definition_ids"] == (
        "effect.innate_sorcery",
    )
    assert result.value["facets"]["final_modifier_closure"] == "NOT_EVALUATED"
    assert result.value["facets"]["movement"] == "NOT_EVALUATED"
    with pytest.raises(TypeError):
        result.value["ability_basis"]["modifier"] = 99


def test_source_mode_value_is_closed_and_uses_exact_local_keys() -> None:
    mode = contracts.SourceMode(
        mode_id="mode.magic_missile.ordinary",
        activity_id="activity.spell.magic_missile",
    )

    assert mode.mode_id == "mode.magic_missile.ordinary"
    assert mode.activity_id == "activity.spell.magic_missile"

    with pytest.raises(TypeError):
        contracts.SourceMode(
            mode_id="mode.magic_missile.ordinary",
            activity_id="activity.spell.magic_missile",
            description="not an admitted member",
        )


def test_named_source_route_result_has_a_closed_projection_contract() -> None:
    profile_schema = _schema(PROFILE_SCHEMA)
    result_schema = profile_schema["$defs"]["namedSourceRouteResult"]
    assert result_schema["additionalProperties"] is False
    assert "source_disposition" in result_schema["required"]
    assert "mode_declaration" in result_schema["required"]
    assert "source_spell_definition" in result_schema["required"]
    assert "selected_activity_definition" in result_schema["required"]
    assert "source_dependency_edge" in result_schema["required"]
    assert "context_identity" in result_schema["required"]
    assert "membership_identity" in result_schema["required"]
    assert "cast_permission" not in result_schema["properties"]

    from DEV.TOOLS import build_activity_contract_shapes as shape_builder

    projection = shape_builder.build_projection(ROOT)
    assert projection["named"]["named_source_route_result"] == {
        "$ref": "https://hedgelion.invalid/schemas/spell-native-profile-values.schema.json#/$defs/namedSourceRouteResult"
    }


@pytest.mark.parametrize(
    ("mutation", "source_spell_id"),
    [
        ("boolean-score", "spell.magic_missile"),
        ("wrong-ability", "spell.magic_missile"),
        ("wrong-proficiency", "spell.magic_missile"),
        ("wrong-base-dc", "spell.magic_missile"),
        ("wrong-base-attack", "spell.magic_missile"),
        ("wrong-base-source-reference", "spell.magic_missile"),
        ("overlapping-selection", "spell.magic_missile"),
        ("wrong-known-union", "spell.magic_missile"),
        ("wrong-prepared-set", "spell.magic_missile"),
        ("wrong-cantrip-option-binding", "spell.magic_missile"),
        ("wrong-prepared-option-binding", "spell.magic_missile"),
        ("missing-innate-sorcery-source", "spell.magic_missile"),
        ("final-modifier-claimed-resolved", "spell.magic_missile"),
        ("unknown-facet", "spell.magic_missile"),
        ("unselected-spell-marked-resolved", "spell.shield"),
    ],
)
def test_source_basis_validator_rejects_noncanonical_or_unselected_source_results(
    mutation: str, source_spell_id: str
) -> None:
    value = _source_basis_result(source_spell_id=source_spell_id)
    if mutation == "boolean-score":
        value["ability_basis"]["score"] = True
    elif mutation == "wrong-ability":
        value["ability_basis"]["ability_id"] = "ability.dexterity"
    elif mutation == "wrong-proficiency":
        value["ability_basis"]["proficiency_bonus"] = 3
    elif mutation == "wrong-base-dc":
        value["ability_basis"]["base_spell_save_dc"] = 14
    elif mutation == "wrong-base-attack":
        value["ability_basis"]["base_spell_attack_bonus"] = 6
    elif mutation == "wrong-base-source-reference":
        value["ability_basis"]["base_source"] = "ARCHETYPE"
    elif mutation == "overlapping-selection":
        value["acquisition"]["cantrip_spell_ids"].append("spell.magic_missile")
        value["acquisition"]["known_spell_ids"].append("spell.magic_missile")
    elif mutation == "wrong-known-union":
        value["acquisition"]["known_spell_ids"].pop()
    elif mutation == "wrong-prepared-set":
        value["acquisition"]["prepared_spell_ids"] = ["spell.shield"]
    elif mutation == "wrong-cantrip-option-binding":
        value["acquisition"]["cantrip_option_ids"][0] = "option.spell.shield"
    elif mutation == "wrong-prepared-option-binding":
        value["acquisition"]["prepared_option_ids"][0] = "option.spell.shield"
    elif mutation == "missing-innate-sorcery-source":
        value["ability_basis"]["modifier_source_definition_ids"] = []
        value["source_definition_refs"] = [
            ref
            for ref in value["source_definition_refs"]
            if ref["definition_id"] != "effect.innate_sorcery"
        ]
        value["read_refs"] = [
            ref
            for ref in value["read_refs"]
            if ref != "bound_definition:effect.innate_sorcery"
        ]
    elif mutation == "final-modifier-claimed-resolved":
        value["facets"]["final_modifier_closure"] = "RESOLVED"
    elif mutation == "unknown-facet":
        value["facets"]["shape_change"] = "NOT_EVALUATED"
    else:
        value["facets"]["source_spell"] = "RESOLVED"
        value["facets"]["source_mode"] = "NOT_EVALUATED"
        value["facets"]["activity_closure"] = "RESOLVED"
        value["source_disposition"] = "SELECTED_PREPARED_LEVEL1"
    with pytest.raises(contracts.ActivityContractError):
        contracts.SourceBasisResult(value)


def test_source_basis_validator_proves_four_plus_two_acquisition_for_score_16_and_17() -> (
    None
):
    for score in (16, 17):
        result = contracts.SourceBasisResult(
            _source_basis_result(score=score, adjustment=score - 16)
        )
        acquisition = result.value["acquisition"]
        assert len(acquisition["cantrip_spell_ids"]) == 4
        assert len(acquisition["level1_spell_ids"]) == 2
        assert set(acquisition["known_spell_ids"]) == set(
            acquisition["cantrip_spell_ids"]
        ) | set(acquisition["level1_spell_ids"])
        assert acquisition["prepared_spell_ids"] == tuple(
            sorted(acquisition["level1_spell_ids"])
        )
        assert acquisition["cantrip_option_ids"] == tuple(
            f"option.{spell_id}" for spell_id in acquisition["cantrip_spell_ids"]
        )
        assert acquisition["prepared_option_ids"] == tuple(
            f"option.{spell_id}" for spell_id in acquisition["level1_spell_ids"]
        )
        assert result.value["ability_basis"]["modifier"] == 3
        assert result.value["ability_basis"]["base_spell_save_dc"] == 13
        assert result.value["ability_basis"]["base_spell_attack_bonus"] == 5
        assert result.value["source_disposition"] == "SELECTED_PREPARED_LEVEL1"
    cantrip_result = contracts.SourceBasisResult(
        _source_basis_result(source_spell_id="spell.fire_bolt")
    )
    assert cantrip_result.value["source_disposition"] == "SELECTED_KNOWN_CANTRIP"
    cast_profile_result = _source_basis_result(score=17, adjustment=1)
    cast_profile_result["profile_id"] = "execution.spell_cast.srd521"
    assert contracts.SourceBasisResult(cast_profile_result).value["profile_id"] == (
        "execution.spell_cast.srd521"
    )
    unselected = contracts.SourceBasisResult(
        _source_basis_result(source_spell_id="spell.shield")
    )
    assert unselected.value["source_disposition"] == "UNAVAILABLE"
    assert unselected.value["facets"]["source_spell"] == "UNAVAILABLE"
    assert unselected.value["facets"]["activity_closure"] == "RESOLVED"
    prohibited = contracts.SourceBasisResult(
        _source_basis_result(source_spell_id="spell.fireball", source_spell_level=3)
    )
    assert prohibited.value["source_disposition"] == "PROHIBITED"
    not_evaluated = contracts.SourceBasisResult(
        _source_basis_result(acquisition_evidence=False)
    )
    assert not_evaluated.value["source_disposition"] == "NOT_EVALUATED"
    assert not_evaluated.value["acquisition"] is None
    assert not_evaluated.value["activity_closure_ids"] == ()
    archetype_basis = _source_basis_result(score=17, adjustment=1)
    archetype_ref = {
        "definition_id": "archetype.sorcerer",
        "kind": "definition.actor_archetype",
    }
    archetype_basis["source_definition_refs"].append(archetype_ref)
    archetype_basis["source_definition_refs"].sort(
        key=lambda reference: reference["definition_id"]
    )
    archetype_basis["read_refs"] = sorted(
        [
            *(
                f"bound_definition:{reference['definition_id']}"
                for reference in archetype_basis["source_definition_refs"]
            ),
            "selector:attack.roll",
            "selector:spell.dc",
        ]
    )
    archetype_basis["ability_basis"]["base_source"] = "ARCHETYPE"
    archetype_basis["ability_basis"]["base_source_ref"] = {
        "kind": "ARCHETYPE",
        "source_definition_ref": archetype_ref,
    }
    assert (
        contracts.SourceBasisResult(archetype_basis).value["ability_basis"]["score"]
        == 17
    )
    build_basis = _source_basis_result(score=17, adjustment=1)
    build_basis["ability_basis"]["base_source"] = "BUILD"
    build_basis["ability_basis"]["base_source_ref"] = {
        "kind": "BUILD",
        "source_actor_ref": build_basis["source_actor_ref"],
        "source_field": "build",
    }
    assert (
        contracts.SourceBasisResult(build_basis).value["ability_basis"]["score"] == 17
    )


def test_canonical_source_basis_result_validation_requires_an_issued_compiler() -> None:
    with pytest.raises(TypeError):
        contracts.validate_source_basis_result(_source_basis_result())


def test_source_descriptors_are_not_calculation_argument_bags_or_fact_channels() -> (
    None
):
    profile_schema = _schema(PROFILE_SCHEMA)
    definitions = profile_schema["$defs"]
    for name, value in (
        ("capabilitySourceBinding", _capability_binding()),
        ("castSourceBinding", _cast_binding()),
    ):
        schema = definitions.get(name)
        assert isinstance(schema, dict), f"{name} schema is missing"
        root = {
            "$schema": profile_schema["$schema"],
            "$defs": definitions,
            "allOf": [schema],
        }
        invalid = {
            **value,
            "arguments": {"caller_selected_ability": "ability.dexterity"},
        }
        assert not Draft202012Validator(root).is_valid(invalid)
        invalid = {**value, "context_fact_ids": ["fiction.target_reachable"]}
        assert not Draft202012Validator(root).is_valid(invalid)


def test_capability_projection_cannot_be_bound_by_an_empty_calculation_policy() -> None:
    profile_schema = _schema(PROFILE_SCHEMA)
    policy = {
        "consumer_id": "activity.conformance.compiler.step.0",
        "profile_id": "calculation.capability_projection_srd521",
        "profile_generation": 1,
        "reads": ["selector:ability.charisma"],
        "selector_operation_pairs": [],
        "context_fact_bindings": [],
        "native_role_bindings": [
            {"read_ref": "selector:ability.charisma", "role_names": ["actor"]}
        ],
    }
    root = {
        "$schema": profile_schema["$schema"],
        "$defs": profile_schema["$defs"],
        "allOf": [profile_schema["$defs"]["calculationPolicyBinding"]],
    }
    assert not Draft202012Validator(root).is_valid(policy)


def test_compiler_inventory_binds_the_source_profile_and_declaration_schemas() -> None:
    from DEV.TOOLS import validate_ruleset_package_closure as closure
    from GAME.TOOLS import ruleset_package

    package_root = ROOT / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
    manifest = ruleset_package.load_json_bytes(
        (package_root / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [package_root],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    projection = closure.derive_activity_compiler_contracts(
        ROOT,
        engine_version=manifest["engine_requirement"]["engine_version"],
        ruleset_set_sha256=lock["ruleset_set_sha256"],
    )
    schema_contract = projection["families"]["schema_contract"]
    assert schema_contract.get("spell_native_profile_values_schema") == _schema(
        PROFILE_SCHEMA
    )
    assert schema_contract.get("spell_definition_data_schema") == _schema(
        ROOT / "DEV/SCHEMAS/spell-definition-data.schema.json"
    )
    assert schema_contract.get("activity_compiler_declaration_schema") == _schema(
        COMPILER_SCHEMA
    )


def _prepare_private_sorcerer_package(
    source_root: Path, *, mutation: str | None = None
) -> dict[str, str]:
    package_root = source_root / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
    seed_path = package_root / "character-mvp-seed.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    definitions = {
        record["id"]: record
        for record in (*seed["definitions"], *seed["support_definitions"])
    }
    class_record = copy.deepcopy(definitions["class.sorcerer"])
    advancement = copy.deepcopy(definitions["advancement.sorcerer.mvp_1"])
    spellcasting = copy.deepcopy(definitions["feature.sorcerer.spellcasting"])
    innate_feature = copy.deepcopy(definitions["feature.sorcerer.innate_sorcery"])
    innate_effect = copy.deepcopy(definitions["effect.innate_sorcery"])
    if mutation == "actor_archetype_ability":
        seed["support_definitions"].append(
            {
                "id": "actor_archetype.sorcerer",
                "kind": "definition.actor_archetype",
                "data": {"abilities": {"ability.charisma": 16}},
                "references": [],
            }
        )
    spell_records = {
        spell_id: copy.deepcopy(definitions[spell_id]) for spell_id in KNOWN_IDS
    }
    activities = {record["id"]: record for record in seed["activity_definitions"]}
    activity_records = {
        activity_id: copy.deepcopy(activities[activity_id])
        for activity_id in ACTIVITY_IDS
    }
    if mutation == "missing_activity_definition_record":
        missing_activity_id = "activity.spell.fire_bolt"
        seed["activity_definitions"] = [
            activity
            for activity in seed["activity_definitions"]
            if activity["id"] != missing_activity_id
        ]
        activity_records.pop(missing_activity_id)
    elif mutation == "missing_second_activity_definition":
        second_activity_id = "activity.spell.fire_bolt.alternate"
        fire_bolt = spell_records["spell.fire_bolt"]
        fire_bolt["data"]["activity_ids"].append(second_activity_id)
        fire_bolt["references"].append(second_activity_id)

    advancement["choice_slots"] = [
        {
            "choice_id": CANTRIP_SLOT_ID,
            "minimum": 4,
            "maximum": 4,
            "decision_policy": "choice.player_or_delegated",
            "options": [
                {
                    "option_id": f"option.{spell_id}",
                    "grant_definition_ids": [spell_id],
                    "spell_bindings": {"known_spell_ids": [spell_id]},
                }
                for spell_id in CANTRIP_IDS
            ],
        },
        {
            "choice_id": PREPARED_SLOT_ID,
            "minimum": 2,
            "maximum": 2,
            "decision_policy": "choice.player_or_delegated",
            "options": [
                {
                    "option_id": f"option.{spell_id}",
                    "grant_definition_ids": [spell_id],
                    "spell_bindings": {
                        "known_spell_ids": [spell_id],
                        "prepared_spell_ids": [spell_id],
                    },
                }
                for spell_id in LEVEL1_IDS
            ],
        },
    ]
    if mutation in {"unselected_legal_spell", "source_prohibited_spell"}:
        source_spell_id = (
            "spell.fixture_unselected"
            if mutation == "unselected_legal_spell"
            else "spell.fixture_level3"
        )
        source_activity_id = f"activity.{source_spell_id.removeprefix('spell.')}"
        source_level = 1 if mutation == "unselected_legal_spell" else 3
        seed["definitions"].append(
            {
                "id": source_spell_id,
                "kind": "definition.spell",
                "data": {
                    "level": source_level,
                    "school_id": "school.evocation",
                    "activity_ids": [source_activity_id],
                },
                "references": [source_activity_id],
            }
        )
        seed["activity_definitions"].append(
            {
                "id": source_activity_id,
                "kind": "definition.activity",
                "data": {
                    "family_id": "activity.cast",
                    "steps": [
                        {
                            "op": "op.roll",
                            "args": {
                                "request": {
                                    "roll_id": "roll.fixture",
                                    "expression": "1d20",
                                    "purpose_id": "roll.check",
                                    "roller_role": "actor",
                                }
                            },
                        }
                    ],
                },
            }
        )
        roll_path = (
            source_root
            / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
        )
        roll = json.loads(roll_path.read_text(encoding="utf-8"))
        exact_consumers = roll["contract"]["exact_seed_consumer_ids"]
        exact_consumers.append(source_activity_id)
        roll["contract"]["exact_seed_consumer_ids"] = sorted(set(exact_consumers))
        roll_path.write_text(json.dumps(roll), encoding="utf-8")
        if mutation == "unselected_legal_spell":
            advancement["references"].append(source_spell_id)
            advancement["choice_slots"][1]["options"].append(
                {
                    "option_id": f"option.{source_spell_id}",
                    "grant_definition_ids": [source_spell_id],
                    "spell_bindings": {
                        "known_spell_ids": [source_spell_id],
                        "prepared_spell_ids": [source_spell_id],
                    },
                }
            )
    if mutation == "bundle_choice_payload":
        advancement["choice_slots"][0]["options"][0]["grant_definition_ids"].append(
            CANTRIP_IDS[1]
        )
    elif mutation == "known_binding_mismatch":
        advancement["choice_slots"][0]["options"][0]["spell_bindings"][
            "known_spell_ids"
        ] = [CANTRIP_IDS[1]]
    elif mutation == "prepared_binding_mismatch":
        advancement["choice_slots"][1]["options"][0]["spell_bindings"][
            "prepared_spell_ids"
        ] = [LEVEL1_IDS[1]]
    elif mutation == "starting_asset_per_choice":
        advancement["choice_slots"][0]["options"][0]["starting_assets"] = [
            {"definition_id": "asset.arcane_focus", "quantity": 1}
        ]
    elif mutation == "cross_slot_spell_level":
        option = advancement["choice_slots"][0]["options"][0]
        option["option_id"] = f"option.{LEVEL1_IDS[0]}"
        option["grant_definition_ids"] = [LEVEL1_IDS[0]]
        option["spell_bindings"]["known_spell_ids"] = [LEVEL1_IDS[0]]
    if mutation == "transitive_definition":
        advancement["references"].remove("feature.sorcerer.spellcasting")
    elif mutation == "definition_cycle":
        advancement["references"].append("class.sorcerer")
    elif mutation == "missing_data_activity_reference":
        spell_records["spell.fire_bolt"]["references"].remove(
            "activity.spell.fire_bolt"
        )
    elif mutation == "missing_spell_primitive_dependency":
        spell_records["spell.fire_bolt"]["primitive_dependencies"].remove(
            "op.resolve_attack"
        )
    elif mutation == "primitive_list_omitted":
        spell_records["spell.fire_bolt"].pop("primitive_dependencies", None)
    elif mutation == "missing_primitive_member_with_unregistered_op":
        spell_records["spell.fire_bolt"].pop("primitive_dependencies", None)
        activity_records["activity.spell.fire_bolt"]["data"]["steps"] = [
            {"op": "op.review_not_registered", "args": {}}
        ]
    elif mutation == "missing_primitive_member_with_dormant_op":
        spell_records["spell.fire_bolt"].pop("primitive_dependencies", None)
        activity_records["activity.spell.fire_bolt"]["data"]["steps"] = [
            {"op": "op.branch", "args": {}}
        ]
    elif mutation == "missing_primitive_member_with_unadmitted_op":
        spell_records["spell.fire_bolt"].pop("primitive_dependencies", None)
        activity_records["activity.spell.fire_bolt"]["data"]["steps"] = [
            {"op": "op.consume_resource", "args": {}}
        ]
    elif mutation == "missing_spellcasting_resource_reference":
        spellcasting["references"].remove("resource.spell_slot.level_1")
    elif mutation == "missing_innate_effect_reference":
        innate_feature["references"].remove("effect.innate_sorcery")
    elif mutation == "missing_focus_reference":
        spellcasting["references"].remove("asset.arcane_focus")
    replacements = [
        ("definitions", class_record),
        ("definitions", advancement),
        ("definitions", spellcasting),
        ("definitions", innate_feature),
        ("support_definitions", innate_effect),
        *(("definitions", spell) for spell in spell_records.values()),
        *(("activity_definitions", activity) for activity in activity_records.values()),
    ]
    for collection_name, replacement in replacements:
        collection = seed[collection_name]
        for index, record in enumerate(collection):
            if record["id"] == replacement["id"]:
                collection[index] = replacement
                break
        else:
            raise AssertionError(
                f"private fixture lost source definition {replacement['id']}"
            )
    seed_path.write_text(json.dumps(seed, ensure_ascii=False), encoding="utf-8")
    final_seed = json.loads(seed_path.read_text(encoding="utf-8"))
    final_records = _seed_source_records(final_seed)
    final_closure = _reference_closure(final_records, ("class.sorcerer",))
    if mutation == "actor_archetype_ability":
        final_closure = tuple(sorted((*final_closure, "actor_archetype.sorcerer")))
    return {
        identity: str(final_records[identity]["kind"])
        for identity in final_closure
        if identity in final_records
        if final_records[identity]["kind"] != "definition.activity"
    }


def _cold_source_compiler_fixture(
    conformance_runtime_root: Path,
    tmp_path: Path,
    *,
    mutation: str | None = None,
    root_roles: dict[str, str] | None = None,
) -> tuple[Path, dict[str, object], dict[str, str]]:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as carrier_tests

    source_root = tmp_path / "source"
    catalog_tests._stage_clean_source_tree(source_root)
    carrier_tests._prepare_sp03_source_tree(source_root)
    if root_roles is not None:
        primitive_root = (
            source_root / "DEV/CATALOG/activity-primitive-contracts/primitives"
        )
        for primitive_path in primitive_root.glob("*.json"):
            primitive = json.loads(primitive_path.read_text(encoding="utf-8"))
            declaration = (
                primitive.get("contract", {})
                .get("compiler_declarations", {})
                .get("activity.conformance.compiler")
            )
            if isinstance(declaration, dict):
                declaration["roles"] = copy.deepcopy(root_roles)
                primitive_path.write_text(json.dumps(primitive), encoding="utf-8")
    dependency_kinds = _prepare_private_sorcerer_package(source_root, mutation=mutation)
    private_seed = json.loads(
        (
            source_root
            / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
        ).read_text(encoding="utf-8")
    )
    private_records = _seed_source_records(private_seed)
    activity_id = "activity.conformance.compiler"
    nested_consumer = f"{activity_id}.step.1.steps.step.0"
    capability_consumer = (
        f"{activity_id}.step.0"
        if mutation in {"distinct_consumers", "selected_cantrip"}
        else nested_consumer
    )
    primitive_path = (
        source_root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
    )
    primitive = json.loads(primitive_path.read_text(encoding="utf-8"))
    declaration = primitive["contract"]["compiler_declarations"][activity_id]
    capability_binding = _capability_binding()
    cast_binding = _cast_binding()
    if mutation == "selected_cantrip":
        capability_binding["source_spell_id"] = "spell.fire_bolt"
    elif mutation == "cast_selected_cantrip":
        cast_binding["source_spell_id"] = "spell.fire_bolt"
    elif mutation == "unselected_legal_spell":
        cast_binding["source_spell_id"] = "spell.fixture_unselected"
    elif mutation == "source_prohibited_spell":
        cast_binding["source_spell_id"] = "spell.fixture_level3"
    capability_binding["dependency_refs"] = [
        "bound_definition:class.sorcerer",
        f"bound_definition:{capability_binding['source_spell_id']}",
    ]
    cast_binding["dependency_refs"] = [
        "bound_definition:class.sorcerer",
        f"bound_definition:{cast_binding['source_spell_id']}",
    ]

    def source_refs(
        source_spell_id: str, *, include_actor_archetype: bool = False
    ) -> list[dict[str, str]]:
        roots = ["class.sorcerer", source_spell_id]
        if include_actor_archetype:
            roots.append("actor_archetype.sorcerer")
        return [
            {
                "definition_id": identity,
                "kind": str(
                    private_records[identity]["kind"]
                    if identity in private_records
                    else "definition.activity"
                    if identity.startswith("activity.")
                    else "definition.spell"
                ),
            }
            for identity in _reference_closure(private_records, tuple(roots))
        ]

    capability_binding["source_definition_refs"] = source_refs(
        str(capability_binding["source_spell_id"])
    )
    if mutation == "extra_source_activity_reference":
        capability_binding["source_definition_refs"].append(
            {
                "definition_id": "activity.attack.ranged_weapon",
                "kind": "definition.activity",
            }
        )
        capability_binding["source_definition_refs"].sort(
            key=lambda reference: reference["definition_id"]
        )
    cast_binding["source_definition_refs"] = source_refs(
        str(cast_binding["source_spell_id"]),
        include_actor_archetype=mutation == "actor_archetype_ability",
    )
    if mutation == "actor_archetype_ability":
        cast_binding["dependency_refs"].append(
            "bound_definition:actor_archetype.sorcerer"
        )
    capability_binding["consumer_id"] = capability_consumer
    cast_binding["consumer_id"] = nested_consumer
    if mutation in {
        "unauthorized_accessor",
        "unauthorized_selector",
        "unauthorized_parent_edge",
        "subject_mismatch",
        "mechanical_cycle",
        "transitive_input_class",
    }:
        source_ref = (
            "accessor:health.maximum"
            if mutation == "unauthorized_accessor"
            else "selector:condition.applicability"
            if mutation == "unauthorized_selector"
            else "selector:spell.dc"
        )
        capability_binding["dependency_refs"].append(source_ref)
        capability_binding["native_role_bindings"].append(
            {"read_ref": source_ref, "role_names": ["actor"]}
        )
    elif mutation == "dormant_accessor":
        capability_binding["dependency_refs"].append("accessor:condition.value")
        capability_binding["native_role_bindings"].append(
            {"read_ref": "accessor:condition.value", "role_names": ["actor"]}
        )
    elif mutation == "fabricated_shield_mode":
        cast_binding["mode_id"] = "mode.spell.shield.standard"
    elif mutation == "unknown_dependency":
        capability_binding["dependency_refs"].append(
            "bound_definition:definition.unavailable"
        )
    elif mutation == "wrong_role":
        capability_binding["native_role_bindings"][0]["role_names"] = ["source_actor"]
    elif mutation == "wrong_definition_ref":
        capability_binding["source_definition_refs"][0]["kind"] = "definition.feature"
    elif mutation == "unknown_facet":
        capability_binding["evaluated_facets"] = [
            "source_class",
            "acquisition",
            "source_ability",
            "proficiency",
            "movement",
        ]
    elif mutation == "fact_dependency":
        capability_binding["context_fact_ids"] = ["fiction.target_reachable"]
    elif mutation == "unknown_selector":
        capability_binding["dependency_refs"].append("selector:source.missing")
        capability_binding["native_role_bindings"].append(
            {
                "read_ref": "selector:source.missing",
                "role_names": ["actor"],
            }
        )
    elif mutation == "unknown_accessor":
        capability_binding["dependency_refs"].append("accessor:source.missing")
        capability_binding["native_role_bindings"].append(
            {"read_ref": "accessor:source.missing", "role_names": ["actor"]}
        )
    elif mutation == "foreign_consumer":
        capability_binding["consumer_id"] = "activity.foreign.step.0"
    elif mutation == "wrong_profile_generation":
        capability_binding["profile_generation"] = 2
    elif mutation == "binding_missing_asset_reference":
        capability_binding["source_definition_refs"] = [
            reference
            for reference in capability_binding["source_definition_refs"]
            if reference["definition_id"] != "asset.arcane_focus"
        ]
    declaration["capability_sources"] = [capability_binding]
    declaration["cast_sources"] = [cast_binding]
    primitive_path.write_text(json.dumps(primitive), encoding="utf-8")

    if mutation in {
        "unauthorized_parent_edge",
        "subject_mismatch",
        "mechanical_cycle",
        "transitive_input_class",
    }:
        mechanical_path = source_root / "DEV/CATALOG/mechanical-surfaces.json"
        mechanical_source = json.loads(mechanical_path.read_text(encoding="utf-8"))
        selector_id = "spell.dc"
        selector = mechanical_source["selectors"][selector_id]
        selector["binding_kinds"] = ["subject"]
        ledger_path = (
            source_root
            / "DEV/CATALOG/catalog-admission-ledger/families/rule_selectors.json"
        )
        ledger_source = json.loads(ledger_path.read_text(encoding="utf-8"))
        selector_ledger = next(
            row for row in ledger_source["entries"] if row["id"] == selector_id
        )
        selector_ledger["consumer_or_dependency"] += "; activity.conformance.compiler"
        if mutation == "unauthorized_parent_edge":
            selector["static_dependencies"] = ["accessor:health.current"]
        elif mutation == "subject_mismatch":
            selector["subject_kinds"] = ["world.asset"]
        elif mutation == "mechanical_cycle":
            selector["allowed_dependency_kinds"] = ["selector"]
            selector["static_dependencies"] = ["selector:spell.dc"]
        else:
            selector["allowed_input_classes"] = ["INVOCATION_ADJUDICATED"]
            selector["permitted_context_fact_ids"] = ["fiction.target_reachable"]
        mechanical_path.write_text(json.dumps(mechanical_source), encoding="utf-8")
        ledger_path.write_text(json.dumps(ledger_source), encoding="utf-8")

    runtime_root = carrier_tests._installed_source_compiler_fixture(
        source_root, conformance_runtime_root, tmp_path / "runtime"
    )
    package_relative = Path("GAME/RULES/packages/hdm.rules.dnd2024-srd52-core")
    source_package = source_root / package_relative
    installed_package = runtime_root / package_relative.relative_to("GAME")
    shutil.copy2(
        source_package / "character-mvp-seed.json",
        installed_package / "character-mvp-seed.json",
    )
    from GAME.TOOLS import ruleset_package

    manifest = ruleset_package.load_json_bytes(
        (source_package / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [source_package],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    marker_path = runtime_root / "RUNTIME_PACKAGE.yaml"
    marker = catalog_tests.yaml.safe_load(marker_path.read_text(encoding="utf-8"))
    marker["ruleset_set_sha256"] = lock["ruleset_set_sha256"]
    marker["resolved_ruleset_lock"] = lock
    marker["ruleset_conformance_attestation"] = (
        ruleset_package.compile_conformance_attestation(
            marker["ruleset_engine_contract_inventory"],
            marker["ruleset_conformance_attestation"]["validator_results"],
            lock=lock,
            engine_version=manifest["engine_requirement"]["engine_version"],
        )
    )
    marker_path.write_text(
        catalog_tests.yaml.safe_dump(marker, sort_keys=False), encoding="utf-8"
    )
    recipe = carrier_tests._source_compiler_recipe()
    if mutation != "missing_profile":
        recipe["data"]["profile_bindings"].append(
            {
                "consumer_id": capability_consumer,
                "profile_id": "calculation.capability_projection_srd521",
                "profile_generation": 1,
            }
        )
    return runtime_root, recipe, dependency_kinds


def _selected_source_route_compiler_fixture(
    conformance_runtime_root: Path,
    tmp_path: Path,
    *,
    route_case: str = "actual_magic_missile",
    symbol_case: str | None = None,
    source_mode_case: str = "declared",
) -> tuple[Path, dict[str, object], dict[str, str]]:
    """Build a private installed-source route case through the real compiler."""
    from DEV.TESTS import test_local_spell_catalog as catalog_tests
    from DEV.TESTS import test_sp03_policy_carriers as carrier_tests

    if route_case not in {
        "actual_magic_missile",
        "cross_spell_union",
        "missing_selected_edge",
        "multi_activity_nonfirst",
        "source_prohibited_spell",
    }:
        raise AssertionError(f"unknown selected-route fixture case: {route_case}")
    if source_mode_case not in {
        "declared",
        "absent",
        "duplicate_key",
        "foreign_activity",
        "ambiguous_activity",
        "missing_definition",
        "missing_edge",
        "reordered",
    }:
        raise AssertionError(f"unknown private source-mode case: {source_mode_case}")
    if symbol_case not in {None, "missing", "wrong_type", "wrong_occurrence", "cycle"}:
        raise AssertionError(f"unknown selected-route symbol case: {symbol_case}")
    private_source = tmp_path / "selected-source-route-source"
    catalog_tests._stage_clean_source_tree(private_source)
    carrier_tests._prepare_sp03_source_tree(private_source)
    mutation = (
        "unselected_legal_spell"
        if route_case == "multi_activity_nonfirst"
        else "source_prohibited_spell"
        if route_case == "source_prohibited_spell"
        else None
    )
    dependency_kinds = _prepare_private_sorcerer_package(
        private_source, mutation=mutation
    )
    package_relative = Path("GAME/RULES/packages/hdm.rules.dnd2024-srd52-core")
    source_package = private_source / package_relative
    seed_path = source_package / "character-mvp-seed.json"
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    records = _seed_source_records(seed)

    if route_case == "multi_activity_nonfirst":
        source_spell_id = "spell.fixture_unselected"
        source_spell = records[source_spell_id]
        first_activity_id = "activity.fixture_unselected"
        route_activity_id = f"{first_activity_id}.alternate"
        alternate = copy.deepcopy(records[first_activity_id])
        alternate["id"] = route_activity_id
        alternate["data"]["steps"][0]["args"]["request"]["roll_id"] = (
            "roll.fixture_unselected.alternate"
        )
        seed["activity_definitions"].append(alternate)
        source_spell["data"]["activity_ids"].append(route_activity_id)
        source_spell["references"].append(route_activity_id)
        records[route_activity_id] = alternate
    elif route_case == "source_prohibited_spell":
        source_spell_id = "spell.fixture_level3"
        route_activity_id = "activity.fixture_level3"
        source_spell = records[source_spell_id]
    else:
        source_spell_id = (
            "spell.fire_bolt"
            if route_case == "cross_spell_union"
            else "spell.magic_missile"
        )
        route_activity_id = "activity.spell.magic_missile"
        source_spell = records[source_spell_id]

    if route_case == "missing_selected_edge":
        alternate_id = "activity.spell.magic_missile.route_conformance"
        alternate = {
            "id": alternate_id,
            "kind": "definition.activity",
            "data": {
                "family_id": "activity.cast",
                "steps": [
                    {
                        "op": "op.roll",
                        "args": {
                            "request": {
                                "roll_id": "roll.magic_missile.route_conformance",
                                "expression": "1d20",
                                "purpose_id": "roll.check",
                                "roller_role": "actor",
                            }
                        },
                    }
                ],
            },
        }
        seed["activity_definitions"].append(alternate)
        magic_missile = records["spell.magic_missile"]
        magic_missile["data"]["activity_ids"] = [alternate_id]
        magic_missile["references"] = [
            reference
            for reference in magic_missile["references"]
            if reference != route_activity_id
        ] + [alternate_id]
        magic_missile["primitive_dependencies"] = ["op.roll"]
        records[alternate_id] = alternate

    route_activity = records[route_activity_id]
    if route_case == "multi_activity_nonfirst":
        source_modes = [
            {
                "mode_id": "mode.fixture_unselected.primary",
                "activity_id": "activity.fixture_unselected",
            },
            {
                "mode_id": "mode.fixture_unselected.alternate",
                "activity_id": route_activity_id,
            },
        ]
    elif route_case == "source_prohibited_spell":
        source_modes = [
            {
                "mode_id": "mode.fixture_level3.ordinary",
                "activity_id": route_activity_id,
            }
        ]
    elif (
        source_spell_id == "spell.magic_missile"
        and route_case == "actual_magic_missile"
    ):
        # Reconciled to SRD CC v5.2.1 Magic Missile, Markdown13259-13273.
        # This explicit private key identifies the staged route only; it does
        # not establish damage, target success, simultaneous execution or upcast.
        source_modes = [
            {
                "mode_id": "mode.magic_missile.ordinary",
                "activity_id": "activity.spell.magic_missile",
            }
        ]
    else:
        source_modes = []

    if source_mode_case == "absent":
        source_spell["data"].pop("source_modes", None)
    elif source_modes:
        source_spell["data"]["source_modes"] = source_modes
    if source_mode_case == "duplicate_key":
        source_spell["data"]["source_modes"].append(
            {
                "mode_id": source_spell["data"]["source_modes"][0]["mode_id"],
                "activity_id": "activity.spell.fire_bolt",
            }
        )
    elif source_mode_case == "foreign_activity":
        source_spell["data"]["source_modes"][0]["activity_id"] = (
            "activity.spell.fire_bolt"
        )
    elif source_mode_case == "ambiguous_activity":
        source_spell["data"]["source_modes"].append(
            {
                "mode_id": "mode.magic_missile.ambiguous",
                "activity_id": "activity.spell.magic_missile",
            }
        )
    elif source_mode_case == "reordered":
        source_spell["data"]["source_modes"].reverse()
    elif source_mode_case == "missing_definition":
        missing_activity_id = "activity.spell.magic_missile.missing"
        source_spell["data"]["activity_ids"].append(missing_activity_id)
        source_spell["references"].append(missing_activity_id)
        source_spell["data"]["source_modes"][0]["activity_id"] = missing_activity_id
    elif source_mode_case == "missing_edge":
        source_spell["references"].remove("activity.spell.magic_missile")
    consumer_id = f"{route_activity_id}.step.0"
    if route_activity_id == "activity.spell.magic_missile":
        # Preserve the actual fact dependency while deliberately not claiming
        # that this conformance root has a reachable target.
        reachability_fact = {
            "fact_id": "fiction.target_reachable",
            "value": False,
            "provenance_class": "INVOCATION_ADJUDICATED",
            "provenance_ref": "sp03-route-fixture:target-reachability-not-established",
            "consumer_id": route_activity_id,
            "binding_fingerprint": "a" * 64,
            "rules_context_fingerprint": "b" * 64,
            "policy_basis_refs": [],
        }

        def preserve_route_inputs(steps: object) -> None:
            if not isinstance(steps, list):
                return
            for step in steps:
                if not isinstance(step, dict):
                    continue
                arguments = step.get("args")
                if not isinstance(arguments, dict):
                    continue
                if arguments.get("candidate_roles") == "invocation.candidate_roles":
                    arguments["candidate_roles"] = ["target"]
                if arguments.get("applicability_facts") == (
                    "invocation.fiction.target_reachable"
                ):
                    arguments["applicability_facts"] = [reachability_fact]
                preserve_route_inputs(arguments.get("steps"))

        preserve_route_inputs(route_activity["data"].get("steps"))

    route_activity["data"].setdefault("profile_bindings", []).append(
        {
            "consumer_id": consumer_id,
            "profile_id": "execution.spell_cast.srd521",
            "profile_generation": 1,
        }
    )
    binding = _cast_binding()
    binding["consumer_id"] = consumer_id
    binding["source_spell_id"] = source_spell_id
    binding["dependency_refs"] = [
        "bound_definition:class.sorcerer",
        f"bound_definition:{source_spell_id}",
    ]
    binding["source_definition_refs"] = [
        {
            "definition_id": identity,
            "kind": str(
                records[identity]["kind"]
                if identity in records
                else "definition.activity"
                if identity.startswith("activity.")
                else "definition.spell"
            ),
        }
        for identity in _reference_closure(records, ("class.sorcerer", source_spell_id))
    ]
    for reference in binding["source_definition_refs"]:
        if reference["kind"] != "definition.activity":
            dependency_kinds[reference["definition_id"]] = reference["kind"]

    first_step = route_activity["data"]["steps"][0]
    primitive_id = first_step["op"]
    primitive_path = (
        private_source
        / "DEV/CATALOG/activity-primitive-contracts/primitives"
        / f"{primitive_id}.json"
    )
    primitive = json.loads(primitive_path.read_text(encoding="utf-8"))
    declarations = primitive["contract"].setdefault("compiler_declarations", {})
    roles = {"actor": "world.actor"}
    if (
        route_activity_id == "activity.spell.magic_missile"
        or primitive_id == "op.select_targets"
    ):
        roles["target"] = "world.actor"
    declaration = declarations.setdefault(
        route_activity_id,
        {"roles": roles, "symbols": {}, "profiles": []},
    )
    declaration.setdefault("roles", roles)
    declaration.setdefault("symbols", {})
    declaration.setdefault("profiles", [])
    declaration["cast_sources"] = [binding]
    if route_activity_id == "activity.spell.magic_missile":
        damage_path = (
            private_source
            / "DEV/CATALOG/activity-primitive-contracts/primitives/op.apply_damage.json"
        )
        damage_primitive = json.loads(damage_path.read_text(encoding="utf-8"))
        damage_declaration = (
            damage_primitive["contract"]
            .setdefault("compiler_declarations", {})
            .setdefault(
                route_activity_id,
                {"roles": {}, "symbols": {}, "profiles": []},
            )
        )
        damage_declaration.setdefault("roles", {})
        damage_declaration.setdefault("symbols", {})
        damage_declaration.setdefault("profiles", [])
        # Fixed compiler conformance input only: never executed or asserted as
        # Magic Missile damage or as a fixed RNG result.
        damage_declaration["symbols"]["compiled.one_dart_force_damage"] = {
            "value_kind": "damage_components",
            "cardinality": "single",
            "value": [{"amount": 1, "damage_type_ref": "damage.force"}],
            "dependencies": [],
            "reads": [],
            "permitted_occurrence_ids": [
                "activity.spell.magic_missile.step.2.steps.step.0"
            ],
        }
        if symbol_case == "missing":
            damage_declaration["symbols"].pop("compiled.one_dart_force_damage")
        elif symbol_case == "wrong_type":
            damage_declaration["symbols"]["compiled.one_dart_force_damage"][
                "value_kind"
            ] = "integer"
            damage_declaration["symbols"]["compiled.one_dart_force_damage"]["value"] = 1
        elif symbol_case == "wrong_occurrence":
            damage_declaration["symbols"]["compiled.one_dart_force_damage"][
                "permitted_occurrence_ids"
            ] = ["activity.spell.magic_missile.step.0"]
        elif symbol_case == "cycle":
            damage_declaration["symbols"]["compiled.one_dart_force_damage"][
                "dependencies"
            ] = ["compiled.one_dart_force_damage"]
        damage_path.write_text(json.dumps(damage_primitive), encoding="utf-8")
    primitive_path.write_text(json.dumps(primitive), encoding="utf-8")

    if route_case in {"missing_selected_edge", "multi_activity_nonfirst"}:
        alternate_id = (
            "activity.spell.magic_missile.route_conformance"
            if route_case == "missing_selected_edge"
            else route_activity_id
        )
        alternate_primitive_path = (
            private_source
            / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
        )
        alternate_primitive = json.loads(
            alternate_primitive_path.read_text(encoding="utf-8")
        )
        alternate_declaration = (
            alternate_primitive["contract"]
            .setdefault("compiler_declarations", {})
            .setdefault(
                alternate_id,
                {"roles": {"actor": "world.actor"}, "symbols": {}, "profiles": []},
            )
        )
        alternate_declaration.setdefault("roles", {"actor": "world.actor"})
        alternate_declaration.setdefault("symbols", {})
        alternate_declaration.setdefault("profiles", [])
        alternate_primitive_path.write_text(
            json.dumps(alternate_primitive), encoding="utf-8"
        )

    seed_path.write_text(json.dumps(seed, ensure_ascii=False), encoding="utf-8")
    runtime_root = carrier_tests._installed_source_compiler_fixture(
        private_source,
        conformance_runtime_root,
        tmp_path / "selected-source-route-runtime",
    )
    installed_package = runtime_root / package_relative.relative_to("GAME")
    shutil.copy2(seed_path, installed_package / "character-mvp-seed.json")

    from GAME.TOOLS import ruleset_package

    manifest = ruleset_package.load_json_bytes(
        (source_package / "ruleset-package-manifest.json").read_bytes()
    )
    lock, _snapshots = ruleset_package.build_resolved_lock(
        [source_package],
        root_package_ids=[manifest["package_id"]],
        engine_version=manifest["engine_requirement"]["engine_version"],
        catalog_generation=manifest["catalog_generation"],
    )
    marker_path = runtime_root / "RUNTIME_PACKAGE.yaml"
    marker = catalog_tests.yaml.safe_load(marker_path.read_text(encoding="utf-8"))
    marker["ruleset_set_sha256"] = lock["ruleset_set_sha256"]
    marker["resolved_ruleset_lock"] = lock
    marker["ruleset_conformance_attestation"] = (
        ruleset_package.compile_conformance_attestation(
            marker["ruleset_engine_contract_inventory"],
            marker["ruleset_conformance_attestation"]["validator_results"],
            lock=lock,
            engine_version=manifest["engine_requirement"]["engine_version"],
        )
    )
    marker_path.write_text(
        catalog_tests.yaml.safe_dump(marker, sort_keys=False), encoding="utf-8"
    )
    dependency_kinds[route_activity_id] = "definition.activity"
    return runtime_root, copy.deepcopy(route_activity), dependency_kinds


def test_cold_source_compiler_rejects_unowned_shield_mode_on_magic_missile(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation="fabricated_shield_mode"
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode != 0, result.stdout
    assert "activity-compiler-declaration is not admitted" in result.stderr


def test_cold_source_compiler_rejects_dormant_condition_value_dependency(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation="dormant_accessor"
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode != 0, result.stdout


def test_cold_source_compiler_derives_activity_primitives_without_optional_list(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation="primitive_list_omitted"
    )
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
source = compiled.capability_source_bindings[0]
assert source.source_activity_primitive_ids["activity.spell.fire_bolt"] == tuple(
    json.loads(sys.argv[4])
)
print(json.dumps(source.source_activity_primitive_ids["activity.spell.fire_bolt"]))
"""
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        "[]",
        json.dumps(SOURCE_ACTIVITY_PRIMITIVE_IDS["activity.spell.fire_bolt"]),
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_cold_ordinary_catalog_rejects_missing_feature_activity_dependency(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    recipe = catalog_tests._nested_recipe()
    recipe["references"] = ["feature.review.missing_activity"]
    feature = {
        "id": "feature.review.missing_activity",
        "kind": "definition.feature",
        "data": {"activity_ids": ["activity.review.unavailable"]},
        "references": ["activity.review.unavailable"],
    }
    result = catalog_tests._run_installed_runtime_probe(
        conformance_runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        "{}",
        json.dumps([feature]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr


def test_cold_ordinary_catalog_rejects_missing_spell_activity_dependency(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    recipe = catalog_tests._nested_recipe()
    recipe["references"] = ["spell.review.missing_activity"]
    spell = {
        "id": "spell.review.missing_activity",
        "kind": "definition.spell",
        "data": {
            "level": 1,
            "school_id": "school.evocation",
            "activity_ids": ["activity.review.unavailable"],
        },
        "references": ["activity.review.unavailable"],
    }
    result = catalog_tests._run_installed_runtime_probe(
        conformance_runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        "{}",
        json.dumps([spell]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr


def _admission_only_probe(catalog_tests) -> str:
    compile_line = "\ncompiled = compile_activity(catalog,identity)"
    assert compile_line in catalog_tests._RECIPE_PROBE
    return catalog_tests._RECIPE_PROBE.replace(compile_line, "")


def test_cold_independent_unavailable_activity_does_not_block_catalog_issuance(
    conformance_runtime_root: Path,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    recipe = catalog_tests._nested_recipe()
    recipe["data"]["steps"][0]["op"] = "op.review_not_registered"
    probe = (
        _admission_only_probe(catalog_tests)
        + r"""
assert identity in catalog.unavailable_activity_reasons
assert "unknown or dormant primitive" in catalog.unavailable_activity_reasons[identity]
assert identity not in catalog.compiled_activities
"""
    )
    result = catalog_tests._run_installed_runtime_probe(
        conformance_runtime_root,
        probe,
        json.dumps(recipe),
        "{}",
    )
    assert result.returncode == 0, result.stderr or result.stdout


@pytest.mark.parametrize("alias_kind", ("definition.feature", "definition.spell"))
def test_cold_source_closure_does_not_defer_foreign_feature_or_spell_activity_edges(
    conformance_runtime_root: Path, tmp_path: Path, alias_kind: str
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path
    )
    activity_id = "activity.spell.fire_bolt"
    alias_id = (
        "feature.review.alias"
        if alias_kind == "definition.feature"
        else "spell.review.alias"
    )
    alias_data = (
        {"activity_ids": [activity_id]}
        if alias_kind == "definition.feature"
        else {
            "level": 1,
            "school_id": "school.evocation",
            "activity_ids": [activity_id],
        }
    )
    alias = {
        "id": alias_id,
        "kind": alias_kind,
        "data": alias_data,
        "references": [activity_id],
    }
    recipe["references"] = [alias_id]
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        _admission_only_probe(catalog_tests),
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        json.dumps([alias]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr
    assert alias_id in result.stderr


def test_cold_source_closure_does_not_defer_transitive_foreign_activity_edge(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path
    )
    activity_id = "activity.spell.fire_bolt"
    alias_leaf = {
        "id": "feature.review.alias_leaf",
        "kind": "definition.feature",
        "data": {"activity_ids": [activity_id]},
        "references": [activity_id],
    }
    alias_root = {
        "id": "feature.review.alias_root",
        "kind": "definition.feature",
        "data": {"activity_ids": []},
        "references": [alias_leaf["id"]],
    }
    recipe["references"] = [alias_root["id"]]
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        _admission_only_probe(catalog_tests),
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        json.dumps([alias_root, alias_leaf]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr
    assert alias_leaf["id"] in result.stderr


def test_cold_failed_source_root_cannot_lend_its_deferred_activity_to_foreign_feature(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        mutation="missing_primitive_member_with_unregistered_op",
    )
    activity_id = "activity.spell.fire_bolt"
    feature = {
        "id": "feature.review.alias",
        "kind": "definition.feature",
        "data": {"activity_ids": [activity_id]},
        "references": [activity_id],
    }
    recipe["references"] = [feature["id"]]
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        _admission_only_probe(catalog_tests),
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        json.dumps([feature]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr
    assert feature["id"] in result.stderr


def test_cold_nonclosure_activity_reference_cannot_be_borrowed_from_source_declaration(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        mutation="extra_source_activity_reference",
    )
    activity_id = "activity.attack.ranged_weapon"
    feature = {
        "id": "feature.review.alias",
        "kind": "definition.feature",
        "data": {"activity_ids": [activity_id]},
        "references": [activity_id],
    }
    recipe["references"] = [feature["id"]]
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        _admission_only_probe(catalog_tests),
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        json.dumps([feature]),
    )
    assert result.returncode != 0, result.stdout
    assert "unavailable transitive dependencies" in result.stderr
    assert feature["id"] in result.stderr


@pytest.mark.parametrize(
    ("mutation", "source_spell_id", "source_spell_level", "source_disposition"),
    [
        (
            "selected_cantrip",
            "spell.fire_bolt",
            0,
            "SELECTED_KNOWN_CANTRIP",
        ),
        (
            "selected_prepared",
            "spell.magic_missile",
            1,
            "SELECTED_PREPARED_LEVEL1",
        ),
        (
            "unselected_legal_spell",
            "spell.fixture_unselected",
            1,
            "UNAVAILABLE",
        ),
        (
            "source_prohibited_spell",
            "spell.fixture_level3",
            3,
            "PROHIBITED",
        ),
        (
            None,
            "spell.magic_missile",
            1,
            "NOT_EVALUATED",
        ),
    ],
)
def test_cold_issued_source_result_distinguishes_spell_availability_states(
    conformance_runtime_root: Path,
    tmp_path: Path,
    mutation: str | None,
    source_spell_id: str,
    source_spell_level: int,
    source_disposition: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    selected_fixture = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation=mutation
    )
    runtime_root, recipe, dependency_kinds = selected_fixture
    if mutation in {"unselected_legal_spell", "source_prohibited_spell"}:
        support_activity = (
            "activity.fixture_unselected"
            if mutation == "unselected_legal_spell"
            else "activity.fixture_level3"
        )
        additional_refs = (
            {
                "definition_id": support_activity,
                "kind": "definition.activity",
            },
        )
    else:
        additional_refs = ()
    basis = _source_basis_result(
        source_spell_id=source_spell_id,
        source_spell_level=source_spell_level,
        source_disposition=source_disposition,
        consumer_id="activity.conformance.compiler.step.1.steps.step.0"
        if mutation != "selected_cantrip"
        else "activity.conformance.compiler.step.0",
        acquisition_evidence=mutation is not None,
        ability_evidence=mutation is not None,
        additional_source_definition_refs=additional_refs,
    )
    if mutation in {"unselected_legal_spell", "source_prohibited_spell"}:
        basis["profile_id"] = "execution.spell_cast.srd521"
    if mutation is None:
        basis["profile_id"] = "execution.spell_cast.srd521"
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
from TOOLS import activity_contracts as contracts
result = contracts.validate_source_basis_result(
    json.loads(sys.argv[4]), compiled=compiled
)
assert result.value["source_disposition"] == sys.argv[5]
assert result.value["mode_id"] is None
assert result.value["facets"]["source_mode"] == "NOT_EVALUATED"
if result.value["source_disposition"] == "UNAVAILABLE":
    import copy
    ambiguous_missing_status = copy.deepcopy(json.loads(sys.argv[4]))
    ambiguous_missing_status["source_disposition"] = "NOT_EVALUATED"
    ambiguous_missing_status["facets"]["source_spell"] = "NOT_EVALUATED"
    try:
        contracts.validate_source_basis_result(
            ambiguous_missing_status, compiled=compiled
        )
    except contracts.ActivityContractError:
        pass
    else:
        raise AssertionError("legal but unselected source collapsed into not-evaluated")
    false_prohibition = copy.deepcopy(json.loads(sys.argv[4]))
    false_prohibition["source_disposition"] = "PROHIBITED"
    false_prohibition["facets"]["source_spell"] = "PROHIBITED"
    try:
        contracts.validate_source_basis_result(false_prohibition, compiled=compiled)
    except contracts.ActivityContractError:
        pass
    else:
        raise AssertionError("legal but unselected source was mislabeled prohibited")
print(json.dumps({"disposition": result.value["source_disposition"]}))
"""
    )
    installed_result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        "[]",
        json.dumps(basis),
        source_disposition,
    )
    assert installed_result.returncode == 0, (
        installed_result.stderr or installed_result.stdout
    )


@pytest.mark.parametrize(
    ("mutation", "diagnostic"),
    [
        ("unauthorized_accessor", "accessor is unknown, dormant, or unauthorized"),
        (
            "unauthorized_selector",
            "selector condition.applicability is not admitted for activity.conformance.compiler",
        ),
        ("unauthorized_parent_edge", "accessor is unknown, dormant, or unauthorized"),
        ("subject_mismatch", "subject/binding roles"),
        ("mechanical_cycle", "source dependency cycle"),
        ("transitive_input_class", "source input class exceeds its root permission"),
    ],
)
def test_cold_source_compiler_rejects_unadmitted_source_dependency_graphs(
    conformance_runtime_root: Path,
    tmp_path: Path,
    mutation: str,
    diagnostic: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation=mutation
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode != 0, result.stdout
    assert diagnostic in result.stderr


def test_cold_source_compiler_retains_both_exact_sorcerer_bindings_and_definition_closure(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path
    )
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
capability_rows = compiled.capability_source_bindings
cast_rows = compiled.cast_source_bindings
assert len(capability_rows) == len(cast_rows) == 1
capability = capability_rows[0]
cast = cast_rows[0]
from TOOLS import activity_contracts as contracts
source_basis = contracts.validate_source_basis_result(
    json.loads(sys.argv[5]), compiled=compiled
)
incomplete_selected_support = json.loads(sys.argv[5])
incomplete_selected_support["activity_closure_ids"].remove(
    "activity.spell.fire_bolt"
)
try:
    contracts.validate_source_basis_result(
        incomplete_selected_support, compiled=compiled
    )
except contracts.ActivityContractError:
    pass
else:
    raise AssertionError("source result accepted an omitted selected spell Activity")
assert capability.binding.consumer_id == identity + ".step.1.steps.step.0"
assert cast.binding.consumer_id == identity + ".step.1.steps.step.0"
assert capability.binding.profile_generation == cast.binding.profile_generation == 1
assert capability.binding.source_variant == cast.binding.source_variant == "SORCERER_1"
assert capability.binding.source_spell_id == cast.binding.source_spell_id == "spell.magic_missile"
assert source_basis.value["consumer_id"] == capability.binding.consumer_id
assert source_basis.value["profile_id"] == capability.binding.profile_id
assert source_basis.value["profile_generation"] == capability.binding.profile_generation
assert source_basis.value["source_spell_id"] == capability.binding.source_spell_id
assert source_basis.value["mode_id"] is None
assert source_basis.value["facets"]["source_mode"] == "NOT_EVALUATED"
expected_spell_activities = set(json.loads(sys.argv[6]))
expected_primitive_dependencies = json.loads(sys.argv[8])
assert set(source_basis.value["activity_closure_ids"]) == expected_spell_activities
assert set(source_basis.value["read_refs"]) == set(capability.dependency_read_refs)
assert {
    (reference["definition_id"], reference["kind"])
    for reference in source_basis.value["source_definition_refs"]
} == {
    (reference.definition_id, reference.kind)
    for reference in capability.binding.source_definition_refs
}
unowned_option_result = json.loads(sys.argv[5])
unowned_cantrips = list(
    unowned_option_result["acquisition"]["cantrip_spell_ids"]
)
unowned_cantrips[0] = "spell.unlisted"
unowned_cantrips.sort()
unowned_option_result["acquisition"]["cantrip_spell_ids"] = unowned_cantrips
unowned_option_result["acquisition"]["cantrip_option_ids"] = [
    "option." + spell_id for spell_id in unowned_cantrips
]
unowned_option_result["acquisition"]["known_spell_ids"] = sorted(
    [*unowned_cantrips, *unowned_option_result["acquisition"]["level1_spell_ids"]]
)
try:
    contracts.validate_source_basis_result(
        unowned_option_result, compiled=compiled
    )
except contracts.ActivityContractError:
    pass
else:
    raise AssertionError("source result accepted a spell absent from its owner slots")
assert "activity.spell.magic_missile" in compiled.dependency_ids
expected_definitions = set(json.loads(sys.argv[4]))
assert set(capability.definition_contracts) == expected_definitions
assert set(cast.definition_contracts) == expected_definitions
assert set(compiled.dependency_ids) >= expected_definitions
assert expected_spell_activities <= {
    identity
    for identity, contract in capability.definition_contracts.items()
    if contract["kind"] == "definition.activity"
}
for activity_id, primitive_ids in expected_primitive_dependencies.items():
    assert capability.source_activity_primitive_ids[activity_id] == tuple(primitive_ids)
assert {
    "asset.arcane_focus",
    "effect.innate_sorcery",
    "feature.sorcerer.innate_sorcery",
        "feature.sorcerer.spellcasting",
        "resource.innate_sorcery",
        "resource.spell_slot.level_1",
        *json.loads(sys.argv[7]),
} <= set(capability.definition_contracts)
assert all(
    capability.definition_contracts[activity_id]["data"]["steps"]
    and capability.definition_contracts[activity_id]["data"]["steps"][0]["op"]
    != "op.branch"
    for activity_id in expected_spell_activities
)
definition_edges = {
    (edge.source_ref, edge.dependency_ref)
    for edge in capability.dependency_edges
}
assert ("bound_definition:class.sorcerer", "bound_definition:advancement.sorcerer.mvp_1") in definition_edges
assert ("bound_definition:advancement.sorcerer.mvp_1", "bound_definition:feature.sorcerer.spellcasting") in definition_edges
assert ("bound_definition:feature.sorcerer.innate_sorcery", "bound_definition:effect.innate_sorcery") in definition_edges
for selected_spell_id in source_basis.value["acquisition"]["known_spell_ids"]:
    activity_ids = capability.definition_contracts[selected_spell_id]["data"]["activity_ids"]
    for selected_activity_id in activity_ids:
        assert (
            f"bound_definition:{selected_spell_id}",
            f"bound_definition:{selected_activity_id}",
        ) in definition_edges
assert capability.selector_contracts == {}
assert capability.accessor_contracts == {}
assert capability.derived_node_contracts == {}
inner_consumer = compiled.instructions[1].children[0]
assert not ({"selector:attack.roll", "selector:spell.dc"} & set(inner_consumer.read_contract_refs))
assert not any(reference.startswith("selector:") for reference in capability.dependency_read_refs)
assert capability.role_contracts["actor"]["family_key"] == "world.actor"
assert capability.binding.context_fact_ids == ()
assert cast.binding.context_fact_ids == ()
assert not any(
    row.binding.profile_id == "calculation.capability_projection_srd521"
    for row in compiled.calculation_policy_bindings
)
assert any(
    row.binding.profile_id == "calculation.roll_advantage_srd521"
    and row.binding.selector_operation_pairs
    for row in compiled.calculation_policy_bindings
)
from dataclasses import replace
import copy
assert contracts._compiler_value_is_issued(
    compiled, kind="compiled", parent=catalog.catalog_context
)
assert not contracts._compiler_value_is_issued(
    copy.copy(compiled), kind="compiled", parent=catalog.catalog_context
)
assert not contracts._compiler_value_is_issued(
    replace(compiled), kind="compiled", parent=catalog.catalog_context
)
try:
    contracts.validate_source_basis_result(
        json.loads(sys.argv[5]), compiled=copy.copy(compiled)
    )
except contracts.ActivityContractError:
    pass
else:
    raise AssertionError("source result accepted a copied, unissued compiler value")
try:
    capability.definition_contracts["class.sorcerer"]["id"] = "class.fighter"
except TypeError:
    pass
else:
    raise AssertionError("compiled source definition contracts must be immutable")
try:
    replace(
        compiled,
        instructions=(inner_consumer, inner_consumer),
        profile_bindings=(),
        calculation_policy_bindings=(),
        cast_profile_bindings=(),
        damage_input_bindings=(),
        capability_source_bindings=(),
        cast_source_bindings=(),
    )
except contracts.ActivityContractError as error:
    assert "duplicate instruction occurrence" in str(error)
else:
    raise AssertionError("copied duplicate consumer occurrence retained compiler validity")
print(json.dumps({
    "capability_consumer": capability.binding.consumer_id,
    "cast_consumer": cast.binding.consumer_id,
    "definition_ids": sorted(capability.definition_contracts),
    "dependency_refs": list(capability.dependency_read_refs),
}))
"""
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        "[]",
        json.dumps(sorted(reference["definition_id"] for reference in DEFINITION_REFS)),
        json.dumps(
            _source_basis_result(
                consumer_id="activity.conformance.compiler.step.1.steps.step.0"
            )
        ),
        json.dumps(list(ACTIVITY_IDS)),
        json.dumps(list(KNOWN_IDS)),
        json.dumps(SOURCE_ACTIVITY_PRIMITIVE_IDS),
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_cold_source_profiles_keep_independent_exact_consumer_occurrences(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation="distinct_consumers"
    )
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
capability = compiled.capability_source_bindings[0]
cast = compiled.cast_source_bindings[0]
assert capability.binding.consumer_id == identity + ".step.0"
assert cast.binding.consumer_id == identity + ".step.1.steps.step.0"
assert set(capability.choice_slot_contracts) == {
    "advancement.sorcerer.level_1.cantrips",
    "advancement.sorcerer.level_1.prepared_spells",
}
assert capability.binding.profile_generation == cast.binding.profile_generation == 1
assert capability.binding.source_spell_id == cast.binding.source_spell_id
print(json.dumps({"capability": capability.binding.consumer_id, "cast": cast.binding.consumer_id}))
"""
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode == 0, result.stderr or result.stdout


@pytest.mark.parametrize(
    "invalidation", ("cache_removed", "source_descriptor", "instruction")
)
def test_cold_source_descriptor_cache_rebuild_preserves_exact_frozen_bindings(
    conformance_runtime_root: Path,
    tmp_path: Path,
    invalidation: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path
    )
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
from copy import copy
from types import MappingProxyType
from TOOLS import activity_contracts as contracts

def source_binding_state(rows):
    return tuple(
        (
            row.binding,
            dict(row.definition_contracts),
            dict(row.choice_slot_contracts),
            dict(row.selector_contracts),
            dict(row.accessor_contracts),
            dict(row.derived_node_contracts),
            dict(row.source_activity_primitive_ids),
            dict(row.role_contracts),
            row.dependency_read_refs,
            row.dependency_edges,
        )
        for row in rows
    )

def instruction_consumers(rows):
    pending = list(rows)
    result = []
    while pending:
        instruction = pending.pop(0)
        result.append((instruction.consumer_id, instruction.primitive_id))
        pending.extend(instruction.children)
    return tuple(result)

expected_capability = source_binding_state(compiled.capability_source_bindings)
expected_cast = source_binding_state(compiled.cast_source_bindings)
expected_instructions = instruction_consumers(compiled.instructions)
expected_dependencies = compiled.dependency_ids
expected_profiles = compiled.profile_bindings
expected_cast_profiles = compiled.cast_profile_bindings
expected_calculation_policies = compiled.calculation_policy_bindings
expected_basis = contracts.validate_source_basis_result(
    json.loads(sys.argv[5]), compiled=compiled
)
if __INVALIDATION__ == "cache_removed":
    object.__setattr__(catalog, "compiled_activities", MappingProxyType({}))
elif __INVALIDATION__ == "source_descriptor":
    object.__setattr__(
        compiled.capability_source_bindings[0],
        "choice_slot_contracts",
        MappingProxyType({}),
    )
elif __INVALIDATION__ == "instruction":
    object.__setattr__(
        compiled.instructions[0], "primitive_id", "op.review_not_registered"
    )
else:
    raise AssertionError("unknown cache invalidation case")

rebuilt = compile_activity(catalog, identity)
assert rebuilt is not compiled
assert source_binding_state(rebuilt.capability_source_bindings) == expected_capability
assert source_binding_state(rebuilt.cast_source_bindings) == expected_cast
assert instruction_consumers(rebuilt.instructions) == expected_instructions
assert rebuilt.dependency_ids == expected_dependencies
assert rebuilt.profile_bindings == expected_profiles
assert rebuilt.cast_profile_bindings == expected_cast_profiles
assert rebuilt.calculation_policy_bindings == expected_calculation_policies
assert catalog.compiled_activities[identity] is rebuilt
assert contracts._compiler_value_is_issued(
    rebuilt, kind="compiled", parent=catalog.catalog_context
)
rebuilt_basis = contracts.validate_source_basis_result(
    json.loads(sys.argv[5]), compiled=rebuilt
)
assert rebuilt_basis.value == expected_basis.value
try:
    contracts.validate_source_basis_result(
        json.loads(sys.argv[5]), compiled=copy(rebuilt)
    )
except contracts.ActivityContractError:
    pass
else:
    raise AssertionError("copied rebuilt source compiler value was accepted")
assert compile_activity(catalog, identity) is rebuilt
print("DESCRIPTOR_CACHE_REBUILD_RETAINED_EXACT_FROZEN_SOURCE")
""".replace("__INVALIDATION__", repr(invalidation))
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
        "[]",
        json.dumps(sorted(reference["definition_id"] for reference in DEFINITION_REFS)),
        json.dumps(
            _source_basis_result(
                consumer_id=("activity.conformance.compiler.step.1.steps.step.0")
            )
        ),
        json.dumps(list(ACTIVITY_IDS)),
        json.dumps(list(KNOWN_IDS)),
        json.dumps(SOURCE_ACTIVITY_PRIMITIVE_IDS),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "DESCRIPTOR_CACHE_REBUILD_RETAINED_EXACT_FROZEN_SOURCE" in result.stdout


@pytest.mark.parametrize("frozen_mismatch", ("member_bytes", "foreign_member"))
def test_cold_source_descriptor_rebuild_rejects_mismatched_frozen_package_members(
    conformance_runtime_root: Path,
    tmp_path: Path,
    frozen_mismatch: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path
    )
    probe = (
        catalog_tests._RECIPE_PROBE
        + r"""
from types import MappingProxyType
from TOOLS.activity_runtime import ActivityRuntimeError

members = dict(catalog.frozen_semantic_members)
if __MISMATCH__ == "member_bytes":
    member_key = next(iter(members))
    members[member_key] = b"{}\n"
elif __MISMATCH__ == "foreign_member":
    member_key = next(iter(members))
    members[("package.foreign", member_key[1])] = members[member_key]
else:
    raise AssertionError("unknown frozen-source mismatch case")
object.__setattr__(catalog, "frozen_semantic_members", MappingProxyType(members))
try:
    compile_activity(catalog, identity)
except ActivityRuntimeError as error:
    assert "Activity catalog is not compiler-issued" in str(error)
else:
    raise AssertionError("mismatched frozen source retained catalog issuance")
""".replace("__MISMATCH__", repr(frozen_mismatch))
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        probe,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode == 0, result.stderr or result.stdout


@pytest.mark.parametrize(
    ("mutation", "diagnostic"),
    [
        ("unknown_dependency", "unavailable source definition dependency"),
        ("wrong_role", "source binding native role is not declared"),
        ("wrong_definition_ref", "source definition reference kind differs"),
        (
            "transitive_definition",
            "source definition references omit automatic grant",
        ),
        (
            "missing_data_activity_reference",
            "source definition references omit spell data Activity",
        ),
        (
            "missing_activity_definition_record",
            "source-bound Activity is unavailable in frozen package source: activity.spell.fire_bolt",
        ),
        (
            "missing_second_activity_definition",
            "source-bound Activity is unavailable in frozen package source: activity.spell.fire_bolt.alternate",
        ),
        (
            "missing_spell_primitive_dependency",
            "source primitive dependencies differ from Activity closure",
        ),
        (
            "missing_primitive_member_with_unregistered_op",
            "unknown or dormant primitive: op.review_not_registered",
        ),
        (
            "missing_primitive_member_with_dormant_op",
            "unknown or dormant primitive: op.branch",
        ),
        (
            "missing_primitive_member_with_unadmitted_op",
            "has no exact consumer activity.spell.fire_bolt",
        ),
        (
            "missing_spellcasting_resource_reference",
            "source definition references omit feature resource",
        ),
        (
            "missing_innate_effect_reference",
            "source definition references omit feature Effect",
        ),
        (
            "binding_missing_asset_reference",
            "source definition references differ from transitive closure",
        ),
        ("definition_cycle", "definition dependency cycle"),
        ("unknown_facet", "activity-compiler-declaration is not admitted"),
        ("fact_dependency", "activity-compiler-declaration is not admitted"),
        ("missing_profile", "source binding has no exact profile binding"),
        ("foreign_consumer", "Activity profile binding is not admitted"),
        ("wrong_profile_generation", "activity-compiler-declaration is not admitted"),
        ("unknown_selector", "unknown selector read"),
        (
            "unknown_accessor",
            "accessor is unknown, dormant, or unauthorized: source.missing",
        ),
        ("bundle_choice_payload", "Sorcerer option must grant exactly one spell"),
        (
            "known_binding_mismatch",
            "Sorcerer known binding differs from its one-spell grant",
        ),
        (
            "prepared_binding_mismatch",
            "Sorcerer prepared binding differs from its one-spell grant",
        ),
        (
            "starting_asset_per_choice",
            "Sorcerer spell choice cannot carry independent starting assets",
        ),
        (
            "cross_slot_spell_level",
            "Sorcerer slot contains a spell at the wrong source level",
        ),
    ],
)
def test_cold_source_compiler_rejects_unclosed_source_binding_edges(
    conformance_runtime_root: Path,
    tmp_path: Path,
    mutation: str,
    diagnostic: str,
) -> None:
    from DEV.TESTS import test_local_spell_catalog as catalog_tests

    runtime_root, recipe, dependency_kinds = _cold_source_compiler_fixture(
        conformance_runtime_root, tmp_path, mutation=mutation
    )
    result = catalog_tests._run_installed_runtime_probe(
        runtime_root,
        catalog_tests._RECIPE_PROBE,
        json.dumps(recipe),
        json.dumps(dependency_kinds),
    )
    assert result.returncode != 0
    assert diagnostic in result.stderr


@pytest.mark.parametrize(
    ("route_case", "expected_route", "expected_disposition"),
    [
        (
            "actual_magic_missile",
            True,
            "SELECTED_PREPARED_LEVEL1",
        ),
        (
            "cross_spell_union",
            False,
            "SELECTED_KNOWN_CANTRIP",
        ),
        (
            "missing_selected_edge",
            False,
            "SELECTED_PREPARED_LEVEL1",
        ),
        (
            "multi_activity_nonfirst",
            True,
            "UNAVAILABLE",
        ),
    ],
)
def test_installed_source_route_requires_the_bound_spell_activity_edge(
    conformance_runtime_root: Path,
    tmp_path: Path,
    route_case: str,
    expected_route: bool,
    expected_disposition: str,
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root, tmp_path, route_case=route_case
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / route_case,
        test_name="PinnedNativeSourceBasisTests.test_selected_source_route_proof",
        route_activity_in_package=True,
        expected_route=expected_route,
        expected_disposition=expected_disposition,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("source_mode_case", "diagnostic"),
    (
        ("duplicate_key", "source spell repeats a source mode key"),
        ("foreign_activity", "source mode Activity is not linked by its spell"),
        ("missing_definition", None),
        (
            "missing_edge",
            "source definition references omit spell data Activity",
        ),
    ),
)
def test_cold_source_compiler_rejects_conflicting_or_foreign_source_mode_rows(
    conformance_runtime_root: Path,
    tmp_path: Path,
    source_mode_case: str,
    diagnostic: str | None,
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        source_mode_case=source_mode_case,
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / f"source-mode-{source_mode_case}",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_route_proof",
        route_activity_in_package=True,
        expected_disposition="SELECTED_PREPARED_LEVEL1",
    )

    assert result.returncode != 0, result.stdout
    if diagnostic is not None:
        assert diagnostic in result.stdout + result.stderr


def test_absent_optional_source_mode_keeps_the_selected_route_partial(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        source_mode_case="absent",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "absent-optional-source-mode",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_route_proof",
        route_activity_in_package=True,
        expected_route=True,
        expected_disposition="SELECTED_PREPARED_LEVEL1",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_named_source_mode_absence_holds_without_upgrading_source_basis(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        source_mode_case="absent",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "named-mode-absent-holds",
        test_name=(
            "PinnedNativeSourceBasisTests."
            "test_selected_source_mode_holds_when_declaration_is_absent"
        ),
        route_activity_in_package=True,
        source_mode_case="absent",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_ambiguous_modes_for_the_selected_activity_hold(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        source_mode_case="ambiguous_activity",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "ambiguous-modes-hold",
        test_name=(
            "PinnedNativeSourceBasisTests."
            "test_selected_source_mode_holds_when_activity_mapping_is_ambiguous"
        ),
        route_activity_in_package=True,
        expected_disposition="SELECTED_PREPARED_LEVEL1",
        source_mode_case="ambiguous_activity",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_magic_missile_named_source_mode_is_derived_from_private_declaration(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "installed-named-magic-missile-mode",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_mode_proof",
        route_activity_in_package=True,
        expected_disposition="SELECTED_PREPARED_LEVEL1",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_nonfirst_activity_uses_its_exact_reordered_mode_and_stays_unavailable(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        route_case="multi_activity_nonfirst",
        source_mode_case="reordered",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "nonfirst-reordered-mode-unavailable",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_mode_proof",
        route_activity_in_package=True,
        expected_disposition="UNAVAILABLE",
        expected_mode_id="mode.fixture_unselected.alternate",
        expected_source_spell_id="spell.fixture_unselected",
        source_mode_case="reordered",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_named_source_mode_does_not_upgrade_prohibited_spell(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        route_case="source_prohibited_spell",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "prohibited-spell-mode-remains-prohibited",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_mode_proof",
        route_activity_in_package=True,
        expected_disposition="PROHIBITED",
        expected_mode_id="mode.fixture_level3.ordinary",
        expected_source_spell_id="spell.fixture_level3",
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_source_mode_changes_existing_compiler_context_identity(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "source-mode-retained-identity",
        test_name=(
            "PinnedNativeSourceBasisTests."
            "test_source_mode_descriptor_participates_in_retained_context_identity"
        ),
        route_activity_in_package=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_named_source_mode_rejects_package_path_tampering(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "tampered-source-package-path",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_mode_proof",
        route_activity_in_package=True,
        tamper_package_path=True,
    )

    assert result.returncode != 0
    assert "rebuilt admitted lock does not match ruleset_lock" in result.stderr


@pytest.mark.parametrize(
    ("symbol_case", "diagnostic"),
    [
        (
            "missing",
            "compiled symbol has unavailable source producer contract: compiled.one_dart_force_damage",
        ),
        (
            "wrong_type",
            "compiled producer has wrong type/cardinality: compiled.one_dart_force_damage",
        ),
        (
            "wrong_occurrence",
            "compiled producer is unauthorized for activity.spell.magic_missile.step.2.steps.step.0",
        ),
        (
            "cycle",
            "compiled producer dependency cycle: compiled.one_dart_force_damage",
        ),
    ],
)
def test_installed_magic_missile_route_requires_its_occurrence_scoped_literal(
    conformance_runtime_root: Path,
    tmp_path: Path,
    symbol_case: str,
    diagnostic: str,
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        route_case="actual_magic_missile",
        symbol_case=symbol_case,
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / f"literal-{symbol_case}",
        test_name="PinnedNativeSourceBasisTests.test_selected_source_route_proof",
        route_activity_in_package=True,
    )
    assert result.returncode != 0, result.stdout
    assert diagnostic in result.stderr


@pytest.mark.parametrize(
    "installed_test_name",
    (
        "test_selected_route_does_not_trust_a_valid_alternative_native_basis",
        "test_selected_route_rejects_a_caller_supplied_context_identity_prefix",
        "test_selected_route_does_not_accept_foreign_actor_or_ability_basis_values",
    ),
)
def test_installed_source_route_rejects_unissued_basis_mutations(
    conformance_runtime_root: Path,
    tmp_path: Path,
    installed_test_name: str,
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        route_case="multi_activity_nonfirst",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / installed_test_name,
        test_name=f"PinnedNativeSourceBasisTests.{installed_test_name}",
        route_activity_in_package=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_installed_actual_source_route_revalidates_native_context_and_membership(
    conformance_runtime_root: Path, tmp_path: Path
) -> None:
    from DEV.TESTS.test_sp03_native_source_basis import (
        _run_installed_source_basis_case,
    )

    runtime_root, recipe, dependency_kinds = _selected_source_route_compiler_fixture(
        conformance_runtime_root,
        tmp_path,
        route_case="actual_magic_missile",
    )
    result = _run_installed_source_basis_case(
        runtime_root,
        recipe,
        dependency_kinds,
        tmp_path / "actual-source-route-revalidation",
        test_name=(
            "PinnedNativeSourceBasisTests."
            "test_selected_source_route_rejects_copied_foreign_and_stale_inputs"
        ),
        route_activity_in_package=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
