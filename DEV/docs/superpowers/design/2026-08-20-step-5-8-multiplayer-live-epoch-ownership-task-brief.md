# Step 5.8 — Multiplayer / Live-Epoch Ownership — Architecture Task Brief

Status: **ARCHITECTURE TASK BRIEF — STEP 5.8 IN PROGRESS**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **Architectural / deep-work**

## 1. Problem statement

Steps 5.1–5.7 established domain-typed authority, resumable runtime closure, temporal continuity, host handoff, durability obligations, Python-owned campaign publication, and current-authority-first cold recovery. They intentionally left one major unresolved concurrency problem to Step 5.8:

> while temporary multiplayer live scopes exist, what exact durable contract determines which native source is the current authority for each mutable shared scope, who may publish to it, how stale writers are fenced, and how authority moves safely between campaign and live sources across crashes/recovery?

The current runtime already has a substantial `LIVE_SCENE.md` design and regression catalogue. Step 5.8 must not merely preserve that prose. It must re-derive the minimum coherent live authority protocol against the now-canonical Step-5.1–5.7 architecture and retire any assumptions that no longer hold.

The design must fit HDM's actual host model rather than a generic always-on multiplayer server.

## 2. Environment constraints that materially shape the problem

The architecture must assume:

- multiple independent ChatGPT sessions may act on the same campaign;
- no reliable process identity survives chat/runtime destruction;
- no reliable online-presence detector exists;
- no autonomous background heartbeat/polling loop is required or guaranteed;
- no trustworthy remaining-context/token/time budget is guaranteed for a dying chat;
- normal gameplay should not depend on wall-clock leases expiring correctly;
- current ordinary live synchronization is intentionally bounded to cheap ref/current-state checks;
- repository work is canonically owned by deterministic Python core through a future authenticated `RepositoryPort`; LLM roles do not own Git choreography;
- current ChatGPT deployment may require an integration bridge for Python-owned repository transport, but Step 5.8 must specify semantics independently of that physical bridge;
- repository technical permission is not gameplay authorization;
- Git storage order is not fictional chronology;
- force-push repair is forbidden.

These are constraints, not reasons to encode ChatGPT-specific process state into campaign authority.

## 3. Goals

Step 5.8 must produce a complete architecture for temporary live/shared authority such that:

1. every mutable live-relevant scope/entity has one decidable current authority source;
2. no scope can be successfully mutated through two concurrent writable authority sources;
3. several valid sessions may safely compete to publish to one authority source without electing a long-lived leader unless evidence proves leadership necessary;
4. stale or revoked writers cannot successfully publish shared mutations;
5. opening, adoption, mutation, close/freeze, compaction/absorption, rollover and recovery have explicit crash-safe state transitions;
6. current-authority-first Step-5.7 recovery can adopt/reject/continue a live source without branch-age, checkpoint-age, timestamp or conversational-memory heuristics;
7. campaign/live partial publication remains truthful under Step-5.6 multi-domain semantics;
8. already accepted gameplay/RNG/causal identity is not replayed merely because repository concurrency changed;
9. membership/controller changes fence obsolete publication authority safely;
10. entity transfer between live scopes cannot create dual ownership;
11. rare multi-scope/global transitions have a bounded safe slow path without imposing distributed transaction overhead on ordinary turns;
12. Step-4 objective truth / fictional knowledge / human disclosure ownership remains separated even if physically co-located in live storage;
13. normal hot-path synchronization remains bounded and cheap enough for ChatGPT interaction.

## 4. Non-goals

Step 5.8 SHALL NOT:

- introduce a generic distributed lock service merely because multiplayer exists;
- introduce heartbeat commits or wall-clock liveness as gameplay authority;
- require background polling;
- create a global total-order frontier/sequence across scenes;
- use Git commit order to settle fictional simultaneity;
- implement distributed transactions across campaign/live refs;
- make checkpoint a live authority/fencing owner;
- finalize chronology persistence/reconciliation owned by Step 5.9;
- finalize Story/transcript publication or host-delivery acknowledgement owned by Steps 5.10–5.12;
- finalize physical orphan/branch garbage collection owned by Step 5.13;
- implement runtime/schema/test changes during this architecture slice;
- solve Step-6 physical deployment/RepositoryPort feasibility beyond recording interface requirements exposed by live semantics.

