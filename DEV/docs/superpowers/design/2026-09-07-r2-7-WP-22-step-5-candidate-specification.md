# R2.7 WP-22 Step 5 — Candidate Specification: Verification / Test / Evaluation Completeness

Status: **CANDIDATE — READY FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-07

Basis:

- WP-22 Step-1 Task Brief / Source Manifest;
- WP-22 Step-1 whole-project critic;
- mandatory independent Senior Step-1 re-review: **GO**;
- Step-2 Verification Coverage Matrix;
- Step-3 Decision Brief;
- Step-4 Cross-System Collaborative Review.

This candidate specifies verification ownership and completeness semantics. It does not implement tests/runtime, execute Protocol 4, begin implementation planning, or activate WP-23.

## Post-review supersession notice

This Step-5 candidate is retained as **historical design provenance**. The mandatory Step-6 adversarial review materially qualified this candidate through:

- `SR22-06-01` — semantic-owner/source-role separation;
- `SR22-06-02` — single primary verification state and explicit bounded-split representation.

Step 7 resolved both findings. Any Step-5 formulation materially qualified by those findings is therefore **non-current and MUST NOT be used as the current canonical WP-22 mapping**. The candidate text below is intentionally preserved as the formulation that was actually reviewed; it is not rewritten as though it originally contained the later repairs.

Current routing:

- finding evidence — `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-step-6-whole-project-adversarial-review.md`;
- resolution/propagation — `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-step-7-resolution-propagation.md`;
- current normative owner — `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md`.

This file remains design provenance and is **not implementation-planning authority**.

---

## 1. Central invariant

HDM verification completeness is established from current semantic owners, not from the set of test/audit/scenario files that happens to exist.

Conceptually:

```text
current semantic owner
    -> material law / bounded law family
    -> realization state
    -> polarity / outcome class
    -> appropriate proof class
    -> exact proof artifact OR explicit defer owner
    -> actual execution/evaluation route
    -> supersession/revisit rule
```

The verification system never becomes a parallel architecture authority.

### LAW WP22-1 — SEMANTIC OWNER PRECEDES VERIFICATION ARTIFACT

Tests, audits, scenarios, fixtures, evaluation protocols, CI workflows, research ledgers and historical reports SHALL verify or support current owners; they SHALL NOT create or supersede engine semantics merely by existing or passing.

---

## 2. Four dimensions must remain separate

The following are independent dimensions:

```text
ARCHITECTURE COVERAGE
MACHINE REALIZATION
VERIFICATION REALIZATION
EMPIRICAL ACCEPTANCE
```

### LAW WP22-2 — COVERAGE IS NOT REALIZATION

An accepted architecture obligation may be covered by the matrix while its machine realization remains deferred. Coverage SHALL NOT authorize implementation or turn a dormant/deferred obligation into current work.

### LAW WP22-3 — REALIZATION IS NOT VERIFICATION

A machine target may exist without sufficient proof. Only then, when the target is material and realized, may missing proof become `VERIFICATION_GAP`.

### LAW WP22-4 — VERIFICATION IS NOT EMPIRICAL ACCEPTANCE

Deterministic/static checks do not establish production-like LLM/host/quality acceptance unless the current owner defines that behavior as deterministically machine-checkable.

---

## 3. Required proof-state vocabulary

Every material matrix row SHALL use exactly one primary current disposition from:

```text
EXECUTABLE_CURRENT
STATIC_AUDIT_CURRENT
SCENARIO_ACCEPTANCE_CURRENT
EMPIRICAL_EVALUATION_CURRENT
DEFERRED_UNTIL_REALIZATION
VERIFICATION_GAP
SUPERSEDED_OR_HISTORICAL
NOT_MACHINE_CHECKABLE
```

A row may name a bounded secondary disposition only when the realization is explicitly split, for example current ref-fence algebra plus deferred end-to-end publication.

### LAW WP22-5 — PROOF CLASS MUST MATCH WHAT THE ARTIFACT CAN ACTUALLY ESTABLISH

