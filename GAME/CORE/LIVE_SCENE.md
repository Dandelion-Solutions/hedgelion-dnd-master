# Multiplayer Live Scene Runtime

framework_module_version: 0.1.2
load_when: multiplayer scene has an active live epoch OR PCs controlled by different bound players share one actionable scene

## Purpose

A live scene is a short-lived GitHub synchronization layer for multiple independent ChatGPT sessions acting in the same fictional environment.

The campaign branch remains durable long-term canon. While a live epoch is active, the live branch is the authoritative current frontier for the mutable state of that scene. At an epoch boundary, its final state is compacted into normal campaign persistence. If the shared scene continues, a fresh live epoch is opened from the newly compacted campaign state without ending the fictional scene.

The design goal is strict shared-world consistency without making ordinary turns perform repository-wide reads, Git-history analysis or multi-file merges.

## When live mode is required

Use a live epoch when one actionable scene contains PCs controlled by two or more different active campaign `PLAYER_` bindings and those PCs can independently observe or affect the same environment.

Do not rely on detecting whether both humans are currently online. If differently controlled PCs share the scene, treat the scene as concurrently addressable until they no longer share that environment.

A very large environment with genuinely independent interaction zones should be represented as separate scene records rather than one oversized live concurrency domain.

## Two canon frontiers

Outside a live epoch, the campaign branch HEAD is the current canonical frontier.

During an active live epoch:
- the campaign branch at `base_campaign_sha` supplies the durable base state;
- `CAMPAIGN/LIVE/LIVE_STATE.yaml` on the live branch supplies authoritative operational overrides and newly established live facts for the scene;
- current truth for the live-owned scope is `base campaign state + live state`;
- unrelated scenes/world records continue to use the current campaign branch normally.

Live state is not provisional narration. Once successfully published to the live branch it is canonical for that active epoch until changed causally or compacted.

## Branch and epoch identity

Use one temporary branch per live scene epoch.

Recommended branch form:
`live/<campaign-technical-id>/<scene_id>/<epoch_id>`

Derive `epoch_id` deterministically from the scene and the pinned campaign HEAD used to open the epoch, for example `E_<first-12-hex-of-base_campaign_sha>`. The scene ID already makes simultaneous epochs in different scenes distinct.

The only runtime-mutated file on a live branch is:
`CAMPAIGN/LIVE/LIVE_STATE.yaml`

Do not edit normal campaign entity files directly on the live branch. This one-file discipline is what makes live synchronization cheap.

## Opening an epoch

Opening is a boundary operation and may use several GitHub calls; do not repeat it per turn.

1. Pin the current campaign HEAD as `base_campaign_sha` and load the durable scene at that SHA.
2. If the durable scene already points to a valid active live epoch, adopt it instead of creating another.
3. Compute the deterministic epoch/branch identity.
4. Create the live branch from `base_campaign_sha` if it does not already exist.
5. Create the initial `LIVE_STATE.yaml` containing the scene identity, base SHA, participants and empty operational overlays/events.
6. Publish a normal campaign-scene update that records the live epoch pointer and its opening live HEAD.
7. Only after the campaign pointer is canonical may gameplay use that epoch as the scene frontier.

Concurrent attempts to open the same scene from the same base should converge on the same branch identity. If another session wins creation/publication, fetch and adopt its valid live state rather than creating a parallel epoch.

A branch created before the durable scene pointer is successfully published is an orphan and is not authoritative. It may be cleaned up later.

## Live state contents

Keep `LIVE_STATE.yaml` compact and scene-centric. It may contain:
- epoch identity, status, base campaign SHA and live revision;
- current participants and local time needed for the scene;
- sparse scene and entity overlays for mutable fields changed during the epoch;
- epoch-scoped newly created entities/facts not yet compacted into normal campaign files;
- per-PC knowledge/disclosure information;
- compact observable events needed so another player's Master can know what their PC saw or heard;
- pending durable semantic events/consequences for later campaign compaction;
- cumulative touched entity IDs and intended campaign paths for close-time conflict detection.

Do not store a transcript. Observable events are compact semantic facts such as an audible statement, visible action, item transfer or obvious environmental change.

Do not trim a knowledge-relevant event merely because another session has not polled recently. If the live file grows beyond a practical hot-state budget, perform an epoch rollover: close/freeze the current epoch, compact its durable result, and open a fresh epoch if the shared scene continues.

## Overlay semantics

Absent live fields inherit from `base_campaign_sha`.

A live overlay explicitly sets or removes only fields changed during the epoch. For deterministic application, use explicit field paths rather than ambiguous prose merge instructions.

If a new entity must exist before durable compaction, assign an epoch-scoped provisional ID. A provisional entity may be referenced inside the same epoch, but it must not cross into another live epoch or durable scene before compaction assigns/creates its normal canonical record.

## Entity ownership during an epoch

A mutable entity physically participating in a live scene is operationally owned by that scene's epoch for current scene-relevant state.

Do not let ordinary gameplay in another scene directly mutate the same entity through the campaign branch while it is live-owned.

