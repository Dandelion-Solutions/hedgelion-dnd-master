# Documentation Corpus Refactor — Specs Census Part 24

Status: **DURABLE CENSUS CHECKPOINT — 250 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-23.md`

This checkpoint records full-content review of the complete nine-file 2026-08-24 R2.4 Single-Context LLM Execution / Chronicler Service specs family.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` for the canonicalization/decision chain.

## Authority / consolidation result

The original Decision Brief treated Chronicler as merely opportunistic/non-hot-path. A subsequent explicit owner clarification strengthened the product contract:

> compatible Story backlog remains an outstanding service obligation and receives bounded Story/Chronicler service at the **first safe execution opportunity**, without fixed wall-clock/turn SLA, scheduler, background worker or commit-every-turn requirement.

Decision Brief v2 explicitly superseded the original brief for decision purposes, incorporated that clarification and recommended **Registered Turn Envelope + Minimal Typed Gateways + first-safe-opportunity Chronicler service**. The owner approved that exact direction.

The canonical R2.4 specification fully consolidates:

- the owner-approved choreography and first-safe-opportunity policy;
- the separate Chronicler owner clarification;
- the existing Step-5.10/5.12 authority boundaries;
- all eight adversarial amendments: no same-envelope Story feedback, envelope-level service checkpoint even on non-mechanical turns, admitted Story source-basis requirement, Story contention/yield before protected Narrator margin, dedicated Chronicler->Narrator assurance handoff, bounded backlog check, turn-local non-scheduler `DEFER(reason)`, and fresh Narrator rebind after Chronicler.

Therefore no accepted implementation-facing R2.4 law is stranded in either Decision Brief, the separate Chronicler clarification, owner decision, candidate, adversarial review or closure gate.

## S-242 — `2026-08-24-r2-4-single-context-llm-execution-task-brief.md`

- **SEMANTIC_BLOCKS:** single-context one-turn orchestration problem, human decision boundary, inherited Step-3/4/5/R2.3 constraints, source manifest, one-turn topology, role activation/rebinding, typed nondeterministic result lifecycle, deterministic gateway, Narrator/emission integration, instruction hierarchy, injection/role confusion, `UNSATISFIABLE` integration, active D16/S21/S28 and exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; task/process framing only. Its weaker Chronicler wording is explicitly refined by S-245/S-244.
- **SUPERSEDED_BY:** S-249 canonical specification for accepted R2.4 law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained beside final law because it mixes research questions with a subsequently strengthened service policy.
- **STRANDED ACCEPTED LAW:** none.

## S-243 — `2026-08-24-r2-4-single-context-llm-execution-decision-brief.md`

- **SEMANTIC_BLOCKS:** alternatives A model-directed collapsed orchestration / B registered TurnEnvelope + minimal typed gateways / C explicit phase FSM; recommended B; proposed role activation, phase frames, typed handoffs, deterministic gateway, instruction hierarchy, output fencing, finite `UNSATISFIABLE` behavior and proposed R2.4 laws -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO. S-244 explicitly supersedes this brief for decision purposes because this version described Chronicler as merely opportunistic/non-hot-path and lacked the first-safe-opportunity anti-starvation obligation.
- **SUPERSEDED_BY:** S-244/S-246 and ultimately S-249.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained because its Chronicler activation semantics are materially weaker than current law.

## S-244 — `2026-08-24-r2-4-single-context-llm-execution-decision-brief-v2.md`

- **SEMANTIC_BLOCKS:** repaired alternatives and recommendation; Registered TurnEnvelope; role frame/minimal handoffs; conditional Interpreter/Dramaturg/Actor activation; mandatory deferred-service Chronicler; first-safe-opportunity/typed defer/bounded catch-up/no-scheduler/gameplay-priority rules; deterministic gateway; instruction hierarchy; output fencing; finite `UNSATISFIABLE`; proposed R2.4 laws -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; owner decision S-246 accepts the direction and S-249 fully consolidates it plus adversarial amendments.
- **SUPERSEDED_BY:** S-246 historical approval and S-249 current implementation-facing law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained as a near-final second law carrier.
- **STRANDED ACCEPTED LAW:** none.

## S-245 — `2026-08-24-r2-4-chronicler-service-owner-clarification.md`

- **SEMANTIC_BLOCKS:** owner-approved strengthening from optional/opportunistic Chronicler to first-safe-opportunity bounded service; Step-5.10 compatibility; safe-opportunity semantics; priority law; bounded service; deterministic-vs-generative Story transform; no commit-per-turn; per-envelope service check -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical clarification boundary, now fully consolidated by S-249.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-249 carries the exact service obligation and later AR safeguards.
- **SUPERSEDED_BY:** S-249 as current carrier; consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if left as coequal owner because it predates the no-same-envelope-feedback/source-basis/Narrator-rebind refinements.
- **STRANDED ACCEPTED LAW:** none.

## S-246 — `2026-08-24-r2-4-single-context-llm-execution-owner-decision.md`

- **SEMANTIC_BLOCKS:** owner approval of Alternative B + first-safe-opportunity Chronicler service; baseline TurnEnvelope responsibility; service priority/defer/no scheduler; rejected A/C; preserved architecture boundaries -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary, fully consolidated by S-249.
- **CURRENT AUTHORITY:** NO as a second implementation-facing owner; S-249 carries the approved direction and later AR-1..AR-8 corrections.
- **SUPERSEDED_BY:** S-249 as compact current carrier.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained as coequal owner because it predates the final containment/source-basis/feedback corrections.
- **STRANDED ACCEPTED LAW:** none.

