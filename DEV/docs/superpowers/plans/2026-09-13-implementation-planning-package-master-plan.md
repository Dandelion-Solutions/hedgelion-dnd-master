# HDM Implementation Planning Package — Master Plan

Status: **POST-SIRR2 AUTHOR CORRECTION PUBLISHED — VERIFICATION / ADVERSARIAL CLOSURE REQUIRED**
Date: 2026-09-14

Fixed accounting remains: 133 active = 116 direct + 9 pure proof + 8 composite parents; 12 trigger-gated; 79 no-work; R004 absent; 14 RD units. Production implementation: **NO**.

```text
PB-01..PB-07 planning package                  COMPLETE / current routes overlaid by repairs
first independent Senior review                FAIL / REPAIR REQUIRED
first independent Senior re-review             FAIL / REPAIR REQUIRED — SIRR-001..005
independent Senior re-review #2                FAIL / REPAIR REQUIRED — SIRR2-001 SIGNIFICANT
SIRR2 shipped-consumer repair                  PUBLISHED / independently unconfirmed
author post-SIRR2 investigation                FOUND 2 SIGNIFICANT plan gaps
scene-route repair                             PUBLISHED AS MANDATORY OVERLAY
checkpoint-coherence repair                    PUBLISHED AS MANDATORY OVERLAY
post-repair exact-head verification            REQUIRED
post-repair author adversarial closure         REQUIRED
next independent Senior review                 BLOCKED UNTIL ZERO-OPEN AUTHOR CLOSURE
```

## Cursor

```text
PLANNING_PACKAGE_STATE: POST_SIRR2_AUTHOR_CORRECTION_PUBLISHED
CURRENT_BLOCK: VERIFY CURRENT CORRECTION HEAD + AUTHOR ADVERSARIAL CLOSURE
LAST_COMPLETED_BLOCK: ROUTE/PUBLISH SCENE-ROUTE AND CHECKPOINT-COHERENCE REPAIRS
NEXT_AUTHORIZED_BLOCK: EXACT-HEAD READBACK/CI -> AUTHOR POST-REPAIR ADVERSARIAL REVIEW ONLY
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

## Current package authority

- Global gate: `DEV/CURRENT_PROGRESS.md`.
- Worker/reviewer route index: `2026-09-13-implementation-planning-package-index.md`.
- Base RD routes: current RD-01..RD-14 from that index.
- Mandatory overlays, in precedence order:
  1. `2026-09-13-implementation-planning-sirr-repair-amendments.md`;
  2. `2026-09-13-implementation-planning-author-self-review-repair-addendum.md`;
  3. `2026-09-13-implementation-planning-author-second-pass-repair-addendum.md`;
  4. `2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md`;
  5. `2026-09-14-implementation-planning-checkpoint-coherence-addendum.md`;
  6. `2026-09-14-implementation-planning-scene-routing-addendum.md`.

## Author investigation disposition

The post-SIRR2 investigation confirmed two additional Significant planning defects and repaired both at plan level.

### Scene-route consumer closure

Canonical WP-16 explicitly names shipped `scene.schema.yaml` scene-wide LIVE-pointer semantics as machine debt. The current package now assigns a real shared physical checkpoint:

```text
RD-08 scene chronology alignment
-> fresh scene bytes
-> RD-09 scene LIVE-route narrowing
```

The scene pointer nominates routing only. Typed claim/currentness determines authority for each target native owner/partition; unclaimed owners remain campaign-routed. The coordinated pre-v1 scene contract changes local schema version `2 -> 3` once, subject to the normal execution-time Version Impact Gate.

### Checkpoint/test coherence

RD-02, RD-03, RD-05, RD-12, RD-13 and RD-14 no longer treat future-task RED groups as something that may already exist in a publishable earlier checkpoint. The latest overlay moves each later group to its owning task/stage and requires the complete committed RD test module, maintenance audit and full DEV unittest discovery to be GREEN at a publication boundary. Focused GREEN cannot override broader RED.

This repair changes no accepted semantic owner, readiness identity, decomposition unit, trigger/no-work classification or runtime implementation.

## Current verification obligation

The published correction is not an author PASS yet. Before independent handoff the author must:

1. read back the exact published overlays and control files;
2. verify the correction diff contains planning/control artifacts only;
3. require hosted maintenance audit + full DEV unittest success on the exact correction HEAD;
4. repeat the bounded WP-15/WP-16/WP-17 consumer/debt and proof-route sweep;
5. repeat the six-RD checkpoint-coherence challenge against the actual latest overlay precedence;
6. record zero-open BLOCKING/SIGNIFICANT/MINOR author closure or repair any new defect first.

```text
HUMAN_PRODUCT_DECISION_REQUIRED: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
SUBSTANTIVE_IMPLEMENTATION_STARTED: NO
MIGRATION_EXECUTION_STARTED: NO
RELEASE_EXECUTION_STARTED: NO
GAMEPLAY_BOOTSTRAP_STARTED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
