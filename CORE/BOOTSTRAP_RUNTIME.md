# Runtime Bootstrap

runtime_bootstrap_version: 0.6.3
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
engine_owner_login: dkolyada
storage_marker: DND_STORAGE.yaml

## Repository and package model

D&D Master runtime files come from exact local extracted release/development package selected for campaign. GitHub campaign storage does not contain engine copy.

Canonical public engine repository: `Dandelion-Solutions/hedgelion-dnd-master`.

Public `main` is development state. Normal gameplay releases are tagged, but gameplay engine files are supplied by local ZIP, not cloned/downloaded during startup.

Campaign storage default branch contains infrastructure metadata; games live in long-lived `campaign/YYYYMMDD[-NN]` branches and contain campaign data only.

Campaign branches never merge back into storage default branch, public engine repository or each other.

## Exact engine selection and CORE context cache

Bootstrap may initially run from any valid local package needed for cheap storage/campaign discovery. Before substantial setup/gameplay, resolve exact package required by EXPLICITLY SELECTED campaign/new-game flow.

Do not use existence of one campaign as permission to select its engine or preload its state.

After exact package resolution, complete local `CORE/*.md` instruction set MUST be loaded into current model context once. Also load `RULES/INDEX.md` and `RULES/README.md`.

This is immutable current-chat engine instruction cache, not ChatGPT Memory and not campaign canon.

Preloaded != active:
- `RUNTIME.md`, `AI_REASONING.md`, `PLAY_POLICY.md` always active during gameplay;
- other CORE modules already present but activate only when domain relevant;
- older `load_when` wording means activation semantics, not permission to reread file.

During normal play do not reread/drop/reload situational CORE modules from disk or GitHub. Scene transitions only change activation set.

Rebuild full CORE cache only after exact package switch or verified loss of required engine instruction context.

Campaign WORLD/STATE/INDEX/LOG/entities remain lazy and are not preloaded with CORE.

## Development-package identity

When `ENGINE_VERSION.release_status: development`, explicit framework testing is allowed only when authenticated GitHub login equals `ENGINE_VERSION.engine_owner_login`.

For that package:
- runtime identity `dev-v<engine_version>`;
- manifest engine SHA fields may be null;
- local extracted package is runtime source;
- do NOT query/pin current public `main` merely to manufacture SHA.

Normal published campaigns use exact release tag + resolved tag commit SHA.

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

Storage v2 marker:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<version>"
```

`baseline_version` is owner-approved default for new campaigns/maintenance. It installs no files and does not automatically change existing campaigns.

Legacy v1 markers remain discovery markers; copied old engine files are inert and MUST NOT become runtime source.

Only authenticated storage owner may change storage metadata.

## Campaign layout resolver

Supported layouts:
- current: `MANIFEST.yaml`, `CAMPAIGN_CARD.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` directly at branch root;
- legacy: logical tree under `CAMPAIGN/`; legacy card, when backfilled, is `CAMPAIGN/CAMPAIGN_CARD.yaml`.

During menu discovery do not resolve/load full campaign working set.

After a campaign is explicitly selected:
1. try root `MANIFEST.yaml`;
2. only if absent try `CAMPAIGN/MANIFEST.yaml`;
3. set root prefix empty/current or `CAMPAIGN/`/legacy;
4. after manifest load prefer `storage.*` roots.

New writes to current layout MUST NOT create `CAMPAIGN/` wrapper. Opening legacy campaign does not automatically relocate it.

## Campaign menu — card first

Enumerate only `campaign/*`.

For each branch:
1. probe root `CAMPAIGN_CARD.yaml`;
2. if absent probe `CAMPAIGN/CAMPAIGN_CARD.yaml`;
3. valid card -> render menu from card only; do not read MANIFEST just for presentation;
4. missing/invalid card -> fall back to root/legacy MANIFEST only.

Never load PC/PLAYER/STATE/WORLD/SCENE/LOG merely to render menu.

`CAMPAIGN_CARD.yaml` is a projection, not authority. Use `CAMPAIGN_CARD.md` for card schema/refresh semantics.

### Menu icon hints

Primary emoji priority:
1. completed -> 🟥;
2. singleplayer and cached creator login differs from current authenticated login -> 🔒;
3. multiplayer and current login absent from cached active participant logins -> 👀;
4. paused/initializing -> 🟡;
5. active normal candidate -> 🟢.

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
- exact engine resolution from candidate campaign;
- campaign-specific CORE cache choice;
- recap/recovery/resume logic;
- campaign update/migration checks.

Menu remains branches + one small card read per modern campaign; legacy fallback may read manifest.

### Existing campaign after choice

Only then:
1. pin selected campaign HEAD;
2. resolve authoritative MANIFEST/CONFIG at same HEAD;
3. resolve creator/PLAYER authorization when a write may matter;
4. ensure exact local engine identity matches campaign or enter authorized maintenance;
5. ensure CORE cache belongs to exact engine;
6. continue checkpoint/state/scene lazy loading through resolved storage roots.

If card conflicts with authoritative records, authoritative records win and card is refreshed in next allowed coherent campaign transaction.

### New campaign after choice

Use selected storage baseline/intended engine and follow `CAMPAIGN_SETUP.md`. Generator receives authenticated creator login so initial card can classify foreign singleplayer cheaply in future menus.

## Write authority

Public engine `main` writes require authenticated login `dkolyada`.

Storage default-branch metadata writes require authenticated repository owner.

Campaign/live writes follow campaign creator and active PLAYER rules. Repository Write/Admin permission alone does not extend gameplay authority.

Campaign creator remains derived authoritatively from Git history: author login of first campaign-specific initialization commit after branch creation. Cached card creator login is not authority.

## Lightweight campaign read path

Treat GitHub as versioned current-state storage, not something to clone/pull.

Keep active campaign branch + working-set `base_head_sha`.

When campaign synchronization is actually required:
1. fetch active branch HEAD only;
2. unchanged -> stop;
3. changed -> compare base..HEAD server-side;
4. intersect changed paths with loaded/dirty/current-decision dependencies;
5. fetch only relevant exact records pinned to one HEAD;
6. advance working-set base.

Commit/history reads remain exceptional/bounded. Full local CORE preload does not relax campaign-data lazy retrieval.

## Gameplay startup

This runs ONLY after selection gate resolves to existing campaign.

After selected campaign + matching engine + CORE cache:
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

Batch normal durable changes at natural boundaries. HARD commitments publish immediately to applicable canonical frontier. Never force-update live campaign/storage refs.

Card projection changes join same campaign transaction as their authoritative source changes and never create a separate save boundary.

## Engine updates

Engine updates are event-driven and owner-controlled under `ENGINE_UPDATES.md`.

A newer GitHub tag does not install files. User supplies corresponding ZIP. Existing campaigns remain pinned until authorized migration succeeds.

After successful package switch, invalidate old CORE cache and build full cache from exact target package once before further adjudication. Update card engine_version inside same campaign migration transaction.

## Canon priority

Project Instructions -> local release launcher -> this Runtime Bootstrap -> preloaded current CORE -> campaign MANIFEST/CONFIG -> checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats as supplementary evidence.

`CAMPAIGN_CARD.yaml` is intentionally NOT inserted into canon priority; it is only a menu projection.

Never repair missing canon through plausible invention.
