# GAME spell production trace and minimal realization evidence

Status: Step-2 design evidence / candidate implications only. Read-only investigation; no production change, gameplay, release-package inspection, remote write, implementation authorization, or canonical amendment.

Repository: Dandelion-Solutions/hedgelion-dnd-master.
Branch: v1/engine-rearchitecture.
Pinned and freshly observed remote HEAD: 05576261665280c3f424d791c19d8c4080343c6a.
Date: 2026-10-04.

## 1. Conclusion and confidence

The accepted HDM architecture already supplies the intended bounded declarative Activity, pinned MechanicalContext/Calculation, native semantic owners, ExecutionSegment, fixed-input retry, HOT/publication and LIVE laws. A separate spell engine, persistent spell state family, gameplay role, sibling service, or arbitrary scripting mechanism is unnecessary.

The shipped Python modules provide meaningful component implementations, but the inspected GAME production path is not an end-to-end spell evaluator. The existing catalog binder establishes exact source identity; the mechanics module produces execution evidence from caller-supplied resolution/event values; native HOT, publication and LIVE components have distinct bounded consumers. No composed caller was found joining these to evaluation of an Activity recipe and atomic native Actor/Effect/Asset consequences.

Two additional contradictions are established from current function signatures and carrier shapes: the current accepted catalog carrier does not match the execution/durability join's flattened generation check; the composed host publication route cannot supply the join required for runtime.command publication. Their predicted runtime consequences are static and not exercised. Neither finding automatically reopens previously accepted Wave closure or bounded fixtures. They are dependencies of a future real casting consumer.

Confidence: HIGH for the exact inspected function/carrier facts and bounded consumer search; MEDIUM for candidate realization implications; no executable/full-339/latency claim.

## 2. Bounded dependency subgraph and source manifest

Subgraph: local package bytes/identity -> source-authenticated catalog context -> exact candidate and accepted command -> compiled Activity/typed read/evaluation -> native owner prospective plans -> Step-3 segment -> HOT or exact LIVE establishment -> execution/durability join -> existing publication/recovery -> role-safe receipt presentation.

Side routes: Effect application/support/temporal state; Procedure costs/continuations; Rule Elements/selectors/accessors/scoped DAG; supporting archetypes/Assets; application authorization/currentness.

All repository evidence below was fetched through the GitHub Connector at the pinned SHA. No local checkout state or default-branch code search was used as correctness evidence.

| Source | Role / inspected scope | Qualification |
|---|---|---|
| AGENTS.md; DEV/AGENT_RUNTIMES/CHATGPT_WORK.md; SKILL_SCOPE.md; DEV/DESIGN_PROCESS.md; DEV/ARCHITECTURE/DESIGN_PROCESS.md | Process/transport/role inheritance and applicable design gate | Parent supplies authorized Stop-1 GO and bounded read-only slice |
| DEV/PROJECT_MAP.md; DEV/CURRENT_PROGRESS.md | Routing/current scope; owner discovery | Derivative map is not semantic authority; global cursor not advanced |
| DEV/ARCHITECTURE/ACTIVITY_MODEL.md | Activity composition, cost, binding, partial completion, cached compilation and no intermediate LLM calls | Accepted design is separate from realization |
| ACTIVITY_PRIMITIVE_CONTRACTS.md; selected primitive shards op.select_targets, op.apply_damage, op.consume_resource, op.create_effect, op.transform_entity, op.schedule_followup | Exact active/closed/quarantined capability boundary | Registered names do not authorize execution |
| RULE_ELEMENT_MODEL.md; MECHANICAL_CONTEXT.md; CALCULATION_SELECTOR_METADATA.md; mechanical-surfaces.json | Pure contributions, pinned reads, exact consumer permissions, single scoped DAG and cache law | Shape/admission evidence is not a shipped evaluator |
| ACTOR_MODEL.md; ASSET_MODEL.md; HEALTH_EFFECTS_RECOVERY.md | Native ownership; stable identities; health/effect/resource/support/temporal boundaries | Health/concentration/periodic breadth remains explicitly bounded |
| 2026-08-19-step-3-execution-boundary-canonical-spec.md | Command, binder, native segment, mandatory children, receipts, retry, continuation/reactions | No standalone segment/Signal/StateDelta lifecycle |
| 2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md | HOT establishment, native owner admission, local atomicity versus LIVE | No SQLite transaction across external edges |
| 2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md | Distinct establishment/durability, current closure, tri-state publication and partial success | One user cast is not a universal commit-count guarantee |
| 2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md | Due/native owner and chronology route | Temporal helpers are derived; not background jobs |
| 2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md | Exact-source CAS, claim isolation, cross-source partial establishment, identity | No distributed transaction or global freshness scalar |
| GAME/TOOLS/catalog_runtime.py; runtime_execution.py; mechanics.py; runtime_host.py; current_owner.py; hot_store.py; ruleset_package.py; temporal.py; native_storage.py; durability.py; publication.py; recovery.py; live_state.py; turn_runtime.py | Actual producers, signatures, call sites, source shapes and closure seams | Function-scoped depth; remaining GAME tools inspected for concrete imports/calls |
| All 31 Python files under GAME/TOOLS in exact recursive remote tree | Bounded consumer search for named binder/evaluation/mutation/join paths | Whole-tool-tree symbols/imports; not claim of recursively read repository or all non-Python behavior |
| DEV/TOOLS/validate_character_mvp_seed.py; validate_health_effects_recovery_seed.py | DEV compilation/reference transitions | DEV is not shipped; health file explicitly labels itself conformance-only |
| DEV/TESTS/test_rd05_runtime_execution.py; test_rd15_catalog_runtime.py; test_rd04_native_routing_index_hot.py; test_rd06_durability_publication.py; test_runtime_host_composition.py; test_s6d_07_character_mvp_seed.py; test_s6d_08_health_effects_recovery_contract.py | Concrete fixture inputs/assertions and test proof boundaries | Tests inspected, not executed |

