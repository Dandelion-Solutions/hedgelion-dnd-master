# Documentation Corpus Refactor — Specs Census Part 18

Status: **DURABLE CENSUS CHECKPOINT — 200 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-17.md`

This checkpoint records full-content review of the remaining 2026-08-21 Step-5.14 Full Recovery / Concurrency Adversarial Review provenance family, a full-content review of the previously omitted Step-6 pre-design framing working note, and a later-authority sweep through the 2026-08-23 Step-4 single-context canonical amendment and Round-1 Step-6 closure / Round-2 rebaseline owner decision.

**Census correction:** the Step-5.14 canonical final was already fully reviewed and counted as **S-118** in Specs Census Part 07. The original Part-18 publication incorrectly assigned that same baseline source a second ID `S-200` while omitting `2026-08-21-step-6-pre-design-framing-working-notes.md`. This corrected checkpoint preserves the unique-source cursor at 200 by:

- reusing **S-118** for the already-counted Step-5.14 canonical final;
- assigning **S-200** to the genuinely previously unreviewed Step-6 pre-design framing working note;
- keeping all later IDs unchanged.

The independent 2026-08-20..2026-08-21 branch compare confirms the omitted working note belongs to the 2026-08-21 specs date group. With this correction the date group is genuinely **45 / 45 unique baseline sources reviewed**.

Common defaults unless overridden:
- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; semantic destination does not authorize physical relocation while DCR-016 remains open.

## Later-authority / supersession result

Step 5.14 remains the current canonical Step-5 cross-slice integration/closure owner. The later 2026-08-23 program decision explicitly inherits accepted Steps 1–5 architecture and does not reopen Step-5 durability/recovery/currentness/concurrency ownership.

However, one forward-looking physical-feasibility detail inside the Step-5.14 canonical final is later superseded:

- Step-5.14 treats genuine role-context isolation/reset as a Step-6 blocking feasibility dependency for mixed-privilege logical-role topology.
- The later owner-approved Step-4 single-context amendment explicitly supersedes the baseline requirement for separate physical invocations/context reset and replaces it with logical role containment inside one physical chat context.
- The Round-1 Step-6 closure decision then retires mandatory physical role isolation/reset as a baseline architecture requirement and reallocates remaining Step-6 concerns into Round 2.

This does **not** supersede Step-5.14 Laws 5.14-1..4 or the general principle in Law 5.14-5 that physical feasibility failure must not silently weaken accepted semantics. It makes the role-isolation/reset example and SD-5 wording a stale derivative surface tracked as DCR-020.

## Step 5.14 family — newly reviewed provenance

### S-196 — `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-task-brief.md`
- **SEMANTIC_BLOCKS:** integrated Step-5 adversarial-review scope, fixed owner/currentness/durability constraints, scenario requirements, authority-contamination attacks, review classifications, explicit non-goals and closure gates -> `DESIGN_PROVENANCE`; current authority: NO.
- **SUPERSEDED_BY:** S-197..S-199 review/closure chain and already-counted S-118 canonical final.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** Step-5.14 review chain; exact inbound set pending.
- **DUPLICATION_RISK:** LOW after move; high discovery noise if retained in final implementation-facing corpus.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-197 — `2026-08-21-step-5-14-integrated-adversarial-review-draft.md`
- **SEMANTIC_BLOCKS:** thirty integrated attack routes; cross-front findings F1–F10; Step-6 feasibility dependencies SD-1..SD-6; accepted product limitations; implementation-debt clusters; composite attacks; authority/contamination sweep; preliminary no-blocker verdict and falsification targets -> `DESIGN_PROVENANCE`; current authority: NO.
- **CURRENT RELATIONSHIP:** review evidence/derivation only. Its preliminary feasibility ledger includes the later-superseded physical role-isolation assumption; current Step-5 integration law is S-118 and later host/topology authority is controlled by 2026-08-23+ owners.
- **SUPERSEDED_BY:** S-198 challenge, S-199 gate and S-118 canonical final for accepted Step-5 closure.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained in `specs/` because it is explicitly pre-resolution and contains forward-looking assumptions later revised.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-198 — `2026-08-21-step-5-14-analytical-challenge.md`
- **SEMANTIC_BLOCKS:** falsification of the no-blocker conclusion across multi-source recovery, multi-live execution, cleanup races, concurrent disclosure, revocation/emission, Step-4 frontier interpretation, Story/Transcript/compaction, Git history and Step-6 deferral; AC-1..AC-5 integration clarifications and simpler-alternative rejection -> `DESIGN_PROVENANCE`; current authority: NO.
- **SUPERSEDED_BY:** S-199/S-118 for accepted integration law.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if retained in `specs/`; it mixes adversarial reasoning with pre-canonical clarification text.
- **PROVENANCE_LINK_REQUIRED:** YES.

### S-199 — `2026-08-21-step-5-14-resolution-gate.md`
- **SEMANTIC_BLOCKS:** zero-blocker gate verdict; blocker ledger; canonical integration clarifications C-5.14-1..5; accepted limitations; Step-6 feasibility gate ledger; implementation-debt disposition; reopen conditions and canonicalization authorization -> `DESIGN_PROVENANCE` / closure evidence; current authority: NO.
- **SUPERSEDED_BY:** S-118 for current Step-5 integration law. Later 2026-08-23 owners revise the physical role-isolation/reset feasibility assumption rather than the Step-5 semantic closure itself.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained as coequal current law beside S-118.
- **PROVENANCE_LINK_REQUIRED:** YES.

## Step 5.14 current owner — revalidated, not recounted

### Existing S-118 — `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`
- **CENSUS ID AUTHORITY:** S-118 from Specs Census Part 07. This source is **not a new Part-18 census source**.
- **FULL-CONTENT REVALIDATION:** YES.
- **SEMANTIC_BLOCKS:**
  - Step-5 closure verdict, integrated invariant, Laws 5.14-1..4, general non-weakening principle of Law 5.14-5, scenario/composite closure, accepted product limitations, implementation-debt clusters, authority-contamination result, falsifiability and Step-5 stage closure -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; **CURRENT AUTHORITY: YES** as Step-5.14 cross-slice integration/closure owner.
  - Law 5.14-5 example list / Section 7 SD-5 wording requiring genuine physical role-context isolation/reset for mixed-privilege topology -> `SUPERSEDED` as a baseline physical-topology requirement by `2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` and the Round-1 Step-6 closure owner decision; the broader principle that deployment feasibility cannot silently weaken semantics remains current.
  - remaining Step-6 forward-looking feasibility ledger -> historical/forward-work context whose current sequencing and concrete baseline are controlled by later Round-2 owners; it does not displace the Step-5 semantic laws.
- **CURRENT AUTHORITY:** YES, with the explicit later-authority qualification above.
- **SUPERSEDED_BY:** none for the Step-5.14 integration laws/Step-5 closure. Later 2026-08-23 owners supersede only conflicting physical role-isolation/topology implications and reallocate Step-6 sequencing.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`.
- **LIVE_CONSUMERS / REFERENCES:** accepted Steps 1–5 inheritance, Round-2 architecture, R2.7/S6D realization/audit, integrated test planning; exact inbound set pending.
- **DUPLICATION_RISK:** LOW once S-196..S-199 move to `design/`, but the embedded stale SD-5/role-isolation wording remains a documentation hazard until routed/qualified; DCR-020 records it.
- **PROVENANCE_LINK_REQUIRED:** YES; preserve canonicalization-basis links after eventual moves.
- **SPLIT_REQUIRED?:** NO. The document remains a genuine final implementation-facing owner; the later qualification is narrow and should be resolved by current-owner routing/repair, not by fragmenting the canonical closure artifact.

