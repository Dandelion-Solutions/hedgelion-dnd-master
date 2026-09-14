# HDM Implementation Planning — Execution Waves / Dependency Graph v2

Status: **CURRENT POST-GRAPH EXECUTION ROUTE — PLANNING ONLY**
Date: 2026-09-14
Finding: **AUTHOR FINDING 21 — SIGNIFICANT**
Production implementation: **NO**.

This document supersedes the 14-RD execution-wave topology for current execution scheduling. Historical wave documents remain provenance for their accepted edges; this v2 reconciles them with RD-15, RD-16 and Findings 6–20.

## Edge law

- `HARD_PRECEDES`: target checkpoint is semantically invalid before predecessor output exists.
- `JOIN_BEFORE_INTEGRATION`: owner-local work may proceed independently; named integrated checkpoint waits for all inputs.
- `SHARED_FILE_CHECKPOINT`: physical writes are serialized against fresh current bytes without transferring semantic authority.
- `PROOF_AFTER_TARGET`: proof waits for the implicated mechanisms.
- wave/tier labels are scheduling preferences, never hidden prerequisites.

Every publishable checkpoint obeys overlay 5: all tests already present, maintenance audit and full DEV discovery are GREEN. Future-task RED groups are not committed early.

## Tier A — independent owner-local work

The following may proceed in parallel when their own local prerequisites are satisfied:

```text
RD-01 shipped projection cleanup
RD-02 information / knowledge / disclosure / message core
RD-03 actor / asset / effect core
RD-04 routing / HOT / allocator owner-local work
RD-05 deterministic mechanics core and Procedure/Continuation owner-local work
RD-08 thread / temporal / chronology owner-local work
RD-09 principal / LIVE owner-local work
RD-10 typed role / Interpreter-result / emission core
RD-11 Context Runtime core
RD-12 collaboration core
RD-13 native history / Story / Dramaturg owner-local work
RD-14 bootstrap/product preparation that does not consume unfinished owners
RD-15 exact BoundCatalogContext construction over current S6D package outputs
RD-16 quiet-world-family strict-schema work over already-current semantic owners
```

RD-06 publication and RD-07 recovery owner-local foundations may also proceed when their existing RD-04/RD-05 inputs are available; they do not wait for unrelated later domains.

## Tier B — semantic seams

### Catalog-backed execution seam

```text
RD-10 typed InterpreterResult
  HARD_PRECEDES
RD-15 candidate binding / deterministic same-context validation
  HARD_PRECEDES for catalog-backed executable requests
RD-05 RuntimeCommand acceptance
```

RD-05 pure deterministic mechanics helpers may exist before RD-15. The hard edge applies to catalog-backed command acceptance/integration, not to owner-native non-catalog transitions.

`SUPPORTED` binding preserves the same catalog-context fingerprint into RuntimeCommand. `UNSUPPORTED` produces no RuntimeCommand and routes to RD-15 gap evidence.

### Execution / publication / recovery seams

```text
RD-05 accepted execution
  JOIN_BEFORE_INTEGRATION -> RD-06 publication
  JOIN_BEFORE_INTEGRATION -> RD-07 accepted-execution recovery
  JOIN_BEFORE_INTEGRATION -> RD-08 accepted occurrence/execution closure
  JOIN_BEFORE_INTEGRATION -> RD-09 current execution source join
```

RD-06 current publication + RD-04 current route evidence join RD-07 current-native recovery. Selected-LIVE recovery additionally joins RD-09 exact selected source/currentness.

### Catalog-gap evidence seam

```text
RD-15 deterministic UNSUPPORTED result
  -> stable runtime.catalog_gap_report candidate
  JOIN_BEFORE_INTEGRATION -> RD-06 campaign publication
  PROOF_AFTER_TARGET -> RD-07 retained evidence / non-authority recovery
```

### Information / LIVE / history seam

RD-09 material LIVE evidence joins RD-02 normalization and RD-13 native SemanticEvent where material. Accepted close and later absorption remain separate: successful close may remain `CLOSED_UNABSORBED` while later normalization/publication is retried.

### Story / bootstrap seam

RD-13 static Story selector and owner-local Story contract join RD-14 generated-scaffold preservation. Story bytes/T0 remain non-prerequisites for blank campaign/New Game readiness.

## Tier C — shared machine integration

