# R2.5 Candidate Specification — Agency-Safe Collaboration and Two-Level Dramaturg Coordination

Status: **CANDIDATE SPECIFICATION / PRE-ADVERSARIAL REVIEW**

Date: 2026-08-24

Owner-approved direction:

> **B3 — AGENCY-SAFE SCOPED COLLABORATION + TWO-LEVEL DRAMATURG COORDINATION**

This candidate formalizes the owner decision. It does not implement schemas/runtime code or choose physical storage paths.

---

## 1. Central invariant

Multiplayer consists of multiple independent participant ChatGPT TurnEnvelopes operating over one campaign repository and one canonical world/history.

R2.5 adds only two missing semantic responsibilities:

```text
COLLABORATION
    preserve still-open human agency across asynchronous participant timing
    and collect bounded joint contributions when needed

DRAMATURG COORDINATION
    preserve compatible noncanonical preparation across independent Masters
```

Existing owners remain authoritative for world/live truth, mechanics, chronology, knowledge/disclosure, player binding and persistence.

---

## 2. Coordination families

Canonical candidate families:

```text
INDEPENDENT_IMMEDIATE
AGENCY_DEPENDENT_COLLECTIVE
RULE_OWNED_ORDERED
```

### INDEPENDENT_IMMEDIATE

The current participant input may resolve immediately when no other human-controlled contribution remains materially relevant to the dependent consequence.

### AGENCY_DEPENDENT_COLLECTIVE

The current scope may progress only to the maximal safe frontier because one or more other human-controlled contributions remain materially capable of changing the dependent result.

### RULE_OWNED_ORDERED

A native Procedure/Continuation/Reaction/Choice/equivalent contract already owns admissible responder/order semantics.

## LAW R2.5-1 — NO GLOBAL ACTIVE PLAYER

No campaign-global `active_player`, universal turn queue or round-robin authority is introduced.

## LAW R2.5-2 — NATIVE ORDER OWNER WINS

Where a native execution/rules owner defines responder/order, R2.5 collaboration cannot override or duplicate it.

---

## 3. Agency dependency and maximal safe frontier

A human contribution is materially required when, under current fiction/rules/authority, its content can still change the correctness-relevant outcome of a dependent decision before that outcome is established.

Candidate dependency classes include:

- joint voluntary action;
- still-open intervention/reaction in negotiation or shared decision;
- contested use of a scarce/common resource;
- scene/chronology convergence where relative action could materially change outcome;
- serious consequence to another PC where that PC has an applicable voluntary choice/reaction;
- another explicit owner-defined human contribution dependency.

The dependency is semantic, not based on online presence, message age or transport order.

## LAW R2.5-3 — MAXIMAL SAFE FRONTIER

Before waiting for another participant, HDM SHALL establish every consequence that can be resolved without consuming the missing participant's still-open decision opportunity, then stop before the first dependent consequence.

## LAW R2.5-4 — TRANSPORT ORDER DOES NOT CONSUME AGENCY

Earlier chat/Git/request arrival SHALL NOT by itself resolve a fictionally material competition or erase another player's still-valid opportunity.

## LAW R2.5-5 — WAITING IS SCOPE-LOCAL

An unresolved agency dependency blocks only the bounded dependent collaboration/native scope. Independent scenes/processes may continue under their own owners.

## LAW R2.5-6 — ABSENCE IS NOT CONSENT

Offline/idle/silent status never supplies voluntary PC speech, action, belief, agreement, pass or consent.

## LAW R2.5-7 — ABSENCE IS NOT IMMUNITY

If a consequence is automatic under current owners and the absent PC has no applicable player decision/reaction opportunity, multiplayer absence does not block that consequence merely to protect the PC.

## LAW R2.5-8 — EXTERNAL COORDINATION IS A HINT

Player reports of agreements made through external channels may guide collaboration discovery but do not authorize another player's controlled PC action.

---

## 4. Scoped collective collaboration

A durable/recoverable collective scope/window exists only when an unresolved human contribution obligation must survive across participant turns/host gaps and no native ordered owner already owns it.

Conceptual semantic state:

