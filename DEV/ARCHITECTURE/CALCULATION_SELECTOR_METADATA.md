# HDM Calculation Selector Metadata

Status: **ACCEPTED S6D-03 ARCHITECTURE OWNER**

Date: 2026-08-25

## 1. Decision

S6D-03 initially admitted three Calculation Selectors and two `rule.*` operations. S6D-07 then admitted a deliberately finite extension; it did not reopen the selectability law.

The current exact executable roster is ten selectors:

- `health.maximum`, `resource.capacity`, `condition.applicability`;
- `check.roll`, `attack.roll`, `save.roll`, `spell.dc`;
- `defense.armor_class`, `damage.received`, `healing.received`.

The current exact executable operation roster is:

- `rule.add_flat`;
- `rule.grant_advantage`;
- `rule.immunity`.

The active roster is closed by the coordinated current `mechanical-surfaces.json` and admission ledger: 10 of 34 selectors and 3 of 26 operations are `ACTIVE_ADMITTED`; the remaining 24 selectors and 23 operations remain `DORMANT_NONSELECTABLE`. No core ID is added or removed.

Canonical semantic owner after acceptance: `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`. The S6D-07 extension is admitted only where the current ledger names its exact completed downstream owner and the current machine metadata supplies the complete contract.

## 2. Selectability law

A selector is selectable only when all are true:

1. exact core registration;
2. current canonical supported mechanic;
3. complete machine metadata;
4. every allowed operation has an independently proved closed pair contract;
5. required value semantics are closed at the S6D-03 boundary;
6. required fact IDs/dependencies are explicit or empty;
7. coordinated admission-ledger verification passes.

Structural examples, historical proposals and generic rules relevance do not satisfy this law.

## 3. Required metadata

Every selectable selector has:

- allowed operations;
- exactly matching operation-contract keys;
- contribution and result types;
- result constraints;
- subject kinds and binding kinds;
- allowed dependency kinds;
- allowed input provenance classes;
- exact permitted context-fact IDs;
- architecture-fixed static dependency references;
- closed combination policy;
- selector-metadata resolution owner;
- provenance-retaining trace policy.

Unknown members fail.

## 4. Active contracts and S6D-07 extension

### 4.1 Health maximum

```text
selector: health.maximum
subject: world.actor
binding: subject
base: accepted Actor/build maximum
operation: rule.add_flat
value: finite integer
result: integer >= 1
policy: integer_additive_v1
inputs: ENGINE_STATE
facts: []
dependencies: accessor | derived; static []
```

### 4.2 Resource capacity

```text
selector: resource.capacity
subject: world.actor | world.asset
bindings: subject + resource_definition
base: definition/resource owner capacity
operation: rule.add_flat
value: finite integer
result: integer >= 0
policy: integer_additive_v1
inputs: ENGINE_STATE
facts: []
dependencies: accessor | derived; static []
```

### 4.3 Condition applicability

```text
selector: condition.applicability
subject: world.actor
bindings: subject + condition_definition
base: applicable
operation: rule.immunity
value: literal true
result: boolean
policy: immunity_any_true_v1
inputs: ENGINE_STATE
facts: []
dependencies: accessor | derived; static []
```

### 4.4 S6D-07 exact extension

The seven added selectors are limited to the current character-MVP consumers: `check.roll`, `attack.roll`, `save.roll`, `spell.dc`, `defense.armor_class`, `damage.received` and `healing.received`. Their exact subject/binding shapes, allowed operation pairs, result constraints and closed combination policies are the current machine metadata. They do not authorize any extra selector, arbitrary fact input, query path or operation.

`attack.roll` admits only `rule.add_flat` and `rule.grant_advantage`; `rule.grant_disadvantage` remains dormant/nonselectable and is not a legal executable pair.

## 5. Policy semantics

### `integer_additive_v1`

