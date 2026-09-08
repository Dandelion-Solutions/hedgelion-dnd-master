# R2.7 WP-24 Step 1 — Mandatory Whole-Project Critic

Status: **SR24-S1-03 MICRO-RECOVERY CRITIC COMPLETE — SR24-S1-01 / SR24-S1-02 PASS/CLOSED — MANDATORY INDEPENDENT SENIOR RE-REVIEW PENDING**

Date: 2026-09-08

Original Step-1 evidence basis: `1c3b85a509a592d0e11da6bc64d9119f5b543a4a`.

Primary Senior-recovery evidence basis: `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`.

SR24-S1-03 micro-recovery evidence basis: `83d018e42db9fa35a900f3b961f69edbee2a3d8e`.

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-task-brief-source-manifest.md`.

This file is the mandatory Step-1 whole-project framing critic required by `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, including the rerun after the new current Story baseline projection and persistence-growth owners entered the dependency graph. It is not a Step-6 candidate-spec adversarial review and does not authorize Step 2.

---

## 1. Critic method

The critic does not accept the Task Brief's dependency list as authority. The current rerun reconstructs the WP-24 dependency subgraph from current `DEV/PROJECT_MAP.md` and actual owners/consumers, including owners published after the earlier recovery checkpoint.

The four canonical WP-24 questions are routed through:

- current process/program/PO owners;
- PO-003/WP-19 performance owner chain;
- context/runtime/host and physical instruction-cache contracts;
- storage/routing/HOT/publication owners;
- LIVE/multiplayer/collaboration owners;
- Story/continuity/planning/retrospective consumers;
- the Story integration contract plus its current baseline projection-source companion;
- the Story persistence-growth/sharding/consumer-decoupling owner decision;
- diagnostics/cleanup/retention/ref-lifecycle owners;
- current CORE consumers and the exact current CORE/RULES physical corpus;
- schema/scaffold/tool/test/CI surfaces;
- WP-22 proof classification;
- explicit closed decisions and revisit triggers.

The rerun searches for scope omissions, duplicated/reopened authority, hidden unbounded hot paths, unsupported host assumptions, non-equivalent measurements, premature optimization, unsafe deferral, misclassified empirical obligations, unsupported numeric budgets and accepted constraints weakened by framing.

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

The bounded recovery repaired those two findings. Current Senior disposition entering this micro-recovery is:

```text
SR24-S1-01: PASS / CLOSED
SR24-S1-02: PASS / CLOSED
SR24-S1-03: MICRO-RECOVERY REQUIRED
WP24_STEP2_AUTHORIZED: NO
```

Current micro-recovery rerun result:

```text
SR24-S1-03_REPAIR_APPLIED: YES
MICRO_RECOVERY_RERUN_NEW_BLOCKING_FOUND: 0
MICRO_RECOVERY_RERUN_NEW_SIGNIFICANT_FOUND: 0
UNRESOLVED_BLOCKING_IN_WORKER_VIEW: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_VIEW: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
STEP2_AUTHORIZED: NO
```

This is a worker micro-recovery disposition pending independent Senior re-review; it is not a Senior PASS claim for SR24-S1-03.

---

## 3. Senior findings and recovery dispositions

### SR24-S1-01 — Unsupported `120 seconds` Product Owner law

**Original severity:** BLOCKING

The earlier recovery established that no current owner defines a `120 seconds` / `T_budget=120s` Product Owner turn law. The actual PO-003/WP-19 law is zero-extra-serial basis capture in its stated scope, and `GAME/CORE/RUNTIME.md` rejects a fixed token/time/step/complexity turn ceiling.

**Current Senior disposition:** **PASS / CLOSED**.

The micro-recovery found no new Story owner that changes this result.

---

### SR24-S1-02 — Full-CORE preload / cache rebuild omitted

**Original severity:** SIGNIFICANT

The earlier recovery split initial full CORE+RULES preload, package-switch cache rebuild, verified-loss rehydration and ordinary-turn zero CORE reread; it also classified the measured `370,728 B` current source corpus as Class A only, not a forecast or production sizing baseline.

**Current Senior disposition:** **PASS / CLOSED**.

The micro-recovery found no new Story owner that changes this result.

---

### SR24-S1-03 — Current Story baseline scale/performance owner omitted

