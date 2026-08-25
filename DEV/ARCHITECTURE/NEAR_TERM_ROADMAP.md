# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE PROGRAM ROADMAP — R2.7 PAUSED / HOUSE RULES HOLD AT STEP 2–3 / S6D BLOCKED**

Date: 2026-08-25

This file is the sequencing/status authority for Architecture Round 2 and the inserted pre-resume architecture workstreams. Detailed semantics remain in owning specifications.

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

Current House-Rules gate authority:

- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-senior-audit-reopen-hold.md`
- `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`

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

Broad implementation remains blocked until final architecture closure and explicit implementation planning, except for owner-authorized clean-slate pre-release **data-structure/catalog/schema/machine-contract materialization required by an architecture decision**.

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

A closed topic becomes active only when current work:

1. materially extends the accepted contract;
2. exposes a contradiction or invalid assumption;
3. introduces a new consumer the accepted contract cannot satisfy; or
4. makes the accepted decision insufficient for a current requirement.

House Rules is currently reopened only because the Senior whole-project audit found a real human-decision-gate failure and an incomplete richer machine-consumer contract. The preserved directions enumerated in the reopen HOLD remain closed to casual relitigation.

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
| House Rules | **HOLD / REOPENED AT STEP 2–3** | campaign semantic policy, rulings, typed adjudication boundary |
| S6D | **PREPARED / BLOCKED / NOT STARTED** | residual rules/seed/catalog debt |
| R2.7 | **PAUSED AT WP-06** | whole-project final architecture & machine-realization audit |

---

## 4. Current dependency graph

```text
R2.0..R2.6 COMPLETE
    -> R2.7 WP-01..WP-05 CLOSED
    -> R2.7 WP-06 PARTIAL / PAUSED
    -> HOUSE RULES STEP 1 PRESERVED
    -> HOUSE RULES STEP 2 AUDIT REPAIR COMPLETE
    -> HOUSE RULES STEP 3 HUMAN DECISION GATE      [CURRENT]
    -> HOUSE RULES STEP 4..8 RERUN/RECONCILE ONLY AFTER HUMAN DECISION
    -> HOUSE RULES CANONICALIZATION
    -> S6D Task/Domain 1 Step 1                    [BLOCKED]
    -> ... each S6D domain full eight-step loop ...
    -> S6D integrated closure
    -> R2.7 WP-06 RESUME
    -> R2.7 WP-07..WP-27
    -> R2.7 final reconciliation
    -> Implementation Planning
```

**S6D may not start from the earlier attempted House-Rules Step-8 closure.** The current House-Rules human decision gate must first close and the downstream House-Rules steps must be rerun/reconciled through a valid Step 8.

---

## 5. House Rules current state

Step 1 remains valid and is not reopened:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

Current Step-2 evidence repair:

- `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`

Current Step-3 human gate:

- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`

The former Step-4..8 artifacts and `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` are **attempted-closure/candidate material while the HOLD is active**. The hold status artifact controls that gate; preserved noncontroversial directions remain evidence inputs.

Machine-contract repair already materialized because it is derivable and independent of the unresolved policy-adoption authority decision:

- `DEV/SCHEMAS/activity-parameter-binding.schema.json`;
- tightened `DEV/SCHEMAS/activity-parameter-spec.schema.json`;
- updated ActionRequest/Resolution/Continuation/receipt schemas;
- `DEV/TESTS/test_house_rules_adjudicated_input_contract.py`.

The registered `mechanical-surfaces.json` context-fact channel remains boolean by design.

Remaining human decisions are responsibility shape and campaign policy-adoption/delegation authority. Step 4 is blocked until those decisions are explicit.

---

## 6. Preserved House-Rules directions during HOLD

Do not reopen these solely because the gate failed:

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
- structured promotion is optional and must not duplicate deterministic owners.

---

## 7. S6D — blocked

S6D decomposition/evidence inputs remain:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

The plan is a decomposition/coverage index only. When unblocked, the next S6D domain begins at **Step 1 — Architecture Task Brief**. No S6D task/domain is active now.

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

The immutable pre-pause R2.7 obligation checkpoint remains recorded in the durable audit status. R2.7 WP-06 resumes only after a valid House-Rules closure and S6D integrated closure.

---

## 9. Current continuation point

```text
HOUSE_RULES_STEP_1: PRESERVED
HOUSE_RULES_STEP_2: REPAIRED / EVIDENCE DELTA COMPLETE
HOUSE_RULES_STEP_3: HUMAN DECISION REQUIRED
HOUSE_RULES_STEP_4_PLUS: BLOCKED
S6D: BLOCKED / NOT STARTED
R2_7_WP06: PAUSED
```

Next action: obtain the explicit human decisions requested by the amended Step-3 Decision Brief. Do not infer them from prior GO language or conversation silence.
