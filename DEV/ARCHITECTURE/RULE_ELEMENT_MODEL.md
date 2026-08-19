# HDM Rule Element Model

Status: **DESIGN BASELINE — STEP 2 SELECTOR/CONTEXT ALIGNMENT APPLIED**

This document defines passive mechanical contributions and bounded reactive
bindings. It supersedes the provisional standalone `definition.rule_element`
and `definition.trigger_binding` model.

## 1. Purpose and ownership

A Rule Element answers one question:

> What does this source contribute to this registered calculation when its
> explicit predicate is true?

It is a pure embedded value object. It does not perform an Activity, mutate
world state, spend resources, discover fiction, issue domain queries, or call
arbitrary code.

Rule Elements live inside the reusable definition that grants the mechanic,
normally a Feature, Effect, Condition, Asset, equipment property, or Feat. A
named Condition may own intrinsic Rule Elements directly; it does not require a
mandatory `Condition -> EffectDefinition` indirection. Concrete Condition
applications are ordinary target-local `world.effect` instances whose
`definition_id` references the Condition definition.

The owning definition supplies stable rules identity. Runtime state such as an
active Effect application or equipped Asset supplies concrete provenance and
availability.

An equipped Asset with passive embedded Rule Elements is evaluated directly
from that Asset and its availability predicates. Runtime does not manufacture a
duplicate `world.effect` merely to activate those rules. An Effect application
is materialized when it has an independent target, duration/temporal binding,
validated application parameter, source/provenance relation, maintained support,
or lifecycle that must survive separately from the equipment/definition.

Consequently HDM does not create a standalone catalog definition or canonical
ID for every modifier. If reuse later requires a shared collection, the reusable
unit should normally be a Feature, Effect, Condition, or other existing
rules-bearing definition rather than a new rule-bundle entity.

## 2. Minimum structure

The minimum Rule Element is:

```json
{
  "operation_id": "rule.add_damage_component",
  "selector": "damage.weapon",
  "value": {
    "dice": "1d6",
    "damage_type_id": "damage.radiant"
  }
}
```

Only `operation_id`, `selector`, and `value` are required. Optional fields
include `predicate`, `stacking_key`, `priority`, and a pure Resource gate.

The embedded object has no standalone `id`, mutable source, phase, recovery
policy, or usage counter:

- provenance is derived from the owning definition and concrete runtime owner;
- a registered selector denotes one calculation surface;
- the Resource owns current/spent state, capacity semantics, and recovery;
- Effect application arbitration decides which applications participate;
- selector resolver policy decides how typed Contributions combine.

`stacking_key` is a Rule-Element **contribution-combination** aid where a proven
operation needs it. It is not the removed generic Effect `stacks` authority and
does not control Effect application lifecycle.

## 3. Three separate mechanical surfaces

Step 2 fixes three intentionally different surfaces:

```text
Calculation Selector
    -> what calculation accepts Contributions?

MechanicalContext accessor/fact
    -> what typed value may this calculation read from one pinned state view?

Runtime-only domain query
    -> how does engine infrastructure locate authoritative/indexed objects?
```

A Rule Element can contribute only to a registered Calculation Selector. A
predicate can read only registered facts/accessors allowed by its contract.
Declarative content cannot contain or execute runtime domain-query syntax.

The initial structured selector/accessor metadata is in:

```text
CATALOG/mechanical-surfaces.json
SCHEMAS/mechanical-surfaces.schema.json
SCHEMAS/mechanical-accessor-ref.schema.json
```

Semantic stems may be shared when the typed surface is unambiguous, for example:

```text
selector:health.maximum
accessor:health.maximum
```

Internal dependency identity always retains the surface kind.

## 4. Selectors, operations, and Contributions

`selector` identifies a registered calculation surface such as attack roll,
received damage, Resource capacity/recovery, Effect duration, maximum HP, or
Condition applicability.

`operation_id` identifies the only transformation the element may contribute,
for example a flat modifier, advantage state, extra damage component,
immunity, cost adjustment, duration adjustment, or bounded override.

At catalog compilation, runtime validates that:

1. selector and operation IDs exist;
2. the operation is legal for that selector;
3. `value` matches the selector/operation value contract;
4. predicates use only registered facts/accessors and legal arguments;
5. subject/entity bindings are legal for those accessors;
6. declared dependency classes are legal;
7. the definition is statically acyclic where that can be proven.

When evaluated, a Rule Element returns a typed `value.contribution`. The
selector resolver accepts, combines, suppresses, or rejects Contributions
according to deterministic policy and retains provenance/reason in the
resolution trace.

No general `phase` field is stored. The calculation/operation contract owns
when the selector is resolved. Exact compound-Resolution phase ordering remains
Step 3 rather than becoming a second timing vocabulary on Rule Elements.

## 5. MechanicalContext and predicates

Every predicate/calculation evaluates against one logically immutable
`MechanicalContext` pinned to an explicit committed or prospective state-view
identity. Lazy reads must resolve against that same view or detect invalidation
and rebuild/reject the context. Silent cross-revision reads are forbidden.

Predicates are closed `all` / `any` / `not` trees with typed comparisons. There
are two important input classes:

### Registered context facts

Facts such as fiction-dependent visibility/reachability may be admitted when the
operation contract explicitly marks them as host/LLM-adjudicated.

### Registered MechanicalContext accessors

Engine-owned state is read through exact typed accessor shapes, for example:

```json
{
  "accessor_id": "condition.present",
  "subject": "target",
  "condition_id": "condition.poisoned"
}
```

or:

