# R2.7 WP-22 Step 1 — Whole-Project Task-Brief Critic

Status: **STEP-1 CRITIC COMPLETE — MECHANICAL REPAIRS APPLIED / MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-07

Domain: **Verification / test / evaluation completeness**

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-task-brief-source-manifest.md`.

Review stance:

> Assume the Step-1 brief can still overclaim completeness, mistake test presence for proof, preserve superseded semantics, turn deferred evaluations into fake implementation, or omit a verification consumer. Reconstruct the verification dependency graph independently and find concrete failure mechanisms before Step 2 is authorized.

This critic does not authorize Step 2 or implementation.

---

## 1. Independently reconstructed verification routes

### 1.1 Architecture-law -> realization -> verification route

```text
current accepted semantic owner
-> current machine/runtime realization or explicit deferred realization
-> appropriate proof class
-> exact verification artifact
-> actual execution/review route
```

The critic checked that a test filename or passing workflow is not accepted as a substitute for the first two links.

### 1.2 Machine/runtime -> owner route

```text
GAME/CORE / GAME/SCHEMA / catalogs / tools / templates
-> exact current owner
-> current verification or explicit gap/defer
```

This detects tests that still encode a superseded machine assumption even when the current runtime text has changed.

### 1.3 CI/audit route

```text
.github/workflows/validate.yml
-> run_maintenance_audit.py
-> audit_engine.py

and

