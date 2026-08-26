import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
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


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contracts():
    return load(CATALOG / "activity-primitive-contracts.json")


def test_registry_contract_equality_and_dormant_selection_boundary():
    core = load(CATALOG / "core-catalog.json")["registries"]
    rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
    assert set(core["activity_primitives"]) == EXPECTED == set(rows)
    for primitive_id, row in rows.items():
        assert row["realization_state"] == "QUARANTINED"
        if primitive_id == "op.emit_fact":
            assert row["selection_state"] == "QUARANTINED_NO_EXACT_CLOSED_VARIANT"
        else:
            assert row["selection_state"] == "DORMANT_NONSELECTABLE"


def test_each_contract_is_closed_item_specific_and_has_execution_ownership():
    expected_keys = {
        "primitive_id", "family", "execution_kind", "realization_state",
        "selection_state", "activation_trigger", "arguments", "results", "reads",
        "rng", "prospective_outputs", "atomicity", "suspension", "failures",
        "bounds", "evidence",
    }
    argument_keys = {"value_kind", "cardinality", "required", "source"}
    for row in contracts()["contracts"]:
        assert set(row) == expected_keys
        assert set(row["arguments"]) == set(dict.fromkeys(row["arguments"]))
        assert set(row["results"]) == set(dict.fromkeys(row["results"]))
        for spec in (*row["arguments"].values(), *row["results"].values()):
            assert argument_keys <= set(spec)
            assert spec["cardinality"] in {"single", "many"}
        assert row["atomicity"]["owner"] == "EXECUTION_SEGMENT"
        assert row["evidence"]["commit_disposition_owner"] == "EXECUTION_SEGMENT"
        assert row["evidence"]["committed_fact_owner"] == "MECHANICAL_EVENT"
        assert row["evidence"]["outcome_owner"] == "RESOLUTION_RECEIPT"


def test_no_generic_executable_or_mutation_language_is_admitted():
    forbidden_names = {"payload", "query", "script", "code", "path", "patch", "file", "network", "sql", "expression_language"}
    for row in contracts()["contracts"]:
        assert not (forbidden_names & set(row["arguments"]))
        assert not (forbidden_names & set(row["results"]))
        assert row["execution_kind"] in {"CALCULATION", "MUTATION", "COMPILER_FORM", "SUSPENSION", "FOLLOWUP", "TEMPORAL"}


def test_rng_suspension_and_structural_bounds_are_not_implicit():
    rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
    assert rows["op.roll"]["rng"]["policy"] == "ONE_FIXED_RESULT_PER_REQUEST_AND_GENERATION"
    for op_id, row in rows.items():
        if op_id != "op.roll":
            assert row["rng"]["policy"] == "NONE"
    assert rows["op.request_choice"]["suspension"]["kind"] == "CHOICE"
    assert rows["op.open_reaction_window"]["suspension"]["kind"] == "REACTION"
    for op_id in ("op.for_each_target", "op.branch"):
        assert rows[op_id]["execution_kind"] == "COMPILER_FORM"
        assert rows[op_id]["bounds"]


def test_transition_event_and_failure_ids_are_registered():
    core = load(CATALOG / "core-catalog.json")["registries"]
    transitions = set(core["transition_kinds"])
    events = set(core["event_kinds"])
    failures = set(core["execution_failure_codes"])
    for row in contracts()["contracts"]:
        assert set(row["prospective_outputs"]["transition_kinds"]) <= transitions
        assert set(row["prospective_outputs"]["event_kinds"]) <= events
        assert set(row["failures"]) <= failures


