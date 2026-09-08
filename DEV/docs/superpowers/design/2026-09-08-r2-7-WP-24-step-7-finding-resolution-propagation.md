# R2.7 WP-24 Step 7 — Finding Resolution / Propagation

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT STEP-6 FINDINGS RESOLVED**

Date: 2026-09-08

Input critic:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-6-whole-project-adversarial-review.md`

Step-6 result entering this gate:

```text
BLOCKING_FOUND: 0
SIGNIFICANT_FOUND: 5
MINOR_FOUND: 2
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 5
HUMAN_DECISION_REQUIRED: NO
```

This step resolves and propagates every finding into the final canonicalization contract. It does not authorize implementation planning, implementation, optimization implementation, release, migration or gameplay bootstrap.

The Step-5 candidate remains design provenance. Where Step-7 repairs differ from Step-5 wording, the Step-8 canonical result must incorporate the repairs and will control after final Senior acceptance.

---

## 1. F24-06-01 — campaign-menu discovery cardinality

**Step-6 severity:** SIGNIFICANT  
**Resolution:** RESOLVED / CANONICAL LAW REQUIRED

### Propagated law

Pre-selection campaign discovery is a bounded operation even when the storage repository retains many campaign refs.

A conforming realization SHALL NOT require exhaustive all-`campaign/*` traversal in one menu operation once the physical candidate set exceeds the admitted bounded retrieval envelope.

The owner-valid implementation may use one or more of:

- provider-supported bounded paging/continuation;
- bounded exact-name/prefix narrowing;
- a compact owner-valid discovery projection;
- another deterministic bounded discovery mechanism compatible with campaign/access owners.

The exact mechanism is implementation/host-profile work and is not selected by WP-24.

Card/menu projection remains nomination only. Selection still triggers current owner/access/currentness validation. Archived/retired/physically retained refs remain non-authoritative, and branch/ref deletion remains forbidden.

### Proof routing

- structural boundedness and provider capability contract -> architecture/current machine verification as applicable;
- realized page/call/card fan-out and menu retrieval cost -> Class B;
- user-visible new-chat/menu latency on supported host -> Class C where material.

**Upstream reopen:** NO. WP-19 already requires bounded preselection discovery.

---

## 2. F24-06-02 — 10 KiB hard-cap activation semantics

**Step-6 severity:** SIGNIFICANT  
**Resolution:** RESOLVED / CANONICAL LAW REQUIRED

### Propagated law

For every mutable GitHub-backed runtime textual artifact, distinguish:

```text
EARLY OPTIMIZATION TRIGGER
    measured size/latency/parse/conflict/tool behavior may justify partitioning earlier

HARD PUBLICATION TRIGGER
    final serialized UTF-8 payload > 10,240 bytes
    -> publication forbidden
    -> owner-valid bounded representation MUST be selected before publication
```

The hard cap is already decisive evidence. A mutable monolithic index, Story control file, planning/collaboration record or equivalent cannot remain in the old representation while waiting for a different latency/scale trigger after it would violate the cap.

Safe partitionability remains mandatory before a plausibly unbounded representation becomes an architectural dead end. WP-24 still selects no concrete shard count, page layout, rollover threshold or path scheme.

Exact material may not be truncated/paraphrased to satisfy the cap.

### Proof routing

- serialized-byte preflight -> deterministic executable verification when writer exists;
- growth/partition routing behavior -> Class B after realization;
- user-visible latency impact -> Class C where material.

**Upstream reopen:** NO. The Product Owner already fixed the 10,240-byte law.

---

## 3. F24-06-03 — Story opportunity detection over growing origin/domain fan-out

**Step-6 severity:** SIGNIFICANT  
**Resolution:** RESOLVED / CANONICAL LAW REQUIRED

### Propagated law

The R2.4 Story service-opportunity check itself SHALL have finite per-envelope work and SHALL NOT scale by exhaustively walking all historical Story source domains/origins/lanes as campaign history grows.

Current Story/native routing and compact coverage/source-basis metadata nominate a bounded candidate set of source domains/windows for the current opportunity.

If the requested broader source-scope completeness cannot be proven within the admitted bound:

```text
UNKNOWN / DEFER
```

not:

```text
scan all LIVE refs
scan all Story records/domains
invent caught-up state
```

Residual compatible backlog remains an outstanding future service obligation under R2.4. This rule introduces no:

- durable Story job queue;
- global cross-origin cursor;
- global source-domain total order;
- scheduler;
- worker/lease;
- heartbeat.

The eight registrations and independent LOCAL/LIVE origin/lane coverage semantics are unchanged.

### Proof routing

Future realized/scenario/empirical coverage must include:

- bounded service-opportunity work as source-domain count grows;
- no full-domain scan fallback;
- residual-backlog preservation on `DEFER`;
- no false caught-up claim from incomplete source-scope evidence;
- anti-starvation behavior under long-lived multi-origin backlog.

Machine work/result size -> Class B. Real supported-host starvation/turn-responsiveness behavior -> Class C.

**Upstream reopen:** NO. This is a performance composition of R2.4 and existing Story contracts.

---

## 4. F24-06-04 — long-stale changed-path synchronization

**Step-6 severity:** SIGNIFICANT  
**Resolution:** RESOLVED / CANONICAL LAW REQUIRED

### Propagated law

Changed-path comparison is an optimization for avoiding irrelevant rereads, not a license for unbounded history traversal.

For a stale local base:

```text
if provider-supported base..HEAD changed-path comparison
fits the admitted bounded envelope:
    compare
    -> intersect with bounded loaded/dirty/current-decision dependency footprint
    -> reread only affected exact owners

else:
    pin current authoritative HEAD/source basis
    -> directly reread/revalidate the bounded current owner/dependency/
       authorization/routing footprint required by the loaded dirty/current decision
    -> reconcile/adopt under native owners
```

A runtime SHALL NOT exhaustively paginate an arbitrarily large stale interval, walk full Git history or treat a partial comparison as proof that omitted changes are irrelevant.

This fallback does not create a global freshness scalar or campaign snapshot. Native owner/currentness laws remain controlling.

### Proof routing

Future realized verification/benchmarking covers:

- bounded compare behavior;
- forced fallback when compare result/provider envelope is exceeded/unavailable;
- correct direct current-footprint revalidation;
- no full-history traversal;
- multi-chat churn/long-idle amplification.

Machine/call/result-size behavior -> Class B. Supported-host responsiveness/contention -> Class C.

**Upstream reopen:** NO. Step 5.6 already requires bounded changed-path/ancestry comparison and bounded semantic footprint.

---

## 5. F24-06-05 — recovery / checkpoint / chronology special path

**Step-6 severity:** SIGNIFICANT  
**Resolution:** RESOLVED / EVIDENCE + CANONICAL LAW PROPAGATION

### Reconciled current owner evidence

WP-14:

- ordinary recovery targets actual current native authority;
- campaign revision is only a bounded discovery anchor;
- each participating mutable source is exact-pinned;
- independent-root discovery is typed/bounded;
- known-ID reads use exact WP-11 routes;
- no campaign-wide WORLD, LOG/history, all-checkpoint, all-runtime-record or broad-Git-history scan;
- transitive hydration is correctness-required only;
- checkpoint is optional assistance/evidence and healthy recovery may read zero checkpoints.

WP-15:

- armed temporal/process occurrences have complete typed dependency enrollment;
- Agenda is rebuildable derivative routing, never authority;
- missing enrollment cannot be repaired by a campaign-wide scan;
- cold recovery hydrates admitted current temporal/process roots and reconstructs required dependency enrollment/Agenda;
- no all-thread/WORLD/LOG fallback;
- chronology remains owner-anchored sparse typed evidence, never a reconstructed global timeline.

### Propagated law

Cold recovery / temporal rebuild is a distinct special workload path:

```text
current routed native sources
-> bounded independent operational roots
-> correctness-required RRC/dependency closure only
-> rebuild derivative Agenda/index/cache support
-> validate current compatible participating basis
```

Its correctness work scales with the admitted current operational root/dependency closure for the requested recovery scope, not with total campaign history/corpus age merely because old history exists.

Checkpoint use may be a measured accelerator but cannot become latest/all-checkpoint enumeration, currentness authority or required startup scan.

Chronology escalation names the concrete typed relation/dependency/question and remains bounded; no global timeline reconstruction is admitted.

No generic recovery cursor/frontier/chronology clock is added.

### Proof routing

- deterministic routing/root/enrollment invariants once realized -> executable/static/scenario proof according to WP-22;
- recovery root cardinality, hydration/read counts and latency -> Class B;
- real supported-host recovery experience where host behavior matters -> Class C.

**Upstream reopen:** NO.

---

## 6. Minor findings

### F24-06-M1 — runtime-package count

**Disposition:** SAFE DEFERRED / DORMANT TRIGGER

Current package discovery is lazy/metadata-only and exposes no current architecture defect. Revisit only if measured installed-package cardinality/startup cost becomes materially unacceptable or a concrete provider/tool limit requires a different bounded package-discovery representation.

No package registry/service is created now.

### F24-06-M2 — initial scaffold publication

**Disposition:** SAFE DEFERRED / FUTURE CLASS-B BENCHMARK

Initial campaign scaffold publication is finite at one selected package and does not grow with campaign age. Its realized object/tree/commit/call/latency cost must be benchmarked when the actual creation publisher exists. No new optimization is activated now.

---

## 7. Cross-system consistency after repairs

The repairs preserve all settled boundaries:

```text
PO-003 zero-extra-serial: PRESERVED
full CORE preload/rebuild: PRESERVED
ordinary-turn zero CORE reread: PRESERVED
R2.3 bounded context semantics: PRESERVED
WP-11 direct known-ID routing: PRESERVED
WP-13 publication/currentness: PRESERVED
WP-14 current-source-first recovery: PRESERVED
WP-15 chronology/Agenda ownership: PRESERVED
WP-16 bounded LIVE authority: PRESERVED
WP-17 no scheduler/heartbeat/global index: PRESERVED
Story eight registrations: PRESERVED
Story corpus retention / no quota: PRESERVED
Story no scheduler/worker/heartbeat: PRESERVED
10 KiB hard file cap: PRESERVED / CLARIFIED AS HARD ACTIVATION TRIGGER
Story line ergonomics: PRESERVED
exact-archive lossless pre-admission rule: PRESERVED
branch/ref deletion: FORBIDDEN
WP-22 proof classes: PRESERVED
fake preimplementation benchmark: FORBIDDEN
concrete partition/shard layout: NOT SELECTED
new numeric SLA: NONE
new global cursor/frontier/scheduler: NONE
```

---

## 8. Finding propagation table

| Finding | Final canonical propagation | Verification/defer propagation | Result |
|---|---|---|---|
| F24-06-01 | bounded campaign-menu discovery | B/C menu scale evidence | RESOLVED |
| F24-06-02 | hard-cap mandatory representation trigger | deterministic preflight + B/C | RESOLVED |
| F24-06-03 | bounded Story opportunity over domain fan-out | B/C fan-out + starvation | RESOLVED |
| F24-06-04 | bounded stale-base compare with direct-footprint fallback | B/C sync/contention | RESOLVED |
| F24-06-05 | bounded recovery/temporal rebuild path | B/C recovery + owner tests | RESOLVED |
| F24-06-M1 | no current change | dormant package-count trigger | SAFE DEFERRED |
| F24-06-M2 | no current change | future Class-B scaffold benchmark | SAFE DEFERRED |

---

## 9. Resolution gate

```text
STEP7_COMPLETE: YES

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
NEEDS_PO: NONE

UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
NEW_ARCHITECTURE_OWNER_CREATED: NO
NEW_GLOBAL_CURSOR_CREATED: NO
NEW_SCHEDULER_WORKER_HEARTBEAT_CREATED: NO
CONCRETE_SHARD_LAYOUT_SELECTED: NO
NEW_NUMERIC_SLA_SELECTED: NO

STEP8_CANONICALIZATION_ELIGIBLE: YES
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
SUBSTANTIVE_IMPLEMENTATION_AUTHORIZED: NO
```
