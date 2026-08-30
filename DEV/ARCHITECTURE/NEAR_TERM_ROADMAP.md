# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE PROGRAM ROADMAP — S6D COMPLETE / R2.7 WP-06 CLOSED / SENIOR REVIEW PASS / DOCUMENTATION CORPUS REFACTOR ACTIVE / WP-07 NOT STARTED**

Date: 2026-08-29

This file is the sequencing/status authority for Architecture Round 2 and inserted pre-resume architecture workstreams. Detailed semantics remain in owning specifications.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Primary program decisions:

- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

Current House-Rules authority:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`

R2.7 durable cursor:

- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`

---

## 1. Program baseline

```text
primary AI host              ChatGPT
plan                         ChatGPT Plus
player-facing surface        ordinary public chat
physical LLM topology        one LLM / one physical chat context
ordinary gameplay execution  one user request / one assistant turn
private HDM hosting          OUT OF CURRENT SCOPE
direct model API calls       OUT OF CURRENT SCOPE
mandatory paid inference     OUT OF CURRENT SCOPE
future provider migration    compatibility concern only
```

Single-context law remains:

> Physical availability of information does not make it logically eligible for the active HDM role.

Broad implementation requires explicit implementation planning. Owner-authorized clean-slate pre-release data-structure/catalog/schema/machine-contract materialization remains governed by its accepted architecture decision.

Current pre-release structural rule:

```text
EXISTING USER CAMPAIGNS REQUIRING COMPATIBILITY: NONE
CURRENT v2.0.0-GENERATION STRUCTURES: NOT A COMPATIBILITY FREEZE
STRUCTURAL/MACHINE-CONTRACT REPLACEMENT: AUTHORIZED WHEN ARCHITECTURE REQUIRES
SHIPPED GAME SEMANTICS/PACKAGING/DEPLOYMENT: NOT GENERALLY AUTHORIZED BY THAT RULE
```

Staleness must still be proven from current ownership/supersession/consumers, not inferred from version strings.

---

## 2. Preservation and operating rules

A closed topic becomes active only when current work materially extends/contradicts it, adds an unsatisfied consumer, or makes the accepted decision insufficient.

Operating rules:

- at most one numbered Round-2 stage may be `IN PROGRESS`;
- inserted owner-approved architecture/development work may pause the next numbered stage when recorded here;
- Source Manifest/evidence/synthesis gates precede Decision Brief/candidate/closure claims;
- current owning sources beat roadmap/index/summary/history;
- YAGNI applies to new owners, registries, schedulers, generic graphs and policy subsystems;
- ordinary-turn correctness remains local/bounded and must not gain unnecessary network/repository/extra-LLM round trips;
- every numbered S6D task/domain uses its own full eight-step deep-design loop.

The owner-approved **Documentation Corpus Refactor** is an inserted workstream, **not a numbered R2.7 WP**. It must close before substantive WP-07 analysis begins.

---

## 3. Stage registry

| Stage | Status | Scope |
|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | evidence rebaseline / dependency graph |
| R2.1 | **COMPLETE / ARCHITECTURE CLOSED** | continuity/history-aligned derived state |
| R2.2 | **COMPLETE / ARCHITECTURE CLOSED** | Actor continuity/cognition/relationships |
| R2.3 | **COMPLETE / ARCHITECTURE CLOSED** | Context Runtime/retrieval/allocation |
| R2.4 | **COMPLETE / ARCHITECTURE CLOSED** | single-context LLM execution/instructions |
| R2.5 | **COMPLETE / ARCHITECTURE CLOSED** | collaboration/multiplayer |
| R2.6 | **COMPLETE / ARCHITECTURE CLOSED** | ChatGPT-Plus assurance/security/degradation |
| House Rules | **COMPLETE / ARCHITECTURE CLOSED** | campaign semantic policy, rulings, typed adjudication boundary, adoption authority |
| S6D | **COMPLETE / INTEGRATED CLOSURE PASS — S6D-12 STEPS 1-8 + MRC-01…04 VERIFIED** | residual rules/seed/catalog debt closed |
| R2.7 | **WP-06 CLOSED / SENIOR REVIEW PASS; DOCUMENTATION CORPUS REFACTOR ACTIVE; WP-07 NOT STARTED** | whole-project final architecture & machine-realization audit, paused before WP-07 for inserted documentation refactor |

