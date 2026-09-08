# Canonical Storage and Persistence

framework_module_version: 1.0.1
load_when: session startup, state retrieval, persistence boundary, resync, canon conflict

The engine package and campaign storage are separate.

- Engine/runtime/schema/rules are read only from the exact selected local `current_runtime_root`.
- Persistent campaign canon lives only in the selected GitHub campaign-storage repository.
- Chat context and extracted runtime cache are temporary working state.
- ChatGPT Memory is never campaign storage.

`PERSISTENCE.md` is authoritative for GitHub write transaction/transport semantics. This module defines what is stored, how it is retrieved, and how canonical working state is organized.

## Storage repository metadata

A campaign-storage repository is discovered by exact root `DND_STORAGE.yaml` on its default branch.

New storage uses storage-format generation 3:

```yaml
storage_format_generation: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "<version>"
    package_id: "<package id>"
    source_commit_sha: "<sha|null>"
    package_sha256: "<sha256>"
    adopted_at: "<timestamp>"
```

Marker existence is sufficient for cheap storage discovery before semantic validation; do not infer storage from repository name.

`engine.baseline` is the storage-owner-approved portable runtime identity for **NEW campaigns only**. It does not install engine bytes and never selects, overrides or mutates the runtime identity of an existing campaign.

Only the authenticated storage owner may persist changes to `DND_STORAGE.engine.baseline`.

Storage default branch does not contain or need CORE/RULES/SCHEMA/INSTALL. Engine bytes always come from validated runtime ZIPs in Project Sources/current-chat attachments and their disposable local cache.

`current_runtime_root` is an environment-specific extracted path and MUST NOT be persisted in storage metadata.

## Campaign data layout

New/current campaign branches store data directly at branch root. Root `MANIFEST.yaml` is the layout discriminator and its `storage.*` fields route STATE/INDEX/WORLD/LOG/CHECKPOINTS.

Every existing campaign chooses its runtime from `MANIFEST.engine.current`, never from storage baseline. Storage baseline is consulted only for New Game.

Resolve layout once before gameplay and use manifest roots for every read/write. New writes MUST NOT create a `CAMPAIGN/` wrapper. Local selected-runtime `CAMPAIGN/` is template source only.

## Campaign write authorization

Before game-state writes determine campaign creator from the first campaign-specific initialization commit.

- singleplayer: creator-only gameplay writes;
- multiplayer: active PLAYER binding according to multiplayer rules;
- campaign semantic engine-version adoption: campaign creator only;
- storage baseline metadata maintenance: authenticated repository-owner only.

Repository permission is necessary infrastructure but not sufficient gameplay or engine-adoption authority. Storage ownership and campaign creator authority are independent.

## Canonical read order

Project Instructions -> exact selected local runtime launcher/bootstrap -> campaign MANIFEST -> preloaded exact current CORE -> latest checkpoint/hot STATE -> exact WORLD records -> bounded LOG -> current chat -> older chats as recovery evidence only.

During an active live epoch, `LIVE_SCENE.md` inserts its operational frontier for the live-owned scope.

## Stable IDs and lazy retrieval

Resolve names/relations through compact INDEX entries and fetch exact records only when current setup/scene/decision needs them. Do not recursively traverse the world graph.

A new stable ID may be allocated/reserved in the hot working set without an immediate singleplayer commit. Before any persistence transaction publishes a durable reference to that new ID, the SAME transaction must include the new record + required index entry. Multiplayer/shared visibility may require earlier publication under its own authority.

## Hot campaign frontier cache

Each active campaign working set maintains:
- `known_head_sha`;
- `known_tree_sha` when resolved;
- the exact loaded canonical records at that known frontier;
- dirty in-memory records not yet durably published;
- only the bounded owner-valid durability-exposure evidence already needed by `DURABILITY_GUARD.md` for the affected dirty scope (for example materiality/loss exposure or observed publication failure), without a synthetic global durability timer/frontier.

