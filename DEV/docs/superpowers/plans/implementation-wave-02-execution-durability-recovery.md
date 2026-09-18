# HDM v1 Implementation Wave 02 — Execution, Durability and Recovery

Status: **COMPLETE / SENIOR INTEGRATION PASS**

Goal: turn accepted typed interpretation into deterministic commands and mechanical events, publish the complete durability promise, and recover the same accepted state without replay, reroll or identity reallocation.

Use `implementation-plan-execution-contract.md`. Every task consumes only named GREEN checkpoints; independent tasks remain parallel where their inputs allow.

## Entry and exit

Entry requires the exact Wave-01 checkpoints named below. Exit requires accepted execution, publication and recovery to agree on identities, fixed RNG, catalog context, adjudication basis, operational roots and currentness.

Minimum wave impact envelope:

- owners: interpreter result, runtime command, procedure/continuation, mechanical event, durability promise, publication outcome, checkpoint, maintenance audit and recovery selectors;
- consumers: LIVE, temporal, collaboration, Story, bootstrap and final 17+17 integration;
- protected invariants: accepted mechanics execute once, fixed RNG never rerolls, recovery never guesses, and no repository-wide transaction/journal becomes authority;
- shared files: emit bounded deltas for `GAME/CORE/STORAGE.md`, `GAME/TEMPLATE/STORAGE_README.md` and related final writers; Wave 05 integrates their bytes.

## Baseline file-action and interface manifest

Fresh-read and reclassify before write. The baseline implementation set is:

| Lane | Direct action paths | Shared/final paths |
|---|---|---|
| execution | `NEW_CREATE GAME/TOOLS/runtime_execution.py`, `GAME/TOOLS/mechanics.py`, `DEV/TESTS/test_rd05_runtime_execution.py`; reconcile the existing `DEV/SCHEMAS/runtime-command-state.schema.json`, `runtime-continuation-state.schema.json`, `runtime-intent-plan-state.schema.json`, `runtime-interaction-state.schema.json`, `runtime-procedure-state.schema.json`, `combat-minimal-procedure-state.schema.json`, `runtime-resolution-state.schema.json`, `runtime-mechanical-event-state.schema.json`, `runtime-resolution-trace-state.schema.json`, `execution-segment.schema.json`, `resolution-receipt.schema.json` | `GAME/CORE/RANDOMNESS.md` consumes W01 currentness and integrates at W05 |
| durability/publication | `NEW_CREATE GAME/TOOLS/durability.py`, `GAME/TOOLS/publication.py`, `DEV/SCHEMAS/durability-promise-result.schema.json`, `campaign-publication-attempt.schema.json`, `DEV/TESTS/test_rd06_durability_publication.py` | `GAME/SCHEMA/session.schema.yaml`, `GAME/TEMPLATE/STORAGE_README.md`, save/persistence CORE modules integrate at W05 |
| recovery/maintenance | `NEW_CREATE GAME/TOOLS/recovery.py`, `DEV/SCHEMAS/recovery-result.schema.json`, `runtime-maintenance-audit-state.schema.json`, `DEV/TESTS/test_rd07_recovery.py`; replace `GAME/SCHEMA/checkpoint.schema.yaml`; modify `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` | session schema, `GAME/CORE/STORAGE.md`, schema/storage READMEs integrate at W05 |
| operational roots | `NEW_CREATE GAME/TOOLS/recovery_roots.py`, `DEV/SCHEMAS/operational-root-routing.schema.json`; create/replace `GAME/SCHEMA/operational_root_routing.schema.yaml` and blank `GAME/CAMPAIGN/STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml` through the scaffold owner; modify the current `runtime.procedure` schema/producer/validator only as required to materialize its accepted owner-native `ACTIVE|TERMINAL` lifecycle | storage documentation and generated scaffold integrate at W05 |
| adjudication/catalog basis | `NEW_CREATE GAME/TOOLS/policy_basis.py` (or the current owner-equivalent path after fresh resolution) as the narrow runtime `PolicyBasisResolver` adapter; modify `GAME/TOOLS/runtime_execution.py` and exact accepted-basis schemas only as required; extend the named RD05/RD07 owner tests | `GAME/CORE/ADJUDICATION.md` and `PLAY_POLICY.md` integrate at W05 |

Required callable boundary:

