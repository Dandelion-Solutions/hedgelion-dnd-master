# R2.7 WP-24 Step 1 — Mandatory Whole-Project Critic

Status: **SR24-S1-04 REPAIR CRITIC COMPLETE — SR24-S1-01 / SR24-S1-02 / SR24-S1-03 PASS/CLOSED — MANDATORY INDEPENDENT SENIOR RE-REVIEW PENDING**

Date: 2026-09-08

Original Step-1 evidence basis: `1c3b85a509a592d0e11da6bc64d9119f5b543a4a`.

Primary Senior-recovery evidence basis: `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`.

SR24-S1-03 micro-recovery evidence basis: `83d018e42db9fa35a900f3b961f69edbee2a3d8e`.

SR24-S1-04 repair evidence basis: `ac111c0d61da7e0bcf4226783eb34f7b0c43c0f7`.

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-task-brief-source-manifest.md`.

This file is the mandatory Step-1 whole-project framing critic required by `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, including the rerun after the current Story persistence growth/sharding owner exposed propagation/completeness gaps. It is not a Step-6 candidate-spec adversarial review and does not authorize Step 2.

---

## 1. Critic method

The critic does not accept the Task Brief's dependency list as authority. The current rerun reconstructs the WP-24 dependency subgraph from current `DEV/PROJECT_MAP.md` and actual owners/consumers.

The four canonical WP-24 questions are routed through:

- current process/program/PO owners;
- PO-003/WP-19 performance owner chain;
- context/runtime/host and physical instruction-cache contracts;
- storage/routing/HOT/publication owners;
- LIVE/multiplayer/collaboration owners;
- Story/continuity/planning/retrospective consumers;
- the Story integration contract plus its baseline projection-source companion;
- the Story persistence-growth/sharding/consumer-decoupling owner decision;
- exact-archive retention/admission owners implicated by the Story operability edge;
- diagnostics/cleanup/retention/ref-lifecycle owners;
- current CORE consumers and the exact current CORE/RULES physical corpus;
- schema/scaffold/tool/test/CI surfaces;
- WP-22 proof classification;
- explicit closed decisions and revisit triggers.

The rerun searches for scope omissions, stale routing, lost item-level owner requirements, duplicated/reopened authority, hidden unbounded hot paths, unsupported host assumptions, non-equivalent measurements, premature optimization, unsafe deferral, misclassified empirical obligations, unsupported numeric budgets and accepted constraints weakened by framing.

Finding severity means **framing risk for WP-24 Step 1**, not a claim that final architecture contains the defect.

---

## 2. Review history and current summary

Original worker critic before first Senior review:

```text
ORIGINAL_BLOCKING_FOUND: 0
ORIGINAL_SIGNIFICANT_FOUND: 6
ORIGINAL_MINOR_FOUND: 3
ORIGINAL_WORKER_REPAIRS_APPLIED: YES
```

Initial mandatory independent Senior review returned:

```text
WP24_STEP1_SENIOR_REVIEW: HOLD
SR24-S1-01: BLOCKING / OPEN
SR24-S1-02: SIGNIFICANT / OPEN
HUMAN_DECISION_REQUIRED_NOW: NO
WP24_STEP2_AUTHORIZED: NO
```

Subsequent bounded recoveries were independently accepted through SR24-S1-03. Current Senior state entering this repair is:

```text
SR24-S1-01: PASS / CLOSED
SR24-S1-02: PASS / CLOSED
SR24-S1-03: PASS / CLOSED
SR24-S1-04: SIGNIFICANT / OPEN
WP24_STEP2_AUTHORIZED: NO
```

Current SR24-S1-04 repair/rerun result:

```text
SR24-S1-04_REPAIR_APPLIED: YES
REPAIR_RERUN_NEW_BLOCKING_FOUND: 0
REPAIR_RERUN_NEW_SIGNIFICANT_FOUND: 0
UNRESOLVED_BLOCKING_IN_WORKER_VIEW: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_VIEW: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
STEP2_AUTHORIZED: NO
```

