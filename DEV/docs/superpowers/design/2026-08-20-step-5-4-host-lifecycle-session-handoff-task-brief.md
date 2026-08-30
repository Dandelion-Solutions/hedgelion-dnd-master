# Step 5.4 — Host Lifecycle & Session Handoff — Task Brief

Status: **RESEARCH ASSIGNMENT — ARCHITECTURAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Problem statement

Define the logical continuity semantics for creation, controlled destruction, transfer, restart, staleness and unexpected loss of an HDM gameplay host/runtime/chat context.

The design must distinguish what the engine can **guarantee before a known destructive lifecycle boundary** from what it can only **recover after an unexpected loss**. It must preserve Step-5.2 resumable-runtime closure and Step-5.3 pending/temporal continuity without making raw chat/model/process memory campaign authority.

This slice must not silently absorb Step 5.5 durability cadence/classification, Step 5.6 Git transaction mechanics, Step 5.7 checkpoint representation, or Step 5.8 multiplayer/live ownership transfer.

## 2. Fixed inherited constraints

Preserve unless a contradiction requires an explicit architecture decision:

- Step 5.1 B-NARROW domain typing and no implicit cross-domain order;
- Step 5.2 native-owner preservation, bounded typed recovery routing, pinned native hydration, owning-scope resolution and no invented lost HOT/SOFT state;
- Step 5.2 conditional recovery relevance of unresolved accepted Interaction/IntentPlan when the applicable handoff/durability policy promises that semantic point;
- Step 5.3 A-NARROW source/execution continuity and continuous bounded recovery reachability;
- Procedure/Resolution/Continuation and other Step-3 owners remain execution authority;
- checkpoints are sparse recovery evidence, not current-state authority or a universal snapshot;
- `STATE/CURRENT` is compact routing/current-state metadata, not a generic pending-work or handoff payload;
- no campaign-wide/history scan on normal cold recovery;
- cold hydration and host elapsed time do not advance fictional time;
- no persistence of hidden chain-of-thought, raw model state, complete prompt/context or opaque process memory as gameplay authority;
- exact old utterance wording may be used only when genuine retained evidence exists; semantic state must not be reconstructed by invented quotation;
- physical model-call topology remains Step 6.

## 3. Owner clarification — periodic safety flush carry-forward

Owner direction on 2026-08-20:

1. A host/runtime that **knows** its current context is about to be destroyed or invalidated should be able to trigger a recovery-publication attempt before that destructive boundary. The lifecycle trigger and success/failure semantics belong to Step 5.4.
2. Independently of any lifecycle warning, singleplayer should have a bounded maximum age/exposure for gameplay-significant unpublished SOFT state so recovery exposure does not grow without bound when ordinary SOFT accumulation is slow. The durability policy belongs to Step 5.5.
3. The previously discussed `one hour` value is an example only and is **not an approved canonical threshold or heuristic**.
4. The architecture should reason in terms of age/exposure of unpublished gameplay-significant state, not merely `time since any Git commit`.
5. Clean state must not create heartbeat/no-op publications merely to keep repository activity recent.

Current runtime prose in `GAME/CORE/DURABILITY_GUARD.md`, `GAME/CORE/SESSION.md`, `GAME/CORE/PERSISTENCE.md`, `GAME/CORE/STORAGE.md` and related tests already hard-codes or assumes a one-hour dirty ceiling. Treat that numerical policy as **pre-Step-5.5 architecture debt / stale provisional policy**, not as a fixed constraint for Step 5.4.

### 3.1 Owner clarification — host conversation-capacity exhaustion

Owner direction on 2026-08-20 adds a concrete observed failure mode: a ChatGPT conversation may become physically unwritable because the host reports that the conversation/message limit has been reached, forcing continuation in another chat.

For Step 5.4:

1. Treat host conversation/context capacity exhaustion as a destructive host-lifecycle case distinct from gameplay lifecycle.
2. The current architecture **MUST NOT assume** that HDM receives a trustworthy remaining-message, remaining-token, remaining-context-capacity or time-to-hard-stop metric.
3. A host-provided **reliable impending-destruction signal**, if one exists, may trigger the ordinary controlled handoff barrier.
4. A host-provided **advisory near-capacity signal**, if one exists, may trigger a player-facing warning and proactive handoff recommendation; correctness still cannot depend on sufficient warning time remaining.
5. Message count, approximate token count, chat age, remembered product limits or inferred context usage are not authoritative remaining-capacity evidence.
6. A future heuristic based on such signals may be investigated as an optimization/advisory feature, but it must be explicitly non-authoritative and failure to predict the cutoff must degrade to ordinary unexpected-loss semantics.
7. If no usable signal exists and the host hard-stops immediately, no pre-destruction action can be guaranteed; Step 5.5 periodic durability risk-control limits the likely loss, and recovery uses the newest actually durable compatible source set.

