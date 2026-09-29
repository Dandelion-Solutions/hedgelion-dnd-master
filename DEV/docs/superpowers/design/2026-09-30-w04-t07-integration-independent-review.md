# W04 T07-INTEGRATION independent review

Status: **PASS — T07A–T07E INTEGRATED REVIEW COMPLETE**

REVIEWED_HEAD: `3c61f636257f5febbfd47339e25a6be420852be9`
REVIEW_SURFACE: published `v1/engine-rearchitecture` source; independent `hdm-reviewer`
PLAN: `DEV/docs/superpowers/plans/implementation-wave-04-collaboration-context-story.md`, T07 rows and integration gate (§§339–423)
VERSION_IMPACT: NONE — review evidence only; no version/revision/schema/generation owner changed.
SYSTEM_IMPACT: NONE — no new cross-owner or architecture trigger found.

## Verdict and scope

**Overall verdict: PASS.** The independent review checked each separately stated T07A–T07E plan RED/requirement against the current owner code and tests, inspected the accepted native-history → Story/T0 → Commentator → Dramaturg chain, and reconciled persisted schema/module versions. No T07 integration finding remains. It found no evidence that reopens the recorded CLS↔HDM preflight; that preflight was not rerun and its existing semantic-change/unavailable-evidence triggers remain in force.

The dependency chain remains source-bound native evidence → four owner-local Story layers and recoverable T0 → separate current Commentator control and pre-materialization privacy filter → noncanonical Dramaturg planning. No observed reverse edge promotes Story, Commentator or Dramaturg data into native history, currentness, gameplay, catch-up or Narrator authority.

## Item-level traceability

Test names below are in `DEV/TESTS/test_rd13_story_t0_commentator.py` unless a different module is named.

### T07A — accepted native history publication/recovery

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| A1 | No gameplay/domain API accepts RepositoryPort, LIVE, runtime/history-service or source-adapter overrides. | `GAME/TOOLS/history.py:647–676`; `GAME/TOOLS/runtime_host.py:1478–1538` | `test_history_api_has_no_caller_adapter_override` (RD13:1093); `test_gameplay_methods_reject_capability_and_service_overrides` (RuntimeHost:624); `test_untrusted_request_data_cannot_select_or_replace_transport` (RuntimeHost:667) |
| A2 | LOCAL aggregate LOG/SEMANTIC_EVENTS is not source-domain proof. | RuntimeHost source-adapter path (around 1169–1303); `history.py:679–795` | `test_history_rejects_aggregate_or_forged_window_shapes` (RD13:819); `test_local_semantic_events_use_index_and_exact_known_ids_not_aggregate_log` (RuntimeHost:1000); `test_local_semantic_events_reject_missing_enrollment_completion_proof` (RuntimeHost:1035) |
| A3 | Caller-shaped SemanticEvent cannot mint accepted history. | `history.py:679–735, 965–977` | `test_caller_shaped_semantic_events_cannot_mint_native_history` (RD13:762) |
| A4 | Duplicate/gapped/nonmonotonic ID or evt-admission ordinal is rejected. | `history.py:746–795, 262–343` | `test_history_rejects_wrong_provenance_order_schema_and_interval` (RD13:962); `test_history_rechecks_forged_gap_duplicate_and_completeness_claims` (RD13:988) |
| A5 | Provenance/currentness/window-completeness mismatch is rejected. | `history.py:714–735, 796–916`; window issuance remains bound to RuntimeHost | `test_history_rejects_wrong_provenance_order_schema_and_interval` (RD13:962); `test_history_recovery_revalidates_ephemeral_publication_provenance` (RD13:1070) |
| A6 | A bounded source window is required. | `history.py:647–676`; RuntimeHost bounds local and selected-LIVE windows | `test_history_owner_reads_exact_bounded_evt_page` (RD13:770); `test_oversized_local_enrollment_reads_only_the_requested_bounded_window` (RuntimeHost:1135); `test_oversized_live_pack_reads_only_the_requested_bounded_window` (RuntimeHost:1179) |
| A7 | Interruption/recovery preserves identity, origin, provenance and source enrollment. | `history.py:817–916, 262–343` | `test_history_recovery_revalidates_ephemeral_publication_provenance` (RD13:1070). **Qualification:** this proves recovery-envelope revalidation, not a distinct process-kill test for every interruption point. |
| A8 | Selected-LIVE reads exact route-selected one-file evidence without inventing a tree index. | `runtime_host.py:502–522, 1169–1452`; `history.py:647–676` | `test_history_uses_exact_selected_live_source_and_preserves_origin` (RD13:916); `test_selected_live_semantic_events_use_exact_source_pack_without_campaign_fallback` (RuntimeHost:1099) |
| A9 | Narration/Story cannot reconstruct native history. | `GAME/TOOLS/story.py:1585–1623`; `history.py:679–735` | `test_caller_shaped_semantic_events_cannot_mint_native_history` (RD13:762); `test_story_validation_never_mutates_native_history` (RD13:3514) |
| A10 | Routed missing LIVE source never falls back to campaign. | Bound selected-LIVE path in RuntimeHost and History | `test_missing_selected_live_history_never_falls_back_to_local` (RD13:944); `test_missing_selected_live_source_does_not_fall_back_to_local` (RuntimeHost:1121) |

