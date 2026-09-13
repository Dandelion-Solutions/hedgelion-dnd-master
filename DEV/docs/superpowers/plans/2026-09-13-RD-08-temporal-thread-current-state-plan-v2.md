# RD-08 — Temporal / Thread / Current-State — Executable Plan v2

Status: **AUTHOR REPAIR — SUPERSEDES THE EARLIER RD-08 PLAN FOR EXECUTION**

Goal: realize accepted temporal/process ownership, remove obsolete campaign-wide and scene-singleton chronology frontiers, maintain bounded derived temporal enrollment, produce typed sparse chronology evidence, and join accepted occurrences to RD-05 execution without transferring authority.

Direct readiness: `R010,R039,R075,R076,R077`.
Composite slices: `R006.THREAD_VISIBILITY,R016.TEMPORAL,R018.TEMPORAL,R062.TEMPORAL_BINDING,R122.CHRONOLOGY`.
Owners: Step-5.3, Step-5.9, WP-15, WP-11/12; RD-05 execution/Procedure/Continuation alignment; RD-07 recovery; RD-02 information owners; RD-13 native SemanticEvent/history realization.

## Exact impact

- `NEW_CREATE GAME/TOOLS/temporal.py`
- `EXISTING_REPLACE GAME/SCHEMA/current_state.schema.yaml`
- `EXISTING_REPLACE GAME/SCHEMA/thread.schema.yaml`
- `EXISTING_MODIFY GAME/SCHEMA/scene.schema.yaml`
- `NEW_CREATE DEV/SCHEMAS/world-thread-state.schema.json`
- `NEW_CREATE DEV/SCHEMAS/temporal-agenda-entry.schema.json`
- `NEW_CREATE DEV/SCHEMAS/chronology-relation-evidence.schema.json` as an embedded/value contract only, never a new durable record family
- `EXISTING_MODIFY DEV/SCHEMAS/temporal-binding.schema.json` only when a focused RED assertion proves a mismatch
- `EXISTING_MODIFY GAME/CORE/CHRONOLOGY.md` for Step-5.9/WP-15 frontier/provider wording
- `EXISTING_MODIFY GAME/CORE/PROCESSES.md` for correctness-dependency simulation budget and information/visibility wording
- `INSPECT_ONLY GAME/SCHEMA/event.schema.yaml` in RD-08; RD-13 owns its native-history replacement and consumes RD-08 typed chronology evidence
- `INSPECT_ONLY DEV/SCHEMAS/runtime-procedure-state.schema.json` and `runtime-continuation-state.schema.json`; RD-05 owns their WP-15 §13.12–13 repair
- exact catalog/admission/identifier projection only if required to admit `world.thread`; name the current file before editing and do not create another registry
- `NEW_CREATE DEV/TESTS/test_rd08_temporal.py`
- direct projection updates only: `GAME/SCHEMA/README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py`.

No campaign-wide chronology owner, autonomous timing authority, alternate world-process owner, technical-order chronology, duplicate accepted firing, generic chronology record family, or global cross-scope synchronization may be introduced.

Every checkpoint is `RED -> GREEN -> REFACTOR -> focused VERIFY -> commit`. No RED-only publication checkpoint.

## Checkpoint 1 — CURRENT / R010 / WP-15 §13.9

Test class: `CurrentStateChronologyTests`.

RED cases:
- shipped CURRENT still contains the obsolete chronology scalar;
- technical ordering values are rejected as fictional chronology authority;
- independent scenes/processes may remain unordered;
- CURRENT is a compact routing/current-summary projection only.

GREEN: replace `current_state.schema.yaml`; remove `world_time.frontier` and any equivalent generic global chronology scalar without adding a substitute; retain only accepted routing/current summaries.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.CurrentStateChronologyTests -v
```

Coherent checkpoint: CURRENT schema + focused test + exact audit/README projection, all green.

## Checkpoint 2 — world.thread / R075

Test class: `WorldThreadContractTests`.

GREEN targets: replace `thread.schema.yaml`; add `world-thread-state.schema.json`.

Prove:
- `world.thread` is admitted only for a durable generic process that has no more specific native owner;
- lifecycle/stage/progress are not chronology;
- deadline/temporal condition uses typed owner-local TemporalBinding;
- prospective metadata does not become established consequence;
- references do not copy another owner's state;
- legacy thread visibility/public/known-by fields are removed or demoted from epistemic authority; current knowledge/disclosure stays with RD-02 owners;
- `THREAD_INDEX`/current-summary presence may nominate discovery but cannot prove temporal-root absence.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.WorldThreadContractTests -v
```

