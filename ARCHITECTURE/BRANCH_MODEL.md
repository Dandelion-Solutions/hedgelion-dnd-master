# Модель репозиториев, release-пакетов, веток и кампаний

## Три уровня

D&D Master разделяет:

1. **Canonical public engine repository** — исходники и releases:
   `Dandelion-Solutions/hedgelion-dnd-master`
2. **Local release package** — ZIP конкретной версии, распакованный во временное рабочее окружение текущего ChatGPT-чата.
3. **Campaign storage repository** — GitHub repository пользователя/хоста, где живут только persistent игровые данные и storage metadata.

Public `main` — development state. Нормальная игра использует опубликованный release package/tag; explicit engine-owner development tests используют локальный development ZIP, а не public main как runtime.

## Local release package

Release ZIP содержит полный engine: CORE/RULES/SCHEMA/CAMPAIGN templates/INSTALL/TOOLS.

Каждый новый чат при необходимости заново материализует/распаковывает package. Нельзя считать временную файловую систему другого чата persistent storage.

Engine-файлы не копируются в campaign storage.

## Campaign-storage default branch

Storage определяется root-файлом `DND_STORAGE.yaml`.

Storage v2:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<version>"
```

Default branch — инфраструктурная точка:
- marker + возможные обычные owner-файлы вроде README;
- НЕТ требования содержать engine tree;
- НЕТ требования содержать пустой campaign skeleton.

`baseline_version` — версия по умолчанию для новых кампаний/maintenance, а не физически установленный engine.

Только authenticated repository owner обслуживает storage metadata.

## Campaign branches

Каждая игра живёт в `campaign/YYYYMMDD[-NN]`.

Branch создаётся от текущего storage default-branch HEAD для normal ancestry/parent semantics.

Первый campaign-specific commit затем заменяет унаследованное storage-содержимое на campaign tree, локально сгенерированный через `TOOLS/init_campaign.py`.

Поэтому `DND_STORAGE.yaml`, storage README и другие storage-root paths не являются campaign canon.

### Current root layout

LOCAL engine directory `CAMPAIGN/` — template source. Generator copies its CONTENTS to the output directory; output is the ROOT of campaign branch.

Новая campaign branch содержит прямо в корне `README.md`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` и другие campaign-data paths. Она не содержит дополнительный wrapper `CAMPAIGN/`.

### Legacy layout

Старые campaign branches могут хранить logical campaign tree под `CAMPAIGN/`. Bootstrap сначала ищет root `MANIFEST.yaml`, затем legacy `CAMPAIGN/MANIFEST.yaml`, после чего работает через resolved prefix/storage roots.

Открытие старой кампании не является автоматической миграцией её layout.

## Campaign creator и gameplay authority

Campaign creator = `author.login` первого campaign-specific initialization commit.

Singleplayer writes — creator-only.
Multiplayer writes — по active PLAYER rules.
Repository collaborator/Admin permission сама по себе не является gameplay authority.

Read access может давать observer/read-only режим.

## Engine identity

Storage хранит только baseline VERSION.

Конкретная published campaign хранит точную engine provenance в MANIFEST: base/integrated tag + exact source SHA + update policy.

Explicit engine-owner development test may use `dev-v<version>` with nullable SHA. Локальный development ZIP является runtime source; current public `main` не запрашивается только ради заполнения SHA.

## Engine update

Обновление не переносит engine tree между repositories.

1. Owner обнаруживает новый published tag.
2. Пользователь добавляет соответствующий Source code ZIP.
3. Local package валидируется.
4. Storage baseline_version при необходимости обновляется metadata-only.
5. Для конкретной campaign выполняются только defined data/schema migrations + manifest provenance update.
6. Engine-файлы в campaign repository не появляются.

Storage baseline может быть новее конкретной campaign.

## Guest Master

Guest не меняет storage baseline и не управляет engine migration владельца. Если exact campaign package отсутствует, guest должен получить/приложить matching ZIP.

## Concurrency и persistence

Обычный gameplay сохраняет optimistic concurrency: force=false, targeted HEAD/compare refresh, semantic reconciliation вместо blind overwrite, batched durable commits и специализированные live-scene rules.

Git history — audit/provenance. Семантическая история мира — compact campaign LOG.
