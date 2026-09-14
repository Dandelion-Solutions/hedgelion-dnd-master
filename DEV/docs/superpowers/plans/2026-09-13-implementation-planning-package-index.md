# HDM Implementation Planning Package — Index

Status: **AUTHOR POST-SIRR2 / POST-GRAPH REPAIR PUBLISHED — ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14

Global gate authority: `DEV/CURRENT_PROGRESS.md`. Production implementation: **NO**.

## Base routes

Current executable decomposition is RD-01 through RD-16. RD-08, RD-10 and RD-11 use their v2 plans. RD-15 is catalog runtime binding / gap evidence. RD-16 is world-family machine integration.

## Mandatory overlay precedence

1. `2026-09-13-implementation-planning-sirr-repair-amendments.md`
2. `2026-09-13-implementation-planning-author-self-review-repair-addendum.md`
3. `2026-09-13-implementation-planning-author-second-pass-repair-addendum.md`
4. `2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md`
5. `2026-09-14-implementation-planning-checkpoint-coherence-addendum.md`
6. `2026-09-14-implementation-planning-scene-routing-addendum.md`
7. `2026-09-14-implementation-planning-wp15-thread-catalog-addendum.md`
8. `2026-09-14-implementation-planning-wp17-shipped-consumer-addendum.md`
9. `2026-09-14-implementation-planning-temporal-completeness-routing-addendum.md`
10. `2026-09-14-implementation-planning-family-reconciliation-addendum.md`
11. `2026-09-14-implementation-planning-principal-player-routing-addendum.md`
12. `2026-09-14-implementation-planning-mechanical-event-identity-addendum.md`
13. `2026-09-14-implementation-planning-wp16-executable-closure-addendum.md`
14. `2026-09-14-implementation-planning-wp16-proof-ledger-post-graph-amendment.md`
15. `2026-09-14-implementation-planning-catalog-binding-shipped-consumer-addendum.md`
16. `2026-09-14-implementation-planning-post-graph-integration-addendum.md`

Later overlays supersede only exact conflicting execution detail.

## Current post-graph applicability

- RD-04 supplies world.player / no-world-faction and routing inputs; final shared machine writes route through RD-16.
- RD-05 owns MechanicalEvent composite identity; shared policy integration routes through RD-16.
- RD-08 supplies world.thread owner-local state and temporal completeness; shared final catalog/identity write routes through RD-16.
- RD-09 supplies LIVE/additive/live-birth/multi-LIVE semantics; shared policy write routes through RD-16.
- RD-15 owns exact same-context catalog binding and runtime.catalog_gap_report.
- RD-16 owns strict 17-family world state closure and the sole final shared catalog/identity integration checkpoint.

**Finding 16 repair — mandatory RD-16 rule:** native `world.player` has exactly one canonical campaign record key: the enclosing world-record `id`. The strict world-player state schema must reject a second persisted `player_id`. If a GAME projection exposes `player_id`, it is derived from the enclosing native record `id` and is not independently assigned. Create/deactivate/reactivate/routing/recovery proofs must preserve the same enclosing record `id`.

**Finding 17 repair — mandatory checkpoint rule:** RD-15 and RD-16 inherit overlay 5. A test group for a later task is introduced only when that task begins, and every test already present is GREEN before a publishable checkpoint. Full DEV discovery and maintenance audit are GREEN at each checkpoint.

## Final family census

World families: **17 exact** — actor, actor_group, asset, location, connection, zone, organization, contract, mission, scene, encounter, hazard, effect, lore_fact, knowledge, thread, player.

`world.faction` is not an independent v1 native family. Runtime families: **17 exact**. Counts are routing aids only; closure remains item-bound.

## Accounting / gate

```text
ACTIVE_READINESS: 133
DIRECT: 116
PURE_PROOF: 9
COMPOSITE_PARENTS: 8
TRIGGER_GATED: 12
NO_WORK: 79
R004: ABSENT
RD_UNITS: 16
MANDATORY_OVERLAYS: 16
AUTHOR_FINDINGS_1_TO_17: PLAN-REPAIRED / INDEPENDENTLY UNCONFIRMED
AUTHOR_POST_REPAIR_INVESTIGATION: ACTIVE
NEXT_INDEPENDENT_REVIEW: BLOCKED UNTIL FRESH ZERO-OPEN AUTHOR CLOSURE + EXACT-HEAD HOSTED VALIDATION
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
