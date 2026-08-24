# R2.7 — Audit Status / Durable Cursor

Status: **PAUSED BY OWNER — HOUSE RULES 8-STEP DESIGN NEXT; S6D AFTER**

Date: 2026-08-24

Execution protocol:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-audit-execution-protocol.md`

R2.7 task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`

Current sequencing owner:

- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

House Rules design input:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

S6D decomposition/evidence inputs:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

## Immutable pre-pause checkpoint

The complete R2.7 cursor, open forward obligations, closed-domain summaries and pre-pause recovery state are preserved in Git blob:

```text
PRE_PAUSE_STATUS_BLOB_SHA: d486825dc5c9463b2e2159086e6c7102c3caf354
```

Do not reconstruct those obligations from conversation history.

## Durable cursor

```text
AUDIT_STATUS: PAUSED
LAST_CLOSED_DOMAIN: WP-05
PAUSED_DOMAIN: WP-06
PAUSED_DOMAIN_TOPIC: Rules / adjudication / domain-module compatibility
PAUSED_SLICE: owning rule-domain graph + CORE/domain reverse audit; first structural rules-seed slice already partially materialized
NEXT_R2_7_DOMAIN_AFTER_RESUME: WP-07
OWNER_GATE: PROGRAM PAUSE / HOUSE_RULES_THEN_S6D
FINAL_RECONCILIATION: NOT_STARTED

NEXT_WORKSTREAM: HOUSE_RULES_ARCHITECTURE
HOUSE_RULES_STATUS: DESIGN BRIEF EXISTS / FULL 8-STEP LOOP NOT STARTED
HOUSE_RULES_START: next chat begins with Step 1 Task-Brief review/challenge

FOLLOWING_WORKSTREAM: S6D — Step-6 Residual Rules/Seed Debt Closure
S6D_STATUS: PREPARED / NOT STARTED
S6D_EXECUTION_RULE: each numbered task/domain runs its own full 8-step deep-design loop
S6D_START_TRIGGER: House Rules Step 8 canonicalization complete
R2_7_RESUME_TRIGGER: S6D integrated closure/resolution gate complete
```

## R2.7 progress at pause

| Domain | Status |
|---|---|
| WP-01 | CLOSED |
| WP-02 | CLOSED |
| WP-03 | CLOSED |
| WP-04 | CLOSED |
| WP-05 | CLOSED |
| WP-06 | PAUSED / IN PROGRESS |
| WP-07..WP-27 | NOT STARTED |

## Important WP-06 state already established before pause

Do not roll back the following merely because House Rules/S6D were inserted:

- catalog generation remains `2.0.0`;
- engine prerelease identity remains `v1.0-alpha` / `engine_version: 1.0-alpha`;
- stable character choice-slot direction and strict character definition schemas already introduced during WP-06 remain valid inputs;
- typed Activity parameter/target/area/cost/roll protocol work already introduced remains valid input;
- `world.encounter` no longer owns procedure-local initiative/round operational state in the current machine inventory;
- WP-06 evidence proved that selector metadata and broader former-Step-6 rules/seed closure remain incomplete.

Later House Rules/S6D evidence may revise insufficient machine details, but does not discard them by default.

## Binding owner decisions

### Clean-slate pre-release structural canonicalization

```text
EXISTING USER CAMPAIGNS REQUIRING MIGRATION: NONE
BACKWARD-COMPATIBILITY REQUIREMENT FOR CURRENT SCAFFOLD: NONE
STRUCTURAL CANONICALIZATION: AUTHORIZED
FUTURE RELEASED-CAMPAIGN EVOLUTION POLICY: R2.7 WP-20
```

### Gameplay-first progressive character materialization

```text
GAMEPLAY MAY BEGIN BEFORE READY_PC: YES
EARLY PROVISIONAL DURABLE WRITE: YES
NAME REQUIRED FOR PROVISIONAL ACTOR: NO
READY_PC: initial mechanical commitment frontier, not complete dossier
SITUATION-AWARE RETROFIT: FORBIDDEN
SAFE POST-READY LAZY MATERIALIZATION: preserved
```

### Gameplay smoothness / hot-path performance

```text
NORMAL TURN: bounded/local execution from already-loaded working set
UNNECESSARY NETWORK/REPOSITORY ROUND-TRIP: FORBIDDEN
UNNECESSARY EXTRA LLM PASS: FORBIDDEN
BROAD ORDINARY-TURN INTEGRITY/REPOSITORY SCAN: FORBIDDEN
SLOW PATH: only for a concrete material trigger
```

House Rules and S6D must not weaken this requirement.

## House Rules design boundary to examine, not assume

The existing design brief proposes a two-channel direction:

```text
formalizable mechanic
    -> typed HDM definitions/policies/Activities/Rule Elements
    -> deterministic execution

nonformalizable/open-ended fiction judgment
    -> bounded LLM adjudication under campaign ruling/house-rule policy
    -> authorized typed input/proposal
    -> deterministic mechanics/RNG/state acceptance where applicable
```

This is **not yet canonical**. The next chat must run Step 1 of the full deep-design loop and may revise the framing.

The owner specifically suspects that `HOUSE_RULES.md` was intended to carry part of HDM logic that is not faithfully formalizable in Python and therefore must remain LLM-interpreted. That suspected responsibility must be researched and designed explicitly rather than silently removed by over-formalization.

## Eight-step rule

For House Rules, then for every numbered S6D task/domain, use the canonical `DEV/DESIGN_PROCESS.md` loop:

1. Architecture Task Brief
2. Research & Architecture Draft
3. Decision Brief
4. Collaborative Architecture Review
5. Candidate Specification
6. Adversarial Architecture Review
7. Resolution Gate
8. Canonicalization

The existing S6D plan is a work decomposition/coverage index only; do not execute Tasks 1–12 directly as a checklist.

## Recovery instruction

At the start of the next chat:

1. perform normal repository bootstrap;
2. read current roadmap;
3. read this status file;
4. read `2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`;
5. read the House Rules architecture design brief;
6. begin **House Rules Step 1 — Architecture Task Brief review/challenge**;
7. do not resume WP-06;
8. do not start S6D until House Rules Step 8 canonicalization closes;
9. after House Rules closes, process each numbered S6D task/domain through its own full eight-step cycle;
10. after S6D integrated closure, recover the full R2.7 pre-pause obligations from blob `d486825dc5c9463b2e2159086e6c7102c3caf354` plus House Rules/S6D closure artifacts and resume WP-06.

Conversation history is not a checkpoint.
