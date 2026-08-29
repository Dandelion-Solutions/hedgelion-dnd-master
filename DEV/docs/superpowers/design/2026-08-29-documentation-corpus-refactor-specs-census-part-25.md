# Documentation Corpus Refactor — Specs Census Part 25

Status: **DURABLE CENSUS CHECKPOINT — 256 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-24.md`

This checkpoint records full-content review of the six previously uncounted 2026-08-24 R2.5 Collaboration / Multiplayer derivation artifacts. The R2.5 canonical specification and resolution gate were already fully reviewed and counted early as **S-149** and **S-150** in Specs Census Part 11. They are revalidated here only as current-owner/closure evidence and are not recounted.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` for the canonicalization/decision chain.

## Authority / consolidation result

The original Decision Brief proposed a narrower scoped collective window. Decision Brief v2 explicitly superseded it for the owner decision and introduced the final **B3 — Agency-Safe Scoped Collaboration + Two-Level Dramaturg Coordination** architecture:

- positive bounded agency dependency and maximal safe frontier rather than transport-order progression or universal waiting;
- scoped collective contribution persistence only when no native rules owner already owns responder/order semantics;
- input-class separation and recipient-scoped join/rejoin/catch-up;
- player-local retained noncanonical Dramaturg horizons plus one multiplayer-only shared horizon;
- preparation has no entitlement to occur; canon invalidates preparation, never the reverse;
- lazy planning retrieval/revalidation and no background global rewrite.

The owner approved B3. The adversarial review added fourteen required corrections covering false waiting, currentness before contributor enrollment, visible maximal-safe-frontier protection, purpose/scope/generation-bound contribution reuse, collaboration-generation supersession, shared-horizon CAS/rebase, revisable provisional direction, multiplayer lifecycle, planning/catch-up secrecy, planning-loss nonauthority, Story/planning lifecycle separation, cross-player containment assurance, bounded planning consistency and planning-relevance-vs-causality.

Already-counted S-149 fully incorporates B3 and AR-1..AR-14. Already-counted S-150 confirms closure and is process provenance. No accepted R2.5 implementation-facing law remains stranded in the six sources classified here.

## S-251 — `2026-08-24-r2-5-collaboration-multiplayer-task-brief.md`

- **SEMANTIC_BLOCKS:** collaboration/input-layer problem above existing Step-5 multiplayer owners; authority/scope/input/async/join/rejoin/catch-up/split-party/TurnEnvelope questions; Source Manifest; D21/D22/D23/S43/S44/S45/S54; inherited constraints; negative/YAGNI boundaries and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; task/process framing only.
- **SUPERSEDED_BY:** S-149 canonical specification for accepted law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained beside final law because it contains unresolved product questions and pre-B3 alternatives.
- **STRANDED ACCEPTED LAW:** none.

## S-252 — `2026-08-24-r2-5-collaboration-multiplayer-decision-brief.md`

- **SEMANTIC_BLOCKS:** original alternatives A immediate-only / B scoped collaboration window + catch-up / C campaign collaboration queue; recommended B; three coordination families; closure/agency/input/join/catch-up/split-party laws and D/S dispositions -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO. S-253 explicitly supersedes this brief for owner decision and materially strengthens agency waiting plus Dramaturg coordination.
- **SUPERSEDED_BY:** S-253/S-254 and ultimately S-149.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained because its selected Alternative B is not the final owner-approved B3 architecture.

## S-253 — `2026-08-24-r2-5-collaboration-multiplayer-decision-brief-v2.md`

- **SEMANTIC_BLOCKS:** B3 alternatives; maximal safe frontier; bounded agency-dependent collaboration; input classes; two-level player-local/shared Dramaturg coordination; no-entitlement/no-plot-restoration law; lazy planning discovery/rebase; join/rejoin/catch-up; split-party composition; proposed laws and narrow S14 activation -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; S-254 records owner choice and S-149 consolidates it plus AR-1..AR-14.
- **SUPERSEDED_BY:** S-254 historical approval and S-149 current implementation-facing law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH as a near-final pre-adversarial law carrier.
- **STRANDED ACCEPTED LAW:** none.

## S-254 — `2026-08-24-r2-5-collaboration-multiplayer-owner-decision.md`

