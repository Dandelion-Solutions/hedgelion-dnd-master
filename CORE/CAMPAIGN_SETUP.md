# Campaign Setup and Branch Initialization

framework_module_version: 0.5.6
load_when: create new campaign, bind player, initialize campaign branch

## Discover before creating

Resolve campaign storage through `BOOTSTRAP_RUNTIME.md`.

If gameplay is requested and no campaign branch is selected:
- enumerate `campaign/*` only;
- read resolved manifests only;
- let the user continue an existing game or create a new one.

## Engine source for a new campaign

A new campaign is initialized from the LOCAL extracted engine package, never from engine files copied into storage.

Read local `ENGINE_VERSION.yaml`.

For a published release resolve its `recommended_tag` to exact public commit SHA.

For explicit engine-owner development testing:
- require authenticated GitHub login == `ENGINE_VERSION.engine_owner_login`;
- identify package as `dev-v<engine_version>`;
- engine SHA fields may be null;
- do not query/pin public untagged `main` merely to manufacture a SHA.

Do not use public untagged `main` as normal player runtime.

## New campaign branch

Create a neutral date-based branch from current storage default-branch HEAD:
- first campaign that date: `campaign/YYYYMMDD`;
- collisions: `campaign/YYYYMMDD-02`, then `-03`, etc.

Do not encode world names, PC names, multiplayer state, owner names or player counts in the branch name.

The branch is created from storage default branch only to establish repository ancestry/parentage. Its FIRST campaign-specific commit replaces inherited storage-root contents with a generated campaign tree. Therefore storage marker/README/other storage-root files are not campaign canon.

## Local scaffold generation

Use local `TOOLS/init_campaign.py`.

The local engine directory `CAMPAIGN/` is a TEMPLATE SOURCE only. The generator copies the CONTENTS of that template directory into its output directory. That output directory is the ROOT TREE of the new campaign branch.

A correct new campaign therefore has root paths such as `README.md`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, and `RULES/`.

Do NOT wrap generator output in another remote `CAMPAIGN/` directory. The earlier nested layout is legacy-only.

The generator:
- fills campaign technical ID, branch, engine identity, created timestamp and initial mode;
- does not contact GitHub;
- does not use base64;
- does not create gameplay lore/world content.

The release skeleton may include template/index/.gitkeep placeholder files. Generating them locally is cheap; GitHub publication must still be one coherent campaign initialization commit rather than one commit per file.

If the generator is unavailable or fails, stop setup. Do not reconstruct the scaffold blob-by-blob from the public engine repository.

## Atomic campaign publication

Before publication resolve:
- selected storage repository;
- campaign branch;
- current branch HEAD/parent;
- authenticated GitHub user.

Publish generated files using UTF-8 Git tree `content` entries (or an equivalent Connector bulk tree operation) in one prepared campaign tree FROM SCRATCH, so storage marker/README are excluded.

Then:
1. create one campaign initialization commit;
2. update the campaign branch once with `force=false`;
3. only after ref publication succeeds consider the campaign created.

Do not explicitly base64 encode scaffold files.
Do not create one commit per scaffold file.
Do not copy local CORE/RULES/SCHEMA/INSTALL files into the campaign branch.

The first campaign initialization commit's `author.login` is the technical campaign creator for access-control purposes.

## Initial manifest

Initialize:
- campaign ID and branch;
- `status: initializing`;
- mode (default `singleplayer` unless multiplayer already chosen);
- engine `base_tag` / `base_sha` from local package identity;
- engine `integrated_tag` / `integrated_main_sha` equal to base values;
- `engine.update_policy: ask`;
- `players.join_policy: invite_only` unless creator explicitly chooses `open_contributors`;
- rules baseline;
- created timestamp.

Current-layout manifest storage roots are `STATE`, `INDEX`, `WORLD`, `LOG`, `CHECKPOINTS`; house rules path is `RULES/HOUSE_RULES.md`.

Do not duplicate creator GitHub identity in MANIFEST.

## Player-facing staged setup

After scaffold publication and before substantial character/world preparation, tell the player once, succinctly:

**«Создание новой игры пройдёт в несколько этапов: сначала соберём персонажа, затем подготовим только нужную стартовую часть мира и сразу перейдём к первой сцене. После каждого этапа я покажу результат и зафиксирую готовую часть.»**

Do not give a duration/time estimate and do not ask the player to wait. Surface player-relevant progress between phases instead of doing one long silent preparation block.

### Stage 1 — Character

Load `CHARACTER.md` plus only exact rules needed for current character decisions.

Resolve the PC first. Do not generate unrelated broad world lore while character identity/mechanics remain unresolved unless a world constraint is genuinely required for an informed PC choice.

When the draft is mechanically valid, present a compact human-readable character summary and obtain explicit player acceptance.

After acceptance create/persist stable PLAYER + PC records and required indexes as one coherent character-stage batch. Tell the player the character stage is complete.

### Stage 2 — Minimal starting world

Use `WORLDGEN.md` and `SAFETY.md`. Create only the starting horizon required for the first meaningful scene: immediate location, relevant actors/pressures/clues, and boundaries/tone actually needed now.

Do not build a continent encyclopedia, full faction network, distant history or unused NPC roster before play. Undefined distant details may remain undefined.

Persist a coherent starting-world batch when ready and give the player only the orientation their PC legitimately knows.

### Stage 3 — First scene

Create starting scene/current-state routing plus initial semantic records and `CP_0000`/latest checkpoint required for reliable resume, then begin play immediately.

Optional deeper worldbuilding happens later through normal prep/lazy world generation.

## Minimum user questions

Ask only decisions that materially affect play now. Typical choices:
- continue/create game;
- singleplayer or explicit multiplayer shared world;
- premise/tone if player wants control;
- PC concept/creation;
- mechanics detail 0..10 (default 3) and decision-support detail (default 6).

Do not force a long session-zero form.

Do not force an engine-update preference during campaign creation; default `ask`.

## Player binding

Create a stable `PLAYER_` record and `PC_` record when accepted, updating corresponding indexes in the same persistence batch.

`invite_only`: creator explicitly establishes the player's binding.

`open_contributors`: follow `MULTIPLAYER.md`; a verified repository collaborator with sufficient access may self-create only their own initial binding.

Mechanics preference defaults:
- `mechanics_detail: 3`
- `decision_support_detail: 6`
- adaptive learning enabled

If player explicitly requests no technical mechanics, initialize both detail levels to 0.

A provisional PC becomes active only after player acceptance and mechanically required choices are valid.

## First world content

Use `WORLDGEN.md`. Create only the starting horizon required for the first scene. Do not populate a full world during initialization.

## Initial durable saves

The scaffold commit establishes campaign identity/creator but not completed session-zero state.

Subsequent setup MAY use separate coherent persistence batches at natural visible phase boundaries: accepted character, starting world, first-scene/checkpoint. This is intentional and protects completed setup while giving the player progress.

Do not create a commit for every question/subchoice. Persist only coherent accepted phases or other HARD commitments.

Do not import experimental content from older chats unless the user explicitly makes it canonical.
