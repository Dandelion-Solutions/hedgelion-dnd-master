# Установка D&D Master by Hedgelion

Для подключения к ChatGPT Project нужны два файла:
- `PROJECT_INSTRUCTIONS.txt` — вставить в Project Instructions;
- `00_DND_BOOTSTRAP.md` — добавить в Project Sources.

Остальная система и игровой канон остаются в GitHub.

## 1. Создайте ChatGPT Project

Рекомендуется выбрать **«Память только в проекте» / Project-only memory**. Это изолирует проект от памяти и чатов за его пределами, но разговоры внутри одного Project всё ещё могут использовать друг друга как контекст.

Поэтому Project memory не считается игровым хранилищем. Канон всегда берётся из GitHub campaign branch. Один ChatGPT Project может обслуживать несколько независимых кампаний; отдельный Project на кампанию — только дополнительная опция пользователя.

В Project-only режиме File Library может быть отключена. Это не мешает D&D Master: bootstrap загружается прямо в Project Sources, а постоянное чтение и запись выполняются через GitHub app.

## 2. Добавьте Project Instructions

Скопируйте содержимое `INSTALL/PROJECT_INSTRUCTIONS.txt` в поле Project Instructions. Файл специально короче лимита 5000 символов.

Не удаляйте запрет использовать ChatGPT Memory и старые чаты как канон даже при Project-only memory.

## 3. Добавьте bootstrap

Скачайте `INSTALL/00_DND_BOOTSTRAP.md` и добавьте его в Project Sources как `00_DND_BOOTSTRAP.md`.

Не добавляйте в Project Sources весь репозиторий: launcher существует именно для lazy loading.

## 4. Подключите GitHub

Подключите GitHub app в ChatGPT и выдайте ему read/write доступ к repository.

Настройки установленных GitHub Apps:
https://github.com/settings/installations/

Откройте ChatGPT/OpenAI → **Configure** → **Repository access** и разрешите нужный repository.

Никогда не передавайте в чат GitHub password, Personal Access Token или SSH private key.

## 5. Проверьте подключение

Попросите мастера прочитать `CORE/BOOTSTRAP_RUNTIME.md` и проверить текущий `main` HEAD.

## 6. Начните игру

Если активная кампания не выбрана, мастер найдёт `campaign/*`, прочитает только их `CAMPAIGN/MANIFEST.yaml` и предложит продолжить существующую игру или создать новую.

Новая ветка получает технический ID по дате: `campaign/YYYYMMDD`; если в этот день ветка уже существует — `campaign/YYYYMMDD-02`, затем `-03` и т. д. Лор, имя мира, режим и игроки в имени ветки не кодируются.

## Игра с друзьями

Владелец repository добавляет друзей как GitHub collaborators. Каждый подключает собственный GitHub account к своему ChatGPT. Текущая архитектура исходит из того, что commits разных игроков атрибутируются их разным GitHub users.

Создатель кампании определяется по Git history как `author.login` первого campaign-specific initialization commit. Отдельное owner-поле в `MANIFEST` не хранится.

В `singleplayer` только создатель может публиковать gameplay changes; остальные collaborators могут наблюдать, но не вмешиваться. Только создатель может переключать `singleplayer ↔ multiplayer`. В `multiplayer` явно связанные игроки могут менять общий мир по shared-world правилам.

## Где что хранится

- `main` — общий engine и пустой campaign skeleton;
- `campaign/YYYYMMDD[-NN]` — конкретная игра;
- Project Sources — только bootstrap;
- ChatGPT Memory / File Library / старые чаты — не канон.

Launcher задуман как стабильный файл и обычно не требует обновления при изменениях CORE.
