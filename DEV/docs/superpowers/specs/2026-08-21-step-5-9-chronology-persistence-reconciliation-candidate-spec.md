# Step 5.9 — Chronology Persistence & Reconciliation — Candidate Specification

Status: **CANDIDATE — NONCANONICAL / ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Derivation inputs:

- `2026-08-20-step-5-9-chronology-persistence-reconciliation-task-brief.md`
- `2026-08-20-step-5-9-chronology-persistence-reconciliation-research-draft.md`
- `2026-08-20-step-5-9-chronology-persistence-reconciliation-analytical-challenge.md`
- `2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`
- canonical Steps 3, 4, 5.1, 5.3, 5.7 and 5.8.

Candidate architecture direction:

> **OWNER-ANCHORED SPARSE CHRONOLOGY / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**

This candidate defines the minimum chronology semantics needed for deterministic mechanics, cross-scene reconciliation, recovery and later safe retention. It intentionally does not implement schemas/runtime code and does not create a campaign-global timeline service.

---

# 1. Central model

HDM chronology is sparse accepted evidence over stable chronology anchors.

```text
NATIVE / ACCEPTED ANCHORS
    SemanticEvent
    accepted execution/boundary occurrence where semantically appropriate
    process milestone
    scene/world transition anchor
    other owner-defined stable accepted point
        |
        +--> owner-local causal / precedence evidence
        +--> optional typed metric position / elapsed evidence
        |
        v
SCOPE-LOCAL CHRONOLOGY BASIS
    bounded set of maximal relevant anchors
    optional exact/bounded position in declared metric coordinate system
        |
        | only when scopes become materially related
        v
MATERIAL BRIDGE EVIDENCE
    causal relation
    strict temporal precedence
    bounded elapsed relation
    rare same-coordinate relation
        |
        v
BOUNDED RECONCILIATION
    determinate relation / due result
    INDETERMINATE
    contradiction -> scoped integrity handling
```

Chronology is not one mutable current-state owner. Current scene/process/world state remains with native owners. Temporal obligations remain with Step-5.3 owners. Chronology evidence only establishes relationships or quantitative temporal facts required by concrete consumers.

---

# 2. Governing boundary — forward-extensible accepted history

The owner-approved Step-5.9 boundary is normative input to this candidate.

Baseline chronology assumes accepted history is **forward-extensible**.

Later canon may:

- add new events;
- establish previously unknown relations between stable historical anchors;
- refine previously indeterminate chronology using valid new evidence;
- establish exact/bounded elapsed evidence when materially required;
- correct storage/integrity defects through explicit repair semantics.

Ordinary baseline chronology does not:

- make an already-established cause cease to have happened;
- replace accepted past with another mutable past;
- maintain several simultaneously authoritative branching timelines/worldlines;
- treat causal loops or retrocausal cycles as normal chronology;
- use Git history rewriting as fictional timeline rewriting.

Immutable-history time travel, visions/records of past periods, temporal anomalies, forward jumps, stasis, time dilation and different local temporal rates remain admissible when accepted causal history remains forward-extensible.

If play genuinely requires mutable past / branching authoritative worldlines / causal-loop semantics, baseline HDM exposes a capability boundary rather than silently fabricating support.

---

# 3. Vocabulary

## 3.1 Chronology anchor

A stable accepted point that may participate in chronology relations.

An anchor is normally a typed reference to an already meaningful owner/evidence identity, for example:

```text
SemanticEvent identity
BoundaryOccurrence identity
accepted process milestone identity
accepted scene/world transition identity
other owner-defined stable causal/temporal point
```

Step 5.9 does **not** require a universal mutable `ChronologyAnchor` record for every event or action.

Anchor identity:

- is stable once externally referenced;
- identifies semantic domain/scope where needed;
- does not derive fictional order from lexical/numeric ID order;
- survives recovery as required by still-live references;
- may outlive detailed source payload when compaction safely preserves the required relation/provenance evidence.

## 3.2 Causal relation

`CAUSES(A,B)` says A is accepted causal ancestry/provenance for B.

Causality is not identical to strict metric precedence. A can causally precede B within the same adjudicated temporal coordinate/instant.

Under baseline forward-extensible chronology:

```text
CAUSES(A,B)
    forbids established B STRICT_BEFORE A
```

but does not by itself prove positive non-zero elapsed duration.

## 3.3 Strict temporal precedence

