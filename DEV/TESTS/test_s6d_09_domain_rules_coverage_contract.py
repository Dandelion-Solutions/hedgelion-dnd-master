import copy, json, unittest
from pathlib import Path
import DEV.TOOLS.validate_domain_rules_coverage as coverage
from DEV.TOOLS.validate_character_mvp_seed import CanonicalSchemaValidator
from DEV.TOOLS.validate_domain_rules_coverage import advance_combat_turn, build_expected_source_sets, execute_asset_equip, execute_asset_transfer, execute_combat_procedure_transition, execute_outside_procedure_movement, execute_procedure_movement, initialize_combat_procedure, resolve_asset_use, validate_combat_procedure_state, validate_contract, validate_gameplay_seed

ROOT=Path(__file__).resolve().parents[2]
CAT=ROOT/"DEV/CATALOG/domain-rules-coverage.json"
PKG=ROOT/"GAME/RULES/packages/hdm.rules.dnd2024-srd52-core"

class CoverageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.value=json.loads(CAT.read_text(encoding="utf-8"))
 def validate_transition(self,value):
  schemas=ROOT/"DEV/SCHEMAS";CanonicalSchemaValidator(schemas).validate(value,json.loads((schemas/"gameplay-spine-transition-result.schema.json").read_text()))
 def test_contract_schema_and_semantics_are_green(self): self.assertTrue(validate_contract(self.value,ROOT))
 def test_three_exact_sets_and_bidirectional_union(self):
  self.assertEqual(self.value["source_sets"],build_expected_source_sets(ROOT))
  union=set().union(*(set(v) for v in self.value["source_sets"].values()))
  self.assertEqual(set(self.value["required_coverage_keys"]),union)
  self.assertEqual({x["source_key"] for x in self.value["coverage_ledger"]},union)
  self.assertEqual(len(self.value["coverage_ledger"]),len(union))
 def test_every_machine_edge_resolves_to_package_activity_and_primitive_owner(self):
  prim=json.loads((ROOT/"DEV/CATALOG/activity-primitive-contracts.json").read_text())
  rows={r["primitive_id"]:r for r in prim["contracts"]}
  facts=json.loads((ROOT/"DEV/CATALOG/mechanical-surfaces.json").read_text())["context_facts"]
  activities=set()
  for name in ("character-mvp-seed.json","gameplay-spine-seed.json"):
   activities|={r["id"] for r in json.loads((PKG/name).read_text())["activity_definitions"]}
  for key in self.value["source_sets"]["ACTIVE_MACHINE_CONSUMER_KEYS"]:
   if key.startswith("MACHINE:edge:"):
    source,consumer=key.removeprefix("MACHINE:edge:").split("->",1)
    self.assertIn(consumer,activities)
    if source in rows:self.assertIn(consumer,rows[source]["exact_seed_consumer_ids"])
    else:self.assertIn(consumer,facts[source]["permitted_consumer_ids"])
 def test_generic_activities_are_identity_bound_and_exact_consumers(self):
  spine=json.loads((PKG/"gameplay-spine-seed.json").read_text())
  self.assertEqual({x["id"] for x in spine["activity_definitions"]},{"activity.check.generic","activity.save.generic"})
  rows={r["primitive_id"]:r for r in json.loads((ROOT/"DEV/CATALOG/activity-primitive-contracts.json").read_text())["contracts"]}
  self.assertIn("activity.check.generic",rows["op.roll"]["exact_seed_consumer_ids"])
  self.assertIn("activity.save.generic",rows["op.roll"]["exact_seed_consumer_ids"])
  self.assertIn("activity.check.generic",rows["op.resolve_check"]["exact_seed_consumer_ids"])
  self.assertIn("activity.save.generic",rows["op.resolve_save"]["exact_seed_consumer_ids"])
 def test_generic_activity_schema_rejects_arbitrary_basis_and_consequence(self):
  schemas=ROOT/"DEV/SCHEMAS";v=CanonicalSchemaValidator(schemas);schema=json.loads((schemas/"gameplay-spine-seed.schema.json").read_text());spine=json.loads((PKG/"gameplay-spine-seed.json").read_text())
  self.assertTrue(v.validate(spine,schema))
  bad=copy.deepcopy(spine);bad["activity_definitions"][0]["data"]["parameters"]["ability_id"]["allowed_values"].append("ability.any")
  with self.assertRaises(Exception): validate_gameplay_seed(bad,schemas)
  bad=copy.deepcopy(spine);bad["activity_definitions"][0]["data"]["consequence_payload"]={"patch":"*"}
  with self.assertRaises(Exception): v.validate(bad,schema)
 def test_current_resource_and_failure_ids_are_registered(self):
  core=json.loads((ROOT/"DEV/CATALOG/core-catalog.json").read_text())["registries"]
  spine=json.loads((PKG/"gameplay-spine-seed.json").read_text())
  self.assertEqual(spine["procedure_profile"]["resource_ids"],["resource.action_budget","resource.movement_budget"])
  self.assertIn("failure.state_revision_conflict",core["execution_failure_codes"])
  self.assertNotIn("failure.execution_conflict",json.dumps(spine))
 def test_spatial_claim_has_a_dedicated_fact_backed_route(self):
  spatial=json.loads((PKG/"gameplay-spine-seed.json").read_text())["spatial_profile"]
  product=next(x for x in json.loads((ROOT/"DEV/CATALOG/product-promise-evidence.json").read_text())["rows"] if x["key"]=="product.spatial.target_range_area_bounded")
  self.assertEqual(product["route_id"],"route.spatial_target_applicability")
  self.assertIn("route.spatial_target_applicability",{x["route_id"] for x in self.value["atomic_routes"]})
  self.assertEqual(spatial["input_class"],"ENGINE_BOUND_OR_INVOCATION_ADJUDICATED")
  self.assertEqual(spatial["adjudicated_fact_ids"],["fiction.target_reachable"])
  facts=json.loads((ROOT/"DEV/CATALOG/mechanical-surfaces.json").read_text())["context_facts"]
  exact={"activity.attack.ranged_weapon","activity.spell.fire_bolt","activity.spell.poison_spray","activity.spell.thunderclap","activity.spell.acid_splash","activity.spell.magic_missile","activity.spell.burning_hands"}
  self.assertEqual(facts["fiction.target_reachable"]["disposition"],"ACTIVE_ADMITTED")
  self.assertEqual(set(facts["fiction.target_reachable"]["permitted_consumer_ids"]),exact)
  self.assertEqual(facts["fiction.target_visible"]["disposition"],"DORMANT_RESERVED")

 def test_supported_spatial_consumers_declare_exact_target_specs_and_fixed_facts(self):
  character=json.loads((PKG/"character-mvp-seed.json").read_text())
  consumers={"activity.attack.ranged_weapon","activity.spell.fire_bolt","activity.spell.poison_spray","activity.spell.thunderclap","activity.spell.acid_splash","activity.spell.magic_missile","activity.spell.burning_hands"}
  rows={x["id"]:x for x in character["activity_definitions"]}
  validator=CanonicalSchemaValidator(ROOT/"DEV/SCHEMAS")
  target_schema=json.loads((ROOT/"DEV/SCHEMAS/target-spec.schema.json").read_text())
  for consumer in consumers:
   spec=rows[consumer]["data"]["targeting"];validator.validate(spec,target_schema)
   select=next(x for x in rows[consumer]["data"]["steps"] if x["op"]=="op.select_targets")
   self.assertEqual(select["args"],{"target_spec":"activity.targeting","source_role":"actor","candidate_roles":"invocation.candidate_roles","applicability_facts":"invocation.fiction.target_reachable"})
  spec=rows["activity.spell.fire_bolt"]["data"]["targeting"]
  fact={"fact_id":"fiction.target_reachable","value":True,"provenance_class":"INVOCATION_ADJUDICATED","provenance_ref":"gm:scene-1","consumer_id":"activity.spell.fire_bolt","binding_fingerprint":coverage.spatial_binding_fingerprint("activity.spell.fire_bolt",spec,"target-1","gm:scene-1","a"*64),"rules_context_fingerprint":"a"*64}
  first=coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[fact],"a"*64)
  retry=coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[fact],"a"*64)
  self.assertEqual(first,retry);self.assertEqual(first,["target-1"])
  with self.assertRaises(ValueError): coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[],"a"*64)
  wrong=copy.deepcopy(fact);wrong["binding_fingerprint"]="b"*64
  with self.assertRaises(ValueError): coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[wrong],"a"*64)
  denied=copy.deepcopy(fact);denied["value"]=False
  with self.assertRaises(ValueError): coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[denied],"a"*64)
  with self.assertRaises(ValueError): coverage.select_spatial_targets("activity.spell.fire_bolt",spec,["target-1"],[fact],"b"*64)
  extra=copy.deepcopy(fact);extra["lifecycle"]="pending"
  with self.assertRaises(Exception): validator.validate(extra,json.loads((ROOT/"DEV/SCHEMAS/invocation-fact.schema.json").read_text()))
 def test_procedure_semantic_invariants_and_advance(self):
  state=initialize_combat_procedure(["a","b"],["b","a"]);self.assertTrue(validate_combat_procedure_state(state));advanced=advance_combat_turn(state);self.assertEqual(advanced["active_turn_index"],1);advanced=advance_combat_turn(advanced);self.assertEqual((advanced["active_turn_index"],advanced["round_number"]),(0,2))
  for mutate in (lambda x:x["initiative_order"].append("c"),lambda x:x["participant_resources"].pop("a"),lambda x:x.update(active_turn_index=2),lambda x:x["participant_resources"]["a"]["resource.action_budget"].update(spent=2)):
   bad=copy.deepcopy(state);mutate(bad)
   with self.assertRaises(ValueError):validate_combat_procedure_state(bad)
 def test_all_control_procedure_transitions_are_closed_retry_safe_and_schema_valid(self):
  schemas=ROOT/"DEV/SCHEMAS";v=CanonicalSchemaValidator(schemas);request_schema=json.loads((schemas/"combat-procedure-transition-request.schema.json").read_text());result_schema=json.loads((schemas/"combat-procedure-transition-result.schema.json").read_text())
  init={"profile_id":"procedure.initialize","idempotency_key":"proc-init-1","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":0,"initiative_entries":[{"actor_id":"actor-a","roll_total":14,"rng_result_ref":"rng-a","tie_break_rank":2},{"actor_id":"actor-b","roll_total":14,"rng_result_ref":"rng-b","tie_break_rank":1}],"action_capacity":1,"movement_capacity":30}
  event_schema=json.loads((schemas/"procedure-state-changed-event.schema.json").read_text());v.validate(init,request_schema);receipts={};transaction=execute_combat_procedure_transition(init,None,receipts);self.assertIs(transaction,execute_combat_procedure_transition(init,None,receipts));wire,after=transaction;v.validate(wire,result_schema);v.validate(after["mechanical_event"],event_schema);v.validate(after["receipt"],json.loads((schemas/"resolution-receipt.schema.json").read_text()));procedure=after["procedure"];self.assertEqual(procedure["state"]["initiative_order"],["actor-b","actor-a"]);self.assertIn("fixed_rng_evidence_fingerprint",after["receipt"]["exports"])
  missing_event=copy.deepcopy(wire);missing_event["event_ids"]=[];missing_event["execution_segment"]["event_ids"]=[]
  with self.assertRaises(Exception):v.validate(missing_event,result_schema)
  sequence=[
   {"profile_id":"procedure.start_turn","actor_id":"actor-b"},
   {"profile_id":"procedure.spend_action","actor_id":"actor-b","amount":1},
   {"profile_id":"procedure.end_turn","actor_id":"actor-b"},
   {"profile_id":"procedure.start_turn","actor_id":"actor-a"},
   {"profile_id":"procedure.end_turn","actor_id":"actor-a"},
   {"profile_id":"procedure.advance_round"},
   {"profile_id":"procedure.terminate"}
  ]
  for index,delta in enumerate(sequence,1):
   req={"idempotency_key":f"proc-{index}","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":procedure["revision"],**delta};v.validate(req,request_schema);wire,after=execute_combat_procedure_transition(req,procedure,{});v.validate(wire,result_schema);v.validate(after["mechanical_event"],event_schema);v.validate(after["receipt"],json.loads((schemas/"resolution-receipt.schema.json").read_text()));procedure=after["procedure"]
  self.assertEqual(procedure["state"]["round_number"],2);self.assertEqual(procedure["state"]["lifecycle_state"],"terminated")
 def test_procedure_rejects_unfixed_tie_overspend_wrong_phase_and_retry_conflict(self):
  bad_init={"profile_id":"procedure.initialize","idempotency_key":"bad-init","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":0,"initiative_entries":[{"actor_id":"a","roll_total":10,"rng_result_ref":"rng-same","tie_break_rank":1},{"actor_id":"b","roll_total":10,"rng_result_ref":"rng-same","tie_break_rank":1}],"action_capacity":1,"movement_capacity":30}
  wire,_=execute_combat_procedure_transition(bad_init,None,{});self.assertEqual(wire["failure_code"],"failure.missing_reference")
  procedure={"id":"procedure-1","revision":1,"state":initialize_combat_procedure(["a"],["a"])}
  spend={"profile_id":"procedure.spend_action","idempotency_key":"spend","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":1,"actor_id":"a","amount":1};wire,_=execute_combat_procedure_transition(spend,procedure,{});self.assertEqual(wire["failure_code"],"failure.transition_requires_procedure")
  start={"profile_id":"procedure.start_turn","idempotency_key":"start","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":1,"actor_id":"a"};_,after=execute_combat_procedure_transition(start,procedure,{});procedure=after["procedure"]
  spend["procedure_revision"]=procedure["revision"];spend["amount"]=2;wire,_=execute_combat_procedure_transition(spend,procedure,{});self.assertEqual(wire["failure_code"],"failure.action_economy_scope_invalid")
  receipts={};spend["amount"]=1;first=execute_combat_procedure_transition(spend,procedure,receipts);conflict=copy.deepcopy(spend);conflict["amount"]=2;wire,_=execute_combat_procedure_transition(conflict,procedure,receipts);self.assertEqual(wire["failure_code"],"failure.idempotency_conflict");self.assertEqual(first[0]["status"],"COMPLETED")
 def test_movement_commits_two_owners_in_one_segment_and_retries(self):
  procedure={"id":"procedure-1","revision":4,"state":initialize_combat_procedure(["actor-1"],["actor-1"])};procedure["state"]["participant_resources"]["actor-1"]["resource.movement_budget"]["spent"]=5
  actor={"record":{"id":"actor-1","kind":"world.actor","state":{"location_id":"location-a"}},"revision":7}
  destination={"record":{"id":"location-b","kind":"world.location","state":{"name":"Corridor"}},"revision":3}
  request={"transition_kind":"transition.location_change","profile_id":"location_change.procedure_movement","idempotency_key":"move-1","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":4,"actor_id":"actor-1","actor_revision":7,"destination_location_id":"location-b","destination_location_revision":3,"movement_cost":10}
  receipts={};first=execute_procedure_movement(request,procedure,actor,destination,receipts);retry=execute_procedure_movement(request,procedure,actor,destination,receipts)
  self.assertIs(first,retry);wire,after=first;self.assertEqual(wire["status"],"COMPLETED");self.assertEqual(len(wire["prospective_mutations"]),2);self.assertEqual(len(wire["execution_segment"]["affected_revision_refs"]),2)
  self.assertEqual(after["procedure"]["state"]["participant_resources"]["actor-1"]["resource.movement_budget"]["spent"],15);self.assertEqual(after["actor"]["record"]["state"]["location_id"],"location-b")
  schemas=ROOT/"DEV/SCHEMAS";validator=CanonicalSchemaValidator(schemas)
  validator.validate(request,json.loads((schemas/"gameplay-spine-transition-request.schema.json").read_text()))
  self.validate_transition(wire)
 def test_movement_conflict_or_budget_failure_has_no_partial_commit(self):
  p={"id":"p","revision":2,"state":initialize_combat_procedure(["a"],["a"],movement_capacity=5)};a={"record":{"id":"a","kind":"world.actor","state":{"location_id":"x"}},"revision":3}
  destination={"record":{"id":"y","kind":"world.location","state":{"name":"Corridor"}},"revision":1};req={"profile_id":"location_change.procedure_movement","idempotency_key":"k","procedure_id":"p","procedure_revision":1,"actor_revision":3,"actor_id":"a","destination_location_id":"y","destination_location_revision":1,"movement_cost":1}
  out,_=execute_procedure_movement(req,p,a,destination,{});self.assertEqual(out["failure_code"],"failure.state_revision_conflict");self.assertEqual(out["prospective_mutations"],[]);self.assertEqual(a["record"]["state"]["location_id"],"x");self.validate_transition(out)
  req.update({"procedure_revision":2,"movement_cost":6});out,_=execute_procedure_movement(req,p,a,destination,{});self.assertEqual(out["failure_code"],"failure.action_economy_scope_invalid");self.assertEqual(out["prospective_mutations"],[]);self.validate_transition(out)
  req.update({"movement_cost":1,"destination_location_revision":2});out,_=execute_procedure_movement(req,p,a,destination,{});self.assertEqual(out["failure_code"],"failure.state_revision_conflict")
  fake={"record":{"id":"y","kind":"world.actor","state":{"location_id":"x"}},"revision":2}
  out,_=execute_procedure_movement(req,p,a,fake,{});self.assertEqual(out["failure_code"],"failure.missing_reference")
 def test_outside_procedure_movement_changes_only_canonical_actor(self):
  actor={"record":{"id":"actor-1","kind":"world.actor","state":{"location_id":"location-a"}},"revision":7};destination={"record":{"id":"location-b","kind":"world.location","state":{"name":"Corridor"}},"revision":3};request={"transition_kind":"transition.location_change","profile_id":"location_change.outside_procedure","idempotency_key":"move-out-1","catalog_generation":"2.0.0","actor_id":"actor-1","actor_revision":7,"destination_location_id":"location-b","destination_location_revision":3,"movement_cost":"NOT_APPLICABLE_OUTSIDE_PROCEDURE"}
  schemas=ROOT/"DEV/SCHEMAS";CanonicalSchemaValidator(schemas).validate(request,json.loads((schemas/"gameplay-spine-transition-request.schema.json").read_text()))
  wire,after=execute_outside_procedure_movement(request,actor,destination,{});self.assertEqual(after["actor"]["record"]["state"]["location_id"],"location-b");self.assertEqual({x["owner_kind"] for x in wire["prospective_mutations"]},{"world.actor"});self.validate_transition(wire)
  invalid=copy.deepcopy(destination);invalid["record"]["state"]={"environment_ids":[]}
  with self.assertRaises(Exception):CanonicalSchemaValidator(schemas).validate(invalid["record"],json.loads((schemas/"world-record.schema.json").read_text()))
  missing_revision=copy.deepcopy(request);missing_revision.pop("destination_location_revision")
  with self.assertRaises(Exception):CanonicalSchemaValidator(schemas).validate(missing_revision,json.loads((schemas/"gameplay-spine-transition-request.schema.json").read_text()))

 def test_within_location_reposition_spends_budget_without_fake_location(self):
  procedure={"id":"procedure-1","revision":2,"state":initialize_combat_procedure(["actor-1"],["actor-1"])}
  start={"profile_id":"procedure.start_turn","idempotency_key":"start-move","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":2,"actor_id":"actor-1"};_,after=execute_combat_procedure_transition(start,procedure,{});procedure=after["procedure"]
  req={"profile_id":"procedure.spend_movement","idempotency_key":"reposition-1","catalog_generation":"2.0.0","procedure_id":"procedure-1","procedure_revision":procedure["revision"],"actor_id":"actor-1","amount":10}
  schemas=ROOT/"DEV/SCHEMAS";validator=CanonicalSchemaValidator(schemas);validator.validate(req,json.loads((schemas/"combat-procedure-transition-request.schema.json").read_text()))
  wire,after=execute_combat_procedure_transition(req,procedure,{})
  validator.validate(wire,json.loads((schemas/"combat-procedure-transition-result.schema.json").read_text()));validator.validate(after["mechanical_event"],json.loads((schemas/"procedure-state-changed-event.schema.json").read_text()))
  self.assertEqual({x["owner_kind"] for x in wire["prospective_mutations"]},{"runtime.procedure"})
  self.assertEqual(after["procedure"]["state"]["participant_resources"]["actor-1"]["resource.movement_budget"]["spent"],10)
  spine=json.loads((PKG/"gameplay-spine-seed.json").read_text())
  self.assertEqual(spine["procedure_profile"]["transition_profiles"]["spend_movement"],"procedure.spend_movement")
  self.assertEqual(spine["spatial_profile"]["within_location_reposition"],"FICTIONAL_POSITION_PLUS_PROCEDURE_BUDGET; NO_WORLD_LOCATION_MUTATION")
 def test_asset_transfer_is_exclusive_atomic_and_retry_safe(self):
  asset={"record":{"id":"asset-1","kind":"world.asset","state":{"owner_actor_id":"actor-a","equipment":{"mode":"held"}}},"revision":2};req={"transition_kind":"transition.asset_transfer","profile_id":"asset.transfer","idempotency_key":"transfer-1","catalog_generation":"2.0.0","asset_id":"asset-1","asset_revision":2,"from_placement":{"owner_actor_id":"actor-a"},"to_placement":{"owner_actor_id":"actor-b"}}
  receipts={};transaction=execute_asset_transfer(req,asset,receipts);self.assertIs(transaction,execute_asset_transfer(req,asset,receipts));wire,after=transaction;self.assertEqual(after["asset"]["record"]["state"]["owner_actor_id"],"actor-b");self.assertNotIn("location_id",after["asset"]["record"]["state"]);self.assertEqual(len(wire["prospective_mutations"]),3);self.validate_transition(wire)
  schemas=ROOT/"DEV/SCHEMAS";CanonicalSchemaValidator(schemas).validate(req,json.loads((schemas/"gameplay-spine-transition-request.schema.json").read_text()))
  legacy={"id":"asset-1","revision":2,"state":{"owner_actor_id":"actor-a"}}
  with self.assertRaises(ValueError):execute_asset_transfer(req,legacy,{})
 def test_asset_equip_and_use_are_canonical_bounded_and_schema_valid(self):
  asset={"record":{"id":"asset-1","kind":"world.asset","state":{"owner_actor_id":"actor-a"}},"revision":2}
  equip={"transition_kind":"transition.asset_status","profile_id":"asset.equip","idempotency_key":"equip-1","catalog_generation":"2.0.0","asset_id":"asset-1","asset_revision":2,"owner_actor_id":"actor-a","mode":"worn"}
  schemas=ROOT/"DEV/SCHEMAS";requests=json.loads((schemas/"gameplay-spine-transition-request.schema.json").read_text());CanonicalSchemaValidator(schemas).validate(equip,requests)
  wire,after=execute_asset_equip(equip,asset,{});self.assertEqual(after["asset"]["record"]["state"]["equipment"],{"mode":"worn"});self.validate_transition(wire)
  use={"profile_id":"asset.use","idempotency_key":"use-1","catalog_generation":"2.0.0","asset_id":"asset-1","asset_revision":2,"owner_actor_id":"actor-a","consequence_profile":"EXACT_ADMITTED_ACTIVITY","activity_id":"activity.check.generic"}
  CanonicalSchemaValidator(schemas).validate(use,requests);receipts={};transaction=resolve_asset_use(use,asset,{"activity.check.generic"},receipts);self.assertIs(transaction,resolve_asset_use(use,asset,{"activity.check.generic"},receipts));wire,after=transaction;self.assertEqual(after,{});self.assertEqual(wire["prospective_mutations"],[]);self.assertEqual(wire["event_ids"],[]);self.assertEqual(wire["activity_binding"],{"binding_kind":"EXACT_ADMITTED_ACTIVITY","activity_id":"activity.check.generic"});self.validate_transition(wire)
  conflict=copy.deepcopy(use);conflict["activity_id"]="activity.save.generic";wire,_=resolve_asset_use(conflict,asset,{"activity.check.generic","activity.save.generic"},receipts);self.assertEqual(wire["failure_code"],"failure.idempotency_conflict");self.validate_transition(wire)
  bad=copy.deepcopy(use);bad["activity_id"]="activity.unadmitted";wire,_=resolve_asset_use(bad,asset,{"activity.check.generic"},{});self.assertEqual(wire["failure_code"],"failure.missing_reference");self.validate_transition(wire)
 def test_mechanical_null_has_no_fake_delta_or_event(self):
  route=next(x for x in self.value["atomic_routes"] if x["route_id"]=="route.mechanical_null")
  self.assertEqual(route["authoritative_mutation"],"NO_AUTHORITATIVE_WORLD_MUTATION");self.assertIn("event.check.resolved",route["event_route"]);self.assertIn("event.save.resolved",route["event_route"]);self.assertNotIn("StateDelta",route["positive_evidence"])
 def test_negative_source_difference_or_orphan_fails(self):
  for mutate in (lambda x:x["source_sets"]["PACKAGE_CLOSURE_KEYS"].pop(),lambda x:x["coverage_ledger"].append(copy.deepcopy(x["coverage_ledger"][0])),lambda x:x["source_sets"]["ACTIVE_MACHINE_CONSUMER_KEYS"].append("MACHINE:edge:op.roll->activity.missing")):
   bad=copy.deepcopy(self.value);mutate(bad)
   with self.assertRaises(ValueError):validate_contract(bad,ROOT)
 def test_negative_route_or_schema_member_fails(self):
  bad=copy.deepcopy(self.value);bad["atomic_routes"][0]["universal_rules_dsl"]=True
  with self.assertRaises(Exception):validate_contract(bad,ROOT)
  bad=copy.deepcopy(self.value);bad["completeness_proof"]["supported_gaps"]=["gap"]
  with self.assertRaises(Exception):validate_contract(bad,ROOT)

if __name__=="__main__": unittest.main()

