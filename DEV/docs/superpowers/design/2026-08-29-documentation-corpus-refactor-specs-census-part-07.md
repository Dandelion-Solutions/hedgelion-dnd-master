# Documentation Corpus Refactor — Specs Census Part 07

Status: **DURABLE CENSUS CHECKPOINT — 118 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-06.md`

This checkpoint records full-content review of the complete 2026-08-20 Step-5.4 Host Lifecycle & Session Handoff family and an early full review of the 2026-08-21 Step-5.14 canonical final integration review because it is the later cross-slice authority relevant to the Step-5.4 supersession check.

## Part-06 cursor correction

Part 06 named a nonexistent next source:

`specs/2026-08-20-step-5-4-host-lifecycle-handoff-pre-research-charter.md`

The authoritative 375-file baseline tree contains no such file. Step 5.4 contains exactly eight files, all under the `host-lifecycle-session-handoff` family, beginning with:

`design/2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`

This is a cursor/inventory correction only. No Part-06 semantic disposition changes.

Common defaults for every entry below unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; GitHub code search has not proved branch-complete inbound references on this non-default branch.
- physical moves remain deferred until the reference/path-repair gate is satisfied.

## 2026-08-20 — Step 5.4 Host Lifecycle & Session Handoff

### S-110 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-task-brief.md`

- **SEMANTIC_BLOCKS:**
  - problem/scope, host-vs-gameplay lifecycle separation, controlled-vs-unexpected loss matrix, inherited Step-5.2/5.3 constraints -> `DESIGN_PROVENANCE`; current authority: NO.
  - host conversation/message/context capacity exhaustion scope, no trustworthy remaining-capacity metric, no numerical threshold assumption -> `DESIGN_PROVENANCE`; current authority: NO; consolidated by S-117.
  - required outputs, alternatives, later-slice boundaries and non-goals -> `DESIGN_PROVENANCE`; current authority: NO.
- **SUPERSEDED_BY:** S-117 for accepted implementation-facing Step-5.4 law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** known derivation consumers S-111..S-117; exact repository-wide inbound set pending.
- **DUPLICATION_RISK:** LOW after move; retaining it in `specs/` would leave process framing beside the final owner.
- **PROVENANCE_LINK_REQUIRED:** YES; S-117 derivation chain must continue to resolve after migration.

### S-111 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-research-draft.md`

- **SEMANTIC_BLOCKS:**
  - research inventory, crash/lifecycle analysis, host/session authority analysis, message-evidence and maintenance analysis -> `DESIGN_PROVENANCE`; current authority: NO.
  - BARRIER-NATIVE recommendation, rejected ticket/session-lease alternatives, no-heartbeat reasoning, unexpected-loss RPO and later-slice obligations -> `DESIGN_PROVENANCE`; current authority: NO; status explicitly research/draft.
- **SUPERSEDED_BY:** S-117 for accepted law; S-112..S-116 preserve intermediate challenge/refinement provenance.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-112..S-117; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move; HIGHER if left in compact final-spec corpus because it contains recommendation-form normative-looking prose.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-112 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-analytical-challenge.md`

- **SEMANTIC_BLOCKS:**
  - challenge of durable handoff token/lease, RELINQUISHED semantics, scoped quiescence, failure handling, acknowledgement, session metadata, accepted-message U1/U2/U3 boundaries, TTL/capacity and live-fencing boundaries -> `DESIGN_PROVENANCE`; current authority: NO.
  - candidate-law synthesis and owner-decision assessment -> `DESIGN_PROVENANCE`; current authority: NO; pre-decision analytical result.
- **SUPERSEDED_BY:** S-113 owner decision and ultimately S-117 canonical specification.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-113..S-117; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-113 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-decision-brief.md`

- **SEMANTIC_BLOCKS:**
  - fixed findings/trade-offs/alternatives and recommendation -> `DESIGN_PROVENANCE`; current authority: NO as standalone final contract.
  - owner-approved `BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF` decision and owner-added capacity-exhaustion refinement -> `FINAL_SPEC_OR_ACCEPTED_DECISION` **at the historical decision boundary**, but fully consolidated into S-117; current authority: NO as a separate owner.
  - canonicalization authorization and implementation/Step-5.5 non-authorization -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-117 as the current implementation-facing carrier of the accepted decision. This is consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-114..S-117; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained as a second current normative owner in `specs/`; move preserves decision provenance while S-117 owns current law.
- **PROVENANCE_LINK_REQUIRED:** YES; S-117 explicitly names it in the derivation chain.
- **EXTRACTION_REQUIRED:** NO; no accepted law is stranded because S-117 carries the approved decision and refinement.

### S-114 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-candidate-spec.md`

- **SEMANTIC_BLOCKS:**
  - owner-approved candidate laws, H0-H8 handoff protocol, native resume-owner matrix, unexpected-loss/stale-host/session/maintenance/capacity semantics and later-slice obligations -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly requires adversarial review, and S-115 requires material refinements before S-117.
