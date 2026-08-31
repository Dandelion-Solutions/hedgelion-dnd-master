# Step 2 Retrospective Assurance — Slice C Coverage and Research

Status: **ASSURANCE SYNTHESIS — MATERIAL TEMPORAL AMENDMENT UNDER REVIEW**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-2-assurance-slice-c-temporal-recovery-task-charter.md`

## 1. Coverage summary

| Requirement family | Coverage | Finding |
|---|---|---|
| no wall-clock/background loop | FULL | explicit runtime/procedure advancement only |
| DurationSpec vs concrete TemporalBinding | FULL | reusable semantics and active obligation separated |
| procedure-native boundaries | FULL | turn/round semantics are not seconds |
| semantic boundary distinct from elapsed duration | FULL | rest completion/dawn etc. use registered boundaries |
| one intrinsic Effect expiry binding | FULL | sufficient for one intrinsic lifetime |
| Resource delayed recovery | FULL after Slice A | one metric recovery binding/policy initial contract |
| Stable automatic recovery | FULL | LifeState progress owns concrete binding |
| earliest-due interruptible time advance | FULL | cannot jump over nearest due boundary |
| same-time due closure | FULL minimum / Step 3 | discover complete due set before mutation; exact execution ordering later |
| Agenda as derived index | FULL | rebuildable from authoritative bindings/checkpointed runtime state |
| boundary producer vs state-owner response | FULL | no Rest/Recovery god object |
| retrospective elapsed query since past event | PARTIAL / unsafe freeze wording | chronology supports optional exact/approximate time, but Step 2 can discard quantified passage when no active timer |
| periodic metric trigger while Effect also has lifetime | MISSING | one `world.effect.temporal_binding` cannot represent both expiry and repeated trigger schedule |
| periodic procedure/semantic trigger | PARTIAL | event/boundary TriggerBinding can respond when producer exists |
| exact/approximate time uncertainty | PARTIAL | CORE chronology permits it, but mechanical elapsed-query result semantics are not explicit |
| due work surviving crash | DEFERRED_OK to Steps 3/5 | continuity requirement is already explicit |
| cross-scene temporal reconciliation | DEFERRED_OK to Step 5 | local partial chronology is accepted |
| active-binding migration/version | DEFERRED_OK | package/context migration later; binding semantics are typed |

## 2. What survives unchanged

The assurance strongly reaffirms these distinctions:

```text
DurationSpec
    reusable rule meaning

TemporalBinding
    one concrete temporal relation/obligation

BoundaryOccurrence
    transient concrete reached boundary context

Temporal Agenda
    disposable due index

Step-3 execution/Event
    causal commit/idempotency authority
```

No global wall clock, timer daemon, scheduler file, or campaign-wide tick loop is justified.

The three concrete temporal bases remain useful:

```text
metric deadline
procedure boundary
semantic boundary
```

They are not competing clocks; they describe the cheapest authoritative basis for one obligation.

## 3. Finding C-F1 — `metric coordinate freezes when no active timer` is too strong

**Severity: SIGNIFICANT chronology/eligibility gap.**

CORE chronology correctly says exact time is optional and fictional chronology is primarily a partial order. It also says exact/approximate time should be retained when rules, deadlines, travel races, world processes, or later consistency require it.

Step 2 currently adds a stronger optimization:

```text
no metric obligation and no current procedure needs precision
    -> coordinate freezes
