# Step 2 Mechanical State Ownership Design

Status: **IN PROGRESS — OWNER-APPROVED OWNERSHIP SUB-DECISIONS**

Target branch: `feature/mechanical-runtime-hot-state`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Process: the HP/LifeState boundary is inherited from the owner-approved Step 1 adversarial audit; the Resource/procedure-budget, Condition/Effect, and maintained Effect support sub-decisions below were developed through the current Superpowers architecture brainstorming flow, critically challenged, and explicitly approved by the owner.

This is the live Step 2 design spec. It records accepted ownership decisions as they close so they do not depend on chat history. Step 2 itself is not complete: intrinsic Duration/expiry anchors, remaining Effect/Recovery ownership, schema alignment, focused validation, and the final Step 2 critical pass remain open.

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

## 5. Maintained Effect lifecycle support

### ACCEPTED

Concentration is not a duration mode. It is the first ruleset use of a narrow generic Effect-to-Effect lifecycle-support relation. Intrinsic duration and maintained support are orthogonal termination mechanisms.

A concrete Effect instance may have **zero or one** structural lifecycle parent, referred to in this design as `support_effect_id`. The exact schema field name remains deferred until the ownership map closes, but the cardinality and semantics are accepted.

Support relationships therefore form a forest rather than an arbitrary graph.

### 5.1 Parent identity and mutability

The lifecycle parent is selected when the dependent Effect is created and is immutable for that Effect instance.

At creation time the parent must:

- exist;
- be nonterminal;
- not be the child itself;
- not make the support chain cyclic.

The same maintenance episode keeps the same Effect identity. Refreshing duration, stacks, or allowed parameters updates that Effect in place. A new maintenance-root Effect ID represents a new lifecycle episode.

Re-parenting an existing Effect is not supported in the initial contract. If rules genuinely move a dependent to another maintenance episode, runtime ends the old dependent and creates a new one under the new parent.

### 5.2 Terminal versus suppressed support

Support depends only on lifecycle existence, not on current mechanical effectiveness.

```text
parent nonterminal -> structural support exists
parent suppressed  -> structural support still exists
parent terminal    -> structural support is lost
```

Suppression, equipment predicates, range checks, antimagic, and other temporary activation conditions do not belong in this support primitive. If a ruleset says such a circumstance actually ends the maintenance episode, that rule explicitly transitions the root Effect to a terminal lifecycle state; the support relation reacts only to that terminal transition.

The primitive does not accept arbitrary predicates, Actor fields, Resource expressions, OR trees, or multiple simultaneous parents.

### 5.3 Downward-only cascade

When a support parent becomes terminal, every descendant that structurally depends on it expires because support was lost. A child becoming terminal has no automatic effect on its parent.

There is no generic `detach`, `restrict`, `auto_end_when_no_children`, or reverse-lifecycle policy. Rules that end a maintenance root when their own higher-level conditions are met do so explicitly through normal Effect/Activity/Trigger resolution.

Before mutation, runtime computes the full descendant closure through a HOT/SQLite reverse index, validates the entire closure, and commits the lifecycle transition atomically. Canon stores only forward support references; reverse child indexes are disposable projections.

Simultaneous intrinsic expiry and support loss must not make final state depend on SQL/update ordering. Step 2 requires deterministic terminal closure; Step 3 will own causal event ordering and receipts.

### 5.4 Shared lifetime and Concentration

A maintenance root may own a shared intrinsic maximum lifetime for its episode. Dependents do not copy the same remaining-time authority merely because they share that root.

Conceptually, `Concentration, up to 1 minute` is represented as:

```text
concentration/maintenance root Effect
    intrinsic maximum lifetime = 1 minute
    -> dependent target Effect A
    -> dependent target Effect B
```

If a dependent has a genuinely shorter independent limit, it may additionally own its own intrinsic lifetime. It then ends at the first of its own intrinsic boundary or loss of structural support.

Ruleset-specific exclusivity such as D&D allowing only one current Concentration episode is not generalized into a maintenance-slot/uniqueness subsystem. The ruleset operation that begins a new Concentration episode atomically ends the old root (and therefore its descendants) and creates the new root.

### 5.5 Durability and recovery boundary

A durable/canonical dependent Effect cannot point to a support parent that remains local-only. Promotion closure therefore includes the required support-parent chain. An unresolved canonical support reference during hydration is an integrity failure, not permission to invent a replacement parent.

The support primitive does not introduce background processing. Cascade occurs only when an explicit runtime command/Activity boundary makes a support Effect terminal.

## 6. Critical-pass results for accepted sub-decisions

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

The maintained-support model was challenged against:

- arbitrary predicate dependencies accidentally creating a second rule engine;
- suppression being confused with termination;
- multiple parents and dependency cycles;
- re-parenting and refresh changing lifecycle identity;
- partial/callback-driven cascades;
- simultaneous termination causes;
- reverse child-to-parent lifecycle semantics;
- orphaned durable references after promotion/recovery;
- unnecessary generic uniqueness policy for Concentration;
- large descendant cascades.

The accepted corrections are a single immutable Effect parent, forest topology, terminal-only support loss, downward-only atomic closure, stable maintenance identity, derived reverse indexes, promotion closure, and ruleset-owned Concentration exclusivity. No blocker was found that requires arbitrary dependency expressions or a separate maintenance subsystem.

No blocker was found that requires a separate Resource entity, Condition world entity, separate action-economy/condition mutation subsystem, or generic dependency rule language.

## 7. Exact continuation point

The next open ownership block is **intrinsic Duration / expiry anchors**.

It must settle, without introducing a background clock:

- who owns reusable duration specification versus concrete current progress/anchors;
- fixed turn/round/local-time durations such as `1 round` or `1 minute`;
- relative boundaries such as `until the start/end of my/your next turn`;
- rest/event endings such as `until Long Rest`, dawn, or another named event;
- how event/condition-based endings relate to Trigger Bindings without becoming arbitrary duration predicates;
- when duration progress must be stored versus derived from a stable anchor;
- expiry advancement only through explicit runtime commands/Activities;
- interaction with suspended Resolutions, procedure-local state, and maintained-support roots.

Concentration support itself is closed by Section 5. A Concentration root may still have an intrinsic maximum duration and rules that explicitly terminate that root; those are handled by the Duration/Trigger contracts rather than by a second concentration timer.

After intrinsic Duration/expiry closes, Step 2 still must close remaining Effect/Recovery ownership, exact minimum LifeState vocabulary/transitions, selectors, schema/catalog alignment, focused cases, and a final independent critical pass before the Step 2 gate can close.
