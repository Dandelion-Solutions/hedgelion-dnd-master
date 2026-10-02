# HDM v1 Implementation Wave 05 — Machine, Bootstrap and Shared Integration

Status: **SENIOR-APPROVED / DEPENDENCY-GATED; W05.T06 REPAIRED-PLAN SENIOR GO REQUIRED; GLOBAL ACTIVATION OWNED BY `DEV/CURRENT_PROGRESS.md`**

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

### W05.T06-P0 — RuntimeHost CurrentOwnerView

**Goal:** route authority-sensitive reads through one read-only operation view
that selects the exact native source for one owner and can include accepted
unpublished HOT/SOFT state without turning HOT into another authority.

**Files:**
- Modify: `GAME/TOOLS/runtime_host.py` — infrastructure-bound HOT composition,
  internal `CurrentOwnerView`, operation-bound result carrier, and current-owner
  service wiring.
- Modify: `GAME/TOOLS/hot_store.py` — a requested-key HOT read snapshot that
  returns detached validated copies and closes its SQLite read transaction
  before any repository/LIVE read or validation requiring external evidence.
- Modify: `GAME/TOOLS/context_runtime.py` — resolve registered current families
  through the RuntimeHost-provided view rather than bypassing it with a pinned-
  campaign-only read.
- Modify: `DEV/TESTS/test_rd04_native_routing_index_hot.py`,
  `DEV/TESTS/test_runtime_host_composition.py`, and
  `DEV/TESTS/test_rd11_context_runtime.py` — HOT establishment/currentness,
  composition, and Context current-family witnesses.

**Internal interface and carrier:**

```text
NativeHotStore.read_owner_snapshot(
    campaign_id: str,
    owner_keys: tuple[tuple[str, tuple[str, ...]], ...],
) -> HotOwnerReadSnapshot

HotOwnerReadSnapshot:
    campaign_id
    requested owner documents copied from one closed SQLite read snapshot
    ephemeral local snapshot token, nonsemantic

CurrentOwnerView.read_owner(
    family_key: str,
    identity: tuple[str, ...],
    *,
    basis: _OperationBasis,
) -> CurrentOwnerRead

CurrentOwnerRead:
    campaign_id
    family_key
    identity
    status: RESOLVED | ABSENT | INCOMPATIBLE | UNAVAILABLE
    source: SELECTED_LIVE | ACCEPTED_HOT | PINNED_CAMPAIGN
    source_basis: exact owner-issued currentness/establishment evidence
    payload: validated immutable owner mapping, or a typed non-success outcome
    operation_token: RuntimeHost-issued token for this exact operation
```

`RuntimeHost`/`compose_runtime_host` bind the HOT reader only at the trusted
infrastructure composition root alongside the authenticated RepositoryPort and
selected-LIVE transport. It is not a gameplay/model/request argument. If the
current HOT reader is unavailable, the view returns typed bounded inability; it
does not assume HOT is empty and silently read a potentially stale campaign
owner.

`CurrentOwnerRead` is issued by RuntimeHost and cannot be minted by gameplay,
model/request data, a raw `OwnerDocument`, or a caller-supplied store payload.
`NativeHotStore` returns a detached, campaign-scoped snapshot for requested
owner keys only. The view validates each row against the accepted native
establishment/source-currentness contract; row presence, `source_basis` text,
generation, mtime, or local recency alone never proves currentness.

Resolution order for each identity is selected LIVE when its native route owns
the scope, otherwise compatible accepted HOT/SOFT state, otherwise the exact
pinned campaign source. A missing/incompatible selected LIVE owner is typed
bounded inability/currentness failure, never a campaign fallback. HOT is used
only after exact owner identity, campaign isolation, owner structure, accepted
establishment and source compatibility validate. The operation snapshot/token
is ephemeral and nonsemantic; it is not a campaign frontier, generation,
lease, chronology or recovery authority.

**Steps and checks:**
1. Add `CurrentOwnerViewTests` to `test_runtime_host_composition.py` for LIVE-
   first selection, compatible HOT use, pinned-campaign fallback, cross-campaign
   rejection, and rejection of an arbitrary `OwnerDocument` as current evidence.
2. Add `NativeHotOwnerSnapshotTests` to `test_rd04_native_routing_index_hot.py`
   proving requested HOT rows come from one local SQLite read basis and no
   repository/LIVE operation runs while its transaction is open.
3. Implement the Host-bound read path and detached HOT snapshot; return typed
   bounded failure when currentness/compatibility cannot be proven.
4. Cut Context's registered current PLAYER/knowledge/disclosure/world-family
   resolutions over to the same RuntimeHost operation basis; retain exact
   selected-LIVE revalidation and existing Context eligibility/allocation.
