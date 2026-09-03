# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC + SENIOR REPAIR APPLIED — READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-03

Target branch: `v1/engine-rearchitecture`

Task-specific open-world Source Manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief-critic.md`

Post-critic Senior recovery:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-process-source-graph-omissions.md` (`SR15-01..SR15-02`)
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-thread-visibility-knowledge-disclosure.md` (`SR15-03`)

---

## 1. Mission

WP-15 realizes the already-accepted HDM temporal-owner / process-continuity / chronology architecture against the current runtime, schema and regression surfaces.

It is **not** a greenfield choice of scheduler, game clock, event loop or timeline database.

Accepted architecture already fixes the controlling split:

```text
NATIVE TEMPORAL OWNER
    owns obligation existence, current occurrence generation/lifecycle,
    arming/settlement and TemporalBinding

TEMPORAL AGENDA
    derived bounded candidate/recheck routing only

CHRONOLOGY
    accepted sparse typed cause/order/metric/bridge evidence

STEP-3 EXECUTION
    accepted consequence execution, Procedure/Resolution/Continuation,
    fixed RNG and idempotency
```

WP-15 Step 1 establishes the evidence perimeter and framing required to audit/machine-realize that architecture. It does not perform Step-2 extraction, choose final schemas/APIs, edit implementation or begin planning.

---

## 2. Current authority / upstream closure

WP-15 consumes without reopening by overlap alone:

- Step-3 deterministic execution boundary and accepted execution continuity;
- Step-4 truth/knowledge/role-context separation where process visibility touches fictional knowledge;
- Step-5.1 domain-typed frontier model;
- Step-5.2 Resumable Runtime Closure;
- Step-5.3 temporal/pending continuity and native temporal ownership;
- Step-5.9 chronology persistence/reconciliation;
- the Step-5.3/5.9 Temporal Agenda/chronology integration amendment;
- the owner-approved forward-extensible temporal capability boundary;
- Step-5.8 live currentness/CAS/absorption semantics;
- Step-5.12 PLAYER-delivery/disclosure evidence boundary where process visibility touches human delivery;
- Step-5.13 chronology/temporal retention and cleanup constraints;
- Step-5.14 integrated recovery/concurrency review;
- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` concrete effect/resource/LifeState/Procedure/rest temporal-owner map;
- closed WP-07 truth/knowledge/disclosure/message-evidence audit constraints;
- closed WP-11 physical routing/indexing;
- closed WP-12 HOT/SQLite/transaction realization;
- closed WP-13 durability/SAVE/publication realization;
- closed WP-14 recovery/checkpoint/session/repair realization.

Reopening threshold:

```text
REAL CONTRADICTION
OR NEW UNSATISFIED CONSUMER
OR MATERIAL UPSTREAM INSUFFICIENCY
```

Stale CORE prose, stale schemas/tests, convenient global-clock designs or implementation difficulty are not sufficient.

---

## 3. Non-negotiable authority separations

### 3.1 Native temporal owner versus Agenda

Every admitted temporal obligation remains with its native owner.

Agenda/candidate structures may:

- enroll bounded recheck dependencies;
- nominate owners whose predicates may need reevaluation;
- rebuild after restart/source movement;
- support bounded local execution cost.

Agenda/candidate structures may **not**:

- own an obligation;
- decide durable DUE truth independently of native owner + chronology evidence;
- become a generic job/firing queue;
- execute consequences;
- advance fictional time;
- invent boundary occurrences;
- use traversal/priority order as fictional order.

### 3.2 Chronology evidence versus temporal owner

Chronology owns accepted typed temporal relations/evidence, not obligations.