```text
collaboration identity / generation
bounded scope ref
current source/currentness basis
required contributor PLAYER/PC refs
optional contributor refs
accepted contribution Interaction/input refs
safe-frontier/ref where applicable
state = OPEN | CLOSED | RESOLVED | OBSOLETE
obsolete/supersession reason where applicable
```

Exact machine shape is deferred.

## LAW R2.5-9 — COORDINATION ONLY

Collaboration state owns contribution collection and waiting semantics only. It does not own world truth, PC intent meaning, mechanics, chronology, knowledge/disclosure, live ownership or player binding.

## LAW R2.5-10 — MINIMAL REQUIRED SET

Only contributors whose human input can materially change the dependent outcome may be required. Party/campaign membership alone never makes a participant required.

## LAW R2.5-11 — OPTIONAL CONTRIBUTORS DO NOT BLOCK

Optional participants may contribute when eligible but cannot prevent closure solely by remaining silent.

## LAW R2.5-12 — EXPLICIT NON-ACTION MAY SATISFY A HUMAN CONTRIBUTION

A required participant may explicitly provide a typed `PASS`, `READY`, `NO_FURTHER_INPUT` or equivalent non-action contribution when semantically valid. This does not fabricate a PC action.

## LAW R2.5-13 — NO TIMEOUT/PRESENCE CORRECTNESS AUTHORITY

Wall-clock debounce, typing indicators, online presence, reconnect state or message-age heuristic cannot close a correctness-critical contribution obligation in the baseline architecture.

## LAW R2.5-14 — CONTRIBUTIONS REFERENCE ACCEPTED INPUT OWNERS

The collaboration artifact references accepted Interaction/input identities; it is not a duplicate transcript/message store.

## LAW R2.5-15 — OBSOLETE WINDOW DOES NOT FORCE RESOLUTION

If the underlying scope is lawfully superseded/invalidated before collective resolution, the collaboration obligation becomes obsolete. Obsolescence does not synthesize missing contributions or force the previously prepared result.

---

## 5. Human input semantic classes

One human message may yield multiple typed contributions:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

## LAW R2.5-16 — NO SILENT INPUT-CLASS PROMOTION

OOC coordination does not become PC speech/action; diegetic communication does not become unrelated action; control signals do not mutate fiction merely because they share one message.

---

## 6. Join/rejoin and catch-up

Before accepting mutable gameplay input after join/rejoin:

```text
authenticate/bind PLAYER
-> resolve controlled PC
-> acquire current campaign/live routing basis
-> acquire native procedure/collaboration admission
-> assemble recipient/PC-eligible R2.3 context
-> assemble bounded catch-up
-> expose unresolved own contribution obligations
-> accept mutable gameplay input
```

## LAW R2.5-17 — FRONTIER ACQUISITION BEFORE MUTATION

A joining/rejoining participant cannot mutate gameplay until authenticated binding, current routing and applicable mode/obligation admission are resolved.

## LAW R2.5-18 — CATCH-UP IS A PROJECTION

Catch-up derives from current owners, eligible continuity/history and unresolved collaboration/native obligations. It is not truth authority, a transcript replacement or an exact read receipt.

## LAW R2.5-19 — FRONTIER HINT DOES NOT PROVE HUMAN CONSUMPTION

Session/collaboration cursor hints may reduce retrieval cost but cannot prove what the human actually read.

---

## 7. Two-level Dramaturg coordination

### 7.1 Player-local Dramaturg horizon

A player-local horizon is retained bounded noncanonical preparation for one player's near horizon.

Candidate semantic content may include:

```text
relevant pressures/problems
involved actors/goals
possible/likely reactions under conditions
possible manifestations
clue/evidence opportunities
local opportunities/constraints
near-horizon developments if unopposed
local pacing/tone emphasis
possible convergence refs
assumptions
invalidation/expiry cues
source basis
shared-planning basis/generation hint where applicable
```

### 7.2 Shared Dramaturg horizon

When multiplayer is enabled, one shared noncanonical planning projection coordinates independent Dramaturg phases across participant lines.

Candidate semantic content may include relevant:

```text
campaign premise/tone/boundary refs
shared pressures/problems
important common/cross-player threads
material developments from one player line that may affect another
campaign-level faction/antagonist directions
possible convergence points
mystery/revelation constraints
common assumptions/invalidation cues
source/currentness basis
planning generation/basis
```

