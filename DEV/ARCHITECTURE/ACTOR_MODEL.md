# HDM Actor Data Model

Status: **AGREED — STEP 2 MACHINE ALIGNMENT APPLIED**

Target: `feature/mechanical-runtime-hot-state`

Schemas:

- `SCHEMAS/actor-archetype-data.schema.json`
- `SCHEMAS/world-actor-state.schema.json`
- `SCHEMAS/world-actor-group-state.schema.json`
- `SCHEMAS/temporal-binding.schema.json`

## 1. One progressively materialized actor

`world.actor` represents narrative NPCs, mechanically resolved creatures,
companions, and player characters. HDM does not create separate entity kinds
for those levels of detail. Only `state.name` is required.

Expected fields are added when known or needed. HP and ability values are not
generated for incidental actors in advance. An actor becomes mechanically
materialized immediately before an interaction that requires those values.
Known bosses, guards, blocking monsters, player characters, and other
intentionally mechanical actors may be prepared earlier.

Materialization happens before any affected roll:

```text
mechanics required
  -> select or create archetype
  -> populate sufficient typed actor state
  -> validate and record materialization event
  -> execute Activity
```

## 2. Actor archetype and LifeState policy

`definition.actor_archetype` contains reusable baseline data for a type of
creature. A particular Actor references it through `definition_id`.

An archetype may declare `life_state_policy_id`. Policy resolution is:

```text
explicit Actor override, if materially present
    -> archetype policy, if declared
    -> selected ruleset default
```

The initial registered D&D policies are:

```text
life_policy.dnd2024.character_like
life_policy.dnd2024.monster_default
```

An ordinary Actor does not copy an inherited/default policy into state merely
for convenience.

The instance stores only individual mutable or exceptional values. Reusable
baseline values stay in the archetype/definition.

## 3. Minimal build

`build` is optional and is intended for player characters, developing
companions, and exceptional NPCs. Its initial contract deliberately excludes
advancement-choice history, respec, and multiclass structures.

Only `level` is required when `build` exists. The history that produced the
level is retained by gameplay events; a resolved profile may be cached by the
runtime.

An actor may use both `definition_id` and `build`. Resolution order is:

```text
archetype -> build -> permanent instance components -> active Effects
```

Numerical contributions are combined; the resolved result is cache data and is
not written back as another authoritative actor field.

## 4. Abilities

Actor ability state stores only instance-owned components:

```json
{
  "str": {"base": 15, "adjustment": 1},
  "dex": {"adjustment": 2}
}
```

- `base`, when present, is the actor's own base value;
- otherwise the resolver may use the archetype base;
- `adjustment` is a permanent instance adjustment;
- dynamic contributions come from participating Effects;
- resolved scores and modifiers live only in HOT cache/MechanicalContext.

## 5. Hit points and LifeState

The Actor HP authority is:

```json
{
  "current": 18,
  "maximum_base": 20,
  "maximum_adjustment": 0,
  "temporary": 3
}
```

All members are optional until HP is needed. Maximum HP resolves from the first
available base (actor, archetype, or build calculation), plus permanent actor
adjustment and active Rule Element contributions at the registered
`health.maximum` calculation selector.

This `hp` object is the single Actor-state authority for current HP, maximum-HP
components, and temporary HP. The generic `resources` map must not store a
second HP or temporary-HP counter. The resolved maximum and `health.bloodied`
are derived values and are never copied back into Actor state as writable
aliases.

`temporary` means D&D temporary HP and is non-negative. A temporary reduction
of maximum HP is a contribution to `health.maximum`, not a negative temporary-HP
value. If resolved maximum falls below current HP, the prospective health plan
normalizes current HP according to the registered health rules before commit.

HP and lifecycle state are separate authorities. When runtime first
materializes an Actor's `hp`, it must materialize `life_state_id` in the same
atomic transition. Zero HP never directly means death.

The initial LifeState vocabulary is exactly:

```text
life.active
life.dying
life.stable
life.dead
```

LifeState is distinct from creature type, Conditions, consciousness, action
availability, Effect lifecycle, and entity retirement.

### State-local progress

`life_state_progress` exists only when the current LifeState intrinsically owns
such progress:

```text
life.active -> absent

life.dying ->
    death_saves.successes = 0..2
    death_saves.failures  = 0..2

life.stable ->
    recovery_binding = concrete TemporalBinding

life.dead -> absent
```

A third death-save success/failure is a transition edge, not a stored value.
Stable automatic recovery uses the common temporal machinery; it does not
create a LifeState-specific scheduler.

A dead Actor remains the same Actor identity. Death does not itself delete or
retire the record, purge every Effect, or create a generic resurrection timer.
Revival eligibility belongs to the concrete revival mechanic.

Exact prospective ordering, atomic commit, idempotent receipts, and transition
Signals/Events are Step-3 responsibilities.

## 6. Resources

Persistent Actor Resources are keyed by stable Resource definition ID:

```json
{
  "resource.second_wind": {"current": 0},
  "resource.spell_slot.level_1": {"current": 3}
}
```

The Resource definition owns mechanic type, lifetime owner, storage model,
baseline capacity/recovery semantics, and spending policy. Persistent
Actor/Asset ResourceState stores its authoritative `current` value and may own a
concrete `recovery_binding` when a real timed recovery obligation exists.

Procedure-local Resources use their procedure lifetime owner and store consumed
state (`spent`) there instead of becoming Actor fields. `resource.capacity` and
`resource.available` hide this physical difference from declarative mechanics.

The Temporal Agenda is a disposable due-index over authoritative temporal
bindings. It is not a second Resource or recovery authority.

## 7. Roles, placement, and ownership

- `roles` are mutable instance classifications such as NPC or companion.
- `location_id` is the actor's single physical world location.
- Scene, encounter, and zone participation are not copied into actor state.
- Inventory is derived from `world.asset.owner_actor_id`.
- Active target-local Effect applications are derived from `world.effect.target_id`.
- Named Condition presence/value is derived from Condition-bearing Effect
  applications and registered Condition aggregation; Actor state has no copied
  Condition list.
- Allegiance is represented by organization membership and relationships.
- GitHub-user ownership of a main character belongs to campaign player
  configuration, not the Actor.

## 8. MechanicalContext reads

Declarative mechanics do not inspect Actor JSON through arbitrary property
paths. The initial Actor-related registered MechanicalContext accessors include:

```text
health.current
health.temporary
health.maximum
health.bloodied
life.state
condition.present
condition.value
resource.capacity
resource.available
```

Every calculation reads one pinned committed/prospective state-view identity.
Engine-owned mechanical facts are resolved by the deterministic core; the LLM
cannot supply them as trusted invocation facts.

## 9. Actor groups

`world.actor_group` is a named collection, not an Actor subtype. It has no HP,
abilities, build, or LifeState. Group actions resolve through members or a
separate Activity. A D&D swarm that acts as one creature remains a
`world.actor` with the `actor.swarm` facet.
