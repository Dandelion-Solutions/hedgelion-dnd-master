# Documentation Corpus Refactor — Semantic Census

Status: **IN PROGRESS — RESEARCH CORPUS REVIEW COMPLETE / SPECS REVIEW NEXT**
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
- pre-refactor `specs/`: inventory captured from the exact baseline tree; exact source count and item-level dispositions remain pending
- `plans/`: outside the required semantic source census unless a later path/reference check identifies a migration dependency

## Research corpus — reviewed entries

### R-001 — `2026-08-22-infrastructure-topology-options.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; no superseding research owner; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO additional pointer while path remains unchanged.
- **EXTRACTION_REQUIRED:** NO.

### R-002 — `2026-08-22-platform-feasibility-comparative-research.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; accepted deployment choices live in later owners; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO additional pointer while path remains unchanged.
- **EXTRACTION_REQUIRED:** NO.

### R-003 — `2026-08-22-platform-feasibility-economic-profile-amendment.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; point-in-time economic evidence; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO.
- **EXTRACTION_REQUIRED:** NO.

### R-004 — `2026-08-22-private-hosted-inference-economics.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; point-in-time economic/feasibility evidence; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO.
- **EXTRACTION_REQUIRED:** NO.

### R-005 — `2026-08-23-role-context-validation-protocol-1-sequential-containment.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; retained empirical feasibility evidence; final behavioral-containment contract is R2.6 canonical; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** R2.6 canonical retains Protocols 1–3 as evidence; exact inbound-path census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO.
- **EXTRACTION_REQUIRED:** NO.

### R-006 — `2026-08-23-role-context-validation-protocol-2-collapsed-multi-role.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `RESEARCH_RESULT`; current authority NO; retained empirical feasibility evidence; final behavioral-containment contract is R2.6 canonical; destination unchanged `research/`; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact.
- **LIVE_CONSUMERS / REFERENCES:** R2.6 canonical retains Protocols 1–3 as evidence; exact inbound-path census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** NO.
- **EXTRACTION_REQUIRED:** NO.

### R-007 — `2026-08-23-role-context-validation-protocol-3-reasoning-budget.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:**
  - research method/results, player-facing limitation, creativity/hallucination interpretation, architecture inference and deferred gameplay-quality validation -> `RESEARCH_RESULT`; current authority NO; destination same research artifact; split NO.
  - `Owner-selected working reasoning baseline` -> `DUPLICATE_OF_CURRENT_OWNER`; current authority NO; final implementation-facing owner is `specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`, which records `High when available` and makes reasoning profile non-campaign semantics; preserve here only as historical evidence; split NO.
- **FINAL_DESTINATION_FILES:** same research artifact; no new spec.
- **LIVE_CONSUMERS / REFERENCES:** R2.6 canonical explicitly retains Protocols 1–3 and downstream reasoning-profile regression.
- **DUPLICATION_RISK:** CONTROLLED; implementation must follow R2.6 canonical, not this embedded historical selection.
- **PROVENANCE_LINK_REQUIRED:** retain current-owner pointer in census; no artifact edit needed solely for that pointer.
- **EXTRACTION_REQUIRED:** NO.

### R-008 — `2026-08-24-r2-1-continuity-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** Source Manifest, evidence ledger, alternatives/emerging synthesis, open Decision-Brief questions and completion gate -> `DESIGN_PROVENANCE`; current authority NO; current accepted semantics are owned by the later R2.1 owner decision/canonical spec; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** `design/2026-08-24-r2-1-continuity-evidence-ledger.md`.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW after move; document explicitly records pre-decision reasoning.
- **PROVENANCE_LINK_REQUIRED:** preserve links to R2.1 final owners when repairing live paths.
- **EXTRACTION_REQUIRED:** NO.