### T07B — four Story layers and eight fixed registrations

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| B1 | T-MSG exists; ordinary transcript is optional and does not discharge archive obligations. | `GAME/TOOLS/story.py:69–97` (MAY_OMIT, zero-or-one); T-ARC separately registered at `84–97` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_registration_requiredness_and_omission_codes_are_closed` (1322); `test_transcript_units_do_not_merge_distinct_message_candidates` (2028) |
| B2 | T-ARC exists and its exact archival promise is distinct from T-MSG. | `story.py:84–97, 1322–1329` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_archive_and_relation_registrations_bind_candidate_owner_source` (1904); `test_candidate_result_enforces_registration_cardinality` (1413) |
| B3 | E-EVT exists; required event material cannot be dropped by importance. | `story.py:99–108, 1217–1284, 1585–1597, 1707–1753` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_candidate_results_cannot_omit_required_or_rank_candidates` (1341); `test_story_catchup_materializes_every_event_without_caller_omission` (2659) |
| B4 | E-REL independently covers late EVENTS relations. | `story.py:109–122`; domain/cardinality validation at `1300–1387` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_archive_and_relation_registrations_bind_candidate_owner_source` (1904) |
| B5 | M-SEG uses segment-specific identity/cardinality. | `story.py:123–136`; exact segment selector validation | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_segment_candidate_binds_exact_segment_sequence_selector` (1998); `test_m_seg_payload_contract_table_runs_through_python_and_json_schema` (2012) |
| B6 | M-OUT preserves terminal zero-change/failure outcomes. | `story.py:137–150, 1315–1387`; only narrow `NO_GAMEPLAY_OUTCOME` omission code | `test_candidate_results_cannot_omit_required_or_rank_candidates` (1341); `test_terminal_outcome_candidate_binds_its_resolution_or_command_owner` (1968) |
| B7 | N-EVT independently registers NARRATIVE events; EVENTS completion cannot substitute. | `story.py:151–160`; domain/generation coverage at `1010–1095` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_candidate_result_enforces_registration_cardinality` (1413); `test_source_window_uses_domain_local_contiguous_coverage_and_cardinality` (1632) |
| B8 | N-REL independently covers late NARRATIVE relations. | `story.py:161–175`; domain/generation coverage at `1010–1095` | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_archive_and_relation_registrations_bind_candidate_owner_source` (1904); `test_source_window_uses_domain_local_contiguous_coverage_and_cardinality` (1632) |
| B9 | EVENTS-only implementation is insufficient. | Four layer-specific validators/prefix rules: `story.py:180–188, 506–597`; four layer schemas | `test_all_four_unit_contracts_validate_their_payload_and_prefix` (1869); `test_closed_registry_has_all_eight_layer_domain_lanes` (1192) |
| B10 | MUST candidates cannot be dropped based on importance. | Required registrations reject MAY_OMIT (`story.py:1315–1329`); publication requires every accepted native event body (`1707–1753`) | `test_candidate_results_cannot_omit_required_or_rank_candidates` (1341); `test_story_window_cannot_advance_coverage_with_a_missing_event_body` (2589); `test_story_catchup_materializes_every_event_without_caller_omission` (2659) |
| B11 | Late relations independently cover EVENTS and NARRATIVE. | Separate E-REL/N-REL registrations; domain-local coverage (`story.py:109–122, 161–175, 1010–1095`) | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_archive_and_relation_registrations_bind_candidate_owner_source` (1904); `test_source_window_uses_domain_local_contiguous_coverage_and_cardinality` (1632) |
| B12 | M-OUT retains terminal zero-change/failure rather than treating it as omission. | `story.py:137–150, 1315–1387` | `test_candidate_results_cannot_omit_required_or_rank_candidates` (1341); `test_terminal_outcome_candidate_binds_its_resolution_or_command_owner` (1968) |
| B13 | T-ARC exact promise cannot be discharged by T-MSG. | Separate source domains, policies and codecs (`story.py:74–97`) | `test_closed_registry_has_all_eight_layer_domain_lanes` (1192); `test_registration_requiredness_and_omission_codes_are_closed` (1322); `test_archive_and_relation_registrations_bind_candidate_owner_source` (1904) |
| B14 | LIVE-origin absorption does not duplicate candidates as LOCAL. | Exact origin is in source-domain identity (`story.py:233–284, 1624–1627, 1803–1814`) | `test_native_origin_scopes_are_byte_escaped_without_case_folding` (1310); `test_selected_live_story_window_preserves_origin_and_uses_campaign_anchor` (2700). **Qualification:** no dedicated single test publishes the same payload through both LOCAL and LIVE and asserts deduplication; code retains origin identity and the LIVE publication test checks it. |
| B15 | Coverage is domain/generation/cardinality-specific, never one global scalar. | `story.py:1010–1095, 1148–1284`; `story-projection-state.schema.json:54–104` | `test_source_window_uses_domain_local_contiguous_coverage_and_cardinality` (1632); `test_incompatible_coverage_generation_cannot_acknowledge_an_older_page` (2401); `test_story_projection_state_validator_rejects_stale_or_incompatible_coverage` (2610) |