It may provide:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
POSITION(provider_scope, C, EXACT|BOUNDED|UNKNOWN)
```

The native owner still evaluates its own predicate as `NOT_DUE | DUE | INDETERMINATE`.

No universal durable `due=true` flag is introduced.

### 3.3 Accepted execution versus temporal rematerialization

Once an admitted occurrence crosses into accepted Step-3 execution, recovery/retry/source movement must resume that accepted execution identity rather than materialize the occurrence again.

Preserve as applicable:

- RuntimeCommand/Procedure/Resolution/Continuation identity;
- occurrence/firing identity;
- fixed accepted RNG;
- accepted invocation/catalog/rules facts;
- pending child identity;
- already committed ExecutionSegments/receipts.

A temporal candidate reevaluation is not permission to replay mechanics or reroll.

### 3.4 Fictional chronology versus technical order

The following are never fictional chronology merely by existing or increasing:

| Technical marker/order | Allowed semantic domain | Forbidden chronology inference |
|---|---|---|
| Git commit/ref/ancestry order | publication/provenance/currentness as defined by owner | earlier/later fiction, elapsed time, simultaneity |
| campaign/live HEAD/revision/CAS winner | current source/fencing | first fictional action, due status |
| SQLite row/insertion/transaction/timestamp | local machine state | fictional order/time |
| path/index/list order | routing/derivative discovery | temporal order/eligibility |
| host process/session/chat/message order | interaction/operational sequence | in-world time/process advancement |
| wall-clock elapsed time | host observation where explicitly allowed | automatic fictional advancement or DUE |
| SemanticEvent ID/allocation order | identity/routing | fictional chronology by magnitude |
| Agenda priority/traversal order | derived reevaluation mechanics | fictional order |
| durability/frontier/timer language | durability/risk control only | current world clock/chronology frontier |
| retention/GC age | cleanup eligibility after owner predicates | fictional age/order or universal temporal cutoff |

Only admitted semantic chronology evidence can establish a chronology relation.

### 3.5 Thread visibility versus truth / knowledge / PLAYER delivery — SR15-03

`GAME/SCHEMA/thread.schema.yaml` contains `visibility.known_by_pc_ids` and `visibility.public`. Their physical presence beside durable process state does not grant them independent information authority.

The controlling split remains:

```text
objective truth / current world owner
    != world.knowledge fictional subject stance
    != runtime.disclosure PLAYER-delivery evidence
    != runtime.message accepted communication evidence
    != thread visibility machine field/projection
