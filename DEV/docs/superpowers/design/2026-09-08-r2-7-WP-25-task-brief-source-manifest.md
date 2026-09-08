# R2.7 WP-25 Step 1 — Error / Degradation / Failure Semantics — Architecture Task Brief + Source Manifest

Status: **STEP 1 COMPLETE — POST-CRITIC REPAIRED / PENDING MANDATORY INDEPENDENT SENIOR STEP-1 REVIEW**

Date: 2026-09-08

This artifact is design-process provenance for **R2.7 WP-25 Step 1 only**. It is not a canonical WP-25 specification, does not authorize Step 2, and does not change native failure, authority, persistence, recovery, compatibility, multiplayer, disclosure, Story or verification owners.

## 1. Authorization and hard stop

Authorized work is limited to:

```text
WP-25 Step 1
    -> open-world Source Manifest
    -> Architecture Task Brief
    -> mandatory whole-project Task-Brief critic
    -> investigation of critic-discovered owners/dependencies
    -> mechanical repair of resolvable BLOCKING/SIGNIFICANT framing gaps
    -> publication/read-back/verification
    -> STOP for independent Senior Step-1 review
```

Not authorized:

```text
Step 2 or Steps 2–8
implementation planning
substantive implementation
runtime/schema/test realization
release or migration execution
gameplay/campaign bootstrap
```

The next process boundary after this package is the mandatory independent WP-25 Step-1 Senior review. This worker does not self-declare Senior PASS.

## 2. Problem statement

HDM already has mature native outcome semantics distributed across domain owners: recovery, Context Runtime, publication/currentness, compatibility/migration, LIVE/multiplayer, collaboration/agency, integrity, Story, diagnostics, package/runtime selection and presentation/disclosure. WP-25 must later determine how material failures compose across those owners without replacing them with a universal error authority.

The architecture problem is therefore broader than an error enum. Later Steps 2–8 must be able to classify a material failure condition with enough independent dimensions to answer, at minimum:

```text
native failure / epistemic outcome
truthful frontier
effective severity
gameplay impact
affected scope / blast radius
risk if ignored
legal continuation
temporal tolerance / semantic fence
bounded recovery
retry / idempotency semantics
prohibited fallback
user-visible disposition
verification / empirical-acceptance obligation
```

The framing must also survive cascading failures: failure during recovery or repair; ambiguity after partial success; retry exhaustion; authority/currentness movement while diagnosing or recovering; local adoption failure after remote semantic acceptance; failure after accepted mechanics/RNG; and failure between accepted state and player-visible presentation.

## 3. Product Owner / accepted direction input

