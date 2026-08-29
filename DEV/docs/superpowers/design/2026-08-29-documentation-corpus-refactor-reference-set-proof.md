# Documentation Corpus Refactor — Branch-Complete Reference-Set Proof

Status: **REFERENCE_SET_PROVEN — READY FOR PHYSICAL MIGRATION**
Date: 2026-08-29
Branch: `v1/engine-rearchitecture`
Pre-migration proof SHA: `0a354e3e5d82c5941f27f642bccb67b674311989`
DCR reference-audit run: `33275237058` — SUCCESS
Artifact digest: `sha256:f6d4709029fd796de17695982bed41c80e78e4c5286f7dbb21b8e54d9be99cf4`

This document closes DCR-016's pre-migration reference-enumeration gate. It is design/audit provenance, not architecture law.

## 1. Proof method

The proof does not rely on GitHub code-search absence.

The repository audit tooling:

1. enumerates the exact checked-out branch with `git ls-files -z`;
2. freezes the complete pre-migration corpus target set;
3. scans every tracked UTF-8 file against the unique frozen target basenames;
4. reports ambiguous basenames instead of guessing target identity;
5. derives the 419-row migration map from the completed semantic census, with later census dispositions overriding earlier pending states;
6. partitions moved-target occurrences into full old paths, old-root-relative paths, and basename-only occurrences;
7. preserves the frozen target manifest so the same old identities can be replayed after physical movement.

The ordinary `Validate engine source` workflow also passed on the proof/tooling chain before this gate was declared.

## 2. Frozen target and migration accounting

```text
CORPUS_TARGETS:                419
  old specs:                   375
  old research:                 44

RESOLVED_TARGETS:              419
UNRESOLVED_TARGETS:              0

MOVE:                          370
  specs -> design:             333
  specs -> research:             1
  research -> design:           36

RETAIN:                         49
  specs:                        41
  research:                      8

EXTRACTIONS:                     1
  R-015 -> research/2026-08-24-chatgpt-plus-host-evidence.md
```

The extraction is additional to the 419 frozen source identities; it does not change source accounting.

## 3. Repository-wide reference inventory

At proof SHA `0a354e3e5d82c5941f27f642bccb67b674311989`:

```text
TRACKED_FILES:                         855
CORPUS_TARGETS:                        419
CORPUS_REFERENCE_OCCURRENCES:         2166
SOURCE_FILES_WITH_CORPUS_REFERENCES:   333
TARGETS_WITH_REFERENCES:               419 / 419
AMBIGUOUS_TARGET_BASENAMES:              0
BINARY_OR_NON_UTF8_TRACKED_FILES:        0
```

Therefore every frozen corpus target has been observed from a branch-complete tracked-tree scan, and no target identity is ambiguous by basename.

## 4. Moved-target path-repair partition

For the 370 moving source identities, the path-repair planner produced:

```text
FULL_OLD_PATH_OCCURRENCES:            333
SHORT_OLD_ROOT_OCCURRENCES:            32
MECHANICAL_REPAIR_OCCURRENCES:        365
MECHANICAL_REPAIR_SOURCE_FILES:       132
BASENAME_ONLY_OCCURRENCES:            923
NON_UTF8_FILES:                         0
```

### 4.1 Mechanical set

The 365 full/short occurrences are deterministic old-path literals. They are eligible for mechanical replacement to the census-derived destination path, except where a physical migration evidence artifact intentionally freezes the old mapping. No such exception exists inside this pre-migration mechanical set.

### 4.2 Basename-only set

All 923 basename-only occurrences were classified by the final source and target directories from the migration map:

- **783** remain same-directory references after migration and therefore remain valid without rewriting;
- **140** are cross-directory occurrences and received explicit review.

The 140 cross-directory occurrences resolve as follows:

- **136** occur in retained canonical specs and point to derivation/source artifacts moving from `specs/` to `design/`; repair to `../design/<basename>` is required so the derivation route remains discoverable;
- **1** occurs in `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` and points to the S6D integrated closure moving to `design/`; current routing path repair is required;
- **1** occurs in `DEV/TESTS/test_release_game_passthrough.py` and constructs the old `specs/` path to an S6D-09 owner-decision artifact moving to `design/`; code path repair is required;
- **2** occur in `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-13.md` and intentionally preserve the pre-migration S-161 source basename while separately recording its final `research/` destination. These are historical migration evidence and remain unchanged.

Thus:

```text
BASENAME_ONLY_REPAIRS_REQUIRED:       138
BASENAME_ONLY_PROVENANCE_EXCEPTIONS:   2
TOTAL_PATH_REPAIR_OCCURRENCES:        503
```

The 503-count is an occurrence count, not a source-file count. Repairs must be applied from the generated plan and reviewed cross-directory dispositions, not by unconstrained global string replacement.

## 5. DCR-016 disposition

DCR-016 is resolved for pre-migration execution:

```text
REFERENCE_ENUMERATION:        PROVEN
TARGET_IDENTITY:              UNAMBIGUOUS
MIGRATION_MAP:                419 / 419 RESOLVED
PATH_REPAIR_SET:              PROVEN
BASENAME_EXCEPTION_SET:       PROVEN (2 historical DCR-provenance occurrences)
PHYSICAL_MIGRATION_GATE:      OPEN
```

Post-migration closure still requires replaying the frozen 419-target manifest and proving that any remaining old literals are exclusively explicit frozen/historical migration evidence rather than live routing or executable paths.

## 6. Execution constraints carried forward

- Physical movement must follow the census-derived 419-row map exactly.
- The 370 source moves are true moves; do not leave duplicate old source files.
- R-015 moves to `design/` intact and yields one bounded H1-H8 evidence extraction under `research/`.
- Retained 49 source identities do not move.
- Preserve the two reviewed Part-13 basename occurrences as pre-migration provenance.
- Do not repair DCR-007/DCR-008 architecture wording; they remain deferred to WP-26.
- Do not perform unrelated README or architecture cleanup.
- WP-07 remains NOT STARTED until full Documentation Corpus Refactor closure and Senior review.