No numerical capacity threshold or prediction heuristic is approved by this clarification.

## 4. Lifecycle cases that must be distinguished

At minimum:

1. fresh/new chat with no old model/process memory;
2. ordinary resume after an already durable prior stop;
3. explicit controlled handoff from one runtime/chat to another;
4. reliable impending context/window destruction signal;
5. advisory host near-capacity warning with uncertain remaining capacity;
6. host conversation/message/context hard stop with no usable prior warning;
7. controlled runtime restart or runtime-package switch;
8. maintenance restart/suspension;
9. explicit player pause/end versus mere host/context destruction;
10. unexpected process/context crash with no finalization opportunity;
11. publication/network failure during a controlled destructive boundary;
12. stale old runtime/chat reappearing after newer authoritative state exists;
13. multiplayer/live-owned scope handoff insofar as 5.4 must state logical requirements without selecting the 5.8 transfer protocol.

## 5. Goals

Step 5.4 must determine:

### G1 — Lifecycle taxonomy

Define a minimal taxonomy that distinguishes:

- non-destructive interruption;
- controlled destructive boundary;
- advisory impending-capacity condition;
- uncontrolled destructive loss/hard stop;
- stale/revoked host;
- fresh hydration.

Do not force all host events into one state machine when their guarantees differ.

### G2 — Controlled handoff guarantee

Define what must be true before the engine may acknowledge a controlled handoff/context destruction as recovery-safe.

Determine whether the correct logical contract is:

```text
known destructive boundary
    -> freeze/close the current semantic mutation window
    -> ensure the promised resumable source set is durably recoverable
    -> acknowledge handoff/destruction
```

and what happens if the required durability attempt cannot complete.

### G3 — Unexpected-loss recovery objective

Define an exact, honest recovery/RPO statement for a crash or host hard stop that occurs without a finalization opportunity.

The design must not imply reconstruction of unpublished volatile state. It must state how a fresh host identifies the newest actually durable compatible recovery source set.

### G4 — Semantic resume point

Determine how an unresolved gameplay point survives destructive handoff without persisting chat/model memory.

Reconcile:

- Step-3 Interaction / IntentPlan / RuntimeCommand / Resolution / Procedure / Continuation owners;
- current `SESSION.md` maintenance-continuation prose;
- `session.schema.yaml` coordination metadata;
- checkpoints/current-state routing;
- exact utterance evidence versus semantic summary.

Prefer existing typed semantic owners over a new generic handoff payload.

### G5 — Bootstrap from durable evidence only

Specify the logical new-host bootstrap contract:

```text
no old process/model memory
    -> select compatible durable native sources
    -> boundedly hydrate active owners
    -> validate interpretation/authority/staleness
    -> rebuild derived state
    -> resume or return typed recovery-required outcome
```

Do not choose the final Step-5.7 wire format here.

### G6 — Failure and acknowledgement semantics

Define outcomes for:

- handoff publication succeeds;
- publication fails before destructive boundary;
- host disappears during/after an ambiguous write attempt;
- host reaches a hard conversation-capacity stop before handoff can complete;
- old host resumes after another host advanced state;
- required recovery evidence is missing or incompatible.

Do not define the physical Git failure algorithm owned by 5.6.

### G7 — Session metadata role

Decide whether persistent `session` records are:

- semantic gameplay owners;
- coordination/recovery projections;
- optional observability metadata;
- partially obsolete.

Do not let session metadata become a duplicate owner of current gameplay/execution state.

### G8 — Host-capacity signal contract

Define the correctness boundary among:

```text
RELIABLE IMPENDING-DESTRUCTION SIGNAL
    -> may force controlled handoff barrier

ADVISORY CAPACITY SIGNAL
    -> may warn / recommend handoff
    -> does not prove remaining time/capacity

NO USABLE SIGNAL
    -> no pre-destruction guarantee
    -> unexpected-loss fallback
```

Ensure that future heuristics cannot silently become correctness authority.

### G9 — Later-slice requirements

Emit logical requirements only for:

- 5.5 durability classification/cadence, including the independent maximum unpublished-SOFT exposure policy;
- 5.6 publication/crash consistency;
- 5.7 checkpoint/hydration protocol;
- 5.8 live/multiplayer authority transfer/staleness;
- 5.11 exact transcript retention when wording evidence matters;
- 5.12 host delivery boundary where emitted/acknowledged narration intersects a crash.

## 6. Non-goals

Step 5.4 SHALL NOT select or canonicalize:

- the numeric maximum SOFT dirty age/exposure or any specific timer value;
- a numeric host-capacity warning threshold;
- a formula for estimating remaining ChatGPT messages/tokens/context lifetime;
- complete SOFT/HARD/EPHEMERAL/SAVE semantics;
- ordinary gameplay publication cadence;
- exact dirty dependency closure for every durability class;
- physical Git tree/commit/ref algorithm;
- checkpoint schema/wire format or exact recovery-cut representation;
- live-epoch lease/CAS/transfer/compaction protocol;
- chronology persistence representation;
- transcript retention duration;
- Story publication jobs;
- exact host-delivery acknowledgement state machine;
- background timers/daemons that the host platform does not provide;
- raw LLM context serialization.

## 7. Required repository evidence

Inspect at least:

- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- Step-5 expanded agenda;
- Step-5.2 canonical v2;
- Step-5.3 canonical spec;
- Step-3 execution/Continuation contracts as needed;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/BOOTSTRAP_RUNTIME.md`;
- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/MULTIPLAYER.md` / `LIVE_SCENE.md` only to identify 5.8 boundary constraints;
- `GAME/SCHEMA/session.schema.yaml`;
- `GAME/SCHEMA/current_state.schema.yaml`;
- `GAME/SCHEMA/checkpoint.schema.yaml`;
- current DEV runtime execution/recovery schemas where needed.

Search current consumers for session/handoff/context-loss/maintenance-continuation terminology after the structural pass.

Host-product capability research may inform whether a particular signal exists, but absence of a documented signal must remain a supported architecture case.

## 8. Framing challenges

The research must actively test these possible mistakes:

1. **Do not equate chat session with gameplay session.** A host context may die while campaign/session semantics continue.
2. **Do not equate controlled handoff with unexpected crash.** The former can require a pre-destruction barrier; the latter cannot retroactively create one.
3. **Do not make a handoff record a second state snapshot.** Prefer native owners + existing recovery routing.
4. **Do not assume a host gives an expiry warning or capacity counter.** Lifecycle-warning capability may be optional; recovery safety cannot depend solely on it.
5. **Do not infer authoritative remaining capacity from message count, approximate token count, chat age or remembered host limits.** Such inputs may support only explicitly advisory future heuristics.
6. **Do not assume background execution.** If no interaction/runtime callback occurs, the engine cannot promise an exactly timed flush.
7. **Do not use `last commit age` as the semantic dirty-age definition.** Unrelated commits may not include the relevant unpublished state.
8. **Do not let `session.status=active` grant or retain write authority.** Stale coordination metadata cannot override current branch/live ownership.
9. **Do not persist transcript/chat simply for seamless prose.** Preserve exact wording only when real evidence/semantics require it.
10. **Do not manufacture a universal recovery frontier.** Step 5.1/5.2 permit composed compatible native source sets.
11. **Do not make maintenance continuation frame RAM-only when the operation may actually destroy that RAM/context.** Distinguish non-destructive maintenance from destructive handoff.
12. **Do not decide 5.5 by accident.** Step 5.4 may require a durability attempt when destruction is known, but the general durability classifier and numerical ceilings remain 5.5.
13. **Do not decide 5.8 by accident.** A stale old host must not mutate new authority, but exact live ownership transfer belongs later.

## 9. Quality attributes / fitness criteria

A candidate architecture must provide:

- no false acknowledgement of a controlled recovery-safe handoff;
- honest RPO semantics after unexpected loss or host hard stop;
- bounded cold bootstrap without prior chat memory;
- no duplicate current-state authority;
- no hidden dependence on exact transcript retention;
- deterministic resume of already accepted execution;
- explicit stale-host behavior;
- compatibility with partitioned multiplayer/live ownership;
- no correctness dependence on host capacity-warning support;
- no required background daemon/timer;
- minimal additional persistent state;
- testable lifecycle/crash-window outcomes;
- clean responsibility boundaries into 5.5–5.8 and 5.11–5.12.

## 10. Required analytical challenge

