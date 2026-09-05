# HDM Product Owner Input Ledger

Status: **AUTHORITATIVE SOURCE OF PRODUCT-OWNER INTENT / ROUTING LEDGER — NOT ARCHITECTURE AUTHORITY**

Purpose: preserve Product Owner requirements, corrections, ideas, reopen requests and program-direction inputs durably even when they do not align with the currently active WP/stage, and route them to the correct current or future architecture consumers without prematurely activating work.

Governing process addendum:

- `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`

Accepted architecture/specifications, runtime contracts, schemas and `DEV/CURRENT_PROGRESS.md` remain the authorities for accepted semantics, machine contracts and current execution state. This ledger preserves **what the Product Owner intended** and how the agent routed that intent; it is not a substitute for architectural incorporation.

---

## 1. Immutability and authorship rules

### Product Owner-authored text is immutable to agents

Text inside any of these blocks is Product Owner-authored evidence and MUST NOT be rewritten, polished, normalized, translated, shortened, expanded or silently corrected by an agent:

- `PO input`;
- `Product Owner correction`;
- `Product Owner amendment`;
- explicitly marked shared Product Owner context.

If the Product Owner later corrects or changes an earlier input, preserve the original block and append a new verbatim correction/amendment block with its own date. Do not rewrite history to make the original text look as if it always contained the later correction.

Agent-owned fields such as interpretation, classification, routing, statuses, triggers, affected owners, current/future impact and incorporation evidence MAY be updated as repository state evolves.

Git history provides the normal audit trail for changes to this ledger; no additional integrity machinery is required.

### Public-repository safety exception

The public HDM repository must not retain credentials, secrets, sensitive personal data, unlawful confidential material, third-party proprietary text, or other content prohibited by repository public-material rules merely to satisfy verbatim preservation.

If a Product Owner message contains such material, do not publish it verbatim here. Record a public-safe placeholder and routing metadata, preserve the semantic intent only through an allowed sanitized/independently rewritten artifact, and use an authorized private evidence location when applicable. The entries below required no such sanitization.

---

## 2. Entry status vocabulary

```text
OPEN
    captured, but routing/reconciliation is not yet complete

ROUTED
    affected owners/stages/triggers are known; no currently applicable incorporation is outstanding
    or the entire entry is waiting on a future trigger

PARTIALLY_INCORPORATED
    at least one applicable semantic/consumer route is incorporated, while another currently
    applicable route remains incomplete

INCORPORATED
    current product semantics have an accepted owner and every known route is either incorporated
    or explicitly deferred with a valid future trigger

DEFERRED
    intentionally not current work; a concrete activation/revisit trigger is recorded

NEEDS_PO
    a genuine unresolved Product Owner decision remains after technical analysis; dependent
    architecture is blocked until an explicit Product Owner answer is recorded

SUPERSEDED
    a later explicit Product Owner input replaces the current intent; original text remains preserved
```

Entry-level status summarizes the whole input. Individual routing targets may carry their own route states such as `ACTIVE`, `PENDING`, `INCORPORATED`, `DEFERRED`, `NOT_APPLICABLE`, or `SUPERSEDED`.

**Coverage does not imply activation.** A future route may be known and fully recorded without changing the current project cursor or creating current work.

---

## 3. Active routing index

This table is an agent-maintained navigation index only. The full entry controls preserved Product Owner intent and routing detail.

| ID | Kind | Status | Current trigger / reason | Primary routes | Open PO decision |
|---|---|---|---|---|---|
| `PO-001` | REQUIREMENT | INCORPORATED | Accepted semantic owner + current WP-19 Step-1 framing incorporated; exact runtime/test realization explicitly deferred to later authorized gates | accepted gameplay/navigation owner decision; WP-19; ordinary gameplay history consumer; later tests/realization | NONE |
| `PO-002` | REQUIREMENT | INCORPORATED | Accepted semantic owner + current WP-19 Step-1 framing incorporated; exact runtime/test realization explicitly deferred to later authorized gates | accepted gameplay/navigation owner decision; WP-19; save/session/bootstrap/menu/multiplayer consumers; later tests/realization | NONE |
| `PO-003` | REQUIREMENT | INCORPORATED | Accepted semantic owner + PO-003-expanded WP-19 Step-1 framing/critic incorporated; latency/interactivity amendment preserved; exact runtime/schema/test realization explicitly deferred to authorized downstream gates | historical Actor decision-basis owner decision; WP-19; Step-4 LOG/SemanticEvent extension; R2.2/world.knowledge current-owner boundaries; retrospective consumers; durability/context/performance/test realization | NONE |

---

