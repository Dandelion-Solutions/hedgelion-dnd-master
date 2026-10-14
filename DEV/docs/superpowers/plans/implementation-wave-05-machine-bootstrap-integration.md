# HDM v1 Implementation Wave 05 — Machine, Bootstrap and Shared Integration

Status: **ACCEPTED BASELINE PRESERVED / COMPLETE LOCAL-SPELL EXTENSION — INDEPENDENT SENIOR PLAN GO / GLOBAL ACTIVATION OWNED BY `DEV/CURRENT_PROGRESS.md`**

Bounded auth/turn reconciliation in SP03 and its SP04 writer joins: **IMPLEMENTATION-PLAN REVIEW CANDIDATE / SENIOR PLAN GO PENDING**. Prior accepted work remains preserved; the older GO does not authorize this revised envelope.

Goal: integrate the completed owner contracts into the single strict 17-world/17-runtime machine, realize the accepted local339 spell profile over existing owners, complete bootstrap/product paths, and finish each shared physical integration through its one designated writer with owner-correct version cutovers.

Use `implementation-plan-execution-contract.md`. Fresh-read every shared file immediately before its final writer; integrate all required GREEN deltas in one checkpoint.

## Entry and exit

Entry requires every owner/join checkpoint named as an input below. Exit requires exact family census, strict schemas/catalogs, complete blank-scaffold/bootstrap paths, current shipped instructions and all retained schema/CORE version targets realized at one coherent HEAD.

W05.T06 has an additional task-specific gate: the accepted T06-A1 architecture
does not authorize its P0–P3 or held product-completion production tasks. Those
tasks remain held until this stable plan and its Impact Envelopes receive Senior
plan GO. T06-S1/S2 remain accepted and are not repeated.
The complete current plan gate is CLOSED by the independent Senior GO in `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/implementation-plan-senior-review.md`, reviewed head `d84c9a367d46f2f6e70bfa4baadac0914a2d19a9`; otherworker implementation is authorized only for tasks with their own accepted inputs. This control closure adds no task semantics or completed production claim.

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


## W05.T02-P0 — W03 source-native identifier-policy consumer cutover

System-Impact owner:
`DEV/docs/superpowers/design/2026-09-30-w05-t02-source-native-policy-consumer-senior-ruling.md`.

Hard inputs: accepted W03 `W03_SOURCE_NATIVE_LIVE_ID_READY` and its closed
scalar `live_birth` disposition table.

This is a bounded Wave-05 prerequisite with W03 LIVE semantic ownership. It
does not reopen Wave 03 and does not write the final shared catalog.

Direct writes:

- `GAME/TOOLS/live_state.py`;
- `DEV/TESTS/test_rd09_access_live.py`;
- mechanically required module-version/control bookkeeping.

Output checkpoint:
`W05_SOURCE_NATIVE_POLICY_CONSUMER_READY`.

Cut the LIVE consumer from the pre-final nested
`live_birth {disposition, encoding}` test/input shape to the accepted final
scalar disposition:

```text
SOURCE_NATIVE_LIVE | OWNER_EQUIVALENT | FORBIDDEN
```

For source-native allocation, scalar disposition must exactly match the local
closed W03 `LIVE_BIRTH_ADMISSION_TABLE`. Encoding remains fixed by
`SOURCE_NATIVE_LIVE_ENCODING == "framed_base32hex_v1"`; catalog/caller data
does not choose it. Keep exact family prefix validation. Do not add an adapter,
nested dual-read, compatibility alias or migration.

Mandatory REDs: scalar source-native row succeeds; missing/wrong scalar fails;
nested legacy row fails; forged scalar cannot admit owner-equivalent/forbidden
families; missing/invalid prefix fails; encoding remains owner-fixed; existing
ordering/cursor/CAS/ambiguous-publication/history witnesses remain GREEN.

Expected Version Impact: `live_state.py 1.0.21 -> 1.0.22`; final identifier
policy schema/catalog remain read-only in P0. Fresh Version Impact Gate,
independent review, clean broader verification, maintenance, non-force
publication and read-back are required.

## W05.T02 — Shared catalog, wrapper and identifier writer

Hard inputs: `W01_CATALOG_CONTEXT_READY`, `W02_CATALOG_BACKED_COMMAND_READY`, accepted adjudication basis, the source-native identifier checkpoints, and `W05_SOURCE_NATIVE_POLICY_CONSUMER_READY`. Explicit joins: `W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY -> JOIN_BEFORE_INTEGRATION -> W05.T02` and `W05.T02-P0 -> W05_SOURCE_NATIVE_POLICY_CONSUMER_READY -> W05.T02`. Consume the published inputs; do not require an integrated 17x17/R018 proof as an input.

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

Senior reconciliation:
`DEV/docs/superpowers/design/2026-10-01-w05-t03-retained-schema-final-writer-senior-ruling.md`.

Hard inputs are satisfied. T03 owns only retained schemas not assigned to a
later explicit final physical writer.

| Schema | Current -> T03 disposition | Required inputs |
|---|---:|---|
| checkpoint | 4 -> VERIFY ONLY / NO BUMP | accepted W02 recovery/checkpoint + runtime closure |
| current_state | 2 -> 3 | temporal/currentness |
| thread | 1 -> 2 | thread/visibility + accepted T02 catalog |
| live_scene | 1 -> 2 | source-native LIVE/currentness |
| index | 2 -> VERIFY ONLY / NO BUMP | accepted W01 native route/index + W03 currentness |
| event | 1 -> 2 | mechanical/semantic event identity |
| lore | 1 -> 2 | information owner |
| session | 1 -> final integrate; keep 1 unless breaking shape proved | durability/publication + recovery/currentness + accepted W04 session delta |

These shared targets are not T03 writers:

- `scene.schema.yaml` 2 -> 3 — W05.T04;
- `location.schema.yaml` 1 -> 2 — W05.T04;
- `player.schema.yaml` 1 -> 2 — W05.T04;
- `campaign_manifest.schema.yaml` 4 -> 5 — W05.T07.

Do not double-bump checkpoint or index. A new material change to either reopens
Version/System Impact.

Integrate durability/publication and recovery/currentness deltas to
`GAME/SCHEMA/session.schema.yaml` once and close
`SESSION_SCHEMA_FINAL_INTEGRATION_READY`; retaining version 1 requires proof
that its wire shape did not break.

Legacy `pc.schema.yaml`, `npc.schema.yaml`, `item.schema.yaml` and any
remaining retired-faction control-plane reference are retired only by W05.T08,
after final `audit_engine.py`, PROJECT_MAP and live-consumer reconciliation.

TDD and verification:

- create/complete `DEV/TESTS/test_implementation_package_version_cutovers.py`
  for T03-owned exact versions/strict shapes and verify-only checkpoint v4/index v2;
- prove all current consumers of T03-owned schemas use the final targets;
- do not publish RED tests for T04/T07/T08-owned future writes;
- do not add migration, dual-read or compatibility aliases for unreleased
  pre-v1 shapes.

Outputs:
`W05_RETAINED_SCHEMA_CUTOVERS_READY` and
`SESSION_SCHEMA_FINAL_INTEGRATION_READY`.

## W05.T04 — Shared README and physical-file integration

Fresh-read and integrate every GREEN semantic delta into the shared targets below. One task owns the actual bytes and closes the named checkpoint:

| Target | Required inputs | Checkpoint |
|---|---|---|
| `GAME/SCHEMA/README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots, temporal/current-state | `SHARED_SCHEMA_README_FINAL_INTEGRATION_READY` |
| `GAME/TEMPLATE/STORAGE_README.md` | information, Actor/Asset/Effect, routing/HOT, recovery/operational roots | `SHARED_STORAGE_README_FINAL_INTEGRATION_READY` |
| scene schema 2 -> 3 | temporal + LIVE route/currentness | `SCENE_SCHEMA_FINAL_INTEGRATION_READY` |
| location schema 1 -> 2 | native location + routing | `LOCATION_SCHEMA_FINAL_INTEGRATION_READY` |
| player schema 1 -> 2 | principal route refs + collaboration strict state | `RD16_PLAYER_STRICT_STATE_INTEGRATION_READY` |

TDD and verification:

- static proof reads actual final bytes after every input is integrated;
- use `SharedSchemaStorageReadmeIntegrationProofTests` in `DEV/TESTS/test_implementation_proof_ledger.py`;
- prove all required semantic markers, current links and target versions, plus absence of old PLAYER/index, duplicate information-owner and incomplete operational-root text.

Output checkpoint: `SHARED_SCHEMA_STORAGE_README_PROOF_READY` after both README checkpoints.

## W05.T05-P1 — Initial campaign publication capability

Senior architecture owner:
`DEV/docs/superpowers/design/2026-10-01-w05-t05-initial-campaign-publication-senior-ruling.md`.

This bounded prerequisite resolves the pre-campaign repository-write seam
without reopening W02 or moving initial creation into campaign-bound RuntimeHost.

Hard inputs:

- accepted W01 campaign/scaffold identity;
- accepted W02 publication/durability outcome semantics;
- accepted T05 bounded discovery output;
- exact selected storage repository + pinned storage default-branch HEAD;
- exact generated scaffold identity contract.

Implement a bootstrap-specific capability view over the same authenticated
RepositoryPort/deployment adapter. It must support exact repository/principal
identity, exact target-ref absence/presence, one tree built from scratch, one
single-parent initialization commit, distinct create-ref-if-absent, and bounded
post-attempt reconciliation.

Required authority sequence:

```text
freeze bootstrap identity + exact generated files
-> exact target campaign ref read
-> if absent: create tree FROM SCRATCH
-> create one initialization commit
     parent = pinned storage default-branch HEAD
-> create_ref_if_absent(target, commit)
-> reconcile accepted/rejected/conflict/indeterminate from exact ref authority
```

Do not use ordinary `update_ref` to create an absent ref. Do not compose a
synthetic campaign-bound RuntimeHost before campaign creation. Do not add an
alternate repository writer or a T05-private transport authority.

Use `GAME/TOOLS/bootstrap.py` and `DEV/TESTS/test_rd14_bootstrap.py` as the
direct implementation/test lane. RuntimeHost, publication.py and
policy_basis.RepositoryPort remain inspect-only unless a fresh test-first
contradiction returns the task to System Impact.

Output checkpoint:
`W05_INITIAL_CAMPAIGN_PUBLICATION_READY`.

The already accepted `W05_BOUNDED_CAMPAIGN_DISCOVERY_READY` is not reopened.
The held blank-scaffold slice resumes only after P1 independent PASS and
publication/read-back.

## W05.T05 — Bounded campaign discovery, generator and blank scaffold

Hard inputs: `W01_CAMPAIGN_IDENTITY_READY`, `W01_SCAFFOLD_INPUT_CONTRACT_READY`, route/operational/LIVE companion contracts and final schemas/catalogs. Bounded discovery may close independently; the blank-scaffold/initial-publication slice additionally requires `W05_INITIAL_CAMPAIGN_PUBLICATION_READY`.

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

## W05.T06-A1 — Accepted current-readiness and ordinary Master retrospective architecture

Accepted implementation-facing owner:
`DEV/docs/superpowers/specs/2026-10-02-w05-t06-readiness-retrospective-canonical-spec.md`.

Senior Review Stop 2: **GO / ARCHITECTURE ACCEPTED**, per
`DEV/docs/superpowers/design/2026-10-02-w05-t06-a1-review-stop-2-senior.md`.
The architecture gate is closed; the ruling requires no Product Owner decision.
This section records accepted architecture only. The implementation tasks and
their envelopes are below; the ruling is decomposition input, not an alternate
executable plan.

Preserve accepted T06-S1/S2. Story remains dormant and is not a baseline Master
retrospective dependency. Current native owners remain current truth; exact
NativeSemanticEvent/native evidence remains historical proof; current PLAYER,
knowledge, disclosure and access owners decide recipient eligibility. Context
keeps its admission/allocation policy. There is no new MASTER role, generic
search subsystem, campaign-wide history scan, readiness flag, persistent
readiness owner, additional serial LLM phase, or independent publication edge.
Story remains dormant. Revisit that choice only if measured native/index
discovery cannot satisfy bounded interaction cost without broad event-body reads,
or concrete product evaluation shows bounded Story orientation materially
improves navigation; neither trigger authorizes an adapter in this plan.

The source-owner composition and the P0–P3 dependency order below preserve the
accepted boundaries of Step-5.1, WP-11, WP-12, WP-14, WP-16, R2.3, WP-19,
S6D-07 and the existing RuntimeHost/History/Context/catalog implementations.

Each P0–P3 checkpoint and held product-completion checkpoint owns its RED/GREEN
tests and focused command below. Before publishing each checkpoint, follow the
package execution contract: compare actual impact to its Envelope, perform the
actual namespace-specific Version Impact Gate, complete task review, run the
applicable clean exact DEV and maintenance verification, publish non-force,
freshly read back the ref/changed paths, and update the cursor. A task does not
publish failing tests for a later task.

### W05.T06-P0 — Trusted HOT admission + RuntimeHost CurrentOwnerView

**Goal:** bind the real selected gameplay RuntimeHost to one trusted local HOT
capability and route authority-sensitive current reads through an operation-
scoped view without turning SQLite into another semantic authority.

**Files:**
- Create only if cohesion requires it: `GAME/TOOLS/current_owner.py` — transient
  establishment/read-session carriers shared by RuntimeHost and native owners.
- Modify: `GAME/TOOLS/runtime_host.py` — infrastructure-only HOT port,
  CurrentOwnerView/read-session, admitted-HOT registry, operation binding and
  current-owner service wiring.
- Modify: `GAME/TOOLS/hot_store.py` — detached requested-key snapshots,
  process-local admission bookkeeping, and trusted local/LIVE-adoption
  establishment entry points.
- Modify: `GAME/TOOLS/context_runtime.py` — current PLAYER/knowledge/
  disclosure/world reads use CurrentOwnerView rather than pinned Git directly.
- Modify: `GAME/TOOLS/bootstrap.py` — thread the infrastructure HOT capability
  through the existing selected-campaign `compose_selected_runtime_host(...)`
  path. Gameplay/model input cannot supply or replace it.
- Modify: `GAME/TOOLS/actor_continuity.py` — minimum trusted self-state
  reconsideration producer join, retaining owner-local validation.
- Modify: `GAME/TOOLS/turn_runtime.py` only for existing issued phase/basis
  provenance and exact current-phase consumption checks needed by that join.
- Modify: `GAME/SCHEMA/actor.schema.yaml` and
  `DEV/SCHEMAS/world-record.schema.json` — already-approved Actor revision
  envelope alignment moved here from P1A.
- Modify tests: RD04 HOT/index, RuntimeHost composition, RD11 Context, RD14
  selected-host composition, RD07 recovery and applicable owner-producer tests.

**Trusted interfaces and carriers:**

```text
HotOwnerStorePort.read_admitted_snapshot(
    campaign_id,
    owner_keys,
) -> HotOwnerReadSnapshot

HotOwnerReadSnapshot:
    campaign_id
    exact requested rows + explicit absent keys from one closed SQLite read
    admitted local generation/fingerprint for each present row
    ephemeral snapshot fingerprint/token; operational only

CurrentOwnerView.begin(basis: _OperationBasis) -> CurrentOwnerReadSession

CurrentOwnerReadSession.require(
    owner_keys: finite tuple[NativeOwnerRef, ...],
) -> CurrentOwnerObservation

CurrentOwnerObservation:
    operation_token
    complete bounded key union observed so far
    owner reads / explicit absences
    exact campaign/HOT/LIVE source bases per owner
    observation_fingerprint

CurrentOwnerRead:
    family_key, identity
    status: RESOLVED | ABSENT | INCOMPATIBLE | UNAVAILABLE | REVALIDATION_REQUIRED
    source: SELECTED_LIVE | ACCEPTED_HOT | PINNED_CAMPAIGN
    exact source/currentness basis
    immutable validated payload when resolved
```

HOT mutation APIs are infrastructure-only. An `OwnerDocument` is not authority
and cannot be supplied to CurrentOwnerView. The store marks a row admitted for
ordinary current reads only when trusted native-owner code reaches an accepted
WP12 establishment/adoption edge through the internal establishment API:

- **LOCAL_ESTABLISHED:** an owner-specific producer has already validated the
  native after-image and the exact predecessor/current-source basis; the local
  SQLite transaction is the WP12 establishment edge;
- **LIVE_ADOPTED:** an owner-specific consumer supplies exact accepted
  post-CAS LIVE evidence and after-image; pre-CAS prospective state is rejected;
- source-derived clean cache rows may be retained operationally but do not
  outrank the exact pinned source and need no separate semantic authority.

The admission marker is process-local operational evidence. After cold restart,
surviving dirty rows are not admitted merely by existence; recovery/revalidation
must re-establish a compatible current basis. Raw `source_basis` text,
generation, mtime or row presence never admits a row.

**Senior source/producer ruling — P0 GO:**

The bounded producer gap is confirmed and resolved as implementation allocation
under R2.2-13/16/17/20, R2.3-11/12, R2.4-14/17/20 and WP12-7/8.
Review provenance: `DEV/docs/superpowers/design/2026-10-03-w05-t06-p0-actor-producer-senior-ruling.md`.
`apply_actor_delta` remains a pure owner-local transformation. P0 now implements
its missing trusted caller; a phase-result seal proves phase provenance, not
semantic acceptance.

**Minimum producer/source path (no universal evidence issuer):**

- Add a fixed internal `ActorContinuityService.establish_from_phase(envelope,
  phase_result: AcceptedPhaseResult) -> ActorContinuityEstablishmentResult`
  through RuntimeHost. Native validation/application stays in
  `actor_continuity.py`; RuntimeHost composes currentness, access and HOT.
  Result statuses: ESTABLISHED | NO_CHANGE | UNSUPPORTED |
  REVALIDATION_REQUIRED. Return exact Actor before/after revision and established
  owner ref when applicable, never a writable after-image capability.
- Consume the existing TurnRuntime-issued `AcceptedContextBasis` and
  `AcceptedPhaseResult` for ACTOR/profile.actor/assess, bound to this Host,
  campaign, subject, turn and exact current phase assembly. The delta carries
  an explicit R2.2 assessment purpose. Reject raw dictionaries, another Host's
  ContextService, substituted bundles, old/rebound phases and caller evidence
  claims. Extend existing provenance checks only as needed for this join.
- P0's positive source is the same NPC's exact accepted current
  `world.actor` record containing a material
  `continuity.evolving.reconsideration_cues` entry. Bind
  `assessment.reconsider` and a bounded evolving-continuity proposal to that
  already-established cue. Own current state is eligible Actor evidence under
  R2.2; it does not prove external truth. Use the actual Actor native ID as the
  source ref, with its exact predecessor revision/fingerprint retained internally.
  No fabricated event or durable cue identity is allocated.
- Obtain the predecessor through CurrentOwnerView, require its inclusion in the
  accepted Actor Context basis, and revalidate exact owner payload/revision,
  source/routing, current phase and applicable access/subject authority before
  establishment. Deterministic native code constructs the legacy transformation's
  `source_evidence` mapping only after those checks; gameplay/model/tests cannot
  supply `accepted/current/authorized_actor_ids` as authority.
- P0 admits only this self-state reconsideration path. External facts/events,
  other Actors' private state, knowledge changes, foundation transitions and
  relationship updates are unsupported by this adapter. The pure validator's
  existing capabilities are not removed. Further source classes require their
  owning evidence/eligibility joins and envelope review, not a generic shortcut.
- Reject player-controlled/PC continuity authorship under the current Actor/
  control owner law. Preserve the full native envelope (including schema and
  definition anchor) when replacing only validated state/revision; do not stage
  the transformation's reduced Actor mapping as the complete stored record.
- For campaign-local SOFT state, revalidate the exact predecessor and admitted
  generations atomically with Actor after-image establishment; advance native
  `state_revision` once. Repeated consumption of the same phase result returns
  the established result/NO_CHANGE without another revision/write, using
  process-local consumption bookkeeping in the same establishment critical
  section. NO_CHANGE performs no semantic write. Failures roll back admission
  and bookkeeping with the row. No persistent receipt or generic pending owner.
- This local producer cannot mutate a LIVE-selected Actor. Return typed
  UNSUPPORTED/revalidation without staging prospective state. Existing P0
  post-CAS adoption plumbing remains separate and requires real accepted LIVE
  evidence. No new LIVE mutation/CAS workflow is created.
- Close external source/access revalidation before the SQLite transaction, then
  compare the retained operation basis and predecessor under the local critical
  section. No model, player or repository exchange occurs inside it.

Move the already-approved SP06-10 Actor-envelope `state_revision` alignment
from P1A into P0: `GAME/SCHEMA/actor.schema.yaml` and
`DEV/SCHEMAS/world-record.schema.json`, plus exact validation/projection tests
and mandatory Version Impact synchronization. Require an explicit compatible
native revision; do not fabricate zero from missing legacy state. This is the
existing Actor revision, not a new generic world-family revision. P1A consumes
this GREEN contract and does not repeat its version bump.

**Producer acceptance cases:** real selected Host -> native current NPC cue ->
Context ACTOR rebind -> issued proposal -> deterministic native validation ->
atomic HOT establishment -> fresh Context read sees the successor before SAVE.
Test changed/missing cue, revision/source movement, stale/rebound/foreign phase,
forged evidence flags, raw after-image, PC agency, external-source proposal,
LIVE-selected owner, NO_CHANGE, repeat consumption, rollback, preserved envelope
and cold restart. Source fixtures may represent native repository bytes; they
must traverse production admission and may not pre-issue an acceptance carrier
or monkeypatch semantic acceptance. RD03's synthetic evidence remains unit
transformation coverage only.

**Bounded expanding-read coherence:**

A CurrentOwnerReadSession may discover more owner keys while closing a request.
Every expansion reacquires the **full accumulated key union** from one closed
SQLite snapshot; previously derived results are invalidated/recomputed against
that union. The final observation revalidates the full union, including explicit
absences and admitted generation/fingerprints. If any retained row/absence or
relevant selected source/routing basis changed, return
`REVALIDATION_REQUIRED`; do not mix snapshots. No remote/LIVE/repository I/O
occurs while a SQLite transaction is open. The dependency closure is finite
under its consuming owner; no retry loop or campaign-global generation/frontier
is introduced.

**Steps and checks:**
0. Fresh-read this Senior-approved producer/source path and revised Envelope;
   P0 is authorized. Record the exact implementation-start HEAD.
1. RED: selected product host lacks the trusted HOT capability; Context after a
   real accepted local Actor change still sees pinned Git; forged/surviving raw
   rows and cross-campaign rows must fail.
2. RED: dependency closure expands between Actor and a second owner while the
   first HOT row changes; mixed observation must be rejected.
3. Implement the bounded Actor producer/revision alignment above with trusted
   HOT composition/admission and operation read sessions;
   thread the capability through `compose_selected_runtime_host`.
4. Cut Context current-family resolution to the view while preserving existing
   eligibility and selected-LIVE revalidation.
5. GREEN: the Senior-approved accepted native producer yields a real local
   after-image visible before SAVE; forged raw rows and synthetic evidence-only
   witnesses do not qualify; cold recovery does not resurrect stale dirty
   state; expansion either returns one compatible union or typed revalidation
   failure.
6. Run the focused and cross-owner checks below, then Version Impact Gate,
   task review, full clean DEV/maintenance verification and remote read-back.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd14_bootstrap.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd10_role_emission.py
```

**Output:** `W05_T06_CURRENT_OWNER_VIEW_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§2–4, 20; Review Stop 2; Step-5.1;
  WP-12/WP-14/WP-16; R2.3; current native Actor/PLAYER/information owners.
- BASELINE REF OR SHA: fresh exact public HEAD after final repaired-plan Senior
  GO; record implementation-start SHA before RED.
- EXPECTED OWNERS TO CHANGE: RuntimeHost/current-owner/HOT infrastructure,
  Context current reads and selected-product bootstrap composition; bounded
  Actor self-state producer/phase join and Actor-envelope revision alignment
  specified above. No universal evidence issuer.
- EXPECTED CONSUMERS TO CHANGE: RuntimeHost fixed service composition,
  Context current-family resolution and bootstrap's selected gameplay host.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: trusted infrastructure HOT port,
  process-local admitted-establishment bookkeeping, operation-scoped
  read-session/results, fixed internal Actor phase-consumption service and the
  trusted compose-selected-host argument; Actor-specific revision envelopes.
  No public gameplay/model raw mutation/service-injection capability.
- PROTECTED ARCHITECTURE INVARIANTS: one semantic owner; LIVE-first exact
  currentness; no pre-CAS state; HOT only after native-owner validation + WP12
  establishment/adoption; no caller-asserted evidence as acceptance; no remote
  I/O in SQLite transactions; no stale restart resurrection; dynamic closure
  cannot mix snapshots; Context retains information/access eligibility.
- ARCHITECTURE-SENSITIVE SURFACES: RuntimeHost composition; SQLite transaction
  scope; current-source precedence; selected LIVE routing; cold recovery;
  Context source eligibility; same-campaign namespace isolation.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: a focused Actor producer
  test that traverses the Senior-approved accepted-source path and WP12
  establishment join (RD03 alone is transformation evidence, not producer
  acceptance); RD04 HOT snapshot/admission; RuntimeHost composition; RD11
  Context; RD14 selected product host; RD07 recovery; RD09 LIVE.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: character build semantics (P1A),
  readiness derivation (P1B), History discovery (P2), Story, persistent
  campaign schema/catalog expansion beyond the listed Actor revision alignment,
  migration, publication timing, general cognition evidence issuance, new Actor
  semantic authority, and LIVE mutation production.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify actual
  changed GAME modules and Actor-envelope schema alignment under current owning
  bump rules. Synchronize affected projections in this checkpoint; no automatic
  campaign/catalog-generation bump or migration is inferred.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: exact current progress/cursor; stable
  plan/index; T06-A1/Review Stop 2; Step-5.1; WP12/14/16; R2.3;
  RuntimeHost/HOT/Context/bootstrap/actor-continuity/TurnRuntime code; issued
  phase carriers; Actor envelope contracts; RD03/04/07/09/11/14 and TurnRuntime;
  current versioning policy/owner.

### W05.T06-P1A — Production character materialization resolver

**Dependencies:** `W05_T06_CURRENT_OWNER_VIEW_READY`, `W05_FULL_SRD_SPELL_PACKAGE_READY` and `W05_SORCERER_ACQUISITION_CONTEXT_READY` from SP29. All must be actually realized, independently reviewed, published and read back; accepted architecture/data-only rows do not replace these inputs.

**Goal:** realize the already-accepted S6D-07/DIEGETIC_ONBOARDING production
resolver that turns accepted typed character anchors/selections into validated
native PC Actor/Asset state and establishes those after-images in HOT. Without
this producer, progressive onboarding could only report “not ready” and could
not converge to READY_PC.

**Files:**
- Create: `GAME/TOOLS/character_progression.py` — typed initial materialization
  request/result and deterministic S6D-07 resolver.
- Modify: `GAME/TOOLS/runtime_host.py` — bind one admitted
  `BoundCatalogContext` at trusted infrastructure composition and expose the
  fixed character-materialization service.
- Modify: `GAME/TOOLS/bootstrap.py` — selected product host receives the
  already-resolved `BoundCatalogContext`; no ambient/default catalog choice.
- Modify: `GAME/TOOLS/hot_store.py` / current-owner internal carrier only as
  needed for the owner-specific character establishment join selected in P0.
- Consume the GREEN P0 native Actor envelope/revision contract. SP06-10 schema
  alignment is owned by P0; P1A does not repeat it or its version bump.
- Consume: `GAME/TOOLS/id_allocator.py` and the current native allocator/
  identifier-policy contracts for new campaign-owned starting Assets. Modify
  only the minimum owner-specific integration needed to stage allocation with
  the P1A HOT batch; no second allocator or new identity policy.
- Consume: `GAME/TOOLS/character_spell_acquisition.py` from SP27 and SP29's exact validator/seed/adoption promotion; do not reimplement selected-union arithmetic or source eligibility.
- Create: `DEV/TESTS/test_character_progression.py`; extend RuntimeHost/RD14,
  RD04 allocator/HOT and native Actor schema/continuity tests.
- Inspect/consume only: S6D-07 owner/seed, Character Readiness,
  Actor/Asset/Effect/health/resource owners, catalog_runtime/ruleset_package and
  DEV conformance tool/fixtures.

**Interfaces:**

```text
CharacterMaterializationRequest:
    actor_ref: exact current PC Actor
    player_ref: exact current active PLAYER expected to control actor_ref
    accepted build anchors / explicit selections already interpreted by the
      existing semantic boundary
    selection_basis per accepted S6D-07 vocabulary
    no raw prose authority, no arbitrary owner after-images

CharacterProgressionService.materialize_initial(
    request: CharacterMaterializationRequest,
) -> CharacterMaterializationResult

CharacterMaterializationResult:
    status: ESTABLISHED | UNRESOLVED_MATERIAL_CHOICE | UNSUPPORTED | REVALIDATION_REQUIRED
    actor_id, player_id
    exact before/after Actor revision when established
    established native owner refs/generations
    deterministic blocker/question descriptors
    exact catalog/ruleset context identity
```

The service validates current Actor + active PLAYER/control through P0, validates
all selected definitions/options against the Host-bound `BoundCatalogContext`,
applies deterministic inheritance/defaults permitted by S6D-07, and creates the
minimum supported Actor/Asset after-images. Concept inference/semantic player
choice remains upstream LLM/Interpreter work; the deterministic resolver only
validates the proposed rules-valid anchor/selection and never infers mechanics
from prose by itself. If materially different legal choices remain unresolved,
it returns the bounded blocker/question descriptor and performs no mutation.

An established result writes the complete owner after-image batch through P0's
trusted HOT establishment boundary in one local transaction. New campaign-owned
starting Assets use the existing campaign allocator and current identifier
policy; the exact allocator after-image joins Actor + Asset creation in that
same transaction. Revalidate the predecessor owner/allocator generations at
local establishment; movement fails boundedly without a partial grant. Existing
Assets and already accepted grants retain their native identities.

Repeat/resume of the same accepted initial materialization recognizes the
already-established native build/grants instead of allocating again, resetting
current HP/resources/equipment, reopening choices or advancing Actor revision
solely for a no-op. A material correction or later acquisition follows its
existing owner transition; this initial resolver does not invent a durable
receipt, pending-work owner or compatibility path. Failure before establishment
leaves Actor, Assets and allocator unchanged.

The resolver does not SAVE, publish, declare READY_PC or create a new lifecycle
state. Unsupported content is absent/nonselectable.

Sorcerer choices consume the admitted SP27/SP29 source-owned acquisition contract: exact16 cantrip/21 level1 SRD subsets plus only individually proved named existing extras; four cantrip selections and two level1 selections; known_spell_ids equals the union of all six selected grants and prepared_spell_ids equals exactly the selected two level1 grants. Derive complete required Activities from selected option union, never options[0]/activity_ids[0]. Preserve spell_selection_binding_mismatch rejection. One starting Arcane Focus is granted once through its deterministic slot, never per selected cantrip. Preserve lawful existing defaults and exact prior-context choices; any necessary lawful-extra default/adoption repair is explicit before offering the new context. Acquisition requires installed support, not every prepared spell's target/current material availability; actual cast preflight owns those situational conditions. An explicit Sorcerer alternative is proved using actual supported options before READY_PC.

The Host-bound catalog context is an already admitted `BoundCatalogContext`
from `catalog_runtime.bind_catalog_context`; RuntimeHost never constructs an
ambient default. Its catalog generation/ruleset digest/fingerprint and relevant
campaign definition frontier are revalidated for each operation. Stale or
foreign context produces typed rebind/currentness failure.

**Acceptance:** positive Human/Criminal Fighter and Sorcerer initial paths under the actual SP29 adopted package,
delegated deterministic defaults, one unresolved material choice, explicit
player override, same Actor ID/state-revision advance, exact current PLAYER
control, unsupported content, forged selection, wrong-host/stale catalog and
HOT before-SAVE visibility. Also prove allocator + Actor + Asset atomicity,
failure rollback, overlapping allocator movement, repeated/resumed initial
materialization with no duplicate IDs/grants, and preservation of already
accepted choices/current resource values. No questionnaire behavior is
implemented in this deterministic service.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_character_progression.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd14_bootstrap.py
```

**Output:** `W05_T06_CHARACTER_MATERIALIZATION_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: S6D-07 Character Progression/READY_PC Seed plus accepted 2026-10-04 content/acquisition annex and actual SP27/SP29 outputs,
  DIEGETIC_ONBOARDING, T06-A1 current-owner laws, Review Stop 2.
- BASELINE REF OR SHA: fresh implementation entry after actual accepted P0/SP29 output read-back; preserve earlier P0 schema transition.
- EXPECTED OWNERS TO CHANGE: new production character-progression resolver;
  RuntimeHost/catalog composition; bootstrap trusted catalog composition;
  P1A-specific HOT establishment/allocator producer join; consume P0's
  accepted Actor-envelope revision contract.
- EXPECTED CONSUMERS TO CHANGE: progressive onboarding product path later in
  T06; P1B readiness; RuntimeHost composition tests.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: typed materialization request/result,
  fixed RuntimeHost character-progression service and trusted Host-bound
  BoundCatalogContext. No raw prose/owner-after-image/catalog service injection.
- PROTECTED ARCHITECTURE INVARIANTS: same PC Actor ID; player-owned choices and
  accepted selection-basis precedence; deterministic grants/defaults only;
  exact current PLAYER control; exact catalog/ruleset context; unsupported
  content absent/nonselectable; one atomic local HOT establishment; no READY_PC,
  SAVE or PLAY_READY side effect; native campaign allocation co-established
  with new Assets; no duplicate grants, resource reset or situational reselection
  on repeat/resume.
- ARCHITECTURE-SENSITIVE SURFACES: Actor/Asset native after-images, catalog
  context/current definition frontier, player agency, HOT atomicity, S6D package
  breadth and same-Actor promotion.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: new character progression
  suite; S6D-07 conformance; RD03 Actor/Asset/Effect; RD15 catalog; RuntimeHost
  composition; RD14 bootstrap; RD04 allocator/HOT atomicity, retry and
  predecessor-movement witnesses; P0 HOT witnesses.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: additional D&D content outside the accepted SP29 package, generic concept NLP,
  Activity execution/RNG, readiness verdict (P1B), History/Story, publication,
  migration, new mechanics primitive/selector/accessor.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: run exact Version
  Impact Gate on new/changed GAME modules. Actor `state_revision` envelope
  alignment and its version synchronization are P0-owned; implementation
  must make those machine contracts agree. Do not preselect the exact schema/
  campaign-contract transition or migration disposition before rereading the
  current pre-release/version owner.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0 output/cursor; S6D-07,
  DIEGETIC_ONBOARDING/CHARACTER_READINESS; Actor/Asset/Effect/health owners;
  id_allocator/native identity policy and current allocator source;
  catalog_runtime/ruleset_package/MechanicalContext; current package seed and
  capability file; RuntimeHost/bootstrap; relevant tests and version owner.

### W05.T06-P1B — Production deterministic readiness

**Dependencies:** `W05_T06_CURRENT_OWNER_VIEW_READY`,
`W05_T06_CHARACTER_MATERIALIZATION_READY` and SP29's `W05_FULL_SRD_SPELL_PACKAGE_READY` / `W05_SORCERER_ACQUISITION_CONTEXT_READY` as the exact adopted context used by P1A. Preserve all selected all-mode/transitive support proof when deriving local/readiness dependencies.

**Goal:** expose local mechanical sufficiency and canonical READY_PC as distinct
deterministic RuntimeHost assessments over the same current Actor/PLAYER/native
owners and Host-bound catalog context.

**Files:**
- Create: `GAME/TOOLS/character_readiness.py`.
- Modify: `GAME/TOOLS/runtime_host.py` — fixed readiness service over P0 and
  the P1A Host-bound catalog context.
- Create: `DEV/TESTS/test_character_readiness.py`.
- Inspect/consume: P1A result, S6D-07, Character Readiness, MechanicalContext,
  selector/activity/catalog/native owners and conformance fixtures.

**Interfaces:**

```text
ReadinessService.bind_local_dependency_set(
    actor_ref: NativeOwnerRef,
    player_ref: NativeOwnerRef,
    executable_binding: exact admitted catalog/activity binding,
    invocation_binding: accepted typed invocation/mechanic binding,
) -> BoundMechanicalDependencySet

BoundMechanicalDependencySet:
    RuntimeHost-issued; same operation token
    actor_ref + current actor_state_revision
    player_ref + proven current control of actor_ref
    catalog_context_fingerprint + ruleset identity
    exact mechanic/use-case identity
    finite owner/accessor/selector/activity dependencies derived from admitted
      definitions/bindings; never caller-authored arbitrary lists

ReadinessService.assess_local_sufficiency(
    dependency_basis: BoundMechanicalDependencySet,
) -> LocalMechanicalSufficiency

ReadinessService.assess_ready_pc(
    actor_ref: NativeOwnerRef,
    player_ref: NativeOwnerRef,
) -> ReadyPcAssessment
```

`bind_local_dependency_set` is the only issuer. It validates the executable
binding with the existing catalog owner, derives finite required engine-state
dependencies from admitted Activity/definition/MechanicalContext metadata and
P0 current owners, and does not execute the mechanic, mutate state or draw RNG.
A forged/wrong-host/stale dependency carrier is rejected.

`assess_ready_pc` explicitly resolves both Actor and PLAYER through P0 and
requires the active PLAYER to control the Actor; no reverse PLAYER scan/index
inference is allowed. The result binds actor/player current bases plus
catalog_generation, ruleset_set_digest_generation, ruleset_set_sha256 and
reconstructive derivation evidence. READY_PC remains transient and does not
publish, SAVE or establish PLAY_READY.

Tests cover P1A-produced Fighter/Sorcerer builds, local-sufficiency vs READY_PC,
wrong PLAYER/control, unresolved initial choices, future acquisition choices,
stale Actor revision/catalog, forged dependency set, missing transitive owner,
unsupported content and wrong-host carrier.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_character_readiness.py DEV/TESTS/test_character_progression.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_runtime_host_composition.py
```

**Output:** `W05_T06_PRODUCTION_READINESS_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§5–7; S6D-07; CHARACTER_READINESS;
  MechanicalContext/selector/Activity contracts.
- BASELINE REF OR SHA: accepted P1A output SHA after fresh read-back.
- EXPECTED OWNERS TO CHANGE: new production readiness module and RuntimeHost
  readiness service wiring only.
- EXPECTED CONSUMERS TO CHANGE: held T06 progress_onboarding/product readiness;
  P1A-produced builds; readiness-focused RuntimeHost tests.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: Host-issued
  BoundMechanicalDependencySet, LocalMechanicalSufficiency and
  ReadyPcAssessment; explicit Actor+PLAYER refs. No caller-authored dependency
  list or reverse PLAYER discovery.
- PROTECTED ARCHITECTURE INVARIANTS: local sufficiency != READY_PC != PLAY_READY;
  active current PLAYER controls Actor; exact Actor revision/current basis;
  exact catalog/ruleset identity; admitted mechanical dependencies only; no
  execution/RNG/mutation while assessing; transient evidence only.
- ARCHITECTURE-SENSITIVE SURFACES: mechanical dependency closure, player
  binding, catalog freshness, current-owner snapshot, unsupported content and
  resume/rejoin reevaluation.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: new readiness suite; P1A
  character progression; S6D-07; RD03; RD15; RuntimeHost composition; selector/
  MechanicalContext/Activity contract suites.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: character semantic choices/content,
  new selectors/accessors/primitives, persistent ready state, save/publication,
  lifecycle mutation, History/Story, migration.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: run exact module
  Version Impact Gate. No persistent schema/catalog/checkpoint/migration change
  is pre-authorized.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0/P1A outputs/cursors; T06-A1;
  S6D-07/CHARACTER_READINESS; Actor/PLAYER/Asset/Effect; current Actor envelope
  schemas/continuity tests; catalog/runtime package;
  MechanicalContext/selectors/Activities; relevant tests and version owner.

### W05.T06-P2 — Bounded native History discovery and enrollment

**Dependency:** `W05_T06_CURRENT_OWNER_VIEW_READY`. P2 is independent of P1A/
P1B semantically. Eligible lanes may prepare in parallel only with isolated/disjoint physical writers; shared-file integration and publication remain serialized under the execution contract.

**Goal:** realize only WP19-L36 bounded SemanticEvent discovery using the
existing EVENT_INDEX artifact plus accepted unpublished HOT and selected LIVE
event evidence.

**Bounded technical allocation:** campaign/selected-LIVE preparation is eligible
now. The complete local-HOT producer arm consumes the actual SP04 native segment
kernel and its kernel-derived strict SemanticEvent establishment, not P0's
Actor-only producer or raw event staging. This holds full P2/P3, not independent
preparation; P2 does not wait for SP28, whose Wish/History integration consumes
accepted P2. Independent ruling/review evidence:
`DEV/docs/superpowers/design/2026-10-06-p2-origin-and-producer-allocation.md`.
Preserve origin-local `semantic_order == admission_ordinal`; campaign index
`ordinal` is routing position. EVENT_INDEX retains `source_origin`, native
admission ordinal and exact LIVE source binding through absorption, with bodies
unchanged and source-anchor retention qualified separately from derived hints.

**Files:**
- Modify: `GAME/TOOLS/history.py`, `runtime_host.py`, `hot_store.py`.
- Modify named accepted event producers/joins only as required:
  `durability.py`, `publication.py`, `live_state.py`, `collaboration.py`.
- Modify: `GAME/TOOLS/init_campaign.py` and
  `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml`.
- Create: `GAME/SCHEMA/event_index.schema.yaml` — strict contract for the
  already-existing EVENT_INDEX/event-enrollment artifact.
- Modify: `GAME/SCHEMA/README.md` to route EVENT_INDEX to that contract.
- Modify: `DEV/SCHEMAS/runtime-semantic-event-state.schema.json` only for
  accepted optional `semantic_delta.discovery_refs`.
- **Do not repurpose `GAME/SCHEMA/index.schema.yaml`**: it remains the generic
  `native_family_index` contract unless fresh owner evidence independently
  proves a shared shape.
- Modify RD04/RuntimeHost/RD13/RD09/RD06/RD14 and schema/template tests.

**Event-index contract:**

```text
EVENT_INDEX:
    schema_version
    entity_type: EVENT
    complete: true
    upper_ordinal: integer | null
    entries[]:
        ordinal
        event_id
        exact path/route as applicable
        discovery_refs[]: index-safe typed native owner refs only
```

Version Impact determines the exact schema-version transition/start; the plan
does not pre-authorize a bump or migration. The blank scaffold represents a
complete empty enrollment with `upper_ordinal: null`.

**Interfaces:**

```text
HistoryService.discover(request) -> HistoryDiscoveryResult

HistoryDiscoveryRequest:
    selector: exact event/source | typed current-owner | accepted session |
              recent-tail | eligible provenance/source ref
    max_candidates: positive finite bound

NativeHistoryCandidate:
    event_id
    source origin/ref/revision
    source-local admission ordinal
    exact known-ID route
    index-safe nomination refs

HistoryDiscoverySourceBasis:
    origin/ref/revision + exact campaign/HOT/LIVE currentness evidence

HistoryDiscoveryResult:
    operation_token
    candidates: bounded tuple[NativeHistoryCandidate, ...]
    contributing_source_bases: bounded tuple[HistoryDiscoverySourceBasis, ...]
    status: MATCHED_BOUNDED_INTERVAL | NO_INDEXED_CANDIDATE |
            TYPED_INCOMPLETE | UNAVAILABLE | REVALIDATION_REQUIRED
    limit_applied
```

There is no singular source basis for a result that may combine campaign, HOT
and selected LIVE candidates. Each candidate retains its own exact source and
exact shortlisted reads revalidate that source.

Producer joins:
1. accepted local runtime.semantic_event establishment validates
   `discovery_refs` and atomically updates the P0-admitted HOT event helper;
2. campaign durable event publication submits event + EVENT_INDEX after-image in
   the existing W02 closure;
3. selected LIVE pack/CAS keeps prospective data non-current; accepted source
   metadata participates only from the exact selected source;
4. absorption constructs the campaign EVENT_INDEX after-image in the same
   absorption closure and deduplicates by exact native event evidence, never ID
   magnitude/order.

EVENT_INDEX/HOT helper contains routing IDs only—no prose, motive, T0 value,
knowledge/disclosure state or raw event body. Missing/invalid coarse metadata is
not absence proof; independently known exact event IDs may bypass it. No
campaign-wide body scan, raw-text/regex/embedding search, arbitrary predicate,
global relevance graph or unbounded pagination exists.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd14_bootstrap.py
```

**Output:** `W05_T06_NATIVE_HISTORY_DISCOVERY_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§9–13, 18–20; WP19 L29–L38; WP11/WP12/
  WP13/WP14/WP16; current History/SemanticEvent owners.
- BASELINE REF OR SHA: accepted P0 output SHA after fresh read-back.
- EXPECTED OWNERS TO CHANGE: History/SemanticEvent discovery realization,
  RuntimeHost History service, HOT event helper, exact event producer/publication
  joins, EVENT_INDEX template/writer and its dedicated event-index schema.
- EXPECTED CONSUMERS TO CHANGE: P3 retrospective; RuntimeHost History users;
  collaboration/LIVE absorption/event publication companions where exact event
  enrollment participates.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: bounded HistoryDiscoveryRequest/
  Candidate/Result/source-basis carriers; optional typed event discovery_refs;
  existing EVENT_INDEX event-specific enrollment/discovery shape. Generic
  native_family_index contract is not changed.
- PROTECTED ARCHITECTURE INVARIANTS: EVENT_INDEX/helper derived only; exact
  NativeSemanticEvent/native source terminates material claims; no absence proof,
  body scan or generic search; accepted HOT participates before SAVE; pre-CAS
  LIVE excluded; no campaign fallback for LIVE current truth; one existing
  durability/absorption closure.
- ARCHITECTURE-SENSITIVE SURFACES: event enrollment completeness, source-local
  provenance/currentness, HOT atomic companion update, selected LIVE packs/CAS,
  absorption deduplication and schema/template consistency.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD04, RuntimeHost, RD13,
  RD09, RD06, RD12 collaboration where absorption participates, RD14 scaffold/
  generator and dedicated event-index schema tests.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: generic family-index semantics, Story,
  current knowledge/disclosure authority, retention/exact-quote expansion,
  chronology authority, generic memory/search, arbitrary migration.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify History/
  RuntimeHost/HOT/LIVE/publication modules and the dedicated event-index/
  SemanticEvent schema surfaces. Do not infer a schema bump or migration before
  the current owner/version law is read.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0 output/cursor; T06-A1; WP19 L29–38;
  WP11/12/13/14/16; History/RuntimeHost/HOT/durability/publication/LIVE/
  collaboration/init_campaign; EVENT_INDEX and both relevant schema contracts;
  RD04/06/09/12/13/14 and version owners.

### W05.T06-P3 — Same-operation sealed ordinary-Master retrospective

**Dependencies:** `W05_T06_NATIVE_HISTORY_DISCOVERY_READY`,
`W05_T06_CURRENT_OWNER_VIEW_READY`.

**Goal:** join current orientation, bounded native History, exact historical
evidence and the ordinary gameplay recipient/subject eligibility contract, then
assemble the existing NARRATOR profile.

**Files:**
- Create: `GAME/TOOLS/retrospective.py`.
- Modify: RuntimeHost and private Context retrospective admission.
- Modify RD11/RD13/RuntimeHost/RD09 tests. Keep PO-012 tests on their existing
  separately named Commentator regression surface.

**Interfaces:** retain the accepted `RetrospectiveService.execute`,
Host-issued same-operation `RetrospectiveEvidenceSet` and private
`ContextService._assemble_retrospective` shape. Request data cannot carry raw
events, Story authority, service capabilities, eligibility lists or a seal.

The service resolves the **current ordinary gameplay subject** from the current
turn/product binding and proves that the current active PLAYER controls that PC.
Multiple controlled PCs are not automatically an error and are never unioned:
the already selected/current gameplay subject is used; if the subject is
materially ambiguous, return the existing bounded clarification/typed inability
rather than importing Commentator selected-PC semantics.

Eligibility is source/aspect-specific under PO-001 + Step-4 + R2.3:

- current human-player disclosure may support what that human has been told;
- current subject-PC `world.knowledge` stance is preserved as
  aware/known/believed/suspected/rejected and may support only the matching
  qualified statement;
- a belief/suspicion never becomes an established objective fact;
- current access/control and exact source eligibility remain mandatory;
- physically readable hidden objective/history material without applicable
  current eligibility is excluded before Narrator context.

PO-012's `PUBLIC + PLAYER disclosure + at-most-one selected PC known` formula
remains Commentator-only. P3 adds ordinary-Master tests for an eligible
qualified belief/suspicion, denial of hidden objective truth, current disclosure,
revoked control, current subject among multiple controlled PCs, ambiguous
subject, hidden field, T0/T1 divergence, stale/cross-host seal and source
movement. Separately rerun existing PO-012 Commentator positive/negative tests
unchanged.

The seal proves same-operation acquisition/source binding only; it grants no
permission. Story is absent from the baseline route. Direct public
`ContextService.assemble(... retrospective=True ...)` stays terminal without
the Host-issued private evidence path.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_runtime_host_composition.py
```

**Output:** `W05_T06_SEALED_RETROSPECTIVE_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§8, 13–19; PO-001/WP19 L20–L23; Step-4/R2.3/
  R2.4 ordinary NARRATOR; current information/access owners.
- BASELINE REF OR SHA: accepted P2 output SHA plus accepted P0 output after
  fresh read-back.
- EXPECTED OWNERS TO CHANGE: new retrospective use-case module, RuntimeHost
  service composition and private Context retrospective admission only.
- EXPECTED CONSUMERS TO CHANGE: held T06 ordinary-Master product route and
  ordinary NARRATOR context assembly; Commentator remains regression-only.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: typed retrospective request/result,
  Host-issued same-operation RetrospectiveEvidenceSet and private Context
  admission. Public candidate maps remain non-authoritative.
- PROTECTED ARCHITECTURE INVARIANTS: ordinary Master != Commentator; current
  gameplay subject/active PLAYER/control; source/aspect-specific current
  knowledge/disclosure/access; epistemic stance preserved; exact History/T0
  source evidence; seal grants no eligibility; no raw private event/index/helper
  material in model context; Story optional/absent; no MASTER role.
- ARCHITECTURE-SENSITIVE SURFACES: subject resolution with multiple controlled
  PCs, current disclosure/knowledge aspect filtering, single-context protected
  material, T0/T1 divergence, source movement, seal lifetime and NARRATOR output.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD11 Context, RD13
  History/T0/Story separation, RD09 access/PLAYER/LIVE, RuntimeHost composition,
  separate existing PO-012 Commentator controls and later RD14 product routing.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: Commentator/PO-012 changes, MASTER role,
  generic retrieval/search, Story reader, new information/access authority,
  persistent retrospective state, extra serial LLM phase, save/publication.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify actual
  new/changed GAME modules; no persistent schema/catalog/checkpoint/migration
  change is pre-authorized.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: accepted P0/P2 cursors; T06-A1;
  PO-001/WP19; Step-4/R2.3/R2.4; information/access/PLAYER owners;
  RuntimeHost/Context/History; RD09/11/13 and version owner.

### T06-A1 accepted-law coverage and critic propagation

| Canonical law | Planned discharge |
|---|---|
| T06A1-1 operation-scoped CurrentOwnerView | P0 |
| T06A1-2 coherent expanding HOT observation; no global frontier | P0 |
| T06A1-3 Context current-family cutover | P0 |
| T06A1-4 deterministic readiness; local sufficiency / READY_PC / PLAY_READY distinct | P1B + product completion |
| T06A1-5 exact Actor/PLAYER/dependency/catalog/ruleset basis | P1A/P1B |
| T06A1-6 re-evaluation after accepted change/resume/rejoin | P1B + product completion |
| T06A1-7 ordinary Master existing Interpreter/Narrator; no MASTER role | P3 + product completion |
| T06A1-8 minimum typed discovery refs under one EVENT_INDEX | P2 |
| T06A1-9 derived event index + exact evidence + empty enrollment alignment | P2 |
| T06A1-10 finite selectors; no generic search/body scan | P2 |
| T06A1-11 accepted HOT + selected LIVE discovery | P2 |
| T06A1-12 NOW resolves through current owners | P0/P3 |
| T06A1-13 thin retrospective orchestration | P3 |
| T06A1-14 sealed acquisition + independent ordinary-Master eligibility | P3 |
| T06A1-15 retained T0 only; no T1 reconstruction | P3 |
| T06A1-16 Story adapter dormant | no baseline task |
| T06A1-17 typed failures/recovery | P0–P3 + product completion |
| T06A1-18 no extra serial LLM/publication boundary | P1A/P1B/P3 + product completion |

S6D-07 deferred production resolver is discharged by P1A; P1B provides its
runtime readiness consumer. Senior plan findings SP06-01..SP06-04 and repair
additions SP06-05..SP06-09 are mapped in the repair-resolution artifact and must
remain closed at final plan re-review.

## W05.T06 — Onboarding, join/rejoin, retrospective and save/exit product paths

This is the held product-completion task after P1A/P1B and P3 are accepted (P0/P2
are transitive prerequisites). T06-S1/S2 below in the execution cursor remain
accepted; do not replay or reopen their implementation. The T06 product task
adds only the progressive-readiness and ordinary Master retrospective
composition, then proves the whole T06 product output.

Hard inputs: accepted `W05_T06_CURRENT_OWNER_VIEW_READY`,
`W05_T06_CHARACTER_MATERIALIZATION_READY`,
`W05_T06_PRODUCTION_READINESS_READY`,
`W05_T06_NATIVE_HISTORY_DISCOVERY_READY`, and
`W05_T06_SEALED_RETROSPECTIVE_READY`; accepted
`W04_RUNTIME_HOST_COMPOSITION_READY`, `W04_RUNTIME_HOST_IO_EXTENSIONS_READY`,
T07E exact-serialized-byte measurement, and the exact completed owner
checkpoints consumed by each product path. PO-012 is a separate Commentator
regression owner only; it is not an ordinary-Master eligibility input. T06-S1/S2 remain accepted without
waiting for or replaying this held task.

Implement the product-facing flows over the completed owners:

- progressive onboarding preserves the campaign selection barrier and canonical identity;
- creator binding uses verified stable account ID; login remains visible for selection and invitations;
- creator uncertainty or login rename does not transfer ownership and yields read-only/fail-closed behavior;
- multiplayer join/rejoin uses the principal route and exact PLAYER reload;
- ordinary Master retrospective follows PO-001/WP-19 and the T06-A1 architecture: current/native owners and native History are authoritative; Story, if used, is orientation/navigation only; current PLAYER/knowledge/disclosure eligibility controls visible material. Commentator-specific PO-012 behavior remains separately preserved for Commentator-facing retrospective/control paths and never promotes Story to Master truth authority;
- save/exit uses the accepted durability promise and reports typed publication outcomes;
- failures/retries do not duplicate campaign, PLAYER, LIVE source or accepted mechanics;
- after campaign selection, product/runtime flow creates or reuses one campaign-bound RuntimeHost composition root; gameplay callers never supply/replace RepositoryPort, LIVE transport, native-ordering, Context or History services;
- the bound `CampaignPublicationTransport` supplies T07E's exact `measure_path_operations(...)` capability using the same serializer as `create_tree`; an adapter without that capability fails closed before any writer that requires accepted size-band review and must never substitute an estimate, hard cap or second serialization.

The product adapters retain the accepted callable names from the baseline
manifest: `progress_onboarding(...)` routes accepted typed onboarding intent
through `RuntimeHost.character_progression`, then obtains local-sufficiency/
READY_PC results from `RuntimeHost.readiness`; `route_active_player_retrospective(...)` delegates
to `RuntimeHost.retrospective.execute(...)`. The adapters do not accept a readiness boolean, raw native owner after-image,
owner service, raw History payload, catalog capability or evidence seal from
gameplay/model input.

Remaining progressive onboarding consumes `RuntimeHost.readiness` and
`CurrentOwnerView`: it preserves the same Actor identity, permits only locally
sufficient provisional mechanics, continuously reevaluates READY_PC after
material accepted build/current-owner changes and on correctness-relevant
resume/rejoin, and crosses READY_PC/PLAY_READY only with the existing semantic
acceptance and confirmed durability boundary. Ordinary retrospective calls the
Host RetrospectiveService. No new bootstrap boolean, lifecycle, save, or
membership authority is introduced.

TDD and verification:

- complete `CampaignSelectionBarrierTests`, `CreationIdentityTests`, `ProgressiveOnboardingTests`, `MultiplayerJoinRejoinTests`, `OrdinaryRetrospectiveRoutingTests`, `SaveExitMenuTests`, `CreatorAuthorityTests`, `ShippedBootstrapProjectionTests` and remaining bootstrap cases;
- include login display/invitation success, email rejection, login-only takeover rejection and legitimate stable-ID rejoin;
- prove ordinary Master retrospective follows PO-001/WP-19 current-player eligibility and exact native/current evidence without treating Story/caller IDs as authority; separately preserve PO-012's PUBLIC + current PLAYER disclosure + at-most-one selected controlled-PC `epistemic.known` rule for Commentator-facing control/retrospective paths, including no multi-PC union and no legacy `visible_to` authority;
- prove the shipped campaign-publication adapter exposes exact `measure_path_operations(...)` with create-tree serializer parity and that missing measurement capability fails closed before a size-governed publication.

The final product proof must include ordinary native History with Story
absent/stale; accepted unpublished event state before SAVE; current control
revocation; T0/T1 divergence; hidden event fields; source movement; and
unsupported content. Existing accepted `SaveExitMenuTests`,
`CreatorAuthorityTests`, `CampaignSelectionBarrierTests`,
`CreationIdentityTests` and `MultiplayerJoinRejoinTests` remain regression
consumers, not permission to repeat T06-S1/S2. Static boundedness is not an
empirical latency/SLA result.

Held T06 product integration command (run sequentially from the repository
root):

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd14_bootstrap.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd12_collaboration.py DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd09_access_live.py
```

Expected: exit 0; all remaining T06 behavior and accepted S1/S2 regression tests
pass. Then run the execution contract's exact clean-source full DEV suite and
maintenance audit before publishing this output.

**Output:** `W05_PRODUCT_PATHS_READY` only after this task's product consumers,
P0–P3 checkpoints, actual Impact Envelopes, Version Impact Gate and exact
cross-owner tests are accepted; the normal Senior final integration audit then
checks the implementation delta before Wave 05 advances.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: this W05.T06 task; T06-A1 canonical spec/ruling;
  WP-19/PO-002; accepted creator-login, access, R2.5 collaboration, durability,
  RuntimeHost, T07E measurement and PO-012 owners.
- BASELINE REF OR SHA: fresh exact public HEAD after repaired-plan Senior GO
  and each named producer read-back; record the exact start SHA before RED.
- EXPECTED OWNERS TO CHANGE: `GAME/TOOLS/bootstrap.py`; a narrow existing
  Access Control callable only if the accepted creator-established/eligible
  own-initial-PLAYER binding requires it; `DEV/TESTS/test_rd14_bootstrap.py`;
  task execution status. P0–P3 producer files change only in their own earlier
  tasks, not again here without a new envelope comparison.
- EXPECTED CONSUMERS TO CHANGE: progressive onboarding and ordinary Master
  retrospective product paths; existing save/exit, creator and join/rejoin
  behavior is regression-tested and preserved.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: T06-local product callables and
  transient results in `bootstrap.py`; any narrow Access Control callable must
  realize already accepted semantics and is test-first. No new transport,
  persistent data, membership transition or capability injection.
- PROTECTED ARCHITECTURE INVARIANTS: same Actor across provisional/READY_PC;
  exact current principal/PLAYER/control; stable account ID binds PLAYER while
  login remains display/invitation and historical creator provenance; confirmed
  durability before READY_PC/PLAY_READY or save/exit clear; ordinary Master
  remains gameplay/NARRATOR; PO-012 remains separate for Commentator; exact T07E
  measurement before size-governed writes; S1/S2 outputs and tests remain
  accepted; no duplicate mechanics, IDs, campaign, LIVE source or save.
- ARCHITECTURE-SENSITIVE SURFACES: bootstrap flow and same-host composition;
  initial readiness transition; player/PC identity; retrospective role and
  current eligibility; save/exit sequencing; publication-size fail-closed
  behavior.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: all named remaining RD14
  classes; accepted S1/S2 regression classes; RuntimeHost composition and
  measurement; RD09 principal/creator; RD12 join/rejoin; RD11 Context;
  RD13 History/T0/Story separation; RD06 publication outcomes; T05
  discovery/generator; P0–P3 cross-owner suite; clean exact full DEV and
  maintenance audit before acceptance.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: `runtime_host.py` transport semantics,
  `publication.py` W02 contracts, policy basis/RepositoryPort, `context_runtime.py`
  or `history.py` owner implementation beyond consuming accepted P0/P2/P3
  services, persistent schemas/catalog, `GAME/INSTALL/*`, `GAME/CORE/*`,
  PROJECT_MAP, `audit_engine.py`, manifest-v5/membership retirement, W06, and
  root README.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: re-read actual
  `bootstrap.py` and any narrowly changed Access Control module. Their values
  observed during the prior T06 envelope are not targets after later commits.
  No persistent schema, campaign/storage/catalog generation, migration or
  dual-read is pre-authorized; classify each actual delta.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: all four P0–P3 accepted output cursors;
  T06-S1/S2 evidence; current progress, W05 plan/index/execution contract;
  WP-19/PO-002, creator continuity, access/PLAYER, collaboration, durability,
  RuntimeHost/T07E measurement; bootstrap/access code; RD14/RD06/RD09/RD11/
  RD12/RD13 and version owners.

The earlier umbrella `ProductExitCreatorTests` is not recreated: its save/exit and creator fail-closed duties are discharged by the task-local `SaveExitMenuTests` and `CreatorAuthorityTests` at their coherent checkpoints.

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

Fresh-read and integrate owner deltas into each material module exactly once.

The separately authorized 2026-10-03 instruction checkpoint projects accepted single-chat role/cache laws early: AI_REASONING is now 1.0.4, PLAY_POLICY 1.0.5 and RUNTIME 1.0.3. It does not close T08 or claim its remaining RuntimeHost/PO-011/adjudication/access joins. The two targets below advance once for those remaining material inputs; preserve the early role/control text. RUNTIME's bounded invocation projection is already realized outside the sixteen-module final-writer table; inspect/preserve it and bump further only for another material change. Concern revisions are already ai_reasoning_revision 4 / runtime_scope_revision 4; apply the version law to any later material concern change, not a stale baseline reset.

Fresh final-writer targets:

| Module | Target | Required semantic inputs |
|---|---:|---|
| BOOTSTRAP_RUNTIME | 1.0.9 | current transport/currentness + bounded bootstrap discovery + `W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY` + `W04_RUNTIME_HOST_IO_BOOTSTRAP_DELTA_READY` + T07E `CampaignPublicationTransport.measure_path_operations(...)` exact-serializer wiring + PO-011 player-visible bootstrap/technical-surface separation |
| RANDOMNESS | 1.0.3 | fixed RNG acceptance/recovery |
| EXPLORATION | 1.0.2 | current exploration/domain cutover |
| STORAGE | 1.0.2 | routing/HOT + exact recovery/operational roots |
| SAVE_CONTRACT | 1.0.2 | durability promise/save-exit |
| PERSISTENCE | 1.0.4 | publication/recovery/currentness + CampaignPublicationService/W02 plan execution wiring + exact `measure_path_operations(...)` transport capability from T07E |
| CHRONOLOGY | 1.0.2 | temporal/thread/current-state |
| PROCESSES | 1.0.3 | procedure/continuation/operational roots + owner-native ordered-response evidence route |
| AI_REASONING | 1.0.5 | typed role/context/protected result + campaign-bound RuntimeHost Context composition + PO-011 `ResolvedResponseLanguage` / internal-vs-visible presentation law |
| LIVE_SCENE | 1.0.4 | source-native LIVE/currentness/state + selected-LIVE evt source-domain reader wiring |
| MULTIPLAYER | 1.0.8 | principal route + LIVE + collaboration/access reconciliation |
| CAMPAIGN_SETUP | 1.0.4 | identity/scaffold/onboarding + PO-011 current player-language Master/setup presentation |
| SESSION | 1.0.2 | exact session/campaign/LIVE/PLAYER handoff + PO-011 human-visible session/status language projection |
| PLAY_POLICY | 1.0.6 | exact accepted adjudication/access policy + PO-011 rule that optional language-policy absence never licenses another visible response language |
| CORE_INDEX | 1.0.2 | current module routing/versions |
| ADJUDICATION | 1.0.3 | bound catalog and accepted policy basis plus exact source-open spell ruling profiles before outcome/cost |
| MAGIC | 1.0.1 | accepted installed spell/Activity preflight and native receipt; genuine source-open/improvised ruling retained, missing promised rule is an installation defect before spend |
| CHARACTER_READINESS | 1.0.4 | SP27/SP29 exact selected4+2 known-all6/prepared-two/all-mode context and actual P1A/P1B producers; no runtime rules lookup |
| MECHANICS_INTEGRITY | 1.0.2 | native accepted receipts/cost/RNG/closure/recovery and supported-gap rejection, no narration/fixture substitution |
| RUNTIME | 1.0.4 | selected sealed recipe/native ExecutionService path, same-chat logical phases and technical holds; no dedicated/deterministic-step model call or warm corpus load |

Shared physical checkpoints:

- integrate `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and `GAME/INSTALL/00_DND_BOOTSTRAP.md` at `RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION_READY`, projecting PO-011 so player-visible bootstrap/setup/failure wording follows the current response language while technical internals remain separate;
- integrate `GAME/CORE/BOOTSTRAP_RUNTIME.md` at `CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY`, including the final deployment wiring law: authenticated Step-5.6 RepositoryPort + campaign publication transport + Step-5.8 LIVE/source-domain adapters compose the Wave-04 RuntimeHost after campaign selection, while no gameplay/model surface can inject those capabilities; the publication transport must implement T07E's exact `measure_path_operations(...)` contract with the same serializer as `create_tree`, and absence must remain fail-closed;
- integrate `GAME/CORE/STORAGE.md` at `CORE_STORAGE_FINAL_INTEGRATION_READY`;
- integrate `GAME/CORE/MULTIPLAYER.md` at `CORE_MULTIPLAYER_FINAL_INTEGRATION_READY`;
- integrate all other material CORE modules once with their listed owner inputs, including the four newly material spell consumers above. This final table has twenty named modules. The accepted instruction checkpoint remains preserved; these are fresh-derived later material changes, not repeat bumps.

TDD and verification:

- use `InstallBootstrapSharedWriterTests` (`STATIC_AUDIT`) and `BoundedCampaignDiscoveryTests` (`FOCUSED_BEHAVIOR`);
- complete `CoreFrameworkModuleVersionCutoverTests` and the retained version suite, including all twenty current table rows and source-owned exact interface/role qualifiers;
- prove final install bytes contain no exhaustive all-campaign card loop, login-only authorization, generic PLAYER_INDEX authorization or stale v0.8 compatibility path; also prove no shipped ordinary Master path uses English, Russian or another fallback solely because an optional language policy/local phrase asset is absent, technical diagnostics remain a separate recipient-safe surface, PO-012 retrospective/Commentator routing never unions multiple controlled-PC knowledge or trusts caller Story visibility, and the final campaign-publication transport exposes exact create-tree-parity size measurement rather than an estimate.

After all module/schema/test paths are final, integrate their routes into `DEV/PROJECT_MAP.md` and all current/stale/schema/catalog/version/package assertions into `DEV/TOOLS/audit_engine.py`. At this same final control-plane cutover: Retire `pc.schema.yaml`, `npc.schema.yaml` and `item.schema.yaml` only after `audit_engine.py` and every remaining legacy-schema consumer are reconciled; retire any remaining retired-faction contract/reference at the same boundary. Retired contracts receive no terminal version bump. Run the actual maintenance entry point after these edits; do not leave per-task partial writers.

Output checkpoints: `W05_SHIPPED_INTEGRATION_READY`, `PROJECT_MAP_FINAL_INTEGRATION_READY` and `MAINTENANCE_AUDIT_FINAL_INTEGRATION_READY`.

## Wave 05 completion evidence

Record the exact 17+17 census, actual shared-file bytes, every schema/module version, manifest field absence, blank-scaffold completeness, bounded discovery behavior and shipped consumer routing at the published HEAD. No owner-local delta may remain waiting outside the final physical writers when this wave closes.

## Historical 2026-10-03 autonomous T06 continuation authorization

AUTHORIZATION_BASE_SHA: `37872ca98c425b7b194e48aaed2a543b2058e7f8`.
The Product Owner directs continued execution until a real product-semantics, material trade-off or explicit risk-acceptance question. This removes the request-local scheduling pause; it does not waive technical verification or change accepted architecture.

P0's `W05_T06_CURRENT_OWNER_VIEW_READY` is accepted/read back at `8f7098c23521237363bca84879485a18f5b7aa25`; published status HEAD `37872ca98c425b7b194e48aaed2a543b2058e7f8` has successful hosted CI run `37153339822`. This continuation uses the already accepted stable T06 plan and Senior rulings; it does not claim a new full P0 implementation audit.

NEXT_AUTHORIZED_BLOCK: dependency-driven T06 continuation: P0 -> P1A -> P1B and independently P0 -> P2 -> P3; P1B + P3 join before held T06 product completion. Each successor activates only after all named inputs are independently reviewed, published and read back. Isolated/disjoint preparation may run in parallel; overlapping physical writers, integration and publication remain serialized. No new human permission is required at ordinary task boundaries. Preserve accepted S1/S2 and P0; do not repeat them without an owner-defined reopen trigger.

Apply the execution contract to every task: fresh currentness/owners, bounded Impact Envelope, TDD, integration and version checks, independent spec/quality review and repair, applicable clean exact verification, publication/read-back and durable cursor/checkpoint update. Technical failures and bounded implementation choices are handled autonomously. A genuine System-Impact change goes to the authorized Senior role, not automatically to the Product Owner; a worker must not self-approve a required Senior ruling.

After T06 completion, route the exact published checkpoint to the mandatory independent Senior integration audit. That is a technical review gate, not a request for PO permission. Only its accepted result produces `W05_PRODUCT_PATHS_READY` and releases consumers whose other inputs are GREEN. T07/T08 and W06 are not activated by this T06 continuation checkpoint. Story and all trigger-gated work remain dormant.

VERSION_IMPACT: NONE — scheduling/control documentation only.

## Historical 2026-10-03 instruction-efficiency checkpoint and scheduling reconciliation

Source basis: `be1c9b919bba65bcb1a9e5d5eb7b19e7c72fd82f`. The Product Owner separately stopped the worker at a safe boundary and authorized the Architect to amend instructions. Evidence/impact/review owner: `DEV/docs/superpowers/design/2026-10-03-hdm-dev-game-instruction-efficiency.md`.

This amendment supersedes earlier one-production-task sequencing and blanket P2/P3 holds only as scheduling authority. Preserve their historical evidence. Accepted dependencies are P0 -> P1A -> P1B, independently P0 -> P2 -> P3, then P1B + P3 -> held T06 completion. The actual P1A NEEDS_PO decision is unchanged. P2 can continue only after its own exact fresh input/envelope checks; P3 remains blocked until P2 is accepted. No production task or Story/T07/T08/W06 activation is claimed here.

DEV uses bounded subagents and isolated/disjoint preparation, with one integrator/publisher. GAME remains logical phases in one chat, without new model calls/roles/authority. The early shipped instruction projection is not T08 completion; preserve all remaining RuntimeHost/PO-011 and other joins. T08 AI_REASONING/PLAY_POLICY targets are reconciled to 1.0.5/1.0.6 after current 1.0.4/1.0.5; RUNTIME is now 1.0.3.

VERSION_IMPACT: AI_REASONING 0.1.3 -> 1.0.4; PLAY_POLICY 0.8.4 -> 1.0.5; RUNTIME 1.0.2 -> 1.0.3; DEV ai_reasoning_revision/runtime_scope_revision 3 -> 4. Other control/process/profile edits NONE under the version owner; no schema/catalog/storage/campaign generation, migration or engine release change.
NEXT_EXACT_TASK: existing authorized W05.T06-P2 entry/envelope, not a new task assignment. P1A waits for the recorded product judgment; completed P0/S1/S2 remain accepted.

## 2026-10-04 accepted local-spell realization — stable executable extension

**Plan state:** INDEPENDENT COMPLETE32-TASK SENIOR GO. Canonical architecture has independent Senior Stop2 GO at84b9da6bbabb6abda274f4cb63408d5a8298b36e; complete-plan GO at `d84c9a367d46f2f6e70bfa4baadac0914a2d19a9` is recorded in `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/implementation-plan-senior-review.md`. Otherworker dependency-eligible implementation is authorized through the unchanged task process. No PO question remains. Current activation is exclusively DEV/CURRENT_PROGRESS.md.

The executable tasks below are part of this existing stable Wave05. Source/architecture/proof reports and the dated independent plan-review report are evidence only. Preserve accepted Waves01..04, W05.T01..T05, T06 S1/S2/P0 and earlier owner-local inputs. Do not rebuild those mechanisms because the new tasks reuse them.

**Task granularity and scheduling:** SP00..SP30 with separate SP15A/SP15B are32 additional independently reviewable deliverables, not339 individual implementations and not13 executor services. Each mechanism task includes its meaningful native behavior and negative-law proof. Each level shard includes every required entry/mode/branch/support mapping and numeric conformance witness, with native production proof joined after SP28. The coordinator may sequence in-scope local iterations within a task, but cannot shrink its supported rule domain or replace native proof with an inventory count.

At worker entry, first complete fresh bootstrap/currentness and select SP00 source qualification, SP01 strict machine/value/profile foundation and the already eligible P2 own-input lane. SP00 and SP01 may do disjoint isolated preparation in parallel; P2 retains its original semantics and later supplies the Wish History consumer. No blanket whole-wave barrier or task-number sequencing applies. Every output activates only after required inputs, independent task review, coherent publication and readback. Continue automatically through eligible tasks and their technical reviews, then original T06 integration/Senior and eligible T07/T08/W06; no new human permission at checkpoint boundaries.

**Physical ownership and coherent partial packages:** one coordinator/final integrator owns shared machine schemas/catalogs, package manifest/seed/capability/NOTICE/evidence projections, host/kernel wiring, version projections, PROJECT_MAP, cursor, Git index and remote publication. Subagents own bounded disjoint modules/tests/content shards in isolated workspaces. Foundation builders may admit closed shapes before production consumers exist, but cannot advertise executable/full support. Package members are admitted explicitly by the coordinator at each coherent content checkpoint; SP17/SP18 relocate existing spell/Activity bodies and required separately named extra bodies out of the seed in that same publication, avoiding duplicate definitions. Every intermediate package truthfully states its realized subset and passes its applicable validators/audit. The final full339 promise is issued only by SP29 after all exact actual producer/proof joins. There are no unmanifested runtime dependencies, audit exemptions, permanent failing tests or runtime DEV dependencies.

One final writer means one responsible integrator and one final joined cutover, not a prohibition on necessary earlier coherent native/materialization checkpoints. A later accepted logical change may advance the same module version again under its actual namespace owner. Never repeat an earlier bump, downgrade a fresh value, or assert obsolete sixteen-module targets after this extension's material inputs. T08 remains the final shipped CORE/install writer.

**Mandatory common task details:** all tasks inherit the complete execution-contract §4 Impact Envelope and mandatory RED/GREEN/review/VersionImpact/currentness/publication loop. Before first RED fill IMPLEMENTATION START HEAD and PRIMARY OWNER ARTIFACTS from a fresh coordinator pinned Source Manifest; before integration fresh-read every actual shared write path and its owning version. Each stated path action is rechecked at current HEAD; an already-created path changes from NEW_CREATE to the approved owner-local modification, never overwritten without currentness. Fixture paths declared by a task have one task owner; source-backed test evidence cannot replace real accepted state. Follow actual OpenCode/LOCAL_MACHINE transport, dependencies and /tmp/hdm-dev isolation; do not import ChatGPT Connector-only execution restrictions into the VPS.

**Version/adoption rules:** unchanged architecture/control publication is NONE; actual new runtime modules start current engine-line revision1, each material existing module change increments from its fresh value. Compatible additive content is distinguishable by exact identity; package revision and compatibility/catalog/schema/campaign/storage/digest generations keep their separate meanings. Derive namespace-specific transitions from accepted version/adoption law and actual edits, synchronize required projections in the same checkpoint and retain exact old accepted contexts. No engine release/tag bump or migration/compatibility verdict follows from339 content count.

**Dependency types:** named tasks use HARD_PRECEDES for absent required production inputs, JOIN_BEFORE_INTEGRATION for disjoint preparation, SHARED_FILE_CHECKPOINT for coordinator integration and PROOF_AFTER_TARGET for proof. Core compiler/native/profile qualification can use exact lawful partial recipes without a full advertised package. Thus SP28 precedes full mode producer proofs/SP29 and SP29 precedes installed package proof SP30; none consumes its own future full support assertion. P1A consumes SP29's actual package and acquisition context as additional inputs; P1B consumes accepted P1A. P0->P2->P3 stays independent of P1A/P1B. P1B+P3 still join before T06 product completion and required independent Senior integration audit. Story/other dormant empirical capabilities retain their exact triggers.

**Bounded worker reads:** each delegated assignment receives its exact task block, shared ABI and pinned source/dependency manifest; do not preload all32 task bodies or all339 source records into each agent. The coordinator owns the complete graph, while a level author reads its exact level roster and necessary native consumers. A reused technical review remains valid only for unchanged scoped bytes/inputs. Full source/production equality is completed by the designated integrator, not delegated to the human.


## Spell task dependency and checkpoint table

This table summarizes completion joins; isolated source/definition preparation may start earlier where the task's JOIN_BEFORE_INTEGRATION permits it. Named external accepted/native checkpoints in the actual task remain mandatory. In particular P2->SP28 Wish History, SP16 INPUTS->SP28 native DOMAINS, and native all-mode proof->SP29 are distinct.

| Task | New-task completion inputs | Delivered scope |
|---|---|---|
| W05.SP00 | accepted baseline / plan GO | qualified source roster |
| W05.SP01 | accepted baseline / plan GO | closed shapes/DTOs |
| W05.SP02 | SP01 | sealed compiler/cache/lookup |
| W05.SP03 | SP02 | pinned reads/calculation/preflight |
| W05.SP04 | SP03 | native/RNG kernel + PT-D1/PT-D2 |
| W05.SP05 | SP04 | three stochastic continuations |
| W05.SP06 | SP04 | choice/reaction/mandatory closure |
| W05.SP07 | SP04, SP06 | ritual/long/nested timing |
| W05.SP08 | SP04 | Health/interception preparation |
| W05.SP09 | SP04 | Effect/concentration/progress/temporal |
| W05.SP10 | SP04 | forms/construction |
| W05.SP11 | SP04 | principal/body/replicas |
| W05.SP12 | SP04 | directed conversion/object return |
| W05.SP13 | SP04 | space/relocation/portals |
| W05.SP14 | SP04 | Information/control/entitlement |
| W05.SP15A | SP04, SP08, SP09, SP10, SP11, SP12, SP13, SP14 | protected recent evidence/counterfactual |
| W05.SP15B | SP15A | source preparation/replacement preparation |
| W05.SP16 | SP00, SP02 | complete supporting DOMAIN INPUTS |
| W05.SP17 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level0 |
| W05.SP18 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level1 |
| W05.SP19 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level2 |
| W05.SP20 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level3 |
| W05.SP21 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level4 |
| W05.SP22 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level5 |
| W05.SP23 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level6 |
| W05.SP24 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level7 |
| W05.SP25 | SP00, SP02, SP16, SP28 | all entry modes/native proof in level8 |
| W05.SP26 | SP00, SP02, SP16, SP28, SP17, SP18, SP19, SP20, SP21, SP22, SP23, SP24, SP25 | all entry modes/native proof in level9 |
| W05.SP27 | SP00, SP02, SP17, SP18, SP28 | source-owned acquisition/adoption inputs |
| W05.SP28 | SP00, SP05, SP06, SP07, SP08, SP09, SP10, SP11, SP12, SP13, SP14, SP15B, SP16 | actual native host/profile/domain/Wish joins |
| W05.SP29 | SP27, SP17, SP18, SP19, SP20, SP21, SP22, SP23, SP24, SP25, SP26, SP28 | full mechanical339 package/context/adoption |
| W05.SP30 | SP29 | installed offline/native/cost proof |

### Exact semantic spell-capability member

SP01 NEW_CREATE DEV/SCHEMAS/spell-capabilities.schema.json closes this selected package metadata contract; SP16's serialized integrator NEW_CREATEs GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-capabilities.json as a truthful partial declaration and explicitly lists it and NOTICE.md in the manifest. SP29 modifies it for the final mechanical support join. This is the semantic promise projection selected by the content annex, not a state/service/digest owner.

Required exact fields: schema_version:1; identity_source:"ruleset-package-manifest.json"; profile_id:"spell.srd52.local"; content_basis:"SRD_5_2_1"; coverage_stage:PARTIAL|MECHANICALLY_COMPLETE; supported_srd_spell_ids:unique sorted array of exact definition IDs; existing_extra_spell_ids:unique sorted disjoint array of separately proved existing IDs; mode_bindings:unique sorted array of closed {spell_id,mode_id,activity_id}; unsupported_content_policy:"ABSENT_NONSELECTABLE"; notice:"NOTICE.md". Unknown fields, duplicate/foreign IDs and roster/mode mismatches reject. Each listed entry has complete all-mode source/definition/machine/native/scenario proof; omitted development entries remain nonselectable. PARTIAL never implies339 support; MECHANICALLY_COMPLETE requires exact339 SRD source/definition/consumer/native-proof equality and separate lawful-extra evidence. Target performance is separately qualified in its exact proof dimension and SP30/W06; this metadata never claims a measured release-ready response.

Do not special-case another semantic identity algorithm: existing manifest->snapshot semantic_entries->resolved lock/comparator/attestation owns exact identity. Changed metadata/options/defaults require its explicit adoption result, not additive-by-count compatibility. Existing character-capabilities remains full_srd_character_corpus=false. Package revisions/schema/catalog/digest/compatibility generations follow their actual owners; only this new protocol's schema begins1.

**Writers:** SP01 all typed/schema foundation; SP02 compiler part activity_runtime; SP03 pure context/calculation/cast; SP04 native kernel/PT repairs; SP05–07 pure separate modules; SP08–15 lifecycle. SP28 final writer adds plan_next_segment/ExecutionService/combined dispatch in shared modules, fresh reads/new material bumps. Production primitive/pair/read/fact/profile/manifest equality belongs final machine/package writer. SP29 full-support claim after all modes. Wish joins actual P2 History; Story dormant.

Fresh version owners control each checkpoint. New versioned GAME module starts revision1/current engine line; material existing change increments once. Inspected runtime_host1.0.14, runtime_execution1.0.8, mechanics1.0.5, durability1.0.4, publication1.0.6, live_state1.0.22, recovery1.0.5, temporal1.0.4; Actor schema2, Effect/Asset1, Procedure2. No stale reset/double bump/catalog generation by content count. Optional schema vs breaking trigger classified separately; retain adopted snapshots/work; no v0.8 dual-read.

## Shared closed ABI

activity_contracts.py defines immutable AdmittedActivityCatalog/CompiledActivity (execution§3), NativeSegmentPlan/Establishment (§6), exactly three StochasticState variants (§8), separate WishReconciliationState (WR03). lifecycle§§2–11/SS2-01 defines exact SubjectBinding/ObjectSubjectBinding/EffectSubjectBinding, TypedHealthCause/TypedEffectEndCause/AttackHitFrontierInput, ConcentrationTransitionInput/SpellProgressTransitionInput/FormTransitionInput/ActorConstructionInput/IdentityTransitionInput/ConversionTransitionInput/SpatialTransitionInput/ControlTransitionInput/InformationTransitionInput/ObjectSuspensionBasis/TruePolymorphObjectReturnAdjudicationResult/TypedObjectReturnCause/native-issued AssetDamageResult. Wish adds RecentRollWitness, ReconciliationDependencyEdge, AcceptedWishRetentionFrontier, WitnessRetentionPlan, WishRollRedoRequest, WishRecentBasis, WishTransitionInput, WishSourcePreparationPlan/Receipt, WishReplacementRelation, ConsequenceValidityProjection under WR01–08. Common typed inputs: CastPreflightInput/CastTransitionInput/CastingProcedureTransitionInput/ClosureTransitionInput/StochasticTransitionInput; no caller HP/resource/RNG truth.

NativePreparationContext is sealed same-builder capability: admitted instruction/profile, command/Resolution/occurrence/roles, owner session/observation, accepted permitted facts/adjudication/policy, fixed rolls, immutable prospective closure/allocation handles. No transport/LLM/patch. PreparedNativeFragment carries exact typed transitions/reads/exports/event-basis/mandatory work, cannot establish; kernel derives events. Internal NativePreparationHold operation_status=REVALIDATION_REQUIRED|CAPACITY_REQUIRED|AUTHORITY_UNAVAILABLE plus continuity refs; no persisted status/failure. Existing input/adjudication errors and genuine offer schemas remain owners.


AttackHitFrontierInput is the exact transient Mirror Image pre-damage consumer: compiled attack occurrence/frontier, source/target SubjectBinding, native fixed attack-result/roll refs and declared sensory-exception basis. The context issuer derives attacker/target/current native observation; caller hit truth is forbidden. No new persistent field/profile or generic trigger follows. SP08 interception accepts it alongside exact Health/EffectEnd causes.

SP04 native_execution helpers:
```python
begin_segment_plan(catalog: AdmittedActivityCatalog, compiled: CompiledActivity | None,
    accepted_command: Mapping[str,object], resolution: Mapping[str,object] | None, *,
    owner_session: CurrentOwnerReadSession, rng: SegmentRngProvider,
    procedure_state: Mapping[str,object]|None=None,
    continuation_state: Mapping[str,object]|None=None) -> NativePlanBuilder
NativePlanBuilder.preparation_context(*,consumer_id:str,occurrence_id:str,
    role_bindings:Mapping[str,NativeOwnerRef],
    accepted_facts:tuple[Mapping[str,object],...]=(),
    fixed_roll_refs:tuple[str,...]=()) -> NativePreparationContext
NativePlanBuilder.merge(fragment:PreparedNativeFragment) -> None
NativePlanBuilder.seal() -> NativeSegmentPlan
establish_segment(plan:NativeSegmentPlan,*,
    owner_session:CurrentOwnerReadSession) -> NativeSegmentEstablishment
```
Derive profiles/IDs/allocations from admitted inputs; reacquire whole union on expansion; changed earlier basis invalidates. Foreign/stale fragment, missing mandatory closure or premature seal reject. Trusted session adapter fixes backend; caller cannot select it. P0 read API preserved.

SP04 sole NEW `DEV/TESTS/spell_native_test_support.py`:
```python
NativeSpellHarness.open(*,source_fixture:Path,activity_id:str | None,
    mode_policy_profile_id:str | None,native_sources:Mapping[str,object],
    entropy:tuple[int,...],selected_live_fixture:Path|None=None) -> NativeSpellHarness
harness.begin(*,accepted_command:Mapping[str,object],resolution:Mapping[str,object] | None,
    procedure_state:Mapping[str,object]|None=None,
    continuation_state:Mapping[str,object]|None=None) -> NativePlanBuilder
harness.establish(plan:NativeSegmentPlan) -> NativeSegmentEstablishment
harness.read(owner_ref:NativeOwnerRef) -> CurrentOwnerRead
harness.recover() -> NativeSpellHarness
```
Actual source-admitted temporary package/lock/compile/accept_command/P0/native SQLite/RNG/native-first recovery. Entropy trusted test composition only; no fixture flag/raw-staging/seal shortcut. Private `DEV/TESTS/fixtures/local-spells/<task>/` sources retain explicit single-package topology, never production claims; later tasks own private fixtures and reuse helper.

The auth/turn reconciliation inside SP03/SP04 qualifies this shared ABI: action requires actual CompiledActivity and Resolution; direct requires `compiled=None`, `resolution=None` and the exact inventory-admitted transition binding/request, with K as execution owner. Never invent an Activity or Resolution to satisfy an action-only signature. Pure response and mixed Plan materialization use their native input/response edges, not an ordinary command wrapper. The existing harness remains one SP04-owned helper; its direct entry uses the exact native profile and no synthetic Activity selection. See the SP04 joins for phase/source/authority requirements.

## W05.SP01 — Closed spell machine shapes and typed preparation contracts

**HARD_PRECEDES:** accepted `W05_OWNER_LOCAL_STRICT_SCHEMA_WRAPPER_INPUTS_READY`, `RD16_SHARED_MACHINE_INTEGRATION_READY`, `W05_RETAINED_SCHEMA_CUTOVERS_READY`, `W05_T06_CURRENT_OWNER_VIEW_READY`; current architecture Stop2 and complete plan GO. **Output:** `W05_SPELL_CLOSED_MACHINE_SHAPES_READY`: strict shapes/interfaces only, no new production profile/definition activation. **JOIN_BEFORE_INTEGRATION:** every actual profile/consumer/proof delta -> final production machine/package writer. Existing active seed continues to validate.

**Files/actions:**

- `NEW_CREATE`: `GAME/TOOLS/activity_contracts.py`; `DEV/SCHEMAS/spell-native-profile-values.schema.json`; `DEV/SCHEMAS/spell-capabilities.schema.json` for the exact semantic-member contract below; `DEV/SCHEMAS/spell-support-row.schema.json`; `DEV/TESTS/test_local_spell_closed_contracts.py` and private SP01 fixture directory.
- `EXISTING_MODIFY`: `DEV/SCHEMAS/activity-definition-data.schema.json`, `activity-primitive-values.schema.json`, `runtime-resolution-state.schema.json`, `runtime-continuation-state.schema.json`, `runtime-procedure-state.schema.json`, `world-actor-state.schema.json`, `world-effect-state.schema.json`, `world-asset-state.schema.json`, `world-zone-state.schema.json`, `world-location-state.schema.json`, `world-connection-state.schema.json`, `world-record.schema.json`; GAME Actor/Effect/Asset schema projections only where actual contract changes require synchronization.
- `EXISTING_MODIFY`: `GAME/TOOLS/actor_continuity.py` only structural validators for the exact new closed Actor/HP/embodiment shapes; no NPC phase permission to mutate embodiment/physical relations. `world.knowledge` already has its native stance/source shape; `DEV/SCHEMAS/world-knowledge-state.schema.json` remains `INSPECT_ONLY`.
- `INSPECT_ONLY`: current ActionRequest/parameter/fact/choice/reaction/roll/segment/receipt schemas; primitive manifest/shards/shared read/value inputs; catalog ledger/core/mechanical surfaces; package manifest/lock/inventory. No absent GAME Zone/Connection schema is invented. No production `ACTIVE_ADMITTED` row changes in this checkpoint.

Close new `profile_bindings` on Activity definitions as an exact finite array of `{consumer_id, profile_id, profile_generation}` tied to compiled instruction occurrences and the corresponding closed profile schema. An entry is usable only when its actual contract/consumer is admitted by the resolved engine inventory. Unknown IDs/generations/occurrences reject; existing definitions may omit the array. Existing `details` never carries executable profile args, stochastic/reconciliation state, cause, geometry, return basis or progress. Add the exact accepted typed optional native members and conditional prohibitions, with the protected object basis as execution evidence rather than a writable health owner. Resolution/Continuation add `stochastic_state` and `reconciliation_state` under separate `$ref` unions; do not add a fourth stochastic discriminator. Common concrete casting Procedure state is a closed subtype of the current Procedure owner, retaining ACTIVE/TERMINAL lifecycle, native participant resources and exact TemporalBinding/accepted execution refs; it has no universal job record.

The support-row schema closes the execution annex section 2 fields and separate six proof dimensions. Each dimension has `{status: NOT_ESTABLISHED|PASS|FAIL, proof_refs: [...]}` plus exact `environment_ref` when applicable; target-performance PASS requires an actual environment reference. This DEV schema is evidence, not GAME state or another admission registry. Default dimensions remain NOT_ESTABLISHED.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§2/5–8; lifecycle§§2–11/SS2-01; WR03
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: Activity/values/native/version
EXPECTED OWNERS TO CHANGE: closed types/projections
EXPECTED CONSUMERS TO CHANGE: strict dispatch/seed
ALLOWED INTERFACES / CONTRACTS TO CHANGE: listed optional unions/sealed DTOs
GAME RUNTIME / PROJECTION SURFACES: listed module/schema projections
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: listed schemas; no admission
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: conditional ownership/adopted work
VALIDATORS / TESTS / AUDITS: SP01 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: schema synchronization only
CROSS-WAVE JOINS: accepted W05/P0; final writer
PROTECTED ARCHITECTURE INVARIANTS: one owner; no copied quantities
ARCHITECTURE-SENSITIVE SURFACES: principal/object/trigger/continuation
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: every branch; seed unchanged
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: import/activation/Story/release
VERSION IMPACT: new revision1; fresh schema owner
SCHEMA / CATALOG / CHECKPOINT IMPACT: optional unions; breaking trigger classified
MIGRATION IMPACT: retained context; no v0.8 alias
HG-01 CONSTRAINTS AFFECTED: native authority/no latent activation
CURRENTNESS RE-READ SET BEFORE WRITE: Files + seed/ledger/version/cursor
```

- [ ] RED `SpellClosedContractTests`: accept every exact supported branch and reject one extra field/foreign profile/illegal phase/reference per branch; require profile generations/typed references, separate stochastic/Wish unions, and no writable prospective delta. Object suspension accepts exactly the finite ruling; reject zero/dead plus overflow, caller residual, phantom original body, HP/location/death-progress on neutral principal, second temporary-HP amount or return resource amounts. Accept `[1,1]` rays. Reject executable state in `details`. Demonstrate current six-spell seed still validates while an unadmitted new profile remains nonexecutable.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_closed_contracts.py DEV/TESTS/test_s6d_05_portable_value_contract.py DEV/TESTS/test_s6d_06_activity_primitive_contract.py DEV/TESTS/test_rd16_world_family_machine_integration.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py`. STATIC_AUDIT + FOCUSED_BEHAVIOR; all GREEN, no support count.

## W05.SP02 — Source-authenticated sealed catalog, compilation and local lookup

**HARD_PRECEDES:** `W05_SPELL_CLOSED_MACHINE_SHAPES_READY` and accepted catalog/package binding checkpoint. **Output:** `W05_SPELL_SEALED_CATALOG_READY`: compiler/cache/index mechanisms verified on admitted conformance sources; full339 content/proof/adoption remains unestablished. **JOIN_BEFORE_INTEGRATION:** source/domain/recipe equality + this output -> final installed package loader/support writer.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/activity_runtime.py`, `DEV/TESTS/test_local_spell_catalog.py`, SP02 private fixtures. `EXISTING_MODIFY` `GAME/TOOLS/catalog_runtime.py` and `ruleset_package.py` only to reuse actual source-validation/freeze interfaces without weakening negatives. `INSPECT_ONLY` package seed/manifests/lock, engine inventory/comparator, source/native frontiers, existing catalog tests. The final integration task later adds `plan_next_segment` to this same module; SP02 does not add dispatch.

**Bounded compiler-source allocation:** independent Senior review in
`DEV/docs/superpowers/design/2026-10-06-sp02-compiler-source-allocation.md`
authorizes the missing immutable path-neutral compiler contract projection.
Reuse the canonical DEV family assemblers/identity producer via the minimum
`validate_ruleset_package_closure.py` generation/equality helper; NEW_CREATE
`GAME/TOOLS/activity_compiler_contracts.json` schema 1. Refine the existing
source input to authenticate inventory plus exact frozen projection, retaining
inventory schema 2 and BoundCatalogContext wire form where possible. Conditional
release-builder/schema/test alignment establishes installed source binding only.
Original source hash and sanitized projection verification stay distinct;
no handwritten duplicate registry, self-hash authority, production activation,
SP01 reopening or final SP28/SP29 writer transfer. The task Impact Envelope
includes precisely this producer -> projection -> compiler integration.

**Compiler ABI/source repair allocation:** the independent technical final audit
`DEV/docs/superpowers/design/2026-10-06-sp02-independent-integration-audit.md`
records the bounded extension to `activity_contracts.py` compiler-only DTOs and
`build_activity_contract_shapes.py`/generated structural projection, plus the
optional physical Activity compiler-declaration schema/primitive declaration
shape. Requirements/guards/scoped children/export associations and typed symbol
producer metadata implement existing accepted semantics, not an evaluator or
new admission registry. Source issuance binds the executing installed root and
owned semantic contents. Genuine legacy recipe/source gaps and the missing
Magic-action taxonomy hold only affected admission; they do not require SP03
or full339 content before compiler-mechanism qualification.

**Interfaces:** exact execution section 7 `admit_activity_catalog(context_request: object, *, package_snapshots: Mapping[str,PackageSnapshot], engine_contract_inventory_source: object, natural_owner_sources: object, compiler_generation: int, mode_policy_profile_id: str) -> AdmittedActivityCatalog`; `compile_activity(catalog: AdmittedActivityCatalog, activity_id: str) -> CompiledActivity`. Add pure `lookup_activity(catalog, activity_id: str) -> CompiledActivity` and `lookup_capability_cards(catalog, *, eligible_activity_ids: tuple[str,...], query: str, maximum_candidates: int) -> tuple[Mapping[str,object],...]`; the supplied IDs must come from the actual source-specific Actor availability projection, and the lookup grants no capability. Hydration returns only eligible catalog-card data for the caller's existing Context budget/disclosure route. Frozen source bytes, exact consumer/read/dependency/profile contracts and compiled cache identity are the section 3 contract, not mutable snapshot paths.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§2–5/7/10; mainSP01–04
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: catalog/package/Activity
EXPECTED OWNERS TO CHANGE: derived loader/compiler
EXPECTED CONSUMERS TO CHANGE: cold compile/local lookup
ALLOWED INTERFACES / CONTRACTS TO CHANGE: exact §7 + bounded lookup
GAME RUNTIME / PROJECTION SURFACES: activity_runtime/binder/package
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01; no production registry
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: handle/adoption; cache nonowner
VALIDATORS / TESTS / AUDITS: SP02 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: none
CROSS-WAVE JOINS: catalog command; final support
PROTECTED ARCHITECTURE INVARIANTS: frozen bytes/one digest/no census
ARCHITECTURE-SENSITIVE SURFACES: source seal/compiler identity
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: real binder->catalog->command
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: all339/grants/mutation/latency
VERSION IMPACT: new revision1; fresh changed owners
SCHEMA / CATALOG / CHECKPOINT IMPACT: no persistent cache; digest owner applies
MIGRATION IMPACT: disposable cache; retained source
HG-01 CONSTRAINTS AFFECTED: offline/bounded/context identity
CURRENTNESS RE-READ SET BEFORE WRITE: Files + source/lock/inventory/version
```

- [ ] RED `SpellSealedCatalogTests`: real source admission/compile succeeds; changed/forged snapshot/path cannot issue or relabel a handle. Mutate/remove the path after lawful issue: warm compiled object still uses frozen exact bytes; a new cold load validates and rejects unavailable authority. Unknown/dormant pair/profile/fact, unavailable transitive edge, cycle, bad branch bound/export/target/cost and wildcard member reject before casting.
- [ ] RED cache-key tests vary each typed set/context hash generation/value, Activity semantic hash/generation, engine inventory/compiler generation and compilation-sensitive mode/policy independently; unrelated owner change does not recompile. Corrupt derived object rebuilds from admitted bytes. Warm repeat performs zero package census/compile/online reads. Direct ID lookup and eligible alias narrowing do not hydrate all339 or hidden NPC cards; a broader catalog question grants nothing.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_catalog.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_s6d_06_activity_primitive_contract.py`. FOCUSED_BEHAVIOR + actual command INTEGRATION_SCENARIO.

## W05.SP03 — Pinned MechanicalContext, calculation policies and exact cast preflight

**HARD_PRECEDES:** `W05_SPELL_SEALED_CATALOG_READY`, `W05_T06_CURRENT_OWNER_VIEW_READY`. **Output:** `W05_SPELL_CONTEXT_CAST_CONSUMERS_READY`: bounded read/calculation/common cast preparation; no installed broad spell availability. **JOIN_BEFORE_INTEGRATION:** actual profile/pair/accessor/fact consumers + source-specific acquisition + lifecycle builders -> final catalog/host integration. Exact dormant IDs remain dormant outside those proved consumers.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/mechanical_context.py`, `calculation.py`, `spell_cast.py`, `DEV/TESTS/test_local_spell_context_cast.py`, SP03 private fixtures. `EXISTING_MODIFY` `GAME/TOOLS/current_owner.py` only if a compiled read-plan adapter cannot reuse `require(tuple[NativeOwnerRef,...])` unchanged; do not rewrite accepted P0 source admission. `INSPECT_ONLY` current mechanical-surfaces/accessor/pair schemas and ledger, class seed/acquisition, Actor/Asset/Procedure/HouseRules/adjudication owners. Shared production metadata stays with the final writer.

**Bounded policy/membership allocation:** independent Senior ruling and partial
read/cache review are recorded in
`DEV/docs/superpowers/design/2026-10-06-sp03-read-slice-and-policy-allocation.md`.
One serialized writer may realize missing finite four-policy/common-cast
carriers in mechanical-surfaces/profile/compiler-declaration schemas, compiler
DTO/retention/read plans and their generated structural/compiler projections.
NEW_CREATE `GAME/TOOLS/mechanical_sources.py` only for the minimum complete
native Effect/equipment/access membership read/revalidation adapter. Preserve
P0 exact reads; no caller ID-list/completeness flag, Actor copied inventory/
Effects, broad body scan, new state/currentness authority or production activation.
Actual complete source-backed conformance preparation may proceed without
waiting for SP04 establishment. Atomic production coverage/fencing joins the
native producer separately; missing coverage holds, never empty-set inference.
The existing inspect-only evaluator assignment is extended only by this explicit
serialized structural/source allocation, with actual namespace synchronization.

The subsequent independent bounded issuer ruling is recorded in
`DEV/docs/superpowers/design/2026-10-07-sp03-root-preparation-issuer-ruling.md`:
realize the missing authentic preparation factory through the existing bound
`CurrentOwnerView` source operation, native accepted command/root Resolution and
exact compiler bindings. Minimal `runtime_host.py` read-adapter, context issuance,
membership consumer enforcement and named test synchronization are admitted;
no host dispatcher, native producer or changed P0/admission/source precedence.
Root-only source-backed preparation and nested instructions within that root do
not prove a separate child Resolution or execution-branch acceptance. Genuine
distinct-child causal acceptance joins its native owner and remains held where
unavailable. Structural DTO construction/copying never issues authority.

Further bounded source realizations and their inspected limits are recorded in
the `2026-10-08-sp03-damage-input-preparation-ruling.md`,
`2026-10-08-sp03-ac-contract-allocation-ruling.md` and
`2026-10-08-sp03-capability-cast-source-allocation-ruling.md` design records.
Damage uses exact frozen compiled source and logical preparation identity,
not a fabricated native Health cause/ID; legacy primitive boundaries remain.
AC admits only the finite Mage Armor candidate/independent modifier/native Dex
route and honest unresolved-participation/controller holds. Capability/cast
source bindings are bound-definition nodes in the existing DAG; ordinary source
basis is not complete preflight. Read-only existing Procedure/turn/controller
joins and exact source descriptors may be realized under those envelopes;
no production activation, new persistent authority or reversed SP03->SP04 gate.

**Interfaces:** execution section 7 `evaluate_selector(compiled: CompiledActivity, selector_id: str, *, consumer_id: str, observation: CurrentOwnerObservation, role_bindings: Mapping[str,NativeOwnerRef], accepted_command: Mapping[str,object], prospective_documents: tuple[OwnerDocument,...] = ()) -> Mapping[str,object]`; prospective documents must originate from the same sealed builder. `calculation.calculate_selector(context: NativePreparationContext, selector_id: str) -> Mapping[str,object]` evaluates the closed policy/result/provenance. `spell_cast.prepare_cast(context: NativePreparationContext, transition: CastTransitionInput) -> PreparedNativeFragment`; `spell_cast.preflight_cast(context: NativePreparationContext, inputs: CastPreflightInput) -> Mapping[str,object]` returns a closed validated preflight decision, never authoritative caller state. SP04 issues production contexts; SP03 tests can use the SP01 trusted context issuer over real read observations, without claiming establishment.

Close the four selected policy profiles exactly, with complete pair/value/subject/normalization/composition/dependency/fact/conflict/trace contracts for each concrete consumer. Advantage/disadvantage cancels applicable contributions, damage defense preserves type/origin/bypass/order/rounding, AC chooses a legal nonadditive base, and capability projection reads source/current native form/equipment restrictions. Do not activate an entire rule.* family or accept model-computed bases. Common casting retains one slot expended to cast per turn, source exceptions, armor training, component access/free hand/focus/material substitution and DC/attack/slot/upcast rules. Physical origin, principal, source and each cost payer remain separate. Binding fault differs from a valid secret-invalid-target result.


Add exact golden assertions under reconciled SRD profile inputs: Charisma modifier3/proficiency2 -> spell DC13/attack modifier5; unarmored base10+Dex3=13 versus eligible Mage Armor13+Dex3=16, with legal Shield modifier5 ->21 rather than summing bases; 7 typed damage -> resistance3, vulnerability14, immunity0, and both applicable resistance/vulnerability ->6 in source-defined order. Preserve raw/result provenance and damage-instance/group identity. These fixtures never supply an engine-owned base through adjudicated input.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§4–6; mainSP05/07/15/24
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: context/calculation/native/cast
EXPECTED OWNERS TO CHANGE: pure context/cast
EXPECTED CONSUMERS TO CHANGE: exact policy/read/fact/cast
ALLOWED INTERFACES / CONTRACTS TO CHANGE: listed APIs/four policies
GAME RUNTIME / PROJECTION SURFACES: three modules; P0 adapter if needed
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01; final registry writer
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: revisions/facts/policy; no cache truth
VALIDATORS / TESTS / AUDITS: SP03 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: none
CROSS-WAVE JOINS: P0/acquisition->native/final
PROTECTED ARCHITECTURE INVARIANTS: one DAG; native state not fact
ARCHITECTURE-SENSITIVE SURFACES: pair/fact/payer/hidden target
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: P0->compiled DAG->preflight
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: time/establishment/import/P1A/Wish
VERSION IMPACT: new revision1; P0 only if changed
SCHEMA / CATALOG / CHECKPOINT IMPACT: no new record/status/cache
MIGRATION IMPACT: accepted fact/policy unchanged
HG-01 CONSTRAINTS AFFECTED: pin before RNG/no probe/refund
CURRENTNESS RE-READ SET BEFORE WRITE: Files + pair/fact/acquisition/version
```

- [ ] RED `SpellMechanicalContextTests`: finite accumulated read union reacquires all keys; changed earlier relevant owner invalidates, unrelated owner does not. Real canonical health/resource cycles and unauthorized transitive fact reject. False remains false; missing remains typed input failure. Caller HP/AC/resource/condition substitution, wrong binding kind/foreign owner Effect and index-only empty-set proof reject. Cache equality includes relevant source revisions, exact bindings/facts and sorted material policy refs; suspension recomputes.
- [ ] RED `SpellCalculationPolicyTests`: multiple advantage contributions plus one disadvantage cancel; raw-dice identity/provenance remains intact. Test exact typed resistance/vulnerability/immunity/bypass/rounding and nonadditive AC choice under independently reconciled current source; ensure order of caller Contributions cannot select a different outcome. Test grant/restriction/form/anatomy/equipment and movement/sense projection with correct native roles and illegal pair/fact negatives.
- [ ] RED `SpellCastPreflightTests`: actual selected prepared/known source and current action/slot/components/hands/focus/armor/material price/consumption checks; an unselected legal spell is unavailable. One-slot-per-turn and exact exception/slotless distinction; range is not a universal ongoing leash. Secret-invalid creature/object target preserves specified action/slot/component/no-effect and safe apparent-save-success outcome; malformed/missing reference rejects before spend. Reject caller resource truth, free type probe and blanket failure refund.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_context_cast.py DEV/TESTS/test_s6d_04_mechanical_context_contract.py DEV/TESTS/test_s6d_05_portable_value_contract.py DEV/TESTS/test_s6d_06_activity_primitive_contract.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py DEV/TESTS/test_rd15_catalog_runtime.py`. FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO; independent source checks accompany arithmetic fixtures.

### SP03 accepted auth/turn reconciliation — implementation-plan review candidate

> **For agentic workers:** use `subagent-driven-development` when bounded independent workers are available, otherwise `executing-plans`; use TDD for each behavior change. This is part of SP03 in this stable plan, not a second executable plan.

**Goal:** prepare the accepted original-input/current-authority and common actual-turn contracts, with complete strict source/read consumers, then transfer native establishment obligations to the existing SP04 writer.

**Architecture:** native Interaction/Message/Plan/clause, command or real Resolution, Procedure and Actor retain their existing ownership. Source validators and immutable contract preparation may precede the kernel; only the native kernel accepts coupled semantic changes. Infrastructure authentication and actual-turn dependencies are not MechanicalContext facts or synthetic gameplay roles.

**Tech stack:** existing standard-library GAME Python, JSON Schema/installed assertion projection, trusted bound RuntimeHost, P0 finite read sessions, existing SQLite/LIVE fences and repository-owned DEV test environment. Add no runtime dependency or test framework.

**Spec:** `DEV/docs/superpowers/specs/2026-10-14-sp03-authenticated-input-canonical-spec.md` (A) and `DEV/docs/superpowers/specs/2026-10-14-sp03-common-turn-gate-canonical-spec.md` (B), read in full. Retained evidence: `DEV/docs/superpowers/design/2026-10-14-sp03-auth-turn-history/{case-source-ledger,resolution-review,stage8-closure}.md`; AT6-01..04 remain closed requirements, not executed implementation proof.

**Gate:** independent AUTH_TURN Stop2 GO is supplied by the planning assignment, session `ses_ec4669fdeffeEgdXm9m8BF8ciG`, published source commit `c3e7b9ad27af0dc62eacec37a86356d090954082`, tree `d8d65037839bb0662693212546f656b0aaec3b9e`, parent `92aa8ce2bc432e9213395595c725374382dd5e3b`. This is historical source evidence, not a target development ref. The source spec/control headers still describe the earlier pending state; the publication coordinator owns their gate/currentness synchronization. **Proposed Senior implementation-plan GO: PENDING.** The older whole-plan GO does not self-approve this changed envelope. No production changes are authorized by this candidate.

#### Global constraints and ordering

- Preserve all accepted SP03 policy/source/read work and all original 32 local-spell tasks. Four subunits below are reviewable slices within SP03; the three named joins below belong inside SP04. They add no task/readiness ID, output checkpoint, roadmap, execution cursor or new task graph.
- Retain `SP02 -> SP03 -> SP04`. SP03 output means source/bridge/read preparation conformance, not native mutation or connected authentication. SP04 consumes it and proves actual establishment; SP03 must not wait for that downstream proof to publish its preparation output. Existing full SP03 obligations outside this amendment still apply.
- Source bytes, verified flag, DTO, hash, random invocation key, publisher identity, method existence or private seal are insufficient external authentication. Deployed supported issuer evidence remains **UNAVAILABLE**. A trusted-composition fixture may prove the contract implementation, never deployment; absent installed capability returns `AUTHORITY_UNAVAILABLE` before protected work/RNG/cost. Do not invent a fixed deployed DTO or substitute another transport.
- Actual GAME creation admission/start/initialize/reset/slot native producer remains **NOT_ESTABLISHED** until SP04 witnesses below. DEV transitions, temporal evaluation, Actor shape admission and synthetic ExecutionStore events cannot close it.
- No new CurrentOwner service/authority, AUTH store, registry/family, ActorGate owner, full-history authority, session lease, extra dedicated model call, broad campaign/Player/LIVE scan, eager reset, generic callback/patch mechanism or always-publish-arrival policy.
- Historical accepted input and current operation authority are independent. Retry first validates the stored identity/result; new protected work separately reacquires current principal/access/purpose/control. Creator singleplayer uses HistoryService's native first-initialization evidence and current login, without a Player. Outbound disclosure remains recipient-qualified.
- Closed variants reject forbidden fields even when empty/null. Integer generations/revisions reject bool. Native envelope identity wins; conflicting flattened aliases reject. Unknown newer schemas/profiles fail closed. Same-I mixed phases preserve irreducible extra meaning and cannot replay a response.
- Each schema cutover includes its producers, parsers, consumers, fixtures, installed projections and current identities in the same checkpoint. A protocol-only activation followed by a later required repair is not a safe checkpoint. Source conformance can exist without production issuance; no stub success or permanently disabled half-migration.

#### Inspected implementation basis and exact owner route

All locations in this paragraph were inspected on the source commit above; line numbers are locators, never patch instructions after intervening changes. `runtime_execution.py:1045–1307` accepts/validates only actions and hashes a fixed action field set. `mechanics.py:522–594,958–963` repeats that codec and schema2 Procedure assumption. `runtime_host.py:1675–1966` issues root-only contexts from K/R/roles, explicitly excludes Procedure/Continuation/progressed work, and does not read I/M/P or original/current author authority. `activity_contracts.py:540–715` independently checks exactly K/R/roles; `spell_cast.py:184–288` independently adds Effect/Asset membership to that old base. These three derivations must change together; removing the exact-union check is forbidden.

`recovery_roots.validate_unresolved_input_owner` requires Player/P, treats any response emission as resolved and returns M as I identity. `durability.RoutedSerializedOperation`, `_handoff_owner_id` repeat M-as-I. `native_storage.native_identity_from_record` already uses envelope.id; preserve WP11 routes. `durability.join_execution_durability` requires one R and event, reads flattened catalog generation, and constructs action-only policy basis. `publication._accepted_identity` and its policy forwarding, `recovery.validate_recovered_basis`, `_validate_recovered_root_closures`, `_hydrate_execution_result`, `_validate_catalog_closure`, `_accepted_policy_refs` repeat those assumptions. `collaboration._load_interaction`, `_load_clause`, `_CLAUSE_FIELDS`, `associate_input`, `_validate_persisted_input_owners` and `_validate_historical_input_associations` need variant/unit-aware validation, while retaining current versus historical agency separation.

`information._normalize_emission:280–363` is the actual outbound Message producer and currently emits no state schema_version: qualify it with initial1 when W02 changes, keeping recipient/disclosure law. `emission.commit_visible_payload:129–219` is the recipient-bound visible surface, not an inbound issuer or compactor; keep it inspect-only unless a concrete retained-input consumer join requires a change. No GAME compaction/retention/protection/garbage-collection module or corresponding dedicated DEV schema exists at this source basis. Do not name an imaginary existing compactor as a hook. Narrow native I/M/R/Actor source-retention and sufficient-survivor validation belongs in these existing owners/kernel joins: same-domain root/reference/retained bytes fence together; cross-source dependence needs the admitted existing freeze/self-containment/protection capability or holds before acceptance. A generic cleanup/protection engine is out of scope. Negative race probes mutate the exact test source between observation/final fence and demand hold; positive compact cause probes establish sufficient native survivor bytes through the actual kernel and recover them. Neither is a claim that a general cleanup producer has been implemented.

`access_control.resolve_principal` accepts trusted mappings/VerifiedPrincipal; its `verified` default is not an external issuer. Reuse `resolve_player(principal, route, load_exact_player, *, campaign_id)` and `authorize_operation(..., operation=..., creator_provenance=..., campaign_id=...)` behind trusted infrastructure, validating complete route plus every nominated native Player envelope/state and exact controlled subject. Do not relabel these helpers as deployed authentication. `RuntimeHost._begin_operation` currently pins campaign/LIVE only; composition is `compose_runtime_host(..., hot_owner_store=None)` / bootstrap's selected-host route. Any admitted input capability is bound there, never in a gameplay request. `HistoryService.observe_first_initialization_history()` is the creator source; no History seal reconstructed from stored fields.

`DEV/TOOLS/validate_domain_rules_coverage.py:198–275` owns DEV seven-transition conformance: initialize/start/spend_action/spend_movement/end/advance_round/terminate; state2, unqualified after-digest and synthetic `resolution:{key}` IDs currently occur there. Its `advance_combat_turn` helper is not that lifecycle and must not be composed into production. `runtime_execution._validate_linked_procedure`, `mechanics._validate_procedure_binding`, `recovery_roots._validate_native_owner` hardcode schema2. Generic `runtime-procedure-state` is closed spent-only schema2, unlike concrete capacity/spent state2. B admits concrete3, not a global rewrite of generic2.

**Read before each relevant subunit:** A/B plus Step3; Step5.2 v2 resumable closure, Step5.4 handoff, Step5.11 retention, Step5.13 protection; WP11 routing, WP12 HOT, WP13 publication, WP14 recovery, WP16 authority/LIVE, WP17 agency, WP15 independently-due enrollment; creator-login continuity decision and current version/clean-slate owners. PROJECT_MAP and CANONICAL_ARCHITECTURE_INDEX are locators only. Re-read the actual current code/schema/test owners named here before editing them. Accepted source interpretations A–F and original lifecycle/cast owners remain binding; this plan adds no source rule.

#### Complete Implementation Impact Envelope

```text
SPEC / APPROVED DESIGN: final A §§1–7; final B §§1–6; existing local-spell execution/lifecycle contracts
BASELINE SHA / TREE: c3e7b9ad27af0dc62eacec37a86356d090954082 / d8d65037839bb0662693212546f656b0aaec3b9e
IMPLEMENTATION START HEAD: record fresh exact published source after independent plan GO; refresh affected owners
PRIMARY OWNER ARTIFACTS: A/B; existing Step3/Step5/WP11–17/access/creator/version owners
EXPECTED OWNERS TO CHANGE: native input/interpretation/command codec; Procedure subtype/turn cause;
  Actor common gate companion; existing root/promise/hydration/collaboration validators;
  immutable contract/compiler/source/read preparation; SP04 alone native coupled establishment
EXPECTED CONSUMERS TO CHANGE: Host + independent activity validation + spell membership;
  mechanics/durability/publication/recovery; native-storage adapters; Actor continuity;
  exact response/mixed clause/use and retention/protection consumers
ALLOWED INTERFACES / CONTRACTS TO CHANGE: exact signatures and wire matrix below; one input codec3;
  action-R/direct-K projection1; input/resume1; concrete3/generic2 dispatch;
  Actor3 strict companion; phase-derived finite infrastructure union; trusted composition binding
GAME RUNTIME / PROJECTION SURFACES: runtime_execution, runtime_host, bootstrap, activity_contracts,
  activity_runtime, catalog_runtime, mechanical_context, mechanical_sources, spell_cast, mechanics, durability,
  publication, recovery, recovery_roots, native_storage, actor_continuity; hot_store/live_state
  only for the SP04 named native acceptance/protection joins; temporal/information/emission only
  for exact occurrence or retained input/recipient validators, never new owners
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: W01–W19 disposition matrix; Actor envelope/state,
  spell-native-profile-values, concrete request/result, existing compiler declaration/inventory
  source members; generated activity_contract_shapes.json/activity_compiler_contracts.json
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: own-I phase roots; same-source closure/fence;
  command/direct/response/mixed hydration; exact native compact causes/protection;
  current source first, no accepted-mechanics replay or serialized capability revival
VALIDATORS / TESTS / AUDITS: four SP03 subunit suites, three SP04 joins; existing RD03–07/09/10/12/14/15,
  S6D04/05/06/09/11, compiler/version/package suites; full unittest/pytest/audit/build
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: module headers + generated installed assertions/compiler
  package/inventory metadata via existing producer; public README untouched; final CORE/install T08 remains
CROSS-WAVE JOINS: existing P0/SP02 -> SP03 prep -> SP04 native -> existing SP06/SP07/SP28 and W06 proof;
  shared physical writer serialized with P2/P3; no full P2 native proof before SP04
PROTECTED ARCHITECTURE INVARIANTS: one native truth/codec/mutation/RNG; complete route/current control;
  no auth/current-owner/gate registry; no synthetic rootR; same-I mixed meaning;
  no publication/DB transaction across external wait; CAS before HOT adoption; survivor before loss
ARCHITECTURE-SENSITIVE SURFACES: issuer TCB, original vs current agency, root release, digest identity,
  subtype dispatch, common gate subject/cost cause, local/LIVE acceptance, retry/compaction races
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: exact 63-case and 19-wire bindings below;
  final source->command/response->native->durability->publication->cold recovery on real kernel
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: new transport/provider, general auth/ACL/delegation, general
  Procedure ordering, import certification, migration fabricated causes, all339 activation,
  History gameplay authority, Story, full host dispatcher (SP28), new temporal scheduler
VERSION IMPACT: documentation reconciliation NONE; realization transitions and per-checkpoint ledger below
SCHEMA / CATALOG / CHECKPOINT IMPACT: no new family/status/root kind/output ID; exact existing contract cutovers
MIGRATION IMPACT: clean-slate pre-v1 replacement, no compatibility shim; released adoption reopens proper gate
HG-01 CONSTRAINTS AFFECTED: bounded source reads/context; pre-RNG authority; no secret-target free probe/refund;
  zero added dedicated model phases, no broad scan or mandatory per-arrival repository publication
CURRENTNESS RE-READ SET BEFORE WRITE: specs/retained cases + all actual owner/consumer bytes in subunit,
  version metadata/namespace owners; current coordinator gate/cursor and accepted previous checkpoints
```

**File-action rules for this amendment:** all named existing modules/schemas are `EXISTING_MODIFY` only where their subunit requires a material delta; `current_owner.py` remains the existing read-session implementation, not a new owner. Source-compatible wire rows explicitly marked verify-only remain `INSPECT_ONLY` unless a failing admitted contract proves a needed bounded edit. `NEW_CREATE` only the two conformance test modules `DEV/TESTS/test_sp03_authenticated_input.py`, `DEV/TESTS/test_sp03_common_turn_gate.py` and their private data fixtures; native tests/harness stay SP04-owned as already declared. New helpers live in the existing natural owner modules, not an AUTH package. Existing SP03 files in the older NEW_CREATE list now exist: modify them, do not recreate them. Every touched GAME surface is `V1_COMPATIBLE` accepted v1 law; old mandatory Player/P, action-only codec and concrete2 checks are `MIXED` surfaces with the specifically superseded fragment replaced, not preserved as a dual-read path.

#### SP03 subunit 1 — own-I and phase-correct input/root closure first

**Deliverable:** deterministic native source parsing, root/promise routing and recovery closure support for all input variants, independently testable without a MechanicalContext DAG, executable command or native kernel. This repairs identity/discoverability before new acceptance can escape. It does not issue authenticated input or consume offers.

**Files:** modify W01–W04 schemas as a coherent initial-schema1 contract, `runtime_execution.py` pure input grammar, `recovery_roots.py`, `durability.py` (`RoutedSerializedOperation`, `_handoff_owner_id`, promise freeze), `recovery.py` (root/input hydration), `native_storage.py` only envelope adapters that still flatten incompatible identity; `collaboration.py` strict input/clause loaders; `information.py` outbound Message initial1 and narrow native content validators. `emission.py` remains inspect-only absent a proved retained-input join. Add tests in `test_sp03_authenticated_input.py`; extend `test_rd02_information_native_contracts.py`, `test_rd05_operational_roots.py`, `test_rd06_durability_publication.py`, `test_rd07_recovery.py`, `test_rd12_collaboration.py`. No native mutation builder in this slice.

**Interfaces:** preserve `route_native_record`, `validate_loaded_identity`, `validate_unresolved_input_owner(campaign_id, owner_kind, native_owner)->str`, `route_serialized_operation(owner_kind, owner_id, payload)->RoutedSerializedOperation` and `issue_durability_handoff_promise` signature. Add owner-local pure `runtime_execution.validate_input_closure(*, campaign_id: str, interaction: Mapping[str, object], message: Mapping[str, object], plan: Mapping[str, object] | None, accepted_response_segment: Mapping[str, object] | None) -> None`. Inputs are native envelopes from exact reads; shape validation here is not authentication/current authority. It checks I/M reciprocity, representation and phase-dependent links; native response proof is separately required for a trusted protected acceptance. Root predicate uses this grammar plus actual owner-issued promise, never response emission alone. Unpromised arrivals do not enroll.

- [ ] RED own-I route test with envelope `id=interaction-1`, `input_message_id=message-9`, current native I/M bytes and accepted promise. Assert root owner_id and route use `interaction-1`; `route_serialized_operation('runtime.interaction','message-9',I)` rejects. Test MP and creator variants; no Player is read for creator. Existing M-as-I code fails for the intended reason.
- [ ] RED phase matrix: intent requires P; pure response forbids P; mixed awaiting forbids P/ref; ready requires genuine ref/marker but forbids P; materialized requires same-I complete P/ref. Response emitted while ready remains unresolved; missing materialized P or missing exact unplanned M yields recovery BLOCKED/INCOMPLETE, not resolved/default text. No fake normal K for response.
- [ ] GREEN parse native envelope before state, require alias equality, enforce A§§2/5 closed grammar. Use `id` as I owner, never M. Root/promise/loaders share phase predicates; keep existing four root families and root1/handoff2 wire. Establish all required I/M/result/protection routing in promise closure; permit P absence only in the lawful phases. Retain roots until downstream bounded discovery/meaning discharge, including nonexec collaboration units.
- [ ] GREEN enforce inbound M has no recipient/delivery evidence, outbound retains old recipient/emission law, compacted M forbids exact_text. Exact retained UTF-8 digest must match I; unplanned meaning cannot compact to a hash. Incomplete protection/negative proof retains. Unknown/duplicate plan clause IDs/order or copied marker mismatch rejects.
- [ ] Run module command S1 below, then root/durability/recovery/collaboration modules in full. Review the actual delta, classify versions, run checkpoint checks and publish only coherent GREEN consumers under later execution authorization. This candidate does not publish.

Concrete root-first regression construction (uses existing public promise/routing APIs; install complete A§2 valid source fixture in this test module, not an issued seal):

```python
text = 'Choose A; then move'
digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
interaction = {
    'kind': 'runtime.interaction', 'id': 'interaction-1',
    'state': {
        'schema_version': 1, 'campaign_id': 'campaign-1', 'session_id': 'session-1',
        'player_id': 'player-1', 'input_message_id': 'message-9',
        'input_kind': 'response_and_intent', 'planning_phase': 'awaiting_response',
        'accepted_input_basis': {
            'basis_generation': 1, 'repository_identity': 'fixture-repository',
            'adapter_profile_id': 'fixture.input', 'adapter_profile_generation': 1,
            'accepted_exchange_key': 'exchange-1', 'host_invocation_ref': 'invocation-1',
            'principal': {'provider': 'github', 'stable_account_id': '123',
                          'login_at_acceptance': 'fixture-player'},
            'representation': {'kind': 'accepted_text', 'digest_generation': 1,
                               'content_digest': digest},
            'authority_at_acceptance': {
                'kind': 'multiplayer', 'player_id': 'player-1',
                'accepted_subject_ids': ['actor-1'], 'campaign_authority_revision': 'access-1',
                'player_revision': 1, 'route_evidence_revision': 'route-1',
            },
        },
        'response_target': {'root_command_id': 'command-1', 'resolution_id': 'resolution-1',
            'continuation_id': 'continuation-1', 'continuation_generation': 1,
            'offer_kind': 'choice', 'offer_id': 'offer-1', 'responder_id': 'actor-1'},
        'response_selection': {'kind': 'choice', 'option_id': 'option-A'},
    },
}
message = {'kind': 'runtime.message', 'id': 'message-9', 'state': {
    'schema_version': 1, 'message_id': 'message-9', 'interaction_id': 'interaction-1',
    'direction': 'inbound', 'input_basis_generation': 1, 'representation_kind': 'accepted_text',
    'payload_state': 'message.exact_retained', 'exact_text': text, 'content_digest': digest,
}}
# These are explicit test source bytes for shape/root tests, not authentication proof.
validate_input_closure(campaign_id='campaign-1', interaction=interaction,
    message=message, plan=None, accepted_response_segment=None)
promise = issue_durability_handoff_promise(
    campaign_id=interaction['state']['campaign_id'], owner_kind='runtime.interaction',
    native_owner=interaction, scope='handoff',
)
page = enumerate_operational_root_page(
    interaction['state']['campaign_id'], [('runtime.interaction', interaction, promise)],
)
self.assertNotEqual(interaction['id'], interaction['state']['input_message_id'])
self.assertEqual(page.roots[0].owner_id, interaction['id'])
self.assertEqual(page.roots[0].relative_path,
                 route_native_record('runtime.interaction', (interaction['id'],)).relative_path)
```

Construction is not a fixture that sets `accepted=True`: write actual closed I/M envelopes and exact phase; the promise issuer must validate source grammar. For ready/materialized positives, initially test retained native source validation only; production-issued marker/atomic acceptance belongs to SP04 join 2. Reject caller-authored success fields.

Required schema construction in W01 (in addition to A's complete closed field/type definitions) includes these phase conditions; native validators enforce equal cross-record identities and actual proof:

```json
{"allOf":[
  {"if":{"properties":{"input_kind":{"const":"response"}},"required":["input_kind"]},
   "then":{"required":["response_target","response_selection"],
           "not":{"anyOf":[{"required":["intent_plan_id"]},{"required":["planning_phase"]}]}}},
  {"if":{"properties":{"input_kind":{"const":"response_and_intent"}},"required":["input_kind"]},
   "then":{"required":["response_target","response_selection","planning_phase"]}},
  {"if":{"properties":{"planning_phase":{"const":"awaiting_response"}},"required":["planning_phase"]},
   "then":{"not":{"anyOf":[{"required":["intent_plan_id"]},{"required":["accepted_resume_ref"]}]}}},
  {"if":{"properties":{"planning_phase":{"const":"ready_to_plan"}},"required":["planning_phase"]},
   "then":{"required":["accepted_resume_ref"],"not":{"required":["intent_plan_id"]}}},
  {"if":{"properties":{"planning_phase":{"const":"materialized"}},"required":["planning_phase"]},
   "then":{"required":["intent_plan_id","accepted_resume_ref"]}}
]}
```

Do not rely on `if.properties` without `required` (absent discriminator otherwise matches); intent separately requires P and forbids response/phase/ref. Authority union separately requires MP.player_id equality or creator no-Player. Test missing/null/extra fields in each branch, plus ready noP lawful versus materialized missingP defective, through both installed and DEV schema validators.

#### SP03 subunit 2 — trusted origin/current authority and one action/direct codec cutover

**Deliverable:** source-backed preparation validates protected accepted origin and current requested authority; all action/direct identity consumers agree on schema4/hash3. Independently testable TC contract with explicit missing-deployed-issuer hold. Exact source origin validation does not manufacture native acceptance.

**Files:** `runtime_execution.py`, `mechanics.py`, `durability.py`, `publication.py`, `recovery.py`, `runtime_host.py`, `bootstrap.py`, `activity_contracts.py`, `mechanical_context.py`, `mechanical_sources.py`, `spell_cast.py`; W05/W06 and W07/W09 initial schema fields; W16 verify only. `access_control.py` only minimum exact envelope/control adapter validation, without changing its underlying creator or account rules. Add S2 tests and update existing RD05/06/07/09/14/15/Host/compiler fixtures and installed schema/compiler projections in the same checkpoint. Do not leave mechanics/recovery running codec2 after the schema4 producer switch.

**Exact planned interfaces in existing owners:**

```text
# runtime_execution.py; new pure source helpers, not authority issuers
def accepted_input_origin(*, campaign_id: str,
    interaction: Mapping[str, object], message: Mapping[str, object],
    plan: Mapping[str, object], clause_id: str,
    accepted_response_segment: Mapping[str, object] | None = None,
) -> Mapping[str, object]

def command_input_fingerprint(command: Mapping[str, object], *,
    origin: Mapping[str, object]) -> str

def execution_identity(command: Mapping[str, object], *,
    execution_owner_kind: str, execution_owner_id: str,
    segment: Mapping[str, object]) -> Mapping[str, object]

# extend existing command entry points; required keyword prevents old unbound calls
def accept_command(interpreter_result: object, context: BoundCatalogContext,
    candidate: object, command_proposal: object, *,
    input_observation: CurrentOwnerObservation,
    adjudication_basis: AcceptedAdjudicationBasis | None = None,
) -> dict[str, object] | CatalogGap

def validate_execution_proposal(accepted_command: object,
    context: BoundCatalogContext, candidate: object, *,
    input_observation: CurrentOwnerObservation,
) -> None
```

These are target signatures, not existing installed APIs. Implement bodies from the construction below; the signature listing is not executable stub code. `input_observation` must belong to the bound Host's current operation and exact source session; copying a dataclass/acceptance flag cannot issue it. Host entry authenticates with its bound infrastructure capability and owner access checks; pure helpers only validate native sources. Recovery rebuilds a read observation from current selected sources, validates historical origin, and applies current auth only for requested new protected work. For direct dispatch `interpreter_result` and `candidate` are `None` and forbidden in serialized command; exact native profile/schema binding is loaded from admitted inventory. Action uses the existing actual interpreter/candidate binder. No fake Activity/interpreter for a transition.

`join_execution_durability(accepted_command, execution, promise, *, routed_operation)` keeps its call signature. Replace its action-only identity members with exact `execution_identity` projection1, including event_ids (possibly empty on an admitted eventless edge); retain catalog/policy/RNG/routed-operation evidence. Update its `to_dict` and every `_accepted_identity`/recovery consumer together. Actual action result alone carries resolution_id; direct carries command owner and no resolution_id. Do not set resolution_id=K or manufacture an event to fit the old constructor. Policy basis is a closed variant: action_request OR transition_request+transition_binding, plus actual invocation_facts/policy_refs. Preserve nested `BoundCatalogContext.to_dict()` and its `basis.catalog_generation` validation, synchronized with PT-D1; do not flatten it.

- [ ] RED actual native I/M/P/C/K/R source test at root preparation, not a fact-read test: remove origin, change M, foreign campaign/host/session association, replace P/C/command reciprocity, duplicate clause, response clause as K, alter action roles/targets/facts/context. Each fails before preparation/RNG/cost. Historical session remains a link, not an executor lease.
- [ ] RED current authority matrix: complete native account route nominates all Players; inactive, duplicate, rebound, omitted/invalid envelope/state, lost subject control fail. Creator uses real HistoryService first-init discovery and current login, no Player; rename/Admin/stable-ID shortcut fails. Old historical author/result remains after revocation; new voluntary work requires fresh exact purpose/control and executor mapping. Automatic mandatory child has real native causal mapping or holds.
- [ ] GREEN bind optional infrastructure-only accepted-input capability at existing Host/bootstrap composition. Its required conformance operations are exact exchange lookup (repository/campaign/profile/key), current acting principal, and exact accepted representation/invocation/retry mapping; gameplay cannot provide/replace the capability or verdict. No current supported deployed implementation has been evidenced: absence is a typed hold, not a fake principal adapter. TC fixture implements those contract operations under trusted constructor composition and persists its retry mapping in its own test infrastructure; native I is the protected source, no product auth registry/store. Lookup nominates I before ambient rebinding; validate exact native basis/result and present read eligibility. Key reuse with changed origin/content conflicts; new intentional equal prose gets new I/M.
- [ ] GREEN derive origin from observed native I/M/P/C (and exact mixed prior marker), not command.shadow_origin. Require exactly one reciprocal C; precommand held clauses have no command_id. Hash complete closed action/direct material below. Mechanics imports the one runtime_execution codec; remove its competing field/domain implementation. Dispatch kind before fields, catalog policy and hydration. Pending direct with no segment is recoverable typed work, not corruption or replayed facts.
- [ ] GREEN change Host, independent activity validation and membership base union together to base execution refs ∪ phase-required input refs ∪ full route-nominated Player refs ∪ owner-native refs; membership then adds its declared complete Effects/Assets. Infrastructure creator/principal/config evidence remains external source evidence, not fake role/fact. Each expansion reacquires the entire accumulated union; final source/control revalidation and wait invalidation remain mandatory. Source-sensitive cache includes origin/unit/resume/current subject/binding, not global revision.
- [ ] Run S2 and existing action/direct acceptance, durability, publication, cold recovery, Host/source membership suites. Exact codec3 mutation tests must fail even when attacker recomputes a plain hash: forged native origin/cross-links still reject. Freeze and review full synchronized checkpoint.

Codec construction (after closed native/profile validation; these are complete algorithms, not constant-success bodies):

```python
common = {'command_kind', 'catalog_context_fingerprint', 'catalog_context', 'invocation_facts'}
variant = {
    'action': {'action_request', 'interpreter_result',
               'interpreter_result_fingerprint_generation',
               'interpreter_result_fingerprint', 'candidate_binding'},
    'transition': {'transition_request', 'transition_binding'},
}[command['command_kind']]
material = {key: thaw(command[key]) for key in common | variant}
material['accepted_input_origin'] = thaw(origin)
digest = hashlib.sha256(b'HDM_RUNTIME_COMMAND_INPUT/3\n' + json.dumps(
    material, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
    allow_nan=False).encode('utf-8')).hexdigest()
```

Use the existing `_thaw`/canonical_json implementation, checking allow_nan=False; the sketch's `thaw` is that operation, not a new serializer. Test each direct payload target/destination/amount/kind/profile/schema and all origin members independently; diagnostic/segment/result/planning progression is excluded. Origin mixed ref is prior accepted provenance and included; pure response cannot create ordinary K. The exact projection is `{identity_generation:1, command_id, input_fingerprint_generation:3, input_fingerprint, execution_owner_kind, execution_owner_id, segment_id, event_ids}`. Root/segment reciprocal linkage is separately validated, never inferred from hash equality.

#### SP03 subunit 3 — response/mixed interpretation, collaboration and retention conformance

**Deliverable:** strict response marker/hash, same-I phased interpretation and protected promise/retention source validation; offers remain offers. Read-only/source conformance does not consume, materialize a current P or certify atomicity.

**Files:** `runtime_execution.py` response/origin validators, `recovery_roots.py`, `durability.py`, `recovery.py`, `collaboration.py`, inbound retention helpers in `information.py`/`emission.py` as required; W01–W04/W07/W09 changes integrated with all strict consumers and generated projection. Verify W08/W10–W16 unchanged wire where sufficient. Add S3 tests and RD05 roots/RD07/RD12/RD10 retained-content tests. Preserve existing complete guard/class/disposition/collection grammar, not a reduced replacement plan.

**Interfaces:** add `runtime_execution.resume_input_fingerprint(*, interaction: Mapping[str, object], message: Mapping[str, object]) -> str`, validating exact A§4 target/selection and I/M representation. Extend `validate_input_closure` from subunit1 with native marker/ref validation. Keep `collaboration.associate_input(obligation, host, interaction_id, clause_id, *, principal, player_route, generation=None)` signature; its public principal/route arguments cannot be new authority, so compare/reacquire through the trusted Host operation before protected association. Current association authorizes present agency; historical-use validation checks fixed accepted native origin/meaning without reauthorizing the old author.

- [ ] RED pure choice/reaction I/M has fixed target/selection and no P/K. `pending_response` alone cannot pass accepted provenance. Resume marker requires protected source issue, same I/M/root/R/G/offer/responder/selection; new I on consumed G is stale, even with equal selection.
- [ ] RED mixed awaiting→ready→materialized source cases with same I/M. Ready has no P; materialized exactly one response clause and ≥1 real extra unit, actual canonical clause.intent.N order, fixed old resume ref. Reject dummy P, P replacement, response clause command/guard/payload, changed input_kind after issue, response replay to plan extras, loss of nonexec/OOC/held material.
- [ ] GREEN resume hash1 uses exactly `response_interaction_id,response_message_id,input_kind,accepted_input_basis,target,selection` and domain `HDM_ACCEPTED_RESUME_INPUT/1\n`, existing canonical JSON; phase/P/C/K are excluded. Serialized `accepted_resume_input` lives only in the real consuming R segment and `accepted_resume_ref` only on I after accepted consume. Strict source validation cannot issue either; production writer is SP04 join2.
- [ ] GREEN preserve accepted interpretation and extra semantics separately from response meaning. Reference-only collaboration associates `(I, clause.intent.N)` with exact class/content/G/purpose/control, never `(I, clause.response)` as actionable consent. No-K coordination is valid; creator cannot be coerced into a fake multiplayer contributor. Missing current MP participation returns existing scoped failure/hold, not invented Player.
- [ ] GREEN promised ready phase retains exact M or admitted equally sufficient exact natural owner and native response closure before durability acknowledgement. I root releases only after P/K/use/history closure gives bounded discovery of every remaining unit; response emission/root settlement alone cannot release it. Compaction/protection validates both response retry and each extra unit; survivor first, release may lag. No full-history scan or hash-as-content.
- [ ] Run S3. Keep all TC assertions separate from NP injection/crash evidence in SP04; no expected-failure future native tests enter this checkpoint.

Concrete property assertions for subunit3 (in a unittest.TestCase, using complete native source fixtures built in this module):

```python
before = resume_input_fingerprint(interaction=ready_i, message=inbound_m)
materialized_i = deepcopy(ready_i)
materialized_i['state']['planning_phase'] = 'materialized'
materialized_i['state']['intent_plan_id'] = plan['id']
self.assertEqual(before, resume_input_fingerprint(
    interaction=materialized_i, message=inbound_m))
self.assertEqual(plan['state']['interaction_id'], ready_i['id'])
self.assertEqual([c['clause_id'] for c in plan['state']['clauses']],
                 ['clause.response', 'clause.intent.1'])
self.assertNotIn('command_id', plan['state']['clauses'][0])
```

Construct mixed fixture from retained whole-message text `Choose A; then move` with actual option A, fixed native result and real extra transition clause; use response+OOC text for no-K case. Do not allocate a second I/M, create a fake response Activity or infer command consent from transcript prose. A matching marker hash does not bypass native issue/protection checks.

#### SP03 subunit 4 — concrete turn3/Actor3 source bridge and pure common-gate reader

**Deliverable:** complete strict subtype/cause/compiler/read conformance, including DEV seven transitions and all old consumers, without native establishment. Read-positive slot observation requires coherent already-established source causes; missing progress/cause holds. SP04 native join3 remains the sole actual issuer.

**Files:** W17/W18/W19, `combat-procedure-transition-{request,result}.schema.json`, `world-record.schema.json`, `world-actor-state.schema.json`, `GAME/SCHEMA/actor.schema.yaml`, `spell-native-profile-values.schema.json`; `validate_domain_rules_coverage.py` and `test_s6d_09_domain_rules_coverage_contract.py`; `runtime_execution.py` linked subtype, `mechanics.py`, `recovery_roots.py`, `recovery.py`, `actor_continuity.py` strict Actor reader, `runtime_host.py`/`activity_contracts.py`/`mechanical_sources.py`/`mechanical_context.py`/`spell_cast.py` read union/gate validation; `activity_runtime.py` compiler infrastructure retention/generation and `catalog_runtime.py` strict installed compiler-source loader; immutable existing cast descriptor/compiler/inventory sources and projections described below. `temporal.py` only boundary projection validation, no reset/enrollment authority. Add S4 tests; extend generic Procedure, RD03/05/07 and closed-contract/compiler tests.

**Interfaces in runtime_execution.py:** `validate_procedure_state(state: Mapping[str, object]) -> None` dispatches exact concrete kind3 or closed generic2 after envelope validation; `turn_occurrence_key(*, campaign_id: str, procedure_id: str, execution_owner_kind: str, execution_owner_id: str, segment_sequence: int, local_boundary_key: str) -> str` implements B§2 framing; `validate_common_turn_gate(*, campaign_id: str, actor: Mapping[str, object], procedure: Mapping[str, object], common_definition: Mapping[str, object]) -> Mapping[str, object]` validates B§§1–4 and returns only an observation (`turn_occurrence_key`, actual subject, consumed), otherwise existing scoped hold. No INITIALIZE/RESET/CONSUME in this reader. Native builder uses the same pure validators, not the reader as mutation authority.

- [ ] RED concrete ACTIVE/turn_active requires complete current_turn_basis; concrete2, generic flattened concrete, kindless3/unknown kind, bool/invalid index/permutation/resource keys/capacity<spent/round-pending active fail. Generic spent/casting/progress schema2 still validates its own grammar and never yields actual-turn permission.
- [ ] RED linked OFFER tests: current R awaiting exact Continuation/G/offer/responder/candidates + exact ACTIVE linked concrete3 or generic2 works; between_turns can link but cannot grant slot permission. ACTIVE combat without pending R offer is not RULE_OWNED_ORDERED/controller evidence; stale/foreign ordering owner holds without independent downgrade.
- [ ] GREEN add exact B§2 basis to concrete3 iff active turn. Frame entire UTF-8 tuple with lengths and hex; derive transient BoundaryOccurrence from validated basis, not current message/round/index. DEV seven-transition conformance takes test-infrastructure execution coordinate separately from request payload, produces concrete3/request-result-event initial1 and qualified digest1; retain exactly one Procedure mutation. Production coordinate must come from native builder, not this DEV harness. Do not call advance_combat_turn from lifecycle.
- [ ] GREEN Actor3 companion restricted to common key, B§3 closed admission/establishment/consumption; require companion iff common progress populated, consumed iff consumption evidence; admission can exist before progress. Include full TurnEvidence, revision and predecessor-pair law, CastEvidence and SlotEvidence with actual remaining/spent arithmetic. Preserve other spell_progress profiles. actor_continuity accepts the new complete envelope but its NPC phase cannot author slot/gate causes or reset via copied state. Missing old/imported creation lifetime remains held; schema bump certifies no history.
- [ ] GREEN immutable existing `execution.spell_cast.srd521` contract binds one exact common definition generation1, all slot source/mode consumers equal it. Reject alias/divergent descriptor, payer/body-as-caster inference and unproved split/provider transfer. Declare infrastructure accepted_input_origin1/actual_combat_turn1 in existing inventory/compiler contract, outside fact DAG; compiler rejects caller fact/role substitution. Keep no-slot/ritual path free of missing-slot-gate dependency, while actual completion slot branch obtains then-current closure.
- [ ] GREEN pure reader validates current Procedure and Actor cause/subject/binding/cost closure; no absent→false default, normalization forecast or initialization write. Host derives actual Procedure identity from accepted R/Continuation.procedure_id (direct start derives the exact Procedure from its admitted transition request), never ambient/caller-selected combat state. Union equality across Host/independent validator/membership includes full input+turn+cost+declared source members, invalidates on relevant movement/control/turn, preserves accepted fixed choice/RNG at safe recompute. No source fallback when selected LIVE missing.
- [ ] Run S4 and strict Actor/Procedure/compiler/membership modules; regenerate/check projections with exact commands below. Accept only source/read bridge proof. No production receipt/actual start/gate atomicity claim.

Concrete framing algorithm and injectivity/Unicode regression basis:

```python
def frame_turn(parts: tuple[str, ...]) -> str:
    frame = bytearray(b'HDM-TURN-OCCURRENCE:1:')
    for part in parts:
        raw = part.encode('utf-8')
        frame.extend(str(len(raw)).encode('ascii'))
        frame.extend(b':')
        frame.extend(raw)
    return 'turn.' + frame.hex()

# Validate nonempty native strings, admitted owner kind, sequence int>=1 (not bool),
# and local_boundary_key=='turn_start' before calling this encoding helper.
left = ('campaign-1', 'procedure-1', 'runtime.command', 'cmd:a', '1', 'turn_start')
right = ('campaign-1', 'procedure-1', 'runtime.command', 'cmd', '11', 'turn_start')
self.assertNotEqual(frame_turn(left), frame_turn(right))
self.assertNotEqual(frame_turn(left), frame_turn(
    ('campaign-1', 'procedure-2', 'runtime.command', 'cmd:a', '1', 'turn_start')))
self.assertEqual(turn_occurrence_key(campaign_id=left[0], procedure_id=left[1],
    execution_owner_kind=left[2], execution_owner_id=left[3], segment_sequence=1,
    local_boundary_key=left[5]), frame_turn(left))
```

Also enumerate empty/colon/multibyte/non-ASCII/invalid-surrogate encodings, owner-kind/sequence/campaign/Procedure variation; the key is complete hex frame, not SHA or lexical ordering. For qualified Procedure state digest use `b'HDM_PROCEDURE_STATE/1\n' + canonical_json(complete_state3)`; assert changes in schema/basis/participant/budget affect digest and NaN/surrogate/bool invalid input rejects. No unqualified digest alias.

#### Exact 19-wire synchronization map

All W paths below are under `DEV/SCHEMAS/`. Every row gets positive valid-native and independent malformed/foreign/missing-field behavior coverage. Targets are initial/future contracts, not claims that they are installed now. “S” identifies the SP03 subunit; “J” identifies the SP04 join below; these are local prose labels, not runtime IDs.

| Wire / physical schema | Source checkpoint and consumers | Version/negative disposition |
|---|---|---|
| W01 runtime-interaction-state.schema.json | S1/S3 -> J1/J2; roots/durability/recovery/collaboration/Host | initial1; own-I distinct M; exact intent/response/mixed phases/authority union |
| W02 runtime-message-state.schema.json | S1/S3 -> J1/J2; information/emission/root protection | initial1; inbound no recipient/delivery; exact/compacted; extra unplanned text irreducible |
| W03 runtime-intent-plan-state.schema.json | S1/S3 -> J1/J2; binder/recovery/collaboration | initial1; complete same-I nonempty units, one native materialization |
| W04 intent-clause.schema.json | S1/S3 -> J2; binder/strict collaboration/current and historical use | initial1; response ref/noK/guard; canonical real extras, full previous fields retained |
| W05 runtime-command-state.schema.json | S2 -> J1; acceptance/mechanics/durability/publication/recovery | 3->4, hash2->3; exact action/direct + protected intent/mixed origin; no response K |
| W06 transition-request.schema.json | S2 -> J1/J3; exact admitted payload schema/binding | structural shape verify-only; payload whole in hash, generic object alone insufficient |
| W07 runtime-resolution-state.schema.json | S2/S3 -> J2; actual root/children/embedded segments/recovery | initial1; response owner and real extra action R distinct, direct never fake R |
| W08 runtime-continuation-state.schema.json | S3 -> J2; offer G/native single-consume/recovery | unchanged wire unless strict initial field qualification needed; offer not accepted marker |
| W09 execution-segment.schema.json | S2/S3 -> J2/J3; native marker/hash/receipt/protection | initial1; optional exact accepted_resume_input only genuine solicited consume |
| W10 resolution-receipt.schema.json | S2/S3 -> J1/J2/J3; joins/recovery/export/children | retain wire; owner K vs R exact; no response receipt implies extra-plan completion |
| W11 choice-request.schema.json | S3 -> J2; native target/candidate/G | verify-only; no free-text/extra-as-option/decline invention |
| W12 reaction-offer.schema.json | S3 -> J2; child remains under offered root | verify-only; no synthetic normal reaction command |
| W13 operational-root-routing.schema.json | S1 -> J1/J2/J3; source-native routing/hydration | 1 unchanged/four kinds; phase-specific own-I/P closure |
| W14 operational-root-handoff.schema.json | S1/S3 -> J1/J2; promise/source refs/protection | 2 unchanged; shape is routing, never accepting authority |
| W15 recovery-result.schema.json | S1/S2/S3/S4 -> all joins; READY/RETRY/BLOCKED | 1 unchanged; lawful absent P vs missing required origin/content distinction |
| W16 world-player-state.schema.json | S2/S3 -> J1/J2; full route/current and historical control | verify-only; history not lease; no creator Player projection |
| W17 combat-minimal-procedure-state.schema.json | S4 -> J3; linked ordering/mechanics/root/recovery | concrete2->3; current basis iff active turn |
| W18 runtime-procedure-state.schema.json | S4 -> J3; subtype dispatch/casting/progress | generic2 unchanged; no current_turn_basis, no kind/number substitution |
| W19 procedure-state-changed-event.schema.json | S4 -> J3; DEV event, native final event/digest/recovery | initial outer1, payload state3/digest1; actual segment causal identity |

**Additional exact schema surfaces:** Actor envelope2->3 simultaneously in `GAME/SCHEMA/actor.schema.yaml`, `world-record.schema.json` world.actor branch, strict `world-actor-state.schema.json`/`spell-native-profile-values.schema.json` companion and all envelope/source validators; do not create a global world-family revision. `combat-procedure-transition-request.schema.json` and result initial1 (including failure variant), `new_value` concrete3, event digest qualification and DEV producer/tests change together in S4. Structural schema conditions do not replace relational native checks (dynamic key equality, permutation, cause edge, controlled subjects, origin). Test strict installed `_wire_contract` projection against DEV owner bytes.

#### Versions, exact identities and coherent checkpoint rules

Read `DEV/RELEASE/VERSIONING.md` and `2026-09-05-hdm-versioning-namespace-compatibility-policy.md` at execution. Inspected current engine `1.0-alpha`, campaign_contract_generation2 in both DEV/GAME manifests, catalog2. Built-in package manifest schema2/revision1/compatibility generation1; inventory schema2; compiler projection schema1; profile contract generation1; ruleset-set/catalog-context/semantic-entry digest generations1. `GAME/SCHEMA/dnd_storage.schema.yaml` is schema4 and specifies portable storage generation3 (actual external storage marker is outside this checkout). Clean-slate pre-v1 replaces obsolete required shapes without compatibility shim/migration and cannot fabricate acceptance/lifetime causes. The family targets above are still explicit; campaign epoch is not mechanically bumped merely because this pre-release source realizes accepted targets. If implementation discovers released/adopted persisted semantics requiring coherent migration, stop for the owning System-Impact/migration ruling and synchronize campaign generation/manifests/projections atomically; do not silently retain2 or invent a migration. Storage layout/routes unchanged: no storage generation bump. Engine release identity unchanged by this plan.

Current inspected material module headers (baseline, not permanent future targets): `runtime_execution 1.0.8`, `runtime_host 1.0.18`, `bootstrap 1.0.5`, `activity_contracts 1.0.12`, `activity_runtime 1.0.9`, `catalog_runtime 1.0.2`, `mechanical_context 1.0.6`, `mechanical_sources 1.0.2`, `spell_cast 1.0.3`, `mechanics 1.0.5`, `durability 1.0.4`, `publication 1.0.6`, `recovery 1.0.5`, `recovery_roots 1.0.15`, `collaboration 1.0.20`, `access_control 1.0.6`, `history 1.0.7`, `temporal 1.0.4`. Each actual coherent material edit increments that module's fresh revision exactly once, e.g. runtime_execution's first material slice8->9, later slice increments from actual then-current value. Unchanged conditional files get no speculative bump. `current_owner`, `native_storage`, `hot_store`, `actor_continuity`, `information`, `emission` have no `framework_module_version` header in the inspected source; do not invent one by analogy. New SP04 modules start1 under current engine1.0 as already planned.

Initialize accepted-input basis/representation digest/resume marker/hash/execution projection/turn key/turn basis/common definition/profile/infrastructure generations at1 exactly as A/B specify. Command input2->3 is required because participating fields/variant/origin changed; no codec2 comparison or null action substitutions. Interpreter hash remains1. Native Continuation G, Actor state_revision and Procedure revision advance only at their real accepted edges, not schema cutover; they are not compatibility generations. Root1/handoff2/recovery-result1 remain because shape is unchanged but validators/predicates change. Common progress value shape unchanged; companion semantics require strict Actor3. No new Plan-digest namespace; native once-only materialization fence supplies identity.

`DEV/TOOLS/validate_ruleset_package_closure.py` currently assembles five existing contract families via `ENGINE_CONTRACT_SOURCE_GROUPS`; schema_contract lists R/Continuation/profile/compiler schema but not the entire new input/turn closure. Add the exact participating W01–W07/W09/W17/W19/Actor and concrete request/result schema members there as needed for escaping admitted contract identity, in the existing family; add no sixth family/auth registry. Update its compiler-projection assembly and `DEV/TOOLS/build_activity_contract_shapes.py` ROOTS/reference closure to include actual required input/concrete/Actor validation. Immutable infrastructure/common definition descriptors belong in the existing cast/profile contract projection, never a gameplay selector or content fact. Review compiler cache identity when these exact contracts affect compiled interpretation: any changed participating-field/encoding rule must bump its owning digest/ABI generation, not merely leave a stale hash. Compatible additive inventory members keep inventory schema2, catalog2 and existing digest algorithm generation1 while exact hashes change; incompatible coordinated vocabulary/compiled ABI requires its actual owner-rule transition and all consumers, not an automatic catalog2 assumption.

**Construction-level namespace classification:** carry immutable infrastructure/common-definition schema assertions as additional members of the existing schema_contract payload and existing compiler declaration/profile validation, not a new inventory family or new top-level compiler protocol. This keeps the enclosing inventory2/compiler-projection1 wire and digest1 algorithms; exact family/inventory/compiler bytes/hashes change and both DEV producer and `catalog_runtime` strict installed source loader must admit the same member set. Catalog2 stays because no coordinated catalog kind/member semantics are replaced by these infrastructure contracts; do not activate content/profile families to hide the change. Existing compiler_generation is supplied at actual admission/compile call sites (inspected fixtures use1), not an engine-global constant. The infrastructure-dependent compilation behavior changes here: move those production/conformance callers and emitted CompiledActivity/AdmittedActivityCatalog/cache metadata to compiler_generation2 in S4, reject stale generation1 compiled handles at this boundary and regenerate from admitted sources; preserve unrelated historical exact evidence. This is a compiler semantic-generation transition, not catalog-context/ruleset digest-generation arithmetic. If an actual output requires a different serialized top-level projection instead of these admitted existing member carriers, its ABI/schema bump and synchronized source loader are mandatory and must be included in the actual Version Impact review before checkpoint, not postponed behind passing tests.

Regenerate `GAME/TOOLS/activity_contract_shapes.json` and `GAME/TOOLS/activity_compiler_contracts.json` through existing producers (`write_activity_compiler_contracts_projection` derives the latter; release builder validates it), update exact inventory/package/lock/attestation projections consumed by current fixtures/build, and reject stale mixed identities. Ruleset content/manifest revision/compatibility are changed only when actual package content/compatibility changes, never to turn missing evidence into support. Recompute affected source-derived identities from admitted bytes; R1/R2/R3 draft hashes were never installed compatibility identities. Every subunit records its actual namespace old->new table or owner-justified NONE. This plan-only change is **VERSION_IMPACT: NONE**: no active machine/runtime/schema/catalog identity or version namespace owner/projection changes.

#### Item-complete 63-case implementation/proof mapping

Each row binds the complete retained requirement, including its negative/qualifier, to a concrete subunit and final native/deployed channel. TC = trusted deterministic contract, NP = real native kernel/injection, DP = actual supported deployment. All outcomes below are **required future assertions**, not PASS. A DP column never becomes green from a fixture. J1/J2/J3 are detailed under SP04 immediately below.

| Case | RED/GREEN assertion retained | Preparation / final proof |
|---|---|---|
| A01 | valid MP original origin + current exact route/control/source | S2 TC; J1 NP; DP unavailable |
| A02 | foreign campaign rejected before RNG/cost | S2 TC; J1 NP |
| A03 | foreign historical session substitution rejected; later executor session no blanket denial | S2 TC; J1 cold NP |
| A04 | foreign M/reciprocal link/digest rejected; hash alone not auth | S1/S2 TC; J1 NP |
| A05 | wrong invocation/replacement random retry key rejected | S2 TC; DP unavailable |
| A06 | wrong P, zero/duplicate C, empty/wrong K separately reject; precommand held noK lawful | S1/S2 TC; J1 NP |
| A07 | inactive Player denies new agency, preserves old result | S2 TC; J1 NP |
| A08 | duplicate/rebound/stale Player/envelope mismatch or route omission denies | S2 TC; J1 NP |
| A09 | removed/transferred PC denies old controller new work, keeps accepted cause | S2 TC; J1/J2 NP |
| A10 | strings/DTO/verified flag/Actor/publisher/gameplay verdict insufficient | S2 TC; DP unavailable |
| A11 | exact retry lookup before ambient rebind; same suspension, no RNG/cost | S2 TC; J1 NP; DP unavailable |
| A12 | equal later prose is new I/M/current authority | S2 TC; DP unavailable |
| A13 | edit/branch/regeneration no retcon/replay/host-cursor authority | S2 TC; J1 NP; DP unavailable |
| A14 | choice/reaction exact candidate/G/current responder, root author may differ, no P/K | S3 TC; J2 NP; DP unavailable |
| A15 | creator noPlayer; real history/login and own-I promise | S1/S2 TC; J1 NP; DP unavailable |
| A16 | rename/unresolved creator login uncertain/read-only, no Admin/stable-ID shortcut | S2 TC; DP unavailable |
| A17 | cold native origin/interpretation, fresh capability, no replay | S1/S2 TC; J1 NP; DP unavailable |
| A18 | actual promised precommand/response/mixed root, irreducible meaning, no arrival SAVE | S1/S3 TC; J2 NP |
| A19 | compaction only sufficient exact/semantic natural owner; hash no reconstruction | S1/S3 TC; J2 NP |
| A20 | acceptance vs retire/compact race; protection before escape, negative proof retains | S3 TC; J2 NP injection |
| A21 | distinct I/M MP and creator cold/handoff/root not stranded | S1 TC; J1/J2 NP |
| A22 | waiting controller change lawful obsolete/successor, no fabricated consent | S2/S3 TC; J2 NP |
| A23 | mandatory descendants native mapping/current required authority; publisher no new agency | S2 TC; J1/J2 NP; DP unavailable |
| A24 | connected issuer evidence unavailable; no DTO/platform-impossibility substitution | S2 explicit capability gate; DP unavailable |
| B01 | full ACTIVE concrete3/current cause+progress positive | S4 TC; J3 NP |
| B02 | generic cannot substitute concrete or relocate gate | S4 TC |
| B03 | malformed permutation/budget/index/phase/pending separately reject; no between/terminal turn | S4 TC; J3 NP |
| B04 | wrong budget active participant denies; caster need not be active | S4 TC; J3 NP |
| B05 | reaction on another creature actual turn with separate caster/control/budget | S4/S3 TC; J2/J3 NP |
| B06 | second slot through another source denied by same definition | S4 TC; J3 NP race |
| B07 | slotless needs no slot dependency/consume; other costs retained | S4 TC; J3 NP |
| B08 | ritual no slot/ordinary slot import; actual time/component cost | S4 TC; J3 NP |
| B09 | countered without slot retains actual cost, no consume/refund fiction | S4 TC; J3 NP |
| B10 | long interrupted before slot no consume, prior accepted costs retained | S4 TC; J3 NP; SP07 final lifecycle |
| B11 | long preparation/repeated action not slot; completion then-current turn | S4 TC; J3 NP; SP07 final lifecycle |
| B12 | missing definition/progress/occurrence holds, not false | S4 TC |
| B13 | forged producer/string/DEV receipt not start issue | S4 TC; J3 NP |
| B14 | wrong subject/provider/execution/resource cause rejected | S4 TC; J3 NP |
| B15 | start/reset/spend retry same key/once, no new unused value | S4 TC; J3 NP |
| B16 | equal round/index different Procedure not time proof; genuine new start distinct | S4 TC; J3 NP |
| B17 | first-use only protected creation; unknown/erased lifetime/re-enrollment held | S4 TC; J3 NP |
| B18 | crash reset before none/after same coupled cause, no recovery reset | J3 NP injection |
| B19 | crash slot spend all-none/no acknowledged half or reroll | J3 NP injection |
| B20 | terminal/provider movement no free turn/reset; unproved continuity held | S4 TC; J3 NP |
| B21 | compact cold cause sufficient/bounded, no hash/order-only summary | S4 TC; J3 NP |
| B22 | LIVE/source split/compaction race; CAS then adoption, no distributed transaction | J3 NP injection |
| B23 | split principal/body/source/payer exact mapping or hold; no second gate | S4 TC; J3 NP |
| B24 | unrelated revisions/save/restart/absorption preserve actual turn/RNG/gate | S4 TC; J3 NP |
| AR01 | direct original typed schema4/hash3 owns K segments/events/receipt, no fakeR | S2 TC; J1 NP; DP unavailable |
| AR02 | direct payload/profile/schema/origin swaps fail; action fields forbidden | S2 TC; J1 NP |
| AR03 | cold direct exact result/receipt; no-segment pending; missing true basis blocks | S2 TC; J1 NP |
| AR04 | pure response no ordinary P/K; exact candidate/promise/hydration | S1/S3 TC; J2 NP; DP unavailable |
| AR05 | old accepted response retry after G advances/Continuation retires no consume/RNG | S3 TC; J2 NP; DP unavailable |
| AR06 | substituted I/M/account/selection conflicts; new I on consumed G stale | S3 TC; J2 NP |
| AR07 | control before consume revalidates; accepted history survives with current disclosure | S2/S3 TC; J2 NP |
| AR08 | marker/I locator/consume/result/child/protection complete before/after crash/LIVE | J2 NP injection, mixed phase included |
| BR01 | concrete3/generic2 exact kind/schema dispatch, concrete2/unknown/schema-swap fail | S4 TC; J3 NP |
| BR02 | linked exact ACTIVE offer concrete3/generic2 valid; bad link/lifecycle deny | S4 TC; J2/J3 NP |
| BR03 | combat alone no ordering/controller; stale ref no independent downgrade | S4 TC |
| MR01 | same message choose A then move; response first, same I/M/P/extra K/origin/ref | S3 TC; J2 NP; DP unavailable |
| MR02 | response+nonexec real extra class/reference-only use no fakeK/response consent | S3 TC; J2 NP |
| MR03 | promised consumed-before-P cold ready exact M/root; no hash/transcript guess | S1/S3 TC; J2 NP injection |
| MR04 | retry materialized same P/K/use; fixed response hash; swapped links/kind fail | S2/S3 TC; J2 NP; DP unavailable |

**Self-review closure required before plan GO:** exact set A01–A24/B01–B24/AR01–AR08/BR01–BR03/MR01–MR04 =63, each mapped above; exact W01–W19 =19, each producer/parser/consumer/projection disposition above. AT6-01 direct variant/codec/owner maps S2/J1; AT6-02 pure response/native survivor maps S1/S3/J2; AT6-03 concrete3/generic2 linked ordering maps S4/J3; AT6-04 same-I mixed phases/meaning/protection maps S1/S3/J2 with codec consumer S2. These bindings follow the actual retained resolution-review rows, not inferred labels. No case is discharged by the presence of its name. Reconcile actual future test methods/results against each row and preserve NP/DP qualifier. A mechanically missing consumer inside this envelope is repaired; new authority/unspecified compatibility or native atomic domain requires System-Impact review.

#### Exact future verification commands and checkpoint receipt

Commands run from the actual isolated implementation checkout; use its declared environment (prepare through `DEV/TOOLS/run_maintenance_audit.py` if absent). All below are future acceptance commands with **no result asserted**. New tests use unittest.TestCase and stdlib table/subTest loops so canonical unittest and pytest both execute them; no pytest-only function tests hidden from unittest. S1–S4 are classes in the two new modules: `InputRootClosureTests`, `AuthenticatedCommandCodecTests`, `ResponseMixedClosureTests`, `CommonTurnGateTests`.

```sh
# S1 / root-first, no DAG input
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_sp03_authenticated_input.InputRootClosureTests -v
# S2
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_sp03_authenticated_input.AuthenticatedCommandCodecTests -v
# S3
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_sp03_authenticated_input.ResponseMixedClosureTests -v
# S4
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_sp03_common_turn_gate.CommonTurnGateTests -v
# Each affected module in full after focused RED/GREEN; then cross-owner integration
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_sp03_authenticated_input.py DEV/TESTS/test_sp03_common_turn_gate.py DEV/TESTS/test_rd05_operational_roots.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd12_collaboration.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_local_spell_context_cast.py
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_runtime_procedure_class_contract.py DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_rd10_role_emission.py DEV/TESTS/test_rd14_bootstrap.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_local_spell_closed_contracts.py DEV/TESTS/test_local_spell_catalog.py DEV/TESTS/test_versioning_namespace_policy.py
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_s6d_04_mechanical_context_contract.py DEV/TESTS/test_s6d_05_portable_value_contract.py DEV/TESTS/test_s6d_06_activity_primitive_contract.py DEV/TESTS/test_s6d_11_ruleset_package_closure.py
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd02_information_native_contracts.py
# Regenerate assertion projection, then verify exact owner agreement
.hdm-devtools/venv/bin/python DEV/TOOLS/build_activity_contract_shapes.py
.hdm-devtools/venv/bin/python DEV/TOOLS/build_activity_contract_shapes.py --check
# Regenerate the compiler projection from the current single package's exact lock/owners
.hdm-devtools/venv/bin/python -c 'from pathlib import Path; import yaml; from GAME.TOOLS.ruleset_package import build_resolved_lock; from DEV.TOOLS.validate_ruleset_package_closure import write_activity_compiler_contracts_projection; r=Path.cwd(); v=yaml.safe_load((r/"GAME/ENGINE_VERSION.yaml").read_text())["engine_version"]; p="hdm.rules.dnd2024-srd52-core"; lock,_=build_resolved_lock([r/"GAME/RULES/packages"/p],root_package_ids=[p],engine_version=v,catalog_generation=2); write_activity_compiler_contracts_projection(r,engine_version=v,ruleset_set_sha256=lock["ruleset_set_sha256"])'
# Every coherent publication boundary / final coherent candidate
DEV/TOOLS/run_maintenance_audit.py
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest discover -s DEV/TESTS -v
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest DEV/TESTS -n auto
DEV/TOOLS/run_release_build.py --output /tmp/hdm-dev/spell-recovery/auth-turn-native-build-20261014
git diff --check
```

Verify compiler/package identity against owner derivation, not hand-edited hashes. Regenerate before the coherent candidate's focused/module/final checks, then run `build_activity_contract_shapes.py --check`; stale output never becomes a verification exception. Use task-owned external output with parent/location verified; no generated build carriers in scanned checkout. Broad parallel failure is reproduced sequentially in affected module before product classification. Add SP04's exact native command below only after its new module exists. Hosted CI result is recorded only if actually inspected for the published candidate, never inferred from local passes.

At each later checkpoint: record expected RED/actual failure, GREEN/module/integration command exits, exact candidate byte identity, spec/code review and resolved findings, actual Impact Envelope delta, version transitions/projection equality, source/currentness evidence, capability holds and produced scope. Coordinator alone owns shared-file integration/index/cursor/publication. Finish with independent qualified Senior plan review now; implementation after GO ends with separate Senior final integration audit, not author self-approval.

## W05.SP04 — Native segment/RNG kernel and connected durability publication repair

**HARD_PRECEDES:** `W05_SPELL_CONTEXT_CAST_CONSUMERS_READY`, accepted execution/durability/publication/recovery and P0 checkpoints. **Output:** `W05_SPELL_NATIVE_SEGMENT_KERNEL_READY`: native atomic machinery, fixed RNG and connected PT-D1/PT-D2 proven with real source-admitted common conformance consumers. It is not health/lifecycle/all339 support. **SHARED_FILE_CHECKPOINT:** serialize hot_store/current_owner/runtime_host/recovery edits against P2/P3 and later integrator. No semantic dependency on P1A/P1B. **JOIN_BEFORE_INTEGRATION:** this kernel + SP08-SP15 preparations + actual recipe consumers -> one final dispatcher/host checkpoint.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/native_execution.py`, `segment_rng.py`, `DEV/TESTS/spell_native_test_support.py`, `DEV/TESTS/test_local_spell_native_segment.py`, SP04 private fixtures. `EXISTING_MODIFY` `GAME/TOOLS/hot_store.py`, `current_owner.py`, `mechanics.py`, `durability.py`, `runtime_host.py`, `recovery.py`; `live_state.py`/`publication.py` for exact adapter validation and the named auth/turn joins below. `runtime_execution.py` supplies strict execution evidence/real nested carrier retention and the accepted input/response/turn validation joins; general command settlement belongs SP06. Native_storage, allocator, operational roots, exact LIVE close/absorb, current package and ActionRequest/Resolution/Continuation/receipt schemas remain inspect-only except the exact accepted input/response/turn establishment/root/protection deltas admitted below. RuntimeHost adds typed join forwarding plus those fixed bound input/response native joins; `ExecutionService` remains final-integrator-owned.

**Interfaces:** the shared builder API above; `SegmentRngProvider.draw(request: Mapping[str,object]) -> Mapping[str,object]`, `before_frontier: str`, `proposed_frontier() -> str`. The native adapter implements the existing RngProvider contract, stages the accepted frontier locally, reuses prior fixed request/generation results and accepts its next frontier only with the coupled segment. Add an internal HOT native-mechanical establishment capability accepting only a final `NativeSegmentPlan`, exact observation and host token, atomically consuming/establishing all declared native/runtime/event/RNG/allocator/mandatory-work/idempotency/generation/dirty facts. No raw staging row becomes admitted. LIVE CAS is establishment for LIVE-owned changes; confirmed acceptance is required before HOT adoption.

PT-D1: retain the complete actual `BoundCatalogContext.to_dict()` and validate `catalog_context.basis.catalog_generation`, exact lock/inventory and typed context/set/fingerprint/candidate/execution identity. Reject flattened/mixed aliases; remove the unsupported hardcoded cast-generation reinterpretation. Existing `join_execution_durability` signature stays. PT-D2: add `execution_durability_join: ExecutionDurabilityJoin | None = None` to `CampaignPublicationService.publish_owner_delta`, forward unchanged to the existing freeze owner and bind same campaign/route/command/input/Resolution/segment/event/native generations/full write/companion closure before transport dispatch. Non-command publication still needs no join.

### SP04 named auth/turn writer joins — same kernel task, no reverse prerequisite

These three joins consume the four SP03 preparation subunits and existing SP04 native kernel/PT-D1/PT-D2 construction. They extend the SP04 Impact Envelope with the exact SP03 envelope/wire/version table above; the old “inspect-only schemas/roots” allocation is superseded only for the named accepted-input/response/turn establishment and protection joins. Production authorizes through independent plan GO plus the task's actual inputs. No new output/task ID is introduced. SP04 kernel machinery can be constructed before its own joined producer proof; do not require its output as its own input or require SP03 to consume it.

**Shared writer files:** `native_execution.py`, `segment_rng.py`, `activity_contracts.py`, `runtime_execution.py`, `runtime_host.py`, `hot_store.py`, `current_owner.py` only existing source fencing, `live_state.py`, `durability.py`, `publication.py`, `recovery.py`, `recovery_roots.py`, `collaboration.py`, strict source/schema/projection members already allocated above. Minimum per-join producer/consumer deltas are integrated once by this writer; SP03 must not stage a competing physical copy. Preserve later SP06 command/mandatory-child settlement, SP07 full long/ritual lifecycle, SP28 dispatcher and P2/P3 ownership. Tests in the existing planned `DEV/TESTS/test_local_spell_native_segment.py` and sole `spell_native_test_support.py`; no second harness/native executor. Production primitives stay with their existing owners.

**Native API qualification:** use shared `begin_segment_plan`/`merge`/`seal`/`establish_segment`. Admit the direct branch with compiled/resolution absent; actual inventory profile controls finite request schema/normalization/read/control/cost/semantics. General plan builder knows command-versus-resolution execution owner, exact segment sequence/local boundary coordinate, immutable command codec3/input observation and native closure. For input-only acceptance/Plan materialization, add fixed internal owner-native functions in `native_execution.py`, invoked only by the bound Host input path:

```text
accept_external_input(host: RuntimeHost, *, accepted_exchange: object) -> Mapping[str, object]
materialize_mixed_plan(host: RuntimeHost, *, interaction_id: str,
    interpreted_plan: Mapping[str, object]) -> Mapping[str, object]
```

`accepted_exchange` means the actual installed adapter's trusted contract result or TC conformance equivalent, not an invented platform DTO. Source/runtime cannot provide it to a public gameplay API. Unknown/unissued/foreign/moved exchange fails before this edge. The input function performs adapter lookup, native identity/content validation and authority closure, derives/allocates I/M under existing native allocation, then co-establishes complete input/root/protection state. It is not a general after-image writer or universal evidence issuer. `interpreted_plan` is a complete typed proposal from the existing interpretation phase over retained text/native response; native validation/fence issues one P, never trusts an LLM acceptance flag. Result mappings return only existing accepted native identity/phase/outcome refs; no new persisted status/receipt/queue. Explicit capability absence is a hold; no dummy successful implementation of either entry point.

#### SP04 join 1 — authentic native input/command and action/direct durability closure

**Files:** native_execution/hot_store/runtime_host/runtime_execution/segment_rng plus mechanics/durability/publication/recovery/root consumers and J1 tests; schemas/projections from S1/S2 only if real native realization changes exact admitted participating contract. No new auth persistence.

- [ ] RED trusted fixture exchange -> native I/M issuance -> ordinary interpretation P/C -> real action K/R OR direct K -> segment -> actual owner read -> durability join -> publication -> cold recovery. Run both MP and creator with I≠M. Missing issuer/current authority denies before any command, cost, RNG or admitted row. Source helpers alone do not count as this witness.
- [ ] GREEN lookup exact prior exchange mapping before ambient rebind; validate native I/M/origin/result under present read eligibility. New input binds actual principal/text/invocation and rejects reused key with changed basis. Allocation/protected input meaning co-establish before protected command/cost/RNG. At command acceptance atomically join C.command_id=K with K/I/P/C reciprocity and actual action R when applicable, root/dirty/protection and stable ID allocation. Held nonexecutable clause has no K. Retry returns exact stored K/result without new allocation/roll/spend.
- [ ] GREEN kernel dispatches action R versus direct K segments/receipt/events and carries projection1 through unchanged join call signature. Direct accepted no-segment remains pending; after segment requires exact increasing K:segment:N IDs and real result/mandatory closure before settled. Eventless lawful native edge exports empty event_ids and no dummy event. Action result carries real R; direct forbids resolution_id. Complete nested catalog and actual policy variant forward to freeze; joined owner generations/write/helper closure must equal actual native result before transport dispatch. PT-D2 forwarding stays owner-issued.
- [ ] RED/GREEN injection before I/M establishment, command/C allocation, every native row/allocator/RNG/root/dirty stage, after established edge before acknowledgement/publication, and cold retry. Before commit none; after commit recover exact IDs/cost/RNG/receipt/remaining closure. Cross-source/LIVE coupling either has one lawful exact-source domain or prerequisite close/freeze/forward closure before edge; otherwise hold. Do not network-wait inside SQLite or roll back an accepted edge after adoption/publication loss.
- [ ] Review and run J1/full RD05/06/07/09/Host; Version Impact actual transitions, full boundary commands and remote read-back under the coordinator. Deployed adapter remains DP unavailable until real profile evidence separately obtained; TCB native mechanics proof may pass without advertising deployed authentication.

#### SP04 join 2 — native response consume, same-I extra Plan and content/protection fences

**Files:** native_execution/runtime_execution/runtime_host/hot_store/live_state/recovery_roots/durability/recovery/collaboration plus strict S3 projections and J2 tests. Original root mandatory reaction children remain owned by their native execution/closure owners, not extra commands.

- [ ] RED pure response exact current Choice/Reaction candidate under another lawful responder than root author; awaiting mixed chooses A then extra move/nonexec coordination; native response consume cannot create normal P/K or change immutable I.kind. Unsupported free-text/decline mapping holds/clarifies under actual offer, never fabricates an option.
- [ ] GREEN one native accepting edge validates current root/R/Continuation/G/offer/responder/control/source, establishes consume+real segment/accepted_resume_input+I.accepted_resume_ref+result/children/next Continuation/fixed RNG/idempotency/consequences/protection/root closure. Mixed additionally advances awaiting_response->ready_to_plan in that same edge, retaining exact unplanned M. LIVE acceptance precedes HOT adoption; unavailable common atomic domain or lawful source freeze holds before consume.
- [ ] GREEN after native response unit/mandatory barrier permits planning, materialize one complete typed P with response clause/native ref and ≥1 real extra intent unit, I.P and ready->materialized in one native fence/allocation/dirty/root/protection edge. New K or no-K collaboration use remains later current agency. Concurrent planner observes same P or conflicts; never a second P/reinterpretation. Response failure cannot be leapfrogged. Response accepted history survives extra-work denial/revocation; old author rights cannot be extended in immutable basis.
- [ ] RED/GREEN inject consume-before-P crash with actual promised SAVE/handoff: cold root discovers I/M/marker/result with no P, resumes planning once without consume/roll/cost; materialized retry returns same P/K/use. Existing I root is kept until complete bounded P/native-use handoff. Exact response retry survives old Continuation retirement through I->R->same segment/survivor. Different I/same offer is stale, not winner's retry. Return old result only with present read/disclosure eligibility.
- [ ] RED/GREEN race compaction/retirement with response acceptance, Plan materialization and collaboration association; verify exact/native sufficient survivor and existing typed protection before dependence escapes. Remove required unplanned text/origin/marker/result and get BLOCKED, not transcript/hash reconstruction. Unknown needed refs remain; release may lag. Crash/LIVE movement cannot expose half consume/I/phase or acknowledged pending meaning only in RAM. No global protection registry/all-LIVE scan.
- [ ] Run J2 and full root/RD06/RD07/RD10/RD12 suites, reviewed namespace/projection checkpoint and boundary commands. Later SP06 closure consumers use this actual accepted response/children, not a fixture copied marker.

#### SP04 join 3 — genuine combat start/creation admission/lazy common slot edge

**Files:** native_execution/runtime_execution/segment_rng/hot_store/runtime_host/live_state, actor_continuity strict validation only, S4 source/read/cause validators, durability/recovery/protection consumers, J3 tests. Procedure-owned source/cost mutation joins its exact native owner; no separate universal turn service or ActorGate store.

- [ ] RED real direct command-driven Procedure initialize/start using bound original input/current authority and exact native execution coordinate. Initialize round1/index0 yields no turn/Actor reset; actual accepted start issues one complete basis and budget reset. Spend action/movement preserves basis; end removes; advance_round between-turn pending issues none; terminate removes active basis but preserves necessary history. No DEV synthetic Resolution/event or advance_combat_turn shortcut.
- [ ] GREEN native creation admits exact common Actor definition before any slot consumer can spend, stores lifetime admission even outside combat; old unproved Actor cannot be enrolled as if newly created. For SP04 conformance, create one minimal ordinary native Actor through the actual owner-valid creation+allocator+admission kernel edge before exercising slots; a source fixture already carrying admission is not producer proof. This is the kernel's minimum owner join, not SP10 forms/construction or P1A production materialization; those later writers consume it and are not prerequisites of SP04. Immutable definition is common to every admitted slot-to-cast source. Native start uses actual K/R owner and segment/local turn_start once, co-establishes phase/budgets/basis/event/receipt/RNG/idempotency/dirty/roots. Current Procedure read and protected compact Actor cause remain separate.
- [ ] GREEN builder dispatches exact `progress.spell_slot.admit/initialize/reset/consume` contract1 from admitted graph. Missing progress+protected creation INITIALIZE; coherent older genuine occurrence RESET with exact predecessor/sufficient old-cause survivor; actual current false CONSUME with real CostSpec slot expenditure. Capability removal/re-enrollment preserves state. Same occurrence true denies a second source; unrelated revision/saving/absorption not a new turn. No numeric/lexical greater-than rule or unproved different-provider reset.
- [ ] GREEN combine normalize+consume in one segment/Actor revision and retain both causes with actual pre-edge predecessor (or absent for INITIALIZE), not fictitious intermediate revision. Slot resource Actor/Asset remaining subtraction or Procedure spent addition and exact before/after resource revision, compiled consumer/cast edge/common subject all agree. Validate actual then-current turn including reaction on another creature's turn; subject/payer/budget remain separate. Unproved split mapping holds.
- [ ] RED/GREEN no-slot/ritual/countered-without-slot/long-before-slot branches do not consume or add missing gate dependence, but retain actual action/component/time/concentration consequences. Temporary real-source common consumers exercise actual branch/cost machinery at SP04; they are not full recipe/long-cast lifecycle acceptance (SP07/SP28 later). Actual long completion selects its then-current slot branch/turn. Secret-invalid target retains source-defined spend/no-effect, never a free probe/refund.
- [ ] RED/GREEN two concurrent slot sources on the same Actor/turn: one accepted native spend, one stale/conflict/revalidation; exact retry of winner same result. Inject before/after normalize/resource/execution/RNG/event/receipt/dirty/root/protection transaction stages; no gate-only/resource-only accepted state, reroll, duplicate consequence or recovery reset. Repeat across selected LIVE conflict/indeterminate/CAS acceptance then lost adoption, and terminal/provider movement/close/absorb. Split domains hold unless lawful prerequisite freeze/exact forward closure exists.
- [ ] GREEN cold recovery after detailed start/cast compaction uses validated bounded admission/establishment/consumption cause + required current source/contract/result refs; missing sufficient survivor blocks. No recursive receipt-history walk/hash/order-only survivor. Independently-due health/Effect/turn-start temporal enrollment remains mandatory; lazy common gate has no separate scheduled reset. Current reader remains pure throughout.
- [ ] Run J3/full S4/Procedure/Actor/RD04/05/06/07/09 suites, per-checkpoint Version Impact and exact boundary commands; independent task review plus final Senior integration audit. Only this actual evidence can change NOT_ESTABLISHED for these native producers; no full spell package/connected deployment claim follows.

**Native test classes/commands:** create `AuthenticatedNativeEdgeTests`, `ResponseMixedNativeEdgeTests`, `ActualTurnSlotNativeEdgeTests` in the sole native test module. Use class-focused unittest in RED/GREEN then the full existing SP04 command; no future nonexistent test is published as RED debt:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_local_spell_native_segment.AuthenticatedNativeEdgeTests -v
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_local_spell_native_segment.ResponseMixedNativeEdgeTests -v
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m unittest DEV.TESTS.test_local_spell_native_segment.ActualTurnSlotNativeEdgeTests -v
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_native_segment.py DEV/TESTS/test_sp03_authenticated_input.py DEV/TESTS/test_sp03_common_turn_gate.py DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd12_collaboration.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd15_catalog_runtime.py
```

**Required native property construction:** the existing harness must create actual source-admitted common consumers, accepted command or response, P0 session and real SQLite/LIVE establishment. For failure injection, capture all coupled native owners/allocator/root/RNG/dirty evidence before dispatch, inject once at each real establishment stage using test-owned infrastructure instrumentation, reopen via `harness.recover()`, then compare either the exact predecessor or exact accepted coherent successor. Retry the same exchange/command and assert unchanged IDs/fingerprint/occurrence/receipt/fixed rolls/resource amount; submit a distinct command/source at the same turn and assert no second accepted slot. Never implement the assertion by assigning desired balances to NativeHotStore, forging _issue_seal, monkeypatching semantic validation, setting consumed=True in a fixture as proof, using FixedRng as accepted roll authority or emitting a synthetic event as establishment. Fixture source envelopes exercise parsers; only traversing actual producer/fence closes NP.

**SP04 completion remains:** its existing kernel checkpoint, not a new auth/turn readiness ID. Record TC/NP case-level actual results and separate DP capability evidence. Deployed issuer proof demands real account bound to exact accepted text/invocation/key, exact retry versus later-identical/edit/branch, cold mapping and no gameplay override on the supported connected profile; this task has no such observed evidence and must retain UNAVAILABLE until obtained. Unsupported capability follows accepted restrict/refine/reopen law, not weakened auth. Original SP06/SP07/SP28/W06 joins retain their own actual input/proof gates.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§6–10; Step3/HOT/WP13/WP16
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: native/RNG/currentness/durability
EXPECTED OWNERS TO CHANGE: adapters/PT-D1D2
EXPECTED CONSUMERS TO CHANGE: native->join->publish/recovery
ALLOWED INTERFACES / CONTRACTS TO CHANGE: shared builder/RNG/HOT/typed join
GAME RUNTIME / PROJECTION SURFACES: listed modules; no dispatcher
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01/existing evidence
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: atomic IDs/frontier/native-first
VALIDATORS / TESTS / AUDITS: SP04 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: module identity only
CROSS-WAVE JOINS: W02/W03/P0; P2/P3 writer lock; SP28
PROTECTED ARCHITECTURE INVARIANTS: one mutation/RNG; no wait transaction
ARCHITECTURE-SENSITIVE SURFACES: readset/idempotency/LIVE/typed join
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: actual source->native->join->host
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: health/import/acquisition/Story
VERSION IMPACT: new revision1; fresh touched modules
SCHEMA / CATALOG / CHECKPOINT IMPACT: same families; actual evidence owner
MIGRATION IMPACT: retained exact carrier; no legacy aliases
HG-01 CONSTRAINTS AFFECTED: atomicity/fixed RNG/currentness
CURRENTNESS RE-READ SET BEFORE WRITE: Files + ports/schema/version/P2-P3
```

- [ ] RED `NativeSpellSegmentTests`: source-admitted temporary common `op.consume_resource` + `op.roll` consumer produces actual native Procedure/Actor resource changes, canonical fixed rolls/events/receipt and admitted subsequent P0 read. Fence all coupled owners and allocator/root/idempotency enrollment. Inject failure at every transaction stage: all-or-none; stale read, incomplete closure, foreign fragment/seal, caller event/owner body/roll/frontier or raw staged row reject. Test several rolls, discarded preparation leaves accepted frontier unchanged, retry/crash recovers identical raw values/IDs/cost once. No independent health algorithm is introduced.
- [ ] RED `NativeSpellLiveTests`: exact selected LIVE pre-CAS consequences stay prospective, accepted CAS adopts once, conflict accepts none, indeterminate retains dispatched basis and holds the affected edge. Confirm one earlier lawful native edge survives later failure; no distributed transaction/compensation or normal campaign override of ACTIVE LIVE truth.
- [ ] RED `ConnectedSpellPublicationTests`: actual binder's nested context and actual native producer pass the unchanged durability owner plus newly forwarded join. Missing/unissued/mismatched join rejects before create-tree/ref dispatch; non-command publication remains valid. Assert complete force=false coherent tree/parent/owner closure, tri-state currentness, disjoint rebuild without mechanical replay, postacceptance publication loss and same-receipt forward recovery. Replace/qualify only affected flattened fixture assumptions.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_native_segment.py DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd15_catalog_runtime.py`. INTEGRATION_SCENARIO + RNG/transaction FOCUSED_BEHAVIOR; no opaque FixedRng authority.

## W05.SP05 — Exact stochastic continuation builders

**HARD_PRECEDES:** `W05_SPELL_NATIVE_SEGMENT_KERNEL_READY`. **Output:** `W05_SPELL_STOCHASTIC_PREPARATION_READY`: exact three finite-state builders and fixed-RNG/chunk/resume machinery, not installed Teleport/Reincarnate/Prismatic support. **JOIN_BEFORE_INTEGRATION:** this output + `W05_SPELL_HEALTH_INTERCEPTION_PREPARATION_READY` + `W05_SPELL_EFFECT_TEMPORAL_PREPARATION_READY` + `W05_SPELL_IDENTITY_PREPARATION_READY` + `W05_SPELL_SPATIAL_PREPARATION_READY` + exact source/recipe proofs -> final real host stochastic conformance. Those lifecycle tasks do not depend on SP05.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/stochastic_profiles.py`, `DEV/TESTS/test_local_spell_stochastic.py`, SP05 private fixtures. `INSPECT_ONLY` SP01 stochastic schemas, builder/RNG/current owner/recovery, exact admitted table/body/source profiles. No shared kernel/Resolution schema rewrites.

**Interface:** `prepare_stochastic(context: NativePreparationContext, transition: StochasticTransitionInput) -> PreparedNativeFragment`; dispatch is a literal three-ID map internal to this module. Preserve execution section 8's exact required fields, phase-dependent ancestry and roll/choice/table references. Each draw uses only `op.roll`, stable ordinal/request/generation and existing fixed RollResult evidence; no loop language or arbitrary recursive callback. Chunk width is an operational work budget, not a semantic attempt limit. Coupled mishap damage is a declared edge before the next draw, with mandatory descriptors retained when the actual health builder has not settled it.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§8/mainSP21/exact modes
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: Activity/continuation/RNG
EXPECTED OWNERS TO CHANGE: pure stochastic preparation
EXPECTED CONSUMERS TO CHANGE: three profile consumers
ALLOWED INTERFACES / CONTRACTS TO CHANGE: prepare_stochastic/closed union
GAME RUNTIME / PROJECTION SURFACES: stochastic_profiles
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01; final activation
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: ordinal/fixed refs/safe re-pin
VALIDATORS / TESTS / AUDITS: SP05 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: none
CROSS-WAVE JOINS: SP04 + health/effect/identity/spatial->SP28
PROTECTED ARCHITECTURE INVARIANTS: no cap/reroll/recharge/false completion
ARCHITECTURE-SENSITIVE SURFACES: attempt/damage-before-draw/choice
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: kernel RNG; final consequences join
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: health/arrival/revival/Wish/loops
VERSION IMPACT: new revision1
SCHEMA / CATALOG / CHECKPOINT IMPACT: no fourth branch/status/family
MIGRATION IMPACT: retained exact profile generation
HG-01 CONSTRAINTS AFFECTED: bounded work without truncation
CURRENTNESS RE-READ SET BEFORE WRITE: §8/source/Files/native/version
```

- [ ] RED `SpellStochasticProfileTests`: Prismatic `[8,1,1]` -> two Red rays; `[8,8,1,2]` retains rejected secondary8 then Red/Orange; duplicate non8 values are legal. Force repeat outcomes beyond several chunk widths; technical hold leaves RUNNING/no failure_code and command.accepted, not arrival/COMPLETED. Reject unknown state fields/profile/table/foreign roll/request/choice refs and stale generation.
- [ ] RED Teleport preparation marks accepted mishap damage as a mandatory predecessor of a dependent next draw; crash after accepted edge/before next draw preserves ordinal/raw sequence. Reincarnate repeated generation-bound choice consumes once under same root/cast cost and selects only eligible local ancestry/body inputs. Revalidate unexpected relevant movement/owner change, while idempotency lookup precedes ambient rebinding. Final full damage/arrival/body assertions are owned by the explicit root join.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_stochastic.py DEV/TESTS/test_local_spell_native_segment.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_s6d_05_portable_value_contract.py`. FOCUSED_BEHAVIOR + native INTEGRATION_SCENARIO; production-realized/scenario-verified dimensions remain NOT_ESTABLISHED until final join.

## W05.SP06 — Common choice/reaction and mandatory command closure

**HARD_PRECEDES:** `W05_SPELL_NATIVE_SEGMENT_KERNEL_READY`, `W05_SPELL_CONTEXT_CAST_CONSUMERS_READY`. **Output:** `W05_SPELL_COMMAND_CLOSURE_PREPARATION_READY`: real generation-bound choice/reaction/root closure machinery; no broad reaction spell support. **JOIN_BEFORE_INTEGRATION:** common profile + lifecycle control/health/temporal + actual source recipes + final ExecutionService -> native Counterspell/caster-payer/nested-control conformance.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/command_closure.py`, `DEV/TESTS/test_local_spell_command_closure.py`, SP06 private fixtures. `EXISTING_MODIFY` `GAME/TOOLS/runtime_execution.py` for the accepted exact `advance_command_closure` interface and shape/idempotency validation only. `INSPECT_ONLY` mechanics close/resume helpers, actual procedure/continuation/choice/reaction/command schemas, protected role handoff. No runtime_host dispatch write.

**Interfaces:** `advance_command_closure(accepted_command: Mapping[str,object], accepted_execution: Mapping[str,object], *, mandatory_child_receipts: tuple[Mapping[str,object],...]) -> dict[str,object]` in runtime_execution, exactly execution section 7. `command_closure.prepare_closure(context: NativePreparationContext, transition: ClosureTransitionInput) -> PreparedNativeFragment` validates bounded branch/offer/response/child closure and receipt basis. Every response pins offer/responder/options/candidates/continuation generation/currentness and single consume. Technical holds retain accepted state; only actual external choice/reaction uses the existing statuses. Empty child tuple settles only when the native obligation set is actually empty.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§6–8/Step3/mainSP05–07/24
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: command/continuation/offer/Procedure
EXPECTED OWNERS TO CHANGE: closure/response preparation
EXPECTED CONSUMERS TO CHANGE: offers/children/settlement
ALLOWED INTERFACES / CONTRACTS TO CHANGE: listed closure APIs
GAME RUNTIME / PROJECTION SURFACES: command_closure/runtime_execution
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01/existing offers
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: root/offer consume/child refs
VALIDATORS / TESTS / AUDITS: SP06 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: none
CROSS-WAVE JOINS: SP03/SP04/lifecycle/source->SP28
PROTECTED ARCHITECTURE INVARIANTS: no wait/reroll/refund/settled pending
ARCHITECTURE-SENSITIVE SURFACES: reaction/payer/child/prior cost
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: admitted kernel->offer->recovery
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: generic reaction/LLM/lifecycle semantics
VERSION IMPACT: new revision1; fresh runtime_execution
SCHEMA / CATALOG / CHECKPOINT IMPACT: same statuses; no queue/record
MIGRATION IMPACT: retain exact response basis
HG-01 CONSTRAINTS AFFECTED: causal root/truthful receipt
CURRENTNESS RE-READ SET BEFORE WRITE: Files + offers/Step3/version
```

- [ ] RED `SpellCommandClosureTests`: valid accept/decline/expiry and duplicate exact response; reject foreign/stale offer/generation/responder/option/candidate and model-authored child/event receipt. Outstanding mandatory work keeps command.accepted; only the complete exact settled children allow command.settled. An expected child re-pins affected owners and recomputes from safe phase while fixed RNG remains; unexpected relevant revision conflict holds. Child failure preserves earlier accepted segments/costs and accurate partial receipt.
- [ ] RED current Counterspell preparation spends interrupted casting action and no interrupted slot; ordinary valid no-effect/invalid target retains its specified costs. Do not infer a universal refund. Source-specific caster-pays/target-acts and target-reaction enclosure inputs preserve explicit native participant owners; reject actor-pays defaults. Exact action execution for those lifecycle consumers remains at final join.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_command_closure.py DEV/TESTS/test_local_spell_native_segment.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd10_role_emission.py DEV/TESTS/test_s6d_05_portable_value_contract.py`. INTEGRATION_SCENARIO + malformed-offer FOCUSED_BEHAVIOR.

## W05.SP07 — Ritual/long casting and nested timing preparation

**HARD_PRECEDES:** `W05_SPELL_NATIVE_SEGMENT_KERNEL_READY`, `W05_SPELL_COMMAND_CLOSURE_PREPARATION_READY`. **Output:** `W05_SPELL_CASTING_PROCEDURE_PREPARATION_READY`: exact typed casting/chronology preparation, no installed ritual/long spell support. **JOIN_BEFORE_INTEGRATION:** this output + `W05_SPELL_EFFECT_TEMPORAL_PREPARATION_READY` + `W05_SPELL_HEALTH_INTERCEPTION_PREPARATION_READY` + source casting/child recipes -> final actual native long/ritual/concentration/nested-work proof. Lifecycle preparation remains independently eligible.

**Files/actions:** `NEW_CREATE` `GAME/TOOLS/casting_procedure.py`, `DEV/TESTS/test_local_spell_casting_procedure.py`, SP07 private fixtures. `INSPECT_ONLY` current temporal.py provider/route/Agenda helpers, Procedure/TemporalBinding/continuation state, lifecycle Effects/concentration and common cast builder. Shared temporal/index integration remains final-writer-owned; no new calendar/job/history service.

**Interface:** `prepare_casting_procedure(context: NativePreparationContext, transition: CastingProcedureTransitionInput) -> PreparedNativeFragment`. It uses existing `evaluate_temporal_binding`, native exact reached boundary/occurrence and typed source-local temporal enrollment; an Agenda candidate is not due authority. A casting subtype retains only accepted root/profile/phase/source/subject/cost-reservation/next-occurrence/completion/concentration refs necessary for start/repeated-action/interruption/completion. No full cast ledger or wall-clock field is added. Continuation carries advancement remainder under the existing `unconsumed_advancement` schema, not another chronology owner.

**Minimum Impact Envelope:**

```text
SPEC / APPROVED DESIGN: execution§§5–8/lifecycle§§6/8/Step5.3/5.9
IMPLEMENTATION START HEAD: fresh HEAD
PRIMARY OWNER ARTIFACTS: casting/Procedure/time/Effect
EXPECTED OWNERS TO CHANGE: pure timing preparation
EXPECTED CONSUMERS TO CHANGE: ritual/long/child timing
ALLOWED INTERFACES / CONTRACTS TO CHANGE: prepare_casting_procedure/SP01 subtype
GAME RUNTIME / PROJECTION SURFACES: casting_procedure
DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01; final activation
PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: slots/reservation/concentration
VALIDATORS / TESTS / AUDITS: SP07 + named suites
DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: none
CROSS-WAVE JOINS: SP04/SP06 + temporal/health->SP28
PROTECTED ARCHITECTURE INVARIANTS: fiction time/source-local spend
ARCHITECTURE-SENSITIVE SURFACES: cost/concentration/nested remainder
EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: native Procedure->timing->recovery
KNOWN OUT-OF-SCOPE OWNERS / SURFACES: calendar/successors/progression/latency
VERSION IMPACT: new revision1; no speculative bump
SCHEMA / CATALOG / CHECKPOINT IMPACT: subtype; no queue/record/checkpoint
MIGRATION IMPACT: retain source/time/profile refs
HG-01 CONSTRAINTS AFFECTED: no wall time/refund/duplicate support
CURRENTNESS RE-READ SET BEFORE WRITE: Files + source/providers/version
```

- [ ] RED `SpellCastingProcedureTests`: prepared ritual adds exactly ten minutes and expends no slot while retaining eligibility/action/components; missing preparation or wrong source fails. At least one-minute casting requires each reached turn's Magic action and concentration; interruption on loss spends no completion slot. Start/repeated-action/material/slot/effect creation remain separate declared transitions. A paid/consumed edge is not refunded by a later child/publication failure.
- [ ] RED exact native chronology/provider/occurrence and nested advance tests: wall clock/chat delay/global turn cannot complete casting; UNKNOWN due evidence holds; duplicate reached occurrence does not spend/rearm twice. Suspension retains advancement remainder and outstanding mandatory descendants; no trusted prospective delta/transaction survives. Cold resume re-pins context/Procedure and retains accepted costs/IDs/fixed RNG. Full concentration damage/save and final effect creation are checked at the explicit lifecycle/root join.

Future: `PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_local_spell_casting_procedure.py DEV/TESTS/test_local_spell_command_closure.py DEV/TESTS/test_local_spell_native_segment.py DEV/TESTS/test_rd08_temporal.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd07_recovery.py`. FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO.

## Core review and downstream joins

Mechanisms cover compile/read/native/RNG/continuation/common costs/closure/time; domain SP08–14/22–24/WR01–08 and all339 source/mode equality remain lifecycle/content/SP28–29 joins. No support inferred from mechanism overlap. Author ran no production/future tests.

Report exact consumer/pair/profile/read/fact/primitive/value edges, actual namespace transitions and partial-proof scope to final writer. Actual primitive topology: `DEV/CATALOG/activity-primitive-contracts/manifest.json`, `shared/read_contracts.json`, `shared/value_contracts.json`, `primitives/op.*.json`; no obsolete flat file. Final integrated metadata/manifest/inventory match actual consumers/proofs bidirectionally.

Required maintenance after affected checks; final clean exact suite, packaged offline/cold/save/LIVE/recovery and WP24 target metrics remain downstream. Early production breadth/performance stays NOT_ESTABLISHED.

## Lifecycle source manifest and constraints

Remote source pin: `84b9da6bbabb6abda274f4cb63408d5a8298b36e`. Final Senior Stop2 GO: `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/senior-stop2-review.md`, accepting repaired architecture `e048106b10350acae49b7f9d2bd3ed5d2f43c4b8`; the separate complete stable-plan Senior GO requirement is now satisfied at `d84c9a367d46f2f6e70bfa4baadac0914a2d19a9` as recorded in `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/implementation-plan-senior-review.md`; actual task entry/technical review/integration gates remain.

The following short references identify actual current owners under `DEV/docs/superpowers/specs/`: S=`2026-10-04-local-spell-execution-canonical-spec.md`; E=`2026-10-04-local-spell-execution-contracts.md`; L=`2026-10-04-local-spell-lifecycle-contracts.md`; W=`2026-10-04-wish-roll-redo-reconciliation-contracts.md`; C=`2026-10-04-local-spell-content-acquisition-contracts.md`. Directly inspected: AGENTS/runtime overlays/skill scope, both DESIGN_PROCESS owners, execution process/contract, stable Wave05; current Actor/Asset/Health/Entity Structures qualifications; actual current_owner/runtime_host/actor_continuity/temporal/information/history/recovery/live_state APIs and RD02/03/08 tests; VERSIONING and its detailed canonical owner. Complete current tree confirms all proposed lifecycle/Wish modules are absent.

SP01–04 foundation → owner-local preparations → SP28 final actual host/native/recovery/publication integration. SP05 stochastic/SP07 casting lifecycle proofs join later, never form preparation dependency cycles. Original P0→P2→P3 remains independent. Wish History validity consumes actual `W05_T06_NATIVE_HISTORY_DISCOVERY_READY` at final join, not before P2 can run. Story remains dormant. All339 source/mode/dependency/admission/production/performance dimensions stay distinct; no preparation checkpoint claims full support.

## Lifecycle exact ABI and test composition

SP01 solely creates strict shapes/shared DTOs in `GAME/TOOLS/activity_contracts.py`. Use L's exact fields/discriminators/conditional members for SubjectBinding/ObjectSubjectBinding/EffectSubjectBinding; TypedHealthCause/TypedEffectEndCause/AttackHitFrontierInput; ConcentrationTransitionInput/SpellProgressTransitionInput/FormTransitionInput/ActorConstructionInput/IdentityTransitionInput/ConversionTransitionInput/TypedObjectReturnCause/SpatialTransitionInput/ControlTransitionInput/InformationTransitionInput; ObjectSuspensionBasis/TruePolymorphObjectReturnAdjudicationResult; exact form/identity/conversion/control/progress/temporal/geometry/portal/place state. Wish requires RecentRollWitness/ReconciliationDependencyEdge/AcceptedWishRetentionFrontier/WitnessRetentionPlan/WishRollRedoRequest/WishRecentBasis/WishReconciliationState/WishTransitionInput/WishSourcePreparationPlan/WishSourcePreparationReceipt/WishReplacementRelation/ConsequenceValidityProjection. Strict Resolution/Continuation `reconciliation_state` is separate from the exactly three-variant `stochastic_state`.

New profile contract generations are integer1; do not reset existing family/module/catalog generations. Expand only E §5/L's exact enumerated IDs plus execution.wish_roll_redo; names/wildcards grant no admission. NativePreparationContext and PreparedNativeFragment constructors are issuer-bound. Context pins admitted instruction/profile, command/Resolution/occurrence/roles, complete observation, accepted facts/adjudication, fixed RNG, prospective closure/allocation handles. Fragment contains validated reads/typed proposed changes/exports/event basis/mandatory work. Only complete NativeSegmentPlan establishes; never a fragment, arbitrary patch/callback, open details bag, incomplete set or missing child.

SP04 exact `GAME/TOOLS/native_execution.py` API:

```python
begin_segment_plan(catalog: AdmittedActivityCatalog, compiled: CompiledActivity | None,
    accepted_command: Mapping[str, object], resolution: Mapping[str, object] | None, *,
    owner_session: CurrentOwnerReadSession, rng: SegmentRngProvider,
    procedure_state: Mapping[str, object] | None = None,
    continuation_state: Mapping[str, object] | None = None) -> NativePlanBuilder
NativePlanBuilder.preparation_context(*, consumer_id: str, occurrence_id: str,
    role_bindings: Mapping[str, NativeOwnerRef],
    accepted_facts: tuple[Mapping[str, object], ...] = (),
    fixed_roll_refs: tuple[str, ...] = ()) -> NativePreparationContext
NativePlanBuilder.merge(fragment: PreparedNativeFragment) -> None
NativePlanBuilder.seal() -> NativeSegmentPlan
```

Preparation functions below return success-only PreparedNativeFragment. NativePreparationHold(Exception) has operation_status `REVALIDATION_REQUIRED | CAPACITY_REQUIRED | AUTHORITY_UNAVAILABLE` and exact continuity_refs. Missing facts/adjudication use existing failure owners; genuine choice/reaction uses existing pending_response/status. Technical holds keep command.accepted/Resolution RUNNING, no invented failure_code.

SP04 is sole writer of `DEV/TESTS/spell_native_test_support.py`:

```python
NativeSpellHarness.open(*, source_fixture: Path, activity_id: str | None,
    mode_policy_profile_id: str | None, native_sources: Mapping[str, object],
    entropy: tuple[int, ...], selected_live_fixture: Path | None = None
) -> NativeSpellHarness
h.begin(*, accepted_command: Mapping, resolution: Mapping | None,
    procedure_state: Mapping | None = None,
    continuation_state: Mapping | None = None) -> NativePlanBuilder
h.establish(plan: NativeSegmentPlan) -> NativeSegmentEstablishment
h.read(owner_ref: NativeOwnerRef) -> CurrentOwnerRead
h.recover() -> NativeSpellHarness
```

The harness authenticates a temporary copy of the single built-in package+lock/catalog; accept_command, P0 CurrentOwner, real SQLite/native admission, SegmentRngProvider and native-first recovery are actual producers. Entropy is test-composition-only, no gameplay accepted flag/raw-draw bypass. Each task owns `DEV/TESTS/fixtures/spell-lifecycle/<task>.json` NEW_CREATE strict conformance-only/nonselectable source fixtures, never a second package or full339 support. Tests obtain builder/context, prepare, merge, seal, establish and inspect real native state/event/RNG/receipt; detached mutable dictionaries/seals cannot pass.

## Complete lifecycle minimum Impact Envelope for every task

Record every field below before RED, with task-local paths/owners/signatures/tests appended. Reuse this common envelope by reference, never omit its fields.

| Mandatory field | Common value / worker evidence |
|---|---|
| SPEC / APPROVED DESIGN | S/E/L/W/C task sections + Stop2 GO + continued independent stable-plan GO |
| IMPLEMENTATION START HEAD | Fresh remote HEAD and exact accepted predecessor checkpoint SHAs |
| PRIMARY OWNER ARTIFACTS | Task annex sections and current composed native owners |
| EXPECTED OWNERS TO CHANGE | Task NEW_CREATE module/test/fixture; SP15B serial modification of SP15A module |
| EXPECTED CONSUMERS TO CHANGE | Exact preparation APIs → SP28 dispatcher/native/recovery; named SP05/SP07 joins |
| ALLOWED INTERFACES / CONTRACTS TO CHANGE | Listed closed source-specific DTO/API only; no second mutation/RNG/execution authority |
| GAME RUNTIME / PROJECTION SURFACES | Task pure module/typed receipt basis; no storage/network/model mutation |
| DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS | SP01 exact published shapes; later one final registry/consumer writer; no task duplicate writes |
| PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS | Native readset/current revision, fixed RNG/IDs, protected source-local relation/progress/continuation roots; SP28 joins |
| VALIDATORS / TESTS / AUDITS | Task tests + command matrix; shared validator/audit final writer |
| DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS | Existing Wave05 cursor/receipt; CORE/INSTALL/package/map later shared writers |
| CROSS-WAVE JOINS | Preserve S1/S2/P0/completed waves, independent original P2/P3, exact later joins; no unrelated activation |
| PROTECTED ARCHITECTURE INVARIANTS | Sole physical HP/placement/resources/knowledge/PLAYER; immutable support; complete closure; fixed acceptance/RNG/IDs; prior immutable evidence; exact LIVE source; same-chat roles |
| ARCHITECTURE-SENSITIVE SURFACES | Task frontier/end/return/suppression/child dependencies; no unknown primitive/fact/profile/propagation activation |
| EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION | Real native kernel proof + named regressions; final actual host/durability/publication/recovery proof |
| KNOWN OUT-OF-SCOPE OWNERS / SURFACES | Root README/release assets/gameplay/bootstrap/new books/universal soul/geometry/undo/Story |
| VERSION IMPACT | Fresh GAME/ENGINE_VERSION engine prefix; new versioned modules revision1; actual logical-change bump/projections, NONE with owner-law reason |
| SCHEMA / CATALOG / CHECKPOINT IMPACT | Exact strict admitted shapes, no17+17 census expansion; preparation checkpoint only; no support from registration |
| MIGRATION IMPACT | None pre-authorized; no obsolete pre-release aliases/dual-read; actual incompatible adopted work follows admitted directed migration or System-Impact Gate |
| HG-01 CONSTRAINTS AFFECTED | No new ordinary network/model/scan/transaction dependency; bound physical read/work evidence, not measured latency |
| CURRENTNESS RE-READ SET BEFORE WRITE | Ref/progress/plan/index/cursor/GO, predecessor receipts, task owners/DTO/schema/kernel, current write/read consumers and version owners |

All tasks: RED positive + material-negative → observe intended failure → minimal GREEN → refactor/focused+cross-owner proof → actual Envelope/Version/schema/migration check → independent spec/quality review/repair → execution-contract audit/broader checks → coherent runtime-applicable authenticated publication/readback → existing Wave05 durable cursor. Receipt: focused RED/GREEN, task/local/integration/static checks, actual impact, version/schema/catalog/checkpoint/stale-reference result, published SHA/ref/bytes, output and newly eligible tasks. No future RED tests published. An unplanned authority/interface/persistence/compatibility/dependency/model/scan change invokes System-Impact Gate before editing.

## W05.SP08 — Health and prospective interception

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_health.py`, `DEV/TESTS/test_spell_health_interception.py`, fixture `sp08.json`. INSPECT_ONLY current Health/Actor/Asset/SP03 defense policy/SP04 kernel/RD03/S6D08. Scope: L §§6–8/S SP08/12/24, sole Actor HP/Asset integrity and exact causal interception frontier.

**API:** `prepare_health(context: NativePreparationContext, cause: TypedHealthCause) -> PreparedNativeFragment`; `prepare_interception(context: NativePreparationContext, cause: TypedHealthCause | TypedEffectEndCause | AttackHitFrontierInput) -> PreparedNativeFragment`. Reuse SP03 defense arithmetic; no second calculation policy. Damage/healing/maximum_change/instant_death remain distinct. AttackHitFrontierInput is transient exact Mirror Image input: compiled attack occurrence/frontier, source/target binding, fixed native attack-result/roll refs and declared sensory-exception basis; no caller hit truth or post-damage inference. Source results include exact unchanged/replace/prevent/end/child combinations only.

**Inputs:** HARD_PRECEDES SP01 closed shapes, SP02 sealed catalog, SP03 context/cast consumers, SP04 native kernel. JOIN_BEFORE_INTEGRATION SP09 support, SP10 form/SP12 conversion/SP14 entitlements + SP28 host; SP05 Teleport mishap actual-health proof consumes output.

- [ ] RED `ProspectiveHealthTests/NativeInterceptionTests`: real Actor current4/max20+Ward+damage5 produces current1 and exact Ward end atomically; failure before acceptance changes neither. `assert actor["hp"]["current"] == 1`; retry has identical receipt/roll/event IDs. Nondamage instant death prevents its exact edge separately. Accepted raw20/type resistance gives received10 before life/concentration consumers; wrong type/origin/bypass differs.
- [ ] Observe RED with command08, expected missing API/declared native behavior; repair unrelated fixture/import failures first.
- [ ] Implement APIs with typed source policy/current prospective readset. Mirror Image count3, fixed d6 [6,1,1] redirects/removes one; sense-exempt attacker draws none, zero count ends, other damage does not decrement. Aura maximum-reduction immunity applies only enrolled ally; eligible zero-HP turn-start heal is distinct. Resistance only once per target turn, no wall-time/another target gate. Contagion removal failed save preserves only that source Poisoned application. Linked Steed heal/retaliation/concentration/form/reversion emits immediate closure or atomically mandatory children; root cannot complete pending work.
- [ ] GREEN command08 + regressions; reject stale/partial readset, forged cause/result, unadmitted handler, receipt-text causality or catalog-order winner without native/event/RNG change. Outcome-sensitive handler order uses Step3 choice/order; fixed rolls survive safe recompute.
- [ ] Review/version/publish/readback common evidence. **Output:** `W05_SPELL_HEALTH_INTERCEPTION_PREPARATION_READY`, not complete composed casting.

## W05.SP09 — Effect support, concentration, progress and temporal state

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_effects.py`, `DEV/TESTS/test_spell_effect_temporal.py`, `sp09.json`. INSPECT_ONLY temporal.py/support/Health/Step5/RD08. SP28 owns temporal enumeration/claim/index validator writes. Scope: L §§6/8, S SP08/13/23.

**API:** `prepare_effect_end(context: NativePreparationContext, cause: TypedEffectEndCause) -> PreparedNativeFragment`; `prepare_concentration(context: NativePreparationContext, transition: ConcentrationTransitionInput) -> PreparedNativeFragment`; `prepare_progress(context: NativePreparationContext, transition: SpellProgressTransitionInput) -> PreparedNativeFragment`; `derive_lifecycle_dependency_keys(context: NativePreparationContext) -> tuple[str, ...]`. Reuse actual evaluate_temporal_binding/materialize_due_occurrence, three-valued due/actual provider.

**Inputs:** four SP01–04 hard outputs; SP08 actual damage/save grouping constrains without creating dependency cycle. SP07 long cast/nested stored spells/Time Stop final proof joins this, exact casting/Procedure/chronology/recipe inputs and SP28.

- [ ] RED `SupportSuccessorTests/SpellProgressTests/TemporalClaimTests`: caster support+two children replacement/loss/incapacity ends full scoped graph; child end leaves parent. Suppressed child retains ID/deadline and expires under original provider. Reject missing descendant/reparent/detach/unrelated dismissal; exact time-span dismissal needs non-Incapacitated caster/source scope, no invented action.
- [ ] Observe RED command09 for named API/transition.
- [ ] Implement independently supported Haste next-turn/Steed minute-fade/Glyph child/Wall existing physical panels/TP persistence successor keyed ending-occurrence+episode+local key before old end; no health/ID renewal. Planar Binding only accepted duration/binding extension, coherent provider dependencies and retained concentration.
- [ ] GREEN progress witnesses: Prayer target gate resets only that target Long Rest; Contagion failures2+failure → established/no testing occurrence, successes2+success → ended, never stored terminal3. Clone maturity, exact repeated-place qualifying succession, provider-day and finite observable-release have own consumer tests. Slot `{generation,phase,binding?,accepted_execution_ref?}` consumes G exactly once by finalize/rearm/claim; terminal source has no unresolved armed/claimed trigger, required descendants protected. No fictitious repeated-save counter/Imprisonment decade timeout. Unknown due/completeness/capacity holds, no false expiry/truncation.
- [ ] Command09+regressions/review/publication. Prove exact fixed concentration save count/order/RNG, pending child root, native-index rebuild after crash, no unrelated-history reads. **Output:** `W05_SPELL_EFFECT_TEMPORAL_PREPARATION_READY`.

## W05.SP10 — Forms and native Actor construction

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_forms.py`, `DEV/TESTS/test_spell_forms_construction.py`, `sp10.json`. INSPECT_ONLY Actor/Asset/Health/archetype/actions. Scope L §§4/5; content tasks own complete eligible statblock/action domains, not representative fixture subset.

**API:** `prepare_form(context: NativePreparationContext, transition: FormTransitionInput) -> PreparedNativeFragment`; `prepare_construction(context: NativePreparationContext, transition: ActorConstructionInput) -> PreparedNativeFragment`.

**Inputs:** SP01–04 hard; final form joins SP08 health/SP09 end/SP14 control; actual construction additionally source content + SP07 relay/cost + SP28.

- [ ] RED `FormGrantTests/NativeConstructionTests`: select an actual admitted Beast form with maximum G from its source-owned `health.maximum`; Polymorph current12 keeps native12/tempG, received G+2 leaves native10 and ends application. `assert actor["hp"]["current"] == 10`. Independent replacement grant7 survives old-form end. Shapechange remaining9→a different eligible form changes generation/stats without grant renewal; zero temp alone cannot import Polymorph end. TP creature retains separate zero-temp/persistence law. Fixtures never invent a Beast statblock to fit a numeric example.
- [ ] Observe RED command10.
- [ ] Implement exact retained/replaced/granted/anatomy/casting policies; form_state stores no health/build snapshot. HP temporary_source exists only positive actual pool, clears on depletion/replacement, cleanup matches exact grant. Source overlap outcome needs lawful choice, no row order. Gear merge/resize preserves placement; drop writes placement; end clears only matching transform, transferred/destroyed/spent/re-equipped remains changed. Suppression preserves identity/deadline/grant under source law.
- [ ] GREEN constructions: Unseen Servant sparse force/no implicit creature type/mind/attack, exact tasks/distance/zero disappearance; creature-only eligibility not inferred from Actor kind. Familiar actual legal Beast/type/initiative/no attack/persistent reappearance/gear/touch reaction. Steed actual type-specific stats/resources/turn switch, linked-heal descriptor/recast choice/gear drop. Summon commands/default/range/control expiry/death/support source-specific. Missing required statblock/action/classification fails before allocation, not sample fallback; retry no new IDs/cost/turn/model.
- [ ] Command10+regressions/version/review/publish, before/after-edge crash witness. **Output:** `W05_SPELL_FORM_CONSTRUCTION_PREPARATION_READY`.

## W05.SP11 — Principal/body, replicas and identity transfer

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_identity.py`, `DEV/TESTS/test_spell_identity_lifecycle.py`, `sp11.json`. INSPECT_ONLY Actor/Asset/Information/LIVE/current source/recovery. Scope L §§2/3/5, S SP10/22; SP28 shared validators/role projections/recovery.

**API:** `prepare_identity(context: NativePreparationContext, transition: IdentityTransitionInput) -> PreparedNativeFragment`; `prepare_identity_recovery(context: NativePreparationContext) -> PreparedNativeFragment`. Four exact identity profiles plus existing Reincarnate APPLY_BODY consumer, no new wildcard identity profile. Recovery validates accepted current roots/projections, never replays historical mutation.

**Inputs:** SP01–04 hard. Final proof joins SP08/09/10/14 + source-native LIVE/recovery/SP28. SP05 Reincarnate reconstruction consumes output + admitted ancestry.

- [ ] RED `PrincipalBodyTests/IdentityProfileTests`: split current13/LocationA transfers sole physical state/physical resources/gear/Procedure into body; principal retains build/continuity/knower/PLAYER with no HP/location/progress. Body later6/B + independently spent/transferred gear returns6/B/current resources, retires carrier, not entry13/A/inventory. Reject unknown propagation/stale relation/second occupancy/denied readset with no half split.
- [ ] Observe RED command11; implement exact source relation phases/principal policies/current binding generations. Physical/mental/identity applications retain IDs/historical meaning; live rebind needs causal evidence. Body/proxy has no copied build/private knowledge/mind; unattended original dead/dying/Unconscious does not veto active-carrier action unless source principal policy requires it.
- [ ] GREEN Magic Jar container/possessed/returning, failed-possession24h immunity, host fixed save/current distance/body death/container destruction resolves both principals. Astral independent original/proxy damage, actual permitted cord-cut kills both/principal, zero returns current original health, plane exit moves actual original body/gear and tears down distinct independent replicas—no mirroring.
- [ ] Clone immature/consent/free eligibility blocks transfer; mature preserves same principal/knowledge, no duplicated equipment, remains revival exclusion and retained instantaneous future obligation. Simulacrum separate intentional Actor/knowledge/current HP/resources, source half maximum/Construct/no spell-level-rest loophole/source repair/zero-recast retire. Reincarnate current native death/body/resource/Effect/gear closure uses fixed accepted ancestry, not reroll.
- [ ] Command11+regressions/review/publish; cold source-owned body/container/replicas follow actual LIVE route, missing roots hold, same IDs/RNG/rebind and no free turn. **Output:** `W05_SPELL_IDENTITY_PREPARATION_READY`.

## W05.SP12 — Directed conversion and True Polymorph object suspension

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_conversion.py`, `DEV/TESTS/test_spell_conversion_object_return.py`, `sp12.json`. INSPECT_ONLY amended Actor/Asset/Health/L §5.1, SP01 result/basis/membership and SP03 resolver-issued adjudication. Scope exact SS2-01, no generic body/form swap.

**API:** `prepare_conversion(context: NativePreparationContext, transition: ConversionTransitionInput) -> PreparedNativeFragment`; `prepare_object_return(context: NativePreparationContext, cause: TypedObjectReturnCause) -> PreparedNativeFragment`; `capture_object_suspension_basis(context: NativePreparationContext) -> ObjectSuspensionBasis`. Last returns immutable protected evidence, no independently accepted mutation/current HP authority.

**Inputs:** SP01–04 hard; final join SP08 actual AssetDamageResult/health, SP09 successors/temporal/end, SP10 current gear/form, SP11 actual independently existing bodies, SP14 knowledge + SP28. SP03 general preflight/resolver fixes the accepted ambiguity basis before target save/relevant RNG/cost/effect acceptance; SP07 joins only for a mode with ritual/long-casting timing.

- [ ] RED `ObjectPolicyTests/ObjectSuspensionTests/DirectedConversionTests`: all required result members generation1: ordinary_return_health=entry_current_normalized; destruction_result=restore_entry_health|zero_original_policy|principal_dead; overflow=none|terminal_damage_overflow_to_return, latter only restore_entry_health. Missing/stale/unauthorized/extra/illegal/after-save changed basis or caller HP/damage rejects before outcome/spend. Entry makes neutral stable principal `actor.embodiment.object_suspension`/`life_policy.spell.true_polymorph_object_principal`, sole active object Asset, finite gear membership, no phantom Actor/hidden HP/location/progress.
- [ ] Observe RED command12; implement capture of principal/activation/binding/rules/entry observation, original physical policy/entry life/progress only needed, minimal entry_health, native resource refs/availability(no amounts), gear identities/equipment/conversion and Effect disposition refs. No old location/sheet/knowledge/charges/durability/full Effect body. original_body_actor_id forbidden absent exact independently surviving admitted relation.
- [ ] Ordinary end/dispel after nonlethal object damage normalizes entry current under current original max/modifiers/physical policy at current object placement; no Animate Objects overflow. Current resources/recovery/Effect binding/expired or replaced temp grant/destroyed-transferred-spent-re-equipped gear survive. Unknown propagation blocks before entry; object binding cannot authorize Actor health accessor/creature target.
- [ ] Native terminal Asset damage prior integrity4/received7 → residual3 only from same accepted terminal AssetDamageResult; permitted overflow applies unchanged once/no second defense/roll. Reject invented3/wrong-hit3/accumulated earlier damage; nondamage destruction residual0. Zero-original/principal-dead prohibit overflow; actual independently admitted principal killing source cannot be overridden.
- [ ] Full-hour successor retains current object integrity/identity/basis/result/grant/source/membership, no detach/renewal. Suppression manifests creature via ordinary mapping without duration pause; current creature damage/resources/gear/placement becomes newest basis on lift, generation increments, same remaining object integrity resumes. End while suppressed retains current HP, clears only source membership; dead/destroyed active representation cannot resume.
- [ ] Animate Objects zero reverts and remaining damage affects sole Asset in same closure; TP object→creature current integrity/control expiry/permanence distinct. Object return reasons only ordinary_end/dispel/suppression/object_destruction/principal_death, not persistence. Object-experience scope no routine personal memory/action/senses; retain preexisting/independent knowledge/human exposure and suppressed-creature experience. Crash at entry/successor/suppression/re-entry/return reuses exact phase/current source/basis/result/RNG/IDs.
- [ ] GREEN command12+regressions/source/native receipt review/version/publish. **Output:** `W05_SPELL_CONVERSION_PREPARATION_READY`.

## W05.SP13 — Space, crossing, relocation and portals

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_spatial.py`, `DEV/TESTS/test_spell_spatial_relocation.py`, `sp13.json`. INSPECT_ONLY Zone/Location/Connection/Asset/chronology/LIVE; SP28 shared route/enrollment validators. Scope L §9/S SP09.

**API:** `prepare_spatial(context: NativePreparationContext, transition: SpatialTransitionInput) -> PreparedNativeFragment`; `derive_spatial_dependency_keys(context: NativePreparationContext) -> tuple[str, ...]`. Exact SpatialTargetFact/MovementSpatialFact/anchors/radial/directional/cube_group/wall_panels/enclosure, not query or global coordinates.

**Inputs:** SP01–04 hard; final crossing joins SP08/09 consequences, SP11 bodies/SP14 enrollment/SP28. SP05 Teleport arrival consumes output + actual source relocation.

- [ ] RED `ZoneGeometryTests/MovementCrossingTests/PortalRelocationTests`: exact units/dimensions/finite membership/support/anchor/adjacency. Fire Storm two disjoint neighbor pairs legal, orphan fails; Wall Ice/Guards Wards preserve distinct predicate. Reject duplicate/self/missing endpoints/stale moving anchor/unknown cover/Actor micro-position. Complete native scene roster before RNG, partial observation cannot prove target set/absence.
- [ ] Observe RED command13; implement source-specific native geometry/participant episodes and exact dependency keys. Outside→outside path enter/exit still fires accepted crossing. Every relevant Zone transition or proved unchanged; first/repeated entry/touch/start/end/forced/teleport behavior uses exact source episode/gate, never universal movement rule. Unknown required fact holds, not false.
- [ ] GREEN relocation validates current destination kind/revision, full party/mount/Assets/occupancy/falling/arrival, chronology follow/preserve/rebase and required LIVE route. Movement spend cannot durable-move; unknown destination fiction needs bounded adjudication. Portal closure removes traversal availability, preserves permitted destination/contents/inhabitants/IDs/parent/provider. Ordinary passage vs source Activity/reaction remains distinct; no remote write authorization from portal.
- [ ] Command13+regressions; multi-LIVE conflict keeps accepted earlier edges, no distributed transaction/compensation; large legitimate set capacity hold no truncation. Recovery exact geometry/participation/indices; unrelated scenes/history do not enlarge body reads. Review/publish. **Output:** `W05_SPELL_SPATIAL_PREPARATION_READY`.

## W05.SP14 — Knowledge, memory, control and entitlement

**Files:** NEW_CREATE `GAME/TOOLS/lifecycle_information.py`, `DEV/TESTS/test_spell_information_control.py`, `sp14.json`. INSPECT_ONLY Information/Step4/PLAYER/Actor/Procedure/reaction. Root SP28 shared normalization/eligibility/emission writes. Scope L §§10/11/S SP11/12/24.

**API:** `prepare_control(context: NativePreparationContext, transition: ControlTransitionInput) -> PreparedNativeFragment`; `prepare_information(context: NativePreparationContext, transition: InformationTransitionInput) -> PreparedNativeFragment`. Existing validate_knowledge_transition/normalize_information_evidence remain native validators; raw private target contexts are not trusted inputs.

**Inputs:** SP01–04 hard; final SP06/07 cost/reaction closure, SP09 source/observable work, SP11 principal + source safe receipts/SP28.

- [ ] RED `SpellKnowledgeTests/SpellControlEntitlementTests`: illusion recognition writes independent source-qualified proposition relation, not world truth or universal visibility/immunity. Corpse answer uses principal/death-occurrence protected eligible knower basis/ignorance/false-belief/deception permissions, rejects omniscient current truth/full-history scan. Memory change source-caused relations+compact original basis; restoration preserves independent later knowledge/history/human exposure. No mind dump/target context union/voluntary PC authoring.
- [ ] Observe RED command14; implement sensory_link/divination/corpse_answers/illusion_recognition/memory_change exact recipient/principal/source/range/plane/protection/fact/acquisition/emission. Sending block/hidden Scrying purpose-save/secret invalidity project safe accepted receipts; internal diagnostics cannot reveal hidden mechanically valid invalidity. Native disclosure advances only actual eligible emission, not preparation.
- [ ] GREEN control source command/default/range/plane/expiry keeps permanent creature and PLAYER identity, charm ≠ domination. Domination reaction performer target/payer caster; target reaction only separately required action. Enclosure movement payer enclosed target; touch relay familiar reaction/caster cast costs; Haste restricted entitlement ≠ unrestricted action.
- [ ] ReactionWindow exact trigger/offer/generation/reactors/profile/cost owner/frontier/child/expiry; Shield/Counterspell safe recompute preserves fixed rolls, Counterspell chain capacity preserves mandatory work. Origin/level/magic/exception source typed, never narration/name matching. Revoke current control/source movement/stale offer rejects or resumes exact accepted work without duplicate costs/draws/emission.
- [ ] Command14+regressions/version/review/publish. **Output:** `W05_SPELL_INFORMATION_CONTROL_PREPARATION_READY`.

## W05.SP15A — Recent evidence and counterfactual derivation

Meaningful independently reviewable SP15 unit, not setup or a parallel plan.

**Files:** NEW_CREATE `GAME/TOOLS/wish_evidence.py`, `GAME/TOOLS/wish_reconciliation.py`, `DEV/TESTS/test_wish_recent_counterfactual.py`, `sp15a.json`. Root SP28 sole accepted-producer enrollment/storage/index/retention writer. Scope WR01–05.

**API:** `derive_recent_roll_witness(context: NativePreparationContext, accepted_segment: NativeSegmentEstablishment) -> RecentRollWitness`; `select_recent_roll_basis(context: NativePreparationContext, request: WishRollRedoRequest) -> WishRecentBasis`; `plan_witness_retention(witnesses: tuple[RecentRollWitness, ...], frontier: AcceptedWishRetentionFrontier) -> WitnessRetentionPlan`; `derive_wish_replacement(context: NativePreparationContext, state: WishReconciliationState, witness: RecentRollWitness) -> PreparedNativeFragment`.

**Inputs:** SP01–04 hard; supported-mode join all affected SP08–14/Procedure/chronology/knowledge/disclosure/durability classifications. Missing treatment forbids support. P2 not prerequisite of private calculation.

- [ ] RED `WishRecentBasisTests/WishCounterfactualTests`: target inside/outside actual last-round boundary including caster prior turn; exact Procedure/BoundaryOccurrence/chronology bridge, indeterminate/missing holds. No Git/wall clock/global-round/ID/message inference. Bounded legal retention expiry compacts unreferenced witness/index, accepted pending reconciliation retains basis. Missing edge and large closure holds, no invented affected list/truncation/history load.
- [ ] Observe RED command15A; implement minimal original adopted recipe/policy/context/facts/choices/raw draws/interpretation/stable refs/pre-post revisions/before-values and consequence-dependency enrollment evidence. It is protected original execution basis, not a second current world store/permanent undo journal.
- [ ] GREEN ORIGINAL/REROLL and NORMAL/ADVANTAGE/DISADVANTAGE: original draws/result immutable, new draws Wish requests. Failed-save/Critical Hit replacement uses same adopted pure recipe; current unrelated later HP/resource/Asset mutation survives. Surviving corresponding dependent roll retains meaning/ID/draws; new branch gets new request; removed consequence retains historical evidence, IDs never recycle, no whole-world snapshot replay.
- [ ] PREFLIGHT→CAST_ACCEPTED→REROLL_FIXED→SELECTION_PENDING exact phase members; single-consume player choice after seeing roll. ORIGINAL still costs action/slot/full nonduplication Wish stress/unpreventable damage/Strength recovery/permanent loss; initiating Wish excluded from replacement. Changed later accepted choice/fact applicability produces bounded exact adjudication/choice request, never chooses for another player. Technical hold preserves phase/RUNNING; genuine choice AWAITING_CHOICE, no transaction across wait.
- [ ] Command15A+regressions; crash after cast/reroll/selection, repeated input/publication failure preserves costs/raw RNG/IDs. Before acceptance no new mutation. Unrelated history growth no broad reads. Review/version/publish. **Output:** `W05_SPELL_WISH_COUNTERFACTUAL_PREPARATION_READY`.

## W05.SP15B — Source preparation and single replacement

**Files:** NEW_CREATE `GAME/TOOLS/wish_source_preparation.py`, `DEV/TESTS/test_wish_source_reconciliation.py`, `sp15b.json`; EXISTING_MODIFY SP15A-created wish_reconciliation.py serially. INSPECT_ONLY existing LIVE close/final/absorption/publication; SP28 actual host network/storage/recovery. Scope WR03–08.

**API:** `plan_wish_source_preparation(context: NativePreparationContext, state: WishReconciliationState) -> WishSourcePreparationPlan`; `advance_wish_source_preparation(context: NativePreparationContext, state: WishReconciliationState, receipts: tuple[WishSourcePreparationReceipt, ...]) -> WishReconciliationState`; `prepare_wish_reconciliation(context: NativePreparationContext, transition: WishTransitionInput) -> PreparedNativeFragment`; `resolve_current_consequence_validity(context: NativePreparationContext, relation: WishReplacementRelation) -> ConsequenceValidityProjection`. Receipts wrap actual existing owner-issued close/final/absorption proof and exact revisions; no fake string seal.

**Inputs:** SP15A/SP04 + existing WP16 source/durability hard; final all affected lifecycle/Procedure/chronology/information/enrollment + SP28; current History validity additionally original accepted P2 output. P2/P3 do not wait for SP15.

- [ ] RED `WishSourcePreparationTests/WishAtomicReplacementTests`: first of two LIVE closes accepted, second conflicts → first close retained, fiction unreconciled, exact durable cursor. Reject stale/fabricated final/missing absorption/access/indeterminate evidence. Material source change safely revalidates without retarget/recharge/redraw/discard; technical prep time cannot alter originally admitted fictional eligibility.
- [ ] Observe RED command15B; implement pure request/cursor using existing close_live_source, freeze_campaign_absorption_delta, validate_accepted_absorption_evidence signatures and exact actual source publication/absorb route in SP28. Shape helper return alone is not accepted close. Sources finals retain chronology/IDs/RNG, every required input under one lawful campaign owner before replacement.
- [ ] GREEN stage full current owners/revisions/access/new fixed RNG/choice relation/receipt/children/idempotency/dirty closure, revalidate at one native edge. No fractional reality edit/cross-ref transaction/compensation of accepted close. ORIGINAL may yield no-fiction-change receipt but paid Wish remains. REROLL yields one current reality/forward old-current validity relation, no backward CAUSES cycle/edited old rolls/events/messages/choices/exposure.
- [ ] Crash after every accepted phase through SETTLED; post-replacement publication/projection/successor failure retains new reality and forward recovery, no old-reality restoration/redraw/duplicate replacement. Successor LIVE derives coherent accepted basis; mandatory pending work blocks root settlement. Large legitimate closure never truncates.
- [ ] Pure valid current projection tests now; SP28 later consumes actual P2 HistoryService.discover exact native sources/currentness and P3 retrospective, preserving old payloads and recipient knowledge/provenance/human exposure. Context resolves relation before current consequence presentation; Story remains routed dormant. Cold recovery accepted source/relation/basis/native reality/children before projections; missing basis integrity hold, not replay.
- [ ] Command15B+regressions/review/version/publish. **Outputs:** `W05_SPELL_WISH_SOURCE_PREPARATION_READY`; with accepted/readback SP15A, `W05_SPELL_WISH_RECONCILIATION_PREPARATION_READY`. Actual host multi-LIVE proof remains SP28, not synthetic list proof.

## Exact future test commands and acceptance receipts

Each RED runs its task module alone using the executable prefix below, expected nonzero for the stated missing API/behavior. Each GREEN runs the full listed command, expected exit0/all tests pass. The command matrix is explicit future verification, not observed execution. Source fixture paths all expand to `DEV/TESTS/fixtures/spell-lifecycle/`; tests/path responsibilities are NEW_CREATE, regression paths INSPECT_ONLY.

```sh
# command08
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_health_interception.py DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py
# command09
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_effect_temporal.py DEV/TESTS/test_rd08_temporal.py DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py
# command10
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_forms_construction.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_r2_7_wp04_actor_asset_conformance.py
# command11
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_identity_lifecycle.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py
# command12
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_conversion_object_return.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_s6d_08_health_effects_recovery_contract.py
# command13
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_spatial_relocation.py DEV/TESTS/test_rd08_temporal.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_w03_t08_live_consumers.py
# command14
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_information_control.py DEV/TESTS/test_rd02_information_native_contracts.py DEV/TESTS/test_rd09_access_live.py
# command15A
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_wish_recent_counterfactual.py DEV/TESTS/test_rd08_temporal.py DEV/TESTS/test_rd07_recovery.py
# command15B
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_wish_source_reconciliation.py DEV/TESTS/test_wish_recent_counterfactual.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd07_recovery.py
```

Use exact required broader DEV/maintenance commands from execution contract before checkpoint; unavailable execution surface is unavailable, never PASS. Version gates inspect real module versions and projections after each logical checkpoint; each publication pins fresh H→C(parent H), force=false, verifies ref/tree/changed bytes and updates existing stable cursor with completed SHA/next exact dependency-eligible task/unpublished work.

## SP28 shared physical joins and currentness

| Actual file owner | Final integration only after GREEN semantic inputs |
|---|---|
| activity_runtime.py/runtime_host.py | Exact dispatch→complete sealed native plan→resume/root closure→owner-issued ExecutionDurabilityJoin→publication, zero deterministic model passes |
| actor_continuity.py/current_owner.py/hot_store.py | Admit closed new states/source-authorized native transition distinct from ACTOR/NPC continuity; sole active body/object/resource, atomic events/RNG/work/indices/dirty/idempotency |
| temporal.py/recovery_roots.py/recovery.py | Exact generations/claims/source-local enrollment/successor roots; current native-first accepted state/basis/RNG/IDs then complete derived support/condition/zone/relation/temporal/recent-roll index rebuild |
| information.py/current Context/disclosure | Principal/physical/control source binding, protected death/original/object-time basis; one native knowledge owner, actual recipient emission/PC agency/PO-012 |
| live_state.py/bound source adapters | Exact source packing/close/freeze/final/absorb/owner receipts, no cross-source transaction or rollback accepted edges |
| history.py + actual P2 event enrollment/HOT/publication/source producers | Wait original W05_T06_NATIVE_HISTORY_DISCOVERY_READY; exact discovery/native currentness + forward Wish validity; preserve P2 companions/history payloads/P3 eligibility |
| SP01 shapes/shared catalog/CORE/INSTALL/audit/map | One final physical writer, exact profile/primitive/pair/accessor/fact/consumer/native producer closure and source/mode/dependency/proof equality |

At pin: temporal1.0.4/recovery1.0.5/live_state1.0.22/history1.0.5. These are provenance, not future frozen targets: fresh-read actual P2/other writer versions before integration; material logical change bumps once with all projections. History contract generation1, local LIVE schemas/profile generations/catalog generation are distinct namespaces. No count-derived compatibility, speculative migration or downgrade.

Still NOT_ESTABLISHED: machine/producer implementations; SP05/SP07 actual lifecycle joins; full339 source/mode/domain/dependency/admission equality; SP28 composed command/native/receipt/publication/recovery/multi-LIVE; original P2 current-validity join; actual packaged failures; WP24 physical invocation/serial depth/context/cache/compute/read-write/retry/cold-warm/save/LIVE/recovery instrumentation and latency. No prepared test/aggregate CI closes these.

## Complete traceability and review focus

| Keys | Exact primary owner / actual join |
|---|---|
| SP-01 / SP-02 | Content admission/support source keys; qualified fixtures, final equality |
| SP-03 / SP-04 | Core sealed loader/cache + actor-eligible lookup/prompt; exact frozen profile inputs |
| SP-05 | Core preflight/SP07; SP12 pre-outcome basis/SP14 payer/SP15 Wish costs |
| SP-06 / SP-07 | Core native/closure/casting; all task currentness/RNG/ID/recovery + SP28 |
| SP-08 | SP09 support/concentration/progress; SP08 health/SP10/12 cleanup |
| SP-09 | SP13 geometry/complete crossing/portal/relocation + chronology/LIVE |
| SP-10 | SP10 form/construction/SP11 bodies/replicas/SP12 conversions |
| SP-11 | SP14 knowledge/control/SP11 principal/SP12 object experience |
| SP-12 | SP08 interception/SP14 reaction entitlement + core defense/casting |
| SP-13 | SP09 stored children/successors/Time Stop chronology + source/core Procedure; Wish ordinary modes content/cost support |
| SP-14 | SP15A/B + SP28 actual source/native/History |
| SP-15 | SP01/compiler exact closed inventory, per-task negative permission tests |
| SP-16 | Full finite affected set/capacity; SP09/13/15 no truncation/partial edge |
| SP-17 | Existing failure/status owner, no unsupported rules fallback/false settled holds |
| SP-18 | Zero dedicated calls/bounded local reads; final actual target instrumentation |
| SP-19 | Task behavioral/negative/kernel proofs + SP28 actual host/package acceptance |
| SP-20 | Shared writer/version/adoption/cursor; no early support/activation |
| SP-21 | Core SP05, real SP08/09/11/13 consequences and fixed resumed cost/RNG |
| SP-22 | SP11 principal/body; SP12 exact neutral object/evidence/current return |
| SP-23 | SP09 successors/native progress; SP10/12 lasting consequence/SP13 portals |
| SP-24 | SP08 interception/SP14 payers/info/SP09 gates/temporal |
| WR-01 | SP15A last-round bridge/mode/old-new/full paid stress |
| WR-02 | SP15A finite witness/expiry/protected enrollment + SP28 accepted producers |
| WR-03 | SP01 strict reconciliation_state + SP15A/B all phase tests |
| WR-04 | SP15A one cast/reroll/choice + SP15B source revalidation/time boundary |
| WR-05 | SP15A pure recipe/delta/surviving-new RNG/IDs/choices/current unrelated state |
| WR-06 | SP15B source close/final/absorb/single replacement + SP28 actual adapters |
| WR-07 | SP14 + SP15B current-validity projection/actual P2/P3 join/dormant Story |
| WR-08 | SP15A/B listed fault witnesses + SP28 real composed/recovery/target proof |

Five required Review Focus cases: independently replaced temp/gear/resource (SP10/12); stale control/body/original unattended death (SP11/14); incomplete roster/outside-endpoint crossing/uncertain provider (SP09/13); missing/changed pre-save object ruling/wrong residual (SP12); Wish earlier close conflict/later unrelated mutation/post-replacement publication loss (SP15A/B). Each has positive/material-negative witness above. Self-check: all24 SP/all8 WR retain item-level semantics/qualifiers, exact agreed types and builder/harness signatures; final joins are explicit unmet work. No new architecture/PO decision or production claim.

## Verified bounded source and file basis

The coordinator's pinned source route is `84b9da6bbabb6abda274f4cb63408d5a8298b36e`. The content coauthor read current AGENTS/runtime overlay/Skill Scope, both design processes, development execution process, stable Wave05/execution contract, package identity/machine-closure/character owners, actual manifest/seed, package/source/domain validators, relevant strict schemas and accepted spell specifications through GitHub Connector. All339 independent body passes are already completed; this plan carries their requirements and qualifies import blockers without reopening their design review. Historical `NEEDS_PO_SP14`/candidate labels in the research matrix are superseded by the accepted owner decision and final Wish annex; raw evidence bytes remain unchanged.

Exact existing package root: `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core`. Existing manifest `ruleset-package-manifest.json` is schema2 with package_revision1, compatibility_generation1 and catalog_generation2 at that pin; these are observations, not execution targets. `character-capabilities.json` still promises Human/Criminal/Fighter1–2/Sorcerer1, `full_srd_character_corpus=false` and `ABSENT_NONSELECTABLE`. Current `character-mvp-seed.json` owns six spell/Activity bodies. `resolve_package` currently reads that seed plus gameplay spine and has first/default-option and activity_ids[0] completeness assumptions. Their exact qualified cutover is owned below; do not leave dual source ownership.

### One serialized content integrator and truthful intermediate packages

1. SP01/SP02 establish strict member/definition compilation, source-qualified support rows and a separately truthful spell profile. The profile initially promises only exact baseline entries actually validated; empty/new source records never make an offer legal.
2. A level worker owns only its one new level shard, its requirement/expectation/scenario fixtures and test module. A supporting-content worker owns its natural shards. None writes the manifest, character seed, capability promise, support registry, primitive consumer census, domain coverage, generated identities or execution cursor.
3. Before each producer checkpoint is published, the same designated shared integrator fresh-reads those shared files, adds the exact new member to `content_files`, integrates the complete active consumer/reference deltas and regenerates all affected identity/validator projections. Include the producer files and integrator changes in one coherent publication. Never publish unmanifested GAME semantics, blanket audit exemptions or half-valid package state.
4. SP17 publication coherently removes relocated `spell.fire_bolt`, `spell.poison_spray`, `spell.acid_splash` and their Activities from the seed. It moves `spell.thunderclap` and its Activity to `spell-content/existing-extras.json` only after its separate lawful lane closes; Thunderclap never appears in the level0 SRD count. SP18 removes the two relocated level1 spell/Activity bodies. Preserve class grants/choice bindings/references; rewrite exact external-dependency closure and current validators/fixtures in the same checkpoint. Source-qualified metadata changes are explicit semantic repairs, not portrayed as byte-preserving moves.
5. Partial packages declare only exact mode-complete, source-closed, admitted, native-realized entries. Other entries remain absent/nonselectable in that profile. SP28 realizes the composed native Host against a finite exact conformance catalog independently of all ten content shards; preparation can proceed earlier, but each shard's native proof and supported-publication acceptance HARD_PRECEDES on SP28.
6. SP29 is the single final writer of the full339 claim, final acquisition/default promotion and integrated runtime evidence. It joins all ten accepted shard proofs. SP30 tests that resulting package; it does not postpone first discovery of unsupported paid casts until release tests.

Different accepted logical shared-file changes may require separate module revisions; “one final writer” prohibits competing writers, not legitimate later owner-qualified increments. No live ref force update, ref deletion or alternate transport is permitted.

## Shared task ABI and evidence law

Core SP01 defines `DEV/SCHEMAS/spell-support-row.schema.json`. Each derived row has exactly `spell_id, mode_id, requirement_key, source_witness_ref, activity_id, compiled_consumer_ids, dependency_ids, contract_refs` and six separately scoped evidence dimensions `source_closure, definition_closure, machine_admission, production_realization, scenario_verification, target_performance`. A dimension has `status=NOT_ESTABLISHED|PASS|FAIL`, exact `proof_refs`, and environment reference when performance is PASS. A row is DEV evidence, not native state, gameplay authority or a digest owner.

Use accepted APIs without parallel compiler/admission implementations:
- `admit_activity_catalog(context_request: object, *, package_snapshots: Mapping[str,PackageSnapshot], engine_contract_inventory_source: object, natural_owner_sources: object, compiler_generation: int, mode_policy_profile_id: str) -> AdmittedActivityCatalog`.
- `compile_activity(catalog: AdmittedActivityCatalog, activity_id: str) -> CompiledActivity`.
- `plan_next_segment(catalog, compiled, accepted_command, resolution, *, owner_session, rng, procedure_state=None, continuation_state=None) -> NativeSegmentPlan`.
- Host-issued `ExecutionService.execute_intent_plan(intent_plan, *, catalog)` and `resume(accepted_command, continuation, response, *, catalog)`; real native establishment, command closure, durability and publication come from SP28. Tests cannot monkeypatch semantic acceptance or supply raw owner after-images as authority.

The SP16 build producer is `DEV/TOOLS/validate_spell_content.py`:
- `derive_spell_support_rows(catalog: AdmittedActivityCatalog, qualified_sources: Mapping[str,object], proof_index: Mapping[str,object]) -> tuple[Mapping[str,object],...]`.
- `validate_spell_support_equality(rows: tuple[Mapping[str,object],...], *, qualified_sources: Mapping[str,object], catalog: AdmittedActivityCatalog, proof_index: Mapping[str,object], promised_spell_ids: tuple[str,...]) -> Mapping[str,object]`.
- `derive_eligible_support_domains(qualified_sources: Mapping[str,object], definitions: Mapping[str,Mapping[str,object]]) -> Mapping[str,tuple[str,...]]`.
These are pure bounded build functions, with a CLI in that same module for explicit package/source/proof inputs. They consume compiler-issued definitions/consumer/read plans and SP00 source witnesses; they cannot accept caller “complete=true”, fabricated PASS flags or arbitrary eligible-ID sets. Equality results use the existing proof/validator channels; they do not choose a package or rule.

Required typed relations:
`promised SRD names/IDs == reconstructed source names/IDs == package SRD spell IDs`;
source requirement keys == mapped requirement keys;
source mode/branch roster == declared roster == exercised production roster;
computed transitive edges == declared/admitted edges;
required contracts == exact available compatible contracts;
required scoped proof keys == fresh actual proof keys.
These are explicit typed mappings, not string equality between source names and Activity IDs. Extras are a separately named disjoint set. Preserve exceptions, applicability/non-goals, confidence, negative evidence and revisit triggers in source/requirement rows. The 13 research families are review facets, never 13 services/executors. Finite parameter domains are source legal domains; chunk size cannot truncate them.

The sole SP04 `DEV/TESTS/spell_native_test_support.py` API is `NativeSpellHarness.open(*, source_fixture: Path, activity_id: str | None, mode_policy_profile_id: str | None, native_sources: Mapping[str,object], entropy: tuple[int,...], selected_live_fixture: Path | None = None) -> NativeSpellHarness`; `begin(*, accepted_command: Mapping[str,object], resolution: Mapping[str,object] | None, procedure_state: Mapping[str,object] | None = None, continuation_state: Mapping[str,object] | None = None) -> NativePlanBuilder`; `establish(plan: NativeSegmentPlan) -> NativeSegmentEstablishment`; `read(owner_ref: NativeOwnerRef) -> CurrentOwnerRead`; `recover() -> NativeSpellHarness`. Action requires real Activity/mode/Resolution; direct uses absent Activity/mode/Resolution and its exact inventory binding as qualified in SP03/SP04. Entropy is trusted test-composition input, never a fixture flag/caller-accepted-roll authority. Harness construction traverses actual package/lock/binder/compiler/accepted-command/P0/native SQLite/RNG/recovery. After SP28, all-mode production proof also traverses its actual bound Host ExecutionService/durability/publication join; direct plan-builder unit proof cannot replace that composed path.

Every native scenario starts from real accepted IntentPlan/Command/BoundCatalogContext carriers, traverses native owner validation, established HOT or accepted LIVE, RuntimeHost/durability/publication, and asserts exact eligible receipt/state/continuation outcomes. A content task owns golden/source/branch arithmetic plus native scenarios and retry/recovery negatives. Source expected outputs are independently authored; do not compute expected arithmetic with the implementation being tested.

## W05.SP00 — Qualified primary source, repair witness and sealed source roster

**Deliverable:** import-ready source/mode/support census for all339 entries and the separate existing-extra lane, retaining the completed full-body design evidence and resolving actual source-layout/provenance blockers.

**Files/actions:** NEW_CREATE `DEV/TOOLS/validate_spell_source_qualification.py`; `DEV/SCHEMAS/spell-source-qualification.schema.json`; `DEV/TESTS/fixtures/spell-source-qualification.json`; `DEV/TESTS/fixtures/spell-source-qualification-rejected.json`; `DEV/TESTS/test_spell_source_qualification.py`. INSPECT_ONLY the frozen `spell-inventory.json`, all three source-pass files, requirement matrix and source-obligation-resolution in the 2026-10-04 research/design directories, official licensed SRD asset and existing seed/NOTICE. The shared integrator alone performs any required NOTICE/provenance or seed metadata projection.

**Interfaces:** `validate_source_qualification(manifest: Mapping[str,object], *, expected_inventory: Mapping[str,object], source_assets: Mapping[str,bytes]) -> Mapping[str,object]` and `derive_source_requirement_roster(manifest: Mapping[str,object]) -> tuple[Mapping[str,object],...]` live in the new DEV tool. The strict source manifest contains source asset URI/license/attribution, exact asset-byte sha256, source page/span/record locator, raw extraction witness hash+basis, reconstructed owning-body qualification, independently formulated requirement/mode/support-domain keys and per-key closure evidence. It distinguishes exact source bytes, historical raw-body hash and later canonical semantic hash. Each row is bound to one exact source entry; extras also carry named provenance, edition and class-eligibility evidence. No primary full spell text is copied wholesale into public fixtures.

**Dependencies/checkpoint:** accepted specifications CONSTRAINS_WITHOUT_ORDERING; `W05_SPELL_SOURCE_QUALIFICATION_READY` HARD_PRECEDES SP16 and all source-bound shard admission. Header/body design review is not repeated. Any still-open source lane stays FAIL/nonselectable; accepted scope requires its lawful closure or explicit content-owner default repair, not a new product gate.

- [ ] RED: `test_qualified_roster_equals_339_and_exact_levels` asserts 339 unique SRD entries and counts `[27,57,57,42,34,38,31,20,17,16]`, source-name equality with inventory, no extra in339 and no duplicate source/mode/requirement key.
- [ ] RED: paired fixture `test_raw_extraction_cannot_admit_foreign_tail_or_missing_block` accepts the correctly scoped owning content and rejects the same witness with Animated Object/Otherworldly Steed omitted, Antipathy/Sympathy or Find the Path continuation attached to the wrong spell, next-heading/footer/control material interpreted as rules, or licensed Telekinesis fine-control continuation unproved.
- [ ] RED: `test_unicode_signs_and_seed_metadata_have_distinct_dispositions` preserves U+2212/U+00D7 exactly, rejects missing/corrupt table cells, and identifies current `spell.acid_splash` school/area metadata conflict against the qualified source without rewriting frozen research. `test_thunderclap_is_separate_lawful_existing_extra` cannot infer provenance from package ancestry; missing legal/edition/Sorcerer/all-mode evidence fails that lane.
- [ ] Run `.hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_source_qualification.py`; RED must identify the absent qualification producer or the intended unresolved lane, never unavailable network accidentally treated as proof.
- [ ] Independently reconcile the exact licensed/visual table/tail evidence and formulate HDM requirement keys. Bind each repaired witness to its source asset and old raw span. Do not import legacy Telekinesis contests, old two-target Acid Splash, old Summon rosters, valid-glyph “repairs” or source-specific protected formulations.
- [ ] GREEN: rerun that module; assert accepted and rejection fixtures differ only in the admitted obligation being challenged. Publish source evidence checkpoint with exact version assessment, reviewer receipt, remote read-back and next cursor.

**Minimum Impact Envelope:** SPEC/APPROVED DESIGN = canonical§§3/4/21/23 + content-annex§§1/3 + owner decision; IMPLEMENTATION START HEAD = fresh recorded remote HEAD; PRIMARY OWNERS = source qualification and current package/character metadata owners. EXPECTED OWNERS = DEV qualification tool/schema/fixtures; EXPECTED CONSUMERS = SP16/content workers/build equality; ALLOWED INTERFACES = bounded DEV witness/roster functions above. GAME RUNTIME/PROJECTIONS = NOTICE/metadata semantic deltas only through shared writer; DEV MACHINE = new source proof schema, no admitted gameplay contract; PERSISTENCE/RECOVERY = none; VALIDATORS/TESTS/AUDITS = new focused source validator/test plus actual package conformance on publication; DOCUMENTATION/PACKAGE = attribution/provenance witness; CROSS-WAVE JOINS = SP16–26/SP29 source closure. PROTECTED INVARIANTS = lawful independent public formulation, exact typed identities, no blind import/no new non-SRD/no reopening closed body review; ARCHITECTURE-SENSITIVE = legal source qualification and source-vs-semantic hashes; INTEGRATION = source/roster/paired negatives + retained S6D07/11 when a shared metadata projection changes; OUT OF SCOPE = production runtime, general content import, class progression, gameplay/bootstrap/release inspection. VERSION IMPACT = DEV-only NONE with owner-law reason unless integrator changes semantic package members; SCHEMA/CATALOG/CHECKPOINT = development schema1, named source checkpoint, no coordinated catalog bump; MIGRATION = metadata repairs become explicit SP29 adoption inputs, no rewrite of accepted snapshots; HG-01 = no affected constraint expected, record actual check; CURRENTNESS RE-READ = task/specs/source obligations, actual source asset, seed/NOTICE/manifest and version owner.

**Receipt:** exact source asset/hash/page evidence, roster equality report, all item-level source dispositions, separate Thunderclap disposition, pairwise negative results, explicit unresolved lanes (must be none for final339 source closure), changed bytes and remote checkpoint HEAD.

## W05.SP16 — Complete source-specific supporting definition/action domains

**Deliverable:** every lawful creature/action/common-rule/species/feat dependency required by the promised spell modes has exact definition-kind/schema/executable-profile/primitive/native-consumer closure. Content presence alone is not executable support.

**Files/actions:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/supporting-content/common.json`, `creatures-beasts.json`, `creatures-other.json`, `actions.json`, `species.json`, `feats.json`; `DEV/TOOLS/validate_spell_content.py`; `DEV/TESTS/fixtures/spell-support-domains.json`; `DEV/TESTS/fixtures/spell-support-domains-rejected.json`; `DEV/TESTS/test_spell_support_domains.py`; `DEV/TESTS/test_spell_support_actions.py`. INSPECT_ONLY existing strict catalog-definition/actor-archetype/species/feat/feature/Activity/Asset/Effect/value/predicate schemas and current content-kind/primitive/selector/accessor/fact admission files. Required bounded strict-shape/registered-consumer deltas go to SP01 and the sole shared integrator; generic `details`/`resources` dictionaries are never an unvalidated mechanical escape hatch.

**Ownership:** records use existing `definition.actor_archetype`, `definition.activity`, `definition.species`, `definition.feat`, `definition.feature`, condition/Asset/Effect/resource kinds. Named shared actions appear once in `actions.json`; spell-created Animated Object/Otherworldly Steed/Draconic Spirit records/actions travel in their owning level5/2/5 spell shard, with exact references into common support. Do not duplicate current Human/Alert/Skilled/fighting-style definitions; the integrator either retains the existing authoritative seed record and references it, or moves it once with a coherent owner-qualified semantic comparison.

**Interfaces:** the three `validate_spell_content.py` functions above; pure eligible-domain producer returns exact sorted IDs for each source-specific predicate, including excluded names with reason in the development witness. Source-derived edges include each creature's feature/action/reaction/Legendary or recharge/resource mechanics when actually required, nested spell acquisition/casting entitlement, senses/movement/defenses, permitted retained fields, and prerequisites/choice/benefit dependents. No arbitrary `eligible_ids` passed by the player or fixture can declare completeness.

**Dependencies/checkpoints:** SP00 source qualification and SP01/02 strict sealed compiler HARD_PRECEDES SP16 definition/action-contract validation; lifecycle owners CONSTRAINS_WITHOUT_ORDERING. SP16 closes only `W05_SPELL_SUPPORTING_DOMAIN_INPUTS_READY`: complete qualified domain definitions, strict compiled action/profile/dependency closure and positive/negative golden boundary fixtures, with production-native proof explicitly NOT_ESTABLISHED. That independently GREEN input checkpoint HARD_PRECEDES SP28 and level preparation. SP28 consumes those inputs and emits `W05_SPELL_SUPPORTING_DOMAINS_READY` only after actual native action/profiling/recovery proof; that integrated output HARD_PRECEDES supported level-publication acceptance and SP29. SP16 does not wait for SP28 or mark native support complete. Review the common, Beast, other-creature/action, species and feat slices independently; the coordinator delegates bounded disjoint slices within this approved task; its total input checkpoint closes only after complete equality. No slice alone closes the complete-domain input census.

- [ ] RED: `test_complete_source_specific_form_domains` derives complete SRD CR0 Beast domain for Find Familiar, complete CR/level-qualified Beast domains for Polymorph/Animal Shapes, and full distinct Shapechange/True Polymorph creature domains. Omit one legal record/action and assert exact missing edge; add Construct/Undead to Shapechange and assert ineligible, while preserving True Polymorph's different predicate.
- [ ] RED: `test_undead_and_spell_created_blocks_require_executable_actions` requires Skeleton/Zombie/Ghoul/Ghast/Wight/Mummy support and exact owning-spell block references. Reject decorative stat blocks, omitted senses/actions, wrong action payer/recharge/Spellcasting profile and unsupported nested spell dependency before a cast can pay.
- [ ] RED: `test_reincarnate_species_and_wish_feat_graph_are_complete` requires every source-table species' traits/choices and the complete eligible SRD feat/prerequisite/benefit graph; missing prerequisite consumer or lingering removed-feat benefit fails. Existing Human/feats are single owned records. The GM species branch is exact accepted choice/adjudication, not new non-SRD import authorization.
- [ ] RED: `test_current_conjure_zone_rules_do_not_import_legacy_monsters` rejects foreign older Conjure creature rosters. `test_support_contract_kind_and_consumer_equality` rejects wrong definition kind, schema substitution, loose opaque mechanical detail, duplicate support ownership, primitive “active” without its actual native consumer and orphan unused consumer claims.
- [ ] Run `.hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_support_domains.py DEV/TESTS/test_spell_support_actions.py`; capture distinct intended REDs.
- [ ] Materialize only the derived legal census using strict admitted contracts, complete source-specific profiles and existing native owners. Add missing minimal contract/consumer deltas through the declared shared writer before claiming support. Source-domain closure is finite; runtime target CR/form selection is evaluated against that complete admitted local domain.
- [ ] GREEN unit/domain/golden boundary proof closes the input checkpoint; integrator publishes natural members, exact manifest/consumer projections and GREEN tests with source/definition/machine dimensions proved and native/performance dimensions NOT_ESTABLISHED. SP28 separately executes real Host actions for every required action/profile/nested spell entitlement and crash/resume/currentness/LIVE negatives, then emits the complete native-domain checkpoint with immutable exact proof references.

**Minimum Impact Envelope:** SPEC = canonical§§3/4/12/21/23 + execution§2 + lifecycle forms/body/control + content-annex§3; START HEAD = fresh exact read; PRIMARY OWNERS = reusable definition kinds/Activity contracts and native Actor/Asset/Effect/mechanical owners. EXPECTED OWNERS = six natural support files and bounded DEV producer/tests; CONSUMERS = source-bound forms/summons/Reincarnate/Wish, compiler, admission and SP29; INTERFACES = existing definitions/native-profile IDs plus explicit pure producer ABI. GAME = immutable package support only; DEV MACHINE = owner-supplied strict schema/profile/consumer deltas to single integrator; PERSISTENCE/RECOVERY = existing lifecycle/action owners, no new family; VALIDATORS/AUDITS = support producer + S6D07/09/11 and native action tests; DOCUMENTATION/PACKAGE = manifest/attribution via integrator; CROSS-WAVE = SP28 Host action producer, W06 promised-support proof. PROTECTED = one definition/state/digest owner, complete legal domains, exact acquisition/resource/prerequisite profiles, no entire class-progressions import, no legacy Conjure or new non-SRD; SENSITIVE = stat fields/actions/entitlement and feat dependency removal; INTEGRATION = actual native execution for all required supporting actions, stale/context/replay/recovery; OUT OF SCOPE = general monster AI, external books, broad class progression, new roles/service or manual stat sheet authority. VERSION = content package revision and material shared-module changes classified by integrator; SCHEMA/CATALOG = strict allowed-kind/profile deltas under SP01, no automatic coordinated generation; MIGRATION = any changed preexisting support semantics join exact comparator/adoption, retained old snapshots; HG-01 = none expected, record; RE-READ = specs/SP00 source-domain census/actual schemas/consumer registries/all touched member and package/version owners.

**SP16 receipt:** exact source eligible/excluded census, every support ID/kind/schema/profile/primitive/consumer edge, byte and generation-qualified semantic witnesses, source/definition/strict-action/golden closure equality, explicit outstanding native-proof keys and shared-writer input-checkpoint HEAD. **SP28 native-domain receipt:** all actual native action receipts/recovery frontiers/currentness negatives and complete production-proof equality bound to those exact published inputs; no counterfeit complete support from the SP16 input receipt.

## SP17–SP26 — Complete level shards, independent review gates

Each row below is one task. NEW_CREATE its exact GAME member, exact test module, and two fixtures `DEV/TESTS/fixtures/spell-level-N-expectations.json` / `DEV/TESTS/fixtures/spell-level-N-native-scenarios.json` (N is the row's literal level). Fixture records preserve every qualified source requirement/mode/branch/dependency key; independent expected arithmetic and native owner setup/accepted responses/crash points are explicit per entry. They cannot issue acceptance seals or raw current after-images.

**Common interfaces:** existing exact definition.spell/activity/effect/etc schemas; complete mode-to-Activity bindings and sealed compiler/read/consumer/dependency plans; SP16 support-row ABI. No new executor functions or services.

**Dependencies:** SP00/SP01/SP02 and SP16 `W05_SPELL_SUPPORTING_DOMAIN_INPUTS_READY` HARD_PRECEDES definition/machine preparation. Entry-specific SP03–SP15 owners constrain preparation; their completed checkpoints, SP28 and its `W05_SPELL_SUPPORTING_DOMAINS_READY` actual native proof HARD_PRECEDES supported-publication acceptance. Levels have disjoint writes and no ordering among them. SP26 Wish duplication joins complete <=8 mode closure from SP17–SP25; its preparation remains independent. All ten checkpoints JOIN_BEFORE_INTEGRATION SP29; SP30 is downstream release/target proof.

**RED/GREEN steps in every row:**
- [ ] Write `test_exact_source_mode_dependency_and_native_proof_equality` and the row's `test_source_specific_branches`; assert exact level count, all required mode/branch/contract/consumer/proof equality and source-specific positives/negatives below.
- [ ] Run the row's exact module with `.hdm-devtools/venv/bin/python -m pytest -q <literal row test path>`; intended RED is missing entry/mode/consumer/native proof, not unrelated infrastructure failure.
- [ ] Implement every source-row obligation in that member with accepted schemas/profiles and compiler APIs; independently sourced arithmetic covers every mode and branch.
- [ ] Run the same module GREEN after SP28. Real Host scenarios cover eligible receipts/state, interruption/reaction/decline/counter and paid invalid-target no-effect where applicable, before-payment missing-support blocking, stale offer/schema/state substitution, replay/idempotency and exact cold/LIVE recovery.
- [ ] Shared integrator publishes member+manifest+partial promise+active consumers+derived identities/legacy-body relocation in one GREEN checkpoint; reviewer and remote read-back close that row's checkpoint.

**Instantiated minimum Impact Envelope for EACH row:** SPEC = accepted spell specs/content-annex§§3–6 plus that exact source slice; START HEAD = fresh recorded dependency HEAD; PRIMARY OWNERS/EXPECTED OWNERS = one level recipe source and its exact files; EXPECTED CONSUMERS = compiler, admitted cast/lifecycle owners, SP29; ALLOWED INTERFACES = current exact definition/profile/primitive/read schemas, no per-entry service; GAME = immutable member plus shared-integrator manifest/partial promise/relocations; DEV MACHINE = task fixtures/proofs and requested bounded registry deltas for sole writer; PERSISTENCE/RECOVERY/CURRENTNESS = existing native Host/Resolution/Continuation footprints; VALIDATORS/TESTS/AUDITS = that module, SP16 equality and affected S6D07/09/11; DOC/INSTALL/PACKAGE = manifest/derived identities via integrator, no install/root README work; CROSS-WAVE JOINS = SP28/SP29/W06; PROTECTED = all modes/branches/support, lawful source, one owner, no new non-SRD/paid support gap/semantic chunk cap; SENSITIVE = source metadata/cost/target/lifecycle/recipient rules and exact accepted contexts; CROSS-MODULE VERIFICATION = real native scoped receipts/replay/recovery above; OUT OF SCOPE = worker writes to manifest/seed/shared registry, broad class acquisition, new state/services; VERSION = actual semantic package/module deltas under fresh owner law; SCHEMA/CATALOG/CHECKPOINT = no assumed generation bump, named level checkpoint; MIGRATION = changed existing mechanics join SP29 retained-context comparator/adoption; HG-01 = actual check, none expected; RE-READ = accepted specs, exact inventory/source-pass/qualified row, member paths, compiler/native/SP16/SP28 inputs and version policy.

**Receipt for EACH row:** source/mode/branch/support roster and arithmetic/proof equality; all entry real native receipts/state/frontiers/replay/cold-recovery witnesses; bytehash/semantic identity; exact shared-writer publication/head. Performance remains NOT_ESTABLISHED until target observation; no unproved mode is advertised.

### W05.SP17: level0 — 27 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-0.json`, `DEV/TESTS/test_spell_content_level_0.py`, `DEV/TESTS/fixtures/spell-level-0-expectations.json`, `DEV/TESTS/fixtures/spell-level-0-native-scenarios.json`. INSPECT_ONLY exact level0 source/support rows. Integrator also creates spell-content/existing-extras.json and relocates three SRD cantrips plus the separately proved Thunderclap extra.
**Source-specific assertions:** exact count27, complete all-row/mode equality; positives: Acid Splash complete sphere/character scaling/current school.evocation; Minor Illusion sound/image; Sorcerous Burst repeat dice; Resistance turn gate; True Strike weapon profile. Negatives fail: legacy two-target Acid Splash or old Poison Spray save recipe; any extra counted among27.
**Output:** `W05_SPELL_LEVEL_0_CONTENT_READY` with the common receipt. Anchor cases supplement all27 entry proofs; they are not representative coverage.
### W05.SP18: level1 — 57 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-1.json`, `DEV/TESTS/test_spell_content_level_1.py`, `DEV/TESTS/fixtures/spell-level-1-expectations.json`, `DEV/TESTS/fixtures/spell-level-1-native-scenarios.json`. INSPECT_ONLY exact level1 source/support rows. Integrator relocates existing Magic Missile/Burning Hands bodies; choice commitments remain until SP27/29.
**Source-specific assertions:** exact count57, complete all-row/mode equality; positives: Sleep own-turn two-stage saves/helper/damage ending; Find Familiar full CR0 forms/senses/actions/relay; Magic Missile simultaneous darts; Shield; Unseen Servant force proxy. Negatives fail: legacy Sleep HP pool or omitted familiar form/action/stage.
**Output:** `W05_SPELL_LEVEL_1_CONTENT_READY` with the common receipt. Anchor cases supplement all57 entry proofs; they are not representative coverage.
### W05.SP19: level2 — 57 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-2.json`, `DEV/TESTS/test_spell_content_level_2.py`, `DEV/TESTS/fixtures/spell-level-2-expectations.json`, `DEV/TESTS/fixtures/spell-level-2-native-scenarios.json`. INSPECT_ONLY exact level2 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count57, complete all-row/mode equality; positives: Find Steed complete Otherworldly Steed type/scaling/actions/healing mirror; Alter Self modes; Detect Thoughts fixedDC; Mirror Image hit frontier; Prayer of Healing rest gates. Negatives fail: displaced Steed omission/foreign FindPath edge or generic contested Detect Thoughts.
**Output:** `W05_SPELL_LEVEL_2_CONTENT_READY` with the common receipt. Anchor cases supplement all57 entry proofs; they are not representative coverage.
### W05.SP20: level3 — 42 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-3.json`, `DEV/TESTS/test_spell_content_level_3.py`, `DEV/TESTS/fixtures/spell-level-3-expectations.json`, `DEV/TESTS/fixtures/spell-level-3-native-scenarios.json`. INSPECT_ONLY exact level3 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count42, complete all-row/mode equality; positives: Counterspell Constitution save with initiating action spent/slot preserved; all Glyph payload modes; Haste successor; Revivify consumed material; current Conjure Animals zone. Negatives fail: legacy spell-level Counterspell check, shared refund policy or old Conjure roster.
**Output:** `W05_SPELL_LEVEL_3_CONTENT_READY` with the common receipt. Anchor cases supplement all42 entry proofs; they are not representative coverage.
### W05.SP21: level4 — 34 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-4.json`, `DEV/TESTS/test_spell_content_level_4.py`, `DEV/TESTS/fixtures/spell-level-4-expectations.json`, `DEV/TESTS/fixtures/spell-level-4-native-scenarios.json`. INSPECT_ONLY exact level4 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count34, complete all-row/mode equality; positives: Polymorph current HP retained/form tempHP source cleanup; Control Water modes; Death Ward zeroHP/death interception; Secret Chest Assets/contents; Dominate Beast control/reaction. Negatives fail: stale replacementHP, newer tempHP erased or omitted Control Water mode.
**Output:** `W05_SPELL_LEVEL_4_CONTENT_READY` with the common receipt. Anchor cases supplement all34 entry proofs; they are not representative coverage.
### W05.SP22: level5 — 38 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-5.json`, `DEV/TESTS/test_spell_content_level_5.py`, `DEV/TESTS/fixtures/spell-level-5-expectations.json`, `DEV/TESTS/fixtures/spell-level-5-native-scenarios.json`. INSPECT_ONLY exact level5 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count38, complete all-row/mode equality; positives: Animate Objects complete owning block/size actions/Asset return; Reincarnate species redraw/choice; Summon Dragon owning Draconic Spirit; Telekinesis licensed fine control; Planar Binding duration; Wall of Stone successor. Negatives fail: unproved licensed tail, semantic redraw cap, legacy opposed-check continuation or missing spell-created block.
**Output:** `W05_SPELL_LEVEL_5_CONTENT_READY` with the common receipt. Anchor cases supplement all38 entry proofs; they are not representative coverage.
### W05.SP23: level6 — 31 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-6.json`, `DEV/TESTS/test_spell_content_level_6.py`, `DEV/TESTS/fixtures/spell-level-6-expectations.json`, `DEV/TESTS/fixtures/spell-level-6-native-scenarios.json`. INSPECT_ONLY exact level6 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count31, complete all-row/mode equality; positives: Create Undead source-specific Ghoul/Ghast/Wight/Mummy and slot closure; Contingency child; FindPath own tail; Guards and Wards shapes; MagicJar principal/body; Harm actual-dealt maxHP coupling. Negatives fail: foreign tail/header interpreted as rule, broad trigger history scan, omitted undead action or possession bypass. Animate Dead's Skeleton/Zombie domain is proved by SP20 and the combined SP16 support census.
**Output:** `W05_SPELL_LEVEL_6_CONTENT_READY` with the common receipt. Anchor cases supplement all31 entry proofs; they are not representative coverage.
### W05.SP24: level7 — 20 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-7.json`, `DEV/TESTS/test_spell_content_level_7.py`, `DEV/TESTS/fixtures/spell-level-7-expectations.json`, `DEV/TESTS/fixtures/spell-level-7-native-scenarios.json`. INSPECT_ONLY exact level7 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count20, complete all-row/mode equality; positives: Prismatic Spray [8,1,1] -> [1,1] and [8,8,1,2] -> [1,2]; Teleport mishap repeats; Simulacrum no-recursive/retained profile; Regenerate anatomy; planes/room contents. Negatives fail: duplicate-ray rejection, probability-changing cutoff, lost resumed frontier or recursive Simulacrum.
**Output:** `W05_SPELL_LEVEL_7_CONTENT_READY` with the common receipt. Anchor cases supplement all20 entry proofs; they are not representative coverage.
### W05.SP25: level8 — 17 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-8.json`, `DEV/TESTS/test_spell_content_level_8.py`, `DEV/TESTS/fixtures/spell-level-8-expectations.json`, `DEV/TESTS/fixtures/spell-level-8-native-scenarios.json`. INSPECT_ONLY exact level8 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count17, complete all-row/mode equality; positives: Antipathy/Sympathy both modes/exact tail/return; Animal Shapes full Beast actions; Clone maturity/death/body; Antimagic exceptions/deadlines; Tsunami phases. Negatives fail: foreign AnimateObjects edge, erased suppressed deadline/identity or omitted source-specific mode/exception.
**Output:** `W05_SPELL_LEVEL_8_CONTENT_READY` with the common receipt. Anchor cases supplement all17 entry proofs; they are not representative coverage.
### W05.SP26: level9 — 16 SRD entries

**Files:** NEW_CREATE `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/spell-content/level-9.json`, `DEV/TESTS/test_spell_content_level_9.py`, `DEV/TESTS/fixtures/spell-level-9-expectations.json`, `DEV/TESTS/fixtures/spell-level-9-native-scenarios.json`. INSPECT_ONLY exact level9 source/support rows. Shared files stay integrator-owned.
**Source-specific assertions:** exact count16, complete all-row/mode equality; positives: Wish all eight modes/stress/real P2 History; True Polymorph three conversions/SS2-01/current-state return/permanence/control expiry; Shapechange first-form-only tempHP; Prismatic Wall layers; Time Stop/Astral. Negatives fail: missing feat graph/real P2 History, retry reroll, stale Actor return, artificial future source coverage gate or refreshed tempHP on form switch.
**Output:** `W05_SPELL_LEVEL_9_CONTENT_READY` with the common receipt. Anchor cases supplement all16 entry proofs; they are not representative coverage.

## W05.SP27 — Initial source-owned 4+2 selected union, defaults, focus and adoption inputs

**Files/actions:** NEW_CREATE `GAME/TOOLS/character_spell_acquisition.py`; `DEV/TESTS/test_character_spell_acquisition.py`; `DEV/TESTS/fixtures/spell-acquisition-adoption.json`. INSPECT_ONLY `DEV/TOOLS/validate_character_mvp_seed.py`, `DEV/TESTS/test_s6d_07_character_mvp_seed.py`, `DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json` and the actual seed/capability files; prepare their exact selected-union/mismatch/Actor-fixture cutover inputs for the sole SP29 writer. SP29 EXISTING_MODIFYs those paths and `character-mvp-seed.json` slot/default/focus definitions together, so the current baseline remains GREEN before promotion. INSPECT_ONLY existing build-choice-slot/advancement/world-actor schemas, `catalog_runtime.py`, `ruleset_package.py`, character owner and held P1A/P1B plan.

**Interfaces:** pure `derive_initial_spell_grants(advancement: Mapping[str,object], choice_bindings: Mapping[str,object], *, catalog: AdmittedActivityCatalog) -> Mapping[str,object]` returns exactly `cantrip_spell_ids, level_1_spell_ids, known_spell_ids, prepared_spell_ids, required_activity_ids, required_dependency_ids, starting_asset_grants`; no spellbook field. `derive_legacy_spell_choice_mapping(actor: Mapping[str,object], *, adopted_catalog: AdmittedActivityCatalog, candidate_catalog: AdmittedActivityCatalog) -> Mapping[str,object]` returns exact original/candidate choice-binding and dependency mapping or typed unsupported reason; it performs no native write, compatibility verdict, grant or fresh choice. Existing `evaluate_ready_pc(actor, resolved_package, evidence=None)` preserves its return shape and `spell_selection_binding_mismatch`, consuming selected union and entire selected support closure instead of options[0]/activity_ids[0]. P1A/P1B consume these helpers only after their actual activation and SP29-supported catalog; SP27 does not implement those held services or a READY flag.

**Definitions:** two player-or-delegated slots `advancement.sorcerer.level_1.cantrips` minimum=maximum4 and `advancement.sorcerer.level_1.prepared_spells` minimum=maximum2. Each exact owner-relative `option.spell.<existing_suffix>` grants one eligible spell; cantrip known singleton, level1 known+prepared singleton. Exact SRD option subsets equal the annex's named16 cantrips/21 level1 entries; named lawful existing extras are separate and disjoint. The known union is all six acquired IDs; prepared equals selected level1 pair; no generic cross-class prepared/known law. Preserve default Fire Bolt/Poison Spray/Thunderclap/Acid Splash plus Magic Missile/Burning Hands when lawful and complete; if extra lane cannot close, content owner repairs the new default explicitly and atomically, retains original snapshots/accepted work and records exact compatibility/mapping evidence. No runtime substitute or new PO gate. One deterministic starting-focus grant uses existing starting_assets carrier, once; selecting four cantrips never grants four foci.

**Dependencies/output:** SP00 lawful eligibility and SP01/02 sealed catalog HARD_PRECEDES; SP17/SP18 complete option modes and SP28 source-native execution proof JOIN_BEFORE_INTEGRATION candidate closure. `W05_SPELL_INITIAL_ACQUISITION_CONTRACT_READY` joins SP29; actual P1A/P1B offers/READY_PC wait for SP29 supported context and their original owner gates. Independent P2/P3 eligibility remains unchanged.

- [ ] RED `test_nondefault_selected_union_is_authority`: pick four legal nondefault cantrips/two legal nondefault level1 entries; assert known=C union P, prepared=P, |C|4/|P|2/C intersect P empty and exact all-mode transitive required Activity/dependency closure, not default or first Activity.
- [ ] RED `test_binding_mismatch_negatives_remain_terminal`: duplicate options/grants, cross-slot ID, wrong class/level, too few/many, extra legal-but-unselected ID, omitted prepared spell, unsupported mode, stale/foreign context, missing selected dependency and bad default all reject with retained mismatch/support reason. `test_pool_and_focus_equality` asserts exact16/21 SRD subset and separate Thunderclap lane plus one focus.
- [ ] RED `test_legacy_mapping_preserves_same_campaign_choices_and_accepted_context`: resolve original bundle in exact retained snapshot; map its four/two unchanged where lawful; retained Resolution/Continuation still uses old context; missing old dependencies blocks; changed options/metadata cannot return assumed COMPATIBLE_ADDITIVE. A repaired new default is explicit, never a silent change to an accepted choice.
- [ ] Run `.hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_character_spell_acquisition.py`, capture intended RED; implement the pure helper against an exact source-closed compiler-issued candidate conformance catalog. Rerun that module GREEN and the unchanged current S6D07 baseline module; prepare the exact validator/seed/current-Actor-fixture cutover for SP29. Source component support must be installed, but READY_PC does not require a current target or every priced consumed material in hand; cast preflight owns scene/resources/components.
- [ ] Publish the independently testable pure helper/candidate/adoption fixtures and GREEN tests. SP29 atomically integrates live seed/validator/current fixture/default promotion with comparator/adoption/native-commit/full-profile evidence. Preserve fixed pre-exposure commitments and accepted current HP/resources/Asset IDs on mapping/repeat.

**Minimum Impact Envelope:** SPEC = content-annex§2/4 + character amendment/execution§2/canonical§4/22; START HEAD = fresh exact dependency HEAD; PRIMARY OWNERS = initial advancement choices/Actor build bindings. EXPECTED OWNERS = pure helper/DEV validator/tests and integrator's exact slot/default/focus definitions; CONSUMERS = compiler, held P1A/P1B, readiness conformance/SP29; INTERFACES = the two pure functions/closed mapping above, existing definition slot shape/evaluate_ready_pc return; GAME = pure source derivation and immutable choice definitions, no semantic establishment; DEV MACHINE = coherent selected-union validation, existing schemas unless actual allowed-contract delta proved; PERSISTENCE/RECOVERY = exact old/candidate contexts and mapping inputs, actual adoption native write SP29; VALIDATORS/AUDITS = new helper/S6D07/11/catalog closure; DOC/PACKAGE = candidate profile/default/adoption evidence; CROSS-WAVE = held P1A/P1B consume after actual package promotion. PROTECTED =4+2/known-all6/prepared2/onefocus/source eligibility/complete support, no post-exposure choice/no blanket castable-known rule/no second readiness owner; SENSITIVE = choice identity/default commitments/exact context/old snapshot retention; INTEGRATION = nondefault alternatives, mismatch negatives, source support and same-campaign exact adoption; OUT OF SCOPE = future class/preparation/replacement, actual P1A/P1B activation, History/Story, general migration service; VERSION = new module revision1 under actual engine line, changed package/module/projections under owner law; SCHEMA/CATALOG/CHECKPOINT = no automatic generation, initial-acquisition checkpoint above; MIGRATION = old bundle interpretable in its original snapshot, explicit comparator/adoption mapping SP29, never silent additive assumption; HG-01 = none expected, record actual; RE-READ = source list/qualified extras, exact advancement/Actor schemas and seed/capability/validator bytes, admitted catalogs, package identity/comparator/retention/version owners.

**Receipt:** exact37 SRD option equality plus separately named extra disposition, selected-union/mismatch/focus tests, default legal/full-support witness or explicit repair record, original-to-candidate mapping and blocked compatibility negatives, integration consumer dependencies, changed byte/read-back HEAD.


## W05.SP28 — Composed native spell execution and owner-consumer joins

**Dependencies:** accepted SP00 source qualification, SP01..SP15 mechanism checkpoints and SP16 W05_SPELL_SUPPORTING_DOMAIN_INPUTS_READY; accepted P0 CurrentOwnerView. Wish/History integration additionally consumes actual W05_T06_NATIVE_HISTORY_DISCOVERY_READY from P2. This edge gates the Wish integrated checkpoint, not SP00..SP14, content preparation or independent P2/P3. SP28's whole checkpoint waits for the Wish join. SP28 has no dependency on completion of the ten level shards: it uses finite lawful source-backed qualification recipes and makes no full339 claim.

**Result:** an actual campaign-bound host runs admitted partial spell Activities through native consequences, closure and recovery. Source-backed fixture recipes test the real producer; fixture events, owner after-images and FixedRng dictionaries never impersonate accepted authority.

**File actions / interfaces:**
- EXISTING_MODIFY GAME/TOOLS/runtime_host.py: one final profile-dispatch integrator binds the admitted Activity catalog, CurrentOwnerView, existing accepted command/closure, SegmentRngProvider and native adapters; expose immutable ExecutionService.execute_intent_plan(intent_plan: Mapping[str,object], *, catalog: AdmittedActivityCatalog) -> Mapping[str,object] and resume(accepted_command: Mapping[str,object], continuation: Mapping[str,object], response: Mapping[str,object] | None, *, catalog: AdmittedActivityCatalog) -> Mapping[str,object]. Recheck catalog/compiled recipe identity and host issuance before use. Caller parameter catalog is an already admitted matching handle, never a means of selecting a trust domain.
- EXISTING_MODIFY GAME/TOOLS/activity_runtime.py: realize canonical plan_next_segment(catalog, compiled, accepted_command, resolution, *, owner_session, rng, procedure_state=None, continuation_state=None) -> NativeSegmentPlan using the finite admitted profiles and SP08..SP15 pure builders. Integrate each primitive-to-consumer mapping once at this checkpoint; reject unregistered pair/profile/read/input contracts and generic rule.* escape hatches.
- EXISTING_MODIFY GAME/TOOLS/native_execution.py: integrate validators/complete companion closure for every produced native profile and dedicated Wish replacement. Only this final integrator joins additional owner validators into the SP04 kernel. No preparation fragment is executable establishment.
- EXISTING_MODIFY GAME/TOOLS/runtime_execution.py, current_owner.py, hot_store.py, live_state.py, durability.py, publication.py, recovery.py, recovery_roots.py, temporal.py, information.py, history.py, actor_continuity.py and id_allocator.py only for named native profile/currentness/companion/consumer joins supplied by SP04/SP08..SP15. Preserve their authorities and APIs outside those joins.
- EXISTING_MODIFY DEV/CATALOG/core-catalog.json, mechanical-surfaces.json, catalog-admission-ledger/manifest.json and applicable existing families/{activity_primitives,mechanical_accessors,rule_operations,rule_selectors,protocol_value_kinds}.json; activity-primitive-contracts/manifest.json, shared/{read_contracts,value_contracts}.json and exact admitted primitives/op.*.json shards; applicable SP01 DEV schema dispatch and owning metadata projections. These are the serialized coordinator's actual consumer/profile/primitive/pair registration joins, preserving the exact17+17 families and the current ledger discipline. Close the actual supported contract inventory without blanket activation of unrelated members; synchronize current coordinated metadata and builder engine inventory. Every machine row names its actual compatible producer/consumer and proof. No opaque generic policy or additional family.
- EXISTING_MODIFY GAME/TOOLS/bootstrap.py: trusted deployment composition passes one admitted local catalog/engine contract and existing native infrastructure; retain selected-campaign fail-closed composition and P0 services. compose_runtime_host may gain keyword-only optional admitted_activity_catalog and segment_rng_provider parameters for the trusted infrastructure path; when absent, existing unrelated services continue but execution requiring them is unavailable. Check exact issuance/context/campaign/frontier; no game prompt or caller-created replacement adapters.
- NEW_CREATE DEV/TESTS/test_spell_host_native_integration.py and DEV/TESTS/test_wish_host_reconciliation.py; EXISTING_MODIFY test_runtime_host_composition.py, test_rd05_runtime_execution.py, test_rd06_durability_publication.py, test_rd07_recovery.py, test_rd08_temporal.py, test_rd09_access_live.py, test_rd11_context_runtime.py, test_rd13_story_t0_commentator.py and test_step3_resume_ordering_contract.py only for actual new consumers. Isolated pure conformance fixtures retain their qualified role.

**Exact integration laws:** native health/resources/assets/effects/zone/Information and runtime Procedure/Resolution/Continuation/RNG/events/receipt/mandatory children/idempotency/dirty changes establish under the one existing lawful fenced owner boundary. CurrentOwner read sessions require/reacquire the complete finite owner union and prove exact predecessor generations. LIVE is exact-source CAS followed by confirmed HOT adoption, never a distributed SQLite/network transaction. PT-D1 consumes actual nested BoundCatalogContext.basis/catalog identity; PT-D2 forwards the owner-issued ExecutionDurabilityJoin unchanged and rejects mismatched campaign/route/command/input/Resolution/segment/event/generation/companion closures before dispatch. Native establishment enrolls minimal original RecentRollWitness and complete causal ReconciliationDependencyEdge while its protection window is legal, without full history scans. Pending accepted refs protect required evidence. Dedicated Wish closes/finalizes/freezes/absorbs required sources via actual WP16 producer receipts, preserves earlier successful close on later failure, then establishes one owner-atomic counterfactual replacement plus current-validity relation. Old raw RNG/events/choice/messages/exposure remain immutable; no accepted mutation replay, whole-owner restore or generic rollback. Replacement acceptance followed by publication failure recovers forward.

True Polymorph creature-to-object uses the exact SS2-01 accepted profile and protected ObjectSuspensionBasis: neutral principal, physical Asset subject, dormant current resources, one current object/gear closure and pre-outcome return adjudication. No Actor-body health accessor, remembered damage history sum or imported older-edition formula can discharge that consumer. Intermediate shape fragments never establish.

Actual semantic event/current validity is consumed by existing Information and P2-produced History/Context; future Story routing carries the relation when its normal producer activates. No Story output or dedicated LLM call is added here. Same-operation emitted result is only accepted eligible receipt exports; technically pending work is represented honestly.

**RED / GREEN witness sequence:** first reproduce real host command acceptance with admitted source context and a native consequence missing, and both PT-D1 nested-carrier/PT-D2 forwarding failures. Assert failure for those causes; repair only approved joins. Then test native HP/effect/resources visible before SAVE, allocator+creation atomicity, mandatory nested/reaction/time closure, actual temporal effect invocation/suppression/dispel, paid secret-invalid target with restricted disclosure, fixed roll retry/cold recovery, authority movement, capacity RUNNING Continuation, command.settled only after complete children, LIVE pre-CAS exclusion/confirmed adoption and indeterminate dispatch reconciliation. Wish tests cover eligibility boundary, original/new selection, same corresponding draws/new branch draws, cost/stress on original selection, complete affected enrollment, two-source partial close, one native replacement, no erasure of exposure, and publication failure after replacement. Add forged plan/receipt/context/RNG/frontier and mixed/flattened alias negatives. Reuse actual owner-local suites, not synthetic evidence flags.

~~~sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_host_native_integration.py DEV/TESTS/test_wish_host_reconciliation.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd05_runtime_execution.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd08_temporal.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_step3_resume_ordering_contract.py
~~~

**Output:** W05_SPELL_NATIVE_HOST_READY; W05_WISH_NATIVE_RECONCILIATION_READY; W05_SPELL_SUPPORTING_DOMAINS_READY after actual complete supporting-action/native proof. SP16 definition-input checkpoint is the earlier input, so this native proof cannot form a cycle. Publish the whole coherent checkpoint after required independent spec/quality review; source-backed qualification catalogs remain explicitly partial.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: parent SP-05..24 as applicable; execution annex §§4..10; lifecycle annex exact profiles; Wish WR-01..08; current Step3/WP12..WP19/native owners and T06-A1.
- IMPLEMENTATION START HEAD / PRIMARY OWNER ARTIFACTS: fresh coordinator remote HEAD after required checkpoints; pin every listed source and selected owner contract in assignment manifest.
- EXPECTED OWNERS TO CHANGE: existing Activity/native/host adapters and named lifecycle/temporal/information/durability/recovery consumers, not their semantic ownership.
- EXPECTED CONSUMERS TO CHANGE: deterministic host execution, CurrentOwnerView, current semantic-event/Information/History consumers and recovery.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: listed bound service/dispatch and exact profile/consumer/companion joins, PT-D1/PT-D2; no arbitrary backend/adjudication/payload injection.
- GAME RUNTIME / PROJECTION SURFACES: listed TOOLS only; shipped CORE/install changes reserved to T08.
- DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01 closed shapes, exact finite admitted consumer/profile/primitive/pair ledger joins and synchronized engine inventory/projections above; no new law, family or unplanned member.
- PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: exact native/HOT/LIVE source and existing owner-first recovery; fixed IDs/RNG and protected Wish evidence/current-validity relation.
- VALIDATORS / TESTS / AUDITS: named suites, all relevant SP01..SP15 owner suites, strict schema/primitive/selector conformance and actual maintenance audit.
- DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: task evidence/cursor only; full package semantic claim is SP29, CORE/install T08.
- CROSS-WAVE JOINS: accepted Waves01..04/P0; actual P2 History joins Wish; SP29/content native-mode proofs consume host output.
- PROTECTED ARCHITECTURE INVARIANTS: one-chat logical roles, no extra model/web/census on warm cast; one native authority; exact state/context/currentness; atomic local or lawful LIVE edge; no replay/reset/rollback/global frontier.
- ARCHITECTURE-SENSITIVE SURFACES: accepted command/RNG/native plan issuance, companion closure, Wish bounded retention/reconciliation and TruePoly protected return policy.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: above positive/negative and full owning SP04..SP15 suites; actual source->command->native->durability->publication->receipt->recovery.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: new semantic owner, generic rule engine/geometry/soul/timeline/distributed transaction; content-full claim, P1A/P1B implementation, unrelated Story activation.
- VERSION IMPACT: actual logical edits to versioned modules each increment once from fresh values under DEV/RELEASE/VERSIONING.md; SP04 earlier edits remain preserved. New versions are not guessed from historical targets.
- SCHEMA / CATALOG / CHECKPOINT IMPACT: consume canonical closed profile generations; any required compatibility change follows exact already accepted family/digest/adoption law; output does not claim full339 availability.
- MIGRATION IMPACT: SP20/current adoption owner, preserve accepted old contexts; never regenerate RNG/IDs to translate accepted work.
- HG-01 CONSTRAINTS AFFECTED: preserve exact unchanged owner binding; verify material changes against current HG-01 owner, no invented exception.
- CURRENTNESS RE-READ SET BEFORE WRITE: actual SP00..SP16/P0/P2 checkpoints, all listed shared files and owner/version/native profile consumers; freeze independent reviews to same integrated bytes.

## W05.SP29 — Full package support, acquisition and adoption join

**Dependencies:** SP00..SP27 outputs, W05_SPELL_NATIVE_HOST_READY, W05_WISH_NATIVE_RECONCILIATION_READY and actual all-mode native conformance for every claimed entry/required action. This is the single final full-profile advertisement writer; honest partial-profile checkpoints precede it. Full claim is not a prerequisite of its own host/conformance tests.

**File actions / interfaces:**
- EXISTING_MODIFY GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/ruleset-package-manifest.json, character-capabilities.json, character-mvp-seed.json, NOTICE.md and the SP16-created semantic support/spell-capability members, exact retained source provenance and snapshots. Preserve mechanically relocated seed bodies from SP17/SP18; new selected-union defaults/focus/adoption promotion happens here after SP27 proof.
- EXISTING_MODIFY GAME/TOOLS/ruleset_package.py, catalog_runtime.py and activity_runtime.py only for complete package closure/adoption/runtime-owned conformance reconstruction already selected by SP01/SP02/SP27. Use existing build_snapshot, build_resolved_lock, compare_resolved_sets and compile_conformance_attestation APIs; no new digest owner.
- EXISTING_MODIFY DEV/TOOLS/validate_ruleset_package_closure.py, validate_domain_rules_coverage.py and validate_character_mvp_seed.py; EXISTING_MODIFY DEV/TESTS/fixtures/s6d-07-character-mvp-actors.json together with the seed/options/default/focus cutover. Register exact source/support/mode/native-proof validator IDs and synchronize closed suite/schema/inventory consumers; no bypass toggle. Modify DEV/TOOLS/release_builder.py only for the already required path-neutral compiled runtime-owned evidence integration proven by its owning RED. Current source/domain/seed validators are real consumers, not inspect-only after promotion. NEW_CREATE DEV/TESTS/test_spell_package_full_support.py and fixtures/spell-full-support-proof.json; EXISTING_MODIFY test_s6d_07_character_mvp_seed.py, test_s6d_09_domain_rules_coverage_contract.py, test_s6d_11_ruleset_package_closure.py, test_rd15_catalog_runtime.py, test_catalog_definition_binding_contract.py, test_implementation_package_version_cutovers.py and test_runtime_package_provenance.py only for admitted inputs/current version evidence.
- One coordinator regenerates existing resolved-lock/inventory/attestation projections from exact admitted bytes and producer proof, preserving old accepted contexts. Runtime-owned conformance evidence has an explicit owning schema and is included through the package builder; DEV reports never become runtime dependencies.

Close typed set and relation equalities: promised339 lawful source entries == package339 SRD entries; exact requirement and all-mode keys == source mappings == production native proof keys; transitive domains/actions/feats == admitted dependency closure; active primitive/selector/accessor/value/policy obligations == real compatible consumers. Separately prove explicitly named existing extras; Thunderclap never counts among339. Report stages independently; 339 design rows/fixture names/census or native kernel green alone cannot justify full support.

Acquisition uses exact16 SRD cantrips/21 SRD level1 subset plus only individually proved existing extras, selected4+2 options -> known-all6/prepared-two, all selected Activities closure, singleton focus grant, explicit alternative before READY_PC. Preserve legal existing recommendation; unresolved lawful-extra qualification causes explicit content-owner default/adoption repair from the existing legal pool before release, not a new human product gate. Test old option.spells.mvp_default exact snapshot interpretation and explicit two-binding adoption; no silent additive compatibility assumption or resource/gear reset.

**RED / GREEN:** construct omissions of one source mode, one otherwise plausible action/feat/domain member, one exact consumer/primitive mapping and one required actual native proof while count remains339. Full-profile admission must reject each. Repair lawful requirements/recipes/consumer/proof, never shrink promised SRD roster. Reject duplicate seed/shard definitions, body/metadata/source mismatch, forged attestation/context/lock, extra SRD option or omitted legal option, selected/prepared mismatch and unsupported newer identity contracts. Positive full union, independent comparator/migration/adoption, retained snapshot and current context reconstruct exactly. Confirm no GAME artifact opens DEV paths.

~~~sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_package_full_support.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_s6d_09_domain_rules_coverage_contract.py DEV/TESTS/test_s6d_11_ruleset_package_closure.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_catalog_definition_binding_contract.py DEV/TESTS/test_implementation_package_version_cutovers.py DEV/TESTS/test_runtime_package_provenance.py
~~~

**Output:** W05_FULL_SRD_SPELL_PACKAGE_READY; W05_SORCERER_ACQUISITION_CONTEXT_READY. P1A's materialization entry now requires these actual published outputs; it does not repeat source/kernel tasks.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: SP-01..05/15/19/20, content/acquisition annex §§1..6, machine/package/domain/S6D-07/adoption/version owners.
- IMPLEMENTATION START HEAD / PRIMARY OWNER ARTIFACTS: fresh remote candidate after all named proof targets; pin exact source/mode/required-key equality inputs and complete producer evidence.
- EXPECTED OWNERS TO CHANGE: existing package semantics/capability/seed and derived builder/validator/conformance projections; no additional gameplay state owner.
- EXPECTED CONSUMERS TO CHANGE: load/cache/adoption/recovery/catalog binding, selected-option validator, P1A/P1B future consumers and release builder.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: exact package/compiled support/value/profile schemas and validators already selected, two-slot acquisition/default/focus/compatibility mapping; existing digest ownership unchanged.
- GAME RUNTIME / PROJECTION SURFACES: listed package and TOOLS; no runtime DEV dependency.
- DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: SP01 admitted schemas/current consumer inventory, per-mode proof projection and exact source/domain obligations; coordinated metadata synchronized by one integrator.
- PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: retained context/Resolution/Continuation/catalog basis and current adopted package; exact owner frontiers, no snapshot retuning.
- VALIDATORS / TESTS / AUDITS: named native/scenario/equality/seed/package/currentness suites plus actual maintenance audit and required broader DEV tests.
- DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: source attribution/package NOTICE, exact builder projections and task evidence; T08 owns shared install/CORE.
- CROSS-WAVE JOINS: accepted catalog/context/native owners; SP28 actual host; P1A/P1B and W06 consume proven package.
- PROTECTED ARCHITECTURE INVARIANTS: truthful full-mode support, no second namespace/digest/state/service, exact lawful membership/defaults/currentness, hidden deterministic math, no warm corpus work.
- ARCHITECTURE-SENSITIVE SURFACES: capability promises, source admission, native evidence, semantic comparator/compatibility, acquisition known/prepared interpretation.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: all ten content mode suites + supporting-domain suite + actual host native tests + exact identity/adoption/equality negatives.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: full class/character corpus, new non-SRD content, new domain-valued options outside source, automatic campaign migration/release/gameplay.
- VERSION IMPACT: run actual namespace-specific gate; each logical package/member/module transition once from fresh values, synchronize coordinated projections. Package revision is order, same generation is eligibility only; no automatic engine release bump.
- SCHEMA / CATALOG / CHECKPOINT IMPACT: source-profile/capability/attestation exact schemas and already admitted contracts; counterfactual/identity generations follow accepted owners, do not invent a flat alias.
- MIGRATION IMPACT: explicit comparator-derived adoption/translation for changed advancement/options/membership; preserve original snapshots/commitments and fail absent dependencies.
- HG-01 CONSTRAINTS AFFECTED: unchanged native owner/knowledge/privacy constraints; verify current owner.
- CURRENTNESS RE-READ SET BEFORE WRITE: all required task proof inputs as applicable, exact current package/seed/manifest/shards/extras/NOTICE/builder/compiled context/snapshots/projections and version/adoption owners.

## W05.SP30 — Installed offline spell runtime and target cost proof

**Dependencies:** W05_FULL_SRD_SPELL_PACKAGE_READY, W05_SPELL_NATIVE_HOST_READY and Wish native join. Full release proof additionally joins normal T06/T07/T08/W06 gates; this task cannot bypass them.

**File actions / interfaces:**
- NEW_CREATE DEV/TESTS/test_spell_offline_runtime.py and test_spell_runtime_cost_shape.py. NEW_CREATE DEV/TOOLS/measure_spell_runtime.py: measure_selected_spell_runtime(host, invocation_set, *, measurement_sink, target_metadata) -> report over existing real adapters, without replacing accepted execution/RNG/model authorities. Reports explicitly distinguish actual model execution from model-free harness observations.
- EXISTING_MODIFY DEV/TESTS/test_release_builder.py, test_release_game_passthrough.py and test_runtime_package_provenance.py for required actual shipped semantics/evidence/transitive support; EXISTING_MODIFY DEV/TOOLS/release_builder.py only if an owning RED proves current package member/evidence omission.
- NEW_CREATE DEV/TESTS/fixtures/spell-runtime-cost-scenarios.json: finite named cold/warm/cast/save/LIVE/recovery and legitimate-large-set cases, qualified context/size configurations. Task measurement report belongs to existing Wave05 cursor evidence or DEV/docs/superpowers/research/2026-10-04-spell-coverage/runtime-performance.md, not another executable plan.
- INSPECT_ONLY current WP24 owner, exact target/VPS tool/provider capabilities and release/runtime metadata. Root architecture session runs no runtime package inspection; the worker's authorized packaging proof inspects the build generated from its exact candidate.

**Witnesses:** run real host/native/cold-recovery paths with external rule/network lookups blocked. Rules offline means no web rules, not removal of required persistence/LIVE transport. Missing/corrupt member or expired local context blocks before supported cast costs, as distinct from missing world fact, lawful paid invalid target, genuine adjudication and capacity continuation. All339 mode proof remains exact and installed supporting actions/features/forms are usable through native owners. Warm selected cast does not rehash/recompile/re-census entire corpus; sealed-handle tamper/currentness negatives remain. Native accepted partial work/reaction/costs/IDs/RNG survive display/model/publication/recovery failure.

Record physical model invocations and serial depth, prompt/context/receipt bytes and tokens, catalog/recipe cache admissions/hits/invalidation, primitive/local CPU work, native local/remote reads/writes, retry amplification and user-to-base-response cold/warm/load/save/LIVE/recovery distributions on the named actual target. Hold relevant working set fixed while unrelated corpus/history grows; separately measure complete large affected sets. Structural checks require zero dedicated spell calls/zero deterministic-step calls and no optional Story/Commentator blocking base output. A harness without actual model calls cannot claim production user latency/model-count proof. No invented SLA or measured speed claim; unavailable real supported target remains explicit EMPIRICAL_DEFERRED under WP24 exact trigger, and does not masquerade as PASS. When actual VPS/GAME target is available, perform its eligible measurement now and route any observed defect to the owning approved task.

~~~sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_spell_offline_runtime.py DEV/TESTS/test_spell_runtime_cost_shape.py DEV/TESTS/test_spell_package_full_support.py DEV/TESTS/test_release_builder.py DEV/TESTS/test_release_game_passthrough.py DEV/TESTS/test_runtime_package_provenance.py
python3 DEV/TOOLS/run_maintenance_audit.py
python3 DEV/TOOLS/run_release_build.py --output /tmp/hdm-dev/<session>/spell-package-proof
~~~

The coordinator supplies a concrete task-owned output directory rather than executing the angle-bracket placeholder. Build uses current development mode, not a new release/tag. Do not inspect unrelated historical ZIPs or offer the proof ZIP as finished product authorization.

**Output:** W05_SPELL_OFFLINE_NATIVE_PROOF_READY; W05_SPELL_RUNTIME_COST_STRUCTURE_READY; exact qualified WP24 target evidence/disposition. W06 consumes all reports against its exact full integrated candidate.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: SP-03/06/07/16..20, execution §10, content §§3..5, WP24/current release/adoption owners.
- IMPLEMENTATION START HEAD / PRIMARY OWNER ARTIFACTS: exact fresh full supported package/native host SHA; exact accepted target/triggers/provider/capabilities.
- EXPECTED OWNERS TO CHANGE: behavior/performance/release proof and measurement tool; release builder only for proved approved member omission.
- EXPECTED CONSUMERS TO CHANGE: W06 owner/proof/version/exact-head/Senior handoff, exact release/runtime evidence consumers.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: bounded observer/report/scenario data, existing builder member inclusion; no invocation/cache/currentness bypass.
- GAME RUNTIME / PROJECTION SURFACES: exercise actual built GAME; no speculative runtime edits.
- DEV SCHEMAS / CATALOGS / MACHINE CONTRACTS: consume exact current support/mode/primitive proof; no count-only closure.
- PERSISTENCE / RECOVERY / CURRENTNESS CONSUMERS: actual cold/save/HOT/LIVE/retry/recovery with strongest accepted frontier; preserve required network barriers.
- VALIDATORS / TESTS / AUDITS: listed suites, all native/source-mode tests, maintenance/full DEV/exact build proof at proper boundaries.
- DOCUMENTATION / INSTALL / PACKAGE PROJECTIONS: qualified measurement/release receipt with target configuration and limitations, W06/cursor routing.
- CROSS-WAVE JOINS: existing W05 product/shipped completion and W06 gates unchanged; proof-after-target only.
- PROTECTED ARCHITECTURE INVARIANTS: rules offline, no deterministic model steps, bounded relevant-context growth, no shortened large-set semantics, no false latency/CI/target claim.
- ARCHITECTURE-SENSITIVE SURFACES: instrumentation parity, cache/admission/runtime provenance, optional model blocking, retry/network amplification.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: installed artifact command->native->durability->publication->receipt->cold recovery, structure and actual target observations separately.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: latency SLA/new product limit, gameplay bootstrap, tag/release publication, broad VPS/global environment changes.
- VERSION IMPACT: DEV proof/report usually NONE with owner reason; any builder semantic change classified at its own owner; no speculative engine release transition.
- SCHEMA / CATALOG / CHECKPOINT IMPACT: none beyond exact admitted report/evidence projection; preserve member identity and accepted schemas.
- MIGRATION IMPACT: NONE from observation; any discovered real defect returns to already admitted owning task/gate.
- HG-01 CONSTRAINTS AFFECTED: report disclosure remains scoped; no confidential context/credentials in telemetry.
- CURRENTNESS RE-READ SET BEFORE WRITE: exact supported package and builder, named tests, WP24 triggers/measurement law, current target/configuration, version/proof/cursor owners.

## Accepted requirement-to-task coverage

This is a planning projection of owning contracts, not proof that the mechanisms or339 entries exist. Tasks become GREEN only from actual review/publication/readback evidence.

| Canonical obligation | Required implementation/proof consumers |
|---|---|
| SP-01 full local entry/mode/support | SP00, SP16, SP17..SP26, SP29, SP30, W06.T01/T02/T06 |
| SP-02 truthful admission | SP01/SP02/SP03, SP27/SP29, P1A/P1B, W06.T04 |
| SP-03 compile/load/cache | SP02, SP29/SP30, W06.T01/T06 |
| SP-04 bounded intent/cards/context | SP02/SP28, T08, SP30/W06 |
| SP-05 preflight/source/cost | SP03/SP07/SP27/SP28, P1A, all ten content native mode suites |
| SP-06 local complete run | SP04/SP06/SP07/SP28, SP30 |
| SP-07 fixed RNG/currentness/recovery | SP04/SP05/SP06/SP15A/SP15B/SP28/SP30, W06 |
| SP-08 Health/Effect/concentration/suppression | SP08/SP09/SP28, all applicable source mode tests |
| SP-09 spatial facts/zones/relocation | SP13/SP28, SP16 and applicable content |
| SP-10 form/construction/gear/native identity | SP10/SP11/SP12/SP16/SP28 |
| SP-11 information/illusion/control | SP14/SP28, P2 current-validity consumer |
| SP-12 defense/counter/interception | SP07/SP08/SP09/SP28 and actual applicable content mode tests |
| SP-13 nested/composed/time closure | SP06/SP07/SP09/SP15B/SP28 |
| SP-14 narrow Wish recent replacement | SP15A/SP15B/SP28/SP29/SP30 |
| SP-15 exact extension/YAGNI | SP01/SP02/SP03 plus native profile consumers; SP29 equality/W06.T04 |
| SP-16 complete large sets/no semantic chunk cap | SP02/SP04/SP06/SP13/SP28/SP30 |
| SP-17 typed installation/fact/adjudication/capacity holds | SP02/SP03/SP04/SP06/SP28/SP30, T08 |
| SP-18 real response cost | SP02/SP28/SP30/T08, W06.T01/T02/T06/T07 with WP24 dispositions |
| SP-19 real native packaged proof | SP28, all ten content native proofs, SP29/SP30, W06.T01/T02/T06/T07 |
| SP-20 exact adoption/version | SP27/SP29/T08, W06.T05/T06/T07 |
| SP-21 exact stochastic state/repetition | SP01/SP05/SP28 and Teleport/Prismatic Spray/Reincarnate content modes |
| SP-22 principal/body factoring | SP11/SP12/SP28 plus exact consumer/Health/native negatives |
| SP-23 successors/permanent consequence/indexed progress | SP09/SP10/SP11/SP12/SP28, supporting content/transitive proof |
| SP-24 interception/source entitlement/Information | SP08/SP14/SP27/SP28, all applicable source modes |
| WR-01 eligibility/recent frontier/selection | SP15A/SP28, exact Procedure/BoundaryOccurrence/chronology evidence and no exposure rewrite |
| WR-02 protected minimal retention/complete affected closure | SP01/SP04/SP15A/SP28, pending refs/proved expiry/native causal enrollment |
| WR-03 closed dedicated reconciliation_state | SP01/SP15A/SP15B/SP28, strict Resolution/Continuation profiles distinct from stochastic_state |
| WR-04 accepted phases/payment/choice | SP07/SP15A/SP15B/SP28, Wish costs/stress survive original selection and later holds |
| WR-05 pure counterfactual/no authoritative replay | SP15A/SP28, corresponding old draw/new branch identity/current-owner difference proof |
| WR-06 multi-LIVE preparation/one native replacement | SP15B/SP28, actual close/final/absorb receipts, partial-close preservation and forward recovery |
| WR-07 Information/current-validity projections | SP14/SP15A/SP15B/SP28, actual P2 History/Context; future Story trigger preserved |
| WR-08 real acceptance/performance witnesses | SP15A/SP15B/SP28/SP29/SP30, level9 Wish all-mode proof and independent W06 Senior |
| SS2-01 exact creature-to-object suspension/return | SP01/SP03/SP08/SP12/SP28, level9 True Polymorph all-mode proof |
| SS2-02 exact owner propagation | preserved canonical21/21 blocks; no implementation task reopens corrected links |
| SS2-03 SRD subset/effective pool/extras | SP00/SP16/SP17/SP18/SP27/SP29/P1A/P1B, separate339/extra proof |
| PT-D1 actual nested BoundCatalogContext | SP04/SP28 real composed durability witnesses |
| PT-D2 owner-issued join forwarding | SP04/SP28 real bound-host publication witnesses |

**Authority/negative-law coverage:** every native module/proof uses exact owning source, current accepted context and complete compiler-derived consumers; no state authority from a source matrix, index/cache, fixture event, Story, caller metadata or flattened alias. Each required branch preserves exceptions, negative evidence, deferred triggers and source confidence. Retained old versions/contexts are inspected/adopted by exact existing owners; they are not deleted to simplify the proof.

**Final continuation joins:** SP29 actual supported acquisition -> P1A -> P1B; independent P0 -> P2 -> P3; P1B+P3+named spell package/native outputs -> T06 product integration -> independent Senior integration. SP30 and materialization reports feed eligible W06 proof after their targets. T07/T08/W06 retain their own accepted inputs and gates; this package authorizes continuation into them only when those inputs are actually satisfied, not by task number or a generated ZIP.