```json
{
  "accessor_id": "health.bloodied",
  "subject": "target"
}
```

The old arbitrary `{"ref":"some.path"}` operand is not part of the current
schema. Accessors cannot read arbitrary JSON paths, run expressions, enumerate
unrelated Effects, or search the world.

Engine-owned direct/derived facts such as HP, LifeState, effective Conditions,
Resource availability, or Bloodied state cannot be supplied by the LLM as
trusted adjudicated values. Attempts to do so fail typed invocation validation.

## 6. Dependency discipline

Acyclicity is enforced through the accepted hybrid model:

```text
registered dependency contracts
    +
scoped concrete DAG for hydrated/prospective mechanics
```

Dependency analysis includes at least:

- Calculation Selectors;
- MechanicalContext accessors;
- Effect availability/suppression derivation;
- Effect arbitration;
- Condition aggregation;
- Condition intrinsic-rule evaluation.

Independently valid definitions may create a cycle only when combined on one
concrete target/procedure. Therefore prospective activation validates the scoped
DAG before commit. No recursion order, cache order, SQL order, repeated-until-
stable loop, or hidden fixed-point semantics may resolve such a cycle.

## 7. Effect and Condition participation

Effect application participation and Rule Element combination are different
layers:

```text
Effect/Condition application lifecycle
    -> availability
    -> Effect arbitration or Condition aggregation
    -> participating/effective mechanics
    -> Rule Element collection
    -> selector resolution
```

Generic Effect arbitration never substitutes for Condition aggregation.
`cumulative_units` Conditions such as Exhaustion may deliberately retain
multiple effective member applications.

Condition intrinsic mechanics have their own per-item scope:

```text
aggregate_once
per_effective_application
```

The latter receives only the bound context of the current effective Condition
application (source/provenance and declared parameters as permitted), not an
arbitrary query capability.

## 8. Limited use and Resource gates

`gate.resource_ref` may require an available limited-use Resource. The Rule
Element itself remains pure: it exposes the gate as part of eligibility/
Contribution planning.

`resource.capacity` and `resource.available` are derived MechanicalContext
values independent of Activity eligibility. Exact reservation/consumption
commit points, retries, and atomic mutation segments belong to Step 3.

Capacity/recovery are never copied into the Rule Element.

## 9. Trigger Bindings

A Trigger Binding represents a reactive mechanic that cannot be expressed as a
passive Contribution. It is also an embedded value object owned by the Feature,
Effect, Condition, Asset, or other rules-bearing definition.

Minimum shape:

```json
{
  "on": "signal.attack.hit.pending",
  "activity_id": "srd.activity.shield_reaction"
}
```

It contains no callback, child steps, arbitrary payload mutation, executable
query, or embedded Activity definition.

The current structural modes are `automatic`, `offer`, and `schedule`. Their
exact Step-3 execution semantics, idempotency, reaction suspension/resume,
Signal/Event ordering, child Resolution identity, and chain bounds remain owned
by Step 3. Step 2 only requires that Trigger Bindings remain typed and bounded.

## 10. Signals, Events, and boundaries

A Signal is transient calculation/timing context; an Event is a committed fact.
Their exact execution contract is intentionally not finalized in this Step-2
document.

Duration, Recovery, and procedure refresh now share one registered boundary
vocabulary (`boundary.*`). A reached boundary may later be exposed through the
Step-3 Signal/Event contract, but `signal.turn.start`, a BoundaryOccurrence, and
an Event must not silently become three independent authorities for whether the
same mechanical edge occurred.

There is no real-time/background event loop. Metric time advances only through
explicit runtime/procedure advancement, and due work is discovered through the
rebuildable Temporal Agenda.

## 11. Fast evaluation

On hydration/definition load, runtime compiles and indexes embedded Rule Elements
by selector and Trigger Bindings by Signal/Event identity. A Resolution evaluates
only mechanics supplied by the actor, source, targets, their relevant active
Effects/Conditions/Resources, and current procedure state.

Derived indexes/caches are disposable. Cache keys for accessor results include
the pinned state-view identity and bound arguments; a committed-view result may
not leak into a prospective view.

Runtime never scans the whole campaign for an ordinary modifier and never asks
the LLM to recalculate deterministic mechanics from prose.

## 12. Forbidden behavior

Rule Elements and Trigger Bindings cannot:

- mutate state directly;
- invoke Python, SQL, shell, network, GitHub, or arbitrary expressions;
- invent selectors, accessors, facts, operations, Signals, Events, boundaries,
  or Activities;
- execute arbitrary world/domain queries;
- iterate or recurse over world state;
- rewrite committed Events;
- own mutable counters or recovery schedules;
- create a generic Effect stack authority;
- bypass the scoped dependency-DAG check;
- treat LLM-provided engine facts as mechanical authority;
- silently disclose or search narrative secrets.

## 13. Current machine contract and remaining boundary

Machine structure is defined by:

- `SCHEMAS/rule-element.schema.json`;
- `SCHEMAS/trigger-binding.schema.json`;
- `SCHEMAS/mechanical-predicate.schema.json`;
- `SCHEMAS/mechanical-accessor-ref.schema.json`;
- `CATALOG/core-catalog.json`;
- `CATALOG/mechanical-surfaces.json`.

Step-2 focused schema cases are executable in
`DEV/TESTS/test_step2_machine_contracts.py` and
`DEV/TESTS/test_step2_mechanical_examples.py`.

Remaining selector/operation value-contract expansion is seed-driven. Exact
IntentPlan/Resolution ordering and mutation/receipt semantics are Step 3 rather
than unfinished Rule Element design.
