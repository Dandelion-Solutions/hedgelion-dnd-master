# Adversarial Review — Step 2 Valued/Cumulative Condition Semantics

Status: **REVIEW COMPLETE — CORRECTIONS REQUIRED**

Reviewed candidate:

- `DEV/docs/superpowers/design/2026-08-19-step-2-valued-cumulative-condition-design.md`

Related architecture:

- `DEV/docs/superpowers/design/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-recovery-boundary-b2-design.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-lifestate-policy-transition-design.md`
- `DEV/docs/superpowers/design/2026-08-19-step-2-health-effect-selector-query-resolution.md`

Selected primary rules evidence:

- D&D Beyond Basic Rules 2024, Rules Glossary — Condition, Exhaustion, Dehydration, Malnutrition, Suffocation, Long Rest;
- D&D Beyond Basic Rules 2024, Greater Restoration.

Review stance: attempt to break the accepted `one cumulative unit = one application` direction by looking for duplicate authority, overlap/arbitration conflicts, accidental double application of Condition mechanics, ambiguous removal, threshold re-triggering, ordering dependence, persistence loss, and needless abstraction.

## Verdict

The per-unit direction remains the strongest model for D&D Exhaustion because real removal semantics require source/provenance to survive at unit granularity. A single mutable `level` would either lose those semantics or require a nested per-level ledger that duplicates Effect application machinery.

The candidate nevertheless has three blocking correctness gaps and several significant contract gaps. None requires reopening the human-approved product direction; all are mechanical consequences of preserving the already accepted Condition/Effect/LifeState/Recovery boundaries.

## BLOCKING B1 — ordinary Effect arbitration can accidentally collapse cumulative units

### Failure mode

The accepted Effect design derives an application family and allows explicit arbitration to choose which simultaneous applications participate. Condition applications normally share the Condition identity as family.

If several Exhaustion unit applications enter a policy intended for ordinary non-stacking overlap, the Effect layer could select only one application before Condition aggregation. The derived Exhaustion level would then become `1` even though several authoritative unit applications exist.

Conversely, blindly declaring all same-Condition applications participating is unsafe for ordinary presence Conditions whose mechanical semantics must not strengthen simply because two independent applications exist.

### Required correction

Condition aggregation must participate explicitly in application participation semantics.

For named Condition intrinsic mechanics:

```text
Condition applications
    -> lifecycle / basic availability
    -> Condition aggregation policy
    -> effective Condition representation
    -> Condition intrinsic mechanical payload
```

The generic Effect arbitration layer must not silently reinterpret `cumulative_units` as a one-winner overlap family.

`cumulative_units` requires all otherwise eligible unit applications to remain aggregation participants. `presence` may have several source applications but produces one effective Condition identity.

Source/application-specific Effect mechanics remain separately subject to their own ordinary Effect arbitration rules.

### Severity

**BLOCKING.** Without this correction, the approved cumulative semantics can be destroyed by the previously accepted overlap machinery.

## BLOCKING B2 — Condition-intrinsic mechanics and application-specific mechanics are conflated

### Failure mode

The candidate suggests that each Exhaustion unit can carry `-2 D20 / -5 Speed` Rule Elements. That works for cumulative Exhaustion, but the broader Condition model permits several applications of an ordinary Condition with different sources/lifetimes.

If every Poisoned application independently carries the full intrinsic Poisoned mechanics, two applications may duplicate Condition-level behavior before the Rule Element resolver. Relying on every selector operation to happen to be idempotent is not a sound Condition contract.

At the same time, a source Effect may legitimately carry additional mechanics that apply only to that source/application while the target has the Condition. Those mechanics must not be collapsed just because the named Condition itself aggregates to one presence state.

### Required correction

Separate two conceptual payload scopes:

```text
Condition intrinsic mechanics
    -> emitted from the effective Condition aggregation result

Application/source-specific mechanics
    -> emitted from each participating Effect application under ordinary Effect rules
```

For `presence`, intrinsic Condition mechanics are emitted once while effective presence is true.

For `cumulative_units`, intrinsic per-unit mechanics may be emitted once per effective unit, or an equivalent typed aggregate calculation may be used when a real rule requires it. The initial Exhaustion seed can use fixed per-unit contributions.