## 4. Shared Product Owner context for PO-001 and PO-002

Date: 2026-09-05  
Source: direct Product Owner conversation

### Shared Product Owner context — VERBATIM / IMMUTABLE

```text
Важно: не надо из этого создавать дополнительную сложную иерархию режимов. Базовая продуктовая модель теперь такая:

- пользователь запускает новый чат;
- HDM показывает доступные ему кампании;
- если выбранная активная кампания допускает gameplay participation для этого пользователя — он входит в обычную игру;
- если активная кампания ему видима, но играть в ней он не может — она открывается read-only через Commentator;
- завершённая видимая кампания также открывается read-only через Commentator.

Commentator не является режимом, в который нормальный активный игрок должен дополнительно входить ради просмотра истории.
```

Agent interpretation: this shared context constrains both inputs. Campaign selection remains campaign-first; participation capability and campaign lifecycle determine ordinary gameplay versus read-only Commentator interaction. It forbids solving either requirement by adding a redundant mode hierarchy.

Current accepted semantic owner:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`.

---

# Entries

## PO-001 — Retrospective/history discussion inside ordinary active gameplay

Date: 2026-09-05  
Kind: REQUIREMENT  
Status: INCORPORATED

### PO input — VERBATIM / IMMUTABLE

```text
1. Просмотр/обсуждение истории внутри активной игры

Если пользователь уже вошёл в активную кампанию как нормальный игрок своим активным персонажем, отдельный Commentator mode ему не нужен.

D&D Master уже является рассказчиком/мастером/управляющим и должен позволять игроку естественным языком обращаться к прошлой истории прямо из обычного gameplay, например:

- «Напомни, что происходило тогда-то».
- «Кто такой этот NPC?»
- «Почему он тогда так поступил?»
- «Расскажи подробнее события той сессии».
- «Покажи/перескажи историю этого места».

Master при этом использует всю имеющуюся историю кампании, но отвечает строго с учётом knowledge/disclosure/no-spoiler policy текущего игрока: не раскрывает тайны и сведения, которые этому principal/персонажу ещё недоступны.

То есть это не переход в Commentator и не отдельный режим. Это штатная retrospective/history capability обычного D&D Master внутри активного gameplay.

Нужно проверить, где эта capability должна быть закреплена канонически: runtime instructions / gameplay interaction contract / Story access consumer requirements / другой owning artifact.
```

### Agent interpretation / classification

```text
NEW EXPLICIT PRODUCT / CONSUMER REQUIREMENT
NO NEW STORY OR MEMORY AUTHORITY
NO NEW GAMEPLAY MODE
NO COMMENTATOR TRANSITION FOR AN AUTHORIZED ACTIVE PLAYER
```

Existing information/continuity owners remain controlling. The delta is an explicit ordinary-gameplay consumer binding for retrospective/history questions, with player/PC knowledge/disclosure/no-spoiler eligibility and proper-source escalation where existing Context Runtime rules require it.

### Routing / affected owners

| Route | State | Trigger / obligation | Evidence / current owner |
|---|---|---|---|
| Product semantics formalization | INCORPORATED | Immediate | `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` |
| R2.7 WP-19 Step-1 framing | INCORPORATED | PO-003 targeted expansion and critic rerun are now complete; current package awaits mandatory Senior review | current WP-19 Source Manifest + Architecture Task Brief + Task-Brief critic |
| Existing Story/continuity/information owners | INCORPORATED AS INPUT / NO REOPEN | Reopen only on demonstrated contradiction/material insufficiency; none found for PO-001 | Step-4 truth/knowledge/disclosure/role-context; Step-5.12; R2.1; R2.3; R2.4; final WP-18 Story/continuity owner |
| Ordinary gameplay interaction/runtime consumer | DEFERRED | Trigger: explicit Senior GO authorizing WP-19 Step 2; then prove exact instruction/consumer placement | `GAME/CORE/RUNTIME.md`, `PLAY_POLICY.md`, `INFORMATION.md`, `NARRATIVE.md` plus context/history owners |
| Verification / acceptance mapping | DEFERRED | Trigger: later authorized WP-19 design-realization / implementation-planning execution; direct PO-001 acceptance gap is already recorded | current supporting `REGRESSION_CASES:T04/T08`, `AI_DM_CRAFT_CASES:ADC08`; exact additions not authorized yet |
| Substantive implementation | DEFERRED | Trigger: approved architecture + implementation-plan gate | no implementation authorized by this input |

### Current impact

PO-001 remains incorporated. PO-003 is a later related requirement that strengthens the historical evidence available to this consumer; its targeted WP-19 Step-1 evidence-basis expansion and critic rerun are now complete. This does not alter the preserved PO-001 semantics.

### Deferred / future impact

Later authorized WP-19 architecture/runtime/test realization must consume the accepted public owner decision rather than treating this ledger as runtime authority. Direct acceptance coverage remains a downstream obligation.

### Product Owner decision still required

`NONE` — the Product Owner already supplied the product semantics. Remaining owner placement, consumer mapping, retrieval composition, test mapping and implementation detail are agent-owned unless evidence exposes a new genuine trade-off.

### Resolution evidence

- accepted semantic owner: `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- current WP-19 Source Manifest;
- current WP-19 Architecture Task Brief;
- current WP-19 whole-project Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md` remains historical PO-001/PO-002 integration provenance.

---

## PO-002 — Explicit save-and-exit from active gameplay back to campaign selection

Date: 2026-09-05  
Kind: REQUIREMENT  
Status: INCORPORATED

### PO input — VERBATIM / IMMUTABLE

```text
2. Явный выход из активной кампании обратно к выбору кампаний

