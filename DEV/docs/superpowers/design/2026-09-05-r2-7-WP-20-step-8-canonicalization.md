# R2.7 WP-20 Step 8 — Canonicalization

Status: **STEP 8 COMPLETE — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-05

Domain: **Engine update / schema evolution / migration**

This record completes the worker-owned Steps 2–8 architecture loop after the mandatory Step-1 Senior GO. It is the exact stop point required by the HDM architecture process.

No WP-21 work, implementation planning, substantive implementation, storage migration or real campaign migration is authorized by this record.

---

## 1. Final selected architecture

WP-20 selects:

> **Immutable exact-target package-scoped compatibility evidence plus an explicit directed migration-edge graph, composed with the existing creator/storage/LIVE/recovery/CAS owners.**

The final implementation-facing review checkpoint is:

- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`.

The architecture does not introduce a mutable global migration registry, global lock, universal compatibility generation or migration-specific publication authority.

---

## 2. Final Step-6/7 disposition

Step 6 found:

```text
BLOCKING: 0
SIGNIFICANT: 6
MINOR: 2
```

Step 7 closed every finding:

```text
F20-01 CLOSED — migration-path ambiguity
F20-02 CLOSED — storage/campaign authority collapse
F20-03 CLOSED — same-version Git ancestry used as released compatibility proof
F20-04 CLOSED — CLOSED LIVE pending absorption
F20-05 CLOSED — accepted resumable-work compatibility gap
F20-06 CLOSED — migration evidence/publication authority and circular identity
F20-07 CLOSED — branch-derived versus local HOT rebuild timing
F20-08 CLOSED — pre-release implication in legacy-layout test wording
```

No material redesign followed the repairs, so a second Step-6 cycle was not required.

---

## 3. Mandatory finding-propagation sweep

For every `SIGNIFICANT` finding, Step 7 identified the affected historical/current surfaces and the current final owner.

This Step-8 checkpoint synchronizes:

- final WP-20 implementation-facing specification;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/MIGRATIONS/README.md`;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md`;
- `DEV/CURRENT_PROGRESS.md`.

Historical 2026-08-18 update/provenance artifacts remain historical rather than being rewritten. Their retained principles and superseded released-v1+ ancestry inference are explicitly accounted for by the final spec and Step-7 record.

```text
FINDING_PROPAGATION_SWEEP: COMPLETE
ONE_CURRENT_FINAL_OWNER_FOR_CHANGED_WP20_LAW: YES
```

---

## 4. Canonicalization self-review

### 4.1 Scope / product boundary

- [x] compatibility horizon begins at released v1.0+;
- [x] no v0.8/pre-release compatibility or migration machinery restored;
- [x] no future all-versions support promise invented;
- [x] no implementation planning or real migration started;
- [x] WP-21 not started.

### 4.2 Versioning / identity

- [x] accepted versioning taxonomy is unchanged;
- [x] no equality/order/Git ancestry is used as compatibility proof;
- [x] exact immutable target artifact identity is separated from semantic compatibility;
- [x] unsupported newer state fails closed.

### 4.3 Authority / ownership

- [x] creator owns existing-campaign migration/adoption;
- [x] storage owner owns storage-default/storage-format evolution;
- [x] storage and campaign transactions remain separate success domains;
- [x] no repository permission/PLAYER role accidentally grants migration authority;
- [x] current `ACCESS_CONTROL.md` wording is synchronized.

### 4.4 Currentness / failure

- [x] migration starts from pinned current source basis;
- [x] active LIVE and CLOSED-unabsorbed LIVE both block migration;
- [x] accepted resumable work remains frozen/interpretation-compatible;
- [x] ref movement invalidates prepared work;
- [x] prepared transform/validation is not durable success;
- [x] publication uses existing one-commit/non-force campaign-ref CAS;
- [x] ambiguous transport uses bounded read-back;
- [x] no blind retry/force/ref-rewind rollback.

### 4.5 Data / schemas / projections

- [x] local schema versions remain owner-local;
- [x] campaign/storage generations remain separate axes;
- [x] only declared authoritative native scope is transformed;
- [x] stable identities/history/owner direction are preserved;
- [x] branch-persistent rebuildable projections are distinguished from local HOT caches;
- [x] no projection/index becomes migration authority.

### 4.6 Migration graph

- [x] edges are immutable exact-target package support data;
- [x] direction is explicit;
- [x] multiple valid paths require exact target canonical order or become indeterminate;
- [x] reverse/downgrade is a separate explicit edge/new forward transaction;
- [x] no mutable central registry/service/graph database is required.

### 4.7 Provenance

- [x] migration evidence is bounded evidence, not publication authority;
- [x] no circular requirement for a record to self-embed its final containing commit hash;
- [x] resulting campaign ref/commit remains authoritative publication identity.

### 4.8 Evidence / traceability

- [x] task-specific Source Manifest was refined through actual owners;
- [x] Product Owner PO-004 and clean-slate decision were incorporated;
- [x] versioning/current realization were reconciled without reopening;
- [x] WP-10/11/12 native/physical/projection distinctions were accounted for;
- [x] WP-13/14 publication/recovery outcomes were accounted for;
- [x] WP-15 chronology/history preservation was accounted for;
- [x] WP-16 LIVE/currentness was accounted for;
- [x] WP-19 creation/storage-baseline boundary was accounted for;
- [x] ruleset/package/schema/update/migration runtime surfaces were inspected;
- [x] Step-6 critic reconstructed direct and indirect routes rather than reviewing only the candidate;
- [x] no final coverage claim depends solely on roadmap/index/search snippets or remembered context.

### 4.9 Status / navigation

- [x] `DEV/CURRENT_PROGRESS.md` moves global cursor to Step-8 complete / mandatory Senior review pending;
- [x] roadmap unchanged because sequence/scope/dependencies did not change;
- [x] project map unchanged because its routing remains correct;
- [x] root README unchanged;
- [x] Product Owner ledger verbatim intent unchanged;
- [x] no new branch created.

---

## 5. Source / authority disposition

### Current final WP-20 law

- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`.

