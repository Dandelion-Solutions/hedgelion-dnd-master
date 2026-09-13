# RD-01 — Shipped / Stale Projection Repairs — Executable Implementation Plan

> For implementation workers: execute task-by-task under the current HDM execution process and Superpowers TDD workflow. RED-only failing checkpoints are never publication checkpoints.

Goal: make shipped instructions and stale GAME/DEV projections conform to accepted v1 owners without recreating removed v0.8 topology.

RD unit: `RD-01`
Direct readiness: `R001,R003,R033,R043,R047,R048,R050`.
Composite slices/parents: none.
Pure-proof leaves: none directly owned.
Canonical owners: exact Step-2 records and their domain/randomness/information owners; WP-26 documentation-routing closure.
Dependencies/joins: semantic owners only; parallel implementation root.
Out of scope: runtime subsystem implementation, release acceptance, new semantic architecture.

## Impact Envelope

Primary owner artifacts: accepted canonical specs only; do not edit them to fit implementation.
GAME runtime/projection surfaces with known active debt:
- `GAME/INSTALL/README.md` (`R001`,`R003`)
- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` (`R003`)
- `GAME/INSTALL/00_DND_BOOTSTRAP.md` (`R003`)
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` (`R003`)
- `GAME/CORE/RANDOMNESS.md` (`R043`)
- `GAME/CORE/DOMAIN_RULES_COVERAGE.md` (`R047`)
- `GAME/CORE/EXPLORATION.md` (`R048`)
- active `GAME/CORE/**` current-projection scan for `R033`/`R050` only.
DEV machine/check surfaces: `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`; `DEV/TOOLS/audit_engine.py` is `INSPECT_ONLY` unless its current assertions contradict repaired projections.
Cross-RD joins: none required before RD-01 completion.
Explicit exclusions / authority not transferred: docs/install files gain no semantic authority; no generic spatial engine; no new epistemic/event owner; no READY_PC blanket gate; no verbose per-turn RNG log requirement.
Version Impact: classify actual delta at execution checkpoint; do not pre-bump.
Schema/catalog/checkpoint impact: expected none.
Migration impact: none; v1 clean-slate policy applies.
HG-01 constraints affected: constraint 3 only.
Currentness/re-read set before write: exact seven Step-2 readiness records, current owners, and every path named above.

## Task 1 — RED: exact stale-projection guards

**Files**
- Create `DEV/TESTS/test_rd01_shipped_projection_repairs.py`.
- Inspect only the known-debt paths and bounded `GAME/CORE/**` scope for R033/R050.

Create test classes:
```text
InstallProjectionTests        -> R001,R003
RandomnessProjectionTests     -> R043
DomainExplorationTests        -> R047,R048
CoreCurrentProjectionTests    -> R033,R050
```

RED assertions:
1. `GAME/INSTALL/README.md` states supported ordinary Project-capable ChatGPT use without persisting model/plan identity (`R001`).
2. Four exact transport consumers use fixed Connector/no-probe/no-fallback (`R003`).
3. `GAME/CORE/RANDOMNESS.md` retains accepted RNG for recovery/retry without trivial-roll Git logging (`R043`).
4. `GAME/CORE/DOMAIN_RULES_COVERAGE.md` does not present old blocked/not-materialized wording as current (`R047`).
5. `GAME/CORE/EXPLORATION.md` uses bounded owner/applicability semantics and does not mandate a generic spatial engine (`R048`).
6. Active CORE scan rejects stale pre-live/complete-dossier/legacy-schema/blanket READY_PC semantics (`R033`).
7. Active CORE scan rejects stale entity prose contradicting current information owners or creating a second epistemic event log (`R050`).
8. Removed `GAME/AGENTS.md` / `GAME/CORE/START.md` are never required targets.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
```
Expected RED only for confirmed current mismatches. Record the failing assertions as RED evidence; **do not publish/commit a knowingly failing RED-only checkpoint**.

## Task 2 — GREEN: repair all exact named projections

**Files**
- Modify `GAME/INSTALL/README.md`.
- Modify `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`.
- Modify `GAME/INSTALL/00_DND_BOOTSTRAP.md`.
- Modify `GAME/CORE/BOOTSTRAP_RUNTIME.md`.
- Modify `GAME/CORE/RANDOMNESS.md`.
- Modify `GAME/CORE/DOMAIN_RULES_COVERAGE.md`.
- Modify `GAME/CORE/EXPLORATION.md`.
- Modify focused test.

GREEN behavior:
- independently rewrite stale current wording into accepted HDM v1 terminology;
- preserve already-correct v1 prose in mixed files;
- transport is absolute no-probe/no-fallback;
- supported product profile is explicit but model/plan identity is not campaign state;
- fixed RNG recovery preserves accepted values without verbose trace requirements;
- domain/exploration wording creates no package/spatial authority.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.InstallProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.RandomnessProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.DomainExplorationTests -v
```
Expected GREEN.

REFACTOR: collapse repeated wording only when one canonical local projection can serve all named shipped consumers; do not remove deliberate defense-in-depth at independent boundaries.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
```

Coherent checkpoint: all Task-2 changed projections + focused tests are green together. No unrelated runtime/schema changes.

## Task 3 — R033/R050 bounded current-projection closure

**Files**
- Inspect `GAME/CORE/**`, `GAME/SCHEMA/**`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` only for exact R033/R050 proof.
- Modify `DEV/TESTS/test_rd01_shipped_projection_repairs.py`.
- Modify a newly discovered active prose-only GAME/CORE consumer only after recording its exact path and tying it to R033/R050; a machine/schema/runtime contradiction is returned to its owning RD rather than edited here.

Run RED/GREEN scan test:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.CoreCurrentProjectionTests -v
```
Expected GREEN after any exact in-scope prose repair. Historical provenance is not rewritten merely to erase stale history.

REFACTOR: keep scan patterns exact to current forbidden semantics; no broad “old words” detector.

VERIFY / completion:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS.

Version Impact Gate: read current version owner and record `NONE` or exact mechanically required namespace transition from actual delta. System Impact Gate: any discovered need for runtime/schema/authority change is an owning-RD plan impact, not RD-01 scope expansion.

Completion evidence:
- all seven direct leaves map to explicit assertions/repairs;
- no historical path resurrected;
- GAME touched files classified `V1_COMPATIBLE`, `MIXED`, or `LEGACY_SUPERSEDED`;
- no trigger-gated/no-work item activated;
- remote read-back and hosted CI obtained after publication.

Final coherent checkpoint: Task 3 verification green + Task 2 checkpoint already green; RD-01 independently reviewable/resumable with no production runtime pulled in.