# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Architecture Task Brief

Status: **STEP-1 TASK BRIEF / WHOLE-PROJECT CRITIC REPAIRS APPLIED — READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-03

Target branch: `v1/engine-rearchitecture`

Task-specific open-world Source Manifest:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief-critic.md`

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
- Step-5.1 domain-typed frontier model;
- Step-5.2 Resumable Runtime Closure;
- Step-5.3 temporal/pending continuity and native temporal ownership;
- Step-5.9 chronology persistence/reconciliation;
- the Step-5.3/5.9 Temporal Agenda/chronology integration amendment;
- the owner-approved forward-extensible temporal capability boundary;
- Step-5.8 live currentness/CAS/absorption semantics;
- Step-5.13 chronology/temporal retention and cleanup constraints;
- Step-5.14 integrated recovery/concurrency review;
- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` concrete effect/resource/LifeState/Procedure/rest temporal-owner map;
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

### 9.1 CORE chronology/runtime/live prose

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

### 9.2 GAME chronology/current/live fields

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
```

Required inherited dispositions include:

- retire `CURRENT.world_time.frontier` as generic global chronology frontier/authority;
- `world_time.display` is presentation only absent another typed owner contract;
- scene singleton `chronology_frontier_event_id` is superseded semantically by multi-anchor-capable `ActiveExtensionFrontier(S)`; singleton remains only a possible physical optimization when semantically valid;
- `world_order.sequence` is not a campaign-global fictional counter;
- `after_event_ids` may encode a clearly owner-defined local order domain, not untyped universal precedence;
- `caused_by_event_ids` is causal ancestry, not calendar order;
- live revision/HEAD/currentness fields are not chronology.

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

### 9.4 Regression debt

`DEV/TESTS/CHRONOLOGY_CASES.md` is mandatory evidence.

- cases preserving independent scenes, Git-order non-authority, contested simultaneity, contradiction handling and boundedness are useful;
- current C12/C13 preserve stale singleton/global frontier expectations and require later repair under final WP-15 architecture.

Step 2 must search the repository for additional direct tests/consumers rather than treating this as a closed list.

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
8. How do event/signal/boundary followups cross from transient evidence into accepted Step-3 execution without a generic job queue?
9. How is one occurrence materialized exactly once even across crash/retry/live conflict?
10. How do accepted fixed RNG/children/Continuation/process state prevent duplicate consequences?
11. What chronology anchor/relation representation is required for current admitted consumers and what remains embedded?
12. How are late-established chronology relations given stable identity/bounded discovery without rewriting old events?
13. What exact semantics replace current singleton/global chronology frontier fields?
14. How does `ActiveExtensionFrontier(S)` admit multiple unordered maxima, safe retirement and singleton optimization?
15. Which current chronology fields remain semantic evidence, presentation only, derivative, stale or retired?
16. How do split/independent scenes remain incomparable until a concrete material bridge is needed?
17. How are global/shared processes represented without forcing one campaign-global mutable now?
18. How do live source currentness/revision/close/absorption compose with stable chronology anchors and relations?
19. How does recovery restore temporal owners/Agenda/provider evidence without advancing time or rematerializing accepted work?
20. Which chronology/temporal evidence is protected for live consumers and when may derivative/source evidence compact?
21. What chronology contradictions are integrity defects versus legitimate INDETERMINATE/incomparability?
22. How is the forward-extensible temporal capability boundary enforced before unsupported mutable-past/branching writes?
23. What current tests are conforming/stale/missing?
24. What boundedness/performance requirements must future implementation verify before any optimization?

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

Synthesis is blocked until architecture→machine and machine→architecture accounting covers every material current temporal owner/consumer/frontier/time/process surface in the active dependency subgraph.

The initial Source Manifest is not a closed world.

---

## 14. Downstream boundaries

Preserve without activation:

- **WP-16:** live physical realization must keep currentness/CAS separate from fiction and preserve chronology identity/evidence across authority transfer;
- **WP-18:** Dramaturg temporal capability guard;
- **WP-22:** executable conformance/failure/adversarial coverage including stale chronology-case repair;
- **WP-24:** measured bounded Agenda/chronology/reconciliation performance before optimization;
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

Final Step-1 critic disposition:

```text
STEP_1_CRITIC_BLOCKING:     3
STEP_1_CRITIC_SIGNIFICANT:  9
UNRESOLVED_BLOCKING:        0
UNRESOLVED_SIGNIFICANT:     0
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
```

No human-owned decision is required at Step 1.

---

## 16. Step-1 closure gate

```text
WP15_STEP1_PACKAGE:          COMPLETE AFTER CURSOR/REMOTE VERIFICATION
SOURCE_MANIFEST_OPEN_WORLD:  YES
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
STEP_2_AUTHORIZED:           NO
WP16_AUTHORIZED:             NO
IMPLEMENTATION_PLANNING:     NOT AUTHORIZED
NEXT_GATE:                   MANDATORY SENIOR REVIEW
```

Stop after publication, cursor synchronization and fresh remote verification. Do not begin Step 2 without explicit Senior GO.
