# HDM v1 Implementation Wave 04 — Collaboration, Context and Story

Status: **PLANNED / DEPENDENCY-GATED — MANDATORY CLS↔HDM PREFLIGHT STOP BEFORE W04.T07 RED**

Goal: realize multiplayer collaboration over the current PLAYER/access-policy view, integrate bounded Context and protected emission, and publish Story/T0/Commentator/Dramaturg projections from native history without creating secondary authority.

Use `implementation-plan-execution-contract.md`. Every projection reloads and validates its native sources; every collaboration transition uses one after-authority view.

## Entry and exit

Entry requires the applicable owner checkpoints from Wave 01, deterministic publication/recovery from Wave 02 and principal/LIVE/access checkpoints from Wave 03. Exit requires obligation lineage, publication/recovery, context/privacy, role protection and Story history/currentness to join without cycles or duplicate owners.

Minimum wave impact envelope:

- owners: collaboration obligation/input/progress/close, multiplayer join/rejoin/catch-up, Context result, protected role emission, native history, T0, Story, Commentator and Dramaturg;
- consumers: PLAYER strict state, runtime families, session/multiplayer shipped instructions, bootstrap and final proof;
- protected invariants: collaboration is not authorization authority, Context/Story are not gameplay truth, catch-up is recipient-safe, and history is never reconstructed from narration;
- shared targets: `GAME/CORE/MULTIPLAYER.md`, player schema and shared catalogs wait for Wave-05 final writers.

## Baseline file-action and interface manifest

| Lane | Direct action paths | Shared/final paths |
|---|---|---|
| collaboration | `NEW_CREATE GAME/TOOLS/collaboration.py`, `GAME/SCHEMA/collaboration_obligation.schema.yaml`, `DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json`, `collaboration-closed-basis.schema.json`, `collaboration-handoff.schema.json`, `collaboration-frontier.schema.json`, `catch-up-projection.schema.json`; modify `DEV/SCHEMAS/intent-clause.schema.json`; extend `DEV/TESTS/test_rd12_collaboration.py` | player/LIVE schemas, shared machine and `MULTIPLAYER.md` integrate at W05 |
| Context | modify the Wave-01 `GAME/TOOLS/context_runtime.py`, `context_budget.py`, Context schemas and `DEV/TESTS/test_rd11_context_runtime.py`; inspect current state/scene/index as routed inputs | retained schemas and CORE projections integrate at W05 |
| protected emission | modify the Wave-01 `turn_runtime.py`, `emission.py`, typed handoff schemas and `DEV/TESTS/test_rd10_role_emission.py` | `AI_REASONING`, `RUNTIME` and `PLAY_POLICY` final bytes integrate at W05 |
| history/Story | modify the Wave-01 history/Story/Commentator/Dramaturg modules and schemas, Story/Dramaturg roots and `DEV/TESTS/test_rd13_story_t0_commentator.py` | event schema, manifest selector and shipped CORE/product consumers integrate at W05 |

Required callable boundary:

```text
classify_coordination_dependency(...) / open_or_successor_obligation(...)
associate_input(...) / close_collection(...) / handoff_closed_collection(...) / obsolete_generation(...)
required_route_holders(...) / reconcile_player_route_companions(...)
recover_obligations_for_player(...) / resolve_waiting(...)
compute_maximal_safe_frontier(...) / build_join_frontier(...) / build_catch_up(...)
reconcile_collaboration_for_player_access_transition(...)
reconcile_collaboration_for_access_policy_transition(...)
load_semantic_event(...) / publish_story_projection(...)
resolve_story_projection_state_path(...) / resolve_story_unit_path(...)
materialize_story_event(...) / materialize_story_narrative(...)
build_commentator_control_projection(...) / build_commentator_snapshot(...)
filter_commentator_request(...) / reconstruct_commentary(...) / refresh_commentator_control(...)
project_shared_dramaturg_horizon(...) / project_player_dramaturg_horizon(...)
prepare_dramaturg_publication(...) / reconcile_dramaturg_publication(...)
promote_accepted_dramaturg_generation(...) / invalidate_dramaturg_horizon(...)
build_dramaturg_candidate(...) / classify_dramaturg_admission(...)
```

## W04.T01 — Collaboration admission, obligation lineage and input association

Hard inputs: `W03_PRINCIPAL_PLAYER_ROUTE_READY`, current PLAYER state and the accepted collaboration owner.

Implement:

- typed coordination admission against exact current participant authority;
- obligation identity and lineage from accepted coordination intent;
- intent-clause collaboration semantics;
- exact input-to-obligation association;
- scope-local progress with no global active-player or universal pending queue;
- deterministic rejection of stale, duplicate, unauthorized, cross-scope or ambiguous input.

TDD and verification:

- use `DEV/TESTS/test_rd12_collaboration.py`;
- retain `CoordinationAdmissionTests`, `ObligationLineageTests`, `IntentClauseCollaborationTests`, `PlayerRouteCompanionTests`, `InputAssociationTests` and `ScopeLocalProgressTests`;
- prove candidate PLAYER IDs are reloaded/revalidated and a login alone cannot admit input.

