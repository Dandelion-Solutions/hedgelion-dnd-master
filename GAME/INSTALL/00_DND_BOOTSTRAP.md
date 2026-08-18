# D&D Master Bootstrap

launcher_version: 17
storage_marker: DND_STORAGE.yaml

This bootstrap runs from a validated local runtime package. Engine installation is NOT a GitHub operation.

## 0. Local runtime packages

A ChatGPT Project may contain several supported runtime ZIPs at once, for example different semantic engine versions required by different campaigns.

At chat startup, index available `hedgelion-dnd-master-runtime-v<version>.zip` assets cheaply. Do NOT eagerly extract every archive. For candidate classification, read only archive filename/root metadata as needed:
- `ENGINE_VERSION.yaml` — semantic engine/runtime contract;
- `RUNTIME_PACKAGE.yaml` — provenance of the exact built artifact;
- SHA-256 of the complete ZIP when exact artifact/cache identity is needed.

GitHub-generated `Source code (zip)` / `Source code (tar.gz)` archives are source snapshots, not runtime packages.

The package used first to open this launcher is only a **bootstrap host** until explicit campaign/new-game selection resolves the required runtime. It does not pin an existing campaign to its own version.

Do not assume an extracted package from another chat or an earlier environment still exists. Extracted runtime directories are disposable cache. If an exact selected package is not currently extracted, silently re-extract it from the available ZIP; missing cache alone is never a player-facing failure.

Never clone, pull, reconstruct, or copy engine files from GitHub during normal startup. Never use base64 as an unpack/install fallback.

### Package validation and artifact identity

Before a package is used, require directly at its package root:
- `ENGINE_VERSION.yaml`;
- `RUNTIME_PACKAGE.yaml`;
- `CORE/`;
- `INSTALL/`;
- `RULES/`;
- `SCHEMA/`;
- `CAMPAIGN/`;
- `TOOLS/`.

Reject source-repository wrappers such as `GAME/` or `DEV/`, nested package markers, mixed package trees, or malformed provenance metadata.

Treat package-root `ENGINE_VERSION.yaml` as the sole machine-authoritative source for semantic engine metadata: version, release status, canonical engine repository, development-owner identity, rules/schema baseline, update compatibility and recommended tag.

Treat package-root `RUNTIME_PACKAGE.yaml` as artifact provenance for the bytes that were built: package identity, source state/ref and exact source commit when available. Do not infer an old ZIP's source commit merely from where a mutable tag points today.

### Isolated runtime cache and `current_runtime_root`

After the required package is resolved, compute/verify its ZIP SHA-256 and bind one ephemeral current-chat path:

```text
current_runtime_root = <session-cache>/hdm-runtime/<version>/<package_sha256>/
```

The path is cache only. NEVER write `current_runtime_root` into storage/campaign Git, ChatGPT Memory, or campaign canon.

If that exact cache directory exists, validate it before reuse. Otherwise silently extract the exact ZIP into that isolated directory and validate it there.

After binding, ALL package-relative runtime access MUST resolve under that one `current_runtime_root`: `ENGINE_VERSION.yaml`, `RUNTIME_PACKAGE.yaml`, `CORE/`, `RULES/`, `SCHEMA/`, `CAMPAIGN/`, `TEMPLATE/`, `MIGRATIONS/`, `INSTALL/`, and runtime `TOOLS/`.

MUST NOT globally search the working filesystem for a convenient `ENGINE_VERSION.yaml`, `CORE/`, `RULES/`, template, or `TOOLS/init_campaign.py` after runtime selection. Sibling cached runtime versions are inert. Never merge or borrow files across runtime roots.

Do NOT preload campaign/world data during package/bootstrap discovery.

### Engine identity

For a normal published package, use its validated `RUNTIME_PACKAGE.package_id`, source provenance and final ZIP SHA-256. Resolve GitHub release/tag metadata only when an update/provenance operation actually needs server-side comparison; never substitute public `main` as gameplay runtime bytes.

For `ENGINE_VERSION.release_status: development`:
- use only for explicit framework testing by authenticated login equal to `ENGINE_VERSION.engine_owner_login`;
- package identity is `dev-v<ENGINE_VERSION.engine_version>`;
- dirty/non-Git package provenance may have null source commit SHA;
- do NOT query/pin public `main` merely to manufacture provenance.

