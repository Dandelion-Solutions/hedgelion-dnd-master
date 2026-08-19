# HDM Catalog Design Status

Status: **STEP 2 COMPLETE / ASSURANCE SLICE D ACTIVE — STEP 3 PAUSED AT SAVED DECISION GATE**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in the linked architecture/spec documents and
Git history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Prior audit:

- `DEV/ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`

## 1. Current checkpoint

Steps 1 and 2 remain complete. Step 3 has started but is temporarily paused at
its saved Decision Gate while the non-numbered retrospective assurance overlay
checks Steps 1–2 under the canonical deep-design process.

Assurance slices completed so far:

```text
0A Catalog meta-model / class boundaries       ASSURED / AMENDED
0B Catalog evolution / identity / strata       ASSURED
A  Actor mechanical state                      ASSURED / AMENDED
B  Effects / Conditions                        ASSURED / AMENDED
C  Temporal / Recovery                         ASSURED / AMENDED
D  Mechanical evaluation / read boundaries     ACTIVE
E  Whole Steps 1–2 integration                 PENDING D
```

Master assurance plan:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`

Slice-C authoritative resolution:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md`

The original integrated Step-2 critical review remains the pre-assurance closure
record:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

The assurance amendments refine that baseline without reopening Step 2 as the
numbered active roadmap stage.

## 2. Step-2 authoritative ownership map

### Actor health and lifecycle

- `world.actor.state.hp` is the sole HP/temporary-HP state authority.
- Resolved maximum HP and Bloodied are derived; no copied writable aliases.
- `life_state_id` is a separate lifecycle authority; zero HP does not hard-code
  death.
- Initial LifeState vocabulary is `active`, `dying`, `stable`, `dead`.
- Dying owns death-save progress 0..2; the third success/failure is a transition
  edge, not stored progress.
- Stable owns its concrete recovery `TemporalBinding`.
- Dead does not imply Actor deletion, Effect purge, or a generic resurrection
  timer.

### Resources

- Persistent Actor/Asset ResourceState owns `current`.
- Procedure-local ResourceState owns `spent`.
- Invalid lifetime/storage combinations are schema-rejected.
- Persistent `current` state is normalized against state-stable resolved
  capacity; a true capacity reduction below current clamps current in the same
  prospective transition, while capacity growth alone does not restore uses.
- Procedure `spent` survives capacity changes; availability is derived.
- `resource.capacity` and `resource.available` are storage-independent derived
  semantics.
- Resource definitions own baseline recovery; Resource state remains the only
  mutable Resource authority.
- A persistent Resource definition may have at most one metric delayed-recovery
  policy in the initial contract; boundary recoveries remain independently
  allowed through the registered boundary vocabulary.

### Effects

- One independent target-local application is one `world.effect` with one
  `target_id`.
- Generic mutable Effect stacks are removed.
- New application is the default; reapplication explicitly separates match
  policy from `refresh|replace` action.
- Effect arbitration chooses participating applications; Rule Element resolvers
  combine typed Contributions.
- Maintained/concentration support is an immutable Effect-parent forest,
  separate from Duration.
- `definition_id`, reusable `rules_origin_id`, concrete `source_id`, and Step-3
  causal execution identity are distinct provenance roles.
- Effect terminal reasons are a closed registered vocabulary.
- Arbitration winners, reverse support children, and similar indexes remain
  derived HOT state.

### Conditions

- A Condition definition is a named rules identity; concrete applications are
  ordinary Effect instances.
- No Actor Condition list is canonical.
- Condition aggregation and intrinsic-rule evaluation are orthogonal:

```text
ConditionAggregationPolicy
    presence
    cumulative_units

IntrinsicRuleScope
    aggregate_once
    per_effective_application
```

- Condition definitions may own intrinsic Rule Elements/Trigger Bindings
  directly.
- Per-effective-application mechanics may bind closed `condition.source` /
  `condition.target` roles.
- `condition.applicability` participates in current application effectiveness,
  not only pre-create validation; later immunity can suppress participation
  without terminating application lifecycle.
- Conditions may own closed automatic boundary responses over their own
  applications; RestPolicy does not mutate Conditions.
- Exhaustion uses one effective application unit per level, derived value 0..6,
  per-unit provenance, aggregate threshold crossing, and Long Rest remove-one
  semantics.

### Duration, boundaries, recovery, and scheduled triggers

- Reusable `DurationSpec` and concrete active `TemporalBinding` are separate.
- Concrete bases are metric deadline, procedure boundary, or semantic boundary.
- No wall-clock or global campaign clock is introduced.
- Uninferred narrative passage may remain imprecise, but explicitly established
  quantitative elapsed evidence must not be discarded merely because no timer
  is currently armed.
- Duration, Recovery, and procedure refresh share one registered boundary
  vocabulary.
- A boundary producer establishes occurrence; each state owner owns its response.
- Resource boundary recovery, Condition boundary response, Effect expiry, and
  HP/LifeState ruleset response are separate state-owner responsibilities.
- Resource delayed recovery uses metric delay only; boundary recovery has one
  direct `boundary_id` encoding.
