# R2.7 WP-26 Step 7 — Finding Resolution and Propagation

Status: **STEP 7 COMPLETE — ALL STEP-6 SIGNIFICANT FINDINGS RESOLVED / STEP 8 CANONICALIZATION NEXT**

Date: 2026-09-09

Scope: item-level closure and propagation accounting for the mandatory Step-6 whole-project adversarial review of WP-26 Documentation / Routing / Supersession Consistency.

Step-6 critic:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-6-whole-project-adversarial-review.md`

Verified repair baseline before this ledger was published:

```text
REMOTE_HEAD: e69c07ad7439f242b624533e015ead07c9e17e44
WORKFLOW: Validate engine source
RUN_ID: 34347612283
RUN_NUMBER: 1936
CONCLUSION: success
```

This ledger does not rewrite the Step-5 candidate or Step-6 critic as though later repairs were present originally. Those documents remain historical design/review provenance. Step 8 will publish the single final WP-26 canonical owner.

## 1. Finding-propagation ledger

### S6-26-01 — PO-009 baseline native-fallback leakage

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / PROPAGATED**.

Affected current surfaces:

- `DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` — updated;
- `DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md` — updated;
- `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` — retained as current semantic owner/amendment;
- Step-5 candidate and Step-6 critic — retained as historical design/review provenance.

Resolution: baseline Commentator support now routes to Story-local retained/bound support plus Story-local eligibility/control projection. Native `ACTOR_DECISION_BASIS` capability remains available for Master/deep-source or other owner-authorized non-baseline consumers. No concrete schema field was invented.

Current owner until Step-8 canonicalization: PO-009 owner decision plus the affected Story owners for their local contracts. Step 8 incorporates the reconciled cross-system law into final WP-26 authority without displacing native Story/gameplay owners.

### S6-26-02 — PO-010 retired hard-cap leakage

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / PROPAGATED**.

Affected current surfaces:

- `DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` — explicitly marked superseded for current threshold semantics;
- `DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md` — updated to current sizing bands;
- `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md` — current threshold projection reconciled while WP-24 remains closed;
- `DEV/TESTS/PERFORMANCE_CASES.md` — changed from exact `10241 => reject` behavior to preferred/review/partition expectations;
- `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` — retained as current semantic owner/amendment.

Resolution: the former universal `>10240 serialized UTF-8 bytes => publication forbidden` rule is no longer current law. Current bands remain approximately 10–12 KiB preferred, 13–16 KiB explicit review, and above approximately 16 KiB default review/partition/rollover expectation. Exact UTF-8 measurement, no semantic truncation and owner-valid partition/currentness obligations survive.

Current owner until Step-8 canonicalization: PO-010 owner decision plus native writer/Story/WP-24 owners for their local constraints.

### S6-26-03 — readiness/lifecycle propagation set

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / PROPAGATED / VERSIONED**.

Affected current CORE projections were updated:

```text
GAME/CORE/RUNTIME.md                    framework_module_version 1.0.1 -> 1.0.2
GAME/CORE/CAMPAIGN_SETUP.md             framework_module_version 1.0.2 -> 1.0.3
GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md     framework_module_version 0.7.3 -> 0.7.4
GAME/CORE/SAVE_CONTRACT.md              framework_module_version 0.2.0 -> 0.2.1
GAME/CORE/CORE_INDEX.md                 framework_module_version 0.3.0 -> 0.3.1
```

Resolution: `initializing` is no longer presented as a no-gameplay/pre-live state. Owner-valid bounded provisional gameplay may occur before PLAY_READY when local committed dependencies are sufficient. READY_PC/PLAY_READY remains the transition to full-active mechanics-capable lifecycle and exact missing mechanics remain locally fail-closed.

Current semantic owners remain `CHARACTER_READINESS.md`, `DIEGETIC_ONBOARDING.md` and the affected native CORE contracts in their own domains. WP-26 reconciles their current cross-document projection; it does not create a new lifecycle owner.

### S6-26-04 — stale executable `pre-live` audit proxy

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / MACHINE GUARD RECONCILED**.

Affected current surface:

- `DEV/TOOLS/audit_engine.py` — updated.

Resolution: the audit no longer requires stale `unfinished pre-live setup/onboarding` phrasing. It checks the actual pre-PLAY_READY lifecycle/readiness invariant instead, while retaining paused/post-PLAY_READY protections.

Current owner: native readiness/save lifecycle semantics; audit remains a machine verification consumer, not semantic authority.

### S6-26-05 — regression prose creates false first-play gate

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / PROPAGATED**.

Affected current regression surfaces:

- `DEV/TESTS/CHARACTER_READINESS_CASES.md` — corrected to distinguish provisional gameplay from full-active/post-PLAY_READY play;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md` — stale pre-live save wording removed;
- `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` — stale first-live-scene lifecycle wording removed.

