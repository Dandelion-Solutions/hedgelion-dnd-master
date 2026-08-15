# Durability Boundary Guard

framework_module_version: 0.1.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding WHEN campaign state must become durable; PERSISTENCE.md remains authoritative for HOW publication is performed

## Purpose

Low latency does not mean keeping important campaign canon only in chat memory.

Most ordinary turns should still use zero GitHub calls, but the runtime must recognize semantic durability boundaries early enough that a context loss, app close, or new chat would not erase the actual game.

This module is an in-memory boundary classifier. Merely checking whether a boundary exists MUST NOT cause a GitHub read. Activate `PERSISTENCE.md` only when a real publication boundary is reached.

If older setup/runtime text treats an already-established character or other durable state as indefinitely provisional merely because the player did not say an exact confirmation phrase, this module wins.

## Scaffold is not playable state

The initial generated scaffold commit proves only that an empty campaign container exists.

A campaign MUST NOT enter live play while the authoritative branch still contains only the blank scaffold.

Before the FIRST live scene is presented, publish at least one post-scaffold coherent **PLAY_READY** campaign transaction containing the minimum durable state required to resume that scene correctly.

For singleplayer this normally includes:
- stable PLAYER binding/preferences needed for play;
- stable PC record and PC index entry;
- `CAMPAIGN_CARD.protagonist` summary;
- minimal current location / current-state routing / opening scene state;
- campaign/card lifecycle changed to `active` when normal play is beginning;
- any recurring companion or other actor already established as part of the starting situation;
- only the minimum world/index/log records needed to resume accurately.

Do not create broad world content merely to satisfy this barrier.

A separate character commit is OPTIONAL when character + minimal starting situation are resolved in one uninterrupted assistant turn: they may be combined into one PLAY_READY launch transaction for lower latency.

However, once the PC has become stable enough that the Master intends to treat it as the player's character, that accepted character MUST NOT cross another player-turn boundary only in RAM. If the Master is about to ask another setup question and return control to the user, persist the stable character first unless the same response is about to publish the full PLAY_READY launch transaction.

## Acceptance is semantic, not a magic phrase

Do not require the player to say an exact `accept`, `confirm`, `готово`, or similar command merely to make an already-settled character durable.

A character is considered accepted when its identity and mechanically necessary choices are sufficiently settled for actual play AND one of these is true:
- the player explicitly approves it;
- after receiving the character summary, the player continues into later setup decisions without rejecting/correcting the character;
- the player supplies later concrete facts for that character/party and the Master proceeds on that basis;
- the Master is about to frame the first live scene using that character.

If a materially important class/species/ability/resource choice is still genuinely unresolved, the character remains provisional. Do not invent acceptance to avoid a needed question.

Beginning live play itself is never allowed to be the first durable acceptance signal after narration; durability must be published first.

## HARD semantic boundaries

A HARD commitment is a durable fact whose loss would make a resumed game materially false, unfair, or contradictory.

The following normally create an immediate persistence boundary when they become settled:
- accepting a quest, contract, bargain, oath, employment, debt, promise, or other obligation with meaningful terms;
- receiving or paying a meaningful/plot-relevant amount of currency, reward, deposit, debt payment, or other resource transfer;
- acquiring, losing, giving away, consuming, stealing, or destroying a plot-relevant or materially important item/resource;
- recruiting, dismissing, permanently losing, or substantially redefining a recurring companion/follower/party member;
- PC death, permanent transformation, level/progression milestone, lasting injury/condition, or another major persistent capability/status change;
- durable ownership, allegiance, reputation, relationship, legal/social status, or faction-standing changes that future play must respect;
- an irreversible revelation/decision whose disappearance after context loss would change future choices or established truth.

These examples are semantic, not exhaustive.

`Immediate` still means ONE coherent campaign transaction containing all causally related changes. It never means one commit per file or one GitHub call per fact.

Routine transient HP movement inside an unresolved encounter, incidental coin accounting with no material continuity value, short-lived tactical positions, and similar high-frequency details may remain SOFT until the appropriate encounter/sequence boundary unless another rule makes them HARD.

## Safety flush for accumulated SOFT canon

Do not use a fixed timer or fixed number of chat messages as an autosave schedule.

Instead, before handing control back to the player, perform a zero-I/O in-memory recovery-risk check.

At the next quiet/natural beat, flush SOFT dirty state when continued buffering has become recovery-sensitive. Strong signals include:
- several independent durable domains are now dirty at once (for example recurring actor + active objective/thread + ownership/resource change);
- a new recurring NPC/companion and the relationship that makes them recurring are already established;
- multiple meaningful scene consequences would be difficult to reconstruct exactly from the last durable frontier;
- a scene transition is occurring while important dirty canon from the previous scene remains unsaved;
- the campaign has accumulated enough accepted facts that losing the current chat would materially change the resumed situation.

The goal is not frequent commits. The goal is to prevent a long stretch of real play from existing only in volatile context.

## Runtime invariants

The following states are bugs and require an immediate coherent save/repair before further ordinary play:
- a live first scene exists while the campaign branch is still scaffold-only;
- a singleplayer PC is already being played while `PC_INDEX`/stable PC record is still empty remotely;
- campaign/card remain `initializing` after the campaign is already operating as normal live play;
- a settled HARD commitment has been narrated as completed while no durable transaction for it has succeeded.

Do not expose the repair plumbing unless it fails or requires user action.

## Latency discipline

Durability checking itself is cheap and local.

Expected pattern:
- most live turns: zero GitHub calls;
- character/setup: at most one character boundary and/or one combined PLAY_READY launch transaction, not a commit after every answer;
- normal play: save only at HARD or meaningful recovery boundaries;
- after successful own publication, continue from known hot state without confirmation rereads.

Do not solve durability by restoring per-turn repository polling.