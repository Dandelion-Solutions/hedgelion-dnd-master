# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — PHYSICAL MIGRATION DEFERRED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`

This file is an operational continuation surface, not semantic authority. Item-level dispositions are owned by the research census and the durable `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md` series.

## Current cursor

```text
PRE_REFACTOR_SPECS_BASELINE: 375
SPECS_FULL_CONTENT_REVIEWED: 312
SPECS_REMAINING_UNREVIEWED: 63
UNAMBIGUOUS_DESIGN_DESTINATIONS: 267
SPECS_TO_RESEARCH_DESTINATIONS: 1
CONFIRMED_CURRENT_SPEC_OR_OWNER_DESTINATIONS: 39
PENDING_FINAL_SUPERSESSION_CHECK: 5
PHYSICAL_MOVES_PERFORMED: 0
REFERENCE_AUDIT_GATE: NOT SATISFIED / DCR-016 OPEN
CURRENT_DURABLE_SEMANTIC_CHECKPOINT: Specs Census Part 41
PART_41_PUBLICATION_SHA: 8e2116e4245a1ec2c4ebaae3fe3a88903e6796d1
```

Part 41 remote read-back is verified.

Unique-source correction remains in force: S-118 is the Step-5.14 canonical final; S-200 is `2026-08-21-step-6-pre-design-framing-working-notes.md`; 2026-08-21 is 45/45 unique reviewed. For 2026-08-24, early-reviewed S-149/S-150/S-169 were not recounted; that date is 57/57 complete.

Current date progress:

```text
2026-08-24: 57 / 57 COMPLETE
2026-08-25: 55 / 55 COMPLETE
```

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

Parts 07–15 and all earlier census parts remain authoritative item-level records even when rows are not duplicated here.

## Next exact task

```text
NEXT_BASELINE_DATE: 2026-08-26
NEXT_BASELINE_ID: S-313
REQUIRED_METHOD: exact frozen-tree enumeration before assigning family IDs; then full-read each family plus current primary-owner/later-authority sweep
CHECKPOINT_STYLE: small coherent census commits after each family authority is proven
PHYSICAL_MIGRATION_STATUS: DEFERRED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
