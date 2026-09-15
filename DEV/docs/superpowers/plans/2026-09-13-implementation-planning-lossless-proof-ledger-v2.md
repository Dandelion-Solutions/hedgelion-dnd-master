# Implementation Planning — Lossless Proof Ledger v2

Status: **CURRENT AUTHOR-REPAIRED CONTROL LEDGER — EXECUTION NOT AUTHORIZED**
Date: 2026-09-13
Supersedes for current routing: `2026-09-13-implementation-planning-lossless-proof-ledger.md`.

Purpose: preserve readiness proof semantics losslessly after SIRR-001 repair. This ledger creates no readiness identity, runtime subsystem or semantic owner.

## 1. Current appendices

Current owner-suite routes are:
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md` — **current repaired WP-12/WP-13 route**;
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp14-wp15.md` — unchanged current route;
- `2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md` — unchanged current route.

The old WP-12/WP-13 appendix is historical provenance only and must not be used by a worker or reviewer as the current proof route.

Planned package witness target remains:
```text
DEV/TESTS/test_implementation_proof_ledger.py
```

## 2. Proof channel law

Every current proof obligation has a primary channel:
```text
FOCUSED_BEHAVIOR
INTEGRATION_SCENARIO
STATIC_AUDIT
HOSTED_CI
EMPIRICAL_DEFERRED
```

Rules:
- static/schema existence cannot discharge behavior or integration;
- hosted CI proves exact published-head repository validation, not unexercised semantics;
- source/local PASS cannot substitute for required hosted CI;
- `EMPIRICAL_DEFERRED` preserves a future trigger and is not current missing implementation work;
- `NOT_APPLICABLE` requires exact current owner reason and evidence;
- a readiness leaf closes only when every current subordinate row has a named executable witness and later passes after authorized implementation.

## 3. Pure-proof readiness routing

| Readiness | Exact current proof responsibility | Planned witness | Channel |
|---|---|---|---|
| R023 | Stage-3 deterministic invariants, path-routing and legacy-schema regressions | `Stage3PackageProofTests` | INTEGRATION_SCENARIO + STATIC_AUDIT |
| R031 | provisional Actor state, READY_PC, lazy derivation, no retrofit | `ActorReadinessProofTests` over RD-03 + RD-14 | INTEGRATION_SCENARIO |
| R032 | reconstructable rules/build + initial commitment/domain behavior; no eager universal sheet | `DomainCommitmentProofTests` over RD-03 + RD-14 | INTEGRATION_SCENARIO |
| R032 empirical branch | real-target performance/coverage | future target measurement | EMPIRICAL_DEFERRED |
| R041 | deterministic retry/RNG/no replay incl. stale continuation and child crash boundary | `ExecutionRetryProofTests` over RD-05/RD-07/RD-08; F62/PG37 additionally binds actual accepted adjudication/source/publication/cold-recovery witnesses under mandatory overlay39 | INTEGRATION_SCENARIO |
| R058 | containment/source escalation/rebind/safe emission/finite UNSATISFIABLE degradation | `RoleContainmentProofTests` over RD-10/RD-11 | INTEGRATION_SCENARIO |
| R058 empirical branch | later protocol/MVP assurance when owner trigger activates | future empirical run | EMPIRICAL_DEFERRED |
| R061 | bounded discovery/no broad scan/lawful degradation/typed context bounds/authority separation | `ContextBoundednessProofTests` over RD-11 | INTEGRATION_SCENARIO |
| R061 empirical branch | supported-target context evaluation | future empirical run | EMPIRICAL_DEFERRED |
| R068 | all exact WP-12 §14 duties | `Wp12HotProofTests` | current WP-12/WP-13 v2 appendix |
| R088 | owner-first positive/negative/failure/indeterminate proof + reverse reconciliation | `OwnerFirstReconciliationProofTests` | INTEGRATION_SCENARIO + STATIC_AUDIT |
| R089 | proof-channel separation + exact-head hosted evidence | `ProofChannelDisciplineTests` + exact-head CI evidence | STATIC_AUDIT + HOSTED_CI |

F62/PG37 later-precedence amendment: R041 retains every original retry/RNG/child-crash duty and consumes the four exact task-owned witnesses in `2026-09-15-implementation-planning-accepted-adjudication-basis-addendum.md` for policy-basis-sensitive accepted inputs. A schema-valid JSON round-trip or conformance hash is not production source resolution, accepted RuntimeCommand identity or cold recovery. No new readiness identity is created.

## 4. Direct readiness with enumerated owner suites

