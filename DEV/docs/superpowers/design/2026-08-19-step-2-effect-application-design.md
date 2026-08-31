# Step 2 Effect Application and Arbitration Design

Status: **PRELIMINARILY ACCEPTED — WHOLE ARCHITECTURE SUBJECT TO HOLISTIC REVIEW**

Target branch: `feature/mechanical-runtime-hot-state`

Parent design: `DEV/docs/superpowers/design/2026-08-18-step-2-mechanical-state-ownership-design.md`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Purpose and review status

This document records the preliminarily accepted Step 2 design for concrete Effect applications, reapplication, overlap/arbitration, target ownership, removal, and non-support end consequences.

The design follows the already accepted HDM boundaries for:

- Condition applications using ordinary Effect-instance machinery;
- immutable single-parent maintained Effect support;
- definition-owned reusable Duration semantics plus instance-owned concrete TemporalBindings;
- disposable HOT/SQLite reverse indexes and Temporal Agenda;
- pure Rule Element contribution calculation;
- Step-3 ownership of exact Resolution/event ordering, idempotency, and trigger execution.

This checkpoint is sufficient for Step 2 sequencing, but it is not exempt from the planned later end-to-end architecture review. The owner intends to re-review **the whole architecture, structures, logic, ownership boundaries, and inter-module relationships** after all major modules have designs. Exact machine field names, exact JSON Schema, catalog migration, and runtime implementation remain unauthorized at this checkpoint.

## 2. Problem statement

The current provisional catalog compresses several different concerns into one broad `stacking` vocabulary. Existing concepts such as `stack.stack`, `stack.replace`, `stack.refresh_duration`, `stack.keep_highest`, `stack.keep_lowest`, `stack.unique_by_source`, `stack.unique_global`, and `world.effect.stacks` mix at least four separate questions:

1. how many concrete applications exist;
2. whether a new application creates, refreshes, or replaces lifecycle state;
3. which simultaneously existing applications are mechanically effective;
4. whether one application owns a mutable intensity/value.

Treating those questions as one enum creates combinatorial policy growth and makes storage identity, lifecycle, mechanical combination, and provenance interfere with one another.

The HDM goal is therefore to make the common case structurally trivial while retaining correct support for rare overlaps:

> one target-local independent application is one Effect instance; new applications are created by default; overlap arbitration is derived and invoked only when a definition/ruleset explicitly requires it; mechanical contribution combination remains the responsibility of Rule Element resolvers rather than the Effect lifecycle subsystem.

## 3. Core invariants

### PRELIMINARILY ACCEPTED

The initial Effect-application contract is governed by these invariants:

```text
ONE independent application
+ ONE target
= ONE EffectInstance
```

and:

```text
application count != stack/intensity value
application existence != mechanical effectiveness
mechanical effectiveness != suppression/availability
refresh != replacement
replacement never overwrites provenance
independent lifetime => independent application
independent source/removal => independent application
```

Additional invariants:

1. a `world.effect` has one concrete target, not `target_ids[]`;
2. a multi-target spell/activity materializes one target-local Effect application per affected target when it creates persistent target state;
3. a Zone, Asset, Location, or other mechanically targetable world record may itself be the one target of an Effect;
4. a shared maintenance/concentration episode may use one support-root Effect targeting the maintainer/owner, with per-target dependent Effects beneath it;
5. a new application creates a new Effect instance unless an explicit validated reapplication policy says otherwise;
6. overlap is a derived fast-path/slow-path concern, never a storage uniqueness constraint;
7. no generic mutable `stacks` counter is required for ordinary repeated applications;
8. a changing intensity/severity inside one lifecycle episode is a typed application parameter, or a Resource when it is genuinely spend/recover state;
9. the Effect subsystem chooses which applications participate; Rule Element resolvers choose how their typed contributions combine;
10. SQL/list order, wall-clock timestamps, and record names are never mechanical arbitration rules.

## 4. Definition versus instance ownership

### 4.1 EffectDefinition ownership

A reusable Effect definition owns stable rules semantics such as:

```text
EffectDefinition
    mechanical payload
    reusable DurationSpec
    validated application-parameter schema
    optional explicit ReapplicationPolicy
    optional explicit ArbitrationPolicy
```

The exact field layout is deferred to schema alignment.

The definition does not own mutable target state, concrete deadlines, source identity, current winner identity, or mutable current-effect flags.

### 4.2 EffectInstance ownership

A concrete application owns facts belonging to that one lifecycle episode:

```text
EffectInstance
    id
    definition reference
    ONE target reference
    source/provenance
    validated application parameters
    concrete TemporalBinding when intrinsic lifetime exists
    optional immutable support parent
    lifecycle state
```

An instance does not copy definition policy into mutable state merely so runtime can evaluate it.

### 4.3 One target is an architectural simplification

The previous provisional `target_ids[]` representation is superseded for target-bearing Effect applications.

Splitting a three-target Bless-like application into three Effects intentionally trades a few additional rows for removal of substantially more complex per-target state:

```text
cast/procedure origin
    -> Effect A -> target Alice
    -> Effect B -> target Bob
    -> Effect C -> target Charlie
```

This avoids universal per-target maps for duration, suppression, removal, values, arbitration, and lifecycle.

The additional record count is acceptable because active long-lived Effects per target are expected to be small and because SQLite/HOT lookup remains indexed.

## 5. Shared multi-target origin and maintained lifecycle

Per-target Effect splitting does not require a new `CastGroup`/`ApplicationGroup` world entity.

Applications created by the same Activity/Resolution share causal provenance. If a mechanically shared lifetime is required, the already accepted support forest provides the lifecycle relation.

Example:

```text
Concentration root C -> target caster
    -> Bless application A -> Alice
    -> Bless application B -> Bob
    -> Bless application C -> Charlie
```

The root owns the shared maintained episode and, where appropriate, the shared maximum lifetime. Dependents do not duplicate the root's remaining-time authority merely because they share the same concentration episode.

If a non-concentration multi-target rule gives each target an equivalent fixed duration, each per-target application may materialize the equivalent independent TemporalBinding because each application genuinely has an independent removable lifecycle even when deadlines initially coincide.

## 6. Provenance and rules-origin identity

Application identity, Effect-template identity, and concrete source are separate concepts.

Conceptually:

```text
effect_id
    = this concrete application

definition_id
    = reusable Effect mechanics/template

rules origin
    = spell / feature / condition / effect identity whose rule created it

source
    = concrete actor / asset / hazard / zone / other source instance

causal origin
    = Activity/Resolution/application event that produced it
```

A reusable Effect template may be used by several different spells or features. Therefore overlap grouping must not assume `definition_id` alone determines semantic sameness.

The exact provenance envelope and committed causal ordering belong to Step 3; Step 2 requires only that enough authoritative provenance exists to derive the correct application family and source-specific rules without treating names as identity.

## 7. Application family

### PRELIMINARILY ACCEPTED

Overlap arbitration is scoped by a derived **application family** rather than by database uniqueness.

The family normally resolves from the rules-bearing origin that defines sameness for the mechanic:

```text
spell-origin application
    -> family normally follows spell definition identity

condition application
    -> family normally follows condition definition identity

direct generic Effect application
    -> family normally follows Effect definition identity
```

This permits two different spells to reuse one Effect template without incorrectly entering one same-spell arbitration group.

The family is a derived/indexed runtime key, not a second canonical identity copied into every Effect by default.

If a future proven rules case requires grouping otherwise-distinct rules origins, schema design may add one registered ruleset-defined grouping policy. No arbitrary user-written grouping expression is authorized by this checkpoint.

## 8. Default reapplication behavior

### PRELIMINARILY ACCEPTED

The default behavior is intentionally simple:

```text
new valid application
    -> create new EffectInstance
```

This remains true even when source, target, and rules origin happen to match.

The default preserves:

- source/provenance;
- independent duration;
- independent removal/dispel;
- causal history;
- support-parent identity;
- correct fallback when a stronger overlapping application later ends.