Mandatory Product Owner inputs are distinct from native semantic owners:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` — accepted Product Owner / architecture-direction input for WP-25; binding direction but explicitly not WP-25 closure.
- `DEV/PRODUCT_OWNER_INPUT.md` — full `PO-008`, including its host-capacity/durability-risk amendment and routing state.

The accepted direction entering WP-25 is:

```text
OWNER-LOCAL NATIVE OUTCOMES
+ EPHEMERAL CROSS-OWNER FAILURE DISPOSITION
+ SCOPE-AWARE CONTINUATION
+ RISK-TRAJECTORY-AWARE DURABILITY PROTECTION
```

Required separation:

```text
FAILURE CAUSE
!= EFFECTIVE SEVERITY
!= GAMEPLAY DISPOSITION
!= RETRY POLICY
```

Required starting effective-severity vocabulary:

```text
S0 NOTICE
S1 DEGRADED
S2 GUARDED
S3 QUARANTINED
S4 CRITICAL
```

Severity is context-derived. `UNSUPPORTED` is an orthogonal capability/deployment/compatibility disposition, not shorthand for the highest severity.

The design must separately preserve gameplay impact, affected scope/blast radius, risk if ignored, semantic temporal tolerance, truthful frontier, recovery/retry semantics, user visibility and proof obligations.

## 4. Goals

1. Establish the complete WP-25 problem horizon without prematurely choosing a final data structure or master error taxonomy.
2. Preserve all current native outcome owners and define the questions needed to compose them later.
3. Make severity, gameplay disposition, retry policy, scope, risk, temporal tolerance, truthful frontier and user visibility independently reasonable dimensions.
4. Cover local and cascading failure chains, including failures in recovery/repair and after partial or remote success.
5. Preserve authority/currentness, agency, information/disclosure and accepted-mechanics/RNG invariants through failure handling.
6. Frame the Product Owner durability-risk requirement as composition with current Step-5.5 / WP-13 / host-assurance / WP-24 owners, not as restoration of a timer-based product law.
7. Distinguish accepted semantic-owner conflicts from stale/incomplete GAME/schema/test realization.
8. Preserve proof-class separation so architecture cannot claim empirical host behavior that requires later realized-target evidence.
9. Leave Steps 2–8 with a finite, auditable owner graph and falsifiable research questions.

## 5. Non-goals

WP-25 Step 1 does not:

- choose the final WP-25 architecture or canonical schema;
- create a persisted master error/failure registry;
- normalize every native owner outcome into one enum;
- define exact host-capacity, token, message, context or time thresholds;
- create a generic timeout, lease, heartbeat, worker, queue or scheduler;
- define a universal retry count or duration;
- rewrite current persistence/recovery/LIVE/migration/Story/disclosure owners;
- repair known stale runtime/tests;
- add telemetry, diagnostics schemas or runtime code;
- claim empirical ChatGPT/host capacity, reliability, latency or emergency-preservation success probability;
- perform migration/release/runtime execution.

## 6. Existing architecture invariants carried into WP-25

The following are constraints, not open questions:

1. Native semantic owners remain authoritative for their own outcomes and state transitions.
2. LLM prose, chat/model memory, Story, checkpoint, planning, cache, index and diagnostics are not campaign authority.
3. Accepted IDs are stable; recovery does not invent replacement identities.
4. Accepted mechanics/RNG and voluntary player actions are not replayed, rerolled or rewritten merely to recover presentation, persistence or transport.
5. Physical data visibility does not promote information eligibility or disclosure authority.
6. Publication/currentness uses pinned authority and the supported non-force exact-source fence; ambiguous authority-changing publication is never blind-retried.
7. Force push/ref rewind and HDM branch/ref deletion are prohibited.
8. Git order, arrival order, timestamps or last-writer-wins do not manufacture fictional authority/chronology.
9. Recovery begins from actual current native authority and bounded required closure.
10. Normal waiting for an authorized contribution is not automatically a failure; required missing contribution may freeze only the dependent scope under its owner.
11. Context `UNSATISFIABLE` must not be converted to guessed required evidence.
12. Unsupported/indeterminate compatibility fails closed; version order/ancestry do not manufacture compatibility or migration paths.
13. Story failure/lag cannot replace native canon and ordinarily cannot block or roll back gameplay/recovery readiness.
14. Ordinary operations remain bounded; no WORLD/history/all-ref/all-LIVE scans are introduced as recovery shortcuts.
15. No background worker/heartbeat correctness dependency is introduced for the supported product.
16. Architecture coverage, machine realization, verification realization and empirical acceptance are separate proof classes.

## 7. Durability / host-capacity framing

### 7.1 Correctness HARD versus operability/loss-protection fence

WP-25 must preserve two different reasons to require preservation:

```text
CORRECTNESS HARD
    durability is a mandatory postcondition of a named semantic edge

OPERABILITY / LOSS-PROTECTION FENCE
    coherent HOT/SOFT state is still semantically correct,
    but allowing materially more single-copy unpublished exposure has become
    an unacceptable product risk
