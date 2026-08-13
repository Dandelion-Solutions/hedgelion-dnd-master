# Hedgelion D&D Project Launcher

launcher_version: 1
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. Add this file to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, all campaign history, or all previous chats. Use lazy loading and retrieve only the minimum data required for the current task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

Startup:
1. Use the connected GitHub app to access `dkolyada/hedgelion-dnd-master`.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main`.
3. For gameplay, resolve the active `campaign/<name>` branch first, then read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
4. If the active campaign branch is not unambiguously known, do not guess; use the campaign-discovery procedure from the runtime bootstrap.
5. Never claim that a persistent state change was saved unless the GitHub write actually succeeded.

Mutable architecture, module routing, synchronization, canon priority and storage procedures live in GitHub CORE, not in this Project Source launcher.
