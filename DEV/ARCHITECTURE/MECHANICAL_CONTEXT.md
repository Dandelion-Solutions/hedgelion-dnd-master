# MechanicalContext Accessors, Invocation Facts and Dependency Graph

Status: **CANONICAL S6D-04 OWNER**

## 1. Authority and scope

This document owns the supported MechanicalContext accessor contract, the bounded invocation-fact registry semantics, the derived mechanical-stage contract and the single dependency-graph law for the v2.0.0-generation supported profile.

It closes S6D-04. It does not own:

- Calculation Selector operation/result/combination policy, owned by `CALCULATION_SELECTOR_METADATA.md`;
- portable invocation-fact/Activity envelope member design, owned by S6D-05;
- Activity primitive behavior, owned by S6D-06;
- valued-Condition rules meaning, owned by S6D-08;
- seed activation evidence, owned by S6D-07–09;
- runtime domain-query APIs;
- resume/checkpoint/GC/reconstruction protocols.

Machine authority is split without duplication:

- `core-catalog.json#/registries/mechanical_accessors` owns the exact accessor ID set;
- `mechanical-surfaces.json#/accessors` owns accessor metadata;
- `mechanical-accessor-ref.schema.json` owns serialized accessor-reference shapes;
- `mechanical-surfaces.json#/context_facts` is the bounded exact fact-ID registry;
- `mechanical-surfaces.json#/derived_nodes` is the bounded exact internal derived-node registry.

Facts and internal node IDs are not copied into `core-catalog.json`; duplicate registries would create competing admission authority.

## 2. Non-negotiable laws

1. Accessors, invocation facts and runtime domain queries are distinct surfaces.
2. Every accessor reads ENGINE_STATE from one pinned committed or prospective state view.
3. Engine-owned state never enters through adjudicated invocation facts.
4. Missing invocation input is not false. Negation cannot manufacture evidence.
5. A source/input class is not exact fact-ID permission.
6. Registry permission and bound compiled-consumer permission are both required.
7. One evaluation graph includes selectors, accessors and derived nodes plus bound predicate/definition edges.
8. If acyclicity cannot be proven, validation fails. No fixed point, iteration-to-stability or evaluation-order fallback exists.
9. Runtime queries remain infrastructure-only, nonserializable and unavailable to content.
10. Derived indexes, MechanicalContext objects and DAG caches are disposable, never recovery authority.
11. Cache identity includes catalog context, pinned state view, bindings and any accepted-fact fingerprint actually permitted by the consumer.
12. Resume rebuilds/re-pins derived context; accepted facts remain fixed only while their accepted work is live.
13. Portable envelope realization remains S6D-05 even where S6D-04 specifies semantic retention requirements.

## 3. Dispositions

### 3.1 Accessors

Nine accessors are `ACTIVE_ADMITTED`:

- `health.current`
- `health.temporary`
- `health.maximum`
- `health.bloodied`
- `life.state`
- `condition.present`
- `resource.capacity`
- `resource.available`
- `owner_effect.parameter`

`condition.value` is `DORMANT_RESERVED`. Its identity and narrow shape remain registered, but compiled content must reject it until S6D-08 supplies one accepted valued-Condition aggregation contract. Dormancy is not absence, activation or a default aggregation choice.

### 3.2 Invocation facts

`fiction.target_visible` and `fiction.target_reachable` are `DORMANT_RESERVED`.

Accepted architecture proves the bounded boolean capability, but current repository evidence contains structural examples rather than an exact admitted compiled consumer. They remain nonselectable until S6D-07–09 names such a consumer and its exact binding/permission. This does not remove the capability or decide seed mechanics.

### 3.3 Derived nodes

All four internal stages are `ACTIVE_INTERNAL`:

- `effect_availability`
- `effect_arbitration`
- `condition_aggregation`
- `condition_intrinsic`

All currently admit ENGINE_STATE only and no invocation fact IDs. The prior class-only `INVOCATION_ADJUDICATED` allowance on `condition_intrinsic` had no permitted exact fact and no path to a selectable selector; it is removed as authority laundering. A future relational mechanic requires an exact reviewed consumer and selector/input path.

## 4. Accessor contracts

All bound role names resolve through the enclosing compiled definition/invocation binding table. A syntactically valid role string is not authority.

