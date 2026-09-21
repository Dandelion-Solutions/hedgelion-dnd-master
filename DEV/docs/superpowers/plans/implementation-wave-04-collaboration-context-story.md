# HDM v1 Implementation Wave 04 — Collaboration, Context and Story

Status: **CURRENT / WAVE 04 EXECUTION AUTHORIZED — MANDATORY CLS↔HDM PREFLIGHT STOP BEFORE W04.T07 RED**

Goal: realize multiplayer collaboration over the current PLAYER/access-policy view, integrate bounded Context and protected emission, and publish Story/T0/Commentator/Dramaturg projections from native history without creating secondary authority.

Use `implementation-plan-execution-contract.md`. Every projection reloads and validates its native sources; every collaboration transition uses one after-authority view.

## Entry and exit

Entry requires the applicable owner checkpoints from Wave 01, deterministic publication/recovery from Wave 02 and principal/LIVE/access checkpoints from Wave 03. Exit requires obligation lineage, publication/recovery, context/privacy, role protection and Story history/currentness to join without cycles or duplicate owners.

Minimum wave impact envelope:

- owners: collaboration obligation/input/progress/close, multiplayer join/rejoin/catch-up, Context result, protected role emission, native history, T0, Story, Commentator and Dramaturg;
- consumers: PLAYER strict state, runtime families, session/multiplayer shipped instructions, bootstrap and final proof;
- protected invariants: collaboration is not authorization authority, Context/Story are not gameplay truth, catch-up is recipient-safe, and history is never reconstructed from narration;
- shared targets: `GAME/CORE/MULTIPLAYER.md`, player schema and shared catalogs wait for Wave-05 final writers.


## Execution decomposition and parallel schedule

This section is the executable decomposition of W04.T01-T08. The numbered task sections below remain the semantic coverage owners; the subtask checkpoints here are the units that receive workers, independent review and publication. A later subtask never inherits trust merely because an earlier typed object exists: every authority/currentness boundary is revalidated at the consuming owner.

### Source manifest for execution

Mandatory semantic owners for this wave include:

- R2.5 plus WP-17 collaboration/agency-safe progression;
- R2.3 plus WP-09 Context Runtime realization;
- R2.4 plus WP-08 role/context/instruction realization;
- WP-18 Story/Dramaturg, the Story producer/persistence contract, the eight baseline Story projection source registrations and PO-009 self-contained Commentator owner decision;
- Step-5 publication/recovery/session/disclosure owners when their exact boundary is consumed;
- Wave-03 accepted principal/PLAYER, LIVE/currentness, access-policy and creator-history checkpoints;
- Wave-05 as the single final writer for shared PLAYER/LIVE schemas, shared catalogs and shipped CORE/session/multiplayer integration.

Before a worker mutates production code it fresh-reads the exact owners named by its row below plus the current consumer tests. Do not recursively preload unrelated architecture.

### Cross-wave protected boundaries

- Wave 03 is a closed producer. W04 collaboration consumes the accepted W03 access transition and after-authority view; it does not conveniently patch GAME/TOOLS/access_control.py or LIVE authority. A required W03 interface change is a System-Impact Gate.
- Collaboration owns collection/current generation only. It cannot grant authorization, synthesize a RuntimeCommand, establish fictional chronology, copy truth/knowledge/disclosure authority, or use timeout/presence as correctness evidence.
- Context remains an ephemeral projection. Discovery hints and caller fields such as current=true / eligible=true are never sufficient material authority; routed owner currentness and eligibility must be resolved before role-local semantic use.
- TurnEnvelope/phase results remain control, not authority. Narrator emission must consume an accepted Context basis and accepted deterministic handoff; matching bundle_id, recipient strings or a shaped bundle alone cannot widen eligibility/disclosure.
- Story and Commentator are projections. Shaped SemanticEvent/Story/control mappings cannot mint native history, currentness or access. Commentator filtering is deterministic and pre-materialization; content basis and access/control basis remain separately current.
- Dramaturg horizons are noncanonical planning. Their source basis and generation are fenced; no horizon or rebase may promote future facts into native history.
- W04 does not physically edit GAME/CORE/MULTIPLAYER.md, GAME/CORE/AI_REASONING.md, GAME/CORE/RUNTIME.md, GAME/CORE/PLAY_POLICY.md, GAME/CORE/SESSION.md, the retained shared PLAYER/scene/event schemas, or shared catalog/identifier-policy bytes. W04 produces bounded owner-local deltas for the Wave-05 final writers.
- The mandatory CLS-HDM preflight is performed immediately before the first W04.T07A RED. A planning-time CLS read is only scheduling evidence and never substitutes for that gate.

