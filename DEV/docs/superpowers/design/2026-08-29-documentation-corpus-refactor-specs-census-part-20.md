# Documentation Corpus Refactor — Specs Census Part 20

Status: **DURABLE CENSUS CHECKPOINT — 221 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-19.md`

This checkpoint records full-content semantic review of the complete 18-file frozen-baseline Campaign House Rules / Rulings `specs/` family spanning 2026-08-24 and 2026-08-25. The House-Rules Step-2 research/evidence artifacts live under `research/` and belong to the already-complete 44-file research census; they are authority evidence here and are **not recounted** as specs sources.

The current semantic owner was revalidated against:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` — primary canonical House-Rules owner, including later S6D-10 integration;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` — derivative sequencing/status authority;
- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` — derivative/non-normative navigation index.

Common defaults unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` for derivation-chain artifacts referenced by the primary owner or repaired closure chain.

## Authority result before item dispositions

The repaired House-Rules architecture has one primary semantic owner outside this directory:

`DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

It carries the accepted House-Rules laws, including the Step-3 human authority decision, the repaired Step-4..7 refinements, mandatory normative-prose/sidecar admission linkage, explicit `realization_refs`, currentness/notification law, frozen richer adjudication inputs and later S6D-10 exact mechanical integration.

The current roadmap still routes both the 2026-08-24 sequencing decision and Step-8 canonicalization-v2 as primary/current program material. Full semantic review shows that neither is required as a separate implementation-facing normative owner after closure:

- the sequencing decision records a completed inserted-work ordering now superseded for current sequencing by the roadmap itself;
- Step-8 v2 is a canonicalization/closure record that explicitly names `CAMPAIGN_HOUSE_RULES.md` as the primary canonical owner and adds no independent House-Rules law beyond the owner + Step-3 human decision.

Their eventual move therefore requires ordinary live-routing repair, not semantic promotion or a new architecture decision.

The one House-Rules `specs/` artifact retained as a final accepted owner decision is the explicit Step-3 human decision record. It remains directly useful as the durable human-choice boundary behind the primary architecture owner and is explicitly routed by the current roadmap.

## 2026-08-24 House-Rules pre-cycle artifacts

### S-204 — `2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

- **SEMANTIC_BLOCKS:** problem framing, possible policy/ruling shapes, authority risks, possible storage/runtime surfaces, alternatives and pre-design questions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly design input / not canonical.
- **SUPERSEDED_BY:** amended Step-1 Task Brief and repaired Step-2..8 chain; current law resides in `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** Step-1/2 derivation and historical House-Rules reasoning; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because exploratory surface/schema possibilities can be mistaken for accepted architecture.
- **STRANDED ACCEPTED LAW:** none.

### S-205 — `2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

- **SEMANTIC_BLOCKS:** owner-amended product purpose, scope, authority boundaries, information eligibility, current-rules-context legality, live-adjudication-vs-adoption distinction, multiplayer currentness questions, instruction/data fencing, scope fencing, mandatory scenarios and Step-2 research questions -> `DESIGN_PROVENANCE` after canonicalization.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner. It remains canonicalization basis/provenance, but its accepted invariants are consolidated in the current primary owner.
- **SUPERSEDED_BY:** repaired Step-3 owner decision + Step-4..8 v2 chain and ultimately `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` for current law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** current primary owner canonicalization-basis list; repaired cycle provenance; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if kept in compact `specs/`: it contains research obligations, alternatives and process gates mixed with binding framing now consolidated elsewhere.
- **STRANDED ACCEPTED LAW:** none; primary owner explicitly carries the preserved Step-1 semantics.

### S-206 — `2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

- **SEMANTIC_BLOCKS:** owner-approved inserted sequence House Rules -> S6D -> resume R2.7 WP-06 and associated stop/start gates -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at its historical program-decision boundary; current semantic role now `HISTORICAL_ONLY / DESIGN_PROVENANCE` because the ordered work has completed and current sequencing is owned by `NEAR_TERM_ROADMAP.md`.
- **CURRENT AUTHORITY:** NO for current sequencing or implementation semantics. The roadmap still lists this as a primary program decision, which is a live routing reference to repair during migration, not evidence that the completed sequence must remain in the compact implementation-facing specs corpus.
- **SUPERSEDED_BY:** `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` for current live sequencing/status; the decision itself remains provenance of why House Rules/S6D were inserted.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** current roadmap and historical House-Rules/S6D routing; exact inbound set pending.
- **DUPLICATION_RISK:** MEDIUM/HIGH if retained in `specs/`: a completed program cursor can be mistaken for current execution order.
- **PROVENANCE LINK REQUIRED:** YES, but current roadmap should not continue treating it as implementation-facing authority after relocation.
- **STRANDED ACCEPTED LAW:** none; no gameplay/runtime semantic law originates only here.