```text
accept_command(...) / validate_execution_proposal(...) / resolve_mechanic(...)
execute_segment(...) / resume_accepted_execution(...) / close_resolution(...)
evaluate_durability(...) / freeze_save_promise(...) / complete_save_promise(...)
freeze_campaign_publication_attempt(...) / build_connector_git_plan(...)
classify_ref_transition(...) / reconcile_indeterminate_publication(...)
recover_current_runtime(...) / select_current_native_sources(...)
hydrate_required_closure(...) / validate_recovered_basis(...)
export_checkpoint_diagnostics(...) / reset_last_checkpoint_reference(...)
validate_repair_candidate(...) / promote_historical_repair(...) / record_maintenance_audit(...)
derive_operational_root_delta(...) / validate_operational_root_delta(...)
enumerate_operational_root_page(...) / hydrate_operational_roots(...)
```

The catalog basis is carried by root/child Resolution and Continuation exactly; generic dependency-frontier refs cannot substitute for it. Unsettled accepted execution protects the bounded owner-local definition evidence required to reconstruct that basis, without a global refcount, snapshot or all-history scan.

## W02.T01 — Typed interpretation and catalog-backed command acceptance

Hard inputs: `W01_CATALOG_CONTEXT_READY`, the current interpreter owner and the exact accepted-input specification.

Implement the hard chain:

```text
typed InterpreterResult
-> exact BoundCatalogContext validation
-> catalog candidate validation or typed gap
-> catalog-backed RuntimeCommand acceptance
```

The accepted command records the exact interpreter input/result identity, catalog context basis and validated candidate identity. A missing, stale, incompatible or ambiguous basis rejects before mechanics. A gap result is evidence, not an implicitly accepted fallback.

TDD and verification:

- extend `DEV/TESTS/test_rd05_runtime_execution.py` with `AcceptedIdentityTests`, `ProposalValidationTests` and `AcceptedExecutionCatalogBasisTests`;
- turn `CatalogBindingIntegrationTests`, `CatalogBindingInstructionCutoverTests` and `CatalogBackedAcceptanceIntegrationTests` GREEN in `DEV/TESTS/test_rd15_catalog_runtime.py`;
- prove rejection when a catalog is selected after acceptance or a context/candidate differs from the pinned basis.

Output checkpoint: `W02_CATALOG_BACKED_COMMAND_READY`.

## W02.T02 — Deterministic execution, fixed RNG and event identity

Hard input: `W02_CATALOG_BACKED_COMMAND_READY`; owner inputs from `W01_ACTOR_ASSET_EFFECT_READY`, `W01_TEMPORAL_OWNER_READY` and `W01_ROLE_CONTRACT_READY` apply where the command touches them.

Implement:

- fixed RNG basis captured before accepted mechanical resolution and retained through retries;
- deterministic procedure and continuation temporal state;
- exactly-once accepted input identity;
- `MechanicalEvent` identity `(segment_id, event_ordinal)`;
- event ordinal allocated within the accepted execution segment, outside the general campaign entity allocator;
- typed downstream execution evidence and an atomic owner-local mutation boundary.

Retrying, publishing or recovering the same accepted input reuses its RNG and identities. A conflicting replay fails closed; it never creates another accepted result.

TDD and verification:

- use `DEV/TESTS/test_rd05_runtime_execution.py`;
- retain `FixedRngTests`, `ProcedureTemporalStateTests`, `ContinuationTemporalStateTests`, `LifecycleEvidenceTests`, `ExecutionAtomicityTests` and `DownstreamExecutionEvidenceTests`;
- include duplicate delivery, interrupted acknowledgement, conflicting payload and recovery replay negatives.

Output checkpoint: `W02_DETERMINISTIC_EXECUTION_READY`.

## W02.T03 — Exact accepted adjudication basis

Hard input: the current adjudication/policy owners plus `W02_CATALOG_BACKED_COMMAND_READY`.

Implement the accepted bounded `PolicyBasisResolver` realization from `DEV/ARCHITECTURE/HOUSE_RULES_MECHANICAL_BOUNDARY.md`. It is a read-side verifier/adapter over exact pinned campaign reads plus existing House-Rules/Access/currentness owners; it is not a new policy/currentness/authorization owner.

