# Step 2 LifeState Policy, Progress, and Transition Design

Status: **PRELIMINARILY ACCEPTED — WHOLE ARCHITECTURE SUBJECT TO HOLISTIC REVIEW**

Target branch: `feature/mechanical-runtime-hot-state`

Parent design: `DEV/docs/superpowers/design/2026-08-18-step-2-mechanical-state-ownership-design.md`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Purpose and review status

This document records the owner-approved Step 2 design for Actor LifeState, including the minimum D&D lifecycle vocabulary, ruleset policy selection, state-local progress, HP/LifeState transition planning, death saves, stabilization, death, revival eligibility, automatic post-death mechanics, and interaction with Conditions, Effects, temporal obligations, and entity lifetime.

The design is **preliminarily accepted for current architecture sequencing**. It closes the LifeState ownership block sufficiently to proceed to health/effect selectors and later Step 2 schema/catalog alignment. It does not authorize runtime implementation or final machine schema by itself.

The later project-wide architecture pass must re-evaluate this checkpoint together with **all** architecture, structures, logic, ownership rules, schemas, runtime contracts, and inter-module relationships. LifeState is not specially frozen or specially singled out for that review.

## 2. Design goals

The LifeState model must satisfy all of the following:

1. preserve one authoritative current lifecycle classification for a mechanically materialized Actor;
2. avoid deriving death from HP alone;
3. keep HP, LifeState, Conditions, creature type/form, Effect lifecycle, and entity retirement as separate authorities;
4. represent character-like death saves without turning them into generic Resources;
5. support the ordinary D&D monster fast path without materializing unnecessary death-save state;
6. support important NPCs that use character-like death rules without changing Actor kind;
7. support direct death, massive-damage death, healing, stabilization, revival, and transformation through prospective atomic transitions;
8. avoid a generic programmable finite-state-machine language;
9. avoid resurrection timers or revival-window records on every dead Actor;
10. materialize future temporal work only when a real automatic future consequence exists;
11. preserve enough causal/temporal provenance to evaluate a revival rule lazily if that rule later becomes relevant;
12. keep the common single-player/HOT path cheap and indexed;
13. leave exact Resolution/event ordering, idempotent receipts, and cross-scene chronology to their roadmap owners instead of inventing LifeState-specific substitutes.

## 3. Core ownership model

### PRELIMINARILY ACCEPTED

The minimum authority split is:

```text
world.actor
    hp
        -> numeric health authority

    life_state_id
        -> current Actor lifecycle classification

    optional state-local lifecycle progress
        -> only progress intrinsically required by current LifeState

LifeStatePolicy
    -> registered ruleset policy for baseline lifecycle semantics

LifeStateResolver
    -> validates and plans transitions

LifeStateTransitionPlan
    -> transient prospective change set

Step-3 Resolution
    -> owns exact atomic commit/event/receipt ordering
```

There is no separate `world.lifecycle` entity and no second persistent lifecycle authority.

## 4. LifeState is not entity lifecycle

A `world.actor` continuing to exist in canon is independent of whether that Actor is alive or dead.

```text
entity existence / retirement
    !=
Actor LifeState
```

Entering `life.dead` does **not** by itself:

- delete the Actor;
- retire the Actor;
- create a replacement Actor identity;
- convert the Actor into a mandatory corpse Asset;
- remove inventory ownership;
- remove all Effects;
- destroy chronology/provenance.

A dead body remains the same Actor identity for corpse interaction, investigation, transport, story continuity, and possible revival.

A later revival normally performs:

```text
same actor ID
life.dead -> life.active
```

not `old actor -> retired` plus `new actor -> created`.

Entity retirement is a separate lifecycle of the world record and must be invoked only when the fiction/persistence rules genuinely say the Actor record no longer participates as an entity.

## 5. LifeState is not Condition, consciousness, or action availability

LifeState answers only the current lifecycle-classification question.

It does not answer all questions about what the Actor can do.

Examples:

```text
life.active + Condition.Paralyzed
life.active + Condition.Unconscious
life.dying  + Condition.Unconscious
life.stable + Condition.Unconscious
```

are all structurally possible when the rules produce them.

Therefore the following must not be persisted as aliases of LifeState:

```text
is_conscious
can_act
is_incapacitated
is_unconscious
```

Those are derived from LifeState plus applicable Conditions/Effects/rules.

## 6. LifeState is not creature type or form

Creature type/form and LifeState are orthogonal.

A functioning undead creature may be:

```text
creature_type = undead
life_state     = active
```

A dead humanoid may be:

```text
creature_type = humanoid
life_state     = dead
```

A transformation/revival Activity may atomically change both form/type and LifeState when a rule genuinely requires both, but neither is derived from the other.

This is important for vampire/lich/undead mechanics: `undead` is not a synonym for `dead`.

## 7. Minimum D&D LifeState vocabulary

### PRELIMINARILY ACCEPTED

The initial D&D baseline contains exactly four lifecycle states:

```text
life.active
life.dying
life.stable
life.dead
```

These names are the accepted conceptual vocabulary. Exact catalog namespace spelling may be aligned during schema/catalog work, but their semantics and cardinality are fixed for the current checkpoint.

### 7.1 `life.active`

The Actor is in the ordinary non-dying, non-stable, non-dead lifecycle state.

`active` does **not** mean the Actor can currently take actions. Conditions and other mechanics may prevent action.

