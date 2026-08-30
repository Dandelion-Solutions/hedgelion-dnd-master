# Documentation Corpus Refactor — Specs Census Part 09

Status: **DURABLE CENSUS CHECKPOINT — 134 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-08.md`

This checkpoint records full-content review of the complete 2026-08-20 Step-5.6 Campaign Publication & Crash Consistency family. The already-counted Step-5.14 integrated canonical review was used only as a later-authority/supersession check and is not counted again here.

Common defaults for every entry below unless overridden:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; GitHub code search has not proved branch-complete inbound references on this non-default branch.
- physical moves remain deferred until the reference/path-repair gate is satisfied.

## 2026-08-20 — Step 5.6 Campaign Publication & Crash Consistency

### S-128 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-task-brief.md`

- **SEMANTIC_BLOCKS:**
  - physical publication/crash-consistency problem, scope, owner-fixed Python-core repository boundary and inherited Steps 5.1–5.5 constraints -> `DESIGN_PROVENANCE`; current authority: NO.
  - goals for freeze/write-set derivation, one-ref authority atomicity, exact success epistemics, crash windows, optimistic concurrency, ambiguity, idempotency, adoption, multi-domain partial success, checkpoint/projection boundary -> `DESIGN_PROVENANCE`.
  - required evidence/challenges/scenario matrix/exit gate -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-134 for accepted implementation-facing Step-5.6 law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-129..S-134; exact repository-wide inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES; S-134 canonicalization basis must continue to resolve.

### S-129 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-research-draft.md`

- **SEMANTIC_BLOCKS:**
  - evidence ledger and `PYTHON-OWNED SINGLE-REF CAS PUBLICATION` recommendation -> `DESIGN_PROVENANCE`; current authority: NO.
  - responsibility split, in-process frozen attempt concept, closure-vs-write-set derivation, single-ref authority model, preflight-vs-final guard, outcome taxonomy, ambiguity protocol, conflict classes, semantic idempotency, crash matrix, adoption, multi-domain/checkpoint/projection interface -> `DESIGN_PROVENANCE`.
  - host/deployment finding that built-in ChatGPT Data Analysis Python lacks external API networking and therefore requires a host-provided authenticated repository capability/bridge -> `DESIGN_PROVENANCE` as evidence/deployment prerequisite; current implementation-facing requirement is consolidated by S-134.
  - alternatives and preliminary decision status -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-130 technical challenge/refinement chain and ultimately S-134.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-130..S-134; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if left in compact final-spec corpus because several transport statements are later tightened.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-130 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-analytical-challenge.md`

- **SEMANTIC_BLOCKS:**
  - challenge/refinement of authority-atomic terminology, single-parent + non-force stale-write guard, ancestry-vs-current compatibility, append-only assumption, normalized no-op suppression, generation-specific dirty clearing, bounded dependency footprint, owner-defined reconciliation, outcome epistemics, authenticated acting principal, host bridge prerequisite, multi-domain composition and checkpoint interface -> `DESIGN_PROVENANCE`; current authority: NO.
  - explicit deployment/access feasibility debt and no-generic-journal conclusion -> `DESIGN_PROVENANCE`.
  - final `PASS WITH MATERIAL TECHNICAL REFINEMENTS` synthesis -> `DESIGN_PROVENANCE`.
- **SUPERSEDED_BY:** S-131 candidate and ultimately S-134; additional adversarial refinements in S-132/S-133.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-131..S-134; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained beside final spec because intermediate ancestry semantics are subsequently tightened.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-131 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-candidate-spec.md`

- **SEMANTIC_BLOCKS:**
  - candidate Laws 5.6-1..31, conceptual Python interface, normal publication protocol, failure/ambiguity matrix, save/security/deployment consequences and deferred realization -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
  - candidate authority-atomic single-ref model and Python-owned RepositoryPort requirement -> accepted direction but current authority: NO; final carrier S-134.
- **CURRENT AUTHORITY:** NO; status explicitly candidate/adversarial review required.
- **SUPERSEDED_BY:** S-134 after S-132/S-133 refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-132..S-134; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if left in `specs/` because candidate laws look final but lack later AR refinements.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-132 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-adversarial-review.md`

- **SEMANTIC_BLOCKS:**
  - AR-1..AR-10 required refinements: ancestry never sufficient by itself for `saved`; bounded/server-side lineage evidence; success response gives point-in-time authority only; resulting-tree completeness before first remote object; explicit delete normalization; narrow post-preflight race window; bounded retries; authorization dependencies in conflict footprint; trustworthy acting-principal/audit evidence; Python bridge as real deployment blocker -> `DESIGN_PROVENANCE`.
  - AR-11/AR-12 runtime/test debt and AR-13/AR-14 scope guards for multi-domain order and fictional chronology -> `DESIGN_PROVENANCE`.
  - failure-matrix rereview and `PASS WITH REQUIRED REFINEMENTS` -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; findings are resolved by S-133 and incorporated by S-134.
- **SUPERSEDED_BY:** S-134 for current law; S-133 records dispositions.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-133/S-134; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move, but review text in `specs/` would pollute compact final-law discovery.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-133 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-resolution-gate.md`

