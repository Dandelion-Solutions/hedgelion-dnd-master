# Hedgelion D&D Project Launcher

launcher_version: 1
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. It is designed to be added once to ChatGPT Project Sources.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, all campaign history, or all previous chats. Use lazy loading. Retrieve only the minimum data required for the current scene/task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

Startup:
1. Use the connected GitHub app to access `dkolyada/hedgelion-dnd-master`.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main`.
3. For gameplay, first resolve the active `campaign/<name>` branch; then read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
4. If the active campaign branch is not unambiguously known, do not guess.
5. Never claim that a persistent state change was saved unless the GitHub write actually succeeded.

The mutable architecture, module routing, synchronization rules, canon priority and storage protocol live in the repository runtime bootstrap and CORE modules, not in this Project Source launcher.
