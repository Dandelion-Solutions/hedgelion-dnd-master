# Step 2 Retrospective Assurance — Slice A Coverage and Research

Status: **ASSURANCE SYNTHESIS — ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-2-assurance-slice-a-actor-state-task-charter.md`

## 1. Coverage summary

| Requirement family | Coverage | Finding |
|---|---|---|
| HP/temp-HP single authority | FULL | Actor `hp`; generic Resource duplication removed |
| derived maximum HP | FULL | base/adjustment + `health.maximum` selector; resolved max not stored |
| max-HP shrink below current | FULL for HP | prospective health plan normalizes current; lifecycle sees same prospective facts |
| HP versus LifeState separation | FULL | zero HP not universal death; explicit current LifeState authority |
| state-local dying/stable progress | FULL | death saves/binding only in owning state |
| repeated lifecycle episodes | FULL | progress is recreated per entry; transition/event provenance distinguishes episodes |
| revival versus healing | FULL | dead cannot be revived by ordinary healing API; revival is explicit lifecycle mechanic |
| character-like versus monster policy | FULL | registered policy, independent of Actor kind |
| persistent Actor/Asset Resources | FULL | owner-local `current`; capacity derived |
| procedure-local Resources | DEFERRED_OK with minimum | semantic/lifetime owner fixed; exact checkpointable execution shape is Step 3 |
| restricted/noninterchangeable budgets | FULL | distinct Resource definitions |
| Resource capacity shrink/growth | PARTIAL | `spent` semantics are explicit; persistent `current` normalization is not |
| multiple delayed Resource recoveries | PARTIAL / schema mismatch | definition allows several timed rules while state owns one `recovery_binding` |
| boundary recovery ownership | FULL | definition/state owner responds; RestPolicy does not mutate Resource |
| Asset charges versus Actor resources | FULL | same semantics, different lifetime owner/state map |
| transformations and definition-dependent state | DEFERRED_OK but must remain explicit | Step-1 audit requires bounded state migration; Step 3 operation contract must enforce it |
| revision-pinned reads/prospective mutation | FULL minimum | Step 2 establishes pinned state/DAG; Step 3 owns segment commit |
| retry/idempotency | DEFERRED_OK | Step 3 explicitly owns command/segment receipts |
| continuity of procedure-local state | DEFERRED_OK | Step 3 Task Brief explicitly requires checkpointable procedure ResourceState |
| stale/concurrent writes | DEFERRED_OK | pinned views now; conflict/revision publication Steps 3/5 |

## 2. Health and LifeState result

The solution-blind requirements did not expose a missing health/lifecycle owner.
The current split remains coherent:

```text
Actor hp.current / hp.temporary / max components
    -> numeric health authority

resolved health.maximum / bloodied
    -> derived

Actor life_state_id
    -> lifecycle classification authority

life_state_progress
    -> only progress intrinsic to current lifecycle episode
```

Important cross-cases remain representable:

- maximum HP reduction and damage in one prospective view;
- max restoration while dead does not resurrect;
- death-prevention mechanics intercept prospective consequence before final LifeState plan;
- Dying/Stable can coexist with Condition.Unconscious without aliasing;
- direct/monster death avoids unnecessary death-save state;
- current dead-episode origin is recovered from transition chronology rather than a second `dead_since` authority.

No generic injury/wound authority is added without a proven rules need.

## 3. Finding A-F1 — persistent `current` ResourceState needs a capacity-shrink invariant

**Severity: SIGNIFICANT semantic omission, but likely mechanically resolvable.**

For procedure-local `spent`, Step 2 explicitly says consumed state survives a temporary capacity change:

```text
available = max(0, capacity - spent)
```

For persistent Actor/Asset state, the current contract stores `current` but does not state what happens when a derived capacity falls below it.

Three naive choices have different behavior:

### Preserve hidden surplus

```text
stored current = 5
capacity drops 5 -> 3
available = min(current, capacity) = 3
```

This looks non-destructive but breaks ordinary spend semantics: decrementing
`current` from 5 to 4 would leave `available` at 3, so the first spend would not
reduce availability. Avoiding that requires a hidden surplus ledger or special
spend arithmetic, which is a second state model.

### Add a generic capacity-change policy

Per-Resource policies such as `preserve`, `clamp`, `convert`, etc. can express
more cases but create a new normalization subsystem without proven need.

### Normalize `current` to actual capacity

Recommended initial invariant:

```text
persistent current-model ResourceState:
    0 <= current <= resolved capacity
