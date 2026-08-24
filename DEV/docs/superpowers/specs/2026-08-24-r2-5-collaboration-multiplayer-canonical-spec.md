# R2.5 Canonical Specification — Agency-Safe Multiplayer Collaboration and Two-Level Dramaturg Coordination

Status: **CANONICAL — R2.5 ARCHITECTURE CLOSED SUBJECT TO RESOLUTION GATE**

Date: 2026-08-24

Canonicalization basis:

- R2.5 task brief;
- R2.5 collaboration/multiplayer evidence ledger;
- R2.5 agency/dramaturg coordination evidence addendum;
- Decision Brief v2;
- owner-approved B3 decision;
- R2.5 candidate specification;
- adversarial review AR-1..AR-14.

Owner-approved architecture:

> **AGENCY-SAFE SCOPED COLLABORATION + TWO-LEVEL DRAMATURG COORDINATION**

This specification defines multiplayer collaboration/input/planning semantics. It does not implement schemas/runtime code, choose physical storage paths, define UI widgets, select timeout values or alter existing Step-5 live/currentness/chronology owners.

---

# 1. Central invariant

Multiplayer HDM consists of multiple independent participant ChatGPT TurnEnvelopes operating over one campaign repository and one canonical world/history.

R2.5 adds two narrow semantic responsibilities only:

```text
COLLABORATION
    preserve still-open human agency across asynchronous participant timing
    and collect bounded joint human contributions when needed

DRAMATURG COORDINATION
    preserve compatible noncanonical preparation across independent Masters
```

Existing owners remain authoritative for current world/live truth, mechanics, chronology, knowledge/disclosure, participant binding and persistence.

## LAW R2.5-1 — NO SECOND GAMEPLAY AUTHORITY

Collaboration and Dramaturg coordination SHALL NOT become alternate owners of world truth, current state, mechanics, chronology, knowledge, disclosure, PC control or persistence authority.

---

# 2. Coordination families

Canonical coordination families are:

```text
INDEPENDENT_IMMEDIATE
AGENCY_DEPENDENT_COLLECTIVE
RULE_OWNED_ORDERED
```

- `INDEPENDENT_IMMEDIATE` — current participant input may resolve now because no other human contribution remains materially relevant to the dependent consequence.
- `AGENCY_DEPENDENT_COLLECTIVE` — one or more human contributions remain materially capable of changing the dependent result, so the scope advances only to its maximal safe frontier and waits/collects there.
- `RULE_OWNED_ORDERED` — Procedure/Continuation/Reaction/Choice/equivalent native owner already controls responder/order semantics.

## LAW R2.5-2 — NO GLOBAL ACTIVE PLAYER

HDM SHALL NOT introduce one campaign-global `active_player`, universal round-robin queue or global turn gate for ordinary multiplayer collaboration.

## LAW R2.5-3 — NATIVE ORDER OWNER WINS

Where a native rules/execution owner defines admissible responder/order semantics, generic collaboration SHALL NOT duplicate or override that owner.

---

# 3. Agency dependency

A missing human contribution may block a dependent consequence only when a **positive bounded material dependency** is identified through an admitted dependency class and current evidence.

Material dependency means the missing contribution can still change the correctness-relevant dependent outcome under current fiction/rules/authority.

Typical admitted classes include:

- joint voluntary action;
- still-open intervention/reaction in a shared decision or negotiation;
- contested/shared scarce-resource choice;
- scene/chronology convergence where relative action can change outcome;
- serious consequence to another PC where an applicable voluntary choice/reaction remains open;
- another explicit owner-defined human contribution dependency.

Hypothetical interest alone is insufficient.

## LAW R2.5-4 — POSITIVE DEPENDENCY REQUIRED

Failure to prove universal independence SHALL NOT make another player required. A concrete bounded dependency candidate must first be identified.

## LAW R2.5-5 — CURRENTNESS BEFORE REQUIRED ENROLLMENT

