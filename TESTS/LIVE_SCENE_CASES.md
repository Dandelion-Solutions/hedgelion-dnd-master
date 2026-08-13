# Multiplayer Live Scene Regression Cases

These cases validate the live-branch architecture. The separate manual two-player smoke-test TODO remains deferred until two independent player sessions are available.

## L01 — Deterministic concurrent opening
Two Masters at the same campaign HEAD discover that differently controlled PCs share SCENE_A and both try to open live mode.
Pass: both derive/adopt the same epoch/branch identity. Only one durable scene live pointer becomes authoritative; no parallel live epochs are created for the same scene/base.

## L02 — Unchanged live HEAD fast path
A session has cached live HEAD `L1` and parsed live state. The next world-dependent player action starts and the live branch still points to `L1`.
Pass: perform only the live ref probe; do not fetch LIVE_STATE, campaign HEAD, compare, WORLD, or history.

## L03 — Changed live HEAD fast refresh
Another player updates the scene from `L1` to `L2`.
Pass: probe the live ref, fetch only `CAMPAIGN/LIVE/LIVE_STATE.yaml` at exact `L2`, replace cache, and do not run Git compare/history.

## L04 — One logical action, one live write
A player moves, attacks, applies damage/condition, and ends in a new position as one declared/resolved action.
Pass: internal mechanics may have many steps, but the resulting shared delta is published as one LIVE_STATE replacement after logical resolution.

## L05 — Commit before shared reveal
The contents of a previously undefined interactable table become concretely established while two PCs share the scene.
Pass: establish the fact in LIVE_STATE and publish successfully before narrating the concrete interactable fact. The other Master later observes the same result.

## L06 — Presentation texture is not forced persistence
One Master describes harmless smell/noise/decoration that creates no actionable object or fact.
Pass: no live write is required merely to synchronize decorative prose.

## L07 — Audible speech knowledge propagation
PC_A says something meaningful aloud while PC_B can hear it.
Pass: store a compact observable event perceived by PC_B; do not store a transcript. PC_B's Master may use the disclosed information on next sync.

## L08 — Hidden fact remains private
A trap exists in live objective state. PC_A detects it; PC_B does not.
Pass: both Masters share the same objective trap state, but knowledge/disclosure marks only PC_A. PC_B is not told the trap exists.

## L09 — Disjoint stale write
Master A resolves a change to NPC_A while Master B concurrently changes unrelated ITEM_B and B publishes first.
Pass: A's stale write is rejected, A fetches current LIVE_STATE only, verifies the action dependency/touch set is disjoint, reapplies the already-resolved delta, preserves the existing valid random result, and retries without history/compare.

## L10 — Conflicting unique item race
Two PCs try to take the same unique item.
Pass: first successful live write fixes current ownership. The stale action refreshes and is re-resolved against the new state; ownership is never overwritten blindly.

## L11 — No reroll just because Git conflicted
A stale live write occurs but refreshed state leaves the exact same random experiment/stakes valid.
Pass: reuse the generated raw random value; do not reroll merely to resolve repository contention.

## L12 — Orphan live branch
Opening creates a live branch but the durable scene pointer is never successfully published.
Pass: the branch is not authoritative and gameplay does not use it. It may be cleaned later.

## L13 — Closing blocks new writes
An epoch is successfully changed from active to closing.
Pass: no ordinary player action is published into that epoch afterward. A session seeing closing resumes/finishes compaction or refreshes routing.

## L14 — Durable compaction is one batch
A live epoch contains many operational commits.
Pass: final scene/entity/knowledge/event results are compacted into one coherent campaign commit rather than replaying every live commit into campaign history.

## L15 — Unrelated campaign advancement during live epoch
While SCENE_A is live, another player changes only unrelated SCENE_B on the campaign branch.
Pass: at close, compare base_campaign_sha to current campaign HEAD, detect no overlap with live cumulative touch set, and compact A directly onto current campaign HEAD.

## L16 — Relevant campaign overlap is slow path
While SCENE_A is live, the durable campaign branch unexpectedly changes an entity that the live epoch also touched.
Pass: fetch only affected durable records and semantically reconcile or raise integrity suspicion; do not blind-merge or scan unrelated history.

## L17 — Idempotent compaction recovery
Campaign compaction succeeded for final live HEAD `L9`, but cleanup crashed and the live branch remains.
Pass: durable scene has `last_absorbed_live_head_sha: L9`; retry does not apply the live delta twice. The leftover branch is non-authoritative.

## L18 — Missing authoritative live branch
Durable scene points to an active live epoch whose branch/state cannot be resolved at latest repository state.
Pass: raise CANON_SUSPECT for the affected scope and invoke bounded integrity diagnosis; do not guess current scene state.

## L19 — Scene split requires ownership boundary
A live-owned NPC/item/PC must move into another concurrently active live scene.
Pass: compact/freeze the source ownership before the entity becomes mutable in the destination epoch. One entity is never actively owned by both epochs.

## L20 — Hot-state growth boundary
A very long shared scene accumulates enough semantic events/overlays that LIVE_STATE becomes too large for the desired hot path.
Pass: close and compact at a safe logical boundary, then open a fresh epoch if the shared scene continues. Do not silently discard knowledge-relevant events.

## L21 — Offline participant does not disable live mode
PC_A and PC_B are controlled by different bound players and share the scene, but only A's human is currently active.
Pass: keep/use live mode because the framework does not depend on reliable online-presence detection. B can later resume against the same live frontier.

## L22 — Cross-scene global event stays exceptional
One world event genuinely affects two active live scenes at once.
Pass: treat it as a boundary/slow path: freeze or compact affected epochs, resolve against reconciled durable state, then reopen as needed. Do not add distributed multi-branch transaction overhead to every ordinary turn.
