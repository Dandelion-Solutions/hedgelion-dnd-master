# HDM Product Owner Input Ledger

Status: **AUTHORITATIVE SOURCE OF PRODUCT-OWNER INTENT / ROUTING LEDGER — NOT ARCHITECTURE AUTHORITY**

Purpose: preserve Product Owner requirements, corrections, amendments and program-direction inputs durably, while agent-owned routing/status metadata tracks their current architectural disposition.

Governing process:
- `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`.

Accepted specifications remain architecture authority. `DEV/CURRENT_PROGRESS.md` remains the sole global current-progress authority.

---

## 1. Immutability and status rules

Text inside `PO input`, Product Owner correction, Product Owner amendment, or explicitly marked shared Product Owner context is immutable to agents: do not polish, translate, normalize, shorten, expand or silently correct it.

Agent-owned interpretation/routing/status may change as the repository changes.

Entry status vocabulary:

```text
OPEN
ROUTED
PARTIALLY_INCORPORATED
INCORPORATED
DEFERRED
NEEDS_PO
SUPERSEDED
```

`INCORPORATED` means current product semantics have an accepted owner and every known route is either incorporated or safely deferred with an explicit future trigger. It does not mean implementation is complete.

### Routing consistency invariant

An agent-owned route marked `ACTIVE` or `PENDING` must not name a work package that `DEV/CURRENT_PROGRESS.md` marks closed as its current pending consumer. A genuinely distinct open route through the same historical WP may remain only when the route row explicitly identifies `DISTINCT OPEN ROUTE` and states the still-open trigger. `DEV/TESTS/test_product_owner_routing_consistency.py` guards this bounded invariant.

---

## 2. Active routing index

| ID | Kind | Status | Current trigger / reason | Primary routes | Open PO decision |
|---|---|---|---|---|---|
| `PO-001` | REQUIREMENT | INCORPORATED | WP-19 final Senior PASS accepted the ordinary active-player retrospective composition; runtime/test realization remains deferred until R2.7 final reconciliation plus approved implementation planning/execution | accepted gameplay/navigation owner decision; WP-19 canonical spec; ordinary Master history consumer; later runtime/tests | NONE |
| `PO-002` | REQUIREMENT | INCORPORATED | WP-19 final Senior PASS accepted save-success -> session-local clear -> same-chat campaign-menu composition; runtime/test realization remains deferred until R2.7 final reconciliation plus approved implementation planning/execution | accepted gameplay/navigation owner decision; WP-19 canonical spec; save/session/menu/live consumers; later runtime/tests | NONE |
| `PO-003` | REQUIREMENT | INCORPORATED | WP-19 final Senior PASS accepted the bounded SemanticEvent historical-decision-basis composition and mandatory zero-extra-serial performance law; physical schema/runtime/test realization remains deferred until R2.7 final reconciliation plus approved implementation planning/execution | historical Actor decision-basis owner decision; WP-19 canonical spec; Step-4 LOG/SemanticEvent extension; R2.2/world.knowledge boundaries; retrospective/performance consumers | NONE |
| `PO-004` | COMPATIBILITY POLICY | INCORPORATED | WP-20 final Senior PASS accepted the released-v1.0+ clean-slate compatibility horizon; only downstream implementation/test realization remains deferred behind its future explicit authorization gate | v1 clean-slate compatibility owner decision; final WP-20 canonical spec; later engine/runtime/schema migration/update/release tests | NONE |
| `PO-005` | AUTHORITY / SECURITY POLICY | INCORPORATED | creator-login continuity policy is fixed fail-closed authority; no current architecture reopen; downstream runtime/test realization must preserve it when implementation is explicitly authorized | creator-login continuity owner decision; access/bootstrap/migration/recovery consumers; later runtime/tests | NONE |
| `PO-006` | AUTHORITY / SAFETY / REPOSITORY POLICY | INCORPORATED | branch/ref deletion is forbidden for every HDM development/runtime agent; WP-21 final Senior PASS consumed the rule and WP-24 may later assess retained-ref operational cost without re-enabling deletion | branch/ref deletion owner decision; `AGENTS.md`; `GAME/CORE/PERSISTENCE.md`; `GAME/CORE/LIVE_SCENE.md`; final WP-21 canonical spec/review; WP-24 | NONE |
| `PO-007` | PUBLIC PROVENANCE / ATTRIBUTION POLICY | INCORPORATED | WP-23 final Senior re-review accepted the repository-wide public provenance reconciliation and closed the architecture consumer; future enforcement remains under the accepted owner and current machine guards | public provenance owner decision; final WP-23 canonical spec; current public `DEV/` + `GAME/`; legal/notice owners; relevant audits/tests | NONE |
| `PO-008` | FAILURE / DEGRADATION / DURABILITY-RISK PRODUCT DIRECTION | INCORPORATED | WP-25 final Senior re-review PASS accepted the severity/gameplay-impact/risk model and proactive durability-risk direction; downstream generic realization and production-like host calibration remain safely deferred behind explicit future gates | accepted WP-25 owner-direction; final WP-25 canonical spec; Step 5.5/WP-13 native durability owners; later runtime/tests/empirical host acceptance | NONE |
| `PO-009` | COMMENTATOR / STORY CORPUS SUFFICIENCY | INCORPORATED | accepted owner decision now requires Story-local retained T0 basis plus a self-contained Commentator eligibility/control projection; physical Story/snapshot/cache realization remains deferred behind its future explicit architecture/implementation gate | Story producer/source contracts; historical Actor basis; Step-4 knowledge/disclosure/access; future Commentator/Story realization | NONE |
| `PO-010` | MUTABLE FILE SIZE / OPERABILITY POLICY | INCORPORATED | accepted superseding owner decision replaces the former absolute 10 KiB publication cap with target/review/review-and-partition sizing bands; WP-26 must reconcile stale routing/current prose and WP-27 must derive later realization work | sizing-bands owner decision; former 10 KiB owner; WP-24; Story growth/sharding owner; WP-26; WP-27; later runtime/Story writers/tests | NONE |

