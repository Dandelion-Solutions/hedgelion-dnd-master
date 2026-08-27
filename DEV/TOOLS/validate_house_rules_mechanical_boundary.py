"""Fail-closed S6D-10 House-Rules/mechanics integration proof."""
import hashlib, json, re, sys
from pathlib import Path

POLICY_BASIS_REF=re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$")
MACHINE_ID=re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
TOP_KEYS={"schema_version","identity_bound_package_capabilities_path","identity_bound_package_candidate","route_profiles","active_adjudicated_consumers","current_supported_policy_realizations","conformance_only_policy_realizations"}
COMMON={"edge_key","input_kind","consumer_id","input_id","value_type","source_class","policy_basis_mode"}
PARAM_KEYS=COMMON|{"cardinality","required","minimum","maximum"}
FACT_KEYS=COMMON|{"disposition"}
POLICY_FAILURES={"failure.adjudication_input_missing","failure.adjudication_input_unauthorized","failure.adjudication_input_invalid","failure.adjudication_context_stale","failure.policy_conflict","failure.policy_realization_gap"}

def load(root,relative): return json.loads((root/relative).read_text(encoding="utf-8"))
def fingerprint(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def validate_policy_basis_resolution(ref,evidence):
    """Validate output of the existing campaign publication/history resolver."""
    if not POLICY_BASIS_REF.fullmatch(ref): raise ValueError("invalid exact policy basis ref")
    policy_id,revision=ref.rsplit("@",1)
    keys={"policy_id","campaign_revision","sidecar_source_path","sidecar_policy_ids","resolved_normative_anchors","authority_validated","applicable"}
    if set(evidence)!=keys: raise ValueError("invalid policy resolver evidence shape")
    if evidence["policy_id"]!=policy_id or evidence["campaign_revision"]!=revision: raise ValueError("policy resolver evidence identity mismatch")
    if policy_id not in evidence["sidecar_policy_ids"]: raise ValueError("policy id absent at exact campaign revision")
    if not evidence["sidecar_source_path"] or not evidence["resolved_normative_anchors"].get(policy_id): raise ValueError("paired normative policy source unresolved")
    if evidence["authority_validated"] is not True or evidence["applicable"] is not True: raise ValueError("policy revision is not accepted and applicable")
    return True

def validate_policy_basis_refs(refs):
    if not isinstance(refs,list) or len(refs)!=len(set(refs)) or refs!=sorted(refs): raise ValueError("policy_basis_refs must be unique lexicographically sorted refs")
    for ref in refs:
        if not POLICY_BASIS_REF.fullmatch(ref): raise ValueError("invalid exact policy basis ref")
    return True

def validate_accepted_policy_basis_collections(parameter_bindings,invocation_facts):
    """Required pre-Resolution gate for every enriched accepted input."""
    for value in parameter_bindings.values():
        if isinstance(value,dict) and value.get("source_class")=="INVOCATION_ADJUDICATED": validate_policy_basis_refs(value.get("policy_basis_refs"))
    for fact in invocation_facts: validate_policy_basis_refs(fact.get("policy_basis_refs"))
    return True

def validate_shape(c):
    if set(c)!=TOP_KEYS: raise ValueError(f"unknown contract members or missing required members: {sorted(set(c)^TOP_KEYS)}")
    if c["schema_version"]!=1: raise ValueError("unsupported contract schema_version")
    if c["identity_bound_package_capabilities_path"]!="GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/character-capabilities.json": raise ValueError("invalid identity-bound package capabilities path")
    identity=c["identity_bound_package_candidate"]; ik={"package_id","package_version","catalog_generation","content_set_sha256","runtime_selection_state"}
    if not isinstance(identity,dict) or set(identity)!=ik or not all(isinstance(identity[k],str) and identity[k] for k in ik) or not re.fullmatch(r"[a-f0-9]{64}",identity["content_set_sha256"]) or identity["runtime_selection_state"]!="BLOCKED_UNTIL_S6D_11": raise ValueError("invalid identity-bound package candidate")
    if (identity["package_id"],identity["package_version"],identity["catalog_generation"]) != ("hdm.rules.dnd2024-srd52-core","0.1.0-mvp","2.0.0"): raise ValueError("unexpected identity-bound package candidate")
    route_keys={"policy_revision_and_lifecycle","authority_and_eligibility","consumer_and_value_contract","provenance_and_freeze","catalog_and_native_validation","rng_and_mutation","execution_and_failure","retry_recovery_and_publication","proof_ids","revisit_trigger"}
    profiles=c["route_profiles"]
    if not isinstance(profiles,dict) or set(profiles)!={"route.adjudicated_parameter_to_mechanics","route.invocation_fact_to_mechanics","route.policy_realization_link_conformance"} or any(set(v)!=route_keys for v in profiles.values()): raise ValueError("invalid route profile matrix")
    rows=c["active_adjudicated_consumers"]
    if not isinstance(rows,list) or not rows: raise ValueError("active adjudicated consumer rows required")
    for row in rows:
        expected=PARAM_KEYS if row.get("input_kind")=="ACTIVITY_PARAMETER" else FACT_KEYS if row.get("input_kind")=="INVOCATION_FACT" else set()
        if not expected or set(row)!=expected: raise ValueError("invalid consumer row shape")
        if row["source_class"]!="INVOCATION_ADJUDICATED" or row["policy_basis_mode"]!="REQUIRED_ARRAY_MAY_BE_EMPTY": raise ValueError("invalid consumer row policy/source contract")
        if not MACHINE_ID.fullmatch(row["consumer_id"]) or not MACHINE_ID.fullmatch(row["input_id"]): raise ValueError("invalid consumer row machine identity")
        prefix="parameter" if row["input_kind"]=="ACTIVITY_PARAMETER" else "fact"
        if row["edge_key"]!=f"{prefix}:{row['consumer_id']}:{row['input_id']}": raise ValueError("consumer edge key disagrees with row semantics")
        if row["input_kind"]=="ACTIVITY_PARAMETER" and (row["value_type"],row["cardinality"],row["required"],row["minimum"],row["maximum"]) != ("integer","single",True,1,30): raise ValueError("invalid consumer row parameter contract")
        if row["input_kind"]=="INVOCATION_FACT" and (row["value_type"]!="boolean" or row["disposition"]!="ACTIVE_ADMITTED"): raise ValueError("invalid consumer row fact contract")
    if not isinstance(c["current_supported_policy_realizations"],list): raise ValueError("invalid current realization collection")
    fixtures=c["conformance_only_policy_realizations"]
    if not isinstance(fixtures,list) or not fixtures: raise ValueError("conformance fixtures required")
    for f in fixtures:
        keys={"fixture_id","policy_basis_ref","target_class","realization_refs","expected"}
        if not isinstance(f,dict) or set(f)!=keys or not MACHINE_ID.fullmatch(f.get("fixture_id","")) or not all(MACHINE_ID.fullmatch(x) for x in f.get("realization_refs",[])): raise ValueError("invalid conformance fixture shape")
        if f["target_class"] not in {"PACKAGE_DEFINITION","PRIMITIVE"} or f["expected"] not in {"CONFORMANCE_VALID_LINK_ONLY","failure.policy_realization_gap"}: raise ValueError("invalid conformance fixture enum")
        if not POLICY_BASIS_REF.fullmatch(f["policy_basis_ref"]): raise ValueError(f"invalid exact policy basis ref: {f['fixture_id']}")
        if not f["realization_refs"] or len(set(f["realization_refs"]))!=len(f["realization_refs"]): raise ValueError("invalid realization reference collection")
    parameter_edges={r["edge_key"] for r in rows if r["input_kind"]=="ACTIVITY_PARAMETER"}; fact_edges={r["edge_key"] for r in rows if r["input_kind"]=="INVOCATION_FACT"}
    if set(profiles["route.adjudicated_parameter_to_mechanics"]["proof_ids"])!=parameter_edges or set(profiles["route.invocation_fact_to_mechanics"]["proof_ids"])!=fact_edges or set(profiles["route.policy_realization_link_conformance"]["proof_ids"])!={f["fixture_id"] for f in fixtures}: raise ValueError("route profile proof coverage mismatch")

def parse_empty_template(root):
    lines=[x for x in (root/"GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml").read_text(encoding="utf-8").splitlines() if x.strip().startswith("policies:")]
    if len(lines)!=1 or not re.fullmatch(r"\s*policies:\s*\[\s*\]\s*",lines[0]): raise ValueError("engine campaign template must contain exactly one empty policies collection")

def package_rows(root,c):
    cap_path=c["identity_bound_package_capabilities_path"]
    cap=load(root,cap_path); package_dir=(root/cap_path).parent
    for k,v in c["identity_bound_package_candidate"].items():
        if k=="runtime_selection_state": continue
        if cap.get(k)!=v: raise ValueError(f"selected package identity mismatch: {k}")
    definitions={}; rows=[]; paths=set()
    for member in cap["content_files"]:
        p=member["path"]
        if p in paths or Path(p).is_absolute() or ".." in Path(p).parts: raise ValueError("invalid package content member path")
        paths.add(p); raw=(package_dir/p).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=member["sha256"]: raise ValueError(f"package content identity mismatch: {p}")
        payload=json.loads(raw)
        for collection in payload.values():
            if not isinstance(collection,list): continue
            for rec in collection:
                if not isinstance(rec,dict) or "id" not in rec or "kind" not in rec: continue
                if rec["id"] in definitions: raise ValueError(f"duplicate package definition: {rec['id']}")
                definitions[rec["id"]]=rec["kind"]
                if rec["kind"]!="definition.activity": continue
                for pid,d in rec.get("data",{}).get("parameters",{}).items():
                    if d.get("source_class")=="INVOCATION_ADJUDICATED": rows.append({"edge_key":f"parameter:{rec['id']}:{pid}","input_kind":"ACTIVITY_PARAMETER","consumer_id":rec["id"],"input_id":pid,"value_type":d.get("value_type"),"source_class":d.get("source_class"),"cardinality":d.get("cardinality"),"required":d.get("required"),"minimum":d.get("minimum"),"maximum":d.get("maximum"),"policy_basis_mode":"REQUIRED_ARRAY_MAY_BE_EMPTY"})
    return definitions,rows

def fact_rows(root):
    result=[]
    for fid,m in load(root,"DEV/CATALOG/mechanical-surfaces.json")["context_facts"].items():
        if m.get("disposition")!="ACTIVE_ADMITTED": continue
        for cid in m.get("permitted_consumer_ids",[]): result.append({"edge_key":f"fact:{cid}:{fid}","input_kind":"INVOCATION_FACT","consumer_id":cid,"input_id":fid,"value_type":m.get("value_type"),"source_class":m.get("source_class"),"disposition":m.get("disposition"),"policy_basis_mode":"REQUIRED_ARRAY_MAY_BE_EMPTY"})
    return result

def validate_failures(root):
    registered=set(load(root,"DEV/CATALOG/core-catalog.json")["registries"]["execution_failure_codes"])
    if not POLICY_FAILURES<=registered: raise ValueError(f"unregistered policy failure codes: {sorted(POLICY_FAILURES-registered)}")
    admitted={r["id"] for r in load(root,"DEV/CATALOG/catalog-admission-ledger.json")["entries"] if r.get("registry_family")=="execution_failure_codes" and r.get("admission_disposition")=="ACTIVE_ADMITTED"}
    if not POLICY_FAILURES<=admitted: raise ValueError(f"unadmitted policy failure codes: {sorted(POLICY_FAILURES-admitted)}")

def validate(root):
    c=load(root,"DEV/CATALOG/house-rules-mechanical-boundary.json"); validate_shape(c)
    definitions,params=package_rows(root,c); derived=params+fact_rows(root); declared=c["active_adjudicated_consumers"]
    dw={fingerprint(x):x for x in declared}; rw={fingerprint(x):x for x in derived}
    if len(dw)!=len(declared) or len(rw)!=len(derived): raise ValueError("duplicate active adjudicated consumer row")
    if set(dw)!=set(rw): raise ValueError("active adjudicated consumer mismatch: complete normalized rows differ")
    parse_empty_template(root)
    if c["current_supported_policy_realizations"]: raise ValueError("empty engine campaign template requires an empty current realization set")
    primitives={r["primitive_id"]:r for r in load(root,"DEV/CATALOG/activity-primitive-contracts.json")["contracts"]}
    for f in c["conformance_only_policy_realizations"]:
        valid=all(definitions.get(x)=="definition.activity" for x in f["realization_refs"]) if f["target_class"]=="PACKAGE_DEFINITION" else all(x in primitives and primitives[x].get("selection_state")=="ACTIVE_ADMITTED" and primitives[x].get("realization_state")=="COMPLETE" for x in f["realization_refs"])
        actual="CONFORMANCE_VALID_LINK_ONLY" if valid else "failure.policy_realization_gap"
        if actual!=f["expected"]: raise ValueError(f"wrong conformance expectation: {f['fixture_id']}")
    validate_failures(root)
    return {"active_adjudicated_consumer_edges":len(declared),"conformance_only_policy_realizations":len(c["conformance_only_policy_realizations"]),"current_supported_policy_realizations":0,"status":"PASS"}

def main(argv):
    if len(argv)!=2: raise SystemExit("usage: validate_house_rules_mechanical_boundary.py REPOSITORY_ROOT")
    try: result=validate(Path(argv[1]).resolve())
    except (KeyError,OSError,TypeError,ValueError,json.JSONDecodeError) as exc: print(str(exc),file=sys.stderr); return 1
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main(sys.argv))

