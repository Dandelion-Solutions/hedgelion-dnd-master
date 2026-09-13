# RD-08 - Temporal / Thread / Current-State Ownership - Executable Implementation Plan

Goal: realize narrow native temporal/process ownership, remove the legacy campaign-global chronology frontier, rebuild bounded temporal dependency enrollment, and hand accepted occurrences to Step-3 execution without creating another authority.

Direct readiness: `R010,R039,R075,R076,R077`.
Composite slices: `R006.THREAD_VISIBILITY,R016.TEMPORAL,R018.TEMPORAL,R062.TEMPORAL_BINDING,R122.CHRONOLOGY`.
Canonical owners: Step-5.3, Step-5.9, WP-15, WP-11/12, RD-05 accepted execution, RD-07 current-native recovery.
Out of scope: global timeline, scheduler/job queue, wall-clock fictional authority, LIVE authority, migration/release execution.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/temporal.py`
- `EXISTING_REPLACE GAME/SCHEMA/thread.schema.yaml`
- `EXISTING_REPLACE GAME/SCHEMA/current_state.schema.yaml`
- `NEW_CREATE DEV/SCHEMAS/world-thread-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/temporal-agenda-entry.schema.json`
- `EXISTING_MODIFY DEV/SCHEMAS/temporal-binding.schema.json` only when RED proves v1 alignment debt
- catalog/admission/identifier projections only as required to admit exact `world.thread`
- `NEW_CREATE DEV/TESTS/test_rd08_temporal.py`
- direct projection updates only: `GAME/SCHEMA/README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`

Forbidden outcomes: campaign-global clock/frontier; host/Git/message-arrival fictional time; Agenda-owned DUE state; scheduler authority; thread mirrors of mission/contract/effect/resource/procedure owners; discovery-index absence as semantic absence; relevance heuristics suppressing declared correctness dependencies; duplicate accepted firing for one occurrence generation; global synchronization for `R122.CHRONOLOGY`.

## Task 1 - RED: current-state chronology authority

Create `DEV/TESTS/test_rd08_temporal.py` proving:
1. `STATE/CURRENT` cannot require or expose `world_time.frontier` as chronology/currentness authority;
2. Git/ref order, event IDs, host time and message arrival cannot establish fictional chronology;
3. independent scenes/processes may remain unordered without a material dependency;
4. CURRENT remains compact routing/current-summary only.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal -v
```
Expected RED because the shipped current-state schema still requires the legacy frontier.

## Task 2 - GREEN: replace current-state contract

Replace `GAME/SCHEMA/current_state.schema.yaml`:
- remove `world_time.frontier` and any replacement global chronology scalar/object;
- retain only accepted positive routing/current summaries;
- active scene/thread summaries are non-exhaustive discovery aids, never absence/completeness authority;
- chronology remains owner/domain typed.

Commit boundary: current-state replacement + focused tests/projection update.

## Task 3 - Narrow `world.thread`

Replace `GAME/SCHEMA/thread.schema.yaml` and add `DEV/SCHEMAS/world-thread-state.schema.json`.

Required laws:
- thread exists only for an independently identified generic world process with durable identity/lifecycle and no more specific admitted owner;
- broad lifecycle status is distinct from temporal occurrence state;
- stage/progress are process state, not chronology;
- deadline uses typed owner-local TemporalBinding semantics;
- `next_development` is prospective metadata only;
- resource/event references do not transfer ownership;
- legacy `visibility.known_by_pc_ids/public` cannot become epistemic authority; RD-02 knowledge/disclosure remains authoritative.

Tests reject thread copies of mission/contract/effect/resource/procedure state and status-only DUE inference.

## Task 4 - TemporalBinding evaluation and dependency enrollment

Implement in `GAME/TOOLS/temporal.py` and reconcile existing `DEV/SCHEMAS/temporal-binding.schema.json` only where RED proves debt.

Interfaces:
```text
evaluate_temporal_binding(owner_state, binding, chronology_evidence)
derive_temporal_dependency_keys(owner_state, binding)
materialize_due_occurrence(owner_state, occurrence_id, execution_evidence)
```

Rules:
- evaluation result is `NOT_DUE | DUE | INDETERMINATE`;
- provider movement is owner-defined and cannot invent/tighten evidence;
- occurrence identity is distinct from timing evidence;
- changing evidence alone does not allocate a replacement occurrence;
- no generic durable `due=true` or scheduler timestamp.

## Task 5 - Derived Agenda contract

Add `DEV/SCHEMAS/temporal-agenda-entry.schema.json` and implement derived enrollment in `GAME/TOOLS/temporal.py`.

Agenda entry contains only native owner reference, occurrence discriminator, binding reference/discriminator, typed dependency keys and bounded routing metadata.

GREEN requirements:
- every independently-due armed occurrence has complete bounded dependency enrollment;
- Agenda order/priority has no fictional or rules precedence;
- INDETERMINATE remains enrolled when later evidence may decide it;
- owner/provider lifecycle changes update enrollment coherently;
- missing enrollment is a routing/recovery defect, not permission for a broad WORLD/LOG scan;
- `CURRENT.active_threads` and indexes cannot prove absence.

## Task 6 - Accepted occurrence -> RD-05 execution

One current occurrence generation may establish exactly one accepted execution identity. RD-08 closes or claims the owner occurrence and passes stable identity to RD-05; payload, RNG, receipt and execution lifecycle remain RD-05-owned.

Tests prove:
- retry/recovery cannot create a second accepted firing for the same occurrence generation;
- stale/rejected contenders cannot establish a duplicate consequence;
- rebuilt Agenda cannot rematerialize already accepted work.

This realizes `R039`, `R016.TEMPORAL` and `R018.TEMPORAL` without moving execution authority.

## Task 7 - Recovery join

RD-07 recovery selects and pins current native owners, hydrates required temporal/process evidence, then RD-08 reconstructs binding/dependency enrollment and derived Agenda. Already accepted firing resumes through RD-05 instead of being rematerialized.

Healthy recovery must not scan all threads/WORLD/LOG when exact typed routing exists.

## Task 8 - `R122.CHRONOLOGY` slice

Emit cross-scope chronology evidence only when a concrete positive material dependency makes relative order/metric/boundary evidence necessary.

The evidence must be typed, owner/evidence anchored and scoped to the actual dependency. It must not become a global frontier, synchronization barrier or convenience total order. Commit time, IDs and arrival order cannot manufacture chronology.

## Task 9 - Verification and Version Impact

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS.

Version Impact Gate classifies `current_state`, `thread`, world-thread and temporal-agenda contract generations and required catalog/admission/identifier projections. No historical migration execution is authorized.

Stale proof must find no active global chronology frontier/clock, scheduler/job authority, Agenda-as-owner semantics, thread copy of a specific native owner, visibility substituting for RD-02, duplicate firing path or global synchronization implementation for `R122.CHRONOLOGY`.

## Completion / currentness fence

Before worker execution, re-read exact owners and touched files at worker HEAD. Mechanical path movement may be adapted and recorded; semantic owner/decomposition drift stops execution and returns to planning authority.

RD-08 completion records only its direct leaves and listed composite slices. Composite parents remain incomplete until sibling slices, proof/root integration and Version Impact closure complete package-wide.