## 2026-08-25 House-Rules repaired cycle

### S-207 — `2026-08-25-campaign-house-rules-senior-audit-reopen-hold.md`

- **SEMANTIC_BLOCKS:** temporary HOLD/gate state, Step-2/3 reopen routing, demotion of the first attempted Step-4..8 closure, preserved directions during reopen -> `DESIGN_PROVENANCE / HISTORICAL_ONLY`.
- **CURRENT AUTHORITY:** NO; the repaired Step-3 owner decision and v2 Step-4..8 cycle subsequently closed the hold.
- **SUPERSEDED_BY:** Step-3 owner decision + Step-8 canonicalization-v2 + current roadmap status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH in `specs/` because its literal HOLD/S6D-blocked cursor is no longer current.
- **STRANDED ACCEPTED LAW:** none; preserved directions were carried into the repaired primary owner.

### S-208 — `2026-08-25-campaign-house-rules-step-1-task-brief-critic.md`

- **SEMANTIC_BLOCKS:** adversarial framing critique covering shadow-rules-engine risk, information leakage, stale executable legality, live-vs-adoption authority, multiplayer currentness, Markdown privilege escalation and scope creep -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; critic process artifact.
- **SUPERSEDED_BY:** repaired cycle/current primary owner for accepted law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; high discovery noise if retained in final-spec corpus.

### S-209 — `2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`

- **SEMANTIC_BLOCKS:** governance correction withdrawing the false inference that earlier `GO FOR STEP 2–8` approved later material choices; established inherited facts and derivable richer-input work; H1 responsibility alternatives; H2 adoption-authority alternatives; H3 delegation-scope alternatives; agent recommendations and exact human decision gate -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as a final decision. It is the decision-ready input to S-211.
- **SUPERSEDED_BY:** S-211 for actual human choices and `CAMPAIGN_HOUSE_RULES.md` for current integrated law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained beside S-211 because unchosen alternatives/recommendations could be misread as current law.
- **STRANDED ACCEPTED LAW:** none; accepted branches are explicitly recorded in S-211 and primary owner.

### S-210 — `2026-08-25-campaign-house-rules-step-3-decision-brief.md`

- **SEMANTIC_BLOCKS:** original Alternative-C decision and authority/currentness/policy-envelope proposal -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO. Its statement that prior `GO FOR STEP 2–8` satisfied the owner gate was explicitly withdrawn by S-209.
- **SUPERSEDED_BY:** S-209 governance correction + S-211 human owner decision + current primary owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` because it contains a materially invalid owner-approval inference.
- **STRANDED ACCEPTED LAW:** none; compatible semantic direction is preserved in the repaired chain.

### S-211 — `2026-08-25-campaign-house-rules-step-3-owner-decision.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`.
- **CURRENT AUTHORITY:** YES as the explicit durable human owner decision behind current House-Rules policy-adoption semantics.
- **CURRENT DECISIONS:** A + narrow C responsibility shape; active multiplayer PLAYER default for `INTERPRETIVE_POLICY`; creator-root `MECHANICAL_OVERRIDE_POLICY` with explicit current per-PLAYER creator-issued delegation; creator identity remains inherited Git initialization provenance rather than MANIFEST duplication; policy-change discovery/notification piggybacks on normal campaign refresh/current output without push/outbox/exactly-once cursor; authorized derivable machine consequences.
- **SUPERSEDED_BY:** none as a human decision record. `CAMPAIGN_HOUSE_RULES.md` consolidates and integrates it but explicitly includes it in the current canonicalization basis; current roadmap also routes it as current House-Rules authority.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`.
- **LIVE CONSUMERS / REFERENCES:** `CAMPAIGN_HOUSE_RULES.md`, roadmap, repaired Step-4..8 chain, access-control/player policy authority realization; exact inbound set pending.
- **DUPLICATION_RISK:** LOW: primary owner is the integrated semantic contract while this file preserves the exact human decision boundary.
- **PROVENANCE LINK REQUIRED:** YES to S-209.

### S-212 — `2026-08-25-campaign-house-rules-step-4-collaborative-review-v2.md`

