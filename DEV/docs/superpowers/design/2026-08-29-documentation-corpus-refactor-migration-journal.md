# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — SEMANTIC CENSUS COMPLETE / REFERENCE_SET_PROVEN / DCR CLOSURE VERIFIED / CLEANUP COMPLETE / WP-07 NOT STARTED**
Date: 2026-08-29
Proof/source branch: `v1/engine-rearchitecture`
Execution branch: `v1/documentation-refactor`

This file is an operational continuation surface, not semantic authority. Item-level dispositions are owned by the research census and the durable `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md` series. Conflict/debt status is the base register plus its current amendments.

## Current cursor

```text
PRE_REFACTOR_SPECS_BASELINE: 375
SPECS_FULL_CONTENT_REVIEWED: 375
SPECS_REMAINING_UNREVIEWED: 0
FINAL_DESIGN_DESTINATIONS: 333
SPECS_TO_RESEARCH_DESTINATIONS: 1
FINAL_CURRENT_SPEC_OR_OWNER_DESTINATIONS: 41
PENDING_FINAL_SUPERSESSION_CHECK: 0
PHYSICAL_MOVES_PERFORMED: 370 / 370
PHYSICAL_MOVES_REMAINING: 0
PATH_REPAIRS_APPLIED: 503 / 503 occurrences
PATH_REPAIRS_REMAINING: 0 occurrences
EXTRACTIONS_PUBLISHED: 1 / 1
REFERENCE_AUDIT_GATE: SATISFIED / REFERENCE_SET_PROVEN
CURRENT_DURABLE_SEMANTIC_CHECKPOINT: Specs Census Part 61
PART_61_PUBLICATION_SHA: 78731e310cd9eae3d7870c2f5c4743ca17d459ad
CONFLICT_STATUS_AMENDMENT_01_SHA: a6531e9bf9477dc4bcd9b624119d3fbfe09e0690
REFERENCE_SET_PROOF: DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-reference-set-proof.md
REFERENCE_SET_PROOF_SHA: 694ca8e203ea813cb5b27033b5570db4d6a82bbb
LAST_PHYSICAL_MIGRATION_CHECKPOINT: 01e6e0072358db75b1ebea91290c51471c9bed9c
ZERO_REPAIR_CLASS: 102 / 102 COMPLETE
R015_SPLIT_CHECKPOINT: 65c66fdd17e75e83357e540b7ba4d0228c48cf3a
```

Part 61, conflict-register Amendment 01 and the branch-complete reference-set proof have remote publication evidence. Physical migration is now in progress on `v1/documentation-refactor`; the frozen semantic census and reference proof remain the execution authority for the move/repair set.

Frozen baseline date closure:

```text
2026-08-18: COMPLETE
2026-08-19: COMPLETE / FINAL SUPERSESSION CHECKS RESOLVED
2026-08-20: COMPLETE
2026-08-21: 45 / 45 COMPLETE
2026-08-23: 3 / 3 COMPLETE
2026-08-24: 57 / 57 COMPLETE
2026-08-25: 55 / 55 COMPLETE
2026-08-26: 26 / 26 COMPLETE
2026-08-27: 18 / 18 COMPLETE
2026-08-28: 18 / 18 COMPLETE
2026-08-29: 1 / 1 COMPLETE
TOTAL: 375 / 375 FULL-CONTENT REVIEWED
```

Unique-source correction remains in force: S-118 is the Step-5.14 canonical final; S-200 is `2026-08-21-step-6-pre-design-framing-working-notes.md`; early-reviewed S-149/S-150/S-169 were not recounted.

## Final pending-case result

```text
S-010 -> design / current owners consolidate accepted sub-decisions
S-015 -> design / retrospective assurance provenance
S-035 -> specs / retained current accepted scheduled-trigger amendment
S-041 -> design / two-axis Condition decision consolidated in current owners
S-043 -> design / final review/closure evidence consolidated in current owners
```

No accepted implementation-facing law is stranded by these dispositions. No split or promotion is required for the five-case set.

## Reference gate result

DCR-016 is satisfied for physical execution by the branch-local tracked-tree audit recorded in `2026-08-29-documentation-corpus-refactor-reference-set-proof.md`.

```text
FROZEN_CORPUS_TARGETS:             419
MIGRATION_MAP_RESOLVED:            419 / 419
MOVE:                              370
RETAIN:                             49
EXTRACTION:                          1
PRE_MIGRATION_REFERENCE_OCCURRENCES: 2166
AMBIGUOUS_BASENAMES:                 0
NON_UTF8_TRACKED_FILES:               0
MECHANICAL_PATH_REPAIRS:            365 occurrences
CROSS_DIRECTORY_BASENAME_REPAIRS:   138 occurrences
HISTORICAL_BASENAME_EXCEPTIONS:       2 occurrences
TOTAL_REQUIRED_PATH_REPAIRS:        503 occurrences
```