## 3. Actual production trace

### 3.1 Package and catalog source binding

GAME/TOOLS/ruleset_package.py:
- build_snapshot (238-264) checks exact manifest/member paths, non-symlink and non-escaping bytes, builds member digests and semantic-entry digests.
- build_resolved_lock (286 onward) resolves package closure and identity.
- compile_conformance_attestation (568-596) and validate_runtime_conformance_evidence (599-619) bind the closed validator roster, engine inventory and ruleset-set digest.
- PackageSnapshot (169-174) carries package_dir, manifest, content_sha256, members and semantic entries. This is not a compiled Activity object.

GAME/TOOLS/catalog_runtime.py:
- bind_catalog_context (537-569) authenticates the exact basis, source inventory/natural-owner bytes and dependencies; returns a sealed immutable BoundCatalogContext.
- _normalize_dependencies (421-534) calls _rebuild_definition_sources (372-418).
- _rebuild_definition_sources reconstructs build_resolved_lock from package directories every binding and verifies source definitions/kinds/package identity against that rebuilt lock.
- bind_interpreter_candidate (593-635) binds exact ID/kind to source and accepted-context fingerprint.
- validate_executable_binding (638-701) rejects stale/forged/incompatible context and source identity.
- bind_executable_catalog (704 onward) returns bound identity or typed catalog gap.

This is strong source identity machinery. It does not parse Activity instructions into a compiled executable object, compute transitive primitive/selector/accessor permission, or make a registered operation executable. Its dependency rows are source identity metadata rather than a verified executable read/write closure. No active compile cache exists here. The present rebuild path is a cold/admission function that should not be silently advertised as a warm cast path.

### 3.2 Accepted command

GAME/TOOLS/runtime_execution.py:
- accept_command (1115-1204) validates exact interpreter/proposal shape, resolver-issued adjudication basis, frozen parameters/facts and policy witnesses; calls bind_executable_catalog and validates the returned binding.
- _typed_command_proposal (1045-1095) restricts action_request to activity_id, actor_id, source_id, target_ids, parameter_bindings.
- validate_execution_proposal (1207-1307) revalidates the accepted source-context/candidate and recomputed accepted/interpreter fingerprints.
- resolve_native_ordering_evidence (886-976) supplies owner-native ordering/pending-continuation evidence. It is not the deterministic recipe evaluator.

Acceptance code does not perform spell-selection eligibility, component availability, action-economy/slot commitment, target owner validation, selector calculation, or primitive dispatch. These remain future invocation consumers. Calling this binder with an exact ID proves source binding, not that the actor can cast it.

### 3.3 Deterministic mechanics evidence

GAME/TOOLS/mechanics.py:
- ExecutionStore (175-233) is an in-memory atomic owner/segment store with command and execution fingerprint conflict checks.
- execute_segment (236-425) accepts a caller-supplied Resolution, optional one roll_request/RngProvider, one event_kind/event_payload, Procedure and Continuation values.
- It derives stable segment/event identity, reuses a prior fixed roll on exact retry/replay, preserves caller-supplied owners, and commits evidence to ExecutionStore.
- Lines 374-390 construct one segment/receipt with pending_child_invocations=[], pending_child_refs=[] and affected_revision_refs=[].
- resolve_mechanic (428-453) and resume_accepted_execution (456-487) only delegate to execute_segment.
- close_resolution (490-519) requires stored committed evidence and cannot change its identities.

No recipe argument, primitive registry dispatcher, MechanicalContext/Calculation evaluator, target enumeration, native HP/Effect/Asset owner plan or HOT/native commit port appears in this module. FixedRng is a small one-value fixture/provider with draw-count and rollback helpers; this is not proof of arbitrary multi-roll production PRNG continuity.

The evidence owner is useful and replay-safe for its tested scope. It cannot itself establish that supplied damage/check exports are mathematically derived from current admitted mechanics. A committed event payload is not proof that a native owner consequence occurred.

### 3.4 Native read and local establishment

GAME/TOOLS/current_owner.py:
- CurrentOwnerReadSession.require (192-250) accumulates an exact finite owner-key union and reacquires one admitted HOT snapshot; otherwise reads pinned campaign or selected LIVE owners.
- revalidate (255-331) refreshes campaign/LIVE basis, checks the union's HOT snapshot and every read basis, and confirms source stability.
- CurrentOwnerView.begin in runtime_host.py (1512-1523) gives the host-bound operation session.
- route_native_record in native_storage.py (107 onward) derives exact native routes; indexes nominate candidates and revalidate loaded identity.

