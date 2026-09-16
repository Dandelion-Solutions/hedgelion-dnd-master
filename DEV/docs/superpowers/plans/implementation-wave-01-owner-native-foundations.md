# HDM v1 Implementation Wave 01 — Owner-Native Foundations

Status: **PLANNED / BLOCKED ON INDEPENDENT SENIOR GO**

Goal: realize the owner-local contracts that later execution, LIVE, collaboration, Story, bootstrap and final-machine joins consume. This wave creates no alternate authority and does not publish shared physical files before their named final-writer checkpoints.

Use `implementation-plan-execution-contract.md` for every task. Wave order does not serialize independent tasks; a consumer may start as soon as its named checkpoint is GREEN and published.

## Entry and exit

Entry requires Senior GO at the exact implementation-start HEAD and fresh reads of every named owner. Exit requires the task checkpoints below, focused suites GREEN, owner projections synchronized and no unresolved System-Impact Gate.

Minimum wave impact envelope:

- owners: current shipped instructions, information/knowledge, Actor/Asset/Effect, routes/index/HOT/allocator, temporal/thread/current-state, role handoff, Context Runtime, native history/Story, catalog binding and bootstrap identity;
- consumers: Waves 02–05 and the Wave-06 proof package;
- protected invariants: one native owner per fact, bounded exact routing, no projection as authority, no v0.8 compatibility layer, no shared-file multi-writer;
- shared-file rule: produce bounded semantic deltas only for the final writers named in the execution contract.

## Baseline file-action manifest

These are the concrete source-HEAD actions. Fresh-read and reclassify a path before mutation as required by the execution contract; do not invent a parallel replacement when an accepted current path has advanced.

