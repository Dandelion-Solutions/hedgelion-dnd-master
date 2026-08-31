# Step 5.9 — Chronology Persistence & Reconciliation — Canonical Specification

Status: **CANONICAL — STEP 5.9 ARCHITECTURE CLOSED**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Canonical architecture direction:

> **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**

Canonicalization basis:

- `../design/2026-08-20-step-5-9-chronology-persistence-reconciliation-task-brief.md`
- `../design/2026-08-20-step-5-9-chronology-persistence-reconciliation-research-draft.md`
- `../design/2026-08-20-step-5-9-chronology-persistence-reconciliation-analytical-challenge.md`
- `../design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`
- `../design/2026-08-21-step-5-9-chronology-persistence-reconciliation-candidate-spec.md`
- `../design/2026-08-21-step-5-9-chronology-persistence-reconciliation-adversarial-review.md`
- `../design/2026-08-21-step-5-9-chronology-persistence-reconciliation-resolution-gate.md`

This document is the Step-5.9 semantic authority. Candidate/research wording is historical derivation where it differs.

It defines chronology evidence, temporal-order domains, metric-coordinate semantics, local chronology basis, cross-scope reconciliation, recovery/retention requirements and the baseline temporal capability boundary. It does not implement schemas/runtime code, Story/transcript/delivery/GC policy or a branching-timeline engine.

---

# 1. Canonical model

HDM chronology is **sparse accepted evidence over stable typed anchors**.

```text
STABLE ACCEPTED ANCHORS
    SemanticEvent / accepted boundary / process milestone / equivalent
        |
        +--> causal ancestry
        +--> domain-typed precedence
        +--> optional exact/bounded metric evidence
        |
        v
NATIVE SCOPE CHRONOLOGY BASIS
    active extension frontier
    optional position provider(s)
        |
        | only when a concrete dependency crosses scopes
        v
MATERIAL BRIDGE EVIDENCE
        |
        v
BOUNDED RECONCILIATION
    determinate relation/result
    INDETERMINATE
    scoped contradiction/integrity outcome
```

There is no mandatory global current fictional clock, no universal event order and no central mutable chronology service.

Chronology evidence describes relations. It does not become current world-state authority, temporal-obligation authority, scheduler authority, live authority or recovery snapshot authority.

---

# 2. Owner-approved temporal capability boundary

Baseline HDM chronology is **forward-extensible**.

Accepted causal history may be extended by:

- new accepted events;
- newly established relations between existing stable anchors;
- refinement of previously unknown/indeterminate chronology through valid evidence;
- exact/bounded elapsed evidence when materially required;
- explicit integrity repair when persisted state was actually wrong/corrupt.

Ordinary baseline chronology does not support as normal semantics:

- rewriting already-established causal history;
- replacing one accepted past with another mutable past;
- several simultaneously authoritative branching timelines/worldlines;
- causal-loop/retrocausal cycles as a normal causality model;
- arbitrary timeline replacement/merge.

This is a complexity/capability boundary, not a ban on temporal fiction.

Supported when compatible with forward-extensible causal history:

- deadlines/countdowns;
- independent scene timing;
- different temporal rates/planes;
- forward jumps/stasis;
- visions, records and historical mysteries;
- immutable-history time travel;
- arrival at an earlier calendar coordinate after a later causal departure;
- newly discovered historical ordering that had previously been unknown.

If a requested action genuinely requires unsupported mutable-past/branching/causal-loop semantics, baseline runtime must not fake support by rewriting old history or interpreting contradictions as proof of time travel.

---

# 3. Stable chronology anchors

A chronology anchor is a stable accepted point that may participate in chronology relations.

Normally it is a typed reference to an existing semantic identity, including as applicable:

```text
runtime.semantic_event
accepted boundary occurrence
accepted process milestone
accepted scene/world transition
accepted execution/event identity where the owner contract admits it
other stable owner-defined chronology point
```

Step 5.9 does not require a universal mutable `ChronologyAnchor` record for every action.

## LAW 5.9-1 — ANCHOR IDENTITY IS SEMANTIC, NOT ORDER

Anchor identity is stable once externally referenced but does not imply chronology by lexical value, allocation order, Git placement, storage order or source revision.

## LAW 5.9-2 — PHYSICAL SOURCE MOVEMENT DOES NOT CHANGE ANCHOR IDENTITY

An accepted anchor that moves from live storage into campaign storage through lawful Step-5.8 absorption remains the same chronology anchor.

Git SHA/HEAD identifies source revision/currentness, not chronology identity.

