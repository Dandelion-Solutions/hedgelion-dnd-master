# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: FINAL_REVIEW — bounded T04A and T07B repair candidates ready for independent re-review
CURRENT_TASK: obtain independent PASS for combined repair candidate `dfca9bc45eecc05e2b7287c20954172e7921ffa7`
LAST_COMPLETED_TASK: bounded code/test repairs for IRR-T04A-01/02 and IRR-T07B-01; no acceptance inferred
LAST_SAFE_SHA: 8ca335f969f3ace1623356e1a6c2b835282ef26f — reviewed failure basis; repair candidates supersede its implementation state

## Current independent review

REPORT: DEV/docs/superpowers/design/2026-09-24-w04-t04a-t07b-independent-re-review.md
REVIEWED_HEAD: b13496b19bc8a7f11b82a24e11508036e815596f
REVIEWED_PARENT: b16ba8d2b4e3cffa86736fb20d10a34b01c97ff9

| Task | Candidate | Independent disposition |
|---|---|---|
| W04.T04A | `0d190a9db11129a02f07c71a812996c78a8d33cf` | repair candidate; independent re-review pending |
| W04.T07B fix-round-3 | `0b4dde06d5bdc70fd85b4b6856da45c3f1147d59` + `dfca9bc45eecc05e2b7287c20954172e7921ffa7` | repair candidate; independent re-review pending |

Findings:

- IRR-T04A-01: the W03 full-body guard receives the frozen campaign body as its own current-body evidence; reload the actual current owner body.
- IRR-T04A-02: unknown creator/agency validity for singleplayer is converted to OBSOLETE; uncertainty must remain a bounded failure rather than terminalization without proof.
- IRR-T07B-01: an M-SEG unit with its exact selector only in sources passes Python but fails MECHANICS schema v4; align both validators.

The report distinguishes static counterexamples from tests actually executed by hosted CI. New regression witnesses have not been run by this reviewer.

## Accepted producer checkpoints retained

| Task | Accepted checkpoint / evidence route |
|---|---|
| W04.T00H | Accepted host-composition chain retained in the historical ledger identified below |
| W04.T01A | b50f490cf8dc1d5448cf3ee3c84ce4112e5f8772 |
| W04.T05A | 995924b2a5448dbf9ae4a52555f64de69f7fd699 |
| W04.T01B | 856abcbd6621da33b9ca5ff59413ae7aeb8b3d20 |
| W04.T05B | a1a4d204fbeec9f8a24e681289e0e530e5b91b75 |
| W04.T01C | 7b66ac881aa8a60dd6d03bd97d1ab74e1a96da62 |
| W04.T02A | 5c77aced9dafd9a7f26177090b3e62466b8ec561 |
| W04.T03A | ca3efa3c7750cffc2eef228b4b8666b75828cea9 |
| W04.T00P | 606cf87caeee427622680f8898a6ba1998fb1a9e — accepted later coherent host/History bridge; earlier 595ff95f10d3d48de5748ae32a60d4839106ea2b chain retained |
| W04.T02B | 711738ce20d449a330313f5e51292408d311a616 |
| W04.T07A | 534653babd788d85663dfc2006fbc921ad1577bd |
| W04.T02C | dd0783c4eca20a94431b17844ca09ac64f8ba2cf |

This review does not reopen any of these accepted tasks. It does not accept the two new candidates or mark Wave 04 complete.

## Scheduling and gates

```text
T04A bounded repair -> independent PASS -> T04B
T05B + T02C + T04B -> T05C -> T06A -> T06B

T07B bounded repair -> independent PASS -> T07C -> T07D -> T07E
T07A..T07E -> T07-INTEGRATION independent review

T04B + T02C + T07-INTEGRATION -> T08A
T06B + accepted W03 currentness -> T08B
T08A + T08B + T03A -> T08C
T08C + all lane checkpoints -> Wave-04 FINAL_REVIEW
mandatory Senior Wave-04 integration audit -> closure decision
```

Only the two repair lanes are ready now. They may run in parallel because their primary production/test files are disjoint; do not create artificial work to fill worker slots.

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE; reviewers do not consume worker slots
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after exact producer independent PASS is published/read back

Current OpenCode reviewer-task permission denial is recorded. Do not change/bypass that permission or self-approve a repaired task. If local independent review remains unavailable, publish the candidate and evidence for the independent reviewer; dependent gates remain closed meanwhile.

## Preserved T04A clarification

Historical hydration and current admission are distinct. Exact durable accepted associations, authorship, PC association and frozen fingerprints survive author deactivation. An inactive historical author is not by itself a reason to reject historical hydration or cancel an otherwise valid satisfied requirement.

A positively established invalid outstanding required agency or decision opportunity may obsolete the affected generation. Do not remove its requirements, synthesize consent/PASS, automatically create a successor, or reinterpret accepted mechanics. Unknown authority/opportunity is a bounded failure, not proof of obsolescence. New inputs and recipient-facing catch-up continue to require current authorization and disclosure eligibility.