`STRICT_BEFORE(A,B)` says A is fictionally earlier than B in the applicable chronology relation.

It does not assert that A caused B.

The inverse `AFTER` is derived and need not be separately stored when direction is unambiguous.

## 3.4 Same-coordinate relation

`SAME_COORDINATE(A,B,C)` says A and B are established at the same relevant coordinate in metric/chronology context C.

It is positive evidence. It is not inferred merely because no order is known or because two repository writes race.

A causal relation may coexist with same-coordinate evidence when causally ordered subevents occur at one metric coordinate.

No general Allen interval algebra is introduced.

## 3.5 Metric coordinate system

A typed interpretation of numeric temporal coordinates.

Conceptually it defines:

```text
context identity
unit / scale semantics
comparison semantics
allowed transformations/bridges if any
owner/profile interpretation
```

A metric coordinate system is a **ruler**, not a mutable global clock.

It does not own one campaign-wide `current_time`.

## 3.6 Scope position

Accepted current/anchor-local position evidence for a specific chronology scope in a declared metric coordinate system.

Conceptual forms:

```text
EXACT(v)
BOUNDED(lo, hi)     # inclusive, lo <= hi
UNKNOWN
```

A scope position belongs to the applicable native scene/process/procedure/other temporal scope contract, not to a generic global clock object.

## 3.7 Elapsed bounds

Quantitative relation between stable anchors:

```text
ELAPSED(A,B,C,[lo,hi])
```

meaning that in metric context C, accepted elapsed quantity from A to B lies inside the established bounds.

Exact elapsed is the degenerate case `lo == hi`.

Elapsed evidence is established only when mechanics/fiction actually justify the quantity. Narrative descriptions are not silently converted to invented ranges.

## 3.8 Material bridge

A persisted causal/temporal relation that connects previously independent chronology scopes because a concrete accepted dependency now makes the relation matter.

Examples:

```text
CAUSES(A3,B4)
STRICT_BEFORE(A3,B4)
ELAPSED(A3,B4,C,[15,25])
SAME_COORDINATE(A3,B4,C)
```

Material bridges are sparse. HDM does not continuously reconcile every active scene pair.

## 3.9 Scope-local maximal-anchor frontier

For chronology scope S:

```text
LocalFrontier(S)
    = bounded set of maximal currently relevant chronology anchors
```

The common serial case has one member.

A same-scope contested/parallel case may temporarily have several maximal anchors.

The frontier is typed retrieval/extension/recovery evidence. The authoritative chronology relation remains the accepted anchor/relation evidence from which the frontier is justified.

---

# 4. Core laws

## LAW 5.9-1 — NO STORAGE ORDER AS FICTIONAL ORDER

Git commit/ref ancestry, live CAS winner order, file order, host/network timing, SemanticEvent ID allocation and traversal order SHALL NOT establish fictional chronology unless a specific owning chronology contract separately establishes an equivalent semantic relation.

## LAW 5.9-2 — INDEPENDENT SCOPES MAY REMAIN INCOMPARABLE

Two accepted chronology scopes/events need no relative fictional order while no material dependency requires one.

HDM SHALL NOT totalize independent history for bookkeeping.

## LAW 5.9-3 — NO GLOBAL CURRENT WORLD CLOCK

Baseline HDM has no mandatory mutable campaign-global `current_world_time` authority.

Several scopes may use one shared metric coordinate system while owning different current positions.

## LAW 5.9-4 — NO GENERIC GLOBAL CHRONOLOGY FRONTIER

No one scalar/event ID/global sequence represents complete campaign chronology progress.

Any future campaign-level chronology summary/index SHALL declare exact typed coverage and remain derivative retrieval evidence.

`CURRENT.world_time.frontier` as a generic globally reconciled frontier is noncanonical implementation debt.

## LAW 5.9-5 — CHRONOLOGY DOES NOT OWN WORLD STATE OR TEMPORAL OBLIGATIONS

World/scene/process/mechanical current state remains with native owners.

Effect/Resource/LifeState/Procedure/etc. temporal obligations remain with Step-5.3 owners.

Chronology supplies evidence needed to compare/advance them; it does not become a scheduler, Agenda, job queue, deadline owner or alternate current-state snapshot.

## LAW 5.9-6 — RELATION EVIDENCE HAS ONE ACCEPTED SEMANTIC SOURCE

