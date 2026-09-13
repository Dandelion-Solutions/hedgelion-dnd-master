# RD-07 — Current-Native Recovery / Checkpoint Alignment — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. No production work is authorized until independent Senior plan GO.

Goal: realize current-native cold recovery and bounded maintenance while demoting checkpoint/session/local-cache data to accepted non-authoritative roles, aligning the active shipped STORAGE read-order instruction, and preserving accepted execution without replay/reroll.

RD unit: `RD-07`
Direct readiness: `R011,R012,R038,R072,R073,R074`.
Canonical owners: Step-5.2 RRC, Step-5.7 recovery, WP-14, WP-11/12 current routes/HOT, RD-05 retained execution evidence, RD-06 publication currentness.
Dependencies/joins: consumes RD-05 accepted execution evidence and RD-06 native publication/currentness results; selected-LIVE recovery additionally consumes RD-09 current source evidence; constrains RD-08 temporal recovery without owning temporal semantics.
Out of scope: gameplay rollback authority, LIVE authority, disclosure rewind, migration/release execution, alternate repository transport, checkpoint-as-current-state owner.

## Implementation Impact Envelope

SPEC / APPROVED DESIGN: Step-5.2/5.7, WP-14, exact readiness R011/R012/R038/R072/R073/R074.
BASELINE REF: fresh branch HEAD at execution.

EXPECTED OWNERS TO CHANGE:
- recovery executor/result contract;
- checkpoint/session shipped projections;
- active shipped `GAME/CORE/STORAGE.md` read-order wording required by R012.

EXPECTED CONSUMERS TO CHANGE:
- cold recovery/startup readers;
- RD-08 temporal recovery join;
- selected-LIVE recovery join with RD-09.

ALLOWED CONTRACTS:
- Create `GAME/TOOLS/recovery.py`;
- Create `DEV/SCHEMAS/recovery-result.schema.json`;
- Replace `GAME/SCHEMA/checkpoint.schema.yaml`;
- Modify `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` (confirmed current scaffold path);
- Modify `GAME/SCHEMA/session.schema.yaml`;
- Modify `GAME/CORE/STORAGE.md` only for current-native recovery/read-order semantics;
- modify named README/project-map/audit/test projections.

PROTECTED INVARIANTS:
- current native owner/source is selected before optional checkpoint/history/cache evidence;
- checkpoint/session/SQLite/chat context cannot select current authority;
- checkpoint may be absent on healthy recovery;
- no replay/reroll/re-ID of accepted execution;
- no generic rollback/ref rewind/allocator regression/disclosure rewind;
- selected LIVE cannot silently fall back to campaign source.

Version Impact: checkpoint/session/recovery contract changes are classified at each checkpoint; no migration is inferred merely because stale v0.8 projections exist.

## Task 1 — RED: current-source recovery selection

**Files**
- Create: `DEV/TESTS/test_rd07_recovery.py`
- Create in Task 2: `GAME/TOOLS/recovery.py`
- Create in Task 2: `DEV/SCHEMAS/recovery-result.schema.json`

**Result contract**
```text
RecoveryResult {
  disposition: READY | RETRY | BLOCKED
  reason_code: string | null
  affected_scopes: tuple[str, ...]
  diagnostic_evidence_refs: tuple[str, ...]
}
```
Ephemeral operation output only; never a stored RecoveryCut/frontier.

**RED cases**
- exact campaign/current native routes pinned before hydration;
- checkpoint/session/SQLite/chat context cannot select current authority;
- live-owned scope cannot fall back to campaign source;
- source movement yields RETRY/BLOCKED according to owner contract;
- healthy recovery may read zero checkpoints;
- no broad directory/history scan when exact roots/routes are known.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.CurrentSourceSelectionTests -v
```
Expected RED: shipped recovery executor/result contract absent.

No RED-only publication checkpoint.

## Task 2 — GREEN: current-native recovery engine

**Files**
- Create: `GAME/TOOLS/recovery.py`
- Create: `DEV/SCHEMAS/recovery-result.schema.json`
- Modify: `DEV/TESTS/test_rd07_recovery.py`

**Interfaces**
```text
recover_current_runtime(requested_scope, current_route_evidence) -> RecoveryResult
select_current_native_sources(requested_scope, current_route_evidence) -> SelectedSources
hydrate_required_closure(selected_sources) -> HydratedClosure
validate_recovered_basis(selected_sources, hydrated_closure) -> RecoveryResult
```

GREEN behavior: enumerate only admitted independent roots from current routing/lifecycle evidence; exact-pin one revision per mutable source; hydrate correctness-required dependencies/interpretation evidence; rebuild derived state only after native hydration; READY verifies source basis, required references and applicable authorization/eligibility.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.CurrentSourceSelectionTests -v
```
Expected GREEN.

REFACTOR: source-selection and hydration helpers remain internal; do not create generic currentness/frontier service.

Coherent checkpoint: recovery core + result schema + focused tests.

## Task 3 — R012 shipped STORAGE read-order alignment

**Files**
- Modify: `GAME/CORE/STORAGE.md`
- Modify: `DEV/TESTS/test_rd07_recovery.py`
- Modify: `DEV/TOOLS/audit_engine.py`

Current confirmed stale text says `MANIFEST -> ... -> latest checkpoint/hot STATE -> exact WORLD records`. Replace that checkpoint-first implication with the accepted order:

