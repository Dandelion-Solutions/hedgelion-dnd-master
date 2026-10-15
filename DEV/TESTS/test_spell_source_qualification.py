from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "DEV/TOOLS/validate_spell_source_qualification.py"
MANIFEST_PATH = ROOT / "DEV/TESTS/fixtures/spell-source-qualification.json"
REJECTED_PATH = ROOT / "DEV/TESTS/fixtures/spell-source-qualification-rejected.json"
INVENTORY_PATH = (
    ROOT
    / "DEV/docs/superpowers/research/2026-10-04-spell-coverage/spell-inventory.json"
)
LEVEL_COUNTS = {0: 27, 1: 57, 2: 57, 3: 42, 4: 34, 5: 38, 6: 31, 7: 20, 8: 17, 9: 16}
FIRST12_SOURCE_CLOSED_KEYS = {
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
FIRST12_SOURCE_HELD_KEYS = {
    "source.spell.aid.unresolved.health_normalization_policy",
    "source.spell.arcane_lock.unresolved.destruction_access_policy",
    "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
}
NEXT12_SOURCE_CLOSED_KEYS = {
    "source.spell.arcanist_s_magic_aura.unresolved.alternate_type_domain",
    "source.spell.arcanist_s_magic_aura.unresolved.false_aura_choice_domain",
    "source.spell.chromatic_orb.unresolved.six_damage_type_members",
    "source.spell.detect_evil_and_good.unresolved.supernatural_type_members",
    "source.spell.detect_poison_and_disease.unresolved.barrier_and_catalog_domain",
    "source.spell.detect_thoughts.unresolved.deeper_failure_disclosure",
    "source.spell.dragon_s_breath.unresolved.five_damage_type_members",
    "source.spell.druidcraft.unresolved.plant_and_fire_eligibility",
    "source.spell.enhance_ability.unresolved.five_ability_members",
    "source.spell.enlarge_reduce.unresolved.mode_exact_modifiers",
    "source.spell.feather_fall.unresolved.descent_rate",
}
NEXT12_SOURCE_HELD_KEYS = {
    "source.spell.detect_magic.unresolved.aura_overlay_policy",
}
SEVENTH_SOURCE_CLOSED_KEYS = {
    "source.spell.augury.unresolved.four_omen_members",
    "source.spell.find_steed.unresolved.type_to_action_mapping",
    "source.spell.find_steed.unresolved.steed_numeric_cells",
    "source.spell.web.unresolved.web_numeric_geometry",
}
SEVENTH_SOURCE_HELD_KEYS = {
    "source.spell.find_familiar.unresolved.eligible_form_census",
    "source.spell.warding_bond.unresolved.copied_damage_policy",
}
FAMILIAR_SOURCE_CLOSED_KEYS = {
    "source.spell.find_familiar.unresolved.eligible_form_census",
}
TENTH_SOURCE_CLOSED_KEYS = {
    "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain",
    "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
    "source.spell.unseen_servant.unresolved.subject_health_classification",
}
OWNER_DECIDED_SOURCE_KEYS = {
    "source.spell.aid.unresolved.health_normalization_policy",
    "source.spell.magic_missile.unresolved.rng_damage_grouping",
    "source.spell.pass_without_trace.unresolved.selection_timing",
    "source.spell.ray_of_frost.unresolved.movement_composition",
    "source.spell.resistance.unresolved.damage_grouping_order",
    "source.spell.warding_bond.unresolved.copied_damage_policy",
}
PRAYER_OWNER_SOURCE_KEY = "source.spell.prayer_of_healing.unresolved.responder_census"
PRAYER_OWNER_DECIDED_SOURCE_KEYS = {PRAYER_OWNER_SOURCE_KEY}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_by_key_for(manifest: dict[str, object], key: str) -> dict[str, object]:
    records = manifest.get("source_unknown_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("source residual resolution evidence must be a list")
    return next(row for row in records if row["unresolved_key"] == key)


def fourth_evidence_by_key_for(
    manifest: dict[str, object], key: str
) -> dict[str, object]:
    records = manifest.get("source_fourth_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("fourth source resolution evidence must be a list")
    return next(row for row in records if row["unresolved_key"] == key)


def seventh_evidence_by_key_category_for(
    manifest: dict[str, object], key: str, category: str
) -> dict[str, object]:
    records = manifest.get("source_seventh_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("seventh source resolution evidence must be a list")
    return next(
        row
        for row in records
        if row["unresolved_key"] == key and row["source_category"] == category
    )


def owner_decision_evidence_by_key_for(
    manifest: dict[str, object], key: str
) -> dict[str, object]:
    records = manifest.get("source_eighth_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("accepted owner source-resolution evidence must be a list")
    return next(row for row in records if row["unresolved_key"] == key)


def prayer_owner_evidence_for(manifest: dict[str, object]) -> dict[str, object]:
    records = manifest.get("source_prayer_owner_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("Prayer owner source-resolution evidence must be a list")
    return next(
        row for row in records if row["unresolved_key"] == PRAYER_OWNER_SOURCE_KEY
    )


def load_tool() -> ModuleType | None:
    if not TOOL_PATH.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        "spell_source_qualification_under_test", TOOL_PATH
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = load_tool()


def make_synthetic_registry() -> tuple[dict[str, object], dict[str, bytes]]:
    manifest = copy.deepcopy(load_json(MANIFEST_PATH))
    payloads: dict[str, bytes] = {}
    assets = manifest["source_assets"]
    if not isinstance(assets, list):
        raise TypeError("source fixture asset registry must be a list")
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            raise TypeError("source fixture asset must be an object")
        uri = (
            "https://media.dndbeyond.com/compendium-images/srd/5.2/"
            f"synthetic-source-{index}.pdf"
        )
        payload = f"synthetic source asset {index}".encode()
        asset["uri"] = uri
        asset["sha256"] = hashlib.sha256(payload).hexdigest()
        payloads[uri] = payload
    return manifest, payloads


def apply_rejected_variant(
    manifest: dict[str, object], variant: dict[str, object]
) -> None:
    if "witness_id" in variant:
        witnesses = manifest["source_reconstruction_witnesses"]
        witness = next(
            row for row in witnesses if row["witness_id"] == variant["witness_id"]
        )
        field = variant["field"]
        operation = variant["operation"]
        if operation == "remove":
            witness[field].remove(variant["value"])
        elif operation == "append":
            witness[field].append(variant["value"])
        elif operation == "remove_field":
            witness.pop(field)
        else:
            raise AssertionError(f"unknown witness mutation: {operation}")
        return

    collection = manifest[variant["collection"]]
    index = variant["index"]
    if variant["operation"] == "replace":
        collection[index][variant["field"]] = variant["value"]
    elif variant["operation"] == "remove_item":
        collection.pop(index)
    else:
        raise AssertionError(f"unknown collection mutation: {variant['operation']}")


class TestSpellSourceQualification(unittest.TestCase):
    def test_source_qualification_producer_exists(self) -> None:
        self.assertIsNotNone(TOOL, "missing SP00 source qualification producer")

    def setUp(self) -> None:
        if (
            TOOL is None
            and self._testMethodName != "test_source_qualification_producer_exists"
        ):
            self.skipTest("source qualification producer has not been implemented")

    def test_source_roster_census_equals_339_and_exact_levels(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(manifest["schema_version"], 1)
        inventory = load_json(INVENTORY_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        inventory_rows = inventory["spells"]
        self.assertIsInstance(inventory_rows, list)
        self.assertEqual(len(roster), 339)
        self.assertEqual(len({row["name"] for row in roster}), 339)
        self.assertEqual(
            {row["name"] for row in roster},
            {row["name"] for row in inventory_rows},
        )
        self.assertEqual(Counter(row["level"] for row in roster), LEVEL_COUNTS)
        self.assertNotIn("Thunderclap", {row["name"] for row in roster})
        self.assertIn(
            "source_mode_mappings",
            manifest,
            "the census needs explicit mode/branch mappings, not summary-number keys",
        )
        explicit_mappings = manifest["source_mode_mappings"]
        mapped_names = {row["entry_name"] for row in explicit_mappings}
        self.assertEqual(mapped_names, {"Alter Self", "Elementalism"})
        element_modes = next(
            row["modes"]
            for row in explicit_mappings
            if row["entry_name"] == "Elementalism"
        )
        self.assertEqual(
            {mode["mode_key"] for mode in element_modes},
            {
                "spell.elementalism.mode.breeze",
                "spell.elementalism.mode.dust_sand",
                "spell.elementalism.mode.fire_smoke",
                "spell.elementalism.mode.mist_clean_water",
                "spell.elementalism.mode.crude_element_shape",
            },
        )
        alter_self = next(
            row for row in explicit_mappings if row["entry_name"] == "Alter Self"
        )
        self.assertEqual(len(alter_self["modes"]), 3)
        self.assertEqual(len(alter_self["control_transitions"]), 1)
        self.assertEqual(element_modes[0]["requirements"][0]["summary_item_index"], 0)
        self.assertEqual(
            next(row for row in explicit_mappings if row["entry_name"] == "Alter Self")[
                "consumer_dependency_status"
            ],
            "NOT_ESTABLISHED",
        )
        self.assertFalse(alter_self["consumer_dependency_edges"])
        roster_by_name = {row["name"]: row for row in roster}
        expected_unmapped_names: set[str] = set()
        actual_unmapped_names = {
            name
            for name, row in roster_by_name.items()
            if row["source_mode_mapping_status"] == "NOT_ESTABLISHED"
        }
        self.assertEqual(actual_unmapped_names, expected_unmapped_names)
        self.assertEqual(sum(len(row["source_mode_keys"]) for row in roster), 638)
        self.assertEqual(
            sum(len(row["source_requirement_keys"]) for row in roster), 3106
        )
        self.assertEqual(
            sum(len(row["source_support_domain_obligation_keys"]) for row in roster),
            862,
        )
        self.assertFalse(
            any(
                key.endswith(".base")
                for row in roster
                for key in row["source_mode_keys"]
            )
        )
        for name in expected_unmapped_names:
            self.assertEqual(roster_by_name[name]["source_mode_keys"], [])
            self.assertEqual(roster_by_name[name]["source_requirement_keys"], [])
        self.assertEqual(
            roster_by_name["Elementalism"]["source_mode_mapping_status"],
            "EXPLICIT_SOURCE_MAPPING_PARTIAL",
        )
        self.assertEqual(
            roster_by_name["Alter Self"]["support_domain_mapping_status"],
            "NOT_ESTABLISHED",
        )
        for witness in manifest["source_reconstruction_witnesses"]:
            owner = roster_by_name[witness["owner_spell"]]
            self.assertTrue(set(witness["reconstruction_obligation_ids"]))
            self.assertEqual(owner["source_status"], "CENSUS_ONLY")
        for row in roster:
            self.assertEqual(
                row["raw_extraction_witness"]["role"],
                "HISTORICAL_RAW_EXTRACTION_ONLY",
            )
            self.assertEqual(row["source_pass_row_ref"]["exact_name"], row["name"])
            self.assertTrue(row["source_pass_row_ref"]["artifact_sha256"])
            self.assertIsInstance(row["source_qualifications"], list)
            self.assertIsInstance(row["source_requirement_summaries"], list)
            for requirement in row["source_requirement_mappings"]:
                self.assertEqual(
                    requirement["closure_evidence"]["exact_name"], row["name"]
                )
                self.assertEqual(
                    requirement["closure_evidence"]["raw_body_sha256"],
                    row["raw_extraction_witness"]["sha256"],
                )
        for key in (
            "source_requirement_keys",
            "source_mode_keys",
            "source_support_obligation_keys",
            "source_support_domain_obligation_keys",
        ):
            flattened = [value for row in roster for value in row[key]]
            self.assertEqual(len(flattened), len(set(flattened)), key)

    def test_source_exact_name_alias_preserves_raw_extraction_label(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        heroes_feast = next(row for row in roster if row["name"] == "Heroes’ Feast")

        self.assertEqual(heroes_feast["source_record_name"], "Heroes' Feast")
        self.assertEqual(
            heroes_feast["source_name_alias_status"], "EXPLICIT_SOURCE_EXACT_NAME"
        )
        self.assertEqual(
            heroes_feast["raw_extraction_witness"]["sha256"],
            "ae00fe248d26b0a41d3ca892501f793e3d46a5a27d98e46d817ffca920485fe3",
        )

    def test_research_labels_are_not_source_support_obligations(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        evidence = TOOL._load_evidence(manifest)
        roster = TOOL.derive_source_requirement_roster(manifest)
        roster_by_name = {row["name"]: row for row in roster}

        for artifact_id, field in (
            ("source-pass-3-5", "dependencies_and_owner_obligations"),
            ("source-pass-6-9", "required_dependency_or_native_contracts"),
        ):
            raw_rows = TOOL._rows(evidence[artifact_id], "rows", artifact_id)
            source_row = next(row for row in raw_rows if field in row)
            census_row = roster_by_name[source_row["name"]]
            self.assertEqual(
                census_row["source_support_obligation_summaries"], source_row[field]
            )
            self.assertEqual(
                census_row["research_dependency_labels"],
                source_row.get("inventory_dependency_labels", []),
            )

        for row in roster:
            self.assertEqual(row["source_support_obligation_keys"], [])
            self.assertIn(
                row["support_domain_mapping_status"],
                {
                    "NOT_ESTABLISHED",
                    "EXPLICIT_SOURCE_OBLIGATIONS_NOT_NATIVE_CLOSURE",
                },
            )
            self.assertEqual(row["consumer_dependency_edges"], [])
            self.assertEqual(row["consumer_dependency_status"], "NOT_ESTABLISHED")

    def test_reviewed_registry_rejects_synthetic_manifest_substitution(self) -> None:
        assert TOOL is not None
        manifest, assets = make_synthetic_registry()
        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL.validate_source_qualification(
                manifest,
                expected_inventory=load_json(INVENTORY_PATH),
                source_assets=assets,
            )
        self.assertEqual(caught.exception.code, "reviewed_manifest_mismatch")

    def test_source_mode_maps_are_explicit_and_census_is_not_ready(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)

        self.assertEqual(receipt["status"], "W05_SPELL_SOURCE_CENSUS_PARTIAL")
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertEqual(receipt["source_mapping_coverage"]["unmapped_entry_names"], [])
        self.assertEqual(
            receipt["source_mapping_coverage"]["unresolved_source_key_count"], 82
        )
        self.assertEqual(
            receipt["source_mapping_coverage"]["unresolved_source_entry_count"], 72
        )
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        mapped_names = set(receipt["candidate_mapped_entry_names"])
        source_names = {row["name"] for row in roster}
        self.assertEqual(mapped_names, source_names)
        self.assertEqual(receipt["unmapped_srd_entry_names"], [])
        self.assertNotEqual(receipt["status"], "W05_SPELL_SOURCE_QUALIFICATION_READY")

        rejected = load_json(REJECTED_PATH)
        for variant in rejected["mode_rejections"]:
            candidate = copy.deepcopy(manifest)
            mapping = next(
                row
                for row in candidate["source_mode_mappings"]
                if row["entry_name"] == variant["entry_name"]
            )
            mapping["modes"][variant["mode_index"]]["mode_name"] = variant["mode_name"]
            with (
                self.subTest(case=variant["case_id"]),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_source_mode_mappings(candidate, roster)

    def test_mapping_lanes_cover_339_and_separate_source_from_future_proof_gates(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)

        self.assertEqual(
            [lane["lane_id"] for lane in manifest["source_mapping_lanes"]],
            ["source-pass-0-2", "source-pass-3-5", "source-pass-6-9"],
        )
        coverage = receipt["source_mapping_coverage"]
        self.assertEqual(coverage["entry_count"], 339)
        self.assertEqual(
            coverage["entry_count_by_lane"],
            {
                "source-pass-0-2": 139,
                "source-pass-3-5": 114,
                "source-pass-6-9": 84,
                "existing-summary-decompositions": 2,
            },
        )
        self.assertEqual(coverage["unmapped_entry_names"], [])
        self.assertEqual(coverage["unresolved_source_key_count"], 82)
        self.assertEqual(coverage["unresolved_source_entry_count"], 72)
        self.assertEqual(
            coverage["source_mode_key_count_by_lane"],
            {
                "source-pass-0-2": 58,
                "source-pass-3-5": 308,
                "source-pass-6-9": 264,
                "existing-summary-decompositions": 8,
            },
        )
        self.assertEqual(
            coverage["source_common_requirement_key_count_by_lane"],
            {
                "source-pass-0-2": 282,
                "source-pass-3-5": 1026,
                "source-pass-6-9": 182,
                "existing-summary-decompositions": 0,
            },
        )
        self.assertEqual(coverage["source_common_requirement_key_count"], 1490)
        self.assertEqual(coverage["source_conditional_branch_key_count"], 1604)
        self.assertEqual(coverage["shared_common_requirement_key_count"], 16)
        self.assertEqual(coverage["source_support_domain_obligation_count"], 862)
        self.assertEqual(
            coverage["source_support_domain_obligation_count_by_lane"],
            {
                "source-pass-0-2": 12,
                "source-pass-3-5": 447,
                "source-pass-6-9": 403,
                "existing-summary-decompositions": 0,
            },
        )
        self.assertEqual(len(receipt["unresolved_source_keys"]), 82)
        self.assertEqual(
            len({row["unresolved_key"] for row in receipt["unresolved_source_keys"]}),
            82,
        )
        self.assertEqual(
            {row["source_exact_name"] for row in receipt["source_modeling_residuals"]},
            {"Word of Recall"},
        )
        self.assertEqual(
            {
                row["source_exact_name"]
                for row in receipt["primary_table_evidence_residuals"]
            },
            set(),
        )
        table_witnesses = receipt["primary_table_evidence_witnesses"]
        self.assertEqual(
            {row["source_exact_name"] for row in table_witnesses},
            {"Teleport", "Control Weather"},
        )
        self.assertTrue(
            all(
                row["status"] == "PRIMARY_TABLE_EVIDENCE_VERIFIED_SOURCE_ONLY"
                and row["machine_execution_proof_status"] == "NOT_ESTABLISHED"
                for row in table_witnesses
            )
        )
        recipe_classifications = receipt[
            "source_recipe_materialization_classifications"
        ]
        self.assertEqual(len(recipe_classifications), 114)
        recipe_by_name = {
            row["source_exact_name"]: row for row in recipe_classifications
        }
        self.assertEqual(len(recipe_by_name), 114)
        self.assertEqual(
            {
                row["source_exact_name"]
                for row in receipt["source_recipe_materialization_residuals"]
            },
            {
                "Animate Objects",
                "Antilife Shell",
                "Fireball",
                "Giant Insect",
                "Raise Dead",
                "Scrying",
                "Slow",
                "Telekinesis",
            },
        )
        future_recipes = receipt["future_executable_recipe_obligations"]
        self.assertEqual(len(future_recipes), 106)
        remove_curse = recipe_by_name["Remove Curse"]
        self.assertEqual(remove_curse["classification"], "FUTURE_EXECUTABLE_RECIPE")
        self.assertFalse(remove_curse["blocks_sp00_source_ready"])
        self.assertIsNone(remove_curse["source_finding_ref"])
        lane35 = next(
            lane
            for lane in manifest["source_mapping_lanes"]
            if lane["lane_id"] == "source-pass-3-5"
        )["mapping_payload"]
        generic_recipe_hold = (
            "Actual numeric and parameter recipes need source-bound materialization; "
            "frozen body review is retained, not repeated."
        )
        self.assertEqual(
            sum(
                row["residuals"].count(generic_recipe_hold) for row in lane35["entries"]
            ),
            114,
        )
        self.assertTrue(
            all(
                row["original_generic_recipe_hold"] == generic_recipe_hold
                for row in recipe_classifications
            )
        )
        remove_curse_map = next(
            row for row in lane35["entries"] if row["entry_name"] == "Remove Curse"
        )
        self.assertEqual(
            {mode["mode_name"] for mode in remove_curse_map["modes"]},
            {"ordinary_curses", "cursed_item"},
        )
        phase_by_name = {
            row["entry_name"]: {3: "SP20", 4: "SP21", 5: "SP22"}[row["level"]]
            for row in lane35["entries"]
        }
        for recipe in future_recipes:
            self.assertEqual(
                recipe["future_recipe_phase"],
                phase_by_name[recipe["source_exact_name"]],
                recipe["source_exact_name"],
            )
        self.assertEqual(remove_curse["future_recipe_phase"], "SP20")
        remove_curse_profile = {
            item["requirement_key"].rsplit(".", 1)[-1]: item["source_value"]
            for item in remove_curse_map["entry_requirements"]
            if item["requirement_key"].startswith("spell.remove_curse.casting_profile.")
        }
        self.assertEqual(
            remove_curse_profile,
            {
                "casting_time": "Action",
                "range": "Touch",
                "components": "V, S",
                "duration": "Instantaneous",
            },
        )
        self.assertNotIn(
            "Remove Curse",
            {
                name
                for blocker in receipt["source_ready_gate"]["blockers"]
                if blocker["code"] == "SOURCE_RECONSTRUCTION_GAP_PENDING"
                for name in blocker["source_exact_names"]
            },
        )
        source_gap = recipe_by_name["Fireball"]
        self.assertEqual(source_gap["classification"], "SOURCE_RECONSTRUCTION_GAP")
        self.assertEqual(source_gap["source_finding_id"], "L35-O9")
        self.assertTrue(source_gap["blocks_sp00_source_ready"])
        self.assertIsNone(source_gap["future_recipe_phase"])
        self.assertEqual(receipt["status"], "W05_SPELL_SOURCE_CENSUS_PARTIAL")
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertEqual(receipt["production_support"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        blocker_codes = {
            blocker["code"] for blocker in receipt["source_ready_gate"]["blockers"]
        }
        self.assertTrue(
            {
                "UNRESOLVED_SOURCE_KEYS",
                "SOURCE_MODELING_RESIDUALS",
                "SOURCE_RECONSTRUCTION_GAP_PENDING",
                "SOURCE_MAPPING_REVIEW_PENDING",
                "SUMMARY_SOURCE_DECOMPOSITION_REVIEW_PENDING",
                "SOURCE_SUPPORT_OBLIGATIONS_NOT_MAPPED",
                "DEFAULT_REPAIR_REQUIRED",
            }.issubset(blocker_codes)
        )
        self.assertFalse(
            any("NATIVE" in code or "EXECUTION" in code for code in blocker_codes)
        )
        self.assertNotIn("PRIMARY_TABLE_SOURCE_EVIDENCE_PENDING", blocker_codes)
        unresolved_blocker = next(
            blocker
            for blocker in receipt["source_ready_gate"]["blockers"]
            if blocker["code"] == "UNRESOLVED_SOURCE_KEYS"
        )
        self.assertEqual(unresolved_blocker["count"], 6)
        self.assertEqual(unresolved_blocker["entry_count"], 6)
        recipe_blocker = next(
            blocker
            for blocker in receipt["source_ready_gate"]["blockers"]
            if blocker["code"] == "SOURCE_RECONSTRUCTION_GAP_PENDING"
        )
        self.assertEqual(recipe_blocker["count"], 8)
        self.assertEqual(len(recipe_blocker["source_exact_names"]), 8)
        future_proofs = receipt["future_proof_dimensions"]
        self.assertEqual(future_proofs["native_consumer_mapping"], "NOT_ESTABLISHED")
        self.assertEqual(
            future_proofs["unknown_key_future_proof_subobligation_count"], 33
        )
        self.assertFalse(
            receipt["source_ready_gate"]["future_native_proof_blocks_sp00"]
        )

    def test_primary_table_witnesses_are_asset_bound_and_reject_corruption(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        witnesses = TOOL._validate_primary_table_evidence_witnesses(manifest)
        self.assertEqual(
            {row["source_exact_name"] for row in witnesses},
            {"Teleport", "Control Weather"},
        )
        teleport = next(
            row for row in witnesses if row["source_exact_name"] == "Teleport"
        )
        weather = next(
            row for row in witnesses if row["source_exact_name"] == "Control Weather"
        )
        self.assertEqual(len(teleport["outcome_cells"]), 24)
        self.assertEqual(len(teleport["familiarity_conditions"]), 6)
        self.assertEqual(len(teleport["outcome_explanations"]), 4)
        self.assertEqual(len(weather["stage_rows"]), 16)
        self.assertEqual(weather["stage_cell_count"], 32)
        source_asset = next(
            row for row in manifest["source_assets"] if row["asset_id"] == "srd52_en"
        )
        expected_locators = {
            "Teleport": (50, 168, 14887),
            "Control Weather": (56, 120, 10284),
        }
        for witness in witnesses:
            name = witness["source_exact_name"]
            source_ref = witness["source_pass_ref"]
            provenance = witness["visual_provenance"]
            self.assertEqual(
                (
                    source_ref["record_index"],
                    source_ref["printed_page"],
                    source_ref["source_header_line"],
                ),
                expected_locators[name],
            )
            self.assertEqual(provenance["source_asset_sha256"], source_asset["sha256"])
            self.assertEqual(
                provenance["source_pass_sha256"],
                next(
                    row["sha256"]
                    for row in manifest["evidence_artifacts"]
                    if row["artifact_id"] == "source-pass-6-9"
                ),
            )
            self.assertFalse(provenance["unqualified_subset_page"]["qualified"])
        self.assertTrue(
            any(
                cell["literal"].endswith("00") and cell["normalized_interval"][1] == 100
                for cell in teleport["outcome_cells"]
                if cell["normalized_interval"] is not None
            )
        )
        self.assertFalse(
            teleport["normalization"]["general_d100_primary_rule_verified"]
        )
        self.assertEqual(weather["transition_formula"], "1d4 × 10 minutes")

        corruptions = (
            ("missing_cell", lambda t, w: t["outcome_cells"].pop()),
            (
                "changed_cell",
                lambda t, w: t["outcome_cells"][8].__setitem__("literal", "01–06"),
            ),
            (
                "range_overlap",
                lambda t, w: (
                    t["outcome_cells"][12].__setitem__("literal", "01–34"),
                    t["outcome_cells"][12].__setitem__("normalized_interval", [1, 34]),
                ),
            ),
            ("wrong_stage", lambda t, w: w["stage_rows"][0].__setitem__("stage", 6)),
            (
                "wrong_source_locator",
                lambda t, w: w["source_pass_ref"].__setitem__("source_page", 121),
            ),
            (
                "minus_instead_of_en_dash",
                lambda t, w: next(
                    cell for cell in t["outcome_cells"] if cell["literal"] == "25–00"
                ).__setitem__("literal", "25−00"),
            ),
            (
                "multiplication_glyph_corruption",
                lambda t, w: w.__setitem__("transition_formula", "1d4 - 10 minutes"),
            ),
        )
        for case, mutate in corruptions:
            with self.subTest(case=case):
                candidate = copy.deepcopy(manifest)
                teleport_candidate = next(
                    row
                    for row in candidate["primary_table_evidence_witnesses"]
                    if row["source_exact_name"] == "Teleport"
                )
                weather_candidate = next(
                    row
                    for row in candidate["primary_table_evidence_witnesses"]
                    if row["source_exact_name"] == "Control Weather"
                )
                mutate(teleport_candidate, weather_candidate)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_primary_table_evidence_witnesses(candidate)
                if case == "range_overlap":
                    self.assertEqual(
                        caught.exception.code, "primary_table_range_partition"
                    )

    def test_mapping_lane_same_count_entry_and_key_substitution_is_rejected(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        for lane in manifest["source_mapping_lanes"]:
            entry_candidate = copy.deepcopy(manifest)
            lane_candidate = next(
                item
                for item in entry_candidate["source_mapping_lanes"]
                if item["lane_id"] == lane["lane_id"]
            )
            rows = lane_candidate["mapping_payload"]["entries"]
            row = rows[0]
            name_field = {
                "source-pass-0-2": "source_exact_name",
                "source-pass-3-5": "entry_name",
                "source-pass-6-9": "name",
            }[lane["lane_id"]]
            row[name_field] = "Unreviewed replacement"
            self.assertEqual(len(rows), len(lane["mapping_payload"]["entries"]))
            with (
                self.subTest(lane=lane["lane_id"], mutation="entry"),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_source_mapping_lanes(entry_candidate, roster)

            key_candidate = copy.deepcopy(manifest)
            key_lane = next(
                item
                for item in key_candidate["source_mapping_lanes"]
                if item["lane_id"] == lane["lane_id"]
            )

            def substitute_key(value: object) -> bool:
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key in {
                            "source_requirement_key",
                            "requirement_key",
                            "source_mode_key",
                            "mode_key",
                            "source_support_domain_key",
                            "support_domain_key",
                        } and isinstance(child, str):
                            value[key] = "source.key.substituted"
                            return True
                        if substitute_key(child):
                            return True
                elif isinstance(value, list):
                    return any(substitute_key(child) for child in value)
                return False

            self.assertTrue(substitute_key(key_lane["mapping_payload"]))
            with (
                self.subTest(lane=lane["lane_id"], mutation="key"),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_source_mapping_lanes(key_candidate, roster)

    def test_unresolved_keys_split_source_gaps_from_future_consumer_proof(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        lane0 = next(
            lane
            for lane in manifest["source_mapping_lanes"]
            if lane["lane_id"] == "source-pass-0-2"
        )
        original = {
            row["unresolved_key"]: row
            for row in lane0["mapping_payload"]["unresolved_key_index"]
        }
        classifications = manifest["source_unknown_classifications"]
        self.assertEqual(len(classifications), 82)
        self.assertEqual(
            {row["unresolved_key"] for row in classifications}, set(original)
        )
        allowed_categories = {
            "source_parameter",
            "source_semantics",
            "source_mapping_review",
            "downstream_domain_consumer_admission_native_proof",
        }
        for row in classifications:
            source_record = original[row["unresolved_key"]]
            self.assertEqual(
                row["source_exact_name"], source_record["source_exact_name"]
            )
            self.assertEqual(row["original_reason"], source_record["reason"])
            self.assertEqual(row["evidence_ref"], source_record["evidence_ref"])
            subobligations = row["subobligations"]
            self.assertTrue(subobligations)
            self.assertEqual(
                len({item["subobligation_id"] for item in subobligations}),
                len(subobligations),
            )
            self.assertTrue(
                {item["category"] for item in subobligations}.issubset(
                    allowed_categories
                )
            )

        by_key = {row["unresolved_key"]: row for row in classifications}
        downstream = "downstream_domain_consumer_admission_native_proof"
        self.assertEqual(
            {
                item["category"]
                for item in by_key[
                    "source.spell.chill_touch.unresolved.recovery_consumer_closure"
                ]["subobligations"]
            },
            {downstream},
        )
        self.assertEqual(
            {
                item["category"]
                for item in by_key[
                    "source.spell.locate_object.unresolved.current_query_consumer"
                ]["subobligations"]
            },
            {"source_semantics", downstream},
        )
        self.assertEqual(
            {
                item["category"]
                for item in by_key[
                    "source.spell.ray_of_frost.unresolved.movement_composition"
                ]["subobligations"]
            },
            {"source_parameter", downstream},
        )
        self.assertEqual(
            {
                item["category"]
                for item in by_key[
                    "source.spell.prayer_of_healing.unresolved.responder_census"
                ]["subobligations"]
            },
            {"source_mapping_review", downstream},
        )

        classification = receipt["source_unknown_classification"]
        self.assertEqual(receipt["source_unknown_classifications"], classifications)
        self.assertEqual(classification["total_record_count"], 82)
        self.assertEqual(
            classification["source_blocking_key_count"],
            len(classification["source_blocking_keys"]),
        )
        self.assertIn(
            "source.spell.chill_touch.unresolved.recovery_consumer_closure",
            classification["downstream_only_keys"],
        )
        self.assertNotIn(
            "source.spell.chill_touch.unresolved.recovery_consumer_closure",
            classification["source_blocking_keys"],
        )
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["downstream_only_key_count"], 5)
        self.assertEqual(classification["mixed_source_and_downstream_key_count"], 28)
        ray = by_key["source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy"]
        ray_semantics = next(
            item
            for item in ray["subobligations"]
            if item["category"] == "source_semantics"
        )
        self.assertIn("subtraction-die", ray_semantics["description"])
        self.assertIn("damage-floor", ray_semantics["description"])
        self.assertNotIn("halving", ray_semantics["description"].lower())
        ray_source = TOOL._load_evidence(manifest)["source-pass-0-2"]["rows"][106]
        self.assertIn(
            "subtraction die on all damage rolls",
            ray_source["required_modes_or_exceptions"],
        )
        self.assertTrue(
            any(
                "not legacy ranged hit/half Strength weapon damage" in item
                for item in ray_source["qualifications"]
            )
        )
        self.assertTrue(ray["source_ready_blocking"])
        self.assertNotIn(
            "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
            classification["source_blocking_keys"],
        )
        self.assertIn(
            "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
            classification["source_resolved_keys"],
        )

        tampered = copy.deepcopy(manifest)
        mixed = next(
            row
            for row in tampered["source_unknown_classifications"]
            if row["unresolved_key"]
            == "source.spell.locate_object.unresolved.current_query_consumer"
        )
        mixed["source_ready_blocking"] = False
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(tampered)

    def test_first12_markdown_review_closes_only_nine_source_subobligations(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        classification = receipt["source_unknown_classification"]

        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(
            manifest["source_unknown_resolution_contract"][
                "source_closed_subobligation_count"
            ],
            9,
        )
        self.assertEqual(
            manifest["source_unknown_resolution_contract"][
                "source_held_subobligation_count"
            ],
            3,
        )
        self.assertEqual(
            manifest["source_unknown_resolution_contract"][
                "active_source_blocker_count"
            ],
            68,
        )
        source_blocking_keys = set(classification["source_blocking_keys"])
        self.assertTrue(FIRST12_SOURCE_CLOSED_KEYS.isdisjoint(source_blocking_keys))
        self.assertTrue(
            (
                FIRST12_SOURCE_HELD_KEYS
                - OWNER_DECIDED_SOURCE_KEYS
                - TENTH_SOURCE_CLOSED_KEYS
                - PRAYER_OWNER_DECIDED_SOURCE_KEYS
            ).issubset(source_blocking_keys)
        )
        self.assertNotIn(
            "source.spell.augury.unresolved.four_omen_members", source_blocking_keys
        )

        evidence = manifest["source_unknown_resolution_evidence"]
        evidence_by_key = {row["unresolved_key"]: row for row in evidence}
        self.assertEqual(
            set(evidence_by_key), FIRST12_SOURCE_CLOSED_KEYS | FIRST12_SOURCE_HELD_KEYS
        )
        for key in FIRST12_SOURCE_CLOSED_KEYS:
            self.assertEqual(evidence_by_key[key]["disposition"], "SOURCE_CLOSED")
        for key in FIRST12_SOURCE_HELD_KEYS:
            self.assertEqual(evidence_by_key[key]["disposition"], "SOURCE_HELD")

        original_by_key = {
            row["unresolved_key"]: row
            for row in manifest["source_unknown_classifications"]
        }
        for key, evidence_row in evidence_by_key.items():
            original = original_by_key[key]
            self.assertEqual(original["original_status"], "NOT_ESTABLISHED")
            self.assertEqual(
                evidence_row["future_native_proof_status"], "NOT_ESTABLISHED"
            )
            self.assertEqual(evidence_row["actual_native_proof_refs"], [])
            self.assertEqual(
                evidence_row["source_record_ref"]["json_pointer"],
                original["evidence_ref"]["json_pointer"],
            )
            self.assertEqual(
                evidence_row["source_record_ref"]["body_witness_ref"]["json_pointer"],
                original["evidence_ref"]["body_witness_ref"]["json_pointer"],
            )

        self.assertEqual(receipt["status"], "W05_SPELL_SOURCE_CENSUS_PARTIAL")
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        self.assertEqual(
            receipt["source_mapping_coverage"]["unresolved_source_key_count"], 82
        )

    def test_accepted_owner_evidence_rejects_cold_identity_and_scope_mutations(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejections = load_json(REJECTED_PATH)["owner_decision_rejections"]

        def owner_row(candidate: dict[str, object], key: str) -> dict[str, object]:
            return owner_decision_evidence_by_key_for(candidate, key)

        def apply_mutation(
            candidate: dict[str, object], rejection: dict[str, object]
        ) -> None:
            mutation = rejection["mutation"]
            if mutation == "owner_field":
                candidate["source_interpretation_owner"][rejection["field"]] = (
                    rejection["value"]
                )
            elif mutation == "owner_row_field":
                owner_row(candidate, rejection["unresolved_key"])[
                    rejection["field"]
                ] = rejection["value"]
            elif mutation == "material_qualifier":
                row = owner_row(candidate, rejection["unresolved_key"])
                row["material_qualifiers"][rejection["index"]] = rejection["value"]
            elif mutation == "golden_value":
                row = owner_row(candidate, rejection["unresolved_key"])
                row["golden_witness"][rejection["field"]] = rejection["value"]
            elif mutation == "prior_hold_disposition":
                row = next(
                    value
                    for value in candidate["source_seventh_resolution_evidence"]
                    if value["unresolved_key"] == rejection["unresolved_key"]
                )
                row["disposition"] = rejection["value"]
            elif mutation == "future_proof_field":
                classification = next(
                    value
                    for value in candidate["source_unknown_classifications"]
                    if value["unresolved_key"] == rejection["unresolved_key"]
                )
                subobligation = next(
                    value
                    for value in classification["subobligations"]
                    if value["category"]
                    == "downstream_domain_consumer_admission_native_proof"
                )
                subobligation[rejection["field"]] = rejection["value"]
            elif mutation == "historical_classification_field":
                classification = next(
                    value
                    for value in candidate["source_unknown_classifications"]
                    if value["unresolved_key"] == rejection["unresolved_key"]
                )
                classification[rejection["field"]] = rejection["value"]
            else:
                raise AssertionError(f"unknown owner-decision mutation: {mutation}")

        self.assertEqual(len({case["case_id"] for case in rejections}), len(rejections))
        for rejection in rejections:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=rejection["case_id"]):
                apply_mutation(candidate, rejection)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )

    def test_first12_markdown_witness_rejects_drift_and_command_static_proximity(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        result = TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(
            result["source_markdown_sha256"],
            "c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e",
        )
        evidence_by_key = {
            row["unresolved_key"]: row
            for row in manifest["source_unknown_resolution_evidence"]
        }
        command = evidence_by_key[
            "source.spell.command.unresolved.command_exact_restrictions"
        ]
        self.assertIn("if it moves within 5 feet", command["source_interpretation"])
        self.assertNotIn(
            "end its turn if within 5 feet", command["source_interpretation"]
        )
        self.assertIn(
            "if it moves within 5 feet of you", result["command_approach_source_text"]
        )

        for mutate in (
            lambda candidate: candidate["source_markdown_source"].update(
                {"sha256": "0" * 64}
            ),
            lambda candidate: evidence_by_key_for(
                candidate, "source.spell.aid.unresolved.health_normalization_policy"
            ).update({"disposition": "SOURCE_CLOSED"}),
            lambda candidate: evidence_by_key_for(
                candidate, "source.spell.alarm.unresolved.audible_sound_bounds"
            )["source_record_ref"].update(
                {"json_pointer": "/rows/4/required_modes_or_exceptions"}
            ),
            lambda candidate: evidence_by_key_for(
                candidate, "source.spell.alarm.unresolved.audible_sound_bounds"
            )["source_markdown_locators"][0].update({"line_start": 9324}),
            lambda candidate: evidence_by_key_for(
                candidate, "source.spell.command.unresolved.command_exact_restrictions"
            ).update(
                {
                    "source_interpretation": "End its turn if within 5 feet of the caster."
                }
            ),
        ):
            tampered = copy.deepcopy(manifest)
            with self.assertRaises(TOOL.SourceQualificationError):
                mutate(tampered)
                TOOL._validate_source_unknown_classifications(tampered)
        tampered = copy.deepcopy(manifest)
        tampered["source_unknown_classifications"][0]["original_reason"] += " Changed."
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(tampered)

    def test_next12_source_closures_preserve_first12_and_detect_magic_hold(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        classification = receipt["source_unknown_classification"]

        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        resolved_keys = set(classification["source_resolved_keys"])
        held_keys = set(classification["source_held_keys"])
        self.assertEqual(
            resolved_keys,
            FIRST12_SOURCE_CLOSED_KEYS
            | NEXT12_SOURCE_CLOSED_KEYS
            | TOOL.THIRD12_SOURCE_CLOSED_KEYS
            | TOOL.FOURTH_SOURCE_CLOSED_KEYS
            | TOOL.FIFTH_SOURCE_CLOSED_KEYS
            | TOOL.SIXTH_SOURCE_CLOSED_KEYS
            | SEVENTH_SOURCE_CLOSED_KEYS
            | FAMILIAR_SOURCE_CLOSED_KEYS
            | TENTH_SOURCE_CLOSED_KEYS
            | OWNER_DECIDED_SOURCE_KEYS
            | PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertEqual(
            held_keys,
            (
                FIRST12_SOURCE_HELD_KEYS
                | NEXT12_SOURCE_HELD_KEYS
                | TOOL.THIRD12_SOURCE_HELD_KEYS
                | TOOL.FOURTH_SOURCE_HELD_KEYS
                | TOOL.FIFTH_SOURCE_HELD_KEYS
                | TOOL.SIXTH_SOURCE_HELD_KEYS
                | SEVENTH_SOURCE_HELD_KEYS
            )
            - OWNER_DECIDED_SOURCE_KEYS
            - FAMILIAR_SOURCE_CLOSED_KEYS
            - TENTH_SOURCE_CLOSED_KEYS
            - PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertEqual(len(classification["source_resolved_keys"]), 71)
        self.assertEqual(len(set(classification["source_resolved_keys"])), 71)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(len(classification["historical_source_blocking_keys"]), 77)
        self.assertNotIn(
            "source.spell.augury.unresolved.four_omen_members",
            classification["source_blocking_keys"],
        )
        self.assertIn(
            "source.spell.detect_poison_and_disease.unresolved.barrier_and_catalog_domain",
            resolved_keys,
        )
        self.assertIn(
            "source.spell.detect_magic.unresolved.aura_overlay_policy", held_keys
        )
        self.assertNotIn(
            "source.spell.chromatic_orb.unresolved.six_damage_type_members",
            classification["source_blocking_keys"],
        )
        self.assertNotIn(
            "source.spell.detect_evil_and_good.unresolved.supernatural_type_members",
            classification["source_blocking_keys"],
        )

        evidence_by_key = {
            row["unresolved_key"]: row
            for row in manifest["source_unknown_resolution_evidence"]
        }
        self.assertEqual(
            set(evidence_by_key), FIRST12_SOURCE_CLOSED_KEYS | FIRST12_SOURCE_HELD_KEYS
        )
        for key in FIRST12_SOURCE_HELD_KEYS:
            self.assertEqual(evidence_by_key[key]["disposition"], "SOURCE_HELD")
        command = evidence_by_key[
            "source.spell.command.unresolved.command_exact_restrictions"
        ]
        self.assertIn("if it moves within 5 feet", command["source_interpretation"])

        next_evidence = manifest["source_next12_resolution_evidence"]
        next_by_key = {row["unresolved_key"]: row for row in next_evidence}
        self.assertEqual(
            set(next_by_key), NEXT12_SOURCE_CLOSED_KEYS | NEXT12_SOURCE_HELD_KEYS
        )
        for key in NEXT12_SOURCE_CLOSED_KEYS:
            self.assertEqual(next_by_key[key]["disposition"], "SOURCE_CLOSED")
        self.assertEqual(
            next_by_key["source.spell.detect_magic.unresolved.aura_overlay_policy"][
                "disposition"
            ],
            "SOURCE_HELD",
        )
        self.assertEqual(len(next_evidence), 13)

        druidcraft = [
            row
            for row in next_evidence
            if row["unresolved_key"]
            == "source.spell.druidcraft.unresolved.plant_and_fire_eligibility"
        ]
        self.assertEqual(
            {row["subobligation_id"].rsplit("::", 1)[-1] for row in druidcraft},
            {"source_mapping_review", "source_parameter"},
        )
        tables = manifest["primary_table_evidence_witnesses"]
        self.assertEqual(
            {row["source_exact_name"] for row in tables},
            {"Teleport", "Control Weather"},
        )
        self.assertEqual(manifest["primary_table_evidence_residuals"], [])
        classifications = {
            row["unresolved_key"]: row
            for row in manifest["source_unknown_classifications"]
        }
        poison_subobligations = classifications[
            "source.spell.detect_poison_and_disease.unresolved.barrier_and_catalog_domain"
        ]["subobligations"]
        downstream = next(
            row
            for row in poison_subobligations
            if row["category"] == "downstream_domain_consumer_admission_native_proof"
        )
        self.assertEqual(downstream["status"], "NOT_ESTABLISHED")
        self.assertEqual(downstream["gate_phase"], "FUTURE_PROOF")
        self.assertEqual(
            manifest["source_next12_resolution_contract"][
                "active_source_blocker_count"
            ],
            57,
        )

    def test_third12_source_qualification_adds_only_reviewed_closures_and_hold(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)

        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["downstream_only_key_count"], 5)
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(len(classification["source_resolved_keys"]), 71)
        self.assertEqual(len(classification["source_held_keys"]), 6)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(
            set(classification["source_resolved_keys"]),
            TOOL.SOURCE_RESOLVED_KEYS
            | TOOL.NEXT12_SOURCE_CLOSED_KEYS
            | TOOL.THIRD12_SOURCE_CLOSED_KEYS
            | TOOL.FOURTH_SOURCE_CLOSED_KEYS
            | TOOL.FIFTH_SOURCE_CLOSED_KEYS
            | TOOL.SIXTH_SOURCE_CLOSED_KEYS
            | SEVENTH_SOURCE_CLOSED_KEYS
            | FAMILIAR_SOURCE_CLOSED_KEYS
            | TENTH_SOURCE_CLOSED_KEYS
            | OWNER_DECIDED_SOURCE_KEYS
            | PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertEqual(
            set(classification["source_held_keys"]),
            (
                TOOL.SOURCE_HELD_KEYS
                | TOOL.NEXT12_SOURCE_HELD_KEYS
                | TOOL.THIRD12_SOURCE_HELD_KEYS
                | TOOL.FOURTH_SOURCE_HELD_KEYS
                | TOOL.FIFTH_SOURCE_HELD_KEYS
                | TOOL.SIXTH_SOURCE_HELD_KEYS
                | SEVENTH_SOURCE_HELD_KEYS
            )
            - OWNER_DECIDED_SOURCE_KEYS
            - FAMILIAR_SOURCE_CLOSED_KEYS
            - TENTH_SOURCE_CLOSED_KEYS
            - PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertIn(
            "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
            classification["source_held_keys"],
        )
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)

    def test_fourth_source_batch_adds_only_reviewed_closures_and_holds(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)

        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(
            set(classification["source_held_keys"]),
            (
                FIRST12_SOURCE_HELD_KEYS
                | NEXT12_SOURCE_HELD_KEYS
                | TOOL.THIRD12_SOURCE_HELD_KEYS
                | TOOL.FOURTH_SOURCE_HELD_KEYS
                | TOOL.FIFTH_SOURCE_HELD_KEYS
                | TOOL.SIXTH_SOURCE_HELD_KEYS
                | SEVENTH_SOURCE_HELD_KEYS
            )
            - OWNER_DECIDED_SOURCE_KEYS
            - FAMILIAR_SOURCE_CLOSED_KEYS
            - TENTH_SOURCE_CLOSED_KEYS
            - PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertNotIn(
            "source.spell.lesser_restoration.unresolved.multisource_condition_removal",
            {
                row["unresolved_key"]
                for row in manifest["source_fourth_resolution_evidence"]
            },
        )

    def test_fourth_source_resolution_rejects_cold_markdown_span_drift(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        read_pinned = TOOL._read_pinned_local_evidence

        def drift_markdown(
            relative_path: str, expected_sha256: str, evidence_name: str
        ) -> bytes:
            data = read_pinned(relative_path, expected_sha256, evidence_name)
            if relative_path == TOOL.SOURCE_MARKDOWN_RELATIVE_PATH:
                return data.replace(
                    b"audible up to 300 feet away", b"audible up to 301 feet away", 1
                )
            return data

        with (
            patch.object(
                TOOL, "_read_pinned_local_evidence", side_effect=drift_markdown
            ),
            self.assertRaises(TOOL.SourceQualificationError) as caught,
        ):
            TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(caught.exception.code, "source_fourth_markdown_span_hash")

    def test_fourth_source_resolution_rejects_a_missing_source_qualifier(self) -> None:
        assert TOOL is not None
        candidate = load_json(MANIFEST_PATH)
        knock = fourth_evidence_by_key_for(
            candidate, "source.spell.knock.unresolved.knock_sound_range"
        )
        knock["source_interpretation"] = "A sound emanates from the target."

        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_source_unknown_classifications(candidate)
        self.assertEqual(caught.exception.code, "source_fourth_qualifier")

    def test_fourth_source_resolution_rejects_a_foreign_source_pointer(self) -> None:
        assert TOOL is not None
        candidate = load_json(MANIFEST_PATH)
        row = fourth_evidence_by_key_for(
            candidate, "source.spell.knock.unresolved.knock_sound_range"
        )
        row["source_record_ref"]["json_pointer"] = (
            "/rows/79/required_modes_or_exceptions"
        )

        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_source_unknown_classifications(candidate)
        self.assertEqual(caught.exception.code, "source_fourth_provenance")

    def test_fourth_source_resolution_rejects_promotion_of_a_held_obligation(
        self,
    ) -> None:
        assert TOOL is not None
        candidate = load_json(MANIFEST_PATH)
        magic_missile = fourth_evidence_by_key_for(
            candidate, "source.spell.magic_missile.unresolved.rng_damage_grouping"
        )
        magic_missile["disposition"] = "SOURCE_CLOSED"

        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_source_unknown_classifications(candidate)
        self.assertEqual(caught.exception.code, "source_fourth_disposition")

    def test_fourth_common_summary_preserves_correct_trigger_and_class_list_rules(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        qualifiers = manifest["source_fourth_resolution_contract"]["common_qualifiers"]
        self.assertTrue(
            any(
                "A Reaction spell is cast in response to the trigger defined in its Casting Time entry."
                in qualifier
                and "Some Bonus Action spells" in qualifier
                for qualifier in qualifiers
            )
        )
        self.assertTrue(
            any(
                "Some features add a spell to a character’s spell list even if the character isn’t a member of a class in the parentheses."
                in qualifier
                for qualifier in qualifiers
            )
        )

        candidate = copy.deepcopy(manifest)
        candidate["source_fourth_resolution_contract"]["common_qualifiers"] = [
            qualifier
            for qualifier in candidate["source_fourth_resolution_contract"][
                "common_qualifiers"
            ]
            if "A Reaction spell is cast in response" not in qualifier
        ]
        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_source_unknown_classifications(candidate)
        self.assertEqual(caught.exception.code, "source_fourth_contract")

    def test_fourth_source_evidence_never_promotes_native_or_full_roster_readiness(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        contract = manifest["source_fourth_resolution_contract"]
        self.assertEqual(contract["future_native_proof_status"], "NOT_ESTABLISHED")
        self.assertEqual(
            contract["full_339_source_qualification_status"], "NOT_ESTABLISHED"
        )
        self.assertEqual(contract["production_claim"], "NONE")
        self.assertTrue(
            all(
                not row["actual_native_proof_refs"]
                for row in manifest["source_fourth_resolution_evidence"]
            )
        )
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])

    def test_fifth_source_batch_is_exact_and_remains_source_only(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        self.assertIn("source_fifth_resolution_evidence", manifest)
        evidence = manifest["source_fifth_resolution_evidence"]
        self.assertEqual(
            [
                (
                    row["review_item_id"],
                    row["unresolved_key"],
                    row["source_category"],
                    row["disposition"],
                )
                for row in evidence
            ],
            [
                (
                    "FIFTH-01",
                    "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
                    "source_parameter",
                    "SOURCE_HELD",
                ),
                (
                    "FIFTH-02",
                    "source.spell.message.unresolved.barrier_thresholds",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-03",
                    "source.spell.mirror_image.unresolved.qualifying_face_threshold",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-04",
                    "source.spell.moonbeam.unresolved.form_source_cleanup",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-05",
                    "source.spell.pass_without_trace.unresolved.selection_timing",
                    "source_semantics",
                    "SOURCE_HELD",
                ),
                (
                    "FIFTH-06A",
                    "source.spell.phantasmal_force.unresolved.dangerous_form_bounds",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-06B",
                    "source.spell.phantasmal_force.unresolved.dangerous_form_bounds",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-07",
                    "source.spell.prayer_of_healing.unresolved.responder_census",
                    "source_mapping_review",
                    "SOURCE_HELD",
                ),
                (
                    "FIFTH-08",
                    "source.spell.prestidigitation.unresolved.object_material_bounds",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-09",
                    "source.spell.protection_from_evil_and_good.unresolved.supernatural_source_members",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-10",
                    "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "FIFTH-11",
                    "source.spell.ray_of_frost.unresolved.movement_composition",
                    "source_parameter",
                    "SOURCE_HELD",
                ),
                (
                    "FIFTH-12",
                    "source.spell.resistance.unresolved.eleven_type_members",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
            ],
        )
        contract = manifest["source_fifth_resolution_contract"]
        self.assertEqual(
            contract["selected_original_classification_indexes"], list(range(56, 68))
        )
        self.assertEqual(contract["selected_source_closed_key_count"], 8)
        self.assertEqual(contract["selected_source_closed_subobligation_count"], 9)
        self.assertEqual(contract["selected_source_held_key_count"], 4)
        self.assertEqual(contract["selected_source_held_subobligation_count"], 4)
        self.assertEqual(contract["cumulative_source_closed_key_count"], 47)
        self.assertEqual(contract["cumulative_source_closed_subobligation_count"], 49)
        self.assertEqual(contract["cumulative_source_held_key_count"], 12)
        self.assertEqual(contract["cumulative_source_held_subobligation_count"], 12)
        self.assertEqual(contract["active_source_blocker_count"], 30)
        self.assertEqual(contract["active_source_blocker_entry_count"], 28)

        classification = TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(len(classification["source_held_keys"]), 6)
        self.assertEqual(
            set(classification["source_held_keys"]),
            (
                FIRST12_SOURCE_HELD_KEYS
                | NEXT12_SOURCE_HELD_KEYS
                | TOOL.THIRD12_SOURCE_HELD_KEYS
                | TOOL.FOURTH_SOURCE_HELD_KEYS
                | TOOL.FIFTH_SOURCE_HELD_KEYS
                | TOOL.SIXTH_SOURCE_HELD_KEYS
                | SEVENTH_SOURCE_HELD_KEYS
            )
            - OWNER_DECIDED_SOURCE_KEYS
            - FAMILIAR_SOURCE_CLOSED_KEYS
            - TENTH_SOURCE_CLOSED_KEYS
            - PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        self.assertEqual(
            classification["source_held_keys"][-1:],
            [
                "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
            ],
        )
        phantasmal_force = [
            row
            for row in evidence
            if row["unresolved_key"]
            == "source.spell.phantasmal_force.unresolved.dangerous_form_bounds"
        ]
        self.assertEqual(len(phantasmal_force), 2)
        self.assertEqual(
            {row["subobligation_id"].rsplit("::", 1)[-1] for row in phantasmal_force},
            {"source_parameter", "source_semantics"},
        )
        self.assertTrue(
            all(
                row["future_native_proof_status"] == "NOT_ESTABLISHED"
                and row["actual_native_proof_refs"] == []
                for row in evidence
            )
        )
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        self.assertNotEqual(receipt["status"], "W05_SPELL_SOURCE_QUALIFICATION_READY")

    def test_fifth_moonbeam_closure_does_not_claim_underlying_source_termination(
        self,
    ) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertIn("source_fifth_resolution_evidence", manifest)
        moonbeam = next(
            row
            for row in manifest["source_fifth_resolution_evidence"]
            if row["unresolved_key"]
            == "source.spell.moonbeam.unresolved.form_source_cleanup"
        )
        formulation = "\n".join(
            [
                moonbeam["source_interpretation"],
                *moonbeam["material_qualifiers"],
                moonbeam["retained_source_residual"],
            ]
        ).casefold()
        self.assertIn("reverts a shape-shifted creature to true form", formulation)
        self.assertIn("underlying transformation source", formulation)
        self.assertIn(
            "does not establish that the underlying transformation source terminates",
            formulation,
        )
        self.assertIn("no automatic reassertion", formulation)

    def test_fifth_source_batch_rejects_item_bound_cold_mutations(self) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)

        def fifth_evidence_for(
            candidate: dict[str, object], key: str, category: str | None = None
        ) -> dict[str, object]:
            rows = candidate["source_fifth_resolution_evidence"]
            return next(
                row
                for row in rows
                if row["unresolved_key"] == key
                and (category is None or row["source_category"] == category)
            )

        cases = (
            (
                "wrong-original-index-roster",
                lambda candidate: candidate["source_fifth_resolution_contract"].update(
                    {"selected_original_classification_indexes": list(range(55, 67))}
                ),
                "source_fifth_contract",
            ),
            (
                "substituted-index-68-key",
                lambda candidate: fifth_evidence_for(
                    candidate, "source.spell.resistance.unresolved.eleven_type_members"
                ).update({"unresolved_key": "source.spell.borrowed.unresolved.key"}),
                "source_fifth_census",
            ),
            (
                "wrong-subobligation-category",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.mirror_image.unresolved.qualifying_face_threshold",
                ).update({"source_category": "source_semantics"}),
                "source_fifth_census",
            ),
            (
                "borrowed-current-map-pointer",
                lambda candidate: fifth_evidence_for(
                    candidate, "source.spell.message.unresolved.barrier_thresholds"
                ).update(
                    {
                        "current_map_pointer": "/source_mapping_lanes/0/mapping_payload/entries/90"
                    }
                ),
                "source_fifth_binding",
            ),
            (
                "foreign-body-witness-hash",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
                )["source_record_ref"].update({"raw_body_sha256": "0" * 64}),
                "source_fifth_provenance",
            ),
            (
                "markdown-span-hash-drift",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.mirror_image.unresolved.qualifying_face_threshold",
                )["source_markdown_locators"][0].update({"span_sha256": "0" * 64}),
                "source_fifth_locator",
            ),
            (
                "enumerated-supernatural-type-omitted",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.protection_from_evil_and_good.unresolved.supernatural_source_members",
                )["members"].remove("Undead"),
                "source_fifth_enum",
            ),
            (
                "invented-resistance-type",
                lambda candidate: fifth_evidence_for(
                    candidate, "source.spell.resistance.unresolved.eleven_type_members"
                )["members"].append("Force"),
                "source_fifth_enum",
            ),
            (
                "promote-mending-hold",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
                ).update({"disposition": "SOURCE_CLOSED"}),
                "source_fifth_disposition",
            ),
            (
                "promote-ray-frost-hold",
                lambda candidate: fifth_evidence_for(
                    candidate,
                    "source.spell.ray_of_frost.unresolved.movement_composition",
                ).update({"disposition": "SOURCE_CLOSED"}),
                "source_fifth_disposition",
            ),
            (
                "drop-future-proof-residual",
                lambda candidate: fifth_evidence_for(
                    candidate, "source.spell.moonbeam.unresolved.form_source_cleanup"
                ).update(
                    {
                        "retained_source_residual": "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY;"
                    }
                ),
                "source_fifth_qualifier",
            ),
            (
                "close-underlying-moonbeam-source",
                lambda candidate: fifth_evidence_for(
                    candidate, "source.spell.moonbeam.unresolved.form_source_cleanup"
                ).update(
                    {
                        "source_interpretation": "Moonbeam terminates the underlying transformation source."
                    }
                ),
                "source_fifth_formulation",
            ),
        )
        for case, mutate, expected_code in cases:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=case):
                mutate(candidate)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(caught.exception.code, expected_code)

    def test_fifth_source_resolution_rejects_cold_markdown_span_drift(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        read_pinned = TOOL._read_pinned_local_evidence

        def drift_markdown(
            relative_path: str, expected_sha256: str, evidence_name: str
        ) -> bytes:
            data = read_pinned(relative_path, expected_sha256, evidence_name)
            if relative_path == TOOL.SOURCE_MARKDOWN_RELATIVE_PATH:
                return data.replace(
                    b"5-foot-radius, 40-foot-high Cylinder",
                    b"6-foot-radius, 40-foot-high Cylinder",
                    1,
                )
            return data

        with (
            patch.object(
                TOOL, "_read_pinned_local_evidence", side_effect=drift_markdown
            ),
            self.assertRaises(TOOL.SourceQualificationError) as caught,
        ):
            TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(caught.exception.code, "source_fifth_markdown_span_hash")

    def test_fifth_source_resolution_rejects_frozen_provenance_hash_drift(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        for field in (
            "candidate_sha256",
            "accepted_review_sha256",
            "task_evidence_sha256",
        ):
            with self.subTest(field=field):
                candidate = copy.deepcopy(baseline)
                candidate["source_fifth_review"][field] = "0" * 64
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(caught.exception.code, "source_fifth_review")

    def test_fifth_source_evidence_preserves_preexisting_holds_and_future_proof(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)
        expected_prior_holds = (
            FIRST12_SOURCE_HELD_KEYS
            | NEXT12_SOURCE_HELD_KEYS
            | TOOL.THIRD12_SOURCE_HELD_KEYS
            | TOOL.FOURTH_SOURCE_HELD_KEYS
        )
        self.assertTrue(
            (
                expected_prior_holds
                - OWNER_DECIDED_SOURCE_KEYS
                - TENTH_SOURCE_CLOSED_KEYS
            ).issubset(set(classification["source_held_keys"]))
        )
        future = [
            subobligation
            for row in manifest["source_unknown_classifications"]
            for subobligation in row["subobligations"]
            if subobligation["category"]
            == "downstream_domain_consumer_admission_native_proof"
        ]
        self.assertEqual(len(future), 33)
        self.assertTrue(
            all(
                subobligation["gate_phase"] == "FUTURE_PROOF"
                and subobligation["status"] == "NOT_ESTABLISHED"
                for subobligation in future
            )
        )
        self.assertEqual(
            manifest["source_fifth_resolution_contract"]["future_native_proof_status"],
            "NOT_ESTABLISHED",
        )
        self.assertEqual(
            manifest["source_fifth_resolution_contract"][
                "full_339_source_qualification_status"
            ],
            "NOT_ESTABLISHED",
        )

    def test_seventh_source_batch_is_included_in_cumulative_accounting(self) -> None:
        assert TOOL is not None
        classification = TOOL._validate_source_unknown_classifications(
            load_json(MANIFEST_PATH)
        )

        self.assertEqual(classification["source_reviewed_key_count"], 77)

    def test_sixth_source_batch_is_exact_and_remains_source_only(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_manifest_schema(manifest)
        evidence = manifest["source_sixth_resolution_evidence"]
        self.assertEqual(
            [
                (
                    row["review_item_id"],
                    row["unresolved_key"],
                    row["source_category"],
                    row["disposition"],
                )
                for row in evidence
            ],
            [
                (
                    "SIXTH-01",
                    "source.spell.resistance.unresolved.damage_grouping_order",
                    "source_semantics",
                    "SOURCE_HELD",
                ),
                (
                    "SIXTH-02",
                    "source.spell.rope_trick.unresolved.boundary_location_profile",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-03",
                    "source.spell.sanctuary.unresolved.retarget_cost_chain",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-04",
                    "source.spell.scorching_ray.unresolved.target_kind_policy",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-05",
                    "source.spell.sorcerous_burst.unresolved.permitted_type_members",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-06",
                    "source.spell.spare_the_dying.unresolved.range_thresholds",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-07",
                    "source.spell.speak_with_animals.unresolved.influence_option_census",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-08",
                    "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
                    "source_parameter",
                    "SOURCE_HELD",
                ),
                (
                    "SIXTH-09A",
                    "source.spell.suggestion.unresolved.agency_and_word_limit",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-09B",
                    "source.spell.suggestion.unresolved.agency_and_word_limit",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-10",
                    "source.spell.thaumaturgy.unresolved.exact_mode_bounds",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SIXTH-11A",
                    "source.spell.unseen_servant.unresolved.subject_health_classification",
                    "source_semantics",
                    "SOURCE_HELD",
                ),
                (
                    "SIXTH-11B",
                    "source.spell.unseen_servant.unresolved.force_numeric_profile",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
            ],
        )
        result = TOOL._validate_source_unknown_classifications(manifest)
        contract = manifest["source_sixth_resolution_contract"]
        self.assertEqual(contract["selected_key_count"], 12)
        self.assertEqual(contract["resolution_record_count"], 13)
        self.assertEqual(contract["selected_source_closed_key_count"], 9)
        self.assertEqual(contract["selected_source_closed_subobligation_count"], 10)
        self.assertEqual(contract["selected_source_held_key_count"], 3)
        self.assertEqual(contract["selected_source_held_subobligation_count"], 3)
        self.assertEqual(result["source_reviewed_key_count"], 77)
        self.assertEqual(len(result["source_resolution_evidence"]), 92)
        self.assertEqual(result["source_resolved_subobligation_count"], 75)
        self.assertEqual(result["source_held_subobligation_count"], 6)
        self.assertEqual(result["source_blocking_key_count"], 6)
        self.assertEqual(result["future_proof_subobligation_count"], 33)
        self.assertEqual(contract["future_native_proof_status"], "NOT_ESTABLISHED")
        self.assertEqual(
            contract["full_339_source_qualification_status"], "NOT_ESTABLISHED"
        )
        self.assertEqual(contract["production_claim"], "NONE")

    def test_sixth_source_batch_preserves_holds_and_exact_wording_corrections(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        result = TOOL._validate_source_unknown_classifications(manifest)
        sixth = manifest["source_sixth_resolution_evidence"]
        by_key_category = {
            (row["unresolved_key"], row["source_category"]): row for row in sixth
        }
        old_holds = (
            FIRST12_SOURCE_HELD_KEYS
            | NEXT12_SOURCE_HELD_KEYS
            | TOOL.THIRD12_SOURCE_HELD_KEYS
            | TOOL.FOURTH_SOURCE_HELD_KEYS
            | TOOL.FIFTH_SOURCE_HELD_KEYS
        )
        self.assertTrue(
            (
                old_holds
                - OWNER_DECIDED_SOURCE_KEYS
                - TENTH_SOURCE_CLOSED_KEYS
                - PRAYER_OWNER_DECIDED_SOURCE_KEYS
            ).issubset(set(result["source_held_keys"]))
        )
        self.assertEqual(
            by_key_category[
                (
                    "source.spell.resistance.unresolved.damage_grouping_order",
                    "source_semantics",
                )
            ]["disposition"],
            "SOURCE_HELD",
        )
        self.assertEqual(
            by_key_category[
                (
                    "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
                    "source_parameter",
                )
            ]["disposition"],
            "SOURCE_HELD",
        )
        self.assertEqual(
            by_key_category[
                (
                    "source.spell.unseen_servant.unresolved.subject_health_classification",
                    "source_semantics",
                )
            ]["disposition"],
            "SOURCE_HELD",
        )
        suggestion = by_key_category[
            (
                "source.spell.suggestion.unresolved.agency_and_word_limit",
                "source_semantics",
            )
        ]
        suggestion_text = "\n".join(
            [suggestion["source_interpretation"], *suggestion["material_qualifiers"]]
        )
        self.assertIn(
            "cannot attack the charmer or target the charmer with damaging abilities or magical effects",
            suggestion_text,
        )
        self.assertNotIn("prevents harm to charmer", suggestion_text)
        concentration_text = "\n".join(
            manifest["source_sixth_resolution_contract"]["common_qualifiers"]
        )
        self.assertIn(
            "the moment the creator starts casting another spell requiring Concentration",
            concentration_text,
        )
        self.assertNotIn("completed Concentration spell", concentration_text)
        self.assertEqual(len(result["future_proof_subobligations"]), 33)
        self.assertTrue(
            all(
                row["status"] == "NOT_ESTABLISHED"
                and row["gate_phase"] == "FUTURE_PROOF"
                for row in result["future_proof_subobligations"]
            )
        )

    def test_sixth_resistance_type_choice_is_bound_to_the_caster(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        resistance = next(
            row
            for row in manifest["source_sixth_resolution_evidence"]
            if row["unresolved_key"]
            == "source.spell.resistance.unresolved.damage_grouping_order"
        )

        self.assertEqual(
            resistance["source_interpretation"],
            "The caster touches a willing creature and chooses one of the exact eleven source-listed damage types. Before the spell ends, damage of the chosen type reduces the willing creature's total damage taken by 1d4, once per turn.",
        )
        result = TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(resistance["disposition"], "SOURCE_HELD")
        self.assertNotIn(
            "source.spell.resistance.unresolved.damage_grouping_order",
            result["source_held_keys"],
        )
        self.assertEqual(
            owner_decision_evidence_by_key_for(
                manifest,
                "source.spell.resistance.unresolved.damage_grouping_order",
            )["disposition"],
            "OWNER_DECIDED",
        )

    def test_sixth_source_batch_rejects_cold_pointer_hash_hold_and_promotion_mutations(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejected = load_json(REJECTED_PATH)["sixth_rejections"]

        def sixth_row(
            manifest: dict[str, object], key: str, category: str | None = None
        ) -> dict[str, object]:
            rows = manifest["source_sixth_resolution_evidence"]
            return next(
                row
                for row in rows
                if row["unresolved_key"] == key
                and (category is None or row["source_category"] == category)
            )

        def apply_mutation(
            candidate: dict[str, object], rejection: dict[str, object]
        ) -> None:
            mutation = rejection["mutation"]
            if mutation == "review_field":
                candidate["source_sixth_review"][rejection["field"]] = rejection[
                    "value"
                ]
            elif mutation in {
                "evidence_field",
                "source_record_field",
                "span_hash",
                "disposition",
                "append_material_qualifier",
                "source_interpretation",
            }:
                row = sixth_row(
                    candidate,
                    rejection["unresolved_key"],
                    rejection.get("source_category"),
                )
                if mutation == "evidence_field":
                    row[rejection["field"]] = rejection["value"]
                elif mutation == "source_record_field":
                    row["source_record_ref"][rejection["field"]] = rejection["value"]
                elif mutation == "span_hash":
                    row["source_markdown_locators"][rejection["locator_index"]][
                        "span_sha256"
                    ] = rejection["value"]
                elif mutation == "disposition":
                    row["disposition"] = rejection["value"]
                elif mutation == "source_interpretation":
                    row["source_interpretation"] = rejection["value"]
                else:
                    row["material_qualifiers"].append(rejection["value"])
            elif mutation == "subobligation_field":
                classification = next(
                    row
                    for row in candidate["source_unknown_classifications"]
                    if row["unresolved_key"] == rejection["unresolved_key"]
                )
                subobligation = next(
                    row
                    for row in classification["subobligations"]
                    if row["category"] == rejection["category"]
                )
                subobligation[rejection["field"]] = rejection["value"]
            elif mutation == "replace_common_qualifier":
                candidate["source_sixth_resolution_contract"]["common_qualifiers"][
                    rejection["index"]
                ] = rejection["value"]
            else:
                raise AssertionError(f"unknown sixth rejection mutation: {mutation}")

        self.assertEqual(len({case["case_id"] for case in rejected}), len(rejected))
        for rejection in rejected:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=rejection["case_id"]):
                apply_mutation(candidate, rejection)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )

    def test_seventh_source_batch_is_exact_and_remains_source_only(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_manifest_schema(manifest)
        evidence = manifest["source_seventh_resolution_evidence"]
        self.assertEqual(
            [
                (
                    row["review_item_id"],
                    row["unresolved_key"],
                    row["source_category"],
                    row["disposition"],
                )
                for row in evidence
            ],
            [
                (
                    "SEVENTH-01",
                    "source.spell.augury.unresolved.four_omen_members",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SEVENTH-02",
                    "source.spell.find_familiar.unresolved.eligible_form_census",
                    "source_mapping_review",
                    "SOURCE_HELD",
                ),
                (
                    "SEVENTH-03",
                    "source.spell.find_steed.unresolved.type_to_action_mapping",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SEVENTH-04A",
                    "source.spell.find_steed.unresolved.steed_numeric_cells",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "SEVENTH-04B",
                    "source.spell.find_steed.unresolved.steed_numeric_cells",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "SEVENTH-05",
                    "source.spell.warding_bond.unresolved.copied_damage_policy",
                    "source_semantics",
                    "SOURCE_HELD",
                ),
                (
                    "SEVENTH-06",
                    "source.spell.web.unresolved.web_numeric_geometry",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
            ],
        )

        classification = TOOL._validate_source_unknown_classifications(manifest)
        contract = manifest["source_seventh_resolution_contract"]
        self.assertEqual(
            contract["selected_original_classification_indexes"],
            [6, 30, 31, 32, 80, 81],
        )
        self.assertEqual(contract["selected_key_count"], 6)
        self.assertEqual(contract["selected_spell_count"], 5)
        self.assertEqual(contract["resolution_record_count"], 7)
        self.assertEqual(contract["selected_source_closed_key_count"], 4)
        self.assertEqual(contract["selected_source_closed_subobligation_count"], 5)
        self.assertEqual(contract["selected_source_held_key_count"], 2)
        self.assertEqual(contract["selected_source_held_subobligation_count"], 2)
        self.assertEqual(contract["cumulative_reviewed_key_count"], 77)
        self.assertEqual(contract["cumulative_resolution_record_count"], 81)
        self.assertEqual(contract["cumulative_source_closed_key_count"], 60)
        self.assertEqual(contract["cumulative_source_closed_subobligation_count"], 64)
        self.assertEqual(contract["cumulative_source_held_key_count"], 17)
        self.assertEqual(contract["cumulative_source_held_subobligation_count"], 17)
        self.assertEqual(contract["active_source_blocker_count"], 17)
        self.assertEqual(contract["active_source_blocker_entry_count"], 17)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(len(set(classification["source_resolved_keys"])), 71)
        self.assertTrue(
            SEVENTH_SOURCE_CLOSED_KEYS.isdisjoint(
                set(classification["source_blocking_keys"])
            )
        )
        self.assertTrue(
            FAMILIAR_SOURCE_CLOSED_KEYS.issubset(
                set(classification["source_resolved_keys"])
            )
        )
        self.assertTrue(
            FAMILIAR_SOURCE_CLOSED_KEYS.isdisjoint(
                set(classification["source_held_keys"])
            )
        )
        self.assertEqual(contract["future_native_proof_status"], "NOT_ESTABLISHED")
        self.assertEqual(
            contract["full_339_source_qualification_status"], "NOT_ESTABLISHED"
        )
        self.assertEqual(contract["production_claim"], "NONE")

    def test_familiar_census_closes_only_its_source_obligation(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)

        classification = TOOL._validate_source_unknown_classifications(manifest)

        self.assertEqual(classification["source_resolved_key_count"], 71)
        self.assertEqual(classification["source_closed_key_count"], 64)
        self.assertEqual(classification["source_owner_decided_key_count"], 7)
        self.assertEqual(classification["source_held_key_count"], 6)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["future_proof_subobligation_count"], 33)
        self.assertEqual(
            classification["source_blocking_keys"],
            [
                "source.spell.arcane_lock.unresolved.destruction_access_policy",
                "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
                "source.spell.detect_magic.unresolved.aura_overlay_policy",
                "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                "source.spell.magic_mouth.unresolved.trigger_episode_frequency",
                "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
            ],
        )

        historical_hold = seventh_evidence_by_key_category_for(
            manifest,
            "source.spell.find_familiar.unresolved.eligible_form_census",
            "source_mapping_review",
        )
        self.assertEqual(historical_hold["disposition"], "SOURCE_HELD")
        self.assertEqual(
            manifest["source_eighth_resolution_contract"][
                "cumulative_source_resolved_key_count"
            ],
            66,
        )
        self.assertEqual(
            manifest["source_eighth_resolution_contract"][
                "active_source_blocker_count"
            ],
            11,
        )
        self.assertEqual(
            set(OWNER_DECIDED_SOURCE_KEYS),
            {
                row["unresolved_key"]
                for row in manifest["source_eighth_resolution_evidence"]
            },
        )
        self.assertEqual(
            manifest["source_interpretation_owner"]["decision_sha256"],
            "9de384b36657bafe7e93252959825ed4ba4494f287ee972904d589f5c8759e5c",
        )

        census = TOOL._validate_source_familiar_census_evidence(manifest)
        self.assertEqual(census["eligible_form_count"], 24)
        self.assertEqual(census["named_example_count"], 11)
        self.assertEqual(census["additional_form_count"], 13)
        self.assertEqual(census["blocked_attack_count"], 23)
        self.assertEqual(census["general_nonattack_action_count"], 11)
        self.assertEqual(census["source_prerequisite_root_count"], 37)
        self.assertEqual(census["source_prerequisite_reference_count"], 151)
        self.assertEqual(census["new_source_clause_count"], 33)
        self.assertEqual(census["parameterized_input_category_count"], 5)
        self.assertEqual(census["native_consumer_admission_status"], "NOT_ESTABLISHED")
        self.assertTrue(
            all(
                row["status"] == "NOT_ESTABLISHED"
                and row["gate_phase"] == "FUTURE_PROOF"
                for row in classification["future_proof_subobligations"]
            )
        )
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        self.assertEqual(
            next(
                row
                for row in receipt["source_ready_gate"]["blockers"]
                if row["code"] == "UNRESOLVED_SOURCE_KEYS"
            )["count"],
            6,
        )
        self.assertEqual(
            [row["source_exact_name"] for row in receipt["source_modeling_residuals"]],
            ["Word of Recall"],
        )
        self.assertTrue(
            TOOL._familiar_source_form_matches_predicate(
                {"creature_type": "Beast", "challenge_rating": "0", "swarm": True}
            )
        )
        self.assertFalse(
            TOOL._familiar_source_form_matches_predicate(
                {"creature_type": "Beast", "challenge_rating": "1/8", "swarm": False}
            )
        )

    def test_familiar_source_census_rejects_cold_identity_and_scope_mutations(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejected = load_json(REJECTED_PATH)["familiar_source_rejections"]
        pinned_reader = TOOL._read_pinned_local_evidence

        def alter_fixture(
            payload: dict[str, object], rejection: dict[str, object]
        ) -> None:
            target = rejection["target"]
            mutation = rejection["mutation"]
            if target == "census_fixture":
                forms = payload["eligible_forms"]
                if mutation == "remove_form":
                    forms[:] = [
                        row for row in forms if row["name"] != rejection["name"]
                    ]
                elif mutation == "change_form_field":
                    next(row for row in forms if row["name"] == rejection["name"])[
                        rejection["field"]
                    ] = rejection["value"]
                elif mutation == "change_eligibility_predicate":
                    payload["eligibility_predicate"][rejection["field"]] = rejection[
                        "value"
                    ]
                elif mutation == "change_span_start":
                    next(row for row in forms if row["name"] == rejection["name"])[
                        "span"
                    ]["line_start"] = rejection["value"]
                elif mutation == "change_span_digest":
                    next(row for row in forms if row["name"] == rejection["name"])[
                        "span"
                    ]["raw_utf8_sha256"] = rejection["value"]
                elif mutation == "change_form_option_field":
                    next(
                        row
                        for row in payload["nonattack_form_options"]
                        if row["name"] == rejection["name"]
                    )[rejection["field"]] = rejection["value"]
                elif mutation == "remove_attack_only_trait":
                    payload["attack_only_traits"].remove(rejection["value"])
                else:
                    raise AssertionError(f"unknown census-fixture mutation: {mutation}")
            elif target == "prerequisites_fixture":
                if mutation == "remove_root":
                    payload["review_register_roots"][:] = [
                        row
                        for row in payload["review_register_roots"]
                        if row[0] != rejection["value"]
                    ]
                elif mutation == "remove_source_clause":
                    payload["new_source_clauses"][:] = [
                        row
                        for row in payload["new_source_clauses"]
                        if row[0] != rejection["value"]
                    ]
                elif mutation == "help_first_aid_field":
                    payload["help_first_aid"][rejection["field"]] = rejection["value"]
                elif mutation == "remove_parameterized_input":
                    payload["parameterized_input_categories"][:] = [
                        row
                        for row in payload["parameterized_input_categories"]
                        if row[0] != rejection["value"]
                    ]
                else:
                    raise AssertionError(
                        f"unknown prerequisites-fixture mutation: {mutation}"
                    )
            else:
                raise AssertionError(f"unknown fixture target: {target}")

        def apply_manifest_mutation(
            candidate: dict[str, object], rejection: dict[str, object]
        ) -> None:
            target = rejection["target"]
            mutation = rejection["mutation"]
            if target == "manifest_review":
                candidate["source_ninth_review"][rejection["field"]] = rejection[
                    "value"
                ]
            elif target == "manifest_contract":
                candidate["source_ninth_resolution_contract"][rejection["field"]] = (
                    rejection["value"]
                )
            elif target == "manifest_evidence":
                row = candidate["source_ninth_resolution_evidence"][0]
                if mutation in {"add_evidence_field", "evidence_field"}:
                    row[rejection["field"]] = rejection["value"]
                else:
                    raise AssertionError(
                        f"unknown manifest-evidence mutation: {mutation}"
                    )
            elif target == "manifest_current_map":
                candidate["source_mapping_lanes"][0]["mapping_payload"]["entries"][48][
                    rejection["field"]
                ] = rejection["value"]
            elif target == "classification_future_proof":
                classification = next(
                    row
                    for row in candidate["source_unknown_classifications"]
                    if row["unresolved_key"]
                    == "source.spell.find_familiar.unresolved.eligible_form_census"
                )
                subobligation = next(
                    row
                    for row in classification["subobligations"]
                    if row["category"] == rejection["category"]
                )
                subobligation[rejection["field"]] = rejection["value"]
            else:
                raise AssertionError(f"unknown manifest target: {target}")

        self.assertGreaterEqual(len(rejected), 10)
        for rejection in rejected:
            candidate = copy.deepcopy(baseline)
            target = rejection["target"]
            with self.subTest(case=rejection["case_id"]):
                if target in {
                    "manifest_review",
                    "manifest_contract",
                    "manifest_evidence",
                    "manifest_current_map",
                    "classification_future_proof",
                }:
                    apply_manifest_mutation(candidate, rejection)
                    with self.assertRaises(TOOL.SourceQualificationError) as caught:
                        TOOL._validate_source_unknown_classifications(candidate)
                else:
                    fixture_path = (
                        TOOL.FAMILIAR_CENSUS_FIXTURE_PATH
                        if target == "census_fixture"
                        else TOOL.FAMILIAR_PREREQUISITES_FIXTURE_PATH
                    )

                    def altered_reader(
                        relative_path: str,
                        expected_sha256: str,
                        evidence_name: str,
                        *,
                        expected_fixture_path: str = fixture_path,
                        rejection_case: dict[str, object] = rejection,
                    ) -> bytes:
                        data = pinned_reader(
                            relative_path, expected_sha256, evidence_name
                        )
                        if relative_path != expected_fixture_path:
                            return data
                        fixture_data = json.loads(data.decode("utf-8"))
                        alter_fixture(fixture_data, rejection_case)
                        return json.dumps(
                            fixture_data,
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ).encode("utf-8")

                    with (
                        patch.object(
                            TOOL,
                            "_read_pinned_local_evidence",
                            side_effect=altered_reader,
                        ),
                        self.assertRaises(TOOL.SourceQualificationError) as caught,
                    ):
                        TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )

    def test_familiar_prerequisite_carrier_is_complete_without_external_reads(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        original_open = Path.open

        def local_only_open(path: Path, *args: object, **kwargs: object) -> object:
            resolved = path.resolve()
            if not resolved.is_relative_to(TOOL.REPOSITORY_ROOT):
                raise AssertionError(f"external evidence read is forbidden: {resolved}")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", new=local_only_open):
            carrier = load_json(
                ROOT / "DEV/TESTS/fixtures/spell-familiar-source-prerequisites.json"
            )
            self.assertIn(
                "source_reference_tuples", carrier, "complete durable rows missing"
            )
            result = TOOL._validate_source_familiar_census_evidence(manifest)

        self.assertEqual(result["source_prerequisite_root_count"], 37)
        self.assertEqual(result["source_prerequisite_reference_count"], 151)
        self.assertIn("entries", carrier)
        self.assertEqual(len(carrier["entries"]), 37)
        reference_rows = carrier["source_reference_tuples"]
        self.assertEqual(len(reference_rows), 151)
        self.assertEqual(
            sum(len(entry["source_refs"]) for entry in carrier["entries"]),
            151,
        )
        self.assertEqual(
            carrier["source_reference_tuples"],
            [
                [
                    entry["prerequisite_id"],
                    ref["collection"],
                    ref.get("index"),
                    ref["line_start"],
                    ref["line_end"],
                    ref["raw_utf8_sha256"],
                ]
                for entry in carrier["entries"]
                for ref in entry["source_refs"]
            ],
        )
        self.assertEqual(
            sum(len(entry["member_body_refs"]) for entry in carrier["entries"]),
            673,
        )
        self.assertTrue(
            all(
                entry["subject_role"]
                and entry["predicates_and_outcomes"]
                and entry["permitted_conditional_contexts"]
                and entry["non_goals"]
                for entry in carrier["entries"]
            )
        )

    def test_familiar_durable_ledger_rejects_item_level_loss_and_grants(self) -> None:
        assert TOOL is not None
        census = load_json(ROOT / TOOL.FAMILIAR_CENSUS_FIXTURE_PATH)
        carrier = load_json(ROOT / TOOL.FAMILIAR_PREREQUISITES_FIXTURE_PATH)
        lines = (
            (ROOT / TOOL.SOURCE_MARKDOWN_RELATIVE_PATH)
            .read_text(encoding="utf-8")
            .splitlines(keepends=True)
        )
        self.assertTrue(hasattr(TOOL, "_validate_familiar_prerequisite_ledger"))
        TOOL._validate_familiar_prerequisite_ledger(carrier, census, lines)
        cases = (
            (
                "missing_reference",
                lambda p: p["entries"][0]["source_refs"].pop(),
                "source_familiar_reference_digest",
            ),
            (
                "swapped_reference",
                lambda p: p["entries"][0]["source_refs"].__setitem__(
                    0, p["entries"][1]["source_refs"][0]
                ),
                "source_familiar_reference_digest",
            ),
            (
                "wrong_member_index",
                lambda p: p["entries"][0]["member_body_refs"][0].__setitem__(
                    "record_index", 240
                ),
                "source_familiar_member_join",
            ),
            (
                "missing_applicability",
                lambda p: p["entries"][15]["applicable_member_source_keys"].pop(),
                "source_familiar_member_join",
            ),
            (
                "missing_condition",
                lambda p: p["entries"][28]["predicates_and_outcomes"].pop(),
                "source_familiar_prerequisite_semantics",
            ),
            (
                "missing_context",
                lambda p: p["entries"][35]["permitted_conditional_contexts"].pop(),
                "source_familiar_prerequisite_schema",
            ),
            (
                "missing_non_goal",
                lambda p: p["entries"][36]["non_goals"].pop(),
                "source_familiar_prerequisite_semantics",
            ),
            (
                "fabricated_grant",
                lambda p: p["entries"][10]["predicates_and_outcomes"].append(
                    "All familiars can cast spells."
                ),
                "source_familiar_prerequisite_semantics",
            ),
            (
                "wrong_subject",
                lambda p: p["entries"][36].__setitem__(
                    "subject_role", "FAMILIAR_OR_APPLICABLE_OTHER_CREATURE"
                ),
                "source_familiar_prerequisite_semantics",
            ),
            (
                "missing_input_qualification",
                lambda p: p["parameterized_inputs"][0].pop("qualification"),
                "source_familiar_prerequisite_semantics",
            ),
            (
                "unowned_field",
                lambda p: p["entries"][0].__setitem__("executor_grant", True),
                "source_familiar_prerequisite_schema",
            ),
        )
        for name, mutate, code in cases:
            with self.subTest(case=name):
                candidate = copy.deepcopy(carrier)
                mutate(candidate)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_familiar_prerequisite_ledger(
                        candidate, census, lines
                    )
                self.assertEqual(caught.exception.code, code)

    def test_familiar_evidence_producer_identity_shape_and_duplicate_keys(self) -> None:
        path = ROOT / "DEV/TOOLS/build_spell_familiar_source_evidence.py"
        self.assertTrue(path.is_file(), "missing repository-owned evidence producer")
        spec = importlib.util.spec_from_file_location(
            "familiar_evidence_producer", path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            module.decode_json(b'{"a":1,"a":2}')
        with self.assertRaisesRegex(ValueError, "identity"):
            module.load_accepted_input(MANIFEST_PATH, "0" * 64)
        with self.assertRaisesRegex(ValueError, "shape"):
            module.closed_object({"extra": 1}, {"expected"}, "probe")

    def test_familiar_cold_carriers_are_required_and_source_drift_is_rejected(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        original = Path.read_bytes
        for relative, code in (
            (
                TOOL.FAMILIAR_CENSUS_FIXTURE_PATH,
                "source_familiar_census_fixture_identity",
            ),
            (
                TOOL.FAMILIAR_PREREQUISITES_FIXTURE_PATH,
                "source_familiar_prerequisites_fixture_identity",
            ),
        ):
            target = ROOT / relative

            def missing(path: Path, *, missing_path: Path = target) -> bytes:
                if path == missing_path:
                    raise FileNotFoundError(missing_path)
                return original(path)

            with (
                self.subTest(path=relative),
                patch.object(Path, "read_bytes", new=missing),
            ):
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_familiar_census_evidence(manifest)
                self.assertEqual(caught.exception.code, code)
        census = load_json(ROOT / TOOL.FAMILIAR_CENSUS_FIXTURE_PATH)
        carrier = load_json(ROOT / TOOL.FAMILIAR_PREREQUISITES_FIXTURE_PATH)
        lines = (
            (ROOT / TOOL.SOURCE_MARKDOWN_RELATIVE_PATH)
            .read_text(encoding="utf-8")
            .splitlines(keepends=True)
        )
        lines[602] += "fabricated source grant"
        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_familiar_prerequisite_ledger(carrier, census, lines)
        self.assertEqual(caught.exception.code, "source_familiar_reference_join")

    def test_seventh_source_qualifiers_preserve_holds_and_separate_residuals(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)
        rows = {
            (row["unresolved_key"], row["source_category"]): row
            for row in manifest["source_seventh_resolution_evidence"]
        }
        familiar = rows[
            (
                "source.spell.find_familiar.unresolved.eligible_form_census",
                "source_mapping_review",
            )
        ]
        self.assertEqual(familiar["disposition"], "SOURCE_HELD")
        self.assertIn("Bat, Cat, Frog", familiar["source_interpretation"])
        self.assertIn(
            "another Beast that has a Challenge Rating of 0",
            familiar["source_interpretation"],
        )
        familiar_qualifiers = "\n".join(familiar["material_qualifiers"])
        self.assertIn("not the complete eligible-form census", familiar_qualifiers)
        self.assertTrue(
            "100-foot predicates are specific to telepathy and touch delivery"
            in familiar_qualifiers
        )
        self.assertIn(
            "Touch delivery uses the familiar's Reaction", familiar_qualifiers
        )
        self.assertIn(
            "Gear is left on zero HP or pocket disappearance, not every dismissal.",
            familiar_qualifiers,
        )

        steed_mapping = rows[
            (
                "source.spell.find_steed.unresolved.type_to_action_mapping",
                "source_mapping_review",
            )
        ]
        self.assertIn("Fiend → Fell Glare", steed_mapping["source_interpretation"])
        self.assertIn("Fey → Fey Step", steed_mapping["source_interpretation"])
        self.assertIn(
            "Celestial → Healing Touch", steed_mapping["source_interpretation"]
        )
        self.assertIn(
            "No action availability is inferred in every mount state from the type/action mapping.",
            steed_mapping["material_qualifiers"],
        )
        self.assertIn(
            "The absence of a rider does not categorically forbid Fey Step.",
            steed_mapping["material_qualifiers"],
        )
        steed_numbers = rows[
            (
                "source.spell.find_steed.unresolved.steed_numeric_cells",
                "source_parameter",
            )
        ]
        self.assertIn("10 + 1 per spell level", steed_numbers["source_interpretation"])
        self.assertIn("5 + 10 per spell level", steed_numbers["source_interpretation"])
        self.assertIn("Int 6/−2/−2", steed_numbers["source_interpretation"])
        self.assertIn(
            "Fly 60 feet only with a level 4+ spell",
            steed_numbers["source_interpretation"],
        )

        bond = rows[
            (
                "source.spell.warding_bond.unresolved.copied_damage_policy",
                "source_semantics",
            )
        ]
        self.assertEqual(bond["disposition"], "SOURCE_HELD")
        self.assertIn(
            "or the spell is cast again on either connected creature.",
            bond["source_interpretation"],
        )
        self.assertIn(
            "reciprocal/recursive bond default", "\n".join(bond["material_qualifiers"])
        )
        self.assertIn(
            "Warding Bond itself is not a Concentration spell.",
            bond["material_qualifiers"],
        )

        web = rows[
            (
                "source.spell.web.unresolved.web_numeric_geometry",
                "source_parameter",
            )
        ]
        self.assertIn("20-foot Cube", web["source_interpretation"])
        self.assertIn("two solid masses", web["source_interpretation"])
        self.assertIn("2d4 Fire", web["source_interpretation"])
        web_qualifiers = "\n".join(web["material_qualifiers"])
        self.assertIn("Cube origin can be anywhere on a face.", web_qualifiers)
        self.assertIn(
            "Cube origin is excluded unless the creator chooses otherwise.",
            web_qualifiers,
        )
        self.assertIn(
            "The Cube is not assumed centered on its origin point.", web_qualifiers
        )
        self.assertIn(
            "Restrained sets Speed to 0 and affects attacks and Dexterity saves.",
            web_qualifiers,
        )

        old_holds = (
            FIRST12_SOURCE_HELD_KEYS
            | NEXT12_SOURCE_HELD_KEYS
            | TOOL.THIRD12_SOURCE_HELD_KEYS
            | TOOL.FOURTH_SOURCE_HELD_KEYS
            | TOOL.FIFTH_SOURCE_HELD_KEYS
            | TOOL.SIXTH_SOURCE_HELD_KEYS
        )
        self.assertEqual(
            set(classification["source_held_keys"]),
            (old_holds | SEVENTH_SOURCE_HELD_KEYS)
            - OWNER_DECIDED_SOURCE_KEYS
            - FAMILIAR_SOURCE_CLOSED_KEYS
            - TENTH_SOURCE_CLOSED_KEYS
            - PRAYER_OWNER_DECIDED_SOURCE_KEYS,
        )
        future = [
            subobligation
            for row in manifest["source_unknown_classifications"]
            for subobligation in row["subobligations"]
            if subobligation["category"]
            == "downstream_domain_consumer_admission_native_proof"
        ]
        self.assertEqual(len(future), 33)
        self.assertTrue(
            all(
                row["status"] == "NOT_ESTABLISHED"
                and row["gate_phase"] == "FUTURE_PROOF"
                for row in future
            )
        )
        self.assertEqual(
            manifest["content_owner_default_repair"]["status"],
            "REQUIRED_BEFORE_PACKAGE_PROMOTION",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["source_exact_name"],
            "Word of Recall",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["status"], "NOT_ESTABLISHED"
        )

    def test_seventh_steed_life_bond_uses_actual_caster_regain(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_source_unknown_classifications(manifest)
        life_bond = seventh_evidence_by_key_category_for(
            manifest,
            "source.spell.find_steed.unresolved.steed_numeric_cells",
            "source_parameter",
        )

        self.assertIn(
            "the caster actually regains Hit Points from a level 1+ spell",
            life_bond["source_interpretation"],
        )
        self.assertIn(
            "the steed regains the same number of Hit Points the caster actually regained",
            life_bond["source_interpretation"],
        )
        self.assertIn(
            "not rolled or nominal spell healing or overheal",
            "\n".join(life_bond["material_qualifiers"]),
        )

    def test_seventh_steed_fell_glare_retains_wisdom_and_steed_target_predicates(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_source_unknown_classifications(manifest)
        fell_glare = seventh_evidence_by_key_category_for(
            manifest,
            "source.spell.find_steed.unresolved.type_to_action_mapping",
            "source_mapping_review",
        )
        interpretation = fell_glare["source_interpretation"]

        self.assertIn(
            "Wisdom saving throw against the caster's spell save DC", interpretation
        )
        self.assertIn(
            "one creature within 60 feet of the steed that the steed can see",
            interpretation,
        )
        self.assertIn(
            "On failure, the target has the Frightened condition until the end of the caster's next turn.",
            interpretation,
        )
        self.assertIn("Bonus Action that recharges after a Long Rest", interpretation)

    def test_seventh_steed_unicode_minus_qualifier_matches_actual_signed_cells(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_source_unknown_classifications(manifest)
        steed = seventh_evidence_by_key_category_for(
            manifest,
            "source.spell.find_steed.unresolved.steed_numeric_cells",
            "source_parameter",
        )
        interpretation = steed["source_interpretation"]
        qualifiers = "\n".join(steed["material_qualifiers"])

        self.assertIn("Int 6/−2/−2", interpretation)
        self.assertIn("Wis 12/+1/+1", interpretation)
        self.assertIn("Cha 8/−1/−1", interpretation)
        self.assertIn(
            "Preserve U+2212 in negative Int (−2/−2) and Cha (−1/−1) modifier/save cells; Wisdom is positive +1/+1.",
            qualifiers,
        )
        self.assertNotIn("U+2212 in Wisdom", qualifiers)

    def test_seventh_source_batch_rejects_frozen_mutations(self) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejected = load_json(REJECTED_PATH)["seventh_rejections"]

        def apply_mutation(
            candidate: dict[str, object], rejection: dict[str, object]
        ) -> None:
            mutation = rejection["mutation"]
            if mutation == "review_field":
                candidate["source_seventh_review"][rejection["field"]] = rejection[
                    "value"
                ]
                return
            if mutation == "replace_common_qualifier":
                candidate["source_seventh_resolution_contract"]["common_qualifiers"][
                    rejection["index"]
                ] = rejection["value"]
                return
            if mutation == "subobligation_field":
                classification = next(
                    value
                    for value in candidate["source_unknown_classifications"]
                    if value["unresolved_key"] == rejection["unresolved_key"]
                )
                subobligation = next(
                    value
                    for value in classification["subobligations"]
                    if value["category"] == rejection["category"]
                )
                subobligation[rejection["field"]] = rejection["value"]
                return
            row = seventh_evidence_by_key_category_for(
                candidate, rejection["unresolved_key"], rejection["source_category"]
            )
            if mutation == "evidence_field":
                row[rejection["field"]] = rejection["value"]
            elif mutation == "source_record_field":
                row["source_record_ref"][rejection["field"]] = rejection["value"]
            elif mutation == "span_hash":
                row["source_markdown_locators"][rejection["locator_index"]][
                    "span_sha256"
                ] = rejection["value"]
            elif mutation == "disposition":
                row["disposition"] = rejection["value"]
            elif mutation == "source_interpretation":
                row["source_interpretation"] = rejection["value"]
            elif mutation == "remove_material_qualifier":
                row["material_qualifiers"].pop(rejection["index"])
            elif mutation == "replace_material_qualifier":
                row["material_qualifiers"][rejection["index"]] = rejection["value"]
            else:
                raise AssertionError(f"unknown seventh rejection mutation: {mutation}")

        self.assertTrue(rejected)
        for rejection in rejected:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=rejection["case_id"]):
                apply_mutation(candidate, rejection)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )

    def test_seventh_source_batch_rejects_current_markdown_span_drift(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        read_pinned = TOOL._read_pinned_local_evidence

        def drift_cube_origin(
            relative_path: str, expected_sha256: str, evidence_name: str
        ) -> bytes:
            data = read_pinned(relative_path, expected_sha256, evidence_name)
            if relative_path == TOOL.SOURCE_MARKDOWN_RELATIVE_PATH:
                return data.replace(
                    b"located anywhere on a face of the Cube",
                    b"located only at the center of the Cube",
                    1,
                )
            return data

        with (
            patch.object(
                TOOL, "_read_pinned_local_evidence", side_effect=drift_cube_origin
            ),
            self.assertRaises(TOOL.SourceQualificationError) as caught,
        ):
            TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(caught.exception.code, "source_seventh_markdown_span_hash")

    def test_seventh_rejected_fixture_keeps_prior_negative_cases_byte_values(
        self,
    ) -> None:
        rejected = load_json(REJECTED_PATH)
        original = {
            key: rejected[key]
            for key in (
                "paired_rejections",
                "numeric_rejections",
                "corroboration_rejections",
                "mode_rejections",
            )
        }
        original_bytes = json.dumps(
            original, sort_keys=True, separators=(",", ":")
        ).encode()
        self.assertEqual(sum(len(values) for values in original.values()), 18)
        self.assertEqual(
            hashlib.sha256(original_bytes).hexdigest(),
            "bce30d5c43a8d5e611200d2fea3b8a1d5af57cbf377c183b681b9d6d0b974988",
        )
        sixth_bytes = json.dumps(
            rejected["sixth_rejections"], sort_keys=True, separators=(",", ":")
        ).encode()
        self.assertEqual(len(rejected["sixth_rejections"]), 11)
        self.assertEqual(
            hashlib.sha256(sixth_bytes).hexdigest(),
            "a714edb5bb72c73eb79eb677534264a909ce59cf6e45b0b6f98eb61b336c99f6",
        )

    def test_third12_rejects_binding_provenance_enum_bound_actor_and_hash_drift(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)

        def third_evidence_for(
            candidate: dict[str, object], key: str
        ) -> dict[str, object]:
            rows = candidate["source_third12_resolution_evidence"]
            return next(row for row in rows if row["unresolved_key"] == key)

        def change_disk_equality(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.floating_disk.unresolved.disk_numeric_limits"
            )
            row["material_qualifiers"][0] = (
                "500 pounds/20 feet/100 feet equality triggers the respective excess rule; "
                "10-foot elevation equality does bar crossing."
            )

        def broaden_familiar_command_leash(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.find_familiar.unresolved.override_type_members"
            )
            row["material_qualifiers"][3] = (
                "The 100-foot predicate limits every familiar command."
            )

        def remove_flaming_sphere_gear_guard(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.flaming_sphere.unresolved.geometry_bounds"
            )
            row["material_qualifiers"][3] = (
                "Contact ignites flammable objects, including worn and carried objects."
            )

        def weaken_hex_later_turn(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.hex.unresolved.ability_member_domain"
            )
            row["material_qualifiers"][1] = (
                "Before spell ends, target dropping to0HP authorizes a same-turn Bonus Action; "
                "death is not required."
            )

        def import_hex_timing_into_hunters_mark(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.hunter_s_mark.unresolved.duration_bands"
            )
            row["material_qualifiers"][2] = (
                "Transfer requires a Bonus Action on a later turn, as with Hex."
            )

        def weaken_jump_actor_boundary(candidate: dict[str, object]) -> None:
            row = third_evidence_for(
                candidate, "source.spell.jump.unresolved.jump_distance_cost"
            )
            row["material_qualifiers"][1] = (
                "A once-per-round use may occur outside the recipient's own turn."
            )

        cases = (
            (
                "wrong-key",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update({"unresolved_key": "source.spell.borrowed.unresolved.key"}),
                "source_third12_census",
            ),
            (
                "wrong-category",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update({"source_category": "source_parameter"}),
                "source_third12_census",
            ),
            (
                "wrong-classification-pointer",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update(
                    {
                        "source_classification_pointer": "/source_unknown_classifications/30"
                    }
                ),
                "source_third12_binding",
            ),
            (
                "borrowed-history-pointer",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update(
                    {
                        "source_unresolved_record_pointer": "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/30"
                    }
                ),
                "source_third12_binding",
            ),
            (
                "borrowed-map-pointer",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update(
                    {
                        "current_map_pointer": "/source_mapping_lanes/0/mapping_payload/entries/30"
                    }
                ),
                "source_third12_binding",
            ),
            (
                "borrowed-source-pass-row",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                )[
                    "source_record_ref"
                ].update({"json_pointer": "/rows/31/required_modes_or_exceptions"}),
                "source_third12_provenance",
            ),
            (
                "borrowed-body-witness",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                )[
                    "source_record_ref"
                ]["body_witness_ref"].update({"json_pointer": "/rows/82"}),
                "source_third12_provenance",
            ),
            (
                "foreign-historical-body-hash",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                )["source_record_ref"].update({"raw_body_sha256": "0" * 64}),
                "source_third12_provenance",
            ),
            (
                "foreign-candidate-hash",
                lambda candidate: candidate["source_third12_review"].update(
                    {"candidate_sha256": "0" * 64}
                ),
                "source_third12_review",
            ),
            (
                "foreign-review-hash",
                lambda candidate: candidate["source_third12_review"].update(
                    {"accepted_review_sha256": "0" * 64}
                ),
                "source_third12_review",
            ),
            (
                "wrong-markdown-locator",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                )["source_markdown_locators"][0].update({"line_start": 11719}),
                "source_third12_locator",
            ),
            (
                "missing-familiar-enum-member",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_familiar.unresolved.override_type_members",
                )["members"].remove("Fey"),
                "source_third12_enum",
            ),
            (
                "extra-guidance-skill",
                lambda candidate: third_evidence_for(
                    candidate, "source.spell.guidance.unresolved.skill_domain"
                )["members"].append("Animal Empathy"),
                "source_third12_enum",
            ),
            (
                "wrong-guidance-enum-member",
                lambda candidate: third_evidence_for(
                    candidate, "source.spell.guidance.unresolved.skill_domain"
                )["members"].__setitem__(0, "Animal Empathy"),
                "source_third12_enum",
            ),
            (
                "hex-slot-2-band",
                lambda candidate: third_evidence_for(
                    candidate, "source.spell.hex.unresolved.duration_bands"
                )["duration_hours_by_slot"].update({"2": 1}),
                "source_third12_duration",
            ),
            (
                "hunters-mark-slot-2-band",
                lambda candidate: third_evidence_for(
                    candidate, "source.spell.hunter_s_mark.unresolved.duration_bands"
                )["duration_hours_by_slot"].update({"2": 4}),
                "source_third12_duration",
            ),
            (
                "floating-disk-equality",
                change_disk_equality,
                "source_third12_qualifier",
            ),
            (
                "familiar-command-leash",
                broaden_familiar_command_leash,
                "source_third12_qualifier",
            ),
            (
                "worn-carried-guard",
                remove_flaming_sphere_gear_guard,
                "source_third12_qualifier",
            ),
            ("hex-later-turn", weaken_hex_later_turn, "source_third12_qualifier"),
            (
                "hunter-immediate-transfer",
                import_hex_timing_into_hunters_mark,
                "source_third12_qualifier",
            ),
            (
                "jump-own-turn-actor",
                weaken_jump_actor_boundary,
                "source_third12_qualifier",
            ),
        )
        for case, mutate, expected_code in cases:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=case):
                mutate(candidate)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(caught.exception.code, expected_code)

    def test_third12_preserves_prior_sets_and_gentle_repose_source_and_downstream_holds(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)

        def third_evidence_for(
            candidate: dict[str, object], key: str
        ) -> dict[str, object]:
            rows = candidate["source_third12_resolution_evidence"]
            return next(row for row in rows if row["unresolved_key"] == key)

        cases = (
            (
                "source-hold-closed",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                ).update({"disposition": "SOURCE_CLOSED"}),
                "source_third12_binding",
            ),
            (
                "source-hold-residual-removed",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                ).update(
                    {
                        "retained_source_residual": (
                            "NONE_FOR_SELECTED_SOURCE_SUBOBLIGATION_ONLY; exact existing "
                            "corpse/body/effect owner reconciliation and identity/expiry/overlap "
                            "proof are still required. The separate "
                            "downstream_domain_consumer_admission_native_proof subobligation "
                            "remains NOT_ESTABLISHED."
                        )
                    }
                ),
                "source_third12_hold",
            ),
            (
                "downstream-hold-promoted",
                lambda candidate: next(
                    value
                    for value in candidate["source_unknown_classifications"][37][
                        "subobligations"
                    ]
                    if value["category"]
                    == "downstream_domain_consumer_admission_native_proof"
                ).update({"status": "SOURCE_CLOSED"}),
                "source_unknown_subobligation",
            ),
            (
                "changed-cumulative-count",
                lambda candidate: candidate[
                    "source_third12_resolution_contract"
                ].update({"cumulative_source_closed_key_count": 32}),
                "source_third12_contract",
            ),
            (
                "native-proof-promotion",
                lambda candidate: third_evidence_for(
                    candidate,
                    "source.spell.find_traps.unresolved.magical_trap_examples",
                ).update({"actual_native_proof_refs": ["unreviewed-proof"]}),
                "source_third12_formulation",
            ),
            (
                "common-total-cover-qualifier-removed",
                lambda candidate: candidate["source_third12_resolution_contract"][
                    "common_qualifiers"
                ].__setitem__(0, "No universal targeting rule is asserted."),
                "source_third12_contract",
            ),
        )
        for case, mutate, expected_code in cases:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=case):
                mutate(candidate)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(caught.exception.code, expected_code)

        prior_first12_removed = copy.deepcopy(baseline)
        prior_first12_removed["source_unknown_resolution_evidence"].pop()
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(prior_first12_removed)

        prior_first12_replaced = copy.deepcopy(baseline)
        prior_first12_replaced["source_unknown_resolution_evidence"][0] = copy.deepcopy(
            prior_first12_replaced["source_third12_resolution_evidence"][0]
        )
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(prior_first12_replaced)

        prior_next12_replaced = copy.deepcopy(baseline)
        prior_next12_replaced["source_next12_resolution_evidence"].pop()
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(prior_next12_replaced)

        prior_next12_replaced_by_third = copy.deepcopy(baseline)
        prior_next12_replaced_by_third["source_next12_resolution_evidence"][0] = (
            copy.deepcopy(
                prior_next12_replaced_by_third["source_third12_resolution_evidence"][0]
            )
        )
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_unknown_classifications(
                prior_next12_replaced_by_third
            )

    def test_next12_source_resolution_rejects_borrowed_provenance_and_qualifiers(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)

        def next_evidence_for(
            candidate: dict[str, object], key: str
        ) -> dict[str, object]:
            rows = candidate["source_next12_resolution_evidence"]
            return next(row for row in rows if row["unresolved_key"] == key)

        def alter_detect_thoughts_escape_turn(candidate: dict[str, object]) -> None:
            row = next_evidence_for(
                candidate,
                "source.spell.detect_thoughts.unresolved.deeper_failure_disclosure",
            )
            row["source_interpretation"] = row["source_interpretation"].replace(
                "on its own turn", "outside its turn"
            )
            row["material_qualifiers"][2] = (
                "The deeper probe uses the next-turn Magic action; the escape is an action "
                "the target can take outside its turn, not an opposed roll."
            )

        def weaken_feather_fall_clear_path(candidate: dict[str, object]) -> None:
            row = next_evidence_for(
                candidate, "source.spell.feather_fall.unresolved.descent_rate"
            )
            row["source_interpretation"] = row["source_interpretation"].replace(
                "The existing target-clear-path rule still applies: a target cannot be behind Total Cover.",
                "The chosen-target wording allows access through Total Cover.",
            )
            row["material_qualifiers"][0] = (
                "The chosen-target sentence does not repeat trigger visibility; Total Cover does not block it."
            )

        def remove_druidcraft_parameter_record(candidate: dict[str, object]) -> None:
            rows = candidate["source_next12_resolution_evidence"]
            row = next(value for value in rows if value["review_item_id"] == "NEXT-09B")
            rows.remove(row)

        def broaden_druidcraft_cube_limit(candidate: dict[str, object]) -> None:
            row = next(
                value
                for value in candidate["source_next12_resolution_evidence"]
                if value["review_item_id"] == "NEXT-09B"
            )
            row["source_interpretation"] = row["source_interpretation"].replace(
                "the harmless Sensory Effect alone must fit within a 5-foot Cube",
                "all Druidcraft modes must fit within a 5-foot Cube",
            )
            row["material_qualifiers"][0] = (
                "The five-foot Cube is a global restriction on all Druidcraft modes."
            )

        cases = (
            (
                "borrowed-key-record",
                lambda candidate: next_evidence_for(
                    candidate,
                    "source.spell.chromatic_orb.unresolved.six_damage_type_members",
                )[
                    "source_record_ref"
                ].update({"json_pointer": "/rows/8/required_modes_or_exceptions"}),
            ),
            (
                "borrowed-entry-map",
                lambda candidate: next_evidence_for(
                    candidate,
                    "source.spell.chromatic_orb.unresolved.six_damage_type_members",
                ).update(
                    {
                        "current_map_pointer": "/source_mapping_lanes/0/mapping_payload/entries/7"
                    }
                ),
            ),
            (
                "borrowed-body-witness",
                lambda candidate: next_evidence_for(
                    candidate,
                    "source.spell.enhance_ability.unresolved.five_ability_members",
                )[
                    "source_record_ref"
                ]["body_witness_ref"].update({"json_pointer": "/rows/81"}),
            ),
            (
                "wrong-markdown-hash",
                lambda candidate: candidate["source_next12_review"].update(
                    {"candidate_sha256": "0" * 64}
                ),
            ),
            (
                "wrong-qualifier",
                alter_detect_thoughts_escape_turn,
            ),
            (
                "clear-path-qualifier",
                weaken_feather_fall_clear_path,
            ),
            (
                "missing-druidcraft-subobligation",
                remove_druidcraft_parameter_record,
            ),
            (
                "global-druidcraft-cube-limit",
                broaden_druidcraft_cube_limit,
            ),
            (
                "removed-detect-magic-hold",
                lambda candidate: next_evidence_for(
                    candidate,
                    "source.spell.detect_magic.unresolved.aura_overlay_policy",
                ).update({"disposition": "SOURCE_CLOSED"}),
            ),
        )
        for case, mutate in cases:
            candidate = copy.deepcopy(manifest)
            with (
                self.subTest(case=case),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                mutate(candidate)
                TOOL._validate_source_unknown_classifications(candidate)

    def test_r5_source_modeling_rulings_close_five_and_preserve_word_recall(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        lane6 = next(
            lane
            for lane in manifest["source_mapping_lanes"]
            if lane["lane_id"] == "source-pass-6-9"
        )
        expected_resolved = {
            "Flesh to Stone",
            "Heroes’ Feast",
            "Instant Summons",
            "Move Earth",
            "Mass Heal",
        }
        resolutions = manifest["source_modeling_resolutions"]
        self.assertEqual(
            {row["source_exact_name"] for row in resolutions}, expected_resolved
        )
        expected_rulings = {
            "Flesh to Stone": "Count the initial failed Constitution save as failure 1 in the three-failure progression; do not begin at zero or count it twice.",
            "Heroes’ Feast": "Roll 2d10 independently for each qualifying partaker and reuse that partaker's result for both the maximum-HP increase and its matching healing.",
            "Instant Summons": "Both activation branches consume the gem and end the binding. If the object is held or carried, transport is prevented; that exception changes transport only and reveals the carrier/location.",
            "Move Earth": "Interruption stops future work and preserves terrain changes already established. When target material is accepted, its exact attained shape is fictional adjudication; do not interpolate linearly or impose a no-effect-until-10-minutes rule.",
            "Mass Heal": "Remove listed conditions only when the target receives positive actual healing; allocation alone, a full-HP target, or blocked/zero healing does not trigger condition removal.",
        }
        self.assertEqual(
            {row["source_exact_name"]: row["ruling"] for row in resolutions},
            expected_rulings,
        )
        for resolution in resolutions:
            self.assertEqual(
                resolution["source_modeling_status"],
                "SETTLED_FOR_SOURCE_CLASSIFICATION",
            )
            self.assertEqual(resolution["native_consumer_status"], "NOT_ESTABLISHED")
            self.assertEqual(resolution["actual_native_proof_refs"], [])
            self.assertIsInstance(
                resolution["source_record_ref"]["source_qualifications"], list
            )
            mapped_entry = next(
                row
                for row in lane6["mapping_payload"]["entries"]
                if row["name"] == resolution["source_exact_name"]
            )
            self.assertEqual(
                mapped_entry["r5_source_modeling_resolution_id"],
                resolution["resolution_id"],
            )

        residuals = manifest["source_modeling_residuals"]
        self.assertEqual(len(residuals), 1)
        self.assertEqual(residuals[0]["source_exact_name"], "Word of Recall")
        self.assertEqual(residuals[0]["status"], "NOT_ESTABLISHED")
        word_recall = next(
            row
            for row in lane6["mapping_payload"]["entries"]
            if row["name"] == "Word of Recall"
        )
        self.assertEqual(
            word_recall["r5_source_modeling_residual_id"], residuals[0]["residual_id"]
        )
        lane_receipt = lane6["receipt_summary"]
        self.assertEqual(
            set(lane_receipt["r5_resolved_source_modeling_names"]), expected_resolved
        )
        self.assertEqual(
            lane_receipt["r5_unresolved_source_modeling_names"], ["Word of Recall"]
        )
        self.assertEqual(
            lane6["mapping_payload"]["lane_reported_source_modeling_residuals"],
            lane_receipt["lane_reported_source_modeling_residuals"],
        )
        self.assertTrue(
            callable(getattr(TOOL, "_validate_source_modeling_r5", None)),
            "missing R5 ruling/source-identity validator",
        )
        tampered = copy.deepcopy(manifest)
        tampered["source_modeling_resolutions"][0]["ruling"] += " Broadened."
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_modeling_r5(tampered)
        tampered = copy.deepcopy(manifest)
        tampered["source_modeling_resolutions"][0]["source_record_ref"][
            "printed_page"
        ] += 1
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_modeling_r5(tampered)
        tampered = copy.deepcopy(manifest)
        tampered["source_modeling_residuals"][0]["prohibited_inferences"].remove(
            "AUTOMATIC_CAP"
        )
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_source_modeling_r5(tampered)

    def test_raw_extraction_cannot_admit_foreign_tail_or_missing_block(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        TOOL._validate_reconstruction_witnesses(manifest, roster)

        rejected = load_json(REJECTED_PATH)
        variants = rejected["paired_rejections"]
        self.assertIsInstance(variants, list)
        for variant in variants:
            candidate = copy.deepcopy(manifest)
            apply_rejected_variant(candidate, variant)
            with (
                self.subTest(case=variant["case_id"]),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_reconstruction_witnesses(candidate, roster)

    def test_official_corroboration_is_not_promoted_to_licensed_primary_text(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        TOOL._validate_corroborating_sources(manifest)
        rejected = load_json(REJECTED_PATH)
        for variant in rejected["corroboration_rejections"]:
            candidate = copy.deepcopy(manifest)
            source = next(
                row
                for row in candidate["corroborating_sources"]
                if row["source_id"] == variant["source_id"]
            )
            source[variant["field"]] = variant["value"]
            with (
                self.subTest(case=variant["case_id"]),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_corroborating_sources(candidate)

    def test_unicode_signs_and_seed_metadata_have_distinct_dispositions(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        TOOL._validate_numeric_witnesses(manifest)
        self.assertTrue(
            callable(getattr(TOOL, "_validate_seed_observation", None)),
            "missing exact current-seed snapshot validator",
        )
        observation = TOOL._validate_seed_observation(manifest)
        glyphs = manifest["numeric_glyph_witnesses"]
        self.assertEqual({row["codepoint"] for row in glyphs}, {"U+2212", "U+00D7"})
        self.assertIn("−", glyphs[0]["literal"])
        self.assertIn("×", glyphs[1]["literal"])
        conflict = TOOL._validate_seed_conflicts(manifest, roster)[0]
        self.assertEqual(conflict["entry_id"], "spell.acid_splash")
        self.assertEqual(conflict["source_facts"]["school_id"], "school.evocation")
        self.assertEqual(
            conflict["source_facts"]["targeting"]["target_mode"],
            "POINT_CENTERED_SPHERE",
        )
        self.assertEqual(
            observation["records_by_id"]["spell.acid_splash"]["data"]["school_id"],
            "school.conjuration",
        )
        self.assertEqual(conflict["disposition"], "EVIDENCE_ONLY_NO_REWRITE")

        rejected = load_json(REJECTED_PATH)
        for variant in rejected["numeric_rejections"]:
            candidate = copy.deepcopy(manifest)
            apply_rejected_variant(candidate, variant)
            with (
                self.subTest(case=variant["case_id"]),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_numeric_witnesses(candidate)

    def test_acid_splash_uses_structured_current_source_facts(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        conflict = manifest["seed_metadata_conflicts"][0]
        self.assertIsInstance(conflict["source_facts"]["targeting"], dict)
        self.assertEqual(
            conflict["source_facts"]["targeting"]["target_mode"],
            "POINT_CENTERED_SPHERE",
        )
        self.assertFalse(conflict["source_facts"]["targeting"]["legacy_two_target"])

        assert TOOL is not None
        roster = TOOL.derive_source_requirement_roster(manifest)
        legacy = copy.deepcopy(manifest)
        legacy["seed_metadata_conflicts"][0]["source_facts"]["targeting"][
            "target_mode"
        ] = "LEGACY_TWO_TARGETS"
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_seed_conflicts(legacy, roster)

    def test_current_seed_observation_is_hash_and_record_bound(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        self.assertTrue(
            callable(getattr(TOOL, "_validate_seed_observation", None)),
            "missing exact current-seed snapshot validator",
        )
        observation = TOOL._validate_seed_observation(manifest)
        self.assertEqual(
            observation["sha256"],
            "711b6a2ec0173407825a9eee5a1432ac6e9ce07f47a1d9d378fd17aac8cf7550",
        )
        stale = copy.deepcopy(manifest)
        stale["seed_metadata_conflicts"][0]["observed_baseline"]["sha256"] = "0" * 64
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_seed_observation(stale)

        falsified = copy.deepcopy(manifest)
        falsified["seed_metadata_conflicts"][0]["observed_baseline"]["records"][0][
            "record"
        ]["data"]["school_id"] = "school.evocation"
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_seed_observation(falsified)

    def test_acid_splash_rejects_falsified_source_range_or_area(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        for field, value in (
            ("point_selection_range_feet", 30),
            ("area_radius_feet", 10),
            ("legacy_two_target", True),
        ):
            falsified = copy.deepcopy(manifest)
            falsified["seed_metadata_conflicts"][0]["source_facts"]["targeting"][
                field
            ] = value
            with (
                self.subTest(field=field),
                self.assertRaises(TOOL.SourceQualificationError),
            ):
                TOOL._validate_seed_conflicts(falsified, roster)

    def test_thunderclap_is_separate_unqualified_existing_extra(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        roster = TOOL.derive_source_requirement_roster(manifest)
        extra = TOOL._validate_extra_lane(manifest, roster)
        self.assertEqual(extra["name"], "Thunderclap")
        self.assertEqual(extra["roster_membership"], "OUTSIDE_SRD_339")
        self.assertEqual(extra["qualification_status"], "NOT_QUALIFIED")
        self.assertFalse(extra["selectable"])
        self.assertNotIn(extra["name"], {row["name"] for row in roster})
        self.assertIn(
            "content_owner_default_repair",
            manifest,
            "unqualified extra needs the accepted content-owner repair disposition",
        )
        self.assertEqual(
            manifest["content_owner_default_repair"]["status"],
            "REQUIRED_BEFORE_PACKAGE_PROMOTION",
        )
        self.assertEqual(
            manifest["content_owner_default_repair"]["owner_section"],
            "Defaults, commitments and migration",
        )
        self.assertEqual(
            manifest["content_owner_default_repair"]["worker_seed_mutation"], "NONE"
        )
        self.assertTrue(
            callable(getattr(TOOL, "_source_qualification_receipt", None)),
            "missing partial source-census receipt classifier",
        )
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        self.assertEqual(receipt["status"], "W05_SPELL_SOURCE_CENSUS_PARTIAL")
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")

        manifest["existing_extra_lane"]["qualification_status"] = "QUALIFIED"
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._validate_extra_lane(manifest, roster)
        with self.assertRaises(TOOL.SourceQualificationError):
            TOOL._source_qualification_receipt(manifest, roster)

    def test_source_asset_bytes_must_match_the_declared_asset_digest(self) -> None:
        assert TOOL is not None
        manifest, assets = make_synthetic_registry()
        self.assertEqual(len(TOOL._validate_source_assets(manifest, assets)), 5)
        first_uri = next(iter(assets))
        assets[first_uri] = b"mutated source bytes"
        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_source_assets(manifest, assets)
        self.assertEqual(caught.exception.code, "source_asset_digest")

    def test_manifest_rejects_unowned_fields(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        manifest["unowned_rule_override"] = "not permitted"
        with self.assertRaises(TOOL.SourceQualificationError) as caught:
            TOOL._validate_manifest_schema(manifest)
        self.assertEqual(caught.exception.code, "manifest_schema")

    def test_accepted_owner_decision_closes_only_the_six_reviewed_source_keys(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)

        resolved_keys = set(classification["source_resolved_keys"])
        held_keys = set(classification["source_held_keys"])
        self.assertEqual(len(resolved_keys), 71)
        self.assertTrue(OWNER_DECIDED_SOURCE_KEYS.issubset(resolved_keys))
        self.assertTrue(FAMILIAR_SOURCE_CLOSED_KEYS.issubset(resolved_keys))
        self.assertTrue(TENTH_SOURCE_CLOSED_KEYS.issubset(resolved_keys))
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(
            held_keys,
            {
                "source.spell.arcane_lock.unresolved.destruction_access_policy",
                "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
                "source.spell.detect_magic.unresolved.aura_overlay_policy",
                "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                "source.spell.magic_mouth.unresolved.trigger_episode_frequency",
                "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
            },
        )
        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["future_proof_subobligation_count"], 33)
        self.assertEqual(len(manifest["source_unknown_classifications"]), 82)
        self.assertEqual(
            [
                len(manifest[field])
                for field in (
                    "source_unknown_resolution_evidence",
                    "source_next12_resolution_evidence",
                    "source_third12_resolution_evidence",
                    "source_fourth_resolution_evidence",
                    "source_fifth_resolution_evidence",
                    "source_sixth_resolution_evidence",
                    "source_seventh_resolution_evidence",
                    "source_tenth_resolution_evidence",
                )
            ],
            [12, 13, 12, 11, 13, 13, 7, 3],
        )

        owner = manifest["source_interpretation_owner"]
        self.assertEqual(
            owner["decision_path"],
            "DEV/docs/superpowers/specs/2026-10-14-sp00-source-interpretation-owner-decision.md",
        )
        self.assertEqual(
            owner["decision_sha256"],
            "9de384b36657bafe7e93252959825ed4ba4494f287ee972904d589f5c8759e5c",
        )
        self.assertEqual(
            owner["decision_git_blob"], "662d17d8299fae1ac264863a7da31bd99a9da183"
        )
        self.assertEqual(owner["accepted_sections"], ["A", "B", "C", "D", "E", "F"])
        self.assertEqual(
            owner["accepted_keys"],
            [
                "source.spell.aid.unresolved.health_normalization_policy",
                "source.spell.magic_missile.unresolved.rng_damage_grouping",
                "source.spell.pass_without_trace.unresolved.selection_timing",
                "source.spell.ray_of_frost.unresolved.movement_composition",
                "source.spell.resistance.unresolved.damage_grouping_order",
                "source.spell.warding_bond.unresolved.copied_damage_policy",
            ],
        )
        evidence = manifest["source_eighth_resolution_evidence"]
        self.assertEqual(
            [row["unresolved_key"] for row in evidence],
            owner["accepted_keys"],
        )
        self.assertEqual({row["disposition"] for row in evidence}, {"OWNER_DECIDED"})
        self.assertEqual(
            {row["resolution_authority"] for row in evidence},
            {"ACCEPTED_PRODUCT_OWNER_DECISION"},
        )
        self.assertEqual(
            classification["source_owner_decided_keys"],
            [*owner["accepted_keys"], PRAYER_OWNER_SOURCE_KEY],
        )
        self.assertEqual(classification["source_owner_decision_evidence"][:6], evidence)
        self.assertEqual(
            classification["source_owner_decision_evidence"][6],
            manifest["source_prayer_owner_resolution_evidence"][0],
        )
        self.assertTrue(
            all(
                row["resolution_basis"]
                == "ACCEPTED_OWNER_INTERPRETATION_NOT_LITERAL_SRD_WORDING"
                for row in evidence
            )
        )
        missile = owner_decision_evidence_by_key_for(
            manifest,
            "source.spell.magic_missile.unresolved.rng_damage_grouping",
        )
        self.assertTrue(
            any(
                "independent damage-die draws are source-grounded" in value
                for value in missile["source_grounded_findings"]
            )
        )
        self.assertIn("one simultaneous group", missile["accepted_interpretation"])
        resistance = owner_decision_evidence_by_key_for(
            manifest,
            "source.spell.resistance.unresolved.damage_grouping_order",
        )
        self.assertTrue(
            any(
                "automatic chosen-type trigger and once-per-turn reduction are source-grounded"
                in value
                for value in resistance["source_grounded_findings"]
            )
        )
        self.assertEqual(resistance["golden_witness"]["expected_total_damage"], 6)
        self.assertIn(
            "selected damage-type subtotal", resistance["accepted_interpretation"]
        )
        self.assertEqual(
            manifest["source_eighth_resolution_contract"][
                "cumulative_source_resolved_key_count"
            ],
            66,
        )
        self.assertEqual(
            manifest["source_eighth_resolution_contract"][
                "cumulative_source_held_key_count"
            ],
            11,
        )
        historical_warding_hold = next(
            row
            for row in manifest["source_seventh_resolution_evidence"]
            if row["unresolved_key"]
            == "source.spell.warding_bond.unresolved.copied_damage_policy"
        )
        self.assertEqual(historical_warding_hold["disposition"], "SOURCE_HELD")
        self.assertEqual(
            manifest["content_owner_default_repair"]["status"],
            "REQUIRED_BEFORE_PACKAGE_PROMOTION",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["source_exact_name"],
            "Word of Recall",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["status"], "NOT_ESTABLISHED"
        )

        receipt = TOOL._source_qualification_receipt(
            manifest, TOOL.derive_source_requirement_roster(manifest)
        )
        self.assertEqual(receipt["status"], "W05_SPELL_SOURCE_CENSUS_PARTIAL")
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])

    def test_prayer_owner_binding_resolves_only_the_accepted_source_subobligation(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)

        self.assertEqual(classification["source_resolved_key_count"], 71)
        self.assertEqual(classification["source_held_key_count"], 6)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["future_proof_subobligation_count"], 33)
        self.assertIn(PRAYER_OWNER_SOURCE_KEY, classification["source_resolved_keys"])
        self.assertNotIn(PRAYER_OWNER_SOURCE_KEY, classification["source_held_keys"])
        self.assertEqual(classification["source_closed_key_count"], 64)
        self.assertEqual(classification["source_owner_decided_key_count"], 7)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(
            set(classification["source_held_keys"]),
            {
                "source.spell.arcane_lock.unresolved.destruction_access_policy",
                "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
                "source.spell.detect_magic.unresolved.aura_overlay_policy",
                "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                "source.spell.magic_mouth.unresolved.trigger_episode_frequency",
                "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
            },
        )

        row = prayer_owner_evidence_for(manifest)
        self.assertEqual(row["disposition"], "OWNER_DECIDED")
        self.assertEqual(row["resolution_authority"], "ACCEPTED_PRODUCT_OWNER_DECISION")
        self.assertEqual(row["future_native_proof_status"], "NOT_ESTABLISHED")
        self.assertEqual(row["actual_native_proof_refs"], [])
        self.assertEqual(
            row["owner_decision_ref"],
            {
                "authority": "ACCEPTED_PRODUCT_OWNER_DECISION",
                "path": "DEV/docs/superpowers/specs/2026-10-15-sp00-prayer-benefits-owner-decision.md",
                "raw_utf8_sha256": "efbe9b06f43306cbf6d325f72c5c8e2959b01eb9288d4e9699dd93e5de64cab0",
                "git_blob_sha1": "8b4cc275c1e85a78ac74c497d9a45d219eed758f",
                "section_numbers": ["1", "2", "3", "4", "5"],
            },
        )
        self.assertEqual(row["source_census_ref"]["responder_count"], 114)
        self.assertEqual(
            row["source_census_ref"]["validated_exact_span_record_count"], 942
        )
        completion_rows = row["accepted_completion_rows"]
        self.assertEqual(
            [value["row_number"] for value in completion_rows],
            [12, 13, 14, 18, 19, 21, 28],
        )
        tireless = completion_rows[0]
        self.assertEqual(tireless["source_exact_name"], "Ranger Tireless")
        self.assertEqual(tireless["actual_grant_condition"], "Ranger10+; Exhaustion >0")
        self.assertEqual(
            tireless["historical_census_disposition"],
            "SOURCE_SUPPORTED_RECHARGE_OR_HD_BENEFIT_IF_ACTUALLY_GRANTED",
        )
        self.assertIn(
            "BROADER_7_POSSESSED_COMPLETION_OPPORTUNITIES", row["owner_decided_claims"]
        )
        self.assertIn(
            "NO_MOUNT_PACE_RENEWAL_WITHOUT_ACTUAL_REST", row["owner_decided_claims"]
        )
        self.assertIn(
            "DIFFERENTIATED_REST_BENEFIT_DENIAL_AND_SIMULACRUM_RESTRICTIONS",
            row["owner_decided_claims"],
        )
        self.assertEqual(
            row["target_gate_qualification"]["lawful_zero_delta_or_declined_option"],
            "AFFECTED_AND_CONSUMES_RECIPIENT_GATE",
        )
        self.assertEqual(
            row["target_gate_qualification"]["proved_all_blocked"],
            "NO_EFFECT_AND_NO_NEW_GATE_CONSUMPTION",
        )
        self.assertEqual(
            row["target_gate_qualification"]["unknown_eligibility"],
            "SCOPED_HOLD_NOT_ALL_BLOCKED_OR_SUCCESS",
        )
        self.assertEqual(
            row["special_branches"]["incubus"],
            "CURSE_DENIES_REST_BENEFIT_UNTIL_24H_OR_INCUBUS_DEATH_DIRECT_HEALING_SEPARATE",
        )
        self.assertEqual(
            row["special_branches"]["rakshasa"],
            "CURSE_DENIES_REST_BENEFIT_WHILE_CURSED_DIRECT_HEALING_SEPARATE",
        )
        self.assertEqual(row["new_feature_or_grant"], "NONE")
        self.assertEqual(len(row["source_grounded_line_refs"]), 14)

        historical_hold = next(
            value
            for value in manifest["source_fifth_resolution_evidence"]
            if value["unresolved_key"] == PRAYER_OWNER_SOURCE_KEY
        )
        self.assertEqual(historical_hold["review_item_id"], "FIFTH-07")
        self.assertEqual(historical_hold["disposition"], "SOURCE_HELD")
        prayer_classification = manifest["source_unknown_classifications"][62]
        self.assertEqual(prayer_classification["original_status"], "NOT_ESTABLISHED")
        self.assertTrue(prayer_classification["source_ready_blocking"])
        self.assertEqual(
            prayer_classification["source_unresolved_record_pointer"],
            "/source_mapping_lanes/0/mapping_payload/unresolved_key_index/62",
        )
        self.assertEqual(
            manifest["source_tenth_resolution_contract"][
                "cumulative_source_resolved_key_count"
            ],
            70,
        )
        self.assertEqual(
            manifest["source_tenth_resolution_contract"][
                "cumulative_source_held_key_count"
            ],
            7,
        )
        self.assertEqual(
            manifest["content_owner_default_repair"]["status"],
            "REQUIRED_BEFORE_PACKAGE_PROMOTION",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["source_exact_name"],
            "Word of Recall",
        )
        self.assertEqual(
            manifest["source_modeling_residuals"][0]["status"], "NOT_ESTABLISHED"
        )

        receipt = TOOL._source_qualification_receipt(
            manifest, TOOL.derive_source_requirement_roster(manifest)
        )
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])

    def test_prayer_owner_evidence_rejects_cold_identity_scope_and_proof_mutations(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejections = load_json(REJECTED_PATH)["prayer_owner_rejections"]
        self.assertEqual(len({case["case_id"] for case in rejections}), len(rejections))

        for rejection in rejections:
            candidate = copy.deepcopy(baseline)
            target: object = candidate
            for part in rejection["path"][:-1]:
                target = target[part]  # type: ignore[index]
            final_part = rejection["path"][-1]
            operation = rejection["operation"]
            if operation == "replace":
                target[final_part] = rejection["value"]  # type: ignore[index]
            elif operation == "append":
                target[final_part].append(rejection["value"])  # type: ignore[index,union-attr]
            elif operation == "delete_index":
                del target[final_part][rejection["index"]]  # type: ignore[index]
            else:
                raise AssertionError(f"unknown Prayer rejection operation: {operation}")

            with self.subTest(case=rejection["case_id"]):
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )

    def test_prayer_owner_binding_reads_exact_owner_and_census_file_bytes(self) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        read_pinned = TOOL._read_pinned_local_evidence
        for target_path, expected_error in (
            (TOOL.PRAYER_OWNER_DECISION_PATH, "source_prayer_owner_identity"),
            (TOOL.PRAYER_RESPONDER_CENSUS_PATH, "source_prayer_census_identity"),
        ):

            def drift_bytes(
                relative_path: str,
                expected_sha256: str,
                evidence_name: str,
                pinned_path: str = target_path,
            ) -> bytes:
                data = read_pinned(relative_path, expected_sha256, evidence_name)
                return data + b"\n" if relative_path == pinned_path else data

            with self.subTest(path=target_path):
                with (
                    patch.object(
                        TOOL, "_read_pinned_local_evidence", side_effect=drift_bytes
                    ),
                    self.assertRaises(TOOL.SourceQualificationError) as caught,
                ):
                    TOOL._validate_source_unknown_classifications(manifest)
                self.assertEqual(caught.exception.code, expected_error)

    def test_tenth_open_domain_batch_closes_only_three_source_obligations(
        self,
    ) -> None:
        assert TOOL is not None
        manifest = load_json(MANIFEST_PATH)
        classification = TOOL._validate_source_unknown_classifications(manifest)
        self.assertEqual(classification["source_resolved_key_count"], 71)

        selected = manifest["source_tenth_resolution_evidence"]
        self.assertEqual(
            [
                (
                    row["review_item_id"],
                    row["unresolved_key"],
                    row["source_category"],
                    row["disposition"],
                )
                for row in selected
            ],
            [
                (
                    "TENTH-01",
                    "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain",
                    "source_mapping_review",
                    "SOURCE_CLOSED",
                ),
                (
                    "TENTH-02",
                    "source.spell.mending.unresolved.repair_dimension_and_missing_matter",
                    "source_parameter",
                    "SOURCE_CLOSED",
                ),
                (
                    "TENTH-03",
                    "source.spell.unseen_servant.unresolved.subject_health_classification",
                    "source_semantics",
                    "SOURCE_CLOSED",
                ),
            ],
        )
        self.assertEqual(classification["source_closed_key_count"], 64)
        self.assertEqual(classification["source_owner_decided_key_count"], 7)
        self.assertEqual(classification["source_resolved_subobligation_count"], 75)
        self.assertEqual(classification["source_held_key_count"], 6)
        self.assertEqual(classification["source_held_subobligation_count"], 6)
        self.assertEqual(classification["source_blocking_key_count"], 6)
        self.assertEqual(classification["source_reviewed_key_count"], 77)
        self.assertEqual(len(classification["source_resolution_evidence"]), 92)
        self.assertEqual(classification["future_proof_subobligation_count"], 33)
        self.assertEqual(
            set(classification["source_held_keys"]),
            {
                "source.spell.arcane_lock.unresolved.destruction_access_policy",
                "source.spell.create_or_destroy_water.unresolved.container_and_extent_bounds",
                "source.spell.detect_magic.unresolved.aura_overlay_policy",
                "source.spell.gentle_repose.unresolved.corpse_and_revival_binding",
                "source.spell.magic_mouth.unresolved.trigger_episode_frequency",
                "source.spell.spike_growth.unresolved.displacement_and_distance_policy",
            },
        )
        contract = manifest["source_tenth_resolution_contract"]
        self.assertEqual(contract["status"], "PARTIAL_TENTH_OPEN_DOMAIN_SOURCE_ONLY")
        self.assertEqual(
            contract["selected_original_classification_indexes"], [47, 56, 78]
        )
        self.assertEqual(contract["cumulative_source_closed_key_count"], 64)
        self.assertEqual(contract["cumulative_owner_decided_key_count"], 6)
        self.assertEqual(contract["cumulative_source_resolved_key_count"], 70)
        self.assertEqual(contract["cumulative_source_held_key_count"], 7)
        self.assertEqual(contract["future_native_proof_status"], "NOT_ESTABLISHED")
        self.assertEqual(
            contract["full_339_source_qualification_status"], "NOT_ESTABLISHED"
        )
        self.assertEqual(contract["production_claim"], "NONE")

        by_key = {row["unresolved_key"]: row for row in selected}
        locate = by_key[
            "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain"
        ]
        locate_text = "\n".join(
            [locate["source_interpretation"], *locate["material_qualifiers"]]
        )
        self.assertIn("Beast, Plant creature and nonmagical plant", locate_text)
        self.assertIn("specific kind", locate_text)
        self.assertIn("closest matching", locate_text)
        self.assertIn("within 5 miles", locate_text)
        self.assertIn("no finite individually named", locate_text.lower())
        self.assertIn("failed completeness", locate_text.lower())
        self.assertNotIn("complete three-member census", locate_text.lower())

        mending = by_key[
            "source.spell.mending.unresolved.repair_dimension_and_missing_matter"
        ]
        mending_text = "\n".join(
            [mending["source_interpretation"], *mending["material_qualifiers"]]
        )
        self.assertIn("1 foot in any dimension", mending_text)
        self.assertIn("1 minute", mending_text)
        self.assertIn("no numeric missing-material allowance", mending_text.lower())
        self.assertIn("not a universal zero-loss prohibition", mending_text.lower())
        self.assertIn("sole native Asset durability authority", mending_text)
        self.assertIn("cosmetic", mending_text.lower())
        self.assertNotIn("missing-matter quantity is zero", mending_text.lower())

        servant = by_key[
            "source.spell.unseen_servant.unresolved.subject_health_classification"
        ]
        servant_text = "\n".join(
            [servant["source_interpretation"], *servant["material_qualifiers"]]
        )
        self.assertIn("Medium force", servant_text)
        self.assertIn("sparse native Actor force proxy", servant_text)
        self.assertIn("does not grant a creature-type tag", servant_text)
        self.assertIn("bounded pre-outcome adjudication", servant_text)
        self.assertNotIn("categorically a creature", servant_text.lower())

        review = manifest["source_tenth_review"]
        self.assertEqual(review["senior_ruling_id"], "ses_ec3aae68fffea0W12EXQmT1zaR")
        self.assertEqual(
            review["source_report_sha256"],
            "100a8c75aa6087bb0c05d81a06b28521c5e8e8328756a3d98300d643aca1c933",
        )

        for index, key in (
            (47, locate["unresolved_key"]),
            (56, mending["unresolved_key"]),
            (78, servant["unresolved_key"]),
        ):
            original = manifest["source_unknown_classifications"][index]
            self.assertEqual(original["unresolved_key"], key)
            self.assertEqual(original["original_status"], "NOT_ESTABLISHED")
            self.assertTrue(original["source_ready_blocking"])
            self.assertEqual(
                original["original_disposition"],
                "RECONCILE_EXACT_QUALIFIED_SOURCE_OR_OWNER; DO_NOT_GUESS",
            )

        self.assertEqual(
            fourth_evidence_by_key_for(
                manifest,
                "source.spell.locate_animals_or_plants.unresolved.eligible_search_domain",
            )["disposition"],
            "SOURCE_HELD",
        )
        self.assertEqual(
            next(
                row
                for row in manifest["source_fifth_resolution_evidence"]
                if row["unresolved_key"]
                == "source.spell.mending.unresolved.repair_dimension_and_missing_matter"
            )["disposition"],
            "SOURCE_HELD",
        )
        self.assertEqual(
            next(
                row
                for row in manifest["source_sixth_resolution_evidence"]
                if row["review_item_id"] == "SIXTH-11A"
            )["disposition"],
            "SOURCE_HELD",
        )
        key79 = next(
            row
            for row in manifest["source_sixth_resolution_evidence"]
            if row["review_item_id"] == "SIXTH-11B"
        )
        self.assertEqual(key79["disposition"], "SOURCE_CLOSED")
        self.assertIn(
            "not an ambient caster-motion leash", key79["material_qualifiers"]
        )

        self.assertTrue(
            all(
                row["status"] == "NOT_ESTABLISHED"
                and row["gate_phase"] == "FUTURE_PROOF"
                for row in classification["future_proof_subobligations"]
            )
        )
        roster = TOOL.derive_source_requirement_roster(manifest)
        receipt = TOOL._source_qualification_receipt(manifest, roster)
        self.assertEqual(receipt["source_qualification_status"], "NOT_ESTABLISHED")
        self.assertFalse(receipt["source_ready_gate"]["ready"])
        self.assertEqual(
            next(
                row
                for row in receipt["source_ready_gate"]["blockers"]
                if row["code"] == "UNRESOLVED_SOURCE_KEYS"
            )["count"],
            6,
        )

    def test_tenth_open_domain_batch_rejects_scope_qualifier_and_proof_mutations(
        self,
    ) -> None:
        assert TOOL is not None
        baseline = load_json(MANIFEST_PATH)
        rejections = load_json(REJECTED_PATH)["tenth_source_rejections"]
        self.assertGreaterEqual(len(rejections), 12)

        def mutate(candidate: dict[str, object], rejection: dict[str, object]) -> None:
            target = rejection["target"]
            if target == "review":
                row = candidate["source_tenth_review"]
            elif target == "contract":
                row = candidate["source_tenth_resolution_contract"]
            elif target == "evidence":
                row = candidate["source_tenth_resolution_evidence"][
                    rejection["record_index"]
                ]
            elif target == "locator":
                row = candidate["source_tenth_resolution_evidence"][
                    rejection["record_index"]
                ]["source_markdown_locators"][rejection["locator_index"]]
            else:
                raise AssertionError(f"unknown tenth-source target: {target}")

            field = rejection["field"]
            operation = rejection["operation"]
            if operation == "replace":
                row[field] = rejection["value"]
            elif operation == "append":
                row[field].append(rejection["value"])
            else:
                raise AssertionError(f"unknown tenth-source mutation: {operation}")

        self.assertEqual(len({row["case_id"] for row in rejections}), len(rejections))
        for rejection in rejections:
            candidate = copy.deepcopy(baseline)
            with self.subTest(case=rejection["case_id"]):
                mutate(candidate, rejection)
                with self.assertRaises(TOOL.SourceQualificationError) as caught:
                    TOOL._validate_source_unknown_classifications(candidate)
                self.assertEqual(
                    caught.exception.code, rejection["expected_error_code"]
                )


if __name__ == "__main__":
    unittest.main()
