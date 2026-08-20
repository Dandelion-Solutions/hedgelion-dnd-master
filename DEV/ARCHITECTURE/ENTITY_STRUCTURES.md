# HDM Catalog — Minimum Entity Structures

Status: **AGREED BASELINE — STEP 1 ASSURANCE + STEP 2 MACHINE ALIGNMENT + STEP-4 CHAPTER RETIREMENT APPLIED**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable field and definition-binding inventory: `CATALOG/entity-structures.json`

Machine-readable identifier policy: `CATALOG/identifier-policies.json`,
validated by `SCHEMAS/identifier-policies.schema.json`.

Accepted nested models:

- `ARCHITECTURE/ACTOR_MODEL.md`;
- `ARCHITECTURE/ASSET_MODEL.md`;
- Step-2 mechanical-state specifications under `DEV/docs/superpowers/specs/`.

## 1. Field classes

Each definition `data` and world-record `state` has three field classes:

1. **required** — the minimum typed data needed to create a valid entity of
   that kind;
2. **expected** — typed fields recognized by schemas and runtime, populated
   when the information becomes known;
3. **details** — optional arbitrary JSON maintained by the LLM for descriptive
   characteristics that have no registered mechanical meaning.

An absent expected field means "not known or not applicable". It must not be
silently replaced with a guessed value. `details` is not a source of runtime
mechanics, references, constraints, or automatic indexes. If a recurring
property later becomes mechanically relevant, it receives one agreed typed
field and existing useful values may be migrated.

The universal definition/world envelopes and canonical class-admission rule are
owned by `ARCHITECTURE/CATALOG_CONTRACTS.md`.

## 2. Research basis and exclusions

The structures were compared with:

- D&D SRD 5.2.1 rules terminology and stat blocks;
- Foundry D&D5e actor, item, activity, resource, effect, and encounter data
  models;
- Avrae character/combat/initiative capabilities.

HDM adopts domain fields that represent game rules or persistent fiction. It
does not copy VTT presentation, token, sheet, icon, ownership-UI, or derived
roll-display fields. D&D has no standard storage model for organizations,
contracts, missions, lore, and abstract chronology; those structures are derived
from HDM requirements. Literary narrative records and Chapter grouping are not
world state: they belong to non-canonical `STORY/NARRATIVE` and its index under
the canonical Step-4 Story contract.

## 3. Definition kinds

Fields below are inside the definition's `data`. The common `id`, `kind`,
localized `name`, optional `facets`, and optional `tags` remain in the envelope.

