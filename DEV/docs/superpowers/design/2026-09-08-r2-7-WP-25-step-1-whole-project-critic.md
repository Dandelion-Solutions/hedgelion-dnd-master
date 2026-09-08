# R2.7 WP-25 Step 1 — Mandatory Whole-Project Task-Brief Critic

Status: **COMPLETE — ALL MECHANICALLY RESOLVABLE STEP-1 FINDINGS REPAIRED / PENDING INDEPENDENT SENIOR STEP-1 REVIEW**

Date: 2026-09-08

Scope: independent whole-project critic of the WP-25 Step-1 framing and Source Manifest for **Error / degradation / failure semantics**. This is the mandatory Step-1 critic required by `DEV/DESIGN_PROCESS.md` and `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

This artifact is design provenance. It is not a canonical WP-25 specification and does not authorize Step 2.

## 1. Critic method

The critic did not review only the draft WP-25 brief or the Product Owner direction. It independently reconstructed direct and indirect dependency routes from current `DEV/PROJECT_MAP.md`, then checked current owners, superseding decisions, runtime projections, schemas/tests and current status authority.

Primary routes independently reconstructed:

```text
failure/degradation
    -> native semantic owner outcome
    -> current authority/currentness basis
    -> truthful surviving frontier
    -> legal continuation / dependent scope
    -> recovery/retry/idempotency
    -> presentation/disclosure
    -> verification/empirical obligation

persistence/durability
    -> Step-5.5 durability
    -> WP-13 publication/currentness
    -> publication-ref repair amendment
    -> WP-14 recovery
    -> GAME persistence/save/session/durability projections
    -> executable durability/publication tests

host/context
    -> R2.3 Context Runtime
    -> R2.4 single-context execution
    -> R2.6 host assurance
    -> WP-08 instruction/package cache
    -> WP-09 bounded context realization
    -> WP-24 scale/performance proof discipline

multiplayer/LIVE/agency
    -> ACCESS_CONTROL
    -> WP-16 LIVE/currentness
    -> WP-17 collaboration/agency
    -> branch/ref policy decisions
    -> LIVE/MULTIPLAYER/CHRONOLOGY projections and schema

accepted mechanics -> persistence/presentation
    -> MECHANICS_INTEGRITY / RANDOMNESS
    -> Step-5.12 delivery/disclosure
    -> Step-5.14 integrated recovery/concurrency laws

update/package
    -> WP-20 compatibility/migration
    -> WP-08 instruction cache
    -> ENGINE_UPDATES
    -> WP-23 exact package/release proof boundaries

Story/diagnostics
    -> WP-18 Story
    -> Story integration contract
    -> WP-21 diagnostics/cleanup
    -> WP-22 proof classes
    -> WP-24 bounded-operation constraints
```

The critic distinguished:

```text
accepted semantic-owner conflict
!= stale/incomplete GAME/schema/test realization
```

A stale projection is not evidence that accepted architecture must be reopened.

## 2. Whole-project owner coverage checked

Current process/status/routing:

- `AGENTS.md`;
- `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/CURRENT_PROGRESS.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`.

Mandatory Product Owner inputs:

- `DEV/docs/superpowers/specs/2026-09-08-hdm-wp25-failure-degradation-durability-risk-owner-direction.md`;
- full `PO-008` in `DEV/PRODUCT_OWNER_INPUT.md`.

Semantic owners/amendments checked:

- Step-5.5 durability;
- WP-13 durability/publication/currentness;
- WP-14 recovery/checkpoint/session repair;
- supported-ref publication/currentness amendment;
- Step-5.14 integrated recovery/concurrency closure;
- R2.3 Context Runtime;
- R2.4 single-context LLM execution;
- R2.6 host assurance;
- WP-08 instruction/role-context realization;
- WP-09 Context loading/resource-bound realization;
- `ACCESS_CONTROL.md`;
- creator-login continuity owner decision;
- branch/ref deletion prohibition owner decision;
- WP-16 multiplayer/LIVE;
- WP-17 collaboration/agency;
- Step-5.12 host delivery/disclosure;
- WP-18 Story;
- Story producer/persistence/retrospective integration contract;
- WP-20 update/migration/compatibility;
- WP-21 diagnostics/cleanup;
- WP-22 verification/evaluation completeness;
- WP-23 package/version/release readiness;
- WP-24 performance/scale/operational budget.

Runtime/machine/test consumers checked include:

- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/LIVE_SCENE.md`;
- `GAME/CORE/MULTIPLAYER.md`;
- `GAME/CORE/CHRONOLOGY.md`;
- `GAME/CORE/ENGINE_UPDATES.md`;
- `GAME/CORE/MECHANICS_INTEGRITY.md`;
- `GAME/CORE/RANDOMNESS.md`;
- `GAME/SCHEMA/live_scene.schema.yaml`;
- `GAME/SCHEMA/checkpoint.schema.yaml`;
- `GAME/SCHEMA/current_state.schema.yaml`;
- `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- structural inventory of `GAME/SCHEMA/` and `DEV/TESTS/`;
- `DEV/TESTS/test_hourly_durability_contract.py`;
- `DEV/TESTS/test_publication_ref_fence_contract.py`;
- `DEV/TESTS/test_engine_mismatch_recovery_contract.py`;
- relevant durability/save/persistence/LIVE/integrity/chronology/update/access/mechanics/multiplayer/performance scenario families;
- `.github/workflows/validate.yml`.

## 3. Finding summary

```text
STEP1_CRITIC_BLOCKING_FOUND: 0
STEP1_CRITIC_SIGNIFICANT_FOUND: 7
STEP1_CRITIC_MINOR_FOUND: 2

