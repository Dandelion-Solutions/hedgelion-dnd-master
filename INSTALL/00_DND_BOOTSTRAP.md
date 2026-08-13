# D&D Master Project Launcher

launcher_version: 3
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, campaign history, or previous chats. Use lazy loading and retrieve only the minimum data required for the current task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

## Repository access gate

The first normal attempt to access the repository is also the installation check. Do not run a separate setup audit when repository access already works.

Attempt a non-mutating repository metadata/read request for `dkolyada/hedgelion-dnd-master`.

- If the repository is readable and the connector reports write/push permission, skip the connection wizard completely and continue to Startup.
- If the repository is readable but write/push permission is absent, explain briefly that the current campaign architecture requires writable persistent storage and stop before gameplay writes. Do not invent a fork/clone fallback unless current repository runtime explicitly defines one.
- If GitHub is unavailable, not connected, or the repository cannot be read, enter the Connection Wizard below.

Never test write access by creating, editing, or deleting a file.

## Connection Wizard

Use this only when the repository access gate fails. Guide the user through **one unresolved step at a time**. Keep instructions short and operational; do not explain connector architecture unless asked. After each completed step, retry repository access before showing another step.

### 1. Connect GitHub to ChatGPT

Ask the user to open ChatGPT **Settings → Apps → GitHub** and connect the GitHub account they intend to use.

Direct settings route:
https://chatgpt.com/#settings/Apps

Official setup guide:
https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt

If GitHub is unavailable or Connect is disabled, say that app availability may depend on the ChatGPT plan/workspace and stop until it is enabled.

After the user completes authorization, retry repository access.

### 2. Verify GitHub account access to the repository

Ask the user to open:
https://github.com/dkolyada/hedgelion-dnd-master

If the repository opens for that GitHub account, continue to step 3.

If it does not open, ask the user to send their GitHub username to the repository owner and have the owner invite them as a collaborator. The owner can manage access here:
https://github.com/dkolyada/hedgelion-dnd-master/settings/access

After the invitation is accepted, retry repository access.

### 3. Allow the ChatGPT GitHub App to access this repository

If the user can open the repository in GitHub but ChatGPT still cannot read it, ask them to open ChatGPT **Settings → Apps → GitHub → Choose repositories / Configure Repositories**, or open GitHub App installations directly:
https://github.com/settings/installations

Select the ChatGPT/OpenAI GitHub App, choose **Configure**, allow access to `dkolyada/hedgelion-dnd-master`, and save.

Repository visibility in ChatGPT can take a few minutes to update. Retry access after configuration; do not make the user repeat earlier steps that were already verified.

### 4. Confirm usable access

Once repository metadata/read succeeds, inspect connector permissions when available.

- read + write/push: setup is complete; continue immediately to Startup;
- read only: current shared-repository gameplay cannot persist changes; stop and state this briefly;
- still unreadable: report exactly which of the verified stages succeeded and which stage still fails. Do not restart the wizard from step 1.

## Startup

1. Use the connected GitHub app to access the repository named above.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main`.
3. For gameplay, resolve the active `campaign/*` branch first. Campaign branch IDs are technical date-based identifiers such as `campaign/YYYYMMDD`.
4. Read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
5. If the active campaign is not unambiguously known, do not guess; use campaign discovery from the runtime bootstrap.
6. Never claim a persistent state change was saved unless the GitHub write actually succeeded.

Mutable architecture, gameplay fast-path rules, routing, authorization, synchronization, canon priority, and storage procedures live in GitHub CORE, not in this launcher.
