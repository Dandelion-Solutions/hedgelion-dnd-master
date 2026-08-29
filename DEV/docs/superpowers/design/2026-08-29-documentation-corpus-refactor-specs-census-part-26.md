# Documentation Corpus Refactor — Specs Census Part 26

Status: **DURABLE CENSUS CHECKPOINT — 263 / 375 UNIQUE PRE-REFACTOR SPECS SOURCES FULLY REVIEWED**
Date: 2026-08-29
Baseline ref: `v1/engine-rearchitecture`
Baseline corpus SHA: `0ebe6c384c88b8d998ce9e385ab0758a6f25e3f6`
Baseline `specs/` tree SHA: `0fb176ec4cee7af3d6765a34174964679c99819d`
Previous specs census: `DEV/docs/superpowers/design/2026-08-29-documentation-corpus-refactor-specs-census-part-25.md`

This checkpoint records full-content review of the complete seven-file 2026-08-24 R2.6 ChatGPT Plus / MVP Host Assurance specs family.

Common defaults:

- `FULL_CONTENT_REVIEWED: YES`
- `SPLIT_REQUIRED?: NO`
- `EXTRACTION_REQUIRED: NO`
- `REPOSITORY-WIDE LIVE PATH CENSUS: PENDING`; DCR-016 still blocks physical relocation.
- `PROVENANCE_LINK_REQUIRED: YES` for the canonicalization/owner-clarification chain.

## Authority / consolidation result

R2.6 contains two genuine owner-approved clarifications that materially changed the stage before canonical closure.

### Fixed repository transport

Repository transport selection was explicitly closed to the already-selected runtime path:

```text
deterministic Python/core preparation
-> ChatGPT GitHub Connector defined Git-data/ref operations
-> non-force authoritative ref transition
```

The owner clarification forbids gameplay/runtime/assurance fallback or alternative-transport probing through `gh`, remote native Git, direct private HTTP/API/token workarounds, custom MCP/backend write services, GitHub Actions bridges or transparent local-commit push assumptions. Missing required Connector capability is a supported-profile capability failure rather than permission to improvise another transport.

### MVP behavioral assurance threshold

The owner clarified that the MVP guarantee is **observable behavioral containment**, not physical/cognitive isolation. Ineligible information may be physically present in the shared chat context, but the active logical role/player-visible output must not materially use or disclose it before lawful eligibility. Prior ineligibility is not permanent forgetting: lawfully eligible information must later remain normally usable.

The owner also moved full production-like Protocol-4-derived integrated evaluation to the implemented MVP rather than requiring a pre-R2.7 parallel-MVP harness. Protocols 1–3 are sufficient pre-implementation feasibility evidence for architecture continuation; cheap bounded blocker checks remain allowed when they answer a concrete architecture question. Protocol-4 scenarios remain mandatory downstream acceptance/test obligations rather than disappearing.

The canonical R2.6 specification fully consolidates both owner clarifications and all fourteen adversarial amendments. The resolution gate explicitly confirms 17/17 revised architecture-assurance criteria pass, no unresolved owner decision remains, and the old execution-heavy pre-R2.7 Protocol-4 gate is superseded only as sequencing/evidence threshold, not by dropping its behavioral requirements.

Therefore no accepted implementation-facing R2.6 law is stranded in either owner clarification, candidate, adversarial review, gate or original Task Brief.

## S-257 — `2026-08-24-r2-6-chatgpt-plus-assurance-task-brief.md`

- **SEMANTIC_BLOCKS:** R2.6 assurance-stage purpose; supported ChatGPT Plus profile; current-evidence reverification; fixed Connector-path assurance; role containment; instruction/data security; Narrator emission; ambient memory; context pressure; reasoning profile; Chronicler/multiplayer assurance; evidence-ledger semantics; adversarial scenarios; original exit criteria and Protocol-4 execution route -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO. The brief was revised after fixed-transport clarification and its broad pre-R2.7 production-like Protocol-4 execution threshold was later superseded by the MVP behavioral-assurance owner clarification/resolution gate.
- **SUPERSEDED_BY:** S-262 for current host-assurance law; S-258/S-259 record the intervening owner decisions.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** HIGH if retained in compact `specs/` because some stage-evidence/transport-selection wording no longer describes the final R2.6 closure contract.
- **STRANDED ACCEPTED LAW:** none.

