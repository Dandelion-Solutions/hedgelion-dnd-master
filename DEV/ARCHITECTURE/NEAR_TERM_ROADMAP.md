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

Inherited examples include:

- LLM interpretation/proposal versus deterministic mechanical commit;
- objective truth versus fictional knowledge versus human disclosure;
- Story nonauthority;
- accepted gameplay/RNG not replayed because presentation is retried;
- Step-5 durability/recovery/currentness/concurrency foundations;
- Git/transport order not defining fictional chronology;
- selective exact versus semantic history principles.

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
| R2.2 | **IN PROGRESS** | Actor continuity, cognition and directed relationships | bounded Actor private/durable/transient state model compatible with Step-4 epistemics and player agency |
| R2.3 | **PLANNED** | Context Runtime, retrieval and allocation | bounded deterministic projection over admitted R2.1/R2.2 sources with complete-packet, budget, trace and degradation rules |
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
R2.3 Context Runtime / Retrieval / Allocation
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

R2.0 replaced the previous thematic problem-horizon claim with source-backed accounting.

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

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`

Evidence ledger:

- `DEV/docs/superpowers/research/2026-08-24-r2-1-continuity-evidence-ledger.md`

Owner decision:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-projection-owner-decision.md`

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`

Adversarial review / closure:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-resolution-gate.md`

Canonical result:

- no generic memory/continuity authority;
- current semantic questions remain with native owners;
- Story remains durable/noncanonical/optional but may serve eligible gameplay roles as broad/episodic orientation;
- material role decisions depending on current/source-specific correctness escalate to the proper source class;
- source-bound does not imply current;
- projection absence does not imply semantic absence;
- history alignment uses HDM-owned source refs/currentness/correction/semantic projection generation, not host Retry/Edit ancestry;
- only admitted HDM evidence may enter durable continuity;
- stale/incompatible projections degrade to stronger evidence rather than guessing;
- entity continuity begins as a scoped view rather than a durable synopsis;
- exact recall remains Step-5.11 Selective Exact;
- no per-turn/background continuity-maintenance correctness clock.

R2.1 active research items are fully dispositioned in its resolution gate. Conditional entity synopsis / separate projection machinery remains dormant until a downstream trigger proves need.

---

