# PB-04 Source Manifest — RD-09..RD-11

Status: **PB-04 CONTROLLED SOURCE MANIFEST / IMPLEMENTATION PLANNING ONLY**

Baseline HEAD: `56319063e03da6678a963cde4da78e726965604c`

This manifest is subordinate to accepted native owners, WP-27 exact readiness records and critic-approved bounded decomposition v2. It authorizes no production implementation.

## Shared controlling sources

- `DEV/CURRENT_PROGRESS.md`
- critic-approved bounded decomposition v2 and round-4 PASS
- WP-27 Step-2 evidence ledger / canonical readiness spec
- Step-4 truth/knowledge/role/context Story owner + single-context containment amendment
- R2.3 Context Runtime canonical spec
- R2.4 single-context LLM execution canonical spec
- R2.5 collaboration/multiplayer canonical spec as downstream join authority
- Step-5.4 host lifecycle/session/handoff
- Step-5.8 multiplayer LIVE epoch ownership
- Step-5.12 response delivery/disclosure
- WP-08 role/context/instruction realization
- WP-09 context loading/resource bounds
- WP-16 multiplayer/access-control/LIVE-state canonical spec
- WP-17 collaboration/agency-safe progression as downstream consumer
- WP-11 routing/identity and WP-12 HOT/currentness owners.

## RD-09 — principal authorization / LIVE identity / currentness

Direct readiness: `R013,R014,R019,R020,R040,R078,R079,R080`.
Composite contributions: `R053.LIVE,R016.LIVE,R018.LIVE,R122.CURRENTNESS_SCENE`.

Owner laws:
- current trustworthy stable external GitHub user ID -> exactly one current active PLAYER binding -> campaign player identity;
- controlled-PC and operation-specific authority are separate checks;
- campaign, LIVE and local HOT currentness remain distinct domains; no cross-domain freshness scalar;
- LIVE is a physical/currentness partition, not semantic mega-owner;
- current route selects one exact epoch/source; exact-source non-force CAS is the authority-changing fence;
- CLOSED_UNABSORBED is selected truth with zero ordinary writers, not permission to fall back to campaign base;
- independently writable/live-born identities are source-native and never derive chronology/currentness from identifier order;
- authorization/routing dependencies are revalidated independently of LIVE CAS.

Current machine debt:
- `GAME/SCHEMA/player.schema.yaml` already encodes stable `github_binding.user_id`, campaign `player_id` and active/inactive semantics, but no shipped principal resolver/authorization runtime exists;
- `GAME/SCHEMA/live_scene.schema.yaml` is legacy/mixed: scene-shaped packing, integer revision, provisional IDs and embedded fact/knowledge-like material cannot define v1 semantic ownership or final source-native identity/currentness law;
- `GAME/TOOLS` has no LIVE/access-control executor.

Exact implementation surfaces selected:
- `GAME/TOOLS/access_control.py` — trustworthy principal -> PLAYER/control/operation authorization resolution only;
- `GAME/TOOLS/live_state.py` — typed claims, route lookup, epoch lifecycle, exact-source attempt/CAS result reconciliation, source-native LIVE identity;
- replace/reconcile `GAME/SCHEMA/live_scene.schema.yaml` as the shipped LIVE epoch/currentness envelope without semantic mega-owner fields;
- reconcile `GAME/SCHEMA/player.schema.yaml` only where needed for final control/currentness law;
- `NEW_CREATE DEV/SCHEMAS/live-claim.schema.json` and `DEV/SCHEMAS/live-publication-attempt.schema.json` as machine validation contracts, not new durable owners;
- focused test: `DEV/TESTS/test_rd09_access_live.py`.

No global active player, login-as-stable-ID, presence/heartbeat authority, path-glob claims, scene-wide wildcard ownership, force update, branch-name currentness, integer-revision authority, campaign allocator for LIVE-born IDs or chronology from IDs.

## RD-10 — role containment / handoff / protected emission

Direct readiness: `R054,R055,R056,R057,R118,R133,R137`.

Owner laws:
- one physical context may execute multiple logical roles, but every material phase explicitly rebinds role/subject/recipient/purpose/profile/bundle/basis/allowed prior results/authority/output contract;
- physical presence never creates logical eligibility;
- only minimum accepted typed result payload crosses role boundaries; no raw bundle/frame/private reasoning result bus;
- TurnEnvelope is bounded ephemeral control, never gameplay authority;
- phase-local steering is non-authoritative;
- fresh Narrator rebind follows Chronicler service;
- only validated Narrator player-facing payload crosses ordinary `EMISSION_COMMIT`; sanitation is defense in depth, not containment.

