# Step 3 Research Draft — Deterministic Execution Boundary

Status: **RESEARCH / ARCHITECTURE DRAFT — HUMAN DECISION REQUIRED BEFORE CANDIDATE SPEC**

Target branch: `feature/mechanical-runtime-hot-state`

Task Brief: `DEV/docs/superpowers/design/2026-08-19-step-3-execution-boundary-task-brief.md`

This draft explores the authority/lifetime model for Step 3. It is not yet a
canonical specification and does not authorize implementation.

## 1. Research synthesis

The repository already contains the right conceptual separation in fragments:

- one Interaction/player input can contain several material intents;
- `IntentPlan` is ordered message-level orchestration and is not globally atomic;
- one Activity invocation is a `Resolution`;
- an already-adjudicated deterministic `TransitionRequest` is not an Activity;
- Activity execution is bounded and may suspend for choice/reaction;
- Signals are transient/pre-commit and MechanicalEvents are post-commit facts;
- a SQLite transaction cannot remain open across a dialogue/suspension boundary;
- fixed random results and already committed mutations must survive resume;
- Step 2 now requires pinned state views, prospective DAG validation, and
  recoverable continuity-critical runtime state.

The missing architecture is therefore **not another mechanics language**. It is
one execution protocol connecting these already-separated responsibilities.

## 2. External sanity checks

Primary technical references support two relevant constraints without dictating
HDM's design:

1. SQLite transactions provide an atomic commit/rollback boundary and do not
   provide a durable cross-process conversational continuation by themselves.
   HDM should therefore make local execution segments explicit rather than treat
   one player interaction as one long transaction.
2. Event interoperability specifications such as CloudEvents distinguish one
   occurrence from one or more emitted event records and require stable event
   identity suitable for duplicate detection. HDM need not adopt CloudEvents,
   but should likewise give committed MechanicalEvents stable producer-scoped
   identity rather than infer duplication from payload equality or timestamps.

HDM deliberately does **not** adopt a full event-replay workflow model as its
world-state authority. Current authoritative state remains authoritative; Events
and traces provide causal/audit/idempotency history.

## 3. Architectural alternatives

### Alternative A — one giant Resolution per IntentPlan

```text
Interaction
  -> IntentPlan
      -> one Resolution containing every clause
```

Advantages:

- one obvious root execution object;
- one place to store overall status;
- straightforward single receipt correlation.

Failure modes:

- turns message-level interpretation into a mechanical procedure;
- makes partial completion and clause-local retry/suspension harder to isolate;
- pressures deterministic transitions and narrative-only clauses into Activity
  semantics;
- makes one clause's reaction/choice lifecycle contaminate unrelated later
  clauses;
- encourages accidental global atomicity or compensation semantics.

**Rejected.** It collapses two existing responsibilities that the repository has
already correctly separated.

### Alternative B — every executable clause becomes an Activity Resolution

```text
IntentPlan clause
  -> synthesize/find Activity
      -> Resolution
```

Advantages:

- one apparent execution path;
- existing Activity machinery handles steps, Events, trace, and suspension.

Failure modes:

- deterministic location/item/currency/domain transitions need fake Activities;
- an already-adjudicated exact state transition acquires unnecessary procedure
  semantics;
- catalog grows wrapper Activities whose only purpose is transaction plumbing;
- transition validation and Activity validation become artificially entangled.

**Rejected.** This is architectural uniformity purchased by semantic dishonesty.

### Alternative C — separate upper paths, one shared lower execution kernel

```text
Interaction
  -> IntentPlan
      -> executable IntentClause
          -> RuntimeCommand
              -> ActionRequest -> Resolution(Activity)
              OR
              -> TransitionRequest -> direct deterministic execution

Both
  -> shared ExecutionSegment kernel
      -> prospective state / validation
      -> atomic local commit
      -> MechanicalEvent batch
      -> trace / idempotency / receipt
      -> optional Continuation transition
```

Advantages:

- preserves the existing meaning of IntentPlan, Activity, Resolution, and
  TransitionRequest;
- actions and transitions share exactly one mutation/event/idempotency path;
- simple deterministic transitions stay simple;
- reactions/choices remain Resolution capabilities rather than becoming generic
  transition features;
