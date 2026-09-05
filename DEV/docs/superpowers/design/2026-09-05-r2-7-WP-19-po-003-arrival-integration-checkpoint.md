# R2.7 WP-19 — PO-003 Arrival / Step-1 Evidence-Basis Reset Checkpoint

Status: **STEP 1 TARGETED PO-003 INTEGRATION REQUIRED — CURRENT SENIOR REVIEW BASIS INVALIDATED**

Date: 2026-09-05

Pre-PO-003 review-ready basis:

`4cb19b178fcfcc08ef8f5bcf24e9f241cc0749fb`

Current domain:

> **Bootstrap / campaign creation / initial materialization**

New Product Owner input:

- `DEV/PRODUCT_OWNER_INPUT.md` — `PO-003`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`.

This checkpoint is process/design provenance. It does not replace the Product Owner semantic owner and does not authorize Step 2 or implementation.

---

## 1. Why the previous Step-1 gate is no longer current

Before PO-003 arrived, WP-19 Step 1 had incorporated PO-001/PO-002, rerun the mandatory whole-project Task-Brief critic and reached:

```text
WP19 STEP 1 COMPLETE — MANDATORY SENIOR REVIEW
```

PO-003 adds a material requirement directly affecting the retrospective/history consumer introduced by PO-001:

> later Master/Commentator retrospective explanation or replay of a material NPC decision must use the relevant Actor/knowledge/relationship basis as it existed at the historical event, rather than silently substituting later current state.

The previous Source Manifest, Architecture Task Brief and critic did not include this requirement. Under `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`, the prior review-ready claim is therefore invalidated only as far back as necessary.

---

## 2. Preserved prior work

The following remain valid unless new evidence directly contradicts them:

```text
PO-001 PRODUCT SEMANTICS:          RETAINED / INCORPORATED
PO-002 PRODUCT SEMANTICS:          RETAINED / INCORPORATED
PREVIOUS_F19_S1_FINDINGS:          RETAINED / CLOSED
SR19_01:                           RETAINED / CLOSED
SR19_02:                           RETAINED / CLOSED
F19_PO_01..F19_PO_06:              RETAINED ON THEIR PRE-PO-003 BASIS
```

PO-003 does not itself reopen R2.2, Step-4, R2.1, WP-10, WP-18 or another closed owner merely because the topics overlap.

---

## 3. Owner-approved PO-003 semantics

The current product constraint is:

```text
NO FULL NPC-PSYCHOLOGY HISTORY
NO PER-TURN FULL ACTOR SNAPSHOT

MATERIAL ACTOR DECISION / MATERIAL COGNITIVE TRANSITION
    -> retain bounded event-time decision basis when later explanation/replay may depend on mutable Actor-private or epistemic state
```

The relevant basis is situation-specific. The Product Owner does not require a fixed universal field set. The LLM may identify the eligible fields materially relevant to the particular event at decision time; exact deterministic validation, serialization and schema are downstream architecture questions.

Historical basis is evidence only. It must not become a second writable owner for current Actor cognition or `world.knowledge`, and it must not retain hidden chain-of-thought.

---

## 4. Mandatory Step-1 reconciliation questions

The targeted expanded Source Manifest / Task Brief / whole-project critic must determine from current owners and consumers:

1. whether accepted SemanticEvent/history evidence already preserves enough event-time Actor-private and epistemic basis;
2. whether the new requirement is `NEW CONSUMER`, `EXTENSION`, `MATERIAL INSUFFICIENCY`, or a combination by owner;
3. which native historical-evidence owner should retain the bounded basis if current contracts are insufficient;
4. how event-time values remain recoverable after mutable current Actor/knowledge/relationship state changes;
5. how R2.2 current cognition ownership remains separate from historical evidence;
6. how Step-4 `world.knowledge` current stance and existing transition history compose with the new basis;
7. whether WP-10 record-family completeness, Step-5.9 history/chronology, WP-13 durability/publication or other closed architecture actually requires reopening under the normal evidence threshold;
8. how R2.1/WP-18 Story and ordinary Master/Commentator retrospective consumers retrieve the basis without treating Story as authority;
9. how current player/principal/PC disclosure/no-spoiler eligibility still controls what historical motives may be revealed;
10. what direct acceptance scenarios are required where current NPC state differs materially from the event-time decision basis.

Do not assume a new record family, event schema or physical package before this evidence work establishes the correct owner boundary.

---

## 5. Current process state

```text
PO003_PRODUCT_SEMANTICS:             OWNER-APPROVED / INCORPORATED
PO003_WP19_STEP1_FRAMING:            PENDING
PO003_WHOLE_PROJECT_CRITIC:          PENDING / NOT STARTED
CURRENT_STEP1_REVIEW_READY:          NO
CURRENT_SENIOR_REVIEW:               INTERRUPTED BY NEW APPLICABLE PO INPUT / MUST RESTART ONLY AFTER UPDATED STEP-1 BASIS
HUMAN_DECISION_REQUIRED:             NO
NEEDS_PO:                            NONE
UPSTREAM_REOPEN_REQUIRED:            UNDETERMINED — EVIDENCE WORK REQUIRED
ARCHITECTURE_REOPENED:               NO
WP19_STEP2_AUTHORIZED:               NO
STEP2_STARTED:                       NO
WP20_STARTED:                        NO
IMPLEMENTATION_PLANNING_STARTED:     NO
SUBSTANTIVE_IMPLEMENTATION_STARTED:  NO
```

The next authorized unit is only the targeted WP-19 Step-1 PO-003 integration / Source-Manifest and Task-Brief repair / mandatory whole-project critic rerun. Senior review resumes only after that package is again review-ready.

No real gameplay/campaign bootstrap is authorized by this checkpoint.
