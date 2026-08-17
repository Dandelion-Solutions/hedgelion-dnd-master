# HDM Actor Data Model

Status: **AGREED**

Target: `feature/mechanical-runtime-hot-state`

Schemas:

- `SCHEMAS/actor-archetype-data.schema.json`
- `SCHEMAS/world-actor-state.schema.json`
- `SCHEMAS/world-actor-group-state.schema.json`

## 1. One progressively materialized actor

`world.actor` represents narrative NPCs, mechanically resolved creatures,
companions, and player characters. HDM does not create separate entity kinds
for those levels of detail. Only `state.name` is required.

Expected fields are added when known or needed:

```json
{
  "name": {"en": "Old Innkeeper", "ru": "Старый трактирщик"},
  "roles": ["actor.nonplayer_character"],
  "location_id": "location-00017",
  "details": {
    "occupation": "innkeeper",
    "appearance": "Седой мужчина с обожжённой рукой"
  }
}
```

HP and ability values are not generated for incidental actors in advance. An
actor becomes mechanically materialized immediately before an interaction that
requires those values. Known bosses, guards, blocking monsters, player
characters, and other intentionally mechanical actors may be prepared earlier.

Materialization happens before any affected roll:

```text
mechanics required
  -> select or create archetype
  -> populate sufficient typed actor state
  -> validate and record materialization event
  -> execute Activity
```

## 2. Actor archetype

`definition.actor_archetype` contains reusable constant or baseline data for a
type of creature. A particular actor references it through `definition_id`.

```json
{
  "id": "ruleset.goblin_warrior",
  "kind": "definition.actor_archetype",
  "name": {"en": "Goblin Warrior", "ru": "Гоблин-воин"},
  "data": {
    "creature_type_id": "creature_type.humanoid",
    "size_id": "size.small",
    "abilities": {
      "str": 8,
      "dex": 14,
      "con": 10,
      "int": 10,
      "wis": 8,
      "cha": 8
    },
    "hp": {"maximum": 7},
    "activity_ids": ["activity.goblin_scimitar"]
  }
}
```

The instance stores only individual mutable or exceptional values:

```json
{
  "id": "actor-00127",
  "kind": "world.actor",
  "definition_id": "ruleset.goblin_warrior",
  "state": {
    "name": {"en": "Grik"},
    "roles": ["actor.nonplayer_character"],
    "location_id": "location-00031",
    "hp": {"current": 4}
  }
}
```

## 3. Minimal build

`build` is optional and is intended for player characters, developing
companions, and exceptional NPCs. Its initial contract deliberately excludes
advancement-choice history, respec, and multiclass structures.

```json
{
  "level": 4,
  "species_id": "species.human",
  "background_id": "background.soldier",
  "class_id": "class.fighter",
  "subclass_id": "subclass.champion"
}
```

Only `level` is required when `build` exists. The history that produced the
level is retained by gameplay events; a resolved profile may be cached by the
runtime. Multiclassing may later evolve `class_id` into a plural structure when
there is a concrete requirement.

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
- dynamic contributions come from active Effects;
- resolved scores and modifiers live only in HOT cache.

For an ordinary archetype instance, `state.abilities` is absent. For a player
character without an archetype, `base` values provide the actor's scores.

## 5. Hit points

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
adjustment and active Effect contributions.

This `hp` object is the single Actor-state authority for current HP, maximum-HP
components, and temporary HP. The generic `resources` map must not store a
second HP or temporary-HP counter. Health-related engine capabilities may read
and change this object, but they do not imply a duplicate
`definition.resource` instance.

`temporary` means D&D temporary HP and is non-negative. A temporary reduction
of maximum HP is a signed Effect contribution to `actor.hp.maximum`, not a
negative temporary-HP value. If resolved maximum falls below current HP,
runtime clamps current HP to the new maximum and records the change.

Current project policy treats zero HP as death or destruction unless a specific
rule says otherwise. In the selected D&D rules, a player character at zero HP
uses unconscious/stable/death-save mechanics instead of being declared dead
immediately. That exception derives from the Actor role and ruleset; it does not
require a second HP field. A broader configurable lifecycle status remains
deferred backlog work.

## 6. Resources

Resources are keyed by stable resource-definition ID:

```json
{
  "resource.second_wind": {"current": 0},
  "resource.spell_slot.level_1": {"current": 3}
}
```

Capacity, recovery, and spending policy come from definitions/build. Actor
state stores current values. No array position has identity. Persistent
resources such as spell slots and feature uses belong here. Procedure-local
action/reaction/movement budgets belong to the active Resolution/Encounter
state, not to this persistent Actor map.

## 7. Roles, placement, and ownership

- `roles` are mutable instance classifications such as NPC or companion.
- `location_id` is the actor's single physical world location.
- Scene, encounter, and zone participation are not copied into actor state.
- Inventory is derived from `world.asset.owner_actor_id`.
- Active effects are derived from `world.effect.target_ids`.
- Allegiance is represented by organization membership and relationships.
- GitHub-user ownership of a main character belongs to campaign player
  configuration, not the actor. Transfer and shared control are not currently
  supported.

## 8. Actor groups

`world.actor_group` is a named collection, not an actor subtype:

```json
{
  "id": "actor-group-00012",
  "kind": "world.actor_group",
  "state": {
    "name": {"en": "Northern Patrol", "ru": "Северный патруль"},
    "member_ids": ["actor-00041", "actor-00042"],
    "leader_id": "actor-00041"
  }
}
```

It has no HP, abilities, or build. Group actions resolve through members or a
separate Activity. A D&D swarm that acts as one creature remains a
`world.actor` with the `actor.swarm` facet.
