# HDM Catalog Design Status

Status: **DISCUSSION CHECKPOINT**

Target branch: `feature/mechanical-runtime-hot-state`

Active sequencing is governed by `ARCHITECTURE/NEAR_TERM_ROADMAP.md`. The
engine-wide architecture workflow is `ARCHITECTURE/DESIGN_PROCESS.md`. The
critical review ledger is `ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`; its
adversarial second-pass verdict package is owner-approved. Step 2 is active,
subject to its independent Superpowers architecture gate. The live Step 2 design
spec is `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`.
The detailed preliminary Recovery B2 design is
`DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`.
The detailed preliminary Effect-application design is
`DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`.
The detailed preliminary LifeState design is
`DEV/docs/superpowers/specs/2026-08-19-step-2-lifestate-policy-transition-design.md`.

This document records the current state of catalog design so that subsequent
work does not depend on reconstructing decisions from a ChatGPT conversation.
It is a design checkpoint, not an implementation contract. Each statement is
marked as `AGREED`, `PROVISIONAL`, or `OPEN`.

All current architecture remains subject to the planned later holistic review
of the **entire architecture, structures, logic, ownership, schemas, and
inter-module relationships** after the major modules have designs. Preliminary
labels indicate current sequencing confidence; they do not imply that only those
specific blocks will be revisited.

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
The HP/LifeState boundary, Resource/procedure-budget ownership,
Condition/Effect/LifeState ownership, maintained Effect-support ownership, and
Duration/Temporal Agenda ownership have passed critical discussion and received
explicit owner approval. Recovery boundary ownership, generic Effect
application/arbitration ownership, and LifeState policy/progress/transition
ownership have reached detailed **preliminarily accepted** checkpoints that are
active for current sequencing.

The exact continuation point is **health/effect selectors and query boundaries**.
Concentration is not a duration mode; maintained support is a separate
Effect-to-Effect lifecycle relation. Intrinsic Duration uses authoritative
Effect temporal bindings with a lazy local metric coordinate and disposable
Temporal Agenda rather than a universal clock or writable countdown. Recovery
uses boundary-producer/state-owner response ownership. Effect applications are
one-target/one-episode records with create-new default semantics and derived
rare-overlap arbitration rather than generic mutable stacks or multi-target
state maps. LifeState uses a four-state D&D baseline, small registered lifecycle
policies, state-local progress, prospective atomic transition planning, lazy
revival eligibility, and opt-in automatic post-death mechanics. Step 2 still
owns health/effect selectors, schema/catalog alignment, focused cases, and its
final critical pass.

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
accepted or preliminarily accepted ownership boundary.

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
- Metric precision is demand-driven. A local monotonic coordinate advances only
  through explicit runtime/procedure advancement while elapsed time is
  mechanically material; it may freeze otherwise and never follows wall clock.
- Intrinsic temporal bindings use the mechanically appropriate basis: metric
  deadline, procedure boundary, or semantic boundary. Turn/rest/dawn semantics
  are not forced into synthetic seconds.
- Temporal Agenda data is a disposable HOT/SQLite due-index rebuilt from
  authoritative bindings, not a persistent scheduler authority.
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
- Multiple applications and effective Condition aggregation are separate;
  application count and valued severity are not one overloaded mutable stack.
- LifeState and Condition are separate authorities, so lifecycle state such as
  dying/stable may coexist with a named Unconscious condition application.
- Concentration is not a duration mode. A maintained Effect may have zero or one
  immutable lifecycle parent; support relations form a forest rather than a
  generic graph or predicate language.
- A nonterminal parent provides structural support even while suppressed. A
  terminal parent causes its full descendant closure to expire atomically;
  child termination has no automatic effect on the parent.
- Maintenance identity is stable for one episode; refresh updates the same
  Effect instance, canonical storage keeps only the forward parent reference,
  and reverse child indexes are disposable HOT/SQLite projections.
- Durable promotion includes any required support-parent chain. Ruleset-specific
  Concentration exclusivity remains ruleset behavior, not a generic uniqueness
  subsystem.
- Definitions own reusable Duration semantics; each active Effect owns the
  concrete temporal binding for its intrinsic lifetime. `remaining` is normally
  derived, not a second mutable countdown authority.
- Metric Duration uses a local exact monotonic coordinate only while elapsed
  precision is materially needed. No global or wall-clock scheduler is added.
- Procedure-relative and semantic expiry boundaries remain typed bases rather
  than being coerced into metric seconds.
- A requested time advance stops at the nearest due boundary, closes same-time
  consequences, and exposes any unconsumed continuation rather than blindly
  executing through a changed world state.
