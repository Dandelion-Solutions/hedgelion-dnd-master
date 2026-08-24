# R2.5 Decision Brief — Multiplayer Collaboration and Free-Form Input Coordination

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Task brief:

- `2026-08-24-r2-5-collaboration-multiplayer-task-brief.md`

Evidence ledger:

- `../research/2026-08-24-r2-5-collaboration-multiplayer-evidence-ledger.md`

---

## 1. Exact decision

Most multiplayer authority/concurrency semantics are already closed by Step 4/5 and R2.3/R2.4.

The remaining material product question is:

> **Should HDM support a narrow durable free-form collaboration window that can collect several human contributions across participant turns/host gaps before one shared resolution, or should all free-form player input resolve immediately unless an existing mechanical Procedure/Continuation explicitly requires waiting?**

This decision does not choose schema fields, filenames, timeout values, UI widgets or transport implementation.

---

## 2. Established facts

### F1 — Do not build another multiplayer authority layer

Step 5.8 already owns shared-scene current truth, mutation claims, exact-source CAS and live lifecycle.

### F2 — Do not build a global turn queue

Step 5.9 already permits independent scene/local chronology fronts. Strict rules-owned sequence already has Procedure/Continuation/Reaction/Choice owners.

### F3 — Absence does not grant PC control

Authenticated `PLAYER_`/controlled-PC binding is already authoritative. Silence/presence/host status cannot authorize AI/GM action for an absent PC.

### F4 — Transcript/session cannot be the collaboration authority

Step 5.4 explicitly makes session data coordination/frontier hints only. Host transcript is mutable presentation/context, not durable collaboration semantics.

### F5 — Catch-up must be recipient-scoped

R2.1/R2.3 + Step 4/5.12 already provide the source/eligibility model for bounded returning-participant orientation. Full transcript replay is neither needed nor desirable.

### F6 — Free-form and strict mechanical sequencing are semantically different

D23 is confirmed by current architecture: strict ordered mechanics already has an owner; free-form social/exploration collaboration does not.

---

## 3. Alternative A — Immediate Free-Form Only / No New Collaboration Owner

Every ordinary free-form player message is resolved independently as soon as possible against current shared/live state.

If a rules-owned Procedure/Continuation requires another participant, that native owner may wait. Otherwise the Master does not durably collect several players' intentions before resolving.

Conceptually:

```text
Player A input -> resolve/publish/narrate
Player B input -> resync -> resolve/publish/narrate
```

### Advantages

- minimum new persistence/coordination machinery;
- lowest latency;
- very clear authority;
- naturally fits asynchronous independent play.

### Costs

- weak support for genuinely collaborative free-form moments such as a group simultaneously declaring an approach before the world reacts;
- first message can advance shared fiction before later participants have contributed, making some natural table interactions artificially sequential;
- participants may compensate with OOC transcript discussion, recreating the transcript-as-coordinator failure D21 warns about;
- no durable way to say “collect these few human contributions, then resolve once” across chat/host gaps unless a mechanical Procedure happens to exist.

### Assessment

Viable minimalist baseline, but leaves D21/S54 materially under-served.

---

## 4. Alternative B — Scoped Mode-Owned Collaboration Window + Recipient Catch-Up — RECOMMENDED

Default free-form play remains immediate/independent.

HDM additionally admits one narrow coordination owner only when the current scope genuinely requires several human contributions before one shared resolution.

Conceptually:

```text
COLLABORATION SCOPE / GENERATION

mode = COLLECTIVE_WINDOW
scope = one scene / bounded interaction scope

required contributors     minimal set whose input is actually required
optional contributors     may contribute without blocking closure
accepted contribution refs
state = OPEN -> CLOSED -> RESOLVED/OBSOLETE
currentness/source basis needed for safe resolution
```

The window references accepted participant Interaction/input identities; it does not copy transcript prose or world state.

### 4.1 Three coordination families

```text
INDEPENDENT / IMMEDIATE
    ordinary default
    one participant input may resolve now

COLLECTIVE_WINDOW
    explicit bounded free-form collection
    several human contributions -> one shared resolution

RULE_OWNED_ORDERED
    Procedure / Continuation / Reaction / Choice / other native rules owner
    native owner alone defines responder/order
```