RD-16 owns one final shared machine checkpoint. Before that checkpoint:

```text
RD-08 world.thread                    LOCAL_SEMANTIC_READY
RD-04 world.player / no-world.faction LOCAL_SEMANTIC_READY
RD-05 MechanicalEvent identity        LOCAL_SEMANTIC_READY
RD-09 exhaustive live-birth table     LOCAL_SEMANTIC_READY
RD-15 catalog-gap policy input         LOCAL_SEMANTIC_READY
RD-16 17-family strict schemas         READY
```

Then:

```text
all inputs
  JOIN_BEFORE_INTEGRATION
RD-16 SHARED_MACHINE_INTEGRATION
  -> core catalog / admission / structures / identifier policy / schema / projections coherent together
```

No producer RD independently publishes a competing final version of those shared machine files after RD-16 integration begins.

RD-16 integration is required before final R018 closure and before RD-14 final scaffold validation claims the v1 family/catalog topology.

## Tier D — shared shipped-consumer checkpoints

Physical file overlap does not create semantic ownership transfer.

- Scene routing: RD-08 chronology/scene delta first, then RD-09 LIVE routing delta against fresh bytes, followed by joint proof.
- Catalog-binding instructions: RD-15 owns binding semantics in `PLAY_POLICY`, `CORE_INDEX`, `ADJUDICATION`; if RD-01 also changes the same file, use one coherent ordered writer/merge and prove both requirement sets.
- Multiplayer/session prose: RD-09 LIVE lifecycle/currentness and RD-12 collaboration deltas use one ordered physical cutover where the same file is touched.
- Historical RD-02/RD-03/RD-04 shared GAME schema ordering remains as accepted by the original execution-wave package.
- `PROJECT_MAP` and `audit_engine.py` are projection surfaces; every later writer fresh-reads current bytes and preserves all admitted routing/audit assertions.

## Tier E — context / collaboration / retained projections

Existing owner-local independence remains:

- RD-11 context and RD-12 collaboration cores are not cyclic.
- RD-11 integrated context acceptance joins applicable RD-02 disclosure, RD-09 currentness, RD-10 containment and RD-12 controlled-actor scope.
- retained Dramaturg candidate generation stays ephemeral until RD-06 campaign publication accepts it; current RD-09/RD-10/RD-12 evidence participates only at admission/publication join.
- RD-13 native history remains independently authoritative and is not gated on Story projection freshness.

## Tier F — product/scaffold integration

RD-14 owner-local bootstrap work may precede later joins. Final bootstrap/product closure waits only for named consumers:

- current 17-family post-RD16 topology/scaffold expectations;
- ruleset-set identity propagation;
- PLAYER/no-faction routing consequences;
- Story selector preservation;
- applicable save/session/menu and creator-provenance joins.

No gameplay bootstrap is executed by this planning package.

## Tier G — proof / coverage closure

`PROOF_AFTER_TARGET` only:

1. historical readiness proof through current v2 ledger/appendices;
2. post-graph proof through `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md`;
3. current bidirectional coverage through `2026-09-14-implementation-planning-bidirectional-coverage-v3-post-graph.md`;
4. R018 waits for RD-15 catalog-gap family + RD-16 exact world-family/shared-machine joins;
5. all eight historical composite parents retain their original accepted semantics;
6. dormant empirical trigger rows remain dormant.

## Cycle check

Current hard-edge graph is acyclic:

```text
RD-10 -> RD-15 -> RD-05 catalog-backed acceptance
RD-04/RD-05/RD-08/RD-09/RD-15 -> RD-16 shared integration
RD-05 -> RD-06 -> RD-07 integration joins
RD-09 -> RD-07 selected-LIVE join
RD-13 -> RD-14 Story-selector consumer join
RD-16 -> RD-14 final topology/scaffold validation
```

Owner-local portions not named by these edges retain parallel eligibility.

## Current completion gate

Before independent handoff, verify:

- every RD-01..RD-16 appears in this graph or is explicitly owner-local;
- no hard edge is inferred merely from tier number;
- RD-15 cannot be bypassed by catalog-backed RD-05 acceptance;
- RD-16 has one final shared machine writer;
- no publishable checkpoint contains future intentional RED tests;
- coverage v3 and proof-ledger v3 match this 16-RD graph;
- exact-head hosted validation is green.

Production implementation remains unauthorized.
