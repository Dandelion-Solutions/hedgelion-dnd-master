# Runtime Bootstrap

runtime_bootstrap_version: 0.5.8
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
engine_owner_login: dkolyada
storage_marker: DND_STORAGE.yaml

## Repository and package model

The D&D Master engine used by the current chat comes from an already extracted local release archive. GitHub campaign storage does not contain an engine copy.

Canonical public engine repository:
`Dandelion-Solutions/hedgelion-dnd-master`

Public `main` is development state. Normal gameplay releases are identified by published tags, but source files for gameplay are supplied by the local release ZIP, not downloaded or cloned during startup.

Each player/host uses a separate campaign-storage repository. Its default branch is infrastructure/storage metadata, identified by root `DND_STORAGE.yaml`. Actual games live in long-lived `campaign/YYYYMMDD[-NN]` branches. Campaign branches contain campaign data, not a private copy of CORE/RULES/SCHEMA.

Campaign branches never merge back into storage default branch, the public engine repository, or each other.

## Engine loading

Project Instructions must ensure an engine ZIP has been extracted in the current chat environment before this module runs.

Do not assume extraction persists between chats.

Local availability is not context preloading:
- read `CORE/CORE_INDEX.md` for routing;
- ALWAYS load `CORE/RUNTIME.md` and `CORE/AI_REASONING.md` for gameplay;
- load other local CORE/RULES/SCHEMA files only when required.

If an existing campaign expects a different integrated release from the currently extracted archive, do not silently substitute the local version. Resolve a matching local ZIP or follow an authorized engine-update path.

## GitHub Connector policy

Use the connected GitHub Connector as the normal transport for campaign-storage reads/writes and GitHub metadata/identity checks.

Do not first use shell git, `gh`, local clone/pull, direct private HTTP, or web scraping.

Engine source installation is not a GitHub Connector workflow. Do not copy engine blobs/tree objects into campaign storage and do not reconstruct the engine from GitHub.

Never explicitly use base64 as an installation/scaffold fallback.

## Storage discovery

At new setup/startup:
1. resolve authenticated GitHub identity;
2. list at most 6 accessible repositories;
3. if more than 5 candidates are visible, ask the user for the repository name instead of probing all of them;
4. otherwise check only exact root `DND_STORAGE.yaml` on each repository default branch;
5. marker existence identifies a storage candidate; content validation is deferred until metadata is actually needed;
6. if one candidate exists select it, if several ask which, if none preserve the own-storage/friend-storage choice;
7. cache the selected storage for the current chat.

Do not use global code search or broad repository scans for storage discovery.

## Storage metadata

Storage v2 marker:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<version>"
```

`baseline_version` is the storage owner's approved default engine version for NEW campaigns and maintenance prompts. It does not place engine files on storage default branch and does not automatically change existing campaigns.

Legacy v1 markers remain discovery markers. Their copied engine files are inert legacy data and MUST NOT become runtime source.

Only the authenticated storage repository owner may change storage metadata.

## Campaign selection

Enumerate only `campaign/*` and read manifests only to show the game list.

A user who can read a campaign but lacks gameplay authorization may observe it read-only.

For an existing campaign:
1. pin campaign HEAD;
2. read `CAMPAIGN/MANIFEST.yaml` and CONFIG as needed;
3. resolve creator/PLAYER authorization when a write may matter;
4. ensure the local engine matches `engine.integrated_tag`/`integrated_main_sha` exactly or enter authorized engine maintenance;
5. continue checkpoint/state/scene lazy loading.

For a new campaign follow `CAMPAIGN_SETUP.md`.

## Write authority

Public engine `main` writes require authenticated login `dkolyada`.

Storage default-branch metadata writes require authenticated repository owner.

Campaign/live writes follow campaign creator and active PLAYER rules. Repository Write/Admin permission alone does not extend gameplay authority.

The campaign creator is derived from Git history: author login of the first campaign-specific initialization commit after branch creation.

## Lightweight campaign read path

Treat GitHub as versioned current-state storage, not something to clone/pull locally.

Keep active campaign branch + working-set `base_head_sha`.

When synchronization is required:
1. fetch active branch HEAD only;
2. if unchanged, stop;
3. if changed, compare base..HEAD server-side;
4. intersect changed paths with loaded/dirty/current-decision dependencies;
5. fetch only relevant exact records at one pinned HEAD;
6. advance working-set base.

Commit/history reads remain exceptional and bounded.

The local engine may be fully materialized on disk; the remote campaign repository should still be read lazily.

## Gameplay startup

After campaign + matching engine are resolved:
1. pin campaign HEAD;
2. read MANIFEST/CONFIG as needed;
3. read latest checkpoint/hot STATE;
4. read only active scene files;
5. read only relevant PC/PLAYER records;
6. read local `CORE/CORE_INDEX.md`;
7. ALWAYS load local `CORE/RUNTIME.md` and `CORE/AI_REASONING.md`;
8. load additional local CORE modules only as required;
9. use campaign INDEX files to resolve additional WORLD records;
10. store pinned campaign HEAD as working-set base.

If required canon is absent/inconsistent, do not invent it.

## Persistence and synchronization

Read local `CORE/STORAGE.md` at persistence/resync boundaries and `CORE/MULTIPLAYER.md` for multiplayer/access-mode work.

Singleplayer gameplay writes are creator-only.
Multiplayer writes require the applicable PLAYER binding/protocol.

Normal durable changes are batched at natural boundaries. HARD commitments publish immediately to the applicable canonical frontier. Never force-update live campaign/storage refs.

## Engine updates

Engine updates are event-driven and owner-controlled. See local `CORE/ENGINE_UPDATES.md`.

A newer GitHub release tag does not itself install files. If a new engine package is required, the user supplies the corresponding release ZIP to Project Sources/current chat.

Existing campaigns remain pinned to their integrated release until an authorized update/migration succeeds.

## Canon priority

Project Instructions -> local release launcher -> this Runtime Bootstrap -> campaign MANIFEST/CONFIG -> local current CORE -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
