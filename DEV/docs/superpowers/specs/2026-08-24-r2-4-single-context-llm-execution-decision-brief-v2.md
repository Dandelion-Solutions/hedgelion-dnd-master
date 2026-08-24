# R2.4 Decision Brief v2 — Single-Context Turn Choreography, Chronicler Service & Instruction Shape

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Supersedes for decision purposes:

- `2026-08-24-r2-4-single-context-llm-execution-decision-brief.md`

Additional owner/evidence inputs:

- `2026-08-24-r2-4-chronicler-service-owner-clarification.md`
- `../research/2026-08-24-r2-4-chronicler-service-evidence-addendum.md`

The original R2.4 task brief/evidence ledger remain valid except where they described Chronicler as merely opportunistic/non-hot-path without a first-safe-opportunity anti-starvation obligation.

## 1. Decision to make

R2.4 must choose the baseline execution shape for one ordinary ChatGPT gameplay turn under:

```text
one user request
one assistant turn
one physical conversational context
multiple sequential logical HDM roles as needed
```

Material decision:

> **Who controls logical phase activation/order, including mandatory anti-starvation service of backlogged Chronicler work, and how explicit must the boundaries between nondeterministic phases be?**

This does not choose concrete prompt wording, JSON schemas, tool names, exact budget numbers or host-specific streaming implementation.

## 2. Established facts

1. Step-4 amendment + Protocols 1–3 support explicit logical role rebinding inside one physical context; separate role calls are not baseline requirements.
2. R2.3 already owns typed context/eligibility/currentness/packet assembly.
3. Step 3 owns deterministic mechanics/state/RNG/idempotency.
4. Protocol 2 argues against large model-owned transport envelopes; deterministic code owns serialization/validation/bookkeeping.
5. `PLAY_POLICY.md` already uses `physically present != semantically active` for the full CORE corpus.
6. Step 5.12 already owns Narrator validation -> `EMISSION_COMMIT`.
7. Step 5.10 already owns queue-free Story backlog/coverage, bounded catch-up, deterministic Story publication and gameplay-priority concurrency.
8. Owner clarification adds a stronger R2.4 product policy: **backlogged Chronicler/Story work must receive bounded service at the first safe opportunity and may not be indefinitely starved by optional work**.

## 3. Alternative A — Model-Directed Collapsed Orchestration

The model internally decides which roles/tasks to perform and when.

```text
Player input
    -> blended model reasoning / self-selected roles
    -> deterministic tools as needed
    -> final response
```

Advantages:

- minimum explicit orchestration;
- low control overhead.

Material problems:

- phase omission is difficult to distinguish from silent model choice;
- Actor/Dramaturg boundaries are less inspectable;
- model can forget or repeatedly defer Chronicler without a deterministic service-opportunity check;
- no robust evidence that Story backlog was evaluated on each envelope;
- typed retry/lifecycle boundaries remain blurry.

Assessment: **REJECT as too weak**.

## 4. Alternative B — Registered Turn Envelope + Minimal Typed Gateways — RECOMMENDED

One logical `TurnEnvelope` owns admitted phase families, required ordering constraints, current deterministic frontier and service-opportunity decisions.

The model may propose optional semantic work, but it cannot grant itself context/authority or cancel a registered service obligation.

Conceptually:

```text
TURN ENVELOPE

Player input
    |
    v
Interpreter?                 conditional
    |
    v
Deterministic bind/context
    |
    +--> Dramaturg?          material current-turn need only
    +--> Actor[A]?           material subject-local decision only
    +--> Actor[B]?           separately rebound
    |
    v
Deterministic execution / accepted state
    |
    +--> evaluate Story backlog + Chronicler service opportunity
    |       |
    |       +--> SERVICE bounded window when safe
    |       +--> DEFER(reason) when genuinely blocked
    |       +--> NO_BACKLOG
    |
    v
Narrator                    protected final visible phase
    |
    v
NarrationResult validation
    |
    v
EMISSION_COMMIT
```

The diagram is semantic. Exact physical sequencing may reserve Narrator/output capacity before executing a Chronicler service slot so that Story work cannot consume the response margin.

### 4.1 Registered phase frame

Each phase binds only minimum control information:

```text
role
subject/player identity where applicable
purpose
RoleContextBundle / need-profile identity
allowed typed prior results
accepted deterministic refs
authority limits
output/result contract
phase-local steering when allowed
```

