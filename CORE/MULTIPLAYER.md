# Shared-World Multiplayer

framework_module_version: 0.1.4
load_when: CAMPAIGN/MANIFEST mode == multiplayer OR explicit multiplayer management

## Mode and ownership

Multiplayer is enabled or disabled only explicitly by the campaign creator.

The creator is determined from Git history: `author.login` of the first campaign-specific initialization commit after branch creation from the engine release. Before changing mode, compare that login with the currently authenticated GitHub user. If they differ, deny the mode change.

`singleplayer` means only that creator may publish gameplay commits to the campaign branch. Other collaborators may observe/read the campaign but must not alter game state.

`multiplayer` permits explicitly bound players to publish gameplay commits according to the rules below. Multiple chats/players share one campaign branch and objective world, while each PC/player has separate knowledge.

Repository collaborator access alone is not player binding.

## Authenticated player binding

Before multiplayer gameplay writes, resolve the currently authenticated GitHub account and map its stable GitHub user ID to exactly one active `PLAYER_` record. The session `player_id` and controlled `pc_id` must come from that binding, not from self-identification in chat.

Use the stable campaign `PLAYER_` ID inside campaign state and semantic events. GitHub login is a mutable authorization/audit label only and must not be used as the gameplay actor ID.

If repository permission exists but no valid active player binding matches the authenticated GitHub user, gameplay writes are not authorized.

## Action provenance

For a durable transition directly initiated by a player, the semantic event records `player_intent.player_id` and the acting `pc_id` when applicable. This is selective causal provenance, not per-turn telemetry.

Example: if a PC takes a unique amulet from a chest, the transfer event records the stable `PLAYER_` ID and PC ID; the item record points to that event through its normal event reference. Do not copy GitHub usernames or player display names into every changed entity file.

If later consequences materially derive from that action, link them through `caused_by_event_ids`. Do not mark unrelated NPC/world/maintenance changes as player-authored merely because the same player's Git commit persisted them.

Git commit authorship is independent audit evidence for who published the batch; semantic event `player_id` is the canonical gameplay attribution.

## Reduce conflicts by structure

Keep independently changing environments in separate records. Each active scene has its own scene file and normally references one location plus the PCs/NPCs/items/processes currently relevant there. Separate players in separate scenes should usually touch different files.

Do not update a global `CURRENT` record for every local movement/action if the scene/entity record is sufficient.

## Shared-scene live frontier

When differently controlled PCs share one actionable scene, use `LIVE_SCENE.md`.

Do not let separate Masters independently improvise mutable versions of the same shared environment. The durable campaign scene opens one temporary live epoch/branch. While that pointer is active, the live state is the authoritative operational frontier for that scene's mutable state and per-PC observed information.

The framework does not depend on detecting online presence: differently controlled PCs sharing the same actionable scene are enough to require live mode.

The live branch uses one runtime-mutated file and a special fast path. Ordinary live synchronization is a live-branch ref probe; if changed, fetch only `CAMPAIGN/LIVE/LIVE_STATE.yaml`. Do not perform campaign compare/history reads for every shared-scene turn.

Campaign branch writes for live-owned scene/entity state are deferred to close-time compaction. Shared live mutations are instead published immediately to the live frontier before narration when another player could observe/use the changed fact.

## Lightweight campaign synchronization reads

Outside an active live-scene hot path, each multiplayer session keeps a cached working-set base HEAD SHA for the campaign branch.

A campaign synchronization probe must be cheap:
1. read only the active campaign branch ref;
2. if HEAD is unchanged, stop — no content or history fetch is needed;
3. if HEAD changed, use server-side `base..HEAD` compare to obtain changed paths;
4. if none of those paths can affect the session's loaded scene/entities, local dirty set, access/mode metadata, or the action being resolved, move the cached base HEAD forward without reloading files;
5. if relevant paths changed, fetch only the exact affected/required records at the new HEAD and refresh the local working set.

All files in one campaign refresh must be pinned to one exact HEAD SHA. Never assemble a shared-world view from multiple branch-relative reads that could observe different commits.

Do not clone/pull the repository or request broad commit history to synchronize ordinary multiplayer play. History is read only for a bounded provenance/conflict/audit reason.

