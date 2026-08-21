# Step 5.9 — Chronology Persistence & Reconciliation — Research Draft

Status: **RESEARCH / DERIVATION — NONCANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Task brief:

- `2026-08-20-step-5-9-chronology-persistence-reconciliation-task-brief.md`

## 1. Executive research result

The current HDM chronology direction is conceptually strong but under-specified at the machine/persistence boundary.

The strongest evidence currently favors a **hybrid sparse constraint fabric**, but not a single generic chronology graph, global clock, vector clock or interval solver.

The likely useful composition is:

```text
owner/event-local causal + precedence evidence
        +
optional scope-local chronology coordinates as convenience/index evidence
        +
explicit sparse cross-domain bridge constraints only when material
        +
optional typed metric-context anchors / elapsed bounds when mechanics require them
        +
derived bounded reconciliation summaries/indexes where measured useful
```

This is a research conclusion, not yet a recommendation or canonical decision.

The largest machine-contract gap found so far is **metric temporal context ownership**. `TemporalBinding.metric_deadline` names a `context_id` and stores `anchor_value` / `deadline_value`, but the inspected active runtime/schema/catalog surfaces do not define a first-class owner of that context's current coordinate, advancement semantics, recovery source or live/campaign transition behavior. Therefore `context_id` is not presently sufficient to make metric due evaluation recoverable. Step 5.9 must close this contract without silently treating `CURRENT.world_time` as a universal clock.

A second likely debt is `CURRENT.world_time.frontier`: current prose describes it as a compact globally reconciled chronology frontier, but Step 5.1 prohibits a generic scalar/global frontier whose scope/comparison semantics are implicit. The concept may survive only if narrowed to typed sparse reconciliation evidence/anchors or a clearly scoped derived index; the current field name/shape is not enough.

## 2. Method

Research used:

1. canonical Step 5.1 domain-typing/frontier laws;
2. Step 5.3 temporal continuity and three-valued due evaluation;
3. Steps 5.7–5.8 recovery/live authority laws;
4. current runtime chronology/process/schema surfaces;
5. chronology regression cases;
6. Step 1–2 retrospective assurance temporal findings;
7. classic primary temporal-ordering models as analytical references, not imported architecture.

External analytical references:

- Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, CACM 21(7), 1978.
- Colin Fidge, *Timestamps in Message-Passing Systems That Preserve the Partial Ordering*, Australian Computer Science Communications, 1988.
- Friedemann Mattern, *Virtual Time and Global States of Distributed Systems*, 1989.
- James F. Allen, *Maintaining Knowledge about Temporal Intervals*, CACM 26(11), 1983, DOI 10.1145/182.358434.
- Rina Dechter, Itay Meiri, Judea Pearl, *Temporal Constraint Networks*, Artificial Intelligence 49, 1991, DOI 10.1016/0004-3702(91)90006-6.

These works provide comparison tools for partial order, vector timestamps, qualitative interval relations and metric difference constraints. HDM is not a distributed-systems simulator or general temporal CSP engine, so mechanisms are retained only where concrete HDM consumers justify them.

## 3. Verified facts from current architecture

### FACT 3.1 — Chronology is already partial-order-first

`GAME/CORE/CHRONOLOGY.md` states:

```text
Chronology must be as precise as causality requires, and no more precise.
```

It explicitly allows independent events/scenes to remain unordered and rejects Git commit order as fictional chronology.

### FACT 3.2 — Existing semantic relation fields already distinguish cause from precedence

Current event schema/prose expose:

```text
caused_by_event_ids
    genuine causal ancestry

after_event_ids
    required precedence without necessarily claiming causation

world_order.scene_id
world_order.sequence
world_order.time
```

This distinction is architecturally valuable and should not be collapsed into one generic `before` counter.

### FACT 3.3 — Existing scene/current chronology fields are weakly typed

Current surfaces include:

```text
scene.local_time
scene.chronology_frontier_event_id
CURRENT.world_time.frontier
CURRENT.world_time.display
live chronology/time envelope fields
```

Their prose meanings predate canonical Step-5 domain-typing and live-authority decisions. They require re-derivation rather than automatic preservation.

### FACT 3.4 — Step 5.1 prohibits implicit universal chronology progress

Step 5.1 establishes:

```text
DOMAIN TYPING
NO IMPLICIT CROSS-DOMAIN ORDER
```

and explicitly says:

