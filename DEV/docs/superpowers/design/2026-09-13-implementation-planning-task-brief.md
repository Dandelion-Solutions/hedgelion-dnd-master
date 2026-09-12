# HDM Implementation Planning — Task Brief

Status: **PLANNING-ENTRY BRIEF — WHOLE-PROJECT CRITIC REPAIRED / READY FOR SUBSTANTIVE PLANNING**

Date: 2026-09-13

No production implementation, migration execution, release execution or gameplay bootstrap is authorized by this brief.

This brief is preparatory planning-entry framing requested by the Product Owner. It is **not** a new architecture stage, not Step 1 of a new eight-step architecture cycle, and does not create an additional Senior gate before implementation planning. Current `DEV/CURRENT_PROGRESS.md` already authorizes implementation planning. The next mandatory Senior gate remains review of the **complete implementation-planning package** before production implementation.

## 1. Purpose

R2.7 architecture and machine-realization reconciliation is closed and the independent Final Senior review authorized implementation-planning entry.

This stage must convert the accepted HDM architecture and exact WP-27 readiness corpus into a **complete executable implementation-planning package**. Its final result is not merely an answer to "what should we code first?". It must establish the complete currently active implementation scope, dependency DAG, bounded plan/task decomposition, verification mapping, Version Impact routing, execution waves and final plan-review package well enough that, after mandatory Senior plan review / GO, an implementation worker can begin the approved initial execution wave without inventing missing architecture or redoing planning.

The governing question is:

> **Can the complete currently active HDM implementation scope be executed from a reviewed set of bounded plans, with every task traceable to accepted owners/readiness leaves, every dependency and proof obligation explicit, and no dormant/rejected work accidentally activated?**

Implementation planning closes only when the answer is **yes** and the complete package has received the required Senior PASS / GO.

## 2. Authority and hard boundaries

Planning derives implementation work; it does not become a semantic owner.

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
- no proof class is silently credited by another proof class;
- no production code, runtime schema mutation, migration execution or release execution occurs during planning;
- implementation-selectable details may be selected only where current owners delegate them;
- any planning choice that would determine semantic authority, canonical ownership, persistent/interface policy, disclosure/access eligibility, material compatibility/migration policy, hard-to-reverse product semantics or another human-owned boundary must stop at the owning decision gate.

## 3. Task-specific Source Manifest

### 3.1 Process / current state — controlling

- `AGENTS.md`
- applicable runtime overlay under `DEV/AGENT_RUNTIMES/`
- current Superpowers process skills, including `using-superpowers` and `writing-plans` when executable plans are constructed
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/DEVELOPMENT_EXECUTION_PROCESS.md`
- `DEV/CURRENT_PROGRESS.md` — sole current gate/cursor authority
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` — sequence/scope only
- `DEV/RELEASE/VERSIONING.md` and its detailed owner for future Version Impact Gates

### 3.2 Planning-entry / readiness corpus

- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md`
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md` — item-level classification/traceability owner
- `DEV/docs/superpowers/design/2026-09-11-r2-7-WP-27-step-5-candidate-readiness-spec.md` — **DESIGN PROVENANCE / PLANNING PROJECTION ONLY**; grouping hints only, never semantic, activation or dependency authority
- `DEV/docs/superpowers/specs/2026-09-11-r2-7-final-architecture-machine-realization-closure-canonical-spec.md` — R2.7 closure projection
- `DEV/docs/superpowers/design/2026-09-11-r2-7-final-reconciliation-final-senior-review.md` — exact independent Senior PASS / GO that enabled planning entry

### 3.3 Routing / Product Owner intent

- `DEV/PROJECT_MAP.md` — discovery only
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — locator only
- `DEV/PRODUCT_OWNER_INPUT.md` — Product Owner intent/routing; accepted owners remain semantic authority

### 3.4 Native owners and current machine consumers — dynamically required

For every active readiness leaf, planning must follow that leaf to its actual current native owner(s), later accepted amendments and implicated machine/runtime/schema/test consumers. An umbrella WP-27 summary is insufficient.

For every bounded plan, the planner must freshly inspect the exact current affected machine/runtime/schema/test surfaces. The Step-2 recorded machine state is routing/evidence, not a substitute for current files.

The dynamic source set includes, where implicated by exact leaves:

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

## 4. Planning baseline and currentness

At substantive planning entry, record:

```text
PLANNING_BASELINE_SHA: <current authoritative v1/engine-rearchitecture HEAD after framing publication/read-back>
```

For each bounded plan, record the exact owner/spec/machine surfaces inspected. Before each coherent plan publication and before final plan review:

1. fresh-check current authoritative HEAD;
2. determine whether accepted owner/spec/machine/runtime surfaces relevant to that plan changed since its baseline/read;
3. if yes, reconcile affected readiness leaves, DAG edges and tasks before claiming completeness;
4. if only planning/research documentation advanced HEAD without changing accepted semantics/machine consumers, preserve the semantic baseline record but still obtain publication read-back.

A stale plan may not enter final review merely because its original baseline was correct when drafted.

## 5. Required planning products

The stage must produce a **package of bounded executable implementation plans plus an orchestration/traceability layer**, not one monolithic document and not eleven plans copied from WP-27 workstream headings.

### P1 — Lossless readiness disposition ledger

Account for all 145 `R27-R###` readiness records and all 79 explicit no-work terminals at item level.

Do **not** encode current state as one lossy enum. Preserve orthogonal axes at least as follows:

```text
readiness/source identity
native owner(s)
activation_state
realization_state / implementation_work
proof_channels[]
future_triggered_channels[]
terminal/no-work disposition when applicable
implementation consequence
predecessors/dependencies
defer/revisit trigger
negative/rejected constraints
version/migration boundary
current machine realization state
planning route(s)
```

A leaf may simultaneously require implementation, deterministic proof and scenario acceptance while empirical/release proof remains separately trigger-gated.

### P2 — Exact current active set + summary reconciliation

Derive the exact current active implementation/proof set from P1 and current owners/triggers.

Do not assume that the final active set equals the historical/global `ROUND2_ACTIVE_READINESS: 43` count. Preserve an explicit reconciliation showing how the final active set relates to:

- the Round-2 active/no-work summary;
- non-Round-2 readiness records;
- already-realized records;
- dormant/deferred records;
- empirical/release-only future obligations.

Any delta must be explained by an exact current owner/trigger.

```text
UNEXPLAINED_ACTIVE_SET_DELTA: 0
```

### P3 — Dependency DAG

Construct a dependency graph over all currently active implementation and currently active proof obligations.

Edges must come from actual owner/consumer/prerequisite relationships. Workstream adjacency, file proximity, similar terminology or preferred coding order are not dependency evidence.

Default progression where applicable:

```text
accepted owner semantics
-> owner-local schema / route / template / validator
-> owner-local producer / consumer / runtime behavior
-> deterministic contract/TDD proof
-> scenario/adversarial acceptance
```

Empirical and release-time proof nodes enter the executable DAG only if their accepted current trigger exists; otherwise they remain exact deferred acceptance routes.

Cycles must be investigated. A genuine semantic/ownership cycle that cannot be decomposed is a planning blocker/System-Impact event, not permission to invent ordering.

### P4 — Bounded executable plan decomposition

Partition the active DAG into bounded implementation plans and independently testable tasks.

Each plan must:

- name every readiness leaf it discharges;
- identify exact approved specs/native owners;
- freshly inspect and name current affected files/consumers;
- define its Implementation Impact Envelope;
- preserve negative laws and out-of-scope surfaces;
- identify task/checkpoint boundaries and interfaces between dependent tasks/plans;
- avoid duplicating another plan's semantic responsibility.

Executable plan artifacts must use the current `superpowers:writing-plans` requirements plus HDM overrides and be stored under `DEV/docs/superpowers/plans/`.

They must include exact file paths, interfaces/signatures/contracts where known from current owners, concrete RED/GREEN verification commands and expected outcomes, integration checks, checkpoint boundaries and no placeholders such as `TODO`, `TBD` or "add tests later". Each plan must self-review spec coverage, placeholder absence and interface/type consistency before final package review.

A task may discharge multiple leaves only when their owner/activation/proof/version semantics remain lossless; otherwise split it.

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

For each plan/task, map the required evidence classes:

- deterministic/static/schema/TDD proof;
- integration/contract proof;
- scenario/adversarial acceptance;
- empirical/supported-target proof only when its real-target trigger exists;
- release-time exact-candidate/asset/fresh-Project proof only when its release trigger exists.

