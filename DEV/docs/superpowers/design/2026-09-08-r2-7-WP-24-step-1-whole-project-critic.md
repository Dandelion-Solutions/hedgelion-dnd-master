# R2.7 WP-24 Step 1 — Mandatory Whole-Project Critic

Status: **CRITIC COMPLETE — ALL MECHANICALLY RESOLVABLE BLOCKING/SIGNIFICANT FRAMING FINDINGS REPAIRED — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-08

Evidence basis: `1c3b85a509a592d0e11da6bc64d9119f5b543a4a`.

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-task-brief-source-manifest.md`.

This critic is the mandatory Step-1 whole-project framing review required by `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. It independently reconstructs the WP-24 dependency subgraph from `DEV/PROJECT_MAP.md` and current owners. It is not a Step-6 candidate-spec adversarial review and does not authorize Step 2.

---

## 1. Independent critic method

The critic did not accept the Task Brief's initial dependency list as complete. It re-routed the four canonical WP-24 questions through:

- current process/program/PO owners;
- context/runtime/host contracts;
- storage/routing/HOT/publication owners;
- LIVE/multiplayer/collaboration owners;
- Story/continuity/planning/retrospective consumers;
- diagnostics/cleanup/retention/ref-lifecycle owners;
- current CORE consumers;
- schema/scaffold/tool/test/CI surfaces;
- WP-22 proof classification;
- explicit closed decisions and revisit triggers.

The critic specifically searched for scope omissions, duplicated/reopened authority, hidden unbounded hot paths, unsupported host assumptions, non-equivalent measurements, premature optimization, unsafe deferral, misclassified empirical obligations, unsupported numeric budgets and accepted constraints weakened by framing.

Finding severity means **framing risk for WP-24 Step 1**, not a claim that the final architecture contains the defect.

---

## 2. Summary

```text
BLOCKING_FOUND: 0
SIGNIFICANT_FOUND: 6
MINOR_FOUND: 3

BLOCKING_RESOLVED: 0
SIGNIFICANT_RESOLVED: 6
MINOR_RESOLVED: 3

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
UNRESOLVED_MINOR: 0

HUMAN_DECISION_REQUIRED: NO
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
STEP2_AUTHORIZED: NO
```

The initial framing was directionally correct but required six material repairs before it was safe for Senior review.

---

## 3. Significant findings and repairs

### F24-S1 — Accepted numerical laws risked being treated as WP-24 optimization targets

**Severity:** SIGNIFICANT

**Finding:** A generic performance audit can accidentally treat all numeric values as candidates for tuning. Current owners already establish two different classes of numeric law: PO-003's 120-second PLAY NOW budget and the 10,240-byte mutable runtime GitHub text artifact cap. Re-selecting either value would duplicate Product Owner authority and could weaken already accepted operability requirements.

**Evidence owners:** `DEV/PRODUCT_OWNER_INPUT.md`, `GAME/CORE/PLAY_POLICY.md`, runtime mutable artifact-size owner decision.

**Repair:** Added the settled-constraint matrix and explicit rule that WP-24 consumes these values as law, audits realization against them and introduces no replacement number without a genuine later Product Owner residual.

**Disposition:** REPAIRED.

---

### F24-S2 — Current measurements could be mistaken for end-to-end gameplay proof

**Severity:** SIGNIFICANT

**Finding:** Existing scaffold/index sizes, DEV tool timings or prior Connector probes are non-equivalent to long-campaign gameplay latency/context/contended publication behavior. Without an explicit evidence taxonomy, a convenient current measurement could falsely close a future empirical obligation.

**Evidence owners:** R2.6 MVP Host Assurance, WP-22 verification/evaluation completeness, Story integration contract.

**Repair:** Added explicit Class A/B/C evidence separation:

```text
existing-surface measurement
!= realized implementation benchmark
!= real-MVP production-like empirical evaluation
```

The current scaffold measurement is narrowly labelled and no preimplementation surrogate is authorized.

**Disposition:** REPAIRED.

---

### F24-S3 — Retained non-authoritative refs were underrepresented as a scale dimension

**Severity:** SIGNIFICANT

**Finding:** PO-006 forbids automated branch/ref deletion. Therefore long-lived campaigns can accumulate non-authoritative refs even though authority/currentness remains bounded. A performance audit that omits repository residue could miss listing/discovery/tool pressure; an audit that tries to solve it with deletion would violate Product Owner law.

**Evidence owners:** branch/ref deletion prohibition owner decision; WP-21 logical retirement/diagnostics owner; WP-16 LIVE authority lookup.

**Repair:** Added retained refs as an explicit scaling dimension and audit question. The brief requires proving ordinary authority lookup avoids all-ref enumeration and preserves logical retirement; deletion remains unavailable unless a later explicit Product Owner supersession occurs.

