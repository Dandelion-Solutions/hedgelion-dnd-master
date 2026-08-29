# Documentation Corpus Refactor — Specs Census Part 29

Status: **DURABLE CENSUS CHECKPOINT — 269 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-28.md`

Small checkpoint for the next two 2026-08-24 R2.7 baseline sources in exact frozen order.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; repository-wide inbound-reference census remains pending under DCR-016.

## S-268 — `2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`

- **SEMANTIC_BLOCKS:** active whole-project R2.7 scope/task definition; 27-domain minimum; bidirectional architecture->machine and machine->architecture proof; full repository machine/runtime/bootstrap/migration/release/test coverage; required audit artifacts; human-gate criteria; 24 exit criteria -> `DESIGN_PROVENANCE / ACTIVE TASK OWNER`.
- **CURRENT AUTHORITY:** YES for current R2.7 task scope/execution target, but NO as final implementation-facing architecture law. It is a Task Brief by semantic role and explicitly derives from owner clarification/current architecture.
- **SUPERSEDES:** S-265 original Round-2-centered machine-realization brief.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`.
- **LIVE CONSUMERS / REFERENCES:** active R2.7 audit protocol/status/roadmap/WP reporting and continuation; exact inbound set pending DCR-016.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because implementation planners would continue to consume active audit workflow/scope as if it were accepted product/runtime specification.
- **PROVENANCE_LINK_REQUIRED:** YES to S-267 owner clarification and superseded S-265.
- **STRANDED ACCEPTED LAW:** none; accepted clean-slate structural authorization remains in S-267, while this file continues to own active audit scope from `design/`.

## S-269 — `2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md`

- **SEMANTIC_BLOCKS:** owner-approved progressive PC materialization semantics; early `PROVISIONAL_IDENTITY`; Actor identity/name/concept distinction; READY_PC as initial mechanical commitment frontier; initialization precedence; anti-retrofit/safe-laziness law; minimum READY_PC outcome; onboarding latency principle; sparse early persistence; exact downstream alignment/test obligations -> `FINAL_SPEC_OR_ACCEPTED_DECISION`.
- **CURRENT AUTHORITY:** YES. Current `DEV/ARCHITECTURE/ACTOR_MODEL.md` explicitly lists this clarification as an **owning addition**. S6D-07 canonical owner narrows and realizes READY_PC/build/seed contracts but does not declare this owner superseded.
- **SUPERSEDED_BY:** none found. Current `ACTOR_MODEL.md` and `CHARACTER_PROGRESSION_READY_PC_SEED.md` consume/consolidate its semantics while preserving its owner role.
- **FINAL_DESTINATION_FILES:** unchanged `DEV/docs/superpowers/specs/2026-08-24-r2-7-wp-04-progressive-ready-pc-owner-clarification.md`.
- **LIVE CONSUMERS / REFERENCES:** `ACTOR_MODEL.md`; world-actor schema/catalog; character/onboarding/readiness/durability CORE; S6D-07 architecture/machine owner and focused tests; future WP-19/WP-22/WP-26 obligations; exact inbound set pending.
- **DUPLICATION_RISK:** MEDIUM because later architecture docs restate/consolidate many laws, but they explicitly preserve this clarification as an owning addition rather than presenting an independent conflicting source.
- **PROVENANCE_LINK_REQUIRED:** YES to WP-04 audit evidence and later S6D-07 realization.
- **STRANDED ACCEPTED LAW:** none while the clarification remains in `specs/`.

## Part-29 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 269
SPECS_REMAINING: 106

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 54 / 57
  2026-08-25: 15 / 55

PART_29_NEW_SOURCES: 2
PART_29_DESIGN_DESTINATIONS: 1
PART_29_FINAL_SPEC_OR_OWNER_DESTINATIONS: 1

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 225
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 38
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_BASELINE_SOURCE:
  S-270  2026-08-24-round-2-roadmap-owner-decision.md
```
