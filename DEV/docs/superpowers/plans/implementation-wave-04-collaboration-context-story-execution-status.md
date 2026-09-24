# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: EXECUTING
CURRENT_TASK: bounded T04B recovery/LIVE-barrier repair and W04.T07C Story-local T0/currentness/publication
LAST_COMPLETED_TASK: T07B independent re-review PASS at a5cd9c517913bcf04d7acfbe895be49cdf941111; T04B independently reviewed FAIL
LAST_SAFE_SHA: a5cd9c517913bcf04d7acfbe895be49cdf941111 — exact reviewed state; T07B accepted, T04B remains unaccepted

## Current independent review

REPORT: DEV/docs/superpowers/design/2026-09-24-w04-t04b-t07b-independent-review.md
REVIEWED_HEAD: a5cd9c517913bcf04d7acfbe895be49cdf941111
REVIEWED_PARENT: 55fb0a52a933b90a15ad2bc8b0af624635edaf26

| Task | Candidate / repair | Independent disposition |
|---|---|---|
| W04.T04A | 20dd5301310bf5db250c229655ac957fe56e23c3 + 0d190a9db11129a02f07c71a812996c78a8d33cf | Prior PASS preserved; IRR-T04A-01/02 CLOSED |
| W04.T04B | f0ba25f34cb60d9b9f0019bcbb414bc6e97b2372 | FAIL / TARGETED_REPAIR_REQUIRED; IRR-T04B-01/02 BLOCKING |
| W04.T07B | 55fb0a52a933b90a15ad2bc8b0af624635edaf26 | PASS / GO; IRR-T07B-02 CLOSED |

T07B now checks an actual positive integer ordinal, explicitly excluding bool, before exact segment selector comparison. Its resolution/receipt boolean cases, nonpositive ordinal cases and retained semantic-binding tests ran successfully in exact-head hosted CI. The earlier explicit payload-link repair is retained.

T04B findings:

- IRR-T04B-01: direct recovery and the advanced-head publish path validate only the carrier-supplied obligation set. A mutually consistent empty/subset carrier can omit affected obligations and route cleanup from recovery proof. Revalidate the complete effect set from existing exact native/publication evidence; preserve bounded cold recovery.
- IRR-T04B-02: T04B physically publishes a W03 transition without enforcing its required LIVE revocation/freeze/forward barrier. Consume applicable existing W03 owner proof and same-boundary closure; unavailable/partial proof must stop before a campaign write or success acknowledgement.

These are exact-code/contract findings with required new RED witnesses, not claims that the reviewer ran those new repository tests. The existing hosted suite was independently read and verified. No production, executable tests or schemas were changed by the review.

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
| W04.T00P | 606cf87caeee427622680f8898a6ba1998fb1a9e — accepted coherent host/History bridge; earlier 595ff95f10d3d48de5748ae32a60d4839106ea2b chain retained |
| W04.T02B | 711738ce20d449a330313f5e51292408d311a616 |
| W04.T07A | 534653babd788d85663dfc2006fbc921ad1577bd |
| W04.T02C | dd0783c4eca20a94431b17844ca09ac64f8ba2cf |
| W04.T04A | 0d190a9db11129a02f07c71a812996c78a8d33cf — independently accepted at combined reviewed HEAD 3c1a9ca1e31e46f8101944ee668a52bd3d3678ff |
| W04.T07B | 55fb0a52a933b90a15ad2bc8b0af624635edaf26 — independently accepted at combined reviewed HEAD a5cd9c517913bcf04d7acfbe895be49cdf941111; prior source-contract repair chain retained |

W04_AUTHORITY_COLLAB_RECONCILIATION_READY: ACCEPTED
W04_AUTHORITY_COLLABORATION_RECONCILED: NOT ACCEPTED
W04_STORY_SOURCE_CONTRACTS_READY: ACCEPTED

No earlier accepted task is reopened. T07C is authorized from its reviewed producer; it is not implemented or accepted by this review.

## Scheduling and gates

```text
READY:
  T04B bounded repair of IRR-T04B-01/02
  T07C from accepted T07B

T04B repair -> independent PASS
T05B + T02C + T04B -> T05C -> T06A -> T06B

T07C -> independent PASS -> T07D -> independent PASS -> T07E
T07A..T07E -> T07-INTEGRATION independent review

T04B + T02C + T07-INTEGRATION -> T08A
T06B + accepted W03 currentness -> T08B
T08A + T08B + T03A -> T08C
T08C + all lane checkpoints -> Wave-04 FINAL_REVIEW
mandatory Senior Wave-04 integration audit -> closure decision
```

T04B repair and T07C may execute in parallel while their production/test write sets are disjoint. Do not manufacture work to fill slots. T05C remains blocked on T04B; Story tasks remain serialized by their producer reviews and shared RD13 test owner.

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE; reviewers do not consume worker slots
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after exact producer independent PASS is published/read back

OpenCode reviewer-task permission denial remains an environment limitation. Do not change/bypass that permission or self-approve. If local independent review remains unavailable, publish each coherent candidate and evidence for independent review here; dependent gates remain closed meanwhile.

## Preserved T04A clarification and T04B obligations

Historical hydration and current admission are distinct. Exact durable accepted associations, authorship, PC association and frozen fingerprints survive author deactivation. An inactive historical author is not by itself a reason to reject historical hydration or cancel an otherwise valid satisfied requirement.

A positively established invalid outstanding required agency or decision opportunity may obsolete the affected generation. Do not remove requirements, synthesize consent/PASS, create an automatic successor, or reinterpret accepted mechanics. Unknown authority/opportunity is a bounded failure, not proof of obsolescence. In the accepted T04A implementation, unavailable singleplayer creator/agency validity raises without producing an OBSOLETE candidate, including for CLOSED state.

