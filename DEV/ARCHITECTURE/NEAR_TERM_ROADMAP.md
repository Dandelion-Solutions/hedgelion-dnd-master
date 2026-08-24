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

This roadmap is the owner-approved Round-2 decomposition and supersedes the earlier R2.1–R2.9 thematic stage plan.

---

# 1. Program baseline

Round 1 remains the accepted architecture base.

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
future provider migration    compatibility concern only
```

Single-context role law:

> Physical availability of information does not make it logically eligible for the active HDM role.

System prompt, Project Instructions and shipped HDM reasoning/procedure instructions participate in role-containment machinery but do not become canonical-state authority.

---

# 2. Round-1 preservation rule

A closed Round-1 topic becomes active Round-2 work only when current work:

1. materially extends the accepted contract;
2. exposes a contradiction or invalid assumption;
3. introduces a new consumer the accepted contract cannot satisfy; or
4. makes the accepted decision insufficient for a current requirement.

Independent confirmation or thematic overlap is evidence, not a new stage.

---

# 3. Evidence / activation rule

Item-level accounting of all 24 DIAMOND and 58 STRONG candidates remains:

```text
ACTIVE / ACTIVE DELTA          43
INHERITED / ALREADY SATISFIED  16
CONDITIONAL / DORMANT          23
unaccounted                     0
```

Research classification is not backlog state. Dormant items create no current task until their preserved trigger fires. RESERVE / NEGATIVE evidence remains stage-local adversarial input.

---

# 4. Operating rules

- Exactly one numbered Round-2 stage may be `IN PROGRESS`.
- Later stages may be inspected only for dependency/contradiction visibility relevant to the active stage.
- Each stage follows task brief -> Source Manifest/evidence extraction -> alternatives/recommendation -> owner decision where required -> candidate specification -> adversarial review -> closure.
- Before Decision Brief, candidate specification, coverage claim or closure, Source Manifest/evidence/synthesis-completeness gates must pass.
- Owning sources beat roadmaps, indexes, summaries and remembered state.
- YAGNI applies aggressively: no new authority, registry, scheduler, generic graph, plugin/agent framework or subsystem without a current requirement.
- Broad implementation remains blocked until Round-2 architecture closes and implementation planning is explicitly entered.
- Dormant work reserves no stage number. If a trigger becomes true, insert the smallest bounded stage where dependencies require it.

---

# 5. Stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | evidence rebaseline/scope reconstruction | 82/82 DIAMOND/STRONG accounted; dependency graph owner-approved |
| R2.1 | **COMPLETE / ARCHITECTURE CLOSED** | continuity, memory and history-aligned derived state | reuse-first continuity; Story nonauthoritative orientation; history/exact/repair contracts |
| R2.2 | **COMPLETE / ARCHITECTURE CLOSED** | Actor continuity, cognition and directed relationships | source-Actor-owned sparse continuity; directed relationships; lazy-discovery handoff |
| R2.3 | **COMPLETE / ARCHITECTURE CLOSED** | Context Runtime, retrieval, lazy discovery and allocation | bounded multi-channel discovery; typed packet closure; packet-first allocation; storage/index boundaries |
| R2.4 | **COMPLETE / ARCHITECTURE CLOSED** | single-context LLM execution and instruction architecture | registered TurnEnvelope; minimal typed gateways; deterministic authority; first-safe-opportunity Chronicler service |
| R2.5 | **IN PROGRESS** | collaboration and multiplayer interaction semantics | sync/async input, mode coordination, rejoin/catch-up and recipient-scoped context over inherited Step-5 shared-state architecture |
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
- Story remains durable/noncanonical/optional and may serve eligible gameplay roles as broad/episodic orientation;
- material current/source-specific decisions escalate to proper source owners;
- source-bound does not imply current;
- projection absence does not imply semantic absence;
- history alignment uses HDM source/currentness/correction/projection-generation semantics rather than host Retry/Edit ancestry;
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

- source Actor owns current non-epistemic private continuity;
- `world.knowledge` remains proposition-stance authority;
- foundation / durable evolving cognition / transient private state are semantic lifetimes, not three stores;
- sparse directed relationships belong to source Actor;
- Actor cognition is sparse/event-driven with valid `NO_CHANGE`;
- persisted transient state uses fictional invalidation rather than generic turn TTL;
- player voluntary mental state remains player-owned;
- Story/history may inform but not establish current cognition;
- full entity state is not required merely to discover relevance.

---

# 10. R2.3 — Context Runtime, Retrieval, Lazy Discovery & Allocation — COMPLETE

Artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-3-context-runtime-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-decision-brief.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-resolution-gate.md`

Canonical result:

- Context Runtime realizes Step-4 Context Assembler and stores no new truth;
- scene/location is cheapest primary discovery seed, not a closed-world oracle;
- bounded multi-channel discovery precedes full semantic load;
- required context is a bounded typed dependency closure;
- routed currentness/eligibility precede role-local use;
- packet-first allocation preserves required representation floors before optional material;
- long-range retrieval expands progressively/dependency-specifically;
- `ASSEMBLED`, `ASSEMBLED_DEGRADED`, `UNSATISFIABLE` are explicit outcomes;
- high-cardinality file-per-record families require deterministic routing-only sharding;
- current `*_INDEX.yaml` files intentionally remain monolithic until a measured scale trigger fires;
- SQLite/HOT may host current SOFT owner state and acceleration structures but storage format creates no semantic authority;
- R2.7 owns exact physical roots/shard/index/SQLite mapping.

