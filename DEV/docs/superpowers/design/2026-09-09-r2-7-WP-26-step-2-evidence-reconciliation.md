# R2.7 WP-26 Step 2 — Documentation / Routing / Supersession Consistency — Evidence Reconciliation

Status: **STEP 2 COMPLETE — EVIDENCE RECONCILED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-09

Authority boundary: this artifact is Step-2 design provenance under the accepted WP-26 Step-1 Task Brief. It does not replace native semantic owners, does not authorize WP-27/implementation planning, and does not itself activate deferred PO-009/PO-010 schema/topology realization.

## 1. Authorization basis

The published Step-1 package received independent Senior `PASS / GO` with:

```text
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

Product Owner then authorized WP-26 Steps 2–8. `DEV/CURRENT_PROGRESS.md` was reconciled before substantive Step-2 work.

## 2. Step-2 method

Step 2 followed the Step-1 open-world Source Manifest rather than treating `D26-01..07` as a closed checklist.

For every current-looking source or machine consumer implicated by the dependency graph, evidence was classified as:

```text
accepted semantic owner / amendment
current derivative locator
current realization / guard
historical provenance
stale current-looking routing or realization
accepted-but-unrealized future consumer
report-only editorial mismatch
```

A current-source correction is classified `REPAIR_NOW` only when all are true:

1. current behavior/routing conflicts with accepted authority;
2. the correction is uniquely implied by existing authority;
3. no new topology/data model/interface/product choice is required;
4. leaving the source unchanged can misroute WP-27 or enforce superseded law.

Historical artifacts remain historical unless their current-looking status/routing creates ambiguity.

## 3. Reconciled owner graph

### 3.1 PO-009 — self-contained Commentator Story corpus

Current owner:

- `DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md`.

Accepted law relevant to WP-26:

```text
BASELINE COMMENTATOR FACTUAL/SUPPORT UNIVERSE
    = Story corpus
    + Story-local self-contained Commentator eligibility/control projection

required WP-19 T0 decision basis
    -> Story-local retained bounded factor values or Story-local binding

baseline Commentator explanation
    -> MUST NOT depend on native-only Actor/T0 escalation

native Master owners
    -> remain gameplay canon / authority

Story
    -> remains noncanonical to gameplay

Commentator eligibility/control projection
    -> derived projection
    -> not a second ACL / knowledge authority / disclosure authority
    -> filter before LLM materialization

Commentator cache/SQLite
    -> separate environment from Master HOT/cache
    -> no schema compatibility requirement
```

The decision explicitly narrows only baseline Commentator fallback/control semantics. It does not remove native retrieval capability for Master use or explicit deep-source modes.

### 3.2 PO-010 — mutable GitHub artifact sizing bands

Current owner:

- `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`.

Accepted law relevant to WP-26:

```text
preferred target: approximately 10–12 KiB serialized UTF-8
explicit review band: 13–16 KiB
above approximately 16 KiB: default review/partition/rollover expectation

these are sizing decision bands
!= universal file-validity enum
!= exact hard publication rejection at 10,240 bytes
```

Retained invariants:

```text
exact serialized UTF-8 is measurement basis
no semantic truncation
owner-valid partition/rollover when required
identity/currentness/atomicity/bounded routing preserved
no concrete shard/page/layout selected by PO-010
```

PO-010 supersedes only old exact-threshold law. It does not reopen WP-24 broadly.

### 3.3 Character readiness / onboarding gameplay

Current semantic chain:

- `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`;
- `GAME/CORE/CHARACTER_READINESS.md`;
- current diegetic onboarding and campaign lifecycle owners.

Current law:

```text
READY_PC false
    != no gameplay

provisional actor + sufficient exact local dependencies
    -> bounded provisional gameplay may proceed

missing exact dependency for proposed outcome
    -> block only that mechanical boundary

READY_PC + coherent durability / PLAY_READY
    -> full active lifecycle / unrestricted gameplay
