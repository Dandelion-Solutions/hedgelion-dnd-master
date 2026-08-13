# Shared-World Multiplayer

framework_module_version: 0.1-development
load_when: CAMPAIGN/MANIFEST mode == multiplayer OR explicit multiplayer management

## Mode switch

Campaign mode is persistent and may change only on explicit user/administrator instruction.

Never infer multiplayer merely because another PC/NPC exists.

## Shared-world model

Multiple players/chats may act in the same canonical world and campaign branch. Their characters may be geographically separated and may not know about each other's actions.

World truth is shared. Player/PC knowledge is not.

## Synchronization before a mutating turn

Before adjudicating a player action capable of changing persistent state:
1. retrieve current campaign branch HEAD;
2. compare with this chat's cached working-set HEAD;
3. if identical, continue;
4. if different, compare the commits/range and identify changed records;
5. refresh CURRENT/active state plus any affected records relevant to this action;
6. update the local working-set HEAD;
7. only then adjudicate the action.

Do not announce hidden changes the player's character has no way to know.

## Optimistic concurrency on commit

Build the state-changing turn on the synchronized HEAD and save it as one atomic commit.

Move the campaign ref only as a fast-forward from that parent. If another session commits first, the ref update must fail rather than overwrite.

On conflict:
1. retrieve new HEAD;
2. refresh affected state;
3. determine whether the player's declared intent is still possible and unchanged in meaning;
4. if it can be resolved without new player input, re-adjudicate against the new state;
5. if the world change materially invalidates/changes the player's decision, return control to the player with only the information their PC can perceive.

Never force-push to win a race.

## World time

Separate players can be at different in-world times only if the campaign explicitly supports asynchronous chronology.

Default shared-world policy: maintain a campaign world-time frontier and prevent unresolved actions from casually rewriting earlier shared events.

If one PC enters a long downtime/travel interval while another remains active, store each character's local availability/time and reconcile shared processes carefully rather than assuming all players advance identically.

## Interaction across distant players

A player's action may create consequences for another player without immediate notification.

Persist the world event and affected objective state. Update another PC's knowledge only when information reaches them through an established channel/event.

## Simultaneous conflicts

When two actions target the same scarce object, NPC, location or process, commit order matters only when actual chronology/causality permits either order.

If actions are fictionally simultaneous and commit order alone would create an arbitrary winner, resolve them under game rules using a combined contested/simultaneous adjudication before committing the resulting shared transition.

## Secrets and privacy

Do not load or disclose another player's private/PC-only information unless needed for objective world resolution.

Even when loaded for DM purposes, narration to one player must respect knowledge boundaries.

## Joining players

Adding a player requires explicit creation/binding of a PC and player visibility identity in campaign state. Do not assume that a user appearing in another chat controls an existing PC.

## Singleplayer optimization disabled

In multiplayer, never rely on the assumption that only this chat writes the branch. HEAD verification is mandatory before every persistent transition regardless of how recently this chat last wrote.
