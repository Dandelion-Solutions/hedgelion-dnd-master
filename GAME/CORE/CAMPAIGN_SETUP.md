# Campaign Setup and Branch Initialization

framework_module_version: 0.8.1
load_when: create new campaign, bind player, initialize campaign branch

## Discover before creating

Resolve campaign storage through `BOOTSTRAP_RUNTIME.md`.

If gameplay is requested and no campaign branch is selected:
- enumerate `campaign/*` only;
- prefer `CAMPAIGN_CARD.yaml` for fast menu presentation;
- fall back to the minimum authoritative manifest data only when the card is missing/invalid;
- let the user explicitly continue/open an existing game or create a new one.

Do not deep-load an existing campaign merely because it is the only one.

## Runtime source for a new campaign

A new campaign is initialized from one exact validated local runtime package, never from engine files copied into storage.

For New Game in an existing storage, resolve `DND_STORAGE.engine.baseline` to an available validated runtime ZIP under `BOOTSTRAP_RUNTIME.md` / `ENGINE_UPDATES.md`. Bind its isolated `current_runtime_root` before generation.

Read semantic identity only from selected `current_runtime_root/ENGINE_VERSION.yaml` and exact artifact provenance only from `current_runtime_root/RUNTIME_PACKAGE.yaml` plus the final ZIP SHA-256.

For an authorized development package:
- require the owner login of the selected campaign/storage repository to equal `ENGINE_VERSION.engine_owner_login`;
- authenticated user identity, collaborator membership, Write/Admin permission, campaign creator identity, or PLAYER binding is not a substitute for that repository-owner gate;
- logical package identity is `dev-v<engine_version>`;
- dirty/non-Git package source commit may be null;
- do not query/pin public untagged `main` merely to manufacture provenance.

Do not use public untagged `main` as normal player runtime and do not substitute another cached runtime version simply because it is already extracted.

## New campaign branch

Create a neutral date-based branch from current storage default-branch HEAD:
- first campaign that date: `campaign/YYYYMMDD`;
- collisions: `campaign/YYYYMMDD-02`, then `-03`, etc.

Do not encode world names, PC names, multiplayer state, owner names or player counts in the branch name.

The branch is created from storage default branch only to establish repository ancestry/parentage. Its FIRST campaign-specific commit replaces inherited storage-root contents with a generated campaign tree. Therefore storage marker/README/other storage-root files are not campaign canon.

## Local scaffold generation

Use exact selected `current_runtime_root/TOOLS/init_campaign.py`. Do not find another generator elsewhere in the filesystem.

The selected runtime directory `current_runtime_root/CAMPAIGN/` is a TEMPLATE SOURCE only. The generator copies the CONTENTS of that template directory into its output directory. That output directory is the ROOT TREE of the new campaign branch.

A correct new campaign therefore has root paths such as `README.md`, `CAMPAIGN_CARD.yaml`, `MANIFEST.yaml`, `CONFIG.yaml`, `STATE/`, `WORLD/`, `INDEX/`, `LOG/`, `CHECKPOINTS/`, and `RULES/`.

Do NOT wrap generator output in another remote `CAMPAIGN/` directory.

Pass the validated portable runtime identity to the generator:
- `--engine-version <ENGINE_VERSION.engine_version>`;
- `--package-id <RUNTIME_PACKAGE.package_id>`;
- `--source-commit-sha <RUNTIME_PACKAGE.source_commit_sha>` only when non-null;
- `--package-sha256 <exact runtime ZIP sha256>`;
- `--created-at <campaign creation timestamp>`;
- `--creator-github-login <authenticated creator login>`.

The creator login is written only to the compact menu card as a display/access hint; actual creator authority remains derived from Git history.

The generator:
- fills campaign technical ID, branch, portable runtime identity, created timestamp and initial mode;
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

Initialize manifest schema v3 with:
- campaign ID and branch;
- `status: initializing`;
- mode (default `singleplayer` unless multiplayer already chosen);
- `engine.created_with.version`, `package_id`, and `source_commit_sha` from the exact selected runtime identity;
- `engine.current.version`, `package_id`, and `source_commit_sha` initially equal to `created_with`;
- `engine.current.package_sha256` equal to the exact selected runtime ZIP digest;
- `engine.current.adopted_at` equal to the initial adoption/creation timestamp;
- `engine.update_policy: ask`;
- `players.join_policy: invite_only` unless creator explicitly chooses `open_contributors`;
- rules baseline;
- created timestamp.

`engine.created_with` is immutable creation provenance. Future compatible refreshes/semantic updates change only `engine.current` under `ENGINE_UPDATES.md`. Never persist `current_runtime_root` in MANIFEST.

Current-layout manifest storage roots are `STATE`, `INDEX`, `WORLD`, `LOG`, `CHECKPOINTS`; house rules path is `RULES/HOUSE_RULES.md`.

