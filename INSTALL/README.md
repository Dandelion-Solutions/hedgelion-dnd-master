# Установка D&D Master by Hedgelion

D&D Master работает внутри ChatGPT Project. Engine поставляется готовым GitHub Release ZIP, а кампании хранятся отдельно в GitHub repository пользователя/хоста.

Терминал, `git clone`, ручное копирование engine в campaign repository и base64 для установки не нужны.

## Что понадобится

- ChatGPT с Projects;
- GitHub account;
- GitHub plugin / Connector в ChatGPT;
- опубликованный D&D Master release **Source code (zip)**.

## 1. Скачайте release ZIP

Откройте нужный Release в:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Скачайте **Source code (zip)**.

Не распаковывайте и не перекладывайте отдельные engine-файлы в GitHub campaign repository.

## 2. Создайте ChatGPT Project

Создайте новый Project.

Скопируйте содержимое `INSTALL/PROJECT_INSTRUCTIONS.txt` выбранного release в **Project Instructions**.

Проще всего получить этот текст, открыв файл на GitHub в том же release tag либо локально посмотрев его внутри скачанного ZIP.

## 3. Добавьте ZIP в Project Sources

Добавьте скачанный Source code ZIP целиком в **Project Sources**.

Рекомендуется хранить там текущий release ZIP. Если старая campaign остаётся pinned на предыдущей версии, можно также сохранить соответствующий старый ZIP; Bootstrap выберет нужный release.

Если Project Source ZIP по ограничениям текущего ChatGPT не удаётся материализовать в конкретном чате, Master попросит приложить тот же ZIP непосредственно к этому чату.

Не рассчитывайте, что распакованная временная рабочая папка другого чата сохранится: новый чат при необходимости распакует release снова.

## 4. Подключите GitHub

Откройте:
https://chatgpt.com/plugins

Подключите plugin **GitHub** и авторизуйте свой GitHub account.

Если доверяете этому Project, при запросе доступа можно выбрать **Always allow / Всегда разрешать**.

## 5. Начните игру

Откройте новый чат в Project и напишите, например:

> Давай сыграем в D&D.

Master:
- распакует локальный engine release;
- запустит Bootstrap из архива;
- найдёт доступное campaign storage;
- предложит продолжить игру или создать новую.

## Если campaign storage ещё нет

Master спросит:

**«Создать своё хранилище игр или подключиться к игре друга?»**

### Своё хранилище

Создайте новый repository в своём личном GitHub account.

Рекомендуется:
- `Private`;
- произвольное имя;
- включить **Add a README**.

Вернитесь и сообщите имя repository.

Master создаст маленький storage marker. Engine в repository копироваться не будет.

Если ChatGPT не видит новый repository, владелец выдаёт Codex Connector App доступ:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

### Подключиться к другу

Master покажет ваш GitHub username.

Передайте его владельцу storage. Владелец добавляет вас collaborator и сообщает имя repository.

После получения доступа Master проверит storage marker и покажет доступные игры.

Если marker отсутствует, guest ничего не исправляет: владелец должен корректно инициализировать своё D&D storage.

## Создание новой игры

Новая campaign создаётся автоматически.

Master локально генерирует полный начальный `CAMPAIGN/` scaffold из release ZIP и публикует его одним GitHub commit. Игроку не нужно вручную создавать папки/файлы.

## Обновление D&D Master

Когда выходит новый release:

1. скачайте новый **Source code (zip)**;
2. замените/добавьте ZIP в Project Sources;
3. обновите Project Instructions содержимым `INSTALL/PROJECT_INSTRUCTIONS.txt` нового release;
4. откройте новый чат.

Storage owner при безопасной возможности сможет обновить baseline и отдельно мигрировать конкретные campaigns.

Если campaign остаётся на старой версии, сохраните/приложите matching старый release ZIP.

## Если что-то не работает

Проверьте:
- ZIP release доступен в Project Sources или приложен к текущему чату;
- Project Instructions взяты из нужной версии;
- GitHub plugin подключён к правильному account;
- App имеет доступ к нужному repository;
- invitation друга принята.

Master не должен пытаться лечить отсутствие ZIP через clone/pull или пофайловое копирование engine из GitHub.
