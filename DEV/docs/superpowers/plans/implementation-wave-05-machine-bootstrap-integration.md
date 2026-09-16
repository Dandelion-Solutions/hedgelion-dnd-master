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

## W05.T01 — Final 17-world and 17-runtime machine

Hard inputs: all relevant owner checkpoints from Waves 01–04, especially information, Actor/Asset/Effect, temporal, PLAYER/collaboration, Story and LIVE source-native identity.

The final world census is exactly:

`world.actor`, `world.actor_group`, `world.asset`, `world.location`, `world.connection`, `world.zone`, `world.organization`, `world.contract`, `world.mission`, `world.scene`, `world.encounter`, `world.hazard`, `world.effect`, `world.lore_fact`, `world.knowledge`, `world.thread`, `world.player`.

The final runtime census is exactly:

`runtime.session`, `runtime.message`, `runtime.interaction`, `runtime.procedure`, `runtime.intent_plan`, `runtime.command`, `runtime.resolution`, `runtime.continuation`, `runtime.mechanical_event`, `runtime.semantic_event`, `runtime.resolution_trace`, `runtime.disclosure`, `runtime.collaboration_obligation`, `runtime.checkpoint`, `runtime.id_allocator`, `runtime.maintenance_audit`, `runtime.catalog_gap_report`.

Required integration:

- strict schemas for every family and exact wrapper dispatch;
- accepted definition-binding modes and shared catalog references;
- native PLAYER identity plus collaboration strict state;
- source-native identifier policy where required;
- information schemas consumed from W01.T02, never recreated;
- `world.faction` remains an organization facet and does not increase the count;
- runtime R018 closure covers all 17 runtime families.

TDD and verification:

- complete `DEV/TESTS/test_rd16_world_family_machine_integration.py` classes `WorldStateSchemaCoverageTests`, `WorldFamilyCensusTests`, `WorldEnvelopeDispatchTests`, `DefinitionBindingModeTests`, `SharedCatalogIntegrationTests`, `R018WorldFamilyProofTests`, `PlayerCollaborationStrictStateIntegrationTests`, `WorldPlayerNativeIdentityTests`, `SourceNativeIdentifierPolicyIntegrationTests`;
- run `DEV/TESTS/test_r2_7_wp03_catalog_conformance.py` after the shared catalogs exist;
- reject an eighteenth family, missing family, duplicate schema owner, loose additional-properties surface and mismatched identifier policy.

Output checkpoint: `W05_STRICT_17X17_MACHINE_READY`.

## W05.T02 — Shared catalog, wrapper and identifier writer

Hard inputs: `W01_CATALOG_CONTEXT_READY`, `W02_CATALOG_BACKED_COMMAND_READY`, accepted adjudication basis, W05.T01 owner inputs and the source-native identifier checkpoints.

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

Output checkpoint: `RD16_SHARED_MACHINE_INTEGRATION_READY`.

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

`session` remains version 1 unless the fresh implementation reveals and separately proves a breaking retained-shape change. Retired pc/npc/item/faction contracts get no terminal bump. Do not add migration, dual-read or deprecated aliases solely for unreleased pre-v1 shapes.

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
