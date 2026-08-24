# R2.4 Decision Brief — Single-Context Turn Choreography & Instruction Shape

Status: **DECISION BRIEF / OWNER DECISION REQUIRED**

Date: 2026-08-24

Task brief:

- `2026-08-24-r2-4-single-context-llm-execution-task-brief.md`

Evidence ledger:

- `../research/2026-08-24-r2-4-single-context-llm-execution-evidence-ledger.md`

## 1. Decision to make

R2.4 must choose the baseline execution shape for one ordinary ChatGPT gameplay turn under the already accepted constraint:

```text
one user request
one assistant turn
one physical conversational context
multiple sequential logical HDM roles as needed
```

The material decision is:

> **Who controls logical phase activation/order and how explicit must the boundaries between nondeterministic phases be?**

This decision does not choose concrete prompt wording, JSON schemas, tool names, tokenizer limits or provider-specific buffering behavior.

---

## 2. Established facts

### F1 — Physical role isolation is not baseline architecture

The Step-4 amendment and Protocols 1–3 support explicit logical rebinding inside one shared physical context. Separate calls/agents remain optional defense/fallback only.

### F2 — Context/eligibility is already deterministic/typed

R2.3 owns `ContextNeedProfile`, currentness, eligibility, required packet closure and `RoleContextBundle`. A role cannot self-grant access merely because the model can physically see material.

### F3 — Accepted mechanics/state remain deterministic

Step 3 owns validation, IDs, rules, RNG, state transition, idempotency and replay boundaries.

### F4 — Model-owned large transport envelopes are undesirable

Protocol 2 observed malformed/repair-prone structured output when the model owned large strict transport JSON. Model-facing interfaces should be minimal semantic payloads; deterministic code owns serialization/bookkeeping.

### F5 — CORE is already physically present but only selectively active

`PLAY_POLICY.md` preloads the whole CORE corpus once and distinguishes `present` from `active`. Role/instruction activation should reuse that pattern rather than duplicate full role prompts.

### F6 — Narrator already has a logical emission boundary

Step 5.12 requires validated Narrator content/disclosure intent before `EMISSION_COMMIT`; ordinary interruption limitations are accepted and do not justify a delivery subsystem.

---

## 3. Alternative A — Model-Directed Collapsed Orchestration

One shared instruction tells the model to reason through whatever Interpreter/Dramaturg/Actor/Narrator responsibilities seem useful, call deterministic tools when needed, then emit the answer.

Conceptually:

```text
Player input
    -> model decides internal role sequence
    -> tool calls as needed
    -> final Narrator-style response
```

### Advantages

- lowest explicit orchestration complexity;
- minimal internal transport/token overhead;
- natural fit to ordinary ChatGPT;
- potentially fastest common path.

### Costs / risks

- phase omission becomes difficult to distinguish from ordinary reasoning choice;
- model can implicitly decide that Actor/Dramaturg context is unnecessary without a registered contract;
- multi-Actor private-state separation becomes less inspectable;
- typed result lifecycle/retry semantics become blurry;
- harder to test whether an authority boundary was crossed in the correct phase;
- tends toward one blended hidden reasoning process rather than explicit HDM role contracts.

### Assessment

Too weak for HDM's existing role/context architecture.

---

## 4. Alternative B — Registered Turn Envelope + Minimal Typed Gateways — RECOMMENDED

Use one logical `TurnEnvelope` for the assistant turn. The envelope defines the legal phase families/order constraints and the currently admitted phase state, but does **not** force every role to run.

Deterministic/registered contracts own:

- legal phase types;
- current role/subject/purpose binding;
- ContextNeedProfile/RoleContextBundle eligibility;
- allowed prior-role typed results;
- deterministic tool/commit gateways;
- terminal/fallback conditions.

The LLM may propose that an optional semantic phase is needed, but that proposal does not grant authority or new context. The phase executes only through the registered envelope/need contract.

Conceptually:

```text
TURN ENVELOPE

Player input
    |
    v
Interpreter? -------------- optional skip only when intent is already typed/unambiguous
    |
    v
Deterministic bind / Context decision
    |
    +--> Dramaturg? -------- only when latent preparation/undefined semantic choice is materially needed
    |
    +--> Actor[A]? --------- only when Actor-local unresolved cognition/action is material
    +--> Actor[B]? --------- separately rebound if needed
    |
    v
Deterministic execution / validation / accepted state
    |
    v
Narrator  ------------------ final ordinary gameplay visible phase
    |
    v
NarrationResult validation
    |
    v
EMISSION_COMMIT
```

