# R2.7 WP-26 Step 1 — Mandatory Whole-Project Task-Brief Critic

Status: **COMPLETE / FINDINGS REPAIRED AT WORKER LEVEL — PENDING MANDATORY INDEPENDENT SENIOR STEP-1 REVIEW**

Date: 2026-09-09

Scope: mandatory whole-project critic of the WP-26 Step-1 framing and open-world Source Manifest. This artifact is design provenance only. It does not authorize Step 2 and does not create a new documentation or supersession authority.

## 1. Critic mandate

The critic did not accept the draft Task Brief's named files as the evidence boundary. It independently reconstructed the task-specific dependency graph from current repository routing and then followed actual owners, amendments, current runtime consumers, schemas/tests/audits, Product Owner routes, and historical derivation where those could change the framing.

The critic specifically attacked:

```text
missed current owners
current-looking historical/status artifacts
hidden accepted semantics in design/history
duplicate authority
stale paths/topology/schema vocabulary
stale CORE activation/readiness semantics
stale tests/audit guards
filename-recency currentness inference
PO-009 native-fallback leakage
PO-009 eligibility oracle / ACL duplication
PO-010 10240 hard-cap leakage
accidental WP-18/WP-19/WP-24 reopen
README opportunistic editing
documentation-registry overengineering
implementation smuggled into WP-26
deferred obligations lost before WP-27
```

## 2. Independently reconstructed routes

### 2.1 Process / authority route

```text
AGENTS.md
    -> DEV/DESIGN_PROCESS.md
    -> DEV/ARCHITECTURE/DESIGN_PROCESS.md
    -> DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md
    -> DEV/CURRENT_PROGRESS.md
    -> DEV/PROJECT_MAP.md
    -> R2.7 whole-project owner clarification
```

Result: WP-26 is a whole-project reconciliation work package, but the current authorization is **Step 1 only**. The critic found no authority for Step 2, implementation planning, implementation, release/migration execution or gameplay/bootstrap.

### 2.2 Product Owner route

```text
DEV/PRODUCT_OWNER_INPUT.md
    -> accepted owner decision per applicable PO entry
    -> current semantic owners / amendments
    -> deferred future consumers
```

High-risk current additions:

```text
PO-009 -> Story/Commentator self-contained corpus decision
PO-010 -> mutable GitHub artifact sizing-band decision
```

The critic also inspected prior entries for route aging and future-realization carry-forward rather than assuming a closed architecture WP means every consumer is realized.

### 2.3 Story / Commentator route

```text
PO-009 owner decision
    -> Story producer/persistence/retrospective contract
    -> baseline Story projection source contracts
    -> Story persistence/growth/sharding owner decision
    -> WP-18 + final Senior recovery amendment
    -> WP-19 + PO-003 Actor historical-basis owner
    -> Step-4 truth/knowledge/role-context/Story owner
    -> R2.3 Context Runtime + WP-09
    -> ACCESS_CONTROL
    -> Story schema/test/runtime realization state
    -> derivative routing
```

The critic preserved:

```text
Master native owners remain gameplay canon
Story remains noncanonical to gameplay
physical possession != permission
no second ACL / world.knowledge / runtime.disclosure owner
```

It treated PO-009 as a targeted baseline Commentator projection/fallback supersession, not a wholesale Story/Actor/access redesign.

### 2.4 Mutable-artifact size route

```text
PO-010 owner decision
    -> September 4 size owner decision
    -> WP-24 LAW WP24-13
    -> Story growth/sharding owner decision
    -> persistence/storage/LIVE writers
    -> layout schemas/templates
    -> tests/audits/deferred realization
```

The critic separated:

```text
retained no-truncation / owner-valid partition / currentness law
    != superseded universal exact-byte rejection threshold
```

### 2.5 Runtime activation / readiness route

```text
PLAY_POLICY
    -> module headers
    -> CORE_INDEX
    -> CHARACTER_READINESS
    -> DIEGETIC_ONBOARDING
    -> WP-19
    -> NEW_CAMPAIGN_FAST_PATH
    -> RUNTIME / CAMPAIGN_SETUP / SAVE_CONTRACT
    -> INSTALL bootstrap / Project Instructions
    -> onboarding/bootstrap tests
    -> DEV maintenance audit
```

This route exposed a current cross-module contradiction that a documentation-only review would have missed.

### 2.6 Routing / provenance route

```text
CURRENT_PROGRESS
    -> PROJECT_MAP / CANONICAL_ARCHITECTURE_INDEX as locators
    -> actual owner
    -> accepted later amendment/decision
    -> current realization/evidence

historical design/status metadata
    -> provenance only unless explicitly adopted by a current owner
```

