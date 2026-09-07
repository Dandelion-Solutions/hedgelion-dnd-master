# R2.7 WP-22 Step 3 — Decision Brief: Verification / Test / Evaluation Completeness

Status: **STEP 3 COMPLETE — RECOMMENDATION ESTABLISHED FOR CANDIDATE SPECIFICATION**

Date: 2026-09-07

Depends on:

- WP-22 Step-1 Task Brief / Source Manifest;
- WP-22 Step-1 whole-project critic;
- mandatory independent Senior Step-1 re-review: **GO**;
- `2026-09-07-r2-7-WP-22-step-2-verification-coverage-matrix.md`.

Scope remains WP-22 only. WP-23, implementation planning and substantive implementation remain excluded.

---

## 1. Decision to make

How should HDM assign verification ownership across a large architecture where:

- some deterministic machine contracts already exist;
- some architecture is implementation-facing but intentionally unrealized;
- some behavior is meaningful only as multi-owner scenario acceptance;
- some host/LLM/product-quality behavior requires empirical evaluation;
- several negative/fail-closed/indeterminate laws are more important than happy-path examples;
- tests, audits, fixtures and research must never become semantic architecture authority merely by existing?

The decision is **not** whether all future tests should be written now. The decision is the durable mapping discipline that implementation and later acceptance must follow.

---

## 2. Established facts from Step 2

1. Current semantic owners, not test filenames, can be mapped to bounded verification law families without reopening accepted architecture.
2. Current deterministic realized slices have current executable/static proof owners at the present frontier.
3. Many WP-08…WP-21 runtime obligations are explicitly unrealized by their owners; missing executable proof there is a defer state, not a current implementation defect.
4. Protocol 4 is a current post-implementation scenario/fixture owner, but has no execution result and must not run on a surrogate MVP.
5. Hosted CI runs maintenance audit + Python unit tests. It does not execute Markdown acceptance catalogs or Protocol 4 merely because they are present.
6. Several historical/TODO/manual surfaces remain useful provenance or revisit support but are not current semantic/proof authority.
7. Green CI can prove only that admitted current machine checks passed an exact HEAD. It cannot prove owner-universe coverage or empirical acceptance.
8. No current realized material target with an unowned proof obligation was identified in Step 2.

---

## 3. Alternatives

### Alternative A — Test-file-driven verification map

Build the project’s verification model by enumerating existing tests/scenarios/audits and inferring the architecture they protect.

**Advantages**

- operationally easy;
- immediately shows what CI runs;
- familiar implementation-centric view.

**Material defects**

- allows stale tests to become accidental architecture authority;
- cannot distinguish missing future implementation from verification defect;
- under-represents negative laws that have no test yet;
- over-credits Markdown scenarios and green CI;
- loses dormant/deferred owner semantics;
- cannot prove accepted architecture coverage.

**Disposition:** **REJECT**.

---

### Alternative B — Universal deterministic CI

Require every accepted architecture law to become a deterministic executable/static CI assertion before architecture closure.

**Advantages**

- superficially simple completeness metric;
- strong automation pressure.

**Material defects**

- forces fake boolean assertions for model/host/quality behavior;
- encourages implementation before authorization merely so an architecture law can be tested;
- collapses scenario acceptance and empirical evaluation into unit-test theater;
- turns absence of future runtime into a current defect;
- risks inventing core vocabulary solely for test convenience.

**Disposition:** **REJECT**.

---

### Alternative C — Owner-first layered verification architecture

For every material current law/law family:

```text
semantic owner
    -> realization state
    -> polarity / failure semantics
    -> appropriate proof class
    -> exact current artifact or explicit defer owner
    -> actual execution/evaluation route
    -> supersession / revisit rule
```

Use four proof channels only where semantically appropriate:

```text
DETERMINISTIC MACHINE LAW
    -> executable unit/contract/integration proof

STRUCTURAL SOURCE LAW
    -> static maintenance audit

BOUNDED MULTI-OWNER ACCEPTANCE LAW
    -> scenario acceptance

HOST / LLM / QUALITY / PERFORMANCE BEHAVIOR
    -> empirical production-like evaluation
```

