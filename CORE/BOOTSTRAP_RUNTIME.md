# Runtime Bootstrap

runtime_bootstrap_version: 0.6.0
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
engine_owner_login: dkolyada
storage_marker: DND_STORAGE.yaml

## Repository and package model

D&D Master runtime files come from the exact local extracted release/development package selected for the campaign. GitHub campaign storage does not contain an engine copy.

Canonical public engine repository: `Dandelion-Solutions/hedgelion-dnd-master`.

Public `main` is development state. Normal gameplay releases are tagged, but gameplay engine files are supplied by local ZIP, not cloned/downloaded during startup.

Campaign storage default branch contains infrastructure metadata; games live in long-lived `campaign/YYYYMMDD[-NN]` branches and contain campaign data only.

Campaign branches never merge back into storage default branch, public engine repository or each other.

## Exact engine selection and CORE context cache

Bootstrap may initially run from any valid local package needed to discover storage/campaign metadata. Before substantial setup or gameplay, resolve the exact package required by the selected/new campaign.

After exact package resolution, the complete local `CORE/*.md` instruction set MUST be loaded into current model context once. Also load `RULES/INDEX.md` and `RULES/README.md`.

This is an immutable current-chat engine instruction cache, not ChatGPT Memory and not campaign canon.

Preloaded != active:
- `RUNTIME.md`, `AI_REASONING.md`, `PLAY_POLICY.md` are always active during gameplay;
- other CORE modules are already present but activate only when their domain is relevant;
- older `load_when` wording is interpreted as activation semantics, not permission to reread the file.

During normal play do not reread/drop/reload situational CORE modules from disk or GitHub. Scene transitions only change the activation set.

Rebuild the full CORE cache only after:
- successful switch to another exact engine package; or
- verified loss of required engine instruction context.

Campaign WORLD/STATE/INDEX/LOG/entities remain lazy and are not preloaded with CORE.

## Development-package identity

When `ENGINE_VERSION.release_status: development`, explicit framework testing is allowed only when authenticated GitHub login equals `ENGINE_VERSION.engine_owner_login`.

For that test package:
- runtime identity is `dev-v<engine_version>`;
- manifest engine SHA fields may be null;
- local extracted package is runtime source;
- do NOT query/pin current public `main` merely to manufacture SHA.

Normal published campaigns use exact release tag + resolved tag commit SHA.

## External research boundary

Normal gameplay is offline-first. Apply preloaded `PLAY_POLICY.md`.

Do not automatically use external web/search/D&D Beyond/wiki/forum sources to validate player wording/actions or resolve ordinary rules questions. If exact RAW is absent locally, make the minimum fair local ruling from campaign mechanics, preloaded engine instructions, model rules knowledge, established fiction and causal/common-sense constraints.

External rules research is opt-in: use it only when user explicitly asks for official verification/RAW/source lookup or during a separate explicit framework-research task.

Links inside local engine files do not trigger browsing.

GitHub campaign persistence/synchronization and owner-authorized release metadata checks remain allowed and are not rules research.

## GitHub Connector policy

Use connected GitHub Connector as normal transport for campaign-storage reads/writes and GitHub identity/metadata.

Do not first use shell git, `gh`, local clone/pull, direct private HTTP or web scraping. Do not copy engine blobs/tree objects into campaign storage and do not reconstruct engine from GitHub.

## Storage discovery

At setup/startup:
1. resolve authenticated GitHub identity;
2. list at most 6 accessible repositories;
3. if more than 5 candidates are visible, ask for repository name instead of probing all;
4. otherwise exact-probe only root `DND_STORAGE.yaml` on each default branch;
5. marker existence identifies candidate; semantic validation is deferred until needed;
6. one candidate -> select; several -> ask; none -> own/friend choice;
7. cache selected storage for current chat.

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
- current: `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `INDEX/`, `WORLD/`, `LOG/`, `CHECKPOINTS/`, `RULES/` directly at branch root;
- legacy: same logical tree under `CAMPAIGN/`.

Resolve once per campaign startup:
1. try root `MANIFEST.yaml`;
2. only if absent try `CAMPAIGN/MANIFEST.yaml`;
3. set root prefix empty/current or `CAMPAIGN/`/legacy;
4. after manifest load prefer `storage.*` roots.

New writes to current layout MUST NOT create a `CAMPAIGN/` wrapper. Local engine template directory `CAMPAIGN/` is scaffold source, not remote path. Opening legacy campaign does not automatically relocate it.

## Campaign selection

Enumerate only `campaign/*` and read resolved manifests only to show game list. A readable but unauthorized campaign may be observed read-only.

For existing campaign:
1. pin campaign HEAD;
2. resolve manifest layout and CONFIG as needed at same HEAD;
3. resolve creator/PLAYER authorization when a write may matter;
4. ensure exact local engine identity matches campaign or enter authorized maintenance;
5. ensure CORE cache belongs to that exact engine;
6. continue checkpoint/state/scene lazy loading through resolved storage roots.

For new campaign follow `CAMPAIGN_SETUP.md` from already-preloaded CORE.

## Write authority

Public engine `main` writes require authenticated login `dkolyada`.

Storage default-branch metadata writes require authenticated repository owner.

Campaign/live writes follow campaign creator and active PLAYER rules. Repository Write/Admin permission alone does not extend gameplay authority.

Campaign creator is derived from Git history: author login of first campaign-specific initialization commit after branch creation.

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

Commit/history reads remain exceptional/bounded.

Full local CORE preload does not relax campaign-data lazy retrieval.

## Gameplay startup

After campaign + matching engine + CORE cache are resolved:
1. pin campaign HEAD;
2. read resolved MANIFEST/CONFIG as needed;
3. read latest checkpoint/hot STATE through storage roots;
4. read only active scene files;
5. read only relevant PC/PLAYER records;
6. activate always-active CORE modules from cache;
7. activate additional preloaded modules only when current decision requires them;
8. use campaign INDEX to resolve additional WORLD records lazily;
9. store pinned campaign HEAD as working-set base.

If required campaign canon is absent/inconsistent, do not invent it.

## Persistence and synchronization

`STORAGE.md` and `MULTIPLAYER.md` are already present in CORE cache; activate them at persistence/resync/multiplayer boundaries without rereading files.

Singleplayer gameplay writes are creator-only. Multiplayer writes require applicable PLAYER binding/protocol.

Batch normal durable changes at natural boundaries. HARD commitments publish immediately to applicable canonical frontier. Never force-update live campaign/storage refs.

## Engine updates

Engine updates are event-driven and owner-controlled under `ENGINE_UPDATES.md`.

A newer GitHub tag does not install files. User supplies corresponding ZIP. Existing campaigns remain pinned until authorized migration succeeds.

After successful package switch, invalidate old CORE cache and build full cache from exact target package once before further adjudication.

## Canon priority

Project Instructions -> local release launcher -> this Runtime Bootstrap -> preloaded current CORE -> campaign MANIFEST/CONFIG -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats as supplementary evidence.

Never repair missing canon through plausible invention.