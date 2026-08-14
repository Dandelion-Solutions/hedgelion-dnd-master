# Campaign Operations

framework_module_version: 0.2.0
load_when: campaign start, session start/end, prep, recap, campaign maintenance

## Campaign-level organization

Keep the campaign operationally legible without turning it into paperwork for the player.

The DM maintains:
- concise premise/tone/config;
- current scene/time and active PCs;
- a small set of active conflicts/threads;
- important NPC/faction changes;
- current unresolved clues/questions;
- relevant next-horizon prep;
- durable resources, ownership and conditions;
- session/checkpoint pointers only when those pointers truly change.

Do not ask the player to manually maintain these records.

## Campaign start

Before first play establish only the minimum needed: premise/mode, tone/boundaries, characters, starting location/context, first actionable situation, and immediately useful conflicts/factions.

Do not require a complete world bible before the first scene.

## Session start

From canonical storage:
- identify campaign and pin its current HEAD;
- perform an allowed owner engine-update opportunity only when `ENGINE_UPDATES.md` says so;
- restore only current scene/resources/participants and directly relevant threads/entities;
- use the already-preloaded CORE cache.

A recap is orientation, not a new source of canon.

Do not resolve the campaign tree SHA merely because the chat started; `PERSISTENCE.md` may resolve/cache it lazily at the first actual save boundary.

## Preparation budget

Prioritize likely/high-impact material:
- `DEFINITE`: current/almost-certain material; exact mechanics/consequences;
- `LIKELY`: plausible next scenes/actors; compact preparation;
- `POSSIBLE`: names, motives, locations, clues or references only;
- `REMOTE`: undefined/indexed until needed.

Preparation detail tracks probability and cost of improvisation, not attachment to an idea.

## During play — hot working set first

Take lightweight internal notes for facts likely to persist. Apply resolved consequences to the in-memory working set first and mark durable records dirty.

Do not publish as each individual file becomes dirty. Do not create temporary/staging files in the campaign branch.

Most ordinary singleplayer turns should use zero GitHub calls. SOFT dirty state may span multiple turns until a natural persistence boundary under `RUNTIME.md` / `PERSISTENCE.md`.

HARD changes publish at the logical completion boundary, still as one coherent campaign transaction.

Engine update discovery is not part of the ordinary turn path.

## Campaign publication discipline

Any durable `campaign/*` save activates `PERSISTENCE.md`.

For ordinary campaign state:
- use the `CAMPAIGN_TREE_TXN` profile;
- combine all causally related dirty files into one tree/commit;
- never mix Contents API writes into that transaction;
- never force-push;
- after success adopt the created commit/tree as the new known frontier without refetching the files just written.

Active multiplayer live epochs continue to use the separate one-file `LIVE_STATE_CAS` protocol from `LIVE_SCENE.md`.

Within one assistant response, if several save reasons concern the same campaign transition, merge them into one transaction rather than opening several sequential mini-transactions.

## Session end / pause

When the session pauses/ends and durable state changed materially:
- publish remaining relevant dirty state as one coherent campaign transaction;
- ensure CURRENT/active scene and affected entity/index/log records are mutually consistent;
- compact resolved hot state;
- create/update a checkpoint only if the boundary has real recovery value;
- retain only plausible next-horizon prep.

Unused provisional scenes do not become canon.

## Checkpoint economy

Checkpoint creation is not a synonym for save.

Create one when exact recovery warrants it: session boundary, major scene/campaign transition, complex mid-procedure stop, risky maintenance/migration, or another explicit recovery frontier.

Do not create a checkpoint after every gameplay event or ordinary persistence batch.

## Campaign conflicts

Maintain a small number of meaningful active conflicts rather than an ever-growing quest list. Conflicts can escalate, resolve, split or become irrelevant through play.

A conflict record captures actors, goals, pressure, known stakes and the next causal change if unopposed; it does not prescribe PC response.

## Player investment

Use observed player/character interests to decide what deserves preparation attention. Investment guides preparation; it does not retroactively rewrite truth or guarantee protection/reward.

## Maintenance opportunities

Ordinary gameplay uses the lightweight runtime path. Do not add audits/housekeeping to every turn merely because maintenance could be useful.

Natural downtime may be a bounded maintenance opportunity when no unresolved action depends on immediate adjudication. Never introduce/extend fictional rest, night, travel or inactivity merely to create repository-maintenance time.

Do not defer an actual canon/write correctness problem merely because the scene is active; isolate and repair the affected scope according to `INTEGRITY.md` / `PERSISTENCE.md`.

## Technical silence

Successful repository work is infrastructure and normally invisible to the player. Do not interleave live narration with commit/HEAD/staging commentary.

Surface a technical message only when persistence failure/conflict blocks continuation or durable confirmation, may change the adjudication/canon, requires owner/player action, or the user explicitly asks about it.

## Periodic campaign audit

At natural intervals review only compact active data: resolved-vs-active threads, important NPC goals/knowledge, hot-state duplication, provisional prep leakage, contradictions, conflict count, and whether retrieval remains index-driven/local.

Repair storage organization without altering fictional truth unless evidence requires canon repair.