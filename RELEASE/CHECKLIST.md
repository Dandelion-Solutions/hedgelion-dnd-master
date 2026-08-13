# Checklist перед engine release

Стабильный engine tag создаётся только когда выполнены пункты ниже.

## Runtime
- [ ] Project launcher указывает на GitHub runtime bootstrap и не требует регулярной ручной замены.
- [ ] Новый чат умеет найти `campaign/*` и предложить продолжить/создать игру.
- [ ] Lazy loading не требует полного чтения CORE/WORLD/LOG.
- [ ] Singleplayer и multiplayer имеют разные sync-policy.

## Framework
- [ ] Player agency и canon boundaries определены.
- [ ] Adjudication/randomness/failure rules определены.
- [ ] NPC/dialogue/information/mystery rules определены.
- [ ] Exploration/combat/magic rules определены.
- [ ] Prep/narrative/world generation rules определены.
- [ ] Processes/world/rewards/advancement rules определены.
- [ ] Storage and multiplayer conflict rules определены.
- [ ] AI anti-patterns определены.

## Persistent data
- [ ] В `main` есть полный пустой `CAMPAIGN/` skeleton.
- [ ] Manifest/current/scene/player/PC/NPC/location/faction/item/lore/secret/thread/event/checkpoint/index schemas существуют.
- [ ] Campaign-specific house rules отделены от CORE.
- [ ] Event log остаётся компактным и не становится стенограммой.

## Rules baseline
- [ ] Rules baseline и версия SRD зафиксированы.
- [ ] Есть официальный routing/fallback для точных механик.
- [ ] Exact mechanics не выдумываются при возможности адресной проверки.

## Regression
- [ ] T01–T16 из `TESTS/REGRESSION_CASES.md` пройдены логически/инспекцией.
- [ ] Проверено чтение/запись GitHub из обычного Project chat.
- [ ] Проверен HEAD conflict/resync path хотя бы синтетически.
- [ ] Проверено создание пустой campaign branch из release base.

## Release
- [ ] README/INSTALL актуальны и написаны для пользователя по-русски.
- [ ] В `main` отсутствуют данные конкретной кампании.
- [ ] Experimental tavern/wizard content не попал в engine canon.
- [ ] Release commit помечен тегом `engine-vX.Y.Z`.
