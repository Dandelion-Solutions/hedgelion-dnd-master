# Runtime Bootstrap

runtime_bootstrap_version: 0.8.6
storage_marker: DND_STORAGE.yaml
load_when: project/campaign bootstrap, storage discovery, campaign selection, exact runtime routing

## Repository and package model

D&D Master runtime files come from exact local runtime ZIP packages. GitHub campaign storage does not contain an engine copy.

A Project may expose multiple supported runtime ZIPs simultaneously. Different campaigns may legitimately remain on different semantic engine versions.

Package-root `ENGINE_VERSION.yaml` is the sole machine-authoritative semantic engine contract: version, release status, canonical engine repository, development-owner identity, rules/schema baseline, update compatibility and recommended tag.

Package-root `RUNTIME_PACKAGE.yaml` is the provenance manifest of the exact built artifact. It records logical package identity and source state/commit when truthfully available. Do not infer an old ZIP's source commit only from the current position of a mutable Git tag.

Public `main` of `ENGINE_VERSION.repository` is development state. Gameplay engine files are supplied only by validated local runtime assets, not cloned/downloaded source trees during startup.

Campaign storage default branch contains infrastructure metadata; games live in long-lived `campaign/YYYYMMDD[-NN]` branches and contain campaign data only.

Campaign branches never merge back into storage default branch, public engine repository or each other.

## Lazy package indexing and disposable cache

At new-chat startup, identify available supported `hedgelion-dnd-master-runtime-v<version>.zip` assets without eagerly extracting all of them.

For cheap indexing, inspect only what is required from each candidate archive:
- filename;
- root `ENGINE_VERSION.yaml`;
- root `RUNTIME_PACKAGE.yaml`;
- final ZIP SHA-256 when exact artifact/cache identity is needed.

A package first opened to reach bootstrap is only a bootstrap host. Before substantial setup/gameplay, the EXPLICITLY SELECTED campaign/new-game flow resolves the required portable runtime identity.

Do not assume cache directories from another chat survive. Extracted packages are disposable. If the exact required ZIP is available but its extracted cache is absent/expired/deleted, silently re-extract it; do not ask the player to recreate local cache.

## Exact runtime selection, `current_runtime_root`, and CORE context cache

Do not use existence of one campaign as permission to select its runtime or preload its state.

After explicit campaign/new-game choice, resolve runtime identity from:
- existing campaign: authoritative `MANIFEST.engine.current`;
- new campaign: selected storage `DND_STORAGE.engine.baseline`;
- authorized development test: validated development package identity.

Validate the candidate ZIP/root before use. New-contract packages require root `ENGINE_VERSION.yaml`, root `RUNTIME_PACKAGE.yaml`, and the required runtime sibling directories with no `GAME/`/`DEV/` source wrapper.

Compute/verify the exact ZIP `package_sha256`, then reuse or extract into an isolated cache:

```text
<session-cache>/hdm-runtime/<version>/<package_sha256>/
```

Bind exactly one ephemeral path:

```text
current_runtime_root = <session-cache>/hdm-runtime/<version>/<package_sha256>/
```

`current_runtime_root` MUST NOT be stored in campaign/storage Git or ChatGPT Memory.

After binding, every package-relative runtime read resolves only below `current_runtime_root`: semantic/provenance manifests, `CORE/`, `RULES/`, `SCHEMA/`, templates, `INSTALL/`, migrations and runtime tools.

Sibling cached engine versions are inert while another `current_runtime_root` is active. Do not globally search for the first `ENGINE_VERSION.yaml`, `CORE/`, `RULES/`, template or `TOOLS/init_campaign.py`, and never combine files from sibling cache roots.

After exact package resolution, complete `current_runtime_root/CORE/*.md` instruction set MUST be loaded into current model context once. Also load exact `current_runtime_root/RULES/INDEX.md` and `RULES/README.md`.

This is immutable current-chat engine instruction cache, not ChatGPT Memory and not campaign canon.