- **SEMANTIC_BLOCKS:** repaired collaborative review of S-211; creator lookup disposition; narrow PLAYER delegation storage; normative Markdown + structured sidecar relation; semantic-effect authority classification; atomic policy revision publication; grant revocation/currentness; notification-no-cursor; consequence-vs-policy durability -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as a separate final owner; all accepted refinements are incorporated into later v2 candidate/gate and primary owner.
- **SUPERSEDED_BY:** S-213/S-215/S-217/S-219 and `CAMPAIGN_HOUSE_RULES.md` for current law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH in `specs/` because it is review/refinement history with implementation-shape observations.
- **STRANDED ACCEPTED LAW:** none.

### S-213 — `2026-08-25-campaign-house-rules-step-4-collaborative-review.md`

- **SEMANTIC_BLOCKS:** first attempted Step-4 review over the invalid original Step-3 gate; CR-1..CR-15 and sharpening requirements -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; v2 explicitly supersedes this attempted closure for the reopened path.
- **SUPERSEDED_BY:** S-212 and repaired downstream chain.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained because it is based on the superseded Step-3 governance state.

### S-214 — `2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`

- **SEMANTIC_BLOCKS:** repaired candidate laws for bounded semantic authority, policy-adoption classes, narrow sidecar, policy publication/currentness, richer typed adjudication inputs, realization gaps, notifications, recovery and current materialized structures -> `SUPERSEDED / DESIGN_PROVENANCE` as a candidate.
- **CURRENT AUTHORITY:** NO; Step-6 v2 found two significant refinements that were not yet complete here: mandatory exact normative-entry/sidecar admission linkage and explicit `realization_refs` semantics.
- **SUPERSEDED_BY:** S-216/S-218 and `CAMPAIGN_HOUSE_RULES.md`.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained in compact `specs/` because its candidate law is close to final but incomplete at two material boundaries.
- **STRANDED ACCEPTED LAW:** none.

### S-215 — `2026-08-25-campaign-house-rules-step-5-candidate-spec.md`

- **SEMANTIC_BLOCKS:** first candidate HR-1..HR-39, failure behavior, test obligations and downstream integration based on the original Step-3/4 path -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; superseded by the reopened v2 path and also lacks later explicit adoption-authority/sidecar/realization refinements.
- **SUPERSEDED_BY:** S-214 and repaired downstream chain/current owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH because it looks normative while being from the invalidated first closure path.

### S-216 — `2026-08-25-campaign-house-rules-step-6-adversarial-review-v2.md`

- **SEMANTIC_BLOCKS:** adversarial attacks over authority-class downgrade, self-grant, stale revocation, prospective authorization, prose/sidecar bypass, realization linkage, interpretive-vs-mechanical distinction, revision identity, notification, stale sessions, sidecar-DSL drift, creator cache and stale typed realization; AR2-5/AR2-6 direct resolutions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO as a final owner; its two significant findings are resolved/materialized by S-218 and consolidated by primary owner.
- **SUPERSEDED_BY:** S-218/S-220 and `CAMPAIGN_HOUSE_RULES.md` for accepted current law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move, but retaining adversarial required-resolution text in `specs/` obscures the final law.
- **STRANDED ACCEPTED LAW:** none; AR2-5/6 appear as Laws HR-12/18/19 and related current contracts in the primary owner.

### S-217 — `2026-08-25-campaign-house-rules-step-6-adversarial-review.md`

- **SEMANTIC_BLOCKS:** first adversarial pass over the superseded first candidate, 0 blocker/0 significant + one Context Runtime navigation minor -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; repaired v2 adversarial review supersedes it and finds two significant issues the first pass missed.
- **SUPERSEDED_BY:** S-216 and repaired downstream chain.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained because its `0 SIGNIFICANT` verdict is no longer the governing adversarial result.

### S-218 — `2026-08-25-campaign-house-rules-step-7-resolution-gate-v2.md`

- **SEMANTIC_BLOCKS:** closure evidence for AR2-5 mandatory sidecar admission, AR2-6 `realization_refs`, delegation lifecycle hardening, creator ownership review, notification/currentness review and focused verification; canonicalization authorization -> `DESIGN_PROVENANCE / closure evidence`.
- **CURRENT AUTHORITY:** NO as separate implementation-facing law; the resolved semantics and machine consequences are consolidated in `CAMPAIGN_HOUSE_RULES.md` and current machine owners/tests.
- **SUPERSEDED_BY:** S-220 for closure state and primary owner for semantic law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if kept as coequal current law; it mixes semantic dispositions with point-in-time test/CI status.
- **STRANDED ACCEPTED LAW:** none.

### S-219 — `2026-08-25-campaign-house-rules-step-7-resolution-gate.md`

