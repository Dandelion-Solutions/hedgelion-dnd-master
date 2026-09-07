# R2.7 WP-22 — Verification / Test / Evaluation Completeness — Canonical Specification

Status: **CANONICAL — WP-22 STEP-8 RESULT / FINAL SENIOR REVIEW PENDING**

Date: 2026-09-07

This specification is the final semantic owner for R2.7 WP-22 verification/test/evaluation completeness architecture.

It does not implement runtime behavior, write implementation plans, execute Protocol 4, activate deferred subsystems, or begin WP-23.

Design provenance:

- Step-1 Task Brief / Source Manifest and whole-project critic;
- mandatory independent Step-1 Senior re-review: **GO**;
- Step-2 owner-first Verification Coverage Matrix;
- Step-3 Decision Brief;
- Step-4 Cross-System Collaborative Review;
- Step-5 Candidate Specification;
- Step-6 Whole-Project Adversarial Review;
- Step-7 Critic Resolution and Finding Propagation.

Where a design artifact contains shorthand repaired by Step 7, this final specification controls.

---

## 1. Central architecture

HDM verification completeness is **owner-first and layered**.

For every material current architecture law or bounded law family, reasoning proceeds in this order:

```text
current semantic owner
-> law / bounded law slice
-> polarity / outcome class
-> machine-realization status
-> primary verification state
-> exact verification/acceptance artifact(s), if any
-> actual current CI/audit/scenario/evaluation route
-> stale/supersession disposition
-> remaining verification/realization gap
-> safe defer/revisit trigger
```

Verification artifacts consume semantic owners. They never become a parallel architecture authority merely by existing, being detailed, or passing.

### LAW WP22-1 — SEMANTIC OWNER PRECEDES VERIFICATION ARTIFACT

Tests, audits, CI workflows, scenarios, fixtures, evaluation protocols, research ledgers, historical syntheses, navigation indexes and TODOs SHALL verify, route or support current semantic owners; they SHALL NOT create, supersede or reactivate engine semantics merely by presence or success.

---

## 2. Source-role separation

Every correctness-sensitive verification mapping SHALL distinguish at least:

```text
SEMANTIC_OWNER
VERIFICATION_OR_ACCEPTANCE_ARTIFACT
SUPPORTING_PROVENANCE_OR_ROUTING
```

### 2.1 Semantic owner

A semantic owner may be:

- an accepted architecture/runtime/model owner;
- a final accepted canonical specification or amendment;
- an explicit accepted Product Owner decision for its decision scope;
- a schema/catalog/machine contract only where accepted architecture delegates exact machine authority to it.

### 2.2 Verification / acceptance artifact

Examples:

- executable unit/contract/integration tests;
- maintenance audit checks;
- bounded Markdown scenario catalogs;
- frozen acceptance fixtures;
- Protocol-4 design/fixture sources;
- production-like evaluation protocol/results.

These may own the verification or acceptance case they define, but they do **not** thereby own the engine semantic law under test.

### 2.3 Supporting provenance / routing

Examples:

- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
- raw Product Owner routing/input not yet incorporated into accepted architecture;
- design/research provenance;
- historical reports/TODOs.

These SHALL NOT appear as semantic owners merely for convenience.

### LAW WP22-2 — SOURCE ROLE MAY NOT BE COLLAPSED

A completeness matrix that cannot distinguish semantic authority from verification/acceptance ownership and provenance/routing support is invalid.

---

## 3. Four dimensions remain independent

The following dimensions SHALL remain separate:

```text
ARCHITECTURE COVERAGE
MACHINE REALIZATION
VERIFICATION REALIZATION
EMPIRICAL ACCEPTANCE
```

### LAW WP22-3 — COVERAGE IS NOT REALIZATION

Accounting for an accepted law in the verification matrix does not authorize or imply its machine realization.

### LAW WP22-4 — REALIZATION IS NOT VERIFICATION

