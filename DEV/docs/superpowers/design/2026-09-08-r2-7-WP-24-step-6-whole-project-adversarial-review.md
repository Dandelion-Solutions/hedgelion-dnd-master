# R2.7 WP-24 Step 6 — Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — 0 BLOCKING / 5 SIGNIFICANT FINDINGS — STEP 7 REQUIRED**

Date: 2026-09-08

Review basis HEAD: `228ddd73aec1287d6791a677f7c09d01d97916c9`

Domain: **Performance / scale / operational budget**.

This is the mandatory independent whole-project adversarial critic of the WP-24 Step-5 candidate. Its purpose is not to confirm the candidate but to reconstruct the relevant dependency graph from current owners and search for hidden unbounded work, false proof, stale assumptions, owner collisions and scale-sensitive special paths.

The critic does not authorize implementation planning, implementation, optimization implementation, release, migration or gameplay bootstrap.

---

## 1. Independent reconstruction basis

The critic rebuilt the relevant source graph from current owners rather than treating the Step-5 candidate as authority.

Primary current owners inspected/reconciled include:

- `DEV/PRODUCT_OWNER_INPUT.md` — PO-003 interactivity requirement;
- `GAME/CORE/PLAY_POLICY.md`;
- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- R2.3 Context Runtime;
- R2.4 single-context execution;
- R2.6 MVP host assurance;
- WP-09 context/resource realization;
- WP-11 physical routing/indexing;
- WP-12 HOT/SQLite;
- WP-13 durability/publication;
- WP-14 recovery/checkpoint/session repair;
- WP-15 temporal/chronology;
- WP-16 LIVE/currentness/access;
- WP-17 collaboration;
- WP-18 Story/Dramaturg;
- WP-19 bootstrap/retrospective/PO-003 composition;
- WP-21 diagnostics/cleanup/ref-retirement;
- WP-22 verification/evaluation completeness;
- Step-5.1 domain-progress law;
- Step-5.6 publication/crash-consistency law;
- Story producer/persistence/retrospective consumer integration contract;
- Story baseline projection source contracts;
- Story persistence growth/sharding/consumer-decoupling owner decision;
- runtime mutable GitHub artifact size owner decision;
- branch/ref deletion prohibition owner decision.

Navigation/status sources were used only for routing and sequencing.

---

## 2. Preservation baseline

The critic found no basis to reopen these accepted constraints:

```text
PO-003 / WP19-L38/L39 zero-extra-serial capture law
no fixed turn time/token/step/complexity ceiling
full exact-package CORE preload at package binding
ordinary-turn zero CORE reread
package-switch / verified-loss full CORE rebuild
R2.3 bounded typed campaign/context discovery and allocation
WP-11 direct known-ID routing without index/directory enumeration
WP-11 monolithic family-index baseline subject to WP-24 trigger
10,240-byte mutable GitHub runtime text-file hard cap
Story eight baseline registrations
independent Story layer/domain/origin/lane coverage semantics
Story corpus has no corpus-wide quota
Story backlog is derived; no durable scheduler/queue/worker/heartbeat
Story read does not force catch-up mutation
Story retrospective consumers remain storage-topology-neutral
~250 / 251–300 / >300 direct-LLM-facing Story ergonomics policy
exact archival material cannot be truncated/paraphrased for storage convenience
exact archive needs safe partition/reconstruction before admission if indivisible size may exceed one file
bounded publication/currentness/conflict footprints
no branch/ref deletion or deletion probing/fallback
WP-22 architecture / realization / verification / empirical-acceptance separation
no fake preimplementation MVP/performance surrogate
no concrete shard/index/partition topology without evidence/trigger
```

No current evidence establishes a need for a new global performance owner, global cursor, global scheduler, universal freshness scalar, repository cleanup service or numeric latency SLA.

---

## 3. Workload-path adversarial sweep

### 3.1 Ordinary turn

Accepted fast path remains structurally bounded:

```text
already-loaded exact CORE cache
+ bounded working set
+ registered current-decision dependency closure
-> one bounded turn envelope
```

No required CORE reread, global campaign scan, global Story scan, generic maintenance pass, background service or PO-003 dedicated serial call is admitted.

### 3.2 New chat / campaign selection

Runtime storage discovery itself is bounded, but campaign-menu discovery currently says `Enumerate only campaign/*` then reads one compact card per branch. The work is semantically narrow but cardinality is not explicitly bounded as campaign refs accumulate.

This becomes finding `F24-06-01`.

### 3.3 Source movement / resynchronization