## LAW 5.9-3 — UNACCEPTED/VOLATILE CANDIDATES ARE NOT DURABLE CROSS-SCOPE ANCHORS

A prospective event/anchor that never crossed its native acceptance/durability edge cannot become a promised durable chronology dependency merely because an LLM/session remembers it.

---

# 4. Domain-typed relation model

Step 5.1 domain typing applies directly to chronology.

The same pair of anchors may have different valid relations in different domains.

Canonical conceptual relation families:

```text
CAUSES(A,B)
PRECEDES(A,B,D)
SAME_COORDINATE(A,B,C)
ELAPSED(A,B,C,[lo,hi])
```

where:

- `D` is a chronology order domain;
- `C` is a typed metric coordinate system/context.

No cross-domain relation is inferred merely because two relations use the same anchors or similar numeric values.

## 4.1 Causal ancestry

`CAUSES(A,B)` says A is accepted causal ancestry/provenance for B.

Causality is not the same thing as calendar order or nonzero elapsed duration.

## LAW 5.9-4 — BASELINE CAUSAL ANCESTRY IS ACYCLIC

Forward-extensible baseline causality does not admit a causal cycle:

```text
A -> ... -> A
```

as normal chronology semantics.

A recognized attempt to create mutable-past/retrocausal cycle is rejected/deferred at the capability boundary before accepted mutation where possible.

A persisted unexpected causal cycle after targeted refresh is integrity/capability suspect, not silently normalized.

## 4.2 Strict precedence in an order domain

`PRECEDES(A,B,D)` says A is strictly earlier than B **inside order domain D**.

It does not by itself say A caused B.

Examples of D may include:

- one scene chronology episode;
- one process chronology domain;
- one world-calendar order domain;
- another owner-defined ordered chronology domain.

## LAW 5.9-5 — PRECEDENCE IS ONLY TRANSITIVE/COMPARABLE INSIDE ITS DOMAIN

`PRECEDES(A,B,D1)` and `PRECEDES(B,C,D2)` do not imply `PRECEDES(A,C,?)` when D1 and D2 are not explicitly related by an owning contract.

## LAW 5.9-6 — STRICT PRECEDENCE IS ACYCLIC PER DOMAIN

A persisted cycle inside one strict order domain is incompatible chronology evidence.

## 4.3 Causal order and calendar order may diverge

Canonical legal example:

```text
A = departure at world-calendar 1250
B = immutable-history arrival at world-calendar 1199

CAUSES(A,B)
PRECEDES(B,A,world_calendar)
```

This is not a causal loop: causal ancestry progresses A -> B while calendar coordinate goes backward.

## LAW 5.9-7 — NO IMPLICIT CAUSAL/CALENDAR EQUIVALENCE

A causal edge does not implicitly create world-calendar precedence, and world-calendar precedence does not create causal ancestry.

This rule is required both by Step-5.1 domain typing and the owner-approved immutable-history temporal boundary.

---

# 5. Same-coordinate / simultaneity evidence

`SAME_COORDINATE(A,B,C)` is positive accepted evidence that A and B share the same relevant coordinate in metric context C.

## LAW 5.9-8 — UNKNOWN ORDER IS NOT SIMULTANEITY

Absence of `PRECEDES` evidence does not establish simultaneity, overlap or same coordinate.

No generic persisted `UNORDERED(A,B)` relation is required.

## LAW 5.9-9 — TRANSPORT CONCURRENCY IS NOT TEMPORAL EQUALITY

Same prior live revision, same Git commit window, same wall-clock second, concurrent requests or CAS contention do not establish `SAME_COORDINATE`.

It may be established only by an admitted mechanic, boundary occurrence, metric equality evidence or accepted reconciliation that gives the relation semantic meaning.

## LAW 5.9-10 — SAME METRIC COORDINATE DOES NOT IMPLY CAUSAL INDEPENDENCE

Causally ordered subevents may share one metric coordinate/instant.

---

# 6. Metric coordinate systems — rulers, not global clocks

A metric coordinate system/context defines interpretation/comparison of quantitative temporal coordinates.

Conceptually:

```text
context_id
unit / scale semantics
ordered deterministic numeric domain
scope applicability / interpretation
admitted bridge/rebase rules, if any
```

## LAW 5.9-11 — NO MANDATORY GLOBAL CURRENT WORLD CLOCK

A metric context may be shared by many scopes, but it does not own one mutable campaign-global current coordinate.

Example:

```text
context C = world elapsed minutes
Scene A position = 710..715
Scene B position = 735
```

Both positions are meaningful in C without requiring one global `now`.

