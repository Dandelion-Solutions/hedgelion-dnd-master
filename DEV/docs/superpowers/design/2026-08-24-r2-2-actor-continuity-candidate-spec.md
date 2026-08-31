# R2.2 Candidate Specification — Actor Continuity, Cognition and Directed Relationships

Status: **CANDIDATE ARCHITECTURE — PENDING ADVERSARIAL REVIEW**

Date: 2026-08-24

Owner decision:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-owner-decision.md`

Evidence:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-evidence-ledger.md`

Upstream continuity:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`

This specification defines semantic architecture only. Concrete schemas, physical file layout, indexes and runtime implementation remain downstream.

---

# 1. Core model

HDM uses **source-Actor-owned sparse continuity**.

One Actor identity may progressively materialize three lifetime classes:

```text
FOUNDATION
    stable identity/values/temperament-level continuity

DURABLE EVOLVING COGNITION
    goals / current objective / intention
    material commitments
    directed relationship views
    reconsideration cues

TRANSIENT PRIVATE STATE
    short-lived affect / attention / urgency / local intention
```

These are semantic lifetimes, not separate required storage systems.

`world.knowledge` remains the separate proposition-stance owner.

---

# 2. Ownership laws

## LAW R2.2-1 — SOURCE ACTOR OWNS CURRENT ACTOR-PRIVATE CONTINUITY

Current non-epistemic Actor-private continuity is semantically owned by the source Actor identity unless another accepted native owner already owns the concern.

Physical normalization into another file/index does not transfer semantic ownership.

## LAW R2.2-2 — `world.knowledge` REMAINS PROPOSITION-STANCE AUTHORITY

Writable current `aware/known/believed/suspected/rejected` state SHALL NOT be copied into Actor biography, goals or relationship fields.

Actor continuity may reference eligible epistemic state but does not duplicate it.

## LAW R2.2-3 — OBJECTIVE FACTS DO NOT BECOME SUBJECTIVE RELATIONSHIP STATE

Membership, ownership, contractual facts, debts, locations, resources and occurred events remain with their native owners.

An Actor may separately own subjective trust, affinity, fear, respect, hostility or felt obligation toward another subject.

---

# 3. Lifetime laws

## LAW R2.2-4 — FOUNDATION / EVOLVING / TRANSIENT ARE DIFFERENT LIFETIMES

Stable foundation, durable evolving cognition and transient private state have different mutation/retention semantics.

They need not be physically separated.

## LAW R2.2-5 — FOUNDATION CHANGES REQUIRE EXPLICIT MATERIAL CAUSE

Ordinary cognition assessment SHALL NOT rewrite core identity/values/temperament merely to fit the current scene or recent model output.

A foundation change requires explicit authored authority, a materially established long-term development, or another accepted cause strong enough to justify changing the durable Actor foundation.

## LAW R2.2-6 — DURABLE EVOLVING COGNITION IS SPARSE

Persist only current Actor-private state whose future behavior materially depends on survival across turns/context loss.

Baseline durable concerns may include:

- long-term goal;
- current objective;
- next intended action/approach;
- material commitment;
- reconsideration cue/condition;
- sparse directed relationship facets.

Do not persist every internal thought or generated rationale.

## LAW R2.2-7 — TRANSIENT PRIVATE STATE IS EPHEMERAL BY DEFAULT

Current affect, attention, urgency and local intention remain transient unless future continuity genuinely requires persistence.

If persisted, a transient state item SHALL have an explicit fictional invalidation basis such as:

- event occurrence;
- state transition;
- condition becoming false;
- materially relevant fictional-time boundary.

No generic turn-count TTL or background scheduler is introduced.

---

# 4. Directed relationship model

## LAW R2.2-8 — RELATIONSHIPS ARE SOURCE-ACTOR-OWNED DIRECTED VIEWS

Conceptually:

```text
(source_actor_id, target_subject_id) -> sparse relationship view
```

`A -> B` and `B -> A` are independent.

Actor A's cognition mutation may mutate only A-owned relationship state.

## LAW R2.2-9 — NO UNIVERSAL RELATIONSHIP SCORE

Baseline material facet families are:

```text
trust
affinity
fear
respect
hostility
felt_obligation
```

Absence means **not materially tracked**, not neutral zero.

R2.2 does not require numeric scales. Concrete value vocabulary is machine-realization work and should prefer the smallest useful qualitative/typed contract unless a real mechanic requires numerical precision.

## LAW R2.2-10 — RELATIONSHIP STATE IS NOT A SOCIAL GRAPH AUTHORITY

Relationship views do not establish objective facts about the target, mutual consent, ownership, allegiance, legal obligation or shared history.

They are source-Actor cognition only.

---

# 5. Goals, intentions and plans

## LAW R2.2-11 — BASELINE PLANNING IS NARROW

Baseline Actor continuity may represent:

```text
long_term_goal
current_objective
next_intention / approach
reconsideration_cues
material_commitments
```

No general private plan graph, branching strategy tree or persistent chain-of-thought is introduced.

A richer retained planning abstraction remains conditional on a demonstrated consumer need.

---

# 6. Cognition assessment

## LAW R2.2-12 — COGNITION IS SPARSE AND EVENT-DRIVEN

HDM SHALL NOT run every Actor through cognition every turn.

A cognition assessment requires a bounded relevant Actor and a material cause such as:

- newly accepted evidence;
- direct interaction;
- material world/process change;
- opportunity/resource change;
- fictional-time condition;
- current objective/commitment conflict;
- explicit reconsideration cue.

Dormant/background Actors remain unchanged unless a legitimate trigger requires assessment.

## LAW R2.2-13 — ASSESSMENT PURPOSE IS EXPLICIT

A cognition assessment uses a narrow purpose rather than an undifferentiated “think as NPC” call.

Conceptual purposes may include:

```text
REACT
REFLECT
PLAN
RECONSIDER
RELATIONSHIP_UPDATE
```

Epistemic proposition updates continue through the Step-4 `world.knowledge` path rather than a duplicate R2.2 mode.

Exact runtime orchestration/activation vocabulary is R2.4 work; R2.2 defines semantic purposes only.

## LAW R2.2-14 — `NO_CHANGE` IS A SUCCESSFUL OUTCOME

Assessment may conclude that no durable Actor state should change.

`NO_CHANGE` creates no semantic write merely to prove assessment occurred.

## LAW R2.2-15 — ONE ASSESSMENT PRODUCES ONE BOUNDED ACTOR-LOCAL DELTA

A semantic assessment is scoped to:

```text
one source Actor
+ one assessment purpose
+ bounded eligible evidence/current state
```

It may propose one coherent Actor-local delta affecting a small set of mutually dependent continuity fields.

R2.2 does not impose one physical field/file mutation per assessment.

## LAW R2.2-16 — DETERMINISTIC CONTROL VALIDATES THE WRITE BOUNDARY

Before commit, deterministic control validates at least:

- source Actor identity;
- target/current revision;
- allowed semantic owner;
- eligible/source evidence membership where represented;
- structural/value shape;
- player-agency restrictions;
- absence of duplicate `world.knowledge` mutation through Actor fields.

Semantic fictional judgment itself remains bounded nondeterministic proposal rather than objective truth.

---

# 7. Progressive materialization and loading discipline

## LAW R2.2-17 — ACTOR DEPTH IS PROGRESSIVELY MATERIALIZED

Incidental Actors may remain name/role-level sparse.

Supporting/significant Actors gain only foundation/cognition/relationship detail that future play actually requires.

Missing untracked state does not authorize speculative durable filling.

## LAW R2.2-18 — FULL ACTOR LOAD IS NOT REQUIRED FOR DISCOVERY

The runtime SHALL be able to discover that an Actor may be relevant to the current scene/location/decision without loading the Actor's complete continuity record into LLM context.

This law preserves lazy-loading/token discipline.

R2.2 does not define the concrete discovery index.

## LAW R2.2-19 — DISCOVERY METADATA IS DERIVED, NOT ACTOR AUTHORITY

A compact scene/location/entity discovery surface may contain only the metadata needed to locate/rank potential sources, such as stable identity/type/path/ref and limited relevance/placement descriptors.

It SHALL NOT become writable authority for:

- Actor cognition;
- relationship state;
- current world truth;
- location when another native owner owns location;
- knowledge/disclosure;
- exact history.

Stale/missing derived discovery metadata must degrade to bounded stronger-source lookup/rebuild rather than silently change canon.

## LAW R2.2-20 — CURRENT REPOSITORY SURFACES ARE INPUTS, NOT PRE-SELECTED IMPLEMENTATION

R2.3/R2.7 may reuse compatible existing surfaces including:

- `CURRENT.active_scenes`;
- `SCENE.location_id` and current scene summary;
- scene participant/PC/thread/environment refs;
- `INDEX/NPC_INDEX.yaml`, `ITEM_INDEX.yaml`, `LOCATION_INDEX.yaml`, `SCENE_INDEX.yaml`;
- live-scene mutation/touch evidence.

R2.2 does not declare any one of these sufficient or authoritative for context discovery.

---

# 8. Player agency

## LAW R2.2-21 — PC VOLUNTARY MENTAL STATE REMAINS PLAYER-OWNED

NPC/Actor cognition machinery SHALL NOT silently author a player-controlled PC's voluntary:

- belief/suspicion/rejection;
- emotion;
- loyalty;
- interpretation;
- goal;
- plan;
- speech;
- consent/commitment choice.

Explicit player authorship or a genuine rules/world constraint is required where such state is represented.

---

# 9. R2.1 continuity boundary

## LAW R2.2-22 — STORY/HISTORY MAY INFORM BUT NOT ESTABLISH CURRENT COGNITION

Eligible R2.1 Story/history may provide evidence/orientation for Actor assessment.

It cannot itself establish that an Actor currently wants, believes, intends or feels something.

Current cognition changes only through the proper Actor/`world.knowledge` owner path.

---

# 10. R2.3 handoff — lazy context discovery

R2.3 receives a mandatory two-level semantic requirement:

```text
LEVEL 1 — DISCOVERY
    compact bounded scene/location/entity candidate metadata
    enough to know what may be worth loading