- Git order does not imply fictional order;
- SemanticEvent ID order does not imply fictional order;
- independent scenes may remain unordered;
- local numeric/sparse chronology values are allowed only inside explicit scope/domain;
- a globally reconciled chronology marker describes chronology constraints/knowledge, not generic campaign progress.

### FACT 3.5 — Step 5.3 requires three-valued due evaluation

Temporal comparison is:

```text
NOT_DUE
DUE
INDETERMINATE
```

Host wall clock, Git order, record ID order, Agenda order and traversal order cannot resolve ambiguity unless an explicit chronology contract grants that evidence meaning.

### FACT 3.6 — Temporal obligation authority is not chronology authority

Effect, Resource, LifeState, Procedure and other native owners retain timing/occurrence authority. Temporal Agenda is rebuilt. Chronology supplies comparison/evidence where needed; it does not become a scheduler or obligation ledger.

### FACT 3.7 — Metric duration is already context-scoped

`TemporalBinding.metric_deadline` conceptually contains:

```text
context_id
anchor_value
deadline_value
unit?
```

This is positive evidence against one mandatory world clock: metric deadlines are already intended to be evaluated in a named context.

### FACT 3.8 — Current metric-context owner is not established in inspected active surfaces

In the inspected:

- `temporal-binding.schema.json`;
- current/scene/live state schemas;
- current `CHRONOLOGY.md` / `PROCESSES.md`;
- mechanical-surface catalog;
- canonical Step-5 temporal/recovery specifications;

the architecture names metric `context_id` but does not define an explicit machine owner/current-coordinate contract with:

```text
current coordinate authority
advancement authority
unit/scale semantics
recovery source
revision/currentness semantics
live close/absorption behavior
cross-context relation rules
```

This is a verified missing contract in the inspected active surfaces. It is not claimed as proof that no historical document ever discussed such an owner.

### FACT 3.9 — Quantitative elapsed evidence can outlive active timers

The Step 1–2 retrospective assurance explicitly states that established quantitative elapsed evidence cannot be discarded merely because no timer is currently armed.

Therefore some quantitative chronology evidence has independent future-consumer value beyond the lifecycle of one active TemporalBinding.

This does **not** imply a globally advancing clock.

### FACT 3.10 — Processes are causally/lazily advanced

Current process architecture advances off-screen/global processes only from accepted fictional triggers, thresholds, direct causal actions or chronology establishing sufficient elapsed fictional time. Host real time is not a driver; continuous world simulation is not required.

### FACT 3.11 — Step 5.8 separates live synchronization order from fictional chronology

Exact live source revision is a CAS fence, not fictional time. Independent live epochs are incomparable by default. Partial multi-scope freeze is valid recovery state and does not mean a cross-scope fictional event partially happened. Campaign absorption order cannot define fictional chronology.

### FACT 3.12 — Existing chronology regression cases already favor sparse reconciliation

Current tests cover:

- same-scene causal chain;
- independent unordered scenes;
- cross-scene information dependency adding only required order;
- deadlines/races requiring precision;
- harmless narrative compression;
- delayed process causal retention;
- material unknown order requiring minimal reconciliation;
- Git-order contradiction ignored;
- impossible chronology classified as suspect;
- contested/simultaneous actions resolved by mechanics/world logic;
- scene frontier/local-time convenience.

The tests support local/sparse semantics, but their frontier vocabulary still needs Step-5.1-compliant representation.

## 4. Constraints

### CONSTRAINT 4.1 — No universal fictional clock requirement

A campaign may contain multiple independently advancing scenes/processes with no meaningful relative coordinate.

### CONSTRAINT 4.2 — No implicit total order

Unrelated accepted events may remain incomparable indefinitely.

### CONSTRAINT 4.3 — Chronology evidence must support recovery

If an active temporal predicate or accepted causal dependency needs evidence after process/chat loss, that evidence must remain boundedly recoverable.

### CONSTRAINT 4.4 — Ordinary hot path must stay local

No full history scan, all-scene vector refresh, global CSP solve or continuous clock simulation is acceptable on ordinary actions.

### CONSTRAINT 4.5 — Precision is consumer-driven

Exact numeric timing is required only when a concrete mechanic, causal race, recovery predicate or future reconciliation depends on it.

### CONSTRAINT 4.6 — Chronology does not own accepted execution

Step 3 owns RuntimeCommand/Resolution/Procedure/Continuation execution identity and lifecycle.

### CONSTRAINT 4.7 — Chronology does not own temporal obligations

Step 5.3 native temporal owners remain authority.

