"""Fail-closed S6D-09 coverage and reference-transition conformance."""
from copy import deepcopy
import hashlib, json, re
from pathlib import Path
from DEV.TOOLS.validate_character_mvp_seed import CanonicalSchemaValidator
from DEV.TOOLS.validate_ruleset_package_closure import build_resolved_lock
from DEV.TOOLS.activity_primitive_contracts import load_activity_primitive_contracts

MACHINE_ID=re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+$")
TOP={"schema_name","schema_version","profile_id","source_manifest","source_sets","required_coverage_keys","coverage_ledger","atomic_routes","scope_exclusions","completeness_proof"}
BINDING={"profile_id","package_id","package_revision","compatibility_family","compatibility_generation","catalog_generation","gameplay_spine_member","package_content_sha256","ruleset_set_digest_generation","ruleset_set_sha256"}
LEDGER={"source_key","source_memberships","coverage_id","package_presence","product_scope","realization","disposition","route_id","source_citations","negative_space"}
ROUTE={"route_id","family","scenario","applicability","consumer_ids","definition_ids","input_provenance","missing_input_behavior","binding_identity","frozen_inputs","currentness","selector_operation_resolver","dependencies","execution_route","rng_retry","authoritative_mutation","mutation_rationale","execution_segment","event_route","receipt_route","failures","idempotency_conflict","multiplayer_currentness","suspension_chronology_recovery","classification","positive_evidence","negative_space","downstream_gap"}

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def exact(value, keys, label):
 if not isinstance(value,dict) or set(value)!=keys: raise ValueError(f"{label} members are not exact")
def strings(value):
 if isinstance(value,dict):
  for x in value.values(): yield from strings(x)
 elif isinstance(value,list):
  for x in value: yield from strings(x)
 elif isinstance(value,str): yield value

def product_rows(root):
 root=Path(root);value=load(root/"DEV/CATALOG/product-promise-evidence.json")
 CanonicalSchemaValidator(root/"DEV/SCHEMAS").validate(value,load(root/"DEV/SCHEMAS/product-promise-evidence.schema.json"));rows=value["rows"]
 if len({r["key"] for r in rows})!=len(rows):raise ValueError("duplicate product evidence key")
 expected={"key","owner_path","evidence_pattern","qualifier","product_scope","route_id"}
 for row in rows:
  exact(row,expected,row.get("key","product evidence"));owner=root/row["owner_path"]
  if not owner.is_file() or row["evidence_pattern"].casefold() not in owner.read_text(encoding="utf-8").casefold():raise ValueError(f"product evidence missing: {row['key']}")
 return rows

def build_expected_source_sets(root):
 root=Path(root); pkg=root/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"
 package=set()
 for name in ("character-mvp-seed.json","health-effects-recovery-seed.json","gameplay-spine-seed.json"):
  package.update(x for x in strings(load(pkg/name)) if MACHINE_ID.fullmatch(x))
 mech=load(root/"DEV/CATALOG/mechanical-surfaces.json"); portable=load(root/"DEV/CATALOG/portable-value-routes.json"); prim=load_activity_primitive_contracts(root)
 machine=[]
 machine += [f"accessor:{k}" for k,v in mech["accessors"].items() if v["disposition"]=="ACTIVE_ADMITTED"]
 machine += [f"selector:{k}" for k in mech["selectors"]]
 machine += [f"derived:{k}" for k,v in mech["derived_nodes"].items() if v["disposition"].startswith("ACTIVE_")]
 for fact_id,metadata in mech["context_facts"].items():
  if metadata["disposition"]=="ACTIVE_ADMITTED":
   machine.append(f"fact:{fact_id}")
   machine += [f"edge:{fact_id}->{c}" for c in metadata["permitted_consumer_ids"]]
 machine += [f"value:{v['value_id']}" for v in portable["routes"] if v["disposition"]=="ACTIVE_STRUCTURAL"]
 for row in prim["contracts"]:
  if row["selection_state"]=="ACTIVE_ADMITTED":
   machine.append(f"primitive:{row['primitive_id']}")
   machine += [f"edge:{row['primitive_id']}->{c}" for c in row["exact_seed_consumer_ids"]]
 return {"PACKAGE_CLOSURE_KEYS":sorted(f"PACKAGE:{x}" for x in package),"ACTIVE_MACHINE_CONSUMER_KEYS":sorted(f"MACHINE:{x}" for x in machine),"PRODUCT_PROMISE_KEYS":sorted(f"PRODUCT:{row['key']}" for row in product_rows(root))}

def route_for(key):
 v=key.split(":",1)[1]
 if key.startswith("PRODUCT:"): raise ValueError("product route requires evidence row")
 if any(x in v for x in ("activity.check.generic","selector:check.roll","op.resolve_check")):return "route.generic_check"
 if any(x in v for x in ("activity.save.generic","selector:save.roll","op.resolve_save")):return "route.generic_save"
 if "fiction.target_reachable" in v:return "route.spatial_target_applicability"
 if "procedure." in v or any(x in v for x in ("procedure.combat_minimal","resource.action_budget","resource.movement_budget","transition.location_change")):return "route.procedure_movement"
 if any(x in v for x in ("asset.transfer","transition.asset_transfer","event.asset.transferred")):return "route.asset_transfer"
 if any(x in v for x in ("asset.equip","transition.asset_status","event.asset.status_changed")):return "route.asset_equip"
 if "asset.use" in v:return "route.asset_use"
 if any(x in v for x in ("life.","life_policy.","health.","effect.","condition.","duration.","recovery","rest.")):return "route.inherited_s6d08"
 return "route.inherited_s6d07"

