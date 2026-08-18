# Durability Boundary Guard

framework_module_version: 0.3.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding WHEN campaign state must become durable; SAVE_CONTRACT adds explicit save semantics; PERSISTENCE owns HOW publication is transported

## Purpose

Singleplayer should spend long stretches with zero GitHub traffic without allowing irreplaceable setup/play state to exist only in chat. This module is a zero-I/O boundary classifier: merely checking for a boundary performs no repository read.

Durable facts become true in the hot working set immediately. Most are SOFT and are flushed later. Only the boundaries below force publication in ordinary singleplayer.

## Readiness and onboarding

The blank scaffold is not playable state.

`DIEGETIC_ONBOARDING.md` may create one pre-live `PROVISIONAL_IDENTITY` checkpoint containing a provisional PC and resumable setup fiction while lifecycle remains `initializing`.

Before the first true live scene, publish a coherent PLAY_READY frontier containing at least:
- stable PLAYER binding/preferences;
- READY_PC + PC index;
- protagonist/menu projection as applicable;
- minimum starting location/current scene routing;
- only world/index/log records needed for honest resume;
- MANIFEST/card lifecycle `active`.

A separate character-stage commit is optional if character + launch state can be published coherently together.

## Semantic acceptance

No magic `accept/confirm/готово` phrase is required. A mechanically ready character may be treated as accepted when the player explicitly approves it, continues with it without rejecting/correcting material choices, supplies later concrete facts on that basis, or the Master is about to frame true live play using it.

If a materially different unresolved legal capability choice remains, keep the PC provisional and ask only the smallest necessary question.

## Singleplayer forced boundaries

Normal forced publication boundaries are:
1. `PROVISIONAL_IDENTITY` — narrowly as defined by `DIEGETIC_ONBOARDING.md`;
2. character establishment when a READY_PC would otherwise cross another player-turn boundary only in RAM, unless the same response will publish PLAY_READY;
3. PLAY_READY / first true live scene;
4. live focal-location establishment/change when the coarse human-facing `CAMPAIGN_CARD.current_location` should change;
5. campaign lifecycle transition (active/paused/completed/archived/reactivated as valid for the phase);
6. explicit save/session boundary (`SAVE_CONTRACT.md` / intentional pause/end);
7. rare catastrophic continuity boundary whose loss would make resume fundamentally wrong, such as permanent PC death/replacement;
8. concrete safety flush when verified context loss/maintenance suspension would otherwise destroy the hot dirty set.

Domain-specific multiplayer/live/access modules may require earlier shared publication. Their explicit boundary overrides the sparse singleplayer cadence only for that scope.

## What stays SOFT in ordinary singleplayer

These changes normally do NOT force a commit by themselves:
- quest/contract acceptance or progress;
- payments, currency, ordinary rewards/resources;
- ordinary item acquisition/use/loss;
- meeting an NPC, relationship/reputation changes, clues, rumors, promises, debts;
- recurring companion/follower introduction during live play;
- routine HP/resource/tactical changes inside an ongoing sequence;
- ordinary action-sequence/scene/encounter completion when no listed boundary also fires.

They are still canon in the hot working set and MUST join the next applicable transaction.

Several SOFT domains being dirty at once does not automatically create a boundary. "A lot happened" is not a boundary.

A focal-location boundary is coarse: tavern -> market square may count; table -> stairs inside the same tavern normally does not. When a forced boundary fires, flush all causally valid accumulated SOFT state in the same coherent transaction.

## Explicit save is not activation

A save flushes established durable state but never manufactures readiness. If PC is provisional/not READY_PC and the fiction is pre-live onboarding, save the resumable setup truth and keep lifecycle `initializing`.

Only READY_PC + PLAY_READY justify `initializing -> active`.

An unfinished setup that is intentionally stopped remains `initializing`; `paused` is reserved for a campaign that has already reached PLAY_READY/normal play and is then intentionally paused.

## Runtime invariants

Repair before further ordinary play if any is true:
- true live play exists while only blank scaffold is durable;
- normal PC mechanics-dependent play occurs while stable PC/index is absent;
- lifecycle is `active` while PC is provisional/not READY_PC or PLAY_READY is absent;
- lifecycle remains `initializing` after legitimate READY_PC/PLAY_READY live play began;
- a live focal-location transition completed but durable card/current routing still describes the old focal location with no corresponding transaction;
- explicit save/pause/end was acknowledged while promised dirty state was not published.

A durable pre-live onboarding vignette with provisional PC and `initializing` is valid.

## Cadence

Expected singleplayer rhythm:

`scaffold -> optional PROVISIONAL_IDENTITY -> character/PLAY_READY -> many zero-I/O turns -> focal-location/lifecycle/session/save boundary -> one flush -> many zero-I/O turns`

After successful own publication continue from known hot state without confirmation rereads.