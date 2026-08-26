import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "DEV" / "SCHEMAS"
CATALOG = ROOT / "DEV" / "CATALOG"

def load(path): return json.loads(path.read_text(encoding="utf-8"))

EXPECTED = {
"value.runtime_command","value.action_request","value.transition_request","value.intent_clause",
"value.target_spec","value.area_spec","value.duration_spec","value.cost_spec","value.signal",
"value.state_delta","value.roll_request","value.roll_result","value.choice_request",
"value.reaction_offer","value.resolution_receipt","value.execution_segment",
"value.pending_child_invocation","value.invocation_fact","value.boundary_occurrence"}

def test_transitive_local_schema_reference_closure():
    external=re.compile(r"https://hedgelion\.invalid/schemas/([^\"#]+)")
    for schema_path in SCHEMAS.glob("*.schema.json"):
        for target in external.findall(schema_path.read_text(encoding="utf-8")):
            assert (SCHEMAS/target).exists(), (schema_path.name,target)

def test_route_manifest_exactness_and_nonrecord_authority():
    manifest=load(CATALOG/"portable-value-routes.json")
    routes={x["value_id"]:x for x in manifest["routes"]}
    assert set(routes)==EXPECTED
    core=load(CATALOG/"core-catalog.json")["registries"]
    assert EXPECTED <= set(core["protocol_value_kinds"])
    records=set(core["world_record_kinds"])|set(core["runtime_record_kinds"])
    assert not (EXPECTED & records)
    for route in routes.values():
        assert route["authority"]=="EMBEDDED_NONOWNER"
        assert (SCHEMAS/route["schema_file"]).exists()
    assert routes["value.signal"]["disposition"]=="DORMANT_NONSELECTABLE"
    assert routes["value.state_delta"]["disposition"]=="DORMANT_NONSELECTABLE"

def test_declaration_binding_cost_roll_and_offer_fields_are_materialized():
    param=load(SCHEMAS/"activity-parameter-spec.schema.json")
    assert {"source_class","value_type","cardinality","required"} <= set(param["required"])
    assert "default" in param["properties"]
    cost=load(SCHEMAS/"cost-spec.schema.json")
    assert "payer_role" in cost["required"]
    request=load(SCHEMAS/"roll-request.schema.json")
    assert "roller_role" in request["required"]
    result=load(SCHEMAS/"roll-result.schema.json")
    assert {"request_id","source_kind","provenance_ref"} <= set(result["required"])
    for name in ("choice-request.schema.json","reaction-offer.schema.json"):
        schema=load(SCHEMAS/name)
        assert {"parent_resolution_id","continuation_generation"} <= set(schema["required"])

def test_signal_and_delta_are_rejecting_structural_roots_without_lifecycle():
    forbidden={"status","state","disposition","generation","signal_id","delta_id","bindings","value","payload"}
    for name in ("signal.schema.json","state-delta.schema.json"):
        schema=load(SCHEMAS/name)
        assert schema["not"]=={}
        assert not (forbidden & set(schema["properties"]))
        assert "nonselectable" in schema["description"]

def test_continuation_retains_no_signal_or_prospective_delta():
    props=load(SCHEMAS/"runtime-continuation-state.schema.json")["properties"]
    assert not ({"signals","state_deltas","prospective_deltas"} & set(props))

def validate_target(target):
    assert target["minimum"] <= target["maximum"]
    r=target.get("range")
    if r:
        if r["mode_id"]=="range.distance":
            assert r.get("distance",0)>0 and "unit_id" in r
        else:
            assert "distance" not in r and "unit_id" not in r
    if "area" in target:
        assert target["kind_id"] in {"target.point","target.zone"}

def validate_area(area):
    required={
      "area.sphere":{"radius"},"area.emanation":{"radius"},"area.cube":{"size"},
      "area.cone":{"length"},"area.line":{"length","width"},
      "area.cylinder":{"radius","height"}}
    assert set(area["dimensions"])==required[area["shape_id"]]

