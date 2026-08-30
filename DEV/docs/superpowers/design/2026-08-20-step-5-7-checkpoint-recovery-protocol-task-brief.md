# Step 5.7 — Checkpoint / Recovery Protocol — Task Brief

Status: **RESEARCH ASSIGNMENT — ARCHITECTURAL / DEEP-WORK**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Problem statement

Define how a completely cold HDM runtime, with no surviving prior chat/model/process memory, selects, pins, validates, hydrates and resumes from a bounded compatible composition of actual domain-native durable sources.

Step 5.7 must also determine the useful role and lifecycle of checkpoint artifacts without allowing a checkpoint, checkpoint pointer, event cursor, commit SHA, chronology value, recovery manifest or convenience cache to become duplicate current-state authority or a universal cross-domain frontier.

The investigation is intentionally solution-blind. It MAY conclude that the current checkpoint format should be substantially reduced, that checkpoint is only an optional immutable acceleration/diagnostic projection, or that some current checkpoint fields should disappear because Step-5.2 native recovery routing already owns their function.

## 2. Classification

**Architectural / deep-work.**

The slice concerns recovery, persistence, source selection, integrity, lifecycle, version compatibility and future multiplayer/live interfaces. Most detailed mechanics are agent-owned once authority semantics are established. Escalate only if analysis exposes a genuine product-semantic, authority, risk-acceptance or costly architectural trade-off not already decided.

## 3. Fixed inherited constraints

Preserve unless a contradiction requires an explicit superseding owner decision:

- Step 5.1 B-NARROW domain typing and no implicit cross-domain ordering;
- Step 5.2 Resumable Runtime Closure (RRC) is a correctness property over compatible domain-native durable sources, not a snapshot/record/frontier;
- native owners remain current-state authority;
- every independently recovery-relevant active owner must be boundedly discoverable through typed routing unless guaranteed reachable from another admitted root;
- routing is recovery evidence, not owner state;
- routing is partitionable by existing writable/semantic scope;
- mutable native sources are pinned to exact revisions per hydration attempt;
- owning-scope resolution forbids silent fallback to stale copies in another domain;
- root-enrollment durability must remain coherent with native lifecycle;
- open execution requires resolvable compatible runtime/catalog/rules interpretation;
- all armed independently-due temporal source owners remain enrolled for their armed lifetime;
- Procedure remains independently recoverable across gaps between Commands;
- fixed accepted RNG/Choice/Reaction/execution inputs are recovered from their native execution owners/evidence, not regenerated;
- Temporal Agenda, MechanicalContext, dependency DAG caches, loaded-record caches, Context Assembler bundles and similar derived state rebuild;
- lost unpublished HOT/SOFT state is never invented;
- Step 5.3 no-lost/no-double temporal continuity remains valid;
- Step 5.4 controlled handoff success requires actual durable RRC; unexpected loss recovers only actual durable sources;
- Step 5.5 SAVE success may be a compatible composition of several native durability domains and checkpoint is not mandatory for save;
- Step 5.6 campaign authority changes only at confirmed/non-force ref publication; prepared Git objects are not authority; ambiguous publication cannot be assumed successful; cold recovery must observe actual authority;
- no heartbeat/no-op publication;
- no force-push recovery;
- Story/transcript/raw model context do not become gameplay recovery authority merely because they may contain evidence.

## 4. Framing challenge

Do NOT assume any of the following are required architecture merely because current schemas/prose contain them:

- `valid_through_event_id` as a universal recovery frontier;
- `expected_commit_sha` embedded in a checkpoint;
- a checkpoint-local `world_time` value;
- `MANIFEST.last_checkpoint_id` as proof of the best/current recovery source;
- one checkpoint file containing every active root;
- one campaign-global recovery manifest;
- checkpoint creation at every save/session boundary;
- historical rollback to a checkpoint as part of ordinary cold recovery;
- one ordered list of campaign/live/operational revisions.

