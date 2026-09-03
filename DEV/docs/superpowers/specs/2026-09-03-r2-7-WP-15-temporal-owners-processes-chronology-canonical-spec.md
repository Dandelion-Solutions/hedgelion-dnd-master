# R2.7 WP-15 — Temporal Owners / Processes / Chronology — Canonical Specification

Status: **CANONICAL WP-15 RESULT — STEPS 1-8 COMPLETE / MANDATORY FINAL SENIOR AUDIT PENDING**

Date: 2026-09-03

Canonical direction:

> **NARROW PROCESS-NATIVE OWNERSHIP + DERIVED TEMPORAL AGENDA + OWNER-ANCHORED SPARSE CHRONOLOGY + ACCEPTED-EXECUTION CONTINUITY**

Canonicalization basis:

- repaired Step-1 Task Brief / Source Manifest / Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-process-source-graph-omissions.md` (`SR15-01..SR15-02`);
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-senior-recovery-thread-visibility-knowledge-disclosure.md` (`SR15-03`);
- Step-2 evidence extraction + Source Manifest expansion;
- Step-3 Decision Brief;
- Step-4 collaborative review;
- Step-5 candidate specification;
- Step-6 independent Source Manifest expansion;
- Step-6 whole-project adversarial review (`F01..F08`);
- Step-7 resolution/propagation gate.

This file is the current implementation-facing WP-15 architecture source of truth, subject to mandatory final Senior audit. Earlier Task Brief/Decision Brief/review/candidate artifacts remain derivation/provenance. Where candidate wording differs from the Step-7 repairs incorporated here, this canonical specification governs.

This specification does not implement schemas, catalogs, runtime code, storage APIs, bootstrap/migration or tests and does not authorize WP-16 or implementation planning.

---

# 1. Core authority split

## LAW WP15-1 — Four responsibilities remain distinct

```text
NATIVE TEMPORAL / PROCESS OWNER
    obligation/process existence
    current lifecycle/state
    occurrence identity
    owner-local TemporalBinding / claim

TEMPORAL AGENDA
    rebuildable dependency-indexed candidate nomination / invalidation support

CHRONOLOGY
    accepted typed causal/order/metric/boundary/bridge evidence

STEP-3 EXECUTION
    accepted consequence execution
    stable execution/firing identity
    fixed accepted RNG
    idempotency / Continuation / receipts
```

Physical co-location, one SQLite transaction or one live-source CAS does not merge these semantic responsibilities.

## LAW WP15-2 — Existing specific owner wins

When an admitted native owner already owns the relevant responsibility, it remains authoritative. A generic process may reference that owner but cannot copy/replace its current state merely to simplify scheduling or narration.

This is an owner-allocation rule, not lookup priority.

---

# 2. Narrow `world.thread` process family

## LAW WP15-3 — WP-15 admits `world.thread` only for an independently identified generic world process

`world.thread` is the native semantic owner for a long-running generic process only when all are true:

1. the process has stable independent world identity/lifecycle;
2. current process state must survive beyond one immediate execution;
3. no more specific admitted owner already owns that responsibility;
4. advancement occurs only through established causes/conditions and accepted transitions;
5. temporal predicates use typed owner/chronology evidence rather than host time or a scheduler.

Examples may include independently tracked threats, projects, countdowns, investigations, pursuits, rituals, research/construction efforts or political-pressure processes.

A deadline, clock, tag, narrative idea or Dramaturg interest alone does not create a thread.

## LAW WP15-4 — Semantic admission and physical routing remain separate

The narrow generic process family satisfies the accepted responsibility/lifecycle-driven `world.*` class rule and is canonically reconciled by WP-15.

Closed WP-11 supplies the accepted physical native route:

```text
world.thread -> WORLD/THREADS
              + INDEX/THREAD_INDEX.yaml discovery support
```

That route does not create semantic ownership by serialization alone.