## S-258 — `2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`

- **SEMANTIC_BLOCKS:** owner-approved closure of repository transport selection; exact fixed Python/core + GitHub Connector non-force path; forbidden alternate gameplay transports/fallbacks; retained prior evidence scope; narrowed R2.6 assurance question; superseded task-brief language; R2.7 wording-repair obligation -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical clarification boundary, fully consolidated by S-262.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-262 Law R2.6-9 carries the fixed transport selection, forbidden fallback class and capability-failure semantics.
- **SUPERSEDED_BY:** S-262 as compact current carrier; consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if kept as coequal final owner because implementation planning should consume one integrated R2.6 host-assurance contract rather than separately reconcile clarification-era scope wording.
- **STRANDED ACCEPTED LAW:** none.

## S-259 — `2026-08-24-r2-6-mvp-behavioral-assurance-owner-clarification.md`

- **SEMANTIC_BLOCKS:** owner-approved observable behavioral-containment MVP standard; explicit non-claim of physical/cognitive isolation; lawful post-eligibility uptake; Protocols 1–3 sufficiency for pre-implementation feasibility; full Protocol-4-derived evaluation moved after real MVP implementation; cheap bounded blocker checks preserved; downstream MVP acceptance inventory; Lab/public experiment boundary; revised R2.6 closure conditions -> `FINAL_SPEC_OR_ACCEPTED_DECISION` at the historical clarification boundary, fully consolidated by S-262.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing owner after canonical consolidation. S-262 Laws R2.6-1..3 and R2.6-10..12 plus the acceptance inventory carry the complete clarification.
- **SUPERSEDED_BY:** S-262 as current carrier; consolidation, not reversal.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM/HIGH if retained separately because it mixes final product policy with transition/process timing now fully represented by the canonical host-assurance contract.
- **STRANDED ACCEPTED LAW:** none.

## S-260 — `2026-08-24-r2-6-mvp-host-assurance-candidate-spec.md`

