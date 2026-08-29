# Documentation Corpus Refactor — Specs Census Part 21

Status: **DURABLE CENSUS CHECKPOINT — 227 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-20.md`

This checkpoint records full-content review of the six previously uncounted 2026-08-24 R2.1 Continuity / Memory / History derivation artifacts. The R2.1 canonical specification was already fully reviewed and counted early as **S-169** in Specs Census Part 14 and is revalidated here only as the later/final authority; it is not counted again.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` because S-169 explicitly names the derivation chain.

## Authority / consolidation result

The owner selected **B — REUSE-FIRST STORY/HISTORY CONTINUITY PROJECTIONS**. The canonical S-169 fully carries that decision and all approved direction, then incorporates adversarial clarifications AR-1..AR-3 and expands the final law set through R2.1-15.

S-169 also preserves the rejected/conditional alternatives and exact reopen triggers. Therefore no accepted R2.1 law is stranded in the Task Brief, Decision Brief, owner decision, candidate, adversarial review or resolution gate. The separate owner-decision artifact remains valuable decision provenance but is not required as a second implementation-facing authority after canonical consolidation.

Current R2.1 implementation-facing owner remains:

`specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` — S-169.

## S-222 — `2026-08-24-r2-1-continuity-memory-history-task-brief.md`

- **SEMANTIC_BLOCKS:** R2.1 problem/scope, continuity classes to investigate, owner/lifecycle/history-alignment/exactness questions, non-goals, inherited laws, Source Manifest, evidence-ledger requirements, adversarial challenges, alternatives A/B/C and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; task framing/process owner only.
- **SUPERSEDED_BY:** S-169 for accepted R2.1 law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** R2.1 evidence/decision/candidate chain and S-169 derivation list; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because research questions and unselected alternatives sit beside final law.
- **STRANDED ACCEPTED LAW:** none.

## S-223 — `2026-08-24-r2-1-continuity-projection-decision-brief.md`

- **SEMANTIC_BLOCKS:** facts F1..F5, alternatives A dedicated continuity subsystem / B reuse-first / C on-demand-only, recommendation B, proposed L1..L12 direction, downstream consequences and deferred/rejected options -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly owner decision required.
- **SUPERSEDED_BY:** S-224 for the human choice and S-169 for current integrated law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained because A/C and recommendation text could be confused with selected architecture.
- **STRANDED ACCEPTED LAW:** none.

## S-224 — `2026-08-24-r2-1-continuity-projection-owner-decision.md`

- **SEMANTIC_BLOCKS:** owner approval of Alternative B; approved L1..L12 direction; preserved product semantics; rejected/conditional choices; stage boundaries and authorization to continue design -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary, now fully consolidated by S-169.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-169 explicitly names this decision, reproduces the selected source/lifecycle model, approved laws, rejected/conditional alternatives and reopen triggers, then adds required adversarial clarifications.
- **SUPERSEDED_BY:** S-169 as the compact current implementation-facing carrier. This is consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** S-225..S-227 and S-169 derivation; exact inbound set pending.
- **DUPLICATION_RISK:** MEDIUM/HIGH if retained as coequal current owner: implementation planning would have to reconcile the pre-adversarial L1..L12 decision record with the final L1..L15 canonical law.
- **STRANDED ACCEPTED LAW:** none.

## S-225 — `2026-08-24-r2-1-continuity-history-candidate-spec.md`

- **SEMANTIC_BLOCKS:** reuse-first source/lifecycle model; candidate R2.1-1..12 laws; stability/consolidation; provenance/coverage; history alignment/correction; generative projection validation; repair/rebuild/retirement; broad/episodic/entity/exact continuity; Story/Chronicler consumer edge; downstream contracts; rejected/conditional alternatives and reopen triggers -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; adversarial review requires AR-1 material-role escalation, AR-2 source-bound != current and AR-3 projection absence != semantic absence before closure.
- **SUPERSEDED_BY:** S-169 after S-226/S-227 refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` because its law text closely resembles final law while missing three material clarifications.
- **STRANDED ACCEPTED LAW:** none.

## S-226 — `2026-08-24-r2-1-continuity-adversarial-review.md`

- **SEMANTIC_BLOCKS:** 24 attacks covering stale Story/current state, source/currentness confusion, eligibility leakage, Actor cognition, derivative self-amplification, host Retry/Edit contamination, exact recall, Story absence, projection-generation compatibility, source correction, duplicate entity memory, whole-history preload, background worker dependency, structurally valid semantic defects and projection absence; AR-1..AR-3 required clarification set -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all three required clarifications are incorporated in S-169.
- **SUPERSEDED_BY:** S-227 closure confirmation and S-169 for current law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; retaining it under final specs pollutes implementation discovery with attack/process detail.
- **STRANDED ACCEPTED LAW:** none. AR-1 maps to final R2.1-5, AR-2 to R2.1-6, AR-3 to R2.1-11/coverage law.

## S-227 — `2026-08-24-r2-1-continuity-resolution-gate.md`

- **SEMANTIC_BLOCKS:** closure verdict, Task-Brief exit matrix, active research-item accounting, AR-1..AR-3 closure mapping, deferred/conditional work, inherited-law preservation and historical R2.1->R2.2 stage transition -> `DESIGN_PROVENANCE / closure evidence`.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner; the gate points to S-169 for law and contains historical stage/status plus completeness evidence.
- **SUPERSEDED_BY:** S-169 for semantic law; current roadmap for current live sequencing/status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM if retained: useful audit evidence, but not required ordinary implementation input.
- **STRANDED ACCEPTED LAW:** none.

## R2.1 family result

```text
R2_1_BASELINE_SPECS_SOURCES:                   7
R2_1_ALREADY_REVIEWED_CURRENT_OWNER:           1  # S-169
R2_1_NEW_SOURCES_THIS_PART:                    6
R2_1_NEW_DESIGN_DESTINATIONS:                  6
R2_1_NEW_RESEARCH_DESTINATIONS:                0
R2_1_NEW_CURRENT_SPEC_DESTINATIONS:            0
R2_1_SPLITS_REQUIRED:                          0
R2_1_EXTRACTIONS_REQUIRED:                     0
R2_1_STRANDED_ACCEPTED_LAW:                    0
R2_1_UNRESOLVED_SUPERSESSION:                  0

KEEP_IN_SPECS_CURRENT_OWNER:
  S-169  2026-08-24-r2-1-continuity-history-canonical-spec.md

MOVE_TO_DESIGN:
  S-222..S-227
```

No new DCR conflict/debt item is required.

## Part-21 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 227
SPECS_REMAINING: 148

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 12 / 57
  2026-08-25: 15 / 55

PART_21_NEW_SOURCES: 6
PART_21_DESIGN_DESTINATIONS: 6
PART_21_RESEARCH_DESTINATIONS: 0
PART_21_NEW_FINAL_SPEC_DESTINATIONS: 0
PART_21_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 189
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 32
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  2026-08-24 R2.2 Actor Continuity / Cognition
```
