# Модель репозиториев, веток и кампаний

## Два уровня хранения

D&D Master разделяет публичный engine и игровые данные.

Canonical public engine repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Его `main` — development branch. Кампания никогда не использует untagged `main` как runtime source. Опубликованный движок определяется immutable release tag вида `vMAJOR.MINOR[-suffix]`.

Игровые данные живут в отдельном campaign-storage repository пользователя/хоста. Его имя произвольно. В первой версии автоматическое обслуживание storage `main` поддерживается для personal-account-owned repositories, чтобы owner authority однозначно определялась GitHub login владельца repository.

## Campaign-storage main

Storage `refs/heads/main` — локальный installed engine baseline:

- полный tree exact published engine tag;
- пустой/template `CAMPAIGN/` skeleton этого release;
- дополнительный storage-owned root file `DND_STORAGE.yaml`.

`DND_STORAGE.yaml` хранит роль repository и exact public release tag/SHA, установленный на storage `main`. Public engine repository этого файла не содержит.

Storage `main` не является игровой веткой. Только authenticated repository owner может изменять его через D&D Master, и только при storage initialization или engine upgrade.

## Campaign branches

Каждая реальная игра живёт в `campaign/YYYYMMDD[-NN]` внутри выбранного storage repository.

Новая campaign branch создаётся от текущего storage `main`, затем первый campaign-specific initialization commit:
- удаляет `DND_STORAGE.yaml` из campaign branch;
- заполняет `CAMPAIGN/MANIFEST.yaml` / `CONFIG.yaml` / стартовое состояние;
- фиксирует engine base/integrated tag и public source SHA из storage baseline.

Имена веток lore-neutral. Игровые ветки никогда не мержатся обратно в storage `main`, public engine `main` или друг в друга.

## Campaign creator и gameplay authority

Campaign creator по-прежнему определяется `author.login` первого campaign-specific initialization commit. Creator identity не дублируется в manifest.

Singleplayer gameplay writes — creator-only. Multiplayer gameplay requires active PLAYER binding according to `CORE/MULTIPLAYER.md`. Repository collaborator/Admin permission сама по себе не является gameplay authority.

Storage owner имеет отдельную узкую engine-maintenance authority: он может обновить storage baseline и интегрировать его в campaign branch по `CORE/ENGINE_UPDATES.md`, не изменяя произвольно игровой канон. Если migration требует решения creator/player, maintenance останавливается до этого решения.

## Engine update

Обновление двухфазное.

Phase A: storage owner устанавливает новый published tag на storage `main`. Все engine-owned paths приводятся в точное соответствие release tree: новые добавляются, изменённые заменяются, obsolete удаляются. `DND_STORAGE.yaml` сохраняется и обновляет installed tag/SHA.

Phase B: конкретная campaign branch безопасно интегрирует storage baseline. Populated `CAMPAIGN/**` не заменяется пустым skeleton release. Engine-owned obsolete paths удаляются; campaign data меняется только через defined migration/compatible metadata update.

Campaign update commit предпочитает merge-style provenance: first parent = текущий campaign HEAD, second parent = storage-main commit с новым baseline. Public release commit находится в другом repository и фиксируется tag/SHA metadata, а не cross-repository parent.

Storage `main` может быть новее конкретной campaign. Если Phase A успешна, а Phase B отложена/неудачна, rollback storage main не выполняется.

## Guest Master

Если authenticated GitHub user не является storage repository owner, Master не выполняет release discovery, не предлагает engine update, не изменяет storage `main` и не интегрирует engine baseline. Guest использует версию, уже установленную в выбранной campaign branch.

## Concurrency и persistence

Обычный gameplay сохраняет существующие правила optimistic concurrency: `force=false`, HEAD check перед publication boundary, targeted changed-path refresh и semantic reconciliation вместо blind overwrite.

Не создавать commit на каждый ход/бросок. Durable changes публикуются пакетами на естественных границах; race-sensitive multiplayer/live changes следуют специализированным runtime rules.

Git history — технический audit/provenance layer. Семантическая история мира хранится компактно в `CAMPAIGN/LOG/`.
