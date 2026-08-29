# Documentation Corpus Refactor — Specs Census Part 36

Status: **DURABLE CENSUS CHECKPOINT — 292 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-35.md`

First small checkpoint for the fully reviewed S6D-03 family. All eight frozen-baseline S6D-03 specs-chain sources and current `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` were read before disposition. The current architecture owner contains the repaired S6D-03 law plus later S6D-04/S6D-07 amendments, so no dated S6D-03 chain source is the current implementation-facing owner.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; inbound-reference census pending under DCR-016.

## S-289 — `2026-08-25-s6d-03-complete-calculation-selector-metadata-adversarial-review.md`

- **SEMANTIC_BLOCKS:** Step-6 review; rejection of circular example-driven activation; ENGINE_STATE-only repair; exact empty fact allowlists; dormancy of unresolved resolver/value semantics; dependency-kind normalization; PASS -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as implementation-facing law; repairs are consolidated in current selector-metadata owner.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-7/8 and `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-03-complete-calculation-selector-metadata-adversarial-review.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-03 design chain/current-owner provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-290 — `2026-08-25-s6d-03-complete-calculation-selector-metadata-brief-critic.md`

- **SEMANTIC_BLOCKS:** Step-1 critic; separate per-operation ledger; exact operation set equality; selector-operation compatibility vs S6D-05 payload boundary; final PASS -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as semantic architecture owner; it is framing/process evidence and performed no selector decision.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** repaired Task Brief and completed S6D-03 chain.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-03-complete-calculation-selector-metadata-brief-critic.md`.
- **LIVE CONSUMERS / REFERENCES:** Task Brief/design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-291 — `2026-08-25-s6d-03-complete-calculation-selector-metadata-candidate-spec.md`

- **SEMANTIC_BLOCKS:** Step-5 repaired candidate; initial 3-selector/2-operation active surface; selectability law; complete metadata; active contracts; deterministic policies; ENGINE_STATE/fact/dependency boundary; dormancy; failure/trace; coordinated changes/verification -> `DESIGN_PROVENANCE / SUPERSEDED CANDIDATE`.
- **CURRENT AUTHORITY:** NO. Candidate names `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md` as semantic owner; current owner now additionally carries S6D-07 finite extension to 10 selectors/3 operations and S6D-04 closure.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** current `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-03-complete-calculation-selector-metadata-candidate-spec.md`.
- **LIVE CONSUMERS / REFERENCES:** review/resolution/canonicalization provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH because its exact active roster is point-in-time and no longer current.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-292 — `2026-08-25-s6d-03-complete-calculation-selector-metadata-canonicalization.md`

- **SEMANTIC_BLOCKS:** Step-8 closure; explicit canonical owner pointer; machine-artifact list; point-in-time 3/2 result and next-step status -> `DESIGN_PROVENANCE / CANONICALIZATION-CLOSURE EVIDENCE`.
- **CURRENT AUTHORITY:** NO as separate semantic owner. It explicitly points to `CALCULATION_SELECTOR_METADATA.md`.
- **SUPERSEDED_BY / CURRENT OWNER:** current selector-metadata architecture owner; roadmap/integrated S6D closure for live status.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-03-complete-calculation-selector-metadata-canonicalization.md`.
- **LIVE CONSUMERS / REFERENCES:** current-owner design history/S6D closure; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH because its 3/2 point-in-time roster is superseded by current 10/3 roster.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## Part-36 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 292
SPECS_REMAINING: 83
2026-08-25: 35 / 55
PART_36_DESIGN_DESTINATIONS: 4
CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 247
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 39
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5
S6D_03_FULL_FAMILY_READ: 8 / 8
S6D_03_PRIMARY_OWNER_CHECKED: DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md
PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_BASELINE_SOURCE: S-293  2026-08-25-s6d-03-complete-calculation-selector-metadata-collaborative-review.md
```
