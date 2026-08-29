# Documentation Corpus Refactor — Specs Census Part 43

Status: **DURABLE CENSUS CHECKPOINT — 320 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-42.md`

This closes the second half of the fully reviewed S6D-06 family. Current semantic authority is `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` plus its catalog/schema/test realization. The dated chain is design provenance and historical closure evidence; no dated S6D-06 source remains necessary as ordinary implementation-facing law.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; inbound-reference census pending under DCR-016.

## S-317 — `2026-08-26-s6d-06-registered-activity-primitive-contracts-collaborative-review.md`

- **SEMANTIC_BLOCKS:** Step-4 whole-subgraph review; 31 quarantines; closed read allowlists; primitive-local prospective outputs rather than StateDelta lifecycle; bounded compiler forms; reuse of accepted suspension/publication owners -> `DESIGN_PROVENANCE / COLLABORATIVE REVIEW`.
- **CURRENT AUTHORITY:** NO as semantic owner. These accepted technical constraints are carried by current `ACTIVITY_PRIMITIVE_CONTRACTS.md`.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** candidate, adversarial review, resolution/canonicalization and current architecture owner.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-06-registered-activity-primitive-contracts-collaborative-review.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-06 design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-318 — `2026-08-26-s6d-06-registered-activity-primitive-contracts-decision-brief.md`

- **SEMANTIC_BLOCKS:** Step-3 evidence-constrained decision to quarantine all 31 registered primitives; future COMPLETE replacement + exact consumer/dependency/admission requirements; rejection of generic query/event/delta/implicit-RNG/global-atomicity surfaces -> `DESIGN_PROVENANCE / TECHNICAL DECISION BRIEF`.
- **CURRENT AUTHORITY:** NO as a separate final owner. The file states no product decision was required, and its technical closure is fully represented in current architecture/machine owners.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Steps 4–8 and current `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-06-registered-activity-primitive-contracts-decision-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-06 design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-319 — `2026-08-26-s6d-06-registered-activity-primitive-contracts-resolution-gate.md`

- **SEMANTIC_BLOCKS:** Step-7 ACCEPT gate; 31/31 explicit fail-closed quarantines; zero execution authority; zero blocking/significant findings; replacement requirements; no human decision -> `DESIGN_PROVENANCE / RESOLUTION EVIDENCE`.
- **CURRENT AUTHORITY:** NO as current executable-disposition owner. The accepted closure snapshot is historical and later selectively amended by S6D-07/S6D-09 in the current owner.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-8 and current `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-06-registered-activity-primitive-contracts-resolution-gate.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D closure provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` as though its 31/0 snapshot were current.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-320 — `2026-08-26-s6d-06-registered-activity-primitive-contracts-task-brief.md`

- **SEMANTIC_BLOCKS:** Step-1 problem/scope for all 31 primitive IDs; exact argument/result/read/mutation/RNG/binding/export/atomicity/failure/suspension evidence requirements; owner/source manifest; primitive/admission/contract/read-mutation/control-flow/RNG/atomicity/failure/verification matrices; alternatives; agent/human boundary; eight-step/full-loop exits -> `DESIGN_PROVENANCE / HISTORICAL TASK BRIEF`.
- **CURRENT AUTHORITY:** NO as implementation-facing law. It is the framing artifact for a completed design loop and explicitly stops before Step 2.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed S6D-06 chain and current `DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md` plus machine companions.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-06-registered-activity-primitive-contracts-task-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-06 design/process provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S6D-06 family closure

```text
FROZEN_FAMILY_SOURCES: 8
FULL_CONTENT_REVIEWED: 8 / 8
DESIGN_DESTINATIONS: 8
FINAL_SPECS_CHAIN_OWNERS_RETAINED: 0
PRIMARY_SEMANTIC_OWNER_OUTSIDE_SPECS:
  DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md
SPLITS_REQUIRED: 0
EXTRACTIONS_REQUIRED: 0
UNRESOLVED_SUPERSESSION: 0
```

The current owner preserves the original S6D-06 31-row quarantine closure and exact activation/admission law, then explicitly records later selective replacements and narrowing. No accepted implementation-facing law would be stranded by moving all eight dated S6D-06 sources to `design/`.

## Part-43 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 320
SPECS_REMAINING: 55
2026-08-26 FROZEN BASELINE: 26
2026-08-26 FULL_CONTENT_REVIEWED/CLASSIFIED: 8 / 26
PART_43_DESIGN_DESTINATIONS: 4
CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 275
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 39
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5
S6D_06: COMPLETE / 8 OF 8 CLASSIFIED
PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_BASELINE_ID: S-321
NEXT_BASELINE_SOURCE: 2026-08-26-s6d-07-character-progression-ready-pc-seed-adversarial-review.md
```
