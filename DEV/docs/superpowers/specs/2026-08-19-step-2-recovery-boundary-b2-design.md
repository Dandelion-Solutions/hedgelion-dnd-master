# Step 2 Recovery Boundary B2 Design

Status: **PRELIMINARILY ACCEPTED — REOPEN DURING FINAL ARCHITECTURE REVIEW**

Target branch: `feature/mechanical-runtime-hot-state`

Parent design: `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Purpose and review status

This document records the owner-approved preliminary B2 recovery model developed after comparing two competing ownership approaches:

1. rest-policy-owned recovery steps, where a RestPolicy explicitly lists the state changes caused by a completed rest;
2. boundary-owned production plus state-owner-owned response, where the producer establishes that a typed boundary occurred and each authoritative subsystem owns its own deterministic response.

The second approach was selected in its improved B2 form because it minimizes cross-subsystem coupling, reuses the already accepted Temporal Agenda model, and avoids a second recovery scheduler or callback engine.

This checkpoint is intentionally **preliminary rather than permanently frozen**. The owner plans a later end-to-end architecture review and another brainstorming pass after all major modules have designs. Until that review reopens or replaces this decision, B2 is the active Step 2 ownership model and should guide remaining design work. Exact machine field names, exact JSON Schema, exact boundary-phase ordering, and implementation code remain unauthorized at this checkpoint.

## 2. Problem statement

Recovery mechanics cut across several existing domains:

- persistent Actor and Asset Resources;
- procedure-local action/reaction/movement budgets;
- HP and LifeState rules;
- Effects and Conditions that expire or change on rests, turns, dawn, or other events;
- fixed-time cooldowns or recharge delays;
- rest procedures whose success depends on duration, interruption, and qualification rules;
- the accepted lazy Temporal Agenda that detects metric, procedure, and semantic boundaries.

The current baseline contains overlapping provisional concepts such as `definition.rest_policy.recovery_steps`, `definition.resource.recovery`, `recovery.*` triggers, duration modes, and turn/rest Signals. If each remains an independent timing/ownership vocabulary, the same fact can acquire several representations and different subsystems can claim authority over the same state transition.

The B2 goal is therefore:

> A boundary has one producer and one occurrence identity; mutable state has one authoritative owner; the Temporal Agenda only discovers due work; every automatic response is deterministic and typed; no Rest god-object, background timer, generic callback language, or duplicated recovery authority is introduced.

## 3. Core ownership rule

### PRELIMINARILY ACCEPTED

B2 uses this separation:

```text
BOUNDARY PRODUCER
    owns whether a typed boundary actually occurred

BoundaryOccurrence
    describes one concrete scoped occurrence

STATE OWNER
    owns whether and how its own state responds to that boundary

Temporal/Boundary Agenda
    owns no canonical mechanics
    only indexes due responders for fast discovery
```

The producer never owns the mutable state of unrelated subsystems merely because its boundary can affect them.

Examples:

```text
RestPolicy
    owns qualification/interruption/success of Long Rest
    -> emits boundary.long_rest_complete

ResourceDefinition
    owns automatic recovery semantics for that Resource

Effect instance
    owns its concrete temporal/semantic expiry binding

HP/LifeState ruleset contract
    owns health/lifecycle changes caused by the boundary
