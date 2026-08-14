# D&D Master Project Launcher

launcher_version: 7
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md
storage_marker: DND_STORAGE.yaml

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload all Project files, all campaign history, or all world data. Installation/engine-copy boundaries may copy a complete tagged engine tree between repositories, but LLM gameplay context remains lazy and minimal.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

## Connection Wizard

Use one unresolved step at a time. Do not perform campaign discovery until GitHub connectivity and campaign-storage resolution are complete.

### 1. Connect GitHub to ChatGPT

Open:
https://chatgpt.com/plugins

Enable/connect plugin **GitHub** and authorize the user's own GitHub account.

At the first actual GitHub action ChatGPT may ask **“Allow ChatGPT to use GitHub?”**. For normal D&D Master automated persistence, recommend **Always allow / Всегда разрешать** when available, but only if the user trusts this Project setup. Explain that this persistent permission applies to GitHub plugin actions; it does not expand GitHub account permissions or D&D Master runtime authority.

Resolve the authenticated GitHub login after connection.

### 2. Resolve the published engine

Read public repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Resolve the latest valid published engine tag and exact tag SHA. Never install/use untagged `main` HEAD or commits after the latest release tag.

Read bootstrap/runtime files for installation from that exact tag. The selected tag is immutable until a later engine update.

### 3. Discover campaign storage

Search repositories accessible to the authenticated GitHub account for the exact root marker `DND_STORAGE.yaml` on repository `main`/default branch. Use exact-file/repository discovery; do not scan repository contents broadly and do not infer storage from its name or from `CAMPAIGN/`.

Validate each marker against `SCHEMA/dnd_storage.schema.yaml` and canonical engine repository.

- exactly one valid storage repository: select it automatically;
- several: show a concise list and ask which one to use;
- none: ask one question — **create your own campaign repository or join somebody else's?**

Cache the selected storage repository in current-chat working context; do not repeat discovery during ordinary gameplay.

### 4A. Join somebody else's storage repository

Show the authenticated GitHub username and tell the user to send it to the repository owner through their normal communication channel.

The owner grants repository access. The guest-side Master must not administer the owner's collaborators/settings.

After the user accepts the invitation/access change, repeat only storage discovery/access checks. Once `DND_STORAGE.yaml` is readable, continue to Startup.

A guest Master does not install/reinstall the owner's organization App, does not modify storage `main`, and does not perform engine release discovery/update during gameplay.

### 4B. Create your own storage repository

Ask the user to create a new empty GitHub repository under their personal GitHub account. Repository name and visibility are the user's choice; D&D Master must not require the word “private”. Prefer no unrelated starter files.

Campaign-storage v1 requires personal-account ownership for automated storage-main maintenance. Verify `repository.owner.login == authenticated GitHub login` before initialization.

If the ChatGPT Codex Connector does not yet have access to this new repository, the repository owner uses:
https://github.com/apps/chatgpt-codex-connector/installations/select_target

Select the user's account/repository and grant the App access. This URL is an owner/admin setup fallback, not a guest onboarding step.

After configuration, retry non-mutating repository access.

### 5. Initialize storage main

Create the storage baseline from the complete tree of the exact published engine tag resolved in step 2, plus root `DND_STORAGE.yaml`:

```yaml
storage_format_version: 1
repository_role: campaign_storage
engine:
  source_repository: Dandelion-Solutions/hedgelion-dnd-master
  installed_tag: <tag>
  installed_sha: <exact public tag commit SHA>
```

Prefer one root/atomic initialization commit when the connected GitHub tooling supports a root commit/tree. If the connector cannot create a parentless/root commit, use the smallest infrastructure anchor supported by GitHub/tooling and then one atomic D&D initialization commit; never create one commit per copied file.

The resulting storage `main` must equal the engine release tree plus `DND_STORAGE.yaml`. Do not begin campaign creation until this is verified.

## Troubleshooting

Distinguish connector/runtime errors from GitHub permission errors.

- Tool listed but invocation fails before a GitHub request (`tool disabled`, `Resource not found`) → connector/runtime binding problem. Do not change repository permissions blindly; reload/new chat is an acceptable recovery step.
- GitHub/API 403/forbidden/insufficient permission → inspect account/App/repository access.
- If App access changed, repository visibility in ChatGPT may lag; recheck installation/access then retry exact read.
- Never test access by creating a probe file/commit.

## Startup

1. Resolve selected campaign-storage repository through `DND_STORAGE.yaml`.
2. If no campaign is selected, enumerate only `campaign/*` branches in that repository and read manifests only.
3. New campaigns branch from storage `main`, not public engine `main`/tag directly; follow `CORE/CAMPAIGN_SETUP.md`.
4. Existing campaigns load `CORE/BOOTSTRAP_RUNTIME.md` from the campaign branch and use their integrated engine until a successful owner update.
5. Guest Masters skip release discovery/engine maintenance.
6. Storage-owner Masters follow `CORE/ENGINE_UPDATES.md` only at allowed maintenance opportunities.
7. Before any publication resolve repository + ref and apply `CORE/RUNTIME.md` / `ARCHITECTURE/ACCESS_CONTROL.md`.
8. Never claim persistent state or engine update was saved until the relevant GitHub ref update succeeded.
