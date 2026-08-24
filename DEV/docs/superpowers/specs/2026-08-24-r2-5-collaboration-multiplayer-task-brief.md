# R2.5 — Collaboration & Multiplayer Interaction Semantics — Task Brief

Status: **TASK BRIEF / IN PROGRESS**

Date: 2026-08-24

Roadmap owner:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Depends on:

- R2.1 continuity/history canonical specification;
- R2.3 Context Runtime canonical specification;
- R2.4 TurnEnvelope/single-context execution canonical specification;
- Step-4 truth/knowledge/disclosure and recipient-scope architecture;
- Step-5.4 host lifecycle/session handoff;
- Step-5.8 multiplayer/live-epoch ownership;
- Step-5.9 chronology/reconciliation;
- Step-5.12 recipient-scoped emission/disclosure;
- current multiplayer/live/chronology runtime owners.

No implementation is authorized by this brief.

---

## 1. Problem statement

HDM already has strong multiplayer state/concurrency architecture:

- authenticated campaign player binding and controlled-PC authority;
- one shared campaign canon with recipient/subject-specific knowledge/disclosure;
- scene-centered live epochs for concurrently mutable shared scenes;
- exact-source CAS and forward absorption;
- independent scene/local chronology frontiers with material cross-scene reconciliation;
- session/handoff metadata that does not become gameplay authority;
- no automatic PC takeover merely because another host/session exists.

R2.5 therefore does **not** redesign shared-state persistence or concurrency.

The active gap is the collaboration/input layer above those owners:

> How does HDM coordinate synchronous and asynchronous human participation, accept/batch/resolve inputs under different interaction modes, preserve player agency during absence, give joining/returning participants a bounded recipient-specific catch-up/frontier, and compose all of this with R2.3 Context Runtime + R2.4 TurnEnvelope without creating a second gameplay authority or universal global turn lock?

---

## 2. Human decision boundary

The agent owns evidence extraction, source reconciliation, lifecycle/formal semantics, alternatives and recommendation.

Ask the owner only about genuine product semantics such as:

- whether free-form shared scenes should permit bounded multi-input collection before resolution;
- how/when play may continue while one participant is absent if several viable agency policies remain;
- whether explicit player readiness/coordination state should be durable when needed across asynchronous gaps;
- what user-visible collaboration modes are supported if they imply materially different agency/latency trade-offs.

Do not ask the owner to choose schema fields, filenames, status spelling, timeout numbers, Git call sequences or prompt syntax unless they encode a real product trade-off.

---

## 3. Current non-negotiable constraints

### C1 — Shared-state authority is already owned

Step 5.8 owns live/current mutable authority, claims, CAS fencing, close/absorption and shared-scene mutation publication.

R2.5 must not create a collaboration record that can override current scene/world/live owner state.

### C2 — Chronology is partial and bridge-driven

Step 5.9 / `CHRONOLOGY.md` permit independent local scene frontiers and reconcile only material causal/temporal bridges.

R2.5 must not introduce one campaign-global turn/clock merely for coordination convenience.

### C3 — Participant binding and PC control are authority boundaries

Current `MULTIPLAYER.md` binds authenticated users to stable campaign `PLAYER_` records and controlled PCs. Repository access/invitation/coordination metadata alone is not PC agency.

### C4 — Absence cannot silently transfer voluntary PC agency

Existing architecture/research rejects automatic AI/host takeover of an absent player-controlled PC. Any future delegated-control capability requires an explicit separate authority contract; it is not assumed by R2.5.

### C5 — Session metadata is non-authoritative

Step 5.4 permits session records for coordination/navigation/audit/frontier hints but not world truth, live authority, definitive recovery or write authorization.

R2.5 may add collaboration metadata only if its authority class is explicit and narrower than gameplay semantic owners.

### C6 — Context and visible output are recipient-scoped

R2.3 assembles role/subject/player-specific bundles; Step 4/5.12 separate objective truth, fictional knowledge and human disclosure.

No shared collaboration context blob may automatically expose all participants' private state.

### C7 — One human chat/session cannot rely on background polling

Current host profile has no correctness dependency on background workers/presence detection. Async readiness/rejoin must survive absence through durable/recomputable campaign semantics, not live websocket-style presence assumptions.

### C8 — R2.4 TurnEnvelope remains one-request/one-assistant-turn per participating chat