Existing CORE instructions are activated/narrowed; they are not duplicated into giant role prompts.

### 4.2 Minimal typed handoffs

Examples:

- Interpreter -> intent candidate / ambiguity;
- Dramaturg -> bounded provisional preparation/cue;
- Actor -> bounded action/cognition proposal or `NO_CHANGE`;
- Chronicler -> `StoryProjectionDraft` semantics for a bounded source window when generative/editorial work is required;
- Narrator -> prose candidate + disclosure intent;
- deterministic owners -> validated results/receipts/state refs.

Private rationale/chain-of-thought is not required persistence or transport.

### 4.3 Activation policy

- **Interpreter** — normally active for materially free-form/ambiguous player input; skippable for already-admitted typed/unambiguous control paths.
- **Dramaturg** — conditional on material current-turn provisional/world-response work not already determined by accepted state/processes.
- **Actor** — zero or more; each subject receives a separate logical rebind when its unresolved cognition/agency materially matters.
- **Chronicler** — **deferred-service role, not merely optional**. Every TurnEnvelope evaluates typed Story backlog. When backlog exists and a safe service window exists, a bounded Chronicler/Story catch-up slot is mandatory. If blocked by heavy scene construction, intense multi-participant play, save/serialization/recovery/conflict or insufficient protected budget, it may defer with the obligation preserved. Backlogged service outranks nonessential optional enrichment once current-turn correctness and protected Narrator/output capacity are reserved.
- **Narrator** — normally final player-facing gameplay phase; its protected output capacity cannot be consumed by Chronicler maintenance.
- **Commentator** — separate mode, not ordinary gameplay hot path.

### 4.4 Chronicler anti-starvation without scheduler

No durable `StoryProjectionJob` is introduced.

Service need is recomputed from existing Step-5.10 state:

```text
Story backlog = source-domain basis/watermark - compatible coverage
```

Every envelope returns conceptually:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

A `SERVICE(window)` need may process only a bounded batch. If backlog remains, subsequent safe envelopes continue servicing it.

There is no fixed `every N turns` or wall-clock SLA in R2.4. The guarantee is **first safe opportunity**, with host-specific practical budget validated in R2.6.

This also does not mean one Story Git commit after every gameplay turn. Step-5.10 batching, validation, layer-local publication and same-ref gameplay priority remain authoritative.

### 4.5 Deterministic gateway/retry

```text
LLM interpretation/proposal
    -> deterministic validation/execution
    -> accepted state/result
    -> later LLM phase
```

After accepted mechanics, Narrator/Chronicler/other nondeterministic failure must not replay mechanics or RNG.

Chronicler itself never owns final Story IDs, coverage advancement, publication or canon promotion.

### 4.6 Instruction hierarchy

```text
HOST CONSTITUTION
    system/developer/project constraints

PROJECT / ENGINE CONTRACT
    Project Instructions + shipped CORE

MODULE ACTIVATION
    present CORE -> active for current situation

TURN ENVELOPE
    legal phases + service obligations + deterministic frontier

ROLE PHASE FRAME
    role / subject / purpose / authority / output

ROLE CONTEXT
    R2.3 RoleContextBundle + legal handoffs

PHASE-LOCAL STEERING
    non-authoritative current emphasis
```

Player/campaign/Story/tool prose remains data/evidence, not executable engine instruction.

### 4.7 Output fencing

Only validated Narrator player-facing payload intentionally crosses ordinary gameplay `EMISSION_COMMIT`.

Chronicler drafts, Story control metadata, role frames, tool/debug traces and operational markers remain internal.

### 4.8 R2.3 `UNSATISFIABLE`

Finite registered alternatives only:

- deterministic path;
- one narrower registered need/profile;
- genuinely blocking player clarification;
- registered legal degradation;
- typed blocked/unsupported result.

No silent guess or unbounded assembly loop.

### Advantages

- explicit Step-4 roles without physical call multiplication;
- low common-path overhead;
- testable Actor rebinding;
- deterministic authority/retry boundaries;
- minimal model transport;
- natural composition with present-vs-active CORE policy;
- structural visible-output fencing;
- **enforces Chronicler first-safe-opportunity service without queue/scheduler/FSM overengineering**.

### Costs / risks

- small envelope/service-decision bookkeeping;
- safe-opportunity classification needs measurable budget rules in R2.6;
- poor role-frame wording remains a behavioral-containment risk to test;
- exact host buffering/streaming remains R2.6 evidence work.

