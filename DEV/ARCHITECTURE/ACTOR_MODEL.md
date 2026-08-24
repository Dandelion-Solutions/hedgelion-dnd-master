# HDM Actor Data Model

Status: **AGREED — STEP 2 + R2.2 / R2.7 MACHINE ALIGNMENT APPLIED**

Schemas:

- `SCHEMAS/actor-archetype-data.schema.json`
- `SCHEMAS/world-actor-state.schema.json`
- `SCHEMAS/world-actor-group-state.schema.json`
- `SCHEMAS/temporal-binding.schema.json`

Owning additions:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md`

## 1. One progressively materialized Actor

`world.actor` represents narrative NPCs, mechanically resolved creatures, companions, summons, swarms and player characters. HDM does not create separate entity kinds for those levels of detail. PC/NPC/companion distinctions are Actor roles/facets unless a concrete rule proves another owner.

No Actor-state content field is universally required merely to create a stable Actor identity. The world-record `id` is the stable record identity. `state.name` is optional; `state.concept` is an optional normalized nonmechanical framing statement. Expected mechanical/private fields are added when known or needed. HP, build choices, private continuity and relationship views are not generated for incidental Actors in advance.

A provisional player character may therefore exist before a name is known. A stable player-authored concept such as `я буду демоном огня` may justify a PROVISIONAL_IDENTITY durability boundary while the same Actor remains mechanically incomplete.

`concept` is not executable mechanics. It may guide preparation/inference, but any mechanical consequence must be translated into accepted rules-valid archetype/build/Actor state before adjudication relies on it.

For a player character, progressive materialization may happen during gameplay under `GAME/CORE/DIEGETIC_ONBOARDING.md`. READY_PC is not a prerequisite for the first scene. Before any mechanically relevant outcome, every dependency material to that outcome must already be established. READY_PC is the later **initial mechanical commitment frontier** for ordinary unrestricted mechanics-capable play; it is not a requirement that every possible dossier field or future mechanic be eagerly materialized.

Mechanical materialization follows:

```text
mechanics required
  -> resolve bounded dependencies for this outcome
  -> use explicit player choices / rules inheritance / accepted concept inference / defaults
  -> select/load reusable definitions as required
  -> populate sufficient typed Actor/Asset/Effect state
  -> validate current state view
  -> execute Activity
```

Missing untracked state never authorizes context-sensitive speculative filling.

### 1.1 Initial mechanical commitment and safe laziness

Before READY_PC, every unresolved discretionary choice that could materially change ordinary current-play legality, probability, defense, resource availability, capability or consequence must be committed through the onboarding precedence in `CHARACTER_READINESS.md`.

After READY_PC, a not-yet-materialized value is safe only when it is:

- uniquely/deterministically derivable from already committed authoritative anchors;
- descriptive/nonmechanical;
- created by a genuine later acquisition/evolution boundary; or
- governed by a deterministic/delegated policy fixed before the situation where the value matters.

HDM never waits for a favorable situation and then selects a previously open mechanical option to fit it.

## 2. Actor archetype and LifeState policy

`definition.actor_archetype` contains reusable baseline data for a type of creature. A particular Actor references it through `definition_id`.

An archetype may declare `life_state_policy_id`. Policy resolution is:

```text
explicit Actor override, if materially present
    -> archetype policy, if declared
    -> selected ruleset default
```

Initial D&D policies:

```text
life_policy.dnd2024.character_like
life_policy.dnd2024.monster_default
```

An ordinary Actor does not copy inherited/default policy into state merely for convenience. Instance state stores only individual mutable or exceptional values.

A concept may motivate selection/creation of a compatible archetype, but the selected validated `definition_id` is the mechanical/reusable anchor. The prose concept does not override archetype/rules contracts.

## 3. Reconstructable build state

`build` is optional and is intended for player characters, developing companions and other leveled Actors whose current mechanical profile depends on instance-owned construction choices.

The Actor stores only selections needed to reconstruct the current build from the resolved catalog. It does **not** store a second flattened character sheet.

Canonical shape:

```text
build
    species_id?
    background_id?
    class_progression[]
        class_id
        level
        subclass_id?
    choice_bindings?
        <stable advancement choice id> -> selected definition IDs
    spellcasting?
        known_spell_ids?
        prepared_spell_ids?
        spellbook_spell_ids?