A realized target may still lack sufficient verification. Missing verification becomes a current gap only under the narrow rule in §7.

### LAW WP22-5 — VERIFICATION IS NOT EMPIRICAL ACCEPTANCE

Deterministic/static verification does not establish production-like host/LLM/product-quality acceptance unless the semantic owner makes the behavior deterministically checkable.

### LAW WP22-6 — EMPIRICAL ACCEPTANCE DOES NOT OVERRIDE ARCHITECTURE

A favorable empirical result may demonstrate observed conformance within its applicability window; it cannot weaken or supersede accepted authority/currentness/mechanics/containment law.

---

## 4. Required polarity inventory

For each material law slice, preserve all applicable polarity classes:

```text
POSITIVE
NEGATIVE
FAILURE
INDETERMINATE
PERFORMANCE
BEHAVIORAL
```

### LAW WP22-7 — NEGATIVE / FAIL-CLOSED / INDETERMINATE LAW IS FIRST-CLASS

Coverage SHALL explicitly retain material:

- prohibitions and negative controls;
- fail-closed conditions;
- conflict/failure outcomes;
- stale/currentness failures;
- indeterminate/ambiguous outcomes;
- performance or resource-pressure obligations;
- behavioral containment/agency/quality boundaries.

Happy-path verification never erases a negative or indeterminate owner law.

Ordinary novel player actions and GM improvisation SHALL NOT be forced into a closed core vocabulary solely to make testing convenient.

---

## 5. Machine-realization status

WP-22 uses the following machine-realization vocabulary for the current mapping layer:

```text
REALIZED_CURRENT
PARTIAL_CURRENT
ARCHITECTURE_ONLY
DORMANT_OR_CONDITIONAL
HISTORICAL_ONLY
```

`PARTIAL_CURRENT` means a specifically named bounded slice exists while the complete subsystem remains unrealized.

A machine-realization status is not a proof result.

---

## 6. Primary verification-state vocabulary

Every material law slice SHALL have exactly one **primary current verification state** from:

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

### 6.1 Interpretation

- `EXECUTABLE_CURRENT` — a current deterministic target exists and current executable verification checks the bounded invariant.
- `STATIC_AUDIT_CURRENT` — a current structural/source/schema/catalog/layout/text/generation-smoke invariant is admitted by the maintenance-audit route that actually checks it.
- `SCENARIO_ACCEPTANCE_CURRENT` — a current bounded scenario/fixture defines acceptance obligations; presence is not an execution result.
- `EMPIRICAL_EVALUATION_CURRENT` — current empirical execution results exist for the claimed behavior and applicability window.
- `DEFERRED_UNTIL_REALIZATION` — the relevant target/proof cannot or should not yet be realized under the current owner and no stronger current proof class applies.
- `VERIFICATION_GAP` — the narrow current defect state defined in §7.
- `SUPERSEDED_OR_HISTORICAL` — retained evidence/scaffold/history that is not current proof authority.
- `NOT_MACHINE_CHECKABLE` — the open-ended semantic/product-quality judgment cannot honestly be reduced to deterministic verification.

### 6.2 Supporting acceptance and bounded splits

A law slice may additionally reference a **supporting acceptance artifact** without changing its primary state.

If an aggregated family has independently realized sub-slices with different primary states, the mapping SHALL split them into bounded sub-rows. Canonical primary-state fields SHALL NOT use `+`, `/`, or prose concatenation to represent multiple states.

Examples:

```text
publication outcome algebra
  machine: PARTIAL_CURRENT
  primary verification: EXECUTABLE_CURRENT

end-to-end remote publication
  machine: ARCHITECTURE_ONLY
  primary verification: DEFERRED_UNTIL_REALIZATION

open-ended GM dramatic quality
  primary verification: NOT_MACHINE_CHECKABLE

bounded GM containment scenario
  primary verification: SCENARIO_ACCEPTANCE_CURRENT
```

### LAW WP22-8 — PROOF CLASS MUST MATCH ACTUAL PROOF POWER