**Source-classified omission qualification:** `validate_story_candidate_result` rejects every `OMITTED` result for SOURCE_CLASSIFIED registrations (`story.py:1371–1378`). This requires owner classification evidence but does not implement a positive native-proven omission admission path. Existing tests prove conservative rejection, not positive omission support. A caller MAY_OMIT/reason flag cannot authorize omission. This is preserved in the accepted T07B qualification at execution-status lines 553–557; it is not evidence that required candidates may be omitted.

### T07C — Story-local T0, exact currentness and publication

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| C1 | Current T1 cannot substitute for historical T0. | `GAME/TOOLS/history.py:1234–1316`; `story.py:1550–1582` | `test_t0_basis_is_explicit_and_reconstructible_without_current_actor_state` (1108); `test_t0_basis_is_extracted_only_from_its_exact_native_semantic_event` (1142) |
| C2 | Required retained WP-19 material T0 is Story-local recoverable. | `history.py:1252–1316`; Story event basis in `story.py:1538–1582` | `test_t0_factor_protection_classification_is_required_and_registered` (1123); `test_story_event_retains_story_local_t0_basis` (2084); `test_native_t0_basis_is_materialized_with_story_state_in_one_publication` (2090) |
| C3 | Private/off-screen material remains retained but availability-filtered. | `history.py:1264–1297`; separate reader filtering in `commentator.py:538–649` | `test_t0_factor_protection_classification_is_required_and_registered` (1123); `test_commentator_filters_hidden_story_material_before_request_materialization` (2743); `test_public_material_is_available_without_a_player_and_ignores_visible_to` (2958) |
| C4 | Stale native or Story basis is rejected. | `story.py:1610–1669, 1670–1709` | `test_changed_native_event_basis_rejects_stale_story_window` (2487); `test_mutated_exact_older_page_is_rejected_after_coverage_advances` (2337); `test_story_projection_state_validator_rejects_stale_or_incompatible_coverage` (2610) |
| C5 | Story cannot block or roll back canon. | W02 owner-delta publication only (`story.py:1801–1863`) | `test_rejected_story_publication_does_not_mutate_native_history` (2565); `test_story_validation_never_mutates_native_history` (3514); `test_campaign_movement_during_story_write_cannot_overwrite_newer_canon` (2520) |