- partial completion and retries are naturally clause-local;
- creates one place to integrate Step-2 pinned views/DAG validation and runtime
  continuity.

Costs:

- `runtime.command` and the shared lower segment protocol need explicit
  lifecycle contracts;
- the receipt model must aggregate command-level and Resolution-level details
  without duplicate authority.

**RECOMMENDED.**

## 4. Recommended authority/lifetime graph

```text
Interaction
  raw user input + host invocation identity
        |
        v
LLM Interpretation / Reference Adjudication
  non-authoritative semantic mapping
        |
        v
IntentPlan
  ordered material clauses for ONE Interaction
  NOT a transaction
        |
        +---- IntentClause 1
        |       |
        |       v
        |    RuntimeCommand
        |       |
        |       +-- ActionRequest ---> Resolution(Activity)
        |       |                         |
        |       |                         +-- ExecutionSegment(s)
        |       |                         +-- Continuation if suspended
        |       |                         +-- child Resolution(s)
        |       |
        |       +-- TransitionRequest ---> ExecutionSegment
        |
        +---- IntentClause 2 -> fresh validation against post-clause-1 state
        |
        +---- ...

ExecutionSegment
  -> pinned committed/prospective views
  -> scoped DAG validation
  -> one atomic SQLite/HOT transaction
  -> state/procedure/runtime deltas
  -> MechanicalEvent batch
  -> trace + RNG frontier + idempotency state
  -> segment receipt

IntentPlanReceipt
  -> ordered references to clause/command receipts
```

## 5. Interaction and IntentPlan

### Interaction

`runtime.interaction` is the host/player exchange boundary. It owns:

- raw player input;
- stable invocation identity used to distinguish transport retry from a later
  intentional repetition of the same text;
- player/session/campaign context references;
- resulting IntentPlan and final compact response references.

It is not a mechanical transaction or state owner.

### IntentPlan

`runtime.intent_plan` owns the normalized ordered material clauses extracted
from one Interaction.

It does **not** own:

- world mutations;
- RNG state;
- reactions/choices;
- MechanicalEvents;
- a SQLite transaction.

Default semantics are sequential:

```text
clause N executes against state after every committed prior clause
```

Earlier committed clauses remain committed if a later clause fails.

A later clause can become `skipped_due_to_prior_result` or fail fresh validation
without compensating earlier game consequences.

### Bounded conditional intent

IntentPlan must support natural phrases such as:

```text
open the door, and if it opens, go through
```

without becoming a workflow language.

Recommended initial rule:

- clauses are a finite ordered list;
- a clause may have a forward-only guard over a **registered typed export/status
  from an earlier clause receipt**;
- no loops, backward edges, arbitrary expressions, dynamic clause generation, or
  user-authored scripts;
- complex reusable rules-defined sequencing belongs in `activity.composite`.

Exact export vocabulary is machine-spec work after the ownership decision.

## 6. LLM -> deterministic-core binding

The LLM should be treated as a semantic interpretation/adjudication coprocessor,
not as a catalog/state authority.

Recommended pipeline:

```text
player prose
   |
   v
LLM IntentDraft
   mention spans / intended outcome / approach / semantic hints
   unresolved or candidate references
   fiction-only adjudicated facts where permitted
   |
   v
bounded discovery/hydration
   engine returns relevant entity/catalog/Activity candidates
   |
   v
LLM semantic selection among bounded candidates
   |
   v
Deterministic Binder
   verifies IDs, entity kinds, visibility/authority, Activity contracts,
   target/source compatibility, engine-owned facts, and request schema
   |
   +-- unique valid binding -> RuntimeCommand
   +-- material ambiguity -> ClarificationRequest
   +-- missing capability -> unsupported/catalog-gap path
```

The LLM may decide that the phrase `тот придурок` refers to one of the
engine-supplied visible candidates because linguistic reference is not a
mechanical calculation. It may not invent an unchecked entity ID, claim that the
candidate is mechanically targetable when the engine can check that fact, or
assert HP/Condition/Resource state.

The discovery interface is an execution-host capability, not a Rule Element /
Activity query DSL. It may use bounded catalog/entity search internally and must
respect knowledge/visibility policy.

This avoids requiring the model to memorize the whole catalog and avoids putting
full campaign state into context.