Campaign config includes `play_style.dnd_lore_fidelity`, a 0..10 campaign-wide preference for how closely fiction follows official D&D lore/terminology/source canon. It NEVER weakens or strengthens D&D mathematics/mechanics.

Initialize card as the compact projection described in `CAMPAIGN_CARD.md`. It mirrors menu-relevant state only and is not added to canon priority.

Do not duplicate creator GitHub identity in MANIFEST.

## Human opening and Master channel

After the empty scaffold is durably published, the first player-facing setup message should feel like the beginning of a game, not an installation wizard.

Before asking about the protagonist, introduce the out-of-character Master channel once. For Russian-speaking play, the default wording is:

**«Я — Мастер этой игры. Если в любой момент обратитесь ко мне „Мастер“, я пойму, что вы говорите со мной, а не с кем-то из персонажей мира.
Мы можем играть практически в любом жанре и на любую тему. Если сегодня хочется чего-то определённого — скажите. А если нет, ничего выбирать заранее не обязательно: начнём и посмотрим, какой мир и какая история сложатся по ходу игры.»**

Localize to the player's language and established register while preserving the meaning. Do not repeat this speech on ordinary resume unless the player needs the convention explained again.

This is an invitation, NOT a required genre/tone question. The player may answer with preferences, boundaries, a character concept, all of them in one sentence, or none of them. Silence/delegation on genre is valid and means the Master may begin from a coherent broad premise and calibrate through play.

Do not lead with internal stage names, repository work, readiness gates or a technical setup plan. Routine plumbing remains invisible. Surface progress only when a real delay/blocker or player-relevant decision makes it useful.

`RUNTIME.md` owns interpretation of direct `Мастер` / `Master` address after this convention is established.

## Low-friction initial setup

Do not turn campaign creation into a compulsory Session Zero questionnaire.

Use defaults and natural-language inference whenever the player has not expressed a preference and no consequential decision is blocked.

### Protagonist

Normally ask one human question after the Master introduction:

**«Кем хочешь играть?»**

A broad idea is enough. The Master translates it into mechanics and asks only later choices that materially affect identity/capabilities and cannot be safely delegated.

If the player already supplied a protagonist concept in the same message that started the game, do not ask it again.

### Mechanics presentation

Do NOT require every player to rate mechanics on a 0–10 scale before play.

Infer explicit natural-language preferences when available:
- `механика не интересует`, `не показывай числа` or equivalent -> `mechanics_detail: 0`, and default `decision_support_detail: 0` unless the player says otherwise;
- explicit request for detailed calculations/sheet tracking -> choose an appropriately high value or ask one compact clarification only if necessary;
- no preference -> silently default `mechanics_detail: 3`, `decision_support_detail: 6`.

If a numeric preference would genuinely help, the available anchors remain:
- `0` — mostly story; hide routine numbers/formulas;
- `5` — show important rolls/resources;
- `10` — expose and track all player-visible mechanics/calculations.

Do not ask the scale merely because the field exists.

Store the resolved preference in PLAYER `preferences.campaign_only`.

### World, genre and tone

The opening invitation already gives the player a chance to request a genre, theme, tone or setting. Do not immediately follow it with `Какой жанр?`, `Насколько серьёзно?`, `Уместны ли шутки?` or a style matrix when the player did not volunteer a preference.

If the player delegates, the Master may establish a coherent initial premise/flavor/setting from the protagonist concept and first situation, then let tone become more specific through actual play. Explicit later corrections/preferences override harmless delegated assumptions under normal campaign authority.

A materially intense premise that needs informed buy-in (for example sustained horror, war atrocities, mass death or another potentially distressing focus) is different: follow `SAFETY.md` and disclose the broad theme without spoilers before leaning on it. Ask only the targeted boundary question(s) actually needed.

### D&D lore/source fidelity

Do NOT require the player to rate lore fidelity before play when it does not matter to their concept.

Infer a clear preference if supplied. Otherwise default `CONFIG.play_style.dnd_lore_fidelity: 3` silently.

If exact fidelity becomes material — for example the player specifically requests a published setting or strict canon — one compact clarification may use these anchors:
- `0` — D&D mechanics stay honest, but lore/terminology may be freely reinterpreted;
- `5` — recognizable D&D without policing every source detail;
- `10` — closely follow adopted official lore/terminology unless campaign canon diverges.

This setting controls lore/terminology/source fidelity only. It must never alter dice math, DC fairness, action economy, resources, spell/feature capability, encounter mechanics or already-established campaign rules.

## Stage 1 — Character

Activate `CHARACTER.md` plus only exact rules needed for current character decisions.

Resolve PC first. Do not generate unrelated broad world lore while character identity/mechanics remain unresolved unless a world constraint is genuinely required for an informed PC choice.

A bounded official-source research pass is allowed during character setup when needed to establish exact durable mechanics. Batch it and store result; do not create future per-turn research dependency.

