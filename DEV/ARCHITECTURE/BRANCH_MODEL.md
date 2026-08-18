# Модель репозиториев, release-пакетов, веток и кампаний

## Три уровня

D&D Master разделяет:

1. **Canonical public engine repository** — development source tree и GitHub Releases: `Dandelion-Solutions/hedgelion-dnd-master`.
2. **Local runtime package** — custom Release Asset `hedgelion-dnd-master-runtime-v<version>.zip`, распакованный во временное рабочее окружение текущего ChatGPT-чата.
3. **Campaign storage repository** — GitHub repository пользователя/хоста, где живут только persistent игровые данные и storage metadata.

Public `main` — development state. Нормальная игра использует опубликованный runtime asset/tag; explicit engine-owner development tests могут использовать локальный development package.

## Source repository layout

Development repository физически разделён на `GAME/` и `DEV/`.

- `GAME/` — точное source tree runtime distribution; builder архивирует **содержимое** `GAME/`, поэтому в установленном ZIP нет wrapper `GAME/`.
- `DEV/` — architecture, tests, release policy, development catalogs/schemas и developer tooling; эта ветка дерева в runtime asset не попадает.

GitHub-generated source archives содержат обе области и не являются runtime packages.

## Local runtime package

Runtime asset содержит `ENGINE_VERSION.yaml` непосредственно в корне рядом с `CORE/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, `INSTALL/`, runtime `TOOLS/` и package support data.

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

Default branch — инфраструктурная точка: marker + возможные обычные owner-файлы вроде README; engine tree и пустой campaign skeleton там не требуются.

`baseline_version` — версия по умолчанию для новых кампаний/maintenance, а не физически установленный engine.

## Campaign branches

Каждая игра живёт в `campaign/YYYYMMDD[-NN]`.

Branch создаётся от текущего storage default-branch HEAD. Первый campaign-specific commit затем заменяет унаследованное storage-содержимое на campaign tree, локально сгенерированный через package-root `TOOLS/init_campaign.py`.

LOCAL runtime directory `CAMPAIGN/` — template source. Generator copies its CONTENTS to the ROOT of campaign branch. Новая campaign branch содержит прямо в корне `README.md`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` и другие campaign-data paths; wrapper `CAMPAIGN/` не создаётся.

Legacy branches могут хранить logical campaign tree под `CAMPAIGN/`; bootstrap сначала ищет root `MANIFEST.yaml`, затем legacy `CAMPAIGN/MANIFEST.yaml`.

## Campaign creator и gameplay authority

Campaign creator = `author.login` первого campaign-specific initialization commit.

Singleplayer writes — creator-only. Multiplayer writes — по active PLAYER rules. Repository collaborator/Admin permission сама по себе не является gameplay authority.

## Engine identity

Storage хранит только baseline VERSION. Published campaign хранит точную engine provenance в MANIFEST: base/integrated tag + exact source SHA + update policy.

Explicit engine-owner development test may use `dev-v<version>` with nullable SHA. Current public `main` не запрашивается только ради заполнения SHA.

## Engine update

Обновление не переносит engine tree между repositories.

1. Owner обнаруживает новый published tag.
2. Пользователь добавляет matching runtime Release Asset.
3. Local package валидируется по root marker/layout/version.
4. Storage baseline_version при необходимости обновляется metadata-only.
5. Для конкретной campaign выполняются только defined data/schema migrations + manifest provenance update.
6. Engine-файлы в campaign repository не появляются.

Storage baseline может быть новее конкретной campaign.

## Guest Master

Guest не меняет storage baseline и не управляет engine migration владельца. Если exact campaign package отсутствует, guest должен получить/приложить matching runtime asset.

## Concurrency и persistence

Обычный gameplay сохраняет optimistic concurrency: force=false, targeted HEAD/compare refresh, semantic reconciliation вместо blind overwrite, batched durable commits и специализированные live-scene rules.

Git history — audit/provenance. Семантическая история мира — compact campaign LOG.