R2.5 composes several independent participant TurnEnvelopes against shared campaign/live owners. It does not merge all humans into one physical LLM context.

---

## 4. Task-specific Source Manifest

The following sources must be inspected to task depth before a Decision Brief or coverage claim:

| Source | Authority/use |
|---|---|
| current Round-2 roadmap | sequencing/status |
| R2.1 canonical | catch-up/continuity source semantics |
| R2.3 canonical | recipient/role Context Runtime, bounded discovery, packet assembly |
| R2.4 canonical | per-chat TurnEnvelope, role activation/output boundaries |
| Step-4 canonical + single-context amendment | knowledge/disclosure/recipient/role law |
| Step-5.4 host lifecycle/session handoff | session/frontier hints vs gameplay authority; recovery-safe host transitions |
| Step-5.8 multiplayer/live-epoch canonical | shared-scene mutable ownership/CAS/claims/live lifecycle |
| Step-5.9 chronology canonical + temporal amendment | independent frontiers, bridge reconciliation, no total clock |
| Step-5.12 emission/disclosure | recipient-scoped visible output and observational exposure |
| Step-5.14 integrated recovery/concurrency final | cross-owner recovery/concurrency closure |
| `GAME/CORE/MULTIPLAYER.md` | shipped membership/join/rejoin/sync/shared-scene behavior |
| `GAME/CORE/LIVE_SCENE.md` | current shared-scene hot path/observable event semantics |
| `GAME/CORE/CHRONOLOGY.md` | shipped partial-order/cross-scene semantics |
| relevant `PLAYER`, `SESSION`, `SCENE`, `LIVE_SCENE`, interaction/message/access schemas | current machine consumer/ownership evidence, not automatic design authority |
| D21, D22-delta, D23, S43, S44, S45, S54 | active research candidates |
| D20, D24, S41, S42, S46, S47, S50, S51, S52, S57 | inherited constraints to verify, not reopen absent insufficiency |
| relevant multiplayer/concurrency/recovery tests | existing behavior expectations |

---

## 5. Required design questions

### 5.1 Collaboration semantic owner

Determine whether HDM needs a durable coordination artifact at all and, if so, its narrow semantic responsibility.

Possible legitimate responsibilities include:

- unresolved participant contribution/request state;
- explicit readiness/collection boundary that must survive async gaps;
- last-consumed collaboration/catch-up frontier hint;
- mode-specific pending participant set.

It must not duplicate:

- current world/scene truth;
- Procedure/Continuation/Reaction owners;
- live mutation authority;
- chronology authority;
- PC knowledge/disclosure;
- authenticated player binding.

### 5.2 Mode-specific input coordination

Define the minimum admitted coordination modes needed by current product behavior, for example:

- free-form independent/asynchronous contribution;
- bounded shared-scene collection/batch before one world resolution;
- strict rules-owned ordered interaction (initiative/Reaction/Choice/Procedure), where the mechanical owner already defines who may respond.

Do not create a universal `active_player` gate.

### 5.3 Input semantic classes

Separate at least conceptually:

```text
OOC / social coordination
DIEGETIC SPEECH / communication
ACTIONABLE PC INTENT
CONTROL / READY / JOIN / REJOIN signal
```

One class must not silently promote into another because it appeared in the same chat message.

### 5.4 Async continuation and absence

Determine how play may progress when participants are absent without:

- choosing voluntary absent-PC actions;
- blocking every unrelated scope;
- fabricating permission from silence;
- conflating actor/world automatic consequences with player decisions.

Use existing Procedure/Continuation/temporal/world owners where they already decide what can progress independently.

### 5.5 Join/rejoin frontier acquisition

Define the semantic steps before a participant can safely act after join/rejoin:

- authenticate/bind participant;
- resolve controlled PC assignment;
- acquire current authoritative campaign/live routing frontier;
- apply current mode-specific admission;
- assemble recipient/PC-eligible context;
- establish bounded catch-up from durable evidence;
- expose unresolved own obligations/expected input.

Do not make joining alone create PC knowledge or control of an existing PC.

### 5.6 Catch-up projection

Define a bounded recipient-specific catch-up product that can orient a returning participant without full transcript preload.

Must preserve:

- current scene/party/actionable state;
- material changes since last relevant frontier;
- unresolved obligations/expected input for that participant;
- selective exact evidence when exact wording materially matters;
- knowledge/disclosure eligibility.

