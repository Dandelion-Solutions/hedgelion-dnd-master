import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
sys.path.insert(0, str(ROOT / "GAME" / "TOOLS"))

from temporal import (
    TemporalContractError,
    derive_temporal_dependency_keys,
    evaluate_temporal_binding,
    materialize_due_occurrence,
    rebuild_temporal_agenda,
    validate_current_state_replacement,
)


METRIC_BINDING = {
    "basis_id": "temporal.metric_deadline",
    "context_id": "scene:market",
    "anchor_value": 12,
    "deadline_value": 15,
    "unit_id": "unit.day",
}
ARMED_ROOT = {
    "root_ref": "world.thread:THREAD_market_siege",
    "occurrence_id": "occurrence:market-siege:1",
    "binding_id": "temporal-binding:market-siege:1",
    "occurrence_state": "ARMED",
    "binding": METRIC_BINDING,
    "dependency_keys": ["METRIC_POSITION:scene:market"],
}


def schema_registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        value = json.loads(path.read_text(encoding="utf-8"))
        if "$id" in value:
            registry = registry.with_resource(value["$id"], Resource.from_contents(value))
    return registry


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class CurrentStateChronologyTests(unittest.TestCase):
    def test_current_state_replacement_is_exactly_next_revision_and_carries_typed_anchor_evidence(self):
        current = {
            "state_revision": 7,
            "chronology_anchor_ids": ["event:market-warning"],
        }
        replacement = {
            "state_revision": 8,
            "chronology_anchor_ids": ["event:market-fall", "event:market-warning"],
        }

        self.assertEqual(
            validate_current_state_replacement(current, replacement),
            {"status": "ACCEPTED", "state_revision": 8},
        )
        with self.assertRaisesRegex(TemporalContractError, "next revision"):
            validate_current_state_replacement(current, dict(replacement, state_revision=9))
        with self.assertRaisesRegex(TemporalContractError, "frontier"):
            validate_current_state_replacement(current, dict(replacement, chronology_frontier="event:market-fall"))

    def test_metric_binding_uses_only_its_named_provider_and_preserves_bounded_uncertainty(self):
        evaluation = evaluate_temporal_binding(
            METRIC_BINDING,
            {
                "provider_id": "scene:market",
                "position": {"kind": "BOUNDED", "lower": 14, "upper": 16},
            },
        )

        self.assertEqual(evaluation.disposition, "INDETERMINATE")

        with self.assertRaisesRegex(TemporalContractError, "provider"):
            evaluate_temporal_binding(
                METRIC_BINDING,
                {"provider_id": "campaign:global", "position": {"kind": "EXACT", "value": 99}},
            )
        with self.assertRaisesRegex(TemporalContractError, "unsupported binding field"):
            evaluate_temporal_binding(
                dict(METRIC_BINDING, global_clock="campaign:now"),
                {"provider_id": "scene:market", "position": {"kind": "EXACT", "value": 15}},
            )


class WorldThreadContractTests(unittest.TestCase):
    def test_world_thread_schema_accepts_owner_local_lifecycle_without_knowledge_or_catalog_authority(self):
        schema = load_schema("world-thread-state.schema.json")
        thread = {
            "record_kind": "world.thread",
            "id": "THREAD_market_siege",
            "state_revision": 3,
            "status": "active",
            "kind": "countdown",
            "state": {"stage": "warning", "progress": {"segments": 2}},
            "temporal": {
                "binding_id": "temporal-binding:market-siege:1",
                "occurrence_id": "occurrence:market-siege:1",
                "occurrence_state": "ARMED",
                "binding": METRIC_BINDING,
                "dependency_keys": ["METRIC_POSITION:scene:market"],
            },
        }

        Draft202012Validator(schema, registry=schema_registry()).validate(thread)
        invalid = dict(thread, knowledge={"pc:one": "knows"})
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema, registry=schema_registry()).validate(invalid)
        missing_binding_identity = dict(thread, temporal=dict(thread["temporal"]))
        del missing_binding_identity["temporal"]["binding_id"]
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema, registry=schema_registry()).validate(missing_binding_identity)
        incomplete_armed = dict(thread, temporal=dict(thread["temporal"], dependency_keys=[]))
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema, registry=schema_registry()).validate(incomplete_armed)