## Synchronization policy

Do not poll the campaign HEAD before every harmless sentence or roll.

Campaign HEAD must be checked:
- before publishing a normal campaign persistence batch;
- before adjudicating an action that targets a known race-sensitive shared object/process not owned by the current live epoch when the local campaign HEAD may be stale;
- after an explicit campaign resync request;
- after any campaign write conflict;
- while opening/closing/compacting a live epoch as required by `LIVE_SCENE.md`.

An active shared scene has its own more frequent but cheaper live ref probe defined in `LIVE_SCENE.md`; do not replace that probe with a full campaign refresh.

## When campaign HEAD changed

Compare external changes since the working-set base HEAD with the local dirty set.

If they are independent, incorporate the new HEAD and keep the local outcome.

If they touch the same shared file but independent data, merge structurally.

If they touch the same world entity or mutually dependent environment, fetch the latest state and evaluate logical compatibility.

Never resolve a semantic conflict by blind text merge.

## Logical conflicts

If two actions cannot both be true, already-published canon constrains the later resolution when chronology supports that ordering.

Example: a unique item is removed from a chest by one player's published action. Another player later tries to take it based on stale local state. After resync, resolve the second action from the fact that the chest no longer contains the item; do not overwrite ownership.

If the PC can observe the consequence, narrate it naturally. Identify another character only if the PC has an in-world basis to know who acted; Git author/session metadata is DM evidence, not automatic character knowledge.

If two actions are fictionally simultaneous and commit order alone would arbitrarily decide a contested outcome, adjudicate under game rules/world timing rather than letting Git order decide the fiction.

## Publish boundaries

Private/local changes may be batched until a natural persistence boundary.

Outside a live epoch, publish race-sensitive shared changes promptly after logical completion: unique object ownership/destruction, persistent shared-location changes, shared NPC relocation/death, global process advancement, access/lock/door state, scarce shared resource consumption, etc.

Inside an active live epoch, use the live-state publication rules instead: the shared operational change is written to the live branch before narration and later compacted into one durable campaign batch.

This is a visibility requirement for the shared world, not a requirement to commit every non-shared turn.

## World chronology

Use `CHRONOLOGY.md` when relative order between scenes/events/processes materially affects a ruling or reconciliation.

Do not force all players/scenes onto one minute-by-minute clock. Separate scenes may advance along independent local chronology frontiers while they are causally independent. Their relative order may remain undefined.

Synchronize/reconcile chronology only when it becomes material, for example when:
- an event/process in one scene causes or enables something in another;
- information, an NPC, item, message, spell effect, pursuit, deadline or other state crosses scene boundaries;
- two scenes converge or participants try to meet/intercept each other;
- a global/shared process constrains both scenes;
- persisted event order would otherwise violate causality or established lore.

When reconciling, establish the minimum relative ordering necessary. Cause must precede effect; a required entity/fact must exist before use; knowledge must follow a valid source. Independent events need not receive artificial timestamps or a total order.

Git commit order is not automatically fictional chronology. If actions are genuinely simultaneous/contested, adjudicate under rules/world logic. If exact elapsed time is not a material stake, ordinary travel/scene duration may remain approximate and should not trigger minute-level accounting.

`CURRENT.world_time.frontier` represents only compact globally reconciled chronology, not a requirement that every active scene share one exact timestamp. Local scene frontiers remain local until a cross-scene dependency makes them relevant.

A cross-scene event that materially touches more than one active live epoch is an exceptional synchronization boundary; follow `LIVE_SCENE.md` and `CHRONOLOGY.md` rather than adding distributed multi-branch transaction overhead to normal play.

## Privacy

DM may load private facts required to resolve objective world state, but player-facing narration must respect PC/player knowledge boundaries.

A live scene stores objective shared truth separately from which PCs actually perceived/learned each relevant fact. Repository visibility is not character knowledge.

## Joining players

Adding a player requires explicit player binding and PC assignment. Do not infer control of an existing PC.

If a newly joined/resumed PC enters a scene with an active live epoch, load/adopt that live frontier before presenting current actionable state.