### CONSTRAINT 4.8 — Synchronization order is not fictional order

CAS winners, repository order, branch absorption order and network timing cannot serve as fictional ordering without separately established semantic relation.

## 5. Theory-to-HDM mapping

### 5.1 Lamport happens-before

Lamport's central useful idea is that causality induces a partial order. A logical-clock scalar can be chosen to respect that order, and an additional convention can extend it to a total order, but that total order contains ordering not implied by causality.

HDM implication:

- partial order is the relevant semantic concept;
- a scalar local ordering aid may be useful;
- extending chronology to total order merely for deterministic storage/debug output would create fiction not justified by mechanics.

### 5.2 Fidge/Mattern vector time

Vector timestamps capture whether distributed events are causally ordered or concurrent without a central clock. Their cost, however, tracks participating processes/domains, and their semantics are fundamentally about communication-derived causality.

HDM implication:

- the distinction between causally related and concurrent/incomparable domains is useful;
- maintaining a vector component for every active scene/process is unnecessary unless HDM needs repeated arbitrary cross-scene causal comparisons at scale;
- current requirements instead favor sparse explicit bridge dependencies and bounded lookup.

Vector-clock ideas are useful as a counterexample/check, not an obvious machine representation.

### 5.3 Allen interval relations

Allen's interval algebra represents qualitative relations such as before/after/overlap/during and supports constraint propagation without requiring every interval to have numeric endpoints.

HDM implication:

- qualitative relations and genuine simultaneity/overlap can be first-class when mechanics care;
- encoding the full Allen relation algebra for ordinary play is probably unnecessary;
- a small typed relation subset may cover HDM without false numeric precision.

### 5.4 Dechter–Meiri–Pearl temporal constraint networks

Temporal constraint networks represent metric information as constraints on time differences. Simple temporal problems use interval bounds and permit efficient reasoning.

HDM implication:

- bounded elapsed-time evidence is naturally represented as difference constraints where required;
- full campaign-wide constraint propagation would be overkill;
- small owner/scope-local constraint components can provide exact mechanical comparisons without introducing a universal clock.

## 6. Alternative A — Sparse causal/precedence graph

### Model

Persist chronology primarily as explicit event/anchor relations:

```text
CAUSES(A,B)
BEFORE(A,B)
SIMULTANEOUS(A,B) only when actually established
```

Metric data, when required, attaches separately to an edge/anchor.

### Strengths

- directly matches current `caused_by_event_ids` / `after_event_ids` semantics;
- preserves incomparability naturally;
- easy to explain/debug;
- cross-scene reconciliation can add one sparse bridge edge;
- no global clock/frontier required;
- causal history survives independent storage order.

### Weaknesses

- metric due/deadline questions require extra structures anyway;
- naive reachability can become unbounded as history grows;
- graph transitivity/compaction needs summary/index strategy;
- genuine intervals/process overlap are awkward if represented only as point events;
- local scene chains can produce many redundant edges.

### Failure mode

If every chronology query becomes graph reachability over retained history, the model violates bounded hot-path/recovery requirements.

### Assessment

Strong semantic foundation, insufficient alone.

## 7. Alternative B — Scene-local logical clocks + sparse cross-scene edges

### Model

Each scene/chronology domain owns a monotonically increasing local coordinate:

```text
(scene A, 41)
(scene A, 42)
(scene B, 9)
```

Within one scene, coordinate order establishes local event order. Cross-domain edges explicitly relate coordinates/events when material.

### Strengths

- very cheap local comparisons;
- compact local frontier/index;
- easy to identify newest relevant local event;
- good fit for ordinary scene-local progression;
- local sequence can compact long chains.

### Weaknesses

- sequence can silently become fictional time even where a user interaction contains unordered/parallel native edges;
- scope migration/rollover/scene split needs careful semantics;
- numeric values across domains are incomparable and easily misused;
- requires a stable coordinate owner/lifecycle;
- vector-clock temptation appears when many scenes interact.

### Failure mode

A convenient local sequence becomes treated as authoritative duration or cross-scene order, recreating the global-frontier problem in smaller pieces.

### Assessment

Useful as a scope-local convenience/index when explicitly nonmetric and owner-scoped; unsafe as the primary chronology authority.

## 8. Alternative C — Temporal anchor / interval constraint network

### Model

Represent relevant temporal points/intervals with exact or bounded relationships:

```text
T(B) - T(A) >= 10 min
T(B) - T(A) <= 20 min
A before B
X overlaps Y
```

