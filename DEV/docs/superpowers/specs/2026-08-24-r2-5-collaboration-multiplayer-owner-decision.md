# R2.5 Owner Decision — Multiplayer Collaboration and Dramaturg Coordination

Status: **OWNER-APPROVED ARCHITECTURE PROGRAM DECISION**

Date: 2026-08-24

Decision basis:

- R2.5 task brief;
- R2.5 collaboration/multiplayer evidence ledger;
- R2.5 agency/dramaturg coordination evidence addendum;
- `2026-08-24-r2-5-collaboration-multiplayer-decision-brief-v2.md`;
- owner discussion/clarification resolving agency waiting and shared/local Dramaturg semantics.

---

## 1. Decision

The owner approves:

> **B3 — AGENCY-SAFE SCOPED COLLABORATION + TWO-LEVEL DRAMATURG COORDINATION**

The earlier Decision Brief alternative B is superseded by the B3 formulation in Decision Brief v2.

This decision approves semantic architecture direction. It does not approve exact schemas, file paths, persistence roots, IDs, timeout values, prompt text, provider-specific mechanisms or implementation.

---

## 2. Owner-approved product semantics

### 2.1 Agency-safe asynchronous progression

HDM may intentionally pause/slow a dependent fictional scope when continuing now would materially consume another player's still-valid voluntary decision/reaction opportunity.

It should resolve as far as safely possible first: the stop point is the **maximal safe frontier**, not an arbitrary earlier global freeze.

Independent scopes remain free to continue.

Silence/absence is not consent and does not authorize acting for another player-controlled PC. Conversely, absence does not grant immunity from automatic consequences when no genuine applicable player decision/reaction exists.

Players may coordinate outside HDM through any channel, but one player's report of another player's intended voluntary action is not authority over that other PC.

### 2.2 Scoped collective input

A bounded collaboration/window semantic is allowed when several human contributions must survive across participant/chat gaps before one dependent shared resolution and no native rules/execution owner already owns the responder/order semantics.

Strict ordered mechanics remain owned by their native Procedure/Continuation/Reaction/Choice/equivalent contracts.

### 2.3 Two-level Dramaturg coordination

In multiplayer, Dramaturg preparation has two retained noncanonical scopes:

1. **player-local Dramaturg horizon** — bounded near-horizon preparation for one player's current trajectory/scene;
2. **shared Dramaturg horizon** — campaign-level preparation coordination across player chats.

The shared upper level exists only when multiplayer is enabled. Singleplayer does not create it merely for architectural symmetry.

All player-local horizons and the shared horizon operate over one campaign repository and one canonical world/history. Local horizons may develop independently in focus, tone and near-term possibilities but must remain compatible with current canon and applicable shared planning constraints.

### 2.4 Preparation is never plot authority

The owner explicitly reaffirms:

> **HISTORY IS NOT WRITTEN IN ADVANCE.**

A preparation artifact describes possibilities, pressures, likely reactions and conditional developments. It has no entitlement to occur.

Any accepted player decision, NPC/Actor decision, mechanic or causal development may overturn prepared direction and send play elsewhere.

Canonical law to preserve:

> **CANON INVALIDATES PREPARATION; PREPARATION DOES NOT CONSTRAIN CANONICAL PLAYER OR ACTOR FREEDOM.**

Shared coherence constrains Dramaturg preparation, not player choices or lawful Actor decisions.

The engine must not manufacture replacement twists, duplicate actors/items, coincidences or coercive redirection solely to restore an invalidated prepared trajectory.

### 2.5 Lazy planning retrieval

Because all chats share one campaign repository, any Dramaturg may discover relevant preparation/developments from other player lines when needed. This is not a requirement to preload all Dramaturg material.

R2.3 lazy discovery/select/load/project applies to local/shared planning horizons. Full planning slices load only when materially relevant to the current Dramaturg task.

No background rewrite of every local horizon is required whenever another player advances.

---

## 3. Authority separation

The approved composition is:

```text
LIVE/current owners
    factual mutable-scene consistency

CHRONOLOGY
    causal/order consistency across independent scopes

R2.5 collaboration
    preserve still-open human agency / collect bounded joint input

R2.5 Dramaturg horizons
    preserve noncanonical planning coherence across independent Masters
```

No layer substitutes for another.

The shared/local Dramaturg horizons are not:

- world truth;
- current state authority;
- chronology authority;
- player/PC knowledge authority;
- disclosure authority;
- mechanical execution authority;
- a global plot database;
- a campaign director;
- a story scheduler.

---

## 4. S14 trigger decision

The owner accepts the evidence conclusion that the preserved S14 revisit trigger has fired narrowly in multiplayer.

S14 is activated only for retained inspectable noncanonical planning continuity needed by multiple independent Dramaturg phases:

- player-local horizon;
- multiplayer-only shared horizon.

This does **not** create a standalone Narrative Dynamics roadmap stage or generic planning framework.

---

## 5. Candidate-spec mandate

The R2.5 candidate specification SHALL formalize at least:

- mode/scope coordination families;
- maximal-safe-frontier / agency-dependency semantics;
- collective window lifecycle and authority limits;
- native ordered-owner precedence;
- OOC/diegetic/action/control separation;
- join/rejoin/catch-up composition;
- player-local/shared Dramaturg horizon relationship;
- source-anchored constraint vs provisional planning distinction;
- lazy planning discovery/revalidation;
- no-entitlement/no-plot-restoration laws;
- cross-scene/live/chronology composition;
- failure/obsolete/supersession behavior;
- Diamond/Strong item-level disposition including newly activated S14.

Adversarial review must challenge both false waiting and premature progression, as well as factual/planning authority contamination and cross-chat genre/ontology drift.

Broad implementation remains unauthorized.