# RD-12 — Collaboration / Multiplayer — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production implementation begins before independent Senior plan GO.

Goal: realize the accepted WP-17 agency-safe collaboration machine — bounded obligation lineage/generation, immutable accepted IntentClause semantics, completeness-protected PLAYER routing companion, pre-command hold/close/handoff and recipient-safe catch-up — without a global active player, generic queue, second world, second knowledge authority or global waiting barrier.

RD unit: `RD-12`
Direct readiness: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146`.
Composite slices: `R016.COLLAB,R018.COLLAB,R122.COLLABORATION_BRIDGE`.
Canonical owners: R2.5 collaboration/multiplayer; WP-17 async collaboration; WP-16 access/currentness; Step-3 Interaction/IntentPlan/IntentClause execution boundary; WP-11 route/identity; WP-13 campaign publication; WP-14 recovery; Multiplayer Model.
Dependencies/joins: RD-09 supplies principal/PLAYER/control/currentness; RD-10 role/recipient containment; RD-11 Context Runtime; RD-02 knowledge/disclosure; RD-08 chronology; RD-05 Step-3 execution evidence; RD-13 history/Story/Dramaturg consumer. Collaboration owns none of those domains.
Out of scope: world/mechanics/RNG/currentness/knowledge/disclosure/Story authority; native ordered Procedure/Continuation/Choice/Reaction responder state; global queue/scheduler/presence/heartbeat/frontier; collaboration-specific RuntimeCommand.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: WP-17 Laws 1–58+, R2.5, Step-3 accepted input graph, WP-11/13/14, exact readiness records.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- `runtime.collaboration_obligation` durable collection owner;
- existing embedded IntentClause machine contract only for WP-17 collaboration semantic payload/hold readiness;
- PLAYER routing companion only as completeness-protected route nomination;
- collaboration runtime coordinator.

EXPECTED CONSUMERS TO CHANGE:
- RD-05 Step-3 command acceptance consumes released original IntentClause;
- RD-09 authorization/currentness validates associations;
- RD-11 recipient/context projection consumes collaboration scope;
- RD-13 retained multiplayer Dramaturg consumes lawful collaboration horizon;
- RD-14 rejoin/bootstrap consumes frontier/catch-up.

ALLOWED INTERFACES / CONTRACTS TO CHANGE:
- Create `GAME/TOOLS/collaboration.py`;
- Create `GAME/SCHEMA/collaboration_obligation.schema.yaml`;
- Create `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json`;
- Create `DEV/SCHEMAS/collaboration-closed-basis.schema.json`;
- Create `DEV/SCHEMAS/collaboration-handoff.schema.json`;
- Create `DEV/SCHEMAS/collaboration-frontier.schema.json`;
- Create `DEV/SCHEMAS/catch-up-projection.schema.json`;
- Modify existing `DEV/SCHEMAS/intent-clause.schema.json`;
- Modify existing `GAME/SCHEMA/player.schema.yaml`;
- inspect-only `GAME/SCHEMA/live_scene.schema.yaml` unless another accepted owner plan explicitly changes it;
- create/modify `DEV/TESTS/test_rd12_collaboration.py`, project-map/audit projections.

PROTECTED INVARIANTS:
- coordination family is exactly `INDEPENDENT_IMMEDIATE | AGENCY_DEPENDENT_COLLECTIVE | RULE_OWNED_ORDERED`;
- durable obligation exists only for independently durable `AGENCY_DEPENDENT_COLLECTIVE`;
- stable `obligation_id` owns one bounded dependency lineage; `(obligation_id,generation)` is owner-local current generation identity;
- accepted human semantic input identity remains `(interaction_id,clause_id)` under existing Interaction/IntentPlan owner;
- collaboration-relevant IntentClause content is immutable while referenced;
- semantic class closed set: `OOC_COORDINATION | DIEGETIC_COMMUNICATION | ACTIONABLE_INTENT | CONTROL_SIGNAL`;
- held actionable unit remains `intent.pending` with no `command_id` until successful handoff;
- PLAYER companion is routing completeness only, never collaboration/agency authority;
- close freezes an order-independent input-set fingerprint;
- collaboration RESOLVED means collection handoff, not gameplay completion;
- no technical arrival/CAS/ID order establishes fictional chronology;
- absence never supplies voluntary agency;
- waiting is scope-local and follows positive material dependency only.

Version Impact: classify obligation/IntentClause/PLAYER/API changes at their task checkpoint. No compatibility shim for global-active-player or transcript-coordinator semantics.

## Task 1 — RED: coordination-family admission and native obligation debt

**Files**
- Create: `DEV/TESTS/test_rd12_collaboration.py`
- Inspect: `DEV/SCHEMAS/intent-clause.schema.json`, `runtime-intent-plan-state.schema.json`, `GAME/SCHEMA/player.schema.yaml`.

**Future interfaces**
```text
classify_coordination_dependency(evidence) -> CoordinationFamily
open_or_successor_obligation(request, current_basis) -> CollaborationMutation
associate_input(obligation, accepted_clause, authorization_basis) -> CollaborationMutation
close_collection(obligation, current_basis) -> ClosedCollectionBasis
handoff_closed_collection(obligation, closed_basis, owner_context) -> CollaborationHandoffResult
```

**RED groups**
- `CoordinationAdmissionTests`: co-presence/silence/possible interest cannot create durable obligation; RULE_OWNED_ORDERED remains native-owner path;
- `ObligationLineageTests`: no native obligation schema/runtime yet;
- `IntentClauseCollaborationTests`: current schema lacks WP-17 immutable semantic class/content fields;
- `PlayerRouteCompanionTests`: current PLAYER has no completeness-protected route refs.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.CoordinationAdmissionTests -v
python3 -m unittest DEV.TESTS.test_rd12_collaboration.ObligationLineageTests -v
```
Expected RED. Do not publish RED-only completion checkpoint.

