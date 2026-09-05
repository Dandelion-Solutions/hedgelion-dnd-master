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
| R2.7 WP-19 Step-1 framing | INCORPORATED | Complete; mandatory Senior review is the current gate | WP-19 Source Manifest + Architecture Task Brief + rerun whole-project critic + integration checkpoint |
| Existing Story/continuity/information owners | INCORPORATED AS INPUT / NO REOPEN | Reopen only on demonstrated contradiction/material insufficiency; none found in Step-1 integration | Step-4 truth/knowledge/disclosure/role-context; Step-5.12; R2.1; R2.3; R2.4; final WP-18 Story/continuity owner |
| Ordinary gameplay interaction/runtime consumer | DEFERRED | Trigger: explicit Senior GO authorizing WP-19 Step 2; then prove exact instruction/consumer placement | `GAME/CORE/RUNTIME.md`, `PLAY_POLICY.md`, `INFORMATION.md`, `NARRATIVE.md` plus context/history owners |
| Verification / acceptance mapping | DEFERRED | Trigger: later authorized WP-19 design-realization / implementation-planning execution; direct PO-001 acceptance gap is already recorded | current supporting `REGRESSION_CASES:T04/T08`, `AI_DM_CRAFT_CASES:ADC08`; exact additions not authorized yet |
| Substantive implementation | DEFERRED | Trigger: approved architecture + implementation-plan gate | no implementation authorized by this input |

### Current impact

The expanded WP-19 Step-1 Source Manifest and Task Brief incorporate PO-001, and the mandatory whole-project Task-Brief critic has been rerun on the expanded basis. The current route is complete for Step 1 and now waits at mandatory Senior review; downstream routes remain dormant until their explicit triggers.

### Deferred / future impact

Later authorized WP-19 architecture/runtime/test realization must consume the accepted public owner decision rather than treating this ledger as runtime authority. Direct acceptance coverage remains a downstream obligation.

### Product Owner decision still required

`NONE` — the Product Owner already supplied the product semantics. Remaining owner placement, consumer mapping, retrieval composition, test mapping and implementation detail are agent-owned unless evidence exposes a new genuine trade-off.

### Resolution evidence

- accepted semantic owner: `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- integrated WP-19 Source Manifest;
- integrated WP-19 Architecture Task Brief;
- rerun WP-19 whole-project Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md`.

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
| R2.7 WP-19 Step-1 framing | INCORPORATED | Complete; mandatory Senior review is the current gate | WP-19 Source Manifest + Architecture Task Brief + rerun whole-project critic + integration checkpoint |
| Explicit save/persistence composition | DEFERRED | Trigger: explicit Senior GO authorizing WP-19 Step 2; then prove exact consumer composition | Step-5.5 canonical durability, `GAME/CORE/SAVE_CONTRACT.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md` |
| Session/gameplay-context closure | DEFERRED | Trigger: explicit Senior GO; prove save-success-before-context-clear and exact session-local state release | `GAME/CORE/SESSION.md`, `GAME/CORE/RUNTIME.md` |
| Campaign-selection re-entry | DEFERRED | Trigger: explicit Senior GO; prove reuse of current card-first menu/explicit choice gate in same chat | `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `CAMPAIGN_CARD.md`, access owners |
| Multiplayer/live non-interference | DEFERRED | Trigger: explicit Senior GO; prove exit != leave/deactivation/control transfer/global stop and only native-required live consolidation occurs | `GAME/CORE/MULTIPLAYER.md`, `LIVE_SCENE.md`, session/concurrency owners |
| Verification / acceptance mapping | DEFERRED | Trigger: later authorized design-realization / implementation-planning execution; direct PO-002 acceptance gap is already recorded | `EXPLICIT_SAVE_CASES:S07/S08/S15/S16`, membership/menu cases; exact additions not authorized yet |
| Substantive implementation | DEFERRED | Trigger: approved architecture + implementation-plan gate | no implementation authorized by this input |

### Current impact

The expanded WP-19 Step-1 package explicitly distinguishes exit-to-menu from `save and stop`, pause/completion/archive, PLAYER leave/deactivation, PC-control transfer and global multiplayer/live termination. The rerun critic closes the framing omissions; current Step-1 incorporation is complete and waits at mandatory Senior review.

### Deferred / future impact

Later architecture/runtime/test realization must consume the accepted owner decision. A new chat remains an alternate route to campaign selection; it is not the only supported navigation path.

### Product Owner decision still required

`NONE` — the Product Owner supplied the required product semantics. Remaining save/session/live composition and failure handling are technical unless later evidence exposes a material product trade-off.

### Resolution evidence

- accepted semantic owner: `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`;
- integrated WP-19 Source Manifest;
- integrated WP-19 Architecture Task Brief;
- rerun WP-19 whole-project Task-Brief critic;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md`.