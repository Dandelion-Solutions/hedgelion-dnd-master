# HDM Actor Data Model

Status: **AGREED — STEP 2 + R2.2 / R2.7 MACHINE ALIGNMENT APPLIED**

Schemas:

- `SCHEMAS/actor-archetype-data.schema.json`
- `SCHEMAS/world-actor-state.schema.json`
- `SCHEMAS/world-actor-group-state.schema.json`
- `SCHEMAS/temporal-binding.schema.json`

Owning additions:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`

## 1. One progressively materialized actor

`world.actor` represents narrative NPCs, mechanically resolved creatures, companions, and player characters. HDM does not create separate entity kinds for those levels of detail. PC/NPC/companion/summon/swarm distinctions are roles/facets of the same Actor kind unless a concrete rule requires another owner.

Only `state.name` is required. Expected fields are added when known or needed. HP, ability values, private continuity and relationship views are not generated for incidental Actors in advance.

Mechanical materialization happens before any affected roll:

```text
mechanics required
  -> select or create archetype
  -> populate sufficient typed Actor state
  -> validate and record materialization event
  -> execute Activity
```

Narrative/continuity materialization is similarly sparse: missing untracked private state does not authorize speculative durable filling.

## 2. Actor archetype and LifeState policy

`definition.actor_archetype` contains reusable baseline data for a type of creature. A particular Actor references it through `definition_id`.

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

An ordinary Actor does not copy an inherited/default policy into state merely for convenience. The instance stores only individual mutable or exceptional values. Reusable baseline values stay in the archetype/definition.

## 3. Minimal build

`build` is optional and is intended for player characters, developing companions, and exceptional NPCs. Only `level` is required when `build` exists. The history that produced the level is retained by gameplay events; a resolved profile may be cached by the runtime.

An Actor may use both `definition_id` and `build`. Resolution order is:

```text
archetype -> build -> permanent instance components -> active Effects
```

Numerical contributions are combined; the resolved result is cache data and is not written back as another authoritative Actor field.

The current build shape is intentionally small. Final rules-surface coverage, including any required multiclass/advancement shape, is audited by WP-06/WP-24 before implementation planning; absence of a field here is not permission to invent unsupported character mechanics at runtime.

## 4. Abilities

Actor ability state stores only instance-owned components:

```json
{
  "str": {"base": 15, "adjustment": 1},
  "dex": {"adjustment": 2}
}
```

- `base`, when present, is the Actor's own base value;
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

All members are optional until HP is needed. Maximum HP resolves from the first available base (Actor, archetype, or build calculation), plus permanent Actor adjustment and active Rule Element contributions at the registered `health.maximum` calculation selector.

This `hp` object is the single Actor-state authority for current HP, maximum-HP components, and temporary HP. The generic `resources` map must not store a second HP or temporary-HP counter. The resolved maximum and `health.bloodied` are derived values and are never copied back into Actor state as writable aliases.

`temporary` means D&D temporary HP and is non-negative. A temporary reduction of maximum HP is a contribution to `health.maximum`, not a negative temporary-HP value. If resolved maximum falls below current HP, the prospective health plan normalizes current HP according to registered health rules before commit.

HP and lifecycle state are separate authorities. When runtime first materializes an Actor's `hp`, it must materialize `life_state_id` in the same atomic transition. Zero HP never directly means death.

The initial LifeState vocabulary is exactly:

```text
life.active
life.dying
life.stable
life.dead
```

LifeState is distinct from creature type, Conditions, consciousness, action availability, Effect lifecycle, and entity retirement.

### 5.1 State-local progress

`life_state_progress` exists only when the current LifeState intrinsically owns such progress:

```text
life.active -> absent

life.dying ->
    death_saves.successes = 0..2
    death_saves.failures  = 0..2

life.stable ->
    recovery_binding = concrete TemporalBinding

life.dead -> absent
```

A third death-save success/failure is a transition edge, not a stored value. Stable automatic recovery uses the common temporal machinery; it does not create a LifeState-specific scheduler.

A dead Actor remains the same Actor identity. Death does not itself delete or retire the record, purge every Effect, or create a generic resurrection timer. Revival eligibility belongs to the concrete revival mechanic.

Exact prospective ordering, atomic commit, idempotent receipts, and transition Signals/Events are Step-3 responsibilities.

## 6. Resources

Persistent Actor Resources are keyed by stable Resource definition ID:

```json
{
  "resource.second_wind": {"current": 0},
  "resource.spell_slot.level_1": {"current": 3}
}
```

The Resource definition owns mechanic type, lifetime owner, storage model, baseline capacity/recovery semantics, and spending policy. Persistent Actor/Asset ResourceState stores its authoritative `current` value and may own a concrete `recovery_binding` when a real timed recovery obligation exists.

Procedure-local Resources use their procedure lifetime owner and store consumed state (`spent`) there instead of becoming Actor fields. `resource.capacity` and `resource.available` hide this physical difference from declarative mechanics.

The Temporal Agenda is a disposable due-index over authoritative temporal bindings. It is not a second Resource or recovery authority.

## 7. Actor-private continuity

Current non-epistemic private continuity belongs to the source Actor. It is not a separate world record and does not duplicate `world.knowledge`.

Durable native Actor state uses one optional sparse `continuity` block:

```text
continuity
    foundation?
    evolving?
    relationships?
