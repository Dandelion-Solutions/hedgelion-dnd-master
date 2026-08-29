# Documentation Corpus Refactor — Specs Census Part 41

Status: **DURABLE CENSUS CHECKPOINT — 312 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-40.md`

This closes the second half of the fully reviewed S6D-05 family and completes the frozen 2026-08-25 specs group. Current semantic authority is `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md`, including the repaired S6D-05 contract and later S6D-09/S6D-10 amendments. The dated chain is design provenance rather than implementation-facing final authority.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; inbound-reference census pending under DCR-016.

## S-309 — `2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-collaborative-review.md`

- **SEMANTIC_BLOCKS:** Step-4 responsibility review and acceptance of the canonical embedded-value direction; downstream human gates for genuinely new targeting/cost/duration/reaction/mutation semantics -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as semantic owner; accepted technical direction is consolidated in current `PORTABLE_ACTIVITY_VALUES.md`.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** candidate/review/resolution chain and current owner.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-collaborative-review.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-05 design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-310 — `2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-decision-brief.md`

- **SEMANTIC_BLOCKS:** Step-3 recommendation for one 19-value embedded-nonowner family; ReactionOffer alignment; minimal Signal/StateDelta roots without lifecycle/disposition; S6D-06 mutation/atomicity boundary; no-human-decision conclusion -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as separate final owner. The file explicitly records no human product decision and its technical result is fully consolidated in the current architecture owner.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed Steps 4–8 and current `PORTABLE_ACTIVITY_VALUES.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-decision-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** candidate/design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-311 — `2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-resolution-gate.md`

- **SEMANTIC_BLOCKS:** Step-7 accepted closure; 19 embedded nonowners; declaration/binding and suspension equality; bounded target/range/area/spatial-unit/cost/duration vocabularies; roll retry reuse; Choice/Reaction currentness; Signal/StateDelta no lifecycle/disposition; S6D-06 mutation-payload routing -> `DESIGN_PROVENANCE / RESOLUTION EVIDENCE`.
- **CURRENT AUTHORITY:** NO as separate implementation law; repaired semantics are carried by the current architecture owner.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-8/current `PORTABLE_ACTIVITY_VALUES.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-resolution-gate.md`.
- **LIVE CONSUMERS / REFERENCES:** canonicalization/design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-312 — `2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-task-brief.md`

- **SEMANTIC_BLOCKS:** Step-1 portable-value problem/scope; embedded-value/nonrecord law; declaration/binding, targeting/area, cost/duration, roll, Choice/Reaction and Signal/StateDelta evidence products; exact Source Manifest; recovery/retry/catalog-context constraints; registry/value/equality/failure/verification ledgers; alternatives; agent/human boundary; eight-step/full-loop exits -> `DESIGN_PROVENANCE / HISTORICAL TASK BRIEF`.
- **CURRENT AUTHORITY:** NO as implementation-facing law. It frames the completed S6D-05 loop and explicitly stops before Step 2/architecture changes.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed S6D-05 chain and current `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-task-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** current-owner design history/S6D provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S6D-05 family and 2026-08-25 closure

```text
FROZEN_FAMILY_SOURCES: 8
FULL_CONTENT_REVIEWED: 8 / 8
DESIGN_DESTINATIONS: 8
FINAL_SPECS_CHAIN_OWNERS_RETAINED: 0
PRIMARY_SEMANTIC_OWNER_OUTSIDE_SPECS:
  DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md
SPLITS_REQUIRED: 0
EXTRACTIONS_REQUIRED: 0
UNRESOLVED_SUPERSESSION: 0

2026-08-25 FROZEN BASELINE: 55
2026-08-25 FULL_CONTENT_REVIEWED: 55 / 55 COMPLETE
```

The current owner preserves the S6D-05 embedded-nonowner model, declarations/bindings, bounded Target/Area/Cost/Duration contracts, roll authority/retry reuse, Choice/Reaction generation/currentness, rejecting Signal/StateDelta roots and commit/outcome authority boundaries. It also incorporates later exact spatial-fact and policy-basis evidence amendments. No dated S6D-05 source is required for ordinary implementation planning.

## Part-41 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 312
SPECS_REMAINING: 63
2026-08-25: 55 / 55 COMPLETE
PART_41_DESIGN_DESTINATIONS: 4
CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 267
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 39
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5
S6D_05: COMPLETE / 8 OF 8 CLASSIFIED
PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_BASELINE_DATE: 2026-08-26
NEXT_BASELINE_ID: S-313
```