---

## 4. Current dependency graph

```text
R2.0..R2.6 COMPLETE
    -> HOUSE RULES STEPS 1-8 COMPLETE / REPAIRED CLOSURE
    -> S6D-01..S6D-12 COMPLETE / INTEGRATED CLOSURE PASS
    -> R2.7 WP-01..WP-06 CLOSED
    -> WP-06 SENIOR SEMANTIC/TECHNICAL REVIEW PASS
    -> DOCUMENTATION CORPUS REFACTOR                  [ACTIVE / REQUIRED BEFORE WP-07 / NOT A NUMBERED WP]
    -> R2.7 WP-07..WP-27
    -> R2.7 final reconciliation
    -> Implementation Planning
```

**Current stop.** WP-06 is closed and has passed Senior semantic/technical review. Its final public SHA is `06f70919d52739f72515a5d315bb0998d7c34c6e`; `Validate engine source #33238159180` completed successfully on that exact SHA. WP-07 remains not started. The inserted Documentation Corpus Refactor is active and must close before substantive WP-07 analysis.

S6D remains complete: `SEMANTIC_ARCHITECTURE_RECONCILED == TRUE`, `MACHINE_REALIZATION_VERIFIED == TRUE`, `S6D_FINAL_CLOSURE_AUTHORIZED == TRUE`, integrated closure PASS. No S6D blocker remains.

---

## 5. House Rules closed state

Primary canonical owner:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

Repaired closure chain:

- Step 1 — `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
- Step 2 repair — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`
- Step 3 amended decision brief — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`
- Step 3 owner decision — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`
- Step 4 — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-4-collaborative-review-v2.md`
- Step 5 — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`
- Step 6 — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-6-adversarial-review-v2.md`
- Step 7 — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-7-resolution-gate-v2.md`
- Step 8 — `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`

Settled responsibility/authority:

```text
runtime responsibility         existing owners + narrow structured sidecar
INTERPRETIVE_POLICY            every active multiplayer PLAYER by default
MECHANICAL_OVERRIDE_POLICY     creator by default; explicit creator-issued per-PLAYER grant
creator source                 existing first campaign initialization commit provenance
MANIFEST creator field         NONE / intentionally unchanged
policy notification            normal refresh + changed paths + OOC notice in current output
background push/outbox         NONE
```

Machine contracts materialized during architecture because clean-slate authorization applies:

- richer frozen adjudicated Activity parameter binding contracts/tests;
- `GAME/SCHEMA/player.schema.yaml` mechanical-override grant;
- `GAME/SCHEMA/house_rules_policy.schema.yaml`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml`;
- matching runtime-facing policy/adjudication/access-control contracts and focused tests.

Registered boolean invocation context facts remain boolean.

---

## 6. Preserved House-Rules laws

- LLM semantic judgment remains separate from deterministic execution;
- LLM/prose does not own RNG or canonical state mutation;
- current authorized campaign policy may invalidate stale baseline realization;
- missing deterministic realization produces a finite gap;
- physical visibility does not imply information eligibility;
- House Rules is scoped policy data below instruction authority;
- retrieval remains bounded through Context Runtime;
- indexes/caches remain routing-only;
- no House-Rules-specific global policy epoch/frontier;
- multiplayer propagation is publication/currentness + context assembly, not chat copying;
- accepted policy-dependent causal inputs remain frozen across retry/recovery;
- later policy publication is forward-looking;
- structured promotion is optional and must not duplicate deterministic owners;
- unindexed normative prose is not admitted as durable policy authority;
- explicit realization refs are linkage, not execution authority.

---

## 7. S6D — complete / integrated closure PASS

S6D decomposition/evidence inputs remain:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

The plan is a decomposition/coverage index only. Current owning architecture and later accepted amendments control semantics.

S6D-12 Step 1 authority:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-task-brief.md`;
- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-task-brief-amendment.md`;
- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-brief-critic.md`.