## LAW 5.9-12 — CONTEXT IDENTITY DOES NOT SELECT CURRENT POSITION

`TemporalBinding.metric_deadline.context_id` identifies the ruler/comparison context. It does not by itself identify which current scope/provider supplies the owner's present position.

---

# 7. Scope position evidence

A temporal scope/provider may expose accepted metric position evidence in a declared context:

```text
EXACT(v)
BOUNDED(lo, hi)    # lo <= hi
UNKNOWN
```

This evidence belongs to the applicable native scene/process/procedure/other owner contract.

## LAW 5.9-13 — DO NOT INVENT A SCALAR FROM A RANGE

If accepted evidence establishes only `[lo,hi]`, deterministic runtime may not choose an arbitrary point inside the range merely to make a ruling easier.

## LAW 5.9-14 — QUALITATIVE TIME DOES NOT IMPLY NUMERIC BOUNDS

`night`, `after the council`, `third day of the siege`, `before coronation` and similar qualitative/narrative descriptions do not automatically become numeric ranges.

Quantitative interpretation exists only when a rule/world contract actually establishes it.

---

# 8. Deterministic temporal position-provider routing

Every metric TemporalBinding/owner family defines how its current comparison position is selected.

Conceptually:

```text
ResolveTemporalPosition(
    temporal_owner,
    binding,
    coherent_current_ownership_basis
)
    -> POSITION(provider_scope_ref, context_id, evidence)
     | INDETERMINATE_NO_COMPATIBLE_PROVIDER
     | INTEGRITY_CONFLICT
```

## LAW 5.9-15 — PROVIDER ROUTING IS OWNER-SPECIFIC AND MACHINE-DECIDABLE

The native owner/binding family determines whether current position comes from:

- the owner's current temporal scene/scope;
- a provider pinned by the binding;
- the process/procedure owner itself;
- another explicit typed provider.

Loaded-context convenience or host memory cannot choose the provider.

## LAW 5.9-16 — MOVEMENT MUST PRESERVE PROVIDER SEMANTICS

When an owner crosses chronology scopes, one of these occurs:

```text
FOLLOW CURRENT SCOPE
    provider routing moves coherently with owner transfer

PRESERVE SOURCE PROVIDER
    binding retains source/provider/bridge evidence

SAFE REBASE
    an equivalent destination binding/provider is established deterministically
```

If no compatible provider exists, the temporal predicate is `INDETERMINATE` rather than guessed.

Conflicting simultaneously applicable exclusive providers are an integrity/ownership defect.

## LAW 5.9-17 — SAFE REBASE PRESERVES ACCEPTED UNCERTAINTY

Rebasing may not tighten a range, invent a scalar, change deadline semantics or discard required provenance merely to simplify storage.

---

# 9. Quantitative elapsed evidence

`ELAPSED(A,B,C,[lo,hi])` records established elapsed quantity between stable anchors in metric context C.

Exact elapsed is `lo == hi`.

## LAW 5.9-18 — QUANTITATIVE EVIDENCE IS MATERIALIZED ONLY WHEN JUSTIFIED

Ordinary narration does not receive minute-by-minute timestamps merely for completeness.

Persist elapsed evidence only when a current/future admitted consumer such as deadline, race, travel/process mechanic, recovery predicate or material historical fact requires it.

## LAW 5.9-19 — ESTABLISHED ELAPSED EVIDENCE MAY OUTLIVE ORIGINAL TIMER

Quantitative evidence cannot be discarded solely because the Effect/process/timer that first caused it to be established has settled when another protected consumer still depends on it.

---

# 10. Step-5.3 due evaluation

Chronology supplies comparison evidence; the native temporal owner remains timing/obligation authority.

For a scalar deadline D in context C and applicable position P:

```text
P = EXACT(x)
    x < D   -> NOT_DUE
    x >= D  -> DUE

P = BOUNDED(lo,hi)
    hi < D   -> NOT_DUE
    lo >= D  -> DUE
    otherwise -> INDETERMINATE

P = UNKNOWN / incompatible context without bridge
    -> INDETERMINATE
```

Equivalent owner-defined three-valued comparisons may exist for other admitted temporal predicates.

## LAW 5.9-20 — DUE RESULT IS DERIVED, NOT A GENERIC DURABLE CHRONOLOGY FLAG

Step-5.3 native owner/binding remains source authority. Chronology does not persist a universal `due=true` state.

## LAW 5.9-21 — RECOVERY MUST REPRODUCE THE LAWFUL COMPARISON BASIS