### 7.2 `life.dying`

The Actor is at the ruleset's death-save lifecycle stage and owns the current dying episode's death-save progress.

### 7.3 `life.stable`

The Actor is at 0 HP but no longer making death saves under the normal D&D character-like lifecycle. It may remain Unconscious and may own a real automatic recovery temporal obligation.

### 7.4 `life.dead`

The Actor is dead under lifecycle rules. Ordinary healing cannot independently restore the Actor to active LifeState. Explicit revival/transformation mechanics may do so.

### 7.5 States intentionally not introduced

The initial contract does not add:

```text
life.destroyed
life.unconscious
life.incapacitated
life.petrified
life.bloodied
life.undead
life.retired
```

Those concepts belong to other existing authorities or are not proven to need a universal LifeState.

A future additional LifeState requires a demonstrated rules need and catalog/architecture extension; the LLM may not invent arbitrary executable LifeState IDs during play.

## 8. LifeStatePolicy

### PRELIMINARILY ACCEPTED

LifeState transition semantics are selected through a small registered policy capability rather than through a user-authored state-machine graph.

The initial D&D baseline requires at least:

```text
life_policy.dnd2024.character_like
life_policy.dnd2024.monster_default
```

Exact machine registry placement is deferred to catalog alignment.

### 8.1 Character-like policy

The character-like policy supports:

- transition from 0 HP into dying when no instant/direct-death rule applies;
- death-save progress;
- stabilization;
- damage while dying/stable;
- natural-20 recovery behavior;
- healing out of dying/stable;
- maximum-HP-zero/direct-death rules;
- validated revival from dead.

### 8.2 Monster-default policy

The ordinary monster policy takes the cheaper default path in which reaching 0 HP normally becomes dead rather than materializing a dying/death-save episode.

This keeps ordinary enemy death cheap.

### 8.3 Important NPC override

Actor role is not policy authority.

HDM must not hard-code:

```text
player character -> character_like
NPC              -> monster_default
```

An important NPC/monster may use character-like rules when the DM/rules require it without becoming a different Actor kind.

Policy resolution is conceptually:

```text
explicit Actor lifecycle-policy override, if materially present
    -> archetype/definition lifecycle policy, if declared
    -> selected ruleset default
```

The exact storage/reference location is deferred to schema alignment. Ordinary actors must not receive redundant override fields when the inherited/default policy is sufficient.

## 9. Why there is no generic FSM definition

The engine does not introduce a data model such as:

```text
states:
transitions:
guards:
actions:
callbacks:
expressions:
```

for arbitrary LifeState programs.

Such a model would duplicate Activity, Rule Element, Trigger Binding, Effect, and Step-3 Resolution responsibilities.

LifeStatePolicy is a registered capability with typed semantics. New special character abilities do not generate new policy objects simply because they can change a lethal outcome.

## 10. Special abilities are not policy variants

A mechanic such as "when you would drop to 0 HP, remain at 1 HP instead" must not create a policy ID equivalent to:

```text
character_like_plus_special_feature_X
```

Instead, the feature participates in the ordinary prospective Resolution/rules path before the final lifecycle plan is committed.

Conceptually:

```text
damage resolves prospectively
    -> candidate HP/lifecycle consequence
    -> applicable registered prevention/interception mechanics
    -> final prospective health facts
    -> LifeStateResolver
    -> LifeStateTransitionPlan
```

Exact pending Signals/reaction ordering and commitment points belong to Step 3.

This prevents combinatorial LifeStatePolicy explosion.

## 11. Actor state and state-local progress

### PRELIMINARILY ACCEPTED

The conceptual Actor structure is:

```text
Actor
    hp
    life_state_id
    optional life_state_progress
```

The exact JSON field name for state-local progress is deferred, but its ownership and conditionality are accepted.

`life_state_progress` is a typed tagged/conditional shape. It is not arbitrary JSON and must be valid for the Actor's current LifeState.

### 11.1 Active

```text
life_state_id = life.active
life_state_progress = absent
```

### 11.2 Dying

```text
life_state_id = life.dying
life_state_progress:
    death_saves:
        successes: 0..2
        failures:  0..2
```

### 11.3 Stable

Conceptually:

```text
life_state_id = life.stable
life_state_progress:
    recovery_binding: <concrete TemporalBinding>
```

The exact binding shape reuses the common temporal contract rather than defining a Stable-specific scheduler format.

### 11.4 Dead

```text
life_state_id = life.dead
life_state_progress = absent
```

There is no mandatory corpse countdown, resurrection window, or `dead_since` counter in Actor state.

## 12. State/progress consistency invariants

The runtime/schema alignment must enforce the equivalent of:

```text
life.active -> no dying/stable progress
life.dying  -> valid death-save progress
life.stable -> valid stable-recovery binding when the rules require automatic recovery
life.dead   -> no dying/stable progress
```

A mismatched state/progress pair is an integrity failure, not permission to guess.

Examples of invalid canonical states include:

```text
life.active + death_saves
life.dead   + death_saves
life.dying  + stable_recovery_binding
life.stable + stale dying progress
```

## 13. Death-save progress is not a Resource

### PRELIMINARILY ACCEPTED

Death saves are lifecycle progress for the current dying episode.

They are not a `definition.resource` because they are not:

- spendable;
- rest-recoverable Resource capacity;
- transferable;
- a generic pool available outside dying;
- an independent mutable mechanic with its own resource identity.

