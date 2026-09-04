import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from activity_primitive_contracts import load_activity_primitive_contracts  # noqa: E402

CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"

EXPECTED = {
    "op.select_targets", "op.roll", "op.resolve_check", "op.resolve_contest",
    "op.resolve_save", "op.resolve_attack", "op.apply_damage", "op.apply_healing",
    "op.set_temporary_hp", "op.consume_resource", "op.restore_resource",
    "op.move_entity", "op.teleport_entity", "op.transfer_asset",
    "op.transfer_currency", "op.create_entity", "op.retire_entity",
    "op.create_effect", "op.update_effect", "op.remove_effect",
    "op.transform_entity", "op.create_zone", "op.update_zone", "op.remove_zone",
    "op.for_each_target", "op.branch", "op.request_choice",
    "op.open_reaction_window", "op.emit_fact", "op.schedule_followup",
    "op.advance_local_time",
}

S6D07_ACTIVE = {
    "op.select_targets", "op.roll", "op.resolve_save",
    "op.resolve_attack", "op.apply_damage", "op.apply_healing",
    "op.consume_resource", "op.for_each_target",
    "op.resolve_check", "op.create_effect", "op.emit_fact",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contracts():
    return load_activity_primitive_contracts(ROOT)


class ActivityPrimitiveContractTests(unittest.TestCase):
    def test_registry_contract_equality_and_dormant_selection_boundary(self):
        core = load(CATALOG / "core-catalog.json")["registries"]
        rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
        self.assertEqual(set(core["activity_primitives"]), EXPECTED)
        self.assertEqual(EXPECTED, set(rows))
        for primitive_id, row in rows.items():
            if primitive_id in S6D07_ACTIVE:
                self.assertEqual(row["realization_state"], "COMPLETE")
                self.assertEqual(row["selection_state"], "ACTIVE_ADMITTED")
            else:
                self.assertEqual(row["realization_state"], "QUARANTINED")
                self.assertEqual(row["selection_state"], "DORMANT_NONSELECTABLE")

    def test_each_contract_is_closed_item_specific_and_has_execution_ownership(self):
        expected_keys = {
            "primitive_id", "family", "execution_kind", "realization_state",
            "selection_state", "activation_trigger", "arguments", "results", "reads",
            "rng", "prospective_outputs", "atomicity", "suspension", "failures",
            "bounds", "evidence",
        }
        argument_keys = {"value_kind", "cardinality", "required", "source"}
        for row in contracts()["contracts"]:
            if row["primitive_id"] in S6D07_ACTIVE:
                self.assertEqual(set(row), expected_keys | {"exact_seed_consumer_ids", "authority_denied"})
                self.assertTrue(row["exact_seed_consumer_ids"])
                self.assertTrue(row["authority_denied"])
            else:
                self.assertEqual(set(row), expected_keys)
            self.assertEqual(set(row["arguments"]), set(dict.fromkeys(row["arguments"])))
            self.assertEqual(set(row["results"]), set(dict.fromkeys(row["results"])))
            for spec in (*row["arguments"].values(), *row["results"].values()):
                self.assertLessEqual(argument_keys, set(spec))
                self.assertIn(spec["cardinality"], {"single", "many"})
            self.assertEqual(row["atomicity"]["owner"], "EXECUTION_SEGMENT")
            self.assertEqual(row["evidence"]["commit_disposition_owner"], "EXECUTION_SEGMENT")
            self.assertEqual(row["evidence"]["committed_fact_owner"], "MECHANICAL_EVENT")
            self.assertEqual(row["evidence"]["outcome_owner"], "RESOLUTION_RECEIPT")

    def test_no_generic_executable_or_mutation_language_is_admitted(self):
        forbidden_names = {"payload", "query", "script", "code", "path", "patch", "file", "network", "sql", "expression_language"}
        for row in contracts()["contracts"]:
            self.assertFalse(forbidden_names & set(row["arguments"]))
            self.assertFalse(forbidden_names & set(row["results"]))
            self.assertIn(row["execution_kind"], {"CALCULATION", "MUTATION", "COMPILER_FORM", "SUSPENSION", "FOLLOWUP", "TEMPORAL"})

    def test_rng_suspension_and_structural_bounds_are_not_implicit(self):
        rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
        self.assertEqual(rows["op.roll"]["rng"]["policy"], "ONE_FIXED_RESULT_PER_REQUEST_AND_GENERATION")
        for op_id, row in rows.items():
            if op_id != "op.roll":
                self.assertEqual(row["rng"]["policy"], "NONE")
        self.assertEqual(rows["op.request_choice"]["suspension"]["kind"], "CHOICE")
        self.assertEqual(rows["op.open_reaction_window"]["suspension"]["kind"], "REACTION")
        for op_id in ("op.for_each_target", "op.branch"):
            self.assertEqual(rows[op_id]["execution_kind"], "COMPILER_FORM")
            self.assertTrue(rows[op_id]["bounds"])

    def test_transition_event_and_failure_ids_are_registered(self):
        core = load(CATALOG / "core-catalog.json")["registries"]
        transitions = set(core["transition_kinds"])
        events = set(core["event_kinds"])
        failures = set(core["execution_failure_codes"])
        for row in contracts()["contracts"]:
            self.assertLessEqual(set(row["prospective_outputs"]["transition_kinds"]), transitions)
            self.assertLessEqual(set(row["prospective_outputs"]["event_kinds"]), events)
            self.assertLessEqual(set(row["failures"]), failures)

    def test_all_value_and_read_dependencies_route_to_closed_vocabularies(self):
        catalog = contracts()
        core = load(CATALOG / "core-catalog.json")["registries"]
        value_kinds = set(catalog["value_contracts"])
        read_contracts = catalog["read_contracts"]
        self.assertEqual(set(read_contracts["SELECTOR"]), set(core["rule_selectors"]))
        self.assertEqual(set(read_contracts["ACCESSOR"]), set(core["mechanical_accessors"]))
        for row in catalog["contracts"]:
            for spec in (*row["arguments"].values(), *row["results"].values()):
                self.assertIn(spec["value_kind"], value_kinds)
            for dependency in row["reads"]:
                if dependency["kind"] in {"SELECTOR", "ACCESSOR", "DOMAIN_OWNER", "INFRASTRUCTURE"}:
                    self.assertIn(dependency["id"], read_contracts[dependency["kind"]])

    def test_every_named_value_kind_has_a_concrete_validation_shape(self):
        value_contracts = contracts()["value_contracts"]
        shape_routes = {"schema_ref", "type", "enum", "one_of", "catalog_ref", "compiler_ref"}
        for value_kind, contract in value_contracts.items():
            self.assertEqual(contract["validation"], "EXACT_NAMED_CONTRACT")
            self.assertEqual(len(shape_routes & set(contract)), 1, value_kind)
            self.assertTrue(contract[shape_routes.intersection(contract).pop()])
            if "type" in contract:
                self.assertIn(contract["type"], {"boolean", "integer", "number", "string", "array", "object"})

    def test_compiler_rejects_unknown_missing_and_dormant_operations(self):
        catalog = contracts()
        with self.assertRaises(KeyError):
            compile_step({"op": "op.unknown", "args": {}}, catalog)
        with self.assertRaises(ValueError) as ctx:
            compile_step({"op": "op.restore_resource", "args": {}}, catalog, allow_dormant=True)
        self.assertEqual(str(ctx.exception), "primitive is quarantined")
        with self.assertRaises(ValueError) as ctx:
            compile_step({"op": "op.restore_resource", "args": {"owner_role": "actor", "resource_id": "x", "amount": 1, "payload": {}}}, catalog, allow_dormant=True)
        self.assertEqual(str(ctx.exception), "primitive is quarantined")
        with self.assertRaises(ValueError) as ctx:
            compile_step({"op": "op.apply_damage", "args": {"target_role": "target"}}, catalog)
        self.assertEqual(str(ctx.exception), "missing argument")

    def test_schema_root_and_activity_embedding_route_are_explicit(self):
        schema = load(SCHEMAS / "activity-primitive-contracts.schema.json")
        self.assertTrue(schema["$id"].endswith("/activity-primitive-contracts.schema.json"))
        activity = load(SCHEMAS / "activity-definition-data.schema.json")
        self.assertTrue(activity["$comment"].endswith("DEV/CATALOG/activity-primitive-contracts.json before admission"))

    def test_catalog_schema_and_exact_item_matrices_close_each_primitive_boundary(self):
        catalog = contracts()
        schema = load(SCHEMAS / "activity-primitive-contracts.schema.json")
        self.assertIn("primitive_validation_matrix", schema["required"])
        self.assertEqual(schema["properties"]["primitive_validation_matrix"]["additionalProperties"], {
            "$ref": "#/$defs/primitiveValidationMatrix"
        })

        matrices = catalog["primitive_validation_matrix"]
        rows = {row["primitive_id"]: row for row in catalog["contracts"]}
        self.assertEqual(set(matrices), set(rows))
        required = {
            "subject_policy", "storage_policy", "failure_policy",
            "validation_policy", "segment_semantics",
            "compiler_form_propagation", "activation_dependencies", "causal_recovery",
            "chronology_barrier",
        }
        for primitive_id, matrix in matrices.items():
            self.assertEqual(set(matrix), required)
            self.assertEqual(matrix["failure_policy"], "EXACT_CONTRACT_FAILURE_CODES")
            self.assertEqual(matrix["validation_policy"], "EXACT_CONTRACT_ARGUMENT_AND_RESULT_VALUE_CONTRACTS")
            self.assertIn(matrix["segment_semantics"], {
                "ONE_SEGMENT", "CHILD_STEPS_DEFINE_SEGMENTS", "SUSPENSION_STATE_ONLY",
                "PENDING_CHILD_IDENTITY_ATOMIC_WITH_TRIGGERING_COMMIT",
                "QUARANTINED_NO_EXECUTION",
            })
            dependencies = matrix["activation_dependencies"]
            self.assertIs(dependencies["requires_exact_seed_consumer"], True)
            self.assertEqual(
                len(dependencies["required_active_primitive_ids"]),
                len(set(dependencies["required_active_primitive_ids"])),
            )
            self.assertEqual(
                len(dependencies["required_active_value_kinds"]),
                len(set(dependencies["required_active_value_kinds"])),
            )

    def test_activation_dependency_traversal_is_closed_and_blocks_missing_dependency(self):
        catalog = contracts()
        rows = {row["primitive_id"]: row for row in catalog["contracts"]}
        matrices = catalog["primitive_validation_matrix"]

        def is_activatable(primitive_id, active_primitives, active_values, seed_consumers):
            if rows[primitive_id]["realization_state"] == "QUARANTINED":
                return False
            matrix = matrices[primitive_id]
            dependencies = matrix["activation_dependencies"]
            return (
                dependencies["requires_exact_seed_consumer"]
                and primitive_id in seed_consumers
                and set(dependencies["required_active_primitive_ids"]) <= active_primitives
                and set(dependencies["required_active_value_kinds"]) <= active_values
            )

        all_values = set(catalog["value_contracts"])
        for primitive_id, row in rows.items():
            dependencies = matrices[primitive_id]["activation_dependencies"]
            self.assertLessEqual(set(dependencies["required_active_primitive_ids"]), set(rows))
            self.assertLessEqual(set(dependencies["required_active_value_kinds"]), all_values)
            result = is_activatable(
                primitive_id,
                set(dependencies["required_active_primitive_ids"]),
                set(dependencies["required_active_value_kinds"]),
                {primitive_id},
            )
            self.assertIs(result, primitive_id in S6D07_ACTIVE)
            self.assertFalse(is_activatable(primitive_id, set(), set(), set()))

    def test_emit_fact_is_exact_action_surge_variant_without_generic_event_authority(self):
        row = {row["primitive_id"]: row for row in contracts()["contracts"]}["op.emit_fact"]
        matrix = contracts()["primitive_validation_matrix"]["op.emit_fact"]
        self.assertEqual(row["selection_state"], "ACTIVE_ADMITTED")
        self.assertEqual(row["realization_state"], "COMPLETE")
        self.assertEqual(row["exact_seed_consumer_ids"], ["activity.feature.action_surge"])
        self.assertEqual(row["arguments"]["fact_kind"]["value_kind"], "action_entitlement_fact_kind")
        self.assertEqual(row["prospective_outputs"]["event_kinds"], ["event.action_entitlement.granted"])
        self.assertEqual(matrix["subject_policy"], "BOUND_ACTOR_CURRENT_TURN_ONLY")
        self.assertEqual(matrix["storage_policy"], "TURN_ACTION_ECONOMY_PROCEDURE_STATE_ONLY")
        self.assertEqual(matrix["segment_semantics"], "ONE_SEGMENT")

    def test_followup_and_time_have_exact_causal_recovery_and_chronology_barriers(self):
        matrices = contracts()["primitive_validation_matrix"]
        schedule = matrices["op.schedule_followup"]
        self.assertEqual(schedule["subject_policy"], "ENCLOSING_OWNER_BOUND_SUBJECT_ONLY")
        self.assertEqual(schedule["storage_policy"], "PENDING_CHILD_INVOCATION_ONLY")
        self.assertEqual(schedule["causal_recovery"], {
            "causal_key": "TRIGGERING_SEGMENT_AND_TEMPORAL_BINDING",
            "recovery_owner": "PENDING_CHILD_INVOCATION",
            "retention": "UNTIL_SETTLED_OR_PROVEN_UNREACHABLE",
        })
        self.assertEqual(schedule["chronology_barrier"], "DUE_DISCOVERY_AFTER_TRIGGERING_SEGMENT_COMMIT")

        advance = matrices["op.advance_local_time"]
        self.assertEqual(advance["subject_policy"], "CHRONOLOGY_CONTEXT_BOUND_SUBJECT_ONLY")
        self.assertEqual(advance["storage_policy"], "CHRONOLOGY_OWNER_AND_COMMITTED_EVENT_ONLY")
        self.assertEqual(advance["causal_recovery"], {
            "causal_key": "CONTEXT_AND_SEGMENT_TIME_ADVANCEMENT",
            "recovery_owner": "CHRONOLOGY_OWNER",
            "retention": "COMMITTED_EVENT_AND_BOUNDARY_OCCURRENCES",
        })
        self.assertEqual(advance["chronology_barrier"], "COMMIT_TIME_BEFORE_DUE_CHILD_DISCOVERY_OR_PUBLICATION")

    def test_compiler_forms_propagate_only_closed_child_steps_and_enclosing_segment_semantics(self):
        matrices = contracts()["primitive_validation_matrix"]
        rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
        for primitive_id in ("op.for_each_target", "op.branch"):
            self.assertEqual(matrices[primitive_id]["compiler_form_propagation"], "CHILD_STEPS_ONLY_WITH_ENCLOSING_SEGMENT_INHERITANCE")
            self.assertEqual(matrices[primitive_id]["segment_semantics"], "CHILD_STEPS_DEFINE_SEGMENTS")
            self.assertEqual(rows[primitive_id]["atomicity"]["policy"], "CHILD_STEPS_DEFINE_SEGMENTS")


def compile_step(step, catalog, allow_dormant=False):
    rows = {row["primitive_id"]: row for row in catalog["contracts"]}
    row = rows[step["op"]]
    if row["realization_state"] != "COMPLETE":
        raise ValueError("primitive is quarantined")
    if row["selection_state"] != "ACTIVE_ADMITTED" and not allow_dormant:
        raise ValueError("primitive is nonselectable")
    supplied = step.get("args", {})
    if set(supplied) - set(row["arguments"]):
        raise ValueError("unknown argument")
    for name, spec in row["arguments"].items():
        if spec["required"] and name not in supplied:
            raise ValueError("missing argument")
    return {"primitive_id": row["primitive_id"], "result_names": sorted(row["results"])}


if __name__ == "__main__":
    unittest.main()
