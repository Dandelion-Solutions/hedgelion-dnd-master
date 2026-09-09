# R2.7 WP-24 — Performance / Scale / Operational Budget — Canonical Specification

Status: **CANONICAL WP-24 RESULT — FINAL SENIOR PASS / CLOSED — CURRENT AS AMENDED BY 2026-09-09 SIZING-BANDS OWNER**

Date: 2026-09-08

Canonical direction:

> **OWNER-COMPOSED BOUNDED OPERATIONS / GROWTH-AWARE RETENTION / TRIGGER-GATED PHYSICAL OPTIMIZATION / STAGED REAL-TARGET PERFORMANCE PROOF**

Canonicalization basis:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-1-whole-project-critic.md`;
- mandatory independent Step-1 Senior re-review: **PASS / GO** (`SR24-S1-01..04 CLOSED`);
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-2-evidence-reconciliation.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-4-cross-system-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-7-finding-resolution-propagation.md`.

This file is the single final implementation-facing WP-24 architecture owner. Mandatory independent final Senior review has passed and WP-24 is closed. Earlier design/review artifacts remain provenance. The later Product Owner decision `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` supersedes only WP24-13/WP24-32's former universal 10 KiB hard-cutoff semantics; all unaffected boundedness, evidence, partitionability and semantic-preservation laws remain current.

This specification does **not** authorize implementation planning, implementation, performance-optimization implementation, release, migration or gameplay bootstrap.

---

# 1. Scope and authority

WP-24 owns the cross-owner integration contract for performance, scale and operability across already accepted runtime, context, storage, durability, recovery, chronology, LIVE, collaboration, Story, cleanup and host-assurance owners.

It does not replace those semantic owners and creates no global performance authority.

WP-24 owns only these architecture responsibilities:

- identify ordinary and special workload paths;
- preserve owner-defined hard resource/interactivity constraints;
- require correctness operations to remain bounded to their semantic scope;
- distinguish per-operation boundedness from retained corpus/repository growth;
- define trigger semantics for physical optimization without selecting premature topology;
- route proof to the correct WP-22 evidence class;
- preserve future realized/supported-target performance acceptance obligations.

WP-24 does not own:

- gameplay semantics;
- ContextNeedProfile semantics or a second context allocator;
- Story candidate/coverage/retention semantics;
- exact index/shard/page/cache/SQLite topology;
- one global retry algorithm/count;
- a scheduler, worker, queue, lease or heartbeat;
- provider-specific context/token ceilings;
- a universal campaign/Story cursor;
- a global freshness/frontier scalar;
- implementation code/schemas/tests;
- release or migration execution.

---

# 2. Central invariant

```text
CAMPAIGN / STORY / REPOSITORY / INSTRUCTION CORPORA MAY GROW

BUT

ONE CORRECTNESS OPERATION
    -> is bounded by current semantic scope and registered dependencies
    -> never falls back to whole-campaign / whole-Story / all-ref / all-LIVE / full-history scanning
    -> preserves hard owner-defined resource/interactivity constraints
    -> degrades/fails through finite owner-defined outcomes when required work cannot be satisfied

AND

PHYSICAL OPTIMIZATION
    -> activates only from an owner-permitted trigger/evidence
    -> activates mandatorily before a hard owner limit would be violated
    -> preserves identity/authority/currentness/eligibility/retention semantics
    -> uses normal Version Impact / migration law if compatibility-bearing
```

## LAW WP24-1 — No global performance authority or invented numerical SLA

WP-24 SHALL NOT define one universal latency, token, context-percentage, repository-call, file-count, record-count, retry-count, campaign-size or Story-corpus quota.

Path-specific accepted owners and explicit Product Owner decisions remain controlling. A numerical target is admitted only when a current owner supplies it or a later authorized owner decision establishes it.

`GAME/CORE/RUNTIME.md`'s reasoning-performance budget remains a stop rule for unnecessary deliberation, not a fixed token/time/step/complexity ceiling.

---

# 3. Proof and evidence classes

WP-24 consumes the WP-22 proof boundary.

## LAW WP24-2 — Structural boundedness, physical measurement, realized benchmark and empirical acceptance remain distinct

```text
SPECIFICATION / STRUCTURAL BOUNDEDNESS
    != CLASS A CURRENT-SURFACE MEASUREMENT
    != CLASS B REALIZED IMPLEMENTATION BENCHMARK
    != CLASS C PRODUCTION-LIKE SUPPORTED-TARGET EMPIRICAL ACCEPTANCE
```

