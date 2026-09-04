"""Regression coverage for the semantically partitioned Activity primitive contracts.

`DEV/CATALOG/activity-primitive-contracts.json` was one physical monolith. It is now
`DEV/CATALOG/activity-primitive-contracts/manifest.json` plus
`shared/value_contracts.json`, `shared/read_contracts.json` and one
`primitives/<primitive_id>.json` shard per registered primitive, assembled into the
same logical contract by `DEV/TOOLS/activity_primitive_contracts.py`. These tests
guard the physical split itself: schema-valid manifest/shards, exact primitive
accounting against `DEV/CATALOG/core-catalog.json`, value/read-dependency closure,
BINDING local-resolution, and the canonical loader's fail-closed rejection of a
malformed physical layout.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from activity_primitive_contracts import (  # noqa: E402
    ActivityPrimitiveContractsError,
    load_activity_primitive_contracts,
)

CORE = ROOT / "DEV/CATALOG/core-catalog.json"
TOPOLOGY_DIR = ROOT / "DEV/CATALOG/activity-primitive-contracts"
MANIFEST_PATH = TOPOLOGY_DIR / "manifest.json"
PRIMITIVES_DIR = TOPOLOGY_DIR / "primitives"
SHARED_DIR = TOPOLOGY_DIR / "shared"
LOGICAL_SCHEMA_PATH = ROOT / "DEV/SCHEMAS/activity-primitive-contracts.schema.json"
MANIFEST_SCHEMA_PATH = ROOT / "DEV/SCHEMAS/activity-primitive-contracts-manifest.schema.json"
PRIMITIVE_SCHEMA_PATH = ROOT / "DEV/SCHEMAS/activity-primitive-contracts-primitive.schema.json"
VALUE_SCHEMA_PATH = ROOT / "DEV/SCHEMAS/activity-primitive-contracts-shared-value-contracts.schema.json"
READ_SCHEMA_PATH = ROOT / "DEV/SCHEMAS/activity-primitive-contracts-shared-read-contracts.schema.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _schema_registry():
    result = Registry()
    for path in ROOT.glob("DEV/SCHEMAS/*.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in schema:
            result = result.with_resource(schema["$id"], Resource.from_contents(schema))
    return result


def _minimal_contract(primitive_id, **overrides):
    base = {
        "primitive_id": primitive_id, "family": "SELECTION", "execution_kind": "CALCULATION",
        "realization_state": "QUARANTINED", "selection_state": "DORMANT_NONSELECTABLE",
        "activation_trigger": "EXACT_CLOSED_EVENT_VARIANT_AND_ACTIVE_DEPENDENCIES",
        "arguments": {}, "results": {}, "reads": [],
        "rng": {"policy": "NONE"},
        "prospective_outputs": {"transition_kinds": [], "event_kinds": [], "state_delta_policy": "PRIMITIVE_LOCAL_TYPED_PROSPECTIVE_ONLY"},
        "atomicity": {"owner": "EXECUTION_SEGMENT", "policy": "x"},
        "suspension": {"kind": "NONE", "retention": "x"},
        "failures": [], "bounds": [],
        "evidence": {"commit_disposition_owner": "EXECUTION_SEGMENT", "committed_fact_owner": "MECHANICAL_EVENT", "outcome_owner": "RESOLUTION_RECEIPT", "trace_policy": "x"},
    }
    base.update(overrides)
    return base


def _minimal_matrix(**overrides):
    base = {
        "subject_policy": "x", "storage_policy": "x", "failure_policy": "EXACT_CONTRACT_FAILURE_CODES",
        "validation_policy": "EXACT_CONTRACT_ARGUMENT_AND_RESULT_VALUE_CONTRACTS",
        "segment_semantics": "QUARANTINED_NO_EXECUTION", "compiler_form_propagation": "NOT_COMPILER_FORM",
        "activation_dependencies": {"requires_exact_seed_consumer": True, "required_active_primitive_ids": [], "required_active_value_kinds": []},
        "causal_recovery": "NOT_APPLICABLE", "chronology_barrier": "NOT_APPLICABLE",
    }
    base.update(overrides)
    return base


def _write_minimal_valid_tree(root):
    """A minimal two-primitive tree that satisfies the loader and both physical schemas."""
    _write(root / "DEV/CATALOG/core-catalog.json", {
        "registries": {"activity_primitives": ["op.select_targets", "op.roll"]},
    })
    _write(root / "DEV/CATALOG/activity-primitive-contracts/manifest.json", {
        "schema_name": "hdm_activity_primitive_contracts", "schema_version": 1,
        "catalog_generation": "test", "owner": "test-owner", "laws": {"a_law": "x"},
        "primitive_shards": ["op.select_targets", "op.roll"],
    })
    _write(root / "DEV/CATALOG/activity-primitive-contracts/shared/value_contracts.json", {
        "role": {"owner": "test", "validation": "EXACT_NAMED_CONTRACT", "type": "string"},
    })
    _write(root / "DEV/CATALOG/activity-primitive-contracts/shared/read_contracts.json", {
        "SELECTOR": [], "ACCESSOR": [], "INVOCATION_FACT": [], "DOMAIN_OWNER": [], "INFRASTRUCTURE": [],
    })
    for pid in ("op.select_targets", "op.roll"):
        _write(root / f"DEV/CATALOG/activity-primitive-contracts/primitives/{pid}.json", {
            "primitive_id": pid,
            "contract": _minimal_contract(pid),
            "validation_matrix": _minimal_matrix(),
        })


class RealRepositoryActivityPrimitiveSplitTests(unittest.TestCase):
    """Checks against the tracked repository's actual physical split."""

    def test_manifest_schema_valid(self):
        schema = _load(MANIFEST_SCHEMA_PATH)
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema, registry=_schema_registry()).validate(_load(MANIFEST_PATH))

    def test_every_primitive_shard_schema_valid(self):
        schema = _load(PRIMITIVE_SCHEMA_PATH)
        jsonschema.Draft202012Validator.check_schema(schema)
        registry = _schema_registry()
        shard_paths = sorted(PRIMITIVES_DIR.glob("*.json"))
        self.assertEqual(len(shard_paths), 31)
        for path in shard_paths:
            jsonschema.Draft202012Validator(schema, registry=registry).validate(_load(path))

    def test_shared_value_and_read_contracts_schema_valid(self):
        registry = _schema_registry()
        jsonschema.Draft202012Validator(_load(VALUE_SCHEMA_PATH), registry=registry).validate(
            _load(SHARED_DIR / "value_contracts.json")
        )
        jsonschema.Draft202012Validator(_load(READ_SCHEMA_PATH), registry=registry).validate(
            _load(SHARED_DIR / "read_contracts.json")
        )

    def test_31_current_primitive_identities_exactly_once(self):
        core = _load(CORE)["registries"]["activity_primitives"]
        self.assertEqual(len(core), 31)
        manifest = _load(MANIFEST_PATH)
        shard_files = {p.stem for p in PRIMITIVES_DIR.glob("*.json")}
        self.assertEqual(set(core), set(manifest["primitive_shards"]))
        self.assertEqual(set(core), shard_files)
        self.assertEqual(len(manifest["primitive_shards"]), len(set(manifest["primitive_shards"])))

    def test_filename_identity_and_contract_identity_agree(self):
        for path in PRIMITIVES_DIR.glob("*.json"):
            shard = _load(path)
            self.assertEqual(shard["primitive_id"], path.stem)
            self.assertEqual(shard["contract"]["primitive_id"], path.stem)

    def test_one_contract_and_one_matrix_per_shard_colocated(self):
        for path in PRIMITIVES_DIR.glob("*.json"):
            shard = _load(path)
            self.assertEqual(set(shard), {"primitive_id", "contract", "validation_matrix"})

    def test_shared_vocabularies_are_not_duplicated_into_manifest_or_shards(self):
        manifest = _load(MANIFEST_PATH)
        self.assertNotIn("value_contracts", manifest)
        self.assertNotIn("read_contracts", manifest)
        for path in PRIMITIVES_DIR.glob("*.json"):
            shard = _load(path)
            self.assertNotIn("value_contracts", shard["contract"])
            self.assertNotIn("read_contracts", shard["contract"])

    def test_core_manifest_contracts_matrix_exact_set_equality(self):
        core = set(_load(CORE)["registries"]["activity_primitives"])
        ledger = load_activity_primitive_contracts(ROOT)
        contract_ids = {c["primitive_id"] for c in ledger["contracts"]}
        matrix_ids = set(ledger["primitive_validation_matrix"])
        manifest_ids = set(_load(MANIFEST_PATH)["primitive_shards"])
        self.assertEqual(core, manifest_ids)
        self.assertEqual(core, contract_ids)
        self.assertEqual(core, matrix_ids)
        self.assertEqual(len(ledger["contracts"]), 31)

    def test_deterministic_assembly_and_order_independent_of_filesystem_enumeration(self):
        first = load_activity_primitive_contracts(ROOT)
        second = load_activity_primitive_contracts(ROOT)
        self.assertEqual([c["primitive_id"] for c in first["contracts"]], [c["primitive_id"] for c in second["contracts"]])
        core_order = _load(CORE)["registries"]["activity_primitives"]
        self.assertEqual([c["primitive_id"] for c in first["contracts"]], core_order)

    def test_argument_and_result_value_kind_closure(self):
        ledger = load_activity_primitive_contracts(ROOT)
        value_kinds = set(ledger["value_contracts"])
        for contract in ledger["contracts"]:
            for spec in (*contract["arguments"].values(), *contract["results"].values()):
                self.assertIn(spec["value_kind"], value_kinds)

    def test_required_active_value_kind_and_primitive_closure(self):
        ledger = load_activity_primitive_contracts(ROOT)
        value_kinds = set(ledger["value_contracts"])
        primitive_ids = {c["primitive_id"] for c in ledger["contracts"]}
        for matrix in ledger["primitive_validation_matrix"].values():
            deps = matrix["activation_dependencies"]
            self.assertLessEqual(set(deps["required_active_value_kinds"]), value_kinds)
            self.assertLessEqual(set(deps["required_active_primitive_ids"]), primitive_ids)

    def test_shared_read_dependency_closure(self):
        ledger = load_activity_primitive_contracts(ROOT)
        read_contracts = ledger["read_contracts"]
        for contract in ledger["contracts"]:
            for dependency in contract["reads"]:
                if dependency["kind"] in {"SELECTOR", "ACCESSOR", "DOMAIN_OWNER", "INFRASTRUCTURE", "INVOCATION_FACT"}:
                    self.assertIn(dependency["id"], read_contracts[dependency["kind"]])

    def test_binding_reads_resolve_primitive_locally_not_through_a_shared_family(self):
        ledger = load_activity_primitive_contracts(ROOT)
        self.assertNotIn("BINDING", ledger["read_contracts"])
        binding_count = 0
        for contract in ledger["contracts"]:
            local_ids = set(contract["arguments"]) | set(contract["results"])
            local_ids |= {spec["value_kind"] for spec in contract["arguments"].values()}
            local_ids |= {spec["value_kind"] for spec in contract["results"].values()}
            for dependency in contract["reads"]:
                if dependency["kind"] == "BINDING":
                    binding_count += 1
                    self.assertIn(dependency["id"], local_ids)
        self.assertGreater(binding_count, 0)

    def test_assembled_object_validates_against_existing_logical_schema(self):
        schema = _load(LOGICAL_SCHEMA_PATH)
        jsonschema.Draft202012Validator.check_schema(schema)
        ledger = load_activity_primitive_contracts(ROOT)
        jsonschema.Draft202012Validator(schema, registry=_schema_registry()).validate(ledger)

    def test_no_physical_monolith_remains(self):
        self.assertFalse((ROOT / "DEV/CATALOG/activity-primitive-contracts.json").exists())


