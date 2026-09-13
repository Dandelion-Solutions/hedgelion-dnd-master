# PB-03 Source Manifest — RD-05..RD-08

Status: **PB-03 CONTROLLED SOURCE MANIFEST / IMPLEMENTATION PLANNING ONLY**

Baseline HEAD: `c7a952b342831d0fbba25a656f07c3bfc715adc2`

This manifest is subordinate to accepted native owners, exact WP-27 Step-2 readiness records, the WP-27 canonical readiness specification and critic-approved bounded decomposition v2. It authorizes no production implementation.

## Shared controlling sources

- `DEV/CURRENT_PROGRESS.md`
- `DEV/docs/superpowers/design/2026-09-13-implementation-planning-candidate-bounded-decomposition-v2.md`
- `DEV/docs/superpowers/design/2026-09-10-r2-7-WP-27-step-2-evidence-ledger.md`
- `DEV/docs/superpowers/specs/2026-09-11-r2-7-WP-27-final-implementation-planning-readiness-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`
- Step-5.2/5.3/5.5/5.6/5.7/5.9 canonical specs and temporal integration amendment
- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md`
- WP-11 routing, WP-12 HOT/atomicity and WP-25 failure/degradation owners
- PB-01 package conventions and Impact/TDD contract.

## RD-05 — deterministic execution / fixed RNG / failure adapters

Direct readiness: `R034,R035,R036,R042,R046,R112`.
Composite contribution: `R062.RUNTIME_LIFECYCLE_EVIDENCE`.

Owner boundaries:
- runtime lifecycle owners remain Interaction / IntentPlan / Command / Procedure / Resolution / Continuation;
- execution/firing/acceptance identities are derived at accepted contract boundaries, not a new global nonce/correlation owner;
- fixed accepted RNG is retained and reused on retry/recovery;
- mechanic transaction covers deterministic declaration/RNG/result/effect establishment only, never host choice or repository/network I/O;
- invalid proposals and unavailable deterministic math return typed failure/degraded outcomes without mutation.

Current machine realization:
- DEV already contains `runtime-command-state`, `runtime-continuation-state`, `runtime-intent-plan-state`, `runtime-interaction-state`, `runtime-procedure-state`, `runtime-resolution-state`, `runtime-mechanical-event-state`, `runtime-resolution-trace-state`, `resolution-receipt`, `execution-segment`, roll and mechanical-surface schemas;
- `GAME/TOOLS` has no shipped execution executor;
- deterministic skill/tool/save derivation still lacks an executable calculator;
- publication metadata is not RD-05 authority.

Exact implementation surfaces selected for the executable plan:
- `GAME/TOOLS/runtime_execution.py` — lifecycle/accepted-execution orchestration only;
- `GAME/TOOLS/mechanics.py` — deterministic rule calculation and fixed RNG application only;
- existing DEV runtime/mechanics schemas above are reconciled rather than duplicated;
- focused test: `DEV/TESTS/test_rd05_runtime_execution.py`.

No generic engine-state/pending/job/transaction owner, no reroll-on-retry, no event-ID RNG seed and no diagnostic-as-gameplay authority.

## RD-06 — SAVE / durability / publication currentness

Direct readiness: `R037,R045,R069,R070,R071`.
Composite contribution: `R029.DURABILITY`.

Canonical owner split:
- execution establishment precedes durability evaluation;
- SAVE is scope-relative composition over admitted native durability domains;
- explicit SAVE freezes one definite selected promise scope; opportunistic/risk-control durability remains distinct;
- campaign publication uses immutable ephemeral attempt, one coherent tree + one parent commit + non-force exact ref transition via fixed Connector transport;
- publication result is epistemic (`APPLIED | NOT_APPLIED | INDETERMINATE`-class semantics), and ambiguity is reconciled rather than blindly retried;
- no global save frontier/clock/dirty generation, no persistent publication journal, no distributed SQLite+Git transaction.

Current machine realization:
- no shipped durability/publication module exists in `GAME/TOOLS`;
- current session/storage schemas contain metadata that must remain coordination/provenance only;
- RD-04 HOT dirty-generation helpers are the local substrate consumed by RD-06, not publication authority.

Exact implementation surfaces selected:
- `GAME/TOOLS/durability.py` — scope evaluation, SAVE composition, generation freeze/result semantics;
- `GAME/TOOLS/publication.py` — immutable campaign publication plan + Connector-operation envelope/result reconciliation, but not an alternate transport client;
- `DEV/SCHEMAS/durability-promise-result.schema.json` and `campaign-publication-attempt.schema.json` as implementation-facing validation contracts for the selected typed values;
- focused test: `DEV/TESTS/test_rd06_durability_publication.py`.

RD-06 consumes RD-04 HOT and RD-05 established execution. `R069 HARD_PRECEDES R070`. Recovery interpretation remains RD-07.

## RD-07 — current-native recovery / checkpoint alignment

Direct readiness: `R011,R012,R038,R072,R073,R074`.

Canonical owner split:
- cold recovery reconstructs current Resumable Runtime Closure from current native authorities selected by current routes;
- checkpoint is optional immutable descriptor/evidence only, never current authority/root registry/SAVE proof/recovery frontier;
- current live/native source never falls back to stale campaign/cache/checkpoint authority;
- already accepted execution resumes with retained identity/RNG/interpretation and is never replayed or reallocated;
- surviving SQLite is cache/acceleration only after source-equivalence proof;
- historical maintenance/repair is a separate evidence-gated operation, never generic rollback/current promotion.

Current machine debt:
- `GAME/SCHEMA/checkpoint.schema.yaml` still requires `valid_through_event_id` and admits `expected_commit_sha` with frontier-like wording even though WP-14 retires both;
- current checkpoint template alignment must follow WP-14 field-by-field disposition;
- `GAME/SCHEMA/session.schema.yaml` is usable only as coordination/navigation/audit projection, not liveness/currentness authority;
- no shipped recovery executor exists.

Exact implementation surfaces selected:
- `GAME/TOOLS/recovery.py` — current-source selection/hydration/final validation and bounded historical-maintenance entry points;
- `GAME/SCHEMA/checkpoint.schema.yaml` and checkpoint template are replaced/reconciled to WP-14 dispositions;
- `GAME/SCHEMA/session.schema.yaml` is reconciled only where current wording grants excess authority;
- `DEV/SCHEMAS/recovery-result.schema.json` validates ephemeral `READY | RETRY | BLOCKED` result shape without making it persistent authority;
- focused test: `DEV/TESTS/test_rd07_recovery.py`.

No checkpoint-first restore, latest-by-enumeration, stale HOT authority, ref rewind, disclosure rewind, allocator regression or synthetic accepted IDs.

## RD-08 — temporal / thread / current-state ownership

Direct readiness: `R010,R039,R075,R076,R077`.
Composite contributions: `R006.THREAD_VISIBILITY,R016.TEMPORAL,R018.TEMPORAL,R062.TEMPORAL_BINDING,R122.CHRONOLOGY`.

Canonical owner split:
- native temporal/process owners own obligation existence/lifecycle/occurrence identity and owner-local TemporalBinding;
- Agenda is rebuildable dependency-indexed nomination/invalidation support only;
- chronology is sparse accepted typed evidence, not a global clock/frontier;
- Step-3 execution owns accepted consequences and stable firing/execution identity;
- `world.thread` is narrow generic process owner only where no more-specific owner exists.

Current machine debt:
- `GAME/SCHEMA/current_state.schema.yaml` still requires global `world_time.frontier`; this must be removed because CURRENT is routing summary only;
- `GAME/SCHEMA/thread.schema.yaml` has under-specified `deadline: object|null` and legacy `visibility.known_by_pc_ids/public`, while thread visibility must use native information/disclosure owners;
- DEV already has `temporal-binding.schema.json`, `boundary-occurrence.schema.json`, `trigger-binding.schema.json`; no final `world.thread` machine contract or derived Agenda contract is installed;
- `GAME/SCHEMA/event.schema.yaml` has useful sparse/local chronology language but cannot become the sole chronology owner or global sequence.

Exact implementation surfaces selected:
- `GAME/TOOLS/temporal.py` — typed dependency enrollment, owner-local due evaluation, derived Agenda rebuild/invalidation and accepted-occurrence handoff to RD-05 execution;
- `GAME/SCHEMA/thread.schema.yaml` replacement/reconciliation;
- `GAME/SCHEMA/current_state.schema.yaml` replacement/reconciliation removing global chronology frontier;
- `DEV/SCHEMAS/world-thread-state.schema.json` and `temporal-agenda-entry.schema.json`;
- existing `DEV/SCHEMAS/temporal-binding.schema.json` is reconciled, not replaced by another owner;
- catalog/admission/identifier projections are updated only as required to admit exact `world.thread` family under existing catalog machinery;
- focused test: `DEV/TESTS/test_rd08_temporal.py`.

No scheduler, durable due flag, global firing ledger, Agenda authority, generic future-RNG frontier, global campaign clock, SQL/Git/ID chronology or broad scan as healthy correctness path.

## Cross-RD joins

- RD-05 consumes RD-04 HOT local atomicity and finalized owner schemas; RD-05 establishes execution before RD-06 durability.
- `R034+R035+R036 JOIN_BEFORE_INTEGRATION R037`.
- RD-06 consumes RD-04 dirty generations and RD-05 established post-transaction state; `R069 HARD_PRECEDES R070`.
- RD-07 consumes RD-06 current publication evidence and RD-05 retained accepted-execution evidence; recovery never owns either.
- RD-08 consumes RD-05 accepted execution for materialized occurrence closure and RD-04 route/HOT substrate; accepted firing identity suppresses duplicate rematerialization during RD-07 recovery.
- R122 chronology slice in RD-08 remains incomplete until RD-09 currentness-scene + RD-11 context + RD-12 collaboration bridge slices and parent proof are complete.

## GAME reconstruction/currentness result

`GAME/**` remains fully reconstructable for v1.0. `current_state`, `checkpoint` and `thread` are confirmed `MIXED`/legacy-bearing machine surfaces; their old fields do not constrain v1 replacement. Existing v1-compatible local chronology/event/session laws are preserved only where consistent with accepted owners.

No architecture contradiction or Product Owner decision was discovered. Exact worker task order/file actions are defined in the four PB-03 executable plans; production implementation remains unauthorized.