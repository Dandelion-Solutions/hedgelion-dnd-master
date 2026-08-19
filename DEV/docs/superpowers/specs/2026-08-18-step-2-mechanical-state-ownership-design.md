# Step 2 Mechanical State Ownership Design

Status: **IN PROGRESS — OWNER-APPROVED OWNERSHIP SUB-DECISIONS**

Target branch: `feature/mechanical-runtime-hot-state`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Process: the HP/LifeState boundary is inherited from the owner-approved Step 1 adversarial audit; the Resource/procedure-budget, Condition/Effect, maintained Effect support, and Duration/Temporal Agenda sub-decisions below were developed through the current Superpowers architecture brainstorming flow, critically challenged, and explicitly approved by the owner. Recovery boundary ownership has additionally reached a **preliminarily accepted B2 checkpoint** that is intentionally marked for reopening during the owner's later holistic architecture review.

This is the live Step 2 design spec. It records accepted ownership decisions as they close so they do not depend on chat history. Step 2 itself is not complete: generic Effect application/stacking policy, minimum LifeState transitions, selectors, schema alignment, focused validation, and the final Step 2 critical pass remain open. Recovery B2 is sufficiently closed for sequencing but is not permanently frozen against the planned final review.

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

## 6. Duration ownership and lazy Temporal Agenda

### ACCEPTED

HDM separates reusable duration semantics from the concrete binding of one active Effect. A definition owns a reusable `DurationSpec`-equivalent rule; an Effect instance owns its concrete `TemporalBinding` for its intrinsic lifetime. Exact machine field names remain deferred until the ownership map closes.

Campaign chronology remains primarily a sparse causal/partial order. Duration does not introduce a universal campaign clock. Temporal precision is activated only where a mechanic or currently executing procedure makes elapsed time material.

### 6.1 Three temporal binding mechanisms

A concrete intrinsic lifetime is materialized on the cheapest basis that preserves the rules:

1. **metric deadline** — elapsed quantities such as one minute or one hour when a local metric coordinate is appropriate;
2. **procedure boundary** — rules-relative edges such as the start or end of a particular participant's next turn;
3. **semantic boundary** — qualifying events such as Long Rest completion, dawn, or another named rules event.

These are alternative temporal bases, not three independent authorities for the same lifetime. A definition may say `1 minute`; runtime compiles that meaning into the basis that is mechanically correct in the current rules context. Encounter turn/round semantics must not be naively implemented as `+6 seconds` per participant turn.

Rest completion is a semantic boundary even if the rest procedure also advances metric time. An interrupted rest therefore does not falsely satisfy `until Long Rest`. Likewise, dawn need not be fabricated as a number of seconds when only a semantic dawn boundary is known.

### 6.2 Local metric context

Where metric precision is required, the relevant local temporal context owns one monotonic exact coordinate. It advances only through explicit runtime/procedure advancement and never follows wall-clock time.

The coordinate is demand-driven:

```text
metric obligations/procedure need elapsed precision
    -> coordinate may advance

no metric obligation and no current procedure needs elapsed precision
    -> coordinate freezes
```

A dormant coordinate does not need an epoch reset. If precision becomes relevant again later, advancement may resume from the same arbitrary local coordinate because no mechanic required accounting for the intervening narrative compression.

Metric storage should use exact integer quanta rather than floating-point time. The exact minimum unit is a schema decision to be made later; Step 2 fixes only the no-float/no-wall-clock ownership rule.

### 6.3 Temporal Agenda is a disposable projection

The Temporal Agenda is not a canonical entity and does not own Effect duration. It is a HOT/SQLite index rebuilt from authoritative temporal bindings and active procedure/semantic waiters.

Conceptually it exposes indexed due work for:

```text
metric deadline -> owning record/effect IDs
procedure edge  -> owning record/effect IDs
semantic event  -> owning record/effect IDs
```

Its physical implementation may be an indexed SQL query, heap, or equivalent runtime structure without changing the architecture. No scheduler file is written to Git merely to mirror active bindings.

If HOT state is lost, recovery restores the authoritative local metric coordinate when it is materially active, restores active bindings from snapshot state, and rebuilds the Agenda. Full campaign event replay is not required.

### 6.4 Time advancement is interruptible