A material chronology relation SHALL have stable accepted evidence sufficient to explain what relation was established and by what accepted transition/evidence basis when provenance matters.

The same semantic relation may be indexed/embedded in multiple derived forms, but no second writable relation authority is created.

## LAW 5.9-7 — CAUSALITY AND STRICT TIME ORDER REMAIN DISTINCT

`CAUSES(A,B)` preserves provenance and causal ancestry.

`STRICT_BEFORE(A,B)` preserves strict fictional temporal precedence without claiming cause.

A derived temporal implication SHALL NOT erase unique causal provenance.

## LAW 5.9-8 — UNKNOWN ORDER IS NOT SIMULTANEITY

Absence of a proven order does not establish `SAME_COORDINATE`, simultaneity or overlap.

No generic persistent `UNORDERED(A,B)` relation is required.

When a consumer requires an order and retained evidence cannot establish one, result is `INDETERMINATE` / typed reconciliation-adjudication requirement as appropriate.

## LAW 5.9-9 — PRECISION IS CONSUMER-DRIVEN

Exact/bounded numeric time is persisted only where a mechanic, causal race, deadline, recovery predicate, cross-scope dependency or retained future consumer requires it.

Do not timestamp every event or convert qualitative labels to metric ranges merely because a conversion can be invented.

## LAW 5.9-10 — ACCEPTED QUANTITATIVE EVIDENCE MAY OUTLIVE THE ORIGINAL TIMER

Established elapsed/metric evidence cannot be discarded merely because the Effect/process/timer that first required it has settled when another still-live or promised consumer retains a semantic dependency on that evidence.

## LAW 5.9-11 — RECONCILIATION MATERIALIZES MINIMUM NECESSARY NEW EVIDENCE

A cross-scope operation adds only relations needed for the accepted current dependency and future promised correctness.

One bridge does not require pairwise total ordering of the histories behind both endpoints.

## LAW 5.9-12 — LATE-ESTABLISHED RELATIONS DO NOT REWRITE OLD EVENTS

SemanticEvents/accepted history remain append-only under ordinary operation.

If a relation between already-existing anchors becomes established later, the new accepted transition/evidence SHALL carry an immutable typed relation assertion/evidence reference rather than mutating the historical identity/meaning of old records in place.

## LAW 5.9-13 — NO MANDATORY CHRONOLOGY DATABASE

Step 5.9 requires stable referencable relation evidence, not a central mutable timeline service.

A relation may be represented:

- directly on the accepted event/owner record that establishes it;
- as an embedded immutable chronology assertion value on a later accepted event/evidence record;
- as a compact immutable relation artifact when independent retention/reference is mechanically justified.

Physical representation must preserve one semantic source and bounded discovery.

## LAW 5.9-14 — LOCAL SEQUENCE IS NOT BASELINE AUTHORITY

`world_order.sequence`, source revision counters and similar numeric values do not become fictional chronology merely because they are monotonic.

An owner may define a scoped chronology coordinate with explicit semantic meaning; otherwise such values are retrieval/debug/storage metadata only.

## LAW 5.9-15 — LOCAL FRONTIER MAY BE MULTI-ANCHOR

A chronology scope is not assumed linear.

`chronology_frontier_event_id` as a mandatory singleton semantic frontier is insufficient for general partial-order cases.

The canonical concept is a bounded maximal-anchor set, with singleton optimization permitted.

## LAW 5.9-16 — SEMANTIC JOIN MAY COLLAPSE FRONTIER WITHOUT ORDERING ITS INPUTS

If a new accepted anchor J is genuinely established after every anchor in current set `{A1...An}`, then relations:

```text
A1 < J
...
An < J
```

may make `{J}` the new local maximal frontier without establishing any relative order among A1...An.

A synthetic fictional join SHALL NOT be invented solely to reduce metadata. A join requires a real accepted semantic boundary/event/state transition for which "after all inputs" is true.

## LAW 5.9-17 — METRIC CONTEXT IS A RULER; SCOPE OWNS POSITION

`TemporalBinding.metric_deadline.context_id` identifies metric interpretation/comparison context.

It SHALL NOT be interpreted as implicit ownership of one mutable `context.current_time` unless an explicit specialized owner contract later defines that behavior.

Current/anchor position evidence belongs to the relevant chronology scope/provider.

## LAW 5.9-18 — METRIC COMPARISON IS TYPE-checked

Numeric coordinates are comparable only when:

