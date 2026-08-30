# Documentation Corpus Refactor — Specs Census Part 17

Status: **DURABLE CENSUS CHECKPOINT — 195 / 375 PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-16.md`

This checkpoint records full-content review of the complete 2026-08-21 Step-5.13 Garbage Collection / Orphan Cleanup family and a later-authority/supersession sweep through Step 5.14 and the current derivative canonical architecture index.

Common defaults unless overridden:
- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; semantic destination does not authorize physical relocation while DCR-016 remains open.
- physical moves remain deferred until the branch-complete inbound-reference/path-repair gate is satisfied.

## Later-authority / supersession result

Fresh current-owner comparison found no later source that supersedes the detailed Step-5.13 owner:

- Step 5.14 explicitly states that its integrated closure supplements earlier Step-5 slices only where it records an integration clarification and does not replace their detailed owner contracts;
- Step-5.14 LAW 5.14-2 tightens cross-source cleanup protection timing while retaining Step-5.13 as the detailed cleanup owner;
- the current derivative `CANONICAL_ARCHITECTURE_INDEX.md` continues to route Step 5.13 as a CLOSED detailed owner for owner-gated retirement / closed blockers / complete typed protection / current-basis proof / survivor-before-removal.

Therefore the final Step-5.13 canonical specification remains current detailed authority.

## Step 5.13 family

### S-189 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-task-brief.md`
- **SEMANTIC_BLOCKS:** solution-blind Step-5.13 problem framing; owner-delegated decision boundary; inherited Steps 5.1–5.12 constraints; required runtime/checkpoint/message/Story/chronology/live-ref/Git-object/index artifact families; explicit non-goals; quality attributes; repository/external research requirements; alternative space and adversarial/exit gates -> `DESIGN_PROVENANCE`; current authority: NO.
- **SUPERSEDED_BY:** S-190..S-195 for accepted direction; S-195 is the current implementation-facing owner.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** Step-5.13 derivation chain; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move; HIGH discovery noise if retained in final `specs/` because it authorizes investigation rather than prescribing current implementation law.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve route to S-195.

### S-190 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-research-draft.md`
- **SEMANTIC_BLOCKS:** repository/architecture observations; Git/GitHub capability facts; five-layer distinction between semantic terminality, compaction, current-namespace retirement, ref retirement and host-managed object reclamation; proposed `SafeRetirementProof` shape; closed cleanup contract; candidate discovery vs authorization; reverse protection routing; cross-source concurrency; replacement-before-removal; artifact responsibility matrix; alternatives and preliminary recommendation -> `DESIGN_PROVENANCE`; current authority: NO.
- **RATIONALE:** integrated architecture research draft directly consumed by the Step-5.13 design chain. Its platform observations and provisional architecture are retained as derivation evidence, while current law is consolidated in S-195. No independent research-only owner is required for downstream implementation.
- **SUPERSEDED_BY:** S-191 challenge, S-192 candidate, S-193/S-194 review/closure and S-195 canonical.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** S-191..S-195; exact inbound set pending.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because it contains preliminary contract vocabulary and time-sensitive Connector/Git capability findings mixed with design synthesis.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve evidence qualifiers and final-owner route.
- **EXTRACTION_REQUIRED:** NO; no stranded accepted law or independently required standalone research result was found.

