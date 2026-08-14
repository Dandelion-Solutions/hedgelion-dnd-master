# Canonical Storage and Persistence

framework_module_version: 0.1.4
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

When an active scene has a valid `live_epoch` pointer, `LIVE_SCENE.md` inserts the referenced live state as the authoritative operational layer for that scene between the durable campaign base and narration/adjudication.

## Stable IDs and lazy retrieval

Resolve names through compact INDEX files, fetch the exact record and only dependencies required for the current decision. Never recursively load the entity graph.

A stable campaign ID is allocated only when the DM determines that an entity/fact now needs persistent identity for future consistency. The engine must not automatically promote every incidental NPC, object, place or detail merely because it appeared in narration. The canonization/promotion decision remains a DM judgment constrained by the relevant entity module and established fiction.

Once a new global stable ID is chosen, reserving it is a `HARD` persistence boundary: publish the new canonical record and its required index entry to the applicable durable campaign frontier immediately. The ID is considered reserved only after the GitHub write succeeds. Never overwrite an already-canonical record merely to reclaim a preferred number.

If concurrent publication reveals that the chosen ID was already reserved, refresh the relevant index/state, preserve the existing canonical record, choose the next available ID in that namespace, and retry. GitHub optimistic concurrency is the uniqueness guard; no separate global allocator is required for the expected campaign scale.

Inside an active live epoch, an entity that has not yet been promoted to durable campaign identity may use an epoch-local provisional identity in live state. Do not consume a global stable ID merely for transient shared-scene bookkeeping. If the DM decides that the entity must survive beyond the live epoch or otherwise requires durable campaign identity, allocate and reserve its global stable ID through the campaign frontier before relying on that ID as durable canon; compaction then maps the provisional live identity to the reserved stable ID.

## Lightweight repository reads

Treat GitHub as a versioned current-state store during gameplay, not as a repository that must be cloned or pulled locally.

Every loaded gameplay working set has a `base_head_sha`: the exact campaign-branch HEAD from which its canonical records were read. All files fetched during one startup/refresh cycle must be pinned to the same SHA so a moving branch cannot produce a mixed-version snapshot.

For a routine campaign synchronization check:
1. fetch only the active campaign branch ref;
2. if current HEAD == `base_head_sha`, stop immediately and perform no content/history reads;
3. if HEAD changed, use GitHub's server-side compare from `base_head_sha` to current HEAD to obtain the changed path set;
4. intersect that set with loaded working-set paths/dependencies, local dirty paths, current decision dependencies, and access/mode metadata;
5. if the intersection is empty, accept current HEAD as the new base without re-reading unchanged content;
6. if relevant paths changed, fetch only those exact files/indexes that are required, pinned to current HEAD, update the working set, then advance `base_head_sha`;
7. if compare cannot be used safely, re-read only the exact records/indexes required for the current decision at current HEAD.

Never use repository clone, full `git pull`, repository archive download, recursive directory traversal, or broad commit-history retrieval as the normal gameplay synchronization path.

Git history is exceptional input. Read only the smallest bounded range needed for campaign-creator provenance, semantic conflict diagnosis, causal/audit reconstruction, or canon repair.

A branch with a long history must not become slower merely because the campaign is old; ordinary read cost should scale with relevant current-state files and relevant changes since the cached HEAD.

Active live scenes use an even cheaper one-file synchronization path from `LIVE_SCENE.md`; do not run campaign compare/history merely because the live HEAD moved.

## Environment-level partitioning

Prefer separate files for independently changing state: scene, PC, NPC, location, item, faction, thread and bounded session/log records. `CAMPAIGN/STATE/CURRENT.yaml` is a compact directory of active scene refs/frontier, not a transcript. Avoid global-file writes when a local record is sufficient.

## Operational live canon

A multiplayer live branch is a temporary canonical frontier, not a second permanent database.

While a durable scene's `live_epoch` pointer is active:
- the referenced live branch owns current mutable operational state for that scene;
- ordinary campaign writes must not independently mutate the same live-owned scene/entity state;
- successful live-state writes are canonical for the epoch even though they have not yet been compacted into normal campaign entity files;
- unrelated campaign state may continue changing normally;
- the final live state is later absorbed into one durable campaign batch.

The live branch is deliberately write-isolated to one `CAMPAIGN/LIVE/LIVE_STATE.yaml` file. Do not mirror every NPC/item file into the live branch.

## Consistency tiers

