# Implementation Planning — Lossless Proof Ledger

Status: **AUTHOR REPAIR / SIP-009 CONTROL ARTIFACT — EXECUTION NOT AUTHORIZED**
Date: 2026-09-13

Purpose: prevent readiness or composite closure from being credited by identity counting, schema existence, static audit or a broad test-suite pass when the owning source requires item-level behavioral/integration evidence.

Canonical inputs are WP-27 final readiness + Step-2 evidence ledger and the exact owner suites referenced by those records. This ledger does not create requirements or activate future-trigger leaves.

Owner-suite appendices:
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13.md`
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp14-wp15.md`
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md`

## Proof channel law

Every current proof obligation is assigned exactly one primary channel and may have supporting channels:

```text
FOCUSED_BEHAVIOR      deterministic owner-local behavior
INTEGRATION_SCENARIO  cross-owner/cross-RD behavior
STATIC_AUDIT          stale path/schema/doc/catalog/projection proof only
HOSTED_CI             exact published-head repository validation only
EMPIRICAL_DEFERRED    real-host/workload evidence whose trigger is not active
```

Rules:
- schema/static evidence cannot discharge behavior or integration;
- source CI cannot substitute for exact-head hosted CI;
- hosted CI cannot establish semantic behavior not exercised by tests;
- `EMPIRICAL_DEFERRED` preserves a future trigger and is not current missing implementation work;
- `NOT_APPLICABLE` is legal only with a cited current owner reason;
- a proof leaf closes only when every current row underneath it has a named executable witness and later passes after implementation.

Package integration proof file planned by this ledger:

```text
DEV/TESTS/test_implementation_proof_ledger.py
```

Its classes are package-level witnesses over implemented RD interfaces; they do not duplicate owner logic.

## Pure-proof readiness routing

| Readiness | Exact current proof responsibility | Planned witness | Channel | Status |
|---|---|---|---|---|
| R023 | Stage-3 deterministic invariants plus path-routing and legacy-schema regressions | `Stage3PackageProofTests` | INTEGRATION_SCENARIO + STATIC_AUDIT | CURRENT_PLANNED |
| R031 | provisional Actor state, READY_PC, lazy derivation, no retrofit | `ActorReadinessProofTests` over RD-03 + RD-14 | INTEGRATION_SCENARIO | CURRENT_PLANNED |
| R032 | reconstructable rules/build + initial commitment/domain behavior; no eager universal sheet | `DomainCommitmentProofTests` over RD-03/RD-14 | INTEGRATION_SCENARIO | CURRENT_PLANNED |
| R032 | measured real-target performance/coverage | future target measurement | EMPIRICAL_DEFERRED | TRIGGER_NOT_ACTIVE |
| R041 | deterministic retry/RNG/no-replay incl stale continuation and child crash boundary | `ExecutionRetryProofTests` over RD-05/RD-07/RD-08 | INTEGRATION_SCENARIO | CURRENT_PLANNED |
| R058 | containment, source escalation, rebind, safe emission, finite UNSATISFIABLE degradation | `RoleContainmentProofTests` over RD-10/RD-11 | INTEGRATION_SCENARIO | CURRENT_PLANNED |
| R058 | later empirical protocol/MVP assurance where owner trigger requires | future empirical run | EMPIRICAL_DEFERRED | TRIGGER_NOT_ACTIVE |
| R061 | bounded discovery, no broad scan, lawful degradation, typed context bounds and authority separation | `ContextBoundednessProofTests` over RD-11 | INTEGRATION_SCENARIO | CURRENT_PLANNED |
| R061 | supported-target context empirical evaluation | future empirical run | EMPIRICAL_DEFERRED | TRIGGER_NOT_ACTIVE |
| R068 | all 17 WP-12 §14 themes | `Wp12HotProofTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO | SEE_WP12_WP13_APPENDIX |
| R088 | owner-first positive/negative/failure/indeterminate proof and reverse reconciliation | `OwnerFirstReconciliationProofTests` | INTEGRATION_SCENARIO + STATIC_AUDIT | CURRENT_PLANNED |
| R089 | channel limits: static/scenario/empirical/exact-head CI remain distinct | `ProofChannelDisciplineTests` + exact-head CI evidence | STATIC_AUDIT + HOSTED_CI | CURRENT_PLANNED |