Cold recovery must restore the owner, binding, deterministic provider routing and required metric/bridge evidence sufficiently to reproduce `NOT_DUE | DUE | INDETERMINATE` without host memory or global clock reconstruction.

---

# 11. Bounded metric relation composition

Baseline chronology may derive exact/bounded relations across a **bounded relevant component**.

Example:

```text
ELAPSED(A,B,C,[5,10])
ELAPSED(B,D,C,[7,12])

=> derived feasible ELAPSED(A,D,C,[12,22])
```

## LAW 5.9-22 — LOCAL CONSTRAINT REASONING IS ALLOWED; CAMPAIGN TEMPORAL CSP IS NOT

A concrete predicate may compose compatible loaded bounds/relations deterministically.

No global temporal constraint solver over campaign history is required or authorized.

Derived composed results need not be persisted unless a concrete future-consumer/performance requirement justifies a typed derivative summary.

A protected consumer whose required evidence closure becomes unbounded violates its routing/retention contract and needs summary/repartition/repair rather than an ordinary full-history scan.

---

# 12. Relation evidence authority and late establishment

When a relation is known at the accepted event/owner transition that establishes it, prefer owner/event-local evidence.

Useful existing forms include:

```text
SemanticEvent.caused_by_event_ids
SemanticEvent.after_event_ids
```

subject to domain-typing rules below.

## LAW 5.9-23 — DO NOT CREATE A SECOND MUTABLE RELATION AUTHORITY

A relation embedded in its establishing accepted record remains semantic source authority. A derivative index/copy does not become a second writable truth.

## LAW 5.9-24 — LATE-ESTABLISHED RELATIONS DO NOT REWRITE OLD EVENT MEANING

If new accepted evidence E establishes a relation between old anchors A and B, ordinary operation does not edit historical A/B identity/meaning in place.

E or a compact immutable evidence artifact justified by E carries a typed relation assertion/evidence value.

Conceptually:

```text
relation identity/key
relation type
endpoint anchor refs
domain/context identity
exact/bounded value if applicable
established_by ref
supporting refs where required
```

A standalone new universal record class is not mandatory.

## LAW 5.9-25 — LATE RELATION ASSERTIONS REQUIRE STABLE IDENTITY WHEN REFERENCED

An embedded assertion may use stable owning-event identity + local declaration key/equivalent owner contract when that proves uniqueness and stable external reference.

---

# 13. Bounded relation discovery / dependency enrollment

Relation evidence identity and relation discovery are distinct.

## LAW 5.9-26 — EVERY PROTECTED CONSUMER HAS A BOUNDED DURABLE PATH TO REQUIRED RELATION EVIDENCE

A still-live or explicitly promised consumer may not depend on "some relation somewhere in history" without bounded routing.

Preferred forms:

```text
consumer/native owner -> direct stable relation/evidence ref
OR
consumer/native owner -> typed bounded dependency index -> relation evidence
```

## LAW 5.9-27 — DERIVATIVE ENDPOINT INDEXES ARE OPTIONAL, TYPED AND NONAUTHORITATIVE

If implementation promises endpoint-only relation lookup, it may maintain an index keyed by anchor/domain.

Such an index:

- declares scope/coverage;
- is not semantic relation authority;
- participates in durability coherently enough that acknowledged protected dependencies do not become undiscoverable;
- has a bounded repair source contract;
- cannot justify a fictional relation absent canonical source evidence.

No campaign-wide relation scan is an ordinary fallback.

---

# 14. Scope-local active extension frontier

A scope may persist/cache a compact extension basis:

```text
ActiveExtensionFrontier(S)
```

It is the set of maximal anchors that future **current extension/recovery of S** is still required to treat as active predecessor/basis.

It is not every maximal historical event in the retained scope history.

## LAW 5.9-28 — FRONTIER IS DERIVATIVE, DOMAIN-TYPED EVIDENCE

Frontier accelerates bounded extension/recovery. Accepted anchor/relation evidence remains chronology authority.

## LAW 5.9-29 — FRONTIER MAY CONTAIN MULTIPLE ANCHORS

A scope is not assumed fictionally linear merely because repository writes are serialized.

Contested/parallel current branches may produce:

```text
frontier = {A,B,...}
```

## LAW 5.9-30 — SEMANTIC JOIN MAY COLLAPSE FRONTIER WITHOUT ORDERING INPUTS

If accepted J is genuinely after all active predecessors in domain D:

```text
PRECEDES(A,J,D)
PRECEDES(B,J,D)
```

then J may replace A/B in current extension frontier without asserting A-vs-B order.

Synthetic fictional joins solely for metadata compression are forbidden.