The critic independently checked the current tree's taxonomy. There is no current repository-root `docs/superpowers/` tree; current artifacts live under `DEV/docs/superpowers/{research,design,specs,plans}`.

## 3. Evidence findings

### F26-S1-01 — PO-009 baseline native-fallback leakage

Severity: **SIGNIFICANT**

Evidence:

- `DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` remains implementation-facing and still describes native WP-19 T0 escalation when Story is insufficient.
- `DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md` still permits required T0 Actor basis to remain represented through native-only navigation rather than retained Story-local values.
- PO-009 later requires `Story corpus + Commentator eligibility/control projection` to be the baseline Commentator's self-contained factual-support universe, including bounded WP-19-required T0 values.

Failure mechanism:

A future implementation agent could follow the older current-looking Story specs and build mandatory native Master fallback or live native eligibility reads into the baseline Commentator.

Required framing repair:

```text
classify PO-009 as targeted supersession/extension
preserve native Master owners as canon
preserve Story nonauthority
make baseline Commentator native fallback nonconforming for required T0/control basis
preserve machine/schema/test realization as future work
```

Disposition: **REPAIRED IN FINAL TASK BRIEF / UNDERLYING CORPUS CLEANUP REMAINS WP-26 WORK AFTER SENIOR GO**.

### F26-S1-02 — PO-010 exact 10240 hard-cap leakage

Severity: **SIGNIFICANT**

Evidence:

- the September 4 mutable-artifact owner decision states a universal `RUNTIME_MUTABLE_GITHUB_TEXT_FILE_MAX_BYTES = 10240` hard rejection rule;
- closed WP-24 LAW WP24-13 repeats final payload `> 10,240 bytes -> publication forbidden`;
- the Story growth/sharding owner consumes the same exact hard threshold;
- PO-010 later supersedes that exact-byte validity enum with sizing decision bands.

Failure mechanism:

A future implementation agent can still implement `>10240 => reject` as an HDM-wide law if it reads the older current-looking implementation-facing corpus without the September 9 decision.

Required framing repair:

```text
classify PO-010 as targeted threshold-policy supersession
keep WP-24 closed
retain no truncation / owner-valid split / currentness / bounded routing
remove exact 10240 validity authority from future current corpus
keep realization future until separately authorized
```

Disposition: **REPAIRED IN FINAL TASK BRIEF / UNDERLYING CORPUS CLEANUP REMAINS WP-26 WORK AFTER SENIOR GO**.

### F26-S1-03 — current provisional-play law conflicts with pre-live/true-live runtime and machine guards

Severity: **SIGNIFICANT**

Evidence:

Current accepted/runtime owner chain:

- `GAME/CORE/CHARACTER_READINESS.md`: READY_PC is not a gate on beginning gameplay; bounded provisional play may proceed when exact local dependencies for the proposed outcome are sufficient.
- repaired `GAME/CORE/DIEGETIC_ONBOARDING.md`: no hard pre-live/live cutover.
- WP-19 preserves provisional gameplay before full READY_PC closure.

Conflicting current surfaces:

- `GAME/CORE/RUNTIME.md` still frames initializing fiction as pre-live and normal mechanics-capable live play as post-READY_PC/PLAY_READY;
- `GAME/CORE/CAMPAIGN_SETUP.md` still stages a first true live scene / true live play after readiness;
- `GAME/CORE/SAVE_CONTRACT.md` still uses unfinished pre-live / legitimate normal live play distinctions;
- `GAME/CORE/CORE_INDEX.md` summarizes old pre-live/first true live language;
- `DEV/TESTS/DIEGETIC_ONBOARDING_CASES.md` and `BOOTSTRAP_STORAGE_REGRESSION_CASES.md` contain old true-live/pre-live assertions;
- `DEV/TOOLS/audit_engine.py` currently requires selected pre-live/post-PLAY_READY wording, so green maintenance audit can fossilize the superseded model.

Failure mechanism:

A later planner can conclude that the old staged lifecycle is current because it is represented in always-active runtime and machine guards even though the readiness/onboarding owners say otherwise.

Required framing repair:

```text
add runtime activation/readiness + audit/test guards to WP-26 graph
classify as stale current realization / machine-guard debt
repair later only where accepted law mechanically determines the correction
no new lifecycle/readiness subsystem
```

Disposition: **REPAIRED IN FINAL TASK BRIEF / UNDERLYING REALIZATION CLEANUP REMAINS WP-26 WORK AFTER SENIOR GO**.

