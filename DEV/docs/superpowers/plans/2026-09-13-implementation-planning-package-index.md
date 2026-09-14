# HDM Implementation Planning Package — Index

Status: **AUTHOR POST-SIRR2 CORRECTION ACTIVE — ADVERSARIAL INVESTIGATION CONTINUES**
Date: 2026-09-14

Global gate authority: `DEV/CURRENT_PROGRESS.md`.
Production implementation authorized: **NO**.

## Current routes

Base plans remain RD-01 through RD-14. RD-08, RD-10 and RD-11 use their current v2 plans.

Mandatory overlays, later precedence first only for exact conflicting detail:

```text
1. 2026-09-13-implementation-planning-sirr-repair-amendments.md
2. 2026-09-13-implementation-planning-author-self-review-repair-addendum.md
3. 2026-09-13-implementation-planning-author-second-pass-repair-addendum.md
4. 2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md
5. 2026-09-14-implementation-planning-checkpoint-coherence-addendum.md
6. 2026-09-14-implementation-planning-scene-routing-addendum.md
```

Current applicability:

```text
RD-01: overlay 5 checkpoint/test materialization timing
RD-02: prior information repairs + overlay 5 checkpoint timing
RD-03: overlay 5 checkpoint timing
RD-04: seven-selector realization; no Story bootstrap prerequisite
RD-05: overlay 5 checkpoint timing
RD-06: shipped SAVE/PERSISTENCE cutover + proof joins
RD-08: temporal owner; scene chronology edit precedes RD-09 shared scene edit
RD-09: LIVE lifecycle + SIRR2 CORE/case cutover + overlay 6 scene route cutover
RD-12: overlay 5 checkpoint timing
RD-13: Dramaturg/Story repairs + overlay 5 checkpoint timing
RD-14: bootstrap repairs + overlay 5 checkpoint timing
```

Overlay 5 is package-wide: a publication checkpoint is invalid if any committed RD test remains intentionally RED, even when the focused subset is GREEN. Explicit repaired instances are RD-01, RD-02, RD-03, RD-05, RD-12, RD-13 and RD-14. RD-04, RD-06, RD-07, RD-08, RD-09, RD-10 and RD-11 were rechecked and do not currently pre-create a later intentional-RED group before an earlier coherent checkpoint.

Overlay 6 makes the shipped scene schema a shared RD-08 -> RD-09 physical surface. RD-08 removes chronology-frontier debt first; RD-09 then narrows the LIVE pointer to route nomination under typed claim/currentness semantics. The coordinated clean-slate scene contract plans one local schema increment, subject to the normal execution-time Version Impact Gate.

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

## Gate

```text
INDEPENDENT_SENIOR_RE_REVIEW_2: FAIL / REPAIR REQUIRED
INDEPENDENT_FINDING: SIRR2-001 SIGNIFICANT — author repair independently unconfirmed
AUTHOR_POST_SIRR2_FINDINGS: 3 SIGNIFICANT plan defects found and plan-repaired
  1 scene-route consumer closure
  2 systemic checkpoint/test publication coherence
  3 RD-01 instance missed by the first checkpoint repair
AUTHOR_POST_REPAIR_INVESTIGATION: ACTIVE
NEXT_INDEPENDENT_REVIEW: BLOCKED UNTIL ZERO-OPEN AUTHOR CLOSURE
HUMAN_PRODUCT_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
