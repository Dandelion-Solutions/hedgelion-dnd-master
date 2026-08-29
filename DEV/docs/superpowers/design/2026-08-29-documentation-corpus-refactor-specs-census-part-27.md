# Documentation Corpus Refactor — Specs Census Part 27

Status: **DURABLE CENSUS CHECKPOINT — 265 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-26.md`

This deliberately small checkpoint records full-content review of the first two remaining 2026-08-24 R2.7 sources in exact frozen-baseline order.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- live references must be repaired in the eventual coherent move batch rather than rewritten piecemeal now.

## S-264 — `2026-08-24-r2-7-audit-execution-protocol.md`

- **SEMANTIC_BLOCKS:** execution-only R2.7 control plane; fresh-session recovery; per-domain Source Manifest/evidence/bidirectional audit/adversarial/disposition loop; durable forward obligations; human-stop policy; mini-report contract; Connector-only checkpoint discipline; interruption recovery; final reconciliation -> `DESIGN_PROVENANCE / ACTIVE PROCESS EXECUTION OWNER`.
- **CURRENT AUTHORITY:** YES for the operational HOW of the still-open R2.7 audit, but **NO as implementation-facing architecture law**. The document explicitly states that it does not change semantic architecture.
- **SUPERSEDED_BY:** none for its operational R2.7 execution algorithm. Current repository-wide process owners and the active roadmap remain higher-level governance/sequencing owners.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`.
- **LIVE CONSUMERS / REFERENCES:** current R2.7 audit-status/recovery flow, roadmap/task routing and agent continuation instructions; exact repository-wide inbound set pending DCR-016 reference census.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`: an active process protocol would keep implementation planners coupled to audit workflow/history. Moving it to `design/` does not remove its process authority.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none; this file owns process execution, not product/runtime semantics.
- **PLACEMENT NOTE:** its historical mini-report path language uses the pre-refactor taxonomy. Current four-directory placement rules control future artifacts; exact live-path repair belongs to the eventual migration/reference batch.

## S-265 — `2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md`

- **SEMANTIC_BLOCKS:** original Round-2-only/final-stage machine-realization mapping scope; responsibility matrix; persistent/HOT/index/context/Actor/Story/multiplayer/Dramaturg/instruction/bootstrap/test mapping domains; holistic composition review; 82 DIAMOND/STRONG recheck; prospective owner gates; 19 exit criteria -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO. The later whole-project final-audit Task Brief v2 explicitly says it supersedes this file and expands the outer audit boundary from Round-2 machine mapping to the complete accepted HDM architecture/runtime dependency graph.
- **SUPERSEDED_BY:** `2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` (later baseline source S-268).
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** historical R2.7 derivation/scope provenance; current execution must route through Task Brief v2, current roadmap and current durable audit cursor. Exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` because its narrower audit boundary can misroute an implementation-planning readiness review.
- **PROVENANCE_LINK_REQUIRED:** YES, especially from Task Brief v2 supersession history.
- **STRANDED ACCEPTED LAW:** none identified. Material mapping concerns preserved by current R2.7 v2 scope remain carried by that later task owner/current audit artifacts.

## Part-27 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 265
SPECS_REMAINING: 110

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 50 / 57
  2026-08-25: 15 / 55

PART_27_NEW_SOURCES: 2
PART_27_DESIGN_DESTINATIONS: 2
PART_27_RESEARCH_DESTINATIONS: 0
PART_27_FINAL_SPEC_DESTINATIONS: 0
PART_27_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 223
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 36
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_BASELINE_SOURCE:
  S-266  2026-08-24-r2-7-mini-report-template.md
```