### F26-S1-04 — derivative routing and current-looking status metadata can misstate currentness

Severity: **SIGNIFICANT**

Evidence:

- `DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` predate PO-009/010 and do not yet provide sufficiently direct targeted-supersession routes for both decisions;
- accepted/current specs such as WP-24 still retain historical worker status stating final Senior review pending while `CURRENT_PROGRESS.md` records WP-24 closed;
- older accepted specs retain transient target-development-branch metadata from earlier feature branches.

Failure mechanism:

A future agent can infer currentness from status/header/date/branch metadata or miss a later owner decision because the derivative index is lagging.

Required framing repair:

```text
CURRENT_PROGRESS is sole global cursor
filename/date/branch metadata is not semantic authority
Project Map/index are derivative and must be reconciled during WP-26
older owner remains current only for unaffected semantics after targeted supersession
```

Disposition: **REPAIRED IN FINAL TASK BRIEF / DERIVATIVE ROUTING CLEANUP REMAINS WP-26 WORK AFTER SENIOR GO**.

### F26-S1-05 — Product Owner route aging and deferred-consumer loss risk

Severity: **SIGNIFICANT**

Evidence:

- PO-006 still states that retained-ref operational-budget consumption is deferred until WP-24 opens, but WP-24 is now closed and its canonical result explicitly preserves retained/archived ref nonauthority and no-delete constraints;
- multiple PO entries intentionally keep runtime/tool/test/empirical consumers deferred beyond architecture closure.

Failure mechanism:

A later agent can either follow a stale future-stage route or wrongly treat a closed architecture WP as proof that deferred implementation consumers are already realized.

Required framing repair:

```text
add PO route lifecycle reconciliation to WP-26
carry all still-deferred PO-001..010 consumers item-wise into WP-27 readiness
closed architecture != realized implementation
```

Disposition: **REPAIRED IN FINAL TASK BRIEF / LEDGER ROUTE CLEANUP REMAINS WP-26 WORK AFTER SENIOR GO**.

### F26-S1-06 — accepted PO-009/010 semantics can be confused with realized machine support

Severity: **SIGNIFICANT**

Evidence:

- Step-1 current-tree inspection found no dedicated baseline Commentator schema by filename and the inspected Story tests do not prove the new T0/control projection;
- inspected current persistence/storage/LIVE runtime text does not establish a universal 10240 cutoff, but absence of that old cutoff also does not prove sizing-band writer/schema/test realization;
- PO-009/010 explicitly defer realization/version/test work to later authorized planning/execution.

Failure mechanism:

An agent could infer either `not implemented => requirement absent/fallback allowed` or `owner decision accepted => implementation already exists`.

Required framing repair:

```text
ACCEPTED CURRENT SEMANTICS
!= MACHINE REALIZATION
!= TEST REALIZATION
!= EMPIRICAL ACCEPTANCE
```

Disposition: **REPAIRED IN FINAL TASK BRIEF**.

### F26-S1-07 — initial documentation-only graph was insufficient for whole-project coverage

Severity: **SIGNIFICANT**

Evidence:

The runtime activation contradiction and stale maintenance-audit guard were discoverable only after following Project Map routes into actual GAME modules and DEV test/audit consumers. A docs/spec/index-only graph would have missed them.

Required framing repair:

- expand Source Manifest to schemas/templates/runtime/tests/audits as open-world families;
- preserve exact owner→consumer and consumer→owner checking;
- record that the Connector's code-search surface targets the repository default branch and therefore cannot prove absence on the active branch; use exact-ref/current-tree reads for authority-sensitive sweeps.

Disposition: **REPAIRED IN FINAL TASK BRIEF**.

### F26-S1-M1 — root README builder path mismatch

Severity: **MINOR**

Evidence:

```text
README: DEV/TOOLS/run_release_build
current AGENTS/tree entry point: DEV/TOOLS/run_release_build.py
```

Impact: public navigation/path mismatch only; no architecture-authority change.

Disposition:

```text
REPORT ONLY
DO NOT EDIT README WITHOUT EXPLICIT PRODUCT OWNER APPROVAL
```

## 4. Specific attack results

### 4.1 PO-009 native fallback attack

```text
QUESTION:
Can future baseline Commentator implementation still be derived as requiring
native Master fallback for WP-19 T0 or live native eligibility reads?

RESULT BEFORE WP-26 CLEANUP: YES

CURRENT CONTROLLING DECISION:
PO-009 targetedly supersedes that baseline representation/fallback requirement.
Native Master owners remain gameplay canon; Story remains noncanonical.
```