WP-10's compact allocation omission does not force this independently persistent process into another owner and does not reopen unrelated WP-10 allocations. WP-15 closes the previously unsatisfied generic-process consumer.

The current catalog-2.0 absence of `world.thread` exact kind/structure/identifier/admission/conformance realization is coordinated unreleased machine-alignment debt. Later approved realization must align catalog classification/admission ledger, exact structure, identity policy, schema/scaffold and conformance tests coherently.

No alternate/duplicate generic process family is authorized.

## LAW WP15-5 — `world.thread` is not a universal temporal/process mega-owner

| Concern | Native owner |
|---|---|
| mission goal/stage/progression | `world.mission` |
| contract obligation/deadline | `world.contract` |
| effect expiration/scheduled trigger | `world.effect` |
| Actor/Asset persistent resource recovery | owning ResourceState |
| stable LifeState recovery | `world.actor` |
| procedure round/turn/budget/local procedure time | `runtime.procedure` |
| rest duration/completion/current progress | RestPolicy + owning rest Procedure/process |
| pending Choice/Reaction | `runtime.continuation` |
| accepted Activity execution/randomness | Resolution/Continuation/Step-3 evidence |
| transient Signal/BoundaryOccurrence/TemporalBinding | embedded value under its source/consumer owner |

A duplicate thread is not created merely to mirror these owners.

---

# 3. Thread/process state semantics

## LAW WP15-6 — Thread lifecycle status and temporal arming are distinct owner-local dimensions

Current broad status labels do not by themselves define a metric provider, chronology coordinate, TemporalBinding, occurrence generation or DUE state.

For the current schema vocabulary:

- `resolved`, `failed`, `obsolete` are terminal for ordinary thread advancement; they expose no new ordinary process occurrence unless a separate explicit reactivation/new-generation owner transition exists;
- `paused` does not by itself freeze fictional time, rewrite a deadline, change provider, erase elapsed evidence, SAFE_REBASE or allocate a new occurrence;
- whether a specific temporal obligation remains armed while the process is paused is defined explicitly by the process/binding mechanic;
- resume/reactivation preserves or changes occurrence/binding identity only through an explicit owner transition.

Machine realization must represent or deterministically derive the actual armed/unarmed/claimed/terminal occurrence lifecycle required by Step-5.3. Broad `status` cannot substitute for occurrence state.

## LAW WP15-7 — Thread subtype and associated entity fields grant no semantic authority

Current process subtype values such as:

```text
threat | goal | project | countdown | investigation | pursuit | custom
```

are owner-local classifications under the `world.thread` family. They are not separate `world.*` catalog kinds and do not override specific-owner allocation.

`owner_entity_id`, if retained, is an in-fiction sponsor/controller/responsible-entity association only. It does not transfer persistence ownership, repository write authority or current-state responsibility to the referenced Actor/Faction/etc.

Subtype labels cannot cause mission/contract/effect/procedure/resource state to be copied into thread.

## LAW WP15-8 — Stage/progress are process state, not chronology

A thread may own current stage and progress/segmented-clock state only where the process defines their in-world meaning, transition rules and completion semantics.

An increasing number/segment count is not by itself:

- elapsed fictional time;
- chronology precedence;
- DUE truth;
- permission to advance;
- a pacing/drama meter.

## LAW WP15-9 — Process advancement requires a lawful cause

A process transition requires an established owner-defined cause/condition, e.g. accepted fictional elapsed-position evidence, an admitted Actor/player action/inaction, resource/fact change, boundary occurrence, accepted event/signal/relation evidence or another typed dependency.

The following never suffice merely by occurring:

- user message arrival;
- host uptime/restart;
- wall-clock elapsed time;
- Git/ref movement;
- Agenda polling/traversal;
- repository save/publication;
- pacing preference or dramatic convenience.

## LAW WP15-10 — `next_development` is prospective metadata only

If retained, `state.next_development` may describe a plausible/defined next owner transition for bounded reasoning. It cannot fire itself, bypass current conditions, become Dramaturg authority or establish accepted world change.

