# Wave 04 Execution Status

PLAN: DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md
SPEC: DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md
BASE_SHA: 3319314e5d4a140a9de01cd52bafc6c25a33b975

STATUS: EXECUTING — T04B SYSTEM-IMPACT GATE / T07C INDEPENDENT REVIEW PENDING
CURRENT_TASK: obtain independent re-review of the published T07C IRR-T07C-01/02 candidate; T04B IRR-T04B-02 blocked at the missing accepted W03 producer interface; T05C/T07D remain blocked
LAST_COMPLETED_TASK: T07B independent PASS at a5cd9c517913bcf04d7acfbe895be49cdf941111; T04A prior PASS retained
LAST_SAFE_SHA: f114eb6a38c50d755cf71094d078c1d362f08bb4 — coherent T07C candidate checkpoint published/read back; independent acceptance remains pending


## Current independent review

REPORT: DEV/docs/superpowers/design/2026-09-25-w04-t04b-t07c-independent-review.md
REVIEWED_HEAD: 959de8e2d91e46ff326b046ee39045afa04b952d

| Task | Candidate / repair | Independent disposition |
|---|---|---|
| W04.T04A | accepted prior chain | Prior PASS preserved |
| W04.T04B | 6bb8723ff5ef8f3508d53303ba614d42222393d3 | FAIL / TARGETED_REPAIR_REQUIRED; IRR-T04B-01 CLOSED, IRR-T04B-02 BLOCKING |
| W04.T07B | 55fb0a52a933b90a15ad2bc8b0af624635edaf26 | Prior PASS preserved |
| W04.T07C | f5732ed31c7b3b5288dd43b62bf6847dc96f4702 + 0c5cbc78174ca3545d4342674ba9afe9ae50622c | FAIL / TARGETED_REPAIR_REQUIRED; IRR-T07C-01/02 BLOCKING |

T04B effect-set completeness is independently rederived. Remaining LIVE path proves source close but omits W03 absorption/final-routing from the same W02 closure and accepts CLOSED_UNABSORBED recovery as completed.

T07C copies exact native T0 and publishes atomically, but retained T0 has no historical protection/availability classification and old exact pages are not idempotent once later coverage has advanced.

Exact-head hosted CI: run 36063512416, job 107847776125, maintenance PASS, 1213 tests / 5 skipped, zero version unclassified/legacy hits. New negative witnesses required by this review were not added/run by the reviewer.

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
W04_T0_STORY_READY: NOT ACCEPTED — IRR-T07C-01/02 BLOCKING

No earlier accepted task is reopened. T07C implementation now materializes source-bound T0 EVENT records and layer-local coverage through exact W02 publication; its candidate is not accepted until independent PASS.


## Scheduling and gates

    READY:
      T04B bounded repair of IRR-T04B-02
      T07C bounded repair of IRR-T07C-01/02

    T04B repair -> independent PASS
    T05B + T02C + T04B -> T05C -> T06A -> T06B

    T07C repair -> independent PASS -> T07D -> independent PASS -> T07E
    T07A..T07E -> T07-INTEGRATION independent review

    T04B + T02C + T07-INTEGRATION -> T08A
    T06B + accepted W03 currentness -> T08B
    T08A + T08B + T03A -> T08C
    T08C + all lane checkpoints -> Wave-04 FINAL_REVIEW
    mandatory Senior Wave-04 integration audit -> closure decision

T04B and T07C repairs may execute in parallel while their production/test write sets remain disjoint. Do not start T05C before T04B PASS or T07D before T07C PASS.

MAX_CONFIGURED_HDM_WORKERS: 5
MAX_SAFE_WAVE04_PRODUCTION_WORKERS: 4
REVIEWER_LIMIT: NONE; reviewers do not consume worker slots
SAME_PRODUCTION_OR_PRIMARY_TEST_FILE_WRITERS: SERIALIZED
DEPENDENT_TASK_START: only after exact producer independent PASS is published/read back

OpenCode reviewer/task permission denial remains an environment limitation. Do not change/bypass that permission or self-approve.

## Preserved T04A clarification and T04B obligations

Historical hydration and current admission are distinct. Exact durable accepted associations, authorship, PC association and frozen fingerprints survive author deactivation. An inactive historical author is not by itself a reason to reject historical hydration or cancel an otherwise valid satisfied requirement.