This keeps Resource semantics narrow and prevents recovery/resource selectors from accidentally applying to death saves.

## 14. Death-save value invariant

Canonical death-save counts are limited to:

```text
successes = 0..2
failures  = 0..2
```

A third success/failure is not stored and then interpreted later.

Instead:

```text
dying + successes=2 + success
    -> prospective third success
    -> life.stable
    -> dying progress removed
    -> stable progress materialized
```

and:

```text
dying + failures=2 + failure
    -> prospective third failure
    -> life.dead
    -> dying progress removed
```

Therefore canonical states such as:

```text
life.dying + successes=3
life.dying + failures=3
```

are structurally invalid.

This eliminates an otherwise ambiguous intermediate authority.

## 15. Stable automatic recovery

### PRELIMINARILY ACCEPTED

The D&D character-like Stable state has one important exception to the otherwise strongly lazy lifecycle model: untreated Stable recovery is a real automatic future mutation.

When the rules create Stable:

```text
dying -> stable
    -> authoritative roll for 1d4-hour recovery delay
    -> materialize one concrete TemporalBinding
    -> index it in the common Temporal Agenda
```

This is justified because reaching that deadline changes world state even if no player asks a question at that moment.

At the due boundary:

```text
life.stable
    -> HP becomes 1
    -> life.active
    -> stable binding removed
    -> lifecycle-origin Unconscious removed if no longer justified
```

No `StableRecoveryScheduler` exists.

### 15.1 Early healing

If the Actor receives valid healing before the stable-recovery boundary:

```text
stable -> active
```

and the stable binding is cancelled as part of the same prospective transition.

### 15.2 Damage while Stable

Damage at 0 HP invalidates stability and applies the appropriate dying/death consequences in one prospective plan.

The runtime must not commit a transient `stable -> dying` state and only later add the failure caused by the same damage.

## 16. Dead is strongly lazy

### PRELIMINARILY ACCEPTED

Entering `life.dead` creates **no generic resurrection machinery**.

The common path is:

```text
enter life.dead
    -> no resurrection timer
    -> no list of revival windows
    -> no scan for resurrection spells
    -> no scan for priests/witches/NPC services
    -> no scan of the campaign for story opportunities
    -> no Temporal Agenda entry merely because revival might be possible
```

This is a core HDM lazy-loading requirement.

A dead incidental enemy therefore remains cheap.

## 17. Revival windows belong to the revival mechanic

A temporal eligibility rule such as:

```text
may target a creature dead no longer than N minutes/days
```

belongs to the spell/Activity/feature/service/other mechanic that performs revival.

It does not become a timer owned by the corpse.

Conceptually:

```text
resolve_revival(mechanic, target)
    -> target is currently life.dead?
    -> resolve all non-temporal mechanic prerequisites
    -> if mechanic requires time-since-death:
           lazily resolve provenance of current dead episode
           evaluate mechanic-owned temporal constraint
    -> if eligible:
           produce revival transition plan
```

A mechanic with no death-age restriction never needs to hydrate death timing at all.

## 18. Sources of revival capability are ordinary HDM content/mechanics

No global `ResurrectionSystem` enumerates every possible way a dead Actor could return.

A currently relevant revival possibility may arise from ordinary existing sources such as:

```text
Actor spell/activity
Feature
Asset/potion
Effect
known NPC service
location/world service
quest/contract/story permission
creature-specific mechanic
ruleset-defined Activity
```

Only when such a mechanic becomes operationally relevant does the runtime hydrate and validate its requirements.

The engine must not link every dead Actor to every potential resurrection source in the world.

## 19. Lazy current-death provenance

### PRELIMINARILY ACCEPTED

There is no mandatory `dead_since` counter/timestamp in Actor state.

However, while an Actor remains in the current dead episode, the start of that episode must remain **mechanically recoverable** so a later mechanic can ask how long the Actor has been dead.

Conceptually the relevant origin is:

```text
the most recent committed non-dead -> dead lifecycle transition
that has not subsequently been ended by revival/other exit from dead
```

Runtime may resolve that origin lazily from HOT transition context, retained event provenance, checkpoint metadata, chronology, or another Step-3/Step-5-approved durable representation.

### 19.1 Snapshot/compaction invariant

Snapshot-first recovery must not make the current dead episode's origin irretrievable merely because old events are compacted.

This does **not** require a running timer or countdown in Actor state.

It requires only that the durable recovery model retain enough provenance/anchor information for the current dead episode to be reconstructed when a later rule genuinely asks for it.

The exact durable representation belongs to Step 3/Step 5.

### 19.2 Insufficient temporal precision

If HDM legitimately did not preserve enough metric precision to decide a newly relevant historical time constraint exactly, runtime must not invent a timestamp.

It produces a typed adjudication/insufficient-chronology case for the owning Resolution path.

## 20. Repeated death episodes

Death provenance is episode-local.

Example:

```text
dead episode A
    -> revival
    -> active
    -> later death
    -> dead episode B
```

A revival-window query for the current state uses episode B's origin, not the earlier death.

Historical episodes remain ordinary event/story history; Actor state needs no accumulating array of death timestamps.

## 21. Automatic post-death mechanics are opt-in rules

A mechanic such as:

> after death, rise as a vampire at the next dawn

is categorically different from a passive revival window.

