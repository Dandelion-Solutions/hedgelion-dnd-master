# Documentation Corpus Refactor — Specs Census Part 04

Status: **DURABLE CENSUS CHECKPOINT — 87 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Parent census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-census.md`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-03.md`

This ledger records the complete Step-5.1 Frontier Model family. It classifies semantic role only. Physical moves remain deferred until a branch-complete inbound-reference/path-repair mechanism is available.

Common defaults:
- `FULL_CONTENT_REVIEWED: YES`
- `LIVE_CONSUMERS / REFERENCES: PENDING BRANCH-COMPLETE INBOUND-REFERENCE CENSUS`
- `PROVENANCE_LINK_REQUIRED: preserve derivation-chain links when paths are repaired`
- `EXTRACTION_REQUIRED: NO`

## 2026-08-20 — Step 5.1 Frontier Model

### S-079 — `2026-08-20-step-5-1-frontier-model-pre-research-charter.md`
- **SEMANTIC_BLOCKS:** solution-blind pre-research constraints, hypotheses, evidence discipline, counterexamples and escalation conditions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; explicitly fixed before substantive research and not a design decision.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-080 — `2026-08-20-step-5-1-frontier-model-task-brief.md`
- **SEMANTIC_BLOCKS:** operational research assignment, mandatory concept ledger/questions/falsification scenarios and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status `RESEARCH ASSIGNMENT — NOT A DESIGN DECISION`.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-081 — `2026-08-20-step-5-1-frontier-model-research-draft.md`
- **SEMANTIC_BLOCKS:** repository evidence map, concept reclassification, Alternative B recommendation, `CURRENT.last_event_id` retirement recommendation, coherent-source-cut hypothesis and later-slice constraints -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status says research complete but analytical challenge required before Decision Brief.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-082 — `2026-08-20-step-5-1-frontier-model-analytical-challenge.md`
- **SEMANTIC_BLOCKS:** strongest opposing A/D case, consumer tests, narrowing of `frontier` and `coherent source cut`, assumption/reversibility analysis, B-NARROW recommendation -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; challenge/decision preparation only.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-083 — `2026-08-20-step-5-1-frontier-model-decision-brief.md`
- **SEMANTIC_BLOCKS:** owner choice A/B-NARROW/C, fixed findings, allocator clarification, `CURRENT.last_event_id` retirement recommendation and exact requested decision -> `DESIGN_PROVENANCE` / accepted-decision provenance.
- **CURRENT AUTHORITY:** NO as implementation-facing owner; B-NARROW is subsequently approved and consolidated in S-087.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-084 — `2026-08-20-step-5-1-frontier-model-candidate-spec.md`
- **SEMANTIC_BLOCKS:** owner-approved B-NARROW candidate laws/classifications and cross-domain constraints before adversarial amendments -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly pending adversarial review.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-085 — `2026-08-20-step-5-1-frontier-model-adversarial-review.md`
- **SEMANTIC_BLOCKS:** F1–F8 attacks/refinements, rejected generic-frontier concerns and cross-system review -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; no new owner decision, resolutions feed S-086/S-087.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-086 — `2026-08-20-step-5-1-frontier-model-resolution-gate.md`
- **SEMANTIC_BLOCKS:** B-NARROW decision confirmation, item-level F1–F8 disposition, immediate `CURRENT.last_event_id` machine cleanup authorization and canonicalization gate -> `DESIGN_PROVENANCE` / closure evidence.
- **CURRENT AUTHORITY:** NO as separate final contract; S-087 incorporates the decision and refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.

### S-087 — `2026-08-20-step-5-1-frontier-model-canonical-spec.md`
- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — STEP 5.1 CLOSED`.
- **CURRENT AUTHORITY:** YES. Owns B-NARROW two-law discipline, domain-native classification, no implicit cross-domain order, conceptual-only coherent source cut, campaign/live/read-authority separation, allocator separation, `CURRENT.last_event_id` retirement, checkpoint/chronology/Story constraints and later-slice invariants.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`.
- **DUPLICATION_RISK:** LOW; explicit consolidated owner.
- **PROVENANCE_LINK_REQUIRED:** keep S-079..S-086 derivation links valid after eventual move.

## Part-04 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 87
SPECS_REMAINING: 288

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 27 / 92

PART_04_SOURCES: 9
PART_04_DESIGN_DESTINATIONS: 8
PART_04_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_04_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 69
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 13
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

CURRENT_STEP5_1_OWNER:
  specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-20-step-5-2-resumable-runtime-closure-pre-research-charter.md

2026_08_20_REMAINING: 65
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
