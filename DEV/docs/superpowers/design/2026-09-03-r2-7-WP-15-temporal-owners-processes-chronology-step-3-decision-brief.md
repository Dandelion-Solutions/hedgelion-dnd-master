# R2.7 WP-15 — Step 3 Decision Brief

Status: **DECISION BRIEF COMPLETE — HUMAN DECISION REQUIRED: NO**

Date: 2026-09-03

Domain: **temporal owners / processes / chronology**

Evidence basis:

- repaired Step-1 Task Brief / Source Manifest / `SR15-01..03`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-source-manifest-step-2-expansion.md`.

---

## 1. Decision required from architecture evidence

Step 2 found no new product-semantics question. It found one repository-level owner reconciliation that must be made explicit before a candidate specification can be implementation-facing:

- the shipped process/thread family has independent identity/lifecycle and an already-closed WP-11 native route;
- current catalog-2.0 classification/machine files have not yet admitted/materialized `world.thread`;
- existing admitted specific owners already own many process-like temporal responsibilities and must not be swallowed by a generic process abstraction.

The architecture therefore needs a narrow process-owner disposition, not a new scheduler design.

---

## 2. Alternatives

### Alternative A — Force every long-running process into existing specific owners

Examples would map all threats, pursuits, investigations, rituals, construction and political pressure into `world.mission`, `world.contract`, Actor/Organization state or another nearby owner.

**Reject.**

Reason:

- current shipped process records have independent identity/status/stage/progress/dependencies and cross-turn/off-screen lifecycle;
- WP-11 already routes `world.thread` as a native family;
- not every independent process is semantically a mission, contract, effect, resource or Procedure;
- forcing process state into unrelated owners would create responsibility distortion and ad-hoc fields rather than preserve the class-admission rule.

### Alternative B — Make `world.thread` the universal temporal/process owner

This would store deadlines, clocks, resource recovery, mission stages, contract obligations, effect timers, combat rounds/rests and off-screen work in one durable process record, potentially driven by a central Agenda/scheduler/global time basis.

**Reject.**

Reason:

- directly contradicts Step-5.3 native temporal ownership and the Step-5.3/5.9 integration amendment;
- duplicates existing specific owners;
- turns a process abstraction into a generic scheduler/current-time authority;
- risks duplicate accepted execution, background advancement and chronology leakage from one queue/order.

### Alternative C — Narrow independent-process owner + existing native owners + derived Agenda + sparse chronology

Recognize `world.thread` only when the process itself has an independent world identity/lifecycle and no stronger admitted owner already owns that state.

Keep:

```text
specific native owner or narrow world.thread
    -> owns current process/temporal state

Temporal Agenda
    -> derived recheck routing

Chronology
    -> sparse typed evidence

Step-3 execution
    -> accepted consequences and fixed RNG
