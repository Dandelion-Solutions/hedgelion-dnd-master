# HDM Implementation Planning — Information World-Schema / RD-16 Integration Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / INDEPENDENTLY UNCONFIRMED**
Date: 2026-09-14
Finding: **AUTHOR FINDING 42 — SIGNIFICANT**
Production implementation: **NO**.

This amendment repairs a shared-schema/semantic-owner collision between RD-02 and RD-16. It changes no accepted information semantics, family census, catalog generation, persistence authority or runtime ownership.

## 1. Finding

RD-02 Task 2 explicitly creates the owner-native strict contracts:

```text
DEV/SCHEMAS/world-lore-fact-state.schema.json
DEV/SCHEMAS/world-knowledge-state.schema.json
```

and owns their information semantics under the accepted truth/knowledge/disclosure architecture.

The later RD-16 machine-integration plan independently lists the same two paths in its "Create strict world-state schemas" set and Task 2 treats them as part of the ten "quiet-family" schemas it constructs locally.

That is not merely a physical shared-file overlap. Two independent workers are authorized to construct the same semantic world-family schemas from different plan contexts. RD-16 is intended to integrate final owner contracts into the strict 17-family wrapper/catalog machine generation; it is not the semantic owner of LoreFact or Knowledge.

Without repair, legal execution could yield:

- RD-02 creates owner-correct information schemas and RD-16 later replaces them from a reduced top-level family matrix;
- RD-16 creates them first and RD-02 later changes them without re-running the final 17-family wrapper/catalog integration;
- both test suites pass locally while the final strict wrapper reflects only one generation of the shared schema bytes;
- R018 closes from an RD-16 matrix that is not the exact RD-02 owner contract.

## 2. Authority correction

RD-02 remains the sole semantic producer/creator of:

```text
world.lore_fact -> DEV/SCHEMAS/world-lore-fact-state.schema.json
world.knowledge -> DEV/SCHEMAS/world-knowledge-state.schema.json
```

RD-16 MUST consume, validate and integrate those exact current GREEN schemas. RD-16 MUST NOT independently create, replace, weaken or reconstruct their owner fields/inner semantics.

RD-16 remains responsible for:

- final exact 17-kind world wrapper dispatch;
- final catalog/structure/identifier shared-machine checkpoint;
- verifying every world family has one strict schema and owner-consistent catalog row;
- fail-closed cross-family machine conformance.

This mirrors the already-correct RD-08 `world.thread` pattern: owner RD produces the schema, RD-16 consumes it in final integration.

## 3. RD-16 file/action correction

In RD-16's "Create strict world-state schemas" set, remove these two create actions:

```text
DEV/SCHEMAS/world-lore-fact-state.schema.json
DEV/SCHEMAS/world-knowledge-state.schema.json
```

The RD-16 quiet-family local-create set is therefore eight families:

```text
world.connection
world.zone
world.organization
world.contract
world.mission
world.scene
world.encounter
world.hazard
```

`world.player` remains the separately integrated RD-16/F35 contract. `world.thread` remains RD-08-owned. Actor/ActorGroup/Asset/Location/Effect remain consumed existing owner contracts. LoreFact/Knowledge become RD-02-owned consumed contracts.

The final 17-family matrix still contains all 17 families; only physical/semantic producer ownership is corrected.

## 4. Required checkpoint edge

RD-02 exposes:

```text
RD02_INFORMATION_WORLD_SCHEMA_LOCAL_SEMANTIC_READY
```

only when:

- both LoreFact and Knowledge schemas are GREEN under `NativeInformationSchemaTests`;
- their required/properties/closed-vocabulary semantics reflect the accepted information owner;
- no embedded legacy knowledge/Secret authority is used as a substitute for the native contracts.

Final RD-16 integration adds:

```text
RD02_INFORMATION_WORLD_SCHEMA_LOCAL_SEMANTIC_READY
+ RD08_THREAD_LOCAL_SEMANTIC_READY
+ RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY
+ other existing RD16 shared-machine inputs
  JOIN_BEFORE_INTEGRATION
RD16_SHARDED_WORLD_SCHEMA_INTEGRATION_READY
```

`RD16_SHARDED_WORLD_SCHEMA_INTEGRATION_READY` is the schema/dispatch portion of the existing `RD16 SHARED_MACHINE_INTEGRATION_JOIN`; it is not a new semantic owner or whole-RD barrier.

RD-02 owner-local runtime/normalization work unrelated to final world-wrapper integration may proceed independently.

## 5. Strict-wrapper integration law

RD-16 final world-record dispatch must validate LoreFact and Knowledge through the exact current RD-02 schema refs/bytes.

The final integration proof must establish:

1. `world.lore_fact` selects exactly `world-lore-fact-state.schema.json` produced by RD-02;
2. `world.knowledge` selects exactly `world-knowledge-state.schema.json` produced by RD-02;
3. final `entity-structures.json` rows do not omit any RD-02 owner-required top-level field;
4. RD-16 does not introduce a weaker duplicate schema, copied field list or generic details bypass;
5. an RD-02 schema change after the final integration invalidates the integration checkpoint until re-run;
6. `world.faction` remains absent and no unrelated family ownership changes.

The `R018WorldFamilyProofTests` family rows for LoreFact/Knowledge must point to RD-02 as semantic/schema producer and RD-16 as final machine integrator.

## 6. Version / catalog-generation disposition

This repair does **not** itself require a catalog-generation change.

The canonical versioning law keeps local schema versions and coordinated catalog generation independent. Future implementation applies the normal Version Impact Gate to the actual RD-02 schema shapes and RD-16 catalog integration. This amendment does not authorize preserving an incompatible released generation, nor does it manufacture a generation bump merely to fix plan ownership.

Clean-slate v1 policy remains unchanged; no pre-v1 migration/shim is introduced.

## 7. Proof obligations

F42 closes only with integrated evidence that:

- RD-02 focused information schema tests are GREEN;
- RD-16 strict world-wrapper tests load those exact owner contracts;
- final 17-row R018 world-family matrix attributes semantic/schema production correctly;
- static audit finds no second planned/generated LoreFact or Knowledge strict schema implementation;
- final shared catalog/structure conformance remains GREEN after the owner schemas join.

Count-only "17 families" proof is insufficient.

## 8. Finding disposition

```text
AUTHOR_FINDING_42: SIGNIFICANT
ROOT_CAUSE: RD-16 independently constructed two strict world schemas already owned/created by RD-02 instead of consuming owner-final contracts
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO
REPAIR_STATE: PLANNED IN THIS MANDATORY AMENDMENT
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
