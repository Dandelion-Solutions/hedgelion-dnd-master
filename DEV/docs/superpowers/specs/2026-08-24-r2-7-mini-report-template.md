# R2.7 — Шаблон русскоязычного mini-report

Status: **ACTIVE REPORTING TEMPLATE**

Date: 2026-08-24

Применяется к `WP-01` … `WP-27` в рамках:

- `2026-08-24-r2-7-audit-execution-protocol.md`
- `2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`

Mini-report — evidence/checkpoint artifact, а не новый semantic owner.

---

# WP-XX — <Название domain>

Статус: **IN PROGRESS | CLOSED | WAITING_OWNER**

## 1. Краткий вывод

2–8 абзацев на русском языке: что установлено, есть ли gap/conflict, что это меняет для implementation planning.

## 2. Покрытые вопросы

Перечислить вопросы domain из scope-discovery и их disposition:

```text
Q1 — SATISFIED | GAP | CONFLICT | SAFE_DEFERRED | OUT_OF_SCOPE
...
```

Нельзя закрывать domain, если mandatory question потерян без явной disposition.

## 3. Source Manifest delta

| Source | Authority role | Required scope | Inspection status | Почему релевантен |
|---|---|---|---|---|

Source roles:

```text
CANONICAL / OWNING
CANONICAL AMENDMENT / OWNER DECISION
DERIVATIVE LOCATOR / INDEX
RESEARCH INPUT
HISTORICAL / SUPERSEDED
IMPLEMENTATION / MACHINE CONTRACT / TEST
```

## 4. Установленные факты и ограничения

Для material items по необходимости фиксировать:

```text
ID
FACT | CONSTRAINT | DECISION | INFERENCE | DEFERRED | DEBT
Claim
Source/owner
Qualifiers / exceptions
Current interpretation
```

## 5. Architecture -> machine

Таблица или структурированный список:

| Semantic responsibility | Accepted owner/source | Machine/runtime destination | Representation verdict | Status |
|---|---|---|---|---|

Допустимые explicit no-representation verdicts:

```text
NO DURABLE RECORD
NO SQLITE OWNER
NO INDEX
INSTRUCTION ONLY
DERIVED ONLY
EPHEMERAL ONLY
POST-MVP EVALUATION ONLY
```

## 6. Machine -> architecture

| Existing machine/runtime surface | Current responsibility | Accepted owner | Classification | Action |
|---|---|---|---|---|

Classification:

```text
OWNED
DERIVED
IMPLEMENTATION-ONLY
HISTORICAL
STALE
DEBT
OUT-OF-SCOPE
```

## 7. Конфликты, stale surfaces и negative findings

Каждый material finding:

```text
Finding ID
Observed state
Why material
Disposition
Blocking? YES | NO
Target owner/domain
```

Отрицательные findings сохраняются: отсутствие необходимости в новом owner/subsystem также является результатом.

## 8. Автоматически принятые технические решения

Только решения, однозначно следующие из accepted architecture или имеющие заведомо доминирующий технический вариант.

Для каждого:

```text
Decision
Rationale
Affected implementation destinations
Why no owner gate is required
```

## 9. Implementation obligations

```text
IMP-XX-NN
Exact obligation
Target files/components/schemas where already knowable
Dependency
Acceptance condition
```

Не выполнять implementation во время R2.7.

## 10. Verification / MVP acceptance obligations

```text
VER-XX-NN
Verification class: unit | schema | integration | scenario | LLM acceptance | manual UI/deployment
Exact behavior/invariant
Downstream owner
```

## 11. Forward obligations

```text
WP-XX/FNN
Target domain
Exact obligation
Why deferred there
Blocking relation
Required discharge evidence
```

Если отсутствуют: `NONE`.

## 12. Round-2 Diamond / Strong delta

Заполнять только если domain изменяет/уточняет machine/test disposition соответствующих D/S items.

Если нет изменения: `NO DELTA`.

## 13. Human decision

```text
NONE
```

или exact gate:

```text
Gate class
Established facts
Residual alternatives
Recommendation
Exact owner decision required
Decision Brief path
```

## 14. Closure verdict

Для закрытого domain:

```text
DOMAIN: WP-XX
VERDICT: CLOSED
UNRESOLVED_ARCHITECTURE_BLOCKERS: 0
OWNER_GATE: NONE
FORWARD_OBLIGATIONS: <count/list>
NEXT_DOMAIN: WP-YY
```

Для незакрытого slice:

```text
DOMAIN: WP-XX
VERDICT: IN_PROGRESS
COMPLETED_SLICE: ...
NEXT_SLICE: ...
OWNER_GATE: NONE
```

Для human gate:

```text
DOMAIN: WP-XX
VERDICT: WAITING_OWNER
OWNER_GATE: <class/id>
NEXT_ACTION_AFTER_DECISION: ...
```

## 15. Точка продолжения

Короткая repository-driven инструкция для следующего reasoning run/chat: что читать и какой exact slice/domain продолжать.