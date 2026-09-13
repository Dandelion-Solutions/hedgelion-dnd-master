# RD-11 — Bounded Context Runtime — Executable Plan v2

Status: **AUTHOR REPAIR — SUPERSEDES EARLIER RD-11 FOR EXECUTION**

Goal: realize bounded discovery, currentness, eligibility, required-packet closure, representation, allocation and diagnostic trace as an ephemeral Context Runtime projection.

Direct readiness: `R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145`.
Composite slices: `R087.RETROSPECTIVE,R122.CONTEXT`.
Owners: R2.3, WP-09, WP-08, R2.4, Step-4 knowledge/disclosure/context laws. RD-02 owns knowledge/disclosure; RD-09 current principal/currentness; RD-10 role containment; RD-12 controlled-actor/collaboration scope.

## Exact impact

- `NEW_CREATE GAME/TOOLS/context_runtime.py`
- `NEW_CREATE GAME/TOOLS/context_budget.py`
- `NEW_CREATE DEV/SCHEMAS/context-need-profile.schema.json`
- `NEW_CREATE DEV/SCHEMAS/context-trace.schema.json`
- `INSPECT_ONLY GAME/SCHEMA/current_state.schema.yaml`, `scene.schema.yaml`, `index.schema.yaml`
- `NEW_CREATE DEV/TESTS/test_rd11_context_runtime.py`
- direct `DEV/PROJECT_MAP.md` / `DEV/TOOLS/audit_engine.py` projections only.

Native owner schemas/indexes remain read/routing inputs. Context Runtime introduces no durable gameplay owner and no alternate knowledge/disclosure authority.

Every checkpoint is `RED -> GREEN -> REFACTOR -> focused VERIFY -> commit`; do not publish a failing checkpoint.

## Checkpoint 1 — request/profile and bounded discovery

Class: `ContextDiscoveryTests`.

Interfaces:
```text
assemble_context(request, profile, budget) -> AssemblyResult
discover_candidates(request, profile) -> CandidateFrontier
resolve_candidate_basis(candidate, request) -> RoutedCandidate
```

Prove request identity includes role/purpose/subject/recipient/current scope; only registered profile and relation families are usable; discovery is typed and bounded across admitted channels; candidate discovery does not require full-body loading; bounded frontier is not closed-world proof.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.ContextDiscoveryTests -v
```

## Checkpoint 2 — currentness and eligibility

Class: `ContextEligibilityTests`.

Pipeline:
```text
discovered ref -> current routed owner/source -> minimum currentness/eligibility reads -> eligible representation
```

Prove cached/easy/first representation cannot outrank current routed owner; routing checks are not automatically role evidence; prompt presence, mention, ranking score, scene presence and cache presence do not establish eligibility. Consume RD-09 evidence where applicable without owning it.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.ContextEligibilityTests -v
```

## Checkpoint 3 — required packet closure

Class: `RequiredPacketClosureTests`.

Implement finite typed closure over registered required dependencies. Required closure reaches legal minimum representations before optional allocation. Prove cycle handling, discovery of registered mandatory dependencies, invalid relation rejection and no broad fallback scan.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.RequiredPacketClosureTests -v
```

## Checkpoint 4 — representation floors and allocation

Class: `ContextAllocationTests`.

Interface in `context_budget.py`:
```text
estimate_size(representation) -> ConservativeSize
allocate(required_packet, supporting, optional, budget_envelope) -> AllocationResult
```

Representation classes may be `EXACT | FULL_STRUCTURED | COMPACT_STRUCTURED | SUMMARY | REFERENCE_ONLY`; minimum floor belongs to source/consumer contract. Allocation order: downstream reservation -> complete required packet -> supporting evidence -> optional material. Required evidence is never ranked against optional evidence or reduced below its legal floor.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.ContextAllocationTests -v
```

## Checkpoint 5 — optional ranking / R139

Class: `OptionalRankingTests`.

Ranking operates only on already-current and eligible supporting/optional candidates. It may order material but cannot establish truth, knowledge, disclosure, authority or requiredness. `R139` includes explicit witnessed-vs-mentioned cases. Deduplication requires typed same-source/slice/proposition/owner or explicit projection-coverage evidence.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.OptionalRankingTests -v
```

## Checkpoint 6 — retrospective / R097 + R087.RETROSPECTIVE

Class: `RetrospectiveContextTests`.

Escalation:
```text
coarse eligible Story/entity/thread/segment hint
-> bounded history candidates
-> exact/native evidence when required
```

Each broader step names the unresolved registered question, eligible source domain, finite bound and stop condition. `R097` includes the ordinary-Master registered retrospective consumer, not retrieval primitives alone. `R087.RETROSPECTIVE` remains only this slice.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.RetrospectiveContextTests -v
```

## Checkpoint 7 — terminal result, trace and dry-run

Class: `ContextResultTraceTests`.

Result is exactly `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE`; degraded still satisfies all required semantics. Dry-run uses the same path without mutation. ContextTrace records request/profile, candidates/channels, currentness, eligibility, representation, required/optional classification, ranking inputs, decisions and result. Trace remains diagnostic/test evidence only.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.ContextResultTraceTests -v
```

## Checkpoint 8 — R124 + R122.CONTEXT joins

Class: `ScopedContextJoinTests`.

`R124` requires:
```text
RD-02 knowledge/disclosure
+ RD-09 principal/currentness where applicable
+ RD-10 role/recipient containment
+ RD-12 controlled-actor/multiplayer scope
-> RD-11 scoped context projection
```
Include recipient-isolation and controlled-actor-isolation positive/negative cases.

`R122.CONTEXT` admits cross-scope material only after a concrete positive material dependency provides lawful chronology/currentness/collaboration evidence from RD-08/RD-09/RD-12. Context Runtime does not create that dependency or synchronize unrelated scopes.

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime.ScopedContextJoinTests -v
```

## Final verification

```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact covers only the ephemeral validation/profile contracts and direct projections. Before every checkpoint fresh-read its exact owners and touched current files; before R124/R122 joins also fresh-read current RD-02/RD-08/RD-09/RD-10/RD-12 plans. Semantic owner drift returns to planning.

RD-11 closes only its direct leaves and named slices. Parent/composite closure remains package-level.