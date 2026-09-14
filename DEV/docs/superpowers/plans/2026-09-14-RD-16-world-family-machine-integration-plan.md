# RD-16 — World-Family Machine Contract / Shared Catalog Integration — Executable Implementation Plan

Status: **AUTHOR GRAPH REPAIR — NEW BOUNDED RD / PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Findings: **AUTHOR GRAPH FINDING 12 — SIGNIFICANT; AUTHOR GRAPH FINDING 13 — SIGNIFICANT**

> For implementation workers: execute only after independent Senior plan GO and under current HDM TDD/process rules. This RD does not authorize production implementation.

## 1. Why this RD exists

Two post-graph defects remain after the earlier family/identity repairs.

### Finding 12 — strict world-family machine shape is incomplete

The final accepted v1 world-family census is 17 kinds:

```text
world.actor
world.actor_group
world.asset
world.location
world.connection
world.zone
world.organization
world.contract
world.mission
world.scene
world.encounter
world.hazard
world.effect
world.lore_fact
world.knowledge
world.thread
world.player
```

`world.faction` is not an independent native family; it is superseded by `world.organization` plus classification/facet semantics.

Current `DEV/SCHEMAS/world-record.schema.json` dispatches strict state schemas for only five current families (`actor`, `actor_group`, `asset`, `location`, `effect`). Other admitted `world.*` records can pass through the generic `state: object` envelope, so catalog admission/structure inventory is not equivalent to exact family validation. R018 requires per-family machine realization, not aggregate kind counts.

### Finding 13 — shared machine files have multiple planned independent writers

The post-graph package separately requires:

- RD-08 / WP-15 `world.thread` admission/structure/identity;
- Finding 8 / RD-04 `world.player` admission/structure/identity;
- RD-05 / Finding 10 MechanicalEvent composite identity;
- Finding 7 / WP-16 exhaustive `live_birth` policy table and identifier-policy schema v3;
- RD-15 `runtime.catalog_gap_report` final policy participation;
- existing catalog projections/conformance updates.

