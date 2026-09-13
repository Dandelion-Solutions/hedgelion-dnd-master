# RD-07 — Current-Native Recovery / Checkpoint Alignment — Executable Implementation Plan

Goal: realize current-native cold recovery and bounded maintenance while demoting checkpoint/session/local-cache data to their accepted non-authoritative roles and preserving accepted execution without replay/reroll.

RD unit: `RD-07`
Direct readiness: `R011,R012,R038,R072,R073,R074`.
Composite slices/parents: none.
Pure-proof leaves: none directly owned.
Canonical owners: Step-5.2 RRC, Step-5.7 recovery, WP-14, WP-11/12 current routes/HOT, RD-05 retained execution evidence, RD-06 publication currentness.
Dependencies/joins: consumes RD-05 accepted execution evidence and RD-06 native publication/currentness results; constrains RD-08 temporal recovery and later LIVE/currentness work without owning them.
Out of scope: gameplay rollback authority, LIVE authority, disclosure rewind, migration/release execution, alternate repository transport, checkpoint-as-current-state owner.

## Impact Envelope

GAME runtime: `NEW_CREATE GAME/TOOLS/recovery.py`.
GAME schemas/templates: `EXISTING_REPLACE GAME/SCHEMA/checkpoint.schema.yaml`; `EXISTING_MODIFY GAME/SCHEMA/session.schema.yaml`; `EXISTING_MODIFY` exact checkpoint template under `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` if present at execution currentness check; no replacement selector/frontier schema.
DEV contracts: `NEW_CREATE DEV/SCHEMAS/recovery-result.schema.json` for ephemeral validation shape only.
Tests: `NEW_CREATE DEV/TESTS/test_rd07_recovery.py`.
Docs/audit: `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` only for direct recovery/checkpoint semantics.
Cross-RD: RD-05 stable acceptance/RNG/interpretation; RD-06 current publication/ref evidence; RD-08 armed temporal owner reconstruction; later RD-09 LIVE exact-source currentness.
Negative laws: no checkpoint-first restore, latest checkpoint by enumeration/time/ID, stale HOT as cold authority, checkpoint/session HEAD as source selector, generic rollback/ref rewind, allocator/disclosure rewind, replay/reroll/re-ID of accepted work, broad Git/WORLD scans as healthy fallback.
Version/schema/checkpoint: checkpoint schema generation likely changes; Version Impact gate decides exact bump.
Migration: no historical campaign migration execution.
HG-01: constraints 2/3; recovery cannot invent transient fiction or hidden semantics from missing evidence.
Currentness set: Step-5.2/5.7, WP-14, WP-11/12, RD-05/06 plans/contracts, checkpoint/session schemas/template and current recovery-related docs.

## Task 1 — RED: current-source recovery selection

Files:
- `NEW_CREATE DEV/TESTS/test_rd07_recovery.py`
- `NEW_CREATE DEV/SCHEMAS/recovery-result.schema.json` in GREEN.

Result contract:
```text
RecoveryResult {
  disposition: READY | RETRY | BLOCKED
  reason_code?
  affected_scopes?
  diagnostic_evidence_refs?
}
```
It is ephemeral operation output, not persisted RecoveryCut/frontier.

