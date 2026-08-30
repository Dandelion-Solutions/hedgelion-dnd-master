# Step 2 Valued/Cumulative Condition Review Resolution

Status: **PRELIMINARILY ACCEPTED — REVIEW FINDINGS RESOLVED**

Target branch: `feature/mechanical-runtime-hot-state`

Candidate design:

- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-design.md`

Adversarial review:

- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-adversarial-review.md`

This document resolves the independent review findings. Where it conflicts with the candidate design, this resolution is authoritative for the remainder of Step 2.

The human architect approved the core direction: D&D Exhaustion uses `cumulative_units`, with one authoritative unit represented by one ordinary target-local Condition/Effect application and the effective level derived from those units.

No runtime implementation or final schema/catalog migration is authorized by this checkpoint.

## 1. Final core model

The initial Condition aggregation family remains deliberately small:

```text
presence
cumulative_units
```

`presence` represents ordinary non-strengthening named Conditions.

`cumulative_units` represents a Condition whose effective value is the bounded count of mechanically effective independent unit applications.

For D&D Exhaustion:

```text
one effective Exhaustion unit application = one Exhaustion level
condition.value(actor, exhaustion) = effective unit count
```

No Actor `exhaustion_level`, generic Effect `stacks`, Condition counter entity, or Resource authority is introduced.

## 2. Condition aggregation is an explicit participation layer

The review blocker concerning generic Effect arbitration is accepted.

Named Condition semantics resolve through this conceptual path:

```text
Condition-bearing applications
    -> lifecycle/basic availability
    -> Condition aggregation policy
    -> effective Condition representation
    -> Condition intrinsic mechanics
```

Generic Effect arbitration must not collapse `cumulative_units` into one winner merely because applications share one Condition identity/family.

For `cumulative_units`, every otherwise eligible unit application participates in the aggregate.

For `presence`, several source applications may exist while the named Condition itself still resolves to one effective presence state.

This refines, rather than replaces, the accepted Effect-application architecture.

## 3. Intrinsic Condition mechanics versus source/application mechanics

The review blocker concerning duplicated Condition payload is accepted.

There are two conceptual mechanical scopes.

### 3.1 Condition-intrinsic mechanics

These belong to the named Condition definition and are emitted from the effective Condition aggregation result.

Examples:

```text
Poisoned intrinsic mechanics
    -> emitted once while effective presence is true

Exhaustion intrinsic mechanics
    -> emitted according to cumulative_units effective value
```

For the initial Exhaustion seed, the cumulative policy may emit fixed per-unit contributions equivalent to:

```text
-2 to D20 Tests per effective unit
-5 feet Speed per effective unit
```

This does not require a generic expression engine.

### 3.2 Application/source-specific mechanics

A particular Effect application may carry additional mechanics owned by its source/rules origin. Those mechanics remain ordinary Effect payload and continue through normal application participation/arbitration rules.

They are not collapsed merely because the named Condition aggregates to one presence/value.

This separation prevents multiple Poisoned applications from duplicating intrinsic Poisoned mechanics while still allowing one source-specific Poisoned application to impose additional rules beyond the base Condition.

Exact schema field layout is deferred to alignment.

## 4. Effective representation

The Condition aggregator produces an immutable effective representation within the pinned MechanicalContext/state view.

Conceptually:

```text
EffectiveCondition
    condition identity
    present
    typed effective value when policy defines one
    effective unit/application set as runtime-internal provenance
```

This is not a new canonical world record.

It is a derived runtime/context value and may be HOT-cached by state-view identity.

`condition.present` and `condition.value` read this representation.

Application IDs/provenance remain domain-query/internal data unless a concrete operation has permission to address them.

## 5. Value typing

`condition.value` remains policy-owned and typed.

For `cumulative_units`:

```text
value type = bounded integer count
```

This does not redefine every future valued Condition as numeric.

A future proven aggregation policy may expose another scalar/enum type, but no universal arithmetic Condition algebra or arbitrary reducer is authorized.

## 6. Exhaustion range invariant

For the selected D&D 2024 Exhaustion policy:

```text
0 <= committed effective Exhaustion value <= 6
```

`6` is the maximum meaningful rules level and carries the lethal threshold consequence.

A prospective operation that would create enough effective units to reach or pass the threshold must validate/normalize the full Resolution plan before commit. It must not accidentally leave a stable committed `7`, `8`, or larger Exhaustion state merely because additional rows could be inserted.

