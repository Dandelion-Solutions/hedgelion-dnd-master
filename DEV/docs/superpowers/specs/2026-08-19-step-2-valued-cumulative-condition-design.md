# Step 2 Valued/Cumulative Condition Semantics

Status: **CANDIDATE — OWNER-APPROVED DIRECTION, ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Parent designs:

- `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-resolution.md`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`.

The human architect approved the recommended `cumulative_units` direction after the selector/query design exposed a real valued-Condition requirement. No runtime implementation or final machine-schema migration is authorized by this checkpoint.

## 1. Problem statement

The preliminary Step 2 Condition model established that:

- `definition.condition` is a named rules identity;
- each concrete Condition application is ordinary target-local Effect-instance state;
- Actor condition lists are derived projections, not canon;
- generic mutable Effect stacks are not part of the preferred model;
- `condition.present` and `condition.value` are derived MechanicalContext reads.

The remaining question is how a Condition whose effective state has a numeric or otherwise valued dimension should be represented without introducing a second Condition authority, a generic stack subsystem, or special-case mutable counters.

D&D 2024 Exhaustion is the required seed case because it is explicitly cumulative, has a bounded lethal threshold, modifies multiple calculations by its current level, loses levels individually, and can impose source-specific restrictions on when particular levels may be removed.

## 2. Evidence and constraints

Selected D&D 2024 Basic Rules establish the following mechanically relevant facts:

1. ordinary identical Conditions do not stack; Exhaustion is an explicit exception;
2. each time a creature receives Exhaustion it gains one level;
3. level 6 is lethal;
4. D20 Tests are reduced by `2 × Exhaustion level`;
5. Speed is reduced by `5 × Exhaustion level` feet;
6. finishing a Long Rest removes one Exhaustion level;
7. Greater Restoration may remove one Exhaustion level;
8. Exhaustion caused by dehydration or malnutrition cannot be removed until the corresponding recovery prerequisite is satisfied;
9. Suffocation can create multiple Exhaustion levels and removes the levels caused by suffocation when breathing resumes.

Source references used for this design:

- D&D Beyond Basic Rules 2024, Rules Glossary — Condition, Exhaustion, Dehydration, Malnutrition, Suffocation, Long Rest.
- D&D Beyond Basic Rules 2024, Greater Restoration.

The architectural implication is important: a single total `level` is not always enough to decide which part of the cumulative state is removable, because provenance can affect removal eligibility.

## 3. Accepted direction

### 3.1 One cumulative unit is one ordinary application

For a Condition using the initial `cumulative_units` aggregation policy:

```text
one mechanically independent unit
    =
one ordinary target-local Condition/Effect application
```

For Exhaustion:

```text
Effect E1 -> Exhaustion unit, origin dehydration
Effect E2 -> Exhaustion unit, origin forced march
Effect E3 -> Exhaustion unit, origin spell/feature
```

The effective Condition value is derived:

```text
condition.present(actor, exhaustion) = true
condition.value(actor, exhaustion) = 3
```

No Actor `exhaustion_level` field, ConditionState counter, generic stack count, or duplicate Resource is introduced.

### 3.2 Why one application per unit

This uses the existing Effect application model to preserve, per unit when needed:

- source/origin provenance;
- lifecycle state;
- duration/TemporalBinding;
- removal eligibility;
- suppression/availability;
- trigger ownership;
- audit/history identity.

A single mutable Effect containing only `level = 3` would lose this information. Adding an internal per-level ledger to that Effect would recreate a miniature stack/application subsystem inside one record and duplicate the already accepted Effect-instance lifecycle machinery.

## 4. Initial Condition aggregation policies

Step 2 introduces only two proven aggregation-policy families.

### `presence`

The ordinary Condition model.

Semantics:

```text
zero mechanically effective applications
    -> Condition absent

one or more mechanically effective applications
    -> Condition present
```

Multiple independently running applications may exist for source/duration provenance, but their ordinary Condition semantics do not numerically strengthen merely because several applications are present.

### `cumulative_units`

The bounded cumulative model proven by Exhaustion.

Semantics:

```text
effective value
    =
count of mechanically effective eligible unit applications
```

Each application contributes exactly one unit in the initial contract.

Do not introduce generic `sum`, `max`, `min`, arbitrary weighted aggregation, expressions, or user-defined aggregation code until a real rules seed proves them necessary.

## 5. Condition definition contract

Conceptually, a Condition definition may select a registered aggregation policy:

```text
aggregation_policy = presence | cumulative_units
```

Exact field naming belongs to schema/catalog alignment.

For `cumulative_units`, the definition also owns the bounded semantic constraints required by the Condition identity, such as:

```text
minimum effective value = 0
maximum meaningful value = 6 for D&D Exhaustion
```

However the maximum is not stored as mutable target state. It is definition/ruleset policy used for validation and threshold semantics.

The Condition definition does not own each unit's provenance, duration, or lifecycle; each application instance owns those facts.

## 6. Authority model

```text
Condition definition
    -> named identity + aggregation policy + reusable mechanics

