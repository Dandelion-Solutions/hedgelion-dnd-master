# HDM v1 Implementation Wave 03 — Principal, LIVE and Temporal Authority

Status: **CURRENT / WAVE 03 EXECUTION AUTHORIZED**

Goal: realize one exact principal-to-PLAYER authorization route, source-native LIVE identity/currentness/state, and lossless handoff among campaign, LIVE, temporal and operational roots.

Use `implementation-plan-execution-contract.md`. Prepared state, a route name, a login, an index entry or physical ordering never becomes authority.

## Entry and exit

Entry requires `W01_CAMPAIGN_IDENTITY_READY`, `W01_NATIVE_ROUTING_READY`, `W01_INFORMATION_OWNER_READY`, `W01_TEMPORAL_OWNER_READY`, `W02_DURABILITY_PUBLICATION_READY` and the applicable recovery checkpoints. Exit requires all identity encodings, route companions, CAS transitions, packing/absorption and access-policy publication paths to agree at one exact campaign closure.

Minimum wave impact envelope:

- owners: principal binding, PLAYER, campaign access policy, LIVE source/scene/epoch/currentness, LIVE routing companion and temporal handoff;
- consumers: multiplayer, collaboration, context/current scene, recovery, bootstrap, retained schemas and final 17+17 machine integration;
- protected invariants: stable account ID authorizes, login remains human-facing, creator uncertainty fails closed, prepared LIVE is not current, exact source CAS is required, and broad PLAYER/index scans are forbidden;
- shared files: `GAME/CORE/MULTIPLAYER.md`, `GAME/CORE/LIVE_SCENE.md`, scene/player schemas and shared READMEs wait for their Wave-05 final integration checkpoints.

## Baseline file-action and interface manifest

| Lane | Direct action paths | Shared/final paths |
|---|---|---|
| principal/access | `NEW_CREATE GAME/TOOLS/access_control.py`; create the fixed principal-routing companion contract and blank `GAME/CAMPAIGN/STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml`; extend `DEV/TESTS/test_rd09_access_live.py` | `GAME/SCHEMA/player.schema.yaml`, `world-player-state.schema.json`, manifest/scaffold and `GAME/CORE/MULTIPLAYER.md` integrate at W05 |
| LIVE owner | `NEW_CREATE GAME/TOOLS/live_state.py`, `DEV/SCHEMAS/live-publication-attempt.schema.json`, `live-routing.schema.json`; replace/modify `DEV/SCHEMAS/live-claim.schema.json`; create blank `GAME/CAMPAIGN/STATE/RUNTIME/LIVE_ROUTING.yaml`; extend `DEV/TESTS/test_rd09_access_live.py` | `GAME/SCHEMA/live_scene.schema.yaml`, scene schema, `GAME/CORE/LIVE_SCENE.md` and multiplayer bytes integrate at W05 |
| identifier policy | prepare owner delta to `DEV/CATALOG/identifier-policies.json` and `DEV/SCHEMAS/identifier-policies.schema.json`; extend allocator and world-machine tests | W05.T02 is the only shared catalog/identifier-policy writer |
| temporal/operational handoff | modify `GAME/TOOLS/live_state.py`, `GAME/TOOLS/temporal.py`, `GAME/TOOLS/recovery_roots.py` and their owner tests; use `STATE/RUNTIME/TEMPORAL_ROUTING.yaml`, `LIVE_ROUTING.yaml` and `RECOVERY_ROOTS/FORMAT.yaml` contracts | generated scaffold and shared storage/schema documentation integrate at W05 |

Required callable boundary:

