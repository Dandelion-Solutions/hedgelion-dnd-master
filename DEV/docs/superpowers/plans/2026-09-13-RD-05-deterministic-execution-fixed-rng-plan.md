# RD-05 — Deterministic Execution / Fixed-RNG Closure / Failure Adapters — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. Do not publish knowingly failing RED-only checkpoints.

Goal: realize accepted runtime-lifecycle execution with deterministic mechanics, stable accepted identities, retained fixed RNG and typed owner-local failure/degradation behavior.

RD unit: `RD-05`
Direct readiness: `R034,R035,R036,R042,R046,R112`.
Composite slices: `R016.EXECUTION,R018.EXECUTION,R062.RUNTIME_LIFECYCLE_EVIDENCE`.
Canonical owners: Step-3 execution boundary; Step-5.2 resumable runtime closure; WP-10 lifecycle/evidence allocation; WP-12 local atomicity; WP-15 Procedure/Continuation temporal alignment; WP-25 failure/degradation; exact Step-2 records.
Dependencies/joins: consumes RD-04 local HOT/owner transaction substrate and finalized native owner schemas; `R034+R035+R036 JOIN_BEFORE_INTEGRATION R037` in RD-06. RD-08 consumes the accepted firing/Continuation evidence after the Procedure/Continuation alignment in Task 3.
Out of scope: durability/publication, recovery source selection, temporal occurrence ownership, LIVE/CAS, role/emission, generic transaction/state engine.

## Impact Envelope

GAME runtime:
- Create `GAME/TOOLS/runtime_execution.py`.
- Create `GAME/TOOLS/mechanics.py`.
- `GAME/CORE/RANDOMNESS.md` inspect-only unless RD-01 currentness leaves a proven contradiction.

DEV machine contracts to reconcile, not duplicate:
- `runtime-command-state.schema.json`
- `runtime-continuation-state.schema.json`
- `runtime-intent-plan-state.schema.json`
- `runtime-interaction-state.schema.json`
- `runtime-procedure-state.schema.json`
- `combat-minimal-procedure-state.schema.json` as the existing concrete Procedure-owned timing/order/budget contract
- `runtime-resolution-state.schema.json`
- `runtime-mechanical-event-state.schema.json`
- `runtime-resolution-trace-state.schema.json`
- `execution-segment.schema.json`
- `resolution-receipt.schema.json`
- exact roll/mechanical schemas implicated by RED.

Tests: create `DEV/TESTS/test_rd05_runtime_execution.py`.
Projection/audit: modify `DEV/PROJECT_MAP.md` and `DEV/TOOLS/audit_engine.py` only for direct new shipped modules/schema checks.
Cross-RD: RD-04 HOT; RD-06 SAVE; RD-07 retained accepted evidence; RD-08 accepted firing/temporal occurrence; RD-09 LIVE execution join; RD-10 role/emission remains separate.

Protected laws: no reroll-on-retry; no event-ID RNG seed; no global nonce/correlation authority; no generic pending/job/transaction owner; no host/repo/network work inside mechanic transaction; diagnostics never become gameplay authority; Procedure-local timing/order/budgets remain `runtime.procedure`; Continuation retains accepted RNG/results but owns no generic future RNG schedule or ambient elapsed-time catch-up.
Version/checkpoint/migration: classify actual API/schema generations; no checkpoint/recovery ownership; no migration activation.

## Task 1 — RED: accepted lifecycle and identity invariants

**Files**
- Create `DEV/TESTS/test_rd05_runtime_execution.py`.
- Inspect exact lifecycle/evidence schemas listed above.

Create test groups:
```text
AcceptedIdentityTests
FixedRngTests
ProposalValidationTests
LifecycleEvidenceTests
ProcedureTemporalStateTests
ContinuationTemporalStateTests
```