Effect/Condition unit applications
    -> DIRECT authoritative concrete units

condition.present(...)
    -> DERIVED effective boolean

condition.value(...)
    -> DERIVED effective typed value
```

No other Condition-value authority is permitted.

For `cumulative_units`, derived value is never persisted onto Actor state merely for convenience. HOT/SQLite may cache/index it as disposable projection keyed by state-view identity.

## 7. Application and gain semantics

When a mechanic grants `N` cumulative units and the rules make those units independently removable/provenance-bearing, the prospective mutation creates `N` application identities atomically.

For the D&D Exhaustion baseline, ordinary gain is one unit at a time, but the contract permits one operation to materialize several units if a real mechanic grants several simultaneously.

Example:

```text
before: exhaustion value = 2
prospective gain = 2 units

after plan:
    create Exhaustion E3
    create Exhaustion E4
    prospective value = 4
```

The mutation is validated under the existing prospective-state and dependency-DAG rules before commit.

The engine must not partially create one of two required units if the operation is semantically atomic.

## 8. Reapplication is not generic stacking

`cumulative_units` is a narrow Condition aggregation policy, not permission to restore generic Effect stacks.

Ordinary Effect reapplication policy remains governed by the Effect application design: create, refresh, replace, or other explicitly registered policy as appropriate.

For a cumulative Condition, gaining a new unit ordinarily creates a new independent application. It does not increment `world.effect.stacks` and does not mutate an existing unit into a count container.

## 9. Mechanical effects of cumulative value

A Condition's downstream mechanical consequences should use existing Rule Element calculations whenever those consequences can be represented compositionally.

For D&D Exhaustion, one unit can contribute the same fixed per-unit mechanics:

```text
D20 Test contribution: -2
Speed contribution: -5 feet
```

Three participating units naturally resolve to `-6` and `-15` through the ordinary typed contribution resolver.

This is preferred to introducing a general arithmetic expression such as:

```text
condition.value(exhaustion) * -2
```

merely for this seed case.

`condition.value` still exists because other mechanics may need the effective level directly, threshold checks require a typed value, diagnostics/UI may expose it, and future proven rules may reference the level explicitly.

## 10. Threshold consequences

Some cumulative Conditions may define a consequence when the effective value reaches or crosses a threshold.

For D&D Exhaustion:

```text
prospective effective value >= 6
    -> lethal consequence
```

The Condition subsystem does not directly mutate `life_state_id` as a hidden side effect.

Instead, reaching the registered threshold produces a typed prospective consequence/trigger owned by the ordinary Resolution/LifeState path. Step 3 owns the exact Signal/Event/Activity representation, same-mutation ordering, idempotency, and receipt semantics.

The architectural requirement for Step 2 is:

- the threshold is detected against the same pinned prospective state view;
- the lethal consequence participates in the same atomic Resolution plan;
- LifeStatePolicy does not hard-code knowledge of the concrete `Exhaustion` Condition ID;
- the Condition does not bypass the ordinary LifeState transition authority.

## 11. Removal semantics

Removing one cumulative unit is a domain operation over concrete applications, not arithmetic mutation of a total counter.

Conceptually:

```text
request: remove 1 unit of Condition X
    -> discover eligible effective unit applications
    -> apply registered removal eligibility/policy
    -> select the unit(s) deterministically when rules determine the result
    -> otherwise surface typed adjudication/choice under Step 3
    -> terminate selected application(s)
    -> derive new effective value
```

### 11.1 Source-specific removal eligibility

A unit may carry origin/provenance or another typed property that causes a removal mechanic to be ineligible for that unit until a rule-owned prerequisite is satisfied.

Examples include dehydration- or malnutrition-origin Exhaustion.

The generic Condition aggregator does not interpret narrative source text. Eligibility must be represented through typed mechanic/provenance data or a typed rule owned by the producing application/definition.

### 11.2 Source-specific mass removal

A rule may remove all units it created rather than a generic number of units.

Suffocation demonstrates this shape: when breathing resumes, Exhaustion gained from suffocation is removed.

This is naturally expressed as a closed domain query/removal contract over applications with the appropriate typed origin/family identity. It does not require subtracting an unqualified integer from a shared total.

### 11.3 Ambiguous removal

If several eligible applications exist and choosing which one to remove changes future mechanics, while the rules do not determine the choice, the engine must not select by array/SQL/application-ID order.

The Resolution path must expose the required typed choice/adjudication.

If all eligible units are mechanically equivalent for all surviving semantics, an implementation may choose one through a registered deterministic tie rule, but this must not erase required provenance.

## 12. Long Rest and recovery boundary

Long Rest remains a typed boundary occurrence under Recovery B2.

The Exhaustion Condition owner may register an automatic response equivalent to:

```text
on boundary.long_rest_complete(subject):
    remove one eligible Exhaustion unit