```

Taken literally, this can discard a mechanically established elapsed quantity merely because no deadline is currently armed.

### Real lazy-query counterexample

```text
T0 Actor dies
no resurrection timer is created (correct)
player explicitly waits/travels 10 minutes
later a revival mechanic asks: dead no longer than 1 minute?
```

The LifeState design promises that current-death origin remains mechanically recoverable without a `dead_since` Actor counter. If the chronology ignored the explicit 10-minute passage because no active deadline existed, the later query cannot be answered deterministically.

### Required refinement — explicit elapsed evidence is never discarded

Keep adaptive precision, but redefine `freeze`:

> A local metric coordinate does not advance from wall-clock time or unquantified narrative passage. Once a gameplay transition/procedure establishes a quantitative elapsed contribution in a chronology domain, that contribution is chronology evidence and must be retained/compacted without losing its metric meaning, even if no current due timer uses it.

This does **not** require timestamping every event or continuously advancing every scene.

Conceptually chronology can retain metric edges/spans:

```text
event/frontier A -- exactly 10 minutes --> event/frontier B
```

or bounded/approximate evidence when only that is established.

A later elapsed-since query composes bounded relevant evidence from its origin to the current frontier. Step 5 may compact a chain into equivalent summary evidence rather than retain every intermediate event.

### Exactness discipline

If fiction establishes only `several hours later`, the engine must not invent an exact integer. Temporal evidence may be exact, bounded/approximate, or insufficient.

A mechanical predicate such as `elapsed <= 1 minute` may resolve:

```text
TRUE          evidence proves within limit
FALSE         evidence proves beyond limit
INDETERMINATE persisted chronology is insufficient
```

`INDETERMINATE` requires the Step-3/4 typed adjudication/clarification policy; it cannot be converted to a convenient number by the LLM as mechanical authority.

This preserves CORE's adaptive chronology while making lazy elapsed predicates sound.

## 4. Finding C-F2 — periodic metric mechanics have no authoritative due-state owner

**Severity: BLOCKING representational gap in Step 2 baseline.**

The initial TemporalBinding model covers one intrinsic Effect lifetime. TriggerBindings currently react to registered Signals/Events, not directly to a materialized metric cadence.

Official 2024 rules contain persistent Effects/Conditions with repeated metric consequences, for example:

- Pale Tincture: Poisoned creature repeats a save every 24 hours;
- Death Dog disease: while Poisoned, repeat the save every 24 hours that elapse.

These mechanics may coexist with the Effect's own overall lifecycle and therefore need an independent next-due obligation.

A single field cannot be both:

```text
Effect intrinsic expiry deadline
and
next periodic save/damage deadline
```

without duplicate/overloaded authority.

### Alternative A — fake timer child Effects

Create a no-mechanics child Effect whose only purpose is to expire after 24 hours; its end Trigger schedules the save and creates another timer Effect.

Advantages:
- reuses current Effect expiry machinery.

Failures:
- creates semantically fake world Effects;
- timer identity/lifecycle becomes confused with actual game effect;
- proliferates records/history;
- uses end-trigger semantics to implement a cadence by accident;
- creates support/definition/provenance questions that do not exist in the rules.

**Rejected.** Same architectural smell as fake Activities for deterministic transitions.

### Alternative B — generic global scheduler/pending-job entity

Persist arbitrary `(time, callback/activity)` jobs independently of the state owner.

Advantages:
- flexible and familiar.

Failures:
- second temporal authority beside Effect/Resource/LifeState bindings;
- callback/job language;
- orphan/cancellation/promotion complexity;
- easy campaign-wide polling/global-clock drift;
- violates B2 ownership rule that state owner owns its response/obligation.

**Rejected.**

### Alternative C — owner-local scheduled temporal obligation for a bounded Trigger

Allow a rules-bearing owner, initially an Effect application, to materialize additional concrete temporal obligations tied to stable bounded trigger declarations.

Conceptually:

```text
Effect definition
    stateful scheduled trigger declaration
        stable local trigger key
        timing/cadence semantics
        registered Activity / typed trigger behavior

world.effect application
    intrinsic temporal_binding               # optional lifetime end
    scheduled_temporal_bindings[key]         # optional next-due trigger state
```

Each scheduled binding is authoritative **inside its owner application**. Temporal Agenda indexes it but does not own it.

When due:

```text
Agenda discovers owner + trigger key
    -> Step-3 schedules/executes bounded child Resolution
    -> committed result may terminate owner or re-arm next binding
