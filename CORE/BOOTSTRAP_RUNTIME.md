# Runtime Bootstrap

runtime_bootstrap_version: 0.2-development
repository: dkolyada/hedgelion-dnd-master
engine_branch: main

## Repository model

`main` contains the complete engine plus a fully empty `CAMPAIGN/` skeleton. Each actual game lives in a long-lived `campaign/<name>` branch. Campaign branches never merge back into `main` or into each other.

## Campaign selection at game start

For framework/setup work, use `main`.

If the user wants to play and no active campaign branch is unambiguously selected, enumerate all `campaign/*` branches. For each branch, read only `CAMPAIGN/MANIFEST.yaml` and present a compact list of existing games (name, status, mode; optionally a short manifest-level note). Ask whether to continue one of them or start a new campaign.

If there are no campaign branches, offer to create a new campaign.

If the user explicitly named a campaign branch, use it without listing all games.

A new campaign branch is created from the selected stable engine release/tag and already contains the full empty `CAMPAIGN/` structure inherited from `main`. Initialize manifest/state; then create world/PC content through play/setup.

## Gameplay startup

1. Resolve active campaign branch and HEAD SHA.
2. Read `CAMPAIGN/MANIFEST.yaml`.
3. Read `CAMPAIGN/CHECKPOINTS/LATEST.yaml`.
4. Read `CAMPAIGN/STATE/CURRENT.yaml`.
5. Read only relevant scene file(s) from `CAMPAIGN/STATE/SCENES/`.
6. Read only PC records relevant to the current player/turn.
7. Read `CORE/CORE_INDEX.md` and always load `CORE/RUNTIME.md`.
8. Load only additional CORE modules required by the current situation.
9. Use `CAMPAIGN/INDEX/` to locate additional WORLD records; never broadly scan WORLD.

If a required record is absent or inconsistent, do not invent it.

## Lazy loading

NPC -> NPC index -> exact NPC record -> only required dependencies.
Location -> location index -> exact record -> required active entities only.
Past event -> event index -> relevant bounded log segment.
Combat/magic/exploration/dialogue -> corresponding CORE modules only as needed.
A reference A -> B is not permission to load B automatically.

## Persistence and synchronization

Read `CORE/STORAGE.md` at persistence/resync boundaries. Read `CORE/MULTIPLAYER.md` when campaign mode is multiplayer.

Singleplayer: synchronize HEAD at new-chat startup; within the session use a cached working set and publish batched changes at natural persistence boundaries or explicit save/resync.

Multiplayer: partition state by scene/entity, batch local changes, and check HEAD before publishing or before a stale action against a race-sensitive shared object/process. Git conflicts trigger semantic resync, never blind overwrite.

## Framework updates

Stable engine versions use tags like `engine-v1.0.0`. Integrate newer `main` into live campaigns by merge by default. Rebase is explicit maintenance only for a paused non-concurrent branch and invalidates cached SHAs. Schema-incompatible changes require migration.

## Canon priority

Project Instructions -> Project Source launcher -> this Runtime Bootstrap -> campaign MANIFEST -> current CORE -> latest checkpoint/STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