---

## 3. Shared Product Owner context for PO-001 and PO-002

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

Agent-owned disposition: incorporated by the accepted PO-001/PO-002 owner decision and the final Senior-approved WP-19 canonical composition. It adds no extra mode hierarchy.

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

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete | `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` |
| WP-19 architecture | INCORPORATED / FINAL SENIOR PASS | WP-19 closed | `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md` + final Senior review |
| Story/information/context boundaries | INCORPORATED / NO REOPEN | current owners remain controlling | Step-4, R2.3/R2.4, WP-18 |
| Runtime consumer realization | DEFERRED | after R2.7 final reconciliation + approved implementation plan/execution gate | `GAME/CORE/RUNTIME.md`, `PLAY_POLICY.md`, `INFORMATION.md`, `NARRATIVE.md` |
| Direct acceptance | DEFERRED | same implementation authorization; prove active player remains ordinary Master and disclosure-safe | current tests are supporting only |

Product Owner decision still required: `NONE`.

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

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete | `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md` |
| WP-19 architecture | INCORPORATED / FINAL SENIOR PASS | WP-19 closed | WP-19 canonical spec, save-and-exit laws + final Senior review |
| Save/session/menu/live composition | INCORPORATED AS ARCHITECTURE / REALIZATION DEFERRED | implement only after R2.7 final reconciliation + approved implementation plan/execution gate | WP-13, `SAVE_CONTRACT.md`, `SESSION.md`, bootstrap/menu, WP-16/live owners |
| Direct acceptance | DEFERRED | same implementation authorization; prove save success -> clear -> menu and no pause/leave/control/global-stop side effects | current save/membership/menu tests are supporting only |

Product Owner decision still required: `NONE`.

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
CLASSIFICATION: NEW CONSUMER + EXTENSION
SPARSE / SITUATION-SPECIFIC EVENT-TIME BASIS
EXISTING HISTORICAL-EVIDENCE OWNER: Step-4 LOG / runtime.semantic_event
DURABLE FAMILY: existing WP-10 SemanticEvent/history family
NO FULL NPC-PSYCHOLOGY HISTORY
NO PER-TURN FULL ACTOR SNAPSHOT
NO HIDDEN CHAIN-OF-THOUGHT RETENTION
CURRENT R2.2 / world.knowledge OWNERSHIP PRESERVED
CLOSED-ARCHITECTURE MATERIAL INSUFFICIENCY: NO
UPSTREAM REOPEN REQUIRED: NO
LATENCY / INTERACTIVITY: MANDATORY PRODUCT CONSTRAINT
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete | `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md` + immutable amendment above |
| WP-19 architecture | INCORPORATED / FINAL SENIOR PASS | WP-19 closed | WP-19 canonical spec `WP19-L29..L39` + final Senior review |
| R2.2 current Actor continuity | INCORPORATED / NO REOPEN | current-state owner preserved | R2.2 canonical spec |
| Step-4 current knowledge + history | INCORPORATED / EXTENSION | `world.knowledge` remains current; bounded T0 basis is SemanticEvent history | Step-4 canonical spec |
| Durable record-family allocation | INCORPORATED / NO REOPEN | existing SemanticEvent/history family is sufficient | WP-10 |
| Story / Master / Commentator consumption | INCORPORATED AS ARCHITECTURE | event-time evidence + current disclosure/no-spoiler boundaries; later Story-local self-containment refinement is owned by PO-009 decision | PO-001, R2.3/R2.4, WP-18, WP-19 canonical spec, `2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` |
| Latency/interactivity | INCORPORATED AS NORMATIVE ARCHITECTURE LAW | zero-extra-serial baseline is mandatory; extra serial critical-path work requires architecture/performance re-evaluation | WP-19 `WP19-L38/L39`, `PLAY_POLICY.md` |
| Exact runtime/schema/validator/index realization | DEFERRED | after R2.7 final reconciliation + approved implementation plan/execution gate | existing SemanticEvent/history/context/persistence owners |
| Direct T0->T1 retrospective acceptance | DEFERRED | same implementation authorization | prove retained T0 basis is used after mutable current state changes |
| Direct performance acceptance | DEFERRED | same implementation authorization | prove 0 dedicated call / redundant read / separate publication / irrelevant-turn work |