Current plan completeness requires executable routes for currently active implementation/deterministic/scenario work and exact deferred owner/trigger routes for future-only empirical/release acceptance. It must **not** fabricate current tasks for future-only proof channels.

No plan may treat current CI or one proof channel as universal acceptance.

### P7 — Version / migration impact routing

Planning must not pre-invent bumps or migrations. Per plan/task identify the HDM-owned version/revision/schema/generation namespaces potentially affected and the exact future Version Impact Gate/owner that will classify the concrete implementation delta.

Migration work remains absent unless the accepted compatibility trigger and concrete source/target delta activate it.

### P8 — HG-01 planning-constraint integration

Route the four HG-01 constraints only into plans/tasks whose actual public owner surface is implicated:

1. NPC/faction voluntary reasoning remains Actor/NPC semantics, not human multiplayer currentness;
2. ordinary micro-position/transient attention/facing/distraction/reaction remains fiction unless a native owner requires typed state;
3. missing exact realization evidence is not automatic new architecture;
4. mechanically-null adjudication must not become a generic prose-to-StateDelta/workflow consequence bridge.

Record where each constraint is owner-backed/enforced and where it is not applicable. HG-01 never becomes an alternate semantic authority.

### P9 — Execution-wave projection

Derive from the complete DAG:

- all topological roots;
- an `INITIAL_EXECUTION_WAVE` containing independently eligible root tasks/plans;
- parallelizable work;
- mandatory joins/integration points;
- blockers;
- final integration/acceptance gates.

Do not manufacture a total order where no dependency exists. A recommended default first task/slice may be named only when dependency, integration-risk, review leverage or other explicit evidence justifies choosing among multiple eligible roots.

"What we code first" is therefore a derived property of the complete package, not the stage's endpoint.

### P10 — Full bidirectional coverage matrix

Maintain mechanically checkable traceability at least equivalent to:

```text
readiness leaf/source
-> native owner
-> current activation/realization/proof state
-> implementation plan
-> task(s)
-> predecessors
-> current expected changed owner/consumer surface
-> proof obligations
-> Version Impact route
-> completion/acceptance route
```

And reverse-check:

```text
planned task
-> exact readiness/native-owner justification
```

The package must make omissions and unauthorized additions detectable.

### P11 — Complete Senior plan-review package

Submit the complete implementation-planning package to mandatory independent Senior plan review before any production implementation starts.

The review must test at least:

- complete leaf/source coverage;
- activation/no-work/defer correctness;
- active-set reconciliation;
- dependency correctness and cycles;
- boundedness/executability of each plan/task;
- currentness/baseline reconciliation;
- fresh machine/consumer inspection;
- Impact Envelope completeness;
- owner/authority preservation;
- negative-law/rejected-architecture preservation;
- proof-channel mapping;
- version/migration routing;
- HG-01 constraint routing;
- absence of hidden architecture/product decisions.

All BLOCKING/SIGNIFICANT plan-review findings must be repaired and re-reviewed before GO.

## 6. Protected cross-system laws

Planning must preserve all current WP-27/Final Reconciliation laws, including:

- LLM semantic judgment separated from deterministic execution;
- truth, Actor knowledge, human disclosure and access eligibility distinct;
- logical role/information containment preserved in one physical context;
- owner-based currentness/publication/recovery;
- accepted causal inputs/RNG/identity frozen across downstream retry/recovery where required;
- bounded/ephemeral non-authoritative Context Runtime;
- exact-owner catalog/current-definition identity;
- noncanonical Story with no second ACL/history authority;
- ordinary-turn zero-extra-serial constraints;
- rejected global failure/retry/queue/scheduler/ACL architecture remains rejected;
- trigger-gated writer-specific partition/scale behavior;
- exact-target/delta-driven migration/version work;
- non-substitutable proof channels.

Exact owner-local negative laws in individual readiness records remain controlling even when not repeated here.

## 7. Forbidden planning shortcuts

Plan failure includes:

- treating all 145 readiness leaves as active backlog;
- forcing the final active set to equal a summary counter;
- planning from the eleven WP-27 workstream headings without exact leaf/native-owner recovery;
- building a plan solely from the historical machine state recorded in Step-2 without reading current consumers;
- using current machine shape as architecture authority;
- subsystem-level tasks such as "implement persistence" or "implement Actor" with no leaf/owner/test boundary;
- turning dormant empirical/release obligations into current implementation work;
- selecting convenience that changes authority/semantics;
- reviving rejected generic registries, buses, schedulers, queues, retry services, ACLs, sharding services or Story-as-canon patterns;
- treating documentation/research/roadmaps as semantic authority;
- high-level plans that omit exact files/interfaces/RED-GREEN verification required by `writing-plans`;
- claiming complete planning while an active leaf/proof lacks a route;
- claiming complete planning while a task lacks native-owner/readiness justification;
- declaring one first task before the complete DAG proves root eligibility.