- `world.effect.temporal_binding` owns intrinsic Effect lifetime only.
- A live Effect may independently own `scheduled_trigger_state[key]` for a
  declared owner-local metric scheduled trigger. Its reusable declaration lives
  under `definition.effect.scheduled_triggers[key]` and names a bounded Activity.
- Terminal Effects cannot retain armed scheduled-trigger state.
- Temporal Agenda indexes intrinsic lifetime, scheduled triggers, Resource
  recovery, LifeState recovery, and checkpointable runtime obligations but
  remains rebuildable due-index state rather than scheduler authority.

### Calculation/read/query boundary

Three surfaces are intentionally separate:

```text
Calculation Selectors
MechanicalContext accessors/facts
runtime-only Domain Query APIs
```

- Declarative content cannot issue arbitrary world/SQL/JSON queries.
- Engine-owned mechanical state uses typed registered accessors; arbitrary
  predicate `ref` paths are rejected.
- `condition.applicability` is currently narrowed to the proven immunity case.
- MechanicalContext is pinned to one committed/prospective state-view identity.
- Dependency-cycle freedom uses registered dependency contracts plus a scoped
  concrete DAG validated before prospective activation commits.
- The DAG includes selectors/accessors, Effect availability/arbitration,
  Condition aggregation, and Condition intrinsic evaluation.

Slice D is now independently re-testing these boundaries, including the
carry-forward requirement that state-normalizing calculations such as
`resource.capacity` cannot depend on invocation-only LLM-adjudicated facts.

### LLM authority boundary

The LLM may interpret natural language and adjudicate only explicitly permitted
fiction-dependent facts. It cannot assert deterministic engine-owned HP,
LifeState, Condition, Resource, Effect, or other registered mechanical facts as
trusted authority; such invocation input fails typed validation.

The complete LLM/deterministic-core integration remains a mandatory Step-3/4
cross-cutting design.

## 3. Current machine contract

Primary catalogs:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/mechanical-surfaces.json`

Primary Step-2 schemas include:

- `DEV/SCHEMAS/world-actor-state.schema.json`
- `DEV/SCHEMAS/world-effect-state.schema.json`
- `DEV/SCHEMAS/resource-definition-data.schema.json`
- `DEV/SCHEMAS/effect-definition-data.schema.json`
- `DEV/SCHEMAS/condition-definition-data.schema.json`
- `DEV/SCHEMAS/rest-policy-definition-data.schema.json`
- `DEV/SCHEMAS/duration-spec.schema.json`
- `DEV/SCHEMAS/temporal-binding.schema.json`
- `DEV/SCHEMAS/mechanical-accessor-ref.schema.json`
- `DEV/SCHEMAS/mechanical-surfaces.schema.json`
- `DEV/SCHEMAS/mechanical-predicate.schema.json`

Focused Step-2 tests under `DEV/TESTS/` cover:

- removed provisional authorities;
- selector/accessor registry consistency;
- Poisoned/Frightened/Grappled/Exhaustion;
- LifeState state-local progress;
- one-target Effects;
- Condition source/target TriggerBinding;
- Condition boundary response;
- Condition applicability narrowing;
- Effect reapplication match/action separation;
- Effect terminal-reason closure;
- Resource lifetime/storage, capacity normalization contract, and recovery
  timing/operation contracts;
- owner-local scheduled Effect declarations/state, intrinsic-lifetime
  independence, terminal cancellation, and absence of a global scheduler kind.

## 4. Primary Step-2 design and assurance chain

Original Step-2 chain:

- `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-lifestate-policy-transition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-schema-catalog-alignment-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

Retrospective assurance amendments are recorded in the slice artifacts under
`DEV/docs/superpowers/specs/`, with Slice C currently resolving the approved
owner-local scheduled-trigger addition.

## 5. Explicit later-stage dependencies

### Step 3

- exact compound Resolution ordering and atomic mutation segments;
- prospective overlay representation;
- Signal/Event/BoundaryOccurrence and scheduled-trigger due-occurrence identity;
- reactions/choices and suspension/resume;
- scheduled-trigger child Resolution construction, idempotency and atomic
  `REARM | UNARM | OWNER TERMINAL` handling;
- provenance-sensitive remove-one selection/adjudication;
- typed dependency-cycle failure during prospective activation;
- checkpointable in-flight execution state and deterministic resume;
- LLM natural-language referent/intent translation into typed engine requests.

### Step 4

- durable lore/knowledge/secrets/disclosure authority;
- LLM context selection and refinement of fiction-only adjudicated facts.

### Step 5

- repository-backed runtime continuity checkpoint publication/restoration;
- SOFT/HARD durability, multiplayer reconciliation, shared revision semantics;
- chronology evidence persistence/compaction and cross-scene time reconciliation;
- checkpoint cleanup/expiry and cross-environment recovery.

### Step 6

- full D&D rules seed/migration/catalog-gap closure;
- exhaustive verification of concrete ruleset response tables;
- extension of scheduled-trigger declaration shapes only for proven seed cases
  not representable by the initial metric-delay + bounded-Activity contract.

## 6. Exact continuation

Proceed with retrospective assurance **Slice D / Mechanical evaluation and read
boundaries** under the master assurance plan.

After Slice D and whole-system Slice E close, resume Step 3 from its preserved
Task Brief/Research Decision Gate rather than restarting execution-boundary
analysis.