Должна существовать понятная пользовательская команда уровня:

«Сохрани игру и выйди из игры».

Семантически она должна:

- корректно зафиксировать необходимое состояние кампании согласно существующему save/persistence contract;
- завершить текущий gameplay context;
- вернуть пользователя к состоянию выбора доступных кампаний.

Пользователь, конечно, всегда может просто открыть новый чат и снова получить список кампаний, поэтому это не обязательно главный UX-путь. Но lifecycle transition должен существовать явно и быть прописан в инструкциях D&D Master.
```

### Agent interpretation / classification

```text
NEW EXPLICIT PRODUCT / NAVIGATION REQUIREMENT
COMPOSITION OF EXISTING SAVE + SESSION + CAMPAIGN-SELECTION OWNERS
NO NEW CAMPAIGN LIFECYCLE ENUM
NO AUTOMATIC CAMPAIGN PAUSE
NO AUTOMATIC MULTIPLAYER MEMBERSHIP LEAVE
```

The requested exit is a current gameplay-session/context navigation transition. Existing save/persistence/session/live/multiplayer owners decide the required durability and closure mechanics. One player's exit must not accidentally pause/terminate a multiplayer campaign or deactivate membership.

### Routing / affected owners

| Route | State | Trigger / obligation | Evidence / current owner |
|---|---|---|---|
| Product semantics formalization | INCORPORATED | Immediate | `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` |
| R2.7 WP-19 Step-1 framing | INCORPORATED | PO-003 targeted expansion and critic rerun are now complete; save-and-exit semantics remain unchanged | current WP-19 Source Manifest + Architecture Task Brief + Task-Brief critic |
| Explicit save/persistence composition | DEFERRED | Trigger: explicit Senior GO authorizing WP-19 Step 2; then prove exact consumer composition | Step-5.5 canonical durability, `GAME/CORE/SAVE_CONTRACT.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md` |
| Session/gameplay-context closure | DEFERRED | Trigger: explicit Senior GO; prove save-success-before-context-clear and exact session-local state release | `GAME/CORE/SESSION.md`, `GAME/CORE/RUNTIME.md` |
| Campaign-selection re-entry | DEFERRED | Trigger: explicit Senior GO; prove reuse of current card-first menu/explicit choice gate in same chat | `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `CAMPAIGN_CARD.md`, access owners |
| Multiplayer/live non-interference | DEFERRED | Trigger: explicit Senior GO; prove exit != leave/deactivation/control transfer/global stop and only native-required live consolidation occurs | `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md`, session/concurrency owners |
| Verification / acceptance mapping | DEFERRED | Trigger: later authorized design-realization / implementation-planning execution; direct PO-002 acceptance gap is already recorded | `EXPLICIT_SAVE_CASES:S07/S08/S15/S16`, membership/menu cases; exact additions not authorized yet |
| Substantive implementation | DEFERRED | Trigger: approved architecture + implementation-plan gate | no implementation authorized by this input |

### Current impact

PO-002 remains incorporated. PO-003 integration is now complete and does not change the save-and-exit product semantics. Later persistence design must still ensure any required historical decision-basis evidence is included in the applicable durability guarantee rather than lost on save/exit.

### Deferred / future impact

Later architecture/runtime/test realization must consume the accepted owner decision. A new chat remains an alternate route to campaign selection; it is not the only supported navigation path.

### Product Owner decision still required

`NONE` — the Product Owner supplied the required product semantics. Remaining save/session/live composition and failure handling are technical unless later evidence exposes a material product trade-off.

### Resolution evidence