def route(rid,family,scenario,consumers,definitions,provenance,mutation,event,classification,positive,negative):
 null=mutation=="NO_AUTHORITATIVE_WORLD_MUTATION"
 return {"route_id":rid,"family":family,"scenario":scenario,"applicability":"hdm.rules.dnd2024-srd52-core/package-revision-1/compatibility-generation-1/catalog-generation-2/gameplay_spine.mvp.v1","consumer_ids":consumers,"definition_ids":definitions,"input_provenance":provenance,"missing_input_behavior":"TYPED_FAILURE_NO_MUTATION_NO_EVENT","binding_identity":"REQUEST_ACTIVITY_ACCEPTED_PARAMETER_FINGERPRINT","frozen_inputs":"ACCEPTED_BINDINGS_AND_FIXED_RNG_REUSED","currentness":"CATALOG_GENERATION_PLUS_PINNED_REVISIONS_OR_NA","selector_operation_resolver":"EXACT_NAMED_ROUTE_ONLY","dependencies":"CLOSED_CATALOG_REFERENCES_AND_OWNER_READS","execution_route":"RESOLUTION_TO_ONE_EXECUTION_SEGMENT_OR_EXPLICIT_OUT_OF_SCOPE","rng_retry":"op.roll only; fixed result reused" if any(x in rid for x in ("check","save","s6d07")) else "NOT_APPLICABLE_NO_RNG","authoritative_mutation":mutation,"mutation_rationale":"No artificial world change" if null else "Exact owner fields commit atomically","execution_segment":"EVENTLESS_ZERO_REVISION_ALLOWED" if null else "ONE_ATOMIC_SEGMENT_PARTIAL_COMMIT_FORBIDDEN","event_route":event,"receipt_route":"value.resolution_receipt linked to segment/events/exports","failures":["failure.idempotency_conflict","failure.state_revision_conflict","failure.hydration_required","failure.missing_reference","failure.catalog_context_incompatible","failure.execution_limit"],"idempotency_conflict":"same key+fingerprint reuses; differing fingerprint rejects","multiplayer_currentness":"pinned revisions fail closed; no global lock","suspension_chronology_recovery":"existing Step-3/5 owner or N/A; no new suspension","classification":classification,"positive_evidence":positive,"negative_space":negative,"downstream_gap":"NONE"}

def expected_routes():
 return [
 route("route.generic_check","check","bounded ability/skill uncertainty",["activity.check.generic"],["activity.check.generic"],"ENGINE_BOUND basis + bounded INVOCATION_ADJUDICATED dc","NO_AUTHORITATIVE_WORLD_MUTATION","event.check.resolved","BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC_EXECUTION_PATH","package Activity and exact primitive consumers","no DSL; separate exact consequence"),
 route("route.generic_save","save","bounded saving throw",["activity.save.generic"],["activity.save.generic"],"ENGINE_BOUND basis + bounded INVOCATION_ADJUDICATED dc","NO_AUTHORITATIVE_WORLD_MUTATION","event.save.resolved","BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC_EXECUTION_PATH","package Activity and exact primitive consumers","no arbitrary basis/threshold/consequence"),
 route("route.procedure_movement","procedure/movement","initiative, turn/action control, within-location budget spend and durable location transition",["transition.location_change"],["procedure.combat_minimal"],"ENGINE_BOUND actor/procedure/current canonical destination/revisions + fixed initiative RNG evidence","runtime.procedure exact state change; durable transition also world.actor location","event.procedure.state_changed or event.entity.moved by exact profile","FORMALIZED_DETERMINISTIC_PATH","closed control/movement request plus canonical world.location snapshot validation","no pathfinding; no fake location for within-location repositioning"),
 route("route.spatial_target_applicability","spatial applicability","seven exact TargetSpec/AreaSpec consumers",["activity.attack.ranged_weapon","activity.spell.fire_bolt","activity.spell.poison_spray","activity.spell.thunderclap","activity.spell.acid_splash","activity.spell.magic_missile","activity.spell.burning_hands"],[],"ENGINE_BOUND exact TargetSpec/candidate roles + fixed accepted fiction.target_reachable per candidate binding","NO_AUTHORITATIVE_WORLD_MUTATION","NONE; target selection is pre-commit calculation evidence","BOUNDED_LLM_ADJUDICATED_INPUT_TO_DETERMINISTIC_EXECUTION_PATH","exact consumer permission, strict fact envelope and binding fingerprint","no geometry/pathfinding/query; missing is typed failure; fact is not world truth"),
 route("route.asset_transfer","asset","exclusive significant Asset transfer",["transition.asset_transfer"],[],"ENGINE_BOUND Asset/placement/revision","world.asset exclusive placement","event.asset.transferred","FORMALIZED_DETERMINISTIC_PATH","closed Asset transfer request/result","no inventory/currency/economy"),
 route("route.asset_equip","asset","owned Asset held or worn",["transition.asset_status"],[],"ENGINE_BOUND Asset/owner/revision + closed mode","world.asset equipment.mode","event.asset.status_changed","FORMALIZED_DETERMINISTIC_PATH","closed Asset equip request/result","no undeclared capability"),
 route("route.asset_use","asset","validate significant Asset use",[],[],"ENGINE_BOUND Asset/owner/revision + admitted Activity","NO_AUTHORITATIVE_WORLD_MUTATION","NONE unless invoked Activity owns event","FORMALIZED_DETERMINISTIC_PATH","NONE|EXACT_ADMITTED_ACTIVITY","no generic consequence payload"),
 route("route.mechanical_null","resolution","valid result without durable world-state change",["activity.check.generic","activity.save.generic"],[],"accepted bindings + fixed roll","NO_AUTHORITATIVE_WORLD_MUTATION","event.check.resolved or event.save.resolved as mandated by the selected primitive","FORMALIZED_DETERMINISTIC_PATH","zero affected world revisions plus genuine resolution event and receipt","no StateDelta lifecycle or extra synthetic mutation event"),
 route("route.inherited_s6d07","character/combat/spell","exact S6D-07 seed routes",[],[],"EXACT S6D-07 OWNER","OWNER_AND_EXACT_CHANGE_OR_MECHANICAL_NULL","EXACT S6D-07 EVENT","FORMALIZED_DETERMINISTIC_PATH","S6D-07 owner + package","no broader corpus"),
 route("route.inherited_s6d08","health/effect/recovery","exact S6D-08 routes",[],[],"EXACT S6D-08 OWNER","OWNER_AND_EXACT_CHANGE_OR_MECHANICAL_NULL","EXACT S6D-08 EVENT","FORMALIZED_DETERMINISTIC_PATH","S6D-08 owner + seed","no scheduler/broad condition corpus"),
 route("route.out_of_scope","excluded","explicit decision-C exclusion",[],[],"NOT_APPLICABLE","NO_AUTHORITATIVE_WORLD_MUTATION","NONE","OUT_OF_SUPPORTED_MVP_SEED","2026-08-27 human decision C","absent/nonselectable pending exact consumer")]

