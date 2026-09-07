# R2.7 WP-22 Step 4 — Cross-System Collaborative Review

Status: **STEP 4 COMPLETE — CROSS-SYSTEM RECONCILIATION PASSED**

Date: 2026-09-07

Inputs:

- WP-22 Step-1 Task Brief / Source Manifest;
- WP-22 Step-1 whole-project critic;
- independent Senior Step-1 re-review: **GO**;
- Step-2 Verification Coverage Matrix;
- Step-3 Decision Brief.

Scope is verification architecture only. No implementation or WP-23 activation is authorized by this review.

---

## 1. Review question

Does the owner-first layered verification recommendation compose with current HDM authority, runtime, storage, persistence, chronology, multiplayer, Story/Dramaturg, bootstrap/update, maintenance, versioning and assurance architecture without reopening accepted semantics or manufacturing new work from dormant/deferred obligations?

---

## 2. Cross-system review ledger

### CR22-01 — Test authority inversion

**Risk:** existing tests could become de facto architecture authority, especially where older machine contracts use vocabulary that later architecture refined.

**Review:** Step 2 maps every executable/scenario/audit artifact back to a current semantic owner. Tests are verification consumers only.

**Disposition:** **RESOLVED / CONFORMS**.

**Constraint retained:** when a test conflicts with a newer accepted owner, repair/retire the test; do not weaken architecture to preserve it.

---

### CR22-02 — Architecture obligation mistaken for current implementation defect

**Risk:** WP-08…WP-21 contain many implementation-facing laws. A naive matrix could mark them red merely because runtime code/tests do not yet exist.

**Review:** each such family carries an explicit realization state. Unrealized targets are `DEFERRED_UNTIL_REALIZATION` when their owners defer implementation.

**Disposition:** **RESOLVED / CONFORMS**.

**Constraint retained:** `VERIFICATION_GAP` is reserved for a realized material target lacking sufficient current proof.

---

### CR22-03 — Partial realization overclaim

**Risk:** a current narrow test could be credited as proof of the whole subsystem.

Examples:

- publication ref-fence algebra vs full publisher;
- WP-18 `planning_entry_classes` provenance vs retained planning runtime;
- engine-update policy text vs updater/migrator behavior;
- bootstrap local generation smoke vs remote campaign publication/activation.

**Review:** Step 2 uses `PARTIAL_CURRENT` and splits current proof from deferred end-to-end behavior.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-04 — Green CI completeness fallacy

**Risk:** hosted audit + unittest success could be presented as proof that the verification matrix is complete or that Protocol 4 passed.

**Review:** CI route is explicitly limited to admitted current audit/unit checks. Scenario catalogs and Protocol 4 are not executed by file presence.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-05 — Protocol 4 sequencing

**Risk:** execute Protocol 4 before implementation or create a surrogate MVP so that an architecture checkpoint can claim empirical success.

**Review:** Step 2 preserves current Protocol-4 design and frozen fixture as scenario acceptance sources only. Execution is explicitly deferred to the real implemented MVP.

**Disposition:** **RESOLVED / CONFORMS**.

Required sequence remains:

```text
R2.6 architecture assurance
-> R2.7 machine/instruction/test mapping
-> implementation planning
-> MVP implementation via TDD
-> production-like evaluation on the real MVP
```

---

### CR22-06 — PO-005 creator-login continuity omitted by older access scenarios

**Risk:** `ACCESS_CONTROL_CASES.md` covers repository-permission separation and owner/player boundaries but does not itself encode the later explicit creator-login-rename/no-stable-ID-substitution decision.

**Review:** PO-005 remains the semantic owner. Full creator authorization runtime is not yet realized, so absence of executable enforcement is not a present implementation defect. However, the later implementation verification plan must include the PO-005 cases explicitly.

**Disposition:** **RESOLVED AS EXPLICIT FUTURE OBLIGATION**.

Mandatory future cases:

- stored/current creator login mismatch after rename -> fail closed/read-only;
- no stable-ID substitution;
- repository Admin/Write/collaborator status cannot recover creator authority;
- no silent ownership transfer.

No new Product Owner decision is required.

---

### CR22-07 — PO-006 branch/ref cleanup regression

**Risk:** cleanup/maintenance verification could reintroduce physical branch/ref deletion, probing or fallback merely as a test setup/cleanup technique.

**Review:** PO-006 is absolute and already has executable negative guards. WP-22 retains logical retirement only.