Retries/idempotency are not solved by merging applications. Step 3 must ensure one committed create operation cannot accidentally create the same application twice on retry.

## 9. Explicit ReapplicationPolicy

Refresh and replacement are exceptions and require explicit validated policy from the ruleset/definition.

Conceptually:

```text
ReapplicationPolicy
    matching semantics
    action = refresh | replace
```

Exact keys and field names are deferred.

### 9.1 Refresh

Refresh means the same lifecycle episode continues:

```text
same Effect ID
same application provenance episode
update permitted application state
update/re-anchor TemporalBinding as rules require
```

Refresh does not resurrect a terminal Effect. Applying the mechanic after terminal state creates a new application.

A refresh policy is appropriate only when the rules genuinely define continuation/renewal of the same episode rather than a new independent application.

### 9.2 Replace

Replace means the old episode ends and a new episode begins:

```text
old Effect -> terminal(reason = replaced)
new Effect -> new identity/provenance
```

The transition must be planned/committed atomically with the new application when the rules require one indivisible replacement operation.

Replace never means overwriting the old row with a new source, deadline, or provenance.

### 9.3 Why uniqueness is not storage uniqueness

Policies such as previous `unique_by_source` or `unique_global` must not become SQL `UNIQUE` constraints or guarantees that only one historical/nonterminal record can exist.

When a rule needs same-source refresh/replace, that is a reapplication rule. When a rule needs only one mechanically effective application among several existing records, that is arbitration. These are different problems.

## 10. Application arbitration

### PRELIMINARILY ACCEPTED

Arbitration answers only:

> Which simultaneously existing target-local applications are mechanically allowed to contribute right now?

If no explicit ArbitrationPolicy applies, all otherwise eligible nonterminal applications participate.

For a policy that requires one effective application, runtime groups candidates by the validated application family and target, then applies a registered deterministic selector.

Conceptually:

```text
(target, application family)
    -> candidate applications
    -> ArbitrationPolicy
    -> effective application set
```

The ordinary case has zero or one candidate and requires no meaningful arbitration work. Multiple candidates are treated as a rare slow path.

### 10.1 Whole-application selection

Arbitration selects complete applications, not individual Rule Elements from several candidates.

A policy must not synthesize a Frankenstein application such as taking one modifier from candidate A and another modifier from candidate B when the rules say only one overlapping application applies.

Once an application is selected, its complete active mechanical payload is passed to the normal Rule Element/Trigger collection path.

### 10.2 Registered selectors only

Selectors may express proven rules semantics such as a whole-application `potency_then_recency` ordering.

HDM does not introduce:

- arbitrary potency expressions;
- user-authored Python/SQL formulas;
- wall-clock tie-breaking;
- JSON/list-order winner selection.

A comparator may inspect only validated typed application parameters exposed for that registered policy.

If a ruleset cannot determine a winner from registered typed facts, runtime produces a typed adjudication requirement for Step 3 rather than guessing.

### 10.3 Mechanical recency

A recency tie-breaker uses committed causal/mechanical ordering, not `created_at` wall-clock timestamps.

Exact event/application ordering representation belongs to Step 3.

## 11. Arbitration versus Rule Element combination

Effect arbitration and Rule Element combination are intentionally separate layers.

```text
Effect Application Resolver
    -> chooses which Effect applications participate

Rule Element Resolver
    -> combines the typed contributions from participating applications
```

Examples of Rule Element-level combination include:

- additive modifiers;
- advantage/disadvantage;
- resistance/immunity/vulnerability;
- minimum/maximum;
- typed override/priority behavior already registered for a selector.

Therefore two independent Effects that both remain effective do not need Effect-level `stack.stack`; they simply contribute through the ordinary selector resolver, which may sum, collapse, reject, or choose according to the registered rule operation.

This prevents Effect lifecycle policy from duplicating the Rule Element combination engine.

## 12. Generic stacks are removed from the conceptual model

### PRELIMINARILY ACCEPTED

