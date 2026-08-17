# HDM Catalog Design Status

Status: **DISCUSSION CHECKPOINT**

Target branch: `feature/mechanical-runtime-hot-state`

This document records the current state of catalog design so that subsequent
work does not depend on reconstructing decisions from a ChatGPT conversation.
It is a design checkpoint, not an implementation contract. Each statement is
marked as `AGREED`, `PROVISIONAL`, or `OPEN`.

## 1. Exact point of continuation

The four-layer separation below is accepted:

1. engine capability registry;
2. reusable content-definition catalog;
3. campaign/world records;
4. runtime records.

The class inventory for those layers was reviewed against SRD 5.2.1, Foundry
D&D5e, Avrae automation, and PF2e Rule Element prior art. The resulting baseline
is fixed in `ARCHITECTURE/CATALOG_INVENTORY.md` and machine-readable catalog
version 1.1.0. It is sufficient for schema design and explicitly extensible.

The minimum universal envelopes and the required/expected field inventory for
every definition and world-record kind are agreed. They are recorded in
`ARCHITECTURE/CATALOG_CONTRACTS.md`, `ARCHITECTURE/ENTITY_STRUCTURES.md`, and
`CATALOG/entity-structures.json`. The next catalog task is to define the nested
value shapes. Actor archetype, actor state, and actor-group state are accepted
in `ARCHITECTURE/ACTOR_MODEL.md`; the remaining kinds follow. Identifier policy
is decided alongside each independently identified record kind.

## 2. Agreed catalog principles

### `AGREED` — Core catalog and extensibility

- Record structures follow minimum sufficiency: speculative fields and generic
  extension mechanisms are not added without a concrete requirement.
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

## 3. Reviewed inventory and provisional structures

The class membership and layer boundaries in `CATALOG_INVENTORY.md` are now the
reviewed baseline. They may be extended later through catalog versioning.

The universal envelopes and field membership in `CATALOG_CONTRACTS.md` and
`ENTITY_STRUCTURES.md` are accepted contracts. The following structures remain
proposals rather than accepted contracts:

- nested shapes and validation rules for kind-specific fields and references;
- exact executable contracts for the registered primitives and Rule Elements;
- identifier policies and promotion rules for each record kind.

Catalog membership is reviewed; schema and runtime behavior are not thereby
approved or implemented.

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

1. Nested shapes and validation rules for kind-specific fields and references.
2. Exact Activity primitive contracts and composition limits.
3. Execution semantics for multi-intent messages: ordering, atomic groups,
   partial failure, suspension, and action-economy boundaries.
4. Event payloads, granularity, and durability classification; the event-kind
   baseline itself is reviewed.
5. Minimum structures for assets and the division between facets, tags,
   capabilities, and mutable state.
6. Actor/NPC/companion archetypes and instance state.
7. Effects, conditions, resources, durations, and recovery contracts.
8. Lore, chapters, visibility/knowledge restrictions, and secret handling.
9. Game-mode profiles, including quick narrative play, canonical mechanics,
    and strict-information-isolation detective play.
10. Event-local time budgets and multiplayer chronology.
11. SOFT accumulation budgets and configurable HARD publication thresholds.
12. Migration, promotion, and catalog-gap workflows.
13. Standard ruleset seed data, including the selected D&D/SRD baseline.

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

The class inventory and extensibility boundary are now reviewed. The catalog
phase is complete only after minimum structures and their identifier policies
have also been reviewed and accepted. Registry counts are never a completeness
metric.
