# R2.7 WP-24 Step 1 — Performance / Scale / Operational Budget — Task Brief + Source Manifest

Status: **SENIOR HOLD RECOVERY CANDIDATE — SR24-S1-01 / SR24-S1-02 REPAIRS APPLIED — MANDATORY INDEPENDENT SENIOR RE-REVIEW PENDING**

Date: 2026-09-08

Original Step-1 evidence basis: `1c3b85a509a592d0e11da6bc64d9119f5b543a4a`.

Senior-recovery evidence basis: `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`.

Domain: **Performance / scale / operational budget**.

Product Owner authorization: explicit authorization received on 2026-09-08 for **R2.7 WP-24 Step 1 only**. The current assignment is bounded recovery of that Step 1 after mandatory independent Senior HOLD.

Mandatory Senior findings under recovery:

```text
SR24-S1-01: BLOCKING — unsupported 120-second Product Owner law attribution
SR24-S1-02: SIGNIFICANT — full-CORE preload / cache-rebuild path omitted from framing
```

This artifact owns WP-24 Step-1 framing, task-specific Source Manifest, evidence classification and the repaired review-ready audit horizon. It does not authorize Step 2, Steps 2–8, implementation planning, substantive implementation, optimization implementation, release work, migration or gameplay bootstrap.

The mandatory whole-project Step-1 critic and recovery rerun are recorded in:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-24-step-1-whole-project-critic.md`.

---

## 1. Architecture Task Brief

WP-24 is a whole-project architecture audit of whether the accepted HDM runtime can remain bounded, responsive and operable as campaigns grow and as multiple chats contend for shared durable state. It is **not** a greenfield performance redesign and it is not permission to replace accepted semantic owners with storage- or transport-driven shortcuts.

The canonical WP-24 question horizon is:

1. Are normal-turn reads/writes bounded for realistic campaigns?
2. Do file count, GitHub API/directory limits, instruction-context loading/rebuild, campaign context loading, index size, publication call count and multi-chat contention have explicit architecture-level bounds/fallbacks?
3. Are optimization candidates distinguished from correctness requirements and guarded by revisit triggers?
4. Is any accepted design relying on background polling/workers/heartbeats unavailable in the target product?

Step 1 expands those questions into an auditable dependency graph without pre-deciding the eventual architecture result.

### 1.1 Required problem coverage for Steps 2–8

Subsequent WP-24 work, if Senior-authorized, must be able to investigate at least:

- realistic normal-operation workload and special-path composition;
- new-chat/substantial-setup instruction preload, package-switch cache rebuild, verified context-loss rehydration and ordinary-turn zero-CORE-reread as distinct paths;
- scaling dimensions and growth drivers;
- boundedness of discovery, hydration, role-context assembly, execution, materialization, durability, publication, Story, collaboration and maintenance paths;
- file, directory, index, Story and retained-ref growth;
- physical instruction-corpus size/rebuild cost separately from campaign context/resource pressure;
- context-loading/resource pressure and required/optional degradation;
- serial LLM/tool/Connector critical-path amplification;
- write/materialization/publication call count and conflict/retry amplification;
- multiplayer/multi-chat contention and source-currentness churn;
- fallback/degradation and terminal failure behavior;
- supported-host capability assumptions;
- absence/presence of polling, heartbeat, background-worker or scheduler dependencies;
- correctness-required performance/resource laws versus optional optimization candidates;
- safe defer/revisit triggers;
- correct verification/benchmark/evaluation route for each obligation class.

This is problem coverage, not an expected finding list.

### 1.2 Non-goals and hard boundaries

WP-24 Step 1 does **not**:

- invent a new runtime/storage/context/Story/collaboration owner;
- replace or theoretically redesign the accepted full-CORE preload strategy during this recovery;
- choose an index partition, cache, database layout, publication batching algorithm or retry algorithm;
- introduce a new numeric latency, throughput, file-count, record-count, call-count or cardinality target without an owning basis;
- infer an exact model token footprint from source bytes without a reliable owning codec/basis;
- weaken or silently replace accepted Product Owner performance/operability constraints;
- turn an optional optimization into correctness law;
- activate dormant work merely because it might improve performance;
- build a preimplementation surrogate, parallel MVP or fake gameplay runtime to obtain performance numbers;
- treat a DEV tool/generator/scaffold or source-corpus measurement as end-to-end gameplay latency/prompt-pressure proof;
- create background workers, queues, schedulers, polling loops or heartbeats merely to compensate for host limitations;
- introduce branch/ref deletion as cleanup or performance optimization;
- begin implementation, release, migration or gameplay bootstrap.

Accepted architecture is reopened only if current or later valid evidence establishes a new performance/scale consumer that makes it insufficient.

---

## 2. Evidence and proof classification

WP-24 preserves the WP-22 proof boundary.

### Class A — current existing-surface measurement

Permitted now when a concrete machine/tool/runtime surface already exists. Examples include current file sizes/counts, physical instruction-corpus bytes, current index/scaffold fan-out, a current tool's runtime, current bounded/unbounded scans, currently defined publication operations and structurally inspectable cardinality/growth characteristics.

A Class-A measurement proves only the measured surface under the stated basis. It does **not**, by itself, assert that the measured surface is complete, mature, production-representative, or suitable as a forecast or sizing baseline for the eventual production surface.

### Class B — future benchmark of realized implementation

Used after the relevant production path exists. This class can measure implemented read/write/materialization/publication path cost, index transfer/lookup behavior, instruction-cache construction mechanics, retry amplification and similar machine-realized properties.

### Class C — future production-like empirical evaluation of the real MVP/supported host

Used for genuinely host/LLM/Connector/user-visible properties such as end-to-end turn responsiveness, behavioral prompt pressure, long-campaign/long-chat context pressure, real Connector latency distributions, multi-chat contention behavior and supported-host degradation/gameplay quality.

Class C must use the real implemented MVP/supported host. A preimplementation parallel MVP is not equivalent evidence.

### Rule

```text
SPECIFICATION / STRUCTURAL BOUNDEDNESS
    != CURRENT PHYSICAL-SURFACE MEASUREMENT
    != REALIZED IMPLEMENTATION BENCHMARK
    != PRODUCTION-LIKE MVP EMPIRICAL ACCEPTANCE
