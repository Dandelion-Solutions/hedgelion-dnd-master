# Step 2 Retrospective Assurance — Slice C Resolution

Status: **ASSURED / AMENDED / STEP 2 REMAINS CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `../design/2026-08-19-step-2-assurance-slice-c-temporal-recovery-task-charter.md`

Coverage/research: `../design/2026-08-19-step-2-assurance-slice-c-temporal-recovery-coverage-research.md`

Adversarial review: `../design/2026-08-19-step-2-assurance-slice-c-temporal-recovery-adversarial-review.md`

This resolution records the human architect's approval of the material temporal amendment found by the retrospective assurance pass. Where earlier Step-2 temporal wording conflicts with this document, this resolution is authoritative for subsequent architecture work.

## 1. Verdict

The accepted Duration/Recovery architecture remains valid with two amendments:

1. adaptive chronology may omit uninferred precision, but must not discard quantitative elapsed evidence that gameplay has actually established;
2. a live Effect application may own a finite set of owner-local scheduled trigger obligations independent of its intrinsic lifetime.

No global clock, background scheduler, generic ScheduledJob entity, fake timer Effect, or long-lived Resolution is introduced.

## 2. Human architecture decision — owner-local stateful scheduled triggers

The human architect approved **Variant A: owner-local stateful scheduled triggers**, noting that the proven mechanics are uncommon and do not justify a generic scheduling subsystem.

The accepted ownership split is:

```text
Effect definition
    scheduled trigger declaration[key]
        metric delay semantics
        bounded Activity identity

world.effect application
    temporal_binding
        optional intrinsic Effect-lifetime binding

    scheduled_trigger_state[key]
        optional concrete next-due TemporalBinding

Temporal Agenda
    disposable index over both kinds of binding

Step 3
    due occurrence, Resolution execution, retry/idempotency, re-arm/unarm
```

The intrinsic binding answers when the Effect itself ends. Scheduled-trigger state answers when a rule owned by the still-live Effect next becomes due. They may reuse the same `TemporalBinding` value contract but are separate authorities.

## 3. Stable owner-local trigger identity

A stateful scheduled trigger declaration has a stable key local to its owning Effect definition.

Conceptually its identity is:

```text
(effect definition ID, local trigger key)
```

The local key is not a new global definition ID, world record, runtime record, or independently meaningful entity. Array position is not semantic identity and may not be used to bind persisted due state to a declaration.

The initial machine contract represents declarations as an object keyed by lowercase local machine keys and represents application state as a map from the same key family to one concrete `TemporalBinding`.

Compiler/loader validation must additionally prove that every active `scheduled_trigger_state` key exists in the resolved owning Effect definition. JSON Schema alone does not attempt cross-record reference validation.

## 4. Initial bounded declaration contract

The initial scheduled-trigger declaration is deliberately narrow:

```text
scheduled_triggers[key]
    after
        duration.metric only
        positive integer amount
        registered unit
    activity_id
        registered reusable Activity reference
```

This is sufficient for the proven `after/every N elapsed time` class.

Procedure/semantic rules such as turn start, dawn, or successful Long Rest continue to use the existing registered boundary/Event mechanisms. The engine must not synthesize metric cadence merely because a semantic event could be approximated as elapsed time.

The declaration is not an arbitrary callback. Exact actor/target binding, occurrence payload, child Resolution construction, branch/roll behavior, chain limits, and result-driven re-arm semantics remain Step-3 responsibilities.

## 5. Application-state lifecycle

A nonterminal Effect may own zero or one current concrete binding per declared scheduled-trigger key.

The bounded state machine is:

```text
UNARMED
    -> arm concrete binding

ARMED(binding)
    -> due
        -> Step-3 execution
        -> REARM(new binding) | UNARM | OWNER TERMINAL

OWNER TERMINAL
    -> no armed scheduled-trigger state remains
```

The machine schema rejects a terminal `world.effect` that still carries `scheduled_trigger_state`.

Refresh/replace must not generically merge stale scheduled state. A rule/definition migration that changes or removes a live stateful trigger declaration must explicitly preserve, re-anchor, reset, migrate, or cancel the corresponding active state as appropriate. Exact reapplication/migration operations remain later implementation work.

## 6. Temporal Agenda remains derived