Before enrolling a required contributor for a material dependency, HDM SHALL verify the smallest applicable currentness/ownership/chronology basis needed to establish that the decision opportunity actually exists.

Planning hints may discover a possibility but cannot establish it.

## LAW R2.5-6 — TRANSPORT ORDER DOES NOT CONSUME AGENCY

Earlier chat request, host response, Git commit or tool arrival order SHALL NOT by itself erase another player's still-valid voluntary opportunity or choose the fictional winner of a materially contested/simultaneous outcome.

---

# 4. Maximal safe frontier

The maximal safe frontier is the latest semantic/visible boundary that can be established without consuming a missing participant's still-open decision opportunity.

Conceptually:

```text
accepted input A
    -> resolve every consequence independent of missing contribution B
    -> establish/narrate only that safe prefix
    -> stop before first dependent consequence
    -> collect B if still required
```

## LAW R2.5-7 — MAXIMAL SAFE FRONTIER

HDM SHALL progress as far as safely possible before waiting. It SHALL NOT globally freeze earlier than needed merely because a later dependent consequence exists.

## LAW R2.5-8 — VISIBLE CONSEQUENCE SHARES THE SAME FRONTIER

Narrator SHALL NOT expose a dependent unresolved outcome as if it occurred. Player-visible established consequence cannot cross beyond the same safe frontier that constrains semantic mutation.

Recipient-safe OOC waiting/status explanation is allowed.

## LAW R2.5-9 — WAITING IS SCOPE-LOCAL

An unresolved agency dependency blocks only the bounded dependent collaboration/native scope. Independent scenes/processes may continue under their owners.

## LAW R2.5-10 — ABSENCE IS NOT CONSENT

Offline, idle, silent, disconnected or delayed status never supplies voluntary PC speech, action, belief, agreement, pass or consent.

## LAW R2.5-11 — ABSENCE IS NOT IMMUNITY

If a consequence is automatic under current owners and the absent PC has no applicable voluntary decision/reaction opportunity, absence does not block that consequence solely to protect the PC.

## LAW R2.5-12 — EXTERNAL COORDINATION IS A HINT, NOT PC AUTHORITY

Players may coordinate through any external channel. One player's report of another player's intended action may assist discovery but cannot authorize the other controlled PC.

---

# 5. Scoped collaboration obligation

A durable/recoverable collaboration obligation exists only when unresolved human contribution state must survive participant/chat gaps and no native ordered owner already owns that obligation.

Conceptually it may bind:

```text
stable collaboration identity / generation
bounded scope ref
current source/currentness basis
required contributor PLAYER/PC refs
optional contributor refs
accepted contribution refs
safe-frontier/ref where applicable
state = OPEN | CLOSED | RESOLVED | OBSOLETE
supersession/obsolete reason where applicable
```

Exact machine representation is R2.7/implementation work.

## LAW R2.5-13 — COLLABORATION OWNS COLLECTION ONLY

The collaboration obligation owns contribution collection/waiting/current-generation semantics only. It does not own the gameplay meaning or consequence of those contributions.

## LAW R2.5-14 — MINIMAL REQUIRED SET

Only human contributors whose input can materially change the dependent outcome may be required. Party/campaign membership alone never enrolls a participant.

## LAW R2.5-15 — OPTIONAL CONTRIBUTORS DO NOT BLOCK

Optional eligible contributors may contribute but cannot prevent closure solely through silence.

## LAW R2.5-16 — EXPLICIT NON-ACTION CAN SATISFY AN OBLIGATION

A required participant may explicitly supply a typed `PASS`, `READY`, `NO_FURTHER_INPUT` or equivalent non-action result where semantically valid. This does not synthesize a PC action.

## LAW R2.5-17 — NO TIMEOUT/PRESENCE CORRECTNESS AUTHORITY

Wall-clock debounce, typing indicators, online presence, reconnect state or message age cannot close a correctness-critical contribution obligation in the baseline architecture.

