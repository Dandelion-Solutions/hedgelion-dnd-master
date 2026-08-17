# HDM Engine Catalog — Model and Initial Taxonomy

Status: **WORKING PROTOTYPE / REVIEWED INVENTORY**

Target: `feature/mechanical-runtime-hot-state`

Companion document: `ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md`

Normative class inventory: `ARCHITECTURE/CATALOG_INVENTORY.md`

Universal record contracts: `ARCHITECTURE/CATALOG_CONTRACTS.md`

Minimum entity structures: `ARCHITECTURE/ENTITY_STRUCTURES.md`

Machine-readable registry: `CATALOG/core-catalog.json` version `1.1.0`

## 1. Purpose

The catalog defines the vocabulary that the LLM Master may select, compose, and
instantiate. It serves three consumers:

1. the Master, as a compact map from natural language to supported structures;
2. the deterministic runtime, as validated definitions and capability IDs;
3. SQLite/campaign loaders, as seed data and versioned reference data.

The catalog is not a list of every sword, spell, sentence, or possible player
idea. Such a list cannot be complete. It is a catalog of stable classes,
facets, primitives, and policies from which concrete content can be described.

## 2. Four layers that must remain distinct

### 2.1 Engine capability registry

This layer is closed for a given engine version. It contains executable meaning:

- activity primitives;
- domain-transition kinds;
- event kinds;
- rule-element operations;
- target/area contracts;
- resource and duration semantics;
- supported failure and suspension behavior.

Adding an entry here may require Python, schema, migration, and tests. The LLM
cannot invent a capability ID during gameplay.

### 2.2 Content-definition catalog

This layer is extensible data. It contains reusable definitions and campaign
extensions composed from registered capabilities:

- activities and abilities;
- actor/creature archetypes;
- items, weapons, artifacts, decorations, tools, and consumables;
- conditions and effects;
- resources;
- locations, scenes, organizations, missions, and contracts;
- lore facts, knowledge restrictions, timeline markers, and chapters.

The engine ships standard definitions. A campaign may create or modify content
without changing Python as long as the result validates against registered
capabilities.

### 2.3 World-record kinds

World records are canonical or local instances: a particular actor, item,
location, organization, contract, mission, lore fact, chapter, scene, encounter,
or timeline marker. Their kind IDs are registered for validation and routing,
but the records themselves are campaign state rather than reusable catalog
definitions.

### 2.4 Runtime-record kinds

Runtime records include sessions, intent plans, resolutions, events, traces,
dirty records, publication batches, and maintenance audit entries. Their kind
IDs are registered because storage and APIs need stable schemas. They are not
content selectable by the Master and never appear as catalog search results.

## 3. Catalog strata

Definition origin is explicit in its catalog layer/path and loader context; it
is not repeated in every definition record:

| Origin | Meaning | May redefine engine semantics? |
|---|---|---:|
| `engine` | Built into the HDM release | Yes, through reviewed engine work |
| `ruleset` | D&D/SRD or another selected rules profile | No |
| `campaign` | Canonical campaign-specific definition | No |
| `session` | Temporary local definition | No; not durable until promoted |

Resolution order is explicit and never based on filename accident:

```text
engine capability registry
  -> selected ruleset definitions
  -> campaign definitions
  -> session-local definitions
```

Definitions compose registered behavior. HDM does not use a universal
inheritance or override mechanism.

## 4. Universal definition envelope

The accepted minimum envelope is defined by `CATALOG_CONTRACTS.md` and
`SCHEMAS/catalog-definition.schema.json`:

```json
{
  "id": "campaign.moonlace_brooch",
  "kind": "definition.asset",
  "name": {"en": "Moonlace Brooch", "ru": "Брошь лунного кружева"},
  "tags": ["jewelry", "moon"],
  "facets": ["asset.wearable", "asset.decoration", "asset.artifact"],
  "data": {}
}
```

Required fields are deliberately small:

- `id` is stable and unique within the resolved catalog;
- `kind` selects the definition schema;
- `name` stores English and at most one campaign/player language;
- `data` is kind-specific validated content.

Optional fields are:

- `tags` support retrieval but never grant mechanics;
- `facets` classify compatible aspects without forcing one inheritance tree.

## 5. Universal instance envelope

