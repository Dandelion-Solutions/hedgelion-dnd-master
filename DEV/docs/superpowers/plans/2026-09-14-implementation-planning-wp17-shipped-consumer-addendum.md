# HDM Implementation Planning — WP-17 Shipped Collaboration Consumer Cutover Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR OVERLAY — EXECUTION NOT AUTHORIZED**
Date: 2026-09-14
Production implementation authorized: **NO**.

This overlay repairs a post-SIRR2 author finding in RD-12. Canonical WP-17 machine-realization debt item 11 requires shipped CORE/session prose alignment. The current RD-12 plan realizes obligation/IntentClause/PLAYER/handoff/recovery/catch-up semantics but ends with a stale-search only; it names no executable shipped consumer cutover.

A stale-search is evidence discovery, not an implementation action. This overlay makes the consumer cutover explicit without transferring collaboration authority to prose modules.

## 1. Exact consumer surfaces

Mandatory shipped prose surfaces:

```text
GAME/CORE/MULTIPLAYER.md
GAME/CORE/SESSION.md
DEV/TESTS/test_rd12_collaboration.py
```

Protected negative surface:

```text
GAME/SCHEMA/session.schema.yaml
```

The session schema remains session coordination/recovery metadata. Do not add collaboration obligation bodies, participant barriers, input queues, collaboration frontiers or collaboration authority to session state. Exact obligation recovery routes through current PLAYER companion -> direct obligation read.

## 2. Shared MULTIPLAYER.md writer coordination

`GAME/CORE/MULTIPLAYER.md` is already a shared shipped consumer in the SIRR2 RD-09 cutover for WP-15/WP-16. Do not perform a second independent stale-based edit.

Use one shared-file checkpoint:

```text
RD-09/WP-16 LIVE/access requirements
+ RD-08/WP-15 chronology consumer requirements
+ RD-12/WP-17 collaboration consumer requirements
-> fresh current MULTIPLAYER.md bytes
-> one coherent physical file edit
-> all three owner test families green
```

This is `SHARED_FILE_CHECKPOINT`, not semantic serialization of RD-08/RD-09/RD-12 owner-local implementation. Their runtime work may proceed independently until this consumer join.

The SIRR2 planned module target remains `framework_module_version: 1.0.8` only when all currently planned WP-15/WP-16/WP-17 changes are included in that one unpublished logical rearchitecture edit. If an earlier material `MULTIPLAYER.md` edit has already been published by execution currentness, the normal version owner requires another local revision rather than reusing `1.0.8`.

## 3. RED — ShippedCollaborationProjectionTests

Create this class only at this checkpoint under the package checkpoint-coherence law.

Required RED cases against current shipped guidance:

```text
test_multiplayer_distinguishes_three_coordination_families
test_multiplayer_copresence_or_absence_does_not_create_global_wait
test_multiplayer_collective_dependency_routes_to_exact_obligation_generation
test_multiplayer_rule_owned_ordered_work_stays_with_native_owner
test_session_recovery_starts_from_player_route_companion_not_session_barrier
test_session_or_chat_state_cannot_close_or_satisfy_collaboration
test_closed_obligation_recovery_preserves_frozen_input_fingerprint
test_shipped_guidance_never_uses_transcript_or_message_arrival_as_collaboration_authority
test_session_schema_contains_no_collaboration_authority
test_rd09_live_and_rd08_chronology_cutovers_survive_shared_file_edit
```

Focused RED command:

```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.ShippedCollaborationProjectionTests -v
```

Do not publish RED-only state.

## 4. GREEN — MULTIPLAYER.md collaboration projection

In the shared file checkpoint, make shipped multiplayer guidance consume WP-17 without replacing its owner:

1. State the coordination family split exactly as `INDEPENDENT_IMMEDIATE | AGENCY_DEPENDENT_COLLECTIVE | RULE_OWNED_ORDERED`.
2. Co-presence, scene membership, disconnect, silence, timeout, message age or possible interest never create a global waiting barrier or satisfy voluntary agency.
3. An independently durable agency-dependent collective dependency routes through exact current `runtime.collaboration_obligation` identity/generation. Required contributors are bounded/material; optional contributor silence never blocks.
4. Existing Procedure/Continuation/Choice/Reaction responder/order semantics remain with those native owners; multiplayer guidance must not mirror them into a generic collaboration queue.
5. Accepted collaboration input is the immutable Interaction/IntentPlan clause semantic unit; transcript/message presence or arrival order is not collaboration input identity or fictional chronology.
6. Held actionable intent has no RuntimeCommand until explicit successful close/handoff releases the original Step-3 clause path.
7. PLAYER collaboration route refs are completeness-protected routing companions only. They do not satisfy/close/authorize an obligation.
8. Waiting exposes the maximal safe/visible native-owner frontier and blocks only the positively dependent scope; unrelated world/process work may continue.
9. Join/rejoin starts from current principal/PLAYER/control, exact route refs and recipient-safe catch-up; no global obligation scan and no private-input leakage.
10. Preserve all current SIRR2 typed LIVE claim/currentness/revocation and WP-15 sparse chronology requirements from the same fresh file. Collaboration prose must not resurrect scene-wide LIVE authority or global/local chronology frontiers.