Something must happen automatically at a future boundary, so an **already active/known indexed mechanic** may respond to entering dead and materialize one future obligation using existing Effect/Trigger/Temporal infrastructure.

Conceptually:

```text
Actor enters life.dead
    -> local interested-mechanic index
    -> ordinary goblin: zero listeners -> done
    -> vampire/curse mechanic: relevant listener found
         -> create/update ordinary Effect/Trigger temporal obligation
         -> Temporal Agenda indexes next dawn/deadline
```

No campaign-wide search occurs.

## 22. Automatic post-death transformation example

A pending vampire rule may be represented conceptually as:

```text
Effect / Feature trigger
    listens to lifecycle transition into dead
    creates semantic obligation: next dawn
```

At dawn its Activity may prospectively perform:

```text
creature type/form -> vampire/undead form
life.dead          -> life.active
HP                 -> mechanic-defined value
other typed Effects/Conditions -> as rules require
```

This is one atomic transformation Resolution, not a hidden timer inside LifeState.

If ordinary revival occurs before dawn, the transformation mechanic's own rule determines whether the pending obligation is cancelled, becomes inapplicable, or remains. LifeState does not invent a universal answer.

## 23. LifeStateResolver responsibilities

### PRELIMINARILY ACCEPTED

LifeStateResolver is a typed domain resolver, not a persistence writer and not a callback engine.

Conceptual entry points include:

```text
resolve_after_hp_change(...)
resolve_death_save(...)
resolve_stabilization(...)
resolve_state_boundary(...)
resolve_direct_death(...)
resolve_revival(...)
```

Exact function names are implementation details; the architectural requirement is typed inputs rather than one arbitrary `context: JSON` bag.

The common reasoning core consumes:

```text
current Actor health/lifecycle state
+ resolved LifeStatePolicy
+ prospective HP / maximum-HP facts
+ typed cause/provenance
+ applicable already-resolved rule facts
```

and returns a prospective `LifeStateTransitionPlan`.

The resolver does not commit durable state itself.

## 24. LifeStateTransitionPlan

### PRELIMINARILY ACCEPTED

A transition plan is a transient/protocol value, not a world entity.

Conceptually it contains enough typed information for Step-3 Resolution to atomically commit the lifecycle change:

```text
LifeStateTransitionPlan
    actor_id

    from_state
    to_state

    progress_before
    progress_after

    HP companion delta(s), if required
    Effect/Condition lifecycle delta(s), if required
    temporal binding create/cancel delta(s), if required

    typed transition cause/provenance
```

Exact field names, event IDs, receipt IDs, and serialization belong to Step 3/schema alignment.

## 25. Prospective planning before mutation

Lifecycle resolution must use prospective state.

Example:

```text
current HP = 7
damage = 12
    -> prospective HP = 0
    -> policy/rules resolve dying or death
    -> construct full transition plan
    -> validate companion deltas
    -> Step 3 commits atomically
```

Runtime must not persist HP first and discover lifecycle consequences afterward.

This is the same discover/plan-before-commit principle already used for Effect support closure, boundary resolution, and overlapping prospective state.

## 26. HP and LifeState atomicity

For a normal character-like zero-HP transition, one committed segment must be equivalent to:

```text
hp.current = 0
life_state  = life.dying
death_saves = 0 successes / 0 failures
create lifecycle-origin Unconscious Condition application
```

There must be no durable intermediate state equivalent to:

```text
hp.current = 0
life_state = life.active
```

for that same resolved outcome.

Likewise direct death, stabilization, healing out of dying, and revival commit all required companion lifecycle changes atomically at the Step-3 mutation boundary.

## 27. Death normalization

### PRELIMINARILY ACCEPTED

A transition to `life.dead` may occur for reasons other than ordinary damage at 0 HP.

Therefore every resolved transition into dead normalizes current HP consistently:

```text
to_state = life.dead
    -> hp.current = 0
```

Resolved maximum HP is not erased merely because current HP becomes zero.

`life.dead`, not the numeric `0`, is the authority that blocks ordinary healing from independently returning the Actor to an active lifecycle.

## 28. Maximum HP changes

Maximum HP is resolved from Actor/build/archetype/Effects according to the accepted HP model.

A rule that causes resolved maximum HP to reach zero may produce death through LifeStateResolver even when no ordinary damage operation occurred.

Crucially:

```text
Effect reduces max HP to 0
    -> life.dead

Effect later ends
    -> max HP becomes positive again
    -> Actor remains life.dead
```

Restoration of numeric capacity does not resurrect a stored lifecycle state.

An explicit valid revival mechanic is still required.

## 29. Ordinary healing and dead Actors

Ordinary healing may transition:

```text
life.dying  -> life.active
life.stable -> life.active
```

when it actually raises current HP above zero under the rules.

Ordinary healing applied to:

```text
life.dead
```

is rejected/ineffective unless the mechanic is explicitly a revival/transformation mechanic authorized to leave dead.

This prevents `hp.current = positive` from becoming an accidental second resurrection API.

## 30. Temporary HP

Temporary HP remain part of Actor HP authority but do not themselves heal or change LifeState.

Therefore:

```text
life.dying  + gain temporary HP -> still life.dying
life.stable + gain temporary HP -> still life.stable
```

No universal death cleanup rule clears temporary HP merely because LifeState becomes dead unless the selected ruleset/mechanic explicitly requires such a change.

