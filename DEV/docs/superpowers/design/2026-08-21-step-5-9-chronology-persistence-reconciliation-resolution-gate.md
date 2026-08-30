# Step 5.9 — Chronology Persistence & Reconciliation — Resolution Gate

Status: **RESOLUTION GATE PASSED — READY FOR CANONICAL CONSOLIDATION**

Date: 2026-08-21

Inputs:

- `2026-08-20-step-5-9-chronology-persistence-reconciliation-task-brief.md`
- `2026-08-20-step-5-9-chronology-persistence-reconciliation-research-draft.md`
- `2026-08-20-step-5-9-chronology-persistence-reconciliation-analytical-challenge.md`
- `2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`
- `2026-08-21-step-5-9-chronology-persistence-reconciliation-candidate-spec.md`
- `2026-08-21-step-5-9-chronology-persistence-reconciliation-adversarial-review.md`

Resolved architecture direction:

> **OWNER-ANCHORED SPARSE CHRONOLOGY / DOMAIN-TYPED ORDER / TYPED METRIC COORDINATES / MATERIAL BRIDGE RECONCILIATION / FORWARD-EXTENSIBLE HISTORY**

No new human architecture decision is required.

---

# 1. Resolution summary

The adversarial review found five blockers and four required refinements. All are resolved without adding a second chronology model, global clock, vector clock, central chronology database or branching-timeline subsystem.

```text
R1  order-domain typing                         RESOLVED
R2  temporal position-provider routing         RESOLVED
R3  late relation bounded discovery/enrollment RESOLVED
R4  active-extension frontier semantics        RESOLVED
R5  consumer-bounded retention/query promise   RESOLVED
R6  bounded metric composition                 RESOLVED
R7  anchor identity across source movement     RESOLVED
R8  same-coordinate positive evidence          RESOLVED
R9  unsupported temporal capability guard      RESOLVED
```

---

# 2. R1 — causal progression and temporal/calendar order are separate domains

## Problem

Immutable-history time travel can have:

```text
A = departure at calendar 1250
B = arrival at calendar 1199

CAUSES(A,B)
calendar(B) < calendar(A)
```

This is legal under the owner-approved boundary and must not be classified as retrocausal corruption.

## Resolution

Every correctness-relevant ordering claim is domain typed.

Canonical conceptual relations become:

```text
CAUSES(A,B)
    causal ancestry/provenance domain

PRECEDES(A,B,D)
    strict precedence inside chronology order domain D

SAME_COORDINATE(A,B,C)
    equality in metric coordinate system C

ELAPSED(A,B,C,[lo,hi])
    metric difference evidence inside C
```

### Consequences

1. `CAUSES` defines accepted causal ancestry and is acyclic under baseline forward-extensible history.
2. `PRECEDES` is transitive/acyclic only within the same order domain D.
3. No causal edge implicitly creates calendar/metric precedence.
4. No calendar/metric precedence implicitly creates causal ancestry.
5. The same anchors may participate in several chronology domains.
6. Cross-domain comparison/contradiction is forbidden unless an owning contract explicitly relates those domains.

Legal example:

```text
CAUSES(A1250_departure, B1199_arrival)
PRECEDES(B1199_arrival, A1250_departure, world_calendar)
```

Unsupported mutable-past semantics instead require rewriting/branching already-established **causal history**, not merely moving to an earlier calendar coordinate.

### Existing field disposition

`SemanticEvent.after_event_ids` may remain a compact field only when its owning event/scope contract makes the relevant local chronology order domain unambiguous.

Where multiple order domains are possible or the relation is cross-domain, implementation must use typed relation evidence carrying domain identity rather than relying on one untyped `after_event_ids` interpretation.

This is machine-realization debt, not a reason to remove the useful existing field immediately.

---

# 3. R2 — deterministic temporal position-provider resolution

## Problem

`TemporalBinding.metric_deadline.context_id` names a ruler but not necessarily the current scope position to compare against.

## Resolution

Every owner/binding family that uses metric comparison defines deterministic provider routing equivalent to:

```text
ResolveTemporalPosition(
    temporal_owner,
    binding,
    coherent_current_ownership_basis
)
    -> POSITION(provider_scope_ref, context_id, exact/bounded evidence)
     | INDETERMINATE_NO_COMPATIBLE_PROVIDER
     | INTEGRITY_CONFLICT
```

### Provider semantics

The native owner/binding contract determines whether the provider is:

- the owner's current temporal scene/scope;
- a pinned source scope retained by the binding;
- the process/procedure owner itself;
- another explicitly typed provider.

`context_id` alone does not choose a current position.

### Movement

When an owner moves across chronology scopes, one of these must be true:

```text
A. binding semantics follow current owner scope
   -> current provider routing moves coherently with owner transfer

B. binding remains anchored to original provider/context
   -> original provider/bridge evidence remains retained and recoverable

C. deterministic safe rebase occurs
   -> equivalent binding/provider evidence is established without narrowing uncertainty
```