A fictional transition that materially advances elapsed time reports one elapsed contribution to the runtime/procedure. Mechanical micro-operations such as arithmetic, a roll, or an inventory field mutation do not individually invent durations merely because a timed Effect exists.

A requested metric advancement may not jump over the earliest due boundary. If `20 minutes` are requested and the next due boundary is in `10 minutes`, runtime advances only to that boundary, resolves the resulting state, and exposes the unconsumed remainder to Step 3 continuation logic.

```text
requested delta = 20m
nearest boundary = 10m

advance 10m
resolve boundary and consequences
return/retain 10m unconsumed continuation
```

The Duration subsystem does not automatically assume the original intent remains valid after the boundary. Step 3 owns whether the interrupted plan may resume, must be revalidated, or requires new player input.

Before time can advance past a reached coordinate, all mechanically required same-time consequences at that coordinate must reach deterministic closure. Scheduler ordering is not allowed to change the final state. Trigger-chain bounds and causal receipt ordering belong to Step 3 rather than to a second scheduler callback engine.

### 6.5 Re-anchoring between incompatible bases

`remaining` is normally derived, not a mutable countdown authority.

For a metric binding:

```text
remaining = deadline - context.now
```

If the same Effect must move to an incompatible temporal basis/context, runtime derives the remaining budget once at the transfer boundary and materializes an equivalent new binding. It does not keep both the old deadline and a writable `remaining` counter.

```text
old binding -> derive remaining once -> new binding
```

Ordinary combat/exploration transitions do not require re-anchoring unless their temporal bases are actually incompatible. A procedure-native turn/round binding may require re-anchoring when leaving that procedure if the Effect survives it.

The temporal binding belongs to the Effect/lifecycle episode, not independently to each target's physical location. A multi-target Effect therefore does not acquire several clocks merely because targets later occupy different scenes. If a surviving temporal dependency begins to connect previously incomparable scene chronologies, the affected contexts must be minimally reconciled/transferred before their metric coordinates are compared; Step 5 owns the multiplayer/cross-scene reconciliation algorithm.

### 6.6 Refresh, expiry, and lifecycle interaction

Refreshing, extending, or shortening the same nonterminal lifecycle episode updates that Effect's authoritative binding and therefore the derived Agenda entry. The Effect identity remains stable.

If an updated deadline is already at or before the current boundary, the Effect becomes due in the current same-time closure rather than creating an expiry event in the past. A terminal Effect is never refreshed back to life; a new application creates a new Effect instance.

Intrinsic Duration and maintained support are orthogonal. A maintained Effect ends at the first valid terminal mechanism: its own intrinsic temporal boundary or loss of its structural support parent. `Concentration, up to 1 minute` therefore uses one maintenance/support episode plus one intrinsic TemporalBinding, not two duration authorities.

No arbitrary future callback language is introduced. A reached temporal boundary reports a typed due fact; existing Effect/Trigger/Activity machinery owns the resulting mechanical transition.

## 7. Recovery boundary ownership — B2 checkpoint

### PRELIMINARILY ACCEPTED — REOPEN DURING FINAL ARCHITECTURE REVIEW

The detailed B2 design is recorded in:

`DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`

This section fixes the ownership boundary needed for Step 2 sequencing; the detailed companion records the full dependency analysis, failure modes, performance implications, rejected alternatives, and final-review reopen list.

### 7.1 Boundary producer versus state-owner response

A procedure/event that establishes a boundary owns only whether that boundary occurred. Each state owner owns how its own state automatically responds.

Conceptually:

```text
RestPolicy
    -> qualifies and completes Long Rest
    -> produces one long-rest-complete boundary occurrence

ResourceDefinition
    -> owns automatic Resource recovery semantics

Effect instance
    -> owns expiry binding

HP/LifeState contract
    -> owns health/lifecycle response
```

`RestPolicy` must not become an authoritative list of spell-slot, HP, Effect, Condition, Feature, or other cross-subsystem mutations merely because those mechanics respond to a completed rest.

### 7.2 One registered boundary vocabulary

Duration, recovery, and procedure refresh must use one semantic boundary identity for the same occurrence. Separate synonymous timing authorities such as `duration.until_rest`, `recovery.long_rest`, and a third independently meaningful rest-completion timing fact must converge during later catalog/schema alignment.

