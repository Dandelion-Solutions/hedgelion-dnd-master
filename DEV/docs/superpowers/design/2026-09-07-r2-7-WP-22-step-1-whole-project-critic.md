# R2.7 WP-22 Step 1 — Whole-Project Task-Brief Critic

Status: **STEP-1 TARGETED RECOVERY CRITIC RE-RUN COMPLETE — MANDATORY SENIOR RE-REVIEW PENDING**

Date: 2026-09-07

Domain: **Verification / test / evaluation completeness**

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-07-r2-7-WP-22-task-brief-source-manifest.md`.

Senior review trigger:

```text
SR22-S1-01 — SIGNIFICANT — Protocol-4 source recovery falsely reported unresolved
checkpoint reviewed: a21df28fdc61d1a01c7e962d617ae7e17902fb46
```

Review stance:

> Assume the Step-1 brief can still overclaim completeness, mistake test presence for proof, preserve superseded semantics, turn deferred evaluations into fake implementation, or omit a verification consumer. Reconstruct the verification dependency graph independently and follow every current semantic owner into the material verification/evaluation provenance before Step 2 is authorized.

This critic does not authorize Step 2 or implementation.

---

## 1. Independently reconstructed verification routes

### 1.1 Architecture-law -> realization -> verification route

```text
current accepted semantic owner
-> current machine/runtime realization or explicit deferred realization
-> appropriate proof class
-> exact verification/evaluation artifact
-> actual execution/review route
```

The critic checks that a test filename, passing workflow or repository-search result is not accepted as a substitute for the current semantic owner.

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

The critic inspects what these routes really execute rather than treating “CI green” as a whole-project proof statement.

### 1.4 Scenario/evaluation route

```text
current semantic owner
-> current evaluation-design / fixture owner(s)
-> scenario/fixture applicability
-> executed empirical result, if any
-> deferred post-implementation execution, if target not yet meaningfully realizable
```

This route is the one the original Step-1 critic failed to follow correctly for R2.6 Protocol 4.

### 1.5 Negative-law route

Representative high-risk current negative/fail-closed owners remain traced to regressions where available:

- branch/ref deletion prohibition;
- logical ref retirement;
- non-force publication/currentness;
- version namespace fail-closed census;
- one global current-progress authority;
- PO routing to closed WPs;
- released-v1+ compatibility not inferred from ancestry/version order.

Representative success does not establish completeness; the later Step-2 negative-law inventory remains mandatory if Senior authorizes Step 2.

---

## 2. Original Step-1 findings and targeted correction

### F22-S1-01 — BLOCKER — No law-to-verification completeness proof structure

**Disposition:** `CLOSED`. The Verification Coverage Matrix remains mandatory before any final completeness claim.

### F22-S1-02 — SIGNIFICANT — Proof-class conflation can turn scenarios/static checks into executable behavioral evidence

**Disposition:** `CLOSED`. Proof classes remain separated.

### F22-S1-03 — SIGNIFICANT — Protocol-4 provenance was misclassified as absent

**Original incorrect mechanism**

The original Step-1 critic asserted that no Protocol-4 source existed in current repository evidence and routed Protocol-4 as a Step-2 source-recovery problem.

That assertion was false.

**Root cause**

The original critic used repository-level discovery/search as if it were authority and failed to traverse the current R2.6 canonical owner:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`.

That current owner explicitly includes in its canonicalization basis:

- `DEV/docs/superpowers/design/2026-08-24-r2-6-production-like-assurance-protocol.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-protocol-4-frozen-fixture-contract.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`.

The same canonical owner explicitly states that architecture-stage host assurance closes without claiming downstream MVP acceptance has executed.

The owner clarification is material because it fixes the sequencing law:

```text
R2.6 architecture assurance
-> R2.7 machine/instruction/test mapping
-> implementation planning
-> MVP implementation (TDD)
-> production-like Protocol-4-derived acceptance/evaluation on the real MVP
```

It also classifies Protocol 4 as a **test-design inventory and acceptance corpus source**, not as a completed pre-implementation execution campaign.