If multiple providers simultaneously claim exclusive current applicability, that is an ownership/integrity defect.

If no compatible provider/bridge is available, due result is `INDETERMINATE`, not guessed global time.

### Recovery

Cold recovery runs the same provider-resolution contract from current native ownership/routing. Host memory does not choose the provider.

---

# 4. R3 — relation identity vs bounded relation discovery

## Problem

A late relation stored on new evidence E must remain discoverable for every still-live consumer without scanning history.

## Resolution

Separate:

```text
RELATION EVIDENCE
    immutable semantic source

RELATION DEPENDENCY ROUTING / INDEX
    bounded derivative discovery evidence
```

### Mandatory rule

Every still-live or explicitly promised consumer whose correctness depends on relation R has one bounded durable evidence path to R.

Preferred mechanisms:

```text
consumer/native owner directly stores stable relation/evidence ref
OR
owner/domain-native typed dependency index routes boundedly to R
```

### Endpoint indexes

If the runtime explicitly supports endpoint-only queries such as:

```text
RelationsForAnchor(A)
```

then a derivative endpoint index may exist.

It must:

- declare scope/coverage;
- not become relation authority;
- be updated/enrolled coherently enough with the accepted relation/consumer dependency to avoid healthy acknowledged dangling dependency;
- be repairable from a bounded source contract.

No campaign-global scan fallback is admitted for ordinary recovery.

### Stable relation identity

A relation assertion embedded in accepted evidence may use a stable composite identity such as owning-event identity + local declaration key when the owner contract proves uniqueness/stability.

A standalone record class is not mandatory.

---

# 5. R4 — frontier is active extension basis, not all historical maxima

## Problem

A mathematical antichain over every retained historical event may grow without bound.

## Resolution

Canonical concept:

```text
ActiveExtensionFrontier(S)
    = maximal anchors still required as current extension/recovery basis for chronology scope S
```

It is **not** the set of every maximal historical anchor ever retained in S.

### Entry

An anchor enters the current frontier when accepted scope semantics require future ordinary extension/recovery to consider it a current predecessor/basis.

### Safe retirement

Anchor A may leave current frontier when either:

```text
1. semantic convergence:
   accepted J is genuinely after A and replaces A as current extension basis

OR

2. lifecycle/relevance retirement:
   owner semantics prove A's branch no longer participates in current ordinary extension,
   AND every still-live consumer depending on A retains its own bounded evidence route
```

Removing A from frontier:

- does not delete A;
- does not erase relation/provenance evidence;
- does not order A against other branches;
- does not imply A never happened.

### Scope decomposition

If many independent activities must remain current simultaneously, represent them as their actual typed scene/process/procedure chronology scopes where appropriate rather than making one scene frontier a vector over unrelated work.

### Semantic join

A real accepted join/barrier J after several frontier anchors may reduce the frontier to J without ordering the inputs among themselves.

Synthetic fictional joins solely for metadata compression remain forbidden.

---

# 6. R5 — consumer-bounded chronology guarantee

## Problem

Guaranteeing exact answers to every arbitrary historical temporal query forever would turn Step 5.9 into a permanent temporal database/retention subsystem.

## Resolution

Baseline guarantee:

> Every still-live or explicitly promised canonical consumer retains a bounded path to sufficient chronology evidence for every temporal/causal predicate admitted by that consumer's owner contract.

Protected consumers include, as applicable:

- armed temporal owners;
- active processes/deadlines;
- open Procedure/Continuation/execution dependencies;
- current scene/scope extension basis;
- current/later canonical state or lore/knowledge relations whose owning contract retains explicit chronology dependency;
- later Story/history/disclosure contracts only when those later stages explicitly enroll a retention dependency.

Not guaranteed by Step 5.9 alone:

> arbitrary exact historical temporal analytics over any pair/interval after lawful compaction.

A historical question may still be answerable from retained events/lore/Story/evidence. Chronology simply does not retain arbitrary detail solely to guarantee every future unanticipated query.

When gameplay establishes a historical relation as materially relevant canon, the accepted owner/evidence that now depends on it enrolls the relation under the normal protected-consumer rule.

---

# 7. R6 — bounded local metric constraint composition

Baseline chronology permits deterministic bounded relation composition for one concrete predicate.

Examples:

```text
ELAPSED(A,B,C,[5,10])
ELAPSED(B,D,C,[7,12])
    -> derived ELAPSED(A,D,C,[12,22])
```

or equivalent bound reasoning.

Rules:

1. composition occurs only inside compatible typed metric/order contexts or through explicit bridges;
2. only the consumer's bounded dependency component is loaded;
3. no campaign-wide temporal CSP service is introduced;
4. derived composed bounds need not be persisted;
5. a persisted summary is derivative and requires explicit coverage if later introduced;
6. a promised consumer whose dependency closure becomes unbounded violates its owner/routing contract and needs repair/summary/repartition rather than an ordinary history scan.