## LAW R2.5-18 — CONTRIBUTIONS REFERENCE ACCEPTED INPUT OWNERS

Collaboration state references accepted Interaction/input identities rather than copying transcript prose or becoming a second message store.

## LAW R2.5-19 — CONTRIBUTION USE IS PURPOSE/SCOPE/GENERATION BOUND

A contribution admitted to one obligation SHALL bind to its typed purpose/scope/generation. It SHALL NOT silently satisfy another obligation unless deterministic interpretation explicitly establishes compatible reuse.

## LAW R2.5-20 — GENERATION CURRENTNESS IS EXPLICIT

A reply aimed at an obsolete/superseded collaboration generation cannot mutate its successor merely because the wording appears relevant. Current obligation acquisition and normal interpretation/reconfirmation apply.

## LAW R2.5-21 — OBSOLESCENCE DOES NOT FORCE RESOLUTION

If the underlying scope is lawfully superseded/invalidated before resolution, the collaboration obligation may become `OBSOLETE`. Obsolescence neither invents missing contributions nor forces the previously anticipated result.

---

# 6. Human input semantic classes

One human message may produce multiple typed semantic contributions:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

## LAW R2.5-22 — NO SILENT INPUT-CLASS PROMOTION

OOC coordination does not silently become PC speech/action; diegetic communication does not silently become unrelated mechanical intent; control signals do not mutate fiction merely because they occur in the same host message.

---

# 7. Join/rejoin and recipient catch-up

Before mutable gameplay input after join/rejoin:

```text
authenticate/bind PLAYER
-> resolve controlled PC
-> acquire current campaign/live routing basis
-> acquire native procedure/collaboration admission
-> assemble recipient/PC-eligible R2.3 context
-> assemble bounded catch-up
-> expose unresolved own obligations
-> accept mutable gameplay input
```

## LAW R2.5-23 — CURRENT FRONTIER BEFORE MUTATION

A joining/rejoining participant cannot mutate gameplay until authenticated binding, current routing and applicable mode/obligation admission are resolved.

## LAW R2.5-24 — CATCH-UP IS RECIPIENT PROJECTION

Catch-up is derived from current owners, eligible continuity/history and unresolved own collaboration/native obligations. It is not truth authority, a second transcript or an exact read receipt.

## LAW R2.5-25 — FRONTIER HINT DOES NOT PROVE HUMAN CONSUMPTION

Session/collaboration cursor hints may reduce retrieval work but do not prove what the human actually read.

## LAW R2.5-26 — PLANNING IS NOT PLAYER CATCH-UP EVIDENCE

Dramaturg horizons SHALL NOT enter player-facing catch-up merely because they exist or were loaded by a GM role. Their factual references reach the player only through independently eligible canonical/Story/disclosure sources.

---

# 8. Two-level Dramaturg coordination

R2.5 activates retained noncanonical planning narrowly for the proven multiplayer consumer.

## 8.1 Player-local Dramaturg horizon

Each participant line may retain bounded near-horizon preparation relevant to that player/chat trajectory.

It may include relevant:

- pressures/problems;
- involved actors/goals;
- likely/possible reactions under conditions;
- possible manifestations;
- clue/evidence opportunities;
- local opportunities/constraints;
- near-horizon developments if unopposed;
- local pacing/tone emphasis;
- possible convergence refs;
- assumptions and invalidation/expiry cues;
- source basis;
- shared-planning basis/generation hint where applicable.

## 8.2 Shared Dramaturg horizon

When multiplayer is enabled, HDM admits one shared noncanonical planning projection coordinating independent Dramaturg phases across player lines.

It may include relevant:

- campaign premise/tone/boundary refs;
- shared pressures/problems;
- important common/cross-player threads;
- material developments from one player line that may affect another;
- campaign-level faction/antagonist directions;
- possible convergence points;
- mystery/revelation constraints;
- common assumptions/invalidation cues;
- source/currentness basis;
- planning generation/basis.

