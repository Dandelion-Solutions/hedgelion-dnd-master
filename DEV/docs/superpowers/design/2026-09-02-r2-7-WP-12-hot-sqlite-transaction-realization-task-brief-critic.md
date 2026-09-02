# R2.7 WP-12 - Step-1 Whole-Project Task-Brief Critic

Status: **COMPLETE - MECHANICALLY RESOLVABLE FINDINGS REPAIRED**

## Method

Starting from `DEV/PROJECT_MAP.md`, this critic followed the WP-12 route through
the R2.7 scope owner, current-progress gate, Step-3 execution boundary, Step-5
durability/publication/recovery/live owners, R2.3/WP-09 context boundary,
WP-10 logical allocation, WP-11 topology law, GAME persistence/live consumers,
GAME schemas, DEV machine contracts and scenario/test consumers. The exact
source set and inspection status are in the companion Source Manifest.

## Findings

| ID | Whole-project attack and evidence route | Result and repair | Severity | Resolved |
|---|---|---|---|---|
| C01 | WP-11 canonical spec and architecture index still said its Senior audit was pending, while `CURRENT_PROGRESS.md` and the R2.7 task-local cursor say WP-11 is closed by Senior review. | Repaired the two current routing/status carriers to `CLOSED / SENIOR REVIEW PASS`. The historical WP-11 Step-1 handoff remains provenance. | SIGNIFICANT | YES |
| C02 | The task-local cursor authorizes WP-12 Step 1 but its final handoff still directs workers to await WP-11 review and not start WP-12. | Repaired the stale handoff to point to the current WP-12 Step-1 package and its Senior stop. | SIGNIFICANT | YES |
| C03 | `LIVE_SCENE_CASES.md` L03 fetched `CAMPAIGN/LIVE/LIVE_STATE.yaml`, conflicting with `LIVE_SCENE.md` and `live_scene.schema.yaml`, which require `LIVE/LIVE_STATE.yaml` at the live-branch root. | Repaired the test-case path. | SIGNIFICANT | YES |
| C04 | Existing GAME durability prose/tests treat a one-hour `durable_frontier_time` as current law, but Step 5.5 rejects a campaign-global timer/frontier and marks it implementation debt. | The brief now classifies this as consumer/debt evidence and requires Step 2 to preserve scope-qualified exposure semantics. No GAME/test rewrite is valid in this documentation-only Step-1 package; the owner-conforming realization remains downstream. | SIGNIFICANT | YES - FRAMING REPAIR |
| C05 | A HOT/SQLite investigation could accidentally use a route, index, cache, checkpoint, live envelope or pending-work helper as a second authority. Step 5.2/5.7/5.8/WP-11 explicitly prohibit those substitutions. | The brief requires owner-state versus derived disposition, exact hydration source, loss/rebuild behavior and native materialization target for every included structure, with explicit negative outcomes. | BLOCKING | YES - FRAMING REPAIR |
| C06 | A transaction design could overreach into external dialogue, generic journaling, cross-ref atomicity, timers or implementation changes. Step 3 and Steps 5.5-5.8 allocate those boundaries elsewhere. | The brief states the external-boundary prohibition and scope exclusions; no unresolved product or architecture trade-off remains. | BLOCKING | YES - FRAMING REPAIR |

## Critic conclusion

The repaired Task Brief does not treat SQLite, the legacy timer model, a
checkpoint, an index, a global transaction or a current GAME scaffold as an
unsettled architecture choice. It has a complete enough dependency route to
begin Step 2 only after mandatory Senior GO. No human decision is requested at
Step 1.