This is sufficient for deadlines/races/elapsed predicates without importing a general temporal-reasoning database.

---

# 8. R7 — stable chronology identity survives source movement

Chronology anchor/relation identity is semantic, not physical-source revision identity.

For accepted live/campaign movement:

```text
accepted anchor A in live E
    -> close
    -> absorption
    -> campaign retained evidence
```

A remains A.

Rules:

- source SHA/HEAD is read/currentness/fencing evidence, not chronology anchor identity;
- absorption preserves accepted anchor/relation IDs/keys required by downstream refs;
- current physical location is resolved through native recovery/routing/retention evidence;
- a durable cross-scope relation may reference another already-accepted live anchor without freezing that source merely for reference;
- a prospective/unpublished anchor is not valid durable cross-scope chronology evidence.

This aligns with Step-5.8 accepted stable live identity law.

---

# 9. R8 — same-coordinate is positive semantic evidence only

`SAME_COORDINATE(A,B,C)` may be accepted only when an owning mechanic/reconciliation/evidence contract establishes equality in C.

It is not derived from:

- same prior Git/live revision;
- same round label unless the rules contract defines that label as the relevant coordinate;
- similar commit timestamps;
- concurrent requests;
- absence of `PRECEDES` relation.

Same-coordinate does not imply causal independence.

Two causally ordered subevents may share one metric coordinate.

---

# 10. R9 — capability validation before unsupported temporal mutation

The owner-approved forward-extensible boundary is enforced before accepting a mutation when the requested semantics are recognizable as requiring:

- rewriting accepted past;
- branching/multiple authoritative worldlines;
- causal-loop/retrocausal rewrite semantics;
- timeline replacement/merge.

The baseline runtime does not first corrupt chronology and then call the contradiction "time travel".

If unsupported semantics become apparent only during resolution:

- the unsupported replacement transition remains unaccepted;
- existing accepted history remains intact;
- the operation surfaces a typed capability/adjudication boundary.

Dramaturg's preparation guard is advisory/preventive; deterministic validation remains the canon boundary.

---

# 11. Consolidated relation model after resolution

The minimum semantic core is now:

```text
STABLE TYPED ANCHOR

CAUSES(A,B)
    causal ancestry

PRECEDES(A,B,D)
    strict order in domain D

SAME_COORDINATE(A,B,C)
    positive equality in metric context C

ELAPSED(A,B,C,[lo,hi])
    exact/bounded quantitative evidence

ActiveExtensionFrontier(S)
    derivative bounded current extension basis

MetricPosition(provider_scope,C)
    exact/bounded/unknown current/anchor position evidence
```

Late relation establishment uses immutable typed assertion/evidence owned by a new accepted record/evidence source; no rewrite of old event meaning.

No generic `UNORDERED` persistence is added.

---

# 12. Integrity model after domain typing

Contradiction is evaluated only within relations that an owning contract says are comparable.

Examples:

### Contradiction

```text
PRECEDES(A,B,D)
PRECEDES(B,A,D)
```

```text
SAME_COORDINATE(A,B,C)
metric evidence in C proves A < B
```

```text
ELAPSED constraints in C have empty feasible set
```

```text
causal graph contains A -> ... -> A
```

### Not contradiction

```text
CAUSES(A1250,B1199)
PRECEDES(B1199,A1250,world_calendar)
```

```text
Scene A position in context CA
Scene B position in incompatible context CB
no bridge
```

```text
no order between independent A and B
```

The latter cases are legal domain separation/incomparability/indeterminacy.

---

# 13. Canonical-spec instructions

The consolidated canonical specification SHALL:

1. supersede untyped `STRICT_BEFORE` wording from the candidate with domain-typed `PRECEDES(A,B,D)`;
2. make causal-vs-calendar separation explicit with immutable-history time-travel example;
3. add deterministic temporal position-provider routing;
4. add protected-consumer relation dependency enrollment/discovery;
5. define `ActiveExtensionFrontier` safe retirement;
6. state consumer-bounded rather than arbitrary-history-complete retention guarantee;
7. permit bounded local metric composition;
8. preserve semantic anchor identity across live absorption/source movement;
9. constrain same-coordinate evidence;
10. enforce unsupported temporal capability before accepting rewrite semantics;
11. retain all candidate laws not contradicted by these resolutions;
12. list machine-realization debt without implementing it.

---

# 14. Resolution verdict

```text
blocking findings resolved      YES
architecture direction changed  NO
owner decision required         NO
candidate requires consolidation YES
ready for canonical spec        YES
```

Proceed to consolidated canonical Step-5.9 specification, then roadmap closure and fresh remote verification.