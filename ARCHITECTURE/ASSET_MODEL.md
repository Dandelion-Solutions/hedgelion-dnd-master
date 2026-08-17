# HDM Asset Model

Status: **AGREED ARCHITECTURE**

Target: `feature/mechanical-runtime-hot-state`

Related contracts:

- `ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `ARCHITECTURE/ACTOR_MODEL.md`.

Machine-readable schemas:

- `SCHEMAS/asset-definition-data.schema.json`;
- `SCHEMAS/world-asset-state.schema.json`.

## 1. Scope

An asset is a particular physical or conceptual object that can be owned,
carried, placed, transferred, used, damaged, transformed, or destroyed. The
same model covers weapons, armor, shields, ammunition, consumables, tools,
containers, clothing, currency, keys, documents, quest items, magic items,
artifacts, vehicles, crafting materials, food, trade goods, treasure, and
decorations.

HDM does not define a separate record kind for each of those categories. A
reusable `definition.asset` combines compatible structural facets and
registered capabilities. A `world.asset` represents one particular object or
one homogeneous stack in the campaign.

Facets classify an asset but never execute mechanics. Damage, healing, checks,
activation, transfer, resource spending, effects, and transformations are
performed through Activities and registered runtime operations.

### 1.1 Research basis

The model was checked against:

- [D&D SRD 5.2.1](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf),
  especially equipment, weapons and weapon properties, armor, tools,
  adventuring gear, containers, mounts and vehicles, magic-item activation,
  attunement, charges, improvised weapons, and breaking objects;
- the current [Foundry D&D5e](https://github.com/foundryvtt/dnd5e) item and
  Activity design, including weapon, equipment, consumable, tool, loot, and
  container records;
- the already accepted HDM catalog inventory and universal record contracts.

HDM retains D&D rules-bearing distinctions but does not copy VTT sheet,
presentation, compendium, or item-subclass structures. SRD content used by a
future ruleset seed remains subject to its CC-BY-4.0 attribution requirement.

## 2. Definition and instance boundary

`definition.asset` contains stable reusable facts:

- physical characteristics and reference value;
- equipment properties and handling requirements;
- Activities, resources, and effects provided by the asset;
- capacity, stacking, attunement, and durability policy.

`world.asset` contains mutable facts about a particular object or stack:

- current placement or controller;
- quantity;
- whether it is currently held or worn;
- current attunement;
- current resource and durability values;
- an explicit access obstacle when ordinary possession is insufficient.

Transaction price, ownership history, previous locations, and transformations
belong to events. Knowledge about an asset belongs to `world.lore_fact` and
`world.knowledge`; it is not represented by an `identified` boolean.

## 3. Minimum definition structure

No field inside `definition.asset.data` is required. A decorative stone,
letter, or plot token may be valid without weight, value, or executable
mechanics.

```json
{
  "id": "ruleset.asset.longsword",
  "kind": "definition.asset",
  "name": {
    "en": "Longsword",
    "ru": "Длинный меч"
  },
  "facets": ["asset.weapon"],
  "data": {
    "physical": {
      "weight": 3
    },
    "value": {
      "amount": 15,
      "currency_id": "currency.gp"
    },
    "property_ids": ["equipment_property.versatile"],
    "activity_ids": ["activity.longsword_attack"]
  }
}
```

Expected fields are:

| Field | Purpose |
|---|---|
| `physical` | Weight and, when mechanically relevant, size |
| `value` | Ruleset reference value, not a completed transaction price |
| `rarity` | Ruleset rarity label when the content uses rarity |
| `property_ids` | References to `definition.equipment_property` |
| `activity_ids` | Activities the asset provides or enables |
| `resource_ids` | Charge, dose, fuel, or other resource definitions |
| `effect_ids` | Passive or applied effect definitions |
| `handling` | Persistent hand occupancy and use requirement |
| `capacity` | Container capacity constraints |
| `stack` | Whether interchangeable instances may form a stack |
| `attunement` | Whether attunement is required and its prerequisites |
| `durability` | Lazy object-durability policy |
| `details` | Arbitrary non-mechanical JSON maintained by the LLM |

Absent fields mean unknown, inapplicable, or unnecessary. Empty placeholder
objects and arrays are not persisted.

### 3.1 Physical characteristics

```json
{
  "physical": {
    "weight": 3,
    "size_id": "size.medium"
  }
}
```

`weight` uses the canonical unit of the selected ruleset. HDM does not repeat a
unit string on every definition. `size_id` is stored only when size affects a
rule. Material, dimensions, color, and similar descriptive facts remain in
`details` until a concrete mechanic justifies a typed field.

### 3.2 Reference value

```json
{
  "value": {
    "amount": 15,
    "currency_id": "currency.gp"
  }
}
```

`amount` is a non-negative integer in the referenced denomination. Exact
arithmetic uses denominations rather than floating-point conversion. The
actual price paid is produced by a transfer, trade, or contract resolution and
is recorded in its event.

### 3.3 Properties, Activities, resources, and effects

`property_ids` references named ruleset properties such as finesse, light,
heavy, loading, reach, or stealth disadvantage. Individual booleans for every
possible equipment property are not added to the asset schema.

`activity_ids` supplies bounded executable behavior. Attack damage and range,
healing, checks, activation, target selection, and costs belong to the
Activity rather than being duplicated in the asset.

`resource_ids` supplies charge, dose, fuel, and use pools. Current values belong
to the world instance. Physical interchangeable units such as arrows use
`quantity`; internal uses of one physical object use resources.

`effect_ids` supplies effects that the asset can apply or that become active
while their predicates are true. The effect itself determines whether it
requires holding, wearing, attunement, activation, or another condition. This
avoids duplicating passive bonuses directly in the asset.

### 3.4 Handling and hands

```json
{
  "handling": {
    "held_hands": 1,
    "use_hands": 2
  }
}
```

`held_hands` is the minimum persistent hand occupancy when the item is in
`held` state. `use_hands` is the number of hands required when using its normal
Activity. Both are optional non-negative integers.

A two-handed asset does not need separate one-handed and two-handed Activities.
It may be carried or held in one hand, but its normal use requires two hands.
An Activity may override `use_hands` only when that particular operation has a
genuinely different requirement. A potion, for example, can require one hand
temporarily without remaining held afterward.

### 3.5 Capacity

```json
{
  "capacity": {
    "weight": 30,
    "volume": 1
  }
}
```

Capacity describes limits, never contents. Contents are derived by reverse
lookup of `world.asset.container_asset_id`. A capacity dimension is implemented
only when the selected ruleset or campaign uses it.

### 3.6 Stacking

```json
{
  "stack": {
    "allowed": true
  }
}
```

A stack contains interchangeable units with identical definition and mutable
state. A poisoned, named, damaged, or otherwise distinct arrow cannot remain in
the same stack as ordinary arrows. A maximum stack size is not modeled until a
real rule requires it.

### 3.7 Attunement

```json
{
  "attunement": {
    "required": true,
    "allowed_class_ids": ["class.paladin"]
  }
}
```

The definition contains the requirement and its prerequisites. The instance
contains the actor currently attuned to it. The runtime checks the ruleset
limit, including the D&D limit of no more than three attuned magic items per
actor. A general prerequisite-expression language is deferred until a concrete
need exceeds simple typed fields or existing predicates.

### 3.8 Durability policy

```json
{
  "durability": {
    "profile": "fragile"
  }
}
```

Durability is lazy. Most assets do not receive calculated AC or HP until they
become a target of damage or a source in a risky impact. Ruleset profiles such
as `fragile`, `ordinary`, `resilient`, and `structural` may supply defaults from
size and material. A definition may instead provide explicit values where the
rules require them.

## 4. Minimum world-asset structure

`world.asset.state` may be empty when its definition provides all known facts.

```json
{
  "id": "asset-00042",
  "kind": "world.asset",
  "definition_id": "ruleset.asset.longsword",
  "state": {}
}
```

Expected state fields are:

| Field | Purpose |
|---|---|
| `owner_actor_id` | Direct actor inventory/control |
| `container_asset_id` | Containment in another asset |
| `location_id` | Direct placement in the world |
| `quantity` | Number of interchangeable units in a stack |
| `equipment` | Persistent `held` or `worn` state |
| `attuned_actor_id` | Current attunement relation |
| `resources` | Current values of definition-provided resources |
| `durability` | Materialized current durability |
| `access` | Explicit exceptional access obstacle |
| `details` | Instance-specific non-mechanical JSON |

### 4.1 Placement invariant

At most one of these fields may be present:

```text
owner_actor_id
container_asset_id
location_id
```

An asset is either directly controlled by an actor, contained by another
asset, or directly placed in a location. Physical position and possession of a
contained asset are derived by traversing its container chain. Container cycles
are invalid.

`owner_actor_id` means current inventory/control, not legal title. Legal
ownership, disputed property, loans, and theft are represented by contracts,
relationships, lore, and events when relevant.

### 4.2 Ordinary access

An asset is ordinarily accessible when it is directly controlled by an actor or
is inside that actor's accessible container chain. Accessibility is derived and
cached; it is not copied into every asset.

Only an exceptional obstacle is persisted, for example:

```json
{
  "access": "blocked"
}
```

Locks, seals, separation, restraint, and similar causes remain in the relevant
object/effect/details and are interpreted by the Activity preflight. HDM does
not require the player to narrate opening a backpack, drawing a potion, closing
the backpack, or returning an ordinary object after use.

### 4.3 Equipment state

```json
{
  "equipment": {
    "mode": "held"
  }
}
```

The initial persistent modes are only:

- `held` — occupies the definition's `held_hands`;
- `worn` — worn on the body and subject to applicable effects or requirements.

Absence of `equipment` means the item is merely carried or stored. `carried`,
`stowed`, and `ready` are derived concepts and are not persisted. Deployment in
a location is expressed with `location_id` and, when mechanically relevant, a
hazard or effect record.

HDM does not initially model detailed body slots. Rules that prevent combining
particular worn items are validated through their properties, Activities,
effects, or attunement requirements when needed.

### 4.4 Quantity

`quantity` is permitted only for stackable definitions. Its absence means one.
An active asset with quantity zero is not retained in current world state.
Exhaustion either removes it from the active snapshot or transforms it into a
meaningful remainder.

### 4.5 Current resources and durability

```json
{
  "resources": {
    "resource.cloak_charges": {
      "current": 2
    }
  },
  "durability": {
    "hp_current": 1
  }
}
```

Capacity, recovery, AC, maximum HP, thresholds, immunities, and other stable
rules come from definitions and active effects. The instance stores current
values only after they matter.

## 5. Automatic access and hand resolution

Routine retrieval and replacement are part of one Activity preflight, not
separate player commands or nested Activities.

```text
resolve possession and access
  -> validate temporary/persistent hand requirement
  -> apply an unambiguous implicit equipment adjustment
  -> execute the requested Activity
  -> commit one atomic result