```

The second category does not retroactively make coherent HOT corrupt and does not redefine all SOFT state as HARD.

### 7.2 Risk trajectory

The Product Owner direction requires at least the conceptual states:

```text
NORMAL
ELEVATED
DANGER
```

Exact machine thresholds are intentionally open pending applicable evidence. Approximate chat/context/message/token/capacity signals may later be advisory evidence for proactive preservation but cannot become truth/currentness/authorization authority or a fictional exact remaining-context contract.

At `DANGER`, later architecture must be able to guard before further materially state-growing gameplay when preservation/repair is required, without declaring the existing coherent HOT frontier corrupt solely because capacity risk is high.

### 7.3 Supersession discipline

The historical `GAME/CORE/DURABILITY_GUARD.md` / `SESSION.md` one-hour dirty ceiling and `DEV/TESTS/test_hourly_durability_contract.py` are current realization evidence, not current product-law authority where they conflict with Step-5.5/WP-13 and the accepted WP-25 direction. Their presence is realization debt to route later; it is not a reason to reopen accepted Step-5.5/WP-13 semantics in Step 1.

## 8. Required failure horizon for later Steps 2–8

The source/critic route must support at least these families without assuming they are the final taxonomy:

1. host capability unavailable or degraded;
2. stale/currentness/moved authority;
3. authentication, identity, eligibility or control failure;
4. malformed, contradictory, dangling or integrity-defective native state;
5. Context assembly degraded/`UNSATISFIABLE`;
6. publication rejection, ambiguous outcome or partial success;
7. recovery source absence/incompatibility/retry exhaustion;
8. LIVE ownership/currentness/conflict ambiguity;
9. collaboration generation/currentness or required-contribution failure, while distinguishing ordinary waiting;
10. migration/update compatibility unsupported/indeterminate/path failure;
11. Story/planning/derived-state lag, stale basis, conflict or optional unavailability;
12. presentation/render/disclosure interruption or re-presentation uncertainty after accepted semantics;
13. diagnostics/cleanup proof unavailable or indeterminate;
14. runtime-package/instruction-basis loss, mismatch or mixed-runtime risk;
15. compound/cascading failure combining several of the above.

For every material condition, later synthesis must ask what remains truthful and legally continuable rather than merely assign an error label.

## 9. Cascading-failure attack routes

Steps 2–8 must explicitly attack at least these compositions:

- recovery attempt fails while native currentness continues moving;
- repair succeeds locally but publication result is indeterminate;
- publication succeeded remotely but local adoption/rebind failed;
- retry reaches its owner-bounded exhaustion condition;
- authorization or PLAYER/LIVE ownership changes while recovery/diagnostics is in progress;
- migration/update prepares successfully but current authority moves before publication;
- migration is accepted remotely but local target-runtime rebind/rehydration fails;
- accepted mechanics/RNG exists but persistence/presentation fails afterward;
- accepted fictional/state transition exists but player-visible rendering is interrupted;
- disclosure acceptance/evidence differs from what was physically rendered;
- Story/planning regeneration fails while native sources remain usable;
- cleanup/retirement evidence becomes stale while assessment runs;
- host capacity moves from operable to dangerous while unpublished established state grows;
- instruction-context loss/mixed package basis is discovered while a gameplay continuation is pending.

## 10. Quality attributes that can distinguish later alternatives

WP-25 later design must compare alternatives against:

- semantic correctness and truthful frontier preservation;
- authority/currentness safety;
- bounded recovery and retry safety;
- agency and disclosure safety;
- loss containment for established unpublished state;
- graceful local degradation rather than unnecessary campaign-global blocking;
- deterministic/idempotent recovery where the owner permits it;
- debuggability and user-actionability without leaking secrets/internal noise;
- bounded ordinary-turn cost and absence of unbounded scans/background correctness work;
- compatibility with single-context supported-host constraints;
- reversibility and implementation complexity;
- verifiability and empirical testability.

No unowned numerical latency/capacity target is introduced by this brief.

## 11. Open-world Source Manifest

Inspection status vocabulary:

- `FULL` — source inspected through its current substantive contract relevant to WP-25.
- `TARGETED` — current relevant owner/consumer portions inspected; full unrelated scope not required for Step-1 framing.
- `STRUCTURAL` — family/tree inspected to establish consumer route; specific members are listed when read.

### 11.1 Process / current-stage / routing authority

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `AGENTS.md` | repository/process authority | bootstrap, Connector-only transport, taxonomy, branch/write/version/checkpoint rules | FULL |
| `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` | runtime overlay | remote publication/currentness/verification mechanics | FULL |
| `DEV/DESIGN_PROCESS.md` | canonical development design process | Step-1 Source Manifest, framing gate, whole-project critic, evidence completeness | FULL |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | whole-project critic and mandatory Senior Step-1 stop | FULL |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md` | PO-input process owner | PO evidence vs semantic owner distinction and routing | FULL |
| `DEV/PROJECT_MAP.md` | derivative locator | open-world dependency reconstruction | FULL |
| `DEV/CURRENT_PROGRESS.md` | global current-progress authority | WP-25 Step-1-only authorization and Senior gate | FULL |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | sequencing/scope authority | R2.7 sequence and WP-25 placement | TARGETED |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | derivative semantic locator | current invariant and owner routing, never semantic override | TARGETED |

