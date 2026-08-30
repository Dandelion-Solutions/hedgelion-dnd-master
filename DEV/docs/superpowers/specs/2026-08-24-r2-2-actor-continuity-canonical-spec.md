# R2.2 Canonical Specification — Actor Continuity, Cognition and Directed Relationships

Status: **CANONICAL ARCHITECTURE — R2.2**

Date: 2026-08-24

Owner decision:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-owner-decision.md`

Derivation:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-cognition-task-brief.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-evidence-ledger.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-decision-brief.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-candidate-spec.md`
- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-adversarial-review.md`

This specification incorporates adversarial clarifications AR-1 through AR-6. It defines architecture only; implementation remains deferred.

---

# 1. Canonical invariant

HDM uses **source-Actor-owned sparse continuity**.

The source Actor semantically owns its current non-epistemic private continuity unless an accepted native owner already owns the concern.

Three lifetime classes are distinguished without creating three required stores:

```text
FOUNDATION
    stable values / temperament / identity-level continuity

DURABLE EVOLVING COGNITION
    goals / current objective / next intention
    material commitments
    directed relationship views
    reconsideration cues

TRANSIENT PRIVATE STATE
    short-lived affect / attention / urgency / local intention
```

`world.knowledge` remains the separate current proposition-stance owner.

Core rule:

> **Actor continuity describes what this Actor currently wants/intends/regards, not what is objectively true and not what another Actor or player-controlled PC must think.**

---

# 2. Ownership

## LAW R2.2-1 — SOURCE ACTOR OWNS ACTOR-PRIVATE CONTINUITY

Current non-epistemic Actor-private continuity is semantically owned by the source Actor identity.

Physical normalization into another file, table, index or shard does not transfer semantic ownership.

## LAW R2.2-2 — `world.knowledge` REMAINS PROPOSITION-STANCE AUTHORITY

Current `aware/known/believed/suspected/rejected` state remains exclusively under the Step-4 `world.knowledge` owner contract.

Actor continuity SHALL NOT maintain a writable duplicate belief/suspicion store.

## LAW R2.2-3 — OBJECTIVE SOCIAL FACTS REMAIN WITH NATIVE OWNERS

Relationship/cognition state SHALL NOT establish objective facts such as:

- organization membership;
- actual legal/contractual obligation;
- ownership;
- physical location;
- resource possession;
- target intent;
- reciprocal relationship state;
- mutual consent.

An Actor may separately own subjective trust, fear, affinity, respect, hostility or felt obligation informed by such facts.

---

# 3. Lifetime semantics

## LAW R2.2-4 — FOUNDATION / EVOLVING / TRANSIENT ARE LIFETIMES, NOT THREE STORES

The three lifetime classes have distinct mutation/retention semantics but need not be separate semantic owners or physical records.

## LAW R2.2-5 — FOUNDATION HAS A STRONGER MUTATION BOUNDARY

Ordinary cognition assessment cannot mutate foundation fields by accumulation.

A foundation change requires an explicitly classified **foundation transition** supported by material accepted cause/authority stronger than an ordinary evolving-cognition update.

Examples may include:

- explicit authored revision;
- materially established long-term transformation;
- another accepted world/rules effect that genuinely changes durable identity/values.

Repeated small ordinary cognition deltas SHALL NOT silently rewrite Actor foundation.

## LAW R2.2-6 — DURABLE EVOLVING COGNITION IS SPARSE

Persist only Actor-private state whose future behavior materially depends on survival across turns/context loss.

Baseline durable concerns may include:

```text
long_term_goal
current_objective
next_intention / approach
material_commitments
reconsideration_cues
sparse directed relationship facets
```

Do not persist every generated thought, rationale or possible plan.

## LAW R2.2-7 — TRANSIENT PRIVATE STATE IS EPHEMERAL BY DEFAULT

Current affect, attention, urgency and local intention remain transient unless future continuity requires persistence.

A persisted transient item must have inspectable invalidation tied where possible to existing fictional state/time/event owners, for example:

- event occurrence;
- state transition;
- condition becoming false;
- relevant fictional-time boundary;
- explicit owner revision/change.

R2.2 introduces no generic turn-count TTL, heartbeat or scheduler.

---

# 4. Directed relationships

## LAW R2.2-8 — RELATIONSHIPS ARE SOURCE-ACTOR-OWNED DIRECTED VIEWS

Conceptually:

```text
(source_actor_id, target_subject_id) -> sparse relationship view
```

`A -> B` and `B -> A` are independent.

Actor A's cognition machinery may mutate only A-owned relationship state.

## LAW R2.2-9 — BASELINE FACETS ARE SPARSE AND TYPED

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

## LAW R2.2-10 — NO UNIVERSAL RELATIONSHIP SCORE

R2.2 does not collapse relationship state into one scalar.

Concrete machine values should prefer the smallest useful qualitative/typed vocabulary unless a real mechanic requires numerical precision.

## LAW R2.2-11 — SUBJECTIVE RELATIONSHIP FACETS DO NOT BECOME OBJECTIVE SOCIAL FACTS

A relationship view may reference objective/evidentiary sources but cannot prove the target's state or an external contract merely because the Actor feels/assumes it.

---

# 5. Goals and plans

## LAW R2.2-12 — BASELINE ACTOR PLANNING IS NARROW

Baseline continuity may represent:

```text
long_term_goal
current_objective
next_intention / approach
reconsideration_cues
material_commitments
```

No general private plan graph, strategy DAG or persistent chain-of-thought is introduced.

Richer retained private planning remains conditional on a demonstrated consumer need.

---

# 6. Cognition assessment

## LAW R2.2-13 — COGNITION IS SPARSE AND EVENT-DRIVEN

HDM SHALL NOT run every Actor through cognition every turn.

Assessment requires a bounded relevant Actor and material cause such as:

- newly accepted evidence;
- direct interaction;
- material world/process change;
- opportunity/resource change;
- fictional-time condition;
- current objective/commitment conflict;
- explicit reconsideration cue.

Dormant/background Actors remain unchanged absent legitimate trigger.

## LAW R2.2-14 — ASSESSMENT PURPOSE IS EXPLICIT

Actor cognition uses a narrow semantic purpose rather than an undifferentiated “think as NPC” operation.

Conceptual purposes include:

```text
REACT
REFLECT
PLAN
RECONSIDER
RELATIONSHIP_UPDATE
```

Epistemic proposition updates remain on the Step-4 `world.knowledge` path.

R2.4 later owns exact runtime phase/orchestration vocabulary.

## LAW R2.2-15 — `NO_CHANGE` IS SUCCESS WITHOUT A SEMANTIC WRITE

A cognition assessment may determine that no durable Actor state should change.

`NO_CHANGE` creates no semantic write merely to prove assessment occurred.

## LAW R2.2-16 — ONE ASSESSMENT PRODUCES ONE BOUNDED ACTOR-PURPOSE DELTA

One assessment is scoped to:

```text
one source Actor
+ one semantic assessment purpose
+ bounded eligible evidence/current state
```

It may propose one coherent Actor-local delta affecting a small set of mutually dependent fields.

R2.2 does not require one physical field/file mutation.

## LAW R2.2-17 — DETERMINISTIC CONTROL VALIDATES THE WRITE BOUNDARY

Before commit, deterministic control validates as applicable:

- source Actor identity;
- target/current revision;
- semantic owner eligibility;
- bounded source/evidence membership;
- allowed shape/value class;
- player-agency restrictions;
- absence of duplicate `world.knowledge` mutation;
- foundation-transition classification when foundation is affected;
- inspectable invalidation basis for persisted transient state.

Semantic fictional judgment remains bounded nondeterministic proposal rather than objective truth.

---

# 7. Progressive materialization

## LAW R2.2-18 — ACTOR DEPTH IS PROGRESSIVELY MATERIALIZED

Incidental Actors may remain name/role-level sparse.

Supporting/significant Actors gain only foundation/cognition/relationship detail that future play materially needs.

Missing untracked state does not authorize speculative durable filling.

## LAW R2.2-19 — DEEP CONTINUITY IS NOT A PRELOAD REQUIREMENT

The existence of detailed Actor continuity does not require that complete continuity be placed in every role context where the Actor is merely nearby or potentially relevant.

R2.3 owns bounded selection and loading.

---

# 8. Player agency

## LAW R2.2-20 — PC VOLUNTARY MENTAL STATE REMAINS PLAYER-OWNED

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

## LAW R2.2-21 — STORY/HISTORY MAY INFORM BUT NOT ESTABLISH CURRENT COGNITION

Eligible R2.1 Story/history may provide evidence/orientation for Actor assessment.

It cannot itself establish that an Actor currently wants, intends, believes or feels something.

Current cognition changes only through the applicable source Actor / `world.knowledge` owner path.

---

# 10. Lazy discovery and LLM loading contract

The owner explicitly requires lazy LLM loading to control context growth/token use while still allowing the runtime to know what may be relevant in the current scene/location/decision.

R2.2 therefore establishes the following downstream laws without fixing physical indexes.

## LAW R2.2-22 — DISCOVERY MUST NOT REQUIRE FULL ENTITY LOAD

The runtime SHALL be able to discover that an Actor/Asset/other entity may be relevant without first loading its complete semantic record into the LLM context.

Full Actor continuity is a second-stage semantic source, not a first-stage discovery prerequisite.

## LAW R2.2-23 — DISCOVERY METADATA IS DERIVED, NOT AUTHORITY

A compact scene/location/entity discovery surface may contain only bounded locator/relevance metadata needed to identify candidate sources.

It SHALL NOT become writable authority for:

- Actor cognition;
- relationship state;
- objective truth;
- location when another native owner owns current location;
- knowledge/disclosure;
- exact history.

## LAW R2.2-24 — INDEX OMISSION IS NOT GENERAL PROOF OF ABSENCE

Absence from a derived index/manifest SHALL NOT prove that an entity/fact is absent unless that exact discovery contract provides a current exhaustive guarantee for the queried scope.

When correctness depends on presence/absence, use a current source/contract capable of proving it.

## LAW R2.2-25 — DISCOVERY CURRENTNESS FOLLOWS ROUTED AUTHORITY

Candidate discovery and material verification SHALL respect the same routed current-authority model as ordinary state reads.

During a live epoch, campaign-base Actor/location/index data may be stale relative to live scene/entity overlays, created entities and touched/current owner state.

Derived campaign indexes remain hints unless their currentness is established for the scope.

## LAW R2.2-26 — DISCOVERY IS MULTI-CHANNEL, NOT LOCATION-ONLY

Physical co-location is one relevance channel, not the complete relevance model.

R2.3 must also support typed channels such as:

- explicit entity/subject reference;
- active thread/dependency;
- causal/process dependency;
- ownership/relationship link when materially relevant;
- recent accepted event/evidence;
- current action/mechanics dependency;
- other bounded registered selectors.

## LAW R2.2-27 — DISCOVERY METADATA MUST NOT LEAK SECRET CONTENT

Low-cost candidate discovery does not bypass role/subject/player eligibility.

Opaque IDs/type/path and non-secret selector metadata may be available before deeper load where safe.

Secret-bearing names, descriptions, relationship facts, motivations, Story spoilers or other protected metadata require ordinary eligibility before exposure to the active role/context.

## LAW R2.2-28 — CURRENT REPOSITORY INDEXES ARE CANDIDATE REALIZATION SURFACES ONLY

Existing surfaces that R2.3/R2.7 may reuse include:

- compact `CURRENT.active_scenes`;
- `SCENE.location_id`, actionable summary, PC/participant/thread/environment refs;
- campaign `INDEX/NPC_INDEX.yaml`, `ITEM_INDEX.yaml`, `LOCATION_INDEX.yaml`, `SCENE_INDEX.yaml`;
- live-scene overlays/created/touched owner evidence.

R2.2 does not declare any one of them sufficient or authoritative for discovery.

---

# 11. R2.3 handoff

R2.3 receives the following semantic source model:

- Actor foundation;
- sparse durable Actor cognition;
- directed source-Actor relationship views;
- separate `world.knowledge` epistemics;
- transient private state only when material under its lifecycle;
- current world/mechanical owners;
- R2.1 Story/history orientation;
- compact derived discovery metadata that allows candidate discovery without mandatory full-record loads.

R2.3 must define a bounded lazy context path conceptually equivalent to:

```text
DISCOVER
    compact typed candidate metadata

