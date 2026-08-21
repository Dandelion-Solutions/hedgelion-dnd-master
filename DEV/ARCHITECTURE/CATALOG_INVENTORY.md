# HDM Catalog Inventory

Status: **REVIEWED BASELINE — STEPS 1–3 + STEP-4 + STEP-5.0 RETIREMENTS APPLIED**

Catalog version: `1.6.0`

This document fixes the class inventory used to design schemas and runtime
contracts. "Complete" means sufficient coverage for the intended HDM
architecture and the SRD 5.2.1 rules surface. Future catalog versions may add
missing classes without repurposing existing IDs.

The exact machine-readable IDs are in `CATALOG/core-catalog.json`. This document
is authoritative for their classification.

## 1. Review basis

The inventory was cross-checked against these primary sources:

- [System Reference Document 5.2.1](https://www.dndbeyond.com/srd), especially
  Playing the Game, character creation, equipment, spellcasting, the Rules
  Glossary, hazards/environment, magic items, and monster stat blocks;
- [Foundry D&D5e activities](https://github.com/foundryvtt/dnd5e/wiki/Activities)
  and the current `foundryvtt/dnd5e` data models, which separate actors, items,
  activities, effects, and attack/check/damage/heal/save/summon/teleport/
  transform behavior;
- [Avrae Automation Reference](https://avrae.readthedocs.io/en/latest/automation_ref.html)
  and `avrae/avrae` automation effects, which demonstrate bounded target, roll,
  attack, check, save, damage, temporary-HP, counter, spell, condition, and
  effect operations;
- [PF2e Rule Elements](https://github.com/foundryvtt/pf2e/wiki/Quickstart-guide-for-rule-elements),
  used as prior art for selectors, predicates, provenance, stacking, grants,
  restrictions, and data-driven modifiers.

HDM does not copy any source's complete hierarchy. Foundry's broad `Item`
container deliberately combines equipment, classes, species, spells, and feats.
HDM keeps those reusable definitions separate while allowing a physical asset
to expose several compatible facets.

## 2. Separation rule

Every registry belongs to exactly one group:

1. **content definitions** — reusable rules/content selected or composed by the
   Master;
2. **world records** — particular things and facts in a campaign;
3. **runtime records** — stored operational/audit objects;
4. **engine capabilities and protocol enums** — executable operations and
   closed values understood by Python.

A concrete SRD spell is a `definition.spell`. Casting it uses a
`definition.activity`; one invocation is a `runtime.resolution`; committed
damage becomes an `event.damage.applied`. These are related objects at different
boundaries, not four names for the same class.

Transient requests, signals, contributions, deltas, rolls, segments, boundary
occurrences, pending child descriptors, publication manifests, and receipts are
protocol value kinds. They are neither world entities nor content-search results.

Literary Story projections are outside these canonical/current record classes.
`STORY/NARRATIVE` owns non-canonical literary records; literary chapter
boundaries are index groupings over those records, not world-record kinds.

A numeric timeline slot or local sparse sequence may be used as an ordering
**value** inside an explicit chronology domain. It is not an independently
identified world record and does not establish a campaign-global total order.

## 3. Reusable content-definition classes

### 3.1 Rules vocabulary

| ID | Boundary |
|---|---|
| `definition.ability` | Ability score and rules identity |
| `definition.skill` | Skill/check specialization |
| `definition.proficiency` | Proficiency category, rank, or group |
| `definition.size_category` | Rules-bearing size |
| `definition.creature_type` | Creature taxonomy used by rules/targets |
| `definition.movement_mode` | Walk, climb, fly, swim, burrow, or custom mode |
| `definition.sense` | Vision/sense capability |
| `definition.language` | Language or communication system |
| `definition.damage_type` | Damage identity and interactions |
| `definition.currency` | Denomination and conversion policy |
| `definition.equipment_property` | Weapon, armor, tool, or gear property |
| `definition.weapon_mastery` | Weapon-mastery behavior |
| `definition.spell_school` | Spell-school vocabulary |
| `definition.rest_policy` | Rest and recovery/time contract |

These are ruleset data. Python implements generic operations; an SRD seed later
supplies concrete abilities, damage types, conditions, and other definitions.

### 3.2 Actor construction and advancement

| ID | Boundary |
|---|---|
| `definition.actor_archetype` | Reusable PC/NPC/monster/stat-block baseline |
| `definition.species` | Species package and traits |
| `definition.background` | Background/origin package |
| `definition.class` | Class progression |
| `definition.subclass` | Class-linked specialization |
| `definition.advancement` | Reusable level/choice/grant progression step |
| `definition.feat` | Selectable feat package |
| `definition.feature` | Class, species, monster, item, or campaign feature |

`actor_archetype` covers monsters; a separate `monster` kind would duplicate
it. PC, NPC, companion, summon, and swarm are instance facets or roles.

### 3.3 Executable and state-bearing definitions

| ID | Boundary |
|---|---|
| `definition.spell` | Spell metadata plus Activities/effects |
| `definition.asset` | Item, vehicle, document, currency, or other asset |
| `definition.activity` | Bounded executable composition of primitives |
| `definition.resource` | Capacity, spending, and recovery policy |
| `definition.effect` | Effect template, duration, rules, and lifecycle |
| `definition.condition` | Named condition expressed through effects/rules |
| `definition.recipe` | Craft inputs, work/time, checks, and outputs |

A condition remains separately named because rules target it by identity. Its
execution uses generic effect machinery. A recipe is reusable content that may
be executed through several crafting Activities.

Rule Elements and Trigger Bindings are embedded mechanical value objects owned
by the Feature, Effect, Asset, equipment property, Feat, or Hazard
that grants them. They have no independent lifecycle or canonical ID. Their
exact contracts are defined in `RULE_ELEMENT_MODEL.md`.

### 3.4 World-building and host policy

| ID | Boundary |
|---|---|
| `definition.hazard` | Trap, poison, disease, curse, or environmental hazard |
| `definition.terrain` | Rules-bearing terrain properties |
| `definition.environment` | Light, weather, temperature, pressure, etc. |
| `definition.location_archetype` | Place/facility structure and capabilities |
| `definition.organization_archetype` | Organization structure and roles |
| `definition.mission_template` | Goal/stage/reward structure |
| `definition.contract_template` | Parties/terms/obligation structure |
| `definition.mode_profile` | Mechanics, information, and presentation policy |

Lore facts and scenes are campaign records rather than reusable engine content.
Chronology ordering lives in event/frontier/value contracts rather than a
standalone `world.timeline_marker`. Literary narrative records live under
non-canonical `STORY/NARRATIVE`; chapter boundaries are index groupings over that
layer.

## 4. World-record classes

| ID | Particular campaign object |
|---|---|
| `world.actor` | Character, NPC, creature, companion, summon, or swarm |
| `world.actor_group` | Party, roster, crowd, crew, or targetable group |
| `world.asset` | Item, stack, document, currency holding, or vehicle |
| `world.location` | Place in the world hierarchy |
| `world.connection` | Navigable/lockable link between locations |
| `world.zone` | Mechanically relevant bounded area |
| `world.organization` | Faction, guild, state, household, or institution |
| `world.relationship` | Typed relationship between world subjects |
| `world.contract` | Agreement, obligations, and state |
| `world.mission` | Goal, stages, and progression |
| `world.scene` | Current or historical narrative context |
| `world.encounter` | Bounded encounter/combat context |
| `world.hazard` | Placed or active hazard |
| `world.effect` | Effect instance attached to a subject/zone |
| `world.lore_fact` | Canonical proposition and truth status |
| `world.knowledge` | In-fiction epistemic state for a knower/proposition |

Inventories, HP, pools, occupancy, mission stages, chronology ordering values,
and similar owner-local state remain inside their owners unless a proven
independent identity/lifecycle requires a record.

Literary Chapters are not catalog records. `STORY/NARRATIVE` stores the
non-canonical literary records, while Chapter title/order/range is maintained by
Story index metadata over NARRATIVE record references.

## 5. Runtime-record classes

| ID | Stored operational/audit object |
|---|---|
| `runtime.session` | Session coordination/runtime identity evidence |
| `runtime.message` | Raw user/Master/tool message when retained for transcript/audit |
| `runtime.interaction` | Player input, plan/commands, and response boundary |
| `runtime.procedure` | Independent rules-procedure scope and sole owner of participant-local procedure ResourceState |
| `runtime.intent_plan` | Ordered material clauses from one player input |
| `runtime.command` | Accepted idempotent executable clause and mandatory descendant closure owner |
| `runtime.resolution` | Exactly one Activity invocation and its execution state |
| `runtime.continuation` | Portable state for one suspended Resolution generation |
| `runtime.mechanical_event` | Immutable committed runtime fact |
| `runtime.semantic_event` | Compact durable campaign-log projection |
| `runtime.resolution_trace` | Rolls, contributions, calculations, deltas |
| `runtime.checkpoint` | Recoverable state/frontier descriptor |
| `runtime.id_allocator` | Allocation state by identity policy |
| `runtime.maintenance_audit` | Diagnostic/control operation audit |
| `runtime.catalog_gap_report` | Non-executable missing-capability report |

`runtime.procedure` is an operational lifetime owner, not a generic workflow
engine. It is distinct from `world.encounter`, from one-Activity
`runtime.resolution`, and from `runtime.continuation`. An Encounter may be a
world referent for a Procedure, but it is not the universal owner of
procedure-local action/reaction/movement-style budgets.

`ExecutionSegment` remains an embedded protocol value addressed through its
owning command/resolution plus sequence. No `runtime.execution_segment` or
`runtime.resolution_chain` class is admitted in catalog version 1.6.0.

`runtime.dirty_record` and `runtime.publication_batch` are not admitted in
catalog 1.6.0. Dirty bookkeeping and publication transactions remain required
operational concepts, but Step 5.5/5.6 must prove independent identity/lifecycle
before any corresponding runtime record is re-admitted. `value.publication_manifest`
remains an embedded protocol value and does not by itself create a record owner.

Protocol values may be embedded in traces, receipts, commands, continuations or
checkpoints but do not receive independent record identity by default.

## 6. Structural facets

Facets may combine and never execute mechanics by themselves.

- Actors: `actor.player_character`, `actor.nonplayer_character`,
  `actor.companion`, `actor.summon`, `actor.swarm`, `actor.mount`,
  `actor.hireling`, `actor.temporary`.
- Assets: `asset.weapon`, `asset.armor`, `asset.shield`, `asset.ammunition`,
  `asset.consumable`, `asset.tool`, `asset.spellcasting_focus`,
  `asset.container`, `asset.wearable`, `asset.currency`, `asset.key`,
  `asset.document`, `asset.quest_item`, `asset.magic`, `asset.artifact`,
  `asset.vehicle`, `asset.mount_gear`, `asset.crafting_material`,
  `asset.food_drink`, `asset.poison`, `asset.trade_good`, `asset.treasure`,
  `asset.decoration`.
- Locations: `location.plane`, `location.world`, `location.region`,
  `location.settlement`, `location.district`, `location.site`,
  `location.structure`, `location.room`, `location.wilderness`,
  `location.dungeon`, `location.battlefield`, `location.abstract`.
- Organizations: `organization.faction`, `organization.government`,
  `organization.guild`, `organization.religious`,
  `organization.military`, `organization.business`, `organization.criminal`,
  `organization.family`, `organization.community`.

There is no `asset.misc` facet. An otherwise unclassified asset remains valid
with an empty or campaign-specific facet set. Creature type, species, class,
and allegiance are referenced definitions or mutable relationships.
An adventuring party is a `world.actor_group`; it is not duplicated as an
organization facet.

## 7. Activity intent families

| ID | Primary intent |
|---|---|
| `activity.perceive` | Directly or passively observe |
| `activity.search` | Actively locate, inspect, or investigate |
| `activity.communicate` | Speak, signal, write, or express |
| `activity.influence` | Persuade, deceive, intimidate, negotiate |
| `activity.perform` | Entertain, demonstrate, or present |
| `activity.move` | Reposition, travel, pursue, flee, climb, jump, swim |
| `activity.manipulate` | Open, close, lock, place, operate, break, alter |
| `activity.use_asset` | Drink, read, apply, consume, or operate an asset |
| `activity.transfer` | Take, give, drop, steal, pay, or exchange |
| `activity.attack` | Attempt harm through an attack |
| `activity.defend` | Dodge, guard, parry, take cover, or protect |
| `activity.control` | Grapple, shove, restrain, escape, reposition another |
| `activity.cast` | Cast a spell or conduct a ritual |
| `activity.activate_feature` | Invoke a feature or artifact capability |
| `activity.test` | Attempt an uncertain task not covered more specifically |
| `activity.assist` | Help another subject's activity |
| `activity.conceal` | Hide self, another subject, an object, or evidence |
| `activity.prepare` | Ready, aim, hold, or prepare a response |
| `activity.rest` | Execute a rules-bearing rest |
| `activity.craft` | Create, repair, dismantle, brew, or scribe |
| `activity.downtime` | Extended work, training, or research |
| `activity.wait` | Deliberately advance local time/procedure state |
| `activity.command` | Direct a companion, group, facility, or vehicle |
| `activity.composite` | Reusable rules-defined ordered composition |

A host-planned natural-language turn remains an ordered
`runtime.intent_plan`; it does not create a permanent composite definition.

Saving throws, damage, healing, effects, and resource changes are resolver
operations or consequences rather than player-intent families.

## 8. Capability deduplication

The machine seed contains the exact closed IDs for operations, transitions,
events, resources, effects, rules, targets, areas, ranges, triggers, time,
stacking, state machines, publication values, knowledge, truth status, and Step-3
execution outcomes/protocol values.

- A condition uses `op.create_effect` with a `definition.condition`; there is
  no second condition-mutation primitive.
- Summoning uses `op.create_entity`; enchantment uses an effect on an asset.
- `rule.cap`/`rule.floor` are `rule.set_maximum`/`rule.set_minimum`.
- Spell slots, charges, HP, and feature uses are content definitions over
  generic resource mechanics.
- Intent mapping outcome and later execution state remain separate axes.
- Transitions are accepted commands; events are committed facts.
- Root command closure is not duplicated by a separate ResolutionChain class.
- Chronology is not duplicated by a standalone timeline-marker world owner.
- Generic dirty/publication record identities are not pre-admitted before their
  Step-5 lifecycle slices prove a need.

## 9. D&D/SRD seed coverage

A separate SRD 5.2.1 seed must later populate at least:

- abilities, skills, proficiencies, sizes, creature types, movement modes,
  senses, languages, damage types, and conditions;
- species, backgrounds, classes, subclasses, advancements, feats, features,
  spells, and monster archetypes;
- coins, weapons, masteries, armor, tools, gear, mounts, vehicles, magic items,
  and recipes;
- actions, bonus actions, reactions, rests, travel/exploration, environments,
  poisons, traps, curses/contagions, and encounter rules.

Concrete SRD names and mechanics do not belong in the engine capability seed.

## 10. Extension test

A later addition must answer:

1. Is it reusable content, a world instance, a runtime record, or a protocol/
   executable value?
2. Does an existing class plus facets/capabilities already express it?
3. Does it need independent identity and lifecycle?
4. Does it introduce Python behavior or only validated data?

New IDs require a catalog version change. Existing IDs are never silently
repurposed.
