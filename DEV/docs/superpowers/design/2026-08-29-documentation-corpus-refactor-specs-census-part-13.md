# Documentation Corpus Refactor — Specs Census Part 13

Status: **DURABLE CENSUS CHECKPOINT — 161 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED; 2026-08-20 COMPLETE**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-12.md`

This checkpoint records full-content review of the final three previously unreviewed 2026-08-20 `specs/` sources. With this checkpoint the entire pre-refactor 2026-08-20 specs date group is semantically reviewed: **92 / 92**.

Common defaults for every entry below unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; GitHub code search has not proved branch-complete inbound references on this non-default branch.
- physical moves remain deferred until the reference/path-repair gate is satisfied.

## S-159 — `2026-08-20-step-5-expanded-architecture-agenda.md`

- **SEMANTIC_BLOCKS:**
  - owner-directed expanded Step-5 sequencing/decomposition, recovery invariant and fixed constraints carried into investigation -> `DESIGN_PROVENANCE`; current authority: NO.
  - detailed investigation agendas and exit gates for Steps 5.0–5.14 -> `DESIGN_PROVENANCE`; each later canonical Step-5 owner supersedes this agenda as implementation-facing law for its slice.
  - Step-6 boundary and sequencing rule -> `DESIGN_PROVENANCE` / historical process-control evidence; current roadmap/process owners now govern active sequencing.
- **CURRENT AUTHORITY:** NO; document status explicitly says `APPROVED WORKING AGENDA — NOT A CANONICAL SUBSYSTEM SPEC`.
- **SUPERSEDED_BY:** detailed canonical Step-5.0–5.14 specifications plus current roadmap/process documents for active sequencing; no one replacement file for the historical decomposition provenance.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** historical Step-5 derivation chain, later Step-5 task/canonical artifacts and project-map/roadmap history; exact repository-wide inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because several early vocabulary assumptions (frontier/checkpoint/live details, hard-coded investigation framings) were intentionally re-derived and changed by later canonical slices.
- **PROVENANCE_LINK_REQUIRED:** YES where later Step-5 artifacts cite the expanded agenda/decomposition.
- **EXTRACTION_REQUIRED:** NO; no accepted implementation-facing law is stranded here. Durable current law resides in the later Step-5 canonical owners and current process/roadmap owners.

## S-160 — `2026-08-20-step-6-llm-role-isolation-feasibility-spike-notes.md`

- **SEMANTIC_BLOCKS:**
  - inherited Step-4 logical-role/context-isolation law quoted as input -> `DUPLICATE_OF_CURRENT_OWNER` for current authority purposes; Step-4 canonical owner remains authoritative.
  - H1–H5 preliminary platform/topology hypotheses explicitly marked `MUST BE REVERIFIED AT SPIKE TIME` -> `DESIGN_PROVENANCE`; these are research questions/hypotheses, not durable findings.
  - deployment profiles A–D, canary-isolation evaluation design, physical-role compatibility matrix, proposed Step-6 investigation sequence, future owner decision surface and reverification rule -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; status explicitly `DEFERRED FEASIBILITY-SPIKE INPUT — NOT CANONICAL ARCHITECTURE` and the file does not report completed measurements/experiments.
- **SUPERSEDED_BY:** future/current Step-6/Round-2 role-host assurance and orchestration owners for accepted conclusions; retained as design provenance of the planned feasibility investigation.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** Step-6/R2.4/R2.6 role isolation/host assurance work and future implementation planning; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because time-sensitive platform hypotheses could be mistaken for accepted architecture facts.
- **PROVENANCE_LINK_REQUIRED:** YES where later role-isolation research/assurance cites the spike agenda.
- **EXTRACTION_REQUIRED:** NO; the inherited current law belongs to Step-4 canonical owners and the remainder is investigation planning rather than accepted law.

## S-161 — `2026-08-20-step-6-repository-port-transport-feasibility-spike.md`

- **SEMANTIC_BLOCKS:**
  - Step-5.6-derived feasibility question and current restricted-Python deployment constraint -> `RESEARCH_RESULT`; evidence/context, not architecture authority.
  - Lab Experiments A–C: Python-precomputed Git blob/tree identities matched connector-created identities; inline-content tree construction; non-force ref update rejected sibling stale commit; measured prior experiment preparation/connector latency evidence -> `RESEARCH_RESULT`.
  - exact `local commit -> current connector transparent push` negative finding -> `RESEARCH_RESULT`; current connector lacks pack/bundle/native-push import semantics.
  - comparative investigation of GraphQL `createCommitOnBranch`, Git Database REST, custom deterministic RepositoryPort service, external Python/direct Git, current connector non-authoritative relay, local-commit transparent push and GitHub Actions -> `RESEARCH_RESULT` / comparative feasibility evidence.
  - recommendation ranking and architectural consequence that deterministic Python can own exact payload/object/tree/frontier closure while the missing piece is authenticated transport -> `RESEARCH_RESULT`; this supports but does not replace canonical Step-5.6.
  - mandatory future Step-6 tests/reverification and explicit `No canonical change yet` -> `RESEARCH_RESULT` with future-revisit conditions.
- **CURRENT AUTHORITY:** NO. The file explicitly says the spike supplies evidence only and canonical Step 5.6 remains unchanged.
- **SUPERSEDED_BY:** none as historical feasibility evidence. Time-sensitive platform findings must be reverified before future design reliance; current accepted transport semantics remain owned by Step-5.6 canonical and later approved Step-6/R2.6 owners.
- **FINAL_DESTINATION_FILES:** `DEV/docs/superpowers/research/2026-08-20-step-6-repository-port-transport-feasibility-spike.md`.
- **LIVE_CONSUMERS / REFERENCES:** Step-5.6 deployment/RepositoryPort carry-forward, Step-6 transport feasibility, R2.6 host assurance and implementation planning; exact inbound set pending.
- **DUPLICATION_RISK:** LOW in `research/` when clearly non-authoritative; HIGH if retained in `specs/` because recommendation/options could be mistaken for selected production transport architecture.
- **PROVENANCE_LINK_REQUIRED:** YES; retain links from later design/spec decisions to the evidence source where useful.
- **EXTRACTION_REQUIRED:** NO; all accepted architecture law remains in Step-5.6/current later owners. No research-only statement must be promoted merely to move this evidence file.

## 2026-08-20 date-group closure

```text
2026_08_20_BASELINE_SOURCES:                 92
2026_08_20_FULL_CONTENT_REVIEWED:            92
2026_08_20_REMAINING:                         0

