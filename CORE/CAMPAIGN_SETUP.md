# Campaign Setup and Branch Initialization

framework_module_version: 0.5.8
load_when: create new campaign, bind player, initialize campaign branch

## Discover before creating

Resolve campaign storage through `BOOTSTRAP_RUNTIME.md`.

If gameplay is requested and no campaign branch is selected:
- enumerate `campaign/*` only;
- prefer `CAMPAIGN_CARD.yaml` / legacy card for fast menu presentation;
- fall back to resolved manifest only when card is missing/invalid;
- let the user explicitly continue/open an existing game or create a new one.

Do not deep-load an existing campaign merely because it is the only one.

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

A correct new campaign therefore has root paths such as `README.md`, `CAMPAIGN_CARD.yaml`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, and `RULES/`.

Do NOT wrap generator output in another remote `CAMPAIGN/` directory. The earlier nested layout is legacy-only.

The generator requires the authenticated campaign creator login through `--creator-github-login`. This value is written only to the compact menu card as a display/access hint; actual creator authority remains derived from Git history.

The generator:
- fills campaign technical ID, branch, engine identity, created timestamp and initial mode;
- initializes `CAMPAIGN_CARD.yaml` with campaign identity, semantic engine version, cached creator login and mode-specific menu shape;
- does not contact GitHub;
- does not use base64;
- does not create gameplay lore/world content.

For singleplayer card initialization:
- `protagonist` exists with null name/role-race placeholders;
- `multiplayer` is null;
- no participant GitHub-login list exists.

For multiplayer card initialization:
- `protagonist` is null;
- `multiplayer.join_policy` starts `invite_only` unless explicitly changed later;
- `multiplayer.participant_github_logins` starts empty and is filled only from active PLAYER bindings.

The release skeleton may include template/index/.gitkeep placeholder files. Generating them locally is cheap; GitHub publication must still be one coherent campaign initialization commit rather than one commit per file.

If generator is unavailable/fails, stop setup. Do not reconstruct scaffold blob-by-blob from public engine repository.

## Atomic campaign publication

Before publication resolve:
- selected storage repository;
- campaign branch;
- current branch HEAD/parent;
- authenticated GitHub user/login.

Publish generated files using UTF-8 Git tree `content` entries (or equivalent Connector bulk tree operation) in one prepared campaign tree FROM SCRATCH, so storage marker/README are excluded.

Then:
1. create one campaign initialization commit;
2. update campaign branch once with `force=false`;
3. only after ref publication succeeds consider campaign created.

Do not explicitly base64 encode scaffold files.
Do not create one commit per scaffold file.
Do not copy local CORE/RULES/SCHEMA/INSTALL files into campaign branch.

The first campaign initialization commit's `author.login` is the authoritative technical campaign creator for access-control purposes. `CAMPAIGN_CARD.creator_github_login` is only a cached menu hint.

## Initial manifest/config/card

Initialize manifest:
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

Campaign config includes `play_style.dnd_lore_fidelity`, a 0..10 campaign-wide preference for how closely fiction follows official D&D lore/terminology/source canon. It NEVER weakens or strengthens D&D mathematics/mechanics.

Initialize card as the compact projection described in `CAMPAIGN_CARD.md`. It mirrors menu-relevant state only and is not added to canon priority.

Do not duplicate creator GitHub identity in MANIFEST.

## Player-facing staged setup

After scaffold publication and before substantial character/world preparation, tell player once, succinctly:

**«Создание новой игры пройдёт в несколько этапов: сначала соберём персонажа, затем подготовим только нужную стартовую часть мира и сразу перейдём к первой сцене. После каждого этапа я покажу результат и зафиксирую готовую часть.»**

Do not give a duration/time estimate and do not ask player to wait. Surface player-relevant progress between phases instead of one long silent preparation block.

## Compact initial questions

Do not expose unexplained engine settings. Ask human questions with anchors.

For a Russian-speaking player, a good compact form is:

1. **Кем хочешь играть?** Достаточно общей идеи персонажа; Master сам переведёт её в механику и уточнит только важные решения.
2. **Сколько игровой механики показывать, 0–10?** `0` — хочу в основном историю, числа/формулы не интересуют; `5` — показывай важные броски и ресурсы; `10` — хочу видеть и сам отслеживать все доступные показатели и расчёты. Если всё равно — `3`.
3. **Мир и стиль.** Можно задать самому или сказать «придумай сам». И насколько «книжным» делать D&D, `0–10`? `0` — механика D&D остаётся честной, но лор, термины и трактовки максимально свободные; `5` — узнаваемый D&D без придирки к каждой мелочи источника; `10` — максимально держимся официального лора, терминологии и опубликованных трактовок. Если всё равно — `3`.

Localize this pattern to player's language. Exact phrase `книжным` is optional; anchors are mandatory because they explain scales.

