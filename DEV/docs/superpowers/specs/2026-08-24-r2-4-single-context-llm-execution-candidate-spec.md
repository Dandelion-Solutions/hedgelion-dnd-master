# R2.4 Candidate Specification — Single-Context Turn Envelope, Typed Role Gateways and Chronicler Service

Status: **CANDIDATE ARCHITECTURE — ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-24

Owner-approved direction:

> **Registered Turn Envelope + Minimal Typed Gateways + first-safe-opportunity Chronicler service**

Inputs:

- R2.4 task brief and evidence ledger;
- R2.4 Chronicler service owner clarification and evidence addendum;
- R2.4 Decision Brief v2;
- R2.4 owner decision;
- Step-4 canonical role/context architecture plus single-context amendment;
- R2.1–R2.3 canonical specifications;
- Step-3 deterministic execution authority;
- Step-5.10 Story projection durability;
- Step-5.12 host emission/disclosure boundary;
- current shipped `PLAY_POLICY.md`, `AI_REASONING.md`, `NPC.md`, `PREP.md`, `NARRATIVE.md`;
- Protocols 1–3.

This candidate defines logical execution/instruction architecture only. It does not implement prompts, schemas, tool APIs, host buffering, exact token thresholds or provider abstraction.

---

## 1. Central invariant

Ordinary HDM gameplay executes inside:

```text
one user request
one assistant turn
one physical conversational context
```

while preserving explicit logical phase boundaries.

Conceptually:

```text
TurnEnvelope
    -> Interpreter?                 # conditional
    -> deterministic bind/context
    -> Dramaturg?                  # conditional
    -> Actor[subject_1]?           # conditional
    -> Actor[subject_2]?           # separately rebound
    -> deterministic execution / accepted state
    -> Story backlog/service decision
         -> NO_BACKLOG
         -> SERVICE(bounded window)
         -> DEFER(typed reason)
    -> Narrator                    # protected final visible phase
    -> NarrationResult validation
    -> EMISSION_COMMIT
```

The exact physical micro-order may vary where dependencies permit, but the semantic boundaries and priority rules in this specification do not.

## LAW R2.4-1 — TURN ENVELOPE, NOT ROLE=CALL

A logical role phase does not imply a separate model invocation, agent, process or chat. Several logical phases may execute sequentially in one assistant turn.

---

## 2. `TurnEnvelope` responsibility

`TurnEnvelope` is the bounded logical execution frame for one assistant turn. It is working control state, not campaign authority.

Conceptually it binds:

```text
turn/request identity where required
current accepted deterministic frontier
legal phase families/order constraints
current phase binding
registered ContextNeedProfile / RoleContextBundle identities
allowed prior-role typed results
safe fallback/terminal classes
protected Narrator/output reservation
Story backlog/service-opportunity result
```

It does not duplicate world state, role-private evidence, Story coverage or deterministic execution state.

## LAW R2.4-2 — REGISTERED PHASE VOCABULARY

Only registered logical phase/result families may participate in ordinary execution. The model may propose an optional phase need but cannot invent a new authority-bearing phase or gateway.

## LAW R2.4-3 — ENVELOPE IS CONTROL, NOT AUTHORITY

The TurnEnvelope may route and constrain work. It cannot establish world truth, Actor cognition, Story coverage, disclosure, mechanics or persistence merely by recording a phase/result.

---

## 3. Phase activation

### 3.1 Interpreter

Interpreter is normally active for materially free-form or ambiguous gameplay input.

It may be skipped only when a registered control/input path already supplies a sufficiently typed and unambiguous intent for the downstream consumer.

### 3.2 Dramaturg

Dramaturg activates only when current play requires material latent/provisional preparation or an unresolved world-response choice not already determined by accepted state/processes.

Dramaturg work remains provisional and cannot become canon by generation.

### 3.3 Actor

Actor activates only when a material fictional subject-local decision/cognition/action is unresolved.

Each `Actor[subject]` receives a separate role rebind. Multiple Actor phases may occur in one assistant turn.

### 3.4 Chronicler

Chronicler is a **deferred-service role**, not merely optional.

Every ordinary TurnEnvelope evaluates compatible Story backlog after planning/reserving current-turn correctness and protected Narrator/output needs.

If a bounded safe service window exists, Story service is mandatory.

