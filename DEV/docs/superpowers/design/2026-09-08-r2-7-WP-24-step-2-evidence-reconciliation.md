# R2.7 WP-24 Step 2 — Evidence Reconciliation

Status: **STEP 2 COMPLETE — CURRENT-HEAD EVIDENCE RECONCILED — NO HUMAN DECISION REQUIRED**

Date: 2026-09-08

Evidence basis at Step-2 start: `14d49e64deea9edd611165b2457fa6aea0e67241`.

Step-1 gate: **mandatory independent Senior re-review PASS / GO**. `SR24-S1-01..04` are closed. WP-24 Step 2 is authorized; implementation planning and implementation are not.

This artifact is evidence/design provenance. It does not supersede any semantic owner and does not select implementation details.

---

## 1. Question being reconciled

WP-24 asks whether the accepted HDM architecture remains bounded, responsive and operationally viable as campaign/state/history cardinality grows, without weakening correctness or inventing unsupported host assumptions.

The reconciliation separates:

```text
OWNER-DEFINED HARD / STRUCTURAL LAW
OWNER-DEFINED OPERABILITY GUIDANCE
CURRENT CLASS-A PHYSICAL MEASUREMENT
FUTURE REALIZED-IMPLEMENTATION MEASUREMENT
FUTURE REAL-HOST / PRODUCT EMPIRICAL ACCEPTANCE
DORMANT / TRIGGER-GATED OPTIMIZATION
```

A future measurement obligation is not a present architecture defect. A physically unbounded retained corpus is not an ordinary-path unbounded operation when every ordinary operation remains bounded and the persistence owner preserves a safe partition path.

---

## 2. Current owner reconciliation