- **SEMANTIC_BLOCKS:**
  - R1..R18 accepted refinements covering authority atomicity, single-parent invariant, preflight status, current-closure proof, bounded lineage, normalized empty delta, resulting-tree completeness, generation-specific dirty clearing, dependency footprint, owner-only reconciliation, epistemic outcomes, bounded retry, auth revalidation, acting-principal bridge, RepositoryPort prerequisite, narrow race window, multi-domain compatibility and no generic journal -> `DESIGN_PROVENANCE` / closure evidence.
  - D1..D4 explicit deployment/acting-principal/runtime/test debt -> `DESIGN_PROVENANCE`.
  - gate result `READY FOR CANONICALIZATION` -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all accepted refinements/debt dispositions are incorporated or explicitly carried by S-134.
- **SUPERSEDED_BY:** S-134 as current Step-5.6 implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-134; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-134 — `2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — STEP 5.6 ARCHITECTURE CLOSED`.
- **CURRENT AUTHORITY:** YES as detailed Step-5.6 owner.
- **CURRENT LAW:** deterministic Python core is sole runtime repository-transport executor; every persistence-capable deployment must provide a trustworthy authenticated `RepositoryPort`; the port is transport, not gameplay authority; freeze authority/dependency inputs before remote mutation; prove resulting-tree completeness locally; distinguish durable source closure from physical writes; normalize explicit UPSERT/DELETE delta and suppress empty/no-op commits; exact pinned base tree; one logical campaign durability boundary -> one complete tree + one single-parent commit; prepared objects non-authoritative; preflight is optimization; final stale-write guard is parent(C)=pinned H + non-force ref selection; authority changes only at ref selection; transport preserves accepted/rejected/indeterminate epistemics; normal confirmed success needs no redundant reread; ambiguity cannot be acknowledged/blindly retried and uses bounded exact lineage evidence; lineage and current closure proof are separate; non-append-only history is integrity evidence; unresolved ambiguity remains unresolved; HEAD movement classification uses bounded semantic/auth/recovery footprint; disjoint movement may transport-rebuild without gameplay replay; overlap reconciliation must be native-owner-defined; semantic idempotency but no commit-SHA idempotency; retries bounded; authorization dependencies revalidated; acting principal preserved; narrow deterministic post-preflight phase; dirty clearing generation-specific; local bookkeeping non-authoritative; no generic publication journal; multi-domain publication composed rather than distributed-atomic; checkpoints only join same-ref transaction when independently required; projections may lag; no unsafe repository-config fallback; per-ref local mutex only optimization; Git storage order is not fictional chronology.
- **DEPLOYMENT/REALIZATION OBLIGATION CARRIED BY OWNER:** Python-to-repository authenticated bridge is a required feasibility prerequisite; plain built-in ChatGPT Data Analysis Python alone does not satisfy it. This remains an implementation/deployment blocker, not an unresolved Step-5.6 semantic decision.
- **SUPERSEDED_BY:** none found. Step-5.14 integrated canonical review supplements earlier Step-5 slices and does not replace detailed owners.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** Steps 5.7–5.14, Step-6 host/deployment feasibility and later machine-realization planning; exact path inbound set pending.
- **DUPLICATION_RISK:** LOW while S-128..S-133 are demoted to provenance; HIGH if candidate/gate are treated as coequal current law.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve S-128..S-133 canonicalization-basis references after eventual moves.

## Step-5.6 semantic-family result

```text
STEP5_6_BASELINE_SOURCES:                     7
STEP5_6_FULL_CONTENT_REVIEWED:                7
STEP5_6_DESIGN_DESTINATIONS:                  6
STEP5_6_CURRENT_FINAL_OWNER:                  1
STEP5_6_SPLITS_REQUIRED:                      0
STEP5_6_EXTRACTIONS_REQUIRED:                 0
STEP5_6_STRANDED_ACCEPTED_LAW:                0
STEP5_6_UNRESOLVED_SUPERSESSION:              0

CURRENT_STEP5_6_OWNER:
  specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md

LATER_INTEGRATION_RELATIONSHIP:
  Step 5.14 supplements cross-slice integration and explicitly does not replace
  the detailed Step-5.6 owner contract.
```

## Part-09 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 134
SPECS_REMAINING: 241

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 72 / 92
  2026-08-21: 2 / 45 (reviewed early for integration/supersession checks)

PART_09_SOURCES: 7
PART_09_DESIGN_DESTINATIONS: 6
PART_09_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_09_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 109
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 20
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not reliably available from GitHub code search for this non-default branch.

NEXT_UNREVIEWED_SOURCE:
  design/2026-08-20-step-5-7-checkpoint-recovery-protocol-task-brief.md

2026_08_20_REMAINING: 20
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```