## LAW WP15-11 — Thread resource fields are references/requirements only

A process may reference resources required/affected by a stage. Current quantity, recovery and spending remain with the native Actor/Asset/Procedure ResourceState owners.

## LAW WP15-12 — Thread event references are provenance/dependency refs only

`created_event_id` / `last_event_id` may identify accepted process-transition provenance or dependencies. Numeric, lexical, allocation or storage order of event IDs does not establish chronology/currentness.

---

# 4. Process deadlines and temporal predicates

## LAW WP15-13 — A process deadline is a typed owner-local predicate

Current generic `thread.state.deadline: object|null` is under-specified machine debt.

A surviving process deadline must use an accepted typed binding/predicate, such as compatible `TemporalBinding` semantics, whose context/provider/evidence behavior is owner-defined and compatible with Step-5.9.

No generic wall-clock timestamp, host timer or repository timestamp is authoritative fictional time.

## LAW WP15-14 — DUE is derived, not generically persisted

The native owner evaluates:

```text
NOT_DUE | DUE | INDETERMINATE
```

from current compatible owner state plus lawful chronology/provider evidence.

No universal durable `due=true`, scheduler-fired flag or Agenda-owned due state exists.

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

Unknown/incompatible evidence remains `INDETERMINATE`.

## LAW WP15-15 — Provider routing/movement is owner-defined and deterministic

Each owner/binding family defines its applicable current position provider and any movement semantics through one compatible rule:

```text
FOLLOW CURRENT SCOPE
PRESERVE SOURCE PROVIDER
SAFE REBASE
```

Movement/rebase is an owner semantic transition, not an ambient-context heuristic. `SAFE_REBASE` cannot tighten accepted uncertainty, invent a scalar or change deadline meaning.

If no compatible provider can be resolved, result remains `INDETERMINATE` or scoped integrity conflict; there is no campaign-global-time fallback.

---

# 5. Temporal Agenda and complete dependency enrollment

## LAW WP15-16 — Every independently-due armed occurrence has complete bounded typed dependency enrollment

Each admitted independently-due `ARMED` owner/binding family SHALL provide or deterministically derive the complete set of typed dependency keys whose accepted change can alter the current occurrence's temporal predicate.

Applicable dependency families include owner-specific forms of:

```text
METRIC_POSITION
BOUNDARY_OCCURRENCE
EVENT_OR_SIGNAL
RELATION_EVIDENCE
OWNER_LOCAL_TEMPORAL_STATE
```

A healthy acknowledged state cannot contain a protected armed occurrence whose declared future reevaluation path is incomplete or unreconstructible.

Completeness is for the declared owner contract, not a universal campaign dependency graph.

## LAW WP15-17 — Dependency enrollment is correctness-critical derivative routing, never semantic authority

Enrollment/index state supports bounded invalidation/recovery only. It does not own:

- obligation existence;
- occurrence identity;
- process state;
- chronology evidence;
- DUE truth;
- accepted execution;
- fictional time.

Missing required enrollment is a typed routing/recovery coherence defect. It does not erase the native obligation and does not authorize a campaign-wide scan as semantic fallback.

## LAW WP15-18 — Agenda is rebuildable candidate/dependency support only

An Agenda entry may include:

```text
native owner ref
owner occurrence identity/discriminator
binding ref/discriminator
typed dependency keys
bounded routing metadata
```

It nominates/reawakens current owner occurrences for reevaluation. It is not a scheduled job, queue item, due-time owner, firing ledger or chronology owner.

Agenda priority/list/traversal order has no fictional/rules precedence unless a separate admitted owner contract establishes such ordering.

## LAW WP15-19 — Correctness invalidation is distinct from speculative simulation budget

Off-screen/dormant simulation may avoid unrelated speculative world work.

However, when accepted evidence changes dependency key K, every currently enrolled armed occurrence whose declared predicate may be changed by K remains reachable for the owner-required invalidation/recheck path.

