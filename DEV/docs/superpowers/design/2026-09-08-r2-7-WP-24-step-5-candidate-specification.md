# R2.7 WP-24 Step 5 — Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE READY FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-08

Selected direction: **OWNER-COMPOSED BOUNDED OPERATIONS / GROWTH-AWARE RETENTION / EVIDENCE-TRIGGERED PHYSICAL OPTIMIZATION / STAGED REAL-TARGET PERFORMANCE PROOF**.

This candidate is implementation-facing architecture only after successful Step-6/7/8 closure and final Senior acceptance. It does not authorize implementation planning or implementation.

---

## 1. Scope and authority

WP-24 owns the cross-owner integration contract for performance/scale/operability questions that span already-accepted runtime, context, persistence, LIVE, collaboration, Story, cleanup and host-assurance owners.

It does **not** replace those semantic owners and does not create a global performance authority.

WP-24 candidate responsibilities:

- classify ordinary/special path boundedness;
- preserve owner-defined hard constraints and negative laws;
- distinguish per-operation boundedness from retained-corpus/repository growth;
- define when physical optimization may activate;
- route scale/performance proof to the correct WP-22 evidence class;
- preserve explicit future measurements/evaluations required for the realized supported target.

WP-24 does not own:

- new gameplay semantics;
- ContextNeedProfile semantics or a second context allocator;
- Story candidate/coverage/retention semantics;
- exact storage shard/index/cache layout;
- retry algorithm/count;
- a new scheduler/worker/heartbeat;
- provider-specific context/token limits;
- implementation code, schemas, tests, release or migration execution.

---

## 2. Central invariant

```text
CAMPAIGN / REPOSITORY / INSTRUCTION CORPORA MAY GROW

BUT

ORDINARY CORRECTNESS WORK
    -> is bounded by current semantic scope and registered dependencies
    -> never becomes a whole-campaign / whole-Story / all-ref / all-LIVE scan by fallback
    -> preserves hard owner-defined resource/interactivity constraints
    -> fails/degrades through owner-defined finite outcomes when required work cannot be satisfied

AND

PHYSICAL OPTIMIZATION
    -> activates only from owner-permitted measured evidence/trigger
    -> preserves semantic identity/authority/currentness/eligibility
    -> receives its own version/migration handling when compatibility-bearing
```

### LAW WP24-1 — No global performance authority

WP-24 SHALL NOT define one universal latency, token, context-percentage, repository-call, file-count, retry-count, campaign-size or Story-corpus quota.

Path-specific accepted owners and explicit Product Owner decisions remain controlling. A numerical target is admitted only when a current owner actually supplies it or a later authorized owner decision establishes it.

`GAME/CORE/RUNTIME.md`'s reasoning-performance budget remains a stop rule for unnecessary deliberation, not a fixed token/time/step/complexity ceiling.

---

## 3. Ordinary gameplay critical path

### LAW WP24-2 — Ordinary work scales with the current decision, not campaign age

When the current working set is sufficient, the ordinary in-scene single-player path uses the already-loaded engine instructions and campaign dependencies and requires no repository traffic merely because the campaign is old or large.

When a material dependency is absent, acquisition follows current bounded owner routing/Context Runtime contracts. The need for one dependency cannot silently expand into whole-campaign/history/repository scanning.

### LAW WP24-3 — PO-003 / WP-19 zero-extra-serial law is invariant

For historical Actor decision-basis capture in WP19-L38 scope:

```text
additional sequential LLM calls solely for capture = 0
additional serial remote/tool reads solely for capture when required T0 data is already admitted = 0
additional separate remote publications solely for basis = 0
basis work on irrelevant/trivial/NO_CHANGE turns = 0
additional context/output = bounded typed material items only
```

If realized correctness would require another serial LLM/tool round trip on the ordinary gameplay critical path, that is a material architecture/performance escalation under WP19-L39. It is not silently accepted as implementation cost.

---

## 4. Engine instruction-cache paths

### LAW WP24-4 — Instruction-cache construction is path-class-specific

Accepted instruction loading remains:

```text
NEW CHAT / SUBSTANTIAL SETUP
    exact package -> complete CORE/*.md + RULES/INDEX.md + RULES/README.md preload

ENGINE PACKAGE SWITCH
    invalidate old cache -> complete target cache rebuild before further adjudication

VERIFIED INSTRUCTION-CONTEXT LOSS / COMPACTION
    complete exact-package cache rehydration

ORDINARY TURN / MODULE ACTIVATION
    already-loaded CORE -> zero CORE reread merely for activation
```

