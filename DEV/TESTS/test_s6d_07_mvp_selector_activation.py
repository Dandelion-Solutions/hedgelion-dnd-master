import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "DEV" / "CATALOG"
REQUIRED = {"attack.roll", "save.roll", "check.roll", "defense.armor_class", "damage.received", "healing.received", "spell.dc"}
REQUIRED_OPERATIONS = {"rule.grant_advantage"}


def test_mvp_primitive_selector_dependencies_are_complete_and_admitted():
    surfaces = json.loads((CATALOG / "mechanical-surfaces.json").read_text(encoding="utf-8"))
    ledger = json.loads((CATALOG / "catalog-admission-ledger.json").read_text(encoding="utf-8"))
    selectors = surfaces["selectors"]
    assert REQUIRED <= set(selectors)
    for selector_id in REQUIRED:
        row = selectors[selector_id]
        assert row["resolution_owner"] == "SELECTOR_METADATA"
        assert row["allowed_input_classes"] == ["ENGINE_STATE"]
        assert row["trace_policy"] == "RETAIN_ACCEPTED_REJECTED_PROVENANCE"
    admissions = {row["id"]: row for row in ledger["entries"] if row["id"] in REQUIRED}
    assert set(admissions) == REQUIRED
    for row in admissions.values():
        assert row["realization_state"] == "COMPLETE"
        assert row["admission_disposition"] == "ACTIVE_ADMITTED"
        assert row["downstream_owner"] == "S6D-07"
    operation_admissions = {row["id"]: row for row in ledger["entries"] if row["id"] in REQUIRED_OPERATIONS}
    assert set(operation_admissions) == REQUIRED_OPERATIONS
    for row in operation_admissions.values():
        assert row["realization_state"] == "COMPLETE"
        assert row["admission_disposition"] == "ACTIVE_ADMITTED"
        assert row["downstream_owner"] == "S6D-07"
    assert "rule.grant_advantage" in selectors["attack.roll"]["allowed_operations"]
    assert selectors["attack.roll"]["operation_contracts"]["rule.grant_advantage"]["fixed_value"] is True