## LAW R2.5-27 — SHARED HORIZON IS MULTIPLAYER-ONLY ACTIVE STATE

Singleplayer does not require the shared upper planning level. When multiplayer is disabled, retained shared planning is inactive and not a singleplayer correctness dependency.

If multiplayer is later re-enabled, retained shared planning must be revalidated against current canon/currentness before reuse; discarding/rebuilding it is legal.

## LAW R2.5-28 — BOTH HORIZONS ARE NONCANONICAL

Neither player-local nor shared Dramaturg horizon owns factual/current/mechanical/chronological/epistemic/disclosure truth.

## LAW R2.5-29 — SOURCE-ANCHORED CONSTRAINT VS PROVISIONAL DIRECTION

Planning material SHALL distinguish:

```text
SOURCE_ANCHORED_CONSTRAINT
    authority comes only from referenced accepted owner

PROVISIONAL_DRAMATURGIC_DIRECTION
    coordination/preparation possibility only
```

A planning projection never creates authority merely by restating a source.

---

# 9. Story is discovered in play, not written in advance

## LAW R2.5-30 — PREPARATION HAS NO ENTITLEMENT TO OCCUR

No prepared scene, event, reveal, NPC action, convergence, twist, payoff or future direction becomes established merely because it exists in either Dramaturg horizon.

## LAW R2.5-31 — CANON INVALIDATES PREPARATION

Any accepted player decision, Actor decision, mechanic, causal development or native owner transition may invalidate local/shared preparation.

Preparation SHALL adapt to accepted canon, never the reverse.

## LAW R2.5-32 — NO PLOT RESTORATION

HDM SHALL NOT manufacture replacement twists, duplicate actors/items, coincidences, forced redirection or equivalent compensating events solely to restore an invalidated prepared trajectory.

## LAW R2.5-33 — SHARED COHERENCE CONSTRAINS PREPARATION, NOT AGENCY

Applicable common planning coordination may require local preparation revision so independent Masters remain part of one campaign. It SHALL NOT restrict a lawful player choice or Actor decision merely to preserve planned coherence.

## LAW R2.5-34 — SHARED PROVISIONAL DIRECTION IS REVISABLE

Shared provisional direction is a coordination baseline, not an immutable constraint. A local Dramaturg may explore an explicitly local/provisional incompatible alternative and may propose revision of shared planning.

Until common planning is revised, that local alternative SHALL NOT be silently treated as the shared campaign direction.

## LAW R2.5-35 — LOCAL INDEPENDENCE IS ALLOWED

Different player-local horizons may develop substantially different scene focus, tone emphasis, pressures and near-term possibilities while remaining compatible with one canon and applicable shared planning basis.

---

# 10. Lazy planning discovery and currentness

R2.3 Context Runtime applies to planning artifacts.

Conceptual flow:

```text
compact planning discovery/basis metadata
    -> material relevance decision
    -> load only required shared/local planning slices + referenced owners
    -> verify current source constraints
    -> use as noncanonical Dramaturg context
```

## LAW R2.5-36 — NO FULL PLANNING PRELOAD REQUIREMENT

A Dramaturg phase does not load all local/shared planning merely because the artifacts exist in the common campaign repository.

## LAW R2.5-37 — CURRENT OWNERS OUTRANK PLANNING GENERATION

Planning generation/basis indicates projection currentness only. Material factual reliance must follow current routed owners as required.

## LAW R2.5-38 — RELEVANT REBASE ONLY

A local horizon need only be revalidated/rebased when newer canon/shared planning changes materially affect the current Dramaturg task. Unrelated changes do not force global rewrite.

## LAW R2.5-39 — NO BACKGROUND GLOBAL PREPARATION REWRITE

Correctness does not require a worker/scheduler that rewrites every player's planning after every other participant action.