No second ACL/knowledge/disclosure owner is required. The Commentator control projection is a derived snapshot input with deterministic filtering before LLM materialization.

### 4.2 PO-009 oracle/ACL duplication attack

No accepted source requires a new Commentator authority. Step-4, ACCESS_CONTROL and PO-009 are compatible when kept layered:

```text
content candidate basis
    != eligibility/control basis

physical possession
    != permission

Commentator control projection
    != Master ACL owner
```

Finding: **NO NEW ARCHITECTURE DECISION REQUIRED**. Future realization must prove anti-oracle behavior.

### 4.3 PO-010 10240 attack

```text
QUESTION:
Can future implementation still derive unconditional >10240 => reject?

RESULT BEFORE WP-26 CLEANUP: YES

CURRENT CONTROLLING DECISION:
PO-010 sizing bands supersede the global exact-byte validity cutoff.
```

No WP-24 reopen is required. Only its exact threshold law is targetedly superseded.

### 4.4 Accidental closed-WP reopen attack

Result:

```text
WP-18 wholesale reopen: NO
WP-19 wholesale reopen: NO
Step-4 wholesale reopen: NO
R2.3 wholesale reopen: NO
WP-24 wholesale reopen: NO
WP-25 reopen: NO
```

The identified deltas are targeted supersession/routing or stale realization, not new semantic alternatives.

### 4.5 README editing attack

Result: root README is report-only under current authorization. The critic found no basis to override the editorial contract.

### 4.6 Documentation subsystem overengineering attack

Result: no global documentation registry/supersession database/metadata framework is needed. Existing owners + local supersession notices + derivative routers are sufficient to frame WP-26.

### 4.7 Implementation-smuggling attack

Result: the Step-1 package records stale runtime/test/audit surfaces but does not repair those surfaces. Such cleanup belongs to later WP-26 Steps after Senior GO unless a later gate establishes a tiny routing-only correction as necessary. No implementation plan or runtime feature is produced.

## 5. Finding summary

```text
STEP1_CRITIC_BLOCKING_FOUND: 0
STEP1_CRITIC_SIGNIFICANT_FOUND: 7
STEP1_CRITIC_MINOR_FOUND: 1

UNRESOLVED_BLOCKING_AFTER_WORKER_REPAIR: 0
UNRESOLVED_SIGNIFICANT_AFTER_WORKER_REPAIR: 0
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
WP26_STEP2_AUTHORIZED: NO
```

Important distinction:

```text
UNRESOLVED STEP-1 FRAMING FINDING = 0

BUT

PROVEN WP-26 CORPUS/REALIZATION CLEANUP OBLIGATIONS
    = D26-01..D26-07 in the repaired Task Brief
    = intentionally pending later authorized Steps 2–8
```

The critic does not mislabel unexecuted WP-26 cleanup as a completed corpus reconciliation.

## 6. Repair verification against the final Task Brief

The final `2026-09-09-r2-7-WP-26-task-brief-source-manifest.md` now includes:

- exact WP-26 problem/in-scope/out-of-scope;
- open-world Source Manifest with source-role classes;
- process/routing/Story/size/activation/WP-27 dependency subgraphs;
- explicit PO-009 current precedence and attack result;
- explicit PO-010 current precedence and attack result;
- current CORE/readiness/onboarding + machine-guard contradiction;
- current-looking status/transient metadata risk;
- PO route aging and deferred-realization preservation;
- README report-only boundary and exact known mismatch;
- architecture↔machine bidirectional consistency requirement;
- repair-now/retain/defer criteria;
- anti-overengineering constraints;
- itemized WP-27 carry-forward obligations;
- Version Impact expectation;
- exact Step-1 exit criteria and Senior stop.

No remaining Step-1 issue requires Product Owner judgment.

## 7. Version Impact critic check

The Step-1 repair package changes only design-process/current-progress/routing bookkeeping artifacts. It does not alter a version-bearing GAME semantic module, persistent/protocol schema, catalog/ruleset generation, package format, migration law or engine identity.

Expected final gate remains:

```text
VERSION_IMPACT: NONE
ENGINE_VERSION_BUMP_REQUIRED: NO
MODULE_VERSION_BUMP_REQUIRED: NO
SCHEMA/GENERATION_BUMP_REQUIRED: NO
```

This must be confirmed against the actual published changed-file set.

## 8. Mandatory stop

```text
STEP1_CRITIC: COMPLETE
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-26 Step-1 Senior review
```

Do not begin Step 2.