| ID | Result | Arguments/binding | Missing behavior | Dependencies |
|---|---|---|---|---|
| `health.current` | integer | explicit `subject`, Actor | typed hydration/materialization required | none |
| `health.temporary` | integer | explicit `subject`, Actor | typed hydration/materialization required | none |
| `health.maximum` | integer, minimum 1 by selector | explicit `subject`, Actor | typed hydration/materialization required | `selector:health.maximum` |
| `health.bloodied` | boolean | explicit `subject`, Actor | propagate typed hydration failure | `accessor:health.current`, `accessor:health.maximum` |
| `life.state` | registered LifeState ID | explicit `subject`, Actor | typed hydration/materialization required | none |
| `condition.present` | boolean | `subject` + `condition_definition` | false only when the named definition is valid and no effective application exists | `derived:condition_aggregation` |
| `condition.value` | scalar/enum/absent, dormant | `subject` + `condition_definition` | absent only after valid aggregation proves no effective value | `derived:condition_aggregation` |
| `resource.capacity` | nonnegative integer | `subject` + `resource_definition`, Actor/Asset | typed hydration/materialization required | `selector:resource.capacity` |
| `resource.available` | nonnegative integer | `subject` + `resource_definition`, Actor/Asset/procedure-bound storage | typed hydration/materialization required | `accessor:resource.capacity` |
| `owner_effect.parameter` | declared scalar | explicit `parameter_definition`; implicit current owner Effect application | illegal/missing owner binding or undeclared parameter is validation failure | none |

False/zero/absent are domain values only where the row explicitly permits them. Unknown definition IDs, wrong subject kinds, missing bound roles and unavailable authoritative records are not those values.

### 4.1 Exact derivations

`health.bloodied` is:

```text
current * 2 <= maximum
```

Both reads use the same pinned view. No Actor `bloodied` flag exists.

`resource.capacity` and `resource.available` are integers in the supported profile, aligned with the active `resource.capacity` selector. They abstract physical `current` versus `spent` storage and do not expose raw state fields.

`owner_effect.parameter` cannot name another Effect. The owner application is an implicit compiler/runtime binding, and `parameter_id` must resolve through that owner's accepted definition.

## 5. Consumer permission

Registry metadata admits only these consumer kinds:

- closed `mechanical_predicate`;
- another registered accessor;
- an internal registered derived node.

This is a ceiling, not a wildcard grant. `permitted_consumer_ids` is the exact
registry/bound-consumer allowlist and is checked before evaluation. The current
fixed matrix is:

| Producer | Exact current consumers |
|---|---|
| `health.current` | `accessor:health.bloodied` |
| `health.maximum` | `accessor:health.bloodied` |
| `resource.capacity` | `accessor:resource.available` |
| every other accessor | none until an exact compiled consumer is admitted |
| both dormant facts | none |
| derived nodes | the fixed consumers in §7 |

Every concrete predicate/definition occurrence has a stable compiled consumer
ID. A dynamic consumer must be added to the producing item's exact allowlist
through its owning seed/domain closure; an explicit reference in an AST does
not grant itself permission. Binding subject/definition/owner/view compatibility
is checked in addition to exact ID.

Static accessor and node dependencies are exact prefixed IDs. Their inverse consumer edges are recorded in derived-node metadata where fixed. Dynamic definition consumers never become global class-wide allowlists.

Dormant IDs fail compiled-content validation even if their JSON shape is syntactically valid.

## 6. Invocation fact contract

For both reserved facts:

```text
producer                 HOST_LLM_BOUNDARY
acceptance authority     ACTIVITY_INVOCATION_VALIDATOR
value                    boolean
occurrence scope         one Activity/Resolution invocation generation
bindings                 exact roles required by the compiled consumer
provenance               stable reference + fingerprint required
missing                  typed missing-input/adjudication result
retention                fixed causal input while accepted work is live
portable owner           DEV/SCHEMAS/invocation-fact.schema.json / S6D-05
```

Three states remain distinct:

```text
accepted true
accepted false
missing / not accepted
```

An optional `BoundaryOccurrence` reference is retained only when that
invocation was actually produced by a reached boundary; it is not universal
fact identity.

Acceptance requires all of:

1. registered active fact ID;
2. exact compiled consumer permission;
3. occurrence and binding match;
4. accepted provenance;
5. compatible pinned `ResolvedCatalogContext`.

The current two IDs fail item 1 because they are dormant. S6D-04 defines their semantics but does not activate or redesign their portable envelope.

Facts never become world truth merely through use. Step 3 retains accepted values and provenance across continuation/retry; Step-5.13 may collect them after no live retry/resume/idempotency edge requires them.

## 7. Derived-node contracts

| Node | Result role | Fixed dependencies | Fixed consumers |
|---|---|---|---|
| `effect_availability` | eligible Effect member set | none | `effect_arbitration`, `condition_aggregation` |
| `effect_arbitration` | winning/participating Effect member set | `effect_availability` | bound runtime collection |
| `condition_aggregation` | effective named-Condition aggregate | `effect_availability`, `selector:condition.applicability` | `condition.present`, dormant `condition.value`, `condition_intrinsic` |
| `condition_intrinsic` | intrinsic Rule Element set | `condition_aggregation` | bound Rule Element collection |

