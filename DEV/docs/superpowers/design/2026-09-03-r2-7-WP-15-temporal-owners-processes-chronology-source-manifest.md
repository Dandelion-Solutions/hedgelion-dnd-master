# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Source Manifest

Status: **STEP-1 TASK-SPECIFIC OPEN-WORLD SOURCE MANIFEST — WHOLE-PROJECT CRITIC + SENIOR REPAIR APPLIED / READY FOR MANDATORY SENIOR REVIEW**

Date: 2026-09-03

Domain: **WP-15 — temporal owners / processes / chronology**

Companion Task Brief:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief.md`

Mandatory whole-project Task-Brief critic:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-task-brief-critic.md`

Post-critic Senior recovery:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-process-source-graph-omissions.md` (`SR15-01..SR15-02`)

This manifest is **open-world**. It records the dependency subgraph established at Step 1 from current `DEV/PROJECT_MAP.md` plus direct owner/consumer inspection. Step 2, if later authorized, must extend it when actual search discovers another owner, consumer, process/domain representation, test, migration/bootstrap dependency or material supersession route.

---

## 1. Source-role vocabulary

| Role | Meaning |
|---|---|
| `CURRENT-PROGRESS / PROCESS AUTHORITY` | Controls current task/gate/process, not gameplay semantics. |
| `DERIVATIVE LOCATOR / INDEX` | Navigation only; never overrides actual owner. |
| `CANONICAL / OWNING` | Current semantic architecture authority. |
| `CANONICAL INTEGRATION / OWNING` | Current accepted integration law reconciling multiple owners. |
| `OWNER-APPROVED DECISION / OWNING` | Explicit accepted owner boundary even when physically retained under `design/`. |
| `R2.7 UPSTREAM / OWNING` | Closed R2.7 implementation-facing architecture constraining this domain. |
| `CANONICAL DOMAIN OWNER` | Durable owner outside the Step-5 spec chain that defines concrete domain semantics. |
| `IMPLEMENTATION / MACHINE CONTRACT` | Current concrete runtime/schema/template realization; evidence/consumer, not semantic owner by existence. |
| `IMPLEMENTATION / TEST CONTRACT` | Current executable/scenario contract; may be stale and has zero presumption over later owner. |
| `NEGATIVE-SCOPE / TECHNICAL EVIDENCE` | Useful evidence that a technical marker/order is not the semantic domain under audit. |
| `DESIGN PROVENANCE / CONDITIONAL` | Read only when current owner/supersession/evidence applicability requires it. |

---

## 2. Process / current-state authority

| Source | Classification | Step-2 treatment |
|---|---|---|
| `AGENTS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Repository boundaries, evidence discipline, publication/checkpoint discipline only. Development-agent transport is not fictional chronology/runtime temporal authority. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | ChatGPT development transport/verification overlay only; never a gameplay temporal/currentness owner. |
| `DEV/DESIGN_PROCESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Generic eight-step architecture process. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | HDM architecture adapter, Source Manifest/completeness/critic gates. |
| `DEV/PROJECT_MAP.md` | `DERIVATIVE LOCATOR / INDEX` | Reconstruct/refresh dependency subgraph; never semantic authority. |
| `DEV/CURRENT_PROGRESS.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Sole global current-progress/gate authority. Its progress words/ordering are not gameplay chronology. |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | `DERIVATIVE LOCATOR / INDEX` | Sequencing/scope only. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Task-local cursor only; audit sequence is not fictional time. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | R2.7 audit contract. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | `DERIVATIVE LOCATOR / INDEX` | WP-15 program questions and downstream routing. |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | `CURRENT-PROGRESS / PROCESS AUTHORITY` | Durable R2.7 execution/checkpoint method only. Conversation/task progress is not gameplay chronology. |

---

## 3. Primary canonical temporal / chronology authority

