# Step 5.9 — Chronology Persistence & Reconciliation — Architecture Task Brief

Status: **ARCHITECTURE TASK BRIEF — STEP 5.9 IN PROGRESS**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **Architectural / deep-work**

## 1. Problem statement

Steps 5.1–5.8 established domain-typed progress semantics, resumable runtime closure, temporal occurrence continuity, host handoff, durability obligations, Python-owned CAS publication, current-authority-first recovery and live-epoch ownership/fencing. Step 5.9 must now close the remaining fictional chronology problem:

> What is the minimum durable temporal/causal evidence HDM must retain so later mechanics, recovery and cross-scene reconciliation can establish every materially required ordering or elapsed-time relation without inventing a campaign-global clock, total event order, Git-order chronology or unnecessary simulation precision?

The current runtime already has a useful `CHRONOLOGY.md` model based on partial ordering and adaptive precision. Step 5.9 must not merely canonize that prose. It must re-derive the architecture against Steps 5.1–5.8, validate or retire existing fields such as `chronology_frontier_event_id`, `CURRENT.world_time.frontier`, local sequences/times and event relation fields, and define persistence/reconciliation/compaction semantics precisely enough for cold recovery and multiplayer.

The design must preserve HDM's deliberately simplified game/runtime model. It must not import distributed-systems mechanisms solely because similar vocabulary exists elsewhere.

## 2. Governing design question

The design must distinguish at least:

```text
causal ancestry
strict temporal precedence without causality
material simultaneity / same temporal coordinate
quantitative elapsed-time evidence
exact / approximate / bounded / qualitative temporal anchors
legitimately unordered events/scenes
insufficient evidence / INDETERMINATE
contradictory chronology / integrity defect
```

It must establish which of these require durable first-class evidence, which can remain owner-local, which can be derived, and which should not be represented at all until a consumer makes the distinction material.

## 3. Goals

Step 5.9 must produce a complete architecture such that:

1. fictional chronology is never inferred from Git commit/ref order, transport timing, SemanticEvent ID allocation, wall-clock host time or arbitrary traversal order;
2. independent scenes/processes may remain unordered when no mechanic or causal dependency requires comparison;
3. local scene chronology stays cheap and bounded during ordinary gameplay;
4. cross-scene reconciliation materializes only the minimum new ordering/elapsed constraints required by the concrete dependency;
5. `NOT_DUE | DUE | INDETERMINATE` from Step 5.3 can be reproduced after recovery from retained native/chronology evidence;
6. exact and approximate fictional time are represented only when they add rule/causal/recovery value;
7. simultaneous/contested actions are not resolved by storage/CAS winner order when fictional adjudication is required;
8. Step-5.8 live epochs can advance independently, close/absorb and later reconcile without absorption order becoming fictional chronology;
9. retained chronology evidence remains sufficient for every still-live temporal predicate, causal dependency, Procedure/Continuation requirement and recovery obligation;
10. chronology compaction may remove redundant old evidence only when all still-live semantic consumers remain decidable;
11. chronology contradictions are distinguishable from legitimate incomparability/uncertainty;
12. no new chronology abstraction becomes duplicate world-state, temporal-obligation, scheduler, live-authority or recovery authority;
13. the resulting machine model remains simple enough for deterministic Python execution and bounded ChatGPT-hosted operation.

## 4. Non-goals

Step 5.9 SHALL NOT:

- introduce one universal campaign clock;
- introduce one global total event sequence/order;
- make SemanticEvent IDs chronological counters;
- use Git storage/publication order as fictional order;
- use host wall-clock time as fictional time unless a specific owning mechanic explicitly establishes such a relation;
- timestamp every event for completeness;
- simulate continuous NPC/world advancement merely to maintain clocks;
- create a global chronology scheduler or duplicate Temporal Agenda;
- make chronology own temporal obligations already owned by Effects, Resources, Actors, Procedures or Step-3 execution;
- make chronology a new current-state or recovery snapshot authority;
- require full event-log or all-scene scans for ordinary chronology decisions;
- finalize Story/transcript representation owned by Steps 5.10–5.11;
- finalize host-delivery/disclosure timing owned by Step 5.12;
- finalize physical deletion/GC mechanics owned by Step 5.13;
- implement GAME/schema/test changes during this architecture slice.

## 5. Inherited canonical constraints

### Step 5.1 — Frontier Model

- every correctness-relevant marker is domain/scope typed;
- no implicit cross-domain ordering/comparison;
- chronology markers are temporal/partial-order evidence, never generic progress authority;
- no generic Frontier record/global monotonic sequence/universal RecoveryCut;
- independent live epochs are incomparable by default;
- Git order and SemanticEvent ID order do not imply fictional chronology.

### Step 5.2 — Resumable Runtime Closure

- native owners remain current authority;
- cold recovery uses bounded typed routing and exact source revisions;
- derived Agenda/cache/context state rebuilds;
- chronology evidence required by active owners must remain boundedly recoverable.

