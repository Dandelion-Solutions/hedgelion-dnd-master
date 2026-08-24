# R2.4 Evidence Addendum — Chronicler Service Opportunity

Status: **RESEARCH EVIDENCE / OWNER-CLARIFICATION RECONCILIATION**

Date: 2026-08-24

Owner clarification:

- `../specs/2026-08-24-r2-4-chronicler-service-owner-clarification.md`

## 1. Why this addendum exists

The initial R2.4 evidence ledger summarized Chronicler as `opportunistic/non-hot-path`. That wording was incomplete because it preserved Step-5.10 nonblocking behavior but did not encode an anti-starvation/service obligation.

The owner clarified that Chronicler may defer under heavy scene/Dramaturg load, intense multi-participant play, serialization/save/recovery or equivalent pressure, but must be serviced whenever a safe opportunity appears and must not be allowed to drift indefinitely.

## 2. Step-5.10 evidence

Current Step-5.10 canonical architecture already provides the required substrate:

- Story may lag without affecting gameplay truth/recovery authority;
- no background worker is required;
- backlog is derived from typed source-domain basis/watermark minus compatible Story coverage;
- no durable `StoryProjectionJob`, worker claim ledger or scheduler is baseline authority;
- bounded catch-up enumerates an uncovered source window, transforms/curates it, validates output and advances coverage only with coherent Story publication;
- activation policy may include a foreground opportunity;
- Chronicler remains editorial/generative only; deterministic Story control owns source selection, validation, final IDs, publication and coverage;
- deterministic transforms are permitted where an LLM Chronicler is unnecessary;
- gameplay remains higher priority under same-ref contention.

Step-5.10 resolution explicitly rejected mandatory Story projection after every canonical turn because of latency/token cost, while leaving Step-6/Round-2 activation policy open.

## 3. Reconciliation

The owner clarification does **not** reopen Step-5.10 durability/authority architecture.

It selects a stronger R2.4 activation policy over the existing queue-free backlog model:

```text
Story correctness requirement:
    remains independent of freshness

Story service product requirement:
    backlog must be serviced at first safe opportunity
```

There is still:

- no wall-clock freshness SLA;
- no fixed `every N turns` rule;
- no required background execution;
- no Story participation in gameplay correctness/save authority;
- no durable job queue.

The anti-starvation guarantee is opportunity-based rather than timer-based.

## 4. Turn-envelope consequence

Every TurnEnvelope must make a bounded Story service decision from current evidence:

```text
backlog_state
current required phase load
protected Narrator/output margin
persistence/recovery contention
bounded Story work estimate
    -> SERVICE | DEFER(reason) | NO_BACKLOG
```

`DEFER(reason)` is not a persisted job lifecycle. The next envelope can recompute backlog from source basis and Story coverage.

## 5. Priority synthesis

The safe priority order is semantic, not necessarily literal execution order:

1. correctness-critical current-turn work and player agency;
2. required Actor/Dramaturg/mechanical work for the current situation;
3. protected Narrator/output capacity;
4. bounded Chronicler/Story catch-up when backlog exists and fits safely;
5. nonessential optional enrichment/ornamental work.

Thus Chronicler does not preempt an intense scene, but backlogged Story must not repeatedly lose to optional flourish once the current turn has spare capacity.

## 6. Batch semantics

A safe opportunity guarantees **bounded service**, not full catch-up.

If the backlog is large:

```text
safe turn 1 -> bounded window
safe turn 2 -> next bounded window
...
```

until compatible coverage catches up, subject to intervening high-priority turns.

## 7. R2.4 decision impact

The A/B/C choreography alternatives remain materially distinct.

The owner clarification strengthens Alternative B because a registered TurnEnvelope can explicitly evaluate and trace Chronicler service opportunity without requiring a rigid role FSM or a generic scheduler.

Alternative A becomes weaker: purely model-directed orchestration provides no robust anti-starvation evidence that Chronicler backlog was checked or deliberately deferred.

Alternative C can enforce the policy but still carries unnecessary per-role checkpoint/FSM overhead.

Recommendation remains **Alternative B — Registered Turn Envelope + Minimal Typed Gateways**, now with a first-safe-opportunity Chronicler service law.
