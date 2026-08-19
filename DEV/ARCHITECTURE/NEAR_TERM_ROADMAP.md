# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes only after required artifacts/review/verification pass and every
  unresolved item has a later owner or explicit deferred/debt/backlog record.
- Step closure updates this roadmap and
  `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`.
- After all major modules have designs, run one holistic architecture review over
  the complete ownership graph, schemas, logic, and cross-module relationships.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE** | Critical audit of previously accepted architecture | Owned audit ledger | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases | Final integrated review has no unresolved Step-2 blocker; maintenance/schema/unit-test validation passes |
| 3 | **IN PROGRESS — ARCHITECTURE GATE OPEN** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary and checkpointable continuation | Exact typed compound-turn/execution contract, operation/result/event/receipt model, reaction/choice suspension, idempotent continuation/checkpoint semantics | Multiple intents, partial completion, reactions, suspension/resume, retries, atomic mutation segments, trigger chains, deterministic receipts, LLM intent binding, and in-flight recovery have one coherent deterministic contract with focused cases and critical review |
| 4 | `BLOCKED BY 3` | Lore, chapters, knowledge, secrets, minimum promotion interface | Durable truth/disclosure model + context-selection boundary | Public/restricted knowledge has one authority; durable references cannot depend on unpromoted local entities |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, event-local time | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model | Publication/live-scene ownership, cross-scene recovery, chronology, local time, continuity restoration, and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, LLM execution budget, migration, catalog gaps, full seed, final closure | Mode profiles + final cross-cutting consistency pass | Mode isolation enforceable; migration/gap/seed ownership complete; full audit passes |

## Step 2 closure

Final verdict:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

Current status index:

- `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`

Step 2 closes with the following core boundaries:

- Actor HP and LifeState are separate authorities;
- persistent and procedure-local Resources use one semantic API but different
  lifetime/storage owners;
- target-local Effects are one application per target; generic mutable stacks
  are absent;
- Effect reapplication matching/action, arbitration, support, and Rule Element
  combination are separate responsibilities;
- Conditions use independent aggregation and intrinsic-rule-scope axes;
- DurationSpec, TemporalBinding, and Temporal Agenda have distinct ownership;
- boundary producers and state-owner automatic responders are separate;
- Calculation Selectors, MechanicalContext accessors, and runtime domain queries
  are separate surfaces;
- MechanicalContext is revision-pinned and dependency cycles are rejected through
  registered contracts plus scoped prospective DAG validation;
- engine-owned mechanical facts cannot be supplied by the LLM as authority.

The machine contracts and focused Step-2 tests are aligned with these decisions.

## Cross-cutting requirement now entering Step 3 — LLM / deterministic core

The LLM/core boundary is no longer merely deferred because Step 3 owns the typed
execution interface where it becomes operationally material.

Step 3 must define at least:

```text
natural-language player input
    -> LLM interpretation / referent candidates
    -> typed intent clauses / Activity candidates
    -> deterministic identity + rules validation
    -> IntentPlan
    -> deterministic Resolution
    -> typed receipt/results
    -> LLM narration
```

The LLM may handle ambiguity, fiction-dependent adjudication, and semantic
mapping, but it may not invent executable capability IDs or assert engine-owned
mechanical facts. The architecture must not depend on the LLM keeping the full
catalog in prompt memory; it needs bounded lookup/hydration/context interfaces.

Step 4 later refines durable knowledge/context selection, but Step 3 owns the
execution-facing typed boundary.

## Cross-cutting requirement now entering Step 3 — runtime continuity

`runtime-only` / `non-canonical` does not mean `safe to lose`.

Step 3 must classify and define checkpointable in-flight execution state,
including as applicable:

- active procedure/encounter execution state;
- procedure-local ResourceState;
- partially executed IntentPlan/Resolution state;
- suspended choices/reactions/Continuations;
- pending typed obligations/triggers;
- mechanically material local metric-time anchors;
- idempotency/receipt information required for deterministic resume.

The Temporal Agenda remains a rebuildable index rather than checkpoint
mechanical authority. Recovery/checkpoint state must preserve enough source
information to reconstruct pending work without replay guessing.

Step 5 later owns repository publication/restoration, shared-state durability,
and checkpoint cleanup/expiry.

## Explicit later-stage ownership carried forward

### Step 4

- lore/knowledge/secrets/disclosure authority;
- LLM context selection and fiction-only adjudicated-fact refinement;
- durable promotion constraints.

### Step 5

- repository-backed runtime checkpoint publication/restoration;
- SOFT/HARD durability and multiplayer reconciliation;
- cross-scene/event-local-time integration;
- shared revision/conflict semantics and checkpoint cleanup.

### Step 6

- full D&D seed and migration/catalog-gap closure;
- exhaustive verification of concrete ruleset response tables, including health/
  lifecycle rules such as Long Rest HP restoration, without moving their
  ownership into RestPolicy or ResourceState.

## Exact continuation point

**Step 3 / Architecture Task Brief: `IntentPlan -> Resolution -> Signal/Event`.**

The first Step-3 design pass must explicitly include, rather than postpone:

1. typed LLM-to-core intent/reference binding;
2. compound/multiple-intent ordering and partial completion;
3. prospective state and atomic mutation-segment boundaries;
4. Signal/Event/BoundaryOccurrence authority and ordering;
5. reaction/choice suspension and continuation identity;
6. retries/idempotency/receipts;
7. trigger-chain execution bounds;
8. provenance-sensitive selection/adjudication;
9. checkpointable in-flight state and deterministic resume;
10. interaction with the Step-2 scoped dependency DAG and pinned state views.
