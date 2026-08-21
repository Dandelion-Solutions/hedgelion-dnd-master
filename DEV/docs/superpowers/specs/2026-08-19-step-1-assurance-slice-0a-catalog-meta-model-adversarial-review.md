# Step 1 Retrospective Assurance — Slice 0A Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — CORRECTIONS REQUIRED, NO HUMAN GATE**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed:

- Slice 0A solution-blind Task Charter;
- Slice 0A coverage/research synthesis;
- current catalog contracts/inventory/machine catalogs/schemas;
- Step-2 Effect/Condition definition-instance semantics where they exercise the catalog boundary.

The critic assumes the current catalog model is wrong until each boundary survives a counterexample.

## 1. Verdict

The fundamental decomposition survives:

```text
engine capability / closed protocol vocabulary
reusable definition
world record
runtime record
embedded transient protocol value
```

No evidence justifies collapsing these into a generic Item/Entity/automation object.

However, the initial synthesis missed one **SIGNIFICANT machine-contract gap** and understated one criterion issue. None requires a new product/ownership decision; both are derivable from accepted class semantics.

## 2. Findings

### 0A-C1 — world-record `definition_id` compatibility is not an explicit contract

**Severity: SIGNIFICANT.**

The universal world envelope permits `definition_id` on every world kind. `entity-structures.json` records only a Boolean-like `requires_definition_id` for `world.effect`. Neither current schema nor maintenance audit defines which definition kinds are legal for a given world kind.

This is no longer safely inferable by name:

```text
world.actor  -> definition.actor_archetype
world.asset  -> definition.asset
world.effect -> definition.effect OR definition.condition
```

The last case proves that a simple `world.foo -> definition.foo` convention is false.

Without a closed compatibility contract, these structurally valid but semantically invalid objects can pass the universal envelope unless another ad-hoc loader branch rejects them:

```text
world.actor  definition_id = definition.asset.sword
world.effect definition_id = definition.actor_archetype.goblin
world.asset  definition_id = definition.condition.poisoned
```

Relying on runtime code to infer expected definition classes would create a second, non-catalog authority for the taxonomy.

**Required correction:** machine catalog metadata must declare, for each world kind, whether `definition_id` is forbidden, optional, or required and, when allowed, the closed set of compatible `definition.*` kinds. Schema/compiler validation must consume that mapping. `world.effect` explicitly accepts both `definition.effect` and `definition.condition`.

This correction makes an already accepted class relationship executable; it does not add a new class or change ownership.

### 0A-C2 — class-admission rule is important enough to be normative, not only guidance

**Severity: MODERATE.**

The initial synthesis correctly found the rule scattered. The critic raises its importance: without a canonical admission decision, future stages can create new records to solve local problems and slowly erode the catalog decomposition.

The contract must state that independent identity/lifecycle/reference need is the deciding criterion for record status, while reusable semantic identity is the deciding criterion for definitions and executable meaning is the deciding criterion for capabilities.

### 0A-C3 — protocol-value serialization does not imply protocol-value identity

**Severity: MODERATE.**

A Continuation/checkpoint may serialize a Signal, StateDelta, RollResult, or other typed value. That does not turn the embedded value into a `runtime.*` record. Its owning runtime record owns versioning/lifecycle/reference identity. If independent retry/reference/lifecycle later becomes necessary, promotion to a runtime record is an explicit architecture change.

### 0A-C4 — reusable definition kind does not force a same-named world instance kind

**Severity: MODERATE clarification.**

`definition.hazard` may describe a reusable poison/disease/curse/trap source, but a current disease on an Actor may be owned by Effect/Condition machinery rather than a `world.hazard`. Likewise, a reusable definition can be consumed by a procedure without ever producing a same-named world object.

The catalog should explicitly describe definition-to-world compatibility as a relation, not a naming convention.

## 3. Attacks that did not break the design

### Generic Item/Entity alternative

A generic object plus programmable automation is simpler in class count, but it displaces semantic boundaries into payload conventions and runtime interpretation. With LLM-authored content this is a worse safety/determinism trade-off. Rejected.

### Facets as behavior

Allowing facets to grant mechanics would reduce definition payload duplication but create hidden executable meaning in classification/search metadata. Rejected.

### Every typed value gets an ID

This would simplify universal tracing but create identity/lifecycle overhead for values whose only owner is a Resolution/Continuation/trace. Rejected.

### Every definition gets a matching world kind

This fails immediately for Conditions, Activities, Resources, and many vocabulary definitions. Runtime instance kinds must follow independent state/lifecycle, not definition taxonomy. Rejected.

## 4. Cross-system impact

The compatibility mapping directly protects Step 2:

- a Condition application remains a `world.effect` while referencing `definition.condition`;
- Actor/Asset Resource definitions stay referenced from their owners rather than being mistaken for world records;
- transformations can validate source/target definitions against world-kind compatibility;
- later promotion/migration can reject a redefinition that would change the semantic class behind a durable world reference.

It also constrains Step 3 binder behavior: deterministic binding validates IDs **and their compatible kinds**, not mere existence.

## 5. Resolution recommendation

Apply C1–C4 mechanically, add focused negative tests, rerun maintenance/schema tests, then repeat a short critic pass.

Recommendation: **AMEND WITHOUT REOPENING STEP 1**.

Human decision required: **NO**.

Confidence: **HIGH**.