**Disposition:** REPAIRED.

---

### F24-S4 — Background-service assumptions required an explicit negative dependency census

**Severity:** SIGNIFICANT

**Finding:** The canonical WP-24 horizon asks whether accepted design relies on polling/workers/heartbeats unavailable in the target product. Merely failing to find a `worker` file is insufficient. The critic had to inspect semantic owners for hidden liveness assumptions.

**Evidence:** WP-09 ephemeral context control/no background service; WP-13 no clean save heartbeat; WP-17 no scheduler/presence heartbeat/global registry; WP-18 no Chronicler queue/lease/heartbeat/worker state; WP-21 no background cleanup queue/service; R2.6 ordinary user-request/assistant-turn host profile.

**Repair:** Added an explicit background-service census and carried a negative-dependency sweep into later research. Current result: no accepted baseline architecture inspected requires autonomous background polling/worker/heartbeat execution for correctness.

**Disposition:** REPAIRED.

---

### F24-S5 — Publication cost needed retry/conflict amplification, not only nominal call count

**Severity:** SIGNIFICANT

**Finding:** Counting only the happy-path publication operations can substantially understate multi-chat cost. WP-13/WP-16 compose source-currentness checks, preflight, tree/commit/ref transitions, exact-source CAS, conflict classification, targeted verification and rebuild/revalidation. Contention can multiply serial remote round trips even when every individual attempt is structurally bounded.

**Evidence owners:** WP-13 durability/publication; WP-16 exact-source LIVE CAS; WP-17 collaboration currentness; `GAME/CORE/PERSISTENCE.md`/`MULTIPLAYER.md`.

**Repair:** Added remote round trips, publication attempts, retry/conflict amplification and multi-chat currentness churn as first-class structural cost dimensions and hot-path questions. No new retry count or SLA is invented at Step 1.

**Disposition:** REPAIRED.

---

### F24-S6 — Architecture boundedness and deferred machine realization needed explicit separation

**Severity:** SIGNIFICANT

**Finding:** Several accepted owners deliberately leave exact machine representation, benchmark or production-like acceptance to later implementation. Treating absence of an executable current surface as a current architecture defect would manufacture work; treating accepted prose as implementation proof would be equally wrong.

**Evidence owners:** WP-09/WP-12/WP-17/WP-18 integration contracts, WP-22 proof taxonomy, current `DEV/SCHEMAS`/CORE/test/tool surfaces.

**Repair:** Added Source-Manifest dispositions for `BOUNDED_BY_ACCEPTED_DESIGN`, `REALIZATION_DEBT_ALREADY_ROUTED`, `EMPIRICAL_AFTER_REALIZATION` and `MEASURE_NOW_SUPPORTING_ONLY`. Later WP-24 work must identify which missing machine bounds actually block a bounded implementation rather than equating all deferred realization with architecture failure.

**Disposition:** REPAIRED.

---

## 4. Minor findings and repairs

### F24-M1 — WP-11 shard-space cardinality could be misread as repository fan-out

**Finding:** The 65,536 leaf-bucket route space is a deterministic selector space, not evidence that a campaign materializes 65,536 directories/files.

**Repair:** Added an explicit qualification to the measurement section.

**Disposition:** REPAIRED.

### F24-M2 — DEV-wide audit scans could be mistaken for gameplay precedent

**Finding:** `run_maintenance_audit.py` and other DEV tooling may legitimately scan broad repository surfaces. Their operational class differs from ordinary gameplay and cannot authorize a runtime full scan.

**Repair:** Added explicit tool/proof qualification.

**Disposition:** REPAIRED.

### F24-M3 — Story projection cost and retrospective read cost needed separate accounting

**Finding:** Story growth could be discussed as one generic “history” cost even though producer catch-up/publication and consumer retrospective acquisition have different owners and hot paths.

**Repair:** Split Story source enumeration/projection publication from retrospective Context Runtime acquisition; reading does not require catch-up mutation.

**Disposition:** REPAIRED.

---

## 5. Hidden unbounded-path sweep

The critic examined the principal ordinary-operation paths for explicit or implicit broad enumeration.