### Class A

Current exact-source measurements may establish only the measured current surface and basis, such as file counts/bytes or inspectable current topology.

### Class B

After the relevant production path exists, benchmark machine-realized reads/writes/materialization/publication/routing/retry/recovery/sharding behavior.

### Class C

Use the real implemented supported target for end-to-end host/LLM/Connector/user-visible properties such as responsiveness, prompt pressure, long-context behavior, contention and gameplay quality.

No preimplementation surrogate or parallel MVP may be used to manufacture Class-C acceptance evidence.

## LAW WP24-3 — Green CI proves only the checks it actually executes

Repository CI/static/unit success does not establish user-visible latency, model token occupancy, prompt pressure, gameplay quality, Story anti-starvation or production contention acceptance unless the executed check genuinely proves that bounded property.

---

# 4. Ordinary gameplay critical path

## LAW WP24-4 — Ordinary work scales with the current decision, not campaign age

When the current working set is sufficient, an ordinary in-scene turn uses the already-loaded engine instructions and current campaign dependencies and requires no repository traffic merely because the campaign is old or large.

When a material dependency is absent, acquisition follows current bounded owner routing/Context Runtime contracts. One missing dependency cannot silently expand into whole-campaign/history/repository scanning.

## LAW WP24-5 — PO-003 / WP19-L38 zero-extra-serial law is invariant

For historical Actor decision-basis capture on the ordinary gameplay critical path:

```text
additional sequential LLM calls solely for capture = 0
additional serial remote/tool reads solely for capture when required T0 data is already admitted = 0
additional separate remote publications solely for basis = 0
basis work on irrelevant/trivial/NO_CHANGE turns = 0
additional context/output = bounded typed material items only
```

If later realization proves another serial LLM/tool round trip is required for correctness, that is a material architecture/performance escalation under WP19-L39 and must be routed through the applicable architecture/Product Owner process before adoption.

---

# 5. Engine instruction-cache paths

## LAW WP24-6 — Full CORE preload is path-class-specific

Accepted instruction loading remains:

```text
NEW CHAT / SUBSTANTIAL SETUP
    exact package
    -> complete CORE/*.md
    -> RULES/INDEX.md
    -> RULES/README.md
    -> one current-chat immutable engine instruction cache

ENGINE PACKAGE SWITCH
    invalidate old cache
    -> build complete exact-target cache
    -> no adjudication on mixed/old cache

VERIFIED INSTRUCTION-CONTEXT LOSS / COMPACTION
    complete exact-package cache rehydration

ORDINARY TURN / MODULE ACTIVATION
    already-loaded cache
    -> zero CORE reread merely for activation
```

Full instruction preload never authorizes campaign/world preload.

## LAW WP24-7 — Current physical CORE measurement is Class A only

The Step-2 exact current measurement at its source basis was:

```text
CORE *.md files                 45
aggregate CORE bytes            364,844 B
RULES/INDEX.md                    1,752 B
RULES/README.md                   4,132 B
complete preload sources             47
complete preload source bytes     370,728 B
```

This is:

```text
CURRENT PHYSICAL CORPUS MEASUREMENT ONLY
!= model token occupancy
!= prompt-pressure proof
!= user-visible latency benchmark
!= real-MVP empirical acceptance
```

If the relevant source corpus changes materially before a size-dependent claim, remeasure the then-current corpus. Do not carry this number forward as an eventual production sizing forecast.

## LAW WP24-8 — Full-preload acceptance is real-target empirical where applicable

If full physical CORE preload remains the production strategy, the implemented supported target must receive production-like evaluation of materially relevant:

- behavioral prompt pressure;
- procedural verbosity/unnecessary checks or retrievals;
- GM/NPC initiative;
- improvisation quality;
- context/resource pressure;
- latency/tool-call amplification;
- gameplay quality/degradation behavior.

Where an appropriate controlled/routed comparison can be performed without changing semantic law, it may be used to diagnose whether full preload materially degrades those properties. This is future real-target evidence, not permission to replace the preload strategy during architecture closure.

---

# 6. Campaign context and known-ID routing

## LAW WP24-9 — Context acquisition retains R2.3/WP-09 finite semantics

Context discovery/closure remains registered, typed, finite and cycle-safe. Required evidence at legal representation floors precedes optional/supporting allocation.

