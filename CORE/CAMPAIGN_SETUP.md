# Campaign Setup and Branch Initialization

framework_module_version: 0.2-development
load_when: create new campaign, bind player, initialize empty campaign branch

## Discover before creating

If gameplay is requested and no campaign branch is selected, follow `BOOTSTRAP_RUNTIME.md`: list `campaign/*`, read manifests only, then let the user continue an existing game or start a new one.

## New campaign branch

Create the new campaign from the selected stable engine release/tag using a neutral date-based technical branch ID:
- first campaign created on a date: `campaign/YYYYMMDD`;
- if that branch already exists, use `campaign/YYYYMMDD-02`, then `-03`, etc.

Do not put world names, PC names, multiplayer state, author names or player counts into the branch name. Those are mutable campaign metadata, not branch identity.

The branch already inherits the complete empty `CAMPAIGN/` skeleton from `main`; do not recreate directory structure file-by-file.

Initialize only the values needed to make the campaign identifiable and playable:
- campaign ID/display name if established, branch/status/mode;
- engine base tag/SHA and integrated-main SHA;
- rules baseline and advancement method;
- player binding(s);
- campaign premise/tone/boundaries if already chosen;
- PC creation state;
- starting scene/location only when play is ready to begin.

Do not populate a full world during initialization.

## Campaign creator provenance

The first persistence commit that initializes the inherited empty `CAMPAIGN/` skeleton is the campaign-specific initialization commit.

Its GitHub `author.login` is the technical campaign owner/creator for access-control purposes. Do not duplicate that identity into `MANIFEST`.

This first commit should contain the coherent campaign initialization state after required setup choices are settled. Later code derives ownership from Git history.

Owner-only operations include switching `singleplayer <-> multiplayer` and other explicit access-mode changes.

In `singleplayer`, only this creator is permitted by the gameplay protocol to publish campaign-state commits. Other repository collaborators may read/observe but not play into or modify the branch.

## Minimum user questions

Ask only decisions that materially affect the game now. Typical first-run choices may be:
- continue existing campaign or create new;
- singleplayer or explicit multiplayer shared world;
- broad campaign premise/tone if the user wants control over it;
- PC concept/creation choices;
- once per new campaign player, preferred mechanics detail on a `0..10` scale; use default `3` when the player does not care, with decision-support default `6`.

Do not ask the user to invent a branch name. The technical branch ID is generated automatically from creation date.

Do not force the player through a long session-zero form if preferences can emerge naturally and safely during play.

## Campaign config

Store campaign-level choices in `CAMPAIGN/CONFIG.yaml`, including premise/tone, advancement method, world/setting mode and explicit campaign boundaries. These are campaign data and never ChatGPT Memory.

## Player binding

Create a stable `PLAYER_` record under `CAMPAIGN/WORLD/PLAYERS/` and a `PC_` record under `CAMPAIGN/WORLD/PCS/` when accepted. Add both to indexes in the same setup persistence batch.

Bind player-facing mechanics preferences to the `PLAYER_` record. If unanswered, initialize `mechanics_detail: 3`, `decision_support_detail: 6`, and adaptive preference learning enabled. If the player explicitly requests no technical mechanics, initialize both detail levels to `0`.

A provisional PC may exist during creation but becomes `active` only after explicit player acceptance and mechanically required choices are valid.

Repository collaborator access is not equivalent to player binding.

## First world content

Use `WORLDGEN.md`: create only the starting horizon required for the first scene. Establish location/NPC/faction records only when they actually exist in the starting situation or are required by the premise/PC.

## Initial save

Campaign initialization should normally be one coherent persistence batch/commit after the required choices are settled. Create initial `CP_0000`/latest checkpoint so a fresh chat can resume without setup transcript.

Do not import experimental scenes or character drafts from earlier chats unless the user explicitly asks to make them canonical.
