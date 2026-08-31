# Step 2 Retrospective Assurance — Slice D Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — AMENDMENTS MECHANICALLY DETERMINABLE**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed:

- Slice-D solution-blind Task Charter;
- Slice-D coverage/research synthesis;
- accepted selector/query resolution and final Step-2 review;
- Rule Element and Activity models;
- mechanical-surface/predicate/accessor machine contracts;
- Slice-A Resource normalization amendment;
- Slice-B current Condition applicability amendment;
- Slice-C owner-local scheduled-trigger amendment;
- saved Step-3 execution-boundary requirements.

## 1. Verdict

The critic agrees with the coverage synthesis on the substantive gaps:

1. context facts are normatively described as registered but are machine-unregistered;
2. current examples incorrectly place engine-owned mechanics in the fact channel;
3. missing fact versus explicit false is ambiguous in the illustrative request shape;
4. persistent/reconstructable calculations such as Resource capacity cannot safely depend on invocation-only LLM facts;
5. derived-stage dependency contracts are not structured despite the approved hybrid-DAG design;
6. current Condition effectiveness needs an explicit dependency on `condition.applicability`;
7. invocation-sensitive cache identity must include accepted fact inputs;
8. multi-result domain-query ordering cannot acquire gameplay meaning from storage order.

The critic does **not** recommend reopening the three-surface model or the hybrid DAG.

The critic also rejects the coverage draft's proposed new semantic taxonomy `STATE_DERIVED | INVOCATION_DERIVED` as unnecessarily strong for the current need.

The minimum correction is narrower:

> context facts are a registered `INVOCATION_ADJUDICATED` input class, and every reviewed selector/derived stage explicitly declares whether that input class is allowed.

This is capability metadata, not a new ontology of calculations.

No human architecture decision is required because the corrections are forced by already-approved authority/reconstructability invariants and choose the simpler viable representation.

## 2. C1 — fact registry is mandatory

### Attack

Could runtime simply maintain an implementation-local allowlist and leave `{fact: machineId}` structurally open?

### Rejection

That would contradict the catalog/compiler architecture. Reusable Rule Elements/Activities are data and must be statically validateable against stable registered capabilities. A hidden Python allowlist would become a second executable catalog authority and would not be visible to maintenance/schema audits.

A machine-readable fact registry is therefore required.

### Minimum shape

The initial registry should remain small and boolean because current predicate syntax uses facts as boolean propositions.

Conceptually:

```text
context_facts
    fiction.target_visible
        source_class = INVOCATION_ADJUDICATED
        value_type = boolean

    fiction.target_reachable
        source_class = INVOCATION_ADJUDICATED
        value_type = boolean
```

The exact initial IDs are illustrative seed-level choices; the important invariant is that every accepted `{fact: id}` must resolve to registered metadata before definition compilation succeeds.

No engine-owned state is registered here.

## 3. C2 — should facts include engine-owned values for convenience?

### Strongest argument

Having one predicate vocabulary is attractive. `actor.can_act`, `source.equipped`, HP thresholds, and visibility could all look like `{fact: ...}` and runtime could decide which provider supplies each.

### Rejection

This erases the authority distinction the selector/query design deliberately created. The same syntax would hide whether the LLM supplied a value or the engine resolved it from the pinned view. It also weakens dependency tracing because engine-derived facts would not identify their accessor/selector dependency.

Engine-owned mechanical state must use accessors/registered calculations. Context facts are reserved for non-engine-owned invocation adjudication.

The misleading examples must be corrected.

## 4. C3 — explicit false versus missing

### Attack

Treat absent fact IDs as false. This preserves the simple current `context_facts: [id, ...]` list.

### Rejection

Absence is not evidence. In a system where the LLM supplies only bounded adjudicated context, a missing fact can mean the host never adjudicated it. Under `not`, treating missing as false creates a mechanically usable negative claim from no input.

Required semantics:

```text
provided true
provided false
missing / unavailable
```

A predicate that references a missing required invocation fact fails with a typed missing-input result rather than evaluating it false.

The exact Step-3 request representation should therefore support explicit boolean values and provenance. Slice D need not freeze the JSON envelope.

## 5. C4 — attack on `STATE_DERIVED | INVOCATION_DERIVED`

### Coverage proposal

Classify each selector by a new evaluation taxonomy.

### Strongest objection

The architecture currently needs only one enforceable question:

> may this calculation depend on `INVOCATION_ADJUDICATED` input?

