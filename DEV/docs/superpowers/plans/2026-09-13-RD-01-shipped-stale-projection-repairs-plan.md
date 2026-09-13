# RD-01 — Shipped / Stale Projection Repairs — Executable Implementation Plan

Goal: make shipped instructions and stale GAME/DEV projections conform to accepted v1 owners without recreating removed v0.8 topology.

RD unit: `RD-01`
Direct readiness: `R001,R003,R033,R043,R047,R048,R050`.
Composite slices/parents: none.
Pure-proof leaves: none directly owned.
Canonical owners: exact Step-2 records and their domain/randomness/information owners; WP-26 documentation-routing closure.
Dependencies/joins: semantic owners only; parallel implementation root.
Out of scope: runtime subsystem implementation, release acceptance, new semantic architecture.

Baseline planning source: PB-02 Source Manifest at/after `8b8e1bad6d581ba4246ced91279ea0fb558f29c4`.

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
DEV machine/check surfaces: `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`; `DEV/TOOLS/audit_engine.py` is `INSPECT_ONLY` unless its current assertions contradict the repaired shipped projections.
Cross-RD joins: none required before RD-01 completion.
Explicit exclusions / authority not transferred: docs/install files gain no semantic authority; no generic spatial engine; no new epistemic/event owner; no READY_PC blanket gate; no verbose per-turn RNG log requirement.
Version Impact: classify actual delta at execution checkpoint; do not pre-bump.
Schema/catalog/checkpoint impact: expected none.
Migration impact: none; v1 clean-slate policy applies.
HG-01 constraints affected: constraint 3 only.
Currentness/re-read set before write: exact seven Step-2 readiness records, their current owners, and every path named above.

## Task 1 — RED: exact stale-projection guards

Files:
- `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`
- `INSPECT_ONLY` all known-debt paths in the Impact Envelope
- `INSPECT_ONLY GAME/CORE/**` only for R033/R050 stale-current-projection discovery.

RED assertions:
1. `GAME/INSTALL/README.md` states supported ChatGPT Plus + ordinary Project-capable chat without persisting model/plan identity (`R001`).
2. The four exact transport consumers use an absolute fixed Connector/no-probe/no-fallback rule (`R003`).
3. `GAME/CORE/RANDOMNESS.md` retains recovery-relevant fixed RNG result with Resolution/Continuation closure and requires restore/reuse/no-reroll without Git-logging trivial rolls (`R043`).
4. `GAME/CORE/DOMAIN_RULES_COVERAGE.md` no longer presents historical B-prime blocked/not-materialized text as current (`R047`).
5. `GAME/CORE/EXPLORATION.md` uses bounded location/procedure/applicability contracts and does not mandate a generic compact-map/spatial engine (`R048`).
6. Active CORE projection scan rejects stale pre-live/complete-dossier/legacy-schema routing or blanket READY_PC semantics (`R033`).
7. Active CORE projection scan rejects stale entity prose that contradicts current catalog knowledge fields or creates a second epistemic event log (`R050`).
8. Removed `GAME/AGENTS.md` / `GAME/CORE/START.md` are never required repair targets.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
```
Expected: RED only for the known current mismatches from the seven readiness leaves.

Commit boundary: combine with Task 2 unless the RED test is independently useful as a diagnostic checkpoint.

## Task 2 — GREEN: repair all known exact projections

Files:
- `EXISTING_MODIFY GAME/INSTALL/README.md`
- `EXISTING_MODIFY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- `EXISTING_MODIFY GAME/INSTALL/00_DND_BOOTSTRAP.md`
- `EXISTING_MODIFY GAME/CORE/BOOTSTRAP_RUNTIME.md`
- `EXISTING_MODIFY GAME/CORE/RANDOMNESS.md`
- `EXISTING_MODIFY GAME/CORE/DOMAIN_RULES_COVERAGE.md`
- `EXISTING_MODIFY GAME/CORE/EXPLORATION.md`
- `EXISTING_MODIFY DEV/TESTS/test_rd01_shipped_projection_repairs.py`

GREEN:
- independently rewrite only stale current wording into accepted HDM v1 terminology;
- preserve already-correct v1 prose in mixed files;
- fixed transport becomes absolute no-probe/no-fallback;
- Plus support profile is explicit but model/plan identity is not campaign state;
- fixed RNG recovery wording preserves accepted values and avoids verbose trace requirements;
- domain/exploration repairs do not invent package or spatial authority.

Run focused test; expected known exact projections PASS.

Commit boundary: these seven files + focused test are one coherent shipped-projection repair checkpoint.

## Task 3 — R033/R050 current-projection closure

Files:
- `INSPECT_ONLY GAME/CORE/**`
- `INSPECT_ONLY GAME/SCHEMA/**`
- `INSPECT_ONLY DEV/PROJECT_MAP.md`
- `INSPECT_ONLY DEV/TOOLS/audit_engine.py`
- `EXISTING_MODIFY DEV/TESTS/test_rd01_shipped_projection_repairs.py`

The scan is proof scope, not blanket write authority. If a currently active R033/R050 contradiction is found outside Task-2 paths, record its exact path before editing and compare it to this Impact Envelope. Because those two readiness leaves explicitly authorize narrow current-projection reconciliation, a prose-only active GAME/CORE consumer may be added to this RD-01 checkpoint; a machine/schema/runtime owner change is **not** implicitly authorized and is a plan-impact finding for its owning RD instead.

GREEN: focused guard proves no current active stale routing/READY_PC/second-epistemic-log contradiction remains; historical provenance docs are not rewritten merely to erase history.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: read `DEV/RELEASE/VERSIONING.md` and detailed owner; record `NONE` or exact mechanically required namespace transitions from actual delta.

Completion evidence:
- all seven direct leaves map to explicit assertions/repairs;
- no historical path resurrected;
- GAME touched files classified `V1_COMPATIBLE`, `MIXED`, or `LEGACY_SUPERSEDED`;
- no trigger-gated/no-work item activated;
- remote read-back and hosted CI obtained after publication.

Final commit boundary: RD-01 independently reviewable and resumable; no runtime implementation is pulled into this unit.