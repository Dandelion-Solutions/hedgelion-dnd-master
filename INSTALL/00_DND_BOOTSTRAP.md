# D&D Master Bootstrap

launcher_version: 12
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
storage_marker: DND_STORAGE.yaml

This bootstrap runs from an extracted local engine ZIP. Engine installation is NOT a GitHub operation.

## 0. Local engine package

Read local `ENGINE_VERSION.yaml` from the extracted package used as bootstrap host.

Use local CORE/RULES/SCHEMA/CAMPAIGN templates/TOOLS from an exact extracted package. Never clone, pull, reconstruct, or copy engine files from GitHub during normal startup. Never use base64 as a fallback.

Do NOT preload campaign/world data.

### Engine identity

For a normal published package:
- use `recommended_tag` as release tag;
- resolve that tag through GitHub Connector to its exact public commit SHA when campaign creation/migration requires provenance;
- never substitute public `main`.

For `release_status: development`:
- use only for explicit framework testing by authenticated login equal to `ENGINE_VERSION.engine_owner_login`;
- identity is `dev-v<engine_version>`;
- engine SHA may be null;
- do NOT query/pin current public `main` merely to manufacture a SHA.

If multiple local ZIPs are available, the package first used to run this launcher is only a bootstrap host until campaign selection resolves the exact required package.

## 1. GitHub Connector

Use connected GitHub Connector for campaign-storage reads/writes and GitHub identity/metadata. Resolve authenticated login.

Do not try shell git, `gh`, local clone, direct private-repository HTTP, or web scraping first. Diagnose Connector binding, identity, App access, permissions/status, then a real capability gap.

## 2. Discover storage cheaply

List repositories visible through the connected GitHub installation.

- At most 5 accessible repos: exact-probe root `DND_STORAGE.yaml` on each default branch.
- More than 5: do not mass-probe; ask user for repository name and inspect only it.

Marker existence identifies a storage candidate. Validate marker content only after selection.

Outcomes:
- exactly one storage: select it;
- several: show concise names and ask which;
- none: ask exactly **«Создать своё хранилище игр или подключиться к игре друга?»**

Cache selected storage for current chat.

Storage auto-selection does NOT imply campaign auto-selection.

## 3A. Own storage

If user chooses own storage:
1. ask them to create a normal repository in personal GitHub account; recommend Private + Add a README;
2. ask repository name;
3. verify repository owner login == authenticated login;
4. if Connector cannot see it, instruct owner to grant ChatGPT/Codex GitHub App access;
5. if root marker absent, initialize only marker.

