# D&D Master Project Launcher

launcher_version: 9
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md
storage_marker: DND_STORAGE.yaml
release_archive_pattern: hedgelion-dnd-master-*.zip

This launcher runs from an already extracted D&D Master source archive. Project Instructions are responsible for making the archive available and extracting it in the current chat working environment.

## Non-negotiable startup assumptions

1. Find the local engine root by `ENGINE_VERSION.yaml`.
2. Confirm `CORE/BOOTSTRAP_RUNTIME.md`, `CORE/RUNTIME.md`, `CORE/AI_REASONING.md`, `SCHEMA/`, `CAMPAIGN/`, and `TOOLS/` are available under that same root.
3. Read only files required for the current step. Local presence is not permission to preload the engine into model context.
4. Never use base64 for installation/scaffolding/file reconstruction.
5. Never download/clone/pull engine source from GitHub as part of normal startup.
6. Never use ChatGPT Memory as campaign canon.

For a normal published release, `ENGINE_VERSION.yaml` is the authoritative local version record and `recommended_tag` is the expected public release tag. Public GitHub may be queried for tag/SHA metadata, but source files come from the local archive.

Development builds on public `main` are allowed only for explicit framework testing by authenticated `engine_owner_login`; they are not normal player releases.

## GitHub Connector policy

Use the connected GitHub Connector for campaign-storage reads/writes and GitHub identity/permission checks.

Do not first try shell git, `gh`, local clone, direct private HTTP, web scraping, or undocumented APIs.

On failure diagnose:
1. Connector connection/runtime binding;
2. authenticated GitHub identity;
3. GitHub App access to the repository;
4. GitHub 401/403/404/rate/service status;
5. actual missing Connector capability.

Do not test access by creating probe commits.

## Connection Wizard

Resolve one unresolved setup step at a time.

### 1. Connect GitHub

Use the GitHub Connector and resolve the authenticated GitHub login.

If GitHub is not connected, guide the user to connect the GitHub plugin/Connector and authorize their own account. Recommend **Always allow / Всегда разрешать** only when the user trusts this Project.

### 2. Discover campaign storage cheaply

Campaign storage is identified only by exact root `DND_STORAGE.yaml` on the repository default branch.

Marker CONTENT is not needed for discovery. Marker existence is the discovery signal.

Use a bounded repository-list probe:
- request at most 6 accessible repositories;
- if 6 are returned (there are more than 5 candidates to inspect), STOP broad discovery and ask the user for the repository name;
- if 0..5 are returned, probe only exact root `DND_STORAGE.yaml` in those repositories.

Do not use global code search as the primary storage discovery mechanism.
Do not recursively inspect repository contents.
Do not infer storage from name, README, `CAMPAIGN/`, fork status, or similarity to the engine repository.

Outcomes:
- no marked storage: ask exactly **«Создать своё хранилище игр или подключиться к игре друга?»**
- exactly one: select it automatically;
- several: show a concise list and ask which storage to use.

Cache the selected storage for this chat.

### 3A. Create/use the user's own storage

Ask the user to create a new GitHub repository under their personal account. Recommend:
- `Private`;
- arbitrary name;
- **Add a README** enabled, because the current Connector commit primitive needs an existing parent commit.

Ask for the repository name.

Resolve it through the Connector and verify:
`repository.owner.login == authenticated GitHub login`.

If ownership does not match, do not initialize it as the user's own storage; route to the friend/join path.

If the App cannot see the new repository, tell the owner to grant the ChatGPT/Codex GitHub App access to it, then retry non-mutating access.

#### First storage initialization

If exact root `DND_STORAGE.yaml` is absent, create it quickly and silently from the LOCAL engine version.