.github/workflows/validate.yml
-> unittest discover -s DEV/TESTS -v
```

The critic inspected what these routes really execute rather than treating “CI green” as a whole-project proof statement.

### 1.4 Scenario/evaluation route

```text
*_CASES.md / TODO / historical audit artifacts
+ role-context empirical protocols/research
-> applicability classification
-> architecture-stage evidence OR future post-implementation evaluation
```

The critic checked that scenarios, historical snapshots, future TODOs and empirical measurements remain distinct.

### 1.5 Negative-law route

Representative high-risk current negative/fail-closed owners were traced to regressions where available:

- branch/ref deletion prohibition;
- logical ref retirement;
- non-force publication/currentness;
- version namespace fail-closed census;
- one global current-progress authority;
- PO routing to closed WPs;
- released-v1+ compatibility not inferred from ancestry/version order.

Representative success does not establish completeness; the Step-2 negative-law inventory remains mandatory.

---

## 2. Findings

### F22-S1-01 — BLOCKER — No law-to-verification completeness proof structure

**Mechanism**

The repository contains many executable tests, static audits and scenario catalogs, but no current whole-project structure proving which important accepted law owns which verification, whether the target behavior is already realized, whether the proof is current, and what is safely deferred.

A file-count/test-count approach could therefore declare WP-22 complete while:

- important laws have no proof;
- several tests prove the same narrow surface;
- a test targets a superseded assumption;
- architecture-only future work is incorrectly marked missing implementation;
- one semantic law needs both deterministic and empirical proof but receives only one.

**Required repair**

The Step-1 brief must require an item-level Verification Coverage Matrix with current owner, polarity, realization status, proof class, exact verification artifacts, execution route, stale/supersession disposition and defer trigger.

**Disposition:** `REPAIRED_IN_STEP1`. The repaired Task Brief makes the matrix a mandatory Step-2 evidence gate and forbids final coverage claims before it exists.

---

### F22-S1-02 — SIGNIFICANT — Proof-class conflation can turn scenarios/static checks into executable behavioral evidence

**Mechanism**

Current verification surfaces mix:

- Python executable unit/contract tests;
- static maintenance audit rules;
- Markdown scenario/adversarial cases;
- empirical LLM evaluation research;
- deferred operational/performance TODOs.

`audit_engine.py` also inspects selected Markdown test files for sentinel content and checks case-ID uniqueness. Without explicit classification, this can be misreported as execution of those scenarios.

**Required repair**

Introduce explicit proof classes and state what each class can and cannot prove. Green CI means the currently admitted audit and unit tests executed at that head; it does not prove semantic completeness or empirical product quality.

**Disposition:** `REPAIRED_IN_STEP1` by the verification proof taxonomy and CI/audit boundary in the repaired brief.

---

### F22-S1-03 — SIGNIFICANT — Protocol-4-derived evaluation source is not present in current repository evidence

**Mechanism**

The controlling WP-22 scope explicitly asks whether “Protocol-4-derived MVP evaluations” are retained as post-implementation acceptance. Current repository discovery establishes Protocols 1–3 and supporting WP-08 MVP obligations, but no current Protocol-4 artifact or commit match was found.

Silently treating Protocol 3 as Protocol 4 would fabricate provenance and could lose the actual intended evaluation dimensions or applicability limits.

**Required repair**

The Source Manifest must mark the exact Protocol-4 source as `INCOMPLETE_SURFACE / NOT FOUND`, preserve Protocols 1–3 and WP-08 as supporting evidence only, and make source recovery/reconciliation mandatory before a final behavioral-evaluation completeness claim.

**Disposition:** `REPAIRED_IN_STEP1 AS SOURCE-MANIFEST DISCIPLINE`; the source gap itself remains an explicit **Step-2 evidence obligation**, not a product decision and not a Step-1 blocker after honest routing.

```text
PROTOCOL_4_SOURCE_RECOVERED: NO
STEP2_SOURCE_RECOVERY_REQUIRED: YES
PO_DECISION_REQUIRED: NO
```

---

### F22-S1-04 — SIGNIFICANT — Current engine-update executable test preserves an obsolete semantic implication

Affected artifact:

- `DEV/TESTS/test_engine_update_policy_contract.py`.

Current test name before repair:

```text
test_same_version_descendant_refresh_is_silent_and_does_not_force_manifest_commit
```

**Mechanism**

The test only checked broad lexical tokens such as `same-version`, `silently prefer` and `ancestor`. Current `GAME/CORE/ENGINE_UPDATES.md` still contains those words but now uses them under a materially different law:

```text
ancestry -> provenance/order evidence only
silent preference -> candidate to evaluate only
different released bytes -> affirmative compatibility classification still required
```

Therefore the old test could remain green while its name and assertion set implied the superseded pre-WP20 rule that ancestry itself authorizes silent refresh/use.

**Required repair**

Synchronize the executable regression with the existing current runtime owner. Assert specifically that provenance/order rules never replace compatibility classification, silent preference is only candidate selection, and different bytes still require affirmative compatibility. Preserve the “no standalone cosmetic commit” and non-creator constraints.

Do **not** change `GAME/CORE/ENGINE_UPDATES.md`; current runtime law is already correct.

**Disposition:** `REPAIRED_IN_STEP1` by a mechanical test-only edit to `DEV/TESTS/test_engine_update_policy_contract.py`.

Negative finding: `DEV/TESTS/ENGINE_UPDATE_CASES.md` is already aligned with released-v1+ clean-slate and ancestry-as-provenance semantics; no repair there.

---

### F22-S1-05 — SIGNIFICANT — Existing negative-law regressions do not prove negative-law completeness

**Mechanism**

The project has strong individual negative-law guards, but no current evidence that every materially regression-prone rejection/fail-closed law has appropriate protection. Particularly dangerous omissions would include:

- duplicate/alternate authority paths;
- stale/currentness guessing;
- unsupported compatibility/migration inference;
- hidden data/knowledge/disclosure promotion;
- mechanics replay/reroll/rebinding;
- force/ref-rewind publication shortcuts;
- Story/planning/cache becoming native authority;
- ambiguous/unsupported state being optimistically interpreted.

**Required repair**

Step 2 must inventory important current `NEGATIVE`, `FAILURE` and `INDETERMINATE` laws separately and map each to executable/static/scenario/deferred proof. A positive happy-path test does not automatically cover its forbidden dual.

**Disposition:** `REPAIRED_IN_STEP1` as a mandatory Step-2 evidence obligation. No broad regression implementation is started in Step 1.

---

### F22-S1-06 — SIGNIFICANT — CI/maintenance-audit success can be overclaimed as architecture completeness

**Mechanism**

Current hosted validation is real and valuable:

```text
Run full maintenance audit
Run DEV unit tests
```

But the maintenance audit is a bounded structural/source/schema/catalog/test-sentinel verifier and unittest discovery runs only the admitted executable suite. Neither independently answers whether:

- all important laws have proof ownership;
- tests are semantically current;
- deferred implementation obligations are correctly deferred;
- LLM behavior/performance acceptance has been measured.

**Required repair**

The brief must define CI as an execution route for admitted machine-checkable proofs, not a completeness oracle. Step 2 must separately decide which additional architecture invariants are honestly machine-checkable and which remain scenario/human/empirical evaluation concerns.

**Disposition:** `REPAIRED_IN_STEP1`.

---

### F22-S1-07 — MINOR — Historical, deferred and current test artifacts need explicit status discipline

**Mechanism**

Without provenance/status classification:

- `PRE_RELEASE_AUDIT_0.1.0.md` could be mistaken for current policy;
- `TODO_LONG_CAMPAIGN_SCALE.md` could be counted as current scale proof;
- `PERFORMANCE_CASES.md` could be counted as measured performance evidence;
- old version strings inside intentional negative fixtures could be mechanically flagged as stale even when the test is correct.

**Required repair**

Classify by semantics and applicability, not filename/token age. Preserve explicitly historical/deferred artifacts without making them current acceptance authority.

**Disposition:** `REPAIRED_IN_STEP1` in the Source Manifest.

---

## 3. Severity / post-repair disposition

Initial critic result:

```text
BLOCKING: 1
SIGNIFICANT: 5
MINOR: 1
```

After the bounded Step-1 repairs:

```text
F22-S1-01: CLOSED — Verification Coverage Matrix is mandatory before completeness claim
F22-S1-02: CLOSED — proof taxonomy separates executable/static/scenario/empirical/deferred evidence
F22-S1-03: CLOSED FOR STEP-1 FRAMING — Protocol-4 source absence is explicit; Step-2 recovery remains mandatory
F22-S1-04: CLOSED — stale engine-update regression repaired against current owner
F22-S1-05: CLOSED — negative-law inventory is mandatory Step-2 evidence
F22-S1-06: CLOSED — CI/audit evidence boundary is explicit
F22-S1-07: CLOSED — historical/deferred/current evidence classification is explicit

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
UNRESOLVED_MINOR: 0
```

`F22-S1-03` closure means the **Step-1 omission/overclaim risk is repaired**, not that a Protocol-4 source was magically recovered. The source-recovery obligation remains deliberately visible for Step 2.

---

## 4. Challenges that did not become findings

### N22-S1-01 — Do not add broad missing tests in Step 1

Most verification gaps cannot be implemented honestly until Step 2 establishes the exact current law and machine-realization state. Adding tests now would risk testing architecture prose rather than realized behavior or activating deferred work.

### N22-S1-02 — Do not change current engine-update runtime law

`GAME/CORE/ENGINE_UPDATES.md` already has the correct released-v1+ compatibility semantics. The stale executable test was the defect.

### N22-S1-03 — Do not treat every old version fixture as stale

Intentional negative fixtures and migration/version boundary tests may need old version values. Staleness is semantic, not lexical.

### N22-S1-04 — Do not create a global test-coverage percentage

Raw statement/line/test percentages do not show semantic ownership, failure-law coverage or evaluation applicability. The Verification Coverage Matrix is the required architecture evidence shape.

### N22-S1-05 — Do not start WP-23 through release-related verification

WP-22 may inspect release-builder/version/package tests as verification consumers. Whether the release package is actually ready, complete and legally correct remains WP-23.

---

## 5. Product Owner / human gate

No current finding requires Product Owner semantics, risk acceptance or material trade-off.

The absent Protocol-4 source is first an evidence-recovery problem. If later recovery fails and current accepted requirements are insufficient to reconstruct the intended evaluation contract without inventing criteria, Step 2 must route that exact unresolved decision rather than guessing.

```text
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

---

## 6. Version Impact of repairs

The only machine-executable change is a DEV regression test synchronized to already-current runtime law. No shipped/runtime/versioned machine owner changes.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
```

---

## 7. Exact next gate

The Step-1 package is review-ready after coherent publication and exact-head verification/read-back.

```text
WP22_STEP1_CRITIC_COMPLETE: YES
WP22_STEP1_MECHANICAL_REPAIRS_COMPLETE: YES
WP22_STEP1_COMPLETE: YES

STEP2_AUTHORIZED_BY_WORKER: NO
WP22_STEP1_SENIOR_REVIEW: REQUIRED / PENDING
NEXT_AUTHORIZED_UNIT: NONE
WP22_STEP2_STARTED: NO
WP23_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```
