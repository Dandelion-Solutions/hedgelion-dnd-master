# Установка D&D Master by Hedgelion

Канонический репозиторий: `Dandelion-Solutions/hedgelion-dnd-master`.

Для подключения к ChatGPT Project нужны два файла:

- `PROJECT_INSTRUCTIONS.txt` — вставить в Project Instructions;
- `00_DND_BOOTSTRAP.md` — добавить в Project Sources.

Остальная система и игровые кампании остаются в GitHub.

## 1. Создайте ChatGPT Project

Создайте отдельный Project для D&D Master.

Рекомендуется выбрать **Project-only memory / «Память только в проекте»**, если этот режим доступен. Это дополнительная изоляция; игровым каноном всё равно остаётся только GitHub.

Один ChatGPT Project может обслуживать несколько независимых кампаний. Отдельный Project для отдельной игры допустим, но не обязателен.

## 2. Добавьте Project Instructions

Откройте [`INSTALL/PROJECT_INSTRUCTIONS.txt`](PROJECT_INSTRUCTIONS.txt), скопируйте содержимое целиком и вставьте его в Project Instructions.

Не удаляйте запрет использовать ChatGPT Memory и старые чаты как игровой канон.

## 3. Добавьте bootstrap

Добавьте [`INSTALL/00_DND_BOOTSTRAP.md`](00_DND_BOOTSTRAP.md) в Project Sources как `00_DND_BOOTSTRAP.md`.

Другие файлы репозитория в Project Sources добавлять не нужно: Мастер получает необходимые данные из GitHub по мере игры.

## 4. Подключите GitHub к ChatGPT

В ChatGPT откройте **Settings → Apps → GitHub** и подключите GitHub account, которым будете пользоваться для D&D Master.

Прямая страница настроек ChatGPT:
https://chatgpt.com/#settings/Apps

Официальная инструкция OpenAI по GitHub:
https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt

Никогда не передавайте в чат пароль GitHub, Personal Access Token или приватный SSH-ключ.

## 5. Получите доступ к репозиторию

Ваш GitHub account должен иметь доступ к `Dandelion-Solutions/hedgelion-dnd-master`.

Если репозиторий приватный и доступа нет, сообщите владельцу репозитория свой GitHub username. Владелец отдельно выдаёт нужный доступ; гостевой ChatGPT не должен менять owner-side repository settings.

После приглашения примите GitHub invitation.

## 6. Разрешите GitHub App видеть репозиторий

Если ваш GitHub account уже видит репозиторий, но ChatGPT его не находит, проверьте доступ установленного GitHub App:

https://github.com/settings/installations

Откройте ChatGPT/OpenAI GitHub App → **Configure** и разрешите доступ к `Dandelion-Solutions/hedgelion-dnd-master`.

Не проверяйте write-доступ созданием тестового файла или commit. Мастер должен сначала использовать read-only metadata/permission checks.

## 7. Проверьте подключение

Создайте чат внутри Project и попросите Мастера проверить GitHub access к `Dandelion-Solutions/hedgelion-dnd-master`.

Подключение считается пригодным для полноценной игры, когда Мастер может читать репозиторий и имеет требуемую транспортную write/push permission. Но repository permission сама по себе не даёт право менять всё подряд:

- `main` — owner-only для engine/framework изменений;
- `singleplayer campaign/*` — писать может только создатель кампании;
- `multiplayer campaign/*` — запись разрешается только по player-binding и multiplayer policy.

Эти ограничения проверяются runtime, даже если GitHub технически разрешает push.

## 8. Начните игру

Создайте новый чат в этом Project.

Можно написать, например:

- **«Начинаем новую игру»** — чтобы создать новую кампанию;
- **«Покажи мои игровые сессии»** — чтобы увидеть существующие игры и выбрать, какую продолжить.

Дальше Мастер сам найдёт нужную campaign branch или проведёт через создание новой.

## Игра с друзьями

Владелец репозитория отдельно предоставляет другу GitHub access. Друг подключает свой GitHub account к своему ChatGPT Project с теми же Project Instructions и bootstrap.

Repository collaborator access сам по себе не делает пользователя участником кампании. В `singleplayer` другие пользователи остаются наблюдателями. Для совместной игры создатель кампании включает multiplayer, после чего доступ игрока определяется persistent player binding и join policy.

## Где что хранится

- `Project Instructions` — основные правила подключения и работы с каноном;
- `00_DND_BOOTSTRAP.md` в Project Sources — маленькая точка входа;
- `main` — engine/runtime, схемы, install/release документация и пустая основа новой кампании;
- `campaign/*` — отдельные игровые миры и их состояние;
- ChatGPT Memory, File Library и старые чаты — не источник игрового канона.
