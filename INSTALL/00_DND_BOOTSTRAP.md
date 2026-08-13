# D&D Master Project Launcher

launcher_version: 2
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, campaign history, or previous chats. Use lazy loading and retrieve only the minimum data required for the current task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

Startup:
1. Use the connected GitHub app to access the repository named above.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main`.
3. For gameplay, resolve the active `campaign/*` branch first. Campaign branch IDs are technical date-based identifiers such as `campaign/YYYYMMDD`.
4. Read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
5. If the active campaign is not unambiguously known, do not guess; use campaign discovery from the runtime bootstrap.
6. Never claim a persistent state change was saved unless the GitHub write actually succeeded.

Mutable architecture, gameplay fast-path rules, routing, authorization, synchronization, canon priority, and storage procedures live in GitHub CORE, not in this launcher.