| Kind | Required | Expected |
|---|---|---|
| `definition.ability` | — | `abbreviation` |
| `definition.skill` | `ability_id` | `activity_ids`, `applications` |
| `definition.proficiency` | — | `category`, `applicable_definition_ids` |
| `definition.size_category` | — | `space`, `carrying_multiplier` |
| `definition.creature_type` | — | `subtype_ids` |
| `definition.movement_mode` | — | `unit`, `environmental_requirements` |
| `definition.sense` | — | `range`, `limitations` |
| `definition.language` | — | `script`, `rarity` |
| `definition.damage_type` | — | `category` |
| `definition.currency` | — | `base_ratio`, `physical_asset_id` |
| `definition.equipment_property` | — | `activity_ids`, `rule_elements`, `trigger_bindings` |
| `definition.weapon_mastery` | `activity_id` | `requirements` |
| `definition.spell_school` | — | — |
| `definition.rest_policy` | `duration`, `completion_boundary_id` | `requirements`, `interruption_policy_id` |
| `definition.actor_archetype` | — | `creature_type_id`, `size_id`, `abilities`, `resources`, `activity_ids`, `feature_ids`, `life_state_policy_id` |
| `definition.species` | `size_options`, `speed` | `creature_type_id`, `feature_ids`, `language_ids` |
| `definition.background` | — | `ability_options`, `proficiency_options`, `feat_ids`, `equipment_options` |
| `definition.class` | `hit_die` | `primary_ability_ids`, `proficiency_ids`, `resource_ids`, `advancement_id` |
| `definition.subclass` | `class_id` | `feature_ids`, `advancement_id` |
| `definition.advancement` | `levels` | `prerequisites`, `grants` |
| `definition.feat` | — | `prerequisites`, `activity_ids`, `rule_elements`, `trigger_bindings` |
| `definition.feature` | — | `activity_ids`, `resource_ids`, `effect_ids`, `rule_elements`, `trigger_bindings` |
| `definition.spell` | `level`, `school_id`, `activity_ids` | `components`, `casting_time`, `range`, `duration`, `concentration`, `ritual` |
| `definition.asset` | — | `physical`, `value`, `rarity`, `property_ids`, `activity_ids`, `resource_ids`, `effect_ids`, `rule_elements`, `trigger_bindings`, `handling`, `capacity`, `stack`, `attunement`, `durability` |
| `definition.activity` | `family_id`, `steps` | `activation`, `requirements`, `targeting`, `costs` |
| `definition.resource` | `mechanic_id`, `lifetime_owner`, `state_model` | `capacity`, `recovery`, `spending_policy_id` |
| `definition.effect` | — | `duration`, `parameter_schema`, `rule_elements`, `trigger_bindings`, `scheduled_triggers`, `activity_ids`, `reapplication`, `arbitration_policy_id` |
| `definition.condition` | `aggregation_policy_id` | `parameter_schema`, `value_constraints`, `intrinsic_mechanics`, `automatic_boundary_responses` |
| `definition.recipe` | `inputs`, `outputs` | `activity_id`, `duration`, `requirements` |
| `definition.hazard` | — | `detection`, `trigger_bindings`, `activity_ids`, `disable_activity_ids` |
| `definition.terrain` | — | `movement_rules`, `visibility_rules`, `hazard_ids` |
| `definition.environment` | — | `effect_ids`, `hazard_ids`, `rest_modifiers` |
| `definition.location_archetype` | — | `facet_ids`, `environment_ids`, `connection_defaults` |
| `definition.organization_archetype` | — | `role_definitions`, `relationship_defaults` |
| `definition.mission_template` | — | `stage_templates`, `objective_templates`, `reward_definitions` |
| `definition.contract_template` | — | `party_roles`, `obligation_templates`, `breach_rules` |
| `definition.mode_profile` | `resolution_policy` | `enabled_subsystems`, `information_policy`, `timing_policy` |

An empty required list is intentional. A language, damage type, decorative
asset, narrative effect, or template may be valid before it has mechanical
attachments. Empty placeholder values are not required.

Rule Elements and immediate Trigger Bindings are embedded value objects, not
definition kinds. Their contracts are specified by `RULE_ELEMENT_MODEL.md`;
Activity data is specified by `ACTIVITY_MODEL.md`. The corresponding structural
schemas are `SCHEMAS/rule-element.schema.json`,
`SCHEMAS/trigger-binding.schema.json`, and
`SCHEMAS/activity-definition-data.schema.json`.

Step-2 definition shapes are further constrained by:

- `SCHEMAS/resource-definition-data.schema.json`;
- `SCHEMAS/effect-definition-data.schema.json`;
- `SCHEMAS/condition-definition-data.schema.json`;
- `SCHEMAS/rest-policy-definition-data.schema.json`;
- `SCHEMAS/duration-spec.schema.json`.

Effect reapplication keeps matching semantics separate from the lifecycle
action. `reapplication.match_policy_id` chooses the existing target/family
application set (with optional same-source restriction in the initial closed
vocabulary), while `reapplication.action_id` is only `refresh` or `replace`.
Absence of `reapplication` retains the default create-new-application behavior.

A `definition.effect` may also declare a finite owner-local
`scheduled_triggers` map for proven elapsed-time mechanics that must invoke a
bounded Activity while the Effect remains live. Each declaration has a stable
local key, one positive metric `after` delay, and one `activity_id`. This is not
a generic callback/scheduler language and does not replace boundary/Event
TriggerBindings for turn, dawn, rest, or other native semantic/procedure edges.
The authoritative amendment is
`DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md`.

Condition aggregation and intrinsic-rule evaluation are deliberately separate:
`aggregation_policy_id` determines effective named-Condition state and member
applications; every item in `intrinsic_mechanics` independently declares
`aggregate_once` or `per_effective_application` scope. A Condition may also own
closed deterministic `automatic_boundary_responses` over its own applications;
for example Exhaustion can remove one eligible unit on a completed Long Rest
without making RestPolicy the owner of Condition mutation.

## 4. World-record kinds and definition compatibility