| Concern | Current owner(s) | Exact current consequence for WP-24 | Classification |
|---|---|---|---|
| Ordinary gameplay fast path | `GAME/CORE/RUNTIME.md`, `PLAY_POLICY.md` | When the loaded working set is sufficient: no GitHub read/write/HEAD refresh in singleplayer, no CORE reread, no research. Additional retrieval requires a concrete decision-level reason. | STRUCTURAL PERFORMANCE LAW |
| Reasoning budget | `GAME/CORE/RUNTIME.md` | Stop unnecessary deliberation; do not impose fixed token/time/step/complexity turn ceiling. Correctness may require deeper reasoning. | STRUCTURAL LAW / NEGATIVE SLA EVIDENCE |
| PO-003 historical basis | PO-003 + WP-19 `L38/L39` | Basis capture adds zero dedicated sequential LLM call, zero redundant serial read when T0 is already admitted, zero separate publication, zero irrelevant-turn work; only bounded typed material. Extra serial round trip is material escalation. | HARD CRITICAL-PATH LAW |
| Engine instruction cache | `PLAY_POLICY.md`, `BOOTSTRAP_RUNTIME.md`, R2.4 `L23`, WP-09 `L1` | Full exact-package CORE + RULES routing preload on initial package resolution; full rebuild on package switch or verified context loss; ordinary activation does not reread CORE. | CURRENT RUNTIME STRATEGY |
| Campaign context | R2.3 + WP-09 | Registered typed finite discovery/closure; required floors before optional; centralized conservative estimator; terminal `UNSATISFIABLE`; no ordinary global campaign/history scan. | STRUCTURAL RESOURCE LAW |
| Known-ID storage routing | WP-11 + WP-12 | Derive exact route from family + identity; no directory/index enumeration. Loaded body revalidates identity. | STRUCTURAL BOUNDEDNESS LAW |
| Family discovery indexes | R2.3 + WP-11 | Baseline family indexes remain monolithic. Partition only when measured size/transfer/host-tool evidence proves baseline operationally unacceptable. | DORMANT MEASURED TRIGGER |
| HOT/SQLite | WP-12 | Local transactional support is owner-typed and derived helpers rebuildable; no external I/O inside a SQLite transaction; no performance target selected by WP-12. | STRUCTURAL SUPPORT / LATER BENCHMARK |
| Campaign durability/publication | WP-13 | Closure is bounded to policy roots/dirty scope/direct dependencies; no whole campaign/WORLD/full-history scan; one coherent campaign tree + single-parent commit + final non-force ref transition. Retry is bounded but exact retry threshold remains implementation-defined. | STRUCTURAL BOUNDEDNESS + LATER BENCHMARK |
| Publication contention | WP-13 | Proven-disjoint movement permits transport-only rebuild; relevant overlap requires owner reconciliation; indeterminate publication is verified, not blindly retried. | STRUCTURAL FAILURE LAW + EMPIRICAL COST LATER |
| LIVE lookup | WP-16 | Per-target `WriteAuthorityLookup` uses current campaign routing + bounded claim metadata; no WORLD/all-ref/all-LIVE scan. Exact-source CAS/currentness remains domain-local. | STRUCTURAL BOUNDEDNESS LAW |
| Collaboration | WP-17 | Direct known-ID collaboration obligation plus completeness-protected bounded PLAYER companions; no collaboration directory enumeration, global registry, scheduler, presence or heartbeat service. | STRUCTURAL BOUNDEDNESS / NEGATIVE SERVICE LAW |
| Story semantics/lifecycle | WP-18 + Story integration | Layer-local Story, derived backlog, bounded source windows, Story publication yields to gameplay; no durable queue/lease/worker/heartbeat. Retrospective reads are typed and bounded. | STRUCTURAL BOUNDEDNESS / NEGATIVE SERVICE LAW |
| Story source registration geometry | Story baseline projection source contracts | Eight fixed registrations. E-EVT/N-EVT and E-REL/N-REL share native enumeration but require independent Story coverage. LOCAL and selected LIVE origins/lane cursors remain independent. | FIXED CONTRACT INVENTORY / SCALE DIMENSION |
| Story backlog/corpus | Story baseline + integration | One candidate/read window is bounded; total backlog and total retained Story corpus may grow with campaign history. No corpus-wide size quota. | PER-OP BOUNDED / TOTAL CORPUS GROWTH ALLOWED |
| Story pre-projection retention | Story baseline + Step-5.13 | Required native source/survivor must remain sufficient until MUST projection is satisfied or an admitted equivalent survivor exists. | RETENTION PRESSURE / OWNER-PROTECTED |
| Story post-coverage retention | Story baseline/integration | Required Story account remains available while compatible coverage promise remains, subject to owner-valid migration/replacement/end-of-promise. | RETENTION PRESSURE |
| Story completeness uncertainty | Story baseline | If native routing cannot prove requested origin/domain scope complete, return `UNKNOWN/defer`; never recover by global LIVE/Story scan or false caught-up status. | FAIL-CLOSED BOUNDEDNESS LAW |
| Mutable runtime text size | runtime mutable artifact-size owner | Final serialized UTF-8 mutable runtime text file <= 10,240 B before publication. Oversize is resolved by owner-valid partition/compaction/rollover; no truncation of required semantics. | HARD PER-FILE OPERABILITY LAW |
| Story partitionability | Story growth/sharding owner | Every plausibly unbounded GitHub-backed Story collection must have a deterministic bounded partition path before monolithic representation becomes an architectural dead end. Activation/how remains measurement-driven. | REQUIRED SAFE PATH / TRIGGER-GATED REALIZATION |
| Direct LLM-facing Story shape | Story growth/sharding owner | ~250 lines preferred ceiling; 251–300 review zone; >300 not acceptable normal steady state without explicit safe bounded alternate-retrieval reason. | ERGONOMICS / OPERABILITY GUIDANCE ONLY |
| Exact archival oversize | Story growth/sharding owner + T-ARCH | Exact material cannot be truncated/paraphrased for file size. If an admitted exact scope may exceed one indivisible file, bounded exact partition/reconstruction semantics must be owner/schema-defined before admission. | PRE-ADMISSION CORRECTNESS LAW |
| Retained Git refs | PO-006 + WP-21 | Physical retired/non-selected refs may persist indefinitely; existence is non-authoritative; automatic deletion/probing/fallback is forbidden; ordinary authority must not depend on all-ref enumeration. | UNBOUNDED PHYSICAL RESIDUE / BOUNDED AUTHORITY DEPENDENCE |
| Diagnostics/cleanup | WP-21 | Diagnostic work is bounded to a concrete question; no package/campaign-wide telemetry baseline and no background cleanup service. Uncertain destructive cleanup retains. | STRUCTURAL BOUNDEDNESS / NEGATIVE SERVICE LAW |
| Host/context behavior | R2.6 | No exact hidden-capacity dependency; centralized conservative estimator; actual long-chat/context/behavior calibration belongs on implemented MVP. | ARCHITECTURE BOUND + EMPIRICAL AFTER REALIZATION |
| Verification proof | WP-22 | Architecture coverage, machine realization, verification realization and empirical acceptance are independent. Static/CI/scenario evidence cannot be over-credited. | PROOF-CLASS LAW |

---

## 3. Current physical measurements and their proof power

### 3.1 Full engine instruction preload

The Step-1 recovery measured on `80649df2ff16f79170c8664f3a09750dcd8708e1`'s corresponding source lineage:

```text
CORE/*.md file count                    45
aggregate CORE/*.md bytes              364,844 B
RULES/INDEX.md                           1,752 B
RULES/README.md                          4,132 B
total preload-source file count             47
total preload-source bytes             370,728 B
```