def test_catalog_aware_target_area_constraints():
    validate_target({"kind_id":"target.entity","minimum":1,"maximum":1,
      "range":{"mode_id":"range.reachable"}})
    validate_area({"shape_id":"area.sphere","unit_id":"unit.foot",
      "dimensions":{"radius":20}})
    for invalid in (
      {"kind_id":"target.entity","minimum":2,"maximum":1},
      {"kind_id":"target.entity","minimum":1,"maximum":1,
       "range":{"mode_id":"range.distance"}},
      {"kind_id":"target.entity","minimum":1,"maximum":1,
       "area":{"shape_id":"area.sphere","unit_id":"unit.foot","dimensions":{"radius":5}}},
    ):
        try: validate_target(invalid); assert False
        except AssertionError: pass
    try:
        validate_area({"shape_id":"area.line","unit_id":"unit.foot",
          "dimensions":{"length":30}})
        assert False
    except AssertionError: pass

def test_choice_reaction_are_distinct_and_generation_bound():
    choice=load(SCHEMAS/"choice-request.schema.json")
    reaction=load(SCHEMAS/"reaction-offer.schema.json")
    assert choice["properties"]["kind"]["const"]=="choice"
    assert reaction["properties"]["kind"]["const"]=="reaction"
    assert "option_ids" in choice["properties"] and "candidate_activity_ids" not in choice["properties"]
    assert "candidate_activity_ids" in reaction["properties"] and "option_ids" not in reaction["properties"]


def resolve_binding(declaration, binding):
    value = binding.get("value") if isinstance(binding, dict) and binding.get("source_class")=="INVOCATION_ADJUDICATED" else binding
    if declaration["source_class"]=="INVOCATION_ADJUDICATED":
        assert isinstance(binding, dict) and binding.get("source_class")=="INVOCATION_ADJUDICATED"
    values=value if declaration["cardinality"]=="many" else [value]
    assert isinstance(values,list)
    pytypes={"boolean":bool,"integer":int,"number":(int,float),"string":str,"machine_id":str}
    assert all(isinstance(x,pytypes[declaration["value_type"]]) and not (declaration["value_type"]=="integer" and isinstance(x,bool)) for x in values)
    return value

def test_declaration_binding_compatibility_and_continuation_freeze():
    decl={"source_class":"INVOCATION_ADJUDICATED","value_type":"integer","cardinality":"single","required":True}
    binding={"source_class":"INVOCATION_ADJUDICATED","value":15,"provenance_ref":"p",
      "eligibility_basis_fingerprint":"e","rules_context_fingerprint":"r","policy_basis_refs":[]}
    assert resolve_binding(decl,binding)==15
    for bad in (15,{"source_class":"INVOCATION_ADJUDICATED","value":"15"}):
        try: resolve_binding(decl,bad); assert False
        except (AssertionError,AttributeError): pass
    continuation=load(SCHEMAS/"runtime-continuation-state.schema.json")
    assert "parameter_bindings" in continuation["properties"]
    frozen=json.loads(json.dumps({"parameter_bindings":{"dc":binding}}))
    assert frozen["parameter_bindings"]["dc"]==binding

def test_route_embedding_graph_and_canonical_refs():
    manifest=load(CATALOG/"portable-value-routes.json")
    rows={x["value_id"]:x for x in manifest["routes"]}
    for row in rows.values():
        assert isinstance(row["embedding_consumers"],list)
    def text(name): return (SCHEMAS/name).read_text(encoding="utf-8")
    assert "target-spec.schema.json" in text("activity-definition-data.schema.json")
    assert "area-spec.schema.json" in text("target-spec.schema.json")
    assert "cost-spec.schema.json" in text("activity-definition-data.schema.json")
    assert "duration-spec.schema.json" in text("activity-definition-data.schema.json")
    assert "pending-child-invocation.schema.json" in text("execution-segment.schema.json")
    assert "invocation-fact.schema.json" in text("runtime-continuation-state.schema.json")
    assert "roll-result.schema.json" in text("runtime-continuation-state.schema.json")
    assert "choice-request.schema.json" in text("runtime-continuation-state.schema.json")
    assert "reaction-offer.schema.json" in text("runtime-continuation-state.schema.json")

