# Durability Boundary Guard

framework_module_version: 0.5.0
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding WHEN campaign state must become durable; SAVE_CONTRACT adds explicit save semantics; PERSISTENCE owns HOW publication is transported

## Purpose

Singleplayer should spend long stretches with zero GitHub traffic without allowing irreplaceable setup/play state to exist only in chat. This module is a zero-I/O boundary classifier: merely checking for a boundary performs no repository read.

Durable facts become true in the hot working set immediately. Most are SOFT and are flushed later. Only the boundaries below force publication in ordinary singleplayer.

## Readiness and onboarding

The blank scaffold is not sufficient resumable character/play state.

`DIEGETIC_ONBOARDING.md` may begin gameplay before READY_PC and creates an early `PROVISIONAL_IDENTITY` durability boundary once a stable protagonist/Actor anchor has been adopted. A name is not required; a stable concept or another accepted protagonist anchor may be sufficient.

That first provisional transaction protects already-established PLAYER/Actor/setup/play truth while lifecycle may remain `initializing`. It must not wait for a 100%-filled character dossier.

READY_PC later marks the reconstructable **initial mechanical commitment frontier** under `CHARACTER_READINESS.md`. Before campaign activation/PLAY_READY, publish a coherent frontier containing at least:
- stable PLAYER binding/preferences;
- the same stable PC Actor ID and READY_PC commitment state;
- PC index/current projection as applicable;
- protagonist/menu projection as applicable;
- minimum starting location/current scene routing required for honest resume;
- only world/index/log/runtime records required by accepted owners;
- MANIFEST/card lifecycle `active` when PLAY_READY also succeeds.

A separate READY_PC transaction is optional if the same response can publish PLAY_READY coherently.

## Semantic acceptance

No magic `accept/confirm/готово` phrase is required.

A mechanical commitment may be accepted when supported by one of the onboarding authorities:
- explicit player statement/choice;
- deterministic rules inheritance from already accepted anchors;
- strong rules-valid inference from explicit player concept;
- adopted campaign/rules default;
- deterministic conservative Master default under delegated bookkeeping.

If materially different unresolved legal choices remain and no accepted deterministic/delegated policy selects among them, keep that portion provisional and ask only the smallest necessary question.

Once a mechanical commitment has been relied upon or crosses READY_PC, later situation-aware retuning is not semantic acceptance; it is a prohibited retrofit or a typed repair/correction case.

## Singleplayer forced boundaries

Normal forced publication boundaries are:
1. `PROVISIONAL_IDENTITY` — early stable protagonist/Actor establishment under `DIEGETIC_ONBOARDING.md`;
2. READY_PC establishment when the initial mechanical commitment frontier would otherwise cross another player-turn boundary only in RAM, unless the same response will publish PLAY_READY;
3. PLAY_READY / campaign activation frontier;
4. live focal-location establishment/change when the coarse human-facing `CAMPAIGN_CARD.current_location` should change;
5. campaign lifecycle transition (active/paused/completed/archived/reactivated as valid for the phase);
6. explicit save/session boundary (`SAVE_CONTRACT.md` / intentional pause/end);
7. rare catastrophic continuity boundary whose loss would make resume fundamentally wrong, such as permanent PC death/replacement;
8. concrete safety flush when verified context loss/maintenance suspension would otherwise destroy the hot dirty set;
9. the one-hour dirty durability ceiling defined below.

Domain-specific multiplayer/live/access modules may require earlier shared publication. Their explicit boundary overrides the sparse singleplayer cadence only for that scope.

## What stays SOFT in ordinary singleplayer

These changes normally do NOT force a commit by themselves:
- quest/contract acceptance or progress;
- payments, currency, ordinary rewards/resources;
- ordinary item acquisition/use/loss;
- meeting an NPC, relationship/reputation changes, clues, rumors, promises, debts;
- recurring companion/follower introduction during play;
- routine HP/resource/tactical changes inside an ongoing sequence;
- ordinary action-sequence/scene/encounter completion when no listed boundary also fires;
- deterministic lazy materialization of a post-READY value that does not change committed character capability.

They are still canon/current owner state in the hot working set and MUST join the next applicable transaction.

Several SOFT domains being dirty at once does not automatically create a boundary. "A lot happened" is not a boundary.