The common vocabulary must cover proven procedure/semantic edges such as turn start/end, round start/end, successful short/long rest completion, dawn, and other named boundaries. Exact IDs remain deferred.

`recovery.manual` is not forced into this temporal vocabulary: explicit restoration initiated by an Activity/command is an operation, not a temporal boundary.

### 7.3 BoundaryOccurrence

A concrete boundary occurrence is transient typed runtime context, not a canonical world entity or persistent scheduler record. It must support a stable occurrence identity, relevant context/provenance, and explicit qualifying scope/subjects so retries can be idempotent and unrelated scenes/actors are not accidentally affected.

Exact occurrence/event fields belong to Step 3.

### 7.4 Closed subsystem responders

State-owner responders are closed typed contracts, not arbitrary callbacks.

Resource recovery may perform only registered bounded Resource-domain operations such as reset consumption, restore toward currently derived capacity, bounded restoration, or cooldown/recharge advancement as proven by focused cases. Effect expiry uses Effect lifecycle machinery. HP/LifeState uses its own ruleset transition contract.

Any mechanic requiring a choice, roll, optional use, reaction window, or spending another Resource belongs to Step-3 Activity/Trigger/Resolution behavior rather than automatic recovery.

### 7.5 Resource baseline plus pure modifiers

`definition.resource` owns baseline recovery semantics. Active Effects/Features may modify the calculation through the existing pure `resource.recovery` Rule Element selector/contribution model. Rule Elements never mutate ResourceState and never own counters.

This preserves:

```text
ResourceDefinition -> baseline semantics
Rule Elements       -> pure contributions
ResourceResolver    -> deterministic calculation/mutation
ResourceState       -> sole mutable authority
```

Multiple recovery modifiers therefore use deterministic contribution combination/conflict semantics rather than list/JSON execution order.

### 7.6 One Temporal Agenda for expiry and recovery

Timed Resource recovery/recharge bindings use the same accepted Temporal Agenda infrastructure as Effect expiry. No separate RecoveryScheduler or action-economy reset engine is introduced.

Procedure-local resets likewise bind to procedure boundaries such as the relevant owner's turn start. The agenda/reverse indexes are disposable HOT/SQLite projections; authoritative state remains on the owning Resource/Effect/procedure state.

### 7.7 Scoped indexed discovery

Boundary handling must not broadcast across the campaign. HOT/SQLite derives bounded indexes equivalent to `(boundary kind, relevant scope/context) -> responder IDs` and evaluates only actually affected state owners.

The intended cost of a boundary is proportional to the mechanics actually due, not total campaign size.

### 7.8 Discover first, mutate later

A reached boundary may simultaneously expire Effects, change derived capacities, reset Resources, and trigger support closure. Runtime therefore discovers the complete immediately due set and computes the prospective boundary closure **before** committing domain mutations.

SQL/index/list iteration order is never mechanical ordering. The exact same-boundary phase/simultaneity contract, occurrence idempotency, causal receipts, and zero-time trigger-chain rules remain Step-3 responsibilities.

### 7.9 Rest duration is not rest completion

A rest procedure may advance metric time, but satisfying its nominal elapsed duration does not itself prove successful completion. RestPolicy applies interruption/qualification rules first; only success produces the semantic rest-completion boundary. Effects/recoveries that key off Long Rest therefore respond to successful completion, not merely to eight hours passing.

### 7.10 Current baseline consequences

The existing baseline field `definition.rest_policy.recovery_steps` is semantically superseded as an authoritative cross-subsystem recovery list. During later schema/catalog alignment it must be removed, renamed, or narrowed to rest-procedure semantics without duplicating state-owner recovery authority.

The independent `recovery_triggers` registry is also provisional where it duplicates common boundary identities. Exact migration/compatibility changes remain deferred until the Step 2 ownership map closes.

### 7.11 Deliberate forward dependencies

B2 deliberately leaves these details to their roadmap owners:

- Step 3: exact same-boundary phase ordering, event/receipt shape, idempotency keys, zero-time chain bounds, and choiceful follow-ups;
- Step 5: cross-scene/multiplayer boundary reconciliation and local-time conflict handling.

