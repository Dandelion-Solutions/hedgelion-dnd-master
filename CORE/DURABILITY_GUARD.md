# Durability Boundary Guard

framework_module_version: 0.2.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding WHEN campaign state must become durable; PERSISTENCE.md remains authoritative for HOW publication is performed

## Purpose

Low latency does not mean keeping the whole campaign only in chat memory, but singleplayer also does not need a Git commit for every meaningful event.

This module is a zero-I/O boundary classifier. Merely deciding whether a save boundary exists MUST NOT cause a GitHub read. Activate `PERSISTENCE.md` only after a real boundary is reached.

The durability profile is mode-aware. Singleplayer deliberately favors sparse commits and a large hot SOFT working set. Multiplayer/shared-world play may require earlier publication because another player can observe or change shared canon from another chat.

If older setup/runtime/persistence examples imply that every quest, payment, item, companion or relationship change must immediately create a singleplayer commit, this module wins.

## Scaffold is not playable state

The initial generated scaffold commit proves only that an empty campaign container exists.

A campaign MUST NOT enter live play while the authoritative branch still contains only the blank scaffold.

Before the FIRST live scene is presented, publish at least one post-scaffold coherent **PLAY_READY** campaign transaction containing the minimum durable state required to resume that scene correctly.

For singleplayer this normally includes:
- stable PLAYER binding/preferences needed for play;
- stable PC record and PC index entry;
- `CAMPAIGN_CARD.protagonist` summary;
- initial focal location and minimal current-state/scene routing;
- campaign/card lifecycle changed to `active` when normal play is beginning;
- only the minimum world/index/log records needed to resume accurately.

A recurring companion already established before the first scene may be included in PLAY_READY, but do not delay launch to invent broad world content.

A separate character commit is OPTIONAL when character + initial focal location + opening situation are resolved without returning control to the player: they may be combined into one PLAY_READY transaction for lower latency.

However, once the PC is stable enough that the Master intends to treat it as the player's character, that accepted PC MUST NOT cross another player-turn boundary only in RAM. If the Master is about to ask another setup question and return control, persist the stable character first unless the same response is about to publish full PLAY_READY state.

## Acceptance is semantic, not a magic phrase

Do not require an exact `accept`, `confirm`, `готово`, or similar command merely to make an already-settled character durable.

A character is considered accepted when identity and mechanically necessary choices are sufficiently settled for play AND one of these is true:
- the player explicitly approves it;
- after seeing the character summary, the player continues into later setup decisions without rejecting/correcting it;
- the player supplies later concrete facts for that character/party and the Master proceeds on that basis;
- the Master is about to frame the first live scene using that character.

If a materially important class/species/ability/resource choice is genuinely unresolved, the character remains provisional. Do not invent acceptance to avoid a needed question.

Beginning live play itself may not be the first durable acceptance signal after narration; publish durability first.

## Singleplayer sparse-save profile

Singleplayer is optimized for long stretches of zero-GitHub play from the hot working set.

The normal key save boundaries are:
1. **Character establishment** — accepted/stable PC becomes durable, either as a character-stage transaction or inside PLAY_READY.
2. **PLAY_READY / first live scene** — the first playable frontier must exist before narration begins.
3. **Focal location establishment/change** — when the human-readable `CAMPAIGN_CARD.current_location` should change, publish the authoritative location/current-state change + card update and flush all accumulated SOFT dirty canon in the same transaction.
4. **Campaign lifecycle boundary** — pause, completion, archive/reactivation or another explicit status transition that must be visible in the campaign menu.
5. **Explicit save/session boundary** — user asks to save, the session is intentionally paused/ended, or the runtime is entering a known context-loss/maintenance boundary where volatile state would be unsafe.
6. **Rare catastrophic continuity boundary** — a truly exceptional irreversible transition whose loss would make resumption fundamentally wrong (for example PC death/permanent replacement or equivalent campaign-defining break). Use sparingly; this is not a license to classify ordinary rewards or quests as HARD.

A focal-location change means the campaign's menu-level location changes, not every movement within a room, combat grid or local conversation. Examples: tavern -> market square -> old quarry. Moving from one table to another in the same tavern does not create a card/save boundary.

When any key boundary fires, include all causally valid accumulated SOFT changes in the same coherent transaction. Do not make a card-only commit and do not split the accumulated delta into multiple commits.

## What normally remains SOFT in singleplayer

The following are normally durable-but-bufferable SOFT state and do NOT create a commit by themselves:
- accepting or progressing a quest/contract/job;
- receiving/paying ordinary or even meaningful currency/reward/deposit;
- acquiring/using/losing ordinary items or resources;
- meeting a new NPC, changing an NPC relationship, learning a clue or opening a thread;
- gaining a recurring companion/follower during live play;
- reputation, promises, debts, rumors, discoveries and other narrative commitments that can safely ride in the hot working set until the next key boundary;
- routine HP/resource/tactical changes inside an ongoing sequence.

These facts become dirty canon immediately in memory and MUST be included in the next applicable batch. `SOFT` means delayed publication, not optional truth.

If one of these changes also causes a key boundary — for example the party accepts a job and then leaves the tavern for the quarry — the location transaction flushes the contract, payment, NPC/thread changes and current state together.

Do not promote SOFT to an immediate singleplayer save merely because several SOFT domains are dirty at once. Accumulation is intentional.

## Singleplayer safety flush

Do not use a fixed timer, message count or arbitrary dirty-record count as an autosave schedule.

A safety flush outside the key boundaries is exceptional. Use it only when there is a concrete recovery risk, such as:
- verified/strongly indicated context compaction or impending context loss;
- explicit maintenance/package switch that will invalidate the current hot state;
- a complex long-running procedure that must be suspended before a normal location/session boundary;
- another concrete reason the runtime cannot safely carry the dirty working set forward.

"A lot happened" by itself is not enough. Prefer the next normal focal-location/session/lifecycle boundary.

## Multiplayer/shared-world note

Do not apply the sparse singleplayer profile blindly to multiplayer.

Shared facts that another player may observe or act upon can require earlier publication under `MULTIPLAYER.md`, `LIVE_SCENE.md` and normal shared-world synchronization rules. The singleplayer rule that contracts/rewards/companions may wait does not grant permission to hide material shared-world changes from other active players.

## Runtime invariants

The following states are bugs and require a coherent save/repair before further ordinary play:
- a live first scene exists while the campaign branch is still scaffold-only;
- a singleplayer PC is already being played while `PC_INDEX`/stable PC record is still empty remotely;
- campaign/card remain `initializing` after normal live play has begun;
- the Master has completed a focal-location transition in fiction but continues ordinary play with the old durable `CAMPAIGN_CARD.current_location` and no corresponding save transaction;
- an explicit pause/end/save was acknowledged while the dirty working set was not durably published.

Do not expose repair plumbing unless it fails or requires user action.

## Latency discipline

Expected singleplayer rhythm:

`scaffold -> character/PLAY_READY -> many zero-I/O turns -> focal-location/status/session boundary -> one large flush -> many zero-I/O turns`

Most ordinary live turns use zero GitHub calls. Boundary classification itself uses zero GitHub calls. After successful own publication, continue from the known hot state without confirmation rereads.

Do not solve durability by restoring per-turn repository polling or per-event commits.