## Task 2 — GREEN: native collaboration-obligation contract and lineage

**Files**
- Create: `GAME/SCHEMA/collaboration_obligation.schema.yaml`
- Create: `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json`
- Create: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Modify: `DEV/PROJECT_MAP.md`
- Modify: `DEV/TOOLS/audit_engine.py`

**Native route**
```text
runtime.collaboration_obligation
-> STATE/RUNTIME/COLLABORATION
-> direct known-ID route
-> no baseline collaboration index
```

**Core state**
```text
CollaborationObligation {
  obligation_id
  generation
  lifecycle: OPEN | CLOSED | RESOLVED | OBSOLETE
  purpose
  dependency_scope
  decision_opportunity_basis
  required_requirements[]
  optional_eligibility[]
  accepted_input_uses[]
  safe_frontier_refs[]
  execution_anchor_clause_ref? 
  closed_input_set_fingerprint?
  source/currentness basis required by owner laws
}
```
No copied transcript/full input body/context bundle/private context.

**Interfaces**
```text
classify_coordination_dependency(evidence) -> CoordinationFamily
open_or_successor_obligation(request, current_basis) -> CollaborationMutation
obsolete_generation(obligation, current_basis, reason) -> CollaborationMutation
```

**RED/GREEN cases**
- durable obligation only when all WP17-6 conditions hold;
- unrelated decision gets new obligation ID; material same-lineage change gets successor generation;
- generation-defining semantics immutable in place;
- lifecycle only OPEN->CLOSED->RESOLVED, OPEN/CLOSED->OBSOLETE; no reopen;
- no directory enumeration/index/scheduler required for known obligation;
- generation numeric order not chronology/global currentness.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.ObligationLineageTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

REFACTOR: lifecycle/lineage helpers remain collaboration-owner-specific; no generic workflow engine.

