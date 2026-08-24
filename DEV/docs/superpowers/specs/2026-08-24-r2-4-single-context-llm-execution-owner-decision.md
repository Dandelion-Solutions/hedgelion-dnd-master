# R2.4 Owner Decision — Registered Turn Envelope with Chronicler First-Safe-Opportunity Service

Status: **OWNER-APPROVED ARCHITECTURE DECISION**

Date: 2026-08-24

Applies to:

- R2.4 Single-Context LLM Execution & Instruction Architecture;
- `2026-08-24-r2-4-single-context-llm-execution-decision-brief-v2.md`;
- `2026-08-24-r2-4-chronicler-service-owner-clarification.md`.

## 1. Decision

The owner approves:

> **Alternative B — Registered Turn Envelope + Minimal Typed Gateways + first-safe-opportunity Chronicler service.**

This approval adopts the semantic direction and laws in Decision Brief v2. It does not approve final schema syntax, exact prompt wording, exact tool-call count, host-specific timing thresholds, buffering implementation or provider abstraction.

## 2. Approved baseline

Ordinary gameplay remains:

```text
one user request
one assistant turn
one physical conversational context
```

Within that turn HDM may execute several explicit logical role phases without requiring one model call per role.

The registered `TurnEnvelope` owns the legal phase vocabulary/order constraints, current deterministic frontier, role/subject/purpose binding boundaries, permitted typed handoffs, and Chronicler service-opportunity evaluation.

The LLM may propose optional semantic work but cannot self-grant additional source eligibility, authority, a new phase family, or cancellation of a registered service obligation.

## 3. Chronicler requirement

Compatible Story backlog creates a deferred service obligation evaluated on every ordinary `TurnEnvelope`.

Current-turn correctness, agency, mechanics, required Dramaturg/Actor work and protected Narrator/output capacity take priority.

After those requirements are reserved:

- if backlog is empty: no Story service;
- if backlog exists and a safe bounded window exists: Story/Chronicler service is mandatory;
- if backlog exists but the turn is genuinely load-critical or the bounded service prerequisites cannot be met: defer for a typed reason; the obligation remains;
- residual backlog remains eligible for the next safe opportunity.

No fixed every-N-turn SLA, background worker, durable Story job queue or Story Git write per gameplay turn is required.

## 4. Explicitly rejected baseline alternatives

### A — Model-Directed Collapsed Orchestration

Rejected because phase omission and Chronicler starvation are insufficiently inspectable and because the model cannot be allowed to self-grant or silently cancel role/context/service obligations.

### C — Deterministic Explicit Phase FSM / Checkpoint per Role

Rejected as baseline overengineering. It adds hot-path checkpoints and lifecycle machinery not justified by current requirements or evidence. It remains a possible future defense/profile option if later host/evaluation evidence proves necessary.

## 5. Boundaries preserved

This decision does not reopen:

- Step-3 deterministic mechanics/RNG/state authority;
- Step-4 logical role/eligibility/disclosure architecture;
- Step-5.10 Story coverage/publication authority;
- Step-5.12 Narrator validation/`EMISSION_COMMIT` semantics;
- R2.1 continuity authority boundaries;
- R2.2 Actor continuity/cognition ownership;
- R2.3 Context Runtime discovery/eligibility/packet allocation.

Broad implementation remains blocked pending Round-2 architecture closure and implementation planning.