def test_all_value_and_read_dependencies_route_to_closed_vocabularies():
    catalog = contracts()
    core = load(CATALOG / "core-catalog.json")["registries"]
    value_kinds = set(catalog["value_contracts"])
    read_contracts = catalog["read_contracts"]
    assert set(read_contracts["SELECTOR"]) == set(core["rule_selectors"])
    assert set(read_contracts["ACCESSOR"]) == set(core["mechanical_accessors"])
    for row in catalog["contracts"]:
        for spec in (*row["arguments"].values(), *row["results"].values()):
            assert spec["value_kind"] in value_kinds
        for dependency in row["reads"]:
            if dependency["kind"] in {"SELECTOR", "ACCESSOR", "DOMAIN_OWNER", "INFRASTRUCTURE"}:
                assert dependency["id"] in read_contracts[dependency["kind"]]


def test_every_named_value_kind_has_a_concrete_validation_shape():
    value_contracts = contracts()["value_contracts"]
    shape_routes = {"schema_ref", "type", "enum", "one_of", "catalog_ref", "compiler_ref"}
    for value_kind, contract in value_contracts.items():
        assert contract["validation"] == "EXACT_NAMED_CONTRACT"
        assert len(shape_routes & set(contract)) == 1, value_kind
        assert contract[shape_routes.intersection(contract).pop()]
        if "type" in contract:
            assert contract["type"] in {"boolean", "integer", "number", "string", "array", "object"}


def compile_step(step, catalog, allow_dormant=False):
    rows = {row["primitive_id"]: row for row in catalog["contracts"]}
    row = rows[step["op"]]
    if row["realization_state"] == "QUARANTINED":
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


def test_compiler_rejects_unknown_missing_and_dormant_operations():
    catalog = contracts()
    try:
        compile_step({"op": "op.unknown", "args": {}}, catalog)
        assert False
    except KeyError:
        pass
    try:
        compile_step({"op": "op.apply_damage", "args": {}}, catalog, allow_dormant=True)
        assert False
    except ValueError as exc:
        assert str(exc) == "primitive is quarantined"
    try:
        compile_step({"op": "op.apply_damage", "args": {"target_role": "target", "components": [], "payload": {}}}, catalog, allow_dormant=True)
        assert False
    except ValueError as exc:
        assert str(exc) == "primitive is quarantined"
    try:
        compile_step({"op": "op.apply_damage", "args": {"target_role": "target", "components": []}}, catalog)
        assert False
    except ValueError as exc:
        assert str(exc) == "primitive is quarantined"


def test_schema_root_and_activity_embedding_route_are_explicit():
    schema = load(SCHEMAS / "activity-primitive-contracts.schema.json")
    assert schema["$id"].endswith("/activity-primitive-contracts.schema.json")
    activity = load(SCHEMAS / "activity-definition-data.schema.json")
    assert activity["$comment"].endswith("DEV/CATALOG/activity-primitive-contracts.json before admission")


def test_catalog_schema_and_exact_item_matrices_close_each_primitive_boundary():
    catalog = contracts()
    schema = load(SCHEMAS / "activity-primitive-contracts.schema.json")
    assert "primitive_validation_matrix" in schema["required"]
    assert schema["properties"]["primitive_validation_matrix"]["additionalProperties"] == {
        "$ref": "#/$defs/primitiveValidationMatrix"
    }

    matrices = catalog["primitive_validation_matrix"]
    rows = {row["primitive_id"]: row for row in catalog["contracts"]}
    assert set(matrices) == set(rows)
    required = {
        "subject_policy", "storage_policy", "failure_policy",
        "validation_policy", "segment_semantics",
        "compiler_form_propagation", "activation_dependencies", "causal_recovery",
        "chronology_barrier",
    }
    for primitive_id, matrix in matrices.items():
        assert set(matrix) == required
        assert matrix["failure_policy"] == "EXACT_CONTRACT_FAILURE_CODES"
        assert matrix["validation_policy"] == "EXACT_CONTRACT_ARGUMENT_AND_RESULT_VALUE_CONTRACTS"
        assert matrix["segment_semantics"] in {
            "ONE_SEGMENT", "CHILD_STEPS_DEFINE_SEGMENTS", "SUSPENSION_STATE_ONLY",
            "PENDING_CHILD_IDENTITY_ATOMIC_WITH_TRIGGERING_COMMIT",
            "QUARANTINED_NO_EXECUTION",
        }
        dependencies = matrix["activation_dependencies"]
        assert dependencies["requires_exact_seed_consumer"] is True
        assert len(dependencies["required_active_primitive_ids"]) == len(
            set(dependencies["required_active_primitive_ids"])
        )
        assert len(dependencies["required_active_value_kinds"]) == len(
            set(dependencies["required_active_value_kinds"])
        )