Narrative relevance, Dramaturg interest, loaded working set or “soon affecting” heuristics cannot suppress an already-declared correctness dependency.

No affected key => no required reevaluation. Affected admitted dependency => optimization cannot silently skip it.

## LAW WP15-20 — `INDETERMINATE` occurrences remain enrolled when future evidence can decide them

An armed occurrence is not removed from dependency routing merely because current evidence cannot establish its temporal relation.

Removal occurs only when native owner lifecycle/binding semantics make the occurrence no longer independently due/relevant or recovery ownership lawfully moves to accepted execution/another root.

## LAW WP15-21 — Enrollment changes coherently with owner/provider lifecycle

Provider movement/rebase, owner transfer, rearm, unarm, claim and terminalization recompute/remove derivative enrollment so no acknowledged healthy state leaves an armed occurrence reachable only from obsolete dependency state.

Transient duplicate routing may exist inside one coherent transition when required for safe handoff; an acknowledged omission gap is not healthy.

## LAW WP15-22 — Discovery indexes/current summaries are not temporal-root completeness authority

`THREAD_INDEX.yaml`, `CURRENT.active_threads`, Agenda lists and similar discovery/current-summary projections may nominate positive candidates but cannot prove absence of an armed independently-due owner.

Known-ID reads use WP-11 exact native routes.

Completeness-required temporal-source routing/enrollment follows typed Step-5.2/5.3 owner lifecycle contracts. No ordinary fallback scans all `WORLD/THREADS`, all WORLD, LOG/history or repository directories.

## LAW WP15-23 — Cold recovery rebuilds Agenda and future invalidatability from current native owners

Recovery:

1. resolves current native authority/routes;
2. hydrates admitted current temporal/process roots and required evidence;
3. reconstructs owner/binding/provider semantics;
4. reconstructs complete required temporal-source/dependency enrollment;
5. rebuilds Agenda/other derivatives;
6. resumes already accepted Step-3 work instead of rematerializing it.

Hydration itself does not advance fiction. A recovered armed owner is not operationally restored if its predicate may later change but no bounded declared path can reach it.

---

# 6. Occurrence identity and accepted execution

## LAW WP15-24 — Owner occurrence identity is distinct from timing evidence

The native owner distinguishes one current logical occurrence generation from the chronology/provider evidence used to evaluate it.

Changing evidence does not allocate a replacement occurrence by itself. Equal timing values do not collapse different occurrence generations.

## LAW WP15-25 — Accepted materialization closes the current owner occurrence using Step-5.3 lifecycle shapes

At the semantic acceptance edge, current occurrence `G` follows exactly one compatible form:

```text
DIRECT FINALIZATION
    ARMED(G)
        -> final owner state
           + stable accepted consequence/evidence as required

SAFE IMMEDIATE REARM
    ARMED(G)
        -> ARMED(G+1)
           + accepted F(G)
    only when schedule-independence + overlap/order-safety are proven

CONTINGENT CLAIM
    ARMED(G)
        -> CLAIMED(G,F)
           + accepted F
    while F controls source-owner settlement
```

At acceptance, the owner ceases exposing the same `G` as a distinct fresh materialization candidate.

`CLAIMED(G,F)` contains only source occurrence -> accepted execution identity. It does not duplicate execution payload/status/deadline/chronology/RNG/receipt state.

## LAW WP15-26 — Step-3 remains accepted consequence authority

Once accepted:

- command/resolution/procedure/firing identity remains stable as applicable;
- fixed RNG remains fixed;
- accepted invocation/rules/catalog facts remain under their accepted interpretation contract;
- committed ExecutionSegments, receipts and mandatory child identities remain accepted evidence;
- Continuation retains the same suspended execution generation;
- Agenda rebuild cannot create a new execution for the same accepted G.

Two distinct accepted firing identities for one occurrence generation are an integrity defect.