---

# 11. R2.4 — Single-Context LLM Execution & Instruction Architecture — COMPLETE

Artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-4-single-context-llm-execution-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-chronicler-service-owner-clarification.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-4-chronicler-service-evidence-addendum.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-decision-brief-v2.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-resolution-gate.md`

Canonical result:

- one user request / one assistant turn / one physical context remains baseline;
- registered `TurnEnvelope` owns legal logical phase/control boundaries but no semantic authority;
- Interpreter/Dramaturg/Actor phases are conditional and each phase rebinds role/subject/purpose/context/authority/output contract;
- minimal typed handoffs cross phase boundaries; raw private role context and hidden chain-of-thought do not;
- deterministic owners remain the only acceptance path for mechanics/state/Story coverage/disclosure;
- accepted mechanics/RNG never replay merely because a later LLM/Story/Narrator phase fails;
- full CORE remains physically present while activation is semantic and phase-scoped;
- data/instruction and role-switch boundaries are explicit;
- Narrator is the only ordinary player-visible logical phase and uses Step-5.12 validation/`EMISSION_COMMIT`;
- compatible Story backlog creates a deferred Chronicler service obligation evaluated every ordinary TurnEnvelope;
- Story receives bounded service at the first safe opportunity after protecting current correctness and Narrator/output capacity;
- no Story scheduler/job queue/background worker/fixed-turn SLA or Story commit-every-turn requirement;
- no same-envelope Story feedback into gameplay roles;
- Story cannot durably outrun its admitted Step-5.10 source basis;
- Narrator is freshly rebound after Chronicler service and Story contention yields before visible-response capacity is threatened;
- R2.6 owns production-like containment/latency/injection/anti-starvation validation.

R2.4 Diamond/Strong disposition is recorded in its resolution gate.

---

# 12. R2.5 — Collaboration & Multiplayer Interaction Semantics — IN PROGRESS

Depends on: **R2.1–R2.4** plus inherited Step-5 multiplayer/live/chronology architecture.

Primary active research: D21, D22-delta, D23, S43, S44, S45, S54; D20/D24 and authenticated binding remain inherited constraints.

Scope is the collaboration/input/context delta:

- sync/async interaction semantics;
- mode coordination;
- input collection/batching;
- OOC vs diegetic vs actionable separation;
- absence without automatic PC takeover;
- join/rejoin/catch-up;
- recipient-scoped Context Runtime / TurnEnvelope composition;
- split-party independent scenes/frontiers and causal bridges only where current Step-5 owners are insufficient.

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

Protocols 1–3 remain regression evidence. R2.6 must also test Chronicler->Narrator containment and first-safe-opportunity anti-starvation under production-like load mixtures.

---

# 14. R2.7 — Machine Realization Mapping & Holistic Architecture Closure — PLANNED

Depends on: **R2.1–R2.6**.

Map accepted architecture to GAME runtime ownership/documents, DEV catalogs/schemas, seeds/templates/migrations, Project Instructions, shipped instruction assets, tests/evaluations, tooling/diagnostics and persistence obligations.

R2.7 specifically maps each durable record family to:

- physical root;
- flat vs sharded storage policy;
- deterministic shard rule where required;
- monolithic index owner/path;
- SQLite hydration/query realization;
- migrations and validation/tests.

Closure includes cross-round authority/duplicate-owner review, Retry/recovery/concurrency composition, history/continuity/context consistency, Actor/context/role-containment composition, multiplayer recipient/secrecy composition, dormant-trigger preservation, full 82-candidate disposition recheck and stale derivative/status repair.

Implementation planning begins only after architecture blockers are closed and machine-realization/test obligations are explicit.

---

# 15. Explicitly removed mandatory stages

Round 2 has no mandatory standalone Narrative Dynamics stage. Existing preparation/process/NPC/narration architecture remains in force; extra planning/world-pressure/timeskip/anti-stagnation machinery appears only if a preserved dormant trigger becomes real and existing owners prove insufficient.

Round 2 has no generic optional-capability gate. Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers, cache-specific optimization and similar ideas remain dormant until their own triggers occur.

---

# 16. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  COMPLETE / ARCHITECTURE CLOSED
R2.2  COMPLETE / ARCHITECTURE CLOSED
R2.3  COMPLETE / ARCHITECTURE CLOSED
R2.4  COMPLETE / ARCHITECTURE CLOSED
R2.5  IN PROGRESS
R2.6  PLANNED
R2.7  PLANNED

R2.5 next activity:
    construct task-specific dependency subgraph / Source Manifest
    -> extract collaboration/multiplayer delta evidence
    -> alternatives/recommendation only for material unresolved owner choices

Broad implementation: BLOCKED.
```
