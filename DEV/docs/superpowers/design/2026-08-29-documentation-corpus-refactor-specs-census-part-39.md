# Documentation Corpus Refactor — Specs Census Part 39

Status: **DURABLE CENSUS CHECKPOINT — 304 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-38.md`

This closes the second half of the fully reviewed S6D-04 family. Current semantic authority is `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`, including repaired S6D-04 law and later S6D-09/S6D-10 amendments. The dated design chain is therefore provenance, not an implementation-facing final source.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; inbound-reference census pending under DCR-016.

## S-301 — `2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-collaborative-review.md`

- **SEMANTIC_BLOCKS:** Step-4 review; conservative dormancy/bound-DAG acceptance; technical-vs-human responsibility split; downstream valued-Condition/fact-consumer/Effect-owner gates -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as semantic owner; the accepted direction is consolidated in current `MECHANICAL_CONTEXT.md`.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** candidate/review/resolution chain and current owner.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-collaborative-review.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-04 design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-302 — `2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-decision-brief.md`

- **SEMANTIC_BLOCKS:** Step-3 facts and conservative dormancy recommendation; exact 9-active-accessor/1-dormant-accessor and 4-internal-node point-in-time direction; one hydrated bound-instance DAG; deferred fact/value semantics; no-human-gate conclusion -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as separate final decision owner. It explicitly records no human product decision and defers genuine semantic choices downstream.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed Steps 4–8 and current mechanical-context owner.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-decision-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** design/candidate provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH because later S6D-09 activates bounded reachability use.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-303 — `2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-resolution-gate.md`

- **SEMANTIC_BLOCKS:** Step-7 acceptance after adversarial repair; canonical-owner/machine/synchronized-owner/test routing; point-in-time dormant `condition.value` and facts; no-open-risk gate -> `DESIGN_PROVENANCE / RESOLUTION EVIDENCE`.
- **CURRENT AUTHORITY:** NO as implementation-facing law; current owner carries repaired semantics plus later amendments.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-8/current `MECHANICAL_CONTEXT.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-resolution-gate.md`.
- **LIVE CONSUMERS / REFERENCES:** canonicalization/design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH due point-in-time fact disposition.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-304 — `2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-task-brief.md`

- **SEMANTIC_BLOCKS:** Step-1 exact 10-accessor/2-fact/4-node problem; accessor/fact/query/input authority boundaries; S6D-04 semantic vs S6D-05 portable realization split; recovery/retry/checkpoint/GC preservation; item ledgers, consumer matrix, bound graph, missing/failure/query-exclusion evidence products; questions/alternatives; human boundary; exit gates -> `DESIGN_PROVENANCE / HISTORICAL TASK BRIEF`.
- **CURRENT AUTHORITY:** NO as implementation-facing law. It frames the completed design loop and explicitly does not decide items or machine contracts.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed S6D-04 chain and current `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-task-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** current-owner design history/S6D provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S6D-04 family closure

```text
FROZEN_BASELINE_SOURCES: 8
FULL_CONTENT_REVIEWED: 8 / 8
DESIGN_DESTINATIONS: 8
FINAL_SPECS_CHAIN_OWNERS_RETAINED: 0
PRIMARY_SEMANTIC_OWNER_OUTSIDE_SPECS:
  DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md
SPLITS_REQUIRED: 0
EXTRACTIONS_REQUIRED: 0
UNRESOLVED_SUPERSESSION: 0
```

The current owner preserves the exact registry/metadata authority split, missing-not-false law, exact consumer/fact permissions, one bound-instance DAG, pinned-view/cache/recovery contract, runtime-query exclusion and failure mapping. Later amendments activate `fiction.target_reachable` only for seven exact S6D-09 consumers and add S6D-10 policy-basis retention without reopening S6D-04 fundamentals.

## Part-39 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 304
SPECS_REMAINING: 71
2026-08-25: 47 / 55
PART_39_DESIGN_DESTINATIONS: 4
CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 259
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 39
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5
S6D_04: COMPLETE / 8 OF 8 CLASSIFIED
PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_BASELINE_FAMILY: 2026-08-25 S6D-05 — Activity Parameters / Targeting / Costs / Portable Values
NEXT_BASELINE_ID: S-305
```
