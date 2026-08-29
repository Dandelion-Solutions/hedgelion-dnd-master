# Documentation Corpus Refactor — Specs Census Part 61

Status: **FINAL SUPERSESSION RESOLUTION — 375 / 375 REVIEWED / 0 PENDING**
Date: 2026-08-29
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-60.md`

This checkpoint resolves the five cases deliberately left at `PENDING_FINAL_SUPERSESSION_CHECK`. Each source was re-read against the current `PROJECT_MAP` route, current durable architecture owners, strict machine contracts and later accepted temporal/execution architecture. The result is four `design/` destinations and one retained accepted decision in `specs/`.

## S-010 — `2026-08-18-step-2-mechanical-state-ownership-design.md`

- **FINAL CLASS:** `DESIGN_PROVENANCE / SUPERSEDED PRELIMINARY OWNERSHIP DESIGN`.
- **FINAL DESTINATION:** `DEV/docs/superpowers/design/2026-08-18-step-2-mechanical-state-ownership-design.md`.
- **WHY:** the file is explicitly `IN PROGRESS`, records preliminary owner-approved sub-decisions, keeps Step 2 open and defers holistic review. Its accepted ownership results were subsequently integrated/corrected by S-043/S-015 and are now carried by current owners.
- **CURRENT OWNER PROOF:** `ACTOR_MODEL.md` owns HP/LifeState/Actor Resource state; `HEALTH_EFFECTS_RECOVERY.md` owns current HP/LifeState/Resource/Effect/Condition/recovery authority and execution boundaries; `ENTITY_STRUCTURES.md` owns current Effect/Condition/Resource/Temporal structural contracts; `MECHANICAL_CONTEXT.md` owns selector/accessor/fact/DAG boundaries.
- **STRANDED LAW:** none. No accepted S-010-only implementation-facing invariant remains.

## S-015 — `2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

- **FINAL CLASS:** `DESIGN_PROVENANCE / RETROSPECTIVE ASSURANCE CLOSURE`.
- **FINAL DESTINATION:** `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`.
- **WHY:** this is explicitly a non-numbered retrospective assurance overlay. It records amendments and carry-forward constraints rather than serving as a durable implementation owner.
- **ITEM-LEVEL SURVIVAL PROOF:** catalog class/definition binding is current in `CATALOG_INVENTORY.md`/`ENTITY_STRUCTURES.md`; `runtime.procedure` is current in `CATALOG_INVENTORY.md`; Resource normalization/storage and Effect/Condition ownership are current in `ACTOR_MODEL.md`, `ENTITY_STRUCTURES.md` and `HEALTH_EFFECTS_RECOVERY.md`; invocation-fact, derived-node and pinned MechanicalContext rules are current in `MECHANICAL_CONTEXT.md`; scheduled-trigger semantics remain separately owned by retained S-035 and current machine structures; execution/Continuation/checkpoint obligations were subsequently owned by Step 3/Step 5.
- **STRANDED LAW:** none. The assurance rationale remains useful provenance, but implementation does not need this file as a second owner.

## S-035 — `2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md`

- **FINAL CLASS:** `FINAL_SPEC_OR_ACCEPTED_DECISION / CURRENT ACCEPTED AMENDMENT`.
- **FINAL DESTINATION:** unchanged: `DEV/docs/superpowers/specs/2026-08-19-step-2-assurance-slice-c-temporal-recovery-resolution.md`.
- **WHY RETAINED:** the human-approved Variant A owner-local stateful scheduled-trigger decision remains a live accepted architecture amendment rather than only historical reasoning.
- **CURRENT ROUTING PROOF:** current `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md` explicitly calls S-035 **the authoritative amendment** for finite owner-local `definition.effect.scheduled_triggers`. The current strict `effect-definition-data.schema.json` realizes stable local trigger keys, positive metric delay and Activity linkage; `world-effect-state.schema.json` realizes owner-local `scheduled_trigger_state[key]` as the next-due `TemporalBinding` and forbids armed state on terminal Effects.
- **LATER INTEGRATION:** Step-5.3 canonical temporal continuity preserves `world.effect` as native scheduled-trigger owner and adds accepted materialization/retry/recovery laws; `HEALTH_EFFECTS_RECOVERY.md` preserves owner-local scheduled-trigger state and derived Agenda semantics. These extend/integrate S-035 but do not supersede its accepted owner decision.
- **STRANDED LAW:** none because the file remains discoverable as the accepted amendment.

