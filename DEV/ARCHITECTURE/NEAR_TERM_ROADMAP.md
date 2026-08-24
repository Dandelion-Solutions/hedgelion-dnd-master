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

This roadmap is a **new decomposition**. It supersedes the earlier Round-2 R2.1–R2.9 stage plan rather than polishing or preserving that stage structure.

---

# 1. Program baseline

Round 1 remains a strong accepted architecture base.

The former Round-1 Step 6 is closed as a separate stage. Its useful unresolved questions were reclassified under the current Round-2 dependency graph.

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

The system prompt, Project Instructions and shipped HDM reasoning/procedure instructions are part of role-containment machinery, but they do not become canonical-state authority.

---

# 2. Round-1 preservation rule

A closed Round-1 topic becomes active Round-2 architecture work only when current work:

1. materially extends the accepted contract;
2. exposes a contradiction or invalid assumption;
3. introduces a new consumer that the accepted contract cannot satisfy; or
4. makes the accepted decision insufficient for a current requirement.

Independent confirmation or thematic overlap is not a new stage.

Examples inherited rather than reopened:

- LLM interpretation/proposal versus deterministic mechanical commit;
- objective truth versus fictional knowledge versus human disclosure;
- Story nonauthority;
- accepted gameplay/RNG not replayed because presentation is retried;
- Step-5 durability/recovery/currentness/concurrency foundations;
- Git/transport order not defining fictional chronology;
- selective exact versus semantic history principles.

---

# 3. Evidence/activation rule

The current roadmap was derived from item-level accounting of all 24 DIAMOND and 58 STRONG research candidates.

Current disposition:

```text
ACTIVE / ACTIVE DELTA          43
INHERITED / ALREADY SATISFIED  16
CONDITIONAL / DORMANT          23
unaccounted                     0
```

Research classification is not a backlog state.

A `CONDITIONAL / DORMANT` item creates no immediate task. Its explicit revisit trigger is preserved in the evidence ledger.

RESERVE / NEGATIVE INTELLIGENCE records remain stage-local adversarial evidence. This roadmap does not claim that every such record is an activated requirement.

---

# 4. Operating rules

- Exactly one numbered Round-2 stage may be `IN PROGRESS`.
- Later stages may be inspected only to expose dependencies/contradictions relevant to the active stage.
- Each stage follows task brief -> source extraction/research -> alternatives/recommendation -> owner decision where required -> candidate specification -> adversarial review -> closure.
- Before a Decision Brief, candidate specification, coverage claim or closure claim, the Source Manifest/evidence/completeness gates must pass.
- Owning sources beat roadmaps, indexes, summaries and remembered state.
- YAGNI applies aggressively: no new authority, registry, scheduler, generic graph, plugin framework, agent framework or subsystem without a current requirement.
- Broad implementation remains blocked until Round-2 architecture closes and the normal implementation-planning gate begins.
- This roadmap is living. Change the decomposition when evidence changes the dependency graph.
- Dormant work does not reserve stage numbers. If a trigger becomes true, insert the smallest required bounded stage where dependencies require it.

---

# 5. Stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | rebuild Round-2 problem horizon from accepted architecture + item-level research disposition | 82/82 DIAMOND/STRONG accounted; previous stage decomposition retired; new dependency graph owner-approved |
| R2.1 | **IN PROGRESS** | continuity, memory and history-aligned derived state | minimum continuity classes/lifecycles, provenance, consolidation, history alignment, repair/retirement and exact-vs-semantic promise |
| R2.2 | **PLANNED** | Actor continuity, cognition and directed relationships | bounded Actor private/durable/transient state model compatible with Step-4 epistemics and player agency |
| R2.3 | **PLANNED** | Context Runtime, retrieval and allocation | bounded deterministic context projection over admitted R2.1/R2.2 sources with complete-packet, budget, trace and degradation rules |
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

A later-stage dependency may be inspected early, but it does not become active unless the roadmap is explicitly changed.

---

# 7. R2.0 — Evidence Rebaseline & Scope Reconstruction — COMPLETE

R2.0 replaced the previous thematic problem-horizon claim with a source-backed rebaseline.

Completed results:

- current repository/process/bootstrap sources re-read;
- accepted Round-1 owners reconciled against the research horizon;
- all 82 DIAMOND/STRONG candidates individually dispositioned;
- `revisit when`/scope qualifiers preserved;
- active versus inherited versus dormant work separated;
- old Context-before-Actor ordering rejected;
- no mandatory Narrative Dynamics subsystem justified;
- no generic optional-capability gate justified;
- collaboration work narrowed to deltas not already owned by Step 5;
- new R2.1–R2.7 dependency graph owner-approved.

R2.0 creates no runtime implementation.

---

# 8. R2.1 — Continuity, Memory & History-Aligned Derived State — IN PROGRESS

