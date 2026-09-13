# HDM Implementation Planning — Decomposition Critic Amendment

Status: **ACTIVE TASK-LOCAL PROCESS AMENDMENT**

Date: 2026-09-13

Applies to `DEV/docs/superpowers/design/2026-09-13-implementation-planning-task-brief.md` and the current implementation-planning route in `DEV/CURRENT_PROGRESS.md`.

This amendment records the Product Owner requirement to validate the implementation decomposition independently before detailed executable plans are authored and before production implementation begins. It changes no accepted product semantics, architecture owner, readiness disposition, activation state, or version/migration law.

## Required route

```text
P1/P2 readiness + active-set reconciliation
-> P3 dependency DAG
-> candidate bounded plan/task decomposition
-> independent Decomposition Critic
-> repair / re-decompose / re-review until PASS
-> detailed executable plans + Impact Envelopes + proof/version/HG-01 routing
-> execution waves + bidirectional coverage/currentness package
-> final independent Senior plan review
-> repair / re-review until PASS / GO
-> production implementation only after Senior GO
```

The Decomposition Critic is an autonomous planning quality gate, not an additional Product Owner/Senior approval stop. A human stop occurs only if it exposes a genuine human-owned product, architecture, scope, compatibility, or material-risk decision.

## Candidate decomposition input

Before the critic runs, the planner must produce a candidate decomposition concrete enough to challenge, but must not yet spend effort on full execution-ready `writing-plans` artifacts. It must show:

- active readiness/proof obligations mapped to candidate implementation units or exact proof-only routes;
- proposed plan/task boundaries;
- native owners and expected owner/consumer surfaces;
- P3 dependency edges, parallel roots, joins and integration points;
- preserved deferred/dormant/no-work/future-triggered items;
- negative laws and out-of-scope surfaces;
- preliminary impact boundaries sufficient to detect hidden coupling.

This candidate belongs under `DEV/docs/superpowers/design/`. Execution-ready plans remain under `DEV/docs/superpowers/plans/` only after critic PASS.

## Critic obligations

The independent critic must reconstruct the relevant whole-project dependency subgraph from current repository owners and actively test for:

- missing or duplicate leaf coverage;
- false ordering and hidden dependencies;
- incorrect parallelism or unnecessary serialization;
- owner responsibilities merged or fragmented for convenience;
- units that are too large or artificially tiny;
- dependency cycles hidden by arbitrary ordering;
- proof-only obligations turned into fake subsystems;
- implementation work lacking required proof routes;
- dormant/deferred/future/no-work obligations activated prematurely;
- rejected architecture reintroduced by plan boundaries;
- hidden cross-plan coupling or missing integration joins;
- plan boundaries that silently make a new human-owned architecture/product decision.

The critic is allowed to reject the candidate decomposition completely and propose a different cut.

## Gate

All `BLOCKING` and `SIGNIFICANT` decomposition findings must be repaired and independently re-reviewed before detailed executable plan authoring proceeds.

```text
DECOMPOSITION_CRITIC_REQUIRED: YES
DECOMPOSITION_CRITIC_STATUS: NOT_REACHED
DETAILED_EXECUTABLE_PLAN_AUTHORING_BEFORE_PASS: NOT_AUTHORIZED
FINAL_SENIOR_PLAN_REVIEW_REQUIRED: YES
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_OWNER_DECISION_REQUIRED_NOW: NO
ARCHITECTURE_REOPEN_REQUIRED_NOW: NO
VERSION_IMPACT: NONE
```

P1/P2 remain complete. The immediate next authorized unit remains P3. After P3, candidate decomposition and the Decomposition Critic occur before full executable plan authoring. The final Senior plan review remains the mandatory gate immediately preceding production implementation authorization.