UNRESOLVED_BLOCKING_AFTER_REPAIR: 0
UNRESOLVED_SIGNIFICANT_AFTER_REPAIR: 0
HUMAN_DECISION_REQUIRED: NO
ACCEPTED_SEMANTIC_OWNER_CONFLICT_FOUND: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

All seven SIGNIFICANT findings were framing/source-manifest omissions or ambiguity risks that could be repaired mechanically from current owners. No Product Owner judgment remained at Step 1.

## 4. Findings and resolutions

### S25-S1-01 — Failure composition could accidentally become a second semantic authority

Severity: **SIGNIFICANT**

Problem:

A WP-25 framing centered on one error taxonomy could flatten native owner outcomes and let a cross-owner object decide semantics already owned elsewhere. Current owners already expose materially different epistemic/result spaces, including:

```text
recovery: READY | RETRY | BLOCKED
Context: ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE
publication: CONFIRMED_ACCEPTED | CONFIRMED_REJECTED | INDETERMINATE
compatibility: DIRECT_COMPATIBLE | MAINTENANCE_REFRESH | MIGRATION_REQUIRED |
               UNSUPPORTED_INCOMPATIBLE | INDETERMINATE
```

Resolution:

The Task Brief now makes native outcome preservation a hard invariant and frames later WP-25 work as ephemeral cross-owner disposition/composition. It explicitly separates cause, effective severity, gameplay disposition and retry policy, with independent scope/risk/tolerance/frontier/user-visibility axes. `UNSUPPORTED` remains orthogonal.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-02 — Durability-risk framing was incomplete without supersession + host-proof route

Severity: **SIGNIFICANT**

Problem:

Reading only current GAME durability text would reintroduce the historical one-hour ceiling as product law. Reading only Step-5.5/WP-13 would miss the Product Owner's newer loss-protection concern near host/context incapacity. Reading host heuristics as precise facts would violate WP-22/WP-24/R2.6 proof discipline.

Concrete stale realization evidence exists:

- `GAME/CORE/DURABILITY_GUARD.md` still asserts a one-hour dirty ceiling;
- `GAME/CORE/SESSION.md` consumes that ceiling;
- `DEV/TESTS/test_hourly_durability_contract.py` actively enforces the stale rule.

Resolution:

The Source Manifest now composes Step-5.5 + WP-13 + R2.6 + WP-24 + PO-008/owner direction and explicitly classifies the GAME/test timer rule as realization debt, not current semantic authority. The brief distinguishes correctness `HARD` from an operability/loss-protection fence, carries `NORMAL/ELEVATED/DANGER`, forbids choosing exact thresholds in Step 1, and reserves near-capacity behavior/reliability for later empirical supported-host evidence.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-03 — Post-accepted mechanics/RNG failure chain was under-scoped

Severity: **SIGNIFICANT**

Problem:

A primary-error-only framing could permit persistence/presentation recovery to rerun an already accepted mechanic or RNG result. It could also miss the distinct edge where fictional/mechanical acceptance succeeded but rendering/disclosure later failed.

The critic route found a realization-reconciliation issue: `GAME/CORE/MECHANICS_INTEGRITY.md` contains an older correction path that permits re-resolution with fresh RNG after discovering unsupported narrated mechanics, while later integrated Step-5 laws forbid replay/reroll of **accepted** mechanics merely to repair persistence/presentation. These are not necessarily the same case; later WP-25 work must preserve that distinction rather than mechanically applying either rule everywhere.

Resolution:

The brief adds the full accepted-mechanics -> persistence -> presentation/disclosure cascade, preserves no-reroll/no-replay for accepted mechanics/RNG, and records the older correction wording as an owner/realization-reconciliation question for later evidence rather than silently changing semantics at Step 1.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-04 — Authority/currentness recovery needed the current LIVE/ref-monotonicity owners

Severity: **SIGNIFICANT**

Problem:

Older runtime LIVE or generic persistence wording can be mistaken for current currentness law. That would risk blind retry, wrong source adoption, branch-age authority or conflict resolution by Git order.

Current accepted route is split across WP-13, the supported-ref publication amendment, WP-16, access control and the no-ref-deletion owner decision. The current Connector realization uses parentage + `force=false` fast-forward for the logical exact-source fence; it does not expose an expected-old-ref argument.

Resolution:

The Source Manifest now explicitly includes all current owners and classifies `GAME/CORE/LIVE_SCENE.md` as a runtime realization consumer that may be stale against WP-16. Cascading attack routes now include ref/currentness movement during recovery/diagnostics and ambiguous results after partial/remote success. Negative invariants explicitly forbid blind retry, force/rewind, ref deletion and Git/LWW fictional authority.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-05 — Package/instruction/migration degradation route was missing exact-basis continuity

Severity: **SIGNIFICANT**

Problem:

Treating runtime mismatch as one high-severity error would collapse distinct compatibility outcomes and could authorize guessed package substitution, mixed-runtime continuation or unauthorized migration. It would also miss failure **after** remote migration acceptance but before successful local target-runtime adoption/rehydration.

Resolution:

The brief now routes this horizon through WP-20 + WP-08 + `ENGINE_UPDATES.md` + WP-23. It preserves exact package/instruction basis, compatibility classes, creator authority, unsupported/indeterminate fail-closed semantics, no ancestry/version-order compatibility inference, no mixed runtime, and a dedicated cascading case for accepted remote update followed by failed local rebind/rehydration.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-06 — Derived-state/diagnostics failures could become accidental canon or global recovery work

Severity: **SIGNIFICANT**

Problem:

A broad failure-management layer could incorrectly treat Story, planning, checkpoint, index/cache or diagnostics as fallback state when native evidence is missing. It could also respond to uncertain Story/cleanup coverage with campaign-wide scans or background correctness workers.

Resolution:

The Task Brief now explicitly includes WP-18, the Story integration contract, WP-21, WP-14 checkpoint semantics and WP-24 bounded-operation law. It forbids using derived/diagnostic surfaces as authority, preserves UNKNOWN/defer where proof is unavailable, prohibits ordinary unbounded WORLD/history/all-ref/all-LIVE scans, and forbids introducing a background worker/heartbeat correctness dependency.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-07 — Proof-strength boundary was insufficient for host-capacity/degradation claims

Severity: **SIGNIFICANT**

Problem:

The Product Owner durability-risk direction intentionally allows advisory capacity heuristics, but current architecture does not supply an exact remaining-context contract, measured emergency-save success probability or universal latency threshold. A Step-1 brief that treated such values as architecture facts would overclaim current evidence.

Resolution:

The brief now carries the explicit proof separation:

```text
ARCHITECTURE COVERAGE
!= MACHINE REALIZATION
!= VERIFICATION REALIZATION
!= EMPIRICAL ACCEPTANCE
```

and routes real supported-host capacity/reliability/latency behavior to future production-like empirical acceptance under R2.6/WP-22/WP-24 after a target is realized. Approximate capacity signals remain advisory evidence only.

Disposition: **REPAIRED / CLOSED**.

## 5. Minor findings

### S25-S1-M1 — Ordinary collaboration wait must not be promoted to failure

Severity: **MINOR**

WP-17 distinguishes ordinary waiting/optional contribution behavior from a missing required contribution that blocks only a dependent scope. The brief now names that distinction explicitly in the failure horizon and invariants.

Disposition: **REPAIRED / CLOSED**.

### S25-S1-M2 — Current schemas must not gain a generic pending/error bucket by implication

Severity: **MINOR**

`GAME/SCHEMA/current_state.schema.yaml` explicitly routes pending work to typed owners and has no generic pending-consequence bucket. `checkpoint.schema.yaml` is recovery metadata, not snapshot/current authority. A later WP-25 machine design must not infer a persisted global failure queue merely for convenience.

The brief now includes these schemas as machine consumers and keeps the prospective cross-owner failure disposition ephemeral unless later evidence establishes a real persistence requirement through an owning decision.

Disposition: **REPAIRED / CLOSED**.

## 6. Negative-invariant attack result