Exact handling of excess same-segment gain after death belongs to Step 3 ordering/normalization, but an out-of-range committed value is invalid.

## 7. Thresholds are crossing semantics

The review blocker concerning repeated lethal consequence is accepted.

A threshold consequence is triggered by a state-view transition, not by continuously evaluating a steady predicate.

For Exhaustion:

```text
before effective value < 6
AND
after prospective effective value >= 6
    -> one lethal threshold-crossing consequence
```

The consequence is part of the same prospective Resolution identity and follows Step-3 idempotency/event rules.

Recomputing a state that is already at 6 does not repeatedly produce death.

Reducing/suppressing units later does not undo an already committed LifeState transition. Exhaustion removal is not resurrection.

If an Actor is explicitly revived by the proper lifecycle mechanic, later exists below the threshold, and then crosses the threshold again, that later crossing is a new legitimate event.

## 8. LifeState boundary

The Exhaustion Condition does not directly write `life_state_id`.

Threshold crossing produces a typed prospective consequence consumed by the ordinary Resolution/LifeState authority.

Therefore:

```text
Condition aggregation
    detects crossing

Resolution
    plans consequence

LifeStateResolver
    owns lifecycle transition plan
```

LifeStatePolicy does not hard-code the concrete Exhaustion Condition ID.

## 9. Removal capability

Cumulative-unit removal operates over concrete eligible unit applications.

The initial semantic families are conceptually:

```text
remove_count(condition, count, typed removal policy/context)
remove_origin_units(condition, typed origin/family identity)
```

Exact names belong to schema/Step-3 operation design.

Neither operation mutates a shared integer total.

No arbitrary filter tree, callback, SQL predicate, JSON path, or free-form source string is allowed.

## 10. Typed provenance/removal identity

A cumulative unit must preserve enough typed identity for rules that refer to how that unit was gained.

The existing generic `source_id` alone is not assumed sufficient.

Schema/Step-3 provenance work must provide a closed typed way to identify mechanically relevant origin, such as validated rules origin, application family, causal mechanic identity, or another registered provenance key.

The representation must support seed semantics such as:

```text
Exhaustion units gained from suffocation
Exhaustion units whose removal is blocked by dehydration
Exhaustion units whose removal is blocked by malnutrition
```

Narrative labels are not mechanical selectors.

## 11. Generic remove-one resolution

A request such as Long Rest or Greater Restoration may remove one Exhaustion level.

Runtime first filters to units eligible for that removal mechanic.

Then:

```text
if exactly one eligible unit
    -> remove it

if several eligible units are mechanically equivalent
    -> use a registered deterministic representational tie rule

if several eligible units are mechanically non-equivalent and rules determine selection
    -> apply the registered typed selector

if several eligible units are mechanically non-equivalent and rules do not determine selection
    -> typed Step-3 adjudication/choice requirement
```

SQL/list/application-ID order is never the rule.

Storage identity alone must not manufacture a fake player choice when alternatives are mechanically equivalent.

## 12. Recovery B2 relationship

Long Rest produces `boundary.long_rest_complete` exactly once under the accepted Recovery B2 ownership model.

The Exhaustion Condition owner may respond with a request to remove one eligible unit.

The response is fully automatic only when the exact transition is deterministically derivable.

If a real provenance combination makes one-unit removal mechanically underdetermined, the boundary remains valid but the Condition consequence moves through the ordinary Step-3 Resolution/adjudication path. RestPolicy still does not own Condition mutation.

## 13. Source-scoped removal

Suffocation proves source-scoped removal as a distinct operation from generic decrement.

When a rule removes all Exhaustion units produced by one typed origin/family, runtime addresses those concrete applications through the closed provenance query/removal contract and terminates the selected set atomically where required.

The effective Exhaustion value is then re-derived.

This operation does not mean `level -= N` without provenance.

## 14. Suppression and already-committed consequences

`condition.value` counts mechanically effective unit applications in the current state view.

Suppression/availability changes can therefore change the derived value without deleting unit records.

Such changes participate in the scoped dependency DAG and may create a new threshold crossing if they move the effective value from below to at/above the threshold.

However already committed external consequences are not algebraically reversed when value later decreases.

Example:

```text
Exhaustion crossed 5 -> 6
    -> Actor became Dead through LifeState resolution

later one unit becomes suppressed
    -> current Exhaustion value may be 5
    -> Actor remains Dead
```