**Finding:** After the main recovery, current Story authority changed materially for WP-24 framing. `DEV/PROJECT_MAP.md` and the Story integration contract now route production projection semantics through `DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md`. Current HEAD additionally contains `DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md`. The prior WP-24 Source Manifest referenced only the older integration contract at this scale boundary and therefore under-specified concrete corpus/backlog/retention/fan-out obligations.

**Current-owner reconstruction:** the baseline companion fixes eight registrations:

```text
T-MSG  TRANSCRIPT / participant messages
T-ARCH TRANSCRIPT / accepted exact-archival requests
E-EVT  EVENTS / SemanticEvents
E-REL  EVENTS / historical relations
M-SEG  MECHANICS / committed segment facts
M-OUT  MECHANICS / terminal gameplay outcomes
N-EVT  NARRATIVE / SemanticEvents
N-REL  NARRATIVE / historical relations
```

The same native SemanticEvent candidates feed E-EVT and N-EVT but their Story progress is independent. Historical relations likewise feed E-REL and N-REL independently. Native origin is `LOCAL` or `LIVE:<native live epoch id>` and each lane/origin has its own append-monotonic cursor. Source routing must prove the requested scope complete; inability to do so returns `UNKNOWN/defer`, not all-LIVE/all-Story enumeration and not a false caught-up declaration.

The baseline companion also establishes that:

- bounded candidate windows cap one operation, not campaign-lifetime Story growth;
- every admitted nontechnical SemanticEvent and historical relation is retained in both EVENTS and NARRATIVE subject to their independent obligations;
- there is no corpus-wide Story size quota or requirement to minimize Story record count;
- MUST candidates create native-source survivor/protection pressure until required output exists or an admitted equivalent survivor is present;
- once required output establishes compatible coverage, the required Story account remains retained unless compatible replacement/migration/end-of-promise semantics preserve the contract;
- catch-up may lag and does not block gameplay responses, SAVE or recovery.

The new Story persistence-growth owner further establishes:

- `RUNTIME_MUTABLE_GITHUB_TEXT_FILE_MAX_BYTES = 10240` remains a **per-file** hard invariant, not a corpus quota;
- no campaign-growing mutable Story collection may rely on an ever-growing singleton as its only supported representation;
- every plausibly unbounded collection requires a deterministic bounded partition path before the current form becomes a dead end;
- physical sharding must preserve known-ID direct routing, bounded discovery, publication/currentness, reference closure and projection-coverage semantics;
- retrospective consumers remain storage-topology-neutral;
- concrete shard/page/count/layout choices remain later implementation/performance evidence work and are not selected by this recovery.

**Repair applied:** the Task Brief now includes both Story owners directly, adds the eight-registration/origin-domain/cursor geometry, separates bounded per-operation windows from total corpus growth, separates native pre-projection retention from post-coverage Story retention, treats catch-up as outside ordinary gameplay critical path, preserves `UNKNOWN/defer` rather than global scan, and carries the new partitionability owner without selecting a Story redesign.

**Worker disposition:** **REPAIR CANDIDATE / PENDING INDEPENDENT SENIOR RE-REVIEW**.

---

## 4. Original critic findings retained after correction

### F24-S1 — Accepted constraints risked being treated as optimization targets

**Severity:** SIGNIFICANT

Current framing keeps owner classes distinct: the 10,240-byte mutable runtime artifact cap is a per-file hard invariant; PO-003/WP-19 is a zero-extra-serial critical-path law; `RUNTIME.md` rejects a fixed turn time/token/step/complexity ceiling; Story partitionability is a required future realization property while concrete partition thresholds/layouts remain evidence-driven.

**Disposition:** REPAIRED.

### F24-S2 — Current measurements could be mistaken for end-to-end gameplay proof

**Severity:** SIGNIFICANT

Existing scaffold/index sizes, physical CORE bytes, DEV tool timings or Connector probes remain non-equivalent to long-campaign gameplay latency/context/Story catch-up/contended publication behavior. The current Story registration/sharding documents are specification law, not realized Story corpus measurements.

**Disposition:** REPAIRED.

### F24-S3 — Retained non-authoritative refs were underrepresented as a scale dimension

**Severity:** SIGNIFICANT

Retained refs remain an explicit scaling dimension; ordinary authority lookup must avoid all-ref enumeration; deletion remains unavailable under PO-006.

**Disposition:** REPAIRED.

### F24-S4 — Background-service assumptions required explicit negative dependency census

**Severity:** SIGNIFICANT

Current accepted Context/SAVE/collaboration/Story/cleanup owners expose no autonomous worker/heartbeat baseline. The new Story baseline explicitly retains bounded turn-local catch-up without queue/worker/global cursor, and the Story growth owner introduces no scheduler/queue/heartbeat.