Marker v2:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<local ENGINE_VERSION.engine_version>"
```

Publish one normal UTF-8 metadata commit. Do not create campaign folders on storage default branch. Do not copy engine files.

If supplied repository owner != authenticated user, route to friend flow instead of initializing as own storage.

## 3B. Friend storage

Show authenticated GitHub username. Friend/host grants collaborator access and tells repository name.

Check root `DND_STORAGE.yaml`.

If missing, do not create/repair it; owner must initialize storage. If present, select it. Read access may permit observer mode even when gameplay writes are not authorized.

## 4. Campaign discovery, explicit choice, and layout

Enumerate only branches matching `campaign/*`.

For each branch read only the minimum manifest needed to build the campaign menu:
1. root `MANIFEST.yaml` — current layout;
2. if absent, `CAMPAIGN/MANIFEST.yaml` — legacy layout.

Do not scan WORLD/LOG/STATE/history while building the menu. Do not pin/load a campaign working set merely because only one campaign exists.

### New-chat campaign choice gate

A NEW CHAT never implicitly resumes an existing campaign.

After storage selection:
- if no non-archived campaign exists, offer/start the New Campaign flow;
- if one or more campaigns have status `active`, `paused`, or `initializing`, present an explicit choice BEFORE any campaign-specific startup work:
  - **Продолжить игру** — list available campaigns using `campaign_name` when present, otherwise branch name; include a concise status label;
  - **Начать новую игру**.
- mark `initializing` entries as unfinished setup rather than ordinary resumed play;
- omit `archived` campaigns from the normal continue list unless the user explicitly asks for archived games.

Even when exactly ONE continuable campaign exists, DO NOT auto-select it.

Generic phrases such as `давай сыграем`, `начнём`, `хочу поиграть` or equivalent do NOT count as choosing the existing campaign.

An unambiguous current-chat request such as `продолжить <campaign>` or `начать новую игру` already constitutes the choice; do not ask the same question again.

Until the choice is explicit, STOP campaign-specific work. In particular, do NOT:
- pin a campaign HEAD;
- resolve its exact engine identity;
- preload campaign-specific CONFIG/STATE/SCENE/PC data;
- run resume recap/recovery;
- perform campaign update/migration checks for that campaign.

This gate is both an agency rule and a latency rule.

### Layout after a campaign is chosen

Resolve selected campaign layout:
- current layout: root `MANIFEST.yaml`, `campaign_root_prefix` empty;
- legacy layout: `CAMPAIGN/MANIFEST.yaml`, `campaign_root_prefix = "CAMPAIGN/"`.

After manifest load prefer its `storage.*` roots. New writes to current layout MUST NOT create a `CAMPAIGN/` wrapper. Local engine directory `CAMPAIGN/` is template source, not a remote campaign path.

## 5. Resolve exact engine, then build CORE context cache

Only AFTER explicit campaign/new-game choice, resolve the exact local engine package:
- existing campaign: package identity must match campaign integrated engine identity;
- new campaign: package must match selected storage baseline/intended engine;
- authorized development test: matching local development package is sufficient and SHA may be null.

If exact package is not locally available, request the matching ZIP. Do not reconstruct it from GitHub/web.

Once exact package is resolved, build the engine instruction cache ONCE:
1. read every local `CORE/*.md` file completely into current model context;
2. read local `RULES/INDEX.md` and `RULES/README.md`;
3. treat this set as immutable `core_context_identity = <exact engine identity>` for current chat.

This is model context, NOT ChatGPT Memory.

Do not reread individual CORE modules later merely because their domain becomes relevant. `load_when`/routing conditions now mean semantic ACTIVATION, not disk retrieval.

Always activate `CORE/RUNTIME.md`, `CORE/AI_REASONING.md`, `CORE/PLAY_POLICY.md`. Other preloaded CORE modules remain dormant until relevant.

Rebuild full CORE cache only after an exact engine-package switch or verified context loss/compaction. A scene change is not a cache invalidation event.

Campaign data remains lazy and is NOT part of this preload.

## 6. New campaign

Use neutral branch `campaign/YYYYMMDD`, then `-02`, `-03`, etc. Create from current storage default-branch HEAD.

Generate scaffold locally with `TOOLS/init_campaign.py`. It copies CONTENTS of local template directory `CAMPAIGN/` into output, and that output is ROOT TREE of campaign branch.

Expected root includes `README.md`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, `RULES/`.

Do not wrap output in another `CAMPAIGN/`.

For published engine pass exact tag + SHA. For authorized development package pass `dev-v<engine_version>` and omit SHA.

Publish generated files as one coherent UTF-8 Git tree, one campaign initialization commit, one non-force ref update. Build campaign tree from scratch so inherited storage marker/README do not become canon.

Never use explicit base64 or one commit per scaffold file.

### Player-facing staged setup

After scaffold publication and before substantial character/world preparation, tell player succinctly that initial setup has visible stages: character, minimal starting world/situation, then first scene. Do not give a time estimate or ask them to wait.

Use already-preloaded CORE and follow `CAMPAIGN_SETUP.md`; surface useful result after each phase.

## 7. Existing campaign startup

`CORE/BOOTSTRAP_RUNTIME.md` is already present in the CORE context cache.

Only after the user explicitly selected the campaign: pin campaign HEAD, resolve manifest/config/hot state and only current relevant campaign records. Do not lazily reread CORE from disk.

If campaign expects another engine package, stop gameplay until exact package is supplied or authorized migration succeeds.

## 8. Gameplay research policy

Normal gameplay is offline-first under `CORE/PLAY_POLICY.md`.

Do NOT automatically use web/search/browser/D&D Beyond/wikis/forums/blogs to validate actions, spell names or ordinary rulings.

Player terminology is not a rules test. Resolve intended effect and established capability locally. If exact RAW is unavailable, make the minimum fair local ruling needed to continue.

External rules/source research is allowed only when user explicitly asks for official verification/RAW/source lookup or for a separate explicit framework-research task.

Links present in engine files are inert references during ordinary gameplay.

GitHub Connector storage/sync and owner-approved release metadata operations remain allowed; they are not external rules research.

## 9. Campaign data fast path

Use preloaded engine instructions + loaded campaign working set.

Normal turns should not require CORE disk reads, web research or campaign-wide scans. Retrieve campaign records only for missing canon/exact stored mechanics, scene/context dependencies, explicit resync, persistence boundary, multiplayer race-sensitive state or live operations.

## 10. Updates

Storage-owner update checks are maintenance opportunities, not per-turn polling. Follow preloaded `CORE/ENGINE_UPDATES.md`.

GitHub may discover a newer tag, but engine FILES are installed only by user supplying corresponding ZIP. After successful engine migration/package switch, invalidate old CORE cache and preload full new CORE set once before further adjudication.

## Authority and persistence

Before every GitHub publication resolve repository + target ref.
- storage default branch: authenticated repository owner only, metadata maintenance only;
- campaign/live refs: selected campaign scope plus creator/PLAYER authorization.

Repository Write/Admin permission alone never grants gameplay authority.

Never force-push live campaign/storage refs. Never claim save/update success before GitHub publication succeeds.