Derive order/due results via constraint reasoning.

### Strengths

- excellent for races, travel, deadlines, rituals, recovery windows;
- precise distinction between known bounds and false exactness;
- natural support for `INDETERMINATE` when permitted intervals overlap;
- supports recovery of quantitative decisions from retained evidence;
- can encode approximate time rigorously where truly needed.

### Weaknesses

- much more machinery than ordinary D&D chronology needs;
- risk of forcing narrative descriptions into numeric ranges;
- constraint propagation over large connected networks can become expensive;
- difficult schema/observability burden;
- still needs causal semantics separate from metric consistency.

### Failure mode

HDM becomes a temporal CSP engine and starts inventing/maintaining precision merely because the model supports it.

### Assessment

Excellent **local quantitative submodel**, poor universal chronology representation.

## 9. Alternative D — Owner-local temporal evidence only / reconciliation on demand

### Model

No first-class chronology fabric beyond native owners/events. Each owner stores the anchors/relations it needs. Cross-scene operations inspect the specific owners and derive whatever relation is needed at the moment.

### Strengths

- maximum YAGNI/minimum persistent machinery;
- semantic evidence stays near its consumer/owner;
- no universal frontier or chronology database;
- ordinary local play is cheap.

### Weaknesses

- multiple consumers may duplicate the same cross-scene relation;
- long-range causal dependencies become hard to discover boundedly;
- after original owner compaction, shared evidence may disappear;
- cross-scene reconciliation risks repeated reconstruction/history scans;
- debugging chronology contradictions across owners is harder.

### Failure mode

A later cold runtime cannot boundedly prove a relation because the only evidence was implicit across several owners or discarded with a no-longer-active source.

### Assessment

Good default locality rule but insufficient as the complete persistence architecture.

## 10. Alternative E — Hybrid sparse constraint fabric

### Model

Use different representations only for the relation they are good at:

```text
1. Native owner/event relation evidence
   caused_by / after / accepted causal provenance

2. Optional scope-local nonmetric coordinate/index
   scene-local ordering convenience, explicitly domain-scoped

3. Sparse cross-domain bridge constraints
   explicit causal/precedence/reconciliation anchors

4. Typed metric temporal context
   current coordinate + exact/bounded elapsed evidence only where mechanics need it

5. Optional qualitative relation
   simultaneous/overlap/relative landmark only where materially established

6. Derived bounded indexes/summaries
   retrieval/reachability acceleration; never authority
```

No global chronology scalar or vector over all scenes is required.

### Strengths

- matches actual heterogeneous HDM consumers;
- preserves partial ordering/incomparability;
- keeps quantitative machinery local;
- gives bounded shared evidence for cross-scene recovery;
- can retain compact relation evidence after original timers disappear;
- compatible with live epochs and Step-5 domain typing;
- allows performance indexes without promoting them to authority.

### Weaknesses

- more relation types/contracts than a pure model;
- requires strict typing to prevent representation confusion;
- compaction becomes dependency-aware across causal and metric evidence;
- metric-context ownership must be explicitly designed;
- derived summaries can become hidden authority if contracts are sloppy.

### Failure mode

The hybrid becomes an unprincipled bag of temporal metadata, especially if `world_time.frontier` is retained as a magic shortcut or if local coordinates are used cross-domain.

### Assessment

Currently strongest candidate, contingent on strict owner/type boundaries and a deliberately small relation vocabulary.

## 11. Alternative F — Landmark/epoch chronology with local overlays

### Model

Use durable campaign/world landmarks as coarse chronology epochs:

```text
after siege begins
before coronation
third night of siege
```

Scenes carry local order/metric overlays relative to nearby landmarks. Cross-scene reconciliation first aligns landmarks, then local evidence.

### Strengths

- natural fit for narrative campaigns;
- excellent compression/readability;
- avoids false minute precision;
- can serve long-term history/lore reconstruction cheaply.

### Weaknesses

- landmarks are not guaranteed to exist where mechanics need exact timing;
- selecting landmarks can become LLM/adjudication-dependent and unstable;
- difficult to derive rigorous due/deadline outcomes without separate metric evidence;
- risk that narrative labels become hidden temporal authority without machine semantics.

### Failure mode

A qualitative campaign landmark is treated as sufficient for a quantitative mechanic or two differently interpreted landmarks silently diverge.

### Assessment

Useful presentation/summary layer or typed qualitative anchor family, not sufficient as core chronology.

