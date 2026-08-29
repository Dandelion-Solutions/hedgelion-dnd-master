# Documentation Corpus Refactor — Semantic Census

Status: **IN PROGRESS — COMPLETENESS ARTIFACT, NON-AUTHORITATIVE**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`

This file is the durable completeness mechanism for the owner-approved Documentation Corpus Refactor. It does not establish architecture law. Current authority remains with the owning architecture/specification sources identified per entry.

## Census contract

Each pre-refactor source under `DEV/docs/superpowers/research/` and `DEV/docs/superpowers/specs/` must receive a final disposition with:

- `FILE`
- `FULL_CONTENT_REVIEWED`
- material `SEMANTIC_BLOCKS` with range/section, class, current authority, supersession/current-owner route, destination and split requirement
- `FINAL_DESTINATION_FILES`
- `LIVE_CONSUMERS / REFERENCES`
- `DUPLICATION_RISK`
- `PROVENANCE_LINK_REQUIRED`
- `EXTRACTION_REQUIRED`

Working semantic classes:

- `RESEARCH_RESULT`
- `DESIGN_PROVENANCE`
- `FINAL_SPEC_OR_ACCEPTED_DECISION`
- `HISTORICAL_ONLY`
- `SUPERSEDED`
- `DUPLICATE_OF_CURRENT_OWNER`

`LIVE_CONSUMERS / REFERENCES` is completed during the repository-wide inbound-reference pass. Until then an entry may explicitly say `PENDING INBOUND-REFERENCE CENSUS`; that state is not eligible for final refactor closure.

## Baseline corpus inventory

- pre-refactor `research/`: **44 files**
- pre-refactor `specs/`: inventory captured from the exact baseline tree; total count and item-level dispositions are pending completion below
- `plans/`: outside the required semantic source census unless a later path/reference check identifies a migration dependency

## Reviewed entries

### R-001

**FILE:** `DEV/docs/superpowers/research/2026-08-22-infrastructure-topology-options.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: none; architecture decisions must be established elsewhere
  - DESTINATION: `research/2026-08-22-infrastructure-topology-options.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS

**DUPLICATION_RISK:** LOW — option/evidence corpus, not a normative owner

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-002

**FILE:** `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-comparative-research.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: none as research evidence; accepted deployment/architecture choices live in later owners
  - DESTINATION: `research/2026-08-22-platform-feasibility-comparative-research.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS

**DUPLICATION_RISK:** LOW

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-003

**FILE:** `DEV/docs/superpowers/research/2026-08-22-platform-feasibility-economic-profile-amendment.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: none as point-in-time economic evidence
  - DESTINATION: `research/2026-08-22-platform-feasibility-economic-profile-amendment.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS

**DUPLICATION_RISK:** LOW

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-004

**FILE:** `DEV/docs/superpowers/research/2026-08-22-private-hosted-inference-economics.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: none as point-in-time economic/feasibility evidence
  - DESTINATION: `research/2026-08-22-private-hosted-inference-economics.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS

**DUPLICATION_RISK:** LOW

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-005

**FILE:** `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: retained as empirical feasibility evidence; final behavioral-containment contract is owned by R2.6 canonical specification
  - DESTINATION: `research/2026-08-23-role-context-validation-protocol-1-sequential-containment.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** R2.6 canonical specification cites retained Protocols 1–3 as evidence; exact inbound-path census still pending

**DUPLICATION_RISK:** LOW — evidence and final law are semantically separated

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-006

**FILE:** `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `entire document`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: retained as empirical feasibility evidence; final behavioral-containment contract is owned by R2.6 canonical specification
  - DESTINATION: `research/2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`
  - SPLIT_REQUIRED?: NO

**FINAL_DESTINATION_FILES:** unchanged research artifact

**LIVE_CONSUMERS / REFERENCES:** R2.6 canonical specification cites retained Protocols 1–3 as evidence; exact inbound-path census still pending

**DUPLICATION_RISK:** LOW

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged

**EXTRACTION_REQUIRED:** NO

### R-007

**FILE:** `DEV/docs/superpowers/research/2026-08-23-role-context-validation-protocol-3-reasoning-budget.md`

**FULL_CONTENT_REVIEWED:** YES

**SEMANTIC_BLOCKS:**

- `Purpose` through `Player-facing quality limitation`, plus `Creativity and hallucination — engineering interpretation`, `Architecture inference`, and `Deferred gameplay-quality validation`
  - CLASS: `RESEARCH_RESULT`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: retained evidence; R2.6 owns the supported host/reasoning-profile contract and downstream regression obligation
  - DESTINATION: same `research/` artifact
  - SPLIT_REQUIRED?: NO
- `Owner-selected working reasoning baseline`
  - CLASS: `DUPLICATE_OF_CURRENT_OWNER`
  - CURRENT_AUTHORITY?: NO
  - SUPERSEDED_BY: `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`, especially Supported MVP host profile and LAW R2.6-8 (`High when available`; reasoning profile is not campaign semantics)
  - DESTINATION: preserved in the research artifact as historical evidence/provenance, not implementation authority
  - SPLIT_REQUIRED?: NO — promotion-before-move check confirms the accepted implementation-facing rule is already present in the final R2.6 canonical spec

**FINAL_DESTINATION_FILES:** unchanged research artifact; no new spec required

**LIVE_CONSUMERS / REFERENCES:** R2.6 canonical spec expressly retains Protocols 1–3 evidence and includes reasoning-profile regression in downstream acceptance; exact inbound-path census still pending

**DUPLICATION_RISK:** CONTROLLED — embedded historical owner choice must not be treated as a second normative owner; current implementation-facing authority is R2.6 canonical spec

**PROVENANCE_LINK_REQUIRED:** NO additional link required if path unchanged; final census should retain the current-owner pointer above

**EXTRACTION_REQUIRED:** NO

## Current census cursor

```text
RESEARCH_BASELINE_COUNT: 44
RESEARCH_FULL_CONTENT_REVIEWED: 7
RESEARCH_REMAINING: 37
SPECS_BASELINE_COUNT: PENDING EXACT COUNT
SPECS_FULL_CONTENT_REVIEWED: 0
MIXED_SOURCE_CASES_FOUND: 1
SPLITS_REQUIRED_CONFIRMED: 0
PROMOTIONS_REQUIRED_CONFIRMED: 0
CURRENT_FILE: next research artifact after Protocol 3
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