Full instruction preload does not authorize campaign/world preload.

### LAW WP24-5 — Current physical CORE measurements have narrow proof power

A current source-file count/byte measurement is Class-A evidence only for that exact source basis. It is not:

- a forecast of eventual production CORE size;
- a sizing baseline for eventual production CORE;
- a token-occupancy calculation;
- prompt-pressure proof;
- user-visible latency proof;
- production-host acceptance.

Whenever a later claim depends on current physical instruction-corpus size and the relevant source corpus changed materially, remeasure the then-current corpus rather than carrying an old Class-A number forward.

### LAW WP24-6 — Full-preload acceptance remains real-target empirical where applicable

If full physical CORE preload remains the production strategy, the implemented supported target must receive production-like evaluation of materially relevant:

- behavioral prompt pressure;
- procedural verbosity / unnecessary checks or retrievals;
- GM/NPC initiative and improvisation quality;
- context/resource pressure;
- latency/tool-call amplification;
- gameplay quality/degradation behavior.

This obligation does not assert that preload is defective and does not authorize a preimplementation surrogate or alternate loading strategy. A material real-target failure may fire an architecture revisit under the normal process.

---

## 5. Campaign context and routing

### LAW WP24-7 — Context acquisition retains R2.3/WP-09 finite semantics

Context discovery/closure remains registered, typed, finite and cycle-safe. Required evidence at legal representation floors precedes optional/supporting allocation. No generic world-graph walk, campaign preload or whole-history fallback is admitted.

If required closure cannot lawfully fit/resolve, preserve the owning terminal/degraded behavior including `UNSATISFIABLE`; performance pressure cannot silently remove required evidence.

### LAW WP24-8 — Known-ID routing remains direct

Known native identity reads derive the exact WP-11 route, load that exact owner and validate identity/currentness/eligibility. They SHALL NOT enumerate a directory or load a discovery index merely to route a known ID.

### LAW WP24-9 — Monolithic family-index partitioning remains trigger-gated

The current monolithic family-index baseline remains accepted until measured size, transfer/parse cost, connected-tool envelope or other owner-admitted operational evidence proves it materially unacceptable.

Neither WP-11's 65,536 shard-selector geometry nor current tiny scaffold indexes fire this trigger by themselves.

Any later index partitioning must preserve:

- known-ID direct routing;
- owner identity validation;
- index non-authority;
- bounded discovery;
- no index-absence semantic proof.

---

## 6. HOT / cache / local operational support

### LAW WP24-10 — Physical support optimizes but never owns semantics

SQLite/HOT/cache/helper structures may be measured/tuned after realization, but their presence, local generation, timestamp, row order or lookup convenience cannot become semantic identity, currentness, chronology, authorization or role eligibility.

A cache optimization is admissible only when the owning source/currentness invalidation contract remains explicit and provable.

No external/network operation may be hidden inside an owner-prohibited local transaction merely for latency optimization.

---

## 7. Durability and publication cost

### LAW WP24-11 — Campaign publication cost is bounded to the participating semantic footprint

Ordinary campaign durability/publication remains bounded to owner-defined policy roots, dirty/current owner generations, required recovery/reference/interpretation companions and the affected semantic/currentness footprint.

Performance work SHALL NOT reintroduce whole-campaign/WORLD/full-Git-history closure scans.

### LAW WP24-12 — One logical campaign publication remains one coherent publication boundary

WP-24 does not optimize one logical campaign durability boundary into per-file Contents writes, merge commits, staging refs, force updates or another transport topology that changes WP-13 publication/currentness semantics.

Remote tree/commit/ref operations, preflight/currentness reads and exact affected dependency refresh are legitimate realized cost dimensions.

### LAW WP24-13 — Retry/contention is bounded and terminal, not globally numbered here

Conflict/currentness movement can amplify preparation, reads and publication attempts. Current owners require bounded retry/failure and typed unresolved outcomes but do not supply one universal retry count or latency ceiling.

WP-24 therefore requires realized measurement of retry/conflict amplification where material while preserving:

- no blind retry of indeterminate publication;
- owner-specific revalidation for relevant overlap;
- transport-only rebuild only for proved-disjoint movement;
- no gameplay mechanics/RNG replay merely because repository base moved.

No new numeric retry SLA is created by WP-24.

---

## 8. LIVE and multi-chat scale

### LAW WP24-14 — LIVE authority lookup remains bounded per affected owner/partition

