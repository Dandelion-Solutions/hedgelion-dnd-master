# Step 2 Condition Intrinsic Rule Scope Resolution

Status: **PRELIMINARILY ACCEPTED — SECOND CRITICAL-PASS BLOCKER RESOLVED**

Target branch: `feature/mechanical-runtime-hot-state`

Parent artifacts:

- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-cumulative-condition-resolution.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-valued-condition-second-critical-pass.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-resolution.md`

This document records the human-architect resolution of the blocker found by the second critical pass. Where this document conflicts with earlier valued-Condition wording, this document is authoritative for the remainder of Step 2.

No runtime implementation or Step-3 execution-order contract is authorized by this checkpoint.

## 1. Human architecture decision

Condition aggregation and intrinsic Condition-rule evaluation are two orthogonal stages with different responsibilities.

The initial accepted axes are:

```text
ConditionAggregationPolicy
    presence
    cumulative_units

IntrinsicRuleScope
    aggregate_once
    per_effective_application
```

`per_effective_application` supersedes the shorter provisional name `per_application` because only applications that participate in the effective Condition representation may emit intrinsic rules.

The two axes are not interchangeable and must not be collapsed into one combinatorial policy enum.

## 2. Responsibility boundary

### `ConditionAggregationPolicy`

Answers:

> Given the mechanically eligible applications of one named Condition in one pinned state view, what effective Condition state exists?

It owns:

- whether the named Condition is mechanically present;
- the policy-owned effective value, when one exists;
- the effective member-application set used for provenance-bound intrinsic evaluation;
- Condition-specific aggregation participation semantics.

It does **not** apply combat modifiers, restrictions, triggers, or other intrinsic rule payloads.

### `IntrinsicRuleScope`

Answers:

> Against which context, and with what cardinality, is one intrinsic rule of the already-aggregated Condition evaluated?

It owns only rule evaluation cardinality/binding:

```text
aggregate_once
    -> evaluate the intrinsic rule once against the aggregate Condition context

per_effective_application
    -> evaluate the intrinsic rule once for each effective member application,
       binding that application's permitted source/provenance/parameters
```

It does **not** decide whether an application is effective and does not alter the aggregate value.

## 3. Normative pipeline

The pipeline is ordered and one-way:

```text
Condition-bearing Effect applications
    -> lifecycle/basic availability
    -> ConditionAggregationPolicy
    -> EffectiveCondition
         present
         typed value when defined
         effective member applications
    -> intrinsic Condition-rule collection
         aggregate_once rules
         per_effective_application rules
    -> ordinary Rule Element / Trigger / Activity machinery
```

The intrinsic-rule stage consumes the aggregation result. It cannot feed application membership changes back into the same aggregation except through separately registered mechanical dependencies that remain subject to the accepted scoped DAG cycle check.

No hidden fixed-point semantics are introduced.

## 4. Why both axes are required

The D&D baseline proves that application multiplicity and intrinsic-rule binding are independent questions.

### Presence-only, source-independent rule

Several Poisoned applications may coexist for independent duration/provenance.

```text
aggregation = presence
Poisoned disadvantage rule = aggregate_once
```

The named Condition is present once and its source-independent intrinsic penalty is not duplicated merely because multiple applications exist.

### Presence-only, source-relative rules

Several Frightened or Charmed applications may coexist and refer to different concrete sources.

```text
aggregation = presence
source-relative intrinsic rule = per_effective_application
```

The Actor has one named Condition presence, while each real source relation is evaluated separately.

### One Condition can require both scopes

A Condition such as Grappled may contain a source-independent global mechanic and source-relative mechanics at the same time.

Conceptually:

```text
Speed restriction
    -> aggregate_once

restriction/relationship relative to the grappler
    -> per_effective_application
