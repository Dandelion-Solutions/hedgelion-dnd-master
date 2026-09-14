# HDM Implementation Planning — Post-Graph Proof Witness Matrix

Status: **CURRENT MANDATORY PROOF AMENDMENT — PLANNING ONLY**
Date: 2026-09-14
Finding: **AUTHOR FINDING 22 — SIGNIFICANT**
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

## Witness placement

Proof-only classes `PostGraphPackageRoutingProofTests`, `PostGraphCheckpointCoherenceProofTests`, `PostGraphCoverageCurrentnessProofTests`, `PostGraphProofRoutingTests`, and `PostGraphExecutionGraphProofTests` belong in the package proof target `DEV/TESTS/test_implementation_proof_ledger.py` when implementation/proof execution is authorized.

`WorldPlayerNativeIdentityTests` belongs to RD-16 Task 3 and must obey Finding 17 checkpoint timing. `CatalogBackedAcceptanceIntegrationTests` belongs to RD-15 final integration task and likewise is not materialized early.

## Exact negative requirements

- PG15 fails if any current RD or mandatory overlay is reachable only through commit-history archaeology.
- PG16 fails if native PLAYER identity can diverge between envelope and state/projection.
- PG17 fails if any publishable checkpoint contains an intentional future-task RED or uses skip/disable as a substitute for choreography.
- PG18 fails if a catalog-backed RuntimeCommand can be accepted with absent/mismatched RD-15 binding basis; native non-catalog transitions are not forced through a fake catalog path.
- PG19/PG20/PG21 fail on stale 14-RD current claims, inconsistent family census, missing RD-15/RD-16 proof join, or a hard-edge cycle.

No row may be discharged by test-name existence alone. Production implementation remains unauthorized.