RED cases:
1. selected campaign/current native routes are exact-pinned before hydration;
2. checkpoint/session/SQLite/chat context cannot select current authority;
3. live-owned route cannot silently fall back to campaign source;
4. current-source movement yields RETRY/BLOCKED as owner requires;
5. ordinary healthy recovery can read zero checkpoints;
6. broad directory/history scans are not required when exact roots/routes are known.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery -v
```
Expected: RED because shipped recovery executor/result contract is absent.

## Task 2 — GREEN: current-native recovery engine

Files:
- `NEW_CREATE GAME/TOOLS/recovery.py`
- `NEW_CREATE DEV/SCHEMAS/recovery-result.schema.json`
- focused test.

Interfaces:
```text
recover_current_runtime(requested_scope, current_route_evidence) -> RecoveryResult
select_current_native_sources(...)
hydrate_required_closure(...)
validate_recovered_basis(...)
```

GREEN:
- enumerate only admitted independent roots from current lifecycle/routing evidence;
- exact-pin one revision per participating mutable source for the attempt;
- hydrate only correctness-required dependencies/interpretation evidence;
- rebuild derived state after native hydration;
- final READY validates participating current basis, authorization/eligibility where applicable, references and RRC completeness.

Commit boundary: current-source recovery core + result schema/tests.

## Task 3 — Preserve accepted execution; no replay/reroll

Files:
- `EXISTING_MODIFY GAME/TOOLS/recovery.py`
- `INSPECT_ONLY GAME/TOOLS/runtime_execution.py`
- focused test.

RED/GREEN scenarios:
- unsettled RuntimeCommand/Procedure/Resolution resumes same stable identity;
- retained fixed RNG from RD-05 is reused;
- accepted invocation/catalog/rules/dependency interpretation is preserved;
- Continuation/pending response evidence resumes same generation;
- accepted temporal firing identity prevents duplicate rematerialization;
- process/cache loss never creates replacement accepted action, receipt or choice.

This realizes R038 integration without transferring execution authority to recovery.

## Task 4 — Replace checkpoint contract with WP-14 descriptor semantics

Files:
- `EXISTING_REPLACE GAME/SCHEMA/checkpoint.schema.yaml`
- `EXISTING_MODIFY GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` if current file exists; if repository topology moved mechanically, use the current checkpoint template at the canonical scaffold location and record path adaptation
- `EXISTING_MODIFY GAME/SCHEMA/README.md`
- focused test.

GREEN disposition:
- retain stable descriptor identity + campaign association + schema-format metadata;
- retire `valid_through_event_id` as recovery frontier;
- retire `expected_commit_sha` self-reference/currentness semantics;
- any retained created/world-time/current-state/active IDs/engine/ruleset fields are explicitly non-authoritative diagnostic/provenance hints per WP-14;
- no new RecoveryCut/root-completeness/source-manifest field;
- nullable `MANIFEST.last_checkpoint_id` remains only selected descriptor pointer; null is healthy.

RED/GREEN tests reject latest-by-timestamp/ID/directory inference and checkpoint-as-RRC proof.

Commit boundary: checkpoint schema/template demotion + tests/docs projection.

## Task 5 — Session/local HOT authority-negative closure

Files:
- `EXISTING_MODIFY GAME/SCHEMA/session.schema.yaml`
- `EXISTING_MODIFY GAME/TOOLS/recovery.py`
- `INSPECT_ONLY GAME/TOOLS/hot_store.py`
- focused test.

GREEN:
- session base/published HEADs are cached observations only;
- session status cannot prove host liveness/death/current gameplay/write authority/save/handoff/recovery frontier;
- surviving HOT is reused only after exact source-equivalence proof; otherwise rebuild from current native sources;
- current-native state wins over apparently newer local mtime/generation.

## Task 6 — Bounded historical maintenance/repair

Files:
- `EXISTING_MODIFY GAME/TOOLS/recovery.py`
- focused test.

Interfaces:
```text
inspect_historical_checkpoint(checkpoint_id, pinned_basis) -> MaintenanceResult
validate_repair_candidate(...) -> MaintenanceResult
```
These are separate evidence-gated maintenance operations, not ordinary current recovery fallback.

RED/GREEN:
- explicit historical target only;
- no ref rewind/current promotion from stale reconstruction;
- no allocator regression or disclosure rewind;
- missing retained dependencies blocks/limits maintenance honestly;
- diagnostics/export evidence never becomes gameplay authority.

## Task 7 — Closure and downstream temporal join

RD-08 recovery integration must consume current temporal owner/binding state and rebuild Agenda, while already accepted firing stays in RD-05 execution. RD-07 records the interface but does not implement thread/Agenda semantics.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify checkpoint/session/recovery contract generations; synchronize exact schema/template/docs/audit projections once.

Stale proof: active GAME/DEV contains no checkpoint/event frontier as current authority, checkpoint commit self-reference requirement, latest-by-enumeration fallback, session-as-current authority, stale-HOT cold authority, generic rollback/ref rewind or recovery replay/reroll.

Final commit boundary: `recovery.py` + recovery-result schema + checkpoint/session alignment + tests/projections form independently reviewable RD-07 result.