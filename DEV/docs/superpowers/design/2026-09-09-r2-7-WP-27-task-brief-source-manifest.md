# R2.7 WP-27 Step 1 — Final Implementation-Planning Readiness — Task Brief + Open-World Source Manifest

Status: **WORKER STEP-1 CRITIC-REPAIRED / MANDATORY INDEPENDENT SENIOR REVIEW PENDING / IMPLEMENTATION PLANNING NOT AUTHORIZED**

Date: 2026-09-09

## 0. Authorization and hard stop

Product Owner stage-entry authorization for WP-27 was supplied explicitly on 2026-09-09.

This authorization starts **WP-27 Step 1 only** under the current R2.7 process:

```text
Source Manifest
-> Task Brief
-> mandatory Wide-Angle Critic
-> repair / redecompose until no unresolved blocking/significant framing defect
-> mandatory independent Senior Step-1 review
-> STOP
```

The mandatory Wide-Angle Critic is published at:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-27-step-1-whole-project-critic.md`.

Worker repair has closed all blocking/significant Step-1 framing findings. The mandatory independent Senior gate remains unsatisfied.

It does **not** authorize:

- WP-27 Steps 2–8 before the mandatory Step-1 Senior gate;
- implementation planning;
- implementation;
- release or migration execution;
- real campaign migration;
- gameplay bootstrap.

Global currentness remains owned by `DEV/CURRENT_PROGRESS.md`.

---

# 1. Problem statement

WP-27 is the final numbered R2.7 audit domain before the mandatory R2.7 final reconciliation. It must determine whether the accepted HDM architecture can be handed to implementation planning without requiring the implementation planner to make hidden architecture, authority, product, compatibility, security or material topology decisions.

The controlling questions from R2.7 scope discovery are:

1. Can every implementation workstream be derived from an approved owner / machine / test mapping?
2. Are dependency order, migration order, test-first obligations and publication/release consequences explicit?
3. Is every remaining unknown classified as implementation detail, post-MVP evaluation, safe deferred trigger or owner-resolved trade-off?
4. Does any unresolved architecture question remain whose answer could materially change implementation topology, data model or interfaces?

WP-27 may pass only if question 4 is ultimately answered `NO` for the implementation-planning entry boundary.

WP-27 closure itself still does not start implementation planning. The required sequence remains:

```text
WP-27 closure
-> R2.7 final reconciliation
-> implementation-planning entry resolution
-> implementation planning only if the final R2.7 gate passes
```

---

# 2. Selected Step-1 framing direction

WP-27 shall use:

```text
OWNER-DERIVED IMPLEMENTATION GRAPH
+ BIDIRECTIONAL READINESS COVERAGE
+ EXPLICIT ACTIVATION / DEFER / EMPIRICAL CLASSIFICATION
+ BLOCKER-ONLY BOUNDED ARCHITECTURE REOPEN
```

This is an audit organization, not a new semantic architecture owner.

## 2.1 Owner-derived implementation graph

Every future implementation workstream candidate must be derivable through a chain equivalent to:

```text
accepted semantic / machine / Product Owner obligation
-> concrete implementation destination family
-> dependency predecessors
-> schema/version/migration consequences
-> TDD / deterministic verification obligations
-> scenario / empirical obligations where applicable
-> release / publication consequences
```

A closed architecture document is not proof of completed machine realization. Conversely, a deferred realization sentence is not automatic authorization to build every concept named in it.

## 2.2 Bidirectional readiness proof

WP-27 must preserve the R2.7 two-way proof:

```text
ARCHITECTURE -> IMPLEMENTATION
for each accepted owner obligation that requires realization:
    identify the future workstream/destination/proof path
    or classify it as already realized / dormant / safe deferred / out of scope

CURRENT MACHINE -> OWNER
for each current GAME/DEV runtime/schema/catalog/template/tool/test responsibility
material to future implementation planning:
    identify its accepted owner
    or classify it as already-realized support, derived support, stale debt,
    implementation-only detail, verification-only surface or historical evidence