GAME/TOOLS/hot_store.py:
- NativeHotStore.atomic_owner_mutation (154-161) stages OwnerDocuments atomically in SQLite.
- OwnerDocument.validate (40-43) checks basic envelope and native identity, not Activity/selector/cost/full semantic transition authority.
- read_admitted_snapshot (174-241) treats persisted/raw rows as absent unless this process's native establishment marks admit the exact fingerprint.
- _establish_actor_owner (322-388) is the private, snapshot-fenced native Actor continuity establishment path; it also records native predecessor evidence and single-use phase result.
- _stage (263-301) maintains generation/dirty state but does not itself issue those admission marks.
- clear_published_generation (243-261) clears only the exact acknowledged generation.

Therefore atomic_owner_mutation is reusable physical machinery, not a ready public spell-commit entitlement. A future native ExecutionSegment establishment needs the equivalent exact predecessor/snapshot fence, typed owner validation, idempotent consumption and atomic admission for its whole lawful owner set. Bypassing read_admitted_snapshot or marking arbitrary staged rows current would violate the current owner boundary.

Existing RuntimeHost.actor_continuity.establish_from_phase (1531-1888) is deliberately a trusted ACTOR/NPC private-state consumer. It rejects a LIVE-owned Actor at 1592-1594. Its accepted ACTOR phase must not be repurposed to authorize spell arithmetic, PC agency or native mechanical writes.

### 3.5 Temporal and persistence components

GAME/TOOLS/temporal.py:
- derive_temporal_dependency_keys (621-643) validates explicit native occurrence keys.
- materialize_due_occurrence (646-660) returns only a CANDIDATE; accepted execution owns later mutation.
- rebuild_temporal_agenda (663-683) consumes explicit roots.
- validate_temporal_route_completeness (730-766) requires owner-issued native enumeration under the same exact source.
- resolve_temporal_dependency_dependents (769-784) filters the explicit route by one dependency key. The present implementation traverses route.entries; a truly large due index needs physical key-index lookup under the same nonauthoritative semantics, not a fabricated constant-time claim.
- No GAME caller found executes a due candidate through the recipe/native mutation path.

GAME/TOOLS/durability.py:
- join_execution_durability (475-551) preserves accepted identity/fixed RNG/catalog/policy evidence in an owner-issued join without rerunning mechanics.
- Its carrier is necessary to execution-backed campaign publication but currently has the source-shape contradiction in section 5.

GAME/TOOLS/publication.py:
- _require_execution_join_for_route (126-131) requires the join for runtime.command.
- freeze_campaign_publication_attempt (643 onward) freezes exact currentness, native route, owner generations and coherent campaign delta; accepts typed joined execution and rejects independent substitutions.
- This is distinct from local execution establishment, with tri-state/non-force currentness laws.

GAME/TOOLS/runtime_host.py:
- RuntimeHost (2061 onward) binds one selected campaign and immutable context/Actor continuity/history/native ordering/publication/event services.
- _begin_operation (2178-2194) freshly pins campaign and rereads selected LIVE.
- CampaignPublicationService.publish_owner_delta (555-656) implements one existing bound publication route, with an unavailable execution join argument described in section 5.
- No composed execution/casting service exists in the current properties/slots. Candidate realization should extend the existing host operation route; do not add a spell role or sibling service.

GAME/TOOLS/live_state.py:
- lookup_write_authority (1876 onward), freeze_live_attempt (2220-2307), classify_cas_result (2417 onward), reconcile_indeterminate (2492 onward) and accepted absorption functions already provide exact-source native infrastructure.
- Source-native creation includes an explicit per-kind identifier policy/cursor and CAS; accepted IDs survive absorption.
- These paths do not establish recipe/owner consequences by themselves.

GAME/TOOLS/recovery.py:
- _validate_catalog_closure (1066-1101) uses an owner resolver to reconstruct compatible context/candidate and validate_execution_proposal; missing resolver evidence fails closed.
- Execution recovery reconstructs native segment/events/fixed inputs, not a warmed ExecutionStore or MechanicalContext authority.

GAME/TOOLS/turn_runtime.py:
- accept_execution_handoff (1095-1138) seals a recipient-scoped execution-result handoff and detects conflicts.
- _execution_handoff (1157-1193) currently projects command/fingerprint/owner/resolution/status/segment/event IDs. It does not carry per-target damage/healing/export details.
- Production narration of a complete spell requires a lawful compact outcome projection or bounded current owner context in addition to these identity references; no new role is implied.

## 4. Bounded negative evidence and test limits

Search domain: exact tree has 31 GAME/TOOLS files, all Python. Every file was fetched at the pinned SHA and inspected for concrete imports/call sites of bind_catalog_context, bind_executable_catalog, accept_command, validate_execution_proposal, execute_segment, resolve_mechanic, resume_accepted_execution, ExecutionStore, atomic_owner_mutation, stage_owner_document, _establish_actor_owner, join_execution_durability, op.select_targets/op.apply_damage/op.create_effect, Calculation/selector and compile/evaluation symbols.

