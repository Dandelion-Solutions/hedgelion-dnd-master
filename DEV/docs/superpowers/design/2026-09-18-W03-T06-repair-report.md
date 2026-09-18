# W03.T06 repair report

## Scope and checkpoint

- **Task:** W03.T06 repair from `9d747c8bf3c097181ffdcacbfd9fe808cb317fe3`.
- **Implementation checkpoint:** `625e5488cf5e4dd51c3d8691196bbea3c30a2144`.
- **Verification/cursor checkpoint:** `32016e09ba5543c917b40ae740b602272a8bb951`.
- **Publication:** non-force push completed; fresh remote read-back matched `32016e09ba5543c917b40ae740b602272a8bb951`.

## Impact Envelope

- **Included owners:** `GAME/TOOLS/live_state.py`, `GAME/TOOLS/temporal.py`, `GAME/TOOLS/recovery_roots.py`, RD08/RD09 tests, and dedicated ephemeral operational-root handoff schemas.
- **Consumers:** campaign/LIVE temporal routing, Agenda rebuilding, operational-root campaign/LIVE handoff, absorption CAS validation, and terminal/replacement removal validation.
- **Excluded:** engine release metadata, campaign/storage generations, existing LIVE routing schema v4, operational-root page schema v1, catalogs, identifier-policy bytes, shared CORE/schema surfaces, and Wave-05 targets.

## Delivered repairs

- `CLOSED_UNABSORBED` remains LIVE-authoritative until exact accepted absorption evidence proves campaign return.
- Campaign recovery requires typed owner-issued accepted absorption CAS evidence bound to the exact source and route.
- Temporal handoffs require exact native-owner root sets and reject omissions, extras, cross-campaign routes, and forged terminal entries.
- Operational terminal and superseded removals require owner-issued native deltas/replacement proofs.
- Temporal and operational handoff wrappers accept exact verified successor retries.
- `OperationalRootHandoff` has a strict distinct `kind`/`schema_version` contract with DEV JSON and GAME YAML schema owners.

## TDD and verification

- Baseline: named T06 suites passed `221` tests with `1` skip.
- RED witnesses covered caller absorption/lifecycle assertions, missing exact temporal sets, stale retries, forged removal proof, and untyped serialized handoff.
- Focused named suites: `229` passed, `1` skipped.
- Full DEV discovery: `911` passed, `7` skipped.
- Maintenance audit, JSON Schema checks, compile verification, and `git diff --check`: passed.
- Hosted CI is unavailable in the local-machine runtime.

## Version Impact

- LIVE runtime `framework_module_version`: `1.0.10 -> 1.0.11`.
- Temporal runtime `framework_module_version`: `1.0.1 -> 1.0.2`.
- Operational-root runtime `framework_module_version`: `1.0.7 -> 1.0.8`.
- New ephemeral operational-root handoff schema namespace starts at `1` in DEV/GAME projections.
- No engine-release, campaign-contract, storage-format, catalog, identifier-policy, existing LIVE routing, operational-root page, or shared projection bump.

## System impact and residual concern

**SYSTEM_IMPACT: NONE.** The repair stays inside the approved temporal/LIVE/operational-root routing envelope and adds no semantic owner, dependency-direction change, distributed transaction, broad scan, fallback authority, or Wave-05 write.

The plan-named `GAME/CAMPAIGN/STATE/RUNTIME/TEMPORAL_ROUTING.yaml` scaffold remains deferred to the planned W05 generated-scaffold/shared-storage integration.