No artifact may be credited with a stronger proof class than the work it actually performs.

---

## 7. Verification-gap semantics

### LAW WP22-9 — DEFERRED PROOF IS NOT A CURRENT IMPLEMENTATION DEFECT

If accepted architecture intentionally leaves a runtime/schema/tool target for later realization, absence of executable proof is not a present defect merely because a future test will be required.

### LAW WP22-10 — `VERIFICATION_GAP` IS NARROW

`VERIFICATION_GAP` applies only when all are true:

```text
material current semantic-owner law exists
AND the relevant machine/runtime target is realized now
AND an appropriate sufficient current proof owner is absent, stale or contradicted
```

`VERIFICATION_GAP` SHALL NOT mean only “no test file exists”.

---

## 8. Partial-realization discipline

### LAW WP22-11 — PARTIAL PROOF MAY NOT EXPAND TO THE WHOLE SUBSYSTEM

A current proof for a bounded realized slice proves only that slice.

Current examples include:

- publication exact-base/currentness outcome algebra vs end-to-end publisher;
- WP-18 planning-entry provenance vocabulary vs retained planning runtime;
- engine-update policy projection vs updater/migrator runtime;
- local bootstrap generation/audit vs remote campaign publication/activation;
- PO-006 branch/ref prohibition guards vs unrelated cleanup-family runtimes.

The unrealized remainder keeps its own realization/proof/gap/defer state.

---

## 9. Bidirectional reconciliation

Every verification-completeness claim SHALL perform both directions:

```text
accepted semantic-owner law
-> realization/defer state
-> appropriate current verification owner

existing test/audit/scenario/evaluation artifact
-> current semantic owner
```

### LAW WP22-12 — REVERSE RECONCILIATION IS MANDATORY

The reverse pass SHALL detect at least:

- stale tests;
- obsolete scaffolds;
- verification assumptions contradicted by later architecture;
- realized laws without sufficient proof;
- tests/audits/scenarios accidentally acting as architecture authority;
- partial tests over-credited as subsystem proof;
- historical/TODO/research evidence accidentally activating dormant work.

When a current test conflicts with a newer accepted owner, repair/retire/reclassify the verification artifact. Do not weaken accepted architecture solely to preserve an old test.

---

## 10. Verification-channel boundaries

### 10.1 Executable tests

Appropriate for deterministic realized contracts such as:

- typed input/output/state transitions;
- schema/catalog/version/identity rules;
- deterministic authorization/currentness gates once realized;
- fail-closed and negative behavior that can be induced deterministically;
- crash/failure/indeterminate behavior that can be injected at a realized machine boundary.

### 10.2 Static maintenance audit

Appropriate for structural/source/schema/catalog/layout/text and bounded deterministic generation-smoke invariants that the audit actually checks.

### LAW WP22-13 — STATIC AUDIT IS NOT BEHAVIORAL AUTHORITY

Static/maintenance audit SHALL NOT be cited as proof of runtime authorization, concurrency/atomicity, LLM containment, player agency, empirical performance or end-to-end publication/currentness unless that behavior is actually exercised by an admitted verification path.

### 10.3 Scenario acceptance

Appropriate where bounded multi-owner composition can be specified before implementation and where sequence/fixture semantics matter.

### LAW WP22-14 — SCENARIO DESIGN IS NOT EXECUTION

A current scenario or frozen fixture defines acceptance obligations; file presence does not establish passed behavior.

### 10.4 Empirical evaluation

Appropriate for genuinely empirical host/LLM/performance/quality behavior such as long-context containment, starvation, latency/context pressure, retry behavior or user-visible composition where deterministic tests cannot honestly establish the full claim.

### LAW WP22-15 — EMPIRICAL EVALUATION FOLLOWS REALIZATION

Production-like evaluation uses the real implemented target. HDM SHALL NOT create a preimplementation surrogate or parallel MVP merely to manufacture acceptance evidence.

