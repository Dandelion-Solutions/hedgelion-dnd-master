# Схемы данных кампании

`SCHEMA/` описывает стабильные форматы persistent state. Во время обычного gameplay весь каталог схем не загружается; конкретная схема нужна только при создании, миграции, валидации или сомнении в формате соответствующей записи.

## Общие принципы

- Значимые сущности имеют стабильный уникальный ID.
- Связи хранятся по ID, без копирования полных записей.
- `null` означает, что значение отсутствует/ещё не установлено; неизвестный факт нельзя заменять догадкой.
- Исторические детали уходят в `LOG`; entity/state records хранят актуальное состояние.
- Objective truth, NPC/PC knowledge и player-visible information разделены; отдельная `Secret`-запись не является самостоятельным владельцем truth/knowledge/disclosure.
- Независимо меняющиеся среды по возможности разделяются на разные scene/entity files.

## Основные схемы

- `campaign_manifest.schema.yaml` — идентичность ветки, mode, engine и storage roots.
- `campaign_config.schema.yaml` — premise, tone, boundaries, advancement и world mode.
- `house_rules_policy.schema.yaml` — узкий machine-readable companion для identity/currentness/adoption/routing evidence House Rules/Rulings; нормативный текст остаётся в `RULES/HOUSE_RULES.md`.
- `session.schema.yaml` — координационные данные отдельного игрового чата/сессии.
- `current_state.schema.yaml` — компактный глобальный каталог активных сцен/процессов.
- `scene.schema.yaml` — состояние отдельного активного окружения/сцены.
- `player.schema.yaml` — binding пользователя к PC внутри кампании и узкие campaign authorization grants, не общий ACL.
- `pc.schema.yaml` — player character.
- `npc.schema.yaml` — NPC.
- `location.schema.yaml` — локация.
- `faction.schema.yaml` — организация/группа.
- `item.schema.yaml` — значимый предмет.
- `lore.schema.yaml` — объективный устойчивый факт мира.
- `thread.schema.yaml` — активный процесс/угроза/проект.
- `event.schema.yaml` — компактное семантическое изменение мира.
- `checkpoint.schema.yaml` — recovery boundary.
- `index.schema.yaml` — маршрутизация к сущностям.

## Версионирование

Artifact-local `schema_version` относится только к конкретному persistent/protocol contract и независим от `engine_version`. Совместимое добавление необязательных полей может не требовать local schema bump; breaking изменение обязательной формы/семантики требует новой local schema version и, если released persisted data нуждается в преобразовании, явного migration edge.

Campaign-wide persistent compatibility отдельно выражается через `campaign_contract_generation`; текущая new-campaign generation — `2`. Storage-repository marker/layout compatibility отдельно выражается через `storage_format_generation`; текущая storage generation — `3`. Эти поколения не заменяют local `schema_version` и не выводятся друг из друга или из engine version.
