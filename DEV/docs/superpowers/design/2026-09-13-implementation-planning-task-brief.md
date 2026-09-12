# HDM Implementation Planning — Task Brief

Status: **STEP 1 DRAFT — PENDING WHOLE-PROJECT CRITIC**

Date: 2026-09-13

No production implementation, migration execution, release execution or gameplay bootstrap is authorized by this brief.

## 1. Purpose

R2.7 architecture and machine-realization reconciliation is closed. The next authorized program unit is implementation planning.

This stage must convert the accepted HDM architecture and the exact WP-27 readiness corpus into a **complete executable implementation-planning package**. Its final result is not merely an answer to "what should we code first?". It must establish the complete currently authorized implementation scope, dependency order, bounded plan/task decomposition, verification mapping and execution gates well enough that, after mandatory Senior plan review / GO, an implementation worker can begin Task 1 without inventing missing architecture or redoing planning.

The governing question is:

> **Can the complete currently active HDM implementation scope be executed from a reviewed set of bounded plans, with every task traceable to accepted owners/readiness leaves, every dependency and proof obligation explicit, and no dormant/rejected work accidentally activated?**

Implementation planning closes only when the answer is **yes** and the complete plan package has received the required Senior PASS / GO.

## 2. Authority and hard boundaries

Planning derives implementation work; it does not become a new semantic owner.

Authority order remains:

```text
accepted native semantic/product owner
  > exact WP-27 Step-2 readiness/source record for classification/traceability
  > WP-27 canonical readiness specification
  > implementation-planning artifacts
  > derivative routing/status/history
```

Hard boundaries:

- no accepted architecture is reopened for implementation convenience;
- no readiness/workstream grouping gains semantic authority;
- no no-work/deferred/dormant/rejected item is activated without its exact accepted trigger;
- no current proof class is silently credited by a different proof class;
- no production code, runtime schema mutation, migration execution or release execution occurs during planning;
- implementation-selectable details may be selected only where current owners actually delegate them;
- any planning choice that would determine semantic authority, canonical ownership, persistent/interface policy, disclosure/access eligibility, material compatibility/migration policy, hard-to-reverse product semantics or another human-owned boundary must stop at the owning decision gate.

## 3. Task-specific Source Manifest

### 3.1 Process / current state — controlling

- `AGENTS.md`
- applicable runtime overlay under `DEV/AGENT_RUNTIMES/`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`
- `DEV/CURRENT_PROGRESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` for sequence/scope only
- `DEV/RELEASE/VERSIONING.md` and its detailed owner for future Version Impact Gates

### 3.2 Planning/readiness corpus — controlling for classification and traceability

- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md`
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-5-candidate-readiness-spec.md` where exact planning-container membership/routing is needed
- `DEV/docs/superpowers/specs/2026-09-11-r2-7-final-architecture-machine-realization-closure-canonical-spec.md`
- final R2.7 reconciliation closure/review artifacts where they constrain current disposition or unresolved-state claims

### 3.3 Routing / Product Owner intent

- `DEV/PROJECT_MAP.md` — discovery only
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — integrated locator only
- `DEV/PRODUCT_OWNER_INPUT.md` — Product Owner intent/routing; accepted owners remain semantic authority

### 3.4 Native owners and machine consumers — dynamically required

For every active readiness leaf, planning must follow that leaf to its actual current native owner(s), later accepted amendments, and implicated machine/runtime/schema/test consumers. The task may not substitute an umbrella WP-27 summary for these sources.

This includes, where implicated by exact leaves, current owners and consumers across:

- catalog/class/identity and deterministic mechanics;
- Actor/entity/rules/effects/lifecycle;
- Context Runtime, role containment, information/disclosure;
- persistence/storage/durability/recovery/session/currentness/LIVE/chronology;
- multiplayer/collaboration;
- Story/Commentator/retrospective continuity;
- bootstrap/install/campaign lifecycle;
- failure/degradation/diagnostics;
- version/update/migration/release/package/legal;
- DEV schemas/catalogs/tests/tools and GAME runtime/schema/template/install surfaces.

### 3.5 Research evidence

- `DEV/docs/superpowers/research/2026-09-13-hg01-novel-action-hourglass-result.md` — planning evidence only; never a semantic owner.

HG-01 constraints must be reconciled to the existing public owners they restate before being attached to any implementation task.

## 4. Required planning products

The stage must produce a **package of bounded implementation plans plus an orchestration/traceability layer**, not one monolithic implementation document and not eleven plans mechanically copied from WP-27 workstream headings.

### P1 — Exact readiness disposition ledger

Account for the complete WP-27 planning corpus at item level.

For every `R27-R###` readiness record and every explicit no-work terminal, preserve at least:

```text
readiness/source identity
native owner(s)
current disposition
current activation state
implementation consequence
predecessors/dependencies
proof-channel obligations
defer/revisit trigger
negative/rejected constraints
version/migration boundary
current machine realization state
planning route
```

The planning route must distinguish at least:

```text
ACTIVE_IMPLEMENTATION
ACTIVE_DETERMINISTIC_PROOF
ACTIVE_SCENARIO_ACCEPTANCE
ALREADY_REALIZED
DORMANT_OR_DEFERRED
EMPIRICAL_ONLY_AFTER_TRIGGER
RELEASE_TIME_ONLY
REJECTED_OR_OUT_OF_SCOPE
EXPLICIT_NO_WORK
```

A readiness leaf may carry more than one future proof obligation, but planning must not collapse distinct proof channels or activation gates.

### P2 — Frozen current active implementation set

Derive the exact set of work that is active *now* under current owners and triggers.

The active set must be reproducible from P1 rather than inferred from previous summary counters. Any difference from prior Round-2 active/no-work accounting must be explained by an exact current owner/trigger, not by convenience.

### P3 — Dependency DAG

Construct a dependency graph over the active implementation/proof obligations.

Edges must come from actual owner/consumer/prerequisite relationships. Workstream adjacency, file proximity, similar terminology or preferred coding order are not dependency evidence.

The DAG must preserve the default owner-valid progression where applicable:

```text
accepted owner semantics
-> owner-local schema / route / template / validator
-> owner-local producer / consumer / runtime behavior
-> deterministic contract/TDD proof
-> scenario/adversarial acceptance
-> empirical proof when activated
-> release-time proof when activated
```

Cycles must be investigated. A genuine semantic/ownership cycle that cannot be decomposed is a planning blocker/System-Impact event, not permission to invent ordering.

### P4 — Bounded plan decomposition

Partition the active DAG into bounded implementation plans and independently testable tasks.

Each plan must:

- name every readiness leaf it discharges;
- identify exact approved specs/native owners;
- define exact expected owners/consumers and interfaces in its Implementation Impact Envelope;
- preserve negative laws and out-of-scope surfaces;
- identify task/checkpoint boundaries;
- define interfaces between dependent tasks/plans;
- contain executable TDD/verification steps sufficient for an implementation worker with no chat-local context;
- avoid duplicating another plan's semantic responsibility.

A single task may discharge multiple leaves only when their owner/activation/proof/version semantics remain lossless. Otherwise split it.

### P5 — Implementation Impact Envelopes

Every substantial plan must include the envelope required by `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`:

```text
SPEC / APPROVED DESIGN
BASELINE REF OR SHA
EXPECTED OWNERS TO CHANGE
EXPECTED CONSUMERS TO CHANGE
ALLOWED INTERFACES / CONTRACTS TO CHANGE
PROTECTED ARCHITECTURE INVARIANTS
ARCHITECTURE-SENSITIVE SURFACES
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION
KNOWN OUT-OF-SCOPE OWNERS / SURFACES
```

### P6 — Verification and acceptance map

For each plan/task, explicitly map the required evidence classes:

- deterministic/static/schema/TDD proof;
- integration/contract proof;
- scenario/adversarial acceptance;
- empirical/supported-target proof, only when activated;
- release-time exact-candidate/asset/fresh-Project proof, only when activated.

