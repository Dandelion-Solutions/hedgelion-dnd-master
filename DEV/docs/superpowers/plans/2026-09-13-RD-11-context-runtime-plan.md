# RD-11 — Bounded Context Runtime — Executable Implementation Plan

Goal: realize deterministic bounded discovery/currentness/eligibility/packet closure/representation/allocation/trace as an ephemeral Context Runtime projection, with no new memory or semantic authority.

Direct readiness: `R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145`.
Composite slices: `R087.RETROSPECTIVE,R122.CONTEXT`.
Canonical owners: R2.3, WP-09, WP-08, R2.4 consumer/fallback contract, Step-4 knowledge/disclosure/context laws. RD-02 owns knowledge/disclosure; RD-09 supplies principal/currentness; RD-10 supplies role/recipient containment; RD-12 later supplies controlled-actor/multiplayer scope for `R124` and collaboration bridge for `R122`.

## Impact Envelope

- `NEW_CREATE GAME/TOOLS/context_runtime.py`
- `NEW_CREATE GAME/TOOLS/context_budget.py`
- `NEW_CREATE DEV/SCHEMAS/context-need-profile.schema.json`
- `NEW_CREATE DEV/SCHEMAS/context-trace.schema.json`
- `INSPECT_ONLY GAME/SCHEMA/current_state.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/scene.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/index.schema.yaml`
- native owner schemas/indexes are read/routing inputs only; RD-11 has no blanket authority to edit them
- no durable GAME schema/root for RoleContextBundle, ContextTrace, profile, source basis or estimator state
- `NEW_CREATE DEV/TESTS/test_rd11_context_runtime.py`
- direct project-map/audit projection updates only.

Forbidden: generic memory DB, vector/graph authority, persistent context bundle/trace/profile/source basis, provider-specific fixed percentages, exact hidden-token dependency, full-world/full-history fallback, arbitrary graph walk, ranking-before-eligibility, optional eviction of required evidence, persistent fairness ledger, background retrieval worker, trace-as-prompt/authority, index/cache omission as semantic absence.

## Task 1 — RED: registered request/profile and bounded discovery

Create `DEV/TESTS/test_rd11_context_runtime.py` proving:
- a request identifies role/purpose/subject/recipient/current scope and uses a registered ContextNeedProfile;
- model text cannot invent a new profile, relation or private eligibility expansion;
- discovery is typed and bounded across admitted channels (current scope, scene, explicit refs, active dependency, LIVE current, index, history hint);
- full bodies are not required merely to discover candidate refs;
- bounded frontier never becomes global closed-world proof.

Expected RED: no shipped Context Runtime exists.

## Task 2 — GREEN: Context Runtime request/discovery pipeline

Implement `GAME/TOOLS/context_runtime.py` interfaces equivalent to:
```text
assemble_context(request, profile, budget) -> AssemblyResult
discover_candidates(request, profile) -> CandidateFrontier
resolve_candidate_basis(candidate, request) -> RoutedCandidate
```

Requiredness belongs to the registered consumer/profile, not a relevance score. Expansion follows only registered typed relations with finite depth/work/result limits and cycle suppression.

Commit boundary: registered request/profile + bounded discovery + tests.

## Task 3 — routed currentness and minimum eligibility reads

Before material semantic use:
1. resolve current routed native owner/source;
2. perform only the minimum internal reads required for currentness/eligibility;
3. admit eligible semantic material to the receiving role projection.

Rules:
- discovered-first/easiest/cached representation cannot outrank current routed owner;
- internal eligibility reads are not automatically role evidence;
- physical prompt presence, explicit mention, ranking score, scene presence or cache presence never grants eligibility;
- secret-bearing routing/trace remains internal unless independently eligible.

RD-09 currentness/principal evidence is consumed where applicable; Context Runtime never owns it. If an inspected native routing/schema surface contradicts these accepted laws, worker stops and returns to planning authority rather than expanding RD-11 write scope.

## Task 4 — bounded required packet closure

Implement typed finite closure over required owners/evidence. Loading one required owner may expose another registered mandatory dependency; complete all required closure at legal minimum representations before optional allocation.

No arbitrary ref/tag/prose graph traversal. If legal/current/eligible required closure cannot be completed, the result is not complete.

Tests cover cycles, hidden mandatory dependency discovery, invalid relation expansion and no broad fallback scan.

## Task 5 — representation floors and packet-first allocation

Implement one centralized `GAME/TOOLS/context_budget.py` interface equivalent to:
```text
estimate_size(representation) -> ConservativeSize
allocate(required_packet, supporting, optional, budget_envelope) -> AllocationResult
```