A positively established invalid outstanding required agency or decision opportunity may obsolete the affected generation. Do not remove requirements, synthesize consent/PASS, create an automatic successor, or reinterpret accepted mechanics. Unknown authority/opportunity is a bounded failure, not proof of obsolescence. In the accepted T04A implementation, unavailable singleplayer creator/agency validity raises without producing an OBSOLETE candidate, including for CLOSED state.

The unchanged W03 full-body guard consumes an independently read pinned MANIFEST. Keep that exact-body check; do not substitute the frozen predecessor, a projected access subset or a caller currentness flag.

T04A remains read-only preparation. T04B owns the physical same-campaign-closure authority/obligation/PLAYER-route publication and its complete recovery. Agreement between a carrier's affected IDs and its candidate tuple does not prove effect-set completeness. Repeated/advanced-head recovery must not skip omitted effects.

T04B must preserve Step-5.8 revocation law. The current repair now proves the source close but still omits positive W03 absorption/final-routing from its W02 write-set and accepts CLOSED_UNABSORBED during recovery. Repair the positive same-boundary handoff without creating Collaboration-owned LIVE authority. If W03 exposes no admitted concrete write-set interface, stop at that exact System-Impact producer gap.

## Preserved Story and cross-project limits

All four Story layers and eight source registrations remain mandatory. No baseline SPARSE coverage, false omission of required material, source substitution, reconstruction of native history from Story, or current T1 substitute for retained T0 is authorized.

Accepted M-SEG validation keeps explicit payload owner links, strict positive non-boolean ordinals and exact candidate/segment binding. Structural schema admission need not itself prove cross-field candidate equality; a well-shaped wrong segment remains rejected by Python.

T07B's unconditional rejection of source-classified OMITTED results is not positive proof of native-proven omission support. Preserve that qualification in subsequent source/materialization evidence. A caller MAY_OMIT/reason flag cannot authorize omission. T07B PASS is not whole-Story or whole-Wave integration acceptance.

T07C must preserve retained T0 values together with the historical availability/protection classification needed for later self-contained filtering. Coverage is the idempotency owner: after exact native revalidation, a compatible page wholly at or below persisted coverage is already covered, not a source rewind.

The mandatory pre-T07 CLS-HDM preflight retains its recorded PASS and explicit semantic-change/unavailable-evidence trigger conditions. This review does not repeat it or waive a future genuine trigger. Its exact original refs/blobs remain in CURRENT_PROGRESS and the historical ledger.


## Wave-04 independent-review verification and Version Impact

    REVIEWED_HEAD: 959de8e2d91e46ff326b046ee39045afa04b952d
    T04B_REPAIR_CANDIDATE: 6bb8723ff5ef8f3508d53303ba614d42222393d3
    T07C_FEATURE_COMMIT: f5732ed31c7b3b5288dd43b62bf6847dc96f4702
    T07C_EXACT_PAGE_CORRECTION: 0c5cbc78174ca3545d4342674ba9afe9ae50622c
    HOSTED_RUN: 36063512416
    HOSTED_JOB: 107847776125

CURRENT_VERIFICATION_STATE:
- exact prior reviewed-head hosted run 36063512416/job 107847776125: maintenance PASS, 1213 tests/5 skipped PASS, `VERSION_UNCLASSIFIED=[]`, `VERSION_LEGACY_HITS=[]`; reviewed HEAD was 959de8e2d91e46ff326b046ee39045afa04b952d, not the current repair candidate;
- candidate-focused `.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_rd13_story_t0_commentator`: 75 tests PASS;
- current-status/routing checks `.hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_current_progress_authority DEV.TESTS.test_product_owner_routing_consistency`: 7 tests PASS;
- `DEV/TOOLS/run_maintenance_audit.py`: PASS;
- clean-tree full DEV discovery for code checkpoint `f114eb6a38c50d755cf71094d078c1d362f08bb4` (code unchanged in status-only HEAD `e60e8bf0d9746ea6e9cf3c54847e1e70ba08a246`), using `.hdm-devtools/venv/bin/python -m unittest discover -s /tmp/opencode/hdm-w04-t07c-verify/DEV/TESTS -v`: 1218 tests, 5 skipped, PASS; `VERSION_UNCLASSIFIED=[]`, `VERSION_LEGACY_HITS=[]`. The test tree was the detached clean worktree at the exact published code checkpoint;
- ordinary local checkout full discovery: 1218 tests, 5 skipped, 1 failure because `test_census_has_zero_unclassified_hits` scans the protected local `.entire/logs/entire.log` and reports 68,657 unclassified hits. The dirty-worktree provenance failure cleared after publication. This local census contamination is not claimed repaired;
- changed production Python modules pass Ruff; all changed Python files pass `ruff format --check`. Full changed test-file Ruff check retains two unrelated pre-existing SIM117 warnings at its earlier StoryProjectionTests and StoryRoot tests;
- IRR-T04B-01 CLOSED; IRR-T04B-02 BLOCKED at the exact W03 producer-interface gate;
- IRR-T07C-01/02 repairs are published at the current safe checkpoint; independent re-review and exact-candidate hosted verification remain pending. GitHub CLI is not installed (`gh: command not found`), so current hosted-run evidence is unavailable; do not claim hosted PASS.