Coherent checkpoint: thread schema + world-thread machine contract + exact catalog/admission projection if required + focused tests/audit, all green.

## Checkpoint 3 — TemporalBinding + derived Agenda / R076

Test class: `TemporalBindingAgendaTests`.

Interfaces in `GAME/TOOLS/temporal.py`:
```text
evaluate_temporal_binding(owner_state, binding, chronology_evidence) -> NOT_DUE | DUE | INDETERMINATE
derive_temporal_dependency_keys(owner_state, binding) -> DependencyKeys
materialize_due_occurrence(owner_state, occurrence_id, execution_evidence) -> OccurrenceResult
rebuild_temporal_agenda(native_owners) -> AgendaEntries
```

Add `temporal-agenda-entry.schema.json`. Agenda stores only owner reference, occurrence discriminator, binding discriminator, dependency keys and bounded routing metadata.

Prove stable occurrence identity, complete bounded dependency enrollment, rebuildability, continued enrollment of unresolved dependencies where later evidence can decide them, and that missing derived enrollment is a routing defect rather than semantic absence. Relevance/working-set/Dramaturg heuristics may suppress speculative simulation but never an invalidation/recheck required by an already-declared correctness dependency.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalBindingAgendaTests -v
```

Coherent checkpoint: TemporalBinding/Agenda runtime + schema + tests, all green.

## Checkpoint 4 — execution + recovery join / R039

Test class: `TemporalExecutionRecoveryTests`.

Prove one current occurrence generation establishes at most one accepted execution identity; stale contenders cannot establish a second consequence; rebuilding derived enrollment does not recreate already accepted work; RD-07 recovery resumes accepted execution through RD-05 using the same accepted identity; RD-05 Procedure/Continuation state is consumed without copying procedure-local timing/order/budget or inventing a generic future RNG schedule.

RD-08 owns occurrence closure/claim only. Command payload, fixed RNG, receipts, Procedure state and execution lifecycle stay RD-05-owned.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalExecutionRecoveryTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProcedureTemporalStateTests DEV.TESTS.test_rd05_runtime_execution.ContinuationTemporalStateTests -v
```

Coherent checkpoint: occurrence/execution/recovery integration green against the already-green RD-05/RD-07 contracts.

## Checkpoint 5 — typed sparse chronology / R122.CHRONOLOGY / WP-15 §13.11

Test class: `ChronologyBridgeTests`.

Create `DEV/SCHEMAS/chronology-relation-evidence.schema.json` as a reusable embedded value contract, not a new `runtime.*`/`world.*` family.

Minimum value shape:
```text
ChronologyRelationEvidence {
  relation_key
  relation_type: PRECEDES | SAME_COORDINATE | ELAPSED
  left_anchor_ref
  right_anchor_ref
  order_domain_id?       # required for PRECEDES
  metric_context_id?     # required for SAME_COORDINATE / ELAPSED
  lower_bound?           # ELAPSED; exact when lower == upper
  upper_bound?           # ELAPSED
  established_by_ref
  supporting_refs[]
}
```