- they are expressed in the same compatible metric coordinate system; or
- explicit deterministic bridge/rebase evidence establishes a valid transformation.

Same numeric values in different contexts are not implicitly comparable.

## LAW 5.9-19 — BOUNDED POSITION PRESERVES UNCERTAINTY

When accepted evidence only establishes `[lo,hi]`, HDM SHALL NOT select an arbitrary scalar inside the range for deterministic convenience.

For scalar deadline D in the same context:

```text
hi < D   -> NOT_DUE
lo >= D  -> DUE
otherwise -> INDETERMINATE
```

Equivalent owner-defined comparisons may exist for other registered temporal predicates.

## LAW 5.9-20 — QUALITATIVE TIME DOES NOT IMPLY METRIC BOUNDS

Labels such as `night`, `after the council`, `third day of the siege` or `before coronation` remain qualitative chronology/presentation evidence unless a specific accepted world/rule contract establishes quantitative interpretation.

## LAW 5.9-21 — TEMPORAL REBASING MUST PRESERVE THE FEASIBLE SET

When a temporal owner/scope moves between coordinate contexts, the owning transfer/reconciliation contract may:

- preserve the original anchor/context and use bridge evidence; or
- deterministically rebase into the destination context.

Rebasing is legal only when it preserves the accepted exact/bounded semantics and provenance needed by the owner. It may not tighten uncertainty or invent a scalar from a range.

## LAW 5.9-22 — NO ARBITRARY RETROACTIVE TOTALIZATION

Later reconciliation may add relations logically established by new accepted evidence.

It may not choose one of several compatible historical orders merely because one is convenient, dramatic or cheaper.

If a current mechanic requires a unique relation that retained evidence cannot lawfully establish, return `INDETERMINATE` / typed adjudication boundary instead of fabricating recovered history.

## LAW 5.9-23 — CONTESTED ACTIONS USE MECHANICS, NOT TRANSPORT RACES

When two actions are fictionally simultaneous/contested and order determines outcome, Step-3/game-rule adjudication establishes the accepted result/order as required.

CAS/storage winner order cannot substitute for fictional adjudication.

Persist only the chronology evidence future correctness actually requires from that adjudication.

## LAW 5.9-24 — FORWARD-EXTENSIBLE STRICT ORDER IS ACYCLIC

Accepted `STRICT_BEFORE` relations form an acyclic relation under baseline chronology.

A persisted strict-order cycle is a chronology integrity defect, not evidence for time travel.

## LAW 5.9-25 — BASELINE CAUSAL ANCESTRY IS ACYCLIC

Accepted causal ancestry SHALL NOT require causal cycles/retrocausal loops under baseline chronology.

A persisted causal cycle after targeted validation is outside the baseline capability and/or an integrity defect according to how it arose; it is not silently normalized.

## LAW 5.9-26 — CONTRADICTION IS NOT INDETERMINACY

Examples of contradiction include:

```text
A STRICT_BEFORE B
B STRICT_BEFORE A

A SAME_COORDINATE B in C
A STRICT_BEFORE B in the same applicable coordinate relation

ELAPSED(A,B,C) <= 5
ELAPSED(A,B,C) >= 10

CAUSES(A,B)
B STRICT_BEFORE A
```

when no explicit compatible temporal model makes the claims semantically distinct.

Missing comparison evidence/context compatibility yields `INDETERMINATE`, not corruption.

---

# 5. Canonical evidence placement

## 5.1 Relation known when accepted event/owner transition is created

Prefer owner-local/event-local evidence.

Current useful examples remain:

```text
SemanticEvent.caused_by_event_ids
SemanticEvent.after_event_ids
```

These fields may continue representing direct accepted causal/precedence relations where their endpoint semantics are sufficient.

Do not duplicate the same relation into a second mutable chronology record merely for normalization.

## 5.2 Relation established later

Suppose old accepted anchors A and B exist, and later accepted event/evidence E establishes that A strictly preceded B.

Ordinary operation SHALL NOT rewrite B.

Instead E (or another compact immutable evidence artifact justified by E) records a typed assertion conceptually equivalent to:

```text
relation_id / stable assertion identity if externally needed
relation_type = STRICT_BEFORE
left_anchor = A
right_anchor = B
established_by = E
supporting_refs = bounded accepted evidence as required
```

Likewise for late causal or elapsed relations.

## 5.3 Derived transitive facts