class TemporalBindingAgendaTests(unittest.TestCase):
    def test_due_binding_produces_a_candidate_without_mutating_the_native_owner(self):
        evaluation = evaluate_temporal_binding(
            METRIC_BINDING,
            {"provider_id": "scene:market", "position": {"kind": "EXACT", "value": 15}},
        )
        candidate = materialize_due_occurrence(ARMED_ROOT, evaluation)

        self.assertEqual(candidate, {
            "status": "CANDIDATE",
            "root_ref": "world.thread:THREAD_market_siege",
            "occurrence_id": "occurrence:market-siege:1",
        })
        self.assertEqual(ARMED_ROOT["occurrence_state"], "ARMED")


class TemporalRoutingCompletenessTests(unittest.TestCase):
    def test_armed_occurrence_requires_unique_complete_typed_dependency_keys(self):
        self.assertEqual(
            derive_temporal_dependency_keys(ARMED_ROOT),
            ("METRIC_POSITION:scene:market",),
        )

        incomplete = dict(ARMED_ROOT, dependency_keys=[])
        with self.assertRaisesRegex(TemporalContractError, "dependency"):
            derive_temporal_dependency_keys(incomplete)


@unittest.skip("Recovery assertions are owned by W02.T06.")
class TemporalExecutionRecoveryTests(unittest.TestCase):
    def test_recovery_handoff_is_deferred_to_its_owner(self):
        self.fail("W02.T06 owns recovery behavior")


class ChronologyBridgeTests(unittest.TestCase):
    def test_chronology_relation_schema_requires_typed_anchor_evidence(self):
        schema = load_schema("chronology-relation-evidence.schema.json")
        relation = {
            "relation_type": "PRECEDES",
            "before_anchor_id": "event:market-warning",
            "after_anchor_id": "event:market-fall",
            "scope_id": "scene:market",
        }
        Draft202012Validator(schema, registry=schema_registry()).validate(relation)

        with self.assertRaises(ValidationError):
            Draft202012Validator(schema, registry=schema_registry()).validate(
                dict(relation, relation_type="TOTAL_ORDER")
            )
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema, registry=schema_registry()).validate(
                dict(relation, relation_type="ELAPSED")
            )


class TemporalMachineAlignmentTests(unittest.TestCase):
    def test_agenda_schema_accepts_a_derived_entry_with_exact_native_routing(self):
        agenda = rebuild_temporal_agenda([ARMED_ROOT])
        schema = load_schema("temporal-agenda-entry.schema.json")

        Draft202012Validator(schema, registry=schema_registry()).validate(agenda[0])
        self.assertEqual(agenda[0]["root_ref"], "world.thread:THREAD_market_siege")


class WorldThreadCatalogAlignmentTests(unittest.TestCase):
    def test_thread_schema_does_not_admit_catalog_generation_as_chronology_authority(self):
        schema = load_schema("world-thread-state.schema.json")
        serialized = json.dumps(schema)

        self.assertNotIn("catalog_generation", serialized)
        self.assertNotIn("chronology_frontier", serialized)


class Wp15TemporalProofTests(unittest.TestCase):
    def test_agenda_rebuild_is_deterministic_and_rejects_duplicate_native_occurrences(self):
        self.assertEqual(rebuild_temporal_agenda([ARMED_ROOT]), rebuild_temporal_agenda([ARMED_ROOT]))

        with self.assertRaisesRegex(TemporalContractError, "duplicate"):
            rebuild_temporal_agenda([ARMED_ROOT, dict(ARMED_ROOT)])


if __name__ == "__main__":
    unittest.main()
