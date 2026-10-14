"""Validate the frozen SRD spell research against pinned source-asset evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "DEV/SCHEMAS/spell-source-qualification.schema.json"
SOURCE_MANIFEST_PATH = (
    REPOSITORY_ROOT / "DEV/TESTS/fixtures/spell-source-qualification.json"
)
REVIEWED_SOURCE_MANIFEST_SHA256 = (
    "3fcbb6d7177a468e00803a2cbf4c8df9bd7021b291fdc7bad568edb194a652eb"
)
SOURCE_SEED_PATH = (
    REPOSITORY_ROOT
    / "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
)
REVIEWED_SEED_SNAPSHOT_SHA256 = (
    "711b6a2ec0173407825a9eee5a1432ac6e9ce07f47a1d9d378fd17aac8cf7550"
)
SEED_RELATIVE_PATH = (
    "GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-mvp-seed.json"
)
EXPECTED_SEED_RECORD_COLLECTIONS: dict[str, str] = {
    "spell.acid_splash": "definitions",
    "activity.spell.acid_splash": "activity_definitions",
    "spell.thunderclap": "definitions",
    "activity.spell.thunderclap": "activity_definitions",
}
EXPECTED_ACID_SPLASH_SOURCE_FACTS: dict[str, object] = {
    "school_id": "school.evocation",
    "targeting": {
        "target_mode": "POINT_CENTERED_SPHERE",
        "point_selection_range_feet": 60,
        "area_shape_id": "area.sphere",
        "area_radius_feet": 5,
        "affected_set": "CREATURES_IN_SPHERE",
        "legacy_two_target": False,
    },
}
ATTRIBUTION = (
    "This work includes material from the System Reference Document 5.2.1 "
    '("SRD 5.2.1") by Wizards of the Coast LLC, available at '
    "https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the "
    "Creative Commons Attribution 4.0 International License, available at "
    "https://creativecommons.org/licenses/by/4.0/legalcode."
)
EXPECTED_LEVEL_COUNTS: dict[int, int] = {
    0: 27,
    1: 57,
    2: 57,
    3: 42,
    4: 34,
    5: 38,
    6: 31,
    7: 20,
    8: 17,
    9: 16,
}
EVIDENCE_PATHS: dict[str, str] = {
    "spell-inventory": "DEV/docs/superpowers/research/2026-10-04-spell-coverage/spell-inventory.json",
    "source-pass-0-2": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-0-2.json",
    "source-pass-3-5": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-3-5.json",
    "source-pass-6-9": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-6-9.json",
    "source-body-witnesses": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-body-witnesses.json",
    "requirement-matrix": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/requirement-matrix.json",
    "source-obligation-resolution": "DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-obligation-resolution.md",
    "content-acquisition-contracts": "DEV/docs/superpowers/specs/2026-10-04-local-spell-content-acquisition-contracts.md",
}
TEXT_EVIDENCE_IDS = frozenset(
    {"source-obligation-resolution", "content-acquisition-contracts"}
)
PASS_RECORD_COUNTS: dict[str, int] = {
    "source-pass-0-2": 141,
    "source-pass-3-5": 114,
    "source-pass-6-9": 84,
}
EXPECTED_ASSET_LANGUAGES: dict[str, str] = {
    "srd52_en": "en",
    "srd52_de": "de",
    "srd52_es": "es",
    "srd52_fr": "fr",
    "srd52_it": "it",
}
SOURCE_MAPPING_LANE_EXPECTATIONS: dict[str, dict[str, object]] = {
    "source-pass-0-2": {
        "map_sha256": "4d4b16a820099a417403e1b9c60f737fd2e090a2c69020f14ea0d93c097b73c2",
        "receipt_sha256": "6b7c878f3dc9b3571ea4dc4b70b19a964ead135ac39d46b5dce33561c6f1ee7d",
        "source_pass_sha256": "23b8872290b5f9786468103faec036de153a4f62ad8dc568cf54f57f6f35c2c1",
        "mapping_payload_sha256": "033ee04e93bd2ddd0b835d9c66d2599c02d65f6df04a83306f79ff4aa04d66ff",
        "entry_count": 139,
    },
    "source-pass-3-5": {
        "map_sha256": "3f47531d9b6aec6eddf0c7209d669b0da195becbf8f0d21ea207539416454c17",
        "receipt_sha256": "59d8128502167f4651f135f8c3010c27fd8b26f57a6a9a253461650f46a1bb9e",
        "source_pass_sha256": "2a57acf7829e680e15952ee30b175a42be0eb62cc67b4951beeb0de8fbaf0d17",
        "mapping_payload_sha256": "48b7103837bad11c92f31b7cadc902da40ea321c018f08e3f539585ef6cde6f6",
        "entry_count": 114,
    },
    "source-pass-6-9": {
        "map_sha256": "7d177d47dbba5d7bb99e09459ee357222f799a82653977124d65220de30adb52",
        "receipt_sha256": "4b93a95094fe4ca4e06a138ac091c19f79fe7939075140aa09fc1f00904483e1",
        "source_pass_sha256": "23f57b38f89c326fa46b7961d9994342bb7cc92d664201ce1289eb3668955cd6",
        "mapping_payload_sha256": "dc3a4d30ce2d58b9cc102945a0fc4f2126cf8e0eb06b0f791ddd92d90e94119b",
        "entry_count": 84,
    },
}
EXPECTED_WITNESSES: dict[str, dict[str, object]] = {
    "animate-objects-owner": {
        "owner_spell": "Animate Objects",
        "artifact_id": "source-pass-3-5",
        "printed_pages": [109],
        "reconstruction_obligation_ids": [
            "source_reconstruction.animate_objects.animated_object_stat_block",
        ],
        "source_locators": [("srd52_en", 109, "Animate Objects / Animated Object")],
        "accepted_segments": ["animate_objects_body", "animated_object_stat_block"],
        "excluded_segments": [
            "antilife_shell_body",
            "antipathy_sympathy_tail",
            "page_number",
            "document_title",
            "next_spell_heading",
            "pdf_control_character",
        ],
        "status": "VISUALLY_RECONSTRUCTED",
    },
    "antilife-shell-owner": {
        "owner_spell": "Antilife Shell",
        "artifact_id": "source-pass-3-5",
        "printed_pages": [109],
        "reconstruction_obligation_ids": [
            "source_reconstruction.antilife_shell.barrier_termination",
        ],
        "source_locators": [("srd52_en", 109, "Antilife Shell")],
        "accepted_segments": ["antilife_shell_body", "barrier_termination_tail"],
        "excluded_segments": [
            "antipathy_sympathy_tail",
            "page_number",
            "document_title",
            "next_spell_heading",
            "pdf_control_character",
        ],
        "status": "VISUALLY_RECONSTRUCTED",
    },
    "antipathy-sympathy-owner": {
        "owner_spell": "Antipathy/Sympathy",
        "artifact_id": "source-pass-6-9",
        "printed_pages": [109, 110],
        "reconstruction_obligation_ids": [
            "source_reconstruction.antipathy_sympathy.ending_save_tail",
            "source_reconstruction.antipathy_sympathy.one_minute_immunity_tail",
        ],
        "source_locators": [
            ("srd52_en", 109, "Antipathy/Sympathy"),
            ("srd52_en", 110, "Ending the Effect"),
        ],
        "accepted_segments": [
            "antipathy_sympathy_body",
            "ending_save_tail",
            "one_minute_immunity_tail",
        ],
        "excluded_segments": [
            "animated_object_stat_block",
            "page_number",
            "document_title",
            "next_spell_heading",
            "pdf_control_character",
        ],
        "status": "VISUALLY_RECONSTRUCTED",
    },
    "find-steed-owner": {
        "owner_spell": "Find Steed",
        "artifact_id": "source-pass-0-2",
        "printed_pages": [131],
        "reconstruction_obligation_ids": [
            "source_reconstruction.find_steed.otherworldly_steed_stat_block",
        ],
        "source_locators": [("srd52_en", 131, "Find Steed / Otherworldly Steed")],
        "accepted_segments": ["find_steed_body", "otherworldly_steed_stat_block"],
        "excluded_segments": [
            "find_the_path_continuation",
            "page_number",
            "document_title",
            "next_spell_heading",
            "pdf_control_character",
        ],
        "status": "VISUALLY_RECONSTRUCTED",
    },
    "find-the-path-owner": {
        "owner_spell": "Find the Path",
        "artifact_id": "source-pass-6-9",
        "printed_pages": [131],
        "reconstruction_obligation_ids": [
            "source_reconstruction.find_the_path.branch_choice_tail",
        ],
        "source_locators": [
            ("srd52_en", 131, "Find the Path / branch-choice continuation")
        ],
        "accepted_segments": ["find_the_path_body", "branch_choice_tail"],
        "excluded_segments": [
            "otherworldly_steed_stat_block",
            "page_number",
            "document_title",
            "next_spell_heading",
            "pdf_control_character",
        ],
        "status": "VISUALLY_RECONSTRUCTED",
    },
    "telekinesis-owner": {
        "owner_spell": "Telekinesis",
        "artifact_id": "source-pass-3-5",
        "printed_pages": [168],
        "reconstruction_obligation_ids": [
            "source_reconstruction.telekinesis.fine_control_simple_tool",
        ],
        "source_locators": [("srd52_en", 168, "Telekinesis")],
        "accepted_segments": [
            "telekinesis_creature_mode",
            "telekinesis_object_mode",
            "fine_control_simple_tool_clause",
        ],
        "excluded_segments": [
            "next_spell_heading",
            "page_number",
            "document_title",
            "pdf_control_character",
            "legacy_2014_contest_rules",
        ],
        "status": "LICENSED_TRANSLATIONS_CLOSE_AT_SIMPLE_TOOL; EXTENDED_EXAMPLES_CORROBORATION_ONLY",
    },
}
TELEKINESIS_TRANSLATION_LOCATORS: tuple[tuple[str, int, str], ...] = (
    ("srd52_de", 180, "Telekinese"),
    ("srd52_es", 187, "Telequinesis"),
    ("srd52_fr", 181, "Télékinésie"),
    ("srd52_it", 194, "Telecinesi"),
)
EXPECTED_GLYPH_WITNESSES: dict[str, tuple[str, int, str, str]] = {
    "U+2212": ("Animate Objects", 109, "Animated Object Intelligence modifier", "−4"),
    "U+00D7": ("Earthquake", 127, "Fissure depth multiplier", "1d10 × 10 feet"),
}


class SourceQualificationError(ValueError):
    """A source manifest, source asset, or pinned research join is invalid."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        super().__init__(f"{code}: {detail}")


def _fail(code: str, detail: str) -> None:
    raise SourceQualificationError(code, detail)


def _object(value: object, path: str) -> dict[str, object]:
    if not isinstance(value, dict):
        _fail("invalid_shape", f"{path} must be an object")
    return value


def _array(value: object, path: str) -> list[object]:
    if not isinstance(value, list):
        _fail("invalid_shape", f"{path} must be an array")
    return value


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value:
        _fail("invalid_shape", f"{path} must be a non-empty string")
    return value


def _digest(data: bytes, basis: str) -> str:
    if basis == "LF_NORMALIZED_UTF8":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    elif basis != "RAW_UTF8":
        _fail("invalid_hash_basis", f"unknown source artifact hash basis {basis!r}")
    return hashlib.sha256(data).hexdigest()


def _decode_json(data: bytes, artifact_id: str) -> dict[str, object]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceQualificationError(
            "invalid_evidence_json", f"{artifact_id} is not UTF-8 JSON"
        ) from exc
    return _object(value, artifact_id)


def _validate_reviewed_manifest(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    path = SOURCE_MANIFEST_PATH.resolve()
    if not path.is_relative_to(REPOSITORY_ROOT) or not path.is_file():
        _fail(
            "reviewed_manifest_missing", "the reviewed source registry is unavailable"
        )
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != REVIEWED_SOURCE_MANIFEST_SHA256:
        _fail("reviewed_manifest_bytes", "reviewed source registry bytes changed")
    reviewed = _decode_json(data, "reviewed source registry")
    if dict(manifest) != reviewed:
        _fail(
            "reviewed_manifest_mismatch",
            "caller manifest differs from the reviewed immutable source registry",
        )
    return reviewed


def _validate_manifest_schema(manifest: Mapping[str, object]) -> None:
    schema = _decode_json(
        SCHEMA_PATH.read_bytes(), "spell-source-qualification.schema.json"
    )
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(dict(manifest)),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "manifest"
        raise SourceQualificationError(
            "manifest_schema", f"{location}: {error.message}"
        )


def _load_evidence(manifest: Mapping[str, object]) -> dict[str, object]:
    evidence_rows = _array(manifest.get("evidence_artifacts"), "evidence_artifacts")
    expected_ids = set(EVIDENCE_PATHS)
    rows_by_id: dict[str, dict[str, object]] = {}
    for index, raw in enumerate(evidence_rows):
        row = _object(raw, f"evidence_artifacts[{index}]")
        artifact_id = _string(
            row.get("artifact_id"), f"evidence_artifacts[{index}].artifact_id"
        )
        if artifact_id in rows_by_id:
            _fail("duplicate_evidence", f"duplicate evidence artifact {artifact_id}")
        if artifact_id not in EVIDENCE_PATHS:
            _fail("foreign_evidence", f"unexpected evidence artifact {artifact_id}")
        relative_path = _string(row.get("path"), f"evidence_artifacts[{index}].path")
        if relative_path != EVIDENCE_PATHS[artifact_id]:
            _fail(
                "foreign_evidence_path", f"{artifact_id} does not use its pinned path"
            )
        target = (REPOSITORY_ROOT / relative_path).resolve()
        if not target.is_relative_to(REPOSITORY_ROOT) or not target.is_file():
            _fail(
                "missing_evidence",
                f"pinned evidence file is unavailable: {relative_path}",
            )
        data = target.read_bytes()
        basis = _string(
            row.get("hash_basis"), f"evidence_artifacts[{index}].hash_basis"
        )
        observed_hash = _digest(data, basis)
        expected_hash = _string(
            row.get("sha256"), f"evidence_artifacts[{index}].sha256"
        )
        if observed_hash != expected_hash:
            _fail("stale_evidence", f"pinned evidence hash differs: {relative_path}")
        rows_by_id[artifact_id] = {"metadata": row, "bytes": data}
    if set(rows_by_id) != expected_ids:
        missing = sorted(expected_ids - set(rows_by_id))
        _fail("missing_evidence", f"required evidence artifacts are absent: {missing}")

    parsed: dict[str, object] = {}
    for artifact_id, record in rows_by_id.items():
        data = record["bytes"]
        if not isinstance(data, bytes):
            _fail("invalid_evidence", f"{artifact_id} bytes are unavailable")
        if artifact_id in TEXT_EVIDENCE_IDS:
            continue
        parsed[artifact_id] = _decode_json(data, artifact_id)
        metadata = _object(record["metadata"], f"{artifact_id}.metadata")
        expected_count = metadata.get("record_count")
        if expected_count is not None:
            record_key = (
                "spells"
                if artifact_id in {"spell-inventory", "requirement-matrix"}
                else "rows"
            )
            records = _array(
                parsed[artifact_id].get(record_key), f"{artifact_id}.{record_key}"
            )
            if type(expected_count) is not int or len(records) != expected_count:
                _fail("stale_evidence_count", f"{artifact_id} record count differs")
    return parsed


def _rows(
    payload: Mapping[str, object], key: str, artifact_id: str
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for index, value in enumerate(_array(payload.get(key), f"{artifact_id}.{key}")):
        result.append(_object(value, f"{artifact_id}.{key}[{index}]"))
    return result


def _resolve_json_pointer(payload: object, pointer: str, context: str) -> object:
    if pointer == "":
        return payload
    if not pointer.startswith("/"):
        _fail("source_pointer_invalid", f"{context} is not a JSON pointer")
    current = payload
    for encoded in pointer.split("/")[1:]:
        token = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            try:
                current = current[int(token)]
            except (ValueError, IndexError) as exc:
                raise SourceQualificationError(
                    "source_pointer_invalid",
                    f"{context} points outside its source array",
                ) from exc
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            _fail(
                "source_pointer_invalid", f"{context} points outside its source object"
            )
    return current


def _unique_name_index(
    rows: list[dict[str, object]], label: str
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for index, row in enumerate(rows):
        name = _string(row.get("name"), f"{label}[{index}].name")
        if name in result:
            _fail("duplicate_source_name", f"{label} contains duplicate name {name}")
        result[name] = row
    return result


def _canonical_source_name(
    row: Mapping[str, object], artifact_id: str
) -> tuple[str, str, str]:
    raw_name = _string(row.get("name"), f"{artifact_id}.row.name")
    exact_name_value = row.get("source_exact_name", raw_name)
    exact_name = _string(
        exact_name_value, f"{artifact_id}.{raw_name}.source_exact_name"
    )
    alias_status = (
        "EXPLICIT_SOURCE_EXACT_NAME" if exact_name != raw_name else "EXACT_NAME_MATCH"
    )
    return raw_name, exact_name, alias_status


def _validate_source_name_aliases(
    manifest: Mapping[str, object],
    source_rows: list[tuple[str, dict[str, object]]],
    inventory_by_name: Mapping[str, dict[str, object]],
) -> None:
    aliases = [
        _object(value, f"source_name_aliases[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_name_aliases"), "source_name_aliases")
        )
    ]
    observed_aliases: list[tuple[str, str, str, dict[str, object]]] = []
    for artifact_id, row in source_rows:
        raw_name, exact_name, status = _canonical_source_name(row, artifact_id)
        if status == "EXPLICIT_SOURCE_EXACT_NAME":
            observed_aliases.append((artifact_id, raw_name, exact_name, row))
    if len(aliases) != 1 or len(observed_aliases) != 1:
        _fail(
            "source_name_alias_census",
            "the one explicit source-name alias must be witnessed",
        )
    alias = aliases[0]
    artifact_id, raw_name, exact_name, row = observed_aliases[0]
    inventory_name = _string(
        alias.get("inventory_exact_name"), "source_name_aliases.inventory_exact_name"
    )
    body_hash = _string(row.get("body_sha256"), f"{raw_name}.body_sha256")
    source_assets = [
        _object(value, f"source_assets[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_assets"), "source_assets")
        )
    ]
    asset_by_id = {str(asset.get("asset_id")): asset for asset in source_assets}
    if (
        alias.get("artifact_id") != artifact_id
        or alias.get("raw_source_pass_name") != raw_name
        or alias.get("source_exact_name") != exact_name
        or alias.get("inventory_exact_name") != exact_name
        or inventory_name != exact_name
        or exact_name not in inventory_by_name
        or row.get("source_page") != alias.get("printed_page")
        or row.get("source_header_line") != alias.get("source_header_line")
        or alias.get("raw_body_sha256") != body_hash
        or alias.get("asset_id") != "srd52_en"
        or alias.get("printed_page") != 140
        or alias.get("source_heading") != "Heroes’ Feast"
        or alias.get("disposition")
        != "EXPLICIT_SOURCE_EXACT_NAME_ALIAS_VISUALLY_CONFIRMED"
        or asset_by_id.get("srd52_en") is None
    ):
        _fail(
            "source_name_alias_mismatch",
            "Heroes’ Feast alias is not bound to the exact official source heading",
        )


def _strings(value: object, path: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    result: list[str] = []
    for index, item in enumerate(_array(value, path)):
        result.append(_string(item, f"{path}[{index}]"))
    return result


def _row_modes(row: Mapping[str, object], name: str) -> list[str]:
    return _strings(
        row.get("required_modes_or_exceptions"), f"{name}.required_modes_or_exceptions"
    )


def _row_support(row: Mapping[str, object], name: str) -> list[str]:
    for field in (
        "dependencies_and_owner_obligations",
        "required_dependency_or_native_contracts",
    ):
        if field in row:
            return _strings(row[field], f"{name}.{field}")
    return []


def _row_research_dependencies(row: Mapping[str, object], name: str) -> list[str]:
    return _strings(
        row.get("inventory_dependency_labels"), f"{name}.inventory_dependency_labels"
    )


def _row_qualifications(row: Mapping[str, object], name: str) -> list[str]:
    return _strings(row.get("qualifications"), f"{name}.qualifications")


def _reviewed_full_body(row: Mapping[str, object]) -> bool:
    return (
        row.get("full_body_reviewed") is True
        or row.get("review")
        == "FULL_SUPPLIED_BODY_READ_AND_INDEPENDENT_REQUIREMENT_PARAPHRASE"
        or (
            isinstance(row.get("read_evidence"), str)
            and str(row["read_evidence"]).startswith(
                "Entire available raw body reviewed"
            )
        )
    )


def _slug(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if not normalized:
        _fail("invalid_source_name", f"cannot build a source key for {name!r}")
    return normalized


EXPECTED_MODE_REQUIREMENT_BRANCHES: dict[str, dict[str, dict[str, str]]] = {
    "Elementalism": {
        "breeze": {
            "spell.elementalism.breeze.bounded_output": "bounded_output",
            "spell.elementalism.breeze.held_door_exception": "held_door_exception",
        },
        "dust_sand": {
            "spell.elementalism.dust_sand.cover": "cover",
            "spell.elementalism.dust_sand.handwritten_word": "handwritten_word",
        },
        "fire_smoke": {
            "spell.elementalism.fire_smoke.harmless_effect": "harmless_effect",
            "spell.elementalism.fire_smoke.ignite_small_lights": "ignite_small_lights",
            "spell.elementalism.fire_smoke.scent_lifetime": "scent_lifetime",
        },
        "mist_clean_water": {
            "spell.elementalism.mist_clean_water.choice": "mist_or_clean_water",
            "spell.elementalism.mist_clean_water.evaporation_lifetime": "evaporation_lifetime",
        },
        "crude_element_shape": {
            "spell.elementalism.crude_element_shape.form": "crude_shape",
            "spell.elementalism.crude_element_shape.hour_lifetime": "one_hour_lifetime",
        },
    },
    "Alter Self": {
        "aquatic": {
            "spell.alter_self.aquatic.underwater_breathing": "underwater_breathing",
            "spell.alter_self.aquatic.swim_speed": "swim_speed_equals_current_speed",
        },
        "appearance": {
            "spell.alter_self.appearance.appearance_change": "appearance_change",
            "spell.alter_self.appearance.size_limbs_stats": "size_limb_and_stat_limits",
        },
        "natural_weapons": {
            "spell.alter_self.natural_weapons.choice": "natural_weapon_choice",
            "spell.alter_self.natural_weapons.unarmed_damage": "unarmed_strike_damage_type_and_die",
            "spell.alter_self.natural_weapons.attack_ability": "attack_and_damage_ability",
        },
    },
}
EXPECTED_CONTROL_TRANSITION_REQUIREMENTS: dict[str, dict[str, dict[str, str]]] = {
    "Elementalism": {},
    "Alter Self": {
        "spell.alter_self.control.switch_modes": {
            "spell.alter_self.switch.magic_action": "later_magic_action_switch",
            "spell.alter_self.switch.appearance_reselection": "appearance_reselection",
            "spell.alter_self.switch.concentration_persists": "concentration_persists",
        }
    },
}


def _validate_source_mode_mappings(
    manifest: Mapping[str, object], roster: tuple[Mapping[str, object], ...]
) -> dict[str, dict[str, object]]:
    contract = _object(
        manifest.get("source_mapping_contract"), "source_mapping_contract"
    )
    rows = [
        _object(value, f"source_mode_mappings[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_mode_mappings"), "source_mode_mappings")
        )
    ]
    by_name = {str(row.get("entry_name")): row for row in rows}
    expected_names = set(EXPECTED_MODE_REQUIREMENT_BRANCHES)
    contract_names = _strings(
        contract.get("summary_decomposition_entry_names"),
        "source_mapping_contract.summary_decomposition_entry_names",
    )
    if (
        len(by_name) != len(rows)
        or set(by_name) != expected_names
        or set(contract_names) != expected_names
        or len(contract_names) != len(expected_names)
        or contract.get("status") != "ALL_339_ENTRY_MAPS_SOURCE_CLOSURE_OPEN"
        or contract.get("source_entry_count") != 339
        or contract.get("candidate_entry_map_count") != 339
        or contract.get("lane_entry_counts")
        != {
            "source-pass-0-2": 139,
            "source-pass-3-5": 114,
            "source-pass-6-9": 84,
            "existing-summary-decompositions": 2,
        }
        or contract.get("unresolved_source_key_count") != 82
        or contract.get("unresolved_source_entry_count") != 72
        or contract.get("source_mapping_review_status") != "PENDING_INDEPENDENT_REVIEW"
        or contract.get("source_modeling_residual_count") != 1
        or contract.get("source_modeling_resolution_count") != 5
        or contract.get("source_unknown_classification_record_count") != 82
        or contract.get("source_blocking_unknown_key_count") != 77
        or contract.get("downstream_only_unknown_key_count") != 5
        or contract.get("mixed_unknown_key_count") != 28
        or contract.get("source_unknown_classification_status") != "ALL_82_CLASSIFIED"
        or contract.get("primary_table_evidence_residual_count") != 0
        or contract.get("summary_string_as_mode_policy") != "FORBIDDEN"
        or contract.get("inventory_dependency_labels_as_support_policy")
        != "NOT_SUPPORT_DOMAIN_MAPPINGS"
        or contract.get("source_support_obligation_status")
        != "PARTIAL_SOURCE_DESCRIPTORS_DOMAIN_CENSUS_NOT_ESTABLISHED"
        or contract.get("future_native_proof_status")
        != "NOT_ESTABLISHED_NOT_AN_SP00_SOURCE_READY_GATE"
        or contract.get("production_claim") != "NONE"
    ):
        _fail(
            "source_mode_mapping_contract", "the explicitly partial source map differs"
        )

    roster_by_name = {str(row.get("name")): row for row in roster}
    for name, mapping in by_name.items():
        roster_row = roster_by_name.get(name)
        if roster_row is None:
            _fail("source_mode_mapping_orphan", f"{name} is not in the source roster")
        source_ref = _object(
            mapping.get("source_record_ref"), f"{name}.source_record_ref"
        )
        pass_ref = _object(
            roster_row.get("source_pass_row_ref"), f"{name}.source_pass_row_ref"
        )
        expected_ref = {
            "artifact_id": pass_ref.get("artifact_id"),
            "asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "raw_record_name": pass_ref.get("raw_record_name"),
            "source_exact_name": name,
            "raw_body_sha256": pass_ref.get("raw_body_sha256"),
            "source_page": pass_ref.get("source_page"),
            "source_header_line": pass_ref.get("source_header_line"),
            "source_heading": name,
            "summary_field": "required_modes_or_exceptions",
            "summary_item_index": 0,
            "qualification_boundary": "SUMMARY_DECOMPOSITION_ONLY_NO_INDEPENDENT_BRANCH_OR_CONSUMER_PROOF",
        }
        if source_ref != expected_ref:
            _fail(
                "source_mode_mapping_witness",
                f"{name} mapping is not bound to its source row",
            )
        summaries = _strings(
            roster_row.get("source_requirement_summaries"),
            f"{name}.source_requirement_summaries",
        )
        if len(summaries) != 1:
            _fail(
                "source_mode_summary_ambiguous",
                f"{name} summary is not one directly indexed source-pass item",
            )
        if (
            mapping.get("mapping_status")
            != "EXPLICIT_SOURCE_SUMMARY_DECOMPOSITION_NOT_MACHINE_ADMISSION"
        ):
            _fail(
                "source_mode_mapping_status",
                f"{name} claims an unsupported mapping status",
            )
        if mapping.get("research_dependency_labels") != roster_row.get(
            "research_dependency_labels"
        ):
            _fail(
                "source_dependency_label_mismatch",
                f"{name} inventory dependency labels were changed or conflated",
            )
        if mapping.get("source_owner_obligation_summaries") != roster_row.get(
            "source_support_obligation_summaries"
        ):
            _fail(
                "source_owner_obligation_mismatch",
                f"{name} source-owner obligations differ from the retained source row",
            )
        if (
            mapping.get("support_domain_mappings") != []
            or mapping.get("support_domain_mapping_status") != "NOT_ESTABLISHED"
        ):
            _fail("source_support_overclaim", f"{name} claims a support-domain mapping")
        if (
            mapping.get("consumer_dependency_edges") != []
            or mapping.get("consumer_dependency_status") != "NOT_ESTABLISHED"
        ):
            _fail(
                "source_consumer_edge_overclaim",
                f"{name} claims consumer dependency closure",
            )

        expected_modes = EXPECTED_MODE_REQUIREMENT_BRANCHES[name]
        modes = [
            _object(value, f"{name}.modes[{index}]")
            for index, value in enumerate(_array(mapping.get("modes"), f"{name}.modes"))
        ]
        modes_by_name = {str(mode.get("mode_name")): mode for mode in modes}
        if len(modes_by_name) != len(modes) or set(modes_by_name) != set(
            expected_modes
        ):
            _fail("source_mode_set", f"{name} mode names omit or replace a source mode")
        seen_requirement_keys: set[str] = set()
        for mode_name, expected_requirements in expected_modes.items():
            mode = modes_by_name[mode_name]
            mode_key = f"spell.{_slug(name)}.mode.{mode_name}"
            if mode.get("mode_key") != mode_key:
                _fail("source_mode_key", f"{name} {mode_name} mode key differs")
            requirements = [
                _object(value, f"{name}.{mode_name}.requirements[{index}]")
                for index, value in enumerate(
                    _array(mode.get("requirements"), f"{name}.{mode_name}.requirements")
                )
            ]
            actual_requirements = {
                str(requirement.get("requirement_key")): requirement
                for requirement in requirements
            }
            if len(actual_requirements) != len(requirements) or set(
                actual_requirements
            ) != set(expected_requirements):
                _fail(
                    "source_requirement_set",
                    f"{name} {mode_name} requirements omit or replace a source branch",
                )
            for requirement_key, branch_key in expected_requirements.items():
                requirement = actual_requirements[requirement_key]
                if (
                    requirement.get("branch_key") != branch_key
                    or requirement.get("summary_item_index") != 0
                    or not isinstance(requirement.get("independent_statement"), str)
                    or not requirement["independent_statement"].strip()
                ):
                    _fail(
                        "source_requirement_witness",
                        f"{name} {requirement_key} lacks its explicit branch witness",
                    )
                seen_requirement_keys.add(requirement_key)

        expected_transitions = EXPECTED_CONTROL_TRANSITION_REQUIREMENTS[name]
        transitions = [
            _object(value, f"{name}.control_transitions[{index}]")
            for index, value in enumerate(
                _array(
                    mapping.get("control_transitions"), f"{name}.control_transitions"
                )
            )
        ]
        transitions_by_key = {
            str(transition.get("transition_key")): transition
            for transition in transitions
        }
        if len(transitions_by_key) != len(transitions) or set(
            transitions_by_key
        ) != set(expected_transitions):
            _fail("source_transition_set", f"{name} control transitions differ")
        for transition_key, expected_requirements in expected_transitions.items():
            transition = transitions_by_key[transition_key]
            requirements = [
                _object(value, f"{name}.{transition_key}.requirements[{index}]")
                for index, value in enumerate(
                    _array(
                        transition.get("requirements"),
                        f"{name}.{transition_key}.requirements",
                    )
                )
            ]
            actual_requirements = {
                str(requirement.get("requirement_key")): requirement
                for requirement in requirements
            }
            if len(actual_requirements) != len(requirements) or set(
                actual_requirements
            ) != set(expected_requirements):
                _fail(
                    "source_transition_requirement_set",
                    f"{name} {transition_key} requirements differ",
                )
            for requirement_key, branch_key in expected_requirements.items():
                requirement = actual_requirements[requirement_key]
                if (
                    requirement.get("branch_key") != branch_key
                    or requirement.get("summary_item_index") != 0
                    or not isinstance(requirement.get("independent_statement"), str)
                    or not requirement["independent_statement"].strip()
                ):
                    _fail(
                        "source_transition_witness",
                        f"{name} {requirement_key} lacks its explicit transition witness",
                    )
                seen_requirement_keys.add(requirement_key)
        if len(seen_requirement_keys) != sum(
            len(requirements) for requirements in expected_modes.values()
        ) + sum(len(requirements) for requirements in expected_transitions.values()):
            _fail("duplicate_source_key", f"{name} duplicates a source requirement key")
    return by_name


def _canonical_json_sha256(value: object) -> str:
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _source_mapping_lane_name(lane_id: str, row: Mapping[str, object]) -> str:
    field_by_lane = {
        "source-pass-0-2": "source_exact_name",
        "source-pass-3-5": "entry_name",
        "source-pass-6-9": "name",
    }
    field = field_by_lane.get(lane_id)
    if field is None:
        _fail("source_mapping_lane_id", f"unknown source mapping lane {lane_id}")
    return _string(row.get(field), f"{lane_id}.{field}")


def _source_mapping_lane_rows(
    lane: Mapping[str, object],
) -> list[dict[str, object]]:
    lane_id = _string(lane.get("lane_id"), "source_mapping_lane.lane_id")
    payload = _object(lane.get("mapping_payload"), f"{lane_id}.mapping_payload")
    return _rows(payload, "entries", lane_id)


def _source_mapping_lane_keys(
    lane_id: str, row: Mapping[str, object]
) -> tuple[
    list[str],
    list[str],
    list[str],
    list[dict[str, object]],
    list[str],
    list[str],
    list[str],
    list[str],
]:
    """Return authored mode/requirement/support keys and explicit unresolved rows."""
    mode_keys: list[str] = []
    requirement_keys: list[str] = []
    support_keys: list[str] = []
    unresolved: list[dict[str, object]] = []
    transition_keys: list[str] = []
    target_form_keys: list[str] = []
    common_requirement_keys: list[str] = []
    conditional_branch_keys: list[str] = []

    def add_requirement(key: object, path: str) -> None:
        requirement_keys.append(_string(key, path))

    def add_support(key: object, path: str) -> None:
        support_keys.append(_string(key, path))

    if lane_id == "source-pass-0-2":
        for group in (
            "common_requirements",
            "conditional_branches",
            "selectable_modes",
            "control_transitions",
            "target_forms",
            "support_domains",
        ):
            records = [
                _object(value, f"{lane_id}.{group}[{index}]")
                for index, value in enumerate(
                    _array(row.get(group), f"{lane_id}.{group}")
                )
            ]
            for index, record in enumerate(records):
                requirement_key = _string(
                    record.get("source_requirement_key"),
                    f"{lane_id}.{group}[{index}].source_requirement_key",
                )
                add_requirement(
                    requirement_key,
                    f"{lane_id}.{group}[{index}].source_requirement_key",
                )
                if group == "common_requirements":
                    common_requirement_keys.append(requirement_key)
                elif group in {
                    "conditional_branches",
                    "selectable_modes",
                    "control_transitions",
                    "target_forms",
                }:
                    conditional_branch_keys.append(requirement_key)
                if group == "selectable_modes":
                    mode_keys.append(
                        _string(
                            record.get("source_mode_key"),
                            f"{lane_id}.selectable_modes[{index}].source_mode_key",
                        )
                    )
                elif group == "control_transitions":
                    transition_keys.append(
                        _string(
                            record.get("source_transition_key"),
                            f"{lane_id}.control_transitions[{index}].source_transition_key",
                        )
                    )
                elif group == "target_forms":
                    target_form_keys.append(
                        _string(
                            record.get("source_target_form_key"),
                            f"{lane_id}.target_forms[{index}].source_target_form_key",
                        )
                    )
                elif group == "support_domains":
                    add_support(
                        record.get("source_support_domain_key"),
                        f"{lane_id}.support_domains[{index}].source_support_domain_key",
                    )
        unresolved = [
            {
                **_object(value, f"{lane_id}.unresolved_keys[{index}]"),
                "source_exact_name": row.get("source_exact_name"),
            }
            for index, value in enumerate(
                _array(row.get("unresolved_keys"), f"{lane_id}.unresolved_keys")
            )
        ]
    elif lane_id == "source-pass-3-5":
        modes = [
            _object(value, f"{lane_id}.modes[{index}]")
            for index, value in enumerate(_array(row.get("modes"), f"{lane_id}.modes"))
        ]
        for index, mode in enumerate(modes):
            mode_key = _string(
                mode.get("mode_key"), f"{lane_id}.modes[{index}].mode_key"
            )
            mode_keys.append(mode_key)
            for req_index, value in enumerate(
                _array(mode.get("requirements"), f"{lane_id}.{mode_key}.requirements")
            ):
                requirement = _object(
                    value, f"{lane_id}.{mode_key}.requirements[{req_index}]"
                )
                requirement_key = _string(
                    requirement.get("requirement_key"),
                    f"{lane_id}.{mode_key}.requirements[{req_index}].requirement_key",
                )
                add_requirement(
                    requirement_key,
                    f"{lane_id}.{mode_key}.requirements[{req_index}].requirement_key",
                )
                conditional_branch_keys.append(requirement_key)
                _object(
                    requirement.get("evidence_ref"),
                    f"{lane_id}.{mode_key}.requirements[{req_index}].evidence_ref",
                )
        for index, value in enumerate(
            _array(row.get("entry_requirements"), f"{lane_id}.entry_requirements")
        ):
            requirement = _object(value, f"{lane_id}.entry_requirements[{index}]")
            requirement_key = _string(
                requirement.get("requirement_key"),
                f"{lane_id}.entry_requirements[{index}].requirement_key",
            )
            add_requirement(
                requirement_key,
                f"{lane_id}.entry_requirements[{index}].requirement_key",
            )
            common_requirement_keys.append(requirement_key)
            _object(
                requirement.get("evidence_ref"),
                f"{lane_id}.entry_requirements[{index}].evidence_ref",
            )
        for index, value in enumerate(
            _array(
                row.get("support_domain_mappings"),
                f"{lane_id}.support_domain_mappings",
            )
        ):
            support = _object(value, f"{lane_id}.support_domain_mappings[{index}]")
            add_support(
                support.get("support_domain_key"),
                f"{lane_id}.support_domain_mappings[{index}].support_domain_key",
            )
            if (
                support.get("consumer_dependency_edges") != []
                or support.get("actual_proof_refs") != []
            ):
                _fail(
                    "source_map_future_proof_inflation",
                    f"{lane_id} support descriptor claims native closure",
                )
    elif lane_id == "source-pass-6-9":
        slug = _slug(_string(row.get("name"), f"{lane_id}.name"))
        shared = _object(row.get("shared") or {}, f"{lane_id}.shared")
        for shared_name, item_indexes in shared.items():
            requirement_key = f"spell.{slug}.common.{shared_name}"
            add_requirement(requirement_key, f"{lane_id}.shared.{shared_name}")
            common_requirement_keys.append(requirement_key)
            for item_index in _array(item_indexes, f"{lane_id}.shared.{shared_name}"):
                if type(item_index) is not int or item_index < 0:
                    _fail(
                        "source_map_reference", f"{lane_id} shared reference is invalid"
                    )
        modes = _object(row.get("modes") or {}, f"{lane_id}.modes")
        for mode_name, mode_value in modes.items():
            mode = _object(mode_value, f"{lane_id}.modes.{mode_name}")
            mode_key = f"spell.{slug}.mode.{mode_name}"
            mode_keys.append(mode_key)
            for branch_name, item_indexes in mode.items():
                requirement_key = f"spell.{slug}.{mode_name}.{branch_name}"
                add_requirement(
                    requirement_key, f"{lane_id}.modes.{mode_name}.{branch_name}"
                )
                conditional_branch_keys.append(requirement_key)
                for item_index in _array(
                    item_indexes,
                    f"{lane_id}.modes.{mode_name}.{branch_name}",
                ):
                    if type(item_index) is not int or item_index < 0:
                        _fail(
                            "source_map_reference",
                            f"{lane_id} mode source item index is invalid",
                        )
        consequences_value = row.get("nonduplication_consequences") or {}
        consequences = _object(
            consequences_value, f"{lane_id}.nonduplication_consequences"
        )
        for consequence_name, consequence_value in consequences.items():
            consequence = _object(
                consequence_value,
                f"{lane_id}.nonduplication_consequences.{consequence_name}",
            )
            for branch_name, item_indexes in consequence.items():
                requirement_key = (
                    f"spell.{slug}.nonduplication.{consequence_name}.{branch_name}"
                )
                add_requirement(
                    requirement_key,
                    f"{lane_id}.nonduplication_consequences.{consequence_name}.{branch_name}",
                )
                conditional_branch_keys.append(requirement_key)
                for item_index in _array(
                    item_indexes,
                    f"{lane_id}.nonduplication_consequences.{consequence_name}.{branch_name}",
                ):
                    if type(item_index) is not int or item_index < 0:
                        _fail(
                            "source_map_reference",
                            f"{lane_id} nonduplication source item index is invalid",
                        )
        support = _object(row.get("support") or {}, f"{lane_id}.support")
        for support_name, item_indexes in support.items():
            add_support(
                f"spell.{slug}.support.{support_name}",
                f"{lane_id}.support.{support_name}",
            )
            for item_index in _array(item_indexes, f"{lane_id}.support.{support_name}"):
                if type(item_index) is not int or item_index < 0:
                    _fail("source_map_reference", f"{lane_id} support index is invalid")
    else:
        _fail("source_mapping_lane_id", f"unknown source mapping lane {lane_id}")

    if len(mode_keys) != len(set(mode_keys)):
        _fail(
            "duplicate_source_mode_key",
            f"{lane_id} duplicates a mode or transition key",
        )
    if len(requirement_keys) != len(set(requirement_keys)):
        _fail(
            "duplicate_source_requirement_key",
            f"{lane_id} duplicates a requirement key",
        )
    if len(support_keys) != len(set(support_keys)):
        _fail(
            "duplicate_source_support_key",
            f"{lane_id} duplicates a support descriptor key",
        )
    return (
        mode_keys,
        requirement_keys,
        support_keys,
        unresolved,
        transition_keys,
        target_form_keys,
        common_requirement_keys,
        conditional_branch_keys,
    )


L35_RECIPE_HOLD = (
    "Actual numeric and parameter recipes need source-bound materialization; "
    "frozen body review is retained, not repeated."
)
L35_O9_SOURCE_GAP_NAMES = {
    "Animate Objects",
    "Antilife Shell",
    "Fireball",
    "Giant Insect",
    "Raise Dead",
    "Scrying",
    "Slow",
    "Telekinesis",
}
L35_FUTURE_RECIPE_PHASE_BY_LEVEL = {3: "SP20", 4: "SP21", 5: "SP22"}
L35_O9_QUALIFICATION = (
    "Source reconstruction must correct displaced blocks/continuations, exclude "
    "foreign tails, preserve Unicode-minus signed values and verify the truncated "
    "licensed continuation before recipe admission."
)


def _source_recipe_materialization_residuals(
    manifest: Mapping[str, object],
) -> list[dict[str, object]]:
    """Classify each generic recipe hold by its item-level source evidence."""
    lane35 = next(
        lane
        for lane in _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        if isinstance(lane, dict) and lane.get("lane_id") == "source-pass-3-5"
    )
    lane35_payload = _object(
        lane35.get("mapping_payload"), "source-pass-3-5.mapping_payload"
    )
    rows = _rows(lane35_payload, "entries", "source-pass-3-5")
    classifications: list[dict[str, object]] = []
    source_gap_names: set[str] = set()
    seen_names: set[str] = set()
    for row in rows:
        name = _string(row.get("entry_name"), "source-pass-3-5.entry_name")
        if name in seen_names:
            _fail("source_recipe_materialization", f"duplicate source-map entry {name}")
        seen_names.add(name)
        residuals = _strings(row.get("residuals"), f"{name}.source_mapping_residuals")
        if residuals.count(L35_RECIPE_HOLD) != 1:
            _fail(
                "source_recipe_materialization",
                f"{name} no longer has exactly one retained generic recipe hold",
            )
        source_ref = _object(row.get("source_record_ref"), f"{name}.source_record_ref")
        pass_ref = _object(source_ref.get("source_pass"), f"{name}.source_pass_ref")
        primary_ref = _object(source_ref.get("primary"), f"{name}.primary_source_ref")
        source_obligation_resolutions = [
            _object(value, f"{name}.source_obligation_resolutions[{index}]")
            for index, value in enumerate(
                _array(
                    row.get("source_obligation_resolutions"),
                    f"{name}.source_obligation_resolutions",
                )
            )
        ]
        o9_resolutions = [
            resolution
            for resolution in source_obligation_resolutions
            if resolution.get("resolution_table_key") == "L35-O9"
        ]
        if len(o9_resolutions) > 1:
            _fail(
                "source_recipe_materialization",
                f"{name} duplicates the L35-O9 source reconstruction finding",
            )
        source_gap = bool(o9_resolutions)
        source_finding = None
        if source_gap:
            resolution = o9_resolutions[0]
            finding = _object(resolution.get("finding"), f"{name}.L35-O9.finding")
            exact_resolution = _object(
                resolution.get("exact_resolution"), f"{name}.L35-O9.exact_resolution"
            )
            witnesses = _strings(finding.get("witnesses"), "L35-O9.witnesses")
            if (
                finding.get("id") != "L35-O9"
                or set(witnesses) != L35_O9_SOURCE_GAP_NAMES
                or finding.get("qualification") != L35_O9_QUALIFICATION
                or name not in witnesses
                or resolution.get("resolution_artifact_id")
                != "source-obligation-resolution"
                or exact_resolution.get("artifact_id") != "source-obligation-resolution"
                or exact_resolution.get("line") != 23
                or resolution.get("disposition")
                != "RETAIN_EXACT_RESOLVER_QUALIFICATION_AND_BEFORE_ADMISSION_PROOF_TRIGGER"
            ):
                _fail(
                    "source_recipe_materialization_source_gap",
                    f"{name} lacks the exact named L35-O9 source-gap witness",
                )
            source_gap_names.add(name)
            source_finding = {
                "finding_id": "L35-O9",
                "artifact_id": "source-obligation-resolution",
                "line": 23,
                "source_finding": exact_resolution.get("source_finding"),
                "qualification": finding.get("qualification"),
                "future_proof_trigger": exact_resolution.get(
                    "exact_resolution_and_future_proof_trigger"
                ),
            }
        level = row.get("level")
        if type(level) is not int or level not in L35_FUTURE_RECIPE_PHASE_BY_LEVEL:
            _fail(
                "source_recipe_materialization_level",
                f"{name} has no stable level-owner recipe phase",
            )
        classification = {
            "source_exact_name": name,
            "source_record_ref": {
                "artifact_id": pass_ref.get("artifact_id"),
                "record_pointer": pass_ref.get("record_pointer"),
                "exact_name": pass_ref.get("exact_name"),
                "asset_id": primary_ref.get("asset_id"),
                "printed_page": primary_ref.get("printed_page"),
                "source_header_line": primary_ref.get("source_header_line"),
                "raw_body_sha256": source_ref.get("raw_body_sha256"),
            },
            "original_generic_recipe_hold": L35_RECIPE_HOLD,
            "source_obligation_resolution_keys": [
                str(resolution.get("resolution_table_key"))
                for resolution in source_obligation_resolutions
            ],
            "classification": (
                "SOURCE_RECONSTRUCTION_GAP"
                if source_gap
                else "FUTURE_EXECUTABLE_RECIPE"
            ),
            "source_finding_id": "L35-O9" if source_gap else None,
            "source_finding_ref": source_finding,
            "future_recipe_phase": (
                None if source_gap else L35_FUTURE_RECIPE_PHASE_BY_LEVEL[level]
            ),
            "status": "NOT_ESTABLISHED",
            "blocks_sp00_source_ready": source_gap,
        }
        classifications.append(classification)
    if (
        len(rows) != 114
        or len(seen_names) != 114
        or source_gap_names != L35_O9_SOURCE_GAP_NAMES
    ):
        _fail(
            "source_mapping_lane_residuals",
            "114 recipe holds or the exact eight L35-O9 source gaps differ",
        )
    return classifications


TELEPORT_TABLE_INTERVALS: dict[str, dict[str, tuple[int, int] | None]] = {
    "Permanent circle": {
        "mishap": None,
        "similar_area": None,
        "off_target": None,
        "on_target": (1, 100),
    },
    "Linked object": {
        "mishap": None,
        "similar_area": None,
        "off_target": None,
        "on_target": (1, 100),
    },
    "Very familiar": {
        "mishap": (1, 5),
        "similar_area": (6, 13),
        "off_target": (14, 24),
        "on_target": (25, 100),
    },
    "Seen casually": {
        "mishap": (1, 33),
        "similar_area": (34, 43),
        "off_target": (44, 53),
        "on_target": (54, 100),
    },
    "Viewed once or described": {
        "mishap": (1, 43),
        "similar_area": (44, 53),
        "off_target": (54, 73),
        "on_target": (74, 100),
    },
    "False destination": {
        "mishap": (1, 50),
        "similar_area": (51, 100),
        "off_target": None,
        "on_target": None,
    },
}
TELEPORT_ROW_SLUGS = {
    "Permanent circle": "permanent_circle",
    "Linked object": "linked_object",
    "Very familiar": "very_familiar",
    "Seen casually": "seen_casually",
    "Viewed once or described": "viewed_once_or_described",
    "False destination": "false_destination",
}
WEATHER_TABLE_CONDITIONS = {
    "precipitation": [
        "Clear",
        "Light clouds",
        "Overcast or ground fog",
        "Rain, hail, or snow",
        "Torrential rain, driving hail, or blizzard",
    ],
    "temperature": ["Heat wave", "Hot", "Warm", "Cool", "Cold", "Freezing"],
    "wind": ["Calm", "Moderate wind", "Strong wind", "Gale", "Storm"],
}


def _validate_primary_table_evidence_witnesses(
    manifest: Mapping[str, object],
) -> list[dict[str, object]]:
    """Validate only the two visually witnessed source tables, never native proof."""
    witnesses = [
        _object(value, f"primary_table_evidence_witnesses[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("primary_table_evidence_witnesses"),
                "primary_table_evidence_witnesses",
            )
        )
    ]
    if len(witnesses) != 2:
        _fail(
            "primary_table_witness_census", "exactly two table witnesses are required"
        )
    by_name: dict[str, dict[str, object]] = {}
    for witness in witnesses:
        name = _string(
            witness.get("source_exact_name"), "primary_table_witness.source_exact_name"
        )
        if name in by_name or name not in {"Teleport", "Control Weather"}:
            _fail(
                "primary_table_witness_census", f"unexpected or duplicate table {name}"
            )
        by_name[name] = witness

    evidence = _load_evidence(manifest)
    source_payload = _object(evidence.get("source-pass-6-9"), "source-pass-6-9")
    source_rows = _rows(source_payload, "rows", "source-pass-6-9")
    body_payload = _object(
        evidence.get("source-body-witnesses"), "source-body-witnesses"
    )
    english_assets = [
        _object(value, f"source_assets[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_assets"), "source_assets")
        )
        if isinstance(value, dict) and value.get("asset_id") == "srd52_en"
    ]
    pass_artifact = next(
        (
            _object(value, "evidence_artifacts[]")
            for value in _array(
                manifest.get("evidence_artifacts"), "evidence_artifacts"
            )
            if isinstance(value, dict) and value.get("artifact_id") == "source-pass-6-9"
        ),
        None,
    )
    if len(english_assets) != 1 or pass_artifact is None:
        _fail(
            "primary_table_witness_provenance",
            "one pinned English source asset and source pass are required",
        )
    asset_sha256 = english_assets[0].get("sha256")
    source_pass_sha256 = pass_artifact.get("sha256")
    proof_sha256 = "c5ee7e0af314c45179addeb763e95afc90ab315a67107495da2d2183279febc4"
    subset_sha256 = "b78eb3ba8663c49adce515749e8fb8bc0cac39792e4aadd5ab337078556f1a36"
    captured_candidate_sha = "9d040f4ee70a063f29a709c063908d3f66315257"
    captured_fixture_sha256 = (
        "13d60dff16a92b700763b031945aaf6b3cb8d6a4c05ad2cdff0e04242b19dde3"
    )
    subset_page_mapping = {"1": 120, "2": 168, "3": 169}
    expected_records = {
        "Teleport": {
            "record_index": 50,
            "page": 168,
            "header": 14887,
            "body_sha256": "c532020059ac049d17f8710ca57d77ec2c9f57862236a5c216c6403c06ec411c",
            "body_witness_pointer": "/rows/306",
            "subset_page": 2,
        },
        "Control Weather": {
            "record_index": 56,
            "page": 120,
            "header": 10284,
            "body_sha256": "1464ca06b0734ab127cce02dfda0f9fea2c1b64006fb9e869fd2a1e2b6d77313",
            "body_witness_pointer": "/rows/66",
            "subset_page": 1,
        },
    }
    for name, witness in by_name.items():
        expected = expected_records[name]
        if (
            witness.get("status") != "PRIMARY_TABLE_EVIDENCE_VERIFIED_SOURCE_ONLY"
            or witness.get("machine_execution_proof_status") != "NOT_ESTABLISHED"
        ):
            _fail(
                "primary_table_witness_scope",
                f"{name} table witness must not imply machine or native execution proof",
            )
        source_ref = _object(witness.get("source_pass_ref"), f"{name}.source_pass_ref")
        record_index = int(expected["record_index"])
        source_row = source_rows[record_index]
        expected_source_ref = {
            "artifact_id": "source-pass-6-9",
            "record_index": record_index,
            "json_pointer": f"/rows/{record_index}",
            "source_exact_name": name,
            "asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": expected["page"],
            "source_header_line": expected["header"],
            "raw_body_sha256": expected["body_sha256"],
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": expected["body_witness_pointer"],
            },
        }
        body_row = _object(
            _resolve_json_pointer(
                body_payload,
                str(expected["body_witness_pointer"]),
                f"{name}.body_witness_ref",
            ),
            f"{name}.body_witness",
        )
        if (
            source_ref != expected_source_ref
            or source_row.get("name") != name
            or source_row.get("source_exact_name", name) != name
            or source_row.get("source_page") != expected["page"]
            or source_row.get("source_header_line") != expected["header"]
            or source_row.get("body_sha256") != expected["body_sha256"]
            or body_row.get("name") != name
            or body_row.get("page") != expected["page"]
            or body_row.get("line") != expected["header"]
            or body_row.get("body_sha256") != expected["body_sha256"]
        ):
            _fail(
                "primary_table_witness_source_ref",
                f"{name} table proof is not bound to its exact source record/body",
            )
        provenance = _object(
            witness.get("visual_provenance"), f"{name}.visual_provenance"
        )
        expected_provenance = {
            "source_asset_sha256": asset_sha256,
            "source_pass_sha256": source_pass_sha256,
            "witness_sha256": proof_sha256,
            "subset_sha256": subset_sha256,
            "captured_candidate_sha": captured_candidate_sha,
            "captured_source_fixture_sha256": captured_fixture_sha256,
            "visual_inspection_status": "NATIVE_PAGE_IMAGES_VISUALLY_INSPECTED",
            "subset_creation_tool": "pypdf 6.19.0",
            "secondary_text_role": "CODEPOINT_COUNTS_ONLY_NOT_VISUAL_SUBSTITUTE",
            "subset_page_mapping": subset_page_mapping,
            "unqualified_subset_page": {
                "subset_page": 3,
                "asset_page": 169,
                "qualified": False,
                "reason": "Unneeded adjacent boundary page; no obligations or claims qualified from it.",
            },
        }
        if provenance != expected_provenance:
            _fail(
                "primary_table_witness_provenance",
                f"{name} witness no longer matches the independently asset-bound visual record",
            )
        if (
            witness.get("asset_page") != expected["page"]
            or witness.get("subset_page") != expected["subset_page"]
        ):
            _fail(
                "primary_table_witness_source_locator",
                f"{name} visual page locator differs from the pinned subset map",
            )

    teleport = by_name["Teleport"]
    cells = [
        _object(value, f"Teleport.outcome_cells[{index}]")
        for index, value in enumerate(
            _array(teleport.get("outcome_cells"), "Teleport.outcome_cells")
        )
    ]
    cells_by_key: dict[str, dict[str, object]] = {}
    row_intervals: dict[str, list[tuple[int, int]]] = {
        label: [] for label in TELEPORT_TABLE_INTERVALS
    }
    for cell in cells:
        cell_key = _string(cell.get("cell_key"), "Teleport.cell_key")
        if cell_key in cells_by_key:
            _fail("primary_table_cell_census", f"duplicate Teleport cell {cell_key}")
        row_label = _string(cell.get("row_label"), f"{cell_key}.row_label")
        outcome = _string(cell.get("outcome"), f"{cell_key}.outcome")
        expected_row = TELEPORT_TABLE_INTERVALS.get(row_label)
        expected_interval = (
            expected_row.get(outcome) if expected_row is not None else None
        )
        expected_key = (
            f"teleport.{TELEPORT_ROW_SLUGS.get(row_label, 'unknown')}.{outcome}"
        )
        literal = _string(cell.get("literal"), f"{cell_key}.literal")
        interval_value = cell.get("normalized_interval")
        if (
            expected_row is None
            or outcome not in expected_row
            or cell_key != expected_key
            or cell.get("visual_locator")
            != "asset p168 / subset p2 / lower-left Teleportation Outcome"
        ):
            _fail(
                "primary_table_cell_identity",
                f"Teleport cell {cell_key} has a wrong row/outcome/locator",
            )
        if expected_interval is None:
            if literal != "—" or interval_value is not None:
                _fail(
                    "primary_table_cell_value",
                    f"{cell_key} must retain its unavailable em-dash cell",
                )
        else:
            match = re.fullmatch(r"(\d{2})–(\d{2})", literal)
            if match is None:
                _fail(
                    "primary_table_cell_unicode",
                    f"{cell_key} must use a literal en-dash range",
                )
            start = int(match.group(1))
            raw_end = int(match.group(2))
            normalized = (start, 100 if raw_end == 0 else raw_end)
            if interval_value != [normalized[0], normalized[1]]:
                _fail(
                    "primary_table_cell_value",
                    f"{cell_key} literal/range differs from the witnessed cell",
                )
            row_intervals[row_label].append(normalized)
        cells_by_key[cell_key] = cell
    expected_cell_keys = {
        f"teleport.{TELEPORT_ROW_SLUGS[row_label]}.{outcome}"
        for row_label, outcomes in TELEPORT_TABLE_INTERVALS.items()
        for outcome in outcomes
    }
    if len(cells) != 24 or set(cells_by_key) != expected_cell_keys:
        _fail(
            "primary_table_cell_census",
            "Teleport must preserve all 24 exact outcome cells",
        )
    for row_label, intervals in row_intervals.items():
        intervals.sort()
        cursor = 1
        for start, end in intervals:
            if start != cursor or end < start:
                _fail(
                    "primary_table_range_partition",
                    f"Teleport {row_label} ranges overlap or leave a gap",
                )
            cursor = end + 1
        if cursor != 101:
            _fail(
                "primary_table_range_partition",
                f"Teleport {row_label} ranges do not partition 1–100",
            )
    for row_label, expected_outcomes in TELEPORT_TABLE_INTERVALS.items():
        for outcome, expected_interval in expected_outcomes.items():
            cell = cells_by_key[f"teleport.{TELEPORT_ROW_SLUGS[row_label]}.{outcome}"]
            expected_pair = (
                None
                if expected_interval is None
                else [int(expected_interval[0]), int(expected_interval[1])]
            )
            if cell.get("normalized_interval") != expected_pair:
                _fail(
                    "primary_table_cell_value",
                    f"{cell['cell_key']} differs from the pinned primary-table cell",
                )
    if (
        sum(cell["literal"].count("—") for cell in cells) != 8
        or sum(cell["literal"].count("–") for cell in cells) != 16
        or sum(cell["literal"].count("−") for cell in cells) != 0
    ):
        _fail(
            "primary_table_unicode",
            "Teleport dash glyphs differ from the visual witness",
        )
    if teleport.get("unicode_profile") != {
        "u2014_em_dash_count": 8,
        "u2013_en_dash_count": 16,
        "u2212_minus_count": 0,
    }:
        _fail("primary_table_unicode", "Teleport Unicode census differs")
    if teleport.get("normalization") != {
        "literal_00_retained": True,
        "normalized_upper_bound": 100,
        "qualification_ref": "/rows/50/qualifications/0",
        "general_d100_primary_rule_verified": False,
    }:
        _fail(
            "primary_table_normalization",
            "Teleport's literal 00 normalization must retain its existing qualification only",
        )
    familiarity_conditions = [
        _object(value, f"Teleport.familiarity_conditions[{index}]")
        for index, value in enumerate(
            _array(
                teleport.get("familiarity_conditions"),
                "Teleport.familiarity_conditions",
            )
        )
    ]
    expected_familiarity_conditions = {
        "Permanent circle": (
            "right column Familiarity bullet 1",
            "Permanent teleportation circle whose sigil sequence the caster knows.",
            None,
        ),
        "Linked object": (
            "right column Familiarity bullet 2",
            "Caster possesses an object taken from the desired destination within the last six months.",
            "Possession and destination provenance/age both apply; mere knowledge of an object is insufficient.",
        ),
        "Very familiar": (
            "right column Familiarity bullet 3",
            "Place visited often, carefully studied, or visible when casting.",
            None,
        ),
        "Seen casually": (
            "right column Familiarity bullet 4",
            "Place seen more than once but not very familiar.",
            None,
        ),
        "Viewed once or described": (
            "right column Familiarity bullet 5",
            "Place seen once, possibly magically, or known from another person’s description, perhaps a map.",
            None,
        ),
        "False destination": (
            "right column Familiarity bullet 6",
            "Place does not exist, such as a scryed illusion or location that no longer exists.",
            "Only Mishap or Similar Area cells apply; no ordinary Off Target or On Target outcome.",
        ),
    }
    if (
        len(familiarity_conditions) != 6
        or {row.get("row_label") for row in familiarity_conditions}
        != set(TELEPORT_TABLE_INTERVALS)
        or any(
            (
                row.get("location"),
                row.get("condition_paraphrase"),
                row.get("qualification"),
            )
            != expected_familiarity_conditions[row["row_label"]]
            for row in familiarity_conditions
        )
    ):
        _fail(
            "primary_table_familiarity_census",
            "Teleport must preserve all six qualified familiarity conditions",
        )
    outcome_explanations = [
        _object(value, f"Teleport.outcome_explanations[{index}]")
        for index, value in enumerate(
            _array(
                teleport.get("outcome_explanations"), "Teleport.outcome_explanations"
            )
        )
    ]
    expected_outcome_explanations = {
        "teleport.mishap.explanation": (
            "right column Mishap",
            "Each teleporting creature or target object takes 3d10 Force damage and the GM rerolls the table; multiple mishaps can occur, dealing damage each time.",
            "The source supplies no repeat cap; this establishes source semantics only, not RNG/cursor implementation.",
        ),
        "teleport.similar_area.explanation": (
            "right column Similar Area",
            "The group or target object appears in a different visually or thematically similar area, at the closest similar place.",
            None,
        ),
        "teleport.off_target.explanation": (
            "right column Off Target",
            "The group or target object appears 2d12 miles away in a random direction; d8 maps 1 east, 2 southeast, 3 south, 4 southwest, 5 west, 6 northwest, 7 north, 8 northeast.",
            None,
        ),
        "teleport.on_target.explanation": (
            "right column On Target",
            "The group or target object appears where intended.",
            None,
        ),
    }
    if (
        len(outcome_explanations) != 4
        or {row.get("clause_key") for row in outcome_explanations}
        != set(expected_outcome_explanations)
        or any(
            (
                row.get("location"),
                row.get("evidence_clause_paraphrase"),
                row.get("qualification"),
            )
            != expected_outcome_explanations[row["clause_key"]]
            for row in outcome_explanations
        )
    ):
        _fail(
            "primary_table_explanation_census",
            "Teleport's four outcome explanations differ",
        )

    weather = by_name["Control Weather"]
    stage_rows = [
        _object(value, f"Control Weather.stage_rows[{index}]")
        for index, value in enumerate(
            _array(weather.get("stage_rows"), "Control Weather.stage_rows")
        )
    ]
    expected_stage_keys = {
        (table, stage, condition)
        for table, conditions in WEATHER_TABLE_CONDITIONS.items()
        for stage, condition in enumerate(conditions, 1)
    }
    observed_stage_keys: set[tuple[str, int, str]] = set()
    stage_cell_keys: set[str] = set()
    for row in stage_rows:
        table = _string(row.get("table"), "Control Weather.stage.table")
        stage = row.get("stage")
        condition = _string(
            row.get("condition_literal"), "Control Weather.stage.condition_literal"
        )
        cell_key = _string(row.get("cell_key"), "Control Weather.stage.cell_key")
        stage_key = _string(
            row.get("stage_cell_key"), "Control Weather.stage.stage_cell_key"
        )
        condition_key = _string(
            row.get("condition_cell_key"), "Control Weather.stage.condition_cell_key"
        )
        expected_key = f"control_weather.{table}.{stage}"
        if (
            type(stage) is not int
            or (table, stage, condition) not in expected_stage_keys
            or cell_key != expected_key
            or stage_key != f"{expected_key}.stage"
            or condition_key != f"{expected_key}.condition"
            or cell_key in stage_cell_keys
        ):
            _fail(
                "primary_table_weather_stage",
                f"Control Weather stage {cell_key} is duplicated or wrong",
            )
        observed_stage_keys.add((table, stage, condition))
        stage_cell_keys.add(cell_key)
    if (
        len(stage_rows) != 16
        or observed_stage_keys != expected_stage_keys
        or len(stage_cell_keys) != 16
        or weather.get("stage_cell_count") != 32
    ):
        _fail(
            "primary_table_weather_stage_census",
            "Control Weather must preserve all 16 stage rows/32 cells",
        )
    transition_clauses = [
        _object(value, f"Control Weather.transition_clauses[{index}]")
        for index, value in enumerate(
            _array(
                weather.get("transition_clauses"), "Control Weather.transition_clauses"
            )
        )
    ]
    expected_transition_clauses = {
        "control_weather.transition": (
            "right column top, before tables",
            "Find a current condition on the tables and change its stage by one, up or down; wind direction may also change.",
            "Stages are the listed bounded sets, not arbitrary numeric weather values; no unlisted stage or invented wraparound.",
        ),
        "control_weather.current_and_end": (
            "left column own body and right column top",
            "GM determines current weather; caster must be outdoors; going indoors ends the spell early; weather gradually returns to normal when it ends.",
            "No fixed normalization rate is given in the inspected body.",
        ),
        "control_weather.delay": (
            "left column final lines continuing at right-column top",
            "New conditions take 1d4 × 10 minutes to take effect; only after they take effect can conditions change again.",
            "Multiplication is preserved; no subtraction, replacement glyph, or fixed ten-minute delay.",
        ),
    }
    if (
        len(transition_clauses) != 3
        or {row.get("clause_key") for row in transition_clauses}
        != set(expected_transition_clauses)
        or any(
            (
                row.get("location"),
                row.get("evidence_clause_paraphrase"),
                row.get("qualification"),
            )
            != expected_transition_clauses[row["clause_key"]]
            for row in transition_clauses
        )
        or weather.get("transition_formula") != "1d4 × 10 minutes"
        or "×" not in str(weather.get("transition_formula"))
        or "−" in str(weather.get("transition_formula"))
        or weather.get("unicode_profile")
        != {"u00d7_multiplication_count": 1, "u2212_minus_count": 0}
    ):
        _fail(
            "primary_table_weather_transition",
            "Control Weather transition qualifiers/Unicode differ from the visual witness",
        )
    if _array(
        manifest.get("primary_table_evidence_residuals"),
        "primary_table_evidence_residuals",
    ):
        _fail(
            "primary_table_residual",
            "verified table witnesses must clear both current table residuals",
        )
    lane6 = next(
        lane
        for lane in _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        if isinstance(lane, dict) and lane.get("lane_id") == "source-pass-6-9"
    )
    lane6_payload = _object(
        lane6.get("mapping_payload"), "source-pass-6-9.mapping_payload"
    )
    lane6_receipt = _object(
        lane6.get("receipt_summary"), "source-pass-6-9.receipt_summary"
    )
    if (
        lane6_payload.get("primary_table_evidence_residuals") != []
        or lane6_receipt.get("primary_table_evidence_residuals") != []
    ):
        _fail(
            "primary_table_residual",
            "source-pass 6-9 payload and receipt must no longer carry these two current residuals",
        )
    return witnesses


def _validate_source_mapping_lane_totals(
    lane_id: str,
    lane: Mapping[str, object],
    payload: Mapping[str, object],
    rows: list[dict[str, object]],
) -> None:
    receipt = _object(lane.get("receipt_summary"), f"{lane_id}.receipt_summary")
    if lane_id == "source-pass-0-2":
        counts = _object(payload.get("counts"), f"{lane_id}.counts")
        expected = {
            "entries": 139,
            "shared_common_requirements": 16,
            "common_requirements": 282,
            "conditional_branches": 209,
            "selectable_modes": 58,
            "control_transitions": 80,
            "target_forms": 31,
            "support_domains": 12,
            "semantic_requirements": 672,
            "explicit_unresolved_keys": 82,
            "entries_with_explicit_residuals": 72,
        }
        if any(counts.get(key) != value for key, value in expected.items()):
            _fail("source_mapping_lane_totals", "source-pass 0-2 map totals differ")
        if _object(receipt.get("counts"), f"{lane_id}.receipt_counts") != counts:
            _fail("source_mapping_lane_totals", "source-pass 0-2 receipt totals differ")
        return

    if lane_id == "source-pass-3-5":
        scope = _object(payload.get("scope"), f"{lane_id}.scope")
        coverage = _object(receipt.get("coverage"), f"{lane_id}.receipt.coverage")
        mode_count = 0
        mode_requirement_count = 0
        entry_requirement_count = 0
        support_count = 0
        for row in rows:
            modes = [
                _object(value, f"{row['entry_name']}.modes[{index}]")
                for index, value in enumerate(
                    _array(row.get("modes"), f"{row['entry_name']}.modes")
                )
            ]
            mode_count += len(modes)
            mode_requirement_count += sum(
                len(
                    _array(
                        mode.get("requirements"), f"{row['entry_name']}.requirements"
                    )
                )
                for mode in modes
            )
            entry_requirement_count += len(
                _array(
                    row.get("entry_requirements"),
                    f"{row['entry_name']}.entry_requirements",
                )
            )
            support_count += len(
                _array(
                    row.get("support_domain_mappings"),
                    f"{row['entry_name']}.support_domain_mappings",
                )
            )
        if (
            scope.get("entries") != 114
            or coverage.get("explicit_modes") != mode_count
            or coverage.get("individual_mode_requirements") != mode_requirement_count
            or coverage.get("individual_support_domain_obligations") != support_count
            or mode_count != 308
            or mode_requirement_count != 744
            or support_count != 447
        ):
            _fail(
                "source_mapping_lane_totals",
                "source-pass 3-5 mode/support totals differ",
            )
        return

    if lane_id == "source-pass-6-9":
        scope = _object(payload.get("scope"), f"{lane_id}.scope")
        mode_count = 0
        requirement_count = 0
        support_count = 0
        for row in rows:
            modes = _object(row.get("modes") or {}, f"{row['name']}.modes")
            mode_count += len(modes)
            shared = _object(row.get("shared") or {}, f"{row['name']}.shared")
            requirement_count += len(shared)
            for mode_name, mode_value in modes.items():
                mode = _object(mode_value, f"{row['name']}.modes.{mode_name}")
                requirement_count += len(mode)
            consequences = _object(
                row.get("nonduplication_consequences") or {},
                f"{row['name']}.nonduplication_consequences",
            )
            for consequence_name, consequence_value in consequences.items():
                requirement_count += len(
                    _object(
                        consequence_value,
                        f"{row['name']}.nonduplication_consequences.{consequence_name}",
                    )
                )
            support_count += len(
                _object(row.get("support") or {}, f"{row['name']}.support")
            )
        if (
            scope.get("unique_names") != 84
            or scope.get("by_level") != {"6": 31, "7": 20, "8": 17, "9": 16}
            or mode_count != 264
            or requirement_count != 643
            or support_count != 403
        ):
            _fail(
                "source_mapping_lane_totals",
                "source-pass 6-9 mode/branch/support totals differ",
            )
        return
    _fail("source_mapping_lane_id", f"unknown source mapping lane {lane_id}")


def _validate_source_mapping_lanes(
    manifest: Mapping[str, object],
    roster: tuple[Mapping[str, object], ...],
    evidence: Mapping[str, object] | None = None,
) -> dict[str, dict[str, object]]:
    lanes = [
        _object(value, f"source_mapping_lanes[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        )
    ]
    if [lane.get("lane_id") for lane in lanes] != list(
        SOURCE_MAPPING_LANE_EXPECTATIONS
    ):
        _fail(
            "source_mapping_lane_set",
            "the three disjoint source-pass map lanes are absent, duplicated, or reordered",
        )
    inventory_names = {str(row["name"]) for row in roster}
    summary_names = {"Alter Self", "Elementalism"}
    roster_by_name = {str(row["name"]): row for row in roster}
    pass_payloads: dict[str, dict[str, object]] = {}
    if evidence is None:
        evidence = _load_evidence(manifest)
    for artifact_id in SOURCE_MAPPING_LANE_EXPECTATIONS:
        pass_payloads[artifact_id] = _object(evidence.get(artifact_id), artifact_id)
    inventory_payload = _object(evidence.get("spell-inventory"), "spell-inventory")
    matrix_payload = _object(evidence.get("requirement-matrix"), "requirement-matrix")
    body_payload = _object(
        evidence.get("source-body-witnesses"), "source-body-witnesses"
    )

    lane_names: dict[str, set[str]] = {}
    map_index: dict[str, dict[str, object]] = {}
    lane_counts: dict[str, int] = {}
    all_requirement_keys: set[str] = set()
    all_mode_keys: set[str] = set()
    all_support_keys: set[str] = set()
    all_unresolved_keys: set[str] = set()
    for lane in lanes:
        lane_id = _string(lane.get("lane_id"), "source_mapping_lane.lane_id")
        expected = SOURCE_MAPPING_LANE_EXPECTATIONS[lane_id]
        if (
            lane.get("map_artifact_sha256") != expected["map_sha256"]
            or lane.get("receipt_artifact_sha256") != expected["receipt_sha256"]
            or lane.get("source_pass_artifact_id") != lane_id
            or lane.get("source_pass_sha256") != expected["source_pass_sha256"]
            or lane.get("source_entry_count") != expected["entry_count"]
            or lane.get("independent_review_status") != "PENDING"
        ):
            _fail("source_mapping_lane_identity", f"{lane_id} lane receipt differs")
        payload = _object(lane.get("mapping_payload"), f"{lane_id}.mapping_payload")
        observed_payload_sha256 = _canonical_json_sha256(payload)
        if (
            observed_payload_sha256 != lane.get("mapping_payload_sha256")
            or observed_payload_sha256 != expected["mapping_payload_sha256"]
        ):
            _fail(
                "source_mapping_lane_digest",
                f"{lane_id} embedded mapping payload differs from its pinned bytes identity",
            )
        expected_payload_status = {
            "source-pass-0-2": "SCRATCH_COORDINATOR_INPUT_NOT_ADMISSION",
            "source-pass-3-5": "SCRATCH_ONLY_BOUNDED_SOURCE_EVIDENCE_CANDIDATE",
            "source-pass-6-9": "BOUNDED_SOURCE_EVIDENCE_NOT_IMPORT_OR_SUPPORT_ADMISSION",
        }[lane_id]
        if payload.get("status") != expected_payload_status:
            _fail(
                "source_mapping_lane_status",
                f"{lane_id} no longer identifies a non-admission map",
            )
        if lane_id in {"source-pass-0-2", "source-pass-3-5"}:
            inherited_assets = payload.get(
                "inherited_source_assets", payload.get("source_assets_inherited")
            )
            if inherited_assets != _array(
                manifest.get("source_assets"), "source_assets"
            ):
                _fail(
                    "source_mapping_asset_registry", f"{lane_id} asset registry differs"
                )
        else:
            map_assets = _object(
                payload.get("evidence_artifacts"),
                "source-pass-6-9.evidence_artifacts",
            )
            english_asset_hash = next(
                asset["sha256"]
                for asset in _array(manifest.get("source_assets"), "source_assets")
                if isinstance(asset, dict) and asset.get("asset_id") == "srd52_en"
            )
            english_map_ref = _object(map_assets.get("srd52_en"), "srd52_en.map_ref")
            if english_map_ref.get("sha256") != english_asset_hash:
                _fail(
                    "source_mapping_asset_registry",
                    "source-pass 6-9 English asset identity differs",
                )
        rows = _rows(payload, "entries", lane_id)
        if len(rows) != expected["entry_count"]:
            _fail("source_mapping_lane_count", f"{lane_id} entry count differs")
        _validate_source_mapping_lane_totals(lane_id, lane, payload, rows)
        if lane_id == "source-pass-3-5":
            receipt_summary = _object(
                lane.get("receipt_summary"), f"{lane_id}.receipt_summary"
            )
            source_residuals = _strings(
                payload.get("residuals"), f"{lane_id}.source_residuals"
            )
            receipt_residuals = _strings(
                receipt_summary.get("residuals"), f"{lane_id}.receipt_residuals"
            )
            if (
                len(source_residuals) != 4
                or not source_residuals[0].startswith(
                    "Independent review of this 114-entry decomposition"
                )
                or len(receipt_residuals) != 4
                or receipt_summary.get("independent_review_status") != "PENDING"
            ):
                _fail(
                    "source_mapping_lane_residuals",
                    "source-pass 3-5 source and review residual records are incomplete",
                )
        names = [_source_mapping_lane_name(lane_id, row) for row in rows]
        if len(set(names)) != len(names):
            _fail("duplicate_source_map_entry", f"{lane_id} repeats an entry name")
        lane_names[lane_id] = set(names)
        lane_counts[lane_id] = len(rows)

        source_rows = _rows(pass_payloads[lane_id], "rows", lane_id)
        for row_index, row in enumerate(rows):
            name = names[row_index]
            roster_row = roster_by_name.get(name)
            if roster_row is None:
                _fail(
                    "source_mapping_orphan",
                    f"{lane_id} map includes {name} outside roster",
                )
            pass_ref = _object(
                roster_row.get("source_pass_row_ref"), f"{name}.source_pass_row_ref"
            )
            if pass_ref.get("artifact_id") != lane_id:
                _fail("source_mapping_wrong_slice", f"{name} is not in {lane_id}")
            actual_source_row_index = pass_ref.get("record_index")
            if type(actual_source_row_index) is not int:
                _fail("source_mapping_witness", f"{name} source row index is absent")
            if lane_id == "source-pass-0-2":
                source_ref = _object(
                    row.get("source_record_ref"), f"{name}.source_record_ref"
                )
                source_item = _resolve_json_pointer(
                    pass_payloads[lane_id],
                    _string(
                        source_ref.get("json_pointer"),
                        f"{name}.source_record_ref.json_pointer",
                    ),
                    f"{name}.source_record_ref",
                )
                inventory_ref = _object(
                    row.get("inventory_ref"), f"{name}.inventory_ref"
                )
                inventory_record = _resolve_json_pointer(
                    inventory_payload,
                    _string(
                        inventory_ref.get("json_pointer"),
                        f"{name}.inventory_ref.json_pointer",
                    ),
                    f"{name}.inventory_ref",
                )
                matrix_ref = _object(
                    row.get("requirement_matrix_ref"), f"{name}.requirement_matrix_ref"
                )
                matrix_record = _resolve_json_pointer(
                    matrix_payload,
                    _string(
                        matrix_ref.get("json_pointer"),
                        f"{name}.requirement_matrix_ref.json_pointer",
                    ),
                    f"{name}.requirement_matrix_ref",
                )
                body_ref = _object(
                    source_ref.get("body_witness_ref"), f"{name}.body_witness_ref"
                )
                body_record = _resolve_json_pointer(
                    body_payload,
                    _string(
                        body_ref.get("json_pointer"),
                        f"{name}.body_witness_ref.json_pointer",
                    ),
                    f"{name}.body_witness_ref",
                )
                if (
                    not isinstance(source_item, str)
                    or _object(inventory_record, f"{name}.inventory_record").get("name")
                    != name
                    or _object(matrix_record, f"{name}.matrix_record").get("name")
                    != name
                    or _object(body_record, f"{name}.body_record").get("name") != name
                    or source_ref.get("record_index") != actual_source_row_index
                    or source_ref.get("exact_record_name") != name
                    or source_ref.get("raw_body_sha256")
                    != pass_ref.get("raw_body_sha256")
                    or source_ref.get("printed_page") != pass_ref.get("source_page")
                    or source_ref.get("source_header_line")
                    != pass_ref.get("source_header_line")
                    or source_ref.get("source_asset_id") != "srd52_en"
                    or source_ref.get("edition") != "SRD_5_2_1"
                ):
                    _fail(
                        "source_mapping_witness",
                        f"{name} map is not bound to its exact source row",
                    )
                if (
                    row.get("consumer_dependency_edges") != []
                    or row.get("actual_native_proof_refs") != []
                    or row.get("consumer_dependency_status") != "NOT_ESTABLISHED"
                    or row.get("support_domain_census_status") != "NOT_ESTABLISHED"
                    or row.get("machine_admission_status") != "NOT_ESTABLISHED"
                    or row.get("production_support_status") != "NOT_ESTABLISHED"
                    or row.get("complete_source_key_roster_status") != "NOT_SEALED"
                ):
                    _fail(
                        "source_map_future_proof_inflation",
                        f"{name} summary decomposition claims downstream closure",
                    )
                for group_name in (
                    "common_requirements",
                    "conditional_branches",
                    "selectable_modes",
                    "control_transitions",
                    "target_forms",
                    "support_domains",
                ):
                    for record_index, record_value in enumerate(
                        _array(row.get(group_name), f"{name}.{group_name}")
                    ):
                        record = _object(
                            record_value, f"{name}.{group_name}[{record_index}]"
                        )
                        if (
                            record.get("native_consumer_mappings") != []
                            or record.get("actual_support_proof_refs") != []
                            or record.get("native_consumer_status") != "NOT_ESTABLISHED"
                            or record.get("support_proof_status") != "NOT_ESTABLISHED"
                        ):
                            _fail(
                                "source_map_future_proof_inflation",
                                f"{name}.{group_name}[{record_index}] claims native support",
                            )
                        if group_name == "support_domains" and (
                            record.get("eligible_member_ids") != []
                            or record.get("transitive_dependency_edges") != []
                            or record.get("member_census_status") != "NOT_ESTABLISHED"
                            or record.get("transitive_closure_status")
                            != "NOT_ESTABLISHED"
                        ):
                            _fail(
                                "source_map_future_proof_inflation",
                                f"{name} source support descriptor claims a completed domain census",
                            )
                for proof_index, proof_value in enumerate(
                    _array(
                        row.get("required_proof_obligations"),
                        f"{name}.required_proof_obligations",
                    )
                ):
                    proof = _object(
                        proof_value, f"{name}.required_proof_obligations[{proof_index}]"
                    )
                    if (
                        proof.get("actual_proof_refs") != []
                        or proof.get("status") != "NOT_ESTABLISHED"
                    ):
                        _fail(
                            "source_map_future_proof_inflation",
                            f"{name} claims a downstream task proof",
                        )
            elif lane_id == "source-pass-3-5":
                source_ref = _object(
                    row.get("source_record_ref"), f"{name}.source_record_ref"
                )
                pass_source_ref = _object(
                    source_ref.get("source_pass"),
                    f"{name}.source_record_ref.source_pass",
                )
                pointer = _string(
                    pass_source_ref.get("record_pointer"),
                    f"{name}.source_pass.record_pointer",
                )
                match = re.fullmatch(r"/rows/(\d+)", pointer)
                primary = _object(
                    source_ref.get("primary"), f"{name}.source_record_ref.primary"
                )
                source_item = _object(
                    _resolve_json_pointer(
                        pass_payloads[lane_id], pointer, f"{name}.source_pass"
                    ),
                    f"{name}.source_pass.row",
                )
                matrix_ref = _object(source_ref.get("matrix"), f"{name}.matrix_ref")
                inventory_ref = _object(
                    source_ref.get("inventory"), f"{name}.inventory_ref"
                )
                body_ref = _object(
                    source_ref.get("body_witness"), f"{name}.body_witness_ref"
                )
                matrix_record = _object(
                    _resolve_json_pointer(
                        matrix_payload,
                        _string(
                            matrix_ref.get("record_pointer"),
                            f"{name}.matrix_ref.record_pointer",
                        ),
                        f"{name}.matrix_ref",
                    ),
                    f"{name}.matrix_record",
                )
                inventory_record = _object(
                    _resolve_json_pointer(
                        inventory_payload,
                        _string(
                            inventory_ref.get("record_pointer"),
                            f"{name}.inventory_ref.record_pointer",
                        ),
                        f"{name}.inventory_ref",
                    ),
                    f"{name}.inventory_record",
                )
                body_record = _object(
                    _resolve_json_pointer(
                        body_payload,
                        _string(
                            body_ref.get("record_pointer"),
                            f"{name}.body_witness_ref.record_pointer",
                        ),
                        f"{name}.body_witness_ref",
                    ),
                    f"{name}.body_witness_record",
                )
                if (
                    match is None
                    or int(match.group(1)) != actual_source_row_index
                    or pass_source_ref.get("exact_name") != name
                    or source_item.get("name") != name
                    or source_ref.get("raw_body_sha256")
                    != pass_ref.get("raw_body_sha256")
                    or source_ref.get("raw_body_sha256")
                    != body_record.get("body_sha256")
                    or source_ref.get("raw_body_sha256")
                    != matrix_record.get("extracted_body_sha256")
                    or matrix_record.get("name") != name
                    or inventory_record.get("name") != name
                    or inventory_record.get("level") != roster_row.get("level")
                    or inventory_record.get("source_page")
                    != pass_ref.get("source_page")
                    or body_record.get("name") != name
                    or primary.get("asset_id") != "srd52_en"
                    or primary.get("printed_page") != pass_ref.get("source_page")
                    or primary.get("source_header_line")
                    != pass_ref.get("source_header_line")
                ):
                    _fail(
                        "source_mapping_witness",
                        f"{name} map is not bound to its exact source row",
                    )
                if row.get("consumer_dependency_status") != "NOT_ESTABLISHED":
                    _fail(
                        "source_map_future_proof_inflation",
                        f"{name} claims consumer closure",
                    )
                if (
                    row.get("source_support_mapping_status")
                    != "OBLIGATIONS_EXPLICIT_EXACT_DOMAIN_CENSUS_NOT_ESTABLISHED"
                    or row.get("production_support") != "NONE"
                    or row.get("scenario_verified") != "NOT_ESTABLISHED"
                ):
                    _fail(
                        "source_map_future_proof_inflation",
                        f"{name} source map overstates support or execution status",
                    )
                if row.get("source_mode_equality") != "NOT_YET_INDEPENDENTLY_REVIEWED":
                    _fail(
                        "source_mapping_review_status",
                        f"{name} source map is not marked for review",
                    )
                for mode_index, mode_value in enumerate(
                    _array(row.get("modes"), f"{name}.modes")
                ):
                    mode = _object(mode_value, f"{name}.modes[{mode_index}]")
                    for req_index, req_value in enumerate(
                        _array(
                            mode.get("requirements"),
                            f"{name}.modes[{mode_index}].requirements",
                        )
                    ):
                        req = _object(
                            req_value,
                            f"{name}.modes[{mode_index}].requirements[{req_index}]",
                        )
                        if (
                            req.get("consumer_mapping_status") != "NOT_ESTABLISHED"
                            or req.get("actual_proof_refs") != []
                            or req.get("source_equality_status")
                            != "INDEPENDENT_FORMULATION_AWAITS_REVIEW"
                        ):
                            _fail(
                                "source_map_future_proof_inflation",
                                f"{name} mode requirement claims closure",
                            )
                for req_index, req_value in enumerate(
                    _array(row.get("entry_requirements"), f"{name}.entry_requirements")
                ):
                    req = _object(req_value, f"{name}.entry_requirements[{req_index}]")
                    if (
                        req.get("consumer_mapping_status") != "NOT_ESTABLISHED"
                        or req.get("actual_proof_refs") != []
                    ):
                        _fail(
                            "source_map_future_proof_inflation",
                            f"{name} entry requirement claims consumer proof",
                        )
                for support_index, support_value in enumerate(
                    _array(
                        row.get("support_domain_mappings"),
                        f"{name}.support_domain_mappings",
                    )
                ):
                    support = _object(
                        support_value,
                        f"{name}.support_domain_mappings[{support_index}]",
                    )
                    if (
                        support.get("consumer_dependency_edges") != []
                        or support.get("actual_proof_refs") != []
                        or support.get("eligible_set_census_status")
                        != "NOT_ESTABLISHED_WHERE_DOMAIN_VALUED"
                        or support.get("declared_admitted_edges_status")
                        != "NOT_ESTABLISHED"
                    ):
                        _fail(
                            "source_map_future_proof_inflation",
                            f"{name} support descriptor claims native closure",
                        )
            else:
                encoding_contract = _object(
                    payload.get("encoding_contract"),
                    "source-pass-6-9.encoding_contract",
                )
                unknowns = _string(
                    encoding_contract.get("unknowns"),
                    "source-pass-6-9.encoding_contract.unknowns",
                )
                if (
                    "NOT_ESTABLISHED" not in unknowns
                    or "consumer_dependency_edges" not in unknowns
                ):
                    _fail(
                        "source_map_future_proof_inflation",
                        "source-pass 6-9 must keep native consumer/evaluation dimensions open",
                    )
                ref = _array(row.get("ref"), f"{name}.ref")
                source_row = source_rows[actual_source_row_index]
                _raw_source_name, exact_source_name, _alias_status = (
                    _canonical_source_name(source_row, lane_id)
                )
                if (
                    len(ref) != 4
                    or ref[0] != actual_source_row_index
                    or ref[1] != roster_row.get("level")
                    or ref[2] != pass_ref.get("source_page")
                    or ref[3] != pass_ref.get("source_header_line")
                    or exact_source_name != name
                ):
                    _fail(
                        "source_mapping_witness",
                        f"{name} map is not bound to its exact source row",
                    )
                summary_values = _strings(
                    source_row.get("required_modes_or_exceptions"),
                    f"{name}.required_modes_or_exceptions",
                )
                dependency_values = _strings(
                    source_row.get("required_dependency_or_native_contracts"),
                    f"{name}.required_dependency_or_native_contracts",
                )
                for group_name in ("shared", "modes", "nonduplication_consequences"):
                    group = row.get(group_name) or {}
                    group_obj = _object(group, f"{name}.{group_name}")
                    for key, branch_group in group_obj.items():
                        if group_name == "shared":
                            indices = _array(branch_group, f"{name}.shared.{key}")
                        else:
                            branches = _object(
                                branch_group, f"{name}.{group_name}.{key}"
                            )
                            indices = [
                                index
                                for branch_indices in branches.values()
                                for index in _array(
                                    branch_indices, f"{name}.{group_name}.{key}"
                                )
                            ]
                        if any(
                            type(index) is not int or index >= len(summary_values)
                            for index in indices
                        ):
                            _fail(
                                "source_mapping_reference",
                                f"{name} has an out-of-range source summary reference",
                            )
                support = _object(row.get("support") or {}, f"{name}.support")
                for key, indices in support.items():
                    if any(
                        type(index) is not int or index >= len(dependency_values)
                        for index in _array(indices, f"{name}.support.{key}")
                    ):
                        _fail(
                            "source_mapping_reference",
                            f"{name} has an out-of-range source support reference",
                        )

            (
                modes,
                requirements,
                support_keys,
                unresolved,
                transitions,
                target_forms,
                common_requirements,
                conditional_branches,
            ) = _source_mapping_lane_keys(lane_id, row)
            if not modes and lane_id != "source-pass-0-2":
                _fail(
                    "source_mapping_modes_missing",
                    f"{name} has no explicit mode mapping",
                )
            if lane_id == "source-pass-0-2":
                for group_name in (
                    "common_requirements",
                    "conditional_branches",
                    "selectable_modes",
                    "control_transitions",
                    "target_forms",
                    "support_domains",
                ):
                    for record in _rows(
                        {"rows": row.get(group_name, [])}, "rows", name
                    ):
                        if record.get("evidence_ref") != row.get("source_record_ref"):
                            _fail(
                                "source_mapping_witness",
                                f"{name} {group_name} record has a foreign evidence ref",
                            )
            if len(requirements) != len(set(requirements)):
                _fail(
                    "duplicate_source_requirement_key",
                    f"{name} has duplicate source requirement keys",
                )
            if all_requirement_keys.intersection(requirements):
                _fail(
                    "duplicate_source_requirement_key",
                    f"{name} duplicates a key owned by another source entry",
                )
            if all_mode_keys.intersection(modes):
                _fail(
                    "duplicate_source_mode_key",
                    f"{name} duplicates a key owned by another source entry",
                )
            if all_support_keys.intersection(support_keys):
                _fail(
                    "duplicate_source_support_key",
                    f"{name} duplicates a key owned by another source entry",
                )
            unresolved_names = {
                _string(value.get("unresolved_key"), f"{name}.unresolved_key")
                for value in unresolved
            }
            if all_unresolved_keys.intersection(unresolved_names):
                _fail(
                    "duplicate_source_unknown_key",
                    f"{name} duplicates an unresolved source key",
                )
            all_requirement_keys.update(requirements)
            all_mode_keys.update(modes)
            all_support_keys.update(support_keys)
            all_unresolved_keys.update(unresolved_names)
            map_index[name] = {
                "lane_id": lane_id,
                "source_mapping": row,
                "source_mode_keys": modes,
                "source_requirement_keys": requirements,
                "source_common_requirement_keys": common_requirements,
                "source_conditional_branch_keys": conditional_branches,
                "source_shared_common_requirement_refs": (
                    _strings(
                        row.get("common_rule_requirement_keys"),
                        f"{name}.common_rule_requirement_keys",
                    )
                    if lane_id == "source-pass-0-2"
                    else []
                ),
                "source_support_domain_obligation_keys": support_keys,
                "source_control_transition_keys": transitions,
                "source_target_form_keys": target_forms,
                "unresolved_source_keys": unresolved,
                "mapping_status": "PENDING_INDEPENDENT_REVIEW",
                "source_record_ref": dict(pass_ref),
                "map_artifact_sha256": lane["map_artifact_sha256"],
                "mapping_payload_sha256": lane["mapping_payload_sha256"],
            }

    expected_lane_names = {
        "source-pass-0-2": {
            str(row["name"])
            for row in roster
            if int(row["level"]) <= 2 and row["name"] not in summary_names
        },
        "source-pass-3-5": {
            str(row["name"]) for row in roster if 3 <= int(row["level"]) <= 5
        },
        "source-pass-6-9": {
            str(row["name"]) for row in roster if int(row["level"]) >= 6
        },
    }
    all_lane_names: set[str] = set()
    for lane_id, expected_names in expected_lane_names.items():
        names = lane_names[lane_id]
        if names != expected_names:
            missing = sorted(expected_names - names)
            extra = sorted(names - expected_names)
            _fail(
                "source_mapping_membership",
                f"{lane_id} entry set differs; missing={missing[:5]} extra={extra[:5]}",
            )
        if all_lane_names.intersection(names):
            _fail(
                "source_mapping_lane_overlap",
                f"{lane_id} overlaps another source map lane",
            )
        all_lane_names.update(names)
    summary_maps = _validate_source_mode_mappings(manifest, roster)
    if all_lane_names.intersection(summary_maps):
        _fail(
            "source_mapping_lane_overlap",
            "source-pass lane overlaps an existing summary decomposition",
        )
    if all_lane_names | set(summary_maps) != inventory_names:
        _fail(
            "source_mapping_roster_equality",
            "mapping lanes and existing maps do not equal the exact 339 roster",
        )
    if len(map_index) != 337:
        _fail(
            "source_mapping_lane_count",
            "the three disjoint map lanes must cover 337 entries",
        )

    for name, mapping in summary_maps.items():
        mode_keys: list[str] = []
        requirement_keys: list[str] = []
        conditional_branch_keys: list[str] = []
        for mode_value in _array(mapping.get("modes"), f"{name}.modes"):
            mode = _object(mode_value, f"{name}.mode")
            mode_key = _string(mode.get("mode_key"), f"{name}.mode_key")
            mode_keys.append(mode_key)
            for req_value in _array(
                mode.get("requirements"), f"{name}.{mode_key}.requirements"
            ):
                req = _object(req_value, f"{name}.{mode_key}.requirement")
                requirement_keys.append(
                    _string(req.get("requirement_key"), f"{name}.requirement_key")
                )
                conditional_branch_keys.append(requirement_keys[-1])
        transition_keys: list[str] = []
        for transition_value in _array(
            mapping.get("control_transitions"), f"{name}.control_transitions"
        ):
            transition = _object(transition_value, f"{name}.control_transition")
            transition_key = _string(
                transition.get("transition_key"), f"{name}.transition_key"
            )
            transition_keys.append(transition_key)
            for req_value in _array(
                transition.get("requirements"), f"{name}.{transition_key}.requirements"
            ):
                req = _object(req_value, f"{name}.{transition_key}.requirement")
                requirement_keys.append(
                    _string(req.get("requirement_key"), f"{name}.requirement_key")
                )
                conditional_branch_keys.append(requirement_keys[-1])
        if (
            len(requirement_keys) != len(set(requirement_keys))
            or all_requirement_keys.intersection(requirement_keys)
            or all_mode_keys.intersection(mode_keys)
        ):
            _fail(
                "duplicate_source_key",
                f"{name} summary map keys collide with a source lane",
            )
        all_requirement_keys.update(requirement_keys)
        all_mode_keys.update(mode_keys)
        map_index[name] = {
            "lane_id": "existing-summary-decompositions",
            "source_mapping": mapping,
            "source_mode_keys": mode_keys,
            "source_requirement_keys": requirement_keys,
            "source_common_requirement_keys": [],
            "source_conditional_branch_keys": conditional_branch_keys,
            "source_shared_common_requirement_refs": [],
            "source_support_domain_obligation_keys": [],
            "source_control_transition_keys": transition_keys,
            "source_target_form_keys": [],
            "unresolved_source_keys": [],
            "mapping_status": "SUMMARY_DECOMPOSITION_ONLY_NOT_SOURCE_QUALIFIED",
            "source_record_ref": {
                "artifact_id": _object(
                    mapping["source_record_ref"], f"{name}.source_record_ref"
                )["artifact_id"],
                "exact_name": name,
                "raw_body_sha256": _object(
                    mapping["source_record_ref"], f"{name}.source_record_ref"
                )["raw_body_sha256"],
            },
            "map_artifact_sha256": REVIEWED_SOURCE_MANIFEST_SHA256,
            "mapping_payload_sha256": REVIEWED_SOURCE_MANIFEST_SHA256,
        }

    first_lane = next(
        lane for lane in lanes if lane.get("lane_id") == "source-pass-0-2"
    )
    first_payload = _object(
        first_lane.get("mapping_payload"), "source-pass-0-2.mapping_payload"
    )
    shared_common_records = [
        _object(value, f"shared_common_requirements[{index}]")
        for index, value in enumerate(
            _array(
                first_payload.get("shared_common_requirements"),
                "shared_common_requirements",
            )
        )
    ]
    shared_common_keys = [
        _string(
            record.get("source_requirement_key"),
            f"shared_common_requirements[{index}].source_requirement_key",
        )
        for index, record in enumerate(shared_common_records)
    ]
    if (
        len(shared_common_keys) != 16
        or len(set(shared_common_keys)) != 16
        or all_requirement_keys.intersection(shared_common_keys)
    ):
        _fail(
            "shared_common_source_keys",
            "shared source requirement keys are missing or duplicated",
        )
    for name, map_row in map_index.items():
        shared_refs = _strings(
            map_row.get("source_shared_common_requirement_refs"),
            f"{name}.source_shared_common_requirement_refs",
        )
        if not set(shared_refs).issubset(set(shared_common_keys)):
            _fail(
                "shared_common_source_key_orphan",
                f"{name} refers to an unknown shared common requirement",
            )
    all_requirement_keys.update(shared_common_keys)
    lane0_unresolved_index = {
        str(record["unresolved_key"]): record
        for record in [
            _object(value, f"source-pass-0-2.unresolved_key_index[{index}]")
            for index, value in enumerate(
                _array(
                    first_payload.get("unresolved_key_index"),
                    "source-pass-0-2.unresolved_key_index",
                )
            )
        ]
    }
    lane0_unresolved_entries = {
        str(record["unresolved_key"]): record
        for map_name, map_row in map_index.items()
        if map_row["lane_id"] == "source-pass-0-2"
        for record in map_row["unresolved_source_keys"]
    }
    if (
        len(all_unresolved_keys) != 82
        or set(lane0_unresolved_index) != set(lane0_unresolved_entries)
        or lane0_unresolved_index != lane0_unresolved_entries
    ):
        _fail(
            "source_mapping_residual_census",
            "source mapping lanes must preserve all 82 keyed residuals",
        )

    contract = _object(
        manifest.get("source_mapping_contract"), "source_mapping_contract"
    )
    if (
        contract.get("status") != "ALL_339_ENTRY_MAPS_SOURCE_CLOSURE_OPEN"
        or contract.get("source_entry_count") != 339
        or contract.get("candidate_entry_map_count") != 339
        or contract.get("summary_decomposition_entry_names")
        != ["Alter Self", "Elementalism"]
        or contract.get("lane_entry_counts")
        != {
            "source-pass-0-2": 139,
            "source-pass-3-5": 114,
            "source-pass-6-9": 84,
            "existing-summary-decompositions": 2,
        }
        or contract.get("unresolved_source_key_count") != 82
        or contract.get("unresolved_source_entry_count") != 72
        or contract.get("source_mapping_review_status") != "PENDING_INDEPENDENT_REVIEW"
        or contract.get("source_modeling_residual_count") != 1
        or contract.get("source_modeling_resolution_count") != 5
        or contract.get("source_unknown_classification_record_count") != 82
        or contract.get("source_blocking_unknown_key_count") != 77
        or contract.get("downstream_only_unknown_key_count") != 5
        or contract.get("mixed_unknown_key_count") != 28
        or contract.get("source_unknown_classification_status") != "ALL_82_CLASSIFIED"
        or contract.get("primary_table_evidence_residual_count") != 0
        or contract.get("summary_string_as_mode_policy") != "FORBIDDEN"
        or contract.get("inventory_dependency_labels_as_support_policy")
        != "NOT_SUPPORT_DOMAIN_MAPPINGS"
        or contract.get("source_support_obligation_status")
        != "PARTIAL_SOURCE_DESCRIPTORS_DOMAIN_CENSUS_NOT_ESTABLISHED"
        or contract.get("future_native_proof_status")
        != "NOT_ESTABLISHED_NOT_AN_SP00_SOURCE_READY_GATE"
        or contract.get("production_claim") != "NONE"
    ):
        _fail("source_mapping_contract", "merged source map coverage contract differs")
    unresolved_keys = [
        _object(value, f"source_modeling_residuals[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_modeling_residuals"), "source_modeling_residuals"
            )
        )
    ]
    table_residuals = [
        _object(value, f"primary_table_evidence_residuals[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("primary_table_evidence_residuals"),
                "primary_table_evidence_residuals",
            )
        )
    ]
    lane6_payload = _object(
        next(
            lane["mapping_payload"]
            for lane in lanes
            if lane.get("lane_id") == "source-pass-6-9"
        ),
        "source-pass-6-9.mapping_payload",
    )
    lane6_row_by_name = {
        str(row.get("name")): row
        for row in _rows(lane6_payload, "entries", "source-pass-6-9")
    }
    for residual in unresolved_keys:
        name = _string(
            residual.get("source_exact_name"),
            "source_modeling_residual.source_exact_name",
        )
        row = lane6_row_by_name.get(name)
        source_ref = _object(
            residual.get("source_record_ref"), f"{name}.source_record_ref"
        )
        if row is None:
            _fail(
                "source_mapping_residual_witness",
                f"{name} is outside source-pass 6-9 maps",
            )
        row_ref = _array(row.get("ref"), f"{name}.ref")
        if (
            source_ref.get("artifact_id") != "source-pass-6-9"
            or source_ref.get("record_index") != row_ref[0]
            or source_ref.get("printed_page") != row_ref[2]
            or source_ref.get("source_header_line") != row_ref[3]
            or residual.get("status") != "NOT_ESTABLISHED"
        ):
            _fail(
                "source_mapping_residual_witness",
                f"{name} source-modeling residual is stale",
            )
    tail_annotations = [
        _object(value, f"source-pass-6-9.tail_and_table_annotations[{index}]")
        for index, value in enumerate(
            _array(
                lane6_payload.get("tail_and_table_annotations"),
                "source-pass-6-9.tail_and_table_annotations",
            )
        )
    ]
    table_annotation_names = {row.get("entry") for row in tail_annotations}
    lane6_reported_residuals = [
        _object(value, f"source-pass-6-9.lane_reported_residuals[{index}]")
        for index, value in enumerate(
            _array(
                lane6_payload.get("lane_reported_source_modeling_residuals"),
                "source-pass-6-9.lane_reported_source_modeling_residuals",
            )
        )
    ]
    lane6_current_residuals = [
        _object(value, f"source-pass-6-9.current_residuals[{index}]")
        for index, value in enumerate(
            _array(
                lane6_payload.get("source_modeling_residuals"),
                "source-pass-6-9.source_modeling_residuals",
            )
        )
    ]
    lane6_resolution_ids = _strings(
        lane6_payload.get("source_modeling_resolutions"),
        "source-pass-6-9.source_modeling_resolutions",
    )
    if (
        len(lane6_reported_residuals) != 6
        or {row.get("source_exact_name") for row in lane6_reported_residuals}
        != {
            "Flesh to Stone",
            "Heroes’ Feast",
            "Instant Summons",
            "Move Earth",
            "Word of Recall",
            "Mass Heal",
        }
        or len(lane6_current_residuals) != 1
        or lane6_current_residuals[0].get("source_exact_name") != "Word of Recall"
        or len(lane6_resolution_ids) != 5
        or len(unresolved_keys) != 1
        or {row.get("source_exact_name") for row in unresolved_keys}
        != {"Word of Recall"}
        or table_residuals
        or lane6_payload.get("primary_table_evidence_residuals") != []
        or _object(
            next(
                lane["receipt_summary"]
                for lane in lanes
                if lane.get("lane_id") == "source-pass-6-9"
            ),
            "source-pass-6-9.receipt_summary",
        ).get("primary_table_evidence_residuals")
        != []
        or not {"Teleport", "Control Weather"}.issubset(table_annotation_names)
    ):
        _fail(
            "source_mapping_residual_census", "named source/modeling residuals differ"
        )
    lane0_payload = next(
        _object(lane.get("mapping_payload"), "lane.mapping_payload")
        for lane in lanes
        if lane.get("lane_id") == "source-pass-0-2"
    )
    lane0_residuals = [
        _object(value, f"source-pass-0-2.unresolved_key_index[{index}]")
        for index, value in enumerate(
            _array(
                lane0_payload.get("unresolved_key_index"),
                "source-pass-0-2.unresolved_key_index",
            )
        )
    ]
    lane0_entry_names = {
        str(row.get("source_exact_name"))
        for row in _rows(lane0_payload, "entries", "source-pass-0-2")
        if _array(row.get("unresolved_keys"), "source-pass-0-2.unresolved_keys")
    }
    lane0_declared_counts = _object(
        lane0_payload.get("counts"), "source-pass-0-2.counts"
    )
    if (
        len(lane0_residuals) != 82
        or len({row.get("unresolved_key") for row in lane0_residuals}) != 82
        or len(lane0_entry_names) != 72
        or lane0_declared_counts.get("explicit_unresolved_keys") != 82
        or lane0_declared_counts.get("entries_with_explicit_residuals") != 72
    ):
        _fail("source_mapping_residual_census", "source-pass 0-2 residual keys differ")
    return map_index


SOURCE_UNKNOWN_CATEGORIES = {
    "source_parameter",
    "source_semantics",
    "source_mapping_review",
    "downstream_domain_consumer_admission_native_proof",
}
SOURCE_UNKNOWN_SOURCE_CATEGORIES = {
    "source_parameter",
    "source_semantics",
    "source_mapping_review",
}
SOURCE_UNKNOWN_EXPECTED_COUNTS = {
    "source_parameter": 36,
    "source_semantics": 22,
    "source_mapping_review": 23,
    "downstream_domain_consumer_admission_native_proof": 33,
}
SOURCE_MARKDOWN_RELATIVE_PATH = "DEV/docs/SRD_CC_v5.2.1.md"
SOURCE_MARKDOWN_SHA256 = (
    "c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e"
)
SOURCE_RESIDUAL_EVIDENCE_RELATIVE_PATH = "DEV/docs/superpowers/design/2026-10-07-sp00-first12-markdown-source-qualification.md"
SOURCE_RESIDUAL_EVIDENCE_SHA256 = (
    "2ab8076aabba92f9e315dcf8e01af7928e50e83ce5645234c099c58d96ad9c08"
)
SOURCE_RESOLVED_KEYS = frozenset(
    {
        "source.spell.alarm.unresolved.audible_sound_bounds",
        "source.spell.animal_messenger.unresolved.travel_and_message_bounds",
        "source.spell.augury.unresolved.recast_probability",
        "source.spell.chromatic_orb.unresolved.leap_distance_and_scaling",
        "source.spell.command.unresolved.command_exact_restrictions",
        "source.spell.continual_flame.unresolved.darkness_interaction",
        "source.spell.dancing_lights.unresolved.movement_and_link_bounds",
        "source.spell.darkness.unresolved.interaction_thresholds",
        "source.spell.detect_evil_and_good.unresolved.barrier_thresholds",
    }
)
SOURCE_HELD_KEYS = frozenset(
    {
        "source.spell.aid.unresolved.health_normalization_policy",
        "source.spell.arcane_lock.unresolved.destruction_access_policy",
        "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
    }
)
SOURCE_RESOLUTION_KEYS = (
    "source.spell.aid.unresolved.health_normalization_policy",
    "source.spell.alarm.unresolved.audible_sound_bounds",
    "source.spell.animal_messenger.unresolved.travel_and_message_bounds",
    "source.spell.arcane_lock.unresolved.destruction_access_policy",
    "source.spell.augury.unresolved.recast_probability",
    "source.spell.chromatic_orb.unresolved.leap_distance_and_scaling",
    "source.spell.command.unresolved.command_exact_restrictions",
    "source.spell.continual_flame.unresolved.darkness_interaction",
    "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
    "source.spell.dancing_lights.unresolved.movement_and_link_bounds",
    "source.spell.darkness.unresolved.interaction_thresholds",
    "source.spell.detect_evil_and_good.unresolved.barrier_thresholds",
)
SOURCE_RESOLUTION_CATEGORIES: dict[str, str] = {
    "source.spell.aid.unresolved.health_normalization_policy": "source_semantics",
    "source.spell.alarm.unresolved.audible_sound_bounds": "source_parameter",
    "source.spell.animal_messenger.unresolved.travel_and_message_bounds": "source_parameter",
    "source.spell.arcane_lock.unresolved.destruction_access_policy": "source_semantics",
    "source.spell.augury.unresolved.recast_probability": "source_parameter",
    "source.spell.chromatic_orb.unresolved.leap_distance_and_scaling": "source_parameter",
    "source.spell.command.unresolved.command_exact_restrictions": "source_semantics",
    "source.spell.continual_flame.unresolved.darkness_interaction": "source_semantics",
    "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds": "source_parameter",
    "source.spell.dancing_lights.unresolved.movement_and_link_bounds": "source_parameter",
    "source.spell.darkness.unresolved.interaction_thresholds": "source_parameter",
    "source.spell.detect_evil_and_good.unresolved.barrier_thresholds": "source_parameter",
}
SOURCE_MARKDOWN_LOCATORS: dict[str, list[dict[str, object]]] = {
    "source.spell.aid.unresolved.health_normalization_policy": [
        {"heading": "Aid", "line_start": 9307, "line_end": 9321},
        {"heading": "Duration", "line_start": 9205, "line_end": 9213},
        {"heading": "Combining Spell Effects", "line_start": 9255, "line_end": 9257},
    ],
    "source.spell.alarm.unresolved.audible_sound_bounds": [
        {"heading": "Alarm", "line_start": 9325, "line_end": 9341}
    ],
    "source.spell.animal_messenger.unresolved.travel_and_message_bounds": [
        {"heading": "Animal Messenger", "line_start": 9385, "line_end": 9401}
    ],
    "source.spell.arcane_lock.unresolved.destruction_access_policy": [
        {"heading": "Arcane Lock", "line_start": 9592, "line_end": 9604}
    ],
    "source.spell.augury.unresolved.recast_probability": [
        {"heading": "Augury", "line_start": 9666, "line_end": 9678},
        {"heading": "Augury", "line_start": 9691, "line_end": 9693},
    ],
    "source.spell.chromatic_orb.unresolved.leap_distance_and_scaling": [
        {"heading": "Chromatic Orb", "line_start": 10105, "line_end": 10121}
    ],
    "source.spell.command.unresolved.command_exact_restrictions": [
        {"heading": "Command", "line_start": 10215, "line_end": 10239}
    ],
    "source.spell.continual_flame.unresolved.darkness_interaction": [
        {"heading": "Continual Flame", "line_start": 10550, "line_end": 10562},
        {"heading": "Darkness", "line_start": 10784, "line_end": 10798},
        {
            "heading": "Using a Higher-Level Spell Slot",
            "line_start": 9106,
            "line_end": 9110,
        },
    ],
    "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds": [
        {"heading": "Create or Destroy Water", "line_start": 10674, "line_end": 10692}
    ],
    "source.spell.dancing_lights.unresolved.movement_and_link_bounds": [
        {"heading": "Dancing Lights", "line_start": 10766, "line_end": 10780},
        {"heading": "Range", "line_start": 9165, "line_end": 9175},
    ],
    "source.spell.darkness.unresolved.interaction_thresholds": [
        {"heading": "Darkness", "line_start": 10784, "line_end": 10798},
        {
            "heading": "Using a Higher-Level Spell Slot",
            "line_start": 9106,
            "line_end": 9110,
        },
    ],
    "source.spell.detect_evil_and_good.unresolved.barrier_thresholds": [
        {"heading": "Detect Evil and Good", "line_start": 10894, "line_end": 10908}
    ],
}
SOURCE_MARKDOWN_REQUIRED_PHRASES: dict[str, tuple[tuple[int, str], ...]] = {
    "source.spell.aid.unresolved.health_normalization_policy": (
        (0, "current Hit Points increase by 5"),
        (0, "for each spell slot level above 2"),
        (1, "if you don’t have the Incapacitated condition"),
        (2, "most potent effect"),
    ),
    "source.spell.alarm.unresolved.audible_sound_bounds": (
        (0, "for 10 seconds within 60 feet of the warded area"),
        (0, "within 1 mile of the warded area"),
        (0, "no larger than a 20-foot Cube"),
    ),
    "source.spell.animal_messenger.unresolved.travel_and_message_bounds": (
        (0, "up to twenty-five words"),
        (0, "covering about 25 miles per 24 hours or 50 miles if the Beast can fly"),
        (0, "the Beast returns to where you cast the spell"),
    ),
    "source.spell.arcane_lock.unresolved.destruction_access_policy": (
        (0, "can’t be unlocked by any nonmagical means"),
        (0, "within 5 feet of the object"),
        (0, "unlocks it for 1 minute"),
    ),
    "source.spell.augury.unresolved.recast_probability": (
        (0, "within the next 30 minutes"),
        (1, "before finishing a Long Rest"),
        (1, "cumulative 25 percent chance for each casting after the first"),
    ),
    "source.spell.chromatic_orb.unresolved.leap_distance_and_scaling": (
        (0, "same number on two or more of the d8s"),
        (0, "within 30 feet of the target"),
        (0, "maximum number of times equal to the level of the slot expended"),
        (0, "creature can be targeted only once"),
    ),
    "source.spell.command.unresolved.command_exact_restrictions": (
        (0, "shortest and most direct route"),
        (0, "if it moves within 5 feet of you"),
        (0, "takes no action or Bonus Action"),
    ),
    "source.spell.continual_flame.unresolved.darkness_interaction": (
        (0, "20-foot radius and Dim Light for an additional 20 feet"),
        (1, "spell of level 2 or lower"),
        (1, "that other spell is dispelled"),
        (2, "takes on the higher level for that casting"),
    ),
    "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds": (
        (0, "up to 10 gallons of clean water"),
        (0, "in an open container"),
        (0, "30-foot Cube"),
        (0, "size of the Cube increases by 5 feet"),
    ),
    "source.spell.dancing_lights.unresolved.movement_and_link_bounds": (
        (0, "move the lights up to 60 feet to a space within range"),
        (0, "within 20 feet of another light created by this spell"),
        (0, "vanishes if it exceeds the spell’s range"),
        (
            1,
            "aren’t restricted by its range unless the spell’s description says otherwise",
        ),
    ),
    "source.spell.darkness.unresolved.interaction_thresholds": (
        (0, "15-foot-radius Sphere"),
        (0, "15-foot Emanation"),
        (0, "Darkvision can’t see through it"),
        (0, "nonmagical light can’t illuminate it"),
        (0, "spell of level 2 or lower"),
        (0, "that other spell is dispelled"),
        (1, "takes on the higher level for that casting"),
    ),
    "source.spell.detect_evil_and_good.unresolved.barrier_thresholds": (
        (0, "within 30 feet of yourself"),
        (0, "*Hallow* spell is active there"),
        (0, "1 foot of stone, dirt, or wood"),
        (0, "1 inch of metal"),
        (0, "a thin sheet of lead"),
    ),
}
SOURCE_RESIDUAL_REVIEW = {
    "review_id": "SP00_FIRST12_MARKDOWN_REVIEW_20261007",
    "integration_base_sha": "4222a6c88234afeee893697241830b4e75521477",
    "candidate_source_base_sha": "4fb8a15108bf6b4b3108dac83a02735bdd21b04e",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-residuals-first12/residuals-first12.json",
    "candidate_sha256": "110b5704d31546c20981d7d179a3dcc78b580db00a50ff5f12a31beef703a8df",
    "candidate_report_path": "/tmp/hdm-dev/spell-recovery/SP00-residuals-first12/report.md",
    "candidate_report_sha256": "7d841d1917f6ec8e98752d7a33832209dcdb7fe0e15fe5c3bbc29d50f5990864",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-first12-markdown-review-20261007.md",
    "accepted_review_sha256": "e0c581fd53df459790266a021122d7be6d3f950a8d3a0d613d8c4ee52f32179c",
    "task_evidence_path": SOURCE_RESIDUAL_EVIDENCE_RELATIVE_PATH,
    "task_evidence_sha256": SOURCE_RESIDUAL_EVIDENCE_SHA256,
}

SOURCE_NEXT12_EVIDENCE_RELATIVE_PATH = (
    "DEV/docs/superpowers/design/2026-10-08-sp00-next-markdown-source-qualification.md"
)
SOURCE_NEXT12_EVIDENCE_SHA256 = (
    "02bbe067448e9c8b0502c960ad39891cdb67d7981d5e00f5a6c14374001a5fd5"
)
SOURCE_NEXT12_REVIEW = {
    "review_id": "SP00_NEXT12_MARKDOWN_REVIEW_20261008",
    "integration_base_sha": "0792404d33baf1d7ce2d4223655dd30a049e8f58",
    "candidate_source_base_sha": "0792404d33baf1d7ce2d4223655dd30a049e8f58",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-next-residuals-20261008.json",
    "candidate_sha256": "ee747f131a118932fbe73d3c1136bbf72d1e6cd5c76f93ee06ac6a03d1259fb6",
    "candidate_summary_path": "/tmp/hdm-dev/spell-recovery/SP00-next-residuals-20261008.md",
    "candidate_summary_sha256": "f6e5c36af4b8b2e4abff78d0083f2eecec79271375ec50af901591f772908bf8",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-next-residuals-review-20261008.md",
    "accepted_review_sha256": "e12bdbe94481c9cd757fd15dfc7966c34fcb576e9350a1099b521cd66715d4bd",
    "task_evidence_path": SOURCE_NEXT12_EVIDENCE_RELATIVE_PATH,
    "task_evidence_sha256": SOURCE_NEXT12_EVIDENCE_SHA256,
}

NEXT12_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.arcanist_s_magic_aura.unresolved.alternate_type_domain": {
        "source_exact_name": "Arcanist’s Magic Aura",
        "category": "source_mapping_review",
        "classification_index": 4,
        "map_entry_index": 7,
        "source_pass_row": 8,
        "body_witness_row": 17,
        "printed_page": 110,
        "source_header_line": 9376,
        "raw_body_sha256": "95dc368e392b20b55d54119445800bf9b06a65ff265ab10c48594f2f3c0ae41b",
        "classification_status": "MIXED_SOURCE_AND_FUTURE_PROOF",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Arcanist’s Magic Aura", "line_start": 9626, "line_end": 9642},
            {"heading": "Creature Type", "line_start": 16344, "line_end": 16350},
        ],
        "required_source_phrases": (
            (0, "Choose a creature type other than the target’s actual type."),
            (0, "same target every day for 30 days"),
            (
                1,
                "Aberration Elemental Monstrosity Beast Fey Ooze Celestial Fiend Plant Construct Giant Undead Dragon Humanoid",
            ),
        ),
        "required_qualifiers": (
            "actual creature type dynamically",
            "not actual type/species truth",
            "object receives False Aura",
        ),
    },
    "source.spell.arcanist_s_magic_aura.unresolved.false_aura_choice_domain": {
        "source_exact_name": "Arcanist’s Magic Aura",
        "category": "source_mapping_review",
        "classification_index": 5,
        "map_entry_index": 7,
        "source_pass_row": 8,
        "body_witness_row": 17,
        "printed_page": 110,
        "source_header_line": 9376,
        "raw_body_sha256": "95dc368e392b20b55d54119445800bf9b06a65ff265ab10c48594f2f3c0ae41b",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Arcanist’s Magic Aura", "line_start": 9626, "line_end": 9642},
            {"heading": "School of Magic", "line_start": 9114, "line_end": 9131},
            {"heading": "Detect Magic", "line_start": 10912, "line_end": 10926},
        ],
        "required_source_phrases": (
            (
                0,
                "You can make a nonmagical object appear magical, make a magic item appear nonmagical",
            ),
            (1, "Abjuration"),
            (1, "Conjuration"),
            (1, "Divination"),
            (1, "Enchantment"),
            (1, "Evocation"),
            (1, "Illusion"),
            (1, "Necromancy"),
            (1, "Transmutation"),
            (2, "you learn the spell’s school of magic"),
        ),
        "required_qualifiers": (
            "neither worn nor carried",
            "false presence starts with a nonmagical object",
            "false absence starts with a magic item",
            "actual origin mutation",
            "Detect Magic multi-origin",
        ),
    },
    "source.spell.chromatic_orb.unresolved.six_damage_type_members": {
        "source_exact_name": "Chromatic Orb",
        "category": "source_mapping_review",
        "classification_index": 11,
        "map_entry_index": 18,
        "source_pass_row": 19,
        "body_witness_row": 42,
        "printed_page": 115,
        "source_header_line": 9801,
        "raw_body_sha256": "6a1f9ba224b9661d66cafe826aaf7c3f28a02ecb7cb46eb6b36a678dc5f2da42",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Chromatic Orb", "line_start": 10105, "line_end": 10121}
        ],
        "required_source_phrases": (
            (
                0,
                "Choose Acid, Cold, Fire, Lightning, Poison, or Thunder for the type of orb you create",
            ),
            (0, "3d8 damage of the chosen type"),
            (0, "for each spell slot level above 1"),
        ),
        "required_qualifiers": (
            "complete selected source domain",
            "before the ranged spell attack",
            "no additional type is inferred",
            "raw-d8 leap",
        ),
    },
    "source.spell.detect_evil_and_good.unresolved.supernatural_type_members": {
        "source_exact_name": "Detect Evil and Good",
        "category": "source_mapping_review",
        "classification_index": 18,
        "map_entry_index": 28,
        "source_pass_row": 29,
        "body_witness_row": 80,
        "printed_page": 123,
        "source_header_line": 10560,
        "raw_body_sha256": "db5ac0c968464e9f0b8c495ce7d8a1ac5ba13bd34d7e91dc96c97548171e29c4",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Detect Evil and Good", "line_start": 10894, "line_end": 10908},
            {"heading": "Arcanist’s Magic Aura", "line_start": 9626, "line_end": 9640},
        ],
        "required_source_phrases": (
            (
                0,
                "Aberration, Celestial, Elemental, Fey, Fiend, or Undead within 30 feet of yourself",
            ),
            (0, "whether the *Hallow* spell is active there"),
            (0, "thin sheet of lead"),
        ),
        "required_qualifiers": (
            "direct filter domain, not six selectable",
            "Hallow presence/location remains separate",
            "Mask affects magical treatment",
        ),
    },
    "source.spell.detect_magic.unresolved.aura_overlay_policy": {
        "source_exact_name": "Detect Magic",
        "category": "source_semantics",
        "classification_index": 20,
        "map_entry_index": 29,
        "source_pass_row": 30,
        "body_witness_row": 81,
        "printed_page": 123,
        "source_header_line": 10571,
        "raw_body_sha256": "e0cdc16bbfdea122a6617dfc7b12d108a55301af2ffef39b15f1dfb7c2b5b45a",
        "classification_status": "MIXED_SOURCE_AND_FUTURE_PROOF",
        "disposition": "SOURCE_HELD",
        "locators": [
            {"heading": "Detect Magic", "line_start": 10912, "line_end": 10926},
            {"heading": "Arcanist’s Magic Aura", "line_start": 9626, "line_end": 9642},
        ],
        "required_source_phrases": (
            (0, "sense the presence of magical effects within 30 feet"),
            (0, "see a faint aura around any visible creature or object"),
            (0, "you learn the spell’s school of magic"),
            (1, "You change the way the target appears"),
        ),
        "required_qualifiers": (
            "presence, visible aura and spell-origin school are distinct",
            "visible bearer and Magic action",
            "multi-origin and self-illusion",
            "SOURCE_HELD",
        ),
    },
    "source.spell.detect_poison_and_disease.unresolved.barrier_and_catalog_domain": {
        "source_exact_name": "Detect Poison and Disease",
        "category": "source_parameter",
        "classification_index": 21,
        "map_entry_index": 30,
        "source_pass_row": 31,
        "body_witness_row": 82,
        "printed_page": 123,
        "source_header_line": 10585,
        "raw_body_sha256": "aa3e92445702ecaf4f18edae3ccea418bc7cf9d2055a162ab1c192bab0520680",
        "classification_status": "MIXED_SOURCE_AND_FUTURE_PROOF",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {
                "heading": "Detect Poison and Disease",
                "line_start": 10930,
                "line_end": 10944,
            }
        ],
        "required_source_phrases": (
            (
                0,
                "poisons, poisonous or venomous creatures, and magical contagions within 30 feet",
            ),
            (0, "You sense the kind of poison, creature, or contagion"),
            (0, "thin sheet of lead"),
        ),
        "required_qualifiers": (
            "magical contagions, not every mundane disease",
            "No numeric lead thickness",
            "lawful poison/contagion catalog census",
            "downstream consumers remain open",
            "complete lawful catalog/search domain remain NOT_ESTABLISHED",
        ),
    },
    "source.spell.detect_thoughts.unresolved.deeper_failure_disclosure": {
        "source_exact_name": "Detect Thoughts",
        "category": "source_semantics",
        "classification_index": 22,
        "map_entry_index": 31,
        "source_pass_row": 32,
        "body_witness_row": 83,
        "printed_page": 123,
        "source_header_line": 10597,
        "raw_body_sha256": "0438b5af49c583315faf6a21369e3f40d2d18258d85c9c2b489fdf12380f07c9",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Detect Thoughts", "line_start": 10948, "line_end": 10964}
        ],
        "required_source_phrases": (
            (0, "As a Magic action on your next turn"),
            (0, "On a failed save, you discern the target’s reasoning, emotions"),
            (0, "the target can take an action on its turn"),
            (0, "Intelligence (Arcana) check against your spell save DC"),
        ),
        "required_qualifiers": (
            "next-turn Magic action",
            "on its own turn",
            "not an opposed roll",
            "presence-only Sense",
        ),
    },
    "source.spell.dragon_s_breath.unresolved.five_damage_type_members": {
        "source_exact_name": "Dragon’s Breath",
        "category": "source_mapping_review",
        "classification_index": 24,
        "map_entry_index": 36,
        "source_pass_row": 37,
        "body_witness_row": 97,
        "printed_page": 126,
        "source_header_line": 10862,
        "raw_body_sha256": "2e78a4c1fd96986216faf7a582b198cb444021d3da17a2dc444b8b0f34b46873",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Dragon’s Breath", "line_start": 11221, "line_end": 11235}
        ],
        "required_source_phrases": (
            (0, "choose Acid, Cold, Fire, Lightning, or Poison"),
            (0, "take a Magic action to exhale a 15-foot Cone"),
            (0, "Dexterity saving throw"),
            (0, "damage increases by 1d6 for each spell slot level above 2"),
        ),
        "required_qualifiers": (
            "Thunder is not a member",
            "recipient a repeatable Magic-action capability",
            "not an immediate caster attack",
            "native support remain NOT_ESTABLISHED",
        ),
    },
    "source.spell.druidcraft.unresolved.plant_and_fire_eligibility": {
        "source_exact_name": "Druidcraft",
        "categories": ("source_mapping_review", "source_parameter"),
        "classification_index": 25,
        "map_entry_index": 37,
        "source_pass_row": 38,
        "body_witness_row": 99,
        "printed_page": 126,
        "source_header_line": 10901,
        "raw_body_sha256": "de059ae3515d9589f7c956818f35a9ef4e62fb7ed8554f61bb3668146839789e",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Druidcraft", "line_start": 11257, "line_end": 11277},
            {"heading": "Duration", "line_start": 9205, "line_end": 9219},
        ],
        "required_source_phrases": (
            (0, "flower blossom, a seed pod open, or a leaf bud bloom"),
            (
                0,
                "Tiny, harmless sensory effect that predicts what the weather will be at your location for the next 24 hours",
            ),
            (0, "This effect persists for 1 round"),
            (0, "must fit in a 5-foot Cube"),
            (0, "light or snuff out a candle, a torch, or a campfire"),
            (
                1,
                "An instantaneous duration means the spell’s magic appears only for a moment",
            ),
        ),
        "required_qualifiers_by_category": {
            "source_mapping_review": (
                "only the named flower, seed-pod and leaf-bud Bloom forms",
                "only lighting or snuffing the named candle, torch and campfire forms",
                "No arbitrary plant growth",
            ),
            "source_parameter": (
                "Cube restriction on harmless Sensory Effect only",
                "Tiny harmless forecast",
                "one round",
                "explicit lifetime",
                "not as a global Druidcraft limit",
            ),
        },
    },
    "source.spell.enhance_ability.unresolved.five_ability_members": {
        "source_exact_name": "Enhance Ability",
        "category": "source_mapping_review",
        "classification_index": 26,
        "map_entry_index": 39,
        "source_pass_row": 41,
        "body_witness_row": 103,
        "printed_page": 127,
        "source_header_line": 11000,
        "raw_body_sha256": "6fe763535996d5c1e5ca28202e6fc4b80d437bbb5876379c6f8ac9aba761a020",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Enhance Ability", "line_start": 11347, "line_end": 11361}
        ],
        "required_source_phrases": (
            (0, "choose Strength, Dexterity, Intelligence, Wisdom, or Charisma"),
            (0, "Advantage on ability checks using the chosen ability"),
            (0, "You can choose a different ability for each target"),
        ),
        "required_qualifiers": (
            "Constitution is not selectable",
            "not attacks or saving throws",
            "No willingness, saving-throw prerequisite",
        ),
    },
    "source.spell.enlarge_reduce.unresolved.mode_exact_modifiers": {
        "source_exact_name": "Enlarge/Reduce",
        "category": "source_parameter",
        "classification_index": 27,
        "map_entry_index": 40,
        "source_pass_row": 42,
        "body_witness_row": 104,
        "printed_page": 127,
        "source_header_line": 11014,
        "raw_body_sha256": "036b77513b31c9c822aade79e3ee3518ca3d9ea59e024ff989e11498522280a0",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Enlarge/Reduce", "line_start": 11365, "line_end": 11383},
            {"heading": "Damage Rolls", "line_start": 1396, "line_end": 1400},
        ],
        "required_source_phrases": (
            (0, "size increases by one category"),
            (
                0,
                "attacks with its enlarged weapons or Unarmed Strikes deal an extra 1d4 damage on a hit",
            ),
            (
                0,
                "attacks with its reduced weapons or Unarmed Strikes deal 1d4 less damage on a hit",
            ),
            (0, "can’t reduce the damage below 1"),
            (1, "it’s possible to deal 0 damage but not negative damage"),
        ),
        "required_qualifiers": (
            "not a doubled/halved dimension or weight",
            "only qualifying weapon or Unarmed Strike hits",
            "specific damage floor of 1",
            "does not establish immunity bypass",
        ),
    },
    "source.spell.feather_fall.unresolved.descent_rate": {
        "source_exact_name": "Feather Fall",
        "category": "source_parameter",
        "classification_index": 28,
        "map_entry_index": 47,
        "source_pass_row": 49,
        "body_witness_row": 116,
        "printed_page": 130,
        "source_header_line": 11229,
        "raw_body_sha256": "19861be011d3111781160ea69876e5523ce6dba9c7688b089abb004657fc380b",
        "classification_status": "SOURCE_LEVEL_OPEN",
        "disposition": "SOURCE_CLOSED",
        "locators": [
            {"heading": "Feather Fall", "line_start": 11593, "line_end": 11605},
            {"heading": "Falling [Hazard]", "line_start": 16593, "line_end": 16597},
            {"heading": "Duration", "line_start": 9205, "line_end": 9213},
            {"heading": "Targets", "line_start": 9223, "line_end": 9227},
        ],
        "shared_common_source_requirement_key": "source.common.target_clear_path",
        "shared_common_source_record_ref": {
            "artifact_id": "source-pass-0-2",
            "json_pointer": "/common_obligations/0",
        },
        "retained_prefix": "NONE_FOR_SELECTED_DESCENT_RATE_AND_DURATION_ONLY",
        "required_source_phrases": (
            (0, "you or a creature you can see within 60 feet of you falls"),
            (0, "Choose up to five falling creatures within range"),
            (0, "slows to 60 feet per round until the spell ends"),
            (0, "the spell ends for that creature"),
            (1, "unless it avoids taking any damage from the fall"),
            (
                2,
                "you can dismiss it (no action required) if you don’t have the Incapacitated condition",
            ),
            (3, "it can’t be behind Total Cover"),
        ),
        "required_qualifiers": (
            "do not copy trigger visibility",
            "source.common.target_clear_path",
            "clear path",
            "Total Cover",
            "do not infer unrestricted target access",
        ),
    },
}

NEXT12_EVIDENCE_ORDER = (
    (
        "NEXT-01",
        "source.spell.arcanist_s_magic_aura.unresolved.alternate_type_domain",
        "source_mapping_review",
    ),
    (
        "NEXT-02",
        "source.spell.arcanist_s_magic_aura.unresolved.false_aura_choice_domain",
        "source_mapping_review",
    ),
    (
        "NEXT-03",
        "source.spell.chromatic_orb.unresolved.six_damage_type_members",
        "source_mapping_review",
    ),
    (
        "NEXT-04",
        "source.spell.detect_evil_and_good.unresolved.supernatural_type_members",
        "source_mapping_review",
    ),
    (
        "NEXT-05",
        "source.spell.detect_magic.unresolved.aura_overlay_policy",
        "source_semantics",
    ),
    (
        "NEXT-06",
        "source.spell.detect_poison_and_disease.unresolved.barrier_and_catalog_domain",
        "source_parameter",
    ),
    (
        "NEXT-07",
        "source.spell.detect_thoughts.unresolved.deeper_failure_disclosure",
        "source_semantics",
    ),
    (
        "NEXT-08",
        "source.spell.dragon_s_breath.unresolved.five_damage_type_members",
        "source_mapping_review",
    ),
    (
        "NEXT-09A",
        "source.spell.druidcraft.unresolved.plant_and_fire_eligibility",
        "source_mapping_review",
    ),
    (
        "NEXT-09B",
        "source.spell.druidcraft.unresolved.plant_and_fire_eligibility",
        "source_parameter",
    ),
    (
        "NEXT-10",
        "source.spell.enhance_ability.unresolved.five_ability_members",
        "source_mapping_review",
    ),
    (
        "NEXT-11",
        "source.spell.enlarge_reduce.unresolved.mode_exact_modifiers",
        "source_parameter",
    ),
    (
        "NEXT-12",
        "source.spell.feather_fall.unresolved.descent_rate",
        "source_parameter",
    ),
)
NEXT12_SELECTED_KEYS = tuple(dict.fromkeys(key for _, key, _ in NEXT12_EVIDENCE_ORDER))
NEXT12_SOURCE_CLOSED_KEYS = frozenset(
    key
    for key, item in NEXT12_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_CLOSED"
)
NEXT12_SOURCE_HELD_KEYS = frozenset(
    key
    for key, item in NEXT12_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_HELD"
)
NEXT12_REQUIRED_EVIDENCE_TOKENS = (
    "ee747f131a118932fbe73d3c1136bbf72d1e6cd5c76f93ee06ac6a03d1259fb6",
    "f6e5c36af4b8b2e4abff78d0083f2eecec79271375ec50af901591f772908bf8",
    "e12bdbe94481c9cd757fd15dfc7966c34fcb576e9350a1099b521cd66715d4bd",
    "on its own turn",
    "source.common.target_clear_path",
    "Total Cover",
    "F12-01 incorporation",
    "does not claim the coordinator's original working checkout is currently clean",
)
SOURCE_THIRD12_EVIDENCE_RELATIVE_PATH = (
    "DEV/docs/superpowers/design/2026-10-09-sp00-third-markdown-source-qualification.md"
)
SOURCE_THIRD12_EVIDENCE_SHA256 = (
    "b7aaf272827328ffa1542cc1c26fed4f0d68fcc8f11405b1763b36e7d834504f"
)
THIRD12_REVIEW = {
    "review_id": "SP00_THIRD_RESIDUALS_REVIEW_20261008",
    "integration_base_sha": "84e3f23020e6d7bdf582222573f96a2901d53dee",
    "candidate_source_base_sha": "061cbe7f9ae4ee7148f62c89c30ea0917aeccc02",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-third-residuals-20261008.json",
    "candidate_sha256": "3e8ed04871f835bb8ec4ab2fd4070fbb219d8a77373b459f5bdef35970984099",
    "candidate_summary_path": "/tmp/hdm-dev/spell-recovery/SP00-third-residuals-20261008.md",
    "candidate_summary_sha256": "5f5f3d448088c92a67e833933d3d4cd1a80ee7a1d768696d028b50be6bd26c62",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-third-residuals-review-20261008.md",
    "accepted_review_sha256": "0921119d7f91c71ee8251fac229b6c2f5d586eedcddadc439e0eb1dd3545ed9d",
    "task_evidence_path": SOURCE_THIRD12_EVIDENCE_RELATIVE_PATH,
    "task_evidence_sha256": SOURCE_THIRD12_EVIDENCE_SHA256,
}
THIRD12_COMMON_MARKDOWN_LOCATORS = [
    {"heading": "Range", "line_start": 9165, "line_end": 9175},
    {"heading": "Duration", "line_start": 9205, "line_end": 9213},
    {"heading": "Effects", "line_start": 9217, "line_end": 9219},
    {"heading": "Targets", "line_start": 9223, "line_end": 9227},
    {"heading": "Area of Effect", "line_start": 16087, "line_end": 16095},
    {"heading": "Concentration", "line_start": 16296, "line_end": 16304},
    {"heading": "Combining Spell Effects", "line_start": 9255, "line_end": 9257},
]
THIRD12_COMMON_QUALIFIERS = [
    "Clear path to a targeted subject is required; Total Cover prevents targeting (9223-9227). Absent repeated visibility never grants through-cover targeting. Area membership/cover realization is not proved.",
    "Range limits origin as the description specifies; movable effects are not generally range-leashed absent an explicit spell restriction (9165-9175).",
    "Effects beyond source statements remain GM purview (9217-9219); no numeric, actor-kind, choice, turn or damage default fills missing semantic proof.",
    "Concentration is a maximum, not guaranteed persistence: creator may end it without action; another concentration effect, Incapacitated/dead creator, or failed damage save ends it (16296-16304).",
    "Time-span spells can be dismissed without action by a non-Incapacitated caster (9205-9213).",
    "Same-spell effects do not combine; most potent applies, then most recent if equal, while durations overlap (9255-9257). Different-spell coexistence does not prove downstream ordering.",
    "No source choice name in this candidate is an admitted recipe/machine/native identifier. Every whole-map, support, admission, execution, recovery, disclosure and performance proof remains NOT_ESTABLISHED.",
]
THIRD12_EVIDENCE_ORDER = (
    (
        "THIRD-01",
        "source.spell.find_familiar.unresolved.override_type_members",
        "source_mapping_review",
    ),
    (
        "THIRD-02",
        "source.spell.find_traps.unresolved.magical_trap_examples",
        "source_mapping_review",
    ),
    (
        "THIRD-03",
        "source.spell.flaming_sphere.unresolved.geometry_bounds",
        "source_parameter",
    ),
    (
        "THIRD-04",
        "source.spell.floating_disk.unresolved.disk_numeric_limits",
        "source_parameter",
    ),
    (
        "THIRD-05",
        "source.spell.fog_cloud.unresolved.strong_wind_judgment",
        "source_semantics",
    ),
    (
        "THIRD-06",
        "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
        "source_semantics",
    ),
    (
        "THIRD-07",
        "source.spell.guidance.unresolved.skill_domain",
        "source_mapping_review",
    ),
    (
        "THIRD-08",
        "source.spell.gust_of_wind.unresolved.wind_numeric_profile",
        "source_parameter",
    ),
    (
        "THIRD-09",
        "source.spell.hex.unresolved.ability_member_domain",
        "source_mapping_review",
    ),
    ("THIRD-10", "source.spell.hex.unresolved.duration_bands", "source_parameter"),
    (
        "THIRD-11",
        "source.spell.hunter_s_mark.unresolved.duration_bands",
        "source_parameter",
    ),
    ("THIRD-12", "source.spell.jump.unresolved.jump_distance_cost", "source_parameter"),
)
THIRD12_SELECTED_KEYS = tuple(key for _, key, _ in THIRD12_EVIDENCE_ORDER)
THIRD12_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.find_familiar.unresolved.override_type_members": {
        "source_exact_name": "Find Familiar",
        "category": "source_mapping_review",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 29,
        "map_entry_index": 48,
        "source_pass_row": 50,
        "body_witness_row": 117,
        "printed_page": 130,
        "source_header_line": 11241,
        "raw_body_sha256": "7ad9e1e88ac2c18e7f7573442ad84ecab53c842c4f0d22616cfd1b446215aac6",
        "locators": [
            {"heading": "Find Familiar", "line_start": 11609, "line_end": 11629}
        ],
        "source_phrases": (
            (0, "Celestial, Fey, or Fiend"),
            (0, "within 100 feet of you"),
            (0, "take a Reaction to deliver the touch"),
            (0, "leaves behind in its space anything it was wearing or carrying"),
        ),
        "required_qualifiers": (
            "not the completed form census",
            "not create that restriction",
            "within100 feet and its Reaction",
            "zeroHP or pocket disappearance",
            "no invented permanent-dismissal gear rule",
        ),
        "members": ["Celestial", "Fey", "Fiend"],
    },
    "source.spell.find_traps.unresolved.magical_trap_examples": {
        "source_exact_name": "Find Traps",
        "category": "source_mapping_review",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 33,
        "map_entry_index": 50,
        "source_pass_row": 52,
        "body_witness_row": 119,
        "printed_page": 131,
        "source_header_line": 11313,
        "raw_body_sha256": "76a88e76bd6f5df2d688064a529fccf7c6eabf3cb1cd8c527644ed9cf81f8068",
        "locators": [{"heading": "Find Traps", "line_start": 11718, "line_end": 11732}],
        "source_phrases": (
            (0, "within line of sight"),
            (0, "created to cause damage or other danger"),
            (0, "Alarm"),
            (0, "Glyph of Warding"),
            (0, "mechanical pit trap"),
            (0, "not its location"),
        ),
        "required_qualifiers": (
            "examples, not an exhaustive catalog",
            "line of sight",
            "not trap location",
            "Natural floor weakness",
        ),
    },
    "source.spell.flaming_sphere.unresolved.geometry_bounds": {
        "source_exact_name": "Flaming Sphere",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 34,
        "map_entry_index": 53,
        "source_pass_row": 55,
        "body_witness_row": 128,
        "printed_page": 132,
        "source_header_line": 11474,
        "raw_body_sha256": "302ebd4433a46a10b817f6ff8bfdb652a78e760f8fb5ce3308b0a820bcf4a49a",
        "locators": [
            {"heading": "Flaming Sphere", "line_start": 11866, "line_end": 11882},
            {"heading": "Range", "line_start": 9165, "line_end": 9175},
        ],
        "source_phrases": (
            (0, "5-foot-diameter"),
            (0, "within 5 feet"),
            (0, "2d6 Fire"),
            (0, "up to 30 feet"),
            (0, "up to 5 feet tall"),
            (0, "up to 10 feet wide"),
            (0, "aren’t being worn or carried"),
        ),
        "required_qualifiers": (
            "Diameter is not radius",
            "not an invented ongoing leash",
            "Collision and nearby end-turn events remain distinct",
            "no universal once-per-turn damage cap",
            "neither worn nor carried",
        ),
    },
    "source.spell.floating_disk.unresolved.disk_numeric_limits": {
        "source_exact_name": "Floating Disk",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 35,
        "map_entry_index": 54,
        "source_pass_row": 56,
        "body_witness_row": 130,
        "printed_page": 133,
        "source_header_line": 11515,
        "raw_body_sha256": "24d5b9598689bf0dd79188ea1b112e0af252b7ceaad7a7d2a76d2fd8796086e0",
        "locators": [
            {"heading": "Floating Disk", "line_start": 11904, "line_end": 11918},
            {"heading": "Duration", "line_start": 9205, "line_end": 9213},
        ],
        "source_phrases": (
            (0, "3 feet in diameter and 1 inch thick"),
            (0, "floats 3 feet above the ground"),
            (0, "within range"),
            (0, "up to 500 pounds"),
            (0, "more than 20 feet away"),
            (0, "10 feet or more"),
            (0, "more than 100 feet"),
        ),
        "required_qualifiers": (
            "500 pounds/20 feet/100 feet equality alone does not trigger",
            "10-foot elevation equality does bar crossing",
            "Overload expressly drops contents",
            "Other termination/fall placement",
        ),
    },
    "source.spell.fog_cloud.unresolved.strong_wind_judgment": {
        "source_exact_name": "Fog Cloud",
        "category": "source_semantics",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 36,
        "map_entry_index": 55,
        "source_pass_row": 57,
        "body_witness_row": 132,
        "printed_page": 133,
        "source_header_line": 11550,
        "raw_body_sha256": "ac0631a710bf18d7ea01b794c1a7427599384740aa4e914687ac6061b082eb67",
        "locators": [
            {"heading": "Fog Cloud", "line_start": 11940, "line_end": 11954},
            {"heading": "Gust of Wind", "line_start": 12417, "line_end": 12431},
            {"heading": "Strong Wind", "line_start": 17693, "line_end": 17697},
            {"heading": "Effects", "line_start": 9217, "line_end": 9219},
        ],
        "source_phrases": (
            (0, "20-foot-radius Sphere"),
            (0, "strong wind"),
            (0, "Gust of Wind"),
            (0, "radius increases by 20 feet"),
            (1, "Line of strong wind"),
        ),
        "required_qualifiers": (
            "qualitative predicate, not a speed threshold",
            "Other wind strength is GM scene judgment",
            "whole-cloud versus partial-overlap implementation rule",
            "not acceptance of a particular scene wind fact",
        ),
    },
    "source.spell.gentle_repose.unresolved.corpse_and_revival_binding": {
        "source_exact_name": "Gentle Repose",
        "category": "source_semantics",
        "disposition": "SOURCE_HELD",
        "classification_index": 37,
        "map_entry_index": 56,
        "source_pass_row": 58,
        "body_witness_row": 141,
        "printed_page": 135,
        "source_header_line": 11749,
        "raw_body_sha256": "72f180622ffb4cd5c343a0d87ba79e0f6cfba5e392f24575c248fc72ce7673dd",
        "locators": [
            {"heading": "Gentle Repose", "line_start": 12108, "line_end": 12122},
            {"heading": "Duration", "line_start": 9205, "line_end": 9213},
            {
                "heading": "Combining Spell Effects",
                "line_start": 9255,
                "line_end": 9257,
            },
            {"heading": "Raise Dead", "line_start": 14236, "line_end": 14250},
        ],
        "source_phrases": (
            (0, "corpse or other remains"),
            (0, "protected from decay"),
            (0, "can’t become Undead"),
            (0, "days spent under the influence of this spell don’t count"),
            (3, "Raise Dead"),
        ),
        "required_qualifiers": (
            "not global chronology pause",
            "Raise Dead requires death no longer than10 days",
            "exact body-identity binding",
            "No semantic default chosen",
            "separate downstream_domain_consumer_admission_native_proof",
        ),
    },
    "source.spell.guidance.unresolved.skill_domain": {
        "source_exact_name": "Guidance",
        "category": "source_mapping_review",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 38,
        "map_entry_index": 59,
        "source_pass_row": 61,
        "body_witness_row": 152,
        "printed_page": 138,
        "source_header_line": 12004,
        "raw_body_sha256": "d844c7a9a6d1a5c680c6e7057356623a126d19eb0754d4b74603e40a08a1b733",
        "locators": [
            {"heading": "Guidance", "line_start": 12383, "line_end": 12395},
            {"heading": "Skill Proficiencies", "line_start": 833, "line_end": 868},
            {
                "heading": "Combining Spell Effects",
                "line_start": 9255,
                "line_end": 9257,
            },
        ],
        "source_phrases": (
            (0, "willing creature"),
            (0, "choose a skill"),
            (0, "adds 1d4 to any ability check using the chosen skill"),
            (1, "Acrobatics"),
            (1, "Survival"),
        ),
        "required_qualifiers": (
            "No proficiency prerequisite",
            "Repeated qualifying checks",
            "not an exclusive matching-ability restriction",
            "No tool choice or extra nineteenth skill",
        ),
        "members": [
            "Acrobatics",
            "Animal Handling",
            "Arcana",
            "Athletics",
            "Deception",
            "History",
            "Insight",
            "Intimidation",
            "Investigation",
            "Medicine",
            "Nature",
            "Perception",
            "Performance",
            "Persuasion",
            "Religion",
            "Sleight of Hand",
            "Stealth",
            "Survival",
        ],
    },
    "source.spell.gust_of_wind.unresolved.wind_numeric_profile": {
        "source_exact_name": "Gust of Wind",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 39,
        "map_entry_index": 61,
        "source_pass_row": 63,
        "body_witness_row": 154,
        "printed_page": 138,
        "source_header_line": 12024,
        "raw_body_sha256": "e250e6255bc7969a01417ec41312795906db25902a2d1f3d022a81df927aa0d8",
        "locators": [
            {"heading": "Gust of Wind", "line_start": 12417, "line_end": 12431},
            {"heading": "Line", "line_start": 16841, "line_end": 16845},
        ],
        "source_phrases": (
            (0, "Line of strong wind 60 feet long and 10 feet wide"),
            (0, "pushed 15 feet away"),
            (0, "spend 2 feet of movement for every 1 foot"),
            (0, "on your later turns"),
            (0, "50 percent chance to extinguish them"),
        ),
        "required_qualifiers": (
            "later turns",
            "Initial and end-turn saves remain distinct",
            "No arbitrary save-on-entry",
            "Closer-to-caster movement predicate is not all movement",
            "wind-speed value inferred",
        ),
    },
    "source.spell.hex.unresolved.ability_member_domain": {
        "source_exact_name": "Hex",
        "category": "source_mapping_review",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 40,
        "map_entry_index": 66,
        "source_pass_row": 68,
        "body_witness_row": 165,
        "printed_page": 140,
        "source_header_line": 12220,
        "raw_body_sha256": "df12f3cda388af329ebf931ae0502b5d98a19a6e56f52af8e4fc22391e6207e3",
        "locators": [
            {"heading": "Hex", "line_start": 12637, "line_end": 12653},
            {"heading": "Ability Descriptions", "line_start": 535, "line_end": 544},
        ],
        "source_phrases": (
            (0, "choose one ability when you cast the spell"),
            (0, "ability checks made with the chosen ability"),
            (0, "drops to 0 Hit Points"),
            (0, "on a later turn"),
            (1, "Constitution"),
        ),
        "required_qualifiers": (
            "Constitution is included",
            "not skill or saving throw",
            "caster attack-roll hit",
            "on a later turn",
            "no death prerequisite",
            "no unrestricted transfer",
            "no freely repeatable ability reselection",
        ),
        "members": [
            "Strength",
            "Dexterity",
            "Constitution",
            "Intelligence",
            "Wisdom",
            "Charisma",
        ],
    },
    "source.spell.hex.unresolved.duration_bands": {
        "source_exact_name": "Hex",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 41,
        "map_entry_index": 66,
        "source_pass_row": 68,
        "body_witness_row": 165,
        "printed_page": 140,
        "source_header_line": 12220,
        "raw_body_sha256": "df12f3cda388af329ebf931ae0502b5d98a19a6e56f52af8e4fc22391e6207e3",
        "locators": [
            {"heading": "Hex", "line_start": 12637, "line_end": 12653},
            {"heading": "Concentration", "line_start": 16296, "line_end": 16304},
            {
                "heading": "Using a Higher-Level Spell Slot",
                "line_start": 9106,
                "line_end": 9110,
            },
        ],
        "source_phrases": (
            (0, "up to 1 hour"),
            (0, "level 2 (up to 4 hours)"),
            (0, "3–4 (up to 8 hours)"),
            (0, "5+ (24 hours)"),
        ),
        "required_qualifiers": (
            "slot2 has its own4-hour band",
            "maximum concentration lifetimes",
            "Transfer uses continuing original spell episode",
            "do not import Hunter's Mark",
        ),
        "duration_hours_by_slot": {
            "1": 1,
            "2": 4,
            "3": 8,
            "4": 8,
            "5": 24,
            "6": 24,
            "7": 24,
            "8": 24,
            "9": 24,
        },
    },
    "source.spell.hunter_s_mark.unresolved.duration_bands": {
        "source_exact_name": "Hunter’s Mark",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 42,
        "map_entry_index": 69,
        "source_pass_row": 71,
        "body_witness_row": 170,
        "printed_page": 141,
        "source_header_line": 12299,
        "raw_body_sha256": "3b0fe49e69de7ead35d81cdf685039b1ce31d41238458d91facd84c1ae08a43d",
        "locators": [
            {"heading": "Hunter’s Mark", "line_start": 12729, "line_end": 12745},
            {"heading": "Concentration", "line_start": 16296, "line_end": 16304},
            {
                "heading": "Using a Higher-Level Spell Slot",
                "line_start": 9106,
                "line_end": 9110,
            },
        ],
        "source_phrases": (
            (0, "one creature you can see within range"),
            (0, "extra 1d6 Force damage"),
            (0, "Bonus Action to move the mark"),
            (0, "level 3–4 (up to 8 hours)"),
            (0, "5+ (up to 24 hours)"),
        ),
        "required_qualifiers": (
            "Slots1-2",
            "Slot2 has no Hex-like4-hour increase",
            "find this target",
            "Unlike Hex no later-turn restriction is stated",
            "ordinary Bonus Action entitlement still applies",
        ),
        "duration_hours_by_slot": {
            "1": 1,
            "2": 1,
            "3": 8,
            "4": 8,
            "5": 24,
            "6": 24,
            "7": 24,
            "8": 24,
            "9": 24,
        },
    },
    "source.spell.jump.unresolved.jump_distance_cost": {
        "source_exact_name": "Jump",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 43,
        "map_entry_index": 75,
        "source_pass_row": 77,
        "body_witness_row": 183,
        "printed_page": 143,
        "source_header_line": 12533,
        "raw_body_sha256": "74e5149b5098fe7446df95ef3ef64bdd23fefe7de49b77d67f03a66d1bffaa13",
        "locators": [
            {"heading": "Jump", "line_start": 12983, "line_end": 12997},
            {"heading": "Duration", "line_start": 9205, "line_end": 9213},
            {"heading": "Jumping", "line_start": 16821, "line_end": 16823},
        ],
        "source_phrases": (
            (0, "Once on each of its turns"),
            (0, "jump up to 30 feet by spending 10 feet of movement"),
            (0, "one additional creature"),
        ),
        "required_qualifiers": (
            "spending10 feet",
            "Own-turn restriction excludes arbitrary off-turn uses",
            "not a proportional1-for3 conversion",
            "No guaranteed jump per turn without movement available",
            "no extra action",
        ),
    },
}
THIRD12_SOURCE_CLOSED_KEYS = frozenset(
    key
    for key, item in THIRD12_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_CLOSED"
)
THIRD12_SOURCE_HELD_KEYS = frozenset(
    key
    for key, item in THIRD12_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_HELD"
)
THIRD12_REQUIRED_EVIDENCE_TOKENS = (
    THIRD12_REVIEW["candidate_sha256"],
    THIRD12_REVIEW["candidate_summary_sha256"],
    THIRD12_REVIEW["accepted_review_sha256"],
    "**I01 — Find Familiar:**",
    "not a universal command leash",
    "zero-HP or pocket-dimension disappearance only",
    "**I02 — common range, cover and qualitative wind:**",
    "Total Cover at 9223–9227",
    "area-origin / line-of-effect membership and origin placement at 16087–16095",
    "Strong wind remains qualitative",
    "**I03 — actors, negative guards, timing and repeated occurrences:**",
    "Hex later-turn versus Hunter's lack of that restriction",
    "**I04 — additive evidence and totals:**",
    "24 prior qualified keys / 20 closed keys / 21 closed subobligations / 4 held",
    "conditional cumulative totals are 36 qualified / 31 closed keys / 32 closed subobligations / 5 held",
    "46 active source keys",
    "W05_SPELL_SOURCE_QUALIFICATION_READY",
    *THIRD12_SELECTED_KEYS,
)

FOURTH_REVIEW: dict[str, str] = {
    "review_id": "SP00_FOURTH_SOURCE_REVIEW_20261013",
    "integration_base_sha": "7ba417d6c8eda10efb30f1cef0459e70d1b56dfc",
    "candidate_source_base_sha": "7ba417d6c8eda10efb30f1cef0459e70d1b56dfc",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-fourth-source-extraction-20261013.md",
    "candidate_sha256": "22f1a64da0054a2680ed3cdae07ab2e144e881f48d0463b9caea0569dcf692ab",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-fourth-source-review-20261013.md",
    "accepted_review_sha256": "859b26ecbf27ab0234c45277c6deea76474bc6134ed1675ed496ba0a8678780a",
    "task_evidence_path": "DEV/docs/superpowers/design/2026-10-13-sp00-fourth-markdown-source-qualification.md",
    "task_evidence_sha256": "fdf603e6e3ba3a53f787441f660f4e6b5d358fb070c2160b30cf741f34bacb5d",
}
FOURTH_SELECTED_CLASSIFICATION_INDEXES = (44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55)
FOURTH_EVIDENCE_ORDER = (
    (
        "FOURTH-01",
        "source.spell.knock.unresolved.knock_sound_range",
        "source_parameter",
    ),
    (
        "FOURTH-02",
        "source.spell.levitate.unresolved.altitude_mass_bounds",
        "source_parameter",
    ),
    (
        "FOURTH-03",
        "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain",
        "source_mapping_review",
    ),
    (
        "FOURTH-04",
        "source.spell.locate_object.unresolved.current_query_consumer",
        "source_semantics",
    ),
    (
        "FOURTH-05",
        "source.spell.longstrider.unresolved.speed_composition",
        "source_semantics",
    ),
    (
        "FOURTH-06",
        "source.spell.mage_armor.unresolved.ac_base_formula",
        "source_parameter",
    ),
    (
        "FOURTH-07",
        "source.spell.mage_hand.unresolved.hand_bounds_and_eligibility",
        "source_parameter",
    ),
    (
        "FOURTH-08",
        "source.spell.magic_missile.unresolved.rng_damage_grouping",
        "source_semantics",
    ),
    (
        "FOURTH-09",
        "source.spell.magic_mouth.unresolved.trigger_episode_frequency",
        "source_semantics",
    ),
    (
        "FOURTH-10",
        "source.spell.magic_mouth.unresolved.message_word_bound",
        "source_parameter",
    ),
    (
        "FOURTH-11",
        "source.spell.magic_weapon.unresolved.bonus_band_numbers",
        "source_parameter",
    ),
)
FOURTH_SELECTED_KEYS = tuple(key for _, key, _ in FOURTH_EVIDENCE_ORDER)
FOURTH_COMMON_MARKDOWN_LOCATORS: tuple[dict[str, object], ...] = (
    {
        "heading": "Casting Spells",
        "line_start": 9068,
        "line_end": 9257,
        "span_sha256": "48ccc959d306e2f349b56e2dea465f9b119c47d414105011fc44104384aa0702",
    },
    {
        "heading": "Class Spell Lists",
        "line_start": 9133,
        "line_end": 9137,
        "span_sha256": "53cf80604eb60606f14e297d71f48bd0b5ccce68f333f5343f9fb34876873eba",
    },
    {
        "heading": "Reaction and Bonus Action Triggers",
        "line_start": 9151,
        "line_end": 9155,
        "span_sha256": "47c13792c1488cfeb403525e6a145fb5dc9cb844bf2a981c7443884b2dc2fb13",
    },
    {
        "heading": "Damage Rolls",
        "line_start": 1396,
        "line_end": 1400,
        "span_sha256": "3bab0640f9638faa8e732906e9ad79fb1941a7cbcfd1bba78b1e8bf69124ac15",
    },
    {
        "heading": "Climbing",
        "line_start": 16282,
        "line_end": 16304,
        "span_sha256": "e0f43114f314cad41d4a9c97e2524c4fed62af077df7852feb5d2f1a963f1a76",
    },
    {
        "heading": "Speed",
        "line_start": 17163,
        "line_end": 17169,
        "span_sha256": "033e5886f45fe2767f324130b4d4cbcc6f4a27e8f7368fb8bb4e30bf4c9b3f15",
    },
    {
        "heading": "Armor Class",
        "line_start": 16099,
        "line_end": 16103,
        "span_sha256": "9ee7bf2f3b3029d8c9408c0143e643762ced1360721a772cfe0292eeff171b49",
    },
    {
        "heading": "Creature Type",
        "line_start": 16344,
        "line_end": 16350,
        "span_sha256": "d2b33fa78917f0ba98ee90a1e114737589ce71c6c365e4a7279c19a19b6ab6fe",
    },
    {
        "heading": "Magic [Action]",
        "line_start": 16887,
        "line_end": 16891,
        "span_sha256": "c058c7161a70af3ac580fd1ce30766347d64288b2a58f0c430a1c31852056565",
    },
    {
        "heading": "Shield",
        "line_start": 14703,
        "line_end": 14715,
        "span_sha256": "156ada53007c0b34b674048e9d977b157a7dd1794c56871586e84702951ad965",
    },
)
FOURTH_COMMON_QUALIFIERS = (
    "Clear path to a targeted subject is required; Total Cover prevents targeting (9223-9227). Absent repeated visibility never grants through-cover targeting. Area membership/cover realization is not proved.",
    "Range limits origin as the description specifies; movable effects are not generally range-leashed absent an explicit spell restriction (9165-9175).",
    "Effects beyond source statements remain GM purview (9217-9219); no numeric, actor-kind, choice, turn or damage default fills missing semantic proof.",
    "Concentration is a maximum, not guaranteed persistence: creator may end it without action; another concentration effect, Incapacitated/dead creator, or failed damage save ends it (16296-16304).",
    "Time-span spells can be dismissed without action by a non-Incapacitated caster (9205-9213).",
    "Same-spell effects do not combine; most potent applies, then most recent if equal, while durations overlap (9255-9257). Different-spell coexistence does not prove downstream ordering.",
    "No source choice name in this candidate is an admitted recipe/machine/native identifier. Every whole-map, support, admission, execution, recovery, disclosure and performance proof remains NOT_ESTABLISHED.",
    "Armor training is caster legality for casting in armor; it is distinct from Mage Armor target eligibility.",
    "Spell levels are 0–9; schools describe spells but confer no rules themselves unless another rule refers to them.",
    "Some features add a spell to a character’s spell list even if the character isn’t a member of a class in the parentheses. Profile class membership alone is not an exhaustive capability prohibition or proof of an installed casting capability.",
    "A level 1+ spell uses a slot of its level or higher; a higher slot makes that casting the higher level, with only body-specified enhancements. Cantrips require no slot.",
    "Special abilities and magic items can provide distinct limited no-slot paths; profile listing alone neither proves nor denies a particular casting capability.",
    "On a turn, only one spell slot can be expended to cast a spell; this is not a universal one-spell-per-turn prohibition.",
    "A Reaction spell is cast in response to the trigger defined in its Casting Time entry. Some Bonus Action spells also specify a trigger in the spell; Bonus Action casting does not universally require a trigger.",
    "Casting for 1 minute or longer, including Ritual casting, requires a Magic action each turn and Concentration during casting; interruption fails without expending a slot and requires starting over. This is not ongoing Concentration for a resulting nonconcentration effect.",
    "A spell’s range limits where its effect can originate as its description specifies; movable effects are not range-restricted unless the description says otherwise. Preserve explicit Levitate control and Mage Hand separation limits.",
    "All specified components must be supplied. Verbal components require a normal speaking voice; Somatic requires a hand; Material needs a free hand, which can also perform Somatic components.",
    "A pouch/focus can replace Material only when the component is neither consumed nor priced; focus use also requires an authorizing feature and held focus. Magic Mouth’s 10+ GP dust is consumed and excluded from substitution.",
    "Time-span dismissal without action applies only while the caster is not Incapacitated; preserve exact Concentration, Until-dispelled and body-specific early-ending rules.",
    "Target bodies define target kinds; clear path excludes Total Cover. Self-selection applies to a creature of choice unless Hostile/other-than-self is required. Do not add an all-purpose visibility constraint to distant queries.",
    "Unperceived targeting is not known unless perceptible. A valid cast at an invalid target preserves slot cost and prescribed no-effect/apparent-save presentation; unsupported binding is a separate failure and not a free hidden-type probe.",
    "Use only source-specified saves and attack rolls and formulas; do not invent a save for willing Levitate targets/objects or an attack roll for Magic Missile.",
    "Different-spell effects add while durations overlap; repeated same-spell effects do not combine, most potent then most recent applies, and suppressed durations persist. Preserve explicit Mage Hand/Magic Weapon recast endings.",
    "Climbing movement costs and its optional DC 15 check retain their conditions; Climb Speed removes the extra cost when used to climb. Concentration ends on another concentration effect, failed damage save, Incapacitated or death; these are source laws, not execution proof.",
)
FOURTH_COMMON_REQUIRED_PHRASES: dict[str, tuple[str, ...]] = {
    "Casting Spells": (
        "Some features add a spell to a character’s spell list",
        "A spell that has a casting time of a Reaction is cast in response to a trigger",
        "Some spells that have a casting time of a Bonus Action",
        "you can expend only one spell slot",
        "movable effects, they aren’t restricted by its range",
    ),
    "Class Spell Lists": (
        "Some features add a spell to a character’s spell list even if the character isn’t a member of a class in the parentheses.",
    ),
    "Reaction and Bonus Action Triggers": (
        "A spell that has a casting time of a Reaction is cast in response to a trigger",
        "Some spells that have a casting time of a Bonus Action are also cast in response to a trigger",
    ),
    "Damage Rolls": (
        "You roll the damage dice",
        "A spell tells you which dice to roll for damage",
    ),
    "Climbing": (
        "each foot of movement costs 1 extra foot",
        "successful DC 15 Strength (Athletics) check",
        "another effect that requires Concentration",
        "Incapacitated or Dead",
    ),
    "Speed": ("any special speed you have increases or decreases by an equal amount",),
    "Armor Class": (
        "you choose which calculation to use; you can’t use more than one",
    ),
    "Creature Type": ("Beast Fey Ooze Celestial Fiend Plant Construct",),
    "Magic [Action]": ("casting time of 1 minute or longer", "maintain Concentration"),
    "Shield": (
        "targeted by the *Magic Missile* spell",
        "take no damage from *Magic Missile*",
    ),
}
FOURTH_REQUIRED_EVIDENCE_TOKENS = (
    FOURTH_REVIEW["candidate_sha256"],
    FOURTH_REVIEW["accepted_review_sha256"],
    "Original indexes 44–55 contain 11 active source subobligations.",
    "A Reaction spell is cast in response to the trigger defined in its Casting Time entry.",
    "feature-authorized casting",
    "47 reviewed keys",
    "38 active source-blocking keys",
    "W05_SPELL_SOURCE_QUALIFICATION_READY",
)

FOURTH_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.knock.unresolved.knock_sound_range": {
        "source_exact_name": "Knock",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 44,
        "map_entry_index": 76,
        "source_pass_row": 78,
        "body_witness_row": 184,
        "printed_page": 143,
        "source_header_line": 12546,
        "raw_body_sha256": "4da42a5511abfaa432d0fb4d673bd236d1d762f848370cd85513794245ab2245",
        "locators": [
            {
                "heading": "Knock",
                "line_start": 13001,
                "line_end": 13015,
                "span_sha256": "f99c908136fdf9389ae79b0f8fd17830b64181189c588a3a6d4bb07614886e5d",
            }
        ],
        "source_phrases": (
            (0, "audible up to 300 feet away"),
            (0, "emanates from the target"),
            (0, "only one of them is unlocked"),
            (0, "suppressed for 10 minutes"),
        ),
        "required_qualifiers": (
            "audible up to 300 feet away",
            "60-foot casting range",
            "only one lock",
            "suppressed for 10 minutes",
            "not dispelled",
            "not a universal guarantee",
        ),
    },
    "source.spell.levitate.unresolved.altitude_mass_bounds": {
        "source_exact_name": "Levitate",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 46,
        "map_entry_index": 78,
        "source_pass_row": 80,
        "body_witness_row": 187,
        "printed_page": 144,
        "source_header_line": 12589,
        "raw_body_sha256": "20365e640e51818fa0cda79a81a675fc48355f702bfcf2db952051b134bb5190",
        "locators": [
            {
                "heading": "Levitate",
                "line_start": 13053,
                "line_end": 13067,
                "span_sha256": "10f815a8ae653de247bb7b29c36f7f32b2c3ac19310c87793df5891e4f828d56",
            }
        ],
        "source_phrases": (
            (0, "loose object"),
            (0, "up to 500 pounds"),
            (0, "up to 20 feet in either direction on your turn"),
            (0, "which must remain within the spell’s range"),
            (0, "floats gently to the ground"),
        ),
        "required_qualifiers": (
            "one visible creature or loose object",
            "500-pound limit is stated for objects",
            "up to 20 feet",
            "on the caster’s turn",
            "in either direction",
            "Magic action",
            "within spell range",
            "fixed object or surface",
            "floats gently",
            "not free horizontal flight",
        ),
    },
    "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain": {
        "source_exact_name": "Locate Animals or Plants",
        "category": "source_mapping_review",
        "disposition": "SOURCE_HELD",
        "classification_index": 47,
        "map_entry_index": 80,
        "source_pass_row": 82,
        "body_witness_row": 190,
        "printed_page": 144,
        "source_header_line": 12635,
        "raw_body_sha256": "6d80aaa14cac0094cf4f3f5ccb31386a263528fe63da0f3882ab71d59e3e29b8",
        "locators": [
            {
                "heading": "Locate Animals or Plants",
                "line_start": 13107,
                "line_end": 13119,
                "span_sha256": "b63c752076f267ac95c197582ad1c377b80139802f7fbcdefa8b3de1bd14b7bf",
            }
        ],
        "source_phrases": (
            (0, "specific kind of Beast, Plant creature, or nonmagical plant"),
            (0, "within 5 miles"),
            (0, "direction and distance"),
            (0, "if any are present"),
        ),
        "required_qualifiers": (
            "Beast",
            "Plant creature",
            "nonmagical plant",
            "kind",
            "closest",
            "within 5 miles",
            "direction and distance",
            "if any are present",
            "individually named complete creature/plant-kind member census",
        ),
    },
    "source.spell.locate_object.unresolved.current_query_consumer": {
        "source_exact_name": "Locate Object",
        "category": "source_semantics",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 48,
        "map_entry_index": 81,
        "source_pass_row": 83,
        "body_witness_row": 192,
        "printed_page": 145,
        "source_header_line": 12666,
        "raw_body_sha256": "976c5efbfb68ce41ef1ad75f91d27f7378a5e2b452f7b96f166a4de38f84da39",
        "locators": [
            {
                "heading": "Locate Object",
                "line_start": 13141,
                "line_end": 13155,
                "span_sha256": "ffdf344ad5c004120951a03582c62dddf4d2c021b9b28d9d63e88acd85dd36d5",
            }
        ],
        "source_phrases": (
            (0, "object that is familiar to you"),
            (0, "within 30 feet"),
            (0, "nearest object of a particular kind"),
            (0, "direction of its movement"),
            (0, "any thickness of lead"),
        ),
        "required_qualifiers": (
            "familiar description/name",
            "specific object known",
            "seen up close within 30 feet",
            "alternative nearest-kind query",
            "within 1,000 feet",
            "direction",
            "not distance",
            "any thickness of lead",
            "not an extra visibility requirement",
        ),
    },
    "source.spell.longstrider.unresolved.speed_composition": {
        "source_exact_name": "Longstrider",
        "category": "source_semantics",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 49,
        "map_entry_index": 82,
        "source_pass_row": 84,
        "body_witness_row": 193,
        "printed_page": 145,
        "source_header_line": 12685,
        "raw_body_sha256": "1c8b4f15108865068b21aa07b40eeb20b174b6af434ce9e4151eba89f3e66d80",
        "locators": [
            {
                "heading": "Longstrider",
                "line_start": 13159,
                "line_end": 13173,
                "span_sha256": "773849548bc7a17fe67217c537b02fc3460ee427b1bf89b1ec9e4374b09ef7fe",
            }
        ],
        "source_phrases": (
            (0, "Speed increases by 10 feet"),
            (0, "one additional creature for each spell slot level above 1"),
        ),
        "required_qualifiers": (
            "one +10-foot Speed increase",
            "one hour",
            "one additional creature",
            "equal temporary Speed increase",
            "same duration",
            "each existing special speed",
            "not independent per-mode bonuses",
            "no new movement mode",
        ),
    },
    "source.spell.mage_armor.unresolved.ac_base_formula": {
        "source_exact_name": "Mage Armor",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 50,
        "map_entry_index": 83,
        "source_pass_row": 85,
        "body_witness_row": 194,
        "printed_page": 145,
        "source_header_line": 12696,
        "raw_body_sha256": "8fa168e51979a0c83e202912ebe0a3dee540fe6e15a9fe0a57d071f47cdada23",
        "locators": [
            {
                "heading": "Mage Armor",
                "line_start": 13177,
                "line_end": 13189,
                "span_sha256": "e7ecbb88b000f22b1d5341210214c7e7b87b7d52f5b8b70f6f017b01ec642c7e",
            }
        ],
        "source_phrases": (
            (0, "willing creature who isn’t wearing armor"),
            (0, "base AC becomes 13 plus its Dexterity modifier"),
            (0, "ends early if the target dons armor"),
        ),
        "required_qualifiers": (
            "13 plus its Dexterity modifier",
            "base calculation",
            "not an additive +13 bonus",
            "willing creature",
            "not wearing armor",
            "8 hours",
            "dons armor",
            "only one base calculation",
            "no claim that Shield use ends",
        ),
    },
    "source.spell.mage_hand.unresolved.hand_bounds_and_eligibility": {
        "source_exact_name": "Mage Hand",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 51,
        "map_entry_index": 84,
        "source_pass_row": 86,
        "body_witness_row": 195,
        "printed_page": 145,
        "source_header_line": 12705,
        "raw_body_sha256": "20f9d0951f32eeee8ba362a3db21121753361970c861d76ee134bd5260f7ae15",
        "locators": [
            {
                "heading": "Mage Hand",
                "line_start": 13193,
                "line_end": 13207,
                "span_sha256": "78fbb06b382d9319772137a4d9054f361ae301d423990eaed2eb3403a958eaeb",
            }
        ],
        "source_phrases": (
            (0, "more than 30 feet away from you"),
            (0, "As a Magic action on your later turns"),
            (0, "up to 30 feet"),
            (0, "can’t attack, activate magic items, or carry more than 10 pounds"),
        ),
        "required_qualifiers": (
            "within 30 feet",
            "ever more than 30 feet",
            "during casting without an extra action",
            "later control is a Magic action",
            "up to 30 feet of movement",
            "unlocked",
            "open container",
            "pouring is limited to vial contents",
            "cannot attack",
            "activate magic items",
            "more than 10 pounds",
            "source permission to manipulate objects is not removed",
        ),
    },
    "source.spell.magic_missile.unresolved.rng_damage_grouping": {
        "source_exact_name": "Magic Missile",
        "category": "source_semantics",
        "disposition": "SOURCE_HELD",
        "classification_index": 52,
        "map_entry_index": 85,
        "source_pass_row": 87,
        "body_witness_row": 198,
        "printed_page": 146,
        "source_header_line": 12789,
        "raw_body_sha256": "0f691800c3e9c5664ebd220ade84cb02ffff15989cecfa111fb365835724019c",
        "locators": [
            {
                "heading": "Magic Missile",
                "line_start": 13259,
                "line_end": 13273,
                "span_sha256": "e772f726833c5dcb9d05591eeb8537634ea860acf3412da63fb95599182b2a0d",
            }
        ],
        "source_phrases": (
            (0, "three glowing darts"),
            (0, "creature of your choice that you can see within range"),
            (0, "1d4 + 1 Force damage"),
            (0, "all strike simultaneously"),
            (0, "one more dart for each spell slot level above 1"),
        ),
        "required_qualifiers": (
            "three darts",
            "visible creature within 120 feet",
            "deals 1d4 + 1 Force damage",
            "simultaneously",
            "one creature or several",
            "one dart per level above 1",
            "body specifies no attack roll or saving throw",
            "prevents Magic Missile damage",
            "shared-versus-separate dart dice",
            "occurrence partition",
            "do not infer grouping from simultaneity",
        ),
    },
    "source.spell.magic_mouth.unresolved.trigger_episode_frequency": {
        "source_exact_name": "Magic Mouth",
        "category": "source_semantics",
        "disposition": "SOURCE_HELD",
        "classification_index": 53,
        "map_entry_index": 86,
        "source_pass_row": 88,
        "body_witness_row": 199,
        "printed_page": 146,
        "source_header_line": 12802,
        "raw_body_sha256": "93e2864ca9f5cbf9b31cc0e5aa7a9304963e97938e3105a2680aff0e63559eb0",
        "locators": [
            {
                "heading": "Magic Mouth",
                "line_start": 13277,
                "line_end": 13291,
                "span_sha256": "f4bae8f5abed8471d713c43cfff53669fb68e253e2157bd42c048f1c04ebc704",
            }
        ],
        "source_phrases": (
            (0, "repeat its message whenever the trigger occurs"),
            (0, "visual or audible conditions that occur within 30 feet of the object"),
        ),
        "required_qualifiers": (
            "whenever the trigger occurs",
            "visual or audible",
            "within 30 feet of the object",
            "examples",
            "does not specify a rearm edge",
            "frequency while a condition remains continuously true",
            "automatic cooldown",
            "do not infer every-tick repetition",
            "word/radius source obligation at index 54 is separate",
        ),
    },
    "source.spell.magic_mouth.unresolved.message_word_bound": {
        "source_exact_name": "Magic Mouth",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 54,
        "map_entry_index": 86,
        "source_pass_row": 88,
        "body_witness_row": 199,
        "printed_page": 146,
        "source_header_line": 12802,
        "raw_body_sha256": "93e2864ca9f5cbf9b31cc0e5aa7a9304963e97938e3105a2680aff0e63559eb0",
        "locators": [
            {
                "heading": "Magic Mouth",
                "line_start": 13277,
                "line_end": 13291,
                "span_sha256": "f4bae8f5abed8471d713c43cfff53669fb68e253e2157bd42c048f1c04ebc704",
            }
        ],
        "source_phrases": (
            (0, "25 words or fewer"),
            (0, "as long as 10 minutes"),
            (0, "within 30 feet of the object"),
            (0, "isn’t being worn or carried by another creature"),
        ),
        "required_qualifiers": (
            "at most 25 words",
            "as long as 10 minutes",
            "within 30 feet of the enchanted object",
            "object-centered",
            "chosen object cannot be worn or carried by another creature",
            "10+ GP jade dust",
            "consumed",
            "pouch/focus substitution is excluded",
            "does not create ongoing Concentration",
            "Trigger episode frequency at index 53",
        ),
    },
    "source.spell.magic_weapon.unresolved.bonus_band_numbers": {
        "source_exact_name": "Magic Weapon",
        "category": "source_parameter",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 55,
        "map_entry_index": 87,
        "source_pass_row": 89,
        "body_witness_row": 200,
        "printed_page": 146,
        "source_header_line": 12830,
        "raw_body_sha256": "26e63b0335e54fa9f5872629b2b252eff2cc9d7bc69d91ceb44a35b294dcd27b",
        "locators": [
            {
                "heading": "Magic Weapon",
                "line_start": 13295,
                "line_end": 13309,
                "span_sha256": "7a2766808ccfdfb60b65362ee75ab5b64d44b807baaa96ce0339ac8a28b17d96",
            }
        ],
        "source_phrases": (
            (0, "nonmagical weapon"),
            (0, "+1 bonus to attack rolls and damage rolls"),
            (0, "level 3–5 spell slot"),
            (0, "level 6+ spell slot"),
        ),
        "required_qualifiers": (
            "level-2 slot grants +1",
            "level-3–5 grants +2",
            "level-6+ grants +3",
            "attack and damage rolls",
            "nonmagical weapon",
            "one hour",
            "nonconcentration",
            "Bonus Action",
            "ordinary Bonus Action does not acquire a trigger",
            "legacy bands/concentration",
            "do not add another point per slot",
        ),
    },
}
FOURTH_SOURCE_CLOSED_KEYS = frozenset(
    key
    for key, item in FOURTH_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_CLOSED"
)
FOURTH_SOURCE_HELD_KEYS = frozenset(
    key
    for key, item in FOURTH_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_HELD"
)

FIFTH_REVIEW: dict[str, str] = {
    "review_id": "SP00_FIFTH_SOURCE_REVIEW_20261013",
    "integration_base_sha": "884257cba9556812973397949e249904a8268052",
    "candidate_source_base_sha": "68134a799ce976d20ebbcc67abb80f5565978b9d",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-fifth-source-extraction-20261013.md",
    "candidate_sha256": "43fbfd3f41caa580fe5a0ac090cc4178fc1703016152d68a83535f2543f83f1e",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-fifth-source-review-20261013.md",
    "accepted_review_sha256": "dad684e0fd159dcb4f65d1200e1db093e7737824cef82562919ce53d03e473bb",
    "task_evidence_path": "DEV/docs/superpowers/design/2026-10-13-sp00-fifth-markdown-source-qualification.md",
    "task_evidence_sha256": "b68c387a11ba8a45800871cda12b508fa91fa841916bc9d49ed378ce0ab362a4",
}
FIFTH_SELECTED_CLASSIFICATION_INDEXES = tuple(range(56, 68))
FIFTH_EVIDENCE_ORDER = (
    (
        "FIFTH-01",
        "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
        "source_parameter",
    ),
    (
        "FIFTH-02",
        "source.spell.message.unresolved.barrier_thresholds",
        "source_parameter",
    ),
    (
        "FIFTH-03",
        "source.spell.mirror_image.unresolved.qualifying_face_threshold",
        "source_parameter",
    ),
    (
        "FIFTH-04",
        "source.spell.moonbeam.unresolved.form_source_cleanup",
        "source_semantics",
    ),
    (
        "FIFTH-05",
        "source.spell.pass_without_trace.unresolved.selection_timing",
        "source_semantics",
    ),
    (
        "FIFTH-06A",
        "source.spell.phantasmal_force.unresolved.dangerous_form_bounds",
        "source_parameter",
    ),
    (
        "FIFTH-06B",
        "source.spell.phantasmal_force.unresolved.dangerous_form_bounds",
        "source_semantics",
    ),
    (
        "FIFTH-07",
        "source.spell.prayer_of_healing.unresolved.responder_census",
        "source_mapping_review",
    ),
    (
        "FIFTH-08",
        "source.spell.prestidigitation.unresolved.object_material_bounds",
        "source_parameter",
    ),
    (
        "FIFTH-09",
        "source.spell.protection_from_evil_and_good.unresolved.supernatural_source_members",
        "source_mapping_review",
    ),
    (
        "FIFTH-10",
        "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
        "source_semantics",
    ),
    (
        "FIFTH-11",
        "source.spell.ray_of_frost.unresolved.movement_composition",
        "source_parameter",
    ),
    (
        "FIFTH-12",
        "source.spell.resistance.unresolved.eleven_type_members",
        "source_mapping_review",
    ),
)
FIFTH_SELECTED_KEYS = tuple(key for _, key, _ in FIFTH_EVIDENCE_ORDER)
FIFTH_COMMON_MARKDOWN_LOCATORS: tuple[dict[str, object], ...] = (
    {
        "heading": "Casting Spells",
        "line_start": 9068,
        "line_end": 9257,
        "span_sha256": "48ccc959d306e2f349b56e2dea465f9b119c47d414105011fc44104384aa0702",
    },
    {
        "heading": "Class Spell Lists",
        "line_start": 9133,
        "line_end": 9137,
        "span_sha256": "53cf80604eb60606f14e297d71f48bd0b5ccce68f333f5343f9fb34876873eba",
    },
    {
        "heading": "Reaction and Bonus Action Triggers",
        "line_start": 9151,
        "line_end": 9155,
        "span_sha256": "47c13792c1488cfeb403525e6a145fb5dc9cb844bf2a981c7443884b2dc2fb13",
    },
    {
        "heading": "Damage Rolls",
        "line_start": 1396,
        "line_end": 1400,
        "span_sha256": "3bab0640f9638faa8e732906e9ad79fb1941a7cbcfd1bba78b1e8bf69124ac15",
    },
    {
        "heading": "Concentration",
        "line_start": 16296,
        "line_end": 16304,
        "span_sha256": "04c55227b54b4481f715a64b6a517f63f5733171d475640db0f6f43d355cc1be",
    },
    {
        "heading": "Round Down",
        "line_start": 17084,
        "line_end": 17086,
        "span_sha256": "eed2effef1332d8e649b1f4ea715bd44fb15bcfb5d6562515d18719da2cbbdf7",
    },
    {
        "heading": "Shape-Shifting",
        "line_start": 17119,
        "line_end": 17121,
        "span_sha256": "a3c9b217f1280c7e66632ac38b5ce9c9fbdc3ef638bee2f85a3fc2d27e7e13e6",
    },
    {
        "heading": "Short Rest",
        "line_start": 17125,
        "line_end": 17141,
        "span_sha256": "f4170d17b36d6fa230f60ea55c49cf5b3d43139530af71fdde1e47833af687cb",
    },
    {
        "heading": "Speed",
        "line_start": 17163,
        "line_end": 17169,
        "span_sha256": "033e5886f45fe2767f324130b4d4cbcc6f4a27e8f7368fb8bb4e30bf4c9b3f15",
    },
)
FIFTH_COMMON_QUALIFIERS = (
    "Armor training is casting legality for the caster wearing armor, not a target limitation (9074–9076).",
    "Class parentheses indicate spell-list membership; some features add spells to a character's list outside those classes, but do not prove a particular casting capability (9133–9137).",
    "Level-1+ spells normally use a slot of their level or higher; cantrips do not; higher-slot benefits apply only where stated. None of these twelve profiles has a Ritual tag (9086–9110).",
    "Only one spell slot may be expended per turn. A Reaction spell responds to its defined trigger; only some Bonus Action spells specify a trigger (9145–9155).",
    "A minute-or-longer casting requires a Magic action each turn and Concentration while casting; interruption fails without slot expenditure and requires a restart (9159–9161).",
    "Range constrains effect origin as the description states; movable effects are not range-restricted unless the spell expressly says otherwise (9165–9175).",
    "Every specified component is required. Verbal needs normal voice, Somatic a hand, and Material a free hand; pouch/focus substitution excludes priced or consumed materials (9179–9201).",
    "An instantaneous duration describes momentary magic but does not erase a separately stated timed rider. Time-span dismissal without action requires the caster not be Incapacitated (9205–9213).",
    "Spell effects are exactly those stated; other outcomes remain GM purview. Body target kinds and clear-path/Total-Cover rules remain applicable, except where the spell states a specific exception (9217–9235).",
    "Use only source-specified saves and attack rolls and their stated branches; do not invent missing saves, attack rolls or outcomes (9239–9251).",
    "Different spells add while durations overlap; repeated same-spell effects do not combine, with the most potent or equally potent most recent effect applying (9255–9257).",
    "Damage penalties can reduce rolled damage to 0 but not below 0; a fixed amount is not a damage roll (1398–1400).",
    "Round down only when division or multiplication yields a fraction, unless a rule says otherwise; fixed subtraction does not acquire a rounding rule (17084–17086).",
    "Shape-Shifting behavior is specified by each transforming effect; ongoing effects generally carry between forms unless that effect says otherwise. This does not establish Moonbeam's underlying-source lifecycle (17119–17121).",
    "An ordinary Short Rest is one hour of downtime and requires at least 1 HP to start. Hit Point Dice and feature recharge follow their own text; Initiative, a noncantrip spell or damage interrupts an ordinary rest (17125–17141).",
    "A temporary Speed change applies equally to each existing special speed for the same duration. Remaining-movement switching rules do not set a Speed-stat floor (17163–17169).",
)
FIFTH_COMMON_REQUIRED_PHRASES: dict[str, tuple[str, ...]] = {
    "Casting Spells": (
        "You must have training with any armor",
        "Every spell has a level from 0 to 9",
        "Some features add a spell to a character’s spell list",
        "you can expend only one spell slot",
        "A spell’s range indicates how far",
        "a clear path to it, so it can’t be behind Total Cover",
        "the effects of the same spell cast multiple times",
    ),
    "Class Spell Lists": (
        "Some features add a spell to a character’s spell list even if the character isn’t a member of a class in the parentheses.",
    ),
    "Reaction and Bonus Action Triggers": (
        "A spell that has a casting time of a Reaction is cast in response to a trigger",
        "Some spells that have a casting time of a Bonus Action are also cast in response to a trigger",
    ),
    "Damage Rolls": ("0 damage but not negative damage",),
    "Concentration": (
        "the moment you start casting a spell that requires Concentration",
        "up to a maximum DC of 30",
    ),
    "Round Down": ("Whenever you divide or multiply a number in the game",),
    "Shape-Shifting": (
        "its description specifies what happens to you",
        "ongoing effects on you—conditions, spells, curses, and the like—carry over",
    ),
    "Short Rest": (
        "To start a Short Rest, you must have at least 1 Hit Point",
        "it recharges in the way specified in its description",
        "An interrupted Short Rest confers no benefits",
    ),
    "Speed": (
        "subtract the distance already moved from the new speed",
        "any special speed you have increases or decreases by an equal amount for the same duration",
    ),
}
FIFTH_REQUIRED_EVIDENCE_TOKENS = (
    FIFTH_REVIEW["candidate_sha256"],
    FIFTH_REVIEW["accepted_review_sha256"],
    "indexes 56–67 inclusive",
    "13 source subobligations",
    "9 closed subobligations across 8 keys",
    "4 held subobligations across 4 keys",
    "underlying transformation source",
    "underlying transformation source terminates",
    "no automatic reassertion",
    "30 keys across 28 entries",
    "W05_SPELL_SOURCE_QUALIFICATION_READY",
)
FIFTH_FUTURE_PROOF_KEYS = frozenset(
    {
        "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
        "source.spell.moonbeam.unresolved.form_source_cleanup",
        "source.spell.prayer_of_healing.unresolved.responder_census",
        "source.spell.protection_from_evil_and_good.unresolved.supernatural_source_members",
        "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
        "source.spell.ray_of_frost.unresolved.movement_composition",
    }
)
FIFTH_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.mending.unresolved.repair_dimension_and_missing_matter": {
        "source_exact_name": "Mending",
        "disposition": "SOURCE_HELD",
        "classification_index": 56,
        "map_entry_index": 88,
        "source_pass_row": 90,
        "body_witness_row": 209,
        "printed_page": 148,
        "source_header_line": 13005,
        "raw_body_sha256": "ef7396f774552d6d76c86bba757b4c685912d33f37fe8a35ed30e9dfa1ba524b",
        "locators": (
            {
                "heading": "Mending",
                "line_start": 13461,
                "line_end": 13475,
                "span_sha256": "49b027486fa211fad47212b375d1ab66586cb5d0bf78e7fdfdeb43b189d32046",
            },
        ),
        "source_phrases": (
            (0, "single break or tear"),
            (0, "no larger than 1 foot in any dimension"),
            (0, "can’t restore magic"),
        ),
        "interpretations": {
            "source_parameter": "Mending repairs a single break or tear in a touched object only when it is no larger than 1 foot in any dimension, leaving no trace; it can physically repair a magic item without restoring its magic."
        },
        "required_qualifiers": {
            "source_parameter": (
                "1 foot in any dimension",
                "missing-material quantity",
                "no matter creation",
            )
        },
    },
    "source.spell.message.unresolved.barrier_thresholds": {
        "source_exact_name": "Message",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 57,
        "map_entry_index": 89,
        "source_pass_row": 91,
        "body_witness_row": 210,
        "printed_page": 148,
        "source_header_line": 13020,
        "raw_body_sha256": "94a57586472ac8d8443f996146d2c143844404426d654ee487fb9049b27de533",
        "locators": (
            {
                "heading": "Message",
                "line_start": 13479,
                "line_end": 13493,
                "span_sha256": "6824f0e35d352e6deb13aa66784eea0ee3495fc06583e7aeebcda954b889f244",
            },
        ),
        "source_phrases": (
            (0, "120 feet"),
            (0, "only the target"),
            (0, "1 foot of stone, metal, or wood"),
            (0, "a thin sheet of lead"),
        ),
        "interpretations": {
            "source_parameter": "Message has 120-foot range; the target alone hears the whispered message and can optionally reply in a whisper only the caster hears. Through-solid casting requires familiarity with the target and knowledge that it is beyond the barrier."
        },
        "required_qualifiers": {
            "source_parameter": (
                "1 foot of stone, metal or wood",
                "thin sheet of lead",
                "no numeric lead thickness",
                "no legacy 1-inch metal",
            )
        },
    },
    "source.spell.mirror_image.unresolved.qualifying_face_threshold": {
        "source_exact_name": "Mirror Image",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 58,
        "map_entry_index": 92,
        "source_pass_row": 94,
        "body_witness_row": 216,
        "printed_page": 150,
        "source_header_line": 13136,
        "raw_body_sha256": "5e31a0533fd9a07384ace82e3f4eae5821add82c9e3a4bcc6e33b16fccca9648",
        "locators": (
            {
                "heading": "Mirror Image",
                "line_start": 13591,
                "line_end": 13605,
                "span_sha256": "4dd612ad90591938c9447dde539acb18e1b00d17f93ac157a62d30e40fd91c61",
            },
        ),
        "source_phrases": (
            (0, "a d6 for each of your remaining duplicates"),
            (0, "a 3 or higher"),
            (0, "Blindsight, or Truesight"),
        ),
        "interpretations": {
            "source_parameter": "When an attack roll hits the caster, roll one d6 per remaining duplicate; any 3 or higher redirects the hit to one duplicate, which is destroyed. Other damage/effects are ignored by duplicates, and the spell ends when all three are destroyed."
        },
        "required_qualifiers": {
            "source_parameter": (
                "only one duplicate",
                "Blinded",
                "Blindsight",
                "Truesight",
                "legacy d20",
                "duplicate AC",
            )
        },
    },
    "source.spell.moonbeam.unresolved.form_source_cleanup": {
        "source_exact_name": "Moonbeam",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 59,
        "map_entry_index": 94,
        "source_pass_row": 96,
        "body_witness_row": 220,
        "printed_page": 150,
        "source_header_line": 13220,
        "raw_body_sha256": "3e8d49e0f7177a8672169646f5c0f88426b149b29232214e4eb9e2adba1f0067",
        "locators": (
            {
                "heading": "Moonbeam",
                "line_start": 13663,
                "line_end": 13679,
                "span_sha256": "aaf21d6a3c3d5a7c704f1f5559c372e6785dee2f3af5fe11734e50b4fa91fb39",
            },
        ),
        "source_phrases": (
            (0, "5-foot-radius, 40-foot-high Cylinder"),
            (0, "reverts to its true form"),
            (0, "until it leaves the Cylinder"),
            (0, "only once per turn"),
        ),
        "interpretations": {
            "source_semantics": "Moonbeam's failed-save form rider reverts a shape-shifted creature to true form and bars shape-shifting until the creature leaves the Cylinder. This application-specific reversion is distinct from ending the underlying transformation source."
        },
        "required_qualifiers": {
            "source_semantics": (
                "underlying transformation source",
                "does not establish that the underlying transformation source terminates",
                "no generic source deletion",
                "no automatic reassertion",
                "blanket survival",
            )
        },
    },
    "source.spell.pass_without_trace.unresolved.selection_timing": {
        "source_exact_name": "Pass without Trace",
        "disposition": "SOURCE_HELD",
        "classification_index": 60,
        "map_entry_index": 95,
        "source_pass_row": 97,
        "body_witness_row": 224,
        "printed_page": 151,
        "source_header_line": 13298,
        "raw_body_sha256": "68b06279a1f031bb6976a24099a1972bce808c44b3c27a6f9f61b7c67d228407",
        "locators": (
            {
                "heading": "Pass without Trace",
                "line_start": 13735,
                "line_end": 13747,
                "span_sha256": "5286728517f232fad21e7a35ba72d36862ab98170e3a06ca57889586678a2132",
            },
        ),
        "source_phrases": (
            (0, "30-foot Emanation"),
            (0, "each creature you choose"),
            (0, "+10 bonus to Dexterity (Stealth)"),
            (0, "leave no tracks"),
        ),
        "interpretations": {
            "source_semantics": "While within the caster's 30-foot concealing Emanation, the caster and each creature the caster chooses gain +10 Dexterity (Stealth) and leave no tracks."
        },
        "required_qualifiers": {
            "source_semantics": (
                "selection occurs at casting",
                "fixed or dynamic membership",
                "free reassignment",
                "outside the aura",
                "magical-tracking immunity",
            )
        },
    },
    "source.spell.phantasmal_force.unresolved.dangerous_form_bounds": {
        "source_exact_name": "Phantasmal Force",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 61,
        "map_entry_index": 96,
        "source_pass_row": 98,
        "body_witness_row": 225,
        "printed_page": 151,
        "source_header_line": 13306,
        "raw_body_sha256": "185c36a4db855231a3b09b9be9a0654cbbc63d1d43a5e2e0b9292465f2f37180",
        "locators": (
            {
                "heading": "Phantasmal Force",
                "line_start": 13751,
                "line_end": 13767,
                "span_sha256": "1746c7ef849e32f2cdee5afe7f59bb8f9f083034df4c6c96f1084177ef29f3d5",
            },
        ),
        "source_phrases": (
            (0, "no larger than a 10-foot Cube"),
            (0, "Study action"),
            (0, "2d8 Psychic damage"),
            (0, "On each of your turns"),
            (0, "within 5 feet"),
        ),
        "interpretations": {
            "source_parameter": "A visible target within 60 feet makes an Intelligence save. On failure, it perceives a target-only phenomenon no larger than a 10-foot Cube and can use Study/Intelligence (Investigation) against spell save DC to end the spell on success. A dangerous phantasm can deal 2d8 Psychic on each caster turn when the target is in its area or within 5 feet.",
            "source_semantics": "Damage eligibility requires the phantasm to represent a dangerous creature or hazard; an arbitrary phenomenon is not enough. The target perceives a type appropriate to the illusion, while actual damage remains Psychic and the illusion does not change objective world truth.",
        },
        "required_qualifiers": {
            "source_parameter": (
                "each caster turn",
                "in its area or within 5 feet",
                "no higher-slot",
                "no unbounded proximity",
            ),
            "source_semantics": (
                "dangerous creature or hazard",
                "arbitrary phenomenon is not enough",
                "actual damage remains Psychic",
                "objective world truth",
                "exhaustive dangerous-form catalog",
            ),
        },
    },
    "source.spell.prayer_of_healing.unresolved.responder_census": {
        "source_exact_name": "Prayer of Healing",
        "disposition": "SOURCE_HELD",
        "classification_index": 62,
        "map_entry_index": 98,
        "source_pass_row": 100,
        "body_witness_row": 237,
        "printed_page": 154,
        "source_header_line": 13554,
        "raw_body_sha256": "fd0df00cfdaf3ed9b6a03304107390c6dbf574f9bef34c924a1642fea74e5e2d",
        "locators": (
            {
                "heading": "Prayer of Healing",
                "line_start": 13973,
                "line_end": 13987,
                "span_sha256": "0d6377b2a1aaa3cbc91b68dbedda8f90b19ac5bb31f40d79108cf50a5ae7c3a4",
            },
        ),
        "source_phrases": (
            (0, "Up to five creatures"),
            (0, "entire casting"),
            (0, "benefits of a Short Rest"),
            (0, "2d8 Hit Points"),
            (0, "finishes a Long Rest"),
            (0, "increases by 1d8"),
        ),
        "interpretations": {
            "source_mapping_review": "At completion of 10-minute casting, up to five chosen creatures remaining within 30 feet for the entire casting gain Short Rest benefits and regain 2d8 HP; each creature cannot be affected again until it finishes a Long Rest. Higher slots add 1d8 healing per slot level above 2."
        },
        "required_qualifiers": {
            "source_mapping_review": (
                "one-hour elapsed rest",
                "global shortened-rest rule",
                "automatic Hit Point Die spending",
                "feature's own description",
                "no complete applicable responder census",
            )
        },
    },
    "source.spell.prestidigitation.unresolved.object_material_bounds": {
        "source_exact_name": "Prestidigitation",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 63,
        "map_entry_index": 99,
        "source_pass_row": 101,
        "body_witness_row": 238,
        "printed_page": 154,
        "source_header_line": 13566,
        "raw_body_sha256": "5534f4c69a03d731a4c6a9bc8fd28428902400cff12734201983417fd33d77af",
        "locators": (
            {
                "heading": "Prestidigitation",
                "line_start": 13991,
                "line_end": 14015,
                "span_sha256": "0c145111e222a38335048c1d92ad0d6a98697865bb076e75db47d52f1489d326",
            },
        ),
        "source_phrases": (
            (0, "instantaneous, harmless sensory effect"),
            (0, "a small campfire"),
            (0, "no larger than 1 cubic foot"),
            (0, "nonliving material for 1 hour"),
            (0, "a small mark"),
            (0, "nonmagical trinket"),
            (0, "has no monetary worth"),
        ),
        "interpretations": {
            "source_parameter": "The six options are harmless instantaneous sensory effect; light/snuff candle, torch or small campfire; clean/soil an object up to 1 cubic foot; chill/warm/flavor up to 1 cubic foot of nonliving material for one hour; create a color, small mark or symbol on an object/surface for one hour; or create a nonmagical trinket or illusory image fitting in hand until the end of the caster's next turn."
        },
        "required_qualifiers": {
            "source_parameter": (
                "six options",
                "trinket deals no damage",
                "no monetary worth",
                "three non-instantaneous effects",
                "small",
                "does not make an illusory image objective material",
            )
        },
    },
    "source.spell.protection_from_evil_and_good.unresolved.supernatural_source_members": {
        "source_exact_name": "Protection from Evil and Good",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 64,
        "map_entry_index": 101,
        "source_pass_row": 103,
        "body_witness_row": 246,
        "printed_page": 157,
        "source_header_line": 13810,
        "raw_body_sha256": "b888ba72de84761569222ad7813068f7ddcbd5ce7b5c6e16756c3b7e74cefa4c",
        "locators": (
            {
                "heading": "Protection from Evil and Good",
                "line_start": 14188,
                "line_end": 14200,
                "span_sha256": "1a5fb548c39c0189eba7ff9593e70b4fc9d2242736cda1d5e4093cfee70fed0c",
            },
        ),
        "source_phrases": (
            (0, "Aberrations, Celestials, Elementals, Fey, Fiends, or Undead"),
            (0, "Advantage on any new saving throw"),
            (0, "worth 25+ GP, which the spell consumes"),
        ),
        "interpretations": {
            "source_mapping_review": "A willing touched creature is protected against exactly the source-listed Aberrations, Celestials, Elementals, Fey, Fiends and Undead, with the described attack Disadvantage, possession/condition prevention and Advantage on a new save against relevant existing control."
        },
        "required_qualifiers": {
            "source_mapping_review": (
                "Advantage on a new relevant save",
                "does not grant a new save",
                "end the effect automatically",
                "Consumed 25+ GP Holy Water",
                "no blanket charm/fear immunity",
            )
        },
        "members": (
            "Aberrations",
            "Celestials",
            "Elementals",
            "Fey",
            "Fiends",
            "Undead",
        ),
    },
    "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy": {
        "source_exact_name": "Ray of Enfeeblement",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 65,
        "map_entry_index": 104,
        "source_pass_row": 106,
        "body_witness_row": 250,
        "printed_page": 157,
        "source_header_line": 13861,
        "raw_body_sha256": "d05feb22a3b228153949caf4f7688d4b777e3da76ace1785aea087f882bac609",
        "locators": (
            {
                "heading": "Ray of Enfeeblement",
                "line_start": 14254,
                "line_end": 14268,
                "span_sha256": "ee7717b3a5f2eb5cc87f26f2517e3d5685d6a03f2c28b3c231c8f0d4f11548db",
            },
        ),
        "source_phrases": (
            (0, "Disadvantage on Strength-based D20 Tests"),
            (0, "subtracts 1d8 from all its damage rolls"),
            (0, "at the end of each of its turns"),
        ),
        "interpretations": {
            "source_semantics": "A successful Constitution save imposes Disadvantage on the target's next attack roll until the caster's next turn starts. Failure imposes Disadvantage on Strength-based D20 Tests and subtracts 1d8 from all damage rolls for the duration; an end-of-turn repeated save ends the spell on success. Damage under the penalty can reach 0 but not become negative."
        },
        "required_qualifiers": {
            "source_semantics": (
                "0 but not become negative",
                "not fixed damage amounts",
                "not a minimum of 1",
                "negative healing",
                "legacy half-Strength weapon damage",
            )
        },
    },
    "source.spell.ray_of_frost.unresolved.movement_composition": {
        "source_exact_name": "Ray of Frost",
        "disposition": "SOURCE_HELD",
        "classification_index": 66,
        "map_entry_index": 105,
        "source_pass_row": 107,
        "body_witness_row": 251,
        "printed_page": 157,
        "source_header_line": 13876,
        "raw_body_sha256": "acbf5544ece9d8b267804f550f65e342733ad0d02eb95f8ee6c0e11d30f3cb35",
        "locators": (
            {
                "heading": "Ray of Frost",
                "line_start": 14272,
                "line_end": 14286,
                "span_sha256": "dae3f77c2b494c1afd20ba279f16583438d1df80127bf260e3a243c491b77ea0",
            },
        ),
        "source_phrases": (
            (0, "ranged spell attack"),
            (0, "1d8 Cold damage"),
            (0, "reduced by 10 feet"),
            (0, "levels 5 (2d8), 11 (3d8), and 17 (4d8)"),
        ),
        "interpretations": {
            "source_parameter": "On a ranged spell attack hit, Ray of Frost deals 1d8 Cold and reduces Speed by 10 feet until the start of the caster's next turn. Character-level damage upgrades at 5/11/17 to 2d8/3d8/4d8; the fixed Speed reduction does not scale."
        },
        "required_qualifiers": {
            "source_parameter": (
                "existing special speeds",
                "no explicit minimum Speed floor",
                "not a stat floor",
                "fixed subtraction needs no rounding",
                "no zero clamp",
                "negative-Speed policy",
            )
        },
    },
    "source.spell.resistance.unresolved.eleven_type_members": {
        "source_exact_name": "Resistance",
        "disposition": "SOURCE_CLOSED",
        "classification_index": 67,
        "map_entry_index": 107,
        "source_pass_row": 109,
        "body_witness_row": 257,
        "printed_page": 158,
        "source_header_line": 13968,
        "raw_body_sha256": "f13455e2f9b58c45a738c097b310d12495a006028c9720b8047d941dd52e885b",
        "locators": (
            {
                "heading": "Resistance",
                "line_start": 14389,
                "line_end": 14401,
                "span_sha256": "c8eb5178fade2834aa5ad5c504723c2499bcbfaeeb821d120b5dbc729ab3432c",
            },
        ),
        "source_phrases": (
            (
                0,
                "Acid, Bludgeoning, Cold, Fire, Lightning, Necrotic, Piercing, Poison, Radiant, Slashing, or Thunder",
            ),
            (0, "reduces the total damage taken by 1d4"),
            (0, "only once per turn"),
        ),
        "interpretations": {
            "source_mapping_review": "A willing touched creature selects exactly one of the eleven listed damage types. Before the spell ends, damage of the chosen type reduces total damage taken by 1d4, only once per turn."
        },
        "required_qualifiers": {
            "source_mapping_review": (
                "Force and Psychic are not listed",
                "spell name does not establish damage halving",
                "only once per turn",
                "event grouping",
                "defense ordering",
            )
        },
        "members": (
            "Acid",
            "Bludgeoning",
            "Cold",
            "Fire",
            "Lightning",
            "Necrotic",
            "Piercing",
            "Poison",
            "Radiant",
            "Slashing",
            "Thunder",
        ),
    },
}
FIFTH_SOURCE_CLOSED_KEYS = frozenset(
    key
    for key, item in FIFTH_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_CLOSED"
)
FIFTH_SOURCE_HELD_KEYS = frozenset(
    key
    for key, item in FIFTH_SOURCE_ITEMS.items()
    if item["disposition"] == "SOURCE_HELD"
)
SIXTH_REVIEW: dict[str, str] = {
    "review_id": "SP00_SIXTH_SOURCE_REVIEW_20261013",
    "integration_base_sha": "afca759c38480f0e4a5629236b08c9d401ecd10d",
    "candidate_source_base_sha": "afca759c38480f0e4a5629236b08c9d401ecd10d",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-sixth-source-extraction-20261013.md",
    "candidate_sha256": "dc9600ae20c80c0f2a653dddb095246ea752b49c8a5493f3ad7411c6f44573a9",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-sixth-source-review-20261013.md",
    "accepted_review_sha256": "862aa04b0a27fa977b099bd0b4c19b1d9151a1313aaafcb8364c23b622f63ca1",
    "source_fixture_basis_sha": "c6d37201cab0a4dc2be1981762066f3d6d7b8be7",
    "task_evidence_path": "DEV/docs/superpowers/design/2026-10-13-sp00-sixth-markdown-source-qualification.md",
    "task_evidence_sha256": "0a8a9a8955c772bf4aea22fe479e407affebcfc860b1fff8fe9e1dd239e52aa5",
}
SIXTH_SELECTED_CLASSIFICATION_INDEXES = tuple(range(68, 80))
SIXTH_EVIDENCE_ORDER = (
    ("SIXTH-01", "source.spell.resistance.unresolved.damage_grouping_order", "source_semantics"),
    ("SIXTH-02", "source.spell.rope_trick.unresolved.boundary_location_profile", "source_semantics"),
    ("SIXTH-03", "source.spell.sanctuary.unresolved.retarget_cost_chain", "source_semantics"),
    ("SIXTH-04", "source.spell.scorching_ray.unresolved.target_kind_policy", "source_mapping_review"),
    ("SIXTH-05", "source.spell.sorcerous_burst.unresolved.permitted_type_members", "source_mapping_review"),
    ("SIXTH-06", "source.spell.spare_the_dying.unresolved.range_thresholds", "source_parameter"),
    ("SIXTH-07", "source.spell.speak_with_animals.unresolved.influence_option_census", "source_mapping_review"),
    ("SIXTH-08", "source.spell.spike_growth.unresolved.displacement_and_distance_policy", "source_parameter"),
    ("SIXTH-09A", "source.spell.suggestion.unresolved.agency_and_word_limit", "source_parameter"),
    ("SIXTH-09B", "source.spell.suggestion.unresolved.agency_and_word_limit", "source_semantics"),
    ("SIXTH-10", "source.spell.thaumaturgy.unresolved.exact_mode_bounds", "source_mapping_review"),
    ("SIXTH-11A", "source.spell.unseen_servant.unresolved.subject_health_classification", "source_semantics"),
    ("SIXTH-11B", "source.spell.unseen_servant.unresolved.force_numeric_profile", "source_parameter"),
)
SIXTH_COMMON_MARKDOWN_LOCATORS: tuple[dict[str, object], ...] = (
    {"heading": "Casting Spells", "line_start": 9068, "line_end": 9257, "span_sha256": "48ccc959d306e2f349b56e2dea465f9b119c47d414105011fc44104384aa0702"},
    {"heading": "Making an Attack", "line_start": 1248, "line_end": 1264, "span_sha256": "35bea2d0812d4a44be7fa07300bf0a7cf90dd6d8c0ad1dba7717889da7908b5e"},
    {"heading": "Ranged Attacks", "line_start": 1286, "line_end": 1302, "span_sha256": "e32e0f321ea5b06703118555d745cd620d585d782b7bb925011670f948331e7c"},
    {"heading": "Damage Rolls", "line_start": 1396, "line_end": 1400, "span_sha256": "3bab0640f9638faa8e732906e9ad79fb1941a7cbcfd1bba78b1e8bf69124ac15"},
    {"heading": "Resistance and Vulnerability", "line_start": 1434, "line_end": 1450, "span_sha256": "70acc27702623bfdce1f86419498e1b345cc5bc470cda3b6d183abdf1fc38378"},
    {"heading": "Stabilizing a Character", "line_start": 1516, "line_end": 1520, "span_sha256": "e52fc17397fe17a22c9054a12d28e355584547809a85b42b7d82fb1aa55b9f5a"},
    {"heading": "Movement and Difficult Terrain", "line_start": 1191, "line_end": 1203, "span_sha256": "1a15d99db21350e9d3cb9c53f846a225c3bf03fe6bc6f601bffdb735c3b8a127"},
    {"heading": "Charmed", "line_start": 16272, "line_end": 16278, "span_sha256": "59b73e22432dc652c3dfda5cc7f578c8b1819da2054c8edc8246fbe9bfb064e3"},
    {"heading": "Difficult Terrain", "line_start": 16493, "line_end": 16509, "span_sha256": "e9e0afb99ffc82ef3458a05377b6d59b5d7fe85332f5afe676e2b57a52946dd1"},
    {"heading": "Influence", "line_start": 16777, "line_end": 16797, "span_sha256": "eb96f2b41eb6a99c11ec3ac0301626e4a6a1366f8252a1c044b9380935071319"},
    {"heading": "Teleportation", "line_start": 17321, "line_end": 17325, "span_sha256": "d5d19757d0bf00d0bc58f4ddc10e59a48067004bae7c67f6b4758d15b62dee1c"},
    {"heading": "Invisible", "line_start": 16809, "line_end": 16817, "span_sha256": "cbf3644671e39a3df5e040933a31a70300194f8cfadffe6b1ff4e68d9e91b73c"},
    {"heading": "Concentration", "line_start": 16296, "line_end": 16304, "span_sha256": "04c55227b54b4481f715a64b6a517f63f5733171d475640db0f6f43d355cc1be"},
)
SIXTH_COMMON_QUALIFIERS = (
    "Casting retains class-list versus individual capability distinction, one slot per turn, defined reaction/bonus-action triggers, exact components and material substitution limits, long-cast restart, range-of-origin, clear path, specified effects/saves and same-spell overlap rules (9068–9257; material hand 9199–9201).",
    "Common attack rules admit a creature, object or location as an attack target; this does not make a location a damage-bearing entity (1248–1264).",
    "Ranged-attack conditions remain applicable; no ray roll, target binding or hit result is inferred beyond the spell body (1286–1302).",
    "Damage penalties may reduce a damage roll to 0 but not below 0; fixed damage is not a damage roll (1396–1400).",
    "The general adjustment → Resistance → Vulnerability order is retained but does not resolve eligible-occurrence grouping, choice or a new defense-consumer policy (1434–1450).",
    "A Stable creature at 0 Hit Points does not make Death Saving Throws, remains Unconscious, loses Stable on damage and gains 1 HP after 1d4 hours without healing (1516–1520).",
    "Difficult Terrain costs one extra foot of movement per foot traveled, noncumulatively; movement expenditure is not distance traveled for Spike Growth damage (1191–1203).",
    "Charmed prevents the charmed creature from attacking the charmer or targeting the charmer with damaging abilities or magical effects, and grants the charmer social-check Advantage; it does not ban every possible indirect or incidental harm (16272–16278).",
    "Difficult Terrain movement cost is not multiplied into distance traveled for a travel-triggered spell effect (16493–16509).",
    "Influence remains GM-determined: willing/unwilling/hesitant branches, exact five skill options, default DC max(15, Intelligence score), and repeat wait are not free action or automatic cooperation (16777–16797).",
    "Teleportation traverses no intervening space; it does not settle every endpoint or zone-entry interaction (17321–17325).",
    "Invisible retains its stated visibility exceptions; invisibility is not proof of nonexistence (16809–16817).",
    "Concentration ends the moment the creator starts casting another spell requiring Concentration, or activates another effect requiring Concentration; completion is not the trigger. Damage uses DC max(10, half damage rounded down), capped at 30; Incapacitated/death ends it, and the creator may end Concentration without an action (16296–16304).",
)
SIXTH_COMMON_REQUIRED_PHRASES: dict[str, tuple[str, ...]] = {
    "Casting Spells": ("You must have training with any armor", "you can expend only one spell slot", "A Material component is a particular material"),
    "Making an Attack": ("a creature, an object, or a location",),
    "Ranged Attacks": ("ranged attack roll",),
    "Damage Rolls": ("0 damage but not negative damage",),
    "Resistance and Vulnerability": ("Modifiers to damage are applied in the following order",),
    "Stabilizing a Character": ("Stable",),
    "Movement and Difficult Terrain": ("Difficult Terrain",),
    "Charmed": ("You can’t attack the charmer or target the charmer with damaging abilities or magical effects.", "The charmer has Advantage on any ability check to interact with you socially."),
    "Difficult Terrain": ("costs 1 extra foot",),
    "Influence": ("Charisma (Deception)", "Wisdom (Animal Handling)"),
    "Teleportation": ("without moving through the intervening space",),
    "Invisible": ("While you have the Invisible condition",),
    "Concentration": ("the moment you start casting a spell that requires Concentration", "up to a maximum DC of 30"),
}
SIXTH_FUTURE_PROOF_KEYS = frozenset({
    "source.spell.resistance.unresolved.damage_grouping_order",
    "source.spell.rope_trick.unresolved.boundary_location_profile",
    "source.spell.sanctuary.unresolved.retarget_cost_chain",
    "source.spell.speak_with_animals.unresolved.influence_option_census",
    "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
    "source.spell.unseen_servant.unresolved.subject_health_classification",
    "source.spell.unseen_servant.unresolved.force_numeric_profile",
})
SIXTH_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.resistance.unresolved.damage_grouping_order": {
        "source_exact_name": "Resistance", "disposition": "SOURCE_HELD", "classification_index": 68, "map_entry_index": 107, "source_pass_row": 109, "body_witness_row": 257, "printed_page": 158, "source_header_line": 13968,
        "raw_body_sha256": "f13455e2f9b58c45a738c097b310d12495a006028c9720b8047d941dd52e885b",
        "locators": ({"heading": "Resistance", "line_start": 14389, "line_end": 14401, "span_sha256": "c8eb5178fade2834aa5ad5c504723c2499bcbfaeeb821d120b5dbc729ab3432c"},),
        "source_phrases": ((0, "You touch a willing creature and choose a damage type:"), (0, "choose a damage type: Acid, Bludgeoning, Cold"), (0, "reduces the total damage taken by 1d4"), (0, "only once per turn")),
        "interpretations": {"source_semantics": "The caster touches a willing creature and chooses one of the exact eleven source-listed damage types. Before the spell ends, damage of the chosen type reduces the willing creature's total damage taken by 1d4, once per turn."},
        "required_qualifiers": {"source_semantics": ("Force and Psychic are not listed", "no saving-throw bonus", "no automatic damage halving", "simultaneous or mixed-type damage grouping", "eligible-occurrence choice", "no first-hit automatic consumption", "no pooled or shared d4")},
        "members": ("Acid", "Bludgeoning", "Cold", "Fire", "Lightning", "Necrotic", "Piercing", "Poison", "Radiant", "Slashing", "Thunder"),
    },
    "source.spell.rope_trick.unresolved.boundary_location_profile": {
        "source_exact_name": "Rope Trick", "disposition": "SOURCE_CLOSED", "classification_index": 69, "map_entry_index": 108, "source_pass_row": 110, "body_witness_row": 261, "printed_page": 159, "source_header_line": 14031,
        "raw_body_sha256": "0967df1adf8eb7b37fb6de2fab37f4bd0d65b5c296eb36d928a759a543fa3cf9",
        "locators": ({"heading": "Rope Trick", "line_start": 14457, "line_end": 14471, "span_sha256": "0c387a71023cea2267db52607ba19c49db32d8ef43ff41ca02d2bb51ef958fa8"},),
        "source_phrases": ((0, "perpendicular to the ground or the rope reaches a ceiling"), (0, "Invisible 3-foot-by-5-foot portal"), (0, "up to eight Medium or smaller creatures"), (0, "Anything inside the space drops out")),
        "interpretations": {"source_semantics": "The rope rises perpendicular to the ground or to a ceiling. Its upper end opens an Invisible 3-foot-by-5-foot portal into an extradimensional space; entry is by climbing and the rope can be pulled in or dropped out. It holds up to eight Medium-or-smaller creatures, bars attacks/spells/other effects both ways while occupants see outward, and anything inside drops out when the spell ends."},
        "required_qualifiers": {"source_semantics": ("no legacy 60-foot rope limit", "no inferred interior size or object capacity", "no universal object-transfer permission", "no bidirectional sight", "no safe landing or canonical location identity", "not portable storage")},
    },
    "source.spell.sanctuary.unresolved.retarget_cost_chain": {
        "source_exact_name": "Sanctuary", "disposition": "SOURCE_CLOSED", "classification_index": 70, "map_entry_index": 110, "source_pass_row": 112, "body_witness_row": 263, "printed_page": 159, "source_header_line": 14061,
        "raw_body_sha256": "172c6947953cab15ba8a03206ccbfaf563010621e778c33d1b6c4ec57f0b9943",
        "locators": ({"heading": "Sanctuary", "line_start": 14493, "line_end": 14505, "span_sha256": "c262ace6d5dc07b1dbf518b054b3c5ffb9450d41159b8409cc59affb91a41dda"},),
        "source_phrases": ((0, "attack roll or a damaging spell"), (0, "choose a new target or lose the attack or spell"), (0, "areas of effect"), (0, "casts a spell")),
        "interpretations": {"source_semantics": "A creature targeting the warded creature with an attack roll or damaging spell must succeed on a Wisdom save or choose a new target or lose that attack/spell; areas of effect bypass the ward. The ward ends if its recipient makes an attack roll, casts any spell or deals damage."},
        "required_qualifiers": {"source_semantics": ("failed ward save is not universally an invalid-target event", "no blanket refund", "no free attack or action entitlement", "no additional slot expenditure", "retargeted spell legality remains separate", "no universal cost algorithm")},
    },
    "source.spell.scorching_ray.unresolved.target_kind_policy": {
        "source_exact_name": "Scorching Ray", "disposition": "SOURCE_CLOSED", "classification_index": 71, "map_entry_index": 111, "source_pass_row": 113, "body_witness_row": 264, "printed_page": 159, "source_header_line": 14074,
        "raw_body_sha256": "18a95736eff0af43acf5cb85f55c9aa982f0e09e16766a596bf4d53d9f9e8ece",
        "locators": ({"heading": "Scorching Ray", "line_start": 14509, "line_end": 14523, "span_sha256": "1a099cfc3c6ca8497b63350f4b7b3d0f1290533987e90a7748a242789d07356f"},),
        "source_phrases": ((0, "three fiery rays"), (0, "Make a ranged spell attack for each ray"), (0, "2d6 Fire damage"), (0, "one additional ray for each spell slot level above 2")),
        "interpretations": {"source_mapping_review": "Scorching Ray creates three rays aimed at one or several targets within range, with a separate ranged spell attack per ray and 2d6 Fire damage per hit; each slot level above 2 adds one ray. The body states no creature-only target restriction, so common attack rules supply creature, object or location aim kinds."},
        "required_qualifiers": {"source_mapping_review": ("location aim is not a damage-bearing entity", "preserve clear path and Total Cover", "do not collapse rays into one roll or total", "no automatic location hits", "no invented object defenses", "no later-ray binding or native consumer proof")},
        "members": ("creature", "object", "location"),
    },
    "source.spell.sorcerous_burst.unresolved.permitted_type_members": {
        "source_exact_name": "Sorcerous Burst", "disposition": "SOURCE_CLOSED", "classification_index": 72, "map_entry_index": 123, "source_pass_row": 125, "body_witness_row": 285, "printed_page": 163, "source_header_line": 14448,
        "raw_body_sha256": "a6861f5b314a1a32a8e9b32f14076c5b057c418ea5ed49294ea6c9d8ff3da902",
        "locators": ({"heading": "Sorcerous Burst", "line_start": 14897, "line_end": 14913, "span_sha256": "6d590ba135423b140efa1ef1126985b28239d1d6ad2111e33c38dfe8d73e19fc"},),
        "source_phrases": ((0, "one creature or object within range"), (0, "Acid, Cold, Fire, Lightning, Poison, Psychic, or Thunder"), (0, "roll another d8"), (0, "maximum number of these d8s"), (0, "levels 5 (2d8), 11 (3d8), and 17 (4d8)")),
        "interpretations": {"source_mapping_review": "The exact source-ordered selectable types are Acid, Cold, Fire, Lightning, Poison, Psychic and Thunder. It is a ranged spell attack against one creature or object, starting at 1d8 and scaling to 2d8/3d8/4d8 at character levels 5/11/17. A rolled 8 permits another d8; the maximum added dice per cast equals the spellcasting ability modifier."},
        "required_qualifiers": {"source_mapping_review": ("Force, Radiant, Necrotic and physical damage types are excluded", "an 8 permits but does not compel an extra die", "modifier caps added dice per cast", "no arbitrary recursion depth", "no minimum-one policy", "critical-hit and RNG sequencing remain unproved")},
        "members": ("Acid", "Cold", "Fire", "Lightning", "Poison", "Psychic", "Thunder"),
    },
    "source.spell.spare_the_dying.unresolved.range_thresholds": {
        "source_exact_name": "Spare the Dying", "disposition": "SOURCE_CLOSED", "classification_index": 73, "map_entry_index": 124, "source_pass_row": 126, "body_witness_row": 286, "printed_page": 163, "source_header_line": 14466,
        "raw_body_sha256": "0c376f4f474c7fb891414aa31b4c2890d82d4f364255548ecc6dd16a80772c4c",
        "locators": ({"heading": "Spare the Dying", "line_start": 14917, "line_end": 14931, "span_sha256": "d7166779d01e13af3f7f44a0f0bba46c3046c8f766fba5a9744dc718593d76ac"},),
        "source_phrases": ((0, "Range:** 15 feet"), (0, "has 0 Hit Points and isn’t dead"), (0, "becomes Stable"), (0, "levels 5 (30 feet), 11 (60 feet), and 17 (120 feet)")),
        "interpretations": {"source_parameter": "Spare the Dying has 15-foot range, doubled at character levels 5, 11 and 17 to 30, 60 and 120 feet. It targets a creature with 0 Hit Points that is not dead and makes it Stable."},
        "required_qualifiers": {"source_parameter": ("not Touch", "no Construct or Undead exception", "Stable remains Unconscious and does not roll Death Saves", "damage breaks Stable", "1d4 hours without healing grants 1 HP", "no immediate healing or resurrection")},
    },
    "source.spell.speak_with_animals.unresolved.influence_option_census": {
        "source_exact_name": "Speak with Animals", "disposition": "SOURCE_CLOSED", "classification_index": 74, "map_entry_index": 125, "source_pass_row": 127, "body_witness_row": 287, "printed_page": 164, "source_header_line": 14477,
        "raw_body_sha256": "bb2656f63664b99cdc33b71a74071dd474465bc4e4410ef5cfb5fc195439e386",
        "locators": (
            {"heading": "Speak with Animals", "line_start": 14935, "line_end": 14949, "span_sha256": "06af8988a16d5c17090ee53692e53453a60171d9afb29c2495c482c29c1045a8"},
            {"heading": "Influence", "line_start": 16777, "line_end": 16797, "span_sha256": "eb96f2b41eb6a99c11ec3ac0301626e4a6a1366f8252a1c044b9380935071319"},
        ),
        "source_phrases": ((0, "communicate with Beasts"), (0, "any of the Influence action’s skill options"), (0, "whatever it has perceived within the past day"), (1, "Charisma (Deception)"), (1, "Wisdom (Animal Handling)")),
        "interpretations": {"source_mapping_review": "Speak with Animals allows comprehension and verbal communication with Beasts and any of Influence's five skill options. Information is limited by survival/companionship interests and at minimum includes nearby locations/monsters and what the Beast perceived within the past day."},
        "required_qualifiers": {"source_mapping_review": ("Deception and Persuasion require understanding", "Animal Handling can coax a Beast or Monstrosity generally", "spell communication remains Beast-only", "willing, unwilling and hesitant outcomes remain GM-determined", "default DC max(15, Intelligence score)", "no automatic truth, cooperation, charm or command authority", "ritual preparation, extra 10 minutes and long-cast Concentration")},
        "members": ("Charisma (Deception)", "Charisma (Intimidation)", "Charisma (Performance)", "Charisma (Persuasion)", "Wisdom (Animal Handling)"),
    },
    "source.spell.spike_growth.unresolved.displacement_and_distance_policy": {
        "source_exact_name": "Spike Growth", "disposition": "SOURCE_HELD", "classification_index": 75, "map_entry_index": 127, "source_pass_row": 129, "body_witness_row": 291, "printed_page": 164, "source_header_line": 14546,
        "raw_body_sha256": "184dd1f3a482f6d5e6f809144f810a55281d4a3c025d0cd73ce4be88b3b17db8",
        "locators": ({"heading": "Spike Growth", "line_start": 15009, "line_end": 15023, "span_sha256": "c5fb06ec056006712ee2c9a8a995391eb7e3e35134d4ad077339f447a6025dd1"},),
        "source_phrases": ((0, "150 feet"), (0, "20-foot-radius Sphere"), (0, "Difficult Terrain"), (0, "2d4 Piercing damage for every 5 feet it travels"), (0, "Wisdom (Perception or Survival) check")),
        "interpretations": {"source_parameter": "Spike Growth has 150-foot range and creates a 20-foot-radius Sphere of Difficult Terrain. A creature moving into or within the area takes 2d4 Piercing for every 5 feet actually traveled; the source states no once-per-turn cap. The unseen-at-casting hazard requires Search and a successful Wisdom (Perception or Survival) check against spell save DC before entry."},
        "required_qualifiers": {"source_parameter": ("movement cost is not distance traveled", "no once-per-turn cap", "exact qualifying forced displacement remains unresolved", "teleportation traverses no intervening space but does not settle all endpoints", "no voluntary-only or universal forced-motion rule", "no fractional-distance accumulation or reset", "no endpoint-only damage or terrain-cost multiplier")},
    },
    "source.spell.suggestion.unresolved.agency_and_word_limit": {
        "source_exact_name": "Suggestion", "disposition": "SOURCE_CLOSED", "classification_index": 76, "map_entry_index": 130, "source_pass_row": 132, "body_witness_row": 299, "printed_page": 166, "source_header_line": 14677,
        "raw_body_sha256": "9751dc59b3173880dd5ffae289b886db01f1ca817884606953947635460f6619",
        "locators": ({"heading": "Suggestion", "line_start": 15161, "line_end": 15175, "span_sha256": "b379e6c0272739ada33bf0839c78f841942e0c1f5c3f73a509ab8038de698a15"},),
        "source_phrases": ((0, "no more than 25 words"), (0, "must sound achievable"), (0, "deal damage to the target or its allies"), (0, "Charmed target pursues the suggestion")),
        "interpretations": {
            "source_parameter": "Suggestion's described course of activity contains no more than 25 words; no tokenizer, language or punctuation convention is stated.",
            "source_semantics": "Suggestion targets one visible creature in range that can hear and understand. It must sound achievable and not obviously deal damage to target or allies. Wisdom failure gives Charmed and separately requires pursuit to best ability; completion, duration or caster/allies damaging the target ends the effect.",
        },
        "required_qualifiers": {
            "source_parameter": ("no legacy sentence-count limit", "no invented language-specific tokenizer"),
            "source_semantics": ("exactly 30 feet", "V and M honey with no Somatic component", "Concentration up to eight hours", "Charmed creature cannot attack the charmer or target the charmer with damaging abilities or magical effects", "Charmed alone is not general compelled obedience", "pursuit is separately specified by Suggestion", "damage to others is not automatically this spell’s break trigger", "no universal agency override or immunity bypass"),
        },
    },
    "source.spell.thaumaturgy.unresolved.exact_mode_bounds": {
        "source_exact_name": "Thaumaturgy", "disposition": "SOURCE_CLOSED", "classification_index": 77, "map_entry_index": 131, "source_pass_row": 133, "body_witness_row": 308, "printed_page": 169, "source_header_line": 14977,
        "raw_body_sha256": "d2364dc16642aced4f66a1d8840a9b3edd638c1048bdc831ee4b86bfebc16581",
        "locators": ({"heading": "Thaumaturgy", "line_start": 15411, "line_end": 15435, "span_sha256": "4bdca80fdecc504d47b7dfc9d447256d5d8477ea9da1503434043162ea8aff31"},),
        "source_phrases": ((0, "up to three of its 1-minute effects"), (0, "up to three times as loud as normal"), (0, "Advantage on Charisma (Intimidation) checks"), (0, "unlocked door or window"), (0, "harmless tremors")),
        "interpretations": {"source_mapping_review": "Thaumaturgy is V-only, 30 feet, up to one minute, with one selected effect per cast and at most three minute-long effects active across recasts. All six named modes are retained: Altered Eyes, Booming Voice, Fire Play, Invisible Hand, Phantom Sound and Tremors. Booming Voice grants Charisma (Intimidation) Advantage; unlocked door/window open or slam and chosen-origin sound are instantaneous."},
        "required_qualifiers": {"source_mapping_review": ("instantaneous effects do not occupy the ongoing minute cap", "no flame ignition or extinguishing", "no damage or lock bypass", "no numeric lumen, decibel, tremor-size or force model", "Phantom Sound examples are not a closed catalog", "Advantage is mechanical, not flavor", "no native object/light/roll/concurrency proof")},
        "members": ("Altered Eyes", "Booming Voice", "Fire Play", "Invisible Hand", "Phantom Sound", "Tremors"),
    },
    "source.spell.unseen_servant.unresolved.subject_health_classification": {
        "source_exact_name": "Unseen Servant", "disposition": "SOURCE_HELD", "classification_index": 78, "map_entry_index": 134, "source_pass_row": 136, "body_witness_row": 320, "printed_page": 171, "source_header_line": 15220,
        "raw_body_sha256": "f650682363b2b72639401347b5415a21fbc9d9e2fab4bd98bf4da8930e94c4b4",
        "locators": ({"heading": "Unseen Servant", "line_start": 15641, "line_end": 15655, "span_sha256": "0f32649763cb95c6ce7d3fde0e844325df5af09d74932110ecec545a9a5265b6"},),
        "source_phrases": ((0, "Invisible, mindless, shapeless, Medium force"), (0, "unoccupied space on the ground within range"), (0, "it can’t attack")),
        "interpretations": {"source_semantics": "The body describes an Invisible, mindless, shapeless, Medium force created on unoccupied ground in range that cannot attack. These labels and the stat line do not establish creature/object classification or creature-target eligibility."},
        "required_qualifiers": {"source_semantics": ("preserve the L02-C01 owner obligation", "no categorical noncreature legality without source/common targeting closure", "neither creature nor object admission is established", "native Actor/Asset/health identity remains future proof", "no private mind or autonomous model is inferred")},
    },
    "source.spell.unseen_servant.unresolved.force_numeric_profile": {
        "source_exact_name": "Unseen Servant", "disposition": "SOURCE_CLOSED", "classification_index": 79, "map_entry_index": 134, "source_pass_row": 136, "body_witness_row": 320, "printed_page": 171, "source_header_line": 15220,
        "raw_body_sha256": "f650682363b2b72639401347b5415a21fbc9d9e2fab4bd98bf4da8930e94c4b4",
        "locators": ({"heading": "Unseen Servant", "line_start": 15641, "line_end": 15655, "span_sha256": "0f32649763cb95c6ce7d3fde0e844325df5af09d74932110ecec545a9a5265b6"},),
        "source_phrases": ((0, "AC 10, 1 Hit Point, and a Strength of 2"), (0, "Once on each of your turns as a Bonus Action"), (0, "move up to 15 feet and interact with an object"), (0, "would move it more than 60 feet away")),
        "interpretations": {"source_parameter": "Unseen Servant has AC 10, 1 HP and Strength 2, cannot attack and ends at 0 HP. Once on each caster turn, a Bonus Action can command up to 15 feet movement plus object interaction. It continues simple human-doable tasks to best ability until completion, then waits. A commanded task that would move it more than 60 feet from the caster ends the spell."},
        "required_qualifiers": {"source_parameter": ("commanded-task termination predicate", "not an ambient caster-motion leash", "15 feet is not a Speed stat", "no own turn or free independent action budget", "no carrying capacity or universal repair/material-generation promise", "classification and native stat/action/health consumers remain NOT_ESTABLISHED")},
    },
}
SIXTH_SOURCE_RESIDUALS: dict[tuple[str, str], str] = {
    ("source.spell.resistance.unresolved.damage_grouping_order", "source_semantics"): "HOLD_SOURCE_SUBOBLIGATION; simultaneous/mixed-type damage occurrence grouping, eligible occurrence choice and exact defense-consumer ordering are not settled by the source spans. No reaction, first-hit rule, pooling or shared die is inferred.",
    ("source.spell.rope_trick.unresolved.boundary_location_profile", "source_semantics"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; portal boundary, occupancy, entry/exit and duration facts are source-closed. Location, persistence, occupant/asset transfer and safe-fall proof remain NOT_ESTABLISHED.",
    ("source.spell.sanctuary.unresolved.retarget_cost_chain", "source_semantics"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; source save/retarget/loss distinctions are closed. Finite interrupts, recursive wards, commitment points and native cost accounting remain NOT_ESTABLISHED.",
    ("source.spell.scorching_ray.unresolved.target_kind_policy", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; common attack target-kind admission is source-grounded and the body adds no creature-only restriction. Exact native target kinds, object health, later-ray binding and roll/consumer proof remain NOT_ESTABLISHED.",
    ("source.spell.sorcerous_burst.unresolved.permitted_type_members", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the exact selectable type roster is source-closed. Exploding-die sequencing, critical accounting, negative modifier realization, RNG ownership and optional-choice recovery remain NOT_ESTABLISHED.",
    ("source.spell.spare_the_dying.unresolved.range_thresholds", "source_parameter"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the exact base and cantrip-upgrade range thresholds and 0-HP/not-dead target condition are source-closed. No immediate healing, temporary HP, resurrection or native LifeState proof follows.",
    ("source.spell.speak_with_animals.unresolved.influence_option_census", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the five Influence skill options and source-level communication census are closed. Attitude/agency adjudication and native consumer realization remain NOT_ESTABLISHED.",
    ("source.spell.spike_growth.unresolved.displacement_and_distance_policy", "source_parameter"): "HOLD_SOURCE_SUBOBLIGATION; exact qualifying forced displacement and any segment-event boundary rule remain unresolved. Movement cost is not distance traveled; no displacement category or fractional-distance policy is selected.",
    ("source.spell.suggestion.unresolved.agency_and_word_limit", "source_parameter"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the 25-word maximum is source-closed. Tokenization, language and punctuation semantics remain NOT_ESTABLISHED.",
    ("source.spell.suggestion.unresolved.agency_and_word_limit", "source_semantics"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; source eligibility, achievability, damage criterion, Charmed boundary and pursuit distinction are source-closed. No universal agency override, generated-world truth or native policy admission follows.",
    ("source.spell.thaumaturgy.unresolved.exact_mode_bounds", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; exact mode names, bounds and mechanical Advantage are source-closed. Native object/light/roll/concurrency consumers remain NOT_ESTABLISHED.",
    ("source.spell.unseen_servant.unresolved.subject_health_classification", "source_semantics"): "HOLD_SOURCE_SUBOBLIGATION; source/common targeting semantics do not classify this subject or establish creature/object target eligibility. Retain L02-C01; native Actor/Asset/health proof remains NOT_ESTABLISHED.",
    ("source.spell.unseen_servant.unresolved.force_numeric_profile", "source_parameter"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; exact stats, command timing, movement/object interaction and commanded-task distance termination are source-closed. This does not close index 78 classification or native stat/action/health consumers.",
}
SIXTH_SOURCE_CLOSED_KEYS = frozenset(key for key, item in SIXTH_SOURCE_ITEMS.items() if item["disposition"] == "SOURCE_CLOSED")
SIXTH_SOURCE_HELD_KEYS = frozenset(key for key, item in SIXTH_SOURCE_ITEMS.items() if item["disposition"] == "SOURCE_HELD")
SEVENTH_REVIEW: dict[str, str] = {
    "review_id": "SP00_SEVENTH_SOURCE_REVIEW_20261013",
    "integration_base_sha": "39ab1b4a1c7a844f4df2e7886c4b2ac17e401243",
    "candidate_source_base_sha": "39ab1b4a1c7a844f4df2e7886c4b2ac17e401243",
    "candidate_path": "/tmp/hdm-dev/spell-recovery/SP00-final-unreviewed-source-inventory-20261013.md",
    "candidate_sha256": "57ce2b2bf272e0afeb0274ddafec6b34412bc21d52931396ca4370757fdcfcc0",
    "accepted_review_path": "/tmp/hdm-dev/spell-recovery/SP00-final-unreviewed-source-review-20261013.md",
    "accepted_review_sha256": "8b0b85cf1d2d9b4741e0d5699182cc188e4d95c3398194870a528847e9f00b71",
    "source_fixture_basis_sha": "87ff9f41a73b346cad7038b5f126aec44c05a5f340fd310cf2fb67853fa9846b",
    "task_evidence_path": "DEV/docs/superpowers/design/2026-10-13-sp00-seventh-markdown-source-qualification.md",
    "task_evidence_sha256": "87a338bd875395c43e09fc51dfc31a45fdd068d07ab3881c242d75a30aec8d08",
}
SEVENTH_SELECTED_CLASSIFICATION_INDEXES = (6, 30, 31, 32, 80, 81)
SEVENTH_EVIDENCE_ORDER = (
    ("SEVENTH-01", "source.spell.augury.unresolved.four_omen_members", "source_mapping_review"),
    ("SEVENTH-02", "source.spell.find_familiar.unresolved.eligible_form_census", "source_mapping_review"),
    ("SEVENTH-03", "source.spell.find_steed.unresolved.type_to_action_mapping", "source_mapping_review"),
    ("SEVENTH-04A", "source.spell.find_steed.unresolved.steed_numeric_cells", "source_parameter"),
    ("SEVENTH-04B", "source.spell.find_steed.unresolved.steed_numeric_cells", "source_mapping_review"),
    ("SEVENTH-05", "source.spell.warding_bond.unresolved.copied_damage_policy", "source_semantics"),
    ("SEVENTH-06", "source.spell.web.unresolved.web_numeric_geometry", "source_parameter"),
)
SEVENTH_COMMON_MARKDOWN_LOCATORS: tuple[dict[str, object], ...] = (
    {"heading": "Longer Casting Times", "line_start": 9159, "line_end": 9161, "span_sha256": "cf31fedb40e11967b8806caa5c42a5613692ef85112fdd6ad27e1309187a88f1"},
    {"heading": "Range", "line_start": 9165, "line_end": 9175, "span_sha256": "179d9da6357281de3a4e376fa4c89f5debd85dfd8751b0f095bc5843dcb38003"},
    {"heading": "Mounted Combat", "line_start": 1328, "line_end": 1344, "span_sha256": "236ea4cd79407b1b1fdc5cffe5f1a655dfe567653144f13b376f294faceb0b6c"},
    {"heading": "Combining Spell Effects", "line_start": 9255, "line_end": 9257, "span_sha256": "459f8f4b95b21ee5993d23fc47d7fb0e5de64dc118051efce761634bb655b952"},
    {"heading": "Resistance and Vulnerability", "line_start": 1434, "line_end": 1450, "span_sha256": "70acc27702623bfdce1f86419498e1b345cc5bc470cda3b6d183abdf1fc38378"},
    {"heading": "Cube [Area of Effect]", "line_start": 16360, "line_end": 16364, "span_sha256": "46c701d69e86c32fec52eee71f624b7c2919619e719ca21b9a3b2c8c84cf53da"},
    {"heading": "Concentration", "line_start": 16296, "line_end": 16304, "span_sha256": "04c55227b54b4481f715a64b6a517f63f5733171d475640db0f6f43d355cc1be"},
    {"heading": "Restrained [Condition]", "line_start": 17066, "line_end": 17074, "span_sha256": "534f630cbdb2b9eee71b37543cb5f29af4617f829c0ab4b905604f69bfdbcf3c"},
    {"heading": "Ritual", "line_start": 17078, "line_end": 17080, "span_sha256": "3f4bc6da069b6634f84d1f834314e621a2b601f777d57d06e74d39bcd7514866"},
)
SEVENTH_COMMON_QUALIFIERS = (
    "Longer casting requires the Magic action each turn and Concentration even for an Instantaneous spell; interruption fails without spending the slot and casting must restart (9159–9161).",
    "Range governs where an effect originates and does not impose a generic post-creation leash; Familiar's explicit 100-foot predicates remain distinct (9165–9175).",
    "A ridden controlled mount moves on its rider's turn and has only Dash, Disengage and Dodge action options; an independent mount retains its own Initiative and acts as it likes. This does not decide every steed Bonus Action state (1328–1344).",
    "Same-spell overlap rules do not replace Warding Bond's explicit end-on-recast clause (9255–9257).",
    "Adjustment → Resistance → Vulnerability is the common damage order; it does not establish Warding Bond copied-occurrence identity, recursion or lifecycle ordering (1434–1450).",
    "A Cube origin may be anywhere on a face; side length defines size; origin is excluded unless the creator chooses otherwise, so it is not presumed centered (16360–16364).",
    "Concentration rules apply to the caster's separately maintained effects; this does not make Warding Bond itself a Concentration spell (16296–16304).",
    "Restrained sets Speed to 0 so it cannot increase, gives Advantage to attacks against the creature and Disadvantage on its attacks and Dexterity saves (17066–17074).",
    "A prepared Ritual takes ten minutes longer, spends no slot and cannot be upcast (17078–17080).",
)
SEVENTH_COMMON_REQUIRED_PHRASES: dict[str, tuple[str, ...]] = {
    "Longer Casting Times": ("must take the Magic action on each of your turns", "must maintain Concentration"),
    "Range": ("how far from the spellcaster the spell’s effect can originate", "aren’t restricted by its range unless"),
    "Mounted Combat": ("has only three action options during that turn", "retains its place in the Initiative order"),
    "Combining Spell Effects": ("same spell cast multiple times don’t combine", "most recent effect applies"),
    "Resistance and Vulnerability": ("Modifiers to damage are applied in the following order", "Resistance is applied second"),
    "Cube [Area of Effect]": ("origin located anywhere on a face", "isn’t included in the area of effect unless its creator decides otherwise"),
    "Concentration": ("moment you start casting a spell that requires Concentration", "half the damage taken", "up to a maximum DC of 30"),
    "Restrained [Condition]": ("Your Speed is 0 and can’t increase", "Disadvantage on Dexterity saving throws"),
    "Ritual": ("takes 10 minutes longer", "can’t be cast at a higher level"),
}
SEVENTH_FUTURE_PROOF_KEYS = frozenset({
    "source.spell.find_familiar.unresolved.eligible_form_census",
    "source.spell.warding_bond.unresolved.copied_damage_policy",
})
SEVENTH_SOURCE_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.augury.unresolved.four_omen_members": {
        "source_exact_name": "Augury", "classification_index": 6, "map_entry_index": 8, "source_pass_row": 9, "body_witness_row": 19, "printed_page": 111, "source_header_line": 9429,
        "raw_body_sha256": "39c373d26ae507e9ef9b00f138c75ffbb16e041d3b647d0a6e2bea0ff92fc36e",
        "dispositions": {"source_mapping_review": "SOURCE_CLOSED"},
        "locators": {"source_mapping_review": ({"heading": "Augury", "line_start": 9666, "line_end": 9693, "span_sha256": "4d975b5dc7df9709bb366aa7e6d792ee6a5fcc0d169ad8e3c74ae4eb842c7891"},)},
        "source_phrases": {"source_mapping_review": ((0, "The GM chooses the omen from the Omens table."), (0, "Weal | Good"), (0, "Woe | Bad"), (0, "Weal and woe | Good and bad"), (0, "Indifference | Neither good nor bad"), (0, "within the next 30 minutes"), (0, "doesn’t account for circumstances"))},
        "interpretations": {"source_mapping_review": "The table defines exactly four omen-to-result entries: Weal → Good; Woe → Bad; Weal and woe → Good and bad; Indifference → Neither good nor bad. The GM chooses the omen for a planned course of action within 30 minutes."},
        "required_qualifiers": {"source_mapping_review": ("Changed circumstances, including other spells, are not accounted for.", "The cumulative 25 percent no-answer chance on later castings before a Long Rest is a separate reviewed obligation, not a fifth omen.", "No guaranteed prediction, probability adjudication or online fallback is established.")},
    },
    "source.spell.find_familiar.unresolved.eligible_form_census": {
        "source_exact_name": "Find Familiar", "classification_index": 30, "map_entry_index": 48, "source_pass_row": 50, "body_witness_row": 117, "printed_page": 130, "source_header_line": 11241,
        "raw_body_sha256": "7ad9e1e88ac2c18e7f7573442ad84ecab53c842c4f0d22616cfd1b446215aac6",
        "dispositions": {"source_mapping_review": "SOURCE_HELD"},
        "locators": {"source_mapping_review": ({"heading": "Find Familiar", "line_start": 11609, "line_end": 11629, "span_sha256": "ab7a578e4bd70abb8a5c3d57a0733b0a5dfd33f2b444ae17b488f68437bd3b98"},)},
        "source_phrases": {"source_mapping_review": ((0, "Bat, Cat, Frog, Hawk, Lizard, Octopus, Owl, Rat, Raven, Spider, Weasel"), (0, "another Beast that has a Challenge Rating of 0"), (0, "statistics of the chosen form"), (0, "Celestial, Fey, or Fiend"), (0, "within 100 feet of you"), (0, "must take a Reaction to deliver the touch"), (0, "A familiar can’t attack, but it can take other actions as normal"), (0, "leaves behind in its space anything it was wearing or carrying"))},
        "interpretations": {"source_mapping_review": "The body names Bat, Cat, Frog, Hawk, Lizard, Octopus, Owl, Rat, Raven, Spider and Weasel, plus another Beast that has a Challenge Rating of 0. The chosen form supplies its statistics and special senses; the selected Celestial, Fey or Fiend type replaces Beast without broadening eligible forms."},
        "required_qualifiers": {"source_mapping_review": ("not the complete eligible-form census", "Only Beast forms with CR 0 are covered by the catch-all; no broader type or CR is admitted.", "The Celestial/Fey/Fiend override does not waive the underlying Beast/CR 0 predicate.", "The familiar rolls its own Initiative and acts on its own turn; it cannot attack but may take other actions normally.", "100-foot predicates are specific to telepathy and touch delivery, not a general command leash.", "Touch delivery uses the familiar's Reaction.", "Sensory relay uses the caster's Bonus Action through the start of the caster's next turn.", "Gear is left on zero HP or pocket disappearance, not every dismissal.", "Longer casting requires the Magic action each turn and Concentration; Ritual adds ten minutes and cannot be upcast.")},
    },
    "source.spell.find_steed.unresolved.type_to_action_mapping": {
        "source_exact_name": "Find Steed", "classification_index": 31, "map_entry_index": 49, "source_pass_row": 51, "body_witness_row": 118, "printed_page": 130, "source_header_line": 11284,
        "raw_body_sha256": "71a581b530f20eb4459e14de65b8d4fced42099209321bdf8106019119342420",
        "dispositions": {"source_mapping_review": "SOURCE_CLOSED"},
        "locators": {"source_mapping_review": ({"heading": "Find Steed", "line_start": 11633, "line_end": 11653, "span_sha256": "7a87d4710316fd37b8ba003941f1fa41d145538844af03bd21e676c4743f3ad0"}, {"heading": "Otherworldly Steed", "line_start": 11657, "line_end": 11696, "span_sha256": "e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2"})},
        "source_phrases": {"source_mapping_review": ((0, "This creature uses the **Otherworldly Steed** stat block."), (1, "Fell Glare (Fiend Only; Recharges after a Long Rest)"), (1, "Wisdom Saving Throw"), (1, "one creature within 60 feet the steed can see"), (1, "*Failure:* The target has the Frightened condition until the end of your next turn"), (1, "Fey Step (Fey Only; Recharges after a Long Rest)"), (1, "Healing Touch (Celestial Only; Recharges after a Long Rest)"), (1, "along with its rider"), (1, "One creature within 5 feet of the steed"), (1, "Radiant (Celestial), Psychic (Fey), or Necrotic (Fiend)"))},
        "interpretations": {"source_mapping_review": "Fiend → Fell Glare; Fey → Fey Step; Celestial → Healing Touch. Each is a Bonus Action that recharges after a Long Rest. Fell Glare is a Wisdom saving throw against the caster's spell save DC, targeting one creature within 60 feet of the steed that the steed can see. On failure, the target has the Frightened condition until the end of the caster's next turn. Fey Step takes the steed and rider to an unoccupied chosen space up to 60 feet from the steed. Healing Touch restores 2d8 plus spell level to one creature within 5 feet. Slam damage is Celestial → Radiant, Fey → Psychic, Fiend → Necrotic."},
        "required_qualifiers": {"source_mapping_review": ("No cross-type availability, action substitution, shared/short-rest recharge or rider-free extra teleport is inferred.", "A ridden controlled mount moves on the rider's turn and has only Dash, Disengage and Dodge action options.", "No action availability is inferred in every mount state from the type/action mapping.", "The absence of a rider does not categorically forbid Fey Step.", "Native resources, condition execution, healing, teleport and mount behavior remain NOT_ESTABLISHED.")},
    },
    "source.spell.find_steed.unresolved.steed_numeric_cells": {
        "source_exact_name": "Find Steed", "classification_index": 32, "map_entry_index": 49, "source_pass_row": 51, "body_witness_row": 118, "printed_page": 130, "source_header_line": 11284,
        "raw_body_sha256": "71a581b530f20eb4459e14de65b8d4fced42099209321bdf8106019119342420",
        "dispositions": {"source_parameter": "SOURCE_CLOSED", "source_mapping_review": "SOURCE_CLOSED"},
        "locators": {
            "source_parameter": ({"heading": "Otherworldly Steed", "line_start": 11657, "line_end": 11696, "span_sha256": "e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2"},),
            "source_mapping_review": ({"heading": "Find Steed", "line_start": 11633, "line_end": 11653, "span_sha256": "7a87d4710316fd37b8ba003941f1fa41d145538844af03bd21e676c4743f3ad0"}, {"heading": "Otherworldly Steed", "line_start": 11657, "line_end": 11696, "span_sha256": "e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2"}),
        },
        "source_phrases": {
            "source_parameter": ((0, "AC** 10 + 1 per spell level"), (0, "HP** 5 + 10 per spell level"), (0, "Fly 60 ft. (requires level 4+ spell)"), (0, "| Int | 6 | −2 | −2 |"), (0, "| Wis | 12 | +1 | +1 |"), (0, "| Cha | 8 | −1 | −1 |"), (0, "Passive Perception 11"), (0, "Telepathy 1 mile (works only with you)"), (0, "When you regain Hit Points from a level 1+ spell, the steed regains the same number of Hit Points if you’re within 5 feet of it."), (0, "1d8 plus the spell’s level"), (0, "2d8 plus the spell’s level")),
            "source_mapping_review": ((0, "This creature uses the **Otherworldly Steed** stat block."), (1, "Otherworldly Steed"), (1, "| Int | 6 | −2 | −2 |"), (1, "Bonus Actions"), (1, "Fey Step (Fey Only; Recharges after a Long Rest)")),
        },
        "interpretations": {
            "source_parameter": "Otherworldly Steed is Large; Celestial, Fey or Fiend by choice; Neutral; AC 10 + 1 per spell level; HP 5 + 10 per spell level; one d10 Hit Die per spell level; Speed 60 feet and Fly 60 feet only with a level 4+ spell. Scores/modifiers/saves are Str 18/+4/+4, Dex 12/+1/+1, Con 14/+2/+2, Int 6/−2/−2, Wis 12/+1/+1 and Cha 8/−1/−1. It has Passive Perception 11, caster-only 1-mile telepathy, no CR and 0 XP; PB equals the caster's. Life Bond triggers when the caster actually regains Hit Points from a level 1+ spell; if the caster is within 5 feet, the steed regains the same number of Hit Points the caster actually regained. Slam uses the caster's spell attack modifier, 5-foot reach and 1d8 plus spell level with the exact type mapping. The three type-limited Bonus Actions have their exact ranges, saves, healing, rider and Long Rest recharge. Upcasting uses the spell-slot level.",
            "source_mapping_review": "The Find Steed body names its Otherworldly Steed stat block. The current owning block is 11657–11696 before the Find the Path boundary. The existing find-steed-owner reconstruction witness accepts the Find Steed body and block and excludes the foreign continuation and page furniture; its machine support remains NOT_ESTABLISHED.",
        },
        "required_qualifiers": {
            "source_parameter": ("Preserve U+2212 in negative Int (−2/−2) and Cha (−1/−1) modifier/save cells; Wisdom is positive +1/+1.", "Use the slot level as spell level when upcast; do not substitute character level.", "Fly 60 feet requires a level 4+ spell.", "Life Bond requires actual HP regain by the caster from a level 1+ spell; mirror the amount actually regained, not rolled or nominal spell healing or overheal.", "Missing or unlisted values are not zero or arbitrary defaults.", "Rideable appearance does not import a horse or other ordinary animal stat block.", "These source cells do not admit native mount, action, health, teleport or healing behavior."),
            "source_mapping_review": ("Keep the Find the Path continuation out of the Find Steed block.", "The historical page 130/header and raw body hash are not the current Markdown block span or printed page 131 witness.", "No fresh PDF visual verification is claimed; existing VISUALLY_RECONSTRUCTED evidence remains distinct from machine support."),
        },
    },
    "source.spell.warding_bond.unresolved.copied_damage_policy": {
        "source_exact_name": "Warding Bond", "classification_index": 80, "map_entry_index": 136, "source_pass_row": 138, "body_witness_row": 329, "printed_page": 173, "source_header_line": 15429,
        "raw_body_sha256": "81941f005a019698af46d35f30a0afe20a613d8cc941a0c6deae0f4d95aa5cc6",
        "dispositions": {"source_semantics": "SOURCE_HELD"},
        "locators": {"source_semantics": ({"heading": "Warding Bond", "line_start": 15811, "line_end": 15825, "span_sha256": "cc1be68ce4911478cbf85ba39ea14612445549e3126ce317f8583707ce51a244"},)},
        "source_phrases": {"source_semantics": ((0, "a pair of platinum rings worth 50+ GP each"), (0, "Duration:** 1 hour"), (0, "within 60 feet of you"), (0, "Resistance to all damage"), (0, "each time it takes damage, you take the same amount of damage"), (0, "drop to 0 Hit Points"), (0, "cast again on either of the connected creatures"))},
        "interpretations": {"source_semantics": "A willing touched other creature must wear one of two platinum rings worth 50+ GP each for the one-hour duration; the spell itself is not Concentration. While within 60 feet, the target gains +1 AC and saving throws and Resistance to all damage, and each time the target takes damage the caster takes the same amount. It ends if the caster reaches 0 HP, separation exceeds 60 feet, or the spell is cast again on either connected creature."},
        "required_qualifiers": {"source_semantics": ("Warding Bond itself is not a Concentration spell.", "Recast on either connected creature explicitly ends the bond even where same-spell overlap rules also exist.", "The general adjustment → Resistance → Vulnerability order does not settle copied damage type or occurrence ordering.", "Damage may require a check for the caster's separately maintained Concentration effect; this does not make Warding Bond a second Concentration spell.", "No copied damage type, blanket unreducibility, reciprocal/recursive bond default or coupled health/Concentration/lifecycle ordering is selected.", "Native damage, health and Concentration proof remains NOT_ESTABLISHED.")},
    },
    "source.spell.web.unresolved.web_numeric_geometry": {
        "source_exact_name": "Web", "classification_index": 81, "map_entry_index": 137, "source_pass_row": 139, "body_witness_row": 332, "printed_page": 174, "source_header_line": 15474,
        "raw_body_sha256": "1b67beef86a550a46365f882a0e021ec7554fffcfc9813260355062c01a3985e",
        "dispositions": {"source_parameter": "SOURCE_CLOSED"},
        "locators": {"source_parameter": ({"heading": "Web", "line_start": 15863, "line_end": 15877, "span_sha256": "8de7309b0b27014012feaced44d167152956b95682a7e1c3b49465af12056cc6"},)},
        "source_phrases": {"source_parameter": ((0, "Range:** 60 feet"), (0, "20-foot Cube"), (0, "two solid masses"), (0, "at the start of your next turn"), (0, "depth of 5 feet"), (0, "The first time a creature enters the webs on a turn or starts its turn there"), (0, "Strength (Athletics) check against your spell save DC"), (0, "Any 5-foot Cube of webs exposed to fire burns away in 1 round"), (0, "2d4 Fire damage"), (0, "Concentration, up to 1 hour"))},
        "interpretations": {"source_parameter": "Web has 60-foot range and fills a 20-foot Cube for up to one hour with Concentration; it is Difficult Terrain and Lightly Obscured. It must be anchored between two solid masses or layered across a floor, wall or ceiling, or collapses and ends at the start of the caster's next turn. A flat-surface layer is 5 feet deep. The first entry on a turn or a creature's turn start calls for a Dexterity save; failure gives Restrained while in the webs or until freed. Escape takes an action for Strength (Athletics) against the caster's spell save DC. Each 5-foot Cube exposed to fire burns away in one round and deals 2d4 Fire to creatures that start their turn in that fire."},
        "required_qualifiers": {"source_parameter": ("Cube origin can be anywhere on a face.", "Cube origin is excluded unless the creator chooses otherwise.", "The Cube is not assumed centered on its origin point.", "Restrained sets Speed to 0 and affects attacks and Dexterity saves.", "The spell uses 20-foot Cube, not a 20-foot radius.", "Burning one local 5-foot Cube does not erase the whole Web area.", "Entry triggers follow first-entry-on-a-turn or start-own-turn wording, not unlimited repeat checks.", "Fire damage applies to creatures starting their turn in the fire, not automatically on contact.", "Spatial/condition/fire consumer admission and complete recipe proof remain NOT_ESTABLISHED.")},
    },
}
SEVENTH_SOURCE_RESIDUALS: dict[tuple[str, str], str] = {
    ("source.spell.augury.unresolved.four_omen_members", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the four table members and their meanings are source-closed. Changed circumstances and the separate repeat-casting no-answer obligation remain distinct.",
    ("source.spell.find_familiar.unresolved.eligible_form_census", "source_mapping_review"): "HOLD_SOURCE_SUBOBLIGATION; the eleven named examples plus the CR 0 Beast predicate do not establish the complete eligible SRD CR 0 Beast census. Do not guess a roster; source-member census remains unresolved and separate native action/sense proof remains NOT_ESTABLISHED.",
    ("source.spell.find_steed.unresolved.type_to_action_mapping", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the three type-limited Bonus Action mappings, rider/target/range/duration and Slam type relations are source-closed. Action availability in each control state and native mount/action execution remain NOT_ESTABLISHED.",
    ("source.spell.find_steed.unresolved.steed_numeric_cells", "source_parameter"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; all enumerated stat, save, speed, scaling, Slam and Bonus Action cells are source-closed. No native stat/action/health or mount consumer is admitted.",
    ("source.spell.find_steed.unresolved.steed_numeric_cells", "source_mapping_review"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; the displaced block's owning Markdown body and boundary are source-mapped. No foreign Find the Path continuation is admitted; reconstruction machine support remains NOT_ESTABLISHED.",
    ("source.spell.warding_bond.unresolved.copied_damage_policy", "source_semantics"): "HOLD_SOURCE_SUBOBLIGATION; copied damage type, full defense/recursion behavior and coupled health/Concentration/lifecycle ordering remain unresolved. Preserve the explicit recast ending; choose no recursive-bond default or damage policy.",
    ("source.spell.web.unresolved.web_numeric_geometry", "source_parameter"): "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; exact source range, Cube, anchoring, collapse, layer, entry/save, escape, burn and fire-damage values are source-closed with common Cube-origin and Restrained qualifications. Spatial/condition/fire consumer admission and recipe proof remain NOT_ESTABLISHED.",
}
SEVENTH_SOURCE_CLOSED_KEYS = frozenset(
    key for key, item in SEVENTH_SOURCE_ITEMS.items()
    if "SOURCE_CLOSED" in item["dispositions"].values()
    and "SOURCE_HELD" not in item["dispositions"].values()
)
SEVENTH_SOURCE_HELD_KEYS = frozenset(
    key for key, item in SEVENTH_SOURCE_ITEMS.items()
    if "SOURCE_HELD" in item["dispositions"].values()
)

SOURCE_INTERPRETATION_OWNER: dict[str, object] = {
    "authority": "ACCEPTED_PRODUCT_OWNER_DECISION",
    "status": "ACCEPTED_PRODUCT_OWNER_DECISION",
    "decision_path": "DEV/docs/superpowers/specs/2026-10-14-sp00-source-interpretation-owner-decision.md",
    "decision_sha256": "9de384b36657bafe7e93252959825ed4ba4494f287ee972904d589f5c8759e5c",
    "decision_git_blob": "662d17d8299fae1ac264863a7da31bd99a9da183",
    "review_path": "DEV/docs/superpowers/design/2026-10-14-sp00-source-interpretation-review.md",
    "review_sha256": "c23981544f9dd0cac9e90f9fd6fe5020bb756bd16fd7cb5a2f0878e6c783b581",
    "historical_brief_path": "DEV/docs/superpowers/design/2026-10-13-sp00-source-interpretation-decision-brief.md",
    "historical_brief_sha256": "ba763309d102089ac82853178f072e2c3e5b09f2d874a3f11d611f06e3226e6a",
    "accepted_scope": "EXACTLY_SIX_NAMED_SP00_SOURCE_INTERPRETATION_SUBOBLIGATIONS; NO_NATIVE_CONSUMER_PROOF_OR_PACKAGE_READINESS",
    "accepted_sections": ["A", "B", "C", "D", "E", "F"],
    "accepted_keys": [
        "source.spell.aid.unresolved.health_normalization_policy",
        "source.spell.magic_missile.unresolved.rng_damage_grouping",
        "source.spell.pass_without_trace.unresolved.selection_timing",
        "source.spell.ray_of_frost.unresolved.movement_composition",
        "source.spell.resistance.unresolved.damage_grouping_order",
        "source.spell.warding_bond.unresolved.copied_damage_policy",
    ],
}

SOURCE_EIGHTH_ITEMS: dict[str, dict[str, object]] = {
    "source.spell.aid.unresolved.health_normalization_policy": {
        "review_item_id": "OWNER-A", "source_exact_name": "Aid", "source_category": "source_semantics",
        "owner_section": "A", "owner_section_heading": "Aid — reversible effective current-HP contribution",
        "classification_index": 0, "map_entry_index": 2, "source_pass_row": 2, "body_witness_row": 2,
        "printed_page": 107, "source_header_line": 9021,
        "raw_body_sha256": "40d66aae2ec29df83884c0d92830ddf6cc2c548bf81694f1e2d212483d1bb27b",
        "markdown_locator": {"heading": "Aid", "line_start": 9307, "line_end": 9321, "span_sha256": "735037ddd8bc5621e8e0a5fade21ea6bc73c26c688d93115911b88a36b4863a0"},
        "source_phrases": [(0, "Each target’s Hit Point maximum and current Hit Points increase by 5 for the duration.")],
        "source_grounding_status": "SOURCE_BODY_HAS_DURATION_BONUS; OWNER_DECIDES_EFFECTIVE_DELTA_POLICY",
        "source_grounded_findings": ["The SRD states that Aid raises target maximum and current Hit Points by 5 for the duration; the effective-bonus delta and overlap arithmetic are not explicit in that clause."],
        "accepted_interpretation": "For a lawful application, expiry, suppression, resumption or overlap-winner transition, change current HP by the change in effective applicable Aid bonus; normalize to zero and the current derived maximum while preserving actual intervening damage and healing.",
        "material_qualifiers": [
            "The duration-bound current-HP increase is source text; reversible effective-bonus delta arithmetic is the accepted HDM owner interpretation.",
            "Same-spell highest-potency/latest-equal arbitration remains unchanged; no independent stacking or repeated healing from unchanged arbitration.",
            "Actor HP remains the sole amount; the bonus is not temporary HP or a second mutable health balance, and entry HP is never restored.",
            "Reaching zero is not damage and creates no invented death-save failure; LifeState and target eligibility remain under existing owners, and dead subjects are not revived.",
            "Native health and required LifeState atomic closure remain FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; do not claim the full arithmetic as explicit SRD wording. Native health and LifeState proof remain FUTURE_PROOF / NOT_ESTABLISHED.",
    },
    "source.spell.magic_missile.unresolved.rng_damage_grouping": {
        "review_item_id": "OWNER-B", "source_exact_name": "Magic Missile", "source_category": "source_semantics",
        "owner_section": "B", "owner_section_heading": "Magic Missile — per-dart instances in one simultaneous group",
        "classification_index": 52, "map_entry_index": 85, "source_pass_row": 87, "body_witness_row": 198,
        "printed_page": 146, "source_header_line": 12789,
        "raw_body_sha256": "0f691800c3e9c5664ebd220ade84cb02ffff15989cecfa111fb365835724019c",
        "markdown_locator": {"heading": "Magic Missile", "line_start": 13259, "line_end": 13273, "span_sha256": "e772f726833c5dcb9d05591eeb8537634ea860acf3412da63fb95599182b2a0d"},
        "source_phrases": [(0, "A dart deals 1d4 + 1 Force damage to its target."), (0, "The darts all strike simultaneously")],
        "source_grounding_status": "INDEPENDENT_DICE_AND_SIMULTANEOUS_GROUP_SOURCE_GROUNDED; OWNER_DECIDES_DAMAGE_INSTANCE_POLICY",
        "source_grounded_findings": ["Ordinary independent damage-die draws are source-grounded; the SRD says each dart deals 1d4 + 1 Force and all darts strike simultaneously."],
        "accepted_interpretation": "Each damaging dart is a distinct damage instance with its own Concentration obligation while the recipient remains concentrating; every dart in the cast remains in one simultaneous group.",
        "material_qualifiers": [
            "Independent dart draws and the simultaneous strike are source-grounded; per-dart damage-instance and Concentration grouping is the accepted owner interpretation.",
            "Distinct instances are not sequential fictional attacks; actual turn-controller ordering applies and engine iteration cannot substitute for a lawful choice.",
            "Draw, request, instance and group identity comes from accepted source occurrence, not caller list order or ambient RNG; retry and recovery reuse fixed results.",
            "Do not make unnecessary saves after Concentration actually ends; damage reduction, rounding, zero-HP and death-save interactions retain their exact qualifications.",
            "Production RNG, damage and Concentration realization remain FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; the source-grounded draw/group clauses do not make per-dart instance grouping explicit SRD wording. Production proof remains FUTURE_PROOF / NOT_ESTABLISHED.",
    },
    "source.spell.pass_without_trace.unresolved.selection_timing": {
        "review_item_id": "OWNER-C", "source_exact_name": "Pass without Trace", "source_category": "source_semantics",
        "owner_section": "C", "owner_section_heading": "Pass without Trace — cast-time membership",
        "classification_index": 60, "map_entry_index": 95, "source_pass_row": 97, "body_witness_row": 224,
        "printed_page": 151, "source_header_line": 13298,
        "raw_body_sha256": "68b06279a1f031bb6976a24099a1972bce808c44b3c27a6f9f61b7c67d228407",
        "markdown_locator": {"heading": "Pass without Trace", "line_start": 13735, "line_end": 13747, "span_sha256": "5286728517f232fad21e7a35ba72d36862ab98170e3a06ca57889586678a2132"},
        "source_phrases": [(0, "each creature you choose have a +10 bonus to Dexterity (Stealth) checks")],
        "source_grounding_status": "SOURCE_BODY_DOES_NOT_SPECIFY_MEMBERSHIP_TIMING; OWNER_DECIDES_CAST_TIME",
        "source_grounded_findings": ["The SRD gives a chosen-creature set and grants its benefits while each selected creature is in the 30-foot Emanation; it does not state when membership is selected or changed."],
        "accepted_interpretation": "Commit selected creature identities at casting and preserve that membership through lawful leave and reentry; benefits apply only while a selected creature is inside the current aura.",
        "material_qualifiers": [
            "Cast-time membership is the accepted HDM owner interpretation, not a timing rule stated by the SRD.",
            "A later unselected entrant gains no benefit by arrival alone; no free reassignment or new update action is granted.",
            "Current aura geometry, occupancy, duration, target legality and caster benefit remain unchanged; no generic ongoing caster-to-target range leash is added.",
            "Spatial eligibility and native membership consumers remain FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; source timing ambiguity is not relabeled as explicit SRD wording. Spatial and native proof remain FUTURE_PROOF / NOT_ESTABLISHED.",
    },
    "source.spell.ray_of_frost.unresolved.movement_composition": {
        "review_item_id": "OWNER-D", "source_exact_name": "Ray of Frost", "source_category": "source_parameter",
        "owner_section": "D", "owner_section_heading": "Speed — final nonnegative movement capability",
        "classification_index": 66, "map_entry_index": 105, "source_pass_row": 107, "body_witness_row": 251,
        "printed_page": 157, "source_header_line": 13876,
        "raw_body_sha256": "acbf5544ece9d8b267804f550f65e342733ad0d02eb95f8ee6c0e11d30f3cb35",
        "markdown_locator": {"heading": "Ray of Frost", "line_start": 14272, "line_end": 14286, "span_sha256": "dae3f77c2b494c1afd20ba279f16583438d1df80127bf260e3a243c491b77ea0"},
        "source_phrases": [(0, "its Speed is reduced by 10 feet until the start of your next turn")],
        "source_grounding_status": "SOURCE_BODY_STATES_NEGATIVE_MODIFIER; OWNER_DECIDES_FINAL_NONNEGATIVE_FLOOR",
        "source_grounded_findings": ["The SRD's Ray of Frost rider reduces Speed by 10 feet; its remaining-movement switching rule does not define a universal derived-Speed floor."],
        "accepted_interpretation": "After complete lawful modifier composition, floor each resulting derived movement capability at zero; retain raw negative contributions and exact special-speed propagation and remaining-movement rules.",
        "material_qualifiers": [
            "The final nonnegative capability floor is the accepted HDM owner interpretation, not an explicit minimum in the Ray of Frost clause or Speed glossary.",
            "Never floor each contribution independently or use source order to choose a result; preserve raw negative contributions and exact special-speed changes.",
            "Exact-zero consumers observe the final capability, including Dodge, voluntary Prone, standing and flying as applicable.",
            "Schema minima do not implement runtime behavior; movement-mode and budget consumers remain FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; this closes the accepted movement-normalization interpretation without claiming literal SRD floor text. Native movement proof remains FUTURE_PROOF / NOT_ESTABLISHED.",
    },
    "source.spell.resistance.unresolved.damage_grouping_order": {
        "review_item_id": "OWNER-E", "source_exact_name": "Resistance", "source_category": "source_semantics",
        "owner_section": "E", "owner_section_heading": "Resistance — automatic chosen-type-only reduction",
        "classification_index": 68, "map_entry_index": 107, "source_pass_row": 109, "body_witness_row": 257,
        "printed_page": 158, "source_header_line": 13968,
        "raw_body_sha256": "f13455e2f9b58c45a738c097b310d12495a006028c9720b8047d941dd52e885b",
        "markdown_locator": {"heading": "Resistance", "line_start": 14389, "line_end": 14401, "span_sha256": "c8eb5178fade2834aa5ad5c504723c2499bcbfaeeb821d120b5dbc729ab3432c"},
        "source_phrases": [(0, "When the creature takes damage of the chosen type before the spell ends"), (0, "only once per turn")],
        "source_grounding_status": "AUTOMATIC_TRIGGER_AND_ONCE_PER_TURN_SOURCE_GROUNDED; OWNER_DECIDES_CHOSEN_TYPE_ONLY_MIXED_ALLOCATION",
        "source_grounded_findings": ["The automatic chosen-type trigger and once-per-turn reduction are source-grounded; the source grants no elective withholding or Reaction, while mixed-type allocation is not specified."],
        "accepted_interpretation": "Automatically use the first eligible positive damaging occurrence of each actual turn; reduce only the selected damage-type subtotal by one fixed d4, floor that subtotal at zero with no spill, then apply ordinary type defenses.",
        "material_qualifiers": [
            "The automatic prescribed occurrence and once-per-turn rule are source-grounded; the target-local actual-turn gate includes other creatures' turns under the accepted lifecycle rule.",
            "Chosen-type-only/no-spill mixed allocation is an accepted HDM owner interpretation, not explicit SRD allocation; do not roll per component or grant elective withholding.",
            "A fully prevented effect does not consume the gate; evaluate prospective eligibility rather than substituting physical current-HP loss for damage taken.",
            "5 Fire + 5 Cold, selected Fire, d4 = 3 and ordinary Fire Resistance yields floor((5-3)/2)+5=6; excess reduction cannot change Cold.",
            "Gate consumption and accepted health changes require native causal/atomic closure, which remains FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; chosen-type-only/no-spill allocation is not labeled explicit SRD wording. Native damage and atomicity proof remain FUTURE_PROOF / NOT_ESTABLISHED.",
        "golden_witness": {
            "components": [{"damage_type": "Fire", "amount": 5}, {"damage_type": "Cold", "amount": 5}],
            "chosen_damage_type": "Fire", "fixed_d4_result": 3,
            "selected_type_subtotal_after_reduction": 2, "ordinary_resistance_type": "Fire",
            "selected_type_damage_after_defense": 1, "unselected_type_damage": 5,
            "expected_total_damage": 6,
        },
    },
    "source.spell.warding_bond.unresolved.copied_damage_policy": {
        "review_item_id": "OWNER-F", "source_exact_name": "Warding Bond", "source_category": "source_semantics",
        "owner_section": "F", "owner_section_heading": "Warding Bond — linked typed input with ordinary caster defenses",
        "classification_index": 80, "map_entry_index": 136, "source_pass_row": 138, "body_witness_row": 329,
        "printed_page": 173, "source_header_line": 15429,
        "raw_body_sha256": "81941f005a019698af46d35f30a0afe20a613d8cc941a0c6deae0f4d95aa5cc6",
        "markdown_locator": {"heading": "Warding Bond", "line_start": 15811, "line_end": 15825, "span_sha256": "cc1be68ce4911478cbf85ba39ea14612445549e3126ce317f8583707ce51a244"},
        "source_phrases": [(0, "each time it takes damage, you take the same amount of damage")],
        "source_grounding_status": "SOURCE_BODY_STATES_SAME_DAMAGE_AMOUNT; OWNER_DECIDES_TYPED_INPUT_AND_PROXIMATE_CAUSE",
        "source_grounded_findings": ["The SRD states that each time the target takes damage, the caster takes the same amount; the accepted owner decision clarifies input typing, defense order and proximate cause."],
        "accepted_interpretation": "Copy target-taken typed damage after target defenses and before HP allocation as a linked input; apply the caster's ordinary defenses and temporary-HP buffer, with Warding Bond as the new proximate cause.",
        "material_qualifiers": [
            "Neither raw attack damage nor physical current-HP loss defines the copied amount; damage absorbed entirely by target temporary HP still supplies the link.",
            "Retain original causal-link, type and amount evidence, but do not blindly copy attack/origin/bypass attributes whose source conditions do not apply to the new Warding Bond cause.",
            "No exceptional final-loss equality or unexpressed defense bypass is selected; target taking 5 Fire leads to a resistant caster taking 2 before its temporary HP.",
            "Explicit recast/range/caster-zero termination and each participant's separate actual Concentration remain; Warding Bond is not itself Concentration and no reciprocal recursive default is added.",
            "Native linked-damage, health and Concentration proof remains FUTURE_PROOF / NOT_ESTABLISHED.",
        ],
        "retained_source_residual": "OWNER_DECISION_ACCEPTED_FOR_SELECTED_SUBOBLIGATION_ONLY; the typed-input/ordinary-defense profile is accepted HDM interpretation, not a claim of extra literal SRD wording. Native proof remains FUTURE_PROOF / NOT_ESTABLISHED.",
    },
}


def _read_pinned_local_evidence(
    relative_path: str, expected_sha256: str, evidence_name: str
) -> bytes:
    path = (REPOSITORY_ROOT / relative_path).resolve()
    if not path.is_relative_to(REPOSITORY_ROOT) or not path.is_file():
        _fail(evidence_name, "pinned local evidence is unavailable")
    try:
        data = path.read_bytes()
    except OSError:
        _fail(evidence_name, "pinned local evidence cannot be read")
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        _fail(evidence_name, "pinned local evidence bytes changed")
    return data


def _validate_source_unknown_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the reviewed first12 dispositions to current Markdown and old witnesses."""
    expected_markdown_source = {
        "path": SOURCE_MARKDOWN_RELATIVE_PATH,
        "asset_id": "srd52_en",
        "edition": "SRD_5_2_1",
        "sha256": SOURCE_MARKDOWN_SHA256,
        "hash_basis": "RAW_UTF8",
        "license_id": "CC-BY-4.0",
        "required_attribution": ATTRIBUTION,
    }
    markdown_source = _object(
        manifest.get("source_markdown_source"), "source_markdown_source"
    )
    if markdown_source != expected_markdown_source:
        _fail(
            "source_unknown_resolution_markdown",
            "source Markdown identity, license or attribution differs",
        )
    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH,
        SOURCE_MARKDOWN_SHA256,
        "source_unknown_resolution_markdown",
    )
    try:
        markdown_lines = markdown_bytes.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        _fail("source_unknown_resolution_markdown", "source Markdown is not UTF-8")

    review = _object(manifest.get("source_residual_review"), "source_residual_review")
    if review != SOURCE_RESIDUAL_REVIEW:
        _fail(
            "source_unknown_resolution_review",
            "frozen candidate, accepted review or task evidence identity differs",
        )
    task_evidence_bytes = _read_pinned_local_evidence(
        SOURCE_RESIDUAL_EVIDENCE_RELATIVE_PATH,
        SOURCE_RESIDUAL_EVIDENCE_SHA256,
        "source_unknown_resolution_review",
    )
    try:
        task_evidence = task_evidence_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_unknown_resolution_review", "task evidence is not UTF-8")
    required_review_tokens = (
        review["accepted_review_sha256"],
        review["candidate_sha256"],
        "F12-01 incorporation",
        "if it moves within 5 feet of the caster",
        *SOURCE_RESOLUTION_KEYS,
    )
    if any(token not in task_evidence for token in required_review_tokens):
        _fail(
            "source_unknown_resolution_review",
            "task evidence omits a frozen review identity, key or Command correction",
        )

    rows = [
        _object(value, f"source_unknown_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_unknown_resolution_evidence"),
                "source_unknown_resolution_evidence",
            )
        )
    ]
    if (
        len(rows) != len(SOURCE_RESOLUTION_KEYS)
        or tuple(row.get("unresolved_key") for row in rows) != SOURCE_RESOLUTION_KEYS
    ):
        _fail(
            "source_unknown_resolution_census",
            "the twelve reviewed residual identities or their order differ",
        )

    source_pass_pointers: list[str] = []
    body_witness_pointers: list[str] = []
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_subobligation_ids: list[str] = []
    command_approach_source_text = ""
    for index, row in enumerate(rows, start=1):
        key = SOURCE_RESOLUTION_KEYS[index - 1]
        classification = classified_by_key.get(key)
        if classification is None:
            _fail(
                "source_unknown_resolution_key", f"{key} has no original classification"
            )
        source_name = str(classification["source_exact_name"])
        expected_subobligation_id = f"{key}::{SOURCE_RESOLUTION_CATEGORIES[key]}"
        source_subobligations = [
            _object(value, f"{key}.subobligation")
            for value in _array(
                classification.get("subobligations"), f"{key}.subobligations"
            )
            if isinstance(value, dict)
            and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        if (
            len(source_subobligations) != 1
            or source_subobligations[0].get("subobligation_id")
            != expected_subobligation_id
            or source_subobligations[0].get("status") != "NOT_ESTABLISHED"
        ):
            _fail(
                "source_unknown_resolution_subobligation",
                f"{key} does not contain exactly the reviewed open source subobligation",
            )
        evidence_ref = _object(
            classification.get("evidence_ref"), f"{key}.evidence_ref"
        )
        expected_record_ref = {
            "artifact_id": evidence_ref.get("artifact_id"),
            "json_pointer": evidence_ref.get("json_pointer"),
            "source_exact_name": evidence_ref.get("exact_record_name"),
            "printed_page": evidence_ref.get("printed_page"),
            "source_header_line": evidence_ref.get("source_header_line"),
            "raw_body_sha256": evidence_ref.get("raw_body_sha256"),
            "body_witness_ref": evidence_ref.get("body_witness_ref"),
        }
        expected_disposition = (
            "SOURCE_CLOSED" if key in SOURCE_RESOLVED_KEYS else "SOURCE_HELD"
        )
        expected_item_id = f"ITEM-{index:02d}"
        if (
            key not in SOURCE_RESOLVED_KEYS | SOURCE_HELD_KEYS
            or row.get("review_item_id") != expected_item_id
            or row.get("source_exact_name") != source_name
            or row.get("subobligation_id") != expected_subobligation_id
            or row.get("disposition") != expected_disposition
            or row.get("source_record_ref") != expected_record_ref
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_unknown_resolution_binding",
                f"{key} differs from its reviewed source record/subobligation binding",
            )

        locators = [
            _object(value, f"{key}.source_markdown_locators[{locator_index}]")
            for locator_index, value in enumerate(
                _array(
                    row.get("source_markdown_locators"),
                    f"{key}.source_markdown_locators",
                )
            )
        ]
        if locators != SOURCE_MARKDOWN_LOCATORS[key]:
            _fail(
                "source_unknown_resolution_locator",
                f"{key} Markdown line locators differ from the reviewed source route",
            )
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                not isinstance(start, int)
                or not isinstance(end, int)
                or start < 1
                or end < start
                or end > len(markdown_lines)
            ):
                _fail(
                    "source_unknown_resolution_locator",
                    f"{key} has an invalid Markdown line span",
                )
            section_text = "\n".join(markdown_lines[start - 1 : end])
            locator_texts.append(section_text)
            if locator_index == 0 and markdown_lines[start - 1].strip() != (
                f"##### {source_name}"
            ):
                _fail(
                    "source_unknown_resolution_locator",
                    f"{key} primary Markdown span does not start at its exact heading",
                )
            first_line = markdown_lines[start - 1].strip()
            if first_line.startswith("#") and locator.get("heading") not in first_line:
                _fail(
                    "source_unknown_resolution_locator",
                    f"{key} Markdown span heading does not match its locator",
                )
        for locator_index, phrase in SOURCE_MARKDOWN_REQUIRED_PHRASES[key]:
            if phrase not in locator_texts[locator_index]:
                _fail(
                    "source_unknown_resolution_source_text",
                    f"{key} source Markdown span omits a required source phrase",
                )

        interpretation = row.get("source_interpretation")
        retained_residual = row.get("retained_source_residual")
        qualifiers = row.get("material_qualifiers")
        if (
            not isinstance(interpretation, str)
            or not interpretation.strip()
            or not isinstance(qualifiers, list)
            or not qualifiers
            or not all(isinstance(value, str) and value.strip() for value in qualifiers)
            or not isinstance(retained_residual, str)
            or not retained_residual.strip()
        ):
            _fail(
                "source_unknown_resolution_formulation",
                f"{key} lacks a concise interpretation, qualifiers or explicit residual",
            )
        if expected_disposition == "SOURCE_HELD":
            if retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY"
            ):
                _fail("source_unknown_resolution_hold", f"{key} hold was removed")
            held_keys.append(key)
        else:
            if not retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY"
            ):
                _fail(
                    "source_unknown_resolution_closure",
                    f"{key} does not limit its closure to the selected subobligation",
                )
            closed_keys.append(key)
            closed_subobligation_ids.append(expected_subobligation_id)
        source_pass_pointers.append(str(expected_record_ref["json_pointer"]))
        body_witness_pointers.append(
            str(
                _object(expected_record_ref["body_witness_ref"], "body_witness_ref")[
                    "json_pointer"
                ]
            )
        )
        if key == "source.spell.command.unresolved.command_exact_restrictions":
            command_approach_source_text = next(
                line for line in locator_texts[0].splitlines() if "Approach." in line
            )
            if (
                "if it moves within 5 feet of you" not in command_approach_source_text
                or "if within 5 feet" in interpretation
                or "if it moves within 5 feet" not in interpretation
            ):
                _fail(
                    "source_unknown_resolution_command_approach",
                    "Command Approach must retain the movement-conditioned 5-foot clause",
                )

    contract = _object(
        manifest.get("source_unknown_resolution_contract"),
        "source_unknown_resolution_contract",
    )
    expected_contract = {
        "status": "PARTIAL_FIRST12_SOURCE_ONLY",
        "reviewed_record_count": 12,
        "source_closed_subobligation_count": 9,
        "source_held_subobligation_count": 3,
        "active_source_blocker_count": 68,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
    }
    if (
        contract != expected_contract
        or set(closed_keys) != SOURCE_RESOLVED_KEYS
        or set(held_keys) != SOURCE_HELD_KEYS
    ):
        _fail(
            "source_unknown_resolution_contract",
            "first12 source closure/hold counts or partial claim differs",
        )
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_subobligation_ids,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_held_subobligation_count": len(held_keys),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
        "source_pass_pointers": source_pass_pointers,
        "body_witness_pointers": body_witness_pointers,
        "command_approach_source_text": command_approach_source_text,
    }


def _validate_source_next12_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the independently reviewed next12 source dispositions and provenance."""
    review = _object(manifest.get("source_next12_review"), "source_next12_review")
    if review != SOURCE_NEXT12_REVIEW:
        _fail(
            "source_next12_review", "frozen candidate/review/evidence identity differs"
        )

    task_evidence_bytes = _read_pinned_local_evidence(
        SOURCE_NEXT12_EVIDENCE_RELATIVE_PATH,
        SOURCE_NEXT12_EVIDENCE_SHA256,
        "source_next12_review",
    )
    try:
        task_evidence = task_evidence_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_next12_review", "task evidence is not UTF-8")
    required_tokens = (
        review["candidate_sha256"],
        review["candidate_summary_sha256"],
        review["accepted_review_sha256"],
        *NEXT12_REQUIRED_EVIDENCE_TOKENS,
        *NEXT12_SELECTED_KEYS,
    )
    if any(token not in task_evidence for token in required_tokens):
        _fail(
            "source_next12_review",
            "bounded evidence omits frozen identities, selected keys or R02/R03 qualifiers",
        )

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH,
        SOURCE_MARKDOWN_SHA256,
        "source_next12_markdown",
    )
    try:
        markdown_lines = markdown_bytes.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        _fail("source_next12_markdown", "source Markdown is not UTF-8")

    rows = [
        _object(value, f"source_next12_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_next12_resolution_evidence"),
                "source_next12_resolution_evidence",
            )
        )
    ]
    if len(rows) != len(NEXT12_EVIDENCE_ORDER):
        _fail(
            "source_next12_census",
            "the next12 source-subobligation record count differs",
        )

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_witnesses = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    witness_rows = _rows(body_witnesses, "rows", "source-body-witnesses")

    lanes = [
        _object(value, f"source_mapping_lanes[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        )
    ]
    lane0 = next(
        (lane for lane in lanes if lane.get("lane_id") == "source-pass-0-2"), None
    )
    if lane0 is None:
        _fail("source_next12_map", "source-pass 0-2 mapping lane is missing")
    lane0_payload = _object(
        lane0.get("mapping_payload"), "source-pass-0-2.mapping_payload"
    )

    expected_order = tuple(
        (item_id, key, category) for item_id, key, category in NEXT12_EVIDENCE_ORDER
    )
    actual_order: list[tuple[str, str, str]] = []
    for row_index, row in enumerate(rows):
        subobligation_id = _string(
            row.get("subobligation_id"),
            f"source_next12_resolution_evidence[{row_index}].subobligation_id",
        )
        if "::" not in subobligation_id:
            _fail("source_next12_binding", "source subobligation ID lacks its category")
        category = subobligation_id.rsplit("::", 1)[1]
        actual_order.append(
            (
                str(row.get("review_item_id")),
                str(row.get("unresolved_key")),
                category,
            )
        )
    if tuple(actual_order) != expected_order or len(
        {row.get("review_item_id") for row in rows}
    ) != len(rows):
        _fail(
            "source_next12_census",
            "selected keys, source categories, Druidcraft split or review order differs",
        )

    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_subobligation_ids: list[str] = []
    held_subobligation_ids: list[str] = []
    for row_index, (row, (item_id, key, category)) in enumerate(
        zip(rows, NEXT12_EVIDENCE_ORDER, strict=True)
    ):
        spec = NEXT12_SOURCE_ITEMS[key]
        classification_index = int(spec["classification_index"])
        map_entry_index = int(spec["map_entry_index"])
        source_pass_row = int(spec["source_pass_row"])
        body_witness_row = int(spec["body_witness_row"])
        source_name = str(spec["source_exact_name"])
        disposition = str(spec["disposition"])
        expected_subobligation_id = f"{key}::{category}"
        classification_pointer = (
            f"/source_unknown_classifications/{classification_index}"
        )
        history_pointer = (
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/"
            f"{classification_index}"
        )
        map_pointer = (
            f"/source_mapping_lanes/0/mapping_payload/entries/{map_entry_index}"
        )
        source_pointer = f"/rows/{source_pass_row}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{source_pass_row}/qualifications"
        body_pointer = f"/rows/{body_witness_row}"

        classification = classified_by_key.get(key)
        if classification is None or classification_index >= len(
            _array(
                manifest.get("source_unknown_classifications"),
                "source_unknown_classifications",
            )
        ):
            _fail("source_next12_key", f"{key} has no exact original classification")
        original_classification = _object(
            _resolve_json_pointer(
                manifest, classification_pointer, "next12 classification pointer"
            ),
            f"{key}.classification",
        )
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != source_name
            or row.get("subobligation_id") != expected_subobligation_id
            or row.get("disposition") != disposition
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original_classification
            or original_classification.get("unresolved_key") != key
            or original_classification.get("source_exact_name") != source_name
            or original_classification.get("source_unresolved_record_pointer")
            != history_pointer
            or original_classification.get("classification_status")
            != spec["classification_status"]
            or original_classification.get("source_ready_blocking") is not True
            or original_classification.get("original_status") != "NOT_ESTABLISHED"
        ):
            _fail(
                "source_next12_binding",
                f"{key} differs from its exact original key/map binding",
            )

        original_history = _object(
            _resolve_json_pointer(
                manifest, history_pointer, "next12 original history pointer"
            ),
            f"{key}.original_history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "next12 current map pointer"),
            f"{key}.current_map",
        )
        map_unresolved_keys = [
            _object(value, f"{key}.map.unresolved_keys[{index}]")
            for index, value in enumerate(
                _array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys")
            )
        ]
        if (
            original_history.get("unresolved_key") != key
            or map_entry.get("source_exact_name") != source_name
            or not any(
                value.get("unresolved_key") == key for value in map_unresolved_keys
            )
        ):
            _fail(
                "source_next12_map",
                f"{key} borrows an unrelated history or entry-map record",
            )

        source_subobligations = [
            _object(value, f"{key}.source_subobligation")
            for value in _array(
                original_classification.get("subobligations"), f"{key}.subobligations"
            )
            if isinstance(value, dict)
            and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        expected_categories = spec.get("categories", (spec.get("category"),))
        if isinstance(expected_categories, str):
            expected_categories = (expected_categories,)
        if category not in expected_categories or not any(
            value.get("subobligation_id") == expected_subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            for value in source_subobligations
        ):
            _fail(
                "source_next12_subobligation",
                f"{key} does not retain the exact open {category} subobligation",
            )

        source_record = source_rows[source_pass_row]
        body_witness = witness_rows[body_witness_row]
        body_sha256 = str(spec["raw_body_sha256"])
        printed_page = int(spec["printed_page"])
        source_header_line = int(spec["source_header_line"])
        expected_source_record = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": source_name,
            "printed_page": printed_page,
            "source_header_line": source_header_line,
            "raw_body_sha256": body_sha256,
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
        }
        evidence_ref = _object(
            original_classification.get("evidence_ref"), f"{key}.evidence_ref"
        )
        if (
            source_record.get("name") != source_name
            or source_record.get("source_page") != printed_page
            or source_record.get("source_header_line") != source_header_line
            or source_record.get("body_sha256") != body_sha256
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != source_name
            or body_witness.get("page") != printed_page
            or body_witness.get("line") != source_header_line
            or body_witness.get("body_sha256") != body_sha256
            or row.get("source_record_ref") != expected_source_record
            or evidence_ref.get("artifact_id") != "source-pass-0-2"
            or evidence_ref.get("json_pointer") != source_pointer
            or evidence_ref.get("exact_record_name") != source_name
            or evidence_ref.get("printed_page") != printed_page
            or evidence_ref.get("source_header_line") != source_header_line
            or evidence_ref.get("raw_body_sha256") != body_sha256
            or evidence_ref.get("body_witness_ref")
            != {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer}
        ):
            _fail(
                "source_next12_provenance",
                f"{key} borrows a different source/pass/body witness",
            )

        locators = [
            _object(value, f"{key}.source_markdown_locators[{locator_index}]")
            for locator_index, value in enumerate(
                _array(
                    row.get("source_markdown_locators"),
                    f"{key}.source_markdown_locators",
                )
            )
        ]
        if locators != spec["locators"]:
            _fail(
                "source_next12_locator",
                f"{key} Markdown locators differ from the reviewed bounds",
            )
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                not isinstance(start, int)
                or not isinstance(end, int)
                or start < 1
                or end < start
                or end > len(markdown_lines)
            ):
                _fail("source_next12_locator", f"{key} has an invalid Markdown span")
            section_text = "\n".join(markdown_lines[start - 1 : end])
            locator_texts.append(section_text)
            first_line = markdown_lines[start - 1].strip()
            if locator_index == 0 and first_line != f"##### {source_name}":
                _fail(
                    "source_next12_locator",
                    f"{key} primary span does not start at its exact heading",
                )
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail(
                    "source_next12_locator",
                    f"{key} Markdown heading does not match its locator",
                )
        for locator_index, phrase in spec["required_source_phrases"]:
            if phrase not in locator_texts[locator_index]:
                _fail(
                    "source_next12_source_text", f"{key} source span omits {phrase!r}"
                )

        interpretation = row.get("source_interpretation")
        qualifiers = row.get("material_qualifiers")
        retained_residual = row.get("retained_source_residual")
        if (
            not isinstance(interpretation, str)
            or not interpretation.strip()
            or not isinstance(qualifiers, list)
            or not qualifiers
            or not all(isinstance(value, str) and value.strip() for value in qualifiers)
            or not isinstance(retained_residual, str)
            or not retained_residual.strip()
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_next12_formulation",
                f"{key} lacks bounded source formulation or proof limit",
            )
        combined_formulation = (
            f"{interpretation}\n" + "\n".join(qualifiers) + f"\n{retained_residual}"
        )
        combined_lower = combined_formulation.casefold()
        required_qualifiers_by_category = spec.get("required_qualifiers_by_category")
        if isinstance(required_qualifiers_by_category, dict):
            required_qualifiers = required_qualifiers_by_category.get(category, ())
        else:
            required_qualifiers = spec.get("required_qualifiers", ())
        for phrase in required_qualifiers:
            if str(phrase).casefold() not in combined_lower:
                _fail(
                    "source_next12_qualifier",
                    f"{key} omits required qualifier {phrase!r}",
                )
        if disposition == "SOURCE_CLOSED":
            retained_prefix = str(
                spec.get(
                    "retained_prefix", "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY"
                )
            )
            if not retained_residual.startswith(retained_prefix):
                _fail(
                    "source_next12_closure",
                    f"{key} closure exceeds its source subobligation",
                )
            closed_keys.append(key)
            closed_subobligation_ids.append(expected_subobligation_id)
        else:
            if retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY"
            ):
                _fail("source_next12_hold", f"{key} source HOLD was removed")
            held_keys.append(key)
            held_subobligation_ids.append(expected_subobligation_id)

        if key == "source.spell.feather_fall.unresolved.descent_rate":
            expected_common_ref = {
                "artifact_id": "source-pass-0-2",
                "json_pointer": "/common_obligations/0",
            }
            common_requirements = [
                _object(value, f"shared_common_requirements[{index}]")
                for index, value in enumerate(
                    _array(
                        lane0_payload.get("shared_common_requirements"),
                        "source-pass-0-2.mapping_payload.shared_common_requirements",
                    )
                )
            ]
            common_target = next(
                (
                    value
                    for value in common_requirements
                    if value.get("source_requirement_key")
                    == "source.common.target_clear_path"
                ),
                None,
            )
            common_clause = _resolve_json_pointer(
                source_pass,
                "/common_obligations/0",
                "Feather Fall common source clause",
            )
            if (
                row.get("shared_common_source_requirement_key")
                != "source.common.target_clear_path"
                or row.get("shared_common_source_record_ref") != expected_common_ref
                or common_target is None
                or common_target.get("evidence_ref") != expected_common_ref
                or common_target.get("native_consumer_status") != "NOT_ESTABLISHED"
                or common_target.get("actual_proof_refs") != []
                or not isinstance(common_clause, str)
                or "target/clear-path rules" not in common_clause
            ):
                _fail(
                    "source_next12_common_target",
                    "Feather Fall must retain the shared clear-path qualification without native proof",
                )
        elif (
            "shared_common_source_requirement_key" in row
            or "shared_common_source_record_ref" in row
        ):
            _fail(
                "source_next12_common_target",
                "common clear-path reference belongs only to Feather Fall",
            )

    contract = _object(
        manifest.get("source_next12_resolution_contract"),
        "source_next12_resolution_contract",
    )
    expected_contract = {
        "status": "PARTIAL_TWO_REVIEWED_SETS_SOURCE_ONLY",
        "selected_key_count": 12,
        "resolution_record_count": 13,
        "selected_source_closed_key_count": 11,
        "selected_source_closed_subobligation_count": 12,
        "selected_source_held_key_count": 1,
        "selected_source_held_subobligation_count": 1,
        "cumulative_reviewed_key_count": 24,
        "cumulative_resolution_record_count": 25,
        "cumulative_source_closed_key_count": 20,
        "cumulative_source_closed_subobligation_count": 21,
        "cumulative_source_held_key_count": 4,
        "cumulative_source_held_subobligation_count": 4,
        "active_source_blocker_count": 57,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
    }
    if (
        contract != expected_contract
        or set(closed_keys) != NEXT12_SOURCE_CLOSED_KEYS
        or set(held_keys) != NEXT12_SOURCE_HELD_KEYS
        or len(set(closed_keys)) != 11
        or len(closed_subobligation_ids) != 12
        or len(held_subobligation_ids) != 1
        or len(set(closed_subobligation_ids)) != 12
    ):
        _fail(
            "source_next12_contract",
            "next12 source closure/HOLD/cumulative counts differ",
        )
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": list(dict.fromkeys(closed_keys)),
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_subobligation_ids,
        "source_held_subobligation_ids": held_subobligation_ids,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_held_subobligation_count": len(held_subobligation_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_third12_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the accepted third12 source-only dispositions to exact source witnesses."""
    review = _object(manifest.get("source_third12_review"), "source_third12_review")
    if review != THIRD12_REVIEW:
        _fail(
            "source_third12_review",
            "frozen candidate, accepted review or task evidence identity differs",
        )
    task_evidence_bytes = _read_pinned_local_evidence(
        SOURCE_THIRD12_EVIDENCE_RELATIVE_PATH,
        SOURCE_THIRD12_EVIDENCE_SHA256,
        "source_third12_review",
    )
    try:
        task_evidence = task_evidence_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_third12_review", "task evidence is not UTF-8")
    if any(token not in task_evidence for token in THIRD12_REQUIRED_EVIDENCE_TOKENS):
        _fail(
            "source_third12_review",
            "bounded evidence omits frozen identities, selected keys or I01-I04 precision",
        )

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH,
        SOURCE_MARKDOWN_SHA256,
        "source_third12_markdown",
    )
    try:
        markdown_lines = markdown_bytes.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        _fail("source_third12_markdown", "source Markdown is not UTF-8")

    contract = _object(
        manifest.get("source_third12_resolution_contract"),
        "source_third12_resolution_contract",
    )
    expected_contract = {
        "status": "PARTIAL_THREE_REVIEWED_SETS_SOURCE_ONLY",
        "selected_key_count": 12,
        "selected_spell_count": 11,
        "resolution_record_count": 12,
        "selected_source_closed_key_count": 11,
        "selected_source_closed_subobligation_count": 11,
        "selected_source_held_key_count": 1,
        "selected_source_held_subobligation_count": 1,
        "prior_reviewed_key_count": 24,
        "prior_source_closed_key_count": 20,
        "prior_source_closed_subobligation_count": 21,
        "prior_source_held_key_count": 4,
        "prior_source_held_subobligation_count": 4,
        "prior_active_source_blocker_count": 57,
        "cumulative_reviewed_key_count": 36,
        "cumulative_resolution_record_count": 37,
        "cumulative_source_closed_key_count": 31,
        "cumulative_source_closed_subobligation_count": 32,
        "cumulative_source_held_key_count": 5,
        "cumulative_source_held_subobligation_count": 5,
        "original_record_count": 82,
        "original_source_blocking_key_count": 77,
        "downstream_only_key_count": 5,
        "active_source_blocker_count": 46,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "common_markdown_locators": THIRD12_COMMON_MARKDOWN_LOCATORS,
        "common_qualifiers": THIRD12_COMMON_QUALIFIERS,
    }
    if contract != expected_contract:
        _fail(
            "source_third12_contract",
            "third12 source closure/HOLD/cumulative counts or common qualifiers differ",
        )

    for locator_index, locator in enumerate(THIRD12_COMMON_MARKDOWN_LOCATORS):
        start = int(locator["line_start"])
        end = int(locator["line_end"])
        if start < 1 or end < start or end > len(markdown_lines):
            _fail("source_third12_common_locator", "common source span is invalid")
        section = "\n".join(markdown_lines[start - 1 : end])
        first_line = markdown_lines[start - 1].strip()
        if (locator_index == 0 or first_line.startswith("#")) and str(
            locator["heading"]
        ) not in first_line:
            _fail(
                "source_third12_common_locator",
                f"common locator {locator['heading']} has a mismatched heading",
            )
        required_common_phrases = {
            "Range": ("spell’s description says otherwise",),
            "Duration": ("dismiss it (no action required)", "Incapacitated"),
            "Effects": ("under the GM’s purview",),
            "Targets": ("A Clear Path to the Target", "Total Cover"),
            "Area of Effect": (
                "point of origin",
                "Total Cover",
                "near side of the obstruction",
            ),
            "Concentration": (
                "another effect that requires Concentration",
                "Incapacitated",
                "you die",
            ),
            "Combining Spell Effects": (
                "don’t combine",
                "most potent effect",
                "most recent effect",
            ),
        }[str(locator["heading"])]
        if any(phrase not in section for phrase in required_common_phrases):
            _fail(
                "source_third12_common_locator",
                f"common source span {locator['heading']} omits a reviewed clause",
            )

    rows = [
        _object(value, f"source_third12_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_third12_resolution_evidence"),
                "source_third12_resolution_evidence",
            )
        )
    ]
    expected_order = tuple(
        (item_id, key, category) for item_id, key, category in THIRD12_EVIDENCE_ORDER
    )
    actual_order: list[tuple[str, str, str]] = []
    for row_index, row in enumerate(rows):
        actual_order.append(
            (
                str(row.get("review_item_id")),
                str(row.get("unresolved_key")),
                str(row.get("source_category")),
            )
        )
    if (
        len(rows) != 12
        or tuple(actual_order) != expected_order
        or len({row.get("unresolved_key") for row in rows}) != 12
    ):
        _fail(
            "source_third12_census",
            "selected third12 key/category/order census differs",
        )

    prior_keys = set(SOURCE_RESOLUTION_KEYS) | set(NEXT12_SELECTED_KEYS)
    if prior_keys & set(THIRD12_SELECTED_KEYS):
        _fail(
            "source_third12_census", "third12 replaces a key from a prior accepted set"
        )

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_witnesses = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    witness_rows = _rows(body_witnesses, "rows", "source-body-witnesses")
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_subobligation_ids: list[str] = []
    held_subobligation_ids: list[str] = []
    previous_selected_keys = set(SOURCE_RESOLUTION_KEYS) | set(NEXT12_SELECTED_KEYS)
    for row_index, ((item_id, key, category), row) in enumerate(
        zip(THIRD12_EVIDENCE_ORDER, rows, strict=True)
    ):
        spec = THIRD12_SOURCE_ITEMS[key]
        classification_index = int(spec["classification_index"])
        map_entry_index = int(spec["map_entry_index"])
        source_pass_row = int(spec["source_pass_row"])
        body_witness_row = int(spec["body_witness_row"])
        source_name = str(spec["source_exact_name"])
        disposition = str(spec["disposition"])
        expected_subobligation_id = f"{key}::{category}"
        classification_pointer = (
            f"/source_unknown_classifications/{classification_index}"
        )
        history_pointer = (
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/"
            f"{classification_index}"
        )
        map_pointer = (
            f"/source_mapping_lanes/0/mapping_payload/entries/{map_entry_index}"
        )
        source_pointer = f"/rows/{source_pass_row}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{source_pass_row}/qualifications"
        body_pointer = f"/rows/{body_witness_row}"
        classification = classified_by_key.get(key)
        if classification is None or key in previous_selected_keys:
            _fail(
                "source_third12_key",
                f"{key} is absent or replaces prior selected evidence",
            )
        original_classification = _object(
            _resolve_json_pointer(
                manifest, classification_pointer, "third12 classification pointer"
            ),
            f"{key}.classification",
        )
        original_history = _object(
            _resolve_json_pointer(manifest, history_pointer, "third12 history pointer"),
            f"{key}.original_history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "third12 map pointer"),
            f"{key}.current_map",
        )
        map_unresolved_keys = [
            _object(value, f"{key}.map.unresolved_keys[{index}]")
            for index, value in enumerate(
                _array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys")
            )
        ]
        evidence_ref = _object(
            classification.get("evidence_ref"), f"{key}.evidence_ref"
        )
        history_matches = (
            original_history.get("unresolved_key") == key
            and original_history.get("source_exact_name") == source_name
            and original_history.get("reason") == classification.get("original_reason")
            and original_history.get("evidence_ref") == evidence_ref
            and original_history.get("status") == classification.get("original_status")
            and original_history.get("disposition")
            == classification.get("original_disposition")
        )
        map_matches = map_entry.get("source_exact_name") == source_name and any(
            value.get("unresolved_key") == key for value in map_unresolved_keys
        )
        source_subobligations = [
            _object(value, f"{key}.source_subobligations[{index}]")
            for index, value in enumerate(
                _array(classification.get("subobligations"), f"{key}.subobligations")
            )
            if isinstance(value, dict)
            and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        exact_subobligation = any(
            value.get("subobligation_id") == expected_subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            for value in source_subobligations
        )
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != source_name
            or row.get("source_category") != category
            or row.get("subobligation_id") != expected_subobligation_id
            or row.get("disposition") != disposition
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original_classification
            or original_classification.get("unresolved_key") != key
            or original_classification.get("source_exact_name") != source_name
            or original_classification.get("source_unresolved_record_pointer")
            != history_pointer
            or original_classification.get("source_ready_blocking") is not True
            or original_classification.get("original_status") != "NOT_ESTABLISHED"
            or not history_matches
            or not map_matches
            or not exact_subobligation
        ):
            _fail(
                "source_third12_binding",
                f"{key} differs from its original category, classification, history or map association",
            )

        source_record = source_rows[source_pass_row]
        body_witness = witness_rows[body_witness_row]
        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": source_name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
        }
        if (
            source_record.get("name") != source_name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != source_name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
            or row.get("source_record_ref") != expected_ref
            or evidence_ref.get("artifact_id") != "source-pass-0-2"
            or evidence_ref.get("json_pointer") != source_pointer
            or evidence_ref.get("exact_record_name") != source_name
            or evidence_ref.get("printed_page") != spec["printed_page"]
            or evidence_ref.get("source_header_line") != spec["source_header_line"]
            or evidence_ref.get("raw_body_sha256") != spec["raw_body_sha256"]
            or evidence_ref.get("body_witness_ref")
            != {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer}
        ):
            _fail(
                "source_third12_provenance",
                f"{key} borrows a foreign source-pass, qualification or body-witness record",
            )

        locators = [
            _object(value, f"{key}.source_markdown_locators[{locator_index}]")
            for locator_index, value in enumerate(
                _array(
                    row.get("source_markdown_locators"),
                    f"{key}.source_markdown_locators",
                )
            )
        ]
        if locators != spec["locators"]:
            _fail(
                "source_third12_locator",
                f"{key} Markdown locators differ from the reviewed bounds",
            )
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                type(start) is not int
                or type(end) is not int
                or start < 1
                or end < start
                or end > len(markdown_lines)
            ):
                _fail("source_third12_locator", f"{key} has an invalid Markdown span")
            section_text = "\n".join(markdown_lines[start - 1 : end])
            locator_texts.append(section_text)
            first_line = markdown_lines[start - 1].strip()
            if locator_index == 0 and first_line != f"##### {source_name}":
                _fail(
                    "source_third12_locator",
                    f"{key} primary span does not start at its exact heading",
                )
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail(
                    "source_third12_locator",
                    f"{key} locator heading does not match its Markdown span",
                )
        for locator_index, phrase in spec["source_phrases"]:
            if phrase not in locator_texts[locator_index]:
                _fail(
                    "source_third12_source_text", f"{key} source span omits {phrase!r}"
                )

        interpretation = row.get("source_interpretation")
        qualifiers = row.get("material_qualifiers")
        retained_residual = row.get("retained_source_residual")
        if (
            not isinstance(interpretation, str)
            or not interpretation.strip()
            or not isinstance(qualifiers, list)
            or not qualifiers
            or not all(isinstance(value, str) and value.strip() for value in qualifiers)
            or not isinstance(retained_residual, str)
            or not retained_residual.strip()
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_third12_formulation",
                f"{key} lacks bounded source formulation or proof limit",
            )
        combined_formulation = (
            f"{interpretation}\n" + "\n".join(qualifiers) + f"\n{retained_residual}"
        )
        for phrase in spec["required_qualifiers"]:
            if str(phrase).casefold() not in combined_formulation.casefold():
                _fail(
                    "source_third12_qualifier",
                    f"{key} omits required qualifier {phrase!r}",
                )

        expected_members = spec.get("members")
        if expected_members is None:
            if "members" in row:
                _fail(
                    "source_third12_enum", f"{key} introduces an unreviewed source enum"
                )
        elif row.get("members") != expected_members:
            _fail("source_third12_enum", f"{key} source enum members differ")
        expected_duration_bands = spec.get("duration_hours_by_slot")
        if expected_duration_bands is None:
            if "duration_hours_by_slot" in row:
                _fail(
                    "source_third12_duration",
                    f"{key} introduces an unreviewed duration map",
                )
        elif row.get("duration_hours_by_slot") != expected_duration_bands:
            _fail("source_third12_duration", f"{key} slot duration bands differ")

        if disposition == "SOURCE_CLOSED":
            if not retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ):
                _fail(
                    "source_third12_closure",
                    f"{key} closure exceeds its selected source subobligation",
                )
            closed_keys.append(key)
            closed_subobligation_ids.append(expected_subobligation_id)
        else:
            if (
                key
                != "source.spell.gentle_repose.unresolved.corpse_and_revival_binding"
            ):
                _fail(
                    "source_third12_hold", f"unexpected third12 source HOLD for {key}"
                )
            if retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY"
            ):
                _fail("source_third12_hold", "Gentle Repose source HOLD was removed")
            downstream_subobligations = [
                value
                for value in _array(
                    classification.get("subobligations"), f"{key}.subobligations"
                )
                if isinstance(value, dict)
                and value.get("category")
                == "downstream_domain_consumer_admission_native_proof"
            ]
            if (
                len(downstream_subobligations) != 1
                or downstream_subobligations[0].get("status") != "NOT_ESTABLISHED"
            ):
                _fail(
                    "source_third12_downstream",
                    "Gentle Repose downstream HOLD was removed or promoted",
                )
            held_keys.append(key)
            held_subobligation_ids.append(expected_subobligation_id)

    contract_previous = _object(
        manifest.get("source_next12_resolution_contract"),
        "source_next12_resolution_contract",
    )
    if (
        contract_previous.get("cumulative_reviewed_key_count") != 24
        or contract_previous.get("cumulative_source_closed_key_count") != 20
        or contract_previous.get("cumulative_source_closed_subobligation_count") != 21
        or contract_previous.get("cumulative_source_held_key_count") != 4
        or contract_previous.get("active_source_blocker_count") != 57
    ):
        _fail(
            "source_third12_prior_contract",
            "third12 integration replaces prior cumulative evidence",
        )
    if (
        set(closed_keys) != THIRD12_SOURCE_CLOSED_KEYS
        or set(held_keys) != THIRD12_SOURCE_HELD_KEYS
        or len(set(closed_keys)) != 11
        or len(closed_subobligation_ids) != 11
        or len(set(closed_subobligation_ids)) != 11
        or len(held_subobligation_ids) != 1
        or len(
            {str(spec["source_exact_name"]) for spec in THIRD12_SOURCE_ITEMS.values()}
        )
        != 11
    ):
        _fail(
            "source_third12_contract",
            "third12 source closure/HOLD or spell counts differ",
        )
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_subobligation_ids,
        "source_held_subobligation_ids": held_subobligation_ids,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_held_subobligation_count": len(held_subobligation_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_fourth_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the reviewed fourth source-only set to exact old and Markdown witnesses."""
    review = _object(manifest.get("source_fourth_review"), "source_fourth_review")
    if review != FOURTH_REVIEW:
        _fail(
            "source_fourth_review",
            "fourth extraction, independent review or task-evidence identity differs",
        )
    task_evidence_bytes = _read_pinned_local_evidence(
        str(FOURTH_REVIEW["task_evidence_path"]),
        str(FOURTH_REVIEW["task_evidence_sha256"]),
        "source_fourth_review",
    )
    try:
        task_evidence = task_evidence_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_fourth_review", "task evidence is not UTF-8")
    if any(token not in task_evidence for token in FOURTH_REQUIRED_EVIDENCE_TOKENS):
        _fail(
            "source_fourth_review",
            "task evidence omits frozen identities, the corrected shared law or limits",
        )

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH,
        SOURCE_MARKDOWN_SHA256,
        "source_fourth_markdown",
    )
    try:
        markdown_bytes_lines = markdown_bytes.splitlines(keepends=True)
        markdown_lines = [line.decode("utf-8") for line in markdown_bytes_lines]
    except UnicodeDecodeError:
        _fail("source_fourth_markdown", "source Markdown is not UTF-8")

    contract = _object(
        manifest.get("source_fourth_resolution_contract"),
        "source_fourth_resolution_contract",
    )
    expected_contract = {
        "status": "PARTIAL_FOURTH_REVIEWED_SET_SOURCE_ONLY",
        "selected_key_count": 11,
        "selected_spell_count": 10,
        "resolution_record_count": 11,
        "selected_source_closed_key_count": 8,
        "selected_source_closed_subobligation_count": 8,
        "selected_source_held_key_count": 3,
        "selected_source_held_subobligation_count": 3,
        "prior_reviewed_key_count": 36,
        "prior_source_closed_key_count": 31,
        "prior_source_closed_subobligation_count": 32,
        "prior_source_held_key_count": 5,
        "prior_source_held_subobligation_count": 5,
        "prior_active_source_blocker_count": 46,
        "cumulative_reviewed_key_count": 47,
        "cumulative_resolution_record_count": 48,
        "cumulative_source_closed_key_count": 39,
        "cumulative_source_closed_subobligation_count": 40,
        "cumulative_source_held_key_count": 8,
        "cumulative_source_held_subobligation_count": 8,
        "original_record_count": 82,
        "original_source_blocking_key_count": 77,
        "downstream_only_key_count": 5,
        "active_source_blocker_count": 38,
        "active_source_blocker_entry_count": 35,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "production_claim": "NONE",
        "selected_original_classification_indexes": list(
            FOURTH_SELECTED_CLASSIFICATION_INDEXES
        ),
        "common_markdown_locators": list(FOURTH_COMMON_MARKDOWN_LOCATORS),
        "common_qualifiers": list(FOURTH_COMMON_QUALIFIERS),
    }
    if contract != expected_contract:
        _fail(
            "source_fourth_contract",
            "fourth source-only counts, preserved totals or shared qualifiers differ",
        )

    for locator_index, locator in enumerate(FOURTH_COMMON_MARKDOWN_LOCATORS):
        start = int(locator["line_start"])
        end = int(locator["line_end"])
        if start < 1 or end < start or end > len(markdown_bytes_lines):
            _fail("source_fourth_common_locator", "common source span is invalid")
        span_bytes = b"".join(markdown_bytes_lines[start - 1 : end])
        if hashlib.sha256(span_bytes).hexdigest() != locator["span_sha256"]:
            _fail(
                "source_fourth_markdown_span_hash",
                f"common Markdown span {locator['heading']} changed",
            )
        section = "".join(markdown_lines[start - 1 : end])
        heading_line = next(
            (
                line.strip()
                for line in markdown_lines[start - 1 : end]
                if line.lstrip().startswith("#")
            ),
            "",
        )
        heading = str(locator["heading"])
        if not heading_line.startswith("#") or heading not in heading_line:
            _fail(
                "source_fourth_common_locator",
                f"common locator {heading} has a mismatched heading",
            )
        if any(
            phrase not in section for phrase in FOURTH_COMMON_REQUIRED_PHRASES[heading]
        ):
            _fail(
                "source_fourth_common_source_text",
                f"common source span {heading} omits a reviewed clause",
            )

    rows = [
        _object(value, f"source_fourth_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_fourth_resolution_evidence"),
                "source_fourth_resolution_evidence",
            )
        )
    ]
    actual_order = [
        (
            str(row.get("review_item_id")),
            str(row.get("unresolved_key")),
            str(row.get("source_category")),
        )
        for row in rows
    ]
    expected_order = tuple(FOURTH_EVIDENCE_ORDER)
    if (
        len(rows) != len(expected_order)
        or tuple(actual_order) != expected_order
        or len({row.get("unresolved_key") for row in rows}) != len(expected_order)
    ):
        _fail(
            "source_fourth_census",
            "the selected fourth source key/category/order census differs",
        )

    previous_keys = (
        set(SOURCE_RESOLUTION_KEYS)
        | set(NEXT12_SELECTED_KEYS)
        | set(THIRD12_SELECTED_KEYS)
    )
    if previous_keys & set(FOURTH_SELECTED_KEYS):
        _fail("source_fourth_census", "fourth evidence replaces a prior accepted key")
    if list(FOURTH_SELECTED_CLASSIFICATION_INDEXES) != [
        int(FOURTH_SOURCE_ITEMS[key]["classification_index"])
        for key in FOURTH_SELECTED_KEYS
    ]:
        _fail("source_fourth_census", "selected original index roster differs")

    skipped = classified_by_key.get(
        "source.spell.lesser_restoration.unresolved.multisource_condition_removal"
    )
    skipped_subobligations = (
        [
            _object(value, "index45.subobligations")
            for value in _array(skipped.get("subobligations"), "index45.subobligations")
        ]
        if skipped is not None
        else []
    )
    if (
        skipped is None
        or skipped.get("source_ready_blocking") is not False
        or skipped.get("classification_status") != "DOWNSTREAM_PROOF_ONLY"
        or len(skipped_subobligations) != 1
        or skipped_subobligations[0].get("category")
        != "downstream_domain_consumer_admission_native_proof"
        or skipped_subobligations[0].get("gate_phase") != "FUTURE_PROOF"
        or skipped_subobligations[0].get("status") != "NOT_ESTABLISHED"
    ):
        _fail(
            "source_fourth_census",
            "original index 45 is not preserved as downstream-only evidence",
        )

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_witnesses = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    witness_rows = _rows(body_witnesses, "rows", "source-body-witnesses")
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_subobligation_ids: list[str] = []
    held_subobligation_ids: list[str] = []

    for (item_id, key, category), row in zip(FOURTH_EVIDENCE_ORDER, rows, strict=True):
        spec = FOURTH_SOURCE_ITEMS[key]
        classification_index = int(spec["classification_index"])
        map_entry_index = int(spec["map_entry_index"])
        source_pass_row = int(spec["source_pass_row"])
        body_witness_row = int(spec["body_witness_row"])
        source_name = str(spec["source_exact_name"])
        disposition = str(spec["disposition"])
        subobligation_id = f"{key}::{category}"
        classification_pointer = (
            f"/source_unknown_classifications/{classification_index}"
        )
        history_pointer = (
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/"
            f"{classification_index}"
        )
        map_pointer = (
            f"/source_mapping_lanes/0/mapping_payload/entries/{map_entry_index}"
        )
        source_pointer = f"/rows/{source_pass_row}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{source_pass_row}/qualifications"
        body_pointer = f"/rows/{body_witness_row}"
        classification = classified_by_key.get(key)
        if classification is None or key in previous_keys:
            _fail("source_fourth_key", f"{key} is absent or replaces prior evidence")

        original_classification = _object(
            _resolve_json_pointer(
                manifest, classification_pointer, "fourth classification pointer"
            ),
            f"{key}.classification",
        )
        original_history = _object(
            _resolve_json_pointer(manifest, history_pointer, "fourth history pointer"),
            f"{key}.original_history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "fourth current-map pointer"),
            f"{key}.current_map",
        )
        unresolved_rows = [
            _object(value, f"{key}.map.unresolved_keys[{index}]")
            for index, value in enumerate(
                _array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys")
            )
        ]
        evidence_ref = _object(
            classification.get("evidence_ref"), f"{key}.evidence_ref"
        )
        history_matches = (
            original_history.get("unresolved_key") == key
            and original_history.get("source_exact_name") == source_name
            and original_history.get("reason") == classification.get("original_reason")
            and original_history.get("evidence_ref") == evidence_ref
            and original_history.get("status") == classification.get("original_status")
            and original_history.get("disposition")
            == classification.get("original_disposition")
        )
        map_matches = map_entry.get("source_exact_name") == source_name and any(
            value.get("unresolved_key") == key for value in unresolved_rows
        )
        source_subobligations = [
            _object(value, f"{key}.source_subobligations[{index}]")
            for index, value in enumerate(
                _array(classification.get("subobligations"), f"{key}.subobligations")
            )
            if isinstance(value, dict)
            and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        exact_subobligation = any(
            value.get("subobligation_id") == subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            and value.get("gate_phase") == "SP00_SOURCE"
            for value in source_subobligations
        )
        if row.get("disposition") != disposition:
            _fail(
                "source_fourth_disposition",
                f"{key} source-only disposition differs from the reviewed ruling",
            )
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != source_name
            or row.get("source_category") != category
            or row.get("subobligation_id") != subobligation_id
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original_classification
            or original_classification.get("unresolved_key") != key
            or original_classification.get("source_exact_name") != source_name
            or original_classification.get("source_unresolved_record_pointer")
            != history_pointer
            or original_classification.get("source_ready_blocking") is not True
            or original_classification.get("original_status") != "NOT_ESTABLISHED"
            or not history_matches
            or not map_matches
            or not exact_subobligation
        ):
            _fail(
                "source_fourth_binding",
                f"{key} differs from its original category, history, map or source subobligation",
            )

        source_record = source_rows[source_pass_row]
        body_witness = witness_rows[body_witness_row]
        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": source_name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
        }
        expected_evidence_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "exact_record_name": source_name,
            "record_index": source_pass_row,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "source_heading": source_name,
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
            "evidence_boundary": "RETAINED_FULL_BODY_REVIEW_SUMMARY_DECOMPOSITION; NO_NEW_PRIMARY_BODY_OR_NATIVE_CONSUMER_PROOF",
        }
        if (
            source_record.get("name") != source_name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or source_record.get("hash_basis")
            != "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization"
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != source_name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
            or row.get("source_record_ref") != expected_ref
            or evidence_ref != expected_evidence_ref
        ):
            _fail(
                "source_fourth_provenance",
                f"{key} borrows or misstates a source-pass, qualification or body-witness record",
            )

        locators = [
            _object(value, f"{key}.source_markdown_locators[{index}]")
            for index, value in enumerate(
                _array(
                    row.get("source_markdown_locators"),
                    f"{key}.source_markdown_locators",
                )
            )
        ]
        if locators != spec["locators"]:
            _fail("source_fourth_locator", f"{key} Markdown locators differ")
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                type(start) is not int
                or type(end) is not int
                or start < 1
                or end < start
                or end > len(markdown_bytes_lines)
            ):
                _fail("source_fourth_locator", f"{key} has an invalid Markdown span")
            span_bytes = b"".join(markdown_bytes_lines[start - 1 : end])
            if hashlib.sha256(span_bytes).hexdigest() != locator["span_sha256"]:
                _fail(
                    "source_fourth_markdown_span_hash",
                    f"{key} Markdown span changed",
                )
            section = "".join(markdown_lines[start - 1 : end])
            locator_texts.append(section)
            first_line = markdown_lines[start - 1].strip()
            if locator_index == 0 and first_line != f"##### {source_name}":
                _fail(
                    "source_fourth_locator",
                    f"{key} primary span does not start at its exact heading",
                )
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail(
                    "source_fourth_locator",
                    f"{key} locator heading does not match its source span",
                )
        for locator_index, phrase in spec["source_phrases"]:
            if phrase not in locator_texts[int(locator_index)]:
                _fail(
                    "source_fourth_source_text",
                    f"{key} source span omits {phrase!r}",
                )

        interpretation = row.get("source_interpretation")
        qualifiers = row.get("material_qualifiers")
        retained_residual = row.get("retained_source_residual")
        if (
            not isinstance(interpretation, str)
            or not interpretation.strip()
            or not isinstance(qualifiers, list)
            or not qualifiers
            or not all(isinstance(value, str) and value.strip() for value in qualifiers)
            or not isinstance(retained_residual, str)
            or not retained_residual.strip()
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_fourth_formulation",
                f"{key} lacks bounded source formulation or proof limits",
            )
        combined_formulation = (
            f"{interpretation}\n" + "\n".join(qualifiers) + f"\n{retained_residual}"
        )
        for phrase in spec["required_qualifiers"]:
            if str(phrase).casefold() not in combined_formulation.casefold():
                _fail(
                    "source_fourth_qualifier",
                    f"{key} omits required qualifier {phrase!r}",
                )

        downstream_subobligations = [
            value
            for value in _array(
                classification.get("subobligations"), f"{key}.subobligations"
            )
            if isinstance(value, dict)
            and value.get("category")
            == "downstream_domain_consumer_admission_native_proof"
        ]
        if any(
            value.get("status") != "NOT_ESTABLISHED"
            or value.get("gate_phase") != "FUTURE_PROOF"
            for value in downstream_subobligations
        ):
            _fail(
                "source_fourth_downstream",
                f"{key} promotes a downstream consumer/native proof",
            )

        if disposition == "SOURCE_CLOSED":
            if not retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ):
                _fail(
                    "source_fourth_closure",
                    f"{key} closure exceeds its selected source subobligation",
                )
            closed_keys.append(key)
            closed_subobligation_ids.append(subobligation_id)
        else:
            if retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ):
                _fail("source_fourth_hold", f"{key} source HOLD was removed")
            closed_residual = retained_residual.startswith("HOLD_SOURCE_SUBOBLIGATION;")
            if not closed_residual:
                _fail("source_fourth_hold", f"{key} lacks an explicit retained HOLD")
            held_keys.append(key)
            held_subobligation_ids.append(subobligation_id)

    prior_contract = _object(
        manifest.get("source_third12_resolution_contract"),
        "source_third12_resolution_contract",
    )
    if (
        prior_contract.get("cumulative_reviewed_key_count") != 36
        or prior_contract.get("cumulative_source_closed_key_count") != 31
        or prior_contract.get("cumulative_source_closed_subobligation_count") != 32
        or prior_contract.get("cumulative_source_held_key_count") != 5
        or prior_contract.get("active_source_blocker_count") != 46
    ):
        _fail(
            "source_fourth_prior_contract",
            "fourth integration replaced or rewrote the prior cumulative evidence",
        )
    if (
        set(closed_keys) != FOURTH_SOURCE_CLOSED_KEYS
        or set(held_keys) != FOURTH_SOURCE_HELD_KEYS
        or len(closed_keys) != 8
        or len(set(closed_subobligation_ids)) != 8
        or len(held_subobligation_ids) != 3
        or len(set(held_subobligation_ids)) != 3
        or len(
            {str(spec["source_exact_name"]) for spec in FOURTH_SOURCE_ITEMS.values()}
        )
        != 10
    ):
        _fail(
            "source_fourth_contract",
            "fourth source closure/HOLD or spell counts differ",
        )
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_subobligation_ids,
        "source_held_subobligation_ids": held_subobligation_ids,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_held_subobligation_count": len(held_subobligation_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_fifth_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the fifth reviewed source-only set to its exact evidence witnesses."""
    review = _object(manifest.get("source_fifth_review"), "source_fifth_review")
    if review != FIFTH_REVIEW:
        _fail(
            "source_fifth_review",
            "fifth extraction, independent review or task-evidence identity differs",
        )
    task_evidence_bytes = _read_pinned_local_evidence(
        FIFTH_REVIEW["task_evidence_path"],
        FIFTH_REVIEW["task_evidence_sha256"],
        "source_fifth_review",
    )
    try:
        task_evidence = task_evidence_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_fifth_review", "task evidence is not UTF-8")
    if any(token not in task_evidence for token in FIFTH_REQUIRED_EVIDENCE_TOKENS):
        _fail(
            "source_fifth_review",
            "task evidence omits frozen identities, source limits or bounded counts",
        )

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH,
        SOURCE_MARKDOWN_SHA256,
        "source_fifth_markdown",
    )
    try:
        markdown_bytes_lines = markdown_bytes.splitlines(keepends=True)
        markdown_lines = [line.decode("utf-8") for line in markdown_bytes_lines]
    except UnicodeDecodeError:
        _fail("source_fifth_markdown", "source Markdown is not UTF-8")

    contract = _object(
        manifest.get("source_fifth_resolution_contract"),
        "source_fifth_resolution_contract",
    )
    expected_contract = {
        "status": "PARTIAL_FIFTH_REVIEWED_SET_SOURCE_ONLY",
        "selected_key_count": 12,
        "selected_spell_count": 12,
        "resolution_record_count": 13,
        "selected_source_closed_key_count": 8,
        "selected_source_closed_subobligation_count": 9,
        "selected_source_held_key_count": 4,
        "selected_source_held_subobligation_count": 4,
        "prior_reviewed_key_count": 47,
        "prior_source_closed_key_count": 39,
        "prior_source_closed_subobligation_count": 40,
        "prior_source_held_key_count": 8,
        "prior_source_held_subobligation_count": 8,
        "prior_active_source_blocker_count": 38,
        "cumulative_reviewed_key_count": 59,
        "cumulative_resolution_record_count": 61,
        "cumulative_source_closed_key_count": 47,
        "cumulative_source_closed_subobligation_count": 49,
        "cumulative_source_held_key_count": 12,
        "cumulative_source_held_subobligation_count": 12,
        "original_record_count": 82,
        "original_source_blocking_key_count": 77,
        "downstream_only_key_count": 5,
        "active_source_blocker_count": 30,
        "active_source_blocker_entry_count": 28,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "production_claim": "NONE",
        "selected_original_classification_indexes": list(
            FIFTH_SELECTED_CLASSIFICATION_INDEXES
        ),
        "common_markdown_locators": list(FIFTH_COMMON_MARKDOWN_LOCATORS),
        "common_qualifiers": list(FIFTH_COMMON_QUALIFIERS),
    }
    if contract != expected_contract:
        _fail(
            "source_fifth_contract",
            "fifth source-only counts, preserved totals or shared qualifiers differ",
        )

    for locator in FIFTH_COMMON_MARKDOWN_LOCATORS:
        start = int(locator["line_start"])
        end = int(locator["line_end"])
        heading = str(locator["heading"])
        if start < 1 or end < start or end > len(markdown_bytes_lines):
            _fail("source_fifth_common_locator", "common source span is invalid")
        span_bytes = b"".join(markdown_bytes_lines[start - 1 : end])
        if hashlib.sha256(span_bytes).hexdigest() != locator["span_sha256"]:
            _fail(
                "source_fifth_markdown_span_hash",
                f"common Markdown span {heading} changed",
            )
        section = "".join(markdown_lines[start - 1 : end])
        heading_line = next(
            (
                line.strip()
                for line in markdown_lines[start - 1 : end]
                if line.lstrip().startswith("#")
            ),
            "",
        )
        if not heading_line.startswith("#") or heading not in heading_line:
            _fail(
                "source_fifth_common_locator",
                f"common locator {heading} has a mismatched heading",
            )
        if any(
            phrase not in section for phrase in FIFTH_COMMON_REQUIRED_PHRASES[heading]
        ):
            _fail(
                "source_fifth_common_source_text",
                f"common source span {heading} omits a reviewed clause",
            )

    rows = [
        _object(value, f"source_fifth_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_fifth_resolution_evidence"),
                "source_fifth_resolution_evidence",
            )
        )
    ]
    actual_order = [
        (
            str(row.get("review_item_id")),
            str(row.get("unresolved_key")),
            str(row.get("source_category")),
        )
        for row in rows
    ]
    if (
        len(rows) != len(FIFTH_EVIDENCE_ORDER)
        or tuple(actual_order) != FIFTH_EVIDENCE_ORDER
        or len({row.get("unresolved_key") for row in rows}) != 12
        or len(
            {(row.get("unresolved_key"), row.get("source_category")) for row in rows}
        )
        != len(FIFTH_EVIDENCE_ORDER)
    ):
        _fail(
            "source_fifth_census",
            "the selected fifth source key/category/order census differs",
        )

    previous_keys = (
        set(SOURCE_RESOLUTION_KEYS)
        | set(NEXT12_SELECTED_KEYS)
        | set(THIRD12_SELECTED_KEYS)
        | set(FOURTH_SELECTED_KEYS)
    )
    selected_keys = set(FIFTH_SOURCE_ITEMS)
    if previous_keys & selected_keys:
        _fail("source_fifth_census", "fifth evidence replaces a prior accepted key")
    if (
        tuple(
            int(FIFTH_SOURCE_ITEMS[key]["classification_index"])
            for key in dict.fromkeys(FIFTH_SELECTED_KEYS)
        )
        != FIFTH_SELECTED_CLASSIFICATION_INDEXES
    ):
        _fail("source_fifth_census", "selected original index roster differs")

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_witnesses = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    witness_rows = _rows(body_witnesses, "rows", "source-body-witnesses")
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_subobligation_ids: list[str] = []
    held_subobligation_ids: list[str] = []
    selected_future_proof_keys: set[str] = set()

    for (item_id, key, category), row in zip(FIFTH_EVIDENCE_ORDER, rows, strict=True):
        spec = FIFTH_SOURCE_ITEMS[key]
        classification_index = int(spec["classification_index"])
        map_entry_index = int(spec["map_entry_index"])
        source_pass_row = int(spec["source_pass_row"])
        body_witness_row = int(spec["body_witness_row"])
        source_name = str(spec["source_exact_name"])
        disposition = str(spec["disposition"])
        subobligation_id = f"{key}::{category}"
        classification_pointer = (
            f"/source_unknown_classifications/{classification_index}"
        )
        history_pointer = (
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/"
            f"{classification_index}"
        )
        map_pointer = (
            f"/source_mapping_lanes/0/mapping_payload/entries/{map_entry_index}"
        )
        source_pointer = f"/rows/{source_pass_row}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{source_pass_row}/qualifications"
        body_pointer = f"/rows/{body_witness_row}"
        classification = classified_by_key.get(key)
        if classification is None or key in previous_keys:
            _fail("source_fifth_key", f"{key} is absent or replaces prior evidence")

        original_classification = _object(
            _resolve_json_pointer(
                manifest, classification_pointer, "fifth classification pointer"
            ),
            f"{key}.classification",
        )
        original_history = _object(
            _resolve_json_pointer(manifest, history_pointer, "fifth history pointer"),
            f"{key}.original_history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "fifth current-map pointer"),
            f"{key}.current_map",
        )
        unresolved_rows = [
            _object(value, f"{key}.map.unresolved_keys[{index}]")
            for index, value in enumerate(
                _array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys")
            )
        ]
        evidence_ref = _object(
            classification.get("evidence_ref"), f"{key}.evidence_ref"
        )
        history_matches = (
            original_history.get("unresolved_key") == key
            and original_history.get("source_exact_name") == source_name
            and original_history.get("reason") == classification.get("original_reason")
            and original_history.get("evidence_ref") == evidence_ref
            and original_history.get("status") == classification.get("original_status")
            and original_history.get("disposition")
            == classification.get("original_disposition")
        )
        map_matches = map_entry.get("source_exact_name") == source_name and any(
            value.get("unresolved_key") == key for value in unresolved_rows
        )
        source_subobligations = [
            _object(value, f"{key}.source_subobligations[{index}]")
            for index, value in enumerate(
                _array(classification.get("subobligations"), f"{key}.subobligations")
            )
            if isinstance(value, dict)
            and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        exact_subobligation = any(
            value.get("subobligation_id") == subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            and value.get("gate_phase") == "SP00_SOURCE"
            for value in source_subobligations
        )
        if row.get("disposition") != disposition:
            _fail(
                "source_fifth_disposition",
                f"{key} source-only disposition differs from the reviewed ruling",
            )
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != source_name
            or row.get("source_category") != category
            or row.get("subobligation_id") != subobligation_id
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original_classification
            or original_classification.get("unresolved_key") != key
            or original_classification.get("source_exact_name") != source_name
            or original_classification.get("source_unresolved_record_pointer")
            != history_pointer
            or original_classification.get("source_ready_blocking") is not True
            or original_classification.get("original_status") != "NOT_ESTABLISHED"
            or not history_matches
            or not map_matches
            or not exact_subobligation
        ):
            _fail(
                "source_fifth_binding",
                f"{key} differs from its original category, history, map or subobligation",
            )

        source_record = source_rows[source_pass_row]
        body_witness = witness_rows[body_witness_row]
        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": source_name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
        }
        expected_evidence_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "exact_record_name": source_name,
            "record_index": source_pass_row,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "source_heading": source_name,
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-0-2",
                "json_pointer": qualification_pointer,
            },
            "evidence_boundary": "RETAINED_FULL_BODY_REVIEW_SUMMARY_DECOMPOSITION; NO_NEW_PRIMARY_BODY_OR_NATIVE_CONSUMER_PROOF",
        }
        if (
            source_record.get("name") != source_name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or source_record.get("hash_basis")
            != "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization"
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != source_name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
            or row.get("source_record_ref") != expected_ref
            or evidence_ref != expected_evidence_ref
        ):
            _fail(
                "source_fifth_provenance",
                f"{key} borrows or misstates a source-pass, qualification or body witness",
            )

        locators = [
            _object(value, f"{key}.source_markdown_locators[{index}]")
            for index, value in enumerate(
                _array(
                    row.get("source_markdown_locators"),
                    f"{key}.source_markdown_locators",
                )
            )
        ]
        if locators != list(spec["locators"]):
            _fail("source_fifth_locator", f"{key} Markdown locators differ")
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start = locator.get("line_start")
            end = locator.get("line_end")
            if (
                type(start) is not int
                or type(end) is not int
                or start < 1
                or end < start
                or end > len(markdown_bytes_lines)
            ):
                _fail("source_fifth_locator", f"{key} has an invalid Markdown span")
            span_bytes = b"".join(markdown_bytes_lines[start - 1 : end])
            if hashlib.sha256(span_bytes).hexdigest() != locator["span_sha256"]:
                _fail(
                    "source_fifth_markdown_span_hash",
                    f"{key} Markdown span changed",
                )
            section = "".join(markdown_lines[start - 1 : end])
            locator_texts.append(section)
            first_line = markdown_lines[start - 1].strip()
            if locator_index == 0 and first_line != f"##### {source_name}":
                _fail(
                    "source_fifth_locator",
                    f"{key} primary span does not start at its exact heading",
                )
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail(
                    "source_fifth_locator",
                    f"{key} locator heading does not match its source span",
                )
        for locator_index, phrase in spec["source_phrases"]:
            if phrase not in locator_texts[int(locator_index)]:
                _fail(
                    "source_fifth_source_text",
                    f"{key} source span omits {phrase!r}",
                )

        interpretation = spec["interpretations"][category]
        qualifiers = row.get("material_qualifiers")
        retained_residual = row.get("retained_source_residual")
        if (
            row.get("source_interpretation") != interpretation
            or not isinstance(qualifiers, list)
            or not qualifiers
            or not all(isinstance(value, str) and value.strip() for value in qualifiers)
            or not isinstance(retained_residual, str)
            or not retained_residual.strip()
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_fifth_formulation",
                f"{key} lacks the bounded accepted source formulation or proof limits",
            )
        combined_formulation = (
            f"{interpretation}\n" + "\n".join(qualifiers) + f"\n{retained_residual}"
        )
        for phrase in spec["required_qualifiers"][category]:
            if str(phrase).casefold() not in combined_formulation.casefold():
                _fail(
                    "source_fifth_qualifier",
                    f"{key} omits required qualifier {phrase!r}",
                )
        expected_members = spec.get("members")
        if (expected_members is None and "members" in row) or (
            expected_members is not None
            and row.get("members") != list(expected_members)
        ):
            _fail("source_fifth_enum", f"{key} exact ordered member roster differs")

        downstream_subobligations = [
            value
            for value in _array(
                classification.get("subobligations"), f"{key}.subobligations"
            )
            if isinstance(value, dict)
            and value.get("category")
            == "downstream_domain_consumer_admission_native_proof"
        ]
        if downstream_subobligations:
            selected_future_proof_keys.add(key)
        if any(
            value.get("status") != "NOT_ESTABLISHED"
            or value.get("gate_phase") != "FUTURE_PROOF"
            for value in downstream_subobligations
        ):
            _fail(
                "source_fifth_downstream",
                f"{key} promotes a downstream consumer/native proof",
            )

        if disposition == "SOURCE_CLOSED":
            if not retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ):
                _fail(
                    "source_fifth_closure",
                    f"{key} closure exceeds its selected source subobligation",
                )
            closed_keys.append(key)
            closed_subobligation_ids.append(subobligation_id)
        else:
            if retained_residual.startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ) or not retained_residual.startswith("HOLD_SOURCE_SUBOBLIGATION;"):
                _fail("source_fifth_hold", f"{key} source HOLD was removed")
            held_keys.append(key)
            held_subobligation_ids.append(subobligation_id)

    prior_contract = _object(
        manifest.get("source_fourth_resolution_contract"),
        "source_fourth_resolution_contract",
    )
    if (
        prior_contract.get("cumulative_reviewed_key_count") != 47
        or prior_contract.get("cumulative_source_closed_key_count") != 39
        or prior_contract.get("cumulative_source_closed_subobligation_count") != 40
        or prior_contract.get("cumulative_source_held_key_count") != 8
        or prior_contract.get("cumulative_source_held_subobligation_count") != 8
        or prior_contract.get("active_source_blocker_count") != 38
        or set(selected_future_proof_keys) != FIFTH_FUTURE_PROOF_KEYS
    ):
        _fail(
            "source_fifth_prior_contract",
            "fifth integration replaced prior cumulative evidence or future-proof IDs",
        )
    if (
        set(closed_keys) != FIFTH_SOURCE_CLOSED_KEYS
        or set(held_keys) != FIFTH_SOURCE_HELD_KEYS
        or len(closed_keys) != 9
        or len(set(closed_subobligation_ids)) != 9
        or len(held_keys) != 4
        or len(set(held_subobligation_ids)) != 4
        or len(selected_keys) != 12
        or len({str(spec["source_exact_name"]) for spec in FIFTH_SOURCE_ITEMS.values()})
        != 12
    ):
        _fail(
            "source_fifth_contract",
            "fifth source closure/HOLD or spell counts differ",
        )
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_subobligation_ids,
        "source_held_subobligation_ids": held_subobligation_ids,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_held_subobligation_count": len(held_subobligation_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_sixth_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the sixth reviewed source-only set to its exact registry and spans."""
    review = _object(manifest.get("source_sixth_review"), "source_sixth_review")
    if review != SIXTH_REVIEW:
        _fail("source_sixth_review", "sixth extraction/review identity differs")
    task_bytes = _read_pinned_local_evidence(
        SIXTH_REVIEW["task_evidence_path"],
        SIXTH_REVIEW["task_evidence_sha256"],
        "source_sixth_review",
    )
    try:
        task_evidence = task_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_sixth_review", "task evidence is not UTF-8")
    task_tokens = (
        SIXTH_REVIEW["candidate_sha256"],
        SIXTH_REVIEW["accepted_review_sha256"],
        "the Charmed creature cannot attack the charmer or target the charmer",
        "the moment its creator starts casting another spell that requires Concentration",
        "All 33 original `FUTURE_PROOF` subobligations remain `NOT_ESTABLISHED`.",
        "`/content_owner_default_repair` remains `REQUIRED_BEFORE_PACKAGE_PROMOTION`",
        "Word of Recall sanctuary redesignation/replacement/survival",
        "No claim is made for source readiness, recipe readiness, native support",
    )
    if any(token not in task_evidence for token in task_tokens):
        _fail("source_sixth_review", "task evidence omits a correction or proof limit")

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH, SOURCE_MARKDOWN_SHA256, "source_sixth_markdown"
    )
    try:
        byte_lines = markdown_bytes.splitlines(keepends=True)
        text_lines = [line.decode("utf-8") for line in byte_lines]
    except UnicodeDecodeError:
        _fail("source_sixth_markdown", "source Markdown is not UTF-8")

    contract = _object(
        manifest.get("source_sixth_resolution_contract"),
        "source_sixth_resolution_contract",
    )
    if contract.get("common_qualifiers") != list(SIXTH_COMMON_QUALIFIERS):
        _fail("source_sixth_qualifier", "common-rule wording differs")
    if contract.get("common_markdown_locators") != list(SIXTH_COMMON_MARKDOWN_LOCATORS):
        _fail("source_sixth_common_locator", "common source registry differs")
    expected_contract = {
        "status": "PARTIAL_SIXTH_REVIEWED_SET_SOURCE_ONLY",
        "selected_key_count": 12,
        "selected_spell_count": 11,
        "resolution_record_count": 13,
        "selected_source_closed_key_count": 9,
        "selected_source_closed_subobligation_count": 10,
        "selected_source_held_key_count": 3,
        "selected_source_held_subobligation_count": 3,
        "prior_reviewed_key_count": 59,
        "prior_resolution_record_count": 61,
        "prior_source_closed_key_count": 47,
        "prior_source_closed_subobligation_count": 49,
        "prior_source_held_key_count": 12,
        "prior_source_held_subobligation_count": 12,
        "prior_active_source_blocker_count": 30,
        "prior_active_source_blocker_entry_count": 28,
        "cumulative_reviewed_key_count": 71,
        "cumulative_resolution_record_count": 74,
        "cumulative_source_closed_key_count": 56,
        "cumulative_source_closed_subobligation_count": 59,
        "cumulative_source_held_key_count": 15,
        "cumulative_source_held_subobligation_count": 15,
        "original_record_count": 82,
        "original_source_blocking_key_count": 77,
        "downstream_only_key_count": 5,
        "active_source_blocker_count": 21,
        "active_source_blocker_entry_count": 20,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "production_claim": "NONE",
        "selected_original_classification_indexes": list(SIXTH_SELECTED_CLASSIFICATION_INDEXES),
        "common_markdown_locators": list(SIXTH_COMMON_MARKDOWN_LOCATORS),
        "common_qualifiers": list(SIXTH_COMMON_QUALIFIERS),
    }
    if contract != expected_contract:
        _fail("source_sixth_contract", "sixth counts or proof limits differ")

    prior = _object(manifest.get("source_fifth_resolution_contract"), "source_fifth_resolution_contract")
    if any(
        prior.get(field) != expected
        for field, expected in {
            "cumulative_reviewed_key_count": 59,
            "cumulative_resolution_record_count": 61,
            "cumulative_source_closed_key_count": 47,
            "cumulative_source_closed_subobligation_count": 49,
            "cumulative_source_held_key_count": 12,
            "cumulative_source_held_subobligation_count": 12,
            "active_source_blocker_count": 30,
            "active_source_blocker_entry_count": 28,
        }.items()
    ):
        _fail("source_sixth_prior_contract", "prior cumulative evidence changed")

    for locator in SIXTH_COMMON_MARKDOWN_LOCATORS:
        start, end = int(locator["line_start"]), int(locator["line_end"])
        heading = str(locator["heading"])
        if start < 1 or end < start or end > len(byte_lines):
            _fail("source_sixth_common_locator", "common span bounds are invalid")
        span = b"".join(byte_lines[start - 1 : end])
        if hashlib.sha256(span).hexdigest() != locator["span_sha256"]:
            _fail("source_sixth_markdown_span_hash", f"common span changed: {heading}")
        section = "".join(text_lines[start - 1 : end])
        if any(phrase not in section for phrase in SIXTH_COMMON_REQUIRED_PHRASES[heading]):
            _fail("source_sixth_common_source_text", f"common span omits {heading} clause")

    rows = [
        _object(value, f"source_sixth_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_sixth_resolution_evidence"), "source_sixth_resolution_evidence")
        )
    ]
    actual_order = tuple(
        (str(row.get("review_item_id")), str(row.get("unresolved_key")), str(row.get("source_category")))
        for row in rows
    )
    if (
        len(rows) != len(SIXTH_EVIDENCE_ORDER)
        or actual_order != SIXTH_EVIDENCE_ORDER
        or len({row.get("unresolved_key") for row in rows}) != 12
        or len({(row.get("unresolved_key"), row.get("source_category")) for row in rows}) != 13
    ):
        _fail("source_sixth_census", "selected source key/category/order census differs")

    previous_keys = (
        set(SOURCE_RESOLUTION_KEYS)
        | set(NEXT12_SELECTED_KEYS)
        | set(THIRD12_SELECTED_KEYS)
        | set(FOURTH_SELECTED_KEYS)
        | set(FIFTH_SELECTED_KEYS)
    )
    selected_keys = set(SIXTH_SOURCE_ITEMS)
    if previous_keys & selected_keys:
        _fail("source_sixth_census", "sixth evidence replaces a prior key")
    selected_indexes = tuple(
        int(SIXTH_SOURCE_ITEMS[key]["classification_index"])
        for key in dict.fromkeys(key for _, key, _ in SIXTH_EVIDENCE_ORDER)
    )
    if selected_indexes != SIXTH_SELECTED_CLASSIFICATION_INDEXES:
        _fail("source_sixth_census", "selected original index roster differs")

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_carrier = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    body_rows = _rows(body_carrier, "rows", "source-body-witnesses")
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_ids: list[str] = []
    held_ids: list[str] = []
    selected_future: set[str] = set()

    for (item_id, key, category), row in zip(SIXTH_EVIDENCE_ORDER, rows, strict=True):
        spec = SIXTH_SOURCE_ITEMS[key]
        index = int(spec["classification_index"])
        entry_index = int(spec["map_entry_index"])
        pass_index = int(spec["source_pass_row"])
        witness_index = int(spec["body_witness_row"])
        name = str(spec["source_exact_name"])
        disposition = str(spec["disposition"])
        subobligation_id = f"{key}::{category}"
        classification_pointer = f"/source_unknown_classifications/{index}"
        history_pointer = f"/source_mapping_lanes/0/mapping_payload/unresolved_key_index/{index}"
        map_pointer = f"/source_mapping_lanes/0/mapping_payload/entries/{entry_index}"
        source_pointer = f"/rows/{pass_index}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{pass_index}/qualifications"
        body_pointer = f"/rows/{witness_index}"
        classification = classified_by_key.get(key)
        if classification is None or key in previous_keys:
            _fail("source_sixth_key", f"{key} is absent or replaces prior evidence")

        original = _object(_resolve_json_pointer(manifest, classification_pointer, "sixth classification pointer"), f"{key}.classification")
        history = _object(_resolve_json_pointer(manifest, history_pointer, "sixth history pointer"), f"{key}.history")
        map_entry = _object(_resolve_json_pointer(manifest, map_pointer, "sixth current-map pointer"), f"{key}.current_map")
        unresolved_rows = [_object(value, f"{key}.map.unresolved_keys[{i}]") for i, value in enumerate(_array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys"))]
        source_ref = _object(classification.get("evidence_ref"), f"{key}.evidence_ref")
        history_matches = (
            history.get("unresolved_key") == key
            and history.get("source_exact_name") == name
            and history.get("reason") == classification.get("original_reason")
            and history.get("evidence_ref") == source_ref
            and history.get("status") == classification.get("original_status")
            and history.get("disposition") == classification.get("original_disposition")
        )
        map_matches = map_entry.get("source_exact_name") == name and any(item.get("unresolved_key") == key for item in unresolved_rows)
        source_subobligations = [
            _object(value, f"{key}.subobligations[{i}]")
            for i, value in enumerate(_array(classification.get("subobligations"), f"{key}.subobligations"))
            if isinstance(value, dict) and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        exact_subobligation = any(
            value.get("subobligation_id") == subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            and value.get("gate_phase") == "SP00_SOURCE"
            for value in source_subobligations
        )
        if row.get("disposition") != disposition:
            _fail("source_sixth_disposition", f"{key} disposition differs")
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != name
            or row.get("source_category") != category
            or row.get("subobligation_id") != subobligation_id
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original
            or original.get("unresolved_key") != key
            or original.get("source_exact_name") != name
            or original.get("source_unresolved_record_pointer") != history_pointer
            or original.get("source_ready_blocking") is not True
            or original.get("original_status") != "NOT_ESTABLISHED"
            or not history_matches
            or not map_matches
            or not exact_subobligation
        ):
            _fail("source_sixth_binding", f"{key} no longer binds to its original records")

        source_record, body_witness = source_rows[pass_index], body_rows[witness_index]
        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
        }
        expected_evidence_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "exact_record_name": name,
            "record_index": pass_index,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "source_heading": name,
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
            "evidence_boundary": "RETAINED_FULL_BODY_REVIEW_SUMMARY_DECOMPOSITION; NO_NEW_PRIMARY_BODY_OR_NATIVE_CONSUMER_PROOF",
        }
        if (
            source_record.get("name") != name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or source_record.get("hash_basis") != "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization"
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
            or row.get("source_record_ref") != expected_ref
            or source_ref != expected_evidence_ref
        ):
            _fail("source_sixth_provenance", f"{key} borrows a source/body witness")

        locators = [_object(value, f"{key}.source_markdown_locators[{i}]") for i, value in enumerate(_array(row.get("source_markdown_locators"), f"{key}.source_markdown_locators"))]
        if locators != list(spec["locators"]):
            _fail("source_sixth_locator", f"{key} locators differ")
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start, end = locator.get("line_start"), locator.get("line_end")
            if type(start) is not int or type(end) is not int or start < 1 or end < start or end > len(byte_lines):
                _fail("source_sixth_locator", f"{key} span bounds are invalid")
            span = b"".join(byte_lines[start - 1 : end])
            if hashlib.sha256(span).hexdigest() != locator["span_sha256"]:
                _fail("source_sixth_markdown_span_hash", f"{key} span changed")
            section = "".join(text_lines[start - 1 : end])
            locator_texts.append(section)
            first_line = text_lines[start - 1].strip()
            if locator_index == 0 and first_line != f"##### {name}":
                _fail("source_sixth_locator", f"{key} body heading differs")
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail("source_sixth_locator", f"{key} locator heading differs")
        if any(phrase not in locator_texts[index] for index, phrase in spec["source_phrases"]):
            _fail("source_sixth_source_text", f"{key} omits a source phrase")

        interpretation = _object(spec["interpretations"], f"{key}.interpretations").get(category)
        qualifiers = _object(spec["required_qualifiers"], f"{key}.required_qualifiers").get(category)
        if (
            row.get("source_interpretation") != interpretation
            or row.get("material_qualifiers") != list(qualifiers)
            or row.get("retained_source_residual") != SIXTH_SOURCE_RESIDUALS[(key, category)]
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail("source_sixth_qualifier", f"{key} formulation/proof limits differ")
        members = spec.get("members")
        if (members is None and "members" in row) or (members is not None and row.get("members") != list(members)):
            _fail("source_sixth_enum", f"{key} member order differs")

        downstream = [
            value for value in _array(classification.get("subobligations"), f"{key}.subobligations")
            if isinstance(value, dict) and value.get("category") == "downstream_domain_consumer_admission_native_proof"
        ]
        if downstream:
            selected_future.add(key)
        if any(value.get("status") != "NOT_ESTABLISHED" or value.get("gate_phase") != "FUTURE_PROOF" for value in downstream):
            _fail("source_sixth_downstream", f"{key} promotes future proof")

        if disposition == "SOURCE_CLOSED":
            if not str(row.get("retained_source_residual", "")).startswith("NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"):
                _fail("source_sixth_closure", f"{key} closure exceeds the selected subobligation")
            closed_keys.append(key)
            closed_ids.append(subobligation_id)
        else:
            if not str(row.get("retained_source_residual", "")).startswith("HOLD_SOURCE_SUBOBLIGATION;"):
                _fail("source_sixth_hold", f"{key} HOLD was removed")
            held_keys.append(key)
            held_ids.append(subobligation_id)

    if (
        selected_future != SIXTH_FUTURE_PROOF_KEYS
        or set(closed_keys) != SIXTH_SOURCE_CLOSED_KEYS
        or set(held_keys) != SIXTH_SOURCE_HELD_KEYS
        or len(set(closed_keys)) != 9
        or len(set(closed_ids)) != 10
        or len(set(held_keys)) != 3
        or len(set(held_ids)) != 3
        or len(selected_keys) != 12
        or len({str(item["source_exact_name"]) for item in SIXTH_SOURCE_ITEMS.values()}) != 11
    ):
        _fail("source_sixth_contract", "sixth closure/HOLD/future proof counts differ")
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_ids,
        "source_held_subobligation_ids": held_ids,
        "source_resolved_subobligation_count": len(closed_ids),
        "source_held_subobligation_count": len(held_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_seventh_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind the seventh reviewed source-only set to its exact registry and spans."""
    review = _object(manifest.get("source_seventh_review"), "source_seventh_review")
    if review != SEVENTH_REVIEW:
        _fail("source_seventh_review", "seventh extraction/review identity differs")
    task_bytes = _read_pinned_local_evidence(
        SEVENTH_REVIEW["task_evidence_path"],
        SEVENTH_REVIEW["task_evidence_sha256"],
        "source_seventh_review",
    )
    try:
        task_evidence = task_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_seventh_review", "task evidence is not UTF-8")
    task_tokens = (
        SEVENTH_REVIEW["candidate_sha256"],
        SEVENTH_REVIEW["accepted_review_sha256"],
        "The independent review accepts five `CLOSE` source subobligations across four keys and two `HOLD` subobligations across two keys.",
        "The exact subtraction remains identity-based: the 77 original source-blocking classification keys minus the 71 keys reviewed by batches one through six leaves exactly indexes `6, 30, 31, 32, 80, 81`.",
        "All 33 original `FUTURE_PROOF` subobligations remain `NOT_ESTABLISHED`.",
        "The conditional Thunderclap installed-default repair remains `REQUIRED_BEFORE_PACKAGE_PROMOTION`",
        "Word of Recall’s source-modeling residual remains `NOT_ESTABLISHED`",
        "Source qualification remains not established; no 339-spell source-ready declaration",
        "Life Bond triggers when the caster actually regains Hit Points from a level 1+ spell",
        "the steed regains the same number of Hit Points the caster actually regained",
        "Fell Glare is a Wisdom saving throw against the caster’s spell save DC",
        "targeting one creature within 60 feet of the steed that the steed can see",
        "Preserve U+2212 in the negative Int",
        "Wisdom is positive (`+1/+1`)",
    )
    if any(token not in task_evidence for token in task_tokens):
        _fail("source_seventh_review", "task evidence omits an accepted disposition or proof limit")

    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH, SOURCE_MARKDOWN_SHA256, "source_seventh_markdown"
    )
    try:
        byte_lines = markdown_bytes.splitlines(keepends=True)
        text_lines = [line.decode("utf-8") for line in byte_lines]
    except UnicodeDecodeError:
        _fail("source_seventh_markdown", "source Markdown is not UTF-8")

    contract = _object(
        manifest.get("source_seventh_resolution_contract"),
        "source_seventh_resolution_contract",
    )
    if contract.get("common_qualifiers") != list(SEVENTH_COMMON_QUALIFIERS):
        _fail("source_seventh_qualifier", "common-rule wording differs")
    if contract.get("common_markdown_locators") != list(SEVENTH_COMMON_MARKDOWN_LOCATORS):
        _fail("source_seventh_common_locator", "common source registry differs")
    expected_contract = {
        "status": "PARTIAL_SEVENTH_REVIEWED_SET_SOURCE_ONLY",
        "selected_key_count": 6,
        "selected_spell_count": 5,
        "resolution_record_count": 7,
        "selected_source_closed_key_count": 4,
        "selected_source_closed_subobligation_count": 5,
        "selected_source_held_key_count": 2,
        "selected_source_held_subobligation_count": 2,
        "prior_reviewed_key_count": 71,
        "prior_resolution_record_count": 74,
        "prior_source_closed_key_count": 56,
        "prior_source_closed_subobligation_count": 59,
        "prior_source_held_key_count": 15,
        "prior_source_held_subobligation_count": 15,
        "prior_active_source_blocker_count": 21,
        "prior_active_source_blocker_entry_count": 20,
        "cumulative_reviewed_key_count": 77,
        "cumulative_resolution_record_count": 81,
        "cumulative_source_closed_key_count": 60,
        "cumulative_source_closed_subobligation_count": 64,
        "cumulative_source_held_key_count": 17,
        "cumulative_source_held_subobligation_count": 17,
        "original_record_count": 82,
        "original_source_blocking_key_count": 77,
        "downstream_only_key_count": 5,
        "active_source_blocker_count": 17,
        "active_source_blocker_entry_count": 17,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "production_claim": "NONE",
        "selected_original_classification_indexes": list(SEVENTH_SELECTED_CLASSIFICATION_INDEXES),
        "common_markdown_locators": list(SEVENTH_COMMON_MARKDOWN_LOCATORS),
        "common_qualifiers": list(SEVENTH_COMMON_QUALIFIERS),
    }
    if contract != expected_contract:
        _fail("source_seventh_contract", "seventh counts or proof limits differ")

    prior = _object(manifest.get("source_sixth_resolution_contract"), "source_sixth_resolution_contract")
    if any(
        prior.get(field) != expected
        for field, expected in {
            "cumulative_reviewed_key_count": 71,
            "cumulative_resolution_record_count": 74,
            "cumulative_source_closed_key_count": 56,
            "cumulative_source_closed_subobligation_count": 59,
            "cumulative_source_held_key_count": 15,
            "cumulative_source_held_subobligation_count": 15,
            "active_source_blocker_count": 21,
            "active_source_blocker_entry_count": 20,
        }.items()
    ):
        _fail("source_seventh_prior_contract", "prior sixth cumulative evidence changed")

    for locator in SEVENTH_COMMON_MARKDOWN_LOCATORS:
        start, end = int(locator["line_start"]), int(locator["line_end"])
        heading = str(locator["heading"])
        if start < 1 or end < start or end > len(byte_lines):
            _fail("source_seventh_common_locator", "common span bounds are invalid")
        span = b"".join(byte_lines[start - 1 : end])
        if hashlib.sha256(span).hexdigest() != locator["span_sha256"]:
            _fail("source_seventh_markdown_span_hash", f"common span changed: {heading}")
        section = "".join(text_lines[start - 1 : end])
        if any(phrase not in section for phrase in SEVENTH_COMMON_REQUIRED_PHRASES[heading]):
            _fail("source_seventh_common_source_text", f"common span omits {heading} clause")

    rows = [
        _object(value, f"source_seventh_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_seventh_resolution_evidence"),
                "source_seventh_resolution_evidence",
            )
        )
    ]
    actual_order = tuple(
        (str(row.get("review_item_id")), str(row.get("unresolved_key")), str(row.get("source_category")))
        for row in rows
    )
    selected_keys = set(SEVENTH_SOURCE_ITEMS)
    if (
        len(rows) != len(SEVENTH_EVIDENCE_ORDER)
        or actual_order != SEVENTH_EVIDENCE_ORDER
        or len({row.get("unresolved_key") for row in rows}) != 6
        or len({(row.get("unresolved_key"), row.get("source_category")) for row in rows}) != 7
    ):
        _fail("source_seventh_census", "selected source key/category/order census differs")

    previous_keys = (
        set(SOURCE_RESOLUTION_KEYS)
        | set(NEXT12_SELECTED_KEYS)
        | set(THIRD12_SELECTED_KEYS)
        | set(FOURTH_SELECTED_KEYS)
        | set(FIFTH_SELECTED_KEYS)
        | set(SIXTH_SOURCE_ITEMS)
    )
    if previous_keys & selected_keys:
        _fail("source_seventh_census", "seventh evidence replaces a prior key")
    selected_indexes = tuple(
        int(SEVENTH_SOURCE_ITEMS[key]["classification_index"])
        for key in dict.fromkeys(key for _, key, _ in SEVENTH_EVIDENCE_ORDER)
    )
    if selected_indexes != SEVENTH_SELECTED_CLASSIFICATION_INDEXES:
        _fail("source_seventh_census", "selected original index roster differs")

    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_carrier = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    body_rows = _rows(body_carrier, "rows", "source-body-witnesses")
    closed_keys: list[str] = []
    held_keys: list[str] = []
    closed_ids: list[str] = []
    held_ids: list[str] = []
    selected_future: set[str] = set()

    for (item_id, key, category), row in zip(SEVENTH_EVIDENCE_ORDER, rows, strict=True):
        spec = SEVENTH_SOURCE_ITEMS[key]
        index = int(spec["classification_index"])
        entry_index = int(spec["map_entry_index"])
        pass_index = int(spec["source_pass_row"])
        witness_index = int(spec["body_witness_row"])
        name = str(spec["source_exact_name"])
        disposition = str(spec["dispositions"][category])
        subobligation_id = f"{key}::{category}"
        classification_pointer = f"/source_unknown_classifications/{index}"
        history_pointer = f"/source_mapping_lanes/0/mapping_payload/unresolved_key_index/{index}"
        map_pointer = f"/source_mapping_lanes/0/mapping_payload/entries/{entry_index}"
        source_pointer = f"/rows/{pass_index}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{pass_index}/qualifications"
        body_pointer = f"/rows/{witness_index}"
        classification = classified_by_key.get(key)
        if classification is None or key in previous_keys:
            _fail("source_seventh_key", f"{key} is absent or replaces prior evidence")

        original = _object(
            _resolve_json_pointer(manifest, classification_pointer, "seventh classification pointer"),
            f"{key}.classification",
        )
        history = _object(
            _resolve_json_pointer(manifest, history_pointer, "seventh history pointer"),
            f"{key}.history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "seventh current-map pointer"),
            f"{key}.current_map",
        )
        unresolved_rows = [
            _object(value, f"{key}.map.unresolved_keys[{i}]")
            for i, value in enumerate(
                _array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys")
            )
        ]
        source_ref = _object(classification.get("evidence_ref"), f"{key}.evidence_ref")
        history_matches = (
            history.get("unresolved_key") == key
            and history.get("source_exact_name") == name
            and history.get("reason") == classification.get("original_reason")
            and history.get("evidence_ref") == source_ref
            and history.get("status") == classification.get("original_status")
            and history.get("disposition") == classification.get("original_disposition")
        )
        map_matches = map_entry.get("source_exact_name") == name and any(
            item.get("unresolved_key") == key for item in unresolved_rows
        )
        source_subobligations = [
            _object(value, f"{key}.subobligations[{i}]")
            for i, value in enumerate(
                _array(classification.get("subobligations"), f"{key}.subobligations")
            )
            if isinstance(value, dict) and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        exact_subobligation = any(
            value.get("subobligation_id") == subobligation_id
            and value.get("category") == category
            and value.get("status") == "NOT_ESTABLISHED"
            and value.get("gate_phase") == "SP00_SOURCE"
            for value in source_subobligations
        )
        if row.get("disposition") != disposition:
            _fail("source_seventh_disposition", f"{key} disposition differs")
        if (
            row.get("review_item_id") != item_id
            or row.get("unresolved_key") != key
            or row.get("source_exact_name") != name
            or row.get("source_category") != category
            or row.get("subobligation_id") != subobligation_id
            or row.get("source_classification_pointer") != classification_pointer
            or row.get("source_unresolved_record_pointer") != history_pointer
            or row.get("current_map_pointer") != map_pointer
            or classification != original
            or original.get("unresolved_key") != key
            or original.get("source_exact_name") != name
            or original.get("source_unresolved_record_pointer") != history_pointer
            or original.get("source_ready_blocking") is not True
            or original.get("original_status") != "NOT_ESTABLISHED"
            or not history_matches
            or not map_matches
            or not exact_subobligation
        ):
            _fail("source_seventh_binding", f"{key} no longer binds to its original records")

        source_record, body_witness = source_rows[pass_index], body_rows[witness_index]
        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": source_record.get("hash_basis"),
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
        }
        expected_evidence_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "exact_record_name": name,
            "record_index": pass_index,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "source_heading": name,
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
            "evidence_boundary": "RETAINED_FULL_BODY_REVIEW_SUMMARY_DECOMPOSITION; NO_NEW_PRIMARY_BODY_OR_NATIVE_CONSUMER_PROOF",
        }
        if (
            source_record.get("name") != name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or source_record.get("hash_basis") != "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization"
            or not isinstance(source_record.get("qualifications"), list)
            or body_witness.get("name") != name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
            or row.get("source_record_ref") != expected_ref
            or source_ref != expected_evidence_ref
        ):
            _fail("source_seventh_provenance", f"{key} borrows a source/body witness")

        locators = [
            _object(value, f"{key}.source_markdown_locators[{i}]")
            for i, value in enumerate(
                _array(row.get("source_markdown_locators"), f"{key}.source_markdown_locators")
            )
        ]
        expected_locators = list(spec["locators"][category])
        if locators != expected_locators:
            _fail("source_seventh_locator", f"{key} Markdown locator set differs")
        locator_texts: list[str] = []
        for locator_index, locator in enumerate(locators):
            start, end = locator.get("line_start"), locator.get("line_end")
            if type(start) is not int or type(end) is not int or start < 1 or end < start or end > len(byte_lines):
                _fail("source_seventh_locator", f"{key} span bounds are invalid")
            span = b"".join(byte_lines[start - 1 : end])
            if hashlib.sha256(span).hexdigest() != locator["span_sha256"]:
                _fail("source_seventh_markdown_span_hash", f"{key} span changed")
            section = "".join(text_lines[start - 1 : end])
            locator_texts.append(section)
            first_line = text_lines[start - 1].strip()
            if locator_index == 0:
                locator_heading = str(locator["heading"])
                heading_prefix = "#####" if locator_heading == name else "####"
                if first_line != f"{heading_prefix} {locator_heading}":
                    _fail("source_seventh_locator", f"{key} body/block heading differs")
            if first_line.startswith("#") and str(locator["heading"]) not in first_line:
                _fail("source_seventh_locator", f"{key} locator heading differs")
        source_phrases = spec["source_phrases"][category]
        if any(phrase not in locator_texts[index] for index, phrase in source_phrases):
            _fail("source_seventh_source_text", f"{key} omits a source phrase")

        if (
            row.get("source_interpretation") != spec["interpretations"][category]
            or row.get("material_qualifiers") != list(spec["required_qualifiers"][category])
            or row.get("retained_source_residual") != SEVENTH_SOURCE_RESIDUALS[(key, category)]
            or row.get("future_native_proof_status") != "NOT_ESTABLISHED"
            or row.get("actual_native_proof_refs") != []
        ):
            _fail("source_seventh_qualifier", f"{key} formulation/proof limits differ")
        if "members" in row:
            _fail("source_seventh_enum", f"{key} adds an unreviewed enumerable member list")

        downstream = [
            value
            for value in _array(classification.get("subobligations"), f"{key}.subobligations")
            if isinstance(value, dict)
            and value.get("category") == "downstream_domain_consumer_admission_native_proof"
        ]
        if downstream:
            selected_future.add(key)
        if any(
            value.get("status") != "NOT_ESTABLISHED" or value.get("gate_phase") != "FUTURE_PROOF"
            for value in downstream
        ):
            _fail("source_seventh_downstream", f"{key} promotes future proof")

        if disposition == "SOURCE_CLOSED":
            if not str(row.get("retained_source_residual", "")).startswith(
                "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
            ):
                _fail("source_seventh_closure", f"{key} closure exceeds the selected subobligation")
            closed_keys.append(key)
            closed_ids.append(subobligation_id)
        else:
            if not str(row.get("retained_source_residual", "")).startswith(
                "HOLD_SOURCE_SUBOBLIGATION;"
            ):
                _fail("source_seventh_hold", f"{key} HOLD was removed")
            held_keys.append(key)
            held_ids.append(subobligation_id)

    if (
        selected_future != SEVENTH_FUTURE_PROOF_KEYS
        or set(closed_keys) != SEVENTH_SOURCE_CLOSED_KEYS
        or set(held_keys) != SEVENTH_SOURCE_HELD_KEYS
        or len(set(closed_keys)) != 4
        or len(set(closed_ids)) != 5
        or len(set(held_keys)) != 2
        or len(set(held_ids)) != 2
        or len(selected_keys) != 6
        or len({str(item["source_exact_name"]) for item in SEVENTH_SOURCE_ITEMS.values()}) != 5
    ):
        _fail("source_seventh_contract", "seventh closure/HOLD/future proof counts differ")
    return {
        "source_resolution_records": rows,
        "source_resolved_keys": closed_keys,
        "source_held_keys": held_keys,
        "source_closed_subobligation_ids": closed_ids,
        "source_held_subobligation_ids": held_ids,
        "source_resolved_subobligation_count": len(closed_ids),
        "source_held_subobligation_count": len(held_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_eighth_resolution_evidence(
    manifest: Mapping[str, object],
    classified_by_key: Mapping[str, dict[str, object]],
) -> dict[str, object]:
    """Bind six held SP00 keys to the accepted owner, without claiming explicit RAW."""
    owner = _object(
        manifest.get("source_interpretation_owner"), "source_interpretation_owner"
    )
    if owner != SOURCE_INTERPRETATION_OWNER:
        _fail(
            "source_interpretation_owner",
            "accepted owner path, byte identity, authority, scope or key set differs",
        )

    decision_bytes = _read_pinned_local_evidence(
        str(SOURCE_INTERPRETATION_OWNER["decision_path"]),
        str(SOURCE_INTERPRETATION_OWNER["decision_sha256"]),
        "source_interpretation_owner",
    )
    review_bytes = _read_pinned_local_evidence(
        str(SOURCE_INTERPRETATION_OWNER["review_path"]),
        str(SOURCE_INTERPRETATION_OWNER["review_sha256"]),
        "source_interpretation_review",
    )
    brief_bytes = _read_pinned_local_evidence(
        str(SOURCE_INTERPRETATION_OWNER["historical_brief_path"]),
        str(SOURCE_INTERPRETATION_OWNER["historical_brief_sha256"]),
        "source_interpretation_brief",
    )
    try:
        decision_text = decision_bytes.decode("utf-8")
        review_text = review_bytes.decode("utf-8")
        brief_text = brief_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("source_interpretation_owner", "owner/review/brief is not UTF-8")

    if not all(
        token in decision_text
        for token in (
            "Status: **ACCEPTED PRODUCT OWNER DECISION — IMPLEMENTATION-FACING LAW**",
            "This is the sole final owner of these six HDM interpretations.",
            "Machine source evidence must bind this owner decision and synchronize",
            "No active schema/catalog/profile/recipe is",
            "registered here. Package/admission/native/end-to-end/latency proof, other source",
            "holds, default/Word of Recall/future-proof lanes and auth/turn bridges remain.",
        )
    ):
        _fail("source_interpretation_owner", "accepted owner status, scope or proof limit differs")
    owner_lines = decision_text.splitlines()
    section_required_tokens = {
        "A": (
            "Change current HP by delta = b_after - b_before",
            "Actor HP remains the sole amount.",
            "never restore entry HP",
        ),
        "B": (
            "Each damaging dart is a distinct native damage instance",
            "All darts of the cast retain the source's simultaneous group",
            "Retry/recovery reuses fixed results and accepted identities.",
        ),
        "C": (
            "Commit the selected creature identities at casting.",
            "A previously unselected later entrant gains no benefit",
            "No free reassignment, new update action or generic ongoing caster-to-target range leash",
        ),
        "D": (
            "floor each resulting derived movement capability at0",
            "Retain raw negative contributions",
            "Exact-zero consumers observe the final nonnegative capability",
        ),
        "E": (
            "Use the first eligible positive damaging occurrence of each actual turn",
            "One fixed d4 reduces only the selected damage-type subtotal",
            "No excess reduction spills into any other type",
        ),
        "F": (
            "Copy the damage the target takes after its defenses, before allocation into its temporary/current HP.",
            "Warding Bond is the new proximate cause",
            "Target taking5Fire leads to resistant caster taking2",
        ),
    }
    for key, spec in SOURCE_EIGHTH_ITEMS.items():
        section = str(spec["owner_section"])
        heading = f"## {section}. {spec['owner_section_heading']}"
        matches = [index for index, line in enumerate(owner_lines) if line == heading]
        if len(matches) != 1:
            _fail("source_interpretation_owner", f"accepted owner section {section} is missing or duplicated")
        start = matches[0] + 1
        end = next(
            (index for index in range(start, len(owner_lines)) if owner_lines[index].startswith("## ")),
            len(owner_lines),
        )
        section_text = " ".join("\n".join(owner_lines[start:end]).split())
        if any(token not in section_text for token in section_required_tokens[section]):
            _fail("source_interpretation_owner", f"accepted owner section {section} lacks its bound clauses")

    review_flat = " ".join(review_text.split())
    brief_flat = " ".join(brief_text.split())
    if not all(
        token in review_flat
        for token in (
            "The subsequent Product Owner accepts the complete proposed package",
            "current final authority is",
            "The six narrower outcome profiles still require the explicit accepted interpretation gate.",
        )
    ):
        _fail("source_interpretation_review", "historical targeted review no longer routes to accepted owner")
    if not all(
        token in brief_flat
        for token in (
            "Status: **HISTORICAL PRE-ACCEPTANCE BRIEF — SIX POLICIES ACCEPTED 2026-10-14**",
            "Current final law: [accepted A–F owner decision]",
            "pending-approval wording is no longer current scheduling or normative authority.",
        )
    ):
        _fail("source_interpretation_brief", "superseded Decision Brief is not explicitly historical")

    rows = [
        _object(value, f"source_eighth_resolution_evidence[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_eighth_resolution_evidence"),
                "source_eighth_resolution_evidence",
            )
        )
    ]
    expected_order = tuple(SOURCE_INTERPRETATION_OWNER["accepted_keys"])
    actual_order = tuple(str(row.get("unresolved_key")) for row in rows)
    if len(rows) != 6 or actual_order != expected_order:
        _fail("source_eighth_census", "owner-decision resolution key/order census differs")

    prior_key_batches = (
        ("source_unknown_resolution_evidence", "source_unknown_resolution_evidence"),
        ("source_next12_resolution_evidence", "source_next12_resolution_evidence"),
        ("source_third12_resolution_evidence", "source_third12_resolution_evidence"),
        ("source_fourth_resolution_evidence", "source_fourth_resolution_evidence"),
        ("source_fifth_resolution_evidence", "source_fifth_resolution_evidence"),
        ("source_sixth_resolution_evidence", "source_sixth_resolution_evidence"),
        ("source_seventh_resolution_evidence", "source_seventh_resolution_evidence"),
    )
    prior_records_by_field = {
        field: [
            _object(value, f"{field}[{index}]")
            for index, value in enumerate(_array(manifest.get(field), field))
        ]
        for field, _ in prior_key_batches
    }
    evidence = _load_evidence(manifest)
    source_pass = _object(evidence["source-pass-0-2"], "source-pass-0-2")
    body_carrier = _object(evidence["source-body-witnesses"], "source-body-witnesses")
    source_rows = _rows(source_pass, "rows", "source-pass-0-2")
    witness_rows = _rows(body_carrier, "rows", "source-body-witnesses")
    markdown_bytes = _read_pinned_local_evidence(
        SOURCE_MARKDOWN_RELATIVE_PATH, SOURCE_MARKDOWN_SHA256, "source_eighth_markdown"
    )
    try:
        markdown_lines = markdown_bytes.splitlines(keepends=True)
        markdown_text_lines = [line.decode("utf-8") for line in markdown_lines]
    except UnicodeDecodeError:
        _fail("source_eighth_markdown", "source Markdown is not UTF-8")

    lane0 = next(
        (
            _object(value, f"source_mapping_lanes[{index}]")
            for index, value in enumerate(_array(manifest.get("source_mapping_lanes"), "source_mapping_lanes"))
            if isinstance(value, dict) and value.get("lane_id") == "source-pass-0-2"
        ),
        None,
    )
    if lane0 is None:
        _fail("source_eighth_binding", "source-pass-0-2 current map is unavailable")

    resolved_keys: list[str] = []
    closed_ids: list[str] = []
    for index, (key, row) in enumerate(zip(expected_order, rows, strict=True)):
        spec = SOURCE_EIGHTH_ITEMS[key]
        category = str(spec["source_category"])
        section = str(spec["owner_section"])
        classification_index = int(spec["classification_index"])
        map_entry_index = int(spec["map_entry_index"])
        source_pass_row = int(spec["source_pass_row"])
        body_witness_row = int(spec["body_witness_row"])
        source_name = str(spec["source_exact_name"])
        subobligation_id = f"{key}::{category}"
        classification_pointer = f"/source_unknown_classifications/{classification_index}"
        history_pointer = (
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/"
            f"{classification_index}"
        )
        map_pointer = f"/source_mapping_lanes/0/mapping_payload/entries/{map_entry_index}"
        source_pointer = f"/rows/{source_pass_row}/required_modes_or_exceptions"
        qualification_pointer = f"/rows/{source_pass_row}/qualifications"
        body_pointer = f"/rows/{body_witness_row}"
        classification = classified_by_key.get(key)
        if classification is None:
            _fail("source_eighth_binding", f"{key} has no exact historical classification")
        original = _object(
            _resolve_json_pointer(manifest, classification_pointer, "eighth classification pointer"),
            f"{key}.classification",
        )
        history = _object(
            _resolve_json_pointer(manifest, history_pointer, "eighth history pointer"),
            f"{key}.history",
        )
        map_entry = _object(
            _resolve_json_pointer(manifest, map_pointer, "eighth current-map pointer"),
            f"{key}.current_map",
        )
        expected_subobligations = [
            value
            for value in _array(original.get("subobligations"), f"{key}.subobligations")
            if isinstance(value, dict) and value.get("category") in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        ]
        matching_subobligations = [
            _object(value, f"{key}.source_subobligation")
            for value in expected_subobligations
            if value.get("subobligation_id") == subobligation_id
        ]
        if (
            len(matching_subobligations) != 1
            or matching_subobligations[0].get("category") != category
            or matching_subobligations[0].get("gate_phase") != "SP00_SOURCE"
            or matching_subobligations[0].get("status") != "NOT_ESTABLISHED"
            or original.get("unresolved_key") != key
            or original.get("source_exact_name") != source_name
            or original.get("source_ready_blocking") is not True
            or original.get("original_status") != "NOT_ESTABLISHED"
            or original.get("source_unresolved_record_pointer") != history_pointer
        ):
            _fail("source_eighth_binding", f"{key} is not the exact open source subobligation")

        expected_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "source_exact_name": source_name,
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
        }
        expected_classification_ref = {
            "artifact_id": "source-pass-0-2",
            "json_pointer": source_pointer,
            "exact_record_name": source_name,
            "record_index": source_pass_row,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": int(spec["printed_page"]),
            "source_header_line": int(spec["source_header_line"]),
            "source_heading": source_name,
            "raw_body_sha256": str(spec["raw_body_sha256"]),
            "raw_hash_basis": "Exact decoded body field UTF8 bytes, no whitespace/glyph/page-tail normalization",
            "body_witness_ref": {"artifact_id": "source-body-witnesses", "json_pointer": body_pointer},
            "qualification_ref": {"artifact_id": "source-pass-0-2", "json_pointer": qualification_pointer},
            "evidence_boundary": "RETAINED_FULL_BODY_REVIEW_SUMMARY_DECOMPOSITION; NO_NEW_PRIMARY_BODY_OR_NATIVE_CONSUMER_PROOF",
        }
        source_record = source_rows[source_pass_row]
        body_witness = witness_rows[body_witness_row]
        unresolved_rows = [
            _object(value, f"{key}.map.unresolved_keys[{map_index}]")
            for map_index, value in enumerate(_array(map_entry.get("unresolved_keys"), f"{key}.map.unresolved_keys"))
        ]
        if (
            history.get("unresolved_key") != key
            or history.get("source_exact_name") != source_name
            or history.get("reason") != original.get("original_reason")
            or history.get("evidence_ref") != original.get("evidence_ref")
            or history.get("status") != original.get("original_status")
            or history.get("disposition") != original.get("original_disposition")
            or map_entry.get("source_exact_name") != source_name
            or not any(value.get("unresolved_key") == key for value in unresolved_rows)
            or original.get("evidence_ref") != expected_classification_ref
            or source_record.get("name") != source_name
            or source_record.get("source_page") != spec["printed_page"]
            or source_record.get("source_header_line") != spec["source_header_line"]
            or source_record.get("body_sha256") != spec["raw_body_sha256"]
            or body_witness.get("name") != source_name
            or body_witness.get("page") != spec["printed_page"]
            or body_witness.get("line") != spec["source_header_line"]
            or body_witness.get("body_sha256") != spec["raw_body_sha256"]
        ):
            _fail("source_eighth_provenance", f"{key} differs from its original pass/body/map evidence")

        prior_field = {
            "A": "source_unknown_resolution_evidence",
            "B": "source_fourth_resolution_evidence",
            "C": "source_fifth_resolution_evidence",
            "D": "source_fifth_resolution_evidence",
            "E": "source_sixth_resolution_evidence",
            "F": "source_seventh_resolution_evidence",
        }[section]
        prior_holds = [
            value
            for value in prior_records_by_field[prior_field]
            if value.get("unresolved_key") == key
            and value.get("subobligation_id") == subobligation_id
        ]
        if (
            len(prior_holds) != 1
            or prior_holds[0].get("disposition") != "SOURCE_HELD"
        ):
            _fail("source_eighth_prior_hold", f"{key} does not preserve its historical HOLD record")

        locator = dict(spec["markdown_locator"])
        locators = [
            _object(value, f"{key}.source_markdown_locators[{locator_index}]")
            for locator_index, value in enumerate(_array(row.get("source_markdown_locators"), f"{key}.source_markdown_locators"))
        ]
        if locators != [locator]:
            _fail("source_eighth_locator", f"{key} Markdown locator differs from reviewed body section")
        start, end = int(locator["line_start"]), int(locator["line_end"])
        if start < 1 or end < start or end > len(markdown_lines):
            _fail("source_eighth_locator", f"{key} Markdown span is out of bounds")
        span = b"".join(markdown_lines[start - 1 : end])
        if hashlib.sha256(span).hexdigest() != locator["span_sha256"]:
            _fail("source_eighth_markdown_span_hash", f"{key} source span hash differs")
        source_section = "".join(markdown_text_lines[start - 1 : end])
        if markdown_text_lines[start - 1].strip() != f"##### {source_name}":
            _fail("source_eighth_locator", f"{key} body span does not start at its exact heading")
        if any(phrase not in source_section for _, phrase in spec["source_phrases"]):
            _fail("source_eighth_source_text", f"{key} source body omits an exact source clause")

        expected_row_values = {
            "review_item_id": spec["review_item_id"],
            "unresolved_key": key,
            "source_exact_name": source_name,
            "source_category": category,
            "subobligation_id": subobligation_id,
            "disposition": "OWNER_DECIDED",
            "source_record_ref": expected_ref,
            "source_classification_pointer": classification_pointer,
            "source_unresolved_record_pointer": history_pointer,
            "current_map_pointer": map_pointer,
            "owner_section": section,
            "owner_section_heading": spec["owner_section_heading"],
            "resolution_authority": "ACCEPTED_PRODUCT_OWNER_DECISION",
            "resolution_basis": "ACCEPTED_OWNER_INTERPRETATION_NOT_LITERAL_SRD_WORDING",
            "source_grounding_status": spec["source_grounding_status"],
            "source_grounded_findings": list(spec["source_grounded_findings"]),
            "accepted_interpretation": spec["accepted_interpretation"],
            "material_qualifiers": list(spec["material_qualifiers"]),
            "retained_source_residual": spec["retained_source_residual"],
            "future_native_proof_status": "NOT_ESTABLISHED",
            "actual_native_proof_refs": [],
            "golden_witness": spec.get("golden_witness"),
        }
        for field, expected in expected_row_values.items():
            actual = row.get(field)
            if actual != expected:
                code = "source_eighth_qualifier" if field in {
                    "source_grounding_status", "source_grounded_findings", "accepted_interpretation",
                    "material_qualifiers", "retained_source_residual", "resolution_basis",
                } else "source_eighth_golden" if field == "golden_witness" else "source_eighth_binding"
                _fail(code, f"{key} field {field} differs from accepted owner/source evidence")

        if section == "E":
            golden = _object(row.get("golden_witness"), f"{key}.golden_witness")
            components = [
                _object(value, f"{key}.golden_witness.components[{component_index}]")
                for component_index, value in enumerate(_array(golden.get("components"), f"{key}.golden_witness.components"))
            ]
            selected = max(0, sum(int(value["amount"]) for value in components if value["damage_type"] == "Fire") - int(golden["fixed_d4_result"]))
            expected_damage = selected // 2 + sum(int(value["amount"]) for value in components if value["damage_type"] != "Fire")
            if (
                len(components) != 2
                or selected != golden.get("selected_type_subtotal_after_reduction")
                or selected // 2 != golden.get("selected_type_damage_after_defense")
                or expected_damage != golden.get("expected_total_damage")
                or expected_damage != 6
            ):
                _fail("source_eighth_golden", "Resistance chosen-type/no-spill witness must yield 6 damage")
        elif row.get("golden_witness") is not None:
            _fail("source_eighth_golden", f"{key} adds an unreviewed golden damage witness")
        resolved_keys.append(key)
        closed_ids.append(subobligation_id)

    if set(resolved_keys) != set(SOURCE_EIGHTH_ITEMS) or len(set(closed_ids)) != 6:
        _fail("source_eighth_census", "owner-decided source keys or subobligations are not unique")
    return {
        "source_resolution_records": rows,
        "source_owner_decided_keys": resolved_keys,
        "source_owner_decided_subobligation_ids": closed_ids,
        "source_owner_decided_subobligation_count": len(closed_ids),
        "source_markdown_sha256": SOURCE_MARKDOWN_SHA256,
    }


def _validate_source_unknown_classifications(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    """Validate the exact 82-key source/downstream split without losing provenance."""
    lanes = [
        _object(value, f"source_mapping_lanes[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        )
    ]
    lane0 = next(
        (lane for lane in lanes if lane.get("lane_id") == "source-pass-0-2"), None
    )
    if lane0 is None:
        _fail("source_unknown_classification", "source-pass 0-2 lane is missing")
    lane0_payload = _object(
        lane0.get("mapping_payload"), "source-pass-0-2.mapping_payload"
    )
    original_rows = [
        _object(value, f"source-pass-0-2.unresolved_key_index[{index}]")
        for index, value in enumerate(
            _array(
                lane0_payload.get("unresolved_key_index"),
                "source-pass-0-2.unresolved_key_index",
            )
        )
    ]
    classifications = [
        _object(value, f"source_unknown_classifications[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_unknown_classifications"),
                "source_unknown_classifications",
            )
        )
    ]
    original_by_key = {
        str(row.get("unresolved_key")): (index, row)
        for index, row in enumerate(original_rows)
    }
    classified_by_key: dict[str, dict[str, object]] = {}
    category_counts: Counter[str] = Counter()
    source_blocking_keys: list[str] = []
    downstream_only_keys: list[str] = []
    future_proof_subobligations: list[dict[str, object]] = []
    mixed_count = 0
    for classification in classifications:
        key = _string(
            classification.get("unresolved_key"),
            "source_unknown_classification.unresolved_key",
        )
        if key in classified_by_key:
            _fail("source_unknown_classification", f"duplicate classified key {key}")
        original_pair = original_by_key.get(key)
        if original_pair is None:
            _fail("source_unknown_classification", f"unknown classified key {key}")
        original_index, original = original_pair
        if (
            classification.get("source_exact_name") != original.get("source_exact_name")
            or classification.get("original_reason") != original.get("reason")
            or classification.get("evidence_ref") != original.get("evidence_ref")
            or classification.get("source_unresolved_record_pointer")
            != f"/source_mapping_lanes/0/mapping_payload/unresolved_key_index/{original_index}"
            or classification.get("original_status") != original.get("status")
            or classification.get("original_disposition") != original.get("disposition")
            or classification.get("original_status") != "NOT_ESTABLISHED"
            or classification.get("original_disposition")
            != "RECONCILE_EXACT_QUALIFIED_SOURCE_OR_OWNER; DO_NOT_GUESS"
        ):
            _fail(
                "source_unknown_classification_witness",
                f"{key} no longer preserves its original reason/evidence/status",
            )
        subobligations = [
            _object(value, f"{key}.subobligations[{index}]")
            for index, value in enumerate(
                _array(classification.get("subobligations"), f"{key}.subobligations")
            )
        ]
        subobligation_ids: set[str] = set()
        categories: set[str] = set()
        for subobligation in subobligations:
            subobligation_id = _string(
                subobligation.get("subobligation_id"), f"{key}.subobligation_id"
            )
            category = _string(subobligation.get("category"), f"{key}.category")
            if (
                category not in SOURCE_UNKNOWN_CATEGORIES
                or subobligation_id != f"{key}::{category}"
                or subobligation_id in subobligation_ids
                or category in categories
                or not isinstance(subobligation.get("description"), str)
                or not str(subobligation["description"]).strip()
                or subobligation.get("status") != "NOT_ESTABLISHED"
            ):
                _fail(
                    "source_unknown_subobligation",
                    f"{key} has an invalid or duplicate categorized subobligation",
                )
            expected_gate = (
                "SP00_SOURCE"
                if category in SOURCE_UNKNOWN_SOURCE_CATEGORIES
                else "FUTURE_PROOF"
            )
            if subobligation.get("gate_phase") != expected_gate:
                _fail(
                    "source_unknown_subobligation",
                    f"{key} assigns {category} to the wrong gate phase",
                )
            subobligation_ids.add(subobligation_id)
            categories.add(category)
            category_counts[category] += 1
            if category == "downstream_domain_consumer_admission_native_proof":
                future_proof_subobligations.append(
                    {
                        "unresolved_key": key,
                        "source_exact_name": classification["source_exact_name"],
                        **subobligation,
                    }
                )
        if not categories:
            _fail("source_unknown_classification", f"{key} has no subobligation")
        has_source_obligation = bool(categories & SOURCE_UNKNOWN_SOURCE_CATEGORIES)
        expected_status = (
            "MIXED_SOURCE_AND_FUTURE_PROOF"
            if has_source_obligation
            and "downstream_domain_consumer_admission_native_proof" in categories
            else "SOURCE_LEVEL_OPEN"
            if has_source_obligation
            else "DOWNSTREAM_PROOF_ONLY"
        )
        if (
            classification.get("classification_status") != expected_status
            or classification.get("source_ready_blocking") is not has_source_obligation
        ):
            _fail(
                "source_unknown_classification_gate",
                f"{key} has a classification/gate mismatch",
            )
        if has_source_obligation:
            source_blocking_keys.append(key)
        else:
            downstream_only_keys.append(key)
        if expected_status == "MIXED_SOURCE_AND_FUTURE_PROOF":
            mixed_count += 1
        classified_by_key[key] = classification

    if (
        len(original_rows) != 82
        or len(original_by_key) != 82
        or len(classifications) != 82
        or set(classified_by_key) != set(original_by_key)
        or len(source_blocking_keys) != 77
        or len(downstream_only_keys) != 5
        or mixed_count != 28
        or dict(category_counts) != SOURCE_UNKNOWN_EXPECTED_COUNTS
    ):
        _fail(
            "source_unknown_classification_census",
            "the 82-key classification/subobligation census differs",
        )
    contract = _object(
        manifest.get("source_unknown_classification_contract"),
        "source_unknown_classification_contract",
    )
    if (
        contract.get("status")
        != "ALL_82_EXACT_RECORDS_CLASSIFIED_WITH_SPLIT_SUBOBLIGATIONS"
        or contract.get("total_record_count") != 82
        or contract.get("source_blocking_key_count") != 77
        or contract.get("downstream_only_key_count") != 5
        or contract.get("mixed_source_and_downstream_key_count") != 28
        or contract.get("subobligation_counts_by_category")
        != SOURCE_UNKNOWN_EXPECTED_COUNTS
        or set(
            _strings(contract.get("source_level_categories"), "source_level_categories")
        )
        != SOURCE_UNKNOWN_SOURCE_CATEGORIES
        or contract.get("downstream_only_category")
        != "downstream_domain_consumer_admission_native_proof"
        or contract.get("original_reason_and_evidence_preserved") is not True
    ):
        _fail(
            "source_unknown_classification_contract",
            "the declared 82-key source/downstream split differs",
        )
    historical_source_blocking_keys = source_blocking_keys
    first12_resolution = _validate_source_unknown_resolution_evidence(
        manifest, classified_by_key
    )
    next12_resolution = _validate_source_next12_resolution_evidence(
        manifest, classified_by_key
    )
    third12_resolution = _validate_source_third12_resolution_evidence(
        manifest, classified_by_key
    )
    fourth_resolution = _validate_source_fourth_resolution_evidence(
        manifest, classified_by_key
    )
    fifth_resolution = _validate_source_fifth_resolution_evidence(
        manifest, classified_by_key
    )
    sixth_resolution = _validate_source_sixth_resolution_evidence(
        manifest, classified_by_key
    )
    seventh_resolution = _validate_source_seventh_resolution_evidence(
        manifest, classified_by_key
    )
    eighth_resolution = _validate_source_eighth_resolution_evidence(
        manifest, classified_by_key
    )
    prior_resolutions = (
        first12_resolution,
        next12_resolution,
        third12_resolution,
        fourth_resolution,
        fifth_resolution,
        sixth_resolution,
        seventh_resolution,
    )
    closed_subobligation_ids = set(
        first12_resolution["source_closed_subobligation_ids"]
    )
    closed_subobligation_ids.update(
        next12_resolution["source_closed_subobligation_ids"]
    )
    closed_subobligation_ids.update(
        third12_resolution["source_closed_subobligation_ids"]
    )
    closed_subobligation_ids.update(
        fourth_resolution["source_closed_subobligation_ids"]
    )
    closed_subobligation_ids.update(fifth_resolution["source_closed_subobligation_ids"])
    closed_subobligation_ids.update(sixth_resolution["source_closed_subobligation_ids"])
    closed_subobligation_ids.update(seventh_resolution["source_closed_subobligation_ids"])
    closed_subobligation_ids.update(
        eighth_resolution["source_owner_decided_subobligation_ids"]
    )
    source_blocking_keys = [
        key
        for key in historical_source_blocking_keys
        if any(
            subobligation["subobligation_id"] not in closed_subobligation_ids
            for subobligation in classified_by_key[key]["subobligations"]
            if subobligation["category"] in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        )
    ]
    active_source_blocker_entry_count = len(
        {classified_by_key[key]["source_exact_name"] for key in source_blocking_keys}
    )
    prior_closed_subobligation_ids = {
        str(subobligation_id)
        for resolution in prior_resolutions
        for subobligation_id in resolution["source_closed_subobligation_ids"]
    }
    prior_resolved_keys = {
        str(key)
        for resolution in prior_resolutions
        for key in resolution["source_resolved_keys"]
    }
    prior_held_keys = {
        str(key)
        for resolution in prior_resolutions
        for key in resolution["source_held_keys"]
    }
    prior_reviewed_records = [
        row
        for resolution in prior_resolutions
        for row in resolution["source_resolution_records"]
    ]
    prior_reviewed_keys = {
        str(row["unresolved_key"]) for row in prior_reviewed_records
    }
    prior_held_subobligation_count = sum(
        int(resolution["source_held_subobligation_count"])
        for resolution in prior_resolutions
    )
    prior_active_source_blocker_keys = [
        key
        for key in historical_source_blocking_keys
        if any(
            subobligation["subobligation_id"] not in prior_closed_subobligation_ids
            for subobligation in classified_by_key[key]["subobligations"]
            if subobligation["category"] in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        )
    ]
    current_open_source_subobligation_ids = {
        str(subobligation["subobligation_id"])
        for key in source_blocking_keys
        for subobligation in classified_by_key[key]["subobligations"]
        if subobligation["category"] in SOURCE_UNKNOWN_SOURCE_CATEGORIES
        and subobligation["subobligation_id"] not in closed_subobligation_ids
    }
    all_records = [
        *prior_reviewed_records,
        *eighth_resolution["source_resolution_records"],
    ]
    all_resolved_keys = prior_resolved_keys | set(
        eighth_resolution["source_owner_decided_keys"]
    )
    reviewed_keys = prior_reviewed_keys | set(
        eighth_resolution["source_owner_decided_keys"]
    )
    expected_eighth_contract = {
        "status": "PARTIAL_EIGHTH_ACCEPTED_OWNER_SET_SOURCE_ONLY",
        "selected_key_count": len(SOURCE_EIGHTH_ITEMS),
        "resolution_record_count": len(eighth_resolution["source_resolution_records"]),
        "selected_owner_decided_key_count": len(
            set(eighth_resolution["source_owner_decided_keys"])
        ),
        "selected_owner_decided_subobligation_count": len(
            set(eighth_resolution["source_owner_decided_subobligation_ids"])
        ),
        "prior_reviewed_key_count": len(prior_reviewed_keys),
        "prior_resolution_record_count": len(prior_reviewed_records),
        "prior_source_resolved_key_count": len(prior_resolved_keys),
        "prior_source_resolved_subobligation_count": len(
            prior_closed_subobligation_ids
        ),
        "prior_source_held_key_count": len(prior_held_keys),
        "prior_source_held_subobligation_count": prior_held_subobligation_count,
        "prior_active_source_blocker_count": len(prior_active_source_blocker_keys),
        "prior_active_source_blocker_entry_count": len(
            {
                classified_by_key[key]["source_exact_name"]
                for key in prior_active_source_blocker_keys
            }
        ),
        "cumulative_reviewed_key_count": len(reviewed_keys),
        "cumulative_resolution_record_count": len(all_records),
        "cumulative_source_resolved_key_count": len(all_resolved_keys),
        "cumulative_source_resolved_subobligation_count": len(
            closed_subobligation_ids
        ),
        "cumulative_source_held_key_count": len(source_blocking_keys),
        "cumulative_source_held_subobligation_count": len(
            current_open_source_subobligation_ids
        ),
        "original_record_count": len(classifications),
        "original_source_blocking_key_count": len(historical_source_blocking_keys),
        "downstream_only_key_count": len(downstream_only_keys),
        "active_source_blocker_count": len(source_blocking_keys),
        "active_source_blocker_entry_count": active_source_blocker_entry_count,
        "future_native_proof_status": "NOT_ESTABLISHED",
        "full_339_source_qualification_status": "NOT_ESTABLISHED",
        "production_claim": "NONE",
        "selected_original_classification_indexes": [
            int(SOURCE_EIGHTH_ITEMS[key]["classification_index"])
            for key in SOURCE_INTERPRETATION_OWNER["accepted_keys"]
        ],
    }
    resolution_contract = _object(
        manifest.get("source_eighth_resolution_contract"),
        "source_eighth_resolution_contract",
    )
    if (
        resolution_contract != expected_eighth_contract
        or len(source_blocking_keys) != active_source_blocker_entry_count
    ):
        _fail(
            "source_eighth_contract",
            "owner-decision cumulative counts differ from derived source-classification sets",
        )
    owner_decided_key_set = set(eighth_resolution["source_owner_decided_keys"])
    source_held_keys: list[str] = []
    seen_held_keys: set[str] = set()
    for resolution in prior_resolutions:
        for key in resolution["source_held_keys"]:
            key_string = str(key)
            if key_string in source_blocking_keys and key_string not in seen_held_keys:
                source_held_keys.append(key_string)
                seen_held_keys.add(key_string)
    if seen_held_keys != set(source_blocking_keys) or owner_decided_key_set & seen_held_keys:
        _fail(
            "source_eighth_hold_accounting",
            "active holds do not equal historical holds minus the accepted owner decisions",
        )
    source_resolved_keys = [
        str(key)
        for resolution in prior_resolutions
        for key in resolution["source_resolved_keys"]
    ] + [str(key) for key in eighth_resolution["source_owner_decided_keys"]]
    return {
        "total_record_count": 82,
        "source_blocking_key_count": len(source_blocking_keys),
        "source_blocking_keys": source_blocking_keys,
        "historical_source_blocking_key_count": len(historical_source_blocking_keys),
        "historical_source_blocking_keys": historical_source_blocking_keys,
        "source_resolved_subobligation_count": len(closed_subobligation_ids),
        "source_resolved_key_count": len(all_resolved_keys),
        "source_resolved_keys": source_resolved_keys,
        "source_owner_decided_keys": eighth_resolution["source_owner_decided_keys"],
        "source_owner_decided_subobligation_count": eighth_resolution[
            "source_owner_decided_subobligation_count"
        ],
        "source_held_subobligation_count": len(current_open_source_subobligation_ids),
        "source_held_keys": source_held_keys,
        "source_resolution_evidence": all_records,
        "source_owner_decision_evidence": eighth_resolution[
            "source_resolution_records"
        ],
        "source_reviewed_key_count": len(reviewed_keys),
        "source_markdown_sha256": first12_resolution["source_markdown_sha256"],
        "command_approach_source_text": first12_resolution[
            "command_approach_source_text"
        ],
        "downstream_only_key_count": len(downstream_only_keys),
        "downstream_only_keys": downstream_only_keys,
        "mixed_source_and_downstream_key_count": mixed_count,
        "future_proof_subobligation_count": len(future_proof_subobligations),
        "future_proof_subobligations": future_proof_subobligations,
        "subobligation_counts_by_category": dict(category_counts),
    }


R5_SOURCE_MODELING_RULINGS: dict[str, dict[str, object]] = {
    "Flesh to Stone": {
        "resolution_id": "r5.source_modeling.flesh_to_stone.initial_failure_count",
        "ruling": "Count the initial failed Constitution save as failure 1 in the three-failure progression; do not begin at zero or count it twice.",
        "ruling_qualifiers": [
            "The initial failed save is counted exactly once.",
            "Subsequent end-turn saves retain the source's nonconsecutive success/failure rules.",
            "This settles source/model interpretation only; native counter execution remains future proof.",
        ],
    },
    "Heroes’ Feast": {
        "resolution_id": "r5.source_modeling.heroes_feast.per_partaker_roll",
        "ruling": "Roll 2d10 independently for each qualifying partaker and reuse that partaker's result for both the maximum-HP increase and its matching healing.",
        "ruling_qualifiers": [
            "The roll is per qualifying partaker, not shared across the group.",
            "The same per-partaker result is reused for maximum HP and healing.",
            "This settles source/model interpretation only; native health proof remains future.",
        ],
    },
    "Instant Summons": {
        "resolution_id": "r5.source_modeling.instant_summons.activation_cost_and_binding",
        "ruling": "Both activation branches consume the gem and end the binding. If the object is held or carried, transport is prevented; that exception changes transport only and reveals the carrier/location.",
        "ruling_qualifiers": [
            "The held/carried branch is not a free activation.",
            "The carrier exception changes transport outcome only, not gem consumption or binding termination.",
            "This settles source/model interpretation only; native possession/transport proof remains future.",
        ],
    },
    "Move Earth": {
        "resolution_id": "r5.source_modeling.move_earth.interruption_and_attained_terrain",
        "ruling": "Interruption stops future work and preserves terrain changes already established. When target material is accepted, its exact attained shape is fictional adjudication; do not interpolate linearly or impose a no-effect-until-10-minutes rule.",
        "ruling_qualifiers": [
            "Established terrain is not rolled back by cast interruption.",
            "No linear interpolation or automatic zero effect before ten minutes is inferred.",
            "The accepted material/attained shape remains bounded fictional adjudication.",
        ],
    },
    "Mass Heal": {
        "resolution_id": "r5.source_modeling.mass_heal.positive_actual_healing_condition_removal",
        "ruling": "Remove listed conditions only when the target receives positive actual healing; allocation alone, a full-HP target, or blocked/zero healing does not trigger condition removal.",
        "ruling_qualifiers": [
            "Condition removal follows actual positive healing, not budget allocation.",
            "Full HP or blocked healing does not independently remove conditions.",
            "This settles source/model interpretation only; native health/condition proof remains future.",
        ],
    },
}


def _validate_source_modeling_r5(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    """Verify R5's five bounded rulings and retained Word of Recall residual."""
    evidence = _load_evidence(manifest)
    source_payload = _object(evidence.get("source-pass-6-9"), "source-pass-6-9")
    source_rows = _rows(source_payload, "rows", "source-pass-6-9")
    body_payload = _object(
        evidence.get("source-body-witnesses"), "source-body-witnesses"
    )
    inventory_payload = _object(evidence.get("spell-inventory"), "spell-inventory")
    inventory_by_name = _unique_name_index(
        _rows(inventory_payload, "spells", "spell-inventory"),
        "spell-inventory.spells",
    )
    mapping_lanes = [
        _object(value, f"source_mapping_lanes[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        )
    ]
    lane6 = next(
        (lane for lane in mapping_lanes if lane.get("lane_id") == "source-pass-6-9"),
        None,
    )
    if lane6 is None:
        _fail("source_modeling_r5", "source-pass 6-9 lane is missing")
    lane6_payload = _object(
        lane6.get("mapping_payload"), "source-pass-6-9.mapping_payload"
    )
    lane6_rows = {
        str(row.get("name")): row
        for row in _rows(lane6_payload, "entries", "source-pass-6-9")
    }
    resolutions = [
        _object(value, f"source_modeling_resolutions[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_modeling_resolutions"),
                "source_modeling_resolutions",
            )
        )
    ]
    resolutions_by_name: dict[str, dict[str, object]] = {}
    for resolution in resolutions:
        name = _string(
            resolution.get("source_exact_name"),
            "source_modeling_resolution.source_exact_name",
        )
        expected = R5_SOURCE_MODELING_RULINGS.get(name)
        if expected is None or name in resolutions_by_name:
            _fail(
                "source_modeling_r5", f"unexpected or duplicate resolution for {name}"
            )
        source_ref = _object(
            resolution.get("source_record_ref"), f"{name}.source_record_ref"
        )
        record_index = source_ref.get("record_index")
        if type(record_index) is not int or not 0 <= record_index < len(source_rows):
            _fail(
                "source_modeling_r5_witness", f"{name} has an invalid source row index"
            )
        source_row = source_rows[record_index]
        raw_name, exact_name, _alias_status = _canonical_source_name(
            source_row, "source-pass-6-9"
        )
        inventory_row = inventory_by_name.get(exact_name)
        body_ref = _object(
            source_ref.get("body_witness_ref"), f"{name}.body_witness_ref"
        )
        qualification_ref = _object(
            source_ref.get("qualification_ref"), f"{name}.qualification_ref"
        )
        body_pointer = _string(
            body_ref.get("json_pointer"), f"{name}.body_witness_ref.pointer"
        )
        qualification_pointer = _string(
            qualification_ref.get("json_pointer"), f"{name}.qualification_ref.pointer"
        )
        body_row = _object(
            _resolve_json_pointer(
                body_payload, body_pointer, f"{name}.body_witness_ref"
            ),
            f"{name}.body_witness",
        )
        expected_qualifications = _row_qualifications(source_row, name)
        raw_body_sha256 = source_row.get("body_sha256")
        hash_basis = source_row.get("body_hash_basis", source_row.get("hash_basis"))
        expected_ref = {
            "artifact_id": "source-pass-6-9",
            "record_index": record_index,
            "raw_record_name": raw_name,
            "source_exact_name": exact_name,
            "source_asset_id": "srd52_en",
            "edition": "SRD_5_2_1",
            "printed_page": source_row.get("source_page"),
            "source_header_line": source_row.get("source_header_line"),
            "source_heading": exact_name,
            "raw_body_sha256": raw_body_sha256,
            "raw_hash_basis": hash_basis,
            "body_witness_ref": {
                "artifact_id": "source-body-witnesses",
                "json_pointer": body_pointer,
            },
            "qualification_ref": {
                "artifact_id": "source-pass-6-9",
                "json_pointer": f"/rows/{record_index}/qualifications",
            },
            "source_qualifications": expected_qualifications,
            "source_review": source_row.get("review"),
            "source_confidence": (
                inventory_row.get("confidence") if inventory_row is not None else None
            ),
            "inventory_qualification": source_row.get("inventory_qualification"),
            "inventory_qualifications": source_row.get("inventory_qualifications"),
        }
        if (
            exact_name != name
            or inventory_row is None
            or body_row.get("name") != exact_name
            or body_row.get("page") != source_row.get("source_page")
            or body_row.get("line") != source_row.get("source_header_line")
            or body_row.get("body_sha256") != raw_body_sha256
            or source_ref != expected_ref
            or qualification_pointer != f"/rows/{record_index}/qualifications"
            or _resolve_json_pointer(
                source_payload, qualification_pointer, f"{name}.qualifications"
            )
            != expected_qualifications
            or resolution.get("resolution_id") != expected["resolution_id"]
            or resolution.get("ruling") != expected["ruling"]
            or resolution.get("ruling_qualifiers") != expected["ruling_qualifiers"]
            or resolution.get("ruling_basis")
            != "USER_SUPPLIED_ACCEPTED_SOURCE_SIX_SENIOR_R5_REVIEW"
            or resolution.get("source_modeling_status")
            != "SETTLED_FOR_SOURCE_CLASSIFICATION"
            or resolution.get("native_consumer_status") != "NOT_ESTABLISHED"
            or resolution.get("actual_native_proof_refs") != []
        ):
            _fail(
                "source_modeling_r5_witness",
                f"{name} ruling or exact source/page/qualification witness differs",
            )
        mapping_row = lane6_rows.get(name)
        if (
            mapping_row is None
            or mapping_row.get("r5_source_modeling_resolution_id")
            != expected["resolution_id"]
        ):
            _fail(
                "source_modeling_r5_mapping",
                f"{name} resolution is not bound to its source-map entry",
            )
        resolutions_by_name[name] = resolution

    expected_names = set(R5_SOURCE_MODELING_RULINGS)
    if len(resolutions) != 5 or set(resolutions_by_name) != expected_names:
        _fail("source_modeling_r5_census", "the five accepted R5 rulings differ")

    residuals = [
        _object(value, f"source_modeling_residuals[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_modeling_residuals"), "source_modeling_residuals"
            )
        )
    ]
    expected_word_ref = {
        "artifact_id": "source-pass-6-9",
        "record_index": 30,
        "raw_record_name": "Word of Recall",
        "source_exact_name": "Word of Recall",
        "source_asset_id": "srd52_en",
        "edition": "SRD_5_2_1",
        "printed_page": 175,
        "source_header_line": 15635,
        "source_heading": "Word of Recall",
        "raw_body_sha256": "7c7e1a030c386301bd8de28292fdef0172c892816517fbc631e67a21439303d6",
        "raw_hash_basis": source_rows[30].get(
            "body_hash_basis", source_rows[30].get("hash_basis")
        ),
        "body_witness_ref": {
            "artifact_id": "source-body-witnesses",
            "json_pointer": "/rows/337",
        },
        "qualification_ref": {
            "artifact_id": "source-pass-6-9",
            "json_pointer": "/rows/30/qualifications",
        },
        "source_qualifications": _row_qualifications(source_rows[30], "Word of Recall"),
        "source_review": source_rows[30].get("review"),
        "source_confidence": inventory_by_name["Word of Recall"].get("confidence"),
        "inventory_qualification": source_rows[30].get("inventory_qualification"),
        "inventory_qualifications": source_rows[30].get("inventory_qualifications"),
    }
    word_body = _object(
        _resolve_json_pointer(
            body_payload, "/rows/337", "Word of Recall.body_witness_ref"
        ),
        "Word of Recall.body_witness",
    )
    word_qualifications = _resolve_json_pointer(
        source_payload, "/rows/30/qualifications", "Word of Recall.qualifications"
    )
    if len(residuals) != 1:
        _fail(
            "source_modeling_r5_residual",
            "exactly one Word of Recall residual is required",
        )
    residual = residuals[0]
    word_entry = lane6_rows.get("Word of Recall")
    if (
        residual.get("residual_id")
        != "r5.source_modeling.word_of_recall.sanctuary_redesignation_survival"
        or residual.get("source_exact_name") != "Word of Recall"
        or residual.get("source_record_ref") != expected_word_ref
        or word_body.get("name") != "Word of Recall"
        or word_body.get("page") != 175
        or word_body.get("line") != 15635
        or word_body.get("body_sha256") != expected_word_ref["raw_body_sha256"]
        or word_qualifications != expected_word_ref["source_qualifications"]
        or not isinstance(residual.get("residual"), str)
        or residual.get("residual")
        != "Sanctuary redesignation/replacement and survival interactions remain source ambiguity. A bounded content-owner policy/reconciliation is required before source-ready; do not infer implicit latest-wins or a cap."
        or residual.get("owner_action")
        != "BOUNDED_CONTENT_OWNER_POLICY_OR_SOURCE_RECONCILIATION_REQUIRED"
        or residual.get("prohibited_inferences")
        != ["IMPLICIT_LATEST_WINS", "AUTOMATIC_CAP"]
        or residual.get("status") != "NOT_ESTABLISHED"
        or word_entry is None
        or word_entry.get("r5_source_modeling_residual_id")
        != residual.get("residual_id")
        or lane6_payload.get("source_modeling_resolutions")
        != [
            R5_SOURCE_MODELING_RULINGS[name]["resolution_id"]
            for name in R5_SOURCE_MODELING_RULINGS
        ]
    ):
        _fail(
            "source_modeling_r5_residual",
            "Word of Recall remains unbounded or loses its source/mapping reference",
        )
    lane_current_residuals = _array(
        lane6_payload.get("source_modeling_residuals"),
        "source-pass-6-9.source_modeling_residuals",
    )
    if lane_current_residuals != residuals:
        _fail(
            "source_modeling_r5_residual",
            "lane and top-level Word of Recall residuals disagree",
        )
    lane_reported_residuals = _array(
        lane6_payload.get("lane_reported_source_modeling_residuals"),
        "source-pass-6-9.lane_reported_source_modeling_residuals",
    )
    receipt_summary = _object(
        lane6.get("receipt_summary"), "source-pass-6-9.receipt_summary"
    )
    if (
        len(lane_reported_residuals) != 6
        or receipt_summary.get("lane_reported_source_modeling_residuals")
        != lane_reported_residuals
        or receipt_summary.get("r5_resolved_source_modeling_names")
        != [
            "Flesh to Stone",
            "Heroes’ Feast",
            "Instant Summons",
            "Mass Heal",
            "Move Earth",
        ]
        or receipt_summary.get("r5_unresolved_source_modeling_names")
        != ["Word of Recall"]
        or receipt_summary.get("source_modeling_residuals") != residuals
    ):
        _fail(
            "source_modeling_r5_lane_receipt",
            "lane receipt does not preserve the six historical residuals and R5 split",
        )
    return {
        "resolutions": resolutions,
        "residuals": residuals,
        "resolved_names": sorted(expected_names),
        "unresolved_names": ["Word of Recall"],
    }


def _derive_roster_from_evidence(
    manifest: Mapping[str, object], evidence: Mapping[str, object]
) -> tuple[dict[str, object], ...]:
    inventory = _object(evidence.get("spell-inventory"), "spell-inventory")
    inventory_rows = _rows(inventory, "spells", "spell-inventory")
    inventory_by_name = _unique_name_index(inventory_rows, "spell-inventory.spells")
    pass_ids = ("source-pass-0-2", "source-pass-3-5", "source-pass-6-9")
    source_rows: list[tuple[str, dict[str, object]]] = []
    source_record_indices: dict[str, int] = {}
    for artifact_id in pass_ids:
        pass_payload = _object(evidence.get(artifact_id), artifact_id)
        pass_rows = _rows(pass_payload, "rows", artifact_id)
        if len(pass_rows) != PASS_RECORD_COUNTS[artifact_id]:
            _fail(
                "source_pass_count",
                f"{artifact_id} row count differs from its pinned slice",
            )
        for record_index, row in enumerate(pass_rows):
            _raw_name, exact_name, _alias_status = _canonical_source_name(
                row, artifact_id
            )
            source_record_indices[exact_name] = record_index
            source_rows.append((artifact_id, row))
    source_by_name: dict[str, tuple[str, dict[str, object]]] = {}
    for artifact_id, row in source_rows:
        _raw_name, exact_name, _alias_status = _canonical_source_name(row, artifact_id)
        if exact_name in source_by_name:
            _fail(
                "duplicate_source_name",
                f"source passes contain duplicate canonical name {exact_name}",
            )
        source_by_name[exact_name] = (artifact_id, row)
    if set(source_by_name) != set(inventory_by_name) or len(source_rows) != 339:
        _fail(
            "roster_name_mismatch",
            "source-pass names do not equal the 339-entry inventory",
        )
    _validate_source_name_aliases(manifest, source_rows, inventory_by_name)

    body_payload = _object(
        evidence.get("source-body-witnesses"), "source-body-witnesses"
    )
    body_rows = _unique_name_index(
        _rows(body_payload, "rows", "source-body-witnesses"),
        "source-body-witnesses.rows",
    )
    matrix_payload = _object(evidence.get("requirement-matrix"), "requirement-matrix")
    matrix_rows = _unique_name_index(
        _rows(matrix_payload, "spells", "requirement-matrix"),
        "requirement-matrix.spells",
    )
    if set(body_rows) != set(inventory_by_name) or set(matrix_rows) != set(
        inventory_by_name
    ):
        _fail(
            "roster_name_mismatch",
            "body or requirement-matrix names do not equal inventory",
        )

    asset_rows = _array(manifest.get("source_assets"), "source_assets")
    english_assets = [
        _object(row, f"source_assets[{index}]")
        for index, row in enumerate(asset_rows)
        if isinstance(row, dict) and row.get("asset_id") == "srd52_en"
    ]
    if len(english_assets) != 1:
        _fail(
            "missing_primary_asset",
            "the roster needs one English SRD5.2.1 source asset",
        )
    english_asset = english_assets[0]
    asset_hash = _string(english_asset.get("sha256"), "source_assets.srd52_en.sha256")
    artifact_hashes = {
        str(row["artifact_id"]): str(row["sha256"])
        for row in _array(manifest.get("evidence_artifacts"), "evidence_artifacts")
        if isinstance(row, dict)
    }
    result: list[dict[str, object]] = []

    for artifact_id, source_row in source_rows:
        source_record_name, name, alias_status = _canonical_source_name(
            source_row, artifact_id
        )
        inventory_row = inventory_by_name[name]
        body_row = body_rows[name]
        matrix_row = matrix_rows[name]
        level = source_row.get("level")
        source_page = source_row.get("source_page")
        header_line = source_row.get("source_header_line")
        body_hash = _string(source_row.get("body_sha256"), f"{name}.body_sha256")
        hash_basis = source_row.get("body_hash_basis", source_row.get("hash_basis"))
        if (
            type(level) is not int
            or type(source_page) is not int
            or type(header_line) is not int
        ):
            _fail(
                "invalid_source_locator", f"{name} lacks level/page/header-line values"
            )
        if source_page != inventory_row.get(
            "source_page"
        ) or level != inventory_row.get("level"):
            _fail(
                "source_inventory_mismatch",
                f"{name} level or page differs from inventory",
            )
        if (
            body_hash != body_row.get("body_sha256")
            or body_hash != matrix_row.get("extracted_body_sha256")
            or level != body_row.get("level")
            or level != matrix_row.get("level")
            or source_page != body_row.get("page")
            or source_page != matrix_row.get("source_page")
            or header_line != body_row.get("line")
        ):
            _fail("raw_witness_mismatch", f"{name} source/body/matrix witness differs")
        if not _reviewed_full_body(source_row):
            _fail(
                "body_review_missing", f"{name} has no complete source-pass body review"
            )
        if not isinstance(hash_basis, str) or not hash_basis:
            _fail("raw_hash_basis_missing", f"{name} has no historical raw-hash basis")

        mode_summaries = _row_modes(source_row, name)
        support_summaries = _row_support(source_row, name)
        research_dependencies = _row_research_dependencies(source_row, name)

        evidence_ref = {
            "artifact_id": artifact_id,
            "artifact_path": EVIDENCE_PATHS[artifact_id],
            "artifact_sha256": artifact_hashes[artifact_id],
            "record_index": source_record_indices[name],
            "exact_name": name,
            "raw_record_name": source_record_name,
            "raw_body_sha256": body_hash,
            "raw_hash_basis": hash_basis,
            "source_page": source_page,
            "source_header_line": header_line,
            "role": "INDEPENDENT_SOURCE_REQUIREMENT_SUMMARY_NOT_MACHINE_PROOF",
        }
        result.append(
            {
                "name": name,
                "source_record_name": source_record_name,
                "source_name_alias_status": alias_status,
                "level": level,
                "source_asset_id": "srd52_en",
                "source_asset_sha256": asset_hash,
                "historical_source_locator": {
                    "source_page": source_page,
                    "source_header_line": header_line,
                },
                "raw_extraction_witness": {
                    "sha256": body_hash,
                    "hash_basis": hash_basis,
                    "role": "HISTORICAL_RAW_EXTRACTION_ONLY",
                },
                "source_requirement_keys": [],
                "source_common_requirement_keys": [],
                "source_conditional_branch_keys": [],
                "source_shared_common_requirement_refs": [],
                "source_mode_keys": [],
                "source_support_obligation_keys": [],
                "source_support_domain_obligation_keys": [],
                "source_control_transition_keys": [],
                "source_target_form_keys": [],
                "source_unknowns": [],
                "source_requirement_mappings": [],
                "source_support_mappings": [],
                "source_requirement_summaries": mode_summaries,
                "source_support_obligation_summaries": support_summaries,
                "research_dependency_labels": research_dependencies,
                "source_mode_mapping_ref": None,
                "source_mode_mapping_status": "NOT_ESTABLISHED",
                "support_domain_mapping_status": "NOT_ESTABLISHED",
                "consumer_dependency_edges": [],
                "consumer_dependency_status": "NOT_ESTABLISHED",
                "source_qualifications": _row_qualifications(source_row, name),
                "source_pass_row_ref": dict(evidence_ref),
                "source_review_context": {
                    key: source_row[key]
                    for key in (
                        "review",
                        "full_body_reviewed",
                        "read_evidence",
                        "review_disposition",
                        "implementation_claim",
                        "rule_source_reconstruction_status",
                        "support_status",
                        "inventory_qualification",
                        "inventory_qualifications",
                        "candidate_routes",
                        "flags",
                        "source_confidence",
                    )
                    if key in source_row
                },
                "source_status": "CENSUS_ONLY",
            }
        )
    if len(result) != 339:
        _fail(
            "roster_count_mismatch", "derived source roster is not exactly 339 entries"
        )
    source_mapping_index = _validate_source_mapping_lanes(
        manifest, tuple(result), evidence
    )
    for row in result:
        name = str(row["name"])
        mapping_info = source_mapping_index.get(name)
        if mapping_info is None:
            _fail("source_mapping_orphan", f"{name} has no explicit source map record")
        mapping = _object(mapping_info.get("source_mapping"), f"{name}.source_mapping")
        lane_id = str(mapping_info["lane_id"])
        if lane_id != "existing-summary-decompositions":
            pass_ref = _object(
                row["source_pass_row_ref"], f"{name}.source_pass_row_ref"
            )
            closure_evidence = {
                "artifact_id": pass_ref["artifact_id"],
                "artifact_path": pass_ref["artifact_path"],
                "artifact_sha256": pass_ref["artifact_sha256"],
                "exact_name": name,
                "record_index": pass_ref["record_index"],
                "raw_body_sha256": pass_ref["raw_body_sha256"],
                "source_page": pass_ref["source_page"],
                "source_header_line": pass_ref["source_header_line"],
                "source_mapping_lane": lane_id,
                "mapping_payload_sha256": mapping_info["mapping_payload_sha256"],
                "role": "CANDIDATE_SOURCE_MAP_RECORD_BINDING_NOT_CLOSURE_PROOF",
            }
            requirement_keys = _strings(
                mapping_info["source_requirement_keys"],
                f"{name}.source_requirement_keys",
            )
            common_requirement_keys = _strings(
                mapping_info["source_common_requirement_keys"],
                f"{name}.source_common_requirement_keys",
            )
            conditional_branch_keys = _strings(
                mapping_info["source_conditional_branch_keys"],
                f"{name}.source_conditional_branch_keys",
            )
            mode_keys = _strings(
                mapping_info["source_mode_keys"], f"{name}.source_mode_keys"
            )
            support_keys = _strings(
                mapping_info["source_support_domain_obligation_keys"],
                f"{name}.source_support_domain_obligation_keys",
            )
            row["source_requirement_keys"] = requirement_keys
            row["source_common_requirement_keys"] = common_requirement_keys
            row["source_conditional_branch_keys"] = conditional_branch_keys
            row["source_shared_common_requirement_refs"] = _strings(
                mapping_info["source_shared_common_requirement_refs"],
                f"{name}.source_shared_common_requirement_refs",
            )
            row["source_mode_keys"] = mode_keys
            row["source_support_domain_obligation_keys"] = support_keys
            row["source_control_transition_keys"] = list(
                mapping_info["source_control_transition_keys"]
            )
            row["source_target_form_keys"] = list(
                mapping_info["source_target_form_keys"]
            )
            row["source_requirement_mappings"] = [
                {
                    "key": key,
                    "source_mapping_lane": lane_id,
                    "closure_evidence": dict(closure_evidence),
                }
                for key in requirement_keys
            ]
            row["source_support_mappings"] = [
                {
                    "key": key,
                    "source_mapping_lane": lane_id,
                    "support_domain_mapping_status": "OBLIGATION_ONLY_NO_DOMAIN_OR_CONSUMER_CENSUS",
                    "closure_evidence": dict(closure_evidence),
                }
                for key in support_keys
            ]
            row["source_unknowns"] = list(mapping_info["unresolved_source_keys"])
            row["source_mode_mapping_ref"] = {
                "lane_id": lane_id,
                "map_artifact_sha256": mapping_info["map_artifact_sha256"],
                "mapping_payload_sha256": mapping_info["mapping_payload_sha256"],
                "entry_name": name,
            }
            row["source_mode_mapping_status"] = "EXPLICIT_SOURCE_MAP_PENDING_REVIEW"
            row["support_domain_mapping_status"] = (
                "EXPLICIT_SOURCE_OBLIGATIONS_NOT_NATIVE_CLOSURE"
                if support_keys
                else "NOT_ESTABLISHED"
            )
            continue
        source_mapping_ref = _object(
            mapping.get("source_record_ref"), f"{name}.source_record_ref"
        )
        source_locator = {
            "asset_id": source_mapping_ref["asset_id"],
            "edition": source_mapping_ref["edition"],
            "printed_page": source_mapping_ref["source_page"],
            "source_header_line": source_mapping_ref["source_header_line"],
            "heading": source_mapping_ref["source_heading"],
        }
        closure_evidence = {
            **_object(row["source_pass_row_ref"], f"{name}.source_pass_row_ref"),
            "summary_field": source_mapping_ref["summary_field"],
            "summary_item_index": source_mapping_ref["summary_item_index"],
            "source_locator": source_locator,
            "qualification_boundary": source_mapping_ref["qualification_boundary"],
            "role": "EXPLICIT_SOURCE_SUMMARY_DECOMPOSITION_ONLY_NOT_MACHINE_PROOF",
        }
        mode_keys: list[str] = []
        requirement_keys: list[str] = []
        requirement_mappings: list[dict[str, object]] = []
        for mode_value in _array(mapping.get("modes"), f"{name}.modes"):
            mode = _object(mode_value, f"{name}.mode")
            mode_key = _string(mode.get("mode_key"), f"{name}.mode_key")
            mode_keys.append(mode_key)
            for requirement_value in _array(
                mode.get("requirements"), f"{name}.{mode_key}.requirements"
            ):
                requirement = _object(
                    requirement_value, f"{name}.{mode_key}.requirement"
                )
                requirement_key = _string(
                    requirement.get("requirement_key"), f"{name}.requirement_key"
                )
                requirement_keys.append(requirement_key)
                requirement_mappings.append(
                    {
                        "key": requirement_key,
                        "mode_key": mode_key,
                        "branch_key": requirement["branch_key"],
                        "independent_statement": requirement["independent_statement"],
                        "summary_item_index": requirement["summary_item_index"],
                        "source_locator": dict(source_locator),
                        "closure_evidence": dict(closure_evidence),
                    }
                )
        for transition_value in _array(
            mapping.get("control_transitions"), f"{name}.control_transitions"
        ):
            transition = _object(transition_value, f"{name}.control_transition")
            transition_key = _string(
                transition.get("transition_key"), f"{name}.transition_key"
            )
            for requirement_value in _array(
                transition.get("requirements"), f"{name}.{transition_key}.requirements"
            ):
                requirement = _object(
                    requirement_value, f"{name}.{transition_key}.requirement"
                )
                requirement_key = _string(
                    requirement.get("requirement_key"), f"{name}.requirement_key"
                )
                requirement_keys.append(requirement_key)
                requirement_mappings.append(
                    {
                        "key": requirement_key,
                        "control_transition_key": transition_key,
                        "branch_key": requirement["branch_key"],
                        "independent_statement": requirement["independent_statement"],
                        "summary_item_index": requirement["summary_item_index"],
                        "source_locator": dict(source_locator),
                        "closure_evidence": dict(closure_evidence),
                    }
                )
        row["source_mode_keys"] = mode_keys
        row["source_requirement_keys"] = requirement_keys
        row["source_common_requirement_keys"] = list(
            mapping_info["source_common_requirement_keys"]
        )
        row["source_conditional_branch_keys"] = list(
            mapping_info["source_conditional_branch_keys"]
        )
        row["source_shared_common_requirement_refs"] = list(
            mapping_info["source_shared_common_requirement_refs"]
        )
        row["source_control_transition_keys"] = list(
            mapping_info["source_control_transition_keys"]
        )
        row["source_requirement_mappings"] = requirement_mappings
        row["source_mode_mapping_ref"] = dict(source_mapping_ref)
        row["source_mode_mapping_status"] = "EXPLICIT_SOURCE_MAPPING_PARTIAL"
    return tuple(result)


def derive_source_requirement_roster(
    manifest: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    """Build the 339-entry census; key only explicitly mapped source requirements."""
    reviewed = _validate_reviewed_manifest(manifest)
    _validate_manifest_schema(reviewed)
    evidence = _load_evidence(reviewed)
    return _derive_roster_from_evidence(reviewed, evidence)


def _validate_source_assets(
    manifest: Mapping[str, object], source_assets: Mapping[str, bytes]
) -> list[str]:
    declarations = [
        _object(value, f"source_assets[{index}]")
        for index, value in enumerate(
            _array(manifest.get("source_assets"), "source_assets")
        )
    ]
    assets_by_id: dict[str, dict[str, object]] = {}
    uris: set[str] = set()
    for index, asset in enumerate(declarations):
        asset_id = _string(asset.get("asset_id"), f"source_assets[{index}].asset_id")
        if asset_id in assets_by_id:
            _fail("duplicate_source_asset", f"duplicate source asset {asset_id}")
        language = _string(asset.get("language"), f"{asset_id}.language")
        if EXPECTED_ASSET_LANGUAGES.get(asset_id) != language:
            _fail("source_asset_language", f"{asset_id} has the wrong language")
        uri = _string(asset.get("uri"), f"{asset_id}.uri")
        parsed = urlparse(uri)
        if (
            parsed.scheme != "https"
            or parsed.hostname != "media.dndbeyond.com"
            or not parsed.path.startswith("/compendium-images/srd/5.2/")
        ):
            _fail(
                "source_asset_uri",
                f"{asset_id} is not an official D&D Beyond SRD asset URI",
            )
        if uri in uris:
            _fail("duplicate_source_asset_uri", f"source asset URI is reused: {uri}")
        uris.add(uri)
        if asset.get("edition") != "SRD_5_2_1" or asset.get("license") != "CC-BY-4.0":
            _fail(
                "source_asset_qualification",
                f"{asset_id} is not qualified as SRD5.2.1 CC-BY-4.0",
            )
        if (
            asset.get("attribution") != ATTRIBUTION
            or manifest.get("required_attribution") != ATTRIBUTION
        ):
            _fail(
                "source_attribution",
                f"{asset_id} attribution differs from the licensed SRD notice",
            )
        assets_by_id[asset_id] = asset
    if set(assets_by_id) != set(EXPECTED_ASSET_LANGUAGES):
        _fail(
            "source_asset_set",
            "the English and four official localized SRD assets are required",
        )
    if set(source_assets) != uris:
        _fail(
            "source_asset_bytes_missing",
            "source_assets bytes must match the exact declared URI set",
        )
    verified: list[str] = []
    for asset in declarations:
        uri = str(asset["uri"])
        data = source_assets[uri]
        if not isinstance(data, bytes):
            _fail("source_asset_bytes_invalid", f"asset bytes for {uri} are not bytes")
        expected_hash = str(asset["sha256"])
        if hashlib.sha256(data).hexdigest() != expected_hash:
            _fail(
                "source_asset_digest",
                f"asset bytes do not match the declared SHA-256: {uri}",
            )
        verified.append(str(asset["asset_id"]))
    return sorted(verified)


def _validate_corroborating_sources(manifest: Mapping[str, object]) -> None:
    sources = [
        _object(value, f"corroborating_sources[{index}]")
        for index, value in enumerate(
            _array(manifest.get("corroborating_sources"), "corroborating_sources")
        )
    ]
    by_id = {str(source.get("source_id")): source for source in sources}
    if len(by_id) != len(sources) or set(by_id) != {
        "ddb_2024_basic_rules_telekinesis",
        "ddb_2014_legacy_telekinesis",
    }:
        _fail(
            "corroborating_source_set",
            "current corroboration and excluded legacy source must be distinct",
        )
    current = by_id["ddb_2024_basic_rules_telekinesis"]
    if (
        current.get("uri")
        != "https://www.dndbeyond.com/sources/dnd/br-2024/spell-descriptions#Telekinesis"
        or current.get("edition") != "DND_2024_BASIC_RULES"
        or current.get("role") != "OFFICIAL_CURRENT_CORROBORATION_ONLY"
        or current.get("license_status") != "CC_BY_NOT_ASSERTED_FOR_THIS_SOURCE"
        or current.get("text_imported") is not False
        or current.get("runtime_dependency") is not False
    ):
        _fail(
            "corroborating_source_role",
            "the current Basic Rules page is corroboration only",
        )
    legacy = by_id["ddb_2014_legacy_telekinesis"]
    if (
        legacy.get("uri") != "https://www.dndbeyond.com/spells/2273-telekinesis"
        or legacy.get("edition") != "DND_2014_LEGACY"
        or legacy.get("role") != "EXCLUDED_LEGACY_SOURCE"
        or legacy.get("license_status") != "NOT_USED"
        or legacy.get("text_imported") is not False
        or legacy.get("runtime_dependency") is not False
    ):
        _fail(
            "legacy_source_included",
            "2014 legacy Telekinesis is not an eligible current source",
        )


def _validate_reconstruction_witnesses(
    manifest: Mapping[str, object], roster: tuple[Mapping[str, object], ...]
) -> None:
    rows = [
        _object(value, f"source_reconstruction_witnesses[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("source_reconstruction_witnesses"),
                "source_reconstruction_witnesses",
            )
        )
    ]
    by_id = {str(row.get("witness_id")): row for row in rows}
    if len(by_id) != len(rows) or set(by_id) != set(EXPECTED_WITNESSES):
        _fail(
            "reconstruction_witness_set",
            "required source-layout reconstruction witnesses differ",
        )
    roster_by_name = {str(row["name"]): row for row in roster}
    for witness_id, expectation in EXPECTED_WITNESSES.items():
        witness = by_id[witness_id]
        for key in (
            "owner_spell",
            "printed_pages",
            "accepted_segments",
            "excluded_segments",
            "reconstruction_obligation_ids",
        ):
            if witness.get(key) != expectation[key]:
                _fail(
                    "source_scope_witness",
                    f"{witness_id} {key} differs from the reconstructed source scope",
                )
        if witness.get("source_reconstruction_status") != expectation["status"]:
            _fail("source_scope_witness", f"{witness_id} is not source-qualified")
        if witness.get("machine_support") != "NOT_ESTABLISHED":
            _fail("source_support_overclaim", f"{witness_id} claims machine support")
        if witness.get("primary_asset_id") != "srd52_en":
            _fail(
                "source_scope_witness",
                f"{witness_id} is not bound to the English licensed source",
            )
        record = _object(witness.get("source_record"), f"{witness_id}.source_record")
        if record.get("artifact_id") != expectation["artifact_id"]:
            _fail(
                "source_record_mismatch",
                f"{witness_id} refers to the wrong source-pass artifact",
            )
        owner = str(expectation["owner_spell"])
        roster_row = roster_by_name.get(owner)
        if roster_row is None:
            _fail(
                "source_record_mismatch",
                f"{witness_id} owner is outside the SRD roster",
            )
        if record.get("exact_name") != owner or record.get(
            "raw_body_sha256"
        ) != _object(
            roster_row["raw_extraction_witness"], f"{owner}.raw_extraction_witness"
        ).get("sha256"):
            _fail(
                "source_record_mismatch",
                f"{witness_id} raw extraction witness does not bind its owner",
            )
        locators = [
            _object(value, f"{witness_id}.source_locators[{index}]")
            for index, value in enumerate(
                _array(witness.get("source_locators"), f"{witness_id}.source_locators")
            )
        ]
        locator_identities: list[tuple[str, int, str]] = []
        for locator in locators:
            if locator.get("asset_id") not in EXPECTED_ASSET_LANGUAGES:
                _fail(
                    "source_locator_asset", f"{witness_id} refers to an unknown asset"
                )
            if (
                locator.get("printed_page") not in witness.get("printed_pages", [])
                and witness_id != "telekinesis-owner"
            ):
                _fail(
                    "source_locator_page",
                    f"{witness_id} locator is outside its printed page witness",
                )
            locator_identities.append(
                (
                    str(locator.get("asset_id")),
                    int(locator.get("printed_page", -1)),
                    str(locator.get("heading")),
                )
            )
        if locator_identities != expectation["source_locators"]:
            _fail(
                "source_locator_mismatch",
                f"{witness_id} source page/span locators differ",
            )

    telekinesis = by_id["telekinesis-owner"]
    expected_translation_pages = list(TELEKINESIS_TRANSLATION_LOCATORS)
    actual_translation_pages = [
        (
            str(_object(locator, "telekinesis.translation_locator").get("asset_id")),
            int(
                _object(locator, "telekinesis.translation_locator").get(
                    "printed_page", -1
                )
            ),
            str(_object(locator, "telekinesis.translation_locator").get("heading")),
        )
        for locator in _array(
            telekinesis.get("localized_translation_locators"),
            "telekinesis.localized_translation_locators",
        )
    ]
    if actual_translation_pages != list(expected_translation_pages):
        _fail(
            "telekinesis_translation_scope",
            "localized licensed source page witnesses differ",
        )
    if telekinesis.get("localized_translation_asset_ids") != [
        asset_id for asset_id, _page, _heading in TELEKINESIS_TRANSLATION_LOCATORS
    ]:
        _fail(
            "telekinesis_translation_scope",
            "localized translation asset identities differ",
        )
    if telekinesis.get("corroborating_source_ids") != [
        "ddb_2024_basic_rules_telekinesis"
    ]:
        _fail(
            "telekinesis_corroboration_scope",
            "current corroboration source is missing or misclassified",
        )

    scope = _object(manifest.get("source_scope_policy"), "source_scope_policy")
    if set(
        _strings(
            scope.get("non_rule_segments"), "source_scope_policy.non_rule_segments"
        )
    ) != {
        "PAGE_NUMBER",
        "DOCUMENT_TITLE",
        "NEXT_SPELL_HEADING",
        "PDF_CONTROL_CHARACTER",
        "FOREIGN_COLUMN_CONTENT",
    }:
        _fail(
            "foreign_source_material",
            "page furniture, foreign columns, headings, and control material are not rules",
        )
    if scope.get("primary_spell_text_copied") is not False:
        _fail(
            "primary_source_text_copied",
            "fixtures must not duplicate full primary spell text",
        )


def _validate_numeric_witnesses(manifest: Mapping[str, object]) -> None:
    witnesses = [
        _object(value, f"numeric_glyph_witnesses[{index}]")
        for index, value in enumerate(
            _array(manifest.get("numeric_glyph_witnesses"), "numeric_glyph_witnesses")
        )
    ]
    by_codepoint = {str(row.get("codepoint")): row for row in witnesses}
    if len(by_codepoint) != len(witnesses) or set(by_codepoint) != set(
        EXPECTED_GLYPH_WITNESSES
    ):
        _fail(
            "unicode_source_witness",
            "required U+2212 and U+00D7 source cells are incomplete",
        )
    for codepoint, expected in EXPECTED_GLYPH_WITNESSES.items():
        owner, page, locator, literal = expected
        row = by_codepoint[codepoint]
        if (
            row.get("owner_spell") != owner
            or row.get("printed_page") != page
            or row.get("cell_locator") != locator
            or row.get("literal") != literal
            or chr(int(codepoint.removeprefix("U+"), base=16)) not in literal
        ):
            _fail(
                "unicode_source_witness",
                f"{codepoint} source cell was missing or normalized",
            )


def _validate_seed_observation(manifest: Mapping[str, object]) -> dict[str, object]:
    conflicts = [
        _object(value, f"seed_metadata_conflicts[{index}]")
        for index, value in enumerate(
            _array(manifest.get("seed_metadata_conflicts"), "seed_metadata_conflicts")
        )
    ]
    if len(conflicts) != 1:
        _fail("seed_conflict_census", "exactly one seed observation is expected")
    baseline = _object(
        conflicts[0].get("observed_baseline"), "acid_splash.observed_baseline"
    )
    if (
        baseline.get("path") != SEED_RELATIVE_PATH
        or baseline.get("hash_basis") != "RAW_FILE_BYTES"
        or baseline.get("sha256") != REVIEWED_SEED_SNAPSHOT_SHA256
    ):
        _fail(
            "seed_observation_identity",
            "seed observation is not the reviewed current file",
        )
    path = SOURCE_SEED_PATH.resolve()
    if not path.is_relative_to(REPOSITORY_ROOT) or not path.is_file():
        _fail("seed_observation_missing", "reviewed seed file is unavailable")
    data = path.read_bytes()
    observed_hash = hashlib.sha256(data).hexdigest()
    if observed_hash != REVIEWED_SEED_SNAPSHOT_SHA256:
        _fail(
            "seed_observation_stale",
            "current seed bytes differ from the reviewed snapshot",
        )
    payload = _decode_json(data, "current character-mvp seed")

    records_by_id: dict[str, dict[str, object]] = {}
    for record_id, collection_name in EXPECTED_SEED_RECORD_COLLECTIONS.items():
        matches = [
            row
            for row in _rows(payload, collection_name, "current character-mvp seed")
            if row.get("id") == record_id
        ]
        if len(matches) != 1:
            _fail(
                "seed_record_census", f"current seed does not contain one {record_id}"
            )
        records_by_id[record_id] = matches[0]

    observed_records = [
        _object(value, f"observed_baseline.records[{index}]")
        for index, value in enumerate(
            _array(baseline.get("records"), "observed_baseline.records")
        )
    ]
    observed_ids = [
        _string(row.get("record_id"), f"observed_baseline.records[{index}].record_id")
        for index, row in enumerate(observed_records)
    ]
    if observed_ids != list(EXPECTED_SEED_RECORD_COLLECTIONS):
        _fail(
            "seed_record_census",
            "observed seed records are missing, reordered, or extra",
        )
    for index, row in enumerate(observed_records):
        record_id = observed_ids[index]
        observed_record = _object(
            row.get("record"), f"observed_baseline.records[{index}].record"
        )
        if observed_record != records_by_id[record_id]:
            _fail(
                "seed_record_mismatch",
                f"observed baseline record {record_id} differs from the exact current seed",
            )
    return {
        "path": SEED_RELATIVE_PATH,
        "sha256": observed_hash,
        "records_by_id": records_by_id,
    }


def _validate_seed_conflicts(
    manifest: Mapping[str, object], roster: tuple[Mapping[str, object], ...]
) -> list[dict[str, object]]:
    conflicts = [
        _object(value, f"seed_metadata_conflicts[{index}]")
        for index, value in enumerate(
            _array(manifest.get("seed_metadata_conflicts"), "seed_metadata_conflicts")
        )
    ]
    if len(conflicts) != 1:
        _fail(
            "seed_conflict_census",
            "exactly the existing Acid Splash source conflict is recorded",
        )
    conflict = conflicts[0]
    source = _object(conflict.get("source_facts"), "acid_splash.source_facts")
    observation = _validate_seed_observation(manifest)
    source_record = _object(conflict.get("source_record"), "acid_splash.source_record")
    row = next(
        (candidate for candidate in roster if candidate.get("name") == "Acid Splash"),
        None,
    )
    if row is None:
        _fail("seed_conflict_census", "Acid Splash source record is absent")
    raw = _object(
        row.get("raw_extraction_witness"), "Acid Splash.raw_extraction_witness"
    )
    acid_spell = _object(
        observation["records_by_id"]["spell.acid_splash"], "seed.spell.acid_splash"
    )
    acid_activity = _object(
        observation["records_by_id"]["activity.spell.acid_splash"],
        "seed.activity.spell.acid_splash",
    )
    acid_spell_data = _object(acid_spell.get("data"), "seed.spell.acid_splash.data")
    acid_activity_data = _object(
        acid_activity.get("data"), "seed.activity.spell.acid_splash.data"
    )
    targeting = _object(
        acid_activity_data.get("targeting"), "seed.activity.spell.acid_splash.targeting"
    )
    area = _object(targeting.get("area"), "seed.activity.spell.acid_splash.area")
    dimensions = _object(
        area.get("dimensions"), "seed.activity.spell.acid_splash.dimensions"
    )
    if (
        conflict.get("entry_id") != "spell.acid_splash"
        or source != EXPECTED_ACID_SPLASH_SOURCE_FACTS
        or conflict.get("source_locator")
        != {"asset_id": "srd52_en", "printed_page": 107, "heading": "Acid Splash"}
        or acid_spell_data.get("school_id") != "school.conjuration"
        or targeting.get("kind_id") != "target.entities"
        or targeting.get("minimum") != 0
        or targeting.get("maximum") != 16
        or _object(targeting.get("range"), "acid_splash.seed.range").get("distance")
        != 60
        or area.get("shape_id") != "area.sphere"
        or dimensions.get("radius") != 5
        or source_record.get("artifact_id") != "source-pass-0-2"
        or source_record.get("exact_name") != "Acid Splash"
        or source_record.get("raw_body_sha256") != raw.get("sha256")
        or conflict.get("disposition") != "EVIDENCE_ONLY_NO_REWRITE"
    ):
        _fail(
            "seed_conflict_mismatch", "Acid Splash seed/source conflict witness differs"
        )
    return conflicts


def _validate_extra_lane(
    manifest: Mapping[str, object], roster: tuple[Mapping[str, object], ...]
) -> dict[str, object]:
    extra = _object(manifest.get("existing_extra_lane"), "existing_extra_lane")
    if extra.get("name") in {row.get("name") for row in roster}:
        _fail(
            "extra_in_srd_roster",
            "Thunderclap cannot be counted among the 339 SRD entries",
        )
    status = extra.get("qualification_status")
    if status != "NOT_QUALIFIED":
        _fail(
            "extra_evidence_missing",
            "Thunderclap lacks independent provenance, edition, license, eligibility, and all-mode evidence",
        )
    if (
        extra.get("roster_membership") != "OUTSIDE_SRD_339"
        or extra.get("provenance_status") != "UNPROVEN"
        or extra.get("edition_status") != "UNPROVEN"
        or extra.get("license_status") != "UNPROVEN"
        or extra.get("sorcerer_eligibility_status") != "UNPROVEN"
        or extra.get("all_mode_support_status") != "UNPROVEN"
        or extra.get("selectable") is not False
        or extra.get("evidence") != []
    ):
        _fail(
            "extra_evidence_missing",
            "unproved existing extra must remain separate and nonselectable",
        )
    return extra


def _validate_content_owner_default_repair(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    repair = _object(
        manifest.get("content_owner_default_repair"), "content_owner_default_repair"
    )
    expected_path = EVIDENCE_PATHS["content-acquisition-contracts"]
    expected_hash = next(
        (
            row.get("sha256")
            for row in _array(manifest.get("evidence_artifacts"), "evidence_artifacts")
            if isinstance(row, dict)
            and row.get("artifact_id") == "content-acquisition-contracts"
        ),
        None,
    )
    if (
        repair.get("owner_artifact_id") != "content-acquisition-contracts"
        or repair.get("owner_path") != expected_path
        or repair.get("owner_sha256") != expected_hash
        or repair.get("owner_section") != "Defaults, commitments and migration"
        or repair.get("trigger")
        != "Thunderclap existing-extra provenance/support lane remains unqualified"
        or repair.get("status") != "REQUIRED_BEFORE_PACKAGE_PROMOTION"
        or repair.get("authorized_action")
        != "REPAIR_NEW_INSTALLED_DEFAULT_ATOMICALLY_FROM_LEGAL_SUPPORTED_POOL"
        or repair.get("preserve") != ["legacy snapshots", "accepted work"]
        or repair.get("record_before_promotion")
        != ["lawful source", "compatibility/migration evidence"]
        or repair.get("product_owner_decision_required") is not False
        or repair.get("worker_seed_mutation") != "NONE"
    ):
        _fail(
            "content_owner_default_repair",
            "Thunderclap default-repair disposition differs from the accepted owner contract",
        )
    owner_path = (REPOSITORY_ROOT / expected_path).resolve()
    if not owner_path.is_relative_to(REPOSITORY_ROOT) or not owner_path.is_file():
        _fail("content_owner_default_repair", "accepted content owner is unavailable")
    owner_bytes = owner_path.read_bytes()
    if hashlib.sha256(owner_bytes).hexdigest() != expected_hash:
        _fail("content_owner_default_repair", "accepted content owner bytes changed")
    owner_text = owner_bytes.decode("utf-8")
    if (
        "### Defaults, commitments and migration" not in owner_text
        or "If that lane cannot lawfully close, the content owner must repair the new installed default atomically from the legal supported pool"
        not in owner_text
    ):
        _fail(
            "content_owner_default_repair",
            "accepted owner section does not contain the default-repair authorization",
        )
    return repair


def _source_qualification_receipt(
    manifest: Mapping[str, object], roster: tuple[Mapping[str, object], ...]
) -> dict[str, object]:
    mappings = _validate_source_mapping_lanes(manifest, roster)
    unknown_classification = _validate_source_unknown_classifications(manifest)
    source_modeling_r5 = _validate_source_modeling_r5(manifest)
    roster_names = {str(row.get("name")) for row in roster}
    unmapped_names = sorted(roster_names - set(mappings))
    if len(roster_names) != 339 or unmapped_names:
        _fail(
            "source_mapping_roster_count",
            "the four disjoint source-map groups must cover the exact 339-entry roster",
        )
    mapping_contract = _object(
        manifest.get("source_mapping_contract"), "source_mapping_contract"
    )
    repair = _validate_content_owner_default_repair(manifest)
    extra_lane = _validate_extra_lane(manifest, roster)
    lane_counts = {
        lane_id: sum(1 for value in mappings.values() if value["lane_id"] == lane_id)
        for lane_id in (
            "source-pass-0-2",
            "source-pass-3-5",
            "source-pass-6-9",
            "existing-summary-decompositions",
        )
    }
    unresolved_keys = [
        dict(key)
        for mapping_record in mappings.values()
        for key in mapping_record["unresolved_source_keys"]
    ]
    unresolved_entries = sorted(
        {
            str(residual["source_exact_name"])
            for mapping_record in mappings.values()
            for residual in mapping_record["unresolved_source_keys"]
        }
    )
    source_modeling_residuals = source_modeling_r5["residuals"]
    source_modeling_resolutions = source_modeling_r5["resolutions"]
    table_residuals = [
        _object(value, f"primary_table_evidence_residuals[{index}]")
        for index, value in enumerate(
            _array(
                manifest.get("primary_table_evidence_residuals"),
                "primary_table_evidence_residuals",
            )
        )
    ]
    primary_table_evidence_witnesses = _validate_primary_table_evidence_witnesses(
        manifest
    )
    source_recipe_materialization_classifications = (
        _source_recipe_materialization_residuals(manifest)
    )
    source_recipe_materialization_residuals = [
        row
        for row in source_recipe_materialization_classifications
        if row["blocks_sp00_source_ready"] is True
    ]
    future_executable_recipe_obligations = [
        row
        for row in source_recipe_materialization_classifications
        if row["blocks_sp00_source_ready"] is False
    ]
    summary_only_names = sorted(
        name
        for name, value in mappings.items()
        if value["lane_id"] == "existing-summary-decompositions"
    )
    mapping_reviews_pending = sorted(
        lane_id
        for lane_id in SOURCE_MAPPING_LANE_EXPECTATIONS
        if any(
            lane.get("lane_id") == lane_id
            and lane.get("independent_review_status") != "ACCEPTED"
            for lane in _array(
                manifest.get("source_mapping_lanes"), "source_mapping_lanes"
            )
        )
    )
    source_blocking_keys = set(unknown_classification["source_blocking_keys"])
    source_blocking_entry_names = sorted(
        {
            str(row["source_exact_name"])
            for row in _array(
                manifest.get("source_unknown_classifications"),
                "source_unknown_classifications",
            )
            if isinstance(row, dict)
            and row.get("unresolved_key") in source_blocking_keys
        }
    )
    blockers: list[dict[str, object]] = []
    if source_blocking_keys:
        blockers.append(
            {
                "code": "UNRESOLVED_SOURCE_KEYS",
                "count": len(source_blocking_keys),
                "entry_count": len(source_blocking_entry_names),
            }
        )
    if source_modeling_residuals:
        blockers.append(
            {
                "code": "SOURCE_MODELING_RESIDUALS",
                "count": len(source_modeling_residuals),
                "source_exact_names": [
                    str(value["source_exact_name"])
                    for value in source_modeling_residuals
                ],
            }
        )
    if table_residuals:
        blockers.append(
            {
                "code": "PRIMARY_TABLE_SOURCE_EVIDENCE_PENDING",
                "count": len(table_residuals),
                "source_exact_names": [
                    str(value["source_exact_name"]) for value in table_residuals
                ],
            }
        )
    if source_recipe_materialization_residuals:
        blockers.append(
            {
                "code": "SOURCE_RECONSTRUCTION_GAP_PENDING",
                "count": len(source_recipe_materialization_residuals),
                "source_exact_names": [
                    str(value["source_exact_name"])
                    for value in source_recipe_materialization_residuals
                ],
                "residuals": source_recipe_materialization_residuals,
            }
        )
    if mapping_reviews_pending:
        blockers.append(
            {
                "code": "SOURCE_MAPPING_REVIEW_PENDING",
                "lane_ids": mapping_reviews_pending,
            }
        )
    if summary_only_names:
        blockers.append(
            {
                "code": "SUMMARY_SOURCE_DECOMPOSITION_REVIEW_PENDING",
                "source_exact_names": summary_only_names,
            }
        )
        blockers.append(
            {
                "code": "SOURCE_SUPPORT_OBLIGATIONS_NOT_MAPPED",
                "source_exact_names": summary_only_names,
            }
        )
    if extra_lane.get("qualification_status") != "QUALIFIED":
        blockers.append(
            {
                "code": "DEFAULT_REPAIR_REQUIRED",
                "source_exact_name": "Thunderclap",
                "status": repair["status"],
            }
        )
    source_ready = not blockers
    source_requirement_counts_by_lane = {
        lane_id: sum(
            len(value["source_requirement_keys"])
            for value in mappings.values()
            if value["lane_id"] == lane_id
        )
        for lane_id in lane_counts
    }
    source_common_counts_by_lane = {
        lane_id: sum(
            len(value["source_common_requirement_keys"])
            for value in mappings.values()
            if value["lane_id"] == lane_id
        )
        for lane_id in lane_counts
    }
    source_conditional_counts_by_lane = {
        lane_id: sum(
            len(value["source_conditional_branch_keys"])
            for value in mappings.values()
            if value["lane_id"] == lane_id
        )
        for lane_id in lane_counts
    }
    source_mode_counts_by_lane = {
        lane_id: sum(
            len(value["source_mode_keys"])
            for value in mappings.values()
            if value["lane_id"] == lane_id
        )
        for lane_id in lane_counts
    }
    source_support_counts_by_lane = {
        lane_id: sum(
            len(value["source_support_domain_obligation_keys"])
            for value in mappings.values()
            if value["lane_id"] == lane_id
        )
        for lane_id in lane_counts
    }
    lane0 = next(
        lane
        for lane in _array(manifest.get("source_mapping_lanes"), "source_mapping_lanes")
        if isinstance(lane, dict) and lane.get("lane_id") == "source-pass-0-2"
    )
    lane0_payload = _object(lane0["mapping_payload"], "source-pass-0-2.mapping_payload")
    shared_common_requirement_count = len(
        _array(
            lane0_payload.get("shared_common_requirements"),
            "source-pass-0-2.shared_common_requirements",
        )
    )
    future_proof_dimensions = {
        "eligible_support_domain_member_census": "NOT_ESTABLISHED",
        "native_consumer_mapping": "NOT_ESTABLISHED",
        "consumer_dependency_edges": "NOT_ESTABLISHED",
        "machine_admission": "NOT_ESTABLISHED",
        "actual_native_execution_recovery": "NOT_ESTABLISHED",
        "target_performance": "NOT_ESTABLISHED",
        "unknown_key_future_proof_subobligation_count": unknown_classification[
            "future_proof_subobligation_count"
        ],
        "future_executable_recipe_entry_count": len(
            future_executable_recipe_obligations
        ),
        "downstream_only_unknown_key_count": unknown_classification[
            "downstream_only_key_count"
        ],
        "blocks_sp00_source_ready": False,
    }
    return {
        "status": (
            "W05_SPELL_SOURCE_QUALIFICATION_READY"
            if source_ready
            else "W05_SPELL_SOURCE_CENSUS_PARTIAL"
        ),
        "source_qualification_status": "ESTABLISHED"
        if source_ready
        else "NOT_ESTABLISHED",
        "source_roster_status": "ALL_339_ENTRY_MAPS_PRESENT",
        "source_entry_count": len(roster),
        "source_mode_mapping_status": "ALL_339_MAPS_PENDING_SOURCE_CLOSURE_OR_REVIEW",
        "candidate_mapped_entry_names": sorted(mappings),
        "unmapped_srd_entry_names": unmapped_names,
        "unmapped_srd_entry_count": len(unmapped_names),
        "source_mapping_coverage": {
            "entry_count": len(mappings),
            "entry_count_by_lane": lane_counts,
            "unmapped_entry_names": unmapped_names,
            "source_mode_key_count_by_lane": source_mode_counts_by_lane,
            "source_requirement_key_count": sum(
                len(value["source_requirement_keys"]) for value in mappings.values()
            ),
            "source_requirement_key_count_by_lane": source_requirement_counts_by_lane,
            "source_common_requirement_key_count": sum(
                source_common_counts_by_lane.values()
            ),
            "source_common_requirement_key_count_by_lane": source_common_counts_by_lane,
            "source_conditional_branch_key_count": sum(
                source_conditional_counts_by_lane.values()
            ),
            "source_conditional_branch_key_count_by_lane": source_conditional_counts_by_lane,
            "shared_common_requirement_key_count": shared_common_requirement_count,
            "source_mode_key_count": sum(
                len(value["source_mode_keys"]) for value in mappings.values()
            ),
            "source_support_domain_obligation_count": sum(
                len(value["source_support_domain_obligation_keys"])
                for value in mappings.values()
            ),
            "source_support_domain_obligation_count_by_lane": source_support_counts_by_lane,
            "unresolved_source_key_count": len(unresolved_keys),
            "unresolved_source_entry_count": len(unresolved_entries),
            "source_blocking_unknown_key_count": len(source_blocking_keys),
            "source_blocking_unknown_entry_count": len(source_blocking_entry_names),
            "downstream_only_unknown_key_count": unknown_classification[
                "downstream_only_key_count"
            ],
            "mixed_source_and_downstream_unknown_key_count": unknown_classification[
                "mixed_source_and_downstream_key_count"
            ],
        },
        "unresolved_source_keys": unresolved_keys,
        "source_unknown_classifications": [
            _object(value, f"source_unknown_classifications[{index}]")
            for index, value in enumerate(
                _array(
                    manifest.get("source_unknown_classifications"),
                    "source_unknown_classifications",
                )
            )
        ],
        "source_unknown_classification": unknown_classification,
        "source_modeling_resolutions": source_modeling_resolutions,
        "source_modeling_residuals": source_modeling_residuals,
        "primary_table_evidence_residuals": table_residuals,
        "primary_table_evidence_witnesses": primary_table_evidence_witnesses,
        "source_recipe_materialization_classifications": (
            source_recipe_materialization_classifications
        ),
        "source_recipe_materialization_residuals": source_recipe_materialization_residuals,
        "future_executable_recipe_obligations": future_executable_recipe_obligations,
        "source_support_mapping_status": "SOURCE_DESCRIPTORS_PRESENT_ELIGIBLE_DOMAIN_CENSUS_NOT_ESTABLISHED",
        "support_domain_mapping_status": "OBLIGATIONS_MAPPED_CENSUS_PENDING",
        "source_ready_gate": {
            "ready": source_ready,
            "blockers": blockers,
            "future_native_proof_blocks_sp00": False,
        },
        "future_proof_dimensions": future_proof_dimensions,
        "source_mapping_contract": mapping_contract,
        "content_owner_default_repair": repair,
        "existing_extra_lane": extra_lane,
        "machine_admission": "NOT_ESTABLISHED",
        "production_support": "NOT_ESTABLISHED",
    }


def validate_source_qualification(
    manifest: Mapping[str, object],
    *,
    expected_inventory: Mapping[str, object],
    source_assets: Mapping[str, bytes],
) -> Mapping[str, object]:
    """Validate reviewed source bytes and produce a non-admitting 339-entry census."""
    manifest = _validate_reviewed_manifest(manifest)
    _validate_manifest_schema(manifest)
    evidence = _load_evidence(manifest)
    inventory = _object(evidence.get("spell-inventory"), "spell-inventory")
    if dict(expected_inventory) != inventory:
        _fail(
            "inventory_input_mismatch",
            "expected_inventory differs from its pinned research artifact",
        )
    roster = _derive_roster_from_evidence(manifest, evidence)
    _validate_corroborating_sources(manifest)
    verified_assets = _validate_source_assets(manifest, source_assets)
    _validate_reconstruction_witnesses(manifest, roster)
    _validate_numeric_witnesses(manifest)
    _validate_seed_observation(manifest)
    seed_conflicts = _validate_seed_conflicts(manifest, roster)
    extra_lane = _validate_extra_lane(manifest, roster)
    receipt = _source_qualification_receipt(manifest, roster)

    level_counts = Counter(int(row["level"]) for row in roster)
    if dict(level_counts) != EXPECTED_LEVEL_COUNTS:
        _fail(
            "level_count_mismatch",
            "source roster level counts differ from the approved 339 census",
        )
    notice = _object(
        manifest.get("package_notice_observation"), "package_notice_observation"
    )
    if notice.get("disposition") != "SHARED_INTEGRATOR_REVIEW_REQUIRED":
        _fail(
            "notice_projection_scope",
            "package NOTICE changes belong to the shared integrator",
        )
    return {
        **receipt,
        "source_roster": list(roster),
        "source_roster_counts": {
            "entries": len(roster),
            "by_level": {
                str(level): level_counts[level] for level in sorted(level_counts)
            },
        },
        "source_asset_ids_verified": verified_assets,
        "seed_metadata_conflicts": seed_conflicts,
        "existing_extra_lane": extra_lane,
        "unresolved_source_lanes": [
            {
                "lane": "SRD_SOURCE_MODE_MAPPING",
                "status": "PARTIAL",
                "unmapped_entry_count": receipt["unmapped_srd_entry_count"],
            },
            {
                "lane": "THUNDERCLAP_EXISTING_EXTRA",
                "status": "NOT_QUALIFIED_DEFAULT_REPAIR_REQUIRED",
                "selectable": False,
            },
        ],
        "package_notice_followup": notice,
    }