```

This keeps ownership aligned with the state being mutated rather than with the event that happens to trigger the mutation.

## 4. Why RestPolicy does not own recovery lists

The rejected strong Rest-owned model would make a RestPolicy enumerate mechanics such as:

```text
restore HP
restore spell slots
restore Hit Dice
restore feature uses
remove/adjust Conditions
expire Effects
```

That representation is attractive because one document visibly describes everything a rest does, but it creates several structural problems.

### 4.1 Excessive fan-out

A RestPolicy would need detailed knowledge of HP, every relevant Resource, Effects, Conditions, Features, and future state kinds. Adding a new recoverable Resource could require editing all applicable RestPolicies instead of editing the Resource definition that owns its mechanic.

### 4.2 Recovery exists outside rests

HDM already needs turn-start, turn-end, round, dawn, timed, named-event, and manual recovery. A Rest-owned engine therefore either fails to cover these cases or evolves into a generic RecoveryPolicy subsystem that no longer has a clean rest-specific responsibility.

### 4.3 Duplicate authority

If `definition.resource.recovery` and `RestPolicy.recovery_steps` can both specify what happens to the same Resource at Long Rest, the architecture has two writable descriptions of one mechanic.

### 4.4 Hidden ordering semantics

A list of recovery steps can accidentally make JSON/list order decide mechanics. If an Effect that grants +2 capacity expires on the same Long Rest that restores a Resource to capacity, `recover then expire` and `expire then recover` can produce different results. Array order must not become rules text.

### 4.5 Centralization can be retained as a view

The useful property of the rejected design is discoverability: a developer wants to ask “what does Long Rest affect?” B2 preserves that benefit through a **derived Boundary Impact View**, not by restoring centralized writable authority.

## 5. One registered boundary vocabulary

### PRELIMINARILY ACCEPTED

Duration, recovery, and procedure timing must converge on one registered boundary vocabulary rather than maintain separate synonymous registries.

Conceptually:

```text
boundary.turn_start
boundary.turn_end
boundary.round_start
boundary.round_end
boundary.short_rest_complete
boundary.long_rest_complete
boundary.dawn
...
```

The exact names are deferred to schema/catalog alignment. The architectural rule is that one semantic occurrence must have one boundary identity.

Consumers then express different reactions to the same fact:

```text
Effect:
    expire on boundary.long_rest_complete

Resource:
    recover on boundary.long_rest_complete

procedure Resource:
    reset consumption on boundary.turn_start(owner)
```

This supersedes the idea that `duration.until_rest`, `recovery.long_rest`, and a rest-completion event must be three independently authoritative timing concepts.

### 5.1 Boundary kinds and temporal bases

The accepted Duration design already recognizes three temporal bases:

1. metric deadline;
2. procedure boundary;
3. semantic boundary.

B2 does not add a fourth time model. It uses those same boundaries as recovery triggers.

A metric deadline may cause a Resource cooldown to become due. A turn-start procedure boundary may reset reaction consumption. A Long Rest semantic boundary may recover spell slots and expire Effects. All are discovered through the same operational agenda/indexing infrastructure.

## 6. BoundaryOccurrence is a runtime value, not a world entity

### PRELIMINARILY ACCEPTED

A concrete boundary occurrence is transient typed runtime context. HDM does not add a canonical `world.boundary`, persistent scheduler row, or definition for each occurrence.

Semantically a BoundaryOccurrence must carry enough information to identify:

- which registered boundary occurred;
- the concrete occurrence identity needed for deterministic retry/idempotency;
- the relevant temporal/procedure context;
- explicit qualifying subject/scope information;
- cause/procedure provenance when required for audit or eligibility.

Exact field names belong to Step 3 event/receipt design.

Example semantics:

```text
boundary = boundary.long_rest_complete
occurrence = one specific completed rest
subjects = actor-A, actor-B
cause = rest-procedure-17
```

Actor C is not affected merely because Actor C exists in the campaign or began an earlier interrupted rest.

## 7. Boundary producers

A boundary producer owns only the rules that establish whether its boundary occurred.

### 7.1 RestPolicy

RestPolicy owns:

- rest type/identity;
- qualification requirements;
- duration/procedure requirements;
- interruption policy;
- success/completion semantics;
- emission of the corresponding successful-completion boundary.

RestPolicy does **not** own:

- spell-slot current values;
- feature-use counters;
- HP counters;
- Effect lifecycle state;
- arbitrary recovery callbacks for other subsystems.

Metric elapsed time and semantic completion remain separate. Eight hours of elapsed time does not automatically produce `boundary.long_rest_complete` if the rules say the rest was interrupted or otherwise invalid.

### 7.2 Encounter/procedure producers

Encounter/procedure state owns when turn/round edges occur. It emits/establishes boundaries such as owner turn start/end according to ruleset procedure state. It does not itself reset every Resource or expire every Effect that is interested in that edge.

### 7.3 Explicit temporal advancement

Metric local-time advancement moves the accepted local monotonic coordinate. When a deadline is reached, the agenda exposes the due binding. The metric clock does not directly mutate the target Resource or Effect.

### 7.4 Semantic/world producers

Named semantic facts such as dawn are produced only when the selected rules/world chronology establishes that they occurred. HDM must not invent synthetic exact seconds merely to manufacture such a boundary when only semantic timing is known.

## 8. State-owner responders

### PRELIMINARILY ACCEPTED

Each subsystem owns a closed response contract over its own authoritative state.

### 8.1 Resource responder

`definition.resource` owns baseline automatic recovery semantics. ResourceState remains the sole mutable authority for current/spent state.

The responder must be storage-independent: it operates through the common Resource resolver whether state is persistent Actor state, persistent Asset state, or procedure-local serializable state.

Candidate response families include only bounded Resource-domain operations proven by real rules, such as:

- reset stored consumption;
- restore to currently derived capacity;
- restore a bounded fixed amount;
- restore a rules-defined portion;
- advance/re-arm a cooldown or next recovery binding.

The exact operation vocabulary is intentionally deferred until focused examples/schema work. No arbitrary executable body is allowed.

### 8.2 Effect responder

An Effect does not use a Resource recovery operation. If its TemporalBinding says it ends on the reached boundary, normal Effect lifecycle machinery makes it due for expiry. Existing maintained-support closure rules then apply if that Effect is a support parent.

### 8.3 HP/LifeState responder

HP and LifeState remain separate authorities, not generic Resources. If a ruleset says a successful rest changes HP or lifecycle state, the health/lifecycle contract owns that response.

The fact that a Long Rest may affect both HP and Resources does not justify moving HP into ResourceState or moving Resource recovery into RestPolicy.

### 8.4 Other future responders

A new subsystem may respond directly to boundaries only when it has a demonstrated authoritative state and a closed typed transition contract. B2 does not authorize a generic “anything can register a callback” mechanism.

## 9. No arbitrary callbacks or second Trigger engine

### PRELIMINARILY ACCEPTED

Boundary responses are not callback programs.

Forbidden examples include:

```text
on long_rest:
    execute arbitrary Activity X

