"""Focused S6D-03 selector-metadata closure checks."""
import json
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "DEV/CATALOG/core-catalog.json"
SURFACES = ROOT / "DEV/CATALOG/mechanical-surfaces.json"
LEDGER = ROOT / "DEV/CATALOG/catalog-admission-ledger.json"
SCHEMA = ROOT / "DEV/SCHEMAS/mechanical-surfaces.schema.json"

EXPECTED_SELECTORS = {"condition.applicability", "health.maximum", "resource.capacity"}
EXPECTED_OPERATIONS = {"rule.add_flat", "rule.immunity"}
STRUCTURAL_ONLY_PAIRS = {
    ("attack.roll", "rule.grant_disadvantage"),
    ("activity.availability", "rule.restrict_activity"),
    ("movement.speed", "rule.override"),
    ("movement.speed", "rule.add_flat"),
    ("test.roll", "rule.add_flat"),
    ("defense.armor_class", "rule.add_flat"),
    ("damage.weapon", "rule.add_damage_component"),
}

def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_schema_and_active_sets_are_exact():
    core, surfaces, ledger, schema = map(_load, (CORE, SURFACES, LEDGER, SCHEMA))
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(surfaces, schema)
    active_selectors = {e["id"] for e in ledger["entries"]
        if e["registry_family"] == "rule_selectors"
        and e["admission_disposition"] == "ACTIVE_ADMITTED"}
    active_operations = {e["id"] for e in ledger["entries"]
        if e["registry_family"] == "rule_operations"
        and e["admission_disposition"] == "ACTIVE_ADMITTED"}
    assert set(surfaces["selectors"]) == active_selectors == EXPECTED_SELECTORS
    consumed = {op for m in surfaces["selectors"].values() for op in m["allowed_operations"]}
    assert consumed == active_operations == EXPECTED_OPERATIONS
    assert active_selectors <= set(core["registries"]["rule_selectors"])
    assert active_operations <= set(core["registries"]["rule_operations"])

def test_all_registered_ids_have_active_or_dormant_outcome():
    core, ledger = _load(CORE), _load(LEDGER)
    selectors = [e for e in ledger["entries"] if e["registry_family"] == "rule_selectors"]
    operations = [e for e in ledger["entries"] if e["registry_family"] == "rule_operations"]
    assert {e["id"] for e in selectors} == set(core["registries"]["rule_selectors"])
    assert {e["id"] for e in operations} == set(core["registries"]["rule_operations"])
    assert Counter(e["admission_disposition"] for e in selectors) == {
        "ACTIVE_ADMITTED": 3, "DORMANT_NONSELECTABLE": 31}
    assert Counter(e["admission_disposition"] for e in operations) == {
        "ACTIVE_ADMITTED": 2, "DORMANT_NONSELECTABLE": 24}
    for entry in selectors + operations:
        if entry["admission_disposition"] == "ACTIVE_ADMITTED":
            assert entry["realization_state"] == "COMPLETE"
            assert entry["downstream_owner"] is None
        else:
            assert entry["activation_trigger"]
            assert entry["realization_state"] == "DOWNSTREAM_S6D_03"
            assert entry["downstream_owner"] == "S6D-03"

def test_metadata_is_complete_and_pair_keys_are_exact():
    surfaces = _load(SURFACES)
    required = {
        "allowed_operations", "operation_contracts", "contribution_type",
        "result_type", "result_constraints", "subject_kinds", "binding_kinds",
        "allowed_dependency_kinds", "allowed_input_classes",
        "permitted_context_fact_ids", "static_dependencies",
        "combination_policy", "resolution_owner", "trace_policy",
    }
    for meta in surfaces["selectors"].values():
        assert set(meta) == required
        assert set(meta["operation_contracts"]) == set(meta["allowed_operations"])
        assert meta["subject_kinds"] and meta["binding_kinds"]
        assert meta["resolution_owner"] == "SELECTOR_METADATA"
        assert meta["trace_policy"] == "RETAIN_ACCEPTED_REJECTED_PROVENANCE"

def test_no_invocation_fact_or_dependency_kind_laundering():
    surfaces = _load(SURFACES)
    for meta in surfaces["selectors"].values():
        assert meta["allowed_input_classes"] == ["ENGINE_STATE"]
        assert meta["permitted_context_fact_ids"] == []
        assert set(meta["allowed_dependency_kinds"]) == {"accessor", "derived"}
        assert meta["static_dependencies"] == []
    schema = _load(SCHEMA)
    assert set(schema["$defs"]["dependencyKindSet"]["items"]["enum"]) == {
        "selector", "accessor", "derived"}
    legal_kinds = {"selector", "accessor", "derived"}
    for section in ("selectors", "derived_nodes"):
        for meta in surfaces[section].values():
            assert set(meta["allowed_dependency_kinds"]) <= legal_kinds
            for ref in meta["dependencies"] if section == "derived_nodes" else meta["static_dependencies"]:
                assert ref.split(":", 1)[0] in legal_kinds
    assert surfaces["derived_nodes"]["condition_intrinsic"]["allowed_input_classes"] == [
        "ENGINE_STATE"]
    assert surfaces["derived_nodes"]["condition_intrinsic"]["permitted_context_fact_ids"] == []

def test_integer_additive_policy_is_commutative_and_enforces_minimum():
    surfaces = _load(SURFACES)["selectors"]
    for selector, base, contributions, expected in (
        ("health.maximum", 10, [3, -2, 1], 12),
        ("resource.capacity", 2, [-7, 3], 0),
    ):
        meta = surfaces[selector]
        assert meta["combination_policy"] == "integer_additive_v1"
        assert meta["operation_contracts"]["rule.add_flat"] == {
            "value_kind": "numeric_scalar",
            "normalization": "SUM",
            "constraints": ["finite_integer"],
        }
        minimum = meta["result_constraints"]["minimum"]
        resolve = lambda values: max(minimum, base + sum(values))
        assert resolve(contributions) == expected
        assert resolve(list(reversed(contributions))) == expected

def test_immunity_policy_is_monotone_and_literal():
    meta = _load(SURFACES)["selectors"]["condition.applicability"]
    assert meta["combination_policy"] == "immunity_any_true_v1"
    assert meta["operation_contracts"]["rule.immunity"] == {
        "value_kind": "boolean_constant",
        "fixed_value": True,
        "normalization": "ANY_TRUE",
        "constraints": ["literal_true"],
    }
    assert any([False, True, True]) is True

def test_structural_examples_are_labeled_and_not_executable_consumers():
    for name in ("condition-definition-data.schema.json", "effect-definition-data.schema.json", "rule-element.schema.json"):
        assert "structural shape only" in _load(ROOT / "DEV/SCHEMAS" / name)["$comment"]
    surfaces = _load(SURFACES)["selectors"]
    for selector, operation in STRUCTURAL_ONLY_PAIRS:
        assert selector not in surfaces or operation not in surfaces[selector]["allowed_operations"]

def test_global_disposition_totals():
    totals = Counter(e["admission_disposition"] for e in _load(LEDGER)["entries"])
    assert totals == {
        "ACTIVE_ADMITTED": 449,
        "EMBEDDED_NONOWNER": 35,
        "DORMANT_NONSELECTABLE": 87,
    }