### 11.2 Mandatory Product Owner direction

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md` | Product Owner / accepted architecture-direction input | required multidimensional failure direction, severity vocabulary, durability-risk intent, negative requirements, proof discipline | FULL |
| `DEV/PRODUCT_OWNER_INPUT.md` — `PO-008` | Product Owner intent/routing evidence | original error/degradation request plus host-capacity amendment and activation routing | FULL ENTRY |

These inputs are binding requirements but do not replace native owners and do not constitute a completed WP-25 architecture.

### 11.3 Durability, publication, recovery and integrity owners

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md` | canonical owner | `ESTABLISHED != DURABLE`, SOFT/HARD semantics, named hard edges; no universal hourly law | FULL |
| `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md` | canonical owner | publication tri-state, currentness, ambiguity, no blind retry, current durability projection | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` | canonical owner | `READY/RETRY/BLOCKED`, bounded recovery, current-authority-first, movement during repair | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md` | canonical amendment | supported ref monotonicity, parent+non-force fence, create-if-absent, ambiguity lineage/current closure | FULL |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | canonical integration owner | compound failure/recovery/concurrency constraints and accepted limitations | FULL |
| `GAME/CORE/SAVE_CONTRACT.md` | runtime consumer/projection | explicit save completeness, no fake materialization, success/user-visible semantics | FULL |
| `GAME/CORE/PERSISTENCE.md` | runtime consumer/projection | current publication/write realization and possible stale local wording | FULL |
| `GAME/CORE/INTEGRITY.md` | runtime consumer/projection | integrity-suspect failure and bounded repair behavior | FULL |
| `GAME/CORE/RUNTIME.md` | runtime consumer/projection | fast-path, recovery/presentation runtime integration | FULL |
| `GAME/CORE/DURABILITY_GUARD.md` | stale runtime realization evidence | one-hour law conflicts with superseding current durability direction | FULL |
| `GAME/CORE/SESSION.md` | stale/current runtime realization evidence | one-hour dependent session behavior plus continuation/recovery consumer | FULL |

### 11.4 Context, instruction basis and supported-host owners

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | canonical owner | `ASSEMBLED/ASSEMBLED_DEGRADED/UNSATISFIABLE`; no guessing required evidence | FULL |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | canonical owner | single-context logical-role containment and no hidden correctness worker | FULL |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | canonical owner | capability fail-closed/degradation boundary; empirical host assurance separation | FULL |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md` | canonical realization owner | exact-package CORE/RULES cache, package-switch invalidation, instruction-context loss rehydration | FULL |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | canonical realization owner | bounded Context realization/resource behavior and failure consumers | FULL |

### 11.5 Authority, LIVE, collaboration, chronology and agency

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | current architecture owner | creator/PLAYER authorization and fail-closed eligibility | FULL |
| `DEV/ARCHITECTURE/BRANCH_MODEL.md` | derivative projection | branch/storage/runtime routing; not semantic override | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md` | Product Owner canonical decision | unresolvable creator login fails closed; no ID substitution/silent transfer | FULL |
| `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md` | Product Owner canonical decision | absolute branch/ref deletion prohibition | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md` | canonical owner | selected native LIVE authority/currentness and partial-freeze semantics | FULL |
| `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md` | canonical owner | required/optional contribution, dependency freeze, no invented voluntary action | FULL |
| `GAME/CORE/LIVE_SCENE.md` | runtime realization evidence | LIVE failure/conflict/absorption consumer; parts predate WP-16 current owner | FULL |
| `GAME/CORE/MULTIPLAYER.md` | runtime realization consumer | membership/currentness/conflict/changed-path behavior | FULL |
| `GAME/CORE/CHRONOLOGY.md` | runtime semantic consumer | partial-order uncertainty and `CANON_SUSPECT` route without global timeline | FULL |

### 11.6 Mechanics/RNG, presentation and disclosure

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `GAME/CORE/MECHANICS_INTEGRITY.md` | runtime correctness owner/projection | mechanical outcome establishment barrier; identifies a stale correction path requiring reconciliation against later no-replay laws | FULL |
| `GAME/CORE/RANDOMNESS.md` | runtime correctness owner/projection | real RNG, no silent reroll/replacement or retrospective fabrication | FULL |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | canonical owner | accepted semantics vs render/delivery; presentation repair and disclosure separation | FULL |
| Step-5.14 integrated owner above | canonical integration owner | explicitly forbids replaying gameplay to repair Story/presentation and preserves emission limitations | FULL |

A later Step must resolve the apparent old `MECHANICS_INTEGRITY.md` correction wording that permits fresh reroll during correction against later integrated no-replay/accepted-mechanics identity laws according to current supersession/owner status. Step 1 records this as realization/owner-reconciliation debt rather than silently choosing new semantics.

### 11.7 Update, compatibility, package and instruction continuity

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md` | canonical owner | compatibility outcome classes, migration path/currentness, accepted-work preservation | FULL |
| `GAME/CORE/ENGINE_UPDATES.md` | runtime realization/consumer | mismatch recovery, compatibility classes, local adoption after remote publication, mixed-runtime prohibition | FULL |
| `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-23-release-package-version-legal-readiness-canonical-spec.md` | canonical owner | exact package/provenance/release proof separation and fresh-Project empirical gates | FULL |

