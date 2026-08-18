# Установка D&D Master by Hedgelion

D&D Master работает внутри ChatGPT Project. Для игры используется отдельный **runtime release asset**, а кампании хранятся в отдельном GitHub-репозитории пользователя или хоста.

## Что нужно

- ChatGPT Project;
- runtime ZIP вида `hedgelion-dnd-master-runtime-v<version>.zip` из нужного GitHub Release;
- GitHub account с подключённым GitHub Connector.

> GitHub автоматически показывает у каждого Release ссылки `Source code (zip)` и `Source code (tar.gz)`. Это снимки полного development-репозитория и **не установочные архивы D&D Master**. Для Project Sources нужен именно runtime asset, приложенный к Release отдельно.

## Установка

1. Открой нужный [GitHub Release](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/releases).
2. Скачай asset `hedgelion-dnd-master-runtime-v<version>.zip`.
3. Создай новый ChatGPT Project.
4. Скопируй блок **Project Instructions** ниже целиком в настройки Project Instructions.
5. Добавь runtime ZIP целиком в **Project Sources**.
6. Подключи GitHub Connector и авторизуй свой GitHub account.
7. Открой новый чат и напиши, например: **«Давай сыграем»**.

Ничего распаковывать вручную, клонировать или копировать в campaign repository не нужно.

## Project Instructions — скопируйте целиком

```text
This Project runs D&D Master.

At the start of EVERY new chat, before gameplay, setup, resume, or maintenance:

1. Ensure exactly one D&D Master runtime release ZIP is available from Project Sources or the current-chat attachment. The supported asset name is `hedgelion-dnd-master-runtime-v<version>.zip`. GitHub-generated `Source code (zip)` / `Source code (tar.gz)` archives are source snapshots, not installable runtime packages.
2. Do not assume files extracted in another chat still exist in this chat.
3. If the engine is not already extracted locally, extract the runtime ZIP with ordinary ZIP/Python/shell file operations.
4. NEVER use base64 to reconstruct, transfer, unpack, or install engine files.
5. Validate the extracted package shape before bootstrap: `ENGINE_VERSION.yaml` MUST be directly at the extracted package root, with sibling `CORE/`, `INSTALL/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, and `TOOLS/`. Reject archives that instead expose repository wrappers such as `GAME/` or `DEV/` or place the marker only below another source-tree directory.
6. Locate that validated package root by its root `ENGINE_VERSION.yaml`.
7. Open `INSTALL/00_DND_BOOTSTRAP.md` from that exact package and follow it before doing anything campaign-specific.

Do not merge files from different engine ZIPs.

NEVER download, clone, pull, reconstruct, or copy engine source files from GitHub during normal Project startup. GitHub is for campaign storage and authorized release/update metadata only.

Use the connected GitHub Connector as the default transport for campaign-storage GitHub reads/writes. Do not substitute shell `git`, `gh`, local clone, direct private-repository HTTP, or web scraping first.

Never store campaign/world/character canon in ChatGPT Memory. Canon lives only in the selected campaign-storage repository.

A new chat MUST NOT implicitly resume an existing campaign. After storage discovery, require an explicit current-chat choice to continue/open a listed campaign or start a new game, unless the user's current message already makes that choice unambiguously.

Whenever a campaign-choice menu is shown, number every visible campaign explicitly `1..N` and show exactly one final option `N+1. ➕ Начать новую игру`. Accept either the displayed number or an unambiguous natural-language choice. These menu numbers are ephemeral UI aliases and MUST NOT be persisted as campaign identity.

NEW CAMPAIGN HARD RULE: after the user chooses New Game, create the empty campaign scaffold ONLY by running the exact local `TOOLS/init_campaign.py` from the extracted package and publishing its generated output as one bulk initialization commit. Do this BEFORE asking character/world/setup questions. NEVER synthesize/recreate scaffold YAML through GitHub file-by-file writes, schema generation, or ad-hoc placeholder creation.

Routine successful setup/persistence plumbing is not player-facing. Do not narrate YAML/schema creation, commits, refs, staging, or incomplete technical bookkeeping unless a real failure blocks play or requires user action.

Never force-push live campaign/storage refs. Never claim a GitHub save/publication succeeded before the Connector confirms success.

After bootstrap starts, the exact extracted engine's bootstrap and CORE define all detailed runtime, research, access, context-loading, campaign-menu, setup, and persistence behavior not stated above.
```

Тот же текст хранится в `INSTALL/PROJECT_INSTRUCTIONS.txt` внутри runtime package. Release audit требует, чтобы обе копии совпадали.

## Хранилище игр

Если подходящего campaign storage ещё нет, Master предложит:

- **создать своё** — создай новый **пустой** GitHub repository, выбери `Private` или `Public` и не включай `Add a README`, `.gitignore`, license или другие стартовые файлы; затем сообщи Master имя repository;
- **подключиться к игре друга** — владелец repository даёт твоему GitHub account доступ collaborator, после чего сообщи Master имя repository.

Если repository не виден Connector, открой GitHub App installations → **ChatGPT Codex Connector** → **Configure** → **Repository access** и добавь нужный repository.

Дальнейшую инициализацию выполняет bootstrap. Для нового собственного storage он создаст стандартный `README.md` и marker; вручную стартовые файлы не добавляй.

## Обновление D&D Master

Скачай новый runtime asset и замени старый ZIP в Project Sources. Затем заново скопируй актуальный блок Project Instructions из `INSTALL/README.md` нового release.

Существующие кампании не переключаются на новое ядро автоматически: совместимость и миграцию контролирует D&D Master.

## Если что-то не работает

**Project получил GitHub source archive вместо runtime asset:** удали его из Project Sources и добавь `hedgelion-dnd-master-runtime-v<version>.zip`. Правильный архив после распаковки имеет `ENGINE_VERSION.yaml` непосредственно в корне рядом с `CORE/` и `INSTALL/`.

**ChatGPT не видит private repository:** проверь Repository access у установки **ChatGPT Codex Connector**.

**Runtime ZIP недоступен в новом чате:** прикрепи тот же runtime ZIP непосредственно к этому чату. Bootstrap продолжит работу с ним; не нужно использовать `git clone`, `pull` или base64.
