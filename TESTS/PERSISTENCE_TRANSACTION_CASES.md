# Persistence Transaction Regression Cases

These cases protect low-latency gameplay, coherent campaign commits, optimistic concurrency and separation of GitHub transport profiles.

## P01 — Ordinary live turn is offline from GitHub
Singleplayer working set contains all state/rules required for an ordinary non-HARD action.
Pass: resolve/narrate with zero GitHub calls; mark any SOFT durable delta dirty in memory.

## P02 — Multi-record campaign batch is one commit
Known campaign HEAD H0/tree T0. Dirty records: LOG + SCENE + CURRENT + one entity.
Pass: one create_tree over T0 with all four final changes, one pre-commit ref probe, one create_commit(parent=H0), one update_ref(force=false). Exactly one gameplay commit.

## P03 — Campaign transport is deterministic even for one file
Only one ordinary campaign file is dirty at a real persistence boundary.
Pass: still use CAMPAIGN_TREE_TXN; do not opportunistically switch to update_file/create_file/delete_file merely because dirty_count==1.

## P04 — No Contents API inside campaign transaction
A CAMPAIGN_TREE_TXN is open.
Pass: no create_file/update_file/delete_file call targets that campaign branch before final update_ref.

## P05 — No remote staging
Runtime needs to compute replacement CURRENT/SCENE/LOG contents.
Pass: preparation is local/in-memory/create_tree payload only; no `.tmp`, `*_NEXT.tmp`, `staging/*`, create-then-delete scratch files, or staging commits appear on campaign/live refs.

## P06 — Verify after tree, before commit
H0 is pinned. Tree object is prepared.
Pass: probe target ref before create_commit. If HEAD != H0, do not create the stale commit.

## P07 — External race before commit creates no orphan commit
H0 pinned; external actor advances branch to HX before pre-commit probe.
Pass: runtime observes HX, discards unpublished prepared tree, creates no commit with parent H0, targeted-refreshes affected records, rebuilds from HX.

## P08 — Narrow race after commit
H0 passes pre-commit probe. External actor advances to HX after runtime creates C(parent=H0) but before update_ref.
Pass: update_ref(force=false) fails; runtime never forces C, invalidates transaction, repins/rebuilds. C may remain unreachable but is treated as exceptional race artifact.

## P09 — Self-race is a bug
A runtime pins H0 for a campaign transaction and then advances the same branch itself through Contents API/another overlapping transaction.
Pass: classify as self-induced persistence race/runtime bug, invalidate stale transaction, never enter a normal multiplayer merge workflow. Architecture should make this unreachable.

## P10 — Write conflict invalidates whole snapshot
Any non-fast-forward/stale blob/SHA mismatch/ref-moved conflict occurs during a transaction.
Pass: do not continue writing other pieces from mixed old/new versions; repin, reread only touched dependencies, rebuild coherently.

## P11 — Successful own publish updates known frontier
Campaign transaction publishes C1/tree T1 successfully.
Pass: set known_head_sha=C1 and known_tree_sha=T1 from own result; clear published dirty set; no immediate HEAD/SCENE/CURRENT/MANIFEST/LOG confirmation fetch.

## P12 — Next live turn reuses known state
P11 succeeded and no synchronization reason appears.
Pass: next ordinary turn performs no GitHub read/write merely to reconfirm C1.

## P13 — First save may lazily obtain tree
Startup pinned H0 but tree SHA was not fetched.
Pass: at first actual save fetch commit H0 once for base tree, then normal campaign transaction. Do not fetch tree every turn/startup without persistence need.

## P14 — Later save round-trip target
Known H1 and T1 cached, no race.
Pass target: create_tree + one ref probe + create_commit + update_ref; no post-write reads.

## P15 — HARD is coherent, not per-file
One HARD logical consequence changes resource ownership, scene state and semantic log.
Pass: publish one coherent multi-record campaign commit before claiming durable completion; never three per-file commits.

## P16 — SOFT batching
Several ordinary actions produce SOFT dirty state without a natural boundary.
Pass: no commit after each message. Publish at a later meaningful sequence/scene/encounter/save/recovery boundary or when dirty state becomes recovery-sensitive.

## P17 — Checkpoint is not every save
Ordinary gameplay batch updates SCENE + CURRENT + LOG.
Pass: no checkpoint and no MANIFEST checkpoint-pointer write unless an independent recovery rule requires one.

## P18 — Session/complex-stop checkpoint
Session ends mid-combat with detailed transient state.
Pass: persist exact resumable state coherently; checkpoint is allowed/expected because it adds recovery value.

## P19 — Live epoch keeps one-file CAS
Multiplayer active live epoch mutates only LIVE_STATE.yaml.
Pass: follow LIVE_SCENE one-file stale-blob CAS; do not replace it with campaign multi-file tree transaction.

## P20 — No mixing in live transaction
A live CAS write is being prepared.
Pass: do not also create_tree/create_commit/update_ref on that same live ref inside the same logical transaction.

## P21 — Storage baseline remains separate
Owner updates DND_STORAGE baseline and then adopts engine in a campaign.
Pass: storage marker update is one independent STORAGE_METADATA_SINGLE transaction; campaign migration is a separate CAMPAIGN_TREE_TXN. One may succeed while the other is deferred.

## P22 — Technical silence
Normal save succeeds.
Pass: player-facing narration does not describe HEAD probes, commits, staging, connector calls or retries.

## P23 — Repeated contention surfaces only when material
One bounded rebuild succeeds after a real external race.
Pass: continue without technical noise if canon/action unchanged. Repeated/conflicting contention that blocks or changes adjudication is surfaced briefly and accurately.

## P24 — No force push
Any campaign/live persistence path encounters mismatch.
Pass: force=false always; repair by repin/rebuild/reconciliation, never history rewrite.