- **SUPERSEDED_BY:** S-117.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-115..S-117; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if left in `specs/` because candidate laws resemble final normative law but are pre-refinement.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-115 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-adversarial-review.md`

- **SEMANTIC_BLOCKS:**
  - challenges/refinements: reliable warning != execution budget; external native-source movement requires revalidation; post-freeze semantic-acceptance barrier; invisible volatile-state epistemic limit; advisory capacity non-authority; advisory-risk durability reaction deferred to 5.5; transitive RRC; resolvable message evidence; Step-5.2 interpretability inheritance; warning delivery boundary -> `DESIGN_PROVENANCE`.
  - authority-contamination check, revisit triggers and recommendation -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; findings feed S-116/S-117 and require no owner-direction reopen.
- **SUPERSEDED_BY:** S-117 for current law; S-116 records dispositions.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-116/S-117; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-116 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-resolution-gate.md`

- **SEMANTIC_BLOCKS:**
  - adversarial finding dispositions, eight mandatory canonical refinements, parallel-volatile-host guarantee limit, capacity-signal resolution and later-slice ownership -> `DESIGN_PROVENANCE` / closure evidence.
  - gate result `READY FOR CANONICALIZATION` -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all accepted refinements are incorporated in S-117.
- **SUPERSEDED_BY:** S-117 as current Step-5.4 implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-117; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-117 — `2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL ARCHITECTURE — STEP 5.4 CLOSED`.
- **CURRENT AUTHORITY:** YES as detailed Step-5.4 owner.
- **CURRENT LAW:** `BARRIER-NATIVE / SCOPED RECOVERY-SAFE HANDOFF`; host lifecycle is not gameplay authority; controlled handoff and unexpected loss have different guarantees; native owners carry resume semantics; scoped mutation/semantic-acceptance quiescence; external source movement invalidates/revalidates rather than creating a global lock; actual durability is required before safe acknowledgement; clean handoff requires no heartbeat write; lost volatile state is never invented; relinquishment is host-local, not a campaign-global lease; hydration cannot prove absence of unseen volatile state elsewhere; session metadata is non-authoritative; destructive maintenance obeys the same handoff guarantee; accepted semantic evidence must be recoverable without chain-of-thought/process memory; compatible interpretation context survives handoff; host capacity telemetry is optional; reliable warning does not imply execution budget; heuristics remain advisory; host time does not advance fiction.
- **SUPERSEDED_BY:** none found. S-118 explicitly supplements earlier Step-5 slices and does not replace their detailed owner contracts.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** known semantic consumers include Steps 5.5, 5.6, 5.7, 5.8, 5.11, 5.12 and Step-5.14 integrated review; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW while S-110..S-116 are demoted to provenance; HIGH if decision/candidate/gate are treated as coequal final owners.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve S-110..S-116 derivation references after eventual moves.

## 2026-08-21 — Step 5.14 canonical integration review checked early

### S-118 — `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`

- **SEMANTIC_BLOCKS:**
  - final integrated Step-5 verdict/invariant -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; current authority: YES as Step-5.14 cross-slice integration authority.
  - LAW 5.14-1..5 integration clarifications, required-scenario closure, stronger composite attacks, accepted product limitations, Step-6 feasibility gates, implementation-debt clusters, authority-contamination sweep and reopen triggers -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; current authority: YES within its explicit integration scope.
- **CURRENT AUTHORITY:** YES. It states that it **supplements earlier Step-5 slices only where it states an explicit integration clarification and does not replace their detailed owner contracts**.
- **SUPERSEDED_BY:** none found in the reviewed baseline.
- **STEP-5.4 EFFECT:** no supersession. It reaffirms actual-durable-state unexpected-loss recovery and withholding SAVE/handoff success until the promised RRC is actually durable, while leaving S-117 as detailed Step-5.4 authority.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`.
- **LIVE_CONSUMERS / REFERENCES:** Step-6/integrated implementation planning and later assurance; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW; explicit supplement/integration scope, not a second detailed Step-5.4 owner.
- **PROVENANCE_LINK_REQUIRED:** preserve its owning Step-5 parent references.

## Step-5.4 semantic-family result

```text
STEP5_4_BASELINE_SOURCES:                     8
STEP5_4_FULL_CONTENT_REVIEWED:                8
STEP5_4_DESIGN_DESTINATIONS:                  7
STEP5_4_CURRENT_FINAL_OWNER:                  1
STEP5_4_SPLITS_REQUIRED:                      0
STEP5_4_EXTRACTIONS_REQUIRED:                 0
STEP5_4_STRANDED_ACCEPTED_LAW:                0
STEP5_4_UNRESOLVED_SUPERSESSION:              0

CURRENT_STEP5_4_OWNER:
  specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md

LATER_INTEGRATION_SUPPLEMENT_CHECKED:
  specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md

RELATIONSHIP:
  Step 5.14 supplements cross-slice integration and explicitly does not replace
  the detailed Step-5.4 owner contract.
```

## Part-07 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 118
SPECS_REMAINING: 257

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 56 / 92
  2026-08-21: 2 / 45 (reviewed early for integration/supersession checks)

PART_07_SOURCES: 9
PART_07_DESIGN_DESTINATIONS: 7
PART_07_UNCHANGED_FINAL_SPEC_OR_INTEGRATION_DESTINATIONS: 2
PART_07_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 95
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 18
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

PART_06_CURSOR_CORRECTION:
  nonexistent `step-5-4-host-lifecycle-handoff-pre-research-charter.md` replaced by
  actual `step-5-4-host-lifecycle-session-handoff-task-brief.md` family start.

NEXT_UNREVIEWED_SOURCE:
  design/2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md

2026_08_20_REMAINING: 36
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
