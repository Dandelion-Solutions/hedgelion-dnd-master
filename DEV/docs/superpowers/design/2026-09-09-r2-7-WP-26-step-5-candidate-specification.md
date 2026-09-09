# R2.7 WP-26 Step 5 — Documentation / Routing / Supersession Consistency — Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE READY FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-09

This is the Step-5 candidate architecture/specification for WP-26. It is not final canonical authority until Step 8 and mandatory independent final Senior review. Native semantic owners and accepted Product Owner decisions remain controlling.

## 1. Purpose

WP-26 defines how the current HDM corpus is reconciled when later accepted owners/amendments make older current-looking documentation or machine guards misleading.

It does not create a documentation subsystem. Its implementation-facing invariant is:

> A future planner must be able to reach current law from current routers/owners without relying on filename recency or chat history, and current machine guards must not enforce superseded semantics.

## 2. Authority model

### LAW WP26-1 — Semantic owners remain primary

```text
current semantic owner / accepted amendment
    > derivative router/index
    > historical design/review provenance
    > filename/date recency
    > chat memory
```

WP-26 does not create a new global authority tier.

### LAW WP26-2 — Local supersession, not corpus erasure

When later accepted authority narrows/supersedes an older statement:

- current-looking implementation-facing text is locally amended or explicitly routed through the superseding owner;
- historical Step/review evidence remains historically accurate;
- history is not rewritten to pretend later decisions were known earlier.

### LAW WP26-3 — Machine realization follows accepted law

A current test/audit/runtime guard that encodes superseded semantics is a realization defect. If the correction is uniquely determined by accepted owners, repair it in WP-26 rather than manufacture future implementation debt.

### LAW WP26-4 — Deferred physical representation remains deferred

WP-26 SHALL NOT invent a schema, cache layout, partition topology, protocol or new runtime subsystem merely to make accepted architecture appear fully implemented.

Accepted architecture and current realization state are separate dimensions.

## 3. PO-009 current-law reconciliation

### LAW WP26-5 — Baseline Commentator Story support is self-contained

For baseline Commentator historical explanation:

```text
required factual/support universe
    = Story corpus
    + Story-local Commentator eligibility/control projection
```

Required WP-19 T0 decision factors needed for later explanation MUST be present or Story-locally bound such that the baseline Commentator does not depend on native-only `ACTOR_DECISION_BASIS` escalation.

### LAW WP26-6 — Story locality does not create Story authority

PO-009 changes support locality, not gameplay authority.

```text
native gameplay owners remain canonical
Story remains derived/noncanonical to gameplay
physical possession does not grant disclosure permission
```

### LAW WP26-7 — NARRATIVE may navigate Story-local support

A readable NARRATIVE projection may stay compact and point to Story-local EVENTS/support records. Baseline Commentator explanation SHALL NOT require the NARRATIVE layer itself to duplicate every detailed factor, but the required detailed support may not be native-only.

### LAW WP26-8 — Eligibility/control projection is derived, not a second ACL

The Commentator eligibility/control projection:

- is derived from current native access/knowledge/control semantics;
- must be sufficient for local baseline Commentator eligibility decisions;
- filters unavailable/private support before LLM materialization;
- is not a new authority over gameplay facts or permissions.

### LAW WP26-9 — Native escalation remains valid outside the narrowed baseline

Native Context Runtime capabilities remain available for Master operation, explicit deep-source research/recovery or another owner-authorized non-baseline consumer. PO-009 does not globally delete those capabilities.

### REALIZATION WP26-P009-R1

Concrete Story schema/event fields, control-projection structures and Commentator cache/SQLite layout remain accepted-but-unrealized and route to WP-27 implementation-planning readiness after final WP-26 closure.

## 4. PO-010 sizing reconciliation

### LAW WP26-10 — Retired exact hard cap is not current law

The former universal rule:

```text
serialized UTF-8 > 10240 bytes -> publication forbidden
```

is superseded for current size-threshold semantics.

### LAW WP26-11 — Current sizing bands

Current decision bands are:

```text
approximately 10–12 KiB
    -> preferred target

13–16 KiB
    -> explicit review band

above approximately 16 KiB
    -> default review / partition / rollover expectation
```

These bands guide representation/operability decisions. They are not universal validity enums and do not establish a new vendor hard limit.

### LAW WP26-12 — Exact byte measurement and no truncation survive

- Compare exact serialized UTF-8 byte size when applying the sizing policy.
- Never truncate authoritative semantic content merely to meet a band.
- Owner-valid partition/rollover must preserve identity/currentness/atomicity/bounded routing.

### LAW WP26-13 — Physical partition topology remains owner-specific

WP-26/PO-010 do not select one universal shard/page/file layout. Where a concrete owner-valid representation is absent, realization is a WP-27 input.

## 5. Character readiness / lifecycle reconciliation

### LAW WP26-14 — `initializing` is not synonymous with no gameplay

A campaign may remain `initializing` while legitimate bounded provisional/onboarding gameplay is already occurring.

`initializing` means the campaign has not yet reached the accepted PLAY_READY/full-active lifecycle frontier.

### LAW WP26-15 — READY_PC is not a blanket gameplay gate

Before READY_PC:

- a proposed bounded outcome may proceed when exact local dependencies are sufficient;
- an outcome requiring missing exact mechanics is blocked locally;
- missing mechanics are not guessed;
- provisional identity/readiness state remains honest.