T04A is read-only candidate reconciliation. T04B owns same-closure authority/obligation/PLAYER-route publication and recovery. The current fixes must not cross that boundary prematurely.

## Preserved Story and cross-project limits

All four Story layers and eight source registrations remain mandatory under the stable plan. No SPARSE baseline coverage, false omission of required material, source-identity substitution, native-history reconstruction from Story, or current T1 substitute for retained T0 is authorized.

T07B currently rejects source-classified OMITTED results unconditionally. This is safe against the old untrusted omission request, but is not positive verification of native-proven omission support. Preserve that qualification in subsequent source/materialization evidence; no caller MAY_OMIT or reason flag may authorize omission.

The mandatory pre-T07 CLS↔HDM preflight remains at its recorded PASS. Its exact evidence and explicit semantic-change/unavailable-evidence reopen conditions are retained in CURRENT_PROGRESS and the prior ledger. This review does not rerun it, treat private planning as evidence, or waive a future genuine trigger.

## Repair-candidate verification and impact

```text
REPAIR_BASE_SHA: 634bed78f4ff211b33632e2a00acf83256fee643
T04A_REPAIR_COMMIT: 0d190a9db11129a02f07c71a812996c78a8d33cf
T07B_REPAIR_COMMITS: 0b4dde06d5bdc70fd85b4b6856da45c3f1147d59, dfca9bc45eecc05e2b7287c20954172e7921ffa7
COMBINED_REPAIR_CANDIDATE_HEAD: dfca9bc45eecc05e2b7287c20954172e7921ffa7
```

CURRENT_VERIFICATION_STATE:
- T04A RED/GREEN: body drift, missing body field, added body field, and unverified
  singleplayer creator/agency cases fail closed without producing an OBSOLETE result;
  positively lost pending required agency still becomes OBSOLETE. OPEN and CLOSED
  uncertainty regressions preserve the exact owner records.
- T07B RED/GREEN: one shared M-SEG fixture table is evaluated by Python and schema v4
  for exact payload/receipt links, absent/empty links, wrong owner and invalid segment
  ordinal. Python retains exact selector-to-candidate matching. JSON Schema validates
  the closed typed-reference shape; it does not replace the Python owner equality check.
- Focused suites: `test_rd12_collaboration` 108 passed; W03
  `PlayerAccessTransitionTests` plus RuntimeHost composition 50 passed;
  `test_rd13_story_t0_commentator` 55 passed.
- Ruff check/format: PASS (the shared RD13 check excludes pre-existing SIM117
  diagnostics only). Maintenance audit: PASS.
- Canonical DEV unittest discovery: 1178 tests, 5 skipped, 1 failure. The remaining
  failure is the version census scanning protected local `.entire/` capture files;
  this tree is untouched. Hosted CI is unavailable for the repair candidates.
- Independent reviewer task dispatch remains denied by OpenCode permissions. No
  independent PASS is claimed; the repair candidates are ready for re-review here.

VERSION_IMPACT:
- Collaboration module `1.0.15 -> 1.0.16`; collaboration obligation schema v3
  unchanged. Story module `1.0.4 -> 1.0.5`; MECHANICS unit schema remains v4 and
  projection-state schema remains v4. No campaign-contract, storage, catalog or engine
  release bump; migration/dual-read remain NONE for the pre-release clean-slate tree.
- This execution-status checkpoint: `VERSION_IMPACT: NONE`.

SYSTEM_IMPACT: NONE — fixes stay within the reviewed T04A/T07B owner/test lanes;
W03 `access_control.py` and RuntimeHost interfaces are unchanged. T04A only reconciles
and returns candidates; T04B retains its same-closure publication and recovery gate.
T07B continues fail-closed for SOURCE_CLASSIFIED omission; no positive native-proof
omission route is asserted. WAVE_05: NOT AUTHORIZED.
NEXT_EXACT_TASK: independently re-review combined repair candidate
`dfca9bc45eecc05e2b7287c20954172e7921ffa7`; start T04B and T07C only after their
respective producer PASS gates.
KNOWN_BLOCKERS: reviewer task permission denied; local full suite census remains
contaminated by protected `.entire/` capture files.
UNPUBLISHED_WORK: NONE after candidate publication/read-back.

No whole-wave restore, production implementation by the reviewer, migration, release, gameplay bootstrap, new branch/ref or force update is authorized here.

## Detailed historical evidence retention

The rolling cursor is compacted to current state; prior detailed material is retained verbatim in repository history:

```text
path: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story-execution-status.md
commit: b13496b19bc8a7f11b82a24e11508036e815596f
blob: 82560dd4b321a91c9f438401b964bcd6904f6ed3
```

Read that exact snapshot for earlier Source Manifests, System-Impact briefs/rulings, rejected attempts and restores, complete version chains, original CLS preflight evidence and detailed author verification. Those historical states do not override the current disposition above or the stable semantic owners. No separate current proof ledger or executable plan is created.
