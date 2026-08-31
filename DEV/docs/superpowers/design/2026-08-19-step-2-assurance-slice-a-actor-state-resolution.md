# Step 2 Retrospective Assurance — Slice A Resolution

Status: **ASSURED / AMENDED / STEP 2 REMAINS CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Verdict

The retrospective problem-first pass reaffirms the accepted HP/LifeState/Resource ownership architecture. No new Actor state subsystem, lifecycle FSM, wound authority, or Resource entity is required.

Two bounded Resource contracts were missing and are now resolved.

## 2. Persistent current-model Resource normalization

For persistent Actor/Asset Resources using `state_model=current`, committed state obeys:

```text
0 <= current <= state-stable resolved capacity
```

When a prospective authoritative state change lowers true Resource capacity below stored `current`, the same prospective transition normalizes:

```text
current := new_capacity
```

Capacity growth alone does not restore/grant uses. Recovery or another explicit typed mechanic does that.

Operations remain:

```text
spend n:
    require current >= n under the same pinned/prospective capacity view
    current := current - n

restore_to_capacity:
    current := capacity

restore_amount n:
    current := min(capacity, current + n)
```

A mechanic that merely prevents use while preserving stored units must affect availability/eligibility, not pretend the true Resource capacity became smaller.

### State-stable capacity constraint

Canonical normalization cannot depend on invocation-only LLM/adjudicated context. A `resource.capacity` value used to constrain ResourceState must be derived from the pinned committed/prospective engine-owned state and participating registered mechanics.

Slice D must make this enforceable in selector/fact dependency metadata rather than leaving it prose-only.

## 3. Procedure spent-model semantics remain unchanged

Procedure-local Resources retain stored consumption:

```text
available = max(0, capacity - spent)
```

Changing capacity does not rewrite `spent`. This preserves already-consumed actions/movement/reactions across temporary capacity changes and suspension.

The exact portable procedure-state container remains Step-3 work. Its semantic key is already fixed:

```text
procedure identity + participant + Resource definition -> spent
```

It must have one continuity owner; Slice E will reject duplication between Encounter/procedure state and Continuation/checkpoint payloads.

## 4. Timed recovery cardinality

Initial ResourceState owns at most one active metric delayed recovery obligation.

Therefore `definition.resource.recovery` may contain:

- any number of direct registered boundary recovery rules;
- at most one metric `after` recovery rule.

That metric rule may re-arm the next concrete `recovery_binding` when a repeated recharge requires it. A future proven rule with simultaneous independent timed recoveries may reopen binding cardinality.

The machine schema now enforces this restriction. A focused TDD case first failed under the prior unrestricted recovery array and passed after the schema correction; the full `Validate engine source` workflow then passed.

## 5. Other assurance results

Retained without amendment:

- HP and temporary HP remain Actor intrinsic authority, not generic Resources;
- maximum HP and Bloodied remain derived;
- HP and LifeState remain separate authorities;
- Dying/Stable state-local progress remains sufficient without episode IDs;
- ordinary healing cannot serve as resurrection API;
- character-like/monster lifecycle policy remains independent of Actor kind;
- persistent Asset resources and Actor resources use the same Resource semantics while keeping separate state owners;
- transformation requires explicit bounded definition-dependent state migration rather than generic merge/carry-forward;
- procedure-local state is continuity-critical but not Actor canon;
- exact retries, costs, atomic segments, same-boundary ordering, and portable continuation are correctly owned by Step 3;
- cross-writer conflict/publication semantics remain Step 5.

## 6. Carry-forward findings

### Slice D

Verify/enforce that selectors whose outputs constrain canonical state invariants, beginning with `resource.capacity`, cannot depend on ephemeral invocation-only adjudicated facts.

### Slice E / Step 3

Verify that procedure-local ResourceState has exactly one portable owner across active procedure, Resolution, Continuation, and checkpoint structures.

### Step 6

If a real rules seed proves a persistent Resource requiring preserved hidden surplus above capacity or several simultaneous metric recovery timers, reopen the corresponding narrow contract with that concrete case.

## 7. Final disposition

Recommendation: **KEEP Step 2 closed with the applied Resource amendments.**

Human decision required: **NO**.

Confidence: **HIGH**.