VERSION_IMPACT:
- T04B collaboration 1.0.18 remains candidate-only.
- T07C repair: History module 1.0.4 -> 1.0.5; embedded T0 basis schema 1 -> 2; Story module 1.0.7 -> 1.0.8; Story EVENTS unit schema 3 -> 4; E-EVT semantic contract generation 1 -> 2.
- SemanticEvent outer schema remains 1, Story projection-state schema remains 4, and durability module remains 1.0.4; their shapes/owners did not materially change.
- `campaign_contract_generation` remains 2: the changed T0/Story shapes are pre-release, unshipped task candidates; canonical Story/versioning owners require local schema versions and explicitly do not require a pre-release shim solely for an obsolete unshipped shape. No campaign migration was executed. Older T0 schema / Story E-EVT generation values fail closed; any released data found to require conversion needs its own authorized explicit migration/adoption edge before consumption.
- this review/control publication: NONE.

SYSTEM_IMPACT:
- T04B IRR-T04B-02 is BLOCKED at the accepted W03 producer-interface boundary. `access_control.publish_forward_transition(...)` returns a pure closed-source forward view; it does not absorb/final-route the selected source. `live_state.freeze_campaign_absorption(...)` returns a `FrozenCampaignAbsorption.candidate_state`, while accepted absorption classification requires a separate owner-issued CAS acknowledgement tied to that candidate digest. Neither exposes a production W03-owned adapter/write-set composer for incorporating absorption/final routing into T04B's single W02 `path_operations` transaction. Production T04B currently calls only the forward-close proof and its operation builder has no absorption adapter. Implementing that missing composition would require a new/changed W03 boundary outside the T04B write envelope; do not manufacture it in Collaboration or publish CLOSED_UNABSORBED as completed revocation.
- T04B repair stops here; T07C remains independently authorized because its production/test write set is disjoint.

NEXT_EXACT_TASK: obtain independent T07C re-review and exact-candidate hosted verification when that surface is available; do not start T07D before independent PASS. T04B resumes only after the owning W03 producer-interface gap receives an authorized resolution.
KNOWN_BLOCKERS: T05C waits for T04B PASS; T07D waits for T07C PASS. Wave 04 not complete; Wave 05 not authorized.
UNPUBLISHED_WORK: NONE after this verification-status update is published and read back; independent re-review remains pending.

STATUS_UPDATE_VERSION_IMPACT: NONE — documentation-only current-state reconciliation; no version-bearing owner or consumer changed.

## Historical evidence retention

Earlier review/candidate evidence is retained verbatim at this cursor path:

- Commit `959de8e2d91e46ff326b046ee39045afa04b952d`, blob `d12e3bc60a4feb6ba7067526f12f4cf0c86b9236`: submitted T04B/T07C candidates and worker verification evidence.
- Commit `a5cd9c517913bcf04d7acfbe895be49cdf941111`, blob `be512b4f01e745c62b44fdd719b68672749dbe1a`: submitted T04B/T07B candidates, author verification and pre-review gates.
- Commit `3c1a9ca1e31e46f8101944ee668a52bd3d3678ff`, blob `7485d887226b93896c03c71fe64aa6177524afe7`: earlier repair candidates, local verification limitations and previous findings.
- Commit `b13496b19bc8a7f11b82a24e11508036e815596f`, blob `82560dd4b321a91c9f438401b964bcd6904f6ed3`: complete earlier Source Manifests, System-Impact rulings, rejected attempts/restores, version chains, original CLS preflight and author verification.

Those snapshots are historical evidence, not competing current cursors or planning authorities. No whole-wave restore, new host prerequisite, production implementation by the reviewer, migration, release, gameplay bootstrap, new branch/ref or force update is authorized here.
