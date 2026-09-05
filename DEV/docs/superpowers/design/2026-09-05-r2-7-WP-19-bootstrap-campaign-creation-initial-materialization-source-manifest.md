# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Source Manifest

Status: **STEP 1 COMPLETE — PO INPUT INTEGRATED — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Original Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

Product-Owner integration basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

Domain:

> **Bootstrap / campaign creation / initial materialization**

This manifest is the task-specific evidence route required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It preserves the previously recovered WP-19 bootstrap/materialization and verification graph, then integrates the applicable Product Owner inputs `PO-001` and `PO-002` and their accepted semantic owner.

The Product Owner inputs add current consumers around campaign entry/interaction/exit. They do not authorize Step 2, WP-20, implementation planning, gameplay bootstrap, or substantive runtime/schema/template/test implementation. Previously closed `F19-S1-*` findings and `SR19-01` remain closed unless new contradictory evidence says otherwise; none was found in this integration pass.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md`.

---

## 1. Discovery route

The integrated WP-19 dependency graph is:

```text
current progress / Product Owner input process / PO ledger
    -> accepted PO-001 / PO-002 owner decision
    -> campaign discovery / explicit selection
        -> selected active + gameplay allowed
             -> ordinary D&D Master gameplay
             -> retrospective/history question when requested
                  -> ordinary gameplay intent/OOC interaction
                  -> R2.3 bounded history/context assembly
                  -> R2.1 + WP-18 Story/continuity orientation where eligible
                  -> stronger current/native owner escalation when material/current/source-specific
                  -> world.knowledge + runtime.disclosure + Step-5.12 output eligibility
                  -> Narrator/player-facing response
        -> selected active + readable but gameplay denied
             -> read-only Commentator
        -> selected completed + readable
             -> read-only Commentator

new campaign branch
    -> storage v3 baseline
    -> exact runtime/ruleset package
    -> init_campaign materializer
    -> initial campaign tree/publication
    -> initializing / provisional / READY_PC / PLAY_READY
    -> active gameplay

explicit save-and-exit intent from selected gameplay
    -> existing explicit-save promise / required native durability closure
    -> persistence + applicable session/live closure
    -> save success must be established
    -> terminate current gameplay context
    -> clear selected-campaign gameplay binding/working context
    -> campaign-selection/menu re-entry in the same chat
    -> next explicit campaign choice
