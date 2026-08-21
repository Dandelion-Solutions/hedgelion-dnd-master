# Step 5 Expanded Architecture Agenda — Durability, Recovery, Multiplayer, Time, and Story Persistence

Status: **APPROVED WORKING AGENDA — NOT A CANONICAL SUBSYSTEM SPEC**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Owner direction:

- complete Step 5 architecture before Step 6;
- do not begin broad implementation planning before the remaining architecture sequence is complete;
- before entering Step 5 sub-slices, re-audit the original roadmap because it was formed early in the project and later architecture may expose missing concerns;
- explicitly include persistence/recovery of gameplay-significant runtime continuity state so a fresh runtime/chat can resume from the real durable point rather than from remembered chat context;
- do not serialize raw process/LLM memory as campaign authority;
- complete Step 5.0 and stop for review before starting Step 5.1.

This document records the expanded Step-5 decomposition discovered after Steps 1–4. It is a sequencing and investigation agenda. Each architectural slice still requires its own deep-design cycle and may refine later slices without silently advancing into them.

---

## 1. Step-5 purpose

Step 5 closes the architecture of durable continuity across:

```text
hot/shared gameplay state
    -> durability classification
    -> publication
    -> durable/recovery frontier
    -> cold recovery / new chat / restarted runtime
    -> resumed deterministic execution

parallel historical/presentation flow:

committed gameplay/history
    -> chronology evidence
    -> LOG / mechanical evidence
    -> STORY projections
    -> retention / compaction / catch-up
```

Step 5 SHALL preserve the ownership decisions from Steps 1–4 rather than create persistence-layer duplicates of them.

Central recovery invariant to investigate and formalize:

> A fresh runtime with no prior chat/model/process memory must be able to reconstruct every gameplay-significant current state, pending obligation, and resumable execution point from the last durable recovery closure. Anything not reconstructible must either be explicitly ephemeral or constitute a persistence/integrity defect.

This guarantee applies to the last successfully reached durable recovery frontier. State that existed only in volatile RAM and was destroyed before any applicable durability boundary cannot be truthfully reconstructed.

---

## 2. Fixed constraints inherited from prior steps

The Step-5 design MUST preserve unless an explicit superseding architecture decision is made:

- one long-lived durable `campaign/*` branch per campaign;
- temporary `live/*` branches only for active shared-scene concurrency;
- no long-lived spectator/public campaign branch;
- no force-push repair path;
- Git commit order is storage order, not fictional chronology;
- chronology is primarily a partial order with adaptive precision;
- current state remains owned by its domain/runtime owner, not by checkpoints, LOG, Story, or recovery indexes;
- checkpoints are sparse recovery frontiers, not alternate state snapshots;
- Temporal Agenda is a disposable derived index over owner-local temporal obligations, not scheduling authority;
- Continuation owns one suspended Resolution generation and does not copy Temporal Agenda, MechanicalContext, Procedure state, or other derived caches;
- mandatory pending child/firing obligations must have stable durable execution identity when required to survive a boundary;
- `STORY/` is non-canonical and lives in the same campaign branch;
- `STORY/{TRANSCRIPT,EVENTS,MECHANICS,NARRATIVE}` remains a read/presentation surface, not current-state authority;
- Chapters are `STORY/NARRATIVE` index groupings only;
- `runtime.disclosure` is human-player exposure authority and exact host delivery acknowledgement belongs to Step 5;
- six logical LLM roles remain semantic/context roles; physical model-call topology belongs to Step 6.

---

# 3. Expanded Step-5 slice sequence

## 5.0 — Authority / contamination audit

Purpose: inspect all current durability, recovery, runtime-continuity, multiplayer, chronology, publication, Story, transcript and cleanup concepts before later Step-5 slices are allowed to depend on them.

Required work:

- inventory every current-state, operational-state, frontier, checkpoint, cache/index, pending-work, transport and projection concept relevant to Step 5;
- map each concept to one semantic owner and lifecycle;
- distinguish authority from projection, recovery evidence, cache/index, transport metadata and historical evidence;
- identify duplicate or ambiguous writable authorities;
- identify early-project abstractions whose meaning no longer matches Steps 1–4;
- identify missing ownership where gameplay-significant state currently survives only in process/chat memory;
- remove/quarantine bad active abstractions before later slices can build on them, or explicitly assign them to a later Step-5 slice when removal cannot be correct until that slice is designed;
- produce a contamination ledger and exact carry-forward questions for 5.1+.