No generic world-graph walk, campaign preload or whole-history fallback is admitted.

If required closure cannot lawfully resolve/fit, preserve the owning finite degraded/terminal semantics including `UNSATISFIABLE`; performance pressure cannot silently remove required evidence.

## LAW WP24-10 — Known-ID routing remains direct

Known native identity reads derive the exact WP-11 route, load that exact owner and validate identity/currentness/eligibility. They SHALL NOT enumerate a directory or load an index merely to route a known ID.

---

# 7. Campaign-menu / preselection scale

## LAW WP24-11 — Campaign discovery is bounded per menu operation

Before campaign selection, storage/campaign discovery remains projection-only and bounded.

A conforming realization SHALL NOT require exhaustive traversal of every physically retained `campaign/*` ref in one menu operation once the candidate set exceeds the admitted bounded retrieval envelope.

Owner-valid realization may use provider-supported bounded paging/continuation, bounded exact-name/prefix narrowing, a compact owner-valid discovery projection or another deterministic bounded discovery mechanism.

WP-24 selects no concrete campaign registry/index/page layout.

Campaign card/menu data nominates only. Current campaign/access/currentness owners are revalidated after selection.

Physically retained/archived refs remain non-authoritative and branch/ref deletion remains forbidden.

---

# 8. Family indexes and mutable-file sizing

## LAW WP24-12 — Monolithic family indexes remain baseline only while safely operable

The current WP-11 monolithic family-index baseline remains accepted while it satisfies every controlling owner limit and no measured size/transfer/parse/tool behavior establishes material operational failure.

WP-11's 65,536 route-bucket geometry and current small scaffold indexes do not themselves require index partitioning.

Any future index partitioning must preserve:

- known-ID direct routing;
- owner identity validation;
- index non-authority;
- bounded discovery;
- no index-absence semantic proof.

## LAW WP24-13 — Mutable artifact sizing uses target / review / review-and-partition bands

Current threshold semantics are owned by `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` and supersede WP-24's former universal `10240` hard publication cutoff.

For growth-bearing runtime-authored mutable GitHub-backed textual artifacts, measure the projected final serialized UTF-8 payload before publication and apply:

```text
PREFERRED TARGET BAND
    approximately 10–12 KiB or smaller where owner-valid

REVIEW BAND
    materially above target through approximately 16 KiB
    with 13–16 KiB as the normal explicit review zone

REVIEW / PARTITION / ROLLOVER BAND
    above approximately 16 KiB
    -> owner-valid bounded representation is the default expectation
       before indefinite further growth
```

These are decision bands, not validity enums and not a universal byte-hard-stop. A file in the review zone is not automatically invalid. One indivisible owner unit may remain intact when splitting would break identity, atomicity, provenance, exactness or another accepted semantic law. Required material must never be truncated or falsely split to meet a target number.

A mutable monolithic index, Story control artifact, retained planning/collaboration record or equivalent must have a deterministic owner-valid bounded partition/rollover path before it becomes an operational dead end. Earlier optimization may be justified by measured size/latency/parse/conflict/tool behavior.

This is per-file operational policy, not a total campaign/Story corpus quota or vendor hard-limit claim.

WP-24 selects no concrete shard/page/rollover layout or exact universal rollover threshold.

---

# 9. HOT / cache / local support

## LAW WP24-14 — Physical support may optimize but never become authority

SQLite/HOT/cache/helper structures may be measured and tuned after realization, but physical presence, local generation, timestamp, row order or lookup convenience cannot become semantic identity, currentness, chronology, authorization or role eligibility.

A cache optimization is admissible only when owning source/currentness invalidation remains explicit and provable.

No external/network operation may be hidden inside an owner-prohibited local transaction merely for latency optimization.

---

# 10. Durability, publication and stale-base synchronization

## LAW WP24-15 — Publication work remains bounded to the participating semantic footprint

Campaign durability/publication remains bounded to owner-defined policy roots, dirty/current owner generations, required recovery/reference/interpretation companions and the affected semantic/currentness footprint.

No whole-campaign/WORLD/full-Git-history closure scan is admitted.

## LAW WP24-16 — One logical campaign durability boundary remains one coherent publication boundary

Performance optimization cannot transform one logical campaign durability boundary into per-file Contents mutations, merge commits, staging refs, force updates or another transport topology that changes WP-13 publication/currentness semantics.