This is a worker repair disposition pending independent Senior re-review; it is not a Senior PASS claim for SR24-S1-04.

---

## 3. Senior findings and recovery dispositions

### SR24-S1-01 — Unsupported `120 seconds` Product Owner law

**Original severity:** BLOCKING

The earlier recovery established that no current owner defines a `120 seconds` / `T_budget=120s` Product Owner turn law. The actual PO-003/WP-19 law is zero-extra-serial basis capture in its stated scope, and `GAME/CORE/RUNTIME.md` rejects a fixed token/time/step/complexity turn ceiling.

**Current Senior disposition:** **PASS / CLOSED**.

---

### SR24-S1-02 — Full-CORE preload / cache rebuild omitted

**Original severity:** SIGNIFICANT

The earlier recovery split initial full CORE+RULES preload, package-switch cache rebuild, verified-loss rehydration and ordinary-turn zero CORE reread; it also classified the measured `370,728 B` current source corpus as Class A only, not a forecast or production sizing baseline.

**Current Senior disposition:** **PASS / CLOSED**.

---

### SR24-S1-03 — Current Story baseline scale/performance owner omitted

The prior micro-recovery directly incorporated the baseline projection source contracts and current Story persistence-growth/sharding owner into WP-24 framing, preserving eight registrations, EVENTS/NARRATIVE independent obligations, LOCAL/LIVE origin/domain/cursor fan-out, bounded-window versus total-corpus separation, native-source and Story-output retention pressure, `UNKNOWN/defer` source-scope completeness, and the 10 KiB per-file rather than corpus-wide invariant.

**Current Senior disposition:** **PASS / CLOSED**.

---

### SR24-S1-04 — Story growth/sharding propagation and owner-item completeness gap

**Severity:** SIGNIFICANT

**Finding:** The SR24-S1-03 package consumed the current growth/sharding owner in the WP-24 artifacts but left two propagation/completeness defects:

1. current `DEV/PROJECT_MAP.md` did not explicitly route Story persistence/operability through `DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md`;
2. WP-24 framing did not explicitly preserve the owner-defined direct-LLM-facing artifact-shape policy and exact-archival oversize pre-admission edge.

**Owner reconstruction:** current exact owner text establishes:

```text
DIRECT LLM-FACING ARTIFACTS
~250 lines: preferred design ceiling
251–300 lines: review zone; prefer safe partitioning/smaller semantic unit
>300 lines: not acceptable normal steady-state unless an explicit reason shows
            bounded alternate retrieval is safe and semantic partitioning would be worse

CLASSIFICATION
line count = LLM/tooling ergonomics signal
line count != 10 KiB replacement
line count != byte measurement
line count != token-pressure proof
line count != latency SLA

EXACT ARCHIVAL EDGE
exact material must never be truncated/paraphrased merely to satisfy storage size
if an accepted exact archival scope can exceed one indivisible file,
owner/schema must define safe bounded partition/reconstruction semantics before admission
```

**Routing repair:** `DEV/PROJECT_MAP.md` now names the integration contract, baseline source-contract companion and growth/sharding owner together in the Story concern route and dependency hot path. This makes the growth/sharding owner discoverable from current routing without making the Project Map a semantic owner.

A Story integration-contract edit was considered and rejected as unnecessary propagation: the repaired Project Map now supplies the direct forward route, while the growth/sharding owner already states that it supplements the integration contract and preserves its semantics. Adding a duplicate normative pointer inside the integration contract is not required for discovery correctness and would broaden the write set without changing ownership.

**Task-Brief repair:** the current Source Manifest now preserves the line-count policy as **owner-supplied ergonomics/operability guidance**, not a token/latency SLA and not a substitute for the 10 KiB hard per-file cap. It also carries exact-material non-truncation and pre-admission bounded partition/reconstruction as a correctness requirement, without selecting a concrete representation.

**Worker disposition:** **REPAIR CANDIDATE / PENDING INDEPENDENT SENIOR RE-REVIEW**.