### Current impact

PO-003 is fully incorporated at the architecture level. Final Senior review passed WP-19 with event-time historical basis bounded and situation-specific, using the existing SemanticEvent owner/family, preserving current Actor/knowledge ownership, and keeping latency/interactivity as a hard product constraint. PO-009 later refines only the Commentator projection/consumption route: retained qualifying T0 factors must also be Story-local rather than remaining native-only behind a reference.

Physical runtime/schema/test realization remains deferred; this does not make the entry partially incorporated because every known current route is either incorporated or safely deferred behind an explicit authorization trigger.

Product Owner decision still required: `NONE`.

### Senior-gate recovery history

```text
SR19_03: CLOSED
SR19_04: CLOSED
```

Those recovery records remain historical provenance; the current architecture result is the final Senior-approved WP-19 canonical spec plus later explicit accepted owner decisions for their narrower scopes.

---

## PO-004 — v1.0 clean-slate compatibility baseline

Date: 2026-09-05  
Kind: COMPATIBILITY POLICY  
Status: INCORPORATED

### PO input — VERBATIM / IMMUTABLE

```text
В данный момент нигде не существует обязательств по совместимости. Версия 1.0 начинается с чистого листа и не совместима с версией 0.8. Весь абсолютно pre-release Skaffold можно считать obsolete и не тащить за собой. Всю структуру и, модели и инструкции можно переписать хоть полностью.
```

### Agent interpretation / classification

```text
CLEAN-SLATE RELEASE BASELINE
PRE-RELEASE COMPATIBILITY OBLIGATION: NONE
V0.8 -> V1.0 MIGRATION OBLIGATION: NONE
PRE-RELEASE STRUCTURAL FREEZE: NONE
PRE-RELEASE SCHEMA/MODEL/INSTRUCTION PRESERVATION: NOT REQUIRED
CURRENT WP-20 CONSUMER: CLOSED / INCORPORATED
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete | `DEV/docs/superpowers/specs/2026-09-05-hdm-v1-clean-slate-compatibility-owner-decision.md` |
| WP-20 architecture | INCORPORATED / FINAL SENIOR PASS | WP-20 closed | `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` + `DEV/docs/superpowers/design/2026-09-06-r2-7-WP-20-final-senior-review.md` |
| Pre-release `0.8 -> 1.0` migration | NOT APPLICABLE BY OWNER DECISION | no compatibility layer/migrator required solely for pre-release state | owner decision above |
| Pre-release structures/models/instructions | NO COMPATIBILITY FREEZE | may be replaced when current accepted architecture requires it | current owners + WP-20 reverse audit |
| Released v1.0+ compatibility/update/migration policy | INCORPORATED | final WP-20 architecture accepted | WP-20 canonical spec |
| Runtime/schema/tool/test realization | DEFERRED | when the owning implementation-planning/execution gate is explicitly authorized; not active during WP-21 architecture work | later implementation consumers |

### Current impact

PO-004 is fully incorporated at the architecture level. Final Senior review passed WP-20 with the compatibility horizon beginning at released v1.0+, with no v0.8/pre-release compatibility or migration obligation.

The only remaining route is downstream realization under a future explicit implementation-planning/execution gate. That deferred route does not make WP-20 a current pending consumer and does not reopen the Product Owner decision.

Product Owner decision still required: `NONE`.

---

## PO-005 — Creator-login continuity and takeover prevention

Date: 2026-09-06  
Kind: AUTHORITY / SECURITY POLICY  
Status: INCORPORATED

Accepted owner decision:
- `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md`.

### Product Owner input — VERBATIM / IMMUTABLE

```text
Переименование GH юзера мы не будем поддерживать. Тут 2 риска: кража сессии игры под видом "я переименовал пользователя" с одной стороны и получение R/O игры с другой стороны. Я выбираю второе! в крайнем случае, если это действительно хозяин репозитория - он может вручную создать копию этой ветки со всей историей и тогда владелец новой ветки-сессии будет новый юзер. Игра тут стоит на своём и ничего менять не будет. Правила есть правила.
```

### Agent interpretation / classification

```text
PRODUCT / AUTHORITY / SECURITY POLICY
AUTOMATIC LOGIN-RENAME CONTINUITY: NOT SUPPORTED
UNRESOLVABLE CREATOR LOGIN: FAIL CLOSED
READ-ONLY CONSEQUENCE: ACCEPTED
STABLE-ID SUBSTITUTION FOR CREATOR AUTHORITY: FORBIDDEN
SILENT OWNER TRANSFER: FORBIDDEN
AUTOMATIC RECOVERY CLAIM: NONE
CURRENT ARCHITECTURE REOPEN: NO
NEEDS_PO: NONE
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete / fixed authority | `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md` |
| Access/bootstrap/migration/recovery architecture | INCORPORATED / BINDING INPUT | current owners must preserve fail-closed creator provenance; no rename substitution | current access/bootstrap/WP-20/recovery owners + accepted decision |
| Runtime/tool/test realization | DEFERRED | only when the owning implementation-planning/execution gate is explicitly authorized | prove unresolvable creator login blocks creator-only writes while read-only remains available and stable PLAYER ID/repository permission do not transfer creator authority |

