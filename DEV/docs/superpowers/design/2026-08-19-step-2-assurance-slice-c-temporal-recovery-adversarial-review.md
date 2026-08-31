# Step 2 Retrospective Assurance — Slice C Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — HUMAN ARCHITECTURE DECISION REQUIRED**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed:

- Slice C solution-blind Task Charter;
- Slice C coverage/research synthesis;
- accepted Duration/Temporal Agenda and Recovery B2 designs;
- LifeState lazy death-origin semantics;
- TriggerBinding/Activity boundaries;
- CORE adaptive chronology contract;
- official D&D/SRD cases requiring relative repeated elapsed-time consequences.

## 1. Verdict

The accepted temporal architecture remains sound for:

- one intrinsic lifetime per state owner;
- Resource delayed recovery;
- Stable automatic recovery;
- procedure and semantic boundaries;
- lazy derived Agenda indexing;
- interruptible explicit time advancement;
- no wall-clock/background scheduler.

However, the assurance found one **BLOCKING representational omission** that the previous Step-2 framing did not ask about:

> A live Effect/Condition can have its own intrinsic lifetime and, independently, one or more future elapsed-time rules that must invoke bounded mechanics before that lifetime ends.

The existing single `world.effect.temporal_binding` cannot represent both authorities, and neither TriggerBinding nor Continuation currently owns durable next-due state.

This requires a material Step-2 boundary amendment and therefore a human decision.

## 2. C1 — adaptive chronology correction survives criticism

The critic agrees that Step 2's previous phrase `coordinate freezes when precision is not currently required` is unsafe if interpreted as discarding already-established quantitative passage.

The corrected invariant is:

```text
no wall-clock / no inferred passage
    remains true

explicitly established quantitative elapsed evidence
    must not be discarded merely because no timer is currently active
```

This is not a global clock. Chronology can remain a sparse partial order and may store exact, bounded/approximate, or insufficient temporal evidence.

A later lazy elapsed query must return a truth status justified by persisted chronology rather than manufacture precision. Exact representation and `INDETERMINATE` execution handling belong to later chronology/execution design.

**Critic disposition:** mechanically required clarification; no human choice needed.

## 3. C2 — periodic elapsed mechanics cannot be reduced to existing boundaries universally

The critic attempted to avoid new state by converting all repeated mechanics to existing boundaries.

This works when the rule actually says:

```text
start/end of turn
at dawn
when Long Rest completes
```

It does not faithfully express rules such as:

```text
repeat after/every 24 hours elapsed from this application
```

unless runtime first materializes an owner-relative future metric deadline. Calling that deadline a boundary does not eliminate the state; it merely renames the required concrete obligation.

Therefore a concrete next-due owner is unavoidable for the proven rule class.

## 4. C3 — a long-lived Resolution/Continuation is the wrong owner

Alternative attack:

```text
Effect applied
    -> original Resolution stays suspended for 24h
    -> Continuation wakes later
```

Rejected.

A Resolution is one Activity invocation. Once application commits, the ongoing disease/poison/effect belongs to the world state, not to the historical invocation that created it. Keeping a Resolution alive for every periodic world rule would:

- conflate procedure execution with persistent world mechanics;
- make Effect survival depend on Continuation retention;
- duplicate Effect lifecycle with execution lifecycle;
- make restore/GC rules pathological;
- turn long-term world processes into suspended chat transactions.

The due obligation must therefore be owned by the persistent mechanic, not its creator Resolution.

## 5. C4 — `op.schedule_followup` alone is not an owner

`op.schedule_followup` can express that execution wants a later child Activity, but an operation request is not durable next-due state after the owning Resolution completes.

For a delayed follow-up to survive process/chat loss, some state owner must retain:

```text
what rule is waiting
when/which boundary makes it due
whether it has been cancelled/rearmed/consumed
which world mechanic owns the obligation
```

Putting this into a global queue creates the scheduler authority rejected below. Putting it in the Effect application keeps cancellation and lifetime ownership local.

## 6. C5 — generic global ScheduledJob/TemporalObligation record is too strong