## 7. RuntimeCommand as common idempotent invocation envelope

`runtime.command` is the common accepted execution request for one executable
IntentClause.

Conceptually it owns:

```text
command_id
interaction_id
intent_plan_id
clause_id
command_kind = action | transition
normalized typed payload
binding/adjudication provenance
input_fingerprint
status
stored terminal/suspended receipt reference
```

A command ID is stable across a transport retry. Reusing the same ID with a
different normalized input is an `IDEMPOTENCY_CONFLICT`, not a second execution.

### Action command

Owns an `ActionRequest` and creates/links one `Resolution` for one Activity
invocation.

### Transition command

Owns one already-adjudicated typed `TransitionRequest` and uses the common
ExecutionSegment kernel directly. It cannot suspend for a mechanical choice or
reaction; if such interaction is required, the request was not actually a
simple deterministic transition and must be represented through the appropriate
Activity/adjudication path.

## 8. Resolution

Keep the existing meaning:

> one invocation of one Activity with concrete bindings.

A Resolution owns:

```text
resolution_id
command_id
activity_id + definition/version identity
actor/source/target bindings
accepted invocation facts + provenance
status
execution cursor / step path
fixed RNG results already generated
typed prior-step exports
child Resolution links
next segment sequence
current suspension reference
trace reference
```

A Resolution may produce zero, one, or several committed ExecutionSegments.

It may suspend for a genuine external choice/reaction. The same Resolution
identity survives suspension/resume; a new parent Resolution is not created for
the resume.

## 9. ExecutionSegment — common lower atomic unit

Use **ExecutionSegment** rather than `MutationSegment` or `CommitSegment`:

- `MutationSegment` is too narrow because a suspension/checkpoint transaction may
  update only runtime execution state;
- `CommitSegment` is confusing in a repository whose durable publication uses
  Git commits;
- `ExecutionSegment` describes the actual responsibility: the smallest local
  atomic execution persistence boundary.

An ExecutionSegment has stable identity scoped to its command/execution, for
example conceptually:

```text
segment_id = command_id + segment_sequence
```

One committed segment transaction may atomically advance:

```text
world authoritative records
procedure-local runtime state
Resolution / RuntimeCommand state
RNG frontier
Continuation creation/consumption
MechanicalEvent batch
ResolutionTrace / segment receipt
idempotency markers
dirty/publication bookkeeping
```

Not every segment must mutate the world. Persisting a suspension with fixed RNG
results and a Continuation is still a legitimate atomic execution-state segment.

A segment is never a campaign world entity.

## 10. Prospective state and Step-2 DAG validation

For a mutating segment:

```text
pinned committed view
   -> prospective overlay
   -> calculations / Signals / state-owner plans
   -> scoped dependency DAG extension/validation
   -> constraint/authority validation
   -> atomic segment commit
   -> new committed view
```

No MechanicalEvent is emitted for an uncommitted candidate result.

A segment that fails validation leaves no partial authoritative mutation.

## 11. Signals, BoundaryOccurrences, and MechanicalEvents

### Signal

A Signal is transient typed pre-commit or timing context inside an execution.
It may collect passive mechanics, automatic triggers, or open a reaction window.
It is not durable truth.

If execution suspends, the Continuation stores the normalized pending
choice/reaction contract and origin/firing identity needed for resume; it need
not preserve a generic Signal object as a new authority.

### BoundaryOccurrence

A BoundaryOccurrence is a typed specialized execution context produced when a
registered boundary is prospectively reached.

It identifies:

```text
boundary kind
producer
scope/subject
causal execution position
occurrence identity/key
```

Mandatory synchronous responders can be resolved in the producer's segment.
If a boundary causes external suspension or post-commit child work, the pending
obligation must be checkpointed atomically so that committed boundary progress
cannot lose its consequences.

### MechanicalEvent

A MechanicalEvent exists only after an ExecutionSegment commits. It records a
mechanically relevant committed fact/change plus causal execution provenance.

Recommended identity discipline:

```text
event source = committed ExecutionSegment
event ordinal = stable within the segment
(source, ordinal) uniquely identifies the event
```

A retry of the same committed segment returns the same event identities rather
than producing duplicate Events.

One occurrence may legitimately produce several events; payload equality does
not define identity.