Results:
- bind_catalog_context: definition only.
- accept_command: definition only; bind_executable_catalog called within that acceptance function.
- execute_segment: called only by mechanics.resolve_mechanic and resume_accepted_execution.
- ExecutionStore: definition/type use only inside mechanics.
- validate_execution_proposal: recovery catalog validation caller.
- atomic_owner_mutation: definition only.
- _establish_actor_owner: current trusted Actor continuity caller in RuntimeHost.
- join_execution_durability: definition only; publication consumes its typed carrier.
- No deterministic primitive/read/Calculation dispatcher or Activity compiler is implemented among the inspected shipped Python producers.

This establishes an absent composed Python caller in this bounded tree and the exact module insufficiencies. It does not prove that no instruction-driven gameplay can ever occur, that no external host adapter exists outside the tree, or that every previously closed execution task is defective. GAME CORE instructions and external deployment can prescribe steps without supplying the missing deterministic native implementation; such instructions are not proof of this requested production closure.

Inspected tests prove narrower boundaries:
- test_rd15_catalog_runtime exercises identity reconstruction, forged/changed source rejection, gaps and context currentness.
- test_rd05_runtime_execution supplies Activity identity/Resolution/event_payload directly. test_retry_reuses_fixed_rng_and_event_identity (549-586) supplies result=17; it proves draw deduplication and event identity, not the check arithmetic or a spell's owner mutations.
- test_s6d_07_character_mvp_seed imports DEV resolve_package and checks compile/admission/reference closure.
- validate_character_mvp_seed.resolve_package (167-299) uses DEV schemas, compiles finite step shapes and exact consumer roster; it does not execute those steps.
- validate_health_effects_recovery_seed is explicitly a conformance aid (line 1). apply_damage/apply_healing (119-181), apply_effect/expire_effect/support-tree functions and tests prove reference transitions/deduplication, not shipped persistence integration.
- test_rd04_native_routing_index_hot proves physical rollback/generation/routing; raw rows are explicitly snapshot absences (191 onward).
- test_rd06_durability_publication uses a flattened fabricated catalog_context at 61-90 and synthetic execution at 93-116.
- test_runtime_host_composition verifies currentness/transport/owner publication and immutable host boundaries; it does not cast a recipe into native state.

No tests/builds/gameplay were executed for this design investigation. Existing test names/assertions are evidence of their defined scope, not fresh PASS claims.

## 5. Established durability/publication contradictions and minimal candidate amendments

### PT-D1: exact accepted carrier versus flattened join check

Established source-shape contradiction:
- catalog_runtime.BoundCatalogContext.to_dict (61-69) emits:
  catalog_context = {basis: {catalog_generation: 2, ...}, definition_dependencies: [...], catalog_context_fingerprint_generation: 1, catalog_context_fingerprint: ...}.
- runtime_execution.accept_command (1200) stores exactly admitted_context.to_dict() as command.catalog_context.
- durability.join_execution_durability (516-521) sets catalog_basis=dict(command.catalog_context), then tests catalog_basis.get("catalog_generation") != 2.
- This valid current carrier has no top-level catalog_generation, so the expression returns None and selects the rejection branch.
- test_rd06_durability_publication._accepted_command (61-90) instead constructs catalog_context.catalog_generation at the top level. Its bounded fixture does not compose the real accept_command producer.

Static consequence, not exercised: a newly admitted command produced by the current accept_command cannot pass that generation check through the current join. This conclusion needs no absent-keyword inference; the producer and consumer literal shapes disagree.

Minimal candidate form, under the existing durability owner:
1. Preserve the complete current catalog_context serialized carrier unchanged as accepted historical basis.
2. Validate/access catalog_context.basis.catalog_generation and its ruleset lock/engine inventory under the actual current carrier contract, rather than inventing a flattening at the new cast boundary.
3. Retain the compatible selected context/dependency/fingerprint evidence required for recovery; do not reread current ambient mechanics to reinterpret accepted history.
4. Add one producer-to-join contract/integration fixture using actual bind_catalog_context -> accept_command -> execute/native segment -> route_serialized_operation -> join. Change synthetic fixture shape only after owner reconciliation.
5. If backward compatibility is required, make versioned accepted-carrier compatibility explicit under the native owner; do not accept arbitrary mixed flattened/nested objects.

Applicable to the future actual casting consumer and any newly composed real accepted-command publication. It does not auto-reopen earlier closed waves or presume that every historical bounded fixture promised this composition.

### PT-D2: composed host publication route versus mandatory join

Established capability/signature contradiction:
- publication._require_execution_join_for_route (126-131) rejects runtime.command with no ExecutionDurabilityJoin.
- freeze_campaign_publication_attempt (643-691) accepts and validates the owner-issued join, uses it as accepted-command/execution evidence, and rejects independent substitutions.
- runtime_host.CampaignPublicationService.publish_owner_delta (555-563) has no join parameter.
- Its call to freeze_campaign_publication_attempt (598-612) passes routed_operation but no execution_durability_join.
- Therefore selecting a runtime.command route through this existing host method deterministically reaches the required-join rejection before tree/commit/ref dispatch.
- test_rd06_durability_publication.test_runtime_command_route_rejects_missing_join_without_raw_execution_arguments (357-363) expressly fixes the lower-owner rejection law.

