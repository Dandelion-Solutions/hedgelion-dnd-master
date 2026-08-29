# Documentation Corpus Refactor — Specs Census Part 23

Status: **DURABLE CENSUS CHECKPOINT — 241 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-22.md`

This checkpoint records full-content review of the complete seven-file 2026-08-24 R2.3 Context Runtime / Retrieval / Lazy Discovery / Allocation specs family.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` for the derivation chain named by the canonical owner.

## Authority / consolidation result

The owner selected **Alternative B — Bounded Multi-Channel Discovery + Packet-First Allocation** and additionally approved three physical/reconstruction constraints that are implementation-relevant but do not create new semantic owners:

- plausible high-cardinality durable file-per-record collections support deterministic bounded physical sharding while stable identity remains path-independent;
- current per-type indexes remain monolithic routing projections until measured scale/host evidence triggers reconsideration;
- Git/native files remain durable reconstruction/interchange representations while HOT/SQLite may physically host current established SOFT owner state and caches/query structures without SQLite format becoming authority or sole durable canon.

The canonical R2.3 specification incorporates all of those owner decisions and all eight adversarial amendments:

1. required packet is bounded typed staged closure, not necessarily a static flat list;
2. bounded discovery is not global closed-world proof; exhaustive scope requires an owner contract;
3. eligibility may require minimum targeted internal reads distinct from role-evidence admission;
4. HOT/SQLite may physically host current owner state but cache/index freshness does not create authority;
5. monolithic-index hot-path lookup must not require enumerating every physical entity directory;
6. shard path/bucket remains routing-only and migration-safe;
7. persistent fairness/starvation state is not introduced without measured need;
8. broader historical fallback is dependency-specific and finitely bounded.

The resolution gate confirms no remaining owner decision and adds no independent implementation-facing law. Therefore no accepted R2.3 semantics are stranded outside the canonical specification.

## S-235 — `2026-08-24-r2-3-context-runtime-lazy-discovery-task-brief.md`

- **SEMANTIC_BLOCKS:** Context Runtime discovery/decision-context problem; required DISCOVER -> SELECT/VERIFY -> LOAD -> ALLOCATE/DEGRADE -> PROJECT model; candidate metadata/currentness/eligibility; complete packets; semantic allocation/degradation; retrieval depth; dedup; centralized token estimate; trace/dry-run; inherited laws; Source Manifest; attacks; alternatives A/B/C; exit criteria -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; task/process framing only.
- **SUPERSEDED_BY:** S-240 canonical specification for accepted law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained beside final spec because it contains unresolved alternatives/research obligations.
- **STRANDED ACCEPTED LAW:** none.

## S-236 — `2026-08-24-r2-3-context-runtime-decision-brief.md`

- **SEMANTIC_BLOCKS:** established facts F1..F8; alternatives A scene-manifest-dominant / B bounded multi-channel packet-first / C query-on-demand; candidate descriptor/channels/bounds/eligibility/currentness; ContextNeedProfile and representation floors; packet-first allocation; optional ranking/dedup/progressive history; central budget estimator; assembly outcomes; ContextTrace; recommendation B; proposed L1..L19 and research-item dispositions -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; owner choice pending.
- **SUPERSEDED_BY:** S-237 owner decision and S-240 canonical specification.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained because rejected alternatives and proposed law wording can be mistaken for final contract.
- **STRANDED ACCEPTED LAW:** none.

## S-237 — `2026-08-24-r2-3-context-runtime-owner-decision.md`

- **SEMANTIC_BLOCKS:** owner approval of Alternative B; eight core Context Runtime obligations; high-cardinality deterministic record sharding; explicit monolithic-index decision and revisit trigger; YAML/native-file versus HOT/SQLite responsibility boundary; deferred physical details -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical decision boundary, fully consolidated by S-240.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-240 carries the approved discovery/allocation direction, sharding/index decisions, YAML/SQLite boundary and later adversarial corrections.
- **SUPERSEDED_BY:** S-240 as compact current carrier; consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained as coequal owner because pre-adversarial wording around packet closure/SQLite/index behavior is materially refined by S-239/S-240.
- **STRANDED ACCEPTED LAW:** none.

## S-238 — `2026-08-24-r2-3-context-runtime-candidate-spec.md`

- **SEMANTIC_BLOCKS:** candidate multi-channel discovery, request/need profile, discovery channels, bounded expansion, monolithic index, deterministic record sharding, routed currentness, eligibility, packet-first allocation, representation floors, optional ranking, conservative dedup, historical retrieval, centralized budgeting, typed assembly outcomes, trace/dry-run, YAML/SQLite boundary and candidate L1..L19 -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; eight adversarial completeness corrections remain outstanding.
- **SUPERSEDED_BY:** S-240 after S-239 refinement.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained because it resembles final law while lacking staged required closure, exhaustive-scope distinction and several storage/routing safeguards.