A standalone record such as:

```text
runtime.scheduled_job
    owner_id
    due
    activity_id
```

looks reusable across Effects, Resources, quests, contracts, and world processes.

The critic rejects it for Step 2 because the obligation has no proven independent semantic identity/lifecycle apart from its owning mechanic. It would create:

- a second owner for cancellation and validity;
- orphan cleanup rules;
- generic callback semantics;
- promotion/publication closure across a new record class;
- temptation to schedule arbitrary Activities from arbitrary data;
- a global scheduler/query surface before other domains prove a need.

The Agenda should remain the shared physical/query layer; canonical obligation state stays embedded under the owner that determines whether it still exists.

If a later world process genuinely has independent identity beyond an Effect/Resource/etc., that process may own its own temporal binding under the class-admission rule rather than reusing a universal job entity.

## 7. C6 — fake timer Effect is semantically dishonest

Using an auxiliary Effect whose only purpose is to expire and trigger another Activity reuses existing storage but creates a world record with false domain meaning.

It also introduces accidental Effect semantics:

- target/source/provenance requirements;
- dispel/removal interactions;
- arbitration/Condition lookup contamination;
- support/promotion implications;
- terminal history noise.

This is the same anti-pattern as creating fake Activities only to reach transaction machinery. Rejected.

## 8. C7 — should `world.effect.temporal_binding` simply become a generic list/map?

A tempting alternative is:

```text
world.effect.temporal_bindings:
    lifetime: ...
    trigger.foo: ...
    trigger.bar: ...
```

This is physically compact, but the critic recommends preserving semantic separation:

```text
intrinsic temporal_binding
    -> answers when the Effect itself ends from intrinsic timing

scheduled trigger state
    -> answers when a rule owned by the still-live Effect next becomes due
```

The two have different consequences, cancellation semantics, and Step-3 execution paths. Making them one undifferentiated collection recreates the same conceptual overload that Step 2 removed from duration/concentration/recovery.

They may reuse the **same TemporalBinding value schema** internally without becoming one authority field.

## 9. C8 — recommended owner-local model

The critic recommends the narrowest new ownership surface:

```text
Effect definition
    scheduled trigger declaration(s)
        stable owner-local trigger key
        registered/bounded timing rule
        bounded Activity/Trigger behavior

world.effect application
    temporal_binding
        optional intrinsic Effect-lifetime binding

    scheduled_trigger_state[key]
        optional concrete next-due TemporalBinding
```

Properties:

1. `key` is stable only inside the owning reusable definition; it is not a new global definition/world/runtime ID.
2. A concrete application owns zero/one current binding per declared stateful trigger key.
3. Only trigger declarations explicitly allowed to own temporal state can have entries.
4. Effect terminal transition atomically cancels/removes all still-armed scheduled trigger state.
5. Removing/replacing the declaration through incompatible catalog migration requires migration of active applications; it cannot be silently ignored.
6. The Agenda indexes `(effect_id, trigger_key, due binding)` as a disposable projection.
7. When due, Step 3 owns occurrence identity, child Resolution execution, retry/idempotency, and atomic re-arm/remove/terminate behavior.
8. Trigger execution may roll/branch because it enters normal bounded Activity/Resolution machinery; it is not an automatic state-owner callback.
9. Procedure/semantic rules use native registered boundaries where possible rather than synthesizing metric cadence.
10. No generic arbitrary scheduled callback is introduced.

The exact JSON field name and TriggerBinding schema can be designed mechanically after the ownership decision; the accepted semantic commitment is owner-local stateful scheduled triggers separate from intrinsic lifetime.

## 10. C9 — why stable owner-local trigger keys are necessary

Current TriggerBindings are embedded anonymous values. Anonymous values are sufficient while they only react to immediate Signals/Events.

Persistent next-due state must survive restart and identify which reusable declaration it belongs to. Array position is not stable enough under definition evolution and cannot safely be a semantic key.

Therefore a stateful scheduled trigger declaration requires a stable local machine key.