Preloaded != active. Activation is header-driven under `PLAY_POLICY.md`: modules marked `load_policy: ALWAYS_DURING_GAMEPLAY` stay active; modules marked `load_when:` activate only when their domain is relevant. `CORE_INDEX.md` is a summary, not a competing policy. Older `load_when` wording never means permission to reread the file.

During normal play do not reread/drop/reload situational CORE modules from disk or GitHub. Scene transitions only change activation set.

Rebuild full CORE cache only after exact runtime-package switch or verified loss of required engine instruction context.

Campaign WORLD/STATE/INDEX/LOG/entities remain lazy and are not preloaded with CORE.

## Development-package identity

When `ENGINE_VERSION.release_status: development`, explicit framework testing is allowed only when authenticated GitHub login equals `ENGINE_VERSION.engine_owner_login`.

For that package:
- logical runtime identity is `dev-v<ENGINE_VERSION.engine_version>`;
- `RUNTIME_PACKAGE.source_state` distinguishes clean HEAD, dirty worktree and non-Git builds;
- dirty/non-Git package source commit SHA may be null;
- exact artifact identity is still the final ZIP SHA-256;
- do NOT query/pin public `main` merely to manufacture provenance.

Normal published packages use release package identity/provenance carried by their own `RUNTIME_PACKAGE.yaml` plus final ZIP digest.

## External research boundary

Apply preloaded `PLAY_POLICY.md` and distinguish live adjudication from preparation.

### Live turn

Do not automatically use external web/search/D&D Beyond/wiki/forum sources to validate player wording/actions or ordinary rules questions. If exact RAW absent locally, make minimum fair local ruling from campaign mechanics, preloaded engine instructions, model rules knowledge, established fiction and causal/common-sense constraints.

External RAW research during live turn is opt-in when user explicitly asks for official verification/RAW/source lookup.

### Setup/prep/worldbuilding

At natural preparation boundary with no unresolved player action, bounded trustworthy-source research MAY be used proactively when it materially improves durable character mechanics, setting accuracy, world texture or lore for current horizon.

Batch research, distill adopted facts/mechanics into campaign/prep state, and do not make ordinary play depend on repeated browsing.

Official sources preferred for exact rules/published facts; reputable wikis secondary; forums/community material may inspire but are not automatic canon authority.

## GitHub Connector policy

Use connected GitHub Connector as normal transport for campaign-storage reads/writes and GitHub identity/metadata.

Do not first use shell git, `gh`, local clone/pull, direct private HTTP or web scraping. Do not copy engine blobs/tree objects into campaign storage and do not reconstruct engine from GitHub.

## Storage discovery

At setup/startup:
1. resolve authenticated GitHub identity;
2. list at most 6 accessible repositories;
3. if more than 5 are visible, ask repository name instead of probing all;
4. otherwise exact-probe only root `DND_STORAGE.yaml` on each default branch;
5. marker existence identifies candidate; semantic validation deferred until needed;
6. one candidate -> select STORAGE; several -> ask which STORAGE; none -> own/friend choice;
7. cache selected storage for current chat.

Selecting one storage never selects one of its campaigns.

Do not use global code search or broad repository scans for storage discovery.

## Storage metadata

New storage uses marker v3:

```yaml
storage_format_version: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "<version>"
    package_id: "<package id>"
    source_commit_sha: "<sha|null>"
    package_sha256: "<sha256>"
    adopted_at: "<timestamp>"
```

`engine.baseline` is the storage-owner-approved default runtime identity for NEW campaigns only. It installs no files and does not automatically change an existing campaign runtime.

Existing campaigns resolve only from their own `MANIFEST.engine.current`; storage baseline never overrides it.

Only authenticated storage owner may persist storage metadata changes. `current_runtime_root` is never storage metadata.

## Campaign layout resolver

New campaigns use root layout: `MANIFEST.yaml`, `CAMPAIGN_CARD.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` directly at branch root.

