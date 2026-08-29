# Documentation Corpus Refactor — Specs Census Part 08

Status: **DURABLE CENSUS CHECKPOINT — 127 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-07.md`

This checkpoint records full-content review of the complete 2026-08-20 Step-5.5 SOFT / HARD / SAVE Durability Semantics family. Later Step-5.14 cross-slice integration was already fully reviewed in Part 07 and was checked again only for supersession relationship; it supplements earlier Step-5 slices and does not replace their detailed owner contracts.

Common defaults for every entry below unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; GitHub code search has not proved branch-complete inbound references on this non-default branch.
- physical moves remain deferred until the reference/path-repair gate is satisfied.

## 2026-08-20 — Step 5.5 SOFT / HARD / SAVE Durability Semantics

### S-119 — `2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md`

- **SEMANTIC_BLOCKS:**
  - problem statement, scope, inherited Steps 3/5.1–5.4 constraints, current runtime debt and required scenario matrix -> `DESIGN_PROVENANCE`; current authority: NO.
  - analytical questions over intrinsic SOFT/HARD labels, durability closure, explicit save, publication failure, dirty exposure, no-background execution, capacity heuristics and later-slice ownership -> `DESIGN_PROVENANCE`; current authority: NO.
  - quality/exit criteria and expected outputs -> `DESIGN_PROVENANCE`; current authority: NO.
- **SUPERSEDED_BY:** S-127 for accepted implementation-facing Step-5.5 law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-120..S-127; exact repository-wide inbound set pending.
- **DUPLICATION_RISK:** LOW after move; leaving it in `specs/` would mix work framing with final law.
- **PROVENANCE_LINK_REQUIRED:** YES; S-127 canonicalization basis must continue to resolve.

### S-120 — `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`

- **SEMANTIC_BLOCKS:**
  - evidence inventory and preliminary three-axis durability model (`EPHEMERAL/ESTABLISHED`, `DURABLE/VOLATILE_DIRTY`, `MAY_DEFER/MUST_BE_DURABLE_BEFORE(edge)`) -> `DESIGN_PROVENANCE`; current authority: NO.
  - preliminary obligation-rooted recovery closure, explicit save scope, failure alternatives, unpublished-exposure model, host-capacity disposition, alternatives/counterarguments -> `DESIGN_PROVENANCE`; current authority: NO.
  - downstream realization debt and unresolved challenge questions -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-121 challenge/refinement chain and ultimately S-127.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-121..S-127; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if left in compact final-spec corpus because several preliminary recommendations are later materially refined.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-121 — `2026-08-20-step-5-5-soft-hard-save-durability-analytical-challenge.md`

- **SEMANTIC_BLOCKS:**
  - challenge of static HARD/SOFT, pure dependency-only closure, scope-aware durability/exposure, explicit-save quiescence, save-vs-handoff and Story/transcript separation -> `DESIGN_PROVENANCE`; current authority: NO.
  - significant refinement from pure dependency-only closure to `POLICY_ROOTS + DIRTY_ACCUMULATION_SCOPE + REQUIRED_DEPENDENCY_CLOSURE` -> `DESIGN_PROVENANCE`; accepted form consolidated by S-127.
  - recommendation that a fired local/private exposure ceiling become non-abandonable and that failed explicit save require explicit abandonment -> `SUPERSEDED`; current authority: NO; explicitly overridden by S-122 owner direction.
- **SUPERSEDED_BY:** S-122 for the two owner-directed failure/exposure dispositions; S-127 for final law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-122..S-127; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because two material recommendations are no longer current.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-122 — `2026-08-20-step-5-5-soft-hard-save-durability-owner-clarification-addendum.md`

- **SEMANTIC_BLOCKS:**
  - owner direction that failed explicit save SHALL NOT hard-lock coherent local/private play and SHALL NOT require a ritualized separate continuation confirmation -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary; current authority: NO as a separate owner because fully incorporated by S-123..S-127.
  - owner direction that local/private unpublished-exposure ceiling is a risk-control/RPO/SLO policy rather than a correctness barrier; failed flush degrades protection while coherent HOT play may continue -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary; current authority: NO as separate owner.
  - scope-aware exposure and Step-5.8 ownership boundary -> `DESIGN_PROVENANCE` once consolidated.
- **SUPERSEDED_BY:** S-127 as implementation-facing carrier; this is consolidation, not reversal. S-122 itself supersedes the conflicting runtime-blocking recommendations in S-121.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-123..S-127; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained as a second current normative owner beside S-127.
- **PROVENANCE_LINK_REQUIRED:** YES; S-127 explicitly lists it in canonicalization basis.
- **EXTRACTION_REQUIRED:** NO; all accepted owner direction is present in S-127 (notably Laws 5.5-14 and 5.5-17 plus related failure/exposure sections).

### S-123 — `2026-08-20-step-5-5-soft-hard-save-durability-decision-brief.md`

- **SEMANTIC_BLOCKS:**
  - recommended `EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY`, alternatives, trade-offs and exact approval surface -> `DESIGN_PROVENANCE`; current authority: NO as standalone final contract.
  - fixed owner-resolved friendly failure/exposure semantics carried from S-122 -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at decision boundary, but fully consolidated by S-127; current authority: NO separately.
  - deferred mechanical/5.6–5.12 work and canonicalization authorization -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-127 as current implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-124..S-127; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained as coequal current normative owner.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **EXTRACTION_REQUIRED:** NO; S-127 carries the approved direction and resolved product semantics.

### S-124 — `2026-08-20-step-5-5-soft-hard-save-durability-candidate-spec.md`

- **SEMANTIC_BLOCKS:**
  - owner-approved candidate model and Laws 5.5-1..20, closure construction, explicit-save state machine, handoff relation, exposure semantics, failure matrix, scenario checks and downstream requirements -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
  - pre-adversarial formulations that do not yet distinguish required durable source closure from pending write set or fully specify multi-domain composed save / partial native success -> `SUPERSEDED` by S-125/S-126/S-127 refinements.
- **CURRENT AUTHORITY:** NO; status explicitly candidate/not canonical.
- **SUPERSEDED_BY:** S-127.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-125..S-127; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if left in `specs/` because candidate laws closely resemble but are not identical to final law.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-125 — `2026-08-20-step-5-5-soft-hard-save-durability-adversarial-review.md`

- **SEMANTIC_BLOCKS:**
  - attacks and required refinements: owner-relative establishment; composed multi-domain save; real partial native success; zero-write clean save; anti-overaggregation; safe points for opportunistic flush; failed-save precedence under independent HARD edges; closure-vs-write-set separation; exposure of oldest still-relevant unpublished state; retry/warning cadence -> `DESIGN_PROVENANCE`.
  - final verdict allowing canonicalization after those refinements -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; findings are resolved by S-126 and incorporated by S-127.
- **SUPERSEDED_BY:** S-127 for current law; S-126 records exact dispositions.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-126/S-127; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move, but leaving review text in `specs/` makes final-law discovery noisy.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-126 — `2026-08-20-step-5-5-soft-hard-save-durability-resolution-gate.md`

- **SEMANTIC_BLOCKS:**
  - R1..R10 accepted mechanical refinements covering owner-relative establishment, multi-domain composed durability, partial success adoption/revalidation, clean save, closure/write-set separation, anti-overaggregation, safe-point flush, HARD precedence, oldest relevant exposure and non-spam retry cadence -> `DESIGN_PROVENANCE` / closure evidence.
  - gate result `READY FOR CANONICALIZATION` -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all accepted refinements are incorporated into S-127.
- **SUPERSEDED_BY:** S-127 as current Step-5.5 implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-127; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-127 — `2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — STEP 5.5 ARCHITECTURE CLOSED`.
- **CURRENT AUTHORITY:** YES as detailed Step-5.5 owner.
- **CURRENT LAW:** three independent durability axes; owner-contract-relative establishment; SOFT as established deferrable dirty state; HARD as edge-bound `MUST_BE_DURABLE_BEFORE(edge)` obligation rather than intrinsic fact class; scope-owned durability policy; required durable source closure distinct from pending write set; closure roots from policy + dirty accumulation scope + semantically bounded transitive recovery/reference/interpretation dependencies; ordinary singleplayer may flush accumulated local SOFT without forcing global multiplayer synchronization; explicit save has a strong selected-scope player-visible promise and may compose multiple native durability domains without a global transaction/frontier; scoped save quiescence; actual durability required for `saved`; already-durable clean save may succeed without heartbeat write; failed explicit save does not hard-lock coherent local/private play; partial native publication remains real and requires coherent adoption/revalidation; independent correctness-critical durability edges cannot be bypassed; local/private exposure is risk-control/RPO/SLO, scope-relative and anchored to oldest still-relevant actual unpublished state; no exact wall-clock guarantee without execution opportunity; no heartbeat; opportunistic/advisory flush only at safe established-state points; host-capacity heuristics are not correctness authority; shared/live policies may be stricter in Step 5.8; checkpoint, Story/transcript and durability bookkeeping remain non-authoritative separate concerns.
- **SUPERSEDED_BY:** none found. Step-5.14 cross-slice integration authority explicitly supplements earlier Step-5 slices rather than replacing detailed owner contracts.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** known semantic consumers include Steps 5.6–5.8, 5.10–5.12, Step-5.14 integrated review and later machine-realization work; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW while S-119..S-126 are demoted to provenance; HIGH if S-122/S-123/S-124 are treated as coequal final owners.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve S-119..S-126 canonicalization-basis references after eventual moves.

## Step-5.5 semantic-family result

```text
STEP5_5_BASELINE_SOURCES:                     9
STEP5_5_FULL_CONTENT_REVIEWED:                9
STEP5_5_DESIGN_DESTINATIONS:                  8
STEP5_5_CURRENT_FINAL_OWNER:                  1
STEP5_5_SPLITS_REQUIRED:                      0
STEP5_5_EXTRACTIONS_REQUIRED:                 0
STEP5_5_STRANDED_ACCEPTED_LAW:                0
STEP5_5_UNRESOLVED_SUPERSESSION:              0

CURRENT_STEP5_5_OWNER:
  specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md

OWNER_DIRECTION_CHAIN:
  analytical challenge recommendation
    -> partially superseded by owner clarification addendum
    -> consolidated into decision/candidate
    -> adversarially refined
    -> fully incorporated into canonical owner

LATER_INTEGRATION_RELATIONSHIP:
  Step 5.14 supplements cross-slice integration and explicitly does not replace
  the detailed Step-5.5 owner contract.
```

## Part-08 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 127
SPECS_REMAINING: 248

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 65 / 92
  2026-08-21: 2 / 45 (reviewed early for integration/supersession checks)

PART_08_SOURCES: 9
PART_08_DESIGN_DESTINATIONS: 8
PART_08_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_08_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 103
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 19
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-task-brief.md

2026_08_20_REMAINING: 27
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