The initial architecture does not require a generic mutable `world.effect.stacks` counter.

Repeated applications with independent source, duration, support, removal, or provenance are represented as independent Effect instances.

Example:

```text
Burning A -> source X -> deadline 1
Burning B -> source Y -> deadline 2
Burning C -> source Z -> deadline 3
```

is not represented as:

```text
Burning.stacks = 3
```

### 12.1 Single-episode intensity

If one lifecycle episode genuinely owns a changing severity/intensity, that state is a typed application parameter validated by the Effect/Condition definition.

Example:

```text
poison application
    severity = 3
```

If the mutable quantity instead has capacity/spending/recovery semantics, it should be modeled as a Resource rather than disguised as an Effect stack.

### 12.2 Schema/catalog consequence

During later Step 2 schema/catalog alignment, the existing `world.effect.stacks`, `effect.stacks` selector, and generic stacking registry values must be reviewed for removal or narrowing. They are not treated as final machine contracts merely because they exist in the current provisional catalog.

No migration is performed at this checkpoint.

## 13. Condition aggregation relationship

Condition applications continue to use ordinary Effect instances, so the one-target/one-application rule naturally applies.

Multiple applications of the same named Condition may coexist because they can have different sources and lifetimes.

The Condition definition retains its previously accepted aggregation semantics for named-condition meaning such as presence or a typed effective value. Generic Effect arbitration may share indexed grouping machinery, but Condition identity and Condition-specific aggregation policy are not collapsed into a generic spell-stacking rule.

Application count, Condition effective value, and any typed application parameter remain separate facts.

## 14. Lifecycle, suppression, and arbitration are separate axes

Runtime must not overload one boolean/status field with three different meanings.

Conceptually:

```text
lifecycle
    nonterminal | terminal

availability/suppression
    mechanically available | suppressed/unavailable

arbitration result
    participating/effective | shadowed by competing application
```

A shadowed application remains a real nonterminal application with its own duration, provenance, support relation, and removal semantics.

When the current winner ends, another still-valid candidate can become effective through derived re-arbitration without any resurrection mutation.

Temporary suppression does not itself terminate support or lifecycle. Candidate eligibility under suppression is evaluated according to the registered availability/arbitration contract; no generic persistent winner/suppressed flags are written merely to cache a current decision.

## 15. Zone and spatial-effect exception to record multiplication

The one-target rule does not mean a Zone Effect must create one child Effect for every creature currently inside the Zone.

For a persistent spatial mechanic:

```text
world.zone Z
world.effect E -> target Z
```

is one valid target-local Effect.

Per-creature child Effects are created only when the rules create independent creature-local state that must survive independently, carry its own duration/value/source, or remain after leaving the Zone.

This prevents record explosion for auras, clouds, hazards, and environments while preserving the one-target invariant.

## 16. Maintained support and concentration

Application arbitration does not replace maintained-support semantics.

A dependent target Effect may be shadowed by another application and still remain structurally supported by its maintenance root.

If its support root becomes terminal, it expires through the already accepted support-forest cascade regardless of whether it was currently the arbitration winner.

Starting a new D&D concentration episode remains a ruleset operation that ends the previous concentration root and its descendants before/with creation of the new episode according to Step-3 atomic ordering. It is not modeled as generic Effect-family uniqueness.

## 17. Removal, dispel, and target transfer

### 17.1 Removal/dispel

Removal addresses concrete Effect applications or a rules-resolved set of applications.

Removing a shadowed application may produce no immediate visible modifier change. Removing the current winner invalidates only the affected arbitration group; another still-valid application may become effective automatically as a derived result.

No fallback/winner state is stored canonically.

### 17.2 Target transfer

A target-local application does not normally mutate its `target_id` from one subject to another.

A transfer-like rule is represented as:

```text
old target application -> terminal
new target application -> create
```

If both are part of one continuing maintained episode, they may share the appropriate support root/provenance without re-parenting an existing Effect.

## 18. Effect end consequences

The Effect subsystem distinguishes three end cases.