The exact physical representation is deferred.

## LAW R2.5-20 — SHARED HORIZON IS MULTIPLAYER-ONLY

Singleplayer does not create the shared upper planning level merely for symmetry.

## LAW R2.5-21 — BOTH HORIZONS ARE NONCANONICAL

Neither local nor shared Dramaturg horizon owns world truth, current state, chronology, knowledge, disclosure or mechanics.

## LAW R2.5-22 — SOURCE-ANCHORED CONSTRAINT VS PROVISIONAL DIRECTION

A planning artifact SHALL distinguish material that merely references an accepted source constraint from provisional planning direction.

A source-anchored entry derives authority only from its referenced owner. A provisional entry has no factual authority.

## LAW R2.5-23 — PREPARATION HAS NO ENTITLEMENT TO OCCUR

No prepared scene, event, reveal, NPC action, convergence, twist or payoff becomes established merely because it exists in either horizon.

## LAW R2.5-24 — CANON INVALIDATES PREPARATION

Any accepted player decision, Actor decision, mechanic, causal development or native owner transition may invalidate local/shared preparation.

Preparation must adapt to accepted canon, never the reverse.

## LAW R2.5-25 — NO PLOT RESTORATION

HDM SHALL NOT manufacture replacement twists, duplicate actors/items, coincidences, forced redirection or equivalent compensating events solely to restore an invalidated prepared trajectory.

## LAW R2.5-26 — SHARED COHERENCE CONSTRAINS PREPARATION, NOT AGENCY

Applicable shared planning constraints may cause local preparation to be revised/discarded so independent Masters remain part of one campaign. They cannot restrict a lawful player choice or Actor decision merely to preserve planned coherence.

## LAW R2.5-27 — LOCAL INDEPENDENCE IS ALLOWED

Different player-local horizons may pursue substantially different scene focus, tone emphasis, pressures and possible developments while remaining compatible with one canon and applicable shared planning basis.

---

## 8. Lazy planning discovery and revalidation

R2.3 Context Runtime applies directly to planning artifacts.

Conceptual flow:

```text
compact planning discovery/basis metadata
    -> determine whether shared/local planning is material to current Dramaturg task
    -> load only required planning slices + source owners
    -> revalidate against current canon/currentness
    -> use as noncanonical preparation context
```

## LAW R2.5-28 — NO MANDATORY FULL PLANNING PRELOAD

A Dramaturg phase does not load all local/shared preparation merely because the artifacts exist in the common repository.

## LAW R2.5-29 — CURRENT OWNERS OUTRANK PLANNING GENERATION

Before material reliance, any source-anchored planning constraint must be checked against current routed owners as required. A planning generation does not prove current factual truth.

## LAW R2.5-30 — RELEVANT REBASE ONLY

A player-local horizon need only be revalidated/rebased when newer canon/shared planning changes are material to its current task. Unrelated changes do not force global rewrite.

## LAW R2.5-31 — NO BACKGROUND GLOBAL PREP REWRITE

Correctness does not require a worker/scheduler that updates every player's preparation whenever any other participant advances.

## LAW R2.5-32 — PLANNING CANNOT SELF-PROMOTE

Repeated presence, restatement or inheritance of a provisional preparation claim across horizons/generations never promotes it to canon.

---

## 9. Split-party and cross-scope composition

Independent scenes retain independent current/context/chronology frontiers.

Cross-scope responsibilities remain separated:

```text
LIVE/currentness
    current mutable factual ownership

CHRONOLOGY
    causal/temporal bridge

COLLABORATION
    still-open human agency bridge

DRAMATURG HORIZONS
    noncanonical preparation coherence bridge
```

## LAW R2.5-33 — NO PERMANENT COMMON PLAYER CONTEXT

Membership in one campaign does not create one permanently shared secret-bearing context or planning preload across participants.

## LAW R2.5-34 — MATERIAL BRIDGE ONLY

Cross-scene synchronization/context expansion occurs only when a concrete factual, causal, ownership/resource, knowledge/disclosure, agency or planning dependency makes it relevant.

