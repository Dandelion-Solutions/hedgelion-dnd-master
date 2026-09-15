# HDM Implementation Planning — Post-Graph Proof Witness Matrix

Status: **CURRENT MANDATORY PROOF AMENDMENT — PLANNING ONLY**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 22 — SIGNIFICANT**, extended through Finding 31, with F58/PG35 operational-root integration.
Production implementation: **NO**.

This matrix amends `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md`. A post-WP27 row is not planned-closed unless its exact mechanism, executable witness and primary proof channel are all present.

| Row | Exact mechanism / join | Exact planned witness | Primary channel |
|---|---|---|---|
| PG06 | temporal route producer + campaign/LIVE publication + recovery reconstruction | `TemporalRoutingCompletenessTests`; RD-06 publication temporal-coherence cases; RD-09 LIVE temporal-route cases; RD-07 recovery cases | INTEGRATION_SCENARIO |
| PG07 | safe additive decision + exhaustive live-birth table + forward-only multi-LIVE transition | `LiveAdditiveAuthorizationTests`; `SourceNativeIdentityTests`; `MultiLiveForwardTransitionTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO |
| PG08 | exact world family reconciliation / no independent faction | RD-16 `WorldFamilyCensusTests`; `SharedCatalogIntegrationTests`; `R018WorldFamilyProofTests` | STATIC_AUDIT + INTEGRATION_SCENARIO |
| PG09 | completeness-protected principal route -> exact PLAYER reload | `PrincipalPlayerRouteCompanionTests`; RD-09 principal route/current-owner cases | INTEGRATION_SCENARIO |
| PG10 | MechanicalEvent composite identity `(segment_id,event_ordinal)` + allocator exclusion | RD-05 identity/lifecycle tests; RD-16 shared integration; `CampaignAllocatorTests` | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG11 | same-context catalog bind / unsupported evidence / publication-recovery seam | RD-15 catalog-context/binding/gap/currentness/integration tests | INTEGRATION_SCENARIO |
| PG12 | strict 17-family world schemas and fail-closed wrapper | RD-16 schema/census/dispatch/binding tests | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG13 | one final writer for shared catalog/admission/identifier generation | RD-16 `SharedCatalogIntegrationTests` plus current catalog conformance suite | INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG14 | shipped CORE adjudication cannot bypass catalog bind | RD-15 `CatalogBindingInstructionCutoverTests` + candidate validation | STATIC_AUDIT + INTEGRATION_SCENARIO |
| PG15 | package router reaches all current base RDs / mandatory routes | `PostGraphPackageRoutingProofTests` | STATIC_AUDIT |
| PG16 | one native PLAYER record key, no nested competing identity | RD-16 `WorldPlayerNativeIdentityTests` | FOCUSED_BEHAVIOR + STATIC_AUDIT |
| PG17 | RD-15/RD-16 checkpoint coherence | `PostGraphCheckpointCoherenceProofTests` + maintenance/full-discovery evidence | STATIC_AUDIT + HOSTED_CI |
| PG18 | RD-15 SUPPORTED basis required for catalog-backed RD-05 acceptance | RD-15 `CatalogBackedAcceptanceIntegrationTests`; RD-05 acceptance negatives | INTEGRATION_SCENARIO |
| PG19 | current coverage uses 16-RD / 17+17 graph and preserves historical accounting | `PostGraphCoverageCurrentnessProofTests` | STATIC_AUDIT |
| PG20 | current proof router requires RD-15/RD-16 for R018 and routes PG rows | `PostGraphProofRoutingTests` | STATIC_AUDIT |
| PG21 | current execution graph is acyclic and routes RD-01..RD-16 joins | `PostGraphExecutionGraphProofTests` | STATIC_AUDIT |
| PG23 | reconstructive accepted `CatalogContextBasis` survives bind -> accepted execution -> durability -> exact recovery | RD-15 basis tests; RD-05 accepted basis tests; RD-06 durability tests; RD-07 recovery tests | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG24 | CAS-owned source-local ordinal + injective `framed_base32hex_v1` freezes SOURCE_NATIVE_LIVE IDs and preserves them through recovery/absorption | RD-09 ID/cursor/ambiguity/schema tests; RD-16 identifier-policy integration; RD-07 source-native recovery | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG25 | semantic campaign identity is canonical `campaign_id`; physical campaign token is derived/validated and campaign identity cannot drift | RD-14 creation/scaffold cases; RD-06 immutability; RD-09 campaign-route identity; RD-07 selected-LIVE campaign identity recovery | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG26 | deterministic attempt-local multiple-creation normalization -> exact slot/ordinal/ID allocation | RD-09 creation-order/ambiguity/encoding tests; RD-07 source-native recovery | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO |
| PG27 | exact immutable opening basis -> canonical epoch identity + bounded scene route token + full route/body validation | RD-09 `LiveEpochRouteIdentityTests`; RD-06 route-selection validation; RD-07 selected-LIVE recovery | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG28 | deterministic candidate preparation is idempotent and acknowledgement-aware | RD-09 `LiveOpeningPreparationTests` | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO |
| PG29 | exact pinned campaign `H` -> initial LIVE native-state seed equivalence | RD-09 `LiveOpeningSeedTests`; RD-06 seed-validation selection cases | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO |
| PG30 | completeness-protected `STATE/RUNTIME/LIVE_ROUTING.yaml` -> bounded `WriteAuthorityLookup` + coherent publication/recovery/scaffold | RD-09 `LiveRoutingCompletenessTests`; RD-06 route-table publication cases; RD-07 recovery; RD-14 scaffold | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG31 | typed LIVE native-state packing -> exact recovery -> deterministic lossless/idempotent forward absorption | RD-09 `LiveNativeStatePackingTests` + `LiveAbsorptionMaterializationTests`; RD-06 publication join; RD-07 recovery; RD-16 strict-family validation | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO + STATIC_AUDIT |
| PG35 | F58 native lifecycle/promise -> active-only operational membership -> campaign/LIVE acceptance and handoff -> complete pinned cold recovery -> generated scaffold/final projections | `test_rd05_runtime_execution.OperationalRootEnrollmentTests`; `test_rd06_durability_publication.OperationalRootPublicationTests`; `test_rd09_access_live.LiveOperationalRootHandoffTests`; `test_rd07_recovery.OperationalRootRoutingContractTests` + `OperationalRootRecoveryTests`; RD-14 `BlankScaffoldCompletenessTests`; final README/CORE witnesses at the exact modules/channels in overlay 37 | INTEGRATION_SCENARIO (primary); FOCUSED_BEHAVIOR and STATIC_AUDIT sub-obligations |

PG32–PG34 remain the logical item-bound rows introduced by mandatory overlays 23–25 (F34 runtime-family closure, F35 PLAYER collaboration integration and F36 temporal handoff). PG35 does not reuse those identities.

`PG22` is not a separate semantic-mechanism row. Finding 22 is the exact-witness routing rule embodied by this matrix and closed by `PostGraphProofRoutingTests` only when every semantic PG row has a named witness/channel.

## Witness placement

Proof-only classes `PostGraphPackageRoutingProofTests`, `PostGraphCheckpointCoherenceProofTests`, `PostGraphCoverageCurrentnessProofTests`, `PostGraphProofRoutingTests`, and `PostGraphExecutionGraphProofTests` belong in `DEV/TESTS/test_implementation_proof_ledger.py` only when implementation/proof execution is authorized.

Owner-local witness classes are created only in the task that owns their RED-to-GREEN mechanism. In particular, Findings 28–31 add `LiveOpeningPreparationTests`, `LiveOpeningSeedTests`, `LiveRoutingCompletenessTests`, `LiveNativeStatePackingTests` and `LiveAbsorptionMaterializationTests` only with their corresponding mechanisms/integration joins. No future-task failing class is pre-created.

## Exact negative requirements

- PG15–PG21 fail on stale package routing/accounting, missing current owners/joins, checkpoint incoherence or a hard-edge cycle.
- PG23 fails on fingerprint-only retry basis, basis divergence, ambient/current/latest rebinding, or stranded accepted definition dependencies.
- PG24–PG27 fail on campaign allocator fallback, accepted-ID rekey, ambiguous reallocation, stale semantic/physical identity mixing, non-deterministic multi-creation order, incomplete opening identity, or route/body mismatch.
- PG28 fails if prepared-source existence establishes authority, equivalent retry creates a second logical epoch, incompatible deterministic candidate is silently accepted, or an uncertain opening is not reconciled before retry.
- PG29 fails if existing claims are seeded from mixed revisions, owner-defined partition seed is incomplete, or `EPOCH_LOCAL_CREATION` fabricates an owner during opening.
- PG30 fails if scene/current/index/ref absence proves campaign authority, if missing/stale routing is treated as empty, if selected-route/table coherence can split, or ordinary lookup depends on scanning LIVE refs.
- PG31 fails if LIVE packing changes semantic ownership, entry absence becomes generic deletion, live-born IDs change during absorption, campaign fallback is used while CLOSED_UNABSORBED remains selected, absorption duplicates accepted semantics after uncertainty, or route release is detached from the campaign-native successor truth for the same transfer.

- PG35 fails on an unproduced root set, active Procedure omitted after Command settlement, promised unresolved input omission, marker/partial listing mistaken for completeness, split owner/root publication, missing/duplicate current handoff domain, historical-runtime scan as ordinary discovery, or proof before actual producer/integration/generated/final projection targets. Exact module/class placement and task-local RED/GREEN order are mandatory under overlay 37.

No row may be discharged by test-name existence alone. Production implementation remains unauthorized.
