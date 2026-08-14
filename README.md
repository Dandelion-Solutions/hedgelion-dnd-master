# D&D Master by Hedgelion

D&D Master — framework для долгих singleplayer и multiplayer D&D-кампаний с AI-мастером и persistent canon в GitHub.

Public engine:
https://github.com/Dandelion-Solutions/hedgelion-dnd-master

`main` — development branch. Нормальные игровые установки используют опубликованные GitHub Release source ZIPs/tags.

Архитектура разделяет:
- **engine package** — release ZIP, локально распакованный в текущем ChatGPT-чате;
- **campaign storage** — отдельный GitHub repository пользователя/хоста;
- **campaigns** — `campaign/*` branches с игровыми данными.

Engine tree больше не копируется в campaign storage. Storage определяется корневым `DND_STORAGE.yaml`; конкретная campaign хранит свою engine provenance в manifest.

Инструкция по установке:
[`INSTALL/README.md`](INSTALL/README.md)

Project Instructions template:
[`INSTALL/PROJECT_INSTRUCTIONS.txt`](INSTALL/PROJECT_INSTRUCTIONS.txt)

ChatGPT plugin directory:
https://chatgpt.com/plugins
