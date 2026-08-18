# HDM Catalog Design Status

Status: **DISCUSSION CHECKPOINT**

Target branch: `feature/mechanical-runtime-hot-state`

Active sequencing is governed by `ARCHITECTURE/NEAR_TERM_ROADMAP.md`. The
engine-wide architecture workflow is `ARCHITECTURE/DESIGN_PROCESS.md`. The
critical review ledger is `ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`; its
adversarial second-pass verdict package is owner-approved. Step 2 is active,
subject to its independent Superpowers architecture gate. The live Step 2 design
spec is `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`.

This document records the current state of catalog design so that subsequent
work does not depend on reconstructing decisions from a ChatGPT conversation.
It is a design checkpoint, not an implementation contract. Each statement is
marked as `AGREED`, `PROVISIONAL`, or `OPEN`.

## 1. Exact point of continuation

The accepted catalog foundations were audited by logical block and for obvious
cross-document contradictions. Stale selectable IDs and the obsolete
per-transition durability table were removed/neutralized in `CATALOG_MODEL.md`.

The owner-approved adversarial second pass found deeper ownership and ordering risks:
health and Asset durability can be confused with generic Resources;
transformation lacks a settled definition-dependent state migration boundary;
and multiplayer/mode stages depend on knowledge, visibility, promotion, and
seed interfaces that were scheduled too late. The roadmap is reordered and the
accepted semantic corrections are applied.

Step 2 is now closing its ownership map before any new schema fields are added.
The HP/LifeState boundary, Resource/procedure-budget ownership, and
Condition/Effect/LifeState ownership have passed separate critical discussion
and received explicit owner approval. Their current normative design record is
the live Step 2 spec above.

The exact continuation point is **Duration / expiry / concentration ownership**.
After that, Step 2 still owns remaining Effect/Recovery ownership, minimum
LifeState transitions, health/effect selectors, schema/catalog alignment,
focused cases, and its final critical pass.

The four-layer separation below is accepted:

1. engine capability registry;
2. reusable content-definition catalog;
3. campaign/world records;
4. runtime records.

The class inventory for those layers was reviewed against SRD 5.2.1, Foundry
D&D5e, Avrae automation, and PF2e Rule Element prior art. The resulting baseline
is fixed in `ARCHITECTURE/CATALOG_INVENTORY.md` and machine-readable catalog
version 1.2.0. It is sufficient for schema design and explicitly extensible.

The minimum universal envelopes and the required/expected field inventory for
every definition and world-record kind are agreed. They are recorded in
`ARCHITECTURE/CATALOG_CONTRACTS.md`, `ARCHITECTURE/ENTITY_STRUCTURES.md`, and
`CATALOG/entity-structures.json`. Actor and asset nested models are accepted in
`ARCHITECTURE/ACTOR_MODEL.md` and `ARCHITECTURE/ASSET_MODEL.md`. The first
Activity and Rule Element contracts are captured by
`ARCHITECTURE/ACTIVITY_MODEL.md` and `ARCHITECTURE/RULE_ELEMENT_MODEL.md`.
Identifier policy is decided alongside each independently identified record
kind.

For Step 2-owned fields, the live ownership spec supersedes older provisional
wording when it explicitly says so. Exact machine field/schema changes remain
frozen until the ownership map closes, so the current machine field inventory
must not be treated as final Step 2 shape where the live spec records a newer
accepted ownership boundary.

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
- Activity executes a bounded mechanical procedure. Rule Elements provide typed
  conditional contributions and do not mutate state. Trigger Bindings connect
  registered Signals/Events to registered Activities without callbacks.
- The dice component only produces rolls. Buffs, debuffs, modifiers, and
  consequences belong to resolution/rule processing.

### `AGREED` — Runtime and durable state

- The physical HOT state is local operational truth. SQLite is a disposable
  working projection/transaction store. GitHub is durable campaign canon.
- Durable recovery is snapshot-first. Events provide causal audit and bounded
  catch-up after the snapshot frontier; HDM does not require replaying the full
  campaign log to reconstruct current state.
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
- Publication uses compare-and-swap semantics against an expected Git HEAD.
  Concurrent advancement requires reload/reconciliation and never a force push.

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

### `AGREED` — Step 2 ownership decisions closed so far

