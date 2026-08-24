# R2.7 — Протокол исполнения whole-project final audit

Status: **OWNER-APPROVED EXECUTION PROTOCOL — ACTIVE**

Date: 2026-08-24

Связанные владельцы:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Этот документ определяет **как исполняется** R2.7. Он не меняет семантическую архитектуру и не разрешает broad implementation.

---

## 1. Цель

R2.7 состоит из 27 обязательных audit domains `WP-01` … `WP-27` плюс финального whole-project reconciliation. Работа должна быть устойчивой к:

- длинному reasoning run;
- прерыванию текущего чата;
- лимиту сообщений/контекста;
- переходу в новый чат;
- необходимости owner decision посреди domain.

Ключевой закон:

> **Conversation state is never an R2.7 checkpoint. Only freshly verified repository state is a checkpoint.**

В новом чате владелец может написать только `Продолжай R2.7`; агент обязан восстановить точную точку работы из репозитория.

---

## 2. Durable control plane

R2.7 использует следующие долговечные артефакты:

1. этот execution protocol — стабильный алгоритм исполнения;
2. `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md` — компактный cursor/status authority внутри R2.7;
3. whole-project Source Manifest и глобальные ledgers — накопительное evidence/conformance accounting;
4. отдельный русскоязычный mini-report для каждого `WP-XX`;
5. Decision Brief только если реально требуется human architecture/product-owner judgment.

`NEAR_TERM_ROADMAP.md` остаётся sequencing authority для стадии R2.7 в целом. `audit-status.md` владеет только внутренним cursor внутри R2.7.

---

## 3. Язык артефактов

Mini-reports `WP-XX` пишутся **на русском языке**, чтобы владелец мог их быстро читать, контролировать и корректировать.

Техническая нотация может оставаться на английском, включая:

- identifiers;
- schema/property names;
- path names;
- enum/status names;
- typed interfaces;
- pseudocode;
- exact quoted contract terms.

Глобальные ledgers могут смешивать русский explanatory text и английскую machine-oriented нотацию, если это повышает точность.

---

## 4. Fresh-session recovery

Перед продолжением R2.7 в новом или существенно оборванном чате агент обязан выполнить:

```text
current remote ref/state
-> AGENTS.md
-> DEV/DESIGN_PROCESS.md
-> DEV/ARCHITECTURE/DESIGN_PROCESS.md
-> DEV/PROJECT_MAP.md
-> DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md
-> R2.7 Task Brief v2
-> R2.7 execution protocol
-> R2.7 audit-status cursor
-> current WP mini-report
-> unresolved forward obligations / owner gate
-> task-specific owning sources for current slice
```

Conversation summaries и remembered state могут ускорять навигацию, но не заменяют эти reads.

---

## 5. Domain execution loop

Для каждого `WP-XX` применяется один и тот же цикл.

### 5.1 RECOVER / BIND

- подтвердить active ref;
- прочитать текущий `audit-status.md`;
- определить `current_domain` и `current_slice`;
- загрузить только relevant dependency subgraph.

### 5.2 DOMAIN SOURCE MANIFEST

Для текущего domain определить:

- canonical/owning sources;
- later amendments/owner decisions;
- derivative routing indexes;
- relevant research evidence;
- GAME runtime consumers;
- GAME persistent schemas/templates;
- DEV catalogs/schemas;
- tests/audit/release/bootstrap/migration consumers;
- historical/superseded artifacts только если они влияют на supersession или current debt.

### 5.3 EVIDENCE EXTRACTION

По материалам domain фиксировать, где применимо:

```text
Source/item
Actual claim
Authority/classification
Qualifiers/applicability
Exceptions/negative findings
Revisit/defer trigger
Existing owner/decision
Conflict / extension / no-delta
Current disposition
Rationale
```

Нельзя заменять item-level accounting тематическим summary там, где coverage зависит от перечислимого набора.

### 5.4 ARCHITECTURE -> MACHINE

Для каждой принятой material semantic responsibility проверить concrete destination либо explicit no-representation verdict.

### 5.5 MACHINE -> ARCHITECTURE

Для каждой material current machine/runtime surface проверить accepted owner либо классифицировать её как:

```text
DERIVED
IMPLEMENTATION-ONLY
HISTORICAL
STALE
DEBT
OUT-OF-SCOPE
```

Existing scaffold получает нулевую презумпцию корректности.

### 5.6 ADVERSARIAL CHECK

Как минимум проверить:

- duplicate authority;
- stale/superseded assumptions;
- bypass deterministic gates;
- invalid currentness/recovery semantics;
- unsafe failure behavior;
- hidden unbounded scan/load;
- cross-domain coupling;
- migration/bootstrap/test/release omissions.

### 5.7 FINDING CLASSIFICATION

Каждый material finding получает один из operational dispositions:

```text
SATISFIED
AUTO_RESOLVED
IMPLEMENTATION_OBLIGATION
VERIFICATION_OBLIGATION
FORWARD_OBLIGATION
SAFE_DEFERRED
STALE_DEBT
OWNER_DECISION_REQUIRED
OUT_OF_SCOPE
```

### 5.8 CLOSE OR CHECKPOINT

Если domain закрываем в текущем reasoning window:

- завершить mini-report;
- обновить global ledgers;
- выполнить fresh verification;
- только после этого продвинуть `audit-status.md` на следующий domain.