The accepted minimum envelope is defined by `CATALOG_CONTRACTS.md` and
`SCHEMAS/world-record.schema.json`:

```json
{
  "id": "asset-00042",
  "kind": "world.asset",
  "definition_id": "campaign.moonlace_brooch",
  "state": {}
}
```

Definitions answer what a thing can be. Instances answer which thing exists and
its current state. Current HP, ownership, charges, location, active effects, and
knowledge are instance state, not catalog data.

## 6. Classification uses facets, not exclusive subclasses

One object may naturally be several things:

```text
Moonlace Brooch
  asset.wearable
  asset.decoration
  asset.artifact
  grants activity.moonlight_pulse
  attaches rule element re.moonlace_rider
```

This avoids choosing whether the brooch is “really” jewelry, an artifact, or a
magic tool. Facets provide classification. Capabilities provide behavior.

Facets alone never alter state. For example, `asset.weapon` makes an item
discoverable as a weapon, but an attack Activity and validated damage profile
provide its mechanics.

## 7. Definition, world, and runtime kind registries

> **Inventory notice:** the exact reviewed class and capability IDs are defined
> by `CATALOG_INVENTORY.md` and `core-catalog.json`. The tables in sections
> 7–18 below record the earlier design derivation and examples. They are
> non-normative where an ID differs from catalog version 1.1.0. This preserves
> the reasoning without allowing the prototype lists to override the reviewed
> inventory.

### 7.1 Content-definition kinds

| ID | Reusable definition |
|---|---|
| `definition.actor_archetype` | Creature/NPC/PC baseline or template |
| `definition.asset` | Item, weapon, artifact, tool, document, etc. |
| `definition.activity` | Executable composition of registered primitives |
| `definition.resource` | Capacity, spending and recovery policy |
| `definition.effect` | EffectInstance template and duration policy |
| `definition.condition` | Ruleset condition expressed through effects/rules |
| `definition.rule_element` | Pure conditional Contribution definition |
| `definition.trigger_binding` | Registered signal/event to reaction/follow-up mapping |
| `definition.location_archetype` | Reusable location/zone properties |
| `definition.mode_profile` | Enabled mechanics and presentation profile |

### 7.2 World-record kinds

| ID | Purpose | Typical mutable state |
|---|---|---|
| `world.actor` | Particular PC, NPC, creature, companion | HP, resources, effects, location, inventory |
| `world.asset` | Particular physical or conceptual object | owner, location, charges, condition |
| `world.location` | Particular place or mechanically relevant zone | occupants, links, hazards, state |
| `world.organization` | Faction, guild, government, group | relationships, resources, status |
| `world.contract` | Agreement with state and parties | status, obligations, fulfillment |
| `world.mission` | Goal/progression record | status, stages, dependencies |
| `world.scene` | Active narrative/mechanical context | participants, focal location, status |
| `world.encounter` | Bounded mechanical procedure | participants, initiative, phase |
| `world.lore_fact` | Canonical proposition and knowledge policy | truth status, audience, revelation |
| `world.chapter` | Human-readable narrative/history block | references, chronology span, visibility |
| `world.timeline_marker` | Abstract gameplay chronology placement | slot, label, scope |

Actor facets initially include PC, NPC, creature, companion, summon, swarm, and
vehicle operator. These remain roles/tags unless their distinction changes a
registered rule.

### 7.3 Runtime-record kinds

| ID | Internal purpose |
|---|---|
| `runtime.session` | HOT runtime identity, frontier and transport mode |
| `runtime.intent_plan` | Complete ordered interpretation of one player message |
| `runtime.resolution` | Active/completed/suspended Activity invocation |
| `runtime.mechanical_event` | Immutable committed runtime fact |
| `runtime.resolution_trace` | Inputs, rolls, contributions, calculations and deltas |
| `runtime.dirty_record` | HOT/canonical divergence and cause |
| `runtime.publication_batch` | Prepared/acknowledged durable projection |
| `runtime.maintenance_audit` | Non-gameplay diagnostic/control operation record |

These records have schemas and storage contracts, but they are excluded from
Master content selection and campaign-authored catalog extensions.

## 8. Initial asset-facet catalog

Assets may combine any compatible facets:

| ID | Meaning |
|---|---|
| `asset.weapon` | Can source one or more attack Activities |
| `asset.armor` | Contributes defense/equipment rules |
| `asset.shield` | Defensive item with shield-specific selectors |
| `asset.ammunition` | Consumable or tracked attack input |
| `asset.consumable` | Has consumption/uses semantics |
| `asset.tool` | Enables or modifies checks/Activities |
| `asset.container` | May contain other assets |
| `asset.wearable` | Can be worn when availability matters |
| `asset.decoration` | Primarily aesthetic/social/narrative |
| `asset.currency` | Fungible denomination/value asset |
| `asset.key` | Grants access or satisfies a predicate |
| `asset.document` | Carries readable information/authority |
| `asset.quest` | Mission-significant asset |
| `asset.artifact` | Unique/high-significance rules-bearing asset |
| `asset.vehicle` | Transport/platform asset |
| `asset.material` | Crafting/ritual/component material |
| `asset.misc` | No more specific facet is mechanically needed |

Ownership normally implies immediate usability. The engine does not track
`in_hand`, `in_backpack`, or similar microstates by default. Explicit blockers
such as bound hands, inaccessible storage, loss, breakage, or separation may
make an owned asset unavailable.

## 9. Activity-family catalog

An Activity family describes intent and routing. Executable behavior comes from
its ordered registered primitives.

| ID | Typical natural-language intent |
|---|---|
| `activity.observe` | look, listen, inspect without a contested check |
| `activity.communicate` | speak, signal, ask, threaten as expression |
| `activity.influence` | persuade, deceive, intimidate, negotiate |
| `activity.move` | go, approach, retreat, climb, jump, travel |
| `activity.manipulate` | open, close, lock, unlock, press, pull, place |
| `activity.use_asset` | drink, activate, read, play, apply, consume |
| `activity.transfer` | give, take, drop, pay, steal, exchange |
| `activity.attack` | armed, unarmed, spell, improvised attack |
| `activity.defend` | dodge, guard, parry, take cover |
| `activity.check` | attempt a task with uncertain outcome |
| `activity.save` | resist an imposed effect |
| `activity.heal` | restore HP or related resource |
| `activity.cast_or_activate` | invoke a spell, feature, artifact, ritual |
| `activity.apply_effect` | create a condition/buff/debuff/zone |
| `activity.manage_resource` | spend, restore, reserve, recharge |
| `activity.rest` | short/long/custom recovery procedure |
| `activity.assist` | help another action or grant a contribution |
| `activity.search` | actively locate hidden information/entities |
| `activity.stealth` | hide, sneak, conceal an action/object |
| `activity.craft` | make, repair, dismantle, prepare |
| `activity.environment` | interact with hazards, mechanisms, terrain |
| `activity.composite` | rules-defined multi-step Activity |

Communication and stated intent are still gameplay interactions even when they
produce no mathematical change. They may resolve to `OBSERVED` rather than being
dropped from the interaction log.

## 10. Activity primitive catalog

The first capability registry should support these bounded primitives:

| ID | Reads/RNG | Possible mutation |
|---|---|---|
| `op.select_targets` | entity/context lookup | none |
| `op.roll` | DiceEngine | none until owning segment commits |
| `op.check` | actor/target/rules + roll | exported outcome |
| `op.save` | actor/target/rules + roll | exported outcome |
| `op.attack` | actor/target/defense + roll | exported hit/critical outcome |
| `op.damage` | damage pipeline + optional rolls | HP/temp HP and related events |
| `op.heal` | healing pipeline | HP/resource |
| `op.temp_hp` | value/rules | temporary HP |
| `op.consume_resource` | resource state | resource amount/use gate |
| `op.restore_resource` | resource state | resource amount/use gate |
| `op.transfer_asset` | ownership/location | owner, inventory, location |
| `op.transfer_currency` | balances/denomination | balances/events |
| `op.move_entity` | location/reachability context | location/occupancy |
| `op.create_effect` | effect definition/targets | EffectInstance |
| `op.remove_effect` | EffectInstance | effect status |
| `op.set_condition` | condition rules | condition/effect state |
| `op.branch` | typed prior result | selects finite branch |
| `op.choice` | bounded options | suspends Resolution |
| `op.reaction_window` | trigger bindings | suspends Resolution |
| `op.emit_fact` | validated semantic payload | event/fact within commit |
| `op.schedule_followup` | registered Activity reference | bounded child Resolution |