## S-041 — `2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md`

- **FINAL CLASS:** `DESIGN_PROVENANCE / CONSOLIDATED HUMAN-DECISION PROVENANCE`.
- **FINAL DESTINATION:** `DEV/docs/superpowers/design/2026-08-19-step-2-condition-intrinsic-rule-scope-resolution.md`.
- **WHY:** the human-approved orthogonal `ConditionAggregationPolicy × IntrinsicRuleScope` decision is fully consolidated into current implementation-facing owners and machine contracts; the dated resolution is no longer needed as a second current owner.
- **CURRENT OWNER PROOF:** `ENTITY_STRUCTURES.md` explicitly keeps Condition aggregation and intrinsic-rule evaluation separate, with `aggregation_policy_id` controlling effective named-Condition state/member applications and every `intrinsic_mechanics` item declaring `aggregate_once` or `per_effective_application`; `condition-definition-data.schema.json` structurally separates `aggregation_policy_id` from per-intrinsic `scope_id`; `MECHANICAL_CONTEXT.md` keeps `condition_aggregation` and `condition_intrinsic` as distinct derived nodes in one fail-closed DAG; `HEALTH_EFFECTS_RECOVERY.md` keeps Condition aggregation and intrinsic mechanics with no mutable `world.condition` owner.
- **STRANDED LAW:** none. Preserve S-041 as decision rationale/provenance in `design/`.

## S-043 — `2026-08-19-step-2-final-critical-review.md`

- **FINAL CLASS:** `DESIGN_PROVENANCE / FINAL REVIEW AND CLOSURE EVIDENCE`.
- **FINAL DESTINATION:** `DEV/docs/superpowers/design/2026-08-19-step-2-final-critical-review.md`.
- **WHY:** S-043 is an authoritative Step-2 closure/review record for the corrections it made at that time, but it explicitly states that the aligned current normative architecture documents and machine inventory carry the resulting contracts and that historical review/candidate documents are not alternate contracts.
- **CURRENT OWNER PROOF:** its B1–B5/S1 corrections and preserved invariants are now represented by `ENTITY_STRUCTURES.md`, current Resource/Effect/Condition schemas, `ACTOR_MODEL.md`, `HEALTH_EFFECTS_RECOVERY.md` and `MECHANICAL_CONTEXT.md`. Its deferred Step-3/4/5/6 obligations subsequently received their named owners.
- **STRANDED LAW:** none. Keeping it in `specs/` would preserve an unnecessary duplicate implementation-facing surface; `design/` preserves the complete review evidence and reopen conditions.

## Final frozen specs semantic accounting

```text
FROZEN_SPECS_BASELINE: 375
FULL_CONTENT_REVIEWED: 375 / 375
FINAL_DESIGN_DESTINATIONS: 333
FINAL_SPECS_TO_RESEARCH_DESTINATIONS: 1
FINAL_CURRENT_SPEC_OR_ACCEPTED_OWNER_DESTINATIONS: 41
PENDING_FINAL_SUPERSESSION_CHECK: 0
TOTAL: 375
```

The retained current-owner count increases from 40 to 41 only because S-035 is confirmed current. S-010, S-015, S-041 and S-043 move from pending to `design/`.

## Semantic gate result

```text
FROZEN_SPECS_CENSUS: COMPLETE
SUPERSESSION_GATE: COMPLETE
STRANDED_ACCEPTED_LAW_FOUND_IN_PENDING_SET: NO
SPLITS_REQUIRED_BY_PENDING_SET: 0
PROMOTIONS_REQUIRED_BY_PENDING_SET: 0
PHYSICAL_MOVES: 0
REFERENCE_AUDIT_GATE: NOT SATISFIED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
NEXT_EXACT_TASK: close DCR-002..006 register dispositions, synchronize migration journal, then prove branch-complete inbound-reference/path-repair set before any physical move
```