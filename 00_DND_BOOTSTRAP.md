# D&D Project Bootstrap

bootstrap_version: 0.3
status: PRE-CAMPAIGN / FRAMEWORK-DEVELOPMENT
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
storage: GitHub repository via connected GitHub app

## Prime directive

This file is the repository runtime entry point. Never preload the repository. Resolve the current task first, then retrieve only the smallest relevant working set.

Campaign data must never be stored in ChatGPT Memory.

## Repository model

`main` contains only shared engine/framework data: CORE, SCHEMA, TEMPLATE, MIGRATIONS, ARCHITECTURE and INSTALL.

Each actual game lives in its own long-lived branch `campaign/<name>` created from a stable engine release. Campaign branches never merge back into `main` and never merge into each other.

Actual game state exists only under `CAMPAIGN/` in a campaign branch.

## Campaign resolution

For framework/setup work, use `main`.

For gameplay, resolve the active campaign branch before loading game state. If the active branch is not unambiguously known in the current Project/chat context, do not guess it. Ask for or explicitly select the campaign branch.

Then read `CAMPAIGN/MANIFEST.yaml` first. It defines campaign identity, mode, schema version, engine base and storage roots.

## Gameplay startup sequence

1. Resolve the campaign branch and obtain its current HEAD SHA.
2. Read `CAMPAIGN/MANIFEST.yaml`.
3. Read `CAMPAIGN/CHECKPOINTS/LATEST.yaml` to resolve the latest canonical checkpoint.
4. Read `CAMPAIGN/STATE/CURRENT.yaml`.
5. Read player state only for player characters relevant to the current turn.
6. Read `CORE/CORE_INDEX.md`; load only CORE modules required by the current situation.
7. Use `CAMPAIGN/INDEX/` to locate additional world records. Never broadly scan `CAMPAIGN/WORLD/`.

If a required startup record is absent or inconsistent, do not invent it.

## Engine routing

`CORE/` — modular Dungeon Master framework.
`SCHEMA/` — canonical persistent-data schemas.
`TEMPLATE/` — clean campaign templates.
`MIGRATIONS/` — schema/framework migration protocols.
`ARCHITECTURE/` — system design documentation.
`INSTALL/` — user setup documentation; not part of gameplay runtime.

## Campaign routing

`CAMPAIGN/MANIFEST.yaml` — identity, mode, versions and storage configuration.
`CAMPAIGN/STATE/` — compact hot state.
`CAMPAIGN/INDEX/` — compact entity/event indexes.
`CAMPAIGN/WORLD/NPC/` — NPC records.
`CAMPAIGN/WORLD/LOCATIONS/` — location records.
`CAMPAIGN/WORLD/FACTIONS/` — faction records.
`CAMPAIGN/WORLD/ITEMS/` — significant item records.
`CAMPAIGN/WORLD/LORE/` — stable world facts.
`CAMPAIGN/WORLD/SECRETS/` — GM-only objective truth and hidden state.
`CAMPAIGN/LOG/` — append-only bounded semantic event log.
`CAMPAIGN/CHECKPOINTS/` — canonical campaign checkpoints.

## Lazy-loading rules

NPC mentioned -> `CAMPAIGN/INDEX/NPC_INDEX.*` -> exact NPC record -> only necessary direct dependencies.
Location mentioned -> `CAMPAIGN/INDEX/LOCATION_INDEX.*` -> exact location record -> only necessary active entities.
Old event questioned -> `CAMPAIGN/INDEX/EVENT_INDEX.*` -> relevant bounded `CAMPAIGN/LOG/` segment.
Combat -> load combat/adjudication/randomness modules only as needed.
Magic -> load magic/adjudication modules only as needed.
Exploration/travel -> load exploration module and relevant location records only.
Dialogue/social scene -> load relevant NPC records plus dialogue/NPC modules only.

A reference A -> B is not permission to load B automatically.

## Synchronization modes

`singleplayer`: at new-chat startup obtain branch HEAD. During the session the DM may use cached HEAD/entity SHAs because the DM is assumed to be the sole writer. An explicit user resync request invalidates the cache and forces a HEAD refresh. A failed non-fast-forward write also forces resync.

`multiplayer`: mode is enabled/disabled only explicitly. Before every turn capable of changing persistent state, obtain current branch HEAD and compare it with the cached working-set HEAD. If changed, refresh affected state before adjudicating the action.

## Atomic persistence

A logically complete state-changing turn should be persisted as one atomic Git commit using tree -> commit -> fast-forward ref update where available. The commit should include the semantic event-log entry and all related state/entity/index changes.

Never force-update a live campaign branch. A non-fast-forward failure is a concurrency conflict and must trigger resynchronization rather than overwrite.

Git history is a technical audit trail; `CAMPAIGN/LOG` is the semantic history of the world. Keep both.

Never report a state change as permanently saved unless the GitHub write and branch ref update succeeded.

## Framework updates

Stable engine versions are identified by release tags such as `engine-v1.0.0`.

Integrate newer `main` into a live campaign by merge by default. Rebase is allowed only as an explicit maintenance operation on a paused branch with no concurrent sessions; after rebase all cached SHAs are invalid.

Schema-incompatible engine changes require a migration defined under `MIGRATIONS/`.

## Canon priority

Project Instructions -> Project Source launcher/bootstrap -> this repository Bootstrap -> active campaign MANIFEST -> current CORE -> latest canonical checkpoint + STATE -> canonical WORLD records -> LOG -> current chat -> older chats.

When sources conflict, prefer the newest authoritative canonical record and investigate when necessary. Never repair missing canon by plausible invention.

## Current initialization state

No campaign is canonical yet. The earlier exploratory tavern/notice-board scene is not campaign canon. The provisional wizard concept is not bound to any campaign.
