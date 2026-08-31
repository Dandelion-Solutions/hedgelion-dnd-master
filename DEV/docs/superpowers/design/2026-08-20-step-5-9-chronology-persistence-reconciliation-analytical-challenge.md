# Step 5.9 — Chronology Persistence & Reconciliation — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NONCANONICAL**

Date: 2026-08-20

Inputs:

- `2026-08-20-step-5-9-chronology-persistence-reconciliation-task-brief.md`
- `2026-08-20-step-5-9-chronology-persistence-reconciliation-research-draft.md`

## 1. Challenge purpose

This pass attacks the preliminary hybrid preference and attempts to reduce Step 5.9 to the simplest architecture that still satisfies all known HDM consumers.

The challenge specifically asks whether any of the following can be removed:

- first-class chronology graph machinery;
- scene-local sequence coordinates;
- metric context objects;
- quantitative interval constraints;
- globally reconciled summaries/frontiers;
- qualitative chronology relations beyond cause/precedence.

The target is not theoretical completeness. It is the smallest deterministic recoverable chronology model that works for HDM.

## 2. Strongest case for one global campaign clock

### Argument

A single world clock appears attractive because most D&D durations, travel, rests, deadlines and world processes conceptually happen in one fictional world. If every event has a common timestamp:

```text
current_world_time
+ event timestamps
+ deadline timestamps
```

then due evaluation, races, scene synchronization, recovery and debugging become straightforward.

It would also make `CURRENT.world_time` and `TemporalBinding.metric_deadline` easy to explain.

### Strongest operational benefit

The hardest chronology query becomes arithmetic rather than graph/constraint reasoning.

### Counterargument

The architecture already admits independently advancing multiplayer scenes. One mutable global `current_world_time` must then do one of three bad things:

1. advance with one scene and silently advance every unrelated scene;
2. refuse independent scene advancement;
3. become a set/range/vector of scene positions, at which point it is no longer one current clock.

A scalar clock also pressures the engine to invent precise elapsed time for ordinary scenes simply to keep them synchronized.

### Resolution

Reject **one global current fictional clock**.

However, preserve a weaker useful concept:

> Multiple scopes may use the same explicitly declared **metric coordinate system** without sharing one mutable current coordinate.

Example:

```text
coordinate system: world fictional elapsed minutes from campaign epoch

scene A position: [600, 610]
scene B position: 735
```

The shared axis makes coordinates comparable when evidence is sufficient; the current positions remain scope-owned.

This captures the useful half of a world clock without global-now authority.

## 3. Strongest case for pure sparse graph chronology

### Argument

Cause and precedence are fundamentally graph relations. Current schema already has causal/after references. Independent scenes remain disconnected. Cross-scene interactions add sparse bridge edges. No clock is required.

### Counterexample

A mechanic says:

```text
Effect expires 60 fictional minutes after A.
```

A later state establishes only:

```text
B after A
```

A graph proves order but not elapsed duration. A separate quantitative mechanism is unavoidable.

Adding duration weights/ranges to graph edges simply turns the relevant connected component into a temporal constraint network.

### Resolution

Pure graph-only is insufficient.

Retain explicit causal/precedence relation evidence as one layer, not the whole chronology model.

## 4. Strongest case for pure interval/constraint chronology

### Argument

Represent every relevant event as a temporal variable and every relation as a constraint. Cause implies precedence; approximate time is a bound; simultaneity and races are naturally expressible. A temporal constraint solver can answer all chronology questions.

### Counterargument

Causality is not merely an inequality. `A caused B` has gameplay provenance semantics that must survive even when timing is compacted or many different temporal assignments satisfy the same order.

Further, most HDM events do not need numeric time variables. Creating them anyway increases persistence and reasoning cost and invites false precision.

### Resolution

Reject universal temporal-CSP representation.

Retain difference/bound constraints only inside metric-context components when a concrete consumer requires quantitative elapsed reasoning.

## 5. Strongest case for vector-clock-like scene chronology

### Argument

Independent scenes resemble distributed processes. Vector timestamps would preserve causal order and detect concurrency without total ordering. Cross-scene communication naturally merges vectors.

### Counterargument

HDM already stores explicit semantic dependencies such as causal/event references. A vector component for every active/relevant scene would duplicate those dependencies in opaque summary form.

It also scales with participant/domain set, complicates scene creation/closure/retention and gives no metric elapsed-time semantics. Sparse cross-scene interactions are exactly the case where explicit bridge edges are cheaper than continuously maintained vectors.

Most importantly, vector causality describes communication/storage topology, while HDM fictional causality may be established by adjudicated world semantics that do not map one-to-one to repository communication.

### Resolution

Reject vector clocks as baseline machine representation.

Vector-time theory remains useful for adversarial checks that no accidental total order is introduced.