---

## 11. Hosted CI and route currentness

At the 2026-09-07 WP-22 checkpoint, `.github/workflows/validate.yml` runs:

```text
DEV/TOOLS/run_maintenance_audit.py
.hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
```

Those exact commands are **checkpoint evidence**, not an eternal architecture requirement.

### LAW WP22-16 — GREEN CI PROVES ONLY ACTUAL ADMITTED CHECKS ON EXACT HEAD

A successful CI run establishes only that the checks actually executed by the current workflow passed on the reported exact HEAD.

It does not itself prove:

- semantic-owner universe completeness;
- scenario execution;
- Protocol-4 execution;
- empirical product quality;
- absence of deferred proof work;
- WP-23 release readiness.

### LAW WP22-17 — EXECUTION ROUTES MUST BE READ FRESH

Every future completeness/closure claim SHALL re-read the actual current CI/audit/evaluation route and bind the claim to the exact HEAD and checks executed. Workflow command changes require mapping/currentness reconciliation even when they do not require an architecture change.

---

## 12. Protocol 4

The current required classification is:

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

The R2.6 accepted assurance spec is the semantic owner. The Protocol-4 design and frozen fixture are current acceptance artifacts, not semantic architecture owners.

### LAW WP22-18 — PROTOCOL 4 EXECUTES ONLY ON THE REAL MVP

Required sequence:

```text
R2.6 architecture assurance
-> R2.7 machine/instruction/test mapping
-> implementation planning
-> MVP implementation via TDD
-> production-like evaluation on the real MVP
```

WP-22 SHALL NOT execute Protocol 4.

### 12.1 Required future Protocol-4 acceptance coverage

The accepted future mapping preserves at least:

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
11. multiplayer agency-barrier false-positive and false-negative controls;
12. maximal-safe-frontier narration;
13. stale collaboration generation, join/rejoin and external-consent impersonation cases;
14. Dramaturg coherence/lazy retrieval/no global planning scan;
15. shared horizon conflict/rebase/no plot restoration;
16. Connector currentness/CAS/conflict/failure under supported current-ref semantics;
17. retry/regeneration without mechanics/RNG/canon replay;
18. reasoning-profile regression when materially applicable.

These remain acceptance obligations, not current execution results.

---

## 13. Owner-specific future verification obligations

Coverage does not activate these obligations. They are routed only when their corresponding realization is authorized.

### 13.1 PO-005 creator authority

Future executable coverage SHALL include:

- creator-login rename mismatch -> fail closed/read-only;
- no stable-ID substitution;
- repository Admin/Write/collaborator permission cannot recover creator authority;
- no silent creator transfer.

### 13.2 PO-006 branch/ref operations

Current law remains absolute unless explicitly reopened by the Product Owner:

- no branch/ref deletion;
- no delete capability probing/retry;
- no native Git/private HTTP/manual/out-of-band fallback;
- physical residue does not establish authority/currentness;
- logical deauthorization/retirement only.

Current executable negative guards remain legitimate proof consumers of PO-006.

### 13.3 Publication/recovery

Future realized coverage SHALL retain:

- conflict vs preauthority failure vs indeterminate outcome;
- no blind retry of indeterminate remote publication;
- no durable-frontier advancement from failed/indeterminate publication;
- recovery never invents missing/corrupt truth.

### 13.4 Chronology/collaboration

Future realized coverage SHALL retain:

- `DUE` as derived state;
- no wall-clock fictional authority or fake total order;
- unresolved chronology remains indeterminate/enrolled;
- absence is not consent and not immunity;
- external report is not PC authority;
- stale collaboration generation cannot mutate successor;
- positive bounded dependency before enrollment;
- independent safe prefix is not globally frozen.

### 13.5 Story/Dramaturg

Future realized/scenario/empirical coverage SHALL retain:

- Story and planning are non-authoritative;
- no same-envelope Story feedback;
- canon invalidates preparation;
- preparation has no entitlement to occur;
- no plot restoration merely to recover an invalidated plan.