- executable proof is for deterministic realized behavior/contracts;
- static audit is for structural/source/schema/catalog/layout/text invariants;
- scenario acceptance defines bounded composition/behavior acceptance but does not itself claim execution;
- empirical evaluation is for genuinely empirical host/LLM/performance/quality behavior;
- unrealized targets use defer rather than false failure;
- historical/support artifacts remain non-authoritative.

A green artifact SHALL NOT be credited with a stronger proof class than it actually performs.

---

## 4. Polarity is mandatory

Material verification rows SHALL retain applicable polarity:

```text
POSITIVE
NEGATIVE
FAILURE
INDETERMINATE
PERFORMANCE
BEHAVIORAL
```

### LAW WP22-6 — NEGATIVE AND NON-HAPPY-PATH LAW IS FIRST-CLASS

Coverage claims SHALL preserve material:

- prohibitions;
- fail-closed conditions;
- conflict/failure outcomes;
- ambiguous/indeterminate outcomes;
- stale/currentness failures;
- negative controls;
- dormant/revisit triggers.

A happy-path test cannot erase a negative/failure/indeterminate owner law.

Ordinary novel player actions or GM improvisation SHALL NOT be forced into a closed core vocabulary solely to make verification easier.

---

## 5. Bidirectional reconciliation

Every verification completeness pass SHALL perform both directions:

```text
accepted architecture law
    -> realization/defer state
    -> appropriate verification owner

existing test/audit/scenario/evaluation artifact
    -> current semantic owner
```

### LAW WP22-7 — BIDIRECTIONAL RECONCILIATION IS REQUIRED FOR COMPLETENESS CLAIMS

The reverse pass SHALL detect at least:

- stale tests;
- obsolete scaffolds;
- assumptions contradicted by later architecture;
- realized laws without sufficient proof owner;
- tests/audits/scenarios that accidentally act as architecture authority;
- partial-realization tests that are being over-credited as subsystem proof.

If a current test conflicts with a newer accepted owner, HDM SHALL repair/retire/reclassify the test rather than weaken accepted architecture solely to preserve it.

---

## 6. Realization-sensitive gap semantics

### LAW WP22-8 — DEFERRED VERIFICATION IS NOT A CURRENT IMPLEMENTATION DEFECT

If the current semantic owner explicitly leaves a runtime/schema/tool behavior for later realization, missing executable proof is `DEFERRED_UNTIL_REALIZATION` unless a current realized projection independently requires proof.

### LAW WP22-9 — VERIFICATION_GAP IS NARROW

`VERIFICATION_GAP` means:

```text
material current owner law
AND relevant machine/runtime target is realized now
AND appropriate sufficient current proof owner is absent or stale
```

It SHALL NOT mean merely “no test file exists”.

---

## 7. Partial realization

Some architecture has a current bounded machine slice while the complete subsystem remains unrealized.

Examples at the WP-22 checkpoint include:

- publication exact-base/ref outcome algebra vs end-to-end publisher;
- WP-18 `planning_entry_classes` provenance vs retained planning runtime;
- engine-update policy projection vs updater/migrator runtime;
- bootstrap local generation smoke vs remote bootstrap publication/activation.

### LAW WP22-10 — PARTIAL PROOF MAY NOT EXPAND BEYOND ITS REALIZED SLICE

A current test/audit for a bounded realized slice SHALL be credited only to that slice. Remaining subsystem behavior keeps its independent defer/gap/acceptance disposition.

---

## 8. Hosted CI semantics

Current hosted validation runs maintenance audit plus Python unit discovery.

### LAW WP22-11 — GREEN CI PROVES ONLY ADMITTED CHECKS ON THE EXACT HEAD

A successful CI run establishes only that the checks actually executed by that workflow passed against the reported exact HEAD.

It does not by itself prove:

- owner-universe completeness;
- scenario acceptance execution;
- Protocol-4 execution;
- empirical behavior quality;
- WP-23 release readiness;
- absence of all future deferred verification work.

---

## 9. Static maintenance audit boundary

### LAW WP22-12 — STATIC AUDIT IS STRUCTURAL, NOT BEHAVIORAL AUTHORITY