Static consequence, not exercised: the current composed method cannot publish a real execution-backed command route. A caller bypass to raw accepted_command/event JSON would violate the established join law.

Minimal candidate form, preserving existing host/publication owners and no new service:
1. Extend the existing bound publication operation with an optional owner-issued ExecutionDurabilityJoin or a sealed execution establishment result from which that same owner creates it.
2. Require it for runtime.command and bind it to the same selected campaign, operation basis, route, accepted identity, complete write set and owner generations.
3. Pass it through the existing freeze_campaign_publication_attempt argument; continue rejecting substitution with raw independently supplied execution.
4. Preserve native owner-only publication for non-command routes.
5. Cover actual producer -> join -> composed publication in a new consumer fixture; preserve one coherent tree/parent and force=false plus accepted/indeterminate/conflict behavior.

This is a composition obligation, not a request to weaken join validation or add another publication service.

### PT-P1: missing composition, separate classification

No producer/current carrier contradiction is required to establish that the current GAME tree lacks an Activity evaluator/native mechanical segment caller. This is qualified negative evidence, not PT-D1/PT-D2. NativeHotStore's raw staging is deliberately weaker than admitted current-state establishment; treating that deliberate limitation as an existing bug would be wrong. New casting requires a typed admitted native execution consumer.

## 6. Minimal candidate production realization

These are design contracts, not implementation or executable schema authority.

### 6.1 Admission/compile once, source-authenticated cache

Use existing package/registry owners. On exact immutable definition-set admission:
- authenticate manifest/member bytes, resolved-set and engine contract inventory with the existing identity chain;
- load exact primitive contracts/value contracts/selector-operation pairs/accessor/fact permissions;
- compile the finite Activity tree, typed exports, arguments, guards, bounded target iteration, registered choices/reactions and declared native transition variants;
- compile/index embedded Rule Elements by selector and triggers by registered event/signal;
- derive exact support-definition dependencies, read capabilities, effect-support and typed mutation owner dependencies; reject any unproven DAG/authority path;
- retain an immutable complete compiled object and small aliases/discovery index, with source-derived receipts of compilation.

Separate cache dimensions:
1. Definition compiled cache key: exact definition member/content identity + transitive definition/engine contract identities + compiler contract generation. A purely unrelated campaign frontier change need not recompile all 339 definitions.
2. Invocation binding key: current accepted resolved catalog context + compiled definition identity + actor/source/target/parameter bindings + accepted permitted fact fingerprint.
3. Calculation/MechanicalContext cache key: that context plus exact committed/prospective view, relevant native revisions and bound source/Effect/Resource roles.

A cache hit does not authorize a stale entity, ability or policy. New invocation binding freshly revalidates current source/current owner eligibility. Existing accepted identity is looked up BEFORE binding under ambient context (Step-3 191-207). Cold recovery reconstructs compatible accepted context and recompiles disposable objects; cache bytes are never accepted work authority.

Avoid calling today's full package-lock rebuild at every deterministic step or ordinary warm cast. An authenticated immutable admitted-definition handle may reuse already-proved immutable bytes; it must not trust caller-mutable PackageSnapshot fields or a caller-provided digest as proof. Preserve a source identity/discontinuity check and explicit cold/reload/incompatible failures.

Ordinary prompt needs bounded currently available candidate names, ambiguity choices and the selected admitted rule/receipt explanation, not 339 descriptions or a whole package object. The runtime still holds all rules/support content locally.

### 6.2 Bind and evaluate through existing owners

Within the existing host operation boundary:
1. Existing command/resume identity lookup; exact retry returns accepted outcome/current suspension.
2. Current operation pin/access and finite capability/target discovery; selected IDs revalidated against package identity and native owner truth.
3. Exact casting prerequisites, acquisition/selection entitlement, components, time, mode, resources and targets; unresolved legal choices suspend before their commitment point.
4. Build the accumulated bounded CurrentOwnerReadSession union for actor, source, explicit targets, relevant effects/resources, Procedure and named support definitions.
5. Construct immutable MechanicalContext/prospective overlay; invoke only registered local dispatch functions and typed selector resolvers; one scoped DAG/input permission proof.
6. Convert calculations into owner-specific typed prospective transitions; validate every native owner consequence and event/child identities.
7. Establish the lawful native segment at its authority edge; emit/store receipt and retain accepted inputs.
8. Continue deterministic clauses/mandatory children until completion, typed failure, currentness suspension or genuine external choice/adjudication. No model calls between steps.

Use the existing RuntimeHost composition root and native execution modules/ports. The operation may expose an owned method but should not add a spell service, actor-per-spell executor, gameplay role or state family.

### 6.3 Native local atomic establishment