```

Therefore:

- `world.thread` must not become a second durable PC-knowledge owner;
- PC knowledge and PLAYER delivery remain distinct responsibilities;
- `runtime.disclosure` remains delivery evidence, not fictional knowledge;
- `public`, file/record readability or record existence alone do not establish PC knowledge, PLAYER delivery or information eligibility;
- Step 1 does **not** select whether either `thread.visibility.*` field is retained, derived, cached, a bounded hint/projection, denormalized, retired or otherwise constrained. Step 2 must establish that disposition from evidence if later authorized.

---

## 4. Accepted chronology model to preserve

WP-15 inherits:

> **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**

Required properties:

1. accepted anchors are stable semantic identities, not order by ID/path/revision;
2. causal ancestry, domain-typed precedence and metric coordinate order remain distinct;
3. unknown/incomparable order is not simultaneity or corruption;
4. no mandatory mutable campaign-global `now` exists;
5. metric contexts are rulers; native providers own current position evidence;
6. exact/bounded evidence preserves uncertainty rather than inventing a scalar;
7. cross-scope chronology is materialized sparsely only for concrete dependencies;
8. late relation evidence extends accepted history without rewriting old event identity;
9. current local extension may use `ActiveExtensionFrontier(S)`, which may contain multiple anchors and remains derivative evidence;
10. independent activity should be decomposed into actual scene/process/procedure scopes instead of a giant vector/global frontier;
11. live revision/CAS/close/absorption remains distinct from fictional chronology;
12. protected consumers retain bounded evidence routes; arbitrary historical temporal analytics are not guaranteed forever;
13. chronology contradiction is domain-typed; legitimate INDETERMINATE/incomparability is not corruption.

---

## 5. Temporal capability boundary

Baseline accepted history is forward-extensible and acyclic in causal ancestry.

Supported, when owner/evidence contracts can represent them:

- deadlines/countdowns;
- independent/split-scene progression;
- differing temporal rates/planes;
- forward jumps/stasis;
- bounded/exact elapsed evidence;
- historical mysteries/newly established old relations;
- immutable-history time travel whose causal ancestry remains forward-extensible.

Not baseline-supported as ordinary semantics:

- rewriting already accepted past;
- multiple simultaneously authoritative branching timelines/worldlines;
- routine retrocausal mutation/causal loops;
- arbitrary timeline replacement/merge.

WP-15 must not fake unsupported behavior through Git history rewriting, hidden worldline IDs, chronology contradiction repair or a global scheduler.

The accepted Dramaturg carry-forward guard remains a downstream WP-18 obligation; it does not grant WP-15 or the LLM a new chronology owner.

---

## 6. Concrete native temporal-owner families

Step 2 must map at least the following admitted families from owner law to current machine representation and accepted consequence path:

| Concern | Native owner / primary state |
|---|---|
| Effect intrinsic expiration | `world.effect` + `temporal_binding` |
| Effect scheduled trigger next occurrence | `world.effect.scheduled_trigger_state[trigger_key]` |
| Actor/asset resource recovery | owner ResourceState / `recovery_binding` |
| Stable LifeState recovery | `world.actor.life_state_progress` / recovery binding |
| Procedure-local boundary/resource recovery | `runtime.procedure` |
| Rest progress/completion | RestPolicy + owning rest Procedure/process |
| Event/signal followup | source binding plus causal Step-3 execution; transient Signal/BoundaryOccurrence values do not become lifecycle owners |
| Choice/Reaction suspension | `runtime.continuation` |
| Generated accepted RNG | Resolution/Continuation accepted execution evidence |

Step 2 must add a discovered real family rather than force it into a generic scheduler owner.

Critically, the presence of a `world.thread` / process record does **not** establish that `world.thread` owns every deadline, clock, advancement predicate or other temporal obligation represented near it. Step 2 must identify the real native owner for each process/clock/deadline and then map any relationship to `TemporalBinding`, chronology, Step-3 execution and derived Agenda.

---

## 7. Processes / off-screen change

A process, clock, countdown or off-screen consequence must be modeled through its actual native owner state/stage/binding and accepted semantic transitions.

Permitted representations may include:

- owner stage/state;
- TemporalBinding;
- explicit accepted boundary occurrence;
- causal/event dependency;
- owner-defined metric position/evidence;
- sparse chronology bridge when a cross-scope dependency becomes material.

Not permitted as baseline authority:

- daemon/background fictional execution tied to host uptime;
- wall-clock catch-up on restart;
- generic scheduled-job records merely because something happens later;
- advancing all world processes whenever the user sends a message;
- moving a threat/clock because pacing wants drama;
- reconstructing process advancement from commit count or elapsed real time.

A future autonomous/background progression product would require a separate architecture decision; Step 5.3 explicitly did not create it.

### 7.1 Shipped process runtime and durable representation — mandatory Step-2 route

Senior recovery `SR15-01` adds these mandatory current machine inputs:

- `GAME/CORE/PROCESSES.md` — shipped process/threat/clock runtime contract;
- `GAME/SCHEMA/thread.schema.yaml` — current durable `world.thread`-shaped process representation.

Step 2 must reverse-audit, field/behavior by field/behavior:

- process kinds: threat, goal, project, countdown, investigation, pursuit and custom;
- process status, owner association, objective and affected entities;
- stage/progress/next-development semantics;
- advancement conditions and causal trigger requirements;
- deadlines and resources;
- segmented clocks and predefined meaning/completion semantics;
- off-screen advancement and simulation-budget rules;
- prohibition on continuously simulating dormant entities;
- multiplayer prevention of advancing the same causal stage/elapsed interval twice;
- `created_event_id` / `last_event_id` dependency semantics;
- visibility (`known_by_pc_ids`, `public`) and information-eligibility interaction;
- recovery/currentness/rebuild behavior;
- publication/durability closure;
- retention/GC/protected-consumer implications.

For each represented process/clock/deadline, Step 2 must establish one actual native owner and an explicit relation to any temporal/chronology/execution/Agenda machinery. `PROCESSES.md` and `thread.schema.yaml` are machine evidence; neither is promoted to universal temporal authority by this repair.

### 7.2 Direct temporal/process CORE consumers — scoped only

Senior recovery `SR15-02` adds these direct current consumers:

- `GAME/CORE/ADVANCEMENT.md` — rest/downtime/long projects and in-world time/resource cost;
- `GAME/CORE/EXPLORATION.md` — elapsed/travel time and causally driven off-screen processes;
- `GAME/CORE/COMBAT.md` — Procedure-local initiative/round/turn/active-participant/local-time ownership;
- `GAME/CORE/ENCOUNTERS.md` — time pressure and active-process consequences.

Step 2 inspects only their temporal/process statements. It must not reopen unrelated advancement, exploration, combat or encounter semantics.

### 7.3 Thread visibility knowledge/disclosure route — mandatory Step-2 evidence

Senior recovery `SR15-03` adds these mandatory owner/consumer inputs:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`;
- `GAME/CORE/INFORMATION.md`;
- current `world.knowledge` / `runtime.disclosure` machine contracts discovered through the owner graph, currently including `DEV/CATALOG/entity-structures.json` and `DEV/CATALOG/identifier-policies.json`;
- applicable closed WP-07 truth/knowledge/disclosure/message-evidence artifacts as upstream constraints.

