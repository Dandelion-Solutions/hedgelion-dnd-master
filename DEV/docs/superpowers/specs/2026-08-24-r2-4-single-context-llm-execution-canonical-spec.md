# R2.4 Canonical Specification — Single-Context Turn Envelope, Typed Role Gateways and Chronicler Service

Status: **CANONICAL — R2.4 ARCHITECTURE CLOSED SUBJECT TO RESOLUTION GATE**

Date: 2026-08-24

Canonicalization basis:

- R2.4 task brief;
- R2.4 evidence ledger;
- Chronicler service owner clarification and evidence addendum;
- Decision Brief v2;
- owner-approved Alternative B;
- candidate specification;
- adversarial review AR-1..AR-8.

Owner-approved architecture:

> **REGISTERED TURN ENVELOPE + MINIMAL TYPED GATEWAYS + FIRST-SAFE-OPPORTUNITY CHRONICLER SERVICE**

This specification defines logical single-context LLM execution and instruction architecture. It does not implement prompt text, schemas, tool APIs, exact ChatGPT budgets, buffering or provider abstraction.

---

## 1. Central invariant

Ordinary HDM gameplay uses:

```text
one user request
one assistant turn
one physical conversational context
```

while preserving explicit logical role phases and deterministic authority boundaries.

Conceptually:

```text
TurnEnvelope
    -> Interpreter?                 conditional
    -> deterministic bind/context
    -> Dramaturg?                  conditional
    -> Actor[subject]?             zero or more, separately rebound
    -> deterministic execution as required
    -> envelope-level Story backlog/service checkpoint
         -> NO_BACKLOG
         -> SERVICE(bounded window)
         -> DEFER(typed reason)
    -> Narrator                    fresh rebind / protected visible phase
    -> NarrationResult validation
    -> EMISSION_COMMIT
```

The Story service checkpoint is envelope-level: it is evaluated even when the turn contains no material deterministic mechanics/state transition.

## LAW R2.4-1 — TURN ENVELOPE, NOT ROLE=CALL

Logical role phase does not imply separate model call, agent, process or chat.

---

## 2. TurnEnvelope

`TurnEnvelope` is transient bounded control state for one assistant turn. It may bind:

```text
request/turn identity where required
current accepted deterministic frontier
legal phase vocabulary/order constraints
current role/subject/purpose binding
registered ContextNeedProfile / RoleContextBundle identities
allowed typed prior results
finite fallback/terminal classes
protected Narrator/output reservation
Story service-opportunity result
```

It does not own semantic world state, cognition, Story coverage, disclosure or mechanics.

## LAW R2.4-2 — REGISTERED PHASE VOCABULARY

Only registered phase/result families participate in ordinary execution. Model suggestion cannot invent an authority-bearing phase.

## LAW R2.4-3 — ENVELOPE IS CONTROL, NOT AUTHORITY

TurnEnvelope routing/control state cannot establish semantic truth or persistence.

---

## 3. Role activation

### Interpreter

Normally active for materially free-form or ambiguous gameplay input; skippable only when a registered path already provides sufficient typed unambiguous intent.

### Dramaturg

Conditional on material latent/provisional preparation or unresolved world-response work not already determined by accepted owners/processes.

### Actor

Zero or more subject-local phases. Each material Actor decision receives a separate logical rebind.

### Chronicler

Deferred-service role. Every ordinary TurnEnvelope evaluates compatible Story backlog and service opportunity.

### Narrator

Normally final ordinary player-facing logical phase. Protected output capacity is reserved before Story service can consume spare capacity.

### Commentator

Separate mode, not ordinary gameplay hot path absent its explicit mode contract.

## LAW R2.4-4 — CURRENT-TURN MATERIAL ACTIVATION

Interpreter/Dramaturg/Actor execute only when their semantic work is material.

## LAW R2.4-5 — CHRONICLER SERVICE OBLIGATION

Compatible Story backlog creates an outstanding service obligation evaluated on every ordinary TurnEnvelope until compatible coverage catches up.

---

## 4. Chronicler first-safe-opportunity policy

Backlog remains Step-5.10-defined:

```text
current typed source-domain basis/watermark
    -
compatible Story-layer coverage
```

Service decision:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

The backlog check uses compact typed coverage/source-basis metadata. It shall not require an unbounded Story/history scan merely to decide whether service is owed.

A safe service window exists only after reserving current-turn correctness/agency/mechanics, materially required Dramaturg/Actor work and protected Narrator/output capacity.

## LAW R2.4-6 — FIRST SAFE OPPORTUNITY

If compatible backlog exists and a bounded Step-5.10-compatible window fits within the remaining safe envelope, Story service is mandatory.

## LAW R2.4-7 — DEFER DOES NOT CANCEL

Load-critical scene construction, intense multi-participant play, save/publication/serialization, recovery/conflict, insufficient protected budget or unavailable Step-5.10 prerequisites may defer service for the current envelope. The backlog-derived obligation remains.

`DEFER(reason)` is turn-local control/diagnostic evidence unless an existing diagnostic owner independently retains it; it is not a durable scheduler state.