### 18.1 Derived mechanics disappear automatically

When an Effect becomes terminal, its Rule Elements/Trigger availability stop participating in relevant derived indexes/calculations. No cleanup mutation is required merely to subtract a modifier.

### 18.2 Structural support cascade

If the ended Effect is a support parent, its descendant closure expires through the already accepted support-forest machinery.

### 18.3 Genuine stateful on-end behavior

If the rules say that ending an Effect causes an additional mechanical procedure, HDM uses the existing typed Effect-end Signal/Event plus TriggerBinding/Activity machinery.

The Effect definition does not receive an arbitrary `on_end` script/callback language.

Exact signal/event timing, causal receipts, simultaneous effects, and trigger-chain bounds remain Step 3.

A Trigger predicate may later receive registered event facts such as whether an application was mechanically effective immediately before ending if a proven rule requires that distinction; Step 2 does not add an ad-hoc callback state field.

## 19. Lifecycle end versus physical deletion

Making an Effect terminal and physically garbage-collecting its record are separate concerns.

Runtime first resolves:

- terminal reason;
- support cascade;
- arbitration invalidation;
- same-time boundary closure;
- required Effect-end Signal/Event consequences.

After required durable publication/audit obligations are satisfied, transient/local terminal Effects may be garbage-collected according to persistence policy. Long-term causal history belongs to events/traces/checkpoints rather than requiring every dead Effect record to live forever.

## 20. Prospective-state and atomic mutation rule

Application create/replace/remove can change arbitration and other derived state in the same Resolution segment.

Runtime must not:

```text
mutate candidate A
query intermediate winner
mutate candidate B
```

and let intermediate SQL state determine mechanics.

Instead it plans the complete prospective application changes, derives affected groups against that prospective state, validates required lifecycle/support closure, and commits the applicable atomic mutation segment under Step-3 ordering rules.

This is consistent with the Recovery B2 principle `discover/plan first, mutate later` and with the accepted same-time Duration closure.

## 21. HOT/SQLite indexes and performance

### PRELIMINARILY ACCEPTED

The expected disposable indexes are conceptually equivalent to:

```text
target -> nonterminal Effect application IDs

(target, application family)
    -> candidate application IDs

support parent -> dependent IDs

temporal boundary -> due Effect IDs
```

The exact physical SQLite representation is an implementation decision.

### 21.1 Common path

For zero or one candidate in an arbitration group:

```text
candidate count <= 1
    -> no meaningful comparator work
```

This is the expected dominant single-player path.

### 21.2 Rare overlap slow path

For N overlapping candidates in one small target/family group, arbitration cost is proportional to N. No whole-Actor or whole-campaign scan is required.

Changing one application invalidates only its relevant target/family group and other indexes directly tied to that application.

### 21.3 Persistence

Derived effective/winner/shadowed states are not written as canonical second authorities. HOT/SQLite may cache them and rebuild after hydration.

## 22. Critical-pass findings and corrections

The proposed model was challenged against the following cases.

### 22.1 Shared Effect template used by different spells/features

**Risk:** grouping only by Effect `definition_id` incorrectly treats otherwise distinct rules origins as one family.

**Correction:** family resolves from the rules-bearing origin responsible for sameness, with Effect definition as the normal fallback for directly applied generic Effects.

### 22.2 Multi-target casts lose shared identity

**Risk:** per-target splitting appears to discard the fact that several applications came from one cast.

**Correction:** causal provenance preserves common origin; shared lifecycle uses the existing support root. No extra CastGroup entity is required.

### 22.3 Stacks with independent durations

**Risk:** a scalar `stack_count` cannot represent independent expiry/removal.

**Correction:** each independent unit is its own Effect application; generic stacks are removed.

### 22.4 One episode accumulates severity

**Risk:** removing generic stacks appears unable to represent intensity 1 -> 2 -> 3.

**Correction:** use a typed application-local parameter when the whole episode shares one lifecycle; use Resource semantics if the quantity is genuinely spend/recover state.

### 22.5 Potency is multi-dimensional or ambiguous