The unchanged W03 full-body guard consumes an independently read pinned MANIFEST. Keep that exact-body check; do not substitute the frozen predecessor, a projected access subset or a caller currentness flag.

T04A remains read-only preparation. T04B owns the physical same-campaign-closure authority/obligation/PLAYER-route publication and its complete recovery. Agreement between a carrier's affected IDs and its candidate tuple does not prove effect-set completeness. Repeated/advanced-head recovery must not skip omitted effects.

T04B must also preserve the existing Step-5.8 revocation law: required exact LIVE source closure precedes the campaign authority change; required absorption/finalization and route changes share the corresponding campaign boundary. A prepared W03 after-view or successful W02 Git write cannot replace owner-bound final-source proof. Partial/unavailable proof fails before the write. W03 remains a read-only producer; a safe rejection alone does not prove positive LIVE-sensitive closure support.

## Preserved Story and cross-project limits

All four Story layers and eight source registrations remain mandatory. No baseline SPARSE coverage, false omission of required material, source substitution, reconstruction of native history from Story, or current T1 substitute for retained T0 is authorized.

Accepted M-SEG validation keeps explicit payload owner links, strict positive non-boolean ordinals and exact candidate/segment binding. Structural schema admission need not itself prove cross-field candidate equality; a well-shaped wrong segment remains rejected by Python.

T07B's unconditional rejection of source-classified OMITTED results is not positive proof of native-proven omission support. Preserve that qualification in subsequent source/materialization evidence. A caller MAY_OMIT/reason flag cannot authorize omission. T07B PASS is not whole-Story or whole-Wave integration acceptance.

The mandatory pre-T07 CLS-HDM preflight retains its recorded PASS and explicit semantic-change/unavailable-evidence trigger conditions. This review does not repeat it or waive a future genuine trigger. Its exact original refs/blobs remain in CURRENT_PROGRESS and the historical ledger.

## Verification and Version Impact

```text
T04B_CANDIDATE_COMMIT: f0ba25f34cb60d9b9f0019bcbb414bc6e97b2372
T07B_ACCEPTED_REPAIR: 55fb0a52a933b90a15ad2bc8b0af624635edaf26
REVIEWED_HEAD: a5cd9c517913bcf04d7acfbe895be49cdf941111
HOSTED_RUN: 35988891445
HOSTED_JOB: 107597978376
STATUS / CONCLUSION: completed / success
MAINTENANCE: PASS
CANONICAL DEV: Ran 1186 tests; OK (skipped=5)
VERSION_UNCLASSIFIED: []
VERSION_LEGACY_HITS: []
```

Independent hosted evidence includes the eight new T04B tests, retained T04A cases and the shared boolean-ordinal regression table. The green suite does not cover the new T04B counterexamples described in the report; those remain required repair REDs.

The author's focused checks remain recorded: RD12 116, cross-owner W03/RuntimeHost/W02 90, RD13 55; Ruff check/format and maintenance PASS, with existing RD13 SIM117 excluded from the optional Ruff check. The author-local full run reported one protected `.entire/` version-census failure. That failure did not reproduce in the clean exact-head hosted run. No local capture data, permission or census behavior is claimed repaired by this review.

VERSION_IMPACT:
- T07B Story module `1.0.5 -> 1.0.6` accepted; MECHANICS schema v4 and projection-state v4 unchanged. No campaign-contract, storage, catalog or engine bump; no migration/dual-read.
- T04B collaboration module `1.0.16 -> 1.0.17` remains the submitted unaccepted candidate; obligation schema v3 unchanged. Further material repair requires a fresh Version Impact Gate.
- This review/control checkpoint: `VERSION_IMPACT: NONE`.

SYSTEM_IMPACT: no new owner decision. T04B must enforce existing complete-recovery and W03 LIVE-boundary obligations; ordinary in-scope repair is authorized. If an actually missing accepted producer interface prevents it, record that specific gap before crossing the owner boundary.
NEXT_EXACT_TASK: repair IRR-T04B-01/02 and execute T07C in disjoint lanes; obtain their respective independent review before dependent work.
KNOWN_BLOCKERS: IRR-T04B-01/02 block T04B/T05C. OpenCode reviewer permission and local `.entire/` census interaction remain environment limitations; do not bypass them.
UNPUBLISHED_WORK: NONE after this review/control publication and read-back.
WAVE_04: NOT COMPLETE
WAVE_05: NOT AUTHORIZED

## Historical evidence retention

Earlier review/candidate evidence is retained verbatim at this cursor path:

- Commit `a5cd9c517913bcf04d7acfbe895be49cdf941111`, blob `be512b4f01e745c62b44fdd719b68672749dbe1a`: submitted T04B/T07B candidates, author verification and pre-review gates.
- Commit `3c1a9ca1e31e46f8101944ee668a52bd3d3678ff`, blob `7485d887226b93896c03c71fe64aa6177524afe7`: earlier repair candidates, local verification limitations and previous findings.
- Commit `b13496b19bc8a7f11b82a24e11508036e815596f`, blob `82560dd4b321a91c9f438401b964bcd6904f6ed3`: complete earlier Source Manifests, System-Impact rulings, rejected attempts/restores, version chains, original CLS preflight and author verification.

Those snapshots are historical evidence, not competing current cursors or planning authorities. No whole-wave restore, new host prerequisite, production implementation by the reviewer, migration, release, gameplay bootstrap, new branch/ref or force update is authorized here.