Player may answer in one natural sentence. Do not require a form.

### Mechanics presentation storage

Store question 2 in PLAYER `preferences.campaign_only.mechanics_detail`.

Default `mechanics_detail: 3` if delegated. `decision_support_detail` defaults to 6, except explicit mechanics-detail 0 defaults both to 0 unless player says otherwise.

### D&D lore/source fidelity storage

Store question 3 source-fidelity answer in campaign `CONFIG.play_style.dnd_lore_fidelity`.

Default to 3 if player delegates/does not care.

This setting controls lore/terminology/source fidelity only. It must never alter dice math, DC fairness, action economy, resources, spell/feature capability, encounter mechanics or already-established campaign rules.

## Stage 1 — Character

Activate `CHARACTER.md` plus only exact rules needed for current character decisions.

Resolve PC first. Do not generate unrelated broad world lore while character identity/mechanics remain unresolved unless a world constraint is genuinely required for an informed PC choice.

A bounded official-source research pass is allowed during character setup when needed to establish exact durable mechanics. Batch it and store result; do not create future per-turn research dependency.

When draft is mechanically valid, present compact human-readable character summary and obtain explicit player acceptance.

After acceptance create/persist stable PLAYER + PC records and required indexes as one coherent character-stage batch. In singleplayer, update the same batch's `CAMPAIGN_CARD.protagonist.name` and `role_race` from the accepted PC. In multiplayer, update cached active participant logins from PLAYER bindings instead; do not create a protagonist entry.

Tell player character stage is complete.

## Stage 2 — Minimal starting world

Activate `WORLDGEN.md`, `PREP.md` as needed, and `SAFETY.md`.

Create only starting horizon required for first meaningful scene: immediate location, relevant actors/pressures/clues, and boundaries/tone actually needed now.

If trustworthy external material would materially improve this horizon, one bounded research/enrichment pass is allowed under `PLAY_POLICY.md`. Source use should respect `CONFIG.play_style.dnd_lore_fidelity`.

Do not research merely because sources exist. Do not build continent encyclopedia, full faction network, distant history or unused NPC roster before play. Undefined distant details may remain undefined.

Persist coherent starting-world batch when ready. In the SAME batch refresh `CAMPAIGN_CARD.current_location` to a human-readable focal location label when known. Give player only orientation their PC legitimately knows.

## Stage 3 — First scene

Create starting scene/current-state routing plus initial semantic records and `CP_0000`/latest checkpoint required for reliable resume, then begin play immediately.

When campaign is actually ready for normal play, set authoritative MANIFEST status `active` and card status `active` in the SAME coherent batch. Do not leave a ready campaign indefinitely marked `initializing`.

Optional deeper worldbuilding/research happens later at normal prep boundaries, not inside routine live turns.

## Card projection during later play

Follow `CAMPAIGN_CARD.md`.

If durable authoritative changes affect protagonist summary, current focal location, campaign name/mode/status, engine version, join policy or active multiplayer membership, mark card dirty and include it in the SAME `CAMPAIGN_TREE_TXN` as those source changes.

Card freshness alone never creates a save boundary and never causes a card-only commit.

`completed` is explicit campaign lifecycle state. Character death does not automatically end campaign; set completed only when campaign is actually concluded. `status_note` may then carry a short human menu reason such as `погиб`.

## Minimum user questions

Ask only decisions that materially affect play now. Compact initial questions normally cover:
- PC concept;
- mechanics presentation preference;
- world/tone delegation;
- D&D lore/source fidelity.

Ask singleplayer/multiplayer only when not already implied/known and materially needed.

Do not force long session-zero form.
Do not force engine-update preference during campaign creation; default `ask`.

## Player binding

Create stable `PLAYER_` record and `PC_` record when accepted, updating corresponding indexes in same persistence batch.

`invite_only`: creator explicitly establishes player's binding.

`open_contributors`: follow `MULTIPLAYER.md`; verified repository collaborator with sufficient access may self-create only their own initial binding.

A provisional PC becomes active only after player acceptance and mechanically required choices are valid.

For multiplayer, active PLAYER binding login labels are projected into `CAMPAIGN_CARD.multiplayer.participant_github_logins` in same durable membership transaction. Inactive bindings are omitted from that cached list.

## First world content

Use `WORLDGEN.md`. Create only starting horizon required for first scene. Do not populate full world during initialization.

## Initial durable saves

Scaffold commit establishes campaign identity/creator but not completed session-zero state.

Subsequent setup MAY use separate coherent persistence batches at natural visible phase boundaries: accepted character, starting world, first-scene/checkpoint. This is intentional and protects completed setup while giving player progress.

Each phase batch includes any corresponding card projection changes; card is never saved separately.

Do not create commit for every question/subchoice. Persist only coherent accepted phases or other HARD commitments.

Do not import experimental content from older chats unless user explicitly makes it canonical.