on dawn:
    run script

on resource recovery:
    emit arbitrary new boundary
```

Automatic responders may only perform their registered domain transition through the ordinary runtime mutation path.

If a rule requires a player/GM choice, a roll, spending another Resource, or an optional follow-up action, that mechanic is not an automatic recovery response. It belongs to Activity/Trigger/Resolution behavior in Step 3.

This preserves a strict distinction:

```text
automatic boundary response
    deterministic state transition

choice/reaction/procedure
    Step-3 Resolution/Activity machinery
```

## 10. `resource.recovery` calculation and modifiers

### PRELIMINARILY ACCEPTED

The baseline Resource recovery rule belongs to `definition.resource`, but active Features/Effects may modify the calculated recovery without becoming a second authority.

The existing Rule Element architecture already has a `resource.recovery` selector and pure Contribution model. B2 reuses that pattern:

```text
ResourceDefinition
    baseline recovery semantics
          ↓
resource.recovery calculation
          ↑
pure Rule Element contributions
          ↓
final typed recovery response
          ↓
ResourceResolver mutates ResourceState
```

Rule Elements remain pure. They never directly restore state and never own counters.

Multiple applicable recovery modifiers therefore do not execute in JSON/list order. They are resolved through registered deterministic combination/priority/conflict semantics, consistent with the general Rule Element model.

## 11. Automatic-only recovery boundary

### PRELIMINARILY ACCEPTED

A Resource recovery response is automatic only when runtime can derive the exact transition from authoritative state plus validated rules without human input.

Examples that fit automatic recovery:

```text
restore all spell slots on successful Long Rest
reset reaction spent at owner turn start
restore one charge at a concrete timed deadline
```

Examples that must not be hidden inside Resource recovery:

```text
choose one of several resources to restore
choose which spell slots to recover
make a roll to determine recovery
spend another resource to decide recovery
ask a player whether to use an optional recovery feature
```

Such mechanics require the ordinary Step-3 execution path. B2 deliberately keeps the automatic recovery engine incapable of suspension, player choice, reaction windows, or arbitrary branching.

## 12. Recovery and the accepted Temporal Agenda

### PRELIMINARILY ACCEPTED

Recovery reuses the same Temporal Agenda that indexes Effect expiry. There is no `RecoveryScheduler` beside an `EffectScheduler`.

Example:

```text
Effect A:
    metric expiry at T+10m

Resource B:
    one-charge recharge due at T+15m

Temporal Agenda:
    T+10m -> Effect A due
    T+15m -> Resource B due
```

The agenda owns neither fact. Effect A owns its TemporalBinding. Resource B owns its concrete recovery binding/state. The agenda is a disposable due-index rebuilt after hydration.

### 12.1 Procedure-bound recovery

Reaction refresh works identically:

```text
procedure ResourceState:
    spent = 1

RecoverySpec:
    reset on boundary.turn_start(owner)