This is a conceptual ownership split; exact schema fields are deferred to alignment.

### Severity

**BLOCKING.** Otherwise ordinary Conditions can double-apply or source-specific mechanics can be incorrectly discarded.

## BLOCKING B3 — lethal threshold is written as a steady predicate rather than an edge

### Failure mode

The candidate states conceptually:

```text
prospective value >= 6 -> lethal consequence
```

If interpreted literally, every recalculation while value remains at 6 can attempt to trigger death again. Suppression/unsuppression, cache rebuild, hydration, retry, or another unrelated mutation could repeatedly generate the lethal consequence.

### Required correction

Threshold consequences are transition/edge semantics:

```text
before effective value < threshold
AND
after prospective effective value >= threshold
    -> threshold-crossing consequence
```

The crossing is part of one prospective Resolution identity and follows Step-3 idempotency rules.

A later reduction below the threshold does not reverse an already committed LifeState transition. Reaching 6 Exhaustion can cause death; later removing/suppressing an Exhaustion unit does not resurrect the Actor.

If a revived Actor later exists below the threshold and a new prospective change crosses it again, that is a new legitimate threshold crossing.

### Severity

**BLOCKING.** This is required to avoid repeated or reversible hidden LifeState mutation.

## SIGNIFICANT S1 — generic remove-one can become semantically ambiguous

### Failure mode

Per-unit provenance is necessary precisely because units can have different future behavior. A generic Long Rest or Greater Restoration may request “remove one Exhaustion level” while several eligible units remain.

If candidate units differ in future expiry, source-specific cleanup, or removal restrictions, selecting one by SQL order or application ID changes future mechanics.

The D&D rules express an abstract level removal and do not generally expose storage identity to the player.

### Required correction

Removal proceeds in two stages:

1. filter to units eligible under the requesting removal contract;
2. determine whether the eligible alternatives are mechanically equivalent for the surviving future semantics.

If equivalent, runtime may apply a registered deterministic representational tie rule without exposing a fake gameplay choice.

If non-equivalent and the rules provide a selector, use that typed selector.

If non-equivalent and the rules do not determine the result, the automatic responder cannot invent a choice. It must surface a typed Step-3 adjudication/choice requirement.

This is consistent with Recovery B2: an automatic boundary response is automatic only when the exact transition is deterministically derivable.

## SIGNIFICANT S2 — provenance must be typed enough for removal rules

`source_id` alone is not sufficient to represent cases such as “levels gained from suffocation” or “dehydration-origin levels are locked until hydration requirement is satisfied.”

Schema/catalog alignment must preserve a closed typed provenance/removal-relation key such as validated rules origin, application family, cause/mechanic identity, or another registered typed origin contract.

Arbitrary narrative strings such as `origin = "dehydration"` must not become the mechanical selector.

The exact envelope belongs to Step 3 provenance/schema alignment, but Step 2 requires enough typed identity for bounded source-scoped removal queries.

## SIGNIFICANT S3 — Long Rest is not always a trivially automatic decrement

The candidate says the Exhaustion owner may automatically remove one eligible unit on Long Rest.

This is correct only if the responder can determine the exact transition. If provenance-distinct eligible units are mechanically non-equivalent and no rule-selected unit is derivable, Recovery B2 requires escalation into ordinary Step-3 Resolution rather than arbitrary automatic deletion.

The boundary still occurs exactly once. The unresolved Condition response is what may require typed resolution/adjudication.

## SIGNIFICANT S4 — source-scoped mass removal must bypass generic decrement semantics

Suffocation demonstrates a different operation from “remove N generic Exhaustion levels”: when breathing resumes, the mechanic removes the levels produced by suffocation.

The Condition removal capability therefore needs at least two closed semantic families:

```text
remove_count(condition, count, eligibility/removal policy)
remove_origin_units(condition, typed origin/family identity)
```

Names are provisional. The important boundary is that source-scoped removal addresses concrete unit provenance and does not mutate a total counter.

No arbitrary filter expression is introduced.

## SIGNIFICANT S5 — committed effective count must not exceed the meaningful range accidentally

For Exhaustion, the rules-defined meaningful range is 0..6 and 6 causes death.