| Source | Classification | Mandatory Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` | `CANONICAL / OWNING` | Accepted RuntimeCommand/Procedure/Resolution/Continuation/ExecutionSegment identity; fixed accepted RNG; idempotency; suspension/resume; no wall-clock fingerprint/replay. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md` | `CANONICAL / OWNING` | Domain typing, no implicit cross-domain order, no generic Frontier/global sequence/RecoveryCut; chronology independent from Git/publication/allocation/durability. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` | `CANONICAL / OWNING` | Native temporal roots/recovery reachability, bounded hydration, Agenda rebuild, no generic scheduler, no accepted-execution replay. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md` | `CANONICAL / OWNING` | Native temporal owner families; occurrence identity/lifecycle; `NOT_DUE|DUE|INDETERMINATE`; owner claim/materialization; no background advancement; fixed RNG/interpretation continuity. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md` | `CANONICAL / OWNING` | Sparse accepted anchors/relations; domain-typed order/metric contexts; position providers; bounded bridge reconciliation; ActiveExtensionFrontier; live/recovery/retention/integrity/capability laws. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md` | `CANONICAL INTEGRATION / OWNING` | **Mandatory because of critic C04.** Four-way owner/Agenda/chronology/Step-3 split; derived enrollment/invalidation/recheck; Agenda never executes or advances chronology; cold rebuild behavior. |
| `DEV/docs/superpowers/design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md` | `OWNER-APPROVED DECISION / OWNING` | **Mandatory because of critic C05.** Forward-extensible accepted history; supported deadlines/split rates/immutable-history travel vs unsupported mutable-past/branching/causal-loop baseline; Dramaturg guard. |
| `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md` | `CANONICAL / OWNING` | Live exact-source currentness/CAS/routing vs fiction; close/absorption/source movement; no campaign fallback; no live revision chronology. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` | `CANONICAL / OWNING` | Chronology/temporal protected-consumer retention, new-consumer enrollment, no age/reachability/global GC frontier, source-vs-derivative cleanup. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | `CANONICAL INTEGRATION / OWNING` | Whole-system recovery/live/currentness/temporal/chronology consistency; no substitute authority; concurrent/source movements do not create fiction. |

---

## 4. Concrete native temporal-domain owner

| Source | Classification | Mandatory Step-2 extraction |
|---|---|---|
| `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` | `CANONICAL DOMAIN OWNER` | Exact concrete owner map: Effect expiration/scheduled triggers, actor/asset ResourceState recovery, LifeState recovery, Procedure boundary/resources, RestPolicy/rest Procedure, transient BoundaryOccurrence/Signal/TemporalBinding value roles; Agenda/DAG non-authority. |

Step 2 must expand this section if another current domain owner proves a temporal obligation/process family not already represented by the accepted Step-5.3 owner table.

---

## 5. Closed R2.7 upstream constraints

| Source | Classification | Mandatory Step-2 extraction |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Native routes/embedded temporal values; paths/indexes/order not identity/chronology/currentness; derived indexes rebuild; bounded lookup. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | SQLite/HOT cannot create chronology; SQL row/timestamp/order not fiction; native owners preserved; accepted execution local/live establishment boundaries; domain-scoped source revisions. |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | No global durability frontier/timer; durability/publication/currentness markers remain separate from chronology; persistence retries cannot replay accepted semantics. |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | `R2.7 UPSTREAM / OWNING` | Current native temporal root recovery; Agenda rebuild; accepted occurrence/execution no replay/reroll; checkpoint/session/SQLite/ambient context/time fields non-authority; technical order not chronology. |

Closed upstream results are constraints, not subjects to reopen by overlap. Step 2 may reopen only on a proved contradiction, new unsatisfied consumer or material insufficiency.

---

## 6. Current CORE runtime consumers / machine debt

| Source | Classification | Step-2 inspection obligation |
|---|---|---|
| `GAME/CORE/CHRONOLOGY.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Reconcile partial-order/adaptive/local behavior with Step 5.9; retire/demote global `CURRENT.world_time.frontier`; replace singleton chronology-frontier semantic assumption with multi-anchor-capable owner-typed basis; preserve INDETERMINATE rather than arbitrary ordering. |
| `GAME/CORE/RUNTIME.md` | `IMPLEMENTATION / MACHINE CONTRACT` | OOC/maintenance/process loss must not advance fiction; world changes require causes; separate stale durability timer/frontier wording from fictional time; no host/message progress as chronology. |
| `GAME/CORE/PROCESSES.md` | `IMPLEMENTATION / MACHINE CONTRACT` | **Mandatory because of SR15-01.** Primary shipped process/threat/clock runtime. Reverse-audit threats/goals/projects/countdowns/investigations/pursuits, stage/progress/advancement conditions/deadlines/resources, clocks, off-screen advancement, causal triggers, simulation budget, multiplayer duplicate-advancement prevention, event dependencies, visibility, recovery/publication/retention implications. Do not presume `world.thread` owns every temporal obligation. |
| `GAME/CORE/ADVANCEMENT.md` | `IMPLEMENTATION / MACHINE CONTRACT` | **Direct scoped consumer from SR15-02.** Inspect only rest/downtime/long-project timing, in-world time/resource cost and causally permitted off-screen process advancement; unrelated advancement semantics out of scope. |
| `GAME/CORE/EXPLORATION.md` | `IMPLEMENTATION / MACHINE CONTRACT` | **Direct scoped consumer from SR15-02.** Inspect only elapsed/travel-time semantics and off-screen process advancement; unrelated exploration/spatial mechanics out of scope. |
| `GAME/CORE/COMBAT.md` | `IMPLEMENTATION / MACHINE CONTRACT` | **Direct scoped consumer from SR15-02.** Preserve active `runtime.procedure` ownership of initiative/round/turn/active-participant/local procedure time; inspect elapsed-time consequences only; unrelated combat mechanics out of scope. |
| `GAME/CORE/ENCOUNTERS.md` | `IMPLEMENTATION / MACHINE CONTRACT` | **Direct scoped consumer from SR15-02.** Inspect only time pressure and active-process consequences; unrelated encounter mechanics out of scope. |
| `GAME/CORE/RANDOMNESS.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Fixed accepted random result survives retries/recovery/materialization; no retrospective/random reroll because temporal candidate is reevaluated. |
| `GAME/CORE/MULTIPLAYER.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Git/commit winner not fiction; current stale global-ish chronology-frontier wording; currentness/access/live synchronization vs fictional chronology. |
| `GAME/CORE/LIVE_SCENE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Live revision/HEAD/frontier is currentness/CAS only; close/rollover/absorption technical transitions do not advance scene; observable-event/local-time fields require typed chronology disposition. |
| `GAME/CORE/INTEGRITY.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Chronology contradiction vs stale/incomplete/INDETERMINATE evidence; targeted current refresh; no invented repair story; bounded diagnosis. |
| `GAME/CORE/STORAGE.md` | `IMPLEMENTATION / MACHINE CONTRACT` | Storage/ref/frontier/timestamps/durability language is not fictional chronology; stale “durable frontier time” and current-frontier terms must not cross domains. |