### S-191 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-analytical-challenge.md`
- **SEMANTIC_BLOCKS:** falsification/tightening of the research recommendation across cleanup-contract authority, completeness-typed reverse routing, cross-source blocker creation, Git-history exact-text resurrection, reference-survival semantics, cycles, idempotency survivors, verified-exact Transcript basis, sparse disclosure retention, checkpoint cleanup, stale live refs and related cleanup risks -> `DESIGN_PROVENANCE`; current authority: NO.
- **CURRENT RELATIONSHIP:** recommendation survives with tighter compatibility, completeness, survivor and reference-semantics requirements; no owner-level decision required.
- **SUPERSEDED_BY:** S-192..S-195 for accepted law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; it remains useful reopening/audit provenance.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-192 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-candidate-spec.md`
- **SEMANTIC_BLOCKS:** law-like candidate architecture for owner-gated retirement; five cleanup layers; no universal GC authority/refcount/frontier; cleanup contracts; ephemeral safe-retirement assessment; candidate discovery; completeness-typed protection routing; cross-source blocker creation; survivor-before-removal; reference survival; execution/checkpoint/message/Story/chronology/disclosure/live-ref/Git-object cleanup; publication/maintenance/legacy/debt/test requirements -> `SUPERSEDED` / `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; explicitly candidate requiring adversarial review.
- **SUPERSEDED_BY:** S-193/S-194 refinements and S-195 canonical consolidation.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` because it presents near-final laws before the mandatory 12-finding adversarial corrections.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-193 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-adversarial-review.md`
- **SEMANTIC_BLOCKS:** 12 required blockers/refinements covering cleanup-contract evolution/runtime adoption; Interaction/message dereference semantics; protection-routing generation retirement; ambiguous ref deletion; semantic removal vs secure erasure; Story enumeration/migration continuity; long-lived idempotency anchors; verified-exact certification survivor scope; checkpoint reader races; unclassified refs/nonreused epoch identity; sparse cross-generation Story survivors; future diagnostic evidence -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; review explicitly finds blockers but mechanically resolves all without owner trade-off.
- **SUPERSEDED_BY:** S-194 resolution gate and S-195 canonical.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if retained in `specs/` because it mixes attack surfaces, transitional candidate wording and accepted refinements.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-194 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-resolution-gate.md`
- **SEMANTIC_BLOCKS:** closure of all 12 adversarial findings; final architecture direction; nine common proof obligations P1–P9; reference-survival semantic requirement; protection-routing requirement; Git semantic-retention/history boundary; live-ref classes; execution/idempotency boundary; no-owner-decision result and canonicalization checklist -> `DESIGN_PROVENANCE` / closure evidence.
- **CURRENT AUTHORITY:** NO; status explicitly says ready for canonical consolidation.
- **SUPERSEDED_BY:** S-195.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; HIGH if treated as a coequal current owner beside S-195.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-195 — `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`
- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; status `CANONICAL — STEP 5.13 ARCHITECTURE CLOSED`.
- **CURRENT AUTHORITY:** YES as the detailed Garbage Collection / Orphan Cleanup owner.
- **CURRENT LAW:** cleanup is a deterministic maintenance composition over native owners, not a universal liveness authority; semantic terminality, representation compaction, current-namespace retirement, ref retirement and host object reclamation are distinct; automatic retirement requires compatible closed cleanup contracts and pinned current-basis proof; stale/unknown/incompatible evidence biases to retain; candidate discovery may be best-effort but negative-loss proof requires completeness-typed protection routing; blocker-creating native sources require self-contained consumers, protection registration or source fencing; survivor/reference closure precedes loss; reference semantics distinguish current-target, opaque provenance and survivor-backed forms; active/unsettled execution remains protected while detailed terminal payload may compact behind minimum idempotency/causal survivors; checkpoints, message envelopes, Story, chronology and live refs follow their native contracts; valid sparse `runtime.disclosure` is not ordinary age-based garbage; ACTIVE/CLOSED_UNABSORBED live refs cannot be deleted; optional ref deletion occurs only after authority ended and uses targeted verification on ambiguous result; current-tree retirement does not erase Git history and no ordinary secure-erasure promise exists; prepared losing objects are nonauthority and server reclamation remains host-managed; maintenance is bounded/optional and creates no background job/heartbeat; legacy/unknown state is retain-first; false-positive deletion is forbidden.
- **SUPERSEDED_BY:** none found. Step 5.14 explicitly supplements rather than replaces detailed owners and retains Step-5.13 cleanup semantics, including stricter cross-source protection-before-acceptance integration.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`.
- **LIVE_CONSUMERS / REFERENCES:** Step 5.14 integrated recovery/concurrency closure; R2.7 machine realization; runtime/message/Story/chronology/checkpoint/live-ref integrity and maintenance implementation; exact inbound set pending.
- **DUPLICATION_RISK:** LOW once S-189..S-194 move to `design/`.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve canonicalization-basis links after eventual moves.

## Family result

```text
STEP5_13_BASELINE_SOURCES:                    7
STEP5_13_FULL_CONTENT_REVIEWED:               7
STEP5_13_DESIGN_DESTINATIONS:                 6
STEP5_13_RESEARCH_DESTINATIONS:               0
STEP5_13_CURRENT_FINAL_OWNER:                 1
STEP5_13_SPLITS_REQUIRED:                     0
STEP5_13_EXTRACTIONS_REQUIRED:                0
STEP5_13_STRANDED_ACCEPTED_LAW:               0
STEP5_13_UNRESOLVED_SUPERSESSION:             0

CURRENT_STEP5_13_OWNER:
  specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md
```

## Conflict / deferred-debt extraction

Part 17 requires a dedicated nonduplicative residual realization entry for Step-5.13 because cleanup correctness depends on several current accepted contracts that are not yet proven machine-realized: cleanup-contract generation/compatibility, completeness-typed protection routing, cross-source blocker enrollment/fencing, reference-survival semantics, survivor-before-removal, compact idempotency/checkpoint/message/Story/chronology cleanup paths, live-ref cleanup and RepositoryPort ref-delete capability, conservative legacy migration and semantic-retention-vs-Git-history behavior. This must be appended to the conflict/debt register before the Part-17 slice is considered fully closed.

## Part-17 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 195
SPECS_REMAINING: 180

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 40 / 45
  2026-08-24: 3 / 57 (reviewed early authority checks)

PART_17_SOURCES: 7
PART_17_DESIGN_DESTINATIONS: 6
PART_17_RESEARCH_DESTINATIONS: 0
PART_17_UNCHANGED_FINAL_SPEC_DESTINATIONS: 1
PART_17_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 160
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 29
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not yet proven; DCR-016 remains open.

NEXT_UNREVIEWED_SOURCE:
  design/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-task-brief.md

WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```