## LAW R2.4-8 — BOUNDED CATCH-UP

One opportunity processes a finite uncovered source window. Residual backlog remains for later safe opportunities.

## LAW R2.4-9 — GAMEPLAY PRIORITY / OPTIONAL-WORK STARVATION BAN

Story never preempts correctness-critical current play or protected Narrator/output capacity. Once those are reserved, serviceable backlog outranks nonessential enrichment, ornamental deliberation and optional preparation.

## LAW R2.4-10 — NO STORY SCHEDULER / NO COMMIT-EVERY-TURN

No durable Story job queue, worker-claim ledger, background-worker correctness dependency, fixed every-N-turn SLA or Story Git commit after every gameplay turn is introduced.

---

## 5. Chronicler source and feedback boundaries

Chronicler may process/publish only candidates admitted by the applicable Step-5.10 `StoryProjectionSourceContract` at a compatible source basis.

Physical presence in HOT/shared context does not by itself make unpublished material eligible for durable Story publication.

If source durability/admission is a prerequisite, Story waits or participates only through an already-authorized coherent owner publication contract.

## LAW R2.4-11 — STORY MAY NOT DURABLY OUTRUN ITS ADMITTED SOURCE BASIS

Durable Story output/coverage cannot be advanced from material that has not satisfied the owning Step-5.10 source-domain admission/basis contract.

## LAW R2.4-12 — NO SAME-ENVELOPE STORY FEEDBACK

Story created or changed by Chronicler service in the current TurnEnvelope is not admitted as a new gameplay-role input in that same TurnEnvelope.

Later Interpreter/Dramaturg/Actor/Narrator phases use independently assembled eligible sources and typed handoffs. Newly published Story becomes ordinary gameplay orientation/retrieval input only in a later eligible assembly cycle, except explicit separate maintenance/Commentator mode contracts.

## LAW R2.4-13 — STORY CONTENTION YIELDS TO CURRENT RESPONSE

Story publication conflict/retry obeys Step-5.10 gameplay-priority/yield semantics. Once protected Narrator/output capacity would be threatened, Story service terminates/defer for the current envelope rather than blocking visible response completion.

---

## 6. Role rebinding

Before each phase, conceptually bind:

```text
role
subject/player identity where applicable
purpose/task class
registered ContextNeedProfile
RoleContextBundle identity/basis
allowed typed prior results
accepted deterministic refs where applicable
authority limits
output/result contract
phase-local steering where allowed
```

## LAW R2.4-14 — REBIND BEFORE PHASE

Every logical phase re-establishes role/subject/purpose/context/handoff/authority/output boundaries before using phase-local evidence.

## LAW R2.4-15 — FRESH NARRATOR REBIND AFTER CHRONICLER

Whenever Chronicler/Story service executes before Narrator, Narrator performs a fresh explicit logical rebind afterward. Chronicler source bundles/drafts are not reused as Narrator evidence.

## LAW R2.4-16 — PHYSICAL PRESENCE IS NOT LOGICAL ELIGIBILITY

Shared physical context never grants source eligibility to a role.

---

## 7. Minimal typed handoffs

Conceptual result families:

```text
InterpreterResult
PreparationDraft
ActorProposal | NO_CHANGE
StoryProjectionDraft
NarrationResult
```

Only minimum semantic payload required downstream crosses a phase boundary. Exact schemas remain R2.7/implementation work.

## LAW R2.4-17 — NO RAW PRIVATE HANDOFF

Raw role frames, complete private source bundles and unstructured private reasoning are not downstream evidence merely because they remain physically present.

## LAW R2.4-18 — NO HIDDEN-REASONING DEPENDENCY

Chain-of-thought/private rationale is not required persistence, recovery, replay or authority evidence.

## LAW R2.4-19 — MINIMUM MODEL TRANSPORT

Deterministic code owns serialization, schema validation, final IDs and bookkeeping. Model-facing structured payloads stay minimal to the semantic boundary.

---

## 8. Deterministic authority and retry

Material transition pattern:

```text
LLM interpretation/proposal
    -> deterministic validation/binding/execution
    -> accepted result/state
    -> downstream phase
```

Chronicler never owns final Story IDs, coverage advancement, repository publication or canon promotion.

Narrator follows Step-5.12 validation and emission semantics.

## LAW R2.4-20 — DETERMINISTIC ACCEPTANCE GATE

Mechanics/state/Story-coverage/disclosure consequences remain with their native deterministic/semantic owners.

## LAW R2.4-21 — NO MECHANICS REPLAY AFTER ACCEPTANCE

Later LLM/Story/presentation failure cannot replay accepted mechanics/RNG solely to regenerate downstream work.

## LAW R2.4-22 — ACCEPTED FRONTIER SURVIVES LATER GENERATION FAILURE

Retry starts from the strongest applicable already accepted frontier, not an implicit rewind of prior accepted work.

Unaccepted LLM drafts may be regenerated/discarded. Story progress exists only after Step-5.10 deterministic publication/coverage advancement. Narrator delivery remains Step-5.12-owned.

