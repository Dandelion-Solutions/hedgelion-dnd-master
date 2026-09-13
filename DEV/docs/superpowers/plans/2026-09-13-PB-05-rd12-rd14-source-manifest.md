# PB-05 Source Manifest — RD-12..RD-14

Status: REPAIRED / SELF-REVIEWED
Baseline HEAD: `05edd81195ba22bbed1467ad2ab49b06061d4535`
Scope: planning only; production implementation is not authorized.

## Sources
Authorities: `DEV/CURRENT_PROGRESS.md`; critic-approved bounded decomposition v2; WP-27 Step-2 ledger/final readiness spec; R2.5 agency-safe collaboration final spec; `DEV/ARCHITECTURE/DECISIONS.md`; `DEV/ARCHITECTURE/DECISIONS_APPENDIX.md`; Multiplayer Model; current GAME/DEV machine inventory.
Excluded as authority: release packages, derivative summaries, trigger-gated/no-work leaves.

## RD-12 — collaboration / multiplayer
Direct: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146` (11).
Composite slices: `R016.COLLAB`, `R018.COLLAB`, `R122.COLLABORATION_BRIDGE`.
`R124` consumes RD-12 controlled-actor/multiplayer scope but completes in RD-11.

Laws: one authoritative world; no global active player; positive material dependency before scope-local waiting; join/rejoin current frontier before mutation; catch-up recipient projection only.

Topology: `NEW_CREATE GAME/TOOLS/collaboration.py`; `NEW_CREATE DEV/SCHEMAS/collaboration-request.schema.json`, `collaboration-frontier.schema.json`, `catch-up-projection.schema.json`; `INSPECT_ONLY GAME/SCHEMA/player.schema.yaml`, `live_scene.schema.yaml`.

## RD-13 — Story / T0 / Commentator / native history integration
Direct: `R022,R051,R084,R085,R099,R102,R131` (7).
Composite slices: `R016.STORY`, `R018.STORY`, `R062.SEMANTIC_EVENT_HISTORY`, `R087.SEMANTIC_EVENT_T0`.

Laws: Story is noncanonical projection; native SemanticEvent/history remains native authority; T0 is sparse event-time reconstructible basis, not mutable T1/parallel timeline; Commentator is read-only; retained multiplayer Dramaturg is recipient-scoped projection and never Story/history/ACL authority.

Topology: `NEW_CREATE GAME/TOOLS/story.py`, `GAME/TOOLS/commentator.py`; `NEW_CREATE DEV/SCHEMAS/story-state.schema.json`, `t0-baseline.schema.json`, `commentator-view.schema.json`; native SemanticEvent/history owner surfaces remain owner-controlled and are modified only where the RD-13 native-history integration task explicitly requires it.

## RD-14 — bootstrap / onboarding / product
Direct: `R030,R086,R098,R100` (4).
Composite slices: `R029.ONBOARDING`, `R087.SAVE_SESSION_MENU`.

Laws: bootstrap establishes valid initial frontier before gameplay mutation; onboarding creates no knowledge/history/currentness authority; save/session clear occurs only after confirmed RD-06 save truth; creator provenance fails closed; shipped instructions project one deterministic machine flow.

Topology: `NEW_CREATE GAME/TOOLS/bootstrap.py`; `NEW_CREATE DEV/SCHEMAS/bootstrap-request.schema.json`, `bootstrap-result.schema.json`; `EXISTING_REPLACE GAME/INSTALL/00_DND_BOOTSTRAP.md`; `EXISTING_MODIFY GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/README.md`; absent legacy `GAME/CORE/START.md` is not recreated.

## Cross-RD parent joins
`R087 = RD-11.RETROSPECTIVE + RD-13.SEMANTIC_EVENT_T0 + RD-14.SAVE_SESSION_MENU`.
`R122 = RD-08 chronology + RD-09 currentness + RD-11 context + RD-12 collaboration bridge`, only for a concrete material bridge.
`R029` joins RD-03 Actor + RD-06 durability + RD-14 onboarding.
`R062` includes RD-13 native SemanticEvent/history alongside its other owner-family slices.

Each detailed plan must carry RED/GREEN/REFACTOR/VERIFY, negative laws, Impact Envelope, Version Impact/checkpoint/migration/HG-01, currentness reread and coherent commits.

Accounting: PB-05 direct placement 22/22 unique; composite slices restored losslessly against critic-approved decomposition. Trigger-gated 12/12 and no-work 79/79 preserved. Production implementation: NO.