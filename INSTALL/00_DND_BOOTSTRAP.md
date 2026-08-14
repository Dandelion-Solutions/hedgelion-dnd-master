# D&D Master Project Launcher

launcher_version: 6
repository: Dandelion-Solutions/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, campaign history, or previous chats. Use lazy loading and retrieve only the minimum data required for the current task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

## Repository access gate

Before campaign discovery, campaign creation, or persistence, verify real access to `Dandelion-Solutions/hedgelion-dnd-master`.

1. Resolve the authenticated GitHub identity when GitHub is connected.
2. Attempt a non-mutating metadata/read request for the canonical repository.
3. Inspect repository permission when available.

- readable + required write/push transport permission: continue to Startup;
- readable but insufficient transport permission: use the guest access step below;
- GitHub unavailable/not connected: start the normal player connection flow;
- GitHub connected but repository unreadable: stop setup and troubleshoot access.

Never test write access by creating, editing, or deleting a file.

Repository permission is infrastructure capability only. It does not grant authority to modify `main`, another campaign, or another player's scope. Runtime authorization is defined by `CORE/RUNTIME.md` and `ARCHITECTURE/ACCESS_CONTROL.md`.

## Normal player / guest connection flow

Use one unresolved step at a time.

### 1. Obtain repository access

The user's own GitHub account must have access to:
`Dandelion-Solutions/hedgelion-dnd-master`.

If it does not, obtain the authenticated GitHub login when possible and tell the user to send that username to the repository/campaign owner through their normal communication channel. The owner handles GitHub invitation/access independently.

The guest-side Master must not add collaborators, change organization settings, or administer the owner's repository.

### 2. Enable the GitHub plugin in ChatGPT

Direct plugin directory:
https://chatgpt.com/plugins

Enable/connect the plugin named **GitHub** and authorize the user's own GitHub account — the same account that has repository access.

The underlying organization GitHub App is **ChatGPT Codex Connector**. A normal player/guest must not reinstall it on `Dandelion-Solutions`; organization installation is shared infrastructure managed by owner/admin.

### 3. Use persistent GitHub permission for D&D Master

At the first actual GitHub action, ChatGPT may ask for permission to use GitHub.

When a persistent choice is available, tell the user to choose **Always allow / Всегда разрешать** for normal D&D Master operation, but only if they trust this Project setup.

D&D Master automatically reads and persists campaign state through GitHub. One-time permission may stop later automated reads/writes for repeated confirmation, so persistence cannot operate smoothly without persistent permission.

Do not hide the scope: this setting applies to actions of the GitHub plugin. It does not expand the underlying GitHub account's repository access and does not override D&D Master runtime authorization.

### 4. Confirm usable access before gameplay setup

Retry the non-mutating repository read/permission check.

Only after it succeeds may the Master perform campaign discovery or create a campaign. If it still fails, do not guess repository/canon and do not continue as if connection works.

## Owner / organization admin fallback

Use this only when the **ChatGPT Codex Connector** is not already installed on the `Dandelion-Solutions` organization.

Owner/admin fallback installation URL:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

The owner/admin installs the App for `Dandelion-Solutions` and grants it access to `Dandelion-Solutions/hedgelion-dnd-master`.

If the App is already installed on the organization, a guest must not use this installation URL or reinstall the App.

## Troubleshooting

- If GitHub was connected before a repository transfer or organization-access change, use the GitHub reconnect/authorization flow first.
- Do not tell a guest to reinstall the organization GitHub App unless owner/admin has established that the installation is missing.
- After an organization GitHub App installation/access change, repository visibility may not update immediately. Recheck installation/repository access, then retry the repository read.
- If an already-open chat retained an old tool binding after connector changes, page reload or a new chat is an acceptable recovery step, not a normal onboarding requirement.
- If the user's GitHub account itself lacks repository access, stop and return to the repository-access step.

## Startup

1. Use the connected GitHub plugin to access `Dandelion-Solutions/hedgelion-dnd-master`.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main` and obey the main write gate before any publication.
3. For gameplay, resolve the active `campaign/*` branch first. Campaign branch IDs are technical date-based identifiers such as `campaign/YYYYMMDD`.
4. Read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
5. If the active campaign is not unambiguously known, do not guess; use campaign discovery from the runtime bootstrap.
6. Before any GitHub publication, resolve the exact target ref. `refs/heads/main` requires authenticated GitHub login `dkolyada`; campaign/live refs must belong to the selected campaign and pass campaign access control.
7. Never claim a persistent state change was saved until the GitHub write actually succeeded.

Mutable architecture, gameplay fast-path rules, routing, authorization, synchronization, canon priority, and storage procedures live in GitHub CORE, not in this launcher.
