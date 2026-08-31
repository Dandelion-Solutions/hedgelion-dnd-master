# HDM Architecture Round 2 — Program Roadmap

Status: **SEQUENCING / SCOPE — NOT CURRENT-PROGRESS AUTHORITY**

Date: 2026-08-31

This file owns intended sequencing, stage scope and dependencies for Architecture Round 2 and inserted workstreams. Global current state, active work and gates are owned only by `DEV/CURRENT_PROGRESS.md`. Detailed semantics remain in owning specifications.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Primary program decisions:

- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

House-Rules owner references:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-8-canonicalization-v2.md`


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

---

## 3. Stage registry

| Stage | Scope |
|---|---|
| R2.0 | evidence rebaseline / dependency graph |
| R2.1 | continuity/history-aligned derived state |
| R2.2 | Actor continuity/cognition/relationships |
| R2.3 | Context Runtime/retrieval/allocation |
| R2.4 | single-context LLM execution/instructions |
| R2.5 | collaboration/multiplayer |
| R2.6 | ChatGPT-Plus assurance/security/degradation |
| House Rules | campaign semantic policy, rulings, typed adjudication boundary, adoption authority |
| S6D | residual rules/seed/catalog closure |
| R2.7 | whole-project final architecture & machine-realization audit; WP-01 through WP-27 and final reconciliation |

---

## 4. Dependency graph

```text
R2.0..R2.6
    -> House Rules
    -> S6D
    -> R2.7 WP-01..WP-27
    -> R2.7 final reconciliation
    -> Implementation Planning
```

For the actual current position, next authorized unit and gate, read
`DEV/CURRENT_PROGRESS.md`. Closure evidence remains in its owning records.

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

- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

The plan is a decomposition/coverage index only. Current owning architecture and later accepted amendments control semantics.

S6D-12 Step 1 authority:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-task-brief.md`;
- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-task-brief-amendment.md`;
- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-brief-critic.md`.

S6D-12 Step 2 evidence:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-evidence.md`.

S6D-12 Step 3 decision:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-decision-brief.md` — `HUMAN_DECISION_REQUIRED: NO`.

S6D-12 Step 4 review:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-step-4-collaborative-review.md` — no semantic contradiction; B′/identity plus Mechanical-Null execution proof remain machine-realization obligations.

S6D-12 Step 5 candidate:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-step-5-candidate-spec.md` — exact final closure predicates, finite machine closure conditions and deferred acceptance boundaries.

S6D-12 Step 6 critic:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-step-6-whole-project-critic.md` — whole-project critic pass after owner-conforming Mechanical-Null clarification.

S6D-12 Step 7 resolution gate:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-step-7-resolution-gate.md` — historical pre-realization gate: semantic architecture reconciled; machine realization then not verified; final closure then not authorized.

S6D-12 Step 8 canonicalization:

- `DEV/docs/superpowers/design/2026-08-28-s6d-12-adversarial-final-closure-step-8-canonicalization.md` — historical canonical semantic reconciliation and pre-realization blocked disposition; its current closure evaluation is superseded by the post-realization record below.

Post-realization closure record:

- `DEV/docs/superpowers/design/2026-08-29-s6d-integrated-machine-realization-closure.md` — current S6D final closure authority/status. Its historical continuation statement authorized WP-06 resume; WP-06 is now closed and Senior-reviewed.

S6D-08 stale identity prose reconciliation:

- `DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md` now routes package/set identity exclusively through the canonical S6D-11 manifest -> package snapshot -> resolved lock -> `ruleset_set_sha256` chain and owns no aggregate content-set identity.

B′ carry-in authority remains:

- `DEV/docs/superpowers/specs/2026-08-28-domain-rules-coverage-derived-binding-owner-decision.md`;
- `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md`;
- `DEV/ARCHITECTURE/RULESET_PACKAGE_MACHINE_CLOSURE.md`.

Recorded S6D closure predicates:

```text
SEMANTIC_ARCHITECTURE_RECONCILED: TRUE
MACHINE_REALIZATION_VERIFIED: TRUE
S6D_FINAL_CLOSURE_AUTHORIZED: TRUE
S6D_FINAL_CLOSURE: PASS
```

---
