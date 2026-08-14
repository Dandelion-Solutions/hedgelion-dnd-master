# Установка D&D Master by Hedgelion

Public engine:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Для ChatGPT Project нужны:
- `INSTALL/PROJECT_INSTRUCTIONS.txt` → Project Instructions;
- `INSTALL/00_DND_BOOTSTRAP.md` → Project Sources как `00_DND_BOOTSTRAP.md`.

## Как теперь устроено хранение

Public engine repository содержит разработку и release tags. Игровые сессии хранятся в отдельном repository пользователя/хоста. Его имя и visibility произвольны.

Campaign-storage repository распознаётся по `DND_STORAGE.yaml` на `main`. Storage `main` содержит exact snapshot опубликованного engine release + этот marker. Реальные игры находятся в `campaign/*`.

## Подключите GitHub

Откройте:
https://chatgpt.com/plugins

Подключите plugin **GitHub** и авторизуйте свой GitHub account.

При первом GitHub action для нормальной автоматической работы D&D Master используйте **Always allow / Всегда разрешать**, если вариант доступен и вы доверяете этому Project. Разрешение относится к GitHub plugin actions и не расширяет GitHub permissions.

## Что делает bootstrap

1. Читает public engine и выбирает latest valid published tag. Untagged `main` не используется.
2. Ищет доступные repositories с root `DND_STORAGE.yaml`.
3. Если storage один — использует его; если несколько — предлагает выбрать.
4. Если storage нет — спрашивает: создать свой или присоединиться к repository другого владельца.

## Если вы присоединяетесь к другу

Bootstrap показывает ваш authenticated GitHub username. Передайте его владельцу campaign repository; владелец выдаёт вам обычный GitHub access.

После принятия invitation bootstrap повторяет discovery. Guest не меняет storage `main`, не устанавливает App за владельца и не проверяет новые engine releases во время игры.

## Если вы создаёте свой repository

Создайте новый пустой repository под своим personal GitHub account. Название и visibility выбираете сами. D&D Master не требует private repository.

Для автоматического обслуживания storage `main` первая версия требует, чтобы repository owner login совпадал с вашим authenticated login.

Если ChatGPT Codex Connector ещё не имеет доступа к новому repository, владелец использует:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

После доступа Master копирует полный tree latest published engine tag и добавляет `DND_STORAGE.yaml` с exact tag/SHA. Предпочтительно это один initial atomic commit; если connector не умеет parentless root commit, допускается минимальный технический anchor и затем один atomic D&D initialization commit. Коммит на каждый файл запрещён.

## Создание игры

Новая `campaign/YYYYMMDD[-NN]` создаётся от storage `main`. Первый campaign initialization commit удаляет `DND_STORAGE.yaml`, заполняет пустой `CAMPAIGN/` skeleton и фиксирует engine base/integrated tag/SHA.

## Engine updates

Только Master authenticated владельца campaign-storage repository выполняет update discovery.

На безопасной границе он:
1. проверяет уже установленный storage baseline;
2. при необходимости проверяет более новый public release tag;
3. по policy `ask` предлагает Update / Not now / Always update automatically;
4. Phase A: обновляет storage `main` до exact release tree, удаляя obsolete/extra engine files и сохраняя только storage-owned `DND_STORAGE.yaml`;
5. Phase B: интегрирует storage baseline в текущую campaign branch, сохраняя populated `CAMPAIGN/**` и выполняя migration при необходимости.

Storage `main` может быть новее campaign branch. Если Phase A прошла, а Phase B отложена/неудачна, rollback не выполняется.

Guest Master ничего из этого не делает.

## Troubleshooting

- `tool disabled` / `Resource not found` до GitHub request → ChatGPT connector/runtime binding; reload или новый chat допустимы. Не меняйте GitHub permissions вслепую.
- GitHub 403/forbidden → проверяйте account/App/repository access.
- После изменения App installation доступ может обновиться не мгновенно; перепроверьте installation и повторите read.
- Никогда не проверяйте write access тестовым commit.

ChatGPT Memory, File Library и старые chats не являются campaign canon.