Catch-up remains a projection, not authority.

### 5.7 Split-party / causal bridges

R2.5 should use already accepted independent scene/context/chronology frontiers.

The active delta is collaboration behavior when:

- participants are in different scenes;
- one scene generates a message/entity/process consequence relevant to another;
- scenes converge;
- a player changes scene/party participation.

Do not create permanent cross-scene shared context merely because participants are in one campaign.

### 5.8 TurnEnvelope composition

Each participant request still gets its own R2.4 TurnEnvelope.

Define how collaboration/mode state influences:

- admitted input;
- whether resolution may proceed now or collect more contributions;
- which shared/live synchronization is required;
- which recipient-specific Narrator output is legal;
- whether a response is gameplay resolution, OOC coordination, catch-up or blocked/waiting state.

---

## 6. Active Diamond / Strong candidates

### D21 — Async multiplayer as persistent collaboration protocol

Active question: what minimal durable/recomputable collaboration semantics must survive participant absence beyond chat transcript, without becoming gameplay authority or global scheduler?

### D22 — Split-party scene/context/chronology frontiers — delta only

Independent scene/chronology frontiers are already accepted. Active question is only participant-context/collaboration behavior across material causal bridges and scene convergence.

### D23 — Mode-specific turn orchestration

Active question: which coordination semantics differ materially between free-form shared play and strict rules-owned ordered procedures?

### S43 — Social/meta separate from diegetic/action channel

Active question: how to classify mixed human input so OOC planning/readiness does not become PC speech/action automatically.

### S44 — Returning-participant catch-up projection

Active question: bounded recipient-scoped catch-up from durable sources without full transcript and without hiding exact-protected details.

### S45 — Explicit join/rejoin frontier acquisition

Active question: minimum semantic frontier acquisition before new/resumed input can mutate shared state.

### S54 — Input collection window/batch

Active question: whether/where free-form shared scenes admit bounded multi-participant collection before one resolution, and what closes the collection without relying on hidden online presence.

---

## 7. Inherited constraints — verify, do not reopen by overlap

- D20 observational finality of shared history;
- D24 one canon + participant-scoped context/disclosure;
- S41 authenticated participant -> controlled actor binding;
- S42 table administration separate from PC agency;
- S46 absence/idle does not grant PC takeover;
- S47 presence/typing/reconnect metadata is UX, not authority;
- S50 conflicting live mutations serialize per scope;
- S51 cheap incremental shared-frontier synchronization;
- S52 collaboration hot transfer bounded; durable deep history separate;
- S57 invitation/discovery does not equal durable authority binding.

If an inherited contract proves insufficient for a concrete R2.5 consumer, record the exact delta rather than redesigning the whole owner.

---

## 8. Negative / YAGNI boundaries

Do not introduce without concrete evidence:

- universal round-robin/global active-player state;
- always-on presence/heartbeat/polling service;
- automatic AI/GM control of absent PCs;
- generic collaboration message bus;
- duplicate party-chat transcript as canon;
- cross-player common secret-bearing context blob;
- global campaign chronology/clock;
- distributed transaction across independent live scenes;
- durable queue for every casual OOC message;
- spectator/replay system (S55 remains dormant);
- mixed human/AI PC controller framework (S58 remains dormant).

---

## 9. Exit criteria

R2.5 closes only when:

1. collaboration/coordination authority is explicitly bounded and does not duplicate gameplay owners;
2. supported input semantic classes are explicit;
3. mode-specific input collection/resolution rules are explicit without one universal global turn gate;
4. absence/async continuation preserves player agency and independent-scope progress;
5. join/rejoin frontier acquisition is explicit and race/currentness-safe at semantic level;
6. recipient-specific catch-up projection is explicit and bounded;
7. split-party collaboration uses existing independent scene/context/chronology frontiers and only material bridges;
8. per-participant R2.4 TurnEnvelope composition is explicit;
9. current live/shared synchronization owners remain authoritative rather than duplicated;
10. D21/D22/D23/S43/S44/S45/S54 have item-level dispositions;
11. inherited D20/D24/S41/S42/S46/S47/S50/S51/S52/S57 are verified or narrowly extended with rationale;
12. adversarial review covers agency takeover, secret leakage, stale rejoin, batch ambiguity, deadlock/starvation and cross-scene causality;
13. R2.6/R2.7 obligations are explicit;
14. no broad implementation is started.