## 31. Lifecycle-origin Unconscious Condition

### PRELIMINARILY ACCEPTED

For the normal character-like zero-HP path, Unconscious remains an ordinary Condition application represented through Effect machinery.

The transition creates a source-local application with provenance tying it to the lifecycle/zero-HP episode.

Conceptually:

```text
life.active -> life.dying
    -> create Unconscious application U_lifecycle
```

When:

```text
life.dying -> life.stable
```

that application remains because Stable is still unconscious under the ordinary rule.

When valid healing/recovery produces:

```text
life.dying/life.stable -> life.active with HP > 0
```

only `U_lifecycle` is removed.

If an independent magical sleep application also grants Unconscious, that other application remains.

This relies on the accepted source-local Condition/Effect application model and avoids a global `remove condition by name` bug.

## 32. Death does not purge all Effects

### PRELIMINARILY ACCEPTED

Entering dead does not call a universal Effect cleanup loop.

Existing Effects are handled according to their own lifecycle/availability rules:

```text
Effect explicitly ends on death
    -> terminates

Concentration root
    -> terminates on death according to D&D rules
    -> accepted support forest expires descendants

curse/other still-running Effect
    -> may remain nonterminal
    -> may become unavailable while target is dead
    -> may become applicable again after revival if still within its lifetime
```

The runtime should use local interested-mechanic indexes rather than scanning all campaign Effects.

This also preserves the already accepted distinction:

```text
Effect lifecycle
    != Effect suppression/availability
    != Effect arbitration
```

## 33. Death-transition interested mechanics

A lifecycle transition may expose a typed transition fact/signal to the existing Trigger/Activity layer.

Step 2 requires only that runtime can index mechanics interested in transitions such as entering dead.

It does not fix the final Step-3 signal/event ID vocabulary yet.

The cost model is:

```text
transition occurs
    -> query local lifecycle-listener index
    -> evaluate only matching active mechanics
```

not:

```text
scan all spells
scan all Features
scan all NPCs
scan all campaign content
```

## 34. Death saves and procedure boundaries

A dying Actor does not run a background timer.

The D&D character-like rule is procedure-boundary driven:

```text
life.dying
+ relevant owner turn-start boundary
    -> mandatory Death Save Activity/Resolution
```

The existing procedure/boundary index infrastructure should discover this obligation.

There is no `DeathSaveScheduler`.

## 35. Procedure-closure forward dependency

Step 3 must define how a procedure/encounter can close when a participant remains mechanically unresolved in `life.dying`.

It may not silently discard future mandatory death-save procedure behavior.

The final execution design must ensure one of the following kinds of outcomes is explicit:

```text
Actor healed/stabilized/dead before closure
or
mandatory lifecycle procedure transferred/continued in an appropriate context
```

Step 2 does not invent a second encounter/lifecycle procedure engine to solve this.

## 36. Baseline transition contract

The accepted conceptual D&D transition matrix is:

| Current state | Stimulus / resolved fact | Prospective result |
|---|---|---|
| `active` | HP remains above zero | `active` |
| `active` | character-like reaches 0 HP, no instant/direct death | `dying`, death saves `0/0` |
| `active` | monster-default reaches 0 HP | `dead` |
| `active` | massive/direct/max-HP death | `dead` |
| `dying` | ordinary death-save success below threshold | increment successes |
| `dying` | third success | `stable`, remove dying progress, create stable recovery binding |
| `dying` | ordinary death-save failure below threshold | increment failures |
| `dying` | third failure | `dead`, remove dying progress |
| `dying` | natural-20 recovery result | HP `1`, `active`, remove dying progress/lifecycle Unconscious |
| `dying` | valid healing to HP > 0 | `active`, remove dying progress/lifecycle Unconscious |
| `dying` | damage at 0 HP | apply appropriate failure(s), possibly `dead` in same plan |
| `stable` | valid healing to HP > 0 | `active`, cancel stable binding, remove lifecycle Unconscious |
| `stable` | stable recovery boundary due | HP `1`, `active`, remove stable progress/lifecycle Unconscious |
| `stable` | damage at 0 HP | re-enter dying and apply appropriate failure(s), or become dead, atomically |
| any nondead | resolved maximum HP reaches zero | `dead` |
| any nondead | authorized direct-death result | `dead` |
| `dead` | ordinary healing | rejected/ineffective |
| `dead` | validated revival/transformation | mechanic-defined HP plus normally `active` and any declared form/state consequences |

Exact D&D formula details remain ruleset data/runtime behavior; the table fixes ownership and transition shape.

## 37. Stable damage atomicity

A Stable Actor taking damage at 0 HP is a useful adversarial case.

Bad implementation:

```text
commit stable -> dying
commit later: failure += 1/2
commit later: maybe dead
```

Required model:

```text
current = stable
incoming damage context
    -> cancel stable binding prospectively
    -> initialize dying progress prospectively
    -> apply damage-at-zero failure consequence
    -> if threshold reached, normalize directly to dead
    -> commit one validated transition segment
```

No mechanically meaningful intermediate state leaks into canon.

## 38. Retry and idempotency

LifeState progress itself is not an idempotency mechanism.

If one death-save operation is retried, it must not increment progress twice merely because the current state still accepts a death-save result.

Step 3 therefore must bind transition application to operation/Resolution/receipt identity.

