# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Whole-Project Task-Brief Critic

Status: **STEP 1 CRITIC RE-RUN COMPLETE — PO INPUT INTEGRATED — MANDATORY SENIOR REVIEW CANDIDATE**

Date: 2026-09-05

Original critic basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

Expanded Product-Owner integration basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

This is the mandatory whole-project Step-1 Task-Brief critic rerun required after `PO-001` and `PO-002` arrived after the prior recovered critic basis. The rerun follows `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`: pre-input findings remain valid for their basis, but the old critic cannot clear a package containing later Product Owner requirements until those routes are independently inspected and incorporated.

The rerun used current `DEV/PROJECT_MAP.md`, the PO ledger/process/accepted owner decision, current canonical owners, runtime consumers and directly implicated tests/scenario catalogs. It did not treat the PO integration checkpoint or prior critic as an answer key.

---

## 1. Independent reconstruction method

The pre-input bootstrap/materialization and SR19-01 verification graph was retained. The critic independently added two consumer legs.

### PO-001 leg

```text
selected campaign
    -> lifecycle + access authority
    -> active + gameplay allowed
    -> ordinary gameplay / OOC Master interaction
    -> retrospective/history intent
    -> R2.3 purpose/player/PC eligibility + bounded retrieval
    -> R2.1 / WP-18 Story-history orientation when eligible
    -> stronger native/current owner escalation when required
    -> Step-4 world.knowledge/runtime.disclosure
    -> Step-5.12 player-visible eligibility
    -> R2.4 ordinary Narrator-visible response
```

The critic separately followed the read-only branch:

```text
active + readable but gameplay denied -> Commentator
completed + readable                  -> Commentator
```

This establishes that Commentator is not an extra history mode for an authorized active player.

### PO-002 leg

```text
explicit save-and-exit
    -> Step-5.5 / SAVE_CONTRACT explicit save promise
    -> PERSISTENCE / DURABILITY_GUARD
    -> SESSION + applicable LIVE_SCENE closure/consolidation
    -> save success established
    -> RUNTIME selected gameplay context termination
    -> clear selected-campaign working binding
    -> BOOTSTRAP_RUNTIME / install campaign-menu re-entry
    -> CAMPAIGN_CARD presentation + ACCESS_CONTROL revalidation
    -> next explicit campaign choice
```

The critic also followed negative neighbors:

```text
save-and-stop/pause
multiplayer leave/deactivation
PC control transfer
campaign completion/archive
live epoch close/global multiplayer stop
```

These remain independently owned operations and are not implied by exit-to-menu.

---

## 2. Findings summary

The original Step-1 findings and SR19-01 remain closed. No new evidence contradicts their dispositions.

Expanded PO-input critic findings:

```text
PO_INTEGRATION_BLOCKING:       1
PO_INTEGRATION_SIGNIFICANT:    4
PO_INTEGRATION_MINOR:          1

UNRESOLVED_BLOCKING:           0
UNRESOLVED_SIGNIFICANT:        0
HUMAN_DECISION_REQUIRED:       NO
UPSTREAM_REOPEN_REQUIRED:      NO
ARCHITECTURE_REOPENED:         NO
STEP2_STARTED:                 NO
WP19_STEP2_AUTHORIZED:         NO
WP20_STARTED:                  NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```

All BLOCKING/SIGNIFICANT defects below were mechanically resolvable framing/consumer-routing defects and are repaired in the Source Manifest and Task Brief. No genuine `NEEDS_PO` remained.

---

## 3. Previously closed findings — retained, not reopened

```text
F19-S1-01 BLOCKING    CLOSED — exact ruleset-set propagation framing
F19-S1-02 BLOCKING    CLOSED — scaffold/provisional/READY_PC/PLAY_READY separation
F19-S1-03 SIGNIFICANT CLOSED — branch/storage/access/stale-v2 reconciliation
F19-S1-04 SIGNIFICANT CLOSED — identity/card/config/current projections
F19-S1-05 SIGNIFICANT CLOSED — first-publication vs later durability/session/resume
F19-S1-06 SIGNIFICANT CLOSED — multiplayer initial authority
F19-S1-07 SIGNIFICANT CLOSED — bidirectional machine/template/schema/test audit
F19-S1-08 MINOR       CLOSED — WP-20/dormant-neighbor boundary
SR19-01   SIGNIFICANT CLOSED — verification/scenario reverse-conformance evidence expansion
```