If the applicable Story transformation is deterministic, deterministic Story control may service the window without creating a gratuitous LLM Chronicler phase.

If editorial/generative transformation is required, the Chronicler logical role is activated.

### 3.5 Narrator

Narrator is normally the final logical player-facing gameplay phase. It receives only settled/eligible evidence and produces the supported player-facing candidate plus required disclosure intent.

### 3.6 Commentator

Commentator remains a separate mode and does not join the ordinary gameplay hot path unless its explicit mode contract is invoked.

## LAW R2.4-4 — CURRENT-TURN MATERIAL ACTIVATION

Interpreter/Dramaturg/Actor phases are conditional on current semantic need. Mere physical presence of instructions/context does not require phase execution.

## LAW R2.4-5 — CHRONICLER SERVICE OBLIGATION

Compatible Story backlog creates an outstanding service obligation evaluated on every ordinary TurnEnvelope until compatible coverage catches up.

---

## 4. Chronicler anti-starvation and priority

Story backlog remains Step-5.10-defined:

```text
current typed source-domain basis/watermark
    minus
compatible Story-layer coverage
```

R2.4 introduces no durable `StoryProjectionJob`, scheduler or worker-claim ledger.

Conceptual service decision:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

A safe service window exists only after the envelope reserves the needs of current-turn correctness/agency/mechanics, materially required Dramaturg/Actor work and protected Narrator/output capacity.

Valid deferral classes include load-critical scene formation, intense multi-participant resolution, save/publication/serialization, recovery/conflict, insufficient protected reasoning/context/output budget, or failure of Step-5.10 prerequisites for the bounded window.

## LAW R2.4-6 — FIRST SAFE OPPORTUNITY

When backlog exists and a bounded Story service window fits without violating higher-priority current-turn requirements, service is mandatory in that TurnEnvelope.

## LAW R2.4-7 — DEFER DOES NOT CANCEL

A valid deferral records/exposes a typed operational reason for the current envelope but does not create a new durable queue and does not cancel the backlog-derived obligation.

## LAW R2.4-8 — BOUNDED CATCH-UP

One service opportunity processes only a finite Step-5.10-compatible source window. Residual backlog remains for subsequent safe opportunities.

## LAW R2.4-9 — GAMEPLAY PRIORITY / OPTIONAL-WORK STARVATION BAN

Story service never preempts correctness-critical current play or protected Narrator/output capacity. Once those are reserved, serviceable backlog outranks nonessential enrichment, ornamental deliberation or optional preparation.

## LAW R2.4-10 — SERVICE DOES NOT MEAN COMMIT-EVERY-TURN

Chronicler service policy does not require one Story repository publication per gameplay turn. Step-5.10 layer-local batching, validation, coverage and publication contracts remain authoritative.

---

## 5. Role rebinding

Before each logical phase, the execution frame conceptually rebinds:

```text
role
subject/player identity where applicable
purpose/task class
registered ContextNeedProfile
RoleContextBundle identity/basis
allowed typed prior-role results
accepted deterministic result/state refs where applicable
authority limits
output/result contract
phase-local steering where permitted
```

Rebinding is correctness framing, not persona/theatrical role-play.

## LAW R2.4-11 — REBIND BEFORE PHASE

Every logical phase re-establishes role/subject/purpose/context/handoff/authority/output boundaries before using phase-local evidence.

## LAW R2.4-12 — PHYSICAL PRESENCE IS NOT PHASE ELIGIBILITY

Material physically present elsewhere in the shared chat/turn remains unusable by the active phase unless independently eligible, lawfully observed/disclosed or transferred through an admitted typed/observable handoff.

---

## 6. Minimal typed nondeterministic handoffs

Cross-phase model-produced results contain only the semantic payload required by downstream consumers.

Conceptual families include:

```text
InterpreterResult
    intent candidate / ambiguity / minimal binding cues

PreparationDraft
    bounded provisional cue/pressure/possibility

ActorProposal
    bounded subject-local action/cognition proposal or NO_CHANGE

StoryProjectionDraft
    Step-5.10-compatible bounded editorial/generative Story draft

NarrationResult
    player-facing prose candidate + material disclosure intent
```

Exact machine schemas remain R2.7/implementation work.

## LAW R2.4-13 — NO RAW PRIVATE HANDOFF

Raw role frames, complete source bundles and private unstructured reasoning do not transfer as downstream role evidence merely because the phases share physical context.