```

`class_progression` is required when `build` exists. Total character level is derived from its entries and is not duplicated as another writable `level` field. Single-class and multiclass Actors use the same representation.

`choice_bindings` stores only material instance-owned selections that cannot be reconstructed from fixed class/species/background/archetype grants. Selected definitions remain reusable catalog definitions; the binding never copies their mechanics.

`spellcasting` stores mutable current spell-selection membership only when the ruleset requires it. Always-granted spells, formulas, save DCs, attack modifiers and other derivable values are not duplicated.

The history that produced the build belongs to accepted events/history. A resolved READY_PC sheet/profile may be cached but is not another authority.

Resolution order is:

```text
archetype
  -> build composition / selected definition grants
  -> permanent instance components
  -> active Effects
  -> derived MechanicalContext
```

A player need not state level, HP maximum, resource capacity or every proficiency as questionnaire answers when those values can be validly selected/derived from accepted anchors. Master-side bookkeeping may establish them through the approved readiness precedence, but once a discretionary commitment is relied upon or crosses READY_PC it cannot be silently retuned to fit later circumstances.

WP-06 owns the final advancement/choice-definition contract that supplies stable choice IDs and validates each `choice_bindings` selection against the loaded ResolvedCatalogContext. Structurally valid arbitrary choice keys are not automatically legal.

## 4. Abilities

Actor ability state stores only instance-owned components:

```json
{
  "str": {"base": 15, "adjustment": 1},
  "dex": {"adjustment": 2}
}
```

- `base`, when present, is the Actor's own base value;
- otherwise resolver may use archetype/build base;
- `adjustment` is a permanent instance adjustment;
- dynamic contributions come from participating Effects;
- resolved scores/modifiers live only in HOT cache/MechanicalContext.

Before READY_PC, common checks/saves must already be deterministically resolvable from committed Actor/archetype/build sources. The number does not have to be player-spoken or redundantly copied when it is uniquely derivable.

## 5. Hit points and LifeState

Actor HP authority:

```json
{
  "current": 18,
  "maximum_base": 20,
  "maximum_adjustment": 0,
  "temporary": 3
}
```

All members are optional until HP matters. Maximum HP resolves from the first available base (Actor, archetype or build calculation), plus permanent Actor adjustment and active Rule Element contributions at `health.maximum`.

This `hp` object is the single Actor-state authority for current HP, maximum-HP components and temporary HP. Generic `resources` must not store a second HP or temporary-HP counter. Resolved maximum and `health.bloodied` are derived.

`temporary` means D&D temporary HP and is non-negative. Temporary maximum-HP reduction is a contribution to `health.maximum`, not negative temporary HP. If resolved maximum falls below current HP, prospective health resolution normalizes current HP before commit.

HP and lifecycle are separate authorities. When runtime first materializes Actor `hp`, it materializes `life_state_id` in the same atomic transition. Zero HP never directly means death.

LifeState vocabulary:

```text
life.active
life.dying
life.stable
life.dead
```

LifeState is distinct from creature type, Conditions, consciousness, action availability, Effect lifecycle and entity retirement.

### 5.1 State-local progress

`life_state_progress` exists only when current LifeState owns such progress:

```text
life.active -> absent
life.dying -> death_saves.successes/failures = 0..2
life.stable -> recovery_binding = concrete TemporalBinding
life.dead -> absent
```

A third death-save success/failure is a transition edge, not stored value. Stable recovery uses common temporal machinery. Dead Actor preserves identity; death alone does not delete/retire the record or imply resurrection machinery.

## 6. Resources

Persistent Actor Resources are keyed by stable Resource definition ID:

```json
{
  "resource.second_wind": {"current": 0},
  "resource.spell_slot.level_1": {"current": 3}
}
```

Resource definition owns mechanic type, lifetime owner, storage model, capacity/recovery semantics and spending policy. Actor/Asset ResourceState stores authoritative `current` and may own a concrete `recovery_binding` when a real timed recovery obligation exists.

Resource capacity is normally derived from the accepted definition + Actor/build/archetype/Effect context. The player is not asked to invent a capacity merely because the engine needs one.

Procedure-local Resources own their consumed state in the Procedure rather than becoming Actor fields. MechanicalContext accessors hide this physical difference. Temporal Agenda is a derived due-index, not Resource authority.

## 7. Actor-private continuity

Current non-epistemic private continuity belongs to the source Actor. It is not a separate world record and does not duplicate `world.knowledge`.

Durable Actor state uses one optional sparse `continuity` block:

```text
continuity
    foundation?
    evolving?
    relationships?