## S-247 — `2026-08-24-r2-4-single-context-llm-execution-candidate-spec.md`

- **SEMANTIC_BLOCKS:** candidate TurnEnvelope/phase activation/service laws; first-safe-opportunity Chronicler priority; rebinding/minimal typed handoffs; deterministic gateway/result lifecycle; instruction hierarchy/injection boundary; visible output fencing; `UNSATISFIABLE`; D16/S21/S28; downstream obligations -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; eight adversarial amendments remain outstanding.
- **SUPERSEDED_BY:** S-249 after S-248 refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH because candidate law closely resembles final architecture while lacking concrete same-envelope Story/source-basis/containment safeguards.

## S-248 — `2026-08-24-r2-4-single-context-llm-execution-adversarial-review.md`

- **SEMANTIC_BLOCKS:** AR-1..AR-8 attacks over same-envelope Story feedback, service-check placement, Story source-basis durability, Story contention/Narrator margin, Chronicler->Narrator containment assurance, backlog-check boundedness, non-scheduler defer semantics and fresh Narrator rebind; rejected overreactions and canonicalization recommendation -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all eight amendments are incorporated into S-249.
- **SUPERSEDED_BY:** S-249 current law and S-250 closure evidence.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; useful audit/provenance rather than ordinary implementation input.
- **STRANDED ACCEPTED LAW:** none.

## S-249 — `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status canonical R2.4 and gate subsequently closes the stage.
- **CURRENT AUTHORITY:** YES as current single-context TurnEnvelope/role-gateway/instruction/Chronicler-service owner.
- **CURRENT LAW:** one request/assistant turn/physical context with explicit logical phases; TurnEnvelope is transient control not authority; registered conditional phase vocabulary; compatible Story backlog service obligation; compact per-envelope backlog check; first-safe-opportunity bounded service after required current play + protected Narrator/output reservation; defer does not cancel and is turn-local; no scheduler/commit-per-turn; admitted Step-5.10 source basis only; no same-envelope Story feedback; Story contention yields before visible response margin; fresh Narrator rebind after Chronicler; shared physical context never grants eligibility; minimal typed handoffs/no hidden reasoning; deterministic acceptance and accepted-frontier retry/no mechanics replay; present-vs-active CORE hierarchy; lower layers narrow not override; data cannot self-promote to instruction; Narrator-only ordinary visible payload; sanitization defense in depth; finite non-looping `UNSATISFIABLE`; D16/S21/S28 dispositions; R2.5/R2.6/R2.7 obligations including dedicated Chronicler->Narrator containment assurance.
- **SUPERSEDED_BY:** none found.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`.
- **LIVE CONSUMERS / REFERENCES:** R2.5 collaboration/multiplayer, R2.6 host assurance, R2.7 realization, TurnEnvelope/role/result/instruction implementation planning; exact inbound set pending.
- **DUPLICATION_RISK:** LOW once S-242..S-248/S-250 move to provenance.

## S-250 — `2026-08-24-r2-4-single-context-llm-execution-resolution-gate.md`

- **SEMANTIC_BLOCKS:** 14 exit-criteria coverage, AR-1..AR-8 closure mapping, final Chronicler policy, D16/S21/S28 disposition, rejected/conditional machinery, downstream handoff and conditional stage-closure verification instructions -> `DESIGN_PROVENANCE / closure evidence`.
- **CURRENT AUTHORITY:** NO as separate implementation-facing law; S-249 owns semantics and current roadmap owns current sequencing.
- **SUPERSEDED_BY:** S-249 for law; roadmap/current verification for status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM if retained because it combines completeness evidence with historical transition status.
- **STRANDED ACCEPTED LAW:** none.

## R2.4 family result

```text
R2_4_BASELINE_SPECS_SOURCES:                  9
R2_4_DESIGN_DESTINATIONS:                     8
R2_4_CURRENT_FINAL_SPEC:                      1
R2_4_RESEARCH_DESTINATIONS:                   0
R2_4_SPLITS_REQUIRED:                         0
R2_4_EXTRACTIONS_REQUIRED:                    0
R2_4_STRANDED_ACCEPTED_LAW:                   0
R2_4_UNRESOLVED_SUPERSESSION:                 0

KEEP_IN_SPECS:
  S-249  2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md

MOVE_TO_DESIGN:
  S-242..S-248, S-250
```

No new DCR conflict/debt item is required.

## Part-24 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 250
SPECS_REMAINING: 125

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 35 / 57
  2026-08-25: 15 / 55

PART_24_NEW_SOURCES: 9
PART_24_DESIGN_DESTINATIONS: 8
PART_24_RESEARCH_DESTINATIONS: 0
PART_24_FINAL_SPEC_DESTINATIONS: 1
PART_24_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 209
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 35
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  2026-08-24 R2.5 Collaboration / Multiplayer remaining derivation chain

ALREADY_REVIEWED_R2_5_SOURCES_TO_SKIP_WITHOUT_DOUBLE_COUNTING:
  S-149  2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md
  S-150  2026-08-24-r2-5-collaboration-multiplayer-resolution-gate.md
```