Step 2 must explicitly disposition `thread.visibility.known_by_pc_ids` and `thread.visibility.public` against those owners and current machine evidence.

The disposition question is deliberately open at Step 1. Later evidence may establish retained/derived/cache/hint/denormalized/retired or another owner-compatible machine role. Step 1 must not decide it by convenience.

The Source Manifest remains open-world: Step 2 must discover any additional current `world.knowledge` / `runtime.disclosure` realization, routing, storage, normalization, recovery, publication, retention or test surfaces actually reached by the owner graph.

---

## 8. Position-provider / due semantics

For metric temporal predicates, Step 2 must preserve owner-specific deterministic provider routing.

Conceptually:

```text
ResolveTemporalPosition(owner, binding, current ownership basis)
    -> POSITION(provider_scope_ref, context_id, EXACT(v))
     | POSITION(provider_scope_ref, context_id, BOUNDED(lo,hi))
     | INDETERMINATE_NO_COMPATIBLE_PROVIDER
     | INTEGRITY_CONFLICT
```

Movement must follow one owner-defined mode:

```text
FOLLOW CURRENT SCOPE
PRESERVE SOURCE PROVIDER
SAFE REBASE
```

Unknown/incompatible position yields `INDETERMINATE`, never guessed world time.

For a scalar deadline D:

```text
EXACT(x):
    x < D  -> NOT_DUE
    x >= D -> DUE

BOUNDED(lo,hi):
    hi < D -> NOT_DUE
    lo >= D -> DUE
    otherwise -> INDETERMINATE
```

No generic durable DUE flag is required.

---

## 9. Current machine debt that Step 2 must reverse-audit

Existing machine material is evidence, not accepted architecture by inertia.

### 9.1 CORE chronology/runtime/live/process/information prose

Mandatory targets:

- `GAME/CORE/CHRONOLOGY.md`:
  - useful partial-order/adaptive/bounded rules;
  - stale singleton `chronology_frontier_event_id` semantics;
  - stale `CURRENT.world_time.frontier` global-reconciliation semantics;
  - “derive minimum compatible ordering” must not authorize arbitrary totalization when evidence remains insufficient.
- `GAME/CORE/RUNTIME.md`:
  - OOC and maintenance do not advance fiction;
  - world changes require causes;
  - stale durability-timer/frontier wording must remain durability-only and cannot imply fictional time.
- `GAME/CORE/PROCESSES.md`:
  - threats/goals/projects/countdowns/investigations/pursuits;
  - stage/progress/advancement conditions/deadlines/resources;
  - clocks and off-screen advancement;
  - causal advancement and simulation budget;
  - multiplayer duplicate-advancement prevention;
  - event dependencies and visibility;
  - no assumption that process abstraction itself owns all temporal obligations.
- `GAME/CORE/INFORMATION.md`:
  - only truth/knowledge/player-information statements needed to disposition thread visibility;
  - record/public readability cannot create PC knowledge, PLAYER delivery or eligibility;
  - unrelated information-domain mechanics are not reopened.
