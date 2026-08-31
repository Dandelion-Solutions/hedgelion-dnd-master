# Step 5.12 — Minimal Host Delivery Scope — Owner Decision

Status: **OWNER-APPROVED PRODUCT / SCOPE DECISION**

Date: 2026-08-21

Applies to: Step 5.12 / Host Delivery & Disclosure Boundary

## Decision

HDM baseline SHALL NOT build a heavyweight reliability subsystem around player interruption of Master output, host-side Retry/regeneration, editing of old host messages, or recovery of partially/ambiguously delivered secrets.

The product may document that ChatGPT can technically be interrupted while the Master is responding, but doing so is discouraged because the player may miss important information. The same principle applies to using host history-edit/retry features as if they were gameplay rewind/correction controls: they are not supported campaign-history editing mechanisms.

The architecture should include only cheap protections that preserve existing authority boundaries and do not materially increase normal-turn latency, repository traffic, runtime state machinery, or token/model-call cost.

## Product rationale

Ordinary HDM turns already have a tight response-time and orchestration budget. Step 5.12 must not introduce an outbox, per-segment acknowledgement ledger, background relay, mandatory post-delivery write, retry worker, or generic partial-stream reconstruction mechanism merely to make uncommon host interruption perfectly recoverable.

The project accepts a bounded presentation risk:

> A player who interrupts the Master, rewrites/retries host history, or experiences an unusual host-delivery failure may miss or duplicate some presentation information. HDM should avoid making this worse, but baseline correctness does not promise perfect reconstruction of such host-side presentation failures.

Gameplay truth, mechanics, pending choices/obligations, fictional knowledge, and other canonical semantics remain protected by their existing owners and MUST NOT depend solely on a successful host-delivery record.

## Required simplification consequences

1. **No baseline durable delivery outbox.**
   - no `pending_delivery` authority;
   - no delivery worker/lease/heartbeat;
   - no mandatory pre-send Git commit solely for delivery reliability.

2. **No baseline partial-stream ledger.**
   - no token/chunk exposure frontier;
   - no per-prefix disclosure accounting;
   - no requirement to recover which subset of an interrupted response was visually rendered.

3. **No baseline host-history rewrite support.**
   - editing an old user message does not retcon accepted campaign history;
   - Retry/regeneration of an old assistant response does not replay accepted mechanics/canon;
   - Branch-from-old-history is not campaign recovery authority;
   - players should use a new message/correction through ordinary HDM semantics when they want to change or clarify something already accepted.

4. **No requirement for exactly-once player-visible prose.**
   - duplicate or missed presentation after abnormal host behavior is an accepted bounded product limitation;
   - deterministic gameplay/execution MUST still remain no-double/no-replay under existing Step-3/Step-5 laws.

5. **Cheap integrity protections remain required.**
   - narration/disclosure refs must be validated before the response is committed to the player-facing output path;
   - gameplay-significant pending communication requirements must remain owned by their native gameplay/runtime owners, not by delivery bookkeeping;
   - player-visible tool/commentary surfaces must not bypass information-eligibility rules;
   - re-presenting an already-established fictional communication must not invent a new fictional action merely to repair presentation.

## Baseline boundary preference

Step 5.12 should prefer the lightest practical semantic boundary available in ordinary ChatGPT:

```text
resolved state
    -> validated NarrationResult / player-visible payload frozen
    -> output committed to the host response path
    -> corresponding outbound communication/disclosure evidence may be established
```

The baseline does **not** require proof that the human literally read the text, nor perfect proof that every byte/segment rendered after the output was committed.

A future host/deployment profile MAY exploit stronger trustworthy acknowledgement or exact established-message identity when that capability is available cheaply. Such support is an optimization/quality improvement and must not make the baseline architecture depend on Work, Pro/Enterprise-only features, background agents, or an always-running external service.

## Documentation requirement

Player-facing documentation/help SHOULD state in substance:

> You can technically interrupt the Master because ChatGPT allows it, but this is not recommended during play: you may miss important information. If you need to correct or clarify something, send a new message instead of treating edit/retry of old chat history as a campaign rewind.

Exact public wording belongs to later documentation implementation and need not be copied verbatim from this decision.

## Decision rights

This is an explicit owner acceptance of the presentation-reliability trade-off in exchange for lower runtime complexity, latency and maintenance burden.

It does not relax correctness requirements for canonical gameplay state, deterministic execution, multiplayer authority, truth/knowledge separation, or durable recovery.