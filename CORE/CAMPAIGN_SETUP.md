# Campaign Setup and Branch Initialization

framework_module_version: 0.1-development
load_when: create new campaign, bind player, initialize empty campaign branch

## Discover before creating

If gameplay is requested and no campaign branch is selected, follow `BOOTSTRAP_RUNTIME.md`: list `campaign/*`, read manifests only, then let the user continue an existing game or start a new one.

## New campaign branch

Create `campaign/<name>` from the selected stable engine release/tag. The branch already inherits the complete empty `CAMPAIGN/` skeleton from `main`; do not recreate directory structure file-by-file.

Initialize only the values needed to make the campaign identifiable and playable:
- campaign ID/name/branch/status/mode;
- engine base tag/SHA and integrated-main SHA;
- rules baseline and advancement method;
- player binding(s);
- campaign premise/tone/boundaries if already chosen;
- PC creation state;
- starting scene/location only when play is ready to begin.

Do not populate a full world during initialization.

## Minimum user questions

Ask only decisions that materially affect the game now. Typical first-run choices may be:
- continue existing campaign or create new;
- singleplayer or explicit multiplayer shared world;
- broad campaign premise/tone if the user wants control over it;
- PC concept/creation choices.

Do not force the player through a long session-zero form if preferences can emerge naturally and safely during play.

## Campaign config

Store campaign-level choices in `CAMPAIGN/CONFIG.yaml`, including premise/tone, advancement method, world/setting mode and explicit campaign boundaries. These are campaign data and never ChatGPT Memory.

## Player binding

Create a stable `PLAYER_` record under `CAMPAIGN/WORLD/PLAYERS/` and a `PC_` record under `CAMPAIGN/WORLD/PCS/` when accepted. Add both to indexes in the same setup persistence batch.

A provisional PC may exist during creation but becomes `active` only after explicit player acceptance and mechanically required choices are valid.

## First world content

Use `WORLDGEN.md`: create only the starting horizon required for the first scene. Establish location/NPC/faction records only when they actually exist in the starting situation or are required by the premise/PC.

## Initial save

Campaign initialization should normally be one coherent persistence batch/commit after the required choices are settled. Create initial `CP_0000`/latest checkpoint so a fresh chat can resume without setup transcript.

Do not import experimental scenes or character drafts from earlier chats unless the user explicitly asks to make them canonical.