Rules:
- causal ancestry remains distinct SemanticEvent/native-owner evidence and is not folded into `PRECEDES`;
- `PRECEDES` is comparable/transitive only inside its declared order domain;
- same coordinate requires positive evidence and cannot be inferred from missing order;
- elapsed ranges preserve uncertainty and cannot be scalarized by convenience;
- a cross-scope relation is produced only for a concrete positive material dependency and carries the minimum owner/evidence-anchored relation needed by that dependency;
- commit/ref IDs, host time, arrival order, event-ID order and list/SQL order cannot manufacture chronology;
- when an event-local legacy `after_event_ids` relation would be ambiguous across domains, RD-13 native-history realization consumes this typed evidence instead of preserving an untyped universal precedence edge;
- late-established relation evidence is attached/referenced by its accepted establishing native owner/event; this value contract is not a second mutable chronology store.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.ChronologyBridgeTests -v
```

Coherent checkpoint: typed relation value contract + temporal producer/validator + focused tests/project-map/audit, all green.

## Checkpoint 6 — scene + CORE reconciliation / WP-15 §13.10,15,16 and local part of R077

Test class: `TemporalMachineAlignmentTests`.

**Files**
- Modify `GAME/SCHEMA/scene.schema.yaml`.
- Modify `GAME/CORE/CHRONOLOGY.md`.
- Modify `GAME/CORE/PROCESSES.md`.
- Modify `DEV/TESTS/test_rd08_temporal.py`.
- Modify `DEV/TOOLS/audit_engine.py` only for exact stale-contract assertions.

RED currentness evidence includes:
- `scene.schema.yaml` still exposes `chronology_frontier_event_id` as a singleton scene frontier;
- `GAME/CORE/CHRONOLOGY.md` still describes `CURRENT.world_time.frontier` as a globally reconciled chronology frontier and recommends scene frontiers;
- `GAME/CORE/PROCESSES.md` still allows relevance/“affect the current working set soon” wording to look like a correctness gate and lists process visibility as process-owned state.

GREEN alignment:
- remove/demote scene singleton frontier semantics; a scene may retain owner-defined local qualitative/typed position evidence only without becoming chronology authority;
- replace global/scene-frontier prose with smallest owner-anchored sparse relation/provider evidence and concrete material-bridge reconciliation;
- distinguish speculative off-screen simulation budget from correctness dependency invalidation: an enrolled affected temporal dependency remains re-evaluable even when narratively irrelevant/unloaded;
- remove process-owned epistemic visibility wording; thread/process facts may reference current information owners but do not own `known_by`/public disclosure state;
- discovery indexes/current summaries remain non-authoritative and non-exhaustive for absence proof;
- no full-history/global-thread scan is introduced as fallback.

Focused verify:
```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalMachineAlignmentTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
```

Coherent checkpoint: scene + CHRONOLOGY/PROCESSES CORE alignment + tests/audit, all green.

## R077 cross-owner completion join — do not pre-claim

R077 is assigned to RD-08 but its WP-15 §13.9–17 obligation set crosses existing owners. RD-08 may not close R077 until package proof has all of these green:

```text
§13.9   RD-08 CurrentStateChronologyTests
§13.10  RD-08 TemporalMachineAlignmentTests / scene schema
§13.11  RD-08 ChronologyBridgeTests + RD-13 NativeHistoryAuthorityTests consumer join
§13.12  RD-05 ProcedureTemporalStateTests
§13.13  RD-05 ContinuationTemporalStateTests
§13.14  RD-02 information-owner tests + RD-09 live normalization + RD-13 NativeHistoryAuthorityTests
§13.15  RD-04 route/index negatives + RD-08 WorldThreadContractTests/TemporalMachineAlignmentTests
§13.16  RD-08 TemporalMachineAlignmentTests / CHRONOLOGY.md + PROCESSES.md
§13.17  package Wp15TemporalProofTests plus focused failure-injection scenarios
```

The empirical WP-15 fanout/partition branch stays dormant until WP-24 measured evidence activates it. No partitioning optimization is manufactured by R077 implementation.

## Final verification and completion

```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.ProcedureTemporalStateTests DEV.TESTS.test_rd05_runtime_execution.ContinuationTemporalStateTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected PASS for RD-08-owned work. R077 itself closes only at the named package join after RD-13 history/information realization is green.

Version Impact classifies the replaced CURRENT/thread contracts, scene/CORE compatibility changes, new world-thread/Agenda/chronology-value contracts and any proven TemporalBinding/catalog projection change. R077 receives one package-level parent/leaf Version Impact reconciliation after all cross-owner members are known; no historical migration is activated here.

Before each checkpoint, fresh-read its exact owners and touched current files. Mechanical path movement may be adapted and recorded; semantic owner/decomposition drift returns to planning authority.

Stale proof: no generic global/scene chronology frontier, technical-order chronology, process-owned knowledge/disclosure, relevance-as-correctness gate, broad-scan fallback, duplicate accepted firing or generic chronology store.

RD-08 completes R010/R039/R075/R076 and named composite slices after its own checkpoints. R077 remains join-pending until the explicit §13.9–17 package proof succeeds; composite parents remain package-level joins with package proof and parent Version Impact reconciliation.