S6D-12 Step 2 evidence:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-evidence.md`.

S6D-12 Step 3 decision:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-decision-brief.md` — `HUMAN_DECISION_REQUIRED: NO`.

S6D-12 Step 4 review:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-step-4-collaborative-review.md` — no semantic contradiction; B′/identity plus Mechanical-Null execution proof remain machine-realization obligations.

S6D-12 Step 5 candidate:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-step-5-candidate-spec.md` — exact final closure predicates, finite machine closure conditions and deferred acceptance boundaries.

S6D-12 Step 6 critic:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-step-6-whole-project-critic.md` — whole-project critic pass after owner-conforming Mechanical-Null clarification.

S6D-12 Step 7 resolution gate:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-step-7-resolution-gate.md` — historical pre-realization gate: semantic architecture reconciled; machine realization then not verified; final closure then not authorized.

S6D-12 Step 8 canonicalization:

- `DEV/docs/superpowers/specs/2026-08-28-s6d-12-adversarial-final-closure-step-8-canonicalization.md` — historical canonical semantic reconciliation and pre-realization blocked disposition; its current closure evaluation is superseded by the post-realization record below.

Post-realization closure record:

- `DEV/docs/superpowers/specs/2026-08-29-s6d-integrated-machine-realization-closure.md` — current S6D final closure authority/status. Its historical continuation statement authorized WP-06 resume; WP-06 is now closed and Senior-reviewed.

S6D-08 stale identity prose reconciliation:

- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` now routes package/set identity exclusively through the canonical S6D-11 manifest -> package snapshot -> resolved lock -> `ruleset_set_sha256` chain and owns no aggregate content-set identity.

B′ carry-in authority remains:

- `DEV/docs/superpowers/specs/2026-08-28-domain-rules-coverage-derived-binding-owner-decision.md`;
- `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md`.

Current closure predicates:

```text
SEMANTIC_ARCHITECTURE_RECONCILED: TRUE
MACHINE_REALIZATION_VERIFIED: TRUE
S6D_FINAL_CLOSURE_AUTHORIZED: TRUE
S6D_FINAL_CLOSURE: PASS
R2_7_WP06_RESUME_ALLOWED: TRUE
R2_7_WP06: COMPLETE / SENIOR REVIEW PASS
```

---

## 8. R2.7 current status

```text
WP-01 CLOSED
WP-02 CLOSED
WP-03 CLOSED
WP-04 CLOSED
WP-05 CLOSED
WP-06 CLOSED / SENIOR REVIEW PASS
DOCUMENTATION CORPUS REFACTOR ACTIVE / REQUIRED BEFORE WP-07 / NOT A NUMBERED WP
WP-07 NOT STARTED
WP-08..WP-27 NOT STARTED
```

No WP-07 substantive analysis is authorized until the inserted Documentation Corpus Refactor reaches verified closure and Senior review.

---

## 9. Current continuation point

```text
HOUSE_RULES: STEPS 1-8 COMPLETE / CANONICAL
S6D: INTEGRATED CLOSURE PASS
S6D_COMPLETED_DOMAIN: S6D-12 / STEPS 1-8 / SEMANTIC ARCHITECTURE CANONICAL
S6D_ACTIVE_DOMAIN: NONE / INTEGRATED CLOSURE PASS
S6D_COMPLETED_STAGE: S6D INTEGRATED CLOSURE / POST-REALIZATION PASS
S6D_ACTIVE_STAGE: NONE / FINAL CLOSURE PASS
S6D_NEXT_STAGE: NONE
S6D_FINAL_CLOSURE_BLOCKER: NONE
R2_7_WP06: COMPLETE / SENIOR REVIEW PASS
INSERTED_WORKSTREAM: DOCUMENTATION CORPUS REFACTOR
INSERTED_WORKSTREAM_STATUS: ACTIVE / REQUIRED BEFORE WP-07
R2_7_WP07: NOT STARTED
NEXT_EXACT_TASK: Documentation Corpus Refactor
```