Only an explicit lifecycle/revival mechanic can change the Dead LifeState.

## 15. Effect arbitration relationship

The parent Effect design remains valid with this refinement:

- source/application-specific Effect payload is still governed by ordinary Effect availability/arbitration;
- named Condition intrinsic mechanics are governed by Condition aggregation;
- cumulative unit applications are not accidentally collapsed by a generic one-winner Condition-family arbitration rule;
- Condition aggregation itself is a registered derived node in the accepted scoped dependency DAG.

This preserves the separation:

```text
application lifecycle/provenance
Condition semantic aggregation
application-specific Effect arbitration
Rule Element contribution combination
```

No one subsystem owns all four concerns.

## 16. Rule Element emission

The ordinary resolver collects Condition-intrinsic Rule Elements from the effective Condition representation rather than blindly from every raw Condition-bearing application.

For `presence`:

```text
0 effective applications -> emit none
1+ effective applications -> emit intrinsic Condition payload once
```

For `cumulative_units`:

```text
N effective units -> emit the registered per-unit/equivalent aggregate intrinsic payload for N
```

The D&D Exhaustion seed uses fixed per-unit contributions, which naturally compose through existing calculation selectors.

This is not a second Rule Element engine; it is a bounded upstream source-selection rule for the same resolver.

## 17. Dependency-cycle validation

`condition_aggregation:<condition/policy identity>` remains a typed derived node in the hybrid dependency graph.

Dependencies include the availability/participation of relevant unit applications and any registered facts required by the aggregation/removal policy.

If an application availability predicate depends on the Condition value in a way that creates a cycle, prospective DAG validation rejects activation before commit.

No fixed-point or repeated-until-stable semantics are introduced.

## 18. Persistence and continuity

Concrete unit applications are authoritative state for their lifetime and persist/checkpoint according to the ordinary Effect/application ownership rules.

The effective count, effective representation, and Condition indexes are derived projections.

Runtime continuity checkpoints must retain any non-canonical execution/procedure state needed to resume a pending cumulative-unit application/removal/threshold plan, but must not create a second writable Condition total.

## 19. Performance

For one target/Condition identity, runtime uses indexed relevant applications and bounded aggregation.

Expected common cases:

```text
ordinary Condition:
    existence/aggregation fast path

Exhaustion:
    <= 6 effective units by committed invariant
```

Therefore one-application-per-unit is not a material scaling risk.

## 20. Resolved adversarial findings

```text
B1  cumulative units vs Effect arbitration       RESOLVED
B2  intrinsic vs application-specific payload    RESOLVED
B3  threshold steady predicate/re-trigger         RESOLVED
S1  generic remove-one ambiguity                  RESOLVED
S2  typed provenance requirement                  RESOLVED
S3  Long Rest automatic-only boundary             RESOLVED
S4  source-scoped mass removal                    RESOLVED
S5  meaningful upper bound                        RESOLVED
S6  suppression does not reverse consequence      RESOLVED
S7  aggregation-owned intrinsic emission          RESOLVED
S8  policy-owned value type                       RESOLVED
M1  unit/application terminology                  RESOLVED
M2  effective-representation caching              RESOLVED
M3  source traceability                           RETAINED
```

## 21. Preliminary acceptance

The valued/cumulative Condition nested block is preliminarily accepted for Step-2 sequencing with these invariants:

1. `presence` and `cumulative_units` are the only initial aggregation families;
2. one Exhaustion unit is one authoritative application;
3. Exhaustion effective value is derived and bounded `0..6`;
4. Condition-intrinsic mechanics are emitted from aggregation, not duplicated raw applications;
5. source/application-specific mechanics remain ordinary Effect mechanics;
6. cumulative units are not collapsed by generic one-winner arbitration;
7. provenance-sensitive removal addresses concrete typed unit origins;
8. threshold consequences use crossing-edge semantics and LifeState authority;
9. generic removal is automatic only when its exact result is deterministic;
10. no generic stack counter, arithmetic DSL, or second Condition authority is introduced.

## 22. Exact continuation

The selector/query block and the valued/cumulative Condition nested blocker are now sufficiently closed for Step-2 sequencing.

The next Step-2 work is **schema/catalog alignment** across the accepted Resource, HP/LifeState, Effect/Condition, Duration/Recovery, selector/query, and valued-Condition designs.

After alignment, Step 2 still requires focused validation cases/tests and the final independent Step-2 critical pass before the Step-2 gate can close.