```

An Activity distinguishes:

- `temporary` hand use: the hands are required only during execution;
- `persistent` hand use: the asset remains `held` after execution.

Drinking an accessible potion is one `use_asset` Activity. Retrieval, opening,
drinking, and ordinary replacement are implicit. The Activity may still spend
the action-economy cost defined by the ruleset; implicit physical handling does
not add another cost.

When an actor tries to hold more assets than their available hands and the
choice is not explicit, preflight returns `choice_required` without changing
state, consuming a turn, or spending resources. It lists the currently held
assets and the required number of hands. If the player's message already says
what to put away, the equipment adjustment and main action commit atomically.

Implicit handling is implemented inside one runtime resolution. It must not
cause extra LLM calls or produce a verbose chain of mechanical events.

## 6. Consumption, stacks, and transformation

### 6.1 Physical units and internal uses

- interchangeable physical units use `quantity`;
- doses, charges, fuel, and reusable activations of one physical object use
  `resources`.

A one-use potion normally transforms its bottle rather than retaining a
zero-use potion record:

```text
healing potion -> empty glass bottle
```

The Activity performs healing, consumption, and transformation atomically.

### 6.2 Stable identity during transformation

When the same physical object remains, runtime changes its `definition_id` and
preserves its `asset_id`, placement, and event history.

```json
{
  "operation": "asset.transform",
  "asset_id": "asset-00042",
  "from_definition_id": "asset.healing_potion",
  "to_definition_id": "asset.empty_glass_bottle"
}
```

Allowed results are declared by the Activity or another registered transition;
the LLM cannot assign an arbitrary mechanically incompatible definition.

The transition is a directed edge, not a declaration that two asset kinds are
generally compatible. Runtime validates the selected Activity's
`from_definition_id` against the current asset before applying
`to_definition_id`. A reverse transformation exists only when another Activity
declares the reverse edge. Thus refill may permit empty bottle -> healing potion
and deploy/stow may permit travelling mortar <-> siege mortar, while neither
creates any route between a bottle and a mortar.

Transition permissions belong to Activities rather than a per-asset list. This
avoids duplicated reverse links and still permits new campaign assets: their
definitions and connecting Activities are validated when loaded, before play
can execute them.

An empty bottle may later transform back through a refill Activity. Breaking it
may transform it into broken glass when the remainder matters, or destroy it
when it does not.

### 6.3 Stack splitting

If one unit of a stack changes definition, runtime atomically splits the stack:

```text
3 healing potions -> 2 healing potions + 1 empty bottle
```

The unchanged stack retains its identity. The physically distinct result
receives a new runtime-allocated asset ID. Events record the split and lineage.

## 7. Universal improvised use

HDM does not attach an attack Activity to every possible asset. The selected
ruleset provides a generic `activity.improvised_attack` that can accept a
suitable world asset.

The Master chooses one closed adjudication profile:

- `harmless` — no mechanical damage;
- `standard` — the ruleset's ordinary improvised-weapon profile;
- `weapon_equivalent` — use a referenced weapon profile when the object closely
  resembles it;
- `environmental` — route to manipulation, falling-object, area, or hazard
  resolution rather than hand-held weapon rules.

The runtime supplies formulas, range, and limitations from the selected
ruleset. The LLM supplies classification and an appropriate damage type, but
does not invent an unrestricted damage formula.

A flower can be `harmless`; a mug or bottle can be `standard`; a table leg may
be a club-equivalent; dropping a cabinet on someone is `environmental`.

## 8. Asset damage and destruction

Using an asset as a weapon does not automatically damage it. An Activity may
request a secondary impact resolution when material, fragility, force, or the
fictional circumstances create a real risk.

Examples:

- a glass bottle may break on impact;
- a mug may break on a target or wall;
- an ordinary sword is not damaged by every normal attack;
- a falling cabinet may damage both its target and itself;
- purely cosmetic harm may remain in `details` or narration until mechanics
  require durability.

When durability becomes mechanically relevant, runtime resolves or
materializes the definition's durability profile. At zero HP the asset is
destroyed or transformed into a meaningful remainder. Zero-quantity and
destroyed assets are absent from active world state, while their history
remains in events and checkpoints.

## 9. Facet guidance

Facets constrain expected components but do not create separate schemas:

| Facet | Common components |
|---|---|
| `asset.weapon` | handling, equipment properties, attack Activities |
| `asset.armor`, `asset.shield` | worn/held state, properties, effects |
| `asset.ammunition` | stack, quantity, attack consumption |
| `asset.consumable` | quantity or resources, use Activity, transformation |
| `asset.tool` | use/craft Activities and proficiency properties |
| `asset.container` | capacity and contained-asset reverse lookup |
| `asset.currency` | currency reference and stack quantity |
| `asset.key` | identity used by an access predicate |
| `asset.document` | lore/knowledge links or reading Activity |
| `asset.magic`, `asset.artifact` | rarity, attunement, resources, effects, Activities |
| `asset.vehicle` | capacity, control Activities, optional durability |
| `asset.decoration`, `asset.treasure` | reference value and details when needed |

Any compatible facets may coexist. An artifact may simultaneously be a weapon,
wearable decoration, key, container, or document.

## 10. Deliberate exclusions

The asset model does not store:

- copied attack damage, range, healing, or checks already owned by Activities;
- copied passive bonuses already owned by Effects or Rule Elements;
- container contents arrays or actor inventory arrays;
- derived possession and accessibility on every nested asset;
- current effects on an owner;
- transaction history or transaction prices;
- universal legal ownership;
- per-player identification booleans;
- UI image, sorting, favorite, or sheet-display state;
- per-record schema versions;
- detailed body-slot simulation;
- durability values for untouched incidental objects;
- a separate asset subtype or JSON schema for each facet.

These exclusions preserve one source of truth and keep routine ChatGPT turns
to a small number of runtime operations.

## 11. Runtime invariants

1. The runtime allocates persistent asset IDs.
2. At most one direct placement field is present.
3. Container relationships are acyclic.
4. A stack contains only interchangeable units with identical mutable state.
5. `quantity` is positive when present; absence means one.
6. Only stackable definitions may have quantity greater than one.
7. Current resource values correspond to resources supplied by the resolved
   definition and effects.
8. Attunement satisfies definition prerequisites and ruleset limits.
9. Persistent held-hand occupancy cannot exceed actor capacity.
10. Ambiguous hand replacement produces `choice_required` before mutation.
11. Transformation, stack splitting, resource spending, effects, and the main
    Activity result commit atomically.
12. Durable state cannot reference an unpublished ephemeral asset.

## 12. SQLite projection and HOT cache

Canonical JSON remains the source for asset state. SQLite projects frequently
queried fields without adding gameplay uniqueness constraints. Initial useful
indexes are:

- assets by `definition_id`;
- direct assets by `owner_actor_id`;
- contents by `container_asset_id`;
- placed assets by `location_id`;
- attuned assets by `attuned_actor_id`;
- held and worn assets by equipment mode.

The HOT cache stores complete resolved asset objects and may additionally cache
derived possession, accessible contents, total carried weight, occupied hands,
and container totals. The first implementation invalidates derived caches with
the session's monotonically increasing `state_revision` after any committed
mutation. This deliberately coarse rule is cheap and correct for chat-scale
state. Targeted dependency invalidation is added only if profiling justifies it.

The LLM sends semantic intent and bounded adjudication. Python performs graph
lookup, hand accounting, validation, arithmetic, ID allocation, atomic state
changes, and receipts.
