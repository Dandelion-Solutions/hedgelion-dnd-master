# HDM v1 Implementation Wave 05 — Machine, Bootstrap and Shared Integration

Status: **SENIOR-APPROVED / DEPENDENCY-GATED; W05.T06 REPAIRED PLAN GO / P0 AUTHORIZED; GLOBAL ACTIVATION OWNED BY `DEV/CURRENT_PROGRESS.md`**

Goal: integrate the completed owner contracts into the single strict 17-world/17-runtime machine, complete bootstrap and product paths, and perform every shared physical write exactly once with the approved version cutovers.

Use `implementation-plan-execution-contract.md`. Fresh-read every shared file immediately before its final writer; integrate all required GREEN deltas in one checkpoint.

## Entry and exit

Entry requires every owner/join checkpoint named as an input below. Exit requires exact family census, strict schemas/catalogs, complete blank-scaffold/bootstrap paths, current shipped instructions and all retained schema/CORE version targets realized at one coherent HEAD.

W05.T06 has an additional task-specific gate: the accepted T06-A1 architecture
does not authorize its P0–P3 or held product-completion production tasks. Those
tasks remain held until this stable plan and its Impact Envelopes receive Senior
plan GO. T06-S1/S2 remain accepted and are not repeated.

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
- Inspect/consume: native owner producers such as
  `GAME/TOOLS/actor_continuity.py`; do not move their semantic validation into
  HOT. A P0 acceptance witness uses a real owner-validated Actor after-image,
  not a fabricated raw OwnerDocument.
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

P0 proves the establishment plumbing with an existing real native producer:
apply one accepted NPC Actor continuity delta through
`actor_continuity.apply_actor_delta`, establish that validated after-image in
HOT through the trusted infrastructure path, and read it through Context before
SAVE. A structurally equivalent row inserted only through an untrusted/test raw
path is not an admitted CurrentOwnerView source. P1A and P2 later add the
T06-specific PC-character and SemanticEvent producer joins to the same
establishment boundary; P0 does not invent their semantics.

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
1. RED: selected product host lacks the trusted HOT capability; Context after a
   real accepted local Actor change still sees pinned Git; forged/surviving raw
   rows and cross-campaign rows must fail.
2. RED: dependency closure expands between Actor and a second owner while the
   first HOT row changes; mixed observation must be rejected.
3. Implement trusted HOT composition/admission and operation read sessions;
   thread the capability through `compose_selected_runtime_host`.
4. Cut Context current-family resolution to the view while preserving existing
   eligibility and selected-LIVE revalidation.
5. GREEN: real owner-produced local after-image is visible before SAVE; forged
   raw row is not; cold recovery does not resurrect stale dirty state; expansion
   either returns one compatible union or typed revalidation failure.
6. Run the focused and cross-owner checks below, then Version Impact Gate,
   task review, full clean DEV/maintenance verification and remote read-back.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd14_bootstrap.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py
```

**Output:** `W05_T06_CURRENT_OWNER_VIEW_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§2–4, 20; Review Stop 2; Step-5.1;
  WP-12/WP-14/WP-16; R2.3; current native Actor/PLAYER/information owners.
- BASELINE REF OR SHA: fresh exact public HEAD after final repaired-plan Senior
  GO; record implementation-start SHA before RED.
- EXPECTED OWNERS TO CHANGE: RuntimeHost/current-owner/HOT infrastructure,
  Context current reads and selected-product bootstrap composition; only the
  minimum owner-producer adapter needed for the real P0 establishment witness.
- EXPECTED CONSUMERS TO CHANGE: RuntimeHost fixed service composition,
  Context current-family resolution and bootstrap's selected gameplay host.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: trusted infrastructure HOT port,
  process-local admitted-establishment bookkeeping, operation-scoped
  read-session/results and the trusted compose-selected-host argument. No
  public gameplay/model mutation/service-injection capability.
- PROTECTED ARCHITECTURE INVARIANTS: one semantic owner; LIVE-first exact
  currentness; no pre-CAS state; HOT only after native-owner validation + WP12
  establishment/adoption; no remote I/O in SQLite transactions; no stale
  restart resurrection; dynamic closure cannot mix snapshots; Context retains
  information/access eligibility.
