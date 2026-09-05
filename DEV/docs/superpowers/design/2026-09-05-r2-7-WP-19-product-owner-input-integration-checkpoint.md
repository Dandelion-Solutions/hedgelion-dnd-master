# R2.7 WP-19 — Product-Owner Input Integration Checkpoint

Status: **STEP 1 TARGETED PO-INPUT INTEGRATION — SENIOR REVIEW NOT READY — CRITIC RE-RUN PENDING**

Date: 2026-09-05

Pre-input public basis: `6be4db0f4e68b91009f41462e6cb1d2eee790b19`

Current domain:

> **Bootstrap / campaign creation / initial materialization**

This checkpoint records a new owner-approved product-semantics input that arrived after the previously recovered WP-19 Step-1 package and before its mandatory Senior re-review.

Canonical Product Owner decision:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`.

This checkpoint is design/process provenance. It does not replace the semantic owner decision above and does not itself create gameplay authority.

---

## 1. Why the prior Step-1 gate state is no longer review-ready

Immediately before this input, WP-19 Step 1 was recorded as recovered and ready for mandatory Senior re-review after closure of `SR19-01`.

That previous result remains valid for the evidence graph it actually inspected, including all closed `F19-S1-*` and `SR19-01` dispositions. None of those findings is reopened by this checkpoint.

However, the new Product Owner decision adds two explicit current consumers that were not part of the basis of the existing Task-Brief critic:

1. ordinary active-gameplay retrospective/history interaction under player/PC disclosure eligibility;
2. explicit save-and-exit navigation from selected gameplay back to campaign selection.

Therefore:

```text
OLD STEP-1 FINDINGS:              RETAINED / NOT REOPENED
OLD SR19-01 RECOVERY:             RETAINED / CLOSED
OLD TASK-BRIEF CRITIC:            VALID FOR ITS PRE-INPUT BASIS ONLY
CURRENT STEP-1 REVIEW READINESS:  NO
CURRENT CRITIC RE-RUN:            REQUIRED
STEP 2:                           BLOCKED
SENIOR REVIEW:                    NOT STARTED FOR EXPANDED BASIS
REPAIR BRIEF:                     NOT AUTHORED
IMPLEMENTATION:                   NOT AUTHORIZED
```

The prior critic must not be presented as clearing the expanded current Step-1 package merely because it previously had zero unresolved blocking/significant findings.

---

## 2. Requirement classification

### PO19-A — ordinary gameplay retrospective/history interaction

Disposition:

```text
NEW EXPLICIT PRODUCT / CONSUMER REQUIREMENT
NO NEW STORY/TRUTH/KNOWLEDGE/DISCLOSURE AUTHORITY
NO COMMENTATOR TRANSITION FOR AN AUTHORIZED ACTIVE PLAYER
NO UPSTREAM REOPEN PRESUMED
```

Current owners/consumers that must enter the WP-19 dependency graph include at minimum:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` where player-facing disclosure semantics matter;
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` and its final Senior amendment where applicable;
- `GAME/CORE/RUNTIME.md`;
- applicable `GAME/CORE/INFORMATION.md`, `NARRATIVE.md` and history/Story-routing consumers discovered from the current project map;
- directly implicated tests/scenario catalogs.

The audit question is consumer realization and instruction composition, not whether Story should become canon or whether a new history subsystem should exist.

### PO19-B — explicit save-and-exit back to campaign selection

Disposition:

```text
NEW EXPLICIT PRODUCT / NAVIGATION REQUIREMENT
COMPOSE EXISTING SAVE + SESSION + CAMPAIGN-SELECTION OWNERS
NO NEW CAMPAIGN LIFECYCLE ENUM
NO AUTOMATIC MULTIPLAYER MEMBERSHIP LEAVE
NO GLOBAL CAMPAIGN PAUSE IMPLIED
```

Current owners/consumers that must enter the WP-19 dependency graph include at minimum:

- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/MULTIPLAYER.md` and live/session neighbors when the selected campaign is multiplayer;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`;
- campaign-menu/card/access owners already in the WP-19 manifest;
- directly implicated persistence/session/bootstrap/menu/multiplayer tests and scenario catalogs.

The audit must distinguish current gameplay-context/session exit from `paused`, `completed`, `archived`, PLAYER deactivation, PC-control transfer and campaign membership leave.

---

## 3. Required Source-Manifest amendment

The current WP-19 Source Manifest remains the base manifest for its already-audited dependency graph.

Before Step 1 can be review-ready again, the manifest must be expanded so that the new Product Owner decision is a **CANONICAL OWNER DECISION / PRODUCT INPUT** and the two new consumer subgraphs above are explicitly inspected and dispositioned.

The manifest must also search the current test/scenario graph for requirements that would accidentally:

- route an active authorized player into Commentator for history questions;
- bypass player/PC knowledge/disclosure eligibility during retrospective recall;
- treat Story/repository visibility as disclosure authority;
- make `save and exit` synonymous with campaign pause or multiplayer leave;
- make a new chat the only valid route back to campaign selection;
- discard dirty promised state before requested save completion.

This checkpoint does not claim that search/inspection has been completed.

---

## 4. Required Architecture Task-Brief amendment

Before the next critic run, the WP-19 Architecture Task Brief must explicitly include the following current product constraints.

### 4.1 Campaign selection and interaction routing

```text
visible selected campaign
    + active
    + gameplay participation allowed
        -> ordinary gameplay

