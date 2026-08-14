# Persistence Transport and Transaction Discipline

framework_module_version: 0.1.0
load_when: any campaign/live/storage GitHub mutation, persistence boundary, save, checkpoint publication, campaign migration
precedence: authoritative for GitHub write sequencing and campaign persistence transport

## Purpose

GitHub remains the authoritative durable campaign store, but ordinary play must run primarily from the hot in-chat working set. Persistence is a boundary operation, not a per-turn ritual.

This module defines one unambiguous write protocol so the runtime cannot create self-induced races by mixing GitHub APIs that move the same branch differently.

If older CORE text conflicts with this module about GitHub write sequencing, transaction lifetime, staging files, HEAD reuse, or campaign publication transport, this module wins.

## Three transport profiles

Choose the profile from the TARGET REF ROLE, not from convenience after individual files are discovered.

### A. CAMPAIGN_TREE_TXN — durable `campaign/*` branch

All normal durable writes to a campaign branch use one Git-database transaction shape:

`create_tree -> optimistic ref check -> create_commit -> update_ref(force=false)`

This is the default even when the final dirty set happens to contain only one campaign file. A single fixed campaign transport is preferred over saving one connector call at the cost of creating two competing write semantics.

Do not use `create_file`, `update_file`, or `delete_file` to mutate ordinary durable campaign state.

### B. LIVE_STATE_CAS — active `live/*` branch

The one-file live-epoch protocol in `LIVE_SCENE.md` is intentionally separate. It may use the Contents API / stale-blob SHA compare-and-set for the single authoritative `LIVE_STATE.yaml` file.

Do not convert ordinary live turns into campaign-tree transactions. Do not mix a live CAS write and a Git-tree write to the same live ref inside one logical live transaction.

### C. STORAGE_METADATA_SINGLE — storage default branch

Root `DND_STORAGE.yaml` initialization or baseline-version maintenance is a rare independent one-file metadata mutation and may use the Contents API.

A storage-default metadata change and a campaign migration are two distinct persistence transactions because they target different refs and have separate durable success/failure boundaries.

## Persistence transaction

A persistence transaction begins only when the runtime decides that one logical durable delta must be published now.

At transaction start freeze:
- exact repository;
- exact target ref;
- authorization identity/scope;
- `pinned_head_sha`;
- `base_tree_sha` when already known;
- complete dirty path set for this logical transition;
- final intended UTF-8 contents or deletions for those paths;
- persistence reason/boundary.

All causally related record changes belong to the same transaction. Examples include LOG + active scene + CURRENT + affected entity/index + MANIFEST only when that manifest field truly changes.

Do not publish individual files while still discovering the rest of the same logical delta.

No operation inside a campaign transaction may advance the target branch except the final `update_ref`.

## Hot known frontier

For each active campaign working set cache:
- `known_head_sha` — latest campaign HEAD proven by startup/resync/external refresh or successful own publication;
- `known_tree_sha` — tree of that known HEAD when available;
- loaded canonical records at that frontier;
- dirty in-memory record contents/deltas.

At startup it is sufficient to pin campaign HEAD. The base tree may be resolved lazily at the first persistence boundary rather than fetched on every chat startup.

After a successful own `CAMPAIGN_TREE_TXN`, the just-created commit SHA becomes `known_head_sha` and the just-created tree SHA becomes `known_tree_sha` immediately. The runtime already knows the exact contents it published, so it MUST NOT immediately refetch HEAD, SCENE, CURRENT, MANIFEST, LOG, or other unchanged records merely to confirm its own successful write.

## Campaign transaction preparation

Before connector mutation:
1. finish STATE/INTENT/RULES/RANDOMNESS/CONSEQUENCES;
2. update the in-memory working set;
3. mark all dirty durable records;
4. decide whether a persistence boundary exists;
5. collapse all causally related dirty changes for the target campaign into one final batch;
6. validate only the dirty records and direct invariants needed for that transition.

Never use remote `*.tmp`, `*_NEXT.tmp`, `staging/*`, scratch records, or create/delete staging commits to assemble a future campaign commit.

Preparation happens in model/tool working memory and directly in the `create_tree` payload.

## Normal campaign publication algorithm

Given known/pinned campaign HEAD `H`:

1. If `known_tree_sha` for `H` is absent, fetch commit metadata for `H` once to obtain its tree SHA. Cache it.
2. Create ONE tree from that base tree containing the complete dirty path delta. Use direct text content entries where supported; represent deletions in the tree operation rather than by branch-mutating file deletion calls.
3. Probe the target branch ref ONCE after the tree is prepared and immediately before creating the commit.
4. If current branch HEAD != `H`, ABORT this transaction before `create_commit`. The prepared tree object is harmless/unpublished. Enter the targeted stale-base slow path below.
5. Assert locally that the intended commit parent is exactly `H`.
6. Create ONE commit with parent `H` and the prepared tree.
7. Immediately call `update_ref` on the target campaign branch with `force=false`.
8. On success, set `known_head_sha = created_commit_sha`, `known_tree_sha = prepared_tree_sha`, clear the published dirty set, and continue from the already-known working set without post-write reads.