## 5. Inherited canonical constraints

### Step 5.1

- correctness-relevant progress/revision/frontier claims are domain/scope typed;
- no implicit ordering/comparison across unrelated domains.

### Step 5.2

- current state stays in native owners;
- recovery uses bounded typed native routing;
- no universal snapshot/RecoveryCut/serialized Agenda;
- operational roots must remain recoverably enrolled while active.

### Step 5.3

- accepted execution identities, occurrence identities and fixed RNG remain owner-scoped;
- repository/recovery contention does not create duplicate temporal/gameplay execution.

### Step 5.4

- host/chat lifecycle is not gameplay authority;
- controlled handoff depends on actual durable recovery closure;
- no heartbeat is introduced to simulate host liveness.

### Step 5.5

- HARD is a named edge obligation, not an intrinsic fact class;
- shared/live write-before-reveal is correctness-critical;
- explicit save may span multiple native durable domains without one distributed transaction;
- clean state creates no heartbeat/no-op write.

### Step 5.6

- repository transport is executed by deterministic Python core;
- one campaign publication uses one complete tree/commit/non-force ref transition;
- final write safety uses optimistic authority selection, not force update;
- ambiguous publication is verified from actual authority;
- retry preserves established semantic identities unless their assumptions are invalidated;
- automatic retries are bounded;
- authorization/routing dependencies participate in conflict analysis;
- multi-domain partial success remains real and is not rolled back to simulate atomicity;
- exact campaign/live transfer ordering and fencing belong here in Step 5.8.

### Step 5.7

- ordinary cold recovery starts from current campaign authority;
- campaign authority may route a scope to a current live/native source;
- each participating mutable source is exact-revision pinned per recovery attempt;
- current native owning-scope routing selects authority;
- source movement means retry/staleness until proven corruption;
- `READY` is not a lease and never bypasses the next write's CAS/fencing;
- partial campaign/live publication is recovered from actual current sources, never checkpoint rollback;
- Step 5.8 owns practical live adoption/fencing/stabilization semantics.

## 6. Existing runtime/design surfaces to inspect

At minimum:

- `GAME/CORE/LIVE_SCENE.md`
- `GAME/CORE/MULTIPLAYER.md`
- `GAME/CORE/PERSISTENCE.md`
- `GAME/CORE/DURABILITY_GUARD.md`
- `GAME/CORE/SAVE_CONTRACT.md`
- `GAME/CORE/INTEGRITY.md`
- `GAME/CORE/SESSION.md`
- `GAME/CORE/CHRONOLOGY.md`
- `GAME/CORE/INFORMATION.md`
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md`
- `DEV/ARCHITECTURE/BRANCH_MODEL.md`
- current scene/live/player/session schemas under `GAME/SCHEMA/`
- `DEV/TESTS/LIVE_SCENE_CASES.md`
- `DEV/TESTS/MULTIPLAYER_MEMBERSHIP_CASES.md`
- `DEV/TESTS/TODO_MULTIPLAYER_LIVE_BRANCH.md`
- current Step-4 canonical information/role spec;
- canonical Step-5.2 through 5.7 specs;
- relevant catalog/runtime owner schemas where live recovery roots or Procedure/Continuation ownership cross a live boundary.

Search concrete references to:

```text
live_epoch
LIVE_STATE
base_campaign_sha
opening_live_head_sha
last_absorbed_live_head_sha
status: closed
player binding status
controlled_pc_ids
live branch
compaction
rollover
membership revocation
scene transfer
```

Do not infer absence from a single keyword miss.

## 7. Required research questions

### 7.1 Authority granularity

Determine the smallest sufficient live authority unit.

Candidates to challenge include:

- whole-scene authority only;
- scene partition plus explicit admitted/owned entity set;
- per-entity ownership claims;
- broader live transaction domain.

The result must explain how an entity referenced/used across scenes cannot be mutated concurrently through campaign and live or two live epochs.

### 7.2 Writer model

Determine whether HDM needs:

- one elected writer/leader;
- several authorized writers competing via CAS on one source;
- a lease/fencing-token model;
- or a smaller combination.

Do not introduce leader/lease merely because those concepts are common in distributed systems. Test them against the actual no-heartbeat/no-background ChatGPT host model.

### 7.3 Fencing semantics

Separate and formally relate:

```text
source authority
writer authorization
current epoch identity
expected source revision
ownership/routing generation if any
```

Determine what exact stale information causes publication rejection and which durable selector is the fence.

### 7.4 Opening/adoption

Define preparation versus authority selection when creating a live source.

Answer:

- what makes a branch/source merely prepared;
- what campaign/native routing publication makes it authoritative;
- how concurrent openers converge;
- how a cold host adopts an already-active epoch;
- how a prepared orphan is classified;
- whether deterministic branch/epoch naming remains useful or accidentally becomes authority.

### 7.5 Active mutation

Define the exact mutation protocol and authority checks for one logically resolved shared action.

Must cover:

- start/currentness probe;
- accepted dependency footprint;
- semantic result freeze;
- CAS publication;
- commit-before-reveal;
- stale conflict classification;
- disjoint transport-only replay versus semantic revalidation;
- preservation/reuse of RNG when the same experiment remains valid;
- bounded contention behavior.

### 7.6 Freeze/close semantics

Clarify whether `closed` means:

- no longer truth authority;
- no longer ordinary writable;
- both;
- or a typed intermediate state.

The model must support safe campaign/live transfer without pretending one source has vanished before its result is absorbed.

### 7.7 Compaction/absorption

Define exact authority-transfer ordering from final live source to campaign authority.

The protocol must answer all crash windows around:

```text
live active
live frozen
final live revision captured
campaign absorption prepared
campaign absorption accepted/rejected/indeterminate
campaign route cleared/changed
successor live prepared/selected
old live cleanup
```

No step may require force rollback or invented global atomicity.

### 7.8 Recovery/adoption under concurrent writers

A completely cold runtime must be able to determine:

- whether a live source is current authoritative;
- whether it is active, frozen but unabsorbed, absorbed, superseded or orphaned;
- whether gameplay may mutate it;
- whether compaction may be resumed;
- whether it must follow a successor route;
- whether current state is suspect/blocking.

Do not use branch age, commit timestamp, checkpoint age or remembered chat state.

### 7.9 Membership/controller changes

Determine fencing behavior when:

- a player leaves;
- creator revokes a player;
- a player rejoins;
- controller assignment changes;
- a late participant enters an active live scene;
- a stale chat retains old authorization data.

The design must distinguish fictional PC presence/state from human write authorization.

### 7.10 Entity transfer between live scopes

Define a safe protocol for one mutable entity moving from live authority E1 to E2, including when E2 already exists.

Challenge whether source-only freeze/compaction is sufficient or whether destination authority must participate in a boundary.

### 7.11 Rare multi-scope/global transition

Define a safe bounded slow path without making normal gameplay a distributed transaction.

The design must preserve partial chronology ownership for Step 5.9 and must not let Git write order silently adjudicate fictional simultaneity.

### 7.12 Knowledge/disclosure

Determine what live storage may physically co-locate while preserving distinct semantic owners for:

- objective truth;
- fictional character knowledge;
- human disclosure/delivery evidence.

Compaction must route each category back to its native owner without creating a live-file mega-authority.

### 7.13 Performance

Derive the minimum correctness-sensitive repository interactions for normal:

- unchanged live read;
- changed live read;
- uncontended write;
- stale write;
- close/rollover;
- cold recovery/adoption.

Do not invent a numerical latency SLO unless evidence requires an owner decision. Preserve bounded hot-path structure where possible.

## 8. Candidate solution families to challenge, not assume

The research must compare at least these conceptual families:

### A. CAS-only routed epoch

Current campaign routing selects one live source; any authorized session may write it using exact-revision CAS. Epoch lifecycle/routing changes fence old writers indirectly because writes must validate current route/epoch/revision.

Potential advantage: minimum infrastructure; natural fit for ChatGPT no-heartbeat environment.

Potential risk: one source revision CAS may not by itself fence a stale writer when authority routing changes but the old live branch remains technically writable.

### B. Routed epoch + explicit monotonic fencing generation/token

Routing selects live source plus a durable epoch/ownership generation that every mutation must present/validate.

Potential advantage: explicit stale-authority fencing across source transitions.

Potential risk: duplicate/global sequencing, extra writes/checks, unclear owner and cross-domain atomicity.

### C. Lease/leader ownership

One session/host owns temporary mutation leadership, with renewal/expiry/fencing.

Potential advantage: fewer direct multi-writer conflicts.

Potential risk: poor fit for ChatGPT lifecycle, no reliable heartbeat/background work, wall-clock dependence, takeover complexity and new failure modes.

Research may reject all three as stated and derive a smaller hybrid.

## 9. Quality attributes / fitness criteria

Rank architecture primarily by:

1. **correctness / single current writable authority**;
2. **deterministic recoverability**;
3. **stale-writer rejection**;
4. **compatibility with no-heartbeat ChatGPT lifecycle**;
5. **bounded hot-path latency/I/O**;
6. **authorization integrity**;
7. **semantic idempotency / no duplicate gameplay**;
8. **scope-local failure isolation**;
9. **testability with deterministic failure injection**;
10. **simplicity / YAGNI**;
11. **migration cost from current runtime contracts**.

Availability is important but shall not outrank correctness: if current shared authority cannot be proven, dependent shared mutation blocks rather than guessing.

## 10. Analytical challenge requirements

Before recommendation, explicitly attack:

- strongest case for keeping current `LIVE_SCENE.md` almost unchanged;
- strongest case for a durable explicit fencing generation;
- strongest case for lease/leader despite ChatGPT constraints;
- stale writer writing an old live branch after campaign route moved;
- cold recovery racing an active writer;
- close succeeds but campaign absorption never occurs;
- campaign absorption succeeds but acknowledgement is lost;
- successor preparation races old compaction;
- membership revocation racing a gameplay write;
- two live epochs claiming the same entity;
- entity transfer into an already-active destination epoch;
- multi-scene global event while one affected epoch is already closed;
- external/manual Git mutation bypassing expected runtime paths;
- missing live branch or malformed routing;
- lack of reliable per-user repository principal in some RepositoryPort implementation;
- performance degeneration caused by revalidating campaign authority on every live turn;
- whether any proposed generation/token becomes an accidental global frontier;
- whether physically co-located live state becomes duplicate semantic authority.

For each failure, identify whether the correct disposition is retry, reject, block, reconcile, resume compaction, integrity suspicion, or safe orphan classification.

## 11. Human decision gate

Do not escalate mechanical details.

Escalate only if, after research/challenge, two materially different architectures remain genuinely reasonable with a trade-off requiring owner judgment, especially:

- authority/ownership granularity that materially changes product behavior;
- accepting a lease/leader operational dependency;
- introducing a new durable fencing authority/generation with cross-system consequences;
- weakening correctness/isolation for materially lower latency;
- expanding multiplayer semantics beyond the existing simplified shared-scene model.

Before escalation, provide recommendation, alternatives, trade-offs, risks, confidence and what evidence would change the recommendation.

## 12. Expected artifacts

Deep-design chain:

1. task brief;
2. research/architecture draft;
3. analytical challenge;
4. decision brief only if material owner choice remains;
5. candidate specification;
6. adversarial review;
7. resolution gate;
8. canonical specification;
9. roadmap/status update.

No GAME/runtime implementation in Step 5.8 architecture.

## 13. Exit criteria

Step 5.8 may close only when the architecture can deterministically answer, for every relevant scope and lifecycle state:

```text
What native source is current truth authority?
Is that source currently writable for ordinary gameplay?
Which actor/principal is authorized to attempt the write?
What exact stale condition/fence makes an obsolete writer fail?
What exact revision is the CAS basis?
What happens if source/routing moves concurrently?
What happens after crash at every opening/close/absorption/successor step?
How does cold recovery adopt/reject/resume the state?
How is duplicate compaction prevented?
How is entity double ownership prevented?
How are membership/controller revocations fenced?
How are knowledge/disclosure owners preserved?
What is the bounded ordinary hot path?
```

Required final invariants:

```text
NO dual writable authority
NO stale writer successful publication
NO force-push repair
NO heartbeat/lease dependence unless owner explicitly accepts such architecture
NO branch-age/timestamp/checkpoint-age authority heuristics
NO distributed transaction in ordinary path
NO gameplay/RNG replay merely for repository contention
NO silent checkpoint rollback
NO Git-order fictional adjudication
NO live mega-owner that erases Step-4 semantic ownership
```

The final canonical spec must leave Step 5.9 with a stable live ownership/transfer substrate for chronology reconciliation.