### SemanticEvent

Existing `GAME/SCHEMA/event.schema.yaml` is a durable semantic/campaign event
shape. Step 3 should not equate every MechanicalEvent with one SemanticEvent.
Later durability/context stages may promote/compact one or more MechanicalEvents
into durable semantic chronology. MechanicalEvents remain execution receipts;
current world records remain current-state authority.

## 12. Suspension and Continuation

A Continuation is the portable authority for one suspended Resolution episode.

It stores **facts that must survive**, not a blindly trusted snapshot of all
prospective calculations.

Minimum conceptual payload:

```text
continuation_id + generation
command_id / resolution_id / activity version identity
execution cursor + next safe recompute phase
actor/source/target bindings
accepted adjudicated facts + provenance
fixed raw RNG results already generated
choices already made
typed prior-step exports
committed segment/event receipt references
current dependency frontier / pinned relevant revisions
pending ChoiceRequest or ReactionWindow
expected/linked child Resolution identities when applicable
RNG state/frontier for future draws
idempotency / consume state
```

Do not require:

```text
SQLite snapshot
all hydrated objects
all derived MechanicalContext values
all prospective StateDeltas as trusted authority
Temporal Agenda copy
whole campaign Event history
```

## 13. Resume semantics: choice versus reaction

This is a critical distinction.

### Resume after external choice

The choice does not normally authorize unrelated world changes.

Runtime validates the continuation's dependency frontier. If mechanically
relevant dependencies changed unexpectedly, it must not silently reuse stale
prospective state; it returns a typed revalidation/conflict outcome according to
policy.

### Resume after expected reaction child

A reaction is *supposed* to change relevant state/results.

Therefore "any revision changed => stale" is wrong.

The parent Continuation records:

```text
expected child Resolution / reaction window
safe recompute phase
fixed facts that must not be regenerated (for example raw original roll)
```

After the child commits:

```text
consume child receipt
advance dependency frontier to the new committed view
rebuild MechanicalContext
recompute from the declared safe phase
preserve fixed prior RNG/choice inputs
continue parent Resolution
```

Unexpected additional relevant changes still produce conflict/revalidation.

This avoids both stale-delta reuse and unnecessary parent failure after a valid
reaction.

## 14. Idempotency hierarchy

Recommended stable hierarchy:

```text
Interaction invocation ID
  -> IntentPlan ID
      -> IntentClause ID
          -> RuntimeCommand ID
              -> Resolution ID (Action only)
                  -> Continuation ID/generation(s)
              -> ExecutionSegment sequence
                  -> MechanicalEvent ordinal(s)
```

Rules:

1. a transport retry reuses the same accepted command/resume identity;
2. same identity + same normalized fingerprint returns existing result/current
   suspension;
3. same identity + different fingerprint is a typed idempotency conflict;
4. a committed ExecutionSegment is inserted/advanced atomically with its Events
   and execution status;
5. a retry cannot allocate a new event batch for an already committed segment;
6. each suspension generation is single-consume; a stale response to an older
   generation is rejected unless it is an exact retry whose receipt is known;
7. a later intentional repetition of identical player text is a new Interaction
   and therefore a new command, not an idempotency retry.

## 15. RNG continuity

Randomness is deterministic runtime state once generated.

For a Resolution:

- raw random values are generated only when the Activity reaches the relevant
  operation;
- generated values are appended to fixed Resolution trace/exports;
- suspension persists those values before returning control externally;
- future RNG frontier/state is checkpointable;
- resume never rerolls an already generated value;
- if a reaction changes modifiers/outcome interpretation, the original raw roll
  may be reused where the rule says the same roll remains the basis.

Exact PRNG implementation remains implementation planning; Step 3 needs only the
state/identity contract.

## 16. Trigger and reaction execution

Trigger candidates are collected from one pinned state view/occurrence.

Recommended ordering discipline:

1. registered phase/priority semantics first;
2. mechanics that are provably order-independent may use a stable deterministic
   trace order;
3. mechanics whose rules explicitly assign ordering to a player/controller
   produce a typed ChoiceRequest;
4. non-commutative triggers with no deterministic/registered rule produce typed
   adjudication instead of arbitrary ID/list/SQL sorting.

