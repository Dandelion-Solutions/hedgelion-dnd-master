# HDM Catalog Design Status

Status: **STEP 2 COMPLETE — STEP 3 IS THE NEXT ACTIVE ARCHITECTURE STAGE**

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

Step 1 critical architecture audit is complete.

Step 2 mechanical-state architecture is complete after:

- ownership design;
- detailed Recovery, Effect-application, and LifeState design;
- selector/query boundary design and adversarial resolution;
- cumulative/valued Condition design;
- Condition aggregation/intrinsic-rule-scope resolution;
- schema/catalog alignment;
- focused executable cases;
- final integrated critical review;
- successful repository maintenance/schema/unit-test validation.

Final Step-2 verdict:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

Step 3 (`IntentPlan -> Resolution -> Signal/Event`) is the next active
architecture stage.

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
- `resource.capacity` and `resource.available` are storage-independent derived
  semantics.
- Resource definitions own baseline recovery; Resource state remains the only
  mutable Resource authority.

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
- Conditions may own closed automatic boundary responses over their own
  applications; RestPolicy does not mutate Conditions.
- Exhaustion uses one effective application unit per level, derived value 0..6,
  per-unit provenance, aggregate threshold crossing, and Long Rest remove-one
  semantics.

### Duration, boundaries, and recovery

- Reusable `DurationSpec` and concrete active `TemporalBinding` are separate.
- Concrete bases are metric deadline, procedure boundary, or semantic boundary.
- Metric time is local/monotonic/demand-driven, never wall clock.
- Duration, Recovery, and procedure refresh share one registered boundary
  vocabulary.
- A boundary producer establishes occurrence; each state owner owns its response.
- Resource boundary recovery, Condition boundary response, Effect expiry, and
  HP/LifeState ruleset response are separate state-owner responsibilities.
- Resource delayed recovery uses metric delay only; boundary recovery has one
  direct `boundary_id` encoding.
- Temporal Agenda is a rebuildable due-index, not a scheduler authority.

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
- Resource lifetime/storage and recovery timing/operation contracts.

## 4. Primary Step-2 design chain

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
- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

## 5. Explicit later-stage dependencies

### Step 3

- exact compound Resolution ordering and atomic mutation segments;
- prospective overlay representation;
- Signal/Event/BoundaryOccurrence identity and idempotency;
- reactions/choices and suspension/resume;
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
- checkpoint cleanup/expiry and cross-environment recovery.

### Step 6

- full D&D rules seed/migration/catalog-gap closure;
- exhaustive verification of concrete ruleset response tables such as Long Rest
  HP restoration without moving that authority into RestPolicy.

## 6. Next architecture task

Proceed with Step 3 under `DEV/DESIGN_PROCESS.md`:

```text
IntentPlan -> Resolution -> Signal/Event
```

The initial Step-3 Task Brief must incorporate the already-owned cross-cutting
requirements for LLM/deterministic-core integration and runtime continuity,
because execution/idempotency/receipts are the boundary where both become
architecturally material.