5. Run the focused RED/GREEN modules, then the P0 cross-owner and recovery
   checks named below before accepting the output.

Focused command (run sequentially from the repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd07_recovery.py DEV/TESTS/test_rd09_access_live.py
```

Expected: exit 0; all selected tests pass.

**Output:** `W05_T06_CURRENT_OWNER_VIEW_READY` — RuntimeHost, HOT and Context
use the same owner-correct operation view; no canonical state owner changes.
The `W05_T06_*_READY` labels in this section are task-local implementation
checkpoints only; they create no GAME/runtime state or serialized family.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 canonical spec §§2–4, 20; Review Stop 2 §§3,
  6; Step-5.1 §§4–8; WP-12 §§2–4; WP-14 §§3–4; WP-16 §§4–5; accepted R2.3
  Context Runtime.
- BASELINE REF OR SHA: fresh exact public HEAD read after repaired-plan Senior
  GO; record the implementation-start SHA in the execution cursor before RED.
- EXPECTED OWNERS TO CHANGE: `runtime_host.py`, `hot_store.py`,
  `context_runtime.py`; only add a new module if a concrete cohesion need is
  demonstrated and remains within this accepted view boundary.
- EXPECTED CONSUMERS TO CHANGE: RuntimeHost composition/current-read paths and
  Context current-family reads; no gameplay/model-provided capability path.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: the internal Host-bound read
  service/result and bounded HOT read-snapshot API described above.
- PROTECTED ARCHITECTURE INVARIANTS: one semantic owner; selected LIVE first;
  no pre-CAS currentness; HOT only with accepted establishment and exact source
  compatibility; coherent operation observation; no remote I/O in SQLite
  transactions; cold recovery excludes stale surviving HOT bytes; no source
  selection by local generation/order/mtime; Context retains eligibility.
- ARCHITECTURE-SENSITIVE SURFACES: Host composition inputs, currentness
  selection, campaign/LIVE/HOT source compatibility, SQLite read scope, Context
  current-family resolver, cold recovery.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD04 `NativeHotStoreTests`
  plus new CurrentOwnerView witnesses; RuntimeHost composition/current-read
  tests; RD11 current Context/readiness regressions; RD07 recovery stale-SQLite
  regressions; exact LIVE-currentness tests in RD09. Focused checks and the
  owning task's broader verification are required.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: semantic state ownership, LIVE CAS or
  transport semantics, publication/recovery protocols, History discovery,
  readiness derivation, Story, schemas/catalogs, GAME CORE/install, W05.T07/T08,
  W06, and README files.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: re-read each
  changed module and namespace owner at implementation start; bump a material
  module contract once if required. No schema, catalog, checkpoint, campaign,
  storage, migration or dual-read change is pre-authorized.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: exact current progress/cursor; this
  plan; T06-A1 spec/ruling; Step-5.1; WP-12/WP-14/WP-16; R2.3 Context;
  `runtime_host.py`, `hot_store.py`, `context_runtime.py`; RD04/RD07/RD09/RD11
  owner tests; current versioning policy and detailed owner.

### W05.T06-P1 — Production deterministic readiness

**Dependency:** `W05_T06_CURRENT_OWNER_VIEW_READY`.

**Goal:** expose local mechanical sufficiency and canonical READY_PC as distinct
deterministic RuntimeHost services over exact current Actor/build/dependency
owners and one admitted catalog/ruleset context.

**Files:**
- Create: `GAME/TOOLS/character_readiness.py` — GAME-only readiness carriers
  and deterministic service.
- Modify: `GAME/TOOLS/runtime_host.py` — fixed readiness-service composition
  using `CurrentOwnerView` and the existing admitted `BoundCatalogContext`.
- Create: `DEV/TESTS/test_character_readiness.py` — production-runtime
  behavior and negative-boundary tests.
- Inspect only: `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`,
  `GAME/CORE/CHARACTER_READINESS.md`,
  `DEV/TOOLS/validate_character_mvp_seed.py`,
  `DEV/TESTS/test_s6d_07_character_mvp_seed.py`, and the accepted catalog,
  Actor, Asset, Effect and mechanics owners.

**Internal interface and carriers:**

```text
NativeOwnerRef:
    family_key: registered native family
    identity: complete exact native identity tuple

BoundMechanicalDependencySet (transient, RuntimeHost-issued):
    actor_ref, actor_state_revision, catalog_context_fingerprint
    exact proposed mechanic/use-case identity
    finite required owner references and their validated dependency roles

ReadinessService.assess_local_sufficiency(
    actor_ref: NativeOwnerRef,
    dependency_basis: BoundMechanicalDependencySet,
) -> LocalMechanicalSufficiency

ReadinessService.assess_ready_pc(
    actor_ref: NativeOwnerRef,
) -> ReadyPcAssessment

LocalMechanicalSufficiency:
    actor_id, actor_state_revision, status, deterministic_blocker_codes,
    typed_dependency_basis

ReadyPcAssessment:
    actor_id, actor_state_revision, ready, deterministic_blocker_codes,
    catalog_generation, ruleset_set_digest_generation, ruleset_set_sha256,
    reconstructive_derivation_basis, required_production_conformance_evidence
```

Both operations resolve their data through the Host's CurrentOwnerView and one
admitted BoundCatalogContext produced by the existing catalog-runtime owner.
`NativeOwnerRef` is a route key, not authority. `BoundMechanicalDependencySet`
is internally issued for one exact mechanic/use case and bound to the same Actor
revision, Host operation and catalog context; callers cannot construct an
unbound dependency/evidence list to establish sufficiency. The assessment is
transient, contains enough owner references/derivation evidence to explain its
result, and creates no persisted ready field or duplicate authority. Derivation
follows admitted definitions, grants/choices, current Actor/Asset/Effect owners
and deterministic mechanics owners; the DEV evaluator is a conformance reference
only, never a runtime import or second rules engine.

**Steps and checks:**
1. Add `ReadinessServiceTests` to `test_character_readiness.py`, distinguishing
   sufficient dependencies for one proposed mechanic from whole-build READY_PC.
2. Add positive Fighter and Sorcerer supported-seed cases plus blocker cases for
   unresolved material choices, stale Actor revision, mismatched catalog or
   ruleset digest, missing transitive dependency, forged evidence and unsupported
   content.
3. Implement the GAME-only deterministic service over current owner results and
   exact admitted catalog evidence; do not import DEV validation tooling or
   recreate a second D&D rules engine.
4. Expose the fixed service through RuntimeHost and verify the same actor,
   current PLAYER/control relation, catalog generation and ruleset-set digest
   remain bound through the returned carrier.
5. Run `test_character_readiness.py`, S6D-07 conformance, RD03 actor/asset/effect,
   RD15 catalog-currentness, and the P1 cross-owner checks before accepting the
   output.

Focused command (run sequentially from the repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_character_readiness.py DEV/TESTS/test_s6d_07_character_mvp_seed.py DEV/TESTS/test_rd03_actor_asset_effect_continuity.py DEV/TESTS/test_rd15_catalog_runtime.py DEV/TESTS/test_runtime_host_composition.py
```

Expected: exit 0; all selected tests pass.

**Output:** `W05_T06_PRODUCTION_READINESS_READY` — local sufficiency and READY_PC
are distinct, transient, exact-basis assessments; neither mutates, publishes,
saves or declares PLAY_READY.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§5–7, 20; Review Stop 2 §6; S6D-07
  `CHARACTER_PROGRESSION_READY_PC_SEED.md`; `GAME/CORE/CHARACTER_READINESS.md`;
  accepted Actor/Asset/Effect, catalog/ruleset and durability owners.
- BASELINE REF OR SHA: fresh exact public HEAD after P0 publication/read-back;
  record exact start SHA before RED.
- EXPECTED OWNERS TO CHANGE: new `character_readiness.py`; RuntimeHost service
  composition; new runtime test module. Existing native Actor/Asset/Effect,
  catalog, access and durability owners are consumed, not replaced.
- EXPECTED CONSUMERS TO CHANGE: progressive onboarding and bounded mechanic
  precondition checks in the later held T06 product-completion task.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: transient local-sufficiency and
  READY_PC carriers and RuntimeHost service entry points only.
- PROTECTED ARCHITECTURE INVARIANTS: provisional play may precede READY_PC;
  mechanically insufficient outcomes do not guess; deterministic derivation
  binds exact Actor revision and admitted catalog/ruleset identity; open material
  initial choices block READY_PC; genuine future choices do not; no questionnaire,
  persisted ready flag, bootstrap boolean, caller evidence list or DEV runtime
  import; READY_PC alone does not perform durability or PLAY_READY transition.
- ARCHITECTURE-SENSITIVE SURFACES: build dependency closure, definition/grant/
  choice admission, Actor binding, catalog/ruleset pin, result-carrier provenance,
  existing durability/PLAY_READY boundary.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: new runtime tests; existing
  S6D-07 conformance fixture/evaluator as reference only; RD03 actor/asset/effect;
  RD15 exact catalog context; RuntimeHost current-view; onboarding consumer
  tests when P1 joins T06 product completion.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: Actor/build schema changes, mechanics
  primitives/catalog expansion, package content expansion, progression write or
  advancement publication, bootstrap product orchestration, persistent readiness
  fields, broad D&D corpus, T07/T08/W06 and Story.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify the new
  module under the current module-version owner and re-read RuntimeHost metadata;
  do not pre-authorize an existing schema/catalog/ruleset/campaign/storage bump,
  migration or dual-read by service name.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0 output/cursor; T06-A1 spec/ruling;
  S6D-07 owner and current character readiness CORE; Actor/Asset/Effect/native
  mechanics; catalog runtime and exact ruleset identity; DEV evaluator/fixture as
  conformance evidence; RuntimeHost; RD03/RD15/RD14 tests; version owners.

### W05.T06-P2 — Bounded native History discovery and enrollment

**Dependency:** `W05_T06_CURRENT_OWNER_VIEW_READY`. P2 does not depend on P1;
the execution plan remains sequential and does not authorize parallel production.

**Goal:** add only the WP19-L36 structured discovery needed for bounded ordinary
Master questions under the existing EVENT_INDEX/History owners, including
accepted unpublished HOT and currently selected LIVE events.

**Files:**
- Modify: `GAME/TOOLS/history.py` — typed bounded request/result and exact native
  candidate loading through the RuntimeHost source adapter.
- Modify: `GAME/TOOLS/runtime_host.py` — same-basis local/HOT/selected-LIVE
  discovery sources and durable EVENT_INDEX publication closure.
- Modify: `GAME/TOOLS/hot_store.py` — rebuildable event-discovery helper updated
  atomically with accepted local `runtime.semantic_event` establishment.
- Modify: `GAME/TOOLS/durability.py` / the existing accepted
  `ExecutionDurabilityJoin` and routed-event input path only as required to carry
  validated refs from accepted event input; no second event owner.
- Modify: `GAME/TOOLS/publication.py` and
  `CampaignPublicationService.publish_owner_delta` in `runtime_host.py` only as
  required to include event plus EVENT_INDEX in one existing W02 campaign
  publication closure.
- Modify: `GAME/TOOLS/live_state.py` and its existing source-pack/absorption
  producer so selected LIVE metadata is validated and exact absorbed event IDs
  plus index-safe refs join the existing campaign absorption path operations.
- Modify: `GAME/TOOLS/init_campaign.py` and
  `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml` so a new campaign begins with the
  already-required complete/upper-ordinal enrollment shape.
- Modify: existing `GAME/SCHEMA/index.schema.yaml` and
  `DEV/SCHEMAS/runtime-semantic-event-state.schema.json` only for the accepted
  EVENT_INDEX and `semantic_delta.discovery_refs` contracts they own; do not add
  a second durable index or a new serialized owner family.
- Modify tests in `DEV/TESTS/test_rd04_native_routing_index_hot.py`,
  `test_runtime_host_composition.py`, `test_rd13_story_t0_commentator.py`,
  `test_rd09_access_live.py`, `test_rd06_durability_publication.py`, and
  `test_rd14_bootstrap.py` as the named producers/consumers require.

**Internal interface and carriers:**

```text
HistoryService.discover(
    request: HistoryDiscoveryRequest,
) -> HistoryDiscoveryResult

HistoryService._discover_from_basis(
    request: HistoryDiscoveryRequest,
    *,
    basis: _OperationBasis,
) -> HistoryDiscoveryResult

HistoryDiscoveryRequest:
    selector: one admitted exact event/source, typed current-owner, session,
             recent-tail, or eligible provenance/source reference
    max_candidates: positive finite bound

NativeHistoryCandidate:
    event_id, source origin/ref/revision, source-local admission ordinal
    exact known-ID route and index-safe nomination refs only

HistoryDiscoveryResult:
    candidates: tuple[NativeHistoryCandidate, ...]
    source_basis: exact campaign / selected-LIVE / accepted-HOT basis
    status: MATCHED_BOUNDED_INTERVAL | NO_INDEXED_CANDIDATE |
            TYPED_INCOMPLETE | UNAVAILABLE
    limit_applied: bool
```

RuntimeHost internally reuses one `_OperationBasis` for this query and exact
loads. The consumer sees nominations and exact owner-issued NativeSemanticEvent
evidence, not raw index/HOT/LIVE helper rows.
`NO_INDEXED_CANDIDATE` means only that this bounded projection nominated none;
it is not proof that an event never existed or does not exist.

Accepted SemanticEvent producer joins are mandatory: (1) local accepted event
establishment updates its narrow HOT helper in the same local atomic mutation;
(2) campaign durable event publication reads the pinned EVENT_INDEX and submits
event plus index after-image through the same existing publication closure; and
(3) selected LIVE event packs carry validated event refs while existing LIVE
absorption builds the exact campaign EVENT_INDEX after-image in the same
absorption closure. A test-only helper/index mutation is not producer coverage.

`semantic_delta.discovery_refs` contains only deterministic typed native owner
family + complete identity references already admitted by accepted event input
and provenance. The EVENT_INDEX copies only the index-safe subset. No prose,
motive, T0 value, knowledge/disclosure state, raw event body or current authority
is copied. Absorption deduplicates by exact native event identity/evidence;
per-source enrollment order and event IDs do not establish global fictional
chronology.

**Steps and checks:**
1. Add `SemanticEventDiscoveryTests` to `test_rd13_story_t0_commentator.py` and
   schema/validator witnesses for one exact nominated event, finite
   multi-candidate selectors, direct-ID bypass of an invalid coarse index, and
   typed incomplete results.
2. Add `NativeHotEventDiscoveryAtomicityTests` to
   `test_rd04_native_routing_index_hot.py`,
   `CampaignEventIndexPublicationTests` to `test_runtime_host_composition.py`,
   and `LiveEventIndexAbsorptionTests` to `test_rd09_access_live.py`. Prove
   EVENT_INDEX/HOT-helper after-images are in the exact event
   establishment/publication closure; fail if only a test/helper updates.
3. Add bounded discovery composition tests for pinned campaign + accepted HOT +
   selected LIVE, and prove absent LIVE discovery produces typed inability with
   no campaign fallback.
4. Validate every ref against already accepted event input/provenance; add
   negative cases for model/prose-nominated refs, owner mismatch, duplicate IDs,
   order gaps, ID-magnitude chronology, oversized candidates and raw body/index
   leakage.
5. Align blank EVENT_INDEX template, its current schema and current source
   readers/writers; extend `BlankScaffoldCompletenessTests` in
   `test_rd14_bootstrap.py` to assert complete empty enrollment and
   upper-ordinal alignment. Classify each actual version namespace before
   deciding any bump. Do not pre-authorize a schema/generation transition or
   migration.
6. Run RD04, RuntimeHost, RD13, RD09, RD06 and RD14 focused suites plus the exact
   event-publication/absorption joins before accepting the output.

Focused command (run sequentially from the repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd04_native_routing_index_hot.py DEV/TESTS/test_runtime_host_composition.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_rd06_durability_publication.py DEV/TESTS/test_rd14_bootstrap.py
```

Expected: exit 0; all selected tests pass.

**Output:** `W05_T06_NATIVE_HISTORY_DISCOVERY_READY` — producers atomically
maintain the one derived index/helper and History returns finite exact candidates
or typed inability; no scan or absence guarantee is introduced.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§8–12, 17–20; Review Stop 2 §§5–6; WP19
  L29–L38; WP-11 index law; WP-12 local establishment; WP-13 publication;
  WP-14 rebuild/recovery; WP-16 selected LIVE/CAS/absorption; existing History,
  NativeSemanticEvent, current index and owner routes.
- BASELINE REF OR SHA: fresh exact public HEAD after P0 acceptance/read-back;
  record exact implementation-start SHA before RED.
- EXPECTED OWNERS TO CHANGE: History discovery; RuntimeHost source adapter and
  existing campaign publication closure; local HOT event helper producer;
  accepted SemanticEvent validation/routed producer; LIVE pack/absorption
  after-image producer; blank EVENT_INDEX template and its existing schemas;
  only their exact producer/consumer tests.
- EXPECTED CONSUMERS TO CHANGE: ordinary Master History nominations and later
  RetrospectiveService exact-evidence path; selected-LIVE and campaign
  absorption consumers.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: optional deterministic typed
  `semantic_delta.discovery_refs`; index-safe EVENT_INDEX ref projection;
  bounded History discovery carriers; atomic derived helper/index maintenance
  at accepted native event establishment/publication boundaries.
- PROTECTED ARCHITECTURE INVARIANTS: one durable EVENT_INDEX only; it remains
  derived and cannot prove truth/currentness/eligibility/absence; no event-body
  scan; direct exact evidence may bypass invalid coarse metadata; candidates are
  exact-loaded before use; no pre-CAS LIVE state; LIVE source movement or missing
  metadata fails boundedly; no global chronology, ID-magnitude order, duplicated
  History store, raw private data or secret-bearing index.
- ARCHITECTURE-SENSITIVE SURFACES: native event admission, event + index
  publication closure, local HOT atomicity, selected LIVE source packing/CAS,
  campaign absorption, schema/template completeness and History exact-read
  proof.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD04 HOT/index; RuntimeHost
  bounded LOCAL/LIVE reader; RD13 NativeHistory/T0; RD09 live-source and
  absorption; RD06 publication; RD14 blank scaffold; schema and producer
  validators. Include recovery rebuild/stale-helper checks.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: any second index/store; Story adapter;
  generic query language, raw-text/regex/embedding search, arbitrary predicate,
  global relevance graph or unbounded pagination; current Actor truth, access or
  disclosure; generic History retention/compaction guarantees; T07/T08/W06;
  package-wide event authority rewrite.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: current observed
  event schema is `schema_version: 1`, EVENT_INDEX is `schema_version: 1`, and
  `GAME/SCHEMA/index.schema.yaml` is schema 2. Re-read all owning rules and
  classify `runtime.semantic_event`, EVENT_INDEX, index schema, module revisions,
  campaign contract, storage, catalog and digest namespaces against the actual
  accepted delta. No bump, migration, generation or dual-read is pre-authorized
  by a service or field name.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0 output/cursor; T06-A1 spec/ruling;
  WP19 L29–L38; WP-11/WP-12/WP-13/WP-14/WP-16; current `history.py`,
  `runtime_host.py`, `hot_store.py`, `durability.py`, `publication.py`,
  `live_state.py`, `collaboration.py`, `init_campaign.py`, EVENT_INDEX template,
  event/index schemas; RD04/RD06/RD09/RD13/RD14 and versioning owners.

### W05.T06-P3 — Same-operation sealed retrospective admission

**Dependency:** `W05_T06_NATIVE_HISTORY_DISCOVERY_READY` and
`W05_T06_CURRENT_OWNER_VIEW_READY`.

**Goal:** implement the thin RuntimeHost RetrospectiveService that joins current
orientation, bounded History, exact evidence and current recipient eligibility,
then asks the existing Context Runtime to assemble the existing NARRATOR profile.

**Files:**
- Create: `GAME/TOOLS/retrospective.py` — typed request/result, use-case service,
  and RuntimeHost-issued sealed evidence carrier.
- Modify: `GAME/TOOLS/runtime_host.py` — fixed RetrospectiveService composition
  and one-operation basis binding.
- Modify: `GAME/TOOLS/context_runtime.py` — private sealed retrospective route
  that accepts only the Host-issued same-operation carrier; keep the public
  `ContextService.assemble(request, candidates)` route terminal for an unsealed
  retrospective request.
- Modify tests in `DEV/TESTS/test_rd11_context_runtime.py`,
  `DEV/TESTS/test_rd13_story_t0_commentator.py`,
  `DEV/TESTS/test_runtime_host_composition.py`, and
  `DEV/TESTS/test_rd09_access_live.py`.

**Internal interface and carrier:**

```text
RetrospectiveService.execute(
    request: RetrospectiveRequest,
) -> RetrospectiveResult

ContextService._assemble_retrospective(
    request: RetrospectiveRequest,
    evidence: RetrospectiveEvidenceSet,
    *,
    basis: _OperationBasis,
) -> ContextResult

RetrospectiveEvidenceSet (RuntimeHost-issued; no public constructor):
    campaign_id, recipient_player_id, selected_controlled_pc_id | None
    operation_token, exact source/currentness basis
    eligible field projections bound to exact NativeSemanticEvent/native sources

RetrospectiveRequest:
    one typed nomination from the accepted Interpreter/owner path
    finite max_candidates; fixed ordinary Master / Narrator purpose

RetrospectiveResult:
    typed Context outcome and the existing bounded Narrator projection only
```

`RetrospectiveRequest` carries only the bounded typed nomination/purpose needed
for this request; it cannot carry raw event bodies, caller-selected services,
currentness claims, Story IDs as authority, a seal, or caller-authored eligibility
lists. The service resolves current active PLAYER and selected PC control from
the current owners, calls `CurrentOwnerView` and P2 History on the same
`_OperationBasis`, exact-loads shortlisted native evidence, obtains current
knowledge/disclosure/access, and issues an unforgeable evidence set. The private
Context route revalidates recipient/control, eligibility and exact source binding
before projecting only eligible fields into `role=NARRATOR`,
`profile=profile.narration`, `purpose=narrate`, `retrospective=true`.

The seal proves acquisition/binding only; it never grants permission. An exact
historical field without current eligibility is omitted/fails closed. Missing
T0 remains insufficient or inference, never T1 reconstruction as established
history. Opaque EVENT_INDEX/HOT helper/private event data never enters a public
tool or model payload. Story is absent from this baseline route.

**Steps and checks:**
1. Add `SealedRetrospectiveContextTests` to `test_rd11_context_runtime.py` and
   `RetrospectiveEvidenceBindingTests` to
   `test_rd13_story_t0_commentator.py`. Prove direct `ContextService.assemble` with
   `retrospective=True`, caller candidates, raw event payload, forged seal,
   cross-host seal or stale operation basis remains terminal and performs no
   unauthorized History read.
2. Add positive use-case tests for active PLAYER with PUBLIC-only eligibility,
   exact current PLAYER disclosure, and at most one selected currently
   controlled PC's exact-current `epistemic.known`; add negative multiple-PC,
   no-PLAYER, revoked-control, hidden-field, source-movement and unsupported
   content cases.
3. Implement `RetrospectiveService.execute` using P0/P2 under one basis and issue
   only a Host-bound sealed evidence carrier after exact history and current
   eligibility validate.
4. Implement the private Context route and field-level eligible projection;
   retain ordinary Context policy/allocation, existing Narrator, and the direct
   unsealed failure behavior.
5. Prove Story absent/stale succeeds for supported native cases; direct known
   IDs can work when coarse discovery metadata is invalid; invalid metadata never
   triggers a body scan or an absence claim; bounds do not promise arbitrary
   complete history or exact quotes after lawful compaction.
6. Run RD11/RD13/RD09/RuntimeHost focused suites, including T0-vs-T1 and same-
   operation/source-binding witnesses, before accepting the output.

Focused command (run sequentially from the repository root):

```sh
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -m pytest -q DEV/TESTS/test_rd11_context_runtime.py DEV/TESTS/test_rd13_story_t0_commentator.py DEV/TESTS/test_rd09_access_live.py DEV/TESTS/test_runtime_host_composition.py
```

Expected: exit 0; all selected tests pass.

**Output:** `W05_T06_SEALED_RETROSPECTIVE_READY` — ordinary Master retrospective
is a bounded gameplay use case with same-operation evidence acquisition and
current recipient-safe Context admission.

**Implementation Impact Envelope:**
- SPEC / APPROVED DESIGN: T06-A1 §§9–18, 20; Review Stop 2 §§5–6; WP19
  L20–L23 and L29–L38; accepted R2.3 Context, Step-4 information/role and
  access/knowledge/disclosure owners; PO-012 only for its separately preserved
  Commentator boundary.
- BASELINE REF OR SHA: fresh exact public HEAD after P2 acceptance/read-back;
  record exact implementation-start SHA before RED.
- EXPECTED OWNERS TO CHANGE: new `retrospective.py`; RuntimeHost service; private
  Context sealed admission route; bounded T06-specific tests. Existing PLAYER,
  control, knowledge/disclosure, History and NativeSemanticEvent owners remain
  semantic authorities.
- EXPECTED CONSUMERS TO CHANGE: ordinary active-player Master retrospective
  routing and NARRATOR context assembly; no Commentator role transition.
- ALLOWED INTERFACES / CONTRACTS TO CHANGE: typed bounded RetrospectiveRequest /
  Result; non-public Host-issued same-operation `RetrospectiveEvidenceSet`; the
  internal Context entry point that consumes it.
- PROTECTED ARCHITECTURE INVARIANTS: current view for NOW questions; exact native
  evidence for material historical claims; current active PLAYER/control and
  field-level eligibility; same-operation seal; no raw caller candidate
  authority; no Story/current truth authority; no T0-to-T1 substitution; no
  hidden/private routing bytes in public output; no additional serial LLM phase
  or publication edge.
- ARCHITECTURE-SENSITIVE SURFACES: active principal/PLAYER reload; selected PC
  control; disclosure and knowledge validation; exact event/source currentness;
  Host token/seal issuance; Context role/purpose/profile binding.
- EXPECTED CROSS-MODULE / INTEGRATION VERIFICATION: RD11 Context and direct
  unsealed terminal tests; RD13 exact History/T0 and Story-separation tests;
  RD09 principal/access/control tests; RuntimeHost same-basis/currentness tests;
  end-to-end P2 History + P0 owner-view joins.
- KNOWN OUT-OF-SCOPE OWNERS / SURFACES: Commentator/CLS, Story adapter or Story
  dependency, new LLM role/model call, generic retrieval/search, new
  authorization/knowledge/disclosure authority, persistent retrospective
  records, T07/T08/W06, and any unrelated Context profiles.
- VERSION / SCHEMA / CATALOG / CHECKPOINT / MIGRATION IMPACT: classify actual
  changed `runtime_host.py`, `context_runtime.py`, and new module version status
  at fresh start; no persistent schema, catalog, checkpoint, campaign/storage
  generation, migration or dual-read is pre-authorized.
- HG-01 CONSTRAINTS AFFECTED: none expected; record the check.
- CURRENTNESS RE-READ SET BEFORE WRITE: P0/P2 outputs/cursor; T06-A1
  spec/ruling; WP19/Context/Step-4/access/information/knowledge/disclosure
  owners; current `runtime_host.py`, `history.py`, `context_runtime.py`,
  `access_control.py`, `collaboration.py`, `story.py` only for separation,
  and existing RD09/RD11/RD13/Host tests; versioning owners.

### T06-A1 accepted-law coverage and critic propagation

This table routes each accepted law to its implementation task; the canonical
spec and Senior ruling remain semantic authorities.

| Canonical law | Planned discharge |
|---|---|
| T06A1-1 operation-scoped CurrentOwnerView | P0 |
| T06A1-2 coherent ephemeral HOT observation; no global frontier | P0 |
| T06A1-3 Context current-family cutover | P0 |
| T06A1-4 deterministic readiness; local sufficiency / READY_PC / PLAY_READY distinct | P1 and held T06 product completion |
| T06A1-5 exact Actor/control/dependency/catalog/ruleset basis and reconstructive READY_PC assessment | P1 |
| T06A1-6 readiness re-evaluated after accepted change and correctness-relevant resume/rejoin | P1 and held T06 product completion |
| T06A1-7 ordinary Master gameplay with existing Interpreter/Narrator; no MASTER role | P3 and held T06 product completion |
| T06A1-8 minimum typed discovery refs under the one EVENT_INDEX owner | P2 |
| T06A1-9 derived index, exact evidence, complete/upper-ordinal enrollment alignment | P2 |
| T06A1-10 finite registered selectors; no generic query or campaign scan | P2 |
| T06A1-11 accepted unpublished HOT and selected LIVE discovery; typed inability on missing LIVE route | P2 |
| T06A1-12 NOW questions resolve through current owners; no T0 restoration | P0 and P3 |
| T06A1-13 thin use-case orchestration only | P3 |
| T06A1-14 same-operation sealed acquisition plus independent current eligibility; private bytes stay internal | P3 |
| T06A1-15 retained T0 motive evidence only; no T1 reconstruction as history | P3 |
| T06A1-16 Story Master adapter remains dormant until one of the two accepted measured-cost/product-navigation triggers | No baseline task; held out of scope |
| T06A1-17 typed bounded failure/recovery for missing readiness, invalid index, LIVE movement, stale sources, lost HOT, inactive PLAYER/control, missing T0 or unavailable Story | P0–P3 and held T06 product completion |
| T06A1-18 no extra serial LLM call or publication boundary | P3 and held T06 product completion |

Senior critic propagation is also discharged item-by-item: H06-01 by P2's
atomic HOT helper and query composition; H06-02 by P2's selected-LIVE source or
typed inability; H06-03 by P0's coherent detached HOT observation; H06-04 by
P2/P3's index-safe metadata and recipient-safe field projection; H06-05 by P3's
unforgeable same-operation seal; H06-06 by P2's blank-template/writer/schema
alignment; H06-07 by the explicit dormant Story disposition above.

## W05.T06 — Onboarding, join/rejoin, retrospective and save/exit product paths

This is the held product-completion task after P1 and P3 are accepted (P0/P2
are transitive prerequisites). T06-S1/S2 below in the execution cursor remain
accepted; do not replay or reopen their implementation. The T06 product task
adds only the progressive-readiness and ordinary Master retrospective
composition, then proves the whole T06 product output.

Hard inputs: accepted `W05_T06_CURRENT_OWNER_VIEW_READY`,
`W05_T06_PRODUCTION_READINESS_READY`,
`W05_T06_NATIVE_HISTORY_DISCOVERY_READY`, and
`W05_T06_SEALED_RETROSPECTIVE_READY`; accepted
`W04_RUNTIME_HOST_COMPOSITION_READY`, `W04_RUNTIME_HOST_IO_EXTENSIONS_READY`,
T07E exact-serialized-byte measurement, PO-012, and the exact completed owner
checkpoints consumed by each product path. T06-S1/S2 remain accepted without
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
manifest: `progress_onboarding(...)` obtains local-sufficiency/READY_PC results
from `RuntimeHost.readiness`; `route_active_player_retrospective(...)` delegates
to `RuntimeHost.retrospective.execute(...)`. The adapters do not accept a
readiness boolean, owner service, raw History payload or evidence seal from
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