1. evaluate legal predicates/gates against one pinned state view;
2. retain applicable finite-integer Contributions as a multiset;
3. sum them commutatively;
4. add the sum to the authoritative base;
5. enforce the selector's declared minimum;
6. retain every accepted/rejected source and reason.

No rounding, override, min/max contribution, multiplication or list-order rule exists in this policy.

### `immunity_any_true_v1`

Any applicable literal-true immunity vetoes condition application. Duplicate true vetoes coalesce semantically while each provenance remains traceable.

## 6. Inputs and dependencies

All selectable selectors admit only `ENGINE_STATE`.

`permitted_context_fact_ids` is exactly empty. A provenance class is not treated as a fact allowlist.

Dependency kinds are only `selector|accessor|derived`. Exact references retain their prefix. Current selectors allow `accessor|derived` and have no architecture-fixed static reference. Every inherited `derived_nodes[*].allowed_dependency_kinds` is normalized to the same closed kind enum; exact node identities occur only in prefixed `dependencies`. S6D-04 closed the inherited `condition_intrinsic` gap as ENGINE_STATE-only with no exact invocation-fact permissions. S6D-04 owns exact accessor/fact graph closure and transitive binding checks.

No generic query, property path, callback, author phase/order, fixed-point semantics or ambient LLM fact access is introduced.

## 7. Dormant boundary

`resource.recovery` and `effect.duration`, though reserved by accepted Step-2 architecture, are dormant because their mode/unit/value compatibility is not closed. The same applies to cost, damage, activity restriction and other portable-shape-dependent pairs.

S6D-05 may define payload members but cannot silently activate a selector/operation. Activation requires a concrete canonical mechanic, complete S6D-03 pair semantics and coordinated catalog verification.

## 8. Structural examples

Current D&D condition tests and JSON-Schema examples validate structural definition shapes only. They are not executable selector consumers. Catalog-aware verification must reject their dormant selector/operation pairs until activation.

## 9. Failure/trace contract

Catalog-aware validation rejects unknown/dormant IDs, illegal pairs, invalid values, subject/binding violations, nonempty unauthorized fact references, illegal dependency kinds/references and cycles.

The Resolution trace retains selector, operation, source, predicate/gate result, normalization, acceptance/rejection reason and final policy. Existing catalog/execution failure envelopes remain owners; no new top-level failure ID is introduced.

## 10. Coordinated change set

- add `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`;
- complete `mechanical-surfaces.json` for the current ten selectors;
- tighten `mechanical-surfaces.schema.json`;
- update admission ledger and `CATALOG_ADMISSION.md`;
- route `RULE_ELEMENT_MODEL.md` to the new owner;
- add focused S6D-03 verification;
- update S6D-02 totals test;
- explicitly classify structural selector examples in tests/schema documentation;
- update PROJECT_MAP, roadmap and dated Steps 2–8 evidence.

## 11. Verification

Prove:

- 34/26 ledger equality;
- active sets exactly 10/3;
- metadata keys equal active selector ledger IDs;
- allowed-operation union equals active operation ledger IDs;
- contract keys equal allowed operations;
- schema validation and closed fields;
- current coordinated 481/35/68 disposition totals after the admitted S6D-07 extension;
- every dormant entry has a trigger;
- no active selector admits invocation facts;
- exact fact allowlists are empty;
- dependency kinds are type names, not node IDs, across selectors and every derived node;
- additive policy is order-independent and respects minima;
- immunity policy is monotone and duplicate-safe;
- structural examples using dormant pairs fail catalog-aware validation;
- no S6D-04/05 scope theft.

## 12. Downstream

S6D-04 is canonically closed by `DEV/ARCHITECTURE/MECHANICAL_CONTEXT.md`.

## Canonical authority

This document owns selector selectability, selector/operation semantic compatibility, active combination policies, subject/binding restrictions and the selector-side dependency/input boundary. It does not own portable payload members, Activity primitives, seed content or the complete MechanicalContext graph.

