# HDM Mechanical Architecture — Six-Step Roadmap

Status: **ACTIVE WORKING PLAN**

Target branch: `feature/mechanical-runtime-hot-state`

This roadmap is the sequencing gate for the current architecture program. It is
a status/order document, not a duplicate normative specification.

The canonical engine-wide architecture workflow is `DEV/DESIGN_PROCESS.md`;
HDM-specific additions are in `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

## Operating rule

- Exactly one numbered step may be `IN PROGRESS`.
- Later steps may be inspected only to expose dependencies/contradictions; they
  do not silently become the active task.
- A step closes only when its required artifacts exist, its review/verification
  gates pass, and every unresolved item is assigned to a later step or recorded
  as deliberate deferred work/debt/backlog.
- Every completed numbered step updates this roadmap and
  `DEV/ARCHITECTURE/CATALOG_DESIGN_STATUS.md` in the same closure change.
- Canonical architecture is reviewed before implementation.
- After all major architecture modules have designs, run one additional holistic
  review over the entire architecture, ownership graph, schemas, logic, and
  cross-module relationships.

## Roadmap

| # | Status | Scope | Required result | Exit gate |
|---:|---|---|---|---|
| 1 | **COMPLETE** | Critical audit of already accepted architecture | One owned audit ledger | Every finding fixed, assigned to steps 2–6, or consciously deferred; no unowned blocker |
| 2 | **IN PROGRESS — FINAL CRITICAL PASS NEXT** | Resources, HP/LifeState, Effects, Conditions, Duration, Recovery, selector/query boundaries | Normative ownership models + aligned schemas/catalogs + focused cases | Health/lifecycle/resources/effects/conditions/time/recovery represent baseline D&D mechanics without duplicate authority; machine contracts and focused cases pass; independent final Step-2 review has no unresolved blocker |
| 3 | `BLOCKED BY 2` | `IntentPlan -> Resolution -> Signal/Event` | Exact compound-turn/execution boundary, operation contracts, event payloads, checkpointable continuation semantics | Multiple intents, partial completion, reactions, suspension/resume, idempotency, atomic mutation segments, and deterministic receipts/tests are defined |
| 4 | `BLOCKED BY 3` | Lore, chapters, knowledge, secrets, minimum promotion interface | Durable truth/disclosure model + context-selection boundary | Public/restricted knowledge has one authority; durable references cannot depend on unpromoted local entities |
| 5 | `BLOCKED BY 4` | Durability, multiplayer, event-local time | Compatible SOFT/HARD publication, shared visibility/conflict/recovery model | Publication/live-scene ownership, cross-scene recovery, chronology, local time, and continuity restoration are coherent |
| 6 | `BLOCKED BY 5` | Modes, LLM execution budget, migration, catalog gaps, full seed, final closure | Mode profiles + final cross-cutting consistency pass | Mode isolation enforceable; migration/gap/seed ownership complete; full audit passes |

## Deferred cross-cutting architecture item — LLM / deterministic-core integration

The project deliberately combines two different execution domains:

- an LLM for natural-language interpretation, lore, narration, ambiguity,
  world/event generation, and other non-formalizable work;
- a deterministic runtime for identity, typed structures, mechanical truth,
  validation, calculation, mutation, persistence, and indexed retrieval.

Their integration must be an explicit typed boundary rather than prompt
convention or an assumption that the LLM keeps every catalog in working memory.

**Revisit trigger:** no later than Step 3, refined in Step 4.

The design must cover referent/entity resolution (`this thing`, `that idiot`),
typed intent/activity binding, catalog lookup/hydration, ambiguity/clarification,
provenance of LLM-adjudicated facts, deterministic validation, compact
receipts/context, unsupported/homebrew mechanics, and the rule that
engine-resolvable mechanical facts remain deterministic-core authority.

Step 2 already establishes one local invariant: an invocation that attempts to
supply engine-owned direct/derived mechanical facts as LLM-adjudicated authority
fails typed validation.

## Deferred cross-cutting architecture item — runtime continuity checkpoints

`runtime-only` / `non-canonical` does not mean `safe to lose`.

HDM must preserve enough continuity-critical runtime state in repository-backed
recovery checkpoints to resume deterministically after process/environment
failure or in another chat/environment without promoting that state to campaign
canon merely because it is recoverable.

Required distinction:

```text
canonical/durable world authority
    -> campaign canon

