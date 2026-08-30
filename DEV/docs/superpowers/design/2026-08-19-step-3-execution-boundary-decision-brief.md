# Step 3 Decision Brief — Deterministic Execution Boundary

Status: **HUMAN ARCHITECTURE DECISION REQUIRED**

Target branch: `feature/mechanical-runtime-hot-state`

Task Brief:

- `DEV/docs/superpowers/design/2026-08-19-step-3-execution-boundary-task-brief.md`

Research Draft:

- `DEV/docs/superpowers/design/2026-08-19-step-3-execution-boundary-research-draft.md`

Retrospective assurance entering this gate:

- `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

This brief asks for the material ownership decision required before a Step-3 Candidate Specification can be written. It incorporates all Steps 1–2 assurance amendments and does not reopen them.

## 1. Decision to make

Choose the authority/lifetime model for executing one natural-language player interaction that may contain several clauses, deterministic transitions, Activities, reactions, choices, partial completion, retries, and suspension.

The key question is:

> Do we preserve distinct upper-level semantic objects and share one lower atomic execution kernel, or collapse them into one more uniform execution object?

## 2. Recommendation — Alternative C

Accept this responsibility split:

```text
Interaction
    host/player exchange boundary

IntentPlan
    ordered material clauses from one Interaction
    NOT a transaction

RuntimeCommand
    one accepted idempotent executable clause envelope
    pins normalized input + ResolvedCatalogContext identity

    action command
        -> ActionRequest
        -> one Resolution(Activity)

    deterministic transition command
        -> TransitionRequest
        -> direct lower execution path

runtime.procedure
    one independently addressable rules-procedure lifetime
    owns participant-local procedure ResourceState
    shared by relevant parent/child Resolutions

ExecutionSegment
    common smallest local atomic execution/persistence kernel

Continuation
    portable authority for one suspended Resolution episode
    references Procedure; does not own procedure ResourceState

Signal / BoundaryOccurrence
    transient/prospective execution context

MechanicalEvent
    immutable fact emitted only after one ExecutionSegment commits
```

Recommendation confidence: **HIGH**.

## 3. Why this is the recommended boundary

### IntentPlan is orchestration, not mechanics

A player message can contain:

```text
pick up the sword
walk into the hall
if the door opens, close it
attack the guard
```

The clauses are related by the player's message but do not form one mechanical transaction. Earlier committed clauses should not be rolled back because a later clause fails or requires clarification.

Therefore `runtime.intent_plan` owns finite ordered orchestration and forward-only guards over typed prior-clause results. It does not own world mutation, RNG, reactions, or a SQLite transaction.

### Resolution keeps one precise meaning

`runtime.resolution` remains:

> one invocation of one reusable Activity with concrete bindings.

This preserves the already accepted Activity boundary and keeps reactions/choices where multi-step procedure execution actually exists.

A Resolution may commit several ExecutionSegments and may suspend/resume under the same Resolution identity.

### Deterministic transitions should not become fake Activities

Moving an already-adjudicated entity to a known location, transferring an exact asset/currency amount, or committing another registered deterministic transition does not need an Activity merely to gain transaction/idempotency/event plumbing.

`TransitionRequest` therefore remains a distinct upper semantic path.

If a requested transition requires a roll, choice, reaction, or other unresolved mechanical procedure, it was misclassified and must use an Activity/Resolution path instead.

### One lower kernel prevents duplicated commit semantics

Actions and deterministic transitions still need the same correctness machinery:

```text
pinned current view
prospective overlay
Step-2 dependency/input validation
state-owner plans
atomic local commit
RNG/frontier where applicable
MechanicalEvent identities
trace/receipt
idempotency markers
continuity bookkeeping
```

`ExecutionSegment` is the single lower atomic kernel for both paths.

This avoids separate mutation/event/retry implementations for Activity versus Transition execution.

## 4. Procedure ownership after assurance

The assurance found that Step 2's procedure-local Resource lifetime already forces an independent operational owner.

Therefore this is now a fixed input to Step 3, not an open alternative:

```text
runtime.procedure
    owns procedure-local participant ResourceState

runtime.resolution
    references/binds procedure when relevant

runtime.continuation
    references procedure + expected frontier

world.encounter
    optional world-facing procedure context/referent
