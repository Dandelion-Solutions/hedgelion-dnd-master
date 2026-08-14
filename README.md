# D&D Master by Hedgelion

D&D Master — framework для долгих singleplayer и multiplayer D&D-кампаний с AI-мастером и persistent canon в GitHub.

Canonical repository:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

Игровой мир живёт независимо от отдельного chat: персонажи, NPC, предметы, отношения, тайны, события и последствия сохраняются в campaign branch. ChatGPT Memory, File Library и старые chats не являются базой данных кампании.

`main` содержит общий engine/runtime, schemas, tests, install/release documentation и пустой campaign skeleton. `refs/heads/main` является engine-maintainer-only по runtime policy; authenticated GitHub login для публикации в `main` — `dkolyada`. Repository Write/Admin permission сама по себе не расширяет эту authority.

Каждая реальная игра живёт в отдельной `campaign/*` branch. В singleplayer gameplay writes доступны creator этой кампании; в multiplayer authority определяется campaign access rules и active `PLAYER_` binding. Campaign updates интегрируют опубликованные engine release tags в campaign branch и не публикуют campaign state обратно в `main`.

Для подключения ChatGPT и GitHub используйте:
[`INSTALL/README.md`](INSTALL/README.md)

ChatGPT plugin directory:
https://chatgpt.com/plugins
