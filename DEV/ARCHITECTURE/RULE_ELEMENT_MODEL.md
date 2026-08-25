# HDM Rule Element Model

Status: **DESIGN BASELINE — STEP 2 ASSURANCE INPUT/DEPENDENCY ALIGNMENT APPLIED**

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

MechanicalContext accessor / registered invocation fact
    -> what typed input may this calculation read?

Runtime-only domain query
    -> how does engine infrastructure locate authoritative/indexed objects?
```

A Rule Element can contribute only to a registered Calculation Selector. A
predicate can read only registered facts/accessors allowed by its contract.
Declarative content cannot contain or execute runtime domain-query syntax.

The complete selector-metadata laws are owned by `CALCULATION_SELECTOR_METADATA.md`.

The structured metadata is in:

```text
CATALOG/mechanical-surfaces.json
SCHEMAS/mechanical-surfaces.schema.json
SCHEMAS/mechanical-accessor-ref.schema.json
```

It includes:

- registered context facts and their input provenance class;
- typed accessor metadata;
- reviewed selector dependency/input capabilities;
- structured derived-stage dependency/input metadata.

Semantic stems may be shared when the typed surface is unambiguous, for example:

```text
selector:health.maximum
accessor:health.maximum
```

Internal dependency identity always retains the surface kind.

## 4. Selectors, operations, Contributions, and allowed inputs

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
7. input provenance classes are legal for the selector/derived consumer;
8. transitive dependencies do not introduce a forbidden input class;
9. the definition is statically acyclic where that can be proven.

The initial input classes are deliberately small:

```text
ENGINE_STATE
    authoritative or derived engine-owned input from the pinned state view

INVOCATION_ADJUDICATED
    explicitly registered non-engine-owned boolean fact accepted for this
    invocation by the host/LLM boundary
```

The current state-sensitive Step-2 selectors (`health.maximum`,
`resource.capacity`, `resource.recovery`, `condition.applicability`, and
`effect.duration`) admit `ENGINE_STATE` only. This prevents an ephemeral LLM
judgment from changing a continuously derived invariant such as Resource
capacity and indirectly normalizing canonical ResourceState.

A future selector may admit `INVOCATION_ADJUDICATED` only through explicit
reviewed metadata. The permission is transitive: a selector that forbids that
input class may not reach it indirectly through an accessor or derived stage.

When evaluated, a Rule Element returns a typed `value.contribution`. The
selector resolver accepts, combines, suppresses, or rejects Contributions
according to deterministic policy and retains provenance/reason in the
resolution trace.

No general `phase` field is stored. The calculation/operation contract owns
when the selector is resolved. Exact compound-Resolution phase ordering remains
Step 3 rather than becoming a second timing vocabulary on Rule Elements.

## 5. MechanicalContext, registered facts, and predicates

Every predicate/calculation evaluates against one logically immutable
`MechanicalContext` pinned to an explicit committed or prospective state-view
identity. Lazy reads must resolve against that same view or detect invalidation
and rebuild/reject the context. Silent cross-revision reads are forbidden.

Predicates are closed `all` / `any` / `not` trees with typed comparisons.
There are two input channels.

### 5.1 Registered invocation-adjudicated context facts

Context facts are not an open string namespace. Every `{ "fact": id }` used by
compiled content must resolve to `CATALOG/mechanical-surfaces.json` metadata.
The initial channel is boolean and `INVOCATION_ADJUDICATED` only.

Examples are genuinely fiction-dependent judgments such as:

```text
fiction.target_visible
fiction.target_reachable
```

They are used only where the engine cannot establish the relevant fiction from
its authoritative state/contracts.

Engine-owned mechanics such as whether an Asset is equipped, current HP,
LifeState, Condition state, Resource state, or mechanically derived ability to
act are **not** context facts. They must use registered accessors/calculations.
The LLM cannot move an engine-owned fact into the invocation channel merely by
choosing a plausible fact name.

Boolean invocation facts have three binding states:

```text
explicitly accepted true
explicitly accepted false
missing / unavailable
```

Missing is not false. A predicate that requires an invocation fact that was not
accepted for the invocation produces a typed missing-input/adjudication result;
`not fact` cannot manufacture evidence from absence.

The exact RuntimeCommand/ActionRequest representation of explicit values and
provenance belongs to Step 3. Step 3 must preserve accepted adjudicated facts as
fixed causal execution inputs when suspension/idempotency/replay requires them.
They do not automatically become canonical lore/world facts.

### 5.2 Registered MechanicalContext accessors

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

### 5.3 MechanicalContext identity and cache identity

For state-only evaluation, context identity includes at least:

```text
pinned state-view identity
bound roles/arguments
```

When a reviewed calculation admits invocation-adjudicated inputs, identity also
includes a fingerprint of the accepted invocation fact values/provenance needed
by that calculation.

Therefore two invocations over the same committed state but different accepted
fiction facts cannot reuse the same invocation-sensitive cached result.

Invocation-input fingerprints are execution identity, not canonical world
state.

## 6. Dependency discipline

Acyclicity is enforced through the accepted hybrid model:

```text
registered static dependency/input contracts
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

