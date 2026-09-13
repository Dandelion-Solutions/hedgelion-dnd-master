# Implementation Planning — Lossless Proof Ledger Appendix: WP-14 / WP-15

Status: **AUTHOR REPAIR — EXECUTION-PROOF ROUTING, NOT PROOF RESULT**
Date: 2026-09-13

This appendix is normative for the package-level proof test planned at `DEV/TESTS/test_implementation_proof_ledger.py`. It preserves each enumerated owner obligation individually. A row is not satisfied by a broad schema/audit PASS; the named witness and supporting focused/integration evidence must exist and be green.

Primary channels: `FOCUSED_BEHAVIOR`, `INTEGRATION_SCENARIO`, `STATIC_AUDIT`, `HOSTED_CI`, `EMPIRICAL_DEFERRED`.

## R074 — WP-14 §15 items 13–25

Canonical source: `2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`, §15. R074 remains direct RD-07 work with cross-owner witnesses where the owner law requires them. The later WP-21 diagnostic/cleanup owner does **not** authorize an installed maintenance command dispatcher; these rows target bounded maintenance operations/audit machine behavior only.

| Item | Exact owner obligation | Package witness | Primary channel | Supporting implementation/test route | State |
|---|---|---|---|---|---|
| 13 | fixed Connector capability/currentness/conflict/failure behavior | `Wp14RecoveryProofTests.test_13_fixed_connector_currentness_conflict_failure` | INTEGRATION_SCENARIO | RD-07 `CurrentSourceSelectionTests` + RD-06 `PublicationOutcomeTests`; fixed gameplay Connector only, typed blocked/retry/indeterminate outcomes | CURRENT_PLANNED |
| 14 | checkpoint export uses exact pinned basis and remains diagnostic | `Wp14RecoveryProofTests.test_14_checkpoint_export_exact_basis` | FOCUSED_BEHAVIOR | RD-07 `HistoricalMaintenanceTests`; `export_checkpoint_diagnostics(...)`; no HOT hydration/authority promotion | CURRENT_PLANNED |
| 15 | reset-last-checkpoint path handles retention unavailable/no guessed pointer/maintenance isolation | `Wp14RecoveryProofTests.test_15_reset_last_checkpoint_no_guess_and_isolated` | FOCUSED_BEHAVIOR | RD-07 `HistoricalMaintenanceTests`; `reset_last_checkpoint_reference(...)`; selected pointer only, no latest-by-enumeration, no gameplay side effect | CURRENT_PLANNED |
| 16 | approved historical repair promotes forward from fresh current basis | `Wp14RecoveryProofTests.test_16_forward_promotion_from_fresh_current_basis` | INTEGRATION_SCENARIO | RD-07 `HistoricalMaintenanceTests`; `validate_repair_candidate(...)` -> `promote_historical_repair(...)`; RD-06 publication currentness | CURRENT_PLANNED |
| 17 | partial multi-domain promotion/recomposition reports truthful incomplete/indeterminate outcomes | `Wp14RecoveryProofTests.test_17_partial_promotion_truthful_outcomes` | INTEGRATION_SCENARIO | RD-07 historical repair + RD-06 `DurabilityPromiseContractTests` / `PublicationOutcomeTests`; no distributed rollback fiction | CURRENT_PLANNED |
| 18 | allocator never regresses and published IDs are never reused across repair | `Wp14RecoveryProofTests.test_18_allocator_non_regression_and_no_reuse` | INTEGRATION_SCENARIO | RD-04 `CampaignAllocatorTests` + RD-07 maintenance promotion; current allocator is authoritative for new repair publication | CURRENT_PLANNED |
| 19 | historical repair preserves actual knowledge/disclosure state | `Wp14RecoveryProofTests.test_19_knowledge_disclosure_preserved` | INTEGRATION_SCENARIO | RD-02 `NativeInformationSchemaTests` / `RecipientIsolationTests` + RD-07 historical maintenance; no disclosure/knowledge rewind | CURRENT_PLANNED |
| 20 | maintenance is isolated from gameplay: no emission, RNG, gameplay IDs or chronology | `Wp14RecoveryProofTests.test_20_maintenance_no_gameplay_emission_rng_or_ids` | INTEGRATION_SCENARIO | RD-07 `HistoricalMaintenanceTests`; RD-05 fixed-RNG/idempotency negatives; RD-10 protected-emission boundary; no Interaction/Resolution/fictional advancement | CURRENT_PLANNED |
| 21 | `runtime.maintenance_audit` has machine representation and uses current allocator/publication/idempotency | `Wp14RecoveryProofTests.test_21_maintenance_audit_native_machine_and_publication` | INTEGRATION_SCENARIO | RD-07 `MaintenanceAuditMachineTests` + `record_maintenance_audit(...)`; RD-04 allocator/native route; RD-06 publication; audit record outside gameplay chronology | CURRENT_PLANNED |
| 22 | pinned historical reader obeys Step-5.13 semantic-retention boundary | `Wp14RecoveryProofTests.test_22_historical_reader_respects_retention` | FOCUSED_BEHAVIOR | RD-07 `HistoricalMaintenanceTests`; missing/compacted required evidence returns typed unavailable/limited result, never reconstructed canon | CURRENT_PLANNED |
| 23 | recovery/repair/support composes application authorization and recipient disclosure | `Wp14RecoveryProofTests.test_23_repair_authorization_and_disclosure` | INTEGRATION_SCENARIO | RD-09 `PrincipalAuthorizationTests` + RD-02 `RecipientIsolationTests` + RD-07 maintenance operation; repository permission/token is insufficient | CURRENT_PLANNED |
| 24 | stale checkpoint-at-PLAY_READY and ordinary-save assumptions are removed | `Wp14RecoveryProofTests.test_24_no_checkpoint_play_ready_or_save_prerequisite` | INTEGRATION_SCENARIO | RD-07 `CheckpointDescriptorTests`/`StorageProjectionTests` + RD-06 durability tests + RD-14 bootstrap readiness; healthy no-checkpoint path remains valid | CURRENT_PLANNED |
| 25 | executable conformance/failure coverage covers final WP-14 laws, repairs and checkpoint-field authority boundaries | `Wp14RecoveryProofTests.test_25_wp14_conformance_failure_matrix_complete` | STATIC_AUDIT | package proof enumerates 13–25; RD-07 full suite + maintenance audit + full `DEV/TESTS` discovery + hosted CI after implementation | CURRENT_PLANNED |