## 6. Strongest case for owner-local-only evidence

### Argument

Let every Effect, Procedure, scene, process and event store whatever temporal evidence it needs. Avoid a chronology subsystem entirely. Reconcile only when a concrete operation spans owners.

### Counterexample 1 — evidence outlives source timer

Step-1/2 assurance already requires explicitly established quantitative elapsed evidence to survive even when no timer is currently armed.

### Counterexample 2 — shared cross-owner relation

If information from scene A causes a state/action in B, the relation may be needed later by knowledge, lore, process, Story provenance or another temporal predicate after the original active owner changes lifecycle.

### Counterexample 3 — bounded recovery

If the only proof of a cross-scene relation is implicit across several old owners, cold recovery may require history scans/re-adjudication.

### Resolution

Owner-local is the default placement rule, but not sufficient alone. Some accepted relation evidence must be independently durable/referencable after original active-owner lifecycle changes.

This does **not** require one chronology database; relations may remain embedded in stable event/evidence records.

## 7. Do we need a first-class `TemporalMetricContext` mutable owner?

### Initial concern

`TemporalBinding.metric_deadline` has:

```text
context_id
anchor_value
deadline_value
```

but no inspected contract defines `context_id.current_value`.

### Reframing

The schema does not logically require the metric context itself to own a current coordinate.

A cleaner distinction is:

```text
METRIC COORDINATE SYSTEM
    immutable/registered interpretation
    identity, unit/scale, comparison semantics

CHRONOLOGY SCOPE POSITION
    current accepted position/evidence for a scene/process/procedure scope
    owned by that native scope
```

Then:

```text
TemporalBinding
    references coordinate system C
    anchor/deadline are values in C

current scene/process scope
    exposes current position/range in C
```

Due comparison uses compatible scope-position evidence.

### Example

```text
C = fictional-world-minutes
Effect deadline = 720

scene A current position = [710, 715]
    -> NOT_DUE

scene A current position = [718, 725]
    -> INDETERMINATE

scene A current position = [725, 730]
    -> DUE
```

No universal `C.current_time` exists.

### Cross-scene case

Two scopes may expose positions in the same coordinate system when fiction has established a shared metric basis. If they use different coordinate systems, an explicit bridge/offset constraint may make values comparable. Otherwise comparison remains `INDETERMINATE`.

### Resolution

Reject a mandatory generic mutable `TemporalMetricContext` owner.

Require instead a **typed metric-coordinate-system + scope-position provider contract**. Physical representation may be scene/process/native-owner fields plus typed references.

This is a technical architecture decision, not a new product semantic choice.

## 8. Should scope position be exact scalar or interval/range?

### Scalar-only case

Simple arithmetic and compact storage.

### Problem

Adaptive precision is a core HDM principle. If fiction only establishes “roughly 10–20 minutes later”, forcing one scalar invents precision.

### Range model

Allow coordinate evidence conceptually as:

```text
EXACT(x)
BOUNDED([lo, hi])
UNKNOWN
```

Potential open/unbounded edges may be allowed only if a concrete consumer needs them; baseline can represent unknown separately.

Comparison to scalar deadline D:

```text
hi < D     -> NOT_DUE
lo >= D    -> DUE
otherwise  -> INDETERMINATE
```

For elapsed relation `[lo, hi]` between anchors, analogous difference reasoning applies.

### False-precision risk

A narrative label such as `night` must not automatically become `[18:00,06:00]`. Quantitative bounds exist only when fiction/mechanics actually establish them.

### Resolution

Use exact or bounded numeric evidence only where established. Preserve qualitative display separately unless an owning rule explicitly maps it to metric bounds.

## 9. Do we need full Allen interval algebra?

No known HDM consumer requires all thirteen interval relations.

Known needs reduce to:

```text
CAUSES
STRICT_BEFORE / AFTER
metric elapsed bounds
possibly SAME_COORDINATE / overlap where a mechanic explicitly cares
```

Contested “simultaneous” actions often need Step-3 adjudication rather than a persistent generic interval relation.

### Resolution

Do not import full interval algebra.

Permit typed simultaneity/overlap evidence only if a concrete mechanic or chronology reconciliation establishes it and future decisions require persistence.

## 10. Do we need a scene-local monotonic sequence?

### Benefit

Cheap local order, compact frontier and debugging.

### Risk

CAS serializes writes even when fiction considers actions simultaneous/contested. Therefore source revision or “next event number” cannot automatically mean fictional-before.

### Candidate safe semantics A — nonsemantic index

`sequence` is only retrieval/storage order. Then chronology queries cannot use it; value is mostly optimization/debug metadata.

### Candidate safe semantics B — chronology step coordinate

Assign a chronology step only when accepted semantics establish progression. Multiple events may belong to the same step or be related by explicit edges.

This is stronger but requires deliberate advancement rules.