Extend the infrastructure-only native segment port behind the existing host rather than exposing arbitrary OwnerDocuments:
- input: admitted accepted command/invocation identity, exact owner-read observation/predecessors, typed owner transition plans, planned segment/event/mandatory-child identities, fixed roll frontier, expected continuation generation, native owner generation transitions;
- validation: caller-issued seals/owner authority, exact campaign/source/write authority, all predecessor fingerprints/revisions, per-owner semantic schema/transition closure, no conflicting command/segment/continuation consumption;
- one SQLite transaction, where local establishment is allowed: all native owner after-images + Resolution/Command/Procedure + fixed RNG + Continuation consume/create + event batch/receipt + mandatory child identity + idempotency + generation/dirty/invalidation;
- atomic current admission for the whole accepted native edge, with the same predecessor discipline as _establish_actor_owner;
- output: owner-issued establishment result/receipt, sufficient publication/recovery closure and native revision refs.

This is a typed extension to the existing HOT execution capability, not a generic patch API. The input plans are ephemeral primitive-local candidates and never persisted as a competing StateDelta owner.

## 7. Candidate typed capability extensions beyond the seed

The six current spell definitions have only level/school/activity IDs and six finite recipes. Seed spellcasting is not full casting semantics. The table below states concrete bounded extension shapes to review against every corpus requirement; it does not claim all 339 rows are already semantically closed. Exact activation/consumer IDs, legal enum sets, source rules and tests must be supplied by the full corpus map.

| Candidate contract | Required closed typed input/output | Existing owner/capability route and limitation |
|---|---|---|
| Casting invocation/preflight | spell+activity ref; Actor/source casting binding; declared mode/slot level/ritual option; engine-derived caster level/ability/known-prepared-grant entitlement; finite target roles; typed component Asset refs; accepted fiction fact provenance; exact resource/time commitment IDs | Spell/Activity/Actor build/resource/Asset/Procedure owners. Current accept_command only validates identity/adjudication; it is not casting entitlement |
| Scaling and spell value calculation | bounded integer slot/caster-level bindings; declared finite tables/formulas using admitted value vocabulary; typed dice/count/duration/range/target-count/component results with provenance | Activity value/Calculation owners. No arbitrary formula/eval or LLM-chosen arithmetic; do not activate selectors merely by reference |
| Spell effect create/update/end | admitted Effect/Condition definition; target/source; declared parameters; duration basis; support parent; application/episode/reapplication policy; end reason; output episode/native ref + temporal binding + affected revisions | Widen exact op.create_effect and activate reviewed remove/update forms. Current create_effect is Innate Sorcery only; support/DAG/reapplication semantics remain owned |
| Concentration/support | one caster-bound concentration support episode; child Effect/summon support refs; declared replacement/end causes; damage-triggered save recipe; fixed damage/roll occurrence; authorized end outcome | Existing world.effect/support, Procedure/Step-3 trigger and temporal owners. Generic concentration remains conformance-only; no new Actor condition array or independent concentration ledger |
| Repeat saves/periodic/triggered consequences | registered binding + occurrence/event identity; owner-local next due binding/state; finite responder targets; accepted historical trigger view; child Resolution or pending descriptor; deterministic reschedule/end | Activate exact schedule/follow-up/reaction/choice consumers; owner-local Effect scheduled_trigger_state and existing Temporal routes, never global scheduler/job owner |
| Rule-element interactions | exact new selector/operation pair; typed result/combination law; legal source/predicate/binding/read permissions; accepted/rejected provenance and DAG edges | Existing S6D-03/04. Resistance/vulnerability, disadvantages, overrides, movement/action restrictions and special saves require closed pair contracts; current roster is 10 selectors/3 operations |
| Temporary HP and special health/life transitions | Actor role; fixed typed amount; replacement choice where rules require; admitted LifeStatePolicy-specific revive/restore/change-max cause and prerequisite evidence; coupled Effect changes | Activate exact set-temporary-HP and health/life variants. Generic healing of a dead Actor is not resurrection authority |
| Entity summon/create/retire | admitted local Actor archetype/support content; bounded multiplicity; source/target placement; duration/support/controller/agency policy; lawful native creation ref and source-native policy | Existing Actor/entity/identity/Effect owners; exact op.create_entity/retire_entity activation. No created generic creature mechanics from prose |
| Actor/Asset transformation | existing identity, from/to admitted definitions/form relation; typed rule-specific retained/replaced statistics, health/resource transition and reversion trigger; required supporting forms | Existing Actor/Asset owners and quarantined transform capability. Preserve stable semantic identity; archetype ID swap alone does not close Polymorph or other transformation rules |
| Zones/ongoing areas | admitted Zone definition; source/location anchor; strict area spec; declared enter/leave/boundary rules and finite candidate-membership proof; effect associations and cleanup | Existing world.zone/Effect/location owners; activate exact create/update/remove-zone consumers. No universal world query or full 3D simulation |
| Movement/teleport/planes | bound actor/asset; exact lawful origin/destination Location/plane route; admitted distance/placement rule; engine prerequisites; accepted fiction evidence for a named exceptional clause | Existing location/Actor/Asset and quarantined move/teleport variants. Native location differs from tactical micro-position; movement is not arbitrary state path |
| Material creation/transformation/cost | exact material/component Asset/quantity/currency binding; consumption or lawful directed transform/create edge; finite accepted output definition and placement; revision refs | Asset owner. Existing transform law requires declared from/to edges and migration; no arbitrary JSON patch or duplicated wealth authority |
| Illusion, divination, memory and open-ended consequences | named admitted mechanic/choice domain; exact targets/knowledge scope; frozen narrow adjudication value with stable provenance/currentness; lawful existing world/knowledge/Actor/access transition selected afterward | Existing truth/knowledge/disclosure/agency/canonical-promotion owners. LLM may adjudicate fiction; it cannot fabricate engine facts or use op.emit_fact as generic world mutation (current exact variant is Action Surge only) |
| Exceptional spell duplication/request | original admitted spell/mode ref; bounded copied level/eligibility rule; invocation ancestry/chain bound and exact consumer dependency; exceptional adjudication disposition where required | Existing Activity/command/Resolution and promotion/House-Rules owners. Wish-like authored effects require reviewed closed owner transition routes, not universal mutation authority |

