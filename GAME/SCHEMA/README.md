# Схемы данных кампании

`SCHEMA/` описывает стабильные форматы persistent state. Во время обычного gameplay весь каталог схем не загружается; конкретная схема нужна только при создании, миграции, валидации или сомнении в формате соответствующей записи.

## Общие принципы

- Значимые сущности имеют стабильный уникальный ID.
- Связи хранятся по ID, без копирования полных записей.
- `null` означает, что значение отсутствует/ещё не установлено; неизвестный факт нельзя заменять догадкой.
- Исторические детали уходят в `LOG`; entity/state records хранят актуальное состояние.
- Objective truth, NPC/PC knowledge и player-visible information разделены.
- Независимо меняющиеся среды по возможности разделяются на разные scene/entity files.

## Основные схемы

- `campaign_manifest.schema.yaml` — идентичность ветки, mode, engine и storage roots.
- `campaign_config.schema.yaml` — premise, tone, boundaries, advancement и world mode.
- `session.schema.yaml` — координационные данные отдельного игрового чата/сессии.
- `current_state.schema.yaml` — компактный глобальный каталог активных сцен/процессов.
- `scene.schema.yaml` — состояние отдельного активного окружения/сцены.
- `player.schema.yaml` — binding пользователя к PC внутри кампании.
- `pc.schema.yaml` — player character.
- `npc.schema.yaml` — NPC.
- `location.schema.yaml` — локация.
- `faction.schema.yaml` — организация/группа.
- `item.schema.yaml` — значимый предмет.
- `lore.schema.yaml` — объективный устойчивый факт мира.
- `secret.schema.yaml` — скрытая объективная истина.
- `thread.schema.yaml` — активный процесс/угроза/проект.
- `event.schema.yaml` — компактное семантическое изменение мира.
- `checkpoint.schema.yaml` — recovery boundary.
- `index.schema.yaml` — маршрутизация к сущностям.

## Версионирование

`schema_version` относится к persistent campaign data и независим от версии Framework. Совместимое добавление необязательных полей может не требовать миграции; изменение семантики/типа обязательных данных требует новой версии и файла в `MIGRATIONS/`.
