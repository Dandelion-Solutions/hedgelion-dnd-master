# Runtime Bootstrap

runtime_bootstrap_version: 0.1-development
repository: dkolyada/hedgelion-dnd-master
engine_branch: main

## Repository model

`main` contains only shared engine/framework data: CORE, SCHEMA, TEMPLATE, MIGRATIONS, ARCHITECTURE and INSTALL.

Each actual game lives in its own long-lived branch `campaign/<name>` created from a stable engine release. Campaign branches never merge back into `main` and never merge into each other.

Actual game state exists only under `CAMPAIGN/` in a campaign branch.

## Campaign resolution

For framework/setup work, use `main`.

For gameplay, resolve the active campaign branch before loading game state. If the active branch is not unambiguously known in the current Project/chat context, do not guess it.

Then obtain campaign HEAD and read `CAMPAIGN/MANIFEST.yaml` first.

## Gameplay startup sequence

1. Resolve campaign branch and current HEAD SHA.
2. Read `CAMPAIGN/MANIFEST.yaml`.
3. Read `CAMPAIGN/CHECKPOINTS/LATEST.yaml`.
4. Read `CAMPAIGN/STATE/CURRENT.yaml`.
5. Read only the player-character records relevant to the current turn.
6. Read `CORE/CORE_INDEX.md` and always load `CORE/RUNTIME.md`.
7. Load only additional CORE modules required by the current situation.
8. Use `CAMPAIGN/INDEX/` to locate additional world records; never broadly scan `CAMPAIGN/WORLD/`.

If a required record is absent or inconsistent, do not invent it.

## Engine routing

`CORE/` — modular Dungeon Master framework.
`SCHEMA/` — canonical persistent-data schemas.
`TEMPLATE/` — clean campaign templates.
`MIGRATIONS/` — schema/framework migration protocols.
`ARCHITECTURE/` — system design documentation.
`INSTALL/` — user setup documentation; not gameplay runtime.

## Campaign routing

`CAMPAIGN/MANIFEST.yaml` — identity, mode, versions and storage configuration.
`CAMPAIGN/STATE/` — compact hot state.
`CAMPAIGN/INDEX/` — compact entity/event indexes.
`CAMPAIGN/WORLD/` — canonical persistent world entities.
`CAMPAIGN/LOG/` — append-only bounded semantic event log.
`CAMPAIGN/CHECKPOINTS/` — recovery checkpoints.

## Lazy loading

NPC -> NPC index -> exact record -> only required dependencies.
Location -> location index -> exact record -> only required active entities.
Past event -> event index -> relevant bounded log segment.
Combat -> runtime + combat + adjudication/randomness as needed.
Magic -> runtime + magic + adjudication as needed.
Exploration -> runtime + exploration + relevant location records.
Dialogue -> runtime + relevant NPC records + NPC/dialogue modules.

A reference A -> B is not permission to load B automatically.

## Synchronization

Read `CORE/STORAGE.md` for persistent writes.
Read `CORE/MULTIPLAYER.md` when campaign mode is multiplayer.

Singleplayer: obtain HEAD at new-chat startup; cached state is allowed under the sole-writer assumption until explicit resync or a write conflict.

Multiplayer: verify HEAD before every state-changing turn.

## Framework updates

Stable engine releases are identified by tags like `engine-v1.0.0`.

Integrate newer `main` into campaigns by merge by default. Rebase is explicit maintenance only and invalidates cached SHAs. Schema-incompatible changes require a migration.

## Canon priority

Project Instructions -> Project Source launcher -> this Runtime Bootstrap -> campaign MANIFEST -> current CORE -> latest checkpoint + STATE -> WORLD -> LOG -> current chat -> older chats.

Never repair missing canon through plausible invention.
