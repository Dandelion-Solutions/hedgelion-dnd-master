# Documentation Corpus Refactor — Conflict Register Amendment 01

Status: **CURRENT STATUS AMENDMENT TO DCR-002…DCR-006**
Date: 2026-08-29
Applies to: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-conflict-debt-register.md`
Evidence owner: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-61.md`

This amendment changes only the current status/disposition of DCR-002 through DCR-006 after the final item-level later-owner sweep. All other fields and DCR items in the base register remain unchanged. The base register plus this amendment form the current conflict/debt register until the required final frozen report consolidates them.

## DCR-002 — S-010 Step-2 preliminary ownership design

- **STATUS:** `RESOLVED_BY_REFACTOR`.
- **RESULT:** accepted preliminary ownership sub-decisions are fully carried by later Step-2 assurance/current Actor, Health/Effects/Recovery, Entity Structures and MechanicalContext owners.
- **CORPUS DISPOSITION:** move S-010 to `design/` when DCR-016 permits physical migration.
- **STRANDED LAW:** none.

## DCR-003 — S-015 retrospective Steps 1–2 assurance final

- **STATUS:** `RESOLVED_BY_REFACTOR`.
- **RESULT:** item-level assurance amendments survive in current catalog/entity/mechanical-state/MechanicalContext owners or in later Step-3/5 owners; the file remains assurance/closure provenance rather than an implementation-facing owner.
- **CORPUS DISPOSITION:** move S-015 to `design/` when DCR-016 permits physical migration.
- **STRANDED LAW:** none.

## DCR-004 — S-035 temporal/recovery resolution

- **STATUS:** `RESOLVED_BY_REFACTOR`.
- **RESULT:** the supersession question is closed in favor of **retention**. The human-approved owner-local scheduled-trigger decision remains a current accepted amendment.
- **CURRENT ROUTE:** current `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` explicitly names S-035 as the authoritative amendment; current Effect/world-effect schemas realize the same contract; later Step-5.3 and S6D-08 integrate but do not supersede it.
- **CORPUS DISPOSITION:** retain S-035 in `specs/`.
- **STRANDED LAW:** none.

## DCR-005 — S-041 Condition aggregation × intrinsic scope

- **STATUS:** `RESOLVED_BY_REFACTOR`.
- **RESULT:** the accepted two-axis decision is fully consolidated in current `ENTITY_STRUCTURES.md`, strict Condition schema, MechanicalContext derived-node graph and Health/Effects/Recovery owner.
- **CORPUS DISPOSITION:** move S-041 to `design/` as preserved human-decision provenance when DCR-016 permits physical migration.
- **STRANDED LAW:** none.

## DCR-006 — S-043 Step-2 final critical review

- **STATUS:** `RESOLVED_BY_REFACTOR`.
- **RESULT:** all authoritative review corrections are represented in current architecture/machine owners; S-043 itself explicitly treats aligned current normative docs/machine inventory as the resulting contract and historical review documents as non-alternate authority.
- **CORPUS DISPOSITION:** move S-043 to `design/` when DCR-016 permits physical migration.
- **STRANDED LAW:** none.

## Accounting effect

```text
PENDING_FINAL_SUPERSESSION_CHECK: 5 -> 0
DESIGN_DESTINATIONS:             329 -> 333
SPECS_TO_RESEARCH:                 1 -> 1
RETAINED_CURRENT_SPECS:           40 -> 41
TOTAL:                            375
```

No architecture semantics were changed by this amendment. It records the semantic-placement result only.