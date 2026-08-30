# R2.7 — Whole-Project Final Architecture & Machine-Realization Audit — Task Brief v2

Status: **ACTIVE TASK BRIEF — R2.7 IN PROGRESS**

Date: 2026-08-24

Supersedes:

- `2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md`

Owner scope clarification:

- `2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`

Scope-discovery inventory:

- `../design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

No broad implementation is authorized by this brief.

---

# 1. Purpose

R2.7 is the **final architecture stage before implementation planning**.

Its job is to establish that the complete accepted HDM architecture — not merely the Round-2 delta — has one coherent, implementable, testable machine realization with no unresolved owner, persistence, currentness, recovery, bootstrap, migration, instruction or release contradiction.

The governing question is:

> **Can implementation planning now be derived from the whole accepted HDM architecture and the current repository without first making another material architecture decision?**

R2.7 closes only when the answer is **yes**.

---

# 2. Coverage boundary

R2.7 SHALL cover the complete architecture/runtime dependency graph:

```text
ROUND 1 / STEPS 1-5
    catalog/class authority
    mechanical state
    deterministic execution
    truth/knowledge/roles/context/Story
    durability/recovery/live/chronology/message/disclosure/cleanup

+ LATER AMENDMENTS / OWNER DECISIONS
    including single-context role containment and other superseding decisions

+ ROUND 2 / R2.1-R2.6
    continuity
    Actor cognition/relationships
    Context Runtime
    single-context execution/Chronicler
    multiplayer collaboration/Dramaturg planning
    MVP host assurance

+ CURRENT MACHINE/PRODUCT SURFACES
    GAME runtime
    persistent schemas/templates
    DEV catalogs/schemas
    install/bootstrap/update/migrations
    persistence/recovery/live/access
    rules/domain modules
    tests/audit/CI/release/version/legal