R074 may close only after all thirteen rows have current implementation evidence. A missing row is RED; no aggregate “recovery tests pass” claim substitutes for an item.

## R077 — WP-15 §13 items 9–17

Canonical source: `2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md`, §13. R077 is assigned to RD-08 but is explicitly join-closed because §13 crosses existing execution, information and history owners.

| Item | Exact owner obligation | Package witness | Primary channel | Supporting implementation/test route | State |
|---|---|---|---|---|---|
| 9 | remove/demote generic `CURRENT.world_time.frontier` | `Wp15TemporalProofTests.test_09_current_has_no_global_chronology_frontier` | FOCUSED_BEHAVIOR | RD-08 `CurrentStateChronologyTests`; `GAME/SCHEMA/current_state.schema.yaml` | CURRENT_PLANNED |
| 10 | remove/demote mandatory singleton scene chronology-frontier semantics | `Wp15TemporalProofTests.test_10_scene_has_no_singleton_chronology_frontier` | FOCUSED_BEHAVIOR | RD-08 `TemporalMachineAlignmentTests`; `GAME/SCHEMA/scene.schema.yaml` | CURRENT_PLANNED |
| 11 | realize explicit typed chronology relation/provider evidence where legacy fields are ambiguous | `Wp15TemporalProofTests.test_11_typed_chronology_relation_provider_evidence` | INTEGRATION_SCENARIO | RD-08 `ChronologyBridgeTests` + `chronology-relation-evidence.schema.json`; RD-13 `NativeHistoryAuthorityTests` consumes typed relation evidence in native SemanticEvent/history | CURRENT_PLANNED |
| 12 | Procedure schema owns procedure-local timing/order/budget state | `Wp15TemporalProofTests.test_12_procedure_owns_local_timing_order_budget` | FOCUSED_BEHAVIOR | RD-05 `ProcedureTemporalStateTests`; `runtime-procedure-state.schema.json` + existing concrete Procedure state, no thread/scene copy | CURRENT_PLANNED |
| 13 | remove/qualify generic Continuation `future_rng_frontier`; type `unconsumed_advancement` as accepted-execution remainder | `Wp15TemporalProofTests.test_13_continuation_has_no_generic_future_rng_schedule` | FOCUSED_BEHAVIOR | RD-05 `ContinuationTemporalStateTests`; `runtime-continuation-state.schema.json` | CURRENT_PLANNED |
| 14 | normalize PC/LIVE/event information fields into native information owners/projections | `Wp15TemporalProofTests.test_14_information_projection_normalization` | INTEGRATION_SCENARIO | RD-02 `LegacyInformationProjectionTests`/`InformationNormalizationTests`; RD-09 `LiveInformationNormalizationIntegrationTests`; RD-13 `NativeHistoryAuthorityTests` removes event-embedded alternate knowledge/disclosure authority | CURRENT_PLANNED |
| 15 | process/thread discovery indexes are non-authoritative and cannot prove temporal-root absence | `Wp15TemporalProofTests.test_15_temporal_discovery_indexes_non_authoritative` | INTEGRATION_SCENARIO | RD-04 `NativeIndexTests` + RD-08 `WorldThreadContractTests`/`TemporalMachineAlignmentTests`; no broad scan fallback | CURRENT_PLANNED |
| 16 | reconcile current CORE wording for simulation budget, chronology frontier and visibility | `Wp15TemporalProofTests.test_16_core_temporal_wording_reconciled` | STATIC_AUDIT | RD-08 `TemporalMachineAlignmentTests`; exact targets `GAME/CORE/CHRONOLOGY.md` and `GAME/CORE/PROCESSES.md`; correctness invalidation cannot be suppressed by narrative relevance | CURRENT_PLANNED |
| 17 | regression/failure-injection covers final temporal/process/chronology laws | `Wp15TemporalProofTests.test_17_temporal_failure_injection_matrix_complete` | INTEGRATION_SCENARIO | RD-08 full suite including stale contender, recovery/no-reroll, missing enrollment, indeterminate provider, no-global-scan; package full test discovery + audit | CURRENT_PLANNED |

Additional WP-15 empirical branch: fanout/partition optimization remains **dormant** until WP-24 measured evidence demonstrates an operational limit. It is not required to mark R077's current deterministic/schema realization PASS and it must not manufacture partitioning work now.

## Appendix completion rule

This appendix is complete as a plan only when every row remains traceable to the current routed RD plan and named test target. At implementation time, each `CURRENT_PLANNED` row must become evidence-bearing PASS/FAIL/NOT_APPLICABLE-with-owner-reason; no row may disappear through aggregation.