The runtime must not silently accumulate committed effective levels 7, 8, 9 because application rows happen to be creatable. A prospective operation that reaches/crosses the upper threshold must normalize/validate the complete plan before commit.

Step 3 owns exact same-segment ordering, but Step 2 should establish a committed invariant:

```text
0 <= effective Exhaustion value <= 6
```

Additional applications whose only meaning would be “level beyond death” must not create a new undefined stable gameplay state.

## SIGNIFICANT S6 — suppression can change value but cannot undo consequences already committed

Because `condition.value` counts mechanically effective applications, suppression can lower the derived value without terminating unit records.

That is acceptable, but threshold consequences are historical transitions, not continuous equations. If a unit is later suppressed and value falls from 6 to 5, the Actor does not automatically leave `dead` LifeState.

The design should explicitly separate:

```text
current derived Condition value
from
already committed consequences caused by prior threshold crossings
```

## SIGNIFICANT S7 — automatic per-unit modifiers need a clear aggregation emission contract

For Exhaustion, fixed per-unit `-2` and `-5` contributions are elegant and avoid a generic expression language.

However those contributions should conceptually originate from the `cumulative_units` effective aggregation result, not from blindly collecting every raw Condition application payload before aggregation.

This keeps `presence` and `cumulative_units` behavior consistent and allows HOT to cache the effective Condition representation before emitting intrinsic mechanics.

## SIGNIFICANT S8 — the Condition value type should remain policy-owned, not universally numeric

The selector/query design intentionally describes `condition.value` as a typed scalar/enum/absent result. This nested design must not accidentally redefine all valued Conditions as integer counts.

`cumulative_units` returns an integer count. Future proven policies may expose another typed value, but no universal numeric algebra is implied.

## MINOR M1 — terminology should distinguish unit application from “stack” everywhere

Avoid `stack`, `stack count`, or `stacking` in the new machine contract except when documenting removed provisional names. Use `unit`, `application`, `effective value`, and `aggregation` consistently.

## MINOR M2 — ordinary Condition fast path should cache the effective representation, not raw duplicated semantics

For `presence`, an indexed existence/aggregation result can feed one intrinsic Condition payload. For `cumulative_units`, a bounded effective-unit set/count can feed per-unit payload emission. Cache keys must include state-view identity under the selector/query revision-pinning rules.

## MINOR M3 — source references should be recorded in the design artifact

The candidate already names primary sources. Final resolution should retain traceability to the selected D&D 2024 Basic Rules cases that prove cumulative units and provenance-sensitive removal.

## Cross-system review

### Effect application/arbitration

The per-unit design is compatible only if Condition aggregation is an explicit participation layer. Generic one-winner Effect arbitration must not collapse cumulative unit applications.

### Rule Elements

Condition-intrinsic mechanics should be emitted from the aggregation result. Application-specific mechanics remain ordinary Effect payload. This prevents double application without creating a second calculation engine.

### LifeState

Threshold crossing produces a typed prospective consequence; LifeStateResolver remains the only lifecycle transition planner. Condition value reduction never reverses death automatically.

### Recovery B2

Long Rest may request one-unit removal. It is automatic only when exact removal is deterministic; otherwise Step 3 owns the required choice/adjudication.

### Step 3

Step 3 must own threshold-crossing event identity, atomic create/remove sets, ambiguous removal choice, same-boundary ordering, idempotency, and committed provenance.

### Performance

The model remains bounded if indexes are keyed by target + Condition identity and aggregation works only over relevant applications. Exhaustion's meaningful range is tiny; record multiplication is not a material scaling risk.

## Resolution recommendation

No new human architecture decision is required.

The accepted `cumulative_units` direction should be retained with these corrections:

1. make Condition aggregation explicit in application participation;
2. separate intrinsic Condition mechanics from application/source-specific mechanics;
3. make thresholds crossing-edge semantics;
4. make remove-one equivalence-aware and escalate only genuinely underdetermined cases;
5. require typed origin/removal identity;
6. preserve `0..6` committed Exhaustion invariant;
7. keep all threshold consequences one-way unless an explicit reverse mechanic exists.

After those corrections, run a focused second critical pass against the resolved contract before preliminary acceptance.