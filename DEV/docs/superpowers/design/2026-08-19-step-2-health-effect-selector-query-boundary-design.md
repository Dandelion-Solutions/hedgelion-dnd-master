# Step 2 Health/Effect Selectors and Query Boundaries Design

Status: **CANDIDATE — OWNER-APPROVED DIRECTION, ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Parent design: `DEV/docs/superpowers/design/2026-08-18-step-2-mechanical-state-ownership-design.md`

Roadmap owner: Step 2 of `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Process: architectural/deep-work path under `DEV/DESIGN_PROCESS.md` and the HDM adapter in `DEV/ARCHITECTURE/DESIGN_PROCESS.md`. The human architect approved the three-surface direction before this candidate specification was written. No runtime implementation or machine-schema migration is authorized by this document.

## 1. Purpose

This design closes the read/calculation boundary required by the accepted Step 2 HP, LifeState, Condition, Effect, Resource, Duration, and Recovery ownership models.

The problem is not merely to add more selector IDs. HDM already uses `selector` for one specific concept: a registered calculation surface into which pure Rule Elements contribute. The architecture also needs a safe way for predicates to read mechanical state and a separate way for runtime internals to locate authoritative records efficiently.

The accepted direction is therefore three intentionally different surfaces:

```text
1. Calculation Selectors
2. Mechanical Context Facts / Values
3. Runtime-only Domain Query APIs
```

They must not collapse into one generic query language.

## 2. Core invariants

The design is governed by these invariants:

1. a calculation selector answers **what calculation is being resolved**;
2. a Mechanical Context accessor answers **what typed fact/value is visible to that calculation**;
3. a domain query answers **how runtime locates the authoritative/derived objects needed to build or execute the calculation**;
4. declarative content may use only registered selectors and registered context accessors;
5. declarative content may not issue arbitrary world/SQL/JSON queries;
6. domain query APIs are runtime capabilities and are not serializable executable content;
7. direct authoritative facts and derived values remain distinguishable;
8. no derived result becomes a second canonical stored authority merely for query convenience;
9. engine-owned mechanical facts cannot be asserted by the LLM as invocation context;
10. all reads participating in one calculation observe one explicit immutable state view;
11. selector/accessor dependencies must be statically bounded and cycles must be rejected;
12. the common HOT/SQLite path scales with relevant hydrated/indexed state, not whole-campaign scans.

## 3. Terminology

### 3.1 Calculation Selector

A registered calculation point that accepts typed Contributions from Rule Elements and resolves them under deterministic combination rules.

Existing examples include:

```text
attack.roll
damage.received
resource.capacity
resource.recovery
effect.duration
```

A selector is not a generic property path and is not a search expression.

### 3.2 Mechanical Context Accessor

A registered typed read available to predicates/calculations within a bound MechanicalContext.

Examples:

```text
health.current(target)
life.state(target)
condition.present(target, condition.poisoned)
resource.available(actor, resource.reaction)
```

The logical contract is parameterized and typed; exact JSON syntax is deferred to schema alignment.

### 3.3 Domain Query API

A runtime-only typed capability used by resolvers/context builders to locate authoritative records or disposable projections through bounded indexes.

Examples include locating target-local Effect applications, arbitration candidates, ResourceState lifetime owners, support descendants, temporal due bindings, and boundary responders.

Domain queries are implementation/runtime contracts. A Rule Element, predicate, Activity definition, or LLM-authored content object cannot contain or execute them.

## 4. MechanicalContext

### 4.1 Logical immutable view

Every calculation/predicate evaluates against one logical `MechanicalContext` bound to an explicit state view.

Conceptually:

```text
MechanicalContext
    state_view
    bound roles (actor/source/target/owner/...)
    registered accessors
    typed prior results, where allowed
    adjudicated invocation facts, where allowed
