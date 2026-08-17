# HDM Asset Model Cases

Status: **ACCEPTANCE CASES**

Architecture: `ARCHITECTURE/ASSET_MODEL.md`

Schemas:

- `SCHEMAS/asset-definition-data.schema.json`;
- `SCHEMAS/world-asset-state.schema.json`.

## A01 — Empty narrative asset

An asset definition with empty `data` and a world asset with empty `state`
validate. No weight, value, mechanics, placement, or guessed defaults are
persisted.

## A02 — Two-handed use

A weapon definition has `held_hands: 1` and `use_hands: 2`. It has one normal
attack Activity, not separate one-handed and two-handed Activities. The actor
may hold it with one hand; normal use requires two available hands.

## A03 — Accessible potion in a worn backpack

The backpack is directly controlled by an actor and has equipment mode `worn`.
The potion references the backpack through `container_asset_id`. Runtime derives
possession and access. "Drink the potion" produces one use Activity; opening,
retrieval, and ordinary handling do not become separate commands.

## A04 — Ambiguous hand conflict

An actor holds a sword and shield and requests a third persistent held item.
Preflight returns `choice_required`, lists the held assets, and performs no
mutation, time spending, or resource spending.

## A05 — Explicit hand replacement

"Put away the sword and take the torch" atomically removes `held` from the
sword, adds `held` to the torch, and completes without another LLM/runtime
round-trip.

## A06 — Potion transformation

Using a single healing potion applies its Activity and changes the same world
asset's definition to an empty bottle. Asset ID, placement, and event lineage
remain stable. No zero-use potion remains active.

## A07 — Stack split

Using one unit from a stack of three potions leaves the original stack with
quantity two and creates one runtime-allocated empty-bottle asset. Healing,
decrement, split, and transformation are atomic.

## A08 — Quantity zero rejection

`quantity: 0` fails schema validation. Exhausting a stack removes it from the
active snapshot or transforms the final unit into a meaningful remainder.

## A09 — Placement conflict rejection

Any world asset containing more than one of `owner_actor_id`,
`container_asset_id`, and `location_id` fails schema validation.

## A10 — Container cycle rejection

Schema-valid individual records that form a containment cycle are rejected by
runtime graph validation. No durable checkpoint contains the cycle.

## A11 — Improvised bottle attack

A bottle without its own attack Activity may be passed to the ruleset's generic
improvised-attack Activity. The Master selects a closed adjudication profile and
damage type; runtime supplies the ruleset formula and may resolve secondary
breakage risk.

## A12 — Harmless and environmental uses

A flower may resolve with the `harmless` profile and zero mechanical damage.
Dropping a cabinet routes to environmental/manipulation resolution rather than
inflating hand-held improvised-weapon damage.

## A13 — Lazy durability

An incidental bottle may exist without current HP. When an impact makes
durability relevant, runtime materializes the applicable profile and current
HP. Reaching zero destroys or transforms the asset atomically.

## A14 — Resources versus quantity

Twenty interchangeable arrows use `quantity: 20`. A single lamp with six hours
of fuel uses a resource current value. The two mechanisms are not mixed.

## A15 — Per-actor identification

An asset has no `identified` boolean. Different actor knowledge is represented
through lore and knowledge records, allowing one actor to know an item's nature
while another does not.