## 1. GitHub Connector

Use connected GitHub Connector for campaign-storage reads/writes and GitHub identity/metadata. Resolve authenticated login.

For semantically textual repository content, use Connector UTF-8/text interfaces whenever a correct text mode exists. Do not manually Base64-encode or Base64-decode text for GitHub transport, chunking, staging, reconstruction or verification. Connector-internal Base64 required by an underlying API is allowed; the runtime must not add its own redundant text-to-Base64-to-text cycle. Use explicit Base64 only for genuinely binary content or when a required Connector operation has no usable text mode.

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
- verify the repository is empty, OR contains only the exact standard storage README from selected `current_runtime_root/TEMPLATE/STORAGE_README.md` as a recognizable partial initialization from an earlier interrupted attempt;
- if marker is absent but unrelated/user content already exists, do NOT silently repurpose the repository as D&D storage; ask the user to provide a new empty repository or explicitly handle it as maintenance.

Before marker creation, resolve an owner-approved baseline runtime package from the available validated packages and bind its `current_runtime_root`. Storage baseline is portable package identity, never a filesystem path.

For a completely empty repository, current Connector Git-data commit creation cannot make a parentless multi-file root commit. Therefore initialize safely in this order:
1. create root `README.md` from exact selected `current_runtime_root/TEMPLATE/STORAGE_README.md` as the repository's first commit;
2. create root `DND_STORAGE.yaml` as the second commit;
3. marker publication is LAST and defines successful storage initialization.

If step 1 succeeded but step 2 failed/interrupted, a retry may recognize the exact standard README and create only the missing marker. Do not create a second README.

Marker v3:

```yaml
storage_format_version: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "<selected ENGINE_VERSION.engine_version>"
    package_id: "<selected RUNTIME_PACKAGE.package_id>"
    source_commit_sha: "<selected RUNTIME_PACKAGE.source_commit_sha|null>"
    package_sha256: "<selected ZIP sha256>"
    adopted_at: "<timestamp>"
```

`engine.baseline` is the default runtime identity for NEW campaigns only. It does not select or mutate an existing campaign runtime. Only storage owner may persist storage-baseline changes.

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

Legacy campaigns without a card remain valid for menu discovery where otherwise supported. This implementation does not invent backward migration for legacy engine-identity fields.

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

For the SELECTED existing campaign resolve authoritative root `MANIFEST.yaml` under the current schema. Do not treat local engine directory `CAMPAIGN/` as a remote campaign path.

After manifest load prefer its `storage.*` roots. New writes to current layout MUST NOT create a `CAMPAIGN/` wrapper.

## 5. Resolve exact runtime, then build CORE context cache

Only AFTER explicit campaign/new-game choice, resolve the required portable runtime identity:
- existing campaign: read authoritative `MANIFEST.engine.current`;
- new campaign in existing storage: read `DND_STORAGE.engine.baseline`;
- authorized development test: use matching validated development package identity.

Index candidate ZIP metadata without eagerly extracting all packages. Candidate provenance MUST come from that ZIP's `RUNTIME_PACKAGE.yaml`, not from current mutable tag position.

Select the package according to `CORE/ENGINE_UPDATES.md` rules for exact artifact, same-version refresh, semantic-version update and downgrade protection. If the needed ZIP is available but its extracted directory is absent, silently re-extract it. If the needed ZIP bytes themselves are unavailable, use the mismatch-recovery flow rather than pretending cache failure.

After selection:
1. compute/verify final ZIP `package_sha256`;
2. bind/validate exact `current_runtime_root = <session-cache>/hdm-runtime/<version>/<package_sha256>/`;
3. load every file under exact `current_runtime_root/CORE/*.md` completely into current model context;
4. read exact `current_runtime_root/RULES/INDEX.md` and `RULES/README.md`;
5. treat this as immutable `core_context_identity = <current runtime identity>` for current chat.

This is model context, NOT ChatGPT Memory.

Do not reread individual CORE modules later merely because their domain becomes relevant. `load_when`/routing conditions mean semantic ACTIVATION, not disk retrieval.