## LAW R2.4-14 — NO HIDDEN-REASONING DEPENDENCY

Chain-of-thought/private rationale is not required persistence, recovery, replay or authority evidence.

## LAW R2.4-15 — MINIMUM MODEL TRANSPORT

Model-facing structured output shall be only as large/strict as needed for the semantic boundary. Deterministic code owns serialization, schema validation, ID allocation, bookkeeping and transport envelopes.

---

## 7. Deterministic authority gateway

Material transitions follow the existing pattern:

```text
LLM interpretation/proposal
    -> deterministic validation/binding/execution
    -> accepted state/result
    -> later LLM phase may react/present from accepted result
```

The LLM cannot commit world/mechanical state merely by prose.

Chronicler cannot commit Story coverage/final IDs/publication merely by draft generation.

Narrator cannot create objective truth or disclosure state merely by prose generation before the existing validation/emission boundary.

## LAW R2.4-16 — DETERMINISTIC ACCEPTANCE GATE

Every material mechanics/state/Story-coverage/disclosure consequence remains owned by its existing deterministic/native acceptance path.

## LAW R2.4-17 — NO MECHANICS REPLAY AFTER ACCEPTANCE

Once mechanics/RNG/state transition is accepted, later Actor/Chronicler/Narrator generation failure, retry or host regeneration cannot replay the accepted mechanics or consume new RNG solely to regenerate downstream nondeterministic/presentation work.

---

## 8. Nondeterministic result lifecycle and retry

### 8.1 Before deterministic acceptance

A failed/unvalidated Interpreter/Dramaturg/Actor result may be regenerated or discarded according to the registered task contract because it has not established accepted semantic consequence.

### 8.2 After deterministic acceptance

Accepted deterministic consequences become the retry frontier. Downstream nondeterministic work regenerates from those accepted refs/state without replaying earlier accepted operations.

### 8.3 Chronicler

An unvalidated Chronicler draft may be regenerated/discarded. Story becomes progressed only through Step-5.10 deterministic publication/coverage advancement.

Story publication conflict/retry follows Step-5.10/Step-5 repository rules and does not re-execute gameplay mechanics.

### 8.4 Narrator

Narrator follows Step 5.12:

```text
private candidate
    != validated NarrationResult
    != EMISSION_COMMIT
```

Host Retry/Edit/branch does not become campaign rewind or mechanics replay.

## LAW R2.4-18 — ACCEPTED FRONTIER SURVIVES LATER GENERATION FAILURE

Retry begins from the strongest already accepted deterministic/Story publication frontier applicable to the failed downstream phase; it does not silently rewind earlier authority boundaries.

---

## 9. Instruction architecture

Semantic instruction hierarchy:

```text
HOST CONSTITUTION
    system/developer/project-level immutable host constraints

PROJECT / ENGINE CONTRACT
    Project Instructions + shipped CORE corpus

MODULE ACTIVATION
    physically present CORE -> semantically active modules

TURN ENVELOPE
    legal phases + deterministic frontier + service obligations

ROLE PHASE FRAME
    role/subject/purpose/authority/output contract

ROLE CONTEXT
    R2.3 RoleContextBundle + admitted typed handoffs

PHASE-LOCAL STEERING
    non-authoritative task/presentation emphasis
```

Existing shipped modules remain the owners of their behavioral doctrine. Role frames instantiate/narrow them; they do not restate giant role-specific prompt packs.

## LAW R2.4-19 — EXISTING CORE, SEMANTIC ACTIVATION

The full preloaded CORE corpus remains physically present under `PLAY_POLICY.md`; R2.4 uses semantic module/role activation rather than per-phase Markdown reread/removal.

## LAW R2.4-20 — LOWER INSTRUCTION LAYERS MAY NARROW, NOT OVERRIDE

Turn/role/context/steering layers may instantiate higher-level engine constraints but cannot override truth, agency, eligibility, deterministic authority or Story/disclosure laws.

## LAW R2.4-21 — PHASE-LOCAL STEERING IS NON-AUTHORITATIVE

Late task/tone/presentation steering is distinct from world evidence and engine law. Prompt position may be a quality optimization but cannot create semantic precedence.

---

## 10. Injection and role-confusion boundary

Player messages, Actor dialogue, campaign records, Story prose, tool output and retrieved external text are data/evidence under their admitted source contracts. Imperative wording inside them does not elevate them to engine instructions.