```

### 7.1 Foundation

`foundation` stores only materially persistent identity-level private continuity. Initial categories are:

```text
values
 temperament
 identity
```

Each entry is a concise statement with optional accepted `source_refs`. Ordinary cognition assessment cannot rewrite foundation by accumulation; material foundation change requires the stronger R2.2 foundation-transition boundary and accepted evidence.

### 7.2 Durable evolving cognition

`evolving` may contain only the baseline sparse near-state needed for future behavior:

```text
long_term_goal
current_objective
next_intention
material_commitments[]
reconsideration_cues[]
```

Entries store concise semantic statements and optional source refs. They do not store hidden reasoning, chain-of-thought, a plan graph, strategy DAG, exhaustive alternatives or every generated thought.

`NO_CHANGE` cognition assessment produces no semantic write.

### 7.3 Directed source-Actor relationship views

Relationship continuity is nested under the source Actor and keyed by target subject ID:

```text
source Actor state
    continuity.relationships[target_subject_id]
```

`A -> B` and `B -> A` are independent. The baseline sparse facets are:

```text
trust
affinity
fear
respect
hostility
felt_obligation
```

Each present facet uses the small qualitative vocabulary:

```text
low | moderate | high
```

Absence means not materially tracked; there is no universal neutral zero or relationship score. Optional `basis_refs` and `last_changed_event_id` support inspectability without turning the relationship view into an event log.

These facets are subjective. They cannot establish organization membership, ownership, contract obligation, target intent, reciprocal feeling, consent, location or any other objective fact.

### 7.4 Transient private state

Affect, attention, urgency and local intention are ephemeral by default. The durable `world.actor` schema deliberately has **no baseline `transient_private` field**.

Short-lived private state may exist in HOT/role-local execution state for the current need. If evaluation later proves that a class of transient state must survive context/process loss, admitting a durable representation requires an explicit bounded lifecycle/invalidation contract; do not smuggle it into `details`.

### 7.5 PC agency

The same Actor schema may physically represent player-authored PC continuity, but Actor cognition machinery cannot silently author a player-controlled PC's voluntary belief, emotion, loyalty, interpretation, goal, plan, speech, consent or commitment.

Player binding/control remains outside Actor state. Mutation authorization, not schema shape, enforces player agency.

## 8. Roles, placement, ownership and derived relations

- `roles` are mutable instance classifications such as PC, NPC or companion.
- `location_id` is the Actor's single physical world location.
- Scene, encounter and zone participation are not copied into Actor state.
- Inventory is derived from `world.asset.owner_actor_id`.
- Active target-local Effect applications are derived from `world.effect.target_id`.
- Named Condition presence/value is derived from Condition-bearing Effect applications and registered Condition aggregation; Actor state has no copied Condition list.
- Objective organization membership belongs to the organization/native membership owner, not subjective Actor relationship continuity.
- GitHub/user ownership of a main character belongs to campaign player configuration, not the Actor.
- Current fictional proposition stance belongs to `world.knowledge`; human exposure belongs to `runtime.disclosure`.

Material Actor-private continuity must use the typed `continuity` block rather than arbitrary `details`. `details` remains nonmechanical descriptive material and is not a hidden alternate cognition store.

## 9. MechanicalContext reads

Declarative mechanics do not inspect Actor JSON through arbitrary property paths. The initial Actor-related registered MechanicalContext accessors include:

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

Every calculation reads one pinned committed/prospective state-view identity. Engine-owned mechanical facts are resolved by deterministic core; the LLM cannot supply them as trusted invocation facts.

Actor continuity is not automatically a MechanicalContext source. If a future mechanic truly consumes a continuity facet, that dependency requires an explicit registered selector/accessor contract rather than reading prose/private fields ad hoc.

## 10. Actor groups

`world.actor_group` is a named collection, not an Actor subtype. It has no HP, abilities, build, LifeState or private cognition merely by being a group. Group actions resolve through members or another explicit Activity/owner. A D&D swarm that acts as one creature remains a `world.actor` with the `actor.swarm` facet.

## 11. Physical representation boundary

Semantic authority follows the Actor owner contract, not a storage format.

- Git-published native Actor records are durable reconstruction/interchange representation.
- During play, accepted SOFT Actor state may be newer in HOT/SQLite than the durable Git frontier.
- SQLite indexes/caches and Context Runtime projections are derived unless they physically host the current accepted owner state for the active runtime.
- Publication materializes the accepted owner state through Step-5 durability/publication laws; Git/YAML format does not create a second semantic owner.

Loss of unpublished SOFT Actor state recovers to compatible durable native sources; recovery never invents the lost progress.
