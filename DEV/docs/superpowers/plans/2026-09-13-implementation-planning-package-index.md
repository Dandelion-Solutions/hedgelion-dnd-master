# HDM Implementation Planning Package — Index

Status: **AUTHOR POST-SIRR2 CORRECTION ACTIVE — SCENE ROUTE + CHECKPOINT COHERENCE REPAIR**
Date: 2026-09-14

Global gate authority: `DEV/CURRENT_PROGRESS.md`.
Independent re-review #2 finding authority: `2026-09-13-implementation-planning-independent-senior-re-review-2-result.md`.
Production implementation authorized: **NO**.

## Current RD-plan routes

Base plans remain RD-01 through RD-14 as previously indexed. Current v2 routes remain authoritative for RD-08, RD-10 and RD-11.

Mandatory overlays in precedence order:

```text
1. 2026-09-13-implementation-planning-sirr-repair-amendments.md
2. 2026-09-13-implementation-planning-author-self-review-repair-addendum.md
3. 2026-09-13-implementation-planning-author-second-pass-repair-addendum.md
4. 2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md
5. 2026-09-14-implementation-planning-checkpoint-coherence-addendum.md
6. 2026-09-14-implementation-planning-scene-routing-addendum.md
```

Later overlays supersede only the exact conflicting execution detail they repair.

## Current applicability

```text
RD-02: prior information repairs + overlay 5 checkpoint/test materialization timing
RD-03: overlay 5 checkpoint/test materialization timing
RD-04: seven-selector manifest/schema/STORAGE realization; no Story bootstrap prerequisite
RD-05: overlay 5 checkpoint/test materialization timing
RD-06: shipped SAVE/PERSISTENCE cutover + exact proof joins
RD-08: WP-15 temporal owner; scene chronology physical edit precedes RD-09 scene-route edit
RD-09: two-phase LIVE lifecycle; SIRR2 CORE/case-catalog cutover; overlay 6 scene-schema owner-typed route cutover
RD-12: overlay 5 checkpoint/test materialization timing
RD-13: retained Dramaturg + exact Story routes + on-demand Story + overlay 5 checkpoint timing
RD-14: repaired bootstrap consumers + overlay 5 checkpoint timing
```

`GAME/SCHEMA/scene.schema.yaml` is now an explicit shared physical surface: RD-08 publishes its chronology alignment first; RD-09 fresh-reads that result and narrows `live_epoch` to route nomination under the typed-claim/currentness model. The coordinated pre-v1 scene-contract checkpoint uses local `scene_state` schema version `2 -> 3` once, subject to the normal Version Impact Gate at execution.

## Proof / coverage / scheduling

Existing lossless proof ledgers remain authoritative, with these latest deltas:

- SIRR2 overlay section 8 supersedes affected WP13-38, WP15-16 and listed R080 supporting routes;
- overlay 6 adds shipped scene-route projection evidence to WP-16 claim/currentness/recovery proof and `R018.LIVE` completion;
- overlay 5 controls checkpoint publication eligibility for RD-02, RD-03, RD-05, RD-12, RD-13 and RD-14;
- a focused GREEN result never permits publication while the committed RD module, maintenance audit or full DEV discovery is RED.

## Accounting

```text
ACTIVE_READINESS: 133
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TRIGGER_GATED: 12
NO_WORK: 79
R004: ABSENT
RD_UNITS: 14
```

No current correction creates a readiness identity, RD unit, semantic owner, runtime subsystem or new wave barrier.

## Gate

```text
INDEPENDENT_SENIOR_RE_REVIEW_2: FAIL / REPAIR REQUIRED — SIRR2-001 SIGNIFICANT
SIRR2_001_AUTHOR_REPAIR: PUBLISHED AT PRIOR CHECKPOINT / INDEPENDENTLY UNCONFIRMED
AUTHOR_ADDITIONAL_FINDINGS: 2 SIGNIFICANT — SCENE ROUTE + CHECKPOINT COHERENCE
AUTHOR_ADDITIONAL_REPAIR: ROUTED BY OVERLAYS 5 AND 6
AUTHOR_POST_REPAIR_INVESTIGATION: REQUIRED AFTER PUBLICATION + EXACT-HEAD VALIDATION
HUMAN_PRODUCT_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