Character setup may be presented directly or through the pre-live vignette in `DIEGETIC_ONBOARDING.md`; a name does not need a separate form field. If PROVISIONAL_IDENTITY fires, persist the provisional PLAYER/PC/setup bundle there and continue building the SAME PC ID.

When the draft is mechanically valid, present a compact human-readable summary if useful. Acceptance is semantic under `DURABILITY_GUARD.md`; do not require a ceremonial `accept/готово`.

Persist/promote stable PLAYER + READY_PC + required indexes as one coherent character-stage or combined PLAY_READY batch. In singleplayer update protagonist projection; in multiplayer update active participant-login cache instead. Tell the player the character stage is complete only when READY_PC is actually complete.

## Stage 2 — Minimal starting world

Activate `WORLDGEN.md`, `PREP.md` as needed, and `SAFETY.md`.

Create only the starting horizon required for the first true live scene: immediate location, relevant actors/pressures/clues, and boundaries/tone actually needed now. Reuse any location/NPC/premise already canonically established by diegetic onboarding; do not regenerate it as a separate world merely because setup has advanced stages.

If trustworthy external material would materially improve this horizon, one bounded research/enrichment pass is allowed under `PLAY_POLICY.md`. Source use should respect `CONFIG.play_style.dnd_lore_fidelity`.

Do not research merely because sources exist. Do not build continent encyclopedia, full faction network, distant history or unused NPC roster before play. Undefined distant details may remain undefined.

Keep the starting-world delta in the hot working set until a `DURABILITY_GUARD.md` boundary requires publication. Normally it joins the character/PLAY_READY launch transaction rather than creating its own commit. When published, refresh `CAMPAIGN_CARD.current_location` in the SAME transaction when the coarse focal location is known. Give player only orientation their PC legitimately knows.

## Stage 3 — First scene

Create/finish the minimum starting scene/current-state routing needed for reliable resume, then begin true live play immediately. A checkpoint is optional unless recovery policy independently requires it; do not manufacture `CP_0000` merely because launch occurs.

Set MANIFEST/card `active` only when READY_PC + PLAY_READY are both true, in the same coherent launch batch. Durable pre-live onboarding remains `initializing`.

Optional deeper worldbuilding/research happens later at normal prep boundaries, not inside routine live turns.

## Card projection during later play

Follow `CAMPAIGN_CARD.md`.

If durable authoritative changes affect protagonist summary, current focal location, campaign name/mode/status, engine version, join policy or active multiplayer membership, mark card dirty and include it in the SAME `CAMPAIGN_TREE_TXN` as those source changes.

Card freshness alone never creates a save boundary and never causes a card-only commit.

`completed` is explicit campaign lifecycle state. Character death does not automatically end campaign; set completed only when campaign is actually concluded. `status_note` may then carry a short human menu reason such as `погиб`.

## Minimum user questions

Ask only decisions that materially affect play now.

For an ordinary delegated singleplayer start, the only initial direct question may be the protagonist concept. Mechanics presentation, broad genre/tone and lore fidelity may use the defaults above and evolve from explicit natural-language feedback.

Ask additional setup questions only when:
- the player volunteered a preference that needs one material clarification;
- two legal character options materially change capabilities and intent does not resolve them;
- a setting/source constraint is required for an informed choice;
- a proposed intense theme requires a targeted boundary check under `SAFETY.md`;
- singleplayer/multiplayer is not already implied/known and is actually needed.

Do not force a long Session Zero form.
Do not ask a preference only to populate a field.
Do not force engine-update preference during campaign creation; default `ask`.

## Player binding

Create stable PLAYER/PC identity records at the first applicable durability boundary: PROVISIONAL_IDENTITY, explicit save, or accepted READY_PC/PLAY_READY. A provisional checkpoint uses `status: provisional`; later promotion reuses the same IDs.

`invite_only`: creator explicitly establishes player's binding.

`open_contributors`: follow `MULTIPLAYER.md`; verified repository collaborator with sufficient access may self-create only their own initial binding.

A provisional PC becomes active only after semantic acceptance and READY_PC; campaign lifecycle becomes active only at PLAY_READY.

For multiplayer, active PLAYER binding login labels are projected into `CAMPAIGN_CARD.multiplayer.participant_github_logins` in same durable membership transaction. Inactive bindings are omitted from that cached list.

## First world content

Use `WORLDGEN.md`. Create only the starting horizon required for the first true live scene. Do not populate full world during initialization.

## Initial durable saves

Scaffold commit establishes campaign identity/creator but not completed Session Zero state.

Subsequent setup persistence follows `DURABILITY_GUARD.md`: optional PROVISIONAL_IDENTITY, accepted READY_PC/character stage when it would otherwise cross a player-turn boundary, PLAY_READY, explicit save/session/safety/one-hour dirty boundaries. Starting-world details alone do not require an extra commit when they can join another required batch.

Each batch includes corresponding card projection changes; card is never saved separately. Do not create a commit for every question/subchoice.

Do not import experimental content from older chats unless user explicitly makes it canonical.