## LAW R2.5-40 — PLANNING CANNOT SELF-PROMOTE

Repeated presence, restatement, copying or inheritance of a provisional planning claim across horizons/generations never promotes it to fact/canon.

## LAW R2.5-41 — SHARED HORIZON CURRENT GENERATION IS FENCED

Concurrent shared-horizon updates SHALL use current-generation/exact-base fencing under the existing publication/currentness discipline or equivalent semantic CAS.

On conflict, revalidate/rebase. Blind last-writer-wins or blind textual merge is nonconforming.

Compatible independent planning deltas may coexist; incompatible provisional directions remain planning alternatives/revision candidates until a coherent current planning basis is selected.

---

# 11. Planning lifecycle and recovery

## LAW R2.5-42 — PLANNING LOSS IS QUALITY LOSS, NOT CANON LOSS

Loss/corruption/staleness of local/shared Dramaturg preparation may require bounded repreparation and may degrade planning quality. It cannot erase, rewrite or invalidate accepted gameplay canon solely because planning was lost.

## LAW R2.5-43 — STORY AND DRAMATURG HORIZONS HAVE DIFFERENT LIFECYCLES

Story is retrospective/history/presentation projection under Chronicler/Step-5.10. Dramaturg horizons are prospective conditional preparation.

Story may orient Dramaturg when eligible, but Story coverage does not prove planning currency and planning generations do not advance Story coverage.

---

# 12. Split-party and cross-scope composition

Independent scenes retain independent current/context/chronology frontiers.

Canonical responsibility separation:

```text
LIVE/current owners
    factual mutable-scene consistency

CHRONOLOGY
    causal/order consistency across independent scopes

COLLABORATION
    still-open human agency / bounded joint input

DRAMATURG HORIZONS
    noncanonical preparation coherence
```

## LAW R2.5-44 — NO PERMANENT COMMON SECRET-BEARING CONTEXT

Campaign membership does not create one permanently shared player/role context. Recipient and role eligibility remain R2.3/Step-4 scoped.

## LAW R2.5-45 — MATERIAL BRIDGE ONLY

Cross-scene synchronization/context expansion occurs only when a concrete factual, causal, ownership/resource, knowledge/disclosure, agency or planning dependency makes it relevant.

## LAW R2.5-46 — PLANNING RELATION DOES NOT CREATE CAUSAL FACT

A possible convergence/planning relationship may activate discovery/preparation only. Any material factual/causal/temporal/ownership/agency bridge must be established through native currentness/chronology/collaboration evidence before resolution.

## LAW R2.5-47 — NO GLOBAL PLANNING CONSISTENCY SCAN

Campaign-wide coherence SHALL NOT require per-turn loading/scanning of every player-local horizon and all campaign state. Bounded source constraints, shared planning basis metadata and material dependency discovery are sufficient architecture.

A later-discovered contradiction in provisional preparation is repaired by revising/discarding preparation, not by rewriting valid canon.

---

# 13. TurnEnvelope and visible-output composition

Each participant request remains one R2.4 TurnEnvelope.

R2.5 state may cause the envelope to:

- resolve immediately;
- advance only to maximal safe frontier;
- record/update a contribution;
- return recipient-safe waiting/OOC coordination output;
- perform join/rejoin catch-up;
- activate Dramaturg with bounded local/shared planning slices;
- enter native ordered execution.

## LAW R2.5-48 — NO CROSS-CHAT MODEL MERGE

Independent human chats are not merged into one physical LLM context. Coordination occurs through shared durable/current owners and typed products.

## LAW R2.5-49 — NARRATOR/RECIPIENT ELIGIBILITY SURVIVES PLANNING CO-PRESENCE

Dramaturg planning loaded earlier in a physical context does not become Narrator/catch-up evidence. R2.4 fresh role rebinding and Step-4/R2.3 recipient eligibility remain mandatory.

---

# 14. Failure / conflict behavior