```

Therefore `initializing` is a lifecycle/readiness state that may already contain legitimate provisional gameplay. `active` marks the post-PLAY_READY/full-active frontier; it is not the first moment that gameplay becomes real.

## 4. Confirmed current-source conflicts and dispositions

### D26-01 — PO-009 native-fallback leakage

Severity: **SIGNIFICANT**

Confirmed current-looking sources:

- `DEV/docs/superpowers/specs/2026-09-07-story-producer-persistence-retrospective-consumer-contract.md` still permits baseline Commentator Story insufficiency to escalate to native `ACTOR_DECISION_BASIS` retrieval;
- `DEV/docs/superpowers/specs/2026-09-08-story-baseline-projection-source-contracts.md` still permits required WP-19 T0 factor values to remain native-only behind Story navigation/reference.

Disposition:

```text
REPAIR_NOW — TARGETED SUPERSESSION
```

Required repair is limited to baseline Commentator semantics:

- Story-local retention/binding of the complete bounded T0 factor set required by PO-009;
- NARRATIVE may navigate to Story-local EVENTS, not native-only T0 data, for baseline explanation;
- preserve native retrieval for Master/deep-source/non-baseline consumers;
- preserve Story nonauthority and native canon ownership.

Deferred realization remains explicit because current `GAME/SCHEMA/event.schema.yaml` does not define a PO-009-specific machine representation and PO-009 intentionally did not select one.

### D26-02 — PO-010 exact 10 KiB hard-cap leakage

Severity: **SIGNIFICANT**

Confirmed current-looking sources:

- `DEV/docs/superpowers/specs/2026-09-04-runtime-mutable-github-artifact-size-owner-decision.md` — old 10,240-byte universal hard cap;
- `DEV/docs/superpowers/specs/2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md` — hard/absolute 10 KiB Story publication trigger;
- `DEV/docs/superpowers/specs/2026-09-08-r2-7-WP-24-performance-scale-operational-budget-canonical-spec.md`, LAW WP24-13 — exact 10 KiB mandatory representation trigger;
- `DEV/TESTS/PERFORMANCE_CASES.md`, P13 — executable regression expectation that 10,241 bytes must be rejected.

Disposition:

```text
REPAIR_NOW — TARGETED THRESHOLD SUPERSESSION + MACHINE-GUARD RECONCILIATION
```

Retain no-truncation, owner-valid bounded representation, currentness and operability semantics. Remove exact 10,240-byte validity boundary from current law. Concrete partition topology stays deferred.

### D26-03 — provisional gameplay vs `pre-live` / `true live` wording

Severity: **SIGNIFICANT**

Current semantic owner `GAME/CORE/CHARACTER_READINESS.md` explicitly allows bounded provisional gameplay before READY_PC when local dependencies are sufficient. `GAME/CORE/DIEGETIC_ONBOARDING.md` likewise says onboarding is part of gameplay.

Current-looking conflicting projections include:

- `GAME/CORE/RUNTIME.md` lifecycle wording equating `initializing` with pre-live and `active` with normal live play;
- `GAME/CORE/CAMPAIGN_SETUP.md` / `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` wording around first `true live` gameplay/scene;
- `GAME/CORE/SAVE_CONTRACT.md` use of `unfinished pre-live` wording;
- `DEV/TESTS/CHARACTER_READINESS_CASES.md`, `DEV/TESTS/EXPLICIT_SAVE_CASES.md`, `DEV/TESTS/BOOTSTRAP_STORAGE_REGRESSION_CASES.md` current regression text that can imply the same false hard cutover;
- `DEV/TOOLS/audit_engine.py` executable durability/save guard explicitly requires the stale `unfinished pre-live setup/onboarding` phrase in `SAVE_CONTRACT.md`.

Disposition:

```text
REPAIR_NOW — CURRENT RUNTIME/TEST/AUDIT REALIZATION RECONCILIATION
```

Repair vocabulary only; preserve lifecycle states and PLAY_READY semantics:

```text
initializing = before PLAY_READY/full-active lifecycle; provisional gameplay may occur
active = post-PLAY_READY/full-active lifecycle
```

No new gameplay architecture is introduced.

### D26-04 — current-looking stale status / transient development metadata

Severity: **SIGNIFICANT**

Confirmed beyond the Step-1 seed list:

- WP-21 canonical spec still says final Senior review pending despite closed final PASS;
- WP-22 canonical spec still says final Senior review pending despite closed final PASS;
- WP-24 canonical spec still says final Senior review pending despite closed final PASS;
- the September-4 mutable-size owner contains a branch line that can be mistaken for semantic applicability/currentness.

WP-20/WP-23/WP-25 canonical headers already reflect closure and require no analogous repair.

Disposition:

```text
REPAIR_NOW — CURRENT CANONICAL STATUS / METADATA CLASSIFICATION ONLY
```

Historical Step design/review documents remain untouched.

### D26-05 — derivative routing lag

Severity: **SIGNIFICANT**

`DEV/PROJECT_MAP.md` Story route names older Story contracts and the old mutable-size owner but does not route through PO-009 or PO-010. `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` likewise needs current owner navigation.

Disposition:

```text
REPAIR_NOW — DERIVATIVE LOCATOR UPDATE
```

The routers remain non-normative and owner-first.

### D26-06 — Product Owner ledger route aging

Severity: **SIGNIFICANT**

Confirmed example:

- PO-006 still routes retained-ref operational cost as deferred to WP-24 `when WP-24 opens`, although WP-24 is closed and incorporated that boundary.

Disposition:

```text
REPAIR_NOW — AGENT-OWNED ROUTING/DISPOSITION TEXT ONLY
```

Immutable/verbatim Product Owner input is not edited or reinterpreted.

All still-deferred PO-001..008 implementation/empirical consumers must remain visible for WP-27 handoff.

### D26-07 — accepted decision != realized implementation

Severity: **SIGNIFICANT**

Confirmed:

- PO-009 is accepted architecture, but the current Story event/schema/cache/control-projection representation is not selected/realized;
- PO-010 is accepted sizing law, but concrete writer/layout partition/rollover realization remains deferred where owner-valid representation is not already implemented;
- closed Product Owner/architecture status must not be rewritten as `partial` merely because realization is deferred.

Disposition:

```text
PRESERVE EXPLICITLY / HAND OFF TO WP-27
```

WP-26 repairs stale guards and routing; it does not invent PO-009 schema fields or PO-010 physical topology.

### D26-08 — closed canonical owner status headers lag current authority

Severity: **SIGNIFICANT — NEW OPEN-WORLD FINDING**

This was not a named Step-1 seed. Exact-current inspection established the WP-21/WP-22/WP-24 stale final-review-pending headers described above.

Disposition:

```text
REPAIR_NOW
```

This validates the Step-1 requirement that D26 seeds were not a closed coverage list.

### D26-09 — stale machine assertion preserves obsolete lifecycle vocabulary

Severity: **SIGNIFICANT — NEW OPEN-WORLD FINDING**

`DEV/TOOLS/audit_engine.py` requires `SAVE_CONTRACT.md` to contain either `unfinished pre-live setup` or `unfinished pre-live onboarding`. Once current readiness semantics are projected correctly, that assertion would reject the corrected runtime text.

Disposition:

```text
REPAIR_NOW — MACHINE GUARD
```

The replacement guard must assert the semantic requirement — an unfinished pre-PLAY_READY/provisional state remains `initializing` on save — without requiring the false implication that no gameplay occurred.

### D26-10 — root README path mismatch

Severity: **MINOR / REPORT ONLY**

```text
README path: DEV/TOOLS/run_release_build
canonical path: DEV/TOOLS/run_release_build.py
```

Disposition:

```text
REPORT ONLY — ROOT README EDIT NOT AUTHORIZED
```

## 5. Negative findings

The open-world evidence pass did **not** establish a need for:

- a global supersession registry;
- a second documentation authority;
- a new Story gameplay authority;
- a second ACL / knowledge / disclosure owner;
- one shared Master/Commentator SQLite schema;
- a universal hard file-size validity threshold replacing PO-010;
- a new partition topology;
- a new lifecycle state;
- a READY_PC prerequisite for all gameplay;
- reopening WP-18, WP-19, WP-21, WP-22, WP-24, WP-25 or R2.3 as architecture work;
- implementation planning before WP-27;
- a Product Owner decision at Step 2.

## 6. Repair / retain / defer matrix

| Item | Current disposition | Reason |
|---|---|---|
| PO-009 baseline Commentator fallback text | REPAIR_NOW | uniquely superseded by accepted PO-009 |
| PO-009 Story schema/control/cache realization | DEFER_WP27 | representation/topology not selected |
| PO-010 old exact 10 KiB threshold text | REPAIR_NOW | uniquely superseded by accepted PO-010 |
| PO-010 performance regression P13 | REPAIR_NOW | machine guard enforces retired threshold |
| PO-010 physical partition/rollover layout | DEFER_WP27 | concrete owner-valid topology not selected |
| readiness `pre-live` / `true live` current projections | REPAIR_NOW | contradict current Character Readiness law |
| readiness audit phrase assertion | REPAIR_NOW | machine guard would enforce stale wording |
| WP-21/WP-22/WP-24 canonical closure status | REPAIR_NOW | current status is known/fixed |
| historical Step/review artifacts | RETAIN | provenance; no current authority conflict when routed correctly |
| PO-006 future-WP24 route wording | REPAIR_NOW | route target already closed/consumed |
| Project Map / Canonical Index PO-009/010 routing | REPAIR_NOW | derivative locator lag |
| README build-script suffix mismatch | REPORT_ONLY | editorial authorization absent |

## 7. Synthesis completeness gate

### 7.1 Source coverage

Coverage includes all high-risk routes from the accepted Step-1 Source Manifest:

- process/current-position authority;
- Product Owner ledger and PO-009/PO-010 decisions;
- Story producer/baseline/growth owners;
- WP-18/WP-19/Step-4/R2.3 neighbor boundaries;
- mutable artifact sizing origin + superseding owner + WP-24 + performance regression;
- Character Readiness + current runtime/setup/save projections;
- current tests and maintenance audit guard;
- Project Map and Canonical Architecture Index;
- closed canonical WP status headers;
- version-impact owner;
- README report-only boundary.

Search-index snippets were used only for candidate discovery where useful; currentness conclusions were based on exact-ref reads.

### 7.2 Semantic coverage

Every material requirement is classified as one of:

```text
already current / retained
repair now
accepted but deferred to WP-27 realization
historical provenance
report only
```

No accepted requirement has been dropped merely because it is not currently realized.

### 7.3 Human-decision gate

```text
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
WHOLESALE_UPSTREAM_REOPEN_REQUIRED: NO
```

The remaining choices are mechanically determined by accepted authority or intentionally deferred representation work.

## 8. Step-2 result

```text
STEP2: COMPLETE
OPEN_WORLD_FINDINGS_BEYOND_SEEDS: 2 SIGNIFICANT (D26-08, D26-09)
TOTAL_SIGNIFICANT_RECONCILIATION_OBLIGATIONS: 9
REPORT_ONLY_MINOR: 1
UNRESOLVED_BLOCKING: 0
HUMAN_DECISION_REQUIRED: NO
NEXT_STEP: Step 3 Decision Brief
```