## LAW 5.9-31 — SAFE FRONTIER RETIREMENT DOES NOT REQUIRE A JOIN

Anchor A may leave active extension frontier when owner lifecycle/relevance proves it no longer participates in current ordinary extension and every protected consumer depending on A retains its own bounded evidence route.

Frontier retirement:

- does not delete A;
- does not erase provenance;
- does not order A against anything;
- does not mean A never happened.

## LAW 5.9-32 — DECOMPOSE REAL INDEPENDENCE INSTEAD OF BUILDING A VECTOR

If many genuinely independent activities remain current, represent them through their actual scene/process/procedure chronology scopes where appropriate rather than forcing one giant frontier/vector over unrelated work.

---

# 15. Cross-scope material bridge reconciliation

Cross-scope chronology is established only when a concrete accepted dependency requires it.

Baseline protocol:

```text
1. identify exact chronology predicate/dependency
2. exact-pin participating current native sources under Steps 5.7/5.8
3. resolve stable endpoint anchors
4. load directly required relation/metric evidence through bounded routes
5. compose only the bounded relevant component
6. if entailed -> use result
7. if current accepted transition establishes new relation -> persist minimum material bridge evidence
8. if insufficient -> INDETERMINATE / typed adjudication-reconciliation outcome
9. if contradictory after targeted refresh -> scoped integrity handling
```

## LAW 5.9-33 — MATERIAL BRIDGES ARE SPARSE

Connecting Scene A to Scene B does not require globally ordering every prior event in A against every event in B.

Example:

```text
A3 creates/sends information
B4 receives it

CAUSES(A3,B4)
```

is sufficient unless another current consumer requires additional relations.

## LAW 5.9-34 — NO ARBITRARY RETROACTIVE TOTALIZATION

If several historical orders remain compatible and no retained accepted evidence determines one, reconciliation may not choose an order because it is convenient, dramatic or storage-cheap.

A required unresolved comparison remains `INDETERMINATE` / explicit adjudication boundary.

---

# 16. Contested/simultaneous actions

When fictional order affects outcome, normal Step-3/game-rule adjudication establishes the accepted mechanics.

## LAW 5.9-35 — CAS WINNER DOES NOT WIN FICTION

The first repository/live write to succeed does not automatically become the first fictional action when mechanics treat actions as simultaneous/contested.

## LAW 5.9-36 — PERSIST ONLY FUTURE-RELEVANT ORDER/TEMPORAL EVIDENCE

After adjudication, retain chronology relation/evidence only when future mechanics, causal provenance, recovery or another canonical consumer needs it.

Do not timestamp/total-order the whole contest merely for audit aesthetics.

---

# 17. Live-epoch chronology integration

Step 5.8 synchronization order remains distinct from fiction.

## LAW 5.9-37 — LIVE SOURCE REVISION IS NOT FICTIONAL TIME

Exact live HEAD/revision is CAS fencing/currentness evidence only.

Independent live epochs remain chronologically incomparable unless accepted semantic evidence connects them.

## LAW 5.9-38 — LIVE ACCEPTED EDGES MAY ESTABLISH CHRONOLOGY EVIDENCE

A native accepted live durability edge may establish stable anchors, relations and metric position/elapsed evidence required by that transition.

## LAW 5.9-39 — CLOSE / ABSORPTION / SUCCESSOR OPENING DO NOT ADVANCE FICTION

Technical authority transitions:

```text
ACTIVE -> CLOSED
campaign absorption
branch cleanup
successor epoch opening
```

create no fictional time/order merely by occurring.

## LAW 5.9-40 — ABSORPTION PRESERVES ANCHOR/RELATION IDENTITY

Required chronology evidence and stable IDs survive lawful live-to-campaign movement.

Absorption order of independent epochs does not establish fictional order.

## LAW 5.9-41 — SUCCESSOR INHERITS THE ACCEPTED SCENE CHRONOLOGY BASIS

A technical rollover continuing the same fictional scene starts from the absorbed current semantic extension/position basis; opening the new epoch is not itself a fictional anchor unless some separate accepted world transition actually occurred.

## LAW 5.9-42 — PARTIAL MULTI-SCOPE FREEZE IS NOT PARTIAL FICTION

Step-5.8 freeze progress only fences writers. Cross-scope fictional relation appears when the shared semantic transition is accepted, not as each branch closes.

---

# 18. Recovery integration

Step 5.7 current-authority-first recovery remains the governing source-selection model.

## LAW 5.9-43 — COLD RECOVERY DOES NOT REBUILD A GLOBAL TIMELINE