### R-009 — `2026-08-24-r2-2-actor-continuity-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** source/evidence reconciliation, candidate ownership model, alternatives and unresolved Decision-Brief choice -> `DESIGN_PROVENANCE`; current authority NO; superseded as decision source by R2.2 owner decision/canonical spec; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-010 — `2026-08-24-r2-3-context-runtime-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** full source ledger, constraints, option synthesis, open ownership/physical questions and Decision-Brief preparation -> `DESIGN_PROVENANCE`; current authority NO; R2.3 owner decision/canonical spec controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-011 — `2026-08-24-r2-4-chronicler-service-evidence-addendum.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** evidence delta, source reconciliation and pre-decision Chronicler-service clarification -> `DESIGN_PROVENANCE`; current authority NO; R2.4 owner clarification/canonical spec controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve R2.4 owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-012 — `2026-08-24-r2-4-single-context-llm-execution-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** Source Manifest, evidence, alternatives/challenge and Decision-Brief synthesis -> `DESIGN_PROVENANCE`; current authority NO; final R2.4 owner/canonical spec controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-013 — `2026-08-24-r2-5-agency-dramaturg-coordination-evidence-addendum.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** agency/Dramaturg evidence reconciliation and pre-decision delta -> `DESIGN_PROVENANCE`; current authority NO; R2.5 owner decision/canonical spec controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve R2.5 final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-014 — `2026-08-24-r2-5-collaboration-multiplayer-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** full collaboration/multiplayer source ledger, alternative analysis and Decision-Brief preparation -> `DESIGN_PROVENANCE`; current authority NO; final R2.5 owner/canonical spec controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-015 — `2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:**
  - Source Manifest, assurance disposition, probe matrix, pre-decision synthesis/completion framing -> `DESIGN_PROVENANCE`; current authority NO; final R2.6 owner clarification/canonical spec controls; destination original document under `design/`; split YES.
  - `Current first-party ChatGPT evidence` H1–H8 -> `RESEARCH_RESULT`; current authority NO; preserves point-in-time host capability/limitation findings on Projects, ambient Project memory, reasoning-profile availability/fallback, absence of exact remaining-context telemetry, Apps approval behavior, Retry/branch limits, absence of a documented byte-exact final-message interception contract, and fixed Connector capability evidence; destination extracted standalone research artifact; split YES.
- **FINAL_DESTINATION_FILES:** `design/2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`; new `research/2026-08-24-chatgpt-plus-host-evidence.md`.
- **LIVE_CONSUMERS / REFERENCES:** R2.6 canonical/assurance chain consumes the evidence semantically; exact path census pending.
- **DUPLICATION_RISK:** MEDIUM until split: host facts and design disposition are interleaved; after split, final law remains only in R2.6 canonical.
- **PROVENANCE_LINK_REQUIRED:** YES — extraction must identify `SPLIT_FROM`, semantic source range and `CURRENT_AUTHORITY: NONE — EVIDENCE ONLY`.
- **EXTRACTION_REQUIRED:** YES — exactly H1–H8, preserving qualifications/negative findings; do not copy final R2.6 law into research as a second owner.

### R-016 — `2026-08-24-r2-6-current-host-assurance-synthesis.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** pre-probe/current-host synthesis, gaps and architecture-facing conclusions -> `DESIGN_PROVENANCE`; current authority NO; final R2.6 canonical controls; destination `design/`; split NO because independent host findings are preserved by R-015 extraction.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW after R-015 extraction.
- **PROVENANCE_LINK_REQUIRED:** retain links to extracted evidence/final owner as appropriate.
- **EXTRACTION_REQUIRED:** NO.

### R-017 — `2026-08-24-r2-6-production-like-assurance-protocol.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** experiment/evaluation protocol, matrix, procedure and acceptance design without executed result -> `DESIGN_PROVENANCE`; current authority NO; final R2.6 implementation-acceptance obligations control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve R2.6 final-owner route.
- **EXTRACTION_REQUIRED:** NO — protocol is method/design, not a standalone executed research result.