The design must remain able to delete, narrow, derive or defer these concepts.

## 5. Repository evidence already exposing tension

Current machine/runtime surfaces include:

- `GAME/SCHEMA/checkpoint.schema.yaml` v2 with `valid_through_event_id`, `expected_commit_sha`, `world_time`, current-state path and active PC/thread/scene lists;
- `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` matching that format;
- `GAME/SCHEMA/campaign_manifest.schema.yaml` with `last_checkpoint_id` and a statement that checkpoint payloads are immutable recovery projections;
- `GAME/CORE/STORAGE.md` and `SESSION.md` already describe checkpoints as sparse descriptors/evidence and optional at ordinary saves;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` still phrases startup order as `latest checkpoint/hot STATE` and checkpoint/STATE in canon-priority prose;
- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` proposes checkpoint export/reset operations that may need refinement once exact Step-5.7 semantics are known;
- Step 5.2 requires typed recovery routing for non-settled RuntimeCommand, active Procedure, conditionally promised unresolved Interaction/IntentPlan and independently-due temporal sources, while the current checkpoint schema does not represent that closure.

These are evidence and implementation debt candidates, not preselected solutions.

## 6. Goals

### G1 — Define the cold-recovery anchor

Determine what authoritative source is consulted first for ordinary current recovery and why.

Challenge at least:

- current campaign ref/HEAD first;
- last checkpoint first;
- checkpoint-selected historical campaign revision;
- another bounded owner-routing anchor.

The result must not introduce a universal cross-domain frontier.

### G2 — Define native source selection/composition

Specify how one recovery attempt selects exact participating source revisions across:

- campaign durable ref/domain;
- zero or more active live scopes;
- campaign-local or live-local operational routing partitions;
- native runtime owners and transitive dependencies;
- required interpretation/runtime identity.

No ordering relation may be invented between independent native domains merely because they participate in one recovery operation.

### G3 — Define the checkpoint role

Determine the minimum useful checkpoint contract.

Possible valid outcomes include checkpoint as:

- immutable sparse routing/validation projection;
- optional acceleration hint over already-sufficient native routing;
- diagnostics/maintenance recovery evidence;
- historical source evidence where exact historical references are explicitly supportable.

Checkpoint SHALL NOT become current-state authority, the only operational-root registry, or a mandatory save artifact.

### G4 — Resolve current checkpoint-field debt

Evaluate at minimum:

- `valid_through_event_id`;
- `expected_commit_sha`;
- checkpoint-local `world_time`;
- `state.current_state_path`;
- `active_pc_ids` / `active_thread_ids` / `active_scene_ids`;
- `engine` projection;
- `recovery_notes`;
- `MANIFEST.last_checkpoint_id`.

For each, classify as authoritative owner, recovery evidence/hint, redundant/debt, later-slice concern or removal candidate.

### G5 — Define bounded root discovery

Describe how a cold runtime enumerates all required Step-5.2 root classes without campaign-wide scans.

At minimum account for:

- non-settled RuntimeCommands with unfinished descendant closure;
- active Procedures independently of Command lifetime;
- promised unresolved accepted Interaction/IntentPlan where applicable;
- all armed independently-due temporal source owners;
- deterministic campaign allocator identity;
- active live ownership/routing references;
- descendants such as Resolution/Continuation/pending child evidence reachable from roots.

Checkpoint may assist but cannot be the only source of this membership.

### G6 — Define hydration order

Specify dependency-aware phases sufficient to avoid using owners before their source/revision/interpretation dependencies are proven.

At minimum consider:

1. campaign identity/layout/runtime selection;
2. current owning-scope routing;
3. exact source-revision pinning;
4. operational root loading;
5. transitive required owner/dependency loading;
6. temporal source loading;
7. fixed execution/choice/RNG evidence;
8. derived-state rebuild;
9. final closure/integrity validation;
10. resumption/adjudication release.

The exact final order may differ if analysis justifies it.

