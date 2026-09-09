# R2.7 WP-26 Step 3 — Documentation / Routing / Supersession Consistency — Decision Brief

Status: **STEP 3 COMPLETE — DECISION-READY DELTA / NO HUMAN DECISION REQUIRED**

Date: 2026-09-09

This brief consumes the accepted Step-1 package and Step-2 evidence reconciliation. It is design provenance, not a replacement semantic owner.

## 1. Decision question

WP-26 asks one integration question:

> Given already accepted owners and later amendments, what is the smallest mechanically determined corpus/routing/current-realization reconciliation that makes current law discoverable and prevents stale guards from enforcing superseded semantics, without redesigning closed architecture or inventing deferred representation?

Step-2 evidence establishes that this question has no remaining Product Owner trade-off.

## 2. Established facts

1. PO-009 is accepted owner law for baseline Commentator self-contained Story support. Required WP-19 T0 factor values/bindings and eligibility/control evidence must be locally decidable from Story-side material for baseline Commentator use.
2. PO-009 does not make Story gameplay authority and does not create a second ACL/knowledge/disclosure owner.
3. PO-010 replaces the old exact 10,240-byte universal rejection threshold with sizing/review/partition bands while preserving no-truncation and owner-valid representation.
4. Current Story specs, WP-24 and performance regression text still expose the older law as current.
5. Current Character Readiness law allows bounded provisional gameplay before READY_PC; current runtime/setup/save wording and one executable audit guard still preserve a false `pre-live` cutover implication.
6. WP-21/WP-22/WP-24 are closed but their canonical spec headers still say final Senior review pending.
7. Project Map / Canonical Architecture Index routing lags PO-009/PO-010.
8. PO-006 routing text still sends a retained-ref operational-cost consumer into future WP-24 although WP-24 is already closed.
9. PO-009 machine schema/cache/control realization and PO-010 concrete physical partition topology remain intentionally unselected/deferred.
10. Root README contains one build-script suffix mismatch, but README edit authorization is absent.

## 3. Alternatives considered

### Alternative A — documentation-only supersession note

Add only a new WP-26 canonical note/router and leave runtime/tests/audit/current canonical headers untouched.

Rejected because:

- executable P13 would continue asserting the retired 10 KiB threshold;
- `audit_engine.py` would continue requiring stale `pre-live` wording;
- current runtime modules would remain semantically misleading;
- the accepted design-realization policy requires mechanically determined synchronization where no new design choice exists.

### Alternative B — broad rewrite / new global supersession system

Introduce a global supersession registry or normalize every historical document and current consumer into a new metadata model.

Rejected because:

- historical provenance need not be rewritten;
- current owner-first routing already exists;
- this would create a second authority and unnecessary machinery;
- it violates WP-26 anti-overengineering constraints.

### Alternative C — owner-first targeted reconciliation

Apply local supersession only at current-looking conflict points; synchronize current runtime/tests/audit where accepted law uniquely determines the result; update derivative routers; keep genuine representation work deferred.

**Selected.** This is the accepted Step-1 framing model:

```text
OWNER-FIRST ROUTING
+ LOCAL SUPERSESSION
+ TARGETED MACHINE-GUARD RECONCILIATION
```

## 4. Selected reconciliation decisions

### DEC-26-01 — PO-009 targeted baseline Commentator supersession

Current Story contracts SHALL be amended so baseline Commentator historical explanation no longer depends on native-only T0/control fallback.

Required bounded T0 factor values or Story-local bindings belong in the Story support corpus for that consumer. NARRATIVE may navigate into Story-local EVENTS.

Preserve:

- native Master gameplay authority;
- Story nonauthority;
- native Context Runtime capability for non-baseline/deep-source consumers;
- no hidden reasoning capture;
- no new Story schema selection in WP-26.

### DEC-26-02 — PO-010 sizing-band supersession

Current implementation-facing law SHALL stop treating `10240` as a universal validity/rejection boundary.

Current law SHALL state:

```text
~10–12 KiB -> preferred target
13–16 KiB -> explicit review band
>~16 KiB -> default review/partition/rollover expectation
```

These are review/representation bands, not universal validity enums. Exact UTF-8 serialized bytes remain the measurement basis. No truncation is permitted.

