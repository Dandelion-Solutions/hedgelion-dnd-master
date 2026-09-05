# HDM Catalog Inventory

Status: **R2.7 WP-03 CANONICAL CLASSIFICATION — STRUCTURAL REALIZATION IN PROGRESS**

Canonical catalog generation: `2`

Generation `2` is the unreleased clean-slate R2.7 coordinated machine-contract generation. Current coordinated machine artifacts serialize this directly as integer `catalog_generation: 2` under `DEV/docs/superpowers/specs/2026-09-05-hdm-versioning-namespace-compatibility-policy.md`. No campaign or released runtime depends on the superseded pre-rearchitecture scaffold or its pre-normalization representation.

All coordinated catalog-generation projections MUST equal the canonical catalog generation. Mixed coordinated generations are invalid. Individual catalog artifact `schema_version` values remain independent structural schema versions and do not have to equal the catalog generation.

The exact closed machine IDs are in `DEV/CATALOG/core-catalog.json`. This document is authoritative for classification and class semantics. `CATALOG_ADMISSION.md` and `DEV/CATALOG/catalog-admission-ledger/` (manifest + per-registry-family shards, assembled by `DEV/TOOLS/catalog_admission.py`) own admission disposition and realization traceability without becoming a second ID or semantic owner. Exact persistent schemas, roots, sharding and HOT/SQLite realization are owned by later R2.7 domains.

---

## 1. Classification rule

Every machine concept belongs to the smallest class that matches its independent responsibility and lifecycle:

1. **engine capability / closed enum** — executable or protocol meaning implemented and reviewed by the engine;
2. **`definition.*`** — reusable validated rules/content composed from registered capabilities;
3. **`world.*`** — one particular campaign thing/fact with independent world identity/lifecycle/current state;
4. **`runtime.*`** — independently addressable non-world operational/evidence owner required across retry, suspension, recovery, collaboration, disclosure or audit;
5. **embedded `value.*`** — typed request/result/control object without independent lifecycle;
6. **noncanonical projection family outside the canonical/current record catalog** — Story and retained Dramaturg planning, which have their own projection lifecycles but cannot become gameplay authority.

Facets/tags classify or route. They never grant executable semantics or create independent identity.

A concept is not promoted to a record merely because it is serialized, cached or useful to an LLM.

---

## 2. Reusable definition classes

Catalog generation 2 retains the accepted reusable definition families. Exact IDs are machine-owned in `core-catalog.json`.

### Rules vocabulary

- `definition.ability`
- `definition.skill`
- `definition.proficiency`
- `definition.size_category`
- `definition.creature_type`
- `definition.movement_mode`
- `definition.sense`
- `definition.language`
- `definition.damage_type`
- `definition.currency`
- `definition.equipment_property`
- `definition.weapon_mastery`
- `definition.spell_school`
- `definition.rest_policy`

### Actor construction / progression

- `definition.actor_archetype`
- `definition.species`
- `definition.background`
- `definition.class`
- `definition.subclass`
- `definition.advancement`
- `definition.feat`
- `definition.feature`

### Executable/state-bearing reusable content

- `definition.spell`
- `definition.asset`
- `definition.activity`
- `definition.resource`
- `definition.effect`
- `definition.condition`
- `definition.recipe`

### World-building / policy content

- `definition.hazard`
- `definition.terrain`
- `definition.environment`
- `definition.location_archetype`
- `definition.organization_archetype`
- `definition.mission_template`
- `definition.contract_template`
- `definition.mode_profile`

A reusable definition never becomes mutable world-instance state. A new executable primitive is engine work, not campaign-authored content.

---

## 3. World-record classes

Catalog generation 2 world owners are:

| ID | Responsibility |
|---|---|
| `world.actor` | particular PC/NPC/creature/companion current state, including source-Actor-owned non-epistemic continuity when retained |
| `world.actor_group` | independently identified group/roster/crowd where group identity matters |
| `world.asset` | particular item/document/vehicle/currency holding/object |
| `world.location` | particular place |
| `world.connection` | independently stateful traversable/lockable link |
| `world.zone` | mechanically relevant bounded area |
| `world.organization` | faction/government/guild/household/institution |
| `world.contract` | agreement and independently stateful obligations/terms |
| `world.mission` | independently tracked goal/stage/progression owner |
| `world.scene` | scene/environment current state and bounded routing context |
| `world.encounter` | world-facing encounter referent where independently useful; not generic Procedure authority |
| `world.hazard` | independently stateful placed/active hazard when hazard identity/lifecycle is required |
| `world.effect` | concrete Effect/Condition application owner |
| `world.lore_fact` | independently identified objective proposition + truth/lifecycle |
| `world.knowledge` | current fictional subject-to-proposition epistemic relation |

### Retired generic relationship record

`world.relationship` is **not** admitted in catalog generation 2.

R2.2 assigns subjective directed relationship continuity to the source Actor:

```text
(source_actor_id, target_subject_id)
    -> sparse trust / affinity / fear / respect / hostility / felt_obligation
```

