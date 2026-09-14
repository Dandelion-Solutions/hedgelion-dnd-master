# HDM Implementation Planning — WP-15 world.thread Catalog Cutover Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR OVERLAY — EXECUTION NOT AUTHORIZED**
Date: 2026-09-14
Production implementation authorized: **NO**.

This overlay repairs a post-SIRR2 author finding in RD-08. Canonical WP-15 explicitly says the current catalog generation lacks coordinated `world.thread` kind/structure/identifier/admission/conformance realization. The current RD-08 v2 plan incorrectly left the catalog edit conditional (`only if required`). Current machine bytes confirm the debt is real.

This overlay adds an executable catalog-alignment checkpoint to RD-08. It does not change the WP-15 semantic owner or create another process family.

## 1. Exact current debt

At the current planning baseline, `world.thread` is absent from:

- `DEV/CATALOG/core-catalog.json` world-record registry;
- `DEV/CATALOG/entity-structures.json` world-record structure map;
- `DEV/CATALOG/identifier-policies.json` world identity policies;
- `DEV/CATALOG/catalog-admission-ledger/families/world_record_kinds.json` admission trace/census;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` current world-record classification table;
- `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` current world-record structure table.

`GAME/SCHEMA/thread.schema.yaml` exists but is legacy/stale and is already a mandatory RD-08 replacement surface. `GAME/CAMPAIGN/INDEX/THREAD_INDEX.yaml` already exists and remains a rebuildable discovery projection, not authority.

## 2. RD-08 checkpoint ordering

The catalog checkpoint is joined to RD-08 world-thread contract realization:

```text
WP-15 world.thread semantic laws
-> RD-08 final world.thread machine schema/state contract
-> coordinated catalog classification / structure / identity / admission projections
-> catalog conformance + RD-08 focused tests
-> green coherent checkpoint
```

The catalog task may not independently redesign thread state. `entity-structures.json` and `ENTITY_STRUCTURES.md` must project the required/expected/binding semantics of the final RD-08 thread contract from the same checkpoint.

## 3. Exact writable surfaces

Mandatory MODIFY surfaces:

```text
DEV/CATALOG/core-catalog.json
DEV/CATALOG/entity-structures.json
DEV/CATALOG/identifier-policies.json
DEV/CATALOG/catalog-admission-ledger/families/world_record_kinds.json
DEV/ARCHITECTURE/CATALOG_INVENTORY.md
DEV/ARCHITECTURE/ENTITY_STRUCTURES.md
DEV/TESTS/test_rd08_temporal.py
DEV/TESTS/test_r2_7_wp03_catalog_conformance.py
```

`DEV/TESTS/test_s6d_02_catalog_admission_contract.py` is a required existing verification consumer. Modify it only if a current hard-coded assertion must be extended; its bidirectional ledger/core-catalog checks must remain green.

Protect/verify, do not rewrite merely for presence:

```text
GAME/CAMPAIGN/INDEX/THREAD_INDEX.yaml
DEV/CATALOG/catalog-admission-ledger/manifest.json
```

The manifest already declares the `world_record_kinds` shard and needs no edit solely because the shard census changes.

## 4. RED — WorldThreadCatalogAlignmentTests

Create the class only when this checkpoint begins, under the package-wide checkpoint-coherence overlay.

Required RED cases before the cutover:

- `world.thread` missing from `core-catalog.json` world-record kinds;
- missing from `entity-structures.json`;
- missing from identifier policies;
- admission shard lacks the exact active entry and still reports count/admitted 15;
- active catalog inventory and entity-structure tables omit the kind;
- catalog machine surfaces are therefore not bidirectionally coherent with the accepted WP-15 owner;
- existing `THREAD_INDEX.yaml` presence alone does not establish catalog admission or semantic ownership.

Focused RED command:

```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.WorldThreadCatalogAlignmentTests -v
```

Do not publish the RED state.

## 5. GREEN — coordinated catalog generation-2 realization

Perform one coordinated logical cutover:

1. Add `world.thread` exactly once to `core-catalog.json` `world_record_kinds`.
2. Add one `world.thread` entry to `entity-structures.json`; its required/expected state fields and forbidden/allowed definition binding must match the final RD-08 thread contract. No copied mission/contract/effect/procedure state and no knowledge/disclosure fields are admitted.
3. Add exact identifier policy:

```json
{"strategy":"sequential","prefix":"thread","minimum_width":4,"scope":"campaign"}
```

This is campaign allocation identity only. Numeric/lexical ID order is not chronology, priority or currentness. No session-local thread identity is introduced because WP-15 admits `world.thread` only for independently persistent generic processes.
4. Add one `ACTIVE_ADMITTED` `world.thread` entry to the `world_record_kinds` admission shard, update its census from 15 to 16 and admitted from 15 to 16, and cite WP-15 + catalog class contract as the accepted owner basis. Do not create a second ID owner in the ledger.
5. Add `world.thread` to `CATALOG_INVENTORY.md` as the narrow independently persistent generic-process owner, with explicit non-mega-owner wording.
6. Add the matching row to `ENTITY_STRUCTURES.md`, projecting the same final RD-08 thread state/binding contract as the machine structure.
7. Extend catalog conformance tests so `world.thread` presence is positively required across registry, structure, identity policy and active admission trace; also assert it is absent from runtime-record kinds and that no alternate generic process kind is created.
8. Preserve existing `THREAD_INDEX.yaml` only as rebuildable discovery support; its presence cannot substitute for the six coordinated catalog/prose surfaces above.

## 6. Verification

Focused and existing conformance witnesses:

```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.WorldThreadCatalogAlignmentTests -v
python3 -m unittest DEV.TESTS.test_r2_7_wp03_catalog_conformance -v
python3 -m unittest DEV.TESTS.test_s6d_02_catalog_admission_contract -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Expected: all PASS before publication.

The checkpoint is not green if any one catalog surface still omits `world.thread`, the admission ledger/core catalog cease to be bidirectionally equal, or a prose owner still presents the old 15-kind world catalog as current.

## 7. Version / migration disposition

This is realization of already-accepted `world.thread` inside the current unreleased clean-slate catalog generation `2`, not an incompatible released-catalog transition.

```text
catalog_generation: stays 2
catalog artifact schema_version: unchanged unless the artifact serialization format itself changes
campaign_contract_generation: no bump solely for this catalog admission repair
migration: none solely to preserve the superseded pre-v1 absence
```

The execution-time Version Impact Gate must still verify that no additional incompatible shape change has appeared since planning currentness.

## 8. Proof / completion join

WP-15 implementation-facing obligation 1 is not complete from thread schema or index presence alone. RD-08 completion/proof must join:

```text
final world.thread schema/state contract
+ core catalog admission
+ machine structure projection
+ identifier policy
+ admission-ledger equality
+ active catalog inventory/structure prose alignment
+ catalog conformance tests
```

This repair changes no readiness identity, semantic owner, RD count or production authorization.

```text
VERSION_IMPACT_OF_THIS_PLANNING_EDIT: NONE
SEMANTIC_OWNER_CHANGE: NONE
READINESS_ID_CHANGE: NONE
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
