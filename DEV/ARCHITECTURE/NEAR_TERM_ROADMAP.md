# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE PROGRAM ROADMAP — S6D-04 COMPLETE / S6D-05 STEP 1 NEXT / R2.7 PAUSED**

Date: 2026-08-25

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
- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

Current House-Rules authority:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`

R2.7 durable cursor:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

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

Broad implementation remains blocked until final architecture closure and explicit implementation planning, except for owner-authorized clean-slate pre-release data-structure/catalog/schema/machine-contract materialization required by an architecture decision.

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
- inserted owner-approved architecture work may pause that stage when recorded here;
- Source Manifest/evidence/synthesis gates precede Decision Brief/candidate/closure claims;
- current owning sources beat roadmap/index/summary/history;
- YAGNI applies to new owners, registries, schedulers, generic graphs and policy subsystems;
- ordinary-turn correctness remains local/bounded and must not gain unnecessary network/repository/extra-LLM round trips;
- every numbered S6D task/domain uses its own full eight-step deep-design loop.

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
| S6D | **IN PROGRESS — S6D-01 THROUGH S6D-04 COMPLETE / S6D-05 STEP 1 NEXT** | residual rules/seed/catalog debt |
| R2.7 | **PAUSED AT WP-06** | whole-project final architecture & machine-realization audit |

---

## 4. Current dependency graph

```text
R2.0..R2.6 COMPLETE
    -> R2.7 WP-01..WP-05 CLOSED
    -> R2.7 WP-06 PARTIAL / PAUSED
    -> HOUSE RULES STEPS 1-8 COMPLETE / REPAIRED CLOSURE
    -> S6D-01 Steps 1-8                            [COMPLETE / ARCHITECTURE CLOSED]
    -> S6D-02 Steps 1-8                            [COMPLETE / CANONICAL]
    -> S6D-03 Steps 1-8                            [COMPLETE / CANONICAL]
    -> S6D-04 Steps 1-8                            [COMPLETE / CANONICAL]
    -> S6D-05 Step 1                               [NEXT / NOT STARTED]
    -> ... remaining S6D domains full eight-step loops ...
    -> S6D integrated closure
    -> R2.7 WP-06 RESUME
    -> R2.7 WP-07..WP-27
    -> R2.7 final reconciliation
    -> Implementation Planning
```

**Current stop.** S6D-04 completed its full eight-step loop with whole-project adversarial PASS and canonicalization. S6D-05 Step 1 is next and has not started.

---

## 5. House Rules closed state

Primary canonical owner:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

Repaired closure chain:

- Step 1 — `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
- Step 2 repair — `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`
- Step 3 amended decision brief — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`
- Step 3 owner decision — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`
- Step 4 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review-v2.md`
- Step 5 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`
- Step 6 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review-v2.md`
- Step 7 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate-v2.md`
- Step 8 — `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`

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

## 7. S6D — S6D-04 complete / S6D-05 Step 1 next

S6D decomposition/evidence inputs remain:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

The plan is a decomposition/coverage index only. S6D-01 through S6D-03 are canonically closed by their named architecture owners. S6D-04 completed its full loop and is canonically owned by `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`; S6D-05 Step 1 is next and has not started.

---

## 8. R2.7 pause

```text
WP-01 CLOSED
WP-02 CLOSED
WP-03 CLOSED
WP-04 CLOSED
WP-05 CLOSED
WP-06 IN PROGRESS / PAUSED
WP-07..WP-27 NOT STARTED
```

R2.7 WP-06 resumes only after S6D integrated closure.

---

## 9. Current continuation point

```text
HOUSE_RULES: STEPS 1-8 COMPLETE / CANONICAL
S6D: IN PROGRESS
S6D_COMPLETED_DOMAIN: S6D-04 / STEPS 1-8 / ARCHITECTURE CLOSED
S6D_NEXT_DOMAIN: S6D-05
S6D_ACTIVE_DOMAIN: NONE
S6D_COMPLETED_STAGE: STEPS 1-8 / CANONICALIZATION VERIFIED
S6D_ACTIVE_STAGE: NONE
S6D_NEXT_STAGE: STEP 1 / ARCHITECTURE TASK BRIEF
R2_7_WP06: PAUSED
```

Next action requires explicit owner continuation into **S6D-05 Step 1 — Architecture Task Brief**. Do not start S6D-05 from this roadmap update alone.