```

WP-27 must not substitute current indexes/roadmaps/status summaries for owning sources where correctness depends on the exact law.

---

# 3. Readiness record model

The later WP-27 synthesis shall maintain one item-level readiness record per material future workstream or deferred obligation, with fields equivalent to:

```text
readiness_id
source_owner_refs[]
accepted_law_or_obligation_refs[]
product_owner_routes[]
current_realization_state
implementation_destination_families[]
dependency_predecessors[]
required_machine_or_persistent_shape_boundary
version_impact_classification
migration_or_update_consequence
test_first_obligations[]
scenario_acceptance_obligations[]
empirical_acceptance_obligations[]
release_or_publication_consequences[]
activation_state
remaining_implementation_choices[]
architecture_blocker_test_result
defer_or_revisit_trigger
negative_requirements[]
```

Exact serialization of this audit ledger is a documentation choice, not a runtime schema.

---

# 4. Remaining-unknown classification

Every still-open item encountered by WP-27 must receive one of the following semantic dispositions or an equivalent explicit class:

```text
ALREADY_REALIZED
IMPLEMENTATION_OBLIGATION
IMPLEMENTATION_DETAIL
VERIFICATION_OBLIGATION
RELEASE_TIME_FORWARD_OBLIGATION
REAL_TARGET_EMPIRICAL_OBLIGATION
MEASUREMENT_DORMANT
SAFE_DEFERRED_TRIGGER
STALE_DEBT
OUT_OF_SCOPE_OR_REJECTED
ARCHITECTURE_BLOCKER_CANDIDATE
OWNER_DECISION_REQUIRED
```

These classes are not runtime enums.

## 4.1 Coverage does not mean activation

A current owner may require future proof or define a safe partition/recovery path without activating immediate implementation work.

In particular:

- dormant measurement triggers do not manufacture optimization work;
- future real-target empirical obligations do not require a preimplementation surrogate;
- release-time acceptance gates are not implementation tasks to execute during planning;
- rejected baseline abstractions must not be converted into implementation work merely because a historical/deferred section names them;
- a future Version Impact Gate is a planning/execution obligation, not evidence that a version bump is already required.

---

# 5. Architecture-blocker test

An unresolved choice is an `ARCHITECTURE_BLOCKER_CANDIDATE` only when the available accepted owners do not determine enough constraints and the unresolved answer could materially change one or more of:

```text
semantic authority / ownership
persistent semantic data model or compatibility-bearing schema contract
cross-component public/runtime interface
lifecycle or authorization semantics
correctness-relevant physical topology contract
compatibility / migration / update law
security / disclosure boundary
release/publication authority contract
material Product Owner scope, risk acceptance or product semantics
```

Examples normally **not** sufficient by themselves to reopen architecture, provided current contracts already bound the behavior:

```text
local class/function/module decomposition
pure algorithm selection inside a fixed contract
internal non-authoritative cache indexes
implementation-language data structures
fixture/test harness organization
exact serialization spelling explicitly delegated by an owner while semantic fields/invariants are fixed
concrete partition/page/bucket geometry explicitly delegated by an owner while identity/currentness/reconstruction laws are fixed
```

Closed architecture must not be reopened merely because implementation planning needs to choose a representation. A bounded reopen is required only when the choice crosses the blocker test above.

---

# 6. Open-world Source Manifest

The manifest is dependency-based. Inclusion of a source family means WP-27 must preserve its material implementation/verification/defer semantics; it does not mean every file has equal authority or must be reread front-to-back.

## 6.1 Process / sequencing / currentness — PRIMARY

- `AGENTS.md`;
- `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` for this runtime;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`;
- `DEV/CURRENT_PROGRESS.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`.

## 6.2 Routing / integrated locators — DERIVATIVE

- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
- applicable CORE indexes and Project Instructions only as current routing/activation surfaces, never as substitutes for semantic owners.

## 6.3 Product Owner routes — PRIMARY INTENT / ROUTING, NOT SEMANTIC AUTHORITY

- `DEV/PRODUCT_OWNER_INPUT.md`, all current `PO-001..PO-010` routes;
- accepted owner decisions named by those entries.

Item-level future realization obligations must survive even when the PO entry is `INCORPORATED`.

## 6.4 Round-1 / foundational canonical owner family — PRIMARY

At minimum the current exact-tree canonical family includes:

- Step-1/2 architecture/model owners under `DEV/ARCHITECTURE/`, their accepted assurance/closure records, current schemas/catalogs/tests;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`;
- Step-5.0 through Step-5.14 canonical family, including the 5.3/5.9 integration amendment;
- current House Rules/S6D owners where implementation planning depends on them;
- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`.

WP-27 Step 2 must extract implementation/verification/forward obligations from this family by owning concern; it shall not assume that later R2.7 WPs replaced every foundational law.

## 6.5 Round-2 canonical owner family — PRIMARY

