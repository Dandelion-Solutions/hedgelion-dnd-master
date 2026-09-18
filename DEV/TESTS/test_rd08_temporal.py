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
    TemporalNativeEnumeration,
    TemporalRoute,
    derive_temporal_dependency_keys,
    derive_temporal_route_entry,
    enumerate_temporal_native_owners,
    evaluate_temporal_binding,
    materialize_due_occurrence,
    rebuild_temporal_agenda,
    rebuild_temporal_agenda_from_route,
    reconcile_temporal_route_membership,
    validate_temporal_route_completeness,
    validate_chronology_relation_evidence,
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

LIVE_SOURCE_KEY = ("campaign-frostfall", "scene-market", "epoch-1")


def _native_enumeration(*, scope: str, revision: str, source_key=None) -> TemporalNativeEnumeration:
    entry = derive_temporal_route_entry(
        ARMED_ROOT,
        campaign_id="campaign-frostfall",
        source_scope=scope,
        source_revision=revision,
        source_key=source_key,
    )
    return enumerate_temporal_native_owners(
        (entry,),
        campaign_id="campaign-frostfall",
        source_scope=scope,
        source_revision=revision,
        source_key=source_key,
    )


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
        non_temporal_terminal = dict(thread, status="resolved")
        del non_temporal_terminal["temporal"]
        Draft202012Validator(schema, registry=schema_registry()).validate(non_temporal_terminal)
        Draft202012Validator(schema, registry=schema_registry()).validate(
            dict(non_temporal_terminal, status="active")
        )


class TemporalBindingAgendaTests(unittest.TestCase):
    def test_all_authoritative_binding_variants_validate_before_evaluation(self):
        metric_binding = {
            "basis_id": "temporal.metric_deadline",
            "context_id": "scene:market",
            "anchor_value": 12,
            "deadline_value": 11,
            "unit_id": "unit.day",
        }
        procedure_binding = {
            "basis_id": "temporal.procedure_boundary",
            "boundary_id": "boundary:turn-start",
            "procedure_id": "procedure:market-fight",
            "anchor_id": "event:market-warning",
            "subject_id": "actor:guard",
            "offset": 1,
        }
        semantic_binding = {
            "basis_id": "temporal.semantic_boundary",
            "boundary_id": "boundary:market-fall",
            "anchor_id": "event:market-warning",
            "subject_id": "actor:guard",
            "scope_id": "scene:market",
        }
        bindings = (
            (metric_binding, {"provider_id": "scene:market", "position": {"kind": "EXACT", "value": 12}}),
            (procedure_binding, {}),
            (semantic_binding, {}),
        )
        validator = Draft202012Validator(load_schema("temporal-binding.schema.json"), registry=schema_registry())
        for binding, evidence in bindings:
            validator.validate(binding)
            evaluate_temporal_binding(binding, evidence)

        malformed = (
            dict(procedure_binding, subject_id=3),
            dict(procedure_binding, offset=0),
            dict(semantic_binding, scope_id=3),
        )
        for binding in malformed:
            with self.assertRaises(ValidationError):
                validator.validate(binding)
            with self.assertRaises(TemporalContractError):
                evaluate_temporal_binding(binding, {})

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

    def test_route_completeness_rejects_native_owner_omissions_and_extras(self):
        entry = derive_temporal_route_entry(
            ARMED_ROOT,
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
        )
        route = TemporalRoute(
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
            entries=(entry,),
        )

        native_enumeration = _native_enumeration(scope="CAMPAIGN", revision="0" * 40)
        validate_temporal_route_completeness(route, native_enumeration)
        with self.assertRaisesRegex(TemporalContractError, "incomplete|omission|native owner"):
            validate_temporal_route_completeness(
                route,
                enumerate_temporal_native_owners(
                    (),
                    campaign_id="campaign-frostfall",
                    source_scope="CAMPAIGN",
                    source_revision="0" * 40,
                ),
            )
        with self.assertRaisesRegex(TemporalContractError, "extra|native owner"):
            validate_temporal_route_completeness(
                route,
                enumerate_temporal_native_owners(
                    (
                        native_enumeration.entries[0],
                        derive_temporal_route_entry(
                            dict(ARMED_ROOT, root_ref="world.thread:THREAD_other"),
                            campaign_id="campaign-frostfall",
                            source_scope="CAMPAIGN",
                            source_revision="0" * 40,
                        ),
                    ),
                    campaign_id="campaign-frostfall",
                    source_scope="CAMPAIGN",
                    source_revision="0" * 40,
                ),
            )

    def test_native_enumeration_is_not_caller_constructible_evidence(self):
        native_enumeration = _native_enumeration(scope="CAMPAIGN", revision="0" * 40)
        route = TemporalRoute(
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
            entries=native_enumeration.entries,
        )

        forged = TemporalNativeEnumeration(
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
            entries=native_enumeration.entries,
        )
        with self.assertRaisesRegex(TemporalContractError, "producer-issued"):
            validate_temporal_route_completeness(route, forged)

    def test_native_enumeration_rejects_caller_native_mappings(self):
        with self.assertRaisesRegex(TemporalContractError, "typed.*entries"):
            enumerate_temporal_native_owners(
                (ARMED_ROOT,),
                campaign_id="campaign-frostfall",
                source_scope="CAMPAIGN",
                source_revision="0" * 40,
            )

    def test_route_completeness_rejects_cross_campaign_owner_set(self):
        entry = derive_temporal_route_entry(
            ARMED_ROOT,
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
        )
        with self.assertRaisesRegex(TemporalContractError, "campaign"):
            TemporalRoute(
                campaign_id="campaign-other",
                source_scope="CAMPAIGN",
                source_revision="0" * 40,
                entries=(entry,),
            )


