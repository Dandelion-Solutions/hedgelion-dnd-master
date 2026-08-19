# HDM Catalog Design Status

Status: **STEP 2 COMPLETE / ASSURANCE SLICE E ACTIVE — STEP 3 PAUSED AT SAVED DECISION GATE**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in the linked architecture/spec documents and
Git history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Master assurance plan:

- `DEV/docs/superpowers/specs/2026-08-19-step-1-2-retrospective-architecture-assurance-plan.md`

## 1. Current checkpoint

Steps 1 and 2 remain complete. Step 3 has started but is temporarily paused at
its saved Decision Gate while the non-numbered retrospective assurance overlay
checks Steps 1–2 under the canonical deep-design process.

Assurance status:

```text
0A Catalog meta-model / class boundaries       ASSURED / AMENDED
0B Catalog evolution / identity / strata       ASSURED
A  Actor mechanical state                      ASSURED / AMENDED
B  Effects / Conditions                        ASSURED / AMENDED
C  Temporal / Recovery                         ASSURED / AMENDED
D  Mechanical evaluation / read boundaries     ASSURED / AMENDED
E  Whole Steps 1–2 integration                 ACTIVE
```

Authoritative assurance resolutions include:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-d-mechanical-evaluation-resolution.md`

The original integrated Step-2 critical review remains the pre-assurance closure
record:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-final-critical-review.md`

The assurance amendments refine that baseline without reopening Step 2 as the
numbered active roadmap stage.

## 2. Current Step-2 ownership map

### Actor health and lifecycle

- `world.actor.state.hp` is the sole HP/temporary-HP state authority.
- Resolved maximum HP and Bloodied are derived; no copied writable aliases.
- `life_state_id` is a separate lifecycle authority; zero HP does not hard-code death.
- Initial LifeState vocabulary is `active`, `dying`, `stable`, `dead`.
- Dying owns death-save progress 0..2; the third success/failure is a transition edge.
- Stable owns its concrete recovery `TemporalBinding`.
- Dead does not imply Actor deletion, Effect purge, or a generic resurrection timer.

### Resources

- Persistent Actor/Asset ResourceState owns `current`.
- Procedure-local ResourceState owns `spent`.
- Invalid lifetime/storage combinations are schema-rejected.
- Persistent `current` is normalized against state-stable resolved capacity; a true capacity reduction below current clamps current in the same prospective transition, while capacity growth alone does not restore uses.
- Procedure `spent` survives capacity changes; availability is derived.
- Resource definitions own baseline recovery; Resource state remains the only mutable Resource authority.
- Persistent Resource definitions may have at most one metric delayed-recovery policy in the initial contract; boundary recoveries remain independently allowed.

### Effects and Conditions

- One independent target-local application is one `world.effect` with one `target_id`.
- Generic mutable Effect stacks are removed.
- New application is default; reapplication separates match policy from `refresh|replace` action.
- Effect arbitration chooses applications; Rule Element resolvers combine Contributions.
- Maintained/concentration support is an immutable Effect-parent forest, separate from Duration.
- `definition_id`, reusable `rules_origin_id`, concrete `source_id`, and Step-3 causal execution identity are distinct provenance roles.
- Effect terminal reasons are a closed registered vocabulary.
- A Condition definition is named rules identity; concrete applications use Effect instances.
- No Actor Condition list is canonical.
- Condition aggregation and intrinsic-rule evaluation remain independent axes:

```text
ConditionAggregationPolicy
    presence
    cumulative_units

IntrinsicRuleScope
    aggregate_once
    per_effective_application
```

- `condition.applicability` participates in current effectiveness, not only pre-create validation; later immunity can suppress participation without terminating application lifecycle.
- Conditions may own closed automatic boundary responses over their own applications; RestPolicy does not mutate Conditions.
- Exhaustion uses one effective application unit per level, derived value 0..6, per-unit provenance, threshold-crossing semantics, and Long Rest remove-one behavior.

### Duration, Recovery, and owner-local scheduled triggers

- Reusable `DurationSpec` and concrete active `TemporalBinding` are separate.
- Concrete bases are metric deadline, procedure boundary, or semantic boundary.
- No wall-clock or global campaign clock is introduced.
- Uninferred narrative passage may remain imprecise, but explicitly established quantitative elapsed evidence must not be discarded merely because no timer is armed.
- Boundary producers establish occurrences; state owners own responses.
- `world.effect.temporal_binding` owns intrinsic Effect lifetime only.
- A live Effect may independently own `scheduled_trigger_state[key]` for a declared owner-local metric scheduled trigger under `definition.effect.scheduled_triggers[key]`.
- Terminal Effects cannot retain armed scheduled-trigger state.
- Temporal Agenda indexes intrinsic lifetime, scheduled triggers, Resource recovery, LifeState recovery, and checkpointable runtime obligations, but remains a rebuildable projection rather than scheduler authority.

