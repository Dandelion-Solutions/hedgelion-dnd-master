# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE WORKING PLAN**

Date: 2026-08-23

This file is the sequencing/status authority for the active HDM architecture program.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Round-1 closure/rebaseline decision:

- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`

Single-context role-containment amendment:

- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`

---

# 1. Program transition

Round 1 established the mechanical/runtime architecture strong base through Steps 1-5.

The former Step 6 is no longer an active stage. It is:

> **CLOSED AS A SEPARATE STAGE / NOT EXECUTED AS ORIGINALLY DECOMPOSED / USEFUL SCOPE REALLOCATED TO ROUND 2**

This does not claim that the old Step-6 exit criteria were completed. The original decomposition was retired because completed validation and the later Step-4 amendment invalidated its mandatory physical-role-isolation premise.

Round-1 status:

| Stage | Final status | Round-2 meaning |
|---|---|---|
| 1 | **COMPLETE / ASSURED** | inherited strong base |
| 2 | **COMPLETE / ASSURED** | inherited strong base |
| 3 | **COMPLETE / ASSURED** | inherited strong base |
| 4 | **COMPLETE / ARCHITECTURE CLOSED + LATER AMENDMENT** | inherited; single-context role containment is current law |
| 5 | **COMPLETE / ARCHITECTURE CLOSED** | inherited strong base |
| 6 | **CLOSED AS SEPARATE STAGE / REALLOCATED** | useful unresolved work redistributed across Round 2 |

Detailed Round-1 semantic lookup remains in:

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
- the owning canonical specifications and owner decisions.

Where that derivative index still describes Step 6 as next, this current roadmap and the Round-1 closure decision supersede that sequencing/status text.

---

# 2. Round-2 baseline

## 2.1 Current product/deployment baseline

Round 2 designs for:

```text
primary AI host              ChatGPT
plan                         ChatGPT Plus
player-facing surface        ordinary public chat
physical LLM topology        one LLM / one physical chat context
ordinary gameplay execution  one user request / one assistant turn
private HDM hosting          out of current scope
direct model API calls       out of current scope
future Claude migration      possible future compatibility concern, not current driver
```

For multiplayer, each human player may use a separate player-facing chat/account as already assumed by the existing architecture. Round 2 must not invent a shared multi-user AI-chat dependency.

## 2.2 Role-containment baseline

HDM SHALL make one LLM sequentially execute multiple logical roles inside one physical chat context while preserving different knowledge and authority boundaries.

Physical availability of information does not make it logically eligible for the active role.

The system prompt, Project Instructions and shipped Markdown reasoning/procedure instructions are part of role-containment machinery, including:

- role rebinding;
- truth / cognition / observation / disclosure separation;
- no transitive knowledge inheritance;
- Actor-specific epistemics;
- Dramaturg latent state;
- Narrator disclosure discipline;
- creativity -> commit boundary.

Round 2 designs the runtime/instruction machinery implied by this law. It does not reopen mandatory physical isolation.

---

# 3. Round-2 evidence base

Round 2 uses all relevant current evidence without treating research as architecture automatically:

- accepted Steps 1-5 architecture;
- the single-context Step-4 canonical amendment;
- role-context validation Protocols 1-3;
- `DEV/docs/superpowers/research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md`;
- current relevant host/platform feasibility research interpreted under the new baseline;
- useful unresolved former Step-6 spikes/working notes;
- actual current GAME/DEV runtime, schemas, catalogs, tests and documentation as each stage requires.

External/research ideas must still survive HDM-specific analysis, simplification and approval before becoming architecture.

---

# 4. Operating rules