- Actor `hp` is the single HP/temporary-HP authority; `life_state_id` is a
  separate lifecycle authority and zero HP is not universal death.
- Persistent Actor/Asset Resources and procedure-local budgets use one Resource
  semantics but different lifetime owners. Procedure-local consumption is
  serializable state owned by the active procedure/encounter, not the Actor and
  not an individual Resolution; its capacity is derived.
- Restricted/non-interchangeable additional action-economy budgets use distinct
  Resource definitions rather than being folded into unrestricted capacity.
- Activity/Rule Elements/Triggers resolve Resource references through one
  storage-independent runtime interface.
- `definition.condition` remains a named rules identity. A concrete application
  is ordinary Effect-instance state; Actor condition lists are derived
  HOT/SQLite indexes, not canon.
- Condition and Effect definitions may share the same mechanical payload model;
  a Condition does not require an intermediate Effect definition merely to hold
  ordinary mechanics.
- Multiple applications and effective Condition aggregation are separate; app
  count, stacks, and valued severity are not one overloaded field.
- LifeState and Condition are separate authorities, so lifecycle state such as
  dying/stable may coexist with a named Unconscious condition application.

## 3. Reviewed inventory and provisional structures

The class membership and layer boundaries in `CATALOG_INVENTORY.md` are now the
reviewed baseline. They may be extended later through catalog versioning.

The universal envelopes and field membership in `CATALOG_CONTRACTS.md` and
`ENTITY_STRUCTURES.md` are accepted contracts. Activity, Rule Element, and
Trigger Binding now have a design baseline and structural JSON Schemas. The
following details remain proposals rather than accepted contracts:

- remaining nested shapes and validation rules for other kind-specific fields;
- exact operation-specific `args`/result and Rule Element value schemas;
- measured composition and trigger-chain limits.

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
- Definitions use semantic namespaced IDs. Protocol values have no independent
  ID by default. Timeline slots and encounter rounds are values, not identities.
- Canonical world and independently numbered runtime records use the
  campaign-scoped policies in `CATALOG/identifier-policies.json`; runtime owns
  allocation and stores `last_allocated` in one `campaign-allocator` object.
- Incidental actors, groups, assets, locations, zones, hazards, and effects may
  use session-local IDs until runtime promotes and atomically rekeys them.
- Widths range from three digits for low-volume records to eight for mechanical
  events. `turn` uses six digits. Width is minimum padding and never an upper
  bound.
- Multiplayer allocation conflicts are resolved only for unpublished records
  after optimistic Git-head comparison; published IDs never change.

### `OPEN`

- No identifier-policy questions remain open at the catalog level. Concrete
  SQLite tables and reconciliation algorithms belong to runtime implementation
  design.

## 5. Other catalog questions still open

1. Nested shapes and validation rules for kind-specific fields and references.
2. Exact Activity primitive argument/result contracts and measured composition
   limits.
3. Focused validation of the sequential multi-intent, partial-failure,
   suspension, and action-economy boundaries.
4. Event payloads, granularity, and durability classification; the event-kind
   baseline itself is reviewed.
5. Step 2 remaining ownership: Duration/expiry/concentration, remaining
   Effect/Recovery behavior, minimum LifeState transitions, selectors, then
   schema/catalog alignment and focused cases.
6. Lore, chapters, visibility/knowledge restrictions, and secret handling.
7. Game-mode profiles, including quick narrative play, canonical mechanics,
   and strict-information-isolation detective play.
8. Event-local time budgets and multiplayer chronology.
9. SOFT accumulation budgets and configurable HARD publication thresholds.
10. Migration, promotion, and catalog-gap workflows.
11. Standard ruleset seed data, including the selected D&D/SRD baseline.

Step 2 continues to own LifeState. HP remains the numeric health authority, but
zero HP does not determine death by itself. When HP is materialized, a separate
`life_state_id` is materialized with it. Scheduled or conditional
transformations remain Effects/Triggers and atomically update form/type,
LifeState, and HP when resolved. This requirement supersedes the earlier
deferred-lifecycle note.

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

The class inventory, universal structures, identifier policies, and
extensibility boundary are reviewed. The first Activity/Rule Element contracts
are recorded as a design baseline pending focused mechanical examples. Registry
counts are never a completeness metric.