```

This does not make RestPolicy the owner of Exhaustion state.

If no unit is removable because every current unit has an unmet source-specific restriction, no impermissible unit is removed merely because the boundary occurred.

The exact ordering between Condition-unit removal, Effect expiry, Resource recovery, HP restoration, and other same-boundary consequences remains Step-3 ordering territory under the accepted discover-first / plan-then-commit model.

## 13. Greater Restoration and explicit removal mechanics

A mechanic such as Greater Restoration requests removal of one Exhaustion unit through the typed Condition-removal capability.

It does not decrement a hidden Actor counter and does not directly delete an arbitrary Effect row.

The removal resolver discovers eligible Exhaustion unit applications in the pinned prospective state view and returns the transition plan or a typed failure/choice result.

## 14. Presence-only Conditions remain cheap

The cumulative model must not make every ordinary Condition expensive.

`presence` remains the fast path:

```text
indexed effective application existence
    -> boolean present
```

`cumulative_units` adds only a bounded count over effective applications for the named Condition/subject. Runtime must use target + Condition identity indexes; no campaign-wide scans are permitted.

HOT may cache effective count by `(state_view, target, condition_id)` and invalidate it when a relevant application changes.

## 15. Dependency-DAG participation

Condition aggregation is already a registered derived-stage node kind under the selector/query resolution.

For cumulative Conditions, conceptually:

```text
condition_aggregation:exhaustion
    -> depends on participation/availability of relevant unit applications
```

If an application's availability predicate itself depends on `condition.value(exhaustion)` or another derived stage that closes a cycle, the scoped prospective DAG validation rejects the mechanic before commit.

No fixed-point interpretation such as "count until stable" is introduced.

## 16. Suppression and effective count

`condition.value` counts mechanically effective applications, not merely stored nonterminal rows.

Therefore an application that is non-participating under its registered availability/suppression/arbitration semantics does not contribute a unit unless that Condition's explicit aggregation contract says otherwise.

Lifecycle existence and effective mechanical participation remain separate axes.

This also means effective value may change when an existing application becomes suppressed/unsuppressed without creating or deleting the underlying application. The resulting change is derived from the state view and must participate in dependency/threshold validation where mechanically relevant.

## 17. Upper bounds and lethal threshold normalization

For D&D Exhaustion the effective rules stop normal play at the lethal threshold of 6.

The engine should not treat `7`, `8`, etc. as ordinary stable Exhaustion levels merely because more unit applications could physically exist.

A prospective operation that would move the effective count through the lethal threshold must first plan the threshold consequence. Exact post-death treatment of additional same-segment Exhaustion applications is a Step-3 ordering/normalization question and must not be inferred from storage insertion order.

Step 2 requires only that values beyond the rules-defined meaningful range never become an accidental independent gameplay state with undefined semantics.

## 18. Why Exhaustion is not a Resource

Exhaustion superficially resembles a numeric pool but fails the Resource ownership test:

- it is a Condition identity with Condition semantics;
- individual units may carry provenance and removal restrictions;
- gaining units is not spending capacity;
- recovery removes Condition applications rather than refilling a reusable pool;
- lethal threshold is a Condition consequence, not zero/full Resource behavior.

Representing Exhaustion as `definition.resource` would duplicate Condition identity and complicate rules that ask whether the creature "has the Exhaustion condition".

## 19. Why a single mutable application value is not preferred

Alternative:

```text
one Exhaustion Effect
    parameter.level = N
```

Advantages:

- fewer stored application records;
- effective value is a direct read.

Rejected as the default because real D&D rules require per-origin removal behavior. To preserve that behavior the single application would need internal structures equivalent to:

```text
units[]
    source
    duration
    removal_lock
    provenance
