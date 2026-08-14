# Установка D&D Master by Hedgelion

Канонический репозиторий:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Для ChatGPT Project нужны два файла:
- `INSTALL/PROJECT_INSTRUCTIONS.txt` — вставить в Project Instructions;
- `INSTALL/00_DND_BOOTSTRAP.md` — добавить в Project Sources как `00_DND_BOOTSTRAP.md`.

Остальная система и игровые кампании остаются в GitHub.

## 1. Создайте ChatGPT Project

Создайте отдельный Project для D&D Master. Project-only memory можно использовать как дополнительную изоляцию, если режим доступен; игровым каноном всё равно остаётся только GitHub.

Один ChatGPT Project может обслуживать несколько независимых кампаний.

## 2. Добавьте Project Instructions и bootstrap

Скопируйте [`PROJECT_INSTRUCTIONS.txt`](PROJECT_INSTRUCTIONS.txt) целиком в Project Instructions.

Добавьте [`00_DND_BOOTSTRAP.md`](00_DND_BOOTSTRAP.md) в Project Sources как `00_DND_BOOTSTRAP.md`.

Другие файлы репозитория в Project Sources добавлять не нужно.

## Normal player / guest: GitHub и ChatGPT

### 3. Получите GitHub access

Получите у владельца кампании/repository доступ к:
`Dandelion-Solutions/hedgelion-dnd-master`.

Используйте обычный процесс GitHub invitation/access. Гостевой ChatGPT не должен сам менять owner-side repository settings.

### 4. Подключите GitHub plugin

Откройте каталог plugins:
https://chatgpt.com/plugins

Включите/подключите plugin **GitHub** и авторизуйте свой GitHub account — именно тот account, которому предоставлен доступ к `Dandelion-Solutions/hedgelion-dnd-master`.

Underlying organization GitHub App для этого подключения — **ChatGPT Codex Connector**. Обычный игрок/guest не должен повторно устанавливать его на `Dandelion-Solutions`: organization installation управляется owner/admin и является общей инфраструктурой.

Никогда не передавайте в чат GitHub password, Personal Access Token или приватный SSH key.

### 5. Разрешите автоматические GitHub actions

При первом фактическом GitHub action ChatGPT может показать permission prompt вида **«Разрешить ChatGPT использовать GitHub?»**.

Для нормальной работы D&D Master выберите **«Всегда разрешать» / “Always allow”**, если этот persistent вариант доступен и вы доверяете этому Project setup.

Причина практическая: D&D Master автоматически читает и сохраняет campaign state через GitHub. One-time permission будет снова останавливать последующие чтения/записи подтверждениями, из-за чего automated persistence не сможет работать нормально без повторного участия пользователя.

Это постоянное разрешение относится к действиям GitHub plugin. Оно не расширяет GitHub access само по себе и не отменяет D&D Master runtime access-control policy. Выдавайте его только если доверяете Project setup.

### 6. Проверьте реальный repository access

После подключения bootstrapper обязан проверить фактический доступ к:
`Dandelion-Solutions/hedgelion-dnd-master`

до campaign discovery, создания кампании или любой попытки persistence.

Если repository недоступен, setup останавливается и показывает troubleshooting. Мастер не должен угадывать repository/canon или продолжать как будто connection работает.

Repository Write/Admin capability — только infrastructure permission. Допустимый target ref определяет runtime:
- `refs/heads/main` — только authenticated GitHub login `dkolyada`;
- `campaign/*` — по campaign creator / multiplayer access rules;
- связанные live refs — только в scope выбранной кампании и active `PLAYER_` binding.

## Owner / organization admin fallback

Этот раздел нужен только owner/admin, если organization-level GitHub App ещё не установлен на `Dandelion-Solutions`.

Underlying GitHub App: **ChatGPT Codex Connector**

Fallback installation URL:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

Owner/admin устанавливает App на `Dandelion-Solutions` и предоставляет ей доступ к:
`Dandelion-Solutions/hedgelion-dnd-master`.

Если App уже установлена на организации, guest этот URL не использует и ничего повторно не устанавливает.

## Troubleshooting

- Если GitHub plugin был подключён до переноса repository или изменения organization/repository access, сначала используйте reconnect/authorization flow для GitHub plugin.
- Не переустанавливайте organization GitHub App от имени guest без необходимости.
- После изменения GitHub App installation repository может появиться в ChatGPT не мгновенно. Сначала перепроверьте installation/repository access, затем повторите read-check.
- Если уже открытый chat сохранил старый tool binding после изменения connector-а, reload страницы или новый chat допустимы как recovery step. Это не обязательная часть обычного onboarding.
- Если GitHub account сам не имеет доступа к repository, connector/plugin это не исправит: сначала нужен repository access для этого account.

## Начало игры

После успешной проверки GitHub access создайте новый chat в этом Project и напишите, например:
- **«Начинаем новую игру»**;
- **«Покажи мои игровые сессии»**.

Bootstrapper сам выполнит campaign discovery по правилам runtime.

## Где что хранится

- Project Instructions — правила Project и runtime routing;
- `00_DND_BOOTSTRAP.md` — минимальная точка входа;
- `main` — engine/runtime, schemas, install/release documentation и пустой campaign skeleton;
- `campaign/*` — отдельные игровые миры и состояние;
- ChatGPT Memory, File Library и старые chats — не источник игрового канона.
