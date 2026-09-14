# HDM Implementation Planning — Schema / Storage README Shared-Writer Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / INDEPENDENTLY UNCONFIRMED**
Date: 2026-09-14
Finding: **AUTHOR FINDING 41 — SIGNIFICANT**
Production implementation: **NO**.

This amendment repairs a physical shared-writer defect in the executable implementation package. It creates no semantic owner, readiness identity, schema family, storage authority, runtime dependency or whole-RD serialization edge.

## 1. Finding

The current executable plans independently schedule writes to shared shipped documentation projections without a named shared-file checkpoint:

- RD-02 Task 4 modifies `GAME/SCHEMA/README.md` and `GAME/TEMPLATE/STORAGE_README.md` for the information/knowledge/disclosure/message owner-native cutover and retirement of embedded epistemic authority.
- RD-03 Task 5 modifies both files for the Actor/Asset/Effect shipped-schema cutover and retirement of PC/NPC/item native projections.
- RD-04 Task 5 modifies both files for owner-native routing, rebuildable family-index and storage projection semantics.
- RD-07 Task 5 modifies `GAME/SCHEMA/README.md` for the repaired checkpoint descriptor/recovery contract and removal of frontier-like checkpoint authority.

Each owner-local delta is independently valid, but the files are single physical projections. The current execution graph contains explicit shared-file coordination for `location.schema.yaml`, legacy PC/NPC/item schemas, shared catalog machinery, install/bootstrap projections and several shipped CORE files, but it does not name these README overlaps.

A legal worker order could therefore publish one GREEN RD checkpoint and later replace or partially rewrite the same README projection while accidentally erasing another already accepted delta. A generic instruction to fresh-read files is insufficient once the overlap is already known and each plan lists the file as a planned modification.

## 2. Authority boundary

Semantic ownership remains unchanged:

- RD-02 owns information/knowledge/disclosure/message semantics and its legacy-epistemic retirement.
- RD-03 owns Actor/Asset/Effect shipped cutover semantics.
- RD-04 owns native routing/index/HOT/storage projection semantics.
- RD-07 owns checkpoint/recovery projection semantics.

`GAME/SCHEMA/README.md` and `GAME/TEMPLATE/STORAGE_README.md` are documentation/projection surfaces only. They gain no schema, storage, currentness, recovery or semantic authority from this repair.

## 3. Required owner-local readiness checkpoints

Each implicated task may perform its semantic/schema/runtime work independently. Before a shared README integration claims final projection readiness, expose bounded owner-local projection readiness:

```text
RD02_SCHEMA_STORAGE_DOC_DELTA_READY
  = RD-02 Task-4 owner-native information cutover semantics/tests are GREEN
    and its required README/storage projection delta is known.

RD03_SCHEMA_STORAGE_DOC_DELTA_READY
  = RD-03 Task-5 Actor/Asset/Effect shipped cutover semantics/tests are GREEN
    and its required README/storage projection delta is known.

RD04_SCHEMA_STORAGE_DOC_DELTA_READY
  = RD-04 Task-5 routing/index/storage semantics/tests are GREEN
    and its required README/storage projection delta is known.

RD07_SCHEMA_DOC_DELTA_READY
  = RD-07 Task-5 checkpoint descriptor/recovery semantics/tests are GREEN
    and its required schema-README projection delta is known.
```

These are checkpoint-level integration inputs only. They do not require whole RD-02/03/04/07 completion.

## 4. Final physical integration checkpoints

### 4.1 `GAME/SCHEMA/README.md`

The final shared projection checkpoint is:

```text
RD02_SCHEMA_STORAGE_DOC_DELTA_READY
+ RD03_SCHEMA_STORAGE_DOC_DELTA_READY
+ RD04_SCHEMA_STORAGE_DOC_DELTA_READY
+ RD07_SCHEMA_DOC_DELTA_READY
  SHARED_FILE_CHECKPOINT / JOIN_BEFORE_INTEGRATION
GAME_SCHEMA_README_FINAL_INTEGRATION_READY
```

One designated physical integration write must:

