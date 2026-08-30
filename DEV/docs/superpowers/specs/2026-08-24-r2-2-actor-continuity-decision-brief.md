# R2.2 Decision Brief — Actor Continuity Ownership and Relationship Model

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-cognition-task-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-evidence-ledger.md`

Upstream canonical continuity:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`

---

## 1. Decision to make

R2.2 needs one material component/ownership decision:

> **Where should current non-mechanical Actor-private continuity live, and how much of goals/plans/relationships/transient cognition should be durably represented?**

The choice must preserve:

- one progressive `world.actor` identity;
- Step-4 `world.knowledge` as proposition-stance owner;
- objective truth / Actor cognition separation;
- player agency;
- sparse/event-driven cognition;
- recovery without hidden model memory;
- no universal psychology/social graph;
- R2.1 Story/history as evidence/orientation, not current cognition.

---

## 2. Facts established before the decision

### F1 — The missing state has a real current consumer

The Actor role already needs current identity/values, goals, relationships and commitments to behave consistently.

Current runtime doctrine likewise expects significant NPCs to preserve stable identity, current goals, relationships and active plans.

Therefore “synthesize everything transiently forever” has a real long-campaign quality/continuity cost.

### F2 — `world.knowledge` already owns belief/suspicion

R2.2 must not introduce a second biography/cognition field containing writable belief/suspicion copies.

### F3 — `world.actor` is already the natural individual Actor state owner

Actor identity and individual mutable state are progressively materialized there.

The current schema's broad `details` object is not itself a semantic design, but it demonstrates that physical Actor representation is not restricted to mechanics-only data.

### F4 — Directed relationships are semantically source-Actor-owned

The question is “how does A currently regard B?”, not a symmetric fact shared by A and B.

Even if later storage normalizes relationship data into separate files for cardinality/performance, semantic ownership can remain Actor A.

### F5 — Objective social facts are not relationship cognition

Organization membership, actual contract/debt occurrence, ownership, location and event history remain with their proper world/runtime owners.

Actor A may separately have a subjective/felt obligation, trust, fear or hostility toward B.

### F6 — Transient state is not durable by default

Current emotion/urgency/local intention should not become permanent biography merely because it existed for one turn.

If it must survive interruption and affect future behavior, it needs explicit invalidation/expiry semantics rather than a generic turn-count TTL.

---

## 3. Alternative A — Source-Actor-Owned Sparse Continuity — RECOMMENDED

Make the **source Actor** the semantic owner of current Actor-private continuity.

Conceptually:

```text
world.actor / Actor semantic ownership

FOUNDATION
    stable values / temperament / identity traits

DURABLE EVOLVING COGNITION
    long-term goal(s)
    current objective
    current intention / next intended action
    material commitments
    sparse directed relationship views
    explicit reconsideration cues where useful

TRANSIENT PRIVATE STATE
    short-lived affect / attention / urgency / local intention
    ephemeral by default
    persisted only when future continuity requires it
```

`world.knowledge` remains outside this structure and is referenced, not copied.

Physical storage is **not** forced to one JSON file by this decision. R2.7 may normalize a high-cardinality relation surface while preserving source-Actor semantic ownership.

### Relationship model

Baseline relation semantics:

```text
source_actor -> target_subject
    sparse material facets only
```

Recommended initial facet families:

- trust;
- affinity;
- fear;
- respect;
- hostility;
- felt obligation.

Rules:

- A->B and B->A are independent;
- absence means **not materially tracked**, not “neutral = 0”;
- facets are qualitative/sparse by default, not a universal numeric score;
- exact machine value vocabulary is agent-owned formalization after the architecture decision;
- `leverage` is not admitted as a baseline relationship facet because it often belongs to knowledge/resources/objective circumstances rather than relationship state.

### Goal / plan simplification

Do not introduce a general private plan graph.

Baseline continuity can express:

```text
long-term goal
current objective
next intended action / approach
reconsideration cue(s)
material commitment(s)
```

A richer retained private plan is admitted only if a concrete future consumer proves this insufficient.

### Transient rule

Transient Actor-private state is ephemeral by default.

Persist it only when:

