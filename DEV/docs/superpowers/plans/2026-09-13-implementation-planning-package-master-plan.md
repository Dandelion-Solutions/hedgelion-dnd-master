# HDM Implementation Planning Package — Master Plan

Status: **AUTHOR SECOND-PASS REPAIR ACTIVE — THIRD PASS REQUIRED BEFORE INDEPENDENT RE-REVIEW #2**
Date: 2026-09-13

Fixed accounting: 133 active = 116 direct + 9 pure proof + 8 composite parents; 12 trigger-gated; 79 no-work; R004 absent; 14 RD units. Production implementation: **NO**.

```text
PB-01..PB-07 planning package                  COMPLETE / current routes overlaid by accepted repairs
first independent Senior review                FAIL / REPAIR REQUIRED
SIP-001..SIP-011 author repair                 COMPLETE
first independent Senior re-review             FAIL / REPAIR REQUIRED — SIRR-001..005
SIRR author repair                             COMPLETE / independently unconfirmed
first author adversarial self-review           FAIL — ASR-001..003
first author self-review repair checkpoint     db23d097abfb9a2cfdbeb88b115689566a575bed / CI PASS
second author adversarial pass                 FAIL — ASR-004..005
current second-pass repair                     AUTHORED / PUBLICATION+THIRD-PASS VERIFICATION REQUIRED
independent Senior re-review #2                NOT YET READY
```

## Cursor

```text
PLANNING_PACKAGE_STATE: AUTHOR_SECOND_PASS_REPAIR_ACTIVE
CURRENT_BLOCK: ASR-004/ASR-005 REPAIR PUBLICATION AND THIRD-PASS VERIFICATION
LAST_COMPLETED_BLOCK: SECOND AUTHOR PASS FOUND ASR-004..ASR-005
NEXT_AUTHORIZED_BLOCK: PUBLISH CURRENT REPAIR -> FRESH READ-BACK/DIFF/HOSTED VALIDATION -> AUTHOR THIRD-PASS ADVERSARIAL REVIEW ONLY
FIRST_SELF_REVIEW_REPAIR_CHECKPOINT: db23d097abfb9a2cfdbeb88b115689566a575bed
FIRST_SELF_REVIEW_REPAIR_CI: Validate engine source run 34785919811 PASS
FIRST_SELF_REVIEW_FINDINGS: DEV/docs/superpowers/plans/2026-09-13-implementation-planning-author-self-review-findings.md
FIRST_SELF_REVIEW_ADDENDUM: DEV/docs/superpowers/plans/2026-09-13-implementation-planning-author-self-review-repair-addendum.md
SECOND_PASS_FINDINGS: DEV/docs/superpowers/plans/2026-09-13-implementation-planning-author-second-pass-findings.md
SECOND_PASS_ADDENDUM: DEV/docs/superpowers/plans/2026-09-13-implementation-planning-author-second-pass-repair-addendum.md

RD_PLANS_BASE_COMPLETE: 14 / 14
CURRENT_MANDATORY_OVERLAYS: SIRR + first self-review + second-pass where applicable
AFFECTED_RD_OVERLAY: RD-02,RD-04,RD-06,RD-09,RD-13,RD-14
DIRECT_LEAVES_PLANNED: 116 / 116
PURE_PROOF_ROUTES: 9 / 9
COMPOSITE_PARENT_ROUTES: 8 / 8
WP12_PROOF_ROWS: 17 / 17 CURRENT ROUTED
WP13_PROOF_ROWS: 38 / 38 CURRENT ROUTED
TRIGGER_GATED_PRESERVED: 12 / 12
NO_WORK_PRESERVED: 79 / 79
FIRST_AUTHOR_FINDINGS: ASR-001..ASR-003
SECOND_AUTHOR_FINDINGS: ASR-004..ASR-005
AUTHOR_THIRD_PASS: REQUIRED / PENDING
INDEPENDENT_SENIOR_RE_REVIEW_2: BLOCKED UNTIL AUTHOR THIRD-PASS CLOSURE
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

## Current package authority

- Global gate: `DEV/CURRENT_PROGRESS.md`.
- Worker route index: `2026-09-13-implementation-planning-package-index.md`.
- Base RD routes: current RD-01..RD-14 listed by package index.
- Mandatory overlays in order:
  1. `2026-09-13-implementation-planning-sirr-repair-amendments.md`;
  2. `2026-09-13-implementation-planning-author-self-review-repair-addendum.md`;
  3. `2026-09-13-implementation-planning-author-second-pass-repair-addendum.md`.
- Base scheduling: `2026-09-13-implementation-planning-execution-waves.md` plus current overlays/addenda.
- Current coverage: `2026-09-13-implementation-planning-bidirectional-coverage-v2.md` plus both author self-review addenda.
- Current proof control: `2026-09-13-implementation-planning-lossless-proof-ledger-v2.md` and current v2 appendices.

## Current repair boundaries

ASR-001 remains corrected to the seven-selector WP-11 MANIFEST/schema contract with local campaign manifest schema `4 -> 5`, but ASR-005 refines that repair: static `story_root` validity does not require Story materialization at bootstrap.

ASR-002 remains corrected: player-local Dramaturg supports `ABSENT | BOUND`; only BOUND carries an exact shared generation.

ASR-003 remains corrected: WP12/WP13 proof supporting owners and gameplay transport authority are explicit.

ASR-004 pins exact Story physical routing already selected by WP-11/WP-18:
```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```
with no worker-selected alternative partition.

ASR-005 removes the first self-review's accidental Story startup prerequisite. RD-04 may close the static selector/schema contract without Story files; RD-13 materializes Story on demand; RD-14 validates all selectors while proving blank New Game/PLAY_READY does not require Story/T0 files.

No runtime implementation has begun. No author-side repair can substitute for the mandatory independent Senior verdict.
