# Documentation Corpus Refactor — Specs Census Part 28

Status: **DURABLE CENSUS CHECKPOINT — 267 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-27.md`

This deliberately small checkpoint records full-content review of the next two 2026-08-24 R2.7 baseline sources in exact frozen-baseline order.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.

## S-266 — `2026-08-24-r2-7-mini-report-template.md`

- **SEMANTIC_BLOCKS:** mandatory R2.7 mini-report evidence/checkpoint sections; domain question disposition; Source Manifest delta; fact/constraint/decision accounting; architecture->machine and machine->architecture tables; findings; automatically derived technical decisions; implementation/verification/forward obligations; D/S delta; human gate; closure/continuation forms -> `DESIGN_PROVENANCE / ACTIVE REPORTING TEMPLATE`.
- **CURRENT AUTHORITY:** YES for current R2.7 report shape, but the document explicitly states that a mini-report is an evidence/checkpoint artifact rather than a semantic owner.
- **SUPERSEDED_BY:** none for report shape. Current four-directory taxonomy supersedes its old placement assumption where any live path still routes routine audit artifacts to `research/`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-24-r2-7-mini-report-template.md`.
- **LIVE CONSUMERS / REFERENCES:** R2.7 execution protocol and active/future WP audit reporting; exact inbound set pending DCR-016.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because it is an active design/audit workflow template, not an implementation-facing specification.
- **PROVENANCE_LINK_REQUIRED:** YES from the execution protocol/current R2.7 process routing.
- **STRANDED ACCEPTED LAW:** none; current report-process requirements remain usable from `design/`.

## S-267 — `2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`

- **SEMANTIC_BLOCKS:** owner-approved widening of R2.7 to whole-project final architecture/machine-realization audit; complete coverage horizon; mandatory bidirectional architecture<->machine proof; project-wide physical/instruction scope; nesting of Round-2 evidence; explicit supersession of the narrower original brief; implementation gate; owner-approved clean-slate prerelease compatibility policy; direct structural-canonicalization authorization and limits -> `FINAL_SPEC_OR_ACCEPTED_DECISION`.
- **CURRENT AUTHORITY:** YES. Task Brief v2 carries the widened audit scope, but does not replace the complete owner-approved prerelease compatibility/structural-canonicalization decision. The active roadmap still lists this clarification as a primary program decision and restates its clean-slate rule while routing detailed semantics to owning specifications.
- **SUPERSEDED_BY:** none found for the complete decision. Later S6D/R2.7 work consumes it; current roadmap preserves it.
- **FINAL_DESTINATION_FILES:** unchanged `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`.
- **LIVE CONSUMERS / REFERENCES:** Task Brief v2, R2.7 execution/audit domains, S6D clean-slate correction, current roadmap, structural machine-contract canonicalization and later WP-20 future-compatibility boundary; exact inbound set pending.
- **DUPLICATION_RISK:** MEDIUM because roadmap contains a compact derivative summary, but roadmap is sequencing/status authority and explicitly routes detailed semantics to owners; it is not a duplicate semantic owner.
- **PROVENANCE_LINK_REQUIRED:** YES to the superseded original brief and Task Brief v2.
- **STRANDED ACCEPTED LAW:** none while this owner decision remains in `specs/`.

## Part-28 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 267
SPECS_REMAINING: 108

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 52 / 57
  2026-08-25: 15 / 55

PART_28_NEW_SOURCES: 2
PART_28_DESIGN_DESTINATIONS: 1
PART_28_RESEARCH_DESTINATIONS: 0
PART_28_FINAL_SPEC_OR_OWNER_DESTINATIONS: 1
PART_28_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 224
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 37
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_BASELINE_SOURCE:
  S-268  2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md
```