Maintenance audit may verify source-tree, schema/catalog/template, version marker, forbidden stale-text, source/runtime boundary and deterministic generation-smoke invariants that it actually inspects.

It SHALL NOT be cited as proof of:

- authorization enforcement it does not execute;
- concurrency/atomicity it does not execute;
- LLM containment;
- player agency behavior;
- empirical performance;
- end-to-end publication/currentness unless those paths are actually exercised by an admitted test.

---

## 10. Scenario acceptance and empirical evaluation

### LAW WP22-13 — SCENARIO DESIGN IS NOT AN EXECUTION RESULT

A current scenario catalog/frozen fixture may define acceptance obligations before implementation, but its presence SHALL NOT be reported as passed behavior.

### LAW WP22-14 — EMPIRICAL EVALUATION FOLLOWS REALIZATION

Production-like evaluation SHALL use the implemented target to measure genuinely empirical behavior. A preimplementation surrogate/parallel MVP SHALL NOT be created merely to manufacture acceptance evidence.

---

## 11. Protocol 4

The following classification is canonical for this WP-22 candidate:

```text
PROTOCOL_4_DESIGN_SOURCE: PRESENT / CURRENT
PROTOCOL_4_FROZEN_FIXTURE_SOURCE: PRESENT / CURRENT
PROTOCOL_4_DESIGN_CLASS: SCENARIO_ACCEPTANCE_CURRENT

PROTOCOL_4_EXECUTION_RESULTS:
    NOT CLAIMED
    NOT YET EXECUTED ON IMPLEMENTED MVP

PROTOCOL_4_POST_IMPLEMENTATION_EXECUTION:
    DEFERRED_UNTIL_REALIZATION

STEP2_PROTOCOL4_SOURCE_RECOVERY_REQUIRED: NO
STEP2_PROTOCOL4_ACCEPTANCE_MAPPING_REQUIRED: YES / COMPLETE
```

### LAW WP22-15 — PROTOCOL 4 EXECUTES ONLY ON THE REAL MVP AFTER IMPLEMENTATION

The sequence is fixed:

```text
R2.6 architecture assurance
-> R2.7 machine/instruction/test mapping
-> implementation planning
-> MVP implementation via TDD
-> production-like evaluation on the real MVP
```

WP-22 SHALL NOT execute Protocol 4 or create a parallel implementation.

---

## 12. Required Protocol-4 post-implementation coverage

The current future acceptance mapping SHALL preserve at least:

1. hidden-information containment;
2. lawful subsequent uptake / positive control;
3. Dramaturg/Actor/Chronicler -> Narrator containment;
4. local/shared planning -> Narrator/catch-up containment;
5. no same-envelope Story feedback;
6. stale/foreign ambient context loses to current owners;
7. instruction-like data cannot self-promote;
8. EMISSION_COMMIT and auxiliary-surface safety;
9. context pressure / representation floors / `UNSATISFIABLE`;
10. Chronicler anti-starvation under heavy/light mixtures;
11. multiplayer agency barrier false-positive and false-negative controls;
12. maximal-safe-frontier narration;
13. stale collaboration generation, join/rejoin and external-consent impersonation cases;
14. Dramaturg coherence/lazy retrieval/no global planning scan;
15. shared horizon conflict/rebase/no plot restoration;
16. Connector currentness/CAS/conflict/failure under the supported current-ref model;
17. retry/regeneration without mechanics/RNG/canon replay;
18. reasoning-profile regression when materially applicable.

These are acceptance obligations, not current execution results.

---

## 13. Mandatory owner-specific future verification obligations

The candidate does not enumerate every future unit test implementation detail, but the following current owner constraints SHALL remain explicitly routable when their implementation becomes authorized:

### PO-005 creator authority

- creator-login rename mismatch fails closed/read-only;
- no stable-ID substitution;
- repository permission cannot recover creator authority;
- no silent ownership transfer.

### PO-006 branch/ref capability

- no branch/ref delete;
- no capability probe/retry;
- no native Git/private HTTP/manual fallback;
- physical residue does not establish authority/currentness;
- logical deauthorization/retirement only.