```

Therefore `IntrinsicRuleScope` belongs to each intrinsic mechanical item, not to the Condition definition as one global switch.

### Cumulative Condition

D&D Exhaustion uses:

```text
aggregation = cumulative_units
per-unit fixed contributions = per_effective_application
lethal threshold crossing = aggregate_once / aggregate-value semantics
```

The effective value remains derived from unit applications; the rule scope only controls how downstream intrinsic mechanics are evaluated.

## 5. Effective application meaning

For intrinsic Condition evaluation, an `effective member application` is an application that survives the Condition's lifecycle/basic availability and aggregation-participation rules for the pinned state view.

This term is intentionally narrower than:

- merely stored/nonterminal application;
- generic Effect arbitration winner;
- arbitrary source Effect payload participation.

Named Condition aggregation owns the member set used by intrinsic Condition semantics. Generic Effect arbitration must not silently collapse `cumulative_units` or erase multiple relational Condition applications.

## 6. Bound context contract

An `aggregate_once` intrinsic mechanic receives only the registered aggregate Condition context needed by its contract, for example:

```text
condition identity
condition target
condition present/value
pinned state-view identity
registered engine-owned accessors
```

A `per_effective_application` intrinsic mechanic additionally receives only the bound context of the current effective application, such as:

```text
condition_application_id   // runtime/domain identity when permitted
condition_source
rules/causal origin where explicitly permitted
condition_application.parameter(<declared parameter>)
```

It may not enumerate unrelated applications, issue arbitrary domain queries, read arbitrary JSON paths, or turn source binding into a collection-valued generic query language.

## 7. Relationship to source-specific Effect payload

Three concepts remain separate:

1. named Condition intrinsic semantics;
2. the application binding needed by source-relative intrinsic Condition semantics;
3. additional mechanics owned by the concrete source Effect/application itself.

A source Effect may therefore carry ordinary application-specific Rule Elements in addition to causing a named Condition. Those Effect payload mechanics remain governed by Effect availability/arbitration and are not reclassified as Condition intrinsic rules.

## 8. Dependency-DAG consequence

Condition aggregation and intrinsic-rule evaluation participate in the accepted hybrid dependency model.

Typed dependency identity must distinguish at least:

```text
condition_aggregation:<condition/policy>
condition_intrinsic:<condition/rule/scope>
```

For `per_effective_application`, concrete application binding is part of scoped node identity where necessary for cycle detection and diagnostics.

A prospective application that creates a dependency cycle through a source-relative intrinsic rule is rejected before commit.

## 9. Schema consequence

Schema/catalog alignment must represent:

- a registered `ConditionAggregationPolicy` on each mechanically defined Condition, defaulting only where the ruleset explicitly defines the default;
- an `IntrinsicRuleScope` on each intrinsic mechanical item or an equivalent unambiguous schema default;
- only the initial values `presence`, `cumulative_units`, `aggregate_once`, and `per_effective_application`;
- no combined enum such as `presence_per_source` or `cumulative_once`;
- no generic aggregation/reducer expression language.

The exact machine IDs may be normalized mechanically during alignment, but the two semantic axes are fixed by this decision.

## 10. Superseded wording

The following earlier simplification is superseded:

```text
presence -> emit intrinsic Condition payload once
```

The correct rule is:

```text
presence -> aggregate to one named Condition presence

then each intrinsic mechanic independently declares:
    aggregate_once
    OR
    per_effective_application
```

All other accepted `cumulative_units`, per-unit provenance/removal, threshold-crossing, LifeState-authority, and selector/query decisions remain in force.

## 11. Acceptance and continuation

The second critical-pass blocker is resolved with no remaining material human decision in this nested block.

Step 2 may proceed to schema/catalog alignment. Alignment must preserve the ordered separation:

```text
application lifecycle/availability
Condition aggregation
intrinsic rule scope/binding
Rule Element / Trigger evaluation
state mutation through Step-3-owned execution
```

Focused cases and the final independent Step-2 critical pass remain required after machine alignment before Step 2 can close.
