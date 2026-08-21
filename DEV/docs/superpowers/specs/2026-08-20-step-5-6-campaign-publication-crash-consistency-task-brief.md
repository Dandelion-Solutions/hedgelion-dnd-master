# Step 5.6 — Campaign Publication & Crash Consistency — Task Brief

Status: **RESEARCH ASSIGNMENT — ARCHITECTURAL / TECHNICAL-HEAVY**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Problem statement

Define the physical campaign-publication and crash-consistency contract that can prove or deny the logical durability promises fixed by canonical Step 5.5.

Step 5.6 owns the deterministic repository transaction boundary: derivation of a physical pending write set from an already-established Step-5.5 durability closure, coherent Git tree/commit/ref publication, optimistic concurrency, crash windows, ambiguous acknowledgement, retry/idempotency, local adoption, and preservation of authority under partial success across distinct native durability domains.

This slice does not redefine SOFT/HARD/SAVE semantics, scope-aware unpublished-exposure policy, checkpoint ownership, live-epoch ownership, chronology, Story/transcript retention, or host delivery.

## 2. Classification

**Architectural / deep-work, technical-heavy.**

The work materially concerns transactions, concurrency, consistency, persistence, crash recovery and future subsystem interfaces. Most decisions are mechanical/derivable once the owner-level repository-execution boundary below is fixed; the agent should close those details without repeatedly escalating implementation mechanics. Escalate only if analysis exposes a genuine product-semantic, authority, risk-acceptance or costly architectural trade-off not already decided.

## 3. Owner decision — repository work belongs to deterministic Python core

The owner has fixed the following architecture boundary:

> **All runtime repository/GitHub work is owned and executed by the deterministic core implemented in Python. The LLM does not perform repository publication operations directly.**

Motivation includes correctness and latency: LLM-driven repository calls are slow, can move textual files through unnecessary Base64-oriented paths, and are a poor substrate for fast deterministic coherent commits.

Canonical-candidate consequences to validate/formalize:

- Python core is the sole runtime executor of Git repository transport and mutation;
- LLM roles SHALL NOT directly create Git trees/commits, move refs, perform retry loops, construct Git transport payloads, manually Base64-encode textual repository content, or decide transport success from prose/tool-call impressions;
- repository mutation SHALL be exposed to higher layers through typed deterministic core operations, not raw GitHub tool choreography owned by an LLM role;
- core derives/validates the physical write set from established native owner state, dirty/recovery metadata and the Step-5.5 durability request/closure;
- the core performs local completeness/invariant checks before mutation;
- the core owns optimistic concurrency, exact success/ambiguity classification, retries, adoption and dirty clearing;
- text remains text at the runtime/core boundary; backend-required wire encoding is an implementation detail below that boundary;
- no runtime correctness guarantee may depend on an LLM remembering or reproducing a specific Git API call sequence.

This decision concerns runtime product architecture. The connected GitHub Connector remains the required development transport for modifying the HDM source repository during engine development; that development workflow is not the gameplay/runtime persistence architecture being designed here.

## 4. Fixed inherited constraints

Preserve unless a contradiction requires an explicit superseding owner decision:

- Step 5.1 B-NARROW domain typing and no implicit cross-domain order;
- Step 5.2 native owners remain authority and recovery closure is a compatible composition of domain-native durable sources, not a universal snapshot;
- Step 5.3 accepted execution/temporal continuity and fixed accepted RNG are not replayed merely because persistence transport fails;
- Step 5.4 successful controlled handoff requires actually durable recovery-safe closure; failed/incomplete publication cannot be falsely acknowledged as safe handoff;
- Step 5.5 EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY;
- Step 5.5 required durable source closure is distinct from pending physical write set;
- Step 5.5 explicit save protects all established dirty roots in selected save scope plus required recovery/reference/interpretation closure;
- Step 5.5 clean already-durable save may succeed with zero repository mutation;
- Step 5.5 failed explicit save does not invent gameplay rollback or hard-lock coherent local/private play;
- Step 5.5 partial publication in one native durability domain remains real authority even when the overall multi-domain save fails;
- Step 5.5 correctness-critical durability edges cannot be falsely crossed without their required durability;
- no heartbeat/no-op/timestamp-only publication;
- no force-push/live-ref rewrite to paper over a race;
- checkpoints do not become state authority merely because publication occurs;
- Story/transcript/other projections may lag according to their later owning slices unless required as recovery evidence.