---

## 4. Original critic findings retained after correction

### F24-S1 — Accepted constraints risked being treated as optimization targets

**Severity:** SIGNIFICANT

Current framing keeps owner classes distinct: the 10,240-byte mutable runtime artifact cap is a per-file hard invariant; PO-003/WP-19 is a zero-extra-serial critical-path law; `RUNTIME.md` rejects a fixed turn time/token/step/complexity ceiling; Story partitionability and exact-archive pre-admission safety are required properties; direct-LLM-facing line thresholds are owner ergonomics guidance rather than a performance SLA.

**Disposition:** REPAIRED.

### F24-S2 — Current measurements could be mistaken for end-to-end gameplay proof

**Severity:** SIGNIFICANT

Existing scaffold/index sizes, physical CORE bytes, DEV tool timings or Connector probes remain non-equivalent to long-campaign gameplay latency/context/Story catch-up/contended publication behavior. The Story line-count policy is owner guidance, not measured token/latency evidence.

**Disposition:** REPAIRED.

### F24-S3 — Retained non-authoritative refs were underrepresented as a scale dimension

**Severity:** SIGNIFICANT

Retained refs remain an explicit scaling dimension; ordinary authority lookup must avoid all-ref enumeration; deletion remains unavailable under PO-006.

**Disposition:** REPAIRED.

### F24-S4 — Background-service assumptions required explicit negative dependency census

**Severity:** SIGNIFICANT

Current accepted Context/SAVE/collaboration/Story/cleanup owners expose no autonomous worker/heartbeat baseline. The Story growth owner introduces no scheduler, queue, lease or heartbeat.

**Disposition:** REPAIRED.

### F24-S5 — Publication cost needed retry/conflict amplification

**Severity:** SIGNIFICANT

Remote round trips, publication attempts, retry/conflict amplification and multi-chat churn remain first-class cost dimensions. Story publication/catch-up adds another bounded publication path but does not authorize an invented retry count.

**Disposition:** REPAIRED.

### F24-S6 — Architecture boundedness and deferred machine realization needed explicit separation

**Severity:** SIGNIFICANT

Current owners can require bounded partitionability, direct-LLM-facing shape guidance and exact-archive pre-admission reconstruction safety while concrete shard layout, file fan-out, catch-up latency and production corpus size remain unrealized evidence questions. These are not conflated.

**Disposition:** REPAIRED.

---

## 5. Original minor findings retained

### F24-M1 — WP-11 shard-space cardinality could be misread as repository fan-out

The 65,536 leaf-bucket route space remains selector geometry, not evidence of materialized file/directory count. **REPAIRED.**

### F24-M2 — DEV-wide audit scans could be mistaken for gameplay precedent

Broad DEV maintenance scans do not authorize ordinary gameplay or Story source-scope global scans. **REPAIRED.**

### F24-M3 — Story projection and retrospective acquisition need separate accounting

Producer catch-up/publication, retained corpus growth and consumer retrospective reads are distinct paths/owners. **REPAIRED.**

---

## 6. SR24-S1-04 whole-project critic rerun

After applying the propagation/completeness repair, the critic re-routed the complete Step-1 horizon through current `DEV/PROJECT_MAP.md`, current Story integration/baseline/growth owners and neighboring accepted consumers rather than checking only the named paragraphs.

### 6.1 Current routing / discoverability audit

The repaired `DEV/PROJECT_MAP.md` now provides two direct discovery surfaces for Story persistence/operability:

- a dedicated `Story / retrospective continuity / persistence operability` concern row naming the integration contract, baseline projection source contracts and growth/sharding owner;
- the Story dependency hot path, which explicitly routes persistence scale/operability through the growth/sharding owner.

Result:

```text
GROWTH_SHARDING_OWNER_DISCOVERABLE_FROM_CURRENT_PROJECT_MAP: YES
PROJECT_MAP_TREATED_AS_SEMANTIC_OWNER: NO
INTEGRATION_CONTRACT_FORWARD_REFERENCE_REQUIRED_FOR_DISCOVERY: NO
```