- it must influence future behavior across interruption/context loss; and
- an explicit fictional-time/event/condition invalidation can be identified.

No generic TTL scheduler is introduced.

### Mutation rule

Use one bounded source Actor + one semantic assessment purpose:

```text
bounded eligible evidence/current state
    -> ActorCognitionDelta | EpistemicDeltaDraft | NO_CHANGE
    -> deterministic target/current-revision/source/shape validation
    -> native-owner commit if accepted
```

One ActorCognitionDelta may update a small coherent set of mutually dependent Actor-local fields. It is not an arbitrary whole-Actor rewrite.

`NO_CHANGE` creates no semantic state write merely to record that assessment happened.

### Advantages

- matches natural ownership;
- preserves progressive Actor materialization;
- avoids new global cognition/relationship authority;
- directionality is natural;
- low cross-record synchronization cost;
- sparse representation scales with actual significance;
- keeps `world.knowledge` cleanly separate;
- physical normalization remains reversible downstream.

### Risks

- a very socially connected major Actor may accumulate many relationship facets;
- careless machine realization could misuse `details` as an untyped blob;
- Actor record concurrency/file size may eventually justify physical normalization.

Those are R2.7 realization/performance questions unless evidence proves an independent semantic lifecycle earlier.

---

## 4. Alternative B — Separate Cognition and Relationship Semantic Owners

Introduce explicit durable owner families such as conceptual:

```text
actor_cognition[actor_id]
actor_relation[source_actor_id, target_subject_id]
```

Keep `world.actor` focused on identity/world/mechanical state.

### Advantages

- explicit typed boundary;
- independently addressable relations;
- easier direct indexing/querying for high-cardinality social state;
- independent lifecycle/concurrency possible.

### Costs / risks

- adds new semantic owners and records before independent lifecycle is proven;
- increases cross-owner consistency/recovery/publication work;
- easy to duplicate Actor foundation/current objective into both Actor and cognition record;
- separate relation owner can obscure that A->B state semantically belongs to A;
- more migration/schema/catalog work;
- pushes implementation/cardinality concerns into architecture prematurely.

### Assessment

Viable if later evidence proves independent lifecycle/concurrency/addressability is a semantic requirement, but **not justified now**.

---

## 5. Alternative C — Minimal Durable Cognition / Mostly Transient Synthesis

Persist only:

- existing `world.knowledge`;
- stable Actor identity/foundation;
- perhaps one current goal/commitment.

Reconstruct relationships/plans/transient cognition from Story/history/context on demand.

### Advantages

- minimum persistence surface;
- less mutation/repair machinery;
- avoids premature relationship vocabulary.

### Costs / risks

- weak long-campaign NPC character continuity;
- repeated reconstruction can drift;
- old history does not directly answer current relationship/intention;
- R2.1 expressly established that Story/history is not current Actor cognition;
- model/helpfulness prior can dominate when current subjective stance is absent;
- recurring important NPCs may behave inconsistently after context loss.

### Assessment

Too weak for the already existing Actor/runtime consumer contract.

---

## 6. Recommendation

Select **Alternative A — Source-Actor-Owned Sparse Continuity**.

Confidence: **HIGH**.

Reason:

> The unresolved data answers current questions about one Actor's own durable fictional cognition. The source Actor is therefore the natural semantic owner. Separate physical records can remain an implementation normalization option without creating a separate semantic authority now.

This design also preserves the strongest research insight — stable/durable/transient separation — without interpreting “three lifetimes” as “three new storage subsystems.”

---

## 7. Proposed R2.2 laws if A is approved

### R2.2-L1 — SOURCE ACTOR OWNS ACTOR-PRIVATE CONTINUITY

Current non-epistemic Actor-private continuity is semantically owned by the source Actor identity unless a specific concern already has another native owner.

Physical normalization does not transfer semantic ownership.

### R2.2-L2 — `world.knowledge` REMAINS THE PROPOSITION-STANCE OWNER

Actor continuity SHALL NOT copy writable `known/believed/suspected/rejected` state into biography/goals/relationships.

### R2.2-L3 — FOUNDATION / EVOLVING / TRANSIENT ARE LIFETIMES, NOT THREE STORES

