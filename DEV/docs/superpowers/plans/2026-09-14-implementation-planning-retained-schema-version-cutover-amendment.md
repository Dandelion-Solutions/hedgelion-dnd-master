# HDM Implementation Planning — Retained Schema Version Cutover Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / INDEPENDENTLY UNCONFIRMED**
Date: 2026-09-14
Finding: **AUTHOR FINDING 43 — SIGNIFICANT**
Production implementation: **NO**.

This amendment closes a deterministic local-version cutover defect in the RD-01..RD-16 implementation package. It changes no accepted gameplay semantics, persistence authority, family census, catalog generation or storage generation.

Product-owner constraint for this repair: HDM v1.0 `GAME/**` is clean-slate/pre-release. Breaking retained contracts may and should receive new local schema versions immediately. Do not preserve obsolete pre-release shapes by migration, dual-read, aliases or compatibility shims.

## 1. Finding

The shipped schema owner states:

```text
Artifact-local schema_version belongs to the concrete persistent/protocol contract.
Compatible optional additions may retain the local version.
Breaking required-shape or semantic changes require a new local schema version.
```

The current executable plans already prescribe incompatible replacements or meaning changes for several retained `GAME/SCHEMA/*.schema.yaml` contracts, but they leave the Version Impact result to an implementation-time classifier. For these files the result is no longer uncertain.

A legal worker could therefore implement the accepted new shape while retaining the old `schema_version`, or two shared-file writers could bump the same contract independently. Either result creates mixed-generation ambiguity and pushes avoidable compatibility debt into v1.

This is a planning defect. No architecture reopen is required.

## 2. Exact deterministic cutover matrix

At the current package baseline, the following retained contracts have one mandatory local version transition:

| Retained schema | Current version | Final v1 target | Breaking basis | Final bump writer/checkpoint |
|---|---:|---:|---|---|
| `GAME/SCHEMA/checkpoint.schema.yaml` | 3 | **4** | RD-07 retires `valid_through_event_id` recovery-frontier meaning and `expected_commit_sha` currentness/self-reference semantics; checkpoint becomes descriptor/evidence only | RD-07 Task 5 checkpoint-descriptor coherent checkpoint |
| `GAME/SCHEMA/current_state.schema.yaml` | 2 | **3** | RD-08 replaces CURRENT and removes `world_time.frontier` / equivalent global chronology scalar | RD-08 Checkpoint 1 |
| `GAME/SCHEMA/thread.schema.yaml` | 1 | **2** | RD-08 replaces legacy thread shape, removes process-owned epistemic visibility and binds temporal conditions to owner-local typed semantics | RD-08 Checkpoint 2 |
| `GAME/SCHEMA/live_scene.schema.yaml` | 1 | **2** | RD-09 plus mandatory LIVE overlays replace arbitrary overlay/epistemic/path authority with typed claims, exact source-native state, cursor/route/opening/currentness and lossless absorption semantics | final RD-09 LIVE schema checkpoint after F24-F31/F36 composition |
| `GAME/SCHEMA/index.schema.yaml` | 1 | **2** | RD-04 replaces generic entity index with rebuildable owner-family discovery/routing contract and owner-approved compact fields | RD-04 Task 5 |
| `GAME/SCHEMA/scene.schema.yaml` | 2 | **3** | RD-08 removes singleton chronology-frontier authority; scene-routing/LIVE overlays also change `live_epoch` route/currentness meaning | final scene schema integration checkpoint after RD-08 chronology delta + RD-09/LIVE routing delta |
| `GAME/SCHEMA/location.schema.yaml` | 1 | **2** | RD-04 removes reverse mobile-presence authority and RD-02 removes embedded knowledge/Secret authority | final coordinated RD-04 -> RD-02 location checkpoint, bumped exactly once after both semantic deltas survive |
| `GAME/SCHEMA/event.schema.yaml` | 1 | **2** | RD-13 replaces legacy `world_order`/embedded delta visibility/knowledge representation with native SemanticEvent/history causal/evidence owner contract | RD-13 Task 2 native-history checkpoint |
| `GAME/SCHEMA/lore.schema.yaml` | 1 | **2** | RD-02 replaces combined canonical/superseded/disputed projection with the pure `world.lore_fact` owner projection and removes alternate knowledge/dispute authority | RD-02 Task 4 legacy-information cutover checkpoint |
| `GAME/SCHEMA/player.schema.yaml` | 1 | **2** | F35 final PLAYER contract makes completeness-protected `collaboration_route_refs` durable state where missing is integrity/repair evidence while an explicit empty collection is valid; final strict PLAYER/shipped projections must agree | RD-16 final PLAYER strict-state integration checkpoint consuming RD-12 local semantic delta |

