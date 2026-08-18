# Step 2 Mechanical State Ownership Design

Status: **IN PROGRESS — OWNER-APPROVED OWNERSHIP SUB-DECISIONS**

Target branch: `feature/mechanical-runtime-hot-state`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Process: Superpowers architecture brainstorming + explicit owner approval + critical pass before each accepted sub-decision.

This is the live Step 2 design spec. It records accepted ownership decisions as they close so they do not depend on chat history. Step 2 itself is not complete: exact Duration/expiry/concentration, remaining Effect/Recovery ownership, schema alignment, focused validation, and the final Step 2 critical pass remain open.

No runtime implementation or new schema fields are authorized by this checkpoint. Existing schemas/catalog field inventories remain implementation-frozen where this document identifies an ownership decision whose exact shape is not yet closed.

## 1. Scope and invariants

Step 2 owns the minimum normative model for:

- Resources;
- HP and temporary HP;
- LifeState;
- Effects;
- Conditions;
- Duration and expiry;
- concentration;
- Recovery.

The design must satisfy these invariants:

1. one mutable fact has one authoritative owner;
2. `0 HP` is not a universal synonym for death;
3. derived capacities/effective values are not copied into canon as second authorities;
4. procedure-local state is not written into persistent Actor resources;
5. no wall-clock/background tick loop is introduced;
6. Effect/Condition mechanics remain indexable and cheap enough for the HOT/SQLite fast path;
7. Step 3 may choose exact commitment points, but Step 2 must expose valid resource/effect state transitions without owning Activity segment timing.

## 2. Already accepted health and lifecycle boundary

### ACCEPTED

- Actor `hp` is the single mutable authority for current HP and temporary HP; generic Resource state must not duplicate either counter.
- When HP becomes mechanically materialized, `life_state_id` is materialized in the same atomic transition.
- `life_state_id` is a separate current lifecycle classification. Numeric HP informs ruleset lifecycle resolution but does not permanently derive LifeState.
- Delayed or conditional transformations remain Effects/Triggers. When resolved, one atomic Activity may update form/type, LifeState, and HP.
- Asset durability remains direct Asset state when tracked; generic Resource is used only for a distinct spend/recover mechanic such as charges or fuel.
- One currency representation is authoritative per account/domain; conversion between physical Assets and an abstract balance is atomic rather than a bidirectional duplicated projection.

## 3. Resource ownership and procedure-local budgets

### ACCEPTED

HDM keeps one `definition.resource` concept and one resource resolver API, but mutable ResourceState lives with the lifetime owner selected by the Resource definition/contract.

Conceptually:

```text
persistent Actor ResourceState
    -> Actor.state.resources

persistent Asset ResourceState
    -> Asset.state.resources

procedure-local ResourceState
    -> active procedure/encounter participant budget state
```

There is no standalone `world.resource` or `Budget` entity for ordinary counters.

### 3.1 Procedure-local state

Action, reaction, movement, and similar procedure budgets are not Actor canon and are not owned by an individual Resolution. They are keyed beneath the specific active procedure/encounter and participant so they can survive separate Activities, reactions during another participant's turn, suspension/resumption, and future parallel procedures.

A procedure-local budget is serializable HOT/checkpoint state. `procedure-local` describes its lifetime owner; it does **not** mean disposable Python-local state.

The procedure owner must be specific (`procedure_id`/encounter identity), never a global singleton `current_encounter`.

### 3.2 Stored consumption versus derived capacity

For procedure-local budgets, mutable state normally stores consumption (`spent`/equivalent) for the current recovery epoch. Capacity is resolved from definitions/build/current Effects and is not persisted as a second authority.

Conceptually:

```text
derived capacity = 30
stored spent = 10
available = 20
```

If an Effect changes capacity to 60, stored consumption remains 10 and available becomes 50 without rewriting canonical capacity.

Consumption state is not discarded merely because current derived capacity temporarily becomes zero. It survives until the applicable reset/expiry boundary, preventing a temporarily removed-and-restored capacity from being spent twice in one recovery epoch.

Persistent Resources may continue to use a natural stored `current` representation when appropriate. `current` versus `spent` is a storage strategy beneath one Resource semantics, not a second mechanics subsystem.

### 3.3 Non-interchangeable extra budgets

Capacity units may be combined only when their eligibility semantics are interchangeable.

A restricted additional Action or other special budget is represented by a distinct Resource definition rather than silently increasing the base action capacity. Step 3 may allow an Activity activation to be satisfied by one of several eligible Resource definitions, but Step 2 does not decide the exact Activity commitment point.

### 3.4 Runtime access boundary

Activity, Rule Elements, and Trigger Bindings do not depend on physical storage layout. They resolve a Resource reference through one runtime interface equivalent to:

```text
resolve
check availability
spend
restore
reset
```

The resolver selects Actor, Asset, or procedure state from the Resource contract. This keeps later SQLite or multiplayer projection changes from leaking into Activity definitions.