### R-018 — `2026-08-24-r2-6-protocol-4-frozen-fixture-contract.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** frozen fixture/evaluation contract and conformance method -> `DESIGN_PROVENANCE`; current authority NO; final R2.6 acceptance obligations control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** PENDING INBOUND-REFERENCE CENSUS.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve R2.6 route.
- **EXTRACTION_REQUIRED:** NO.

### R-019 — `2026-08-24-r2-7-WP-01-product-deployment-repository-boundary-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** Source Manifest delta, architecture↔machine audit, findings/dispositions, forward obligations and verification/closure record -> `DESIGN_PROVENANCE`; current authority NO; exact linked owners remain authority; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 status/forward-obligation chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES as normal audit provenance; no new metadata subsystem.
- **EXTRACTION_REQUIRED:** NO.

### R-020 — `2026-08-24-r2-7-WP-02-global-authority-duplicate-owner-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** WP-02 bidirectional audit, duplicate-owner findings and closure evidence -> `DESIGN_PROVENANCE`; current authority NO; linked canonical owners control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 audit chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES as audit provenance.
- **EXTRACTION_REQUIRED:** NO.

### R-021 — `2026-08-24-r2-7-WP-03-catalog-class-capability-completeness-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** machine/catalog census, TDD correction evidence, reverse audit and forward obligations -> `DESIGN_PROVENANCE`; current authority NO; `CATALOG_*`, schemas/catalogs/tests remain controlling; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 audit chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES as audit provenance.
- **EXTRACTION_REQUIRED:** NO.

### R-022 — `2026-08-24-r2-7-WP-04-actor-asset-mechanical-state-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** Actor/Asset/mechanical-state bidirectional audit, machine deltas and forward obligations -> `DESIGN_PROVENANCE`; current authority NO; Actor/Asset owners, R2.2 and WP-04 owner clarification control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 audit chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES as audit provenance.
- **EXTRACTION_REQUIRED:** NO.

### R-023 — `2026-08-24-r2-7-WP-05-deterministic-execution-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** deterministic execution architecture→machine and machine→architecture audit, typed-value routing, corrections and forward obligations -> `DESIGN_PROVENANCE`; current authority NO; Step-3/S6D/current architecture owners control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 audit chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES as audit provenance.
- **EXTRACTION_REQUIRED:** NO.

### R-024 — `2026-08-24-r2-7-WP-06-rules-adjudication-domain-compatibility-mini-report.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** complete WP-06 source manifest delta, incoming-obligation reconciliation, bidirectional audit, exact domain dispositions, F02/F03 forward obligations and final verification record -> `DESIGN_PROVENANCE`; current authority NO; linked Step-3/S6D/domain owners control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path, content preserved without rewriting findings.
- **LIVE_CONSUMERS / REFERENCES:** durable R2.7 cursor and later WP-26 obligation accounting; exact inbound census pending.
- **DUPLICATION_RISK:** LOW if explicitly treated as audit provenance.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve `WP-06/F02` and `WP-06/F03` exactly.
- **EXTRACTION_REQUIRED:** NO.

### R-025 — `2026-08-24-r2-7-audit-status.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire document -> `DESIGN_PROVENANCE`; it is the **current operational durable cursor**, but not a semantic architecture owner; destination `design/`; split NO.
- **CURRENT_AUTHORITY?:** YES for R2.7 operational cursor/status only; NO for architecture semantics.
- **SUPERSEDED_BY:** none while R2.7 remains active; path move must be atomic with all live routing references.
- **FINAL_DESTINATION_FILES:** `design/2026-08-24-r2-7-audit-status.md`.
- **LIVE_CONSUMERS / REFERENCES:** bootstrap/process/roadmap/task execution chain; exact inbound census REQUIRED before move.
- **DUPLICATION_RISK:** HIGH if copied; perform true move, never retain two current cursors.
- **PROVENANCE_LINK_REQUIRED:** YES through active routing documents.
- **EXTRACTION_REQUIRED:** NO.