## LAW R2.5-35 — FACTUAL BRIDGE BEFORE PLANNING USE

A Dramaturg planning relationship between scenes cannot substitute for required live/currentness/chronology reconciliation when the actual current fact/order is material.

---

## 10. TurnEnvelope composition

Each participant request remains one R2.4 TurnEnvelope.

Collaboration state may affect whether the envelope:

- resolves immediately;
- advances only to a maximal safe frontier;
- records/updates a bounded contribution;
- returns a waiting/OOC coordination result;
- performs join/rejoin catch-up;
- activates a Dramaturg phase with local/shared planning slices;
- uses native ordered execution.

## LAW R2.5-36 — NO CROSS-CHAT MODEL MERGE

Multiplayer coordination occurs through durable/current owners and typed products; independent human chats are not merged into one physical LLM context.

## LAW R2.5-37 — NARRATION RESPECTS CURRENT PARTICIPANT SCOPE

Each Narrator output remains recipient/PC scoped under Step 4/5.12 and cannot expose other players' private planning/knowledge merely because shared collaboration/planning exists.

---

## 11. Failure / stale / conflict behavior

### Stale collaboration basis

If the underlying current/live/chronology basis moved materially, refresh/revalidate before resolving the dependent collective result.

### Stale planning

If a planning horizon conflicts with current owner state, discard/rebase the affected preparation. Do not repair canon to match planning.

### Ambiguous agency dependency

If the system cannot establish that the missing participant's contribution is irrelevant to a serious irreversible dependent outcome, it may stop at the last proven safe frontier and expose a bounded waiting reason rather than guessing.

This conservative rule applies only where a concrete material dependency is plausible; uncertainty must not become a reason to globally freeze routine unrelated play.

## LAW R2.5-38 — STALE PREP FAILS SOFT

Stale/invalid preparation degrades planning quality only; it cannot invalidate already accepted canon solely because preparation was wrong.

## LAW R2.5-39 — NO UNBOUNDED WAIT/FANOUT

Required contributor discovery and dependency expansion must remain bounded to the smallest current scope. Do not recursively enroll every potentially interested player/entity.

---

## 12. Diamond / Strong disposition

### Active/adopted

- **D21** — adopted narrowly as scoped persistent collaboration semantics.
- **D22** — inherited independent frontiers plus R2.5 agency/planning bridge delta.
- **D23** — adopted as three mode/scope coordination families; no universal active player.
- **S43** — adopted typed human input classes.
- **S44** — adopted recipient-scoped bounded catch-up.
- **S45** — adopted join/rejoin frontier/admission/context acquisition before mutation.
- **S54** — adopted/refined as agency-dependent bounded collection, not generic timer batching.
- **S14** — activated narrowly for player-local + multiplayer-shared noncanonical planning horizons.

### Inherited/preserved

- **D20, D24, S41, S42, S46, S47, S50, S51, S52, S57** remain inherited constraints and are not reopened.

### Still dormant

No other dormant Narrative Dynamics candidate is activated merely because S14 fired. In particular this candidate does not create a world-pressure ladder, authored arc state machine, generic planning graph, AI-PC controller framework or spectator system.

---

## 13. Adversarial review requirements

The next review SHALL challenge at least:

1. false-positive waiting that unnecessarily blocks play;
2. false-negative waiting that steals another player's agency;
3. transport/Git order incorrectly becoming fictional priority;
4. absent-PC immunity exploit;
5. external coordination impersonation;
6. required-set explosion / party-wide blocking;
7. collective window stale currentness;
8. overlapping collaboration scopes/generations;
9. shared horizon turning into plot authority;
10. local horizon contradicting current canon;
11. source-anchored planning claim going stale;
12. provisional planning self-promoting through repetition;
13. cross-chat genre/ontology drift despite factual consistency;
14. global planning preload defeating lazy loading;
15. shared-horizon secret leakage into recipient Narrator;
16. planning dependency incorrectly substituting for chronology/live bridge;
17. join/rejoin race with open collective/native ordered scope;
18. stale catch-up omitting current obligation;
19. no-plot-restoration violation after players destroy prepared trajectory;
20. split-party independent progress accidentally serialized globally.

Broad implementation remains blocked.