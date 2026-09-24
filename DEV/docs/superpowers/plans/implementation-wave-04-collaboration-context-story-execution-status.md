# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: EXECUTING
CURRENT_TASK: bounded T04A and T07B repairs after independent re-review FAIL
LAST_COMPLETED_TASK: independent re-review of T04A and T07B fix-round-2 on combined HEAD b13496b19bc8a7f11b82a24e11508036e815596f
LAST_SAFE_SHA: b13496b19bc8a7f11b82a24e11508036e815596f — reproducible reviewed repair basis, NOT task acceptance

## Current independent review

REPORT: DEV/docs/superpowers/design/2026-09-24-w04-t04a-t07b-independent-re-review.md
REVIEWED_HEAD: b13496b19bc8a7f11b82a24e11508036e815596f
REVIEWED_PARENT: b16ba8d2b4e3cffa86736fb20d10a34b01c97ff9

| Task | Candidate | Independent disposition |
|---|---|---|
| W04.T04A | 20dd5301310bf5db250c229655ac957fe56e23c3 | FAIL / REPAIR REQUIRED — IRR-T04A-01 and IRR-T04A-02 |
| W04.T07B fix-round-2 | 5a53b8e4323f53cde2f3c718e477003a4da3ce29 | FAIL / REPAIR REQUIRED — IRR-T07B-01 |

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

## Verification and impact

```text
EXACT REVIEWED HEAD: b13496b19bc8a7f11b82a24e11508036e815596f
HOSTED_RUN: 35945179177
HOSTED_JOB: 107461446825
STATUS / CONCLUSION: completed / success
MAINTENANCE: PASS
CANONICAL DEV: Ran 1175 tests; OK (skipped=5)
VERSION_UNCLASSIFIED: []
VERSION_LEGACY_HITS: []
```

The local `.entire/` census issue did not reproduce on hosted CI; the local issue is not claimed repaired. Protected capture files remain untouched.

Candidate version changes remain recorded, not erased: T04A collaboration 1.0.14 -> 1.0.15 with obligation schema v3 unchanged; T07B repair round 2 Story 1.0.3 -> 1.0.4, MECHANICS schema 3 -> 4 and projection-state schema 3 -> 4. Further material repairs require fresh Version Impact assessment; do not reuse an already-spent revision silently.

VERSION_IMPACT: NONE for this review/control-only checkpoint
SYSTEM_IMPACT: no new owner/architecture decision made by this review; findings require bounded implementation/contract repairs
NEXT_EXACT_TASK: repair IRR-T04A-01/02 and IRR-T07B-01 in their existing lanes; focused and cross-owner regressions; coherent publish/read-back and exact-head verification; fresh independent re-review before T04B/T07C
KNOWN_BLOCKERS: independent FAIL on both candidates; T04B/T07C remain blocked; downstream follows the named joins above
UNPUBLISHED_WORK: NONE after verified publication/read-back
WAVE_05: NOT AUTHORIZED

No whole-wave restore, production implementation by the reviewer, migration, release, gameplay bootstrap, new branch/ref or force update is authorized here.

## Detailed historical evidence retention

The rolling cursor is compacted to current state; prior detailed material is retained verbatim in repository history:

```text
path: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story-execution-status.md
commit: b13496b19bc8a7f11b82a24e11508036e815596f
blob: 82560dd4b321a91c9f438401b964bcd6904f6ed3
```

Read that exact snapshot for earlier Source Manifests, System-Impact briefs/rulings, rejected attempts and restores, complete version chains, original CLS preflight evidence and detailed author verification. Those historical states do not override the current disposition above or the stable semantic owners. No separate current proof ledger or executable plan is created.
