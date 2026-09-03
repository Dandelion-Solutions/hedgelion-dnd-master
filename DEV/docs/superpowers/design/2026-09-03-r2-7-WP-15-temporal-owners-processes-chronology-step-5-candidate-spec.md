# R2.7 WP-15 — Step 5 Candidate Specification

Status: **CANDIDATE SPECIFICATION COMPLETE — READY FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-03

Candidate direction:

> **NARROW PROCESS-NATIVE OWNERSHIP + DERIVED TEMPORAL AGENDA + OWNER-ANCHORED SPARSE CHRONOLOGY + ACCEPTED-EXECUTION CONTINUITY**

This candidate realizes accepted temporal/process/chronology architecture against current R2.7 machine evidence. It does not implement schemas, catalogs, tests, storage APIs or runtime code.

---

# 1. Scope and authority

## LAW WP15-C01 — Four responsibilities remain distinct

```text
NATIVE TEMPORAL / PROCESS OWNER
    obligation/process existence + current lifecycle/state + owner-local binding/claim

TEMPORAL AGENDA
    rebuildable dependency-indexed candidate nomination only

CHRONOLOGY
    accepted typed cause/order/metric/bridge evidence

STEP-3 EXECUTION
    accepted consequence execution + stable identity + fixed RNG + idempotency
```

No physical representation may merge these responsibilities by convenience.

## LAW WP15-C02 — Existing specific owner wins

When an already-admitted owner owns the relevant responsibility, that owner remains authoritative. A generic process record may reference it but may not copy or replace its current state.

This is an owner-allocation law, not a search priority heuristic.

---

# 2. Narrow `world.thread` process owner

## LAW WP15-C03 — `world.thread` owns only an independently identified generic world process

`world.thread` is the current native owner for a long-running generic process only when all are true:

1. the process has stable independent world identity/lifecycle;
2. its current process state must survive beyond one immediate execution;
3. no more specific admitted owner already owns that responsibility;
4. the process advances only through established causes/conditions and accepted transition execution;
5. its temporal predicates use typed owner/chronology evidence rather than host time or a scheduler.

Examples may include independently tracked threats, projects, countdowns, investigations, pursuits, rituals, research/construction efforts or political pressure processes.

The existence of a deadline/clock alone does not create a thread.

## LAW WP15-C04 — `world.thread` is not a universal temporal/process mega-owner

The following remain with their existing owners:

| Concern | Owner |
|---|---|
| mission goal/stage/progression | `world.mission` |
| contract obligation/deadline | `world.contract` |
| effect expiration / scheduled trigger | `world.effect` |
| Actor/Asset persistent resource recovery | owning ResourceState |
| stable LifeState recovery | `world.actor` |
| combat/procedure round/turn/budget/local procedure time | `runtime.procedure` |
| rest duration/completion/current progress | RestPolicy + owning rest Procedure/process |
| pending Choice/Reaction | `runtime.continuation` |
| accepted Activity execution/randomness | Resolution/Continuation/Step-3 evidence |
| transient Signal/BoundaryOccurrence/TemporalBinding | embedded value under its source/consumer owner |

No duplicate thread is required merely to mirror these owners.

## LAW WP15-C05 — Current WP-11 thread route plus independent lifecycle requires coordinated catalog alignment

Closed WP-11 already routes native `world.thread` records through `WORLD/THREADS` with `THREAD_INDEX.yaml` as discovery-only support. Current shipped process/thread schema/scaffold supplies independent lifecycle evidence.

The current catalog-2.0 omission of `world.thread` from exact classification/structure/identifier contracts is `COORDINATED_MACHINE_ALIGNMENT_DEBT` inside the unreleased generation.

Later approved realization must align kind/admission/structure/identity/schema/scaffold/tests coherently. WP-15 does not invent an incompatible alternate family or identifier path.

---

# 3. Process-state semantics

## LAW WP15-C06 — Process stage and progress are owner-local state, not chronology

A thread may own its current stage and a progress/segmented-clock value only where the process defines the value's in-world meaning and transition/completion semantics.

An increasing number or segment count is not by itself:

- elapsed fictional time;
- chronology order;
- DUE truth;
- permission to advance;
- a pacing/drama meter.

## LAW WP15-C07 — Process advancement requires a lawful cause

