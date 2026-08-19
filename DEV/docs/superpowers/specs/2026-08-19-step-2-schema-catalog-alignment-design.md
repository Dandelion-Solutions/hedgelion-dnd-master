# Step 2 Schema and Catalog Alignment Design

Status: **MECHANICAL ALIGNMENT SPEC — DERIVED FROM APPROVED STEP-2 DECISIONS**

Target branch: `feature/mechanical-runtime-hot-state`

Primary decision bases:

- `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-lifestate-policy-transition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md`

This document translates already accepted architecture into machine catalog/schema consequences. It does not introduce new product semantics. Exact Step-3 execution ordering, event/receipt identity, prospective-overlay representation, and multiplayer publication behavior remain owned by later roadmap stages.

## 1. Alignment goals

The aligned development artifacts must make these Step-2 invariants mechanically visible:

1. HP/temporary HP are Actor health state, not generic Resources;
2. LifeState has one current Actor authority plus state-local progress;
3. Condition applications are ordinary one-target Effect instances;
4. Condition definitions directly own their intrinsic mechanics; mandatory `Condition -> EffectDefinition` indirection is removed;
5. generic mutable Effect stacks are removed;
6. Effect reapplication, arbitration, Condition aggregation, and intrinsic-rule scope are separate concepts;
7. Concentration is maintained Effect support, not a duration mode;
8. Duration/recovery use one registered boundary vocabulary;
9. concrete temporal bindings use typed metric/procedure/semantic bases without wall-clock time or duplicate writable countdowns;
10. selector calculations, MechanicalContext accessors, and runtime domain queries remain separate surfaces;
11. engine-owned mechanical values are accessed through typed registered accessors rather than arbitrary `fact/ref` paths;
12. Condition aggregation uses `presence | cumulative_units` and intrinsic mechanics use `aggregate_once | per_effective_application` independently;
13. no machine artifact may retain an old field/ID as an apparently valid alternative authority merely for backward convenience.

## 2. Catalog vocabulary changes

### 2.1 Resource vocabulary

Remove health-specific generic Resource mechanics:

```text
resource.health
resource.temporary_health
```

HP and temporary HP remain in `world.actor.state.hp`.

Persistent ResourceState may store `current`; procedure-local ResourceState may store `spent`. The reusable Resource definition selects its lifetime/storage contract; Activities continue to use one storage-independent Resource resolver.

### 2.2 Rule selectors

Remove:

```text
effect.stacks
```

Add:

```text
health.maximum
condition.applicability
```

`health.maximum` is a contribution calculation. `condition.applicability` is a pure allow/block/typed applicability calculation and does not create a Condition application.

### 2.3 MechanicalContext accessors

Introduce the initial registered accessor surface:

```text
health.current
health.temporary
health.maximum
health.bloodied
life.state
condition.present
condition.value
resource.capacity
resource.available
owner_effect.parameter
```

These IDs are not calculation selectors even when a semantic stem is shared, for example:

```text
selector:health.maximum
accessor:health.maximum
```

Internal dependency identity always includes surface kind.

### 2.4 LifeState vocabulary

Register exactly:

```text
life.active
life.dying
life.stable
life.dead
```

Register the initial policies:

```text
life_policy.dnd2024.character_like
life_policy.dnd2024.monster_default
```

The Actor may carry an explicit policy override; otherwise the resolver inherits from archetype/definition and finally the selected ruleset default.

### 2.5 Condition policy vocabulary

Register:

```text
condition_aggregation.presence
condition_aggregation.cumulative_units
```

and independently:

```text
condition_rule_scope.aggregate_once
condition_rule_scope.per_effective_application
```

No combined aggregation/scope enum and no generic reducer language are introduced.

### 2.6 Effect lifecycle policy vocabulary

Replace generic stacking behavior with separated policy registries.

Initial reapplication actions:

```text
effect_reapplication.refresh
effect_reapplication.replace
```

Absence means the accepted default: create a new application.

Initial arbitration capability may register only proven whole-application policies. The machine contract must not restore `stack.stack`, `unique_global`, `keep_highest`, etc. as one mixed vocabulary.

### 2.7 Temporal/boundary vocabulary

Remove Concentration from duration modes.

Replace the separate `recovery_triggers` authority with one `boundary_kinds` registry used by Duration, Recovery, and procedure refresh. Initial required boundaries include:

```text
boundary.turn_start
boundary.turn_end
boundary.round_start
boundary.round_end
boundary.short_rest_complete
boundary.long_rest_complete
boundary.dawn
```

The runtime may expose a reached boundary into Step-3 Signal/Event machinery, but the semantic occurrence has one boundary identity.

Concrete temporal bindings distinguish:

```text
temporal.metric_deadline
temporal.procedure_boundary
temporal.semantic_boundary
```