Step 2 must search additional `GAME/CORE` and domain consumers/representations reached from process kinds, clocks/deadlines, TemporalBinding, chronology, Agenda, execution and recovery/publication/retention dependencies. This list remains open-world.

---

## 7. GAME persistent schema/template consumers

| Source | Classification | Step-2 field/behavior accounting |
|---|---|---|
| `GAME/SCHEMA/current_state.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `world_time.frontier` is stale as generic global chronology frontier; `world_time.display` presentation only unless typed owner gives meaning; current-state routing/progress is not chronology owner. |
| `GAME/CAMPAIGN/STATE/CURRENT.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | Scaffold impact for `world_time.frontier/display`; no global clock/frontier requirement. |
| `GAME/SCHEMA/event.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `caused_by_event_ids`, `after_event_ids`, `world_order.scene_id/time/sequence`: exact domain/owner/retention semantics; IDs/sequence/storage order never implicit chronology. |
| `GAME/SCHEMA/scene.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `local_time`, singleton `chronology_frontier_event_id`, `last_event_id`, live routing fields; multi-anchor-capable chronology semantics and identity/order separation. |
| `GAME/SCHEMA/live_scene.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | `revision`, `local_time`, observable-event `world_time`, live-event identity, close status; distinguish currentness/observability from accepted chronology evidence. |
| `GAME/SCHEMA/thread.schema.yaml` | `IMPLEMENTATION / MACHINE CONTRACT` | **Mandatory because of SR15-01.** Current durable `world.thread`-shaped process representation. Account field-by-field for kind/status/owner/objective, stage/progress/next-development/advancement-conditions/deadline/resources, affected entities, visibility, `created_event_id` and `last_event_id`; map each temporal/process meaning to the actual native owner rather than inferring blanket thread ownership. |

Mandatory Step-2 rule: map every current chronology/process-adjacent field/behavior encountered to one current owner/disposition. Similar names such as `frontier`, `sequence`, `revision`, `time`, `event_id`, `deadline`, `progress` or `clock` are never presumed comparable or owner-equivalent.

---

## 8. DEV temporal/process/execution machine contracts

### 8.1 Temporal values / domain-owner state

| Source | Classification | Step-2 obligation |
|---|---|---|
| `DEV/SCHEMAS/temporal-binding.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Metric deadline / Procedure boundary / semantic boundary shape vs current Step-5.9 provider routing and chronology context semantics. |
| `DEV/SCHEMAS/duration-spec.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Metric/boundary/permanent duration definitions; duration is not host timer/current clock. |
| `DEV/SCHEMAS/boundary-occurrence.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Stable occurrence identity + causal position; transient value, not independent owner/scheduler record. |
| `DEV/SCHEMAS/world-effect-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | `temporal_binding`, `scheduled_trigger_state`, effect lifecycle/current occurrence semantics. |
| `DEV/SCHEMAS/world-actor-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | LifeState and ResourceState `recovery_binding` native-owner semantics. |
| `DEV/SCHEMAS/resource-definition-data.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Owner-specific boundary/metric recovery definition; no central job. |
| `DEV/SCHEMAS/rest-policy-definition-data.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Duration + completion boundary; rest Procedure/current process owner integration. |
| `DEV/SCHEMAS/trigger-binding.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Embedded event/signal trigger including `schedule` mode; mode does not create scheduler authority. |
| `DEV/SCHEMAS/signal.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Explicit negative evidence: transient Signal has no lifecycle/durable owner/callback authority. |