### Reviewer and publication discipline

Each row below is a coherent reviewer gate. The worker uses RED -> expected RED -> minimal GREEN -> focused verification -> Version Impact Gate -> coherent commit -> non-force publication -> remote read-back. An independent hdm-reviewer starts immediately after publication. A dependent row is READY only after the producer reviewer PASS is durably recorded.

Ordinary reviewer findings are repaired inside the same row family. A System-Impact finding stops only the affected lane. Independent lanes continue.

Do not run two workers concurrently when they write the same production file or the same primary test file, even if their semantic topics differ. Version-bearing shared metadata is also a write owner: before dispatch, the coordinator reserves any required shared version projection. If a worker discovers that a global version namespace must change unexpectedly, it reports VERSION_SYNC_REQUIRED before editing another active task's shared version owner; publication is serialized and freshly reverified.

### Executable dependency graph

    Wave-04 entry
      |-- SHARED HOST-COMPOSITION PREREQUISITE
      |   T00H runtime host composition
      |     |-> T01A coordination admission
      |     |-> T05A routed currentness + eligibility admission
      |     +-> T07A accepted native history (after T07-PREFLIGHT)
      |
      |-- COLLABORATION LANE
      |   T01A coordination admission
      |     -> T01B lineage/input association
      |     -> T01C safe-frontier/currentness
      |          |-> T02A explicit close + frozen handoff
      |          |    -> T02B publication/recovery
      |          |         -> T02C join/rejoin catch-up
      |          |              -> T04A after-authority reconciliation
      |          |                   -> T04B same-closure recovery
      |          |
      |          +-> T03A PLAYER strict-state delta (parallel with T02*)
      |
      |-- CONTEXT / EMISSION LANE
      |   T05A routed currentness + eligibility admission
      |     -> T05B required closure / allocation / retrospective core
      |          + T04B
      |          -> T05C collaboration-aware Context join
      |               -> T06A phase rebind + accepted Context basis
      |                    -> T06B protected Narrator emission
      |
      |-- STORY / COMMENTATOR LANE
      |   T07-PREFLIGHT (coordinator gate immediately before first RED)
      |     -> T07A accepted native history publication/recovery
      |     -> T07B eight Story source registrations + layer codecs/coverage
      |     -> T07C Story-local T0 + Story currentness/publication
      |     -> T07D Commentator control/snapshot anti-oracle currentness
      |     -> T07E Dramaturg admission/publication/rebase
      |     -> T07-INTEGRATION reviewer gate
      |
      |-- FINAL CONSUMER JOIN
          T04B + T02C + T07-INTEGRATION -> T08A multiplayer/catch-up delta
          T06B                         -> T08B session identity/handoff delta
          T08A + T08B + T03A           -> T08C consumer convergence
          T08C + all lane checkpoints  -> Wave-04 FINAL_REVIEW

### Shared host-composition prerequisite - W04.T00H

**W04.T00H - campaign-bound runtime host composition**

Input: current accepted W01-W03 owner surfaces plus the accepted
`2026-09-21-w04-runtime-host-ordering-route-owner-decision.md`.

Direct writes: create `GAME/TOOLS/runtime_host.py`,
`DEV/TESTS/test_runtime_host_composition.py` and one bounded Wave-05 bootstrap
delta/evidence artifact. No persisted schema.

Outputs: `W04_RUNTIME_HOST_COMPOSITION_READY` and
`W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY`.

Required behavior:

- one host/root is bound to one selected campaign;
- authenticated RepositoryPort and selected-LIVE transport enter only at the
  infrastructure composition boundary;
- Context, History and native-ordering are sibling bound services;
- public/gameplay calls cannot supply or replace repository/LIVE/route/service
  capabilities;
- root re-pins/revalidates per operation and is not a lease;
- no local token/registry/marker is used to authenticate arbitrary in-process
  Python objects;
