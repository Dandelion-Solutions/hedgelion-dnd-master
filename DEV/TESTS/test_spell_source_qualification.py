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


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_by_key_for(manifest: dict[str, object], key: str) -> dict[str, object]:
    records = manifest.get("source_unknown_resolution_evidence")
    if not isinstance(records, list):
        raise TypeError("source residual resolution evidence must be a list")
    return next(row for row in records if row["unresolved_key"] == key)


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
        self.assertEqual(unresolved_blocker["count"], 68)
        self.assertEqual(unresolved_blocker["entry_count"], 61)
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
        self.assertEqual(classification["source_blocking_key_count"], 68)
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
        self.assertIn(
            "source.spell.ray_of_enfeeblement.unresolved.damage_floor_policy",
            classification["source_blocking_keys"],
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

        self.assertEqual(classification["source_blocking_key_count"], 68)
        self.assertEqual(classification["historical_source_blocking_key_count"], 77)
        self.assertEqual(classification["source_resolved_subobligation_count"], 9)
        self.assertEqual(classification["source_held_subobligation_count"], 3)
        source_blocking_keys = set(classification["source_blocking_keys"])
        self.assertTrue(FIRST12_SOURCE_CLOSED_KEYS.isdisjoint(source_blocking_keys))
        self.assertTrue(FIRST12_SOURCE_HELD_KEYS.issubset(source_blocking_keys))
        self.assertTrue(
            {
                "source.spell.augury.unresolved.four_omen_members",
                "source.spell.chromatic_orb.unresolved.six_damage_type_members",
                "source.spell.detect_evil_and_good.unresolved.supernatural_type_members",
            }.issubset(source_blocking_keys)
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


if __name__ == "__main__":
    unittest.main()