These exact targets are part of the current implementation package. A worker must not leave them as `Version Impact: classify` decisions.

## 3. One semantic cutover = one bump

The table names the **final bump writer/checkpoint**. Shared physical writers may prepare owner-local deltas, but they must not independently increment the same retained schema.

Specific shared-file laws:

```text
location.schema.yaml
  RD-04 presence delta
  -> RD-02 information delta
  -> one final v2 file

scene.schema.yaml
  RD-08 chronology delta
  -> RD-09/LIVE routing/currentness integration
  -> one final v3 file

player.schema.yaml
  RD-12 collaboration companion semantic delta
  -> RD-16 final strict PLAYER integration
  -> one final v2 shipped schema

live_scene.schema.yaml
  RD-09 base replacement
  + F24-F31/F36 later-precedence LIVE realization
  -> one final v2 file
```

Do not bump once per RD or once per amendment. Version identity follows the final incompatible retained contract generation.

If implementation currentness reveals that an earlier authorized checkpoint has already published the exact same target generation, later writers preserve that version and validate the bytes; they do not increment it again merely because they are later in the graph.

## 4. Explicit exclusions

### `GAME/SCHEMA/session.schema.yaml`

Remain at current local version **1** for this package unless an actual wire/required-field break is discovered later.

RD-06/RD-07 planned edits make base/published HEAD observations and session status explicitly non-authoritative. The current schema already defines session as coordination/recovery metadata and does not grant current-state/publication authority. The planned change is a clarification/negative invariant, not a currently established breaking shape cutover.

### `GAME/SCHEMA/pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml`

No terminal version bump. RD-03 retires these legacy native projections during Actor/Asset cutover. Do not manufacture a final legacy generation immediately before deletion/retirement.

### `GAME/SCHEMA/faction.schema.yaml`

No terminal version bump. F8 classifies independent `world.faction` as a stale false family; v1 uses `world.organization` plus faction classification/facet semantics. The legacy faction schema is not a retained v1 owner contract.

### New schemas

New v1 schemas created by the package start at the owner-approved initial local version. They are not part of this retained-contract bump matrix.

## 5. Clean-slate migration/compatibility law

For every row in the matrix:

- update the retained schema and its local `schema_version` in the **same coherent GREEN checkpoint**;
- update any shipped blank/template/example/generated instance of that exact retained contract to the target version in the same owning cutover or required scaffold integration;
- update exact validators/tests/readers/writers to consume only the final v1 contract;
- do **not** create a v1 compatibility reader for the superseded pre-release local version solely to preserve current repository fixtures;
- do **not** add migration jobs/edges for unreleased v0.8/pre-v1 data;
- do **not** keep old fields as deprecated aliases merely to avoid updating consumers;
- stale old-version fixture/template bytes in the final generated v1 scaffold are a failure, not migration evidence.

If a future released persisted-data obligation appears, that future owner decision may add a migration edge. F43 does not pre-build one.

## 6. Generated/template consumer closure

A schema bump is incomplete if only `GAME/SCHEMA/*.schema.yaml` changes while shipped/generated campaign bytes still advertise the prior generation.