An unarmed attack uses `op.attack` with a registered unarmed profile and no
asset. A body part is not an inventory item.

## 11. Multiple intents in one player message

The Master must not force one natural-language message to contain one action.
It first produces an ordered `IntentPlan` containing every material clause:

```json
{
  "message_id": "turn-00042",
  "intents": [
    {"order": 1, "verb": "leave", "object": "item.potion", "status": "mapped"},
    {"order": 2, "verb": "move", "destination": "location.hall", "status": "mapped"},
    {"order": 3, "verb": "lock", "object": "door.room_hall", "status": "mapped"}
  ]
}
```

The host normally submits separate ordered ActionRequests, stopping only when:

- a request fails or requires clarification;
- a choice/reaction suspends the plan;
- a prior result invalidates a later intent;
- action-economy or time-budget rules prohibit continuing.

A rules-defined composite Activity may resolve the plan as one Activity. The
player is asked to clarify only genuine ambiguity, not merely because several
clear actions appeared in one message.

Each intent clause is recorded as `mapped`, `narrative_only`,
`clarification_required`, or `unsupported`. No clause may disappear silently.

## 12. Domain-transition catalog

These transitions represent already-adjudicated deterministic world changes.
They share revision, atomicity, events, dirty tracking, and publication policy
with Activities, but require no invented check or roll.

| ID | Core payload | Default durability |
|---|---|---|
| `transition.asset_transfer` | asset, from, to/location | IMMEDIATE |
| `transition.asset_status` | asset, status/value | policy-defined |
| `transition.currency_transfer` | denomination/value, from, to | IMMEDIATE |
| `transition.location_change` | entity, from, to | focal: IMMEDIATE; tactical: BATCH |
| `transition.contract_state` | contract, previous/new state, parties | IMMEDIATE |
| `transition.companion_state` | actor, relationship/status | IMMEDIATE |
| `transition.mission_state` | mission, stage/status | critical: IMMEDIATE |
| `transition.entity_promotion` | entity, new canonicality | IMMEDIATE |
| `transition.relationship_change` | parties, typed delta/value | policy-defined |
| `transition.lore_commit` | fact, truth/knowledge policy | policy-defined |
| `transition.chapter_append` | chapter metadata/content reference | BOUNDARY |
| `transition.scene_change` | previous/new scene and roots | BOUNDARY |
| `transition.timeline_place` | marker and abstract slot | BOUNDARY |
| `transition.event_time_advance` | active procedure and budget delta | BATCH |

The union is versioned and closed per engine version. It is not JSON Patch.

## 13. Mechanical-event catalog

Events are immutable committed facts. Initial families include:

- `event.activity.completed`, `event.activity.rejected`;
- `event.attack.hit`, `event.attack.missed`, `event.attack.critical`;
- `event.check.resolved`, `event.save.resolved`;
- `event.damage.applied`, `event.healing.applied`, `event.temp_hp.changed`;
- `event.resource.consumed`, `event.resource.restored`;
- `event.effect.created`, `event.effect.expired`, `event.effect.removed`;
- `event.condition.applied`, `event.condition.removed`;
- `event.asset.transferred`, `event.asset.status_changed`;
- `event.currency.transferred`;
- `event.location.changed`;
- `event.contract.changed`, `event.mission.changed`;
- `event.companion.changed`, `event.relationship.changed`;
- `event.entity.promoted`;
- `event.lore.committed`, `event.lore.revealed`;
- `event.chapter.appended`, `event.scene.changed`;
- `event.timeline.placed`, `event.event_time.advanced`.

Every event minimally records:

```json
{
  "event_id": "event-0000001234",
  "event_kind": "event.asset.transferred",
  "schema_version": 1,
  "causation_id": "resolution-00000088",
  "correlation_id": "turn-00042",
  "entity_ids": ["item.potion", "actor.hero", "actor.goblin"],
  "before": {},
  "after": {},
  "durability_class": "HARD"
}
```

## 14. Resource catalog

