# Step 2 Retrospective Assurance — Slice A Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — BOUNDED CORRECTIONS REQUIRED, NO HUMAN GATE**

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Verdict

The critic could not break the accepted HP/LifeState ownership split or justify a new Actor-state subsystem.

The Resource review does uncover one important qualification to the proposed capacity-normalization rule and confirms the timed-recovery cardinality mismatch. Both can be corrected without changing the accepted `current`/`spent` ownership model.

## 2. Health/LifeState attacks

### Derive LifeState entirely from HP

Rejected. It fails character-like dying/stable rules, direct-death/revival semantics, undead/form distinctions, and important NPC policy variation.

### Make death saves a generic Resource

Rejected. Their identity/lifetime is intrinsically the current Dying episode and they are not an ordinary spend/recovery pool.

### Add explicit lifecycle episode IDs

Not justified. Transition/event identity plus state-local progress already distinguishes episodes and avoids another current-state authority.

### Persist `dead_since`

Not justified. Only mechanics with death-age requirements need it, and current dead-episode origin is recoverable from causal chronology. Snapshot/compaction must preserve that recoverability later.

No new health/lifecycle finding remains.

## 3. Resource finding A-C1 — `current <= capacity` is valid only for state-stable capacity

**Severity: SIGNIFICANT cross-slice constraint.**

The coverage recommendation proposed:

```text
persistent current-model ResourceState:
0 <= current <= resolved capacity
```

and prospective clamping when capacity shrinks.

This is coherent only if the capacity used to enforce canonical state is derived from the same authoritative/prospective state being committed. It becomes unsafe if `resource.capacity` can depend on ephemeral invocation-only adjudicated facts:

```text
same canonical ResourceState
call A context -> capacity 5
call B context -> capacity 3
```

Canonical `current` cannot be clamped differently depending on which Activity happens to ask.

### Resolution

Keep the normalization rule, but add the following architectural invariant:

> A calculation whose output constrains canonical ResourceState normalization must be **state-stable** for the pinned committed/prospective view. `resource.capacity` may depend on registered engine-owned authoritative/derived state and participating mechanics, but not on ephemeral `INVOCATION_ADJUDICATED` facts whose truth exists only for one invocation.

A temporary inability to spend a Resource belongs to Resource/Activity availability or a usage gate, not a context-specific capacity value.

This belongs mechanically to both Slice A and later Slice D. Slice D must verify that selector/accessor registry metadata can enforce the distinction rather than leaving it as prose.

With that constraint, true capacity changes caused by committed/prospective state changes may normalize persistent `current` atomically:

```text
current := min(current, new_capacity)
```

Capacity growth never restores units by itself.

### Why not preserve hidden surplus?

A hidden surplus is incompatible with a simple `current` representation: if `current=5`, `capacity=3`, then decrementing current by one leaves `available=min(4,3)=3`, so a spend can fail to reduce availability. Fixing that requires extra state or special arithmetic and destroys the purpose of the current-model fast path.

### Why not change persistent resources to `spent`?

D&D persistent pools such as charges, spell-slot counts, feature uses, and similar recoverable quantities naturally support partial restore/current-value semantics. Procedure budgets such as movement/actions have a stronger reason to preserve consumption through dynamic capacity. The existing owner/storage split remains justified for the current rules surface.

## 4. Resource finding A-C2 — multiple metric recovery policies do not fit one binding

**Severity: MODERATE machine-contract mismatch.**

Confirmed. The definition schema allows multiple independent `after` rules, but Actor/Asset ResourceState owns one `recovery_binding`.

The critic tested two alternatives:

### Make ResourceState own `recovery_bindings[]`

Flexible, but adds list lifecycle, due-set identity, multiple re-arm semantics, and more Agenda entries without a proven D&D case.

### Restrict the initial definition contract

Allow:

- any number of registered boundary-based recovery rules;
- at most one metric-delay recovery rule per Resource definition/current state model;
- the one metric rule may re-arm the next binding after it fires when the rule describes repeated recharge.

Recommended. A future concrete mechanic with simultaneous independent timed recoveries can reopen binding cardinality.

The restriction also makes operation provenance unambiguous: the sole metric recovery rule associated with the Resource definition determines what the current `recovery_binding` means, so the TemporalBinding itself does not need a duplicated recovery-policy ID.

## 5. Procedure-local state attack

The critic asked whether Step 2 is incomplete because procedure-local ResourceState has no final world/runtime JSON owner.

Verdict: **DEFERRED_OK**, because the semantic owner is already exact:

```text
procedure identity + participant + Resource definition -> spent
```

and Step 3 explicitly owns checkpointable active procedure execution state. Prematurely placing the same map into both `world.encounter` and `runtime.continuation` now would be worse. Slice E must verify exactly one portable owner is chosen.

## 6. Transformation attack

The critic confirms that transformation is safe only because Step 1 already forbids blind state carry-forward. Step 3's `op.transform_entity` contract must explicitly validate definition-dependent Resource/HP/LifeState state migration. No generic merge algorithm belongs in Step 2.

## 7. Same-boundary interaction attack

Consider a Long Rest boundary where:

- an Effect that changes Resource capacity expires;
- the Resource restores to capacity;
- HP/LifeState also responds.

The final value can depend on whether recovery uses old or new capacity. Step 2 correctly assigns response ownership but does not choose list/SQL order. Step 3 must resolve the boundary as one deterministic prospective closure against explicit phase/dependency semantics. This remains a safe downstream dependency and is already in the Step-3 Task Brief.

## 8. Recommendation

Apply:

1. persistent-current capacity normalization semantics;
2. state-stable restriction for capacity used to constrain canonical state;
3. at-most-one metric-delay recovery rule in the initial Resource contract;
4. focused negative tests for recovery cardinality;
5. carry selector state-stability enforcement to Slice D.

Recommendation: **AMEND / KEEP STEP 2 CLOSED**.

Human decision required: **NO**.

Confidence: **HIGH** for health/lifecycle ownership and capacity normalization under the state-stable constraint; **HIGH** for restricting metric recovery to one active policy until a real multi-timer rule appears.