Storage v2 marker:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<ENGINE_VERSION.engine_version>"
```

Publish this as one normal non-force storage-default-branch commit.

Preferred GitHub publication path:
1. pin storage default-branch HEAD and base tree;
2. create a tree based on that tree with UTF-8 `content` for `DND_STORAGE.yaml`;
3. create one commit with the pinned parent;
4. move the default branch once with `force=false`.

Do not explicitly base64-encode anything.
Do not copy engine files into storage.
Do not create `CAMPAIGN/`, WORLD, LOG, indexes, `.gitkeep`, templates, or engine directories on storage default branch.
Do not create one commit per placeholder.

If the marker already exists, do not rewrite it merely because startup occurred.

### 3B. Connect to a friend's storage

Show the authenticated GitHub username.

Tell the user to ask the storage owner to add that GitHub account as a collaborator with the intended access and to give the repository name.

After the user provides the repository name:
1. resolve only that repository;
2. check exact root `DND_STORAGE.yaml` on its default branch.

If the marker is missing:
- do not create it;
- do not modify the friend's repository;
- tell the user the friend's D&D storage is installed incorrectly and the owner must initialize/fix it.

If the marker exists, select the storage and continue.

A guest Master never administers the owner's GitHub App or storage-default-branch metadata.

## Campaign discovery

After storage selection:
1. enumerate only branches matching `campaign/*`;
2. read only `CAMPAIGN/MANIFEST.yaml` from each candidate branch;
3. do not load WORLD/LOG/history merely to show the game list.

If none exist, offer a new game.
If one or more exist, let the user continue one or create a new one.

Repository read access permits observation. Gameplay writes are separately controlled by creator/PLAYER authorization; a user may be read-only observer for a campaign they can see.

## Resolve the engine for a campaign

### New campaign

Use the currently extracted local engine package.

For a published release:
- read local `ENGINE_VERSION.yaml`;
- take `recommended_tag`;
- resolve that public tag to its exact commit SHA using GitHub metadata;
- verify the tag's `ENGINE_VERSION.yaml` metadata is coherent when needed.

For explicit engine-owner development testing:
- require authenticated login == local `engine_owner_login`;
- use a clearly development-only engine tag marker such as `dev-v<engine_version>`;
- pin the exact current public development commit SHA.
Development campaigns are test data and are not normal release campaigns.

### Existing campaign

Read its `CAMPAIGN/MANIFEST.yaml`.

The campaign's `engine.integrated_tag` and `engine.integrated_main_sha` define the engine it expects.

If the currently extracted local engine is the exact required release, continue.

If it is not:
- first look for a matching D&D Master ZIP already available in Project Sources/current-chat attachments;
- if available, extract that version separately and use it for this campaign;
- otherwise ask the user to attach/add the matching release ZIP.

Do not silently run a campaign on a different engine version.

A storage owner may instead choose an allowed engine upgrade through `CORE/ENGINE_UPDATES.md`; a guest cannot bypass an engine mismatch by upgrading someone else's campaign.

## New campaign creation

Follow local `CORE/CAMPAIGN_SETUP.md`.

High-level flow:
1. choose the first free neutral branch ID `campaign/YYYYMMDD[-NN]`;
2. create that branch from current storage default-branch HEAD;
3. generate the initial campaign tree locally from the release package with `TOOLS/init_campaign.py`;
4. publish the generated campaign tree in ONE campaign-initialization commit;
5. move the campaign branch once with `force=false`;
6. only after publication succeeds, continue player/PC/world setup.

The first campaign commit replaces inherited storage-default-branch contents with the generated campaign tree. Therefore `DND_STORAGE.yaml`, storage README, and other storage-root files do not become campaign canon.

Use UTF-8 text/tree publication. Never use explicit base64. Never publish one commit per scaffold file.

## Storage v1 compatibility

A root marker with `storage_format_version: 1` still identifies a storage candidate.

Do not use copied engine files found on legacy storage `main` as runtime source.

For a storage owner, v1 metadata may be migrated lazily to v2 at a safe maintenance/setup boundary. Derive `baseline_version` from unambiguous legacy installed-tag metadata or from an explicitly accepted local engine release. Do not delete arbitrary legacy files merely to migrate the marker.

For guests, do not rewrite legacy storage metadata. Existing campaign branches remain selectable; new campaign creation may require the owner to migrate the storage marker first.

## Player-facing setup language

Hide infrastructure unless actionable.

Prefer:
- **«Создать своё хранилище игр или подключиться к игре друга?»**
- **«ChatGPT пока не видит репозиторий. Дай GitHub Connector доступ к нему и сообщи имя ещё раз.»**
- **«Готово. Хранилище настроено.»**
- **«Выбери существующую игру или создай новую.»**

Do not normally mention marker names, SHAs, tree objects, commit topology, or engine archive internals unless the user asks or an error requires them.

## Startup handoff

After storage/campaign/engine resolution:
1. open local `CORE/BOOTSTRAP_RUNTIME.md`;
2. pin selected campaign HEAD;
3. load campaign MANIFEST/CONFIG/state lazily;
4. ALWAYS load local `CORE/RUNTIME.md` and `CORE/AI_REASONING.md`;
5. load additional CORE modules only as needed;
6. apply access/persistence rules before publication.

Never claim setup/save/update success before the corresponding GitHub publication succeeds.
