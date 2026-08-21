# Step 2 Retrospective Assurance — Slice B Resolution

Status: **ASSURED / AMENDED / STEP 2 REMAINS CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Verdict

The retrospective problem-first pass reaffirms the accepted Effect/Condition architecture:

```text
one independent target-local application -> one world.effect
Condition named identity -> definition.condition
Condition application -> ordinary world.effect
application lifecycle -> canonical application state
availability/suppression -> derived
Effect arbitration -> derived
Condition aggregation -> derived
Rule Element combination -> separate calculation layer
maintained support -> zero/one immutable support parent
```

No generic stack counter, multi-target mutable Effect record, `world.condition`, persistent winner state, general support graph, or callback language is required.

## 2. Condition immunity/effectiveness refinement

`condition.applicability` is now interpreted narrowly as:

> whether a specific named Condition may mechanically affect a specific subject in the current pinned/prospective application context.

It has two consumers:

1. prospective validation of a new Condition application;
2. eligibility of an already-existing nonterminal Condition application before Condition aggregation.

This closes the real D&D case where immunity is gained after application. A currently immune target is not mechanically affected by the Condition even if an independent application record still has remaining lifecycle/duration.

Therefore:

```text
nonterminal application
+ current condition immunity
    -> application excluded from effective Condition aggregation
    -> lifecycle remains nonterminal unless another rule explicitly ends it
```

If immunity later ends before the application's independent lifecycle ends, the application may become effective again by derived reevaluation. No resurrection mutation occurs.

This uses the already accepted lifecycle-versus-availability separation rather than adding a stored suppression flag.

Slice D must machine-close the selector's bounded consumer/binding/dependency contract.

## 3. Provenance identities

Effect application provenance keeps four concepts distinct:

```text
definition_id
    reusable Effect/Condition payload applied by this application

rules_origin_id
    reusable definition whose rule semantically created the application and,
    where applicable, defines application-family sameness

source_id
    concrete world source instance when one exists

causal execution origin
    concrete Step-3 command/Resolution/segment/Event occurrence that created or
    materially changed this application episode
```

The causal execution origin is not stored in `rules_origin_id` or `source_id`.

### Application-family derivation

Initial family rule:

```text
Condition-bearing application:
    family = Condition definition_id

non-Condition application with explicit rules_origin_id:
    family = rules_origin_id

otherwise direct generic Effect:
    family = Effect definition_id
```

`source_id` does not define family by default. Reapplication can explicitly add same-source matching through its registered match policy.

`rules_origin_id`, when present, must resolve to reusable content in the same `ResolvedCatalogContext`; it is not arbitrary world identity or free-form prose. Exact cross-record compiler validation remains part of the reference/compiler work rather than string-prefix inference.

## 4. Causal recency carry-forward

Registered Effect arbitration may require mechanical recency. Wall-clock time, SQL order, lexical Effect IDs, and current cache order are invalid recency sources.

Step 3 must provide a durable concrete causal ordering relation for Effect application create/refresh/replace, sufficient for:

- deterministic arbitration after restart;
- retry/idempotency;
- causal receipts/audit;
- replacement/refresh ordering.

The exact authority may be a creator/last-material-change Event/segment reference on Effect state or another single durable causal relation. Slice E/Step 5 must ensure history compaction cannot remove the only recency fact required by a still-live application.

## 5. Closed terminal reasons

`world.effect.lifecycle.terminal_reason_id` is executable lifecycle vocabulary, not descriptive metadata.

The schema now accepts only the registered initial reasons:

```text
effect_end.expired
effect_end.removed
effect_end.replaced
effect_end.support_lost
```

A focused RED test showed the prior schema accepted an invented reason; after the schema correction the contract is closed. New reasons require coordinated registry/schema evolution.

## 6. Support/source/lifecycle boundaries retained

- `source_id` is provenance, not automatic structural support.
- Source death/retirement does not universally end an Effect.
- Concentration/support explicitly models rules that do depend on another Effect episode's existence.
- Parent suppression does not break support; parent terminal state expires descendants.
- No multi-parent support or reparenting is introduced without a concrete rules case.
- Target transfer ends the old target-local episode and creates a new one rather than mutating `target_id`.

## 7. Condition aggregation retained

The accepted independent axes remain:

```text
ConditionAggregationPolicy
    presence
    cumulative_units

IntrinsicRuleScope
    aggregate_once
    per_effective_application
```

Immunity/applicability is evaluated before aggregation participation. It does not replace aggregation.

Exhaustion remains one application/unit per level with derived bounded effective value, per-unit provenance, crossing semantics, source-sensitive removal, and no generic stack field.

## 8. Zone/aura boundary retained

Persistent spatial mechanics may target a Zone/Location/Asset as the one Effect lifecycle owner. Creature-local child applications are created only when the rule creates independently targetable/persistent creature state.

This avoids mandatory per-creature Effect multiplication for transient aura/zone participation while preserving one-target application semantics.

## 9. Terminal retention/GC

Terminal lifecycle and physical retention remain separate.

After support/end consequences, durable publication/audit requirements, and live references permit it, terminal Effects may be compacted/garbage-collected by later persistence policy. Long-term causal history belongs to committed event/trace/checkpoint history rather than requiring all terminal Effects to remain in active world state forever.

Step 5 must preserve any causal/recency/provenance fact still required by live Effects before compacting its source row/history.

## 10. Safe deferrals

### Step 3

- concrete causal create/refresh/replace identity/order;
- exact typed provenance-sensitive remove-one operations/adjudication;
- same-time terminal/event ordering;
- reference validation at execution binding;
- retry/idempotency for application creation.

### Slice D

- machine metadata for `condition.applicability` consumers/bound application context/dependencies;
- integration of immunity-driven Effect/Condition availability into the scoped DAG.

### Step 5

- promotion closure for local source/support/definition references;
- retention/GC/history compaction preserving live causal requirements;
- cross-scene spatial Effect ownership.

### Step 6

- any additional arbitration/support/removal semantics proven by the full rules seed.

## 11. Verification

Focused schema validation now rejects unregistered Effect terminal reasons. The full engine-source validation workflow is rerun on the corrected branch before the assurance overlay is closed.

## 12. Final disposition

Recommendation: **KEEP Step 2 closed with the applied Effect/Condition amendments.**

Human decision required: **NO**.

Confidence: **HIGH**.