Coherent checkpoint: native obligation schemas/runtime core + tests/audit/project-map. No PLAYER/IntentClause half-change included yet.

## Task 3 — existing IntentClause collaboration payload and pre-command hold

**Files**
- Modify: `DEV/SCHEMAS/intent-clause.schema.json`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Inspect: `DEV/SCHEMAS/runtime-intent-plan-state.schema.json` (no duplicate owner/schema creation).

Add optional collaboration-relevant fields only when clause participates:
```text
collaboration_semantic_class:
  OOC_COORDINATION | DIEGETIC_COMMUNICATION | ACTIONABLE_INTENT | CONTROL_SIGNAL
normalized_semantics: bounded structured semantic payload
material_exact_text_refs?: array[MessageEvidenceRef]
```
Existing identity remains `(interaction_id from IntentPlan, clause_id)`. Existing `execution_state`/`command_id` carry hold/release mechanics.

**Cases**
- collaboration-relevant accepted payload immutable while referenced;
- one host message with independent executable and collective-dependent meaning yields distinct clauses;
- held ACTIONABLE_INTENT is `intent.pending` and has no `command_id`;
- collaboration cannot synthesize command/system Interaction/multi-Interaction command identity;
- explicit semantic execution anchor required for one collective command;
- same prose in later Interaction is new input identity;
- exact wording is retained only by Message evidence when materially required; normalized semantics remain content-sufficient after message compaction.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.IntentClauseCollaborationTests -v
```
Expected GREEN.

Coherent checkpoint: existing IntentClause schema extension + focused tests. Step-3 owner identity is preserved.

## Task 4 — completeness-protected PLAYER routing companion

**Files**
- Modify: `GAME/SCHEMA/player.schema.yaml`
- Modify: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Modify: `DEV/TOOLS/audit_engine.py`

Add conceptually:
```text
collaboration_route_refs:
  - obligation_id: string
    generation: integer
```
with invariants from WP17-28..31.

**Interfaces**
```text
required_route_holders(obligation) -> tuple[player_id, ...]
reconcile_player_route_companions(obligation_before, obligation_after, player_records) -> PlayerRouteDelta
recover_obligations_for_player(current_player) -> tuple[ObligationRef, ...]
```

**Cases**
- every required contributor PLAYER and every PLAYER owning held accepted input has exact route ref;
- optional merely eligible contributor has none unless explicit recovery contract requires it;
- create/successor/terminal route-ref changes publish with obligation in one campaign native-domain durability closure;
- nonterminal ref never points to unpublished generation;
- RESOLVED/OBSOLETE removes refs same closure;
- companion cannot close/satisfy/authorize/transfer control/prove underlying opportunity;
- exact current PLAYER with validated completeness may terminate ordinary lookup when no ref; mismatch is repair condition, not broad scan permission.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.PlayerRouteCompanionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```
Expected GREEN.

Coherent checkpoint: PLAYER companion + collaboration reconciliation + audit/tests. This is a real `EXISTING_MODIFY`, not INSPECT_ONLY.

## Task 5 — input association authorization, identity and idempotency

**Files**
- Modify: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Consume: RD-09 `resolve_principal/resolve_player/authorize_operation` and currentness interfaces.

**Interface**
```text
associate_input(
    obligation,
    interaction,
    intent_plan,
    clause,
    principal_player_control_basis,
    current_opportunity_basis,
) -> CollaborationMutation
```

Validate full WP17-32 chain. Store only `AcceptedInputUse` association refs.