Those are forward dependencies, not permission for Step 2 to create substitute Recovery-specific execution or reconciliation systems.

### 7.12 Final-review reopen condition

B2 is the active preliminary ownership contract, but the planned end-to-end architecture review must explicitly re-check the common boundary vocabulary, bounded automatic Resource response vocabulary, same-boundary phase assumptions, cross-scene scope requirements, and developer Boundary Impact tooling before the whole architecture is declared final.

## 8. Critical-pass results for accepted sub-decisions

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

The Duration/Temporal Agenda model was challenged against:

- turning adaptive chronology into a universal world clock;
- resetting scheduler epochs unnecessarily;
- decrementing every timed Effect on every advance;
- crossing a material expiry in the middle of a long declared action;
- blindly resuming that action after the world changes;
- same-time cascades and zero-time consequence chains;
- treating each combatant turn as six additional elapsed seconds;
- forcing all turn/rest/dawn boundaries into metric seconds;
- multi-target Effects whose targets move into different scenes;
- restart/hydration with a disposable agenda;
- refresh/shorten producing past deadlines;
- scheduler callbacks becoming a second execution engine.

The accepted corrections are an anchor-first authoritative binding, a lazy local metric coordinate, three typed temporal bases, a disposable Agenda, interruptible next-boundary advancement, same-time closure, derived remaining/re-anchor only at incompatible-basis transfer, Effect-owned rather than target-owned temporal binding, semantic rest/dawn boundaries, and Step-3-owned continuation/trigger execution.

The preliminary Recovery B2 model was challenged against:

- RestPolicy becoming a god-object over every recoverable state kind;
- recovery existing outside rests;
- duplicate RestPolicy/Resource authorities;
- parallel duration/recovery timing vocabularies;
- campaign-wide boundary broadcasts;
- arbitrary responder callbacks becoming a second Trigger engine;
- multiple recovery modifiers depending on array order;
- choiceful recovery leaking into automatic state mutation;
- a separate timed Recovery scheduler or action-economy reset engine;
- rest duration being confused with successful rest completion;
- simultaneous Effect expiry changing Resource capacity on the same boundary;
- retry/resume applying one recovery occurrence twice;
- responders recursively manufacturing new boundaries;
- cross-scene scope leakage;
- distributed ownership becoming hard for developers to inspect.

The B2 corrections are boundary-producer/state-owner separation, a common registered boundary vocabulary, scoped occurrence identity, closed deterministic subsystem responders, `resource.recovery` pure contributions, one Temporal Agenda, indexed responder discovery, discover-first/mutate-later BoundaryPlan construction, Step-3-owned simultaneity/idempotency, Step-5-owned reconciliation, and a derived read-only Boundary Impact View. No blocker was found that requires authoritative Rest recovery lists, a persistent scheduler, a second recovery execution engine, or arbitrary callbacks.

No blocker was found that requires a separate Resource entity, Condition world entity, separate action-economy/condition mutation subsystem, generic dependency rule language, global clock, persistent scheduler entity, mass countdown updates, arbitrary scheduled callbacks, or a Rest-owned cross-subsystem recovery list.

## 9. Exact continuation point

Recovery ownership is preliminarily closed by the B2 checkpoint. The next open Step 2 ownership block is **generic Effect application policy**.

It must settle, without reopening the accepted support/Duration boundaries unless a contradiction is found:

- stacking versus genuinely independent applications;
- replacement versus refresh of an existing lifecycle episode;
- unique-by-source versus unique-global behavior;
- how `world.effect.stacks`, application multiplicity, and valued Effect parameters remain distinct;
- which stacking/refresh policy belongs to the definition versus which mutable facts belong to the concrete Effect instance;
- non-support expiry/removal consequences;
- whether generic Effect policy can share machinery with the already accepted Condition aggregation boundary without conflating Condition identity with Effect application identity.

After generic Effect application policy, Step 2 still must close the exact minimum LifeState vocabulary/transitions, health/effect selectors, schema/catalog alignment, focused cases, and a final independent critical pass before the Step 2 gate can close.

The planned later holistic architecture review and additional brainstorming pass may reopen the preliminary Recovery B2 checkpoint; that planned review is explicitly documented rather than being treated as an unresolved blocker to current Step 2 sequencing.