### R-026 — `2026-08-24-r2-7-global-semantic-owner-matrix.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** owner taxonomy/matrix, false-authority matrix, physical-movement law, acceptance-boundary mapping and later-machine obligations -> `DESIGN_PROVENANCE`; file explicitly declares derivative evidence; destination `design/`; split NO.
- **CURRENT_AUTHORITY?:** NO; exact linked semantic owners control.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** later R2.7 domains; exact inbound census pending.
- **DUPLICATION_RISK:** LOW if derivative status preserved.
- **PROVENANCE_LINK_REQUIRED:** YES as audit mapping provenance.
- **EXTRACTION_REQUIRED:** NO.

### R-027 — `2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** whole-project audit question inventory, coverage method, required artifact set and critique of prior narrow brief -> `DESIGN_PROVENANCE`; current authority NO; owner-approved R2.7 Task Brief v2/execution protocol control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 Task Brief/protocol/source manifest; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve relation to Task Brief v2.
- **EXTRACTION_REQUIRED:** NO.

### R-028 — `2026-08-24-r2-7-whole-project-source-manifest.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** entire file -> `DESIGN_PROVENANCE`; explicitly a source-selection/coverage ledger and not semantic owner; destination `design/`; split NO.
- **CURRENT_AUTHORITY?:** YES only as current R2.7 evidence-coverage working ledger; NO for architecture semantics.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** R2.7 domain audit loop; exact inbound census pending.
- **DUPLICATION_RISK:** MEDIUM if copied rather than moved.
- **PROVENANCE_LINK_REQUIRED:** YES through active R2.7 workflow.
- **EXTRACTION_REQUIRED:** NO.

### R-029 — `2026-08-24-round-2-evidence-disposition-ledger.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** all 82 DIAMOND/STRONG item dispositions, qualifiers, dormant/revisit triggers, roadmap derivation consequences and completeness proof -> `DESIGN_PROVENANCE`; explicitly non-normative evidence accounting; destination `design/`; split NO.
- **CURRENT_AUTHORITY?:** NO; accepted R2.1–R2.6 owners and owner-approved roadmap decisions control.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path, preserved intact.
- **LIVE_CONSUMERS / REFERENCES:** Round-2 provenance and possible future reopening; exact inbound census pending.
- **DUPLICATION_RISK:** LOW if non-normative status remains explicit.
- **PROVENANCE_LINK_REQUIRED:** YES; item-level `revisit when` semantics must survive.
- **EXTRACTION_REQUIRED:** NO.

### R-030 — `2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** reopened Source Manifest delta, machine-contract materialization evidence, A–E responsibility alternatives, unresolved policy-adoption human gate and Step-2 result -> `DESIGN_PROVENANCE`; current authority NO; later House-Rules owner decision/canonical chain controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** House-Rules design chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve rejected alternatives and rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-031 — `2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** Source Manifest, evidence synthesis, alternatives, 20 candidate requirements, evidence gaps and Step-2 completion gate -> `DESIGN_PROVENANCE`; current authority NO; later House-Rules owner/canonical chain controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** House-Rules design chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve rationale/rejected DSL/second-engine alternatives.
- **EXTRACTION_REQUIRED:** NO.

### R-032 — `2026-08-25-s6d-01-ruleset-package-catalog-snapshot-identity-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** identity evidence ledger, alternatives A–D, recommended exact package/set identity architecture, downstream obligations and no-human-decision assessment -> `DESIGN_PROVENANCE`; document explicitly not canonical; final S6D-01 canonicalization and durable package/catalog owners control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain and later package identity audit; exact inbound census pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** preserve final-owner route.
- **EXTRACTION_REQUIRED:** NO.

### R-033 — `2026-08-25-s6d-02-catalog-admission-gap-closure-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** 571-ID evidence/mismatch/admission synthesis, alternatives, recommendation and post-critic corrections -> `DESIGN_PROVENANCE`; current authority NO; current `CATALOG_ADMISSION`, ledger/catalog/schema owners and S6D canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve exact evidence/activation distinction.
- **EXTRACTION_REQUIRED:** NO.