```

The 82 Round-2 DIAMOND/STRONG items remain a mandatory Round-2 completeness sub-ledger. They do not define the outer audit scope.

---

# 3. Process / evidence standard

R2.7 is a high-risk whole-system deep-work task and must follow:

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

Before any final coverage/canonicalization claim, R2.7 must maintain an auditable Source Manifest and structured evidence accounting.

Owning sources beat derivative indexes. `DEV/PROJECT_MAP.md` and `CANONICAL_ARCHITECTURE_INDEX.md` are routing aids only.

R2.7 must not ask the owner to proofread the corpus for missing dependencies. Source discovery/completeness is agent-owned.

---

# 4. Required bidirectional proof

## 4.1 Architecture -> machine

For **every accepted material semantic responsibility**, identify as applicable:

```text
semantic owner / authority
accepted source(s)
shipped CORE owner(s)
persistent native representation
exact root/path
stable identity/version/generation policy
flat vs deterministic sharded layout
index/discovery/currentness route
HOT/SQLite realization
transient typed interface/result
publication/durability/recovery behavior
Project Instructions / host instruction responsibility
DEV catalog/schema obligation
template/bootstrap/migration implication
deterministic tests
scenario/adversarial tests
production-like MVP acceptance owner
```

Where no representation belongs, record it explicitly:

```text
NO DURABLE RECORD
NO SQLITE OWNER
NO INDEX
INSTRUCTION ONLY
DERIVED ONLY
EPHEMERAL ONLY
POST-MVP EVALUATION ONLY
```

## 4.2 Machine -> architecture

For **every material current repository machine/runtime responsibility**, identify:

```text
accepted semantic owner
or
DERIVED / IMPLEMENTATION-ONLY / HISTORICAL / STALE / DEBT / OUT-OF-SCOPE
```

This reverse audit applies to:

- GAME/CORE behavior/contracts;
- GAME persistent schemas/templates;
- DEV catalogs/schemas;
- bootstrap/update/migration tooling;
- persistence/recovery/access/live structures;
- tests/audit/release/CI responsibilities.

Existing scaffold state gets no presumption of correctness merely because it predates Round 2.

---

# 5. Task-specific Source Manifest — required families

The detailed manifest will be built during audit execution, but it must cover at least these source families where implicated.

## 5.1 Governance and sequencing

- `AGENTS.md`
- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/PROJECT_MAP.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 5.2 Complete accepted architecture

- owning Steps 1-5 specs, model contracts, owner decisions and amendments;
- Step-5.14 integrated closure/recovery-concurrency assurance;
- Step-4 single-context canonical amendment;
- Round-1 closure/Round-2 rebaseline decision;
- all R2.1-R2.6 owner decisions, canonical specs and resolution gates;
- current durable architecture contracts under `DEV/ARCHITECTURE/`.

## 5.3 Shipped GAME runtime

Inspect all implicated current `GAME/CORE/*.md`, not only R2-specific modules.

At minimum the dependency graph includes:

- always-active guards/routing;
- bootstrap/campaign lifecycle;
- gameplay/domain modules;
- reasoning/information/NPC/prep/narration;
- persistence/storage/save/integrity/session;
- multiplayer/live/chronology/processes;
- sources/rules routing.

## 5.4 Persistent runtime representation

- all implicated `GAME/SCHEMA/*.schema.yaml`;
- complete `GAME/CAMPAIGN/` template tree;
- `GAME/TOOLS/init_campaign.py`;
- `GAME/MIGRATIONS/` contract;
- `GAME/TEMPLATE/` storage template;
- runtime version/provenance fields.

## 5.5 DEV machine contracts

- current `DEV/CATALOG/*.json`;
- all implicated `DEV/SCHEMAS/*.schema.json`;
- catalog/entity/activity/rule-element/Actor/Asset contracts;
- identifier/mechanical-surface policies;
- access/branch/storage-related architecture contracts.

## 5.6 Install/update/release/verification

- `GAME/INSTALL/*` including Project Instructions;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `DEV/RELEASE/*`;
- `DEV/TOOLS/run_maintenance_audit`, `audit_engine.py`, release builder;
- `.github/workflows/validate.yml`, `release-runtime.yml`;
- relevant `DEV/TESTS/test_*.py` and `*_CASES.md`;
- root/runtime version/legal parity obligations.

## 5.7 Research/evaluation evidence

Use only where it still constrains current architecture/test mapping:

- Protocols 1-3 promoted behavioral conclusions;
- R2.6 Protocol-4-derived post-MVP acceptance inventory;
- Round-2 DIAMOND/STRONG disposition ledger and later S14/S53/D15 changes;
- any relevant private Lab evidence only through sanitized independent conclusions.

Research is evidence, not architecture authority.

---

# 6. Required audit domains

The minimum domain/question inventory is defined by:

- `2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`

Its 27 domains (`WP-01` through `WP-27`) are mandatory starting coverage:

1. product/deployment/repository boundary;
2. global authority / duplicate-owner audit;
3. catalog/class/capability completeness;
4. Actor/Asset/mechanical-state model;
5. deterministic execution pipeline;
6. rules/adjudication/domain-module compatibility;
7. truth/knowledge/disclosure/message evidence;
8. LLM role/context/instruction architecture;
9. context loading/retrieval/resource bounds;
10. durable campaign record-family completeness;
11. storage topology/identity/indexing;
12. HOT/SQLite/transaction realization;
13. durability/SAVE/publication;
14. recovery/checkpoints/session/repair;
15. temporal owners/processes/chronology;
16. multiplayer/access/live state;
17. async collaboration/agency-safe progression;
18. Story/continuity/Dramaturg planning;
19. bootstrap/campaign creation;
20. engine update/schema evolution/migration;
21. diagnostics/observability/cleanup;
22. verification/test/evaluation completeness;
23. release/package/version/legal readiness;
24. performance/scale/operational budget;
25. error/degradation/failure semantics;
26. documentation/routing/supersession consistency;
27. implementation-planning readiness.

This list is a minimum. If Source Manifest work discovers another material owner/consumer dependency, it must be added rather than excluded because it was not known when the brief was written.

---

# 7. Whole-project physical realization requirements

## 7.1 Persistent record/root matrix

Resolve exact root/record/schema/layout for **all** material persistent owners across the project.

Do not limit sharding analysis to Round-2 additions. Review pre-existing world/event/session/checkpoint/current/scene and mechanical-owner families as well.

For every high-cardinality family define:

- stable semantic ID;
- deterministic routing-only shard rule;
- physical root;
- monolithic index path/interaction;
- ordinary exact lookup route;
- rebuild/audit behavior;
- migration/bootstrap implication.

Current `*_INDEX.yaml` remain monolithic unless the accepted measured revisit trigger has fired.

## 7.2 HOT/SQLite

Map the full accepted current working state, not only R2.3/R2.5 additions.

For each table/structure class identify:

- represented semantic owner;
- owner-state working copy vs derived cache/index/projection;
- hydration/currentness basis;
- dirty/publication role;
- transaction/CAS role;
- recovery/loss behavior;
- durable materialization target;
- rebuildability.

SQLite format creates no semantic authority.

## 7.3 Typed runtime interfaces

Map all required deterministic execution/context/currentness/publication interfaces, including Steps 2-5 and Round 2.

Do not persist hidden chain-of-thought or require large model-generated transport JSON.

---

# 8. Runtime CORE / instruction conformance audit

R2.7 must audit the current shipped CORE set against accepted architecture in both directions.

Required questions include:

- Does each CORE module use the current semantic owners?
- Can any domain module bypass deterministic mechanics/currentness/disclosure gates?
- Are obsolete scaffold concepts still stated as current law?
- Are activation headers and `CORE_INDEX` consistent with actual responsibility?
- Are `PLAY_POLICY`, rules/source routing and Project Instructions consistent with the supported host/deployment profile?
- Is the R2.6 behavioral rule owned once and correctly applied in Actor/Narrator/prep/information consumers?
- Are `gh`, remote native Git, direct private API/token workarounds and alternate transport probing absolutely forbidden wherever runtime repository behavior is described?

Exact runtime edits occur during implementation, after R2.7 maps the changes.

---

# 9. Bootstrap / migration / release conformance audit

Before implementation planning, R2.7 must know how the final architecture reaches a real user/campaign.

Map:

```text
runtime package installation
-> Project Instructions / package discovery
-> existing/new campaign selection
-> campaign scaffold/materialization
-> schema/version validation
-> gameplay readiness
-> engine update
-> persistent migration when required
-> release packaging / compatibility verification
```

The audit must identify every final architecture change that requires:

- new template roots/files;
- schema evolution;
- identifier/version changes;
- migration of existing campaigns;
- release/checklist/CI updates;
- compatibility restriction.

---

# 10. Verification and MVP-evaluation mapping

Every material accepted law from **all architecture rounds** must map to the appropriate verification class:

```text
unit / schema / catalog contract
integration / persistence / recovery
scenario / adversarial
LLM production-like MVP evaluation
manual UI/deployment check where unavoidable
```

Existing tests must be reverse-audited for stale assumptions.

R2.6 Protocol-4-derived integrated LLM scenarios remain post-implementation MVP acceptance obligations; R2.7 assigns durable test/evaluation ownership and IDs but does not build a parallel MVP test harness.

---

# 11. Whole-project adversarial composition review

Closure review must challenge at least:

- duplicate authority across all storage/derived/instruction layers;
- schema/model/runtime disagreement;
- LLM/narration bypass of deterministic execution;
- retry/recovery/presentation replay of accepted mechanics/RNG;
- stale/cached/session/checkpoint state outranking current owners;
- Git/host ordering becoming fictional chronology;
- player disclosure vs PC knowledge confusion;
- live/campaign authority overlap;
- absent-player agency invention;
- Story/planning becoming canon/plot authority;
- hidden campaign-wide scans or unsafe high-cardinality layouts;
- bootstrap unable to construct required owners;
- migrations unable to preserve currentness/identity/history;
- runtime dependency on DEV-only artifacts;
- unsupported host/tool fallback paths;
- debug/audit/approval surfaces leaking authority or secrets;
- cleanup deleting still-required evidence/state;
- stale tests/docs directing implementation toward superseded architecture.

Round-2-only composition and all 82 DIAMOND/STRONG dispositions are rechecked inside this broader review.

---

# 12. Required R2.7 artifacts

R2.7 must produce enough inspectable evidence to support a final whole-project closure claim. At minimum:

1. whole-project Source Manifest / coverage ledger;
2. global semantic-owner matrix;
3. architecture -> machine realization matrix;
4. machine -> architecture reverse-conformance ledger;
5. persistent record/root/index/sharding matrix;
6. HOT/SQLite realization matrix;
7. instruction/CORE/Project-Instructions map;
8. bootstrap/migration/version/update matrix;
9. verification/evaluation/release-readiness matrix;
10. gap/conflict/stale/debt ledger;
11. whole-project adversarial composition review;
12. Decision Brief(s) only for genuine residual human trade-offs;
13. canonical final architecture/machine-realization specification;
14. implementation-planning entry resolution gate.

Artifacts may be combined where doing so preserves auditability; document count is not a goal.

---

# 13. Human decision gate

Do not escalate replaceable implementation detail.

Escalate only when the audit leaves multiple materially different viable choices affecting product semantics, authority, persistent model, hard-to-reverse compatibility/migration, major quality trade-offs or accepted risk.

For every such gate provide:

```text
established facts
exact conflict/delta
credible alternatives
consequences
recommendation
uncertainty
exact owner decision required
```

---

# 14. Exit criteria

R2.7 closes only when all are true:

1. whole-project Source Manifest is complete enough for an implementation-planning readiness claim;
2. every material accepted Round-1 and Round-2 semantic responsibility has a machine/instruction/test destination or explicit no-representation disposition;
3. every material current GAME/DEV machine/runtime responsibility has an accepted owner or explicit stale/debt/derived/implementation-only disposition;
4. no duplicate semantic owner remains;
5. current catalog/classes/mechanical state and deterministic execution are fully mapped to machine contracts/runtime/tests;
6. truth/knowledge/disclosure/role/context/Story/planning architecture is fully mapped without authority duplication;
7. all material persistent record families have exact roots/schemas/layout/index/currentness policy;
8. all required high-cardinality families have deterministic sharding/routing that composes with monolithic indexes;
9. HOT/SQLite current/cache/dirty/publication/recovery responsibilities are fully mapped;
10. durability/publication/live/recovery/session/checkpoint/cleanup composition is unambiguous;
11. multiplayer access/live/collaboration/agency/Dramaturg planning realization is fully mapped;
12. temporal/process/chronology realization is fully mapped without implicit host/Git order;
13. CORE/domain/rules/Project-Instructions conformance gaps are identified with exact implementation destinations;
14. bootstrap/new-campaign/update/migration paths can construct/upgrade every required persistent owner;
15. tests/evaluation/CI/audit obligations cover all material laws and stale tests are identified;
16. release/package/version/legal implications are explicit;
17. operational scale/degradation/failure paths have architecture-level dispositions;
18. all Round-2 DIAMOND/STRONG items plus later activation changes remain correctly dispositioned at machine/test level;
19. stale derivative/status/documentation references that could misroute implementation are identified;
20. whole-project adversarial review has zero unresolved architecture blockers;
21. all genuine owner trade-offs are resolved;
22. every remaining issue is classified as implementation detail, implementation task, safe debt, post-MVP evaluation, dormant trigger or out-of-scope item;
23. no unresolved question remains that could materially change implementation topology/data model/interfaces/authority/migration strategy;
24. broad implementation has not started before this gate closes.

Only after this gate may implementation planning begin.

---

# 15. Immediate continuation

```text
construct whole-project Source Manifest / coverage ledger
    -> global semantic-owner inventory
    -> bidirectional architecture<->machine conformance pass
    -> physical persistence/HOT/index mapping
    -> CORE/bootstrap/migration/test/release conformance
    -> whole-project adversarial review
    -> owner gates only where genuine
    -> canonical final architecture
    -> implementation-planning entry gate
```

Microsteps are derived just in time from the dependency graph; this brief intentionally does not pre-script every audit subtask.

Broad implementation remains **BLOCKED**.