Fresh Step-2 comparison from the earlier measurement commit lineage through `14d49e64deea9edd611165b2457fa6aea0e67241` shows no `GAME/` file change; the current `GAME/CORE` directory metadata also matches the measured largest-file values. Therefore the narrow physical-source measurement remains current at this Step-2 basis.

Its classification remains:

```text
CURRENT PHYSICAL CORPUS MEASUREMENT ONLY
!= forecast of eventual production CORE size
!= sizing baseline for eventual production CORE
!= representativeness claim for eventual production CORE corpus
!= model token occupancy
!= prompt-pressure proof
!= user-visible latency benchmark
!= real-MVP empirical acceptance
```

No bytes-to-token conversion is admitted.

### 3.2 Scaffold family indexes

The Step-1 tiny scaffold `GAME/CAMPAIGN/INDEX/*.yaml` files remain evidence only of the shipped empty/minimal scaffold. They do not establish large-campaign index size, parse cost, transfer latency or that WP-11's measured partition trigger has fired.

### 3.3 Existing connected-transport probes

The 10 KiB owner decision already records content-shape-dependent whole-file retrieval observations. Those probes justify the owner-selected conservative 10 KiB project invariant; WP-24 does not reinterpret them as a vendor hard limit or derive another numeric threshold.

---

## 4. Workload-class reconciliation

### 4.1 Ordinary single-player turn

Baseline:

```text
already-loaded exact CORE cache
+ sufficient campaign working set
-> bounded turn pipeline
-> no repository traffic unless concrete dependency/persistence boundary requires it
-> narration
```

The ordinary path is structurally independent of total campaign age/cardinality except when the current decision names a concrete dependency not already loaded. R2.3/WP-09 then constrain discovery/closure to finite registered relations.

PO-003 adds no dedicated serial capture work.

### 4.2 New chat / substantial setup

Full engine instruction-cache construction is a foreground one-time package cost before substantial setup/gameplay. Campaign data remains lazy. Current physical corpus size is known only for today's source tree; final production behavior requires future real-target evaluation.

### 4.3 Package switch / verified instruction-context loss

Both rebuild the complete exact-package CORE cache. They are foreground exceptional paths, not permission for ordinary module rereads. Their frequency/cost is a later realized-host measurement question.

### 4.4 Campaign persistence / SAVE

Publication cost scales with the bounded participating owner/dependency footprint plus conflict/currentness revalidation, not the whole campaign. One logical campaign publication is one coherent tree + one commit + non-force ref transition. Multi-chat movement can amplify bounded work through repin/rebuild/revalidation; no numeric retry SLA is owner-defined.

### 4.5 LIVE multiplayer

Per-target routing is bounded, but contention can increase exact-source refresh/revalidation/CAS attempts. This is a real-target concurrency/performance measurement concern, not permission to add a global registry/lock/server.

### 4.6 Collaboration

Durable collaboration exists only for positive bounded agency-dependent collective input. Current route recovery is by bounded PLAYER companions + direct known-ID obligation read. No whole collaboration frontier/index/scheduler exists.

### 4.7 Story opportunity check versus Story catch-up

R2.4 requires an envelope-level Story backlog/service-opportunity decision. This must not be conflated with executing catch-up.

```text
opportunity decision:
    compact typed coverage/source-basis metadata
    -> NO_BACKLOG | SERVICE(window) | DEFER(reason)

SERVICE(window):
    bounded native candidate window
    -> optional Chronicler transformation
    -> deterministic validation/publication/coverage advance
```

The opportunity decision is ordinary envelope control and must remain compact/bounded; it may not require unbounded Story/history scanning. Actual catch-up generation/publication yields to current-play correctness and protected Narrator/output capacity, may lag, and does not become a background worker.

This distinction prevents two false claims:

- "Story has zero involvement in every ordinary turn" — false because the accepted envelope evaluates service opportunity;
- "Story catch-up is a mandatory serial gameplay publication on every turn" — also false.

### 4.8 Story long-campaign growth

Story intentionally retains a navigable retrospective corpus and can grow with campaign history. Bounded reads/windows are not a total-corpus bound. Operability is preserved by:

- per-file 10 KiB hard bound;
- bounded candidate/read operations;
- deterministic partitionability for every plausibly unbounded collection;
- known-ID/bounded routing after partitioning;
- storage-topology-neutral consumer contract;
- no global scan fallback;
- no requirement to choose a concrete shard layout before evidence/realization.

### 4.9 Retained refs

Physical repository residue may grow without bound because HDM never deletes branches/refs. Correctness is insulated by logical deauthorization and bounded owner routing. Operational listing/discovery pressure remains a future measurement surface; it cannot be "solved" by reintroducing ref deletion.

---

## 5. Structural risk register after reconciliation