```

At the applicable turn-start occurrence, the derived `(boundary, scope) -> responders` index finds both Effects expiring there and Resources resetting there. No separate action-economy reset engine is required.

### 12.2 Rest plus metric expiry

If a Long Rest procedure attempts to advance eight hours while a curse expires after one hour, the already accepted interruptible advancement model applies:

```text
requested advance = 8h
nearest due boundary = curse expiry at +1h

advance only +1h
resolve expiry and same-time consequences
retain/revalidate remaining rest progression through Step 3
```

At the end of the required metric duration, RestPolicy still must validate successful completion before producing `boundary.long_rest_complete`.

This keeps Effect expiry and Resource recovery on one temporal infrastructure while preserving the semantic distinction between elapsed time and successful procedure completion.

## 13. Scoped responder discovery and performance

### PRELIMINARILY ACCEPTED

Boundary handling must never scan the whole campaign to ask every record whether it cares about an occurrence.

HOT/SQLite keeps disposable reverse indexes conceptually equivalent to:

```text
(boundary kind, relevant scope/context)
    -> responder/binding IDs
```

Examples:

```text
(boundary.turn_start, actor-A, encounter-17)
    -> actor-A reaction Resource
    -> Effect X until actor-A next turn

(boundary.long_rest_complete, actor-A)
    -> actor-A spell-slot Resource
    -> actor-A Hit Dice Resource
    -> Effect Y until Long Rest
```

The physical implementation may be ordinary SQLite indexes, generated projections, heaps, or another bounded HOT representation. Architecture requires only that cost scale with the due/affected mechanics rather than total campaign size.

For N actual responders, the desired boundary-discovery/transition cost is approximately proportional to N plus the cost of the real domain calculations. B2 does not require mass countdown mutation or catalog-wide scans.

## 14. Discover first, mutate later

### PRELIMINARILY ACCEPTED

The most important critical correction is that a reached boundary may have several interacting responders. Runtime must not mutate state while iterating the agenda in arbitrary index order.

Boundary processing therefore follows this architectural shape:

```text
1. establish one BoundaryOccurrence
2. discover the complete immediately due responder set
3. compute Effect lifecycle/support closure
4. compute prospective typed automatic responses
5. resolve any mechanically meaningful same-boundary ordering under Step 3
6. validate the complete BoundaryPlan
7. commit the plan atomically
8. close same-time consequences before advancing time further
```

The Step 2 requirement is **discover first, mutate later** and deterministic closure. Step 2 does not freeze every cross-subsystem phase rule.

### 14.1 Capacity-change counterexample

Suppose:

```text
Resource base capacity = 5
Effect grants +2 capacity until Long Rest
Resource current = 1
Long Rest recovery = restore to capacity
```

At `boundary.long_rest_complete` both Effect expiry and Resource recovery are due.

A naive loop can produce:

```text
recover to 7
then expire Effect
```

or:

```text
expire Effect
then recover to 5
```

depending on iteration order.

B2 forbids deriving rules from agenda/SQL order. The whole due set is discovered first. Exact ruleset simultaneity/phase semantics are finalized in Step 3, where event ordering and atomic mutation segments belong.

## 15. Same-time closure and zero-time chains

Boundary resolution may cause additional same-coordinate consequences, for example an expiring maintenance root expiring descendants. Runtime must complete mechanically required same-time closure before advancing beyond the current coordinate.

B2 does not create an independent recursion/loop policy. Step 3 already owns bounded trigger/resolution-chain behavior and idempotency. The boundary engine relies on that common protection rather than adding a second chain-limit subsystem.

An automatic state-owner responder itself must not manufacture arbitrary new semantic boundaries. If a committed state change legally triggers another mechanic, it proceeds through the ordinary Event/Trigger path.

## 16. Idempotency and retry boundary

A concrete BoundaryOccurrence needs stable occurrence identity sufficient for Step 3 to make automatic responses idempotent across retry/resume.

Failure case:

```text
long_rest_complete applied
process crashes
Resolution resumes
same occurrence is processed again
```

The Resource must not recover twice merely because the host retried execution.

B2 therefore requires compatibility with a responder idempotency key conceptually based on occurrence identity plus responder/owner identity. Exact receipt/event fields and storage belong to Step 3; Step 2 does not invent a parallel recovery transaction log.

## 17. Parallel scenes and scope isolation

A boundary occurrence is local/scoped unless rules and chronology establish a wider scope.

Examples:

- `turn_start` belongs to a specific encounter/procedure and participant;
- `long_rest_complete` applies only to qualifying participants in that completed rest;
- `dawn` may belong to an appropriate local/world chronology scope.

One scene's boundary must not recover state in an unrelated incomparable temporal context merely because both use the same boundary kind.

Cross-scene reconciliation remains a Step 5 concern. B2 requires only that responder discovery never compare or broadcast across incomparable contexts without that reconciliation.

## 18. RestPolicy field consequence

### PRELIMINARILY ACCEPTED SEMANTIC CORRECTION

The current baseline field `definition.rest_policy.recovery_steps` is not accepted as a list of authoritative cross-subsystem recoveries.

During later schema/catalog alignment it should be removed, renamed, or narrowed so RestPolicy contains only its procedure/completion semantics. The exact replacement shape is deferred until the ownership map closes.

If a RestPolicy requires internal procedural steps to establish success, those steps may be represented by its rest procedure contract, but they must not duplicate Resource/HP/Effect ownership.

## 19. Recovery-trigger registry consequence

### PRELIMINARILY ACCEPTED SEMANTIC CORRECTION

The current independent `recovery_triggers` registry is provisional. Long-rest, short-rest, turn, round, dawn, and similar timing identities should converge with the common registered boundary vocabulary rather than remain a separate parallel namespace describing the same occurrence.

This does not yet authorize deleting machine IDs. Exact migration/compatibility treatment belongs to schema/catalog alignment after Step 2 ownership closes.

`recovery.manual` is conceptually different: explicit restoration initiated by an Activity/command is not a temporal boundary and should not be forced into the boundary vocabulary merely for symmetry.

## 20. Boundary Impact View and developer management

B2 deliberately distributes writable ownership, but developer discoverability must remain good.

Development tooling should be able to derive a read-only Boundary Impact View such as:

```text
boundary.long_rest_complete

