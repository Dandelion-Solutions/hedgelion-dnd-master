# Implementation Planning — Lossless Proof Ledger WP-12 / WP-13 v2

Status: **CURRENT AUTHOR-REPAIRED APPENDIX — EXECUTION NOT AUTHORIZED**
Date: 2026-09-13
Supersedes for current routing: `2026-09-13-implementation-planning-lossless-proof-ledger-wp12-wp13.md`.
Canonical owners: WP-12 §14 and WP-13 §15.

Purpose: bind every canonical WP-12/WP-13 proof duty to its actual semantics, implementation target and executable witness. Row counts alone are not coverage.

Primary channels:
- `FOCUSED_BEHAVIOR` — deterministic owner-local behavior;
- `INTEGRATION_SCENARIO` — cross-owner/currentness behavior;
- `STATIC_AUDIT` — supporting stale/projection evidence only.

No STATIC_AUDIT/HOSTED_CI result may discharge a behavioral or integration row.

## 1. R068 — WP-12 §14 exact 17 duties

Package class: `Wp12HotProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`.

| # | Canonical duty | Supporting target(s) | Named package witness | Primary channel |
|---|---|---|---|---|
| 1 | Owner adoption validates native family, native identity and native shape before HOT participation. | RD-04 native routing/HOT | `test_wp12_01_owner_adoption_validates_native_identity_and_shape` | FOCUSED_BEHAVIOR |
| 2 | Campaign/context namespaces are isolated; identical local keys cannot alias across admitted scopes. | RD-04 route/HOT namespace | `test_wp12_02_campaign_context_namespace_isolation` | FOCUSED_BEHAVIOR |
| 3 | HOT possession/cached bytes cannot bypass role, access or information eligibility. | RD-04 + RD-09 + RD-02/RD-10 eligibility | `test_wp12_03_hot_possession_does_not_bypass_eligibility` | INTEGRATION_SCENARIO |
| 4 | SQL row identity/order is not native identity, fictional chronology, priority or mechanics. | RD-04 + RD-08 | `test_wp12_04_sql_metadata_is_nonsemantic` | INTEGRATION_SCENARIO |
| 5 | Native edge remains atomic; pre-CAS LIVE state is prospective, exact-source CAS establishes LIVE authority, post-CAS SQLite adoption is local only. | RD-04 + RD-09 | `test_wp12_05_native_edge_atomic_live_cas_authoritative` | INTEGRATION_SCENARIO |
| 6 | No SQLite transaction spans external dialogue, repository or network I/O. | RD-04 HOT transaction | `test_wp12_06_sqlite_transaction_contains_no_external_io` | FOCUSED_BEHAVIOR |
| 7 | Accepted execution resumes only under a compatible accepted interpretation/currentness context. | RD-05 + RD-07 + RD-08 | `test_wp12_07_resume_requires_compatible_interpretation_context` | INTEGRATION_SCENARIO |
| 8 | Known-ID hydration derives WP-11 native route without scan and validates full identity. | RD-04 route/index | `test_wp12_08_known_id_hydrates_via_native_route_without_scan` | FOCUSED_BEHAVIOR |
| 9 | Cache/index absence is not native absence; rebuild from native authority succeeds. | RD-04 route/index/HOT | `test_wp12_09_cache_or_index_absence_is_not_native_absence` | FOCUSED_BEHAVIOR |
| 10 | Disjoint source movement can preserve local semantics; overlapping movement invokes owner revalidation. | RD-04 + RD-06/RD-09 currentness | `test_wp12_10_disjoint_movement_preserves_overlap_revalidates` | INTEGRATION_SCENARIO |
| 11 | Frozen publication records principal/authorization plus exact generation G; success for G cannot clear G+1. | RD-06 + RD-04 generation support | `test_wp12_11_frozen_publication_principal_and_generation_specific_clear` | INTEGRATION_SCENARIO |
| 12 | HOT/recovery introduces no generic pending-work, publication-journal or second recovery authority. | RD-04 + RD-06 + RD-07 | `test_wp12_12_no_generic_pending_or_publication_journal_authority` | INTEGRATION_SCENARIO |
| 13 | Pre-CAS LIVE prospective state is not current/shared truth. | RD-09 LIVE currentness | `test_wp12_13_pre_cas_live_state_is_not_current` | FOCUSED_BEHAVIOR |
| 14 | If LIVE CAS was accepted but local adoption failed, recover from accepted LIVE authority without gameplay/mechanics/RNG replay. | RD-09 + RD-07 + RD-05 | `test_wp12_14_post_cas_adoption_failure_recovers_without_replay` | INTEGRATION_SCENARIO |
| 15 | Cold recovery ignores unpublished local generations unless another durable/equivalent owner established them. | RD-07 + RD-04 | `test_wp12_15_cold_recovery_ignores_unpublished_hot_generation` | INTEGRATION_SCENARIO |
| 16 | Storage baseline may select runtime for New Game but cannot override an existing campaign runtime. | RD-14 bootstrap + storage/runtime owner; RD-06 proves no SAVE coupling | `test_wp12_16_storage_baseline_does_not_override_campaign_runtime` | INTEGRATION_SCENARIO |
| 17 | Legacy global timer/frontier/checkpoint debt is not a WP-12 HOT law. | RD-04 + RD-06/RD-07 negative law | `test_wp12_17_no_legacy_global_timer_frontier_or_checkpoint_debt` | INTEGRATION_SCENARIO |