- `2026-08-24-r2-1-continuity-history-canonical-spec.md`;
- `2026-08-24-r2-2-actor-continuity-canonical-spec.md`;
- `2026-08-24-r2-3-context-runtime-canonical-spec.md`;
- `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`;
- `2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`;
- `2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`;
- applicable later amendments/owner decisions and S6D canonical/model owners.

## 6.6 R2.7 closed-domain family WP-01..WP-06 — CLOSED PROVENANCE + CURRENT OWNERS

The early R2.7 domains predate the later one-file-per-WP canonical pattern. Their material implementation obligations must therefore be recovered through:

```text
closed domain design/research/critic/Senior provenance
+ current owning architecture/model/spec contracts
+ current machine/catalog/schema/test realization
+ later accepted supersession/amendment
```

No filename pattern or historical mini-report alone is allowed to define the implementation handoff.

Domains:

- WP-01 product/deployment/repository boundary;
- WP-02 duplicate/global authority;
- WP-03 catalog/class/capability completeness;
- WP-04 Actor/Asset/mechanical-state model, including the progressive READY_PC owner clarification;
- WP-05 deterministic execution pipeline;
- WP-06 rules/adjudication/domain-module compatibility.

## 6.7 R2.7 closed-domain family WP-07..WP-11 — PRIMARY + PROVENANCE

Current exact-tree anchors include:

- WP-07 mini-report plus Step-4/Step-5 information owners;
- WP-08 mini-report + `2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md`;
- WP-09 mini-report + `2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md`;
- WP-10 `2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md` plus its exact record-family/schema/template evidence;
- WP-11 mini-report + `2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`.

## 6.8 R2.7 closed-domain family WP-12..WP-20 — PRIMARY

- `2026-09-02-r2-7-WP-12-hot-sqlite-transaction-realization-canonical-spec.md`;
- `2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`;
- `2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`;
- `2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md`;
- `2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`;
- `2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md`;
- `2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` + final-Senior recovery amendment;
- `2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md`;
- `2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` + current versioning/compatibility owners.

## 6.9 R2.7 closed-domain family WP-21..WP-26 — PRIMARY

- `2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md`;
- `2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md`;
- `2026-09-08-r2-7-WP-23-release-package-version-legal-readiness-canonical-spec.md`;
- `2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md`;
- `2026-09-08-r2-7-WP-25-error-degradation-failure-semantics-canonical-spec.md` + accepted owner direction + final Senior recovery evidence;
- `2026-09-09-r2-7-WP-26-documentation-routing-supersession-consistency-canonical-spec.md` + final independent Senior review.

## 6.10 Current cross-cutting owner decisions — PRIMARY

At minimum:

- PO-001/002 gameplay retrospective + save-and-exit owner decision;
- PO-003 historical Actor decision basis owner decision;
- PO-004 v1 clean-slate compatibility owner decision;
- PO-005 creator-login continuity owner decision;
- PO-006 branch/ref deletion prohibition owner decision;
- PO-007 public provenance/attribution owner decision;
- PO-008 failure/degradation/durability-risk owner direction;
- PO-009 `2026-09-09-story-commentator-self-contained-corpus-owner-decision.md`;
- PO-010 `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`;
- Story producer/source/growth contracts implicated by PO-009/010;
- publication-currentness and logical-ref-retirement amendments where implementation ordering depends on them.

## 6.11 Current machine/runtime realization families — PRIMARY FOR REVERSE CONFORMANCE

Open-world family coverage includes all implicated current:

```text
GAME/CORE/*.md
GAME/SCHEMA/*
GAME/CAMPAIGN/*
GAME/INSTALL/*
GAME/RULES/*
GAME/MIGRATIONS/*
GAME/TOOLS/*

DEV/ARCHITECTURE/*
DEV/CATALOG/*
DEV/SCHEMAS/*
DEV/TESTS/*
DEV/TOOLS/*
DEV/RELEASE/*
.github/workflows/*
```

Step 1 does not claim every file in these families has been semantically re-audited. Step 2 must inspect the concrete consumers nominated by owner obligations and reverse-conformance evidence, expanding only when unresolved references require it.

## 6.12 Release / version / legal / empirical proof family

- `DEV/RELEASE/VERSIONING.md`;
- `DEV/RELEASE/CHECKLIST.md`;
- current release builder/workflow/test surfaces;
- legal/notice owners;
- WP-20 version/migration law;
- WP-22 proof-channel law including Protocol 4;
- WP-23 release-time acceptance order;
- WP-24 Class-B/Class-C scale proof;
- WP-25 real-target host-risk calibration boundary;
- R2.6 empirical acceptance owners.

