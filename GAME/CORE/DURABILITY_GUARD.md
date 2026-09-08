# Durability Boundary Guard

framework_module_version: 1.0.2
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for deciding WHEN campaign state must become durable; SAVE_CONTRACT adds explicit save semantics; PERSISTENCE owns HOW publication is transported

## Purpose

Singleplayer should spend long stretches with zero GitHub traffic without allowing irreplaceable setup/play state to remain exposed to avoidable loss. This module is a zero-I/O boundary and durability-exposure classifier: merely checking a boundary or exposure state performs no repository read.

Durable facts become true in the hot working set immediately. Most are SOFT and are flushed later. Stronger owner-defined HARD edges below still require publication before their named continuation edge. Separately, deferrable dirty state follows the `NORMAL / ELEVATED / DANGER` loss-protection trajectory defined here; that trajectory does not create correctness HARD.

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

Normal owner-defined forced publication boundaries are:
1. `PROVISIONAL_IDENTITY` — early stable protagonist/Actor establishment under `DIEGETIC_ONBOARDING.md`;
2. READY_PC establishment when the initial mechanical commitment frontier would otherwise cross another player-turn boundary only in RAM, unless the same response will publish PLAY_READY;
3. PLAY_READY / campaign activation frontier;
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
- recurring companion/follower introduction during play;
- routine HP/resource/tactical changes inside an ongoing sequence;
- ordinary action-sequence/scene/encounter completion when no listed boundary also fires;
- deterministic lazy materialization of a post-READY value that does not change committed character capability.

They are still canon/current owner state in the hot working set and MUST join the next applicable transaction.

Several SOFT domains being dirty at once does not automatically create a boundary. "A lot happened" is not a boundary.

A focal-location boundary is coarse: tavern -> market square may count; table -> stairs inside the same tavern normally does not. When a forced boundary fires, flush all causally valid accumulated SOFT state in the same coherent transaction.

## Durability exposure trajectory

For owner-permitted deferrable dirty HOT/SOFT state, classify the affected durability scope as:

```text
NORMAL
ELEVATED
DANGER
```

This is an operability/loss-protection trajectory over still-relevant unpublished established state. It is not a durability status, corruption state, correctness HARD edge, global campaign health value, timer or scheduler.

Use only owner-valid evidence already lawfully available for the affected scope. Relevant signals may include:
- materiality/amount of still-relevant unpublished established state;
- severity of losing that state;
- increasing difficulty of later coherent durability closure;
- repeated publication/preservation failure;
- available safe low-cost preservation opportunities;
- weak age/time evidence;
- advisory host/context pressure;
- whether the next operation would materially enlarge the same exposed dirty scope.

No single signal is currentness/durability authority. Exact token/message/context limits, exact elapsed-time thresholds and empirical calibration are not defined here.

### NORMAL

Ordinary sparse persistence continues. SOFT dirty state may remain batched until an owner-defined boundary or a later exposure transition.

### ELEVATED

At the next suitable safe established-state opportunity, proactive preservation of the affected dirty scope should outrank optional Story service, planning/enrichment and other nonessential work. ELEVATED does not by itself block gameplay or create HARD.

### DANGER

At the current admitted execution opportunity, before accepting another operation that would materially enlarge the same exposed dirty scope, request **one owner-valid bounded preservation/recovery attempt**.

If that attempt remains unavailable or unsuccessful, guard that state-growing operation in the affected scope and expose the applicable owner-native/external-action disposition. Operations proven not to use or enlarge that affected dirty scope may remain available under their own owners.

DANGER alone MUST NOT:
- create `MUST_BE_DURABLE_BEFORE(edge)` as a correctness law;
- declare coherent HOT state false/corrupt;
- create rollback/rewind;
- create an exact wall-clock trigger;
- create a background scheduler/worker/heartbeat/polling loop;
- create automatic retry;
- invent an exact retry count or host-capacity threshold.

Approximate host/context pressure may contribute to exposure assessment or request conservative proactive preservation, but **cannot alone create a gameplay-affecting DANGER guard**. Such a guard additionally requires owner-valid still-relevant unpublished-state/loss-exposure evidence for the affected scope.

Successful publication clears the published dirty set and the exposure trajectory is re-evaluated from the remaining actual state; do not maintain a synthetic global durability timer/frontier merely to drive this classifier.

### No heartbeat commits

If there is **no dirty canonical/current state**, elapsed time, chat age, host pressure or exposure re-evaluation alone is not a persistence reason. The guard MUST NOT create an empty/no-op commit, timestamp-only mutation, checkpoint or other heartbeat merely to make repository activity look recent.

The invariant is protection of actual unpublished accepted state, not continuous repository activity.

### Inactive chat

This runtime does not execute in the background while the user is absent. Inactivity alone creates no timed save promise and no durability boundary.

At the next user interaction, if current-chat/environment state still retains dirty HOT/SOFT working state, evaluate the current owner-valid exposure evidence before a new operation that would materially enlarge the same scope. A long gap or approximate context pressure may be advisory evidence but cannot by itself establish gameplay-affecting DANGER.

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
- DANGER is established from owner-valid unpublished-state/loss-exposure evidence and another operation is materially enlarging that same dirty scope without the required one bounded preservation/recovery attempt or applicable guard.

A durable gameplay onboarding sequence with provisional PC and lifecycle `initializing` is valid.

## Cadence

Expected singleplayer rhythm:

```text
scaffold
    -> early PROVISIONAL_IDENTITY
    -> gameplay + rapid baseline materialization
    -> READY_PC / PLAY_READY
    -> many zero-I/O turns
    -> ordinary owner-defined boundary or risk-trajectory preservation opportunity
    -> one coherent flush when publication is required/requested
    -> many zero-I/O turns
```

Sparse persistence remains the normal rhythm. NORMAL/ELEVATED/DANGER protects exposed dirty state without introducing a fixed autosave cadence.