All propagate typed dependency failure. All are evaluated in the pinned view. Their caches are disposable and keyed by view, catalog and bindings. No node has a permitted invocation fact.

`condition.value` dormancy does not deactivate `condition_aggregation`: presence-only Conditions and intrinsic mechanics still require the aggregate/member-set stage.

## 8. One dependency graph

### 8.1 Registry graph

Registry metadata supplies:

- node kind and ID;
- allowed dependency kinds;
- static exact edges;
- allowed input classes;
- exact fact IDs;
- state-view and cache policy.

### 8.2 Bound-instance graph

Compilation/hydration adds:

- concrete Rule Element/predicate nodes;
- source, target, owner-Effect, Resource and Condition bindings;
- definition references;
- prospective activation/delta edges;
- exact consumer occurrence identity.

The validation scope is the hydrated/prospective mechanical closure for the affected actors/assets/effects/resources/procedure. If a required referenced definition or bound edge is unavailable, acyclicity is unproven and validation fails.

Canonical rejected shapes include:

```text
selector:health.maximum(subject)
 -> bound effect predicate
 -> accessor:health.bloodied(subject)
 -> selector:health.maximum(subject)
```

and:

```text
selector:resource.capacity(subject,R)
 -> bound effect predicate
 -> accessor:resource.available(subject,R)
 -> selector:resource.capacity(subject,R)
```

Cross-effect and cross-resource binding does not evade rejection.

### 8.3 Transitive input proof

For every consumer, the union of input classes and fact IDs reachable through its bound closure must be a subset of the consumer's own permissions. A derived node with class permission but no exact fact permission cannot carry that fact. There is one graph for cycle and input-authority validation.

## 9. State view, cache and recovery

A context identity contains:

```text
ResolvedCatalogContext identity
pinned committed/prospective view identity
bound roles and definition/application IDs
relevant native record revisions
accepted fact fingerprint, only when permitted
```

A prospective view is an immutable evaluation overlay owned by the current Resolution. It is not trusted after suspension. After expected child work or revision change, Step 3 revalidates native revisions and rebuilds/re-pins MechanicalContext.

Checkpoint/recovery hydrates authoritative native state and accepted work; it does not restore MechanicalContext, DAG caches, Condition indexes or prospective deltas as authority. GC retains facts/receipts/fingerprints only while live accepted-work edges require them. Reconstruction must use the compatible pinned catalog context required by S6D-01.

## 10. Missing and failure mapping

| Situation | Result |
|---|---|
| accepted boolean false | false |
| fact absent | typed missing-input/adjudication |
| fact dormant/unknown/unauthorized | compile or invocation validation failure |
| engine value supplied as fact | reject as unauthorized authority |
| valid named Condition with no effective application | `condition.present = false` |
| dormant `condition.value` use | compile validation failure |
| missing Actor HP/LifeState/Resource authority | typed hydration/materialization requirement |
| missing bound role/definition | binding/validation failure |
| undeclared owner Effect parameter | binding/validation failure |
| stale occurrence/view/catalog identity | currentness/compatibility failure |
| incomplete graph or cycle | definition/prospective compilation failure |

Existing Step-3 dispositions/failure owners remain authoritative; this document does not mint a parallel top-level error taxonomy.

## 11. Runtime-query exclusion

Runtime may use bounded indexes/read models to locate relevant Effect applications, Resources, temporal bindings, occurrences and accepted work. These facilities:

- are host capabilities, not catalog values;
- are absent from Rule Element/predicate/accessor schemas;
- cannot be serialized in content;
- default to unordered-set semantics unless an owning query contract states order;
- do not copy derived lists into Actor authority.

No generic duration/recovery/world-search accessor is admitted.

## 12. Verification and maintenance

Machine verification must prove:

- exact 10-ID equality among core registry, accessor metadata and accessor-ref branches;
- exact two-fact/four-node registry sets;
- item metadata/schema validation;
- `condition.value` and both facts remain dormant/nonselectable;
- all derived nodes are ENGINE_STATE-only with empty exact fact permissions;
- accessor dependency targets resolve;
- `resource.capacity/available` integer alignment;
- owner-Effect implicit binding;
- missing-not-false behavior;
- canonical health/resource cycle rejection;
- no query syntax in serializable predicate/accessor surfaces;
- S6D-03 selector restrictions remain unchanged.

Activation of any dormant item requires its named downstream owner, exact consumer evidence, synchronized metadata/schema/tests and the same whole-project review discipline.