---

## 9. Instruction architecture

Semantic hierarchy:

```text
HOST CONSTITUTION
    system/developer/project host constraints

PROJECT / ENGINE CONTRACT
    Project Instructions + shipped CORE corpus

MODULE ACTIVATION
    present CORE -> active modules for current situation

TURN ENVELOPE
    legal phases + service obligations + deterministic frontier

ROLE PHASE FRAME
    role / subject / purpose / authority / output

ROLE CONTEXT
    R2.3 RoleContextBundle + admitted typed handoffs

PHASE-LOCAL STEERING
    non-authoritative task/presentation emphasis
```

Existing shipped modules remain owners of their behavior doctrine; role frames instantiate/narrow rather than duplicate giant role prompts.

## LAW R2.4-23 — EXISTING CORE, SEMANTIC ACTIVATION

Full preloaded CORE remains physically present under `PLAY_POLICY.md`; activation/rebinding is semantic rather than per-phase file reread/removal.

## LAW R2.4-24 — LOWER LAYERS MAY NARROW, NOT OVERRIDE

Turn/role/context/steering layers cannot override higher truth, agency, eligibility, deterministic authority or Story/disclosure law.

## LAW R2.4-25 — PHASE-LOCAL STEERING IS NON-AUTHORITATIVE

Late steering is distinct from evidence and engine law. Prompt position may optimize behavior but grants no semantic precedence.

---

## 10. Injection / role confusion

Player text, campaign records, Story prose, Actor dialogue, tool output and retrieved text are data/evidence under their source contracts.

## LAW R2.4-26 — DATA CANNOT SELF-PROMOTE TO ENGINE INSTRUCTION

Instruction-like prose inside data cannot change role, authority, eligibility, phase vocabulary or engine law.

## LAW R2.4-27 — ROLE SWITCHING IS ENVELOPE-BOUND

Role transition occurs only through the registered TurnEnvelope phase transition, not because source/prior-role prose requests a switch.

---

## 11. Visible output fencing

Only validated Narrator player-facing payload intentionally crosses ordinary gameplay `EMISSION_COMMIT`.

Internal role frames, Chronicler drafts, Story control metadata, ContextTrace and tool/debug payloads remain internal.

## LAW R2.4-28 — NARRATOR-ONLY ORDINARY VISIBLE PAYLOAD

Ordinary gameplay visible content uses the Narrator/Step-5.12 path.

## LAW R2.4-29 — SANITIZATION IS DEFENSE IN DEPTH

String cleanup cannot replace structural role/context/output fencing.

---

## 12. R2.3 `UNSATISFIABLE`

Registered finite alternatives may include:

```text
deterministic path without failed LLM phase
one narrower registered need/profile attempt
one genuinely blocking player clarification
registered legal degradation/omission
typed BLOCKED / UNSUPPORTED
```

## LAW R2.4-30 — FINITE UNSATISFIABLE FALLBACK

No silent guessing, new ad-hoc need profile or unbounded reassembly loop.

---

## 13. Diamond / Strong disposition

### D16 — invisible auxiliary generation/work

**ADOPTED WITH CURRENT-BASELINE REWRITE.** Invisible logical internal phases/results are admitted; mandatory extra model calls/subagents/background workers are rejected. Chronicler deferred-service work is a concrete consumer.

### S21 — late steering

**ADOPTED.** Phase-local steering is semantically separate and non-authoritative; position is not authority.

### S28 — operational protocol sanitation

**ADOPTED / STRUCTURALIZED.** Internal protocol remains behind structural output fencing; string sanitation is defense in depth.

---

## 14. Non-goals / rejected current baseline

No mandatory physical isolation, one-call-per-role architecture, nested subagent framework, direct API/provider abstraction, generic prompt DSL, large universal role-result envelope, persistent chain-of-thought, Story scheduler/background worker, per-role deterministic checkpoint FSM, exact host timing/token thresholds or final prompt/schema implementation is introduced.

---

## 15. Downstream obligations

### R2.5

Compose collaborative/multiplayer input and recipient identity with the same TurnEnvelope/rebinding/context laws without cross-participant leakage or accidental PC takeover.

### R2.6

Validate actual ChatGPT Plus supported envelope, including:

- role containment under production-like phase frames;
- **Chronicler -> Narrator containment** with hidden historical material and lawful positive controls;
- no same-envelope Story feedback;
- long-chat behavior;
- latency/context pressure;
- safe-opportunity classification and anti-starvation across heavy/light turn mixtures;
- Story contention/yield behavior;
- visible surface/streaming risks;
- malformed result/retry behavior;
- instruction injection/role confusion;
- `UNSATISFIABLE` degradation;
- reasoning-profile behavior.

### R2.7

Map TurnEnvelope, phase/result contracts, Project Instructions vs CORE ownership/versioning, deterministic gateways, Story service decision, tests/evaluation and exact schema/catalog/runtime realization.

No broad implementation is authorized by this specification.
