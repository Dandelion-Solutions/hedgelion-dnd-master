# HDM Catalog — Minimum Entity Structures

Status: **AGREED BASELINE — STEP 2 MACHINE ALIGNMENT APPLIED**

Target: `feature/mechanical-runtime-hot-state`

Machine-readable field inventory: `CATALOG/entity-structures.json`

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

The universal definition and world-record envelopes remain defined by
`ARCHITECTURE/CATALOG_CONTRACTS.md`.

## 2. Research basis and exclusions

The structures were compared with:

- D&D SRD 5.2.1 rules terminology and stat blocks;
- Foundry D&D5e actor, item, activity, resource, effect, and encounter data
  models;
- Avrae character/combat/initiative capabilities.

HDM adopts domain fields that represent game rules or persistent fiction. It
does not copy VTT presentation, token, sheet, icon, ownership-UI, or derived
roll-display fields. D&D has no standard storage model for organizations,
contracts, missions, lore, chapters, and abstract chronology; those structures
are derived from HDM requirements.

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
| `definition.effect` | — | `duration`, `parameter_schema`, `rule_elements`, `trigger_bindings`, `activity_ids`, `reapplication_policy_id`, `arbitration_policy_id` |
| `definition.condition` | `aggregation_policy_id` | `parameter_schema`, `value_constraints`, `intrinsic_mechanics` |
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

Rule Elements and Trigger Bindings are embedded value objects, not definition
kinds. Their contracts are specified by `RULE_ELEMENT_MODEL.md`; Activity data
is specified by `ACTIVITY_MODEL.md`. The corresponding structural schemas are
`SCHEMAS/rule-element.schema.json`, `SCHEMAS/trigger-binding.schema.json`, and
`SCHEMAS/activity-definition-data.schema.json`.

Step-2 definition shapes are further constrained by:

- `SCHEMAS/resource-definition-data.schema.json`;
- `SCHEMAS/effect-definition-data.schema.json`;
- `SCHEMAS/condition-definition-data.schema.json`;
- `SCHEMAS/rest-policy-definition-data.schema.json`;
- `SCHEMAS/duration-spec.schema.json`.

Condition aggregation and intrinsic-rule evaluation are deliberately separate:
`aggregation_policy_id` determines effective named-Condition state and member
applications; every item in `intrinsic_mechanics` independently declares
`aggregate_once` or `per_effective_application` scope.

## 4. World-record kinds

Fields below are inside `state`. `definition_id` remains in the universal
envelope and may be made mandatory by a kind-specific schema.

| Kind | Required | Expected |
|---|---|---|
| `world.actor` | `name` | `roles`, `location_id`, `build`, `abilities`, `hp`, `life_state_id`, `life_state_policy_id`, `life_state_progress`, `resources` |
| `world.actor_group` | `name` | `member_ids`, `leader_id`, `location_id`, `purpose` |
| `world.asset` | — | `owner_actor_id`, `container_asset_id`, `location_id`, `quantity`, `equipment`, `attuned_actor_id`, `resources`, `durability`, `access` |
| `world.location` | `name` | `parent_location_id`, `organization_id`, `environment_ids`, `status` |
| `world.connection` | `from_location_id`, `to_location_id` | `direction`, `traversal_activity_id`, `status`, `requirements` |
| `world.zone` | `location_id`, `name` | `participant_ids`, `effect_ids`, `geometry`, `status` |
| `world.organization` | `name` | `archetype_id`, `member_ids`, `leader_ids`, `location_ids`, `resources`, `status` |
| `world.relationship` | `subject_id`, `object_id`, `relation` | `attitude`, `strength`, `status` |
| `world.contract` | `party_ids`, `terms`, `status` | `obligations`, `deadlines`, `collateral_asset_ids`, `breach_consequences` |
| `world.mission` | `name`, `status` | `stages`, `participant_ids`, `location_ids`, `reward_ids`, `dependencies` |
| `world.scene` | `name` | `location_id`, `participant_ids`, `focal_entity_ids`, `status` |
| `world.encounter` | `participant_ids`, `status` | `scene_id`, `initiative`, `round`, `active_participant_id`, `local_time` |
| `world.hazard` | `status` | `location_id`, `zone_id`, `detected_by_actor_ids`, `effect_ids` |
| `world.effect` | `target_id`, `lifecycle` | `source_id`, `rules_origin_id`, `parameters`, `support_effect_id`, `temporal_binding` |
| `world.lore_fact` | `statement`, `truth_status` | `subject_ids`, `chronology`, `importance` |
| `world.knowledge` | `fact_id`, `knower_id`, `status` | `learned_from_id`, `confidence` |
| `world.chapter` | `title`, `body` | `entity_ids`, `scene_ids`, `timeline_span`, `visibility` |
| `world.timeline_marker` | `slot`, `summary` | `entity_ids`, `scene_id`, `relative_to` |

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
  own a concrete `recovery_binding`; the Temporal Agenda remains a derived due
  index over authoritative bindings rather than a second scheduler authority.
- `world.asset` may have empty `state` when its definition contains all stable
  properties and no mutable fact is yet known.
- One independent target-local application is one `world.effect`; `target_id` is
  singular. Generic mutable `stacks`, stored arbitration winner/shadow state,
  copied Condition presence/value, reverse support children, and writable
  remaining-duration countdowns are not world-effect authorities.
- `world.effect` requires `definition_id` in its kind-specific envelope. Its
  definition may be an Effect or Condition definition according to loader
  validation.
- Maintained/concentration support is represented by immutable
  `support_effect_id`; concentration is not a duration mode.
- `world.hazard` normally uses `definition_id`; an improvised narrative hazard
  may exist without one until it gains mechanics.
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

This inventory fixes field membership through the Step-2 machine alignment.
Actor and asset nested shapes are accepted in `ARCHITECTURE/ACTOR_MODEL.md` and
`ARCHITECTURE/ASSET_MODEL.md`; Activity and Rule Element shapes are defined by
`ARCHITECTURE/ACTIVITY_MODEL.md` and `ARCHITECTURE/RULE_ELEMENT_MODEL.md`.
Step-2 machine contracts are validated by the schemas/catalogs under `DEV/` and
focused tests in `DEV/TESTS/test_step2_machine_contracts.py` and
`DEV/TESTS/test_step2_mechanical_examples.py`.

Exact IntentPlan/Resolution ordering, prospective-overlay representation,
event/receipt identity, reaction suspension, multiplayer reconciliation, and
repository continuity-checkpoint publication remain owned by later roadmap
stages and are not silently encoded here.
