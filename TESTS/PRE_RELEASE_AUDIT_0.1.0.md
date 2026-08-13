# Pre-release audit engine 0.1.0

Дата: 2026-08-13
Цель: проверить, что `main` пригоден как чистая база до создания первой campaign-ветки.

## Regression cases

T01 PASS — reward bait запрещён `REWARDS.md`/`PREP.md`.
T02 PASS — вопрос игрока не создаёт удобный NPC/событие (`RUNTIME.md`, `ANTIPATTERNS.md`).
T03 PASS — мотив невезучего мага не подменяет RNG без явной механики (`RANDOMNESS.md`, `MAGIC.md`, `CHARACTER.md`).
T04 PASS — knowledge boundaries явно разделены (`NPC.md`, `INFORMATION.md`, schemas secret/NPC/PC).
T05 PASS — roll только при реальной неопределённости и значимой цене (`ADJUDICATION.md`).
T06 PASS — social roll не mind control (`DIALOGUE.md`, `ADJUDICATION.md`).
T07 PASS — one-clue chokepoint запрещён, важные выводы имеют резервные маршруты (`INFORMATION.md`, `PREP.md`).
T08 PASS — старый NPC восстанавливается index -> exact record -> bounded log, а не полной историей (`STORAGE.md`, bootstrap).
T09 PASS by design — независимые multiplayer changes объединяются после HEAD compare (`MULTIPLAYER.md`, `STORAGE.md`).
T10 PASS by design — уникальный предмет не может иметь двух владельцев; stale action переоценивается по новому канону.
T11 PASS by design — независимые index entries являются структурно mergeable.
T12 PASS by design — несовместимое одновременное перемещение NPC требует semantic adjudication, не text merge.
T13 PASS / tool verified — поиск `campaign/*` на чистом repo выполнен; список пуст, что соответствует new-campaign flow.
T14 PASS — lazy loading задан во всех entrypoint/storage правилах.
T15 PASS — commit-per-turn удалён; persistence batching является правилом.
T16 PASS — race-sensitive shared change в multiplayer публикуется сразу после логического завершения.

## GitHub integration

PASS — приватный repository доступен через connected GitHub app с admin/push permissions.
PASS — create/read/update operations фактически выполнены в обычном Project chat.
PASS — tree -> commit -> fast-forward ref использован для пакетных engine commits.
PASS — stale-writer smoke test: создан конкурентный commit от старого parent; попытка update `main` с `force=false` вернула GitHub 422 `Update is not a fast forward`; текущий `main` остался неизменным.

## Campaign skeleton

PASS — `main` содержит пустые MANIFEST/CONFIG/CURRENT, scene/tactical dirs, session/log/checkpoint templates, indexes, WORLD directories, campaign house-rules file.
PASS — конкретных PC/NPC/location/world facts в `main` нет.
PASS — экспериментальные tavern/wizard данные не импортированы.

## Rules

PASS — baseline закреплён как D&D 2024 / SRD 5.2.1.
PASS — точные механики не должны выдумываться; rules routing ведёт к stored mechanics или official source.
PASS — SRD attribution добавлена.
PASS — DM-generated dice требуют реальный RNG tool; число нельзя придумывать языковой моделью.

## Remaining external step

Текущий GitHub connector не предоставляет write-операции создания `refs/tags/*`. Поэтому после финального release commit пользователь должен один раз создать tag `engine-v0.1.0` на указанный SHA. Это не влияет на runtime; tag нужен как стабильная база для новых campaign branches.

Создание первой реальной `campaign/<name>` ветки намеренно не выполнялось в smoke test, чтобы не засорять репозиторий тестовой веткой. Первое создание campaign branch одновременно будет production-проверкой этого шага.
