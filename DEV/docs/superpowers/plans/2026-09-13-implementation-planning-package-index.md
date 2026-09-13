# HDM Implementation Planning Package — Index

Status: **SIRR AUTHOR REPAIR COMPLETE / AWAITING GENUINELY INDEPENDENT SENIOR RE-REVIEW #2**
Date: 2026-09-13

Global gate authority: `DEV/CURRENT_PROGRESS.md`.
Current author repair checkpoint: `87941ed63028efea71eb38e03375573e31a70be2`.
Current repair disposition: `2026-09-13-implementation-planning-senior-re-review-repair-disposition.md`.
Current repair closure: `2026-09-13-implementation-planning-senior-re-review-repair-closure.md`.
Current re-review instructions: `2026-09-13-implementation-planning-senior-re-review-2-brief.md`.
Previous independent finding authority: `2026-09-13-implementation-planning-independent-senior-re-review-result.md`.

## Package provenance

```text
PB-01 control/conventions/template/Impact-TDD/index
PB-02 source manifest + RD-01..RD-04 + closure
PB-03 source manifest + RD-05..RD-08 + closure
PB-04 source manifest + RD-09..RD-11 + closure
PB-05 source manifest + RD-12..RD-14 + closure
PB-06 execution waves/integration
PB-07 bidirectional coverage/currentness
first independent Senior review -> FAIL / REPAIR REQUIRED
SIP-001..SIP-011 author repair -> COMPLETE
first independent Senior re-review -> FAIL / REPAIR REQUIRED (SIRR-001..005)
SIRR-001..SIRR-005 author repair -> COMPLETE at 87941ed63028efea71eb38e03375573e31a70be2
current gate -> genuinely independent Senior re-review #2
```

## Current RD-plan routes

Base plans:
```text
RD-01 2026-09-13-RD-01-shipped-stale-projection-repairs-plan.md
RD-02 2026-09-13-RD-02-information-knowledge-disclosure-message-plan.md
RD-03 2026-09-13-RD-03-actor-asset-effect-continuity-plan.md
RD-04 2026-09-13-RD-04-owner-native-routing-index-hot-plan.md
RD-05 2026-09-13-RD-05-deterministic-execution-fixed-rng-plan.md
RD-06 2026-09-13-RD-06-save-durability-publication-plan.md
RD-07 2026-09-13-RD-07-current-native-recovery-checkpoint-plan.md
RD-08 2026-09-13-RD-08-temporal-thread-current-state-plan-v2.md
RD-09 2026-09-13-RD-09-principal-live-currentness-plan.md
RD-10 2026-09-13-RD-10-role-handoff-protected-emission-plan-v2.md
RD-11 2026-09-13-RD-11-context-runtime-plan-v2.md
RD-12 2026-09-13-RD-12-collaboration-multiplayer-plan.md
RD-13 2026-09-13-RD-13-story-t0-commentator-history-plan.md
RD-14 2026-09-13-RD-14-bootstrap-onboarding-product-plan.md
```

Mandatory current overlay:
```text
2026-09-13-implementation-planning-sirr-repair-amendments.md
```

Overlay applicability:
```text
RD-02: SIRR-005 close/absorb integration wording/tests
RD-06: SIRR-001/SIRR-003 proof + shipped SAVE/publication consumer cutover
RD-09: SIRR-005 two-phase close/absorb semantics/tests
RD-13: SIRR-002 Dramaturg publication/admission/rebase + SIRR-004 Story selector
RD-14: SIRR-003 exact generator consumer synchronization + Story selector scaffold proof
```

For those five RDs the executable route is **base plan + mandatory overlay**. The overlay does not supersede unchanged base-plan content. Earlier RD-08/RD-10/RD-11 files without `-v2` remain superseded provenance.

## Current execution scheduling

```text
BASE: 2026-09-13-implementation-planning-execution-waves.md
MANDATORY ADDENDUM: 2026-09-13-implementation-planning-execution-waves-sirr-repair-addendum.md
```

The addendum repairs R071 completion, Story-selector/generator join, E11 retained Dramaturg publication/admission and CLOSED_UNABSORBED wording without adding a whole-wave barrier.

## Current lossless proof routes

```text
2026-09-13-implementation-planning-lossless-proof-ledger-v2.md
2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13-v2.md
2026-09-13-implementation-planning-lossless-proof-ledger-wp14-wp15.md
2026-09-13-implementation-planning-lossless-proof-ledger-wp16-wp17.md
```

Historical `...lossless-proof-ledger.md` and `...wp12-wp13.md` are superseded for current routing. The v2 WP-12/WP-13 appendix owns exact semantic mapping of all 17/38 duties.

Planned package witness target remains:
```text
DEV/TESTS/test_implementation_proof_ledger.py
```

## Current coverage/currentness route

```text
2026-09-13-implementation-planning-bidirectional-coverage-v2.md
```

It preserves:
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

## Current review/control route

```text
FINDINGS:
  2026-09-13-implementation-planning-independent-senior-re-review-result.md

AUTHOR REPAIR:
  2026-09-13-implementation-planning-senior-re-review-repair-disposition.md
  2026-09-13-implementation-planning-senior-re-review-repair-closure.md

NEXT INDEPENDENT REVIEW:
  2026-09-13-implementation-planning-senior-re-review-2-brief.md
```

The repair checkpoint was read back from remote state and exact-head GitHub Actions `Validate engine source` succeeded. These author-side checks do not substitute for independent Senior review.

## Gate accounting

```text
SIRR_FINDINGS: 5
AUTHOR_SIRR_DISPOSITION: 5 / 5 REPAIRED FOR REVIEW
SEMANTIC_OWNER_DRIFT_DURING_SIRR_REPAIR: NONE FOUND
DECOMPOSITION_REOPEN: NOT REQUIRED
HUMAN_PRODUCT_DECISION_REQUIRED: NO
NEXT_AUTHORIZED_UNIT: GENUINELY INDEPENDENT SENIOR RE-REVIEW #2 ONLY
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

No implementation worker may start from this index until the next independent Senior result is `PASS / GO` and `DEV/CURRENT_PROGRESS.md` advances accordingly.