One entity may not be actively owned by two live epochs at once. If an entity must cross from one live scene into another, compact/freeze the source ownership first.

A rare event that genuinely affects multiple active live scenes is a slow-path synchronization boundary: close/freeze the affected epochs, resolve the shared event against reconciled durable state, then reopen live epochs as needed. Do not build distributed multi-branch transactions into the normal turn path.

## Hot read path

Each participating session caches:
- live branch name;
- `live_head_sha`;
- current `LIVE_STATE.yaml` blob SHA;
- parsed live state.

Before an action or observation whose answer depends on the shared scene, perform exactly one cheap live-branch ref probe.

If live HEAD is unchanged:
- perform no live content read;
- perform no compare/history query;
- resolve immediately from the cached state.

If live HEAD changed:
- fetch only `CAMPAIGN/LIVE/LIVE_STATE.yaml` pinned to that exact new SHA;
- replace the cached live state/blob/head;
- do not run `base..HEAD` compare for ordinary live synchronization because the branch is one-file write-isolated.

If the refreshed live state has `status: closed`, do not publish or adjudicate a new shared-state mutation against that epoch. Perform one targeted campaign routing check for the durable scene:
- if `last_absorbed_live_head_sha` equals the final closed live HEAD and a successor `live_epoch` is present, adopt that successor and preserve all safe local conversational/working context;
- if the old HEAD is absorbed and no successor exists, use the durable campaign scene; if differently controlled PCs still share it, the normal opening protocol may create/adopt the next epoch;
- if the durable scene still points to the closed epoch and has not absorbed its final HEAD, rollover/compaction is still in progress. Do not switch early to an uncommitted campaign state.

There is no background polling requirement. A later player message whose resolution depends on the shared scene repeats the normal routing check. Pure OOC/rules discussion or another response that cannot depend on changing shared-scene state may continue without pretending that fictional time passed.

Do not probe the durable campaign branch on every live-scene turn. Query it only when the action depends on world state outside the epoch, a closed epoch requires routing, during opening/compaction, explicit resync/repair, or another existing campaign synchronization boundary.

## Hot write path

A player message may contain many internal mechanical substeps, but one logically resolved shared action produces at most one normal live-state write.

If the resolved turn does not alter shared state or another PC's usable knowledge, do not write merely because a turn occurred.

Only an `active` epoch accepts ordinary gameplay writes.

If an active epoch changes shared state, creates a new interactive fact, or creates information another PC could legitimately observe/use:
1. resolve intent, rules, randomness and consequences from the synchronized live state;
2. apply the complete logical delta to the in-memory live snapshot;
3. increment the live revision and update compact touched/event metadata;
4. replace `LIVE_STATE.yaml` once using the cached current blob SHA as the optimistic concurrency guard;
5. narrate the shared consequence only after that write succeeds.

Do not perform a second pre-write HEAD probe after the turn-start synchronization. The stale-blob/CAS write is the concurrency check.

This is the intended common mutating-turn cost: one ref probe, optional one-file refresh only if another player changed the scene, then one live-state write.

## Commit-before-reveal

A newly established interactive shared fact must be live-canonical before narration exposes it.

Example: two players can inspect the same previously undefined table. The first Master that determines a concrete interactable item records it in live state and successfully publishes before describing it. The other Master then sees the same fact on its next live sync.

Presentation-only texture that does not establish an actionable object/fact may remain local narration.

## Speech, observation and knowledge

Objective scene truth and player knowledge remain separate.

When an action/speech is perceivable by another PC and can matter to later decisions, record a compact observable event with the PCs that actually perceived it. Do not automatically disclose it to PCs who were absent, unable to perceive it, or lack the relevant knowledge channel.

A hidden trap may exist in objective live state while only PC_A has detected it. PC_B's Master uses the same objective world but must not narrate the hidden fact until PC_B legitimately learns it.

## Stale write conflict

A rejected live-state update means another session published after the cached blob.

Do not inspect Git history. Fetch the latest `LIVE_STATE.yaml` once and compare the cached and new snapshots only across the current action's dependency/touch set.

If the refreshed state is `closed`, discard any uncommitted shared consequence and follow the closed-epoch routing rule. Do not retry the gameplay write into the old epoch.

If external changes are semantically disjoint from the action:
- apply the already-resolved local delta onto the new snapshot;
- preserve the already generated random result because the action's rules/stakes did not change;
- retry the single-file write with the new blob SHA.

If external changes touch an assumption needed by the action:
- discard only the uncommitted consequence derived from stale state;
- resolve the same declared action again from the new canonical state;
- do not reroll merely because Git conflicted; reuse the existing raw random value when the same random experiment still applies;
- obtain new randomness only if the previous experiment no longer corresponds to the action under the new state or the player must choose a materially different action.

Never use an unbounded retry loop. Repeated active contention enters the explicit synchronization slow path; do not narrate an uncommitted outcome.

## Closing, compaction and rollover

