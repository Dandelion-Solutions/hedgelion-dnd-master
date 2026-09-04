import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "DEV" / "TOOLS"))
from catalog_admission import load_catalog_admission_ledger  # noqa: E402

CATALOG = ROOT / "DEV" / "CATALOG"
SCHEMAS = ROOT / "DEV" / "SCHEMAS"

ACCESSORS = {
    "health.current", "health.temporary", "health.maximum", "health.bloodied",
    "life.state", "condition.present", "condition.value", "resource.capacity",
    "resource.available", "owner_effect.parameter",
}
FACTS = {"fiction.target_visible", "fiction.target_reachable"}
DERIVED = {
    "effect_availability", "effect_arbitration",
    "condition_aggregation", "condition_intrinsic",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def accessor_schema_ids(schema):
    return {
        schema["$defs"][branch["$ref"].split("/")[-1]]
        ["properties"]["accessor_id"]["const"]
        for branch in schema["oneOf"]
    }


def compile_accessor(surfaces, accessor_id, consumer_id, *, bound_view="view:1",
                     consumer_view="view:1", owner_effect=None,
                     requested_effect=None, declared_parameters=()):
    meta = surfaces["accessors"][accessor_id]
    if meta["disposition"] != "ACTIVE_ADMITTED":
        raise ValueError("dormant accessor")
    if consumer_id not in meta["permitted_consumer_ids"]:
        raise ValueError("unauthorized exact consumer")
    if bound_view != consumer_view:
        raise ValueError("state-view mismatch")
    if accessor_id == "owner_effect.parameter":
        if owner_effect != requested_effect:
            raise ValueError("cross-owner effect access")
        if "requested" not in declared_parameters:
            raise ValueError("undeclared owner parameter")
    return True


def compile_fact(surfaces, fact_id, consumer_id, supplied):
    try:
        meta = surfaces["context_facts"][fact_id]
    except KeyError as exc:
        raise ValueError("unknown fact") from exc
    if meta["disposition"] != "ACTIVE_ADMITTED":
        raise ValueError("dormant fact")
    if consumer_id not in meta["permitted_consumer_ids"]:
        raise ValueError("unauthorized exact consumer")
    if supplied is None:
        raise ValueError("typed missing input")
    return supplied


def graph_from_metadata(surfaces):
    graph = {}
    for section, kind in (("accessors", "accessor"), ("derived_nodes", "derived")):
        for item_id, meta in surfaces[section].items():
            graph[f"{kind}:{item_id}"] = list(meta["dependencies"])
    for selector_id in surfaces["selectors"]:
        graph.setdefault(f"selector:{selector_id}", [])
    return graph


def validate_bound_graph(surfaces, extra_edges, node_views=None, fact_inputs=None):
    graph = graph_from_metadata(surfaces)
    for node, deps in extra_edges.items():
        graph.setdefault(node, []).extend(deps)
    for deps in graph.values():
        for dep in deps:
            if dep not in graph:
                raise ValueError(f"unproven dependency: {dep}")
    for consumer, deps in graph.items():
        for producer in deps:
            kind, item_id = producer.split(":", 1)
            if kind == "accessor":
                allowed = surfaces["accessors"][item_id]["permitted_consumer_ids"]
                if consumer not in allowed:
                    raise ValueError("unauthorized inverse accessor edge")
            if kind == "derived":
                allowed = surfaces["derived_nodes"][item_id]["permitted_consumer_ids"]
                if consumer not in allowed:
                    raise ValueError("unauthorized inverse derived edge")
    views = node_views or {}
    for node, deps in graph.items():
        for dep in deps:
            if node in views and dep in views and views[node] != views[dep]:
                raise ValueError("committed/prospective view mismatch")
    facts = fact_inputs or {}
    memo, fact_visiting = {}, set()
    def reachable_facts(node):
        if node in memo:
            return memo[node]
        if node in fact_visiting:
            raise ValueError("dependency cycle")
        fact_visiting.add(node)
        result = set(facts.get(node, ()))
        for dep in graph[node]:
            result |= reachable_facts(dep)
        fact_visiting.remove(node)
        memo[node] = result
        return result
    for consumer in graph:
        kind, item_id = consumer.split(":", 1)
        if kind == "selector":
            allowed = set(surfaces["selectors"][item_id]["permitted_context_fact_ids"])
        elif kind == "derived":
            allowed = set(surfaces["derived_nodes"][item_id]["permitted_context_fact_ids"])
        else:
            continue
        reached = reachable_facts(consumer)
        if not reached <= allowed:
            raise ValueError("transitive forbidden fact")
        allowed_classes = set(
            surfaces["selectors"][item_id]["allowed_input_classes"]
            if kind == "selector"
            else surfaces["derived_nodes"][item_id]["allowed_input_classes"]
        )
        reached_classes = {
            surfaces["context_facts"][fact_id]["source_class"]
            for fact_id in reached
        }
        if not reached_classes <= allowed_classes:
            raise ValueError("transitive forbidden input class")
    visiting, done = set(), set()
    def visit(node):
        if node in visiting:
            raise ValueError("dependency cycle")
        if node in done:
            return
        visiting.add(node)
        for dep in graph[node]:
            visit(dep)
        visiting.remove(node)
        done.add(node)
    for node in graph:
        visit(node)
    return True


def test_s6d04_surface_schema_and_exact_census():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    Draft202012Validator(load(SCHEMAS / "mechanical-surfaces.schema.json")).validate(surfaces)
    assert set(surfaces["accessors"]) == ACCESSORS
    assert set(surfaces["context_facts"]) == FACTS
    assert set(surfaces["derived_nodes"]) == DERIVED
    assert accessor_schema_ids(load(SCHEMAS / "mechanical-accessor-ref.schema.json")) == ACCESSORS


def test_accessors_are_item_complete_and_ledger_disposition_matches():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    accessors = surfaces["accessors"]
    required = {
        "source_class", "value_type", "subject_kinds", "dependencies",
        "disposition", "input_class", "argument_kinds", "implicit_binding_kinds",
        "missing_policy", "permitted_consumer_kinds", "permitted_consumer_ids",
        "state_view_policy", "cache_policy",
    }
    for meta in accessors.values():
        assert required <= set(meta)
        assert meta["input_class"] == "ENGINE_STATE"
    assert sum(x["disposition"] == "ACTIVE_ADMITTED" for x in accessors.values()) == 9
    assert accessors["condition.value"]["disposition"] == "DORMANT_RESERVED"
    ledger = load_catalog_admission_ledger(ROOT)
    entries = {e["id"]: e for e in ledger["entries"]
               if e["registry_family"] == "mechanical_accessors"}
    assert entries["condition.value"]["admission_disposition"] == "DORMANT_NONSELECTABLE"
    assert all(entries[item]["realization_state"] == "COMPLETE"
               for item in ACCESSORS - {"condition.value"})


def test_types_missing_and_owner_binding_are_exact():
    accessors = load(CATALOG / "mechanical-surfaces.json")["accessors"]
    assert accessors["resource.capacity"]["value_type"] == "integer"
    assert accessors["resource.available"]["value_type"] == "integer"
    assert accessors["condition.present"]["missing_policy"] == "FALSE_WHEN_NO_EFFECTIVE_APPLICATION"
    assert accessors["condition.value"]["missing_policy"] == "ABSENT_WHEN_NO_EFFECTIVE_VALUE"
    assert accessors["owner_effect.parameter"]["implicit_binding_kinds"] == ["owner_effect_application"]


def test_exact_accessor_consumer_and_view_permission():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    assert compile_accessor(surfaces, "health.current", "accessor:health.bloodied")
    for consumer in ("selector:health.maximum", "derived:condition_aggregation"):
        try:
            compile_accessor(surfaces, "health.current", consumer)
            assert False, "unauthorized consumer accepted"
        except ValueError as exc:
            assert "consumer" in str(exc)
    try:
        compile_accessor(surfaces, "health.current", "accessor:health.bloodied",
                         consumer_view="prospective:1")
        assert False, "cross-view read accepted"
    except ValueError as exc:
        assert "view" in str(exc)


def test_dormant_ids_rejected_before_input_class_and_false_is_not_missing():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    try:
        compile_accessor(surfaces, "condition.value", "predicate:def:1")
        assert False, "dormant accessor accepted"
    except ValueError as exc:
        assert "dormant" in str(exc)
    for fact_id in FACTS:
        for supplied in (False, None):
            try:
                compile_fact(surfaces, fact_id, "activity:def:1", supplied)
                assert False, "dormant fact accepted"
            except ValueError as exc:
                assert "dormant" in str(exc)
    active = dict(surfaces)
    active["context_facts"] = dict(surfaces["context_facts"])
    meta = dict(active["context_facts"]["fiction.target_visible"])
    meta["disposition"] = "ACTIVE_ADMITTED"
    meta["permitted_consumer_ids"] = ["activity:def:1"]
    active["context_facts"]["fiction.target_visible"] = meta
    assert compile_fact(active, "fiction.target_visible", "activity:def:1", False) is False
    try:
        compile_fact(active, "fiction.target_visible", "activity:def:1", None)
        assert False, "missing coerced to false"
    except ValueError as exc:
        assert "missing" in str(exc)


def test_fact_identity_is_invocation_generation_not_universal_boundary():
    for fact in load(CATALOG / "mechanical-surfaces.json")["context_facts"].values():
        assert fact["occurrence_scope"] == "ACTIVITY_RESOLUTION_GENERATION"
        assert fact["binding_policy"] == "EXACT_COMPILED_CONSUMER_ROLES"
        assert fact["optional_boundary_context"] == "ONLY_WHEN_INVOCATION_ARISES_FROM_BOUNDARY"


def test_all_derived_nodes_engine_only_and_no_fact_laundering():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    for node in surfaces["derived_nodes"].values():
        assert node["allowed_input_classes"] == ["ENGINE_STATE"]
        assert node["permitted_context_fact_ids"] == []
    assert surfaces["consumer_permission_contract"]["policy"] == "EXACT_ID_AND_BINDING_REQUIRED"


def test_bound_graph_uses_actual_metadata_and_rejects_canonical_cycles():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    assert validate_bound_graph(surfaces, {})
    surfaces["accessors"]["health.bloodied"]["permitted_consumer_ids"] = ["predicate:effect-a"]
    surfaces["accessors"]["resource.available"]["permitted_consumer_ids"] = ["predicate:effect-b"]
    cases = [
        {
            "selector:health.maximum": ["predicate:effect-a"],
            "predicate:effect-a": ["accessor:health.bloodied"],
        },
        {
            "selector:resource.capacity": ["predicate:effect-b"],
            "predicate:effect-b": ["accessor:resource.available"],
        },
    ]
    for edges in cases:
        try:
            validate_bound_graph(surfaces, edges)
            assert False, "cycle accepted"
        except ValueError as exc:
            assert "cycle" in str(exc)


def test_bound_graph_rejects_cross_effect_resource_unproven_and_transitive_fact():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    surfaces["accessors"]["resource.available"]["permitted_consumer_ids"] = ["predicate:effect-b"]
    cross = {
        "selector:resource.capacity": ["predicate:effect-a"],
        "predicate:effect-a": ["predicate:effect-b"],
        "predicate:effect-b": ["accessor:resource.available"],
    }
    try:
        validate_bound_graph(surfaces, cross)
        assert False, "cross-effect/resource cycle accepted"
    except ValueError as exc:
        assert "cycle" in str(exc)
    try:
        validate_bound_graph(surfaces, {"predicate:def": ["accessor:not.registered"]})
        assert False, "incomplete closure accepted"
    except ValueError as exc:
        assert "unproven" in str(exc)
    edges = {"predicate:def": [], "selector:health.maximum": ["predicate:def"]}
    try:
        validate_bound_graph(
            surfaces, edges,
            fact_inputs={"predicate:def": {"fiction.target_visible"}},
        )
        assert False, "transitive forbidden fact accepted"
    except ValueError as exc:
        assert "forbidden fact" in str(exc)


def test_owner_effect_same_owner_only():
    surfaces = load(CATALOG / "mechanical-surfaces.json")
    meta = surfaces["accessors"]["owner_effect.parameter"]
    meta["permitted_consumer_ids"] = ["predicate:effect-a"]
    assert compile_accessor(
        surfaces, "owner_effect.parameter", "predicate:effect-a",
        owner_effect="effect:a", requested_effect="effect:a",
        declared_parameters={"requested"},
    )
    for requested, declared in (("effect:b", {"requested"}), ("effect:a", set())):
        try:
            compile_accessor(
                surfaces, "owner_effect.parameter", "predicate:effect-a",
                owner_effect="effect:a", requested_effect=requested,
                declared_parameters=declared,
            )
            assert False, "owner authority escape accepted"
        except ValueError:
            pass


def test_structural_schemas_do_not_claim_execution_authority():
    for name in ("mechanical-accessor-ref.schema.json", "mechanical-predicate.schema.json"):
        assert "Structural shape only" in load(SCHEMAS / name)["$comment"]