```

There is no arbitrary callback and no independent global scheduled-job authority.

Recommended initial cardinality is bounded by the finite scheduled trigger declarations in the Effect definition; each stateful trigger key owns zero/one current concrete binding. Several different declared periodic mechanics may therefore coexist without an unstructured list of jobs.

**RECOMMENDED.**

## 5. Trigger identity requirement

Current TriggerBindings are embedded values with no independent identity. A trigger that owns persistent next-due state needs a stable key **within its owning definition**, otherwise a concrete binding cannot reliably point back to the reusable rule after restart/catalog reload.

Therefore any stateful scheduled Trigger declaration must have a stable local machine key. This does not make TriggerBinding a world/definition record; it remains an embedded value with owner-local identity, analogous to a named step/export inside a larger definition.

Exact TriggerBinding schema belongs to Step 3 because trigger execution is Step-3 scope, but Step 2 must establish the owner/state requirement now.

## 6. Finding C-F3 — periodic procedure/semantic mechanics should reuse boundaries when naturally available

**Severity: MODERATE clarification.**

Do not materialize metric scheduled bindings for mechanics whose actual rules trigger on an existing procedure/semantic boundary:

```text
start of each turn
end of each Long Rest
daily at dawn
```

These use registered boundary/Event TriggerBindings. A metric scheduled temporal obligation is justified only when the rule is genuinely elapsed-duration relative (for example every 24 hours that elapse from infection), not merely because a calendar conversion is possible.

This preserves the cheapest-basis principle.

## 7. Finding C-F4 — Temporal Agenda rebuild source must include scheduled trigger bindings

**Severity: SIGNIFICANT consequence of C-F2.**

Agenda rebuild inputs become explicitly:

```text
Effect intrinsic TemporalBindings
Effect owner-local scheduled temporal trigger bindings
Resource recovery bindings
LifeState Stable recovery bindings
checkpointable procedure/runtime temporal obligations
```

Agenda remains a disposable index. Rebuild never infers a missing obligation from prose or rerolls its original delay.

## 8. Recovery/boundary review

The B2 recovery ownership model survives:

```text
producer proves boundary occurred
state owner owns its deterministic response
Agenda/index only discovers due responders
```

Automatic responders remain limited to exact typed state-owner mutations. A periodic poison save/damage is **not** smuggled into `Condition automatic_boundary_responses`, because it requires a save/roll/Activity. The scheduled Trigger path reaches Step-3 Resolution instead.

This distinction is important:

```text
automatic Resource/Condition/Effect/LifeState response
    deterministic owner-local transition

scheduled trigger due
    bounded rule-defined Resolution may roll/branch/trigger
```

## 9. Same-time closure and crash/retry

Step 2 correctly requires the complete immediately due set to be discovered before mutation and forbids arbitrary index order from deciding final state. Step 3 must assign occurrence/segment identities so:

- crash after discovery but before commit does not mark work completed;
- committed due response is not repeated on resume;
- re-armed periodic binding becomes visible only through the committed segment;
- one due trigger can change/cancel another prospective obligation deterministically.

No Step-2 scheduler callback is introduced.

## 10. Re-anchoring

The accepted rule remains: one obligation has one active temporal basis. Crossing incompatible contexts derives equivalent remaining/boundary state once and replaces the old binding; it never maintains writable `remaining` beside a deadline.

The new scheduled-trigger binding follows the same rule independently from the Effect's intrinsic lifetime binding.

## 11. Cross-scene chronology

No global exact campaign clock is required. Independent scene/process chronologies remain partially ordered.

When an elapsed query or obligation crosses scene frontiers, Step 5 must reconcile the smallest relevant temporal evidence/frontiers. If exact evidence was never established and cannot be derived, the answer remains typed `INDETERMINATE`; Git commit order or wall time cannot decide fictional chronology.

## 12. Strongest case against Alternative C

The current rules seed may implement many periodic effects using turn/dawn/rest boundaries. Adding stateful scheduled Trigger bindings creates new schema/state complexity before full seed closure.

The counterevidence is direct: official rules include relative `every 24 hours` mechanics, and the current model has no faithful owner for their next due occurrence. Fake timers/global jobs are worse abstractions. Therefore at least the **ownership concept** is required now; exact general Trigger schema can remain Step 3.

## 13. Recommendation

C-F1 is a required clarification of adaptive chronology and does not need a human decision.

C-F2 changes the accepted Step-2 temporal ownership surface: Effects need a bounded owner-local state slot for scheduled temporal Trigger obligations in addition to intrinsic lifetime. This is a material but strongly evidenced architecture amendment.

Recommended architecture:

```text
intrinsic TemporalBinding
    owns one lifetime/end relation

owner-local ScheduledTemporalBinding[key]
    owns one next-due stateful trigger obligation

Temporal Agenda
    derived index over both + other state-owner bindings

Step-3 Trigger/Resolution
    owns execution/re-arm/idempotency when scheduled trigger becomes due
```

Recommendation confidence: **HIGH**.

Human decision required: **PENDING ADVERSARIAL REVIEW**, because C-F2 adds a new persistent state-bearing concept to the accepted Effect/Temporal boundary.