### T07D-P0 — registered Commentator-control Context evidence

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| P1 | Unknown Commentator profile rejected before registration. | `GAME/TOOLS/context_runtime.py:93–134, 258–327` | `test_context_schema_and_module_contract_are_registered` (RD11:646); `test_wrong_registered_role_purpose_and_unknown_profile_fail_closed` (619); exact profile binding (659) |
| P2 | Arbitrary PLAYER/PC identity cannot bypass exact-current PLAYER reload. | `context_runtime.py:511–529, 985–998` | `test_disclosure_requires_a_required_current_player_candidate` (RD11:834); `test_missing_exact_player_record_stops_before_selected_pc_knowledge` (1208); `test_player_candidate_identity_cannot_substitute_another_recipient` (1149) |
| P3 | Foreign/uncontrolled selected PC is rejected. | `context_runtime.py:527–529, 985–998` | `test_uncontrolled_selected_pc_fails_before_knowledge_read` (911); single Commentator nomination (691) |
| P4 | Multiple controlled PCs are never unioned. | One selected PC binds request subject/knowledge (`context_runtime.py:1010–1021`) | `test_multiple_controlled_pcs_never_union_knowledge` (955) |
| P5 | Knowledge for another subject is rejected. | `context_runtime.py:556–576, 1010–1021` | `test_required_knowledge_for_another_subject_is_not_loaded` (1041); `test_knowledge_owner_identity_mismatch_fails_closed` (1001) |
| P6 | Disclosure for another PLAYER is rejected. | `context_runtime.py:579–590, 1023–1036` | `test_disclosure_for_another_player_is_not_loaded_or_admitted` (1081); exact disclosure mismatch (1251) |
| P7 | Caller `current`/`eligible` flags remain forbidden. | `context_runtime.py:173–203, 258–270, 950–966` | `test_forged_current_and_eligible_flags_cannot_admit_required_material` (RD11:460); `test_commentator_profile_rejects_index_and_forbidden_authority_fallbacks` (1306) |
| P8 | Missing/stale exact nominated owner evidence is UNSATISFIABLE. | Required closure and exact owner reads fail closed (`context_runtime.py:511–590, 1310 onward`) | `test_missing_exact_knowledge_owner_record_is_unsatisfiable` (1173); `test_missing_exact_player_record_stops_before_selected_pc_knowledge` (1208); `test_missing_or_mismatched_exact_disclosure_owner_fails_closed` (1251) |
| P9 | No scan/index fallback. | Fixed profile channels and owner resolution (`context_runtime.py:126–132, 971–976`) | Forbidden fallback (RD11:1306); bounded registered channels (1363) |
| P10 | No persistent capability/control state. | Fixed ephemeral profile table (`context_runtime.py:93–134`); no persisted control owner | Profile/schema registration (RD11:646); `test_host_capabilities_are_not_serializable_or_persistable` (RuntimeHost:687). **Qualification:** no separate test attempts to persist a P0 result; implementation has no persistence route. |

### T07D — Commentator control/snapshot and anti-oracle filter

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| D1 | Arbitrary player→Story-ID map cannot mint eligibility. | `GAME/TOOLS/commentator.py:65–129, 138–245, 248–377` | `test_arbitrary_player_to_story_ids_cannot_mint_eligibility` (2811); only assembled registered profile (2817) |
| D2 | CONTENT_FINAL is not ACCESS_FINAL. | Independent control refresh/filter (`commentator.py:436–448, 652–674`) | `test_content_unchanged_control_refresh_replaces_the_filter_basis` (3313) |
| D3 | Changed permission/control basis refreshes when content is unchanged. | `commentator.py:436–448` | Same control-refresh test (3313) |
| D4 | Ineligible IDs/counts/metadata do not reach model materialization. | Whole-record filter (`commentator.py:538–649, 652–674`) | `test_ineligible_story_ids_and_content_do_not_enter_the_filtered_bundle` (3350); pre-materialization filter test (2743) |
| D5 | No native-only fallback for qualifying retained T0 factors. | Snapshot requires Story `t0_basis` (`commentator.py:380–409`); Story materializes it (`story.py:1550–1582`) | `test_story_event_retains_story_local_t0_basis` (2084); `test_unmatched_or_insufficient_native_anchor_evidence_fails_closed` (3036); `test_unsupported_t0_anchor_value_fails_closed` (3253) |

### T07E — Dramaturg source/generation admission, publication and rebase

| ID | Plan requirement | Owner evidence | Test evidence |
|---|---|---|---|
| E1 | Retained horizon is multiplayer-only. | `GAME/TOOLS/dramaturg.py:1481–1518` | `test_multiplayer_candidate_reads_mode_membership_and_context_profile_before_preparing` (4264); `test_retained_families_have_only_the_fixed_shared_and_stable_player_routes` (3397) |
| E2 | Future/planning text is noncanonical. | Planning-only types/fields and accepted-publication promotion (`dramaturg.py:23–109, 329–408, 1180–1325`) | `test_dramaturg_horizon_is_provisional_and_has_no_future_fact_field` (3488); `test_only_confirmed_w02_publication_promotes_the_prepared_owner_generation` (4085) |
| E3 | Stale/incompatible basis is discarded/reprepared, never text-merged. | Revalidation/conflict handling (`dramaturg.py:1481–1570`) | `test_conflict_with_newer_planning_generation_is_discarded_without_text_merge` (4181); `test_conflict_without_horizon_movement_reprepares_exact_candidate_without_retrying` (4230); `test_successful_campaign_cas_does_not_retain_candidate_after_live_source_moves` (4126) |
| E4 | Generation cannot self-authorize. | Candidate excludes generation; accepted W02 publication promotes it (`dramaturg.py:329–408, 1180–1325`) | `test_generated_dramaturg_candidate_has_no_self_authorizing_generation` (3373); rejected publication no promotion (4110) |
| E5 | Planning cannot leak through catch-up/Narrator or mutate native history. | Fixed planning route, no native-history writer; TurnRuntime vocabulary at `turn_runtime.py:15` | `test_raw_horizon_cannot_enter_narrator_commentator_or_catchup_contracts` (4010); Story validation does not mutate history (3514); rejected Dramaturg write does not mutate history (2565) |