Exact mechanic blockers were not weakened.

Current owners remain the native readiness/save/bootstrap contracts. Regression cases are executable/scenario evidence only.

### S6-26-06 — closed canonical headers claim pending final review

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / CURRENT STATUS CORRECTED**.

Affected current canonical headers:

- WP-21 canonical spec — corrected to closed/PASS state;
- WP-22 canonical spec — corrected to closed/PASS state;
- WP-24 canonical spec — corrected to closed/PASS state.

Historical Step/review artifacts were not rewritten.

Current owner of global closure state remains `DEV/CURRENT_PROGRESS.md`; each closed canonical spec remains the semantic owner for its own WP.

### S6-26-07 — derivative routing can bypass PO-009/PO-010

Severity: **SIGNIFICANT**

Final disposition: **STEP-7 ROUTING REPAIR COMPLETE / STEP-8 FINAL-OWNER ROUTE REQUIRED**.

Affected derivative locators:

- `DEV/PROJECT_MAP.md` — now routes directly to PO-009 and PO-010 current owner/amendment surfaces;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — now locates PO-009 and PO-010 current owners.

Both remain explicitly non-normative locators. Step 8 must add the final WP-26 canonical owner to these routes after that owner exists. This is a deterministic Step-8 canonicalization obligation, not an unresolved finding or human decision.

Current semantic owners before Step 8 remain the linked native owners and accepted PO-009/PO-010 amendments.

### S6-26-08 — Product Owner ledger route aging

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / AGENT-OWNED ROUTING UPDATED**.

Affected current surface:

- `DEV/PRODUCT_OWNER_INPUT.md` — PO-006 agent-owned routing/current-impact prose reconciled to the fact that WP-24 is already incorporated/closed.

The verbatim Product Owner quotation was not rewritten. The deletion prohibition remains unchanged. Future realized measurement/planning remains routed through applicable current proof/planning owners rather than a fictional future opening of WP-24.

Current authority: immutable PO-006 input for the Product Owner decision itself; current agent-owned routing for disposition/consumer status.

### S6-26-09 — accepted architecture can be mistaken for machine completion

Severity: **SIGNIFICANT**

Final disposition: **SEMANTIC RESOLUTION COMPLETE / STEP-8 CANONICAL PROPAGATION REQUIRED**.

Current evidence preserves the distinction:

```text
PO-009 / PO-010 architecture decision = accepted / incorporated
machine realization = explicitly deferred where concrete representation is not selected
```

In particular, current `GAME/SCHEMA/event.schema.yaml` does not contain invented `commentator_eligibility_projection` or `commentator_control_projection` fields. WP-26 does not select the concrete Story schema/cache topology or a universal physical writer partition topology.

Step 8 must make this realization boundary explicit in the final WP-26 canonical owner, derivative routes and WP-27 handoff. That is deterministic canonicalization of an already settled disposition, not unresolved architecture.

Current owners: PO-009 and PO-010 for accepted semantic decisions; future selected representation remains deferred to the later authorized implementation-planning owner.

### S6-26-10 — focused machine regression missing

Severity: **SIGNIFICANT**

Final disposition: **RESOLVED / MACHINE REGRESSION ADDED AND GREEN**.

Added current guard:

- `DEV/TESTS/test_wp26_routing_supersession_contract.py`.

It mechanically protects the current supersession surface against reintroduction of:

- missing PO-009/PO-010 router links;
- baseline Commentator native-only Story fallback;
- universal `10241 => reject` sizing behavior;
- stale readiness/pre-live projection wording;
- stale audit proxy wording;
- closed WP headers claiming final review pending;
- stale PO-006 future-WP-24 routing;
- false claim that deferred PO-009 schema fields already exist.