LifeStateResolver remains deterministic for a given authoritative input and does not maintain its own retry ledger.

## 39. Same-boundary interactions

Examples include:

- lethal damage and an Effect expiry at the same boundary;
- death and Resource recovery at the same boundary;
- revival and an automatic vampire transformation at dawn;
- maximum-HP modifier expiry and healing in one Resolution closure.

LifeState does not define a hidden global SQL/list order for these cases.

It participates in the common prospective boundary/Resolution closure, while Step 3 defines exact causal/simultaneity ordering and atomic receipts.

## 40. Derived HOT queries

The following kinds of values are derived, not independent writable Actor authorities:

```text
is_alive
is_dead
is_dying
is_stable
needs_death_save
can_receive_ordinary_healing
can_act
```

Some queries use only LifeState; others require Conditions, Effects, or policy context.

For example, `can_act` cannot be defined from `life.active` alone because an active Actor may be Paralyzed or Unconscious.

HOT/SQLite may cache/index these queries when useful, but the caches are disposable.

## 41. Common-path performance

The intended cost profile is deliberately asymmetric.

### 41.1 Active Actor above zero HP

```text
HP/prospective facts
-> policy fast path
-> no lifecycle state change
```

Near-constant cost.

### 41.2 Ordinary monster reaches zero HP

```text
monster_default
-> dead
-> query local lifecycle listeners
-> usually zero listeners
-> done
```

No death-save state and no resurrection scheduling.

### 41.3 Character-like dying Actor

Only the affected Actor owns a tiny `0..2 / 0..2` progress object and participates in the relevant turn-start boundary index.

### 41.4 Stable Actor

Only the actually Stable Actor owns one real automatic temporal binding.

### 41.5 Dead Actor

No time work is materialized unless an already-active mechanic requires a future automatic consequence. Revival-window calculations remain query-time/lazy.

## 42. Hydration and progressive materialization

An incidental Actor without mechanically materialized HP does not need speculative LifeState mechanics.

When HP becomes materially required, the accepted Actor contract materializes HP and LifeState atomically.

Policy resolution must be sufficient at that point to establish a valid initial lifecycle state; runtime may hydrate the minimum archetype/ruleset facts necessary to do so.

HDM must not generate death-save counters, resurrection capabilities, or post-death schedules merely because the Actor might someday need them.

## 43. Persistence and recovery

Canonical recovery must restore enough information to reconstruct the current lifecycle authority:

```text
hp
life_state_id
current state-local progress, if any
```

Stable recovery binding is authoritative state-local temporal progress and therefore must survive a durable checkpoint when the Stable Actor is durable.

For dead Actors, no timer is required, but the current dead episode's transition origin must remain recoverable according to the lazy-provenance invariant in Section 19.

SQLite/HOT-derived flags and listener indexes are rebuilt.

## 44. Validation rules for later schema alignment

The later machine schema/catalog pass should enforce equivalent constraints to:

```text
HP materialized => LifeState materialized

life.active => no dying/stable progress
life.dying  => death-save progress required and counts 0..2
life.stable => applicable stable recovery binding required for the selected policy
life.dead   => no dying/stable progress

transition to dead => hp.current normalized to 0

ordinary healing cannot independently produce dead -> active
```

Exact JSON Schema conditionals and machine property names remain deferred until the ownership map is fully closed.

## 45. Policy validation

LifeState policy references must resolve to registered engine/ruleset capabilities.

The LLM may select an allowed policy/override when fiction/rules require it but may not invent executable policy IDs or arbitrary transition code.

Unknown/unavailable policy at a mechanically required lifecycle decision is a validation/hydration/catalog-gap problem, not permission to assume `0 HP -> dead`.

## 46. Error handling

Hard/integrity errors include:

- impossible state/progress combinations;
- missing required stable binding for a materialized stable state under a policy that requires automatic recovery;
- transition request incompatible with the current state and selected policy;
- dead Actor receiving an ordinary healing mutation that would make HP positive without revival authority;
- a durable current-death episode whose required provenance has been irretrievably discarded when a mechanic now needs it.

Resolvable/adjudication cases include:

- a newly relevant revival mechanic requires historical metric precision that was legitimately never established;
- a registered rules mechanic cannot determine same-boundary causal order without Step-3 adjudication;
- policy data/definition needs bounded hydration before a transition can be resolved.

## 47. Rejected alternatives

### 47.1 Derive LifeState entirely from HP/death-save counters/Conditions

Rejected because `0 HP` is ruleset- and Actor-policy-dependent, direct death may occur independently of ordinary HP damage, and later restoration of maximum HP must not automatically resurrect a dead Actor.

### 47.2 Represent Dying/Stable/Dead as Conditions

Rejected because LifeState is mutually exclusive lifecycle authority while Conditions are independently applicable named mechanics with source-local multiplicity.

Unconscious remains a Condition.

### 47.3 Store Death Saves as Resources

Rejected because they are state-local progress without resource capacity/spending/recovery semantics.

### 47.4 Generic programmable lifecycle FSM

Rejected because it duplicates the rule engine and creates arbitrary guards/callbacks/actions that existing Activity/Rule Element/Trigger machinery already owns.

### 47.5 One policy variant per special ability

Rejected because it creates combinatorial policy explosion. Features/Effects intercept prospective outcomes through normal rules machinery instead.

### 47.6 Persistent `dead_since` countdown/timer on every corpse