Current campaign routing + bounded claim/owner metadata selects `CAMPAIGN`, one exact LIVE source, or integrity conflict for an affected target. Ordinary correctness never recovers write authority by scanning WORLD, all refs or all LIVE branches.

### LAW WP24-15 — Multi-chat contention is a realized amplification dimension, not a new authority

Measure, after realization where material:

- exact-source refresh/revalidation work;
- CAS/currentness rejection/ambiguity cost;
- conflict retry frequency/amplification;
- affected-dependency reload scope.

Performance pressure cannot introduce a global LIVE registry, leader, lease, server, total freshness scalar or last-writer-wins semantics.

---

## 9. Collaboration scale

### LAW WP24-16 — Collaboration remains bounded to positive agency dependencies

Durable collaboration exists only under WP-17's admitted bounded collective dependency. Recovery/routing uses completeness-protected bounded PLAYER companions and direct known-ID obligation reads.

No collaboration directory enumeration, global obligation index, scheduler, presence service or heartbeat becomes a performance optimization or correctness dependency.

---

## 10. Story opportunity and catch-up

### LAW WP24-17 — Story service-opportunity check and catch-up execution are distinct cost classes

Every ordinary R2.4 TurnEnvelope retains its accepted compact typed Story backlog/service-opportunity evaluation:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

The opportunity decision SHALL be bounded and must not require an unbounded Story/history scan.

This does **not** mean Story catch-up generation/publication is an unconditional serial per-turn critical-path requirement.

### LAW WP24-18 — Catch-up is bounded per operation and yields to current play

A Story catch-up opportunity processes a finite registered source window. Current-turn correctness/agency/mechanics and protected Narrator/output capacity remain prior. Catch-up may defer/lag and Story publication contention yields rather than blocking the current visible response.

No durable Chronicler queue, worker, lease, heartbeat, global cursor or mandatory commit-after-every-turn is introduced.

---

## 11. Story scale geometry and retention

### LAW WP24-19 — Baseline Story scale preserves all eight registrations

Performance accounting SHALL preserve the fixed production registrations:

```text
T-MSG
T-ARCH
E-EVT
E-REL
M-SEG
M-OUT
N-EVT
N-REL
```

E-EVT/N-EVT independently project the shared native event stream; E-REL/N-REL independently project the shared native relation stream. One layer's coverage cannot be treated as satisfying the other to reduce work.

Scale geometry includes, where applicable:

```text
registration
× native origin (LOCAL or selected LIVE epoch)
× lane/source domain/generation
× independent coverage cursor/state
```

This geometry is not a global Story cursor or a throughput SLA.

### LAW WP24-20 — Bounded Story window/read does not bound total Story corpus

A finite producer candidate window or retrospective read window bounds that operation only.

The total retained Story corpus and total backlog may grow with campaign history and selected origins. There is no corpus-wide Story size quota and no performance license to discard required campaign account merely because the corpus grows.

### LAW WP24-21 — Story retention pressure is phase-distinct

Before required projection, preserve the minimum sufficient native source/anchor or admitted equivalent survivor required by the source/retention owner.

After compatible required Story coverage, preserve the required Story account under its compatible retention/migration/replacement/end-of-promise semantics.

Successful projection does not imply that all storage pressure disappears; native pre-projection protection and post-coverage Story retention are distinct scale dimensions.

### LAW WP24-22 — Source-scope uncertainty fails/defer boundedly

If native routing cannot prove the requested origin/domain source scope complete, return/retain `UNKNOWN/defer` for that completeness claim.

Never recover completeness by scanning all LIVE refs, all Story files or an incomplete source set and declaring coverage caught up.

---

## 12. Mutable-file operability and Story partitionability

### LAW WP24-23 — 10 KiB is a hard per-file invariant, not a corpus quota

Every runtime-authored mutable GitHub-backed textual artifact remains subject to:

```text
RUNTIME_MUTABLE_GITHUB_TEXT_FILE_MAX_BYTES = 10240
```

The final serialized UTF-8 payload is measured before publication. An oversized pending file is resolved through an owner-valid partition/compaction/rollover/ownership operation before publication.

This value is not a total Story/campaign quota and not a vendor hard-limit claim.

### LAW WP24-24 — Every plausibly unbounded Story collection needs a safe bounded partition path

A campaign-growing Story collection cannot rely on one ever-growing mutable singleton as its only supported representation.

Physical realization must define/preserve a deterministic path to an owner-valid bounded representation before the monolithic form becomes an architectural dead end.