`CATALOG/mechanical-surfaces.json` now represents derived stages as structured
`derived_nodes`, not a bare name list. Static metadata declares legal dependency
kinds, legal input classes, and fixed architecture edges where they exist.
Concrete source/target/application bindings add the remaining edges in the
scoped runtime DAG.

Input-class legality is checked transitively through that same graph. HDM does
not build a second graph for provenance/stability validation.

Independently valid definitions may create a cycle only when combined on one
concrete target/procedure. Therefore prospective activation validates the scoped
DAG before commit. No recursion order, cache order, SQL order, repeated-until-
stable loop, or hidden fixed-point semantics may resolve such a cycle.

## 7. Effect and Condition participation

Effect lifecycle, Condition meaning, and Rule Element combination remain
separate layers.

For ordinary Effect payload:

```text
Effect application lifecycle
    -> Effect availability
    -> Effect arbitration where applicable
    -> participating mechanics
    -> Rule Element collection
    -> selector resolution
```

For a named Condition application, Slice-B assurance makes current applicability
an explicit derived input:

```text
nonterminal Condition application
    -> basic Effect availability/suppression
    -> selector:condition.applicability(target, condition)
    -> eligible Condition member set
    -> Condition aggregation
    -> Condition intrinsic mechanics
    -> Rule Element collection
```

`condition.applicability` remains pure. It neither creates/removes applications
nor stores an `applicable` flag. A later immunity can make an existing live
Condition application ineffective; removal of that immunity can make the same
still-live application participate again.

The static `condition_aggregation` dependency contract therefore includes both
`derived:effect_availability` and `selector:condition.applicability`. A concrete
cycle, including a self-referential immunity rule, is rejected by prospective
DAG validation rather than resolved by evaluation order.

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
arbitrary query capability. A relational intrinsic rule may admit a registered
invocation fact such as fiction-dependent visibility when its eventual selector
also allows that input class; state-sensitive selectors do not.

## 8. Limited use and Resource gates

`gate.resource_ref` may require an available limited-use Resource. The Rule
Element itself remains pure: it exposes the gate as part of eligibility/
Contribution planning.

`resource.capacity` and `resource.available` are derived MechanicalContext
values independent of Activity eligibility. Exact reservation/consumption
commit points, retries, and atomic mutation segments belong to Step 3.

Capacity/recovery are never copied into the Rule Element. Because persistent
Resource current state may be normalized after a real capacity decrease,
`resource.capacity` is explicitly restricted to `ENGINE_STATE` dependencies.

## 9. Trigger Bindings and owner-local scheduled triggers

A Trigger Binding represents a reactive mechanic that cannot be expressed as a
passive Contribution. It is an embedded value object owned by the Feature,
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
by Step 3.

Slice-C owner-local `scheduled_triggers` are a separate bounded temporal
mechanism for a live Effect's next-due Activity. They do not gain a privileged
read/query context. When due, Step 3 constructs ordinary bounded Activity/
Resolution execution from the owning Effect bindings. That execution uses the
same fact/accessor/input rules as any other Activity.