---

# 7. Mandatory Step-2 evidence-extraction obligations

If Step 1 passes Senior review, Step 2 must produce item-level evidence sufficient to build the readiness graph. It must at minimum extract:

### R27-E01 — closed-domain implementation handoff

For every WP-01..WP-26, identify all material surviving:

```text
implementation obligations
implementation-neutral choices
deterministic verification obligations
scenario acceptance obligations
real-target empirical obligations
release-time forward obligations
measurement-dormant or revisit triggers
rejected/non-goal abstractions that must not become work
```

Do not summarize an enumerated owner list as “covered” without preserving item semantics.

### R27-E02 — Product Owner carry-forward

Map PO-001..PO-010 to current semantic owner, future implementation consumer(s), proof consumer(s), activation state and any remaining representation risk.

### R27-E03 — current realization census by destination family

For each implementation obligation, establish whether its target is already realized, partly realized, absent, stale or intentionally deferred across runtime/schema/catalog/template/instruction/tool/test/release surfaces.

### R27-E04 — dependency and ordering graph

Derive prerequisite ordering, especially across:

```text
semantic/persistent schema definition
-> generators/templates/loaders/validators
-> runtime producers/consumers
-> migration/compatibility machinery where required
-> deterministic tests
-> scenario/empirical acceptance
-> release-time gates
```

Do not infer one universal sequence where owner-local workstreams can proceed independently.

### R27-E05 — Version Impact routing

For every material workstream, identify whether the later implementation must run a Version Impact Gate for:

- Category-B module semantics;
- persistent/protocol schema/generation;
- campaign/storage/catalog/ruleset compatibility;
- migration/adoption support;
- package/release format.

Do not predeclare bumps not yet implied by a chosen authorized implementation.

### R27-E06 — negative architecture preservation

Preserve rejected global abstractions and negative laws so implementation planning cannot accidentally introduce them for convenience.

---

# 8. High-risk readiness probes

The later evidence/critic passes must attack these seams explicitly.

## R27-P01 — PO-003 + PO-009 Story-local T0/control realization

Question:

> Is the accepted HDM-side Story/export/control contract sufficiently bounded that exact persisted representation can be chosen during implementation planning, or does any unresolved choice materially alter persistent semantics/cross-component interface and therefore require a bounded architecture decision?

Mandatory preserved constraints include:

- SemanticEvent/history remains native historical owner;
- qualifying bounded T0 meaning must be Story-local recoverable for baseline Commentator;
- eligibility/control projection is derived from existing knowledge/disclosure/access owners;
- no second ACL/history authority;
- Commentator-local SQLite topology is downstream/internal, not Master HOT;
- baseline Commentator does not depend on native-only fallback for required T0/control;
- PO-003 zero-extra-serial latency law remains mandatory.

## R27-P02 — WP-25 deferred-vs-rejected normalization

Do not interpret every noun in a historical/deferred list as an implementation obligation.

Explicitly distinguish legitimate future realization such as a focus-scoped evaluator/adapters or proof work from rejected/non-required baselines such as global health authority, generic ACL/operation registry and universal retry engine. A persisted global failure registry is not implied merely because one historical/deferred section names schema/registry possibilities.

## R27-P03 — PO-010/WP-24 partition activation

Determine which future growth-bearing writers need an owner-valid bounded representation path in their implementation workstream while keeping concrete geometry implementation-selectable where the owner already delegates it.

Do not create a universal partition project solely because sizing bands exist.

## R27-P04 — migration/version dependency order

Use WP-20's explicit realization boundary. Exact migration-edge serialization, transform-module format and evaluator implementation are implementation-planning choices only within the fixed compatibility/currentness/authority laws. Any compatibility-bearing persisted shape change still triggers its own Version Impact/migration analysis.

## R27-P05 — proof-channel separation

Current CI/maintenance/unit success proves only the checks actually executed on the exact HEAD. It does not satisfy future MVP, Protocol-4, scenario or empirical acceptance obligations.

## R27-P06 — release-time gates

WP-23 pre-tag fresh-Project acceptance, immutable tag/publication, exact uploaded-asset verification, post-upload fresh-Project acceptance and release announcement are forward release obligations, not work to execute inside WP-27 or ordinary implementation planning.

## R27-P07 — dormant scale/host triggers