Startup/resync pins HEAD. Tree SHA may be resolved lazily at first save.

A successful own campaign publication updates known HEAD/tree directly from the created commit/tree and clears the published dirty set. Do not immediately refetch records the runtime just wrote. A later sync is required only for an explicit/external/concurrency/missing-canon reason under `RUNTIME.md` and `PERSISTENCE.md`.

## Lightweight repository reads

Treat campaign GitHub as a versioned current-state store, not something to clone/pull.

When synchronization is actually required:
1. probe active campaign ref once;
2. unchanged from `known_head_sha` -> stop;
3. changed -> compare changed paths only when needed;
4. intersect with loaded/dirty/current-decision/access dependencies;
5. fetch only affected exact records pinned to the same new HEAD;
6. advance the working-set frontier.

If changed paths cannot affect current loaded/dirty/decision scope, accept the newer HEAD as frontier without rereading unrelated files; resolve its tree SHA lazily if/when persistence later requires it.

No broad archive/history/directory scan for ordinary play.

## Environment-level partitioning

Prefer separate files for independently changing scene/PC/NPC/location/item/faction/thread/session/log records. `STATE/CURRENT.yaml` is compact routing/hot state, not transcript.

## Operational live canon

Active live scenes follow `LIVE_SCENE.md`. Its single-file live CAS write path is intentionally distinct from durable campaign-tree transactions.

Do not use a temporary live file as staging for ordinary campaign commits.

## Working set and durability

`DURABILITY_GUARD.md` is authoritative for HARD/SOFT/EPHEMERAL classification, ordinary singleplayer save boundaries and the separate `NORMAL / ELEVATED / DANGER` operability/loss-protection trajectory for owner-permitted deferrable dirty state. This storage module does not invent timing, threshold or retry rules.

Keep relevant canonical records plus dirty paths/final contents in memory. Do not write GitHub files as soon as each thought/consequence is discovered. Ordinary singleplayer quest/NPC/item/resource/relationship/scene changes may remain SOFT until a guard-defined boundary or bounded preservation opportunity applies.

When a boundary requires publication, publish the complete causally valid dirty delta through `PERSISTENCE.md`; HARD never means per-file publication. When DANGER requests one bounded owner-valid preservation attempt, use the same coherent transport without promoting DANGER to HARD or creating automatic retry. Clean state never creates a heartbeat commit merely because time/chat/context signals changed.

## Concurrency

Campaign-tree transactions use optimistic non-force publication.

If the branch changed before commit creation, abort/rebase from the new frontier before creating a stale commit. If it changes in the final narrow race window, invalidate the transaction and rebuild. Never force-update campaign/live refs.

A branch movement caused by the same runtime mixing write APIs/transactions is a self-induced persistence race and must be treated as a runtime bug, not as normal multiplayer behavior.

## Event log and checkpoints

LOG is compact semantic history, not a transaction journal/transcript.

A normal gameplay persistence batch does NOT automatically create a checkpoint.
Checkpoints are sparse recovery descriptors/evidence associated with session
boundaries, major transitions, complex mid-procedure stops, risky
maintenance/migration, or another concrete recovery need. `MANIFEST.last_checkpoint_id`
is the pointer to the selected descriptor; the checkpoint does not itself become
current-state authority or a universal cross-domain frontier.

When a checkpoint is created, its `engine` block is a recovery projection of the then-current `MANIFEST.engine.current` portable runtime identity (`version`, `package_id`, `source_commit_sha`, `package_sha256`, `adopted_at`). It never stores `current_runtime_root`.

Do not touch MANIFEST checkpoint pointers when no new checkpoint is needed.

Checkpoint/entity paths are campaign-root-relative; new campaigns use root-layout paths.

## Canon conflicts

Inspect the smallest relevant records/log/commit range and repair only with evidence. Never invent a reconciliation story.