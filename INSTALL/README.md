# Установка D&D Master by Hedgelion

Public engine:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Для ChatGPT Project нужны:
- `INSTALL/PROJECT_INSTRUCTIONS.txt` → Project Instructions;
- `INSTALL/00_DND_BOOTSTRAP.md` → Project Sources как `00_DND_BOOTSTRAP.md`.

## Подключите GitHub

Откройте:
https://chatgpt.com/plugins

Подключите plugin **GitHub** и авторизуйте свой GitHub account. D&D Master использует GitHub Connector как штатный способ работы с репозиториями. Он не должен сначала пробовать `gh`, локальный git, web-обходы или другие транспорты.

При первом GitHub action для нормальной автоматической работы используйте **Always allow / Всегда разрешать**, если вариант доступен и вы доверяете этому Project.

## Что делает bootstrap

1. Выбирает последний опубликованный engine release; незатегированный `main` не используется.
2. Ищет ваши доступные кампании.
3. Если подходящее хранилище одно — использует его; если несколько — предлагает выбрать.
4. Если кампаний ещё нет — спрашивает: **создать свою кампанию или присоединиться к кампании друга?**

Технические Git-детали bootstrap обычно выполняет молча и не показывает игроку без необходимости.

## Если вы присоединяетесь к другу

Bootstrap показывает ваш GitHub username. Передайте его другу/хосту кампании; он выдаёт вам обычный GitHub access.

После принятия приглашения bootstrap повторяет только проверку доступа. Гостю не нужно настраивать инфраструктуру владельца или обслуживать engine updates.

## Если вы создаёте свою кампанию

Создайте новый GitHub repository под своим personal account. Название и visibility выбираете сами.

**Включите “Add a README”.** Этот первый GitHub-коммит позволяет D&D Master затем установить всю систему одним общим initialization commit без служебного anchor-коммита.

Если ChatGPT Codex Connector ещё не видит новый repository, владелец использует:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

Выберите свой account/repository и дайте App доступ. После этого Master продолжит автоматически.

Во время установки release копируется как единое непрозрачное дерево данных: файлы не должны изучаться или загружаться как игровой контекст. Сначала собирается полная копия release, затем вся копия проверяется одним root tree checksum, после чего добавляется служебная metadata и публикуется один D&D initialization commit. Пофайловые commits и пофайловая верификация запрещены.

## Создание игры

После настройки можно создать первую игру. Новая campaign branch создаётся автоматически; техническое имя ветки игрок придумывать не должен.

## Engine updates

Только Master владельца campaign repository обслуживает engine updates. Обновления берутся только из опубликованных release tags и устанавливаются на безопасных границах, не во время обычного игрового хода.

Гостевой Master использует уже установленную в кампании версию и не занимается обслуживанием engine.

## Troubleshooting

Сначала диагностируется GitHub Connector, а не подбирается другой транспорт:
- Connector/binding error до GitHub request → проблема подключения ChatGPT;
- GitHub 401/403 → авторизация/доступ;
- GitHub 404 для только что созданного repository → сначала проверьте доступ Codex Connector App;
- временная service/rate ошибка → повторите штатный Connector path.

Только подтверждённое отсутствие нужной возможности Connector может быть основанием искать другой реально доступный метод.

ChatGPT Memory, File Library и старые chats не являются campaign canon.