## 4. Condition, Effect, and LifeState ownership

### ACCEPTED

`definition.condition` remains a distinct named rules identity because rules address conditions by identity. A concrete application of a Condition is represented by the ordinary Effect instance machinery (`world.effect` referencing the Condition definition). HDM does not add `world.condition`.

Actor state does not own canonical `condition_ids` or copied condition state. Active/effective conditions are derived from indexed active Effect applications.

Conceptually:

```text
definition.condition.poisoned
        -> world.effect application A (source X, duration X)
        -> world.effect application B (source Y, duration Y)

HOT/SQLite projection:
        target + condition identity -> active application IDs
```

Removing one application cannot incorrectly remove the named Condition while another valid application remains.

### 4.1 Shared mechanical payload, not mandatory Effect-definition indirection

Condition and Effect definitions may use the same validated mechanical payload model (Rule Elements, Trigger Bindings, Activities, stacking/aggregation semantics as justified by the final schema). A Condition does **not** require an additional `definition.effect` merely to hold its ordinary mechanics.

The earlier idea that every Condition must grant mechanics only through required `effect_ids` is superseded for Step 2 ownership. Exact field names and schema changes remain deferred until the ownership map closes.

A separate referenced/materialized Effect remains valid only when it genuinely has its own independent lifecycle, target set, duration, stacks, or parameters. This avoids a chain of duplicate lifecycle owners.

### 4.2 Application multiplicity versus mechanical aggregation

Several Effect applications may reference the same Condition definition because they have different sources or lifecycle. Application count is not itself mechanical stacking.

The Condition definition owns the deterministic aggregation policy for its applications. The minimum policy vocabulary is intentionally kept small and will be finalized with schema work; simple presence and highest/effective-value behavior are the initial required cases unless further rules evidence proves another policy necessary.

`world.effect.stacks`, number of applications, and a valued Condition's severity/value are separate concepts and must not be silently overloaded into one field.

### 4.3 LifeState is not Condition

LifeState and Condition are separate authorities.

LifeState answers the lifecycle classification question (for example active/dying/stable/dead under a selected ruleset). Condition answers whether a named rules-bearing status is currently applied.

A ruleset may therefore legitimately produce a combination such as:

```text
life_state = dying
condition = unconscious
```

then later:

```text
life_state = stable
condition = unconscious
```

This prevents `life_state_id` and `condition.unconscious` from becoming duplicate writable representations of the same fact.

### 4.4 Condition mutation and fast path

Condition application/removal uses the existing Effect mutation machinery rather than a second condition-mutation subsystem. Semantic commands may resolve matching Condition applications, but committed mutations remain Effect create/update/remove operations.

Transient Condition applications may remain session-local/HOT until durable publication closure requires promotion. HOT/SQLite maintains derived indexes for fast `has_condition`, effective-value, and source lookups; those indexes are disposable projections, not canon.

## 5. Critical-pass results for accepted sub-decisions

The Resource model was challenged against:

- reaction expenditure outside the actor's own turn;
- suspended Resolutions;
- temporary capacity changes;
- restricted/non-interchangeable additional Actions;
- recovery after capacity temporarily becomes zero;
- multiple concurrent/parallel procedures;
- later SQLite/multiplayer storage changes.

The accepted corrections are the specific procedure owner, serializable local state, stored consumption, non-interchangeable Resource IDs, and storage-independent resolver interface above.

The Condition/Effect model was challenged against:

- multiple simultaneous sources of the same Condition;
- lifecycle/removal ambiguity;
- duplicate Actor condition lists;
- mandatory `Condition -> EffectDefinition -> EffectInstance` indirection;
- valued/stacked conditions;
- transient-effect record growth;
- overlap between LifeState and Unconscious/death-related Conditions.

The accepted corrections are direct Condition-to-Effect application identity, shared mechanical payload, derived condition indexing, explicit application-versus-aggregation separation, local Effect IDs where appropriate, and strict LifeState/Condition separation.

No blocker was found that requires a separate Resource entity, Condition world entity, or separate action-economy/condition mutation subsystem.

## 6. Exact continuation point

The next open ownership block is **Duration / expiry / concentration**.

It must settle, without introducing a background clock:

- who owns the duration specification versus current duration progress;
- turn-relative forms such as `until the start/end of my/your next turn`;
- round-count and local-time durations such as `1 minute`;
- event/condition-based endings such as `until Long Rest` or `until condition X`;
- concentration as a lifecycle dependency rather than a second duration authority;
- expiry/reset advancement only through explicit runtime commands/Activities;
- interaction with suspended Resolutions and procedure-local state.

After that, Step 2 still must close remaining Effect/Recovery ownership, exact minimum LifeState vocabulary/transitions, selectors, schema/catalog alignment, focused cases, and a final independent critical pass before the Step 2 gate can close.