| ID | Semantics |
|---|---|
| `resource.hp` | bounded current/max health |
| `resource.temp_hp` | non-stacking temporary health profile |
| `resource.spell_slot` | level/keyed pool |
| `resource.hit_die` | typed recovery pool |
| `resource.charge` | item/feature charges |
| `resource.use` | limited uses with recovery policy |
| `resource.action` | active-procedure action economy |
| `resource.bonus_action` | active-procedure action economy |
| `resource.reaction` | active-procedure reaction availability |
| `resource.movement` | optional event-local movement budget |
| `resource.currency` | denomination/balance or fungible asset projection |
| `resource.custom_counter` | validated bounded counter without new behavior |

Resource definitions specify minimum, maximum or capacity expression, recovery
policy, spending timing, and durability policy.

## 15. Effect and condition catalog

An EffectInstance is state with duration and attached Rule Elements. Initial
effect facets are:

- `effect.condition` — named rules condition;
- `effect.modifier` — temporary stat/check/attack/damage contribution;
- `effect.damage_over_time` and `effect.healing_over_time`;
- `effect.transformation` — replaces/adds bounded facets or capabilities;
- `effect.zone` — applies by area/location membership;
- `effect.concentration` — carries concentration lifecycle;
- `effect.equipment_passive` — active while availability predicate holds;
- `effect.narrative` — tracked fiction with no numeric contribution.

Condition names such as blinded, restrained, frightened, poisoned, prone, and
unconscious belong to the selected ruleset definition catalog. The engine
capability is the generic condition/effect machinery.

## 16. Rule-element catalog

Rule Elements are pure contributions. Initial operations are:

- `rule.add_flat`;
- `rule.add_dice`;
- `rule.grant_advantage`, `rule.grant_disadvantage`;
- `rule.set_minimum`, `rule.set_maximum`, `rule.cap`, `rule.floor`;
- `rule.multiply` with explicit phase and rounding;
- `rule.override` for narrowly registered selectors;
- `rule.add_damage_component`;
- `rule.resistance`, `rule.immunity`, `rule.vulnerability`;
- `rule.adjust_cost`;
- `rule.grant_activity`, `rule.restrict_activity`;
- `rule.adjust_target`, `rule.adjust_range`;
- `rule.adjust_duration`;
- `rule.usage_gate` for once-per-turn/rest/etc.

Every contribution records selector, phase, predicate, value, stacking group,
source, and usage policy. Rules cannot mutate state or call arbitrary Activities.

## 17. Target, position, and area catalog

Target contracts include self, one entity, bounded multiple entities, explicit
entity list, location, object, and area membership. Initial area shapes include
line, cone, sphere, cube, cylinder, and radius around source/point.

Exact positions/ranges exist only when mechanics require them. Otherwise the
scene may use qualitative reachability such as `same_location`, `near`,
`reachable`, or `not_reachable`. The catalog must not turn ordinary narrative
play into mandatory tactical geometry.

## 18. Chronology and duration catalog

HDM keeps two time domains:

### 18.1 Gameplay chronology

The gameplay timeline preserves ordering and rough comparison, not a simulated
calendar. Canonical markers use abstract numeric slots normally allocated in
steps of ten:

```text
00430  coronation
00440  tavern fight
```

An intermediate marker may use 00431–00439. Lore about events before active
play remains lore unless it must be placed for gameplay causality.

### 18.2 Event-local time

An active procedure may use narrative/mechanical budgets such as round, turn,
minute, hour, scene, until-rest, until-event, or finite uses. The runtime spends
time only through registered Activity/duration policies. The LLM may adjudicate
a duration estimate where the rules leave it fictional, but the estimate must be
explicit in the request/trace rather than hidden arithmetic.

Real wall-clock time does not automatically advance singleplayer mechanics.
Multiplayer concurrency is ordered by committed canonical state and publication
frontier, not by pretending chat latency is game time.

## 19. Lore, knowledge, and chapter catalog

Public lore requires no visibility annotation. Restricted knowledge is explicit:

```json
{
  "fact_id": "lore.amulet_origin",
  "truth_status": "established",
  "visibility": {
    "mode": "restricted",
    "known_by": ["actor.npc_archivist"],
    "revealed_to": []
  }
}
```

The runtime can validate the policy and select allowed context. It cannot prove
that an LLM-generated paraphrase does not leak a secret. Strict information
isolation is therefore an optional game mode with stronger context filtering,
not mandatory overhead for every adventure.

Chapters are large human-readable narrative/history blocks with metadata:

- chapter ID/title/order;
- covered timeline slots/event frontier;
- referenced entities, locations, missions, and lore facts;
- visibility/restriction references;
- source checkpoint/revision;
- text body.

Chapters are suitable both for fast LLM loading and repository browsing.

## 20. LLM mapping contract

The Master is responsible for classification, but it must produce inspectable
output before mechanics:

1. preserve the exact player message;
2. segment every material intent clause;
3. resolve actor, targets, assets, and context references;
4. select an existing Activity or compose allowed primitives;
5. mark unmatched clauses instead of dropping them;
6. submit typed requests;
7. narrate only from receipts plus non-mechanical adjudication.

Turn identity is host-owned. Runtime state stores only `last_turn_number` as an
integer. Before accepting a new ordinary message, Python increments it and
formats `turn-{number:05d}`. No `next_turn` field is persisted; it is derived by
adding one. Maintenance commands do not increment the counter.

Mapping outcomes are:

| Outcome | Meaning |
|---|---|
| `exact` | Existing definition matches directly |
| `composed` | Expressed with registered primitives/data |
| `narrative_only` | Fictional response with no mechanical mutation |
| `clarification_required` | Material ambiguity prevents safe mapping |
| `unsupported` | Required capability is absent |

`unsupported` must never be rewritten as a fictional game rule. For example,
an experimental runtime that lacks unarmed attacks reports a capability gap; it
does not tell the player that every attack requires a weapon.

## 21. Creating custom content

When the player introduces a custom item, creature, action, effect, or lore
element, the Master:

1. chooses entity kind and compatible facets;
2. binds existing Activities/Rule Elements/resources;
3. proposes natural values from the selected ruleset and fictional description;
4. validates the definition;
5. creates a campaign instance or definition;
6. reports `unsupported` for any semantic part outside engine capabilities.

Example custom artifact:

```json
{
  "id": "campaign.moonlace_brooch",
  "kind": "definition.asset",
  "name": {
    "en": "Moonlace Brooch",
    "ru": "Брошь лунного кружева"
  },
  "tags": ["jewelry", "moon"],
  "facets": ["asset.wearable", "asset.decoration", "asset.artifact"],
  "data": {
    "activity_ids": ["activity.moonlight_pulse"],
    "rule_elements": ["re.moonlace_radiant_rider"],
    "resources": [{"kind": "resource.use", "capacity": 1, "recovery": "long_rest"}]
  }
}
```

If all referenced operations already exist, this needs no Python handler.

## 22. Catalog-gap reports

A missing capability or useful reusable definition may produce a bounded
`CatalogGapReport` for later submission to the public engine repository:

```json
{
  "schema_version": 1,
  "engine_version": "0.7",
  "category": "activity_primitive",
  "summary": "Support unarmed attack profiles",
  "observed_phrase": "отвешиваю ему тумака",
  "attempted_mapping": "activity.attack with asset_id null",
  "missing_capability": "unarmed attack profile",
  "workaround": null
}
```

The report is diagnostic data, not executable content. Publication requires an
explicit user/host action and must remove campaign secrets or personal data.

## 23. Machine-readable seed and SQLite loading

`CATALOG/core-catalog.json` is the initial engine seed. It contains IDs and
descriptive routing metadata, not executable Python. A loader may import it into
SQLite reference tables keyed by `(catalog_version, registry, id)`.

Startup behavior:

1. validate the catalog against `SCHEMAS/core-catalog.schema.json`;
2. verify supported catalog version;
3. import/upsert the immutable engine registry transactionally;
4. compile selected ruleset/campaign definitions separately;
5. reject unknown capability references before gameplay.

The human document remains authoritative for design boundaries. The JSON seed is
authoritative for the initial registered IDs once implementation begins.

## 24. Deliberate limits of the prototype

- The initial seed catalogs capability families, not full D&D content.
- Exact D&D 2024/SRD definitions belong to a later ruleset catalog.
- The catalog does not authorize arbitrary scripts or expressions.
- Game modes may disable whole mechanical families for quick/narrative play.
- Switching from a narrative-only campaign to strict canonical D&D mechanics is
  not guaranteed when earlier state lacks required definitions and history.
- Performance work begins only after catalog validation and runtime traces are
  measured in the vertical slice.
