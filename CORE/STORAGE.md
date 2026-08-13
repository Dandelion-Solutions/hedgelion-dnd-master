# Canonical Storage and Persistence

framework_module_version: 0.1-development
load_when: session startup, state retrieval, any durable state change, canon conflict

## Storage roles

`main` stores shared engine/framework data only.

Each campaign branch stores game-specific data only under `CAMPAIGN/`.

Chat context is temporary working memory, not canonical storage. ChatGPT Memory is never campaign storage.

## Canonical read order

For gameplay:
1. Project Instructions / launcher constraints;
2. repository bootstrap;
3. active `CAMPAIGN/MANIFEST.yaml`;
4. current framework modules;
5. latest checkpoint pointer + hot STATE;
6. exact WORLD entity records;
7. bounded semantic LOG segments;
8. current chat;
9. older chats only as recovery evidence.

Never use a lower-priority source to silently overwrite a higher-priority canonical fact.

## Stable IDs

Every significant persistent entity/event receives a stable ID independent of display name.

Recommended prefixes:
- `PC_` player character;
- `NPC_` nonplayer character;
- `LOC_` location;
- `FAC_` faction;
- `ITEM_` significant item;
- `LORE_` stable world fact;
- `SECRET_` hidden objective fact/process;
- `EVENT_` semantic event;
- `THREAD_` active thread/process;
- `CP_` checkpoint.

IDs are never recycled after deletion/death/retirement.

## Lazy retrieval

Never scan WORLD to discover an entity if an index exists.

Lookup flow:
name/reference -> relevant INDEX -> stable ID/path -> exact record -> only dependencies required for the current decision.

Do not recursively dereference the graph. A linked entity is loaded only when it is needed.

## Hot versus cold state

`CAMPAIGN/STATE` contains only facts needed frequently now:
- current time/location/scene;
- active PCs/resources/conditions;
- active participants;
- active threads/threats/processes;
- current mode/runtime metadata.

Long-lived entity detail belongs in WORLD. Historical detail belongs in LOG. Do not duplicate full biographies/history into hot state.

## Semantic event log

LOG is append-only. A durable event record contains only what is necessary to reconstruct causality, for example:
- event ID;
- in-world time/order;
- participants/entity IDs;
- location ID;
- player/action intent when relevant;
- resolved rule/random outcome when relevant;
- factual deltas;
- causal/predecessor event links when useful;
- visibility/knowledge changes when important.

Do not store full chat transcripts as event records.

## Atomic turn persistence

A logically complete persistent game transition should be one Git commit.

Preferred transaction:
1. obtain/cached expected campaign HEAD;
2. construct all changed file contents plus new EVENT record;
3. build a Git tree based on the expected parent tree;
4. create one commit with expected HEAD as parent;
5. fast-forward campaign branch ref to the new commit;
6. only after ref update succeeds, treat the transition as durably saved and update cached HEAD.

Never force branch ref during live play.

If fast-forward fails, no stale transaction may be declared canonical. Resync and re-evaluate affected consequences.

## Materialized views

STATE, INDEX and WORLD records are materialized canonical views maintained in the same atomic commit as the semantic EVENT when they change.

The event log records why/how the world changed; materialized records represent what is true now.

## Checkpoints

A checkpoint is a compact recovery boundary, not a copy of the entire repository.

It should identify:
- checkpoint ID;
- campaign HEAD/event through which it is valid;
- current scene/time/location;
- pointers/hashes/IDs for active state;
- any migration/schema metadata required for recovery.

Create checkpoints at session boundaries, major transitions or before risky migrations, not after every trivial turn.

## Canon conflicts

If two records disagree:
1. determine authority/version/event chronology;
2. inspect the smallest relevant LOG/commit history range;
3. repair the materialized record only when evidence supports the repair;
4. persist the repair as an explicit maintenance commit/event if it changes game canon.

Never invent a reconciliation story merely to hide data inconsistency.

## Persistence threshold

Persist facts that can matter later. Avoid permanent writes for disposable prose texture.

Examples worth persisting:
- resource/HP/inventory changes;
- location/time changes that affect continuity;
- NPC relationship/knowledge/goal changes;
- discovered secrets;
- ownership/death/destruction;
- active clocks/processes;
- promises/debts/contracts;
- new significant entities;
- consequential rulings/house rules.