### Step 5.3 — Temporal & Pending-Obligation Continuity

- due evaluation is `NOT_DUE | DUE | INDETERMINATE`;
- Git/ref/ID/Agenda/host-time order does not resolve temporal ambiguity by default;
- native temporal owners own obligations/timing bindings;
- multiple actionable obligations do not imply total order;
- cold hydration does not itself advance fictional time;
- Step 5.9 owns final chronology persistence/reconciliation representation.

### Step 5.4–5.7

- host/chat lifecycle is not fictional time authority;
- durability/publication/recovery metadata do not become chronology authority;
- recovery may use chronology evidence but must not reconstruct fictional time from checkpoint age, Git timestamps or remembered chat state.

### Step 5.8 — Live-Epoch Ownership

- exact live-source revision is synchronization/fencing evidence, not fictional chronology;
- independent live epochs may advance without implicit temporal comparability;
- partial multi-scope freeze is a valid recoverable mixed state and does not mean a multi-scope fictional event partially happened;
- campaign absorption order must not imply fictional order;
- cross-scope/global transitions may use bounded freeze/reconcile/transition slow paths;
- accepted execution/RNG/temporal evidence survives close/absorption under native ownership.

## 6. Existing project surfaces to inspect

At minimum:

- `GAME/CORE/CHRONOLOGY.md`
- `GAME/CORE/PROCESSES.md`
- `GAME/CORE/EXPLORATION.md`
- `GAME/CORE/COMBAT.md`
- `GAME/CORE/RUNTIME.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/RANDOMNESS.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/STORAGE.md`
- relevant `GAME/SCHEMA/*.schema.yaml` event/current/scene/live/process/runtime structures;
- relevant `DEV/SCHEMAS/*.schema.json` TemporalBinding, duration, boundary occurrence, execution/event/procedure/continuation structures;
- chronology/temporal/multiplayer test and scenario families under `DEV/TESTS/`;
- Step-2 temporal/duration architecture;
- canonical Steps 3, 4, 5.1, 5.2, 5.3, 5.7 and 5.8;
- catalog/mechanical-surface definitions that consume elapsed/order evidence.

Concrete symbols/fields to search include:

```text
world_time
local_time
chronology_frontier_event_id
frontier
world_order
sequence
time
caused_by_event_ids
after_event_ids
simultaneous
elapsed
duration
TemporalBinding
metric_time
boundary
process clock
stage
round
turn
initiative
deadline
travel
```

Do not infer absence from one keyword-search miss.

## 7. Required alternative space

The research SHALL compare **at least five materially distinct chronology architectures** before recommending a result. Hybrids are allowed and expected, but each baseline must be analyzed independently enough to expose its failure modes.

At minimum investigate candidates in these families:

### Alternative A — Sparse causal/precedence graph

Events/anchors persist explicit causal and noncausal ordering edges; quantitative time is optional attached evidence. No global frontier beyond derived/local indexes.

### Alternative B — Scene-local logical clocks + sparse cross-scene edges

Each chronology domain keeps a monotonic local coordinate/sequence; cross-scene constraints bridge domains only when needed. Challenge whether this becomes accidental vector-clock/global-frontier machinery.

### Alternative C — Temporal anchor / interval constraint model

Chronology is primarily constraints over exact/approximate fictional-time anchors and elapsed intervals; ordering derives from constraint propagation where possible. Challenge cost/complexity and whether narrative time becomes over-mathematized.

### Alternative D — Owner-local temporal evidence only, reconciliation-on-demand

Avoid a first-class chronology graph as much as possible. Keep timing/order evidence beside native owners/events and derive cross-scene relations only when a concrete consumer requires them. Challenge bounded discoverability and long-range causal reconstruction.

### Alternative E — Hybrid sparse constraint fabric

Combine local event/owner evidence, scene-local convenience coordinates, explicit cross-domain causal/precedence edges and optional quantitative interval/anchor evidence; keep global reconciliation as sparse derivative knowledge rather than one scalar frontier.

Research may add further candidates if repository evidence suggests them. The final recommendation may combine elements, but must explain why each retained mechanism has a concrete owner/consumer and why rejected mechanisms are unnecessary or unsafe.

## 8. Evaluation dimensions

Compare alternatives against at least:

- causal/temporal correctness;
- preservation of legitimate incomparability;
- deterministic due evaluation;
- cross-scene reconciliation cost;
- cold recovery sufficiency;
- live-epoch compatibility;
- ordinary-turn latency/read complexity;
- storage growth;
- compaction/GC safety;
- corruption detection;
- observability/debuggability;
- implementation complexity;
- machine-schema complexity;
- LLM/context burden;
- migration from current runtime structures;
- risk of accidental duplicate authority/global clock;
- reversibility/extensibility.

Do not use generic distributed-systems elegance as a quality criterion unless it maps to an HDM requirement.

## 9. Required research questions

