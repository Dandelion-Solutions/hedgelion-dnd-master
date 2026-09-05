# R2.7 WP-19 — Product-Owner Input Integration Checkpoint

Status: **STEP 1 PO-INPUT INTEGRATION COMPLETE — CRITIC RE-RUN COMPLETE — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Pre-input recovery basis: `6be4db0f4e68b91009f41462e6cb1d2eee790b19`

Expanded integration basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

Current domain:

> **Bootstrap / campaign creation / initial materialization**

Canonical Product Owner decision:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`.

This checkpoint is design/process provenance. It does not replace the semantic owner decision and does not authorize Step 2 or implementation.

---

## 1. Integration result

The Product Owner inputs that arrived after the recovered WP-19 Step-1 package have now been integrated into the current Source Manifest and Architecture Task Brief. The mandatory whole-project Task-Brief critic was rerun on the expanded basis.

Previous findings remain retained rather than reopened:

```text
PREVIOUS_F19_S1_FINDINGS: RETAINED / CLOSED
SR19_01:                  RETAINED / CLOSED
```

No new evidence contradicted their accepted dispositions.

Current expanded-basis finding result:

```text
F19_PO_01: BLOCKING    — CLOSED
F19_PO_02: SIGNIFICANT — CLOSED
F19_PO_03: SIGNIFICANT — CLOSED
F19_PO_04: SIGNIFICANT — CLOSED
F19_PO_05: SIGNIFICANT — CLOSED
F19_PO_06: MINOR       — CLOSED AS ROUTING / DOWNSTREAM VERIFICATION OBLIGATION

PO_INTEGRATION_BLOCKING:      1
PO_INTEGRATION_SIGNIFICANT:   4
PO_INTEGRATION_MINOR:         1
UNRESOLVED_BLOCKING:          0
UNRESOLVED_SIGNIFICANT:       0
```

---

## 2. PO-001 route status — retrospective/history in ordinary gameplay

```text
PRODUCT SEMANTICS OWNER:      INCORPORATED
WP19 STEP-1 FRAMING:          INCORPORATED
STORY/CONTINUITY OWNERS:      CONSUMED / NO REOPEN
TRUTH/KNOWLEDGE/DISCLOSURE:   CONSUMED / NO REOPEN
ORDINARY GAMEPLAY CONSUMER:   ROUTED TO LATER WP-19 AUDIT AFTER SENIOR GO
DIRECT ACCEPTANCE COVERAGE:   MISSING / ROUTED DOWNSTREAM
SUBSTANTIVE IMPLEMENTATION:   DEFERRED
```

Required framing now states:

- authorized active-player retrospective/history questions remain ordinary D&D Master gameplay;
- no Commentator transition is required;
- R2.3 purpose/player/PC eligibility precedes bounded history retrieval;
- R2.1/WP-18 Story may orient/rout retrieval but is not truth/currentness/knowledge/disclosure authority;
- material/current/source-specific claims escalate to stronger native owners;
- Step-4 / Step-5.12 disclosure/no-spoiler boundaries control player-visible output;
- no new memory/history owner is created.

Campaign interaction routing is explicit:

```text
active + gameplay allowed       -> ordinary gameplay
active + readable/non-playable  -> read-only Commentator
completed + readable            -> read-only Commentator
```

No additional mode hierarchy is introduced.

---

## 3. PO-002 route status — explicit save-and-exit to campaign selection

```text
PRODUCT SEMANTICS OWNER:      INCORPORATED
WP19 STEP-1 FRAMING:          INCORPORATED
SAVE/PERSISTENCE OWNERS:      CONSUMED / NO REOPEN
SESSION/RUNTIME CONSUMERS:    ROUTED TO LATER WP-19 AUDIT AFTER SENIOR GO
MENU/BOOTSTRAP CONSUMERS:     ROUTED TO LATER WP-19 AUDIT AFTER SENIOR GO
MULTIPLAYER/LIVE BOUNDARY:    ROUTED / NON-INTERFERENCE EXPLICIT
DIRECT ACCEPTANCE COVERAGE:   MISSING / ROUTED DOWNSTREAM
SUBSTANTIVE IMPLEMENTATION:   DEFERRED
```

Required composition is now explicit:

```text
explicit save-and-exit
    -> satisfy existing explicit-save durability promise
    -> applicable session/live closure or consolidation
    -> establish success
    -> terminate current gameplay context
    -> clear selected-campaign gameplay working binding
    -> return to existing campaign-selection/menu gate
```

The framing explicitly distinguishes this navigation intent from:

- `save and stop` / pause;
- `completed` / `archived`;
- multiplayer leave;
- PLAYER deactivation;
- PC-control transfer;
- mode/join-policy change;
- global campaign stop;
- closing a still-needed live epoch merely because one participant's chat exits.

The existing Step-5.5 / `EXPLICIT_SAVE_CASES:S08` `save and stop` semantics remain current only for a separately expressed stop/pause intent; they are not superseded, but they must not be generalized to exit-to-menu.

---

## 4. Verification evidence result

Current supporting cases were inspected:

- `REGRESSION_CASES:T04/T08` — knowledge separation + bounded historical retrieval;
- `AI_DM_CRAFT_CASES:ADC08` — eligible known context presentation;
- `EXPLICIT_SAVE_CASES:S07/S08/S15/S16` — save/pause distinction, stop qualifier, failure/success semantics;
- `MULTIPLAYER_MEMBERSHIP_CASES:M01/M10` — explicit membership leave/removal and live consequences;
- campaign-card/install menu cases — card-first presentation/selection and read-only hints.

No current direct end-to-end acceptance case covers the full PO-001 or PO-002 flow. This is recorded as `F19-PO-06 / MINOR` and routed to later authorized verification realization. No test file was changed during Step 1.

Previous SR19-01 stale/current scenario dispositions remain unchanged.

---

## 5. Product Owner / upstream gate

The expanded evidence was checked against the Product Owner decision categories.

```text
HUMAN_DECISION_REQUIRED:  NO
NEEDS_PO:                 NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED:    NO
```

The new inputs are new consumer/product requirements with already-supplied semantics. Current owner composition is technically sufficient for Step-1 framing; exact downstream realization remains agent-owned after later gates.

---

## 6. Current stop state

```text
WP19_STEP1_STATUS:                 COMPLETE — MANDATORY SENIOR REVIEW
WP19_STEP2_AUTHORIZED:            NO
STEP2_STARTED:                    NO
CURRENT_SENIOR_REVIEW:            NOT STARTED
WP20_STARTED:                     NO
IMPLEMENTATION_PLANNING_STARTED:  NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```

The current worker stops after publication/read-back/verification. The next authorized process action is the **mandatory Senior review of the expanded WP-19 Step-1 package**. This checkpoint does not perform that review and does not grant Step-2 GO.