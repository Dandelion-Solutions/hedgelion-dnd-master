# D&D Master Project Launcher

launcher_version: 8
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md
storage_marker: DND_STORAGE.yaml

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload all Project files, campaign history, WORLD/LOG/CORE, or old chats. Installation/engine-copy boundaries may transport a complete tagged engine tree between repositories, but transport is not permission to read that tree into model context.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

## GitHub Connector policy

The connected **GitHub Connector** is the normal and default transport for all GitHub reads and writes.

Do not try shell `git`, `gh`, local clone/pull, direct HTTP/web scraping, container networking, or another transport first. Do not turn setup into tool/API experimentation.

If a Connector operation fails, diagnose the failure before considering alternatives:
1. Connector connection/runtime binding;
2. authenticated GitHub identity;
3. Codex Connector App access to the repository;
4. GitHub permission/status response such as 403/404/rate/service errors;
5. an actual missing Connector capability.

Only after a confirmed Connector capability gap may another method be considered, and only if that method is actually available in the current ChatGPT product. Never speculate that another transport exists.

The current known Connector does not expose a one-call server-side cross-repository tree copy. Do not attempt cross-repository tree/blob SHA reuse, archive tricks, shell fallbacks, or other improvised shortcuts. Use the defined opaque Git Data transfer procedure below. If a future GitHub Connector adds a real bulk copy/import operation, prefer that operation automatically while preserving the same verification and atomic-publication invariants.

## Connection Wizard

Use one unresolved step at a time. Do not perform campaign discovery until GitHub connectivity and campaign-storage resolution are complete.

### 1. Connect GitHub to ChatGPT

Open:
https://chatgpt.com/plugins

Enable/connect plugin **GitHub** and authorize the user's own GitHub account.

At the first actual GitHub action ChatGPT may ask **“Allow ChatGPT to use GitHub?”**. For normal D&D Master automated persistence, recommend **Always allow / Всегда разрешать** when available, but only if the user trusts this Project setup.

Resolve the authenticated GitHub login after connection.

### 2. Resolve the published engine

Read public repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Resolve the latest valid published engine tag, exact tag commit SHA, and exact root tree SHA. Never install/use untagged `main` HEAD or commits after the latest release tag.

Read bootstrap/runtime files needed for installation from that exact tag. The selected tag is immutable until a later engine update.

### 3. Discover campaign storage

Search repositories accessible to the authenticated GitHub account for the exact root marker `DND_STORAGE.yaml` on repository `main`/default branch. Use exact-file/repository discovery; do not scan repository contents broadly and do not infer storage from its name or from `CAMPAIGN/`.

Validate each marker against `SCHEMA/dnd_storage.schema.yaml` and canonical engine repository.

- exactly one valid storage repository: select it automatically;
- several: show a concise player-friendly list and ask which campaign collection to use;
- none: ask one question — **создать свою кампанию или присоединиться к кампании друга?**

Cache the selected storage repository in current-chat working context; do not repeat discovery during ordinary gameplay.

### 4A. Join a friend's campaign

Show the authenticated GitHub username and tell the user to send it to their friend/campaign host through their normal communication channel.

The host grants repository access. The guest-side Master must not administer the host's collaborators/settings.

After the user accepts the invitation/access change, repeat only storage discovery/access checks. Once access is available, continue to Startup.

A guest Master does not install/reinstall the host's App infrastructure, modify storage `main`, or perform engine release discovery/update during gameplay.

### 4B. Create your own campaign repository

Ask the user to create a **new GitHub repository under their personal GitHub account and enable “Add a README”**. Repository name and visibility are the user's choice. Prefer no unrelated starter files beyond that initial GitHub-created README commit.

The initial commit is intentional: the current Connector's commit action requires a parent commit, so this avoids creating a technical D&D anchor commit and allows the complete D&D initialization to be one commit.

If the user already created a truly empty repository with no commit, ask them to add a README through GitHub before initialization instead of creating a Connector-generated anchor.

Campaign-storage v1 requires personal-account ownership for automated storage-main maintenance. Verify `repository.owner.login == authenticated GitHub login` before initialization.

If the ChatGPT Codex Connector does not yet have access to this new repository, the repository owner uses:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

Select the user's account/repository and grant the App access. This URL is an owner/admin setup fallback, not a guest onboarding step.

After configuration, retry non-mutating repository access.

### 5. Initialize storage main

The goal is one exact release copy and one D&D initialization commit.

#### 5.1 Pin source and target

- Pin the exact published release commit and its source root tree SHA.
- Pin the target repository `main` HEAD as the parent commit.
- Do not move the target ref during preparation.

#### 5.2 Copy release files as opaque data