Logical representation classes may include `EXACT | FULL_STRUCTURED | COMPACT_STRUCTURED | SUMMARY | REFERENCE_ONLY`, with minimum floor owned by source/consumer contract.

Allocation order:
1. downstream instruction/output/safety reservation;
2. complete required packet at legal floors;
3. protected/high-value supporting evidence;
4. ranked optional/supporting material.

No fixed global percentages or exact remaining-token telemetry dependency. Required evidence is never ranked against optional evidence or silently summarized below legal floor.

## Task 6 — optional ranking, fairness and conservative deduplication

Ranking applies only to already legal supporting/optional candidates. Signals may include task relevance, scope participation, semantic/source class, meaningful recurrence/recency, diversity and deterministic fairness.

`R139` stays here: ranking consumes native epistemic/history evidence only after eligibility and currentness. It never establishes knowledge, disclosure, importance authority or requiredness.

Deduplication requires typed same-source/slice/proposition/owner or explicit projection-coverage evidence. Generic semantic similarity alone cannot collapse distinct facts; Story cannot displace a current owner because it discusses the same subject.

## Task 7 — historical retrieval and `R087.RETROSPECTIVE`

Historical escalation follows:
```text
coarse eligible Story/entity/thread/segment hint
-> bounded episodic/history candidates
-> exact/native evidence when required
```

Every broader step names the unresolved registered dependency/question, eligible source domain, finite bound and success/failure condition.

`R087.RETROSPECTIVE` is only the Context Runtime retrieval slice. It does not own save/T0/history creation; sibling slices and parent proof remain elsewhere. No whole-history scan as ordinary fallback.

## Task 8 — terminal assembly result, trace and dry-run

Result is exactly one of:
```text
ASSEMBLED
ASSEMBLED_DEGRADED
UNSATISFIABLE
```
`ASSEMBLED_DEGRADED` still satisfies all required semantics; only optional/supporting/preferred representation is reduced. `UNSATISFIABLE` is terminal for this attempt and hands control to RD-10 finite fallback.

Implement side-effect-free dry-run through the same path. ContextTrace records request/profile identity, candidates/channels/expansions, currentness, eligibility, representation, required/optional class, ranking inputs, include/exclude/downgrade reason and result.

Trace is restricted diagnostic/test evidence only: never role evidence, prompt content, gameplay state or player-visible output.

## Task 9 — `R124` scoped recipient/controlled-actor projection join

RD-11 realizes projection composition only after prerequisites are available:
```text
RD-02 native knowledge/disclosure
+ RD-10 role/recipient containment
+ RD-12 controlled-actor/multiplayer scope
+ RD-09 principal/currentness where applicable
-> RD-11 R124 scoped context projection
```

One native canon yields recipient/controlled-actor scoped projections; no second canon or disclosure owner is introduced. RD-11 plan/test scaffolding may be authored now, but package-level completion of `R124` remains gated on RD-12.

Tests must include recipient isolation and controlled-actor isolation positives/negatives.

## Task 10 — `R122.CONTEXT` cross-scope bridge slice

RD-11 may include cross-scope material only when a concrete positive material dependency has already supplied lawful chronology/currentness/collaboration-bridge evidence from RD-08/RD-09/RD-12.

Context Runtime does not create the dependency, global scene synchronization, shared frontier or universal active-scene set. It consumes the smallest lawful scoped basis and applies ordinary currentness/eligibility/requiredness laws.

## Task 11 — verification / Version Impact

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd11_context_runtime -v
DEV/TOOLS/run_maintenance_audit
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Version Impact Gate classifies DEV ephemeral validation-contract/profile registrations and direct project-map/audit projections. No durable campaign migration exists for RoleContextBundle/Trace/profile/source basis.

Negative stale proof must find no durable context-memory owner, hidden-token dependency, ranking/physical-presence eligibility, required-evidence eviction, arbitrary graph/history scan, trace-as-evidence/output, persistent fairness, background retrieval authority or global R122 synchronization.

## Currentness fence

Before execution, fresh-read R2.3, WP-09, WP-08, R2.4, RD-02/RD-09/RD-10 current plans and exact source/routing consumers. When RD-12 exists, fresh-read its controlled-actor/collaboration contracts before closing `R124` or `R122.CONTEXT` integration tests. Semantic owner/decomposition drift stops execution.

RD-11 closes only its direct leaves and listed slices. `R087`, `R122` and downstream `R124` integration remain subject to their sibling joins and package proof/Version Impact closure.