# Runtime Bootstrap

runtime_bootstrap_version: 0.4.7
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
engine_development_branch: main
engine_owner_login: dkolyada
storage_marker: DND_STORAGE.yaml

## Repository model

The canonical public engine repository is `Dandelion-Solutions/hedgelion-dnd-master`. Its `main` branch is development state; gameplay installs only published release tags.

Each player/host uses a separate campaign-storage repository. Storage `refs/heads/main` contains the exact tree of one published engine release plus root `DND_STORAGE.yaml`. Actual games are long-lived `campaign/YYYYMMDD[-NN]` branches inside that storage repository. Related live refs are temporary multiplayer operational frontiers.

Campaign branches never merge back into storage `main`, the public engine repository, or each other. Storage `main` moves only through owner-authorized engine baseline installation/upgrade.

## GitHub Connector policy

Use the connected GitHub Connector as the normal/default transport for repository reads and writes. Do not first try shell `git`, `gh`, local clone/pull, direct HTTP/web scraping, container networking, or another transport.

On Connector failure, diagnose connection/runtime binding, authenticated identity, Codex Connector App repository access, GitHub permission/status responses, and only then an actual missing Connector capability. Do not perform speculative transport/API experiments during player setup. Another transport may be considered only after a confirmed Connector capability gap and only when that method is explicitly available in the current product.

For storage initialization/engine-copy boundaries, treat copied engine file bodies as opaque transport data. Copying the full release tree does not authorize semantic reading, summarization, or loading that tree into gameplay context.

The current known Connector has no one-call server-side cross-repository tree copy. Use the launcher-defined Git Data transfer path; do not attempt cross-repository object-SHA reuse or archive/shell tricks. If a future Connector exposes real bulk copy/import, prefer it while preserving exact-tree verification and atomic publication.

## Bootstrap repository resolution

At a new gameplay/setup chat:
1. connect/resolve the authenticated GitHub identity through the GitHub Connector;
2. read the public engine repository and resolve the latest valid published release tag; never treat untagged public `main` commits as installable engine;
3. discover accessible campaign-storage repositories by the exact root marker `DND_STORAGE.yaml` on their default/main branch, using the cheapest supported exact-file/repository query rather than broad content scans;
4. if exactly one valid storage repository is found, select it; if several are found, show a concise player-friendly list; if none are found, ask whether to create the user's own campaign or join a friend's campaign;
5. cache the selected storage repository in current-chat working context.

The public latest tag is installation/update information, not automatically the engine of an existing campaign. Existing gameplay always uses the engine already integrated into the selected campaign branch.

## Storage initialization invariant

When setup creates a new storage repository, prefer a fresh personal repository initialized by GitHub with a README so an existing parent commit is available. Do not manufacture a D&D technical anchor when this can be avoided.

Storage initialization follows this strict order:
1. pin source release commit/root tree and target `main` parent;
2. copy the complete release as opaque Git data without moving target `main`;
3. build a release-only target tree from scratch;
4. verify once that target release root tree SHA exactly equals source release root tree SHA;
5. only then create `DND_STORAGE.yaml` and build the final tree as exact release tree + marker;
6. recheck target parent, create one D&D initialization commit, and move `main` once with `force=false`;
7. consider initialization successful only after the ref update succeeds.

Never verify copied files individually, never create per-file commits, never publish the marker before the release tree is complete, and never use a marker-only `create_file`/`update_file` as an initialization step.

## Player-facing setup discipline

Normal setup messages should describe player goals rather than Git infrastructure. Do not normally mention marker filenames, refs, SHAs, tree checksums, commit topology, blob transfer, or force-push unless the user explicitly requests technical/debug detail or an actionable error requires it.

Prefer wording such as “создать свою кампанию” and “присоединиться к кампании друга”. After successful setup, a simple player-facing confirmation such as “Готово. Всё настроено — можно создавать первую игру.” is sufficient.

## Write authority summary

Public engine `refs/heads/main` requires authenticated login `dkolyada`.

Campaign-storage `refs/heads/main` requires authenticated login == repository owner and is used only for storage initialization/engine baseline upgrade. Campaign-storage v1 expects a personal-account-owned repository; organization-owned storage main is read-only to D&D Master until an explicit maintainer identity model exists.

Campaign/live writes follow campaign creator and active `PLAYER_` rules. Repository Write/Admin permission alone does not extend authority.

## Campaign selection at game start

After storage repository selection, enumerate only its `campaign/*` branches. Read each `CAMPAIGN/MANIFEST.yaml` and present a compact list of existing games. If there are none, offer a new campaign. If the user explicitly selected a campaign, skip the list.

A new campaign branch is created from current storage `main` and initialized through `CAMPAIGN_SETUP.md`.

## Gameplay startup