Concentration/maintenance support is represented by `support_effect_id`, not by a temporal mode.

## 3. New kind-specific schemas

The generic envelopes remain intentionally small. Step-2 semantics move into kind-specific schemas selected by `kind`.

Create at least:

```text
SCHEMAS/resource-definition-data.schema.json
SCHEMAS/effect-definition-data.schema.json
SCHEMAS/condition-definition-data.schema.json
SCHEMAS/rest-policy-definition-data.schema.json
SCHEMAS/world-effect-state.schema.json
SCHEMAS/duration-spec.schema.json
SCHEMAS/temporal-binding.schema.json
SCHEMAS/mechanical-accessor-ref.schema.json
SCHEMAS/mechanical-surfaces.schema.json
```

and the corresponding machine metadata file:

```text
CATALOG/mechanical-surfaces.json
```

Existing Actor schemas are updated rather than duplicated.

## 4. Actor schema alignment

`world-actor-state.schema.json` retains:

```text
hp.current
hp.maximum_base
hp.maximum_adjustment
hp.temporary
life_state_id
resources
```

and adds:

```text
life_state_policy_id      // optional explicit override
life_state_progress       // conditional state-local authority
```

Consistency is schema-enforced:

```text
life.active -> progress absent
life.dying  -> death_saves successes/failures 0..2
life.stable -> stable recovery TemporalBinding when progress is materialized
life.dead   -> progress absent
```

`hp` still depends on `life_state_id` being materialized in the same Actor state.

Actor archetypes may declare `life_state_policy_id`. Ordinary Actors need no copied override when inherited/default policy is sufficient.

Persistent Actor Resources continue to use their persistent ResourceState shape. Procedure-local `spent` state is not added to Actor state.

## 5. Resource definition schema

The initial Resource definition must be able to state:

```text
mechanic_id
lifetime_owner
state_model
capacity baseline when definition-owned
automatic recovery specifications
```

Closed initial lifetime owners:

```text
actor
asset
procedure
```

Closed state models:

```text
current
spent
```

The definition owns baseline recovery semantics. A recovery entry binds one registered boundary/deadline to one closed Resource-domain response family, such as:

```text
reset_spent
restore_to_capacity
restore_amount
```

Choice, rolls, optional activation, spending another Resource, or arbitrary Activity execution do not belong in automatic Resource recovery.

The schema does not copy resolved capacity/current availability into the definition or into parallel runtime fields.

## 6. DurationSpec and TemporalBinding

`DurationSpec` is reusable definition semantics, not active instance state.

The minimum shape distinguishes:

```text
instant
metric amount + exact unit
registered future boundary
permanent
```

Turn/round/rest/dawn semantics use registered boundaries rather than synthetic seconds.

`TemporalBinding` is concrete active state and uses exactly one basis:

### metric deadline

Stores an exact local temporal context/anchor/deadline representation sufficient to derive remaining duration without a writable `remaining` counter.

### procedure boundary

Stores the registered boundary plus the specific procedure/subject scope needed to identify the future qualifying edge. Exact Step-3 occurrence sequencing remains deferred.

### semantic boundary

Stores the registered semantic boundary plus qualifying scope/subject binding. No fabricated wall-clock deadline is required.

A binding never stores multiple independent bases for one intrinsic lifetime.

## 7. Effect definition schema

A reusable Effect definition may contain:

```text
duration
application parameter declarations
rule_elements
trigger_bindings
activity_ids
reapplication_policy_id
arbitration_policy_id
```

Reapplication and arbitration are optional and independent.

No `stacking` field and no generic stack counter are accepted.

Application parameter declarations are closed typed declarations used to validate concrete `world.effect.state.parameters`; arbitrary untyped executable JSON is not introduced.

## 8. Condition definition schema

A Condition uses the same ordinary mechanical payload concepts but owns named-Condition semantics directly.

It requires:

```text
aggregation_policy_id
```

and may contain intrinsic mechanical items. Each intrinsic item is wrapped with one scope:

```text
aggregate_once
per_effective_application
```

Conceptually:

```json
{
  "aggregation_policy_id": "condition_aggregation.presence",
  "intrinsic_mechanics": [
    {
      "scope_id": "condition_rule_scope.aggregate_once",
      "rule_element": { ... }
    }
  ]
}
```

The initial machine shape supports Rule Elements and Trigger Bindings as intrinsic typed items without introducing an arbitrary script body.

`condition.present/value` remain derived from the Condition aggregator.

No mandatory `effect_ids` indirection remains.

## 9. `world.effect` schema

One application has exactly one target:

```text
target_id
```

not `target_ids[]`.

The state may additionally own:

```text
source_id
rules_origin_id
parameters
support_effect_id
temporal_binding
lifecycle
```

