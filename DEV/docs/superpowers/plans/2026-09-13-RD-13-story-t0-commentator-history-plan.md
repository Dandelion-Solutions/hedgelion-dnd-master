# RD-13 — Story / T0 / Commentator / Native History — Executable Implementation Plan

Goal: realize native SemanticEvent/history integration plus noncanonical Story projection, sparse event-time T0 basis, read-only Commentator and accepted retained multiplayer Dramaturg horizons without authority transfer.

Direct readiness: `R022,R051,R084,R085,R099,R102,R131`.
Composite slices: `R016.STORY`, `R018.STORY`, `R062.SEMANTIC_EVENT_HISTORY`, `R087.SEMANTIC_EVENT_T0`.
Owners: Story decisions/appendix, native history/continuity architecture, Multiplayer Model. RD-03 Actor continuity; RD-05 accepted execution evidence; RD-08 temporal; RD-09 access/currentness; RD-10 recipient containment; RD-12 collaboration.

## Impact Envelope
- `NEW_CREATE GAME/TOOLS/story.py`, `GAME/TOOLS/commentator.py`
- `NEW_CREATE DEV/SCHEMAS/story-state.schema.json`, `t0-baseline.schema.json`, `commentator-view.schema.json`
- native SemanticEvent/history owner schemas/catalogs — owner-controlled integration target, not Story-owned
- accepted retained multiplayer Dramaturg paths only where current owners require them
- `NEW_CREATE DEV/TESTS/test_rd13_story_t0_commentator.py`
- direct project-map/audit projections.

Forbidden: Story/history/ACL/canon authority transfer; T0 mutable T1 substitute/parallel timeline; Commentator mutation; transcript as SemanticEvent history; hidden reasoning/current pointer as T0; Story feedback into same envelope; untriggered single-player durable Dramaturg.

## Task 1 — RED authority boundaries
Tests prove native SemanticEvent/history is causal authority, Story is rebuildable projection, Commentator read-only, and T0 cannot advance independently. Expected RED: no complete v1 path.

## Task 2 — native history integration: `R062.SEMANTIC_EVENT_HISTORY`
Realize the native SemanticEvent/history slice using accepted owner contracts and RD-03/RD-05 inputs as applicable. Preserve ancestry/provenance and source suitability. Story/Commentator are consumers, never the owner. Add negative tests for transcript/history substitution and derived-source silent promotion.

## Task 3 — Story composite slices `R016.STORY` / `R018.STORY`
Implement `story-state.schema.json` and `story.py` projection/transition boundary. Wire only Story-owned portions of the composite parents; information/Actor/execution/collaboration/routing slices remain their owners. Story summary carries source/frontier identity and cannot override newer native evidence.

## Task 4 — T0 basis `R099` + `R087.SEMANTIC_EVENT_T0`
Implement deterministic sparse event-time T0 construction in `t0-baseline.schema.json`. R099 T0 precedes qualifying Story/Commentator consumption. T0 is reconstructible baseline, not mutable history/currentness authority. Preserve zero-extra-serial and disclosure boundaries required by R087.

## Task 5 — Commentator route
Implement `reconstruct_commentary(...) -> CommentatorView` over eligible Story/history/T0 evidence. No authoritative mutations, SemanticEvents, knowledge grants or currentness changes. Evidence basis is explicit and disposable.

## Task 6 — R051/R084/R102 consumer join
Prove accepted T0/history/Story inputs join the qualifying Commentator/Story consumer exactly as owner decisions require, including no hidden native-only fallback where prohibited.

## Task 7 — retained multiplayer Dramaturg / R085/R131
Integrate only accepted multiplayer retained horizons after RD-09 access/currentness and RD-12 collaboration/recipient constraints. Recipient-specific retained projections cannot become Story/history/ACL canon. No single-player durable planning system is admitted without its future trigger.

## Task 8 — Version Impact/persistence/checkpoint
Classify durable native history and Story-state schema effects separately. Route schema version/checkpoint/migration to their owners. T0 retention follows its owner; CommentatorView is not durable authority. No compatibility layer preserves legacy Story semantics by default.

## Task 9 — verification/currentness
Fresh-read Story/native-history owners and RD-03/RD-05/RD-08/RD-09/RD-10/RD-12. Run focused unittest, maintenance audit and full DEV discovery. Negative stale proof searches Story-as-canon/history/ACL, Commentator writes, T0 parallel timeline, transcript-as-history, native-only fallback and untriggered durable Dramaturg.

RD-13 closes its seven direct leaves and listed slices only. `R016`, `R018`, `R062`, `R087` parent closure remains package-level join work.