def test_activation_dependency_traversal_is_closed_and_blocks_missing_dependency():
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
        assert set(dependencies["required_active_primitive_ids"]) <= set(rows)
        assert set(dependencies["required_active_value_kinds"]) <= all_values
        assert not is_activatable(
            primitive_id,
            set(dependencies["required_active_primitive_ids"]),
            set(dependencies["required_active_value_kinds"]),
            {primitive_id},
        )
        assert not is_activatable(primitive_id, set(), set(), set())


def test_emit_fact_is_quarantined_without_generic_event_authority():
    row = {row["primitive_id"]: row for row in contracts()["contracts"]}["op.emit_fact"]
    matrix = contracts()["primitive_validation_matrix"]["op.emit_fact"]
    assert row["selection_state"] == "QUARANTINED_NO_EXACT_CLOSED_VARIANT"
    assert row["realization_state"] == "QUARANTINED"
    assert "event_kind" not in row["arguments"]
    assert not row["results"]
    assert not row["prospective_outputs"]["event_kinds"]
    assert matrix["segment_semantics"] == "QUARANTINED_NO_EXECUTION"


def test_followup_and_time_have_exact_causal_recovery_and_chronology_barriers():
    matrices = contracts()["primitive_validation_matrix"]
    schedule = matrices["op.schedule_followup"]
    assert schedule["subject_policy"] == "ENCLOSING_OWNER_BOUND_SUBJECT_ONLY"
    assert schedule["storage_policy"] == "PENDING_CHILD_INVOCATION_ONLY"
    assert schedule["causal_recovery"] == {
        "causal_key": "TRIGGERING_SEGMENT_AND_TEMPORAL_BINDING",
        "recovery_owner": "PENDING_CHILD_INVOCATION",
        "retention": "UNTIL_SETTLED_OR_PROVEN_UNREACHABLE",
    }
    assert schedule["chronology_barrier"] == "DUE_DISCOVERY_AFTER_TRIGGERING_SEGMENT_COMMIT"

    advance = matrices["op.advance_local_time"]
    assert advance["subject_policy"] == "CHRONOLOGY_CONTEXT_BOUND_SUBJECT_ONLY"
    assert advance["storage_policy"] == "CHRONOLOGY_OWNER_AND_COMMITTED_EVENT_ONLY"
    assert advance["causal_recovery"] == {
        "causal_key": "CONTEXT_AND_SEGMENT_TIME_ADVANCEMENT",
        "recovery_owner": "CHRONOLOGY_OWNER",
        "retention": "COMMITTED_EVENT_AND_BOUNDARY_OCCURRENCES",
    }
    assert advance["chronology_barrier"] == "COMMIT_TIME_BEFORE_DUE_CHILD_DISCOVERY_OR_PUBLICATION"


def test_compiler_forms_propagate_only_closed_child_steps_and_enclosing_segment_semantics():
    matrices = contracts()["primitive_validation_matrix"]
    rows = {row["primitive_id"]: row for row in contracts()["contracts"]}
    for primitive_id in ("op.for_each_target", "op.branch"):
        assert matrices[primitive_id]["compiler_form_propagation"] == "CHILD_STEPS_ONLY_WITH_ENCLOSING_SEGMENT_INHERITANCE"
        assert matrices[primitive_id]["segment_semantics"] == "CHILD_STEPS_DEFINE_SEGMENTS"
        assert rows[primitive_id]["atomicity"]["policy"] == "CHILD_STEPS_DEFINE_SEGMENTS"