```

**Recommend.**

This is the minimum change consistent with current evidence and existing architecture.

---

## 3. Recommended owner allocation

### `world.thread` may own

Only one independently tracked generic process such as a threat, project, countdown, investigation, pursuit, ritual, research/construction effort or political pressure process when:

1. the process has stable independent identity/lifecycle;
2. current state must survive across turns/sessions/off-screen intervals;
3. no more specific already-admitted owner owns that responsibility;
4. transitions remain causally driven and owner-local;
5. any temporal predicate uses accepted typed binding/evidence rather than a scheduler/global clock.

It may own:

- process status;
- stage;
- semantically defined progress/segmented clock;
- causal advancement/dependency conditions;
- process-local deadline as a typed TemporalBinding/predicate;
- affected-entity references;
- provenance references.

### `world.thread` may not own

- generic campaign current time;
- chronology relations/frontier service;
- Agenda candidates/jobs;
- accepted Step-3 execution;
- effect expiration/trigger state;
- Actor/Asset resource recovery;
- LifeState recovery;
- mission state already owned by `world.mission`;
- contract obligations/deadlines already owned by `world.contract`;
- Procedure initiative/round/turn/budgets/local procedure time;
- RestPolicy semantics or accepted rest Procedure state;
- Resolution/Continuation RNG/execution state;
- fictional knowledge;
- PLAYER disclosure;
- information eligibility.

---

## 4. Thread visibility decision

Evidence is sufficient to choose a clean-slate canonical disposition now.

### `thread.visibility.known_by_pc_ids`

**Decision:** retire from canonical writable `world.thread` owner state.

Reason:

- `world.knowledge` is the sole durable fictional subject-to-proposition owner;
- the field cannot prove the complete epistemic relation or its provenance/stance;
- keeping it writable would create a parallel knowledge authority;
- if a concrete presentation/discovery use remains valuable, an implementation may derive/cache an equivalent non-authoritative projection from eligible current knowledge evidence.

### `thread.visibility.public`

**Decision:** retire as a standalone canonical knowledge/delivery/eligibility authority.

Reason:

- public/readable/existing does not establish PC knowledge;
- it does not prove PLAYER delivery under `runtime.disclosure`;
- it does not replace Step-4/R2.3 eligibility;
- any concrete UI/discovery hint must be explicitly non-authoritative/derived and cannot gate semantic access by itself.

No new secret/public-information owner is introduced.

---

## 5. Chronology/current-field decisions

The candidate must preserve existing Step-5.9 corrections:

- retire `CURRENT.world_time.frontier` as global/generic chronology authority;
- retire singleton `scene.chronology_frontier_event_id` as a general semantic field; owner-scoped `ActiveExtensionFrontier(S)` is a rebuildable multi-anchor-capable helper, with singleton optimization allowed only when equivalent;
- keep `world_time.display`, scene/live `local_time` and event/live `world_time` as presentation or typed provider observations only where an owner contract supplies exact semantics;
- keep `caused_by_event_ids` causal;
- keep noncausal precedence only in an explicit order domain;
- never turn `world_order.sequence`, ID order, live revision or storage order into global chronology.

Chronology remains distributed owner-anchored evidence, not a central mutable service.

---

## 6. Execution/recovery decisions

- Agenda entries remain derived/rebuildable candidate/dependency routes.
- DUE remains owner-evaluated from typed evidence; no durable generic DUE flag.
- Once occurrence materializes into accepted Step-3 execution, accepted identity/Continuation/fixed RNG/committed segments resume across retry/recovery/source movement.
- `runtime.continuation.future_rng_frontier` is stale machine debt unless a concrete accepted reservation mechanic is separately proven; WP-15 does not create one.
- `unconsumed_advancement` may survive only as exact accepted execution remainder with typed context, never host/wall-clock catch-up.
- cold recovery never advances process state merely because real time elapsed or the host was absent.

---

## 7. Catalog and machine-alignment decision

`world.thread` is a current semantic/native family only in the narrow independent-process sense above.

Current mismatch:

```text
WP-11 + shipped scaffold/schema
    -> world.thread family exists

catalog 2.0 exact classification/structure/identity files
    -> world.thread missing
```

**Disposition:** `COORDINATED_MACHINE_ALIGNMENT_DEBT`.

Later approved machine realization must align the same unreleased catalog generation coherently:

- world-record kind/admission;
- field structure;
- identifier policy consistent with WP-11/native identity law;
- schema/scaffold;
- conformance tests;
- routing/index documentation.

WP-15 architecture does not edit those machine contracts or choose implementation APIs/DDL/migration procedure now.

This does not reopen WP-03 class semantics or WP-11 routing; it applies them to a proven current family.

---

## 8. Candidate direction

> **NARROW PROCESS-NATIVE OWNERSHIP + DERIVED TEMPORAL AGENDA + OWNER-ANCHORED SPARSE CHRONOLOGY + ACCEPTED-EXECUTION CONTINUITY**

Required invariants:

1. every temporal/process obligation has exactly one real native owner;
2. `world.thread` is only the owner of an independently identified generic process, never a blanket temporal owner;
3. Agenda is rebuildable dependency routing only;
4. chronology is typed sparse evidence only;
5. no global fictional clock/frontier or background fictional progression;
6. no fictional chronology from technical order;
7. accepted execution/RNG/Continuation never rematerialize/replay/reroll;
8. thread visibility does not own knowledge/disclosure/eligibility;
9. recovery and retention preserve owner/currentness/evidence boundaries;
10. unsupported mutable-past/branching/causal-loop semantics remain outside baseline capability.

---

## 9. Human-decision gate

```text
REAL_CONTRADICTION_REQUIRING_OWNER:  NO
NEW_PRODUCT_SEMANTICS:              NO
MATERIAL_ARCHITECTURE_TRADEOFF:     NO
COMPATIBILITY_POLICY_DECISION:      NO
EXPLICIT_RISK_ACCEPTANCE:           NO
HUMAN_DECISION_REQUIRED:            NO
RECOMMENDED_ALTERNATIVE:            C
STEP_4_ALLOWED:                     YES
```