### 8.2 Accepted execution / process continuation

| Source | Classification | Step-2 obligation |
|---|---|---|
| `DEV/SCHEMAS/runtime-command-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Command accepted/settled state and pending-child ownership; no duplicate temporal firing execution owner. |
| `DEV/SCHEMAS/runtime-procedure-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Procedure-local resources/process state and missing/required temporal boundary representation. |
| `DEV/SCHEMAS/runtime-resolution-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Fixed RNG, cursor/segments/children/Continuation integration; materialized occurrence executes here/Step 3, not Agenda. |
| `DEV/SCHEMAS/runtime-continuation-state.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Fixed accepted RNG and dependencies; inspect stale generic `future_rng_frontier`; disposition `unconsumed_advancement` without host/global-clock semantics. |
| `DEV/SCHEMAS/execution-segment.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Committed accepted edge/event/child evidence; segment sequence is execution-domain order only. |
| `DEV/SCHEMAS/procedure-state-changed-event.schema.json` | `IMPLEMENTATION / MACHINE CONTRACT` | Procedure transition causal evidence; before/after revision and event ordinal do not create fictional chronology outside owning semantics. |

Step 2 must add any direct concrete schema/process consumer discovered by reference traversal/search rather than assuming this initial list is exhaustive.

---

## 9. Regression / scenario evidence

| Source | Classification | Step-2 treatment |
|---|---|---|
| `DEV/TESTS/CHRONOLOGY_CASES.md` | `IMPLEMENTATION / TEST CONTRACT` | Classify all cases against current Step-5.9. Preserve useful Git-order/simultaneity/independent-scene/boundedness tests; C12/C13 currently encode stale singleton/global-frontier assumptions and require later repair. |

Mandatory Step-2 open-world search terms include:

```text
TemporalBinding
Agenda
chronology
frontier
world_time
chronology_frontier_event_id
after_event_ids
caused_by_event_ids
local_time
future_rng_frontier
unconsumed_advancement
occurrence_key
recovery_binding
scheduled_trigger_state
duration.metric
boundary
signal
due
wall-clock
revision
sequence
process
thread
threat
goal
project
countdown
investigation
pursuit
stage
progress
advancement_conditions
deadline
clock
off-screen
rest
downtime
travel
initiative
round
turn
time pressure
```

Any directly relevant test or process/domain consumer/representation found becomes part of evidence accounting; existence never overrides canonical owners.

---

## 10. Binding semantic separation matrix

Step 2 must preserve these exact category boundaries while extracting evidence:

| Thing | What it may own/mean | What it cannot own/mean |
|---|---|---|
| Native TemporalBinding owner | Obligation existence, occurrence generation/lifecycle, binding/settlement | Generic Agenda job, current world clock, accepted execution progress |
| Process / `world.thread` representation | Owner-approved process state only where current architecture assigns it; may carry stage/progress/dependency/visibility data | Blanket ownership of every clock/deadline/temporal obligation, generic scheduler, chronology or execution authority |
| Agenda / candidate routing | Derived enrollment/recheck nomination; correctness-critical bounded discoverability where promised | Temporal obligation, DUE truth, firing execution, fictional order |
| Chronology anchor/relation/provider evidence | Typed cause/order/metric-position/elapsed evidence | Current world state, scheduler, live/currentness, publication/durability authority |
| Step-3 RuntimeCommand/Procedure/Resolution/Continuation | Accepted execution/process continuation, fixed RNG, idempotency | New native temporal source authority merely by consuming an occurrence |
| Git/campaign/live ref/revision | Publication/currentness/CAS evidence in its own domain | Fictional order, simultaneity, elapsed time, due status |
| SQLite/storage/session/host/message order | Local/technical operation evidence in own domain | Fictional chronology |
| Durability/frontier/timer exposure | Durability/risk-control bookkeeping only where owner admits it | Current fictional time/chronology frontier |
| Retention/GC age/boundary | Cleanup eligibility evidence after owner predicates | Fictional age/order or universal chronology cutoff |

---

## 11. Step-2 mandatory evidence route

If Senior GO later authorizes Step 2, run:

```text
fresh current ref / DEV/CURRENT_PROGRESS.md
-> refresh open-world Source Manifest from DEV/PROJECT_MAP.md + actual searches
-> extract Step-3 accepted execution / continuation / fixed-RNG laws
-> extract Step-5.1 domain frontier typing and no cross-domain-order laws
-> extract Step-5.3 native temporal owner / occurrence / materialization laws item-by-item
-> extract Step-5.9 sparse chronology / domain-order / metric-provider / bridge / frontier / capability laws item-by-item
-> extract Step-5.3/5.9 integration amendment item-by-item
-> extract forward-extensible temporal owner decision
-> extract Step-5.8 live-currentness boundary
-> extract Step-5.13 retention/GC chronology protection
-> extract Step-5.14 cross-slice consistency
-> extract HEALTH_EFFECTS_RECOVERY concrete temporal owner map
-> consume WP-11/WP-12/WP-13/WP-14 realization constraints
-> reverse-audit GAME/CORE/PROCESSES.md as the primary shipped process/threat/clock runtime
-> field/behavior-map GAME/SCHEMA/thread.schema.yaml as current durable process representation
-> for every process/clock/deadline establish actual native owner + relation to TemporalBinding / chronology / Step-3 execution / derived Agenda
-> inspect only temporal/process statements in ADVANCEMENT.md / EXPLORATION.md / COMBAT.md / ENCOUNTERS.md
-> reverse-audit remaining current CORE temporal/frontier/process wording
-> field/behavior-map GAME current/event/scene/live schemas/templates
-> inspect DEV temporal/process/execution machine contracts including Continuation debt
-> inspect recovery/publication/retention/visibility consequences for discovered process owners/representations
-> classify current tests and search for additional direct process/domain consumers/representations
-> architecture -> machine accounting
-> machine -> architecture accounting
-> synthesis-completeness gate
```

No Step-3 Decision Brief/candidate synthesis may begin until that completeness gate is satisfied.

---

## 12. Step-2 completeness requirements

Before synthesis may claim complete evidence, account explicitly for at least:

- every admitted native temporal owner family from Step 5.3 plus actual current domain owners;
- every current occurrence identity/materialization shape relevant to those families;
- Agenda enrollment/invalidation/rebuild path and no scheduler authority;
- current position-provider routing and `NOT_DUE | DUE | INDETERMINATE` reproduction;
- accepted execution/Continuation/fixed RNG no-rematerialization boundary;
- every current relevant chronology/frontier/time/sequence/revision field and behavior;
- current `frontier` terms by semantic domain rather than English-name similarity;
- `PROCESSES.md` threats/goals/projects/countdowns/investigations/pursuits and all stage/progress/conditions/deadline/resources/clock/off-screen/simulation-budget/duplicate-advancement behaviors;
- `thread.schema.yaml` field-by-field process representation, event dependencies and visibility;
- actual native owner for every represented process/clock/deadline, without blanket `world.thread` ownership;
- TemporalBinding / chronology / Step-3 execution / Agenda relation for each temporal process obligation;
- scoped temporal/process statements in advancement, exploration, combat and encounters without unrelated semantic reopening;
- recovery/currentness/publication/durability/retention consequences of process state and event dependencies;
- independent/split scenes and material cross-scope bridge reconciliation;
- live source currentness/close/absorb semantics versus chronology;
- recovery/cold hydration and zero-background-advance behavior;
- chronology protected-consumer retention/compaction/GC boundary;
- supported forward-extensible temporal capability and unsupported mutable-past boundary;
- stale/conforming tests;
- downstream consumers/verification/performance obligations.

The manifest remains open-world even after this checklist is met. Step 2 must actively discover additional process/domain consumers and representations rather than treating the repaired list as closed-world.

---

## 13. Downstream routes — preserved, not activated

| Target | Forward obligation |
|---|---|
| `WP-16` | Final live physical machine must keep source revision/CAS/fencing separate from fictional chronology and preserve accepted anchor/relation/process identity across live transitions. |
| `WP-18` | Dramaturg realization must preserve the owner-approved temporal capability guard and cannot gain chronology/process authority. |
| `WP-22` | Conformance/adversarial coverage for native temporal/process owners, Agenda non-authority/rebuild, provider/INDETERMINATE behavior, no duplicate materialization/advancement, domain-typed chronology, live/Git-order separation, current field retirements and difficult supported/unsupported scenarios. |
| `WP-24` | Measure bounded Agenda/chronology/process/reconciliation/relationship lookup before any optimization; no speculative global vectors/clock/CSP. |
| `WP-26` | Reconcile stale current CORE/schema/test wording routed by final architecture without reopening semantic owners. |

These entries do not authorize any listed domain now.

---

## 14. Critic + Senior repair accounting

The historical mandatory Task-Brief critic found C01-C12:

```text
3 BLOCKING
9 SIGNIFICANT
```

This manifest incorporates all original mechanical repairs:

- C01 four-way temporal responsibility split;
- C02 technical-order non-authority matrix;
- C03 current runtime/schema/test debt mandatory reverse audit;
- C04 integration amendment mandatory;
- C05 temporal capability owner decision mandatory;
- C06 RRC/WP-14 recovery/no-rematerialization route;
- C07 Step-3 execution/Continuation machine-debt route;
- C08 concrete owner-family map + schemas;
- C09 live currentness versus chronology route;
- C10 field-level GAME schema accounting;
- C11 chronology retention/GC route;
- C12 downstream verification/performance/consumer routing.

Historical `C01–C12` remain unchanged.

Separate Senior recovery `SR15-01..SR15-02` adds:

- `SR15-01 BLOCKING` — mandatory `GAME/CORE/PROCESSES.md` + `GAME/SCHEMA/thread.schema.yaml` process-runtime/representation route, including actual native-owner proof and recovery/publication/retention implications;
- `SR15-02 SIGNIFICANT` — direct scoped temporal/process consumer routes for `ADVANCEMENT.md`, `EXPLORATION.md`, `COMBAT.md` and `ENCOUNTERS.md`.

Both Senior findings are mechanically closed by this repaired manifest and companion Task Brief; no human decision or upstream reopening is required.

Final Step-1 manifest state:

```text
SOURCE_MANIFEST_OPEN_WORLD:      YES
SR15_01:                         CLOSED
SR15_02:                         CLOSED
UNRESOLVED_BLOCKING:             0
UNRESOLVED_SIGNIFICANT:          0
HUMAN_DECISION_REQUIRED:         NO
UPSTREAM_REOPEN_REQUIRED:        NO
STEP_2_AUTHORIZED:               NO
NEXT_GATE:                       MANDATORY SENIOR REVIEW
```