- `GAME/CORE/ADVANCEMENT.md` — only rest/downtime/long-project temporal/process statements.
- `GAME/CORE/EXPLORATION.md` — only elapsed/travel-time and off-screen-process statements.
- `GAME/CORE/COMBAT.md` — only Procedure-local initiative/round/turn/local-time ownership and elapsed-time consequences.
- `GAME/CORE/ENCOUNTERS.md` — only time-pressure/process-consequence statements.
- `GAME/CORE/MULTIPLAYER.md`:
  - Git/commit winner does not win simultaneous fiction;
  - local/global chronology-frontier wording requires Step-5.9 reconciliation.
- `GAME/CORE/LIVE_SCENE.md`:
  - live HEAD/revision/frontier is source-currentness/CAS;
  - close/rollover/absorption and technical synchronization delay do not advance fiction;
  - local/observable time requires typed disposition.
- `GAME/CORE/RANDOMNESS.md`:
  - accepted RNG cannot reroll just because a temporal candidate/retry is reevaluated.
- `GAME/CORE/INTEGRITY.md`:
  - targeted chronology contradiction handling must distinguish stale/incomplete/INDETERMINATE from corruption.
- `GAME/CORE/STORAGE.md`:
  - storage/durable frontier and timestamps remain technical and cannot leak into fictional chronology.

### 9.2 GAME chronology/current/live/process fields

Step 2 must field/behavior-map at least:

```text
GAME/SCHEMA/current_state.schema.yaml
    world_time.frontier
    world_time.display

GAME/CAMPAIGN/STATE/CURRENT.yaml
    scaffold world_time fields

GAME/SCHEMA/event.schema.yaml
    caused_by_event_ids
    after_event_ids
    world_order.scene_id
    world_order.sequence
    world_order.time

GAME/SCHEMA/scene.schema.yaml
    local_time
    chronology_frontier_event_id
    last_event_id
    live_epoch / last_absorbed_live_head_sha interactions

GAME/SCHEMA/live_scene.schema.yaml
    revision
    local_time
    observable_events[].live_event_id
    observable_events[].world_time
    status/base/currentness fields

GAME/SCHEMA/thread.schema.yaml
    id / status / kind / owner_entity_id / objective
    state.stage / state.progress / state.next_development
    state.advancement_conditions / state.deadline / state.resources
    affected_entity_ids
    visibility.known_by_pc_ids / visibility.public
    created_event_id / last_event_id
```

Required inherited dispositions include:

- retire `CURRENT.world_time.frontier` as generic global chronology frontier/authority;
- `world_time.display` is presentation only absent another typed owner contract;
- scene singleton `chronology_frontier_event_id` is superseded semantically by multi-anchor-capable `ActiveExtensionFrontier(S)`; singleton remains only a possible physical optimization when semantically valid;
- `world_order.sequence` is not a campaign-global fictional counter;
- `after_event_ids` may encode a clearly owner-defined local order domain, not untyped universal precedence;
- `caused_by_event_ids` is causal ancestry, not calendar order;
- live revision/HEAD/currentness fields are not chronology;
- `thread` process fields are durable machine representation only to the authority actually assigned by owning architecture; deadline/clock/event fields do not automatically grant `world.thread` temporal or chronology ownership;
- `thread.visibility.known_by_pc_ids` and `thread.visibility.public` must be separately dispositioned against Step-4/Step-5.12/WP-07/current machine evidence; neither has automatic PC-knowledge, PLAYER-delivery or eligibility authority.

### 9.3 DEV temporal/process/execution contracts

Mandatory inspection includes:

- `DEV/SCHEMAS/temporal-binding.schema.json`;
- `DEV/SCHEMAS/duration-spec.schema.json`;
- `DEV/SCHEMAS/boundary-occurrence.schema.json`;
- `DEV/SCHEMAS/world-effect-state.schema.json`;
- `DEV/SCHEMAS/world-actor-state.schema.json`;
- `DEV/SCHEMAS/resource-definition-data.schema.json`;
- `DEV/SCHEMAS/rest-policy-definition-data.schema.json`;
- `DEV/SCHEMAS/trigger-binding.schema.json`;
- `DEV/SCHEMAS/signal.schema.json`;
- `DEV/SCHEMAS/runtime-command-state.schema.json`;
- `DEV/SCHEMAS/runtime-procedure-state.schema.json`;
- `DEV/SCHEMAS/runtime-resolution-state.schema.json`;
- `DEV/SCHEMAS/runtime-continuation-state.schema.json`;
- `DEV/SCHEMAS/execution-segment.schema.json`;
- `DEV/SCHEMAS/procedure-state-changed-event.schema.json`.