Current runtime uses:

```text
HEAD probe
-> base..HEAD changed-path comparison if moved
-> intersect with bounded current dependencies
-> exact relevant reads
```

Step 5.6 requires bounded changed-path/ancestry comparison, but the candidate did not state what happens when a long-stale chat or high-churn multiplayer interval makes the compare result itself operationally large.

This becomes `F24-06-04`.

### 3.4 Recovery / checkpoint / chronology

WP-14 explicitly requires bounded independent-root discovery and correctness-required transitive hydration only; ordinary recovery forbids WORLD/LOG/all-checkpoint/broad-history scans. Checkpoint is optional assistance, not startup authority. WP-15 requires typed dependency enrollment and rebuildable Agenda; it forbids all-thread/WORLD/LOG fallback scans and global chronology reconstruction.

These owners were in the Step-1 Source Manifest but not preserved as a distinct workload path in Step 2/Step 5.

This becomes `F24-06-05`.

### 3.5 Story production and retrospective reads

Story per-operation windows are bounded, but total retained corpus and source-domain count may grow indefinitely. The eight fixed registrations are instantiated over `LOCAL` and each relevant `LIVE:<epoch>` native origin, with independent lane/domain coverage. The Step-5 candidate prohibited an unbounded Story scan but did not make explicit that the **service-opportunity check itself** cannot become O(total historical origin/domain count) on every ordinary envelope.

This becomes `F24-06-03`.

### 3.6 Mutable monolithic controls/indexes

The candidate preserved evidence-triggered index/Story partitioning but did not explicitly state the priority relation between an optional earlier optimization trigger and the already-binding 10,240-byte prepublication hard cap. A pending mutable singleton that exceeds the hard cap cannot remain monolithic while waiting for another measurement.

This becomes `F24-06-02`.

### 3.7 Publication / contention

Current publication owners already provide:

- bounded semantic footprint;
- one coherent campaign tree/commit boundary;
- non-force ref transition;
- typed accepted/rejected/indeterminate outcomes;
- bounded retry;
- transport-only rebuild for proven-disjoint movement;
- no mechanics/RNG replay.

No new architecture defect found beyond the read-side stale-base issue above.

### 3.8 Collaboration / LIVE / maintenance

No global collaboration index/scheduler/presence heartbeat, all-LIVE scan, global diagnostics scan or cleanup worker is required. Per-target LIVE authority lookup and collaboration routing remain bounded and direct. Retained refs may accumulate physically but are non-authoritative; deletion remains absolutely forbidden.

No additional blocking/significant defect found.

---

# 4. Findings

## F24-06-01 — SIGNIFICANT — Campaign-menu discovery cardinality is not explicitly bounded

**Evidence**

- WP-19 requires bounded storage/campaign discovery before campaign selection.
- `BOOTSTRAP_RUNTIME.md` limits storage-repository discovery but campaign menu currently enumerates `campaign/*` and performs compact per-branch card probing.
- Campaign refs can accumulate across a long-lived storage repository; archived/retired refs may remain physically because branch/ref deletion is prohibited.
- Card-first projection avoids deep campaign reads but does not itself bound branch-count work.

**Risk**

A new-chat/menu operation could scale with total retained campaign-ref count and eventually become a large all-campaign enumeration even though no individual campaign body is loaded.

**Required resolution**

WP-24 final law must require bounded campaign/menu discovery per operation. A conforming realization may use provider-supported bounded paging, bounded continuation, exact-name narrowing/filtering or an owner-valid compact discovery projection, but WP-24 must not select the concrete mechanism now. Exhaustive all-`campaign/*` traversal is not a required single-operation behavior as cardinality grows.

Retained/archived refs stay non-authoritative and are not deleted to solve this problem.

**Decision status:** no Product Owner decision required; this is propagation of already accepted bounded preselection semantics.

---

## F24-06-02 — SIGNIFICANT — 10 KiB hard cap is a mandatory activation trigger

**Evidence**

The accepted owner law requires every runtime-authored mutable GitHub text artifact to serialize to at most `10,240` UTF-8 bytes before publication. An oversized pending artifact must be resolved by an owner-valid partition/compaction/rollover/redesign before publication.

The Step-5 candidate correctly treated partitioning as evidence-triggered but did not explicitly distinguish:

```text
optional earlier operational optimization trigger
vs
already-binding hard prepublication size failure
```

**Risk**

A later implementer could misread “remain monolithic until measured trigger” as permission to reach the hard cap and then fail without an already admitted activation path, or as permission to wait for latency evidence after publication is already impossible.

