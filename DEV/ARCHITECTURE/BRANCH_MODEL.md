# Модель репозиториев, runtime-пакетов, веток и кампаний

Status: **CURRENT DERIVATIVE ARCHITECTURE PROJECTION**

Этот документ — компактная проекция текущих владельцев. Он не заменяет `DND_STORAGE`/campaign schemas, runtime-selection/storage-baseline canonical amendment, WP-11 storage topology, Step-5 publication, WP-16 access/live semantics или WP-19 canonical creation specification. При конфликте owning source имеет приоритет.

## Три уровня

D&D Master разделяет:

1. **Canonical public engine repository** — development source tree и GitHub Releases: `Dandelion-Solutions/hedgelion-dnd-master`.
2. **Local runtime package** — validated `hedgelion-dnd-master-runtime-v<version>.zip` / compatible development package, распакованный во временное рабочее окружение текущего чата.
3. **Campaign storage repository** — GitHub repository пользователя/хоста, где живут persistent campaign data и storage metadata, но не engine tree.

`GAME/` — source runtime distribution; builder архивирует его содержимое в package root. `DEV/` в runtime asset не входит. GitHub source archives не являются runtime packages.

## Local runtime package

Validated package root содержит `ENGINE_VERSION.yaml`, generated `RUNTIME_PACKAGE.yaml`, `CORE/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, `INSTALL/`, runtime `TOOLS/` и package support data.

`RUNTIME_PACKAGE.yaml` — transport/provenance metadata конкретного package. Для creation exact identity включает как минимум:

```text
engine_version
package_id
source_commit_sha | null
package_sha256
ruleset_set_sha256
```

Временный `current_runtime_root` — session/environment state и не является campaign/storage metadata.

Engine files никогда не копируются в campaign storage.

## Campaign-storage default branch

Storage определяется root `DND_STORAGE.yaml` schema v3.

Current portable baseline shape conceptually:

```yaml
storage_format_version: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "<version>"
    package_id: "<package-id>"
    source_commit_sha: "<sha-or-null>"
    package_sha256: "<sha256>"
    adopted_at: "<timestamp>"
```

`engine.baseline` — storage-owner-approved default runtime identity **для новых кампаний только**. Он не выбирает, не обновляет и не переписывает runtime существующей campaign.

Default branch остаётся инфраструктурной точкой: storage marker + обычные owner-файлы вроде README. Engine tree и пустой campaign skeleton там не нужны.

## Campaign branches

Каждая current-layout campaign живёт на `campaign/YYYYMMDD[-NN]`.

Creation composition принадлежит WP-19:

```text
pin storage default HEAD H
 -> explicit New Game
 -> resolve exact validated local package from storage baseline
 -> freeze creation envelope
 -> run that package's TOOLS/init_campaign.py once
 -> complete generated campaign tree FROM SCRATCH
 -> one initialization commit parent=H
 -> one non-force campaign-ref publication
```

Branch создаётся/публикуется с neutral technical name; имя ветки не несёт lore/mode/player-count/owner authority.

Generator copies contents of package `CAMPAIGN/` to campaign branch root. Current campaign root содержит directly `README.md`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` и другие campaign-data paths; wrapper `CAMPAIGN/` не создаётся.

Historical legacy nested campaign layouts могут существовать только по совместимым legacy rules. Их наличие не меняет current-layout creation law.

## Campaign creator и gameplay authority

Campaign creator = `author.login` первого campaign-specific initialization commit.

MANIFEST/card не дублируют creator как authority; их creator/participant projections — hints/caches.

- singleplayer gameplay publication — creator-only;
- multiplayer gameplay publication — только по current active PLAYER authority;
- repository collaborator/Admin/Write permission сама по себе не является gameplay authority;
- campaign creation не даёт engine-maintainer или storage-default-branch maintenance authority.

Точные access/policy rules принадлежат `DEV/ARCHITECTURE/ACCESS_CONTROL.md` и WP-16.

## Campaign engine / ruleset identity

New campaign materializes exact creation identity into MANIFEST:

```text
engine.created_with
engine.current
ruleset.created_with.ruleset_set_sha256
ruleset.current.ruleset_set_sha256
```

`engine.current` / `ruleset.current` — current portable campaign identities; local extraction path не персистится.

Existing campaign runtime выбирается из `MANIFEST.engine.current`, а не из storage baseline, branch name, current public branch/tag или "latest" package.

Source SHA может быть null только когда это truthful package provenance; runtime не делает tag archaeology или network lookup только ради заполнения SHA.

## Engine / ruleset evolution

Этот документ не владеет migration/compatibility policy.

- clean creation-side identity/materialization — WP-19;
- existing campaign package/ruleset adoption uses current `ENGINE_UPDATES.md`/owning update contracts;
- future released-campaign schema/engine/ruleset migration/evolution audit — WP-20.

Storage baseline может изменяться независимо как owner metadata for future NEW campaigns and не меняет уже существующую campaign автоматически.

## Guest / non-owner use

Guest не меняет storage baseline и не получает owner/migration authority из технического GitHub доступа. Если required exact campaign package отсутствует, runtime следует current package-resolution/update contract; он не подменяет campaign identity ближайшей доступной версией.

## Concurrency и persistence

Initial blank scaffold — единственное current from-scratch campaign-tree publication исключение.

После initialization обычный campaign persistence использует existing base-tree delta / optimistic currentness / non-force publication semantics и specialized live-scene ownership where applicable.

Git history — transport/audit/provenance evidence. Семантическая история мира принадлежит campaign historical owners, включая compact `LOG/SemanticEvent`; Git chronology сама по себе не является fictional chronology.