A process transition requires an established causal/owner-defined condition such as:

- accepted fictional elapsed-position evidence under the process's own predicate;
- an accepted Actor/PLAYER action or inaction where the owning rules make it causal;
- acquisition/loss of a required resource or fact;
- a boundary occurrence;
- accepted event/signal/chronology relation evidence;
- another owner-defined semantic dependency.

The following never suffice merely by occurring:

- user message arrival;
- host uptime/restart;
- wall-clock elapsed time;
- Git commits/ref movement;
- Agenda polling/traversal;
- pacing preference or dramatic convenience.

## LAW WP15-C08 — `next_development` is non-executable owner-local prospective metadata if retained

`state.next_development` may describe a likely/defined next process transition for bounded reasoning. It cannot fire itself, become Dramaturg planning authority, bypass conditions, or become accepted world change without a lawful causal transition.

## LAW WP15-C09 — Thread resource fields are references/requirements, not ResourceState

A process may reference resources required/affected by a stage. Current quantity, recovery and spending remain with the native Actor/Asset/Procedure ResourceState owners.

## LAW WP15-C10 — Thread event references are provenance/dependency references only

`created_event_id` / `last_event_id` may identify creation or accepted process-transition provenance. Numeric, lexical, allocation or storage order of those IDs is not chronology/currentness.

---

# 4. Process deadlines and temporal predicates

## LAW WP15-C11 — A surviving process deadline is a typed owner-local temporal predicate

Current generic `thread.state.deadline: object|null` is under-specified machine debt.

A canonical process deadline must be representable through an accepted typed binding/predicate, such as a compatible `TemporalBinding`, whose context/provider/evidence semantics are defined by current chronology/owner contracts.

No generic wall-clock timestamp or host timer is authoritative fictional time.

## LAW WP15-C12 — DUE is evaluated, not generically persisted

The native owner evaluates:

```text
NOT_DUE | DUE | INDETERMINATE
```

from current compatible owner state + typed chronology/provider evidence.

No universal durable `due=true`, scheduler-fired bit or Agenda-owned due status is introduced.

For a compatible scalar deadline D:

```text
EXACT(x):
    x < D  -> NOT_DUE
    x >= D -> DUE

BOUNDED(lo,hi):
    hi < D -> NOT_DUE
    lo >= D -> DUE
    otherwise -> INDETERMINATE
```

Unknown/incompatible provider evidence remains INDETERMINATE.

## LAW WP15-C13 — Provider movement is owner-defined and deterministic

Movement/rebinding of metric temporal context follows exactly one admitted owner rule:

```text
FOLLOW CURRENT SCOPE
PRESERVE SOURCE PROVIDER
SAFE REBASE
```

If no compatible provider can be resolved without invention, the temporal predicate remains INDETERMINATE or enters scoped integrity handling. It never falls back to campaign-global time.

---

# 5. Temporal Agenda

## LAW WP15-C14 — Agenda is a rebuildable candidate/dependency index

An Agenda entry may contain enough data to nominate a current owner occurrence for reevaluation, including:

- native owner identity;
- occurrence/binding discriminator;
- typed dependency keys;
- bounded routing metadata.

It does not own:

- the obligation;
- process state;
- DUE truth;
- firing identity after acceptance;
- chronology;
- execution;
- fictional time advancement.

## LAW WP15-C15 — Agenda invalidation/recheck is not execution

Change to a metric position, boundary occurrence, event/signal, relation evidence or owner-local temporal state may invalidate/nominate candidates. The owner must still evaluate its predicate and cross the accepted Step-3 boundary before any consequence exists.

Agenda priority/list/traversal order never becomes fictional order or rules priority unless a separate owner contract explicitly supplies such order.

## LAW WP15-C16 — Cold recovery rebuilds Agenda from current native owners

Agenda is reconstructible after restart/cache loss from current native owner routes and admitted armed obligations. Rebuild does not advance fiction and does not require a durable scheduler/job queue.

---

# 6. Occurrence identity and accepted execution

## LAW WP15-C17 — Owner occurrence identity is distinct from temporal evidence

The native owner must distinguish the current logical occurrence from the evidence used to decide when it becomes due. Changed chronology/provider evidence does not allocate a replacement occurrence by itself.

## LAW WP15-C18 — Accepted materialization crosses the existing Step-3 execution boundary exactly once