def build_contract(root):
 root=Path(root); sets=build_expected_source_sets(root); required=sorted(set().union(*map(set,sets.values())));products={f"PRODUCT:{r['key']}":r for r in product_rows(root)}
 citations={"PACKAGE_CLOSURE_KEYS":["character-capabilities.json","character-mvp-seed.json","health-effects-recovery-seed.json","gameplay-spine-seed.json"],"ACTIVE_MACHINE_CONSUMER_KEYS":["DEV/CATALOG/mechanical-surfaces.json","DEV/CATALOG/portable-value-routes.json","DEV/CATALOG/activity-primitive-contracts.json"],"PRODUCT_PROMISE_KEYS":sorted({r["owner_path"] for r in products.values()})}
 ledger=[]
 for key in required:
  membership=[n for n,v in sets.items() if key in v];product=products.get(key);rid=product["route_id"] if product else route_for(key);out=(product and product["product_scope"]=="EXPLICITLY_OUT_OF_SCOPE") or rid=="route.out_of_scope";row_citations=[product["owner_path"]+" :: "+product["evidence_pattern"]] if product else citations[membership[0]]
  ledger.append({"source_key":key,"source_memberships":membership,"coverage_id":"coverage."+hashlib.sha256(key.encode()).hexdigest()[:16],"package_presence":"ABSENT" if out and key.startswith("PRODUCT:") else "PRESENT_ACTIVE_OR_TRANSITIVE","product_scope":"EXPLICITLY_OUT_OF_SCOPE" if out else "SUPPORTED","realization":"NOT_APPLICABLE" if out else "COMPLETE","disposition":"OUT_OF_SUPPORTED_MVP_SEED" if out else "IN_SUPPORTED_MVP","route_id":rid,"source_citations":row_citations,"negative_space":product["qualifier"] if product else "No utterance enumeration or authority beyond cited owner"})
 return {"schema_name":"hdm_domain_rules_coverage","schema_version":3,"profile_id":"gameplay_spine.mvp.v1","source_manifest":citations,"source_sets":sets,"required_coverage_keys":required,"coverage_ledger":ledger,"atomic_routes":expected_routes(),"scope_exclusions":["contest.generic","reaction.generic","damage_defense.broad","concentration.generic","currency.economy","crafting","downtime","teleportation","zone_entity_creation","equipment_corpus.broad","spell_hazard_corpus.broad"],"completeness_proof":{"coverage_minus_required":[],"required_minus_coverage":[],"orphan_machine_consumer_edges":[],"unresolved_matrix_references":[],"duplicate_source_keys":[],"supported_gaps":[]}}

def _package_identity(root):
 root=Path(root);package=root/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core";manifest=load(package/"ruleset-package-manifest.json")
 lock,snapshots=build_resolved_lock([package],root_package_ids=[manifest["package_id"]],engine_version=manifest["engine_requirement"]["engine_version"],catalog_generation=manifest["catalog_generation"])
 return manifest,lock,snapshots[manifest["package_id"]]