The ref check is deliberately placed AFTER `create_tree` but BEFORE `create_commit`: tree objects do not move the branch, and this ordering narrows the race window while avoiding a normal-path orphan commit when HEAD was already stale.

There remains an irreducible tiny race window between the final ref probe and `update_ref`. `update_ref(force=false)` is the final server-side guard.

## Stale-base slow path

If the pre-commit ref probe shows HEAD moved:
- do not call `create_commit` for the stale transaction;
- repin the new HEAD;
- compare changed paths against the transaction dirty/dependency set only when needed;
- fetch only affected canonical records;
- re-evaluate/rebase the logical delta against the new canon;
- rebuild a fresh tree and transaction from the new HEAD.

If external changes are semantically disjoint, preserve valid already-resolved consequences/random values and merge the local delta onto refreshed state. If they invalidate a premise of the action, re-adjudicate only the affected consequence under normal runtime rules.

Never force-push.

## Ref moved after commit creation

If the branch moves in the narrow interval after the pre-commit probe and `update_ref(force=false)` rejects publication:
- treat the whole transaction snapshot as invalid;
- do not continue sequential writes from the stale files;
- repin and rebuild through the targeted slow path;
- never force the prepared commit onto the branch.

The unreachable prepared commit may remain as a harmless Git object until server garbage collection. This is an exceptional external-race artifact, not the normal persistence path.

## Self-induced persistence race

A `self-induced persistence race` exists when the runtime itself advanced the same target ref after pinning a transaction and before its final `update_ref` — for example by opportunistically calling Contents API file writes or by starting another overlapping campaign transaction.

This is a runtime bug, not normal multiplayer concurrency.

Recovery is still safe: invalidate the stale transaction, adopt the new own HEAD if its contents are known, rebuild one coherent campaign transaction, never force-push. But the architecture should make this state unreachable during ordinary operation.

Within one assistant response, do not open multiple overlapping campaign transactions for causally related consequences. Combine them.

## Error invalidation

A transaction is valid only while all its inputs belong to one canonical snapshot.

After any write/conflict error that can imply stale branch/file state — non-fast-forward, stale blob, SHA mismatch, ref moved, conflict — do not keep publishing pieces of the old transaction.

Invalidate the affected transaction, repin the authoritative frontier, reread only touched/dependent records, and rebuild coherently.

A connector transport failure that provably did not mutate the ref may be retried safely only when the transaction snapshot remains valid.

## Persistence frequency

Most ordinary singleplayer live turns should perform ZERO GitHub calls.

Keep SOFT durable consequences in the dirty working set and batch them. Natural boundaries include:
- completion of a meaningful action sequence rather than each atomic exchange;
- scene transition;
- encounter/combat completion or a practical recovery boundary inside a long procedure;
- significant durable ownership/resource/thread/state change;
- canon revelation or commitment whose loss after context failure would materially damage continuity;
- explicit save;
- pause/session end;
- risky context transition/maintenance;
- dirty state becoming large or recovery-sensitive enough that continued in-memory buffering is unsafe.

Do not invent a fixed message-count autosave rule. The boundary follows durability/recovery value, not chat-turn count.

HARD commitments still publish immediately at their logical completion boundary, but `immediately` means one coherent transaction containing every causally related record — never a burst of per-file commits.

SOFT consequences may be narrated while dirty when runtime policy permits. If a HARD consequence would make the player-facing statement materially false after resume unless durable, complete its publication before asserting durable completion.

## Checkpoint discipline

A persistence transaction does NOT imply a new checkpoint.

Create/update checkpoints only when they add real recovery value: session boundary, major transition, complex mid-procedure stop, risky migration/maintenance, or another explicit recovery frontier.

Ordinary gameplay batches normally update active STATE/SCENE/LOG/entities/indexes as needed without creating a checkpoint or touching the MANIFEST checkpoint pointer.

## Round-trip performance target

Singleplayer hot path targets:
- most live turns: 0 GitHub calls;
- first campaign persistence in a chat when tree SHA is not cached: normally at most 5 calls (`fetch commit tree` + `create_tree` + `ref probe` + `create_commit` + `update_ref`);
- later campaign persistence boundaries with cached tree: normally 4 calls (`create_tree` + `ref probe` + `create_commit` + `update_ref`);
- successful own publication: 0 immediate confirmation reads.

These are performance targets, not correctness caps. A real external race, missing canon, multiplayer/live synchronization, repair, or maintenance may require the bounded slow path.

## Player-facing silence

Repository persistence is infrastructure. Do not narrate GitHub operations, commit staging, HEAD checks, retries, or save plumbing during normal play.

Mention persistence only when:
- the user explicitly asks;
- a failure blocks continuation or durable confirmation;
- a conflict can materially change canon/action resolution;
- a repair requires a player/owner decision.

A transparent technical error is preferable to pretending a failed save succeeded, but successful routine persistence should be invisible.