### Calculation/read/query and invocation-input boundary

Three surfaces remain distinct:

```text
Calculation Selector
MechanicalContext accessor / registered invocation fact
runtime-only Domain Query
```

- Declarative content cannot issue arbitrary world/SQL/JSON queries.
- Engine-owned state uses typed accessors; arbitrary predicate `ref` paths are rejected.
- Context facts are a registered boolean `INVOCATION_ADJUDICATED` input channel, not an open namespace.
- Engine-owned HP/LifeState/Condition/Resource/equipment state cannot be supplied through that channel.
- Explicit true, explicit false, and missing invocation facts are distinct; missing is not false.
- Reviewed state-sensitive Step-2 selectors admit `ENGINE_STATE` only, including `health.maximum`, `resource.capacity`, `resource.recovery`, `condition.applicability`, and currently `effect.duration`.
- Input-class restrictions are transitive through the same scoped dependency DAG.
- Structured `derived_nodes` metadata now records dependency/input contracts.
- `condition_aggregation` depends on current `condition.applicability` plus Effect availability.
- MechanicalContext is pinned to one committed/prospective state-view identity; invocation-sensitive calculations also include the accepted invocation-input fingerprint.
- Runtime multi-result queries have unordered semantic-set behavior unless their typed contract defines rules-significant order.

### LLM authority boundary

The LLM may interpret natural language and adjudicate only explicitly permitted registered fiction-dependent inputs. It cannot assert deterministic engine-owned mechanical facts as trusted authority. Accepted invocation facts remain causal execution input, not automatically canonical lore.

Exact RuntimeCommand fact-value/provenance shape and continuation preservation remain Step-3 work; lore/secret context selection/promotion remains Step 4.

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
- `DEV/SCHEMAS/rule-element.schema.json`

Focused Step-2 tests under `DEV/TESTS/` now cover:

- selector/accessor/input metadata and registry consistency;
- rejection of unregistered invocation facts at compile-contract level;
- state-sensitive selector rejection of invocation-adjudicated inputs;
- structured derived-node metadata/current Condition applicability edge;
- Poisoned/Frightened/Grappled/Exhaustion;
- LifeState state-local progress;
- one-target Effects and closed terminal reasons;
- Condition source/target TriggerBinding and boundary response;
- Effect reapplication match/action separation;
- Resource lifetime/storage/capacity/recovery contracts;
- owner-local scheduled Effect declarations/state, intrinsic-lifetime independence, terminal cancellation, and absence of a global scheduler kind.

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

Retrospective assurance slice artifacts live under `DEV/docs/superpowers/specs/` and supersede conflicting earlier provisional wording where each resolution says so.

## 5. Explicit later-stage dependencies

### Step 3

- exact compound Resolution ordering and atomic ExecutionSegment semantics;
- prospective overlay representation;
- Signal/Event/BoundaryOccurrence and scheduled-trigger due-occurrence identity;
- reactions/choices and suspension/resume;
- scheduled-trigger child Resolution construction and atomic `REARM | UNARM | OWNER TERMINAL` handling;
- provenance-sensitive selection/adjudication;
- dependency-cycle typed failure;
- checkpointable in-flight execution state and deterministic resume;
- explicit invocation-fact boolean values/provenance, binder validation, fingerprinting, and Continuation preservation;
- natural-language referent/intent translation into typed engine requests.

### Step 4

- durable lore/knowledge/secrets/disclosure authority;
- context selection and knowledge-safe exposure of invocation-adjudicated facts;
- promotion of genuinely durable adjudicated truth.

### Step 5

- repository-backed runtime continuity checkpoint publication/restoration;
- SOFT/HARD durability, multiplayer reconciliation, shared revision semantics;
- chronology evidence persistence/compaction and cross-scene time reconciliation;
- checkpoint cleanup/expiry and cross-environment recovery.

### Step 6

- full D&D rules seed/migration/catalog-gap closure;
- complete structured selector/input/dependency metadata coverage;
- extension of scheduled-trigger/fact shapes only for proven seed cases.

## 6. Exact continuation

Proceed with retrospective assurance **Slice E / Whole Steps 1–2 Integration** under the master assurance plan.

After Slice E and the final assurance artifact close, resume Step 3 from its preserved Task Brief/Research Decision Gate rather than restarting execution-boundary analysis.
