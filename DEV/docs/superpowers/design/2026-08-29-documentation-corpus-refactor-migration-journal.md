# Documentation Corpus Refactor — Migration Journal

Status: **ACTIVE OPERATIONAL JOURNAL — PHYSICAL MIGRATION DEFERRED**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`
Initial verified HEAD: `584322f640a14b05e4cbfcaa63d8349187cd3780`

This is the compact operational continuation surface for the owner-approved Documentation Corpus Refactor. It is **not** architecture or semantic-census authority.

Semantic classification remains owned by:

- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-census.md`
- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-*.md`

Connector/path-enumeration guidance remains in:

- `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-connector-operations-note.md`

The journal intentionally does not duplicate item-level census semantics. Census IDs are the durable join key.

## 1. Current baseline

```text
PRE_REFACTOR_SPECS_BASELINE:               375
SPECS_FULL_CONTENT_REVIEWED:               203
UNAMBIGUOUS_DESIGN_DESTINATIONS:           166
SPECS_TO_RESEARCH_DESTINATIONS:              1
CONFIRMED_CURRENT_SPEC/AMENDMENT_OWNERS:     31
PENDING_FINAL_SUPERSESSION_CHECK:             5
SPECS_REMAINING_UNREVIEWED:                 172

PHYSICAL_MOVES_PERFORMED:                    0
MIGRATED_VERIFIED:                            0
REFERENCE_AUDIT_GATE:           NOT SATISFIED / DCR-016 OPEN
```

Current durable semantic checkpoint: **Specs Census Part 19**.

Unique-source correction applied before continuing 2026-08-24:

```text
STEP5_14_CANONICAL_FINAL_CENSUS_ID: S-118  # counted in Part 07
S-200: 2026-08-21-step-6-pre-design-framing-working-notes.md
PART18_UNIQUE_CURSOR: 200 / 375
PART19_UNIQUE_CURSOR: 203 / 375
2026-08-21 UNIQUE REVIEW: 45 / 45
```

Part 18 correction commit: `21c3462fc720feefcbdd12376d2fffc59e0d3cb7`.
Part 19 cumulative-count correction commit: `5cc22f32befcf3be514c1faf9b82714bab4ee2b1`.

The 2026-08-24 exact baseline inventory is independently cross-checked by branch compare and contains exactly **57** `specs/2026-08-24-*` sources. Three were already reviewed early and must not be counted again:

- S-149 `2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md`;
- S-150 `2026-08-24-r2-5-collaboration-multiplayer-resolution-gate.md`;
- S-169 `2026-08-24-r2-1-continuity-history-canonical-spec.md`.

Therefore **54 unique 2026-08-24 baseline specs sources remain unreviewed** at the Part-19 cursor.

## 2. Stable migration dispositions

- `KEEP_IN_SPECS_CURRENT_OWNER`
- `KEEP_IN_SPECS_CURRENT_AMENDMENT`
- `MOVE_TO_DESIGN_PROVENANCE`
- `SUPERSEDED_CANONICAL_TO_DESIGN`
- `RESEARCH_SPLIT_OR_EXTRACTION`
- `PENDING_SUPERSESSION_CHECK`
- `BLOCKED_REFERENCE_AUDIT`

A known semantic destination is not authorization to move. All relocation remains blocked until branch-complete inbound references/path repairs are proven.

## 3. Physical-move gate

Before any relocation batch:

1. fresh-read remote branch HEAD;
2. re-read controlling census entries and current owners/amendments;
3. confirm later authority has not changed disposition;
4. obtain a **branch-complete inbound-reference census** for every source path;
5. enumerate every path repair; unresolved/unprovable references block the batch;
6. check outbound links and current-owner/provenance routing;
7. publish one coherent move + path-repair batch only to `v1/engine-rearchitecture`;
8. verify new paths, absence of old paths, all enumerated repairs, canonical owners, applicable tests/audits;
9. fresh remote read-back before marking `MIGRATED_VERIFIED`.

DCR-016 remains the controlling blocker. GitHub code-search absence is not sufficient negative evidence on this non-default branch.

## 4. Safety invariants

- preserve provenance; do not erase superseded/rejected reasoning;
- authority is semantic, not directory-derived;
- no accepted law may be stranded only in `design/`/`research/`;
- no opportunistic semantic modernization during path repair;
- current canonical parents/amendments stay in `specs/` unless explicit supersession is proven;
- reference correctness is batch-wide;
- coherent semantic-family batches are preferred;
- historical path text may remain when it is genuinely historical, while live routing must point to current locations.

## 5. Batch record schema for executed moves

```text
BATCH_ID
CENSUS_IDS
SOURCE_PATHS
DESTINATION_PATHS
SEMANTIC_DISPOSITIONS
CURRENT_OWNER_OR_AMENDMENT
SUPERSESSION_EVIDENCE
INBOUND_REFERENCE_AUDIT_METHOD
INBOUND_REFERENCE_SET
OUTBOUND_PATH_REPAIRS
OTHER_PATH_REPAIRS
PRE_WRITE_HEAD
MIGRATION_COMMIT_SHA
POST_WRITE_HEAD
VERIFICATION_COMMANDS_OR_HOSTED_CHECKS
REMOTE_READBACK_EVIDENCE
FINAL_STATUS
NOTES / DEFERRED FOLLOWUPS
```

## 6. Migration queue

| Batch | Census authority | Operational disposition | Status |
|---|---|---|---|
| M-001 | Research R-001..R-044 | realize changed destinations + R-015 controlled research extraction; unchanged research stays | `BLOCKED_REFERENCE_AUDIT` |
| M-002 | Specs Part 01, S-001..S-060 | move explicit design destinations; exclude five pending supersession cases/current owners | `BLOCKED_REFERENCE_AUDIT` |
| M-003 | Parts 02–03, S-061..S-078 | move Step-4 / Step-5.0 derivation provenance; keep consolidated owners | `BLOCKED_REFERENCE_AUDIT` |
| M-004 | Part 04, S-079..S-087 | S-079..S-086 -> `design/`; keep S-087 Step-5.1 canonical | `BLOCKED_REFERENCE_AUDIT` |
| M-005 | Part 05, S-088..S-099 | S-088..S-098 -> `design/`, including superseded canonical S-096; keep S-099 v2 | `BLOCKED_REFERENCE_AUDIT` |
| M-006 | Part 06, S-100..S-109 | S-100..S-107 -> `design/`; keep S-108 + canonical amendment S-109 | `BLOCKED_REFERENCE_AUDIT` |
| M-007 | Part 16, S-179..S-188 | S-179..S-187 -> `design/`; keep S-188 Step-5.12 canonical | `BLOCKED_REFERENCE_AUDIT` |
| M-008 | Part 17, S-189..S-195 | S-189..S-194 -> `design/`; keep S-195 Step-5.13 canonical | `BLOCKED_REFERENCE_AUDIT` |
| M-009 | Corrected Part 18 + Part 07 owner | S-196..S-200 -> `design/`; keep existing S-118 Step-5.14 canonical; DCR-020 tracks stale SD-5 wording | `BLOCKED_REFERENCE_AUDIT` |
| M-010 | Part 19, S-201..S-203 | keep S-201 Round-1 rebaseline owner + S-202 Step-4 single-context amendment; S-203 working note -> `design/` | `BLOCKED_REFERENCE_AUDIT` |

Parts 07–15 already contain authoritative semantic dispositions for their reviewed families. Their compact queue rows may be backfilled before physical execution; omission from this table does not change their census destination.

## 7. Queue extension rule

Append a batch only after the entire semantic family/group is fully reviewed and later-authority relationships are checked. Never infer a move from filenames or a partially read family.

For semantic enumeration use the frozen baseline `specs/` tree directly:

```text
PRE_REFACTOR_SPECS_TREE_SHA: 0fb176ec4cee7af3d6765a34174964679c99819d
require: truncated == false
```

Day-scoped branch compares may be used as an independent exact-path inventory cross-check when their source count reconciles exactly with the frozen-tree census count; semantic classification still requires exact full-content `fetch_file` review.

This solves census-family inventory only. It does not solve the branch-complete inbound-reference gate.

## 8. Current execution cursor

```text
CORPUS_REFACTOR_STATUS: IN_PROGRESS
DURABLE_SPECS_CENSUS_CURSOR: 203 / 375 UNIQUE SOURCES
DURABLE_LAST_CHECKPOINT: Specs Census Part 19 (corrected cumulative counts)
LAST_CLOSED_SEMANTIC_GROUP: all frozen-baseline 2026-08-23 specs sources
NEXT_DURABLE_SEMANTIC_FAMILY: 2026-08-24 campaign rulings / House Rules architecture family
2026_08_24_BASELINE_SOURCES: 57
2026_08_24_ALREADY_REVIEWED_EARLY: 3
2026_08_24_REMAINING_UNREVIEWED: 54
PHYSICAL_MIGRATION_STATUS: DEFERRED
REFERENCE_AUDIT_STATUS: BRANCH-COMPLETE INBOUND-REFERENCE METHOD NOT YET PROVEN / DCR-016 OPEN
NEXT_ACTION: continue full-content 2026-08-24 specs census from campaign-rulings House-Rules task brief; skip S-149/S-150/S-169 when their chronological families are reached
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```