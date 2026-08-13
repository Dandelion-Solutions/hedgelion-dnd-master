# D&D Project Bootstrap

bootstrap_version: 0.2
status: PRE-CAMPAIGN / FRAMEWORK-DEVELOPMENT
repository: dkolyada/hedgelion-dnd-master
storage: GitHub repository via connected GitHub app

## Prime directive

This file is the single entry point for every new campaign chat. Do not preload the repository. Resolve the current task first, then retrieve only the smallest relevant working set.

Campaign data must never be stored in ChatGPT Memory.

## Startup sequence

1. Read this bootstrap.
2. Read `CHECKPOINTS/LATEST.md` to resolve the latest canonical checkpoint.
3. Read `STATE/CURRENT.md`.
4. Read `STATE/PLAYER.md` when the player character is relevant.
5. Read `CORE/CORE_INDEX.md` and load only the CORE modules required by the current situation.
6. Use `INDEX/` files to locate additional world records. Do not scan `WORLD/` broadly.

If any required startup file does not yet exist, treat the repository as not fully initialized. Do not invent its contents.

## Repository routing

`CORE/` — modular Dungeon Master framework and adjudication rules.
`STATE/` — compact hot state required frequently during play.
`INDEX/` — compact lookup tables mapping stable entity IDs/names to canonical records.
`WORLD/NPC/` — NPC records.
`WORLD/LOCATIONS/` — location records.
`WORLD/FACTIONS/` — faction records.
`WORLD/ITEMS/` — significant item records.
`WORLD/LORE/` — stable world facts.
`WORLD/SECRETS/` — GM-only objective truth and hidden state.
`LOG/` — append-only bounded event-log segments.
`CHECKPOINTS/` — canonical campaign checkpoints.
`INSTALL/` — human-facing installation/setup material; never part of game runtime unless setup is being discussed.

## Lazy-loading rules

NPC mentioned -> `INDEX/NPC_INDEX.*` -> exact NPC record -> only necessary direct dependencies.
Location mentioned -> `INDEX/LOCATION_INDEX.*` -> exact location record -> only necessary active entities.
Old event questioned -> `INDEX/EVENT_INDEX.*` -> relevant bounded `LOG/` segment.
Combat -> load combat/adjudication/randomness modules only as needed.
Magic -> load magic/adjudication modules only as needed.
Exploration/travel -> load exploration module and relevant location records only.
Dialogue/social scene -> load relevant NPC records plus dialogue/NPC modules only.

A reference A -> B is not permission to load B automatically. Retrieve B only if the current decision requires it.

## Persistence

GitHub is the persistent read/write campaign store. Before replacing an existing file, fetch its current version and use the current blob SHA for the update. Do not perform conflicting writes to the same path in parallel.

Significant game changes must be persisted according to the Framework storage protocol. Event history is append-only; current state and indexes may be updated. Git history is an audit trail, but it does not replace the campaign event log.

Never report a state change as permanently saved unless the GitHub write succeeded.

## Canon priority

Project Instructions -> this Bootstrap -> current CORE Framework -> latest canonical Checkpoint + STATE -> canonical WORLD records -> LOG -> current chat -> older chats.

When sources conflict, prefer the newest authoritative canonical record and investigate the conflict when necessary. Never repair missing canon by plausible invention.

## Current initialization state

The repository is being initialized. The earlier exploratory tavern/notice-board test scene is not automatically canonical. The provisional wizard concept may be migrated into canonical PLAYER state only after the framework and campaign initialization are explicitly completed.