- **SEMANTIC_BLOCKS:** first closure gate and old frozen decisions, based on superseded Step-3..6 path; one navigation minor and canonicalization authorization -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; v2 repaired gate supersedes it.
- **SUPERSEDED_BY:** S-218 + repaired closure.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH because its zero-significant result predates the Senior-audit repair/v2 adversarial findings.

### S-220 — `2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`

- **SEMANTIC_BLOCKS:** repaired derivation-chain record, accepted-decision summary, policy representation/adjudication/currentness summary, materialized-contract list, focused verification disposition and program transition -> `DESIGN_PROVENANCE / canonicalization closure evidence`.
- **CURRENT AUTHORITY:** NO as a separate semantic owner. The document explicitly names `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` as the **Primary canonical owner**. Its implementation-relevant semantic summary is fully carried there; point-in-time verification/program transition belongs to process history.
- **SUPERSEDED_BY:** `CAMPAIGN_HOUSE_RULES.md` for current law and current roadmap for current sequencing/status. It supersedes S-221 only for historical closure/gate status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE CONSUMERS / REFERENCES:** current roadmap currently lists it as current House-Rules authority; that route must be repaired in the eventual move batch to point implementation discovery to the primary owner + S-211 human decision record.
- **DUPLICATION_RISK:** HIGH if retained in compact `specs/` because downstream planning would see a second summary owner plus obsolete point-in-time CI/program-state claims.
- **STRANDED ACCEPTED LAW:** none.

### S-221 — `2026-08-25-campaign-house-rules-step-8-canonicalization.md`

- **SEMANTIC_BLOCKS:** first attempted eight-step closure record, owner pointer, runtime-facing alignment, source list, result summary, old S6D-next cursor and stop gate -> `SUPERSEDED / DESIGN_PROVENANCE / HISTORICAL_ONLY`.
- **CURRENT AUTHORITY:** NO; the Senior audit reopened that closure and S-220 explicitly supersedes it for gate/status purposes.
- **SUPERSEDED_BY:** S-207 reopen hold followed by repaired S-209..S-220 chain; current law resides in `CAMPAIGN_HOUSE_RULES.md`.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained because it claims a closure later explicitly reopened and repaired.

## House-Rules family result

```text
HOUSE_RULES_SPECS_BASELINE_SOURCES:            18
HOUSE_RULES_FULL_CONTENT_REVIEWED:             18
HOUSE_RULES_DESIGN_DESTINATIONS:               17
HOUSE_RULES_CURRENT_FINAL_OWNER_DECISIONS:      1
HOUSE_RULES_RESEARCH_DESTINATIONS:               0
HOUSE_RULES_SPLITS_REQUIRED:                     0
HOUSE_RULES_EXTRACTIONS_REQUIRED:                0
HOUSE_RULES_STRANDED_ACCEPTED_LAW:               0
HOUSE_RULES_UNRESOLVED_SUPERSESSION:             0

KEEP_IN_SPECS:
  S-211  2026-08-25-campaign-house-rules-step-3-owner-decision.md

PRIMARY_CANONICAL_SEMANTIC_OWNER_OUTSIDE_SPECS:
  DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md

MOVE_TO_DESIGN:
  S-204..S-210, S-212..S-221

ROUTING_REPAIRS_REQUIRED AT MIGRATION:
  - current roadmap/index/project-map/process references that route completed sequencing or
    Step-8 closure record as implementation-facing House-Rules authority must instead route
    implementation discovery through CAMPAIGN_HOUSE_RULES.md + S-211 where the exact human
    decision record is relevant;
  - primary-owner canonicalization-basis links to Step-1/Step-3-amended/Step-4..7 provenance
    must be updated to their new design/ paths without changing historical semantics.
```

No new DCR conflict/debt item is required. The routing changes are ordinary consequences of the approved documentation taxonomy and will be handled inside the physical move + path-repair batch after DCR-016 is satisfied.

## Part-20 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 221
SPECS_REMAINING: 154

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 6 / 57
  2026-08-25: 15 / 55

PART_20_NEW_SOURCES: 18
PART_20_DESIGN_DESTINATIONS: 17
PART_20_RESEARCH_DESTINATIONS: 0
PART_20_UNCHANGED_FINAL_OWNER_DECISIONS: 1
PART_20_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 183
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 32
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  2026-08-24 R2.1 Continuity / History remaining derivation chain

ALREADY_REVIEWED_R2_1_SOURCE_TO_SKIP_WITHOUT_DOUBLE_COUNTING:
  S-169  specs/2026-08-24-r2-1-continuity-history-canonical-spec.md
```
