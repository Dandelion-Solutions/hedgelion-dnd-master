# Second Critical Pass — Step 2 Valued/Condition Aggregation

Status: **BLOCKING FOLLOW-UP FOUND — PRELIMINARY ACCEPTANCE SUSPENDED**

Reviewed artifacts:

- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-design.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-adversarial-review.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-resolution.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-effect-application-design.md`

Purpose: run a focused attack pass against the resolved Condition model before allowing schema/catalog alignment.

## Verdict

The `cumulative_units` Exhaustion direction still survives. The per-unit provenance/removal model and threshold corrections remain sound.

However, the resolution's statement that a `presence` Condition emits its intrinsic mechanics once is too coarse for D&D Conditions whose intrinsic definition is relational to the concrete application source.

This is a blocker for schema alignment because it determines how Condition definitions bind application context and emit Rule Elements/requirements.

## Evidence

D&D 2024 explicitly permits multiple effects to impose the same Condition while each instance retains its own duration; the Condition's effects do not generally become numerically stronger, and Exhaustion is the cumulative exception.

At the same time, several baseline Conditions define mechanics relative to the specific source/application:

```text
Charmed
    cannot harm the charmer
    charmer gains social-interaction Advantage

Frightened
    penalties depend on the source of fear being in line of sight
    cannot willingly move closer to the source of fear

Grappled
    attack restriction refers to the grappler
    movement/dragging semantics refer to the grappler
```

Therefore the effective Condition cannot always be reduced to:

```text
present = true
-> emit one source-free intrinsic payload
```

because source identity can be part of the Condition's intrinsic semantics.

## BLOCKING B1 — intrinsic Condition rule evaluation needs an explicit scope

### Failure mode

Consider two independent Frightened applications on one Actor:

```text
F1 source = dragon-A
F2 source = dragon-B
```

If the `presence` aggregator emits the Frightened intrinsic payload only once, which source is bound to `source of fear`?

Choosing one application loses the other source. Merging both into one arbitrary source list changes the Condition contract and creates ad-hoc collection semantics.

The same issue exists for Charmed and Grappled.

Conversely, simply emitting every intrinsic rule once per application is unsafe for source-independent Condition mechanics: multiple Poisoned applications must not numerically strengthen the Condition merely because several durations/sources coexist.

### Required architecture choice

Condition aggregation and Condition intrinsic rule evaluation must be separate axes.

Recommended minimum model:

```text
AggregationPolicy
    presence | cumulative_units

IntrinsicRuleScope
    aggregate_once | per_application
```

The scope belongs to each intrinsic Condition rule/mechanical payload item, not necessarily to the whole Condition, because one Condition may contain both global and source-relative rules.

Examples:

```text
Poisoned:
    disadvantage on attacks/checks
        -> aggregate_once

Frightened:
    disadvantage while source of fear visible
        -> per_application, source bound
    cannot move closer to source of fear
        -> per_application, source bound

Grappled:
    Speed = 0
        -> aggregate_once
    attack restriction relative to grappler
        -> per_application, source/grappler bound
    grappler movement relationship
        -> per_application, source/grappler bound

Exhaustion:
    per-level D20/Speed contributions
        -> per_application under cumulative_units
```

This is not a new query DSL. `per_application` evaluation receives only the validated bound context of the current effective Condition application, such as target, source/provenance roles, and declared typed application parameters.

### Why scope should be per rule, not per Condition

Grappled demonstrates that one Condition can mix source-independent and source-relative effects. A single Condition-wide `aggregate_once` or `per_application` switch therefore either loses relational semantics or duplicates global mechanics.

Per-rule scope is the smallest model that represents the baseline rules without duplicating entire Condition definitions.

## Relationship to non-stacking semantics

`aggregate_once` ensures source-independent intrinsic mechanics are emitted once for effective presence regardless of application count.

`per_application` does not mean arbitrary numeric stacking. Each emitted rule still resolves through its registered Rule Element/constraint combination semantics.

For relational rules, multiple application contexts represent multiple real relations rather than a generic stack count.

Example:

```text
Charmed by A + Charmed by B
    -> one named Charmed presence
    -> relational restrictions/benefits can bind A and B separately
```

The engine does not turn this into `Charmed level = 2`.

## Bound context contract

A per-application intrinsic Condition rule may read only registered application-bound roles/parameters.

Conceptually:

```text
condition_target
condition_source
condition_application.parameter(<declared id>)
causal/rules origin where explicitly permitted
```

It may not perform arbitrary world queries or enumerate unrelated applications.

This fits the previously accepted three-surface selector/query boundary.

## Dependency-DAG impact

Per-application intrinsic rules become ordinary typed mechanical dependency nodes/edges in the scoped DAG.

The application binding is part of concrete node identity where required. A cycle created only by one source-relative application must still be detected before prospective commit.

No fixed-point semantics are introduced.

## Effect-application relationship

The refined pipeline becomes:

```text
Condition-bearing Effect applications
    -> lifecycle/basic availability
    -> Condition aggregation
    -> effective Condition + effective member applications
    -> aggregate_once intrinsic rules
    -> per_application intrinsic rules with bound application context

PLUS

participating source/application-specific Effect payload
    -> ordinary Effect arbitration/Rule Element path
```

This preserves three distinct concepts:

1. named Condition intrinsic semantics;
2. Condition application/source binding;
3. source Effect's additional mechanics.

## Alternatives considered

### A. Emit all intrinsic Condition mechanics per application

Simpler runtime, but correctness depends on every source-independent operation being idempotent under duplication. That is an undocumented global assumption and unsafe for future rulesets.

Rejected.

### B. Emit one intrinsic payload per effective Condition and make source a collection

This creates collection-valued source semantics for every relational Condition, complicates predicates and constraints, and makes simple one-source rules reason about sets.

Rejected.

### C. Two intrinsic rule scopes: `aggregate_once` and `per_application`

Recommended. It makes source-independent non-stacking explicit and retains application-relative semantics without introducing a generic aggregation language.

## Decision brief

### Recommendation

Adopt per-intrinsic-rule scope:

```text
aggregate_once
per_application
```

orthogonal to:

```text
presence
cumulative_units
```

### Strongest cost

Condition definition/schema and runtime collection become slightly more explicit: each intrinsic rule must declare or inherit its evaluation scope.

### Why the cost is justified

The selected D&D baseline already proves both scopes and even proves that one Condition can require both. Without the distinction, the engine either loses application-source semantics or relies on accidental idempotence.

### Confidence

**HIGH**.

### What would change the recommendation

A representation that preserves source-relative Charmed/Frightened/Grappled semantics and ordinary non-stacking with fewer explicit concepts, while remaining deterministic and typed, would justify reopening this choice. No such simpler representation is currently evident.

## Gate status

The earlier valued/cumulative Condition resolution remains valid for Exhaustion-specific cumulative-unit semantics except for its overly broad `presence -> emit intrinsic payload once` wording.

Schema/catalog alignment remains blocked until the human architect accepts or replaces the intrinsic-rule-scope correction above.
