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
    "ccdc7195e95e7281b9b8e56eced81bb30e383506dda5509703279dd6e8200e26"
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
    return {
        "total_record_count": 82,
        "source_blocking_key_count": len(source_blocking_keys),
        "source_blocking_keys": source_blocking_keys,
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
