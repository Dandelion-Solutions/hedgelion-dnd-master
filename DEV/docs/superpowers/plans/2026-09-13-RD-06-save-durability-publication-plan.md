# RD-06 — Scoped SAVE / Durability / Publication Currentness — Executable Implementation Plan

Goal: realize scope-relative durability and explicit SAVE composition over admitted native domains, plus exact immutable campaign publication and bounded ambiguity reconciliation.

RD unit: `RD-06`
Direct readiness: `R037,R045,R069,R070,R071`.
Composite slices/parents: `R029.DURABILITY`.
Pure-proof leaves: none directly owned.
Canonical owners: Step-5.5 durability/SAVE; Step-5.6 publication/crash consistency; WP-13; WP-11 route/index; WP-12 HOT; exact Step-2 records.
Dependencies/joins: consumes RD-05 established post-transaction state and RD-04 owner-generation/dirty substrate; `R069 HARD_PRECEDES R070`; outputs current publication evidence to RD-07 and provisional Actor durability join to RD-14.
Out of scope: execution establishment, recovery selection, LIVE CAS semantics, alternate Git transport, global transaction/save frontier, migration/release execution.

## Impact Envelope

GAME runtime: `NEW_CREATE GAME/TOOLS/durability.py`, `NEW_CREATE GAME/TOOLS/publication.py`.
DEV contracts: `NEW_CREATE DEV/SCHEMAS/durability-promise-result.schema.json`, `campaign-publication-attempt.schema.json`; existing source/native owner schemas inspected only.
Tests: `NEW_CREATE DEV/TESTS/test_rd06_durability_publication.py`.
Projection/docs: `GAME/SCHEMA/session.schema.yaml`, `GAME/TEMPLATE/STORAGE_README.md`, `DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` only where current text/assertions grant excess save/publication authority.
Cross-RD: RD-04 HOT generation freeze/clear helpers; RD-05 execution; RD-07 recovery; RD-14 R029 durability.
Negative laws: no global durable frontier/clock/dirty generation, no per-file Contents publication, alternate transport fallback, force push, merge commit, persistent publication journal, generic rollback, SQLite+Git transaction, blind retry after ambiguity, or “saved” before compatible current closure proof.
Version/schema/checkpoint: classify new API/contracts; checkpoint semantics remain RD-07.
Migration: none under clean-slate.
HG-01: constraint 3; implementation may choose operation data shapes but no new semantic owner.
Currentness set: Step-5.5/5.6, WP-11/12/13, exact readiness records, RD-04/05 published implementation contracts, named session/storage/projection surfaces.

## Task 1 — RED: durability promise semantics

Files:
- `NEW_CREATE DEV/TESTS/test_rd06_durability_publication.py`
- `NEW_CREATE DEV/SCHEMAS/durability-promise-result.schema.json` in GREEN.

Required typed result:
```text
DurabilityPromiseResult
  disposition: SUCCEEDED | FAILED | INDETERMINATE
  domain_results: typed native-domain results
  covered_generations/source_basis
  reason/evidence refs as bounded diagnostics
```
The shape is operation evidence, not persistent gameplay authority.

RED cases:
1. explicit SAVE freezes one definite selected scope/root/generation set;
2. automatic/risk-control durability is distinguishable from explicit user SAVE metadata (`R045`);
3. clean current closure may return no-write only with sufficient current evidence, not merely empty dirty set;
4. partial domain success remains real while overall SAVE is incomplete;
5. failed explicit SAVE cannot claim `saved`;
6. independent scopes are not forced into one global barrier/frontier.

Run:
```bash
python3 -m unittest DEV.TESTS.test_rd06_durability_publication -v
```
Expected: RED because durability implementation/contracts are absent.

## Task 2 — GREEN: scope-relative durability engine

Files:
- `NEW_CREATE GAME/TOOLS/durability.py`
- `NEW_CREATE DEV/SCHEMAS/durability-promise-result.schema.json`
- `EXISTING_MODIFY DEV/TESTS/test_rd06_durability_publication.py`.

Shipped interfaces:
```text
evaluate_durability(scope, reason, owner_generations, source_basis) -> DurabilityEvaluation
freeze_save_promise(...) -> FrozenSavePromise
complete_save_promise(...) -> DurabilityPromiseResult
```
`FrozenSavePromise`/evaluation are ephemeral in-memory values, not durable owners.

GREEN:
- only already-established state participates;
- derive required compatible closure separately from pending write set;
- freeze scope locally without campaign-global lock;
- compose native-domain results and final compatibility proof;
- clear only exact published generations through RD-04 HOT helper; newer generations remain dirty.

VERIFY focused durability tests PASS.

Commit boundary: durability module + typed result schema + tests.

## Task 3 — RED/GREEN: immutable publication attempt

Files:
- `NEW_CREATE GAME/TOOLS/publication.py`
- `NEW_CREATE DEV/SCHEMAS/campaign-publication-attempt.schema.json`
- focused test.

Interfaces:
```text
freeze_campaign_publication_attempt(...) -> FrozenCampaignPublicationAttempt
build_connector_git_plan(attempt) -> ConnectorGitPlan
classify_ref_transition(...) -> APPLIED | NOT_APPLIED | INDETERMINATE
reconcile_indeterminate_publication(...) -> RefTransitionOutcome
```
`ConnectorGitPlan` is deterministic data consumed by the fixed gameplay Connector boundary; this module is not an HTTP/Git/CLI client.