Close/compact a live epoch when:
- the scene ceases to be concurrently addressable by different players;
- the scene/combat meaningfully ends;
- an entity must cross into another live concurrency domain;
- the live hot-state file becomes too large;
- a substantial durable bundle makes compaction useful;
- an explicit save/maintenance boundary requires durable consolidation;
- a cross-scene/global event requires reconciliation.

Do not close merely because one player's chat ended while differently controlled PCs still share the scene.

Do not require a fixed turn/message counter for rollover. Use a practical boundary when the live state has accumulated enough durable material or hot-state growth that a fresh epoch would improve operation.

`closed` is the only non-active live status. It means the old epoch is frozen and accepts no new ordinary gameplay writes. It does not by itself prove that durable compaction has completed. Durable absorption is proven by the campaign scene's `last_absorbed_live_head_sha` and routing pointer.

Compaction protocol:
1. synchronize the live state and replace its status `active -> closed` using an optimistic write;
2. after `closed` is canonical, accept no new ordinary actions into that epoch;
3. capture the exact final live HEAD `L`;
4. fetch current campaign HEAD `C`;
5. compare `base_campaign_sha..C` only to determine whether campaign changes overlap the cumulative entity/path set touched by the live epoch;
6. if disjoint, compact directly onto current `C`;
7. if overlapping, fetch only the affected durable records and perform semantic reconciliation; never blind-merge;
8. publish one coherent campaign persistence batch containing the durable scene/entity/event/knowledge results, clear the old scene live pointer, and set `last_absorbed_live_head_sha: L`;
9. use a human-readable commit message such as `live: compact <scene_id> <epoch_id>` or, when the shared scene will continue, `live: rollover <scene_id> <epoch_id>`. The message is audit/help text only; runtime correctness must never depend on parsing it;
10. after the campaign batch succeeds, the old live branch is non-authoritative and may be deleted/cleaned up when ref deletion is available;
11. if differently controlled PCs still share the actionable scene, immediately use the normal opening protocol from the new campaign HEAD to create/adopt a fresh live epoch. This is a technical rollover, not a fictional scene transition.

The Master performing rollover keeps its safe local conversational/working context while replacing the authoritative shared-state snapshot with the newly compacted campaign base and successor live state.

## Another Master observes `closed`

A participating Master does not periodically poll for rollover. It learns about it through the normal live ref probe before a shared-state-dependent action/observation.

When it sees `closed`:
1. cache the final closed live HEAD `L` and stop ordinary writes to that epoch;
2. perform one targeted campaign scene/HEAD routing refresh;
3. if the campaign scene has absorbed `L`, adopt any successor live epoch or, if still required and none exists yet, open/adopt one from the new campaign HEAD;
4. if `L` is not yet absorbed, do not move to an imagined intermediate state and do not adjudicate a new shared mutation from stale state.

If the player is waiting on an action that requires mutable shared state while compaction is genuinely still incomplete, the Master may give a brief neutral synchronization/save message. Do not invent night, rest, delay, NPC behavior or any other in-world event to hide repository work. OOC discussion and responses independent of the mutable shared state may continue.

The next relevant player message is a natural retry point; no autonomous timer or polling loop is required. If a closed epoch remains unabsorbed and appears abandoned/stuck rather than merely concurrent, an authorized session may resume bounded compaction using the same idempotency rules.

## Idempotency and recovery

`last_absorbed_live_head_sha` prevents duplicate compaction.

If a retry sees that the exact final closed live HEAD has already been absorbed into the durable scene, do not apply its deltas again; only finish routing/cleanup or open/adopt the successor epoch when required.

Recovery cases:
- durable scene points to an active live branch: resume from that branch;
- durable scene still points to a closed live branch whose final HEAD is not absorbed: compaction is pending; do not resume ordinary gameplay in that epoch;
- durable scene records the closed final HEAD as absorbed: the old branch is non-authoritative; adopt/open successor only if the shared scene still requires live mode;
- durable scene points to a missing/invalid live branch or invalid live state: raise `CANON_SUSPECT` and use `INTEGRITY.md`;
- live branch exists but no durable scene points to it: it is not authoritative; if its head equals `last_absorbed_live_head_sha`, it is a harmless post-compaction leftover; otherwise treat it as an orphan pending cleanup, not as gameplay truth.

Never force-push a live or campaign branch to repair concurrency.

## Performance invariants

Normal live play must never require:
- repository clone/pull/archive download;
- commit-history scan;
- broad WORLD/index traversal;
- server-side compare on every live HEAD change;
- multi-file live merges;
- campaign-branch refresh every turn.

Expected hot path:
- unchanged observation/action: one live ref probe;
- changed-by-other-player observation/action: one live ref probe + one `LIVE_STATE` fetch;
- shared mutating turn without contention: one live ref probe + one `LIVE_STATE` write, plus a fetch only when the ref showed external change;
- encountering `closed`: one live refresh plus one targeted campaign routing check, only at that rollover boundary.

Opening, compaction/rollover, repair and true cross-scene conflicts are allowed to be slower because they are boundaries, not the ordinary rhythm of play.
