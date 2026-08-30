# Owner Decision — House Rules First, Then S6D via Full Eight-Step Deep-Design Cycles

Status: **OWNER-APPROVED SEQUENCING DECISION / CURRENT HANDOFF AUTHORITY**

Date: 2026-08-24

## 1. Decision

R2.7 remains paused at WP-06.

The next architecture work is not direct continuation of WP-06 and not direct execution of the existing S6D checklist.

The owner-approved sequence is:

```text
R2.7 WP-06 PAUSED
    -> Campaign Rulings / House Rules architecture
         full canonical eight-step deep-design loop
    -> House Rules canonicalization complete
    -> S6D residual rules/seed debt closure
         each numbered S6D task/domain gets its own full eight-step deep-design loop
    -> S6D integrated closure / resolution gate
    -> R2.7 WP-06 resume from saved durable checkpoint
    -> R2.7 WP-07..WP-27
```

No S6D task may be executed as a mere bounded checklist item merely because an older execution plan already exists.

## 2. Canonical eight-step loop

For House Rules and for every numbered S6D task/domain, follow `DEV/DESIGN_PROCESS.md` Part III without skipping steps:

1. **Architecture Task Brief** — formulate and challenge the assignment itself; build/refine the Source Manifest and exit criteria.
2. **Research & Architecture Draft** — inspect owning sources, extract evidence/qualifiers, reconcile amendments/consumers, analyze alternatives, and make a recommendation.
3. **Decision Brief** — present the decision-ready delta, recommendation, uncertainty, and exact residual human decision.
4. **Collaborative Architecture Review** — owner decides only genuine product/architecture trade-offs; nested research loops resolve material unknowns.
5. **Candidate Specification** — write one concrete architecture after significant choices are settled.
6. **Adversarial Architecture Review** — attack requirement fit, authority, state/invariant boundaries, failure/retry/recovery, latency, YAGNI, LLM/deterministic boundaries, and evidence completeness.
7. **Resolution Gate** — resolve all blocking/significant findings; return only genuine residual trade-offs to the owner; repeat candidate/adversarial loop if material changes require it.
8. **Canonicalization** — final consistency/traceability/self-review, canonical artifact, roadmap/status update, and exact next continuation point.

The Source Manifest/evidence-extraction/synthesis-completeness gates remain mandatory before Decision Brief, candidate specification, coverage claims, or canonicalization.

## 3. House Rules workstream — NEXT

Start from:

- `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`

That file is a **design-brief input**, not a canonical result. The next chat must begin by reviewing/challenging the brief under Step 1 rather than treating its proposed two-channel model, lifecycle, `RULINGS.md`, or `HOUSE_RULES.md` shape as already settled.

The architectural question includes the suspected intended responsibility of the LLM-readable rules layer: HDM must preserve a legitimate place for campaign-specific/open-ended logic that cannot be faithfully reduced to Python/catalog mechanics, while ensuring that LLM judgment does not acquire direct authority over engine-owned state, RNG, or deterministic mutation.

House Rules canonicalization must settle at least:

- the boundary between formalizable deterministic mechanics and nonformalizable/open-ended LLM adjudication;
- one-off adjudication vs temporary ruling vs durable campaign precedent vs deliberate house rule;
- what `HOUSE_RULES.md` is allowed to own;
- whether durable rulings need stable identity/scope/status/supersession structure and in what physical form;
- how LLM-only judgments become typed execution inputs/proposals;
- when recurring rulings should or should not be formalized;
- precedence/conflict/supersession/correction semantics;
- traceability without chain-of-thought persistence;
- latency discipline so ordinary play remains one bounded local reasoning/execution flow where possible.

S6D does not start until this House Rules design completes Step 8 canonicalization.

## 4. S6D execution rule after House Rules closes

Existing S6D artifacts remain useful decomposition/evidence inputs:

- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/design/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

However, the plan is now a **workstream decomposition and coverage index**, not permission to execute Tasks 1–12 directly.

Each numbered S6D task/domain must be treated as its own architecture/deep-work block and pass the full eight-step loop above before it is considered closed. If a numbered task reveals multiple independently material architecture sub-blocks, decompose them further rather than forcing them into one reasoning run.

Technical details that follow unambiguously from approved architecture remain agent-owned inside each cycle; stop for the owner only when a genuine product-semantic, authority, material trade-off, compatibility, risk-acceptance, or scope decision remains.

## 5. R2.7 recovery boundary

The immutable pre-pause R2.7 state remains preserved by the current audit status artifact and its recorded pre-pause blob SHA. Do not reconstruct WP-01..WP-06 obligations from chat history.

After House Rules and S6D canonical closure, resume WP-06 from that repository checkpoint plus the newly canonical House Rules/S6D outputs.

## 6. New-chat start instruction

After normal repository bootstrap, read in order:

1. `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
2. `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-status.md`;
3. this owner decision;
4. `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-design-brief.md`;
5. canonical design-process owners.

Then begin **House Rules Step 1 — Architecture Task Brief review/challenge**. Do not resume WP-06 and do not start S6D first.

Conversation history is not a checkpoint.
