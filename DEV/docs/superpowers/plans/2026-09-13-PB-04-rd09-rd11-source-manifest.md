# PB-04 Source Manifest — RD-09..RD-11

Status: **PB-04 CONTROLLED SOURCE MANIFEST / IMPLEMENTATION PLANNING ONLY**
Baseline HEAD: `56319063e03da6678a963cde4da78e726965604c`

Subordinate to accepted native owners, WP-27 exact readiness records and critic-approved bounded decomposition v2. No production implementation is authorized.

## Controlling owners

- Step-4 truth/knowledge/role/context Story owner + single-context containment amendment
- R2.3 Context Runtime; R2.4 single-context LLM execution; R2.5 collaboration/multiplayer
- Step-5.4 host lifecycle/session/handoff; Step-5.8 LIVE epoch ownership; Step-5.12 delivery/disclosure
- WP-08 role/context/instruction realization; WP-09 context loading/resource bounds
- WP-16 access-control/LIVE; WP-17 collaboration downstream consumer
- WP-11 identity/routing; WP-12 HOT/currentness
- WP-27 readiness ledger/canonical spec and decomposition-v2 critic PASS.

## RD-09 — principal / LIVE / currentness

Direct: `R013,R014,R019,R020,R040,R078,R079,R080`.
Composite slices: `R053.LIVE,R016.LIVE,R018.LIVE,R122.CURRENTNESS_SCENE`.

Binding laws: trustworthy stable external principal -> exactly one current active PLAYER -> separate controlled-PC/operation authorization; campaign/LIVE/HOT currentness remain distinct; LIVE is physical/currentness partition only; selected exact source is fenced by non-force CAS; CLOSED_UNABSORBED is selected truth with zero ordinary writers; LIVE-born identity is source-native and has no chronology meaning.

Current evidence: `GAME/SCHEMA/player.schema.yaml` already correctly carries stable `github_binding.user_id`, canonical `player_id`, active/inactive and controlled-PC relations. It is `INSPECT_ONLY`, not a planned rewrite. `GAME/SCHEMA/live_scene.schema.yaml` is mixed/legacy and must be replaced because scene-shaped packing, integer revision, provisional IDs and embedded fact/knowledge-like fields cannot define v1 authority.

Exact surfaces:
- `NEW_CREATE GAME/TOOLS/access_control.py`
- `NEW_CREATE GAME/TOOLS/live_state.py`
- `EXISTING_REPLACE GAME/SCHEMA/live_scene.schema.yaml`
- `INSPECT_ONLY GAME/SCHEMA/player.schema.yaml`
- `NEW_CREATE DEV/SCHEMAS/live-claim.schema.json`
- `NEW_CREATE DEV/SCHEMAS/live-publication-attempt.schema.json`
- existing identifier-policy/catalog projections updated for `source_native_live`
- `NEW_CREATE DEV/TESTS/test_rd09_access_live.py`

Forbidden: login-as-ID, global active player, presence authority, wildcard LIVE claims, semantic mega-owner, branch/integer freshness authority, force update, campaign allocator for LIVE-born IDs, chronology from IDs.

## RD-10 — role containment / typed handoff / protected emission

Direct: `R054,R055,R056,R057,R118,R133,R137`.

Binding laws: one physical context may host multiple logical roles; every material phase rebinds role/subject/recipient/purpose/profile/bundle/allowed typed prior results/authority/output; physical presence is not eligibility; TurnEnvelope is ephemeral control; handoffs are minimum typed results only; late steering is non-authoritative; Narrator freshly rebinds after Chronicler; only validated Narrator payload crosses ordinary `EMISSION_COMMIT`; sanitization is defense in depth only.

Current evidence: `GAME/CORE/AI_REASONING.md` is the one primary containment-text owner. `GAME/CORE/RUNTIME.md` and `PLAY_POLICY.md` are invocation/activation consumers and are `INSPECT_ONLY` for this RD. No shipped turn/emission runtime exists.

Exact surfaces:
- `NEW_CREATE GAME/TOOLS/turn_runtime.py`
- `NEW_CREATE GAME/TOOLS/emission.py`
- `EXISTING_MODIFY GAME/CORE/AI_REASONING.md`
- `INSPECT_ONLY GAME/CORE/RUNTIME.md`
- `INSPECT_ONLY GAME/CORE/PLAY_POLICY.md`
- `NEW_CREATE DEV/SCHEMAS/turn-envelope.schema.json`
- `NEW_CREATE DEV/SCHEMAS/interpreter-result.schema.json`
- `NEW_CREATE DEV/SCHEMAS/preparation-draft.schema.json`
- `NEW_CREATE DEV/SCHEMAS/actor-proposal.schema.json`
- `NEW_CREATE DEV/SCHEMAS/story-projection-draft.schema.json`
- `NEW_CREATE DEV/SCHEMAS/narration-result.schema.json`
- `NEW_CREATE DEV/TESTS/test_rd10_role_emission.py`

All DEV phase schemas validate ephemeral machine values only. No role=call requirement, raw private handoff/result bus, chain-of-thought persistence, same-envelope Story feedback, TurnEnvelope authority, second disclosure owner, visible trace/debug/tool path or sanitizer-only fencing.

## RD-11 — bounded Context Runtime

Direct: `R059,R060,R097,R105,R106,R107,R117,R119,R120,R124,R125,R127,R134,R135,R138,R139,R140,R144,R145`.
Composite slices: `R087.RETROSPECTIVE,R122.CONTEXT`.

Binding laws: Context Runtime is ephemeral projection only; registered consumer/profile owns requiredness/relations/floors/bounds/fallback; bounded typed discovery precedes full load; routed currentness and eligibility precede semantic use; complete required packet at legal floors precedes optional allocation; optional ranking cannot override authority/eligibility/requiredness; historical escalation is dependency-specific/finite; trace is diagnostic only; result terminates as `ASSEMBLED | ASSEMBLED_DEGRADED | UNSATISFIABLE`; no durable RoleContextBundle/Trace/profile/source-basis/estimator state.

Critical joins:
- `R124`: RD-02 knowledge/disclosure + RD-10 role/recipient containment + RD-12 controlled-actor scope + RD-09 principal/currentness where applicable -> RD-11 scoped projection. No second canon/disclosure owner.
- `R139`: RD-11 ranking over already eligible optional/supporting material only.
- `R122.CONTEXT`: consumes RD-08 chronology + RD-09 currentness-scene + RD-12 collaboration bridge only when a concrete positive material cross-scope dependency exists.

Exact surfaces:
- `NEW_CREATE GAME/TOOLS/context_runtime.py`
- `NEW_CREATE GAME/TOOLS/context_budget.py`
- `NEW_CREATE DEV/SCHEMAS/context-need-profile.schema.json`
- `NEW_CREATE DEV/SCHEMAS/context-trace.schema.json`
- no durable GAME schema/root for RoleContextBundle, ContextTrace, profile, source basis or estimator state
- `NEW_CREATE DEV/TESTS/test_rd11_context_runtime.py`

Forbidden: generic memory/vector/graph authority, persistent fairness ledger, background retrieval worker, exhaustive world/history fallback, hidden-token dependency, ranking-before-eligibility, optional eviction of required evidence, trace-as-role-evidence/output, durable context authority or global R122 synchronization.

## Cross-RD ordering

RD-09 supplies principal/control/current-source evidence without owning role eligibility/collaboration. RD-10 supplies phase/recipient containment and emission without owning Context Runtime. RD-11 consumes both and remains ephemeral. `R124` and `R122` remain package-incomplete until RD-12 supplies its required slices. No architecture contradiction or Product Owner decision is open.