Those repairs overlap physical files including `core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, their schemas/admission ledgers/projections and conformance tests. Independent workers editing them in parallel would make the final machine contract order-dependent even when every semantic delta is individually correct.

RD-16 is therefore a **machine-contract integration RD**. It does not become semantic authority for the underlying families.

## 2. Authority boundary

Semantic owners remain unchanged:

- current S6D/catalog architecture owns the existing 15 world kinds and binding modes;
- RD-08/WP-15 owns `world.thread` semantics/state contract;
- WP-16 + Finding 8 own `world.player` campaign identity/access semantics;
- RD-05 owns MechanicalEvent identity `(segment_id,event_ordinal)`;
- WP-16 owns per-kind LIVE-born disposition;
- RD-15 owns deterministic runtime catalog binding and `runtime.catalog_gap_report` behavior.

RD-16 owns only:

1. exhaustive final world-state schema realization;
2. fail-closed `world-record` dispatch/binding validation;
3. one ordered physical integration checkpoint for shared catalog/identity machine files;
4. item-bound conformance proof that the accepted semantic deltas appear together in one coherent final machine generation.

Owner-local work may reach `LOCAL_SEMANTIC_READY`. A semantic RD whose required shared machine delta has not yet passed RD-16 remains **integration-pending** and may not claim package-level R018/machine closure.

## 3. Exact impact envelope

### Create strict world-state schemas

```text
DEV/SCHEMAS/world-connection-state.schema.json
DEV/SCHEMAS/world-zone-state.schema.json
DEV/SCHEMAS/world-organization-state.schema.json
DEV/SCHEMAS/world-contract-state.schema.json
DEV/SCHEMAS/world-mission-state.schema.json
DEV/SCHEMAS/world-scene-state.schema.json
DEV/SCHEMAS/world-encounter-state.schema.json
DEV/SCHEMAS/world-hazard-state.schema.json
DEV/SCHEMAS/world-lore-fact-state.schema.json
DEV/SCHEMAS/world-knowledge-state.schema.json
DEV/SCHEMAS/world-player-state.schema.json
DEV/TESTS/test_rd16_world_family_machine_integration.py
```

### Consume / validate owner-local schema

`DEV/SCHEMAS/world-thread-state.schema.json` remains created by RD-08 because thread semantics belong there. RD-16 consumes its final GREEN owner-local contract and validates it in the 17-family wrapper/census.

### Modify final machine integration surfaces

```text
DEV/SCHEMAS/world-record.schema.json
DEV/CATALOG/core-catalog.json
DEV/CATALOG/entity-structures.json
DEV/CATALOG/identifier-policies.json
DEV/CATALOG/catalog-admission-ledger/families/world_record_kinds.json
DEV/SCHEMAS/identifier-policies.schema.json
DEV/ARCHITECTURE/CATALOG_INVENTORY.md
DEV/ARCHITECTURE/ENTITY_STRUCTURES.md
DEV/TESTS/test_r2_7_wp03_catalog_conformance.py
DEV/TOOLS/audit_engine.py                  # only exact new/stale conformance assertions
DEV/PROJECT_MAP.md                         # routing only
```

Modify any additional current catalog schema/projection only when a focused RED test demonstrates that the final accepted machine set cannot validate without it. Name the exact current file before editing; do not create a second registry.

## 4. Final 17-family schema matrix

The integration test must enumerate these exact members; counts alone are insufficient.

| Family | Strict state contract | Required top-level owner fields |
|---|---|---|
| `world.actor` | existing `world-actor-state.schema.json` | current `entity-structures` row |
| `world.actor_group` | existing `world-actor-group-state.schema.json` | `name` |
| `world.asset` | existing `world-asset-state.schema.json` | current row |
| `world.location` | existing `world-location-state.schema.json` | `name` |
| `world.connection` | new `world-connection-state.schema.json` | `from_location_id,to_location_id` |
| `world.zone` | new `world-zone-state.schema.json` | `location_id,name` |
| `world.organization` | new `world-organization-state.schema.json` | `name` |
| `world.contract` | new `world-contract-state.schema.json` | `party_ids,terms,status` |
| `world.mission` | new `world-mission-state.schema.json` | `name,status` |
| `world.scene` | new `world-scene-state.schema.json` | `name` |
| `world.encounter` | new `world-encounter-state.schema.json` | `participant_ids,status` |
| `world.hazard` | new `world-hazard-state.schema.json` | `status` |
| `world.effect` | existing `world-effect-state.schema.json` | `target_id,lifecycle` |
| `world.lore_fact` | new `world-lore-fact-state.schema.json` | `statement,truth_status,record_status` |
| `world.knowledge` | new `world-knowledge-state.schema.json` | `knower_id,fact_id,stance` |
| `world.thread` | RD-08 `world-thread-state.schema.json` | final RD-08/WP-15 owner contract |
| `world.player` | new `world-player-state.schema.json` | `status,controlled_pc_ids`; stable campaign identity stays envelope `id`/player_id |

The test must compare actual schema required/property sets against the **final** `DEV/CATALOG/entity-structures.json` row, not a duplicated hard-coded inventory alone. Owner-specific additional invariants may make a schema stricter than the row but may not silently omit an owner field.

## 5. Strict schema construction law

Every state schema in this layer uses the existing DEV strict-state style:

```text
object
additionalProperties = false
owner-required fields = required
owner-expected fields = admitted properties
optional details = object, descriptive/nonmechanical only
```

Use exact stronger value contracts where an accepted owner already defines them. Examples:

- machine IDs/refs: nonempty constrained strings;
- ID/ref sets: unique arrays of constrained strings;
- `world.lore_fact.truth_status`: `truth.undetermined | truth.established | truth.disproven`;
- `world.lore_fact.record_status`: `active | superseded`;
- `world.knowledge.stance`: `epistemic.aware | epistemic.known | epistemic.believed | epistemic.suspected | epistemic.rejected`;
- temporal fields: reuse accepted `temporal-binding.schema.json` or typed chronology-value contracts only where the semantic owner actually establishes that equivalence;
- PLAYER: preserve current accepted status/authorization/binding/control semantics, including stable GitHub `user_id`, mutable login convenience only, controlled-PC relations, inactive/reactivation law, preferences/policy authority and provenance fields.

For complex owner fields whose inner wire representation is intentionally not canonical yet (for example contract terms/obligations, mission stages/dependencies, zone geometry, organization resources, lore chronology/scope or optional knowledge confidence), enforce the **minimum non-semantic structural type** needed to close the top-level family shape. Do not invent enums, numeric scales, ordering, chronology semantics, new authority, or gameplay policy merely to make JSON Schema more detailed.

A reusable local `structuredValue` may admit object and/or array only where the canonical owner leaves the container representation open. Optional confidence may use a bounded machine scalar union without inventing a 0..1 scale. Any later stronger native owner supersedes the coarse value type through normal Version Impact.

`details` never provides a bypass for required/expected mechanical fields and never becomes executable mechanic authority.

## 6. Fail-closed world envelope

Replace permissive `world-record.schema.json` behavior with exact final dispatch.

Required laws:

1. `kind` is one of the exact 17 accepted world kinds, not merely a `^world\.` regex.
2. Every accepted kind selects exactly one strict state schema.
3. `world.faction` and every unknown/unadmitted `world.*` value fail validation.
4. Definition binding follows final `entity-structures.json` mode:
   - `required`: envelope requires `definition_id`;
   - `forbidden`: envelope rejects `definition_id`;
   - `optional`: envelope may carry it.
5. Schema-level binding mode does not pretend to prove referenced definition kind/currentness; catalog conformance/runtime validation retains that responsibility.
6. `id` remains the native stable record identity; ID lexical order carries no chronology/currentness meaning.

The wrapper may be generated/composed from one checked machine mapping, but generation must remain deterministic and auditable; no runtime discovery of schemas by directory scan.

## 7. Shared machine integration checkpoint

RD-16 is the only final physical writer for the shared post-graph machine cutover. Semantic producer RDs provide accepted deltas; they do not race commits to these shared files.

Input set:

```text
RD-08 LOCAL_SEMANTIC_READY:
  world.thread state + admission/structure/default identity requirements

