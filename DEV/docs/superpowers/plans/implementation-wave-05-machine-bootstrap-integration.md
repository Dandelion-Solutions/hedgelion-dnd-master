# HDM v1 Implementation Wave 05 — Machine, Bootstrap and Shared Integration

Status: **PLANNED / BLOCKED ON INDEPENDENT SENIOR GO**

Goal: integrate the completed owner contracts into the single strict 17-world/17-runtime machine, complete bootstrap and product paths, and perform every shared physical write exactly once with the approved version cutovers.

Use `implementation-plan-execution-contract.md`. Fresh-read every shared file immediately before its final writer; integrate all required GREEN deltas in one checkpoint.

## Entry and exit

Entry requires every owner/join checkpoint named as an input below. Exit requires exact family census, strict schemas/catalogs, complete blank-scaffold/bootstrap paths, current shipped instructions and all retained schema/CORE version targets realized at one coherent HEAD.

Minimum wave impact envelope:

- owners: world/runtime schema machine, shared catalogs/wrappers/identifiers, bootstrap/onboarding, campaign manifest/scaffold, install documentation and material CORE modules;
- consumers: every runtime path and Wave-06 proof;
- protected invariants: one semantic owner, one final physical writer, no duplicate PLAYER/membership authority, no unbounded campaign discovery, no clean-slate compatibility debt;
- version rule: use the exact targets in the index after a fresh current-version check; never double-bump or downgrade an intervening accepted target.

## Baseline file-action and interface manifest

| Integration | Exact physical paths |
|---|---|
| strict world machine | `DEV/SCHEMAS/world-record.schema.json`; strict `world-connection`, `world-zone`, `world-organization`, `world-contract`, `world-mission`, `world-scene`, `world-encounter`, `world-hazard`, `world-player` schemas; owner-provided Actor/Asset/Effect/information/thread schemas; `DEV/TESTS/test_rd16_world_family_machine_integration.py` |
| shared catalog/identity | `DEV/CATALOG/core-catalog.json`, `entity-structures.json`, `identifier-policies.json`, `catalog-admission-ledger/families/world_record_kinds.json`; `DEV/SCHEMAS/identifier-policies.schema.json`; `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`, `ENTITY_STRUCTURES.md`; `DEV/TESTS/test_r2_7_wp03_catalog_conformance.py` |
| retained GAME schemas | `GAME/SCHEMA/checkpoint.schema.yaml`, `current_state.schema.yaml`, `thread.schema.yaml`, `live_scene.schema.yaml`, `index.schema.yaml`, `scene.schema.yaml`, `location.schema.yaml`, `event.schema.yaml`, `lore.schema.yaml`, `player.schema.yaml`, `campaign_manifest.schema.yaml`; inspect `session.schema.yaml` for the separately governed shared durability/recovery delta |
| scaffold/bootstrap | `GAME/TOOLS/bootstrap.py`, `init_campaign.py`; bootstrap request/result/selection schemas; `GAME/CAMPAIGN/MANIFEST.yaml`, `GAME/CAMPAIGN/README.md`, all five empty routing/root scaffold inputs, Story/Dramaturg roots and `DEV/TESTS/test_rd14_bootstrap.py` |
| install/shared docs | `GAME/INSTALL/README.md`, `PROJECT_INSTRUCTIONS.txt`, `00_DND_BOOTSTRAP.md`, `GAME/SCHEMA/README.md`, `GAME/TEMPLATE/STORAGE_README.md` |
| CORE cutover | the sixteen exact modules listed in W05.T08, with one final integration of shared `BOOTSTRAP_RUNTIME.md`, `STORAGE.md` and `MULTIPLAYER.md` |
| control plane | `DEV/PROJECT_MAP.md` and `DEV/TOOLS/audit_engine.py` receive all new module/schema/test routes in one final physical integration; `DEV/TOOLS/run_maintenance_audit.py` is modified only if a focused current RED requires it |

Bootstrap/product callable boundary:

```text
discover_campaign_candidates(...) / hydrate_campaign_cards(...) / select_campaign(...)
resolve_new_campaign_identity(...) / create_new_campaign(...) / resume_existing_campaign(...)
invoke_init_campaign(...) / validate_generated_scaffold(...)
plan_initial_campaign_publication(...) / adopt_initial_publication(...)
progress_onboarding(...) / compute_play_readiness(...)
route_active_player_retrospective(...)
save_and_exit_to_selection(...) / clear_selected_gameplay_context(...) / build_campaign_selection_menu(...)
load_campaign_creator_provenance(...) / classify_creator_authority(...)
```

## W05.T01 — Owner-local strict schema and wrapper inputs

Hard inputs: all relevant owner checkpoints from Waves 01–04, especially information, Actor/Asset/Effect, temporal, PLAYER/collaboration, Story and LIVE source-native identity.

The final world census is exactly:

`world.actor`, `world.actor_group`, `world.asset`, `world.location`, `world.connection`, `world.zone`, `world.organization`, `world.contract`, `world.mission`, `world.scene`, `world.encounter`, `world.hazard`, `world.effect`, `world.lore_fact`, `world.knowledge`, `world.thread`, `world.player`.

The final runtime census is exactly:

`runtime.session`, `runtime.message`, `runtime.interaction`, `runtime.procedure`, `runtime.intent_plan`, `runtime.command`, `runtime.resolution`, `runtime.continuation`, `runtime.mechanical_event`, `runtime.semantic_event`, `runtime.resolution_trace`, `runtime.disclosure`, `runtime.collaboration_obligation`, `runtime.checkpoint`, `runtime.id_allocator`, `runtime.maintenance_audit`, `runtime.catalog_gap_report`.

Required owner-local output:

- strict family schemas or bounded deltas for a named final physical writer, plus the exact family-to-schema wrapper-dispatch inputs;
- accepted definition-binding modes and reference inputs for the shared catalog writer;
- native PLAYER identity plus collaboration strict state;
- source-native identifier policy where required;
- information schemas consumed from W01.T02, never recreated;
- `world.faction` remains an organization facet and does not increase the count;
- the runtime-family matrix below supplies all 17 item-bound realization inputs; census alone cannot close R018.

TDD and verification:

- run the owner-local assertions in `WorldStateSchemaCoverageTests`, `WorldFamilyCensusTests`, `WorldEnvelopeDispatchTests`, `DefinitionBindingModeTests`, `PlayerCollaborationStrictStateIntegrationTests` and `WorldPlayerNativeIdentityTests` in `DEV/TESTS/test_rd16_world_family_machine_integration.py` against the published strict schemas/delta fixtures and dispatch inputs;
- reject an eighteenth family, missing family, duplicate schema owner and loose additional-properties surface in those inputs;
- publish only the assertions that are GREEN with these owner-local inputs. Final catalog/wrapper/identifier assertions in `SharedCatalogIntegrationTests`, `SourceNativeIdentifierPolicyIntegrationTests` and `DEV/TESTS/test_r2_7_wp03_catalog_conformance.py` belong to W05.T02; final `R018WorldFamilyProofTests` and `R018RuntimeFamilyProofTests` belong to W06.T02 after all implicated final writers. Neither is a prerequisite of this owner-local checkpoint.

Output checkpoint: `W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY` (GREEN and published). This checkpoint transfers schema/reference inputs, not final shared catalog/wrapper bytes or an integrated R018 PASS. W05.T01 closes here and never waits for W05.T02.

### Exact runtime-family realization matrix

This item-bound planning fixture preserves the accepted R018 schema/root obligations. Native route authority remains in `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`; the current WP-27 evidence ledger requires per-family schema/root validation and forbids completion from catalog admission. Roots below are native route selectors under that owner, not identity/currentness authority or a new runtime registry.

