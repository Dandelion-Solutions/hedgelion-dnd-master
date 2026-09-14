# HDM Implementation Planning — Post-Graph Proof Witness Matrix

Status: **CURRENT MANDATORY PROOF AMENDMENT — PLANNING ONLY**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 22 — SIGNIFICANT**, extended through Finding 26.
Production implementation: **NO**.

This matrix amends `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md`. A post-WP27 row is not planned-closed unless its exact mechanism, executable witness and primary proof channel are all present.

| Row | Exact mechanism / join | Exact planned witness | Primary channel |
|---|---|---|---|
| PG06 | temporal route producer + campaign/LIVE publication + recovery reconstruction | `TemporalRoutingCompletenessTests`; RD-06 `PublicationPlanTests`/`PublicationOutcomeTests` temporal coherence cases; RD-09 `LivePublicationTests` temporal-route cases; RD-07 `CurrentSourceSelectionTests` + `AcceptedExecutionRecoveryTests` | INTEGRATION_SCENARIO |
| PG07 | safe additive decision + exhaustive live-birth table + forward-only multi-LIVE transition | `LiveAdditiveAuthorizationTests`; `SourceNativeIdentityTests`; `MultiLiveForwardTransitionTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO |
| PG08 | exact world family reconciliation / no independent faction | RD-16 `WorldFamilyCensusTests`; `SharedCatalogIntegrationTests`; `R018WorldFamilyProofTests` | STATIC_AUDIT + INTEGRATION_SCENARIO |
| PG09 | completeness-protected principal route -> exact PLAYER reload | `PrincipalPlayerRouteCompanionTests`; RD-09 `PrincipalAuthorizationTests` extended with route/current-owner cases | INTEGRATION_SCENARIO |
| PG10 | MechanicalEvent composite identity `(segment_id,event_ordinal)` + allocator exclusion | RD-05 `AcceptedIdentityTests` + `LifecycleEvidenceTests`; RD-16 `SharedCatalogIntegrationTests`; `CampaignAllocatorTests` | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG11 | same-context catalog bind / unsupported evidence / publication-recovery seam | RD-15 `CatalogContextBindingTests`, `CatalogCandidateValidationTests`, `CatalogGapReportTests`, `CatalogBindingCurrentnessTests`, `CatalogBindingIntegrationTests` | INTEGRATION_SCENARIO |
| PG12 | strict 17-family world schemas and fail-closed wrapper | RD-16 `WorldStateSchemaCoverageTests`, `WorldFamilyCensusTests`, `WorldEnvelopeDispatchTests`, `DefinitionBindingModeTests` | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG13 | one final writer for shared catalog/admission/identifier generation | RD-16 `SharedCatalogIntegrationTests` plus existing catalog conformance suite | INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG14 | shipped CORE adjudication cannot bypass catalog bind | RD-15 `CatalogBindingInstructionCutoverTests` + `CatalogCandidateValidationTests` | STATIC_AUDIT + INTEGRATION_SCENARIO |
| PG15 | package router reaches all current base RDs / mandatory routes | `PostGraphPackageRoutingProofTests` in package proof target | STATIC_AUDIT |
| PG16 | one native PLAYER record key, no nested competing identity | RD-16 `WorldPlayerNativeIdentityTests` created/activated in PLAYER integration task | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG17 | RD-15/RD-16 checkpoint coherence | `PostGraphCheckpointCoherenceProofTests` + recorded maintenance-audit/full-discovery evidence at each future publishable checkpoint | STATIC_AUDIT + HOSTED_CI |
| PG18 | RD-15 SUPPORTED basis required for catalog-backed RD-05 acceptance | RD-15 `CatalogBackedAcceptanceIntegrationTests` created in final seam task; RD-05 acceptance negative cases | INTEGRATION_SCENARIO |
| PG19 | current coverage uses 16-RD / 17+17 graph and preserves historical accounting | `PostGraphCoverageCurrentnessProofTests` | STATIC_AUDIT |
| PG20 | current proof router requires RD-15/RD-16 for R018 and routes PG rows | `PostGraphProofRoutingTests` | STATIC_AUDIT |
| PG21 | current execution graph is acyclic and routes all RD-01..RD-16 joins | `PostGraphExecutionGraphProofTests` | STATIC_AUDIT |
| PG23 | one reconstructive accepted `CatalogContextBasis` survives bind -> accepted execution -> durability/retention -> exact recovery; unpublished session-only dependency cannot be stranded | RD-15 `CatalogContextBasisContractTests` + `CatalogGapContextEvidenceTests`; RD-05 `AcceptedExecutionCatalogBasisTests`; RD-06 `CatalogDependencyDurabilityTests`; RD-07 `CatalogBasisRecoveryTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG24 | CAS-owned source-local ordinal + injective `framed_base32hex_v1` freezes SOURCE_NATIVE_LIVE IDs at accepted creation and preserves them through ambiguity/recovery/absorption; F25/F26 provide the corrected campaign source key and multi-creation ordering | RD-09 `SourceNativeLiveIdEncodingTests`, `LiveSourceCreationCursorTests`, `SourceNativeAmbiguousPublicationTests`, `LiveSourceNativeSchemaCutoverTests`; RD-16 `SourceNativeIdentifierPolicyIntegrationTests`; RD-07 `SourceNativeLiveRecoveryTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG25 | semantic campaign identity is canonical `campaign_id`; WP-11 physical LIVE campaign route component is derived `c1-<sha256>` and verified against LIVE envelope identity; post-init campaign identity cannot drift | RD-14 `CreationIdentityTests` / `GeneratorScaffoldTests` campaign-ID cases; RD-06 `CampaignIdentityImmutabilityTests`; RD-09 `LiveCampaignRouteIdentityTests` + corrected `SourceNativeLiveIdEncodingTests`; RD-07 `SelectedLiveCampaignIdentityRecoveryTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG26 | deterministic attempt-local source-native creation normalization maps owner-provided per-family deterministic sequences to exact slot/ordinal/ID allocation and preserves original frozen allocation across indeterminate reconciliation | RD-09 `SourceNativeCreationOrderingTests`, `SourceNativeAmbiguousPublicationTests`, `SourceNativeLiveIdEncodingTests`; RD-07 `SourceNativeLiveRecoveryTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |

`PG22` is intentionally not a separate semantic-mechanism row: Finding 22 is the proof-routing rule realized by this matrix itself. Its closure is tested by `PostGraphProofRoutingTests`, which must fail if any PG semantic row lacks an exact witness or primary channel.

## Witness placement

Proof-only classes `PostGraphPackageRoutingProofTests`, `PostGraphCheckpointCoherenceProofTests`, `PostGraphCoverageCurrentnessProofTests`, `PostGraphProofRoutingTests`, and `PostGraphExecutionGraphProofTests` belong in the package proof target `DEV/TESTS/test_implementation_proof_ledger.py` when implementation/proof execution is authorized.

`WorldPlayerNativeIdentityTests` belongs to RD-16 Task 3 and must obey Finding 17 checkpoint timing. `CatalogBackedAcceptanceIntegrationTests` belongs to RD-15 final integration task and likewise is not materialized early.

Finding-23 executable witnesses are owner-local rather than proof-only:

- RD-15 `CatalogContextBasisContractTests` and `CatalogGapContextEvidenceTests` are created in the RD-15 task that materializes the basis/gap-evidence GREEN;
- RD-05 `AcceptedExecutionCatalogBasisTests` is created with the catalog-backed acceptance/basis propagation GREEN;
- RD-06 `CatalogDependencyDurabilityTests` is created with the durability/protection join GREEN;
- RD-07 `CatalogBasisRecoveryTests` is created with exact reconstruction/recovery GREEN.

Finding-24/25/26 executable witnesses are also owner-local:

- RD-14 extends `CreationIdentityTests` / `GeneratorScaffoldTests` with canonical `campaign_id` propagation and no-second-campaign-identity cases when F25 creation work is implemented;
- RD-06 creates `CampaignIdentityImmutabilityTests` with the ordinary-publication protected-field GREEN;
- RD-09 creates `LiveCampaignRouteIdentityTests` with F25 route/body identity GREEN, `SourceNativeCreationOrderingTests` with F26 normalization GREEN, `SourceNativeLiveIdEncodingTests` with the corrected canonical-campaign frame GREEN, `LiveSourceCreationCursorTests` with cursor/CAS allocation GREEN, `SourceNativeAmbiguousPublicationTests` with exact frozen-allocation ambiguity reconciliation GREEN, and `LiveSourceNativeSchemaCutoverTests` with final v1 LIVE schema GREEN;
- RD-16 creates `SourceNativeIdentifierPolicyIntegrationTests` only in the shared identifier-policy integration task;
- RD-07 creates `SelectedLiveCampaignIdentityRecoveryTests` and extends `SourceNativeLiveRecoveryTests` only with the corresponding selected-LIVE recovery GREEN.

None is pre-created as a future-task failing class.

## Exact negative requirements

- PG15 fails if any current RD or mandatory overlay is reachable only through commit-history archaeology.
- PG16 fails if native PLAYER identity can diverge between envelope and state/projection.
- PG17 fails if any publishable checkpoint contains an intentional future-task RED or uses skip/disable as a substitute for choreography.
- PG18 fails if a catalog-backed RuntimeCommand can be accepted with absent/mismatched RD-15 binding basis; native non-catalog transitions are not forced through a fake catalog path.
- PG19/PG20/PG21 fail on stale 14-RD current claims, inconsistent family census, missing RD-15/RD-16 proof join, missing routed current authority, or a hard-edge cycle.
- PG23 fails on fingerprint-only retry basis, command/resolution/continuation basis divergence, ambient/current/latest definition rebinding, missing retained dependency treated as recoverable, durable dependence on unpublished session-only definition, dropped retention evidence, or gap evidence reinterpreted under a newer context.
- PG24 fails if any SOURCE_NATIVE_LIVE family can use campaign allocator fallback, mutable ref/time in its semantic ID, unversioned/non-injective printable encoding, accepted ID rekey at absorption, ordinal reuse/wrap, allocation before resolving an indeterminate prior attempt, generic provisional->compaction rekey baseline, or recovery from directory/index order rather than exact source evidence.
- PG25 fails if semantic source-native identity uses the physical campaign route token instead of canonical `campaign_id`, raw unconstrained campaign bytes become a Git ref component, a second persisted semantic `campaign_technical_id` can drift, ordinary publication can rewrite MANIFEST campaign identity, or recovery trusts token equality without LIVE-body identity validation.
- PG26 fails if allocation order can depend on unordered container iteration, final ID, payload/hash, serialization order, wall clock or randomness; if ambiguous owner-local order is silently enumerated; if OWNER_EQUIVALENT/FORBIDDEN families consume cursor slots; or if an indeterminate prior attempt can allocate a second range before reconciliation.

No row may be discharged by test-name existence alone. Production implementation remains unauthorized.