# 9. R2.2 — Actor Continuity, Cognition & Directed Relationships — IN PROGRESS

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-cognition-task-brief.md`

Depends on: **R2.1**.

## Why before Context Runtime

R2.2 defines Actor-owned/private source semantics that R2.3 will later select. Projection machinery must not invent upstream state semantics for retrieval convenience.

## Primary active research inputs

D10, D11-delta, D12-delta, D13, S07, S10, S11; specialized D09/S27 application where Actor mutation needs it.

## Required decisions

- stable foundation versus durable evolving continuity versus transient Actor state;
- exact boundary of `world.knowledge` versus other Actor-private cognition;
- goals/intentions/promises/private plans;
- directional `A -> B` relationship semantics;
- minimum useful relationship dimensions;
- evidence-bound persistent updates;
- `NO_CHANGE`;
- sparse/event-driven cognition;
- transient expiry/refresh using appropriate fictional-time semantics;
- active/relevant Actor depth without over-modeling;
- PC agency exclusions;
- explicit R2.3 source contract for resulting Actor state.

## Inherited constraints

- `world.knowledge` remains current proposition-stance owner;
- objective truth remains separate;
- Story/generic continuity is not current Actor cognition;
- consuming information does not automatically establish belief/knowledge;
- player voluntary belief/emotion/interpretation is not silently committed;
- LLM cognition output remains proposal until proper validation/commit.

## Exit

Bounded Actor continuity architecture with one owner per semantic concern, lifecycle/evidence rules, directional relationships, sparse cognition and explicit R2.3 handoff.

---

# 10. R2.3 — Context Runtime, Retrieval & Allocation

Depends on: **R2.1, R2.2**.

Primary active research inputs:

D02, D03, D04, D14, D19, D24-delta, S02, S22, S25, S29, S36, S40, S48, S49, plus D18 retrieval realization and R2.1 dedup requirements.

Required scope:

- context candidate/source metadata;
- role/player/subject eligibility;
- `required | protected | downgradable | omittable`;
- complete decision packets;
- representation downgrade before defer;
- broad/episodic/entity/exact retrieval;
- typed selectors/dependency activation;
- source-aware dedup;
- token/model-limit accounting;
- party-size degradation;
- starvation/fairness;
- dry-run;
- inclusion/exclusion/representation trace;
- failure/defer when correctness-critical context is incomplete.

Context Runtime remains deterministic projection, not canon, ACL authority, generic knowledge graph, universal query language or campaign-wide scan permission.

---

# 11. R2.4 — Single-Context LLM Execution & Instruction Architecture

Depends on: **R2.1–R2.3**.

Primary evidence:

D16-delta, S21, S28, role-context Protocols 1–3, Step-4 single-context amendment, current host-feasibility evidence, useful non-superseded former Step-6 questions and the reusable-instruction working note.

Required scope:

- one-turn envelope and phase activation;
- role rebinding and Actor-to-Actor public/private transfer semantics;
- minimal typed handoffs/results and retry/freeze lifecycle;
- deterministic tool/validation/commit gateway and mechanics interleaving;
- Narrator/emission boundary;
- stable constitution vs Project Instructions vs shipped procedures vs role frame;
- admit/partial/reject reusable first-party procedure modules;
- instruction versioning/regression;
- untrusted text as data and injection/role-confusion defense;
- no hidden chain-of-thought persistence requirement.

D16 does not imply separate subagents/background calls.

---

# 12. R2.5 — Collaboration & Multiplayer Interaction Semantics

Depends on: **R2.1–R2.4** plus inherited Step-5 multiplayer/live/chronology architecture.

Primary active research:

D21, D22-delta, D23, S43, S44, S45, S54; D20/D24 and authenticated binding as inherited constraints.

Required scope:

- sync versus async interaction;
- free-form versus strict-sequence coordination;
- multi-participant input collection/batching;
- OOC/social vs diegetic vs actionable intent;
- absence without implicit PC takeover;
- catch-up and join/rejoin conversational/action frontier;
- split-party context integration over existing scene/chronology frontiers;
- recipient-scoped Context Runtime outputs;
- shared-established outcome vs local retry/correction.

Do not redesign live CAS, campaign routing, chronology ownership or participant authentication without proven insufficiency.

---

# 13. R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation

Depends on concrete R2.1–R2.5 architecture.

Primary active research: S53-delta plus actual obligations produced upstream. D15 remains dormant unless retry evaluation triggers it.

Assurance areas:

- long-chat/context behavior;
- role-containment/cross-Actor contamination;
- instruction conflict/drift;
- injection/untrusted data;
- player-visible host surfaces;
- Retry/Edit/branch;
- latency/tool failure;
- context-incomplete/defer behavior;
- recovery after context loss;
- model/reasoning-profile change;
- gameplay-quality/over-completion regressions;
- diagnostics without secret exposure.

Classify required behavior as:

```text
SUPPORTED
SUPPORTED WITH DOCUMENTED LIMITATION
DEGRADED MODE
UNSUPPORTED
```

Protocols 1–3 become regression evidence, not a reason to reopen mandatory physical isolation.

---

# 14. R2.7 — Machine Realization Mapping & Holistic Architecture Closure

Depends on: **R2.1–R2.6**.

Map accepted architecture to:

- GAME runtime ownership/documents;
- DEV catalogs/schemas;
- seeds/templates/migrations;
- Project Instructions and shipped instruction/procedure assets;
- tests/evaluations;
- tooling/diagnostics;
- persistence obligations.

Closure review must include:

- cross-round authority/duplicate-owner sweep;
- Retry/recovery/concurrency composition;
- history/continuity/context consistency;
- Actor/context/role-containment composition;
- multiplayer recipient/secrecy composition;
- dormant-trigger preservation;
- full 82-candidate disposition recheck;
- stale derivative/status/navigation repair;
- implementation/deferred/dormant/debt classification.

Implementation planning begins only after no architecture blocker remains and machine-realization/test obligations are explicit.

---

# 15. Explicitly removed mandatory stages

Round 2 has **no mandatory standalone Narrative Dynamics stage**. Existing preparation/process/NPC/narration architecture remains in force. Retained planning, staged world pressure, additional timeskip or anti-stagnation machinery appears only if a preserved dormant trigger becomes a real requirement and existing owners prove insufficient.

Round 2 has **no generic optional-capability gate**. Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers, cache-specific optimization and similar ideas remain dormant until their own triggers occur.

---

# 16. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  COMPLETE / ARCHITECTURE CLOSED
R2.2  IN PROGRESS
R2.3  PLANNED
R2.4  PLANNED
R2.5  PLANNED
R2.6  PLANNED
R2.7  PLANNED

R2.2 next activity:
    establish task-specific Source Manifest
    -> extract Actor/cognition/relationship evidence
    -> alternatives/recommendation

Broad implementation: BLOCKED.
```