LEVEL 2 — SEMANTIC LOAD
    fetch only the Actor/Asset/knowledge/Story/history/current owner material
    required for the concrete role decision packet
```

R2.3 must determine:

- how candidate manifests are constructed and refreshed;
- whether scene-local refs, reverse indexes and typed selectors are combined;
- how NPCs/assets/features at a location become discoverable without global scans;
- how off-scene but causally relevant entities enter candidates;
- role/subject/player eligibility before full context inclusion;
- staleness/currentness checks;
- token/cost-aware progressive representation;
- fallback when an index is stale or incomplete;
- how secrets are prevented from leaking through index labels/metadata;
- diagnostics/trace for discovery and later inclusion/exclusion.

R2.3 SHALL NOT require full entity records merely to perform first-pass discovery.

---

# 11. Rejected and conditional designs

Rejected baseline designs:

- separate global cognition authority;
- separate relationship semantic authority solely for query/cardinality convenience;
- symmetric relationship state;
- universal relationship scalar;
- universal psychology ontology;
- general persistent private-plan graph;
- permanent retention of generated Actor reasoning;
- every-Actor/every-turn cognition;
- generic turn-count TTL;
- reconstructing current Actor cognition from Story alone;
- full-record preload for relevance discovery.

Conditional:

- high-cardinality physical relationship normalization — R2.7/performance evidence;
- richer retained private planning — demonstrated consumer need;
- additional Actor-local indexes — R2.3/R2.7 evidence;
- authored staged evolution — preserved research trigger for major authored companion/NPC arcs;
- selective Actor-core forgetting/pruning — only under demonstrated Actor-local pressure.

---

# 12. Downstream contract

R2.3 may assume these semantic source classes exist without inventing them:

- Actor foundation;
- sparse durable Actor cognition;
- directed source-Actor relationship views;
- separate `world.knowledge` epistemics;
- transient private state only when material under its lifecycle;
- current world/mechanical owners;
- R2.1 Story/history orientation;
- compact derived discovery metadata sufficient to avoid mandatory full-record discovery loads.

R2.3 owns retrieval, candidate assembly, eligibility, ranking, budgets, dedup, representation downgrade, placement, trace and lazy-load mechanics.

---

# 13. Candidate exit questions for adversarial review

The review must challenge at least:

1. whether source-Actor ownership creates hidden cross-Actor consistency obligations;
2. whether relationship facets duplicate objective social facts;
3. whether transient state can become immortal through missing expiry;
4. whether `NO_CHANGE` avoids forced drift without starving meaningful updates;
5. whether the assessment delta boundary is actually bounded;
6. whether PC agency can be violated through indirect relationship/cognition inference;
7. whether Actor foundation can drift through repeated “small” updates;
8. whether Story/history can launder stale cognition into current state;
9. whether sparse continuity loses material history after context loss;
10. whether lazy discovery can function without full Actor loads or a global scan;
11. whether discovery indexes can leak secrets or become stale pseudo-authority;
12. whether off-scene causal relevance is lost by a location-only manifest.