Rejected because most dead Actors will never need revival-age computation and no automatic state mutation happens merely when a revival window closes.

### 47.7 Register every possible revival window in Temporal Agenda

Rejected because passive eligibility expiration is not due work. Only automatic future consequences are Agenda obligations.

### 47.8 Campaign-wide search on death for resurrection possibilities

Rejected because it violates HDM lazy loading and scales with campaign content instead of affected mechanics.

### 47.9 Purge all Effects on death

Rejected because Effect lifecycle is rule-specific; some Effects end on death, some become unavailable, and some remain valid through later revival.

### 47.10 Retire/delete Actor on death

Rejected because death is reversible and corpse/world identity must remain stable.

## 48. Critical-pass cases and corrections

The design was challenged against the following adversarial cases.

### 48.1 Policy explosion

**Risk:** every feature that prevents/alters death becomes a policy variant.

**Correction:** policy owns only baseline lifecycle behavior; feature-specific interception stays in normal prospective rules/Step-3 execution.

### 48.2 Direct death at positive HP

**Risk:** an HP-only FSM cannot represent death from a direct rule.

**Correction:** typed direct-death resolution exists; any transition into dead normalizes current HP to zero.

### 48.3 Temporary maximum-HP restoration accidentally revives

**Risk:** if dead is derived from HP/max HP, ending a max-HP-reduction Effect could resurrect the Actor.

**Correction:** LifeState is stored authority and remains dead until explicit revival.

### 48.4 Stable Actor takes critical/damaging hit

**Risk:** sequential writes expose invalid intermediate stable/dying/failure states.

**Correction:** cancel stable binding, initialize dying progress, apply failure consequence, and resolve any resulting death in one prospective plan.

### 48.5 Third Death Save stored as progress

**Risk:** `dying + 3 successes/failures` becomes a second representation of Stable/Dead.

**Correction:** counts are limited to 0..2; threshold crossing atomically changes LifeState.

### 48.6 Retry duplicates a Death Save

**Risk:** one operation increments the counter twice after retry/resume.

**Correction:** Step 3 operation/receipt identity provides idempotency; progress is not a retry ledger.

### 48.7 Stable recovery conflicts with lazy architecture

**Risk:** any automatic stable timer appears to violate no-background-work goals.

**Correction:** it is retained because the rule has a real future mutation; only actually Stable Actors receive one binding, using the common Agenda.

### 48.8 Revival age after snapshot/event compaction

**Risk:** lazy time evaluation becomes impossible if the death origin is discarded.

**Correction:** no timer is stored, but the current dead episode's origin remains mechanically recoverable across snapshot compaction.

### 48.9 Old death has insufficient exact chronology

**Risk:** runtime fabricates a timestamp to answer a newly relevant revival rule.

**Correction:** exact time is never invented; insufficient chronology becomes typed adjudication.

### 48.10 Automatic vampire/undead return

**Risk:** every death starts generic resurrection scheduling.

**Correction:** only an already-active/known indexed mechanic interested in entering dead materializes a future Effect/Trigger obligation.

### 48.11 Death versus retirement

**Risk:** death destroys Actor identity and makes revival/corpse interaction awkward.

**Correction:** dead is Actor LifeState; retirement is separate entity lifecycle.

### 48.12 Monster with character-like death saves

**Risk:** Actor kind/role hard-codes lifecycle behavior.

**Correction:** policy can be overridden/inherited independently of player/NPC role.

### 48.13 Undead meaning dead

**Risk:** creature type and lifecycle are conflated.

**Correction:** functioning undead are normally `life.active`; type/form and LifeState remain orthogonal.

### 48.14 Death and Effect cleanup

**Risk:** a global purge loses ongoing curses/conditions or duplicates Effect ownership.

**Correction:** death exposes typed lifecycle consequences only to locally indexed interested mechanics; Effect lifecycle remains Effect-owned.

### 48.15 Same-boundary revival versus automatic transformation

**Risk:** SQLite/list order determines whether the Actor is revived normally or transformed.

**Correction:** both participate in one prospective Step-3 same-boundary closure; LifeState does not define a second ordering engine.

No blocker in this critical pass requires a fifth baseline LifeState, a generic FSM, a separate lifecycle entity, a DeathSave Resource, a corpse scheduler, or mandatory resurrection timers.

## 49. Focused examples for later validation

The Step 2 focused-case pass should include at least:

### 49.1 Ordinary goblin

```text
monster_default
HP 4 -> 0
=> dead, HP 0
=> no dying progress
=> no revival timer
=> local death-listener index normally empty
```

### 49.2 Important NPC using character-like policy

```text
NPC role
policy override = character_like
HP -> 0
=> dying 0/0 + lifecycle Unconscious
```

### 49.3 PC reaches third Death Save success

```text
dying 2 successes / 1 failure
success
=> stable
=> no death-save count of 3 stored
=> create 1d4-hour stable binding
```

### 49.4 Stable Actor healed

```text
stable, recovery deadline pending
healing raises HP above zero
=> active
=> cancel stable binding
=> remove lifecycle-origin Unconscious only
```

### 49.5 Stable Actor takes critical damage

```text
stable at 0 HP
critical damage-at-zero consequence
=> initialize dying progress
=> apply appropriate failures immediately
=> maybe dead in same plan
```

### 49.6 Maximum HP reduced to zero