```

The context is logically immutable for one calculation. A resolver must not observe one predicate before a mutation and another predicate after that mutation merely because both read the same mutable SQLite connection.

### 4.2 Committed versus prospective view

The context declares which state view it represents:

```text
committed
prospective
```

`committed` means the currently committed authoritative state.

`prospective` means a typed prospective state assembled by the current Resolution/planner before commit. This is required by already accepted HP/LifeState semantics, where lifecycle resolution consumes prospective HP/max-HP facts.

Step 3 owns the exact construction, phase ordering, atomic mutation segments, event identity, and commit boundary of prospective views. Step 2 requires only that context reads never silently choose a state view.

### 4.3 Lazy physical realization is allowed

`MechanicalContext` is a logical isolation contract, not a requirement to eagerly materialize every possible fact.

Runtime may lazily evaluate and memoize registered accessors from already hydrated records and bounded HOT/SQLite indexes, provided that:

- all reads observe the same declared state view;
- evaluation is deterministic;
- accessors cannot mutate state;
- no accessor performs an unbounded campaign scan;
- a repeated accessor call within the context returns the same value unless the context itself is replaced by a new prospective/committed view.

## 5. Authority/source classes for context data

Each registered accessor/fact family declares its source class.

### `DIRECT_AUTHORITY`

Reads an authoritative state value without creating an alias.

Step 2 examples:

```text
health.current
health.temporary
life.state
owner_effect.parameter
```

`owner_effect.parameter` is restricted to validated typed parameters of the Rule Element/Trigger's owning Effect application. It is not arbitrary Effect JSON access.

### `DERIVED_MECHANICAL`

Deterministically computes from authoritative state and registered resolvers/projections.

Step 2 examples:

```text
health.maximum
health.bloodied
condition.present
condition.value
resource.capacity
resource.available
```

Derived values are cache/context data, never new canonical fields.

### `INVOCATION_ADJUDICATED`

A fact the deterministic engine cannot infer by itself and which is supplied by the host/LLM after explicit adjudication, for example certain fiction-dependent visibility/reachability/context facts from the existing Activity model.

This class is outside the Step 2 health/effect authority itself but is essential to the LLM/runtime boundary.

### `PRIOR_RESULT`

A typed result exported by a previous operation in the same Resolution according to that operation's contract.

## 6. LLM authority boundary

The host/LLM must not assert values belonging to `DIRECT_AUTHORITY` or `DERIVED_MECHANICAL` accessor families as trusted invocation facts.

Forbidden examples include an ActionRequest effectively claiming:

```text
"target is dead"
"target has Poisoned"
"actor has 2 reactions available"
"target is Bloodied"
```

when those are engine-resolvable facts.

Runtime derives them from the bound state view.

The LLM may adjudicate only facts whose registry/source class explicitly permits `INVOCATION_ADJUDICATED` input. Engine-checkable contradictions remain validation errors.

This preserves the intended split:

```text
LLM
    natural-language interpretation
    entity/reference mapping
    fiction-only adjudication
    intent construction

Deterministic core
    authoritative state
    mechanical facts
    calculations
    validation
    mutation
```

The complete LLM/core integration architecture is a separate cross-cutting roadmap concern; this Step 2 rule is a local non-negotiable authority boundary.

## 7. Step 2 calculation-selector surface

The selector registry remains reserved for calculations that can accept typed Contributions.

### 7.1 Existing selectors retained as Step 2 dependencies

```text
damage.received
healing.received
resource.cost
resource.capacity
resource.recovery
effect.duration
```

Their exact operation compatibility tables are finalized during catalog/schema alignment and focused seed validation.

### 7.2 `health.maximum`

Add a dedicated maximum-HP calculation selector.

Rationale: accepted Actor ownership makes resolved maximum HP a calculation over base/permanent components plus active Effect contributions. Persisting the resolved maximum would create duplicate authority.

Conceptually:

```text
base/archetype/build HP maximum
+ permanent actor adjustment
+ active Rule Element Contributions at health.maximum
= resolved health.maximum
```

The exact allowed operations should remain narrow and evidence-driven, initially covering only deterministic numeric adjustment/replacement semantics required by the selected rules seed.

### 7.3 `condition.application`

Add a narrow calculation/application gate for attempting to apply a named Condition to a target.

Its purpose is to support rules such as Condition Immunity without storing copied per-target booleans and without giving the application operation arbitrary query logic.

Conceptually:

```text
attempt Condition X on target
    -> condition.application calculation
    -> applicable target/source mechanics contribute
    -> deterministic allow/block/typed disposition
    -> if allowed, ordinary Effect-instance application proceeds