- **SEMANTIC_BLOCKS:** candidate supported profile; behavioral containment; lawful uptake; instruction handoff; pre-Narrator admission; auxiliary surfaces; ambient memory; context envelope; S53 resolution; fixed transport; post-implementation integrated evaluation; acceptance inventory; known-blocker-only gate -> `SUPERSEDED / DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; fourteen adversarial amendments remain outstanding in this version.
- **SUPERSEDED_BY:** S-262 after S-261 refinements.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** VERY HIGH if retained because its near-final law lacks final wording that behavioral containment is correctness/release-critical, Protocol-4 mapping cannot disappear, cheap blocker checks remain allowed, auxiliary-surface deployment gates, public/Lab boundaries and other AR clarifications.

## S-261 — `2026-08-24-r2-6-mvp-host-assurance-adversarial-review.md`

- **SEMANTIC_BLOCKS:** AR-1..AR-14 attacks/amendments over behavioral-containment strictness, lawful uptake, Protocol-4 deferral process risk, cheap pre-MVP blocker probes, visible auxiliary surfaces, ambient memory, context pressure, Chronicler anti-starvation, multiplayer currentness/generation, Dramaturg coherence, S53, D15, fixed transport and public-vs-Lab experiment governance -> `DESIGN_PROVENANCE`.
- **CURRENT AUTHORITY:** NO; all amendments are incorporated into S-262 and closure confirmed by S-263.
- **SUPERSEDED_BY:** S-262 current law and S-263 closure evidence.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** LOW after move; adversarial detail remains useful provenance but is not ordinary implementation input.
- **STRANDED ACCEPTED LAW:** none.

## S-262 — `2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`

- **SEMANTIC_BLOCKS:** entire document -> `FINAL_SPEC_OR_ACCEPTED_DECISION`; canonical R2.6 host-assurance contract and closure gate subsequently passes.
- **CURRENT AUTHORITY:** YES as the compact implementation-facing R2.6 owner.
- **CURRENT LAW:** ChatGPT Plus ordinary Project-capable one-chat-per-player MVP candidate; observable behavioral containment is correctness and material ineligible use/reveal is a release/support failure; no physical/cognitive isolation claim; lawful eligibility restores normal use; explicit shipped instruction handoff; pre-Narrator semantic admission/`EMISSION_COMMIT` baseline; auxiliary surfaces cannot intentionally carry protected material and require synthetic-canary deployment evaluation; ambient Project/chat memory has no campaign authority; no exact hidden-capacity dependency; S53 capability envelope with High recommended but no exact cross-player serving identity requirement; fixed Python/core + GitHub Connector non-force transport with no alternate runtime fallback/probing; do not build a parallel MVP to test the MVP; cheap bounded blocker checks remain allowed; exploratory probes/raw fixtures default to HDM Lab; explicit post-implementation acceptance obligations; only a known host/architecture incompatibility blocks R2.7; upstream Chronicler/multiplayer/Dramaturg laws remain unchanged; D15 dormant.
- **SUPERSEDED_BY:** none found.
- **FINAL_DESTINATION_FILES:** unchanged `specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`.
- **LIVE CONSUMERS / REFERENCES:** R2.7 machine/instruction/test mapping, implementation planning/TDD, deployment/release/MVP acceptance; exact inbound set pending.
- **DUPLICATION_RISK:** LOW once S-257..S-261/S-263 move to provenance.

## S-263 — `2026-08-24-r2-6-mvp-host-assurance-resolution-gate.md`

- **SEMANTIC_BLOCKS:** gate verdict `R2.6 MAY CLOSE`; explicit supersession of original execution-heavy pre-R2.7 Protocol-4 evidence threshold; 17 revised exit criteria; accepted limitations; AR-1..AR-14 closure; D/S dispositions; R2.7 mandatory handoff and historical stage transition -> `DESIGN_PROVENANCE / closure evidence`.
- **CURRENT AUTHORITY:** NO as a separate implementation-facing law; S-262 owns current host-assurance semantics and current roadmap owns current sequencing/status.
- **SUPERSEDED_BY:** S-262 for semantic law; roadmap/current implementation/release gates for live status.
- **FINAL_DESTINATION_FILES:** corresponding `design/` path.
- **DUPLICATION_RISK:** MEDIUM if retained because it combines useful completeness evidence with a historical stage transition and point-in-time PASS matrix.
- **STRANDED ACCEPTED LAW:** none.

## R2.6 family result

```text
R2_6_BASELINE_SPECS_SOURCES:                  7
R2_6_DESIGN_DESTINATIONS:                     6
R2_6_CURRENT_FINAL_SPEC:                      1
R2_6_RESEARCH_DESTINATIONS:                   0
R2_6_SPLITS_REQUIRED:                         0
R2_6_EXTRACTIONS_REQUIRED:                    0
R2_6_STRANDED_ACCEPTED_LAW:                   0
R2_6_UNRESOLVED_SUPERSESSION:                 0

KEEP_IN_SPECS:
  S-262  2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md

MOVE_TO_DESIGN:
  S-257..S-261, S-263
```

No new DCR conflict/debt item is required.

## Part-26 checkpoint summary

```text
SPECS_BASELINE_COUNT: 375
SPECS_FULL_CONTENT_REVIEWED: 263
SPECS_REMAINING: 112

REVIEWED_DATE_GROUPS:
  2026-08-18: 10 / 10
  2026-08-19: 50 / 50
  2026-08-20: 92 / 92
  2026-08-21: 45 / 45
  2026-08-23: 3 / 3
  2026-08-24: 48 / 57
  2026-08-25: 15 / 55

PART_26_NEW_SOURCES: 7
PART_26_DESIGN_DESTINATIONS: 6
PART_26_RESEARCH_DESTINATIONS: 0
PART_26_FINAL_SPEC_DESTINATIONS: 1
PART_26_PENDING_SEMANTIC_DISPOSITIONS: 0

CUMULATIVE_UNAMBIGUOUS_DESIGN_DESTINATIONS_REVIEWED: 221
CUMULATIVE_SPECS_TO_RESEARCH_DESTINATIONS_REVIEWED: 1
CUMULATIVE_UNCHANGED_FINAL_SPEC_OR_OWNER_DESTINATIONS_CONFIRMED: 36
CUMULATIVE_PENDING_FINAL_SUPERSESSION_CHECK: 5

PHYSICAL_MOVE_STATUS: NOT STARTED / DCR-016 OPEN
WP07_SUBSTANTIVE_ANALYSIS: NOT STARTED

NEXT_UNREVIEWED_SEMANTIC_FAMILY:
  remaining 2026-08-24 R2.7 machine-realization/final-audit process owners and Step-6/Round-2 program decisions
```
