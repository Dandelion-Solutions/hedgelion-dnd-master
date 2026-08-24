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

Item-level accounting of all 24 DIAMOND and 58 STRONG candidates remains the Round-2 accounting basis. R2.5 additionally fired the preserved S14 revisit trigger narrowly for multiplayer retained noncanonical Dramaturg planning continuity; this does not create a new numbered stage.

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
- Dormant work reserves no stage number. If its trigger becomes true, insert the smallest bounded stage only when dependency ordering requires one; otherwise resolve the delta inside the active owning stage.

---

# 5. Stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | evidence rebaseline/scope reconstruction | 82/82 DIAMOND/STRONG accounted; dependency graph owner-approved |
| R2.1 | **COMPLETE / ARCHITECTURE CLOSED** | continuity, memory and history-aligned derived state | reuse-first continuity; Story nonauthoritative orientation; history/exact/repair contracts |
| R2.2 | **COMPLETE / ARCHITECTURE CLOSED** | Actor continuity, cognition and directed relationships | source-Actor-owned sparse continuity; directed relationships; lazy-discovery handoff |
| R2.3 | **COMPLETE / ARCHITECTURE CLOSED** | Context Runtime, retrieval, lazy discovery and allocation | bounded multi-channel discovery; typed packet closure; packet-first allocation; storage/index boundaries |
| R2.4 | **COMPLETE / ARCHITECTURE CLOSED** | single-context LLM execution and instruction architecture | registered TurnEnvelope; minimal typed gateways; deterministic authority; first-safe-opportunity Chronicler service |
| R2.5 | **COMPLETE / ARCHITECTURE CLOSED** | collaboration and multiplayer interaction semantics | agency-safe scoped collaboration; bounded async joint input; recipient catch-up; two-level noncanonical Dramaturg coordination |
| R2.6 | **COMPLETE / ARCHITECTURE CLOSED** | ChatGPT-Plus assurance, evaluation, security and degradation | observable behavioral-containment MVP envelope; fixed Connector path; S53 capability envelope; integrated Protocol-4 validation deferred to implemented-MVP acceptance |
| R2.7 | **IN PROGRESS** | machine-realization mapping and holistic closure | GAME/DEV/schema/catalog/instruction/test obligations mapped; cross-round review passed; implementation-planning entry criteria satisfied |

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

Owning R2.1 artifacts remain under `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/research/` dated `2026-08-24-r2-1-*`.

---

# 9. R2.2 — Actor Continuity, Cognition & Directed Relationships — COMPLETE

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

Owning R2.2 artifacts remain under `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/research/` dated `2026-08-24-r2-2-*`.

---

# 10. R2.3 — Context Runtime, Retrieval, Lazy Discovery & Allocation — COMPLETE

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

Owning R2.3 artifacts remain under `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/research/` dated `2026-08-24-r2-3-*`.

---

# 11. R2.4 — Single-Context LLM Execution & Instruction Architecture — COMPLETE

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
- R2.6 closed the host-assurance contract; final integrated containment/latency/injection/anti-starvation validation is an implemented-MVP acceptance obligation.

Owning R2.4 artifacts remain under `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/research/` dated `2026-08-24-r2-4-*`.

---

# 12. R2.5 — Collaboration & Multiplayer Interaction Semantics — COMPLETE

Owning artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-task-brief.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-5-collaboration-multiplayer-evidence-ledger.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-5-agency-dramaturg-coordination-evidence-addendum.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-decision-brief-v2.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-resolution-gate.md`

Canonical result:

- multiple participant chats remain independent TurnEnvelopes over one campaign repository/canon;
- no campaign-global active-player/turn queue;
- `INDEPENDENT_IMMEDIATE`, `AGENCY_DEPENDENT_COLLECTIVE`, and `RULE_OWNED_ORDERED` are distinct coordination families;
- another player becomes required only after positive bounded material agency dependency plus applicable currentness/chronology verification;
- dependent play advances to a maximal safe semantic/visible frontier before waiting;
- absence is neither consent nor immunity from automatic consequences where no valid choice/reaction exists;
- external player coordination is allowed but does not authorize another player's PC;
- bounded collaboration obligations own collection/generation only, not gameplay consequence;
- contribution reuse is purpose/scope/generation-bound;
- join/rejoin acquires current route/mode/context/catch-up before mutation;
- catch-up is recipient-scoped projection and never a read receipt;
- player-local retained Dramaturg horizons are admitted;
- a shared Dramaturg horizon is active only in multiplayer and coordinates campaign-level noncanonical preparation across chats;
- all Dramaturg horizons distinguish source-anchored constraints from provisional direction and remain noncanonical;
- **history is not written in advance**: preparation has no entitlement to occur, canon invalidates preparation, and no plot-restoration machinery is allowed;
- shared coherence constrains preparation rather than player/Actor freedom; shared provisional direction remains revisable;
- local horizons may develop independently while staying compatible with canon/applicable shared planning basis;
- local/shared preparation is lazily discovered/loaded through R2.3 and never requires a global per-turn planning scan;
- concurrent shared-horizon updates require current-generation/exact-base fencing and semantic rebase rather than blind merge;
- Story and Dramaturg planning retain separate retrospective/prospective lifecycles;
- S14 revisit trigger fired narrowly for multiplayer retained noncanonical planning; no standalone Narrative Dynamics stage was created;
- R2.6 closed architecture-stage host assurance; actual agency/planning/current-generation/lazy-load reliability remains implemented-MVP acceptance work.

R2.5 Diamond/Strong disposition is recorded in its canonical spec/resolution gate.

---

# 13. R2.6 — ChatGPT-Plus Assurance, Evaluation, Security & Degradation — COMPLETE

Owning closure artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-6-current-host-assurance-synthesis.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-6-production-like-assurance-protocol.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-6-protocol-4-frozen-fixture-contract.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-candidate-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-adversarial-review.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-resolution-gate.md`