## 12. Comparative matrix

Ratings: `++` strong, `+` good, `0` mixed, `-` weak, `--` poor.

| Dimension | A Graph | B Local clocks | C Interval/constraints | D Owner-local only | E Hybrid | F Landmarks |
|---|---:|---:|---:|---:|---:|---:|
| Preserve incomparability | ++ | + | + | ++ | ++ | + |
| Causal semantics | ++ | 0 | 0 | + | ++ | + |
| Metric deadlines/races | - | - | ++ | 0 | ++ | - |
| Cheap local hot path | + | ++ | - | ++ | ++ | ++ |
| Bounded cross-scene recovery | + | + | 0/+ | - | ++ | 0 |
| Live-epoch compatibility | + | + | 0 | + | ++ | + |
| Simple schema | + | + | - | ++ | 0 | + |
| Avoid false precision | ++ | + | -/0 | ++ | ++ if gated | ++ |
| Compaction potential | 0 | + | 0 | - | + | ++ |
| Contradiction detection | + | 0/+ | ++ | - | ++ | 0 |
| Risk of hidden global authority | low | medium | medium | low | medium if sloppy | medium |
| LLM/context burden | + | + | - | + | + | ++ |
| Covers all known consumers alone | - | - | - | - | ++ | -- |

## 13. Preliminary synthesis

The alternatives suggest the following separation of concerns rather than one universal chronology representation.

### 13.1 Causal provenance should remain explicit

If B exists because of A, retain a direct stable causal relation owned by the accepted event/execution/history evidence that establishes it.

Do not infer causation from temporal precedence.

### 13.2 Noncausal precedence should be explicit only when future consumers need it

`after_event_ids`-like evidence is useful for synchronization without pretending causal ancestry.

Transitive consequences can be derived within bounded components/indexes; every implied pair does not need materialization.

### 13.3 Local sequence may survive only as scoped convenience evidence

A scene-local monotonic coordinate can make local chronology cheap, but:

```text
(scene_id, sequence)
```

must be semantically interpreted only within that chronology domain and must not imply elapsed duration.

Whether it remains necessary at all should be challenged in the analytical pass.

### 13.4 Metric temporal contexts need explicit owners

A viable metric context contract likely needs to define conceptually:

```text
TemporalMetricContext
    context identity
    unit/scale semantics
    current accepted fictional coordinate/evidence basis
    advancement authority/rules
    recovery source
    relation to scene/process/live ownership
```

However Step 5.9 should avoid creating a generic mutable `world.clock` owner if narrower native contexts suffice.

Candidate context families to test:

```text
scene-local fictional metric context
procedure/process-local metric context
shared/global process metric context where mechanically justified
campaign/world metric context only when the campaign actually establishes one common metric basis
```

A context may be synchronized with another by explicit chronology relation; identity alone does not imply comparability.

### 13.5 Quantitative elapsed evidence is difference evidence, not necessarily current clock state

When a future consumer needs to know that 40–60 minutes elapsed between A and B, the durable semantic fact can be a bounded elapsed relation anchored to A/B/context. It need not require a globally advancing time value forever.

### 13.6 `CURRENT.world_time.frontier` is likely too coarse

The existing scalar-like naming obscures:

- which chronology domains it covers;
- which exact relations are established;
- whether it is an index or authority;
- how independent scenes remain incomparable.

Research recommendation for challenge: retire or radically narrow it unless a concrete bounded consumer proves a typed sparse summary is required.

### 13.7 `scene.chronology_frontier_event_id` may remain only with exact semantics

A single local frontier ID can be useful if it means a local retrieval/index anchor and its relation to prior local evidence is guaranteed by the scene's chronology contract.

It cannot mean “everything before this event is globally ordered/covered.”

### 13.8 Unordered versus indeterminate should be consumer-relative

Absence of a relation means no relation is established. For a consumer:

```text
relation not required
    -> legitimate incomparability / no work

relation required but retained evidence cannot decide
    -> INDETERMINATE / reconcile
```

Persisting explicit `UNORDERED` for every independent pair would be quadratic and unnecessary. Explicit durable non-relation should exist only if a concrete mechanic needs to preserve a stronger statement such as proven simultaneity/concurrency window.

## 14. Recovery implications

A cold runtime should not load a chronology world graph.

For operation O, recover:

```text
native owner/source roots
+ O's explicit chronology dependency refs/anchors
+ bounded indexes/routing to those refs
+ exact/bounded metric context evidence if O requires it
```

