# Схемы данных кампании

`SCHEMA/` описывает persistent state и протокольные записи. Во время обычного gameplay весь каталог схем не загружается; конкретная схема нужна для целевого создания, чтения, проверки или диагностики соответствующего owner record.

## Общие принципы

- Каждый значимый record имеет стабильный ID; связи хранятся по ID, а не через копирование полных записей.
- `null` означает, что значение отсутствует или ещё не установлено. Неизвестное нельзя заменять догадкой.
- Record identity задаёт точный native route. Индекс и current summary помогают найти кандидата, но не подтверждают существование, отсутствие, размещение, membership, authorization или currentness.
- `details` сохраняет только owner-разрешённые описательные данные; оно не создаёт ссылки, механику, маршруты, ограничения или автоматические индексы.
- Исторические события хранятся в `LOG`; они не являются transaction journal, transcript или заменой текущего состояния.
- Objective truth (`world.lore_fact`), fictional knowledge (`world.knowledge`), human exposure (`runtime.disclosure`) и communication (`runtime.message`) остаются отдельными owners. Visibility, possession, narration, repository readability и отдельная `Secret`-запись не создают параллельного truth/knowledge/disclosure owner.
- `STATE/CURRENT.yaml` — компактная маршрутизация по `scene_id`. У него нет campaign-global chronology frontier; exact Scene, temporal и LIVE owners определяют свои данные и currentness.

## Основные current-схемы

| Native record / контракт | Схема | Что она описывает |
|---|---|---|
| Campaign identity/config/card | [campaign_manifest.schema.yaml](campaign_manifest.schema.yaml), [campaign_config.schema.yaml](campaign_config.schema.yaml), [campaign_card.schema.yaml](campaign_card.schema.yaml) | Кампания, её конфигурацию и compact display projection. Card не выбирает authority. |
| Storage metadata | [dnd_storage.schema.yaml](dnd_storage.schema.yaml) | Storage marker/layout и portable baseline для новых кампаний. |
| Current summary | [current_state.schema.yaml](current_state.schema.yaml) | Компактные nominations активных сцен/processes; Scene route выводится по `scene_id`. |
| `world.scene` | [scene.schema.yaml](scene.schema.yaml) | Native Scene state, location, participant/focal IDs и owner-defined status/details. `STATE/RUNTIME/LIVE_ROUTING.yaml` selects LIVE currentness separately. |
| `world.location` | [location.schema.yaml](location.schema.yaml) | Native location topology/environment; Actor и Asset owners хранят собственное текущее placement. |
| `world.player` | [player.schema.yaml](player.schema.yaml) | Stable PLAYER identity/binding, controlled-PC relation, narrow preferences/grants и collaboration route references. Это не общий ACL. |
| `world.actor` / `world.asset` / `world.effect` | [actor.schema.yaml](actor.schema.yaml), [asset.schema.yaml](asset.schema.yaml), [effect.schema.yaml](effect.schema.yaml) | Current native entity state; knowledge, location placement, resource/effect lifecycle и mechanics не дублируются между owners. |
| Lore/thread/event | [lore.schema.yaml](lore.schema.yaml), [thread.schema.yaml](thread.schema.yaml), [event.schema.yaml](event.schema.yaml) | Objective proposition, narrow process state и compact semantic history. Они не заменяют knowledge/disclosure/current state. |
| LIVE physical carrier | [live_scene.schema.yaml](live_scene.schema.yaml) | Source-key/revision-bound pack of native owner states and evidence. Current route/claims remain with LIVE routing. |
| Collaboration | [collaboration_obligation.schema.yaml](collaboration_obligation.schema.yaml) | Scoped collaboration obligation state. PLAYER route references name obligations but grant no authority. |
| Recovery routing/handoff | [operational_root_routing.schema.yaml](operational_root_routing.schema.yaml), [operational_root_handoff.schema.yaml](operational_root_handoff.schema.yaml) | Bounded routes to current `runtime.command`, `runtime.procedure`, `runtime.interaction` and `runtime.intent_plan` owners; those records own lifecycle and closure. |
| Session/checkpoint/index | [session.schema.yaml](session.schema.yaml), [checkpoint.schema.yaml](checkpoint.schema.yaml), [index.schema.yaml](index.schema.yaml) | Coordination observations, optional immutable evidence and derived discovery. None selects current gameplay truth or proves completeness. |
| EVENT_INDEX | [event_index.schema.yaml](event_index.schema.yaml) | Campaign route positions plus source-local SemanticEvent admission coordinates and exact LIVE source bindings; bounded nominations remain non-authoritative. The generic family index remains separate. |
| Policy/allocation support | [house_rules_policy.schema.yaml](house_rules_policy.schema.yaml), [id_allocator.schema.yaml](id_allocator.schema.yaml) | Narrow typed policy and allocation support, each subordinate to its native owner. |

## Current retained schema targets

| Схема | Local `schema_version` |
|---|---:|
| [current_state.schema.yaml](current_state.schema.yaml) | 3 |
| [thread.schema.yaml](thread.schema.yaml) | 2 |
| [live_scene.schema.yaml](live_scene.schema.yaml) | 2 |
| [event.schema.yaml](event.schema.yaml) | 2 |
| [lore.schema.yaml](lore.schema.yaml) | 2 |
| [session.schema.yaml](session.schema.yaml) | 1 |
| [checkpoint.schema.yaml](checkpoint.schema.yaml) | 4 |
| [index.schema.yaml](index.schema.yaml) | 2 |
| [event_index.schema.yaml](event_index.schema.yaml) | 2 |
| [scene.schema.yaml](scene.schema.yaml) | 3 |
| [location.schema.yaml](location.schema.yaml) | 2 |
| [player.schema.yaml](player.schema.yaml) | 2 |

Artifact-local schema versions are independent from `engine_version`, `campaign_contract_generation` and `storage_format_generation`. Compatible optional additions may retain a version when the owner preserves semantics; incompatible released data needs an explicit owner-approved migration edge. The current v1 baseline has no pre-release v0.8 migration/compatibility obligation.