```

That duplicates the ordinary Effect application lifecycle model and creates a bespoke nested stack ledger.

A future Condition whose valued state is genuinely one indivisible episode rather than independent cumulative units may justify a single typed application value. That would be a distinct proven aggregation/application policy, not a reason to weaken the Exhaustion model.

## 20. No universal valued-Condition algebra

This design intentionally does not define a general Condition algebra.

Not introduced:

```text
sum arbitrary values
max/min aggregation
weighted units
custom reducer code
expression trees
arbitrary per-application arithmetic
user-defined aggregation callbacks
```

If another ruleset later proves a `max_severity` or single-episode scalar model, add the smallest registered policy that represents that real mechanic.

## 21. LLM boundary

The LLM may narrate that a creature looks exhausted or interpret fiction that leads to a typed Exhaustion-producing mechanic.

It may not assert authoritative values such as:

```text
"Exhaustion level is 4"
"remove these two engine-owned Exhaustion applications"
```

unless the deterministic runtime exposes an explicit typed choice/action permitting that input.

The engine derives present/value, eligible unit identities, source restrictions, and threshold consequences from the pinned state view.

## 22. Persistence and recovery

Each unit application is ordinary authoritative Effect/Condition state and therefore participates in the normal campaign/runtime persistence rules for that application's lifetime.

Derived effective Condition counts are disposable projections and need not be independently canonicalized.

Continuity checkpoints must preserve any non-canonical runtime state required to determine whether a unit is currently effective/removable or to resume a pending removal/threshold Resolution, consistent with the separate runtime-continuity roadmap item. They must not store a second writable Exhaustion total as recovery authority.

## 23. Performance characteristics

For one target and one named Condition:

```text
lookup relevant applications by indexed (target, condition identity/family)
filter/derive effective participation
count eligible participating units
```

Cost should be proportional to applications for that target/Condition, not total campaign Effect count.

For D&D Exhaustion, the mechanically meaningful count is tiny and bounded, so separate application identities are not a scaling concern.

## 24. Failure behavior

Representative typed failures include:

- unknown aggregation policy -> definition validation failure;
- `cumulative_units` applied to an application contract that does not represent one unit -> definition validation failure;
- removal request with zero eligible units -> typed ineligible/no-op result according to the requesting mechanic;
- ambiguous mechanically meaningful removal choice -> typed choice/adjudication requirement;
- prospective application causes dependency cycle -> reject before commit;
- threshold consequence cannot be planned -> Resolution validation failure, not partial application commit;
- LLM attempts to supply derived Condition value as authority -> invocation validation failure.

## 25. Analytical challenge

### Strongest alternative

Use one mutable Exhaustion application with a numeric `level`.

### Why it loses

It is simpler only if provenance does not matter. The selected rules prove provenance-sensitive removal behavior, so preserving correctness would require a nested per-level ledger, duplicating the Effect application model.

### Simplest viable alternative

One unit = one ordinary application, with `condition.value` as derived count. It reuses existing lifecycle, provenance, indexing, duration, suppression, dependency, removal, and persistence infrastructure.

### Strongest risk in the recommendation

A future valued Condition may not decompose into independent units. The mitigation is not to generalize Exhaustion further: `cumulative_units` is one registered policy among a deliberately small evidence-driven family.

### Recommendation confidence

**HIGH** for Exhaustion and other truly cumulative independent-unit Conditions.

**HIGH** that only `presence` and `cumulative_units` should be introduced in the initial Step-2 schema.

**MEDIUM** on exact serialized field names and threshold/removal operation vocabulary until schema/catalog alignment and Step-3 operation contracts.

### What would change the recommendation

A primary rules seed showing that Exhaustion levels must behave as one inseparable mutable episode with no mechanically relevant per-unit provenance would weaken the per-unit model. The currently selected D&D 2024 rules show the opposite.

## 26. Candidate acceptance criteria

This nested design can be preliminarily accepted if adversarial review confirms that:

1. effective valued Condition state has one authority path;
2. Exhaustion provenance/removal restrictions remain representable;
3. ordinary Conditions remain `presence` fast-path mechanics;
4. generic Effect stacks are not reintroduced;
5. no unnecessary general aggregation DSL is created;
6. lethal threshold uses ordinary LifeState/Resolution authority rather than hidden mutation;
7. Long Rest and other removal mechanics respect Recovery B2 ownership;
8. Condition aggregation participates in the scoped dependency DAG;
9. HOT indexes/caches remain derived projections;
10. schema alignment can represent the model without inventing duplicate state.

## 27. Next process step

Run an independent adversarial review against this design, the Effect-application model, Recovery B2, LifeState transition model, selector/query resolution, and selected Exhaustion seed cases.

Resolve findings before marking valued/cumulative Condition semantics preliminarily accepted and proceeding to Step-2 schema/catalog alignment.