## Previously omitted 2026-08-21 source

### S-200 — `2026-08-21-step-6-pre-design-framing-working-notes.md`
- **SEMANTIC_BLOCKS:**
  - complete pre-design Step-6 framing, inherited Steps 3–5 constraints, owner-provided product inputs, preliminary hot-path/call-graph hypotheses, latency/cost/context/model-quality questions, role compatibility and typed handoff investigation framing -> `DESIGN_PROVENANCE`; current authority: NO.
  - physical role-isolation/reset, pre-visible Narrator staging, RepositoryPort, host identity, retry, player-visible surface, provider comparison and capability hypotheses -> `DESIGN_PROVENANCE`; many are explicitly questions/hypotheses and several physical-topology assumptions are later revised by the 2026-08-23 single-context amendment / Round-1 closure.
  - candidate Step-6 work decomposition, evaluation/canary plans, platform/provider comparison track, open research questions, security/prompt-injection/economic/portability framing and closure criteria -> `DESIGN_PROVENANCE`; current authority: NO.
- **CURRENT AUTHORITY:** NO. The source explicitly states `NON-CANONICAL / WORKING THOUGHTS / PRE-DESIGN FRAME`, denies being a task brief/spec/owner decision/approved topology/implementation plan/platform-capability evidence, and routes sequencing to the roadmap.
- **SUPERSEDED_BY:** current 2026-08-23 single-context amendment and Round-1 Step-6 closure for baseline physical topology/program decomposition; later Round-2 R2.1–R2.7/current roadmap owners for accepted architecture and sequencing. Retain this source as design provenance of the pre-Round-2 framing.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **LIVE_CONSUMERS / REFERENCES:** historical Step-6/Round-2 framing and later role/host/assurance work; exact inbound set pending.
- **DUPLICATION_RISK:** VERY HIGH if retained in `specs/` because preliminary constraints, candidate laws and proposed decomposition could be mistaken for current accepted Step-6 architecture despite explicit noncanonical status.
- **PROVENANCE_LINK_REQUIRED:** YES where later Round-2 sources cite the framing.
- **EXTRACTION_REQUIRED:** NO. Current owner/product law is carried by later accepted sources; this file contains framing/hypotheses rather than a stranded final owner.