Assessment: **BEST FIT**.

## 5. Alternative C — Deterministic Explicit Phase FSM / Checkpoint per Role

Every role transition/service slot is a deterministic FSM edge with explicit checkpoint/tool state.

Advantages:

- strongest inspectability;
- easy explicit Chronicler scheduling/deferral state.

Costs:

- unnecessary hot-path checkpoints;
- encourages persistence of transient role results;
- higher latency/token/transport complexity;
- duplicates queue/lifecycle machinery already avoided by Step 5.10;
- no current evidence requires this rigidity.

Assessment: **future defense/profile option; overengineered baseline**.

## 6. Recommendation

Choose **Alternative B — Registered Turn Envelope + Minimal Typed Gateways**, amended with **first-safe-opportunity Chronicler service**.

Confidence: **HIGH**.

This preserves both goals:

```text
current gameplay always wins when materially loaded
AND
Story/Chronicler cannot be forgotten once spare safe capacity returns
```

## 7. Proposed R2.4 laws if B is approved

1. **TURN ENVELOPE, NOT ROLE=CALL** — one assistant turn may execute several explicit logical phases without one physical call per role.
2. **REGISTERED PHASE VOCABULARY** — model suggestion cannot invent authority-bearing phases.
3. **CURRENT-TURN MATERIAL PHASE ACTIVATION** — Interpreter/Dramaturg/Actor activate only when their current semantic work is material.
4. **CHRONICLER SERVICE OBLIGATION** — compatible Story backlog creates a deferred service obligation evaluated on every TurnEnvelope.
5. **FIRST SAFE OPPORTUNITY** — when backlog exists and a bounded service window fits after reserving current-turn correctness and Narrator/output requirements, Chronicler/Story service is mandatory.
6. **DEFER DOES NOT CANCEL** — heavy scene/Dramaturg load, intense multi-Actor play, save/serialization/recovery/conflict or insufficient protected budget may defer Story service, but backlog/coverage keeps the obligation alive.
7. **BOUNDED CATCH-UP** — one service slot may process a finite source window; residual backlog continues to future safe opportunities.
8. **NO STORY SCHEDULER REQUIRED** — backlog/service need is recomputed from Step-5.10 coverage and source basis; no durable job queue or background-worker dependency.
9. **GAMEPLAY PRIORITY / OPTIONAL-WORK STARVATION BAN** — Chronicler never preempts correctness-critical current play, but backlogged service outranks nonessential optional enrichment once protected current-turn needs are reserved.
10. **REBIND BEFORE PHASE** — role/subject/purpose/context/handoff/authority/output contract rebound every phase.
11. **NO RAW PRIVATE HANDOFF** — only minimum typed results or lawful observable evidence cross role boundaries.
12. **NO HIDDEN-REASONING DEPENDENCY** — chain-of-thought/private rationale is not required persistence/recovery state.
13. **DETERMINISTIC ACCEPTANCE GATE** — mechanics/state/Story coverage/disclosure consequences remain with native deterministic owners.
14. **NO MECHANICS REPLAY AFTER ACCEPTANCE** — later LLM/Story/presentation failure cannot rerun accepted mechanics/RNG.
15. **EXISTING CORE, SEMANTIC ACTIVATION** — role frames activate/narrow existing shipped instructions rather than duplicating them.
16. **PHASE-LOCAL STEERING IS NON-AUTHORITATIVE**.
17. **NARRATOR-ONLY ORDINARY VISIBLE PAYLOAD** — Chronicler/internal/tool protocol remains invisible.
18. **SANITIZATION IS DEFENSE IN DEPTH** — structural fencing is primary.
19. **FINITE `UNSATISFIABLE` FALLBACK** — no guessing/retry loops.
20. **COMMENTATOR SEPARATE MODE** — Commentator does not join ordinary gameplay hot path unless explicitly invoked by its mode contract.

## 8. Exact owner decision

Choose one:

- **A — Model-Directed Collapsed Orchestration**
- **B — Registered Turn Envelope + Minimal Typed Gateways + first-safe-opportunity Chronicler service** **[recommended]**
- **C — Deterministic Explicit Phase FSM / Checkpoint per Role**

Approval of B approves the semantic direction/laws above, not final schema syntax, prompt text, exact tool count or host-specific timing thresholds.
