# Causal Chronology

framework_module_version: 0.1.1
load_when: relative event order materially affects causality, knowledge, deadlines, world processes, lore chronology, cross-scene interaction, or multiplayer reconciliation

## Purpose

Chronology protects causal consistency without turning the campaign into a timestamp simulator.

Use the least precise temporal model that is sufficient for the current decision. The Master is not required to account for every minute of travel, conversation, rest, shopping, NPC movement, or scene duration when that precision cannot affect play.

The core rule is:

**Chronology must be as precise as causality requires, and no more precise.**

Independent events may remain unordered until their relative order becomes materially relevant.

## Partial ordering, not one universal clock

Treat campaign chronology primarily as a partial order of meaningful events.

Useful relations are:
- event B is caused by event A;
- event B must occur after event A even though A did not cause B;
- events A and B are independent and their relative order is currently undefined;
- exact/approximate world time is known because the fiction or rules make it relevant.

Do not invent a total ordering for unrelated scenes merely for bookkeeping.

Git commit order is storage order, not automatically fictional chronology.

## Required chronology invariants

When materially relevant:

- a cause cannot occur after its consequence;
- an entity/item/place/process must exist or be established before an event that requires it;
- information cannot be known before a valid information source/path exists;
- a state transition must follow a compatible prior state unless another canonical event explains the discontinuity;
- a process cannot advance before the trigger/resource/cause required for that advancement;
- a later historical/lore claim must not require an artifact, institution, NPC, discovery, technology, spell effect, or other fact to act before it exists;
- destruction/removal/death does not prevent later use only when a canonical restoration, replacement, mistaken belief, time displacement, or other legitimate cause explains it.

Do not manufacture causal links merely because two events happen near each other.

## Event ordering fields

Use semantic event fields only when they add real recovery/consistency value.

- `caused_by_event_ids` means genuine causal ancestry.
- `after_event_ids` means the event must occur after those events, but they are not necessarily causes.
- `world_order.scene_id` identifies the local scene/order domain when useful.
- `world_order.sequence` is an optional local ordering aid, not a mandatory campaign-global counter.
- `world_order.time` is optional. Populate it only when actual/approximate time matters to rules, fiction, deadlines, travel races, world processes, or reconciliation.

Do not timestamp every event merely because a timestamp can be invented.

## Scene and world frontiers

An active scene may keep a compact `chronology_frontier_event_id`: the latest local event that must be considered before extending that scene's chronology.

`CURRENT.world_time.frontier` is a compact globally reconciled chronology frontier, not necessarily a date/time value and not a requirement that all active scenes share one exact clock position.

The global frontier should represent only ordering that has actually become shared/global enough to constrain multiple scenes or processes. Keep it sparse.

A scene may also retain `local_time` when a useful local temporal description exists. It may be exact, approximate, narrative (`night`, `after the council`, `third day of the siege`), or null according to what the game needs.

## Adaptive precision

Increase temporal precision only when duration/order can change a decision or consequence, for example:
- a spell/effect duration;
- rest/recovery mechanics;
- a race, pursuit, interception, or rendezvous;
- a ritual/deadline/countdown;
- resource depletion tied to elapsed time;
- whether a messenger/process/event could plausibly arrive before another material event;
- synchronization of scenes that begin to affect each other.

When exact precision stops mattering, return to coarse chronology. Do not preserve unnecessary minute-by-minute bookkeeping.

Harmless narrative compression is allowed. Do not retroactively audit whether every ordinary journey or conversation consumed the physically exact number of minutes unless that discrepancy changes a material stake, cause, resource, deadline, or cross-scene interaction.

## Independent scenes

Different active scenes may advance along independent local chronologies.

For example, `A1 -> A2 -> A3` and `B1 -> B2 -> B3` need no defined ordering between A and B while they are causally independent.

When a new connection appears, establish only the ordering needed by that connection. If an event in scene B receives information created by A3, the new event must be after A3; earlier unrelated B events do not need to be globally reordered unless the new fact makes their order material.

Do not rewrite already valid independent history just to create a neat single timeline.

## Multiplayer reconciliation

In multiplayer, synchronize chronology when an action/process can cross a local scene frontier or depends on a shared/global event.

Before resolving such a dependency:
1. identify the smallest relevant scene/process/event frontiers;
2. refresh only the records required by the normal multiplayer read path;
3. establish the minimum relative ordering needed for the current action;
4. preserve already-canonical causal dependencies;
5. if two actions are fictionally simultaneous/contested, adjudicate under game rules/world logic rather than using Git commit order as the winner;
6. persist newly material cross-scene ordering when future consistency depends on it.

Do not reconcile every pair of scenes on every turn.

## Processes and delayed consequences

Off-screen processes may use approximate durations, stages, triggers, clocks, or event dependencies. Choose the representation that best preserves meaningful causality with minimal bookkeeping.

A delayed consequence may occur long after its initiating event. Preserve causal/event linkage when future reconstruction needs to know why it happened; exact elapsed time is optional unless material.

## Chronology uncertainty

It is valid for the relative order of independent events to remain `UNDEFINED` or insufficiently resolved.

If the current decision requires an order that was never established, derive the minimum compatible ordering from canonical constraints. Do not choose the ordering because one version is more dramatic or convenient.

If authoritative persisted records require an impossible chronology and the issue remains after a targeted latest-state refresh, mark the affected scope `CANON_SUSPECT` and use `INTEGRITY.md`. Do not repair it by silently changing dates/order or inventing an in-world explanation.

## Performance discipline

Chronology must stay local and cheap during ordinary play.

Do not:
- scan the full event log to prove every turn is chronological;
- build a complete total-order timeline of the campaign;
- assign timestamps to unrelated historical records for completeness;
- simulate all NPC travel continuously;
- load remote scenes merely to compare their clocks.

Use already-loaded causal references/frontiers first. Retrieve only the bounded events/records whose order can materially change the current ruling, process advancement, lore statement, or multiplayer reconciliation.