The two reviewed exceptions are the Part-13 census mentions of the pre-migration S-161 basename; the same entry already records S-161's final `research/` destination and therefore preserves migration provenance without acting as live routing.

## Migration gate

Physical relocation is authorized by the DCR process gate and is being executed in small coherent checkpoints from the proven migration map and path-repair set. Every publication requires fresh remote HEAD, coherent move+repair publication, applicable verification and fresh remote read-back.

Safety invariants: preserve provenance/rejected/superseded reasoning; strand no accepted law in `design/` or `research/`; do not modernize semantics opportunistically; authority is semantic rather than directory-derived; historical path text may remain only when genuinely historical while live routing must resolve current locations.

Published physical checkpoints through the current cursor:

```text
ZERO_REPAIR_BATCHES: 102 moves complete; final zero-repair SHA 995d68decd4d142dc19c19f853ccc166b9710a72
S6D02_RESEARCH_R033: aa5f15b1968a8fc9fc11f3293acd500102dce900
R2_6_HOST_ASSURANCE_CHAIN_8: 2dd06c09688f990f4b1da8876b24f475937f76cb
R015_MOVE_PLUS_H1_H8_EXTRACTION: 65c66fdd17e75e83357e540b7ba4d0228c48cf3a
HOUSE_RULES_S207_HOLD: f0cc926968228ea3acf0f8ac9175d3dd41af66fa
STEP2_TEMPORAL_RECOVERY_S033_S034_S036: 24bb808336ca7267393725df192534e808e2b2b2
STEP5_0_S074_S077: 9d58c7eed501e6b5466fae7a1d3b05e220f49f71
STEP5_1_S082_S086: 269bbf46aa73090c2aea181b7a60421fcbc13531
S6D01_PACKAGE_IDENTITY_PARTIAL: 3fc223210c34c269b3c12ac17424d9022356cc90
STEP5_2_PHASE_A_S089_S098_EXCEPT_S096: a22f85dcd147975298388dea2e881b55be5be9e3
STEP5_2_PHASE_B_S088_S096: d04403c39644cfcfda0a346b66f11cab2f30063e
STEP5_3_S100_S107: c80a6cc1fd26ef16426d6780674b9da31e9fa1e7
STEP5_4_S110_S116: c2b061411f868b02556062eb21fd39414dbbd712
STEP5_5_S119_S126: 47521d48e3a8594c8a8adeea128fa9db58cd8621
STEP5_6_S128_S133: ff843bfc3d1729276a939936b6cf93cdff962bd2
STEP5_7_S135_S140: fd00fd0d44b473cf9d38542d7858f52122eaba5c
STEP5_8_S142_S147: dbeff310cb7ae49b3e26539c048b3ca11b1abdda
STEP5_9_S151_S157_EXCEPT_S158: 198bc6197e6fb07e198928928675f4de3b543297
RESEARCH_PROVENANCE_R2_EVIDENCE_CLUSTER: 27091a150cfc50aad2d3c2792dd282d6d9c69f55
STEP2_STEP3_DESIGN_HISTORY: 5066afff9d1d12edcb3f291c6dc9fa80077db049
STEP4_STEP5_0_STEP5_1_DESIGN_HISTORY: b9bf85faad7784b0cd22878e7d16aefc7f3dd05b
STEP5_9_STEP6_EARLY_DESIGN_HISTORY: 9af5a18b73ca0bc028166ec0ee44debc77b025c7
STEP5_11_STEP5_13_STEP5_14_STEP6_DESIGN_HISTORY: b8dd067c47d886d444e7a280020925a643ebdeba
HOUSE_RULES_DESIGN_HISTORY: ad9ba43bda0ee7c30e7a1763c1b5fa1f4322b992
R2_1_R2_5_DESIGN_HISTORY: 3dddc5c689601098e57eadff47cd61bf43bab982
R2_5_R2_7_DESIGN_HISTORY: 928b5234528f2cc2c6160ad1da3cec5624bfc870
S6D_01_S6D_06_DESIGN_HISTORY: cc0454c7d0b143e9525d36807f4a3e10b68ce72b
```