```

This selector does not own Condition lifecycle, aggregation, duration, or removal.

### 7.4 Selectors explicitly not introduced here

Do not add the following merely as read conveniences:

```text
life.state
effect.active
condition.present
condition.value
resource.available
duration.remaining
```

They are context accessors or domain-query results, not contribution calculations.

### 7.5 `effect.stacks`

The current provisional `effect.stacks` selector is not part of the preferred Step 2 conceptual model. The accepted Effect-application design removed generic mutable Effect stacks. During schema/catalog alignment this selector must be removed unless a concrete seed mechanic proves a separate typed calculation requirement that cannot be represented by application parameters, Condition aggregation, Resource semantics, or Rule Element combination.

## 8. Minimum Step 2 Mechanical Context accessors

Exact serialized syntax is deferred, but each accessor has a registered ID, typed argument contract, return type, source class, permitted consumers, and dependency metadata.

### 8.1 Health

```text
health.current(subject) -> integer
    DIRECT_AUTHORITY

health.temporary(subject) -> integer
    DIRECT_AUTHORITY

health.maximum(subject) -> integer
    DERIVED_MECHANICAL

health.bloodied(subject) -> boolean
    DERIVED_MECHANICAL
```

`health.bloodied` is derived from the same state-view values used by the current calculation. Conceptually:

```text
bloodied = (current * 2 <= maximum)
```

No `bloodied` flag is stored on Actor state.

### 8.2 LifeState

```text
life.state(subject) -> registered LifeState ID
    DIRECT_AUTHORITY
```

Do not add aliases such as `is_dead`, `is_alive`, `can_act`, `is_unconscious`, or `is_incapacitated` as stored/read duplicates. Rules compare the typed state ID or use separate Condition/activity-availability mechanics.

State-local progress is not exposed as a general accessor in the initial surface. A future rule that truly needs direct death-save-progress inspection must prove a bounded typed use rather than receiving arbitrary lifecycle JSON access.

### 8.3 Conditions

```text
condition.present(subject, condition_id) -> boolean
    DERIVED_MECHANICAL

condition.value(subject, condition_id) -> typed scalar/enum/absent
    DERIVED_MECHANICAL
```

Both derive from nonterminal/eligible Effect applications plus the registered Condition aggregation contract. They do not read a copied Actor `condition_ids` list.

`condition.value` exists because some named Conditions can carry an effective typed severity/level. The exact aggregation semantics are definition/ruleset-owned and must be resolved by the dedicated Exhaustion/valued-Condition nested analysis before Step 2 schema alignment.

The ordinary declarative surface does not initially expose application count, source list, application IDs, or arbitrary Effect provenance. Those belong to runtime domain queries unless a concrete rules need proves otherwise.

### 8.4 Resources

```text
resource.capacity(subject, resource_id) -> nonnegative numeric capacity
    DERIVED_MECHANICAL

resource.available(subject, resource_id) -> nonnegative numeric availability
    DERIVED_MECHANICAL
```

`resource.available` is the semantic abstraction over storage strategy.

For a persistent Resource, state may naturally store `current`.
For a procedure-local Resource, state may store `spent` while capacity is derived.
Predicates do not depend on that physical difference.

Do not expose raw `current`/`spent` through the generic declarative accessor surface merely because those fields exist internally.

### 8.5 Owning Effect parameter

```text
owner_effect.parameter(parameter_id) -> value validated by owning definition
    DIRECT_AUTHORITY