### Current supporting owners synchronized

- `DEV/ARCHITECTURE/ACCESS_CONTROL.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/MIGRATIONS/README.md`;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md`.

### Upstream law retained

- v1.0 clean-slate owner decision;
- versioning namespace/compatibility policy;
- versioning realization status amendment;
- WP-10…19 accepted owners according to their native scopes.

### Historical/superseded applicability

2026-08-18 update/provenance documents remain historical design provenance. For released v1.0+ only, same-version Git-descendant ancestry no longer grants compatibility/silent-use authority. Exact package provenance, storage/campaign baseline separation and creator adoption ownership survive where not otherwise superseded.

---

## 6. Deferred realization boundary

The following are explicitly not performed in WP-20 Steps 2–8:

```text
migration-edge machine schema/catalog
migration transform code/interpreter
runtime compatibility evaluator implementation
release-builder migration validation
executable migration implementation/tests
implementation plan
real storage migration
real campaign migration
WP-21
```

These remain later implementation consumers after complete R2.7 architecture and required planning/review gates.

---

## 7. Human / PO gate

No Step-2…8 evidence exposed a genuine unresolved product semantic, architecture ownership trade-off, compatibility-horizon decision or material risk acceptance requiring Product Owner judgment.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
VERSIONING_TAXONOMY_REOPENED: NO
```

---

## 8. Publication and verification gate

This Step-8 package must be published as one coherent non-force checkpoint from a freshly verified `v1/engine-rearchitecture` parent and then read back through the GitHub Connector.

The artifact intentionally does not self-embed its containing commit SHA. Final handoff/Senior review uses the actual remote ref/commit returned and independently read back after publication.

Hosted CI/status is additional evidence when a run/status is available. An unavailable or still-pending hosted-CI result must be reported accurately and must not be represented as PASS.

---

## 9. Exact next gate

After coherent publication/read-back, stop.

```text
WP20_STEP8_COMPLETE: YES
WP20_FINAL_SENIOR_REVIEW: REQUIRED / PENDING
NEXT_AUTHORIZED_UNIT: NONE UNTIL SENIOR PASS/GO
WP21_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
REAL_MIGRATION_EXECUTED: NO
```