- Re-anchoring derives remaining once only when an Effect actually transfers
  across an incompatible temporal basis/context. Persistent multi-target
  mechanics use target-local applications rather than one Effect carrying
  several target clocks; shared maintained lifetime belongs to the support root.

### `PROVISIONAL` — Step 2 Recovery B2 ownership

- One registered boundary identity is shared by Duration, Recovery, and
  procedure refresh when they refer to the same semantic occurrence. Parallel
  synonymous timing registries are not separate authorities.
- A RestPolicy or procedure owns whether its typed scoped boundary occurred; it
  does not own mutations to unrelated Resource/HP/Effect state.
- A concrete BoundaryOccurrence is transient typed runtime context with stable
  occurrence identity and explicit scope/provenance, not a canonical world
  entity or persistent scheduler record.
- `definition.resource` owns baseline automatic recovery semantics. ResourceState
  remains the sole mutable authority, and the common Resource resolver applies
  recovery independent of Actor/Asset/procedure storage layout.
- Active mechanics may modify recovery through pure `resource.recovery` Rule
  Element contributions; they do not directly mutate ResourceState or own
  recovery counters.
- Automatic recovery is deterministic and bounded. Mechanics requiring choices,
  rolls, optional use, reaction windows, or spending another Resource are owned
  by Step-3 Activity/Trigger/Resolution execution instead.
- Timed Resource recovery and Effect expiry share the same disposable Temporal
  Agenda/index infrastructure. Turn/round resets use the same procedure-boundary
  indexing rather than a separate action-economy reset engine.
- Boundary discovery is scoped/indexed rather than campaign-wide. Runtime
  discovers the complete immediately due set before mutation so SQL/list order
  cannot become mechanical order.
- Exact same-boundary phase ordering, occurrence idempotency/receipts, and
  zero-time chain limits remain Step 3; cross-scene/multiplayer boundary
  reconciliation remains Step 5.
- `definition.rest_policy.recovery_steps` is provisionally superseded as an
  authoritative cross-subsystem recovery list. The independent
  `recovery_triggers` registry is likewise provisional where it duplicates the
  common boundary vocabulary. Exact machine migration is deferred until schema
  alignment.
- Developer discoverability should be recovered through a derived read-only
  Boundary Impact View, never by recreating a second editable recovery list.

### `PROVISIONAL` — Step 2 Effect application and arbitration ownership

- One independent target-local Effect application is one Effect instance.
  Persistent multi-target Activities create one application per target instead
  of one mutable Effect carrying `target_ids[]` and per-target state.
- Zone/Asset/Location records may be the one target when a mechanic is genuinely
  spatial/object-local; creature-local Effects are materialized only when the
  rules create independent creature-local state.
- New valid applications create new Effect identities by default. Explicit
  refresh keeps one lifecycle identity; explicit replace ends the old identity
  and creates a new one without overwriting provenance.
- Application identity, reusable Effect template identity, rules-bearing origin,
  concrete source, and causal Resolution origin remain distinct concepts.
- Rare overlap groups are derived by target plus rules-origin/application family,
  normally using spell/feature/condition identity rather than blindly grouping
  by Effect template ID.
- If no ArbitrationPolicy applies, all eligible applications participate. A
  registered arbitration policy selects whole applications through deterministic
  typed comparison such as a proven potency/recency rule; arbitrary formulas,
  wall-clock ordering, and list order are forbidden.
- Effect arbitration chooses which applications participate. Rule Element
  resolvers independently decide how their typed contributions add, collapse,
  override, grant advantage, apply resistance, or otherwise combine.
- Generic mutable `world.effect.stacks` is not part of the preferred model.
  Independent repeated units are separate Effects; one-episode severity or
  intensity is a typed application parameter, or a Resource if it has genuine
  capacity/spending/recovery semantics.
- Lifecycle, suppression/availability, and arbitration winner/shadowed state are
  distinct. Winner/shadowed state is derived HOT/SQLite data, not canonical
  mutable authority.
- Removal/dispel acts on concrete applications or a rules-resolved set. Removing
  a winner invalidates only the affected group; a shadowed candidate may become
  effective without a resurrection mutation.
- Genuine on-end consequences use typed Effect-end Signal/Event plus the existing
  TriggerBinding/Activity execution path. No arbitrary `on_end` callback or
  separate Effect scripting/combination engine is added.
- The current `target_ids`, generic `stacks`, `effect.stacks`, and broad
  `stacking_behaviors` machine inventory is provisional and must be decomposed,
  narrowed, or removed during later Step 2 schema/catalog alignment rather than
  expanded with more combined enum values.