Verification on the repaired pre-ledger HEAD:

```text
HEAD: e69c07ad7439f242b624533e015ead07c9e17e44
Validate engine source: success
```

Current owners remain the linked semantic owners. This test is a regression consumer only.

### S6-26-11 — release/install surfaces add no stale-law obligation

Severity: **NEGATIVE FINDING**

Final disposition: **CLOSED / NO REPAIR**.

The inspected install/bootstrap surfaces do not establish the stale READY_PC pre-live cutoff or retired 10 KiB hard-cap law. They remain unchanged. This negative finding is retained as evidence that Step 7 did not manufacture unnecessary work.

### S6-26-12 — root README path mismatch

Severity: **MINOR**

Final disposition: **REPORT ONLY / NO WRITE AUTHORIZED**.

Known mismatch remains:

```text
README: DEV/TOOLS/run_release_build
canonical path: DEV/TOOLS/run_release_build.py
```

The root README is manually curated and outside this WP-26 repair authorization. Step 7 does not edit it and does not convert this minor routing mismatch into a blocking/significant closure issue.

## 2. Historical/currentness disposition

The following artifacts remain historical design/review provenance and are not rewritten to pretend later findings were already incorporated:

- Step-1 Task Brief and whole-project critic;
- Step-2 evidence reconciliation;
- Step-3 Decision Brief;
- Step-4 cross-system review;
- Step-5 candidate specification;
- Step-6 whole-project adversarial review.

The Step-6 critic remains intentionally readable with its original OPEN finding dispositions. This Step-7 ledger is the explicit resolution route for those findings. Step 8 will create the final canonical WP-26 owner.

## 3. Version Impact Gate

Classification under `DEV/RELEASE/VERSIONING.md`:

```text
ENGINE_VERSION: 1.0-alpha
VERSION_IMPACT: CATEGORY_B_MODULE_REVISIONS
ENGINE_VERSION_BUMP_REQUIRED: NO
MODULE_PATCH_REVISIONS_REQUIRED: YES — five materially changed CORE modules
PERSISTENT_SCHEMA_OR_GENERATION_BUMP_REQUIRED: NO
MIGRATION_REQUIRED: NO
RELEASE_EXECUTION_REQUIRED: NO
```

The five component-local revisions are listed under S6-26-03. WP-26 did not change `engine_version`, a persistent/protocol schema, campaign/storage/catalog/ruleset generation, package/release format or migration law.

## 4. Step-7 synthesis-completeness gate

```text
STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 10
STEP6_MINOR_FOUND: 1
STEP6_NEGATIVE_FINDINGS: 1

STEP7_SIGNIFICANT_FINDINGS_ACCOUNTED: 10 / 10
STEP7_NEGATIVE_FINDINGS_ACCOUNTED: YES
STEP7_MINOR_FINDINGS_ACCOUNTED: YES
UNRESOLVED_BLOCKING_AFTER_STEP7: 0
UNRESOLVED_SIGNIFICANT_AFTER_STEP7: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
ROOT_README_WRITE_PERFORMED: NO
```

Deterministic Step-8 obligations remaining after Step-7 finding resolution:

1. publish the final WP-26 canonical spec from the repaired candidate/current owners;
2. explicitly preserve the accepted-architecture versus deferred-machine-realization boundary for PO-009/PO-010;
3. add the final WP-26 canonical owner to `DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
4. synchronize `DEV/CURRENT_PROGRESS.md` to Step-8-complete / final-Senior-review-pending state;
5. review the near-term roadmap and update it only if sequence/scope/dependency actually changed;
6. perform Step-8 self-review, exact-head verification and remote read-back;
7. stop for the mandatory independent final WP-26 Senior review.

## 5. Step-7 gate

```text
STEP7: COMPLETE
FINDING_PROPAGATION_SWEEP: COMPLETE
NEXT_STEP: Step 8 canonicalization and self-review
NEXT_HUMAN_GATE: mandatory independent final WP-26 Senior review after completed Step 8
WP27_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
RELEASE_EXECUTION_AUTHORIZED: NO
GAMEPLAY_BOOTSTRAP_AUTHORIZED: NO
```