RD-04 / Finding 8 LOCAL_SEMANTIC_READY:
  world.player admission/structure/campaign identity + false world.faction disposition

RD-05 / Finding 10 LOCAL_SEMANTIC_READY:
  runtime.mechanical_event composite identity [segment_id,event_ordinal]

RD-09 / Finding 7 LOCAL_SEMANTIC_READY:
  identifier-policy schema v3 + exhaustive 17 world / 17 runtime live_birth table

RD-15 LOCAL_SEMANTIC_READY:
  runtime.catalog_gap_report final campaign identity / live_birth=FORBIDDEN participation

RD-16 family-schema work:
  complete 17-family strict world schema/wrapper realization
```

Final physical checkpoint applies all accepted deltas together to:

- catalog kind census/admission;
- structures/binding modes;
- identifier policies and schema v3;
- prose projections;
- world wrapper/state-schema references;
- conformance/audit tests.

The checkpoint may not publish a state where one required delta is intentionally RED or deferred to a later shared-file worker. Missing owner-local input blocks the final integration checkpoint; it does not license a partial catalog generation.

## 8. TDD / checkpoint choreography

### Task 1 — RED: expose family-dispatch incompleteness

Create `DEV/TESTS/test_rd16_world_family_machine_integration.py` with:

```text
WorldFamilyCensusTests
WorldStateSchemaCoverageTests
WorldEnvelopeDispatchTests
DefinitionBindingModeTests
SharedCatalogIntegrationTests
R018WorldFamilyProofTests
```

Initial RED proves at least:

- current wrapper accepts an unadmitted `world.fake`/unknown kind;
- current wrapper admits arbitrary state for one quiet admitted family;
- ten current quiet families have no dedicated strict state schema;
- `world.thread`/`world.player` are missing from the current catalog generation before their owner deltas integrate;
- false `world.faction` cannot appear in the final family set;
- independently applying only one shared writer delta cannot satisfy the final census/policy conformance.

Do not publish a RED-only checkpoint.

### Task 2 — GREEN: quiet-family strict schemas

Create the ten quiet-family schemas listed above.

Tests prove:

- every `entity-structures` required field is schema-required;
- every expected owner field is admitted explicitly;
- unknown top-level fields fail except `details` contents;
- known IDs/ref sets reject empty/invalid shapes as appropriate;
- lore truth/record status and knowledge stance use canonical closed vocabularies;
- no invented chronology/order/confidence scale is introduced.

Focused verify:

```bash
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration.WorldStateSchemaCoverageTests -v
```

### Task 3 — GREEN: PLAYER + thread integration inputs

Create `world-player-state.schema.json` from the accepted WP-16/Finding-8/current PLAYER contract; consume RD-08 final `world-thread-state.schema.json` without redefining thread semantics.

PLAYER tests include:

- `active|inactive` status only;
- stable external authorization binding uses GitHub `user_id`, not mutable login;
- controlled-PC IDs retained through inactive/reactivation;
- LIVE birth/claim of `world.player` rejected by final policy;
- policy/preferences remain campaign authority/presentation only and cannot bypass mechanics/currentness.

If RD-08 thread schema is not yet GREEN/current, Task 3 remains integration-pending rather than creating a competing thread schema.

### Task 4 — GREEN: fail-closed 17-kind wrapper

Modify `world-record.schema.json`.

Tests enumerate all exact 17 positive cases plus negatives for:

```text
world.faction
world.fake
unknown future world kind
wrong-family state shape
definition_id on forbidden family
missing definition_id on required family
```

Focused verify:

```bash
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration.WorldFamilyCensusTests DEV.TESTS.test_rd16_world_family_machine_integration.WorldEnvelopeDispatchTests DEV.TESTS.test_rd16_world_family_machine_integration.DefinitionBindingModeTests -v
```

### Task 5 — GREEN: single shared catalog/identity machine checkpoint

Fresh-read all semantic input artifacts immediately before editing. Apply thread/player/MechanicalEvent/live-birth/RD-15 deltas in one coherent final machine state.

Required final assertions:

- world kind census exactly 17;
- runtime kind census exactly 17;
- no independent world.faction;
- entity structures exactly cover admitted world kinds;
- identifier-policy schema version 3, catalog generation remains 2 unless normal Version Impact proves a different required change;
- every admitted world/runtime kind has explicit `live_birth` disposition;
- `runtime.mechanical_event` is composite `[segment_id,event_ordinal]`, never campaign sequential;
- `world.player` is campaign-owned and LIVE birth forbidden;
- `world.knowledge` retains owner-equivalent composite `(knower_id,fact_id)` LIVE identity semantics;
- `runtime.catalog_gap_report` LIVE birth forbidden;
- campaign allocator tests reject non-sequential/forbidden paths;
- admission ledger/prose projections match machine bytes.

Focused verify:

```bash
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration.SharedCatalogIntegrationTests -v
python3 -m unittest DEV.TESTS.test_r2_7_wp03_catalog_conformance -v
```

### Task 6 — R018 item-bound integration proof

For each of the 17 world families prove:

```text
semantic owner
-> admitted machine kind
-> exact structure/binding mode
-> strict state schema
-> identity/live_birth policy
-> native route/root
-> owning semantic RD/producers
-> RD-06 durability publication where applicable
-> RD-07 current-native recovery/non-authority
-> item-bound proof witness
```

This is a family matrix, not a count-only assertion.

For current durable world families, generic RD-06/RD-07 contracts may be referenced as shared lifecycle mechanisms, but the matrix must show the family actually satisfies their input identity/route/schema preconditions. Do not duplicate durability/recovery semantic ownership inside RD-16.

### Task 7 — final coherent verification

```bash
python3 -m unittest DEV.TESTS.test_rd16_world_family_machine_integration -v
python3 -m unittest DEV.TESTS.test_r2_7_wp03_catalog_conformance -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Every committed checkpoint must be GREEN for all tests materialized at that checkpoint. No future intentional RED group is committed ahead of its repair.