```

This accessor is available only to mechanics owned by that Effect application/definition and only for declared application parameters. It cannot name another Effect ID, walk support relations, or access arbitrary stored fields.

### 8.6 Duration and Recovery

No generic declarative `duration.remaining` or `recovery.next_due` accessor is introduced in the initial surface.

Runtime certainly needs to inspect remaining duration/due bindings for execution, diagnostics, context assembly, and user-facing summaries, but that is a domain-query/read-model concern unless a concrete mechanical rule proves that another selector/predicate must depend on the value.

This keeps temporal internals out of ordinary Rule Element predicates and avoids turning time bindings into a generic expression language.

## 9. Typed accessor syntax, not arbitrary paths

The existing mechanical-predicate schema currently supports simple machine-ID facts/refs. Schema alignment must evolve it toward typed registered accessor references without creating a path/query DSL.

Conceptually valid forms may resemble:

```json
{"ref":"health.current","subject":"target"}
```

```json
{
  "ref":"condition.present",
  "subject":"target",
  "condition_id":"condition.poisoned"
}
```

```json
{
  "ref":"resource.available",
  "subject":"actor",
  "resource_id":"resource.reaction"
}
```

The registry defines the exact allowed arguments for each accessor. Unknown parameters are invalid.

Forbidden concepts include:

```text
json_path
sql
where
join
aggregate
arbitrary filter expressions
reflection over record fields
unregistered computed expressions
```

Binding roles (`actor`, `source`, `target`, `owner`, etc.) are supplied by the calculation/Activity/Trigger operation contract. Catalog content does not hard-code incidental world IDs where a bound role is intended.

## 10. Runtime-only domain query boundaries

### 10.1 Effect domain

Runtime must have bounded indexed capabilities equivalent to:

```text
applications for target
applications for named Condition identity
application-family candidates for target
participating/effective applications after arbitration
support descendants / reverse support lookup
applications matching a removal/dispel contract
```

These queries use HOT/SQLite projections over authoritative Effect instances. Their result sets are not copied into Actor canon.

### 10.2 Resource domain

Runtime capabilities must resolve:

```text
Resource definition/reference
lifetime owner and storage location
stored ResourceState
resolved capacity
resolved available amount
due recovery binding/responders
```

The same semantic Resource API hides Actor/Asset/procedure physical storage differences.

### 10.3 Temporal/Boundary domain

Runtime capabilities must resolve:

```text
nearest due temporal binding
bindings due at reached coordinate/boundary
responders for (boundary, scope/context)
```

These use the disposable Temporal Agenda and scoped responder indexes. No campaign-wide polling API is introduced.

### 10.4 Content boundary

Domain queries are not representable as Rule Elements, predicates, Activities, Effect parameters, or arbitrary user/LLM data.

A later host/context-assembly layer may expose selected typed read operations to the LLM, but that is a separate interface with its own permissions and hydration policy. It does not make domain query syntax executable catalog content.

## 11. Effect collection and Condition lookup

Runtime mechanics normally should not need a generic `effect.present(...)` predicate accessor.

Effects that grant mechanics carry their Rule Elements/Triggers with the application or its reusable definition; the resolver collects mechanics from relevant participating applications. This is cheaper and more precise than asking every unrelated Rule Element to search for Effects by ID.

Named Conditions are different because D&D rules explicitly address Condition identity across mechanics. `condition.present/value` therefore receive a narrow registered accessor family backed by the Condition/Effect index.

A future proven mechanic that must address another Effect family from outside that Effect's own payload may justify a narrowly typed accessor. It must not be generalized pre-emptively.

## 12. Dependency discipline and cycle prevention

### 12.1 Why this is required

Derived calculations can recursively depend on active Effects whose predicates depend on other derived calculations.

Example of an invalid cycle:

```text
health.maximum
    -> Effect contribution
        -> predicate reads health.bloodied
            -> health.bloodied reads health.maximum
```

Likewise:

```text
resource.capacity(R)
    -> Effect contribution
        -> predicate reads resource.available(R)
            -> resource.available(R) reads resource.capacity(R)