During menu discovery do not resolve/load full campaign working set.

After a campaign is explicitly selected, resolve authoritative root `MANIFEST.yaml` and prefer its `storage.*` roots. New writes MUST NOT create a `CAMPAIGN/` wrapper.

This implementation cycle does not invent backward migration from old engine-identity fields.

## Campaign menu — card first

Enumerate only `campaign/*`.

For each branch:
1. probe root `CAMPAIGN_CARD.yaml`;
2. if a valid card exists, render menu from card only; do not read MANIFEST just for presentation;
3. if card is missing/invalid, read only the minimum authoritative metadata required by the currently supported campaign layout.

Never load PC/PLAYER/STATE/WORLD/SCENE/LOG merely to render menu.

`CAMPAIGN_CARD.yaml` is a projection, not authority. Use `CAMPAIGN_CARD.md` for card schema/refresh semantics.

### Menu presentation contract

Use one primary emoji per row. These mappings are fixed; do not substitute visually similar or semantically related emoji.

Primary emoji priority:
1. completed -> 🟥;
2. singleplayer and cached creator login differs from current authenticated login -> 🔒;
3. multiplayer and current login absent from cached active participant logins -> 👀;
4. initializing -> 🟡;
5. paused -> ⏸️;
6. active normal candidate -> 🟢;
7. new-game option -> ➕.

Do not add icon explanations to ordinary campaign rows. After every rendered campaign-choice menu, append exactly one separate italic prompt: *Показать легенду?*

If the user asks to show the legend, render exactly:

- 🟢 активная игра (возможен несохраненный прогресс соседнем чате), можно продолжить тут;
- 🟡 незавершённая настройка;
- ⏸️ игра на паузе, никакого несохраненного прогресса в другом чате нет, можно продолжить тут;
- 🟥 завершённая история, продолжение невозможно;
- 🔒 чужая одиночная кампания, доступная только для просмотра;
- 👀 multiplayer-кампания, к которой можно подключиться.
- ➕ начать новую игру.

For unbound multiplayer:
- `open_contributors`: label `можно присоединиться`, but verify collaborator/write eligibility after selection;
- `invite_only`: label `присоединение по приглашению`.

The cached creator/participant login values never grant authority. Real access is revalidated after selection.

### Visible lifecycle

Default menu includes `active`, `paused`, `initializing`, `completed`. `archived` is hidden unless explicitly requested.

Completed campaigns may be shown as ended/history but MUST NOT be silently resumed.

## Campaign selection — mandatory new-chat choice

A new chat MUST NOT infer `resume` from exactly one campaign, active status, recency, previous-chat use, or generic `давай сыграем`/equivalent.

If at least one visible campaign exists and user has not already made an unambiguous current-chat choice, show campaign list plus **Начать новую игру** and wait for explicit choice — even when exactly one campaign exists.

If current-chat request already unambiguously identifies campaign to continue or explicitly says start new game, treat that as choice and do not ask redundantly.

### Selection barrier

Before explicit choice, no selected campaign exists yet. Forbidden:
- gameplay HEAD pin;
- CONFIG/checkpoint/STATE/SCENE/PLAYER/PC/WORLD reads;
- exact runtime resolution from candidate campaign;
- campaign-specific CORE cache choice;
- recap/recovery/resume logic;
- campaign update/migration checks.

Menu remains branches + one small card read per modern campaign.

### Existing campaign after choice

Only then:
1. pin selected campaign HEAD;
2. resolve authoritative MANIFEST/CONFIG at same HEAD;
3. resolve creator/PLAYER authorization when a write may matter;
4. resolve `MANIFEST.engine.current` against indexed local runtime ZIPs and `ENGINE_UPDATES.md`;
5. silently re-extract the chosen exact ZIP if its cache is missing;
6. bind its `current_runtime_root` and ensure CORE cache belongs to it;
7. continue checkpoint/state/scene lazy loading through resolved storage roots.