class TemporalExecutionRecoveryTests(unittest.TestCase):
    def test_interrupted_temporal_recovery_retries_both_directions_from_native_enumeration(self):
        campaign_revision = "0" * 40
        live_revision = "1" * 40
        recovered_campaign_revision = "2" * 40
        campaign_route = TemporalRoute(
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision=campaign_revision,
            entries=(
                derive_temporal_route_entry(
                    ARMED_ROOT,
                    campaign_id="campaign-frostfall",
                    source_scope="CAMPAIGN",
                    source_revision=campaign_revision,
                ),
            ),
        )
        campaign_enumeration = _native_enumeration(
            scope="CAMPAIGN", revision=campaign_revision
        )
        live_route = reconcile_temporal_route_membership(
            campaign_route,
            expected_source_scope="CAMPAIGN",
            expected_source_revision=campaign_revision,
            target_source_scope="LIVE",
            target_source_revision=live_revision,
            target_source_key=LIVE_SOURCE_KEY,
            native_enumeration=campaign_enumeration,
        )
        live_enumeration = _native_enumeration(
            scope="LIVE", revision=live_revision, source_key=LIVE_SOURCE_KEY
        )
        live_retry = reconcile_temporal_route_membership(
            live_route,
            expected_source_scope="LIVE",
            expected_source_revision=live_revision,
            expected_source_key=LIVE_SOURCE_KEY,
            target_source_scope="LIVE",
            target_source_revision=live_revision,
            target_source_key=LIVE_SOURCE_KEY,
            native_enumeration=live_enumeration,
        )
        campaign_return = reconcile_temporal_route_membership(
            live_route,
            expected_source_scope="LIVE",
            expected_source_revision=live_revision,
            expected_source_key=LIVE_SOURCE_KEY,
            target_source_scope="CAMPAIGN",
            target_source_revision=recovered_campaign_revision,
            native_enumeration=live_enumeration,
        )
        recovered_enumeration = _native_enumeration(
            scope="CAMPAIGN", revision=recovered_campaign_revision
        )
        campaign_retry = reconcile_temporal_route_membership(
            campaign_return,
            expected_source_scope="CAMPAIGN",
            expected_source_revision=recovered_campaign_revision,
            target_source_scope="CAMPAIGN",
            target_source_revision=recovered_campaign_revision,
            native_enumeration=recovered_enumeration,
        )

        self.assertEqual(live_retry, live_route)
        self.assertEqual(campaign_retry, campaign_return)
        self.assertEqual(
            rebuild_temporal_agenda_from_route(campaign_retry),
            rebuild_temporal_agenda_from_route(campaign_route),
        )

    def test_temporal_route_completeness_rejects_caller_root_reference_lists(self):
        entry = derive_temporal_route_entry(
            ARMED_ROOT,
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
        )
        route = TemporalRoute(
            campaign_id="campaign-frostfall",
            source_scope="CAMPAIGN",
            source_revision="0" * 40,
            entries=(entry,),
        )

        with self.assertRaises(TemporalContractError):
            validate_temporal_route_completeness(
                route, ("world.thread:THREAD_market_siege",)  # type: ignore[arg-type]
            )