This does not promote TriggerBinding to a standalone definition. The key has meaning only under `(owning definition ID, trigger key)`.

The same pattern may later be reused for other stateful embedded declarations if proven, but no general embedded-object identity framework is added now.

## 11. C10 — cancellation and re-arm semantics

The state machine remains bounded:

```text
UNARMED
    -> materialize concrete binding when rule creates/arms obligation

ARMED(binding)
    -> due occurrence
        -> Step-3 child Resolution/typed execution
        -> exactly one of:
             REARM(new binding)
             UNARM
             OWNER TERMINAL

OWNER TERMINAL
    -> all scheduled trigger state removed/cancelled atomically
```

Refresh/replacement of the Effect must explicitly decide whether each scheduled trigger is preserved, re-anchored, reset, or replaced according to the reusable definition/reapplication contract. It must not inherit stale bindings by generic object merge.

Exact action vocabulary belongs in the later schema/Step-3 integration and should initially be limited to proven cases.

## 12. C11 — interaction with automatic owner responses

Do not merge scheduled triggers with B2 automatic boundary responses.

```text
automatic owner response
    deterministic typed mutation of that owner's state

scheduled trigger due
    bounded rule invocation that may roll, branch, produce reactions/events,
    and therefore uses Step-3 Resolution
```

For example, `remove one Exhaustion on Long Rest` may remain a deterministic Condition response, while `repeat a Constitution save after 24 hours` is a scheduled trigger.

## 13. C12 — Agenda remains non-authoritative

The new state does not turn Agenda into a scheduler authority.

Agenda rebuild inputs become:

```text
Effect intrinsic lifetime bindings
Effect scheduled-trigger bindings
Resource recovery bindings
LifeState recovery bindings
checkpointable procedure/runtime temporal obligations
```

If Agenda is lost, it is rebuilt from those owners. If owner state is lost without checkpoint/publication, the obligation can be lost; this is exactly why continuity-critical noncanonical state remains a Step-3/5 durability requirement.

## 14. Strongest argument against the recommendation

The strongest objection is YAGNI: full seed coverage is Step 6, and introducing persistent trigger state now increases Effect schema, trigger compilation, migration, Agenda indexing, and Step-3 execution complexity.

The critic does not accept that objection because the rules class is already proven and cannot be represented without either fake Effects, a global scheduler, or long-lived Resolutions. Deferring the *shape* is fine; deferring the *ownership decision* would leave Step 2 falsely closed with a known unrepresentable mechanic.

## 15. Human decision

The material decision is whether to amend the Step-2 temporal/Effect boundary to allow finite owner-local scheduled trigger obligations independent of intrinsic lifetime.

### Recommended choice — A: owner-local stateful scheduled triggers

```text
world.effect owns scheduled trigger due-state keyed by stable embedded trigger key
TemporalBinding value is reused
Agenda remains derived
Step 3 executes/rearms due triggers
```

**Pros:** one owner, deterministic cancellation, no fake entities/jobs, supports proven periodic mechanics, composes with current Agenda/Resolution architecture.

**Cost:** adds a second temporal state family under Effect applications and requires stable local trigger keys plus Step-3 execution/re-arm semantics.

### Alternative B: standalone generic scheduler/job records

**Not recommended.** More generic but introduces duplicate ownership/callback/job lifecycle and broad future coupling.

### Alternative C: fake timer Effects / long-lived Continuations

**Rejected.** Reuses existing records only by assigning them false semantics and creates lifecycle/recovery problems.

### Alternative D: declare periodic elapsed mechanics unsupported until Step 6

**Rejected.** We already know the accepted Step-2 model cannot represent a proven baseline rules class; knowingly preserving that gap would invalidate the assurance objective.

Recommendation confidence: **HIGH**.

Human decision required: **YES**.

What would change the recommendation: evidence that every supported periodic elapsed mechanic can be reduced without loss to an already-materialized procedure/semantic boundary, or a simpler owner-local representation that preserves independent intrinsic lifetime plus next-due trigger state without introducing a second authority.