RED cases:
- stable `acceptance_id` and derived execution/segment/firing identities survive retry;
- duplicate invocation with same accepted boundary is idempotent;
- invalid required proposal returns `EXECUTION_PROPOSAL_INVALID_REQUIRED_FIELD` and mutates nothing;
- fixed accepted RNG is retained/reused;
- receipt/segment are evidence, not independent workflow owners;
- unresolved lifecycle cannot collapse into generic pending/status state;
- generic `runtime.procedure` machine contract does not yet expose/compose the accepted Procedure-owned local lifecycle/order/timing/budget state already represented by concrete Procedure contracts;
- `runtime.continuation` still requires generic `future_rng_frontier`, which WP-15 rejects absent a separately proven reserve-before-generation mechanic.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.AcceptedIdentityTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.FixedRngTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProcedureTemporalStateTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ContinuationTemporalStateTests -v
```
Expected RED because shipped executor is absent and Procedure/Continuation contracts retain the stated machine debt. Record RED evidence only; no publication checkpoint.

## Task 2 — GREEN: deterministic mechanics core

**Files**
- Create `GAME/TOOLS/mechanics.py`.
- Modify only exact mechanical/roll schemas proven incomplete by Task 1.
- Modify focused test.

**Interfaces**
```text
resolve_mechanic(normalized_request, definition, binding, accepted_rng=None) -> MechanicalOutcome
validate_execution_proposal(proposal) -> ValidationResult
```

GREEN laws:
- same normalized request/definition/binding + same accepted RNG => same result;
- deterministic math is code/rule-defined, not LLM prose arithmetic;
- missing/invalid required deterministic input returns typed failure/degraded outcome and zero mutation;
- accepted RNG is input/evidence, never regenerated on retry.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.FixedRngTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProposalValidationTests -v
```
Expected GREEN.

REFACTOR: keep mechanical calculation helpers pure and owner-specific; no generic rules engine/state service.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.FixedRngTests DEV.TESTS.test_rd05_runtime_execution.ProposalValidationTests -v
```

Coherent checkpoint: mechanics module + exact implicated schemas + focused tests all green.

## Task 3 — GREEN: runtime lifecycle executor + Procedure/Continuation contract alignment

**Files**
- Create `GAME/TOOLS/runtime_execution.py`.
- Modify exact runtime lifecycle schemas proven incomplete by RED.
- Modify `DEV/SCHEMAS/runtime-procedure-state.schema.json` so the native `runtime.procedure` record structurally owns or composes the applicable concrete Procedure lifecycle/order/timing/budget state instead of leaving that state as an unrelated second owner.
- Reconcile `DEV/SCHEMAS/combat-minimal-procedure-state.schema.json` only if required to keep its existing `procedure_kind`, lifecycle, participant, initiative, round/turn and participant-budget state one Procedure-owned contract; do not copy those fields into scene/thread/Continuation.
- Modify `DEV/SCHEMAS/runtime-continuation-state.schema.json`: remove generic required `future_rng_frontier` unless a separate accepted reserve-before-generation mechanic is proven at execution time; retain already accepted `fixed_rng_results`; permit `unconsumed_advancement` only as the exact typed remainder of accepted execution suspended at an admitted due boundary, never host-time/restart/global-fictional-time catch-up.
- Modify focused test.
- Modify `DEV/PROJECT_MAP.md` / `DEV/TOOLS/audit_engine.py` for newly shipped runtime module/contracts.

**Interfaces**
```text
accept_command(interaction, intent_plan, command_request, acceptance_basis) -> RuntimeCommand
execute_segment(command, procedure, owner_state, accepted_rng) -> SegmentResult
resume_accepted_execution(accepted_execution, retained_evidence) -> SegmentResult
close_resolution(segment_results, owner_deltas) -> RuntimeResolution
```

GREEN:
- Interaction/IntentPlan/Command/Procedure/Resolution/Continuation are typed owner-native lifecycle records;
- accepted IDs are allocated once and reused;
- unresolved Continuation preserves same execution generation;
- Procedure-local initiative/order/round/turn/budget/timing state remains in `runtime.procedure` or its concrete Procedure schema and is not mirrored into `world.thread`, scene or Continuation;
- concrete Procedure subtype state is part of the same native Procedure authority, not a parallel record owner;
- Continuation retry uses stored accepted fixed RNG and never derives a new RNG schedule from `future_rng_frontier`;
- `unconsumed_advancement`, when present, is validated as an exact accepted-execution remainder in its declared context/unit and cannot mean ambient elapsed time;
- MechanicalEvent/receipt/ResolutionTrace remain evidence under runtime.execution ownership;
- generic execution state/result bus is not introduced.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.AcceptedIdentityTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.LifecycleEvidenceTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProcedureTemporalStateTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ContinuationTemporalStateTests -v
```
Expected GREEN.