Canonical result:

- MVP secrecy/role-boundary guarantee is **observable behavioral containment**, not physical/cognitive isolation;
- physical presence of ineligible information is permitted; material ineligible use/disclosure is not;
- the internal suppression/ignoring mechanism is outside the HDM correctness contract;
- prior ineligibility is not permanent forgetting: lawfully eligible information must remain normally usable;
- retained Protocols 1-3 are sufficient pre-implementation feasibility evidence for architecture continuation;
- full production-like Protocol-4 execution moves to the implemented-MVP acceptance stage rather than requiring a parallel pre-implementation MVP harness;
- cheap bounded blocker checks remain allowed when a concrete host/architecture incompatibility question appears;
- Narrator baseline is pre-Narrator semantic admission + fresh recipient-scoped rebind + logical `EMISSION_COMMIT`; no byte-exact outbox is required;
- ambient Project/chat memory is physical context only, never campaign authority/currentness/knowledge/disclosure;
- context allocation does not depend on exact hidden remaining-token telemetry;
- S53 resolves to a supported capability/behavior envelope with High recommended, not exact cross-player model identity;
- D15 remains dormant;
- repository transport remains fixed to deterministic Python/core preparation + GitHub Connector; no transport reselection/fallback probes;
- experiments/prototypes/raw fixtures/instrumentation belong in HDM Lab by default;
- Protocol-4-derived scenarios remain mandatory downstream test/release-readiness obligations and are not discarded.

Resolution gate: **17/17 PASS; unresolved architecture blockers 0**.

---

# 14. R2.7 — Machine Realization Mapping & Holistic Architecture Closure — IN PROGRESS

Depends on: **R2.1–R2.6**.

Map accepted architecture to GAME runtime ownership/documents, DEV catalogs/schemas, seeds/templates/migrations, Project Instructions, shipped instruction assets, tests/evaluations, tooling/diagnostics and persistence obligations.

R2.7 specifically maps each durable record family to:

- physical root;
- flat vs sharded storage policy;
- deterministic shard rule where required;
- monolithic index owner/path;
- SQLite hydration/query realization;
- migrations and validation/tests.

R2.7 additionally maps R2.5 collaboration and Dramaturg planning identities/generations, physical roots, current-generation fencing, discovery metadata, retention and schema/runtime/instruction integration.

R2.7 also owns the R2.6 machine/instruction/test handoff:

- exact CORE/Project-Instructions placement of the behavioral eligibility rule;
- `ineligible now -> do not materially use/disclose` plus `lawfully eligible later -> may use normally`;
- Context Runtime status/result realization and conservative estimator hooks;
- Narrator/`EMISSION_COMMIT` realization;
- deployment capability prerequisites and visible auxiliary-surface test obligations;
- fixed Connector call/currentness mapping;
- Protocol-4-derived test/evaluation catalog and MVP release/readiness gates;
- Lab-vs-public experiment/result boundary.

Closure includes cross-round authority/duplicate-owner review, Retry/recovery/concurrency composition, history/continuity/context consistency, Actor/context/role-containment composition, multiplayer recipient/secrecy/planning composition, dormant-trigger preservation, full candidate-disposition recheck and stale derivative/status repair.

Implementation planning begins only after architecture blockers are closed and machine-realization/test obligations are explicit.

---

# 15. Explicitly removed mandatory stages

Round 2 has no mandatory standalone Narrative Dynamics stage. Existing preparation/process/NPC/narration architecture remains in force. R2.5 narrow S14 activation is owned inside multiplayer collaboration because that concrete consumer triggered it; it does not activate generic authored-arc/world-pressure/planning machinery.

Round 2 has no generic optional-capability gate. Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers, cache-specific optimization and similar ideas remain dormant until their own triggers occur.

---

# 16. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  COMPLETE / ARCHITECTURE CLOSED
R2.2  COMPLETE / ARCHITECTURE CLOSED
R2.3  COMPLETE / ARCHITECTURE CLOSED
R2.4  COMPLETE / ARCHITECTURE CLOSED
R2.5  COMPLETE / ARCHITECTURE CLOSED
R2.6  COMPLETE / ARCHITECTURE CLOSED
R2.7  IN PROGRESS

R2.7 next activity:
    construct task-specific dependency subgraph / Source Manifest
    -> map accepted semantic owners into GAME/DEV/schema/catalog/instruction/test obligations
    -> perform holistic duplicate-authority / composition / dormant-trigger review
    -> produce implementation-planning entry criteria

Broad implementation: BLOCKED.
```