## Family/date-group result

```text
STEP5_14_BASELINE_SOURCES:                    5
STEP5_14_FULL_CONTENT_REVIEWED:               5
STEP5_14_NEW_SOURCES_COUNTED_PART18:          4
STEP5_14_DESIGN_DESTINATIONS:                 4
STEP5_14_CURRENT_FINAL_OWNER:                 1  # S-118, counted in Part 07

STEP6_PREDESIGN_WORKING_NOTES_NEW:             1  # S-200
STEP6_PREDESIGN_DESIGN_DESTINATIONS:           1

PART18_UNIQUE_NEW_BASELINE_SOURCES:            5
PART18_REVALIDATED_ALREADY_COUNTED_SOURCES:    1  # S-118
PART18_SPLITS_REQUIRED:                        0
PART18_EXTRACTIONS_REQUIRED:                   0
PART18_STRANDED_ACCEPTED_LAW:                  0
PART18_UNRESOLVED_SUPERSESSION:                0

CURRENT_STEP5_14_OWNER:
  S-118
  specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md
```

## Conflict / deferred-debt extraction

DCR-020 records the stale physical-role-isolation/reset feasibility wording embedded in the otherwise-current Step-5.14 canonical final. Do not treat that historical Step-6 gate as an active unfulfilled requirement after the later single-context owner decision.

No new machine-realization debt is created merely from S-200: it is a pre-design framing source and later Round-2/S6D/current owners must be consulted before any historical Step-6 question is treated as current debt.

## Part-18 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 200
SPECS_REMAINING: 175

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-24: 3 / 57 (reviewed early authority checks)

PART_18_UNIQUE_NEW_SOURCES: 5
PART_18_DESIGN_DESTINATIONS: 5
PART_18_REVALIDATED_ALREADY_COUNTED_FINAL_OWNER: 1  # S-118
PART_18_NEW_FINAL_SPEC_DESTINATIONS: 0
PART_18_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 165
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_DESTINATIONS_CONFIRMED: 29
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS:
  NOT STARTED
  Reason unchanged: branch-complete inbound-reference/path-repair evidence is not yet proven; DCR-016 remains open.

NEXT_UNREVIEWED_SOURCE:
  specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md

WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED
```