### DEC-26-03 — provisional gameplay lifecycle vocabulary

Current runtime/test/audit projections SHALL distinguish:

```text
initializing
    = before PLAY_READY/full-active lifecycle
    = may already contain legitimate bounded provisional gameplay

active
    = post-PLAY_READY/full-active lifecycle
```

`READY_PC` remains a full-active/unrestricted readiness boundary, not a blanket gate on all gameplay.

No lifecycle enum/state is added.

### DEC-26-04 — current canonical closure status

Current canonical WP-21/WP-22/WP-24 headers SHALL reflect their already-established final Senior PASS/closure. Historical Step/review artifacts remain unchanged.

### DEC-26-05 — owner-first routing refresh

`DEV/PROJECT_MAP.md` and `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` SHALL route current readers through PO-009/PO-010 and, after Step 8, the final WP-26 canonical reconciliation owner.

These files remain derivative locators.

### DEC-26-06 — PO ledger route aging repair

Agent-owned PO routing/disposition text SHALL be reconciled to current closed work packages. Immutable Product Owner quotations SHALL remain byte-semantic provenance and SHALL NOT be rewritten as later interpretation.

Still-deferred realization/empirical consumers from PO-001..010 SHALL survive into the WP-27 handoff.

### DEC-26-07 — machine guards follow semantic owners

Current regression/audit checks SHALL verify the current law, not preserve retired phrases or thresholds merely because prior tests encoded them.

At minimum:

- performance P13 uses PO-010 bands;
- durability/save audit asserts unfinished pre-PLAY_READY state remains `initializing` without requiring `pre-live` wording;
- readiness/save/bootstrap regression descriptions preserve provisional-play semantics.

### DEC-26-08 — accepted architecture versus deferred realization

WP-26 SHALL mark the following as accepted-but-unrealized rather than designing them:

- concrete PO-009 Story event/control projection representation, schemas and Commentator cache layout;
- concrete PO-010 writer partition/rollover layout where current owners do not already supply one;
- other deferred implementation/empirical consumers still present in Product Owner routes.

These become explicit WP-27 planning-readiness inputs after final WP-26 Senior closure.

### DEC-26-09 — README boundary

The root README mismatch remains report-only:

```text
README: DEV/TOOLS/run_release_build
canonical path: DEV/TOOLS/run_release_build.py
```

No root README edit occurs without separate Product Owner authorization.

## 5. Material change versus non-change

Material current-law presentation changes:

- baseline Commentator fallback source locality;
- mutable artifact sizing threshold semantics;
- lifecycle vocabulary that currently implies gameplay starts only at PLAY_READY;
- executable regression/audit expectations that encode those stale semantics.

Explicit non-changes:

- no gameplay canon authority change;
- no Story authority change;
- no ACL/disclosure redesign;
- no READY_PC semantic redesign;
- no lifecycle-state addition;
- no partition topology selection;
- no Commentator cache/schema selection;
- no WP-18/WP-19/WP-24 wholesale reopen;
- no implementation plan;
- no release/migration execution.

## 6. Version-impact direction

Expected classification before Step-7 exact file delta:

```text
ENGINE VERSION BUMP: NO
PERSISTENT SCHEMA/GENERATION BUMP: NO
MIGRATION: NO

Category-B module revision bumps:
    only current GAME/CORE modules whose semantic lifecycle wording changes
```

Design/spec/router/test/audit corrections do not themselves require engine version bumps. Exact module version increments will be computed from the final affected CORE set under `DEV/RELEASE/VERSIONING.md`.

## 7. Human decision gate

```text
HUMAN_DECISION_REQUIRED: NO
PRODUCT_OWNER_DECISION_REQUIRED: NO
RECOMMENDATION: execute Alternative C continuously through Steps 4–8
```

No unresolved point changes product semantics, topology or material trade-offs.

## 8. Step-3 result

```text
STEP3: COMPLETE
SELECTED_DIRECTION: OWNER-FIRST TARGETED RECONCILIATION
UNRESOLVED_BLOCKING: 0
UNRESOLVED_SIGNIFICANT_DECISION_GAPS: 0
NEXT_STEP: Step 4 cross-system review
```
