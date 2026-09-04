"""Regression coverage for the semantically partitioned catalog-admission ledger.

`DEV/CATALOG/catalog-admission-ledger.json` was one physical monolith. It is now
`DEV/CATALOG/catalog-admission-ledger/manifest.json` plus one
`DEV/CATALOG/catalog-admission-ledger/families/<registry_family>.json` shard per
registry family, assembled into the same logical ledger contract by
`DEV/TOOLS/catalog_admission.py`. These tests guard the physical split itself:
schema-valid manifest/shards, exact family/entry accounting against
`DEV/CATALOG/core-catalog.json`, and the canonical loader's fail-closed rejection
of a malformed physical layout.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from catalog_admission import CatalogAdmissionLedgerError, load_catalog_admission_ledger  # noqa: E402

CORE = ROOT / "DEV/CATALOG/core-catalog.json"
MANIFEST_PATH = ROOT / "DEV/CATALOG/catalog-admission-ledger/manifest.json"
FAMILIES_DIR = ROOT / "DEV/CATALOG/catalog-admission-ledger/families"
LOGICAL_SCHEMA = ROOT / "DEV/SCHEMAS/catalog-admission-ledger.schema.json"
MANIFEST_SCHEMA = ROOT / "DEV/SCHEMAS/catalog-admission-ledger-manifest.schema.json"
FAMILY_SCHEMA = ROOT / "DEV/SCHEMAS/catalog-admission-ledger-family.schema.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _write_minimal_valid_tree(root):
    """A minimal two-family tree that satisfies the loader and both physical schemas."""
    _write(root / "DEV/CATALOG/core-catalog.json", {
        "registries": {"fam_a": ["a.1", "a.2"], "fam_b": ["b.1"]},
    })
    _write(root / "DEV/CATALOG/catalog-admission-ledger/manifest.json", {
        "schema_name": "hdm_catalog_admission_ledger", "schema_version": 1,
        "catalog_generation": "test", "source_registry": "DEV/CATALOG/core-catalog.json",
        "decision_owner": "test-owner", "laws": {}, "ruleset_package_admission": {},
        "retired_reference_audit": [], "family_shards": ["fam_a", "fam_b"],
    })

    def entry(family, entry_id):
        return {
            "registry_family": family, "id": entry_id, "profile": family,
            "scope_stratum": "S6D_PRIMARY", "admission_disposition": "ACTIVE_ADMITTED",
            "evidence_class": "ACCEPTED_OWNER_REQUIREMENT", "evidence_citation": "test",
            "semantic_owner": "test", "consumer_or_dependency": "test",
            "realization_state": "COMPLETE", "downstream_owner": None,
        }

    def census(family, count):
        return {
            "registry_family": family, "count": count, "scope_stratum": "S6D_PRIMARY",
            "admitted": count, "embedded_nonowner": 0, "dormant_nonselectable": 0, "stale_remove": 0,
        }

    _write(root / "DEV/CATALOG/catalog-admission-ledger/families/fam_a.json", {
        "registry_family": "fam_a", "registry_census": census("fam_a", 2),
        "family_policy": {}, "entries": [entry("fam_a", "a.1"), entry("fam_a", "a.2")],
    })
    _write(root / "DEV/CATALOG/catalog-admission-ledger/families/fam_b.json", {
        "registry_family": "fam_b", "registry_census": census("fam_b", 1),
        "family_policy": {}, "entries": [entry("fam_b", "b.1")],
    })


class RealRepositoryLedgerSplitTests(unittest.TestCase):
    """Checks against the tracked repository's actual physical split."""

    def test_manifest_schema_valid(self):
        schema = _load(MANIFEST_SCHEMA)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(_load(MANIFEST_PATH), schema)

    def test_every_family_shard_schema_valid(self):
        schema = _load(FAMILY_SCHEMA)
        jsonschema.Draft202012Validator.check_schema(schema)
        shard_paths = sorted(FAMILIES_DIR.glob("*.json"))
        self.assertTrue(shard_paths)
        for path in shard_paths:
            jsonschema.validate(_load(path), schema)

    def test_family_set_matches_core_catalog_exactly_once(self):
        core = _load(CORE)
        manifest = _load(MANIFEST_PATH)
        family_shards = manifest["family_shards"]
        self.assertEqual(len(family_shards), len(set(family_shards)))
        self.assertEqual(set(family_shards), set(core["registries"]))
        shard_files = {p.stem for p in FAMILIES_DIR.glob("*.json")}
        self.assertEqual(shard_files, set(family_shards))

    def test_no_duplicate_ids_and_no_cross_family_entries(self):
        seen = set()
        for path in FAMILIES_DIR.glob("*.json"):
            shard = _load(path)
            family = shard["registry_family"]
            for entry in shard["entries"]:
                self.assertEqual(entry["registry_family"], family)
                key = (entry["registry_family"], entry["id"])
                self.assertNotIn(key, seen)
                seen.add(key)

    def test_census_matches_actual_shard_contents(self):
        from collections import Counter
        for path in FAMILIES_DIR.glob("*.json"):
            shard = _load(path)
            census = shard["registry_census"]
            counts = Counter(e["admission_disposition"] for e in shard["entries"])
            self.assertEqual(census["count"], len(shard["entries"]))
            self.assertEqual(census["admitted"], counts["ACTIVE_ADMITTED"])
            self.assertEqual(census["embedded_nonowner"], counts["EMBEDDED_NONOWNER"])
            self.assertEqual(census["dormant_nonselectable"], counts["DORMANT_NONSELECTABLE"])
            self.assertEqual(census["stale_remove"], counts["STALE_REMOVE"])

    def test_assembled_ledger_exact_bidirectional_trace_against_core_catalog(self):
        core = _load(CORE)
        ledger = load_catalog_admission_ledger(ROOT)
        core_pairs = {(family, item) for family, items in core["registries"].items() for item in items}
        ledger_pairs = [(e["registry_family"], e["id"]) for e in ledger["entries"]]
        self.assertEqual(len(ledger_pairs), len(set(ledger_pairs)))
        self.assertEqual(core_pairs, set(ledger_pairs))
        self.assertEqual(set(core["registries"]), set(ledger["family_policies"]))
        self.assertEqual(len(ledger["registry_census"]), len(core["registries"]))

    def test_assembled_ledger_validates_against_existing_logical_schema(self):
        """The pre-existing 69-violation drift (activation_trigger, downstream_owner
        COMPLETE-implies-null, evidence_class enum, entry-level admission_evidence)
        was repaired as part of this split: entry data corrected where the field
        had no current owner/consumer, and the schema corrected where the data
        reflected an already-accepted current contract the schema had not caught
        up with (S6D-10, the WP-18 owner-chain literal, MACHINE_CONTRACT_AND_EXACT_CONSUMER,
        ACCEPTED_HOUSE_RULES_OWNER_PLUS_EXACT_MACHINE_CONSUMER, and COMPLETE entries
        that legitimately carry a non-null closed-vocabulary downstream_owner).
        """
        schema = _load(LOGICAL_SCHEMA)
        ledger = load_catalog_admission_ledger(ROOT)
        jsonschema.validate(ledger, schema)

    def test_complete_realization_state_downstream_owner_vocabulary(self):
        """COMPLETE may carry null or any closed-vocabulary owner, never an arbitrary string."""
        schema = _load(LOGICAL_SCHEMA)
        entry_defs = schema["$defs"]["entry"]

        def make_entry(**overrides):
            base = {
                "registry_family": "fam_a", "id": "a.1", "profile": "fam_a",
                "scope_stratum": "S6D_PRIMARY", "admission_disposition": "ACTIVE_ADMITTED",
                "evidence_class": "ACCEPTED_OWNER_REQUIREMENT", "evidence_citation": "test",
                "semantic_owner": "test", "consumer_or_dependency": "test",
                "realization_state": "COMPLETE", "downstream_owner": None,
            }
            base.update(overrides)
            return base

        jsonschema.validate(make_entry(downstream_owner=None), entry_defs)
        jsonschema.validate(make_entry(downstream_owner="S6D-07"), entry_defs)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(make_entry(downstream_owner="not-a-real-owner"), entry_defs)

    def test_evidence_class_enum_is_exact_closed_current_vocabulary(self):
        schema = _load(LOGICAL_SCHEMA)
        self.assertEqual(
            set(schema["$defs"]["entry"]["properties"]["evidence_class"]["enum"]),
            {
                "ACCEPTED_OWNER_REQUIREMENT",
                "ACCEPTED_ENUM_CONSISTENCY",
                "MACHINE_CONTRACT_AND_EXACT_CONSUMER",
                "ACCEPTED_HOUSE_RULES_OWNER_PLUS_EXACT_MACHINE_CONSUMER",
            },
        )
        ledger = load_catalog_admission_ledger(ROOT)
        used = {e["evidence_class"] for e in ledger["entries"]}
        allowed = set(schema["$defs"]["entry"]["properties"]["evidence_class"]["enum"])
        self.assertTrue(used <= allowed)

    def test_no_entry_carries_the_retired_admission_evidence_field(self):
        """admission_evidence is a family_policy-level field; no entry may carry it."""
        ledger = load_catalog_admission_ledger(ROOT)
        offenders = [(e["registry_family"], e["id"]) for e in ledger["entries"] if "admission_evidence" in e]
        self.assertEqual(offenders, [])

    def test_dormant_nonselectable_entries_all_have_a_meaningful_activation_trigger(self):
        ledger = load_catalog_admission_ledger(ROOT)
        for e in ledger["entries"]:
            if e["admission_disposition"] == "DORMANT_NONSELECTABLE":
                self.assertTrue(
                    e.get("activation_trigger", "").strip(),
                    msg=f"missing activation_trigger: {(e['registry_family'], e['id'])}",
                )