| Runtime family | Final schema / machine-shape surface | Native root / exceptional route | Owning realization route |
|---|---|---|---|
| `runtime.session` | `GAME/SCHEMA/session.schema.yaml` | `SESSIONS` | W02.T06 recovery/session owner -> W05.T03 `SESSION_SCHEMA_FINAL_INTEGRATION_READY` |
| `runtime.message` | `DEV/SCHEMAS/runtime-message-state.schema.json` | `LOG/MESSAGES` | W01.T02 `W01_INFORMATION_OWNER_READY` |
| `runtime.interaction` | `DEV/SCHEMAS/runtime-interaction-state.schema.json` | `STATE/RUNTIME/INTERACTIONS` | W02.T02 `W02_DETERMINISTIC_EXECUTION_READY` |
| `runtime.procedure` | `DEV/SCHEMAS/runtime-procedure-state.schema.json` plus admitted concrete Procedure-owned subtype shape where applicable | `STATE/RUNTIME/PROCEDURES` | W02.T02 `W02_DETERMINISTIC_EXECUTION_READY` |
| `runtime.intent_plan` | `DEV/SCHEMAS/runtime-intent-plan-state.schema.json` | `STATE/RUNTIME/INTENT_PLANS` | W02.T02 `W02_DETERMINISTIC_EXECUTION_READY` |
| `runtime.command` | `DEV/SCHEMAS/runtime-command-state.schema.json` | `STATE/RUNTIME/COMMANDS` | W02.T01 `W02_CATALOG_BACKED_COMMAND_READY` + W02.T02 lifecycle; W01.T08 catalog context |
| `runtime.resolution` | `DEV/SCHEMAS/runtime-resolution-state.schema.json` | `STATE/RUNTIME/RESOLUTIONS` | W02.T02 `W02_DETERMINISTIC_EXECUTION_READY` |
| `runtime.continuation` | `DEV/SCHEMAS/runtime-continuation-state.schema.json` | `STATE/RUNTIME/CONTINUATIONS` | W02.T02 lifecycle -> W02.T06 `W02_EXACT_RECOVERY_READY` |
| `runtime.mechanical_event` | `DEV/SCHEMAS/runtime-mechanical-event-state.schema.json` | `LOG/MECHANICAL_EVENTS` | W02.T02 identity -> W05.T02 `RD16_SHARED_MACHINE_INTEGRATION_READY` |
| `runtime.semantic_event` | `DEV/SCHEMAS/runtime-semantic-event-state.schema.json` | `LOG/SEMANTIC_EVENTS` | W01.T07 native shape -> W04.T07 `W04_NATIVE_HISTORY_PUBLICATION_READY` |
| `runtime.resolution_trace` | `DEV/SCHEMAS/runtime-resolution-trace-state.schema.json` | `STATE/RUNTIME/RESOLUTION_TRACES` | W02.T02 `W02_DETERMINISTIC_EXECUTION_READY` |
| `runtime.disclosure` | `DEV/SCHEMAS/runtime-disclosure-state.schema.json` | `STATE/RUNTIME/DISCLOSURES` | W01.T02 `W01_INFORMATION_OWNER_READY` |
| `runtime.collaboration_obligation` | `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json` + shipped `GAME/SCHEMA/collaboration_obligation.schema.yaml` projection | `STATE/RUNTIME/COLLABORATION` | W04.T01 `W04_COLLABORATION_ADMISSION_READY` -> W04.T02 `W04_COLLABORATION_PUBLICATION_READY` |
| `runtime.checkpoint` | `GAME/SCHEMA/checkpoint.schema.yaml` | `CHECKPOINTS` | W02.T06 recovery owner -> W05.T03 `W05_RETAINED_SCHEMA_CUTOVERS_READY` |
| `runtime.id_allocator` | `DEV/SCHEMAS/campaign-id-allocator-state.schema.json` + `GAME/SCHEMA/id_allocator.schema.yaml` | exceptional fixed `STATE/ID_ALLOCATOR.yaml` | W01.T04 `W01_NATIVE_ROUTING_READY`; W05.T02 final identifier integration |
| `runtime.maintenance_audit` | `DEV/SCHEMAS/runtime-maintenance-audit-state.schema.json` | `STATE/RUNTIME/MAINTENANCE_AUDITS` | W02.T06 `W02_EXACT_RECOVERY_READY` |
| `runtime.catalog_gap_report` | `DEV/SCHEMAS/runtime-catalog-gap-report-state.schema.json` | `STATE/RUNTIME/CATALOG_GAP_REPORTS` | W01.T08 gap producer -> W02.T05 `W02_DURABILITY_PUBLICATION_READY` -> W02.T06 `W02_EXACT_RECOVERY_READY`; W05.T02 final shared integration |

