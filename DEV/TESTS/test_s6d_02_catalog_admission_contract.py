"""Focused S6D-02 catalog-admission contract checks."""
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from catalog_admission import load_catalog_admission_ledger  # noqa: E402

CORE = ROOT / "DEV/CATALOG/core-catalog.json"
SCHEMA = ROOT / "DEV/SCHEMAS/catalog-admission-ledger.schema.json"

EXPECTED_REASONS = [
    "invalid_manifest", "content_mismatch", "missing_dependency",
    "ambiguous_dependency", "dependency_cycle", "package_id_ambiguity",
    "namespace_conflict", "engine_incompatibility", "catalog_incompatibility",
    "resolved_set_mismatch", "unreconstructable_context",
]


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _pairs(core):
    return [(family, item) for family, items in core["registries"].items() for item in items]


class CatalogAdmissionContractTests(unittest.TestCase):
    def test_schema_and_exact_bidirectional_trace(self):
        core, ledger, schema = _load(CORE), load_catalog_admission_ledger(ROOT), _load(SCHEMA)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(ledger, schema)
        core_pairs = _pairs(core)
        ledger_pairs = [(entry["registry_family"], entry["id"]) for entry in ledger["entries"]]
        expected_count = len(core_pairs)
        self.assertEqual(len(ledger_pairs), expected_count)
        self.assertEqual(len(set(ledger_pairs)), expected_count)
        self.assertEqual(set(core_pairs), set(ledger_pairs))
        self.assertEqual(set(core["registries"]), set(ledger["family_policies"]))
        self.assertTrue(all(entry["profile"] == entry["registry_family"] for entry in ledger["entries"]))

    def test_item_level_evidence_disposition_and_realization(self):
        ledger = load_catalog_admission_ledger(ROOT)
        schema = _load(SCHEMA)
        allowed_evidence_classes = set(schema["$defs"]["entry"]["properties"]["evidence_class"]["enum"])
        for entry in ledger["entries"]:
            self.assertTrue(entry["evidence_citation"].strip())
            self.assertTrue(entry["consumer_or_dependency"].strip())
            self.assertTrue(entry["semantic_owner"].strip())
            if entry["scope_stratum"] == "S6D_PRIMARY":
                self.assertIn(entry["evidence_class"], allowed_evidence_classes)
                self.assertNotEqual(entry["realization_state"], "INHERITED_ACTIVE")
            if entry["scope_stratum"] == "INHERITED_ROUND2":
                self.assertEqual(entry["realization_state"], "INHERITED_ACTIVE")
            if entry["admission_disposition"] == "EMBEDDED_NONOWNER":
                self.assertTrue(entry["containing_owner"].strip())
                self.assertNotIn("exact accepted interface owner", entry["containing_owner"])
                self.assertEqual(entry["registry_family"], "protocol_value_kinds")
            if entry["admission_disposition"] == "DORMANT_NONSELECTABLE":
                self.assertTrue((entry.get("activation_trigger") or entry["consumer_or_dependency"]).strip())
            if entry["realization_state"] == "INHERITED_ACTIVE":
                self.assertTrue(entry["downstream_owner"])
            if entry["realization_state"].startswith("DOWNSTREAM_S6D_"):
                suffix = entry["realization_state"].removeprefix("DOWNSTREAM_S6D_")
                self.assertEqual(entry["downstream_owner"], f"S6D-{suffix}")
            self.assertNotEqual(entry["admission_disposition"], "STALE_REMOVE")

    def test_census_arithmetic_matches_entries(self):
        ledger = load_catalog_admission_ledger(ROOT)
        core = _load(CORE)
        by_family = {}
        for entry in ledger["entries"]:
            row = by_family.setdefault(entry["registry_family"], Counter())
            row["count"] += 1
            row[entry["admission_disposition"]] += 1
        self.assertEqual(len(ledger["registry_census"]), len(core["registries"]))
        for census in ledger["registry_census"]:
            actual = by_family[census["registry_family"]]
            self.assertEqual(census["count"], actual["count"])
            self.assertEqual(census["admitted"], actual["ACTIVE_ADMITTED"])
            self.assertEqual(census["embedded_nonowner"], actual["EMBEDDED_NONOWNER"])
            self.assertEqual(census["dormant_nonselectable"], actual["DORMANT_NONSELECTABLE"])
            self.assertEqual(census["stale_remove"], actual["STALE_REMOVE"])

    def test_executable_capabilities_are_supported_or_quarantined(self):
        ledger = load_catalog_admission_ledger(ROOT)
        entries = {(e["registry_family"], e["id"]): e for e in ledger["entries"]}
        surfaces = _load(ROOT / "DEV/CATALOG/mechanical-surfaces.json")
        active_selectors = {i for (f, i), e in entries.items()
                            if f == "rule_selectors" and e["admission_disposition"] == "ACTIVE_ADMITTED"}
        active_accessors = {i for (f, i), e in entries.items()
                            if f == "mechanical_accessors" and e["admission_disposition"] == "ACTIVE_ADMITTED"}
        active_ops = {i for (f, i), e in entries.items()
                      if f == "rule_operations" and e["admission_disposition"] == "ACTIVE_ADMITTED"}
        consumed_ops = {op for selector in surfaces["selectors"].values()
                        for op in selector["allowed_operations"]}
        self.assertEqual(active_selectors, set(surfaces["selectors"]))
        self.assertEqual(active_accessors, {key for key, row in surfaces["accessors"].items() if row["disposition"] == "ACTIVE_ADMITTED"})
        operation_rows = {e["id"]: e for e in ledger["entries"] if e["registry_family"] == "rule_operations"}
        self.assertLessEqual(active_ops, consumed_ops)
        self.assertLessEqual(consumed_ops, set(operation_rows))
        self.assertTrue(all(operation_rows[op]["admission_disposition"] in {"ACTIVE_ADMITTED", "DORMANT_NONSELECTABLE"} for op in consumed_ops))
        self.assertTrue(all(operation_rows[op].get("activation_trigger") for op in consumed_ops - active_ops))
        primitives = [e for e in ledger["entries"] if e["registry_family"] == "activity_primitives"]
        core = _load(CORE)
        self.assertEqual(len(primitives), len(core["registries"]["activity_primitives"]))
        self.assertTrue(all("S6D-06" in e["activation_trigger"] for e in primitives if e["admission_disposition"] == "DORMANT_NONSELECTABLE"))
        self.assertTrue(all(e["realization_state"] == "COMPLETE" for e in primitives if e["admission_disposition"] == "ACTIVE_ADMITTED"))

    def test_package_plan_namespaces_and_failure_distinctions(self):
        core, ledger = _load(CORE), load_catalog_admission_ledger(ROOT)
        plan = ledger["ruleset_package_admission"]
        expected_claims = {item.removeprefix("definition.") + ".*"
                           for item in core["registries"]["content_definition_kinds"]}
        self.assertEqual(plan["artifact_kind"], "NON_RUNTIME_ADMISSION_PLAN")
        self.assertIs(plan["selectable_now"], False)
        self.assertEqual(set(plan["namespace_claims"]), expected_claims)
        self.assertEqual(plan["failure_mapping"]["required_reasons"], EXPECTED_REASONS)
        self.assertEqual(plan["failure_mapping"]["top_level_code"], "failure.catalog_context_incompatible")
        self.assertEqual(plan["failure_mapping"]["unsupported_capability_surface"], "runtime.catalog_gap_report")

    def test_retired_ids_and_owner_wording_repairs(self):
        core_text = json.dumps(_load(CORE))
        for retired in ("world.relationship", "world.timeline_marker", "runtime.dirty_record",
                        "runtime.publication_batch", "runtime.execution_segment",
                        "runtime.resolution_chain"):
            self.assertNotIn(retired, core_text)
        structures = (ROOT / "DEV/ARCHITECTURE/ENTITY_STRUCTURES.md").read_text(encoding="utf-8")
        combat = (ROOT / "GAME/CORE/COMBAT.md").read_text(encoding="utf-8")
        rewards = (ROOT / "GAME/CORE/REWARDS.md").read_text(encoding="utf-8")
        pc = (ROOT / "GAME/SCHEMA/pc.schema.yaml").read_text(encoding="utf-8")
        self.assertNotIn("| `world.relationship` |", structures)
        self.assertIn("`world.encounter`", structures)
        self.assertIn("`active_procedure_id`", structures)
        self.assertIn("`runtime.procedure`", combat)
        self.assertIn("`world.encounter`", combat)
        self.assertIn("`definition.asset`", rewards)
        self.assertIn("`world.asset`", rewards)
        self.assertIn("`world.knowledge`", rewards)
        self.assertIn("significant items reference `world.asset` IDs", pc)
        self.assertIn("non-authoritative projection/input surfaces", pc)


if __name__ == "__main__":
    unittest.main()