class LoaderFailClosedTests(unittest.TestCase):
    """The canonical loader must reject every malformed physical layout it is handed."""

    def _root(self, tmp):
        root = Path(tmp)
        _write_minimal_valid_tree(root)
        return root

    def test_valid_minimal_tree_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            ledger = load_catalog_admission_ledger(root)
            self.assertEqual({e["id"] for e in ledger["entries"]}, {"a.1", "a.2", "b.1"})

    def test_missing_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/catalog-admission-ledger/manifest.json").unlink()
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_missing_declared_shard_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/catalog-admission-ledger/families/fam_b.json").unlink()
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_undeclared_shard_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest_path = root / "DEV/CATALOG/catalog-admission-ledger/manifest.json"
            manifest = _load(manifest_path)
            manifest["family_shards"] = ["fam_a"]
            _write(manifest_path, manifest)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_duplicate_family_in_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest_path = root / "DEV/CATALOG/catalog-admission-ledger/manifest.json"
            manifest = _load(manifest_path)
            manifest["family_shards"] = ["fam_a", "fam_b", "fam_a"]
            _write(manifest_path, manifest)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_duplicate_entry_id_within_a_shard_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            fam_b_path = root / "DEV/CATALOG/catalog-admission-ledger/families/fam_b.json"
            fam_b = _load(fam_b_path)
            duplicate = copy.deepcopy(fam_b["entries"][0])
            fam_b["entries"].append(duplicate)
            fam_b["registry_census"]["count"] += 1
            fam_b["registry_census"]["admitted"] += 1
            _write(fam_b_path, fam_b)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_entry_with_mismatched_registry_family_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            fam_a_path = root / "DEV/CATALOG/catalog-admission-ledger/families/fam_a.json"
            fam_a = _load(fam_a_path)
            fam_a["entries"][0]["registry_family"] = "fam_b"
            _write(fam_a_path, fam_a)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_census_count_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            fam_a_path = root / "DEV/CATALOG/catalog-admission-ledger/families/fam_a.json"
            fam_a = _load(fam_a_path)
            fam_a["registry_census"]["count"] = 99
            _write(fam_a_path, fam_a)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_census_disposition_arithmetic_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            fam_a_path = root / "DEV/CATALOG/catalog-admission-ledger/families/fam_a.json"
            fam_a = _load(fam_a_path)
            fam_a["registry_census"]["admitted"] = 0
            _write(fam_a_path, fam_a)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_family_inventory_mismatch_with_core_catalog_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            core_path = root / "DEV/CATALOG/core-catalog.json"
            core = _load(core_path)
            core["registries"]["fam_c"] = ["c.1"]
            _write(core_path, core)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)

    def test_shard_filename_not_matching_declared_registry_family_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            fam_a_path = root / "DEV/CATALOG/catalog-admission-ledger/families/fam_a.json"
            fam_a = _load(fam_a_path)
            fam_a["registry_family"] = "fam_a_renamed"
            _write(fam_a_path, fam_a)
            with self.assertRaises(CatalogAdmissionLedgerError):
                load_catalog_admission_ledger(root)


if __name__ == "__main__":
    unittest.main()