If:

```text
A < B
B < C
```

then a query may derive `A < C` without persistently materializing a third canonical relation unless:

- bounded future recovery/query cost requires a summary; and
- the summary has explicit coverage/provenance semantics; and
- it remains derivative rather than a second source of truth.

## 5.4 Relation evidence and source payload compaction

A stable chronology relation may outlive detailed narration/event payload.

If physical compaction extracts minimum relation/provenance evidence into a compact retained form, the transition must preserve stable relation identity/reference semantics for every still-live consumer.

Step 5.9 defines semantic safety; Step 5.13 owns physical deletion/GC.

---

# 6. Metric coordinate contract

## 6.1 Coordinate systems are typed

Conceptually each admitted metric context establishes:

```text
context_id
unit_id
ordered numeric domain / deterministic comparison
scope applicability / interpretation
optional admitted bridge/rebase rules
```

The baseline does not require one context for every campaign.

A normal campaign/profile MAY use a common world elapsed-time coordinate system as a convenience, but correctness SHALL NOT depend on its existence.

## 6.2 Position providers are native

A scene/process/procedure/other temporal scope that supports metric comparison exposes accepted current/anchor position evidence in the relevant context through its owning contract.

Examples:

```text
Scene A -> C @ EXACT(720)
Scene B -> C @ BOUNDED(700,735)
Process P -> process-local metric context @ EXACT(4 stages/minutes/etc as defined)
```

The exact persistence field belongs to machine realization. No generic mutable context owner is mandated.

## 6.3 Monotonicity is scope/context-specific

A given owner contract may guarantee nondecreasing position within one chronology episode/context.

HDM SHALL NOT infer campaign-global monotonicity across:

- independent scenes;
- incompatible coordinate contexts;
- time-dilated planes;
- separate chronology episodes;
- unsupported mutable-history semantics.

## 6.4 Elapsed evidence may bridge positions without persistent rate machinery

Time dilation or different temporal rates do not require a universal affine-conversion subsystem.

When a boundary/cross-scope mechanic establishes a quantitative relation, persist the exact/bounded elapsed/offset evidence needed by concrete consumers.

A generic permanent rate function is introduced only if a real registered mechanic later requires it.

---

# 7. Scope-local chronology and frontier semantics

## 7.1 Ordinary local extension

For a typical serial scene:

```text
frontier = {A}
accept B after A
frontier = {B}
```

The accepted relation may be causal, strict precedence, or another owner-defined local chronology step as actually established.

No global state changes solely because this local event happened.

## 7.2 Parallel/contested local anchors

If two accepted events share a scene/scope but no fictional order is established:

```text
frontier = {A,B}
```

Repository serialization does not collapse this to one semantic order.

## 7.3 Semantic convergence

When accepted J genuinely follows both:

```text
A < J
B < J
```

then:

```text
frontier = {J}
```

without establishing A-vs-B order.

## 7.4 Frontier boundedness

A frontier is bounded by the practical current chronology/mutation scope and owner decomposition.

If independent same-container activity would cause unbounded frontier growth, the architecture should first ask whether those activities are actually separate chronology scopes/process owners rather than inventing a global vector or artificial fictional joins.

Implementation MAY materialize compact typed maximal-anchor indexes where needed for hot path/recovery.

A missing/stale derivative frontier may require bounded repair; it does not rewrite canonical relation evidence.

---

# 8. Cross-scope reconciliation protocol

A material operation needing relation between scopes A and B proceeds conceptually:

```text
1. identify concrete chronology predicate/query
2. exact-pin current participating native sources under Steps 5.7/5.8
3. load endpoint anchors + directly required relation/metric evidence
4. follow only bounded dependency/summary refs needed by the predicate
5. derive relation if entailed
6. if new accepted transition itself establishes a relation, materialize minimum relation evidence in that transition
7. if evidence is insufficient -> INDETERMINATE / typed adjudication boundary
8. if accepted evidence is contradictory -> scoped integrity handling
```

Examples:

### Cross-scene message

```text
A3 = message sent/knowledge established
B4 = message received

CAUSES(A3,B4)
```

No requirement to order A1/A2 against B1/B2/B3 unless another consumer requires it.

### Rendezvous/race

Load only relevant departure/arrival/deadline anchors and metric evidence. Increase precision only enough to determine result.

### Shared process

