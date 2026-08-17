# HDM Catalog Design Status

Status: **DISCUSSION CHECKPOINT**

Target branch: `feature/mechanical-runtime-hot-state`

This document records the current state of catalog design so that subsequent
work does not depend on reconstructing decisions from a ChatGPT conversation.
It is a design checkpoint, not an implementation contract. Each statement is
marked as `AGREED`, `PROVISIONAL`, or `OPEN`.

## 1. Exact point of continuation

The four-layer separation below is accepted. The proposed contents of those
layers have not yet been reviewed category by category:

1. engine capability registry;
2. reusable content-definition catalog;
3. campaign/world records;
4. runtime records.

The next catalog task is to review the proposed classes in those four layers,
decide whether each class belongs there, and identify missing or redundant
classes. Minimum field sets and executable contracts follow only after that
review.

## 2. Agreed catalog principles

### `AGREED` — Core catalog and extensibility

- The core repository contains a versioned catalog that serves as architecture
  documentation and as seed data for runtime/SQLite loading.
- The catalog describes stable classes, facets, primitives, and policies. It
  cannot enumerate every concrete player idea or world object.
- The engine ships standard definitions. The Master may classify, combine, and
  customize them within capabilities explicitly supported by the engine.
- New executable semantics require an engine capability. The Master may not
  invent executable capability IDs or arbitrary Python/SQL during play.
- Objects may have several facets simultaneously. An artifact may also be a
  weapon, wearable object, decoration, document, or tool.
- Tags and facets support classification and retrieval. They do not themselves
  grant mechanical behavior.

### `AGREED` — LLM/runtime boundary

- The player speaks naturally and does not need to know the catalog.
- The LLM Master interprets the request, identifies all material intents,
  classifies entities, selects definitions/capabilities, and prepares typed
  input for the runtime.
- The runtime owns authoritative random rolls, arithmetic, validation, atomic
  state transitions, identifiers, and persistence mechanics.
- No material clause in a player message may be silently discarded.
- One player message may contain several actions. The interface must not force
  the player to submit one microscopic action per message.
- Activity executes a bounded action. Rule Elements provide typed conditional
  contributions and do not mutate arbitrary state.
- The dice component only produces rolls. Buffs, debuffs, modifiers, and
  consequences belong to resolution/rule processing.

### `AGREED` — Runtime and durable state

- The physical HOT state is local operational truth. SQLite is a disposable
  working projection/transaction store. GitHub is durable campaign canon.
- A new environment must be able to reconstruct canonical state from GitHub at
  the last published checkpoint. Byte-identical SQLite recovery is unnecessary.
- Incidental, non-canonical entities may disappear with the local environment.
  Anything referenced by durable canon must be promoted before publication.
- Critical changes require prompt durable publication. Examples include
  contracts, money, significant items/artifacts, focal-location changes,
  companions or critical NPCs, and mission-critical transitions.
- Git data remains human-readable JSON/YAML/Markdown. HDM adds no custom archive
  or compression layer; Git transport compression is sufficient.
- Lore, history, and story may also be stored as substantial chapter documents
  with metadata and entity references.

### `AGREED` — Chronology and play model

- HDM is dialogue-driven and turn-based; it has no real-time simulation loop.
- General campaign chronology needs causal and ordering consistency but does
  not require a universal calendar or clock.
- Event-local time budgets may be mechanically meaningful, for example a
  ten-minute effect duration.
- Gameplay timeline slots use increments of ten to leave room for later
  insertion, for example `00430`, `00440`.
- Historical facts discovered during play remain lore unless placing them on
  the active gameplay timeline is operationally useful.

## 3. Provisional model — review required

The following structures exist in `CATALOG_MODEL.md` and
`core-catalog.json`, but their presence is a proposal rather than acceptance of
completeness or exact shape:

- definition kinds such as actor archetype, asset, activity, resource, effect,
  condition, Rule Element, trigger binding, location archetype, and mode profile;
- world kinds such as actor, asset, location, organization, contract, mission,
  scene, encounter, lore fact, chapter, and timeline marker;
- runtime kinds such as session, intent plan, resolution, mechanical event,
  resolution trace, dirty record, publication batch, and maintenance audit;
- the universal definition and instance envelopes;
- the initial activity, asset-facet, event, primitive, target, duration,
  resource, and rules registries.

These entries are working material. Their current presence must not be cited as
evidence that the catalog is complete or approved.

## 4. Identifier and HOT-cache policy

### `AGREED`

- Stable identifiers are allocated by the runtime, not counted or invented by
  the LLM.
- Identifier allocation and creation of the corresponding canonical record
  must be one atomic runtime operation.
- Numeric widths are formatting choices, not hard limits. A value may naturally
  grow beyond its configured zero-padded width.
- Persistent identifiers are never reused by default.
- Identifier policy is per entity class and includes at least namespace/prefix,
  scope, presentation width, allocator ownership, and durability.
- HOT caching concerns complete working objects, not merely their numeric
  counters. Allocator state may be cached alongside those objects.
- A process cache is an acceleration layer. Recoverable HOT state and the last
  durable checkpoint remain the relevant authorities after process loss.

### `OPEN`

- Which entity classes require canonical sequential IDs at all.
- Whether incidental/pass-through actors, objects, and locations receive only
  runtime-local identity until promoted to canon.
- Exact scopes and widths for scenes, actors, locations, assets, events,
  chapters, turns, resolutions, and other records.
- Whether every counter is stored independently or derived from an allocator
  registry and existing records.
- Collision handling and allocation strategy for concurrent multiplayer
  writers.

The previously discussed five-digit turn presentation is a reasonable
candidate, not a general identifier policy for all classes.

## 5. Other catalog questions still open

1. Complete class list and the layer containing each class.
2. Minimum universal definition and instance envelopes.
3. Exact Activity primitives and composition limits.
4. Execution semantics for multi-intent messages: ordering, atomic groups,
   partial failure, suspension, and action-economy boundaries.
5. Event taxonomy, granularity, and durability classification.
6. Minimum structures for assets and the division between facets, tags,
   capabilities, and mutable state.
7. Actor/NPC/companion archetypes and instance state.
8. Effects, conditions, resources, durations, and recovery contracts.
9. Lore, chapters, visibility/knowledge restrictions, and secret handling.
10. Game-mode profiles, including quick narrative play, canonical mechanics,
    and strict-information-isolation detective play.
11. Event-local time budgets and multiplayer chronology.
12. SOFT accumulation budgets and configurable HARD publication thresholds.
13. Override, versioning, migration, promotion, and catalog-gap workflows.
14. Standard ruleset seed data, including the selected D&D/SRD baseline.

## 6. Deferred work that must remain possible

- A client chat may eventually submit a catalog-gap/asset request or bug report
  to the public engine repository. The submission contract is not designed yet.
- Edited-message branches may eventually map to runtime checkpoints so a scene
  can be replayed from an earlier state. Current development should avoid
  making that restoration model impossible, but it is not part of the catalog
  phase.
- Game/bootstrap instructions may need periodic refresh in long ChatGPT
  sessions so that the runtime-call sequence stays in hot conversational
  context. This is a runtime-host concern, not catalog content.

## 7. Scope guard

The catalog phase is complete only after the class inventory, minimum
structures, extensibility boundaries, and their identifier policies have been
reviewed and explicitly accepted. The current 195 catalog IDs are candidates,
not a completeness metric.