The integration contract remains unchanged because its semantic integration role remains correct and the current routing now points directly to the supplemental operability owner.

### 6.2 Growth/sharding owner item-level operability audit

The critic checked material owner requirements individually rather than accepting a thematic “sharding covered” statement:

| Owner requirement | Current WP-24 framing result |
|---|---|
| 10 KiB mutable Story file hard cap remains controlling | preserved as per-file hard invariant, not corpus quota |
| direct LLM-facing ~250 preferred design ceiling | preserved as owner ergonomics guidance |
| 251–300 direct LLM-facing review zone | preserved; safe partition/smaller semantic unit preferred where appropriate |
| >300 not normal steady state without explicit bounded-alternate-retrieval / anti-partition reason | preserved without converting to SLA |
| line count does not replace byte/token/host evidence | explicit |
| machine-facing structures may be denser when deterministic runtime consumption justifies it | not contradicted; no universal line rule is applied to machine-only structures |
| no unbounded campaign-growing mutable singleton as sole representation | preserved |
| deterministic bounded partition/rollover/compaction/root+subordinate path must exist | preserved as realization requirement; no concrete option selected |
| physical partition keys are not Story/native identity, chronology, eligibility, coverage or currentness | preserved through no-semantic-topology rule |
| known-ID direct routing / bounded discovery / no whole-corpus enumeration | preserved |
| partition transition must preserve publication/currentness/reference closure/coverage | retained as owner constraint; not redesigned here |
| compatibility-bearing physical changes must use Version Impact/migration law | not weakened; activation remains future realization work |
| direct retrospective consumer remains storage-topology-neutral | preserved |
| Story backlog remains derived/bounded per operation, with no worker/queue/heartbeat | preserved |
| exact material cannot be truncated/paraphrased for storage limit | explicit |
| potentially oversized indivisible exact scope requires bounded partition/reconstruction semantics before admission | explicit carried-forward requirement |
| concrete PROJECTION_STATE shard layout/index partition count/chapter layout/rollover threshold | **not selected** |

No item-level owner requirement material to WP-24 scale/operability was found missing after the repair.

### 6.3 Hidden-unbounded-path sweep

| Path | Current owner result | Repair critic disposition |
|---|---|---|
| new chat / substantial setup engine cache | complete exact-package CORE + two RULES routing files loaded once | finite current corpus; physical size measurement remains supporting-only |
| package switch engine cache | full invalidation + exact-target rebuild | event-driven bounded-to-package corpus; not ordinary-turn path |
| verified instruction-context loss | full rehydrate once after positive loss determination | event-driven bounded-to-package corpus |
| ordinary CORE use | already-loaded cache; no CORE reread merely for activation | structural fast-path law |
| known native owner read | exact route; no directory/index enumeration | structurally bounded by accepted design |
| role-context acquisition | typed finite expansion; no ordinary campaign/history scan | bounded by accepted design; realization/empirical proof later |
| durability closure | no whole campaign/WORLD/full Git-history closure scan | bounded by accepted design |
| LIVE authority lookup | bounded routing/claim metadata; no WORLD/all-ref/all-LIVE scan | bounded by accepted design |
| collaboration lookup | direct known-ID + completeness-protected companions; no global scheduler/index | bounded by accepted design |
| Story source-scope discovery | LOCAL plus selected LIVE origin/domain routing must prove requested scope complete | `UNKNOWN/defer` on unprovable completeness; global LIVE/Story scan forbidden |
| Story candidate enumeration | fixed registration + origin/lane/generation cursor; bounded frozen window | per-operation bounded; does not bound total backlog/corpus |
| Story backlog/catch-up | derived from source cursors vs coverage, bounded one window at a time | campaign-lifetime backlog may grow; catch-up outside gameplay critical path |
| native pre-projection retention | minimum sufficient native source/anchor or admitted equivalent survivor retained for MUST candidates | typed growth/cleanup pressure until projection |
| post-coverage Story retention | required Story account preserved while compatible coverage promise remains | corpus growth dimension distinct from native-source retention |
| direct LLM-facing Story file | independently retrievable semantic unit with owner line-count ergonomics | line guidance is shape/operability signal; not token/latency proof |
| exact archival scope | cannot be truncated/paraphrased for file cap | potentially oversized indivisible scope requires pre-admission bounded partition/reconstruction contract |
| Story physical growth collections | no campaign-growing singleton may lack bounded partition path | structural partitionability required; concrete layout deferred |
| retrospective read | Context Runtime typed bounded acquisition; no catch-up mutation/whole-history preload | read boundedness does not imply corpus boundedness |
| diagnostic operation | bounded to concrete question | bounded by accepted design |
| retained refs | authority lookup must not depend on all-ref scan; residue may grow | operational-scale surface remains |