There is no campaign-global `active_player`.

### 4.2 Collection closure

Baseline closure is semantic, not presence/time based.

A collection closes when:

- every **required** contributor has supplied an accepted contribution or an explicit non-action control result such as `READY/PASS/NO_FURTHER_INPUT`; or
- the owning scope becomes obsolete/superseded before resolution under a valid native transition.

Optional contributors do not block closure.

No wall-clock debounce, online-presence detection or silence-as-consent is a correctness trigger in the current baseline.

The required set must be minimal. A window must not mark every player in the campaign as required merely because they are members of the party.

### 4.3 Agency

A missing contribution means exactly that: no contribution is supplied for that PC.

Window closure never fabricates absent-PC speech, action, belief or consent.

If the fiction/mechanics cannot resolve without a missing PC decision, that bounded scope waits. Independent scenes/scopes may continue normally.

### 4.4 Input classes

One incoming human message may be partitioned into typed semantic contributions:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

OOC planning/ready signals do not silently become PC speech/action.

### 4.5 Join/rejoin

Before mutable gameplay after join/rejoin:

```text
authenticate/bind PLAYER
-> resolve controlled PC
-> acquire current campaign/live routing frontier
-> acquire mode/window/native-procedure admission
-> assemble recipient/PC eligible catch-up/context
-> expose unresolved own obligations
-> accept gameplay mutation input
```

### 4.6 Catch-up

Catch-up is a bounded R2.1/R2.3 projection, not a new durable truth/history owner.

It includes as applicable:

- current actionable state;
- material eligible changes useful since a known basis;
- current collaboration/native-procedure obligation for the returning participant;
- selective exact evidence when exactness is protected/material.

Session/frontier hints may reduce retrieval cost but do not prove exact human consumption/read state. If the hint is missing/stale, over-include a bounded eligible orientation rather than omit correctness-critical context.

### 4.7 Split-party

Each collaboration window belongs to one bounded scene/interaction scope.

Participants in independent scenes do not wait on each other. Cross-scene effects use existing Step-5.9 material causal bridges/currentness before the receiving scope resolves.

### Advantages

- satisfies D21 async collaboration without transcript-as-coordinator;
- satisfies D23/S54 without a global turn model;
- preserves absent-PC agency;
- allows natural table-like “hear several people, then resolve” moments;
- durable only when a real open collaboration obligation survives host/participant gaps;
- composes with existing live/CAS/chronology owners rather than replacing them;
- no timeout/presence/background service required.

### Costs / risks

- introduces one new narrow coordination semantic owner when a collective window is active;
- incorrect required-participant selection could cause unnecessary waiting;
- overlapping windows need scope/generation rules to prevent ambiguity;
- implementation must carefully reference, not duplicate, accepted Interaction/input content;
- catch-up quality/size still needs R2.6/R2.7 testing/mapping.

### Assessment

Best fit. The new semantic state exists only where D21 proves host/transcript/session state is insufficient.

---

## 5. Alternative C — Campaign-Level Collaboration Queue / Persistent Turn Board

Create one persistent multiplayer coordination board for the campaign containing participant readiness, pending messages/intents, current turn/phase and return frontier.

### Advantages

- easy global overview;
- straightforward async task-board UX;
- simple answer to “who are we waiting for?”.

### Costs / risks

- recreates a campaign-global turn model that D23 rejects;
- conflicts with split-party independent scopes;
- risks duplicating Procedure/Continuation/live ownership;
- tends toward persistent presence/read-receipt semantics the host cannot prove;
- becomes a second scheduler/authority surface;
- every unrelated scene now competes through one coordination state.

### Assessment

Reject as over-centralized and semantically conflicting with accepted architecture.

---

## 6. Recommendation

Choose **Alternative B — Scoped Mode-Owned Collaboration Window + Recipient Catch-Up**.

Confidence: **HIGH**.

Reason:

> HDM already has the hard parts of multiplayer authority, currentness and chronology. The missing primitive is much narrower: occasionally several humans must contribute before one free-form shared resolution, and that obligation must survive asynchronous host gaps without becoming a global turn system or taking control of absent PCs.