A named evaluation taxonomy invites future semantic arguments about whether a materialization calculation, one-roll calculation, Event projection, or recovery calculation belongs to one class even when all the compiler needs is an input capability restriction.

### Resolution

Use the narrower metadata:

```text
allowed_input_classes
    ENGINE_STATE
    INVOCATION_ADJUDICATED
```

or equivalent capability flags.

For current reviewed Step-2 selectors, the safe baseline is:

```text
health.maximum
resource.capacity
resource.recovery
condition.applicability
    -> ENGINE_STATE only

effect.duration
    -> ENGINE_STATE only initially
```

No current Step-2 seed proves that `effect.duration` requires LLM-adjudicated input. If a later concrete rule does, its calculation can explicitly add `INVOCATION_ADJUDICATED` with Step-3 causal-input preservation rather than pre-authorizing the capability now.

This is YAGNI-preserving and does not prevent invocation-sensitive attack/test selectors from admitting facts later when their structured metadata is expanded.

## 6. C5 — transitive restriction is essential

### Attack

It is enough to reject a direct `{fact: ...}` predicate on `resource.capacity` Rule Elements.

### Rejection

A Rule Element could instead read an accessor or derived stage that itself depends on an invocation fact. The resulting capacity is still not reconstructable.

Therefore input-class validation propagates through the scoped dependency graph:

```text
consumer allowed_input_classes
    must cover
transitive source input classes
```

A dependency path from `resource.capacity` to `INVOCATION_ADJUDICATED` is invalid regardless of how many selector/accessor/derived nodes intervene.

This fits the already-approved DAG model; it does not require another graph.

## 7. C6 — derived-node metadata should be structured, not another parallel registry

### Attack

Keep `derived_node_kinds` as a list and add a separate `derived_node_dependencies` object.

### Rejection

That creates two machine authorities whose key sets may drift.

Use one structured object keyed by derived-node kind, for example conceptually:

```text
derived_nodes:
    effect_availability:
        allowed_dependency_kinds: [...]
        allowed_input_classes: [...]
        dependencies: [...fixed edges if any...]
```

The object keys themselves are the registry.

Concrete bound dependencies still come from hydrated definitions/applications. Static metadata does not serialize the whole runtime DAG.

## 8. C7 — Condition applicability must be a current-effectiveness input

The critic confirms Slice B's amendment is incomplete until it reaches the dependency contract.

For a named Condition application:

```text
nonterminal application
    -> basic Effect availability
    -> condition.applicability(target, condition)
    -> eligible member application
    -> Condition aggregation
    -> intrinsic mechanics
```

`condition.applicability` remains a pure selector. It does not own application lifecycle, suppression storage, or a copied `is_applicable` flag.

The static `condition_aggregation` derived node therefore has a fixed dependency on at least:

```text
derived:effect_availability
selector:condition.applicability
```

The concrete DAG binds these to the specific target/Condition/application context.

If an immunity mechanic itself depends on the Condition's effective presence and creates a cycle, prospective activation rejects the cycle rather than selecting an evaluation order.

## 9. C8 — should `condition.applicability` be applied only to Condition definitions?

Yes.

The selector name and accepted `rule.immunity` semantics are about named Conditions. Generic Effect suppression/availability remains a separate derived stage. Applying `condition.applicability` to every `definition.effect` would collapse Condition semantics back into generic Effect availability.

This restriction is implementation/compiler binding, not another world-state field.

## 10. C9 — invocation facts and cache identity

The critic agrees that state-view identity alone is insufficient for an invocation-sensitive calculation.

Required invariant:

```text
MechanicalContext identity
    = pinned state-view identity
    + bound roles/arguments
    + accepted invocation-input fingerprint when invocation inputs are admitted
```

A state-only calculation naturally has an empty invocation-input component.

The fingerprint is not world authority. Step 3 already plans to preserve accepted adjudicated facts + provenance in Resolution/Continuation state; this correction tells Step 3 that those facts are part of deterministic calculation identity.

## 11. C10 — fact provenance should not become a canonical world fact automatically

A tempting overcorrection is to persist every accepted invocation fact into `world.lore_fact` or another canonical record so replay is always possible.

Rejected.

Most invocation facts are situational adjudications, not durable world truth. Step 3 must preserve them as fixed causal execution inputs where needed for suspension/idempotency/receipt. Step 4 may later promote genuinely durable truth through the lore/knowledge model.

This preserves the boundary:

```text
accepted invocation input != automatically canonical fiction
```