Once an occurrence becomes accepted execution:

- its accepted command/resolution/procedure/firing identity is stable as applicable;
- fixed RNG remains fixed;
- accepted invocation/rules/catalog facts remain fixed subject to their existing compatibility contracts;
- committed ExecutionSegments/receipts/children remain committed evidence;
- a rebuilt Agenda cannot create the same occurrence again.

Recovery/retry/source movement resumes or revalidates the accepted work; it does not rematerialize, replay or reroll it.

## LAW WP15-C19 — Continuation retains accepted execution, not a generic future RNG schedule

Current `runtime.continuation.fixed_rng_results`, accepted dependencies, committed segments and child identities remain valid continuity evidence.

Generic required `future_rng_frontier` is stale machine debt unless a separate concrete accepted reserve-before-generation mechanic proves a real semantic need. WP-15 creates no such generic frontier.

`unconsumed_advancement` is valid only as an exact accepted execution remainder tied to a typed context. It cannot mean elapsed host time, restart catch-up or a global time delta.

---

# 7. Sparse chronology

## LAW WP15-C20 — Chronology is owner-anchored sparse typed evidence

Accepted chronology may include stable semantic anchors and typed relations such as:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
POSITION(provider_scope,C,EXACT|BOUNDED|UNKNOWN)
```

Causal ancestry, noncausal precedence and metric coordinate order remain distinct.

## LAW WP15-C21 — Unknown/incomparable order remains unknown/incomparable

Independent scenes/processes may remain unordered. Absence of an order relation is not simultaneity and not corruption.

A cross-scope bridge is established only when a concrete dependency makes it material.

## LAW WP15-C22 — No campaign-global mutable fictional clock or chronology frontier

HDM does not require one campaign-global mutable `now`, chronology counter or global frontier.

`CURRENT.world_time.frontier` is retired as generic/global chronology authority.

`world_time.display` may remain presentation only and cannot decide chronology/DUE/currentness without another typed owner contract.

## LAW WP15-C23 — Active extension frontier is derivative and may be multi-anchor

For an owner/scope S, `ActiveExtensionFrontier(S)` may be a rebuildable set of maximal accepted anchors relevant to safe local extension.

A mandatory singleton semantic `scene.chronology_frontier_event_id` is retired. A physical singleton optimization is permitted only when the current derivative set is provably equivalent and cardinality one.

ActiveExtensionFrontier is not a current-world owner, scheduler, RecoveryCut or global history edge.

## LAW WP15-C24 — Late relation evidence extends history without rewriting accepted identities

Newly established old relations may add accepted chronology evidence while preserving existing event/owner identities. Baseline history is forward-extensible; the architecture does not rewrite accepted past to insert chronology.

---

# 8. Current chronology-adjacent field dispositions

## LAW WP15-C25 — SemanticEvent chronology fields are domain typed

- `caused_by_event_ids` may encode causal ancestry;
- `after_event_ids` may encode noncausal required precedence only where an owning order domain is explicit/unambiguous;
- `world_order.sequence` may be an owner-local/domain-local coordinate only;
- `world_order.time` may be accepted metric/position evidence only with compatible context/provider semantics;
- none becomes a campaign-global ordering scalar by serialization.

Future machine alignment may replace ambiguous legacy shapes with explicit typed relation/provider fields while preserving accepted semantics.

## LAW WP15-C26 — Scene/live time fields are observation/provider inputs, not automatic authority

`scene.local_time`, live `local_time`, observable-event `world_time` and similar fields may be retained only with an explicit typed semantic/presentation disposition.

They cannot independently establish:

- current campaign-global time;
- DUE truth;
- ordering of unrelated scopes;
- source currentness.

## LAW WP15-C27 — Live revision/currentness is not fictional chronology

Live HEAD/base SHA, epoch, revision, CAS winner, close/rollover/absorption order and synchronization delay are Step-5.8/WP-16 currentness/fencing evidence only.

A technical live transition does not advance fiction. Fictional consequences require accepted gameplay owners/evidence.

---

# 9. Technical-order non-authority

## LAW WP15-C28 — Technical order never implicitly becomes fictional order

The following cannot establish fictional before/after, simultaneity, elapsed time or DUE without a separate explicit semantic owner contract:

- Git commit/ref/ancestry;
- campaign/live HEAD/revision/CAS order;
- SQLite row/insertion/transaction/timestamp order;
- path/shard/index/list order;
- host process/session/chat/message order;
- wall-clock elapsed time;
- ID allocation/magnitude/lexical order;
- Agenda priority/traversal order;
- durability exposure/timer/frontier order;
- checkpoint timestamp/ID/order;
- retention/GC age/reachability/removal order.

Operational order chosen by persistence/recovery may be deterministic without acquiring fictional chronology meaning.

---

# 10. Information/visibility boundary

## LAW WP15-C29 — `world.thread` owns no fictional knowledge relation

`thread.visibility.known_by_pc_ids` is retired from canonical writable thread state.

Current fictional knowledge remains solely with `world.knowledge` keyed by `(knower_id, fact_id)` under Step-4/catalog owner law.

If a concrete presentation/discovery implementation benefits from a thread-to-PC visibility projection, it must be rebuildable/non-authoritative from current eligible knowledge/evidence and revalidated before use.

## LAW WP15-C30 — Thread publicness is not knowledge, disclosure or eligibility

`thread.visibility.public` is retired as a standalone canonical semantic authority.

`public=true`, file readability, repository possession, index discovery or current record existence does not prove:

- PC knowledge;
- PLAYER delivery;
- `runtime.disclosure`;
- role-context eligibility.

A derived presentation hint may exist only with explicit non-authority semantics.

## LAW WP15-C31 — Event/live/PC knowledge and visibility fields remain evidence/projections

Legacy PC knowledge arrays, SemanticEvent knowledge deltas/event visibility and live epoch perception/knowledge fields may support migration/history/normalization under their existing owners. They do not become parallel current `world.knowledge` or `runtime.disclosure` owners.

Human PLAYER delivery remains recipient-scoped `runtime.disclosure`; accepted communication evidence remains `runtime.message`.

---

# 11. Procedure/process integration

## LAW WP15-C32 — Procedure-local timing stays with `runtime.procedure`

Initiative, round/turn position, active participant, action/reaction budgets and local Procedure timing remain `runtime.procedure` state when applicable.

Current Procedure schema under-realization is downstream machine debt. `world.encounter` or `world.thread` cannot be used as a substitute timing owner.

## LAW WP15-C33 — Off-screen change is causal, bounded and owner-local

A process may advance off-screen only when its native owner predicate becomes satisfied by accepted fictional evidence. Dormant processes are not continuously simulated.

At a material accepted fictional advancement boundary, only relevant/active/scheduled/soon-affecting process owners whose dependencies may have changed need reevaluation.

No “advance all processes on every message” rule exists.

## LAW WP15-C34 — Multiplayer cannot double-advance one semantic occurrence/interval

Two hosts/participants observing the same causal process transition or elapsed semantic interval cannot establish duplicate process advancement merely because they publish/compute concurrently.

Use native owner identity/currentness + stable occurrence/execution identity and existing Step-5.8/WP-12 transaction/CAS laws. Transport winner does not define fictional winner.

---

# 12. Recovery, durability and cleanup

## LAW WP15-C35 — Recovery is current-native-owner-first

Cold recovery:

1. resolves current native sources/routes;
2. hydrates current temporal/process owners and required evidence;
3. resumes accepted Step-3 work where already materialized;
4. rebuilds Agenda/derived frontiers/indexes/caches;
5. validates participating source/currentness basis.

Checkpoint/session/SQLite/ambient chat/model context cannot select fictional time/process state by apparent freshness.

## LAW WP15-C36 — Durability/publication does not advance fiction

Publication, SAVE, dirty-generation/exposure accounting and retry operate under WP-13/native domains. Commit creation/ref transition/order and persistence cadence do not themselves change process/chronology state.

## LAW WP15-C37 — Cleanup is owner-gated and consumer-complete

Chronology/temporal/process/RNG/Continuation evidence may compact/delete only after every protected current consumer remains decidable or has a lawful survivor.

Age, reachability, old commit position or global GC frontier cannot settle obligations or establish fictional age/order.

---

# 13. Failure / uncertainty behavior

## LAW WP15-C38 — Insufficient temporal evidence stays INDETERMINATE

If current compatible provider/relation evidence cannot decide a material owner predicate:

```text
insufficient evidence -> INDETERMINATE / bounded dependency resolution
```

Do not guess time/order or use technical freshness as substitute.

## LAW WP15-C39 — Persisted contradiction is scoped integrity failure

After bounded refresh, a contradiction such as indispensable cause after effect or incompatible exact coordinates enters scoped integrity handling/CANON_SUSPECT as owned elsewhere.

Do not invent timestamps, time travel, retcons or Git-history rewrites to make the contradiction disappear.

---

# 14. Temporal capability boundary

## LAW WP15-C40 — Baseline history is forward-extensible

Supported when current owner/evidence contracts can represent them:

- deadlines/countdowns;
- independent/split-scene progression;
- differing temporal rates/planes;
- forward jumps/stasis;
- exact/bounded elapsed evidence;
- historical mysteries/newly established old relations;
- immutable-history time travel with forward-extensible causal ancestry.

Not baseline ordinary semantics:

- rewriting accepted past;
- multiple simultaneously authoritative branching timelines/worldlines;
- routine retrocausal mutation/causal loops;
- arbitrary timeline replacement/merge.

Unsupported semantics require a future explicit architecture decision, not hidden fields or transport rewriting.

---

# 15. Boundedness / performance principles

## LAW WP15-C41 — Ordinary temporal/chronology work is dependency-local

Correctness must not require ordinary:

- full campaign WORLD scans;
- full LOG/history scans;
- all-scene scans;
- global timeline reconstruction;
- giant vector frontiers;
- campaign-wide temporal CSP solving.

Known owner reads use direct native routes; Agenda and chronology discovery remain bounded by typed dependencies/material bridges.

Performance optimization/partitioning requires WP-24 measured evidence and cannot change authority semantics.

---

# 16. Required later machine-realization alignment

This candidate routes, but does not perform, coordinated later work:

1. catalog-2.0 `world.thread` kind/admission/structure/identifier/conformance alignment;
2. `thread.schema.yaml` tightening to narrow process-owned state, typed deadline semantics and removal/demotion of writable visibility fields;
3. CURRENT/schema removal/demotion of global `world_time.frontier`;
4. scene schema removal/demotion of mandatory singleton chronology frontier semantics;
5. explicit typed chronology relation/provider representation where current legacy fields are ambiguous;
6. Procedure schema realization of already-owned local timing/order/budget state;
7. Continuation removal/qualification of generic `future_rng_frontier` and typed `unconsumed_advancement` semantics;
8. PC/live/event information-field normalization/projection constraints;
9. chronology regression C12/C13 repair and new owner/nonauthority/no-duplicate-firing tests;
10. bootstrap/migration/scaffold consistency only in their owning later WPs.

No item authorizes implementation now.

---

# 17. Downstream boundaries

- **WP-16:** live physical realization must preserve currentness-vs-chronology, native process identities and accepted execution continuity.
- **WP-18:** Dramaturg may consume temporal capability constraints but gains no process/chronology owner authority.
- **WP-19/WP-20:** bootstrap/migration eventually realize approved schema/catalog/scaffold changes.
- **WP-22:** executable conformance/adversarial/failure-injection coverage.
- **WP-24:** measured boundedness/performance before optimization.
- **WP-26:** stale CORE/schema/document consistency after final architecture.

None is activated by WP-15 Step 5.

---

# 18. Candidate gate

```text
CANDIDATE_DIRECTION:              NARROW PROCESS-NATIVE + DERIVED AGENDA + SPARSE CHRONOLOGY + EXECUTION CONTINUITY
WORLD_THREAD_UNIVERSAL_OWNER:     NO
GENERIC_SCHEDULER:                NO
GLOBAL_FICTIONAL_CLOCK_FRONTIER:  NO
BACKGROUND_FICTIONAL_PROGRESS:   NO
TECHNICAL_ORDER_AS_CHRONOLOGY:    NO
THREAD_KNOWLEDGE_OWNER:           NO
THREAD_DISCLOSURE_OWNER:          NO
ACCEPTED_EXECUTION_REPLAY:        NO
FIXED_RNG_REROLL:                 NO
SOURCE_MANIFEST_OPEN_WORLD:       YES
HUMAN_DECISION_REQUIRED:          NO
READY_FOR_STEP_6:                 YES
```