- arbitrary Python mutation inside the trusted deterministic runtime is outside
  the gameplay attacker model; an unsupported deployment allowing untrusted
  code in that TCB must isolate it rather than weaken owner semantics.

Mandatory REDs: capability override through a domain API rejected; cross-campaign
root use rejected; stale pin not reused as currentness; no Context->History trust
dependency; no persistence/serialization of host capabilities.

### Collaboration lane - W04.T01-T04

**W04.T01A - coordination-family admission and exact participant authority**

Inputs: `W04_RUNTIME_HOST_COMPOSITION_READY`, W03 principal route/current PLAYER and accepted Interaction/IntentPlan owners.

Direct writes: create GAME/TOOLS/collaboration.py, extend the Step-3 owner machine in GAME/TOOLS/runtime_execution.py only for owner-native ordered-evidence production, DEV/TESTS/test_rd12_collaboration.py, base collaboration obligation DEV/GAME schemas, and the collaboration fields in DEV/SCHEMAS/intent-clause.schema.json. Do not add ordering authority to GAME/TOOLS/mechanics.py.

Output: W04_COLLAB_COORDINATION_ADMISSION_READY.

Mandatory REDs: caller cannot self-select coordination family, required contributors or currentness; login alone cannot authorize; positive RULE_OWNED_ORDERED requires an exact current Resolution in AWAITING_CHOICE/AWAITING_REACTION plus its exact Continuation generation/pending ChoiceRequest or ReactionOffer, with ACTIVE Procedure validation when linked; Procedure existence alone is insufficient; stale/mismatched ordered refs fail closed; independent input creates no obligation; mechanical value.contribution remains a separate vocabulary.

**W04.T01B - obligation lineage, contributor semantics, input association and route companions**

Input: T01A reviewer PASS. Same collaboration production/test lane.

Output: W04_COLLAB_LINEAGE_INPUT_READY.

Mandatory REDs: exact human input identity is (interaction_id, clause_id); obligation stores references rather than copied transcript/prose authority; optional silence cannot block; old generation cannot mutate successor; identity-defining generation semantics are immutable; PLAYER route companion is complete but cannot grant authority or omit required holders.

**W04.T01C - maximal safe frontier and scope-local currentness**

Input: T01B reviewer PASS. Same collaboration production/test lane plus collaboration-frontier schema.

Output: original W04_COLLABORATION_ADMISSION_READY.

Mandatory REDs: technical arrival/CAS/generation order is not fictional chronology; timeout/presence/silence cannot close; unrelated scopes continue; visible consequence cannot cross the same safe frontier as semantic mutation.

**W04.T02A - explicit close, frozen input basis and handoff**

Inputs: T01C PASS plus accepted W02 execution owner. Same collaboration production/test lane plus collaboration-closed-basis and collaboration-handoff schemas.

Output: W04_COLLAB_CLOSE_HANDOFF_READY.

Mandatory REDs: close requires exact current generation; closed input set fingerprint is deterministic and order-independent; held ACTIONABLE_INTENT remains pre-command until handoff; collaboration never synthesizes a RuntimeCommand; duplicate input is idempotent; late input never replays accepted mechanics.

**W04.T02B - publication/recovery and route-companion closure**

Inputs: T02A PASS plus W02 publication/recovery. Same collaboration production/test lane and owner-local persistence contract inputs only.

Output: W04_COLLAB_DURABILITY_RECOVERY_READY.

Mandatory REDs: no collaboration index/global directory scan; exact known-ID recovery; OPEN/CLOSED/RESOLVED/OBSOLETE recovery; CAS rejection/ambiguity fail closed; route companion joins the same campaign closure; LIVE dependency creates neither 2PC nor a LIVE collaboration owner; recovery never rerolls/replays mechanics.

**W04.T02C - join/rejoin and recipient-safe catch-up**

Inputs: T02B PASS plus current W03 access/LIVE routes. Same collaboration owner/test plus catch-up projection schema.

Output: original W04_COLLABORATION_PUBLICATION_READY.

Mandatory REDs: current binding/routing precedes mutable input; another participant's private input content is absent; planning-only material is absent; stale/deactivated access fails closed; a cursor does not prove human consumption.

**W04.T03A - strict PLAYER collaboration delta**

Input: T01C PASS. This row may run in parallel with T02A-T02C because it does not write collaboration.py/test_rd12.