Recovery hydrates chronology evidence required by recovered active owners/scopes through bounded typed dependencies.

No full LOG load or campaign timeline reconstruction is required.

## LAW 5.9-44 — POSITION PROVIDER IS RE-RESOLVED FROM CURRENT NATIVE ROUTING

Host/chat memory does not select current temporal position provider after restart.

## LAW 5.9-45 — DERIVED CHRONOLOGY INDEXES MAY REBUILD

Frontiers, relation lookup indexes, reachability/metric caches and other derivative structures may rebuild from their bounded owning source contract.

If one is required for bounded correctness, its lifecycle/enrollment is correctness-critical derivative evidence analogous to Step-5.2/5.7 routing, but it still does not own the semantic relation.

---

# 19. Consumer-bounded retention guarantee

Baseline Step 5.9 intentionally does **not** promise a permanent temporal database able to answer every arbitrary historical query forever.

Canonical guarantee:

> Every still-live or explicitly promised canonical consumer retains a bounded path to sufficient temporal/causal evidence for the predicates admitted by that consumer's owner contract.

Protected consumers include as applicable:

- armed temporal owners;
- active processes/deadlines;
- open Procedure/Continuation/execution dependencies;
- current scene/scope extension basis;
- current durable state/lore/knowledge whose owning contract explicitly retains chronology dependency;
- later Story/history/disclosure owners only if their later canonical contracts enroll such a dependency.

## LAW 5.9-46 — ARBITRARY HISTORICAL TEMPORAL ANALYTICS ARE NOT BASELINE RETENTION AUTHORITY

A later arbitrary question about old chronology may be answerable from retained canon, but Step 5.9 does not retain otherwise unnecessary chronology solely to guarantee every unanticipated historical pair/query after lawful compaction.

When gameplay later establishes a historical relation as materially relevant canon, the new accepted owner/evidence becomes a protected consumer and retains the needed relation from then onward.

---

# 20. Compaction semantic eligibility

Step 5.9 defines when chronology evidence is semantically eligible for compaction. Step 5.13 owns physical deletion/GC.

## LAW 5.9-47 — PROTECTED CONSUMER DECIDABILITY SURVIVES COMPACTION

Evidence is compaction-eligible only if every protected consumer retains the same lawful answer/feasible relation set required by its owner contract.

Preserving only today's result is insufficient if another still-live predicate could distinguish the removed information.

## LAW 5.9-48 — CAUSAL PROVENANCE IS NOT REPLACED BY TEMPORAL ORDER

If `CAUSES(A,B)` is independently meaningful provenance, another proof that A precedes B does not make the causal evidence disposable.

## LAW 5.9-49 — METRIC SUMMARY MUST PRESERVE REQUIRED FEASIBLE SET

Widening `[47,53]` to `[0,60]` is not semantic equivalence merely because one current deadline remains unchanged.

## LAW 5.9-50 — REDUNDANT DERIVED PRECEDENCE MAY BE COMPACTED WHEN LOSSLESS

A redundant precedence edge/summary may become eligible when retained evidence still proves every protected required relation and the removed item carries no unique causal/provenance/identity meaning.

No campaign-wide transitive-reduction pass is required.

## LAW 5.9-51 — FRONTIER/INDEX LIFECYCLE IS SEPARATE FROM SOURCE-EVIDENCE RETENTION

Deleting/rebuilding derivative extension/index metadata does not itself authorize deleting canonical relation evidence.

---

# 21. Integrity classification

Chronology contradiction is domain typed and scope local.

Examples of contradiction:

```text
PRECEDES(A,B,D)
PRECEDES(B,A,D)
```

```text
SAME_COORDINATE(A,B,C)
metric evidence in C proves A strictly before B
```

```text
metric bounds in C have empty feasible set
```

```text
causal ancestry contains a cycle
```

Examples that are **not** contradiction:

```text
CAUSES(A1250,B1199)
PRECEDES(B1199,A1250,world_calendar)
```

```text
Scene A uses context CA
Scene B uses incompatible CB
no bridge
```

```text
no relation established between independent A and B
```

## LAW 5.9-52 — INDETERMINATE IS NOT CORRUPTION

Insufficient evidence, incompatible contexts without bridge and legitimate incomparability remain non-corrupt states.

## LAW 5.9-53 — TARGETED CURRENT REFRESH PRECEDES CORRUPTION CONCLUSION

As with `INTEGRITY.md`, chronology suspicion is checked against current relevant pinned sources. Persisted contradiction after bounded refresh is scoped `CANON_SUSPECT`/corrupt according to the integrity protocol.

