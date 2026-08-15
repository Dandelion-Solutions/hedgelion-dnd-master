# Установка D&D Master by Hedgelion

D&D Master работает внутри ChatGPT Project. Ядро поставляется готовым **GitHub Release ZIP**, а игровые кампании хранятся отдельно в GitHub-репозитории пользователя или хоста.

## Что нужно

- ChatGPT Project;
- скачанный **Source code (zip)** нужного D&D Master Release;
- GitHub account с подключённым GitHub Connector.

## Установка

1. Создайте новый ChatGPT Project.
2. Скопируйте блок **Project Instructions** ниже целиком в настройки Project Instructions.
3. Добавьте скачанный release ZIP целиком в **Project Sources**.
4. Подключите GitHub Connector и авторизуйте свой GitHub account.
5. Откройте новый чат и напишите, например: **«Давай сыграем»**.

Ничего распаковывать вручную, клонировать или копировать в campaign repository не нужно.

## Project Instructions — скопируйте целиком

```text
This Project runs D&D Master.

At the start of EVERY new chat, before gameplay, setup, resume, or maintenance:

1. Ensure one D&D Master release ZIP is available from Project Sources or the current-chat attachment.
2. Do not assume files extracted in another chat still exist in this chat.
3. If the engine is not already extracted locally, extract the ZIP with ordinary ZIP/Python/shell file operations.
4. NEVER use base64 to reconstruct, transfer, unpack, or install engine files.
5. Locate the extracted engine root by `ENGINE_VERSION.yaml`.
6. Open `INSTALL/00_DND_BOOTSTRAP.md` from that exact package and follow it before doing anything campaign-specific.

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

Тот же текст хранится в `INSTALL/PROJECT_INSTRUCTIONS.txt` внутри release для проверки/автоматизации. Для обычной установки искать этот файл не требуется — достаточно блока выше.

## Хранилище игр

Если подходящего campaign storage ещё нет, Master предложит:

- **создать своё** — создайте новый **пустой** GitHub repository, выберите `Private` или `Public` по своему желанию и не включайте `Add a README`, `.gitignore`, license или другие стартовые файлы; затем сообщите Master имя repository;
- **подключиться к игре друга** — владелец repository даёт вашему GitHub account доступ collaborator, после чего вы сообщаете Master имя repository.

Дальнейшую инициализацию выполняет bootstrap. Для нового собственного storage он сам создаст полезный `README.md` и служебный marker; вручную добавлять стартовые файлы не нужно.

## Обновление D&D Master

Скачайте ZIP нового release и замените старый ZIP в Project Sources. Затем заново скопируйте актуальный блок Project Instructions из `INSTALL/README.md` этого release.

Существующие кампании не переключаются на новое ядро автоматически: совместимость и миграцию контролирует сам D&D Master.

## Если что-то не работает

**ChatGPT не видит private repository:** проверьте, что GitHub App/Connector получил доступ именно к этому repository.

**Project Source ZIP недоступен в новом чате:** прикрепите тот же ZIP непосредственно к этому чату. Bootstrap продолжит работу с ним; не нужно использовать `git clone`, `pull` или base64.