producer:
    rest_policy.long

responders:
    HP/LifeState rules
    resource.spell_slots
    resource.hit_dice
    resource.feature-X
    Effect definitions/bindings ending on Long Rest
```

This view is not canonical mechanics and must never become a second editable recovery list.

Validation should eventually detect at least:

- references to unknown boundaries;
- invalid boundary scope requirements;
- orphaned or impossible responder bindings;
- duplicate incompatible baseline recovery definitions for the same Resource state;
- illegal response operations for the selected subsystem;
- attempts to treat a choiceful mechanic as an automatic recovery response.

This preserves the primary management advantage of centralized Rest recovery without restoring its coupling and duplicate authority.

## 21. Dependency analysis

B2 intentionally produces mostly one-way dependencies:

```text
RestPolicy / procedure
    -> registered boundary vocabulary

ResourceDefinition
    -> registered boundary vocabulary
    -> Resource resolver contract

Effect Duration
    -> registered boundary vocabulary

Temporal Agenda
    -> authoritative bindings only as an index/projection

Rule Elements
    -> resource.recovery selector
    -> pure Contribution contract
```

It avoids these undesirable reverse dependencies:

```text
RestPolicy -> every Resource definition
RestPolicy -> HP internals
RestPolicy -> Effect mutation internals
ResourceDefinition -> RestPolicy implementation
Effect -> Resource storage implementation
Temporal Agenda -> domain-specific mutation code
```

The remaining intentional cross-step dependencies are:

- Step 3: exact same-boundary phase/simultaneity ordering, receipts, idempotency, zero-time trigger-chain limits, and choiceful follow-ups;
- Step 5: cross-scene/multiplayer boundary reconciliation and local-time conflict handling.

These are forward roadmap dependencies, not reasons for Step 2 to invent substitute systems.

## 22. Failure modes explicitly rejected

B2 rejects the following designs unless the later global review finds concrete evidence requiring them:

- `RestPolicy.recovery_steps` as authoritative cross-subsystem mutation list;
- global boundary broadcast over all campaign records;
- persistent/canonical Temporal Agenda or scheduler entity;
- separate Effect and Recovery schedulers;
- mutable `remaining` countdowns duplicated beside deadlines;
- arbitrary boundary callbacks/scripts;
- automatic recovery that asks players for choices;
- SQL/list iteration order as mechanical phase order;
- state-owner responders that emit arbitrary new semantic boundaries;
- a second recovery-specific idempotency/event log;
- a second action-economy reset engine;
- treating elapsed rest duration as proof of successful rest completion;
- treating HP as a generic Resource merely to simplify rest handling.

## 23. Performance characteristics

The intended fast path is:

- no work while no relevant temporal/procedure boundary is reached;
- indexed lookup of only due responders;
- one Resource calculation per actually affected Resource;
- no decrement of every timed record on each advance;
- no full campaign/catalog scan;
- no persistent duplication of reverse indexes;
- agenda/index rebuilding after hydration from authoritative bindings.

A boundary with K affected mechanics should require work roughly proportional to K plus the true rule calculations and mutation closure. Large campaigns with many unrelated dormant records should not make an actor's Long Rest or turn-start reset materially more expensive.

## 24. Recovery examples

### 24.1 Long Rest resource recovery

```text
Rest procedure succeeds
    -> boundary.long_rest_complete(actor-A)