The resolver must start from the selected campaign and exact pinned authoritative revision H, use the supported RepositoryPort-equivalent exact-read capability, and validate the sidecar + normative source + policy identity/lifecycle/adoption/applicability against trustworthy principal/creator/PLAYER evidence. When mechanically material, `realization_refs` are checked against the already selected compatible `BoundCatalogContext`.

Bind the complete accepted parameter/fact basis and unique sorted `policy_id@H` refs into the command/result identity. Raw caller booleans, caller-selected paths/revisions, the DEV conformance validator, static JSON round-trip and current/latest policy at retry time are insufficient. The resolver result is ephemeral; do not add a persisted proof registry or policy epoch.

The accepted basis must support:

- exact source identity/version/currentness;
- all nine source-derived parameter/fact consumer edges defined by the accepted adjudication owner;
- deterministic idempotency for the complete accepted input;
- historical reuse after newer policy is published, without revalidating accepted work against later grants/policy revisions;
- typed rejection for missing, stale, inconsistent, unauthorized, inapplicable or unsupported policy sources;
- explicit negative coverage proving that forged `authority_validated`/`applicable` booleans, caller-selected source paths/revisions and direct use of the DEV validator cannot create an accepted policy basis.

TDD and verification:

- use `ExactPolicyBasisResolutionTests` in `DEV/TESTS/test_rd07_recovery.py` for the bounded resolver;
- use `AcceptedAdjudicationBasisTests` in `DEV/TESTS/test_rd05_runtime_execution.py` for acceptance/idempotency;
- publication and cold-recovery halves close in W02.T05 and W02.T06.

Output checkpoint: `W02_ACCEPTED_ADJUDICATION_BASIS_READY`.

## W02.T04 — Operational-root enrollment and routing contract

Hard inputs: `W01_NATIVE_ROUTING_READY` and accepted command/procedure semantics.

Define the native active-root set for independently recoverable work:

- accepted commands that still require publication/recovery;
- procedures with remaining accepted work;
- promised unresolved inputs that must survive interruption.

Implement typed eligibility and idempotent enrollment/removal under the accepted Step-5.2 machine-realization ruling:

- materialize explicit owner-native `runtime.procedure.lifecycle = ACTIVE|TERMINAL` in the current Procedure schema/producer/validator;
- derive Procedure root eligibility only from validated Procedure-native lifecycle evidence;
- derive RuntimeCommand root eligibility from its native accepted/settled disposition plus unfinished mandatory closure;
- define the unresolved Interaction/IntentPlan eligibility/derivation interface, but create such a root only when the later durability/handoff owner supplies an accepted promise for that semantic point;
- derive a bounded typed operational-root delta from exact owner identity/state; never accept a caller-built before/after root set as lifecycle proof;
- prepare terminal removal as derivative evidence only. W02.T05 owns the publication closure that atomically/coherently applies native owner transition plus required root-membership mutation.

The root set is active-only, campaign-scoped, completeness-protected and bounded. It is not a publication journal, durability frontier, lifecycle owner or global pending queue. Temporal roots remain under their temporal owner and join through explicit routing, rather than being silently absorbed here.

TDD and verification:

- use `OperationalRootEnrollmentTests` in `DEV/TESTS/test_rd05_runtime_execution.py`;
- prepare `OperationalRootRoutingContractTests` in `DEV/TESTS/test_rd07_recovery.py` in the owning task; do not publish it RED before W02.T06;
- prove idempotent enrollment, exact owner-kind+identity matching, rejection of same-kind/different-owner carrier substitution, rejection of forged caller-built removal, Procedure ACTIVE/TERMINAL derivation, completeness failure and no scan fallback;
- T04 may prove the terminal-removal delta shape, but the actual terminal-publication/removal closure becomes GREEN only in W02.T05.

Output checkpoint: `W02_OPERATIONAL_ROOT_ENROLLMENT_READY`.

## W02.T05 — Durability promise and publication closure

Hard inputs: `W02_DETERMINISTIC_EXECUTION_READY`, `W02_ACCEPTED_ADJUDICATION_BASIS_READY`, `W02_OPERATIONAL_ROOT_ENROLLMENT_READY` and the current persistence/save owners.

Implement:

- explicit durability promise contract and publication plan;
- typed publication outcome for success, rejection, conflict and indeterminate acknowledgement;
- execution/durability join preserving accepted identity, fixed RNG, catalog basis and adjudication basis;
- one campaign publication closure with exact parent/currentness evidence;
- operational-root publication/removal in that closure;
- identity immutability, including the canonical campaign identity established by W01.T10;
- persistence and save-contract cutover without a repository/network-spanning transaction.

An indeterminate acknowledgement causes read/reconcile; it never causes blind re-execution. Published owner state, not the plan or a local journal, is authority.

TDD and verification:

- use `DEV/TESTS/test_rd06_durability_publication.py`;
- retain `DurabilityPromiseContractTests`, `PublicationPlanTests`, `PublicationOutcomeTests`, `ExecutionDurabilityJoinTests`, `DurabilityProjectionTests`, `Wp13ProofTests`, `SaveContractCutoverTests`, `PersistencePublicationContractTests`, `ShippedPersistenceDispositionTests`, `OperationalRootPublicationTests`, `AcceptedAdjudicationPublicationTests`, `CatalogDependencyDurabilityTests` and `CampaignIdentityImmutabilityTests`;
- verify retry after indeterminate acknowledgement and non-fast-forward reconciliation.

Output checkpoint: `W02_DURABILITY_PUBLICATION_READY`.

## W02.T06 — Exact current-source recovery and maintenance

Hard inputs: `W02_DURABILITY_PUBLICATION_READY`, `W01_NATIVE_ROUTING_READY`, `W01_TEMPORAL_OWNER_READY` and all persisted accepted bases.

Implement exact recovery:

- select only the current authoritative source through its owner-native route;
- reconstruct accepted execution with the same command identity, event identity, RNG, catalog context and adjudication basis;
- validate checkpoint descriptors and reject stale/incomplete descriptors;
- preserve session HOT as a derived current accelerator, not recovery authority;
- recover every completeness-protected operational root from the pinned campaign source;
- maintain and audit historical/native material without rewriting authority;
- return typed missing, stale, corrupt, incomplete and ambiguous failures.

TDD and verification:

- use `DEV/TESTS/test_rd07_recovery.py`;
- retain `CurrentSourceSelectionTests`, `AcceptedExecutionRecoveryTests`, `CheckpointDescriptorTests`, `SessionHotAuthorityTests`, `StorageProjectionTests`, `HistoricalMaintenanceTests`, `MaintenanceAuditMachineTests`, `OperationalRootRoutingContractTests`, `OperationalRootRecoveryTests`, `ExactPolicyBasisResolutionTests`, `AcceptedAdjudicationRecoveryTests`, `CatalogBasisRecoveryTests`, `SourceNativeLiveRecoveryTests` and `SelectedLiveCampaignIdentityRecoveryTests`;
- the last two classes turn fully GREEN after the Wave-03 LIVE owner exists; this task owns the generic recovery mechanism and Wave 03 owns the LIVE fixtures/integration;
- extend `TemporalExecutionRecoveryTests` only after this checkpoint and preserve chronology/currentness.

Produce bounded `GAME/CORE/STORAGE.md` and storage README deltas for the Wave-05 final writers.

Output checkpoints: `W02_EXACT_RECOVERY_READY` and `W02_OPERATIONAL_ROOT_RECOVERY_READY`.

## W02.T07 — Role-protected execution handoff

Hard inputs: `W01_ROLE_CONTRACT_READY`, `W01_CONTEXT_OWNER_READY` and `W02_DETERMINISTIC_EXECUTION_READY`.

Join interpreter/execution outcomes to the protected role envelope. Tool, diagnostic, context and downstream role results must enter through the typed handoff and capacity rules before emission. Rejection or truncation cannot silently change mechanics or expose private material.

TDD and verification:

- extend the role and execution suites with accepted, rejected, over-capacity, diagnostic and auxiliary-fallback integration cases;
- preserve one instruction owner and one emitted public result;
- prove no bypass through an untyped dictionary/string result.

Output checkpoint: `W02_PROTECTED_EXECUTION_HANDOFF_READY`.

## Wave 02 completion evidence

The wave closes only when a single accepted input can be traced through interpretation, catalog binding, adjudication, deterministic execution, publication and cold recovery with identical identities and bases. Record focused suites, cross-owner joins, version impacts, shared-file deltas and remote read-back. This is a prerequisite for the LIVE and collaboration publication joins, not production completion.