**Risk:** an arbitrary universal `potency` score hides rules complexity or selects different parts of competing applications.

**Correction:** registered whole-application comparator only. If the rules do not expose deterministic typed comparison facts, return adjudication required rather than inventing a score.

### 22.6 Shadowed Effect ends with on-end behavior

**Risk:** treating shadowed as nonexistent would lose real lifecycle consequences.

**Correction:** shadowed remains a real nonterminal application; when it actually becomes terminal, ordinary Effect-end semantics apply. Whether a specific Trigger requires prior effectiveness is a typed Step-3 event predicate question.

### 22.7 Winner removal and new application occur simultaneously

**Risk:** sequential mutation exposes invalid intermediate winners.

**Correction:** derive arbitration from prospective mutation state and commit under one validated atomic segment.

### 22.8 Retry creates a duplicate Effect

**Risk:** runtime might mistake retry idempotency for stacking/reapplication policy.

**Correction:** Step 3 idempotency identifies repeated execution of one operation. Effect reapplication semantics only handle genuinely distinct applications.

### 22.9 Same spell from different casters

**Risk:** source-specific grouping would incorrectly let the same spell stack merely because casters differ.

**Correction:** D&D-like same-spell arbitration groups by spell/rules origin plus target unless a specific rule states otherwise; source remains provenance, not the family identity.

### 22.10 Zone/aura record explosion

**Risk:** one-target applications could materialize one child per creature for every spatial effect.

**Correction:** target the Zone itself unless the rule genuinely creates independent creature-local state.

### 22.11 Replace and immutable support parent

**Risk:** replacing a maintenance root might tempt re-parenting old children.

**Correction:** old root becomes terminal and its descendants close; the new root receives newly created dependents. No re-parenting is added.

### 22.12 Suppression versus arbitration

**Risk:** one `active/suppressed` flag becomes responsible for availability, overlap winner selection, and lifecycle.

**Correction:** keep lifecycle, availability/suppression, and derived arbitration as separate axes. No persistent winner flag is required.

## 23. Current baseline consequences

This design semantically supersedes several provisional field/registry assumptions and must be reflected during later Step 2 schema/catalog alignment:

- `world.effect.target_ids` should become one target reference for a concrete Effect application;
- generic `world.effect.stacks` is not part of the preferred application model;
- `effect.stacks` selector is suspect unless a proven typed use remains after seed validation;
- the broad `stacking_behaviors` registry currently mixes application multiplicity, reapplication, and arbitration and should be decomposed or removed rather than extended with more combined enum values;
- `stack.unique_by_source` / `stack.unique_global` must not become storage uniqueness constraints;
- `stack.replace` and `stack.refresh_duration` should become explicit reapplication semantics if they survive concrete seed cases;
- `stack.keep_highest` / `stack.keep_lowest` should become registered whole-application arbitration/comparator semantics only where proven.

No machine catalog/schema edits are authorized before the Step 2 ownership map closes.

## 24. Explicitly rejected complexity

The initial HDM Effect application system does not add:

- multi-target mutable Effect records;
- universal per-target state maps inside an Effect;
- a generic application/composition graph;
- generic mutable stack counters;
- generic stack-unit child objects;
- a CastGroup world entity merely to connect siblings from one cast;
- arbitrary potency/grouping expressions;
- arbitrary Effect-end callbacks;
- persistent winner/shadowed flags;
- SQL uniqueness as gameplay semantics;
- separate Effect-combination arithmetic that duplicates Rule Element resolvers;
- target re-parenting or mutable support topology.

A future addition requires a demonstrated rules case that cannot be represented by target-local applications, typed parameters/Resources, registered arbitration, Rule Elements, support, Duration, or ordinary Trigger/Activity execution.

## 25. Focused examples

### 25.1 Three-target concentration spell

```text
Concentration root C -> caster
    -> Effect E-A -> Alice
    -> Effect E-B -> Bob
    -> Effect E-C -> Charlie
```

