# R2.4 — Chronicler Service Opportunity — Owner Clarification

Status: **OWNER-APPROVED PRODUCT/ARCHITECTURE CLARIFICATION**

Date: 2026-08-24

Applies to:

- active R2.4 single-context LLM execution design;
- Step-5.10 Story projection activation policy;
- the current one-chat / one-assistant-turn baseline.

## 1. Owner clarification

The Chronicler must not be treated as merely optional or indefinitely opportunistic.

Story projection may lag while the current turn is genuinely load-critical, including examples such as:

- substantial scene formation requiring heavy Dramaturg work;
- active/high-pressure scenes with many simultaneous participants or decisions;
- serialization/save/publication/recovery work;
- another correctness/latency-critical turn whose required phases consume the available budget.

However, deferred Chronicler work remains an outstanding service obligation.

> **Whenever compatible Story backlog exists, the runtime SHALL attempt Chronicler/Story catch-up at the first safe execution opportunity and SHALL continue servicing bounded backlog windows on subsequent safe opportunities until compatible coverage catches up.**

Repeated deferral does not cancel the obligation.

## 2. Compatibility with Step 5.10

This clarification deliberately does not introduce a durable job queue, scheduler, background worker or Story freshness authority.

Step 5.10 already defines backlog as:

```text
current typed source-domain basis/watermark
    minus
compatible Story-layer coverage
```

and already permits foreground opportunity activation while keeping gameplay authority independent of Story freshness.

R2.4 strengthens only the **activation/service policy** for the current product baseline.

The Step-5.10 weaker product statement `eventual/opportunistic; no SLA` is therefore refined for this deployment profile as follows:

```text
no wall-clock / fixed-turn freshness SLA
no background-worker guarantee
BUT
first-safe-opportunity service obligation
```

## 3. Safe opportunity semantics

A `Chronicler service opportunity` exists when all of the following hold conceptually:

1. compatible Story backlog is non-empty;
2. current gameplay correctness/agency/mechanics requirements have reserved enough context/reasoning/output budget;
3. the turn is not blocked by a load-critical scene-construction, high-pressure multi-participant, persistence/save, recovery/conflict or equivalent higher-priority operation;
4. a bounded Story catch-up window can execute without violating the current gameplay latency/quality envelope;
5. Step-5.10 source/coverage/publication prerequisites for that bounded window can be satisfied.

The exact host-specific budget threshold is not fixed in R2.4; R2.6 validates it.

## 4. Priority law

Current-turn correctness-critical work remains higher priority than Chronicler catch-up.

Once those requirements and the protected Narrator/output margin are reserved, backlogged Chronicler service outranks optional enrichment/ornamental work that is not required for the current turn.

This means the runtime may defer Chronicler for genuinely heavy work, but it may not repeatedly spend spare capacity on nonessential elaboration while Story backlog remains serviceable.

## 5. Bounded service, not full catch-up in one turn

One opportunity does not require draining an arbitrarily large backlog.

The runtime selects a bounded uncovered Story window under Step 5.10, runs the required deterministic and/or Chronicler transformation, validates it, and advances Story coverage only through the normal deterministic Story publication contract.

If backlog remains, the service obligation remains active for the next safe opportunity.

## 6. Chronicler role versus deterministic Story transform

Step 5.10 permits deterministic transformation for layers/operations that do not require generative/editorial judgment.

This clarification therefore means:

- when a bounded Story window requires generative/editorial transformation, the **Chronicler logical role** must be activated at the safe opportunity;
- when an accepted Story transformation is deterministic, deterministic Story control may service that portion without inventing an unnecessary LLM phase;
- neither form changes Story/canon authority boundaries.

## 7. No Git-write-per-turn requirement

`service opportunity` is not equivalent to `publish one Story commit after every gameplay turn`.

Step-5.10 bounded source windows, layer-local coverage, deterministic validation and publication remain in force. The activation policy may coalesce a useful bounded window and may defer while gameplay/persistence contention makes Story work unsafe.

The requirement is that service is not forgotten or starved once a useful safe opportunity exists.

## 8. R2.4 consequence

The R2.4 turn planner SHALL evaluate Chronicler/Story service opportunity in every ordinary TurnEnvelope.

Conceptually:

```text
plan current-turn required gameplay phases
reserve correctness + Narrator/output budget
inspect typed Story backlog

if backlog empty:
    no Chronicler service

if backlog non-empty and safe opportunity exists:
    schedule bounded Chronicler/Story service

if backlog non-empty and blocked:
    defer for typed reason
    obligation remains
```

A persistent `StoryProjectionJob` is still not required because backlog and service need are recomputable from existing Story coverage plus current source basis.

## 9. Decision effect

This clarification supersedes any R2.4 draft/brief wording that describes Chronicler as merely `opportunistic/non-hot-path` without an anti-starvation / first-safe-opportunity obligation.

It does not approve the remaining R2.4 A/B/C choreography choice by itself.
