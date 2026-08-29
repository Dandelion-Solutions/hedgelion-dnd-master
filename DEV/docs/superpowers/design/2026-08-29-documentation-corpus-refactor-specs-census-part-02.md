# Documentation Corpus Refactor — Specs Census Part 02

Status: **DURABLE CENSUS CHECKPOINT — 72 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Parent census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-census.md`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-01.md`

This companion ledger records item-level semantic review of the first coherent 2026-08-20 slice: the two pre-Step-5 general artifacts and the complete Step-4 architecture chain. It does not establish architecture law. Physical moves still require an inbound-reference/path-repair pass; GitHub code search is not treated as branch-complete evidence for this non-default branch.

Common defaults unless overridden below:

- `FULL_CONTENT_REVIEWED: YES`
- `LIVE_CONSUMERS / REFERENCES: PENDING BRANCH-COMPLETE INBOUND-REFERENCE CENSUS`
- `PROVENANCE_LINK_REQUIRED: preserve current-owner/canonicalization chain when paths are repaired`
- `EXTRACTION_REQUIRED: NO`
- no physical move is authorized by this ledger entry alone unless references can be repaired coherently in the same migration slice.

## 2026-08-20 — general / pre-Step-5

### S-061 — `2026-08-20-llm-logical-roles-draft.md`
- **SEMANTIC_BLOCKS:** six-role logical decomposition, role/context envelopes, non-authority boundaries, Step-4/6 open questions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as an independent contract; status is `DRAFT — ROLE SET APPROVED IN PRINCIPLE / INDIVIDUAL CONTRACTS NOT YET CANONICAL` and the accepted role semantics are consolidated by S-071.
- **FINAL_DESTINATION_FILES:** `design/2026-08-20-llm-logical-roles-draft.md`.
- **DUPLICATION_RISK:** LOW after S-071 remains routed as the current Step-4 owner. Later role-containment amendments may extend S-071 but do not make this draft a normative owner.

### S-062 — `2026-08-20-project-map-retrospective-hotfix-review.md`
- **SEMANTIC_BLOCKS:** bounded retrospective repository-discovery audit, five applied hot-fix findings, TDD/verification evidence, procedural lesson -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; document explicitly does not reopen Steps 1–5.1 and records cleanup of already-decided semantics.
- **FINAL_DESTINATION_FILES:** `design/2026-08-20-project-map-retrospective-hotfix-review.md`.
- **DUPLICATION_RISK:** LOW; active source changes remain in their actual owners.

## 2026-08-20 — initial Step-4 framing

### S-063 — `2026-08-20-step-4-lore-knowledge-story-research-draft.md`
- **SEMANTIC_BLOCKS:** repository evidence, external sanity checks, alternatives T/K/D/S, first Alternative-C recommendation, Story/promotion/migration analysis -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status requires human decision before candidate spec and later rerun/canonicalization supersedes conflicting wording.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after S-071 routing.

### S-064 — `2026-08-20-step-4-lore-knowledge-story-task-brief.md`
- **SEMANTIC_BLOCKS:** initial Step-4 problem framing, accepted inputs, repository conflicts, investigation questions, human decision rights and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as final architecture; full-cycle rerun explicitly supersedes this framing where needed.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-065 — `2026-08-20-step-4-truth-knowledge-disclosure-decision-brief.md`
- **SEMANTIC_BLOCKS:** Alternative A/B/C comparison and human decision request for `world.lore_fact` / `world.knowledge` / separate player disclosure / Secret retirement -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; accepted Alternative C is revalidated by S-068 and consolidated normatively by S-071.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after canonical routing.

## 2026-08-20 — Step-4 full-cycle rerun

### S-066 — `2026-08-20-step-4-rerun-task-brief.md`
- **SEMANTIC_BLOCKS:** six-role-informed reframing, fixed owner decisions, Context Assembler/typed-handoff/Story/promotion scope, required challenge and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; task framing only, explicitly input to descendants.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-067 — `2026-08-20-step-4-rerun-research-draft.md`
- **SEMANTIC_BLOCKS:** revalidation of Alternative C, role-specific source eligibility, Context Assembler recommendation, Story availability/promotion analysis, failure scenarios and assumptions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; research/architecture draft and direct basis for decision/candidate/canonicalization.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-068 — `2026-08-20-step-4-rerun-decision-resolution.md`
- **SEMANTIC_BLOCKS:** records owner decisions as revalidated, no new human gate, D4.1–D4.10 settled inputs for candidate -> `DESIGN_PROVENANCE` / accepted-decision provenance.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner; S-071 consolidates the revalidated decisions and subsequent adversarial amendments.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-069 — `2026-08-20-step-4-rerun-candidate-spec.md`
- **SEMANTIC_BLOCKS:** pre-adversarial candidate architecture for truth/knowledge/disclosure, role contexts, Story and promotion -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status requires adversarial review and S-070 identifies material mechanical corrections before canonicalization.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after S-071 remains current.

### S-070 — `2026-08-20-step-4-rerun-adversarial-review.md`
- **SEMANTIC_BLOCKS:** A–J mechanically required corrections, L1–L4 later-owner assignments, rejected concerns and residual-model-risk analysis -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; amendment package is accepted by S-072 and incorporated into S-071.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

### S-071 — `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`
- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL ARCHITECTURE — IMPLEMENTATION PLANNING REQUIRED`.
- **CURRENT AUTHORITY:** YES. It explicitly consolidates the full rerun chain, accepted Alternative C, six logical roles, adversarial amendments, Context Assembler, Story, promotion, Secret/Chapter retirement and Step-5/6 handoffs. Earlier Step-4 task/research/decision wording is historical derivation where conflicting.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md`.
- **DUPLICATION_RISK:** LOW; explicit normative owner.
- **PROVENANCE_LINK_REQUIRED:** keep links to moved rerun/design chain valid. Later canonical amendments may narrow/extend this owner without making the derivation chain normative again.

### S-072 — `2026-08-20-step-4-rerun-resolution-gate.md`
- **SEMANTIC_BLOCKS:** resolution of adversarial findings, R4.1–R4.10 amendment accounting, Step-5/6 handoffs, residual generative-risk acceptance -> `DESIGN_PROVENANCE` / closure evidence.
- **CURRENT AUTHORITY:** NO as a separate normative contract; gate says `READY FOR CANONICAL CONSOLIDATION`, and all ten accepted amendments are incorporated into S-071.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW.

## Part-02 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 72
SPECS_REMAINING: 303

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 12 / 92

PART_02_SOURCES: 12
PART_02_DESIGN_DESTINATIONS: 11
PART_02_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_02_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 56
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 11
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

CURRENT_STEP4_OWNER:
  specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason: branch-complete inbound-reference/path-repair evidence is not yet available from GitHub code search for this non-default branch; do not move files on an incomplete reference census.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-20-step-5-0-state-contamination-audit-adversarial-review.md

2026_08_20_REMAINING: 80
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```

The physical organization decision is intentionally separated from semantic disposition. All eleven Part-02 design files are safe in semantic role, but they remain in `specs/` until the migration slice can repair every current-branch inbound path coherently.