visible selected campaign
    + active
    + gameplay participation not allowed
        -> read-only Commentator

visible selected campaign
    + completed
        -> read-only Commentator
```

No extra Commentator transition is required for an authorized active player to inspect/discuss history.

### 4.2 Retrospective gameplay consumer

The normal Master must support bounded retrospective/history questions during active gameplay and answer only from information eligible for the current player/PC/role purpose, using existing continuity/history owners and proper-source escalation where required.

### 4.3 Explicit save-and-exit navigation

An explicit save-and-exit intent must compose:

```text
existing explicit-save contract
+ applicable session/live closure
+ current gameplay-context exit
+ selected-campaign context clear
+ campaign-selection/menu re-entry
```

without inventing a new lifecycle/membership state.

### 4.4 Additional Step-2 evidence questions

After Senior GO, Step-2 analysis must be able to answer at least:

1. Which runtime interaction owner recognizes retrospective/history intent during ordinary gameplay?
2. Which registered context purpose/consumer requirements guarantee Story/history retrieval cannot bypass player/PC knowledge/disclosure eligibility?
3. When Story is insufficient or a claim is material/current/source-specific, what existing owner-escalation route supplies stronger evidence?
4. Which instruction surfaces guarantee an active authorized player remains in ordinary gameplay rather than entering Commentator merely to ask about history?
5. Which exact save/session/live boundaries must complete before a requested save-and-exit may be reported successful?
6. How is the current selected-campaign gameplay context cleared without mutating campaign lifecycle or multiplayer membership accidentally?
7. How does the existing campaign-choice/menu gate re-enter in the same chat after explicit exit?
8. What differs for singleplayer versus multiplayer session exit, and what does not change?
9. Which tests/scenario expectations verify these semantics, and which existing expectations are stale or missing?

This checkpoint does not perform that Step-2 analysis.

---

## 5. Product Owner decision status

The product semantics themselves are settled by the canonical owner decision. No additional Product Owner trade-off is currently open merely to integrate them into WP-19 framing.

```text
HUMAN_DECISION_REQUIRED_FOR_PO19_A: NO — SEMANTICS SUPPLIED BY PRODUCT OWNER
HUMAN_DECISION_REQUIRED_FOR_PO19_B: NO — SEMANTICS SUPPLIED BY PRODUCT OWNER
TECHNICAL_OWNER_RECONCILIATION:     AGENT-OWNED
NEW_UPSTREAM_REOPEN:                NOT ESTABLISHED
```

If later evidence reveals a real contradiction, meaningful product trade-off, new canonical authority choice, hard-to-reverse lifecycle choice or explicit risk decision, the normal HDM human-decision gate applies.

---

## 6. Exact stop point requested for this checkpoint

This publication intentionally stops before the work that would complete Step 1 again.

Not performed here:

- no rerun of the whole-project Task-Brief critic;
- no Senior review of the expanded Step-1 package;
- no repair assignment/repair brief;
- no Step 2;
- no WP-20;
- no implementation planning;
- no substantive runtime/schema/template/test implementation;
- no real gameplay/campaign bootstrap.

The next architecture action, when explicitly resumed, is to integrate this checkpoint into the base Source Manifest/Task Brief as needed, independently reconstruct the expanded dependency/test graph, rerun the mandatory whole-project Task-Brief critic, mechanically repair any framing defects it finds, and only then return a complete Step-1 package to the mandatory Senior gate.