## LAW WP24-17 — Retry/contention is bounded and terminal, with no universal retry count

Current owners require bounded retry/failure and typed unresolved outcomes. WP-24 does not invent a global retry count or latency ceiling.

Realized retry/conflict measurement must preserve:

- no blind retry after indeterminate publication;
- owner-specific revalidation for relevant overlap;
- transport-only rebuild only for proven-disjoint movement;
- no mechanics/RNG replay merely because repository base moved.

## LAW WP24-18 — Changed-path comparison has a bounded direct-footprint fallback

Changed-path comparison is an optimization, not permission for unbounded stale-interval traversal.

```text
if provider-supported base..HEAD changed-path comparison
fits the admitted bounded envelope:
    compare
    -> intersect with bounded loaded/dirty/current-decision dependency footprint
    -> reread only affected exact owners

else:
    pin current authoritative HEAD/source basis
    -> directly reread/revalidate only the bounded current owner/dependency/
       authorization/routing footprint required by loaded dirty/current-decision state
    -> reconcile/adopt under native owners
```

Do not exhaustively paginate an arbitrarily large stale interval, walk full Git history or treat a partial comparison as proof that omitted changes are irrelevant.

Real comparison result size/read amplification belongs to Class B; real multi-chat contention/responsiveness belongs to Class C where material.

---

# 11. LIVE and collaboration scale

## LAW WP24-19 — LIVE authority lookup stays bounded per affected owner/partition

Current campaign routing plus bounded claim/owner metadata selects `CAMPAIGN`, one exact LIVE source or integrity conflict for the affected target.

Ordinary correctness never recovers authority by scanning WORLD, all refs or all LIVE branches.

## LAW WP24-20 — Multi-chat contention is a realized amplification dimension, not a new authority

Measure after realization, where material:

- exact-source refresh/revalidation work;
- CAS/currentness rejection/ambiguity cost;
- conflict retry frequency/amplification;
- affected dependency reload scope;
- stale-base synchronization behavior.

Performance pressure cannot introduce a global LIVE registry, leader, lease, total freshness scalar or last-writer-wins semantics.

## LAW WP24-21 — Collaboration stays bounded to positive agency dependencies

Durable collaboration exists only under WP-17's bounded collective-dependency law. Recovery/routing uses bounded PLAYER companions and direct known-ID obligation reads.

No collaboration directory enumeration, global obligation index, scheduler, presence service or heartbeat becomes a performance optimization/correctness dependency.

---

# 12. Recovery / checkpoint / chronology scale

## LAW WP24-22 — Cold recovery is a bounded current-root special path

Ordinary cold recovery follows:

```text
current routed native sources
-> exact participating source pins
-> bounded independent operational roots
-> correctness-required RRC/dependency closure only
-> rebuild derivative Agenda/index/cache support
-> validate current compatible participating basis
```

Its correctness work scales with the admitted current operational roots and required dependency closure for the requested recovery scope, not total campaign age/history merely because old history exists.

No campaign-wide WORLD, LOG/history, all-checkpoint, all-runtime-record or broad-Git-history scan is admitted.

## LAW WP24-23 — Checkpoint is optional acceleration/evidence, never a scale shortcut to authority

Checkpoint may be measured as a recovery accelerator where useful, but healthy ordinary recovery may read zero checkpoints.

Do not select “latest” checkpoint by directory enumeration, timestamp, ID magnitude or Git order. Checkpoint never replaces current native routing/root completeness/currentness.

## LAW WP24-24 — Temporal rebuild and chronology remain owner-bounded

Cold recovery hydrates admitted temporal/process roots and reconstructs the complete owner-declared dependency enrollment/Agenda required for future invalidatability.

Missing derivative enrollment cannot authorize all-thread/WORLD/LOG scanning.

Chronology/historical relation retrieval expands only for the concrete typed dependency/question with finite owner-valid work. No global fictional timeline reconstruction, chronology clock or generic recovery frontier/cursor is introduced.

Recovery root cardinality/hydration/read counts and machine latency belong to Class B. Real supported-host recovery experience is Class C where host behavior is material.

---

# 13. Story service opportunity and catch-up

## LAW WP24-25 — Story opportunity check and catch-up execution are distinct cost classes

Every ordinary R2.4 TurnEnvelope retains its compact typed Story service-opportunity evaluation:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