### Current impact

This decision is fixed authority. It does not reopen creator identity semantics and does not add automatic rename continuity, stable-ID creator substitution or silent authority transfer.

Manual repository-owner recovery/copy remains outside HDM's automatic creator-continuity guarantee exactly as stated by the accepted owner decision.

Product Owner decision still required: `NONE`.

---

## PO-006 — Branch/ref deletion prohibition

Date: 2026-09-06  
Kind: AUTHORITY / SAFETY / REPOSITORY POLICY  
Status: INCORPORATED

Accepted owner decision:
- `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md`.

### Product Owner input — VERBATIM / IMMUTABLE

```text
На счет permanent delete: нет, никакая LLMка не имеет права удалять ветки в репозитории. Можешь так прямо и зафиксировать в core-файлах HDM и GAME, что удаление веток не предусмотрено, и команда `delete branch` не должна вызываться вообще никогда, ни при каких обстоятельствах.
```

### Agent interpretation / classification

```text
AUTHORITY / SAFETY / REPOSITORY-OPERATION POLICY
BRANCH/REF DELETION: PROHIBITED
DELETE-BRANCH / DELETE-REF OPERATION: NOT ADMITTED
STEP-5 OPTIONAL REF-DELETION CAPABILITY: SUPERSEDED
CURRENT-TREE / PATH CLEANUP: UNAFFECTED
HOST-MANAGED UNREACHABLE-OBJECT GC: OUTSIDE HDM
WHOLESALE STEP-5 REOPEN: NO
CURRENT WP-21 CONSUMER: CLOSED / INCORPORATED
FUTURE WP-24 OPERATIONAL CONSUMER: DEFERRED
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics / prohibition | INCORPORATED | complete / fixed authority | `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md` |
| Development-agent core | INCORPORATED | every HDM development runtime must obey it regardless of tool availability | `AGENTS.md` |
| GAME persistence/live runtime | INCORPORATED | no runtime branch/ref deletion; absorbed/orphan refs remain non-authoritative retained transport artifacts | `GAME/CORE/PERSISTENCE.md`, `GAME/CORE/LIVE_SCENE.md` |
| Step-5 cleanup/recovery | INCORPORATED / TARGETED SUPERSESSION | replace only optional ref-delete semantics; retain all other native-owner cleanup/survivor/currentness laws | owner decision above supersedes Step-5.13 laws 4/71..73 and Step-5.14 SD-6 |
| WP-21 architecture | INCORPORATED / FINAL SENIOR PASS | WP-21 closed; diagnostics/cleanup/retirement framing treats retained refs as non-authoritative and does not reintroduce delete capability | final WP-21 canonical spec + final Senior review |
| WP-24 operational budget | DEFERRED | when WP-24 opens, assess accumulation/observability cost of retained refs without re-enabling deletion | WP-24 scope |
| Regression protection | INCORPORATED | machine guard rejects executable branch/ref-delete invocations and stale core projections | `DEV/TESTS/test_branch_ref_deletion_prohibition.py` |

### Current impact

The Product Owner decision is complete and requires no further human choice. It narrows previous cleanup capability rather than introducing a new subsystem: authority is still ended by existing routing/currentness owners, while non-authoritative branches may remain indefinitely.

WP-21 final Senior PASS consumed this entry and accepted owner decision without reopening deletion capability. The only named future architecture consumer is the deferred WP-24 operational-cost route, which may measure retained-ref cost but may not re-enable deletion.

Product Owner decision still required: `NONE`.

---

## PO-007 — Public development/research provenance and attribution boundary

Date: 2026-09-08  
Kind: PUBLIC PROVENANCE / ATTRIBUTION POLICY  
Status: INCORPORATED

Accepted owner decision:
- `DEV/docs/superpowers/specs/2026-09-08-hdm-public-research-provenance-attribution-owner-decision.md`.

### Product Owner input — VERBATIM / IMMUTABLE

```text
Да, всё верно. Мы НЕ хотим тащить в HDM Dev и Game "какие сайты, авторов и исследования мы использовали при разработке". Только обязательная или отдельно осознанно одобренная атрибуция. Так что, да, тут я с тобой согласен.
```

### Agent interpretation / classification

```text
PUBLIC PRODUCT / PROVENANCE POLICY
PUBLIC DEV/GAME SOURCE-SPECIFIC DEVELOPMENT/RESEARCH PROVENANCE: NOT ALLOWED BY DEFAULT
LEGAL-REQUIRED ATTRIBUTION: PRESERVE
SEPARATELY EXPLICITLY PRODUCT-OWNER-APPROVED ATTRIBUTION: PRESERVE
PUBLIC HDM SEMANTICS: INDEPENDENTLY STATED IN HDM TERMINOLOGY
TECHNICAL ARTIFACT/RELEASE/VERSION/MIGRATION PROVENANCE: UNAFFECTED / PRESERVE WHERE OWNED
GIT HISTORY REWRITE: NOT REQUIRED
CURRENT WP-23 CONSUMER: CLOSED / FINAL SENIOR RE-REVIEW PASS
NEW WORKSTREAM: NO
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics / public provenance boundary | INCORPORATED | complete / fixed policy | `DEV/docs/superpowers/specs/2026-09-08-hdm-public-research-provenance-attribution-owner-decision.md` |
| WP-23 architecture | INCORPORATED / FINAL SENIOR RE-REVIEW PASS | WP-23 closed; package/version/legal/provenance composition accepted | final WP-23 canonical spec + Step-7/Step-8 closure |
| Required legal attribution | INCORPORATED / PRESERVE | license/notice owners remain controlling | root/GAME legal/notice/license surfaces |
| Technical package/version provenance | INCORPORATED / UNAFFECTED | preserve release/update/migration integrity evidence | runtime package provenance/version/update owners |
| Current public provenance surfaces and machine checks | INCORPORATED / RECONCILED | audited current frontier reconciled; future ambiguous artifacts remain owner-aware classification under the fixed policy | final WP-23 canonical spec; affected public sources/tests/audits |