The Protocol-4 design artifact itself is statused:

```text
PROTOCOL DESIGN — EXECUTION EVIDENCE NOT YET CLAIMED
```

The frozen fixture is statused:

```text
RESEARCH FIXTURE CONTRACT — NO EXECUTION RESULTS CLAIMED
```

**Correct classification**

```text
PROTOCOL_4_DESIGN_SOURCE: PRESENT / CURRENT
PROTOCOL_4_FROZEN_FIXTURE_SOURCE: PRESENT / CURRENT
PROTOCOL_4_CURRENT_PROOF_CLASS: SCENARIO_ACCEPTANCE_CURRENT
PROTOCOL_4_EXECUTED_EMPIRICAL_ACCEPTANCE: NO
PROTOCOL_4_POST_IMPLEMENTATION_EXECUTION: DEFERRED_UNTIL_REALIZATION
STEP2_PROTOCOL4_SOURCE_RECOVERY_REQUIRED: NO
STEP2_PROTOCOL4_ACCEPTANCE_MAPPING_REQUIRED: YES
PO_DECISION_REQUIRED: NO
```

**Required repair**

1. Add the current R2.6 owner chain to the WP-22 Source Manifest.
2. Remove every current projection that says Protocol 4 is missing/not found or requires source recovery.
3. Preserve the distinction between current protocol/fixture design evidence and not-yet-executed post-implementation MVP acceptance.
4. Re-run the whole-project Step-1 critic against the corrected source set.

**Disposition:** `REPAIRED_IN_TARGETED_STEP1_RECOVERY`.

---

### F22-S1-04 — SIGNIFICANT — Current engine-update executable test preserves an obsolete semantic implication

**Disposition:** `CLOSED`. The previously published mechanical regression repair remains unchanged; `GAME/CORE/ENGINE_UPDATES.md` remains unchanged.

### F22-S1-05 — SIGNIFICANT — Existing negative-law regressions do not prove negative-law completeness

**Disposition:** `CLOSED FOR STEP1 FRAMING`. The later item-level inventory remains a Step-2 evidence obligation if authorized.

### F22-S1-06 — SIGNIFICANT — CI/maintenance-audit success can be overclaimed as architecture completeness

**Disposition:** `CLOSED`. CI remains an execution route for admitted machine-checkable proofs, not a completeness oracle.

### F22-S1-07 — MINOR — Historical, deferred and current test artifacts need explicit status discipline

**Disposition:** `CLOSED`. Classification remains semantic/applicability-based.

---

## 3. Whole-project critic re-run after Protocol-4 recovery

The corrected re-run starts from the same five mandatory WP-22 scope questions but rebuilds the source graph with an explicit rule:

> **Current semantic owner first. Repository search/discovery may find candidate evidence, but cannot override or replace owner-linked provenance.**

### 3.1 R2.6 owner-chain re-walk

Current canonicalization basis was rechecked for verification/evaluation-specific sources.

Material current chain now included directly in WP-22:

1. R2.6 canonical spec — current semantic owner;
2. MVP Behavioral Assurance / Post-Implementation Evaluation Owner Clarification — owner sequencing/acceptance law;
3. Production-Like Assurance Protocol — Protocol-4 evaluation design;
4. Protocol-4 Frozen Fixture Contract — frozen scenario/control/scoring contract;
5. Protocols 1–3 — completed pre-implementation empirical evidence within their applicability.

Supporting non-normative provenance also rechecked:

- `2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md` — explicitly non-normative pre-decision research;
- `2026-08-24-r2-6-current-host-assurance-synthesis.md` — explicitly non-canonical pre-probe synthesis and explicitly not a Protocol-4 execution claim.

These supporting sources do not supersede or compete with the canonical R2.6 owner.

### 3.2 Additional omission exposed by SR22-S1-01

The re-walk found one additional material omission in the original WP-22 Source Manifest:

```text
DEV/docs/superpowers/design/2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md
```

Why material: without it, a future reader could correctly find the Protocol-4 protocol/fixture but still misclassify them as a pre-implementation execution requirement. The clarification is the owner-approved source that moves production-like execution to the implemented MVP.

