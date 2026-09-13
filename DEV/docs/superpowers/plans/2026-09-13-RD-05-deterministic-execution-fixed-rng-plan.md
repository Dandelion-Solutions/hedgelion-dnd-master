# RD-05 — Deterministic Execution / Fixed-RNG Closure / Failure Adapters — Executable Implementation Plan

Goal: realize accepted runtime-lifecycle execution with deterministic mechanics, stable accepted identities, retained fixed RNG and typed owner-local failure/degradation behavior.

RD unit: `RD-05`
Direct readiness: `R034,R035,R036,R042,R046,R112`.
Composite slices/parents: `R016.EXECUTION,R018.EXECUTION,R062.RUNTIME_LIFECYCLE_EVIDENCE`.
Pure-proof leaves: none directly owned.
Canonical owners: Step-3 execution boundary; Step-5.2 resumable runtime closure; WP-10 lifecycle/evidence allocation; WP-12 local atomicity; WP-25 failure/degradation; exact Step-2 records.
Dependencies/joins: consumes RD-04 local HOT/owner transaction substrate and finalized native owner schemas; `R034+R035+R036 JOIN_BEFORE_INTEGRATION R037` in RD-06.
Out of scope: durability/publication, recovery source selection, temporal occurrence ownership, LIVE/CAS, role/emission, generic transaction/state engine.

## Impact Envelope

GAME runtime: `NEW_CREATE GAME/TOOLS/runtime_execution.py`, `NEW_CREATE GAME/TOOLS/mechanics.py`; `GAME/CORE/RANDOMNESS.md` is read/currentness input and modified only if tests prove a remaining contradiction after RD-01.
DEV machine contracts: reconcile existing `runtime-*-state` schemas, `execution-segment.schema.json`, `resolution-receipt.schema.json`, roll/mechanical schemas; no duplicate lifecycle family.
Tests: `NEW_CREATE DEV/TESTS/test_rd05_runtime_execution.py`.
Docs/audit: `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` only for direct new shipped-module/schema projection.
Cross-RD: RD-04 HOT; RD-06 SAVE after established transaction; RD-07 retained accepted evidence; RD-08 accepted firing handoff.
Negative laws: no reroll-on-retry, event-ID RNG seed, global nonce/correlation authority, generic pending/job/transaction owner, host/repo/network work inside mechanic transaction, diagnostic authority.
Version/schema/checkpoint: classify actual schema/API generation changes; no checkpoint ownership.
Migration: none under v1 clean-slate.
HG-01: constraints 1/3; deterministic executor cannot become semantic/NPC intent authority and missing realization does not reopen architecture.
Currentness set: Step-3, Step-5.2, WP-10/12/25, exact six readiness records, all named DEV schemas and current GAME/TOOLS.

## Task 1 — RED: accepted lifecycle and identity invariants

Files:
- `NEW_CREATE DEV/TESTS/test_rd05_runtime_execution.py`
- `INSPECT_ONLY DEV/SCHEMAS/runtime-command-state.schema.json`
- `runtime-continuation-state.schema.json`
- `runtime-intent-plan-state.schema.json`
- `runtime-interaction-state.schema.json`
- `runtime-procedure-state.schema.json`
- `runtime-resolution-state.schema.json`
- `runtime-mechanical-event-state.schema.json`
- `runtime-resolution-trace-state.schema.json`
- `execution-segment.schema.json`
- `resolution-receipt.schema.json`.

RED cases:
1. stable accepted `acceptance_id` and derived execution/segment/firing identities survive retry;
2. duplicate invocation with same accepted boundary is idempotent;
3. invalid required proposal field returns `EXECUTION_PROPOSAL_INVALID_REQUIRED_FIELD` and mutates nothing;
4. fixed accepted RNG result is retained and reused;
5. receipt/segment remain evidence under owning execution lifecycle, not independent workflow owners;
6. no unresolved lifecycle object can be represented only by generic pending/status state.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution -v
```
Expected: RED because shipped executor is absent and any schema gaps are identified precisely.

## Task 2 — GREEN: deterministic mechanics core

Files:
- `NEW_CREATE GAME/TOOLS/mechanics.py`
- `EXISTING_MODIFY` only exact mechanical/roll schemas failing Task-1 assertions.

Shipped interfaces:
```text
resolve_mechanic(normalized_request, definition, binding, accepted_rng=None) -> MechanicalOutcome
validate_execution_proposal(proposal) -> ValidationResult
```

GREEN laws:
- same normalized request/definition/binding + same accepted RNG => same result;
- no LLM arithmetic or prose-only mechanic math;
- unavailable required deterministic math returns typed degraded/failure result and no mutation;
- accepted RNG is input/evidence, never regenerated during retry.

VERIFY focused tests PASS for mechanics cases.

Commit boundary: mechanics + exact schema reconciliation + tests.

## Task 3 — GREEN: runtime lifecycle executor

Files:
- `NEW_CREATE GAME/TOOLS/runtime_execution.py`
- `EXISTING_MODIFY` exact runtime lifecycle schemas proven incomplete by RED
- `EXISTING_MODIFY DEV/TESTS/test_rd05_runtime_execution.py`.

Shipped interfaces:
```text
accept_command(...)
execute_segment(...)
resume_accepted_execution(...)
close_resolution(...)
```
Each consumes/returns typed owner-native lifecycle records; functions do not create a generic engine-state record.

GREEN:
- declaration -> accepted execution -> deterministic mechanics -> owner/effect delta -> receipts/evidence occurs within permitted local owner-establishment boundary;
- lifecycle transition is independently schema-valid/routable;
- retries with retained accepted evidence do not allocate replacement accepted IDs;
- unresolved Continuation preserves same execution generation.

VERIFY focused tests PASS.

Commit boundary: lifecycle executor + reconciled lifecycle contracts.

## Task 4 — Local atomicity and observable outcome closure

Files:
- `EXISTING_MODIFY GAME/TOOLS/runtime_execution.py`
- `INSPECT_ONLY GAME/TOOLS/hot_store.py` from RD-04 implementation contract
- focused test.

RED/GREEN scenarios:
- permitted mechanic transaction commits declaration/RNG/result/effects/evidence together or none;
- validation failure performs zero owner mutation;
- exception/failure before establishment leaves no partial accepted consequence;
- external host choice, Connector/repository I/O and network work cannot occur inside the local transaction boundary.

The test uses the RD-04 `NativeHotStore` interface; it does not reimplement persistence.

## Task 5 — Composite and downstream closure

Evidence:
- R016.EXECUTION and R018.EXECUTION explicitly map to accepted runtime execution behavior;
- `R062.RUNTIME_LIFECYCLE_EVIDENCE` maps to exact lifecycle/evidence schemas and tests;
- no publication/currentness metadata is introduced here;
- RD-06 receives established post-transaction owner-generation set;
- RD-07 receives retained acceptance/RNG/interpretation evidence;
- RD-08 receives stable accepted execution/firing identity.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify actual runtime/mechanical schema/API changes under current version owners and synchronize required projections once.

Stale proof: active GAME/DEV surfaces contain no reroll-on-retry requirement, global execution nonce, generic pending/job/transaction owner or alternate mechanic arithmetic authority.

Final commit boundary: `mechanics.py` + `runtime_execution.py` + exact schema/audit projection + tests form one independently reviewable RD-05 result.