Before recommendation, explicitly challenge:

- strongest case for a first-class durable handoff/session-transfer record;
- strongest case for using the existing `session` record as handoff authority;
- whether a controlled handoff can be valid without flushing every gameplay-significant volatile state promised across that handoff;
- whether a final handoff publication must block further mutation while pending;
- whether failure to publish should abort the handoff, permit degraded handoff to the older durable point, or depend on user intent;
- ambiguity when publication result is unknown because the host dies mid-transport;
- old host resurrection after new host resumes;
- maintenance that switches runtime package but retains host context versus maintenance that destroys it;
- exact wording that is the only evidence of accepted player meaning;
- whether a known maximum context lifetime without an explicit warning should create a 5.4 lifecycle trigger or remain solely a 5.5 risk-mitigation input;
- whether a host advisory warning can safely trigger proactive handoff without being mistaken for a guaranteed remaining-capacity measurement;
- whether a future heuristic based on message/token/context estimates can remain strictly advisory under failure.

## 11. Minimum lifecycle/crash matrix

Research must cover at least:

1. clean new chat from durable state;
2. controlled handoff with no dirty state;
3. controlled handoff with dirty canonical state;
4. handoff while RuntimeCommand/Resolution/Continuation is active;
5. handoff while waiting on Choice/Reaction;
6. handoff publication failure while old host remains alive;
7. old host dies after preparing but before acknowledging publication;
8. write may have succeeded but acknowledgement is lost;
9. abrupt crash with recent unpublished SOFT state;
10. abrupt crash immediately after a previously successful durable boundary;
11. reliable context-destruction warning arrives during an unresolved player interaction;
12. advisory near-capacity warning arrives but remaining usable capacity is unknown;
13. hard conversation/message/context stop occurs with no usable warning and no finalization opportunity;
14. a future heuristic predicts imminent exhaustion incorrectly (false positive or false negative);
15. maintenance switch with current context retained;
16. maintenance switch that destroys current context;
17. fresh host sees stale `session.status=active` from dead host;
18. stale old host tries to continue after fresh host has advanced durable state;
19. multiplayer/live scope has newer authority than campaign base;
20. exact prior utterance unavailable but accepted semantic Interaction/IntentPlan is durable;
21. exact prior utterance is genuinely the only evidence preserving accepted meaning;
22. no host warning exists and SOFT state accumulates for a long time;
23. no dirty state exists when lifecycle warning/dirty-exposure limit is evaluated.

## 12. Expected outputs

Produce:

A. lifecycle taxonomy and ownership matrix;
B. controlled-handoff state/guarantee model;
C. unexpected-loss recovery/RPO contract;
D. semantic resume-point disposition by current owner family;
E. stale-host / failure matrix;
F. host-capacity signal classification and advisory-heuristic boundary;
G. alternatives with recommendation;
H. analytical challenge and decision brief only if a genuinely reasonable owner-level choice remains;
I. explicit carry-forward requirements/debt for 5.5–5.8 and 5.11–5.12.

## 13. Exit criteria

Step 5.4 research is decision-ready only when:

- controlled handoff and unexpected crash/hard-stop have distinct, non-contradictory guarantees;
- known destructive context loss has an explicit logical publication obligation without assuming a specific Git protocol;
- missing host warning/capacity telemetry remains a supported correctness case;
- advisory future capacity heuristics cannot become authoritative durability or recovery evidence;
- the fresh host can resume from durable native evidence without old chat/process memory;
- unresolved accepted gameplay state is owned by existing typed semantic/execution owners wherever possible;
- stale host/session metadata cannot become write authority;
- no exact transcript requirement is introduced merely for narrative smoothness;
- failure/ambiguity during handoff has explicit outcomes;
- the independent maximum unpublished-SOFT exposure concept is explicitly deferred to 5.5 with no approved numerical value;
- current one-hour runtime prose is identified as provisional/stale until 5.5 decides the durability policy;
- later physical persistence/live/checkpoint/delivery details remain cleanly deferred;
- no generic handoff snapshot/ledger is introduced without demonstrated need.

## 14. Task-brief self-review

Self-review result: **PASS FOR RESEARCH**.

The brief does not assume that a new handoff record, a session record, a checkpoint, a universal recovery frontier, a particular durability timer or a host-provided capacity counter is the correct solution. It permits the investigation to conclude that existing native recovery owners plus a lifecycle barrier are sufficient, while treating host-capacity detection as optional capability rather than correctness authority.