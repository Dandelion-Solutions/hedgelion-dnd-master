# Миграции кампаний

Этот каталог используется только когда **released v1.0+** persistent campaign contract или конкретная persistent schema меняется несовместимо и для перехода существующей кампании требуется явное преобразование данных.

Pre-release/v0.8 campaign state не входит в текущий compatibility horizon и не получает migration path лишь потому, что исторические файлы когда-то описывали такую структуру.

Engine-файлы не копируются и не merge'ятся в campaign repository. Runtime всегда берётся из точного валидированного локального runtime package; миграция кампании меняет только явно объявленные campaign data/schema/native paths и допустимые creator-owned campaign identity/adoption projections.

## Version/generation discipline

`engine_version`, `campaign_contract_generation`, `storage_format_generation`, ruleset/catalog generations и artifact-local `schema_version` — разные namespace.

- равенство/порядок внутри namespace само по себе не доказывает compatibility;
- значения разных namespace не сравниваются друг с другом;
- Git ancestry, timestamps, mutable tags/current `main` не создают migration path;
- unsupported newer contract/generation fail closed.

## Explicit migration edges

Каждая поддерживаемая миграция должна существовать как явный **directed edge** immutable support data точного target runtime package.

Логически edge указывает как минимум:

```text
edge_id
source compatibility predicate
exact target/intermediate predicate
affected authoritative record/family/schema predicates
prerequisites/dependencies
ordered transform identity
post-transform validation obligations
immutable edge artifact/provenance identity
```

Точная machine-schema/transform realization определяется позже implementation plan; этот README не задаёт отдельный runtime registry.

Migration graph не является mutable global service или campaign-owned authority. Target package может поддерживать только direct edges — общий graph framework не обязателен.

## Deterministic path selection

Для конкретного source compatibility envelope и exact target:

1. учитываются только edges, source predicate которых доказан;
2. edge composition допустима только при точном совпадении intermediate target/source predicates и всех prerequisites;
3. selected path с cycle недопустим;
4. missing immutable transform/edge artifact делает путь неподдерживаемым;
5. один valid path выбирается;
6. несколько valid paths разрешаются только target-declared canonical path/order;
7. несколько valid paths без такого declaration дают `INDETERMINATE`;
8. shortest/newest/highest-version/lexical tie-breaker запрещён.

Обратное направление не выводится автоматически. `A -> B` не означает `B -> A`.

## Campaign versus storage migration

Campaign migration и storage migration имеют разные authority.

### Campaign

Existing-campaign migration, которая меняет creator-controlled current engine/ruleset identity или authoritative campaign semantic/native state, выполняется только campaign creator и публикуется в campaign ref.

### Storage

`storage_format_generation` и storage-default layout/marker принадлежат storage owner. Storage migration — отдельный storage-owner edge/transaction на storage-default authority.

Storage migration может быть prerequisite для campaign migration, но она:

- не мигрирует sibling campaigns;
- не меняет creator-owned campaign current identity;
- не получает campaign authority от storage ownership.

Если нужны обе операции, их success/failure независимы и должны быть отражены отдельно.

## LIVE/currentness/accepted-work prerequisites

Campaign migration готовится только от pinned current campaign HEAD и owner-qualified currentness evidence.

Она блокируется, пока:

```text
active LIVE-selected mutable authority существует
OR
CLOSED LIVE state ожидает обязательного absorption/reconciliation
```

Подготовленный migration basis становится stale при изменении campaign ref или другого required mutable owner. Такой migration пересобирается от нового current authority; force/implicit merge запрещены.

Target runtime также должен уметь безопасно интерпретировать всё сохранившееся accepted/resumable work под его frozen causal/ruleset/package/RNG/provenance semantics. Migration не может ambient-rebind, reroll, discard или реконструировать hidden reasoning ради совместимости.

## Transformation scope

Authoritative native records трансформируются только в явно объявленном edge scope.

Стабильные campaign/entity/PLAYER/event/command/resolution/continuation identities, unrelated canon/history, chronology, truth/knowledge/disclosure separation, House Rules provenance и recovery semantics сохраняются, если конкретный edge не задаёт semantics-preserving representation change.

Required branch-persistent derived/index projections можно детерминированно rebuild из подготовленного migrated authority и включить в тот же campaign tree transaction, если это допускает их owner.

Local HOT/SQLite/runtime caches не являются migration authority и rebuild/invalidated только после подтверждённой authoritative publication.

## Publication and outcomes

Migration не становится authority после локального transform/validation. Это только `PREPARED`.

Authoritative campaign publication использует существующий persistence contract:

```text
complete prepared campaign tree
-> one commit parented to pinned source HEAD H
-> one non-force campaign-ref CAS/update
```

Outcomes:

- confirmed accepted ref update -> durable success;
- rejected/ref-moved update -> old/current ref remains authority, migration не произошла;
- unknown transport result -> bounded authoritative ref read-back; blind retry запрещён;
- unreachable prepared commit/object не имеет campaign authority.

## Rollback / reverse migration

До accepted publication rollback означает просто discard подготовленного результата.

После rejected publication rollback не нужен: current ref не менялся.

После confirmed migration старый ref/checkpoint не является generic rollback authority. Downgrade/reverse поддерживается только отдельным explicit reverse edge/path и публикуется как новый forward creator-authorized campaign transaction от текущего authority.

## Migration provenance

Migration evidence является audit/history evidence, а не второй publication authority.

Логически достаточно сохранить:

```text
pinned source campaign HEAD / source envelope identity
exact target runtime/package identity
ordered edge IDs + immutable edge artifact identities
creator/authorization basis
validation outcome
```

Resulting campaign ref/commit остаётся authoritative publication identity. Запись внутри коммита не обязана и не должна циклически self-embed final hash собственного containing commit.

## No migration needed

Если exact target runtime affirmatively совместим с released campaign state и authoritative persistent transformation не требуется, отдельная migration не нужна. Сам `engine_version` либо равенство generation/schema values этого не доказывает.