```

A naive lazy evaluator would recurse, oscillate, depend on cache order, or require undocumented fixed-point semantics.

### 12.2 Registry metadata

Every calculation selector and context accessor declares enough dependency metadata to determine what it may read.

At minimum the registry records:

```text
return/value type
source class
allowed binding/arguments
allowed consumers/selectors
calculation/accessor dependencies
```

### 12.3 Compile/load-time cycle rejection

Catalog compilation/hydration must build the relevant dependency graph for each validated mechanical definition/combination and reject any dependency cycle that can affect a calculation.

If acyclicity cannot be established from registered typed dependencies, the mechanic is invalid rather than implicitly receiving fixed-point or evaluation-order semantics.

HDM does not introduce generic fixed-point iteration, repeated-until-stable rule evaluation, or SQL/cache-order tie breaking in Step 2.

### 12.4 Cross-resource/effect cycles

Cycle detection must not be limited to a selector name alone. Bound references may create cross-resource or cross-effect dependencies. Schema/catalog work must preserve enough typed identity to detect or conservatively reject those cycles.

Exact compiler algorithm is implementation planning, but the architectural invariant is normative: mechanically relevant dependency graphs are acyclic unless a future explicit subsystem is designed for a proven cyclic rules case.

## 13. Condition application versus Condition aggregation

`condition.application` and `condition.present/value` solve different problems.

```text
condition.application
    -> prospective calculation: may this named Condition application be created?

condition.present/value
    -> read: what is the effective named Condition state in this MechanicalContext?
```

Application does not consult a copied condition flag. Aggregation does not mutate or create applications.

The application selector must use prospective context when the pending Resolution has already established relevant prospective facts.

## 14. Effect arbitration relationship

Effect arbitration remains upstream of Rule Element contribution collection.

Conceptually:

```text
Effect domain query/index
    -> nonterminal candidate applications
    -> availability/arbitration
    -> participating applications
    -> collect Rule Elements/Triggers
    -> Calculation Selector resolution
```

Current winner/shadowed state remains derived and disposable. No context accessor writes it back to canon.

## 15. Performance model

The ordinary path should hydrate/index only:

- acting Actor/source;
- explicit target(s);
- relevant persistent/procedure Resources;
- relevant target/source Effects and Conditions;
- current procedure state;
- due temporal/boundary records when the operation requires them.

Registered accessors may use bounded indexes and memoization inside one state view.

Forbidden fast-path regressions include:

- scanning all world Effects to answer `condition.present`;
- scanning all Resources to resolve one named Resource;
- scanning all campaign records for a boundary occurrence;
- rebuilding derived condition/effect lists into canonical Actor records merely to avoid indexes;
- asking the LLM to recompute mechanical modifiers from descriptive text.

## 16. Error and ambiguity behavior

The runtime does not guess when a mechanical read cannot be resolved.

Examples:

- unknown accessor/selector ID -> validation failure;
- accessor used with illegal argument/binding -> validation failure;
- engine-owned fact supplied by LLM as trusted context -> reject/ignore as authoritative input and derive from engine state;
- unresolved mandatory authoritative state -> typed hydration/materialization requirement;
- required fiction-only fact missing -> typed adjudication/clarification requirement according to existing Activity policy;
- dependency cycle -> catalog/definition compilation failure;
- no deterministic arbitration winner where rules require one -> typed adjudication requirement owned by the Resolution path, never list-order selection.

## 17. Direct/derived authority map

```text
Actor.hp.current                         DIRECT
Actor.hp.temporary                       DIRECT
HP maximum base/permanent components     DIRECT
resolved health.maximum                  DERIVED
health.bloodied                          DERIVED

Actor.life_state_id                      DIRECT
life.state accessor                      DIRECT READ

Condition applications                   DIRECT Effect instances
condition.present/value                  DERIVED

Effect target/source/lifecycle/
parameters/support/TemporalBinding        DIRECT
Effect participation/arbitration result  DERIVED

Resource stored state at lifetime owner  DIRECT
resource.capacity/available               DERIVED

TemporalBinding                           DIRECT
remaining duration                        DERIVED
Temporal Agenda                           DERIVED disposable index

