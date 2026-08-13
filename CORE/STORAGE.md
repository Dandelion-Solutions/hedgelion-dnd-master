# Canonical Storage and Persistence

framework_module_version: 0.1.1
load_when: session startup, state retrieval, persistence boundary, resync, canon conflict

`main` stores shared engine/framework data plus an empty `CAMPAIGN/` skeleton. Actual campaign branches fill that skeleton with game-specific data. Chat context is temporary working memory; ChatGPT Memory is never campaign storage.

## Campaign write authorization

Before any game-state write to `campaign/*`, determine campaign creator from Git history: `author.login` of the first campaign-specific initialization commit after branch creation from an engine release. Compare it with the currently authenticated GitHub user.

- `singleplayer`: only creator may publish gameplay-state commits; other repository collaborators are read-only observers at gameplay-protocol level.
- `multiplayer`: explicitly bound participating players may publish according to multiplayer rules.
- switching `singleplayer <-> multiplayer` is creator-only.

If creator identity or current GitHub identity cannot be established reliably, do not perform an owner-only or singleplayer write.

Repository permission is necessary but not sufficient: collaborator write access does not grant authority over another user's singleplayer campaign.

## Authenticated player binding

For multiplayer gameplay, resolve the currently authenticated GitHub account before accepting a session/player identity. Map its stable GitHub user ID to exactly one active `PLAYER_` record, then use that record's `player_id` as the canonical player identity for the session and semantic events.

The GitHub login is only a mutable authorization/audit label. Do not use it as the actor ID in world state, logs, lore, item provenance or semantic events.

If the authenticated GitHub identity cannot be mapped to an active player binding, repository write permission alone does not authorize gameplay changes.

## Canonical read order

Project Instructions -> Project launcher -> repository runtime bootstrap -> campaign MANIFEST -> current CORE -> latest checkpoint/hot STATE -> exact WORLD records -> bounded LOG -> current chat -> older chats as recovery evidence only.

## Stable IDs and lazy retrieval

Resolve names through compact INDEX files, fetch the exact record and only dependencies required for the current decision. Never recursively load the entity graph.

## Environment-level partitioning

Prefer separate files for independently changing state: scene, PC, NPC, location, item, faction, thread and bounded session/log records. `CAMPAIGN/STATE/CURRENT.yaml` is a compact directory of active scene refs/frontier, not a transcript. Avoid global-file writes when a local record is sufficient.

## Consistency tiers

Classify gameplay information by durability:
- `HARD`: a canonical commitment whose loss would make resumed world state materially wrong or incomplete; publishing it is itself a persistence boundary and must happen after the current logical action completes;
- `SOFT`: durable state that may safely remain in the dirty working set briefly and be published at the next boundary or safety limit;
- `EPHEMERAL`: current-chat context only; it does not enter campaign storage unless later play promotes it to durable state.

Published `HARD` or `SOFT` state belongs to the GitHub canon frontier. Later chat edits, branching or omission do not erase it.

## Working set and persistence

Keep only relevant canonical records plus an internal dirty set of intended changed paths/entity IDs/scenes/processes and durable facts not yet published. Do not commit after every roll or action.

Publish a batch at natural boundaries: scene/combat/travel completion, pause/end, substantial durable bundle, explicit save, risky context/maintenance transition; in multiplayer also after completed race-sensitive shared changes that other sessions may encounter.

One persistence batch should normally be one Git commit containing all files changed by that batch.

## Causal provenance

Preserve player authorship when it is useful to explain a durable world transition, not as blanket telemetry.

A direct player-initiated semantic event records `player_intent.player_id` and the acting `pc_id` when applicable. Use the stable campaign `PLAYER_` ID, never the GitHub login or display name.

Entity records should normally point to the relevant semantic event (`last_event_id`, `established_by_event_id`, or equivalent) instead of duplicating actor labels in every changed file. Resolve a human-readable player name through the `PLAYER_` record only when presenting the history to a person.

For consequences that arise from an earlier player action, preserve the chain with `caused_by_event_ids` when the causal link matters. Do not stamp the player onto unrelated automatic consequences, NPC actions, world processes, maintenance changes, or incidental derived values merely because they were persisted in the same Git commit.

Git commit author is independent transport/audit evidence. It may corroborate who published a batch, but the canonical gameplay attribution is the bound `player_id` recorded in the semantic event.

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