### Current impact

`WP23-S1-F01` is closed. The policy is broader than runtime packaging alone: public `DEV/` and `GAME/` are both in scope. Required or explicitly approved attribution remains, technical HDM artifact provenance remains, and source-specific research/development narratives are not a public HDM authority or default public artifact.

The mandatory independent WP-23 final Senior re-review passed after the targeted `SR23-FINAL-01` repair. WP-23 is closed with no new workstream and no WP-20 reopen required. Future enforcement of PO-007 remains under its accepted owner plus current legal/release/provenance checks rather than an active WP-23 route.

Product Owner decision still required: `NONE`.

---

## PO-008 — Failure/degradation severity and proactive durability-risk protection

Date: 2026-09-08  
Kind: FAILURE / DEGRADATION / DURABILITY-RISK PRODUCT DIRECTION  
Status: INCORPORATED

Accepted direction:
- `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md`.

### Product Owner input — VERBATIM / IMMUTABLE

```text
ну.... ты всё правильно рассуждаешь! поручаю тебе ответственно подойти к проектированию этого блока! раздели ошибки по severity, и тому как они влияют на геймплей и насколько рискованно продолжать их игнорировать (ждать пока они исправятся), и так далее. Подключай  всю мощь superpowers и не жалей критики и whole-project аудита!
```

### Product Owner amendment — VERBATIM / IMMUTABLE

```text
"каждый час" - это было условность. Потому что лимиты чата не бесконечны и в какой-то момент он не дает сказать/сделать вообще ничего! И не хотелось бы оказаться в этой точке с огромным накопленными HOT/SOFT который фиг знает как теперь сохранить в репо....
```

### Product Owner approval / publication direction — VERBATIM / IMMUTABLE

```text
да, вот теперь я согласен с всем твоим массивом рассуждений и предложений.
предлагаю всё это не прятать в Lab  а наоборот, зафиксировать как направление разработки. Мы тут много чего выяснили и уточнили - это должно стать основой дальнейшей работы. Ну а в Lab ты всё равно можешь записать, какие неочевидные whole-project риски надо будет проверить после встроенного критика. Фиксируй все документы и пиши промпт Агенту.
```

### Agent interpretation / classification