Output checkpoint: `W04_COLLABORATION_ADMISSION_READY`.

## W04.T02 — Close handoff, publication, recovery and catch-up

Hard inputs: W04.T01, `W02_DURABILITY_PUBLICATION_READY`, `W02_EXACT_RECOVERY_READY` and current LIVE routing where applicable.

Implement:

- exact close handoff from completed obligation to the owning execution/temporal path;
- idempotent collaboration publication within the campaign closure;
- cold recovery of open obligations and associated inputs;
- join/rejoin catch-up derived from native history/current PLAYER/access state;
- recipient-safe catch-up and typed incomplete-currentness failure;
- composite bridge evidence without making collaboration a mechanical/history authority.

TDD and verification:

- retain `CloseHandoffTests`, `PublicationRecoveryTests`, `JoinRejoinCatchUpTests`, `CompositeBridgeTests` and `ShippedCollaborationProjectionTests`;
- cover interruption before/after publish, duplicate close, stale participant, removed/revoked access and missing history source.

Output checkpoint: `W04_COLLABORATION_PUBLICATION_READY`.

## W04.T03 — PLAYER route references and strict collaboration state

Implement the collaboration-owned delta to strict `world.player` and runtime state:

- route references use the principal route companion and exact PLAYER identity;
- PLAYER carries only its accepted native binding/status/state, not a duplicate membership registry;
- collaboration obligation references are exact and scoped;
- no `MANIFEST.players.player_ids` fallback or generic-index authorization path exists;
- missing references fail closed and route to repair/recovery.

TDD and verification:

- turn `PlayerCollaborationStrictStateIntegrationTests` GREEN in `DEV/TESTS/test_rd16_world_family_machine_integration.py` after owner-local collaboration tests pass;
- include static schema/reference checks and current-state behavioral reload checks;
- publish a bounded player-schema delta for Wave 05, not a competing physical edit.

Output checkpoint: `W04_PLAYER_COLLABORATION_DELTA_READY`.

## W04.T04 — Authority and access-policy reconciliation

Hard input: `W03_ACCESS_POLICY_TRANSITION_READY` plus W04.T01–T02.

For every accepted PLAYER or campaign-access mutation:

1. load the same exact after-authority view used by publication;
2. enumerate the bounded affected collaboration obligations;
3. reconcile each obligation exactly once;
4. preserve already accepted historical mechanics while applying prospective eligibility;
5. publish authority and collaboration effects in one campaign closure;
6. recover to the same view after interruption.

No reverse dependency allows collaboration to grant authority. Missing or stale route/currentness fails closed.

TDD and verification:

- use `PlayerAuthorityCollaborationReconciliationTests` and `AccessPolicyCollaborationReconciliationTests`;
- cover deactivation, reactivation, grant revocation, join-policy change, creator uncertainty, duplicate reconciliation and crash boundaries.

Output checkpoint: `W04_AUTHORITY_COLLABORATION_RECONCILED`.

## W04.T05 — Bounded Context integration

Hard inputs: `W01_CONTEXT_OWNER_READY`, current information/knowledge, history, PLAYER, LIVE/scene and collaboration sources.

Integrate Context Runtime:

- discover only bounded eligible candidates through owner routes;
- close all required packets before allocating optional capacity;
- rank optional material deterministically within the declared budget;
- preserve recipient/privacy/knowledge scope;
- emit a trace of selected and rejected inputs without making that trace authority;
- retrospective context reloads native history and current permission rather than trusting old projection bytes.

TDD and verification:

- complete `RequiredPacketClosureTests`, `ContextAllocationTests`, `OptionalRankingTests`, `RetrospectiveContextTests`, `ContextResultTraceTests` and `ScopedContextJoinTests` with integrated sources;
- prove no unbounded scan, no hidden required-packet eviction, no leakage and no stale LIVE/PLAYER acceptance.

Output checkpoint: `W04_CONTEXT_INTEGRATION_READY`.

## W04.T06 — Protected role and emission integration

Hard inputs: `W02_PROTECTED_EXECUTION_HANDOFF_READY` and `W04_CONTEXT_INTEGRATION_READY`.

Integrate role results, Context packets, tools, diagnostics, collaboration inputs and private material through one protected turn envelope. Capacity handling and auxiliary fallback must be deterministic, preserve accepted mechanics, and expose only permitted recipient material.

TDD and verification:

- complete all six role classes in `DEV/TESTS/test_rd10_role_emission.py` with integrated Context/collaboration cases;
- include malformed/untyped handoff, over-capacity, tool error, private diagnostic and auxiliary-fallback negatives;
- prove one instruction owner and no side-channel public emission.

Output checkpoint: `W04_PROTECTED_EMISSION_READY`.