```

The graph was reconstructed through current `DEV/PROJECT_MAP.md`, accepted owners, runtime consumers and `DEV/TESTS`. The Senior-provided earlier SR19-01 test list and the Product Owner integration checkpoint were routing aids, not answer keys.

Two evidence rules remain explicit:

```text
TEST EXISTS / CI GREEN != EXPECTATION IS CURRENT ARCHITECTURE
PRODUCT OWNER LEDGER ENTRY != ACCEPTED ARCHITECTURE OWNER
```

The ledger preserves intent. The canonical owner decision supplies accepted product semantics. Runtime/spec/schema/test consumers remain subordinate to their actual semantic owners.

---

## 2. Source-role manifest

### 2.1 Process, state and Product Owner input

| Source | Role | WP-19 disposition |
|---|---|---|
| `AGENTS.md` | CANONICAL repository process | Current repository/process constraints. |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | REQUIRED runtime overlay | Connector-only remote work/publication/verification. |
| `DEV/DESIGN_PROCESS.md` | CANONICAL development process | Source Manifest, item-level evidence, critic and human-decision gates. |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM adapter | Mandatory whole-project Step-1 critic and Senior stop. |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | CANONICAL process addendum | PO input routing, mid-stage critic invalidation, NEEDS_PO discipline. |
| `DEV/PRODUCT_OWNER_INPUT.md` | PRODUCT OWNER INTENT / ROUTING LEDGER | `PO-001`, `PO-002`, shared immutable Product Owner context. Intent evidence, not architecture authority. |
| `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` | CANONICAL OWNER DECISION | Accepted PO-001/PO-002 semantics and campaign interaction routing. |
| `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md` | DESIGN PROVENANCE / TASK CURSOR | Explains why pre-input critic could not clear expanded Step 1 and enumerates required integration graph. |
| `DEV/CURRENT_PROGRESS.md` | CANONICAL global progress | Current authorized unit/gate; Step 2 blocked. |
| `DEV/PROJECT_MAP.md` | DERIVATIVE routing index | Used to independently rebuild bootstrap, gameplay-information, save/session/menu, access/live and verification routes. |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | DERIVATIVE locator | Owner discovery only. |
| R2.7 program brief/scope discovery/owner clarification | PROGRAM EVIDENCE / OWNER DECISION | Whole-project bidirectional audit, clean-slate unreleased scaffold, WP-20 future-evolution boundary. |

### 2.2 Existing bootstrap / creation / initial materialization owners — retained

| Source family | Role / retained disposition |
|---|---|
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md` | Entry, package/storage discovery, explicit choice, card-first menu, exact runtime routing. CURRENT. |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md`, `GAME/CORE/CAMPAIGN_SETUP.md`, `GAME/TOOLS/init_campaign.py` | Scaffold-first New Game ordering, setup, exact materializer. CURRENT, with previously recorded ruleset-argument prose defect retained under `F19-S1-01`. |
| `GAME/CORE/STORAGE.md`, `GAME/SCHEMA/dnd_storage.schema.yaml` | Storage v3 baseline authority. CURRENT. |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md`, `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | Branch/root/creator/access laws; stale Storage-v2 wording remains qualified/superseded where later owners conflict. |
| ruleset package identity/machine closure, `DEV/TOOLS/release_builder.py`, release integration tests | Exact package/ruleset identity chain. CURRENT. |
| `GAME/CAMPAIGN/` + manifest/card/config/current templates and schemas | Current generated campaign topology/projections. CURRENT subject to native-owner/projection boundaries. |
| character readiness / diegetic onboarding / durability / session owners | Scaffold -> provisional -> READY_PC -> PLAY_READY -> active distinction. CURRENT. |
| multiplayer / House-Rules neighbors | Inherited closed owners; no reopen from creation consumption alone. |

### 2.3 PO-001 — ordinary gameplay retrospective/history owner graph

| Source | Role | Disposition for PO-001 |
|---|---|---|
| canonical PO owner decision | PRODUCT SEMANTICS OWNER | Authorized active player retrospective/history questions remain ordinary D&D Master gameplay; no Commentator transition. CURRENT. |
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | TRUTH / KNOWLEDGE / DISCLOSURE / ROLE-CONTEXT OWNER | Repository/Story visibility does not grant disclosure; `world.knowledge` and `runtime.disclosure` remain controlling. CURRENT. |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | PLAYER-VISIBLE DISCLOSURE/EMISSION OWNER | Player-facing eligibility validated before emission; historical re-presentation remains evidence-bound. CURRENT. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` | CONTINUITY/HISTORY RETRIEVAL OWNER | Story is bounded orientation/routing, not canon/currentness/knowledge/disclosure; material claims escalate. CURRENT. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | CONTEXT ASSEMBLY OWNER | Purpose/player/PC/role eligibility precedes historical retrieval; bounded progressive history retrieval; no whole-history fallback. CURRENT. |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | ORDINARY TURN/ROLE EXECUTION OWNER | Ordinary gameplay uses Narrator-visible path; Commentator remains a separate spectator/read-only concern. **CURRENT WITH QUALIFIER:** “Commentator separate mode” must not be interpreted as requiring an authorized active player to leave ordinary gameplay for retrospective questions. |
| `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` + final amendment | FINAL STORY/CONTINUITY OWNER | Story remains noncanonical retrospective projection; Continuity remains derived; Story presence does not create truth/knowledge/disclosure authority. CURRENT. |
| `GAME/CORE/RUNTIME.md` | ORDINARY GAMEPLAY INTERACTION CONSUMER | Current OOC `Master` channel permits direct Master discussion without advancing fiction; exact retrospective consumer mapping is a WP-19 downstream realization question. |
| `GAME/CORE/PLAY_POLICY.md` | GAMEPLAY ACTIVATION/INTENT POLICY | Ordinary player intent is interpreted inside gameplay; no engine-maintenance or external-history mode is implied. CURRENT supporting consumer. |
| `GAME/CORE/INFORMATION.md` | INFORMATION CONSUMER | Separates truth, PC/NPC knowledge and player disclosure; focused questions answer only what is determinable/eligible. CURRENT. |
| `GAME/CORE/NARRATIVE.md` | NARRATOR CONSUMER | Visible narration projects resolved/eligible state and respects agency; no authority to invent history. CURRENT. |