### 11.8 Story, planning, diagnostics and scale

| Source | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md` | canonical owner | Story derived/noncanonical failure/lag, UNKNOWN/defer, no global scan | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` | implementation-facing integration contract | native-basis Story production/consumer failure route | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-21-diagnostics-observability-cleanup-retirement-canonical-spec.md` | canonical owner | diagnostics nonauthority, UNKNOWN proof, cleanup failure/indeterminacy | FULL |
| `DEV/docs/superpowers/specs/2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md` | canonical owner | architecture/machine/verification/empirical proof separation | FULL |
| `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md` | canonical owner | bounded operations, no unowned SLA/thresholds, staged real-target performance proof | FULL |

### 11.9 Machine/schema/test consumers

| Source/family | Role | WP-25 relevance | Inspection |
|---|---|---|---|
| `GAME/SCHEMA/*.schema.yaml` | persistent/runtime machine contracts | identify current state/LIVE/checkpoint/manifest consumers and avoid accidental new authority | STRUCTURAL |
| `GAME/SCHEMA/live_scene.schema.yaml` | machine consumer | current LIVE physical schema; objective truth/knowledge and closed-vs-absorbed distinction | FULL |
| `GAME/SCHEMA/checkpoint.schema.yaml` | machine consumer | checkpoint remains recovery metadata/projection, not snapshot/current authority | FULL |
| `GAME/SCHEMA/current_state.schema.yaml` | machine consumer | compact current routing/chronology; no generic pending bucket | FULL |
| `GAME/SCHEMA/campaign_manifest.schema.yaml` | machine consumer | engine/ruleset identity, force-push false, campaign current identity | FULL |
| `DEV/TESTS/` | executable/scenario consumer family | realization drift, recovery/publication/compatibility regression routes | STRUCTURAL |
| `DEV/TESTS/test_hourly_durability_contract.py` | executable stale realization evidence | actively asserts retired one-hour product rule | FULL |
| `DEV/TESTS/test_publication_ref_fence_contract.py` | executable currentness evidence | stale sibling rejection, ambiguity lineage/current closure, rewind prohibition | FULL |
| `DEV/TESTS/test_engine_mismatch_recovery_contract.py` | executable package recovery evidence | valid restore/update paths and no arbitrary migration fallback | FULL |
| `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md`, `EXPLICIT_SAVE_CASES.md`, `PERSISTENCE_TRANSACTION_CASES.md`, `LIVE_SCENE_CASES.md`, `INTEGRITY_CASES.md`, `CHRONOLOGY_CASES.md`, `ENGINE_UPDATE_CASES.md`, `ACCESS_CONTROL_CASES.md`, `MECHANICS_INTEGRITY_CASES.md`, `MULTIPLAYER_MEMBERSHIP_CASES.md`, `PERFORMANCE_CASES.md` | scenario/acceptance families | later verification-realization mapping; not architecture authority | STRUCTURAL |
| `.github/workflows/validate.yml` | hosted CI consumer | exact-head maintenance audit + DEV unit-test verification route | FULL |

## 12. Source-role reconciliation / current-owner rules

The Task Brief will treat the following as settled source-order rules:

1. Product Owner direction constrains WP-25 but does not override native semantic owners except where it explicitly supersedes a product policy such as restoration of the old hourly proxy.
2. Step-5.5/WP-13 current durability law wins over stale hourly GAME/test realization.
3. WP-16 current LIVE owner wins over older runtime projection wording where the two differ.
4. The supported-ref publication amendment supplies current Git-backed currentness realization and supersedes wording that assumes an unavailable expected-old parameter; logical exact-source law remains.
5. WP-20 compatibility owner wins over package/version heuristic shortcuts.
6. WP-22/WP-24/R2.6 control proof strength: structural architecture cannot establish production-like host behavior.
7. Story/diagnostics/checkpoints/indexes remain consumers/evidence/projections and never substitute for missing native canon/currentness.
8. A stale runtime/schema/test projection creates machine-realization debt unless it exposes an actual insufficiency/contradiction in the accepted semantic owner.

## 13. Step-2 research questions prepared by Step 1

If the independent Senior Step-1 review later gives GO, Step 2 must answer with evidence rather than assumption:

1. What is the minimal ephemeral cross-owner disposition model that composes native outcomes without creating a second authority?
2. Which inputs are sufficient to derive effective `S0..S4` severity contextually, and which must remain owner-specific?
3. How should gameplay-impact and typed blast-radius classifications compose across local, dependent-scope, campaign-resume and deployment-profile failures?
4. Which risk dimensions meaningfully distinguish quality/operability debt, accumulating progress-loss exposure, canon/currentness/agency risk and disclosure/security risk?
5. For each native failure family, what truthful frontier survives and what continuation is legal now?
6. What semantic fences/tolerances are owner-specific, and where must WP-25 explicitly reject a universal timeout?
7. What bounded retry/idempotency rule applies after confirmed rejection, indeterminate authority-changing operation, recovery reassembly, local post-remote adoption failure and retry exhaustion?
8. How should `UNSUPPORTED` compose with severity/gameplay impact without becoming a terminal-universal error class?
9. How should NORMAL/ELEVATED/DANGER loss-protection state be derived from unpublished established state and advisory host-survivability evidence while avoiding an exact-capacity fiction?
10. Which transitions at DANGER must guard further state growth, and what preservation/repair outcomes permit return to continued play?
11. Which user-visible notices are actionable and safe, and which routine recovery/degradation details should remain invisible?
12. What machine/test/empirical obligations arise from each failure disposition, without overclaiming proof strength?
13. Which stale runtime/test projections must later be repaired under already accepted semantics versus which expose a genuine architecture insufficiency?

## 14. Framing falsifiability / reopen conditions

The current framing should be rejected or materially revised if later evidence shows any of the following:

- a native owner cannot express a required truthful outcome without a new shared persistent authority;
- owner-local outcomes cannot be composed without losing correctness/currentness/agency/disclosure semantics;
- a safe bounded recovery path requires a currently forbidden global scan or hidden background dependency;
- the accepted durability direction cannot protect significant single-copy HOT/SOFT exposure without silently redefining correctness HARD or inventing unsupported host-capacity authority;
- an existing accepted owner directly contradicts the mandatory Product Owner direction in a way that cannot be mechanically reconciled;
- a real supported-host limitation makes an accepted semantic boundary physically unrealizable and therefore requires explicit deployment restriction or architecture reopening.

Implementation inconvenience or stale projections alone are not reopen evidence.

## 15. Step-1 completion / Senior handoff

The mandatory whole-project critic is recorded separately at:

- `DEV/docs/superpowers/design/2026-09-08-r2-7-WP-25-step-1-whole-project-critic.md`.

All mechanically resolvable BLOCKING/SIGNIFICANT framing/source-manifest findings from that critic are incorporated into this post-critic Task Brief/Manifest.

```text
WP25_STEP1_COMPLETE: YES
WP25_STEP1_SENIOR_REVIEW: PENDING
WP25_STEP2_AUTHORIZED: NO
HUMAN_DECISION_REQUIRED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-25 Step-1 Senior review
```

## 16. Version Impact

```text
VERSION_IMPACT: NONE
```

This Step-1 package changes design provenance and global progress routing only. It does not modify any version-bearing runtime module, persistent/protocol schema, campaign/storage/catalog/ruleset generation, package/release format, migration law, or executable gameplay/runtime realization.