If card conflicts with authoritative records, authoritative records win and card is refreshed in next allowed coherent campaign transaction.

### New campaign after choice

Resolve selected storage `engine.baseline` to a validated local runtime package, bind its `current_runtime_root`, then follow `CAMPAIGN_SETUP.md`.

Run exact `current_runtime_root/TOOLS/init_campaign.py`. Pass semantic version, package identity, package source SHA when available, exact ZIP SHA-256 and authenticated creator login so new MANIFEST starts with matching `engine.created_with` and `engine.current` identities.

## Write authority

Engine repository writes are not a gameplay operation and are governed by the development/release policy of `ENGINE_VERSION.repository`; development-package authorization inside runtime uses `ENGINE_VERSION.engine_owner_login` rather than a hard-coded login.

Storage default-branch metadata writes require authenticated repository owner.

Campaign/live writes follow campaign creator and active PLAYER rules. Repository Write/Admin permission alone does not extend gameplay or campaign-engine-adoption authority.

Campaign creator remains derived authoritatively from Git history: author login of first campaign-specific initialization commit after branch creation. Cached card creator login is not authority.

## Lightweight campaign read path

Treat GitHub as versioned current-state storage, not something to clone/pull.

Keep active campaign branch + working-set `base_head_sha`.

When campaign synchronization is actually required:
1. fetch active campaign HEAD only;
2. unchanged -> stop;
3. changed -> compare base..HEAD server-side;
4. intersect changed paths with loaded/dirty/current-decision dependencies;
5. fetch only relevant exact records pinned to one HEAD;
6. advance working-set base.

Commit/history reads remain exceptional/bounded. Full local CORE preload does not relax campaign-data lazy retrieval.

## Gameplay startup

This runs ONLY after selection gate resolves to existing campaign.

After selected campaign + selected exact runtime + matching CORE cache:
1. pin campaign HEAD;
2. read resolved MANIFEST/CONFIG as needed;
3. read latest checkpoint/hot STATE through storage roots;
4. read only active scene files;
5. read only relevant PC/PLAYER records;
6. activate always-active CORE modules from cache;
7. activate additional preloaded modules only when current decision requires them;
8. use campaign INDEX to resolve additional WORLD records lazily;
9. store pinned campaign HEAD as working-set base.

If required campaign canon absent/inconsistent, do not invent it.

## Persistence and synchronization

`STORAGE.md`, `PERSISTENCE.md`, `CAMPAIGN_CARD.md`, and `MULTIPLAYER.md` are already present in CORE cache; activate them at applicable boundaries without rereading files.

Singleplayer gameplay writes are creator-only. Multiplayer writes require applicable PLAYER binding/protocol.

Classify publication timing through `DURABILITY_GUARD.md` / explicit domain authorities. Do not invent additional "natural" boundaries in bootstrap. When a forced boundary exists, publish its coherent dirty batch. Never force-update live campaign/storage refs.

Card projection changes join same campaign transaction as their authoritative source changes and never create a separate save boundary.

## Engine updates

Runtime update/refresh checks are event-driven under `ENGINE_UPDATES.md`.

A newer GitHub tag does not install files. Runtime bytes come from Project Sources/current-chat runtime assets. Existing campaigns remain governed by `MANIFEST.engine.current` until an authorized semantic update or compatible same-version refresh applies.

After successful package switch, atomically bind the new `current_runtime_root`, invalidate old CORE cache and build full cache from exact target package once before further adjudication. Do not adjudicate with mixed runtime roots.

When campaign semantic engine version changes durably, update card engine_version inside the same campaign maintenance transaction.

## Canon priority

Project Instructions -> selected local runtime launcher -> this Runtime Bootstrap -> preloaded selected CORE -> campaign MANIFEST/CONFIG -> checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats as supplementary evidence.

`CAMPAIGN_CARD.yaml` is intentionally NOT inserted into canon priority; it is only a menu projection.

Never repair missing canon through plausible invention.