If process stage depends on event X from another scene, retain explicit dependency/bridge to X rather than reconciling all scene history.

---

# 9. Due evaluation integration with Step 5.3

Chronology supplies evidence; native temporal owner remains authority.

For `TemporalBinding.metric_deadline`:

```text
binding:
    context C
    deadline D

owner/applicable scope-position provider:
    position P in C

compare(P,D)
    -> NOT_DUE | DUE | INDETERMINATE
```

Cold recovery must restore enough current native position/bridge evidence to reproduce the lawful result.

If the owner moves to another scope/context:

- preserve original context + bridge; or
- safely rebase under LAW 5.9-21.

No due result is stored as generic chronology authority.

Procedure/semantic boundary TemporalBindings continue using their owner/boundary identities rather than being forced into numeric metric time.

---

# 10. Live-epoch integration

## LAW 5.9-27 — LIVE SOURCE ORDER IS NOT FICTIONAL ORDER

Step-5.8 source revision/CAS order remains concurrency evidence only.

Two independent live epochs remain chronologically incomparable until accepted semantic evidence connects them.

## LAW 5.9-28 — LIVE TRANSITIONS MAY ESTABLISH CHRONOLOGY EVIDENCE

An accepted live native durability edge may establish anchors/relations/metric evidence required by its semantic transition.

That chronology evidence participates in the same accepted live source authority/recovery semantics as the native owners it describes.

## LAW 5.9-29 — CLOSE DOES NOT ADVANCE FICTION

`ACTIVE -> CLOSED`, campaign absorption, branch cleanup and successor opening are technical authority/persistence transitions.

They SHALL NOT create fictional elapsed time/order merely by occurring.

## LAW 5.9-30 — ABSORPTION PRESERVES CHRONOLOGY IDENTITY

Forward absorption must preserve stable chronology anchor/relation identity and required metric evidence from the live source.

Absorption order between independent epochs does not impose fictional order.

## LAW 5.9-31 — SUCCESSOR INHERITS SEMANTIC SCENE BASIS, NOT GIT ORDER

If a live scene continues through rollover, the successor's current scene chronology basis is the absorbed scene's accepted maximal-anchor/position evidence.

Opening the successor is not itself a fictional event.

## LAW 5.9-32 — MULTI-SCOPE FREEZE IS NOT PARTIAL FICTION

When Step 5.8 freezes multiple epochs for a shared transition, partial technical freeze preserves each scope's pre-transition chronology state.

Only the later accepted shared semantic transition adds cross-scope chronology bridges/order/metric evidence.

---

# 11. Recovery and bounded discovery

## LAW 5.9-33 — RECOVERY DOES NOT REBUILD A GLOBAL TIMELINE

Cold recovery follows Step-5.7 current authority/routing and hydrates chronology evidence required by recovered active owners/scopes.

No full LOG/history load or campaign-wide chronology reconstruction is required.

## LAW 5.9-34 — LIVE TEMPORAL CONSUMER HAS BOUNDED EVIDENCE ROUTE

Every still-live temporal/causal consumer that requires chronology after recovery SHALL retain/directly route to sufficient evidence or typed retrieval summaries to answer its admitted predicates boundedly.

Examples:

```text
Effect -> TemporalBinding -> context + applicable scope position/bridge
Process -> prerequisite/elapsed anchor refs
Continuation/Procedure -> pinned boundary/causal dependencies
scene -> local maximal-anchor frontier/index as needed for bounded extension
```

## LAW 5.9-35 — DERIVED CHRONOLOGY INDEXES MAY REBUILD

Reachability caches, maximal-anchor indexes, shared-anchor lookup maps and other derived structures may be rebuilt when their owner contract gives a bounded source.

They do not become relation authority.

If a particular index is required to prevent unbounded discovery, its enrollment/update joins the applicable native durability closure analogously to other correctness-critical routing evidence while remaining derivative.

---

# 12. Integrity semantics

Chronology validation is bounded to the touched/relevant connected component.

Potential result classes:

```text
VALID / relation established
INDETERMINATE / insufficient or incomparable evidence
CANON_SUSPECT / possible persisted contradiction after targeted current refresh
CANON_CORRUPT / confirmed incompatible persisted chronology evidence under INTEGRITY contract
UNSUPPORTED_TEMPORAL_MODEL / genuinely requires mutable-past/branching/causal-loop semantics
```

Exact user-facing names may be normalized later; semantic distinctions are required.