- ARCHITECTURE-SENSITIVE SURFACES: RuntimeHost composition; SQLite transaction
  scope; current-source precedence; selected LIVE routing; cold recovery;
  Context source eligibility; same-campaign namespace isolation.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD03 owner-produced Actor
  after-image witness; RD04 HOT snapshot/admission; RuntimeHost composition;
  RD11 Context; RD14 selected product host; RD07 recovery; RD09 LIVE.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: character build semantics (P1A),
  readiness derivation (P1B), History discovery (P2), Story, persistent
  campaign schema/catalog expansion, migration, publication timing.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify actual
  changed GAME modules. No persistent campaign schema/catalog/generation,
  checkpoint or migration change is pre-authorized.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: exact current progress/cursor; stable
  plan/index; T06-A1/Review Stop 2; Step-5.1; WP12/14/16; R2.3;
  RuntimeHost/HOT/Context/bootstrap/actor-continuity code; RD03/04/07/09/11/14;
  current versioning policy/owner.

### W05.T06-P1A — Production character materialization resolver

**Dependency:** `W05_T06_CURRENT_OWNER_VIEW_READY`.

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
- Modify the current native Actor envelope contracts
  `GAME/SCHEMA/actor.schema.yaml` and `DEV/SCHEMAS/world-record.schema.json`
  only as needed to represent the already-owned Actor `state_revision`
  required by Actor Continuity and S6D-07. Do not invent a second revision field
  inside `world-actor-state`.
- Create: `DEV/TESTS/test_character_progression.py`; extend RuntimeHost/RD14
  composition and native Actor schema/continuity tests.
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
trusted HOT establishment boundary in one local transaction. It does not SAVE,
publish, declare READY_PC or create a new lifecycle state. Unsupported content
is absent/nonselectable.

The Host-bound catalog context is an already admitted `BoundCatalogContext`
from `catalog_runtime.bind_catalog_context`; RuntimeHost never constructs an
ambient default. Its catalog generation/ruleset digest/fingerprint and relevant
campaign definition frontier are revalidated for each operation. Stale or
foreign context produces typed rebind/currentness failure.

