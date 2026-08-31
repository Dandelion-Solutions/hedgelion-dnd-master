# Step 3 Architecture Task Brief — IntentPlan -> Resolution -> Signal/Event

Status: **ACTIVE ARCHITECTURE TASK BRIEF**

Target branch: `feature/mechanical-runtime-hot-state`

Roadmap owner: Step 3 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Process: `DEV/DESIGN_PROCESS.md` plus `DEV/ARCHITECTURE/DESIGN_PROCESS.md`.

Step 2 is closed. This Step 3 task must preserve its state-authority, pinned-view,
prospective-DAG, temporal, Condition, Effect, and Resource invariants.

## 1. Classification

**Architectural / Deep-Work.**

This stage fixes the execution boundary shared by natural-language intent,
Activities, deterministic domain transitions, reactions/choices, prospective
state, atomic commits, Events, retries, and recoverable suspended work. Mistakes
here would propagate into durability, multiplayer, LLM integration, and every
mechanical subsystem.

## 2. Problem statement

HDM already has several individually useful concepts:

```text
player message
Intent / IntentClause
IntentPlan
RuntimeCommand
ActionRequest
DomainTransitionRequest
Activity
Resolution
Signal
Contribution
StateDelta / prospective plans
MechanicalEvent
ResolutionTrace
Continuation
Checkpoint
```

The open problem is their **authority/lifetime composition**.

Step 3 must define one coherent deterministic execution protocol such that:

- the LLM can interpret informal player language without becoming mechanical
  authority;
- one message can contain multiple material intents without becoming one giant
  transaction;
- a rules-defined Activity can suspend for choice/reaction and resume without
  repeating rolls or committed mutations;
- deterministic transitions do not require fake Activities but also do not
  create a second transaction/event/idempotency engine;
- every mutable segment observes a pinned Step-2 state view and validates its
  prospective dependency graph before commit;
- committed facts are distinguishable from transient Signals and uncommitted
  plans;
- retry, crash, another chat/environment, and repository restore cannot duplicate
  an already committed consequence or lose a pending mandatory consequence.

## 3. Verified repository facts

### FACT — IntentPlan already exists as the one-message orchestration concept

`CATALOG_INVENTORY.md` defines `runtime.intent_plan` as ordered material clauses
from one player input, and `ACTIVITY_MODEL.md` says one player message may
contain several intents. Normal execution is sequential and is not globally
atomic; earlier committed intents survive a later failure.

### FACT — Resolution currently means one Activity invocation

`CATALOG_INVENTORY.md`, `ACTIVITY_MODEL.md`, and
`MECHANICAL_RUNTIME_PROPOSAL.md` consistently use `runtime.resolution` for one
Activity invocation. `activity.composite` is reserved for reusable rules-defined
composition rather than ad-hoc wrapping of one player message.

### FACT — deterministic domain transitions are a distinct upper path

Existing architecture distinguishes already-adjudicated deterministic
`DomainTransitionRequest` from Activity-backed `ActionRequest`. A transition is
a fixed tagged union, not JSON Patch, and should not require invented dice or a
fake Activity.

### FACT — Activity execution is bounded and data-driven

Activities use finite ordered typed steps, bounded branches/target iteration,
registered primitives, prior typed results, and explicit choice/reaction
suspension. They do not contain arbitrary code, world queries, or unbounded
loops.

### FACT — Signals are transient and Events are committed facts

The existing proposal distinguishes a pre-commit/transient Signal from an
immutable MechanicalEvent emitted only after an atomic mutation segment commits.
TriggerBindings may react before commit or schedule child work after a committed
Event.

### FACT — SQLite transactions cannot span dialogue turns

Existing design already requires a suspended Resolution to serialize enough
continuation state to close the transaction. Fixed rolls must survive resume;
committed effects must never be replayed.

### FACT — current runtime-record vocabulary already includes the relevant owners

The catalog currently registers at least:

```text
runtime.interaction
runtime.intent_plan
runtime.command
runtime.resolution
runtime.continuation
runtime.mechanical_event
runtime.resolution_trace
runtime.checkpoint
```

and protocol values for runtime/action/transition requests, intent clauses,
Signals, StateDeltas, choices/reactions, and receipts.

