# Lossless Proof Ledger — WP-12 / WP-13

Status: **SIP-009 AUTHOR REPAIR / PLANNING ONLY**

This appendix expands `R068` and `R071` item-by-item. Planned package witness file: `DEV/TESTS/test_implementation_proof_ledger.py`.

No row is runtime PASS yet. `CURRENT_PLANNED` means the current implementation package has an executable target; `JOIN_REQUIRED` means the proof is explicitly cross-RD. Future empirical work is not activated by this ledger.

## R068 — WP-12 §14, all 17 themes

Package class: `Wp12HotProofTests`.

| # | Owner theme | Exact planned package test | Supporting RD target(s) | Primary channel | Status |
|---:|---|---|---|---|---|
| 1 | nested savepoint behavior | `test_wp12_01_nested_savepoint_behavior` | RD-04 HOT transaction | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 2 | rollback-marker behavior | `test_wp12_02_rollback_marker_behavior` | RD-04 HOT transaction | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 3 | duplicate no-op replay | `test_wp12_03_duplicate_noop_replay` | RD-04 HOT + RD-05 accepted execution | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 4 | same-source input fingerprint conflicts | `test_wp12_04_same_source_fingerprint_conflict` | RD-05 execution identity + RD-04 transaction | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 5 | cross-source operation-key collisions | `test_wp12_05_cross_source_operation_key_collision` | RD-05 accepted identity + RD-09 source identity | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 6 | dependency staleness | `test_wp12_06_dependency_staleness_rejected` | RD-04 HOT + RD-05 validation/current basis | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 7 | updater/handler observational restrictions | `test_wp12_07_transaction_callbacks_do_not_gain_authority` | RD-04 HOT API | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 8 | sparse-relative-delta replay | `test_wp12_08_sparse_relative_delta_replay` | RD-04 HOT + RD-05 owner delta | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 9 | retained RNG reuse across close/reopen and recovery | `test_wp12_09_rng_reused_across_recovery` | RD-05 fixed RNG + RD-07 recovery | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 10 | G/G+1 dirty-generation clearing | `test_wp12_10_g_plus_1_survives_g_clear` | RD-04 HOT + RD-06 durability | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 11 | crash after local commit | `test_wp12_11_crash_after_local_commit_recovers_from_native_basis` | RD-04 local establishment + RD-07 recovery | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 12 | crash after remote publication | `test_wp12_12_crash_after_remote_publication_does_not_replay` | RD-06 publication + RD-07 recovery | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 13 | independent local-domain transactions | `test_wp12_13_independent_local_domains_do_not_share_transaction` | RD-04 HOT | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 14 | multiplayer/epoch bootstrap identity isolation | `test_wp12_14_epoch_and_campaign_identity_isolation` | RD-09 LIVE source-native identity + RD-14 bootstrap | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 15 | failure/degradation integration | `test_wp12_15_failure_does_not_promote_partial_local_state` | RD-04 HOT + RD-05 failure adapter + RD-10 typed degradation | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 16 | storage baseline cannot override existing campaign exact runtime identity | `test_wp12_16_storage_baseline_is_new_campaign_only` | RD-14 exact package/bootstrap runtime selection | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 17 | offline host diagnostics separate from runtime HOT state | `test_wp12_17_diagnostics_do_not_become_hot_authority` | RD-04 HOT + shipped diagnostic projections | FOCUSED_BEHAVIOR + STATIC_AUDIT | CURRENT_PLANNED |

R068 closes only after all 17 package methods pass against implemented targets. Item 16 is intentionally routed to RD-14, not misassigned to HOT/recovery.

## R071 — WP-13 §15, all 38 themes

Package class: `Wp13DurabilityProofTests`.