This does not make catch-up generation/publication an unconditional serial per-turn critical-path requirement.

## LAW WP24-26 — Story service-opportunity detection is bounded across campaign-age/source-domain fan-out

The opportunity check itself SHALL have finite per-envelope work and SHALL NOT exhaustively walk all historical Story source domains/origins/lanes as campaign history grows.

Current Story/native routing and compact coverage/source-basis metadata nominate only a bounded candidate set of source domains/windows for the current opportunity.

If broader source-scope completeness cannot be proven within the admitted bound:

```text
UNKNOWN / DEFER
```

Never recover completeness by scanning all LIVE refs/Story domains or by declaring an incomplete set caught up.

Residual compatible backlog remains an outstanding future service obligation. No durable queue, global cursor, cross-origin total order, scheduler, worker, lease or heartbeat is introduced.

## LAW WP24-27 — Catch-up is bounded per operation and yields to current play

One Story catch-up opportunity processes a finite registered source window.

Current-turn correctness/agency/mechanics and protected Narrator/output capacity remain prior. Catch-up may defer/lag; Story publication contention yields rather than blocking current visible response.

---

# 14. Story growth geometry and retention

## LAW WP24-28 — Baseline scale accounting preserves all eight Story registrations

Performance accounting SHALL preserve:

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

E-EVT/N-EVT independently project shared native event candidates; E-REL/N-REL independently project shared native relation candidates. One layer's coverage does not satisfy the other merely to save work.

Scale geometry includes, where applicable:

```text
registration
× native origin (LOCAL or LIVE:<native epoch>)
× lane/source domain/generation
× independent coverage state
```

There is no global Story cursor or cross-origin/lane ordering.

## LAW WP24-29 — Bounded producer/read windows do not bound total retained Story corpus

A finite producer candidate window or retrospective read bounds one operation only.

The total retained Story corpus and total backlog may grow with campaign history and admitted origins. There is no corpus-wide Story quota and no performance license to discard required accepted campaign account merely because the corpus grows.

## LAW WP24-30 — Story retention pressure is phase-distinct

Before required projection, preserve the minimum sufficient native source/anchor or admitted equivalent survivor required by the source/retention owner.

After compatible required Story coverage, preserve the required Story account under its retention/migration/replacement/end-of-promise semantics.

Successful projection does not imply all storage pressure disappears; native pre-projection protection and post-coverage Story retention are separate scale dimensions.

---

# 15. Story partitionability and consumer decoupling

## LAW WP24-31 — Every plausibly unbounded Story collection needs a safe bounded partition path

A campaign-growing Story collection cannot rely on one ever-growing mutable singleton as its only supported physical representation.

Physical realization must preserve a deterministic path to owner-valid bounded representation before the monolithic form becomes an architectural dead end.

Physical partition/shard/page/bucket/path/offset SHALL NOT become:

- Story/native source identity;
- chronology or causal evidence;
- reader eligibility/disclosure authority;
- coverage semantics;
- currentness authority.

Known-ID direct routing, bounded discovery, publication/currentness, reference closure and consumer topology-neutrality remain controlling.

## LAW WP24-32 — Concrete partition layout remains evidence-triggered and unselected

WP-24 selects no:

- `PROJECTION_STATE` shard layout;
- Story partition count;
- chapter-file layout;
- family-index partition scheme;
- exact universal rollover threshold;
- universal shard width.

Earlier activation may be justified by measured size, whole-file replacement cost, transfer/parse latency, Git amplification, conflict pressure or supported-tool behavior.

Current `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` policy is also an activation input: 13–16 KiB is the normal explicit review zone and above approximately 16 KiB is the default review/partition/rollover zone for growth-bearing mutable artifacts. Those bands are not a universal semantic hard stop; owner identity, atomicity, exactness, provenance and safe reconstruction remain controlling.

---

# 16. Direct LLM-facing Story ergonomics

## LAW WP24-33 — Preserve the owner-defined line policy in its exact class

For directly LLM-facing Story text artifacts expected to be read as normal semantic units:

```text
about 250 lines  -> preferred design ceiling
251–300 lines    -> review zone; prefer safe partition/smaller semantic unit where appropriate
more than 300    -> not acceptable normal steady state without explicit reason that bounded alternate retrieval is safe and semantic partitioning would be worse
```

This is LLM/tooling ergonomics guidance only.

