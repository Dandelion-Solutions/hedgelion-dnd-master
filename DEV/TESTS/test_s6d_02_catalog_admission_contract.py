"""Focused S6D-02 catalog-admission contract checks."""
import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "DEV/CATALOG/core-catalog.json"
LEDGER = ROOT / "DEV/CATALOG/catalog-admission-ledger.json"
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

def test_schema_and_exact_bidirectional_trace():
    core, ledger, schema = _load(CORE), _load(LEDGER), _load(SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(ledger, schema)
    core_pairs = _pairs(core)
    ledger_pairs = [(entry["registry_family"], entry["id"]) for entry in ledger["entries"]]
    assert len(core_pairs) == len(ledger_pairs) == 571
    assert len(set(ledger_pairs)) == 571
    assert set(core_pairs) == set(ledger_pairs)
    assert set(core["registries"]) == set(ledger["family_policies"])
    assert all(entry["profile"] == entry["registry_family"] for entry in ledger["entries"])

def test_item_level_evidence_disposition_and_realization():
    ledger = _load(LEDGER)
    strata = Counter()
    dispositions = Counter()
    for entry in ledger["entries"]:
        strata[entry["scope_stratum"]] += 1
        dispositions[entry["admission_disposition"]] += 1
        assert entry["evidence_citation"].strip()
        assert entry["consumer_or_dependency"].strip()
        assert entry["semantic_owner"].strip()
        if entry["scope_stratum"] == "S6D_PRIMARY":
            assert entry["evidence_class"] == "ACCEPTED_OWNER_REQUIREMENT"
            assert entry["realization_state"] != "INHERITED_ACTIVE"
        if entry["scope_stratum"] == "INHERITED_ROUND2":
            assert entry["realization_state"] == "INHERITED_ACTIVE"
        if entry["admission_disposition"] == "EMBEDDED_NONOWNER":
            assert entry["containing_owner"].strip()
            assert "exact accepted interface owner" not in entry["containing_owner"]
            assert entry["registry_family"] == "protocol_value_kinds"
        if entry["admission_disposition"] == "DORMANT_NONSELECTABLE":
            assert entry["activation_trigger"].strip()
        if entry["realization_state"] == "INHERITED_ACTIVE":
            assert entry["downstream_owner"]
        if entry["realization_state"].startswith("DOWNSTREAM_S6D_"):
            suffix = entry["realization_state"].removeprefix("DOWNSTREAM_S6D_")
            assert entry["downstream_owner"] == f"S6D-{suffix}"
        if entry["realization_state"] == "COMPLETE":
            assert entry["downstream_owner"] is None
        assert entry["admission_disposition"] != "STALE_REMOVE"
    assert strata == {"S6D_PRIMARY": 192, "ENGINE_ENUM_CONSISTENCY": 276, "INHERITED_ROUND2": 103}
    assert dispositions == {"ACTIVE_ADMITTED": 450, "EMBEDDED_NONOWNER": 35, "DORMANT_NONSELECTABLE": 86}

def test_census_arithmetic_matches_entries():
    ledger = _load(LEDGER)
    by_family = {}
    for entry in ledger["entries"]:
        row = by_family.setdefault(entry["registry_family"], Counter())
        row["count"] += 1
        row[entry["admission_disposition"]] += 1
    assert len(ledger["registry_census"]) == 67
    for census in ledger["registry_census"]:
        actual = by_family[census["registry_family"]]
        assert census["count"] == actual["count"]
        assert census["admitted"] == actual["ACTIVE_ADMITTED"]
        assert census["embedded_nonowner"] == actual["EMBEDDED_NONOWNER"]
        assert census["dormant_nonselectable"] == actual["DORMANT_NONSELECTABLE"]
        assert census["stale_remove"] == actual["STALE_REMOVE"]


def test_executable_capabilities_are_supported_or_quarantined():
    ledger = _load(LEDGER)
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
    assert active_selectors == set(surfaces["selectors"])
    assert active_accessors == set(surfaces["accessors"])
    assert active_ops == consumed_ops
    primitives = [e for e in ledger["entries"] if e["registry_family"] == "activity_primitives"]
    assert len(primitives) == 31
    assert all(e["admission_disposition"] == "DORMANT_NONSELECTABLE" for e in primitives)
    assert all("S6D-06" in e["activation_trigger"] for e in primitives)

def test_package_plan_namespaces_and_failure_distinctions():
    core, ledger = _load(CORE), _load(LEDGER)
    plan = ledger["ruleset_package_admission"]
    expected_claims = {item.removeprefix("definition.") + ".*"
                       for item in core["registries"]["content_definition_kinds"]}
    assert plan["artifact_kind"] == "NON_RUNTIME_ADMISSION_PLAN"
    assert plan["selectable_now"] is False
    assert set(plan["namespace_claims"]) == expected_claims
    assert plan["failure_mapping"]["required_reasons"] == EXPECTED_REASONS
    assert plan["failure_mapping"]["top_level_code"] == "failure.catalog_context_incompatible"
    assert plan["failure_mapping"]["unsupported_capability_surface"] == "runtime.catalog_gap_report"

def test_retired_ids_and_owner_wording_repairs():
    core_text = json.dumps(_load(CORE))
    for retired in ("world.relationship", "world.timeline_marker", "runtime.dirty_record",
                    "runtime.publication_batch", "runtime.execution_segment",
                    "runtime.resolution_chain"):
        assert retired not in core_text
    structures = (ROOT / "DEV/ARCHITECTURE/ENTITY_STRUCTURES.md").read_text(encoding="utf-8")
    combat = (ROOT / "GAME/CORE/COMBAT.md").read_text(encoding="utf-8")
    rewards = (ROOT / "GAME/CORE/REWARDS.md").read_text(encoding="utf-8")
    pc = (ROOT / "GAME/SCHEMA/pc.schema.yaml").read_text(encoding="utf-8")
    assert "| `world.relationship` |" not in structures
    assert "`world.encounter`" in structures and "`active_procedure_id`" in structures
    assert "`runtime.procedure`" in combat and "`world.encounter`" in combat
    assert "`definition.asset`" in rewards and "`world.asset`" in rewards and "`world.knowledge`" in rewards
    assert "significant items reference `world.asset` IDs" in pc
    assert "non-authoritative projection/input surfaces" in pc