Known debt requiring explicit Step-2 disposition includes current Continuation `future_rng_frontier`: Step 5.3 rejects a generic future PRNG frontier absent a real reserve-before-generation mechanic. `unconsumed_advancement` must remain accepted execution/Continuation evidence with an exact typed context if retained; it cannot become wall-clock/global-time catch-up.

### 9.4 Current knowledge/disclosure machine contracts — SR15-03

Mandatory current machine evidence includes:

- `DEV/CATALOG/entity-structures.json` — `world.knowledge` current field contract;
- `DEV/CATALOG/identifier-policies.json` — composite identity for `world.knowledge=(knower_id,fact_id)` and `runtime.disclosure=(player_id,fact_id)`.

Step 2 must discover any additional actual current realization/routing/storage/schema/test surfaces for these owners. Catalog admission/identity is not proof of a dedicated durable physical GAME path, and a missing path is not permission to invent one in Step 1.

### 9.5 Regression debt

`DEV/TESTS/CHRONOLOGY_CASES.md` is mandatory evidence.

- cases preserving independent scenes, Git-order non-authority, contested simultaneity, contradiction handling and boundedness are useful;
- current C12/C13 preserve stale singleton/global frontier expectations and require later repair under final WP-15 architecture.

Step 2 must search the repository for additional direct tests/consumers rather than treating this as a closed list. Senior repair additionally requires open-world discovery of process/domain/information consumers and representations reached from `PROCESSES.md`, `world.thread`, process fields, clocks/deadlines, rest/downtime/travel/combat/encounter statements, `thread.visibility.*`, `world.knowledge`, `runtime.disclosure` and their recovery/publication/retention dependencies.

---

## 10. In-scope architecture questions for later Steps 2–8

If later authorized, WP-15 must answer at implementation-facing precision:

1. What are all current admitted native temporal owner families and exact lifecycle/occurrence states?
2. What exact value/identity distinguishes an owner occurrence from Agenda candidate, boundary evidence and accepted firing/execution?
3. How is derived Agenda enrollment represented/rebuilt/invalidated without becoming scheduler authority?
4. Which dependency keys trigger bounded reevaluation and how are provider/source movements reflected?
5. How does one temporal owner evaluate `NOT_DUE | DUE | INDETERMINATE` from lawful chronology/provider evidence?
6. How are metric contexts/providers selected and transferred/rebased across scene/process movement?
7. How do Effect/resource/LifeState/Procedure/rest/off-screen process owners map to current schemas and routes?
8. For every shipped process/clock/deadline in `PROCESSES.md` / `thread.schema.yaml`, what is the actual native owner and what is only durable process representation?
9. How do process stage/progress/conditions/deadline/resources and created/last-event dependencies compose with TemporalBinding/chronology without becoming a generic scheduler or chronology owner?
10. How do event/signal/boundary followups cross from transient evidence into accepted Step-3 execution without a generic job queue?
11. How is one occurrence materialized exactly once even across crash/retry/live conflict?
12. How do accepted fixed RNG/children/Continuation/process state prevent duplicate consequences?
13. What chronology anchor/relation representation is required for current admitted consumers and what remains embedded?
14. How are late-established chronology relations given stable identity/bounded discovery without rewriting old events?
15. What exact semantics replace current singleton/global chronology frontier fields?
16. How does `ActiveExtensionFrontier(S)` admit multiple unordered maxima, safe retirement and singleton optimization?
17. Which current chronology fields remain semantic evidence, presentation only, derivative, stale or retired?
18. How do split/independent scenes remain incomparable until a concrete material bridge is needed?
19. How are global/shared processes represented without forcing one campaign-global mutable now or duplicate multiplayer advancement?
20. How do live source currentness/revision/close/absorption compose with stable chronology anchors and relations?
21. How does recovery restore temporal/process owners/Agenda/provider evidence without advancing time or rematerializing accepted work?
22. Which chronology/temporal/process evidence is protected for live/recovery consumers and when may derivative/source evidence compact?
23. What chronology contradictions are integrity defects versus legitimate INDETERMINATE/incomparability?
24. How is the forward-extensible temporal capability boundary enforced before unsupported mutable-past/branching writes?
25. What current tests are conforming/stale/missing?
26. What boundedness/performance requirements must future implementation verify before any optimization?
27. What evidence-based machine disposition does `thread.visibility.known_by_pc_ids` receive relative to `world.knowledge`, without creating a second durable PC-knowledge owner?
28. What evidence-based machine disposition does `thread.visibility.public` receive relative to information eligibility and `runtime.disclosure`, without treating public/readable/existing as proof of PC knowledge or PLAYER delivery?