1. fresh-read the then-current `GAME/SCHEMA/README.md`;
2. preserve every already-admitted unrelated current projection;
3. apply all four owner deltas in one coherent final document;
4. preserve owner boundaries rather than merging information, Actor, routing/index or checkpoint semantics into one generic state/storage owner;
5. remove stale wording only where an implicated owner/test proves it contradicted;
6. run all four relevant focused projection assertions plus maintenance audit before the checkpoint is publishable.

No later owner may independently replace the integrated README with an owner-local snapshot. A later legitimate change must fresh-read and preserve all current admitted sections.

### 4.2 `GAME/TEMPLATE/STORAGE_README.md`

The final storage-template documentation checkpoint is:

```text
RD02_SCHEMA_STORAGE_DOC_DELTA_READY
+ RD03_SCHEMA_STORAGE_DOC_DELTA_READY
+ RD04_SCHEMA_STORAGE_DOC_DELTA_READY
  SHARED_FILE_CHECKPOINT / JOIN_BEFORE_INTEGRATION
GAME_STORAGE_README_FINAL_INTEGRATION_READY
```

The final projection must simultaneously preserve:

- information-owner routing/storage separation and absence of embedded writable epistemic authority;
- Actor/Asset/Effect native-family cutover and absence of PC/NPC/item native compatibility fiction;
- owner-native direct routing, rebuildable non-authoritative indexes and storage/HOT negative laws from RD-04.

RD-07 has no currently planned write to `GAME/TEMPLATE/STORAGE_README.md` and therefore is not an input to this checkpoint.

## 5. Execution graph effect

Add only these bounded edges:

```text
RD02_SCHEMA_STORAGE_DOC_DELTA_READY ----\
RD03_SCHEMA_STORAGE_DOC_DELTA_READY -----+-> GAME_SCHEMA_README_FINAL_INTEGRATION_READY
RD04_SCHEMA_STORAGE_DOC_DELTA_READY -----+
RD07_SCHEMA_DOC_DELTA_READY -------------/

RD02_SCHEMA_STORAGE_DOC_DELTA_READY ----\
RD03_SCHEMA_STORAGE_DOC_DELTA_READY -----+-> GAME_STORAGE_README_FINAL_INTEGRATION_READY
RD04_SCHEMA_STORAGE_DOC_DELTA_READY -----/
```

No semantic `HARD_PRECEDES` edge is introduced among RD-02, RD-03, RD-04 and RD-07. Existing owner-specific shared schema orders remain unchanged, including RD-04 -> RD-02 for `location.schema.yaml` and the RD-02/RD-03 legacy PC/NPC/item cutover rule.

The checkpoint graph remains acyclic because these documentation joins are sinks for the implicated owner-local projection deltas and do not feed any earlier semantic checkpoint.

## 6. Proof obligations

The package must add a direct cross-owner projection witness proving at minimum:

1. final `GAME/SCHEMA/README.md` contains no stale embedded epistemic-authority route;
2. final schema README projects Actor/Asset/Effect rather than PC/NPC/item as independent native families;
3. final schema README describes indexes/routes as non-authoritative and preserves known-ID direct routing semantics;
4. final schema README does not present checkpoint/event/frontier metadata as currentness or recovery authority;
5. final `GAME/TEMPLATE/STORAGE_README.md` simultaneously preserves RD-02/RD-03/RD-04 storage/routing laws;
6. executing any one later owner-local documentation delta against the integrated form cannot legally drop another owner section; final proof runs on the integrated bytes, not on isolated fixture text.

Existing focused RD tests remain supporting evidence. Independent single-RD GREEN results do not close F41 without final integrated-file proof.

## 7. Version / migration disposition

This amendment is planning-only and has **Version Impact: NONE**.

Future implementation must run the existing Version Impact Gate for the actual schema/API/storage changes owned by RD-02/03/04/07. The README integration itself does not manufacture a schema/catalog generation bump merely because several projections share one file. Migration remains governed by the underlying owner changes and clean-slate v1 policy.

## 8. Finding disposition

```text
AUTHOR_FINDING_41: SIGNIFICANT
ROOT_CAUSE: known multi-RD physical writers to shared schema/storage README projections lacked a named final integration checkpoint
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO
REPAIR_STATE: PLANNED IN THIS MANDATORY AMENDMENT
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