- accepted semantic owner: `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- current WP-19 Source Manifest;
- current WP-19 Architecture Task Brief;
- current WP-19 whole-project Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md` remains historical PO-001/PO-002 integration provenance.

---

## PO-003 — Historical event-time Actor decision basis for retrospective explanation and replay

Date: 2026-09-05  
Kind: REQUIREMENT  
Status: INCORPORATED

### PO input — VERBATIM / IMMUTABLE

```text
Значит, смотри. Хранить всю историю психики всех NPC — мы сами себя закопаем. А вот сохранять decision basis со всеми (или минимально необходимым набором - Причем я даже не утверждаю, что этот набор должен быть фиксированный. Он может быть абсолютно разный в разных ситуациях - пусть решает LLM на момент события) релевантными полями — это хорошее решение, как мне кажется. своего рода компромисс. Я думаю, что это нужно включать уже сейчас, потому что и мастер, и комментатор при возврате либо проигрывании исторических событий должны пользоваться как раз-таки информацией на момент события.
```

### Product Owner amendment — VERBATIM / IMMUTABLE

Date: 2026-09-05

```text
Это всё чудесно, но не забывай про эффективность и скорость ответа. Я боюсь, что всеми этими дополнительными действиями мы окончательно угробим интерактивность. И это будет слайд-шоу по пять минут ожидания. Никто в это играть не будет.
```

### Agent interpretation / classification

```text
NEW EXPLICIT PRODUCT / HISTORICAL-EXPLANATION REQUIREMENT
SPARSE EVENT-TIME DECISION BASIS
VARIABLE SITUATION-SPECIFIC FIELD SET
NO FULL NPC-PSYCHOLOGY HISTORY
NO PER-TURN FULL ACTOR SNAPSHOT
NO HIDDEN CHAIN-OF-THOUGHT RETENTION
CURRENT R2.2 / WORLD.KNOWLEDGE OWNERSHIP PRESERVED
CLASSIFICATION: NEW CONSUMER + EXTENSION
EXISTING HISTORICAL-EVIDENCE OWNER: STEP-4 LOG / runtime.semantic_event
CLOSED-ARCHITECTURE MATERIAL INSUFFICIENCY: NO
UPSTREAM REOPEN REQUIRED: NO
LATENCY / INTERACTIVITY: MANDATORY PRODUCT CONSTRAINT
STEP-1 PERFORMANCE FRAMING: SATISFIED BY CURRENT ZERO-EXTRA-SERIAL ANALYSIS
CURRENT MACHINE / TEST REALIZATION GAP: YES — DEFERRED TO AUTHORIZED DOWNSTREAM GATES
```

The requirement is to preserve bounded historical evidence sufficient to explain or replay a material NPC decision using the Actor's relevant knowledge/cognition/relationship state as it existed at that event, rather than substituting the NPC's later current state. The relevant field set is intentionally not universal: the LLM may identify which eligible values materially formed the decision basis for that situation, subject to later architecture-defined boundedness/source-validation rules.

The Product Owner amendment makes latency/interactivity a mandatory product constraint on this requirement. The current WP-19 Step-1 performance analysis already satisfies the present framing obligation by requiring a zero-extra-serial baseline: no additional sequential LLM call solely for decision-basis capture; no additional serial remote/tool read solely for capture when required data is already in the decision context; no separate remote publication solely for the basis; and no work on irrelevant turns. Exact runtime/schema/test realization and proof remain downstream and require their normal authorization gates.

### Routing / affected owners