def build_binding(root):
 manifest,lock,snapshot=_package_identity(root)
 member="gameplay-spine-seed.json"
 if member not in {row["path"] for row in snapshot.members}: raise ValueError("detached gameplay spine member")
 return {"profile_id":"gameplay_spine.mvp.v1","package_id":manifest["package_id"],"package_revision":manifest["package_revision"],"compatibility_family":manifest["compatibility_family"],"compatibility_generation":manifest["compatibility_generation"],"catalog_generation":manifest["catalog_generation"],"gameplay_spine_member":member,"package_content_sha256":snapshot.content_sha256,"ruleset_set_digest_generation":lock["ruleset_set_digest_generation"],"ruleset_set_sha256":lock["ruleset_set_sha256"]}

def validate_binding(value,root=None):
 root=Path(root or Path(__file__).resolve().parents[2]);exact(value,BINDING,"coverage binding")
 CanonicalSchemaValidator(root/"DEV/SCHEMAS").validate(value,load(root/"DEV/SCHEMAS/domain-rules-coverage-binding.schema.json"))
 expected=build_binding(root)
 if value!=expected: raise ValueError(f"coverage binding differs from reconstructed package snapshot/resolved lock; expected={expected!r}; actual={value!r}")
 return True

def validate_gameplay_seed(spine,schemas):
 validator=CanonicalSchemaValidator(schemas);validator.validate(spine,load(Path(schemas)/"gameplay-spine-seed.schema.json"))
 rows={x["id"]:x for x in spine["activity_definitions"]}
 if set(rows)!={"activity.check.generic","activity.save.generic"}:raise ValueError("generic Activity inventory")
 abilities=["ability.charisma","ability.constitution","ability.dexterity","ability.intelligence","ability.strength","ability.wisdom"]
 check=rows["activity.check.generic"]["data"];save=rows["activity.save.generic"]["data"]
 if set(check)!={"family_id","parameters","steps"} or set(save)!={"family_id","parameters","steps"}:raise ValueError("Activity data escape hatch")
 if check["parameters"]["ability_id"]["allowed_values"]!=abilities or save["parameters"]["ability_id"]["allowed_values"]!=abilities:raise ValueError("ability basis not exact")
 if check["parameters"]["proficiency_id"]["allowed_values"]!=["proficiency.skill.sleight_of_hand","proficiency.skill.stealth"]:raise ValueError("proficiency basis not exact")
 if [x["op"] for x in check["steps"]]!=["op.roll","op.resolve_check"] or [x["op"] for x in save["steps"]]!=["op.roll","op.resolve_save"]:raise ValueError("generic Activity operation route")
 return True