| Task | Direct action paths | Deferred shared/final paths |
|---|---|---|
| W01.T01 | `NEW_CREATE DEV/TESTS/test_rd01_shipped_projection_repairs.py`; inspect current `GAME/CORE/**`; produce bounded reconciliation/repair inputs for Wave-05 writers | `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/00_DND_BOOTSTRAP.md`, `GAME/CORE/BOOTSTRAP_RUNTIME.md`, `GAME/CORE/RANDOMNESS.md`, `GAME/CORE/EXPLORATION.md`; keep absent `GAME/CORE/DOMAIN_RULES_COVERAGE.md` absent |
| W01.T02 | `NEW_CREATE GAME/TOOLS/information.py`, `DEV/SCHEMAS/information-normalization-result.schema.json`, `world-lore-fact-state.schema.json`, `world-knowledge-state.schema.json`, `runtime-disclosure-state.schema.json`, `runtime-message-state.schema.json`, `DEV/TESTS/test_rd02_information_native_contracts.py`; modify `GAME/CORE/INFORMATION.md` | retained/legacy GAME schemas and both shared READMEs integrate at W05 |
| W01.T03 | `NEW_CREATE GAME/TOOLS/actor_continuity.py`, `GAME/TOOLS/continuity_projection.py`, `DEV/SCHEMAS/actor-assessment-request.schema.json`, `actor-delta-draft.schema.json`, `continuity-projection-candidate.schema.json`, `world-actor-state.schema.json`, `world-actor-group-state.schema.json`, `world-asset-state.schema.json`, `world-effect-state.schema.json`, `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`; create strict `GAME/SCHEMA/actor.schema.yaml`, `asset.schema.yaml`, `effect.schema.yaml`; retain superseded `pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml` as physical legacy residue until the Wave-05 final control-plane cutover | shared READMEs and legacy schema/audit-consumer retirement integrate at W05 |
| W01.T04 | `NEW_CREATE GAME/TOOLS/native_storage.py`, `id_allocator.py`, `hot_store.py`, `DEV/SCHEMAS/native-route.schema.json`, `campaign-id-allocator-state.schema.json`, `native-family-index.schema.json`, `native-owner-hot-envelope.schema.json`, `DEV/TESTS/test_rd04_native_routing_index_hot.py`; modify `GAME/SCHEMA/index.schema.yaml`, `id_allocator.schema.yaml`, `GAME/CAMPAIGN/STATE/ID_ALLOCATOR.yaml` | `GAME/SCHEMA/location.schema.yaml` and shared READMEs integrate at W05 |
| W01.T05 | `NEW_CREATE GAME/TOOLS/temporal.py`, `DEV/SCHEMAS/world-thread-state.schema.json`, `temporal-agenda-entry.schema.json`, `chronology-relation-evidence.schema.json`, `DEV/TESTS/test_rd08_temporal.py`; modify `DEV/SCHEMAS/temporal-binding.schema.json` only on focused RED | `current_state`, `thread`, `scene`, `event`, `GAME/CORE/CHRONOLOGY.md`, `GAME/CORE/PROCESSES.md` and schema README integrate at W05 |
| W01.T06 | `NEW_CREATE GAME/TOOLS/turn_runtime.py`, `emission.py`, `context_runtime.py`, `context_budget.py`; create `DEV/SCHEMAS/turn-envelope.schema.json`, `interpreter-result.schema.json`, `preparation-draft.schema.json`, `actor-proposal.schema.json`, `story-projection-draft.schema.json`, `narration-result.schema.json`, `context-need-profile.schema.json`, `context-trace.schema.json`; create both owner tests | `GAME/CORE/AI_REASONING.md`, `RUNTIME.md`, `PLAY_POLICY.md` are integrated/inspected at W05 |
| W01.T07 | `NEW_CREATE GAME/TOOLS/history.py`, `story.py`, `commentator.py`, `dramaturg.py`; create `DEV/SCHEMAS/runtime-semantic-event-state.schema.json`, `story-projection-state.schema.json`, `story-event-unit.schema.json`, `story-narrative-unit.schema.json`, `story-mechanics-unit.schema.json`, `semantic-event-t0-basis.schema.json`, `commentator-snapshot.schema.json`, `commentator-control-projection.schema.json`, `commentator-view.schema.json`, `dramaturg-horizon.schema.json`, `DEV/TESTS/test_rd13_story_t0_commentator.py`; create accepted scaffold paths under `GAME/CAMPAIGN/STORY/**` and the two Dramaturg template roots | `GAME/SCHEMA/event.schema.yaml` integrates at W05 |
| W01.T08 | `NEW_CREATE GAME/TOOLS/catalog_runtime.py`, `DEV/SCHEMAS/catalog-binding-request.schema.json`, `catalog-binding-result.schema.json`, `catalog-context-basis.schema.json`, `catalog-definition-dependency-ref.schema.json`, `runtime-catalog-gap-report-state.schema.json`, `DEV/TESTS/test_rd15_catalog_runtime.py`; inspect/reuse `GAME/TOOLS/ruleset_package.py` | catalogs/identifier policy and shipped instruction consumers integrate at W05 |
| W01.T09 | create the strict quiet-family `DEV/SCHEMAS/world-*-state.schema.json` inputs and `DEV/TESTS/test_rd16_world_family_machine_integration.py`; consume information/thread schemas from their owners | `world-record.schema.json`, shared catalogs/admission/inventory and conformance test integrate at W05 |
| W01.T10 | `NEW_CREATE GAME/TOOLS/bootstrap.py`, `DEV/SCHEMAS/bootstrap-request.schema.json`, `bootstrap-result.schema.json`, `campaign-selection-result.schema.json`, `DEV/TESTS/test_rd14_bootstrap.py`; inspect `GAME/TOOLS/init_campaign.py` | generator/scaffold, manifest, install and bootstrap CORE bytes integrate at W05 |

Required owner-local interface names remain stable through refactor:

```text
normalize_information_evidence(...) / normalize_live_material_evidence(...)
normalize_embedded_epistemic_input(...) / validate_knowledge_transition(...)
assess_actor(...) / validate_actor_delta(...) / apply_actor_delta(...)
build_continuity_source_bundle(...) / validate_continuity_projection(...) / classify_projection_compatibility(...)
route_native_record(...) / validate_loaded_identity(...) / load_campaign_allocator(...) / rebuild_family_index(...)
resolve_discovery_candidate(...) / allocate_and_stage_record(...)
stage_owner_document(...) / stage_allocator_state(...) / stage_index_delta(...)
clear_published_generation(...) / rebuild_helper(...)
evaluate_temporal_binding(...) / derive_temporal_dependency_keys(...) / materialize_due_occurrence(...) / rebuild_temporal_agenda(...)
start_turn(...) / bind_phase(...) / accept_phase_result(...) / advance_phase(...) / select_fallback(...)
validate_narration_result(...) / commit_visible_payload(...)
assemble_context(...) / discover_candidates(...) / resolve_candidate_basis(...) / estimate_size(...) / allocate(...)
validate_semantic_event_draft(...) / append_semantic_event(...) / build_t0_basis(...) / validate_t0_basis(...)
build_story_source_bundle(...) / project_story_window(...) / validate_story_projection(...)
bind_catalog_context(...) / bind_interpreter_candidate(...) / validate_executable_binding(...)
bind_executable_catalog(...)
```