```text
resolve_principal(...) / resolve_player(...) / authorize_operation(...)
lookup_write_authority(...) / select_live_source(...) / validate_exact_source(...)
freeze_live_attempt(...) / revalidate_application_authorization(...)
classify_cas_result(...) / reconcile_indeterminate(...)
extract_material_live_information(...) / apply_normalization_candidates_under_native_owners(...)
encode_live_campaign_route_token(...) / encode_live_scene_route_token(...) / derive_live_epoch_id(...)
encode_source_native_live_id(...) / parse_source_native_live_id(...) / normalize_source_native_creations(...)
validate_live_route_identity(...) / build_live_ref(...)
derive_temporal_route_entry(...) / resolve_temporal_dependency_dependents(...)
reconcile_temporal_route_membership(...) / rebuild_temporal_agenda_from_route(...)
classify_additive_authorization_change(...)
freeze_multi_live_forward_plan(...) / advance_multi_live_freeze(...) / publish_forward_transition(...)
freeze_player_access_transition(...) / freeze_access_policy_transition(...)
```

## W03.T01 — Principal-to-PLAYER authority route

Implement `STATE/RUNTIME/PRINCIPAL_PLAYER_ROUTING.yaml` as a completeness-protected derived route from verified stable GitHub account ID to candidate PLAYER identities. Every authorization read follows:

```text
verified stable account ID
-> route companion candidate PLAYER IDs
-> exact current PLAYER reload
-> binding/status/scope revalidation
-> authorized PLAYER or typed fail-closed result
```

Required laws:

- GitHub login is stored/displayed for selection, invitations and user comprehension;
- the verified stable account ID is the PLAYER binding authority;
- email is neither identity nor invitation authority;
- login rename is unsupported and cannot transfer creator or PLAYER authority;
- inactive bindings remain routable for a legitimate rejoin decision but never imply active authorization;
- missing/stale/incomplete route is a repair condition; generic `PLAYER_INDEX`, repository scans and first-match selection are forbidden for ordinary authorization.

TDD and verification:

- use `PrincipalAuthorizationTests` and `PrincipalPlayerRouteCompanionTests` in `DEV/TESTS/test_rd09_access_live.py`;
- cover exact success, stale candidate, duplicate/ambiguous binding, inactive rejoin candidate, login-only impersonation, creator uncertainty and absent route.

Output checkpoint: `W03_PRINCIPAL_PLAYER_ROUTE_READY`.

## W03.T02 — Base LIVE envelope, claim and exact currentness

Implement the strict LIVE source/scene envelope and currentness claim. The semantic source key is:

```text
LiveSourceKey = (campaign_id, scene_id, epoch_id)
```

Currentness is exact-source compare-and-swap evidence against the selected campaign/LIVE route. Candidate preparation, commit existence, newest timestamp, physical ref order and successful local write are not authority.

TDD and verification:

- use `LiveEnvelopeClaimTests`, `LiveCurrentnessTests`, `LivePublicationTests` and `LiveLifecycleTests` in `DEV/TESTS/test_rd09_access_live.py`;
- prove claim success, stale predecessor, parallel candidate, ambiguous acknowledgement, non-monotonic source and no latest-looking fallback.

Output checkpoint: `W03_LIVE_CURRENTNESS_READY`.

## W03.T03 — Campaign, scene, epoch and physical route identity

Hard input: W01.T10 campaign identity plus W02.T05 campaign-identity immutability.

Implement the exact encodings owned by the accepted LIVE/routing specifications:

- physical campaign route token: `c1-<full sha256(domain-separated length-framed UTF8 campaign_id)>`;
- versioned campaign/scene/epoch route components `c1`, `s1`, `e1` with their exact canonical encoders;
- exact body tuple verification against `(campaign_id, scene_id, epoch_id)` after every route load;
- collision/alias rejection and no truncation of the campaign digest;
- source identity remains semantic; the physical token is routing material only.

TDD and verification:

- use `LiveCampaignRouteIdentityTests`, `LiveEpochRouteIdentityTests` and `SceneLiveRouteProjectionTests`;
- cover Unicode UTF-8 framing, delimiter-like values, wrong body tuple, wrong version tag and near-collision cases.