## 9. Execution ordering / shared-writer law

RD-16 is not a whole-project serialization barrier. Owner-local work that does not edit the final shared machine files may proceed independently.

The required ordering is:

```text
owner-local semantic/schema work
    -> LOCAL_SEMANTIC_READY
    -> RD-16 SHARED_MACHINE_INTEGRATION_JOIN
    -> final catalog/schema/conformance GREEN
    -> package R018 / affected RD integration completion
```

No owner-local worker may independently publish the final versions of `identifier-policies.json`, `core-catalog.json`, `entity-structures.json` or the world-kind admission ledger after RD-16 starts its integration checkpoint. Newly discovered conflicting shared-file need returns to RD-16 integration planning/currentness rather than creating another writer.

## 10. Version / migration disposition

Planning publication Version Impact: **NONE**.

Future implementation is an unreleased v1 clean-slate machine realization. Legacy v0.8 is not a preservation constraint. Do not introduce a compatibility world-faction family, permissive fallback dispatch, dual identifier policy, or migration shim solely to preserve provisional pre-v1 machine shape.

At implementation time run the normal Version Impact Gate for actual schema/catalog/GAME contract changes. If stronger field representation is required by a then-current semantic owner, classify that delta normally rather than hiding it inside RD-16.

## 11. Coverage consequence

Do not invent new historical WP-27 readiness IDs. Track these as post-WP27 graph-closure findings:

```text
AUTHOR_GRAPH_FINDING_12
  problem: incomplete strict world-family state realization / permissive envelope
  decomposition owner: RD-16
  readiness contribution: R018 per-family machine closure

AUTHOR_GRAPH_FINDING_13
  problem: multiple independent writers of shared catalog/identity machine files
  decomposition owner: RD-16 shared integration checkpoint
  readiness contribution: R018 + affected identity/proof joins
```

Original active-readiness accounting remains 133; decomposition RD count becomes 16 after RD-15 + RD-16.

## 12. Disposition

```text
AUTHOR_GRAPH_FINDING_12: REPAIRED_IN_PLANNING_BY_RD16
AUTHOR_GRAPH_FINDING_13: REPAIRED_IN_PLANNING_BY_RD16
NEW_RD_REQUIRED: YES — RD-16
FINAL_WORLD_FAMILY_COUNT: 17
FINAL_RUNTIME_FAMILY_COUNT: 17
SEMANTIC_OWNER_TRANSFER: NONE
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