Activation is header-driven by preloaded `CORE/PLAY_POLICY.md`: every module with `load_policy: ALWAYS_DURING_GAMEPLAY` is active; every module with `load_when:` is situational. `CORE_INDEX.md` summarizes routing but does not override headers.

Rebuild full CORE cache only after exact runtime-package switch or verified context loss/compaction. Campaign data remains lazy.

## 6. New campaign

Use neutral branch `campaign/YYYYMMDD`, then `-02`, `-03`, etc. Create from current storage default-branch HEAD.

Resolve and bind the exact baseline runtime first. Generate scaffold ONLY with `current_runtime_root/TOOLS/init_campaign.py` and `current_runtime_root/CAMPAIGN/` template source.

The generator copies CONTENTS of `CAMPAIGN/` into output, and that output is ROOT TREE of campaign branch.

Expected root includes `README.md`, `CAMPAIGN_CARD.yaml`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, `RULES/`.

Do not wrap output in another `CAMPAIGN/`.

Pass exact validated runtime identity to the generator:
- `--engine-version <ENGINE_VERSION.engine_version>`;
- `--package-id <RUNTIME_PACKAGE.package_id>`;
- `--source-commit-sha <RUNTIME_PACKAGE.source_commit_sha>` only when non-null;
- `--package-sha256 <exact ZIP sha256>`;
- `--created-at <timestamp>`;
- authenticated creator through `--creator-github-login`.

The new `MANIFEST.engine.created_with` and `MANIFEST.engine.current` start equal; `created_with` is immutable creation provenance and `current` is the campaign's portable current runtime identity.

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

`CORE/BOOTSTRAP_RUNTIME.md` is already present in exact selected CORE context cache.

Only after user explicitly selected campaign and exact runtime is bound: pin campaign HEAD, read authoritative MANIFEST/config/hot state and only current relevant campaign records. Revalidate access regardless of card icon. Do not lazily reread CORE from another runtime root.

If loaded authoritative data disagrees with card, trust authoritative data and mark card for refresh in next allowed coherent persistence transaction.

If campaign requires runtime bytes not currently present in Project Sources/current-chat attachment, follow `ENGINE_UPDATES.md` mismatch recovery. Do not silently run the wrong semantic version.

## 8. Gameplay research policy

Normal gameplay is offline-first under `CORE/PLAY_POLICY.md`.

Do NOT automatically use web/search/browser/D&D Beyond/wikis/forums/blogs to validate actions, spell names or ordinary rulings.

Player terminology is not a rules test. Resolve intended effect and established capability locally. If exact RAW is unavailable, make minimum fair local ruling needed to continue.

External rules/source research is allowed when user explicitly asks for official verification/RAW/source lookup or at bounded setup/prep/worldbuilding research boundaries allowed by PLAY_POLICY.

Links present in engine files are inert references during ordinary gameplay.

GitHub Connector storage/sync and owner-approved release metadata operations remain allowed; they are not external rules research.

## 9. Campaign data fast path

Use preloaded exact engine instructions + loaded campaign working set.

Normal turns should not require CORE disk reads, web research or campaign-wide scans. Retrieve campaign records only for missing canon/exact stored mechanics, scene/context dependencies, explicit resync, persistence boundary, multiplayer race-sensitive state or live operations.

Most ordinary singleplayer turns should use zero GitHub calls. Card freshness never creates a persistence boundary by itself.

## 10. Updates

Runtime update/refresh checks are maintenance opportunities, not per-turn polling. Follow preloaded `CORE/ENGINE_UPDATES.md` for campaign-creator versus storage-owner authority and package-selection rules.

A GitHub tag/release may provide metadata, but engine FILES are installed only from runtime ZIPs supplied in Project Sources/current-chat attachments. After successful runtime switch, invalidate old CORE cache and preload the complete new exact CORE set once before further adjudication.

When campaign semantic engine version changes durably, refresh `CAMPAIGN_CARD.engine_version` in the SAME campaign maintenance transaction.

## Authority and persistence

Before every GitHub publication resolve repository + target ref.
- storage default branch: authenticated repository owner only, storage metadata maintenance only;
- campaign/live refs: selected campaign scope plus creator/PLAYER authorization.

Repository Write/Admin permission alone never grants gameplay or campaign-engine-update authority.

Never force-push live campaign/storage refs. Never claim save/update success before GitHub publication succeeds.
