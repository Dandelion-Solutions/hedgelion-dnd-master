# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is a status/order document, not a duplicate normative specification.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

## Operating rule

- Exactly one numbered step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions.
- A step closes only after required artifacts/review/verification pass and every unresolved item has a later owner or explicit deferred/debt/backlog record.
- Step closure updates this roadmap and `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md`.
- After all major modules have designs, run one holistic architecture review over the complete ownership graph, schemas, logic, and cross-module relationships.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE / ASSURED** | Critical audit of catalog/class architecture and accepted baseline | Owned audit ledger + retrospective assurance | Every finding fixed, assigned, or consciously deferred; no unowned blocker |
| 2 | **COMPLETE / ASSURED** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases + retrospective assurance | No unresolved Step-2 blocker; maintenance/schema/unit-test validation passes |
| 3 | **IN PROGRESS — DECISION GATE ACTIVE** | `IntentPlan -> Resolution -> Signal/Event`, including LLM/core execution boundary, Procedure ownership and checkpointable continuation | Exact typed compound-turn/execution contract, operation/result/event/receipt model, reaction/choice suspension, idempotent continuation/checkpoint semantics | Multiple intents, partial completion, reactions, suspension/resume, retries, atomic mutation segments, trigger chains, deterministic receipts, LLM intent binding, procedure-local state, and in-flight recovery have one coherent deterministic contract with focused cases and critical review |
| 4 | `BLOCKED BY 3` | Lore, chapters, knowledge, secrets, minimum promotion interface | Durable truth/disclosure model + context-selection boundary | Public/restricted knowledge has one authority; durable references cannot depend on unpromoted local entities |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, event-local time | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model | Publication/live-scene ownership, cross-scene recovery, chronology, local time, continuity restoration, and shared revision semantics are coherent |
| 6 | `BLOCKED BY 5` | Modes, LLM execution budget, migration, catalog gaps, full seed, final closure | Mode profiles + final cross-cutting consistency pass | Mode isolation enforceable; migration/gap/seed ownership complete; full audit passes |

## Completed retrospective assurance overlay — Steps 1–2

The non-numbered assurance overlay is complete. It did not reopen Steps 1 or 2 as active roadmap stages.

Master plan and final resolution:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Final slice status:

```text
0A Catalog meta-model and class boundaries      ASSURED / AMENDED
0B Catalog evolution, identity, strata          ASSURED
A  Actor mechanical state                       ASSURED / AMENDED
B  Effects and Conditions                       ASSURED / AMENDED
C  Temporal and Recovery                        ASSURED / AMENDED
D  Mechanical evaluation/read boundaries        ASSURED / AMENDED
E  Whole Steps 1–2 integration                  ASSURED / AMENDED
```

Key assurance amendments now entering Step 3:

- one coherent `ResolvedCatalogContext`; incompatible adoption migrates coherently or blocks;
- catalog version `1.3.0` after admitting `runtime.procedure`;
- `runtime.procedure` is the independent operational owner for procedure-local participant ResourceState, distinct from Encounter/Resolution/Continuation;
- persistent Resource current state is normalized only from state-stable engine-derived capacity;
- current Condition effectiveness includes `condition.applicability`;
- live Effects may own finite owner-local scheduled-trigger due state independent of intrinsic lifetime;
- explicitly established quantitative elapsed evidence is retained even with no armed timer;
- invocation facts are a closed boolean `INVOCATION_ADJUDICATED` channel and reviewed state-sensitive Step-2 selectors admit `ENGINE_STATE` only;
- structured dependency/input metadata + scoped prospective DAG reject cycles and forbidden transitive inputs;
- live Effect recency must use compact immutable mechanical-order evidence independent of trace/event-body retention;
- checkpoints are immutable recovery frontiers, not parallel mutable owners.

Steps 1–2 remain closed.

## Step 3 preserved Decision Gate

Resume from:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-task-brief.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-research-draft.md`

The decision pass must incorporate the assurance constraints rather than restarting from the earlier baseline.

Current candidate responsibility split entering the gate:

```text
runtime.intent_plan
    message-level ordered orchestration

runtime.command
    idempotent executable clause envelope

runtime.resolution
    one Activity invocation

runtime.procedure
    one active rules-procedure lifetime / procedure-local Resource owner

ExecutionSegment
    prospective atomic local commit kernel (candidate concept)

runtime.continuation
    portable suspended Resolution authority, not Procedure owner

Signal / BoundaryOccurrence
    transient/prospective execution context

MechanicalEvent
    immutable post-commit mechanical fact
```

Material Step-3 decisions still requiring the human architect include exact execution ownership/segment/event boundaries and the associated trade-offs in the preserved Decision Brief. No candidate specification is canonicalized before that gate.

## Mandatory Step-3 carry-forward

1. Natural-language intent/referent mapping must produce typed bounded requests; LLM cannot invent engine-owned facts/capability IDs.
2. Accepted invocation facts carry explicit value/provenance/missing semantics and deterministic fingerprinting across suspension/retry.
3. Resolution/Continuation pin ResolvedCatalogContext identity; incompatible adoption cannot silently reinterpret suspended work.
4. Relevant commands/Resolutions bind one `runtime.procedure` identity and share its procedure-local Resources with child reactions.
5. A child commit advances the parent frontier; parent re-pins/recomputes from a safe phase rather than trusting stale prospective state.
6. Effect create/replace materializes compact immutable application-order evidence; refresh preserves it.
7. Owner-local scheduled triggers create ordinary bounded due execution and atomically resolve `REARM | UNARM | OWNER TERMINAL`.
8. Checkpointable in-flight state preserves source owners/inputs needed for deterministic resume; derived Agenda/DAG/winner caches remain rebuildable.
9. Runtime-only/noncanonical state may still be continuity-critical and therefore checkpointable.

## Later-stage ownership

### Step 4

- lore/knowledge/secrets/disclosure authority;
- knowledge-safe context selection and invocation-fact exposure;
- explicit promotion of durable truth.

### Step 5

- repository-backed runtime checkpoint publication/restoration;
- SOFT/HARD durability and multiplayer reconciliation;
- chronology evidence persistence/compaction and cross-scene time reconciliation;
- shared revision/conflict semantics and checkpoint cleanup.

### Step 6

- exact engine/ruleset/package/catalog snapshot identity metadata;
- full D&D seed and migration/catalog-gap closure;
- complete structured selector/input/dependency metadata coverage;
- exhaustive concrete ruleset verification and final architecture closure.

## Documentation debt

Before implementation planning relies on `DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`, align its stale pre-Step-2 examples with current normative Activity/Rule Element/assurance contracts. Older explanatory catalog-version labels are likewise non-authoritative relative to the normative inventory/machine catalogs at `1.3.0`.

## Exact continuation point

**Step 3 / Human Decision Gate: `IntentPlan -> Resolution -> Signal/Event`.**

Do not begin candidate specification or implementation before the decision gate resolves the material execution-boundary choices.
