# W04.T01A Fix Round 1 — Version Impact Checkpoint Evidence

Status: **CHECKPOINT EVIDENCE — TARGETED REVIEW REPAIR**

Base remote HEAD before this repair: `9f9fc4855958b4238ea7bdf304ec0f63a5544bdf`

## Scope

This repair is limited to the already authorized W04.T01A collaboration lane:

- closed dependency-class-specific native basis admission for the five ruled classes;
- current pending Procedure/Continuation response-order precedence;
- fail-closed stale/incomplete native basis evidence;
- no new owner, generic record, registry, callback, Wave-05 write or shared cursor edit.

## Version Impact Gate

| Owner / namespace | Before | After | Classification and result |
|---|---:|---:|---|
| `GAME/TOOLS/collaboration.py` `framework_module_version` | absent (new module) | `1.0.1` | New engine-bound module starts at current engine line `1.0`, local revision `1`; no additional bump in this repair. |
| `runtime.collaboration_obligation` local schema | absent (new family) | `1` | New persistent family starts at schema version `1`; no prior family version exists to bump. |
| `GAME/SCHEMA/collaboration_obligation.schema.yaml` projection | absent (new projection) | `1` | Synchronized with the JSON owner at schema version `1`. |
| `IntentClause` collaboration semantics | absent | additive optional collaboration fields; native basis refs require `revision` | Existing non-collaboration clauses remain valid. This pre-release owner has no independent schema-version field; no separate IntentClause bump is defined. |
| `campaign_contract_generation` | `2` | `2` | No bump: no released-campaign migration or campaign-wide persistent interpretation change is introduced. |
| `storage_format_generation` | `3` | `3` | No bump: deterministic WP-11 route/layout is unchanged. |
| `catalog_generation` | `2` | `2` | No bump: no coordinated catalog vocabulary change. |
| `engine_version` | `1.0-alpha` | `1.0-alpha` | No release bump: this is an owner-local pre-release repair. |

**VERSION_IMPACT:** new collaboration module initialized at `1.0.1`; new collaboration schema and synchronized GAME projection initialized at `1`; IntentClause change is additive/pre-release with no independent bump; campaign/storage/catalog/engine namespaces unchanged.

## Basis-table result

The implementation uses one closed native basis rule per ruled dependency class:

| Dependency class | Required native family | Scope identity |
|---|---|---|
| `JOINT_VOLUNTARY_ACTION` | `world.scene` | `scene_id` |
| `SHARED_DECISION_OR_NEGOTIATION` | `world.scene` | `scene_id` |
| `SHARED_SCARCE_RESOURCE_CHOICE` | `world.asset` | `asset_id` |
| `SCENE_CHRONOLOGY_CONVERGENCE` | `world.scene` | `scene_id` |
| `PC_CONSEQUENCE_DECISION` | `world.actor` | `actor_id` |

`runtime.procedure` and `runtime.continuation` are admitted only as native ordered-owner candidates and only when current active pending response/order/resume evidence exists. Terminal or no-pending owners fail closed; generic world-owner state markers cannot claim ordered precedence.

## Protected surfaces

`DEV/CURRENT_PROGRESS.md`, the Wave-04 execution cursor, Wave-05 shared owners and `.entire/` are outside this checkpoint and remain untouched.

**SYSTEM_IMPACT: NONE.**