`S6D01_PACKAGE_IDENTITY_PARTIAL` is a validated frozen-corpus checkpoint. It moves six frozen MOVE rows (`R-032`, `S-273`, `S-275`, `S-277`, `S-278`, `S-279`) to `design/` and applies seven frozen path repairs. `S-274`, `S-276` and `S-280` remain for the rest of the S6D-01 family. The commit also contains only benign EOF/line-ending representation churn beyond the intended placement/link changes.

## Migration queue tail

Earlier batches M-001..M-018 retain their census-defined dispositions; individual source identities may already have moved through the checkpoint sequence above. Remaining MOVE rows continue from the frozen map rather than from this summary table.

| Batch | Census | Disposition | Status |
|---|---|---|---|
| M-019 | Parts 32-33 S-273..S-280 | move complete S6D-01 chain to design; owner `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | PARTIAL — R-032/S-273/S-275/S-277/S-278/S-279 MOVED; S-274/S-276/S-280 REMAIN |
| M-020 | Parts 34-35 S-281..S-288 | move complete S6D-02 chain to design; owner `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` | PARTIAL — R-033 RESEARCH COMPANION MOVED; S-281..S-288 REMAIN |
| M-021 | Parts 36-37 S-289..S-296 | move complete S6D-03 chain to design; owner `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` | REMAINING |
| M-022 | Parts 38-39 S-297..S-304 | move complete S6D-04 chain to design; owner `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` | REMAINING |
| M-023 | Parts 40-41 S-305..S-312 | move complete S6D-05 chain to design; owner `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` | REMAINING |
| M-024 | Parts 42-43 S-313..S-320 | move complete S6D-06 chain to design; owner `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` | REMAINING |
| M-025 | Parts 44-45 S-321..S-328 | move complete S6D-07 chain to design; owner `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`; preserve accepted human-decision provenance | REMAINING |
| M-026 | Parts 46-47 S-329..S-336 | move complete S6D-08 chain to design; owner `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md`; preserve multi-pass/Senior-HOLD repair provenance | REMAINING |
| M-027 | Parts 48-51 S-337..S-348 | move complete S6D-09 chain to design; owner `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`; preserve Decision-C and Senior spatial-repair provenance | REMAINING |
| M-028 | Parts 52-53 S-349..S-356 | move complete S6D-10 chain to design; owner `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md` | REMAINING |
| M-029 | Part 54 S-357 | retain accepted B′ owner decision in specs; only pre-realization blocked status is superseded by integrated closure | NO_MOVE / CURRENT_OWNER |
| M-030 | Parts 55-56 S-358..S-365 | move complete S6D-11 chain to design; owner `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | REMAINING |
| M-031 | Parts 57-59 S-366..S-374 | move complete S6D-12 design/review/closure chain to design; retain current semantics in existing S6D owners | REMAINING |
| M-032 | Part 60 S-375 | move current integrated S6D closure status/evidence record to design; roadmap remains sequencing/status authority | REMAINING |
| M-033 | Part 61 S-010/S-015/S-041/S-043 | move final four resolved pending artifacts to design | REMAINING UNLESS ALREADY INCLUDED BY EARLIER CHECKPOINT |
| M-034 | Part 61 S-035 | retain current accepted temporal/recovery amendment in specs | NO_MOVE / CURRENT_OWNER |

Known post-realization stale blocker wording in current domain-rules/package-machine owners remains separately tracked status-maintenance debt and is not repaired by corpus classification.

## Latest physical checkpoint

