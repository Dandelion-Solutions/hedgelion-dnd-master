# R2.7 WP-26 — Documentation / Routing / Supersession Consistency — Canonical Specification

Status: **CANONICAL WP-26 RESULT — FINAL INDEPENDENT SENIOR PASS / CLOSED**

Date: 2026-09-09

This specification is the canonical integration owner for WP-26. It reconciles current routing and current machine-facing projections with already accepted owners/amendments. It does not replace the native semantic owners named below. The mandatory independent final Senior review passed on the reviewed Step-8 head; public review evidence is `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-final-senior-review.md`.

Primary provenance:

- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-task-brief-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-5-candidate-specification.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-7-finding-resolution-and-propagation.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-step-8-canonicalization-self-review.md`;
- `DEV/docs/superpowers/design/2026-09-09-r2-7-WP-26-final-senior-review.md`.

Accepted cross-cutting amendments integrated here:

- `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` (PO-009);
- `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` (PO-010).

## 1. Canonical result

WP-26 selects and closes:

```text
OWNER-FIRST ROUTING
+ LOCAL SUPERSESSION
+ TARGETED MACHINE-GUARD RECONCILIATION
```

The purpose is narrow: current readers and future planners must be able to reach current law from current owners/routers without relying on filename recency or chat history, and current machine guards must not enforce semantics already superseded by accepted authority.

WP-26 creates no global documentation subsystem, supersession registry, lifecycle owner, Story authority, ACL, schema family, partition topology, scheduler or release mechanism.

## 2. Authority and supersession laws

### LAW WP26-1 — Semantic owners remain primary

```text
current semantic owner / accepted amendment
    > derivative router/index
    > historical design/review provenance
    > filename/date recency
    > chat memory
```

WP-26 is an integration owner for routing/supersession consistency, not a new authority tier over native domain semantics.

### LAW WP26-2 — Supersession is local, not corpus erasure

When later accepted authority narrows or supersedes older wording:

- current-looking implementation-facing text is locally amended or explicitly routed through the superseding owner;
- historical Step/review evidence remains historically accurate;
- history is not rewritten to pretend later decisions were already known.

A stale statement may therefore survive as provenance while losing current implementation-facing authority.

### LAW WP26-3 — Current machine realization follows accepted law

A current test, audit or runtime guard that enforces superseded semantics is a realization defect. When the correction is uniquely determined by accepted owners, the current realization SHALL be repaired in this reconciliation rather than mislabeled as future architecture debt.

### LAW WP26-4 — Accepted architecture and machine realization are separate dimensions

WP-26 SHALL NOT invent schema fields, cache layouts, physical partition topology, protocols or runtime subsystems merely to make accepted architecture appear fully implemented.

Routers and status must preserve both facts independently:

```text
architecture decision = accepted / incorporated / closed as actually evidenced
machine realization   = current / partial / deferred as actually evidenced
```

## 3. PO-009 — self-contained baseline Commentator Story support

### LAW WP26-5 — Baseline Commentator support is Story-local

For supported baseline Commentator historical explanation:

```text
required factual/support universe
    = imported Story corpus
    + Story-local Commentator eligibility/control projection
```

Qualifying retained WP-19 T0 decision-factor meaning required for later explanation MUST be present or Story-locally bound so that baseline Commentator operation does not require native-only `ACTOR_DECISION_BASIS` fallback.

### LAW WP26-6 — Story locality does not create Story authority

PO-009 changes support locality for this consumer, not gameplay authority:

```text
native gameplay/history/knowledge/disclosure/access owners remain authoritative
Story remains derived/noncanonical to gameplay
physical possession does not grant disclosure permission
```

### LAW WP26-7 — Compact NARRATIVE may navigate Story-local detail

The readable NARRATIVE layer may remain compact and navigate to Story-local EVENTS/support records. Required detailed support need not be duplicated into NARRATIVE, but it may not be available only through a native-source fallback for the supported baseline Commentator route.

### LAW WP26-8 — Eligibility/control projection is derived, not a second ACL

The Commentator eligibility/control projection:

- derives from current native access/knowledge/control semantics;
- must be sufficient for local baseline Commentator eligibility decisions;
- filters unavailable/private support before LLM materialization;
- does not own gameplay facts, knowledge, disclosure or permission.

### LAW WP26-9 — Native capability remains valid for other admitted consumers

Native Context Runtime capabilities remain available for Master operation, explicit deep-source research/recovery or another owner-authorized non-baseline consumer. PO-009 does not globally delete native source access.

### REALIZATION WP26-P009-R1 — accepted but not machine-complete

WP-26 does **not** select or claim realization of:

- concrete Story event/schema fields for retained T0 support;
- concrete eligibility/control projection representation;
- concrete pre-LLM filtering machinery;
- Commentator cache/SQLite topology.

Current `GAME/SCHEMA/event.schema.yaml` intentionally contains no invented `commentator_eligibility_projection` or `commentator_control_projection` fields from WP-26. These are downstream planning/realization inputs after WP-26 closure.

## 4. PO-010 — mutable GitHub-backed text sizing

### LAW WP26-10 — The universal exact 10 KiB publication hard stop is retired

The former rule:

```text
serialized UTF-8 > 10240 bytes -> publication forbidden
```

is superseded for current threshold semantics.

The 2026-09-04 size owner remains provenance but is explicitly superseded in this threshold scope by PO-010.

### LAW WP26-11 — Current sizing bands

Current owner-approved bands are:

```text
approximately 10–12 KiB
    -> preferred target