## 8. Completion predicates

The complete package may enter final Senior plan review only when:

```text
WP27_READINESS_RECORDS_ACCOUNTED: 145 / 145
EXPLICIT_NO_WORK_TERMINALS_ACCOUNTED: 79 / 79
ACTIVE_SET_DERIVED_FROM_CURRENT_OWNERS: YES
ROUND2_AND_NON_ROUND2_ACTIVE_SET_RECONCILED: YES
UNEXPLAINED_ACTIVE_SET_DELTA: 0
ACTIVE_IMPLEMENTATION_LEAVES_WITHOUT_EXECUTABLE_PLAN: 0
CURRENTLY_ACTIVE_PROOF_OBLIGATIONS_WITHOUT_ROUTE: 0
FUTURE_ONLY_EMPIRICAL_OR_RELEASE_OBLIGATIONS_WITHOUT_OWNER_TRIGGER_ROUTE: 0
PLANNED_TASKS_WITHOUT_NATIVE_OWNER_OR_READINESS_JUSTIFICATION: 0
UNRESOLVED_DEPENDENCY_EDGES: 0
UNRESOLVED_DAG_CYCLES: 0
DORMANT_OR_NO_WORK_PREMATURELY_ACTIVATED: 0
REJECTED_ARCHITECTURE_RESURRECTED: 0
PLANS_WITH_STALE_UNRECONCILED_OWNER_OR_MACHINE_BASELINE: 0
IMPACT_ENVELOPE_MISSING: 0
EXECUTABLE_PLAN_PLACEHOLDERS: 0
REQUIRED_PROOF_CHANNELS_UNMAPPED: 0
HG01_CONSTRAINTS_UNROUTED_WHERE_APPLICABLE: 0
VERSION_IMPACT_ROUTE_MISSING_FOR_PLANNED_TASKS: 0
MATERIAL_HUMAN_DECISION_HIDDEN_IN_PLAN: 0
INITIAL_EXECUTION_WAVE_DERIVED: YES
```

Final stage closure additionally requires:

```text
COMPLETE_IMPLEMENTATION_PLAN_PACKAGE: YES
MANDATORY_SENIOR_PLAN_REVIEW: PASS / GO
SUBSTANTIVE_IMPLEMENTATION_STARTED_BEFORE_GO: NO
```

## 9. Human-decision rule

Current R2.7/WP-27 closure reports no open Product Owner or architecture decision at planning entry. The planner therefore proceeds autonomously through evidence recovery, classification, DAG construction, plan writing, traceability and verification mapping.

Stop for Product Owner/human-architect judgment only if exhaustive evidence exposes a genuine unresolved decision involving product semantics, material architecture trade-offs, canonical authority/ownership, meaningful compatibility/migration policy, explicit material risk acceptance, hard-to-reverse scope or another current human-owned boundary.

Repository volume, incomplete reading, ambiguity resolvable from current owners, or inconvenience in DAG decomposition are not human-decision triggers.

## 10. Current route after brief critic

The strict whole-project framing critic is recorded in:

- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-task-brief-critic.md`

Its mechanically resolvable findings are incorporated in this repaired brief.

This critic is a preparatory quality gate requested by the Product Owner. It does **not** create an additional mandatory Senior stop.

After critic re-review confirms the repairs, the authorized route is:

```text
fresh planning baseline/currentness pin
-> P1/P2 exact lossless readiness + active-set reconciliation
-> P3 complete dependency DAG
-> P4-P8 bounded executable plans / envelopes / proof and HG-01 routing
-> P9/P10 execution waves + bidirectional completeness proof
-> P11 complete independent Senior plan review
-> repair/re-review until PASS / GO
-> production implementation may begin only after GO
```

## 11. Version Impact

This brief is planning-process documentation only and changes no runtime/module/schema/catalog/protocol/persistence/release/migration semantics.

```text
VERSION_IMPACT: NONE
```