```text
CHECKPOINT: S6D_01_S6D_06_DESIGN_HISTORY
COMMIT: cc0454c7d0b143e9525d36807f4a3e10b68ce72b
MOVES_ADDED: 19
FROZEN_REPAIRS_ADDED: 30
CUMULATIVE_MOVES: 346 / 370
CUMULATIVE_FROZEN_REPAIRS: 457 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: R2_5_R2_7_DESIGN_HISTORY
COMMIT: 928b5234528f2cc2c6160ad1da3cec5624bfc870
MOVES_ADDED: 6
FROZEN_REPAIRS_ADDED: 4
CUMULATIVE_MOVES: 327 / 370
CUMULATIVE_FROZEN_REPAIRS: 427 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: R2_1_R2_5_DESIGN_HISTORY
COMMIT: 3dddc5c689601098e57eadff47cd61bf43bab982
MOVES_ADDED: 22
FROZEN_REPAIRS_ADDED: 34
CUMULATIVE_MOVES: 321 / 370
CUMULATIVE_FROZEN_REPAIRS: 423 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: HOUSE_RULES_DESIGN_HISTORY
COMMIT: ad9ba43bda0ee7c30e7a1763c1b5fa1f4322b992
MOVES_ADDED: 16
FROZEN_REPAIRS_ADDED: 51
CUMULATIVE_MOVES: 299 / 370
CUMULATIVE_FROZEN_REPAIRS: 389 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: STEP5_11_STEP5_13_STEP5_14_STEP6_DESIGN_HISTORY
COMMIT: b8dd067c47d886d444e7a280020925a643ebdeba
MOVES_ADDED: 20
FROZEN_REPAIRS_ADDED: 30
CUMULATIVE_MOVES: 283 / 370
CUMULATIVE_FROZEN_REPAIRS: 338 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: STEP5_9_STEP6_EARLY_DESIGN_HISTORY
COMMIT: 9af5a18b73ca0bc028166ec0ee44debc77b025c7
MOVES_ADDED: 17
FROZEN_REPAIRS_ADDED: 23
CUMULATIVE_MOVES: 263 / 370
CUMULATIVE_FROZEN_REPAIRS: 308 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: STEP4_STEP5_0_STEP5_1_DESIGN_HISTORY
COMMIT: b9bf85faad7784b0cd22878e7d16aefc7f3dd05b
MOVES_ADDED: 13
FROZEN_REPAIRS_ADDED: 19
CUMULATIVE_MOVES: 246 / 370
CUMULATIVE_FROZEN_REPAIRS: 285 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: STEP2_STEP3_DESIGN_HISTORY
COMMIT: 5066afff9d1d12edcb3f291c6dc9fa80077db049
MOVES_ADDED: 25
FROZEN_REPAIRS_ADDED: 83
CUMULATIVE_MOVES: 233 / 370
CUMULATIVE_FROZEN_REPAIRS: 266 / 503
UNPUBLISHED_WORK: NONE
```

## Latest physical checkpoint

```text
CHECKPOINT: RESEARCH_PROVENANCE_R2_EVIDENCE_CLUSTER
COMMIT: 27091a150cfc50aad2d3c2792dd282d6d9c69f55
MOVES_ADDED: 18
FROZEN_REPAIRS_ADDED: 77
CUMULATIVE_MOVES: 208 / 370
CUMULATIVE_FROZEN_REPAIRS: 183 / 503
UNPUBLISHED_WORK: NONE
```

## Next exact task

```text
SEMANTIC_CENSUS: COMPLETE
SUPERSESSION_GATE: COMPLETE
REFERENCE_SET: PROVEN
PHYSICAL_MIGRATION: COMPLETE / CLOSURE VERIFICATION IN PROGRESS
COMPLETED_MOVES: 370 / 370
COMPLETED_REQUIRED_PATH_REPAIRS: 503 / 503
EXTRACTION: 1 / 1 COMPLETE
NEXT: stop after verified DCR closure, cleanup and final status publication; await further user command
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```


## Latest physical checkpoint

```text
CHECKPOINT: FINAL_FROZEN_MOVE_REPAIR_BATCH
COMMIT: 01e6e0072358db75b1ebea91290c51471c9bed9c
MOVES_ADDED: 0
FROZEN_REPAIRS_ADDED: 2
X_REPAIR_ADDED: 0
CUMULATIVE_MOVES: 370 / 370
CUMULATIVE_FROZEN_REPAIRS: 503 / 503
UNPUBLISHED_WORK: NONE
```


## DCR closure verification and cleanup

```text
CLOSURE_VERIFICATION_BASE_HEAD: 6d997ca2024492551c670f5462242793b4a5e387
FROZEN_REPLAY: PASS / 419 targets / 370 MOVE / 49 RETAIN / 504 actionable repairs (503 frozen + X) / 0 outstanding
MOVE_AND_RETAIN_INVARIANTS: PASS / all MOVE old paths absent and final paths present; all RETAIN paths present with preserved blobs
EXTRACTION: PASS / R-015 extracted research evidence present with SPLIT_FROM provenance
HISTORICAL_EXCEPTIONS: PASS / E23 lines 48 and 59 preserved unchanged
LIVE_OLD_PATH_SCAN: PASS / branch-complete scan; only allowed R-015 SPLIT_FROM provenance remained
AGGREGATE_DCR_DIFF: PASS / 404 expected changed paths / 0 unexpected / 0 missing from the initial execution baseline
POST_CLEANUP_RECONCILIATION: PASS / 863 remaining blobs unchanged; exactly four temporary artifacts absent
CANDIDATE_REPLAY_VERIFICATION: PASS / Connector exact-diff and frozen replay verification
MAINTENANCE_AND_DEV_TESTS: PASS / applicable Validate workflow completed maintenance audit and DEV unit tests
CLEANUP_COMMIT: 6d997ca2024492551c670f5462242793b4a5e387
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