The repaired Step-1 framing explicitly prevents WP-25 from legalizing any of the following as recovery/degradation shortcuts:

```text
guessing missing required evidence
silent authority/source substitution
chat/model memory as campaign authority
replay/reroll of accepted mechanics/RNG
replacement accepted IDs for recovery
blind retry after ambiguous authority-changing publication
force push / ref rewind
branch/ref deletion
alternate forbidden repository transport
last-writer-wins / Git order / arrival order as fictional authority
invented voluntary player action/consent/pass/speech
information/disclosure promotion from physical visibility
Story/planning/checkpoint/index/cache/diagnostics as missing-canon substitute
ordinary unbounded WORLD/history/all-ref/all-LIVE scans
infinite retry/reassembly loops
background worker/heartbeat correctness dependency absent from the supported product
```

No current owner requires relaxing any of these invariants for WP-25 Step 1.

## 7. Accepted owner conflict vs stale realization audit

### Accepted semantic-owner conflicts

```text
FOUND: 0
```

The mandatory Product Owner direction is compatible with the current owner graph at Step-1 framing depth. It extends/composes current owners rather than replacing their native semantics.

### Current stale/incomplete realization debt observed

At least the following current projections need later realization/verification attention, but are not Step-1 architecture reopen triggers:

1. `GAME/CORE/DURABILITY_GUARD.md` — historical one-hour dirty ceiling conflicts with superseding Step-5.5/WP-13/Product Owner direction.
2. `GAME/CORE/SESSION.md` — still consumes the one-hour rule.
3. `DEV/TESTS/test_hourly_durability_contract.py` — actively enforces the retired timer semantics.
4. `GAME/CORE/LIVE_SCENE.md` — parts predate current WP-16 stable selected-source/currentness law and must be judged against WP-16 rather than treated as architecture authority.
5. selected local error/retry/presentation wording in runtime projections may predate WP-13/WP-14/Step-5.12/Step-5.14 composition and must be audited during later realization rather than normalized now.

Step 1 performs no runtime/test repair because realization is outside authorization.

## 8. Residual human judgment check

The critic found no unresolved Step-1 question requiring Product Owner judgment.

Already decided by Product Owner/current owners:

- multidimensional failure framing rather than one master error enum;
- context-derived `S0..S4` starting severity vocabulary;
- `UNSUPPORTED` orthogonal to severity;
- no restoration of hourly save product law;
- NORMAL/ELEVATED/DANGER durability-risk direction without exact threshold selection now;
- no weakening of authority/currentness/agency/disclosure/no-reroll/no-ref-delete invariants;
- proof-class separation.

Later Steps may expose a genuine trade-off, but Step 1 does not invent one merely to create an approval pause.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
```

## 9. Completeness gate

```text
[x] Project Map used to reconstruct direct and indirect dependency routes.
[x] Mandatory Product Owner direction and full PO-008 inspected.
[x] Actual semantic owners inspected rather than relying on indexes/roadmaps.
[x] Superseding owner decisions/amendments reconciled.
[x] Relevant GAME projections inspected as realization/consumer evidence.
[x] Relevant schema/test families structurally inspected and selected material consumers read.
[x] Cascading failure routes included, not only primary errors.
[x] Scope/agency/disclosure/currentness/accepted-mechanics negative invariants preserved.
[x] Stale realization distinguished from accepted architecture conflict.
[x] Durability host-risk direction composed with Step-5.5/WP-13/R2.6/WP-24.
[x] Proof-strength separation preserved.
[x] All critic BLOCKING/SIGNIFICANT framing gaps mechanically repaired in the Task Brief/Manifest.
[x] Remaining questions are legitimate Step-2 research questions, not omitted Step-1 evidence.
```

## 10. Step-1 critic verdict

```text
STEP1_CRITIC_BLOCKING_FOUND: 0
STEP1_CRITIC_SIGNIFICANT_FOUND: 7
STEP1_CRITIC_MINOR_FOUND: 2

UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO

WP25_STEP1_COMPLETE: YES
WP25_STEP1_SENIOR_REVIEW: PENDING
WP25_STEP2_AUTHORIZED: NO
NEXT_AUTHORIZED_UNIT: NONE
NEXT_GATE: mandatory independent WP-25 Step-1 Senior review
```

This is a worker Step-1 completion verdict only. It is **not** the mandatory independent Senior verdict.

## 11. Version Impact

```text
VERSION_IMPACT: NONE
```

The critic and repaired Task Brief are design provenance only. No version-bearing runtime/schema/catalog/protocol/package/migration or executable gameplay surface is changed.