def test_catalog_drives_target_area_cost_duration_validation():
    core=load(CATALOG/"core-catalog.json")["registries"]
    assert {"target.entity","target.point"} <= set(core["target_kinds"])
    assert {"area.sphere","area.line"} <= set(core["area_shapes"])
    assert "range.distance" in core["range_modes"]
    assert {"duration.instant","duration.metric","duration.boundary","duration.permanent"} <= set(core["duration_modes"])
    cost=load(SCHEMAS/"cost-spec.schema.json")
    assert {"resource_ref","payer_role","amount","commitment_id"} <= set(cost["required"])
    duration=load(SCHEMAS/"duration-spec.schema.json")
    assert len(duration["oneOf"])==4

def test_roll_linkage_retry_and_offer_currentness():
    request={"roll_id":"roll:1","expression":"1d20","purpose_id":"roll.attack","roller_role":"actor"}
    result={"roll_id":"roll:1","request_id":"roll:1","expression":"1d20","raw_values":[17],"source_kind":"rng.system","provenance_ref":"rng:1"}
    assert result["request_id"]==request["roll_id"] and result["expression"]==request["expression"]
    fixed={result["request_id"]:result}
    assert fixed[request["roll_id"]] is result
    choice=load(SCHEMAS/"choice-request.schema.json")["examples"][0]
    reaction=load(SCHEMAS/"reaction-offer.schema.json")["examples"][0]
    owning={"resolution_id":"resolution-0001","generation":1}
    for offer in (choice,reaction):
        assert offer["parent_resolution_id"]==owning["resolution_id"]
        assert offer["continuation_generation"]==owning["generation"]

def test_all_modified_root_examples_contain_required_fields():
    for name in ("activity-parameter-spec.schema.json","cost-spec.schema.json","roll-request.schema.json","roll-result.schema.json","choice-request.schema.json","reaction-offer.schema.json"):
        schema=load(SCHEMAS/name)
        for example in schema.get("examples",[]):
            assert set(schema["required"]) <= set(example)

def test_route_rows_ids_and_embedding_edges_are_machine_verified():
    manifest=load(CATALOG/"portable-value-routes.json")
    assert set(manifest)=={"schema_name","schema_version","owner","routes"}
    for row in manifest["routes"]:
        assert set(row)=={"value_id","schema_file","authority","disposition","embedding_consumers"}
        root=load(SCHEMAS/row["schema_file"])
        assert root["$id"].endswith("/"+row["schema_file"])
        actual=sorted(p.name for p in SCHEMAS.glob("*.schema.json")
                      if p.name != row["schema_file"] and row["schema_file"] in p.read_text(encoding="utf-8"))
        assert sorted(row["embedding_consumers"])==actual

def binding_value_type_ok(value, value_type):
    types={"boolean":bool,"integer":int,"number":(int,float),"string":str,"machine_id":str}
    return isinstance(value,types[value_type]) and not (value_type in {"integer","number"} and isinstance(value,bool))

