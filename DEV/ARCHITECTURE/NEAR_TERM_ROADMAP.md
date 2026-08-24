# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE PROGRAM ROADMAP**

Date: 2026-08-24

This file is the sequencing/status authority for Architecture Round 2.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Program decisions:

- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`

Evidence accounting:

- `DEV/docs/superpowers/research/2026-08-24-round-2-evidence-disposition-ledger.md`

This roadmap is the owner-approved **new Round-2 decomposition**. It supersedes the earlier R2.1–R2.9 thematic stage plan.

---

# 1. Program baseline

Round 1 remains a strong accepted architecture base.

The former Round-1 Step 6 is closed as a separate stage. Useful unresolved questions were reclassified under the current Round-2 dependency graph.

Current product/deployment baseline:

```text
primary AI host              ChatGPT
plan                         ChatGPT Plus
player-facing surface        ordinary public chat
physical LLM topology        one LLM / one physical chat context
ordinary gameplay execution  one user request / one assistant turn
private HDM hosting          OUT OF CURRENT SCOPE
direct model API calls       OUT OF CURRENT SCOPE
mandatory paid inference     OUT OF CURRENT SCOPE
future provider migration    compatibility concern only, not a current driver
```

Single-context role law:

> Physical availability of information does not make it logically eligible for the active HDM role.

System prompt, Project Instructions and shipped HDM reasoning/procedure instructions participate in role-containment machinery but do not become canonical-state authority.

---

# 2. Round-1 preservation rule

A closed Round-1 topic becomes active Round-2 architecture work only when current work:

1. materially extends the accepted contract;
2. exposes a contradiction or invalid assumption;
3. introduces a new consumer the accepted contract cannot satisfy; or
4. makes the accepted decision insufficient for a current requirement.

Independent confirmation or thematic overlap is evidence, not a new stage.

---

# 3. Evidence / activation rule

The current roadmap was derived from item-level accounting of all 24 DIAMOND and 58 STRONG candidates:

```text
ACTIVE / ACTIVE DELTA          43
INHERITED / ALREADY SATISFIED  16
CONDITIONAL / DORMANT          23
unaccounted                     0
```

Research classification is not backlog state.

A `CONDITIONAL / DORMANT` item creates no current task. Its original revisit trigger remains preserved in the evidence ledger.

RESERVE / NEGATIVE INTELLIGENCE remains stage-local adversarial evidence rather than automatic requirement scope.

---

# 4. Operating rules

- Exactly one numbered Round-2 stage may be `IN PROGRESS`.
- Later stages may be inspected only for dependency/contradiction visibility relevant to the active stage.
- Each stage follows task brief -> Source Manifest/evidence extraction -> alternatives/recommendation -> owner decision where required -> candidate specification -> adversarial review -> closure.
- Before Decision Brief, candidate specification, coverage claim or closure, the Source Manifest/evidence/synthesis-completeness gates must pass.
- Owning sources beat roadmaps, indexes, summaries and remembered state.
- YAGNI applies aggressively: no new authority, registry, scheduler, generic graph, plugin/agent framework or subsystem without a current requirement.
- Broad implementation remains blocked until Round-2 architecture closes and implementation planning is explicitly entered.
- This roadmap is living. Change the decomposition when evidence changes the dependency graph.
- Dormant work reserves no stage number. If a trigger becomes true, insert the smallest bounded stage where dependencies require it.

---

# 5. Stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | rebuild Round-2 problem horizon from accepted architecture + item-level research disposition | 82/82 DIAMOND/STRONG accounted; previous decomposition retired; dependency graph owner-approved |
| R2.1 | **COMPLETE / ARCHITECTURE CLOSED** | continuity, memory and history-aligned derived state | reuse-first continuity source/lifecycle model; Story admitted only as nonauthoritative orientation; history/exact/repair contracts closed |
| R2.2 | **COMPLETE / ARCHITECTURE CLOSED** | Actor continuity, cognition and directed relationships | source-Actor-owned sparse continuity; directed relationships; sparse cognition; player-agency and lazy-discovery handoff closed |
| R2.3 | **IN PROGRESS** | Context Runtime, retrieval, lazy discovery and allocation | bounded deterministic projection over R2.1/R2.2 sources with candidate discovery, complete-packet, budget, trace and degradation rules |
| R2.4 | **PLANNED** | single-context LLM execution and instruction architecture | one-request/one-assistant-turn role pipeline, rebinding, handoffs, instruction composition and deterministic authority gateway |
| R2.5 | **PLANNED** | collaboration and multiplayer interaction semantics | sync/async input, mode coordination, rejoin/catch-up and recipient-scoped context over inherited Step-5 shared-state architecture |
| R2.6 | **PLANNED** | ChatGPT-Plus assurance, evaluation, security and degradation | tested supported host envelope and explicit supported/degraded/unsupported behavior |
| R2.7 | **PLANNED** | machine-realization mapping and holistic closure | GAME/DEV/schema/catalog/instruction/test obligations mapped; cross-round review passed; implementation-planning entry criteria satisfied |

---

# 6. Dependency graph

```text
R2.0 Evidence Rebaseline
        |
        v
