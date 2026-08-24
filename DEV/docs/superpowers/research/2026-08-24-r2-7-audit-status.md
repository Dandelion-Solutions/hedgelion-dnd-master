# R2.7 — Audit Status / Durable Cursor

Status: **PAUSED BY OWNER — HOUSE RULES STEP 1 COMPLETE / STEP 2 NEXT; S6D AFTER**

Date: 2026-08-24

Execution protocol:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-audit-execution-protocol.md`

R2.7 task brief:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`

Current sequencing owner:

- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

House Rules design input:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

House Rules Step-1 Task Brief:

- `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`

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
HOUSE_RULES_STATUS: STEP 1 COMPLETE / STEP 2 RESEARCH NEXT
HOUSE_RULES_TASK_BRIEF: DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md
HOUSE_RULES_NEXT: Step 2 — Research & Architecture Draft

FOLLOWING_WORKSTREAM: S6D — Step-6 Residual Rules/Seed Debt Closure
S6D_STATUS: PREPARED / NOT STARTED
S6D_EXECUTION_RULE: each numbered task/domain runs its own full 8-step deep-design loop
S6D_START_TRIGGER: House Rules Step 8 canonicalization complete
R2_7_RESUME_TRIGGER: S6D integrated closure/resolution gate complete
```

The roadmap still owns program sequencing. If its narrative continuation text still says that the next chat begins House Rules Step 1, this durable cursor is the later workstream-progress record: Step 1 is now complete and Step 2 is next. The sequencing itself is unchanged.

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

## House Rules design boundary — Step-1 challenge result

The design input proposed a two-channel direction:

```text
formalizable mechanic
    -> typed HDM definitions/policies/Activities/Rule Elements
    -> deterministic execution

nonformalizable/open-ended fiction judgment
    -> bounded LLM adjudication under campaign ruling/house-rule policy
    -> authorized typed input/proposal
    -> deterministic mechanics/RNG/state acceptance where applicable
```

Step 1 did **not** accept that decomposition as canonical. The Task Brief classifies it as a useful hypothesis and requires Step 2 to test whether representation/execution form, lifecycle/durability and authority/ownership are better treated as independent axes.

Step 1 also established these framing corrections:

- the design brief's Section 13 allowance for early independent S6D work is stale and superseded by the sequencing owner decision;
- `HOUSE_RULES.md` must not be assumed to own every durable campaign ruling because its current file contract is narrower than the ruling precedence/persistence language in `PLAY_POLICY.md`;
- a new `GAME/CORE/RULINGS.md`, generic ruling record/DSL, stable ruling ID schema or specific typed receiving surface must be justified by evidence rather than embedded in the assignment;
- examples such as `fiction.target_reachable` are illustrative and do not prove an existing canonical machine type;
- retrieval/discoverability is part of correctness because durable precedent must remain applicable without introducing an ordinary-turn full-corpus/repository scan;
- the intended LLM-readable campaign policy responsibility remains explicitly in scope and must not be silently eliminated by over-formalization.

Full details and Step-2 Source Manifest/questions/alternatives are in the Step-1 Task Brief.

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
5. read `2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md` as noncanonical design input;
6. read `2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md` as the completed Step-1 framing and current research assignment;
7. begin **House Rules Step 2 — Research & Architecture Draft** using its Source Manifest/evidence gates;
8. do not resume WP-06;
9. do not start S6D until House Rules Step 8 canonicalization closes;
10. after House Rules closes, process each numbered S6D task/domain through its own full eight-step cycle;
11. after S6D integrated closure, recover the full R2.7 pre-pause obligations from blob `d486825dc5c9463b2e2159086e6c7102c3caf354` plus House Rules/S6D closure artifacts and resume WP-06.

Conversation history is not a checkpoint.