Output checkpoint: `W03_LIVE_ROUTE_IDENTITY_READY`.

## W03.T04 — Source-native LIVE ID, ordering and cursor

Hard inputs: `W03_LIVE_ROUTE_IDENTITY_READY`, canonical campaign identity and the current source-native identifier owner.

Implement:

- source-native cursor type `uint64`;
- identifier encoding `framed_base32hex_v1`;
- deterministic multi-creation order by native-family UTF-8 byte order, then owner-local index;
- deterministic slot and ordinal assignment from that order;
- ID derivation that binds the exact source/campaign/scene/epoch and creation position;
- cursor advance only with the accepted exact-source CAS transition.

The generic entity allocator, wall time, random UUID, iteration order and a prepared candidate cannot allocate source-native LIVE identity.

TDD and verification:

- use `SourceNativeIdentityTests`, `SourceNativeLiveIdEncodingTests`, `LiveSourceCreationCursorTests`, `SourceNativeCreationOrderingTests` and `SourceNativeAmbiguousPublicationTests`;
- cover reordered inputs, duplicate owner-local index, cursor overflow, CAS loss and indeterminate acknowledgement reconciliation.

The shared identifier-policy machine is finalized once from all owner inputs before final LIVE identity proof. Cut `identifier-policies.schema_version` from 2 to 3 while retaining `catalog_generation = 2`. Every admitted family has one explicit `live_birth` disposition: `SOURCE_NATIVE_LIVE`, `OWNER_EQUIVALENT` or `FORBIDDEN`. Unknown/missing dispositions fail closed. `world.player`, runtime collaboration obligations, checkpoints, allocator, maintenance audit and catalog-gap reports are LIVE-forbidden; semantic composite families such as knowledge, intent/command/continuation, MechanicalEvent, resolution trace and disclosure retain owner-equivalent identity; the accepted independently creatable families use source-native identity. `CampaignAllocatorTests` proves none of the latter two groups falls back to campaign allocation.

The closed v1 disposition table is exact:

| Family | `live_birth` |
|---|---|
| world.actor | SOURCE_NATIVE_LIVE |
| world.actor_group | SOURCE_NATIVE_LIVE |
| world.asset | SOURCE_NATIVE_LIVE |
| world.location | SOURCE_NATIVE_LIVE |
| world.connection | SOURCE_NATIVE_LIVE |
| world.zone | SOURCE_NATIVE_LIVE |
| world.organization | SOURCE_NATIVE_LIVE |
| world.contract | SOURCE_NATIVE_LIVE |
| world.mission | SOURCE_NATIVE_LIVE |
| world.scene | SOURCE_NATIVE_LIVE |
| world.encounter | SOURCE_NATIVE_LIVE |
| world.hazard | SOURCE_NATIVE_LIVE |
| world.effect | SOURCE_NATIVE_LIVE |
| world.lore_fact | SOURCE_NATIVE_LIVE |
| world.knowledge | OWNER_EQUIVALENT |
| world.thread | SOURCE_NATIVE_LIVE |
| world.player | FORBIDDEN |
| runtime.session | FORBIDDEN |
| runtime.message | SOURCE_NATIVE_LIVE |
| runtime.interaction | SOURCE_NATIVE_LIVE |
| runtime.procedure | SOURCE_NATIVE_LIVE |
| runtime.intent_plan | OWNER_EQUIVALENT |
| runtime.command | OWNER_EQUIVALENT |
| runtime.resolution | SOURCE_NATIVE_LIVE |
| runtime.continuation | OWNER_EQUIVALENT |
| runtime.mechanical_event | OWNER_EQUIVALENT |
| runtime.semantic_event | SOURCE_NATIVE_LIVE |
| runtime.resolution_trace | OWNER_EQUIVALENT |
| runtime.disclosure | OWNER_EQUIVALENT |
| runtime.collaboration_obligation | FORBIDDEN |
| runtime.checkpoint | FORBIDDEN |
| runtime.id_allocator | FORBIDDEN |
| runtime.maintenance_audit | FORBIDDEN |
| runtime.catalog_gap_report | FORBIDDEN |