### R-034 — `2026-08-25-s6d-03-complete-calculation-selector-metadata-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** exact selector/operation evidence ledgers, closed pair semantics, dependency corrections, dormant gates, alternatives and no-human-decision result -> `DESIGN_PROVENANCE`; current authority NO; `CALCULATION_SELECTOR_METADATA` and machine contracts/canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve dormant-trigger evidence.
- **EXTRACTION_REQUIRED:** NO.

### R-035 — `2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** 10/2/4 item census, accessor/fact/derived graph synthesis, missing/failure matrix, graph/cache/recovery alternatives and completeness gate -> `DESIGN_PROVENANCE`; current authority NO; `MECHANICAL_CONTEXT` and current machine contracts/canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve dormant items/negative cases.
- **EXTRACTION_REQUIRED:** NO.

### R-036 — `2026-08-25-s6d-05-activity-parameters-targeting-costs-portable-values-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** 19 embedded-value census, owner reconciliation, item-family decisions, machine products, alternatives and no-human-gate result -> `DESIGN_PROVENANCE`; current authority NO; `PORTABLE_ACTIVITY_VALUES` and current schemas/canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve no-owner/no-generic-payload rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-037 — `2026-08-26-s6d-06-registered-activity-primitive-contracts-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** primitive census/evidence synthesis, draft exact-row architecture and rejected generic/family/blanket-activation alternatives -> `DESIGN_PROVENANCE`; current authority NO; `ACTIVITY_PRIMITIVE_CONTRACTS` and current machine/canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve quarantine/activation rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-038 — `2026-08-26-s6d-07-character-progression-ready-pc-seed-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** package/content absence findings, schema/readiness/projection/dependency evidence, architecture consequences and residual product-scope decision -> `DESIGN_PROVENANCE`; current authority NO; later S6D-07 owner decision/canonical architecture and machine seed control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve original product-scope decision context.
- **EXTRACTION_REQUIRED:** NO.

### R-039 — `2026-08-26-s6d-08-hp-lifestate-resource-effect-condition-duration-recovery-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** residual/inherited obligation ledgers, bounded seed recommendation, owner/temporal/recovery matrices, machine gaps and alternatives -> `DESIGN_PROVENANCE`; current authority NO; `HEALTH_EFFECTS_RECOVERY` plus current machine/canonical chain controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve HP nonduplication and negative-space rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-040 — `2026-08-27-s6d-09-domain-rules-coverage-matrix-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** package/product mismatch census, finite support ledger, atomic routes, alternatives A/B/C, analytical challenge and material product-scope decision -> `DESIGN_PROVENANCE`; current authority NO; later S6D-09 owner decision/canonical architecture/derived binding controls; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW if later Decision C remains current owner.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve rejected broad/minimal alternatives and product-scope rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-041 — `2026-08-27-s6d-10-campaign-rulings-house-rule-boundary-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** current boundary census, 13-item evidence ledger, gaps G1–G5, alternatives and analytical challenge -> `DESIGN_PROVENANCE`; current authority NO; `HOUSE_RULES_MECHANICAL_BOUNDARY`, House-Rules owner and current schemas/canonical chain control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve exact-consumer/fail-closed rationale.
- **EXTRACTION_REQUIRED:** NO.

### R-042 — `2026-08-28-s6d-11-tests-machine-contract-closure-research-architecture-draft.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** transitional identity consumer census, compatibility evidence analysis, package/lock/comparator candidate architecture, alternatives and decision-rights result -> `DESIGN_PROVENANCE`; current authority NO; `RULESET_PACKAGE_MACHINE_CLOSURE`, S6D-01/11 owners and current machine contracts control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW.
- **PROVENANCE_LINK_REQUIRED:** preserve why old aggregate identity was rejected.
- **EXTRACTION_REQUIRED:** NO.

### R-043 — `2026-08-28-s6d-12-adversarial-final-closure-evidence.md`

