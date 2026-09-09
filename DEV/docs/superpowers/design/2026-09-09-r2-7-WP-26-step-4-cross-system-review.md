# R2.7 WP-26 Step 4 — Documentation / Routing / Supersession Consistency — Cross-System Review

Status: **STEP 4 COMPLETE — CROSS-SYSTEM REVIEW PASS / NO HUMAN DECISION REQUIRED**

Date: 2026-09-09

This artifact reviews the Step-3 selected reconciliation against neighboring architecture, runtime, persistence, Story, access, readiness, performance, Product Owner, versioning and verification owners. It does not replace those owners.

## 1. Review objective

The Step-4 question is not whether the selected WP-26 direction is convenient. It is whether each targeted repair preserves the accepted boundaries of every participating owner and does not accidentally activate deferred architecture.

The review therefore attacks the selected delta from both directions:

```text
upstream owner -> proposed correction -> current consumer
current consumer -> proposed correction -> upstream owner
```

A correction passes only if the same accepted semantics survive both routes.

## 2. PO-009 cross-system review

### 2.1 Story versus gameplay canon

Required invariant:

```text
native campaign owners = gameplay canon
Story = noncanonical derived/navigation corpus
```

The PO-009 repair changes what the baseline Commentator support corpus retains, not which source owns gameplay truth.

PASS conditions:

- no Story event becomes gameplay authority by possession alone;
- no Story reconstruction may overwrite native Actor/scene/world owners;
- currentness/identity still comes from the native owner chain;
- Story retains source identity/provenance needed to interpret its derived material.

Result: **PASS**.

### 2.2 WP-19 Actor decision basis

WP-19 requires bounded T0 decision-basis capture for relevant historical Actor decisions, with zero additional serial LLM/tool/publication rounds solely for capture when required T0 evidence is already admitted.

PO-009 requires the bounded factor values/binding needed by baseline Commentator explanation to be Story-local.

These are compatible:

```text
capture once at the accepted decision edge
    -> preserve bounded typed T0 factors
    -> Story projection retains/binds those factors
    -> baseline Commentator later reads Story-local support
```

No extra live-turn round trip is introduced by the documentation correction.

Result: **PASS**.

### 2.3 R2.3 Context Runtime / WP-09

PO-009 does not remove native `ACTOR_DECISION_BASIS` capability from Context Runtime. It changes baseline Commentator sufficiency/fallback policy only.

Thus:

- Master or explicit deep-source consumers may still use bounded native acquisition when authorized/needed;
- baseline Commentator explanation must not rely on that native fallback;
- no universal preload/global scan is introduced.

Result: **PASS**.

### 2.4 Access / knowledge / disclosure boundary

The self-contained Commentator eligibility/control projection is derived from native control/access/knowledge semantics. It is not a second authority.

The selected repair preserves:

```text
physical Story possession != permission
CONTENT basis != CONTROL basis
CONTENT_FINAL != ACCESS_FINAL
eligibility filter before LLM materialization
```

No new `world.knowledge`, ACL or disclosure subsystem is created.

Result: **PASS**.

### 2.5 Commentator cache isolation

The selected WP-26 repair does not define SQLite tables, cache compatibility or shared Master/Commentator storage. PO-009 explicitly allows a separate Commentator cache environment.

Result: **PASS / DEFER PHYSICAL REALIZATION TO WP-27**.

## 3. PO-010 cross-system review

### 3.1 Persistence/currentness

Removing an exact 10,240-byte hard cutoff must not permit semantic truncation or invalid publication topology.

Retained law:

- measure exact serialized UTF-8 bytes;
- prefer compact artifacts around the target band;
- review larger artifacts;
- partition/roll over through an owner-valid representation when size/operability warrants;
- preserve currentness/identity/atomicity and bounded routing;
- never truncate semantic state to make a file fit.

Result: **PASS**.

### 3.2 WP-24 scale law

WP-24 owns bounded-operation and trigger semantics, not one eternal universal byte cutoff. PO-010 is a later Product Owner sizing amendment.

Targeted amendment of LAW WP24-13 is sufficient:

```text
old: >10240 bytes -> publication forbidden
new: sizing/review/partition bands; no universal validity rejection at 10240
```

All other WP-24 boundedness/no-global-scan/no-hidden-worker laws remain unchanged.

Result: **PASS / NO WP-24 WHOLESALE REOPEN**.

### 3.3 Story growth/sharding

Story growth owner retains:

- no semantic truncation;
- bounded service opportunity;
- owner-valid partition/rollover when needed;
- exact currentness/retention semantics;
- no physical topology selected prematurely.

Replacing hard 10 KiB wording with PO-010 bands does not weaken those laws.

Result: **PASS**.

### 3.4 Machine performance regression

`DEV/TESTS/PERFORMANCE_CASES.md` P13 currently encodes the old exact boundary. It must be updated to test all three PO-010 decision bands and the retained no-truncation/owner-valid representation invariant.

Result: **REPAIR REQUIRED / MECHANICALLY DETERMINED**.

## 4. Character Readiness / lifecycle cross-system review

### 4.1 Character Readiness

Current law:

```text
READY_PC false != no gameplay
```

The selected vocabulary repair preserves:

- exact missing mechanics fail closed locally;
- provisional Actor remains provisional;
- `PLAY_READY`/full active lifecycle requires readiness + durability;
- no unsupported capability is invented.

Result: **PASS**.

### 4.2 Campaign lifecycle

No enum/state change is proposed.

Correct interpretation after reconciliation:

```text
initializing
    = campaign has not reached PLAY_READY/full active lifecycle
    = may include legitimate provisional onboarding gameplay

active
    = campaign has reached PLAY_READY/full active lifecycle
```

This is a terminology/current-projection repair, not lifecycle redesign.

Result: **PASS**.

### 4.3 Persistence/save

An explicit save before PLAY_READY must still preserve honest provisional state and keep lifecycle `initializing`; it must not fabricate readiness or activate the campaign.

The repair only removes the phrase `pre-live` as a semantic proxy. Save completeness/durability law is unchanged.

Result: **PASS**.

### 4.4 Audit / regression realization

The current audit guard requires stale wording rather than the actual semantic condition. It must instead assert:

- unfinished pre-PLAY_READY/provisional state remains `initializing` on save;
- `paused` remains reserved for an already PLAY_READY/normal active campaign where applicable;
- corrected runtime docs do not reintroduce a first-gameplay hard gate.

Result: **REPAIR REQUIRED / MECHANICALLY DETERMINED**.

## 5. Product Owner ledger review

Immutable Product Owner quotations remain provenance and are not rewritten.

Agent-owned routing can and must reflect later closed work.

### PO-006

The old route says retained-ref operational cost is future WP-24 work. WP-24 is closed and already consumed the prohibition/operational consequence without re-enabling deletion.

Required route repair:

```text
WP-24 operational consumer: INCORPORATED / CLOSED
future realization/measurement: route through current WP-24/WP-22/WP-27 implementation-readiness chain where applicable
branch/ref deletion remains forbidden
```

No Product Owner decision is needed.

### PO-009 / PO-010

Both remain `INCORPORATED` architecture decisions. Their machine realization remains deferred and must be carried to WP-27 after final WP-26 closure.

No accepted decision should be marked `partial` merely because physical implementation is future work.

Result: **PASS WITH ROUTING REPAIRS**.

## 6. Canonical status/currentness review

Current progress authority already records WP-21/WP-22/WP-24 closed with final Senior PASS. Their canonical spec headers remain stale.

Updating only current canonical headers/current introductory status is safe because:

- no historical Step artifact is altered;
- no semantic law changes;
- current routing becomes consistent with the sole global progress authority.

Result: **REPAIR REQUIRED**.

## 7. Derivative locator review

### Project Map

Must route Story/Commentator and mutable-size concerns through PO-009/PO-010. It remains explicitly non-normative.

### Canonical Architecture Index

Must include current owner/amendment locators and, at Step 8, the final WP-26 canonical reconciliation owner.

No duplicate semantic authority is created.

Result: **REPAIR REQUIRED**.

## 8. Version-impact review

The selected repairs are split into:

### Development/spec/router/test/audit files

No engine/module version bump merely for DEV documentation/test/audit changes.

### GAME/CORE current semantic wording

A patch component revision is required for each version-bearing CORE module whose lifecycle/readiness semantics are materially clarified.

Expected affected modules subject to exact Step-7 delta:

- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/CAMPAIGN_SETUP.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md`;
- `GAME/CORE/CORE_INDEX.md` only if its current routed wording requires a semantic correction and it carries module-version metadata.

No engine version bump, persistent schema/generation bump or migration is implied because WP-26 does not introduce a new persistent representation.

Result: **PASS**.

## 9. Verification review

Step-7/8 verification must prove at least:

1. no current test/audit guard still requires exact 10,240-byte rejection;
2. no corrected runtime/audit path requires `pre-live` wording as the lifecycle truth;
3. Project Map/Canonical Index route PO-009/PO-010;
4. closed canonical WP status headers no longer claim final Senior review pending;
5. PO-006 route no longer points to future opening of WP-24;
6. PO-009 current specs no longer allow baseline Commentator native-only T0/control dependency;
7. PO-010 current specs/tests expose sizing bands and preserve no-truncation/currentness;
8. all module-version changes satisfy versioning audit;
9. full maintenance audit and DEV tests pass on exact final HEAD.

A focused WP-26 static regression test is appropriate because these are current-source consistency contracts and can regress independently of prose review.

## 10. Cross-system negative findings

The review found no accepted-owner conflict requiring Product Owner judgment.

Specifically absent:

- no conflict between PO-009 and native gameplay authority;
- no conflict between PO-010 and no-truncation/currentness;
- no need for a new lifecycle state;
- no need to alter READY_PC mechanics;
- no need to choose a Story schema now;
- no need to choose a partition topology now;
- no need to alter branch/ref deletion prohibition;
- no need to edit root README;
- no need to reopen closed WPs wholesale.

## 11. Step-4 result

```text
STEP4: COMPLETE / CROSS-SYSTEM PASS
BLOCKING_FOUND: 0
NEW_HUMAN_DECISION: NO
MECHANICAL_REPAIRS_CONFIRMED: YES
DEFERRED_REPRESENTATION_WORK_PRESERVED: YES
NEXT_STEP: Step 5 candidate specification
```