- Exactly one Round-2 architecture stage may be `IN PROGRESS` at a time.
- A later stage may be inspected to expose dependencies or contradictions but must not silently replace the active stage.
- Each stage follows the normal task-brief -> research -> alternatives/recommendation -> decision -> specification -> adversarial review -> closure process at a depth proportional to risk.
- Round-1 architecture is not automatically re-reviewed.
- A closed Round-1 topic enters Round 2 only if new work materially extends it, contradicts it, introduces a new consumer it cannot satisfy, or makes it insufficient.
- Independent confirmation of an accepted Round-1 principle is evidence, not a new roadmap stage.
- Research candidates that solve no concrete current HDM problem remain deferred even if attractive.
- YAGNI applies aggressively: do not create a new authority, subsystem, registry, scheduler, agent framework, plugin framework or generic graph unless a real current requirement needs it.
- Broad implementation remains deferred until the relevant Round-2 architecture closes and the normal implementation-planning gate is reached.
- The roadmap is living. If a stage proves wrongly grouped or wrongly ordered, change the roadmap rather than preserving the first decomposition by inertia.

---

# 5. Round-2 stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / REBASELINED** | close former Step 6; establish single-context/ChatGPT-Plus baseline; derive problem horizon | old Step-6 sequencing retired; Round-2 dependency structure established |
| R2.1 | **NEXT / NOT STARTED** | continuity, memory and history-aligned derived-state model | explicit continuity layers/lifecycles, consolidation and history-alignment contracts without duplicate authority |
| R2.2 | **PLANNED** | Context Runtime: retrieval, allocation, complete decision packets, trace/observability | bounded explainable role-context construction policy over R2.1 sources |
| R2.3 | **PLANNED** | Actor continuity, cognition, directional relationships and private state | bounded persistent/transient Actor model compatible with Step-4 knowledge and player agency |
| R2.4 | **PLANNED** | single-context LLM turn architecture and shipped instruction machinery | enforceable logical role pipeline, rebinding, activation, handoffs, tool/authority boundaries and instruction composition |
| R2.5 | **PLANNED** | Dramaturg/narrative dynamics, latent planning, world pressure, long-range narrative continuity and Chronicler integration | useful adaptive narrative development without plot authority or maintenance-turn pollution |
| R2.6 | **PLANNED** | multiplayer collaboration and scene topology | sync/async collaboration, split-party, participant/controller/channel semantics and recipient-scoped projections over existing Step-5 authority |
| R2.7 | **PLANNED** | ChatGPT-Plus runtime reliability, evaluation, failure/degradation and security/quality validation | tested supported host envelope and integrated nondeterministic-layer assurance criteria |
| R2.8 | **PLANNED** | secondary modes and optional-capability gate | explicit admit/defer/reject decisions for Commentator refinements, extensibility, multimodal and future-provider portability surfaces |
| R2.9 | **PLANNED** | machine-realization mapping and holistic architecture closure | catalog/schema/seed/runtime-doc obligations mapped; cross-round adversarial review passed; implementation obligations consolidated |

---

# 6. R2.0 — Rebaseline and problem horizon — COMPLETE

Completed by the owner decision and this roadmap.

Results:

- former Step 6 closed as a separate stage;
- mandatory physical role isolation removed from the active problem set;
- ChatGPT Plus ordinary chat fixed as current baseline;
- private hosting/direct API removed from current scope;
- Round-1 closed architecture retained as strong base;
- new work grouped by unresolved dependency rather than old numbering;
- external idea dossier, experiments and former Step-6 evidence retained as inputs rather than automatic requirements.

---

# 7. R2.1 — Continuity, Memory and History-Aligned Derived State

## Problem

Round 1 defines canonical current state, knowledge, disclosure, history evidence, Story and selective exact retention, but it does not yet define a complete long-campaign continuity architecture for LLM reasoning.

Round 2 must distinguish durable truth from derived continuity products and decide how long-lived semantic memory survives Retry/Edit/branch/history changes without becoming hidden authority.

## Primary questions

