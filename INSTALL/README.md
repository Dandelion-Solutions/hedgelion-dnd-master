# Установка Hedgelion D&D Master

Этот каталог содержит только материалы подключения engine к ChatGPT Project.

Для обычной установки нужны два файла:

- `PROJECT_INSTRUCTIONS.txt` — вставить в Project Instructions;
- `00_DND_BOOTSTRAP.md` — добавить в Project Sources.

Остальные данные и Framework остаются в GitHub и подгружаются мастером по мере необходимости.

## 1. Создайте ChatGPT Project

Создайте отдельный Project для D&D-кампаний. В нём будут находиться игровые чаты и минимальная стартовая конфигурация.

## 2. Добавьте Project Instructions

Откройте `INSTALL/PROJECT_INSTRUCTIONS.txt`, скопируйте его содержимое целиком и вставьте в поле Project Instructions.

Файл специально держится короче технического лимита ChatGPT Project в 5000 символов. Подробные правила AI reasoning, GM craft, хранения и синхронизации находятся в `CORE/` и не дублируются в Project Instructions.

## 3. Добавьте launcher в Project Sources

Скачайте файл `INSTALL/00_DND_BOOTSTRAP.md` и добавьте его в Project Sources.

После загрузки он должен быть доступен проекту как `00_DND_BOOTSTRAP.md`.

Не добавляйте в Project Sources весь GitHub-репозиторий, `CORE/`, `CAMPAIGN/` или историю сессий. Launcher нужен именно для того, чтобы агент находил остальное через GitHub с lazy loading.

## 4. Подключите GitHub к ChatGPT

Подключите GitHub app в ChatGPT и разрешите ему доступ к репозиторию, где находится Hedgelion D&D Master.

Страница GitHub с установленными приложениями:

https://github.com/settings/installations/

Откройте нужную установку ChatGPT/OpenAI → **Configure** → **Repository access** и либо выберите репозиторий вручную, либо разрешите доступ к нужной группе репозиториев.

Для полноценной работы мастеру необходим доступ к содержимому репозитория на чтение и запись: он должен уметь читать, создавать и обновлять файлы и ветки кампаний.

Никогда не передавайте в чат пароль GitHub, Personal Access Token или приватный SSH-ключ.

## 5. Проверьте подключение

В чате внутри Project можно попросить мастера проверить GitHub repository и текущий engine HEAD. Он должен уметь прочитать `CORE/BOOTSTRAP_RUNTIME.md` через connected GitHub app.

Если repository недоступен, сначала проверьте `Repository access` на странице GitHub Apps.

## 6. Начните игру

Откройте новый чат внутри Project и скажите, что хотите играть.

Если активная кампания не выбрана, мастер:

1. найдёт ветки `campaign/*`;
2. прочитает только `CAMPAIGN/MANIFEST.yaml` каждой найденной игры;
3. покажет краткий список существующих кампаний;
4. предложит продолжить одну из них или создать новую.

Если campaign-веток ещё нет, начнётся создание новой игры из пустого `CAMPAIGN/` skeleton стабильной версии engine.

## Что хранится где

`Project Instructions` — только короткая политика загрузки и канона.

`00_DND_BOOTSTRAP.md` в Project Sources — стабильный launcher к GitHub runtime.

`main` в GitHub — общий engine, AI reasoning, GM craft, schemas, tests и пустой campaign skeleton.

`campaign/<name>` — конкретный мир, персонажи, состояние, события, secrets и checkpoints одной игры.

ChatGPT Memory не используется как хранилище игрового канона.

## Обновление engine

Общие улучшения делаются в `main`. Стабильные версии фиксируются engine tag. Живые campaign-ветки могут получать новые общие правила отдельно, обычно через merge с `main` или по описанной в Framework процедуре миграции.

Launcher задуман как максимально стабильный файл: его не нужно заменять при каждом изменении CORE. Ручное обновление Project Source требуется только если изменился сам launcher/protocol подключения.

## Для другого пользователя

Если вы делитесь репозиторием или его клоном с другим игроком, ему нужны:

1. доступ к соответствующему GitHub repository;
2. отдельный ChatGPT Project с этим `PROJECT_INSTRUCTIONS.txt`;
3. `00_DND_BOOTSTRAP.md` в Project Sources;
4. GitHub app с нужными правами на repository.

После этого один и тот же engine может обслуживать отдельные кампании или общий multiplayer-мир через разные `campaign/*` ветки.
