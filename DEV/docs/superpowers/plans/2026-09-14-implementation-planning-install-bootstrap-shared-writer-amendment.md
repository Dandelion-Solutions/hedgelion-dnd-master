# Implementation Planning — Install / Bootstrap Shared-Writer Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 39 — SIGNIFICANT**

## Finding

RD-01 and RD-14 independently plan writes to the same shipped installation/bootstrap projection files:

```text
GAME/INSTALL/README.md
GAME/INSTALL/PROJECT_INSTRUCTIONS.txt
GAME/INSTALL/00_DND_BOOTSTRAP.md
```

RD-01 owns stale-projection cleanup for accepted v1 transport/product/currentness laws. RD-14 owns the final bootstrap/New-Game/campaign-selection/product flow projected into the same shipped surfaces.

The current execution graph has explicit shared-file checkpoints for scene routing, catalog-binding prose, multiplayer/session prose, historical GAME schema overlaps, `PROJECT_MAP` and `audit_engine.py`, but no checkpoint for these three install/bootstrap files.

Therefore both RDs may be locally correct while a legal implementation order still overwrites the other's admitted semantics. A worker would have to invent merge/order policy. Because these are shipped operational instructions, this is not cosmetic documentation drift: stale guidance can direct incorrect bootstrap/currentness/transport behavior.

No semantic owner changes. This is a physical shared-writer / shipped-consumer cutover defect.

---

# 1. Ownership split

Semantic ownership remains unchanged:

- RD-01 owns only the stale/current projection deltas required by `R001,R003,R033,R043,R047,R048,R050` and WP-26 documentation-routing closure;
- RD-14 owns bootstrap/product flow semantics from WP-19 and its accepted downstream joins;
- install files remain projections and gain no semantic authority.

Physical final-writer responsibility for the three overlapping install files is assigned to the RD-14 **final install/bootstrap projection checkpoint**, because RD-14 necessarily composes the later product flow after its runtime/bootstrap joins are known.

This physical assignment does not transfer RD-01 semantic duties to RD-14.

---

# 2. Required checkpoint split

RD-01 Task 2/3 produces a named local projection checkpoint:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
```

It means the RD-01-required v1 transport/currentness/stale-projection assertions have a coherent candidate delta and focused tests are GREEN. RD-01 may publish owner-local changes to non-overlapping files independently.

For the three overlapping install files, RD-14 final product documentation integration produces:

```text
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

Required edge:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
+ RD14 bootstrap/product semantic checkpoints required by the touched text
  SHARED_FILE_CHECKPOINT / JOIN_BEFORE_INTEGRATION
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

The final writer fresh-reads current bytes at its exact execution checkpoint and composes both admitted requirement sets.

---

# 3. File-specific merge law

For each overlapping path:

## `GAME/INSTALL/README.md`

Final content must preserve simultaneously:

- RD-01 accepted ordinary Project-capable ChatGPT / transport projection and no persisted model/plan identity;
- RD-14 campaign selection/New Game/resume/bootstrap product entry behavior;
- no stale path resurrection or v0.8 compatibility fiction.

## `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`

Final content must preserve simultaneously:

- RD-01 fixed Connector/no-probe/no-fallback transport instructions and current v1 routing constraints;
- RD-14 explicit selection/bootstrap/product flow and exact package/campaign identity handling;
- no shorter alternate bootstrap path that bypasses current selection/currentness/creator checks.

## `GAME/INSTALL/00_DND_BOOTSTRAP.md`

RD-14 remains the final structural replacement owner, but the result must satisfy every applicable RD-01 shipped-projection assertion. Replacement does not erase RD-01's accepted transport/currentness requirements.

No file may be accepted by taking one RD's complete version and then replaying the other RD's stale pre-integration version.

---

# 4. TDD / proof requirements

RD-14 final install/bootstrap integration must run both focused suites:

```text
python3 -m unittest DEV.TESTS.test_rd01_shipped_projection_repairs.InstallProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap -v
```

and the final package verification required by checkpoint law.

Add an exact cross-RD witness conceptually:

```text
InstallBootstrapSharedWriterTests
```

Required cases:

1. final `README.md` satisfies RD-01 transport/current-product projection and RD-14 selection/bootstrap semantics together;
2. final `PROJECT_INSTRUCTIONS.txt` contains no stale transport fallback and no bootstrap/currentness bypass;
3. final `00_DND_BOOTSTRAP.md` replacement preserves every applicable RD-01 accepted invariant;
4. reversing the stale writer order cannot silently remove the other RD's requirement set because final integration always rereads current bytes;
5. no removed `GAME/AGENTS.md` or `GAME/CORE/START.md` path is recreated;
6. install docs remain non-authoritative projections and point to current runtime owners.

A single-RD focused test suite is insufficient to close the shared-writer checkpoint.

---

# 5. Execution graph amendment

Add to Tier D shared shipped-consumer checkpoints:

```text
RD01_INSTALL_PROJECTION_LOCAL_READY
  CONSTRAINS_WITHOUT_ORDERING RD14 owner-local bootstrap work

RD01_INSTALL_PROJECTION_LOCAL_READY
+ RD14 final bootstrap/product semantics ready
  SHARED_FILE_CHECKPOINT
RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION
```

RD-14 final product closure may not claim shipped install/bootstrap readiness before this checkpoint.

This does not require all of RD-01 to precede all of RD-14. Only the physical shared-file integration checkpoint is ordered.

---

# 6. Non-goals

This repair does not:

- make install docs semantic authority;
- serialize unrelated RD-01/RD-14 tasks;
- reopen WP-19 or WP-26 architecture;
- introduce a generated documentation system;
- preserve obsolete v0.8 paths;
- authorize production implementation.

---

## Disposition

```text
AUTHOR_GRAPH_FINDING_39: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