REFACTOR: common transition validation may be private helpers in `runtime_execution.py`; do not create a generic workflow framework or a second Procedure/temporal owner.

VERIFY:
```bash
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProcedureTemporalStateTests DEV.TESTS.test_rd05_runtime_execution.ContinuationTemporalStateTests -v
```

Coherent checkpoint: lifecycle executor + exact reconciled lifecycle/evidence/Procedure/Continuation schemas + tests/audit/project-map all green. This checkpoint is the concrete machine discharge used by WP-15 §13 items 12–13; package proof still joins it with RD-08/RD-13 for R077.

## Task 4 — local atomicity and observable outcome closure

**Files**
- Modify `GAME/TOOLS/runtime_execution.py`.
- Consume `GAME/TOOLS/hot_store.py` / `NativeHotStore.transaction(...)` from RD-04.
- Modify focused test.

Create `ExecutionAtomicityTests`.

**RED cases** before integration:
- accepted mechanic path has no real HOT all-or-none binding;
- injected validation/commit failure can expose partial accepted consequence.

**GREEN behavior**
```text
accepted command/segment basis
-> deterministic mechanic resolution
-> owner/effect delta validation
-> one permitted local HOT transaction
-> owner delta + runtime evidence/receipt establishment
-> commit all or none
```
External player/host choice, Connector/repository/network I/O remain outside transaction.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ExecutionAtomicityTests -v
```
Expected GREEN after binding.

REFACTOR: transaction adapter is narrow; execution does not reimplement HOT/storage.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution -v
```

Coherent checkpoint: execution/HOT integration + atomicity tests, all green.

## Task 5 — stable downstream evidence adapters

**Files**
- Modify `GAME/TOOLS/runtime_execution.py` only if Tasks 3–4 do not already expose the required typed read interfaces.
- Modify focused tests.

**Interfaces produced**
```text
established_owner_generation_set(resolution) -> OwnerGenerationSet       # RD-06
retained_execution_recovery_basis(resolution_or_continuation) -> ExecutionRecoveryBasis  # RD-07
accepted_firing_execution_basis(resolution) -> AcceptedFiringBasis       # RD-08
current_execution_source_basis(resolution) -> ExecutionSourceBasis        # RD-09
```
These are typed projections of accepted execution evidence, not new durable owners.

Create `DownstreamExecutionEvidenceTests` proving no adapter can reroll/re-ID/reinterpret accepted execution.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.DownstreamExecutionEvidenceTests -v
```
Expected GREEN.

REFACTOR: reuse existing retained evidence records where sufficient; avoid parallel evidence DTOs if an accepted schema already carries the required basis.

Coherent checkpoint: only missing adapters + tests; otherwise evidence-only no-code checkpoint recorded in execution notes.

## Task 6 — direct/composite closure and verification

Map:
- R016.EXECUTION / R018.EXECUTION -> Tasks 2–4 accepted runtime behavior;
- `R062.RUNTIME_LIFECYCLE_EVIDENCE` -> exact lifecycle/evidence schemas + Task-3/5 tests;
- R034/R035/R036 -> identity/atomicity/RNG target consumed by RD-06 R037;
- R042/R046/R112 -> exact proposal/failure/determinism scenarios named in focused tests;
- WP-15 §13.12 -> `ProcedureTemporalStateTests` + reconciled Procedure contracts;
- WP-15 §13.13 -> `ContinuationTemporalStateTests` + reconciled Continuation contract.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS.

Version Impact Gate: classify runtime/mechanical/Procedure/Continuation schema/API changes and synchronize required projections. System Impact Gate stops if realization requires a new mechanics/transaction/currentness/role/Procedure/temporal authority.

Stale proof: no reroll-on-retry, global execution nonce, generic pending/job/transaction owner, generic future RNG schedule, host-time/restart catch-up in Continuation, duplicate Procedure timing owner, host/repo/network inside local mechanic transaction or alternate arithmetic authority.

Final coherent checkpoint: all RD-05 focused/full verification green, direct/composite evidence recorded, remote read-back obtained. R041 pure-proof reconciliation and R077 package-level join remain proof-ledger work.