```

A reaction child and its parent use the same Procedure identity where they participate in the same rules procedure.

After the child commits, the parent's previously prospective mechanical view may be stale. The parent must:

```text
consume expected child receipt
advance/re-pin dependency frontier
rebuild MechanicalContext
recompute from a declared safe phase
preserve fixed historical inputs
continue
```

It must not restore or merge an old copy of procedure ResourceState.

## 5. ExecutionSegment semantics

`ExecutionSegment` is recommended as the smallest local atomic execution persistence boundary.

One committed segment may atomically advance any coherent subset required by that execution edge:

```text
world authoritative state
runtime.procedure state
RuntimeCommand / Resolution state
RNG frontier
Continuation creation/consumption
MechanicalEvent batch
ResolutionTrace / segment receipt
idempotency state
dirty/publication bookkeeping
```

Not every segment mutates world state. Persisting fixed RNG results plus a suspension Continuation is a valid segment even if no world delta commits.

A failed prospective segment commits none of its candidate authoritative mutations and emits no committed MechanicalEvents for them.

`ExecutionSegment` is not a world entity and does not become a general workflow node language.

## 6. Signal, BoundaryOccurrence, and Event boundary

### Signal

Transient typed pre-commit/calculation context. It can collect Rule Element contributions and expose a reaction window. It is never committed truth.

### BoundaryOccurrence

Transient typed occurrence context for a registered boundary with stable occurrence identity/key, producer, scope/subject, and causal execution position.

It is the common edge used by state-owner automatic responses. It is not a second scheduler/event authority.

### MechanicalEvent

Exists only after an ExecutionSegment commits.

Recommended identity:

```text
committed segment identity + stable event ordinal
```

Retry of the same committed segment returns the same Event identities.

MechanicalEvents are immutable execution facts/audit evidence. Current world records remain current-state authority; HDM does not become an event-sourced engine.

## 7. Continuation semantics

A Continuation stores what must survive one suspended Resolution, not a trusted snapshot of the entire prospective calculation.

It must preserve as applicable:

```text
command/resolution identity
pinned ResolvedCatalogContext identity/frontier
procedure identity
execution cursor + safe recompute phase
actor/source/target bindings
accepted invocation facts + provenance/fingerprint
fixed generated RNG results
choices already made
typed prior-step exports
committed segment/event references
expected dependency frontier/revisions
pending ChoiceRequest or ReactionWindow
expected child Resolution identities
future RNG frontier
idempotency / single-consume generation state
```

It should not require:

```text
SQLite snapshot
all hydrated objects
all derived MechanicalContext values
trusted prospective deltas
Temporal Agenda copy
Condition/arbitration/DAG caches
whole campaign Event history
procedure ResourceState copy
```

## 8. Catalog-context migration barrier

RuntimeCommand, Resolution, and Continuation are validated under one ResolvedCatalogContext.

An incompatible engine/catalog adoption cannot silently resume a stored Continuation under new semantics.

Later migration/maintenance design must either:

```text
finish before adoption
explicitly migrate in-flight execution
block/reject adoption
or abort through an authorized typed maintenance result
```

No mixed old/new definition meaning inside one active runtime.

## 9. Invocation-adjudicated facts

Accepted fiction-dependent invocation facts are fixed typed execution inputs when used.

Step 3 must define:

```text
registered fact ID
explicit boolean value
provenance
missing-input behavior
normalized input fingerprint
Continuation preservation
```

Missing is not false.

Engine-owned facts cannot be injected through this channel.

Invocation facts do not become lore/current world truth merely because an execution commits.

## 10. Live Effect order evidence

Step 2 accepts whole-application arbitration that may use mechanical recency. Assurance proved that live correctness cannot require indefinite trace/Event-body retention.

Therefore Effect create/replace must receive compact immutable order evidence from the committed execution boundary.

Conceptually:

```text
application_order_key
    stable for one Effect lifecycle episode
    allocated/derived at committed create/replace
    retry-stable
    comparable where recency policy requires it
    independent of wall time / Effect ID / SQL order
    preserved by refresh
```

Exact encoding is mechanical specification work after this gate. ExecutionSegment identity/order plus intra-segment ordinal is one plausible implementation, not yet a decision.

## 11. Owner-local scheduled-trigger due execution

When an Effect scheduled trigger becomes due:

```text
Temporal Agenda discovers due owner/key
    -> stable due occurrence identity
    -> ordinary bounded child Activity/Resolution
    -> normal read/input/reaction rules
    -> atomic result
         REARM(new binding)
         UNARM
         OWNER TERMINAL
```

The Temporal Agenda remains derived. The scheduled trigger does not receive a privileged query/callback interface.

Exact same-time ordering between owner expiry, scheduled trigger due work, boundary responders, and reactions remains Step-3 specification work after the core ownership model is approved.

## 12. Alternative A — one giant Resolution per IntentPlan

```text
Interaction
    -> IntentPlan
        -> one Resolution for the whole message
```

### Advantage

One apparent root execution object and one place for status/receipt.

### Costs

- conflates message interpretation with one mechanical procedure;
- pressures narrative-only and deterministic transition clauses into Activity semantics;
- makes one clause's suspension/reaction lifetime contaminate unrelated clauses;
- makes partial completion/independent retry harder;
- encourages accidental all-or-nothing transaction or compensation semantics;
- clashes with procedure Resource ownership because a player message is not necessarily one rules procedure.

**Recommendation: reject.**

## 13. Alternative B — every executable clause is an Activity Resolution

```text
IntentClause
    -> synthesize/find Activity
    -> Resolution