No plan may treat current CI or one proof channel as universal acceptance.

### P7 — Version / migration impact routing

Planning must not pre-invent bumps or migrations. It must identify, per task/plan, the HDM-owned version/revision/schema/generation namespaces potentially affected and the exact future Version Impact Gate/owner that will decide the concrete delta.

Migration work remains absent unless the accepted compatibility trigger and concrete source/target delta activate it.

### P8 — HG-01 planning-constraint integration

Route the four HG-01 constraints only into plans/tasks whose actual owner surface is implicated:

1. NPC/faction voluntary reasoning remains Actor/NPC semantics, not human multiplayer currentness;
2. ordinary micro-position/transient attention/facing/distraction/reaction remains fiction unless a native owner requires typed state;
3. missing exact realization evidence is not automatic new architecture;
4. mechanically-null adjudication must not become a generic prose-to-StateDelta/workflow consequence bridge.

The planning package must record where each constraint is enforced by owner/plan/test and where it is not applicable. HG-01 must not become an alternate semantic authority.

### P9 — Execution-wave projection

Derive an execution projection from the DAG:

- topological roots;
- plans/tasks that may execute independently in parallel;
- mandatory join/integration points;
- blockers that prevent downstream work;
- final integration/acceptance gates.

Do not manufacture a total order where no dependency edge exists. "What we code first" is a derived property of the complete DAG/package, not the purpose of the stage.

### P10 — Full coverage matrix

Maintain mechanically checkable traceability at least equivalent to:

```text
readiness leaf/source
-> native owner
-> current disposition/activation
-> implementation plan
-> task(s)
-> predecessors
-> expected changed owner/consumer surface
-> proof obligations
-> Version Impact route
-> completion/acceptance route
```

The package must make omissions and unauthorized additions detectable.

### P11 — Senior plan-review package

Submit the complete implementation-planning package to mandatory independent Senior plan review before any production implementation starts.

The review must test at least:

- complete leaf/source coverage;
- activation/no-work/defer correctness;
- dependency correctness and cycles;
- boundedness of each plan/task;
- Impact Envelope completeness;
- owner/authority preservation;
- negative-law and rejected-architecture preservation;
- proof-channel mapping;
- version/migration routing;
- HG-01 constraint routing;
- executable detail sufficient for autonomous implementation;
- absence of hidden architecture/product decisions.

All BLOCKING/SIGNIFICANT plan-review findings must be repaired and re-reviewed before GO.

## 5. Protected cross-system laws

Planning must preserve the current WP-27 laws, including at minimum:

- LLM semantic judgment remains separated from deterministic execution;
- truth, actor knowledge, human disclosure and access eligibility remain distinct;
- one physical context does not erase logical role/information containment;
- currentness/publication/recovery remain owner-based;
- accepted causal inputs/RNG/identity remain frozen across downstream retry/recovery where required;
- Context Runtime remains bounded/ephemeral and non-authoritative;
- catalog/current-definition identity remains exact-owner based;
- Story remains noncanonical to gameplay and does not become an ACL/history authority;
- ordinary-turn zero-extra-serial constraints remain valid;
- rejected global failure/retry/queue/scheduler/ACL architecture remains rejected;
- partition/scale behavior remains trigger-gated and writer-specific;
- migration/version work remains exact-target/delta-driven;
- proof channels remain non-substitutable.

Planning must also preserve all exact owner-local negative laws carried by individual readiness records even when not repeated here.

## 6. Forbidden planning shortcuts

The following are plan failures:

- treating all 145 readiness leaves as active backlog;
- planning from the eleven WP-27 workstream headings without exact leaf/native-owner recovery;
- using current machine shape as proof of desired architecture;
- creating tasks named only at subsystem level (for example "implement persistence" or "implement Actor") with no leaf/owner/test boundary;
- turning dormant empirical/release obligations into current implementation work;
- selecting implementation convenience that changes authority/semantics;
- reviving rejected generic registries, buses, schedulers, queues, retry services, ACLs, sharding services or Story-as-canon patterns;
- treating documentation/research/roadmaps as semantic authority;
- claiming complete planning while any active leaf lacks a plan/task/proof route;
- claiming complete planning while any task lacks a native owner/readiness justification;
- declaring a single first task before the dependency graph is complete enough to prove that it is actually a root and not an artifact of partial discovery.

## 7. Completion predicates

Implementation Planning may enter final Senior review only when all of the following are true:

```text
WP27_READINESS_RECORDS_ACCOUNTED: 145 / 145
EXPLICIT_NO_WORK_TERMINALS_ACCOUNTED: 79 / 79
ACTIVE_SET_DERIVED_FROM_CURRENT_OWNERS: YES
UNEXPLAINED_ACTIVATION_DELTA: 0
ACTIVE_IMPLEMENTATION_LEAVES_WITHOUT_PLAN: 0
ACTIVE_PROOF_OBLIGATIONS_WITHOUT_ROUTE: 0
PLANNED_TASKS_WITHOUT_NATIVE_OWNER_OR_READINESS_JUSTIFICATION: 0
UNRESOLVED_DEPENDENCY_EDGES: 0
UNRESOLVED_DAG_CYCLES: 0
DORMANT_OR_NO_WORK_PREMATURELY_ACTIVATED: 0
REJECTED_ARCHITECTURE_RESURRECTED: 0
IMPACT_ENVELOPE_MISSING: 0
REQUIRED_PROOF_CHANNELS_UNMAPPED: 0
HG01_CONSTRAINTS_UNROUTED_WHERE_APPLICABLE: 0
VERSION_IMPACT_ROUTE_MISSING_FOR_PLANNED_TASKS: 0
MATERIAL_HUMAN_DECISION_HIDDEN_IN_PLAN: 0
```

Final stage closure additionally requires:

```text
COMPLETE_IMPLEMENTATION_PLAN_PACKAGE: YES
MANDATORY_SENIOR_PLAN_REVIEW: PASS / GO
SUBSTANTIVE_IMPLEMENTATION_STARTED_BEFORE_GO: NO
```

## 8. Human-decision rule

Current R2.7/WP-27 closure records report no open Product Owner or architecture decision at planning entry. The planner therefore proceeds autonomously through evidence recovery, classification, decomposition, plan writing, traceability and verification mapping.

The planner stops for Product Owner/human-architect judgment only if exhaustive evidence work exposes a genuine unresolved decision involving product semantics, material architecture trade-offs, canonical authority/ownership, meaningful compatibility/migration policy, explicit material risk acceptance, hard-to-reverse scope, or another boundary reserved to the human architect by current process.

Repository/document volume, uncertainty caused by incomplete reading, or inconvenience in decomposing the DAG are not human-decision triggers.

## 9. Step-1 output and next gate

This Task Brief itself is Step-1 framing for the implementation-planning stage. Before planning decomposition begins it must pass the mandatory whole-project Task-Brief critic required by `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

The critic must use `DEV/PROJECT_MAP.md` to reconstruct direct and indirect dependencies, inspect the actual controlling/readiness/native-owner sources needed to challenge this framing, and attempt to prove that the brief:

- misses required source families or consumers;
- weakens a current owner/negative law;
- confuses planning with architecture or implementation;
- cannot actually produce a complete executable plan package;
- creates unverifiable completion criteria;
- makes the human architect compensate for incomplete evidence work;
- or prematurely activates deferred/rejected work.

All mechanically resolvable BLOCKING/SIGNIFICANT findings must be repaired in this brief before the Step-1 package is presented for the mandatory Senior review stop.

Step 2 / substantive readiness decomposition must not begin until that review stop receives GO.

## 10. Version Impact

This Task Brief is planning-process documentation only. It changes no runtime/module/schema/catalog/protocol/persistence/release/migration semantics.

```text
VERSION_IMPACT: NONE
```
