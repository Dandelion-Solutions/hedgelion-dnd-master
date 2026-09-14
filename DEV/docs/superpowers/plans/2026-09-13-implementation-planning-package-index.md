# HDM Implementation Planning Package — Index

Status: **AUTHOR POST-SIRR2 CORRECTION ACTIVE — ADVERSARIAL INVESTIGATION CONTINUES**
Date: 2026-09-14

Global gate authority: `DEV/CURRENT_PROGRESS.md`.
Production implementation authorized: **NO**.

## Current routes

Base plans remain RD-01 through RD-14. RD-08, RD-10 and RD-11 use their current v2 plans.

Mandatory overlays, in precedence order:

```text
1. 2026-09-13-implementation-planning-sirr-repair-amendments.md
2. 2026-09-13-implementation-planning-author-self-review-repair-addendum.md
3. 2026-09-13-implementation-planning-author-second-pass-repair-addendum.md
4. 2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md
5. 2026-09-14-implementation-planning-checkpoint-coherence-addendum.md
6. 2026-09-14-implementation-planning-scene-routing-addendum.md
7. 2026-09-14-implementation-planning-wp15-thread-catalog-addendum.md
8. 2026-09-14-implementation-planning-wp17-shipped-consumer-addendum.md
```

Later overlays supersede only exact conflicting execution detail.

## Current applicability

```text
RD-01: overlay 5 checkpoint/test materialization timing
RD-02: prior information repairs + overlay 5 checkpoint timing
RD-03: overlay 5 checkpoint timing
RD-04: seven-selector realization; no Story bootstrap prerequisite
RD-05: overlay 5 checkpoint timing
RD-06: shipped SAVE/PERSISTENCE cutover + exact proof joins
RD-08: temporal owner + overlay 7 mandatory world.thread catalog/classification/structure/identifier/admission/conformance cutover; scene chronology edit precedes RD-09 shared scene edit
RD-09: LIVE lifecycle + SIRR2 CORE/case cutover + overlay 6 scene-route cutover; MULTIPLAYER shared consumer later joins RD-12 overlay 8
RD-12: overlay 5 checkpoint timing + overlay 8 shipped collaboration consumer/proof cutover
RD-13: Dramaturg/Story repairs + overlay 5 checkpoint timing
RD-14: bootstrap repairs + overlay 5 checkpoint timing
```

Overlay 5 is package-wide: a publication checkpoint is invalid if any committed RD test remains intentionally RED, even when the focused subset is GREEN. Explicit repaired instances are RD-01, RD-02, RD-03, RD-05, RD-12, RD-13 and RD-14. RD-04, RD-06, RD-07, RD-08, RD-09, RD-10 and RD-11 were rechecked and do not currently pre-create a later intentional-RED group before an earlier coherent checkpoint.

Overlay 6 makes the shipped scene schema a shared RD-08 -> RD-09 physical surface. Overlay 7 makes canonical `world.thread` catalog debt an explicit coordinated RD-08 cutover rather than conditional discovery.

Overlay 8 closes canonical WP-17 machine-debt item 11. `GAME/CORE/MULTIPLAYER.md` and `GAME/CORE/SESSION.md` now have an executable collaboration consumer checkpoint. MULTIPLAYER remains one shared physical file edit consuming WP-15 chronology, WP-16 LIVE/access and WP-17 collaboration requirements; no second independent writer is introduced. R083 rows for rejoin/frontier/absence/timeout/catch-up/recovery/no-replay also join the shipped projection witness.

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

No current repair changes these identities/counts.

## Gate

```text
INDEPENDENT_SENIOR_RE_REVIEW_2: FAIL / REPAIR REQUIRED
INDEPENDENT_FINDING: SIRR2-001 SIGNIFICANT — author repair independently unconfirmed
AUTHOR_POST_SIRR2_FINDINGS: 5 SIGNIFICANT plan defects found and plan-repaired
  1 scene-route consumer closure
  2 systemic checkpoint/test publication coherence
  3 RD-01 instance missed by the first checkpoint repair
  4 WP-15 world.thread catalog machine cutover was conditional despite canonical known debt
  5 WP-17 shipped CORE/session collaboration alignment had only stale-search coverage, no executable consumer cutover
AUTHOR_POST_REPAIR_INVESTIGATION: ACTIVE
NEXT_INDEPENDENT_REVIEW: BLOCKED UNTIL ZERO-OPEN AUTHOR CLOSURE
HUMAN_PRODUCT_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