- If collaboration basis moves materially, refresh/revalidate before dependent resolution.
- If a collaboration generation is obsolete, stale input does not silently bind to its successor.
- If planning conflicts with current owner state, discard/rebase planning; do not repair canon to match it.
- If shared planning publication conflicts, semantic rebase occurs under current generation; gameplay need not roll back.
- If a concrete agency dependency exists but safe continuation cannot yet be determined, stop at the last proven safe frontier rather than guessing the dependent result.
- Uncertainty without a concrete material dependency is not permission for global waiting.

## LAW R2.5-50 — STALE PREPARATION FAILS SOFT

Invalid planning degrades preparation only. It cannot invalidate already accepted canon solely because preparation was wrong.

## LAW R2.5-51 — NO UNBOUNDED REQUIRED-SET FANOUT

Dependency discovery and required-contributor enrollment remain bounded to the smallest current scope. Do not recursively enroll every potentially interested campaign participant.

---

# 15. Diamond / Strong disposition

## Adopted / active

- **D21** — adopted narrowly as scoped persistent async collaboration semantics.
- **D22** — independent scene/context/chronology frontiers inherited; agency/planning bridge delta added.
- **D23** — adopted as `INDEPENDENT_IMMEDIATE`, `AGENCY_DEPENDENT_COLLECTIVE`, `RULE_OWNED_ORDERED`; universal active-player rejected.
- **S43** — adopted typed OOC/diegetic/action/control separation.
- **S44** — adopted bounded recipient-scoped catch-up.
- **S45** — adopted join/rejoin current-frontier/admission/context acquisition before mutation.
- **S54** — adopted/refined as material agency-dependent collective input, not timeout/debounce batching authority.
- **S14** — **activated narrowly** for retained player-local + multiplayer-shared noncanonical Dramaturg horizons.

## Inherited / preserved

- **D20** observational finality;
- **D24** one canon + recipient-scoped projection;
- **S41** authenticated participant -> controlled actor;
- **S42** admin authority separate from PC agency;
- **S46** absence does not authorize takeover;
- **S47** presence/reconnect not authority;
- **S50** scoped live mutation serialization/CAS;
- **S51** cheap currentness synchronization;
- **S52** bounded collaboration hot state with durable deeper history elsewhere;
- **S57** invitation/discovery not gameplay authority.

## Still dormant

No other dormant Narrative Dynamics candidate is activated by R2.5. In particular no authored arc state machine, world-pressure ladder, generic planning graph, AI-PC controller framework, spectator/replay subsystem or campaign director is introduced.

---

# 16. R2.6 assurance handoff

R2.6 must test the approved host profile for at least:

1. false-positive agency waiting under ordinary independent split-party play;
2. false-negative waiting where async transport order would steal another player's valid decision;
3. maximal-safe-frontier narration fencing;
4. stale/superseded collaboration generation handling;
5. cross-player external-consent impersonation attempts;
6. shared-horizon concurrent update/rebase behavior under actual connector/host limits;
7. shared-horizon -> Narrator containment;
8. other-player local-horizon -> Narrator containment;
9. catch-up exclusion of planning-only information;
10. injection-like instructions embedded in planning text;
11. local/shared planning lazy-loading cost and relevance behavior;
12. anti-railroad/no-plot-restoration regression scenarios;
13. split-party coherence without global planning preload;
14. current ChatGPT Plus feasibility for the required multi-chat/repository synchronization envelope.

---

# 17. R2.7 machine-mapping handoff

R2.7 owns exact realization of:

- collaboration identity/generation/state representation;
- player-local/shared Dramaturg horizon physical roots and retention lifecycle;
- compact planning discovery/basis metadata;
- shared-horizon publication/CAS realization;
- schemas/index references/SQLite acceleration if justified;
- migrations/seeds/templates;
- instruction/runtime integration;
- regression/evaluation mapping.

Broad implementation remains blocked until Round-2 closure and implementation planning.