## 5. GREEN — SESSION.md collaboration recovery projection

Reconcile shipped session guidance so a session/chat never becomes collaboration authority:

- session start/resume may use current PLAYER route refs to nominate exact nonterminal obligations relevant to the current player;
- each nominated obligation is dereferenced and revalidated against its exact generation, underlying current opportunity, authorization and accepted input refs;
- no matching route ref on an exact completeness-valid current PLAYER may terminate ordinary obligation lookup for that player; do not scan all collaboration records;
- OPEN remains open until owner rules satisfy it; CLOSED recovery preserves the frozen input-set fingerprint and retries the owner handoff rather than recollecting/reordering agency;
- RESOLVED/OBSOLETE route refs are absent after the coherent campaign-domain closure;
- chat/session pause, end, disconnect, timeout or inactivity cannot close/satisfy/obsolete a collaboration obligation or synthesize PASS/READY;
- session transcript/message arrival is evidence at most and cannot become collaboration semantic input identity;
- session recovery never reruns accepted mechanics/fixed RNG/Continuation from stale collaboration metadata;
- `SESSION.md` may orient the runtime to the exact RD-12 recovery path but stores no new collaboration owner/frontier/queue.

## 6. Verification

Required commands before the shared consumer checkpoint is published:

```bash
python3 -m unittest DEV.TESTS.test_rd12_collaboration.ShippedCollaborationProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd12_collaboration.PublicationRecoveryTests DEV.TESTS.test_rd12_collaboration.JoinRejoinCatchUpTests DEV.TESTS.test_rd12_collaboration.ScopeLocalProgressTests DEV.TESTS.test_rd12_collaboration.CloseHandoffTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.MultiplayerCoreCutoverTests -v
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalMachineAlignmentTests -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Expected: PASS. Focused collaboration GREEN cannot publish over a stale WP-15/WP-16 `MULTIPLAYER.md` consumer or vice versa.

## 7. Version impact

Planning edit itself: `VERSION_IMPACT: NONE`.

Future shipped edit:

```text
GAME/CORE/SESSION.md
  framework_module_version: 1.0.1 -> 1.0.2

GAME/CORE/MULTIPLAYER.md
  use the SIRR2 coordinated target 1.0.8 only if the WP-15/WP-16/WP-17 cutover is one unpublished material logical edit;
  otherwise increment from the then-current module revision exactly once.

GAME/SCHEMA/session.schema.yaml
  no collaboration-driven schema bump; protect its nonauthority role.
```

No campaign contract/storage generation bump is created solely by these shipped prose projections.

## 8. Lossless proof supersession

For R083/WP-17 proof routes, add `ShippedCollaborationProjectionTests` as a required supporting witness for:

```text
item 7  join/rejoin recovers current obligations without global scan
item 18 maximal safe/visible frontier before waiting
item 19 absence is neither consent nor immunity
item 20 timeout/presence/heartbeat/message age never closes voluntary agency dependency
item 22 recipient-safe catch-up/private-input containment
item 25 OPEN/CLOSED/RESOLVED/OBSOLETE recovery through exact routes
item 26 stale collaboration metadata never replays/rerolls accepted mechanics
```

R083 closure also requires canonical WP-17 machine-debt item 11 to be dispositioned by this exact shipped consumer checkpoint. Semantic scenario tests alone are insufficient while contradictory or incomplete active shipped guidance remains.

## 9. Scope

This overlay changes no collaboration semantics, readiness identity, RD count or owner. It converts known canonical shipped-consumer debt into an executable cutover and coordinates one already-shared physical file.

```text
SEMANTIC_OWNER_CHANGE: NONE
READINESS_ID_CHANGE: NONE
ARCHITECTURE_REOPEN_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