Direct writes: DEV/TESTS/test_rd16_world_family_machine_integration.py plus a bounded owner-local Wave-05 delta record. Do not edit the physical shared PLAYER schema.

Output: W04_PLAYER_COLLABORATION_DELTA_READY.

Mandatory REDs: no MANIFEST.players.player_ids or generic-index authorization fallback; missing route refs fail closed; collaboration references remain scoped and non-authoritative.

**W04.T04A - exact after-authority reconciliation**

Inputs: complete T02C plus W03 access-policy checkpoint.

Direct writes: collaboration owner/test only; W03 access owner is a read-only producer.

Output: W04_AUTHORITY_COLLAB_RECONCILIATION_READY.

Mandatory REDs: collaboration cannot grant or recover authorization; deactivation/reactivation/grant revocation/join-policy changes apply prospectively; creator uncertainty fails closed; only the bounded affected obligation set is reconciled.

**W04.T04B - same-closure authority/collaboration publication and recovery**

Input: T04A PASS. Same collaboration production/test lane.

Output: original W04_AUTHORITY_COLLABORATION_RECONCILED.

Mandatory REDs: duplicate reconciliation idempotent; crash before/after publication; campaign/body drift; stale obligation generation; recovery reproduces the same after-authority view; no reverse dependency into access control.

### Context and protected-emission lane - W04.T05-T06

**W04.T05A - owner-routed Context currentness and eligibility admission**

Inputs: `W04_RUNTIME_HOST_COMPOSITION_READY`, W01 Context owner plus W03 information/PLAYER/LIVE/currentness owners.

Direct writes: GAME/TOOLS/context_runtime.py, applicable Context schemas and DEV/TESTS/test_rd11_context_runtime.py.

Output: W04_CONTEXT_CURRENTNESS_ELIGIBILITY_READY.

The current scaffold's current=true and eligible=true fields may survive only as internal post-resolution carrier data; they are never caller authority.

Mandatory REDs: no gameplay/domain API accepts RepositoryPort/LIVE/runtime/service override; forged current/eligible booleans, index/cache/scene presence, stale LIVE/PLAYER, wrong registered role/purpose/profile/recipient and physical co-presence cannot admit semantic material.

**W04.T05B - typed required closure, allocation and retrospective core**

Input: T05A PASS.

Direct writes: context_runtime.py, GAME/TOOLS/context_budget.py, Context schemas and test_rd11.

Output: W04_CONTEXT_CORE_READY.

Mandatory REDs: required floors cannot be evicted by optional content; no arbitrary graph/history scan; caller-supplied size rejected; deterministic optional ordering; UNSATISFIABLE is terminal; trace/private routing material is not role evidence; retrospective source escalation revalidates native evidence.

**W04.T05C - collaboration-aware scoped Context join**

Inputs: T05B plus T04B and T02C.

Direct writes: Context owner/test only; collaboration/access/history owners are read-only producers.

Output: original W04_CONTEXT_INTEGRATION_READY.

Mandatory REDs: stale obligation after an access mutation rejected; another player's private contribution excluded; recipient/profile/frontier mismatch rejected; retrospective context revalidates current permission instead of trusting old projection bytes.

**W04.T06A - phase rebind and accepted Context basis**

Inputs: T05C plus W02 protected execution handoff.

Direct writes: GAME/TOOLS/turn_runtime.py, turn/result schemas and DEV/TESTS/test_rd10_role_emission.py.

Output: W04_ROLE_CONTEXT_HANDOFF_READY.

Mandatory REDs: a shaped arbitrary bundle with matching bundle_id cannot widen eligibility; raw bundle/trace/private diagnostics rejected; Actor subject/purpose isolated; Narrator freshly rebinds after Chronicler; only minimum typed prior results cross phases.

**W04.T06B - protected Narrator emission and finite fallback**

Input: T06A PASS.

Direct writes: turn_runtime.py, GAME/TOOLS/emission.py, narration/turn schemas and test_rd10.

Output: original W04_PROTECTED_EMISSION_READY.

Mandatory REDs: emission requires accepted Context basis plus owner-verified ExecutionHandoff where applicable; disclosure cannot exceed eligible bundle; side-channel/internal role emission rejected; over-capacity fails safely; exactly one registered fallback; no mechanics/RNG replay.