**Cases**
- duplicate same `(interaction_id,clause_id)` same use is idempotent;
- same prose later Interaction is distinct input;
- stale/terminal generation cannot append/reopen/carry automatically to successor;
- current controller/authorization change forces re-evaluation and successor/obsolete semantics, never in-place authority rewrite;
- semantic class must satisfy requirement/purpose/scope/generation;
- optional input accepted only while OPEN and compatible;
- explicit PASS/READY/NO_FURTHER_INPUT satisfies only owner-admitted requirement; silence never does.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.InputAssociationTests -v
```
Expected GREEN.

Coherent checkpoint: association logic + RD-09 consumer adapter + focused tests.

## Task 6 — scope-local waiting, maximal safe frontier and the three modes

**Files**
- Modify: `GAME/TOOLS/collaboration.py`
- Create: `DEV/SCHEMAS/collaboration-frontier.schema.json`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`

**Interfaces**
```text
resolve_waiting(obligation, current_basis) -> PROGRESS | WAIT_SCOPE_LOCAL | OBSOLETE
compute_maximal_safe_frontier(dependency, native_owner_evidence) -> CollaborationFrontier
```

**Cases**
- `INDEPENDENT_IMMEDIATE` progresses now and creates no durable obligation;
- `RULE_OWNED_ORDERED` routes to native Procedure/Continuation/Choice/Reaction owner, no mirrored responder queue;
- `AGENCY_DEPENDENT_COLLECTIVE` waits only after independent consequences/safe prefix persist/expose;
- unrelated scene/process continues;
- absence/disconnect/timeout/presence/heartbeat/message age cannot supply voluntary agency or close generation;
- automatic owner-proven consequence can progress despite absence;
- OOC coordination, diegetic communication and actionable intent remain semantically distinct; CONTROL_SIGNAL is explicit control input, not gameplay truth;
- technical arrival/CAS/ID order never chooses fictional order; unresolved material order stays behind safe frontier.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.ScopeLocalProgressTests -v
```
Expected GREEN.

Coherent checkpoint: waiting/frontier logic + schema + tests.

## Task 7 — explicit close, order-independent fingerprint and handoff transaction

**Files**
- Create: `DEV/SCHEMAS/collaboration-closed-basis.schema.json`
- Create: `DEV/SCHEMAS/collaboration-handoff.schema.json`
- Modify: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Consume: RD-05 Step-3 command path, RD-04 HOT/native transaction, RD-13 history only where handoff consequence is material history.

**Interfaces**
```text
close_collection(obligation, current_basis) -> ClosedCollectionBasis
handoff_closed_collection(obligation, closed_basis, owner_context) -> CollaborationHandoffResult
```

`ClosedCollectionBasis = (obligation_id,generation,closed_input_set_fingerprint)` with deterministic canonical set encoding independent of physical list/order.

Handoff disposition exactly:
```text
RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT
HAND_TO_EXISTING_NATIVE_OWNER
CLARIFICATION_OR_UNSUPPORTED
```

Campaign native-domain handoff closure includes:
```text
closed basis
+ affected IntentPlan clause readiness/disposition
+ obligation RESOLVED
+ affected PLAYER route-ref removals
```
If any required element cannot be established, obligation remains CLOSED and no dependent RuntimeCommand is accepted.

**Cases**
- close requires required-set satisfaction/current opportunity/no ordered-owner takeover/resolved material chronology ambiguity;
- physical input order does not change fingerprint;
- release transitions original clause pending->ready; only then Step-3 may allocate command;
- RESOLVED does not wait for command/Procedure completion and never mirrors it;
- material downstream execution preserves obligation/generation/fingerprint/relevant input refs;
- stale collaboration metadata never reruns accepted mechanics/fixed RNG/Continuation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.CloseHandoffTests -v
```
Expected GREEN.

Coherent checkpoint: close/handoff contracts + runtime wiring + PLAYER/IntentPlan transaction proof + tests.

## Task 8 — concurrent publication and recovery

**Files**
- Modify: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Consume: RD-06 campaign publication, RD-07 recovery, RD-09 currentness.

