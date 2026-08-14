# Модель репозиториев, release-пакетов, веток и кампаний

## Три уровня

D&D Master разделяет:

1. **Canonical public engine repository** — исходники и releases:
   `Dandelion-Solutions/hedgelion-dnd-master`
2. **Local release package** — ZIP конкретной версии, распакованный во временное рабочее окружение текущего ChatGPT-чата.
3. **Campaign storage repository** — GitHub repository пользователя/хоста, где живут только persistent игровые данные и storage metadata.

Public `main` — development state. Нормальная игра использует опубликованный release package/tag.

## Local release package

Release ZIP содержит полный engine: CORE/RULES/SCHEMA/CAMPAIGN templates/INSTALL/TOOLS.

Каждый новый чат при необходимости заново материализует/распаковывает пакет. Нельзя считать временную файловую систему другого чата persistent storage.

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
- НЕТ требования содержать пустой CAMPAIGN skeleton.

`baseline_version` — версия по умолчанию для новых кампаний/maintenance, а не физически установленный engine.

Только authenticated repository owner обслуживает storage metadata.

## Campaign branches

Каждая игра живёт в `campaign/YYYYMMDD[-NN]`.

Branch создаётся от текущего storage default-branch HEAD для нормальной ancestry/parent semantics.

Первый campaign-specific commit затем заменяет унаследованное storage-содержимое на campaign tree, локально сгенерированный из release package через `TOOLS/init_campaign.py`.

Поэтому `DND_STORAGE.yaml`, storage README и другие storage-root paths не являются campaign canon.

Campaign branch содержит `CAMPAIGN/**` данные, но не CORE/RULES/SCHEMA/INSTALL engine copy.

## Campaign creator и gameplay authority

Campaign creator = `author.login` первого campaign-specific initialization commit.

Singleplayer writes — creator-only.
Multiplayer writes — по active PLAYER rules.
Repository collaborator/Admin permission сама по себе не является gameplay authority.

Read access может давать observer/read-only режим.

## Engine identity

Storage хранит только baseline VERSION.

Конкретная campaign хранит точную engine provenance в MANIFEST:
- base tag/SHA;
- integrated tag/SHA;
- update policy.

Runtime должен использовать соответствующий local release ZIP. Нельзя молча запускать старую campaign на другом engine.

## Engine update

Обновление больше не является переносом дерева между repositories.

1. Master/owner обнаруживает новый published tag.
2. Пользователь добавляет соответствующий Source code ZIP в Project Sources/current chat.
3. Local package валидируется.
4. Storage baseline_version при необходимости обновляется одним metadata commit.
5. Для конкретной campaign выполняются только определённые data/schema migrations + обновление manifest provenance.
6. Engine-файлы в campaign repository не появляются.

Storage baseline может быть новее конкретной campaign.

## Guest Master

Guest не меняет storage baseline и не управляет engine migration владельца.

Если exact campaign engine package отсутствует, guest должен получить/приложить matching release ZIP; он не заменяет его произвольной более новой версией.

## Concurrency и persistence

Обычный gameplay сохраняет optimistic concurrency:
- `force=false`;
- targeted HEAD/compare refresh;
- semantic reconciliation вместо blind overwrite;
- batched durable commits;
- специализированные live-scene rules для race-sensitive multiplayer state.

Git history — audit/provenance. Семантическая история мира — компактный `CAMPAIGN/LOG/`.