```text
PRODUCT DIRECTION + CLOSED WP-25 ARCHITECTURE INPUT
CONTEXT-DERIVED EFFECTIVE SEVERITY, NOT INTRINSIC ERROR SEVERITY
GAMEPLAY IMPACT / AFFECTED SCOPE / IGNORE-RISK / TEMPORAL-TOLERANCE ARE DISTINCT AXES
UNSUPPORTED IS AN ORTHOGONAL DISPOSITION
SELECTED DIRECTION: OWNER-LOCAL NATIVE OUTCOMES + EPHEMERAL CROSS-OWNER FAILURE DISPOSITION
PROACTIVE DURABILITY INTENT: PRESERVE ESTABLISHED HOT/SOFT BEFORE PROBABLE HOST INCAPACITY
HOURLY AUTOSAVE AS PRODUCT LAW: REJECTED
CAPACITY HEURISTIC AS SEMANTIC AUTHORITY: REJECTED
DANGEROUS SINGLE-COPY LOSS EXPOSURE MAY CREATE OPERABILITY / LOSS-PROTECTION FENCE
OPERABILITY FENCE != GENERIC CORRECTNESS HARD
WHOLE-PROJECT CRITIC: MANDATORY / AGGRESSIVE
LAB ROLE: PRIVATE ADVERSARIAL RISK CHECKLIST ONLY, NOT ARCHITECTURE AUTHORITY
NEEDS_PO: NONE
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product / architecture direction | INCORPORATED | accepted direction published and consumed | `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` |
| Step 5.5 / WP-13 durability-risk semantics | INCORPORATED / RECONCILED / NO REOPEN | final WP-25 preserves scope-relative `MAY_DEFER` semantics while adding bounded loss-protection trajectory without converting risk into generic correctness HARD | Step 5.5 canonical durability spec + WP-13 + final WP-25 canonical spec |
| WP-25 architecture | INCORPORATED / FINAL SENIOR RE-REVIEW PASS | WP-25 closed | `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-25-error-degradation-failure-semantics-canonical-spec.md` + final independent Senior review |
| Runtime/schema/test realization | DEFERRED | after R2.7 final reconciliation + explicit implementation-planning/execution authorization | later implementation consumers |
| Production-like host/capacity acceptance | DEFERRED | run only on realized supported target where empirical evidence is required | R2.6 + WP-22 + WP-24 + WP-25 proof contract |
| Independent Senior adversarial support | HISTORICAL / NON-AUTHORITATIVE | retained only as review evidence; public/current architecture comes from accepted owners | final WP-25 review chain |

### Current impact

PO-008 is fully incorporated at the architecture level. WP-25 final Senior re-review passed with the Product Owner severity/gameplay-impact/risk separation and proactive durability-risk direction preserved. The retired hourly proxy is not product law; current durability protection uses scope-local `NORMAL / ELEVATED / DANGER`, with DANGER remaining distinct from correctness HARD and from any timer/scheduler/retry authority.

Remaining generic `FailureDisposition` realization, exact host-risk calibration and production-like empirical acceptance are safely deferred behind explicit future implementation/empirical gates. Those deferred routes do not make PO-008 partially incorporated and do not reopen WP-25.

Product Owner decision still required: `NONE`.

---

## PO-009 — Self-contained Commentator Story corpus, historical T0 basis and eligibility projection

Date: 2026-09-09  
Kind: COMMENTATOR / STORY CORPUS SUFFICIENCY  
Status: INCORPORATED

Accepted owner decision:
- `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md`.

### Product Owner context — VERBATIM / IMMUTABLE

```text
Во-первых, не путай SQLite файлы мастера с SQLite файлами комментатора. Это два разных режима, хоть и работающих в одном чате для соседних игровых веток. То есть можно создавать SQLite кэши под каждую кампанию свой. При этом надо понимать, что даже если сейчас эта кампания read-only и пользователь может зайти в него только как комментатор, он может через пять минут получить инвайт и перезайти в кампанию уже как игрок, и тогда ему нужен будет совершенно другой SQLite файл с другим форматом данных, таблицами и все остальное, который предназначен для работы мастера, а не комментатора. То есть здесь я тебе хотел сказать, что SQLite база комментатора для тебя — это совершенно другое окружение. HDM мастер к нему не имеет никакого отношения. И, соответственно, мы будем разрабатывать SQL cache в формате, удобном для быстрой навигации, поиска и пересказа истории комментаторам. Это его внутренняя кухня. Пусть там и остается.
```

### Product Owner local-canon clarification — VERBATIM / IMMUTABLE

```text
Во-вторых, это для HDM-мастера каноном является текущая игра, а стори является не канонической. А вот для комментатора, который видит только стори, уже она является локальным каноном. Так что всё правильно он написал.
```

### Product Owner secrets/snapshot clarification — VERBATIM / IMMUTABLE

```text
Что касается секретов, разумеется, их надо все хранить в том же самом месте/хранилище. единственное, что стори снапшот должен в том числе содержать и эту информацию: кому что доступно, кто что знает. Но я думаю, что это уже и так реализовано.
```

### Product Owner T0 correction — VERBATIM / IMMUTABLE

```text
Видимо, в какой-то момент произошло недопонимание. Потому что я всегда считал, что bounded historical decision basis будет в том числе попадать в историю вместе с самим событием или действием.
```

### Product Owner required change — VERBATIM / IMMUTABLE

```text
В общем да, твои выводы верны и нужно вносить изменения в HDM (снапшоты и/или летописца), чтобы обеспечить целостность и достаточность информации для комментатора.
```

### Agent interpretation / classification

```text
PRODUCT / CONSUMER CORRECTION + MATERIAL INSUFFICIENCY IN PRIOR STORY PROJECTION
COMMENTATOR LOCAL FACTUAL CANON: STORY CORPUS WITH COMMENTATOR CONTROL PROJECTION
HDM GAMEPLAY CANON / CURRENT NATIVE AUTHORITY: UNCHANGED
COMMENTATOR CACHE != MASTER HOT / WP-12 SQLITE
COMMENTATOR CACHE PHYSICAL SCHEMA: DOWNSTREAM INTERNAL / NOT PUBLIC HDM CONTRACT
QUALIFYING WP-19 T0 BASIS: MUST BE STORY-LOCAL, NOT NATIVE-REF-ONLY
PRIVATE/OFF-SCREEN T0 MATERIAL: RETAIN WITH PROTECTION, DO NOT OMIT
SELF-CONTAINED COMMENTATOR ELIGIBILITY/CONTROL PROJECTION: REQUIRED
WORLD.KNOWLEDGE / RUNTIME.DISCLOSURE / ACCESS OWNERSHIP: PRESERVED
CONTENT_FINAL != ACCESS_FINAL
BASELINE COMMENTATOR NATIVE FALLBACK FOR REQUIRED T0: NOT REQUIRED / NOT A DEPENDENCY
NEW STORY LAYER: NO
NEW HISTORY OR ACL AUTHORITY: NO
MASTER/COMMENTATOR SHARED SQLITE FORMAT: NO
NEEDS_PO: NONE
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product semantics | INCORPORATED | complete | `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` |
| PO-003 historical Actor basis | INCORPORATED / NARROW CONSUMER SUPERSESSION | SemanticEvent remains native historical owner; Story must also carry the already-retained bounded factor meaning for Commentator | PO-003 owner decision + WP-19 + new PO-009 owner decision |
| Story producer / Chronicler / source contracts | INCORPORATED AS BINDING FUTURE REQUIREMENT | when Story realization/design is next activated, native-only T0 pointers no longer satisfy Commentator corpus completeness | Story integration + baseline projection contracts as narrowed/superseded by PO-009 |
| Step-4 knowledge/disclosure/access | INCORPORATED / OWNERS PRESERVED | future Commentator snapshot must export a derived sufficient control projection without creating a second owner | Step-4, R2.3, Access Control, PO-009 |
| Commentator local read cache | DOWNSTREAM INTERNAL / OUTSIDE MASTER HOT | implementation may choose campaign-local SQL schema/indexes optimized for history/search/retelling; no compatibility with Master HOT required | PO-009 public boundary only; exact consumer implementation remains downstream |
| Content/access currentness | INCORPORATED | content finality may freeze content but not access/knowledge/disclosure projection; refresh control basis when those owners change | PO-009 `SCC-9/SCC-10` |
| Story/snapshot schema, sharding, validator and tests | DEFERRED | next explicit Story/Commentator architecture/implementation gate | PO-009 + existing Story sharding/versioning/test owners |
| Current R2.7 program cursor | NOT ACTIVATED | this cross-cutting owner decision does not authorize WP-26 or implementation planning | `DEV/CURRENT_PROGRESS.md` |