class ChronologyBridgeTests(unittest.TestCase):
    def test_bounded_coordinate_accepts_an_ordered_signed_range(self):
        relation = {
            "relation_type": "SAME_COORDINATE",
            "first_anchor_id": "event:market-warning",
            "second_anchor_id": "event:market-fall",
            "provider_scope_id": "scene:market",
            "context_id": "chronology:market",
            "coordinate": {"kind": "BOUNDED", "lower": -8, "upper": 3, "unit_id": "unit.day"},
        }

        schema = load_schema("chronology-relation-evidence.schema.json")
        Draft202012Validator(schema, registry=schema_registry()).validate(relation)

        self.assertEqual(validate_chronology_relation_evidence(relation), relation)

    def test_chronology_relation_schema_encodes_each_typed_relation_shape(self):
        schema = load_schema("chronology-relation-evidence.schema.json")
        validator = Draft202012Validator(schema, registry=schema_registry())
        relations = (
            {
                "relation_type": "CAUSES",
                "cause_anchor_id": "event:market-warning",
                "effect_anchor_id": "event:market-fall",
                "scope_id": "scene:market",
            },
            {
                "relation_type": "PRECEDES",
                "predecessor_anchor_id": "event:market-warning",
                "successor_anchor_id": "event:market-fall",
                "order_domain_id": "order-domain:market",
                "scope_id": "scene:market",
            },
            {
                "relation_type": "SAME_COORDINATE",
                "first_anchor_id": "event:market-warning",
                "second_anchor_id": "event:market-fall",
                "provider_scope_id": "scene:market",
                "context_id": "chronology:market",
                "coordinate": {"kind": "EXACT", "value": 15, "unit_id": "unit.day"},
            },
            {
                "relation_type": "ELAPSED",
                "start_anchor_id": "event:market-warning",
                "end_anchor_id": "event:market-fall",
                "provider_scope_id": "scene:market",
                "context_id": "chronology:market",
                "elapsed": {"lower": 2, "upper": 4, "unit_id": "unit.day"},
            },
        )
        for relation in relations:
            validator.validate(relation)
            self.assertEqual(validate_chronology_relation_evidence(relation), relation)

        with self.assertRaises(ValidationError):
            validator.validate(dict(relations[1], relation_type="TOTAL_ORDER"))
        with self.assertRaises(ValidationError):
            validator.validate(dict(relations[1], order_domain_id=None))
        with self.assertRaises(ValidationError):
            validator.validate(dict(relations[0], order_domain_id="order-domain:market"))
        for relation in (relations[2], relations[3]):
            missing_context = dict(relation)
            del missing_context["context_id"]
            with self.assertRaises(ValidationError):
                validator.validate(missing_context)

        bounded_coordinate = dict(
            relations[2],
            coordinate={"kind": "BOUNDED", "lower": 8, "upper": 3, "unit_id": "unit.day"},
        )
        invalid_elapsed = dict(
            relations[3],
            elapsed={"lower": 4, "upper": 2, "unit_id": "unit.day"},
        )
        for relation in (bounded_coordinate, invalid_elapsed):
            with self.assertRaisesRegex(TemporalContractError, "lower"):
                validate_chronology_relation_evidence(relation)


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