---

## 11. Scope / non-goals

WP-15 does **not** authorize:

- a generic scheduler/job queue/pending-work mega-owner;
- a central mutable chronology service;
- a campaign-global fictional clock/current time;
- a universal chronology/global progress/currentness/durability frontier;
- vector-clock-like fiction ordering across unrelated owners;
- campaign-wide temporal CSP or full timeline rebuild;
- background/daemon fictional progression from wall-clock/host uptime;
- replay/reroll/reallocation of accepted execution;
- automatic total ordering of independent scenes;
- mutable-past/branching/causal-loop baseline architecture;
- using Git/ref/live CAS/storage/session/message/ID order as fictional order;
- treating `world.thread`/process representation as blanket owner for every temporal obligation;
- treating `thread.visibility.known_by_pc_ids` or `thread.visibility.public` as automatic knowledge/delivery/eligibility authority;
- choosing the final retained/derived/cache/hint/denormalized/retired machine shape of either thread visibility field during Step 1;
- reopening unrelated truth/knowledge/disclosure/message semantics or unrelated advancement/exploration/combat/encounter mechanics merely because their consumers intersect temporal/process state;
- starting WP-16;
- implementation planning;
- runtime/schema/template/catalog/test implementation during Step 1.

---

## 12. Failure and uncertainty bias

When a material temporal predicate cannot be decided from current accepted owner/provider/chronology evidence:

```text
insufficient compatible evidence
    -> INDETERMINATE / typed dependency resolution
    -> do not guess time/order

legitimate incomparable independent scopes
    -> remain incomparable
    -> do not manufacture join/order

persisted contradiction after bounded current refresh
    -> scoped integrity handling
    -> do not invent time travel/retcon
```

Unknown order is not simultaneity. A later technical write winning is not chronology repair.

---

## 13. Step-2 evidence / completeness gate

Senior GO is required before Step 2.

If authorized, Step 2 must follow the mandatory route in the Source Manifest and preserve item-level evidence including:

```text
Source/item
Actual claim
Authority/classification
Qualifiers/applicability
Exceptions/negative findings
Revisit/defer trigger
Existing owner/decision
Conflict / extension / no-delta
Current disposition
Rationale
```

Synthesis is blocked until architecture→machine and machine→architecture accounting covers every material current temporal owner/consumer/frontier/time/process/information-boundary surface in the active dependency subgraph.

The initial Source Manifest is not a closed world. Step 2 must explicitly discover further process/domain consumers and representations and additional actual `world.knowledge` / `runtime.disclosure` machine surfaces, not merely the files enumerated in Step 1.

The repaired mandatory evidence perimeter includes:

- `GAME/CORE/PROCESSES.md`, `GAME/SCHEMA/thread.schema.yaml`, and the scoped temporal/process statements in `ADVANCEMENT.md`, `EXPLORATION.md`, `COMBAT.md` and `ENCOUNTERS.md`, together with their recovery/publication/retention implications;
- Step-4 and Step-5.12 canonical information boundaries;
- `GAME/CORE/INFORMATION.md`;
- current `world.knowledge` / `runtime.disclosure` catalog/identity/machine surfaces reached through the owner graph;
- applicable closed WP-07 truth/knowledge/disclosure/message-evidence artifacts as upstream constraints;
- explicit evidence-based disposition of `thread.visibility.known_by_pc_ids` and `thread.visibility.public` without preselecting their final machine shape.