| # | Owner theme | Exact planned package test | Supporting RD target(s) | Primary channel | Status |
|---:|---|---|---|---|---|
| 1 | policy/effective requiredness | `test_wp13_01_effective_requiredness` | RD-06 durability | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 2 | dirty-generation attachment/no-downgrade | `test_wp13_02_dirty_generation_not_downgraded` | RD-04 HOT + RD-06 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 3 | scope-relative closure cleanliness | `test_wp13_03_scope_relative_closure` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 4 | zero-write current save | `test_wp13_04_zero_write_current_save` | RD-06 `DurabilityPromiseContractTests` | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 5 | bounded no-write revalidation | `test_wp13_05_bounded_no_write_revalidation` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 6 | SOFT-only automatic durability | `test_wp13_06_soft_automatic_durability` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 7 | explicit SAVE all dirty | `test_wp13_07_explicit_save_includes_all_dirty_in_scope` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 8 | explicit SAVE independently required closure | `test_wp13_08_save_includes_required_clean_dependencies` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 9 | LIVE-domain delegation | `test_wp13_09_live_domain_delegates_to_live_owner` | RD-06 + RD-09 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 10 | non-live listed-root inclusion | `test_wp13_10_non_live_required_roots_included` | RD-06 + RD-04 routing | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 11 | publication pipeline correctness | `test_wp13_11_publication_pipeline` | RD-06 `PublicationPlanTests` | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 12 | save quiescence and release | `test_wp13_12_save_freeze_is_scope_local_and_released` | RD-06 + RD-04 owner generations | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 13 | one-tree publication | `test_wp13_13_one_tree_publication` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 14 | one-commit publication | `test_wp13_14_one_single_parent_commit` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 15 | stale-head conflict | `test_wp13_15_stale_head_conflict` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 16 | ambiguous ref-update reconciliation | `test_wp13_16_ambiguous_ref_update_reconciles_by_observation` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 17 | no blind replay after unknown | `test_wp13_17_unknown_outcome_never_blind_replays` | RD-06 + RD-07 recovery | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 18 | byte-identity UPSERT skip | `test_wp13_18_identical_upsert_skipped` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 19 | absent DELETE skip | `test_wp13_19_absent_delete_skipped` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 20 | resulting-tree proof | `test_wp13_20_resulting_tree_matches_frozen_closure` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 21 | scope-level failure propagation | `test_wp13_21_scope_failure_propagation` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 22 | retryable domain subset handling | `test_wp13_22_retryable_domain_subset` | RD-06 + domain adapters | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 23 | rejection cause propagation | `test_wp13_23_rejection_cause_preserved` | RD-06 publication outcome | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 24 | non-overlap CAS/retry handling | `test_wp13_24_non_overlap_conflict_revalidated` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 25 | overlap conflict no-auto-rebase | `test_wp13_25_overlap_never_auto_rebases` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 26 | disjoint concurrent edit retry | `test_wp13_26_disjoint_edit_retry_rebuilds_from_current_basis` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 27 | no-write race handling | `test_wp13_27_no_write_race_revalidates_current_basis` | RD-06 | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 28 | compatible publication clears G | `test_wp13_28_compatible_publication_clears_g` | RD-04 + RD-06 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 29 | incompatible publication retains G | `test_wp13_29_incompatible_publication_retains_g` | RD-04 + RD-06 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 30 | G+1 race preservation | `test_wp13_30_g_plus_1_race_preserved` | RD-04 + RD-06 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 31 | no persistent publication journal | `test_wp13_31_no_persistent_publication_journal` | RD-06 + static shipped-state scan | FOCUSED_BEHAVIOR + STATIC_AUDIT | CURRENT_PLANNED |
| 32 | provenance source/runtime separation | `test_wp13_32_publication_provenance_does_not_select_runtime` | RD-06 + RD-14 runtime identity | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 33 | failure/degradation separation | `test_wp13_33_failure_and_degradation_are_distinct` | RD-06 + RD-10 typed degradation | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 34 | campaign path normalization/root anchoring | `test_wp13_34_campaign_paths_are_root_anchored` | RD-06 publication planner | FOCUSED_BEHAVIOR | CURRENT_PLANNED |
| 35 | independent storage transaction behavior | `test_wp13_35_storage_transaction_is_independent_from_remote_publication` | RD-04 HOT + RD-06 | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 36 | maintenance authority separation | `test_wp13_36_maintenance_authority_does_not_grant_gameplay_publication` | RD-06 + RD-07 maintenance | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 37 | event-time/Git-time non-equivalence | `test_wp13_37_git_time_is_not_fictional_event_time` | RD-06 + RD-08 chronology | INTEGRATION_SCENARIO | JOIN_REQUIRED |
| 38 | existing stale test disposition | `test_wp13_38_stale_publication_tests_have_explicit_disposition` | package current-test audit + RD-06 | STATIC_AUDIT | CURRENT_PLANNED |

## R071 completion checkpoint

RD-06 `Wp13ProofTests` and package `Wp13DurabilityProofTests` are complementary:
- RD-06 proves owner-local behavior at its checkpoint;
- package tests prove cross-owner rows and one-to-one traceability for all 38 items.

A generic `unittest discover` PASS is supporting evidence only. R071 remains incomplete if any numbered row lacks its exact witness, even when all RD-06 direct functional tests pass.

## Currentness rule

Before implementation of either suite, fresh-read WP-12/WP-13 and the supporting RD plans at worker HEAD. If an owner later supersedes any numbered theme, update this ledger from that owner first; do not silently reinterpret the row in test code.