**Acceptance:** positive Human/Criminal Fighter and Sorcerer initial paths,
delegated deterministic defaults, one unresolved material choice, explicit
player override, same Actor ID/state-revision advance, exact current PLAYER
control, unsupported content, forged selection, wrong-host/stale catalog and
HOT before-SAVE visibility. No questionnaire behavior is implemented in this
deterministic service.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_character_progression.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd14_bootstrap.py
```

**Output:** `W05_T06_CHARACTER_MATERIALIZATION_READY`.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: S6D-07 Character Progression/READY_PC Seed,
  DIEGETIC_ONBOARDING, T06-A1 current-owner laws, Review Stop 2.
- BASELINE REF OR SHA: accepted P0 output SHA after fresh remote read-back.
- EXPECTED OWNERS TO CHANGE: new production character-progression resolver;
  RuntimeHost/catalog composition; bootstrap trusted catalog composition;
  P1A-specific HOT establishment producer join.
- EXPECTED CONSUMERS TO CHANGE: progressive onboarding product path later in
  T06; P1B readiness; RuntimeHost composition tests.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: typed materialization request/result,
  fixed RuntimeHost character-progression service and trusted Host-bound
  BoundCatalogContext. No raw prose/owner-after-image/catalog service injection.
- PROTECTED ARCHITECTURE INVARIANTS: same PC Actor ID; player-owned choices and
  accepted selection-basis precedence; deterministic grants/defaults only;
  exact current PLAYER control; exact catalog/ruleset context; unsupported
  content absent/nonselectable; one atomic local HOT establishment; no READY_PC,
  SAVE or PLAY_READY side effect.
- ARCHITECTURE-SENSITIVE SURFACES: Actor/Asset native after-images, catalog
  context/current definition frontier, player agency, HOT atomicity, S6D package
  breadth and same-Actor promotion.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: new character progression
  suite; S6D-07 conformance; RD03 Actor/Asset/Effect; RD15 catalog; RuntimeHost
  composition; RD14 bootstrap; P0 HOT witnesses.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: new D&D content, generic concept NLP,
  Activity execution/RNG, readiness verdict (P1B), History/Story, publication,
  migration, new mechanics primitive/selector/accessor.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: run exact Version
  Impact Gate on new/changed GAME modules and the Actor envelope schema
  alignment. Current code/tests already require Actor `state_revision` while
  installed Actor/world-record envelopes do not represent it; implementation
  must make those machine contracts agree. Do not preselect the exact schema/
  campaign-contract transition or migration disposition before rereading the
  current pre-release/version owner.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0 output/cursor; S6D-07,
  DIEGETIC_ONBOARDING/CHARACTER_READINESS; Actor/Asset/Effect/health owners;
  catalog_runtime/ruleset_package/MechanicalContext; current package seed and
  capability file; RuntimeHost/bootstrap; relevant tests and version owner.

### W05.T06-P1B — Production deterministic readiness

**Dependencies:** `W05_T06_CURRENT_OWNER_VIEW_READY`,
`W05_T06_CHARACTER_MATERIALIZATION_READY`.

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
P1B semantically; execution remains one production task at a time.

**Goal:** realize only WP19-L36 bounded SemanticEvent discovery using the
existing EVENT_INDEX artifact plus accepted unpublished HOT and selected LIVE
event evidence.

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

Fresh-read and integrate owner deltas into each material module exactly once:

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
| AI_REASONING | 1.0.4 | typed role/context/protected result + campaign-bound RuntimeHost Context composition + PO-011 `ResolvedResponseLanguage` / internal-vs-visible presentation law |
| LIVE_SCENE | 1.0.4 | source-native LIVE/currentness/state + selected-LIVE evt source-domain reader wiring |
| MULTIPLAYER | 1.0.8 | principal route + LIVE + collaboration/access reconciliation |
| CAMPAIGN_SETUP | 1.0.4 | identity/scaffold/onboarding + PO-011 current player-language Master/setup presentation |
| SESSION | 1.0.2 | exact session/campaign/LIVE/PLAYER handoff + PO-011 human-visible session/status language projection |
| PLAY_POLICY | 1.0.5 | exact accepted adjudication/access policy + PO-011 rule that optional language-policy absence never licenses another visible response language |
| CORE_INDEX | 1.0.2 | current module routing/versions |
| ADJUDICATION | 1.0.3 | bound catalog and accepted policy basis |

Shared physical checkpoints:

- integrate `GAME/INSTALL/README.md`, `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` and `GAME/INSTALL/00_DND_BOOTSTRAP.md` at `RD14_INSTALL_BOOTSTRAP_FINAL_INTEGRATION_READY`, projecting PO-011 so player-visible bootstrap/setup/failure wording follows the current response language while technical internals remain separate;
- integrate `GAME/CORE/BOOTSTRAP_RUNTIME.md` at `CORE_BOOTSTRAP_RUNTIME_FINAL_INTEGRATION_READY`, including the final deployment wiring law: authenticated Step-5.6 RepositoryPort + campaign publication transport + Step-5.8 LIVE/source-domain adapters compose the Wave-04 RuntimeHost after campaign selection, while no gameplay/model surface can inject those capabilities; the publication transport must implement T07E's exact `measure_path_operations(...)` contract with the same serializer as `create_tree`, and absence must remain fail-closed;
- integrate `GAME/CORE/STORAGE.md` at `CORE_STORAGE_FINAL_INTEGRATION_READY`;
- integrate `GAME/CORE/MULTIPLAYER.md` at `CORE_MULTIPLAYER_FINAL_INTEGRATION_READY`;
- integrate all other material CORE modules once with their listed owner inputs.

TDD and verification:

- use `InstallBootstrapSharedWriterTests` (`STATIC_AUDIT`) and `BoundedCampaignDiscoveryTests` (`FOCUSED_BEHAVIOR`);
- complete `CoreFrameworkModuleVersionCutoverTests` and the retained version suite;
- prove final install bytes contain no exhaustive all-campaign card loop, login-only authorization, generic PLAYER_INDEX authorization or stale v0.8 compatibility path; also prove no shipped ordinary Master path uses English, Russian or another fallback solely because an optional language policy/local phrase asset is absent, technical diagnostics remain a separate recipient-safe surface, PO-012 retrospective/Commentator routing never unions multiple controlled-PC knowledge or trusts caller Story visibility, and the final campaign-publication transport exposes exact create-tree-parity size measurement rather than an estimate.

After all module/schema/test paths are final, integrate their routes into `DEV/PROJECT_MAP.md` and all current/stale/schema/catalog/version/package assertions into `DEV/TOOLS/audit_engine.py`. At this same final control-plane cutover: Retire `pc.schema.yaml`, `npc.schema.yaml` and `item.schema.yaml` only after `audit_engine.py` and every remaining legacy-schema consumer are reconciled; retire any remaining retired-faction contract/reference at the same boundary. Retired contracts receive no terminal version bump. Run the actual maintenance entry point after these edits; do not leave per-task partial writers.

Output checkpoints: `W05_SHIPPED_INTEGRATION_READY`, `PROJECT_MAP_FINAL_INTEGRATION_READY` and `MAINTENANCE_AUDIT_FINAL_INTEGRATION_READY`.

## Wave 05 completion evidence

Record the exact 17+17 census, actual shared-file bytes, every schema/module version, manifest field absence, blank-scaffold completeness, bounded discovery behavior and shipped consumer routing at the published HEAD. No owner-local delta may remain waiting outside the final physical writers when this wave closes.