1. Resolve selected campaign-storage repository and active campaign branch.
2. Resolve active campaign HEAD SHA once and pin the startup read cycle to it.
3. Read `CAMPAIGN/MANIFEST.yaml` / `CONFIG.yaml` only as needed at that SHA.
4. Resolve campaign creator from bounded Git history only when campaign write authorization may matter.
5. Resolve the authenticated GitHub user.
6. If singleplayer, normal gameplay is read-only unless current user == campaign creator.
7. Determine whether current user is the campaign-storage repository owner. If not, this is a guest Master for engine-maintenance purposes: skip public release discovery/update prompting entirely and continue with the campaign-integrated engine.
8. If current user is storage owner, load `CORE/ENGINE_UPDATES.md` at an allowed update opportunity. First consider a storage-main baseline newer than the campaign; query public release tags only when looking for a release newer than storage `main`.
9. If engine integration succeeds, discard stale engine caches, repin campaign HEAD and reread required runtime/bootstrap modules before adjudication.
10. Continue ordinary startup from checkpoint/state/scene using lazy loading.
11. Read only relevant scene file(s) from `CAMPAIGN/STATE/SCENES/` at the pinned SHA.
12. Read only PC records relevant to the current player/turn.
13. Read `CORE/CORE_INDEX.md`.
14. ALWAYS load `CORE/RUNTIME.md` and `CORE/AI_REASONING.md` during gameplay.
15. Load only additional CORE modules required by the situation.
16. Use `CAMPAIGN/INDEX/` to locate additional WORLD records; never broadly scan WORLD.
17. Store the pinned SHA as the working-set base HEAD.

If a required record is absent or inconsistent, do not invent it.

At campaign creation/session-preparation boundaries, use the recommended bundles from `CORE_INDEX.md`; do not keep those larger modules loaded after they stop being relevant.

## Lightweight repository read path

Gameplay synchronization is API-first and current-state-first. Do not clone the repository, run a full `git pull`, download repository archives, or retrieve commit history merely to learn the current world state.

Keep the active campaign branch name and working-set base HEAD SHA cached.

When a synchronization check is required:
1. query only the active branch ref to obtain the current HEAD SHA;
2. if it equals the working-set base HEAD, stop — perform no campaign-content reads;
3. if it differs, ask GitHub to compare `base_HEAD..current_HEAD` server-side and inspect the changed path set;
4. if those paths cannot affect the loaded working set, local dirty paths, access/mode metadata, or the decision being resolved, advance the working-set base HEAD to the current HEAD without re-reading unchanged files;
5. if relevant paths changed, fetch only the exact affected/required records and indexes, all pinned to the same current HEAD SHA, then update the working set and base HEAD;
6. if compare is unavailable or too broad to use safely, fall back to re-reading only the exact records/indexes required for the current decision at the current HEAD — never to full-history/full-repository retrieval.

Commit/history reads are exceptional. Use a bounded range only when required for creator provenance, causal/audit questions, semantic conflict diagnosis, or canon repair.

The cost of ordinary gameplay reads should depend on the current scene and changed relevant paths, not on total campaign age or commit count.

Engine-release discovery is separate from campaign-state synchronization. Do not inspect `main` HEAD or release tags merely because the campaign branch moved. Use only the update opportunities in `ENGINE_UPDATES.md`.

## Lazy loading

NPC -> NPC index -> exact NPC record -> only required dependencies.
Location -> location index -> exact record -> required active entities only.
Past event -> event index -> relevant bounded log segment.
Combat/magic/exploration/dialogue/lore -> corresponding CORE modules only as needed.
A reference A -> B is not permission to load B automatically.

## Persistence and synchronization

Read `CORE/STORAGE.md` at persistence/resync boundaries. Read `CORE/MULTIPLAYER.md` when campaign mode is multiplayer or access mode is being changed.

Singleplayer: only campaign creator may publish gameplay changes. Other repository collaborators may inspect/read but must not write game state. Synchronize HEAD at new-chat startup; within an authorized session use cached working state and publish batched changes at natural persistence boundaries or explicit save/resync.

Multiplayer: partition state by scene/entity, batch local changes, and check HEAD before publishing or before a stale action against a race-sensitive shared object/process. A HEAD check uses the lightweight read path above; a changed HEAD does not imply a full reload. Git conflicts trigger semantic resync, never blind overwrite. Switching mode remains creator-only.

## Framework updates

Published campaign updates come only from stable/prerelease engine release tags, not from current `main` HEAD. Follow `CORE/ENGINE_UPDATES.md` for discovery, user choices, automatic-update policy, safe integration, live-epoch restrictions and post-update cache invalidation.

Stable engine versions use tags in the `vMAJOR.MINOR` form with an optional prerelease suffix, for example `v0.1-beta` or `v0.2-RC`. Integrate the exact selected release tag into live campaigns by merge-style maintenance by default. Rebase is explicit maintenance only for a paused non-concurrent branch and invalidates cached SHAs. Schema-incompatible changes require migration.

## Canon priority

Project Instructions -> Project launcher -> this Runtime Bootstrap -> campaign MANIFEST/CONFIG -> current CORE -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