---

## 14. Downstream boundaries

Preserve without activation:

- **WP-16:** live physical realization must keep currentness/CAS separate from fiction and preserve chronology identity/evidence across authority transfer;
- **WP-18:** Dramaturg temporal capability guard;
- **WP-22:** executable conformance/failure/adversarial coverage including stale chronology-case repair and process/clock/deadline ownership/non-duplication cases plus information-owner isolation for thread visibility;
- **WP-24:** measured bounded Agenda/chronology/process/reconciliation performance before optimization;
- **WP-26:** stale documentation/schema/test consistency routes owned there by the eventual final package.

No downstream route authorizes work now.

---

## 15. Whole-project Task-Brief critic repair record

The mandatory critic found:

```text
C01 BLOCKING    four-way temporal responsibility split not binding enough
C02 BLOCKING    technical order/frontier non-authority perimeter incomplete
C03 BLOCKING    current machine/test chronology debt not forced into completeness accounting

C04 SIGNIFICANT Step-5.3/5.9 integration amendment not mandatory
C05 SIGNIFICANT temporal capability owner decision omitted
C06 SIGNIFICANT recovery/Agenda rebuild/no-rematerialization route under-specified
C07 SIGNIFICANT Step-3 execution/Continuation machine debt omitted
C08 SIGNIFICANT concrete temporal-owner family map incomplete
C09 SIGNIFICANT live currentness versus chronology boundary under-specified
C10 SIGNIFICANT GAME chronology-field accounting incomplete
C11 SIGNIFICANT retention/GC chronology protection omitted
C12 SIGNIFICANT downstream verification/performance/consumer routes incomplete
```

All C01-C12 are mechanically repaired in this Task Brief and its Source Manifest.

Final historical Step-1 critic disposition remains:

```text
STEP_1_CRITIC_BLOCKING:     3
STEP_1_CRITIC_SIGNIFICANT:  9
UNRESOLVED_BLOCKING:        0
UNRESOLVED_SIGNIFICANT:     0
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
```

The historical critic is not rewritten by later Senior findings.

### 15.1 Post-critic Senior recovery — SR15-01 / SR15-02

Separate recovery artifact:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-process-source-graph-omissions.md`

```text
SR15-01  BLOCKING     shipped PROCESSES runtime + thread durable representation omitted
SR15-02  SIGNIFICANT  direct ADVANCEMENT/EXPLORATION/COMBAT/ENCOUNTERS temporal consumers omitted

SR15-01: CLOSED BY SENIOR REPAIR
SR15-02: CLOSED BY SENIOR REPAIR
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

Those repairs extend only the mandatory Step-2 evidence perimeter. They do not choose final process ownership/schema semantics and do not authorize Step 2.

### 15.2 Post-critic Senior recovery — SR15-03

Separate recovery artifact:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-thread-visibility-knowledge-disclosure.md`

```text
SR15-03  SIGNIFICANT  thread.visibility.known_by_pc_ids / thread.visibility.public owner route omitted

SR15-03: CLOSED BY SENIOR REPAIR
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

This repair makes Step-4, Step-5.12, `GAME/CORE/INFORMATION.md`, current `world.knowledge` / `runtime.disclosure` machine contracts and applicable closed WP-07 evidence mandatory for Step 2. It requires explicit later disposition of both thread visibility fields while deliberately leaving their final machine shape undecided at Step 1.

---

## 16. Step-1 closure gate

```text
WP15_STEP1_PACKAGE:          STEP 1 + SENIOR REPAIR COMPLETE
SOURCE_MANIFEST_OPEN_WORLD:  YES
SR15_01:                     CLOSED
SR15_02:                     CLOSED
SR15_03:                     CLOSED
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
STEP_2_AUTHORIZED:           NO
WP16_AUTHORIZED:             NO
IMPLEMENTATION_PLANNING:     NOT AUTHORIZED
NEXT_GATE:                   MANDATORY SENIOR REVIEW
```

Stop after publication, cursor synchronization and fresh remote verification. Do not begin Step 2 without explicit Senior GO.