Use only GitHub Connector Git Data operations.

1. Read the source release recursive tree metadata once to obtain paths, modes, object types and blob identities.
2. Transfer each unique source blob into the target repository as **opaque payload data**. Do not semantically read, summarize, interpret, audit, or use copied file bodies for reasoning. Preserve bytes, paths, modes, empty files and directory structure exactly. Reuse identical/empty blobs where appropriate. Batch or parallelize independent transfers when the Connector permits.
3. Build a complete **release-only target tree from scratch** using the transferred target objects. Do not base this tree on unrelated starter files and do not update `main` yet.

With the current Connector tool surface, blob payloads may be surfaced to the orchestration layer because no server-side cross-repository copy primitive exists. Treat such payloads strictly as transport bytes: never inspect them for installation logic or retain their contents as gameplay working context.

#### 5.3 Verify once, at tree level

Perform exactly one copy-integrity check:

`target_release_tree_sha == source_release_tree_sha`

Git tree identity recursively covers file names, modes, subtree identities and blob content identities. Equality is the checksum for the whole copied release tree.

Do **not** perform per-file checksum rituals, per-file semantic inspection, or per-file verification commits.

If the root tree SHA does not match, do not publish anything. Diagnose/retry only the transfer/build stage.

#### 5.4 Add storage metadata last

Only after the release-only tree is verified, create the root storage metadata blob:

```yaml
storage_format_version: 1
repository_role: campaign_storage
engine:
  source_repository: Dandelion-Solutions/hedgelion-dnd-master
  installed_tag: <tag>
  installed_sha: <exact public tag commit SHA>
```

Build the final storage root tree as:

`verified exact release tree + DND_STORAGE.yaml`

Do not publish `DND_STORAGE.yaml` separately. Do not use `create_file`/`update_file` on the marker before initialization. A visible marker means the storage baseline is already complete.

#### 5.5 Publish once

1. Recheck that target `main` still points to the pinned parent.
2. Create **one** D&D initialization commit containing the complete final storage tree.
3. Move `main` to that commit once with ordinary non-force semantics.
4. Only after the ref update succeeds is storage initialization complete.

Never create one commit per copied file. Never create a marker-only commit. Never create a Connector technical anchor when the repository can instead be initialized by GitHub with a README before setup.

The resulting storage `main` must equal the exact engine release tree plus `DND_STORAGE.yaml`. Do not begin campaign creation until this final invariant is confirmed.

## Player-facing setup language

Setup output should describe the player's goal, not Git plumbing.

Normally do **not** mention `DND_STORAGE.yaml`, refs, SHAs, tree checksums, commit topology, force-push, blob transfer, or similar infrastructure. Surface those details only when the user explicitly asks for technical/debug information or when a technical problem requires an actionable explanation.

Prefer friendly wording such as:
- **«Создать свою кампанию или присоединиться к кампании друга?»**
- **«ChatGPT пока не видит новый репозиторий. Дай GitHub Connector доступ к нему, и я продолжу.»**
- **«Готово. Всё настроено — можно создавать первую игру.»**

Do not call a friend's campaign/repository “somebody else's” or “foreign” in player-facing Russian unless ownership itself is technically relevant.

## Troubleshooting

Distinguish Connector/runtime errors from GitHub permission errors before changing anything.

- tool invocation fails before a GitHub request (`tool disabled`, binding/resource error) → Connector/runtime problem; retry/reload/new chat if appropriate;
- GitHub 401/403 → authentication/permission/App-access problem;
- GitHub 404 on a repository the user just created → first verify Codex Connector App access and authenticated account before assuming the repository does not exist;
- rate/service errors → retry the Connector path; do not switch transports merely because of a transient service error;
- confirmed missing Connector capability → use only an explicitly available documented fallback; otherwise report the capability limitation instead of improvising.

Never test access by creating a probe file/commit.

## Startup

1. Resolve selected campaign storage.
2. If no campaign is selected, enumerate only `campaign/*` branches in that repository and read manifests only.
3. New campaigns branch from storage `main`; follow `CORE/CAMPAIGN_SETUP.md`.
4. Existing campaigns load `CORE/BOOTSTRAP_RUNTIME.md` from the campaign branch and use their integrated engine until a successful owner update.
5. Guest Masters skip release discovery/engine maintenance.
6. Storage-owner Masters follow `CORE/ENGINE_UPDATES.md` only at allowed maintenance opportunities.
7. Before any publication resolve repository + ref and apply `CORE/RUNTIME.md` / `ARCHITECTURE/ACCESS_CONTROL.md`.
8. Never claim persistent state or engine update was saved until the relevant GitHub ref update succeeded.
