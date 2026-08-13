# Canonical Storage and Persistence

framework_module_version: 0.2-development
load_when: session startup, state retrieval, persistence boundary, resync, canon conflict

## Roles

`main` stores shared engine/framework data plus an empty `CAMPAIGN/` skeleton. Actual campaign branches fill that skeleton with game-specific data.

Chat context is temporary working memory. ChatGPT Memory is never campaign storage.

## Canonical read order

Project Instructions -> Project launcher -> repository runtime bootstrap -> campaign MANIFEST -> current CORE -> latest checkpoint/hot STATE -> exact WORLD records -> bounded LOG -> current chat -> older chats as recovery evidence only.

## Stable IDs and lazy retrieval

Use stable entity IDs. Resolve name/reference through the relevant compact INDEX, then fetch the exact record and only dependencies required for the current decision. Never recursively load the entity graph.

## Environment-level partitioning

Prefer separate files for independently changing state:
- each active scene has its own `CAMPAIGN/STATE/SCENES/<SCENE_ID>.yaml`;
- each PC/NPC/location/item/faction/thread has its own canonical record;
- each chat/session has its own bounded session/log file when needed.

`CAMPAIGN/STATE/CURRENT.yaml` is a compact global directory of active scene refs and world frontier, not a transcript of every local action. Avoid modifying shared global files when a local entity/scene record is sufficient.

Indexes may remain shared compact routing files. Concurrent additions to an index are structurally mergeable when their entity entries are independent.

## Working set and dirty set

During play, keep in context only the relevant canonical records plus an internal dirty set:
- intended changed paths;
- affected entity IDs;
- affected scene/location/process IDs;
- durable facts/events not yet published.

Do not commit after every roll or action.

## Persistence boundaries

Publish a batch when one of these is true:
- a scene/combat/meaningful travel segment ends;
- the session pauses/ends;
- a substantial durable state bundle has accumulated;
- user explicitly asks to save/resync;
- before maintenance/context transition where unsaved state would be risky;
- in multiplayer, a completed change affects a race-sensitive shared entity/location/process that another session may interact with.

Pure narration, failed actions with no durable consequence and disposable details require no repository write.

## Commit shape

One persistence batch should normally be one Git commit containing all files changed by that batch. A batch may represent several turns/actions.

Commit messages should identify campaign/session/player when useful, for example:
`game: session S_001 player P_001 — tavern scene resolved`

This helps conflict analysis without exposing information to characters automatically.

## Concurrent HEAD change

Before publishing, compare current branch HEAD with the base HEAD of the working set.

If unchanged, commit normally.

If changed:
1. compare base..HEAD and identify external changed paths/entities;
2. if external and local dirty sets are disjoint in both storage and game semantics, rebuild/apply the local batch on the new HEAD;
3. if a shared index changed only by independent entries, merge entries;
4. if the same entity/path changed, fetch the latest record and perform semantic merge only when changes are logically compatible;
5. if logically incompatible, do not overwrite: latest canonical state becomes input to re-adjudication.

Never force-update a live campaign branch.

## Race-sensitive examples

Compatible: two players in different cities talk to different NPCs; two unrelated items move; two independent index entries are added.

Potentially mergeable: both learn different facts about the same NPC; changes affect separate relationship dimensions and do not imply contradictory chronology.

Incompatible: both take the same unique item; one destroys a door while another assumes it remains locked/intact; both move the same NPC to different places at the same time; mutually exclusive process outcomes.

In an incompatible case, the first canonical world change is respected when chronology supports it. The second action is resolved against the new state. Tell the player only what their character can perceive or infer.

## Event log

LOG is semantic and compact, not a transaction journal. One event/log entry may summarize several related actions that form one meaningful world transition. Do not store full chat transcripts or every die roll.

## Checkpoints

Create compact checkpoints at session boundaries, major transitions and before risky migrations/maintenance. They are recovery markers, not copies of the whole world.

## Canon conflicts

Inspect the smallest relevant records/log/commit range. Repair only with evidence. Never invent a reconciliation story to hide inconsistent storage.