PO-001/PO-002 add consumers around the existing owners. They do not establish a contradiction that would reopen those findings.

---

## 4. Expanded-basis finding dispositions

### F19-PO-01 — BLOCKING — applicable accepted Product Owner semantics absent from the pre-input Step-1 frame

**Defect**

The pre-input Source Manifest/Task Brief/critic were valid for their inspected basis but did not contain the later accepted owner decision for:

1. retrospective/history interaction inside ordinary active gameplay;
2. save-and-exit navigation back to campaign selection;
3. the explicit campaign routing table separating ordinary gameplay from read-only Commentator.

A Step-1 package that omitted an applicable current owner decision could not safely authorize Step-2 research because the Step-2 problem statement itself would be incomplete.

**Resolution**

CLOSED. The Source Manifest now treats the PO ledger as intent evidence, the Product Owner Input Process as process authority, and `2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` as the accepted semantic owner. The Task Brief contains the exact interaction and exit contracts and new evidence questions.

**Human decision required:** NO — the Product Owner already supplied the semantics.

---

### F19-PO-02 — SIGNIFICANT — retrospective consumer could be misrouted to Commentator or use Story as disclosure authority

**Defect**

Without an explicit consumer binding, older role topology could be read as “history => Commentator”, and a weak implementation could answer directly from Story/repository-visible history without current player/PC disclosure eligibility.

That would violate the new product requirement and existing Step-4/R2.1/R2.3/WP-18 ownership:

- authorized active-player retrospective is ordinary gameplay;
- Story is noncanonical orientation/routing, not truth/currentness/knowledge/disclosure;
- eligibility precedes retrieval/use;
- material/current/source-specific claims escalate to stronger owners;
- player-visible output remains disclosure-filtered.

`R2.4` saying Commentator is a separate mode is not a contradiction. It remains correct for spectator/read-only serving and is now explicitly qualified so it cannot become a mandatory history transition for an authorized active player.

**Resolution**

CLOSED. The manifest/brief now route PO-001 through `RUNTIME`/OOC Master interaction, R2.3 bounded context retrieval, R2.1/WP-18 Story orientation, Step-4 knowledge/disclosure, Step-5.12 delivery and ordinary Narrator-visible output. They explicitly forbid a new memory/history owner and forbid Story availability from creating disclosure authority.

**Upstream reopen:** NO.

---

### F19-PO-03 — SIGNIFICANT — post-selection interaction routing was under-specified

**Defect**

The pre-input WP-19 frame strongly specified campaign discovery/selection but not the newly owner-approved interaction route after selection:

```text
active + gameplay allowed       -> ordinary gameplay
active + readable/non-playable  -> read-only Commentator
completed + readable            -> read-only Commentator
```

Without this route, a future consumer could infer ordinary gameplay merely from `active`, or treat completed/read-only campaigns as resumable, or add an unnecessary extra mode-selection hierarchy.

**Resolution**

CLOSED. The routing table is now a Task-Brief invariant. Lifecycle and access owners provide authoritative facts; card status/login fields remain presentation hints requiring authoritative revalidation after selection. No additional mode hierarchy is admitted.

**Human decision required:** NO.

---

### F19-PO-04 — SIGNIFICANT — save-and-exit ordering/failure boundary was missing

**Defect**

The existing save stack proves what `save` means and how durability/publication works, but the pre-input frame did not define the new ordered navigation composition. A weak implementation could clear selected gameplay context before required save closure succeeds, then either lose promised state or falsely claim save/exit success.

**Resolution**

CLOSED in framing:

```text
explicit save-and-exit
    -> establish existing save promise across applicable native domains
    -> perform applicable session/live closure/consolidation
    -> only after successful required closure terminate selected gameplay context
    -> clear selected-campaign working binding
    -> enter the existing campaign-selection/menu gate
```

Failure preserves/adopts the strongest truthful recovery-safe context/frontier and may not report the combined operation successful.

No new persistence authority is created.

---

### F19-PO-05 — SIGNIFICANT — exit, stop/pause, membership leave and live closure could be conflated

**Defect**

Current Step-5.5 §4.4 and `EXPLICIT_SAVE_CASES:S08` correctly define `save and stop` as save plus a separately intended stop/pause lifecycle/session action. `MULTIPLAYER_MEMBERSHIP_CASES:M01/M10` separately define membership leave/removal and its live consequences.

The new product command “save and exit to campaign selection” is different. Without an explicit qualifier, future work could incorrectly:

- set `paused` merely because the player exits to menu;
- deactivate PLAYER membership;
- transfer/relinquish PC control;
- close/stop a campaign or still-needed live epoch for other participants.

`LIVE_SCENE.md` provides decisive negative evidence: do not close an epoch merely because one player's chat ended while differently controlled PCs still share the actionable scene.

**Resolution**

CLOSED. The Task Brief now distinguishes the intents and forbids all listed implicit side effects. Applicable save-driven live consolidation remains native-owner-controlled; exit itself does not create membership/lifecycle/global-live authority.

**Upstream reopen:** NO — the later Product Owner decision composes/qualifies consumers without contradicting the existing owners.

---

### F19-PO-06 — MINOR — direct end-to-end acceptance cases for PO-001/PO-002 are absent

**Evidence**

Current tests/scenarios cover important pieces:

- `REGRESSION_CASES:T04/T08` — knowledge separation and bounded old-history retrieval;
- `EXPLICIT_SAVE_CASES:S07/S15/S16` — save does not pause, failure is not success, dirty state clears after successful save;
- `S08` — true save+stop intent;
- `MULTIPLAYER_MEMBERSHIP_CASES:M01/M10` — explicit leave/removal distinct from ordinary session exit;
- campaign-card/install cases — menu/choice presentation and read-only hints.

But no current case directly verifies the whole new PO-001 or PO-002 flow.

**Disposition:** CLOSED AS STEP-1 ROUTING / DOWNSTREAM VERIFICATION OBLIGATION. The Source Manifest explicitly records the gap and the Task Brief requires later acceptance mapping. Tests are not rewritten in Step 1 because that would be premature design realization/implementation-adjacent work.

---

## 5. Verification/scenario item-level PO dispositions

### PO-001

| Evidence | Disposition |
|---|---|
| `REGRESSION_CASES:T04` | CURRENT SUPPORTING — prevents knowledge leak; not full retrospective routing proof. |
| `REGRESSION_CASES:T08` | CURRENT SUPPORTING — bounded old-NPC history retrieval; not full disclosure/interaction proof. |
| `AI_DM_CRAFT_CASES:ADC08` | CURRENT SUPPORTING — eligible known context may be stated directly. |
| direct active-player retrospective/no-Commentator acceptance | MISSING / ROUTED DOWNSTREAM. |

### PO-002

| Evidence | Disposition |
|---|---|
| `EXPLICIT_SAVE_CASES:S07` | CURRENT — save alone does not pause. |
| `EXPLICIT_SAVE_CASES:S08` | CURRENT WITH QUALIFIER — only when stop/pause intent is separately present; not exit-to-menu semantics. |
| `EXPLICIT_SAVE_CASES:S15/S16` | CURRENT — no false success; successful save adopts durable frontier/clears dirty set. |
| `MULTIPLAYER_MEMBERSHIP_CASES:M01` | CURRENT — membership leave is an explicit distinct transition. |
| `MULTIPLAYER_MEMBERSHIP_CASES:M10` | CURRENT — live freeze/compaction belongs to actual membership removal, not ordinary exit. |
| card/install menu cases | CURRENT SUPPORTING — existing menu/choice contract; same-chat exit re-entry is a new consumer. |
| direct save-success -> context-clear -> same-chat menu with no side effects acceptance | MISSING / ROUTED DOWNSTREAM. |