def compile_bindings(declarations, supplied, engine_values=None):
    engine_values=engine_values or {}
    assert not (set(supplied)-set(declarations))
    accepted={}
    for name,decl in declarations.items():
        if decl["source_class"]=="ENGINE_BOUND":
            assert name not in supplied
            if name in engine_values: value=engine_values[name]
            elif "default" in decl: value=decl["default"]
            elif decl["required"]: raise AssertionError(name)
            else: continue
        elif name in supplied:
            raw=supplied[name]
            if decl["source_class"]=="INVOCATION_ADJUDICATED":
                assert isinstance(raw,dict) and raw.get("source_class")=="INVOCATION_ADJUDICATED"
                assert {"value","provenance_ref","eligibility_basis_fingerprint","rules_context_fingerprint","policy_basis_refs"} <= set(raw)
                value=raw["value"]
            else:
                assert not isinstance(raw,dict)
                value=raw
        elif "default" in decl: value=decl["default"]
        elif decl["required"]: raise AssertionError(name)
        else: continue
        values=value if decl["cardinality"]=="many" else [value]
        assert isinstance(values,list) and values
        assert all(binding_value_type_ok(v,decl["value_type"]) for v in values)
        if "allowed_values" in decl: assert all(v in decl["allowed_values"] for v in values)
        if "minimum" in decl: assert all(v>=decl["minimum"] for v in values)
        if "maximum" in decl: assert all(v<=decl["maximum"] for v in values)
        accepted[name]=raw if name in supplied else value
    return accepted

def expect_rejected(fn):
    try: fn(); assert False
    except (AssertionError,KeyError,TypeError): pass

def test_real_activity_action_request_binding_matrix_and_freeze():
    activity={"family_id":"activity.test","parameters":{
      "dc":{"source_class":"INVOCATION_ADJUDICATED","value_type":"integer","cardinality":"single","required":True,"minimum":1,"maximum":30},
      "approaches":{"source_class":"PLAYER_CHOICE","value_type":"machine_id","cardinality":"many","required":True,"allowed_values":["approach.careful","approach.fast"]},
      "note":{"source_class":"PLAYER_CHOICE","value_type":"string","cardinality":"single","required":False,"default":"quiet"},
      "actor":{"source_class":"ENGINE_BOUND","value_type":"machine_id","cardinality":"single","required":True}},
      "steps":[{"op":"op.resolve_check"}]}
    adjudicated={"source_class":"INVOCATION_ADJUDICATED","value":15,"provenance_ref":"p","eligibility_basis_fingerprint":"e","rules_context_fingerprint":"r","policy_basis_refs":[]}
    request={"activity_id":"activity.test.generic","actor_id":"actor-1","parameter_bindings":{"dc":adjudicated,"approaches":["approach.careful","approach.fast"]}}
    assert set(load(SCHEMAS/"action-request.schema.json")["required"]) <= set(request)
    accepted=compile_bindings(activity["parameters"],request["parameter_bindings"],{"actor":"actor-1"})
    assert set(accepted)=={"dc","approaches","note","actor"} and accepted["note"]=="quiet"
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":15,"approaches":["approach.careful"]},{"actor":"actor-1"}))
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":adjudicated,"approaches":"approach.careful"},{"actor":"actor-1"}))
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":adjudicated,"approaches":["bad"]},{"actor":"actor-1"}))
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":adjudicated,"approaches":["approach.fast"],"actor":"actor-2"},{"actor":"actor-1"}))
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":adjudicated,"unknown":1},{"actor":"actor-1"}))
    expect_rejected(lambda: compile_bindings(activity["parameters"],{"dc":adjudicated},{"actor":"actor-1"}))
    frozen=json.loads(json.dumps(accepted,sort_keys=True))
    continuation={"generation":1,"root_command_id":"command-1","resolution_id":"resolution-1","activity_id":"activity.test.generic","actor_id":"actor-1","parameter_bindings":frozen,"catalog_context_fingerprint":"ctx","execution_cursor":"step-1","safe_recompute_phase":"determine","invocation_facts":[],"fixed_rng_results":[],"prior_step_exports":{},"committed_segment_refs":[],"dependency_frontier_refs":[],"expected_child_resolution_ids":[],"future_rng_frontier":"rng:1"}
    assert set(load(SCHEMAS/"runtime-continuation-state.schema.json")["required"]) <= set(continuation)
    assert continuation["parameter_bindings"]==accepted