- Which continuity classes actually exist: authoritative state, recent exact evidence, broad summary, episodic recall, entity-local continuity, private Actor continuity, transient scene state, deep archive?
- Which are authoritative, derived, rebuildable, cached, exact-protected or disposable?
- What is the minimum viable layer set rather than the maximum imaginable one?
- When may recent evidence be consolidated into longer-lived derived representations?
- How are summaries/memories associated with source revisions/history ancestry?
- What happens to derived continuity after Retry/Edit/branch divergence?
- What exact-recall promise already follows from Step 5.11 and what additional retrieval promise, if any, is needed?
- How are stale, conflicting, duplicate or superseded derived continuity records repaired or retired?

## Round-1 constraints preserved

Do not reopen:

- current canonical ownership;
- Step-4 truth/knowledge/disclosure separation;
- Step-5 selective exact retention semantics;
- the rule that Story/summary/memory does not become canon by persistence or usefulness.

## Candidate research inputs

Strongly relevant Dossier areas include D01, D05-D08, D18 and related STRONG/negative-intelligence items. Their recommendations remain candidates, not stage outcomes.

## Exit result

A canonical continuity model that defines:

- admitted continuity layers and their owners/lifecycles;
- provenance/source-coverage rules;
- consolidation/stability boundaries;
- history/branch alignment obligations for derived state;
- rebuild/repair/retirement semantics;
- exact versus semantic recall promises;
- explicit rejection of duplicate authority.

---

# 8. R2.2 — Context Runtime, Retrieval, Allocation and Observability

Depends on: **R2.1**.

## Problem

Step 4 established deterministic Context Assembler ownership and role eligibility. Round 2 must design how a real long campaign produces one bounded role-local execution projection under finite context pressure.

## Primary questions

- What is a context candidate and what metadata/provenance accompanies it?
- Which semantic classes receive hard minimum reservations versus optional budget?
- Which inputs are `required`, `protected`, `downgradable` or `omittable`?
- Which decision packets must remain complete rather than be partially truncated?
- What representation downgrade chain is permitted before omission/defer?
- How are relevance, entity/scope selectors, chronology, witnessed knowledge and long-range retrieval combined without building a second rules engine?
- How is starvation prevented deterministically?
- How are duplicate semantic facts removed across multiple derived channels?
- How can context assembly run in dry-run/test mode?
- What trace explains inclusion, exclusion, ranking, downgrade, budget use and final placement without becoming player-visible secret leakage?

## Round-1 constraints preserved

Context Assembler remains a deterministic projection capability, not canonical authority, generic ACL, universal query language or campaign-wide scan license.

## Candidate research inputs

D02-D04, D14, D19 and relevant STRONG items such as critical pins, typed dependency activation, tokenizer accounting, dry-run assembly, starvation/fairness and party-size degradation.

## Exit result

A canonical bounded Context Runtime contract covering:

- candidate acquisition and typed selection;
- semantic budget allocation;
- complete decision-packet rules;
- downgrade/defer behavior;
- retrieval/dependency limits;
- deterministic dedup/fairness rules where justified;
- inspectable context trace and dry-run behavior;
- failure semantics when correctness-critical context cannot be assembled completely.

---

# 9. R2.3 — Actor Continuity, Cognition and Relationships

Depends on: **R2.1, R2.2**.

## Problem

Step 4 defines fictional epistemic relations and Actor role eligibility, but living NPC continuity requires more than a `world.knowledge` row: stable identity, evolving goals, directional relationships, private plans, transient states and evidence-driven updates need explicit boundaries.

## Primary questions

- Which Actor state belongs to stable foundation, durable evolving continuity and transient private state?
- Which state is canonical world fact versus subject-local fictional cognition?
- How are goals, intentions, promises, relationships and suspicions represented without universal social/epistemic over-modeling?
- Are relationships directional `A -> B`, and which material dimensions deserve typed persistence?
- When does Actor cognition run, and how is sparse/event-driven activation preferred over simulating every NPC every turn?
- What counts as sufficient evidence for a durable cognition mutation?
- How does `NO_CHANGE` work as a legitimate assessment result?
- How are transient states refreshed/expired without using arbitrary turn-count TTL where fictional time matters?
- Which NPCs receive deep continuity and how are inactive/background actors compacted safely?
- How is PC/player agency protected from Actor-style automatic cognition mutation?