**Disposition:** **RESOLVED / CONFORMS**.

No branch/ref deletion test, probe, retry, native-git fallback or capability discovery is permitted.

---

### CR22-08 — Chronology and collaboration indeterminate states lost in happy-path tests

**Risk:** later TDD could encode only binary success/failure and erase `INDETERMINATE`, stale-generation, unresolved-currentness or partial-order semantics.

**Review:** Step 2 has a separate item-level negative/failure/indeterminate inventory and preserves these cases independently of positive law-family aggregation.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-09 — Open-ended player/GM behavior over-formalized for test convenience

**Risk:** verification completeness pressure could force ordinary novel player actions, GM improvisation, tone or dramaturgic quality into a closed deterministic vocabulary.

**Review:** open-ended semantic/product-quality judgments remain `NOT_MACHINE_CHECKABLE` or bounded scenario/empirical acceptance where appropriate. Only authority/failure/containment/mechanics boundaries are formalized.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-10 — Story/Dramaturg verification creates new authority

**Risk:** a fixture, scoring rubric, planning catalog or Story test could become future-intent/canon authority.

**Review:** Story remains retrospective non-authoritative projection; planning remains provisional/noncanonical; fixtures are acceptance evidence only. Current WP-18 provenance test protects vocabulary synchronization without granting semantic authority.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-11 — Historical/TODO artifacts activate dormant work

**Risk:** old TODO/performance/live-branch notes could be mistaken for current requirements or triggers.

**Review:** Step 2 classifies them as historical/supporting. Revisit triggers remain with current owners (for example measured R2.3/WP-11 scale evidence), not with TODO file existence.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-12 — Release-tool tests accidentally activate WP-23

**Risk:** because release tests are already executable, WP-22 could claim release readiness or begin WP-23.

**Review:** release tests are current tooling/source-boundary verification consumers only. Release-readiness synthesis remains WP-23 and is explicitly out of scope.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-13 — Static audit overclaims runtime behavior

**Risk:** maintenance audit source/schema/catalog checks could be presented as proof of authorization, concurrency, LLM containment or publication semantics.

**Review:** the proof taxonomy limits static audit to structural/source invariants. Runtime/behavioral claims require executable/scenario/empirical routes as applicable.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-14 — Empirical evaluation overrules deterministic architecture

**Risk:** a model/host evaluation result could be treated as permission to weaken owner law because the observed output “looks fine”.

**Review:** empirical evaluation measures conformance of a realized system to accepted owners. It does not grant semantic precedence over deterministic authority, eligibility, currentness or failure law.

**Disposition:** **RESOLVED / CONFORMS**.

---

### CR22-15 — Coverage becomes activation

**Risk:** naming a deferred row in a “complete” matrix could be interpreted as authorization to implement it now.

**Review:** realization/defer state is mandatory for every row and safe triggers are explicit.

**Disposition:** **RESOLVED / CONFORMS**.

---

## 3. Cross-system consistency result

The owner-first layered model composes with current architecture without changing product semantics.

It preserves the following important boundaries:

```text
semantic authority != verification artifact
architecture coverage != machine realization
machine realization != verification realization
verification realization != empirical acceptance
green CI != verification completeness
coverage != activation
deferred obligation != current defect
scenario design != execution result
research provenance != semantic owner
```

No accepted architecture was reopened merely because an old test/scenario overlapped it.

---

## 4. Review findings

```text
BLOCKING: 0
SIGNIFICANT_UNRESOLVED: 0
SIGNIFICANT_RESOLVED_IN_REVIEW: 4
MINOR/CLARIFYING_RESOLVED: 11
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
```

The material resolved issues are:

1. partial-realization overclaim;
2. PO-005 exact future denial cases absent from older scenario catalog;
3. stale/historical verification surfaces accidentally becoming authority;
4. release/static/CI proof scopes accidentally expanding beyond what they actually establish.

All are addressed by the Step-2 matrix plus candidate-spec requirements; none requires changing current engine/gameplay architecture.

---

## 5. Step-4 exit

Step 5 may produce the candidate verification specification using Alternative C, provided it retains:

- the exact proof-state vocabulary;
- owner-first / bidirectional reconciliation;
- item-level negative/fail-closed/failure/indeterminate preservation;
- Protocol-4 deferred execution;
- PO-005 and PO-006 future/current negative obligations;
- explicit partial-realization handling;
- no WP-23 activation.