**Required resolution**

For every mutable monolithic index/control/Story/planning/collaboration or equivalent runtime text file:

- earlier partitioning remains measurement/owner-triggered;
- final serialized size `> 10,240 B` is itself decisive evidence and a hard publication blocker;
- a safe owner-valid bounded representation must activate before an oversized payload is published;
- WP-24 still selects no concrete shard count/layout.

**Decision status:** no Product Owner decision required; the Product Owner already fixed the cap.

---

## F24-06-03 — SIGNIFICANT — Story service-opportunity cost must not scale with total historical source-domain fan-out

**Evidence**

The baseline Story contracts define eight registrations instantiated over native origin scopes. `LOCAL` and each selected `LIVE:<epoch>` origin retain distinct source domains/cursors, and lanes are independent. Source-scope completeness that cannot be proven by current routing yields `UNKNOWN/defer`; a global live/Story scan is forbidden.

R2.4 requires every ordinary TurnEnvelope to evaluate Story service opportunity, but does not require catch-up generation/publication on every turn.

**Risk**

If opportunity detection walks every historical Story source domain/origin/lane each turn, ordinary-turn work grows with campaign lifetime even while each individual catch-up window remains bounded.

**Required resolution**

WP-24 final law must state:

- Story service-opportunity detection itself has a finite per-envelope resource bound;
- current owner routing/coverage metadata nominates only bounded candidate source domains/windows for that opportunity;
- inability to prove broader scope completeness within the bound yields `UNKNOWN`/`DEFER`, not a global scan or false caught-up claim;
- residual backlog remains a future service obligation without durable scheduler/global cursor/heartbeat;
- no cross-origin/lane total order is introduced;
- future realized/empirical evaluation checks campaign-age/source-domain fan-out and starvation behavior.

**Decision status:** no Product Owner decision required; this composes current R2.4 + Story source-contract laws.

---

## F24-06-04 — SIGNIFICANT — Long-stale changed-path synchronization needs a bounded fallback

**Evidence**

`RUNTIME.md` / `BOOTSTRAP_RUNTIME.md` use server-side `base..HEAD` changed-path comparison only when HEAD moved. Step 5.6 requires a **bounded changed-path / ancestry comparison** and bounded semantic conflict footprint.

The candidate did not explicitly state the operational fallback when the changed interval/result is too large or the supported provider cannot return it within the admitted bounded envelope.

**Risk**

A long-idle chat or high-contention campaign could turn a synchronization operation into work proportional to every change since the old base, or encourage pagination/history walking until the whole interval is consumed.

**Required resolution**

WP-24 final law must require:

```text
if bounded changed-path comparison is available and fits admitted envelope:
    use it to avoid irrelevant rereads
else:
    pin current authoritative HEAD
    directly reread/revalidate only the bounded current owner/dependency/
    authorization/routing footprint needed by loaded dirty/current-decision state
    reconcile/adopt under native owners
```

Do not exhaustively paginate the old interval, walk full history or infer safety from missing partial comparison data.

Real comparison/result-size and contention latency remain Class-B/Class-C measurement obligations.

**Decision status:** no Product Owner decision required; bounded repository comparison is already an accepted transport requirement.

---

## F24-06-05 — SIGNIFICANT — Recovery and chronology special paths were omitted from the Step-2/Step-5 performance composition

**Evidence**

The Step-1 Source Manifest explicitly included WP-14/WP-15. Current owners establish:

- current-source-first pinned recovery;
- bounded independent-root discovery;
- correctness-required transitive hydration only;
- no campaign-wide WORLD/LOG/history/all-checkpoint scans;
- checkpoint as optional acceleration/evidence, not startup authority;
- typed temporal dependency enrollment;
- rebuildable Agenda;
- no all-thread/WORLD/LOG fallback;
- chronology/order evidence remains owner-anchored and sparse, not a global reconstructed timeline.

Step-2 evidence reconciliation and the Step-5 candidate did not preserve this as a distinct workload/special-path result.

**Risk**

WP-24 could incorrectly claim whole-project scale coverage while leaving cold recovery/temporal rebuild susceptible to later unbounded “reconstruct everything” interpretations.

**Required resolution**

Add a recovery/chronology performance law:

- cold recovery cost follows current routed independent roots + bounded correctness-required RRC closure, not campaign age/history corpus size;
- checkpoint use may accelerate but cannot require newest/all-checkpoint enumeration;
- temporal recovery rebuilds complete owner-declared dependency enrollment/Agenda from admitted current roots without global world/history traversal;
- chronology retrieval expands only for the concrete typed relation/dependency being resolved;
- no generic recovery/chronology cursor/frontier is introduced;
- realized recovery cardinality/latency is Class B; real supported-host recovery experience is Class C where applicable.