### WP-12 mandatory positive/negative shape

Every row above has both a positive acceptance path and a negative rejection/non-authority assertion inside the named method or its fixture matrix. In particular:
- rows 3/4 reject authority or chronology derived merely from cached/SQL metadata;
- rows 5/13 reject pre-CAS LIVE authority;
- rows 11/14/15 prove crash/generation behavior without a parallel journal;
- row 16 is explicitly storage-baseline independence and must not be rewritten as a HOT/publication requirement.

`R068` cannot close until all 17 methods pass through their assigned primary channel.

## 2. R071 — WP-13 §15 exact 38 duties

Package class: `Wp13DurabilityProofTests` in planned `DEV/TESTS/test_implementation_proof_ledger.py`.

| # | Canonical duty | Supporting target(s) | Named package witness | Primary channel |
|---|---|---|---|---|
| 1 | Serialization/persistence does not semantically establish gameplay state by itself. | RD-06 + native owner establishment | `test_wp13_01_serialization_is_not_semantic_establishment` | INTEGRATION_SCENARIO |
| 2 | No campaign-global one-hour timer, durable frontier, save clock or universal HARD queue exists. | RD-06 durability | `test_wp13_02_no_global_hour_timer_frontier_or_save_queue` | FOCUSED_BEHAVIOR |
| 3 | Scope exposure tracks the oldest still-relevant unpublished state for that scope, not a universal timestamp. | RD-06 durability | `test_wp13_03_scope_exposure_tracks_oldest_relevant_unpublished_state` | FOCUSED_BEHAVIOR |
| 4 | Risk-control durability failure does not become HARD merely from that failure absent a separate owner edge. | RD-06 + DURABILITY_GUARD consumer | `test_wp13_04_risk_control_failure_is_not_implicitly_hard` | FOCUSED_BEHAVIOR |
| 5 | Required compatible closure is distinct from the pending write set. | RD-06 | `test_wp13_05_compatible_closure_is_distinct_from_pending_writes` | FOCUSED_BEHAVIOR |
| 6 | Closure is bounded and native-routed; no universal campaign graph scan/frontier is required. | RD-06 + RD-04 | `test_wp13_06_closure_is_bounded_and_native_routed` | INTEGRATION_SCENARIO |
| 7 | Explicit SAVE freezes one definite selected scope/root/generation set. | RD-06 | `test_wp13_07_explicit_save_freezes_definite_scope` | FOCUSED_BEHAVIOR |
| 8 | SAVE composes native-domain durability results; it does not impose global ordering, rollback or one cross-domain transaction. | RD-06 + RD-09 LIVE join | `test_wp13_08_save_composes_native_domains_without_global_transaction` | INTEGRATION_SCENARIO |
| 9 | A no-write SAVE success requires current compatible closure evidence, not merely an empty dirty set. | RD-06 | `test_wp13_09_no_write_success_requires_current_compatible_closure` | FOCUSED_BEHAVIOR |
| 10 | Partial native-domain success remains true evidence but cannot produce false overall SAVE acknowledgement. | RD-06 | `test_wp13_10_partial_native_success_suppresses_overall_save_ack` | FOCUSED_BEHAVIOR |
| 11 | Final SAVE success proves one current compatible composition for all required frozen domains. | RD-06 | `test_wp13_11_final_save_success_proves_current_compatible_composition` | INTEGRATION_SCENARIO |
| 12 | Quiescence/freeze is released only after safe success, explicit abandonment or owner-valid currentness/reconciliation; uncertainty cannot silently release it. | RD-06 | `test_wp13_12_quiescence_release_requires_safe_disposition` | FOCUSED_BEHAVIOR |
| 13 | Campaign publication attempt freezes before the first remote mutation. | RD-06 publication | `test_wp13_13_publication_attempt_freezes_before_remote_mutation` | FOCUSED_BEHAVIOR |
| 14 | Frozen attempt contains exact generations, authorization, reads/dependencies/currentness and path/index closure required for the mutation. | RD-06 + RD-04/RD-09 | `test_wp13_14_frozen_attempt_contains_complete_currentness_basis` | INTEGRATION_SCENARIO |
| 15 | Trustworthy principal/authorization evidence is required; commit metadata or repository permission alone is insufficient. | RD-06 + RD-09 | `test_wp13_15_publication_requires_trustworthy_principal_authorization` | INTEGRATION_SCENARIO |
| 16 | WP-11 native record plus required index/projection UPSERT/DELETE participate coherently in one campaign-domain publication closure. | RD-04 + RD-06 | `test_wp13_16_native_record_index_projection_delta_is_coherent` | INTEGRATION_SCENARIO |
| 17 | Resulting-tree preflight checks the bounded touched closure for missing required path/invariant before ref transition. | RD-06 | `test_wp13_17_bounded_resulting_tree_preflight_rejects_missing_invariant` | FOCUSED_BEHAVIOR |
| 18 | Byte-identical UPSERT and already-absent DELETE normalize to no-op and do not force publication. | RD-06 | `test_wp13_18_normalized_noop_delta_does_not_publish` | FOCUSED_BEHAVIOR |
| 19 | Supported campaign publication transport remains the admitted Python/core -> Connector -> non-force Git-data path. | RD-06 + process transport | `test_wp13_19_supported_transport_is_connector_nonforce_path` | INTEGRATION_SCENARIO |
| 20 | Missing Connector capability does not authorize alternate shell git/gh/direct HTTP transport. | RD-06 + process negative law | `test_wp13_20_missing_connector_capability_has_no_transport_fallback` | INTEGRATION_SCENARIO |
| 21 | One campaign publication boundary builds one base-derived tree, one single-parent commit and one non-force target-ref transition. | RD-06 | `test_wp13_21_campaign_boundary_uses_one_tree_single_parent_nonforce_transition` | FOCUSED_BEHAVIOR |
| 22 | Target-ref transition result is explicitly `ACCEPTED`, `REJECTED` or `INDETERMINATE`. | RD-06 | `test_wp13_22_ref_transition_has_three_epistemic_outcomes` | FOCUSED_BEHAVIOR |
| 23 | A rejected transition is classified against current authority before retry. | RD-06 | `test_wp13_23_rejection_is_classified_before_retry` | FOCUSED_BEHAVIOR |
| 24 | INDETERMINATE forbids success acknowledgement, generation clear, quiescence release, gameplay replay and blind retry until reconciled. | RD-06 | `test_wp13_24_indeterminate_transition_blocks_ack_clear_release_and_replay` | FOCUSED_BEHAVIOR |
| 25 | Ambiguity reconciliation uses bounded current-ref plus lineage/current-closure observation. | RD-06 | `test_wp13_25_indeterminate_reconciliation_reads_bounded_authority` | INTEGRATION_SCENARIO |
| 26 | Disjoint target movement preserves already-established semantic IDs/RNG/outcomes and rebuilds only transport/currentness basis as needed. | RD-06 + RD-05 | `test_wp13_26_disjoint_movement_preserves_semantics_and_rng` | INTEGRATION_SCENARIO |
| 27 | Overlapping movement invokes owner-defined rejection/reconciliation and is never resolved by generic text merge. | RD-06 + affected owner | `test_wp13_27_overlapping_movement_uses_owner_revalidation_not_text_merge` | INTEGRATION_SCENARIO |
| 28 | Retry/reconciliation is bounded; no unbounded publication loop is permitted. | RD-06 | `test_wp13_28_publication_retry_is_bounded` | FOCUSED_BEHAVIOR |
| 29 | Accepted publication for frozen generation G clears only G; concurrent/newer G+1 remains dirty. | RD-06 + RD-04 generation helper | `test_wp13_29_generation_g_success_preserves_g_plus_1` | INTEGRATION_SCENARIO |
| 30 | Partial/unrelated adoption cannot reset another owner's dirty exposure basis. | RD-06 | `test_wp13_30_unrelated_adoption_does_not_reset_other_scope_exposure` | INTEGRATION_SCENARIO |
| 31 | Crash after remote success but before local adoption recovers from native authority without a persistent publication journal or gameplay replay. | RD-06 + RD-07 | `test_wp13_31_remote_success_local_loss_recovers_from_native_authority` | INTEGRATION_SCENARIO |
| 32 | LIVE exact-source CAS remains the LIVE establishment/currentness boundary and is not replaced by campaign SAVE publication. | RD-09 + RD-06 composition | `test_wp13_32_live_exact_source_cas_remains_live_establishment` | INTEGRATION_SCENARIO |
| 33 | Checkpoint creation is optional owner policy and is not itself SAVE success, handoff success or currentness proof. | RD-07 + RD-06 | `test_wp13_33_checkpoint_is_not_save_handoff_or_currentness_proof` | INTEGRATION_SCENARIO |
| 34 | Session/local cached HEAD is a hint/basis, not repository/current gameplay authority. | RD-07/RD-14 + RD-06 publication | `test_wp13_34_cached_head_is_not_authority` | INTEGRATION_SCENARIO |
| 35 | Storage-baseline transaction/metadata authority is independent from campaign SAVE composition. | RD-14 storage/bootstrap + RD-06 | `test_wp13_35_storage_baseline_is_independent_from_campaign_save` | INTEGRATION_SCENARIO |
| 36 | Engine/rules maintenance uses ordinary authorized campaign publication after its own compatibility/adoption checks; SAVE does not broaden maintenance authority. | RD-06 + current ENGINE_UPDATES consumer | `test_wp13_36_engine_rules_maintenance_reuses_publication_without_authority_broadening` | INTEGRATION_SCENARIO |
| 37 | Git commit/ref order/time never manufactures fictional chronology or semantic priority. | RD-08 + RD-06 | `test_wp13_37_git_order_and_time_do_not_define_fictional_chronology` | INTEGRATION_SCENARIO |
| 38 | Every named stale SAVE/durability/publication regression consumer/test is explicitly repaired, owner-routed or proved non-applicable/current-conforming. | RD-06 + RD-09/RD-14 consumer joins | `test_wp13_38_stale_consumer_and_test_dispositions_are_complete` | STATIC_AUDIT + INTEGRATION_SCENARIO |