### Story / Commentator / Dramaturg lane - W04.T07

W04.T07-PREFLIGHT is a coordinator gate, not a worker task. Immediately before T07A RED, fresh-read and record the exact public and private refs required by the T07 section below. Planning-time evidence currently indicates private-only CLS work and no public-HDM semantic change, but that is not the mandatory preflight result.

**W04.T07A - accepted native history publication/recovery**

Inputs: preflight PASS_TO_IMPLEMENT or PRIVATE_CLS_REPAIR_DEBT_ONLY, `W04_RUNTIME_HOST_COMPOSITION_READY`, plus W02 publication/recovery.

Direct writes: GAME/TOOLS/history.py, native-history schemas and DEV/TESTS/test_rd13_story_t0_commentator.py.

Output: W04_NATIVE_HISTORY_PUBLICATION_READY.

Mandatory REDs: no gameplay/domain API accepts RepositoryPort/LIVE/runtime/history-service override; caller-shaped SemanticEvent cannot mint accepted history; duplicate ID/evt-admission ordinal; provenance/currentness mismatch; incomplete source window cannot claim coverage; interruption/recovery preserves identity/origin/provenance/source enrollment; narration/Story cannot reconstruct native history; routed missing LIVE source never falls back to campaign.

**W04.T07B - all four Story layers and eight fixed source registrations**

Input: T07A PASS.

Direct writes: GAME/TOOLS/story.py, Story source/coverage schemas, same rd13 test file. Create the missing owner-local TRANSCRIPT unit machine contract and update EVENTS/MECHANICS/NARRATIVE owner-local contracts as required.

Required registrations: T-MSG, T-ARC, E-EVT, E-REL, M-SEG, M-OUT, N-EVT, N-REL.

Output: W04_STORY_SOURCE_CONTRACTS_READY.

Mandatory REDs: an EVENTS-only implementation is insufficient; MUST candidates cannot be dropped by importance; late historical relations independently cover EVENTS/NARRATIVE; M-OUT preserves terminal zero-change/failure; T-ARC exact promise remains distinct from T-MSG; LIVE origin absorption does not duplicate LOCAL candidates; coverage is domain/generation/cardinality specific and never one global scalar.

**W04.T07C - Story-local T0, exact Story currentness and publication**

Inputs: T07B plus PO-009.

Direct writes: history.py, story.py, T0/Story projection schemas and rd13.

Output: original W04_T0_STORY_READY.

Mandatory REDs: current T1 cannot substitute historical T0; every required retained WP-19 material T0 factor is Story-local recoverable; private/off-screen material stays retained but availability-filtered; stale native/Story basis rejected; Story cannot block or roll back canon.

**W04.T07D - Commentator self-contained control/snapshot and anti-oracle filtering**

Inputs: T07C plus current W03 information/access owners.

Direct writes: GAME/TOOLS/commentator.py, Commentator schemas and rd13.

Output: W04_COMMENTATOR_CONTROL_READY.

Mandatory REDs: arbitrary player-to-story-id mapping cannot mint eligibility; CONTENT_FINAL is not ACCESS_FINAL; changed permission/control basis refreshes even with unchanged content; IDs/counts/metadata of ineligible material do not reach model materialization; no native-only fallback for qualifying retained T0 factors.

**W04.T07E - Dramaturg source/generation admission, publication and rebase**

Input: T07C; execute after T07D in this shared test-file lane.

Direct writes: GAME/TOOLS/dramaturg.py, Dramaturg schemas and rd13.

Output: original W04_COMMENTATOR_DRAMATURG_READY.

Mandatory REDs: retained horizon is multiplayer-only; future/planning text is noncanonical; stale/incompatible source basis is discarded/reprepared rather than text-merged; generation cannot self-authorize; planning cannot leak through catch-up/Narrator or mutate native history.

After T07E reviewer PASS, run a T07-INTEGRATION independent review over T07A-T07E together. It must verify the whole accepted-native-evidence -> four Story layers/T0 -> Commentator filter -> Dramaturg chain has no reverse authority edge and that all persisted schema/version impacts are coherent.

### Final consumer join - W04.T08

**W04.T08A - multiplayer join/rejoin/catch-up delta**