Если domain слишком велик:

- разделить его JIT на evidence slices;
- после законченного содержательного slice обновить mini-report как `IN_PROGRESS`;
- записать exact `current_slice`, полученные findings и следующий slice;
- выполнить fresh read-back verification;
- продолжить автоматически.

Не создавать заранее подробный sub-roadmap на все slices: деление возникает только по реальному dependency graph.

---

## 6. Forward obligations

Если finding принадлежит более позднему domain, но текущий domain можно безопасно закрыть без его результата, создать typed forward obligation:

```text
ID: WP-XX/FNN
Source domain
Target domain
Exact obligation
Why deferred there
Blocking relation: NON_BLOCKING_CURRENT | BLOCKS_FINAL_CLOSURE
Required discharge evidence
```

Forward obligation не исчезает при переходе между чатами и должен быть снят в target domain или в финальном reconciliation.

---

## 7. Human stop conditions

Нормальный режим — **AUTO_CONTINUE**.

Агент НЕ останавливается для:

- naming;
- exact path placement, если owner уже определён;
- schema shape, однозначно следующей из принятой архитектуры;
- test-level choice;
- derived-index bookkeeping;
- stale-document classification;
- технического mapping;
- obvious best implementation-neutral architecture detail;
- механической traceability/consistency работы.

Агент обязан сам принять и зафиксировать такие решения с rationale.

Остановка `WAITING_OWNER` допускается только для residual decision одного из классов:

```text
PRODUCT_SEMANTICS
ARCHITECTURE_TRADEOFF
AUTHORITY_CHANGE
COMPATIBILITY_POLICY
RISK_ACCEPTANCE
SCOPE_CHANGE
SUPERSESSION
```

Перед остановкой агент обязан:

1. исчерпать техническое исследование;
2. зафиксировать все established facts и completed findings в репозитории;
3. обновить mini-report;
4. обновить `audit-status.md` в `WAITING_OWNER`;
5. создать Decision Brief с:
   - exact delta/conflict;
   - viable alternatives;
   - consequences;
   - recommendation;
   - uncertainty;
   - exact owner decision required;
6. выполнить fresh verification публикации;
7. только после этого обратиться к владельцу.

После owner decision агент формализует решение, снимает gate и автоматически продолжает тот же domain.

---

## 8. Mini-report contract

Каждый `WP-XX` получает отдельный mini-report в `DEV/docs/superpowers/research/`.

Filename:

```text
2026-08-24-r2-7-WP-XX-<short-topic>-mini-report.md
```

Обязательные разделы:

```text
Статус
Краткий вывод
Покрытые вопросы
Source Manifest delta
Установленные факты
Architecture -> machine
Machine -> architecture
Конфликты / stale / negative findings
Автоматически принятые технические решения
Implementation obligations
Verification / MVP acceptance obligations
Forward obligations
Round-2 Diamond/Strong delta, если применимо
Human decision: NONE | exact gate
Closure verdict
Точка продолжения
```

Mini-report не обязан повторять весь исходный материал; он обязан сохранять доказательную трассировку и qualifiers, достаточные для проверки вывода.

---

## 9. Checkpoint publication discipline

Repository write discipline:

```text
fresh current remote state
-> prepare coherent checkpoint delta
-> Connector write on active ref only
-> no new branch
-> fresh read-back verification
-> only then advance durable cursor
```

Никакие `gh`, remote native Git, direct HTTP/token workarounds, probe branches или alternative transport experiments не допускаются.

Commit frequency:

- не коммитить после каждого прочитанного файла;
- делать durable checkpoint после завершённого evidence slice;
- обязательно делать checkpoint при domain closure;
- обязательно делать checkpoint перед `WAITING_OWNER`.

---

## 10. Failure / interruption semantics

Если чат прерван после анализа, но до verified checkpoint:

- незаписанный reasoning считается потерянным;
- новый чат начинает с последнего verified repository cursor;
- нельзя угадывать, что «мы наверняка уже закончили slice».

Если write произошёл, но read-back не подтверждён:

- cursor не считается продвинутым;
- при recovery сначала проверяется remote state;
- затем либо принимается подтверждённый write, либо повторно формируется coherent checkpoint без дублирования semantic effect.

---

## 11. Final reconciliation

После закрытия `WP-27` R2.7 НЕ закрывается автоматически.

Запускается final reconciliation:

1. discharge всех forward obligations;
2. reconcile global semantic-owner matrix;
3. reconcile architecture->machine matrix;
4. reconcile machine->architecture reverse ledger;
5. reconcile persistent/HOT/index/instruction/bootstrap/migration/test/release matrices;
6. перепроверить 82 Round-2 DIAMOND/STRONG + S14/S53/D15 deltas;
7. проверить dormant/revisit triggers;
8. выполнить whole-project adversarial composition review;
9. проверить 24 exit criteria Task Brief v2;
10. поднять owner gates только для реальных residual decisions;
11. сформировать canonical final architecture/machine-realization spec;
12. выполнить implementation-planning entry resolution gate.

Только после этого возможен переход в implementation planning.

---

## 12. Continuation command

Если работа переходит в новый чат, достаточно пользовательского сообщения:

> `Продолжай R2.7`

Агент не должен просить владельца пересказывать историю. Точная точка продолжения восстанавливается из verified repository state.