```

### Advantage

Uniform upper execution path.

### Costs

- exact deterministic domain transitions require fake wrapper Activities;
- catalog accumulates procedural wrappers whose only role is plumbing;
- Activity validation becomes coupled to direct state-transition validation;
- semantic distinction between unresolved procedure and already-adjudicated exact transition disappears.

**Recommendation: reject.**

## 14. Alternative D — generic persistent workflow/execution DAG

One graph could theoretically contain message clauses, Activities, transitions, reactions, choices, timers, retries, and child work.

### Advantage

Maximum structural uniformity and apparent future flexibility.

### Costs

It immediately requires a generic language for:

```text
mutation nodes
query nodes
guards
loops/branching
choice nodes
scheduling
retry semantics
persistence
compensation/cancellation
```

HDM already has bounded Activities for reusable procedure composition and needs only a small finite ordered IntentPlan above them.

This would materially enlarge the executable surface, persistence model, LLM attack surface, migration burden, and implementation cost without a demonstrated rules case.

**Recommendation: reject under YAGNI.**

## 15. Strongest argument against Alternative C

Alternative C introduces several explicit objects (`RuntimeCommand`, `Resolution`, `Procedure`, `ExecutionSegment`, `Continuation`) where a generic workflow model or one universal Resolution might look simpler conceptually.

The cost is real:

- more identity relationships;
- more schema/compiler/trace bookkeeping;
- explicit parent/child/frontier rules;
- careful distinction between command, procedure, Activity invocation, segment, and suspension.

The counterpoint is that these objects already have materially different lifetimes and authorities. Collapsing them does not remove complexity; it hides it inside one overloaded record and makes retry, partial completion, reactions, direct transitions, procedure budgets, and recovery ambiguous.

The recommended model spends explicit type complexity to avoid semantic/authority complexity.

## 16. Failure modes the recommendation specifically prevents

1. same player message accidentally becomes one transaction;
2. later clause failure rolls back already committed fiction/mechanics;
3. deterministic item/location/currency transition gains fake Activity semantics;
4. Action and Transition paths implement different idempotency/event commit rules;
5. reaction child owns a duplicate procedure budget;
6. parent resumes with stale pre-reaction prospective deltas;
7. same command retry creates a second event/effect/spend;
8. old Continuation silently runs under incompatible catalog semantics;
9. Effect recency changes after trace compaction or local ID promotion;
10. scheduled trigger due work bypasses normal Resolution/read/reaction constraints;
11. missing invocation fact silently becomes false;
12. persistent state becomes dependent on an ephemeral LLM fact;
13. uncommitted Signal/candidate result becomes historical Event;
14. checkpoint/Continuation becomes a second mutable world/procedure authority.

## 17. What approval authorizes

Approval of Alternative C authorizes the agent to produce a Step-3 Candidate Specification using the following as fixed responsibility boundaries:

```text
IntentPlan        ordered message orchestration
RuntimeCommand    one idempotent executable clause
Resolution        one Activity invocation
TransitionRequest deterministic direct upper path
runtime.procedure independent operational procedure owner
ExecutionSegment shared atomic local execution kernel
Continuation      suspended Resolution authority
Signal            transient calculation/reaction context
BoundaryOccurrence transient registered-boundary occurrence
MechanicalEvent   immutable post-segment committed fact
```

Approval does **not** freeze:

- exact JSON field names;
- exact ExecutionSegment ID encoding;
- exact Effect application-order-key encoding;
- exact SQLite table layout;
- exact simultaneous trigger/controller ordering vocabulary;
- exact IntentPlan forward-guard export vocabulary;
- exact checkpoint repository transport;
- migration implementation details.

Those are mechanical formalization or later roadmap work unless subsequent analysis exposes another material tradeoff.

## 18. Human decision

### Recommended decision

**Approve Alternative C: separate semantic upper paths with one shared ExecutionSegment kernel and the responsibility split above.**

### Confidence

**HIGH** on the ownership/lifetime split.

**MEDIUM-HIGH** on the eventual small IntentPlan guard/export vocabulary.

**MEDIUM** on exact simultaneous-trigger ordering vocabulary; that remains a focused Step-3 seed/design question, not a reason to reject the core ownership split.

### What would change the recommendation

Reconsider Alternative C only if evidence shows either:

1. deterministic `TransitionRequest` operations routinely require the same multi-step suspension/reaction semantics as Activities, making the distinct upper path artificial; or
2. ordinary natural-language player interactions genuinely require a reusable general workflow DAG rather than a finite ordered IntentPlan with bounded forward guards.

Current repository requirements and assurance findings show neither.
