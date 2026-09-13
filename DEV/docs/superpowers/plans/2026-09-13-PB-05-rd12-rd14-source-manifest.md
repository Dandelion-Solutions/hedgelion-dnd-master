# PB-05 Source Manifest — RD-12..RD-14

Status: AUTHORING BASELINE
Baseline HEAD: `05edd81195ba22bbed1467ad2ab49b06061d4535`
Scope: planning only; production implementation is not authorized.

## Sources

Authorities: `DEV/CURRENT_PROGRESS.md`; critic-approved bounded decomposition v2; WP-27 Step-2 evidence ledger and final readiness spec; `DEV/docs/superpowers/design/2026-09-09-r2-5-agency-safe-collaboration-architecture-final-spec.md`; `DEV/ARCHITECTURE/DECISIONS.md`; `DEV/ARCHITECTURE/DECISIONS_APPENDIX.md`; `DEV/ARCHITECTURE/FINAL/MULTIPLAYER_MODEL.md`; current `GAME/INSTALL/**`, `GAME/SCHEMA/**`, `GAME/TOOLS/**`, `DEV/SCHEMAS/**`, `DEV/CATALOGS/**` inventory.

Excluded as authority: runtime release packages; derivative history/summaries; trigger-gated and explicit no-work leaves.

## RD-12 — collaboration / multiplayer

Direct readiness: `R021,R044,R081,R082,R083,R121,R123,R141,R142,R143,R146` (11). Composite completion: `R122.COLLABORATION`; `R124` is a prerequisite join surface and completes in RD-11.

Laws: one authoritative world; no global active player; no implicit active-user fallback; positive material dependency precedes waiting; waiting is scope-local; absent/departed actors do not block unrelated work; join/rejoin obtains a current frontier before mutation; catch-up is recipient projection, not history/knowledge authority.

Selected machine topology:
- `GAME/TOOLS/collaboration.py` — NEW_CREATE runtime coordinator.
- `DEV/SCHEMAS/collaboration-request.schema.json` — NEW_CREATE.
- `DEV/SCHEMAS/collaboration-frontier.schema.json` — NEW_CREATE.
- `DEV/SCHEMAS/catch-up-projection.schema.json` — NEW_CREATE.
- `GAME/SCHEMA/player.schema.yaml`, `GAME/SCHEMA/live_scene.schema.yaml` — INSPECT_ONLY consumer/projection surfaces.

## RD-13 — Story / T0 / Commentator / history

Direct readiness: `R022,R051,R084,R085,R099,R102,R131` (7).

Laws: one canonical Story state; summary is non-authoritative compression; SemanticEvent/history authority remains separate; T0 is reconstructible baseline, not a second timeline; Commentator is reconstructive/explanatory and cannot mutate gameplay truth; multiplayer transport cannot create a second Story/history authority.

Selected machine topology:
- `GAME/TOOLS/story.py` — NEW_CREATE Story transition/projection boundary.
- `GAME/TOOLS/commentator.py` — NEW_CREATE read-only reconstruction boundary.
- `DEV/SCHEMAS/story-state.schema.json` — NEW_CREATE Story-specific durable-state contract.
- `DEV/SCHEMAS/t0-baseline.schema.json` — NEW_CREATE reconstructible baseline contract.
- `DEV/SCHEMAS/commentator-view.schema.json` — NEW_CREATE non-authoritative output contract.
- SemanticEvent/history owner surfaces — INSPECT_ONLY except explicit consumer integration.

## RD-14 — bootstrap / onboarding / product

Direct readiness: `R030,R086,R098,R100` (4). Composite: `R029.ONBOARDING`. Completion consumes approved Actor/current-frontier, Story/T0 and collaboration joins where applicable.

Laws: bootstrap establishes a valid initial authoritative frontier before gameplay mutation; onboarding creates no knowledge/history/currentness authority; bootstrap/onboarding semantics are explicit and deterministic; shipped instructions project the same machine contract.

Selected machine topology:
- `GAME/TOOLS/bootstrap.py` — NEW_CREATE bootstrap/onboarding orchestrator.
- `DEV/SCHEMAS/bootstrap-request.schema.json` — NEW_CREATE.
- `DEV/SCHEMAS/bootstrap-result.schema.json` — NEW_CREATE.
- `GAME/INSTALL/00_DND_BOOTSTRAP.md` — EXISTING_REPLACE v1 projection.
- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`, `GAME/INSTALL/README.md` — EXISTING_MODIFY aligned projections.
- missing legacy `GAME/CORE/START.md` — do not recreate solely because old evidence named it.

## Cross-RD / closure constraints

RD-12 consumes principal/LIVE/currentness and Context Runtime without taking their authority. RD-13 consumes accepted history and temporal/currentness evidence without becoming those authorities. RD-14 integrates only after owner contracts are available. Protected emission remains RD-10; Context Runtime remains RD-11.

Each detailed plan must state RED/GREEN/REFACTOR/VERIFY, negative-law tests, Impact Envelope, version/schema/checkpoint/migration/HG-01 effects, currentness reread and coherent worker commits. Compatibility shims are not invented: `GAME/**` may be reconstructed for v1 when the plan explicitly says so.

Accounting: PB-05 direct placement 22/22, no duplicates. Trigger-gated preserved 12/12. Explicit no-work preserved 79/79. Production implementation authorized: NO.