## Direct readiness with enumerated proof suites

These direct leaves cannot be closed merely because their owning RD functional tests pass generally:

| Readiness | Exact suite | Package witness | Item ledger |
|---|---|---|---|
| R071 | WP-13 §15 items 1–38 | `Wp13DurabilityProofTests` | WP-12/WP-13 appendix |
| R074 | WP-14 §15 items 13–25 | `Wp14RecoveryProofTests` | WP-14/WP-15 appendix |
| R077 | WP-15 §13 items 9–17 | `Wp15TemporalProofTests` | WP-14/WP-15 appendix |
| R080 | WP-16 §15 items 1–21 current machine/scenario + item 22 measured-target empirical branch | `Wp16LiveAccessProofTests` | WP-16/WP-17 appendix |
| R083 | WP-17 §28 26 explicit verification themes | `Wp17CollaborationProofTests` | WP-16/WP-17 appendix |
| R099 | qualifying sparse T0 capture/rejection/lookup/zero-extra-serial | `T0HistoricalBasisProofTests` | this control ledger + RD-13 named cases |
| R102 | Story-local T0 + self-contained Commentator control/filter/currentness separation | `CommentatorSelfContainedProofTests` | this control ledger + RD-13 named cases |

R099 current deterministic rows must prove retained T0 remains explainable after T1 mutation, invalid/current-pointer/hidden-reasoning capture rejection, bounded lookup and zero-extra-serial design. Real-target critical-path observation remains `EMPIRICAL_DEFERRED` until its trigger.

R102 current rows must prove no native fallback for retained qualifying T0, deterministic pre-LLM exclusion of protected cached material, locally decidable eligibility, content-final/control-refresh independence and no second ACL/history authority.

## Composite-parent package proof

Composite parent closure requires all named slices plus a parent integration witness; sibling slice PASS labels alone are insufficient.

| Parent | Required slice join | Planned parent witness |
|---|---|---|
| R006 | RD-02 INFO + RD-03 ACTOR + RD-08 THREAD_VISIBILITY | `CompositeR006ProofTests` |
| R016 | INFO + ACTOR + EXECUTION + TEMPORAL + LIVE + COLLAB + STORY | `CompositeR016ProofTests` |
| R018 | INFO + ACTOR + ROUTE/ROOT + EXECUTION + TEMPORAL + LIVE + COLLAB + STORY | `CompositeR018ProofTests` |
| R029 | RD-03 provisional Actor + RD-06 DURABILITY + RD-14 ONBOARDING | `CompositeR029ProofTests` |
| R053 | RD-02 INFO + RD-09 LIVE normalization producer/currentness | `CompositeR053ProofTests` |
| R062 | RD-02 information/history inputs + RD-03 Actor continuity/effect application + RD-05 runtime lifecycle evidence + RD-08 TemporalBinding + RD-13 SemanticEvent history | `CompositeR062ProofTests` |
| R087 | RD-11 retrospective + RD-13 SemanticEvent/T0 + RD-14 save/session/menu | `CompositeR087ProofTests` |
| R122 | RD-08 chronology + RD-09 currentness/scene + RD-11 context + RD-12 collaboration bridge | `CompositeR122ProofTests` |

Each parent witness must include negative authority-transfer assertions and must consume the current native owner interfaces, not mocked replacement authority.

## Version Impact reconciliation

Every RD records local Version Impact evidence. Package closure additionally runs one parent-level reconciliation across all eight composite parents:

```text
CompositeVersionImpactProofTests
```

It verifies that schema/catalog/API/checkpoint/version impacts introduced by sibling slices are mutually compatible, no parent is closed across incompatible contract generations, and `NONE` is used only when supported by the actual implemented delta. This is proof/reconciliation, not a new version owner.

## Completion rule

SIP-009 is author-repaired only when:
1. this control ledger and all three named owner-suite appendices are routed from the package index;
2. every owner-suite item has a named package test/scenario and supporting RD target;
3. composite parent witnesses and package Version Impact reconciliation are present;
4. future empirical/release triggers remain dormant rather than being counted as current failures;
5. the final author bidirectional/currentness gate rechecks the ledger against current plans.

No row in this planning document claims runtime PASS. Production implementation remains forbidden pending independent Senior GO.