Current machine debt:
- `GAME/CORE/AI_REASONING.md` is the primary shipped containment-text owner and must remain the single ordinary-gameplay wording owner;
- `GAME/CORE/RUNTIME.md`/`PLAY_POLICY.md` may invoke control but cannot create competing eligibility authority;
- no shipped TurnEnvelope/phase-gateway/emission executor exists in `GAME/TOOLS`.

Exact implementation surfaces selected:
- `GAME/TOOLS/turn_runtime.py` — TurnEnvelope phase registration, rebind, typed phase-result gateway and finite fallback control;
- `GAME/TOOLS/emission.py` — NarrationResult validation and protected `EMISSION_COMMIT` boundary only;
- `GAME/CORE/AI_REASONING.md` targeted containment wording alignment; `RUNTIME.md` / `PLAY_POLICY.md` only invocation/reference projection changes where required;
- `NEW_CREATE DEV/SCHEMAS/turn-envelope.schema.json` and minimal registered phase-result schemas only as ephemeral machine contracts;
- focused test: `DEV/TESTS/test_rd10_role_emission.py`.

No role=call topology, persistent chain-of-thought, raw private handoff, second disclosure authority, Story feedback in same envelope, mechanical authority in TurnEnvelope, visible debug/trace/tool leakage or string-sanitizer-only fencing.

## RD-11 — bounded Context Runtime

Direct readiness: `R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145`.
Composite contributions: `R087.RETROSPECTIVE,R122.CONTEXT`.

Owner laws:
- Context Runtime is an ephemeral materialized logical projection over current/native owners and admitted derived evidence; it stores no truth;
- registered consumer/ContextNeedProfile owns requiredness, legal discovery relations, representation floors, bounds and fallback;
- bounded discovery precedes full load; no generic world-graph walk;
- routed currentness and eligibility resolve before role-local semantic use;
- complete required packet at legal minimum representations precedes optional/supporting allocation;
- optional ranking cannot override authority, eligibility or requiredness;
- historical escalation is dependency-specific and finite;
- trace/dry-run are diagnostic evidence only, never prompt content or authority;
- result is finite `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE` with no blind retry loop;
- no durable RoleContextBundle, ContextTrace, profile, source-basis or estimator-control record.

Critical joins:
- `R124` completes in RD-11 only after native disclosure/knowledge from RD-02 + role/recipient containment from RD-10 + controlled-actor/multiplayer scope from RD-12 + RD-09 principal/currentness where applicable; no second canon/disclosure owner;
- `R139` remains RD-11 Context Runtime: consumes native epistemic/history evidence and ranks only eligible optional/supporting candidates;
- `R122.CONTEXT` joins RD-08 chronology + RD-09 currentness-scene + RD-12 collaboration bridge only for a concrete positive material cross-scope dependency; no global sync/frontier.

Current machine debt:
- WP-09 confirms no durable representation is wanted for RoleContextBundle/Trace/profile/source-basis;
- `GAME/TOOLS` has no context assembler/runtime;
- current CORE/index/current/scene surfaces are discovery/routing support only and may not become closed-world/currentness/eligibility authority.

Exact implementation surfaces selected:
- `GAME/TOOLS/context_runtime.py` — registered request/profile pipeline, bounded discovery, routed currentness/eligibility, packet closure, representation selection, packet-first allocation, terminal result and dry-run trace;
- `GAME/TOOLS/context_budget.py` — one centralized conservative size estimator/budget envelope; no provider-specific fixed percentages or hidden-token dependency;
- `NEW_CREATE DEV/SCHEMAS/context-need-profile.schema.json` and `DEV/SCHEMAS/context-trace.schema.json` as DEV validation/test contracts for ephemeral values only, never campaign durable records;
- focused test: `DEV/TESTS/test_rd11_context_runtime.py`.

No generic memory DB, vector/graph authority, persistent fairness ledger, background retrieval worker, exhaustive world/history fallback, exact-hidden-token dependency, ranking-before-eligibility, optional eviction of required evidence, trace-as-role-evidence or durable context authority.

## Cross-RD joins and ordering

- RD-09 supplies trustworthy principal/control/current-source evidence to RD-10/RD-11/RD-12 but owns neither role eligibility nor collaboration semantics.
- RD-10 supplies role/recipient containment and protected emission; it consumes eligible context from RD-11 but does not own Context Runtime selection/ranking.
- RD-11 consumes RD-10 phase identity/recipient and RD-09 currentness when needed; its output remains an ephemeral role projection.
- `R124` cannot close package-wide until RD-12 controlled-actor/multiplayer scope exists; RD-11 plan must encode that downstream join rather than prematurely completing it.
- `R122` remains a four-slice composite across RD-08/RD-09/RD-11/RD-12 and is activated only by a concrete positive material cross-scope dependency.

No architecture contradiction or Product Owner decision was discovered. Production implementation remains unauthorized.