Fields below are inside `state`. `definition_id` stays in the universal envelope,
but `CATALOG/entity-structures.json` declares whether it is forbidden, optional,
or required for each world kind and which reusable definition kinds are legal.
The loader validates the relation; it is not inferred from names.

| Kind | Required state | Expected state | `definition_id` binding |
|---|---|---|---|
| `world.actor` | `name` | `roles`, `location_id`, `build`, `abilities`, `hp`, `life_state_id`, `life_state_policy_id`, `life_state_progress`, `resources` | optional `definition.actor_archetype` |
| `world.actor_group` | `name` | `member_ids`, `leader_id`, `location_id`, `purpose` | forbidden |
| `world.asset` | — | `owner_actor_id`, `container_asset_id`, `location_id`, `quantity`, `equipment`, `attuned_actor_id`, `resources`, `durability`, `access` | optional `definition.asset` |
| `world.location` | `name` | `parent_location_id`, `organization_id`, `environment_ids`, `status` | optional `definition.location_archetype` |
| `world.connection` | `from_location_id`, `to_location_id` | `direction`, `traversal_activity_id`, `status`, `requirements` | forbidden |
| `world.zone` | `location_id`, `name` | `participant_ids`, `effect_ids`, `geometry`, `status` | forbidden |
| `world.organization` | `name` | `member_ids`, `leader_ids`, `location_ids`, `resources`, `status` | optional `definition.organization_archetype` |
| `world.relationship` | `subject_id`, `object_id`, `relation` | `attitude`, `strength`, `status` | forbidden |
| `world.contract` | `party_ids`, `terms`, `status` | `obligations`, `deadlines`, `collateral_asset_ids`, `breach_consequences` | optional `definition.contract_template` |
| `world.mission` | `name`, `status` | `stages`, `participant_ids`, `location_ids`, `reward_ids`, `dependencies` | optional `definition.mission_template` |
| `world.scene` | `name` | `location_id`, `participant_ids`, `focal_entity_ids`, `status` | forbidden |
| `world.encounter` | `participant_ids`, `status` | `scene_id`, `initiative`, `round`, `active_participant_id`, `local_time` | forbidden |
| `world.hazard` | `status` | `location_id`, `zone_id`, `detected_by_actor_ids`, `effect_ids` | optional `definition.hazard` |
| `world.effect` | `target_id`, `lifecycle` | `source_id`, `rules_origin_id`, `parameters`, `support_effect_id`, `temporal_binding`, `scheduled_trigger_state` | required `definition.effect` or `definition.condition` |
| `world.lore_fact` | `statement`, `truth_status` | `subject_ids`, `chronology`, `importance` | forbidden |
| `world.knowledge` | `fact_id`, `knower_id`, `status` | `learned_from_id`, `confidence` | forbidden |
| `world.timeline_marker` | `slot`, `summary` | `entity_ids`, `scene_id`, `relative_to` | forbidden |

Literary records and Chapter groupings are deliberately absent from this table.
They belong to the non-canonical `STORY/NARRATIVE` projection and its Story
index, not to a `world.*` state owner or definition-binding contract.

`world.organization` intentionally does **not** keep a second
`state.archetype_id`; its reusable archetype relationship is the universal
`definition_id` binding. The same one-path rule applies to every world kind.

A reusable definition does not imply a same-named world record. A
`definition.condition` materializes through `world.effect` when applied. A
`definition.hazard` may be provenance for an Actor-local Effect/Condition rather
than materializing a `world.hazard` when the placed-hazard lifecycle is not the
actual state owner.

Additional kind rules:

- An actor's inventory and active effects are reverse projections of
  `world.asset.owner_actor_id` and `world.effect.target_id`; they are not
  duplicated in actor state. Organizational allegiance is represented by
  organization membership and relationships.
- `hp` and `life_state_id` are separate Actor-state authorities. When `hp` is
  materialized, `life_state_id` is required as well; zero HP alone never
  determines death, destruction, or transformation.
- `life_state_progress` is state-local authority: Dying owns death-save progress,
  Stable owns its concrete automatic-recovery `TemporalBinding`, and Active/Dead
  own no dying/stable progress.
- Persistent Actor/Asset ResourceState owns its stored `current` amount and may
  own a concrete `recovery_binding`; procedure-local ResourceState owns `spent`.
  Resource definition/schema forbids swapping those storage models. The Temporal
  Agenda remains a derived due index over authoritative bindings rather than a
  second scheduler authority.
