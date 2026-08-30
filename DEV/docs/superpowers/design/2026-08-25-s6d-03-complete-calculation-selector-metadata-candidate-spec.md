# S6D-03 — Complete Calculation Selector Metadata — Candidate Specification

Status: **STEP 5 CANDIDATE — REPAIRED / PENDING FINAL ADVERSARIAL REVIEW**

Date: 2026-08-25

## 1. Decision

Exactly three Calculation Selectors are selectable:

- `health.maximum`;
- `resource.capacity`;
- `condition.applicability`.

Exactly two `rule.*` operations are executable through those selectors:

- `rule.add_flat`;
- `rule.immunity`.

All other 31 registered selectors and 24 operations remain `DORMANT_NONSELECTABLE`. No core ID is added or removed.

Canonical semantic owner after acceptance: `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`.

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

## 4. Active contracts

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

Dependency kinds are only `selector|accessor|derived`. Exact references retain their prefix. Current selectors allow `accessor|derived` and have no architecture-fixed static reference. Every inherited `derived_nodes[*].allowed_dependency_kinds` is normalized to the same closed kind enum; exact node identities occur only in prefixed `dependencies`. The existing `condition_intrinsic` invocation-adjudicated input remains an explicitly unresolved S6D-04-owned graph obligation, not an S6D-03 selector permission. S6D-04 owns exact accessor/fact graph closure and transitive binding checks.

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
- complete `mechanical-surfaces.json` for three selectors;
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
- active sets exactly 3/2;
- metadata keys equal active selector ledger IDs;
- allowed-operation union equals active operation ledger IDs;
- contract keys equal allowed operations;
- schema validation and closed fields;
- 450/35/86 disposition totals;
- every dormant entry has a trigger;
- no active selector admits invocation facts;
- exact fact allowlists are empty;
- dependency kinds are type names, not node IDs, across selectors and every derived node;
- additive policy is order-independent and respects minima;
- immunity policy is monotone and duplicate-safe;
- structural examples using dormant pairs fail catalog-aware validation;
- no S6D-04/05 scope theft.

## 12. Downstream

S6D-04 Step 1 is next after canonicalization and is not started.