Objective social facts remain with their natural owners such as organization membership, contract, ownership or another specific future typed owner. A future objective relation class must prove independent identity/lifecycle; the old generic `attitude/strength/status` container is not retained as an extensibility placeholder.

### Lore and knowledge

`world.lore_fact` uses separate axes:

```text
truth_status:
    truth.undetermined
    truth.established
    truth.disproven

record_status:
    lore_record.active
    lore_record.superseded
```

In-world disagreement does not add `truth.disputed`; it belongs to `world.knowledge`.

`world.knowledge` is conceptually keyed by `(knower_id, fact_id)` and uses:

```text
epistemic.aware
epistemic.known
epistemic.believed
epistemic.suspected
epistemic.rejected
```

Legacy Actor/PC/Faction embedded knowledge arrays are not parallel writable owners.

---

## 4. Runtime-record classes

Catalog generation 2 runtime owners are:

| ID | Responsibility |
|---|---|
| `runtime.session` | independently retained session coordination/lifecycle evidence where required |
| `runtime.message` | accepted communication evidence identity and retained exact/compacted payload state |
| `runtime.interaction` | one accepted external exchange/invocation identity |
| `runtime.intent_plan` | finite ordered material clauses from one Interaction |
| `runtime.command` | accepted idempotent root execution request + mandatory descendant closure disposition |
| `runtime.procedure` | independent procedure-local operational state owner |
| `runtime.resolution` | exactly one Activity invocation state |
| `runtime.continuation` | one suspended Resolution generation |
| `runtime.mechanical_event` | immutable committed mechanical evidence |
| `runtime.semantic_event` | compact accepted semantic-history evidence |
| `runtime.resolution_trace` | bounded diagnostic/calculation evidence |
| `runtime.disclosure` | sparse human-player material exposure relation |
| `runtime.collaboration_obligation` | bounded unresolved multi-human contribution collection/generation owner |
| `runtime.checkpoint` | optional immutable recovery/maintenance descriptor |
| `runtime.id_allocator` | allocation state only where the selected identity policy actually uses campaign allocation |
| `runtime.maintenance_audit` | maintenance/diagnostic audit object |
| `runtime.catalog_gap_report` | explicit unsupported-capability report |

### Disclosure

`runtime.disclosure` is conceptually keyed by `(player_id, fact_id)`. It owns material human exposure only. It does not own PC knowledge, objective truth or host read receipts.

### Collaboration

`runtime.collaboration_obligation` is admitted because R2.5 proves an independent recoverable lifecycle/generation when unresolved human input must survive participant/chat gaps and no native Procedure/Continuation/Choice owner already owns the response obligation.

It owns collection/waiting/current-generation state only, never gameplay consequence or PC control.

---

## 5. Values, not records

The following remain embedded typed values because they do not independently own lifecycle/state merely by crossing a phase/API boundary:

### Deterministic execution values

- `value.runtime_command`
- `value.action_request`
- `value.transition_request`
- `value.intent_clause`
- `value.target_spec`
- `value.area_spec`
- `value.duration_spec`
- `value.cost_spec`
- `value.signal`
- `value.contribution`
- `value.state_delta`
- `value.roll_request`
- `value.roll_result`
- `value.choice_request`
- `value.reaction_offer`
- `value.resolution_receipt`
- `value.execution_segment`
- `value.pending_child_invocation`
- `value.invocation_fact`
- `value.boundary_occurrence`
- `value.publication_manifest`
- `value.validation_issue`

### Step-4 / Round-2 typed gateway values

- `value.epistemic_delta`
- `value.role_context_request`
- `value.context_need_profile`
- `value.role_context_bundle`
- `value.context_trace`
- `value.context_budget_envelope`
- `value.turn_envelope`
- `value.interpreter_result`
- `value.preparation_draft`
- `value.actor_proposal`
- `value.story_projection_draft`
- `value.narration_result`
- `value.story_service_decision`

`RoleContextBundle`, `ContextTrace` and `TurnEnvelope` do not become campaign memory/current truth merely because implementations may serialize them for diagnostics or local execution.

---

## 6. Closed semantic/protocol vocabularies added in generation 2

Catalog generation 2 registers later accepted architecture where exact machine spelling was previously deferred.

### Actor continuity

- lifetimes: `actor_continuity.foundation`, `actor_continuity.durable_evolving`, `actor_continuity.transient_private`;
- cognition purposes: `cognition.react`, `cognition.reflect`, `cognition.plan`, `cognition.reconsider`, `cognition.relationship_update`;
- subjective relationship facets: `relationship.trust`, `relationship.affinity`, `relationship.fear`, `relationship.respect`, `relationship.hostility`, `relationship.felt_obligation`.

### Logical roles / Context Runtime

- roles: Interpreter, Dramaturg, Actor, Narrator, Chronicler, Commentator under `role.*` IDs;
- discovery channels: current scope, scene manifest, explicit ref, active dependency, live current, index lookup, history hint;
- representation classes: exact, full structured, compact structured, summary, reference only;
- assembly outcomes: assembled, assembled degraded, unsatisfiable.

These enums control deterministic assembly/routing contracts; they create no context authority.

### Chronicler service