One target application can be removed without changing sibling identity. Ending C expires all remaining descendants through support closure.

### 25.2 Overlapping same spell

```text
Spell S application A -> Bob -> stronger/older
Spell S application B -> Bob -> stronger/newer
Spell S application C -> Bob -> weaker
```

All applications remain independently nonterminal. The registered selector chooses the one rules say is effective. When the winner ends, the next eligible candidate is derived without resurrecting any record.

### 25.3 Independent additive effects

```text
Effect A -> target Bob -> contributes +2
Effect B -> target Bob -> contributes +3
```

If both applications participate, the relevant Rule Element selector decides whether the final contribution is +5, max(+2,+3), an override, or another registered behavior. Effect arbitration does not perform that arithmetic.

### 25.4 Independent repeated burn applications

```text
Burn A -> deadline T1
Burn B -> deadline T2
Burn C -> deadline T3
```

Each expires/removes independently. No stack bookkeeping or partial stack expiry is required.

### 25.5 One-episode severity

```text
Condition/Effect P -> target Bob
    severity = 3
    one shared lifecycle
```

Severity is a typed parameter because no historical sub-application must independently expire. If each severity unit came from different applications with separate lifetimes, they must instead be separate Effects.

### 25.6 Zone effect

```text
Effect Cloud -> target Zone Z
```

Creatures entering/leaving are evaluated against Zone mechanics. A creature-local child Effect is created only if the rules grant an independent lasting consequence.

## 26. Exit criteria for this sub-block

This Effect-application checkpoint is sufficiently closed for Step 2 sequencing when the following remain true:

1. every target-local independent application can be represented by one Effect instance;
2. multi-target effects do not require per-target mutable maps in one record;
3. default reapplication is create-new and does not destroy provenance;
4. explicit refresh and replace remain distinguishable lifecycle operations;
5. overlapping applications can coexist without database uniqueness or canonical winner flags;
6. arbitration can select whole applications through registered deterministic policies;
7. mechanical contribution combination remains in Rule Element resolvers;
8. generic mutable stacks are unnecessary for independent applications;
9. single-episode intensity can be represented by typed parameters or Resource semantics;
10. support, Duration, suppression, and arbitration remain orthogonal;
11. removal/dispel and Effect-end behavior do not require arbitrary callbacks;
12. common-case runtime cost remains indexed and near-constant for zero/one candidate groups;
13. no demonstrated rules case requires a multi-target mutable Effect record or generic application graph.

## 27. Whole-architecture review requirement

This checkpoint does not receive a special exemption or special freeze. The later holistic architecture review must re-evaluate this design together with **all** other architecture, structures, ownership rules, runtime logic, schemas, and inter-module relationships.

Effect-specific questions to include in that whole-system pass are:

- whether one-target-per-application remains optimal after Zone, lore, multiplayer, and persistence design are complete;
- whether the rules-origin-derived family is sufficient for the selected ruleset seed;
- whether any real mechanic still justifies a generic stack selector/counter;
- whether arbitration and Rule Element combination remain cleanly separated once all selectors are known;
- whether prospective-state arbitration fits the final Step-3 Resolution transaction model;
- whether transient-effect garbage collection and durable audit requirements remain compatible;
- whether cross-scene target-local Effects expose missing Step-5 reconciliation needs.

These review questions do not block current Step 2 sequencing.

## 28. Exact continuation

Generic Effect application/stacking/refresh/replacement ownership is preliminarily closed by this checkpoint.

The next open Step 2 ownership block is **minimum LifeState vocabulary and transitions**:

- minimum lifecycle states actually required by the selected rules surface;
- ownership of transitions among active/dying/stable/dead or equivalent ruleset states;
- interaction with HP, healing, death saves, Conditions such as Unconscious, and terminal entity state;
- which lifecycle facts are stored versus derived;
- how transformation/resurrection/revival interact with Effect and Activity machinery without duplicating authority.

After LifeState, Step 2 still must close health/effect selectors, schema/catalog alignment, focused cases, and the final independent Step 2 critical pass before its gate can close.