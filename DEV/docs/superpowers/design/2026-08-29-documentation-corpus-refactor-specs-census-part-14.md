# Documentation Corpus Refactor — Specs Census Part 14

Status: **DURABLE CENSUS CHECKPOINT — 169 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-13.md`

This checkpoint records full-content review of the complete 2026-08-21 Step-5.10 Story Projection Durability family plus an early full-content later-authority check of the R2.1 continuity/history canonical specification.

The R2.1 canonical source is counted honestly against the 375-file baseline and the 2026-08-24 date group. It SHALL NOT be counted again when the chronological census reaches R2.1.

Common defaults for every entry below unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; GitHub code search has not proved branch-complete inbound references on this non-default branch.
- physical moves remain deferred until the reference/path-repair gate is satisfied.

## 2026-08-21 — Step 5.10 Story Projection Durability

### S-162 — `2026-08-21-step-5-10-story-projection-durability-task-brief.md`

- **SEMANTIC_BLOCKS:**
  - solution-blind architectural scope, inherited Story/publication/recovery/chronology constraints and conservative single-sequential-chat deployment constraint -> `DESIGN_PROVENANCE`; current authority: NO.
  - required research questions over Story-local progress, typed frontiers, work identity/idempotency, Chronicler boundary, publication atomicity, same-ref concurrency, IDs, availability, lag/catch-up, correction, retention and SAVE/recovery -> `DESIGN_PROVENANCE`.
  - alternatives A–F, adversarial scenario matrix, likely decision rights and non-goals -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-168 for accepted Step-5.10 implementation-facing law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-163..S-168; exact repository-wide inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES; S-168 canonicalization basis must continue to resolve.

### S-163 — `2026-08-21-step-5-10-story-projection-durability-research-draft.md`

- **SEMANTIC_BLOCKS:**
  - repository facts, time-sensitive platform research, external materialized-view/CQRS/idempotence research and quality attributes -> `DESIGN_PROVENANCE` in this artifact: they are evidence inputs to a pre-acceptance architecture derivation and explicitly require later platform reverification; current authority: NO.
  - alternatives A–F and leading queue-free coverage-driven projection recommendation -> `DESIGN_PROVENANCE`.
  - deterministic projection-control vs Chronicler boundary, layer-specific observations, preliminary coverage/catch-up/transaction/allocator/concurrency/SAVE/retention/correction model -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-164 challenge and ultimately S-168.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-164..S-168; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in compact final-spec corpus because several preliminary coverage/contract/compaction assumptions are later tightened.
- **PROVENANCE_LINK_REQUIRED:** YES.
- **EXTRACTION_REQUIRED:** NO; no platform/external research block is required as a standalone durable research owner for current architecture, and time-sensitive platform details are explicitly nonpermanent evidence.

### S-164 — `2026-08-21-step-5-10-story-projection-durability-analytical-challenge.md`

- **SEMANTIC_BLOCKS:**
  - challenge proving need for durable Story-local coverage while rejecting per-source skip ledger for cursor-capable domains -> `DESIGN_PROVENANCE`; current authority: NO.
  - domain-typed coverage, intentional omission, Story-local allocators, publication-time final IDs, nonreuse, layer-local transaction/reference closure, same-ref gameplay-priority behavior, ambiguous ACK idempotency, source-retention handoff, correction/regeneration and plain-chat activation limits -> `DESIGN_PROVENANCE`.
  - minimal baseline promises: eventual/opportunistic freshness, no permalink guarantee, source identity provenance only, no background/Work dependency -> `DESIGN_PROVENANCE` consolidated by S-168.
- **SUPERSEDED_BY:** S-165 candidate and ultimately S-168; S-166/S-167 add contract-generation/source-watermark/cursor-continuity refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-165..S-168; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained beside final owner because semantic projection-contract generation and compaction continuity are not yet final.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-165 — `2026-08-21-step-5-10-story-projection-durability-candidate-spec.md`

- **SEMANTIC_BLOCKS:**
  - candidate direction `LAYER-LOCAL COVERAGE / QUEUE-FREE PULL CATCH-UP / DETERMINISTIC STORY PUBLICATION / OPTIONAL GENERATIVE CHRONICLER / GAMEPLAY-PRIORITY SAME-REF CAS`, Laws 5.10-1..34, machine debt and scenarios -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
  - candidate coverage cursor/source basis semantics and projection-state placement are incomplete before adversarial blocker resolution -> `SUPERSEDED` by S-166/S-167/S-168.
- **CURRENT AUTHORITY:** NO; status explicitly candidate/not canonical.
- **SUPERSEDED_BY:** S-168.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-166..S-168; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if left in `specs/` because candidate laws closely resemble but omit five blocking final refinements.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-166 — `2026-08-21-step-5-10-story-projection-durability-adversarial-review.md`

- **SEMANTIC_BLOCKS:**
  - five blocking gaps: coverage must be typed by semantic projection-contract generation; campaign HEAD is not Story source watermark; mutable Story progress must not leak into MANIFEST/CURRENT/RRC; source cursor continuity must survive lawful compaction; concurrent workers cannot advance incompatible contract generations -> `DESIGN_PROVENANCE`.
  - strengthenings: append-monotonic source enumeration or typed sparse fallback; layer-specific MUST_MATERIALIZE cardinality; Transcript admission handoff to 5.11/5.12; Story-to-Story refs remain presentation, not factual source authority -> `DESIGN_PROVENANCE`.
  - race/ambiguous-ack/compaction/YAGNI/owner-decision analysis and `PASS WITH REQUIRED TECHNICAL AMENDMENTS` -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; findings resolved by S-167 and incorporated by S-168.
- **SUPERSEDED_BY:** S-168 for current law; S-167 records exact dispositions.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-167/S-168; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move; keeping review in `specs/` pollutes compact final-law discovery.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-167 — `2026-08-21-step-5-10-story-projection-durability-resolution-gate.md`

- **SEMANTIC_BLOCKS:**
  - accepted alternative resolution and all adversarial amendments -> `DESIGN_PROVENANCE` / closure evidence.
  - final authority geometry, typed `(layer, source_domain, projection_contract_generation)` coverage invariant, single-chat deployment statement, same-ref gameplay-priority statement, layer independence and retention handoff -> `DESIGN_PROVENANCE`.
  - gate result `READY FOR CANONICALIZATION`; no material owner decision remains -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all accepted refinements are incorporated in S-168.
- **SUPERSEDED_BY:** S-168 as current Step-5.10 implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-168; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-168 — `2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — STEP 5.10 ARCHITECTURE CLOSED`.
- **CURRENT AUTHORITY:** YES as detailed Story projection durability/catch-up/publication owner.
- **CURRENT LAW:** Story remains durable/noncanonical and may lag/fail/restart without affecting gameplay; no Story-to-canon authority flow; correctness works with one ordinary sequential execution stream and no background/Work/Pro/Enterprise dependency; typed source projection domains; projection enumeration order is nonfictional and campaign HEAD is transport pin only; coverage is typed by semantic projection-contract generation; model/prompt changes alone do not rewind coverage; incompatible contract generation is a real dependency conflict; contiguous coverage requires append-monotonic source enumeration or typed sparse fallback; `MUST_MATERIALIZE | MAY_OMIT` terminal disposition with contract-specific mapping/cardinality; Story projection state stays under Story ownership and out of MANIFEST/CURRENT/RRC/canonical allocator; queue-free backlog derives source-domain basis minus compatible layer coverage; deterministic core owns source selection/basis pinning/validation/final IDs/publication/coverage while Chronicler is editorial/generative only; nonreusing layer-local IDs assigned at publication; ordinary Story catch-up is layer-local atomic and cross-layer lag legal; no dangling Story refs; Story-to-Story refs do not promote prose to factual authority; availability remains Story retrieval eligibility rather than disclosure; coverage is ambiguous-ACK idempotency evidence; Story-only same-ref movement is semantically disjoint from ordinary gameplay authority and gameplay never waits for Story freshness/lock; Story yields under contention; draft reuse after canon movement is dependency-aware; future workers reuse same coverage/CAS semantics without queue/lease authority; SAVE/RRC exclude Story freshness; typed projection-before-delete can be required only by later retention policy; cursor interpretation/resume continuity must survive source compaction; source refs preserve identity rather than permanent payload; generated text is not automatically Transcript; Story correction never rewrites canon; full Story loss degrades presentation only; ordinary gameplay requires zero Story work.
- **SUPERSEDED_BY:** none found.
- **LATER AUTHORITY RELATIONSHIP:** R2.1 continuity/history canonical explicitly reuses Step-5.10 `source_refs`, typed source-domain coverage and semantic projection-contract generation, and says Story responsibility changes only at the **consumer edge**. It does not replace Step-5.10 durability/publication ownership.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** Steps 5.11–5.14, R2.1 continuity, R2.3 Context Runtime, R2.4/R2.6 host execution, R2.7 Story machine realization; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW while S-162..S-167 are demoted.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve S-162..S-167 canonicalization-basis references after eventual moves.

## 2026-08-24 — early later-authority check for R2.1

### S-169 — `2026-08-24-r2-1-continuity-history-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL ARCHITECTURE — R2.1`.
- **CURRENT AUTHORITY:** YES for long-campaign continuity source/lifecycle classification and the Story-to-gameplay continuity consumer edge.
- **CURRENT LAW RELEVANT TO THIS CENSUS:** no generic memory authority; current semantic questions resolve through current owners; eligible Story may provide broad/episodic/entity-linked continuity orientation and routing evidence toward stronger sources; derived continuity never widens role/player/subject eligibility; material role decisions escalate to proper owner/source classes; source-bound does not mean current; history alignment uses HDM source refs/source-domain coverage/source-specific correction/currentness/semantic projection-contract generation, not host chat ancestry; only admitted HDM evidence enters durable continuity; stale projection degrades to stronger evidence; derived text cannot self-amplify factual authority; projection absence is not semantic absence; entity continuity starts as a scoped view; exact recall remains selective exact; no per-turn/background memory clock; no whole-history preload permission; projection semantic generation changes require explicit migration/reprojection while model/style changes alone do not; Story/Chronicler authority itself does not expand.
- **RELATION TO S-168:** `SUPPLEMENT / DISTINCT OWNER`, not supersession. R2.1 explicitly states that Story responsibility changes only at the **consumer edge** and preserves Step-5.10 source refs, typed coverage and projection-contract generation as the baseline durable Story mechanisms. S-168 remains projection durability/publication owner; S-169 owns continuity consumption/escalation semantics.
- **SUPERSEDED_BY:** none found in this authority check.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** R2.2 actor continuity, R2.3 Context Runtime, R2.4 LLM execution, R2.5 multiplayer, R2.7 machine realization; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW because the owner boundary is explicit.
- **PROVENANCE_LINK_REQUIRED:** YES to the R2.1 design chain after eventual migration.
- **NOTE:** reviewed early; do not double count later.

## Step-5.10 + R2.1 authority relationship result

```text
STEP5_10_BASELINE_SOURCES:                    7
STEP5_10_FULL_CONTENT_REVIEWED:               7
STEP5_10_DESIGN_DESTINATIONS:                 6
STEP5_10_CURRENT_FINAL_OWNER:                 1

EARLY_R2_1_SOURCES_REVIEWED:                  1
EARLY_R2_1_CURRENT_FINAL_OWNERS:               1

STEP5_10_SUPERSEDED_BY_R2_1:                  NO
RELATIONSHIP:                                 DISTINCT COMPOSING OWNERS

STORY_PROJECTION_DURABILITY_OWNER:
  specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md

CONTINUITY_CONSUMER_EDGE_OWNER:
  specs/2026-08-24-r2-1-continuity-history-canonical-spec.md

STRANDED_ACCEPTED_LAW:                        0
EXTRACTIONS_REQUIRED:                         0
SPLITS_REQUIRED:                              0
```

## Part-14 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 169
SPECS_REMAINING: 206

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 14 / 45
  2026-08-24: 3 / 57 (reviewed early authority checks)

PART_14_SOURCES: 8
PART_14_DESIGN_DESTINATIONS: 6
PART_14_RESEARCH_DESTINATIONS: 0
PART_14_UNCHANGED_FINAL_SPEC_DESTINATIONS: 2
PART_14_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 137
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 26
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-21-step-5-11-selective-exact-semantic-continuity-owner-decision.md

WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
