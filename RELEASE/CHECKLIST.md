# Checklist engine 0.1.0

## Runtime
- [x] Project launcher указывает на GitHub runtime bootstrap и не требует регулярной ручной замены.
- [x] Новый чат умеет искать `campaign/*` и предлагать продолжить/создать игру.
- [x] Lazy loading не требует полного чтения CORE/WORLD/LOG.
- [x] Singleplayer и multiplayer имеют разные sync-policy.
- [x] `RUNTIME.md` + `AI_REASONING.md` обязательны во время gameplay.

## AI-specific reasoning
- [x] Canon/evidence отделены от plausibility и player suggestion.
- [x] `canonical / inferred / undefined / unknown-to-runtime / secret / provisional` различаются явно.
- [x] Anti-sycophancy: пользовательское давление не меняет world truth/ruling без новых оснований.
- [x] Commitment preservation запрещает тихие ретконы.
- [x] Hidden facts precommit до результата броска, когда это материально.
- [x] Counterfactual symmetry проверяет bias в пользу/против PC.
- [x] NPC assistant-helpfulness leakage запрещён.
- [x] Context discipline встроен в reasoning layer.

## GM craft
- [x] DMG 2024 campaign/session practices синтезированы в Framework.
- [x] Situation-based design / Three Clue / node / smart-prep practices встроены.
- [x] Lazy GM strong start / secrets & clues / spiral campaign / horizons встроены.
- [x] Отдельные `GM_CRAFT.md`, `LORE.md`, `CAMPAIGN_OPERATIONS.md` существуют.
- [x] Lore/history имеет truth-vs-belief и exposition-drip discipline.
- [x] Prep является provisional и disposable, а не скрытым canon.

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

## Installation package
- [x] Всё, что нужно для установки, находится в `INSTALL/`.
- [x] `INSTALL/README.md` содержит полную пользовательскую инструкцию.
- [x] `INSTALL/PROJECT_INSTRUCTIONS.txt` короче лимита ChatGPT Project 5000 символов (текущая версия: 3288 символов).
- [x] `INSTALL/00_DND_BOOTSTRAP.md` является стабильным Project Source launcher.
- [x] Корневой `README.md` является описанием/презентацией проекта, а не установочной инструкцией.
- [x] В корне больше нет установочного bootstrap-файла.

## Regression/integration
- [x] T01–T30 проверены инспекцией Framework; см. `TESTS/PRE_RELEASE_AUDIT_0.1.0.md`.
- [x] GitHub RW из обычного Project chat проверен.
- [x] Non-fast-forward stale-HEAD path фактически проверен.
- [x] Пустой campaign skeleton присутствует в `main`.
- [ ] Создание первой production campaign branch — выполнить после engine tag.

## Release
- [x] Пользовательская документация написана по-русски.
- [x] В `main` нет данных конкретной кампании.
- [x] Experimental tavern/wizard content не является engine canon.
- [x] `ENGINE_VERSION.yaml` = 0.1.0.
- [ ] Создать tag `engine-v0.1.0` на текущем финальном release HEAD.