def validate_contract(value,root=None):
 root=Path(root or Path(__file__).resolve().parents[2]); exact(value,TOP,"contract")
 if (value["schema_name"],value["schema_version"],value["profile_id"]) != ("hdm_domain_rules_coverage",3,"gameplay_spine.mvp.v1"): raise ValueError("identity mismatch")
 schemas=root/"DEV/SCHEMAS"; validator=CanonicalSchemaValidator(schemas); validator.validate(value,load(schemas/"domain-rules-coverage.schema.json")); validate_gameplay_seed(load(root/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json"),schemas)
 expected=build_contract(root)
 if value!=expected: raise ValueError("semantic coverage differs from deterministic producer")
 for key in ("source_manifest","source_sets","required_coverage_keys","atomic_routes","scope_exclusions","completeness_proof"):
  if value[key]!=expected[key]: raise ValueError(f"{key} differs from current owners")
 if len(value["coverage_ledger"])!=len(expected["coverage_ledger"]): raise ValueError("ledger cardinality")
 bykey={r.get("source_key"):r for r in value["coverage_ledger"]}
 if len(bykey)!=len(value["coverage_ledger"]) or set(bykey)!=set(value["required_coverage_keys"]): raise ValueError("ledger difference/orphan/duplicate")
 for row in value["coverage_ledger"]: exact(row,LEDGER,row.get("source_key","row"))
 if value["coverage_ledger"]!=expected["coverage_ledger"]: raise ValueError("ledger evidence/route mismatch")
 for row in value["atomic_routes"]: exact(row,ROUTE,row.get("route_id","route"))
 prim=load_activity_primitive_contracts(root); rows={x["primitive_id"]:x for x in prim["contracts"]}; activities=set()
 for name in ("character-mvp-seed.json","gameplay-spine-seed.json"): activities|={x["id"] for x in load(root/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"/name)["activity_definitions"]}
 for key in value["source_sets"]["ACTIVE_MACHINE_CONSUMER_KEYS"]:
  if key.startswith("MACHINE:edge:"):
   source,consumer=key.removeprefix("MACHINE:edge:").split("->",1)
   primitive_ok=source in rows and consumer in rows[source]["exact_seed_consumer_ids"]
   fact=load(root/"DEV/CATALOG/mechanical-surfaces.json")["context_facts"].get(source)
   fact_ok=fact is not None and fact["disposition"]=="ACTIVE_ADMITTED" and consumer in fact["permitted_consumer_ids"]
   if not (primitive_ok or fact_ok) or consumer not in activities: raise ValueError("orphan machine edge")
 validate_binding(load(root/"DEV/CATALOG/domain-rules-coverage-binding.json"),root)
 return True

def _fingerprint(request):
 return hashlib.sha256(json.dumps(request,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def _failure(request,code):
 return {"profile_id":request.get("profile_id","unknown.profile"),"idempotency_key":request.get("idempotency_key","unknown-key"),"status":"REJECTED","failure_code":code,"prospective_mutations":[],"event_ids":[]}
def _committed(profile,key,mutations,event_ids):
 revisions=sorted({f"{m['owner_id']}@{m['after_revision']}" for m in mutations})
 return {"profile_id":profile,"idempotency_key":key,"status":"COMPLETED","prospective_mutations":mutations,"execution_segment":{"segment_sequence":1,"commit_state":"committed","resulting_execution_state":"COMPLETED","affected_revision_refs":revisions,"event_ids":event_ids},"event_ids":event_ids,"receipt_ref":f"{key}:receipt"}
def _receipt_fixture(wire,exports=None):
 return {"execution_owner_id":f"resolution:{wire['idempotency_key']}","segment_refs":[f"resolution:{wire['idempotency_key']}:segment:1"],"status":wire["status"],"event_ids":wire["event_ids"],"exports":exports or {},"pending_child_refs":[]}
def _generic_activity_contract(activity_id):
 root=Path(__file__).resolve().parents[2]
 spine=load(root/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json")
 rows={row["id"]:row for row in spine["activity_definitions"]}
 activity=rows.get(activity_id)
 if activity is None:return None
 parameters=activity["data"]["parameters"]
 return {"ability_ids":set(parameters["ability_id"]["allowed_values"]),"dc_minimum":parameters["dc"]["minimum"],"dc_maximum":parameters["dc"]["maximum"]}
def execute_mechanical_null_resolution(req,receipts=None):
 receipts={} if receipts is None else receipts
 if not isinstance(req,dict):return (_failure({},"failure.missing_reference"),{})
 key=req.get("idempotency_key")
 if not isinstance(key,str) or not key:return (_failure(req,"failure.missing_reference"),{})
 fp=_fingerprint(req)
 if key in receipts:
  return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 exact_keys={"profile_id","idempotency_key","activity_id","ability_id","dc","roll"}
 family={"resolution.check":"check","resolution.save":"save"}.get(req.get("profile_id"))
 expected_activity=f"activity.{family}.generic" if family else None
 contract=_generic_activity_contract(expected_activity) if expected_activity else None
 roll=req.get("roll")
 roll_ok=isinstance(roll,dict) and set(roll)=={"rng_result_ref","d20","basis_modifier","proficiency_bonus"} and isinstance(roll.get("rng_result_ref"),str) and bool(roll.get("rng_result_ref")) and isinstance(roll.get("d20"),int) and 1<=roll["d20"]<=20 and all(isinstance(roll.get(k),int) for k in ("basis_modifier","proficiency_bonus"))
 request_ok=set(req)==exact_keys and req.get("activity_id")==expected_activity and contract is not None and req.get("ability_id") in contract["ability_ids"] and isinstance(req.get("dc"),int) and contract["dc_minimum"]<=req["dc"]<=contract["dc_maximum"] and roll_ok
 if not request_ok:return (_failure(req,"failure.missing_reference"),{})
 total=roll["d20"]+roll["basis_modifier"]+roll["proficiency_bonus"];result="SUCCESS" if total>=req["dc"] else "FAILURE"
 owner_id=f"resolution:{key}";segment_id=f"{owner_id}:segment:1";event_id=f"{segment_id}:event:1"
 segment={"segment_sequence":1,"commit_state":"committed","resulting_execution_state":"COMPLETED","event_ids":[event_id],"pending_child_invocations":[],"receipt_exports":{"result":result,"roll_total":total,"rng_result_ref":roll["rng_result_ref"]},"affected_revision_refs":[]}
 wire={"profile_id":req["profile_id"],"idempotency_key":key,"status":"COMPLETED","result":result,"prospective_mutations":[],"execution_segment":segment,"event_ids":[event_id],"receipt_ref":f"{owner_id}:receipt"}
 event={"segment_id":segment_id,"event_ordinal":1,"event_kind":f"event.{family}.resolved","root_command_id":key,"causal_ref":owner_id,"payload":{"activity_id":req["activity_id"],"ability_id":req["ability_id"],"dc":req["dc"],"roll":deepcopy(roll),"roll_total":total,"result":result}}
 receipt={"execution_owner_id":owner_id,"segment_refs":[segment_id],"status":"COMPLETED","event_ids":[event_id],"exports":{"result":result,"roll_total":total,"rng_result_ref":roll["rng_result_ref"]},"pending_child_refs":[]}
 transaction=(wire,{"segment_id":segment_id,"event_id":event_id,"mechanical_event":event,"receipt":receipt});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction
def _world_record(snapshot,kind,schemas):
 if set(snapshot)!={"record","revision"} or not isinstance(snapshot["revision"],int) or snapshot["revision"]<0:raise ValueError("owner snapshot is not exact")
 record=snapshot["record"]
 if record.get("kind")!=kind:raise ValueError("owner record kind mismatch")
 CanonicalSchemaValidator(schemas).validate(record,load(Path(schemas)/"world-record.schema.json"))
 return record
def validate_combat_procedure_state(state):
 participants=state["participant_ids"];order=state["initiative_order"];resources=state["participant_resources"]
 if len(participants)!=len(set(participants)) or len(order)!=len(participants) or set(order)!=set(participants):raise ValueError("initiative order is not exact participant permutation")
 if set(resources)!=set(participants):raise ValueError("participant resource keys mismatch")
 if not 0<=state["active_turn_index"]<len(participants):raise ValueError("active turn index out of range")
 if state["lifecycle_state"]=="turn_active" and state["round_advance_pending"]:raise ValueError("active turn cannot await round advance")
 for owned in resources.values():
  if set(owned)!={"resource.action_budget","resource.movement_budget"}:raise ValueError("procedure budget inventory mismatch")
  for budget in owned.values():
   if budget["spent"]>budget["capacity"]:raise ValueError("procedure spent exceeds capacity")
 return True
def initialize_combat_procedure(participants,initiative_order,action_capacity=1,movement_capacity=30):
 state={"procedure_kind":"procedure.combat_minimal","lifecycle_state":"between_turns","participant_ids":list(participants),"initiative_order":list(initiative_order),"round_number":1,"round_advance_pending":False,"active_turn_index":0,"participant_resources":{p:{"resource.action_budget":{"capacity":action_capacity,"spent":0},"resource.movement_budget":{"capacity":movement_capacity,"spent":0}} for p in participants}}
 validate_combat_procedure_state(state);return state
def advance_combat_turn(state):
 validate_combat_procedure_state(state);result=deepcopy(state);result["active_turn_index"]+=1
 if result["active_turn_index"]==len(result["participant_ids"]):result["active_turn_index"]=0;result["round_number"]+=1
 actor=result["initiative_order"][result["active_turn_index"]]
 for budget in result["participant_resources"][actor].values():budget["spent"]=0
 validate_combat_procedure_state(result);return result
def _procedure_failure(req,code):return _failure(req,code),{}
def execute_combat_procedure_transition(req,procedure=None,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else _procedure_failure(req,"failure.idempotency_conflict")
 profile=req["profile_id"]
 if profile=="procedure.initialize":
  if procedure is not None or req["procedure_revision"]!=0:return _procedure_failure(req,"failure.state_revision_conflict")
  rows=req["initiative_entries"];actors=[r["actor_id"] for r in rows];ranks=[r["tie_break_rank"] for r in rows];rng_refs=[r["rng_result_ref"] for r in rows]
  if len(actors)!=len(set(actors)) or len(rng_refs)!=len(set(rng_refs)) or sorted(ranks)!=list(range(1,len(rows)+1)):return _procedure_failure(req,"failure.missing_reference")
  ordered=[r["actor_id"] for r in sorted(rows,key=lambda r:(-r["roll_total"],r["tie_break_rank"]))]
  state=initialize_combat_procedure(actors,ordered,req["action_capacity"],req["movement_capacity"]);after={"id":req["procedure_id"],"revision":1,"state":state};before_revision=0
 else:
  if procedure is None or req["procedure_id"]!=procedure["id"]:return _procedure_failure(req,"failure.missing_reference")
  validate_combat_procedure_state(procedure["state"])
  if req["procedure_revision"]!=procedure["revision"]:return _procedure_failure(req,"failure.state_revision_conflict")
  state=deepcopy(procedure["state"]);before_revision=procedure["revision"]
  if state["lifecycle_state"]=="terminated":return _procedure_failure(req,"failure.transition_requires_procedure")
  active=state["initiative_order"][state["active_turn_index"]]
  if profile in {"procedure.start_turn","procedure.spend_action","procedure.spend_movement","procedure.end_turn"} and req["actor_id"]!=active:return _procedure_failure(req,"failure.missing_reference")
  if profile=="procedure.start_turn":
   if state["lifecycle_state"]!="between_turns" or state["round_advance_pending"]:return _procedure_failure(req,"failure.transition_requires_procedure")
   state["lifecycle_state"]="turn_active"
   for budget in state["participant_resources"][active].values():budget["spent"]=0
  elif profile=="procedure.spend_action":
   if state["lifecycle_state"]!="turn_active":return _procedure_failure(req,"failure.transition_requires_procedure")
   budget=state["participant_resources"][active]["resource.action_budget"]
   if budget["spent"]+req["amount"]>budget["capacity"]:return _procedure_failure(req,"failure.action_economy_scope_invalid")
   budget["spent"]+=req["amount"]
  elif profile=="procedure.spend_movement":
   if state["lifecycle_state"]!="turn_active":return _procedure_failure(req,"failure.transition_requires_procedure")
   budget=state["participant_resources"][active]["resource.movement_budget"]
   if budget["spent"]+req["amount"]>budget["capacity"]:return _procedure_failure(req,"failure.action_economy_scope_invalid")
   budget["spent"]+=req["amount"]
  elif profile=="procedure.end_turn":
   if state["lifecycle_state"]!="turn_active":return _procedure_failure(req,"failure.transition_requires_procedure")
   state["lifecycle_state"]="between_turns"
   if state["active_turn_index"]==len(state["initiative_order"])-1:state["round_advance_pending"]=True
   else:state["active_turn_index"]+=1
  elif profile=="procedure.advance_round":
   if state["lifecycle_state"]!="between_turns" or not state["round_advance_pending"]:return _procedure_failure(req,"failure.transition_requires_procedure")
   state["round_number"]+=1;state["active_turn_index"]=0;state["round_advance_pending"]=False
  elif profile=="procedure.terminate":state["lifecycle_state"]="terminated";state["round_advance_pending"]=False
  else:return _procedure_failure(req,"failure.missing_reference")
  validate_combat_procedure_state(state);after={"id":procedure["id"],"revision":procedure["revision"]+1,"state":state}
 mutation={"owner_kind":"runtime.procedure","owner_id":after["id"],"field_path":"state","before_revision":before_revision,"after_revision":after["revision"],"new_value":deepcopy(after["state"])}
 event_id=f"{key}:event:procedure-state-changed";wire=_committed(profile,key,[mutation],[event_id]);exports={"procedure_revision":after["revision"]}
 if profile=="procedure.initialize":
  exports["initiative_order_fingerprint"]=hashlib.sha256(json.dumps(after["state"]["initiative_order"],separators=(",",":")).encode()).hexdigest();exports["fixed_rng_evidence_fingerprint"]=hashlib.sha256(json.dumps(req["initiative_entries"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
 state_sha=hashlib.sha256(json.dumps(after["state"],sort_keys=True,separators=(",",":")).encode()).hexdigest();event={"segment_id":f"resolution:{key}:segment:1","event_ordinal":1,"event_kind":"event.procedure.state_changed","root_command_id":key,"causal_ref":f"resolution:{key}","procedure_id":after["id"],"payload":{"profile_id":profile,"field_path":"state","before_revision":before_revision,"after_revision":after["revision"],"after_state_sha256":state_sha}}
 transaction=(wire,{"procedure":after,"mechanical_event":event,"receipt":_receipt_fixture(wire,exports)});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction
def execute_procedure_movement(req,procedure,actor,destination,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 schemas=Path(__file__).resolve().parents[1]/"SCHEMAS";actor_record=_world_record(actor,"world.actor",schemas)
 try: destination_record=_world_record(destination,"world.location",schemas)
 except (ValueError,KeyError):return (_failure(req,"failure.missing_reference"),{})
 validate_combat_procedure_state(procedure["state"])
 if req["procedure_revision"]!=procedure["revision"] or req["actor_revision"]!=actor["revision"] or req["destination_location_revision"]!=destination["revision"]:return (_failure(req,"failure.state_revision_conflict"),{})
 aid=req["actor_id"]
 if req["procedure_id"]!=procedure["id"] or aid!=actor_record["id"] or aid not in procedure["state"]["participant_resources"] or req["destination_location_id"]!=destination_record["id"]:return (_failure(req,"failure.missing_reference"),{})
 budget=procedure["state"]["participant_resources"][aid]["resource.movement_budget"]
 if budget["spent"]+req["movement_cost"]>budget["capacity"]:return (_failure(req,"failure.action_economy_scope_invalid"),{})
 p=deepcopy(procedure);a=deepcopy(actor);p["state"]["participant_resources"][aid]["resource.movement_budget"]["spent"]+=req["movement_cost"];a["record"]["state"]["location_id"]=req["destination_location_id"];p["revision"]+=1;a["revision"]+=1;event=f"{key}:event:entity-moved"
 mutations=[{"owner_kind":"runtime.procedure","owner_id":p["id"],"field_path":f"state.participant_resources[{aid}].resource.movement_budget.spent","before_revision":procedure["revision"],"after_revision":p["revision"],"new_value":p["state"]["participant_resources"][aid]["resource.movement_budget"]["spent"]},{"owner_kind":"world.actor","owner_id":a["record"]["id"],"field_path":"state.location_id","before_revision":actor["revision"],"after_revision":a["revision"],"new_value":req["destination_location_id"]}]
 transaction=(_committed("location_change.procedure_movement",key,mutations,[event]),{"procedure":p,"actor":a});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction

def execute_outside_procedure_movement(req,actor,destination,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 schemas=Path(__file__).resolve().parents[1]/"SCHEMAS";record=_world_record(actor,"world.actor",schemas)
 try: destination_record=_world_record(destination,"world.location",schemas)
 except (ValueError,KeyError):return (_failure(req,"failure.missing_reference"),{})
 if req["actor_id"]!=record["id"] or req["destination_location_id"]!=destination_record["id"]:return (_failure(req,"failure.missing_reference"),{})
 if req["actor_revision"]!=actor["revision"] or req["destination_location_revision"]!=destination["revision"]:return (_failure(req,"failure.state_revision_conflict"),{})
 after=deepcopy(actor);after["record"]["state"]["location_id"]=req["destination_location_id"];after["revision"]+=1;event=f"{key}:event:entity-moved"
 mutation={"owner_kind":"world.actor","owner_id":record["id"],"field_path":"state.location_id","before_revision":actor["revision"],"after_revision":after["revision"],"new_value":req["destination_location_id"]}
 transaction=(_committed("location_change.outside_procedure",key,[mutation],[event]),{"actor":after});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction

def spatial_binding_fingerprint(consumer_id,target_spec,candidate_role,provenance_ref,rules_context_fingerprint,source_role="actor"):
 value={"consumer_id":consumer_id,"source_role":source_role,"target_spec":target_spec,"candidate_role":candidate_role,"spatial_provenance_ref":provenance_ref,"rules_context_fingerprint":rules_context_fingerprint}
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def select_spatial_targets(consumer_id,target_spec,candidate_roles,applicability_facts,rules_context_fingerprint):
 root=Path(__file__).resolve().parents[2];schemas=root/"DEV/SCHEMAS";validator=CanonicalSchemaValidator(schemas)
 validator.validate(target_spec,load(schemas/"target-spec.schema.json"))
 registry=load(root/"DEV/CATALOG/mechanical-surfaces.json")["context_facts"]["fiction.target_reachable"]
 if registry["disposition"]!="ACTIVE_ADMITTED" or consumer_id not in registry["permitted_consumer_ids"]:raise ValueError("spatial fact consumer is not admitted")
 if len(candidate_roles)>target_spec["maximum"]:raise ValueError("candidate set exceeds TargetSpec bound")
 by_binding={}
 for fact in applicability_facts:
  validator.validate(fact,load(schemas/"invocation-fact.schema.json"))
  if fact["fact_id"]!="fiction.target_reachable" or fact["consumer_id"]!=consumer_id:raise ValueError("wrong spatial fact binding")
  if fact["rules_context_fingerprint"]!=rules_context_fingerprint:raise ValueError("stale spatial fact rules context")
  if fact["binding_fingerprint"] in by_binding:raise ValueError("duplicate spatial fact binding")
  by_binding[fact["binding_fingerprint"]]=fact
 selected=[];used=set()
 for role in candidate_roles:
  candidates=[f for f in applicability_facts if f.get("consumer_id")==consumer_id and f.get("fact_id")=="fiction.target_reachable"]
  keys=[spatial_binding_fingerprint(consumer_id,target_spec,role,f["provenance_ref"],rules_context_fingerprint) for f in candidates]
  matches=[key for key in keys if key in by_binding]
  if len(matches)!=1:raise ValueError("missing or ambiguous fixed spatial applicability fact")
  key=matches[0]
  used.add(key)
  if by_binding[key]["value"]:selected.append(role)
 if used!=set(by_binding):raise ValueError("unbound spatial applicability fact")
 if len(selected)<target_spec["minimum"]:raise ValueError("too few spatially applicable targets")
 return selected

def execute_asset_transfer(req,asset,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 schemas=Path(__file__).resolve().parents[1]/"SCHEMAS";record=_world_record(asset,"world.asset",schemas)
 if req["asset_id"]!=record["id"]:return (_failure(req,"failure.missing_reference"),{})
 if req["asset_revision"]!=asset["revision"]:return (_failure(req,"failure.state_revision_conflict"),{})
 current={k:record["state"][k] for k in ("owner_actor_id","container_asset_id","location_id") if record["state"].get(k) is not None}
 if current!=req["from_placement"] or len(req["to_placement"])!=1:return (_failure(req,"failure.state_revision_conflict"),{})
 after=deepcopy(asset)
 for k in ("owner_actor_id","container_asset_id","location_id"):after["record"]["state"].pop(k,None)
 after["record"]["state"].update(req["to_placement"]);after["revision"]+=1;event=f"{key}:event:asset-transferred";muts=[{"owner_kind":"world.asset","owner_id":record["id"],"field_path":f"state.{k}","before_revision":asset["revision"],"after_revision":after["revision"],"new_value":after["record"]["state"].get(k)} for k in ("owner_actor_id","container_asset_id","location_id")]
 transaction=(_committed("asset.transfer",key,muts,[event]),{"asset":after});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction

def execute_asset_equip(req,asset,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 schemas=Path(__file__).resolve().parents[1]/"SCHEMAS";record=_world_record(asset,"world.asset",schemas)
 if req["asset_id"]!=record["id"] or record["state"].get("owner_actor_id")!=req["owner_actor_id"]:return (_failure(req,"failure.missing_reference"),{})
 if req["asset_revision"]!=asset["revision"]:return (_failure(req,"failure.state_revision_conflict"),{})
 after=deepcopy(asset);after["record"]["state"]["equipment"]={"mode":req["mode"]};after["revision"]+=1;event=f"{key}:event:asset-status-changed"
 mutation={"owner_kind":"world.asset","owner_id":record["id"],"field_path":"state.equipment.mode","before_revision":asset["revision"],"after_revision":after["revision"],"new_value":req["mode"]}
 transaction=(_committed("asset.equip",key,[mutation],[event]),{"asset":after});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction

def resolve_asset_use(req,asset,admitted_activity_ids,receipts=None):
 receipts={} if receipts is None else receipts;key=req["idempotency_key"];fp=_fingerprint(req)
 if key in receipts:return receipts[key]["transaction"] if receipts[key]["fingerprint"]==fp else (_failure(req,"failure.idempotency_conflict"),{})
 schemas=Path(__file__).resolve().parents[1]/"SCHEMAS";record=_world_record(asset,"world.asset",schemas)
 if req["asset_id"]!=record["id"] or record["state"].get("owner_actor_id")!=req["owner_actor_id"]:return (_failure(req,"failure.missing_reference"),{})
 if req["asset_revision"]!=asset["revision"]:return (_failure(req,"failure.state_revision_conflict"),{})
 if req["consequence_profile"]=="EXACT_ADMITTED_ACTIVITY" and req.get("activity_id") not in admitted_activity_ids:return (_failure(req,"failure.missing_reference"),{})
 wire=_committed("asset.use",key,[],[]);wire["activity_binding"]={"binding_kind":req["consequence_profile"]}
 if req["consequence_profile"]=="EXACT_ADMITTED_ACTIVITY":wire["activity_binding"]["activity_id"]=req["activity_id"]
 transaction=(wire,{});receipts[key]={"fingerprint":fp,"transaction":transaction};return transaction