- **SEMANTIC_BLOCKS:** owner approval of B3; maximal-safe-frontier agency semantics; scoped collective input; player-local + multiplayer-only shared Dramaturg horizons; explicit `HISTORY IS NOT WRITTEN IN ADVANCE`; canon-invalidates-preparation/no-plot-restoration; lazy planning retrieval; authority separation; narrow S14 trigger activation and candidate mandate -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary, fully consolidated by S-149.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-149 carries the owner decisions and later AR safeguards.
- **SUPERSEDED_BY:** S-149 as compact current carrier; consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained as coequal owner because it predates fourteen final adversarial clarifications.
- **STRANDED ACCEPTED LAW:** none.

## S-255 — `2026-08-24-r2-5-collaboration-multiplayer-candidate-spec.md`

- **SEMANTIC_BLOCKS:** candidate coordination families, maximal safe frontier, scoped contribution lifecycle/input classes/join-rejoin, local/shared Dramaturg horizons, preparation nonauthority/no-restoration, lazy planning/currentness, split-party composition, TurnEnvelope behavior, failure/currentness behavior, D/S dispositions and adversarial attack requirements -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; AR-1..AR-14 remain outstanding in this version.
- **SUPERSEDED_BY:** S-149 after S-256 refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH because its law text closely resembles final architecture while missing contributor/generation/planning-concurrency/secrecy safeguards.

## S-256 — `2026-08-24-r2-5-collaboration-multiplayer-adversarial-review.md`

- **SEMANTIC_BLOCKS:** AR-1..AR-14 over positive dependency proof, currentness, visible consequence frontier, contribution purpose/generation binding, supersession, shared-horizon lost-update fencing, soft-railroad risk, multiplayer mode transition, catch-up planning leakage, planning-loss recovery, Story/planning lifecycle, cross-player containment, bounded consistency and planning-vs-causal bridge -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all amendments are incorporated into S-149 and closure confirmed by S-150.
- **SUPERSEDED_BY:** S-149 current law and S-150 closure evidence.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; useful adversarial provenance rather than normal implementation input.
- **STRANDED ACCEPTED LAW:** none.

## Existing S-149 / S-150 revalidation

### S-149 — R2.5 canonical specification

- **RECOUNT:** NO; already counted in Part 11.
- **CURRENT AUTHORITY:** YES.
- **REVALIDATION:** full canonical law incorporates owner-approved B3 and AR-1..AR-14, preserves existing Step-5 live/currentness/chronology authority, and hands concrete assurance/machine-mapping obligations to R2.6/R2.7.
- **DESTINATION:** unchanged `specs/`.

### S-150 — R2.5 resolution gate

- **RECOUNT:** NO; already counted in Part 11.
- **CURRENT AUTHORITY:** NO as a separate law carrier; closure/process evidence.
- **DESTINATION:** corresponding `design/` path under its already-recorded Part-11 disposition.

## R2.5 family result

```text
R2_5_BASELINE_SPECS_SOURCES:                  8
R2_5_ALREADY_REVIEWED:                        2  # S-149/S-150
R2_5_NEW_SOURCES_THIS_PART:                   6
R2_5_NEW_DESIGN_DESTINATIONS:                 6
R2_5_NEW_FINAL_SPEC_DESTINATIONS:             0
R2_5_SPLITS_REQUIRED:                         0
R2_5_EXTRACTIONS_REQUIRED:                    0
R2_5_STRANDED_ACCEPTED_LAW:                   0
R2_5_UNRESOLVED_SUPERSESSION:                 0

KEEP_IN_SPECS:
  S-149  2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md

MOVE_TO_DESIGN:
  S-150, S-251..S-256
```

No new DCR conflict/debt item is required.

## Part-25 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 256
SPECS_REMAINING: 119

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 41 / 57
  2026-08-25: 15 / 55

PART_25_NEW_SOURCES: 6
PART_25_DESIGN_DESTINATIONS: 6
PART_25_RESEARCH_DESTINATIONS: 0
PART_25_FINAL_SPEC_DESTINATIONS: 0
PART_25_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 215
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 35
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  2026-08-24 R2.6 ChatGPT Plus / MVP Host Assurance
```