Partitioning remains physical routing. A partition/shard/page/bucket/path/offset SHALL NOT become:

- Story or native source identity;
- chronology/causal evidence;
- reader eligibility/disclosure authority;
- coverage semantics;
- currentness authority.

Known-ID direct routing, bounded discovery, publication/currentness, reference closure and storage-topology-neutral retrospective consumption remain controlling.

### LAW WP24-25 — Partition activation/how is evidence-driven

Safe partitionability is mandatory architecture; **concrete partition activation and layout are not selected by WP-24 without evidence**.

Measurement may include:

- actual serialized size/growth;
- whole-file replacement cost;
- transfer/parse latency;
- Git diff/commit amplification;
- conflict pressure;
- connected-host/tool behavior;
- other owner-admitted operational evidence.

WP-24 selects no `PROJECTION_STATE` shard layout, Story partition count, chapter-file layout, family-index partition, rollover threshold or universal shard width.

---

## 13. Direct LLM-facing artifact ergonomics

### LAW WP24-26 — Preserve owner-defined line guidance in its exact class

For directly LLM-facing Story text artifacts expected to be read as normal semantic units:

```text
about 250 lines  = preferred design ceiling
251–300 lines     = review zone; prefer safe partition/smaller semantic unit where appropriate
more than 300     = not acceptable normal steady state without explicit reason that bounded alternate retrieval is safe and semantic partitioning would be worse
```

This is owner-supplied LLM/tooling ergonomics and operability guidance only.

It is **not**:

- a token budget;
- a latency SLA;
- a context-window guarantee;
- a byte-size substitute;
- a replacement for the 10 KiB hard per-file cap;
- a universal line limit for primarily machine-consumed structured artifacts.

A large single serialized line is not made acceptable merely by low line count.

---

## 14. Exact archival edge

### LAW WP24-27 — Storage pressure never authorizes exactness loss

Exact material SHALL NOT be truncated, paraphrased or silently downgraded merely to satisfy file-size or performance pressure.

If an accepted exact archival scope can exceed one indivisible mutable file, its owner/schema must define safe bounded **lossless partition and deterministic reconstruction semantics before that representation is admitted**.

Until such semantics exist, a representation that could make the accepted exact promise impossible is not safely admissible. WP-24 does not choose the archive partition layout.

---

## 15. Diagnostics, cleanup and retained refs

### LAW WP24-28 — Diagnostics remain question-bounded

Performance/scale investigation does not create a package-wide/campaign-wide runtime telemetry scan, persistent observability owner or background cleanup service. Diagnostic evidence stays bounded to the concrete question and owner-qualified currentness.

### LAW WP24-29 — Retained Git refs may grow physically; ordinary authority dependence may not

Because automatic branch/ref deletion is forbidden, non-selected/retired physical refs may persist and accumulate.

WP-24 does **not** claim this physical residue is bounded.

Instead:

- physical ref existence is never authority/currentness;
- ordinary campaign/LIVE authority lookup does not enumerate all refs;
- ref retirement remains logical deauthorization/de-routing;
- performance study of residue may use non-destructive/read-only measurement only;
- no deletion capability probe, deletion fallback, force rewrite or delete/recreate optimization is admitted.

---

## 16. No mandatory autonomous service

### LAW WP24-30 — Performance architecture cannot manufacture unsupported liveness

Current correctness shall not depend on a newly invented always-running:

- save/persistence heartbeat;
- context service;
- Story/Chronicler worker/queue/lease;
- collaboration scheduler/presence heartbeat;
- cleanup/GC worker;
- ref-retirement service.

Accepted foreground/event-driven/turn-local obligations remain with their owners. Host inactivity creates no exact wall-clock execution guarantee unless a future explicit owner changes that product contract.

---

## 17. Optimization admission gate

### LAW WP24-31 — Trigger-gated optimization is mandatory discipline

A physical optimization can be selected only when:

```text
current owner permits the optimization class
AND current/relevant evidence establishes the applicable measured trigger or material operational problem
AND the proposed optimization preserves identity/authority/currentness/eligibility/retention laws
AND the proof class matches the claim
AND compatibility-bearing changes pass applicable Version Impact / migration-adoption gates
```

Future possibility alone is not a trigger.

Examples:

- partition family indexes only when WP-11 measured trigger fires;
- activate Story partition layout when realized growth/transport/operability evidence requires it, while safe partitionability already exists as a design requirement;
- tune retry strategy only from realized contention evidence while preserving WP-13 terminal/epistemic law;
- revisit full instruction loading only if real supported-target evidence materially fails current strategy and the owning architecture is explicitly reopened;
- introduce caches only when measured benefit is real and cache semantics remain non-authoritative.

---

## 18. Proof and acceptance matrix

### LAW WP24-32 — Match proof class to the claim

#### Structural/specification evidence may establish

- direct known-ID routing;
- finite registered context closure/failure forms;
- absence of owner-required global scans;
- hard 10 KiB per-file law;
- Story safe-partitionability requirement;
- no background-service correctness dependency;
- authority/currentness/eligibility separations;
- trigger/defer rules.

#### Class A current physical measurement may establish only the measured current surface

Examples: current instruction-source count/bytes, current scaffold/index serialized size. It is never automatically a production forecast or empirical host acceptance.

#### Class B realized implementation benchmarks should measure, where applicable

- instruction-cache construction/rebuild mechanics;
- context discovery/hydration operation count/volume;
- family-index transfer/parse/routing behavior;
- publication object/ref operation and conflict rebuild cost;
- Story candidate enumeration/catch-up/publication/partition routing;
- exact-archive partition/reconstruction mechanics;
- retained-ref non-destructive operational/listing pressure.

#### Class C real supported-target production-like evaluation should measure, where applicable

- end-to-end responsiveness;
- long-chat/context pressure;
- full-preload behavioral prompt pressure;
- procedural verbosity/unnecessary work;
- GM/NPC initiative/improvisation/gameplay quality;
- real Connector latency and multi-chat contention;
- Story opportunity/catch-up interaction with visible output;
- degradation/`UNSATISFIABLE`/supported-host behavior.

WP-22 remains the proof-class owner. A preimplementation parallel MVP is forbidden as acceptance substitute.

### LAW WP24-33 — Green repository CI is not performance acceptance

A successful exact-head source CI proves only the current checks actually executed by that workflow. It does not by itself prove latency, token/context occupancy, prompt pressure, concurrency performance, Story growth behavior or real-host gameplay acceptance.

---

## 19. Version and migration boundary

### LAW WP24-34 — Current architecture documentation has no runtime version impact

WP-24 Steps 2–8 and its canonical specification change no current machine representation, runtime schema, storage generation, Story generation, package protocol or executable behavior.

A later physical optimization that changes a compatibility-bearing layout/schema/representation performs its own Version Impact Gate and consumes WP-20/native migration/adoption law as applicable. Performance motivation is not permission for unversioned semantic reinterpretation.

---

## 20. Explicit non-goals / deferred decisions

WP-24 candidate does not select:

```text
GLOBAL TURN LATENCY SLA
GLOBAL TOKEN/CONTEXT PERCENTAGE
GLOBAL STORY/CAMPAIGN SIZE QUOTA
GLOBAL FILE COUNT LIMIT
GLOBAL RETRY COUNT
FAMILY INDEX PARTITION LAYOUT
STORY PROJECTION_STATE SHARD LAYOUT
STORY PARTITION COUNT / WIDTH
CHAPTER FILE LAYOUT
EXACT ARCHIVE SHARD LAYOUT
GENERIC CACHE SERVICE
GENERIC BATCHING FRONTIER
GLOBAL LIVE/COLLAB REGISTRY
BACKGROUND STORY/CLEANUP WORKER
REF DELETION
ALTERNATE CORE LOADING STRATEGY
```

Those that are legitimate future choices remain dormant behind existing evidence/owner/version gates.

---

## 21. Candidate result

```text
WP24_STEP5_COMPLETE: YES
CANDIDATE_DIRECTION:
    OWNER-COMPOSED BOUNDED OPERATIONS
    + GROWTH-AWARE RETENTION
    + EVIDENCE-TRIGGERED PHYSICAL OPTIMIZATION
    + STAGED REAL-TARGET PERFORMANCE PROOF

NEW_GLOBAL_PERFORMANCE_AUTHORITY: NO
NEW_NUMERIC_SLA: NO
STORY_CORPUS_QUOTA: NO
CONCRETE_INDEX_PARTITION: NO
CONCRETE_STORY_SHARD_LAYOUT: NO
BACKGROUND_WORKER/SCHEDULER: NO
FULL_CORE_STRATEGY_REOPENED: NO
HUMAN_DECISION_REQUIRED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
IMPLEMENTATION_STARTED: NO

NEXT: STEP 6 WHOLE-PROJECT ADVERSARIAL REVIEW
```
