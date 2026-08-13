# Canonical Storage and Persistence

framework_module_version: 0.2-development
load_when: session startup, state retrieval, persistence boundary, resync, canon conflict

`main` stores shared engine/framework data plus an empty `CAMPAIGN/` skeleton. Actual campaign branches fill that skeleton with game-specific data. Chat context is temporary working memory; ChatGPT Memory is never campaign storage.

## Campaign write authorization

Before any game-state write to `campaign/*`, determine campaign creator from Git history: `author.login` of the first campaign-specific initialization commit after branch creation from an engine release. Compare it with the currently authenticated GitHub user.

- `singleplayer`: only creator may publish gameplay-state commits; other repository collaborators are read-only observers at gameplay-protocol level.
- `multiplayer`: explicitly bound participating players may publish according to multiplayer rules.
- switching `singleplayer <-> multiplayer` is creator-only.

If creator identity or current GitHub identity cannot be established reliably, do not perform an owner-only or singleplayer write.

Repository permission is necessary but not sufficient: collaborator write access does not grant authority over another user's singleplayer campaign.

## Canonical read order

Project Instructions -> Project launcher -> repository runtime bootstrap -> campaign MANIFEST -> current CORE -> latest checkpoint/hot STATE -> exact WORLD records -> bounded LOG -> current chat -> older chats as recovery evidence only.

## Stable IDs and lazy retrieval

Resolve names through compact INDEX files, fetch the exact record and only dependencies required for the current decision. Never recursively load the entity graph.

## Environment-level partitioning

Prefer separate files for independently changing state: scene, PC, NPC, location, item, faction, thread and bounded session/log records. `CAMPAIGN/STATE/CURRENT.yaml` is a compact directory of active scene refs/frontier, not a transcript. Avoid global-file writes when a local record is sufficient.

## Working set and persistence

Keep only relevant canonical records plus an internal dirty set of intended changed paths/entity IDs/scenes/processes and durable facts not yet published. Do not commit after every roll or action.

Publish a batch at natural boundaries: scene/combat/travel completion, pause/end, substantial durable bundle, explicit save, risky context/maintenance transition; in multiplayer also after completed race-sensitive shared changes that other sessions may encounter.

One persistence batch should normally be one Git commit containing all files changed by that batch.

## Concurrent HEAD change

Before publishing, compare current branch HEAD with working-set base HEAD.

If unchanged, commit normally.

If changed:
1. compare base..HEAD and identify external paths/entities;
2. if external and local dirty sets are disjoint in storage and game semantics, rebuild/apply local batch on new HEAD;
3. merge structurally independent shared-index entries;
4. if same entity/path changed, fetch latest record and semantically merge only compatible changes;
5. if logically incompatible, do not overwrite: latest canonical state becomes input to re-adjudication.

Never force-update a live campaign branch.

Git conflicts are prompts to re-read world state, not reasons to overwrite it.

## Event log and checkpoints

LOG is semantic and compact, not a transaction journal. One entry may summarize several related actions. Do not store transcripts or every die roll.

Create compact checkpoints at session boundaries, major transitions and before risky migrations/maintenance.

## Canon conflicts

Inspect the smallest relevant records/log/commit range. Repair only with evidence. Never invent a reconciliation story to hide inconsistent storage.