## Round-1 constraints preserved

- `world.knowledge` remains the durable current fictional epistemic owner for proposition stance;
- objective truth remains separate;
- PC voluntary belief/emotion/interpretation is not silently chosen by the engine;
- LLM-produced cognition changes remain proposals until accepted by the proper owner path.

## Exit result

A bounded Actor-continuity architecture with explicit state classes, authority, lifecycle, evidence/provenance, directional relation semantics, sparse activation and persistence boundaries.

---

# 10. R2.4 — Single-Context LLM Turn and Instruction Machinery

Depends on: **R2.2, R2.3**.

## Problem

The single-context Step-4 amendment is now canonical, but its execution machinery is not designed. Round 2 must define how one LLM in one ChatGPT chat/user request reliably traverses several logical role phases without collapsing their knowledge or authority contracts.

## Primary questions

- What is the stable global runtime constitution?
- What belongs in Project Instructions versus shipped MD runtime/procedure modules versus turn-built role frames?
- What is the canonical conceptual turn envelope?
- How is role rebinding made explicit before Interpreter, Dramaturg, each Actor and Narrator phase?
- Which roles are always, conditionally or rarely activated?
- How do multiple Actor phases observe earlier public actions/speech without inheriting private cognition?
- What are the minimal cross-role handoffs?
- What should remain prose and what requires minimal structured result/receipt?
- How does deterministic Python/runtime/tooling remain the only acceptance/commit gateway?
- How are deterministic mechanics interleaved with role phases when a turn requires them?
- How are invalid role outputs, retries and already-accepted mechanics handled without replay?
- How are system prompt, Project Instructions and shipped MD versioned/tested as correctness-relevant runtime assets?
- Should reusable first-party procedure modules be adopted, partially adopted or rejected?
- How is untrusted player/world/tool text kept data rather than instruction?
- How is hidden chain-of-thought kept out of runtime protocols and persistence requirements?

## Explicit non-goal

Do not design separate agents/chats/model calls merely to recreate the superseded physical-isolation architecture.

## Exit result

A canonical one-request/one-assistant-turn LLM runtime architecture defining:

- role phase order and conditional activation;
- role rebinding semantics;
- turn-envelope and role-frame structure;
- instruction ownership/composition;
- allowed logical handoffs;
- deterministic authority/tool gateway;
- nondeterministic-result lifecycle where needed;
- failure/retry/degradation behavior;
- instruction versioning and regression obligations.

---

# 11. R2.5 — Dramaturg, Narrative Dynamics and Long-Range Narrative Continuity

Depends on: **R2.1-R2.4**.

## Problem

Step 4 admits noncanonical Dramaturg preparation and Step 5 admits optional/lagging Chronicler Story projection. Round 2 must decide what adaptive narrative/world-development machinery is actually useful without turning preparation into plot authority or auxiliary maintenance into gameplay turns.

## Primary questions

- What private/provisional Dramaturg state is worth retaining across turns?
- How are pressures, unresolved situations, likely reactions and latent branches represented without predetermining outcomes?
- Which narrative developments are pure suggestions, which are fictional cognition and which require canonical event/commit paths?
- Should world pressures have staged progression, and if so how is railroading prevented?
- How should timeskip/domain advancement interact with existing temporal owners?
- What pacing/anti-stagnation signals are advisory only?
- How do global narrative continuity and episodic/entity retrieval feed Dramaturg without becoming a giant summary blob?
- Where does Chronicler run logically, how much lag is acceptable, and which continuity products may it help produce without gaining canon authority?
- How are auxiliary semantic maintenance operations kept invisible from the player-facing turn history?

## Exit result

A bounded adaptive narrative architecture that preserves player agency, causality and commit boundaries while supplying useful long-term Dramaturg/Story continuity.

