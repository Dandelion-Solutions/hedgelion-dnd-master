# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — SEMANTIC CENSUS COMPLETE / REFERENCE_SET_PROVEN / PHYSICAL MIGRATION IN PROGRESS**
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
PHYSICAL_MOVES_PERFORMED: 125 / 370
PHYSICAL_MOVES_REMAINING: 245
PATH_REPAIRS_APPLIED: 23 / 503 occurrences
PATH_REPAIRS_REMAINING: 480 occurrences
EXTRACTIONS_PUBLISHED: 1 / 1
REFERENCE_AUDIT_GATE: SATISFIED / REFERENCE_SET_PROVEN
CURRENT_DURABLE_SEMANTIC_CHECKPOINT: Specs Census Part 61
PART_61_PUBLICATION_SHA: 78731e310cd9eae3d7870c2f5c4743ca17d459ad
CONFLICT_STATUS_AMENDMENT_01_SHA: a6531e9bf9477dc4bcd9b624119d3fbfe09e0690
REFERENCE_SET_PROOF: DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-reference-set-proof.md
REFERENCE_SET_PROOF_SHA: 694ca8e203ea813cb5b27033b5570db4d6a82bbb
LAST_PHYSICAL_MIGRATION_CHECKPOINT: 269bbf46aa73090c2aea181b7a60421fcbc13531
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
```

## Migration queue tail

Earlier batches M-001..M-018 retain their census-defined dispositions; individual source identities may already have moved through the checkpoint sequence above. Remaining MOVE rows continue from the frozen map rather than from this summary table.

| Batch | Census | Disposition | Status |
|---|---|---|---|
| M-019 | Parts 32-33 S-273..S-280 | move complete S6D-01 chain to design; owner `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | REMAINING |
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

## Next exact task

```text
SEMANTIC_CENSUS: COMPLETE
SUPERSESSION_GATE: COMPLETE
REFERENCE_SET: PROVEN
PHYSICAL_MIGRATION: IN PROGRESS
COMPLETED_MOVES: 125 / 370
COMPLETED_REQUIRED_PATH_REPAIRS: 23 / 503
EXTRACTION: 1 / 1 COMPLETE
NEXT: continue small coherent move+repair checkpoints from the frozen migration-map.json and path-repair-plan.json; replay and closure verification only after all 370 moves and 503 repairs are complete
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```