Each owning checkpoint must enumerate and update every current bounded static/template consumer for its contract. At minimum the package must check:

- checkpoint scaffold/template uses checkpoint v4;
- blank/generated CURRENT uses current-state v3;
- blank/generated scene state, where materialized, uses scene v3;
- blank/generated PLAYER records, when created, use player v2;
- any generated family index document uses index v2;
- LIVE source creation emits live-scene v2;
- new native history/lore/location/thread records are emitted only at their target versions.

Absence of a blank instance is valid when the owner intentionally creates records lazily; do not add compatibility/example files solely to demonstrate the version.

## 7. Proof obligations

Add a package-level focused witness conceptually named:

```text
RetainedSchemaVersionCutoverTests
```

It must prove from exact current final bytes:

1. all ten retained schemas carry the target versions in the matrix;
2. each target schema contains the accepted final owner shape, not merely a bumped integer;
3. shared schemas are bumped exactly once at their final integration checkpoint;
4. final shipped/generated/template consumers carry the same generation where an instance exists;
5. no active v1 reader/writer requires a superseded pre-release shape;
6. no migration/dual-read/legacy-alias code was introduced solely for these cutovers;
7. `session.schema.yaml` remains v1 unless a separately proven breaking change exists;
8. retired PC/NPC/item/faction schemas are not kept alive by compatibility/version work.

The relevant RD focused tests remain primary semantic witnesses. The package-level test is the mixed-generation/identity witness and cannot substitute for owner tests.

Run before final package closure:

```bash
python3 -m unittest DEV.TESTS.test_implementation_package_version_cutovers.RetainedSchemaVersionCutoverTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Exact test module spelling may follow the existing package-test naming convention, but one explicit package-level witness for this matrix is mandatory.

## 8. Namespace separation

F43 does **not** infer any of the following merely from local schema bumps:

```text
catalog_generation bump
campaign_contract_generation bump
storage_format_generation bump
engine_version bump
install_layout_revision bump
```

Those namespaces remain independently governed. The ongoing audit checks catalog/module generation separately.

Therefore F43 neither preserves `catalog_generation=2` by fiat nor bumps it mechanically. It only closes the already-deterministic local retained-schema version law.

## 9. Execution/proof graph consequence

F43 adds no whole-RD semantic ordering. It adds owner-local version obligations to existing coherent checkpoints plus one package proof sink:

```text
checkpoint v4 local GREEN -------------------------\
current_state v3 local GREEN -----------------------+
thread v2 local GREEN ------------------------------+
live_scene v2 final LIVE GREEN ---------------------+
index v2 local GREEN -------------------------------+
scene v3 final shared GREEN ------------------------+-> RETAINED_SCHEMA_VERSION_CUTOVER_PROOF_READY
location v2 final shared GREEN ---------------------+
event v2 local GREEN -------------------------------+
lore v2 local GREEN --------------------------------+
player v2 final RD12->RD16 integration GREEN -------/

RETAINED_SCHEMA_VERSION_CUTOVER_PROOF_READY
  PROOF_AFTER_TARGET
package author closure / independent Senior handoff
```

This proof sink does not block unrelated owner-local implementation work and creates no semantic cycle.

## 10. Finding disposition

```text
AUTHOR_FINDING_43: SIGNIFICANT
ROOT_CAUSE: deterministic incompatible retained-schema cutovers were left as worker-time Version Impact choices and shared writers had no single-bump law
RETained_BREAKING_SCHEMA_COUNT: 10
MIGRATION_FOR_PRE_RELEASE_SHAPES: FORBIDDEN
DUAL_READ_OR_COMPAT_SHIM: FORBIDDEN
CATALOG_GENERATION_DECISION: SEPARATE AUDIT
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO — clean-slate version-bump direction confirmed
REPAIR_STATE: PLANNED IN THIS MANDATORY AMENDMENT
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
