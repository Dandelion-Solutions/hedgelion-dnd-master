# Documentation Corpus Refactor — Specs Census Part 45

Status: **DURABLE CENSUS CHECKPOINT — 328 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-44.md`

This closes the second half of the fully reviewed S6D-07 family. The accepted human scope decision is not stranded: its bounded playable-MVP semantics and implementation-boundary clarification are fully consolidated in current `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`, which also carries the final seven-pass repairs and later S6D-09/S6D-11 amendments. Therefore all eight dated S6D-07 process/decision/closure artifacts are design provenance rather than separate current implementation-facing owners.

Common defaults: `FULL_CONTENT_REVIEWED: YES`; no split/extraction; inbound-reference census pending under DCR-016.

## S-325 — `2026-08-26-s6d-07-character-progression-ready-pc-seed-collaborative-review.md`

- **SEMANTIC_BLOCKS:** Step-4 exact bounded profile; minimal definition/content inventory; onboarding choice policy; item-level primitive necessity challenges; martial/spellcaster walkthroughs; package capability semantics; deferred behavioral acceptance trigger -> `DESIGN_PROVENANCE / COLLABORATIVE REVIEW`.
- **CURRENT AUTHORITY:** NO as separate final owner. The accepted profile, onboarding laws, primitive boundaries and behavioral trigger are consolidated in current `CHARACTER_PROGRESSION_READY_PC_SEED.md` and coordinated primitive/selector owners.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** candidate, seven-pass adversarial repair, Step-7/8 closure and current owners.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-07-character-progression-ready-pc-seed-collaborative-review.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-07 design provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-326 — `2026-08-26-s6d-07-character-progression-ready-pc-seed-decision-brief.md`

- **SEMANTIC_BLOCKS:** human-accepted Step-3 product scope decision A: bounded playable MVP vertical slice instead of full SRD or synthetic-only fixtures; minimal content/dependency surface; progressive/diegetic onboarding; martial + spellcaster path; material/default/delegated choice evidence; unsupported content absent/nonselectable; per-primitive necessity challenge; architecture+machine-contract implementation-boundary clarification and deferred behavioral fast-start proof -> `DESIGN_PROVENANCE / ACCEPTED HUMAN DECISION HISTORY`.
- **CURRENT AUTHORITY:** NO as a separate current owner because the complete accepted decision is consolidated in current `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`: exact bounded profile, non-full-SRD breadth, progressive onboarding/no questionnaire, local provisional play, exact primitive set, implementation boundary and mandatory post-runtime behavioral acceptance are all explicit there.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-4 exact-profile derivation, Step-6 repairs, Step-7/8 closure and current canonical owner.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-07-character-progression-ready-pc-seed-decision-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** accepted-decision provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained as a second law owner after full consolidation.
- **PROVENANCE_LINK_REQUIRED:** YES, including preservation of alternatives and human-decision rationale.
- **STRANDED ACCEPTED LAW:** none.

## S-327 — `2026-08-26-s6d-07-character-progression-ready-pc-seed-resolution-gate.md`

- **SEMANTIC_BLOCKS:** Step-7 ACCEPT after seven adversarial passes; bounded Human/Criminal/Fighter1-2/Sorcerer1 profile; sparse Actor bindings/progressive readiness; eleven primitive replacements; Action Surge entitlement; narrow Innate Sorcery Effect; deterministic advancement; deferred behavioral acceptance; no unresolved product/risk issue -> `DESIGN_PROVENANCE / RESOLUTION EVIDENCE`.
- **CURRENT AUTHORITY:** NO as separate implementation owner. Accepted closure is carried by current architecture/machine owners and later amendments.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** Step-8 and current `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md` plus current primitive/selector/effect/temporal owners.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-07-character-progression-ready-pc-seed-resolution-gate.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D closure provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S-328 — `2026-08-26-s6d-07-character-progression-ready-pc-seed-task-brief.md`

- **SEMANTIC_BLOCKS:** Step-1 character-seed/choice/readiness/advancement problem and scope; definition-family/choice/frontier/advancement/cross-owner evidence matrices; GAME projection-debt requirement; S6D-06 quarantine boundary; alternatives; agent/human boundary; eight-step/full-loop exits -> `DESIGN_PROVENANCE / HISTORICAL TASK BRIEF`.
- **CURRENT AUTHORITY:** NO as implementation-facing law. It frames a completed design loop and explicitly stops before Step 2.
- **SUPERSEDED_BY / CONSOLIDATED_IN:** completed S6D-07 chain and current canonical owner/machine realization.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/design/2026-08-26-s6d-07-character-progression-ready-pc-seed-task-brief.md`.
- **LIVE CONSUMERS / REFERENCES:** S6D-07 design/process provenance; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/`.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **STRANDED ACCEPTED LAW:** none.

## S6D-07 family closure

```text
FROZEN_FAMILY_SOURCES: 8
FULL_CONTENT_REVIEWED: 8 / 8
DESIGN_DESTINATIONS: 8
FINAL_SPECS_CHAIN_OWNERS_RETAINED: 0
PRIMARY_SEMANTIC_OWNER_OUTSIDE_SPECS:
  DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md
COORDINATED_CURRENT_OWNERS:
  DEV/ARCHITECTURE/ACTIVITY_PRIMITIVE_CONTRACTS.md
  DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md
  current Effect/Temporal/package machine owners
SPLITS_REQUIRED: 0
EXTRACTIONS_REQUIRED: 0
UNRESOLVED_SUPERSESSION: 0
```

The accepted human product decision remains fully traceable in `design/`, while ordinary implementation-facing semantics route to the current architecture owner. No current law depends on retaining the dated decision brief or canonicalization in `specs/`.

## Part-45 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 328
SPECS_REMAINING: 47
2026-08-26 FROZEN BASELINE: 26
2026-08-26 FULL_CONTENT_REVIEWED/CLASSIFIED: 16 / 26
PART_45_DESIGN_DESTINATIONS: 4
CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 283
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 39
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5
S6D_07: COMPLETE / 8 OF 8 CLASSIFIED
PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_BASELINE_ID: S-329
NEXT_BASELINE_SOURCE: 2026-08-26-s6d-08-hp-lifestate-resource-effect-condition-duration-recovery-adversarial-review.md
```