Every row is mandatory. None of these 17 current families has a no-durable-record disposition. A later accepted owner may supersede a surface only through an explicit row/proof update under the Version/System Impact process; missing realization is never silently converted to no-work. The natural owner supplies the complete native identity/state shape and executable producer/consumer behavior; the final writer integrates only its declared physical targets. Procedure-owned subtype shapes remain covered where applicable.

The proof consumer is W06.T02 `R018RuntimeFamilyProofTests` / `R018_RUNTIME_FAMILY_PROOF_READY`, also consumed by PG32. It validates each exact family/schema/root/realization tuple and all six negative cases specified there. Presence of 17 names, a world-only proof or a catalog-gap-only witness cannot substitute for this matrix. Owner-local family work remains independently eligible; only the affected final schema/root/identifier and proof joins order work.


## W05.T02 — Shared catalog, wrapper and identifier writer

Hard inputs: `W01_CATALOG_CONTEXT_READY`, `W02_CATALOG_BACKED_COMMAND_READY`, accepted adjudication basis and the source-native identifier checkpoints. Explicit join: `W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY -> JOIN_BEFORE_INTEGRATION -> W05.T02`. Consume the published W05.T01 inputs; do not require an integrated 17x17/R018 proof as an input.

Perform the one final shared integration of:

- catalog family/member census and strict binding references;
- wrapper dispatch for every 17+17 family;
- exact catalog generation/package/compatibility context;
- catalog gap-report family and evidence;
- source-native and campaign/native identifier policies;
- shipped adjudication/instruction consumers of the exact bound catalog context.

There is one shared catalog writer. Owner-local tasks supply deltas; none may edit a competing catalog copy after this checkpoint.

TDD and verification:

- complete the catalog-runtime integration classes from W01.T08;
- run `SharedCatalogIntegrationTests`, source-native identifier integration and catalog conformance;
- prove no name-only/default-latest binding, no catalog selected after command acceptance and no independent information-schema recreation.

Output checkpoint: `RD16_SHARED_MACHINE_INTEGRATION_READY`. It proves this final shared catalog/wrapper/identifier write. Final 17x17 and R018 integrated proof is downstream in W06.T02, after this checkpoint and the exact schema/realization checkpoints listed in the runtime-family matrix. A missing final proof cannot prevent publication of the GREEN producer it needs. Unrelated owner-local work does not wait for the whole wave.

## W05.T03 — Retained schema cutovers

Apply one final physical writer and one exact local-version transition for each breaking retained schema:

| Schema | Target transition | Required inputs |
|---|---:|---|
| checkpoint | 3 -> 4 | recovery/checkpoint + runtime closure |
| current_state | 2 -> 3 | temporal/currentness |
| thread | 1 -> 2 | thread/visibility/catalog |
| live_scene | 1 -> 2 | source-native LIVE/currentness |
| index | 1 -> 2 | native route/index/currentness |
| scene | 2 -> 3 | scene + LIVE route projection |
| location | 1 -> 2 | native location + routing |
| event | 1 -> 2 | mechanical/semantic event identity |
| lore | 1 -> 2 | information owner |
| player | 1 -> 2 | principal binding + collaboration strict state |
| campaign_manifest | 4 -> 5 | manifest membership retirement + bootstrap scaffold |

`session` remains version 1 unless the fresh implementation reveals and separately proves a breaking retained-shape change. Retire `pc.schema.yaml`, `npc.schema.yaml` and `item.schema.yaml` only in this final control-plane cutover, after `audit_engine.py` and every remaining legacy-schema consumer are reconciled; retired pc/npc/item/faction contracts get no terminal bump. Do not add migration, dual-read or deprecated aliases solely for unreleased pre-v1 shapes.

Integrate the durability/publication and recovery/currentness deltas to `GAME/SCHEMA/session.schema.yaml` once and close `SESSION_SCHEMA_FINAL_INTEGRATION_READY`; retaining schema version 1 requires proof that its accepted wire shape did not break.

TDD and verification:

- create/complete `DEV/TESTS/test_implementation_package_version_cutovers.py` with retained-schema exact-version and strict-shape assertions;
- prove all consumers/generators/fixtures use the same target and no old shape remains on a live path.

Output checkpoints: `W05_RETAINED_SCHEMA_CUTOVERS_READY` and `SESSION_SCHEMA_FINAL_INTEGRATION_READY`.