Resource spell-slots responder discovered
    -> baseline restore_to_capacity
    -> resource.recovery contributions resolved
    -> final ResourceState delta prepared
```

The RestPolicy never writes spell-slot state directly.

### 24.2 Reaction reset

```text
encounter procedure reaches actor-A turn start
    -> boundary.turn_start(actor-A, encounter-17)

reaction Resource responder
    -> reset stored spent/consumption
```

The Actor's persistent Resource state does not duplicate the procedure-local reaction budget.

### 24.3 Timed charge recovery

```text
ResourceState owns next recharge deadline T+15m
Temporal Agenda indexes it
metric pointer reaches T+15m
    -> Resource recovery becomes due
    -> deterministic Resource responder prepares restoration
```

No RecoveryScheduler is created.

### 24.4 Effect and recovery on the same Long Rest

```text
boundary.long_rest_complete
    -> Effect A due to expire
    -> Resource B due to recover
    -> HP rules may also respond

runtime discovers all responders first
computes lifecycle/support closure
builds one BoundaryPlan
commits under Step-3 simultaneity contract
```

## 25. Exit criteria for this preliminary sub-block

This B2 checkpoint is considered sufficiently closed for Step 2 to proceed when all of the following remain true under later neighboring design work:

1. RestPolicy need not enumerate authoritative Resource/HP/Effect state mutations.
2. Resource recovery can represent persistent and procedure-local automatic reset/recharge behavior through the common resolver.
3. Effect expiry and Resource recovery use one boundary/Temporal Agenda infrastructure without sharing mutable authority.
4. A common boundary vocabulary can replace synonymous duration/recovery timing IDs without requiring a universal clock.
5. Boundary processing can discover complete due work before mutation and remain compatible with Step-3 deterministic simultaneity/idempotency.
6. Parallel scenes can remain isolated until Step-5 reconciliation is materially required.
7. No demonstrated rules case requires arbitrary recovery callbacks or a second scheduler.
8. Developer discoverability can be recovered through derived tooling rather than centralized writable lists.

## 26. Explicitly open for final architecture review

The owner intends a later holistic review and additional brainstorming after all major modules are designed. The following points should be rechecked then even if no immediate contradiction appears:

- whether one registered boundary vocabulary remains sufficient across all modules;
- whether any standard ruleset has a legitimate automatic recovery that cannot fit the bounded Resource responder vocabulary;
- whether `resource.recovery` Contribution semantics are sufficient for all modifiers without leaking Step-3 choices into Step 2;
- whether same-boundary phase ordering can remain entirely Step-3-owned without requiring a small Step-2 priority class;
- whether cross-scene retained Effects/Resources expose a missing boundary-scope concept during Step 5;
- whether Boundary Impact tooling is sufficient for maintainability once the catalog is fully seeded;
- whether recovery bindings need any additional authoritative state beyond existing Actor/Asset/procedure ResourceState plus accepted TemporalBindings.

Until that review, this document is the active preliminary B2 ownership record.

## 27. Exact continuation

Recovery ownership is preliminarily closed by B2. Step 2 should next continue with the still-open **generic Effect application policy**:

- stacking versus independent applications;
- replacement versus refresh;
- unique-by-source/global semantics;
- valued/stacks distinction;
- definition-owned policy versus instance-owned mutable state;
- non-support expiry/removal consequences.

After generic Effect application policy, Step 2 still must close the minimum LifeState vocabulary/transitions, health/effect selectors, schema/catalog alignment, focused cases, and the final independent critical pass. The later holistic architecture review may reopen this B2 recovery checkpoint.