---

## 14. Historical/supporting evidence

### LAW WP22-19 — HISTORICAL/SUPPORTING ARTIFACTS DO NOT SELF-REACTIVATE

Historical audits, TODOs, research cases, old scenarios and retained scaffolds may remain discoverable. Their presence cannot reactivate dormant architecture or become current semantic/proof authority without current-owner reconciliation.

Examples at this checkpoint:

- `PRE_RELEASE_AUDIT_0.1.0.md` — historical for current readiness;
- `TODO_MULTIPLAYER_LIVE_BRANCH.md` — historical/deferred scaffold under later LIVE/collaboration owners;
- `TODO_LONG_CAMPAIGN_SCALE.md` — supporting trigger evidence only; current R2.3/WP-11 owners control scale-revisit activation;
- older context/performance research — supporting evidence unless explicitly mapped to a current owner/acceptance claim.

---

## 15. Product-quality boundary

### LAW WP22-20 — OPEN-ENDED QUALITY IS NOT FAKED AS DETERMINISTIC CI

Believable GM craft, tone, dramatic quality and similar open-ended judgments SHALL NOT be converted into artificial boolean architecture assertions.

Bounded authority/mechanics/currentness/containment constraints around them may still be executable or scenario-checkable. Product-quality acceptance may use bounded scenario/human/empirical evaluation where appropriate.

---

## 16. Release boundary

### LAW WP22-21 — WP-22 DOES NOT ACTIVATE WP-23

Existing release tooling/tests are verification consumers for their current tooling/source-boundary owners. Their presence does not constitute WP-23 release-readiness synthesis and does not authorize WP-23.

---

## 17. Current verification-frontier disposition

The Step-2 owner universe, corrected by Step-7 source-role and primary-state normalization, yields:

```text
OWNER_UNIVERSE_RECONCILED: YES
VERIFICATION_UNIVERSE_RECONCILED: YES
BIDIRECTIONAL_RECONCILIATION: COMPLETE FOR WP-22 DESIGN SCOPE
NEGATIVE_FAIL_CLOSED_INVENTORY: COMPLETE AT MATERIAL LAW-FAMILY LEVEL
PROTOCOL_4_ACCEPTANCE_MAPPING: COMPLETE
PROTOCOL_4_EXECUTED: NO
CURRENT_REALIZED_MATERIAL_TARGET_WITH_UNOWNED_PROOF: NONE IDENTIFIED
VERIFICATION_GAP_COUNT: 0
DEFERRED_VERIFICATION_OBLIGATIONS: PRESENT / EXPECTED
STALE_EXECUTABLE_TEST_FORCING_ARCHITECTURE: NONE IDENTIFIED
HISTORICAL_OR_SUPPORTING_NONAUTHORITATIVE_SURFACES: PRESENT / CLASSIFIED
```

`VERIFICATION_GAP_COUNT: 0` is scoped to the current machine-realization frontier. It is not a claim that the future MVP is implemented, fully tested or empirically accepted.

---

## 18. Version Impact

WP-22 canonicalization changes DEV architecture/traceability only.

It does not change:

- shipped `GAME/` runtime behavior;
- machine schema/catalog/template formats;
- engine release identity;
- campaign/storage version;
- ruleset semantics;
- migration behavior;
- implementation authorization.

Therefore:

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

---

## 19. Canonical exit / gate

```text
WP22_STEPS_2_8_ARCHITECTURE_RESULT: CANONICAL
STEP6_BLOCKING_UNRESOLVED: 0
STEP6_SIGNIFICANT_UNRESOLVED: 0
STEP6_MINOR_UNRESOLVED: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
PROTOCOL_4_EXECUTED: NO
WP23_STARTED: NO
NEXT_GATE: MANDATORY INDEPENDENT FINAL SENIOR REVIEW OF WP-22
```

No next work package or implementation plan is authorized by this specification.
