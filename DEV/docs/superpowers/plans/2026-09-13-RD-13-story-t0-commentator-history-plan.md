# RD-13 — Story / T0 / Commentator / History — Executable Implementation Plan

Goal: realize the Story-specific durable projection, reconstructible T0 baseline and read-only Commentator path while preserving SemanticEvent/history, temporal and world owners as the only authorities for their domains.

Direct readiness: `R022,R051,R084,R085,R099,R102,R131`.
Owners: Story architecture decisions/appendix, accepted history/continuity architecture, Multiplayer Model. RD-03 owns Actor continuity, RD-08 temporal/current-state, RD-09 currentness, RD-12 collaboration projection.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/story.py`
- `NEW_CREATE GAME/TOOLS/commentator.py`
- `NEW_CREATE DEV/SCHEMAS/story-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/t0-baseline.schema.json`
- `NEW_CREATE DEV/SCHEMAS/commentator-view.schema.json`
- accepted SemanticEvent/history owner schemas/catalogs — INSPECT_ONLY except explicit consumer wiring
- `NEW_CREATE DEV/TESTS/test_rd13_story_t0_commentator.py`
- direct project-map/audit projections only.

Forbidden: Story summary as truth/currentness/history authority; T0 as parallel timeline; Commentator mutation; transcript as canonical event history; multiplayer copy as second Story/history canon; summary text silently promoting external/derived material.

## Task 1 — RED: Story authority boundaries

Create tests proving Story state contains only Story-specific durable state and references native world/history/temporal evidence rather than copying their authority. A summary cannot override a current native owner or accepted SemanticEvent.

Expected RED: no v1 Story runtime contract exists.

## Task 2 — GREEN: Story-state contract and transition boundary

Implement `story-state.schema.json` and `GAME/TOOLS/story.py` interfaces equivalent to:
```text
project_story_state(native_evidence, prior_story) -> StoryProjection
advance_story_state(accepted_event, prior_story) -> StoryTransition
```

Transitions consume already accepted authoritative evidence. Story may maintain narrative phase/goals/hooks/threads only where canonical decisions assign that ownership. It does not accept free-form truth mutations.

Commit boundary: Story schema + transition/projection + tests.

## Task 3 — non-authoritative summaries and reconstruction

Add deterministic summary/projection behavior whose outputs carry source/frontier identity. Summary is replaceable/rebuildable compression. Tests prove stale summary cannot defeat newer native evidence and summary omission is not semantic absence.

## Task 4 — T0 baseline

Implement `t0-baseline.schema.json` and a deterministic T0 construction path. T0 records the accepted initial reconstruction basis needed by downstream Story/history consumers. It is not a mutable second history and cannot advance independently of accepted owner evidence.

Tests cover reproducibility, invalid mixed-frontier input and rejection of T0-as-current-world authority.

## Task 5 — Commentator read-only boundary

Implement `GAME/TOOLS/commentator.py` and `commentator-view.schema.json`:
```text
reconstruct_commentary(request, eligible_story, eligible_history, t0) -> CommentatorView
```

Commentator may explain/reconstruct using eligible evidence; it cannot emit authoritative gameplay mutations, SemanticEvents, knowledge grants or currentness changes. Output identifies its evidence basis and remains disposable.

## Task 6 — history / transcript / SemanticEvent separation

Integration tests enforce:
- transcript is communication evidence, not canonical SemanticEvent history;
- accepted SemanticEvent/history remains the causal/history authority;
- Story may reference history but not rewrite ancestry/provenance;
- T0 + later history reconstructs the intended baseline/continuation without a parallel event stream.

## Task 7 — multiplayer and source-trust negatives

Consume RD-12 recipient projection only after disclosure/eligibility. A participant-specific Story/Commentator view cannot become a second canon. Derived/external narrative material remains non-canonical until an owner-defined promotion path accepts it.

Tests include divergent lawful recipient views over one canon and rejection of summary-derived truth promotion.

## Task 8 — Version Impact / persistence / checkpoint

Classify `story-state.schema.json` as a durable v1 contract and explicitly route schema version, checkpoint serialization and migration consequences through their owners. T0 is reconstructible evidence with owner-defined retention; CommentatorView is not durable authority.

No compatibility layer preserves legacy Story semantics merely because old GAME text/schema existed.

## Task 9 — verification and currentness fence

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd13_story_t0_commentator -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Negative stale proof searches for Story-as-world/history/currentness authority, Commentator writes, T0 parallel timeline, transcript-as-history and recipient projection promoted to canon.

Before implementation/closure fresh-read Story decisions/appendix, history/continuity owners, RD-03/RD-08/RD-09/RD-12 and exact SemanticEvent/history machine owners. Owner drift stops execution.

RD-13 closes only its seven direct leaves; proof/composite/package closure remains PB-07 work.