RED/GREEN laws:
- freeze repository/ref/principal evidence/pinned H/base tree/frozen generations/closure/authorized path delta before first remote mutation;
- normalize byte-identical UPSERT and absent DELETE;
- one base-derived tree + one single-parent commit + `force=false` target-ref transition;
- no per-file Contents writes, merge/staging/force publication;
- target movement before final transition yields typed conflict/reconcile path;
- ambiguous outcome never triggers blind replay; reconciliation observes authority first;
- resulting-tree proof remains bounded to touched closure/dependencies.

Commit boundary: publication planner/result epistemics + tests.

## Task 4 — Integrate established execution with SAVE barrier

Files:
- `EXISTING_MODIFY GAME/TOOLS/durability.py`
- `INSPECT_ONLY GAME/TOOLS/runtime_execution.py`
- `INSPECT_ONLY GAME/TOOLS/hot_store.py`
- focused test.

RED/GREEN scenarios:
- `R034+R035+R036` established execution completes before R037 freeze;
- SAVE cannot freeze partial/unaccepted execution as durable gameplay state;
- exact post-transaction owner generations become input to durability;
- publication success clears only frozen generation(s);
- unrelated new owner mutation G+1 during/after publication is not erased by success for G.

No distributed transaction across runtime execution/HOT/Connector is introduced.

## Task 5 — Session/storage projection cleanup and R029 durability join

Files:
- `EXISTING_MODIFY GAME/SCHEMA/session.schema.yaml` only to make base/published HEAD observations explicitly non-authoritative where needed;
- `EXISTING_MODIFY GAME/TEMPLATE/STORAGE_README.md` only for fixed publication/save semantics actually exposed there;
- `EXISTING_MODIFY DEV/PROJECT_MAP.md`, `DEV/TOOLS/audit_engine.py` for new shipped modules/contracts;
- focused test.

Prove `R029.DURABILITY`: provisional Actor/onboarding state from RD-03 can enter the same scope-relative durability machinery, while RD-14 retains onboarding/lifecycle completion authority.

Do not implement checkpoint recovery or onboarding here.

## Task 6 — Publication/currentness closure

Scenario suite must cover WP-13 proof obligations relevant to R069-R071, including:
- current no-write proof;
- conflicting ref movement;
- ambiguous final transition then observation/reconcile;
- G/G+1 exact generation clearing;
- partial native-domain success;
- failed/indeterminate SAVE acknowledgement suppression;
- no stale-basis publication;
- no fictional chronology derived from commit order/time.

Full verification:
```bash
python3 -m unittest DEV.TESTS.test_rd06_durability_publication -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```
Expected: PASS.

Version Impact Gate: classify new durability/publication API/schema generations and direct projection changes under current version owners.

Stale proof: active GAME/DEV contains no global save frontier/heartbeat, blanket HARD timer, per-file publication path, transport fallback, force update, persistent publication journal or commit-time chronology authority.

Final commit boundary: durability + publication planner/currentness semantics + direct projections/tests form an independently reviewable RD-06 result.

## Fresh-worker checkpoint protocol

The task sequence above is implemented as four green publication checkpoints. A RED-only diagnostic commit is not allowed.

1. **DURABILITY** — `DurabilityPromiseContractTests`: exact scope/root/generation freeze, explicit-vs-automatic durability, current no-write proof, partial-domain truth, acknowledgement suppression, scope-locality, exact G/G+1 clearing. Task 1 RED and Task 2 GREEN/REFACTOR are one checkpoint.
2. **PUBLICATION** — `PublicationPlanTests` + `PublicationOutcomeTests`: frozen base/ref/principal/path closure, normalized delta, one base-derived tree/single parent/non-force transition, conflict and indeterminate reconciliation, no alternate transport, bounded resulting-tree proof. Task 3 is one checkpoint.
3. **EXECUTION_JOIN** — `ExecutionDurabilityJoinTests`: RD-05 accepted execution precedes freeze, partial execution excluded, exact owner generations consumed, G+1 survives G publication. Task 4 is one checkpoint.
4. **PROJECTION_AND_PROOF** — `DurabilityProjectionTests` + `Wp13ProofTests`: Task 5 current-body corrections plus the exact R071 proof rows assigned by the package lossless-proof ledger.

Focused commands are respectively:
```bash
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.DurabilityPromiseContractTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.PublicationPlanTests DEV.TESTS.test_rd06_durability_publication.PublicationOutcomeTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.ExecutionDurabilityJoinTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.DurabilityProjectionTests DEV.TESTS.test_rd06_durability_publication.Wp13ProofTests -v
```

For every checkpoint: RED must identify only the intended missing target; GREEN implements only named files/interfaces; REFACTOR removes duplication without changing owners; focused VERIFY must PASS before commit.

`R071` cannot close from Task 6's thematic list alone. The package lossless-proof ledger must enumerate every active WP-13 proof theme and attach it to one named test/scenario/channel. In particular it must explicitly witness quiescence/freeze release, owner-defined rejection/disjoint-vs-overlap handling, independent storage transaction semantics, maintenance-vs-gameplay authority, and disposition of named stale tests in addition to the cases already listed above. Missing witness is RED; `NOT_APPLICABLE` requires an owner-backed reason. Future-trigger leaves stay dormant.

RD-06 completion requires all five direct leaves, `R029.DURABILITY` recorded only as a slice, every RD-06-owned R071 proof-ledger row witnessed, local Version Impact evidence, remote read-back and hosted CI.