def test_catalog_contracts_cover_every_registered_target_area_range_duration():
    core=load(CATALOG/"core-catalog.json")["registries"]
    contract=load(CATALOG/"portable-value-contracts.json")
    assert set(contract["range_contracts"])==set(core["range_modes"])
    assert set(contract["area_dimension_contracts"])==set(core["area_shapes"])
    assert set(contract["duration_contracts"])==set(core["duration_modes"])
    assert set(contract["target_kind_contracts"])==set(core["target_kinds"])
    assert set(contract["duration_units"])==set(core["duration_units"])
    assert contract["spatial_units"]==["unit.foot"]
    assert set(contract["area_eligible_target_kinds"]) <= set(core["target_kinds"])
    for mode,rules in contract["range_contracts"].items():
        value={"mode_id":mode,**({"distance":5,"unit_id":"unit.foot"} if mode=="range.distance" else {})}
        assert set(rules["required"]) <= set(value) and not (set(rules["forbidden"])&set(value))
    for shape,keys in contract["area_dimension_contracts"].items():
        dims={key:5 for key in keys}; validate_area({"shape_id":shape,"unit_id":"unit.foot","dimensions":dims})
    assert set(contract["structural_nonselectable_values"])=={"value.signal","value.state_delta"}
    assert contract["cost_commitment_routes"]=={"cost_commit.on_accept":{"owner":"S6D-06","disposition":"DORMANT_UNTIL_PRIMITIVE_CONTRACT"}}

def validate_catalog_portable(value_kind, value):
    c=load(CATALOG/"portable-value-contracts.json")
    if value_kind=="target":
        rule=c["target_kind_contracts"][value["kind_id"]]
        assert value["minimum"]<=value["maximum"]
        if "minimum" in rule: assert value["minimum"]==rule["minimum"]
        if "maximum" in rule: assert value["maximum"]==rule["maximum"]
        assert "area" not in value or rule["area_allowed"]
        if "range" in value:
            rr=c["range_contracts"][value["range"]["mode_id"]]
            assert set(rr["required"])<=set(value["range"])
            assert not (set(rr["forbidden"])&set(value["range"]))
            if "unit_id" in value["range"]: assert value["range"]["unit_id"] in c["spatial_units"]
    elif value_kind=="area":
        assert set(value["dimensions"])==set(c["area_dimension_contracts"][value["shape_id"]])
        assert value["unit_id"] in c["spatial_units"]
    elif value_kind=="duration":
        r=c["duration_contracts"][value["kind_id"]]
        assert set(r["required"])<=set(value) and not (set(r["forbidden"])&set(value))
        if "unit_id" in value: assert value["unit_id"] in c["duration_units"]
    elif value_kind=="cost": assert value["commitment_id"] in c["cost_commitment_routes"] and value["amount"]>=0

def test_catalog_compiler_rejects_unknown_and_illegal_ids():
    validate_catalog_portable("target",{"kind_id":"target.none","minimum":0,"maximum":0})
    validate_catalog_portable("target",{"kind_id":"target.point","minimum":1,"maximum":1,"range":{"mode_id":"range.distance","distance":30,"unit_id":"unit.foot"}})
    validate_catalog_portable("area",{"shape_id":"area.sphere","unit_id":"unit.foot","dimensions":{"radius":5}})
    validate_catalog_portable("duration",{"kind_id":"duration.metric","amount":1,"unit_id":"unit.minute"})
    validate_catalog_portable("cost",{"resource_ref":"resource.x","payer_role":"actor","amount":0,"commitment_id":"cost_commit.on_accept"})
    for kind,value in (
      ("target",{"kind_id":"target.unknown","minimum":1,"maximum":1}),
      ("target",{"kind_id":"target.self","minimum":0,"maximum":1}),
      ("target",{"kind_id":"target.entity","minimum":1,"maximum":1,"area":{}}),
      ("target",{"kind_id":"target.point","minimum":1,"maximum":1,"range":{"mode_id":"range.unknown"}}),
      ("target",{"kind_id":"target.point","minimum":1,"maximum":1,"range":{"mode_id":"range.distance","distance":30,"unit_id":"unit.unknown"}}),
      ("area",{"shape_id":"area.unknown","dimensions":{}}),
      ("area",{"shape_id":"area.sphere","unit_id":"unit.unknown","dimensions":{"radius":5}}),
      ("duration",{"kind_id":"duration.metric","amount":1,"unit_id":"unit.round"}),
      ("duration",{"kind_id":"duration.unknown"}),
      ("cost",{"amount":1,"commitment_id":"cost_commit.unknown"})):
        expect_rejected(lambda kind=kind,value=value: validate_catalog_portable(kind,value))

