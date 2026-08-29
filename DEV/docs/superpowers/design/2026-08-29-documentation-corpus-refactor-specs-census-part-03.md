# Documentation Corpus Refactor — Specs Census Part 03

Status: **DURABLE CENSUS CHECKPOINT — 78 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Parent census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-census.md`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-02.md`

This companion ledger records the complete Step-5.0 authority/contamination family. It classifies semantic role only; physical moves remain deferred until a branch-complete inbound-reference/path-repair mechanism is available.

Common defaults unless overridden below:

- `FULL_CONTENT_REVIEWED: YES`
- `LIVE_CONSUMERS / REFERENCES: PENDING BRANCH-COMPLETE INBOUND-REFERENCE CENSUS`
- `PROVENANCE_LINK_REQUIRED: preserve full-cycle basis links when paths are repaired`
- `EXTRACTION_REQUIRED: NO`

## 2026-08-20 — Step 5.0 Authority / Contamination Audit

### S-073 — `2026-08-20-step-5-0-authority-contamination-task-brief.md`
- **SEMANTIC_BLOCKS:** solution-blind audit scope, fixed constraints, classification model, required questions/challenges/deliverables -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; architectural research brief only. It explicitly forbids pre-deciding later Step-5 slice formats.
- **FINAL_DESTINATION_FILES:** `design/2026-08-20-step-5-0-authority-contamination-task-brief.md`.
- **DUPLICATION_RISK:** LOW after S-078 remains routed as final Step-5.0 owner.

### S-074 — `2026-08-20-step-5-0-authority-contamination-research-draft.md`
- **SEMANTIC_BLOCKS:** verified authority inventory, F-01..F-12 contamination/pointer/class findings, analytical challenge, cleanup recommendations and two proposed owner decisions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status `RESEARCH / ANALYTICAL DRAFT — NOT CANONICAL`. Recommendations are filtered through Decision Brief, Candidate and Adversarial review before S-078.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-075 — `2026-08-20-step-5-0-authority-contamination-decision-brief.md`
- **SEMANTIC_BLOCKS:** owner-choice alternatives for contamination retirement policy and sole latest-checkpoint pointer; derivable cleanup package -> `DESIGN_PROVENANCE` / accepted-decision provenance.
- **CURRENT AUTHORITY:** NO as standalone implementation-facing law. The selected Alternative C decisions are incorporated into S-076 and finally S-078.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-076 — `2026-08-20-step-5-0-authority-contamination-candidate-spec.md`
- **SEMANTIC_BLOCKS:** owner-approved candidate retirement set, timeline clarification, pointer normalization, catalog-version consequences and exit conditions -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly says adversarial review pending. S-077 adds required consistency amendments and S-078 is final resolution.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-077 — `2026-08-20-step-5-0-authority-contamination-adversarial-review.md`
- **SEMANTIC_BLOCKS:** H1–H3, M1–M5, L1–L2 attacks, accidental-capability-loss tests and cleanup gate -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; no new owner decision, amendments are incorporated into S-078 and active machine/template cleanup.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-078 — `2026-08-20-step-5-0-authority-contamination-final.md`
- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; final accepted retirement/normalization law and Step-5.0 carry-forward after owner decisions, adversarial review and active cleanup.
- **CURRENT AUTHORITY:** YES for Step-5.0. It fixes the accepted contamination-retirement rule; retired Secret/tactical/pending/timeline/premature runtime-record surfaces; sole `MANIFEST.last_checkpoint_id` pointer; chronology/event routing normalization; root-layout semantics; preserved owners; catalog `1.6.0`; explicit later-slice obligations.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-5-0-authority-contamination-final.md`.
- **DUPLICATION_RISK:** LOW; final resolution is the consolidated Step-5.0 owner.
- **PROVENANCE_LINK_REQUIRED:** preserve links to S-073..S-077 after their eventual move.

## Part-03 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 78
SPECS_REMAINING: 297

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 18 / 92

PART_03_SOURCES: 6
PART_03_DESIGN_DESTINATIONS: 5
PART_03_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_03_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 61
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 12
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

CURRENT_STEP5_0_OWNER:
  specs/2026-08-20-step-5-0-authority-contamination-final.md

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-20-step-5-1-frontier-model-task-brief.md

2026_08_20_REMAINING: 74
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```

The final Step-5.0 document remains in `specs/` even though it also contains closure/verification material because it is the consolidated accepted owner of the retirement and normalization decisions; the earlier five documents contain the derivation and review chain.