## W01.T01 — Current shipped projections and negative reconciliation

Read the current architecture/spec owners and the shipped `GAME/**` surfaces named by R001, R003, R033, R043, R047, R048 and R050. Classify each existing file before editing.

Required behavior:

- prove only a current shipped contradiction at the implementation-start HEAD, then produce its exact bounded Wave-05 final-writer repair input/delta;
- retain fixed RNG semantics and the current clean-slate v1 transport/currentness rules;
- prove that the historical R047 path `GAME/CORE/DOMAIN_RULES_COVERAGE.md` remains absent and has no active contradictory consumer;
- do not recreate an absent module, add a compatibility alias or bump a version for a negative-only reconciliation.

TDD and verification:

- extend `DEV/TESTS/test_rd01_shipped_projection_repairs.py` with `CoreCurrentProjectionTests`, `DomainExplorationTests`, `InstallProjectionTests` and `RandomnessProjectionTests`;
- RED must identify the exact contradictory bytes or active stale consumer; GREEN proves the reconciliation/repair-input contract without changing a deferred final-writer surface;
- run the focused module and static absence/reference checks.

Output checkpoint: `W01_CURRENT_PROJECTIONS_READY` means reconciliation/repair-input readiness, not final shipped-byte integration. Bounded install and `BOOTSTRAP_RUNTIME` deltas flow to the Wave-05 final writers; current bytes are not edited twice.

## W01.T02 — Information, knowledge, disclosure and message ownership

Implement the strict native information contracts for `world.lore_fact` and `world.knowledge`, disclosure eligibility and recipient-safe message normalization. Knowledge must arise only from accepted native evidence; visibility, possession, narration and cache presence do not imply knowledge.

Required interfaces and laws:

- owner-native lore fact identity and immutable semantic content;
- knowledge provenance, subject/principal scope and exact currentness;
- disclosure result that carries the accepted source/provenance basis;
- recipient-specific message normalization with no cross-recipient leakage;
- deterministic rejection of missing, stale, unauthorized or ambiguous source evidence.

File actions are limited to current information schemas/owners and owner-local tests. Produce bounded deltas for `GAME/SCHEMA/README.md` and `GAME/TEMPLATE/STORAGE_README.md`; Wave 05 is their only final physical writer.

TDD and verification:

- use `DEV/TESTS/test_rd02_information_native_contracts.py`;
- retain `NativeInformationSchemaTests`, `InformationNormalizationTests`, `LegacyInformationProjectionTests` and `RecipientIsolationTests`;
- prove positive normalization plus negative visibility-to-knowledge and recipient-leakage cases;
- defer the LIVE normalization join to W03.T08 and strict shared-machine integration to W05.T01.

Output checkpoint: `W01_INFORMATION_OWNER_READY`.

## W01.T03 — Actor, Asset and Effect continuity

Implement the strict native Actor/Asset/Effect shapes, their assessment and mutation rules, and continuity admission. Provisional or projected entities cannot silently become native authority.

Required interfaces and laws:

- native Actor identity and state envelope;
- Asset ownership/location/status with exact source validation;
- Effect subject, lifecycle and accepted provenance;
- deterministic assessment and mutation outputs suitable for the execution carrier;
- explicit admission or rejection of legacy/provisional inputs, with no duplicate entity authority.

Produce only owner-local schema/code changes and bounded README/storage deltas. The three superseded PC/NPC/item schema files remain temporary physical legacy residue until the Wave-05 final control-plane cutover reconciles `audit_engine.py` and remaining consumers; new code must not use them as authority. Final shared documentation, wrapper/catalog integration and physical legacy retirement occur in Wave 05.

TDD and verification:

- use `DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`;
- retain `NativeActorShapeTests`, `ActorAssessmentBehaviorTests`, `ActorMutationIntegrationTests`, `ContinuitySourceAdmissionTests`, `LegacyEntityProjectionTests` and `ProvisionalActorConsumerTests`;
- cover accepted mutation, stale input, conflicting identity and failed provisional promotion.

Output checkpoint: `W01_ACTOR_ASSET_EFFECT_READY` requires current native Actor/Asset/Effect ownership and explicit legacy non-authority, not early physical retirement of the legacy schema bytes.

## W01.T04 — Native routes, allocator, index and HOT contracts

Create the bounded owner-native routing primitives used by later waves. Known identifiers must derive exact routes; index and HOT material are derived accelerators and cannot become authority.

Required interfaces and laws:

- deterministic native route derivation and validation;
- campaign-scoped allocator state with monotonic, collision-safe allocation;
- presence authority separated from index membership;
- native index entries that are revalidated by exact owner reads;
- HOT storage semantics and atomic owner mutation without a cross-owner transaction;
- fixed campaign-root selector and typed missing/stale/ambiguous outcomes;
- route-companion contract inputs for principal, LIVE and operational roots, without prematurely creating their later-wave authority.

TDD and verification:

- use `DEV/TESTS/test_rd04_native_routing_index_hot.py`;
- retain `NativeRouteTests`, `CampaignAllocatorTests`, `PresenceAuthorityTests`, `NativeIndexTests`, `NativeHotStoreTests`, `NativeAtomicityTests` and `FixedCampaignRootSelectorTests`;
- prove no broad scan or latest-looking record is an ordinary known-ID route.

Produce bounded schema/storage documentation deltas for Wave 05.

Output checkpoint: `W01_NATIVE_ROUTING_READY`.

## W01.T05 — Temporal, thread, current-state and chronology owner contracts

Implement owner-local temporal primitives before LIVE integration:

- strict current-state chronology and versioned current-state replacement;
- world-thread identity/state/visibility contract;
- temporal binding agenda and exact chronology bridge;
- bounded routing-completeness contract for every accepted temporal root;
- world-thread catalog alignment without making the catalog a chronology authority.

TDD and verification:

- use `DEV/TESTS/test_rd08_temporal.py`;
- retain `CurrentStateChronologyTests`, `WorldThreadContractTests`, `TemporalBindingAgendaTests`, `TemporalRoutingCompletenessTests`, `TemporalExecutionRecoveryTests`, `ChronologyBridgeTests`, `TemporalMachineAlignmentTests`, `WorldThreadCatalogAlignmentTests` and `Wp15TemporalProofTests`;
- in this task turn owner-local cases GREEN; recovery and LIVE handoff assertions become GREEN only in W02.T06 and W03.T06 respectively, in those owning tasks rather than as pre-published intentional failures.

Produce `RD08_SCHEMA_DOC_DELTA_READY` for the Wave-05 schema README writer.

Output checkpoint: `W01_TEMPORAL_OWNER_READY`.

## W01.T06 — Typed role handoff and bounded Context foundations

Implement the owner-local result envelopes that prevent role, tool, diagnostic and private-data bypass, plus bounded Context discovery/allocation primitives.

Role interfaces:

- typed handoff and turn envelope;
- protected-capacity accounting;
- protected emission with deterministic auxiliary fallback;
- explicit instruction owner and rejection of unowned emission.

Context interfaces:

- bounded discovery and eligibility;
- required packet closure before optional allocation;
- deterministic optional ranking within budget;
- scoped join and result trace that do not create gameplay truth;
- retrospective context remains a projection of native history.

TDD and verification:

- use `DEV/TESTS/test_rd10_role_emission.py` and retain `TurnEnvelopeContainmentTests`, `TypedHandoffTests`, `ProtectedCapacityTests`, `ProtectedEmissionTests`, `AuxiliaryFallbackTests`, `InstructionOwnerTests`;
- use `DEV/TESTS/test_rd11_context_runtime.py` and retain `ContextDiscoveryTests`, `ContextEligibilityTests`, `RequiredPacketClosureTests`, `ContextAllocationTests`, `OptionalRankingTests`, `RetrospectiveContextTests`, `ContextResultTraceTests`, `ScopedContextJoinTests`;
- integrated execution and collaboration/story cases are owned by Waves 02 and 04.

Output checkpoints: `W01_ROLE_CONTRACT_READY` and `W01_CONTEXT_OWNER_READY`.

## W01.T07 — Native history, Story root and static selection

Implement native semantic history authority and the owner-local Story projection boundary.

Required behavior:

- native semantic events are the history authority; Story is a projection;
- T0 basis is explicit and reconstructible from accepted native inputs;
- Story has a bounded physical root/selector and exact source currentness;
- Commentator input is self-contained and privacy-bounded;
- Dramaturg horizon/admission/rebase primitives never mutate history by narration alone.
- Owner-native Python ingress is the strict schema-version admission boundary: accept only a real integer `1`, reject `1.0`, `True`, strings, `null` and unsupported integers. Draft 2020-12 structural schemas may treat numeric `1.0` as integer-valued under their standard semantics; this task does not create a generic lexical schema validator.

TDD and verification:

- start in `DEV/TESTS/test_rd13_story_t0_commentator.py`;
- retain `NativeHistoryAuthorityTests`, `T0BasisTests`, `StoryProjectionTests`, `StoryT0MaterializationTests`, `CommentatorSelfContainedTests`, `DramaturgHorizonTests`, `HistoryProjectionSeparationTests`, `CompositeIntegrationTests`, `StoryStorageSelectorTests`, `StoryPhysicalRouteTests`, `DramaturgPublicationTests`, `DramaturgAdmissionTests`, `DramaturgRebaseTests`;
- this task turns owner-local identity/selection cases GREEN; W04.T07 owns the publication/integrated currentness cases.

Output checkpoint: `W01_HISTORY_STORY_OWNER_READY`.

## W01.T08 — Catalog context, binding and gap foundations

Implement the exact catalog-context carrier and deterministic binding/gap-report primitives consumed by execution and the final machine.

Required interfaces:

- `BoundCatalogContext` with exact catalog identity/generation/package/compatibility basis;
- candidate validation against the pinned context;
- typed gap report containing requested identity, context basis and deterministic reason;
- currentness validation and reconstruction inputs;
- no acceptance from name-only lookup, stale default or a catalog selected after mechanics were accepted.

TDD and verification:

- use `DEV/TESTS/test_rd15_catalog_runtime.py`;
- retain `CatalogContextBindingTests`, `CatalogCandidateValidationTests`, `CatalogGapReportTests`, `CatalogBindingCurrentnessTests`, `CatalogBindingIntegrationTests`, `CatalogContextBasisContractTests`, `CatalogGapContextEvidenceTests`, `CatalogBindingInstructionCutoverTests`, `CatalogBackedAcceptanceIntegrationTests`;
- owner-local context/candidate/gap cases close here; execution acceptance closes at W02.T01/W02.T03 and shipped/final integration at W05.T02.

Output checkpoint: `W01_CATALOG_CONTEXT_READY`.

## W01.T09 — Quiet world-schema and machine inputs

Implement owner-local strict schemas or deltas for the world families that do not depend on later runtime joins. The final family census remains exactly:

`world.actor`, `world.actor_group`, `world.asset`, `world.location`, `world.connection`, `world.zone`, `world.organization`, `world.contract`, `world.mission`, `world.scene`, `world.encounter`, `world.hazard`, `world.effect`, `world.lore_fact`, `world.knowledge`, `world.thread`, `world.player`.

`world.faction` remains an organization facet. W01.T02 exclusively owns `world.lore_fact` and `world.knowledge`; this task consumes those GREEN schemas and must not recreate them. `world.player`, shared wrappers/catalogs and cross-family dispatch wait for Wave 05.

Prepare owner-local assertions in `DEV/TESTS/test_rd16_world_family_machine_integration.py`, including `WorldStateSchemaCoverageTests`, `WorldFamilyCensusTests`, `WorldEnvelopeDispatchTests`, `DefinitionBindingModeTests`, `SharedCatalogIntegrationTests`, `PlayerCollaborationStrictStateIntegrationTests`, `WorldPlayerNativeIdentityTests` and `SourceNativeIdentifierPolicyIntegrationTests`. Publish no future-task failing tests.

Output checkpoint: `W01_WORLD_OWNER_INPUTS_READY`.

## W01.T10 — Early campaign identity and bootstrap request contract

Implement the campaign selection/creation boundary required before source-native LIVE identity can be accepted.

Required behavior:

- typed campaign selection barrier;
- canonical creation identity allocated before dependent roots or LIVE IDs;
- creator authority input carries verified stable GitHub account ID and current login separately;
- login is used for human-facing display/selection/invitations; email is not an identity source;
- login rename does not transfer creator or PLAYER authority; unresolved creator evidence fails closed to read-only;
- generator/scaffold input contract is bounded and contains all owner inputs, but final scaffold generation and install bytes wait for Wave 05.

TDD and verification:

- begin `DEV/TESTS/test_rd14_bootstrap.py` with `CampaignSelectionBarrierTests`, `CreationIdentityTests` and owner-local portions of `GeneratorScaffoldTests` and `CreatorAuthorityTests`;
- cover ambiguous/missing identity and prohibited login-only transfer;
- do not publish unfinished onboarding/join/save tests; their owning task is W05.T06.

Output checkpoints: `W01_CAMPAIGN_IDENTITY_READY` and `W01_SCAFFOLD_INPUT_CONTRACT_READY`.

## Wave 01 completion evidence

Record the exact published commits for every checkpoint, the focused GREEN commands, all bounded shared-writer deltas, version-impact dispositions and any still-dormant empirical trigger. Wave 02 may consume typed owner outputs after their checkpoint; Wave 05 alone integrates the shared physical files.
