# Установка D&D Master by Hedgelion

D&D Master работает внутри ChatGPT Project и хранит кампании в GitHub. Для установки не нужны терминал, команды `git`, локальный clone или ручное редактирование игровых файлов.

## Что понадобится

- аккаунт ChatGPT с возможностью создавать Projects;
- аккаунт GitHub;
- подключённый к ChatGPT GitHub plugin / Connector;
- если вы хотите вести свои кампании — возможность создать repository в своём личном GitHub account.

## 1. Создайте ChatGPT Project

Создайте новый Project в ChatGPT. Название можно выбрать любое.

## 2. Добавьте два установочных файла

Откройте нужный опубликованный release D&D Master в repository:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Берите оба файла **из одного и того же release tag**, не из development-ветки `main`.

1. Скопируйте содержимое `INSTALL/PROJECT_INSTRUCTIONS.txt` в **Project Instructions**.
2. Добавьте `INSTALL/00_DND_BOOTSTRAP.md` в **Project Sources** под именем `00_DND_BOOTSTRAP.md`.

На этом установка самого ChatGPT Project закончена.

## 3. Подключите GitHub

Откройте:
https://chatgpt.com/plugins

Подключите plugin **GitHub** и авторизуйте свой GitHub account.

При первом запросе ChatGPT на доступ к GitHub для обычной автоматической работы удобно выбрать **Always allow / Всегда разрешать**, если этот Project ваш и вы ему доверяете.

## 4. Начните игру

Откройте новый чат внутри созданного Project и напишите, например:

> Давай сыграем в D&D.

Мастер проверит доступные вам кампании и проведёт дальше по настройке. Если кампаний ещё нет, он предложит создать свою или присоединиться к кампании друга.

## Если вы создаёте свою кампанию

Когда Мастер попросит создать repository:

1. Создайте новый GitHub repository **в своём личном account**.
2. Название можно выбрать любое.
3. Visibility может быть `Private` или `Public` — как вам удобнее.
4. При создании включите **Add a README**. Это нужно текущей версии автоматической установки.
5. Вернитесь в чат и сообщите Мастеру имя repository.

Дальше Мастер настроит repository сам. Не нужно вручную копировать туда engine, создавать папки или редактировать служебные файлы.

### Если ChatGPT не видит новый repository

Откройте:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

Выберите свой GitHub account и разрешите App доступ к нужному repository. Затем вернитесь в чат и скажите, что доступ настроен.

## Если вы присоединяетесь к кампании друга

1. Мастер покажет ваш GitHub username.
2. Передайте его владельцу кампании.
3. Владелец выдаст вам доступ к своему campaign repository.
4. Примите GitHub invitation, если она появится.
5. Вернитесь в чат и сообщите, что доступ получен.

Вам не нужно устанавливать или перенастраивать GitHub App владельца кампании.

## Обновление D&D Master

Когда выходит новый release и вы хотите обновить сам ChatGPT Project:

1. Откройте новый release tag.
2. Замените Project Instructions содержимым нового `INSTALL/PROJECT_INSTRUCTIONS.txt`.
3. Замените Project Source `00_DND_BOOTSTRAP.md` новой версией `INSTALL/00_DND_BOOTSTRAP.md` из того же release.

Существующие кампании при этом остаются в GitHub. Обновление engine внутри конкретной кампании Мастер выполняет отдельно по правилам кампании.

## Если что-то не работает

Сначала проверьте простые вещи:

- GitHub plugin подключён к нужному GitHub account;
- invitation к кампании принята;
- для нового собственного repository ChatGPT Codex Connector получил к нему доступ;
- вы используете оба установочных файла из одного опубликованного release.

Если проблема остаётся, опишите её Мастеру в чате. Не нужно самостоятельно менять GitHub permissions или игровые файлы наугад.