### Current impact

The prior Story design was sufficient for a consumer allowed to escalate from Story into native historical evidence, but it was insufficient for the now-explicit baseline Commentator requirement that the imported Story corpus be self-contained for supported factual explanation and secret-safe filtering.

The correction is targeted: native SemanticEvent/history ownership remains unchanged, while qualifying retained T0 factors must also be projected into Story and the Commentator-importable snapshot must include enough derived knowledge/disclosure/access state to evaluate Story eligibility locally. The Commentator cache remains an independent downstream read model and is never reused as Master HOT or gameplay authority.

Product Owner decision still required: `NONE`.

---

## PO-010 — Mutable GitHub-backed text file sizing bands

Date: 2026-09-09  
Kind: MUTABLE FILE SIZE / OPERABILITY POLICY  
Status: INCORPORATED

Accepted owner decision:
- `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`.

### Product Owner input — VERBATIM / IMMUTABLE

```text
По поводу размера файлов в репозитории. Я вижу, что везде фигурирует 10 килобайт, но это была нижняя граница с большим запасом. То есть можно везде говорить 10 килобайт для простоты, но в реальности тот, кто будет это решать, пора ли начинать новый файл или можно писать в текущий, должен иметь следующие ориентиры: 10–12 килобайт — это целевой размер, 13–16 килобайт — зона пересмотра, 16 плюс килобайт — зона пересмотра/деления.
```

### Agent interpretation / classification

```text
PRODUCT / RUNTIME OPERABILITY POLICY CORRECTION
OLD 10 KIB ABSOLUTE PUBLICATION CAP: SUPERSEDED
10 KIB SHORTHAND: ALLOWED FOR SIMPLE CONSERVATIVE HUMAN GUIDANCE
PREFERRED STEADY-STATE TARGET: APPROXIMATELY 10–12 KIB OR SMALLER
NORMAL REVIEW ZONE: APPROXIMATELY 13–16 KIB
ABOVE APPROXIMATELY 16 KIB: REVIEW / PARTITION / ROLLOVER DEFAULT EXPECTATION
UNIVERSAL EXACT BYTE HARD-STOP: NO
SEMANTIC INTEGRITY / ATOMICITY / IDENTITY: PRESERVED
NO TRUNCATION TO HIT SIZE TARGET
WP24 WHOLESALE REOPEN: NO
STORY WHOLESALE REOPEN: NO
NEEDS_PO: NONE
```