### `PROVISIONAL` — Step 2 LifeState policy/progress/transition ownership

- The minimum D&D LifeState vocabulary is `active`, `dying`, `stable`, and
  `dead`. `active` is ordinary lifecycle, not action availability. Unconscious,
  Incapacitated, creature type, Effect lifecycle, and Actor retirement remain
  separate authorities.
- Baseline lifecycle behavior uses a small registered policy capability. The
  initial D&D baseline needs character-like and monster-default behavior; an
  important NPC may use an override/inherited policy without changing Actor kind.
- Special death-prevention/alteration Features do not create combinatorial policy
  variants. They participate in the normal prospective rules/Step-3 path before
  the final lifecycle transition is committed.
- Actor stores current `life_state_id` plus typed state-local progress only when
  the current state requires it. Dying owns death-save successes/failures in the
  range `0..2`; threshold value 3 is never canonical because it immediately
  transitions to Stable/Dead.
- Death saves are lifecycle progress, not Resources, and therefore do not acquire
  generic resource capacity/spending/recovery semantics.
- Stable owns the real automatic `1d4`-hour recovery TemporalBinding required by
  the D&D rule. It uses the common Temporal Agenda; healing/damage cancels or
  supersedes that binding prospectively rather than via a separate scheduler.
- Dead creates no generic resurrection timer, no revival-window records, no
  search for spells/NPCs/services, and no Agenda work merely because revival
  could be possible.
- A revival spell/Activity/feature/service owns its own temporal eligibility and
  other requirements. The current death origin is hydrated lazily only when a
  relevant mechanic actually needs time-since-death.
- No mandatory `dead_since` countdown is added to Actor state, but snapshot/event
  compaction must preserve enough provenance for the start of the current dead
  episode to remain mechanically recoverable. If exact historical precision was
  legitimately unavailable, runtime adjudicates instead of inventing time.
- Automatic post-death returns/transformations are ordinary opt-in indexed
  Feature/Effect/Trigger mechanics. Only an Actor with such an already-known
  rule materializes a future temporal/semantic obligation.
- LifeStateResolver is a typed planner, not a writer. It produces a prospective
  LifeStateTransitionPlan carrying state/progress plus required HP,
  Condition/Effect, temporal-binding, and provenance deltas for Step-3 atomic
  commitment.
- Any resolved transition to Dead normalizes `hp.current` to zero. Restoration of
  maximum HP later does not revive the stored Dead state, and ordinary healing
  does not function as a second revival API.
- Character-like zero HP creates a lifecycle-origin Unconscious Condition
  application; Stable keeps it; valid return to Active removes only that source-
  local application and cannot accidentally remove an independent magical
  Unconscious application.
- Death does not universally purge Effects or retire/delete the Actor.
  Concentration and other explicitly interested mechanics react through local
  indexes and existing Effect/support/Trigger machinery; unrelated still-valid
  Effects may persist through revival.
- Dying Death Saves are driven by the relevant turn/procedure boundary, not by a
  background timer. Step 3 must preserve mandatory lifecycle continuation when a
  procedure would otherwise close with an unresolved dying participant.
- Derived queries such as `is_dead`, `needs_death_save`, or `can_act` are HOT
  computations/indexes, not additional writable Actor authorities.

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
- Widths range from three digits for low-volume records to eight digits for
  mechanical events. `turn` uses six digits. Width is minimum padding and never
  an upper bound.
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
5. Step 2 remaining architecture: health/effect selectors and query boundaries,
   then schema/catalog alignment and focused cases. Recovery, Effect-application,
   and LifeState checkpoints are provisionally closed for current sequencing;
   all architecture remains subject to the later holistic review.
6. Lore, chapters, visibility/knowledge restrictions, and secret handling.
7. Game-mode profiles, including quick narrative play, canonical mechanics,
   and strict-information-isolation detective play.
8. Cross-scene event-local time reconciliation and multiplayer chronology.
9. SOFT accumulation budgets and configurable HARD publication thresholds.
10. Migration, promotion, and catalog-gap workflows.
11. Standard ruleset seed data, including the selected D&D/SRD baseline.

Step 2 now has a preliminary LifeState transition baseline in addition to the
previous HP ownership boundary. HP remains the numeric health authority while
`life_state_id` is the stored lifecycle classification. The D&D baseline uses
`active/dying/stable/dead`; state-local dying/stable progress is materialized
only when required. Revival eligibility is lazy and mechanic-owned rather than a
corpse timer. Scheduled or conditional transformations remain Effects/Triggers
and may atomically update form/type, LifeState, and HP when resolved. Exact
machine fields remain deferred until ownership/query design is complete.

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
