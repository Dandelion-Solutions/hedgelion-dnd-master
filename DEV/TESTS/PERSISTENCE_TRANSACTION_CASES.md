# Persistence Transaction Regression Cases

These cases protect zero-I/O live play, coherent campaign transactions, optimistic concurrency, ref-role separation, base-tree preservation and formatting stability.

## PT01 — Ordinary live turn is offline from GitHub
Singleplayer working set is sufficient and no DURABILITY boundary fires. Pass: resolve/narrate with zero GitHub calls; SOFT state remains dirty.

## PT02 — Multi-record batch is one commit
Dirty logical transition touches LOG/SCENE/CURRENT/entity/index. Pass: one tree, one ref probe, one commit, one non-force ref update.

## PT03 — One dirty campaign file still uses CAMPAIGN_TREE_TXN
Pass: do not opportunistically switch to Contents API.

## PT04 — No Contents API inside campaign transaction
Pass: create/update/delete-file calls do not mutate the campaign ref.

## PT05 — No remote staging
Pass: no tmp/staging/create-then-delete artifacts or staging commits.

## PT06 — Verify after tree, before commit
Pass: prepare tree, probe ref, and create commit only if HEAD still equals pinned H.

## PT07 — External race before commit creates no stale commit
Pass: if HEAD moved, discard unpublished tree and rebuild from new frontier.

## PT08 — Narrow race after commit
Pass: update_ref(force=false) rejects stale parent; never force; repin/rebuild. Unreachable commit is acceptable exceptional artifact.

## PT09 — Conflict invalidates whole snapshot
Pass: do not continue publishing pieces from mixed frontiers.

## PT10 — Successful own publish updates known frontier
Pass: adopt created commit/tree and clear published dirty state; no confirmation reread.

## PT11 — Next live turn reuses known state
Pass: no read/write just to reconfirm successful own publication.

## PT12 — First save may lazily obtain tree
Pass: fetch pinned commit tree once when first transaction needs it, not every startup/turn.

## PT13 — Later save round-trip target
Pass target with cached tree: create_tree + ref probe + create_commit + update_ref; no post-write reads.

## PT14 — HARD is coherent, not per-file
An explicit authoritative HARD boundary changes several records. Pass: one coherent batch.

## PT15 — Many SOFT changes do not force save
Quest/NPC/item/resource/relationship state changes but no DURABILITY boundary. Pass: no commit solely by count or "importance".

## PT16 — Scene/encounter completion alone is not a singleplayer boundary
Pass: remain dirty unless focal-location/lifecycle/save/safety/other explicit guard also fires.

## PT17 — Sparse checkpoint
Ordinary save is resumable from CURRENT/SCENE/entities. Pass: no checkpoint solely because publication happened.

## PT18 — Mid-procedure stop may checkpoint
Session ends mid-combat/complex procedure. Pass: exact transient state + checkpoint allowed when recovery benefits.

## PT19 — Live epoch keeps one-file CAS
Multiplayer active live epoch. Pass: use LIVE_SCENE CAS, not campaign tree for the live-owned file.

## PT20 — No mixed live transaction
Pass: do not combine LIVE_STATE CAS and campaign-tree mutation on the same live ref in one logical transaction.

## PT21 — Storage metadata is separate
Pass: default-branch storage metadata and campaign migration are independent transactions.

## PT22 — No force push
Any mismatch. Pass: force=false; repair by repin/rebuild.

## PT23 — Existing campaign uses base tree
Pass: routine create_tree uses pinned HEAD tree as base; never from scratch.

## PT24 — Only semantic dirty paths enter delta
Pass: unrelated paths inherit exact base blobs.

## PT25 — README guide survives ordinary save byte-for-byte
Pass: README absent from delta unless overview itself is legitimately dirty.

## PT26 — Narrow README overview update preserves guide
Pass: only bytes between overview begin/end change; protected guide/outside bytes remain exact.

## PT27 — HOUSE_RULES survives unrelated save
Pass: unchanged HOUSE_RULES absent from delta.

## PT28 — YAML formatting is not dirtiness
Pass: serializer quote/array/key-order/whitespace differences alone never publish.

## PT29 — Unexpected unrelated path aborts plan
Pass: local changed-path assertion fails and tree is rebuilt before commit.

## PT30 — Blank scaffold is the from-scratch exception
Pass: exact init_campaign generator output may create first campaign tree from scratch; all later campaign writes use base-tree deltas.

## PT31 — Text payload transport avoids manual Base64
Campaign-tree, live-state CAS and storage-metadata publication handle semantically textual payloads.
Pass: use Connector UTF-8/text modes whenever available; do not manually Base64-encode/decode text for reads, writes, chunking, staging or exactness checks. Connector-internal Base64 required by an underlying API is allowed and is not a runtime failure; genuine binary content or a required operation with no usable text mode remains an exception.