BoundaryOccurrence                        TRANSIENT typed runtime context
boundary responder set                    DERIVED disposable index
```

None of the DERIVED rows above becomes a canonical stored field because of this query design.

## 18. Nested Step 2 item: valued Conditions / Exhaustion

The selector/query analysis proves that `condition.value` is needed, but it also exposes an unresolved Condition-aggregation detail.

The selected D&D rules contain at least one cumulative valued Condition (Exhaustion). The current preliminary Condition design deliberately did not finalize whether such semantics are represented by one mutable application parameter, aggregation across multiple applications, a specialized reapplication rule, or another minimal typed mechanism.

Before Step 2 schema/catalog alignment, perform a bounded nested design specifically for valued/cumulative Condition semantics using real seed cases. It must preserve:

- one clear authority for the effective value;
- source/provenance where rules require it;
- deterministic gain/reduction semantics;
- compatibility with ordinary presence-only Conditions;
- no resurrection of generic mutable Effect stacks.

This item does not invalidate the three-surface selector/query architecture.

## 19. Deferred cross-cutting item: LLM <-> deterministic core integration

The project owner raised a fundamental concern about the integration of two deliberately different systems:

- an LLM responsible for natural-language interpretation, lore, narration, imagination, world/event generation, ambiguity and informal player language;
- a deterministic runtime responsible for typed structures, identity, authoritative mechanics, validation, calculation, mutation, persistence and indexed retrieval.

This design locally establishes one boundary: engine-resolvable mechanical facts cannot be supplied as LLM authority.

The complete integration design is consciously deferred to the roadmap stages that own execution/context assembly. It must be revisited no later than Step 3 and refined with Step 4 context selection. Topics include:

- natural-language referent/entity resolution (`this thing`, `that idiot`, etc.);
- mapping prose intents to registered Activities/transition requests;
- catalog lookup versus keeping entire catalogs in LLM context;
- ambiguity/clarification policy;
- hydration and compact context assembly;
- typed receipts returned to the LLM for narration;
- provenance of LLM-adjudicated facts;
- prevention of LLM bypass around deterministic validation;
- graceful handling of unsupported/homebrew mechanics and catalog gaps.

The likely direction is a typed translation/adjudication boundary rather than requiring the LLM to memorize all engine catalogs, but no new canonical decision is made here beyond the authority rule above.

## 20. Analytical challenge summary

### Strongest alternative

One universal typed query system could serve Rule Elements, predicates, runtime internals, and LLM context assembly. It would initially reduce API surface.

### Rejection reason

That approach gives declarative content the same expressive retrieval power as runtime infrastructure. It would tend toward filters, paths, joins, source queries, support traversal, temporal inspection, and aggregation, making correctness/performance depend on a generic query engine and weakening authority isolation.

### Simplest viable alternative

The accepted three-surface model is the smallest design that preserves the already-existing distinction between Rule Element calculation selectors and Activity predicate facts while giving runtime internal resolvers the indexed access they need.

### Recommendation confidence

**HIGH** for the three-surface separation and engine-owned mechanical fact rule.

**MEDIUM** for the exact minimum accessor/selector IDs until full seed/schema validation, especially `condition.application` operation vocabulary and valued-Condition aggregation.

### What would change the recommendation

A substantial real rules seed showing that declarative mechanics routinely require ad-hoc cross-entity queries that cannot be represented by owning Effects/Triggers, registered context accessors, and typed Activity/Resolution bindings would justify reopening the boundary. No such evidence exists in the current architecture baseline.

## 21. Candidate acceptance criteria

This sub-block can proceed to preliminary acceptance after adversarial review and owner resolution if:

1. selector, context-accessor, and runtime-query responsibilities remain non-overlapping;
2. engine-owned mechanical facts cannot be forged by LLM invocation context;
3. direct versus derived authority is explicit;
4. prospective/committed state-view semantics are explicit;
5. health/LifeState/Condition/Resource minimum reads cover proven Step 2 cases;
6. Duration/Recovery remain runtime-query concerns unless a proven predicate need appears;
7. dependency cycles are rejected rather than assigned hidden evaluation-order semantics;
8. no generic Effect stack selector survives without evidence;
9. valued-Condition/Exhaustion work is explicitly owned before schema alignment;
10. schema/catalog alignment remains frozen until this design and its nested blocker are resolved.

## 22. Next process step

Run an independent adversarial architecture review against this Candidate Specification, the parent Step 2 designs, Rule Element/Activity models, and current catalog/schema assumptions.

Classify findings as `BLOCKING`, `SIGNIFICANT`, or `MINOR`, then resolve them before recording this sub-block as preliminarily accepted and moving to the valued-Condition nested item / Step 2 schema alignment.