No current owner requires a whole-campaign, whole-WORLD, all-ref, all-LIVE or whole-Story scan for ordinary correctness.

### 6.4 Direct-LLM shape / SLA classification audit

The line-count policy is preserved exactly in class, not only in numbers:

```text
~250 lines   = preferred design ceiling
251–300      = review zone
>300         = exceptional / not acceptable normal steady-state without owner-required reason

OWNER CLASS = LLM/tooling ergonomics + operability guidance
!= hard 10 KiB byte cap
!= token budget
!= latency SLA
!= throughput SLA
!= context-window guarantee
!= empirical host acceptance
```

The critic found no new numerical SLA introduced by the repair.

### 6.5 Exact-archival edge audit

The repaired framing now distinguishes two non-substitutable constraints:

```text
per-file storage constraint
    -> never authorizes truncation/paraphrase of exact material

possible exact scope > one indivisible file
    -> owner/schema must define bounded exact partition + reconstruction semantics BEFORE ADMISSION
```

This is not a request to choose a shard layout now. It is an admission-safety dependency that later Story physical realization/schema work must satisfy before accepting such a representation.

### 6.6 Critical-path / background-service audit

Current accepted Story laws preserve:

- no mandatory per-turn Story generation;
- no new serial gameplay LLM call solely for Story catch-up;
- no durable Chronicler queue, lease, worker state or heartbeat;
- no background scheduler/global cursor;
- Story lag does not block gameplay responses, SAVE or native recovery;
- retrospective reads do not trigger projection catch-up.

The direct-LLM file-shape and exact-archive pre-admission rules add no runtime liveness service and do not activate implementation.

### 6.7 Numerical/structural budget audit

| Value / constraint | Basis | Current classification |
|---|---|---|
| 120 seconds | no current owner | unsupported prior assertion removed; SR24-S1-01 PASS/CLOSED |
| PO-003 extra serial basis-capture work = 0 in stated L38 scope | WP-19 `WP19-L38/L39` | accepted structural critical-path law |
| 10,240 bytes | runtime mutable GitHub artifact owner + Story growth owner | accepted **per-file** hard invariant; not corpus quota |
| ~250 lines | Story growth/sharding owner | preferred direct-LLM-facing design ceiling; ergonomics guidance, not SLA |
| 251–300 lines | Story growth/sharding owner | review zone; ergonomics guidance, not SLA |
| >300 lines | Story growth/sharding owner | not acceptable normal direct-LLM-facing steady-state absent explicit owner-required safe reason; not SLA |
| 8 Story registrations | Story baseline projection source contracts | fixed source-contract inventory; not corpus-size/throughput limit |
| 65,536 route buckets | WP-11 route geometry | structural selector property, not performance budget |
| 370,728 B current CORE+RULES preload source corpus | exact earlier recovery measurement | narrow Class-A current-source measurement only; not production forecast |

No new latency, throughput, token, Story-record-count, corpus-size, shard-count, API-call or retry-count SLA is introduced.

### 6.8 Authority/reopen/activation audit