13–16 KiB
    -> explicit review band

above approximately 16 KiB
    -> default review / partition / rollover expectation
```

These are representation/operability review bands, not universal validity enums or a vendor hard limit.

### LAW WP26-12 — Exact measurement and semantic integrity survive

- applicable checks use exact serialized UTF-8 byte measurement;
- authoritative semantic content is never truncated merely to hit a band;
- owner-valid partition/rollover preserves applicable identity, currentness, atomicity and bounded routing obligations.

### LAW WP26-13 — Physical partition topology remains owner-specific

Neither PO-010 nor WP-26 selects one universal shard/page/file layout. Where a concrete owner-valid representation is still absent, that realization remains downstream planning input.

## 5. Character readiness and lifecycle projection

### LAW WP26-14 — `initializing` is not a no-gameplay state

A campaign may remain `initializing` while legitimate bounded provisional/diegetic gameplay already occurs.

`initializing` means the campaign has not yet reached the accepted PLAY_READY/full-active lifecycle frontier.

### LAW WP26-15 — READY_PC is not a blanket gate on all gameplay

Before READY_PC:

- an attempted bounded outcome may proceed when its exact committed local dependencies are sufficient;
- an outcome requiring missing exact mechanics remains locally blocked;
- missing mechanics are not guessed;
- provisional identity/readiness state remains honest.

### LAW WP26-16 — `active` denotes post-PLAY_READY full-active lifecycle

`active` denotes the campaign after READY_PC/PLAY_READY and the coherent required durability frontier have been satisfied. It is not the first moment at which any gameplay becomes real.

### LAW WP26-17 — Save semantics use readiness, not a `pre-live` wording proxy

An explicit save before PLAY_READY preserves established durable provisional/onboarding/gameplay state and keeps lifecycle `initializing`. It does not fabricate readiness or mark the campaign active.

Audit/test guards SHALL assert this semantic condition directly rather than require stale `pre-live` phraseology.

## 6. Current status and routing consistency

### LAW WP26-18 — Current canonical status must match accepted closure

A current canonical owner already closed after its mandatory Senior PASS SHALL NOT continue to present itself as pending that same review. Historical review/Step artifacts remain unchanged.

This rule was applied to the current headers for WP-21, WP-22 and WP-24 during Step 7 and to WP-26 itself by the final closure publication.

### LAW WP26-19 — Derivative locators route through current owners/amendments

`DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` remain non-normative. They SHALL route material current concerns through applicable current semantic owners/amendments, including PO-009, PO-010 and this final WP-26 reconciliation owner.

The locators never override the linked owner.

### LAW WP26-20 — Product Owner quotations remain immutable provenance

Agent-owned routing/status/disposition around a Product Owner entry may be updated when later work closes or moves. Verbatim Product Owner input is not rewritten to match later interpretation.

PO-006 agent-owned routing has therefore been reconciled to already-closed WP-24 while its Product Owner quotation remains preserved.

### LAW WP26-21 — Closure does not imply every downstream representation exists

An incorporated Product Owner decision or closed architecture package remains accepted/closed even when a later schema/code/empirical consumer is still deferred.

Specifically:

- PO-009 semantic architecture is accepted/incorporated while concrete Story/control/cache representation remains deferred;
- PO-010 sizing law is accepted/incorporated while concrete writer-specific partition/rollover topology may remain deferred;
- WP-26 is closed without falsely claiming either physical realization.

## 7. Step-6 findings incorporated

The mandatory Step-6 whole-project adversarial review found:

```text
BLOCKING: 0
SIGNIFICANT: 10
MINOR: 1
NEGATIVE: 1
HUMAN_DECISION_REQUIRED: NO
```

Step 7 resolved and propagated all ten significant findings item-by-item. This canonical spec incorporates their resulting current law:

- S6-26-01 -> Laws WP26-5..9 and PO-009 realization boundary;
- S6-26-02 -> Laws WP26-10..13;
- S6-26-03..05 -> Laws WP26-14..17 plus current CORE/audit/regression repairs;
- S6-26-06 -> Law WP26-18;
- S6-26-07 -> Law WP26-19 and Step-8 derivative-router synchronization;
- S6-26-08 -> Law WP26-20;
- S6-26-09 -> Laws WP26-4 and WP26-21 plus explicit deferred-realization sections;
- S6-26-10 -> focused machine regression coverage;
- S6-26-11 -> negative finding retained with no manufactured repair;
- S6-26-12 -> root README path mismatch retained as report-only, with no README write.

Detailed artifact-by-artifact resolution evidence remains in the Step-7 ledger.

## 8. Current machine-realization evidence

WP-26 repairs current realization only where accepted law uniquely determined the correction.

### 8.1 Focused regression guard

`DEV/TESTS/test_wp26_routing_supersession_contract.py` protects, at minimum:

- PO-009/PO-010 current-owner routing;
- baseline Commentator Story-local support;
- absence of the universal `10241 => reject` rule;
- current sizing-band projection;
- explicit supersession of the old threshold owner;
- provisional-gameplay/PLAY_READY lifecycle semantics;
- removal of stale audit proxy wording;
- corrected closed WP canonical headers;
- corrected PO-006 current route;
- absence of invented deferred PO-009 event-schema fields.

### 8.2 Versioned CORE realization

The five materially changed CORE projections carry one component-local revision increment each:

```text
GAME/CORE/RUNTIME.md                    1.0.1 -> 1.0.2
GAME/CORE/CAMPAIGN_SETUP.md             1.0.2 -> 1.0.3
GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md     0.7.3 -> 0.7.4
GAME/CORE/SAVE_CONTRACT.md              0.2.0 -> 0.2.1
GAME/CORE/CORE_INDEX.md                 0.3.0 -> 0.3.1
```

Tests, audit code, development routers and documentation receive no synthetic module/schema version solely because their current wording/routing changed.

## 9. Downstream planning handoff

This section records planning-readiness inputs only. WP-26 closure makes WP-27 eligible according to the R2.7 sequence; it does not authorize WP-27 or implementation planning.

### PO-009 realization inputs

- Story-local retained/bound T0 support representation;
- Story-local eligibility/control projection representation;
- pre-LLM filtering realization;
- Commentator cache/SQLite design isolated from Master cache;
- schema/version/migration implications only after representation is selected.

### PO-010 realization inputs

- writer-specific handling of preferred/review/partition bands;
- owner-valid partition/rollover where needed;
- exact-byte measurement in implicated writer/test paths;
- no semantic truncation;
- no assumption of one universal physical layout.

### Other Product Owner routes

Still-deferred implementation/empirical consumers from PO-001..008 survive into the applicable future planning slice. Architecture incorporation does not delete those consumer obligations.

## 10. Version Impact Gate

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

WP-26 changes no engine release identity, persistent/protocol schema, campaign/storage/catalog/ruleset generation, package/release format or migration law.

## 11. Explicit non-goals and rejected generalizations

WP-26 does not:

- create a global documentation/supersession registry;
- redesign Story authority or Actor capture;
- create a second ACL/knowledge/disclosure owner;
- select PO-009 schema/cache topology;
- select universal PO-010 partition topology;
- create a lifecycle state;
- make READY_PC a blanket gameplay gate;
- convert approximate sizing bands into exact universal validity thresholds;
- re-enable branch/ref deletion;
- authorize implementation planning or WP-27;
- edit the root README without separate Product Owner authorization;
- execute release/migration/gameplay bootstrap.

## 12. Final closure result

```text
WP26_SELECTED_DIRECTION:
    OWNER-FIRST ROUTING
    + LOCAL SUPERSESSION
    + TARGETED MACHINE-GUARD RECONCILIATION