Do not classify these as corruption:

- independent scopes without order;
- missing optional exact timestamp;
- different metric contexts without bridge;
- broad position range crossing a deadline;
- stale derivative frontier before refresh/repair;
- technical live close/absorption occurring in another order than fiction.

Do classify incompatible current accepted evidence as suspect after bounded refresh, including strict cycles, empty metric feasible sets, impossible direct endpoint contradictions and missing required relation anchors.

---

# 13. Compaction / retention eligibility

Step 5.9 defines semantic eligibility only. Step 5.13 owns physical deletion/GC.

## LAW 5.9-36 — LIVE CONSUMER DECIDABILITY MUST SURVIVE COMPACTION

Chronology evidence is compaction-eligible only if every still-live or explicitly promised retained consumer remains lawfully decidable from retained evidence with the same admitted semantic answer set.

Do not preserve merely today's answer while weakening evidence needed by another future admitted predicate.

## LAW 5.9-37 — UNIQUE CAUSAL PROVENANCE IS NOT REPLACED BY PRECEDENCE

If `CAUSES(A,B)` is independently meaningful provenance, deriving `A < B` elsewhere does not make the causal evidence disposable.

## LAW 5.9-38 — METRIC SUMMARY MUST PRESERVE FEASIBLE RELATIONS

Replacing quantitative evidence with a summary is safe only if every still-live promised consumer retains the same feasible exact/bounded relation set needed by its contract.

A wider interval is not equivalent merely because one current deadline result happens to remain unchanged.

## LAW 5.9-39 — DERIVED REDUNDANT EDGES MAY BE DROPPED WHEN SEMANTICALLY LOSSLESS

A derived/redundant precedence edge may become compaction-eligible when retained evidence still proves the same required relation and the removed edge carries no unique causal/provenance/identity meaning.

No full campaign transitive reduction is required.

## LAW 5.9-40 — FRONTIER/INDEX COMPACTION DOES NOT DELETE SOURCE RELATIONS BY ITSELF

Dropping/rebuilding a derived frontier or retrieval index is separate from deciding whether canonical relation evidence may be discarded.

---

# 14. Current runtime/schema disposition

This candidate intentionally separates architecture from machine realization, but the following current fields are classified for later implementation planning.

## Keep/refine

```text
SemanticEvent.caused_by_event_ids
    keep causal semantics

SemanticEvent.after_event_ids
    keep strict/noncausal precedence semantics; exact naming may be refined

world_order.scene_id
    useful chronology-domain tag where appropriate

scene.local_time
live.local_time
    may survive only with explicit split between semantic typed position/evidence and presentation label
```

## Retire as generic authority

```text
CURRENT.world_time.frontier
    retire as generic global chronology frontier

CURRENT.world_time.display
    presentation only; no correctness authority

world_order.sequence
    not baseline chronology authority unless an owner explicitly defines scoped chronology-step semantics

scene.chronology_frontier_event_id
    replace semantic singleton assumption with typed maximal-anchor-set concept
```

## New machine concepts likely required later

Not yet exact schemas/classes:

```text
typed chronology anchor reference
immutable chronology relation assertion/evidence value
scope-local maximal-anchor refs/index
metric coordinate-system identity/metadata
exact/bounded scope-position evidence
bounded elapsed relation evidence
bounded relation lookup/routing where direct refs are insufficient
```

No implementation is authorized by this candidate.

---

# 15. Dramaturg / LLM boundary carry-forward

Step-4 Dramaturg remains noncanonical preparation.

The owner-approved forward-extensible boundary creates an eventual policy constraint:

> Dramaturg does not deliberately prepare baseline campaign premises/developments whose correctness requires mutable past, branching authoritative timelines or causal-loop chronology unless a future explicit temporal extension is selected.

Dramaturg may freely use temporal themes compatible with baseline semantics: deadlines, historical mysteries, immutable-history time travel, time dilation, prophecies, forward jumps, independent scenes and temporal anomalies that do not rewrite accepted causal history.

No LLM role becomes chronology authority. Accepted chronology evidence crosses the normal deterministic validation/promotion boundary.

---

# 16. Difficult supported scenarios

## 16.1 Global countdown

Many scopes may reference one common metric coordinate system/deadline.

Each scope retains its own accepted position evidence. More actions may require quantitative evidence/reconciliation, but no global mutable `now` is introduced.

