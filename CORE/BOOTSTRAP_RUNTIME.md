# Runtime Bootstrap

runtime_bootstrap_version: 0.1.0
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

A new campaign branch is created from the selected stable engine release/tag using the technical date-based branch ID and already contains the full empty `CAMPAIGN/` structure inherited from `main`. Initialize manifest/config/state; then create world/PC content through setup/play.

## Gameplay startup

1. Resolve active campaign branch and HEAD SHA.
2. Read `CAMPAIGN/MANIFEST.yaml` and `CAMPAIGN/CONFIG.yaml` only as needed.
3. Resolve campaign creator from Git history when write authorization may matter: `author.login` of the first campaign-specific initialization commit.
4. Resolve the currently authenticated GitHub user.
5. If mode is `singleplayer`, treat the session as read-only unless current GitHub user == campaign creator.
6. Read `CAMPAIGN/CHECKPOINTS/LATEST.yaml`.
7. Read `CAMPAIGN/STATE/CURRENT.yaml`.
8. Read only relevant scene file(s) from `CAMPAIGN/STATE/SCENES/`.
9. Read only PC records relevant to the current player/turn.
10. Read `CORE/CORE_INDEX.md`.
11. ALWAYS load `CORE/RUNTIME.md` and `CORE/AI_REASONING.md` during gameplay.
12. Load only additional CORE modules required by the situation.
13. Use `CAMPAIGN/INDEX/` to locate additional WORLD records; never broadly scan WORLD.

If a required record is absent or inconsistent, do not invent it.

At campaign creation/session-preparation boundaries, use the recommended bundles from `CORE_INDEX.md`; do not keep those larger modules loaded after they stop being relevant.

## Lazy loading

NPC -> NPC index -> exact NPC record -> only required dependencies.
Location -> location index -> exact record -> required active entities only.
Past event -> event index -> relevant bounded log segment.
Combat/magic/exploration/dialogue/lore -> corresponding CORE modules only as needed.
A reference A -> B is not permission to load B automatically.

## Persistence and synchronization

Read `CORE/STORAGE.md` at persistence/resync boundaries. Read `CORE/MULTIPLAYER.md` when campaign mode is multiplayer or access mode is being changed.

Singleplayer: only campaign creator may publish gameplay changes. Other repository collaborators may inspect/read but must not write game state. Synchronize HEAD at new-chat startup; within an authorized session use cached working state and publish batched changes at natural persistence boundaries or explicit save/resync.

Multiplayer: partition state by scene/entity, batch local changes, and check HEAD before publishing or before a stale action against a race-sensitive shared object/process. Git conflicts trigger semantic resync, never blind overwrite. Switching mode remains creator-only.

## Framework updates

Stable engine versions use tags like `engine-v0.1.0`. Integrate newer `main` into live campaigns by merge by default. Rebase is explicit maintenance only for a paused non-concurrent branch and invalidates cached SHAs. Schema-incompatible changes require migration.

## Canon priority

Project Instructions -> Project Source launcher -> this Runtime Bootstrap -> campaign MANIFEST/CONFIG -> current CORE -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