---

# 12. R2.6 — Multiplayer Collaboration and Scene Topology

Depends on: **R2.1-R2.5** plus inherited Step-5 authority/concurrency architecture.

## Problem

Round 1 closed shared-state durability/concurrency, but multiplayer collaboration semantics remain broader than storage: asynchronous participation, split party, rejoin/catch-up, input coordination and controller ownership need explicit product/runtime contracts.

## Primary questions

- What collaboration state is actually needed beyond canonical world/live state?
- How do synchronous and asynchronous play share one architecture without universal round-robin?
- What are the baseline coordination modes for free-form shared scene versus strict actor sequence?
- When are multiple participant inputs collected before one resolution?
- How are OOC/social coordination, diegetic speech and actionable intent distinguished?
- How does participant identity bind to controlled PC(s), and how is delegation/controller transfer explicit and reversible?
- How is absence handled without silently giving the AI control of a PC?
- What does join/rejoin mean at an active scene/frontier?
- What bounded catch-up projection does a returning participant receive?
- How does split-party create independent scene/context/chronology frontiers while preserving one shared canon?
- What material causal bridges force reconciliation between scenes?
- Which shared outcomes are observationally final under existing Step-5 publication/delivery semantics and where, if anywhere, does Round 2 need an extension rather than a restatement?
- How do recipient-specific Context Runtime projections avoid secret leakage across players/scenes?

## Round-1 constraints preserved

Do not replace Step-5 live/currentness/concurrency ownership with a new generic collaboration authority or let network/message order define fictional chronology.

## Exit result

A narrow collaboration/scene architecture supporting synchronous and asynchronous play, split-party and explicit participant/controller/channel semantics over the existing Step-5 shared-state model.

---

# 13. R2.7 — ChatGPT-Plus Reliability, Evaluation, Security and Quality

Depends on the concrete contracts produced by **R2.1-R2.6**.

## Problem

Round 2 must prove that the designed nondeterministic layer is usable and testable on the current ChatGPT-Plus ordinary-chat baseline rather than treating prompt success as self-evident.

## Primary questions

- What ChatGPT-Plus capabilities/limitations materially affect the accepted architecture?
- How does long-chat growth/provider-managed history behavior interact with campaign-owned continuity/context rebuilding?
- What latency envelope is acceptable for ordinary versus exceptional turns?
- Which work may degrade/defer when latency/context pressure rises, and which correctness inputs may not?
- What host Retry/Edit/branch behaviors can HDM safely support under existing Step-5 semantics?
- Which player-visible host surfaces materially matter under the ordinary-chat baseline?
- What residual Narrator emission/disclosure limitation must be documented if the host cannot provide pre-visible candidate staging?
- How are prompt injection, role confusion, cross-Actor contamination and unauthorized tool/state mutation attacked in tests?
- What evaluation dimensions are independent: correctness, role containment, gameplay quality, latency, robustness?
- How are model/reasoning-profile drift and instruction-package changes regression-tested?
- Which diagnostics are retained without creating a new secret archive or player-visible leak surface?

## Evidence rule

Use current official platform evidence and direct probes only where the architecture actually depends on a host property. Do not turn provider feature reconnaissance into the roadmap itself.

## Exit result

One explicit supported ChatGPT-Plus capability envelope with:

- known limitations/degradation behavior;
- role-containment and prompt-injection regression suite requirements;
- context/continuity evaluation obligations;
- gameplay-quality evaluation axes;
- latency/robustness targets;
- residual-risk statements where the host cannot provide a stronger guarantee.

---

# 14. R2.8 — Secondary Modes and Optional-Capability Gate

Depends on the core architecture above.

Purpose: prevent optional ideas from contaminating the baseline while still making explicit V1 decisions.

Evaluate and either **ADMIT / DEFER / REJECT** at least:

- Commentator serving/perspective/spoiler refinements not already fixed by Steps 4-5;
- multimodal/voice/attachments beyond normalized text/evidence intake;
- extension/plugin/script capability model;
- reusable runtime-procedure module registry beyond the minimum needed by R2.4;
- future provider portability boundary and possible later Claude migration;
- explicit solo/shared fork product semantics where not already required;
- optional advanced memory/cognition features that failed the earlier YAGNI gate.

This stage is not permission to build these systems. Its exit may legitimately be mostly `DEFER` decisions.

## Exit result

A bounded V1 capability envelope and explicit deferred list with no speculative subsystem left masquerading as a baseline dependency.

---

# 15. R2.9 — Machine-Realization Mapping and Holistic Architecture Closure

Depends on: all admitted Round-2 architecture stages.

## Scope

- map accepted Round-1 + Round-2 architecture to GAME runtime ownership;
- identify catalog/schema/seed/template/migration obligations;
- identify shipped prompt/Project Instruction/MD asset obligations;
- identify tests/evals/tooling required for realization;
- reconcile stale derivative/status/navigation documents;
- confirm no duplicate authority or hidden persistence owner was introduced;
- confirm context/memory/Actor/multiplayer designs compose with Step-3/5 retry, durability, recovery and concurrency semantics;
- run full cross-round adversarial review;
- classify remaining work as implementation obligation, explicit deferred capability, accepted debt or future architecture;
- prepare the handoff to implementation planning only after architecture closure.

## Exit result

```text
Round-2 architecture closed
+
accepted canonical specification chain complete
+
machine/runtime realization obligations traceable
+
full integrated review passes
+
implementation planning may begin
```

No implementation is authorized merely by reaching this roadmap stage; the normal Superpowers design/specification/planning gates still apply.

---

# 16. Dependency spine

The intended dependency direction is:

```text
ROUND-1 STRONG BASE
        |
        v
R2.1 Continuity / Memory / History-Aligned Derived State
        |
        v
R2.2 Context Runtime / Retrieval / Budgets / Trace
        |
        v
R2.3 Actor Continuity / Cognition / Relationships
        |
        v
R2.4 Single-Context LLM Turn / Instruction Machinery
        |
        +----------------------+
        |                      |
        v                      v
R2.5 Narrative Dynamics   R2.6 Multiplayer Collaboration
        |                      |
        +-----------+----------+
                    v
R2.7 ChatGPT-Plus Reliability / Eval / Security / Quality
                    |
                    v
R2.8 Secondary/Optional Capability Gate
                    |
                    v
R2.9 Machine Mapping / Holistic Closure
```

Parallel research is allowed when it does not create premature decisions, but canonical stage closure follows the dependency order above.

---

# 17. Explicitly not separate Round-2 stages

Unless a later stage exposes a real contradiction/extension need, the following remain inherited rather than being re-planned:

- deterministic mechanics and RNG ownership;
- IntentPlan/Resolution/Procedure execution boundary;
- objective truth ownership;
- basic `world.knowledge` proposition stance semantics;
- human disclosure ownership;
- Story non-authority;
- base promotion/commit boundary;
- durability classes and publication/recovery semantics;
- existing live currentness/concurrency ownership;
- canonical chronology principles;
- selective exact transcript/history retention;
- cleanup authority/safety principles;
- mandatory physical LLM role isolation (superseded, not pending).

If Round 2 later requires changing one of these, the active stage must explicitly identify the dependency and open a superseding decision rather than silently rewriting it.

---

# 18. Exact continuation point

**Round 1: CLOSED / strong base retained.**

**Former Step 6: CLOSED AS SEPARATE STAGE / useful scope reallocated to Round 2.**

**Round 2: ACTIVE.**

Next architecture stage:

> **R2.1 — Continuity, Memory and History-Aligned Derived State — NEXT / NOT STARTED**

The next substantive action is to create the R2.1 Architecture Task Brief and begin the normal architecture/deep-work cycle. Broad implementation remains blocked.