Exit gate:

> Step 5 has no unknown duplicate current/pending-work authority that could silently leak into later slices, and every identified inconsistency is either resolved in 5.0 or explicitly owned by a named later slice.

Do not start 5.1 before owner review of the 5.0 result.

---

## 5.1 — Frontier model

Purpose: establish the vocabulary and relationships among durable and operational frontiers before defining publication behavior.

Investigate at least:

- HOT working frontier;
- SOFT dirty frontier;
- HARD durability requirement;
- campaign durable HEAD;
- checkpoint/recovery frontier;
- active live-epoch frontier(s);
- local/global chronology frontier(s);
- Story projection frontier(s);
- transcript/history retention frontier(s);
- recovery cut across campaign + active live scopes + operational state.

Exit gate:

> For every gameplay-significant state or obligation the architecture can state where current authority lives, which frontier proves durability, and which other frontiers are derived or lagging.

---

## 5.2 — Resumable Runtime Closure

Purpose: define what gameplay-significant in-memory state must survive process/chat loss and how it is represented without persisting raw RAM or LLM context.

Classify all relevant runtime state into:

```text
AUTHORITATIVE OPERATIONAL STATE
    must survive when active

RECOVERY PROJECTION / POINTER
    may be persisted compactly to make bounded recovery possible

REBUILDABLE DERIVED STATE
    reconstructed from authorities after restart

TRULY EPHEMERAL STATE
    may disappear without gameplay-semantic loss
```

Candidate inventory to validate includes:

- world/domain state;
- runtime.command / resolution / procedure / continuation state;
- pending mandatory child descriptors;
- fixed RNG values and required RNG frontier;
- active TemporalBindings and owner-local scheduled trigger state;
- resource/LifeState delayed recovery obligations;
- ID allocation/reservation state that can affect durable identity;
- active scene/live routing;
- dirty/publication bookkeeping where necessary for a controlled handoff;
- semantic resume point / unresolved player decision when not already represented by a Continuation;
- bounded recovery references to active owners.

Explicitly rebuildable candidates include Temporal Agenda, MechanicalContext, dependency DAG caches, loaded-record caches, condition/effect aggregation indexes and Context Assembler bundles.

Exit gate:

> A cold runtime can enumerate the exact authoritative/recovery inputs required to reconstruct the last durable gameplay point without a raw memory dump or campaign-wide guesswork.

---

## 5.3 — Temporal & pending-obligation continuity

Purpose: guarantee that timers, delayed rules and other mandatory future work are neither lost nor duplicated across crash/restart boundaries.

Investigate:

- rebuilding Temporal Agenda from authoritative owner-local bindings;
- chronology evidence required to decide due/not-due/indeterminate after restart;
- lifecycle from armed obligation -> due occurrence -> pending child -> committed execution -> rearm/unarm/terminal;
- no-lost-work and no-double-work crash windows;
- pending child invocation recovery;
- suspended Resolution/Continuation recovery;
- pending Choice/Reaction recovery;
- delayed Resource/LifeState recovery;
- pending global consequences;
- fixed RNG and random-experiment continuity;
- idempotency/firing identities across restart;
- pending live compaction, Story projection and disclosure-delivery work insofar as they need durable obligation identity.

Exit gate:

> Every gameplay-significant pending obligation either reconstructs from its semantic owner or has an explicit durable pending execution identity; restart cannot silently drop it or execute it twice.

---

## 5.4 — Host lifecycle & session handoff

Purpose: model known and unexpected loss of the active runtime/chat context.

Distinguish at least:

- fresh/new chat;
- explicit session handoff;
- known context/window expiration or controlled runtime restart;
- maintenance restart;
- unexpected process/context crash;
- stale multiplayer chat;
- network/write failure during a boundary.

Investigate:

- when a known impending context destruction forces a recovery publication attempt;
- exact recoverability/RPO statement for unexpected loss;
- semantic resume point representation;
- last meaningful player/master utterance references versus durable summaries;
- prohibition on persisting hidden LLM state/raw prompt as gameplay authority;
- bootstrap behavior from only durable evidence.

Exit gate:

> The runtime has explicit semantics for controlled handoff versus unexpected crash and never promises reconstruction of unpublished lost RAM.