A phase boundary is explicit logically even when no separate physical model call occurs.

### 4.1 Phase frame

Each active phase binds only the minimum control data needed conceptually:

```text
role
subject/player identity if applicable
purpose
ContextNeedProfile / RoleContextBundle identity
allowed typed prior-role results
accepted deterministic result refs where applicable
authority limits
output/result contract
phase-local steering if allowed
```

It does not restate all CORE instructions.

### 4.2 Minimal typed semantic handoffs

Role output crossing a phase boundary is the smallest semantic result needed downstream.

Examples:

- Interpreter: intent candidate / ambiguity signal;
- Dramaturg: bounded preparation/cue proposal;
- Actor: bounded action/cognition proposal or `NO_CHANGE`;
- Narrator: player-facing prose candidate + material disclosure intent;
- Context Runtime: typed assembly outcome/bundle identity;
- deterministic tools: validated results/receipts/state refs.

Private rationale/chain-of-thought is neither required nor persisted.

Large generic role-result JSON is not required; exact machine shapes remain implementation work.

### 4.3 Phase activation

Baseline roles are not all mandatory every turn.

Working activation rule:

- **Interpreter** — normally active for materially free-form/ambiguous user gameplay input; may be bypassed when an admitted typed/control path already provides unambiguous intent.
- **Dramaturg** — conditional; used when a material latent/provisional preparation/world-response choice is actually unresolved and existing state/processes do not already determine the next situation.
- **Actor** — zero or more; each material NPC/fictional subject decision gets its own subject-bound phase when Actor cognition/agency is actually required.
- **Narrator** — normally final ordinary gameplay phase whenever a player-facing gameplay response is emitted.
- **Chronicler** — opportunistic/non-hot-path under Step 5.10; may run as invisible logical work at a suitable boundary but cannot block ordinary gameplay correctness.
- **Commentator** — separate mode, not ordinary gameplay hot path.

### 4.4 Deterministic gateway

Every material transition follows:

```text
LLM proposal/interpretation
    -> deterministic validation/binding/execution
    -> accepted result/state
    -> later LLM phase may present/react to accepted result
```

If mechanics/state are already accepted and Narrator/another later phase fails, retry/regeneration starts from accepted result; it does not rerun mechanics/RNG.

### 4.5 Instruction hierarchy

R2.4 would recognize the following semantic layers:

```text
HOST CONSTITUTION
    system/developer/project-level immutable constraints

PROJECT / ENGINE CONTRACT
    Project Instructions + shipped CORE corpus

MODULE ACTIVATION
    present CORE text -> active modules for current situation

TURN ENVELOPE
    current request, legal phases, deterministic state/result frontier

ROLE PHASE FRAME
    role + subject + purpose + authority + output contract

ROLE CONTEXT
    R2.3 RoleContextBundle + allowed typed handoffs

PHASE-LOCAL STEERING
    non-authoritative presentation/task emphasis
```

Lower layers may narrow/instantiate higher layers but cannot override them.

Campaign/player/Story/tool text is data/evidence under applicable eligibility rules, not engine instruction merely because it contains imperative language.

### 4.6 Operational-output fencing

Only the validated Narrator player-facing payload intentionally crosses the ordinary gameplay `EMISSION_COMMIT` boundary.

Internal role frames/results, tool payloads, debug/trace material and operational markers remain internal.

String cleanup may be defense in depth but is not the semantic security boundary.

### 4.7 R2.3 UNSATISFIABLE caller policy

The envelope may choose only a finite registered response:

- skip the LLM phase and use a deterministic path if possible;
- narrow/reframe to another registered need profile once;
- ask one genuinely blocking player clarification;
- return a typed blocked/unsupported limitation;
- use another already-defined safe degradation.

It cannot silently guess or indefinitely reassemble the same impossible packet.

### Advantages

- preserves explicit Step-4 roles without multiplying physical calls;
- reuses R2.3 need/bundle boundaries;
- allows conditional phases and low common-path latency;
- makes multi-Actor rebinding testable;
- keeps deterministic authority/retry semantics explicit;
- avoids giant model-generated transport envelopes;
- composes naturally with full-CORE present-vs-active policy;
- supports structural S28 visible-output fencing;
- does not require provider abstraction or subagents.

### Costs / risks

- requires a small amount of phase state/bookkeeping;
- optional semantic activation cannot be entirely deterministic, so model-proposed phase need must itself be bounded;
- poor role-frame wording could still cause behavioral contamination despite correct logical architecture;
- physical streaming/buffering limitations remain to be validated in R2.6.