continuity-critical runtime authority
    -> recovery/checkpoint state, not campaign canon

rebuildable projection/cache
    -> discardable and reconstructable
```

Examples requiring explicit classification include active procedure/encounter
state, procedure-local ResourceState, suspended Continuations/choices/reactions,
mechanically material local metric-coordinate state, and pending typed
obligations whose loss would change future mechanics.

The Temporal Agenda remains a derived/rebuildable due-index. Recovery must
persist the authoritative/checkpoint sources necessary to rebuild it and pending
trigger/boundary work; a serialized index may be cached only as verified,
disposable acceleration data.

**Revisit trigger:** Step 3 defines checkpointable execution/runtime state and
idempotent resume; Step 5 closes repository durability, publication/recovery,
cross-environment restoration, and checkpoint cleanup/expiry. Step 5 cannot
close while this item remains unresolved.

## Step 2 accepted architecture

The detailed normative reasoning remains in the Step-2 specs. Current accepted
results include:

- Actor `hp` is sole HP/temporary-HP authority; `life_state_id` is separate and
  zero HP never hard-codes death;
- persistent Actor/Asset Resources and procedure-local Resources use one
  semantic resolver but different lifetime/storage owners;
- Conditions are named rules identities; concrete applications are ordinary
  one-target Effect instances; Actor Condition lists are derived projections;
- Condition definitions may own intrinsic mechanics directly;
- Condition aggregation (`presence | cumulative_units`) and per-intrinsic-rule
  scope (`aggregate_once | per_effective_application`) are orthogonal stages;
- LifeState baseline is `active | dying | stable | dead`, with state-local
  death-save/stable-recovery progress and prospective transition planning;
- generic Effect stacks are removed; repeated independent applications are
  separate Effect instances; reapplication and arbitration are separate policy
  axes;
- maintained/concentration support is an immutable Effect-parent forest,
  separate from Duration;
- reusable DurationSpec and concrete TemporalBinding are distinct; metric,
  procedure-boundary, and semantic-boundary bases never use wall clock or a
  duplicate writable remaining countdown;
- Duration, Recovery, and procedure refresh share one registered boundary
  vocabulary; state owners own automatic responses;
- Temporal Agenda and reverse indexes are HOT/rebuildable projections, not
  second authorities;
- Calculation Selectors, MechanicalContext accessors/facts, and runtime-only
  domain queries are separate surfaces;
- MechanicalContext is pinned to one committed/prospective state-view identity;
- dependency-cycle freedom uses registered dependency contracts plus a scoped
  concrete DAG validated before prospective activation commits;
- engine-owned mechanical reads use typed registered accessors and cannot be
  forged by LLM invocation context.

## Step 2 artifacts

Primary design chain:

- `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-lifestate-policy-transition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-condition-second-critical-pass.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-schema-catalog-alignment-design.md`

Machine alignment:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/mechanical-surfaces.json`
- corresponding schemas under `DEV/SCHEMAS/`, including typed
  MechanicalContext accessors, DurationSpec/TemporalBinding, Resource/Effect/
  Condition/RestPolicy definition data, Actor/Effect world state;
- `DEV/TESTS/test_step2_machine_contracts.py`;
- `DEV/TESTS/test_step2_mechanical_examples.py`.

## Exact continuation point

**Run the final independent Step-2 critical architecture pass.**

It must attack the *integrated* Step-2 result rather than one local spec and
check at least:

- cross-spec/schema contradictions and duplicate authority;
- HP/LifeState/Condition interactions;
- Effect application/arbitration/support/Condition aggregation interactions;
- Resource lifetime/recovery/temporal interactions;
- duration/boundary/Temporal Agenda recovery correctness;
- selector/accessor/domain-query boundaries and dependency cycles;
- LLM/deterministic authority leakage;
- revision/prospective-state consistency;
- recovery/checkpoint dependencies deliberately deferred to Steps 3/5;
- performance/index implications and YAGNI;
- whether machine alignment accidentally froze a Step-3/5 decision.

If no blocker remains after resolution, Step 2 can close and Step 3 becomes the
single active roadmap stage.