## W05.T04 — Shared README and physical-file integration

Fresh-read and integrate every GREEN semantic delta into the shared targets below. One task owns the actual bytes and closes the named checkpoint:

| Target | Required inputs | Checkpoint |
|---|---|---|
| `GAME/SCHEMA/README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots, temporal/current-state | `SHARED_SCHEMA_README_FINAL_INTEGRATION_READY` |
| `GAME/TEMPLATE/STORAGE_README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots | `SHARED_STORAGE_README_FINAL_INTEGRATION_READY` |
| scene schema | temporal + LIVE route/currentness | `SCENE_SCHEMA_FINAL_INTEGRATION_READY` |
| location schema | native location + routing | `LOCATION_SCHEMA_FINAL_INTEGRATION_READY` |
| player schema | principal route refs + collaboration strict state | `RD16_PLAYER_STRICT_STATE_INTEGRATION_READY` |

TDD and verification:

- static proof reads actual final bytes after every input is integrated;
- use `SharedSchemaStorageReadmeIntegrationProofTests` in `DEV/TESTS/test_implementation_proof_ledger.py`;
- prove all required semantic markers, current links and target versions, plus absence of old PLAYER/index, duplicate information-owner and incomplete operational-root text.

Output checkpoint: `SHARED_SCHEMA_STORAGE_README_PROOF_READY` after both README checkpoints.

## W05.T05 — Bounded campaign discovery, generator and blank scaffold

Hard inputs: `W01_CAMPAIGN_IDENTITY_READY`, `W01_SCAFFOLD_INPUT_CONTRACT_READY`, route/operational/LIVE companion contracts and final schemas/catalogs.

Implement:

- provider-independent bounded campaign candidate/page producer;
- bounded card hydration before `select_campaign`;
- continuation/narrowing or typed bounded inability when more campaigns remain;
- exact-selector direct routing;
- no ordinary exhaustive traversal of all campaign refs/cards;
- generator consumes the exact current schema/catalog inputs;
- blank scaffold contains every required owner-native root and completeness-protected companion, including operational roots;
- initial publication is idempotent and reconciles ambiguous acknowledgement.

TDD and verification:

- use `GeneratorScaffoldTests`, `InitialPublicationTests`, `FailureRetryTests`, `GeneratorConsumerProjectionTests`, `BlankScaffoldCompletenessTests` and `BoundedCampaignDiscoveryTests` in `DEV/TESTS/test_rd14_bootstrap.py`;
- cover multi-page/narrowing, exact direct selection, provider limitation, partial scaffold, duplicate creation and indeterminate publish.

Output checkpoints: `W05_BOUNDED_CAMPAIGN_DISCOVERY_READY` and `W05_BLANK_SCAFFOLD_READY`.

## W05.T06 — Onboarding, join/rejoin, retrospective and save/exit product paths

Implement the product-facing flows over the completed owners:

- progressive onboarding preserves the campaign selection barrier and canonical identity;
- creator binding uses verified stable account ID; login remains visible for selection and invitations;
- creator uncertainty or login rename does not transfer ownership and yields read-only/fail-closed behavior;
- multiplayer join/rejoin uses the principal route and exact PLAYER reload;
- ordinary retrospective routes to native history/Story/current permissions;
- save/exit uses the accepted durability promise and reports typed publication outcomes;
- failures/retries do not duplicate campaign, PLAYER, LIVE source or accepted mechanics.

TDD and verification:

- complete `CampaignSelectionBarrierTests`, `CreationIdentityTests`, `ProgressiveOnboardingTests`, `MultiplayerJoinRejoinTests`, `OrdinaryRetrospectiveRoutingTests`, `SaveExitMenuTests`, `CreatorAuthorityTests`, `ShippedBootstrapProjectionTests` and remaining bootstrap cases;
- include login display/invitation success, email rejection, login-only takeover rejection and legitimate stable-ID rejoin.

The earlier umbrella `ProductExitCreatorTests` is not recreated: its save/exit and creator fail-closed duties are discharged by the task-local `SaveExitMenuTests` and `CreatorAuthorityTests` at their coherent checkpoints.

Output checkpoint: `W05_PRODUCT_PATHS_READY`.

