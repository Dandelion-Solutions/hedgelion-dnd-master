# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Owner Clarification Addendum

Status: **OWNER DIRECTION — INPUT TO DECISION BRIEF, NOT YET CANONICAL**

Date: 2026-08-20

Applies to:

- `2026-08-20-step-5-5-soft-hard-save-durability-research-draft.md`
- `2026-08-20-step-5-5-soft-hard-save-durability-analytical-challenge.md`

## 1. Explicit-save failure must not hard-lock play

Owner direction:

> If an explicit `save` / `сохрани игру` attempt fails while coherent HOT state still survives, do not hard-block the player merely because persistence is temporarily unavailable. The runtime should remain maximally friendly while being truthful about the durability risk.

Consequences:

- never acknowledge `saved` unless the promised save closure is actually durable;
- preserve the coherent HOT dirty state when publication failure does not itself invalidate it;
- report the save failure briefly and honestly;
- offer retry/repair when useful;
- if the player proceeds with ordinary gameplay, that continuation is allowed and merely increases the unpublished-loss exposure of the affected local/private scope;
- do not require a separate ritualized `continue without saving` confirmation when the player's next intent already makes that choice clear;
- a later successful save/forced publication includes the still-established dirty state according to the applicable accumulation scope and recovery closure;
- if HOT state is subsequently lost, recovery returns to the newest actually durable compatible source set and does not invent the unpublished continuation.

This friendly continuation rule does **not** waive an independent correctness-critical durability edge such as shared/live write-before-reveal, successful controlled handoff before relinquishment, or another domain contract whose semantic postcondition itself requires durability.

## 2. Risk-control exposure ceiling is not a correctness barrier

The analytical challenge initially recommended treating a fired singleplayer/private dirty-exposure ceiling as non-abandonable until publication succeeds. Owner direction toward friendly operation, combined with the already accepted risk model, changes that recommendation.

For a deferrable local/private scope, a maximum intended unpublished-exposure policy is a **risk-control/SLO policy**, not proof that state becomes semantically invalid after the configured age.

When its threshold is reached at an available runtime opportunity:

```text
unpublished local/private SOFT exposure reaches configured policy threshold
    -> request/attempt durability closure
    -> if success: exposure resets for included state
    -> if failure: warn/record degraded durability condition, keep coherent HOT state usable
    -> retry at later suitable opportunities
```

It SHALL NOT, by itself, permanently block ordinary singleplayer/private gameplay while coherent HOT state survives.

The policy still has operational force:

- the runtime should attempt the flush before needlessly extending stale exposure when an execution opportunity exists;
- repeated/continued failure should remain visible as degraded durability rather than silently pretending the target exposure is satisfied;
- no background callback means there is no guarantee of publication at the exact wall-clock threshold;
- clean state produces no heartbeat publication;
- no universal numeric threshold is canonicalized by Step 5.5.

The distinction is deliberate:

```text
RISK-CONTROL BOUNDARY
    protects against larger RPO/loss exposure
    failure may degrade protection while play continues

SEMANTIC/CORRECTNESS DURABILITY EDGE
    durability is part of the edge's truth/visibility/ownership postcondition
    edge itself cannot be acknowledged/crossed as successful without durability
```

Examples of the second category include current same-scene shared write-before-reveal semantics and Step-5.4 recovery-safe handoff acknowledgement.

## 3. Scope-aware exposure remains required

The previous owner clarification remains in force:

- no campaign-global dirty timeout;
- exposure policy belongs to a durability/authority/visibility scope or partition;
- singleplayer/private scopes may tolerate comparatively long unpublished exposure because host/context loss is the primary risk;
- multiplayer shared scopes generally require stronger event-driven durability/visibility edges;
- same-scene live shared state is expected to publish at logical-action granularity before shared reveal;
- Step 5.8 owns the concrete multiplayer/live bindings and authority mechanics.

## 4. Decision-brief effect

The refined Step-5.5 recommendation should therefore distinguish:

1. **SOFT deferral / risk-control publication policy** — allowed to degrade temporarily after publication failure while HOT state survives;
2. **explicit SAVE promise** — success acknowledgement requires durability, but failed save does not hard-lock subsequent local/private play;
3. **correctness-critical HARD edge** — the named semantic edge cannot be acknowledged/crossed as successful until its required durability closure holds;
4. **controlled handoff** — governed by Step 5.4 and remains non-successful until recovery-safe durability succeeds.

This supersedes the analytical-challenge recommendation that a fired local/private exposure ceiling be non-abandonable at runtime.
