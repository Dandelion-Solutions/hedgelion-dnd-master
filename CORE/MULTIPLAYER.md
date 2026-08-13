# Shared-World Multiplayer

framework_module_version: 0.2-development
load_when: CAMPAIGN/MANIFEST mode == multiplayer OR explicit multiplayer management

## Mode

Multiplayer is enabled/disabled only explicitly. Multiple chats/players share one campaign branch and objective world, while each PC/player has separate knowledge.

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

If they touch the same shared file but independent data (for example, separate index entries), merge structurally.

If they touch the same world entity or mutually dependent environment, fetch the latest state and evaluate logical compatibility.

Never resolve a semantic conflict by blind text merge.

## Logical conflicts

If two actions cannot both be true, already-published canon constrains the later resolution when chronology supports that ordering.

Example: ITEM_004 is unique and was in CHEST_009. Player A's published batch moves ITEM_004 to PC_A. Player B later tries to take ITEM_004 based on stale scene state. After resync, the chest no longer contains it; resolve Player B's action from that fact rather than overwriting ownership.

If the PC can observe the consequence, narrate it naturally (for example, the chest is empty). Identify the other character only if the PC has an in-world basis to know who acted; Git author/session metadata is DM evidence, not automatic character knowledge.

If two actions are fictionally simultaneous and commit order alone would arbitrarily decide a contested outcome, adjudicate the interaction under game rules/world timing rather than declaring the first Git commit the winner solely for technical reasons.

## Publish boundaries

Private/local changes may be batched until a natural persistence boundary.

Publish race-sensitive shared changes promptly after logical completion: unique object ownership/destruction, persistent shared location changes, shared NPC relocation/death, global process advancement, access/lock/door state, scarce shared resource consumption, etc.

This is a visibility requirement for the shared world, not a requirement to commit every turn.

## World time

Maintain chronology sufficient to determine whether actions can conflict. Separate scenes may progress independently when the campaign supports asynchronous local time, but shared/global events must reconcile against a common world-time frontier.

## Privacy

DM may load private facts required to resolve objective world state, but player-facing narration must respect PC/player knowledge boundaries.

## Joining players

Adding a player requires explicit player binding and PC assignment. Do not infer control of an existing PC.