```text
Project Instructions
-> exact selected runtime/bootstrap
-> campaign MANIFEST/routing
-> exact current native owner/source routes for requested scope
-> correctness-required native dependencies
-> rebuildable HOT/index helpers after authority/currentness validation
-> optional selected checkpoint only as descriptor/evidence when a concrete recovery need calls for it
-> bounded history/log evidence as required
-> chat/older chats as non-authoritative recovery evidence only
```

During selected LIVE ownership, exact current LIVE source is resolved by RD-09 routing/currentness; checkpoint/hot campaign state never outranks it.

**RED cases**
- active `GAME/CORE/STORAGE.md` contains no `latest checkpoint` current-source/read-order rule;
- checkpoint/hot state cannot precede current native-source selection;
- null/no checkpoint remains healthy;
- storage prose and `recovery.py` source-selection tests express the same authority order.

Run RED before prose repair:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.StorageProjectionTests -v
```
Expected RED against the current shipped wording.

Run GREEN after repair:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.StorageProjectionTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: `GAME/CORE/STORAGE.md` + exact conformance test/audit projection. No unrelated persistence semantics changed.

## Task 4 — preserve accepted execution; no replay/reroll

**Files**
- Modify: `GAME/TOOLS/recovery.py`
- Inspect: `GAME/TOOLS/runtime_execution.py`
- Modify: `DEV/TESTS/test_rd07_recovery.py`

**RED/GREEN cases**
- unsettled RuntimeCommand/Procedure/Resolution resumes same stable identity;
- fixed RNG retained by RD-05 is reused;
- accepted invocation/catalog/rules/dependency interpretation preserved;
- Continuation/pending response resumes same generation;
- accepted temporal firing identity prevents duplicate rematerialization;
- cache/process loss creates no replacement accepted action/receipt/choice.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.AcceptedExecutionRecoveryTests -v
```

Coherent checkpoint: execution-recovery join R038 + focused tests. Recovery acquires no execution authority.

## Task 5 — checkpoint descriptor contract

**Files**
- Replace: `GAME/SCHEMA/checkpoint.schema.yaml`
- Modify: `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml`
- Modify: `GAME/SCHEMA/README.md`
- Modify: `DEV/TESTS/test_rd07_recovery.py`

**GREEN disposition**
- retain stable descriptor identity, campaign association and schema-format metadata;
- retire `valid_through_event_id` as recovery frontier;
- retire `expected_commit_sha` self-reference/currentness semantics;
- retained created/world-time/current-state/active IDs/engine/ruleset fields are diagnostic/provenance only where WP-14 permits;
- no RecoveryCut/root-completeness/source-manifest authority;
- nullable `MANIFEST.last_checkpoint_id` is selected descriptor pointer only.

**Tests** reject latest-by-timestamp/ID/directory inference and checkpoint-as-RRC proof.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.CheckpointDescriptorTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: checkpoint schema + exact current scaffold template + README/tests.

## Task 6 — session/HOT authority-negative closure

**Files**
- Modify: `GAME/SCHEMA/session.schema.yaml`
- Modify: `GAME/TOOLS/recovery.py`
- Inspect: `GAME/TOOLS/hot_store.py`
- Modify: `DEV/TESTS/test_rd07_recovery.py`

**Cases**
- session base/published HEADs are cached observations only;
- status cannot prove host liveness/death/current gameplay/write authority/save/handoff/recovery frontier;
- surviving HOT reused only after exact source-equivalence proof;
- current-native state wins over apparently newer local mtime/generation.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.SessionHotAuthorityTests -v
```

Coherent checkpoint: session/HOT recovery negatives + tests.

## Task 7 — bounded historical maintenance/repair

**Files**
- Modify: `GAME/TOOLS/recovery.py`
- Modify: `DEV/TESTS/test_rd07_recovery.py`

**Interfaces**
```text
inspect_historical_checkpoint(checkpoint_id, pinned_basis) -> MaintenanceResult
validate_repair_candidate(candidate, current_basis) -> MaintenanceResult
```

**Cases**: explicit historical target only; no ref rewind/current promotion; no allocator regression/disclosure rewind; missing retained dependency blocks/limits honestly; diagnostics/export never become gameplay authority.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.HistoricalMaintenanceTests -v
```

Coherent checkpoint: maintenance-only helpers/tests; ordinary recovery path remains unchanged.

## Task 8 — temporal/selected-LIVE joins and RD-07 verification

RD-08 consumes current temporal owner/binding state and rebuilds Agenda; accepted firing identity remains RD-05 evidence. Selected-LIVE recovery additionally requires RD-09 R079/R080 exact-source evidence before this integration can close.

Integration tests must prove both joins without moving their authority into recovery.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd07_recovery -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS.

Version Impact Gate: checkpoint/session/recovery contracts and projections synchronized exactly once. System Impact Gate stops on any new recovery/currentness/rollback authority.

Stale proof: no checkpoint/event frontier as current authority; no checkpoint commit self-reference requirement; no `latest checkpoint/hot STATE` current-source read rule; no latest-by-enumeration fallback; no session-as-current authority; no stale-HOT cold authority; no generic rollback/ref rewind or recovery replay/reroll.

Final coherent checkpoint: recovery runtime + result schema + STORAGE projection + checkpoint/session alignment + selected joins + tests/audits, with remote read-back. R068 pure-proof closure is reconciled package-wide rather than pre-claimed here.