### Challenge result

A mandatory numeric sequence is not necessary to close semantics. Sparse explicit frontier/edge evidence can represent local chronology.

However a local chronology coordinate may be a valuable machine optimization once implementation measurements show need.

### Resolution

Do **not** make local sequence a canonical required authority.

Canonical architecture should permit scoped local chronology coordinates/indexes with exact declared semantics, but correctness must not depend on a generic `world_order.sequence` unless the owning scene contract establishes its chronology meaning.

## 11. What should replace one `chronology_frontier_event_id`?

A single local event pointer works only if local chronology is guaranteed linear. Same-scene contested/simultaneous branches make that assumption unsafe.

The mathematically sufficient current frontier of a partial order is an antichain/set of maximal relevant anchors.

### Candidate concept

```text
LocalChronologyFrontier(scope)
    = bounded set of maximal chronology anchor refs
```

For ordinary serial scenes this set usually has size 1.

For simultaneous/independent local branches it may contain more than one anchor until a later event/reconciliation joins them.

This frontier is:

- derivative/routing evidence for extension/retrieval;
- not a global progress scalar;
- not a copy of owner state;
- scope typed.

The actual chronology relation remains in accepted event/constraint evidence.

### Resolution

Recommend replacing the semantic assumption of one frontier event with a **bounded scope-local maximal-anchor set**. Exact machine realization may optimize the common singleton case.

This is a strong candidate for canonicalization.

## 12. Do we need `CURRENT.world_time.frontier`?

### Strongest case

A compact globally reconciled marker might accelerate recovery and cross-scene synchronization.

### Problem

There is no one total chronology position. A scalar/id pointer cannot faithfully summarize several independent scenes without hidden coverage semantics.

A set of reconciled global constraints/anchors can be useful, but then it is not a frontier in the Step-5.1 generic sense.

### Resolution

Retire `CURRENT.world_time.frontier` as a generic scalar/global chronology frontier.

If implementation later needs a campaign-level retrieval index, it must expose exact typed coverage such as a sparse set of shared chronology anchors/constraint refs and remain derivative.

`CURRENT.world_time.display` may remain presentation metadata only if it does not claim universal current-time authority.

## 13. Is explicit `UNORDERED` state needed?

Persisting all unordered pairs is impossible/quadratic and semantically useless.

Absence of an ordering path/constraint means no ordering has been established.

Consumer semantics distinguish:

```text
comparison irrelevant
    -> leave incomparable

comparison required + evidence insufficient
    -> INDETERMINATE / reconcile
```

There are rare stronger facts such as “these actions share one adjudicated temporal coordinate”. Those are positive relations, not generic `UNORDERED` records.

### Resolution

No generic persistent `UNORDERED` relation.

## 14. Can later reconciliation invent an ordering that was previously undefined?

### Case A — new causal event establishes order prospectively

Allowed.

Example: B4 receives message produced by A3. Persist `A3 < B4`; no need to order A3 against B1–B3 unless material.

### Case B — current decision requires historical relation that was never established

The engine may derive only relations logically entailed by retained canonical constraints plus deterministic mechanic/world facts available to the adjudication boundary.

It may not choose one compatible order merely because one is convenient.

If several histories remain compatible and the current mechanic needs one unique answer:

```text
INDETERMINATE
-> typed adjudication/reconciliation requirement
```

If the game rules intentionally grant an adjudicator discretion here, the new accepted adjudication must be explicit prospective canon/evidence and must not masquerade as a recovered historical fact unless that is the approved mechanic.

### Resolution

No arbitrary retroactive totalization.

## 15. Cross-scene bridge structure

The simplest sufficient bridge is not a vector clock. It is an explicit typed constraint between stable anchors:

```text
CAUSES(A3, B4)
BEFORE(A3, B4)
ELAPSED(A3, B4, context C, [lo,hi])
SAME_COORDINATE(A3,B4,C) if actually established
```

One relation may imply another (`CAUSES` implies admissible precedence under normal forward chronology), but causal provenance must not be discarded merely because precedence is derivable.

Cross-domain relation identity names endpoint domains/anchors. It does not make unrelated coordinates comparable.

### Resolution

Sparse explicit bridges are the baseline cross-scene reconciliation mechanism.

## 16. Metric rebasing across scene/live transitions

Consider a TemporalBinding created in scope A and an actor/effect later moves to scope B.

Two safe models exist:

### Preserve original anchor

Binding stays anchored in coordinate system/context evidence from A. B must have compatible coordinate position or bridge evidence to evaluate it.

### Rebase

At transfer/reconciliation boundary, derive an equivalent new anchor/deadline in B's coordinate system and persist the equivalence/provenance required to preserve semantics.

Rebasing is legal only when the transformation is deterministic and does not tighten/loosen uncertainty incorrectly.

### Resolution