A focal-location boundary is coarse: tavern -> market square may count; table -> stairs inside the same tavern normally does not. When a forced boundary fires, flush all causally valid accumulated SOFT state in the same coherent transaction.

## One-hour dirty durability ceiling

The one-hour rule protects canonical HOT/SOFT state from remaining solely in an ephemeral chat/environment for too long. It is **additive** to every stronger/immediate boundary above; it never delays a boundary that should already have fired.

Track the time of the latest known durable campaign frontier as `durable_frontier_time` in the current working set. Reuse already-known commit/frontier metadata; merely evaluating this timer should not require a repository read.

The forced-boundary condition is:

```text
dirty_hot_or_soft == true
AND now - durable_frontier_time >= 1 hour
=> forced durability boundary
```

`dirty_hot_or_soft` means at least one canonical/current campaign owner has a material unpublished change in the current HOT/SOFT working set. EPHEMERAL conversational material that is not canon does not count.

When the condition is true, publish the complete causally coherent dirty campaign batch at the next available authoritative interaction/persistence point before allowing additional ordinary gameplay to extend the stale dirty frontier. Use `PERSISTENCE.md` for transport; this guard owns only the WHEN decision.

A shorter normal boundary may flush the dirty set earlier. A critical/HARD boundary remains immediate under its own rule. Successful publication resets the dirty set and advances `durable_frontier_time` to the new known durable frontier.

### No heartbeat commits

If there is **no dirty canonical/current state**, elapsed wall-clock time alone is not a persistence reason. The one-hour rule MUST NOT create an empty/no-op commit, timestamp-only mutation, checkpoint, or other heartbeat merely to make the latest Git commit appear recent.

The invariant is protection of unpublished accepted state, not continuous repository activity.

### Inactive chat

This runtime does not execute in the background while the user is absent. It cannot promise a commit exactly one hour after the last interaction.

After a long inactive gap, if the current chat/environment still retains dirty HOT/SOFT working state, evaluate the ceiling at the next user interaction before applying a new gameplay action. If the condition is already true, create the required coherent publication first, subject to normal authorization/concurrency checks.

If the environment lost that unpublished dirty state entirely, there are no truthful bytes to reconstruct. Recover only the latest durable campaign frontier and never invent the missing unpublished canon/current state.

## Explicit save is not activation

A save flushes established durable state but never manufactures readiness.

If the PC remains provisional/not READY_PC, save the resumable provisional Actor/build/world/play truth and keep lifecycle `initializing` unless another accepted lifecycle owner says otherwise.

Only READY_PC + PLAY_READY justify `initializing -> active`.

An intentionally stopped campaign that has not reached PLAY_READY remains `initializing`; `paused` is reserved for a campaign that already reached the active lifecycle and is then intentionally paused.

## Runtime invariants

Repair before further dependent play if any is true:
- gameplay has established a stable protagonist anchor while only blank scaffold is durable and PROVISIONAL_IDENTITY should already have fired;
- ordinary PC mechanics-dependent play occurs while stable PC/index is absent;
- lifecycle is `active` while READY_PC or PLAY_READY is absent;
- lifecycle remains `initializing` after legitimate READY_PC + PLAY_READY activation frontier was durably crossed;
- READY_PC was granted while a discretionary initial choice remains open and could change ordinary current-play mechanics;
- a later value is chosen with situational knowledge even though it should have been committed before READY_PC;
- a live focal-location transition completed but durable card/current routing still describes the old focal location with no corresponding transaction;
- explicit save/pause/end was acknowledged while promised dirty state was not published;
- retained dirty HOT/SOFT state has exceeded the one-hour ceiling and ordinary gameplay is continuing without the required durability boundary.

A durable gameplay onboarding sequence with provisional PC and lifecycle `initializing` is valid.

## Cadence

Expected singleplayer rhythm:

```text
scaffold
    -> early PROVISIONAL_IDENTITY
    -> gameplay + rapid baseline materialization
    -> READY_PC / PLAY_READY
    -> many zero-I/O turns
    -> focal-location/lifecycle/session/save/hourly-dirty boundary
    -> one coherent flush
    -> many zero-I/O turns
```

The one-hour ceiling is a safety maximum for dirty state, not the normal desired commit frequency. After successful own publication continue from known hot state without confirmation rereads.