- **FULL_CONTENT_REVIEWED:** YES
- **SEMANTIC_BLOCKS:** current machine observations, integrated obligation table O-01..O-25, attack matrix, blocker classification and Step-2 disposition -> `DESIGN_PROVENANCE`; current authority NO; later S6D-12 canonicalization/integrated machine closure and durable architecture owners control; destination `design/`; split NO.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S6D final-closure provenance; exact inbound census pending.
- **DUPLICATION_RISK:** LOW if retained as assurance history.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve known-realization-blocker/stale/future-not-due distinctions.
- **EXTRACTION_REQUIRED:** NO.

### R-044 — `HDM_External_Architecture_Idea_Dossier_2026-08-21.md`

- **FULL_CONTENT_REVIEWED:** YES — continuous full-file review completed in bounded line ranges through EOF.
- **SEMANTIC_BLOCKS:** executive synthesis; all 24 DIAMOND candidates; all 58 STRONG candidates; all 48 RESERVE/NEGATIVE INTELLIGENCE items; cross-cutting design questions; possible Round-2 grouping; decision-hygiene checklist -> `RESEARCH_RESULT`; current authority NO; document explicitly says RESEARCH INPUT / NON-NORMATIVE / NOT CANONICAL; destination unchanged `research/`; split NO.
- **SUPERSEDED_BY:** none as retained research intelligence. Individual candidate dispositions and accepted results are separately represented by the Round-2 disposition ledger and R2.1–R2.6 owners; that does not erase the dossier's research value, counterarguments, risks or revisit triggers.
- **FINAL_DESTINATION_FILES:** unchanged `research/HDM_External_Architecture_Idea_Dossier_2026-08-21.md`.
- **LIVE_CONSUMERS / REFERENCES:** Round-2 evidence disposition/provenance chain; exact inbound census pending.
- **DUPLICATION_RISK:** LOW because it explicitly disclaims decision authority.
- **PROVENANCE_LINK_REQUIRED:** NO new public provenance metadata. Private source-provenance material remains outside the public repository and must not be copied into this dossier during refactor.
- **EXTRACTION_REQUIRED:** NO.

## Research-corpus classification summary

```text
RESEARCH_BASELINE_COUNT: 44
RESEARCH_FULL_CONTENT_REVIEWED: 44
RESEARCH_REMAINING: 0

WHOLE_SOURCE_RESEARCH_RESULT: 8
WHOLE_SOURCE_DESIGN_PROVENANCE: 35
MIXED_SPLIT_SOURCE: 1
SOURCE_TOTAL_CHECK: 8 + 35 + 1 = 44

CONFIRMED_SPLIT_SOURCES:
  - 2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md

CONFIRMED_RESEARCH_EXTRACTIONS:
  - research/2026-08-24-chatgpt-plus-host-evidence.md

CONFIRMED_PROMOTIONS_REQUIRED_FROM_RESEARCH: 0
CONFIRMED_STRANDED_FINAL_LAW_IN_RESEARCH: 0
```

The source-level summary counts R-015 as `MIXED_SPLIT_SOURCE`, not again inside either whole-source bucket. After migration, the research corpus will contain the eight unchanged research sources plus the one extracted host-evidence artifact, subject to any additional research extractions discovered while reviewing the old `specs/` corpus.

## Current census cursor

```text
RESEARCH_BASELINE_COUNT: 44
RESEARCH_FULL_CONTENT_REVIEWED: 44
RESEARCH_REMAINING: 0
SPECS_BASELINE_COUNT: PENDING EXACT COUNT
SPECS_FULL_CONTENT_REVIEWED: 0
MIXED_SOURCE_CASES_FOUND: 2
  - R-007 contains an embedded historical owner choice already superseded by final R2.6 authority; no split required
  - R-015 requires semantic split
SPLITS_REQUIRED_CONFIRMED: 1
PROMOTIONS_REQUIRED_CONFIRMED: 0
RESEARCH_EXTRACTIONS_CONFIRMED: 1
CURRENT_FILE: first pre-refactor specs artifact after exact specs inventory/count
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