SELECT / VERIFY
    role + subject + purpose eligibility/currentness

LOAD
    only semantic sources required for the decision packet

PROJECT
    bounded representation for the active logical role
```

R2.3 owns:

- candidate-manifest construction;
- typed discovery channels;
- reverse indexes/scene-local refs combination;
- staleness/currentness fallback;
- off-scene causal relevance;
- ranking/budget/dedup;
- representation downgrade;
- secret-safe candidate metadata;
- inclusion/exclusion trace;
- failure/defer behavior.

---

# 12. Research disposition

| Item | Canonical R2.2 result |
|---|---|
| D10 stable/durable/transient | **ADOPTED / REFINED** — three lifetimes under one source-Actor semantic owner; foundation mutation is explicit; transient persistence needs inspectable invalidation. |
| D11 truth/knowledge/belief/intention | **PARTLY INHERITED + DELTA ADOPTED** — Step-4 epistemics remain `world.knowledge`; R2.2 owns only missing non-epistemic Actor continuity. |
| D12 directed relationships/player agency | **ADOPTED** — A->B independent of B->A; PC voluntary mental state excluded. |
| D13 sparse/event-driven cognition | **ADOPTED** — bounded relevant Actors/material triggers; no always-on simulation. |
| S07 explicit cognition modes | **ADOPTED AS SEMANTIC PURPOSES** — narrow purposes, no new orchestration framework. |
| S10 NO_CHANGE | **ADOPTED** — valid assessment without forced state mutation. |
| S11 transient TTL | **PROBLEM ADOPTED / TURN-TTL REJECTED** — fictional event/state/time invalidation replaces generic turn counter. |
| D09 evidence-bound mutation | **ADOPTED AS SPECIALIZED APPLICATION** — bounded Actor-purpose delta + deterministic owner/currentness/source/shape checks. |
| S27 one mutation per assessment | **REFORMULATED** — one bounded Actor-purpose delta may update several coherent dependent fields. |
| S06 bounded active cast | **INHERITED / PRESERVED** — progressive materialization/current runtime already establish the principle. |
| S08 protected core/selective forgetting | **DORMANT** — revisit under demonstrated Actor-local pressure. |
| S09 staged evolution | **DORMANT** — revisit for authored companions/major NPC arcs. |

---

# 13. Rejected / conditional architecture

Rejected baseline designs:

- separate global cognition authority;
- separate relationship semantic authority solely for indexing/cardinality convenience;
- symmetric relationship state;
- universal relationship scalar;
- universal psychology ontology;
- generic persistent private-plan graph;
- permanent generated Actor-reasoning retention;
- every-Actor/every-turn cognition;
- generic turn-count TTL;
- current cognition reconstructed from Story alone;
- full-record preload for entity discovery;
- derived index as negative/closed-world authority by default.

Conditional:

- physical high-cardinality relationship normalization — only if later machine/performance evidence warrants it while source-Actor semantic ownership remains unchanged;
- richer retained private planning — demonstrated consumer need;
- additional Actor-local/index projections — R2.3/R2.7 evidence;
- authored staged evolution — preserved dormant trigger;
- selective Actor-core forgetting/pruning — demonstrated Actor-local pressure.

---

# 14. Non-goals

R2.2 does not define:

- concrete JSON field names;
- file/shard/index layout;
- candidate ranking/token budgets;
- exact Context Runtime selectors;
- LLM role orchestration;
- multiplayer collaboration protocol;
- machine migration/implementation.

Those remain downstream under the active roadmap.