| Route | State | Trigger / obligation | Evidence / current owner |
|---|---|---|---|
| Product semantics formalization | INCORPORATED | Immediate | `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md` + immutable PO-003 amendment in this ledger |
| R2.7 WP-19 Step-1 framing | INCORPORATED | PO-003 dependency expansion and mandatory whole-project critic rerun are complete; package is at mandatory Senior review | current WP-19 Source Manifest + Architecture Task Brief + Task-Brief critic |
| R2.2 current Actor continuity | INCORPORATED / NO REOPEN | Current-state ownership is preserved; historical evidence is not stored as a second writable Actor owner | `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`, `GAME/CORE/NPC.md` |
| Step-4 current knowledge + transition history | INCORPORATED / EXTENSION | `world.knowledge` remains current epistemic owner; bounded historical decision basis extends existing LOG/SemanticEvent history ownership | Step-4 truth/knowledge/role-context canonical spec + SemanticEvent/log owners |
| Durable history / record-family allocation | INCORPORATED / NO REOPEN | Existing Step-4 LOG/runtime.semantic_event + WP-10 SemanticEvent/history family is sufficient; no material closed-architecture insufficiency found | WP-10 durable record-family completeness + current event/history owners |
| Story / retrospective Master / Commentator consumers | INCORPORATED IN STEP-1 FRAMING | Event-time basis is required for material historical motive claims; current disclosure/no-spoiler boundaries remain controlling | R2.1, R2.3/R2.4, final WP-18 Story/continuity owner, PO-001 ordinary gameplay retrospective owner |
| Latency / interactivity constraint | INCORPORATED IN STEP-1 FRAMING | Current obligation satisfied by zero-extra-serial performance analysis; any future correctness claim requiring a new serial round-trip must be treated as a material architecture/performance problem | current WP-19 Source Manifest performance section + Task Brief performance criterion + critic F19-PO003-04 |
| Exact runtime/schema realization | DEFERRED | Trigger: explicit Senior GO for WP-19 Step 2 for exact design placement; substantive realization still requires later approved architecture/implementation gate | existing SemanticEvent/history, context, runtime and persistence owners |
| Durability / publication realization | DEFERRED | Trigger: explicit Senior GO and later authorized realization; required basis must join ordinary native history/persistence batching, not create a separate publication path | Step-5.5, WP-13, save/persistence owners |
| Verification / acceptance mapping | DEFERRED | Trigger: later authorized design-realization / implementation-planning/execution; prove T0 basis survives T1 current-state change and prove zero-extra-serial behavior | current supporting Actor/history/context/performance/persistence/chronology tests; direct PO-003 case remains downstream |
| Substantive implementation | DEFERRED | Trigger: approved architecture + implementation-plan gate | no schema/runtime/test implementation authorized by this input |

### Current impact

PO-003 is incorporated for the current WP-19 Step-1 gate. Product semantics are accepted; the Step-1 Source Manifest/Task Brief/critic expansion is complete; classification is `NEW CONSUMER + EXTENSION`; Step-4 `LOG/runtime.semantic_event` is the existing historical-evidence owner; no closed-architecture material insufficiency or upstream reopen was found; and direct machine/test realization remains explicitly downstream.

The Product Owner amendment adds a durable latency/interactivity constraint without reopening the completed Step-1 framing. The existing performance analysis already encodes the required current baseline and therefore satisfies the present framing obligation. The package remains at mandatory Senior review; no Step-2 authorization is implied.

PO-001 and PO-002 remain valid and are not reopened by this requirement. The previous Step-1 findings remain closed unless new evidence directly contradicts them.

### Deferred / future impact

Later authorized architecture/runtime/test realization must preserve an event-time basis sparse enough to avoid exhaustive psychological history while strong enough for faithful retrospective/replay. It must also preserve the mandatory interactivity constraint by keeping capture on the zero-extra-serial baseline unless future correctness evidence demonstrates that this is impossible and the resulting material performance trade-off is explicitly handled through the normal architecture process.

The historical basis remains evidence, not a second current cognition/knowledge owner, and must not retain hidden chain-of-thought. Exact physical representation, trigger policy, validation boundary, schema/runtime realization and direct acceptance tests remain deferred to their explicit authorization gates.

### Product Owner decision still required

`NONE` — the Product Owner explicitly chose the product trade-off: sparse event-time decision basis rather than exhaustive NPC psychological history, with a situation-specific relevant field set that need not be fixed globally, and explicitly made latency/interactivity mandatory. Exact architecture realization remains agent-owned unless later evidence exposes a new genuine Product Owner trade-off.

### Resolution evidence

- accepted product-semantic owner: `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`;
- current WP-19 Source Manifest: PO-003 owner classification + mandatory performance/latency evidence;
- current WP-19 Architecture Task Brief: PO-003 classification + mandatory performance/latency criterion;
- current WP-19 whole-project Task-Brief critic: `F19-PO003-04` closes the Step-1 latency/performance framing defect and records downstream verification;
- `DEV/CURRENT_PROGRESS.md` and `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`: current Step-1 complete / mandatory Senior review state;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-po-003-arrival-integration-checkpoint.md`: historical arrival provenance only.

### Senior-gate recovery disposition

```text
SR19_03: CLOSED — PO-003 entry-level and route states synchronized to the current incorporated Step-1 package; future runtime/schema/test work remains safely DEFERRED with explicit triggers.
SR19_04: CLOSED — Product Owner latency/interactivity amendment preserved verbatim; current zero-extra-serial Step-1 framing recognized as satisfying the present obligation; exact realization remains downstream.

WP19_STEP1: COMPLETE — MANDATORY SENIOR REVIEW
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
ARCHITECTURE_REOPENED: NO

WP19_STEP2_AUTHORIZED: NO
STEP2_STARTED: NO
WP20_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
```
