# Установка D&D Master by Hedgelion

D&D Master работает внутри ChatGPT Project. Engine поставляется готовым GitHub Release ZIP, а кампании хранятся отдельно в GitHub repository пользователя/хоста.

Терминал, `git clone`, ручное копирование engine в campaign repository и base64 для установки не нужны.

## Установка Project

1. Скачайте **Source code (zip)** нужного D&D Master Release.
2. Создайте ChatGPT Project.
3. Скопируйте `INSTALL/PROJECT_INSTRUCTIONS.txt` из этого release в Project Instructions.
4. Добавьте ZIP целиком в Project Sources.
5. Подключите GitHub plugin / Connector и авторизуйте свой GitHub account.
6. Откройте новый чат и напишите: **«Давай сыграем в D&D»**.

Новый чат при необходимости заново распакует package локально. Engine в campaign repository не копируется.

## Если storage ещё нет

Master спросит: **«Создать своё хранилище игр или подключиться к игре друга?»**

Для своего storage создайте обычный repository в личном GitHub account; рекомендуется Private + Add a README. Сообщите Master имя repository. Он создаст только маленький storage marker.

Для игры друга владелец добавляет ваш GitHub account collaborator и сообщает имя repository. Guest не исправляет marker/инфраструктуру владельца.

## Новая campaign

Каждая игра живёт в отдельной `campaign/*` branch. Данные игры находятся прямо в корне этой branch — без дополнительной папки `CAMPAIGN/`.

При первой настройке Master проведёт несколько видимых этапов: персонаж, минимальная стартовая часть мира, первая сцена. После каждого завершённого этапа результат можно зафиксировать, поэтому не требуется один длинный скрытый процесс подготовки.

## Updates

Для нового release замените/добавьте новый Source code ZIP и обновите Project Instructions из того же release. Existing campaigns сохраняют свою engine identity и мигрируются отдельно только при разрешённом maintenance.

Если ChatGPT не видит новый private repository, владелец должен дать GitHub App доступ к нему. Master не лечит отсутствие ZIP через clone/pull или копирование engine-файлов из GitHub.