### FACT — existing campaign checkpoint is only compact canonical recovery metadata

`GAME/SCHEMA/checkpoint.schema.yaml` records canonical recovery roots/frontiers,
not a copy of all world state and not enough today to preserve an arbitrary
suspended mechanical Resolution. Step 3 must therefore define the portable
in-flight execution payload; Step 5 later owns repository publication/
restoration policy for that payload.

## 4. Step-2 constraints inherited by Step 3

Step 3 must not violate:

1. one `MechanicalContext` reads one pinned committed/prospective state view;
2. prospective changes that extend mechanical dependencies validate the scoped
   concrete DAG before commit;
3. HP, LifeState, Resource, Effect, Condition, and TemporalBinding authorities
   remain with their Step-2 owners;
4. Temporal Agenda and reverse indexes are rebuildable projections;
5. declarative content has no runtime domain-query capability;
6. engine-owned mechanical facts cannot be asserted by the LLM;
7. no fixed-point/evaluation-order semantics resolve mechanical cycles;
8. a boundary producer and state-owner responders are distinct responsibilities;
9. no SQLite transaction remains open across an external choice/reaction/chat
   boundary.

## 5. Required quality attributes

### Correctness / determinism

- same accepted request + same pinned inputs + same fixed random/choice results
  yields the same prospective/committed mechanical result;
- no committed consequence executes twice because a host/tool call was retried;
- no continuation combines unrelated revisions silently;
- pre-commit reactions may change a pending result; post-commit child work may
  add later facts but never rewrite the triggering committed fact.

### Recoverability

- a suspended Resolution has a portable, versioned continuation contract;
- fixed rolls, explicit choices already made, causal child receipts, execution
  cursor, and dependency frontier survive process loss when checkpointed;
- derived caches/prospective deltas need not be trusted as authority after
  restore; they can be recomputed from the continuation's authoritative inputs;
- pending mandatory trigger/reaction obligations are not lost merely because
  SQLite or one chat disappears.

### Isolation

- LLM semantic interpretation and deterministic execution remain distinct;
- IntentPlan orchestration is distinct from one Activity Resolution;
- Activity and deterministic TransitionRequest remain distinct upper paths;
- both upper paths share one lower commit/event/idempotency primitive;
- Signal/BoundaryOccurrence/Event identities cannot become duplicate authorities
  for the same committed edge.

### Performance

- normal single-intent/no-reaction execution stays local and bounded;
- no campaign-global scan/rebuild per action;
- continuation/checkpoint state is proportional to active/suspended execution,
  not total campaign history;
- ordinary retries return stored receipts rather than recomputing the world.

### Testability / observability

Every committed segment must have enough stable identity/provenance to test and
trace:

```text
request / plan / clause
execution owner
segment
state view(s)
fixed random/choice inputs
candidate/applied deltas
events
continuation transition
idempotency outcome
```

## 6. Explicit non-goals

Step 3 does **not** own:

- durable lore/knowledge/secrets model or full LLM context-selection policy
  (Step 4);
- Git SOFT/HARD publication mechanics, multiplayer merge/reconciliation, or
  cross-scene durability policy (Step 5);
- full D&D seed/migration/catalog-gap completion (Step 6);
- a general workflow programming language;
- arbitrary compensation/rollback after already committed game consequences;
- background wall-clock execution;
- a second event-sourced world authority replacing canonical state.

## 7. Architecture decisions Step 3 must make

### D1 — IntentPlan versus Resolution ownership

Decide whether one message-level IntentPlan owns several independently executable
clauses/Resolutions or whether one Resolution swallows the whole plan.

Current evidence favors keeping them separate.

### D2 — shared lower execution primitive

ActionRequest and DomainTransitionRequest need one common deterministic lower
path for:

```text
preflight
prospective state
validation
atomic commit
MechanicalEvents
trace
idempotency
receipt
```

without forcing transitions to become Activities.

### D3 — atomic MutationSegment authority

Define the smallest indivisible commit unit and which artifacts advance
atomically with it: state records, Event batch, trace, RNG state, dirty state,
idempotency record, continuation state, and any procedure-local ResourceState.

### D4 — Signal / BoundaryOccurrence / Event authority