| Readiness | Exact suite | Package witness | Current route |
|---|---|---|---|
| R071 | WP-13 §15 exact 38 duties | `Wp13DurabilityProofTests` | WP-12/WP-13 **v2** appendix |
| R074 | WP-14 §15 items 13..25 | `Wp14RecoveryProofTests` | WP-14/WP-15 appendix |
| R077 | WP-15 §13 items 9..17 | `Wp15TemporalProofTests` | WP-14/WP-15 appendix |
| R080 | WP-16 §15 items 1..21 current + item 22 empirical branch | `Wp16LiveAccessProofTests` | WP-16/WP-17 appendix |
| R083 | WP-17 §28 exact 26 themes | `Wp17CollaborationProofTests` | WP-16/WP-17 appendix |
| R099 | sparse qualifying T0 capture/rejection/lookup/zero-extra-serial | `T0HistoricalBasisProofTests` | RD-13 + this control ledger |
| R102 | Story-local T0 + self-contained Commentator control/filter/currentness separation | `CommentatorSelfContainedProofTests` | RD-13 + this control ledger |

R099 current deterministic proof must include retained T0 explainability after later mutation, invalid/current-pointer/hidden-reasoning capture rejection, bounded lookup and zero-extra-serial design. Real-target critical-path observation remains dormant empirical work until trigger.

R102 current proof must include no native fallback for retained qualifying T0, deterministic pre-LLM exclusion of protected cached material, locally decidable eligibility, content-final/control-refresh independence and no second ACL/history authority.

## 5. Composite-parent package proof

Composite parent closure requires every named slice plus a package integration witness. Slice PASS labels alone cannot close the parent.

| Parent | Required slice join | Planned witness |
|---|---|---|
| R006 | RD-02 INFO + RD-03 ACTOR + RD-08 THREAD_VISIBILITY | `CompositeR006ProofTests` |
| R016 | RD-02 INFO + RD-03 ACTOR + RD-05 EXECUTION + RD-08 TEMPORAL + RD-09 LIVE + RD-12 COLLAB + RD-13 STORY | `CompositeR016ProofTests` |
| R018 | RD-02 INFO + RD-03 ACTOR + RD-04 ROUTE/ROOT + RD-05 EXECUTION + RD-08 TEMPORAL + RD-09 LIVE + RD-12 COLLAB + RD-13 STORY | `CompositeR018ProofTests` |
| R029 | RD-03 ACTOR + RD-06 DURABILITY + RD-14 ONBOARDING | `CompositeR029ProofTests` |
| R053 | RD-02 INFO + RD-09 LIVE normalization/currentness | `CompositeR053ProofTests` |
| R062 | RD-02 Knowledge/Disclosure/Message + RD-03 Actor continuity/Effect + RD-05 lifecycle evidence + RD-08 TemporalBinding + RD-13 SemanticEvent history | `CompositeR062ProofTests` |
| R087 | RD-11 retrospective + RD-13 SemanticEvent/T0 + RD-14 save/session/menu | `CompositeR087ProofTests` |
| R122 | RD-08 chronology + RD-09 currentness/scene + RD-11 context + RD-12 collaboration bridge | `CompositeR122ProofTests` |

Each composite witness includes negative authority-transfer assertions and consumes current native owner interfaces, not mocked substitute authority.

SIRR repair consequences:
- R016/R018 Story slice cannot close until `MANIFEST.storage.story_root` exists and generated-scaffold preservation is proven;
- R029 durability slice consumes repaired native-domain SAVE composition;
- R053 must preserve close vs CLOSED_UNABSORBED absorption semantics from the RD-02/RD-09 amendment.

## 6. Parent Version Impact reconciliation

Package closure still runs:
```text
CompositeVersionImpactProofTests
```

It proves sibling schema/catalog/API/checkpoint/version effects are compatible, no parent crosses incompatible generations and `NONE` is used only when supported by the actual implemented delta. This is proof only, not a version owner.

The repaired Story selector and future CORE consumer edits are therefore classified from their actual worker deltas before any composite parent closes.

## 7. SIRR-001 exactness gate

A reviewer/worker must validate semantic identity, not row count:
- WP-12 v2 appendix has exactly 17 rows and each corresponds one-to-one to WP-12 §14 duty 1..17;
- WP-13 v2 appendix has exactly 38 rows and each corresponds one-to-one to WP-13 §15 duty 1..38;
- each row has a supporting target, named witness and primary channel;
- storage baseline remains a distinct authority from HOT/campaign SAVE;
- LIVE exact-source CAS remains a distinct establishment boundary from campaign publication;
- journal/global-frontier alternatives remain negative laws;
- row 38 carries explicit shipped-consumer and stale-test disposition rather than an aggregate stale-search claim.

Any semantic mismatch, missing row or duplicate substitution is RED even if totals remain 17/38.

## 8. Completion rule

Current lossless proof routing is complete for planning only when:
1. this v2 control ledger is routed by the current package index;
2. the WP-12/WP-13 v2 appendix is the only current route for R068/R071;
3. unchanged WP-14/15 and WP-16/17 appendices remain routed;
4. all eight composite witnesses and parent Version Impact witness remain planned;
5. future empirical/release triggers remain dormant;
6. repaired bidirectional/currentness closure rechecks these routes;
7. genuinely independent Senior re-review recomputes semantic coverage and returns PASS / GO.

No row in this planning ledger claims runtime PASS. Production implementation remains forbidden.

## 9. Planning Version Impact

Planning-only proof-route repair. Version Impact: **NONE**.