```

When a prospective state change makes resolved capacity lower than stored
`current`, the same prospective transition normalizes `current` down to capacity
before commit.

Capacity growth does **not** grant/restores uses automatically; recovery/grant
semantics do that explicitly.

This makes `current` truly mean remaining units and keeps spend/restore simple.
A mechanic that only temporarily prevents use without destroying stored units
must model **availability/eligibility restriction**, not a lower Resource
capacity. This is analogous to keeping suppression separate from Effect
lifecycle.

If a real seed mechanic later requires capacity reduction with preserved hidden
surplus, it should prove a different storage model rather than overload `current`.

## 4. Finding A-F2 — one ResourceState binding versus multiple timed recovery definitions

**Severity: MODERATE machine-contract mismatch.**

Actor/Asset ResourceState currently owns at most one concrete
`recovery_binding`. That is sufficient for a cooldown or repeated one-at-a-time
timed recharge where firing the current obligation may arm the next one.

However `definition.resource.recovery` is an unrestricted array and can currently
encode several independent metric `after` rules. Such a definition can require
several simultaneously active concrete deadlines that the state shape cannot
represent.

No D&D seed case has proven the need for multiple concurrent timed obligations on
one ResourceState.

Recommended initial restriction:

```text
one Resource definition may have any number of named boundary recovery rules,
but at most one metric-delay recovery rule that can own/re-arm the ResourceState
recovery_binding.
```

If a future mechanic requires genuinely concurrent independent recovery timers,
reopen the binding cardinality with that case rather than adding a list now.

## 5. Procedure-local ResourceState ownership

The physical machine shape is intentionally incomplete in Step 2 but the owner
is not ambiguous:

```text
(active procedure identity, participant, resource definition)
    -> stored spent
```

It is not Actor canon and not owned by one Resolution. It survives child
Activities/reactions/suspension as continuity-critical procedure state.

Step 3 already requires checkpointable active procedure/encounter execution
state and procedure-local ResourceState. Therefore exact serialization/location
is a safe downstream dependency rather than a hidden missing Step-2 authority.

Slice E must verify Step 3 does not accidentally create a second copy in both
Encounter and Continuation.

## 6. Transformation and resource/lifecycle state

Step-1 audit already established that `op.transform_entity` cannot blindly keep
all definition-dependent state. A transformation must declare/validate bounded
state removal/initialization/mapping while preserving only universally valid
instance identity/state.

For Actor state this means a form/definition change may need to update in one
prospective operation:

```text
archetype/definition identity
HP components/current HP according to rule
LifeState when the rule requires it
ResourceState entries granted/invalidated by the new form
Effects whose own rules require change
```

Step 2 correctly does not invent a universal transform merge algorithm. Step 3
must make the operation atomic/typed; Step 6 seed/migration supplies concrete
rules. This deferral is safe because arbitrary state carry-forward is already
forbidden.

## 7. Lifecycle episode identity

No extra `life_episode_id` is required for the accepted D&D model.

Dying progress is destroyed/recreated on state entry, Stable owns its current
binding, and dead-origin queries identify the most recent committed non-dead to
dead transition not ended by revival. Step-3 event/segment identity supplies
causal identity for retry/history.

Adding an episode field now would duplicate transition chronology without a
proven consumer.

## 8. Resource operations under the recommended invariant

For `state_model=current`:

```text
capacity growth:
    current unchanged

capacity shrink below current:
    prospective normalization current := capacity

spend n:
    require current >= n under the same prospective capacity view
    current := current - n

restore_to_capacity:
    current := capacity

restore_amount n:
    current := min(capacity, current + n)
```

For `state_model=spent`:

```text
available := max(0, capacity - spent)
capacity change does not rewrite spent
reset_spent := 0
```

The asymmetry is intentional and is why the two storage models are already
separate machine contracts.

## 9. Counterexamples attempted

### Temporary debuff should block use but preserve charges

Do not model this as reduced capacity if charges must return unchanged. Use
availability/eligibility mechanics. PASS under F1 recommendation.

### Temporary capacity bonus grants two extra uses immediately

Raising capacity alone does not restore units. The granting mechanic must also
perform the appropriate typed Resource restore/grant or use a distinct Resource
when eligibility differs. This avoids capacity calculation secretly mutating
state. PASS.

### Capacity modifier expires while Resource is partially used

If the modifier represented a true maximum, `current` is normalized to the new
maximum in the same prospective segment. Deterministic. PASS.

### Procedure capacity changes from 3 to 1 after two actions spent

`spent=2`, `capacity=1`, `available=0`; restoring capacity to 3 later yields
`available=1`, so previous consumption is not refunded. PASS.

### Asset charge and Actor resource spent in same Activity

Both are independent ResourceState authorities and Step 3 commits both atomically
when the Activity contract requires it. PASS.

### Crash while reaction budget is spent

Procedure ResourceState is continuity-critical and Step 3 must checkpoint the
single procedure owner. No Actor write is required. DEFERRED_OK.

## 10. Research conclusion

The actor-state architecture is substantially stronger than the original manual
framing. The assurance found no missing HP/LifeState authority and no need for a
new Actor entity class, generic lifecycle FSM, wound subsystem, or second
Resource entity.

The two actionable gaps are narrow:

- define/validate persistent-current normalization on true capacity shrink;
- restrict initial Resource timed recovery to one active metric-delay policy per
  ResourceState unless a real future rule proves concurrent bindings.

## 11. Recommendation

**AMEND, do not REOPEN Step 2.**

Proposed amendments follow directly from the accepted `current`/`spent`
storage meanings and single-binding state model. No human product trade-off is
currently required unless the critic finds a concrete mechanic that needs
hidden preserved current above capacity or multiple concurrent timed deadlines.

Confidence: **HIGH** on the ownership model; **MEDIUM-HIGH** on the initial
single-metric-recovery restriction pending adversarial review.