B adds exactly that primitive and nothing broader.

---

## 7. Proposed R2.5 laws if B is approved

1. **NO SECOND GAMEPLAY AUTHORITY** — collaboration state owns collection coordination only, never world/live/mechanics/chronology/knowledge truth.
2. **MODE/SCOPE-OWNED COORDINATION** — no campaign-global `active_player`; coordination belongs to the smallest applicable scene/interaction/native-procedure scope.
3. **IMMEDIATE IS DEFAULT** — ordinary free-form input resolves independently unless a registered collective window or native ordered owner requires waiting.
4. **COLLECTIVE WINDOW IS EXPLICIT AND BOUNDED** — created only when several human contributions materially belong to one shared future resolution.
5. **NATIVE ORDER OWNER WINS** — Procedure/Continuation/Reaction/Choice semantics supersede generic collaboration sequencing for their obligations.
6. **MINIMAL REQUIRED SET** — only contributors whose input is semantically required block a collective window; campaign/party membership alone does not.
7. **NO SILENCE-AS-CONSENT** — no absent PC speech/action/choice is synthesized because the player is offline, idle or missing from a batch.
8. **NO PRESENCE/TIMEOUT AUTHORITY** — wall-clock debounce, typing/presence and reconnect signals do not close a correctness-critical collection in baseline.
9. **EXPLICIT NON-ACTION IS VALID** — required participant may satisfy contribution need through a typed `PASS/READY/NO_FURTHER_INPUT` control result without creating a PC action.
10. **INPUT SEMANTICS ARE TYPED** — OOC coordination, diegetic communication, actionable intent and control signals do not silently promote into one another.
11. **CONTRIBUTIONS REFERENCE ACCEPTED INPUT OWNERS** — collaboration state references accepted Interaction/input identities; it is not another transcript/message store.
12. **SCOPE-LOCAL ASYNC WAITING** — a waiting collective window blocks only the dependent bounded scope; independent scenes/processes may advance under their owners.
13. **JOIN/REJOIN ACQUIRES CURRENT FRONTIER BEFORE MUTATION** — player/PC binding, campaign/live route, mode admission and eligible context/catch-up precede mutable gameplay input.
14. **CATCH-UP IS RECIPIENT PROJECTION** — current state + eligible history/continuity + unresolved own obligations; never truth authority or full-transcript requirement.
15. **FRONTIER HINT IS NOT READ RECEIPT** — session/collaboration hints may optimize catch-up but do not prove exact human consumption.
16. **SPLIT PARTY REMAINS SPLIT** — collaboration/context does not merge independent scenes; only material causal bridges trigger reconciliation.
17. **OBSERVATIONAL FINALITY PRESERVED** — accepted/shared-established outcomes are not silently rewritten by host Retry/Edit or late batch text.
18. **NO BACKGROUND COORDINATION SERVICE REQUIRED** — correctness does not depend on heartbeat/push/polling.

---

## 8. Diamond / Strong decision summary

| Idea | Under B |
|---|---|
| **D21** | adopted narrowly as durable scoped collection semantics, not transcript/global coordinator |
| **D22** | collaboration delta only; existing independent scene/chronology frontiers preserved |
| **D23** | adopted as three coordination families; universal active-player rejected |
| **S43** | adopted typed OOC/diegetic/action/control separation |
| **S44** | adopted as bounded recipient-specific projection; full transcript rejected |
| **S45** | adopted as explicit current-frontier/mode/context acquisition before mutation |
| **S54** | adopted only as explicit bounded `COLLECTIVE_WINDOW`; timeout/debounce not baseline authority |

Inherited D20/D24/S41/S42/S46/S47/S50/S51/S52/S57 remain constraints and are not reopened.

---

## 9. Exact owner decision

Choose one:

- **A — Immediate Free-Form Only / No New Collaboration Owner**
- **B — Scoped Mode-Owned Collaboration Window + Recipient Catch-Up** **[recommended]**
- **C — Campaign-Level Collaboration Queue / Persistent Turn Board**

Approval of B approves the semantic direction/laws above. Exact schema representation, contribution/window IDs, persistence file location, UI and host-specific latency/catch-up limits remain R2.7/implementation or R2.6 assurance work.