## LAW WP15-27 — Local and live materialization use existing native establishment boundaries

For campaign/local state whose owner contract permits local establishment, owner occurrence closure and the associated accepted consequence identity use the already admitted local atomic owner/ExecutionSegment boundary.

For live-owned state:

- deterministic pre-CAS materialization is prospective/non-current;
- authoritative establishment occurs only through the exact-source live CAS native durability edge;
- stale/rejected contenders cannot establish a second accepted consequence from old G;
- post-CAS local adoption copies the already accepted live authority and cannot roll it back/replay it.

No SQLite+Git/live distributed transaction or global firing ledger is introduced.

## LAW WP15-28 — Multiplayer cannot double-advance one semantic occurrence/interval

Concurrent hosts/participants evaluating the same causal process occurrence or semantic interval use native owner currentness, stable occurrence identity, Step-5.3 source/execution closure and Step-5.8/WP-12 currentness/CAS.

Transport winner does not define fictional precedence. Stale attempts refresh/reconcile; they do not allocate another accepted firing or reroll accepted mechanics.

## LAW WP15-29 — Continuation retains accepted execution, not a generic future RNG schedule

Existing accepted fixed RNG, dependencies, committed segments and child identities remain continuity evidence.

Generic required `runtime.continuation.future_rng_frontier` is stale machine debt unless a separately proven reserve-before-generation mechanic later establishes such semantics.

`unconsumed_advancement` is valid only as an exact typed accepted-execution remainder; it cannot mean elapsed host time, restart catch-up or global fictional-time delta.

---

# 7. Sparse chronology

## LAW WP15-30 — Chronology is owner-anchored sparse typed evidence