It is not a token budget, latency SLA, context-window guarantee, byte-size substitute or universal limit for primarily machine-facing structured artifacts.

A very large single serialized line is not made acceptable by low line count.

---

# 17. Exact archival edge

## LAW WP24-34 — Performance/storage pressure never authorizes exactness loss

Exact material SHALL NOT be truncated, paraphrased or silently downgraded merely to satisfy file-size/performance pressure.

If an accepted exact archival scope can exceed one indivisible mutable file, its owner/schema must define safe bounded **lossless partition and deterministic reconstruction semantics before that representation is admitted**.

Until such semantics exist, a representation that could make the accepted exact promise impossible is not safely admissible.

WP-24 does not choose the archival partition layout.

---

# 18. Diagnostics, retained refs and background-liveness prohibitions

## LAW WP24-35 — Performance diagnostics remain question-bounded

Performance/scale investigation does not create a runtime telemetry mega-scan, persistent observability authority or background cleanup service. Diagnostic evidence remains bounded to the concrete question and owner-qualified currentness.

## LAW WP24-36 — Retained refs may grow physically; ordinary authority dependence may not

Branch/ref deletion is forbidden. Non-selected/retired refs may persist and accumulate physically.

Therefore:

- physical ref existence is never authority/currentness;
- ordinary campaign/LIVE authority lookup does not enumerate all refs;
- campaign-menu discovery obeys LAW WP24-11 rather than relying on unbounded enumeration;
- ref retirement remains logical deauthorization/de-routing;
- residue may be measured non-destructively;
- no deletion capability probe, deletion fallback, force rewrite or delete/recreate optimization is admitted.

## LAW WP24-37 — No hidden background-liveness dependency

WP-24 preserves existing negative laws. Correctness does not require a new:

- save heartbeat;
- Story worker/queue/lease/heartbeat;
- collaboration scheduler/presence heartbeat;
- background cleanup queue/service;
- polling loop that must run while the host is inactive.

An event-driven foreground rebuild/service opportunity is not a background service.

---

# 19. Optimization activation law

## LAW WP24-38 — Coverage is not activation

A future scale dimension, measurement obligation or revisit trigger does not manufacture current optimization work.

Classify each candidate as one of:

```text
ALREADY BOUNDED / NO ACTION
HARD OWNER CONSTRAINT / MUST PRESERVE
MEASUREMENT-DORMANT
TRIGGERED BY CURRENT EVIDENCE
DEFERRED UNTIL REALIZATION
DEFERRED UNTIL REAL-TARGET EMPIRICAL EVIDENCE
OUT OF SCOPE
```

## LAW WP24-39 — Optimization cannot change semantic authority by convenience

A physical optimization is legal only when it preserves all applicable:

- semantic identity;
- source/currentness authority;
- role/recipient eligibility;
- coverage meaning;
- chronology neutrality;
- publication/crash-consistency law;
- retention/exactness requirements;
- known-ID/direct-route behavior;
- failure/indeterminate semantics.

If an optimization changes a compatibility-bearing physical layout/schema/generation meaning, use the applicable Version Impact and migration/adoption law.

---

# 20. Future verification / benchmark / evaluation obligations

The final implementation plan, when separately authorized, must route the following without treating this list as current implementation authorization.

## 20.1 Deterministic / structural verification where realized

Verify as applicable:

1. current mutable-artifact target/review/review-and-partition sizing bands with exact serialized UTF-8 measurement, no universal `10240` rejection, and owner-valid no-truncation/partition semantics;
2. direct known-ID route without directory/index enumeration;
3. bounded campaign-menu discovery/continuation behavior;
4. bounded Context Runtime required closure and finite failure;
5. bounded changed-path compare with direct current-footprint fallback;
6. bounded current-source recovery/root hydration without global scans;
7. temporal dependency enrollment/Agenda rebuild without global fallback;
8. bounded Story service-opportunity selection with `UNKNOWN/DEFER` on unproved broader completeness;
9. Story eight-registration/source-domain semantics remain intact;
10. no branch/ref deletion/probing;
11. no hidden background worker/heartbeat correctness dependency;
12. safe exact archival partition/reconstruction once such representation is realized.

## 20.2 Class-B realized benchmarks

Measure where material:

- campaign-menu/card fan-out and calls;
- Context Runtime discovery/hydration/read counts;
- index transfer/parse behavior;
- initial scaffold publication calls/objects/latency;
- ordinary publication call count;
- retry/conflict amplification;
- stale-base changed-path result/fallback behavior;
- LIVE/currentness refresh cost;
- Story opportunity/catch-up source-domain fan-out and publication cost;
- Story partition routing/reconstruction cost;
- recovery root cardinality/hydration reads/latency;
- retained-ref operational read/list cost where relevant;
- package-discovery count only if its dormant trigger fires.

## 20.3 Class-C supported-target empirical evaluation

Evaluate on the real implemented MVP/supported host where materially applicable:

- ordinary-turn responsiveness;
- new-chat/menu responsiveness;
- long-chat/context pressure;
- full-preload prompt/behavior pressure;
- unnecessary procedural verbosity/checking;
- GM/NPC initiative and improvisation;
- real Connector latency/tool-call amplification;
- multiplayer/multi-chat contention;
- Story anti-starvation under growing multi-origin backlog;
- retrospective navigation quality under large retained Story corpus;
- recovery user-visible experience;
- gameplay quality/degradation under representative long campaigns.

Do not build a parallel preimplementation MVP to execute these obligations.

---

# 21. Step-6 findings and final dispositions

| Finding | Severity | Final disposition |
|---|---|---|
| `F24-06-01` campaign-menu cardinality | SIGNIFICANT | RESOLVED by LAW WP24-11 / WP24-36 |
| `F24-06-02` former 10 KiB hard activation trigger | SIGNIFICANT | RESOLVED by original LAW WP24-13 / WP24-32, then threshold semantics SUPERSEDED by `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` while bounded partitionability remains current |
| `F24-06-03` Story opportunity domain fan-out | SIGNIFICANT | RESOLVED by LAW WP24-26 / future B/C proof |
| `F24-06-04` stale-base changed-path scale | SIGNIFICANT | RESOLVED by LAW WP24-18 |
| `F24-06-05` recovery/chronology omitted path | SIGNIFICANT | RESOLVED by LAW WP24-22..24 |
| `F24-06-M1` installed package count | MINOR | SAFE DEFERRED / dormant measured trigger |
| `F24-06-M2` initial scaffold publication | MINOR | SAFE DEFERRED / future Class-B benchmark |

```text
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
```

---

# 22. Version Impact

```text
VERSION_IMPACT: VERIFIED
VERSION_BUMP_REQUIRED: NO
VERSION_IMPACT_DISPOSITION: NONE
VERSIONING_TAXONOMY_REOPENED: NO
```

Reason: WP-24 Steps 2–8 and the later WP-26 documentation/supersession reconciliation alter architecture/design/status prose and tests only. They do not by themselves alter a version-bearing runtime module, persistent schema, Story semantic generation, storage generation, protocol, package/release format or executable gameplay implementation.

A later optimization implementation that changes a compatibility-bearing physical layout/schema/generation must perform its own Version Impact Gate.

---

# 23. Final architecture result

```text
SELECTED_ARCHITECTURE:
    OWNER-COMPOSED BOUNDED OPERATIONS
    + GROWTH-AWARE RETENTION
    + TRIGGER-GATED PHYSICAL OPTIMIZATION
    + STAGED REAL-TARGET PERFORMANCE PROOF

WP24_STEP1_SENIOR_RE_REVIEW: PASS / GO
WP24_STEPS_2_8: COMPLETE
WP24_STEP6_COMPLETE: YES
WP24_STEP7_COMPLETE: YES
WP24_STEP8_CANONICALIZATION: COMPLETE
WP24_FINAL_SENIOR_RE_REVIEW: PASS / GO
WP24_FINAL_CLOSURE: PASS
WP24_CLOSED: YES

STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 5
STEP6_MINOR_FOUND: 2
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO

NEW_GLOBAL_PERFORMANCE_OWNER: NO
NEW_GLOBAL_CURSOR_FRONTIER: NO
NEW_SCHEDULER_WORKER_HEARTBEAT: NO
CONCRETE_SHARD_LAYOUT_SELECTED: NO
NEW_NUMERIC_LATENCY_TOKEN_SLA: NO
BRANCH_REF_DELETION: FORBIDDEN

IMPLEMENTATION_PLANNING_AUTHORIZED: NO
SUBSTANTIVE_IMPLEMENTATION_AUTHORIZED: NO
PERFORMANCE_OPTIMIZATION_IMPLEMENTATION_AUTHORIZED: NO
```
