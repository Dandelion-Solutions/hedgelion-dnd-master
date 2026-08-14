# Runtime Bootstrap

runtime_bootstrap_version: 0.1.4
repository: dkolyada/hedgelion-dnd-master
engine_branch: main

## Repository model

`main` contains the complete engine plus a fully empty `CAMPAIGN/` skeleton. Each actual game lives in a long-lived technical branch named `campaign/YYYYMMDD` by creation date. If more than one campaign is created on the same date, use deterministic suffixes: `campaign/YYYYMMDD-02`, `-03`, etc.

Branch names are intentionally lore-neutral and mode-neutral. Campaign display name, premise, players and `singleplayer`/`multiplayer` mode live in `CAMPAIGN/MANIFEST.yaml` / `CONFIG.yaml`, never in the branch name.

Campaign branches never merge back into `main` or into each other.

## Campaign selection at game start

For framework/setup work, use `main`.

If the user wants to play and no active campaign branch is unambiguously selected, enumerate all `campaign/*` branches. For each branch, read only `CAMPAIGN/MANIFEST.yaml` and present a compact list of existing games (display name if established, technical branch/date, status, mode; optionally a short manifest-level note). Ask whether to continue one of them or start a new campaign.

If there are no campaign branches, offer to create a new campaign.

If the user explicitly named a campaign branch or unambiguously selected a listed campaign, use it without listing all games again.

A new campaign branch is created from the selected stable engine release/tag using the technical date-based branch ID and already contains the full empty `CAMPAIGN/` structure inherited from that tagged release. Initialize manifest/config/state; then create world/PC content through setup/play.

## Gameplay startup

1. Resolve active campaign branch and its current HEAD SHA once.
2. Pin the startup read cycle to that exact SHA. Do not mix branch-relative file reads from a moving HEAD.
3. Read `CAMPAIGN/MANIFEST.yaml` and `CAMPAIGN/CONFIG.yaml` only as needed at the pinned SHA.
4. Resolve campaign creator from Git history only when write authorization may matter: `author.login` of the first campaign-specific initialization commit. Cache the resolved identity for the session unless a maintenance/access change requires revalidation.
5. Resolve the currently authenticated GitHub user.
6. If mode is `singleplayer`, treat the session as read-only unless current GitHub user == campaign creator.
7. If the current user is the campaign creator, load `CORE/ENGINE_UPDATES.md` from the campaign branch and perform the startup release-tag opportunity described there. This checks published engine tags, never untagged `main` HEAD. Non-owner multiplayer sessions skip campaign-wide update prompting.
8. If a tagged engine update is successfully integrated, discard the old startup engine cache, repin the campaign branch to the new HEAD, reread this bootstrap and the manifest from that new HEAD, then continue startup. Do not keep adjudicating from pre-update CORE content.
9. Read `CAMPAIGN/CHECKPOINTS/LATEST.yaml` at the pinned SHA.
10. Read `CAMPAIGN/STATE/CURRENT.yaml` at the pinned SHA.
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

Project Instructions -> Project Source launcher -> this Runtime Bootstrap -> campaign MANIFEST/CONFIG -> current CORE -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