If a required invocation-adjudicated fact is unavailable when due, execution
must use a typed suspension/adjudication path rather than fabricate the fact or
silently skip the mandatory mechanic.

## 10. Signals, Events, and boundaries

A Signal is transient calculation/timing context; an Event is a committed fact.
Their exact execution contract is intentionally not finalized in this Step-2
document.

Duration, Recovery, and procedure refresh share one registered boundary
vocabulary (`boundary.*`). A reached boundary may later be exposed through the
Step-3 Signal/Event contract, but `signal.turn.start`, a BoundaryOccurrence, and
an Event must not silently become three independent authorities for whether the
same mechanical edge occurred.

There is no real-time/background event loop. Metric time advances only through
explicit runtime/procedure advancement, and due work is discovered through the
rebuildable Temporal Agenda.

## 11. Runtime domain queries and result ordering

Runtime domain queries are infrastructure capabilities used to locate bounded
state owners/index entries such as relevant target-local Effects, one Resource
binding, support descendants, or due temporal obligations.

They are not serializable catalog mechanics and are never callable from Rule
Elements/predicates as arbitrary query syntax.

Arguments are operation/domain-specific typed keys. Generic predicate trees,
callbacks, SQL fragments, JSON paths, joins, free-form `where`, and user-authored
sort expressions are forbidden.

Unless a specific query contract defines a rules-significant order, a
multi-result query has **unordered set semantics**. Implementations may apply a
stable representational sort for traces/tests, but callers may not treat the
first serialized/SQL/index result as a mechanical winner.

If an operation needs non-commutative selection, it must use the relevant
registered comparator, controller choice, or typed adjudication path.

## 12. Fast evaluation

On hydration/definition load, runtime compiles and indexes embedded Rule Elements
by selector and immediate Trigger Bindings by Signal/Event identity. A Resolution
evaluates only mechanics supplied by the actor, source, targets, their relevant
active Effects/Conditions/Resources, and current procedure state.

Derived indexes/caches are disposable. Cache keys for accessor results include
the pinned state-view identity and bound arguments. Invocation-sensitive results
also include the accepted invocation-input fingerprint. A committed-view result
may not leak into a prospective view, and one invocation's adjudicated fact set
may not leak into another invocation.

Runtime never scans the whole campaign for an ordinary modifier and never asks
the LLM to recalculate deterministic mechanics from prose.

## 13. Forbidden behavior

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
- bypass the scoped dependency-DAG/input-class check;
- treat LLM-provided engine facts as mechanical authority;
- interpret a missing invocation fact as false;
- use query serialization/storage order as gameplay semantics;
- silently disclose or search narrative secrets.

## 14. Current machine contract and later boundary

Machine structure is defined by:

- `SCHEMAS/rule-element.schema.json`;
- `SCHEMAS/trigger-binding.schema.json`;
- `SCHEMAS/mechanical-predicate.schema.json`;
- `SCHEMAS/mechanical-accessor-ref.schema.json`;
- `SCHEMAS/mechanical-surfaces.schema.json`;
- `CATALOG/core-catalog.json`;
- `CATALOG/mechanical-surfaces.json`.

Focused tests include:

- `DEV/TESTS/test_step2_machine_contracts.py`;
- `DEV/TESTS/test_step2_mechanical_examples.py`;
- `DEV/TESTS/test_step2_evaluation_input_contract.py`.

Exact RuntimeCommand fact-value/provenance encoding, deterministic binder
failures, Continuation preservation, prospective overlay identity, and
mutation/receipt semantics are Step 3.

The larger rule-selector inventory is not yet fully described by structured
selector metadata. Expansion is seed-driven and must be closed in Step 6;
unstructured selectors must not be assumed state-safe merely because detailed
metadata is absent.

## S6D-03 selector metadata closure

`CALCULATION_SELECTOR_METADATA.md` owns current selector selectability, selector/operation compatibility, contribution/result typing, subject/binding restrictions and deterministic combination-policy semantics. This document continues to own Rule Elements as pure embedded Contributions. Neither owner grants portable payload-member authority, generic queries, mutation, callbacks or author-controlled execution order.