## 3. WP-13 shipped-consumer disposition required by row 38

The implementation checkpoint must materialize this table against fresh current bytes; a stale table entry is RED rather than permission to edit arbitrarily.

| Surface | Planning-baseline disposition | Owning implementation route |
|---|---|---|
| `GAME/CORE/SAVE_CONTRACT.md` | **MODIFY** — remove universal campaign-only SAVE composition; express native-domain composition and exact-generation acknowledgement/clear rules | RD-06 Task 5 repair overlay |
| `GAME/CORE/PERSISTENCE.md` | **MODIFY** — preserve valid Git-data laws; add frozen basis, transition epistemics, rejection/ambiguity reconciliation, G/G+1 and crash-currentness rules | RD-06 Task 5 repair overlay |
| `GAME/CORE/DURABILITY_GUARD.md` | **CURRENT_CONFORMING / INSPECT** at planning baseline | RD-06 currentness test; edit only on concrete contradiction |
| `GAME/CORE/STORAGE.md` | **CURRENT_CONFORMING / INSPECT**; storage baseline remains independent | RD-06/RD-14 integration witness |
| `GAME/CORE/ENGINE_UPDATES.md` | **CURRENT_CONFORMING / INSPECT**; maintenance keeps own authority and consumes ordinary campaign publication | RD-06 integration witness |
| `GAME/CORE/MULTIPLAYER.md` | **OWNER-ROUTED** LIVE/access semantics; do not let RD-06 overwrite WP-16 authority | RD-09 current plan + repair overlay integration |
| `GAME/CORE/LIVE_SCENE.md` | **OWNER-ROUTED** exact-source LIVE lifecycle/currentness | RD-09 current plan + repair overlay integration |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | **MODIFY** generator identity prose to include exact ruleset-set digest | RD-14 Task 3 repair overlay |
| `GAME/CORE/CAMPAIGN_SETUP.md` | **MODIFY** same | RD-14 Task 3 repair overlay |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | **CURRENT_CONFORMING / PROTECT** at planning baseline | RD-14 `GeneratorConsumerProjectionTests` |
| `GAME/TOOLS/init_campaign.py` | **CURRENT_CONFORMING / PROTECT** exact digest argument + MANIFEST propagation at planning baseline | RD-14 generator tests |
| existing stale SAVE/hour/frontier/blanket-clear tests | **DISCOVER_AND_REWRITE/RETIRE BY SEMANTICS**; absence recorded, no invented retirement work | RD-06/RD-09/RD-14 focused tests |

## 4. Proof-channel and closure laws

`R068` closes only when all 17 WP-12 rows pass. `R071` closes only when all 38 WP-13 rows pass. A maintenance-audit PASS, schema existence, broad unittest discovery or hosted CI result is supporting evidence only and cannot substitute for the row's primary channel.

Rows 16/35 explicitly preserve storage baseline as a separate authority from existing-campaign runtime/HOT/SAVE publication. Rows 5/13/14/32 explicitly preserve LIVE exact-source establishment as separate from campaign publication. Rows 12/24/31 reject a parallel generic journal/recovery authority.

If a future execution baseline makes a row genuinely `NOT_APPLICABLE`, the worker must cite the exact current owner clause and current shipped evidence. Silent omission is failure.

## 5. Planning Version Impact

This v2 appendix changes proof routing only. Planning publication Version Impact: **NONE**. Runtime/version effects are classified only when future workers implement the actual repaired deltas.