### LAW WP26-16 — `active` means post-PLAY_READY/full-active lifecycle

`active` denotes the campaign after READY_PC/PLAY_READY and coherent required durability have been satisfied. It must not be described as the first moment that any gameplay becomes real.

### LAW WP26-17 — Save semantics use readiness, not `pre-live` proxy wording

An explicit save before PLAY_READY preserves established durable provisional/onboarding state and keeps lifecycle `initializing`. It does not fabricate readiness or mark the campaign active.

Current audit/test guards must assert this semantic rule directly rather than requiring `pre-live` wording.

## 6. Canonical status and routing reconciliation

### LAW WP26-18 — Current canonical status must match accepted closure

A current canonical owner that is already closed after mandatory Senior PASS SHALL NOT continue to present itself as pending that same review.

Historical review artifacts remain unchanged.

### LAW WP26-19 — Derivative locators route through current amendments

`DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` remain non-normative locators but SHALL route material current concerns through applicable later owner decisions/amendments such as PO-009 and PO-010.

### LAW WP26-20 — Product Owner quotations are immutable provenance

Agent-owned routing/status/disposition around a Product Owner entry may be updated as later work closes or moves. Verbatim Product Owner input is not rewritten to match later state.

### LAW WP26-21 — Closed architecture and unrealized implementation are separate

An `INCORPORATED` Product Owner decision or closed architecture WP remains closed even when a later schema/code/empirical consumer is still deferred.

Routers SHALL preserve both facts:

```text
architecture status = accepted/closed
realization status = current / partial / deferred as actually evidenced
```

## 7. WP-27 handoff contract

After final WP-26 Senior closure, WP-27 implementation-planning readiness must consume, at minimum:

### PO-009 realization

- Story-local retained/bound T0 support representation;
- Story-local eligibility/control projection representation;
- pre-LLM filtering realization;
- Commentator cache/SQLite design isolated from Master cache;
- schema/version/migration implications only after the representation is selected.

### PO-010 realization

- concrete writer-specific handling of preferred/review/partition bands;
- owner-valid partition/rollover where needed;
- exact-byte measurement in relevant writer/test paths;
- no semantic truncation;
- no assumption of one universal physical layout.

### Other Product Owner routes

All still-deferred implementation/empirical consumers from PO-001..008 remain planning inputs when their owning implementation slice is reached. WP-26 must not lose them merely because their architecture entries are `INCORPORATED`.

## 8. Repair propagation set

The Step-5 candidate expects Step 7 to reconcile the proven current sources, subject to Step-6 adversarial findings.

### Story / PO-009

- producer/persistence/retrospective consumer contract;
- baseline projection source contracts;
- current derivative routers;
- focused regression assertions where current machine checks need the new routing law.

### Sizing / PO-010

- September-4 size owner: explicit partial supersession/currentness note;
- Story growth/sharding owner: remove absolute 10 KiB current-law claims;
- WP-24 LAW WP24-13: current sizing amendment;
- `DEV/TESTS/PERFORMANCE_CASES.md` P13;
- current routers.

### Readiness / lifecycle

- current affected CORE projections;
- readiness/save/bootstrap regression cases whose wording encodes the old cutover;
- `DEV/TOOLS/audit_engine.py` save/readiness guard.

### Status / routing

- WP-21/WP-22/WP-24 canonical closure headers;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`;
- agent-owned Product Owner route/status text, especially PO-006;
- `DEV/CURRENT_PROGRESS.md` at Step 8.

### Editorial boundary

- root README mismatch remains report-only and is not repaired without explicit Product Owner authorization.

## 9. Verification contract

A final conforming WP-26 worker closure requires:

```text
Step-6 adversarial critic complete
all BLOCKING/SIGNIFICANT findings mechanically resolved or valid human gate raised
Step-7 propagation complete
Step-8 canonical owner published
current routers updated
CURRENT_PROGRESS stops at final Senior gate
focused regression coverage present
full maintenance audit PASS
DEV unit tests PASS
exact-head workflow PASS
fresh remote ref read after verification
```

Coverage does not mean all PO-009/PO-010 physical realization is implemented. Deferred realization must be explicit and routable.

## 10. Version impact

Expected candidate classification:

```text
ENGINE_VERSION_BUMP_REQUIRED: NO
PERSISTENT_SCHEMA_OR_GENERATION_BUMP_REQUIRED: NO
MIGRATION_REQUIRED: NO
```

Version-bearing GAME/CORE modules materially corrected in Step 7 receive patch component revisions according to `DEV/RELEASE/VERSIONING.md`.

## 11. Non-goals

WP-26 SHALL NOT:

- create a new global documentation/supersession registry;
- redesign Story authority;
- redesign Actor capture;
- create a second ACL/knowledge/disclosure owner;
- select PO-009 schema/cache topology;
- select universal PO-010 partition topology;
- create a new lifecycle state;
- make READY_PC a blanket gameplay gate;
- re-enable branch/ref deletion;
- begin WP-27 or implementation planning;
- edit the root README without separate authorization;
- execute release/migration/gameplay bootstrap.

## 12. Candidate result

```text
STEP5: COMPLETE
CANDIDATE_DIRECTION: OWNER-FIRST LOCAL SUPERSESSION + CURRENT MACHINE RECONCILIATION
HUMAN_DECISION_REQUIRED: NO
NEXT_STEP: Step 6 mandatory whole-project adversarial review
```
