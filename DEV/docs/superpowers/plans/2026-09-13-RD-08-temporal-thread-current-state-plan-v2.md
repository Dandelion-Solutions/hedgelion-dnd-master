# RD-08 — Temporal / Thread / Current-State — Executable Plan v2

Status: **AUTHOR REPAIR — SUPERSEDES THE EARLIER RD-08 PLAN FOR EXECUTION**

Goal: realize accepted temporal/process ownership, remove the obsolete campaign-wide chronology scalar, maintain bounded derived temporal enrollment, and join accepted occurrences to RD-05 execution without transferring authority.

Direct readiness: `R010,R039,R075,R076,R077`.
Composite slices: `R006.THREAD_VISIBILITY,R016.TEMPORAL,R018.TEMPORAL,R062.TEMPORAL_BINDING,R122.CHRONOLOGY`.
Owners: Step-5.3, Step-5.9, WP-15, WP-11/12; RD-05 execution; RD-07 recovery.

## Exact impact

- `NEW_CREATE GAME/TOOLS/temporal.py`
- `EXISTING_REPLACE GAME/SCHEMA/current_state.schema.yaml`
- `EXISTING_REPLACE GAME/SCHEMA/thread.schema.yaml`
- `NEW_CREATE DEV/SCHEMAS/world-thread-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/temporal-agenda-entry.schema.json`
- `EXISTING_MODIFY DEV/SCHEMAS/temporal-binding.schema.json` only when a focused RED assertion proves a mismatch
- exact catalog/admission/identifier projection only if required to admit `world.thread`; name the current file before editing and do not create another registry
- `NEW_CREATE DEV/TESTS/test_rd08_temporal.py`
- direct projection updates only: `GAME/SCHEMA/README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.

No campaign-wide chronology owner, autonomous timing authority, alternate world-process owner, technical-order chronology, duplicate accepted firing, or global cross-scope synchronization may be introduced.

Every checkpoint is `RED -> GREEN -> REFACTOR -> focused VERIFY -> commit`. No RED-only publication checkpoint.

## Checkpoint 1 — CURRENT / R010

Test class: `CurrentStateChronologyTests`.

RED cases:
- shipped CURRENT still contains the obsolete chronology scalar;
- technical ordering values are rejected as fictional chronology authority;
- independent scenes/processes may remain unordered;
- CURRENT is a compact routing/current-summary projection only.

GREEN: replace `current_state.schema.yaml`; remove the obsolete scalar without adding a substitute; retain only accepted routing/current summaries.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.CurrentStateChronologyTests -v
```

## Checkpoint 2 — world.thread / R075

Test class: `WorldThreadContractTests`.

GREEN targets: replace `thread.schema.yaml`; add `world-thread-state.schema.json`.

Prove:
- `world.thread` is admitted only for a durable generic process that has no more specific native owner;
- lifecycle/stage/progress are not chronology;
- deadline/temporal condition uses typed owner-local TemporalBinding;
- prospective metadata does not become established consequence;
- references do not copy another owner's state;
- legacy thread visibility fields are removed from epistemic authority and RD-02 owners remain authoritative.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.WorldThreadContractTests -v
```

## Checkpoint 3 — TemporalBinding + derived Agenda / R076,R077

Test class: `TemporalBindingAgendaTests`.

Interfaces in `GAME/TOOLS/temporal.py`:
```text
evaluate_temporal_binding(owner_state, binding, chronology_evidence) -> NOT_DUE | DUE | INDETERMINATE
derive_temporal_dependency_keys(owner_state, binding) -> DependencyKeys
materialize_due_occurrence(owner_state, occurrence_id, execution_evidence) -> OccurrenceResult
rebuild_temporal_agenda(native_owners) -> AgendaEntries
```

Add `temporal-agenda-entry.schema.json`. Agenda stores only owner reference, occurrence discriminator, binding discriminator, dependency keys and bounded routing metadata.

Prove stable occurrence identity, complete bounded dependency enrollment, rebuildability, continued enrollment of unresolved dependencies where later evidence can decide them, and that missing derived enrollment is a routing defect rather than semantic absence.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalBindingAgendaTests -v
```

## Checkpoint 4 — execution + recovery join / R039

Test class: `TemporalExecutionRecoveryTests`.

Prove one current occurrence generation establishes at most one accepted execution identity; stale contenders cannot establish a second consequence; rebuilding derived enrollment does not recreate already accepted work; RD-07 recovery resumes accepted execution through RD-05 using the same accepted identity.

RD-08 owns occurrence closure/claim only. Command payload, fixed RNG, receipts and execution lifecycle stay RD-05-owned.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalExecutionRecoveryTests -v
```

## Checkpoint 5 — R122.CHRONOLOGY

Test class: `ChronologyBridgeTests`.

A cross-scope chronology relation is produced only for a concrete positive material dependency. It carries the minimum owner/evidence-anchored relative-order, metric or boundary evidence required by that dependency. It cannot create a campaign-wide frontier or synchronize unrelated scopes. Commit/ref IDs, host time and arrival order cannot manufacture the relation.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.ChronologyBridgeTests -v
```

## Final verification and completion

```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact classifies the replaced CURRENT/thread contracts plus new world-thread/Agenda and any proven TemporalBinding/catalog projection change. No historical migration is activated.

Before each checkpoint, fresh-read its exact owners and touched current files. Mechanical path movement may be adapted and recorded; semantic owner/decomposition drift returns to planning authority.

RD-08 completes only its five direct leaves and named composite slices. Composite parents remain package-level joins with package proof and parent Version Impact reconciliation.