## LAW 5.9-54 — FALSE/DISPUTED CLAIMS DO NOT ENTER OBJECTIVE CHRONOLOGY

An NPC belief, document claim or Narrator statement that A caused/preceded B belongs to Step-4 truth/knowledge semantics until objective relation is established through normal validation/promotion.

Chronology does not accept it merely because text states it.

---

# 22. Unsupported mutable-past/branching boundary enforcement

## LAW 5.9-55 — RECOGNIZABLE UNSUPPORTED TEMPORAL SEMANTICS ARE BLOCKED BEFORE ACCEPTED REWRITE

When requested semantics explicitly require rewriting accepted past, branching authoritative worldlines or causal-loop mutation, deterministic validation surfaces a capability boundary before committing replacement chronology/world state.

## LAW 5.9-56 — CONTRADICTION IS NOT AUTOMATIC TIME-TRAVEL EXPLANATION

If persisted records conflict, HDM does not invent temporal anomalies/retcons as repair unless such semantics were already supported and canonically established by an explicit future extension.

## LAW 5.9-57 — DRAMATURG PREPARATION CARRY-FORWARD

Step-4 Dramaturg remains noncanonical preparation, but eventual role/policy realization must include this owner-approved guard:

> Baseline Dramaturg does not deliberately prepare campaign premises/developments whose correctness requires mutable past, branching authoritative timelines or causal-loop chronology unless a future explicit temporal extension is selected.

Dramaturg may prepare deadlines, historical mysteries, immutable-history time travel, time dilation, prophecies, forward jumps and other temporal themes compatible with forward-extensible causal history.

No LLM role gains chronology authority from this rule.

---

# 23. Difficult supported scenario disposition

## 23.1 Global countdown

Supported.

Many scopes may share a metric coordinate system/deadline while retaining independent positions. Cost rises because more actions need quantitative evidence; no global mutable now is required.

## 23.2 Dense synchronized multi-scene operation

Supported with degraded cost, not degraded correctness.

The affected relation component becomes denser and more frequent bounded reconciliation is required.

If real measurements later show repeated arbitrary cross-scope comparisons dominate runtime cost, introduce a derivative typed summary/index only after proving need. Do not preemptively add vector clocks/global frontier.

## 23.3 Time dilation / planar temporal differences

Supported when owner/bridge evidence can establish exact/bounded relationships.

Unknown conversion may legitimately yield `INDETERMINATE` for affected predicates.

A generic permanent rate-conversion engine is not baseline-required.

## 23.4 Historical mystery

Supported through new accepted relation evidence attached to the later discovery/establishment transition without rewriting old event identity.

## 23.5 Immutable-history time travel

Supported insofar as causal ancestry remains forward-extensible and acyclic even if an event occupies an earlier calendar/metric coordinate.

Mutable-past rewrite/branching remains outside baseline.

---

# 24. Current runtime/schema disposition

Architecture closure does not implement these changes. Current GAME/schema wording remains implementation debt where it conflicts with this spec.

## 24.1 Keep/refine

`SemanticEvent.caused_by_event_ids`

- retain objective causal ancestry semantics;
- no chronological meaning from ID ordering.

`SemanticEvent.after_event_ids`

- may remain for a clearly owner-defined single local order domain;
- must not serve as an untyped universal precedence relation when domain ambiguity exists.

`world_order.scene_id`

- remains useful as scope/domain tagging where its owner contract defines exact chronology meaning.

`scene.local_time` / live `local_time`

- may survive only with explicit distinction between typed semantic position/evidence and presentation/qualitative label.

## 24.2 Retire/demote

`CURRENT.world_time.frontier`

- retired as generic global chronology frontier/authority.

`CURRENT.world_time.display`

- presentation convenience only; no correctness/current-world-time authority.

`world_order.sequence`

- not baseline fictional chronology authority unless a specific scope contract explicitly defines a local semantic chronology coordinate.

`scene.chronology_frontier_event_id`

- singleton semantic assumption superseded by `ActiveExtensionFrontier(S)`; common singleton physical optimization remains allowed.

---

# 25. Machine-realization debt

Later implementation planning must cover at least:

1. typed chronology anchor references across admitted event/boundary/process owners;
2. relation domain/context identity for precedence and metric evidence;
3. exact machine representation for late immutable relation assertion/evidence;
4. deterministic stable relation IDs/keys where externally referenced;
5. owner-specific `ResolveTemporalPosition` contracts for each metric TemporalBinding family;
6. exact/bounded metric position representation and deterministic arithmetic/units;
7. bounded elapsed relation representation and local composition tests;
8. active extension frontier representation, including safe retirement and singleton optimization;
9. direct relation dependency refs and/or typed bounded discovery indexes for protected consumers;
10. live close/absorption preservation of chronology IDs/evidence;
11. retirement/demotion migration for `CURRENT.world_time.frontier`, singleton scene frontier and ambiguous sequence semantics;
12. Step-4 Dramaturg temporal capability guard in eventual role/context policy realization;
13. integrity validation for typed cycles, impossible metric constraints and missing required anchor refs;
14. chronology compaction-safety metadata/dependency integration feeding Step 5.13;
15. regression cases for all difficult supported and unsupported temporal scenarios.

No broad implementation begins during Step 5 architecture closure.

---

# 26. Required regression/adversarial realization cases

Later machine/runtime tests should include at least:

```text
ordinary serial scene frontier
same-scene parallel/contested frontier
semantic join after two unordered anchors
safe frontier retirement without join
independent scenes remain incomparable
cross-scene message creates one minimal bridge
late historical relation asserted without rewriting old event
causal relation distinct from noncausal precedence
same-coordinate not inferred from CAS order
exact deadline due/not-due
bounded position -> INDETERMINATE crossing deadline
owner moves scene and provider routing changes coherently
binding preserves source context across transfer
safe deterministic rebase
unsafe/unknown rebase -> INDETERMINATE
bounded elapsed-chain composition
metric contradiction in one bounded component
strict precedence cycle in one domain
immutable-history backward calendar jump with acyclic causal order
mutable-past rewrite rejected at capability boundary
global countdown across several independent scope positions
nonconstant/unknown planar conversion
live cross-scope anchor reference survives close/absorption
independent live absorption order does not create fictional order
partial multi-live freeze adds no fictional event
cold recovery reproduces due result without global timeline
late relation protected consumer recovers by bounded dependency path
arbitrary unpromised historical query has no retention guarantee
compaction preserves causal provenance
compaction does not widen metric evidence needed by live consumer
```

---

# 27. Performance contract

Ordinary chronology work must remain local/bounded:

```text
ordinary local action
    O(native current scope + direct chronology dependencies/frontier)

material cross-scope action
    O(bounded affected chronology dependency component)
```

Baseline ordinary play must not require:

```text
full campaign event scan
all-scene scan
global chronology reconstruction
global vector refresh
campaign-wide temporal constraint solve
mandatory timestamping of events
continuous fictional clock simulation
```

A derivative optimization must have a concrete measured/owner requirement and cannot replace accepted relation authority.

---

# 28. Final architecture invariants

Step 5.9 is closed when these statements are taken together:

```text
1. Fictional chronology never comes from Git/ID/transport order by accident.

2. Causal ancestry, domain-typed precedence and metric coordinate order are distinct.

3. Independent chronology scopes may remain incomparable indefinitely.

4. No global current world clock or generic chronology frontier is required.

5. Metric contexts are rulers; native scopes/providers own current position evidence.

6. Exact/bounded evidence preserves uncertainty and drives Step-5.3 three-valued due evaluation.

7. Cross-scope relations materialize only when concrete accepted dependencies require them.

8. Late-established relations extend history without rewriting old event identity.

9. Every protected consumer has a bounded durable evidence path; arbitrary historical analytics are not a baseline retention promise.

10. Local extension frontier is bounded active basis, not all historical maxima.

11. Live CAS/close/absorption order remains separate from fictional chronology.

12. Compaction may remove chronology evidence only when protected consumers remain semantically decidable and unique provenance is preserved.

13. Contradiction is domain-typed and distinct from INDETERMINATE/incomparability.

14. Baseline accepted causal history is forward-extensible; mutable-past/branching/causal-loop semantics require a future explicit extension.
```

---

# 29. Closure / carry-forward

Step 5.9 owns chronology persistence/reconciliation architecture and is **CLOSED** by this specification subject to final remote/status verification.

Carry-forward:

- Step 5.10 Story Projection Durability may consume chronology/causal evidence for projection provenance but cannot become chronology authority;
- Step 5.11 transcript/history retention must respect chronology evidence still protected by live consumers;
- Step 5.12 disclosure timing cannot reinterpret fictional chronology from host delivery order;
- Step 5.13 GC must use Step-5.9 chronology dependency/compaction eligibility predicates;
- Step 5.14 full adversarial review must include chronology + live/recovery/concurrency interactions;
- Step 6/implementation must realize the Dramaturg temporal-capability guard and machine contracts without weakening Step-5.9 domain typing/boundedness.

No second temporal compensation model is introduced.