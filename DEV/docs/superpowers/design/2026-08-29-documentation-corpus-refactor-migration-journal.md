# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — PHYSICAL MIGRATION DEFERRED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`

This file is an operational continuation surface, not semantic authority. Item-level dispositions are owned by the research census and `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md`.

## Current cursor

```text
PRE_REFACTOR_SPECS_BASELINE: 375
SPECS_FULL_CONTENT_REVIEWED: 272
SPECS_REMAINING_UNREVIEWED: 103
UNAMBIGUOUS_DESIGN_DESTINATIONS: 227
SPECS_TO_RESEARCH_DESTINATIONS: 1
CONFIRMED_CURRENT_SPEC_OR_OWNER_DESTINATIONS: 39
PENDING_FINAL_SUPERSESSION_CHECK: 5
PHYSICAL_MOVES_PERFORMED: 0
REFERENCE_AUDIT_GATE: NOT SATISFIED / DCR-016 OPEN
```

Current durable semantic checkpoint: **Specs Census Part 31**.

Part 31 publication SHA: `075aca8a51cdaec280f3ccb41569707cbf037b72`; remote read-back verified.

Unique-source correction remains in force:

```text
S-118 = Step-5.14 canonical final
S-200 = 2026-08-21-step-6-pre-design-framing-working-notes.md
2026-08-21 = 45 / 45 unique reviewed
```

Frozen 2026-08-24 baseline contains 57 sources. Early-reviewed sources that were not recounted:

- S-149 R2.5 canonical;
- S-150 R2.5 resolution gate;
- S-169 R2.1 canonical.

Current date-group progress:

```text
2026-08-24: 57 / 57 COMPLETE
2026-08-25: 15 / 55
```

## Migration gate

No physical relocation is authorized until a branch-complete inbound-reference census is proven. GitHub code-search absence alone is not sufficient. Before each move batch: fresh remote HEAD, controlling census/current-owner recheck, complete inbound/outbound path repair set, coherent move+repair write, applicable verification, and fresh remote read-back.

Safety invariants:

- preserve provenance and rejected/superseded reasoning;
- no accepted law may become stranded only in `design/` or `research/`;
- no opportunistic semantic modernization during path repair;
- authority is semantic, not directory-derived;
- historical path text may remain only when genuinely historical; live routing must resolve current locations.

## Migration queue

| Batch | Census | Disposition | Status |
|---|---|---|---|
| M-001 | Research R-001..R-044 | execute research census destinations/extraction | BLOCKED_REFERENCE_AUDIT |
| M-002 | Part 01 S-001..S-060 | move classified provenance; preserve pending/current owners | BLOCKED_REFERENCE_AUDIT |
| M-003 | Parts 02-03 S-061..S-078 | Step-4/5.0 provenance migration | BLOCKED_REFERENCE_AUDIT |
| M-004 | Part 04 S-079..S-087 | S-079..086 design; keep S-087 | BLOCKED_REFERENCE_AUDIT |
| M-005 | Part 05 S-088..S-099 | S-088..098 design; keep S-099 | BLOCKED_REFERENCE_AUDIT |
| M-006 | Part 06 S-100..S-109 | S-100..107 design; keep S-108/S-109 | BLOCKED_REFERENCE_AUDIT |
| M-007 | Part 16 S-179..S-188 | S-179..187 design; keep S-188 | BLOCKED_REFERENCE_AUDIT |
| M-008 | Part 17 S-189..S-195 | S-189..194 design; keep S-195 | BLOCKED_REFERENCE_AUDIT |
| M-009 | Corrected Part 18 | S-196..200 design; keep existing S-118 | BLOCKED_REFERENCE_AUDIT |
| M-010 | Part 19 S-201..S-203 | keep S-201/S-202; S-203 design | BLOCKED_REFERENCE_AUDIT |
| M-011 | Part 20 S-204..S-221 | S-204..210 and S-212..221 design; keep S-211 | BLOCKED_REFERENCE_AUDIT |
| M-012 | Part 21 S-222..S-227 | R2.1 derivation to design; keep previously counted S-169 canonical | BLOCKED_REFERENCE_AUDIT |
| M-013 | Part 22 S-228..S-234 | R2.2 derivation to design; keep canonical owner | BLOCKED_REFERENCE_AUDIT |
| M-014 | Part 23 S-235..S-241 | R2.3 derivation to design; keep canonical owner | BLOCKED_REFERENCE_AUDIT |
| M-015 | Part 24 S-242..S-250 | R2.4 derivation/clarifications to design after canonical consolidation; keep canonical owner | BLOCKED_REFERENCE_AUDIT |
| M-016 | Part 25 S-251..S-256 + prior S-149/S-150 | R2.5 derivation/gate to design; keep S-149 canonical | BLOCKED_REFERENCE_AUDIT |
| M-017 | Part 26 S-257..S-263 | R2.6 derivation/owner clarifications to design after consolidation; keep S-262 canonical | BLOCKED_REFERENCE_AUDIT |
| M-018 | Parts 27-31 S-264..S-272 | move S-264..266, S-268, S-271/S-272 to design; keep S-267, S-269, S-270 | BLOCKED_REFERENCE_AUDIT |

Parts 07–15 retain their authoritative item-level census dispositions even where compact rows are not repeated here.

## Next exact task

```text
NEXT_FAMILY: 2026-08-25 S6D-01 — Ruleset / Package / Catalog Snapshot Identity
NEXT_EXPECTED_CENSUS_IDS: S-273..S-280
REQUIRED_METHOD: full-read all 8 family sources + later-authority sweep before disposition
CHECKPOINT_STYLE: small commits after family authority is proven
PHYSICAL_MIGRATION_STATUS: DEFERRED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