```text
active HP > 0
Effect changes resolved max HP -> 0
=> dead + current HP normalized to 0
Effect later ends
=> max HP positive, still dead
```

### 49.7 Ordinary healing of dead Actor

```text
dead
ordinary healing
=> rejected/ineffective
```

### 49.8 Lazy Revivify-like attempt

```text
dead Actor has no resurrection timer
player actually invokes revival mechanic
=> hydrate mechanic
=> lazily resolve current death origin only because mechanic needs it
=> compare mechanic-owned window
=> eligible/ineligible/adjudication
```

### 49.9 Story witch with no time limit

```text
dead Actor
story/service Activity becomes available
mechanic has no death-age requirement
=> no death chronology hydration required
=> other prerequisites decide eligibility
```

### 49.10 Vampire rise at dawn

```text
Actor has active known post-death Feature
enter dead
=> indexed listener creates dawn obligation
at dawn, if rule still applies
=> transformation Activity atomically changes form/LifeState/HP
```

### 49.11 Independent Unconscious applications

```text
U_lifecycle from zero HP
U_sleep from spell
healing returns Actor active
=> remove U_lifecycle
=> U_sleep remains
```

### 49.12 Dead Actor with continuing curse

```text
curse has remaining duration and no ends-on-death rule
Actor enters dead
=> curse remains nonterminal
revival before curse expiry
=> curse can become applicable again
```

## 50. Forward dependencies

### Step 3 owns

- exact lethal-transition interception/pending Signal semantics;
- exact atomic mutation segmentation;
- `LifeStateTransitionPlan` protocol/event/receipt representation;
- idempotent operation identity for death saves and revival;
- same-boundary ordering and zero-time causal closure;
- exact transition provenance representation;
- mandatory Death Save continuation when an encounter/procedure otherwise closes;
- choice/reaction/Activity sequencing around stabilization and revival.

### Step 5 owns

- cross-scene/multiplayer chronology reconciliation;
- durable/local temporal context transfer;
- preservation/reconciliation of sufficient current-death provenance for lazy revival eligibility when scenes or publication boundaries differ.

These are deliberate forward dependencies. Step 2 must not invent substitute LifeState-specific event, scheduler, or reconciliation systems.

## 51. Schema/catalog consequences deferred to alignment

The later Step 2 schema/catalog pass is expected to need equivalent machine support for:

- registered LifeState IDs for the four baseline states;
- registered LifeStatePolicy IDs/capabilities;
- optional Actor lifecycle-policy override/inheritance reference if needed by the selected final shape;
- typed conditional LifeState progress;
- death-save count bounds `0..2`;
- common TemporalBinding reuse for Stable recovery;
- selectors/queries required by the health/effect block;
- typed transition operation/value contracts owned jointly with Step 3 boundaries.

No machine file is changed by this design checkpoint.

## 52. Exit criteria for this sub-block

LifeState ownership is sufficiently closed for current Step 2 sequencing when all of the following remain true:

1. `active / dying / stable / dead` represent the minimum baseline without duplicate Condition/entity/type semantics;
2. Actor HP and current LifeState are separate authorities;
3. death-save progress exists only for dying and never stores threshold value 3;
4. Stable owns only the one real automatic recovery temporal obligation required by the rules;
5. Dead creates no generic revival timer/window/index;
6. revival windows are mechanic-owned and evaluated lazily;
7. current-death provenance remains retrievable without requiring a running Actor countdown;
8. automatic post-death mechanics are opt-in indexed Trigger/Effect behavior;
9. LifeStateResolver plans but does not commit;
10. HP/LifeState/progress/companion Condition/temporal deltas can commit atomically through Step 3;
11. ordinary death does not retire Actor identity or purge all Effects;
12. policies remain small registered ruleset capabilities instead of arbitrary FSMs;
13. common-path performance is proportional to the affected Actor and local interested mechanics;
14. no discovered D&D case requires a fifth baseline state or separate lifecycle subsystem.

## 53. Whole-architecture review requirement

This checkpoint is not final in isolation.

The later holistic review and additional brainstorming pass must reconsider it together with **the entire HDM architecture, structures, logic, ownership, schemas, execution model, persistence model, chronology, and inter-module relationships**.

LifeState-specific questions for that pass include:

- whether the four-state vocabulary remains minimal after complete ruleset seed review;
- whether policy inheritance/override is still the cheapest way to support important NPCs;
- whether stable temporal progress fits the final common TemporalBinding schema cleanly;
- whether Step-3 prospective interception is sufficient for all lethal-outcome prevention mechanics;
- whether lazy current-death provenance survives the final snapshot/compaction and Step-5 chronology model without redundant Actor fields;
- whether health/effect selectors remain orthogonal to Conditions and LifeState;
- whether any real full-seed mechanic proves a fifth state, extra state-local progress, or a different transition boundary necessary.

These questions do not block current Step 2 sequencing.

## 54. Exact continuation

LifeState policy/progress/transition ownership is preliminarily closed for current sequencing.

The next open Step 2 architecture block is **health/effect selectors and query boundaries**.

That block must determine the minimum registered selector/query surface required by the accepted HP, LifeState, Condition, Effect, Resource, Duration, and Recovery models without creating duplicate stored authorities.

After selectors, Step 2 still requires schema/catalog alignment, focused validation cases, and the final independent Step 2 critical pass before the Step 2 gate can close.