R2.1 Continuity / History-Aligned Derived State
        |
        v
R2.2 Actor Continuity / Cognition / Relationships
        |
        v
R2.3 Context Runtime / Retrieval / Lazy Discovery / Allocation
        |
        v
R2.4 Single-Context LLM Execution / Instructions
        |
        v
R2.5 Collaboration / Multiplayer Interaction
        |
        v
R2.6 ChatGPT Assurance / Evaluation / Security
        |
        v
R2.7 Machine Mapping / Holistic Closure
        |
        v
Implementation Planning
```

---

# 7. R2.0 — Evidence Rebaseline & Scope Reconstruction — COMPLETE

Closed results:

- current process/bootstrap and repository owners re-read;
- accepted Round-1 architecture reconciled against research;
- 82/82 DIAMOND/STRONG candidates individually dispositioned;
- `revisit when` / scope qualifiers preserved;
- active, inherited and dormant work separated;
- Actor-before-Context dependency established;
- no mandatory standalone Narrative Dynamics stage justified;
- no generic optional-capability gate justified;
- collaboration narrowed to deltas not already owned by Step 5;
- R2.1–R2.7 graph owner-approved.

---

# 8. R2.1 — Continuity, Memory & History-Aligned Derived State — COMPLETE

Artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-1-continuity-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-projection-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-resolution-gate.md`

Canonical result:

- no generic memory/continuity authority;
- current semantic questions remain with native owners;
- Story remains durable/noncanonical/optional but may serve eligible gameplay roles as broad/episodic orientation;
- material role decisions depending on current/source-specific correctness escalate to the proper source class;
- source-bound does not imply current;
- projection absence does not imply semantic absence;
- history alignment uses HDM-owned source refs/currentness/correction/semantic projection generation rather than host Retry/Edit ancestry;
- only admitted HDM evidence may enter durable continuity;
- stale/incompatible projections degrade to stronger evidence rather than guessing;
- entity continuity begins as a scoped view rather than a durable synopsis;
- exact recall remains Step-5.11 Selective Exact;
- no per-turn/background continuity-maintenance correctness clock.

---

# 9. R2.2 — Actor Continuity, Cognition & Directed Relationships — COMPLETE

Artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-cognition-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-2-actor-continuity-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-resolution-gate.md`

Canonical result:

- source Actor semantically owns current non-epistemic private continuity;
- `world.knowledge` remains proposition-stance authority;
- foundation / durable evolving cognition / transient private state are distinct lifetimes, not three stores;
- foundation changes require an explicit stronger transition boundary;
- goals/objectives/intentions/commitments remain sparse;
- relationships are directed source-Actor views with sparse typed facets and no universal scalar;
- objective social facts remain with native owners;
- Actor cognition is sparse/event-driven with explicit semantic purpose and valid `NO_CHANGE`;
- one assessment produces one bounded Actor-purpose delta rather than arbitrary whole-Actor rewrite;
- persisted transient state needs inspectable fictional invalidation rather than generic turn TTL;
- progressive materialization prevents incidental-NPC over-modeling;
- player-controlled voluntary mental state remains player-owned;
- Story/history may inform but not establish current cognition.

Mandatory R2.3 handoff from owner requirement:

> **LLM/runtime semantic detail SHALL be lazy-loaded. Full entity records are not required merely to discover potential scene/location/decision relevance.**

R2.2 therefore requires R2.3 to provide compact derived discovery metadata while preserving these constraints:

- discovery/index metadata is not semantic authority;
- omission is not general proof of absence;
- currentness follows routed/live authority;
- discovery is multi-channel, not location-only;
- secret-bearing metadata remains eligibility-protected;
- existing CURRENT/SCENE/INDEX/live surfaces are candidate realization inputs, not pre-selected final design.

R2.2 Diamond/Strong disposition is recorded item-by-item in its resolution gate.

---

# 10. R2.3 — Context Runtime, Retrieval, Lazy Discovery & Allocation — IN PROGRESS

Depends on: **R2.1, R2.2**.

R2.3 now owns the complete path from cheap candidate awareness to bounded role-local context construction.

Primary active research inputs:

- D02 — context as materialized bounded projection;
- D03 — semantic allocator/reservations/degradation;
- D04 — context assembly trace;
- D14 — complete decision packets before defer;
- D19 — typed reactive selectors;
- D24-delta — recipient/controlled-Actor scoped projections;
- S02 — multi-signal ranking;
- S22 — bounded dependency activation;
- S25 — centralized token/model-limit accounting;
- S29 — side-effect-free dry-run;
- S36 — witness/knowledge-aware retrieval;
- S40 — starvation/fairness;
- S48 — explicit entity/Actor targeting as hint;
- S49 — party-size-aware representation/budget;
- D18 retrieval realization;
- R2.1 source-aware dedup/Story-history escalation;
- R2.2 lazy-discovery/currentness/secrecy handoff.

Required decisions include at least:

### Discovery / lazy load

- first-tier scene/location/entity candidate manifest semantics;
- whether existing scene refs and campaign reverse indexes are sufficient, complementary or incomplete;
- candidate metadata needed to rank/filter before full entity load;
- discovery from physical co-location plus explicit refs, active threads, causal/process dependencies, ownership/relationship links and recent accepted evidence;
- false-negative protection when indexes are stale/incomplete;
- current/live routing and overlays;
- secret-safe pre-load metadata;
- fallback that avoids a global full-record scan.

### Selection / eligibility

- role/player/subject/purpose eligibility;
- typed selectors and bounded dependency activation;
- explicit entity/Actor targeting as hint, never privilege escalation;
- source/currentness verification before material use.

### Loading / representation

- `required | protected | downgradable | omittable` classes;
- complete minimum decision packets;
- representation ladder before omission/defer;
- broad/episodic/entity/exact retrieval;
- source-aware semantic dedup;
- token/model-limit accounting;
- party-size-aware degradation and starvation prevention.

### Trace / diagnostics

- dry-run assembly;
- inclusion/exclusion/currentness/eligibility/rank/budget/representation trace;
- secret handling inside trace;
- failure/defer behavior when correctness-critical context cannot be assembled completely.

Constraints:

- Context Runtime remains deterministic projection, not canon;
- no generic ACL authority, universal knowledge graph/query language or campaign-wide scan permission;
- archive availability does not imply preload;
- index omission does not imply semantic absence unless an exact exhaustive contract says so;
- R2.3 does not redesign upstream R2.1/R2.2 semantic owners.

Exit result:

> canonical bounded Context Runtime contract covering discovery -> select/verify -> lazy load -> project, with explainable budgets/degradation and correctness-safe failure behavior.

---

# 11. R2.4 — Single-Context LLM Execution & Instruction Architecture — PLANNED

Depends on: **R2.1–R2.3**.

Primary evidence: D16-delta, S21, S28, role-context Protocols 1–3, Step-4 single-context amendment, current host-feasibility evidence, useful non-superseded former Step-6 questions and reusable-instruction working note.

Scope includes one-turn envelope/activation, role rebinding, typed handoffs, deterministic authority/tool gateway, mechanics interleaving, Narrator/emission boundary, instruction ownership/composition/versioning and injection/role-confusion defense.

D16 does not imply separate subagents/background calls.

---

# 12. R2.5 — Collaboration & Multiplayer Interaction Semantics — PLANNED

Depends on: **R2.1–R2.4** plus inherited Step-5 multiplayer/live/chronology architecture.

Primary active research: D21, D22-delta, D23, S43, S44, S45, S54; D20/D24 and authenticated binding remain inherited constraints.

Scope is the collaboration/input/context delta: sync/async interaction, coordination modes, batching, OOC/diegetic/actionable separation, absence without PC takeover, catch-up/rejoin and recipient-scoped Context Runtime composition.

Do not redesign live CAS, campaign routing, chronology ownership or participant authentication without proven insufficiency.

---

# 13. R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation — PLANNED

Depends on concrete R2.1–R2.5 architecture.

Primary active research: S53-delta plus actual obligations produced upstream. D15 remains dormant unless retry evaluation triggers it.

Required behavior will be classified as:

```text
SUPPORTED
SUPPORTED WITH DOCUMENTED LIMITATION
DEGRADED MODE
UNSUPPORTED
```

Protocols 1–3 become regression evidence, not a reason to reopen mandatory physical isolation.

---

# 14. R2.7 — Machine Realization Mapping & Holistic Architecture Closure — PLANNED

Depends on: **R2.1–R2.6**.

Map accepted architecture to GAME runtime ownership/documents, DEV catalogs/schemas, seeds/templates/migrations, Project Instructions, shipped instruction assets, tests/evaluations, tooling/diagnostics and persistence obligations.

Closure includes cross-round authority/duplicate-owner review, Retry/recovery/concurrency composition, history/continuity/context consistency, Actor/context/role-containment composition, multiplayer recipient/secrecy composition, dormant-trigger preservation, full 82-candidate disposition recheck and stale derivative/status repair.

Implementation planning begins only after architecture blockers are closed and machine-realization/test obligations are explicit.

---

# 15. Explicitly removed mandatory stages

Round 2 has **no mandatory standalone Narrative Dynamics stage**. Existing preparation/process/NPC/narration architecture remains in force. Retained planning, staged world pressure, additional timeskip or anti-stagnation machinery appears only if a preserved dormant trigger becomes a real requirement and existing owners prove insufficient.

Round 2 has **no generic optional-capability gate**. Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers, cache-specific optimization and similar ideas remain dormant until their own triggers occur.

---

# 16. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  COMPLETE / ARCHITECTURE CLOSED
R2.2  COMPLETE / ARCHITECTURE CLOSED
R2.3  IN PROGRESS
R2.4  PLANNED
R2.5  PLANNED
R2.6  PLANNED
R2.7  PLANNED

R2.3 next activity:
    establish task-specific Source Manifest
    -> extract Context Runtime / lazy-discovery evidence
    -> alternatives/recommendation

Broad implementation: BLOCKED.
```