**Decision status:** no Product Owner decision required; this is omitted current-owner propagation.

---

## F24-06-M1 — MINOR — Runtime-package count is a future startup scaling dimension

New-chat package discovery is already lazy and metadata-only, so no current architecture defect is established. If many simultaneously supplied runtime packages later make startup/package-indexing materially costly, measure and revisit under the existing package/bootstrap owner rather than preemptively creating a new registry/service.

**Disposition:** safe deferred measurement trigger.

---

## F24-06-M2 — MINOR — Initial scaffold publication is finite-at-package but deserves explicit proof classification

Initial campaign scaffold construction/publication is a from-scratch special path. Its work scales with the selected package scaffold/configuration rather than campaign age. Current architecture exposes no unbounded campaign-growth loop here, but realized call count/latency belongs to future Class-B benchmarking rather than architectural assumption.

**Disposition:** safe deferred benchmark classification.

---

# 5. Adversarial negative scan

The critic explicitly searched for and did **not** find a current requirement for:

```text
whole campaign preload
whole WORLD scan on ordinary gameplay
whole LOG/history scan on ordinary gameplay
all-LIVE/ref scan for per-target write authority
global Story scan for one retrospective read
global Story scan for one catch-up window
durable Chronicler queue/worker/lease/heartbeat
save heartbeat / wall-clock flush worker
collaboration scheduler / presence heartbeat
global cleanup worker
branch/ref deletion or deletion fallback
global chronology clock
global Story cursor
global campaign progress scalar
new global performance budget object
fixed numeric turn SLA
mandatory extra LLM call for PO-003 basis capture
preimplementation parallel MVP/performance surrogate
premature concrete index/Story shard topology
```

No new duplicate semantic owner was discovered.

---

# 6. Proof-class adversarial scan

The following remain strictly separated:

- source/corpus/cardinality measurements at current exact HEAD -> **Class A only**;
- realized implementation path latency/call/result-size/shard behavior -> **Class B**;
- end-to-end supported-host responsiveness, prompt pressure, gameplay quality and real contention -> **Class C**.

Current physical CORE bytes do not prove model token occupancy, prompt pressure or user-visible latency.

Current source topology does not prove production retry latency, Story starvation, menu latency or recovery latency.

Green repository CI does not prove empirical performance acceptance.

---

# 7. Upstream-reopen audit

```text
R2.3 CONTEXT ARCHITECTURE REOPEN: NO
R2.4 SINGLE-CONTEXT / STORY-OPPORTUNITY REOPEN: NO
R2.6 HOST PROFILE REOPEN: NO
WP11 ROUTING / INDEX AUTHORITY REOPEN: NO
WP13 PUBLICATION AUTHORITY REOPEN: NO
WP14 RECOVERY AUTHORITY REOPEN: NO
WP15 TEMPORAL / CHRONOLOGY AUTHORITY REOPEN: NO
WP16 LIVE AUTHORITY REOPEN: NO
WP17 COLLABORATION AUTHORITY REOPEN: NO
WP18 STORY / DRAMATURG AUTHORITY REOPEN: NO
WP19 PO-003 / RETROSPECTIVE REOPEN: NO
WP21 REF-DELETION POLICY REOPEN: NO
WP22 PROOF-CLASS REOPEN: NO
STORY REGISTRATIONS REOPEN: NO
STORY CORPUS-RETENTION SEMANTICS REOPEN: NO
```

The five significant findings are cross-owner performance/scale composition gaps, not evidence that accepted upstream semantic owners are insufficient.

---

# 8. Step-6 result

```text
STEP6_COMPLETE: YES

BLOCKING_FOUND: 0
SIGNIFICANT_FOUND: 5
MINOR_FOUND: 2

SIGNIFICANT_IDS:
    F24-06-01
    F24-06-02
    F24-06-03
    F24-06-04
    F24-06-05

MINOR_IDS:
    F24-06-M1
    F24-06-M2

UNRESOLVED_BLOCKING_AFTER_STEP6: 0
UNRESOLVED_SIGNIFICANT_AFTER_STEP6: 5

HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO

NEXT_REQUIRED_STEP: STEP 7 — FINDING RESOLUTION / PROPAGATION
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
SUBSTANTIVE_IMPLEMENTATION_AUTHORIZED: NO
```