**Disposition:** REPAIRED.

### F24-S5 — Publication cost needed retry/conflict amplification

**Severity:** SIGNIFICANT

Remote round trips, publication attempts, retry/conflict amplification and multi-chat churn remain first-class cost dimensions. Story publication/catch-up adds another bounded publication path but does not authorize an invented retry count.

**Disposition:** REPAIRED.

### F24-S6 — Architecture boundedness and deferred machine realization needed explicit separation

**Severity:** SIGNIFICANT

Current owners can require bounded partitionability and bounded source windows while concrete shard layout, file fan-out, catch-up latency and production corpus size remain unrealized evidence questions. These are not conflated.

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

## 6. SR24-S1-03 whole-project critic rerun

After applying the micro-recovery framing repair, the critic re-routed the complete Step-1 horizon through current `DEV/PROJECT_MAP.md`, current Story integration/baseline/growth owners and neighboring accepted consumers rather than checking only the new paragraphs.

### 6.1 Hidden-unbounded-path sweep

| Path | Current owner result | Micro-recovery critic disposition |
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
| Story E/N semantic event projection | E-EVT and N-EVT independently cover same native candidate stream | two separate projection obligations; no E coverage substitution for N |
| Story E/N relation projection | E-REL and N-REL independently cover same native relation stream | two separate projection obligations; no lower-layer substitution |
| Story backlog/catch-up | derived from source cursors vs coverage, bounded one window at a time | campaign-lifetime backlog may grow; catch-up outside gameplay critical path |
| native pre-projection retention | minimum sufficient native source/anchor or admitted equivalent survivor retained for MUST candidates | typed growth/cleanup pressure until projection; no whole-record retention by default |
| post-coverage Story retention | required Story account preserved while compatible coverage promise remains | corpus growth dimension distinct from native-source retention |
| Story physical growth collections | no campaign-growing singleton may lack bounded partition path | structural partitionability required; concrete layout deferred |
| retrospective read | Context Runtime typed bounded acquisition; no catch-up mutation/whole-history preload | read boundedness does not imply corpus boundedness |
| diagnostic operation | bounded to concrete question | bounded by accepted design |
| retained refs | authority lookup must not depend on all-ref scan; residue may grow | operational-scale surface remains |
| monolithic native family index | expected family index baseline | measured WP-24 partition trigger remains; no current activation inferred |

No current owner requires a whole-campaign, whole-WORLD, all-ref, all-LIVE or whole-Story scan for ordinary correctness. The newly explicit Story corpus can be unbounded in **total retained cardinality** while all individual acquisition/catch-up operations remain bounded; that is now represented as a first-class WP-24 scale property rather than hidden behind the word “bounded.”

### 6.2 Story fan-out / retention audit

The critic checked the user-visible “eight registrations” statement against the current baseline companion and found exactly eight fixed production dispatch registrations. That number is a contract inventory, not a throughput/cardinality SLA.

Fan-out is not merely eight static files:

```text
registration
× native origin (LOCAL or selected LIVE epoch)
× lane/domain generation
× independent coverage cursor
```

E-EVT/N-EVT and E-REL/N-REL intentionally duplicate projection obligation over shared native enumeration because EVENTS and NARRATIVE have independent readable outputs/coverage. This may increase backlog/publication/storage pressure but cannot be optimized away by treating one layer as satisfying the other.

Retention pressure is two-phase:

```text
before required projection:
    native minimum sufficient source/anchor or admitted equivalent survivor must remain

after compatible coverage:
    required Story output/account must remain or be compatibly replaced/migrated/ended
```

The critic therefore rejects any framing that treats successful projection as automatic total storage release, or native compaction as permission to lose required projection material before coverage.

### 6.3 Per-file cap / corpus-growth audit

```text
10 KiB mutable runtime text invariant
    = per-file publication constraint
    != total Story corpus quota
```

The baseline source-contract owner explicitly permits retained Story corpus growth with campaign history. The Story growth/sharding owner closes the corresponding physical-operability hole by requiring deterministic bounded partitionability for every plausibly unbounded collection, while leaving concrete partition mechanics to later evidence/realization work.

This is not permission to choose a shard layout in Step 1 and not evidence that current Story implementation has already met the requirement.

### 6.4 Critical-path / background-service audit

Current accepted Story laws preserve:

- no mandatory per-turn Story generation;
- no new serial gameplay LLM call solely for Story catch-up;
- no durable Chronicler queue, lease, worker state or heartbeat;
- no background scheduler/global cursor;
- Story lag does not block gameplay responses, SAVE or native recovery;
- retrospective reads do not trigger projection catch-up.

Therefore backlog/catch-up cost is a separate WP-24 operational path, not an implicit ordinary-turn tax. Later implementation may still need performance evidence for explicit catch-up invocations/publications, but Step 1 does not invent an autonomous service to pay that cost.

### 6.5 Source-scope completeness audit

The current baseline companion explicitly closes a prior temptation toward broad discovery:

```text
if native campaign/live routing proves requested source-scope set complete:
    operate over that finite declared scope
else:
    UNKNOWN/defer the completeness claim
```

It is invalid to recover completeness by scanning all LIVE refs, all Story records or an incomplete source set and calling it caught up. This composes with WP-11/WP-16 no-global-enumeration laws rather than reopening them.

### 6.6 Numerical/structural budget audit

| Value / constraint | Basis | Current classification |
|---|---|---|
| 120 seconds | no current owner | unsupported prior assertion removed; SR24-S1-01 PASS/CLOSED |
| PO-003 extra serial basis-capture work = 0 in stated L38 scope | WP-19 `WP19-L38/L39` | accepted structural critical-path law |
| 10,240 bytes | runtime mutable GitHub artifact owner + Story growth owner | accepted **per-file** hard invariant; not corpus quota |
| 8 Story registrations | Story baseline projection source contracts | fixed source-contract inventory; not a corpus-size/throughput limit |
| 65,536 route buckets | WP-11 route geometry | structural selector property, not performance budget |
| 370,728 B current CORE+RULES preload source corpus | exact earlier recovery measurement | narrow Class-A current-source measurement only; not production forecast |

The Story growth owner also supplies direct-LLM-facing line-count ergonomics, but those are consumer-shape design signals under that owner, not a replacement for byte/token/latency evidence and not a corpus quota.

No new latency, throughput, token, Story-record-count, corpus-size, shard-count, API-call or retry-count SLA is introduced.

### 6.7 Authority-reopen audit

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
WP21 CLEANUP/RETIREMENT OWNER REOPEN: NO
PO-003 ZERO-EXTRA-SERIAL LAW REOPEN: NO
PO-006 REF-DELETION POLICY REOPEN: NO
```

The micro-recovery consumes new current Story owners without redesigning them.

### 6.8 Open-world rerun result

The critic did not stop at the named finding. It rechecked the current dependency graph for additional BLOCKING/SIGNIFICANT framing defects created or exposed by the new Story owners.

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
- Story persistence growth/sharding/consumer-decoupling owner directly;
- Story backlog, origin/domain/cursor fan-out and two-phase retention pressure;
- diagnostics/retention/ref residue;
- current CORE/RULES physical consumers;
- schema/scaffold/tool/test/CI routes;
- verification/empirical boundary;
- negative evidence and revisit triggers.

This does not claim repository-global semantic completeness or replace later Step-2 evidence extraction. It means the current Step-1 dependency subgraph is ready for independent Senior re-review without requiring the reviewer to discover these owner classes by corpus proofreading.

---

## 8. Final worker micro-recovery verdict

```text
SR24-S1-01: PASS / CLOSED
SR24-S1-02: PASS / CLOSED
SR24-S1-03: REPAIR CANDIDATE / PENDING INDEPENDENT SENIOR RE-REVIEW
MICRO_RECOVERY_WHOLE_PROJECT_CRITIC_RERUN_COMPLETE: YES
MICRO_RECOVERY_RERUN_NEW_BLOCKING: 0
MICRO_RECOVERY_RERUN_NEW_SIGNIFICANT: 0
SOURCE_MANIFEST_COMPLETE_FOR_CURRENT_STEP1_MICRO_RECOVERY: YES
UNRESOLVED_BLOCKING_IN_WORKER_VIEW: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_VIEW: 0
HUMAN_DECISION_REQUIRED: NO
STEP2_AUTHORIZED: NO
NEXT_GATE: MANDATORY INDEPENDENT SENIOR RE-REVIEW OF SR24-S1-03 MICRO-RECOVERY PACKAGE
```

This is a worker micro-recovery result, **not** an independent Senior PASS for SR24-S1-03.

**STOP FOR MANDATORY INDEPENDENT SENIOR RE-REVIEW.**