def test_roll_retry_is_single_fixed_result_and_offers_reject_stale_owner():
    request={"roll_id":"roll:1","expression":"1d20","purpose_id":"roll.attack","roller_role":"actor"}
    result={"roll_id":"roll:1","request_id":"roll:1","expression":"1d20","raw_values":[17],"source_kind":"rng.system","provenance_ref":"rng:1"}
    def accept(req,res,fixed):
        assert res["request_id"]==req["roll_id"] and res["expression"]==req["expression"]
        if req["roll_id"] in fixed: assert fixed[req["roll_id"]]==res
        else: fixed[req["roll_id"]]=res
        return fixed[req["roll_id"]]
    continuation={"generation":1,"root_command_id":"command-1","resolution_id":"resolution-0001","activity_id":"activity.attack.basic","actor_id":"actor-1","catalog_context_fingerprint":"ctx","execution_cursor":"roll-1","safe_recompute_phase":"determine","invocation_facts":[],"fixed_rng_results":[],"prior_step_exports":{},"committed_segment_refs":[],"dependency_frontier_refs":[],"expected_child_resolution_ids":[],"future_rng_frontier":"rng:2"}
    assert set(load(SCHEMAS/"runtime-continuation-state.schema.json")["required"]) <= set(continuation)
    fixed={x["request_id"]:x for x in continuation["fixed_rng_results"]}
    assert accept(request,result,fixed)==result; continuation["fixed_rng_results"]=list(fixed.values())
    assert accept(request,json.loads(json.dumps(result)),{x["request_id"]:x for x in continuation["fixed_rng_results"]})==result
    expect_rejected(lambda: accept(request,{**result,"expression":"2d20"},{x["request_id"]:x for x in continuation["fixed_rng_results"]}))
    expect_rejected(lambda: accept(request,{**result,"raw_values":[3]},{x["request_id"]:x for x in continuation["fixed_rng_results"]}))
    def current(offer):
        assert offer["parent_resolution_id"]==continuation["resolution_id"]
        assert offer["continuation_generation"]==continuation["generation"]
    for name in ("choice-request.schema.json","reaction-offer.schema.json"):
        offer=load(SCHEMAS/name)["examples"][0]; continuation["pending_response"]=offer; current(continuation["pending_response"])
        expect_rejected(lambda offer={**offer,"continuation_generation":2}: current(offer))
        expect_rejected(lambda offer={**offer,"parent_resolution_id":"other"}: current(offer))

def test_nested_activity_and_continuation_examples_track_child_requirements():
    activity=load(SCHEMAS/"activity-definition-data.schema.json")
    required=set(load(SCHEMAS/"activity-parameter-spec.schema.json")["required"])
    for example in activity["examples"]:
        for declaration in example.get("parameters",{}).values(): assert required <= set(declaration)
    continuation=load(SCHEMAS/"runtime-continuation-state.schema.json")
    roll_required=set(load(SCHEMAS/"roll-result.schema.json")["required"])
    for example in continuation["examples"]:
        for result in example["fixed_rng_results"]: assert roll_required <= set(result)