### G7 — Define staleness and supersession

Determine semantics when:

- checkpoint exists but campaign HEAD has advanced;
- checkpoint references a live epoch that has advanced/closed/been absorbed;
- current owner routing differs from checkpoint hints;
- checkpoint runtime identity differs from current MANIFEST identity;
- checkpoint pointer itself is stale or absent.

An old checkpoint must not cause silent rollback of valid newer authority.

### G8 — Define failure/outcome taxonomy

Produce a small typed recovery outcome model that does not conflate:

- healthy current resume;
- unavailable but not known-corrupt required source;
- incompatible runtime/interpretation prerequisite;
- stale/optional checkpoint evidence;
- persisted integrity suspicion;
- confirmed corruption;
- unresolved Step-5.6 publication ambiguity where actual authority cannot yet be observed.

Reuse `INTEGRITY.md` `CANON_SUSPECT/CANON_CORRUPT` ownership rather than duplicating it when possible.

### G9 — Define Step-5.6 interaction

For restart after:

- confirmed campaign publication;
- remote publication success followed by local crash before bookkeeping;
- lost/ambiguous ref acknowledgement;
- partial success across independent durability domains;

state what cold recovery observes and how actual source authority supersedes stale local bookkeeping.

Recovery SHALL NOT replay gameplay merely to discover persistence outcome.

### G10 — Define checkpoint lifecycle

Determine:

- when checkpoint creation is independently justified;
- immutability expectations;
- pointer update atomicity;
- whether old checkpoints remain valid historical evidence or only stale hints;
- retention/expiry eligibility;
- what Step 5.13 must later own for physical GC/orphan cleanup.

No checkpoint refresh/heartbeat merely to update freshness.

### G11 — Define historical rollback boundary

Separate ordinary cold recovery from explicit maintenance rollback/debugging.

Determine whether exact historical checkpoint reset is:

- guaranteed by the checkpoint contract;
- supported only when exact historical native revisions remain resolvable;
- a maintenance-only best-effort capability;
- or outside current architecture.

Do not distort ordinary recovery around a support/debug command unless the product actually requires it.

### G12 — Preserve future 5.8 ownership

5.7 may define generic source-selection requirements for active live scopes but SHALL NOT finalize live epoch opening, fencing, CAS mutation, close/absorb/rollover or authority-transfer order. Step 5.8 owns those semantics.

### G13 — Preserve performance/boundedness

Normal cold recovery may perform several reads, but it must be bounded by typed roots/dependencies and must not require:

- repository clone/pull;
- campaign-wide WORLD traversal;
- broad Git-history scan;
- transcript/Story reconstruction;
- scanning every checkpoint to find a maximum;
- loading all engine versions;
- global comparison of incomparable native revisions.

## 7. Quality attributes

Priority order for this slice:

1. correctness / no invented canon;
2. unambiguous authority ownership;
3. deterministic bounded recovery;
4. crash/retry integrity;
5. source compatibility/version safety;
6. testability/diagnosability;
7. bounded I/O and startup latency;
8. minimal persistent metadata / YAGNI;
9. compatibility with later multiplayer/live and GC design.

No numerical latency target is established by architecture.

## 8. Non-goals

Step 5.7 SHALL NOT:

- implement the runtime/schema changes yet;
- redefine Step-5.5 save/durability semantics;
- redefine Step-5.6 repository transaction protocol;
- choose the physical Python-to-GitHub RepositoryPort bridge;
- finalize live epoch authority transfer — Step 5.8;
- finalize chronology representation/compaction — Step 5.9;
- make Story/transcript/delivery synchronous — Steps 5.10–5.12;
- finalize checkpoint/orphan physical deletion — Step 5.13;
- create a generic snapshot, generic RecoveryCut record, global scheduler or transaction journal;
- define migration policy beyond the compatibility requirements recovery needs to state — Step 6 owns final migration closure.

## 9. Required repository research

Inspect at least:

- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- Step-5 expanded agenda;
- Step-5.1 through 5.6 canonical specs, especially 5.2 and 5.6;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/LIVE_SCENE.md` / `MULTIPLAYER.md` only for dependency exposure;
- `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md`;
- `GAME/SCHEMA/checkpoint.schema.yaml`;
- `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- `GAME/SCHEMA/current_state.schema.yaml`;
- checkpoint template and related bootstrap/storage tests;
- Step-3 runtime owner schemas and current Step-5 routing machine debt where relevant.

## 10. Required analytical challenge

Explicitly challenge at least:

1. checkpoint-first recovery vs current-authority-first recovery;
2. mandatory checkpoint vs optional checkpoint;
3. one checkpoint root manifest vs partitioned native typed routing;
4. `last_checkpoint_id` as authoritative latest frontier vs advisory selected descriptor pointer;
5. `valid_through_event_id` vs domain-native source claims;
6. self-referential `expected_commit_sha` vs no embedded containing-commit authority;
7. checkpoint world-time copy vs chronology-owner evidence;
8. historical rollback support vs ordinary current recovery;
9. stale checkpoint fallback vs owning-scope resolution;
10. one global recovery outcome enum vs recovery status + existing integrity status/reason codes;
11. eager hydration of every referenced record vs transitive correctness-required bounded closure;
12. checkpoint retention for convenience vs explicit retention/GC value.

## 11. Minimum scenario matrix

Cover at least:

1. no checkpoint, simple campaign-only current recovery;
2. valid recent checkpoint, no operational roots;
3. stale checkpoint but newer coherent campaign HEAD;
4. checkpoint pointer missing but native routing complete;
5. pointer references missing checkpoint file;
6. checkpoint malformed but native routing/current sources otherwise coherent;
7. current campaign source missing a required native owner;
8. active Procedure with no open Command;
9. suspended Resolution + Continuation + fixed RNG;
10. mandatory pending child after committed event;
11. armed independently-due temporal owner reachable also from another root;
12. unresolved accepted input promised across handoff;
13. active live route with current live head newer than checkpoint hint;
14. pointed live branch missing/invalid;
15. closed-unabsorbed live source;
16. checkpoint engine projection older than current compatible MANIFEST runtime;
17. required open execution cannot resolve accepted interpretation context;
18. crash after confirmed campaign publication but before local dirty clearing;
19. cold restart after lost publication ACK where remote campaign ref did advance;
20. cold restart after lost ACK where remote ref did not advance;
21. multi-domain partial publication;
22. old checkpoint with deleted/GC-eligible historical dependencies;
23. explicit maintenance request to restore historical checkpoint;
24. derived caches entirely absent;
25. exact transcript unavailable but typed accepted state sufficient;
26. checkpoint absent after explicit save;
27. checkpoint creation independently justified with no gameplay-state delta beyond already durable state;
28. attempted heartbeat/latest-pointer-only refresh.

## 12. Success / exit criteria

Step 5.7 may close only when the architecture can answer, for a cold runtime:

```text
What current authority is selected first?
Which exact native source revisions participate?
How are they discovered without broad scans?
Which checkpoint evidence may help and which may be ignored as stale?
How are owning-scope/current revisions distinguished from historical hints?
What required dependencies must hydrate before resume?
What rebuilds rather than persists?
When is recovery ready?
When is it blocked but not corrupt?
When does integrity become suspect/corrupt?
How are Step-5.6 crash/ambiguity cases resolved from actual authority?
When may an old checkpoint be deleted?
Why can no checkpoint become duplicate current-state authority?
```

Exit target:

> A cold runtime deterministically selects and validates a bounded compatible composition of actual current native durable sources, rebuilds derived state, and resumes only when RRC is proven. Checkpoint evidence may accelerate, diagnose or support explicit historical maintenance, but ordinary recovery correctness does not depend on checkpoint as a second state authority.

Do not begin Step 5.8 until Step 5.7 is canonical and closed.