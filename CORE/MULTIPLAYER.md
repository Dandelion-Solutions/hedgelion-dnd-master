# Shared-World Multiplayer

framework_module_version: 0.1.1
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

## Synchronization policy

Do not poll HEAD before every harmless sentence or roll.

HEAD must be checked:
- before publishing a persistence batch;
- before adjudicating an action that targets a known race-sensitive shared object/process when the local HEAD may be stale;
- after an explicit resync request;
- after any Git write conflict.

## When HEAD changed

Compare external changes since the working-set base HEAD with the local dirty set.

If they are independent, incorporate the new HEAD and keep the local outcome.

If they touch the same shared file but independent data, merge structurally.

If they touch the same world entity or mutually dependent environment, fetch the latest state and evaluate logical compatibility.

Never resolve a semantic conflict by blind text merge.

## Logical conflicts

If two actions cannot both be true, already-published canon constrains the later resolution when chronology supports that ordering.

Example: a unique item is removed from a chest by one player's published action. Another player later tries to take it based on stale scene state. After resync, resolve the second action from the fact that the chest no longer contains the item; do not overwrite ownership.

If the PC can observe the consequence, narrate it naturally. Identify another character only if the PC has an in-world basis to know who acted; Git author/session metadata is DM evidence, not automatic character knowledge.

If two actions are fictionally simultaneous and commit order alone would arbitrarily decide a contested outcome, adjudicate under game rules/world timing rather than letting Git order decide the fiction.

## Publish boundaries

Private/local changes may be batched until a natural persistence boundary.

Publish race-sensitive shared changes promptly after logical completion: unique object ownership/destruction, persistent shared-location changes, shared NPC relocation/death, global process advancement, access/lock/door state, scarce shared resource consumption, etc.

This is a visibility requirement for the shared world, not a requirement to commit every turn.

## World time

Maintain chronology sufficient to determine whether actions can conflict. Separate scenes may progress independently when the campaign supports asynchronous local time, but shared/global events must reconcile against a common world-time frontier.

## Privacy

DM may load private facts required to resolve objective world state, but player-facing narration must respect PC/player knowledge boundaries.

## Joining players

Adding a player requires explicit player binding and PC assignment. Do not infer control of an existing PC.