Stable foundation, durable evolving cognition and transient private state have different mutation/retention rules but need not be separate semantic owners.

### R2.2-L4 — FOUNDATION CHANGES REQUIRE EXPLICIT MATERIAL CAUSE/AUTHORITY

Actor assessment cannot casually rewrite core identity/values/temperament merely to fit the current scene.

### R2.2-L5 — DURABLE EVOLVING COGNITION IS SPARSE AND CURRENT

Persist goals/objectives/intentions/commitments/relationship facets only where future Actor behavior materially depends on them.

History of their changes belongs to normal semantic event/evidence surfaces, not copied state logs.

### R2.2-L6 — RELATIONSHIPS ARE DIRECTED ACTOR VIEWS

`A -> B` and `B -> A` are independent. Actor A's cognition machinery may mutate only A's view.

Objective social facts remain with their native owners.

### R2.2-L7 — NO UNIVERSAL RELATIONSHIP SCORE

Material relationship state uses sparse typed facets rather than one scalar. Baseline facet families are trust, affinity, fear, respect, hostility and felt obligation.

Absence means untracked, not neutral zero.

### R2.2-L8 — NO GENERAL PRIVATE PLAN GRAPH

Baseline Actor continuity uses goal/current objective/next intention/reconsideration cues/material commitments. Richer planning remains conditional.

### R2.2-L9 — TRANSIENT PRIVATE STATE IS EPHEMERAL BY DEFAULT

Persist transient affect/urgency/local intention only when continuity across interruption requires it and an explicit fictional invalidation/expiry basis exists.

No turn-count TTL or generic scheduler is baseline architecture.

### R2.2-L10 — COGNITION IS SPARSE / EVENT-DRIVEN

No every-NPC/every-turn cognition loop is required. Assessment is triggered only for bounded relevant Actors by material evidence, pressure, opportunity, elapsed-fiction condition or another justified cause.

### R2.2-L11 — `NO_CHANGE` IS SUCCESS WITHOUT A SEMANTIC WRITE

A cognition assessment may conclude no durable mutation is warranted. Do not persist meaningless state merely to prove evaluation occurred.

### R2.2-L12 — DURABLE COGNITION MUTATION IS BOUNDED AND EVIDENCE-CARRYING

A mutation proposal is scoped to one source Actor and one semantic assessment purpose with bounded eligible evidence/current state. Deterministic control validates target/current revision/source membership/shape before commit.

Semantic fictional judgment remains nondeterministic proposal, not objective truth.

### R2.2-L13 — ACTOR DEPTH IS PROGRESSIVELY MATERIALIZED

Incidental Actors remain sparse. Supporting/significant Actors gain only continuity that future play needs. Missing untracked state does not authorize speculative filling.

### R2.2-L14 — PC VOLUNTARY MENTAL STATE REMAINS PLAYER-OWNED

NPC cognition machinery does not silently mutate a player-controlled PC's voluntary beliefs, emotions, loyalties, interpretations, goals or plans absent explicit player authorship or a genuine rules/world constraint.

### R2.2-L15 — STORY/HISTORY MAY INFORM BUT NOT ESTABLISH CURRENT COGNITION

R2.1 continuity may orient Actor assessment. Current Actor goals/relationships/intentions change only through the R2.2 owner path from eligible evidence/authority.

---

## 8. Downstream consequence

Approval of A gives R2.3 a source model containing:

- Actor foundation;
- sparse durable Actor cognition;
- directed relationship views;
- separate `world.knowledge` epistemics;
- transient state only when currently material/persisted under its lifecycle;
- current world/mechanical owners;
- R2.1 history/Story orientation.

R2.3 then decides retrieval, eligibility, ranking, budget, dedup and placement without inventing Actor semantics.

---

## 9. Exact owner decision requested

Choose one:

```text
A — Source-Actor-Owned Sparse Continuity  [RECOMMENDED]
B — Separate cognition / relationship semantic owners
C — Minimal durable cognition / mostly transient synthesis
```

Approval of **A** also approves the proposed R2.2-L1 through R2.2-L15 direction for candidate-spec formalization.

It does not approve concrete JSON/schema field names, file normalization, indexes or implementation.