| Risk | Current status | Required treatment |
|---|---|---|
| Ordinary path accidentally grows with campaign age | No current owner requires it | Preserve direct routing, finite registered context, bounded publication closure and no global-scan fallbacks. |
| Full CORE physical corpus grows substantially before production | Open scaling variable, not current defect | Remeasure realized/production-relevant corpus; evaluate real host behavior before acceptance. |
| Full preload causes prompt pressure/behavior degradation | Unknown until real target | WP-22 Class C after implementation; do not build surrogate or silently change loading strategy now. |
| Monolithic family index becomes operationally large | Dormant | Measure actual grown index size/transfer/parse/tool behavior; partition only if trigger fires. |
| Story corpus grows indefinitely | Expected/allowed | Keep per-operation reads bounded and require deterministic bounded partition path. No corpus quota. |
| Story projection/control metadata grows in a singleton | Architecture prevents dead-end, exact layout unrealized | Physical realization must inspect growth-bearing fields and select bounded representation before limits are hit. |
| Exact archival unit cannot fit one file | Explicit pre-admission gate | Owner/schema must define lossless bounded partition/reconstruction before representation admission. |
| Multi-chat publication retries amplify latency | Real concern, no current numeric threshold | Preserve bounded retry/typed failure; benchmark/evaluate realized path. |
| Retained refs accumulate | Expected under PO-006 | Measure operational pressure; never make all-ref enumeration correctness dependency; deletion remains forbidden. |
| Background service assumed for Story/save/collaboration/cleanup | Rejected by current owners | Keep foreground/event-driven/turn-local semantics and no heartbeat correctness dependency. |
| Static/CI evidence over-credited as performance acceptance | Prohibited by WP-22 | Preserve claim-specific proof matrix. |

No risk above currently establishes a product trade-off that requires Product Owner judgment before WP-24 architecture can close.

---

## 6. Alternatives exposed by the evidence

### Alternative A — Global numeric performance SLA / global budget

Examples would be fixed turn seconds, fixed token cap, global file count, global Story corpus quota or universal API-call count.

**Rejected by current evidence.** No owner supplies such a number; `RUNTIME.md` specifically rejects a fixed reasoning ceiling; exact hidden context telemetry is unavailable by contract; Story explicitly has no corpus quota.

### Alternative B — Owner-composed path budgets + trigger-gated optimization + staged proof

Use existing hard/structural laws for correctness and ordinary-path boundedness, preserve explicit operability constraints (10 KiB, Story safe partitionability, direct-LLM ergonomics, exact-archive admission safety), and activate physical optimization only when owner-defined measured triggers fire. Verify realized costs after implementation and empirical host/product behavior on the real supported target.

**Evidence-supported.** This preserves every current owner without adding an unowned performance authority.

### Alternative C — Preemptive physical optimization now

Partition family indexes now, select Story shard counts/layouts, add generic cache/batching/worker infrastructure, or choose a retry threshold before realization evidence.

**Rejected for current WP-24.** This would activate dormant decisions, duplicate existing owners or violate the explicit measurement/evidence gates.

---

## 7. Evidence-completeness result

The current-head reconciliation directly covered the Step-1 Source Manifest's material owner classes:

```text
PO / interactivity: COVERED
runtime fast path + reasoning: COVERED
full CORE preload/rebuild: COVERED
Context Runtime / allocation: COVERED
known-ID routing / indexes: COVERED
HOT / SQLite: COVERED
publication / currentness / contention: COVERED
LIVE: COVERED
collaboration: COVERED
Story lifecycle + integration: COVERED
8 baseline Story registrations: COVERED ITEM-LEVEL
Story growth / sharding / LLM-facing shape / exact archive: COVERED ITEM-LEVEL
mutable 10 KiB invariant: COVERED
cleanup / retained refs: COVERED
host assurance: COVERED
verification proof classes: COVERED
current Class-A source measurement: REVALIDATED FOR CURRENT GAME TREE
```

No material contradictory owner was found. No previously closed Step-1 constraint was reopened.

---

## 8. Step-2 conclusion

```text
WP24_STEP2_COMPLETE: YES
CURRENT_HEAD_EVIDENCE_RECONCILED: YES
SOURCE_MANIFEST_COMPLETENESS_GATE: PASS FOR STEP 2
OWNER_CONFLICT_REQUIRING_HUMAN_DECISION: NO
HUMAN_DECISION_REQUIRED: NO
PO_DECISION_REQUIRED: NO
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
RECOMMENDED_DIRECTION: ALTERNATIVE B
STEP3_AUTHORIZED_BY_EXISTING_GO: YES
IMPLEMENTATION_PLANNING_STARTED: NO
IMPLEMENTATION_STARTED: NO
```

Proceed to Step 3 Decision Brief without an intermediate approval pause.