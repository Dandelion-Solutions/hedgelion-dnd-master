# RD-01 — Shipped / Stale Projection Repairs — Executable Implementation Plan

Goal: make shipped instructions and stale GAME/DEV projections conform to accepted v1 owners without recreating removed v0.8 topology.

RD unit: `RD-01`
Direct readiness: `R001,R003,R033,R043,R047,R048,R050`
Composite slices/parents: none.
Pure-proof leaves: none directly owned.
Canonical owners: exact Step-2 records and their domain/randomness/information owners; WP-26 documentation-routing closure.
Dependencies/joins: semantic owners only; parallel implementation root.
Out of scope: runtime subsystem implementation, release acceptance, new semantic architecture.

Baseline planning source: PB-02 Source Manifest at/after `8b8e1bad6d581ba4246ced91279ea0fb558f29c4`.

## Impact Envelope

Primary owner artifacts: existing canonical specs only; do not edit them to fit implementation.
GAME runtime/projection surfaces: `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, implicated install/bootstrap docs, implicated `GAME/CORE/**` prose.
DEV schemas/catalogs/machine contracts: only maintenance/routing guards proven necessary by RED.
Validators/tests/audits: `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`; maintenance audit only if an invariant is stable and low-noise.
Documentation/install/package projections: yes.
Cross-RD joins: none required before RD-01 completion.
Explicit exclusions / authority not transferred: docs/install files gain no semantic authority; no generic spatial engine; no new epistemic/event owner; no READY_PC blanket gate; no verbose per-turn RNG log requirement.
Version Impact: classify actual delta at execution checkpoint; do not pre-bump.
Schema/catalog/checkpoint impact: expected none unless a current guard contract proves otherwise.
Migration impact: none; v1 clean-slate policy applies.
HG-01 constraints affected: constraint 3 only — missing exact realization evidence does not imply new architecture.
Currentness/re-read set before write: exact readiness records, named owner specs, current instruction/install/CORE surfaces and any validator to be changed.

## Task 1 — Encode stale-projection failures

Files:
- `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`
- `INSPECT_ONLY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- `INSPECT_ONLY GAME/CORE/**`
- `INSPECT_ONLY GAME/INSTALL/**`

Interfaces: shipped instruction paths/references and exact accepted wording constraints from the seven readiness leaves.

RED:
1. Add focused tests that scan the actual shipped projection set and fail on the exact stale assumptions named by the leaves.
2. Assert removed historical paths such as `GAME/AGENTS.md` / `GAME/CORE/START.md` are not required as repair targets.
3. Add leaf-specific assertions for the implicated randomness/domain/exploration/information wording; do not create broad style assertions.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
```
Expected: failures identify current stale projection(s), not missing historical files as a reason to recreate them.

GREEN: none in this task; stop after RED is demonstrated and evidence identifies concrete modify targets.

REFACTOR: deduplicate test helpers only if semantics remain leaf-specific.

VERIFY: focused test remains RED for expected reasons only.

Commit boundary: checkpoint test/evidence only if independently understandable; otherwise commit with Task 2 as one coherent slice.

## Task 2 — Repair actual shipped projections

Files:
- `EXISTING_MODIFY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`
- `EXISTING_MODIFY` only the exact current install/bootstrap/CORE files exposed by Task 1 RED.
- Never create `GAME/AGENTS.md`, `GAME/CORE/START.md`, or other stale path solely to satisfy historical evidence.

Interfaces: installed prompt/instruction projection; current runtime-facing prose contract.

RED: re-run Task 1 test before edits and retain recorded expected failures.

GREEN:
- independently rewrite stale v0.8 wording into current HDM v1 terminology;
- preserve already-correct v1 prose in mixed files;
- remove path/authority assumptions that contradict accepted owners;
- keep fixed-RNG/recovery language at accepted granularity, not per-turn verbose logging.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
```
Expected: PASS.

REFACTOR: collapse duplicate prose only when doing so does not change owner scope or installation behavior.

VERIFY:
```bash
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: both PASS.

Commit boundary: coherent RD-01 projection repair, including focused test.

## Task 3 — Negative stale-reference and impact closure

Files:
- repository-wide inspected references under `GAME/**`, `DEV/**`, `.github/**` as applicable;
- modify only false/stale consumers justified by the readiness leaves.

RED: targeted repository search/test must expose any surviving forbidden stale reference or false authority claim.

GREEN: remove/repoint only confirmed stale consumers; do not broaden RD-01 into unrelated documentation cleanup.

VERIFY:
```bash
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS; no leaf-targeted stale references remain.

Version Impact Gate: read `DEV/RELEASE/VERSIONING.md` and detailed owner; record `NONE` or exact mechanically required namespace transitions from actual delta.

Completion evidence:
- all seven direct leaves mapped to assertions/repairs;
- no historical path resurrected;
- GAME touched files classified `V1_COMPATIBLE`, `MIXED`, or `LEGACY_SUPERSEDED` in execution review;
- no dormant/trigger-gated work activated;
- remote read-back and hosted CI obtained after publication.

Final commit boundary: RD-01 independently reviewable and resumable; then mark RD-01 plan task set complete without advancing another RD unit’s semantics.