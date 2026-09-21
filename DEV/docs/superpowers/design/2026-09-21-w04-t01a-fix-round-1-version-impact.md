# W04.T01A Fix Round 1 — Version Impact Checkpoint Evidence

Status: **CHECKPOINT EVIDENCE — TARGETED REVIEW REPAIR (CORRECTED)**

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
| `GAME/TOOLS/collaboration.py` `framework_module_version` | `1.0.1` | `1.0.2` | Corrected material-repair impact: the actual parent/checkpoint already contained collaboration module revision `1.0.1`; this owner-local behavioral repair advances the revision to `1.0.2`. |
| `runtime.collaboration_obligation` local schema | `1` | `1` | Existing schema owner is unchanged by this repair; no schema bump is required. |
| `GAME/SCHEMA/collaboration_obligation.schema.yaml` projection | `1` | `1` | Existing synchronized projection is unchanged; no projection bump is required. |
| `IntentClause` collaboration semantics | existing additive collaboration fields | unchanged | Existing non-collaboration clauses remain valid. This pre-release owner has no independent schema-version field; no separate IntentClause bump is defined. |
| `campaign_contract_generation` | `2` | `2` | No bump: no released-campaign migration or campaign-wide persistent interpretation change is introduced. |
| `storage_format_generation` | `3` | `3` | No bump: deterministic WP-11 route/layout is unchanged. |
| `catalog_generation` | `2` | `2` | No bump: no coordinated catalog vocabulary change. |
| `engine_version` | `1.0-alpha` | `1.0-alpha` | No release bump: this is an owner-local pre-release repair. |

**VERSION_IMPACT:** corrected material repair advances `GAME/TOOLS/collaboration.py` from `1.0.1` to `1.0.2`; collaboration schema and synchronized GAME projection remain at `1`; IntentClause change is additive/pre-release with no independent bump; campaign/storage/catalog/engine namespaces unchanged.

## Correction record

The earlier `absent (new module) -> 1.0.1` classification was incorrect: the real parent/checkpoint already carried `framework_module_version: 1.0.1`, and the existing collaboration schema/projection were already at `1`. This correction supersedes the earlier Version Impact rows; the implementation scope and protected-surface statements remain unchanged.

The current round-2 execution starts from checkpoint `7c2a2a16db3df4cdad4952e48f7ea9b848ed3578`, which also carries collaboration `1.0.1`; the material owner repair in this checkpoint advances it to `1.0.2`.

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