Overlay explicit states for unrealized, historical and genuinely unverified targets.

**Advantages**

- preserves architecture authority;
- makes negative/failure/indeterminate cases first-class;
- prevents missing future implementation from becoming a false defect;
- prevents green CI from becoming a completeness claim;
- naturally incorporates Protocol 4 after implementation;
- supports bidirectional stale-test detection;
- allows exact implementation-phase TDD obligations to be generated later without premature implementation.

**Costs**

- requires owner-aware maintenance of the matrix;
- more disciplined than a simple test inventory;
- completeness review is semantic, not reducible to one CI badge.

**Disposition:** **RECOMMENDED**.

---

### Alternative D — Empirical-evaluation-first

Treat scenario/production-like evaluation as the main proof for most architecture, using deterministic tests only for low-level helpers.

**Advantages**

- close to observed product behavior;
- useful for LLM/host effects.

**Material defects**

- weakens deterministic owner contracts that should fail cheaply and exactly;
- makes root-cause isolation difficult;
- can hide structural/schema/currentness violations behind acceptable-looking outputs;
- is expensive and unsuitable for every change;
- risks empirical results outranking architecture.

**Disposition:** **REJECT** as a primary architecture; retain empirical evaluation as one required layer.

---

## 4. Recommendation

Adopt **Alternative C — Owner-first layered verification architecture**.

### 4.1 Durable rules

1. **Semantic owners precede verification artifacts.**
2. **Realization state precedes proof expectation.**
3. **Polarity is explicit.** Positive, negative, failure, indeterminate, performance and behavioral obligations may require different proof.
4. **Executable proof is preferred only for deterministic realized law.**
5. **Static audit is structural only.** It must not claim behavior it cannot execute.
6. **Scenario acceptance is a current acceptance specification, not an execution result.**
7. **Empirical evaluation is required where host/LLM/quality/performance behavior is genuinely empirical.**
8. **Deferred is a valid current disposition.** Coverage does not activate the deferred subsystem.
9. **`VERIFICATION_GAP` is reserved for realized material targets lacking sufficient proof.**
10. **Historical/supporting artifacts remain non-authoritative.**
11. **Bidirectional reconciliation is mandatory whenever coverage/completeness is claimed.**
12. **Green CI means admitted checks passed exact HEAD only.**

### 4.2 Protocol 4

Protocol 4 remains:

```text
SCENARIO_ACCEPTANCE_CURRENT
execution result: NOT CLAIMED
post-implementation execution: DEFERRED_UNTIL_REALIZATION
```

Required sequence remains unchanged:

```text
R2.6 architecture assurance
-> R2.7 machine/instruction/test mapping
-> implementation planning
-> MVP implementation via TDD
-> production-like evaluation on the real MVP
```

### 4.3 Negative-law handling

Implementation planning must not derive a test plan only from happy-path machine features. It must route the Step-2 item-level negative/fail-closed/failure/indeterminate inventory into future TDD/scenario/evaluation work where the corresponding realization is authorized.

This does not require converting open-ended player/GM behavior into a closed core vocabulary.

---

## 5. Consequences for downstream work

### Implementation planning — later, not now

When authorized, implementation planning should consume the canonical WP-22 mapping and generate tests from current owners plus the item-level negative inventory.

It must not infer requirements from legacy tests that are inconsistent with newer owners.

### MVP implementation — later, not now

TDD will realize deterministic obligations together with their current proof owners.

### Post-implementation acceptance — later, not now

Protocol 4 and other production-like evaluations execute against the actual implemented MVP, preserving fixture provenance and applicability.

### WP-23

WP-23 remains separate release/readiness work and is not activated by current release-tool tests or by WP-22 canonicalization.

---

## 6. Product-owner decision analysis

No new material product semantics or trade-off requires Product Owner judgment in Step 3.

The key product/architecture boundaries are already fixed by accepted owners and the explicit WP-22 assignment:

- owner-first mapping;
- no surrogate Protocol 4 execution;
- deferred != defect;
- green CI != completeness;
- coverage != activation.

Therefore:

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
```

Step 4 may review cross-system consistency, but it must not invent a new owner merely to make verification simpler.