**Cases**
- same-generation OPEN independently valid associations form identity-keyed semantic set; current-ref conflict may refresh/revalidate and union/reapply deterministically;
- generation/lifecycle/purpose/current opportunity change blocks stale carry-forward;
- CLOSED accepts no new association;
- recovery starts from current PLAYER route companion -> direct known obligation -> current underlying opportunity/authorization/input refs;
- no broad scan, no stale session/cache authority;
- CLOSED handoff retry uses frozen fingerprint and accepted IDs, never recomputes human agency or replay order.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.PublicationRecoveryTests -v
```
Expected GREEN.

Coherent checkpoint: publication/recovery consumer adapters + tests; no new publication/currentness authority.

## Task 9 — join/rejoin frontier and recipient-safe catch-up

**Files**
- Create: `DEV/SCHEMAS/catch-up-projection.schema.json`
- Modify: `GAME/TOOLS/collaboration.py`
- Modify: `DEV/TESTS/test_rd12_collaboration.py`
- Consume RD-09 currentness, RD-02 disclosure/knowledge, RD-11 context and RD-13 eligible history/Story hints.

**Interfaces**
```text
build_join_frontier(player, current_routes, eligible_owner_evidence) -> CollaborationFrontier
build_catch_up(player, frontier, eligible_history) -> CatchUpProjection
```

Before new mutable input: current trusted principal -> current PLAYER/control -> exact obligation refs/current native route -> recipient-safe catch-up.

Catch-up is disposable recipient projection; it cannot replay as SemanticEvent/world mutation/knowledge grant or expose another player's private accepted input/context.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.JoinRejoinCatchUpTests -v
```
Expected GREEN.

Coherent checkpoint: catch-up contract/runtime/tests.

## Task 10 — `R016.COLLAB` / `R018.COLLAB` / `R122.COLLABORATION_BRIDGE`

**Files**
- Modify focused integration tests only unless Tasks 2–9 lack the exact adapter.

`R016.COLLAB`: native durable family/root realization uses obligation schema + WP-11 route + PLAYER routing companion.
`R018.COLLAB`: owner-valid route/body/load/HOT integration joins RD-04 without transferring collaboration semantics.
`R122.COLLABORATION_BRIDGE`: bridge exists only for concrete positive material dependency and supplies smallest scope/dependency evidence consumed by RD-08 chronology, RD-09 currentness and RD-11 context. It creates no universal active-scene set/frontier/barrier.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.CompositeBridgeTests -v
```
Expected GREEN.

Coherent checkpoint: integration proof only.

## Task 11 — retained multiplayer Dramaturg consumer join

RD-13 owns exact retained horizon representation. RD-12 supplies lawful collaboration generation/input/handoff evidence only after recipient/access/currentness checks. Tests must prove private input isolation and that collaboration state never becomes Story/ACL/history authority.

No RD-12 file action creates Dramaturg storage.

## Task 12 — RD-12 verification / Version Impact

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for currently active deterministic/scenario obligations.

Negative stale proof searches for global active player/current speaker, implicit active-user fallback, collaboration index/registry/queue/scheduler, global waits/frontier, co-presence-as-dependency, transcript-as-input identity, mutable old-generation semantics, command-before-handoff, technical-order chronology, catch-up authority and collaboration-owned canon/knowledge/history.

Version Impact Gate: reconcile obligation/IntentClause/PLAYER/catch-up schema/API/checkpoint impacts. System Impact Gate stops on any new global collaboration authority, new semantic input owner, distributed campaign+LIVE transaction, synthetic command owner or changed human-agency semantics.

Currentness fence: fresh-read WP-17, R2.5, WP-16, Step-3, RD-02/RD-04/RD-05/RD-06/RD-07/RD-09/RD-10/RD-11/RD-13 and exact touched files. Semantic owner/decomposition drift stops execution.

Final coherent checkpoint: all native obligation/IntentClause/PLAYER/handoff/catch-up tasks green, cross-owner joins proven, audit/full DEV tests green and remote read-back recorded. RD-12 closes only its direct leaves and listed slices; parent/composite/pure-proof closure remains package proof-ledger work.