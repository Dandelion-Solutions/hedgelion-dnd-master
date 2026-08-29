# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — SEMANTIC BASELINE CENSUS COMPLETE / PHYSICAL MIGRATION DEFERRED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`

This file is an operational continuation surface, not semantic authority. Item-level dispositions are owned by the research census and the durable `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md` series.

## Current cursor

```text
PRE_REFACTOR_SPECS_BASELINE: 375
SPECS_FULL_CONTENT_REVIEWED: 375
SPECS_REMAINING_UNREVIEWED: 0
UNAMBIGUOUS_DESIGN_DESTINATIONS: 329
SPECS_TO_RESEARCH_DESTINATIONS: 1
CONFIRMED_CURRENT_SPEC_OR_OWNER_DESTINATIONS: 40
PENDING_FINAL_SUPERSESSION_CHECK: 5
PHYSICAL_MOVES_PERFORMED: 0
REFERENCE_AUDIT_GATE: NOT SATISFIED / DCR-016 OPEN
CURRENT_DURABLE_SEMANTIC_CHECKPOINT: Specs Census Part 60
PART_60_PUBLICATION_SHA: 41448329a7cb2d0d16cb7f76b0957d8d0373b096
```

Part 60 remote read-back is verified.

Frozen baseline date closure:

```text
2026-08-18: COMPLETE
2026-08-19: COMPLETE SUBJECT TO FIVE EXPLICIT FINAL SUPERSESSION CHECKS
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

## Remaining semantic gate

The initial census intentionally left five early accepted artifacts pending final later-owner proof:

```text
S-010  2026-08-18-step-2-mechanical-state-ownership-design.md
S-015  2026-08-19-step-1-2-retrospective-architecture-assurance-final.md
S-035  2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md
S-041  2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md
S-043  2026-08-19-step-2-final-critical-review.md
```

Do not finalize migration counts until these five are classified against current owning authority.

## Migration gate

No physical relocation is authorized until a branch-complete inbound-reference census is proven. GitHub code-search absence alone is insufficient. Every move batch requires fresh HEAD, current-owner recheck, complete inbound/outbound path-repair set, coherent move+repair publication, applicable verification and fresh remote read-back.

Safety invariants: preserve provenance/rejected/superseded reasoning; strand no accepted law in `design/` or `research/`; do not modernize semantics opportunistically; authority is semantic rather than directory-derived; historical path text may remain only when genuinely historical while live routing must resolve current locations.

## Migration queue tail

Earlier batches M-001..M-018 retain their census-defined dispositions and remain `BLOCKED_REFERENCE_AUDIT`.

| Batch | Census | Disposition | Status |
|---|---|---|---|
| M-019 | Parts 32-33 S-273..S-280 | move complete S6D-01 chain to design; owner `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md` | BLOCKED_REFERENCE_AUDIT |
| M-020 | Parts 34-35 S-281..S-288 | move complete S6D-02 chain to design; owner `DEV/ARCHITECTURE/CATALOG_ADMISSION.md` | BLOCKED_REFERENCE_AUDIT |
| M-021 | Parts 36-37 S-289..S-296 | move complete S6D-03 chain to design; owner `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` | BLOCKED_REFERENCE_AUDIT |
| M-022 | Parts 38-39 S-297..S-304 | move complete S6D-04 chain to design; owner `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md` | BLOCKED_REFERENCE_AUDIT |
| M-023 | Parts 40-41 S-305..S-312 | move complete S6D-05 chain to design; owner `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` | BLOCKED_REFERENCE_AUDIT |
| M-024 | Parts 42-43 S-313..S-320 | move complete S6D-06 chain to design; owner `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` | BLOCKED_REFERENCE_AUDIT |
| M-025 | Parts 44-45 S-321..S-328 | move complete S6D-07 chain to design; owner `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`; preserve accepted human-decision provenance | BLOCKED_REFERENCE_AUDIT |
| M-026 | Parts 46-47 S-329..S-336 | move complete S6D-08 chain to design; owner `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md`; preserve multi-pass/Senior-HOLD repair provenance | BLOCKED_REFERENCE_AUDIT |
| M-027 | Parts 48-51 S-337..S-348 | move complete S6D-09 chain to design; owner `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`; preserve Decision-C and Senior spatial-repair provenance | BLOCKED_REFERENCE_AUDIT |
| M-028 | Parts 52-53 S-349..S-356 | move complete S6D-10 chain to design; owner `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md` | BLOCKED_REFERENCE_AUDIT |
| M-029 | Part 54 S-357 | retain accepted B′ owner decision in specs; only pre-realization blocked status is superseded by integrated closure | NO_MOVE / CURRENT_OWNER |
| M-030 | Parts 55-56 S-358..S-365 | move complete S6D-11 chain to design; owner `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md` | BLOCKED_REFERENCE_AUDIT |
| M-031 | Parts 57-59 S-366..S-374 | move complete S6D-12 design/review/closure chain to design; retain current semantics in existing S6D owners | BLOCKED_REFERENCE_AUDIT |
| M-032 | Part 60 S-375 | move current integrated S6D closure status/evidence record to design; roadmap remains sequencing/status authority | BLOCKED_REFERENCE_AUDIT |

Known post-realization stale blocker wording in current domain-rules/package-machine owners remains separately tracked status-maintenance debt and is not repaired by corpus classification.

## Next exact task

```text
NEXT_SEMANTIC_TASK: resolve S-010 / S-015 / S-035 / S-041 / S-043 against current owning authority
THEN: finalize semantic destination counts and migration queue
THEN: solve DCR-016 branch-complete inbound-reference/path-repair proof
PHYSICAL_MIGRATION_STATUS: DEFERRED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