### Current routing

| Route | State | Trigger / obligation | Current evidence / owner |
|---|---|---|---|
| Product/runtime sizing semantics | INCORPORATED | complete / current owner published | `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` |
| Former 10 KiB hard-cap decision | INCORPORATED / TARGETED SUPERSESSION | preserve provenance and unaffected partition/no-truncation laws; old exact hard cutoff is not current | `2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` as historical/superseded in threshold scope |
| WP-24 performance/scale | INCORPORATED / NARROW SUPERSESSION | WP-24 remains closed; only LAW WP24-13 absolute 10 KiB trigger is superseded by the new bands | WP-24 canonical spec + current owner decision |
| Story persistence/growth | INCORPORATED / NARROW SUPERSESSION | bounded partitionability remains; absolute 10 KiB Story cap is replaced by the same bands | Story growth/sharding owner + current sizing owner |
| WP-26 routing/supersession | ACTIVE / CURRENT AUTHORIZED STEP-1 INPUT | identify stale current hard-cap wording and route readers to the current sizing owner without rewriting safe history | WP-26 Step 1 Source Manifest/brief/critic |
| WP-27 implementation-planning readiness | DEFERRED | derive concrete writer/rollover/schema/test workstreams after WP-26 closure | WP-27 |
| Runtime/Story machine realization and tests | DEFERRED | future approved implementation planning/execution; run Version Impact Gate for any material persisted/module changes | relevant writers/schemas/tests |

### Current impact

The Product Owner input is fully incorporated and does not remain as an unresolved requirement. The project may continue using “about 10 KiB” as shorthand, but implementation-facing logic must use the target/review/review-and-partition model rather than rejecting every payload above 10,240 bytes.

The correction is cross-cutting but narrow: it changes the sizing trigger policy, not semantic ownership, partition identity, publication atomicity, Story authority or transport authority. WP-26 must reconcile stale current routing/prose; WP-27 later derives realization work.

Product Owner decision still required: `NONE`.

---

## 4. Current ledger terminal state

This is a routing-ledger projection only; `DEV/CURRENT_PROGRESS.md` remains the sole global cursor authority.

```text
PO-001: INCORPORATED
PO-002: INCORPORATED
PO-003: INCORPORATED — COMMENTATOR STORY ROUTE REFINED BY PO-009
PO-004: INCORPORATED — WP-20 FINAL SENIOR PASS / NO CURRENT PENDING WP-20 ROUTE
PO-005: INCORPORATED — FIXED CREATOR-LOGIN FAIL-CLOSED AUTHORITY
PO-006: INCORPORATED — BRANCH/REF DELETION PROHIBITED / WP-21 FINAL SENIOR PASS
PO-007: INCORPORATED — PUBLIC DEV/GAME RESEARCH-PROVENANCE POLICY / WP-23 FINAL SENIOR RE-REVIEW PASS
PO-008: INCORPORATED — WP-25 FINAL SENIOR RE-REVIEW PASS / DOWNSTREAM REALIZATION AND EMPIRICAL ACCEPTANCE DEFERRED
PO-009: INCORPORATED — STORY-LOCAL T0 + SELF-CONTAINED COMMENTATOR ELIGIBILITY PROJECTION / REALIZATION DEFERRED
PO-010: INCORPORATED — 10 KIB HARD CAP SUPERSEDED BY TARGET / REVIEW / REVIEW-AND-PARTITION SIZING BANDS

WP19_FINAL_SENIOR_REVIEW: PASS
WP20_FINAL_SENIOR_REVIEW: PASS
WP20_CLOSED: YES
WHOLE_PROJECT_AUDIT_REPAIR: COMPLETE / SENIOR PASS
WP21_FINAL_SENIOR_REVIEW: PASS
WP21_CLOSED: YES
WP22_FINAL_SENIOR_REVIEW: PASS
WP22_CLOSED: YES
WP23_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP23_CLOSED: YES
WP24_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP24_CLOSED: YES
WP25_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP25_CLOSED: YES

HUMAN_DECISION_REQUIRED: NONE
NEEDS_PO: NONE
UPSTREAM_REOPEN_REQUIRED: NO
TARGETED_STORY_CONSUMER_SUPERSESSION: YES / PO-009 OWNER DECISION PUBLISHED
TARGETED_SIZE_POLICY_SUPERSESSION: YES / PO-010 OWNER DECISION PUBLISHED

IMPLEMENTATION_PLANNING_STARTED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
REAL_GAMEPLAY_BOOTSTRAP_STARTED: NO
```

Current global gate and authorization remain governed only by `DEV/CURRENT_PROGRESS.md`.