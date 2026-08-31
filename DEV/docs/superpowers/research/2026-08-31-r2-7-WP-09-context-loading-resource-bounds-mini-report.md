# R2.7 WP-09 — Context loading, retrieval and resource-bounded operation — mini-report

## Статус

**STEP 2 IN PROGRESS — EVIDENCE SLICE 2: CURRENT RUNTIME/RETRIEVAL COMPLETE**

Глобальная авторизация и gate принадлежат `DEV/CURRENT_PROGRESS.md`. Этот
mini-report — task-local evidence/cursor WP-09, а не global current-progress
authority.

## Краткий вывод

Первичные owners фиксируют весь logical context contract. Обратная проверка
текущих GAME consumers подтверждает совместимую основу: immutable CORE cache
отделён от lazy campaign working set, а CURRENT/scene/INDEX — routing support
для exact targeted reads. Она не создаёт alternative architecture и не превращает
текущие hints/cache/catalog registration в роль-context authority.

## Покрытые вопросы

- bounded discovery before full load;
- routing-only scene/location/index hints;
- packet floors, optional degradation и `UNSATISFIABLE`;
- отсутствие exact hidden token telemetry;
- no global/history preload;
- ephemeral Context Runtime versus durable/HOT support;
- currentness/eligibility, recipient catch-up и bounded history orientation;
- actual CORE cache, current working-set, schema/index and direct test/catalog
  consumer compatibility.

## Source Manifest delta

Прочитаны actual primary owners R2.1, R2.3, R2.4, R2.5, R2.6, Step-4 amendment
и Step-5.14, затем current GAME CORE, schemas/templates, catalog, direct tests,
MechanicalContext, branch/package and CI surfaces. Подробная item-level evidence:

- `2026-08-31-r2-7-WP-09-step-2-canonical-owner-evidence.md`;
- `2026-08-31-r2-7-WP-09-step-2-current-runtime-evidence.md`.

## Установленные факты

1. Requiredness и floors принадлежат registered consumer/profile, не LLM ranking.
2. CORE instruction cache и campaign working set различны; cache не является
   campaign canon, role bundle или ChatGPT Memory.
3. Index/current/scene являются discovery/routing support; они не доказывают
   closed world и не заменяют current native owner.
4. Existing catalog registration aligns vocabulary, but is not behavioural proof
   of assembly/fallback/eligibility.
5. `ASSEMBLED_DEGRADED` сохраняет все required semantics; `UNSATISFIABLE`
   terminal и требует finite registered caller path.
6. R2.6 запрещает exact hidden token telemetry; calibration — post-implementation
   evidence, не причина для parallel MVP.

## Architecture -> machine

Existing law requires future runtime-local realization of a registered profile,
bounded candidate/closure route, routed currentness/eligibility, legal packet
allocation and finite outcome handling. It must preserve the current cache/lazy
working-set distinction and use current routing surfaces only as non-authoritative
inputs.

## Machine -> architecture

No material contradiction. Current schemas, CORE policy and catalog vocabulary
support the accepted logical architecture but do not supersede R2.3/R2.4/R2.6.
MechanicalContext is a distinct deterministic mechanics contract, not a context
assembly owner.

## Конфликты / stale / negative findings

Нет material contradiction. Index partitioning остаётся CONDITIONAL / DORMANT
до доказанного R2.3 trigger. Generic memory/graph/worker/provider-cache не
авторизованы. Existing tests are partial and cannot certify full R2.3 runtime
behaviour.

## Автоматически принятые технические решения

Не принимать current cache/index/schema/catalog registration за authority по
названию или наличию; проверять каждый consumer against R2.3/R2.4/R2.6 и
downstream boundaries.

## Implementation obligations

Предварительно выявлена только existing-law realization gap: будущая поведенческая
проверка должна доказать profile-owned required closure, currentness/eligibility,
floors/degradation, central estimate и finite `UNSATISFIABLE` path. Exact
placement и implementation plan ещё не формируются.

## Verification / MVP acceptance obligations

Current regressions already cover cache/lazy retrieval; future R2.6 behavioural
proof for floors/degradation/`UNSATISFIABLE` still requires direct mapping.

## Forward obligations

Physical topology/HOT details остаются evidence boundaries WP-11/WP-12 и будут
routed только при material finding.

## Human decision

**NONE.**

## Точка продолжения

Step-2 slice 3: remaining DEV machine contracts, maintenance/audit route and
test/CI consumers; then consolidate Step 2.