Agenda rebuild inputs now include at least:

```text
Effect intrinsic TemporalBindings
Effect scheduled-trigger TemporalBindings
Resource delayed recovery bindings
LifeState Stable recovery bindings
checkpointable procedure/runtime temporal obligations
```

Agenda may index `(effect_id, trigger_key, concrete binding)` for fast due discovery, but it owns no canonical scheduling fact. Losing the Agenda never authorizes inferring a missing trigger deadline from prose or rerolling its delay.

## 7. Scheduled trigger versus automatic boundary response

These remain different execution classes:

```text
automatic state-owner response
    exact deterministic typed mutation owned by that subsystem

scheduled trigger due
    bounded Activity/Resolution that may roll, branch, suspend, or trigger
```

A deterministic Resource reset or Condition remove-count can remain a B2 automatic response. A disease save every 24 hours belongs to scheduled-trigger execution through Step 3.

## 8. Adaptive chronology amendment

The old optimization wording that a metric coordinate may `freeze` is narrowed.

Still true:

- wall-clock time never advances fiction;
- unquantified narrative passage need not be converted into exact units;
- unrelated scenes do not receive a global exact timestamp merely for bookkeeping.

New normative rule:

> Once gameplay/procedure state establishes a quantitative elapsed contribution, that temporal evidence must not be discarded merely because no currently armed timer needs it.

This allows later lazy rules such as a revival window to reason from established chronology rather than discovering that an explicit ten-minute wait vanished because no deadline was active at the time.

A later elapsed predicate must resolve only as strongly as retained evidence permits:

```text
TRUE
FALSE
INDETERMINATE
```

The engine must not convert approximate or absent evidence into a convenient exact value. Exact chronology evidence representation, compaction, and `INDETERMINATE` execution handling remain later-stage work.

## 9. Rejected alternatives

The assurance rejects for this requirement:

- generic global `ScheduledJob` / scheduler records;
- fake child Effects used only as timers;
- long-lived suspended Resolutions/Continuations after the creating action has completed;
- one undifferentiated `temporal_bindings` collection mixing intrinsic lifetime and scheduled rule execution;
- declaring the proven periodic elapsed rules unsupported until Step 6.

These either create duplicate ownership, false domain entities, callback/scheduler architecture, or leave a known baseline mechanics class unrepresentable.

## 10. Machine alignment and verification

A focused TDD contract was added in `DEV/TESTS/test_step2_scheduled_trigger_contract.py`.

RED evidence on the pre-amendment schemas:

- Effect definitions rejected `scheduled_triggers`;
- active world Effects rejected `scheduled_trigger_state`;
- field inventory did not expose either field;
- all earlier tests and the maintenance audit remained green.

The minimum GREEN alignment added:

- `definition.effect.data.scheduled_triggers`;
- `world.effect.state.scheduled_trigger_state`;
- matching field-inventory entries;
- terminal-Effect rejection of armed scheduled trigger state.

The complete `Validate engine source` workflow then passed, including the maintenance audit and all DEV unit tests.

## 11. Carry-forward

### Slice D

Verify that scheduled-trigger execution cannot become a declarative world-query surface or a bypass around pinned `MechanicalContext`, registered facts/accessors, dependency-DAG rules, or LLM mechanical-authority restrictions.

Also close earlier Slice-A/B carry-forwards for state-stable `resource.capacity` and current `condition.applicability` evaluation.

### Step 3

Own:

- due-occurrence identity;
- child Resolution construction;
- actor/target/source binding from the owning Effect context;
- retry/idempotency;
- atomic `REARM | UNARM | OWNER TERMINAL` result handling;
- same-time ordering with Effect expiry and other due work;
- exact handling of an Effect being terminated while its scheduled trigger is due;
- checkpointable in-flight execution state.

### Step 5

Own chronology evidence persistence/compaction, cross-scene temporal reconciliation, and continuity publication for local active scheduled-trigger state.

### Step 6

Full seed may add a new scheduled-trigger shape only when a concrete rule cannot be represented by the initial metric-delay + bounded Activity contract.

## 12. Final disposition

Recommendation: **KEEP Step 2 closed with the approved temporal amendment.**

Human decision: **APPROVED — Variant A owner-local stateful scheduled triggers.**

Confidence: **HIGH**.