Classify gameplay information by durability:
- `HARD`: a canonical commitment whose loss would make resumed world state materially wrong or incomplete. The completion of that logical action is itself a persistence boundary; publish it to the applicable canonical frontier before continuing ordinary play.
- `SOFT`: durable state that may safely remain in the dirty working set briefly and be published at the next boundary or safety limit.
- `EPHEMERAL`: current-chat context only; do not persist unless later play promotes it to durable state.

For an active live-owned scene, a shared `HARD` commitment may be satisfied by a successful live-state publication; it does not require an immediate normal campaign commit. Durable campaign compaction occurs at the live close/boundary protocol.

Published `HARD` or `SOFT` state belongs to the applicable GitHub canon frontier. Later chat edits, branching or omission do not erase it.

## Working set and persistence

Keep only relevant canonical records plus an internal dirty set of intended changed paths/entity IDs/scenes/processes and durable facts not yet published. Do not create normal campaign commits after every roll or action.

Publish a normal campaign batch at natural boundaries: scene/combat/travel completion, pause/end, substantial durable bundle, explicit save, risky context/maintenance transition.

In multiplayer:
- outside a live epoch, race-sensitive shared changes are published promptly to the campaign frontier;
- inside a live epoch, shared operational changes use the one-file live publication protocol and are compacted later;
- do not duplicate the same state transition to both frontiers turn-by-turn.

One durable persistence batch should normally be one Git commit containing all files changed by that batch.

## Causal provenance

Preserve player authorship when it is useful to explain a durable world transition, not as blanket telemetry.

A direct player-initiated semantic event records `player_intent.player_id` and the acting `pc_id` when applicable. Use the stable campaign `PLAYER_` ID, never the GitHub login or display name.

Entity records should normally point to the relevant semantic event (`last_event_id`, `established_by_event_id`, or equivalent) instead of duplicating actor labels in every changed file. Resolve a human-readable player name through the `PLAYER_` record only when presenting the history to a person.

For consequences that arise from an earlier player action, preserve the chain with `caused_by_event_ids` when the causal link matters. Do not stamp the player onto unrelated automatic consequences, NPC actions, world processes, maintenance changes, or incidental derived values merely because they were persisted in the same Git commit.

Git commit author is independent transport/audit evidence. It may corroborate who published a batch, but the canonical gameplay attribution is the bound `player_id` recorded in the semantic event.

Live observable/pending events are compact operational records. At compaction, preserve only durable semantic provenance/knowledge that still matters; do not replay the live Git commit history into the campaign LOG.

## Concurrent campaign HEAD change

Before publishing a normal campaign batch, compare current campaign branch HEAD with working-set base HEAD.

If unchanged, commit normally.

If changed:
1. compare base..HEAD and identify external paths/entities;
2. if external and local dirty sets are disjoint in storage and game semantics, rebuild/apply local batch on new HEAD;
3. merge structurally independent shared-index entries;
4. if same entity/path changed, fetch latest record and semantically merge only compatible changes;
5. if logically incompatible, do not overwrite: latest canonical state becomes input to re-adjudication.

For live-state stale writes, do not use this multi-file campaign algorithm; use the single-file conflict protocol in `LIVE_SCENE.md`.

Never force-update a live campaign branch or multiplayer live branch.

Git conflicts are prompts to re-read world state, not reasons to overwrite it.

## Live compaction and recovery

Live compaction is a durable campaign persistence boundary.

Use the final live HEAD plus its cumulative touched entity/path set. Compare the epoch's `base_campaign_sha` to current campaign HEAD only at close to detect overlap. Disjoint external campaign changes may be preserved while applying the compacted live result on top. Relevant overlap requires targeted semantic reconciliation.

The durable scene record clears `live_epoch` and stores `last_absorbed_live_head_sha` in the same successful campaign batch that absorbs the live state. This makes compaction retry-safe: an already-absorbed live HEAD is never applied twice.

A leftover live branch after successful absorption is non-authoritative. Branch deletion/cleanup is best effort and may be deferred when the connected GitHub interface cannot delete refs.

## Event log and checkpoints

LOG is semantic and compact, not a transaction journal. One entry may summarize several related actions. Do not store transcripts or every die roll.

Create compact checkpoints at session boundaries, major transitions and before risky migrations/maintenance.

A live epoch's Git commit sequence is operational concurrency history, not campaign narrative history. Do not copy it commit-by-commit into LOG/checkpoints.

## Canon conflicts

Inspect the smallest relevant records/log/commit range. Repair only with evidence. Never invent a reconciliation story to hide inconsistent storage.

A durable pointer to a missing/invalid live epoch, impossible dual live ownership, or a live/durable disagreement that remains after latest-state refresh is `CANON_SUSPECT` and routes to `INTEGRITY.md`.
