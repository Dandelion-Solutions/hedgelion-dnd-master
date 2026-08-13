# Checklist engine 0.1.0

## Runtime
- [x] Project launcher указывает на GitHub runtime bootstrap и не требует регулярной ручной замены.
- [x] Новый чат умеет искать `campaign/*` и предлагать продолжить/создать игру.
- [x] Lazy loading не требует полного чтения CORE/WORLD/LOG.
- [x] Singleplayer и multiplayer имеют разные sync-policy.

## Framework
- [x] Player agency и canon boundaries.
- [x] Adjudication/randomness/failure rules.
- [x] NPC/dialogue/information/mystery rules.
- [x] Exploration/encounters/combat/magic rules.
- [x] Prep/narrative/world generation.
- [x] Processes/rewards/advancement/safety.
- [x] Storage/multiplayer conflict rules.
- [x] AI anti-patterns.

## Persistent data
- [x] Полный пустой `CAMPAIGN/` skeleton находится в `main`.
- [x] Manifest/config/current/scene/session/player/PC/NPC/location/faction/item/lore/secret/thread/event/checkpoint/index schemas существуют.
- [x] Campaign-specific house rules отделены от CORE.
- [x] Event log остаётся компактным и не является стенограммой.

## Rules baseline
- [x] D&D 2024 / SRD 5.2.1 зафиксирован.
- [x] Есть rules routing к exact mechanics/official source.
- [x] Реальный RNG обязателен для DM dice.
- [x] SRD attribution присутствует.

## Regression/integration
- [x] T01–T16 проверены инспекцией Framework; см. `TESTS/PRE_RELEASE_AUDIT_0.1.0.md`.
- [x] GitHub RW из обычного Project chat проверен.
- [x] Non-fast-forward stale-HEAD path фактически проверен.
- [x] Пустой campaign skeleton фактически присутствует в `main`.
- [ ] Создание первой production campaign branch — выполнить после engine tag, без отдельной мусорной test branch.

## Release
- [x] README/INSTALL актуальны и написаны для пользователя по-русски.
- [x] В `main` нет данных конкретной кампании.
- [x] Experimental tavern/wizard content не является engine canon.
- [x] `ENGINE_VERSION.yaml` = 0.1.0.
- [ ] Создать tag `engine-v0.1.0` на финальном release SHA.