Task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-memory-history-task-brief.md`

## Problem

HDM already owns current truth, fictional knowledge, disclosure, semantic/mechanical evidence, Story and selective exact history.

It does not yet have a complete architecture for **derived long-campaign continuity used by LLM reasoning**.

R2.1 must define the minimum continuity products that survive long campaigns without becoming duplicate canon or depending on mutable host conversation memory.

## Primary active research inputs

D01, D05, D06, D07, D08, D09-delta, D18, S03, S04, S19, S27.

Relevant negative/adversarial evidence remains stage-local research input.

## Required decisions

- admitted continuity classes;
- authoritative versus derived/rebuildable/disposable classification;
- source provenance/coverage;
- stability/consolidation boundary;
- history/ancestry alignment after Retry/Edit/branch/correction;
- stale/conflict/repair/rebuild/retirement behavior;
- semantic versus exact recall promises;
- Story/Chronicler relationship;
- bounded evidence-bound derived mutation where generative transformation is used.

## Constraints

Do not reopen Step-4 truth/knowledge/disclosure ownership or Step-5 selective exact history.

Do not design Actor cognition details, context ranking/budgets or LLM orchestration here.

## Exit

Canonical continuity architecture plus explicit downstream contracts for R2.2/R2.3 and closed adversarial review.

---

# 9. R2.2 — Actor Continuity, Cognition & Directed Relationships

Depends on: **R2.1**.

## Why before Context Runtime

R2.2 defines the Actor-owned/private source semantics that R2.3 will later select.

The projection layer must not invent upstream state semantics for retrieval convenience.

## Primary active research inputs

D10, D11-delta, D12-delta, D13, S07, S10, S11; specialized use of D09/S27 where Actor mutation requires it.

## Required decisions

- stable foundation versus durable evolving continuity versus transient state;
- exact boundary of `world.knowledge` versus other Actor-private cognition;
- goals/intentions/promises/private plans;
- directional `A -> B` relationship semantics;
- minimum useful relation dimensions;
- evidence-bound persistent updates;
- `NO_CHANGE`;
- sparse/event-driven cognition;
- expiry/refresh using appropriate fictional-time semantics;
- active/relevant Actor depth without over-modeling;
- PC agency exclusions.

## Inherited constraints

`world.knowledge` remains the durable proposition-stance owner. Objective truth remains separate. Player voluntary belief/emotion/interpretation is not silently committed.

## Exit

Bounded Actor continuity architecture with one owner per semantic concern and explicit R2.3 context-source contract.

---

# 10. R2.3 — Context Runtime, Retrieval & Allocation

Depends on: **R2.1, R2.2**.

## Problem

Step 4 already defines Context Assembler eligibility/projection semantics. R2.3 must design a real bounded long-campaign execution projection over finite ChatGPT context.

## Primary active research inputs

D02, D03, D04, D14, D19, D24-delta, S02, S22, S25, S29, S36, S40, S48, S49, plus D18 retrieval realization and R2.1 dedup requirements.

## Required decisions

- context candidate/source metadata;
- eligibility and recipient/subject scope;
- `required | protected | downgradable | omittable`;
- minimum complete decision packets;
- representation downgrade before defer;
- broad/episodic/entity/exact retrieval;
- typed selectors/dependency activation;
- dedup across continuity channels;
- token/model-limit accounting;
- party-size degradation;
- starvation/fairness;
- dry-run;
- inclusion/exclusion/representation trace;
- failure/defer semantics when correctness-critical context is incomplete.

## Constraints

Context Runtime is a deterministic projection capability, not canon, ACL authority, generic knowledge graph, universal query language or campaign-wide scan permission.

## Exit

Canonical bounded Context Runtime contract consumable by R2.4 and R2.5.

---

# 11. R2.4 — Single-Context LLM Execution & Instruction Architecture

Depends on: **R2.1–R2.3**.

## Problem

The canonical single-context law exists; the concrete turn/instruction machinery does not.

## Primary active research inputs

D16-delta, S21, S28, role-context Protocols 1–3, current Step-4 amendment, current host-feasibility evidence, useful non-superseded former Step-6 questions, reusable-instruction working note.

## Required decisions

- one-turn envelope;
- role activation/sequencing;
- role rebinding;
- Interpreter/Dramaturg/Actor(s)/Narrator handoffs;
- Chronicler/Commentator placement where relevant;
- minimal typed nondeterministic results;
- retry/freeze lifecycle for those results;
- deterministic tool/validation/commit gateway;
- mechanics interleaving;
- Narrator/emission boundary;
- stable constitution versus Project Instructions versus shipped procedure modules versus role frame;
- admit/partial/reject reusable first-party procedure modules;
- instruction versioning/regression;
- untrusted text as data;
- injection/role-confusion defenses;
- no hidden chain-of-thought persistence requirement.

`D16` does not imply separate subagents/background calls. Invisible auxiliary work may be a logical phase inside the same supported turn when that is sufficient.

## Exit

Canonical one-request/one-assistant-turn LLM execution architecture for the current ChatGPT-Plus baseline.

---

# 12. R2.5 — Collaboration & Multiplayer Interaction Semantics

Depends on: **R2.1–R2.4** and inherited Step-5 multiplayer/live/chronology architecture.

## Problem

Step 5 already owns shared-state currentness, CAS, chronology and split-scene foundations. R2.5 designs the missing collaboration/input/context layer.

## Primary active research inputs

D21, D22-delta, D23, S43, S44, S45, S54; D20/D24 and authenticated binding rules as inherited constraints.

## Required decisions

- synchronous versus asynchronous interaction;
- free-form versus strict-sequence coordination policy;
- multi-participant input collection/batching;
- OOC/social versus diegetic speech versus actionable intent;
- expected-contribution/readiness semantics only where actually needed;
- absence without implicit PC takeover;
- catch-up projection;
- join/rejoin conversational/action frontier;
- split-party context integration over existing independent scene/chronology frontiers;
- recipient-scoped Context Runtime outputs;
- shared-established outcome versus local retry/correction behavior.

## Non-goal

Do not redesign live CAS, campaign routing, chronology ownership or participant authentication already owned by accepted runtime architecture unless a concrete insufficiency is proven.

## Exit

Narrow collaboration architecture that composes with Step 5 rather than replacing it.

---

# 13. R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation

Depends on: **R2.1–R2.5 concrete architecture**.

## Problem

Only after HDM knows what the runtime requires can it test the actual ChatGPT-Plus operating envelope.

## Primary active research input

S53-delta plus concrete obligations from R2.1–R2.5.

D15 remains dormant unless retry evaluation demonstrates the specific repetitive-sibling failure and justifies a PoC.

## Required assurance areas

- long-chat/context behavior;
- role-containment regression;
- cross-Actor/private-state contamination;
- instruction conflict/drift;
- prompt injection/untrusted data;
- player-visible host surfaces;
- Retry/Edit/branch behavior;
- latency/tail latency;
- tool/connector failure;
- context-incomplete/defer behavior;
- recovery after context loss;
- model/reasoning-profile change;
- gameplay quality and over-completion;
- diagnostics without secret exposure.

Classify required behavior as:

```text
SUPPORTED
SUPPORTED WITH DOCUMENTED LIMITATION
DEGRADED MODE
UNSUPPORTED
```

Protocol 1–3 findings become regression evidence, not permission to reopen mandatory physical isolation.

## Exit

Measured/tested supported ChatGPT-Plus envelope and explicit assurance obligations.

---

# 14. R2.7 — Machine Realization Mapping & Holistic Architecture Closure

Depends on: **R2.1–R2.6**.

This remains architecture closure, not broad implementation.

## Required mapping

Map accepted Round-1 + Round-2 architecture to:

- GAME runtime ownership/documents;
- DEV catalogs;
- schemas;
- seeds/templates;
- migrations;
- Project Instructions;
- shipped instruction/procedure assets;
- tests/evaluations;
- tooling/diagnostics;
- persistence obligations.

## Required closure review

- cross-round authority/duplicate-owner sweep;
- Retry/recovery/concurrency composition;
- history/continuity/context consistency;
- Actor/context/role containment composition;
- multiplayer recipient/secrecy composition;
- dormant-trigger preservation;
- full 82-candidate disposition recheck;
- stale derivative/status/navigation document repair;
- implementation/deferred/dormant/debt classification.

## Exit

Architecture is ready for Superpowers implementation planning only when:

- no unresolved architecture blocker remains;
- machine-realization obligations are explicit;
- adversarial review passes;
- implementation boundaries and tests are mapped;
- broad implementation has not already leaked into the architecture phase.

---

# 15. Explicitly removed mandatory stages

Round 2 has **no mandatory standalone Narrative Dynamics stage**.

Existing preparation/process/NPC/narration architecture remains in force. Retained planning, staged world pressure, additional timeskip or anti-stagnation machinery is introduced only if a preserved dormant trigger becomes a real requirement and existing owners prove insufficient.

Round 2 has **no generic optional-capability gate**.

Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers, cache-specific optimization and similar conditional ideas remain dormant until their own triggers occur.

---

# 16. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  IN PROGRESS
R2.2  PLANNED
R2.3  PLANNED
R2.4  PLANNED
R2.5  PLANNED
R2.6  PLANNED
R2.7  PLANNED

R2.1 task brief established.
Next activity: R2.1 source extraction and evidence ledger.
Broad implementation: BLOCKED.
```