PART_13_SOURCES:                              3
PART_13_DESIGN_DESTINATIONS:                  2
PART_13_RESEARCH_DESTINATIONS:                1
PART_13_FINAL_SPEC_DESTINATIONS:              0
PART_13_SPLITS_REQUIRED:                      0
PART_13_EXTRACTIONS_REQUIRED:                 0
PART_13_STRANDED_ACCEPTED_LAW:                0
```

## Part-13 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 161
SPECS_REMAINING: 214

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 7 / 45
  2026-08-24: 2 / 57 (reviewed early for Step-5.8 supersession check)

PART_13_SOURCES: 3
PART_13_DESIGN_DESTINATIONS: 2
PART_13_RESEARCH_DESTINATIONS: 1
PART_13_UNCHANGED_FINAL_SPEC_DESTINATIONS: 0
PART_13_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 131
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 24
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_CHRONOLOGICAL_DATE_GROUP:
  2026-08-21

ALREADY_REVIEWED_2026_08_21_SOURCES_TO_SKIP_WITHOUT_DOUBLE_COUNTING:
  specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md
  design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md
  design/2026-08-21-step-5-9-chronology-persistence-reconciliation-adversarial-review.md
  design/2026-08-21-step-5-9-chronology-persistence-reconciliation-candidate-spec.md
  specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md
  design/2026-08-21-step-5-9-chronology-persistence-reconciliation-resolution-gate.md
  specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md

WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