Admission is per exact consumer and rule semantics, not per table row, marketing group or number of executors. Existing primitive names may cover much of the breadth after typed contracts are closed; a genuinely new transition semantic needs an owner-local registered variant and its own evidence. Do not activate all twenty quarantined operations, all dormant selectors or every conformance shape in bulk.

## 8. Currentness, partial completion and LIVE variants

Local:
- Read and evaluate against one exact current owner union and prospective view; no lazy cross-revision mixing.
- A failed prospective segment commits none of that candidate's world/evidence consequences.
- Already committed earlier clauses/segments survive later failure; receipt lists completed/skipped/failed/suspended clauses and all pending mandatory work.
- Precommit choice/reaction closes the SQLite boundary; resume is generation/offer/responder/option-bound and single-consume.
- Expected reaction child receipt legitimately changes the parent view; repin/rebuild from declared safe phase while preserving historical raw rolls and choices.
- Mandatory post-commit trigger identity co-commits with the causing event. Root command stays unsettled while mandatory work remains.
- Event/receipt/trace failure after accepted semantics cannot authorize reroll/reapply or fictional rollback.

LIVE:
- lookup_write_authority determines every target owner's current authority from selected claims; actor/source/targets can span campaign and different selected LIVE sources.
- A LIVE-claimed candidate remains prospective until exact-source CAS is accepted; local post-CAS adoption is a separate transaction.
- Same native source may pack its lawful owner/event/continuity edge coherently, preserving distinct semantic owners.
- Multiple LIVE/campaign sources do not become one transaction. Freeze/currentness/prerequisite composition and dependency-owned native order remain required.
- A successful native edge survives a later sibling rejection. Preserve accepted identities/rolls/receipts, repin the rejected edge and report partial completion/currentness pending work under the existing root.
- Application authorization is revalidated independently of native CAS. CLOSED_UNABSORBED is current truth with zero ordinary writers; source movement is not cancellation of accepted Step-3 work.
- Source-native creations use per-kind admitted policy/cursor in the same accepted LIVE edge, never campaign allocation as an ordinary extra serial round-trip.

Boundedness:
- A host target/step/chain limit must not silently truncate published spell semantics.
- Before commitment, provide typed execution-limit/currentness/adjudication outcome if the complete lawful target/owner closure cannot be established.
- Batching/continuation is legal only where the rules and native atomicity/order contract permit it; retain explicit remainder and completeness evidence. Do not divide a rules-coupled atomic segment to meet a speed target.
- Current seed maximum=16 for several areas is a seed bound, not universal full-SRD proof.

## 9. Necessary acceptance evidence for the new actual consumer

1. Package-byte identity -> compile closure -> discovery -> entitlement -> actual cast -> native read/Calculation -> native owner mutation -> event/receipt -> join -> composed publication -> cold recovery, using the same real carriers throughout.
2. Unsupported/dormant/unknown primitive/pair, undeclared argument/read/fact, cycle and transitive authority laundering fail before mutation.
3. Actual attack/save/damage/healing/temporary-HP/resource arithmetic and applicable condition/effect consequences; wrong caller-supplied result cannot substitute.
4. Multitarget shared rolls, duplicate target bindings, zero/missing/false distinctions, scaling and components/time commitment according to exact spell rules.
5. Native multi-owner rollback versus preserved earlier accepted segments; generation conflicts; raw cache/staged rows never become authority.
6. Lost ack/exact retry/resume/duplicate due occurrence do not redraw/reapply/reconsume; changed accepted input/generation produces conflict.
7. Atomic event/mandatory child identity and no accepted event -> lost-child crash window; parent recomputation after expected reaction.
8. Real current accepted command crosses PT-D1 and PT-D2 joins; recovery uses compatible historical basis.
9. Local, campaign HARD/SAVE, same-LIVE, cross-LIVE/campaign, indeterminate CAS/ref, post-CAS adoption failure and closed source cases.
10. Ordinary narration receives compact authorized outcomes and omits protected diagnostic/raw Context/Actor-private material.
11. Instrument supported target environment: cold/admission vs warm/new invocation vs resume vs due processing vs LIVE; physical model calls, serial model depth, prompt/receipt bytes/tokens, local compute, native reads/writes and retries. Measure end-to-end latency separately.
12. Reject whole-catalog prompt, per-turn full recompilation/package rehash, whole-campaign modifier scan, global Effect scan, dedicated spell LLM call or model call between deterministic steps.