Accepted chronology may use stable semantic anchors and typed relations such as:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
POSITION(provider_scope,C,EXACT|BOUNDED|UNKNOWN)
```

Causal ancestry, noncausal order and metric coordinates remain distinct domains.

Chronology describes relations/evidence; it is not current world-state, temporal-obligation, execution, scheduler or live authority.

## LAW WP15-31 — Unknown/incomparable chronology remains unknown/incomparable

Independent scenes/processes may remain unordered. Absence of precedence is not simultaneity and not corruption.

Cross-scope bridge evidence is established only when a concrete admitted dependency makes it material.

## LAW WP15-32 — No campaign-global mutable fictional clock/frontier

HDM does not require one campaign-global mutable `now`, chronology counter or global fictional frontier.

Current `CURRENT.world_time.frontier` is retired as generic/global chronology authority.

`world_time.display` may remain presentation/observation only and cannot decide DUE/currentness/ordering without an explicit typed owner contract.

## LAW WP15-33 — Active extension frontier is derivative and may be multi-anchor

For scope S, `ActiveExtensionFrontier(S)` is a derivative set of maximal accepted anchors still relevant to safe current extension/recovery of S.

It may contain multiple anchors. A mandatory singleton semantic `scene.chronology_frontier_event_id` is retired; a physical singleton optimization is legal only when provably equivalent for the current typed scope and cardinality one.

Frontier is not a world owner, scheduler, RecoveryCut or global history edge.

## LAW WP15-34 — Late relation evidence extends history without rewriting accepted identities

New accepted evidence may establish a typed relation between old stable anchors without rewriting their accepted identity/meaning.

Ordinary baseline history is forward-extensible rather than mutable-past replacement.

This capability does not guarantee indefinite retention of every old event/detail or arbitrary historical pair query.

## LAW WP15-35 — Historical chronology capability is consumer-bounded

Still-live or explicitly promised consumers retain bounded sufficient temporal/causal evidence under their owner contracts.

After lawful compaction, an unpromised historical query may remain `INDETERMINATE`/unavailable when required evidence is no longer retained.

New accepted historical evidence may establish a relation prospectively when it independently supplies/addresses adequate stable support. Old Git bytes, host memory, transcript remnants or arbitrary scans do not recreate semantic evidence authority.

---

# 8. Chronology-adjacent machine-field dispositions

## LAW WP15-36 — SemanticEvent chronology fields are domain typed

- `caused_by_event_ids` may encode causal ancestry;
- `after_event_ids` may encode noncausal required precedence only where an owning order domain is explicit/unambiguous;
- `world_order.sequence` may be an owner/domain-local coordinate only;
- `world_order.time` may be accepted metric/position evidence only with compatible context/provider semantics.

None becomes a campaign-global ordering scalar by serialization.

Legacy ambiguous shapes may be replaced/narrowed in later machine alignment while preserving accepted semantics.

## LAW WP15-37 — Scene/live time fields are observation/provider inputs only when explicitly typed

`scene.local_time`, live `local_time`, observable-event `world_time` and similar fields may survive only with explicit semantic/presentation/provider disposition.

They do not independently establish global current time, DUE, unrelated-scope ordering or source currentness.

## LAW WP15-38 — Live currentness/revision is not fictional chronology

Live HEAD/base SHA, epoch identity, source revision, CAS winner, close/rollover/absorption order and synchronization delay are currentness/fencing/authority evidence only.

Technical live transitions do not advance fiction unless a separate accepted gameplay transition establishes chronology evidence.

## LAW WP15-39 — Technical order never implicitly becomes fictional order

The following cannot establish fictional before/after, simultaneity, elapsed time or DUE without a separate semantic owner contract:

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

---

# 9. Information/visibility boundary

## LAW WP15-40 — `world.thread` owns no fictional knowledge relation

Current `thread.visibility.known_by_pc_ids` is retired from canonical writable thread state.

Current fictional subject knowledge remains solely with `world.knowledge` keyed by `(knower_id, fact_id)` under Step-4/catalog owner law.

A thread-to-PC presentation/discovery projection may exist only as rebuildable/non-authoritative derived state revalidated from eligible current knowledge/evidence.

## LAW WP15-41 — Thread publicness is not knowledge/disclosure/eligibility authority

Current `thread.visibility.public` is retired as a standalone canonical semantic authority.

`public=true`, repository readability, file possession, index discovery or record existence does not prove:

- PC knowledge;
- PLAYER delivery;
- `runtime.disclosure`;
- role-context eligibility.

A derived presentation hint may survive only with explicit non-authority semantics.

## LAW WP15-42 — Legacy event/live/PC visibility/knowledge fields remain evidence/projections

Legacy PC knowledge arrays, event knowledge deltas/visibility and live perception/knowledge fields may support migration/history/normalization under their owning contracts. They are not parallel writable `world.knowledge` or `runtime.disclosure` owners.

Human PLAYER delivery remains recipient-scoped `runtime.disclosure`; accepted communication evidence remains `runtime.message`.

---

# 10. Procedure and off-screen integration

## LAW WP15-43 — Procedure-local timing remains `runtime.procedure`

Initiative, round/turn position, active participant, action/reaction budgets and procedure-local timing/order remain `runtime.procedure` state when applicable.

Current Procedure schema under-realization is downstream machine debt. `world.encounter` or `world.thread` cannot substitute as timing owner.

## LAW WP15-44 — Off-screen process change is causal and dependency-local

A process advances off-screen only when its current native owner predicate is satisfied by accepted fictional evidence and the occurrence lawfully crosses its owner/Step-3 acceptance boundary.

Dormant/unrelated processes are not continuously simulated. The simulation budget limits speculative work, while LAW WP15-19 preserves correctness-required invalidation for declared changed dependencies.

No “advance all processes on every message” behavior exists.

---

# 11. Recovery, durability, cleanup and failure behavior

## LAW WP15-45 — Recovery is current-native-owner-first and never fiction-advancing

Cold recovery follows current owner routes/sources, hydrates required current roots/evidence, resumes accepted execution, reconstructs complete temporal dependency routing and rebuilds Agenda/frontiers/indexes/caches.

Checkpoint/session/SQLite/ambient chat/model context cannot select fictional time/process state by apparent freshness.

Recovery/hydration alone does not create a boundary, fire an occurrence, advance a process or reroll accepted execution.

## LAW WP15-46 — Durability/publication does not advance fiction

SAVE, publication, dirty-generation/exposure accounting, Git commit/ref transitions and persistence retry remain technical durability/currentness semantics under their native owners.

They cannot alter process/chronology state merely by occurring.

## LAW WP15-47 — Cleanup is owner-gated and consumer-complete

Chronology/temporal/process/RNG/Continuation evidence may compact/retire only after every protected current consumer remains lawfully decidable or has an accepted sufficient survivor under Step-5.9/5.11/5.13 contracts.

Age, reachability, old commit position or a global GC frontier cannot settle obligations or establish fictional age/order.

## LAW WP15-48 — Insufficient evidence stays `INDETERMINATE`; contradiction is scoped integrity

If current compatible provider/relation evidence cannot decide a material predicate, preserve `INDETERMINATE` and perform only bounded dependency-specific resolution when required.

After bounded current refresh, incompatible accepted chronology evidence enters scoped integrity/CANON_SUSPECT handling. Do not invent timestamps, retcons, time travel or Git-history rewriting to conceal contradiction.

---

# 12. Temporal capability boundary

## LAW WP15-49 — Baseline chronology is forward-extensible

Supported when current owner/evidence contracts can represent them:

- deadlines/countdowns;
- independent/split-scene progression;
- differing temporal rates/planes;
- forward jumps/stasis;
- exact/bounded elapsed evidence;
- historical mysteries and newly established old relations;
- immutable-history time travel with forward-extensible causal ancestry.

Not baseline ordinary semantics:

- rewriting accepted past;
- multiple simultaneously authoritative branching timelines/worldlines;
- routine retrocausal mutation/causal loops;
- arbitrary timeline replacement/merge.

Immutable-history time travel is not a generic rewind or unrestricted historical-state reconstruction guarantee. Unsupported semantics require a future explicit architecture decision rather than hidden transport/storage tricks.

## LAW WP15-50 — Ordinary temporal/chronology work is bounded and dependency-local

Correctness must not require ordinary:

- full WORLD scans;
- full LOG/history scans;
- all-scene scans;
- all-thread directory scans;
- global timeline reconstruction;
- giant vector frontiers;
- campaign-wide temporal CSP solving.

Known owner reads use direct native routes. Temporal-source/enrollment completeness uses typed owner-specific routing. Chronology discovery uses typed material dependencies/bridges.

If fanout becomes operationally unbounded, later machine work must introduce an owner/domain-specific bounded partition/summary/index without changing semantic authority. WP-24 measured evidence precedes optimization.

---

# 13. Implementation-facing machine alignment obligations

After final Senior approval and only in the owning downstream work, machine realization must account for at least:

1. coordinated catalog-2.0 `world.thread` classification/admission-ledger/structure/identifier/conformance alignment;
2. `thread.schema.yaml` tightening for narrow process owner state, actual arming lifecycle, typed deadline semantics, terminal/pause boundaries, association/subtype nonauthority and visibility retirement/demotion;
3. completeness-typed temporal-source routing for independently-due armed owners, distinct from discovery indexes/current summaries;
4. deterministic extraction of complete dependency keys for each admitted armed owner/binding family;
5. bounded reverse dependency enrollment/invalidation and coherent rewrite on provider move/rebase/rearm/unarm/claim/terminalization;
6. cold-recovery reconstruction of temporal-source routing + Agenda + future invalidatability from current native owners;
7. Step-5.3 source/execution closure realization including direct-finalize/safe-rearm/claim and duplicate-firing prevention;
8. live exact-source CAS realization preserving one accepted occurrence/execution establishment edge;
9. CURRENT/schema removal/demotion of generic global `world_time.frontier`;
10. scene schema removal/demotion of mandatory singleton chronology-frontier semantics;
11. explicit typed chronology relation/provider representation where legacy fields are ambiguous;
12. Procedure schema realization of already-owned local timing/order/budget state;
13. Continuation removal/qualification of generic `future_rng_frontier` and typed `unconsumed_advancement` semantics;
14. PC/live/event information-field normalization/projection constraints;
15. process/thread discovery indexes kept non-authoritative and non-exhaustive for temporal-root absence proof;
16. current CORE reconciliation for process simulation budget, chronology frontier and visibility wording;
17. regression/failure-injection coverage for all final laws.

No item authorizes implementation in WP-15 Step 8.

---

# 14. Downstream ownership / deferred obligations

- **WP-16:** final live physical realization must preserve native process occurrence identity, source/execution closure, exact-source currentness and no chronology-from-CAS semantics.
- **WP-18:** Dramaturg may consume temporal capability/constraints but gains no process/chronology/knowledge owner authority.
- **WP-19/WP-20:** bootstrap/migration realize approved catalog/schema/scaffold/current-summary changes only after architecture approval.
- **WP-22:** executable coverage for complete enrollment, stale/missing routes, no broad scans, DUE/INDETERMINATE, provider movement, pause/terminal lifecycle, duplicate materialization/CAS races, fixed RNG/no replay, recovery rebuild, visibility-owner separation, sparse chronology and retention boundaries.
- **WP-24:** measure dependency fanout/index size/latency and only then justify repartition/optimization.
- **WP-26:** stale CORE/schema/document consistency, including global/singleton chronology wording, process status/visibility and thread machine-contract normalization.

These are routed obligations, not activated work.

---

# 15. Canonical invariant

WP-15's final invariant is:

> **A gameplay-significant temporal/process occurrence exists only in its native owner; complete typed derivative enrollment makes the armed occurrence boundedly re-evaluable and recoverable; chronology supplies sparse accepted evidence but never scheduling authority; once the occurrence crosses its owner-native Step-5.3 acceptance edge, the same occurrence becomes unavailable for fresh materialization and Step-3 owns one stable accepted consequence with fixed RNG/idempotency. `world.thread` is only the narrow independently persistent generic process owner, never a substitute for specific owners, knowledge/disclosure, Procedure timing or global time. Technical storage/currentness/order and speculative simulation policy cannot invent, suppress or reorder fictional causality.**

---

# 16. Final gate

```text
WP15_DIRECTION:                     NARROW PROCESS-NATIVE + DERIVED AGENDA + SPARSE CHRONOLOGY + EXECUTION CONTINUITY
STEP_6_BLOCKING:                    2
STEP_6_SIGNIFICANT:                 6
UNRESOLVED_BLOCKING:                0
UNRESOLVED_SIGNIFICANT:             0
WORLD_THREAD_UNIVERSAL_OWNER:       NO
WORLD_THREAD_SEMANTIC_ADMISSION:    YES — NARROW INDEPENDENT GENERIC PROCESS ONLY
GENERIC_SCHEDULER:                  NO
GLOBAL_FICTIONAL_CLOCK_FRONTIER:    NO
TEMPORAL_ENROLLMENT_COMPLETE:       REQUIRED DERIVATIVE INVARIANT
DISCOVERY_INDEX_AS_ROOT_AUTHORITY:  NO
ACCEPTED_OCCURRENCE_REOPEN:         NO
DUPLICATE_ACCEPTED_FIRING:          NO
FIXED_RNG_REROLL:                   NO
THREAD_KNOWLEDGE_OWNER:             NO
THREAD_DISCLOSURE_OWNER:            NO
ARBITRARY_HISTORICAL_QUERY_PROMISE: NO
HUMAN_DECISION_REQUIRED:            NO
UPSTREAM_REOPEN_REQUIRED:           NO
IMPLEMENTATION_AUTHORIZED:          NO
NEXT_GATE:                          MANDATORY FINAL SENIOR AUDIT
```