## W04.T07 — Native history, T0, Story, Commentator and Dramaturg integration

Hard inputs: `W01_HISTORY_STORY_OWNER_READY`, deterministic publication/recovery, current information/knowledge, temporal and PLAYER/LIVE authority.

### Mandatory CLS <-> HDM preflight before the first RED step

This gate is intentionally narrow. It protects the public Story/T0/Commentator integration boundary without making private CLS repair debt a global HDM blocker.

Immediately before W04.T07 implementation starts, fresh-read and record exact refs/blobs for:

```text
PUBLIC HDM
  DEV/docs/superpowers/specs/2026-09-09-story-commentator-self-contained-corpus-owner-decision.md
  the current Story baseline/source/version owners routed by that decision and the current task Source Manifest

PRIVATE CLS
  dkolyada/hedgelion-dnd-master-lab@audit/cls-project-audit-workspace
    CLS-AUDIT/CURRENT_AUDIT_STATE.md
    CLS-AUDIT/graph/HDM_INTEGRATION_GRAPH.md

  dkolyada/hedgelion-dnd-master-lab@feature/commentator-language-stack
    HDM-CLS/docs/SENIOR_AUDITOR_HDM_INTEGRATION_HANDOFF.md
    HDM-CLS/docs/CURRENT_PROGRESS.md
```

Preflight classification:

```text
PASS_TO_IMPLEMENT
  no current CLS/audit finding requires a new or changed public-HDM semantic owner,
  persisted/wire contract, Story/T0/control meaning, authority transfer or incompatible
  source/version law for W04.T07.

PRIVATE_CLS_REPAIR_DEBT_ONLY
  findings are confined to private CLS SQLite/read-model/lifecycle/query/performance
  realization while preserving current public owners -> does NOT block W04.T07.

SYSTEM_IMPACT_GATE
  a current finding/accepted CLS architecture requires a new or changed public-HDM
  owner/semantic/persisted/interface contract, or conflicts with the current SCC/Story
  owner -> stop before RED and publish the exact conflict/current refs for reconciliation.

PREFLIGHT_UNAVAILABLE
  the required current private CLS evidence cannot be fresh-read -> do not guess; stop
  only W04.T07 until the cross-project evidence route is available.
```

The preflight does **not** require all CLS `Rxx` code repairs to be closed, does not require WP12-03+ activation, and does not require the REAL CLS reader to already exist. It checks only whether current public HDM semantics/owners remain sufficient for the Story/T0/Commentator producer work about to begin.

Record the disposition and exact refs in W04.T07 execution evidence. A later private CLS implementation bug is not retroactively an HDM semantic defect unless its accepted repair actually changes this public boundary.

Implement the complete projection chain:

```text
accepted SemanticEvent/native history
-> explicit T0 historical basis
-> current Story projection
-> recipient-safe Commentator packet
-> bounded Dramaturg horizon/admission/rebase
```

Required laws:

- history identity/provenance and semantic order survive publication/recovery;
- T0 is a materialized, reconstructible basis, not an invented summary;
- Story selection uses its bounded physical route and validates native sources;
- Commentator is self-contained for its allowed audience and cannot disclose hidden knowledge;
- Dramaturg output is advice/projection; accepted native events alone change history;
- rebasing rejects stale or incompatible horizons rather than silently merging narration.

TDD and verification:

- complete every class in `DEV/TESTS/test_rd13_story_t0_commentator.py`;
- cover publication interruption, stale Story, changed knowledge/permission, T0 reconstruction, private-source exclusion and Dramaturg rebase conflict.

Output checkpoints: `W04_NATIVE_HISTORY_PUBLICATION_READY`, `W04_T0_STORY_READY` and `W04_COMMENTATOR_DRAMATURG_READY`.

## W04.T08 — Multiplayer and session consumer deltas

Prepare the final shipped-consumer deltas:

- join/rejoin follows principal route -> candidate PLAYER IDs -> exact current PLAYER revalidation;
- catch-up consumes current collaboration/history/access projections;
- multiplayer never searches `PLAYER_INDEX` or scans PLAYER records for authorization;
- session handoff retains exact campaign/LIVE/current PLAYER identities and does not become their authority;
- user-facing invitations and participant selection use current GitHub login; stable account ID remains the stored binding.

TDD and verification:

- extend `ShippedCollaborationProjectionTests` and the applicable principal/LIVE cutover tests;
- emit one bounded `MULTIPLAYER` delta for `CORE_MULTIPLAYER_FINAL_INTEGRATION_READY` and a session delta for the Wave-05 module/version writer.

Output checkpoint: `W04_MULTIPLAYER_SESSION_DELTAS_READY`.

## Wave 04 completion evidence

Record exact after-authority reconciliation traces, obligation publication/recovery fixtures, recipient/privacy proofs, bounded Context evidence, protected-emission cases and history/Story/T0 reconstruction. The wave closes only when collaboration, Context and Story remain consumers/projections of native authority through interruption and rejoin.