## W05.T07 — Campaign manifest v5 and membership retirement

At the final manifest/scaffold writer:

- remove obsolete `MANIFEST.players.player_ids`;
- retain `players.join_policy` under the campaign policy owner;
- keep campaign-card participant logins explicitly non-authoritative and display-only;
- route membership/authorization exclusively through exact current PLAYER plus principal companion;
- update generator, blank scaffold, validators, fixtures and consumers together;
- set `campaign_manifest.schema_version` to 5.

No migration/dual-read or compatibility alias is added solely for the removed pre-release field.

TDD and verification:

- extend manifest/scaffold and retained-version tests;
- statically reject any live consumer of `players.player_ids` and behaviorally prove join/rejoin through the current route.

Output checkpoint: `W05_CAMPAIGN_MANIFEST_V5_READY`.

## W05.T08 — Install, shipped CORE and exact module versions

Fresh-read and integrate owner deltas into each material module exactly once:

| Module | Target | Required semantic inputs |
|---|---:|---|
| BOOTSTRAP_RUNTIME | 1.0.9 | current transport/currentness + bounded bootstrap discovery |
| RANDOMNESS | 1.0.3 | fixed RNG acceptance/recovery |
| EXPLORATION | 1.0.2 | current exploration/domain cutover |
| STORAGE | 1.0.2 | routing/HOT + exact recovery/operational roots |
| SAVE_CONTRACT | 1.0.2 | durability promise/save-exit |
| PERSISTENCE | 1.0.4 | publication/recovery/currentness |
| CHRONOLOGY | 1.0.2 | temporal/thread/current-state |
| PROCESSES | 1.0.3 | procedure/continuation/operational roots |
| AI_REASONING | 1.0.4 | typed role/context/protected result |
| LIVE_SCENE | 1.0.4 | source-native LIVE/currentness/state |
| MULTIPLAYER | 1.0.8 | principal route + LIVE + collaboration/access reconciliation |
| CAMPAIGN_SETUP | 1.0.4 | identity/scaffold/onboarding |
| SESSION | 1.0.2 | exact session/campaign/LIVE/PLAYER handoff |
| PLAY_POLICY | 1.0.5 | exact accepted adjudication/access policy |
| CORE_INDEX | 1.0.2 | current module routing/versions |
| ADJUDICATION | 1.0.3 | bound catalog and accepted policy basis |

Shared physical checkpoints:

- integrate `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and `GAME/INSTALL/00_DND_BOOTSTRAP.md` at `RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION_READY`;
- integrate `GAME/CORE/BOOTSTRAP_RUNTIME.md` at `CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY`;
- integrate `GAME/CORE/STORAGE.md` at `CORE_STORAGE_FINAL_INTEGRATION_READY`;
- integrate `GAME/CORE/MULTIPLAYER.md` at `CORE_MULTIPLAYER_FINAL_INTEGRATION_READY`;
- integrate all other material CORE modules once with their listed owner inputs.

TDD and verification:

- use `InstallBootstrapSharedWriterTests` (`STATIC_AUDIT`) and `BoundedCampaignDiscoveryTests` (`FOCUSED_BEHAVIOR`);
- complete `CoreFrameworkModuleVersionCutoverTests` and the retained version suite;
- prove final install bytes contain no exhaustive all-campaign card loop, login-only authorization, generic PLAYER_INDEX authorization or stale v0.8 compatibility path.

After all module/schema/test paths are final, integrate their routes into `DEV/PROJECT_MAP.md` and all current/stale/schema/catalog/version/package assertions into `DEV/TOOLS/audit_engine.py`. Run the actual maintenance entry point after these edits; do not leave per-task partial writers.

Output checkpoints: `W05_SHIPPED_INTEGRATION_READY`, `PROJECT_MAP_FINAL_INTEGRATION_READY` and `MAINTENANCE_AUDIT_FINAL_INTEGRATION_READY`.

## Wave 05 completion evidence

Record the exact 17+17 census, actual shared-file bytes, every schema/module version, manifest field absence, blank-scaffold completeness, bounded discovery behavior and shipped consumer routing at the published HEAD. No owner-local delta may remain waiting outside the final physical writers when this wave closes.