## S-239 — `2026-08-24-r2-3-context-runtime-adversarial-review.md`

- **SEMANTIC_BLOCKS:** AR-1..AR-8 attacks and required amendments over staged packet closure, non-closed-world discovery, eligibility internal reads, HOT/SQLite owner-vs-cache authority, monolithic index hot-path enumeration, shard-path coupling, fairness-state overengineering and dependency-specific bounded historical escalation -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; every amendment is incorporated into S-240.
- **SUPERSEDED_BY:** S-240 current law and S-241 closure evidence.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; attack/refinement detail is useful provenance rather than normal implementation input.
- **STRANDED ACCEPTED LAW:** none.

## S-240 — `2026-08-24-r2-3-context-runtime-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — R2.3 ARCHITECTURE CLOSED SUBJECT TO RESOLUTION GATE` and closure gate subsequently passes.
- **CURRENT AUTHORITY:** YES as current Context Runtime discovery/retrieval/currentness/eligibility/packet-closure/allocation/trace/storage-routing owner.
- **CURRENT LAW:** context is ephemeral materialized logical projection; registered task-owned requiredness; discovery-before-load; bounded multi-channel discovery with scene as primary seed but not closed-world oracle; required packet is bounded typed staged closure; no generic graph walk; monolithic routing indexes with no ordinary directory enumeration; index partitioning dormant; deterministic high-cardinality file sharding with stable-ID/path separation; routed currentness; minimum internal eligibility reads before role-local admission; packet-first allocation; source/consumer-owned representation floors; centralized size estimation; optional ranking cannot override authority/eligibility/requiredness; conservative typed dedup; dependency-specific bounded historical escalation; `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE` with non-looping failure; restricted ContextTrace/dry-run; semantic-owner-relative HOT/SQLite boundary; native-file durability publication; downstream R2.4/R2.6/R2.7 obligations; no new generic memory/query/vector/partition/fairness/background subsystem.
- **SUPERSEDED_BY:** none found.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`.
- **LIVE CONSUMERS / REFERENCES:** R2.4 single-context execution, R2.5 multiplayer, R2.6 assurance, R2.7 machine realization, Context Runtime schemas/indexes/SQLite realization; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after S-235..S-239/S-241 move to provenance.

## S-241 — `2026-08-24-r2-3-context-runtime-resolution-gate.md`

- **SEMANTIC_BLOCKS:** owner-decision satisfaction, exit-criteria matrix, AR-1..AR-8 disposition, Diamond/Strong accounting, conscious monolithic-index debt/revisit trigger, approved sharding physical constraint, downstream handoff and R2.3 closure -> `DESIGN_PROVENANCE / closure evidence`.
- **CURRENT AUTHORITY:** NO as separate semantic owner; S-240 owns current law and current roadmap owns live sequencing.
- **SUPERSEDED_BY:** S-240 for semantic law; roadmap for current status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM if retained because it mixes completeness/debt proof with historical closure/status.
- **STRANDED ACCEPTED LAW:** none; owner-approved physical debt/constraints are already present in S-240.

## R2.3 family result

```text
R2_3_BASELINE_SPECS_SOURCES:                  7
R2_3_DESIGN_DESTINATIONS:                     6
R2_3_CURRENT_FINAL_SPEC:                      1
R2_3_RESEARCH_DESTINATIONS:                   0
R2_3_SPLITS_REQUIRED:                         0
R2_3_EXTRACTIONS_REQUIRED:                    0
R2_3_STRANDED_ACCEPTED_LAW:                   0
R2_3_UNRESOLVED_SUPERSESSION:                 0

KEEP_IN_SPECS:
  S-240  2026-08-24-r2-3-context-runtime-canonical-spec.md

MOVE_TO_DESIGN:
  S-235..S-239, S-241
```

No new DCR conflict/debt item is required.

## Part-23 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 241
SPECS_REMAINING: 134

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 26 / 57
  2026-08-25: 15 / 55

PART_23_NEW_SOURCES: 7
PART_23_DESIGN_DESTINATIONS: 6
PART_23_RESEARCH_DESTINATIONS: 0
PART_23_FINAL_SPEC_DESTINATIONS: 1
PART_23_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 201
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 34
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  2026-08-24 R2.4 Single-Context LLM Execution / Chronicler service clarification
```