---

## 5.5 — SOFT / HARD / SAVE durability semantics

Purpose: define one coherent meaning of durability requirement and explicit save.

Investigate:

- exact SOFT/HARD/EPHEMERAL semantics;
- when HARD blocks further relevant execution or narration;
- complete dirty dependency closure;
- forced boundary interaction with accumulated SOFT state;
- explicit `SAVE_ALL_DIRTY` relation to ordinary durability boundaries;
- publication failure behavior;
- acknowledgement semantics;
- one-hour dirty ceiling interaction with resumable operational state;
- shared/multiplayer overrides.

Exit gate:

> There is one architecture-level definition of when established state must become durable and what completeness means.

---

## 5.6 — Campaign publication & crash consistency

Purpose: formalize the durable campaign transaction and all failure points.

Investigate:

- pinned campaign frontier;
- complete semantic dirty set;
- tree/commit/ref atomicity semantics;
- stale-head conflict handling;
- prepared but unreachable commit objects;
- retries/idempotency;
- crash between transport phases;
- relation between publication and checkpoint creation;
- promotion/ID/index closure from Step 4;
- same-batch runtime/LOG/disclosure/Story requirements versus allowed lagging projections.

Exit gate:

> Every transport failure point has an unambiguous recovery/retry path without force-push, invented canon or split authority.

---

## 5.7 — Checkpoint / recovery protocol

Purpose: define sparse recovery metadata, recovery cuts and bounded hydration.

Investigate:

- what a checkpoint identifies versus what current state owns;
- campaign + live + operational recovery cut semantics;
- active owner/reference manifests needed for bounded recovery;
- hydration and rebuild order;
- validation before resume;
- `NORMAL_RESUME`, `RECOVERY_REQUIRED`, `CANON_SUSPECT` or equivalent outcomes;
- missing/stale/corrupt references;
- checkpoint cleanup/expiry;
- compatibility with engine/runtime identity and migration boundaries.

Exit gate:

> A checkpoint/recovery frontier improves bounded exact recovery without becoming a second writable snapshot authority.

---

## 5.8 — Multiplayer / live-epoch ownership

Purpose: finalize temporary shared-scene operational authority and durable compaction.

Investigate:

- opening/adopting one epoch;
- operational entity ownership/lease scope;
- active CAS mutation;
- stale write reconciliation;
- freeze/close;
- compaction/absorption;
- rollover;
- orphan branches;
- membership changes during an epoch;
- entity transfer between live scopes;
- rare multi-scene/global-event slow path;
- recovery from abandoned/stuck epoch/compaction state;
- compatibility with Step-4 knowledge/disclosure compaction.

Exit gate:

> One mutable entity cannot have two concurrent writable authorities, and every live frontier can be recovered or safely classified as non-authoritative.

---

## 5.9 — Chronology persistence & reconciliation

Purpose: persist only temporal/causal evidence required for later correct rulings and recovery.

Investigate:

- event-local partial ordering;
- local scene frontiers;
- globally reconciled sparse frontier;
- retained quantitative elapsed evidence;
- exact/approximate time;
- cross-scene dependencies;
- simultaneous/contested actions;
- chronology interaction with live compaction and recovery;
- compaction of old chronology evidence without breaking later temporal predicates.

Exit gate:

> Fictional chronology cannot be accidentally inferred from Git commit order, and retained evidence is sufficient for every still-live temporal obligation and causal dependency.

---

## 5.10 — Story projection durability

Purpose: make Story a durable but non-canonical read model that can lag, restart and catch up safely.

Investigate:

- Story record and index publication atomicity;
- layer-local ID allocation under concurrency;
- cross-reference closure;
- dependency/reveal availability;
- projection frontiers per layer;
- lag/catch-up semantics;
- idempotent Chronicler restart;
- correction/regeneration;
- source provenance after compaction;
- guarantee that NARRATIVE failure cannot block canonical gameplay publication.

Exit gate:

> Story may lag or be regenerated/corrected without becoming gameplay authority, and a restarted Chronicler can catch up without duplicate or invented events.

---

## 5.11 — Transcript / history retention & compaction

Purpose: define exact-utterance retention independently from truth, knowledge and semantic history.

Investigate:

