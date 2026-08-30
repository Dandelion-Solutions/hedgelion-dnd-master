# R2.2 Owner Decision — Source-Actor-Owned Sparse Continuity

Status: **OWNER-APPROVED ARCHITECTURE DECISION**

Date: 2026-08-24

Decision brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-decision-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-evidence-ledger.md`

Upstream continuity architecture:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`

---

## 1. Decision

The owner selects:

> **A — SOURCE-ACTOR-OWNED SPARSE CONTINUITY**

Current non-mechanical Actor-private continuity is semantically owned by the source Actor identity unless a concern already has another accepted native owner.

This decision approves the R2.2-L1 through R2.2-L15 direction from the Decision Brief for candidate-spec formalization.

It does **not** approve concrete JSON field names, file normalization, indexes, storage paths or implementation.

---

## 2. Approved semantic model

R2.2 distinguishes lifetimes without creating one store per lifetime:

```text
SOURCE ACTOR

FOUNDATION
    stable values / temperament / identity traits

DURABLE EVOLVING COGNITION
    long-term goal(s)
    current objective
    current intention / next intended action
    material commitments
    sparse directed relationship views
    reconsideration cues where useful

TRANSIENT PRIVATE STATE
    short-lived affect / attention / urgency / local intention
    ephemeral by default
    persisted only when future continuity requires it
```

`world.knowledge` remains the separate current proposition-stance owner and is referenced rather than copied.

---

## 3. Approved relationship direction

Relationship semantics are Actor-owned and directed:

```text
source_actor -> target_subject
```

`A -> B` and `B -> A` are independent.

Baseline material facet families are:

- trust;
- affinity;
- fear;
- respect;
- hostility;
- felt obligation.

Absence means untracked, not neutral zero.

No universal relationship scalar or symmetric social state is approved.

Objective social facts remain with their proper world/runtime owners.

---

## 4. Approved cognition discipline

Actor cognition is sparse/event-driven rather than every-Actor/every-turn simulation.

A bounded assessment may use explicit purposes such as react, reflect, plan, reconsider or another narrowly defined Actor-local purpose. `world.knowledge` changes continue through the Step-4 epistemic owner path rather than through duplicate Actor fields.

`NO_CHANGE` is a successful assessment outcome and creates no semantic write merely to prove cognition ran.

A durable Actor-local mutation uses bounded eligible evidence/current state and deterministic target/current-revision/source/shape validation before commit. Semantic fictional judgment remains nondeterministic proposal, not objective truth.

---

## 5. Player-agency boundary

NPC cognition machinery SHALL NOT silently mutate a player-controlled PC's voluntary:

- beliefs;
- emotions;
- loyalties;
- interpretations;
- goals;
- plans;
- consent/commitment choices

unless explicit player authorship or a genuine rules/world constraint authorizes the change.

---

## 6. Progressive materialization

Actor continuity follows the existing progressive-materialization doctrine:

- incidental Actors remain sparse;
- supporting/significant Actors acquire only continuity that future play materially needs;
- missing untracked cognition is not permission to invent durable state;
- deeper continuity is loaded/materialized only when a real consumer requires it.

---

## 7. Owner clarification — lazy LLM loading is a required downstream constraint

The owner explicitly reiterates that LLM/runtime context must use **lazy loading** to avoid unnecessary context growth and token consumption.

This creates the following architecture constraint without changing R2.2 ownership:

> **Full Actor/Asset/etc. records must not be required merely to discover that an entity may be relevant to the current scene/location/decision.**

R2.2 therefore hands R2.3 a mandatory requirement for a lightweight discovery tier.

The exact physical/index realization is **not** decided here.

Current repository evidence already provides compatible candidate surfaces:

- compact `CURRENT.active_scenes` routing;
- `SCENE` with `location_id`, participant/PC refs, active threads, relevant item refs, persistent feature refs and compact actionable summary;
- campaign `INDEX/` families including NPC, Item, Location and Scene indexes;
- live-scene touched/claim evidence for current shared mutation horizons.

These are candidate inputs to R2.3, not automatically new authorities.

R2.3 must distinguish:

```text
DISCOVERY / RELEVANCE METADATA
    compact derived/rebuildable locator/index information

FULL SEMANTIC SOURCE
    Actor / Asset / knowledge / Story / history / mechanics owner loaded only when required
```

A discovery index/projection SHALL NOT become writable truth, current cognition, current location authority or a substitute for the native owner.

---

## 8. Rejected / conditional directions

Rejected for current scope:

- separate global cognition owner;
- separate relationship semantic authority merely for indexing/cardinality convenience;
- universal relationship score;
- generic private-plan graph;
- permanent storage of every transient emotion/thought;
- every-Actor/every-turn cognition loop;
- generic turn-count TTL scheduler;
- reconstructing current cognition from Story/history alone.

Conditional:

- physical normalization of high-cardinality relationships into separate files — only if later machine-realization/performance evidence warrants it while preserving source-Actor semantic ownership;
- richer retained private planning — only if a concrete downstream consumer proves the approved goal/objective/intention/commitment model insufficient;
- additional Actor-local indexing — R2.3/R2.7 only if bounded discovery/retrieval requires it.

---

## 9. Next architecture work

The agent may proceed with:

1. R2.2 candidate specification;
2. adversarial review;
3. canonicalization/closure if no new material owner decision appears.

The lazy-loading/index requirement must be preserved as an explicit R2.3 handoff rather than solved prematurely inside R2.2.