- `world.asset` may have empty `state` when its definition contains all stable
  properties and no mutable fact is yet known.
- One independent target-local application is one `world.effect`; `target_id` is
  singular. Generic mutable `stacks`, stored arbitration winner/shadow state,
  copied Condition presence/value, reverse support children, and writable
  remaining-duration countdowns are not world-effect authorities.
- `world.effect.temporal_binding` owns only intrinsic Effect lifetime timing.
  Independently, a live Effect may own `scheduled_trigger_state[key]`, where one
  concrete `TemporalBinding` is the next-due state for a declared owner-local
  scheduled trigger. A terminal Effect cannot retain armed scheduled-trigger
  state. The Temporal Agenda indexes both forms but owns neither.
- Each `scheduled_trigger_state` key must exist in the resolved owning Effect
  definition's `scheduled_triggers`; loader/compiler validation enforces this
  cross-record contract rather than inventing a second stored declaration.
- `world.effect` requires `definition_id`; its definition must be an allowed
  Effect or Condition definition according to the machine binding table.
- Maintained/concentration support is represented by immutable
  `support_effect_id`; concentration is not a duration mode.
- `world.hazard` may exist without a definition while still narrative/local; if
  it carries `definition_id`, only `definition.hazard` is compatible.
- `world.knowledge` separates who knows a fact from the truth stored in
  `world.lore_fact`.
- `world.zone` exists only for a mechanically or operationally significant
  region. Descriptive parts of a room remain prose/details.

## 5. SQLite projection

SQLite is a disposable HOT-state projection, not durable canon. The base table
stores the universal envelope as ordinary columns and the kind-specific body as
JSON:

```sql
CREATE TABLE world_records (
    id            TEXT PRIMARY KEY,
    kind          TEXT NOT NULL,
    definition_id TEXT,
    state_json    TEXT NOT NULL CHECK (json_valid(state_json))
);
```

Presence of the nullable SQL column does not authorize `definition_id` for every
world kind. Hydration/validation uses `definition_binding` before a record is
accepted into the typed runtime.

HDM does not add `UNIQUE` constraints for kind-specific gameplay fields merely
because SQLite can support them. Canonical identity and conflict policy belong
to runtime/checkpoint logic. The table's technical `PRIMARY KEY` is still
required for local row identity and efficient replacement; it does not assert a
new gameplay-level uniqueness rule.

Frequently queried typed fields may receive generated columns, expression
indexes, or partial indexes. Expected fields may be indexed when their access
pattern justifies it; requiredness alone is not a reason to duplicate or index
a value.

```sql
CREATE INDEX actor_location_idx
ON world_records(json_extract(state_json, '$.location_id'))
WHERE kind = 'world.actor';
```

References that need fast reverse lookup may be projected into a disposable
`record_refs(source_id, field, target_id)` table. `details` is never indexed
automatically.

Condition/effect/resource/temporal reverse indexes are likewise HOT projections.
They may be rebuilt from authoritative records and continuity-critical runtime
checkpoints; they are never written back as alternate world authority merely to
make a lookup cheap.

## 6. Current design boundary

This inventory fixes field membership and world-definition compatibility through
the Step-1 retrospective assurance correction, Step-2 machine alignment, and
the Step-4 retirement of literary Chapter from the world-record namespace,
including the Slice-C owner-local scheduled-trigger amendment. Actor and asset
nested shapes are accepted in `ARCHITECTURE/ACTOR_MODEL.md` and
`ARCHITECTURE/ASSET_MODEL.md`; Activity and Rule Element shapes are defined by
`ARCHITECTURE/ACTIVITY_MODEL.md` and `ARCHITECTURE/RULE_ELEMENT_MODEL.md`.
Machine contracts are validated by schemas/catalogs under `DEV/` and focused
unit tests, including `DEV/TESTS/test_catalog_definition_binding_contract.py`,
`DEV/TESTS/test_step2_scheduled_trigger_contract.py`, and
`DEV/TESTS/test_step4_story_retirement_contract.py`.

Exact IntentPlan/Resolution ordering, prospective-overlay representation,
event/receipt identity, scheduled-trigger due execution/re-arm, reaction
suspension, source-sensitive remove-one adjudication, multiplayer reconciliation,
and repository continuity-checkpoint publication remain owned by later roadmap
stages and are not silently encoded here.