| Path | Current owner result | Step-1 critic disposition |
|---|---|---|
| known native owner read | WP-11/12 derives exact route; no directory/index enumeration | structurally bounded by accepted design |
| role-context acquisition | WP-09 typed finite expansion; no ordinary campaign/history scan | bounded by accepted design; realization/empirical proof later |
| durability closure | WP-13 no whole campaign/WORLD scan, broad directory enumeration or full Git history | bounded by accepted design |
| LIVE authority lookup | WP-16 bounded routing/claim metadata; no WORLD/all refs/all LIVE scan | bounded by accepted design |
| collaboration lookup | WP-17 direct known-ID + completeness-protected companions; no directory registry/scheduler baseline | bounded by accepted design; machine debt routed |
| Story backlog | WP-18 derived from compatible source enumeration + layer coverage; no durable queue | source-contract boundedness must be audited per layer/domain in later WP-24 work |
| retrospective reading | Story integration + Context Runtime typed capabilities; no implicit catch-up mutation | boundedness contract exists; realization/empirical proof later |
| diagnostic operation | WP-21 evidence bounded to concrete question | bounded by accepted design |
| retained refs | authority lookup must not depend on all-ref scan; physical residue may grow | operational-scale question remains legitimate WP-24 research surface |
| monolithic family index | one expected family index for discovery | **explicit WP-24 measured partition revisit trigger**; not yet proven problematic by scaffold |

The critic found no Step-1 evidence that ordinary correctness currently *requires* a whole-campaign, whole-WORLD, all-ref or all-LIVE scan. It does identify Story source-domain enumeration, monolithic family-index growth, retained-ref operational pressure and contention amplification as legitimate later audit surfaces rather than prematurely declaring them defects.

---

## 6. Unsupported-host / autonomous-liveness sweep

Current supported profile is ordinary ChatGPT Plus chat with fixed connected GitHub transport. The inspected accepted owners explicitly avoid requiring autonomous liveness:

- no exact hidden-context telemetry dependency;
- no background context service;
- no clean SAVE heartbeat;
- no collaboration scheduler/presence heartbeat;
- no Chronicler worker/heartbeat/queue requirement;
- no background cleanup queue;
- no automatic branch/ref deletion process.

This is a **negative architectural finding**, not empirical proof that the future MVP meets its user-visible latency objective. Integrated responsiveness, long-chat calibration and real contention remain appropriately classified as future realized/production-like evidence.

---

## 7. Numerical-budget audit

Numbers currently admitted into Step-1 framing have an owner basis:

| Value | Basis | Critic classification |
|---|---|---|
| 120 seconds | PO-003 PLAY NOW law | accepted product constraint |
| 10,240 bytes | runtime mutable GitHub artifact Product Owner decision | accepted runtime operability hard invariant |
| 65,536 route buckets | WP-11 deterministic route geometry | structural routing property, not performance budget |
| current scaffold index byte sizes | exact current GitHub metadata at Step-1 basis | narrow existing-surface measurement only |

No new latency, throughput, file-count, index-size, API-call, retry-count or cardinality limit is introduced by Step 1.

---

## 8. Authority-reopen audit

```text
R2.3 CONTEXT ARCHITECTURE REOPEN: NO
R2.6 HOST TRANSPORT SELECTION REOPEN: NO
WP11 ROUTING/INDEX AUTHORITY REOPEN: NO
WP13 PUBLICATION AUTHORITY REOPEN: NO
WP16 LIVE AUTHORITY REOPEN: NO
WP17 COLLABORATION OWNER REOPEN: NO
WP18 STORY/DRAMATURG OWNER REOPEN: NO
WP21 CLEANUP/RETIREMENT OWNER REOPEN: NO
PO-003 PERFORMANCE LAW REOPEN: NO
PO-006 REF-DELETION POLICY REOPEN: NO
```

WP-11 index partitioning is an explicitly delegated later choice if its measured trigger fires; evaluating that trigger is not reopening route/index authority.

---

## 9. Source Manifest critic result

The repaired Task Brief now contains all materially necessary Step-1 owner classes exposed by independent dependency reconstruction:

- process/program/PO authority;
- R2.7 scope owner;
- context/host/resource owners;
- storage/routing/HOT/publication owners;
- multiplayer/LIVE/collaboration owners;
- Story/planning/retrospective consumers;
- diagnostics/retention/ref residue;
- current CORE consumers;
- schema/scaffold/tool/test/CI routes;
- verification/empirical boundary;
- negative evidence and revisit triggers.

No unresolved BLOCKING/SIGNIFICANT source omission remains for Step-1 framing.

This does not claim repository-global semantic completeness or replace Step-2 evidence extraction. It means the Step-1 dependency subgraph is sufficiently reconstructed for independent Senior review without making the human reviewer discover missing owner classes by corpus proofreading.

---

## 10. Final critic verdict

```text
STEP1_FRAMING_REVIEW_READY: YES
SOURCE_MANIFEST_COMPLETE_FOR_STEP1: YES
MECHANICALLY_RESOLVABLE_BLOCKING_REPAIRED: YES
MECHANICALLY_RESOLVABLE_SIGNIFICANT_REPAIRED: YES
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
STEP2_AUTHORIZED: NO
NEXT_GATE: MANDATORY INDEPENDENT SENIOR REVIEW OF WP-24 STEP 1
```

**STOP FOR MANDATORY INDEPENDENT SENIOR REVIEW.**