Canonical architecture should permit both under owner contract. It should not require every timer to retain historical scene dependencies forever if safe rebasing can preserve exact/bounded semantics.

## 17. Time travel / nonmonotonic fictional dates challenge

A mutable global calendar clock fails badly if the fiction can move to another temporal frame.

A coordinate-system/scope-position model can instead open a new chronology scope/context episode and relate it causally/temporally to origin evidence without requiring coordinate monotonicity across incompatible frames.

HDM does not need to design a general time-travel engine in 5.9, but the architecture should avoid making monotonic global world date a correctness axiom.

### Resolution

Monotonicity may be required only inside a specific chronology scope/metric context contract, not across all campaign fiction.

## 18. Compaction challenge

### Pure graph transitive reduction

Removing an edge because another path proves the same precedence is safe only if the removed edge carries no independent causal/provenance meaning.

### Metric summary

Replacing several bounds by a summary is safe only if the summary preserves every still-live query's feasible relation set, not merely one current due answer.

### Owner lifecycle

Evidence cannot disappear merely because the original timer/effect/process ended if later accepted facts depend on its elapsed/causal relation.

### Canonical semantic rule candidate

Chronology evidence can become compaction-eligible only when every still-live or promised future consumer remains decidable with the retained closure and no unique causal/provenance fact is lost.

Physical deletion remains Step 5.13.

## 19. Contradiction detection

Chronology contradiction is not the same as insufficient precision.

Examples:

```text
A < B
B < C
C < A
    -> impossible strict-order cycle

T(B)-T(A) <= 5
T(B)-T(A) >= 10
    -> empty metric feasible set
```

A contradiction should be detected within the bounded connected component touched by a material operation/reconciliation or during validation of newly added constraints. Full campaign scans are not required on every action.

Accepted conflicting current evidence after targeted refresh is an integrity defect for the affected chronology component/scope.

## 20. Revised architecture candidate after challenge

The challenge reduces Alternative E substantially.

Recommended candidate for specification work:

> **OWNER-ANCHORED SPARSE CHRONOLOGY / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION**

Conceptually:

```text
NATIVE / ACCEPTED EVENT EVIDENCE
    causal refs
    precedence refs
    optional metric anchor/elapsed evidence
        |
        v
SCOPE-LOCAL CHRONOLOGY BASIS
    bounded maximal-anchor frontier (usually singleton)
    optional metric position in declared coordinate system
        |
        +--------------------+
                             |
CROSS-SCOPE MATERIAL EVENT  |
        |                    |
        v                    |
SPARSE BRIDGE CONSTRAINTS <--+
    cause / before / elapsed bounds / rare same-coordinate
        |
        v
BOUNDED RECONCILIATION
    ORDERED / NOT_ORDERED_KNOWN? no generic persisted state
    metric DUE / NOT_DUE / INDETERMINATE
    contradiction -> integrity
```

No mandatory:

```text
global current clock
global chronology frontier
vector clock
full interval algebra
campaign-wide temporal solver
mandatory local sequence
persistent unordered-pair records
```

## 21. Remaining potential owner-level questions

After challenge, no clear owner-level product decision is yet required.

The apparent choices collapse technically:

- global current clock conflicts with accepted independent-scene semantics;
- vector clocks add cost without a required consumer;
- full temporal CSP is unnecessary;
- owner-local-only cannot meet retained cross-owner/recovery evidence requirements;
- approximate metric bounds follow the already accepted adaptive-precision principle.

The one issue that could become material is **whether ordinary D&D campaigns should always instantiate one shared world metric coordinate system by default** (for example fictional elapsed seconds/minutes from an epoch) even though scopes own independent positions on it.

Preliminary recommendation: this should be an implementation/profile convenience, not an architecture invariant. Architecture should permit a common world axis where the campaign/ruleset establishes it, but must work when only local/relative metric contexts exist.

No human decision is requested yet; adversarial review of the eventual candidate may expose a concrete semantic trade-off.

## 22. Challenge verdict

Alternative E survives, but in reduced form.

Retained mechanisms each have a concrete consumer:

```text
causal refs
    -> provenance/knowledge/process/history

precedence refs
    -> noncausal ordering constraints

scope-local maximal-anchor frontier
    -> bounded local extension/recovery

metric coordinate-system identity + scope position
    -> durations/deadlines/races without global now

bounded elapsed constraints
    -> approximate quantitative evidence

sparse cross-scope bridge relations
    -> multiplayer/reconciliation/recovery
```

Rejected mechanisms have no sufficient current justification:

```text
global current world clock
vector timestamps
full interval algebra
campaign-wide constraint solver
generic unordered relation
generic global chronology frontier
mandatory semantic local sequence
```

Proceed to candidate specification after fresh consistency review against Steps 5.1, 5.3, 5.7 and 5.8.