- `story_service.no_backlog`
- `story_service.service`
- `story_service.defer`

No durable Story scheduler/job queue is implied.

### Collaboration / input

Coordination families:

- `collaboration.independent_immediate`
- `collaboration.agency_dependent_collective`
- `collaboration.rule_owned_ordered`

Input classes:

- `input.ooc_coordination`
- `input.diegetic_communication`
- `input.actionable_intent`
- `input.control_signal`

Collaboration lifecycle:

- `collaboration.open`
- `collaboration.closed`
- `collaboration.resolved`
- `collaboration.obsolete`

Typed explicit non-action results include pass/ready/no-further-input. Presence, silence and timeout are not equivalent results.

### Dramaturg planning content class

- `planning.source_anchored_constraint`
- `planning.provisional_dramaturgic_direction`

These classify noncanonical planning entries. They do not make planning a `world.*` owner.

### Chronology / recovery / Story / message retention

Closed vocabularies include:

- chronology relation kinds: causes, precedes, same-coordinate, elapsed;
- recovery outcomes: ready, retry, blocked;
- Story layers: transcript, events, mechanics, narrative;
- Story candidate dispositions: must-materialize, may-omit;
- message payload states: exact-retained, compacted.

Exact physical representations remain owned by their later R2.7 domains.

---

## 7. Durability/publication vocabulary correction

The superseded pre-rearchitecture catalog scaffold incorrectly represented `soft|hard` as intrinsic durability classes and exposed a generic publication-state ladder.

Step 5.5 instead defines independent logical axes:

```text
SEMANTIC SURVIVAL
    survival.ephemeral
    survival.established

CURRENT DURABILITY
    durability.durable
    durability.volatile_dirty

CURRENT OBLIGATION
    durability.may_defer
    durability.must_be_durable_before(edge)
```

`SOFT` and `HARD` remain useful prose shorthands; they are not persistent intrinsic fact types.

Step 5.6 final ref transition exposes exactly the epistemic outcomes:

- `repository_ref.confirmed_accepted`
- `repository_ref.confirmed_rejected`
- `repository_ref.indeterminate`

Prepared Git objects, queued work or a transport request do not become publication authority through a generic `publication.state` enum.

Therefore catalog generation 2 retires:

- `canonicality_classes`;
- old `durability_classes`;
- old generic `publication_states`;
- old `knowledge_modes`.

---

## 8. Noncanonical projection families remain outside world/runtime catalog classes

### Story

Story is a durable noncanonical source-bound projection with its own layer-local records, IDs and projection progress. It is deliberately not modeled as `world.story_*` or generic `runtime.memory`.

### Dramaturg horizons

Player-local and multiplayer-shared Dramaturg horizons are retained noncanonical prospective planning projections. Their exact record/root/schema and generation fencing are owned by WP-18. They are not admitted as world truth or generic runtime workflow classes by WP-03.

### Context products

RoleContextBundle, ContextTrace and transient recap/working continuity are values/projections, not durable record classes.

---

## 9. Extension boundary

HDM still has no generic plugin/provider/free-form executable extension architecture.

A new catalog addition must answer:

1. which class-admission category owns it;
2. why an existing class/value/facet cannot express it;
3. whether independent identity/lifecycle truly exists;
4. whether it adds executable engine behavior or validated data only;
5. which schema/tests/versioned registry change together.

Campaign/LLM content may add validated definitions but cannot invent new executable capability IDs or protocol authority.

---

## 10. Explicitly retired IDs/classes

At minimum, current machine contracts must not re-admit:

- `world.timeline_marker`;
- generic `world.relationship`;
- standalone Secret record authority;
- `runtime.dirty_record`;
- `runtime.publication_batch`;
- `runtime.execution_segment`;
- `runtime.resolution_chain`;
- `transition.timeline_place`;
- `transition.relationship_change` as a generic relationship owner mutation;
- `event.timeline.placed`;
- `event.relationship.changed` as a generic relationship-owner event;
- `truth.disputed` on the objective truth axis.

Later WPs may retire additional stale machine vocabulary when their owning semantics are examined. Existing IDs are never silently repurposed for a different meaning.

---

## 11. R2.7 handoff

WP-03 fixes class admission and the closed catalog vocabulary. It does **not** claim final answers for:

- Actor/Asset state field shapes — WP-04;
- execution-record schemas/identity details — WP-05;
- truth/knowledge/disclosure/message full schemas — WP-07;
- Context Runtime schema realization — WP-08/09;
- all durable record roots/schemas — WP-10;
- source-native IDs, sharding and index topology — WP-11;
- HOT/SQLite — WP-12;
- recovery/checkpoint — WP-14;
- chronology storage — WP-15;
- LIVE identity/fencing/packing — WP-16;
- collaboration full schema — WP-17;
- Story/planning projection schemas — WP-18.

Those domains may refine coordinated generation-2 machine artifacts before R2.7 final closure without creating a compatibility obligation to the discarded pre-rearchitecture scaffold. Current coordinated machine projections use integer `catalog_generation: 2`; any mixed or obsolete representation is rejected by maintenance audit/admission and does not redefine catalog generation as an engine-style three-component version.