class LoaderFailClosedTests(unittest.TestCase):
    """The canonical loader must reject every malformed physical layout it is handed."""

    def _root(self, tmp):
        root = Path(tmp)
        _write_minimal_valid_tree(root)
        return root

    def test_valid_minimal_tree_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            contract = load_activity_primitive_contracts(root)
            self.assertEqual({c["primitive_id"] for c in contract["contracts"]}, {"op.select_targets", "op.roll"})

    def test_missing_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/activity-primitive-contracts/manifest.json").unlink()
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_missing_declared_primitive_shard_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json").unlink()
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_undeclared_primitive_shard_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest_path = root / "DEV/CATALOG/activity-primitive-contracts/manifest.json"
            manifest = _load(manifest_path)
            manifest["primitive_shards"] = ["op.select_targets"]
            _write(manifest_path, manifest)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_duplicate_declared_primitive_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            manifest_path = root / "DEV/CATALOG/activity-primitive-contracts/manifest.json"
            manifest = _load(manifest_path)
            manifest["primitive_shards"] = ["op.select_targets", "op.roll", "op.select_targets"]
            _write(manifest_path, manifest)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_filename_declared_identity_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            shard_path = root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
            shard = _load(shard_path)
            shard["primitive_id"] = "op.renamed"
            _write(shard_path, shard)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_contract_primitive_id_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            shard_path = root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
            shard = _load(shard_path)
            shard["contract"]["primitive_id"] = "op.select_targets"
            _write(shard_path, shard)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_core_catalog_inventory_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            core_path = root / "DEV/CATALOG/core-catalog.json"
            core = _load(core_path)
            core["registries"]["activity_primitives"].append("op.extra_not_declared")
            _write(core_path, core)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_missing_shared_value_contracts_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/activity-primitive-contracts/shared/value_contracts.json").unlink()
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_missing_shared_read_contracts_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            (root / "DEV/CATALOG/activity-primitive-contracts/shared/read_contracts.json").unlink()
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)

    def test_extra_unwrapped_shard_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp)
            shard_path = root / "DEV/CATALOG/activity-primitive-contracts/primitives/op.roll.json"
            shard = _load(shard_path)
            shard["extra_key"] = "unexpected"
            _write(shard_path, shard)
            with self.assertRaises(ActivityPrimitiveContractsError):
                load_activity_primitive_contracts(root)


if __name__ == "__main__":
    unittest.main()