Identity capability does not itself grant creation. `SOURCE_NATIVE_LIVE` still requires an admitted immutable `EPOCH_LOCAL_CREATION(family)` claim plus owner-specific containment/currentness/authorization. `OWNER_EQUIVALENT` creates no surrogate ID. `FORBIDDEN` rejects LIVE birth. `world.player` is never a LIVE claim; `world.thread` additionally requires the selected mutation partition to contain its final scope.

Use `LiveSourceNativeSchemaCutoverTests` to prove the final cursor/canonical IDs, absence of provisional-to-durable rekey semantics and identity-preserving absorption. Wave 05 performs the one shared identifier-policy/catalog write and `SourceNativeIdentifierPolicyIntegrationTests` checks every row.

Output checkpoint: `W03_SOURCE_NATIVE_LIVE_ID_READY`.

## W03.T05 — Opening preparation, seed, routing, packing and absorption

Implement one idempotent opening pipeline:

```text
exact campaign/LIVE selection
-> opening preparation
-> source-native seed/materialization
-> exact CAS publication
-> completeness-protected LIVE route companion
-> lossless native-state packing
-> idempotent absorption into campaign state
```

Required laws:

- preparation is repeatable and distinguishable from accepted publication;
- opening seed contains all required native owner inputs and no implicit authority defaults;
- `STATE/RUNTIME/LIVE_ROUTING.yaml` is complete for accepted current LIVE roots and revalidates exact bodies;
- packing is lossless across all implicated owner families;
- absorption is idempotent and preserves native identities, provenance, knowledge/privacy, chronology, unresolved work and currentness;
- ambiguous publication is resolved by exact remote/source read, not by creating another opening.

TDD and verification:

- use `LiveOpeningPreparationTests`, `LiveOpeningSeedTests`, `LiveRoutingCompletenessTests`, `LiveNativeStatePackingTests`, `LiveAbsorptionMaterializationTests`, `SourceNativeLiveRecoveryTests` and `SelectedLiveCampaignIdentityRecoveryTests`;
- use `LiveClosedUnabsorbedTests` for successful source close followed by failed normalization, indeterminate campaign publication and later absorption from the same final source;
- include missing route member, extra stale route member, partial pack, double absorption and failed-CAS cases. A closed source remains `CLOSED_UNABSORBED` until phase-B campaign absorption succeeds; it never reopens or falls back to campaign base.

Output checkpoints: `W03_LIVE_ROUTING_READY`, `W03_LIVE_NATIVE_PACKING_READY` and `W03_LIVE_ABSORPTION_READY`.

## W03.T06 — Temporal and operational-root handoff

Hard inputs: Wave-01 temporal owner, Wave-02 operational-root recovery and W03.T05.

In the same accepted campaign closure:

- route every active LIVE temporal binding to its native temporal owner;
- preserve chronology/current-state/thread identities through campaign-to-LIVE and LIVE-to-campaign transitions;
- hand active operational roots into LIVE selection and back into campaign recovery;
- remove/replace only roots proven terminal or superseded by exact CAS;
- reject incomplete, stale or cross-campaign route companions.

No global clock, universal pending queue or LIVE-owned copy becomes temporal/operational authority.

TDD and verification:

- use `LiveTemporalRoutingHandoffTests` and `LiveOperationalRootHandoffTests`;
- turn the Wave-02 LIVE recovery joins GREEN;
- extend `TemporalRoutingCompletenessTests`, `TemporalExecutionRecoveryTests` and `ChronologyBridgeTests` with both handoff directions and interruption points.

Output checkpoints: `W03_TEMPORAL_LIVE_HANDOFF_READY` and `W03_OPERATIONAL_LIVE_HANDOFF_READY`.