Disposition: `ADDED_TO_SOURCE_MANIFEST`.

### 3.3 Other R2.6 canonicalization-basis artifacts

The remaining task brief, candidate-spec, adversarial-review and routing artifacts are design provenance already resolved into the current canonical owner. The re-run found no unique current verification owner, execution-result artifact or acceptance law in that remainder that must be separately promoted into the WP-22 current Source Manifest.

Disposition:

```text
OTHER_MATERIAL_CURRENT_SOURCE_MANIFEST_OMISSIONS_FOUND: NO
```

### 3.4 Five mandatory WP-22 routes after correction

1. **law -> verification ownership** — still requires the Step-2 Verification Coverage Matrix; Step 1 framing remains sufficient;
2. **stale tests** — engine-update stale regression remains repaired; no new stale executable assumption was exposed by Protocol-4 recovery;
3. **Protocol-4-derived MVP evaluation** — source/design is present and current; integrated empirical execution remains correctly deferred until implemented MVP;
4. **negative/failure laws** — later item-level inventory remains mandatory; no new Step-1 architecture repair exposed;
5. **CI/audit boundary** — unchanged; no deterministic CI claim can substitute for Protocol-4 production-like execution.

### 3.5 Re-run finding result

```text
NEW_BLOCKING: 0
NEW_SIGNIFICANT: 0
NEW_MINOR: 0

SR22_S1_01_ROOT_CAUSE_CONFIRMED: YES
SR22_S1_01_REPAIRED: YES
ADDITIONAL_MATERIAL_OMISSION_FOUND: 1
ADDITIONAL_MATERIAL_OMISSION_REPAIRED: 1
UNRESOLVED_MATERIAL_SOURCE_MANIFEST_OMISSIONS: 0
```

This is a worker critic re-run, not an independent Senior PASS.

---

## 4. Challenges that did not become new findings

### N22-S1-R1 — Do not claim Protocol-4 PASS

Finding the design/fixture sources does not create execution results. No production-like Protocol-4 MVP run is claimed.

### N22-S1-R2 — Do not convert deferred acceptance into architecture implementation

The R2.6 owner explicitly moved production-like integrated evaluation after MVP implementation because a pre-implementation harness would recreate the MVP. Targeted recovery preserves that sequencing.

### N22-S1-R3 — Do not promote non-normative R2.6 research to semantic ownership

The evidence ledger and current-host synthesis remain supporting provenance. The canonical R2.6 spec and owner clarification own current semantics.

### N22-S1-R4 — Do not start Step 2 through “mapping” language

The targeted recovery identifies what Step 2 must later map if Senior authorizes it. It does not build the Verification Coverage Matrix or execute Protocol-4 acceptance now.

### N22-S1-R5 — Do not start WP-23

Release/package/legal readiness remains outside WP-22 Step-1 recovery.

---

## 5. Product Owner / human gate

No current finding requires Product Owner semantics, risk acceptance or material trade-off.

Protocol-4 provenance is resolved from existing current authority; no new criteria need to be invented.

```text
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

---

## 6. Version Impact of targeted recovery

The targeted recovery changes only DEV design/status documentation. It changes no shipped/runtime/versioned machine owner and does not modify the previously repaired DEV engine-update test.

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

---

## 7. Exact next gate

The targeted Step-1 recovery is review-ready only after coherent publication, exact-head read-back and hosted verification.

```text
WP22_STEP1_SOURCE_MANIFEST_RECOVERY_COMPLETE: YES
WP22_STEP1_CRITIC_RERUN_COMPLETE: YES
WP22_STEP1_TARGETED_RECOVERY_COMPLETE: YES

WP22_STEP1_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD — SR22-S1-01
WP22_STEP1_SENIOR_REREVIEW: REQUIRED / PENDING
STEP2_AUTHORIZED_BY_WORKER: NO
NEXT_AUTHORIZED_UNIT: NONE
WP22_STEP2_STARTED: NO
WP23_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```