Define which object represents:

- a candidate/pre-commit timing edge;
- a reached boundary context used by state-owner responders;
- an immutable fact after producer/response mutation commits.

Do not create three durable authorities for one occurrence.

### D5 — suspension and continuation

Define what is authoritative while a Resolution is paused, what may be safely
recomputed, how child reactions advance the parent's dependency frontier, and
how stale/invalid continuations fail.

### D6 — idempotency hierarchy

Define stable request/plan/clause/execution/segment/Event/continuation identities,
input fingerprints, retry behavior, and stale resume behavior.

### D7 — trigger/reaction ordering and chain bounds

Define deterministic collection/order/adjudication of multiple pre-commit and
post-commit triggers without arbitrary list/SQL order or unbounded recursive
execution.

### D8 — LLM-to-core typed binding

Define how the LLM maps phrases such as `эта хреновина` / `жахну того придурка`
to candidate entity/Activity references, how bounded catalog/state lookup is
supplied, what the deterministic binder verifies, and when ambiguity produces a
clarification instead of a guess.

The architecture must not require the LLM to hold the complete catalog in
working memory.

### D9 — portable in-flight checkpoint payload

Define which Resolution/Continuation data is continuity-critical and portable.
Step 3 owns the payload/restore semantics; Step 5 owns repository durability and
publication/cleanup policy.

## 8. Research questions

1. Can `runtime.command` serve as the common idempotent invocation envelope for
   both ActionRequest and TransitionRequest while preserving distinct execution
   semantics?
2. Should the common lower atomic owner be called `MutationSegment`,
   `CommitSegment`, or another term, and does it need an independent runtime
   record or only stable identity inside execution/Event/trace records?
3. How should a parent Resolution resume after a reaction child legitimately
   changes state: fail stale, rebase, or recompute from an explicit safe phase?
4. Which fixed values survive suspension (raw rolls, choices, selected targets,
   resolved references) and which derived values must be recomputed?
5. Does a committed boundary need a dedicated MechanicalEvent kind, or should
   its identity be represented by the producer transition Event plus occurrence
   metadata/causal links?
6. What is the smallest IntentClause dependency vocabulary needed for natural
   `first X, then Y / if X succeeds, Y` without turning IntentPlan into an
   Activity/workflow DSL?
7. Which trigger-ordering cases are mechanically commutative, which have a
   registered ordering rule, and which must produce typed adjudication?
8. What portable continuation data is sufficient to restore a suspended chain
   without serializing SQLite or trusting stale prospective deltas?

## 9. Analytical challenge requirements

Before presenting a recommendation, explicitly attack at least these tempting
simplifications:

- one giant Resolution per player message;
- make every deterministic transition a fake Activity;
- separate event/transaction/idempotency engines for actions and transitions;
- persist the whole prospective delta and blindly continue after a reaction;
- treat any revision change as stale, even when caused by the expected child
  reaction;
- use arbitrary stable sorting for mechanically non-commutative simultaneous
  triggers;
- let the LLM choose unchecked IDs because it saw them in prompt context;
- make checkpointing a SQLite snapshot or rely on event replay from campaign
  beginning;
- add a generic workflow/DAG language before real rules prove one is necessary.

## 10. Done criteria for the Step-3 design

The Step-3 candidate architecture is decision-ready when it contains:

- one authority/lifetime diagram for Interaction/IntentPlan/Clause/Command/
  Resolution/Transition/Segment/Signal/Event/Continuation/Trace/Receipt;
- exact committed versus transient versus checkpointable classifications;
- request and resume idempotency contract;
- prospective-view and reaction-resume semantics;
- trigger ordering/chain rules;
- typed LLM binding/discovery boundary;
- portable continuation/checkpoint payload contract;
- focused mini-cases covering ordinary attack, Counterspell-like precommit
  reaction, post-damage follow-up, multiple intents with partial completion,
  deterministic item/currency/location transition, ambiguous natural-language
  target, retry after committed segment, crash while suspended, and a boundary
  with multiple state-owner responders;
- cross-impact notes for Steps 4/5;
- adversarial review with no unresolved Step-3 blocker.

No runtime implementation begins before this architecture gate closes.