STEP6_BLOCKING_FOUND: 0
STEP6_SIGNIFICANT_FOUND: 10
STEP7_SIGNIFICANT_RESOLVED: 10 / 10
UNRESOLVED_BLOCKING_AT_WORKER_STEP8: 0
UNRESOLVED_SIGNIFICANT_AT_WORKER_STEP8: 0
UNRESOLVED_BLOCKING_AT_FINAL_SENIOR: 0
UNRESOLVED_SIGNIFICANT_AT_FINAL_SENIOR: 0
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO

ARCHITECTURE_RECONCILIATION: COMPLETE
PO009_CONCRETE_MACHINE_REALIZATION: DEFERRED
PO010_CONCRETE_PARTITION_TOPOLOGY: DEFERRED WHERE NOT ALREADY OWNER-DEFINED
WP26_FINAL_SENIOR_REVIEW: PASS / GO
WP26_CLOSED: YES
WP27_ELIGIBLE: YES
WP27_AUTHORIZED: NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
RELEASE_EXECUTION_AUTHORIZED: NO
GAMEPLAY_BOOTSTRAP_AUTHORIZED: NO
```

Reviewed Step-8 exact-head evidence:

```text
REVIEWED_HEAD: d9ea286e8d80067c606acff0840939fca6d24a06
WORKFLOW: Validate engine source
RUN_ID: 34357466924
RUN_NUMBER: 1942
CONCLUSION: success
FULL_MAINTENANCE_AUDIT: PASS
DEV_UNIT_TESTS: 458 / 458 PASS
VERSION_UNCLASSIFIED: []
VERSION_LEGACY_HITS: []
```

The final closure-publication HEAD must itself remain green before closure is reported externally. That exact-head verification is publication evidence, not another architecture gate.
