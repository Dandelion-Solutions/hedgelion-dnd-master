# D&D Master by Hedgelion

D&D Master — framework для долгих singleplayer и multiplayer D&D-кампаний с AI-мастером и persistent canon в GitHub.

Public engine:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

`main` этого repository — development branch; игровые установки используют только опубликованные release tags. Framework writes в public `main` разрешены runtime policy только GitHub login `dkolyada`.

Игровые данные хранятся отдельно — в campaign-storage repository пользователя/хоста. Его `main` содержит установленный release snapshot + `DND_STORAGE.yaml`, а реальные миры живут в `campaign/*`. Guest players работают только в разрешённом campaign/live scope и не обслуживают engine updates.

Инструкция по установке ChatGPT/GitHub и созданию/подключению campaign storage:
[`INSTALL/README.md`](INSTALL/README.md)

ChatGPT plugin directory:
https://chatgpt.com/plugins