Inputs: T04B + T02C + T07-INTEGRATION.

Direct writes: collaboration/multiplayer integration tests plus a bounded Wave-05 MULTIPLAYER delta record. Do not edit GAME/CORE/MULTIPLAYER.md.

Output: W04_MULTIPLAYER_CONSUMER_DELTA_READY.

Mandatory REDs: principal route -> candidate PLAYER IDs -> exact current PLAYER reload; no PLAYER_INDEX/scan authorization; catch-up uses current collaboration/history/access only; planning/private input excluded; login remains human selection/display while stable account ID is the binding.

**W04.T08B - session identity/currentness handoff delta**

Input: T06B plus accepted W03 campaign/LIVE/PLAYER currentness. May run in parallel with T08A.

Direct writes: session-focused tests plus a bounded Wave-05 SESSION delta record. Do not edit GAME/CORE/SESSION.md or the shared session schema.

Output: W04_SESSION_CONSUMER_DELTA_READY.

Mandatory REDs: session metadata cannot become campaign/LIVE/PLAYER authority; stale/relinquished host revalidates native sources; controlled handoff names exact durable/current source basis; no heartbeat/lease/no-op publication.

**W04.T08C - final consumer convergence**

Inputs: T08A + T08B + T03A.

Direct writes: task-local delta/evidence documents and integration tests only.

Output: original W04_MULTIPLAYER_SESSION_DELTAS_READY.

Verify no shared final-writer bytes changed, no scan/index authorization path, no planning leakage and all campaign/LIVE/PLAYER/currentness fields have one native owner.

### Safe concurrency schedule

Maximum configured worker capacity remains five, but maximum safe Wave-04 production concurrency is normally four because each semantic lane deliberately serializes a shared owner/test file. Do not fill the fifth slot with artificial work.

Recommended scheduler:

    START
      worker H: T00H runtime host composition
      -> local reviewer PASS / publish / read-back

    after T00H PASS
      worker C: T01A
      worker X: T05A
      coordinator: retain/recheck the recorded T07 preflight only if its semantic trigger fired
      worker S: T07A with the still-current preflight PASS
      => normally 3 production workers

    as lanes advance
      C serially T01A -> T01B -> T01C
      X serially T05A -> T05B
      S serially T07A -> T07B -> T07C -> T07D -> T07E

    after T01C PASS
      worker P: T03A in parallel
      C continues T02A -> T02B -> T02C -> T04A -> T04B
      => up to 4 production workers

    after T04B + T05B
      X -> T05C -> T06A -> T06B

    after T04B + T07 integration
      worker M: T08A
    after T06B
      worker H: T08B
      T08A and T08B may run in parallel

    T08A + T08B + T03A
      -> T08C
      -> exact-head Wave-04 verification
      -> mandatory Senior Wave-04 integration audit

Independent reviewers start as soon as each checkpoint publishes and do not consume the production-worker limit.

### Version-impact checkpoints

Perform the normal Version Impact Gate at every row. In addition, treat these as high-risk namespaces that must not be deferred to the end of the wave:

- T01A introduces a persistent collaboration family/schema; determine local schema and aggregate campaign-contract impact before its checkpoint.
- Any material change to intent-clause.schema.json is classified with its owning persisted Interaction/IntentPlan contract.
- T05/T06 ephemeral Context/Turn control must not become persistent for implementation convenience. If implementation pressure requires durable Context/trace/role-control state, stop at the System-Impact Gate.
- T07B-T07D concretely realize Story/PO-009 persisted machine contracts. Each changed Story/Commentator schema owns its local version impact; any breaking persistent-family change also evaluates campaign-contract generation and migration/adoption obligations immediately.
- T07E evaluates Dramaturg schema/version separately from Story content/control.
- T08 emits semantic deltas only; final shipped CORE/module version changes remain Wave-05-owned unless a current direct W04 owner is actually modified.


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

Final T05 closure hard inputs: `W01_CONTEXT_OWNER_READY`, current information/knowledge, history, PLAYER, LIVE/scene and collaboration sources. The decomposed T05A/T05B rows are explicitly authorized owner-local preparatory slices over the already-ready subset; they do not claim `W04_CONTEXT_INTEGRATION_READY`. T05C is the first row that requires the completed collaboration producer and closes the original T05 hard-input join.

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