### T07E — 2026-09-29 exact-size Senior resolution

| ID | Separately stated condition | Owner evidence | Test evidence |
|---|---|---|---|
| S1 | Exact per-path UTF-8 size uses the same serializer as `create_tree`. | `GAME/TOOLS/runtime_host.py:99–113, 645–688` | `test_measure_path_operations_uses_create_tree_utf8_serializer_without_writes` (RuntimeHost:531) |
| S2 | Missing/incomplete/invalid measurement fails closed before publication. | `runtime_host.py:653–688`; `dramaturg.py:1373–1404` | `test_missing_w02_size_capability_fails_closed_before_publication` (RD13:3565); `test_measurement_fails_closed_if_transport_lacks_exact_serializer_capability` (RuntimeHost:578); `test_review_band_candidate_is_measured_and_withheld_without_owner_outcome` (RD13:3579) |
| S3 | Review-band publication defers absent an ephemeral trusted outcome bound to candidate, route, base and size. | `dramaturg.py:421–508, 1405–1434`; no persisted outcome | Same candidate approval (RD13:3623); candidate transfer rejected (3733); changed measure invalidates outcome (3779); binding test (3824); model-shaped review rejected (3885) |
| S4 | No hard cap or new partition route. | Two fixed routes (`dramaturg.py:124–135`); size bands remain guidance (`106–108, 411–418`) | Partition-band approval without hard cap (RD13:3965); fixed-route assertion (3397) |
| S5 | W02 accepted outcome and publication transaction semantics are unchanged. | Measurement is separate (`runtime_host.py:645–688`); normal owner delta remains (`dramaturg.py:1436–1459`) | Measurement performs no writes (RuntimeHost:531); exact one create-tree/ref-read/commit/update sequence (RD13:3623) |

## Integrated version impact and verification

The inspected projections match the recorded Version Impact Gate: History module `1.0.5`; T0 basis schema `2`; Story module `1.0.8`; Story unit schemas TRANSCRIPT/EVENTS/MECHANICS/NARRATIVE `2/4/4/3`; Story projection-state schema `4`; E-EVT semantic generation `2`; Commentator control/snapshot schemas `2`; Context Runtime `1.0.9`; Dramaturg horizon schema `2`; RuntimeHost `1.0.11`. Native-history schemas and `runtime.semantic_event` outer schema remain `1`. Campaign-contract generation `2`, storage generation `3`, catalog generation `2`, engine release, migration and dual-read are unchanged/NONE. The recorded source set is current execution status lines 9, 33–35 and 582–592; module constants/schema owners were inspected directly.

Reviewer verification command:

```text
PYTHONDONTWRITEBYTECODE=1 .hdm-devtools/venv/bin/python -B -m unittest DEV.TESTS.test_rd13_story_t0_commentator DEV.TESTS.test_rd11_context_runtime DEV.TESTS.test_runtime_host_composition
224 passed
```

This was a focused integration run, not a full DEV rerun. The exact-candidate full DEV result remains **1411 passed, 5 skipped, 4 failed**, with all four S6D/A26-02 nodes reproduced sequentially and separate from T07; clean package provenance, the 18-test version/provenance/current-progress suite and maintenance audit passed. Hosted CI was unavailable in this local runtime and is not claimed.

## Gate disposition

T07-INTEGRATION is **PASS**. No T07 integration finding remains. The qualifications above remain explicit: T07A’s cited recovery test is not a process-kill test for every interruption point; T07B has no dedicated same-payload LOCAL/LIVE deduplication test and no positive source-classified omission-admission path; and T07D-P0 has no separate persistence-attempt test for its result. These limits do not change the accepted task contracts or create an integration finding. A26-02 remains separate.

The stable Wave-04 plan’s T08A inputs are T04B, T02C and T07-INTEGRATION. T04B and T02C were already accepted through the T05C dependency chain; with this PASS, T08A is now the next authorized lane. T08A remains limited to collaboration/multiplayer integration tests and its bounded Wave-05 MULTIPLAYER delta; do not edit `GAME/CORE/MULTIPLAYER.md`.