## 5. Primary quality goal — maximal atomicity in one native campaign publication domain

For one logical campaign durability transaction targeting one campaign ref, the intended shape is:

```text
complete semantic durability obligation
    -> deterministic complete physical pending write set
    -> ONE tree derived from pinned base tree
    -> ONE commit with pinned parent
    -> ONE non-force authoritative ref transition
```

A single logical campaign save/boundary SHALL NOT be decomposed into product-visible per-record commits such as:

```text
PC commit
CURRENT commit
INDEX commit
LOG commit
...
```

when those records form one required coherent campaign transaction.

The design must preserve one coherent old authoritative campaign revision until one coherent new revision is atomically selected by the ref transition.

## 6. Goals

### G1 — Python persistence subsystem boundary

Define the smallest typed runtime/core interface that allows the deterministic Python core to own repository publication without making Git transport details part of LLM role responsibilities.

Investigate the separation among:

- established semantic/native owner state;
- durability request/reason/scope;
- deterministic physical publication plan;
- backend transport execution;
- transport outcome classification;
- local state adoption/dirty clearing.

Do not prematurely require a universal serialized `PublicationPlan` record if an in-process typed value is sufficient.

### G2 — Transaction freeze and deterministic input

Define the exact point at which one campaign publication pins/fixes at least:

- target repository/ref;
- authorization/write scope;
- pinned campaign HEAD;
- pinned/base tree identity;
- Step-5.5 durability roots/closure relevant to this domain;
- complete semantic dirty/new/delete set for this transaction;
- final intended textual/binary contents;
- publication reason and correctness-critical edge, if any.

No later repository mutation may add ad-hoc paths to an already-prepared transaction without invalidating/rebuilding it.

### G3 — Required source closure -> physical pending write set

Define deterministic derivation of the write set.

Already-sufficiently-durable required dependencies participate in closure proof but SHALL NOT be rewritten merely because they are dependencies.

Dirty/new/deleted native state and required companion indexes/routing/provenance enter the physical delta when necessary for the promised durable source set.

Unchanged formatting/serialization differences are not semantic dirtiness.

### G4 — Single-ref campaign atomicity

Formally establish how Git tree/commit/ref semantics provide maximal publication atomicity for a campaign ref:

- all required changed paths exist together in the prepared tree;
- no campaign authority changes when tree/commit objects are merely prepared;
- the ref remains at the old coherent commit until the authoritative ref update succeeds;
- readers observe old or new ref-selected campaign tree, not a sequence of partially published product commits.

### G5 — Exact durability success point

Determine the precise evidence required to classify publication as:

```text
CONFIRMED_SUCCESS
CONFIRMED_NOT_PUBLISHED / CONFLICT
AMBIGUOUS
FAILED_PRE_PUBLICATION
```

or a smaller equivalent closed set.

Do not infer `saved` merely because `create_tree` or `create_commit` returned successfully.

### G6 — Crash/failure window matrix

Analyze at minimum:

1. before any object preparation;
2. after tree preparation;
3. before/after pre-commit ref probe;
4. after commit creation but before ref update;
5. ref race between commit creation and non-force update;
6. transport/process failure during ref update;
7. ref update succeeded but response/ack was lost;
8. ref update succeeded but process crashed before local adoption/dirty clearing;
9. local adoption completed but later host loss occurs.

For each, state actual authority, durable state, safe retry/revalidation and possible orphan artifacts.

### G7 — Optimistic concurrency / stale-head handling

Define the campaign race protocol:

```text
pin H
prepare complete transaction against H
recheck ref
if HEAD != H:
    no stale commit publication
    invalidate snapshot
    repin current authority
    refresh only touched/dependent state
    semantically revalidate established delta
    rebuild
```

Distinguish a transport-only rebase/rebuild of an already-established compatible delta from a conflict that invalidates action dependencies and therefore requires higher-level semantic revalidation/re-resolution.

Step 5.6 must not silently decide Step-5.8 live ownership semantics.

### G8 — Prepared/unreachable Git objects

Define the authority status and cleanup implications of trees/commits created but never selected by an authoritative ref.

Unreachable/prepared objects are not gameplay authority. Their existence must not cause false acknowledgement or force-update attempts.

### G9 — Ambiguous acknowledgement

Define recovery when the core cannot tell whether the final ref transition succeeded.

The protocol must prevent both:

- false `saved` acknowledgement when publication did not occur;
- replaying/re-executing gameplay semantics merely to discover whether transport succeeded.

Targeted authoritative ref/source verification after ambiguity is allowed/expected when necessary; routine successful writes should not add redundant confirmation reads.

### G10 — Idempotent publication retry

Retries operate on established state/publication intent, not by re-running gameplay consequences.

Preserve accepted IDs, random experiments/results, execution receipts and native state unless current authoritative changes invalidate their semantic assumptions.

A retry may create a new physical tree/commit when the base HEAD changes; physical object identity need not be idempotent if semantic publication is.

### G11 — Local adoption and dirty clearing

Define when Python core may:

- adopt created commit/tree as known frontier;
- mark included state durable;
- clear/adjust dirty partitions;
- update exposure tracking;
- release a correctness-critical durability edge.

A crash after actual remote success but before local bookkeeping must recover by observing current authoritative repository state, not by pretending the write failed or applying semantic changes again.

### G12 — Multiple native durability domains

When a Step-5.5 promise spans distinct authoritative refs/domains, Step 5.6 must not invent a distributed atomic transaction.

If domain A succeeds and B fails:

- A remains real authority;
- overall composed save/handoff promise is not successful until required compatible sources hold;
- retry/recovery starts from actual current sources;
- no rollback/force rewrite of A merely to recreate an older imagined all-or-nothing cut.

Define the generic physical requirements only. Step 5.8 owns exact live/campaign authority-transfer and compaction protocol.

### G13 — Checkpoint relationship

Clarify whether an independently justified checkpoint is:

- another path in the same campaign tree transaction when it belongs to the same campaign ref and the closure requires it;
- a separate native publication when owned elsewhere;
- omitted when no checkpoint policy requires it.

Publication itself does not force checkpoint creation.

### G14 — Step-4 promotion/ID/index closure

Ensure newly established durable identities cannot be published with dangling required references/indexes/routing caused by transaction decomposition.

The physical transaction must include every dirty companion record required by semantic/recovery closure, but no unrelated records.

### G15 — Projection lag boundaries

Determine which Step-4/Step-5 outputs are part of canonical/recovery-critical same-transaction state versus independently lagging projections.

Do not automatically force noncanonical Story/transcript freshness into campaign publication; later Steps 5.10–5.12 own those guarantees.

## 7. Non-goals

Step 5.6 SHALL NOT:

- implement the Python persistence subsystem yet;
- choose detailed package/module/class names unless needed to make the architecture unambiguous;
- redefine SOFT/HARD/SAVE semantics;
- choose dirty exposure durations;
- create heartbeat/no-op publications;
- specify checkpoint schema/hydration protocol — Step 5.7;
- define live ownership/fencing/compaction in full — Step 5.8;
- use Git commit order as fictional chronology — Step 5.9;
- force Story/transcript/delivery projections synchronous without their owning contracts — Steps 5.10–5.12;
- introduce distributed transactions across independent refs;
- make Git commit messages protocol authority;
- make an LLM role repository transport authority.

## 8. Required repository evidence

Inspect at least:

- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- Step-5.5 canonical spec;
- Step-5 expanded agenda;
- Step-3 execution canonical spec where persistence failure must not replay semantics;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/RANDOMNESS.md`;
- `GAME/CORE/MULTIPLAYER.md` and `LIVE_SCENE.md` only to expose cross-domain constraints;
- access/branch model docs;
- current persistence/storage/concurrency tests/case catalogs;
- existing shipped Python runtime/tool surfaces that can own repository transport, if any.

## 9. Required analytical challenge

Explicitly challenge at least:

1. one campaign ref update vs per-record/per-module commits;
2. Python-owned repository gateway vs direct LLM/tool-driven repository calls;
3. Git object preparation vs authoritative publication;
4. preflight ref check alone vs non-force update as final race guard;
5. no confirmation reread on normal success vs targeted verification after ambiguous acknowledgement;
6. semantic idempotency vs physical commit/object idempotency;
7. automatic rebase of an established delta vs mandatory semantic revalidation after dependency overlap;
8. rollback of already-published native domain vs preserve-and-compose-after-partial-success;
9. checkpoint in same transaction vs independent/later checkpoint;
10. same-batch canonical/recovery state vs allowed lagging projections;
11. backend-neutral Python repository abstraction vs over-generalized storage layer with no current need.

## 10. Minimum failure scenario matrix

At minimum cover:

1. clean explicit save — zero writes;
2. one dirty campaign record — still one coherent tree transaction;
3. many dirty campaign records/indexes — one commit;
4. crash before tree creation;
5. tree created, process crashes;
6. ref changes before commit creation;
7. commit created, ref update loses race;
8. ref update definitely fails;
9. ref update succeeds normally;
10. ref update succeeds remotely but local response is lost;
11. ref update succeeds then process crashes before dirty clearing;
12. retry after ambiguous outcome where remote ref did advance to intended state;
13. retry after ambiguous outcome where remote ref did not advance;
14. unrelated concurrent writer changes disjoint record;
15. concurrent writer changes dependency/touched record;
16. fixed RNG result survives transport retry;
17. new entity + ID/index/reference closure publishes together;
18. explicit save includes optional checkpoint because checkpoint policy independently requires it;
19. explicit save does not create checkpoint when none required;
20. campaign publication succeeds but another required native domain fails;
21. prepared/unreachable commit remains after race;
22. empty/no-op/heartbeat attempt is rejected/no-op at core planning boundary;
23. LLM requests repository mutation directly — runtime architecture rejects/routes through Python core;
24. textual campaign state never requires an LLM-managed Base64 round trip.

## 11. Expected output chain

1. task brief;
2. repository research/evidence draft;
3. analytical challenge;
4. decision brief only if a real owner-level decision remains after analysis;
5. candidate specification;
6. adversarial review;
7. resolution gate;
8. canonical Step-5.6 specification if no unresolved owner blocker remains;
9. roadmap/status update to `Step 5.6 CLOSED / Step 5.7 NEXT, NOT STARTED`;
10. implementation obligations/debt recorded for later integrated implementation planning.

## 12. Exit gate

Step 5.6 closes when every physical publication/failure point can answer deterministically:

```text
what source/ref is authoritative now?
what state is actually durable?
may the promise/edge be acknowledged successful?
what remains dirty/unconfirmed?
what exact bounded reread/revalidation is required?
may publication retry without replaying gameplay semantics?
can an orphan/prepared object exist, and why is it non-authoritative?
why can one campaign logical save not leave split per-record canon?
```

and the design enforces:

```text
PYTHON CORE OWNS REPOSITORY TRANSPORT
ONE COHERENT CAMPAIGN REF TRANSITION PER LOGICAL CAMPAIGN TXN
NO FORCE PUSH
NO PARTIAL PER-RECORD CAMPAIGN SAVE
NO HEARTBEAT / NO-OP COMMIT
NO LLM-MANAGED GIT CHOREOGRAPHY
NO LLM-MANAGED BASE64 FOR TEXT
NO INVENTED ROLLBACK
NO DUPLICATE GAMEPLAY EXECUTION
NO FALSE SAVED ACKNOWLEDGEMENT
```