```text
R2.3 CONTEXT ARCHITECTURE REOPEN: NO
R2.4 FULL-CORE PRELOAD STRATEGY REOPEN: NO
R2.6 HOST TRANSPORT SELECTION REOPEN: NO
WP11 ROUTING/INDEX AUTHORITY REOPEN: NO
WP13 PUBLICATION AUTHORITY REOPEN: NO
WP16 LIVE AUTHORITY REOPEN: NO
WP17 COLLABORATION OWNER REOPEN: NO
WP18 STORY/DRAMATURG SEMANTICS REOPEN: NO
STORY BASELINE REGISTRATIONS REOPEN: NO
STORY RETROSPECTIVE CONSUMER SEMANTICS REOPEN: NO
STORY PHYSICAL SHARD LAYOUT SELECTED: NO
STORY IMPLEMENTATION ACTIVATED: NO
STORY REDESIGN ACTIVATED: NO
WP24 STEP2 ACTIVATED: NO
WP21 CLEANUP/RETIREMENT OWNER REOPEN: NO
PO-003 ZERO-EXTRA-SERIAL LAW REOPEN: NO
PO-006 REF-DELETION POLICY REOPEN: NO
```

The repair consumes and routes current owners without redesigning them.

### 6.9 Open-world rerun result

The critic did not stop at the named finding. It rechecked the current dependency graph for additional BLOCKING/SIGNIFICANT framing defects created or exposed by the propagation repair.

```text
NEW_BLOCKING_FINDINGS: 0
NEW_SIGNIFICANT_FINDINGS: 0
```

No unresolved owner conflict or new Product Owner decision was found.

---

## 7. Current Source Manifest result

The repaired Task Brief now covers all materially necessary Step-1 owner classes exposed by the original critic, Senior reviews and current Story-owner changes:

- process/program/PO authority;
- R2.7 scope owner;
- true PO-003/WP-19 performance owner;
- full-CORE preload/cache-rebuild/runtime fast-path owners;
- context/host/resource owners;
- storage/routing/HOT/publication owners;
- multiplayer/LIVE/collaboration owners;
- Story integration and retrospective consumers;
- Story baseline projection source-contract registrations directly;
- Story persistence growth/sharding/consumer-decoupling owner directly and discoverably from `DEV/PROJECT_MAP.md`;
- Story backlog, origin/domain/cursor fan-out and two-phase retention pressure;
- direct-LLM-facing artifact-shape ergonomics;
- exact-archive oversized-scope pre-admission safety;
- diagnostics/retention/ref residue;
- current CORE/RULES physical consumers;
- schema/scaffold/tool/test/CI routes;
- verification/empirical boundary;
- negative evidence and revisit triggers.

This does not claim repository-global semantic completeness or replace later Step-2 evidence extraction. It means the current Step-1 dependency subgraph is ready for independent Senior re-review without requiring the reviewer to discover these owner classes by corpus proofreading.

---

## 8. Final worker repair verdict

```text
SR24-S1-01: PASS / CLOSED
SR24-S1-02: PASS / CLOSED
SR24-S1-03: PASS / CLOSED
SR24-S1-04: REPAIR CANDIDATE / PENDING INDEPENDENT SENIOR RE-REVIEW
REPAIR_WHOLE_PROJECT_CRITIC_RERUN_COMPLETE: YES
REPAIR_RERUN_NEW_BLOCKING: 0
REPAIR_RERUN_NEW_SIGNIFICANT: 0
SOURCE_MANIFEST_COMPLETE_FOR_CURRENT_STEP1_REPAIR: YES
UNRESOLVED_BLOCKING_IN_WORKER_VIEW: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_VIEW: 0
HUMAN_DECISION_REQUIRED: NO
STEP2_AUTHORIZED: NO
NEXT_GATE: MANDATORY INDEPENDENT SENIOR RE-REVIEW OF SR24-S1-04 REPAIR PACKAGE
```

This is a worker repair result, **not** an independent Senior PASS for SR24-S1-04.

**STOP FOR MANDATORY INDEPENDENT SENIOR RE-REVIEW.**