## 16.2 Dense synchronized multi-scene operation

Frequent material bridges may make the affected connected component denser and therefore more expensive.

Correctness still uses sparse accepted relations + bounded affected-component reconciliation. If measurements later prove repeated arbitrary comparisons dominate cost, a derived summary/index optimization may be introduced without changing semantic authority.

No vector clock is introduced preemptively.

## 16.3 Different planar temporal rates

Use separate or shared metric contexts plus exact/bounded bridge evidence at relevant transitions.

Unknown conversion legitimately yields `INDETERMINATE` for predicates that require it.

No permanent global rate-conversion engine is required unless a concrete mechanic proves need.

## 16.4 Historical mystery

A later accepted discovery may establish a relation between old anchors via new immutable relation evidence without rewriting old events.

## 16.5 Immutable-history visit to the past

The visited period is represented through an appropriate chronology scope/context while accepted history remains self-consistent and forward-extensible in causal evidence.

The baseline does not support actions that replace already-established past outcomes.

---

# 17. Performance requirements

Ordinary local action target:

```text
O(local owner/frontier/direct chronology dependencies)
```

Material cross-scope action target:

```text
O(bounded affected relation/evidence component)
```

Not allowed on ordinary turns:

```text
O(all campaign events)
O(all active scenes)
full chronology graph reconstruction
global vector refresh
campaign-wide temporal CSP solve
continuous world-clock simulation
```

A future derived index is justified only by a measured/query requirement and must preserve source-evidence authority.

---

# 18. Assumptions / risks

## ASSUMPTION A — ordinary HDM cross-scope chronology remains sparse enough

Confidence: HIGH.

Evidence: current runtime design and regression cases treat cross-scene synchronization as material/rare rather than every-turn global activity.

If false: dense synchronized campaigns may need additional derivative chronology summaries/indexes; this does not automatically require a new semantic model.

## ASSUMPTION B — stable accepted anchors are available for material temporal relations

Confidence: HIGH.

Step 3/5.3 already require stable execution/event/boundary identities for causal/idempotent continuity.

If false for a new owner class: that owner must define stable anchor identity before participating in persisted chronology.

## ASSUMPTION C — exact/bounded scalar metric evidence covers current baseline quantitative needs

Confidence: MEDIUM-HIGH.

Current consumers are durations, deadlines, travel/races and process elapsed time. No current requirement proves need for full interval algebra or general non-linear conversion.

Revisit trigger: a registered baseline mechanic requires a temporal relation not faithfully representable by anchor order + exact/bounded elapsed evidence.

## ASSUMPTION D — forward-extensible accepted history is acceptable baseline product semantics

Status: OWNER-APPROVED boundary.

Mutable past / branching worldlines / causal-loop semantics require explicit future architecture extension.

---

# 19. Explicit non-goals / rejected baseline mechanisms

No baseline requirement for:

```text
universal current world clock
global chronology sequence
generic global frontier
vector timestamps across scenes
full Allen interval algebra
general campaign temporal CSP solver
mandatory timestamp on every event
generic persisted UNORDERED relation
central mutable chronology service
history scan on ordinary action
background fictional-time advancement
mutable-past / branching-worldline engine
```

---

# 20. Candidate exit claims requiring adversarial review

Before canonicalization the review must attempt to falsify at least:

1. direct + late relation evidence can remain one-authority without central chronology DB;
2. maximal-anchor frontiers remain bounded/recoverable under contested and long-running local parallelism;
3. semantic joins cannot accidentally invent ordering;
4. exact/bounded metric scope positions reproduce Step-5.3 due results after recovery;
5. TemporalBinding movement/rebase cannot lose or tighten uncertainty;
6. cross-live absorption/rollover preserves chronology without Git-order contamination;
7. partial multi-scope freeze does not create phantom fictional order;
8. dense cross-scene campaigns degrade in cost rather than correctness;
9. time dilation/global countdown remain representable without one global mutable now;
10. late historical relation establishment works with append-only SemanticEvents;
11. compaction rules preserve causal provenance and future temporal predicates;
12. contradiction detection remains bounded and distinct from legitimate incomparability;
13. forward-extensible boundary cleanly catches mutable-past/branching/causal-loop cases rather than corrupting baseline history;
14. LLM/Dramaturg cannot silently introduce unsupported temporal semantics as canon.

Candidate status remains noncanonical until adversarial review and resolution gate close these claims.