```

### 7.1 Foundation

`foundation` stores only materially persistent identity-level private continuity:

```text
values
temperament
identity
```

Each entry is a concise statement with optional accepted `source_refs`. Ordinary cognition does not rewrite foundation by accumulation; material foundation change uses the stronger R2.2 transition boundary.

For a player-controlled PC, voluntary self-concept/inner identity remains player-owned. Top-level `concept` is a compact current framing input; it does not authorize Actor cognition machinery to invent the player's beliefs, goals or self-interpretation.

### 7.2 Durable evolving cognition

`evolving` may contain only sparse near-state needed for future behavior:

```text
long_term_goal
current_objective
next_intention
material_commitments[]
reconsideration_cues[]
```

Entries contain concise semantic statements and optional source refs. They do not store chain-of-thought, hidden reasoning traces, strategy DAGs, exhaustive alternatives or every generated thought. `NO_CHANGE` produces no semantic write.

### 7.3 Directed source-Actor relationships

Relationship continuity is nested under source Actor and keyed by target subject ID:

```text
source Actor state
    continuity.relationships[target_subject_id]
```

`A -> B` and `B -> A` are independent. Baseline sparse facets:

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

Absence means not materially tracked, not neutral zero. Optional `basis_refs` and `last_changed_event_id` support inspectability without becoming an event log.

These facets are subjective. They cannot establish organization membership, legal ownership, contract obligation, target intent, reciprocal feeling, consent, location or another objective fact.

### 7.4 Transient private state

Affect, attention, urgency and local intention are ephemeral by default. Durable `world.actor` has **no baseline `transient_private` field**.

Short-lived private state may exist in HOT/role-local execution state. If later evidence proves a class must survive process/context loss, admitting durable representation requires explicit bounded lifecycle/invalidation; do not hide it in `details`.

### 7.5 PC agency

The same Actor schema may represent player-authored PC continuity, but Actor cognition machinery cannot silently author a player-controlled PC's voluntary belief, emotion, loyalty, interpretation, goal, plan, speech, consent or commitment.

Player binding/control lives outside Actor state. Mutation authorization, not schema shape, enforces agency.

## 8. Roles, placement, ownership and derived relations

- `name` is optional current presentation identity; stable record identity is Actor ID.
- `concept` is optional nonmechanical framing/player-intent summary; it is not executable mechanics.
- `roles` are mutable instance classifications such as PC/NPC/companion.
- `location_id` is Actor's single physical world location.
- Scene/encounter/zone participation is not copied into Actor state.
- Inventory derives from `world.asset.owner_actor_id`.
- Active target-local Effects derive from `world.effect.target_id`.
- Named Condition presence/value derives from Condition-bearing Effects and aggregation; Actor has no copied Condition list.
- Objective organization membership belongs to its native owner, not subjective relationship continuity.
- GitHub/user ownership of a PC belongs to campaign player configuration, not Actor.
- Current proposition stance belongs to `world.knowledge`; human exposure belongs to `runtime.disclosure`.
- Material Actor-private continuity uses typed `continuity`, not arbitrary `details`.

## 9. MechanicalContext reads

Declarative mechanics do not inspect Actor JSON through arbitrary property paths. Initial Actor-related accessors include:

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

Every calculation reads one pinned committed/prospective state-view identity. Engine-owned mechanical facts are deterministic; LLM cannot supply them as trusted invocation facts.

Concept text and Actor continuity are not automatically MechanicalContext sources. A concept-derived mechanical choice must first be promoted into validated Actor/build/archetype/definition state. A future mechanic consuming a continuity facet requires an explicit registered selector/accessor rather than ad-hoc prose reads.

## 10. Actor groups

`world.actor_group` is a named collection, not an Actor subtype. It has no HP, abilities, build, LifeState or private cognition merely by being a group. Group actions resolve through members or another explicit owner. A D&D swarm acting as one creature remains `world.actor` with `actor.swarm` facet.

## 11. Physical representation boundary

Semantic authority follows the Actor owner contract, not storage format.

- Git-published native Actor records are durable reconstruction/interchange representation.
- During play, accepted SOFT Actor state may be newer in HOT/SQLite than durable Git frontier.
- SQLite indexes/caches and Context Runtime projections are derived unless physically hosting current accepted owner state for the active runtime.
- Publication materializes accepted owner state through Step-5 laws; Git/YAML format does not create another semantic owner.

Loss of unpublished SOFT Actor state recovers to compatible durable sources; recovery never invents lost progress.