- which player/master/NPC utterances may be retained exactly;
- transcript boundaries and OOC/tool/system exclusions;
- multiplayer observable speech/event relationship;
- retention duration/policy;
- compaction/deletion;
- Story refs to retained/deleted transcript;
- minimum evidence that must remain when exact wording is removed;
- interaction with LOG and disclosure evidence.

Exit gate:

> Transcript retention/deletion cannot change canon, current fictional knowledge or human-player disclosure authority.

---

## 5.12 — Host delivery / disclosure boundary

Purpose: connect Step-4 NarrationResult disclosure refs to actual player-visible delivery.

Investigate:

```text
NarrationResult prepared
    -> validation
    -> host emission
    -> acknowledgement boundary
    -> runtime.disclosure persistence eligibility
```

Include:

- generation failure;
- host-emission failure;
- retry/duplicate delivery;
- interaction identity;
- shared/multiplayer observable delivery;
- distinction between emitted and literally read by the human.

Exit gate:

> HDM never records a human exposure merely because the Narrator intended to say something that did not reach the player-facing host surface.

---

## 5.13 — Garbage collection / orphan cleanup

Purpose: ensure retention cleanup cannot destroy evidence required by active state, recovery, chronology or projections.

Investigate safe-deletion dependencies for:

- checkpoints;
- superseded runtime/continuation state;
- traces/receipts/mechanical event detail;
- transcripts;
- chronology evidence;
- old live branches;
- orphan prepared commits/branches where applicable;
- Story source material.

Establish a safe compaction/deletion frontier based on actual dependency closure rather than age alone.

Exit gate:

> Deletion/compaction cannot strand an active owner, pending obligation, recovery reference, required causal relation or the only retained source promised by a durable projection.

---

## 5.14 — Full recovery & concurrency adversarial review

Purpose: attack the complete Step-5 model after individual slices converge.

Minimum scenarios:

1. long singleplayer sequence with accumulated SOFT state;
2. explicit save;
3. controlled chat/runtime handoff;
4. abrupt crash before a durability boundary;
5. crash during campaign publication;
6. crash with suspended Resolution/Continuation;
7. crash with a due scheduled trigger before/after child materialization;
8. fixed RNG generated before suspension/restart;
9. two players in independent scenes;
10. two players in one live scene;
11. live CAS conflict;
12. live epoch close/rollover/abandoned compaction;
13. entity crossing live ownership scopes;
14. global event touching multiple active scenes;
15. campaign commit order conflicting with fictional chronology;
16. cross-scene temporal dependency after independent advancement;
17. Story projection lag and Chronicler restart;
18. Story publication failure while canon publication succeeds;
19. transcript cleanup while Story/history refs exist;
20. disclosure response generation/emission/retry failure;
21. checkpoint recovery with missing/corrupt dependency;
22. stale multiplayer session after membership/authority change;
23. local entity/fact promotion forced by a durable runtime/history/knowledge dependency;
24. cleanup of obsolete artifacts without losing recovery evidence.

Final contamination sweep:

- identify every new Step-5 abstraction;
- verify whether it is authority, projection, cache, evidence or transport state;
- remove/retire any misleading abstraction before Step 6 may depend on it;
- explicitly carry all unresolved implementation obligations into Step 6/final integrated implementation program.

Exit gate:

> Publication/live-scene ownership, resumable runtime state, cross-scene recovery, chronology, Story/index publication, transcript retention, disclosure delivery and shared revision semantics form one coherent recoverable model with no unresolved Step-5 architecture blocker.

---

# 4. Step-6 boundary

Step 5 SHALL NOT decide:

- physical model-call topology for the six LLM roles;
- model selection;
- token/latency/cost budgets;
- prompt packing strategy beyond persistence/context-safety constraints already required by Step 4;
- role-call co-location/isolation implementation beyond stating durability/recovery requirements;
- full seed/catalog-gap closure or final migration program.

Those remain Step 6.

Step 5 may define durable semantic inputs needed by a future fresh Context Assembler/Narrator after restart; it must not persist hidden LLM thought/state as a shortcut.

---

# 5. Sequencing rule

Work strictly in order unless a later slice is inspected only to expose a dependency or contradiction in the active slice.

The immediate continuation point is:

**Step 5.0 — Authority / contamination audit.**

Per owner direction, complete the full 5.0 design cycle and stop for review. **Do not begin Step 5.1 until the 5.0 result has been summarized and reviewed.**