```

Unknown future empirical results are not automatically current architecture defects. They become architecture defects only when current evidence already establishes an incompatible assumption or when a later trigger fires.

---

## 3. Settled constraints that WP-24 must consume, not reopen

| Constraint | Current owner | WP-24 Step-1 disposition |
|---|---|---|
| PO-003 historical-basis interactivity boundary | `DEV/PRODUCT_OWNER_INPUT.md` PO-003 + WP-19 `WP19-L38/L39` | **ACCEPTED STRUCTURAL PERFORMANCE LAW.** For PO-003 basis capture on the ordinary gameplay critical path: additional sequential LLM calls solely for capture = 0; additional serial remote/tool reads solely for capture when required T0 material is already admitted = 0; additional separate remote publications solely for basis = 0; irrelevant/trivial/`NO_CHANGE` turns do no basis work; added material is bounded typed items only. A later realization that requires an extra serial LLM/tool round trip is a material architecture/performance escalation. |
| No fixed turn time/token/step/complexity cap | `GAME/CORE/RUNTIME.md` reasoning-performance budget | **ACCEPTED RUNTIME LAW.** Performance is a stop rule for unnecessary deliberation, not a fixed ceiling that may force a knowingly weaker ruling. No current owner establishing a 120-second turn SLA was found in the recovery owner reconstruction. |
| Full exact-package instruction cache | `GAME/CORE/PLAY_POLICY.md`, `BOOTSTRAP_RUNTIME.md`, R2.4 `LAW R2.4-23`, WP-09 `LAW WP09-1` | **CURRENT PHYSICAL RUNTIME STRATEGY.** Complete local `CORE/*.md` plus `RULES/INDEX.md` and `RULES/README.md` preload once after exact package resolution and before gameplay/substantial setup; ordinary turns reuse the cache without CORE rereads; package switch and verified instruction-context loss rebuild the full cache. This is distinct from lazy campaign/RoleContext retrieval. |
| Mutable GitHub-backed runtime text artifact cap | `DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` | **ACCEPTED RUNTIME OPERABILITY LAW.** Final serialized UTF-8 mutable runtime artifacts are capped at 10,240 bytes. This is a project invariant, not a claimed vendor hard limit. |
| Bounded campaign/role context assembly | R2.3 + WP-09 | **CORRECTNESS / RESOURCE LAW.** Registered finite expansion, required floors first, optional reduction, terminal `UNSATISFIABLE`, one finite caller alternative; no ordinary campaign/history scan. Full engine-instruction preload does not relax this law. |
| Direct known-ID routing | WP-11 + WP-12 | **CORRECTNESS / BOUNDEDNESS LAW.** Known-ID hydration derives one route; no directory/index enumeration. Discovery uses expected family index then exact owner load. |
| Monolithic family indexes | WP-11 | **BASELINE + EXPLICIT WP-24 REVISIT TRIGGER.** Partitioning may be selected only on measured size/transfer/host-tool evidence while preserving authority/direct routing. |
| Publication/currentness discipline | WP-13 + publication-currentness repair | **CORRECTNESS LAW.** Bounded closure/currentness footprint, immutable attempt before remote mutation, one coherent campaign tree/commit boundary, non-force ref transition, typed conflict/indeterminate handling. |
| No background save heartbeat | WP-13 | **NEGATIVE CORRECTNESS/OPERABILITY LAW.** Clean risk-control evaluation creates no heartbeat; host inactivity does not promise wall-clock flush. |
| LIVE bounded authority lookup | WP-16 | **CORRECTNESS / BOUNDEDNESS LAW.** Per-target write authority uses bounded campaign routing/claim metadata; no WORLD/all-ref/all-LIVE scan. |
| Collaboration has no global scheduler/index | WP-17 | **NEGATIVE CORRECTNESS/OPERABILITY LAW.** No background scheduler, presence/heartbeat service, global registry or total frontier baseline. |
| Story backlog is derived/turn-local | WP-18 + Story integration contract | **NEGATIVE CORRECTNESS/OPERABILITY LAW.** No durable Chronicler queue/lease/heartbeat/worker state; bounded candidate windows and turn-local service; Story never blocks accepted gameplay publication. |
| Diagnostics are question-bounded | WP-21 | **CORRECTNESS / OPERABILITY LAW.** No package/campaign-wide telemetry scan implied, no background cleanup queue/service. |
| Branch/ref deletion | PO-006 owner decision + AGENTS + WP-21 | **ABSOLUTE PROHIBITION.** WP-24 may assess retained-ref operational cost, but cannot make deletion a performance optimization. |
| Host/LLM integrated behavior | R2.6 + WP-22 | **FUTURE EMPIRICAL OBLIGATION WHERE APPLICABLE.** Long-chat calibration, behavioral prompt pressure and integrated host behavior belong on the realized MVP, not a surrogate. |

### SR24-S1-01 owner-reconstruction result

Recovery re-read the actual current owners named by Senior plus neighboring current sources:

- `DEV/PRODUCT_OWNER_INPUT.md` PO-003;
- WP-19 canonical `WP19-L29..L39`, especially `WP19-L38/L39`;
- `DEV/docs/superpowers/specs/2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`;
- `GAME/CORE/PLAY_POLICY.md`;
- `GAME/CORE/RUNTIME.md`;
- current canonical architecture navigation as a locator only.

No current owning artifact was found that establishes `120 seconds` as an HDM turn/PLAY-NOW Product Owner law. The prior Step-1 attribution to PO-003 / `PLAY_POLICY.md` was therefore unsupported and is removed from current WP-24 framing. No replacement numerical SLA is invented.

The actual accepted PO-003/WP-19 zero-extra-serial law remains in force, and `RUNTIME.md` independently prevents converting performance pressure into a fixed time/token/step/complexity ceiling that weakens correctness.

---

## 4. Initial realistic workload / hot-path model

This model is a framing device for audit accounting, not a latency benchmark.

### 4.1 New chat / substantial setup — full instruction preload

After explicit campaign/new-game selection resolves the exact runtime package and `current_runtime_root`:

```text
exact runtime package resolved
-> load complete local CORE/*.md
-> load RULES/INDEX.md
-> load RULES/README.md
-> establish immutable current-chat engine instruction cache
-> only then proceed to substantial setup/gameplay
```

This is physical instruction-context loading. It is not campaign-data preload and not a RoleContextBundle. Audit dimensions include source-file count, aggregate source bytes, largest files, cache-construction path, host/context pressure and any serial loading/tool amplification in the realized supported target.

### 4.2 Engine package switch — full cache invalidation and rebuild

After a successful authorized engine migration/update selects a different exact package:

```text
bind exact target current_runtime_root
-> invalidate old engine instruction cache
-> rebuild complete target CORE + RULES routing cache
-> no further adjudication on a mixed/old cache
```

This is a special maintenance/update path, not ordinary-turn rereading. Later benchmark/evaluation must account for its full rebuild cost without turning it into a normal-turn tax.

### 4.3 Verified context loss / compaction — full cache rehydration

When runtime can positively determine that required engine instructions are no longer available because of context loss/compaction:

```text
verified instruction-context loss
-> rehydrate complete CORE + RULES routing cache once
-> resume against the restored exact package basis
```

Do not repeatedly reread individual CORE modules merely because they become relevant. A vague concern about context pressure is not itself permission to rebuild.

### 4.4 Ordinary single-player turn — already-loaded CORE fast path

Normal in-scene turns operate with the engine cache already present:

```text
already-loaded exact CORE instruction cache
+ already-loaded campaign working set where sufficient
-> bounded role/current-state work
-> deterministic execution as applicable
-> persistence only at an owning boundary
-> player-visible response
```

Fast-path properties from current runtime owners include:

- zero CORE rereads from disk/GitHub merely for module activation;
- no campaign/world preload merely because CORE is preloaded;
- no GitHub read/write/HEAD refresh in singleplayer when the current working set is sufficient and no persistence/sync boundary fires;
- targeted retrieval only for a concrete current dependency;
- PO-003 historical-basis capture adds no dedicated sequential LLM call/redundant admitted-data read/separate publication.

Audit dimensions:

- number of index/discovery lookups;
- number of exact owner body loads;
- amount of campaign material admitted to role context;
- LLM/tool calls on the serial path;
- native records touched/materialized;
- publication attempts and remote round trips;
- retries after currentness conflict;
- optional work that must degrade/yield before correctness-critical work.

### 4.5 Explicit SAVE / campaign publication

WP-13 already prevents whole-campaign closure scans and defines one coherent tree + commit + final non-force ref transition for one logical campaign durability boundary. WP-24 must audit the structural and realized cost of the bounded participating-source footprint, tree construction, preflight/currentness reads, final publication and conflict/ambiguity recovery without reopening publication authority.

### 4.6 LIVE multiplayer mutation

The path composes principal/PLAYER/control authorization, campaign routing, bounded `WriteAuthorityLookup`, exact LIVE source basis and exact-source CAS. WP-24 must treat multi-chat contention and stale-basis retry/rebuild as a separate amplification dimension rather than infer cost from single-writer publication.

### 4.7 Async collaboration

Durable collaboration is admitted only for bounded agency-dependent collection that must survive gaps. Ordinary correctness does not enumerate a collaboration directory or run a background scheduler. WP-24 must audit PLAYER companion/direct-route fan-out and contention, not invent an always-running collection service.

### 4.8 Story / retrospective consumer

Story uses layer-local projections and bounded source-candidate windows. Retrospective reading is typed through Context Runtime and does not require catch-up mutation or index repair. WP-24 must separately account for source enumeration, Story file growth, projection publication and retrospective acquisition; none may be treated as a mandatory same-turn global history scan.

### 4.9 Maintenance / diagnostics / retained repository residue

Maintenance evidence is bounded to a concrete question. Retained non-authoritative refs may accumulate indefinitely because automated deletion is forbidden. WP-24 must assess any host/repository discovery/listing/operational pressure caused by retained residue while preserving the invariant that physical existence is not authority and deletion is unavailable.

---

## 5. Scaling dimensions and structural cost ledger

Steps 2–8 must account for the following dimensions where applicable. No numeric limit is implied unless an owner or verified platform constraint supplies one.

| Dimension | Why it matters | Owning/bounding sources |
|---|---|---|
| CORE preload file count | new-chat/setup and rebuild source fan-out | PLAY_POLICY / BOOTSTRAP_RUNTIME / R2.4 |
| aggregate CORE + routing source bytes | physical preload/rebuild volume; source measurement only | current GAME corpus + preload owners |
| largest preload source files | single-source loading/tool envelope and rebuild composition | current GAME corpus + preload owners |
| cache rebuild frequency/path class | package switch/context loss must not become an ordinary-turn tax | PLAY_POLICY / BOOTSTRAP_RUNTIME |
| total native record count | long-campaign growth must not force ordinary global scans | WP-10/11/12/13 |
| per-family discoverable record count | monolithic index transfer/parse growth | WP-11, WP-24 trigger |
| per-record serialized bytes | runtime mutable transport safety | 10 KiB PO owner decision + native schemas |
| Story units per layer/source domain | retrospective corpus growth and candidate coverage | WP-18 + Story integration contract |
| retained planning/collaboration generations | multiplayer continuity pressure | WP-17/18/21 |
| retained non-authoritative refs | repository operational residue without deletion | PO-006 + WP-21 |
| active participants/chats | authorization, shared-state contention, collaboration fan-out | R2.5/WP-16/17 |
| records/files discovered | remote/tool cost and search boundedness | WP-09/11/12/16 |
| records/files fully loaded | campaign context/materialization pressure | R2.3/WP-09/Story integration |
| context/materialized bytes | conservative estimator/resource pressure where measurable | R2.3/WP-09/R2.6 |
| index lookups | discovery amplification | WP-11/12 |
| full scans | usually prohibited on ordinary runtime path; DEV/maintenance scans need separate classification | WP-09/13/16/21 |
| LLM calls | serial user-visible critical-path amplification | R2.4/R2.6 + role contracts + WP19-L38/L39 |
| Connector/API calls and remote round trips | target transport is fixed and serial portions can dominate | R2.6/WP-13/16 |
| writes/materializations | durability/publication and generated projection cost | WP-12/13/18 |
| publication attempts | one logical publication may include conflict/revalidation work | WP-13/16 |
| retry/conflict amplification | multi-chat/currentness churn can multiply reads/preparation/publication | WP-13/16/17 |

For each hot path, later analysis must distinguish **bounded by construction**, **bounded by registered finite policy**, **owner-bounded but realization deferred**, **empirical measurement required**, and **candidate unbounded gap**.

Physical source bytes are not model token occupancy. Host prompt pressure and gameplay behavior remain empirical where their owners say so.

---

## 6. Source Manifest methodology

The Source Manifest was reconstructed from current `DEV/PROJECT_MAP.md`, current progress/roadmap authority, explicit PO inputs, current R2.7 scope owner, semantic owners, current CORE/runtime projections, schemas/index scaffold, tooling/tests and downstream verification owners. The Senior recovery independently re-routed disputed performance and instruction-cache claims through their current owners instead of trusting the first Step-1 prose.

Disposition vocabulary:

```text
SETTLED_CONSTRAINT
    accepted owner already fixes the relevant architecture law

BOUNDED_BY_ACCEPTED_DESIGN
    accepted design supplies a structural/finite bound, but realization still needs later proof

REALIZATION_DEBT_ALREADY_ROUTED
    architecture is accepted; exact implementation/schema/test surface remains explicitly downstream

EMPIRICAL_AFTER_REALIZATION
    meaningful proof requires realized implementation or production-like MVP

MEASURE_NOW_SUPPORTING_ONLY
    current existing surface can be measured now, with narrow scope

WP24_REVISIT_TRIGGER
    accepted owner explicitly delegates a decision to WP-24 when evidence fires the trigger

NEGATIVE_EVIDENCE
    owner explicitly rejects a mechanism/assumption relevant to performance framing
```

---

## 7. Source Manifest — process / program / Product Owner authority

| Source | Role in WP-24 | Disposition |
|---|---|---|
| `AGENTS.md` | bootstrap, repository transport, write fence, branch/ref deletion prohibition, taxonomy, Version Impact | SETTLED_CONSTRAINT |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | Connector-only development transport and publication verification discipline | SETTLED_CONSTRAINT |
| `DEV/DESIGN_PROCESS.md` | Source Manifest/evidence/synthesis gates; measurable quality attributes; no invented numerical budgets | SETTLED_CONSTRAINT |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | 8-step architecture loop; whole-project Step-1 critic; mandatory Senior stop | SETTLED_CONSTRAINT |
| `DEV/PROJECT_MAP.md` | dependency-subgraph reconstruction and machine/runtime/test routing | SETTLED_CONSTRAINT |
| `DEV/CURRENT_PROGRESS.md` | sole current program cursor | synchronized by this recovery checkpoint |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | R2.7 sequencing/scope only | SETTLED_CONSTRAINT |
| `DEV/PRODUCT_OWNER_INPUT.md` | PO-003 immutable interactivity concern and routed zero-extra-serial performance law | SETTLED_CONSTRAINT; **does not own a 120-second SLA** |
| WP-19 canonical spec | `WP19-L38/L39` zero-extra-serial basis-capture law and escalation trigger | SETTLED_CONSTRAINT |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | human-vs-agent decision boundary | SETTLED_CONSTRAINT |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` + owner clarification | canonical WP-24 question horizon and R2.7 audit boundary | SETTLED_CONSTRAINT |
| runtime mutable artifact-size owner decision | 10 KiB mutable GitHub text hard invariant and revisit triggers | SETTLED_CONSTRAINT |
| branch/ref deletion prohibition owner decision | retained-ref cost may be studied; deletion cannot be selected | SETTLED_CONSTRAINT / NEGATIVE_EVIDENCE |

No new Product Owner decision is required by Step-1 recovery.

---

## 8. Source Manifest — semantic and realization owners

| Source / owner | Performance-scale relevance | Step-1 result |
|---|---|---|
| R2.3 Context Runtime | finite registered campaign discovery/expansion, required floors, optional degradation; downstream context-pressure evaluation | BOUNDED_BY_ACCEPTED_DESIGN + EMPIRICAL_AFTER_REALIZATION |
| R2.4 Single-Context Execution | one physical turn/context; logical role phases do not imply calls; `LAW R2.4-23` preserves full preloaded CORE; exact timing/token thresholds rejected | SETTLED_CONSTRAINT + EMPIRICAL_AFTER_REALIZATION |
| R2.6 MVP Host Assurance | conservative hidden-capacity-independent estimator; fixed Connector path; real-MVP integrated evaluation; no parallel MVP | SETTLED_CONSTRAINT + EMPIRICAL_AFTER_REALIZATION |
| WP-09 | exact-package full CORE cache explicitly distinct from bounded campaign packet; no generic background context service | SETTLED_CONSTRAINT + BOUNDED_BY_ACCEPTED_DESIGN |
| `GAME/CORE/PLAY_POLICY.md` | full CORE preload, loaded-vs-active separation, zero ordinary CORE reread, bounded runtime research/latency priority | SETTLED_CONSTRAINT |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | exact-package selection, full cache creation, package-switch invalidation/rebuild and verified-loss rehydration | SETTLED_CONSTRAINT; MEASURE_NOW_SUPPORTING_ONLY for physical corpus |
| `GAME/CORE/RUNTIME.md` | ordinary working-set fast path and reasoning stop rule; prohibits fixed time/token/step/complexity cap | SETTLED_CONSTRAINT / NEGATIVE_EVIDENCE against invented SLA |
| `GAME/CORE/STORAGE.md` | separate native files, compact discovery indexes, hot/cold routing expectations | BOUNDED_BY_ACCEPTED_DESIGN |
| WP-10 | durable native family census / owner allocation | scaling-family inventory input |
| WP-11 | exact direct routes, sharding, monolithic discoverable indexes, WP-24 partition trigger | SETTLED_CONSTRAINT + WP24_REVISIT_TRIGGER |
| WP-12 | typed HOT/SQLite, exact known-ID hydration, rebuildable narrow helpers, no external I/O inside SQLite transaction | BOUNDED_BY_ACCEPTED_DESIGN; exact physical tuning deferred |
| `GAME/CORE/PERSISTENCE.md` + WP-13 | bounded durability closure, publication attempt, ref transition, retries/currentness | BOUNDED_BY_ACCEPTED_DESIGN; publication-call/round-trip benchmark later |
| WP-14/15 | recovery/checkpoint and chronology owners | prevent performance shortcuts from turning derived order/cache into authority |
| `GAME/CORE/LIVE_SCENE.md` + WP-16 | bounded write-authority lookup, exact-source CAS, no all-ref/all-LIVE scan | BOUNDED_BY_ACCEPTED_DESIGN; contention empirical later |
| `GAME/CORE/MULTIPLAYER.md` + WP-17 | async collection without scheduler/heartbeat/global registry | BOUNDED_BY_ACCEPTED_DESIGN + NEGATIVE_EVIDENCE |
| WP-18 | layer-local Story, derived backlog, turn-local Chronicler, ephemeral SP planning | BOUNDED_BY_ACCEPTED_DESIGN + NEGATIVE_EVIDENCE |
| Story Producer/Persistence/Retrospective Consumer integration spec | bounded candidate bundles, typed retrospective capability, no always-running process/additional service, read does not force catch-up mutation | BOUNDED_BY_ACCEPTED_DESIGN; implementation not activated |
| WP-20 | migration/evolution boundary | performance cannot silently become migration work; package-switch measurements do not authorize migration |
| WP-21 | bounded diagnostics, cleanup classes, retained refs logical only, no background cleanup service | BOUNDED_BY_ACCEPTED_DESIGN + NEGATIVE_EVIDENCE |
| WP-22 | proof/evaluation taxonomy and real-MVP boundary | SETTLED_CONSTRAINT |
| WP-23 | release/readiness boundary | performance evidence must not be mislabeled as release acceptance | SETTLED_CONSTRAINT |

Closed semantic owners are inputs. WP-24 does not reopen them merely because a performance topic overlaps them.

---

## 9. Source Manifest — machine, physical corpus, scaffold, tool and test surfaces

### 9.1 Current instruction-corpus surface inspected — SR24-S1-02 Class A

Current exact source basis: `80649df2ff16f791d2abbeb0403e74bff8cf1d1b`.

Connected GitHub directory metadata for the exact current `GAME/CORE/` and `GAME/RULES/` source tree gives:

```text
CORE/*.md file count                    45
aggregate CORE/*.md bytes              364,844 B
RULES/INDEX.md                           1,752 B
RULES/README.md                          4,132 B
total preload-source file count             47
total preload-source bytes             370,728 B
```

Largest current preload sources by serialized repository byte size include:

```text
CORE/RUNTIME.md                20,143 B
CORE/BOOTSTRAP_RUNTIME.md      19,957 B
CORE/LIVE_SCENE.md             19,097 B
CORE/CAMPAIGN_SETUP.md         18,946 B
CORE/MULTIPLAYER.md            18,028 B
CORE/ENGINE_UPDATES.md         17,526 B
CORE/GM_CRAFT.md               15,372 B
CORE/PLAY_POLICY.md            15,210 B
CORE/CHARACTER_READINESS.md    14,500 B
CORE/AI_REASONING.md           10,849 B
```

Classification:

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

The current `370,728 B` result is therefore **not** a forecast, sizing baseline, or representativeness claim for the eventual production CORE corpus. Material corpus growth remains an explicit WP-24 scaling variable, and any later sizing claim must be re-measured against the then-current realized/production-relevant corpus under the appropriate evidence class.

No bytes-to-token conversion is made because no current owner supplies a stable exact codec/capacity contract that would justify one.

### 9.2 Current runtime/scaffold surfaces inspected

- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/PLAY_POLICY.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/MULTIPLAYER.md`;
- `GAME/CORE/LIVE_SCENE.md`;
- `GAME/CAMPAIGN/INDEX/` current scaffold metadata;
- current `DEV/SCHEMAS/` inventory as machine-realization evidence routing, not as proof that all later R2.7 contracts are implemented.

Current scaffold `GAME/CAMPAIGN/INDEX/` metadata remains the earlier narrow Step-1 Class-A measurement:

```text
EVENT_INDEX.yaml     49 bytes
FACTION_INDEX.yaml   51 bytes
ITEM_INDEX.yaml      48 bytes
LOCATION_INDEX.yaml  52 bytes
LORE_INDEX.yaml      48 bytes
NPC_INDEX.yaml       47 bytes
PC_INDEX.yaml        46 bytes
PLAYER_INDEX.yaml    50 bytes
SCENE_INDEX.yaml     49 bytes
```

These are measurements of the **current shipped scaffold files only**. They are not evidence of long-campaign index size, transfer latency or the WP-11 partition trigger. No partition decision is justified by these scaffold values.

WP-11's 65,536 leaf-bucket route space is an accepted structural route property, not a claim that 65,536 directories/files exist in a campaign and not a performance SLA.

### 9.3 Existing measurement evidence reused, not re-executed

The 10 KiB owner decision records earlier Connector whole-file probes demonstrating payload-shape-dependent behavior. Step 1 consumes that approved conclusion; it did **not** rerun those probes and does not reinterpret them as a vendor hard limit.

### 9.4 Tool / CI / test surfaces

- `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md` currently defines scenario obligations for exact-engine selection, complete CORE preload, loaded-not-active behavior, no CORE reread, no scene-change eviction, package-switch invalidation/rebuild and context-loss rehydration;
- those scenario cases establish/guard the intended contract shape, but file presence is not empirical execution evidence under WP-22;
- `DEV/TOOLS/run_maintenance_audit.py` — current repository/source maintenance audit; useful for source integrity, not gameplay latency proof;
- `.github/workflows/validate.yml` — hosted push/PR validation runs maintenance audit + all `DEV/TESTS` unittests;
- owner-specific regression tests and scenario suites mapped by WP-22 — later performance verification must use proof classes matching the claim;
- static/catalog/schema/maintenance checks may prove structural contracts, but not host/LLM/Connector end-to-end responsiveness or prompt-pressure/gameplay-quality acceptance.

A DEV-wide audit or generator scan may legitimately be broad because its operational class differs from ordinary gameplay. Its existence does not license an ordinary runtime full scan.

### 9.5 Future real-target full-preload evaluation trigger

If the complete physical CORE preload remains the intended realized production strategy, the realization/acceptance route must preserve an explicit future empirical obligation:

```text
real implemented supported target
-> production-like matched evaluation
-> current full-preload strategy vs an appropriate controlled/routed comparison where the evaluation design can do so without changing semantic law
-> inspect behavioral prompt pressure
   + procedural verbosity / unnecessary checks or retrievals
   + GM/NPC initiative and improvisation quality
   + context/resource pressure
   + latency/tool-call amplification
   + gameplay quality / degradation behavior
-> classify observed material failure under current owner/revisit rules
```

This obligation does **not** assert that the full-preload strategy is defective. It preserves the R2.4/R2.6/WP-22 evidence boundary: scenario/static proof can establish the preload contract, while behavioral/context/latency/gameplay-quality claims require the real implemented supported target. No preimplementation surrogate or parallel MVP is authorized.

---

## 10. Explicit background-service census

Current accepted owners inspected in the WP-24 dependency graph do **not** require an always-running runtime service for correctness:

| Concern | Accepted result |
|---|---|
| risk-control SAVE cadence | no clean heartbeat; no background exact wall-clock flush when host is inactive |
| Context Runtime | ephemeral request-local controls; no generic memory/vector/graph service or persistent fairness ledger |
| collaboration | no background scheduler, presence/heartbeat service or global obligation registry baseline |
| Story/Chronicler | no durable queue, lease, heartbeat, worker-state or backlog record; service is turn-local/derived |
| diagnostics/cleanup | no background cleanup queue/service |
| single-player Dramaturg | ephemeral; recompute on loss/staleness |

The recovery critic repeated the negative dependency sweep over the newly added instruction-cache path and found no autonomous worker/heartbeat requirement there either: preload/rebuild is foreground/event-driven after exact package selection, package switch or positively verified instruction-context loss.

---

## 11. Audit questions carried forward after repaired Step-1 evidence extraction

If mandatory independent Senior re-review later authorizes Step 2, research must answer, without presupposing a redesign:

1. Which ordinary gameplay read/discovery paths are structurally finite, and which still depend on owner-supplied finite registrations that lack a realized machine bound?
2. Which native family indexes can realistically approach the 10 KiB mutable-file cap or connected-tool envelope as campaign cardinality grows, and what measurement basis would fire WP-11's partition trigger?
3. Does any normal publication path have remote-call or retry amplification not already terminally bounded by current owner law?
4. Where can multi-chat contention multiply source revalidation/publication work, and what correctness-preserving degradation/fallback exists?
5. How do Story source enumeration/coverage and retrospective acquisition remain bounded as history grows without turning Story omission into semantic absence or requiring global catch-up?
6. What is the operational cost of retained non-authoritative refs under PO-006, and can all ordinary authority lookup avoid enumerating them?
7. Which context/resource/calibration questions can be proven structurally, which require realized benchmarks, and which require production-like MVP evaluation?
8. How do full-CORE initial preload, package-switch rebuild and verified-loss rehydration scale with the shipped instruction corpus, while ordinary turns preserve zero CORE reread?
9. On the real implemented supported target, does the intended full-preload strategy preserve acceptable behavioral/context/resource characteristics, or does its explicit empirical revisit route fire?
10. Which optional optimizations have a concrete revisit trigger, and which have no evidence sufficient to activate them?
11. Are there machine/schema/test gaps that are realization debt rather than architecture defects, and does any such debt currently prevent a bounded implementation?
12. Does the composed ordinary critical path preserve PO-003/WP-19 zero-extra-serial basis capture and `RUNTIME.md`'s decision-scoped fast path without fabricating a numeric turn SLA?

---

## 12. Source Manifest completeness gate

Repaired Step-1 completeness result:

```text
PROCESS OWNERS: COVERED
CURRENT PROGRAM / PO AUTHORITY: COVERED
R2.7 WP-24 SCOPE OWNER: COVERED
PO-003 / WP-19 TRUE PERFORMANCE OWNER: COVERED
FULL CORE PRELOAD / CACHE-REBUILD OWNERS: COVERED
CONTEXT / HOST / ROLE RESOURCE OWNERS: COVERED
STORAGE / ROUTING / HOT / PUBLICATION OWNERS: COVERED
LIVE / MULTIPLAYER / COLLABORATION OWNERS: COVERED
STORY / RETROSPECTIVE / PLANNING OWNERS: COVERED
DIAGNOSTICS / RETENTION / RETAINED-REF OWNERS: COVERED
CURRENT CORE CONSUMERS: COVERED
SCHEMA / SCAFFOLD / TOOL / TEST / CI ROUTES: COVERED FOR STEP-1 FRAMING
WP-22 EVIDENCE-CLASS BOUNDARY: COVERED
NEGATIVE EVIDENCE / DORMANT-TRIGGER DISCIPLINE: COVERED
SENIOR HOLD FINDINGS SR24-S1-01 / SR24-S1-02: INCORPORATED
RECOVERY WHOLE-PROJECT CRITIC RERUN: COMPLETE
RECOVERY-RERUN NEW BLOCKING FINDINGS: 0
RECOVERY-RERUN NEW SIGNIFICANT FINDINGS: 0
UNRESOLVED BLOCKING SOURCE-MANIFEST OMISSION: 0
UNRESOLVED SIGNIFICANT SOURCE-MANIFEST OMISSION: 0
```

This is **complete for repaired WP-24 Step-1 framing**, not a claim that every file in the repository was read or that later Step-2 evidence extraction is already complete. The dependency subgraph was reconstructed through current routing/owners rather than thematic sampling, and the Senior-exposed omissions/false attribution were reconciled before re-review.

---

## 13. Decision / defer posture

No new Product Owner decision is required by this Step-1 recovery.

Current accepted numerical performance/resource law in this framing includes the `10 KiB` mutable runtime text cap. PO-003/WP-19 supplies a **zero-extra-serial structural critical-path law**, not a 120-second SLA. `RUNTIME.md` rejects an invented fixed time/token/step/complexity ceiling on turn reasoning.

Potential index partitioning, alternate instruction loading/cache strategies, cache/materialization optimizations, call reductions, batching/tuning and other optimizations remain **inactive candidates** until their owning evidence/revisit trigger is established. The full-CORE preload strategy is not reopened by this recovery; its physical costs are now in scope and its real-target behavioral/context/latency evaluation obligation is explicit.

Future empirical obligations remain future empirical obligations; they are not converted into current defects merely because they have not yet run.

If later evidence exposes a product-visible trade-off whose numeric value materially changes UX/behavior and cannot be technically derived from existing law/platform constraints, the applicable later WP-24 artifact must provide a decision-ready Product Owner residual with evidence, alternatives, consequences, recommendation and the exact unresolved human choice.

---

## 14. Step-1 recovery gate

```text
WP24_LAUNCH_AUTHORIZED_BY_PO: YES
WP24_STEP1_TASK_BRIEF_COMPLETE: YES
WP24_SOURCE_MANIFEST_COMPLETE_FOR_STEP1: YES
WP24_STEP1_EVIDENCE_EXTRACTION_SUFFICIENT_FOR_FRAMING: YES
WP24_STEP1_SENIOR_REVIEW_PREVIOUS_RESULT: HOLD
SR24-S1-01: REPAIR APPLIED / PENDING SENIOR RE-REVIEW
SR24-S1-02: REPAIR APPLIED / PENDING SENIOR RE-REVIEW
WP24_STEP1_RECOVERY_WHOLE_PROJECT_CRITIC_RERUN_COMPLETE: YES
WP24_STEP1_RECOVERY_NEW_BLOCKING: 0
WP24_STEP1_RECOVERY_NEW_SIGNIFICANT: 0
WP24_STEP1_UNRESOLVED_BLOCKING: 0
WP24_STEP1_UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
WP24_STEP2_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
NEXT_GATE: MANDATORY INDEPENDENT SENIOR RE-REVIEW OF REPAIRED WP-24 STEP 1
```

**STOP FOR MANDATORY INDEPENDENT SENIOR RE-REVIEW.**
