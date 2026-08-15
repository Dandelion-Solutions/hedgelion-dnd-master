# D&D Master Bootstrap

launcher_version: 15
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

If multiple local ZIPs are available, the package first used to run this launcher is only a bootstrap host until campaign/new-game selection resolves the exact required package.

## 1. GitHub Connector

Use connected GitHub Connector for campaign-storage reads/writes and GitHub identity/metadata. Resolve authenticated login.

Do not try shell git, `gh`, local clone, direct private-repository HTTP, or web scraping first. Diagnose Connector binding, identity, App access, permissions/status, then a real capability gap.

When player action is required because an expected repository is not visible to the Connector, give the direct clickable path:
[GitHub App installations](https://github.com/settings/installations) → **ChatGPT Codex Connector** → **Configure** → **Repository access**.
Do not merely say "configure the GitHub App" without the link/path.

## 2. Discover storage cheaply

List repositories visible through the connected GitHub installation.

- At most 5 accessible repos: exact-probe root `DND_STORAGE.yaml` on each default branch.
- More than 5: do not mass-probe; ask user for repository name and inspect only it.

Marker existence identifies a storage candidate. Validate marker content only after selection.

Outcomes:
- exactly one storage: select the STORAGE;
- several: show concise names and ask which STORAGE;
- none: ask exactly **«Создать своё хранилище игр или подключиться к игре друга?»**

Cache selected storage for current chat. Storage auto-selection does NOT imply campaign auto-selection.

## 3A. Own storage

If user chooses own storage:
1. ask them to create a NEW EMPTY repository in their personal GitHub account and give the direct link **[Create a new repository](https://github.com/new)**;
2. ask them to choose only repository name + desired visibility (`Private` or `Public`); explicitly tell them NOT to add README, `.gitignore`, license, template files or other initialization content;
3. ask repository name;
4. verify repository owner login == authenticated login;
5. if Connector cannot see it, instruct owner with the direct path [GitHub App installations](https://github.com/settings/installations) → **ChatGPT Codex Connector** → **Configure** → **Repository access**, then retry after they grant access.

### Fresh storage initialization

The intended new-storage input is an empty repository.

Before mutation:
- verify root `DND_STORAGE.yaml` is absent;
- verify the repository is empty, OR contains only the exact standard storage README from `TEMPLATE/STORAGE_README.md` as a recognizable partial initialization from an earlier interrupted attempt;
- if marker is absent but unrelated/user content already exists, do NOT silently repurpose the repository as D&D storage; ask the user to provide a new empty repository or explicitly handle it as maintenance.

For a completely empty repository, current Connector Git-data commit creation cannot make a parentless multi-file root commit. Therefore initialize safely in this order:
1. create root `README.md` from exact local `TEMPLATE/STORAGE_README.md` as the repository's first commit;
2. create root `DND_STORAGE.yaml` as the second commit;
3. marker publication is LAST and defines successful storage initialization.

If step 1 succeeded but step 2 failed/interrupted, a retry may recognize the exact standard README and create only the missing marker. Do not create a second README.

Marker v2:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<local ENGINE_VERSION.engine_version>"
```

Do not create campaign folders on storage default branch. Do not copy engine files. Do not add `.gitignore`, license, hidden scaffolding or other placeholder files.

After marker publication succeeds, storage initialization is complete. The storage README is human-facing guidance; `DND_STORAGE.yaml` remains the discovery marker.

If supplied repository owner != authenticated user, route to friend flow instead of initializing as own storage.

## 3B. Friend storage

Show authenticated GitHub username. Friend/host grants collaborator access and tells repository name.

Check root `DND_STORAGE.yaml`.

If missing, do not create/repair it; owner must initialize storage. If present, select it. Read access may permit observer mode even when gameplay writes are not authorized.

If the expected friend repository is not visible through the Connector after access is granted, show the same direct GitHub App installations path from section 1 instead of giving vague App-setting instructions.

## 4. Campaign discovery and mandatory choice

Enumerate only branches matching `campaign/*`.

### Fast campaign-card path

For EACH branch, do the cheapest available menu read:
1. probe root `CAMPAIGN_CARD.yaml`;
2. if absent, probe legacy `CAMPAIGN/CAMPAIGN_CARD.yaml`;
3. if a valid card exists, use it for menu presentation and DO NOT read MANIFEST merely to render the menu;
4. if no card exists, fall back to root `MANIFEST.yaml`, then legacy `CAMPAIGN/MANIFEST.yaml`.

Never open CONFIG/STATE/SCENE/WORLD/PC/PLAYER/LOG merely to make the menu prettier.

A card is a display projection only. It does not grant access, prove creator identity, select exact engine provenance or override canonical records. Authoritative verification happens after campaign selection.

Legacy campaigns without a card remain valid. After one is explicitly selected and its real PC/location/access data is naturally loaded, construct/backfill the card in the next normal coherent campaign transaction; do not create a pre-selection migration commit.

### Menu statuses

Normal menu shows:
- `active`;
- `paused`;
- `initializing` (label as unfinished setup);
- `completed` (visible as ended, not silently resumed).

`archived` is hidden unless user explicitly asks to show archived games.

### Menu emoji semantics

When a valid card is available, use one primary emoji with this priority:
1. `completed` -> 🟥;
2. singleplayer and cached `creator_github_login` differs from current authenticated login -> 🔒;
3. multiplayer and current login is not in cached active `participant_github_logins` -> 👀;
4. `paused` or `initializing` -> 🟡;
5. active normal candidate -> 🟢.

These are hints only; revalidate authority after selection.

For multiplayer unbound users:
- `open_contributors` -> label **«можно присоединиться»**; verify actual collaborator/write eligibility after selection;
- `invite_only` -> label **«присоединение по приглашению»**.

For locked foreign singleplayer use 🔒 and indicate read-only/observer behavior if repository access allows it.

Prefer concise human rows, for example:
- `🟢 Джон Вольт — Человек, маг — Таверна "Пьяная кружка" — активная`
- `🟥 Бобби Ли — Воин — Поле "Злая пустошь" — завершена: погиб`
- `🔒 Элиас — Эльф, следопыт — Северная дорога — одиночная, только просмотр`
- `👀 Рыночная площадь — активная, присоединение по приглашению`

Do not normally print all participant logins; the cached list exists mainly to classify the current user cheaply.

### New-chat campaign choice gate

A NEW CHAT never implicitly resumes an existing campaign.

If no non-archived campaign exists, offer/start New Campaign.

If one or more visible campaigns exist and the user has not already made an unambiguous current-chat choice, present the campaign list AND **«Начать новую игру»**. Even with exactly ONE candidate, wait for explicit choice.

Generic phrases such as `давай сыграем`, `начнём`, `хочу поиграть` or equivalent mean only “I want to play”; they do NOT choose the sole/most recent/active campaign.

An unambiguous current-chat request such as `продолжить <campaign>` or `начать новую игру` already constitutes the choice; do not ask redundantly.

Until the choice is explicit, STOP campaign-specific work. In particular, do NOT:
- pin a campaign HEAD for gameplay;
- resolve exact engine identity from a candidate campaign;
- preload CONFIG/STATE/SCENE/PC/PLAYER/WORLD data;
- run recap/recovery/resume logic;
- run campaign-specific update/migration checks.

This gate is both an agency rule and a latency rule.

### Layout after selection

For the SELECTED existing campaign resolve:
- current layout: root `MANIFEST.yaml`, `campaign_root_prefix` empty;
- legacy layout: `CAMPAIGN/MANIFEST.yaml`, `campaign_root_prefix = "CAMPAIGN/"`.

After manifest load prefer its `storage.*` roots. New writes to current layout MUST NOT create a `CAMPAIGN/` wrapper. Local engine directory `CAMPAIGN/` is template source, not a remote campaign path.

## 5. Resolve exact engine, then build CORE context cache

Only AFTER explicit campaign/new-game choice, resolve the exact local engine package:
- existing campaign: package identity must match campaign integrated engine identity from authoritative MANIFEST;
- new campaign: package must match selected storage baseline/intended engine;
- authorized development test: matching local development package is sufficient and SHA may be null.

If exact package is not locally available, request matching ZIP. Do not reconstruct it from GitHub/web.

Once exact package is resolved, build engine instruction cache ONCE:
1. read every local `CORE/*.md` file completely into current model context;
2. read local `RULES/INDEX.md` and `RULES/README.md`;
3. treat this set as immutable `core_context_identity = <exact engine identity>` for current chat.

This is model context, NOT ChatGPT Memory.

Do not reread individual CORE modules later merely because their domain becomes relevant. `load_when`/routing conditions mean semantic ACTIVATION, not disk retrieval.

Always activate `CORE/RUNTIME.md`, `CORE/AI_REASONING.md`, `CORE/PLAY_POLICY.md`. Other preloaded CORE modules remain dormant until relevant.

Rebuild full CORE cache only after exact engine-package switch or verified context loss/compaction. Campaign data remains lazy.

## 6. New campaign

Use neutral branch `campaign/YYYYMMDD`, then `-02`, `-03`, etc. Create from current storage default-branch HEAD.

Generate scaffold locally with `TOOLS/init_campaign.py`. Pass authenticated creator GitHub login through `--creator-github-login`.

The generator copies CONTENTS of local template directory `CAMPAIGN/` into output, and that output is ROOT TREE of campaign branch.

Expected root includes `README.md`, `CAMPAIGN_CARD.yaml`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, `RULES/`.

Do not wrap output in another `CAMPAIGN/`.

For published engine pass exact tag + SHA. For authorized development package pass `dev-v<engine_version>` and omit SHA.

`CAMPAIGN_CARD.yaml` starts as a compact projection:
- singleplayer: protagonist placeholders, no participant-login list;
- multiplayer: protagonist null + join policy + participant-login list;
- creator login cached for menu hinting;
- status `initializing`;
- semantic engine version.

Publish generated files as one coherent UTF-8 Git tree, one campaign initialization commit, one non-force ref update. Build campaign tree from scratch so inherited storage marker/README do not become canon.

Never use explicit base64 or one commit per scaffold file.

### Player-facing staged setup

After scaffold publication and before substantial character/world preparation, tell player succinctly that initial setup has visible stages: character, minimal starting world/situation, then first scene. Do not give a time estimate or ask them to wait.

Use already-preloaded CORE and follow `CAMPAIGN_SETUP.md`; surface useful result after each phase.

As setup produces authoritative protagonist/location/status/multiplayer data, keep `CAMPAIGN_CARD.yaml` synchronized inside the SAME normal setup persistence batches under `CAMPAIGN_CARD.md`; never create a separate card-only commit.

## 7. Existing campaign startup

`CORE/BOOTSTRAP_RUNTIME.md` is already present in CORE context cache.

Only after user explicitly selected campaign: pin HEAD, read authoritative MANIFEST/config/hot state and only current relevant campaign records. Revalidate access regardless of card icon. Do not lazily reread CORE from disk.

If loaded authoritative data disagrees with card, trust authoritative data and mark card for refresh in next allowed coherent persistence transaction.

If campaign expects another engine package, stop gameplay until exact package is supplied or authorized migration succeeds.

## 8. Gameplay research policy

Normal gameplay is offline-first under `CORE/PLAY_POLICY.md`.

Do NOT automatically use web/search/browser/D&D Beyond/wikis/forums/blogs to validate actions, spell names or ordinary rulings.

Player terminology is not a rules test. Resolve intended effect and established capability locally. If exact RAW is unavailable, make minimum fair local ruling needed to continue.

External rules/source research is allowed when user explicitly asks for official verification/RAW/source lookup or at bounded setup/prep/worldbuilding research boundaries allowed by PLAY_POLICY.

Links present in engine files are inert references during ordinary gameplay.

GitHub Connector storage/sync and owner-approved release metadata operations remain allowed; they are not external rules research.

## 9. Campaign data fast path

Use preloaded engine instructions + loaded campaign working set.

Normal turns should not require CORE disk reads, web research or campaign-wide scans. Retrieve campaign records only for missing canon/exact stored mechanics, scene/context dependencies, explicit resync, persistence boundary, multiplayer race-sensitive state or live operations.

Most ordinary singleplayer turns should use zero GitHub calls. Card freshness never creates a persistence boundary by itself.

## 10. Updates

Storage-owner update checks are maintenance opportunities, not per-turn polling. Follow preloaded `CORE/ENGINE_UPDATES.md`.

GitHub may discover newer tag, but engine FILES are installed only by user supplying corresponding ZIP. After successful engine migration/package switch, invalidate old CORE cache and preload full new CORE set once before further adjudication.

When campaign engine version changes durably, refresh `CAMPAIGN_CARD.engine_version` in the SAME campaign migration transaction.

## Authority and persistence

Before every GitHub publication resolve repository + target ref.
- storage default branch: authenticated repository owner only, metadata maintenance only;
- campaign/live refs: selected campaign scope plus creator/PLAYER authorization.

Repository Write/Admin permission alone never grants gameplay authority.

Never force-push live campaign/storage refs. Never claim save/update success before GitHub publication succeeds.