Structural target: one local orchestration invocation until completion/typed stop on sufficient local path; zero dedicated spell model invocation; no whole-catalog prompt. This is not measured latency and not a claim that every cast needs one native commit/read/write across independent LIVE sources.

## 10. Explicit continuation

Parent should reconcile these candidate contracts against the exact 339-entry requirement/mode map, supporting stat blocks, catalog/admission owner evidence and adjacent information/chronology design. Keep PT-D1/PT-D2 source contradictions separate from PT-P1 bounded missing composition. Required production work stays deferred until accepted architecture, implementation decomposition and Senior plan GO. No automatic Wave reopen or P1A authorization follows this investigation.

VERSION_IMPACT: NONE for this evidence-only artifact. Future accepted source/schema/engine changes require their own owning Version/System Impact reconciliation.

## Appendix A. Exact pinned evidence links

All links address the pinned source, not the moving branch.

| Claim / seam | Exact source |
|---|---|
| PT-D1 producer carrier | [GAME/TOOLS/catalog_runtime.py:61-69](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/catalog_runtime.py#L61-L69) |
| PT-D1 producer assignment | [GAME/TOOLS/runtime_execution.py:1187-1204](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/runtime_execution.py#L1187-L1204) |
| PT-D1 consumer generation check | [GAME/TOOLS/durability.py:475-551](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/durability.py#L475-L551) |
| PT-D1 bounded fixture shape | [DEV/TESTS/test_rd06_durability_publication.py:61-138](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/TESTS/test_rd06_durability_publication.py#L61-L138) |
| PT-D2 lower-owner mandatory join | [GAME/TOOLS/publication.py:126-131](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/publication.py#L126-L131) |
| PT-D2 lower-owner join validation | [GAME/TOOLS/publication.py:643-691](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/publication.py#L643-L691) |
| PT-D2 composed route signature and call | [GAME/TOOLS/runtime_host.py:555-656](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/runtime_host.py#L555-L656) |
| PT-D2 negative fixture | [DEV/TESTS/test_rd06_durability_publication.py:346-367](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/TESTS/test_rd06_durability_publication.py#L346-L367) |
| Package admission and member bytes | [GAME/TOOLS/ruleset_package.py:238-264](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/ruleset_package.py#L238-L264) |
| Catalog source rebuild | [GAME/TOOLS/catalog_runtime.py:372-569](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/catalog_runtime.py#L372-L569) |
| Accepted command binder | [GAME/TOOLS/runtime_execution.py:1115-1204](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/runtime_execution.py#L1115-L1204) |
| In-memory segment evidence | [GAME/TOOLS/mechanics.py:175-425](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/mechanics.py#L175-L425) |
| HOT raw staging versus admission | [GAME/TOOLS/hot_store.py:148-241](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/hot_store.py#L148-L241) |
| HOT fenced Actor establishment | [GAME/TOOLS/hot_store.py:322-388](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/hot_store.py#L322-L388) |
| Accumulated current-owner read/currentness | [GAME/TOOLS/current_owner.py:192-331](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/current_owner.py#L192-L331) |
| Host composed services/currentness | [GAME/TOOLS/runtime_host.py:2061-2236](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/runtime_host.py#L2061-L2236) |
| Due candidate and route lookup | [GAME/TOOLS/temporal.py:621-784](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/temporal.py#L621-L784) |
| Accepted-context recovery validation | [GAME/TOOLS/recovery.py:1066-1101](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/recovery.py#L1066-L1101) |
| Role-safe execution handoff | [GAME/TOOLS/turn_runtime.py:1095-1193](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/turn_runtime.py#L1095-L1193) |
| Exact-source LIVE freeze | [GAME/TOOLS/live_state.py:2220-2307](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/GAME/TOOLS/live_state.py#L2220-L2307) |
| DEV seed shape compiler | [DEV/TOOLS/validate_character_mvp_seed.py:167-299](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/TOOLS/validate_character_mvp_seed.py#L167-L299) |
| DEV health conformance scope | [DEV/TOOLS/validate_health_effects_recovery_seed.py:1-181](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/TOOLS/validate_health_effects_recovery_seed.py#L1-L181) |
| Real mechanics fixture inputs | [DEV/TESTS/test_rd05_runtime_execution.py:453-586](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/TESTS/test_rd05_runtime_execution.py#L453-L586) |
| Step-3 idempotency lookup-before-rebind | [DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md:176-248](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md#L176-L248) |
| Step-3 atomic segment and obligation evidence | [DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md:281-429](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md#L281-L429) |
| WP-12 local versus LIVE atomicity | [DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md:100-185](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md#L100-L185) |
| WP-16 cross-source composition | [DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md:416-465](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/blob/05576261665280c3f424d791c19d8c4080343c6a/DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md#L416-L465) |