**PO-001 owner conclusion:** this is a **NEW CONSUMER BINDING / EXTENSION**, not a new memory/history owner and not an upstream contradiction. The existing Story/history stack supplies bounded evidence; current knowledge/disclosure owners control what may be said.

### 2.4 PO-002 — explicit save-and-exit owner graph

| Source | Role | Disposition for PO-002 |
|---|---|---|
| canonical PO owner decision | PRODUCT/NAVIGATION SEMANTICS OWNER | Save succeeds first, then current gameplay context exits and same-chat campaign selection resumes. Exit alone does not mutate campaign lifecycle/membership/control. CURRENT. |
| Step-5.5 canonical durability spec | LOGICAL SAVE DURABILITY OWNER | Explicit save promise/closure remains current. **CURRENT WITH QUALIFIER:** §4.4 `save and stop` means save + separately intended stop/pause lifecycle action; it is not synonymous with new `save and exit to campaign selection` navigation intent. |
| `GAME/CORE/SAVE_CONTRACT.md` | RUNTIME EXPLICIT SAVE OWNER | SAVE_ALL_DIRTY, completeness, no false save acknowledgement, save alone does not pause. CURRENT; new exit consumer composes after successful save. |
| `GAME/CORE/PERSISTENCE.md` | PUBLICATION TRANSPORT OWNER | HOW native campaign publication occurs. CURRENT; no new publication authority. |
| `GAME/CORE/DURABILITY_GUARD.md` | WHEN / DURABILITY BOUNDARY OWNER | Save/session boundaries flush required state; save does not manufacture readiness or pause. CURRENT. |
| `GAME/CORE/SESSION.md` | SESSION/RECOVERY OWNER | Session boundary/closure and resume semantics. CURRENT; same-chat campaign-selection re-entry is a new WP-19 consumer composition. |
| `GAME/CORE/RUNTIME.md` | GAMEPLAY CONTEXT OWNER/CONSUMER | Current selected gameplay context must terminate/clear only after required save/session closure succeeds. New consumer mapping required later. |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/INSTALL/00_DND_BOOTSTRAP.md` | CAMPAIGN SELECTION/MENU OWNER | Card-first campaign menu and explicit choice gate. **EXTENDED CONSUMER:** same menu/selection state must be reusable after in-chat exit, not only at new-chat entry. |
| `GAME/CORE/CAMPAIGN_CARD.md` | MENU PROJECTION OWNER | Card provides menu hints only; active/read-only/completed rows remain projection, not authorization. CURRENT. |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | AUTHORIZATION OWNER | Active gameplay eligibility vs readable observer access remains authoritative after selection. CURRENT. |
| `GAME/CORE/MULTIPLAYER.md` | MEMBERSHIP/SHARED-WORLD OWNER | PLAYER leave/deactivation is a separate explicit operation. Exit-to-menu does not deactivate or transfer control. CURRENT. |
| `GAME/CORE/LIVE_SCENE.md` | ACTIVE LIVE EPOCH OWNER | Explicit save may require durable consolidation, but **do not close an epoch merely because one player chat ends** while shared scene remains concurrently addressable. Exit must not become global multiplayer stop. CURRENT. |

**PO-002 owner conclusion:** this is a **NEW NAVIGATION CONSUMER COMPOSITION**, not a new lifecycle enum or membership transition. Save success is a prerequisite to successful save-and-exit acknowledgement; failure must preserve the strongest recovery-safe current context and must not falsely claim both save and exit succeeded.

### 2.5 Verification / scenario graph — retained SR19-01 dispositions

The prior SR19-01 reverse-conformance expansion remains valid. Material retained dispositions include:

| Expectation | Disposition |
|---|---|
| `BOOTSTRAP_STORAGE_REGRESSION_CASES.md:B12` Storage v2 | **STALE / SUPERSEDED** by storage schema v3. |
| `B22` tag-derived package provenance | **STALE / SUPERSEDED** by package-owned `RUNTIME_PACKAGE.source_commit_sha`. |
| `B23` visible technical setup stages | **STALE / SUPERSEDED** by invisible fast-path owner. |
| `B25` mandatory checkpoint wording | **CURRENT WITH QUALIFIER**: checkpoint optional unless recovery owner requires it; launch still needs READY_PC + PLAY_READY. |
| `CAMPAIGN_CARD_CASES.md:C12` paused -> 🟡 | **STALE / SUPERSEDED**; current paused -> ⏸️, initializing -> 🟡. |
| `REGRESSION_CASES.md:T13` manifest-only menu | **STALE / SUPERSEDED** by card-first + manifest fallback. |
| access storage-main/guest wording | **CURRENT WITH QUALIFIER / SUPERSEDED IN PART** under current storage/package/adoption ownership. |
| engine-update/migration family | **OWNED DOWNSTREAM / WP-20** except creation-adjacent identity evidence. |
| `PRE_RELEASE_AUDIT_0.1.0.md` | **HISTORICAL ONLY**. |

Current executable v3/package/readiness evidence remains supporting evidence and does not promote stale Markdown scenario text into semantic authority.

### 2.6 PO-001 / PO-002 verification consumers

| Source / expectation | Disposition |
|---|---|
| `DEV/TESTS/REGRESSION_CASES.md:T04` knowledge leak | **CURRENT SUPPORTING** no-spoiler/knowledge separation; not a complete retrospective-flow test. |
| `REGRESSION_CASES.md:T08` old-NPC bounded retrieval | **CURRENT SUPPORTING** bounded history retrieval; not a complete player/disclosure/interaction-route test. |
| `AI_DM_CRAFT_CASES.md:ADC08` known context may be stated directly | **CURRENT SUPPORTING** direct eligible context presentation. |
| `EXPLICIT_SAVE_CASES.md:S07` save alone does not pause | **CURRENT** and directly supports PO-002 non-lifecycle semantics. |
| `EXPLICIT_SAVE_CASES.md:S08` save and stop combines boundaries | **CURRENT WITH QUALIFIER**: applies only when stop/pause intent is separately expressed; must not be generalized to exit-to-menu. |
| `EXPLICIT_SAVE_CASES.md:S15/S16` no false success / clear dirty state after success | **CURRENT** save-before-exit prerequisites. |
| `MULTIPLAYER_MEMBERSHIP_CASES.md:M01` voluntary leave | **CURRENT** and proves membership leave is a distinct explicit PLAYER transition. |
| `MULTIPLAYER_MEMBERSHIP_CASES.md:M10` removal freezes old live epoch | **CURRENT** for actual membership removal; must not be triggered by ordinary save-and-exit. |
| `CAMPAIGN_CARD_CASES.md:C07-C11/C13` active/locked/multiplayer/completed menu hints | **CURRENT SUPPORTING** campaign-routing presentation; authority still revalidated after selection. |
| `INSTALL_ONBOARDING_CASES.md:I06/I08` explicit campaign choice/menu | **CURRENT SUPPORTING** menu contract; currently written for entry/new chat, not explicit same-chat exit re-entry. |

**Missing direct acceptance coverage:** no current scenario/executable case directly proves either full PO-001 flow (authorized active player asks history -> ordinary gameplay -> eligibility-filtered answer -> no Commentator transition) or full PO-002 flow (save success -> context clear -> same-chat menu -> no pause/leave/control/global-live side effect). This is a downstream verification obligation, not authority to implement tests during Step 1.

---

## 3. Material evidence ledger

The previously recovered claims remain in force:

- `SM19-01` explicit campaign selection precedes campaign-specific work — CURRENT.
- `SM19-02` New Game runtime comes from storage v3 baseline — CURRENT.
- `SM19-03` branch ancestry differs from first campaign-specific root tree — CURRENT.
- `SM19-04` creator derives from first campaign-specific publication provenance — CURRENT.
- `SM19-05` exact materializer input includes `ruleset_set_sha256` — CURRENT.
- `SM19-06` bootstrap prose omits that required input — closed `F19-S1-01`, later WP-19 reconciliation obligation.
- `SM19-07` branch/storage prose includes stale v2 projections — current consistency obligation.
- `SM19-08` scaffold is not PLAY_READY — CURRENT.
- `SM19-09` provisional onboarding is distinct from mechanical readiness — CURRENT.
- `SM19-10` READY_PC and PLAY_READY are distinct gates — CURRENT.
- `SM19-11` card/README/test projections never become authority — CURRENT.
- `SM19-12` first scaffold publication and later setup publication have different transaction shapes — CURRENT.
- `SM19-13` initial multiplayer choices remain creator/access controlled — inherited CURRENT.
- `SM19-14` House-Rules baseline is inherited, not reactivated — already satisfied unless contradiction found.
- `SM19-15` campaign naming/config may remain partially undefined — CURRENT low-friction constraint.
- `SM19-16` future released-campaign evolution is WP-20 — DEFERRED by explicit sequencing.
- `SM19-17` verification/test evidence is a consumer graph, not an authority shortcut — `SR19-01` CLOSED.

### SM19-18 — campaign selection determines interaction route without a new mode hierarchy

```text
active + gameplay authorized   -> ordinary gameplay
active + readable/non-playable -> read-only Commentator
completed + readable           -> read-only Commentator
```

**Disposition:** CURRENT Product Owner semantic owner; access/lifecycle owners supply authorization/status facts. Card is presentation only.

### SM19-19 — active-player retrospective is ordinary gameplay

An authorized active player may ask for campaign history/retrospective naturally inside the current Master interaction, including via the existing OOC Master channel when appropriate. No Commentator transition is required.

**Disposition:** NEW CURRENT CONSUMER BINDING. R2.4's separate Commentator role remains valid for spectator/read-only routing and is qualified, not contradicted.

### SM19-20 — Story/history availability never grants disclosure

Retrospective retrieval follows R2.3 purpose/player/PC eligibility, R2.1/WP-18 bounded Story/history orientation, stronger-source escalation when needed, and Step-4/Step-5.12 knowledge/disclosure/output law. A retrospective question does not create world truth, PC knowledge, player disclosure entitlement or a new memory/history owner.

**Disposition:** CURRENT composition; no upstream reopen.

### SM19-21 — explicit save-and-exit is ordered composition

```text
save request
    -> satisfy existing save durability promise
    -> applicable session/live closure
    -> only after success terminate selected gameplay context
    -> clear selected-campaign working binding
    -> enter campaign-selection/menu state