## W03.T07 — PLAYER and campaign access-policy transitions

Implement typed exact-current mutations for the narrow accepted authority set:

- PLAYER binding/status transitions;
- creator-owned campaign mode and join-policy fields;
- accepted narrow PLAYER mechanical-override grants/revocations.

Required semantics:

- mutations validate exact current PLAYER/campaign authority through W03.T01;
- join-policy change does not revoke existing bindings;
- grant revocation is prospective and does not rewrite accepted historical mechanics;
- creator uncertainty fails closed;
- each mutation computes a complete bounded impact set for LIVE, collaboration, planning/catch-up and publication consumers;
- publication is one campaign closure; recovery reproduces the same after-authority view.

Classify additive activation/reactivation with six current-owner predicates: immutable claim sets unchanged; every existing writer's authorization unchanged; no affected controlled-PC transfer; no selected source revoked/invalidated; the new/reactivated PLAYER gains no LIVE write authority without reacquiring current obligations; and the campaign change publishes without changing selected LIVE routing/currentness. Only then return `NO_LIVE_ROLLOVER`; missing or false evidence returns `LIVE_TRANSITION_REQUIRED` and closes/freezes affected sources first.

For a transition spanning several LIVE sources, use an ephemeral `FrozenMultiLiveForwardPlan`: pin campaign and exact source revisions, close each source by its own CAS, retain every confirmed close as final, resolve stale/indeterminate sources, and publish the campaign forward transition only after all exact final revisions are proven. Already closed sources remain `CLOSED_UNABSORBED`; no rollback/reopen, 2PC, lease, leader or fictional chronology from technical CAS order is allowed. Recovery re-derives outstanding work from current campaign routes and exact source lifecycle.

TDD and verification:

- use `PlayerAccessTransitionTests`, `LiveAdditiveAuthorizationTests`, `MultiLiveForwardTransitionTests`, `CampaignAccessPolicyTransitionTests`, `AccessPolicyPublicationIntegrationTests`, `AccessPolicyConsumerIntegrationTests` and the existing static `HouseRulesPolicyAuthorityContractTests`;
- include stale currentness, lost authority, partial consumer update, rejoin and historical accepted-result negatives;
- include A-closed/B-stale, A-closed/B-indeterminate, all-closed/campaign-conflict, already-accepted-RNG and no-CAS-order-as-chronology multi-LIVE cases;
- W04.T04 owns the collaboration reconciliation join.

Output checkpoint: `W03_ACCESS_POLICY_TRANSITION_READY`.

## W03.T08 — Information, scene and shipped LIVE cutover

Integrate current LIVE with the information and scene owners without changing their authority:

- recipient-safe LIVE information normalization consumes `W01_INFORMATION_OWNER_READY`;
- material/current scene bridge uses exact LIVE currentness and rejects stale projection material;
- strict LIVE/source-native schema replaces obsolete pre-v1 shape;
- shipped `LIVE_SCENE` and multiplayer semantics point to source-native currentness and the principal route.

TDD and verification:

- use `LiveInformationNormalizationIntegrationTests`, `MaterialBridgeCurrentnessTests`, `SourceNativeLiveSchemaCutoverTests`, `ShippedLiveCoreCutoverTests` and `MultiplayerCoreCutoverTests`;
- keep physical `GAME/CORE/LIVE_SCENE.md`, `GAME/CORE/MULTIPLAYER.md` and scene schema edits owner-local until Wave-05 shared checkpoints.

Output checkpoint: `W03_LIVE_CONSUMER_DELTAS_READY`.

## Wave 03 completion evidence

Record canonical encoding vectors, exact route/body validation, CAS and ambiguous-ack traces, source-native cursor/order fixtures, principal/creator negative cases, lossless pack/absorption fixtures and campaign/LIVE handoff recovery. The wave closes only when no login, index, prepared state or physical order can substitute for stable identity and exact currentness.