Then evaluate only the connected chronology component needed by O.

If required evidence is unavailable:

```text
missing optional/rebuildable index
    -> rebuild/targeted fetch

insufficient valid evidence
    -> INDETERMINATE / bounded reconciliation

contradictory authoritative constraints
    -> chronology integrity defect / CANON_SUSPECT for affected scope
```

No checkpoint age, Git timestamp or host elapsed time fills the gap.

## 15. Live-epoch implications

Each live epoch may carry physical representations of chronology evidence for its claimed scope while semantic relation ownership remains typed.

Normal local live mutation may establish:

- local causal relation;
- local precedence relation;
- metric-context advancement/evidence if the owning context is contained in the live partition;
- references to external chronology anchors read as dependencies.

Cross-live dependency must use a bounded reconciliation/freeze path when it needs to establish a relation that affects both writable scopes.

On absorption:

- accepted chronology evidence moves/persists with its semantic owner/evidence contract;
- live source revision and absorption commit order remain nonchronological;
- local sequence values retain their original domain identity if preserved;
- successor epoch may continue from explicit compatible local chronology basis, not from Git order.

## 16. Compaction implications

Step 5.9 should define semantic compaction safety, not physical deletion.

Evidence E cannot become discardable while any live consumer requires E as the only basis for:

```text
due/not-due decision
quantitative elapsed bound
accepted causal explanation/idempotency dependency
cross-scene precedence
Procedure/Continuation interpretation
process/deadline state
knowledge/lore causal constraint
future required chronology reconciliation
```

Potential safe reduction patterns to challenge:

1. replace a long local chain by a retained typed local coordinate/anchor plus indispensable causal edges;
2. replace several metric difference edges by a derived bounded summary only if the summary has exact declared coverage and original evidence has no independent consumer;
3. retain causal provenance even when intermediate purely-ordering nodes can disappear;
4. never infer deletion safety from event age, event ID magnitude, Git ancestry position or checkpoint age alone.

Physical GC remains Step 5.13.

## 17. Open questions for analytical challenge

1. Does HDM need a first-class `TemporalMetricContext` entity/owner, or can metric current-coordinate ownership remain embedded in scene/process/native owners with a typed context reference abstraction?
2. Does a scene-local sequence provide enough bounded-recovery benefit to justify keeping it?
3. Can causal/precedence edges be owned directly by SemanticEvent/MechanicalEvent records without creating a chronology relation record class?
4. Which quantitative elapsed relations must be durable after both endpoint owners become historical?
5. Is genuine simultaneity a needed first-class relation, or can known overlap/equal-coordinate evidence remain metric/owner-specific?
6. What bounded index/routing is required to avoid graph/history scans without creating a global frontier?
7. Can `CURRENT.world_time.frontier` be deleted entirely?
8. What exact migration maps existing `scene.local_time` narrative strings into typed semantic versus presentation-only data?
9. When a later cross-scene dependency discovers insufficient past precision, what evidence may deterministic adjudication lawfully add versus what remains irreducibly `INDETERMINATE`?
10. What happens when approximate ranges are mutually inconsistent but no exact timestamp ever existed?

## 18. Preliminary ranking

Current research ranking before analytical challenge:

```text
1. E — Hybrid sparse constraint fabric
2. A + D — sparse explicit relations with owner-local default
3. B — local logical coordinates as optional acceleration only
4. C — metric constraint network as local specialist submodel
5. F — landmark anchors as optional qualitative/presentation-compatible evidence
```

This ranking is intentionally provisional.

The strongest alternative to E is not one pure model. It is a **minimal A+D design**: explicit causal/precedence edges only where required, everything else owner-local, with no generic metric-context object unless a concrete mechanic proves need. The analytical challenge must compare E against this simpler baseline aggressively.

## 19. Research conclusion

The evidence does not justify:

- a global campaign clock;
- vector clocks across active scenes;
- a total event sequence;
- a campaign-wide interval constraint solver;
- owner-local-only chronology with no durable bridge evidence.

The likely architecture is a sparse typed combination whose machine law is closer to:

```text
chronology = retained constraints/evidence required by concrete consumers
             + bounded retrieval aids
             - invented order
             - invented precision
```

The next step is analytical challenge. It must attempt to collapse the hybrid into the simpler A+D model and require every additional mechanism — local sequence, metric context, qualitative anchor, sparse reconciliation index — to justify itself independently.