### 9.1 Authority and evidence

- Which temporal/causal facts are canonical gameplay evidence versus derived indexes/projections?
- Is chronology itself an owner of relations, or are relations always owned by the events/native owners that establish them?
- What is the minimum durable evidence that must survive after the event that originally established a relation is compacted?

### 9.2 Ordering semantics

- What exact relation set is needed: cause, happens-before, same-coordinate/simultaneous, bounded elapsed, or something smaller?
- Is explicit `UNORDERED` persisted, or is absence of a proven relation sufficient?
- How is `INDETERMINATE` distinguished from intentionally incomparable/unordered?
- How are cycles/impossible constraints detected without whole-history scans?

### 9.3 Adaptive time precision

- Which exact/approximate representations are machine-semantic?
- Are quantitative intervals/ranges first-class evidence or only owner-specific forms?
- How should qualitative anchors such as `night`, `after council`, or `third day of siege` participate in mechanics without pretending to be numeric?
- When may precision safely decrease after a high-precision episode?

### 9.4 Local scene chronology

- Does a scene need a local monotonic sequence at all?
- If yes, is it authority, indexing evidence or merely a local ordering convenience?
- What replaces/clarifies `chronology_frontier_event_id`?
- What, if anything, survives of `CURRENT.world_time.frontier`?

### 9.5 Cross-scene reconciliation

- What exact input footprint is sufficient to connect two previously independent chronology domains?
- When does one cross-scene dependency require only a new edge versus quantitative elapsed reconciliation?
- Can later evidence force contradiction with already accepted independent histories, and how is that classified?
- How can reconciliation remain bounded without maintaining vector clocks over every active scene?

### 9.6 Simultaneous/contested actions

- What evidence establishes genuine simultaneity versus unknown order?
- Which subsystem adjudicates when order is materially contested?
- What chronology evidence must be persisted after adjudication so retries/recovery cannot choose a different ordering basis?

### 9.7 Temporal obligations and recovery

- What chronology evidence must remain while an Effect/Resource/Procedure/process/deadline still depends on it?
- Can active owners hold sufficient relative anchors directly, or do they require persistent chronology references?
- What cold-recovery check proves the evidence set is sufficient without loading world history?

### 9.8 Live epochs

- How do local chronology coordinates/evidence survive `ACTIVE -> CLOSED -> campaign absorption`?
- How do two live epochs become temporally related without Git/absorption order?
- What chronology evidence is required in the multi-scope freeze/transfer/global-event slow path?

### 9.9 Compaction

- When can an intermediate event/anchor/edge be removed while preserving all still-live predicates?
- Is transitive reduction/summary evidence useful, or does it create a second derived authority?
- Which safety predicates belong to 5.9 versus physical deletion in 5.13?

## 10. Required analytical challenge

Before a recommendation, explicitly test:

1. strongest argument for a global campaign clock despite current constraints;
2. strongest argument for pure graph-only chronology;
3. strongest argument for pure interval/constraint chronology;
4. strongest argument for no first-class chronology subsystem beyond owner-local evidence;
5. whether a vector-clock-like model solves a real HDM problem or merely imports distributed-systems machinery;
6. whether local sequence counters silently become fictional order authority;
7. whether approximate quantitative intervals create false precision;
8. whether absence of explicit global reconciliation makes recovery/cross-scene queries unbounded;
9. whether sparse global summaries become a forbidden universal frontier in disguise;
10. whether compaction can preserve temporal obligations without retaining arbitrary old history.

## 11. Expected deliverables

The 5.9 architecture chain should normally include:

- this task brief;
- research draft with repository evidence and ≥5 alternatives;
- analytical challenge;
- decision brief if a genuine owner-level trade-off remains;
- candidate specification;
- adversarial review;
- resolution gate;
- canonical specification;
- roadmap/status update after closure.

No broad implementation plan is produced until the architecture sequence reaches its later approved planning gate.

## 12. Exit criteria

Step 5.9 may close only when the architecture can demonstrate:

```text
1. Storage/publication/event-ID order cannot silently become fictional order.
2. Independent chronology domains may remain incomparable without corruption.
3. Every materially required causal/temporal relation has one bounded durable evidence path.
4. Step-5.3 due evaluation remains reproducible after cold recovery.
5. Cross-scene reconciliation is bounded and materializes only required constraints.
6. Simultaneous/contested actions do not use transport race as fictional adjudication.
7. Live close/absorption does not impose fictional order across independent epochs.
8. Exact/approximate elapsed evidence has explicit semantics without universal timestamping.
9. Contradiction is distinguishable from uncertainty/incomparability.
10. Old chronology evidence can become compaction-eligible only when every still-live temporal/causal consumer remains decidable.
11. No chronology record/frontier becomes duplicate world/temporal/recovery authority.
12. Ordinary gameplay does not require campaign-wide chronology scans or continuous world simulation.
```

Until these are resolved, Step 5.10 SHALL NOT begin.
