# R2.7 WP-24 Step 1 — Mandatory Whole-Project Critic

Status: **SENIOR HOLD RECOVERY CRITIC COMPLETE — SR24-S1-01 / SR24-S1-02 REPAIRS INSPECTED — MANDATORY INDEPENDENT SENIOR RE-REVIEW PENDING**

Date: 2026-09-08

Original Step-1 evidence basis: `1c3b85a509a592d0e11da6bc64d9119f5b543a4a`.

Senior-recovery evidence basis: `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`.

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-task-brief-source-manifest.md`.

This file is the mandatory Step-1 whole-project framing critic required by `DEV/ARCHITECTURE/DESIGN_PROCESS.md`, including the bounded rerun after mandatory independent Senior HOLD. It reconstructs the WP-24 dependency subgraph from `DEV/PROJECT_MAP.md` and current owners. It is not a Step-6 candidate-spec adversarial review and does not authorize Step 2.

---

## 1. Critic method

The critic does not accept the Task Brief's dependency list as authority. The original pass and Senior recovery rerun route the four canonical WP-24 questions through:

- current process/program/PO owners;
- PO-003/WP-19 performance owner chain;
- context/runtime/host and physical instruction-cache contracts;
- storage/routing/HOT/publication owners;
- LIVE/multiplayer/collaboration owners;
- Story/continuity/planning/retrospective consumers;
- diagnostics/cleanup/retention/ref-lifecycle owners;
- current CORE consumers and the exact current CORE/RULES physical corpus;
- schema/scaffold/tool/test/CI surfaces;
- WP-22 proof classification;
- explicit closed decisions and revisit triggers.

The rerun specifically searches again for scope omissions, duplicated/reopened authority, hidden unbounded hot paths, unsupported host assumptions, non-equivalent measurements, premature optimization, unsafe deferral, misclassified empirical obligations, unsupported numeric budgets and accepted constraints weakened by framing.

Finding severity means **framing risk for WP-24 Step 1**, not a claim that the final architecture contains the defect.

---

## 2. Review history and current summary

Original worker critic before first Senior review:

```text
ORIGINAL_BLOCKING_FOUND: 0
ORIGINAL_SIGNIFICANT_FOUND: 6
ORIGINAL_MINOR_FOUND: 3
ORIGINAL_WORKER_REPAIRS_APPLIED: YES
```

Mandatory independent Senior review then returned:

```text
WP24_STEP1_SENIOR_REVIEW: HOLD
SR24-S1-01: BLOCKING / OPEN
SR24-S1-02: SIGNIFICANT / OPEN
HUMAN_DECISION_REQUIRED_NOW: NO
WP24_STEP2_AUTHORIZED: NO
```

Bounded recovery/rerun result:

```text
SENIOR_BLOCKING_UNDER_RECOVERY: 1
SENIOR_SIGNIFICANT_UNDER_RECOVERY: 1
SENIOR_BLOCKING_REPAIRS_APPLIED: 1
SENIOR_SIGNIFICANT_REPAIRS_APPLIED: 1
RECOVERY_RERUN_NEW_BLOCKING_FOUND: 0
RECOVERY_RERUN_NEW_SIGNIFICANT_FOUND: 0
UNRESOLVED_BLOCKING_IN_WORKER_RECOVERY: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_RECOVERY: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
STEP2_AUTHORIZED: NO
```

These are worker recovery dispositions pending independent Senior re-review; they are not a Senior PASS claim.

---

## 3. Senior findings and recovery dispositions

### SR24-S1-01 — Unsupported `120 seconds` Product Owner law

**Severity:** BLOCKING

**Senior finding:** Published Step-1 artifacts treated `PLAY_NOW_T_BUDGET = 120 seconds` as an accepted PO-003 / `PLAY_POLICY.md` law, but current owning sources did not support that attribution.

**Recovery owner reconstruction:**

- `DEV/PRODUCT_OWNER_INPUT.md` PO-003 preserves the Product Owner interactivity concern and routes a mandatory zero-extra-serial performance law;
- WP-19 canonical `WP19-L38` defines the exact zero-extra-serial baseline for historical Actor decision-basis capture;
- WP-19 `WP19-L39` requires material architecture/performance escalation if later realization would add an extra serial LLM/tool round trip on ordinary gameplay critical path;
- the historical Actor decision-basis owner decision contains no 120-second SLA;
- `GAME/CORE/PLAY_POLICY.md` protects latency through local-first/decision-scoped work and contains no 120-second law;
- `GAME/CORE/RUNTIME.md` explicitly states that the reasoning-performance budget is a stop rule for unnecessary deliberation and **must not become a fixed token, time, step-count or complexity cap on a turn**;
- current canonical architecture navigation was inspected as a locator and exposed no current 120-second owner.

**Result:** **NO CURRENT OWNER FOUND** for the asserted 120-second Product Owner/turn law.

**Repair:**

1. remove `120 seconds`, `T_budget=120s` and the false PO-003/`PLAY_POLICY.md` attribution from current Task Brief framing, carried-forward questions and current progress;
2. preserve the actual PO-003/WP-19 law:

```text
additional sequential LLM calls solely for basis capture = 0
additional serial remote/tool reads solely for capture when required T0 data is already admitted = 0
additional separate remote publications solely for basis = 0
basis work on irrelevant/trivial/NO_CHANGE turns = 0
additional context/output = bounded typed material items only
```

3. preserve WP19-L39's explicit serial-cost escalation trigger;
4. preserve `RUNTIME.md`'s prohibition on a fixed turn reasoning cap;
5. invent no replacement numerical SLA.

**Conflict / human decision:** none. The false attribution is mechanically removable; current owners are reconcilable.

**Worker recovery disposition:** **REPAIRED / PENDING SENIOR RE-REVIEW**.

---

### SR24-S1-02 — Full-CORE preload / cache rebuild omitted

**Severity:** SIGNIFICANT

**Senior finding:** Step-1 framing discussed generic context loading but omitted the current physical runtime strategy in which complete local CORE instructions plus two RULES routing files are preloaded once, rebuilt after package switch or verified context loss, and not reread on ordinary turns.

**Recovery owner reconstruction:**

- `GAME/CORE/PLAY_POLICY.md` owns complete exact-package `CORE/*.md` + `RULES/INDEX.md` + `RULES/README.md` current-chat preload and zero ordinary CORE reread;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md` owns exact package selection, cache construction, package-switch invalidation/rebuild and verified-loss rehydration;
- `GAME/CORE/RUNTIME.md` consumes the already-loaded cache on the ordinary fast path;
- R2.4 `LAW R2.4-23` preserves full preloaded CORE physically present while activation/rebinding stays semantic;
- WP-09 `LAW WP09-1` explicitly separates the full engine instruction cache from bounded campaign/role context;
- `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md` C02/C04/C05/C06/C08/C09 encode scenario obligations for preload, loaded-not-active, no reread, scene-change persistence, package-switch rebuild and context-loss rehydration;
- WP-22 says scenario/static evidence does not establish empirical host/LLM performance and production-like evaluation belongs on the realized target.

**Repair:** Task Brief now splits four paths explicitly:

```text
NEW CHAT / SUBSTANTIAL SETUP
    -> full CORE + RULES routing preload

ENGINE PACKAGE SWITCH
    -> invalidate old instruction cache
    -> full target cache rebuild

VERIFIED CONTEXT LOSS / COMPACTION
    -> full cache rehydration

ORDINARY TURN
    -> already-loaded CORE
    -> zero CORE reread
```

It adds physical instruction-corpus file/byte/rebuild dimensions and keeps campaign Context Runtime separate.

**Class-A measurement on exact recovery basis `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`:**

```text
CORE/*.md file count                    45
aggregate CORE/*.md bytes              364,844 B
RULES/INDEX.md                           1,752 B
RULES/README.md                          4,132 B
total preload-source file count             47
total preload-source bytes             370,728 B
```

Largest relevant files are also recorded in the repaired Task Brief.

Measurement qualification:

```text
CURRENT PHYSICAL CORPUS MEASUREMENT ONLY
!= model token occupancy
!= prompt-pressure proof
!= user-visible latency benchmark
!= real-MVP empirical acceptance
```

No bytes-to-token conversion is inferred.

**Future evidence repair:** If full physical CORE preload remains the realized production strategy, preserve a real-target production-like evaluation comparing/controlling the strategy appropriately and inspecting behavioral prompt pressure, procedural verbosity/unnecessary checks or retrievals, GM/NPC initiative/improvisation, context/resource pressure, latency/tool-call amplification and gameplay quality/degradation. This is future Class C evidence on the real implemented supported target, not a preimplementation surrogate and not a current finding that preload must change.

**Worker recovery disposition:** **REPAIRED / PENDING SENIOR RE-REVIEW**.

---

## 4. Original critic findings retained after correction

### F24-S1 — Accepted constraints risked being treated as optimization targets

**Severity:** SIGNIFICANT

**Corrected finding:** WP-24 must not casually retune accepted performance/resource law. Current owners establish different kinds of constraint: the 10,240-byte mutable runtime artifact cap is a numerical hard invariant; PO-003/WP-19 is a zero-extra-serial critical-path law rather than a turn-time SLA; `RUNTIME.md` rejects a fixed turn time/token/step/complexity ceiling.

**Repair:** The settled-constraint matrix now preserves those actual owners/classes. The erroneous 120-second premise from the first critic is superseded by SR24-S1-01 recovery.

**Disposition:** REPAIRED.

### F24-S2 — Current measurements could be mistaken for end-to-end gameplay proof

**Severity:** SIGNIFICANT

**Finding:** Existing scaffold/index sizes, physical CORE bytes, DEV tool timings or prior Connector probes are non-equivalent to long-campaign gameplay latency/context/contended publication behavior.

**Repair:** Preserve explicit Class A/B/C separation:

```text
existing-surface measurement
!= realized implementation benchmark
!= real-MVP production-like empirical evaluation
```

**Disposition:** REPAIRED.

### F24-S3 — Retained non-authoritative refs were underrepresented as a scale dimension

**Severity:** SIGNIFICANT

**Finding:** PO-006 forbids automated branch/ref deletion, so residue may accumulate even though authority/currentness remains bounded.

**Repair:** Retained refs remain an explicit scaling dimension/audit question; ordinary authority lookup must avoid all-ref enumeration; deletion remains unavailable.

**Disposition:** REPAIRED.

### F24-S4 — Background-service assumptions required an explicit negative dependency census

**Severity:** SIGNIFICANT

**Finding:** The canonical horizon requires an owner-level negative dependency census, not merely absence of a worker file.

**Repair:** Current accepted Context/SAVE/collaboration/Story/cleanup owners expose no autonomous worker/heartbeat baseline. Recovery additionally confirms full-CORE preload/rebuild is foreground/event-driven, not autonomous.

**Disposition:** REPAIRED.

### F24-S5 — Publication cost needed retry/conflict amplification, not only nominal call count

**Severity:** SIGNIFICANT

**Finding:** Multi-chat currentness/conflict can multiply bounded remote operations.

**Repair:** Remote round trips, publication attempts, retry/conflict amplification and multi-chat churn remain first-class cost dimensions. No unsupported retry count is invented.

**Disposition:** REPAIRED.

### F24-S6 — Architecture boundedness and deferred machine realization needed explicit separation

**Severity:** SIGNIFICANT

**Finding:** Missing future machine/benchmark/evaluation work cannot automatically be called a current architecture defect, while accepted prose cannot be over-credited as realized proof.

**Repair:** Source Manifest retains `BOUNDED_BY_ACCEPTED_DESIGN`, `REALIZATION_DEBT_ALREADY_ROUTED`, `EMPIRICAL_AFTER_REALIZATION` and `MEASURE_NOW_SUPPORTING_ONLY`, with WP-22 proof power controlling claims.

**Disposition:** REPAIRED.

---

## 5. Original minor findings retained

### F24-M1 — WP-11 shard-space cardinality could be misread as repository fan-out

The 65,536 leaf-bucket route space is a selector space, not evidence that every campaign materializes that many files/directories. **REPAIRED.**

### F24-M2 — DEV-wide audit scans could be mistaken for gameplay precedent

Broad DEV maintenance work does not authorize ordinary gameplay full scans. **REPAIRED.**

### F24-M3 — Story projection and retrospective acquisition need separate accounting

Producer catch-up/publication and consumer retrospective reads remain distinct paths/owners. **REPAIRED.**

---

## 6. Recovery whole-project critic rerun

After applying SR24-S1-01/SR24-S1-02 framing repairs, the critic re-routed the repaired horizon through current `DEV/PROJECT_MAP.md` and actual owners/consumers rather than checking only the edited paragraphs.

### 6.1 Hidden unbounded-path sweep

| Path | Current owner result | Recovery critic disposition |
|---|---|---|
| new chat / substantial setup engine cache | complete exact-package CORE + two RULES routing files loaded once | finite current corpus; physical size measured; host/behavior cost empirical later |
| package switch engine cache | full invalidation + exact-target rebuild before adjudication | event-driven bounded-to-package corpus; not ordinary-turn path |
| verified instruction-context loss | full rehydrate once after positive loss determination | event-driven bounded-to-package corpus; host incidence/cost empirical later |
| ordinary CORE use | already-loaded cache; no disk/GitHub CORE reread for activation | structural fast-path law |
| known native owner read | WP-11/12 derives exact route; no directory/index enumeration | structurally bounded by accepted design |
| role-context acquisition | WP-09 typed finite expansion; no ordinary campaign/history scan | bounded by accepted design; realization/empirical proof later |
| durability closure | WP-13 no whole campaign/WORLD scan, broad directory enumeration or full Git history | bounded by accepted design |
| LIVE authority lookup | WP-16 bounded routing/claim metadata; no WORLD/all refs/all LIVE scan | bounded by accepted design |
| collaboration lookup | WP-17 direct known-ID + completeness-protected companions; no directory registry/scheduler baseline | bounded by accepted design; machine debt routed |
| Story backlog | WP-18 derived from compatible source enumeration + layer coverage; no durable queue | source-contract boundedness remains later WP-24 audit surface |
| retrospective reading | Story integration + Context Runtime typed capabilities; no implicit catch-up mutation | boundedness contract exists; realization/empirical proof later |
| diagnostic operation | WP-21 evidence bounded to concrete question | bounded by accepted design |
| retained refs | authority lookup must not depend on all-ref scan; physical residue may grow | operational-scale question remains legitimate WP-24 surface |
| monolithic family index | one expected family index for discovery | explicit measured WP-24 partition revisit trigger; not fired by current scaffold |

No recovery evidence establishes that ordinary correctness requires a whole-campaign, whole-WORLD, all-ref or all-LIVE scan.

### 6.2 Unsupported-host / autonomous-liveness sweep

Current accepted profile remains ordinary ChatGPT chat with fixed connected GitHub transport. The inspected owners continue to avoid autonomous liveness:

- no exact hidden-context telemetry dependency;
- no background context service;
- no clean SAVE heartbeat;
- no collaboration scheduler/presence heartbeat;
- no Chronicler worker/heartbeat/queue requirement;
- no background cleanup queue;
- no automatic branch/ref deletion process;
- full-CORE cache construction/rebuild is event-driven foreground work, not a background service.

This is architectural negative evidence, not empirical proof of acceptable runtime latency or prompt pressure.

### 6.3 Proof-class rerun

`DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md` can preserve scenario obligations for full preload/no-reread/rebuild behavior, but under WP-22 it does not prove:

- actual model-context occupancy;
- behavioral prompt pressure;
- user-visible latency;
- GM/NPC initiative or improvisation quality;
- absence of unnecessary procedural checks/retrievals;
- real multi-chat/Connector behavior.

The Task Brief now routes those claims to real-target Class C evaluation after realization. No fake parallel MVP was introduced.

### 6.4 Numerical/structural budget audit

| Value / constraint | Basis | Recovery classification |
|---|---|---|
| 120 seconds | **no current owner found** | unsupported prior assertion removed; not a current WP-24 law |
| PO-003 basis capture: added sequential LLM call/read/publication/irrelevant-turn work = 0 in the stated L38 scope | WP-19 `WP19-L38/L39` + PO-003 routing | accepted structural critical-path law, scope-qualified |
| 10,240 bytes | runtime mutable GitHub artifact Product Owner decision | accepted runtime operability hard invariant |
| 65,536 route buckets | WP-11 deterministic route geometry | structural routing property, not performance budget |
| 364,844 B CORE + 5,884 B routing = 370,728 B preload sources | exact current GAME corpus metadata at recovery basis | narrow Class-A physical-source measurement only |
| current scaffold index byte sizes | exact current GitHub metadata | narrow Class-A scaffold measurement only |

No new latency, throughput, token, file-count, API-call, retry-count or cardinality SLA is introduced.

### 6.5 Authority-reopen audit

```text
R2.3 CONTEXT ARCHITECTURE REOPEN: NO
R2.4 FULL-CORE PRELOAD STRATEGY REOPEN: NO AT STEP-1 RECOVERY
R2.6 HOST TRANSPORT SELECTION REOPEN: NO
WP11 ROUTING/INDEX AUTHORITY REOPEN: NO
WP13 PUBLICATION AUTHORITY REOPEN: NO
WP16 LIVE AUTHORITY REOPEN: NO
WP17 COLLABORATION OWNER REOPEN: NO
WP18 STORY/DRAMATURG OWNER REOPEN: NO
WP21 CLEANUP/RETIREMENT OWNER REOPEN: NO
PO-003 ZERO-EXTRA-SERIAL LAW REOPEN: NO
PO-006 REF-DELETION POLICY REOPEN: NO
```

The recovery adds the full-CORE physical cost/evaluation horizon without choosing an alternate loading strategy. WP-11 index partitioning remains an explicitly delegated later choice only if its measured trigger fires.

---

## 7. Recovery Source Manifest result

The repaired Task Brief now covers all materially necessary Step-1 owner classes exposed by the original critic, Senior review and recovery rerun:

- process/program/PO authority;
- R2.7 scope owner;
- true PO-003/WP-19 performance owner;
- full-CORE preload/cache-rebuild/runtime fast-path owners;
- context/host/resource owners;
- storage/routing/HOT/publication owners;
- multiplayer/LIVE/collaboration owners;
- Story/planning/retrospective consumers;
- diagnostics/retention/ref residue;
- current CORE/RULES physical consumers;
- schema/scaffold/tool/test/CI routes;
- verification/empirical boundary;
- negative evidence and revisit triggers.

Recovery rerun discovered **0 additional BLOCKING** and **0 additional SIGNIFICANT** framing findings beyond SR24-S1-01/SR24-S1-02.

This does not claim repository-global semantic completeness or replace later Step-2 evidence extraction. It means the repaired Step-1 dependency subgraph is ready for independent Senior re-review without asking the human reviewer to discover these owner classes by corpus proofreading.

---

## 8. Final worker recovery verdict

```text
WP24_STEP1_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD
SR24-S1-01: REPAIR APPLIED / PENDING SENIOR RE-REVIEW
SR24-S1-02: REPAIR APPLIED / PENDING SENIOR RE-REVIEW
RECOVERY_WHOLE_PROJECT_CRITIC_RERUN_COMPLETE: YES
RECOVERY_RERUN_NEW_BLOCKING: 0
RECOVERY_RERUN_NEW_SIGNIFICANT: 0
SOURCE_MANIFEST_COMPLETE_FOR_REPAIRED_STEP1: YES
UNRESOLVED_BLOCKING_IN_WORKER_RECOVERY: 0
UNRESOLVED_SIGNIFICANT_IN_WORKER_RECOVERY: 0
HUMAN_DECISION_REQUIRED: NO
STEP2_AUTHORIZED: NO
NEXT_GATE: MANDATORY INDEPENDENT SENIOR RE-REVIEW OF REPAIRED WP-24 STEP 1
```

This is a worker recovery result, **not** an independent Senior PASS.

**STOP FOR MANDATORY INDEPENDENT SENIOR RE-REVIEW.**