Typed prior-role results are interpreted according to their declared result contract, not as arbitrary instructions to the next phase.

## LAW R2.4-22 — DATA CANNOT SELF-PROMOTE TO ENGINE INSTRUCTION

Campaign/player/Story/tool text cannot change logical role, authority, eligibility, phase vocabulary or engine law merely by containing instruction-like prose.

## LAW R2.4-23 — ROLE SWITCHING IS ENVELOPE-BOUND

A logical role change occurs only through the registered TurnEnvelope/phase transition, not because a retrieved source or prior-role prose says to switch roles.

---

## 11. Player-visible output fencing

Only validated Narrator player-facing payload intentionally crosses the ordinary gameplay emission boundary.

Internal phase frames, Chronicler drafts, Story control/coverage metadata, ContextTrace, tool/debug payloads and operational markers remain internal.

## LAW R2.4-24 — NARRATOR-ONLY ORDINARY VISIBLE PAYLOAD

Ordinary gameplay player-visible content is produced only through the Narrator/Step-5.12 validation path.

## LAW R2.4-25 — SANITIZATION IS DEFENSE IN DEPTH

Final string cleanup may remove accidental operational markers but cannot establish secrecy/correctness. Structural role/context/output fencing is primary.

---

## 12. R2.3 `UNSATISFIABLE` integration

A phase receiving `UNSATISFIABLE` may select only a finite registered alternative appropriate to the task:

```text
use deterministic path without that LLM phase
one narrower/reframed registered need attempt
ask one genuinely blocking player clarification
use an already-defined legal degradation/omission
return typed BLOCKED / UNSUPPORTED
```

The exact allowed alternative is task/profile-owned.

## LAW R2.4-26 — FINITE UNSATISFIABLE FALLBACK

The caller cannot silently guess missing required evidence, invent a new need profile, or indefinitely re-run equivalent assembly attempts.

---

## 13. Diamond / Strong disposition for R2.4

### D16 — invisible auxiliary work

**ADOPTED WITH CURRENT-BASELINE REWRITE.**

Internal auxiliary work is represented as invisible logical phases/results inside the current turn where required. Mandatory extra calls/subagents/background workers are rejected. Chronicler is a concrete deferred-service consumer of this pattern.

### S21 — late steering

**ADOPTED.**

Phase-local steering is semantically distinct and explicitly non-authoritative. Positional prompt effects are not semantic guarantees.

### S28 — operational protocol sanitation

**ADOPTED / STRUCTURALIZED.**

Only validated Narrator output crosses the ordinary visible boundary; string stripping is defense in depth.

---

## 14. Explicit non-goals / rejected current baseline

R2.4 does not introduce:

- mandatory physical role isolation;
- one-call-per-role architecture;
- nested subagent framework;
- direct API/provider abstraction;
- generic prompt DSL;
- universal large role-result JSON envelope;
- persistent chain-of-thought store;
- Story job queue/background-worker correctness dependency;
- deterministic checkpoint FSM per logical role;
- exact host token/time thresholds;
- final prompt text or schema implementation.

---

## 15. Downstream obligations

### R2.5 — Collaboration / multiplayer

Must compose participant/recipient identity, multiple active PCs/scenes and collaborative input modes with the same TurnEnvelope, role rebinding and recipient-scoped Narrator/Context semantics without leaking cross-participant private material.

### R2.6 — ChatGPT Plus assurance

Must test/measure:

- behavioral containment under actual role/phase frames;
- long-chat/context behavior;
- latency/context pressure across ordinary/heavy turns;
- practical safe-opportunity thresholds for Chronicler service;
- Chronicler anti-starvation under repeated heavy/light turn mixtures;
- visible-surface/streaming risks;
- malformed typed result/retry rates;
- `UNSATISFIABLE` degradation behavior;
- instruction injection/role confusion;
- high reasoning working profile and supported degradation.

### R2.7 — Machine realization

Must map:

- TurnEnvelope/phase/result contracts;
- Project Instructions vs shipped CORE ownership/versioning;
- ContextNeedProfile/RoleContextBundle interfaces;
- deterministic gateway/tool bindings;
- Story service-decision representation;
- tests/evaluation fixtures;
- exact schema/catalog/runtime/file responsibilities.

No broad implementation is authorized by this candidate.