```

**Disposition:** NEW CURRENT NAVIGATION CONSUMER. Save/persistence/session/live owners remain unchanged.

### SM19-22 — exit-to-menu is not stop/pause/leave

Exit alone does not imply `paused`, `completed`, `archived`, multiplayer leave, PLAYER deactivation, PC-control transfer, mode/join-policy change or campaign-global stop. Existing `save and stop` rules remain applicable only when the user separately intends stop/pause.

**Disposition:** CURRENT qualifier required to prevent lifecycle/access misrouting.

### SM19-23 — one participant leaving a chat does not globally close multiplayer/live play

An explicit save may force native durable consolidation where existing live/session owners require it. But live epoch closure/membership changes remain independently owned; `LIVE_SCENE.md` explicitly forbids closing merely because one player's chat ended while differently controlled PCs still share the actionable scene.

**Disposition:** CURRENT non-interference constraint.

### SM19-24 — same-chat menu re-entry reuses existing campaign-selection authority

The post-exit destination is the normal campaign-selection/menu state under bootstrap/card/access owners. It does not create a second campaign menu or a second authorization authority. The user must make a new explicit campaign choice before campaign-specific work resumes.

**Disposition:** NEW CURRENT consumer of existing menu/choice gate.

### SM19-25 — dedicated PO acceptance cases are missing but routed

Current tests provide supporting pieces but not end-to-end PO-001/PO-002 acceptance. Later authorized realization must add/repair verification against the canonical owner decision rather than infer semantics from unrelated older cases.

**Disposition:** DOWNSTREAM VERIFICATION OBLIGATION; does not authorize Step-1 test edits.

---

## 4. Negative findings / non-activation boundaries

The integrated evidence does **not** require:

- a new Commentator/history mode for an authorized active player;
- a new Story, memory, history, truth, knowledge or disclosure owner;
- whole-history preload or Story-only answers for material/current claims;
- turning a retrospective question into a world-state or PC-knowledge mutation merely by asking it;
- a new campaign lifecycle enum/state for “exited”;
- interpreting exit-to-menu as pause, completion, archive, multiplayer leave, PLAYER deactivation or PC-control transfer;
- closing a global multiplayer campaign/live epoch merely because one participant exits their chat;
- a second campaign menu/selection authority;
- rewriting scenario/test files during Step 1;
- reopening `F19-S1-*`, `SR19-01`, WP-16, WP-18, R2.1, R2.3 or Step-5.5 absent contradiction/material insufficiency;
- starting WP-20, implementation planning or substantive implementation.

---

## 5. Product Owner boundary check on expanded evidence

| Watch area | Integrated disposition |
|---|---|
| Product semantics | Explicitly supplied and accepted for retrospective gameplay, routing, and save-and-exit. No residual semantic choice. |
| Canonical authority / ownership | Existing truth/knowledge/disclosure/Story/save/session/access/live owners remain allocated; new owner decision binds consumers without creating duplicate authority. |
| Meaningful compatibility policy | No change; current unreleased scaffold remains clean-slate and future released-campaign evolution remains WP-20. |
| Hard-to-reverse lifecycle/product behavior | PO-002 explicitly says exit is context navigation, not lifecycle/membership mutation; ambiguity is resolved by the owner decision. |
| Material quality trade-off | No unresolved trade-off: ordinary active-player history access and same-chat exit navigation are required product semantics. |
| Explicit risk acceptance | No new risk acceptance request surfaced. |

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

No `NEEDS_PO` route was discovered.

---

## 6. Completeness gate after PO-input integration

```text
[x] Applicable PO ledger entries and immutable shared context inspected.
[x] Product Owner Input Process inspected and mid-stage critic invalidation honored.
[x] Accepted PO owner decision included as canonical evidence.
[x] PO-001 graph expanded through Step-4, Step-5.12, R2.1, R2.3, R2.4, WP-18, RUNTIME, PLAY_POLICY, INFORMATION and NARRATIVE.
[x] PO-002 graph expanded through Step-5.5, SAVE_CONTRACT, PERSISTENCE, DURABILITY_GUARD, SESSION, RUNTIME, BOOTSTRAP_RUNTIME, install bootstrap, CAMPAIGN_CARD, ACCESS_CONTROL, MULTIPLAYER and LIVE_SCENE.
[x] Campaign interaction routing active/playable vs active/read-only vs completed/read-only recorded without extra hierarchy.
[x] `save and stop` versus `save and exit-to-menu` semantics explicitly separated.
[x] Relevant test/scenario consumers inspected and item-level qualifiers preserved.
[x] Missing direct PO acceptance cases routed downstream without premature test implementation.
[x] Prior F19-S1-* findings retained/closed; SR19-01 retained/closed.
[x] Product Owner boundary rerun; no NEEDS_PO/human decision found.
[x] Whole-project Task-Brief critic rerun on expanded basis and all mechanically resolvable BLOCKING/SIGNIFICANT framing defects repaired.
[x] Step 2 remains unauthorized/unstarted.
[x] WP-20 remains unstarted.
[x] Implementation planning and substantive implementation remain unstarted.
```

The integrated Source Manifest now supports the expanded Step-1 framing claim. The next gate is **mandatory Senior review**; this manifest does not grant Step-2 authorization.