The lifecycle shape distinguishes nonterminal/terminal state and terminal reason without using arbitration/suppression as lifecycle aliases.

Not stored:

```text
stacks
winner/shadowed flag
condition present/value
derived application family
reverse support children
remaining duration countdown
```

`definition_id` remains required in the world-record envelope and may reference either a reusable Effect or Condition definition according to loader validation.

## 10. Predicate/accessor schema

The existing generic `{"ref":"some.path"}` operand is too permissive for engine-owned state.

Mechanical predicates retain closed boolean/comparison composition, but engine-owned reads use typed registered accessor references.

Example:

```json
{
  "compare": {
    "left": {
      "accessor_id": "condition.present",
      "subject": "target",
      "condition_id": "condition.poisoned"
    },
    "operator": "eq",
    "right": true
  }
}
```

Accessor schema variants have exact argument sets. Unknown arguments fail schema validation.

The remaining `fact` shorthand is reserved for registered context facts whose source contract permits them, particularly adjudicated/non-engine facts. It is not a way for the LLM to assert values from the engine-owned accessor families.

## 11. Mechanical surface metadata

`CATALOG/mechanical-surfaces.json` provides structured metadata for Step-2 reviewed selectors/accessors without replacing the core ID registry.

The core catalog remains identity authority for registered IDs. The structured surface catalog is metadata authority for typed contract details and is cross-validated against those identities.

Accessor metadata includes at least:

```text
source_class
value_type
subject kinds / argument contract
derived-stage dependency metadata where applicable
```

Selector metadata includes at least:

```text
allowed operation IDs
value/contribution family
allowed accessor/dependency classes
```

The dependency model also recognizes registered derived stages for:

```text
effect availability
Effect arbitration
Condition aggregation
Condition intrinsic-rule evaluation
```

Concrete scoped DAG validation remains runtime behavior; the machine catalog records only the closed static capability/dependency contract.

## 12. RestPolicy alignment

`definition.rest_policy` stops owning `recovery_steps`.

It owns the procedure facts needed to establish a successful rest and emit one completion boundary, including:

```text
duration
completion_boundary_id
interruption policy / requirements as defined
```

HP/Resource/Condition/Effect responders remain owned by their respective state domains.

A read-only Boundary Impact View may later show all responders to a boundary; it is never written back into RestPolicy.

## 13. Machine inventory corrections

`CATALOG/entity-structures.json` and `ARCHITECTURE/ENTITY_STRUCTURES.md` must be corrected together.

Required changes include:

```text
definition.rest_policy:
    remove recovery_steps authority

definition.effect:
    remove stacking
    add duration / parameters / reapplication / arbitration payload fields

definition.condition:
    remove required effect_ids
    add aggregation_policy_id / intrinsic_mechanics / removal semantics as applicable

world.effect:
    target_ids -> target_id
    status -> lifecycle
    remove stacks
    add parameters / support_effect_id / temporal_binding / provenance fields
```

Actor reverse-effect projections use `world.effect.target_id`, not `target_ids`.

## 14. Naming policy during alignment

Provisional machine names may be normalized without another human gate when semantics remain unchanged.

In particular:

- prefer `health.maximum` consistently for the Step-2 selector/accessor semantic stem;
- use typed surface kind internally where selector/accessor names share a stem;
- use `condition.applicability`, not the mutation-sounding `condition.application`;
- use `per_effective_application`, not ambiguous `per_application`;
- remove obsolete synonyms rather than retain aliases in the authoritative catalog.

Compatibility aliases are not justified because these machine names have not been published as a stable external contract.

## 15. Explicit deferrals to Step 3 / Step 5

Alignment must not freeze these later-stage decisions:

```text
exact IntentPlan/Resolution mutation segment ordering
prospective overlay representation
exact BoundaryOccurrence/Event/Signal payload and receipt IDs
reaction/choice suspension semantics
causal event sequencing and idempotency representation
cross-scene/multiplayer revision reconciliation
repository continuity-checkpoint publication/cleanup format
```

Step-2 schemas may reference opaque registered identities supplied by those later contracts, but may not invent a competing execution subsystem.

## 16. Verification gates

Before claiming schema/catalog alignment complete:

1. every JSON file parses;
2. every JSON Schema passes Draft 2020-12 schema checks;
3. all schema examples validate;
4. machine catalog instances validate;
5. core registry IDs and structured metadata keys cross-check;
6. stale Step-2 authorities are absent from current normative artifacts;
7. maintenance audit passes after being updated for newly authoritative machine files;
8. focused Step-2 cases validate Poisoned/Frightened/Grappled/Exhaustion, HP/LifeState, maintained Effects, Duration/Recovery, Resource ownership, and selector/accessor boundaries.

Only after these gates does Step 2 enter its final independent critical pass.