WP-24 measurements and R2.6/WP-25 host-risk calibration remain dormant or post-realization where their owners say so. Do not manufacture current optimization/telemetry/background-service work.

## R27-P08 — reverse conformance

A future plan must not leave current machine responsibilities ownerless, but current machine support may already satisfy part of a workstream. Distinguish:

```text
already realized and owner-conforming
needs extension
stale debt
verification-only support
historical/provenance-only artifact
```

---

# 9. Candidate implementation-workstream families — NOT YET A PLAN

Step 1 may use the following as discovery buckets only. They are **not** approved implementation workstreams until Step 2 evidence derives them item-wise:

```text
A. semantic/persistent record and schema realization
B. runtime deterministic execution / context / role / information consumers
C. persistence / HOT / publication / recovery / migration
D. Story / Chronicler / retrospective / Commentator export support
E. multiplayer / LIVE / collaboration / agency
F. bootstrap / campaign selection / character readiness / save-exit
G. failure / degradation / maintenance / diagnostics
H. bounded discovery / scale / partition / performance realization where activated
I. verification / scenario / empirical acceptance
J. packaging / version / legal / release-time readiness
```

The final graph may merge, split or discard these buckets based on actual owner/dependency evidence.

---

# 10. Explicit non-goals

WP-27 Step 1 does not:

- write an implementation plan;
- choose concrete code structure;
- choose concrete Story/Commentator cache SQL topology;
- choose one universal Story/index shard geometry;
- invent a global migration registry;
- invent a global failure/health/retry subsystem;
- execute benchmarks or Protocol 4;
- execute release/migration/gameplay;
- reopen WP-01..WP-26 wholesale;
- reactivate dormant evidence solely because it exists;
- edit the root README without separate Product Owner approval.

Known root README builder-path mismatch remains report-only under the editorial contract.

---

# 11. Step-1 critic attack surface

The mandatory Wide-Angle Critic must independently attack at least:

```text
missed WP-01..26 implementation/defer obligations
closed architecture mistaken for realized implementation
historical/deferred noun mistaken for active work
rejected architecture resurrected as implementation debt
Product Owner route aging
PO-003/009 duplicate history/access authority or extra serial latency
PO-009 persisted-interface ambiguity hidden as implementation detail
PO-010 sizing bands converted into universal partition work
WP-20 delegated representation choices unnecessarily reopening architecture
future Version Impact treated as already-selected migration/bump
current green CI treated as future acceptance proof
Protocol 4 / empirical work executed before real target
WP-23 release-time gates pulled into implementation work
machine->owner reverse-conformance gaps
dormant optimization triggers manufactured into work
missing dependency/migration/test-first ordering
WP-27 incorrectly treated as direct implementation-planning authorization
README opportunistic editing
```

---

# 12. Step-1 exit criteria

Step 1 is Senior-ready only when:

```text
SOURCE_MANIFEST_OPEN_WORLD: YES
TASK_BRIEF_OWNER_DERIVED: YES
MANDATORY_WIDE_ANGLE_CRITIC_COMPLETE: YES
ALL_BLOCKING_FRAMING_FINDINGS_REPAIRED: YES
ALL_SIGNIFICANT_FRAMING_FINDINGS_REPAIRED: YES
HUMAN_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
PRODUCT_OWNER_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
WP27_STEP2_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

Worker result after critic repair:

```text
SOURCE_MANIFEST_OPEN_WORLD: YES
TASK_BRIEF_OWNER_DERIVED: YES
MANDATORY_WIDE_ANGLE_CRITIC_COMPLETE: YES
STEP1_BLOCKING_FOUND: 0
STEP1_SIGNIFICANT_FOUND: 11
STEP1_MINOR_FOUND: 1
ALL_BLOCKING_FRAMING_FINDINGS_REPAIRED: YES
ALL_SIGNIFICANT_FRAMING_FINDINGS_REPAIRED: YES
ALL_MINOR_FRAMING_FINDINGS_REPAIRED: YES
HUMAN_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
PRODUCT_OWNER_DECISION_REQUIRED_FOR_STEP1_FRAMING: NO
WP27_STEP2_STARTED: NO
IMPLEMENTATION_PLANNING_STARTED: NO
```

The process is now stopped at:

```text
NEXT_GATE: MANDATORY INDEPENDENT WP-27 STEP-1 SENIOR REVIEW
```

A Senior `PASS / GO` is required before WP-27 Steps 2–8 become eligible for separate authorization under the current process.