Each trigger firing receives an idempotency/firing key scoped to the source
binding plus triggering occurrence so the same binding cannot refire on the same
occurrence because of retry.

Trigger chains are explicit parent/child Resolution chains and have configurable
limits on depth/total child executions/trigger emissions. Hitting a limit is a
typed failure/suspension condition, never silent truncation.

Pre-commit reaction children may change the parent result and therefore force
parent recomputation from a safe phase. Post-commit Event-trigger children cannot
rewrite the triggering Event or its already committed segment.

## 17. Checkpoint continuity

Step 3 defines the portable in-flight execution payload. Step 5 later decides
when/how repository commits publish and restore it.

Checkpoint continuity must preserve enough authority to reconstruct:

- current suspended Resolution/Continuation;
- procedure-local ResourceState needed by it;
- fixed RNG/choice inputs;
- committed segment/event frontier;
- pending reaction/trigger obligations;
- local metric anchors when mechanically material;
- idempotency state needed to distinguish replay from new execution.

The checkpoint may also cache derived indexes, but those are validated/rebuilt
from authoritative/checkpoint sources.

## 18. Analytical challenge

### Counterargument: one generic workflow/execution DAG would be more future-proof

It could represent message plans, Activities, transitions, triggers, choices,
reactions, and recovery with one node graph.

**Rejection:** those objects have intentionally different ownership/lifetime
semantics. A generic workflow graph would immediately need mutation nodes,
choice nodes, query nodes, loops/guards, retry semantics, and persistence rules.
HDM already has bounded Activities for reusable procedure composition and only
needs a small ordered IntentPlan above them. Building a workflow language now is
high-cost YAGNI.

### Counterargument: save the prospective delta during suspension and resume it

This minimizes recomputation.

**Rejection:** a reaction exists precisely to modify facts on which the old
prospective result may depend. Trusting the serialized delta would violate the
Step-2 pinned-view model. Store fixed historical inputs and a recompute frontier,
not stale derived truth.

### Counterargument: any relevant revision change should invalidate continuation

This is safe but simple.

**Rejection:** expected child reactions intentionally create relevant changes.
A parent must distinguish expected causal child receipts from unrelated external
changes and re-pin/recompute accordingly.

### Counterargument: deterministic stable sorting is enough for simultaneous triggers

It guarantees reproducibility.

**Rejection:** reproducible arbitrariness is still mechanically wrong when
ordering changes outcomes and the rules assign choice/adjudication. Stable order
is valid only for order-independent or explicitly ordered cases.

### Counterargument: let the LLM emit final IDs and trust validation failures

This reduces binding machinery.

**Rejection:** it still assumes the model has sufficient catalog/context and
encourages hallucinated IDs/hidden state leakage. Bounded discovery plus semantic
selection makes the LLM good at language while the engine remains authority for
identity existence, scope, permissions, and mechanics.

## 19. Decision brief preview

The primary human architecture decision is whether to accept the recommended
ownership model:

```text
IntentPlan = message-level ordered orchestration, not transaction
RuntimeCommand = one idempotent executable clause envelope
Resolution = one Activity invocation only
TransitionRequest = deterministic direct upper path, not fake Activity
ExecutionSegment = shared atomic local execution/commit kernel
Continuation = portable suspended Resolution authority
Signal/BoundaryOccurrence = transient/prospective execution context
MechanicalEvent = immutable post-segment committed mechanics fact
```

The remaining sections are mostly mechanical formalization if this ownership
model is approved.

## 20. Recommendation confidence

**HIGH** for the separation of IntentPlan, Resolution, TransitionRequest, and the
shared ExecutionSegment kernel.

**HIGH** for continuation storing fixed inputs + recompute frontier rather than
trusted prospective deltas.

**MEDIUM-HIGH** for the exact IntentPlan guard/export surface until focused
natural-language compound-intent seed cases are enumerated.

**MEDIUM** for the exact Trigger ordering vocabulary until D&D seed review proves
which simultaneous-order cases require player/controller choice versus
commutative stable ordering.

What would change the core recommendation: evidence that deterministic domain
transitions regularly require the same multi-step/suspend/react mechanics as
Activities, or that ordinary player messages require a reusable general
execution DAG rather than an ordered finite clause plan. Current repository
contracts show neither.