The earlier SR19-01 stale scenario dispositions remain unchanged and closed.

---

## 6. Product Owner boundary rerun

The expanded critic explicitly retested all human-owned categories.

### Product semantics

Already supplied by `PO-001`/`PO-002` and the accepted owner decision. No residual alternative remains for the agent to choose.

### Canonical authority / ownership

No new owner allocation is required:

- Story/continuity/history remain existing R2.1/WP-18 projection/retrieval concerns;
- truth/knowledge/disclosure remain Step-4/Step-5.12 owners;
- context retrieval remains R2.3;
- ordinary gameplay role execution remains R2.4/runtime;
- save/durability/publication/session remain existing Step-5.5/CORE owners;
- access/membership/control/live concurrency remain their existing owners;
- menu/card remains existing bootstrap/projection authority.

### Meaningful compatibility policy

No change. WP-20 remains future released-campaign migration/evolution.

### Hard-to-reverse lifecycle/product behavior

The Product Owner explicitly settled the material distinction: exit-to-menu is context navigation and does not itself mutate campaign lifecycle/membership/control/global multiplayer state.

### Material quality trade-off

No unresolved trade-off remains. Natural retrospective interaction and explicit safe return-to-menu are required product semantics, not optional optimization choices.

### Explicit risk acceptance

No new risk acceptance is required.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

---

## 7. Closed-upstream review

The critic found no real contradiction/material insufficiency requiring upstream reopen:

- PO-001 is compatible with R2.1/R2.3/WP-18 because Story was already designed as bounded nonauthoritative orientation and stronger-source routing;
- PO-001 is compatible with Step-4/Step-5.12 because disclosure eligibility remains controlling;
- R2.4 Commentator separation is qualified by consumer routing, not invalidated;
- PO-002 is compatible with Step-5.5/SAVE_CONTRACT because save remains unchanged and navigation occurs after it;
- `save and stop` remains valid for a true stop/pause intent and is not redefined;
- membership/live owners already distinguish explicit leave/removal from chat/session termination;
- existing menu/selection owners can be reused as the return destination without creating a second authority.

```text
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO
```

---

## 8. Expanded Step-1 critic gate

```text
PREVIOUS F19-S1-*:           RETAINED / CLOSED
SR19-01:                     RETAINED / CLOSED

F19-PO-01 BLOCKING:          CLOSED — accepted PO semantics integrated into current Step-1 basis
F19-PO-02 SIGNIFICANT:       CLOSED — ordinary retrospective consumer + eligibility/no-Commentator route framed
F19-PO-03 SIGNIFICANT:       CLOSED — campaign selection interaction routing made explicit
F19-PO-04 SIGNIFICANT:       CLOSED — save-before-exit ordering/failure boundary framed
F19-PO-05 SIGNIFICANT:       CLOSED — exit separated from pause/leave/control/global live effects
F19-PO-06 MINOR:             CLOSED AS ROUTING — direct acceptance gaps recorded downstream

PO_INTEGRATION_BLOCKING:     1
PO_INTEGRATION_SIGNIFICANT:  4
PO_INTEGRATION_MINOR:        1
UNRESOLVED_BLOCKING:         0
UNRESOLVED_SIGNIFICANT:      0
HUMAN_DECISION_REQUIRED:     NO
UPSTREAM_REOPEN_REQUIRED:    NO
ARCHITECTURE_REOPENED:       NO
WP19_STEP2_AUTHORIZED:       NO
STEP2_STARTED:               NO
WP20_STARTED:                NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```

### Critic recommendation to Senior

The expanded Step-1 package now incorporates `PO-001`/`PO-002`, independently covers their current owner/consumer/test graph, distinguishes all material intent/authority boundaries, and has no unresolved BLOCKING/SIGNIFICANT framing defect or human-owned decision.

**Recommendation:** return the completed expanded WP-19 Step-1 package to the mandatory Senior review gate. This critic does not grant Step-2 GO and does not perform Senior review itself.