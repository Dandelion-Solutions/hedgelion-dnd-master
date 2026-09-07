# R2.7 WP-23 — Step-1 Whole-Project Task-Brief Critic

Status: **COMPLETE — MECHANICAL REPAIRS APPLIED / SENIOR REVIEW PENDING**

Date: 2026-09-08

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-23-task-brief-source-manifest.md`

Review basis:

- public branch `v1/engine-rearchitecture`;
- starting/review evidence HEAD `a37c474e1da54be4a8f3e216e407e528f03cfed9`;
- current process and R2.7 owners;
- task-specific dependency subgraph reconstructed from `DEV/PROJECT_MAP.md` and actual owners/consumers rather than from the Task Brief's own source list.

This critic evaluates Step-1 framing completeness. It does not perform Step 2, make a Decision Brief, declare release readiness, or authorize implementation/release activity.

---

## 1. Independence method

The critic independently walked the composed chain:

```text
source authority
-> release/version identity
-> builder + workflow
-> exact GAME package boundary
-> installation/package selection
-> compatibility/update/migration consumer
-> formal legal copies
-> other shipped provenance surfaces
-> CI/tests/audit evidence
-> publishable artifact boundary
```

It also performed the reverse pass from current machine/test surfaces back to current owners so that detailed tests or historical design documents could not silently become semantic authority.

The three requested lanes were treated as coverage structure only. Findings were not assumed in advance.

---

## 2. Dependency-subgraph checks

### 2.1 Process/currentness

PASS:

- `DEV/CURRENT_PROGRESS.md` is the current global gate owner.
- WP-22 is closed/PASS.
- WP-23 launch required explicit Product Owner authorization; this assignment supplies it.
- Step 1 must stop at independent Senior review.
- `DEV/PROJECT_MAP.md` is used only for routing.

### 2.2 Package/build/install route

PASS after repair:

- builder implementation and launcher are included;
- tag-triggered publication workflow is included separately from builder behavior;
- current validation workflow is included as verification evidence, not release authority;
- exact `GAME/` passthrough, generated `RUNTIME_PACKAGE.yaml`, final ZIP digest, install instructions and installed-package bootstrap consumer are all represented;
- source archives are preserved as an explicit negative case;
- actual release/upload/fresh-Project smoke remains deferred, not falsely claimed.

### 2.3 Version/update route

PASS after repair:

- canonical version policy is paired with its later machine-realization status amendment;
- current pre-release normalization is not misclassified as deferred;
- WP-20 owns released-v1.0+ compatibility/migration semantics and is consumed rather than reopened;
- future exact-target migration-edge/transform realization remains deferred/implementation-only at the current pre-release frontier;
- semantic engine identity, artifact provenance and final ZIP digest remain separate.

### 2.4 Legal/provenance route

PASS for **framing completeness**, with one material evidence issue preserved:

- root formal legal/notice/license payload and distributable `GAME/` copies are included;
- builder parity checks and executable negative legal-drift test are included;
- the critic independently identified `GAME/CORE/SOURCES.md` as an additional shipped provenance surface because the builder packages all valid `GAME/` content;
- maintenance-audit enforcement of selected source-specific provenance anchors is included;
- therefore formal legal-copy parity is not allowed to stand in for complete public-provenance readiness.

The remaining provenance-policy boundary is recorded as `WP23-S1-F01` in the Task Brief. It is not mechanically decided by this critic.

---

## 3. Critic findings and disposition

### CR23-S1-01 — SIGNIFICANT — release-facing provenance surface undercounted

**Problem in initial framing:** Lane C could have been read as only `LICENSE` / `NOTICE` / `THIRD_PARTY_NOTICES.md` / `LICENSES/` plus builder parity.

**Whole-project evidence:** all valid `GAME/` files ship automatically; `GAME/CORE/SOURCES.md` is therefore release-facing and contains source-specific development provenance; the maintenance audit actively protects selected anchors in that file.

**Why significant:** a locally correct package boundary plus locally correct formal legal-copy parity can still compose into an unresolved public-provenance boundary.

**Mechanical repair:** added L08/L09, L-COV-05, explicit cross-lane synthesis and `WP23-S1-F01`.

**Disposition:** CLOSED as Task-Brief framing defect. The underlying human-owned provenance-policy question remains open evidence.

### CR23-S1-02 — SIGNIFICANT — historical version-realization status could create false gap

**Problem in initial framing:** the primary version policy retains historical future-tense realization wording.

**Whole-project evidence:** `2026-09-05-hdm-versioning-machine-realization-status-amendment.md` explicitly supersedes only that temporal status and records completed/Senior-passed pre-release normalization.

**Why significant:** treating the old temporal phrase as current would manufacture WP-23 work and violate the rule that coverage does not imply activation.

**Mechanical repair:** added the status amendment as a required current source and split current realized normalization from future released-v1.0+ migration realization.

**Disposition:** CLOSED.

### CR23-S1-03 — SIGNIFICANT — builder-only framing undercounted publication consumer

**Problem in initial framing:** proving `release_builder.py` behavior is not sufficient to frame the repository-source-to-published-artifact chain.

**Whole-project evidence:** `.github/workflows/release-runtime.yml` is the actual tag-triggered publication route and adds exact-tag checkout, tag mode, release creation and immutable asset-upload behavior; `.github/workflows/validate.yml` is a different source-validation route.

**Mechanical repair:** added both workflows with distinct roles and explicit deferred actual-release/fresh-Project obligations.

**Disposition:** CLOSED.

### CR23-S1-04 — MINOR — open-world package expansion risk was implicit

**Problem in initial framing:** the builder's all-`GAME` policy was described, but its future-content implication was not explicit.

**Whole-project evidence:** `test_release_game_passthrough.py` proves new valid root files/directories under `GAME/` are automatically archived.

**Mechanical repair:** made the expansion rule explicit in Lane A and cross-lane synthesis: any future valid `GAME/` file automatically becomes a release/legal/provenance consumer.

**Disposition:** CLOSED.

---

## 4. Adversarial checks against common false closures

| False closure | Critic result |
|---|---|
| “Formal legal files match, therefore legal/provenance readiness is complete.” | REJECTED — other shipped provenance surface exists; `WP23-S1-F01` retained. |
| “The builder can make a ZIP, therefore release workflow is complete.” | REJECTED — workflow consumer/gates separately accounted. |
| “Old version spec says realization deferred, therefore WP-23 must implement normalization.” | REJECTED — status amendment wins temporally. |
| “WP-20 overlaps updates, therefore reopen it.” | REJECTED — no contradiction/unsatisfied release consumer found. |
| “Future migration machinery is absent, therefore current pre-release product has a defect.” | REJECTED — deferred released-v1.0+ realization preserved. |
| “Green source CI proves a production Release asset.” | REJECTED — WP-22 proof-class rule retained. |
| “Known release directories are the full Source Manifest.” | REJECTED — install, runtime update, legal copies, provenance, tests and workflow consumers included. |
| “Step 1 can choose a new licensing/provenance policy to close the issue.” | REJECTED — human-owned material decision boundary preserved. |

---

## 5. Remaining material issue after mechanical repairs

```text
TASK_BRIEF_CRITIC_UNRESOLVED_BLOCKING: 0
TASK_BRIEF_CRITIC_UNRESOLVED_SIGNIFICANT: 0
TASK_BRIEF_CRITIC_UNRESOLVED_MINOR: 0
```

Separately, Step-1 evidence contains:

```text
WP23-S1-F01
SEVERITY: SIGNIFICANT
CLASS: HUMAN_OWNED_MATERIAL_DECISION / CROSS_LANE ARCHITECTURE GAP
SUBJECT: release-facing provenance policy for source-specific development/research provenance shipped under GAME/
```

The critic agrees that this issue cannot be closed mechanically in Step 1 and does not justify inventing a new workstream. It must be resolved by the Product Owner/Senior gate before Step 2 is authorized to design the final Lane-C boundary.

---

## 6. Critic verdict

```text
PROBLEM_STATEMENT: ADEQUATE AFTER REPAIR
SOURCE_MANIFEST: ADEQUATE / OPEN-WORLD FOR RECONSTRUCTED WP-23 DEPENDENCY GRAPH
LANE_A_COVERAGE: ADEQUATE
LANE_B_COVERAGE: ADEQUATE
LANE_C_COVERAGE: ADEQUATE AFTER REPAIR
CROSS_LANE_SYNTHESIS: ADEQUATE AFTER REPAIR
NEGATIVE_EVIDENCE: ADEQUATE
DEFER_VS_GAP_DISCIPLINE: ADEQUATE
WP20_REOPEN: NOT JUSTIFIED
NEW_WORKSTREAM: NOT JUSTIFIED BY WORKER

MECHANICALLY_RESOLVABLE_FINDINGS_REMAINING: 0
HUMAN_DECISION_REQUIRED: YES — exact WP23-S1-F01 provenance boundary

WP23_STEP1_FRAMING_READY_FOR_SENIOR_REVIEW: YES
WP23_STEP2_GO_RECOMMENDATION: HOLD UNTIL PO DECISION + SENIOR GO
NEXT_AUTHORIZED_UNIT: NONE
```

STOP FOR SENIOR REVIEW.