PO-006 already has current executable negative guards and remains absolute unless the Product Owner explicitly reopens it.

### Publication/recovery

- conflict vs preauthority failure vs indeterminate outcomes remain distinct;
- indeterminate remote publication is reconciled, not blindly retried;
- durable frontier never advances from failed/indeterminate publication;
- recovery never invents missing/corrupt truth.

### Chronology/collaboration

- `DUE` remains derived;
- no wall-clock chronology authority or fake total order;
- indeterminate chronology remains unresolved/enrolled;
- absence is not consent and not immunity;
- external intent report is not PC authority;
- stale collaboration generation cannot mutate successor;
- positive bounded dependency is required before enrollment;
- safe independent prefix is not globally frozen.

### Story/Dramaturg

- Story/planning remain non-authoritative;
- no same-envelope Story feedback;
- canon invalidates preparation;
- no preparation entitlement/no plot restoration.

---

## 14. Historical/supporting artifact disposition

### LAW WP22-16 — HISTORICAL OR SUPPORTING EVIDENCE CANNOT SELF-REACTIVATE

Historical audits, TODOs, research cases and old scenario scaffolds may remain discoverable. Their existence does not make them current proof, activate dormant architecture or override newer owners.

At this checkpoint:

- `PRE_RELEASE_AUDIT_0.1.0.md` is historical for current readiness;
- `TODO_MULTIPLAYER_LIVE_BRANCH.md` is historical/deferred scaffold under later LIVE/collaboration owners;
- `TODO_LONG_CAMPAIGN_SCALE.md` supports future measured-scale revisit only; R2.3/WP-11 own the trigger;
- old performance/context scenarios are supporting unless explicitly reconciled to current owners.

---

## 15. Release boundary

### LAW WP22-17 — VERIFICATION MAPPING DOES NOT ACTIVATE WP-23

Existing release-tool tests may remain current tooling verification. They do not make WP-22 a release-readiness gate and do not authorize WP-23.

---

## 16. Product-quality boundary

### LAW WP22-18 — SEMANTIC QUALITY IS NOT FAKED AS DETERMINISTIC CI

Open-ended judgments such as believable GM craft, tone or dramatic quality SHALL NOT be converted into artificial architecture booleans.

When material, bounded scenario or empirical evaluation may assess them while deterministic rules continue to verify authority/mechanics/currentness/containment constraints.

---

## 17. Current checkpoint disposition

Applying the candidate to the Step-2 owner universe yields:

```text
CURRENT_REALIZED_MATERIAL_TARGET_WITH_UNOWNED_PROOF: NONE IDENTIFIED
VERIFICATION_GAP_COUNT: 0
DEFERRED_VERIFICATION_OBLIGATIONS: PRESENT / EXPECTED
PROTOCOL_4_EXECUTED: NO
STALE_EXECUTABLE_TEST_FORCING_ARCHITECTURE: NONE IDENTIFIED
HISTORICAL_SUPPORTING_SURFACES: CLASSIFIED
```

`VERIFICATION_GAP_COUNT: 0` is scoped to the current realization frontier. It is not a claim that the future MVP has been implemented, fully tested or empirically accepted.

---

## 18. Version / implementation impact at candidate stage

This candidate changes verification architecture documentation only.

It does not change:

- `GAME/CORE` behavior;
- schema/catalog/template machine formats;
- engine release identity;
- campaign/storage version;
- ruleset semantics;
- implementation authorization.

Final Version Impact remains a Step-7/8 obligation after adversarial review.

---

## 19. Candidate exit

Step 6 SHALL attack this candidate from a whole-project perspective, including at least:

- green-CI overclaim;
- stale test authority inversion;
- deferred-as-defect confusion;
- Protocol-4 premature execution;
- missing negative/indeterminate cases;
- PO-005 future proof omission;
- PO-006 regression;
- partial-realization overclaim;
- release-test/WP-23 scope leak;
- static-audit behavioral overclaim;
- coverage-as-activation;
- empirical results becoming architecture authority.
