# HDM v1 Implementation Plan — Execution Contract

Status: **CURRENT PACKAGE-WIDE EXECUTION CONTRACT / SENIOR GO REQUIRED**

This contract applies to every task in Waves 01–06. It consolidates the former package conventions, impact/TDD contract and checkpoint-coherence amendments. A wave may strengthen it for a concrete owner, but cannot weaken it.

## 1. Worker bootstrap and authority

Before work on any task:

1. fresh-read the current remote ref through the applicable runtime transport;
2. read `AGENTS.md`, the runtime overlay, `DEV/CURRENT_PROGRESS.md`, `DEV/PROJECT_MAP.md`, this contract, the wave task and every canonical owner named by that task;
3. confirm that independent Senior GO for this consolidated package is recorded at the current exact HEAD;
4. fresh-read every existing path in the task's write set and its current version owner;
5. stop only for an actual System-Impact Gate, unresolved owner conflict, missing authorization or currentness discontinuity.

Chat history, retired plans and the non-normative traceability file are never implementation authority.

## 2. File-action vocabulary

Every touched path is classified before mutation:

| Action | Meaning |
|---|---|
| `EXISTING_MODIFY` | retain the current owner/surface and edit it in place |
| `EXISTING_REPLACE` | keep the path but replace a materially obsolete pre-v1 contract |
| `EXISTING_RETIRE` | remove an obsolete current-tree artifact after its surviving obligations and references are routed elsewhere |
| `NEW_CREATE` | add a deliberate owner-native artifact that is absent at the fresh HEAD |
| `MOVE_RENAME` | relocate an accepted v1 artifact and update all consumers in the same envelope |
| `INSPECT_ONLY` | verify currentness/compatibility without a planned write |

Any new path is rechecked against the current tree before creation. An absent historical path is not recreated to satisfy stale text. Touched `GAME/**` is classified `V1_COMPATIBLE`, `MIXED` or `LEGACY_SUPERSEDED`; obsolete v0.8 shape is not a compatibility constraint.

## 3. Dependency vocabulary

- `HARD_PRECEDES`: the consumer cannot be correct before the predecessor output exists.
- `JOIN_BEFORE_INTEGRATION`: owner-local work may proceed independently, but the named integrated checkpoint waits for every input.
- `SHARED_FILE_CHECKPOINT`: semantic deltas remain owner-local; one final writer fresh-reads and integrates the physical file.
- `PROOF_AFTER_TARGET`: the proof task runs only after the implicated mechanisms exist.
- `CONSTRAINS_WITHOUT_ORDERING`: accepted law constrains a task without adding serialization.

Wave and task numbers are not dependency evidence. Only named inputs/checkpoints order work.

## 4. Implementation Impact Envelope

Before the first RED step in each task, record this envelope in task execution evidence:

```text
SPEC / APPROVED DESIGN:
IMPLEMENTATION START HEAD:
PRIMARY OWNER ARTIFACTS:

EXPECTED OWNERS TO CHANGE:
EXPECTED CONSUMERS TO CHANGE:
ALLOWED INTERFACES / CONTRACTS TO CHANGE:

GAME RUNTIME / PROJECTION SURFACES:
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS:
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS:
VALIDATORS / TESTS / AUDITS:
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS:
CROSS-WAVE JOINS:

PROTECTED ARCHITECTURE INVARIANTS:
ARCHITECTURE-SENSITIVE SURFACES:
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION:
KNOWN OUT-OF-SCOPE OWNERS / SURFACES:

VERSION IMPACT:
SCHEMA / CATALOG / CHECKPOINT IMPACT:
MIGRATION IMPACT:
HG-01 CONSTRAINTS AFFECTED:
CURRENTNESS RE-READ SET BEFORE WRITE:
```

The wave task supplies the minimum envelope. Execution adds newly discovered current consumers only when they remain within accepted ownership and semantics. A materially broader owner set, new authority or unplanned persistent/interface policy triggers the System-Impact Gate.

## 5. Mandatory task loop

Each task is one coherent independently reviewable deliverable:

```text
fresh currentness read
-> RED: add the smallest positive and material-negative witness
-> run focused witness and verify expected failure reason
-> GREEN: implement the smallest owner-correct behavior
-> run focused witness GREEN
-> REFACTOR without semantic/authority change
-> run the complete task-local module suite
-> run named cross-owner/integration checks
-> compare actual impact with the Impact Envelope
-> run Version Impact Gate and synchronize projections
-> review code/spec conformance and repair local findings
-> maintenance audit + applicable broader DEV tests GREEN
-> coherent checkpoint commit/publication
-> remote read-back of ref and changed bytes
-> update durable execution cursor
```

The task that owns a mechanism owns its RED-to-GREEN witnesses. Do not publish future-task failing tests. Related assertions may share one test class and one coherent checkpoint; do not create a commit per assertion.

## 6. Test and proof channels

Every obligation names one primary channel:

- `FOCUSED_BEHAVIOR` — deterministic owner-local behavior;
- `INTEGRATION_SCENARIO` — cross-owner/currentness/failure/indeterminate behavior;
- `STATIC_AUDIT` — exact schema, bytes, routing, absence or stale-reference evidence;
- `HOSTED_CI` — validation of the exact published HEAD;
- `EMPIRICAL_DEFERRED` — dormant measured/supported-target evidence whose trigger has not fired.

Static existence cannot discharge behavior. Hosted CI cannot prove semantics that no test exercises. Test-name existence cannot close a row. `EMPIRICAL_DEFERRED` does not become missing current work.

## 7. Negative-law minimum

Applicable tasks prove both acceptance and rejection for these classes:

- no second gameplay, identity, knowledge, history, chronology, currentness, recovery or authorization authority;
- no authority from cache/index/checkpoint/Story/projection/route name/commit metadata/SQL order/directory order;
- no visibility-to-knowledge inference and no recipient leakage;
- no accepted-mechanics replay, RNG reroll or identity reallocation on retry/recovery;
- no force update, ref deletion, broad ordinary authority scan or alternate Git transport;
- no role/diagnostic/tool/private result bypass around protected emission;
- no global active-player, campaign clock, universal pending queue, publication journal, durability frontier or cross-owner transaction;
- no pre-release compatibility layer, dual-read alias or migration solely for obsolete v0.8 bytes;
- no email identity authority and no login-only transfer of a stable PLAYER or creator binding.

## 8. Publication and currentness

Every correctness-sensitive publication uses:

```text
pin fresh remote parent H
-> build one coherent successor C with parent H
-> non-force update
-> read back remote ref/tree/files
```

An intervening ref advance, non-fast-forward rejection, indeterminate acknowledgement or non-monotonic movement is a currentness/integrity event. Reconcile it; never force, rewind, delete/recreate or blindly retry. No SQLite transaction spans repository, network, dialogue or model I/O.

Checkpoint-ready means another qualified worker can resume from published HEAD without hidden chat state or an unpublished second half required to make the repository valid.

## 9. Shared physical writers

The following final files have multiple semantic inputs and exactly one final integration checkpoint:

| Physical target | Required semantic inputs | Final checkpoint |
|---|---|---|
| `GAME/SCHEMA/README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots, temporal/current-state | `SHARED_SCHEMA_README_FINAL_INTEGRATION_READY` |
| `GAME/TEMPLATE/STORAGE_README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots | `SHARED_STORAGE_README_FINAL_INTEGRATION_READY` |
| `GAME/INSTALL/README.md` | shipped stale-projection repair + bootstrap/product | `RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION_READY` |
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | shipped stale-projection repair + bootstrap/product | same |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | shipped stale-projection repair + bootstrap/product | same |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | shipped transport/currentness + bounded bootstrap/product discovery | `CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY` |
| `GAME/CORE/STORAGE.md` | routing/storage + recovery/operational-root semantics | `CORE_STORAGE_FINAL_INTEGRATION_READY` |
| `GAME/CORE/MULTIPLAYER.md` | LIVE lifecycle, principal routing, collaboration and join/rejoin | `CORE_MULTIPLAYER_FINAL_INTEGRATION_READY` |
| `GAME/SCHEMA/scene.schema.yaml` | temporal chronology + LIVE route/currentness | `SCENE_SCHEMA_FINAL_INTEGRATION_READY` |
| `GAME/SCHEMA/location.schema.yaml` | routing/presence + information authority cleanup | `LOCATION_SCHEMA_FINAL_INTEGRATION_READY` |
| `GAME/SCHEMA/player.schema.yaml` and strict DEV PLAYER schema | collaboration route refs + final PLAYER authority shape | `RD16_PLAYER_STRICT_STATE_INTEGRATION_READY` |
| `GAME/SCHEMA/session.schema.yaml` | durability/publication observations + recovery/session currentness | `SESSION_SCHEMA_FINAL_INTEGRATION_READY` |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` and `GAME/CAMPAIGN/MANIFEST.yaml` | Story selector + bootstrap identity/scaffold + membership-field retirement | `W05_CAMPAIGN_MANIFEST_V5_READY` |
| `DEV/CATALOG/core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, world-kind admission ledger, identifier-policy schema and catalog projections | all 17 world families, 17 runtime families, MechanicalEvent, catalog-gap and source-native policy inputs | `RD16_SHARED_MACHINE_INTEGRATION_READY` |
| `DEV/PROJECT_MAP.md` | every new/changed shipped module, schema, test and current plan route | `PROJECT_MAP_FINAL_INTEGRATION_READY` |
| `DEV/TOOLS/audit_engine.py` | all new current/stale/schema/catalog/version/package checks | `MAINTENANCE_AUDIT_FINAL_INTEGRATION_READY` |

Owner-local tasks prepare bounded deltas/checkpoints. The final writer fresh-reads the current bytes, preserves every admitted input, applies one version transition where the target is versioned and runs integrated-byte proof.

## 10. Version Impact Gate

Every task identifies affected version/revision/schema/generation namespaces, applies each required transition exactly once and updates every projection/consumer in the same coherent checkpoint. `VERSION_IMPACT: NONE` requires an owner-law reason.

The exact consolidation-baseline targets are in `implementation-plan-index.md` and Wave 05. Inspect-only/conditional files are not bumped speculatively. Retired PC/NPC/item/faction contracts receive no terminal compatibility bump. `session.schema.yaml` remains v1 unless an actual fresh breaking shape is proven.

## 11. System-Impact Gate

Continue autonomously for ordinary RED/GREEN/debugging/path-currentness repair when accepted semantics unambiguously determine the result. Stop and publish a safe checkpoint only when implementation would require one of:

- a new or moved semantic authority;
- an unapproved persistent/interface/compatibility/migration/product rule;
- weakening an accepted invariant or proof;
- an owner/dependency set materially broader than this package;
- a new hard-to-reverse product decision;
- an unresolved conflict among current canonical owners.

Record the exact conflict, affected task/checkpoints, safe completed work and required decision. Do not ask a reviewer to reconstruct it from chat.

## 12. Per-task completion evidence

Before advancing to a dependent task, record:

```text
focused RED observed:
focused GREEN observed:
task-local suite:
integration/static witnesses:
actual Impact Envelope vs planned:
Version Impact result:
schema/catalog/checkpoint result:
stale-reference result:
published commit:
remote read-back:
produced checkpoint(s):
newly eligible dependent tasks:
```

Wave closure does not authorize the next unrelated task by number; it publishes the named outputs consumed by downstream tasks.