## 12. C11 — query results are sets unless order is part of the typed contract

The critic accepts the coverage clarification.

Runtime query APIs locate relevant owners/records. If several results are returned and the domain contract does not define mechanical order, the semantic result is an unordered set.

A stable serialization sort is allowed for trace/test reproducibility but cannot be consumed as a winner/selection rule.

Operations requiring non-commutative choice must invoke a registered comparator, rules-defined controller choice, or typed adjudication requirement.

No general `ORDER BY`/sort expression is exposed to declarative content.

## 13. C12 — scheduled triggers remain ordinary execution consumers

The new owner-local scheduled-trigger mechanism survives the read-boundary attack.

A due trigger does not receive:

- arbitrary Effect enumeration;
- a generic temporal query handle;
- campaign search;
- privileged LLM fact injection.

Step 3 constructs a child Activity/Resolution from the owning Effect and trigger declaration. That child uses the same registered fact/accessor/context contracts as any other Activity.

If a required invocation-adjudicated fact is unavailable when a due mechanic must execute, Step 3 must produce the appropriate typed suspension/adjudication path rather than fabricate the fact or skip the due mechanic.

## 14. C13 — potential concern: boolean-only context facts

Could future adjudicated inputs require numbers/enums (cover amount, approximate distance, improvised DC)? Yes.

The critic recommends **not** generalizing now.

Current predicate `{fact: id}` is boolean. Exact numeric mechanical inputs should normally be produced through a registered operation/typed Activity argument, not a free scalar fact channel. If a future concrete case proves a typed invocation fact is needed, the registry/value schema can be extended deliberately.

Initial boolean-only facts are therefore a feature, not a limitation to solve preemptively.

## 15. C14 — potential concern: selector metadata covers only reviewed Step-2 selectors

`core-catalog.json` has a larger selector inventory than `mechanical-surfaces.json`.

The critic does not require Slice D to fully seed structured metadata for every attack/save/damage selector. That is Step-6 catalog/seed closure.

However:

1. every `{fact: id}` must already resolve to a registered fact regardless of selector;
2. any selector with structured metadata must enforce its `allowed_input_classes`;
3. unstructured selectors must not be assumed state-safe merely because metadata is absent;
4. Step 6 must close structured selector coverage before final architecture/catalog closure.

This avoids turning assurance into a full seed implementation while protecting the state-sensitive Step-2 surfaces now.

## 16. Required machine/document corrections

The critic recommends the following bounded implementation package:

1. add `context_facts` metadata to `mechanical-surfaces.json` and its schema;
2. replace `derived_node_kinds` with structured `derived_nodes` metadata;
3. add `allowed_input_classes` to reviewed selector/derived-node metadata;
4. encode the static `condition_aggregation` dependency on `effect_availability` and `condition.applicability`;
5. add focused compile-contract tests proving unknown fact rejection and state-sensitive selector fact rejection;
6. update misleading `source.equipped` / `actor.can_act` examples to genuine fiction-adjudicated facts or engine accessors;
7. document explicit true/false/missing fact semantics and invocation-input cache fingerprint;
8. document unordered query-result semantics;
9. carry exact fact-value/provenance request schema into Step 3 rather than inventing it in Step 2.

## 17. Human decision analysis

Could this package reasonably require a human decision because it restricts homebrew expressiveness?

The critic says **no** for the current amendments.

The already-approved architecture says:

- LLM input is not mechanical authority;
- engine-owned facts cannot be supplied as adjudicated context;
- facts must be registered;
- persistent state has one reconstructable authority;
- dependency cycles are validated through typed contracts;
- arbitrary query/expression surfaces are forbidden.

Permitting unregistered/ephemeral facts to alter Resource capacity or current Condition effectiveness would contradict those decisions rather than represent a legitimate alternative product direction.

The correction therefore enforces existing product semantics; it does not choose new semantics.

A later proposal to let campaign authors define new invocation fact families, numeric fact types, or persist adjudicated fact state automatically would be a separate material design question.

## 18. Final critic recommendation

**AMEND / KEEP STEP 2 CLOSED.**

Use narrow input-capability metadata rather than a new calculation taxonomy.

No human decision required.

Confidence: **HIGH**.

What would change this verdict: a concrete rules case proving that one of the continuously state-derived Step-2 calculations must depend on an ephemeral LLM-only fact and cannot instead depend on canonical mechanical/world state or a materialized invocation result. No such case is currently known.