### Assessment

Best fit with current architecture/evidence.

---

## 5. Alternative C — Deterministic Explicit Phase FSM / Tool Checkpoint per Role

Every role transition is a deterministic state-machine edge and normally uses an explicit runtime/tool checkpoint before the next logical role phase.

Conceptually:

```text
Interpreter
 -> validate/store result
 -> Dramaturg decision gate
 -> validate/store result
 -> Actor gate
 -> validate/store result
 -> deterministic execution
 -> Narrator gate
 -> validate
 -> emit
```

### Advantages

- maximum inspectability;
- strongest explicit phase/retry identity;
- easy to test/control individual boundaries;
- clean future mapping to API/multi-agent profile.

### Costs / risks

- unnecessary tool/checkpoint overhead in ordinary ChatGPT turns;
- encourages persistence of transient nondeterministic results simply because the FSM has states;
- increases token/latency and malformed-transport surface;
- makes creative role activation excessively procedural;
- risks turning HDM into an orchestration framework rather than a game engine;
- no current evidence requires this amount of physical checkpointing.

### Assessment

Useful future defense/profile option, but overengineered as baseline.

---

## 6. Recommendation

Choose **Alternative B — Registered Turn Envelope + Minimal Typed Gateways**.

Confidence: **HIGH**.

Reason:

> The accepted architecture already separates logical roles, context eligibility and deterministic authority, while empirical evidence shows those role boundaries can behave correctly in one physical context. The minimum additional machinery is therefore an explicit bounded turn/phase contract and small typed handoffs — not separate agents, and not an unstructured blended reasoning pass.

B preserves the product requirement:

```text
one user request
one assistant turn
```

without sacrificing:

```text
role-local eligibility
Actor-local cognition
deterministic authority
retry safety
Narrator disclosure boundary
```

---

## 7. Proposed R2.4 laws if B is approved

1. **TURN ENVELOPE, NOT ROLE=CALL** — one physical assistant turn may contain several explicit logical phases; a logical role does not imply a separate model invocation.
2. **REGISTERED PHASE VOCABULARY** — only admitted phase/result families participate in ordinary execution; model suggestion cannot invent a new authority-bearing phase.
3. **CONDITIONAL ACTIVATION** — Interpreter/Dramaturg/Actor phases run only when their semantic work is materially required; Narrator is the final ordinary player-facing gameplay phase.
4. **REBIND BEFORE PHASE** — every phase rebinds role, subject, purpose, eligible bundle/handoffs, authority and output contract.
5. **NO RAW PRIVATE HANDOFF** — only minimum typed semantic results or lawful observable evidence cross role boundaries.
6. **NO HIDDEN-REASONING DEPENDENCY** — private rationale/chain-of-thought is not required persistence, recovery or authority evidence.
7. **DETERMINISTIC ACCEPTANCE GATE** — material mechanics/state/disclosure consequences require their existing deterministic/native owner acceptance path.
8. **NO MECHANICS REPLAY AFTER ACCEPTANCE** — later LLM failure/regeneration cannot rerun accepted mechanics/RNG.
9. **EXISTING CORE, SEMANTIC ACTIVATION** — the physically present CORE corpus is activated/narrowed; role frames do not duplicate the engine instruction set.
10. **PHASE-LOCAL STEERING IS NON-AUTHORITATIVE** — turn-local task/tone/presentation steering cannot override truth, eligibility or engine law; prompt position is optimization only.
11. **NARRATOR-ONLY ORDINARY VISIBLE PAYLOAD** — internal phases/tool/debug protocol do not intentionally cross the player-facing emission boundary.
12. **SANITIZATION IS DEFENSE IN DEPTH** — structural output fencing is primary; string stripping cannot establish secrecy.
13. **FINITE UNSATISFIABLE FALLBACK** — Context Runtime failure produces a registered finite alternate path, never silent guessing or an unbounded assembly loop.
14. **CHRONICLER NONBLOCKING / COMMENTATOR SEPARATE MODE** — neither expands the ordinary hot path absent a concrete current need.

---

## 8. Exact owner decision

Choose one:

- **A — Model-Directed Collapsed Orchestration**
- **B — Registered Turn Envelope + Minimal Typed Gateways** **[recommended]**
- **C — Deterministic Explicit Phase FSM / Tool Checkpoint per Role**

Approval of B approves the semantic direction/laws above, not final schema syntax, prompt text, tool count or host-specific streaming implementation.
