# S6D-03 — Complete Calculation Selector Metadata — Architecture Task Brief

Status: **STEP 1 COMPLETE — STEP 2 NOT STARTED**

Date: 2026-08-25

Authoritative preparation ref: `v1/engine-rearchitecture@f01e30e5560e790449153ad6c7b1aeeef00b5eed`

Program inputs:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Predecessors:

- S6D-01 closed exact ruleset/package/catalog identity;
- S6D-02 closed catalog admission and routed selector/operation realization to S6D-03.

Whole-project brief critic: `DEV/docs/superpowers/specs/2026-08-25-s6d-03-complete-calculation-selector-metadata-brief-critic.md`.

This artifact frames only S6D-03 Step 1. It does not perform selector-by-selector activation decisions, change catalog/schema/test/runtime files, begin S6D-04, or resume R2.7.

---

## 1. Current problem

HDM has 34 registered Calculation Selector IDs and 26 registered `rule.*` operation IDs. S6D-02 proved that registration is not executable support:

- five selectors are currently materialized in `DEV/CATALOG/mechanical-surfaces.json`;
- seven operations are currently consumed by those selectors;
- twenty-nine selectors and nineteen operations are `DORMANT_NONSELECTABLE` with S6D-03 activation gates;
- all ten MechanicalContext accessors are active but their complete metadata and dependency-graph closure belong to S6D-04.

For every selector that remains or becomes selectable, S6D-03 must define enough exact metadata to validate Rule Elements deterministically:

- contribution and resolved-result type;
- legal `rule.*` operations;
- selector/operation compatibility contract at the S6D-03 boundary;
- legal dependency kinds;
- legal input provenance classes;
- subject and binding restrictions where applicable;
- architecture-fixed static dependency edges;
- deterministic combination/resolution-policy ownership.

The current five-selector machine surface is only a partial realization. Conversely, dormant selector names appearing in old examples, schemas or design prose are not proof that the supported profile needs them. Step 2 must reconcile actual rules/seed consumers, accepted mechanics owners, machine metadata, schemas, examples and tests without laundering provisional vocabulary into support.

Registry equality means equality between **selectable** selectors and complete machine metadata. It does not require all reserved dormant IDs to become selectable.

---

## 2. Goal

Produce a decision-ready selector architecture and evidence set that:

1. accounts for all 34 registered selectors and 26 operations while preserving S6D-02 admission dispositions until evidence justifies a change;
2. identifies the minimum selector surface required by the supported D&D 2024 / SRD 5.2.1 profile and accepted HDM mechanics;
3. gives every selectable selector a complete, typed, machine-validatable metadata contract;
4. gives every legal selector/operation pair an exact value contract and deterministic resolver owner;
5. separates selector calculation, MechanicalContext reads, Activity execution, runtime domain queries and LLM-adjudicated invocation facts;
6. preserves provenance, subject/binding and dependency legality without creating a generic query language;
7. rejects cycles and hidden evaluation-order/fixed-point semantics;
8. removes or keeps nonselectable any selector/operation lacking current supported evidence;
9. routes accessor/fact graph details to S6D-04, portable value shapes to S6D-05, Activity primitives to S6D-06, seed content to S6D-07–09 and package verification to S6D-11;
10. leaves zero unresolved contradiction among selector owners, catalog metadata, Rule Element schemas, supported examples and tests.

---

## 3. Scope

### In scope

- all `core-catalog.json#/registries/rule_selectors` IDs;
- all `core-catalog.json#/registries/rule_operations` IDs insofar as selector legality/value contracts require them;
- selector entries in `mechanical-surfaces.json` and their schema;
- Rule Element contribution/result typing and selector-operation validation;
- resolver/combination policy ownership and determinism;
- selector subject kinds, binding restrictions and applicability;
- selector-visible dependency kinds, input classes and architecture-fixed static edges;
- selector activation evidence from supported mechanics/seed requirements;
- contradictions in schemas, examples, tests, prose owners and runtime consumers;
- exact downstream boundaries with S6D-04/05/06/07–09/11;
- focused verification and maintenance-audit requirements.

### Out of scope

- implementing the selector evaluator or compiler;
- completing MechanicalContext accessor/fact metadata or building its full graph (S6D-04);
- defining portable protocol-value payloads not required to settle selector metadata (S6D-05);
- defining Activity primitive contracts (S6D-06);
- authoring character/spell/monster/equipment seed content (S6D-07–09);
- package manifest/lock/builder/loader implementation (S6D-11);
- generic runtime domain-query APIs;
- arbitrary expression languages, callbacks, executable code or global repository queries;
- gameplay/campaign bootstrap;
- reopening S6D-01/S6D-02 or accepted Step-2 ownership without concrete contradiction or unsatisfied consumer.

---

## 4. Inherited invariants

1. Rule Elements are embedded pure Contributions; they do not mutate state or invoke Activities.
2. A Calculation Selector is a registered calculation surface, not a property path, search expression or runtime query.
3. Selector, accessor and runtime-query responsibilities remain non-overlapping.
4. Registration alone does not imply selectability.
5. A dormant ID stays nonselectable until its exact activation trigger is proved and machine metadata is complete.
6. Rule Element `operation_id`, `selector` and `value` are validated against the exact resolved catalog context.
7. Legal input provenance is explicit. Engine-owned state and bounded invocation-adjudicated facts are distinct; missing is not false.
8. Invocation-adjudicated input cannot be introduced transitively through a dependency that forbids it.
9. Dependencies retain typed identity (`selector:`, `accessor:`, `derived:`) and mechanically relevant graphs are acyclic.
10. There is no hidden fixed-point engine or author-controlled evaluation order.
11. Combination/resolution behavior is deterministic and owned by the selector/resolver contract, not JSON/list order.
12. Provenance and reasons survive contribution acceptance/rejection into the Resolution trace boundary.
13. Effect arbitration/lifecycle and Activity execution do not become selector combination policy.
14. House rules and LLM rulings cannot create same-ID overrides, new executable operations or unregistered selector authority.
15. The exact machine catalog remains ID authority; S6D-03 owns realization metadata, not package identity or catalog admission history.
16. Whole-project conflicts are resolved at the actual owner: change the S6D-03 candidate when an accepted owner governs, and seek a human decision only if accepted owners remain materially incompatible.

---

## 5. Mandatory Source Manifest and dependency subgraph

Step 2 must start from the current remote ref and refine a role-labelled Source Manifest.

### Process, sequencing and predecessor owners

- `AGENTS.md`;
- both design-process owners;
- `DEV/PROJECT_MAP.md`;
- current roadmap;
- S6D owner decision, parent Task Brief and plan;
- S6D-01 and S6D-02 canonical owners and full review chains.

### Selector and Rule Element owners

- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- current accepted Step-2 mechanical-state and selector/query designs;
- Step-2 assurance/resolution artifacts that supersede provisional statements;
- current execution boundary and Resolution/Continuation owners;
- House Rules and adjudication owners where invocation facts or rulings touch calculations.

### Machine surfaces and schemas

- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- `DEV/CATALOG/catalog-admission-ledger.json`;
- selector, Rule Element, mechanical predicate, accessor-ref, effect/resource/activity and definition schemas;
- examples embedded in schemas;
- catalog/schema validation tools and focused tests.

### Domain consumers

Trace actual supported calculations through the owning Actor/Asset/Resource/Effect/Condition/Duration/Recovery/Activity contracts and:

- `GAME/CORE/MECHANICS_INTEGRITY.md`;
- combat, magic, exploration, dialogue, advancement, character readiness and rewards;
- `GAME/RULES/` and exact supported-package/seed evidence;
- accepted rules examples and adversarial cases;
- recovery/retention consumers where a calculation is required by resumable accepted work.

### Historical and derivative evidence

Historical proposals and earlier inventories may explain an ID but cannot prove current selectability. Record supersession/applicability explicitly, especially for examples that use dormant IDs.

### Whole-project search obligations

For each of the 34 selectors and 26 operations:

- search current owners, schemas, examples, tests, catalog content and runtime branches;
- classify every hit as canonical, accepted requirement, machine realization, test/example, derivative, historical or stale;
- distinguish a concrete supported mechanic from a spelling example;
- follow indirect consumers through definitions, Effects, Resources, Activities, rules packages and recovery;
- record negative results only after the relevant owner route and repository boundary were checked.

---

## 6. Required Step-2 evidence products

### 6.1 Selector evidence ledger

For every selector:

```text
Selector ID:
S6D-02 disposition:
Current machine metadata:
Canonical semantic owner:
Supported mechanic/definition/consumer:
Supported-profile applicability:
Contribution type:
Resolved-result type:
Legal operations:
Operation-specific value contracts:
Legal dependency kinds:
Legal input provenance classes:
Subject kinds/binding restrictions:
Static dependency edges:
Combination/resolution policy owner:
Trace/provenance requirements:
Activation decision:
Exact evidence:
Contradictions/stale references:
Confidence and revisit trigger:
```

### 6.2 Operation evidence ledger

For every one of the 26 registered operations, including operations with no currently claimed legal selector pair:

```text
Operation ID:
S6D-02 disposition:
Registration/current machine state:
Canonical semantic owner:
All references/consumers and evidence class:
Supported-profile applicability:
Value family and semantic constraints:
Candidate selector pairs, if any:
Realization state:
Activation, continued-dormancy or stale decision:
Machine destination:
Contradictions/stale references:
Exact evidence and revisit trigger:
```

The operation-ledger ID set must equal `core-catalog.json#/registries/rule_operations`. An operation cannot evade disposition merely because no current selector claims it.

### 6.3 Operation compatibility matrix

For every selector/operation pair that is legal or claimed by current content:

```text
Selector:
Operation:
Input/value schema:
Contribution normalization:
Combination/conflict behavior:
Result-type compatibility:
Identity/stacking/arbitration relevance:
Failure on invalid value/pair:
Canonical owner:
Machine destination:
Verification case:
```

The matrix must prove absence of globally legal operations. Legality is selector-specific.

S6D-03 owns the **compatibility contract** for a selector/operation pair: nominal value-kind reference, semantic/range/unit/cardinality constraints, normalization behavior and compatibility with the contribution and resolved-result types. S6D-05 owns portable serialized payload schemas and their member-level realization. Every pair must point to an exact existing value owner or a precise S6D-05 obligation. S6D-03 must not invent portable payload members or claim an unresolved portable shape complete.

### 6.4 Supported-mechanics coverage map

Trace supported rules cases from domain owner and definition/content requirement to selector, operation, required inputs and resolver. This map proves activation; generic D&D familiarity, registry presence or an example alone does not.

### 6.5 Dependency/input legality ledger

For each selectable selector record direct dependency kinds, static edges, allowed input classes and transitive restrictions. Identify the S6D-04 facts/accessors it requires without defining their full contracts.

### 6.6 Cross-surface mismatch ledger

Record conflicts among:

- core registration and admission ledger;
- machine metadata and schema;
- Rule Element model/schema/examples;
- current tests and supported selectability;
- accepted Step-2 designs and later canonical owners;
- runtime/domain consumers and package/seed evidence.

Each mismatch gets an owner and disposition. Editing only one surface is not closure.

### 6.7 Verification matrix

Define executable checks for:

- selectable selector registry equals metadata registry;
- dormant selectors/operations cannot validate or execute;
- every selector metadata object is complete;
- operation evidence-ledger IDs equal all 26 registered operation IDs;
- every legal operation belongs to the registered operation set;
- operation/value/result compatibility;
- subject and binding restrictions;
- input/provenance legality including transitive rejection;
- dependency-kind and static-edge legality;
- cycle rejection;
- deterministic combination independent of serialized order;
- invalid selector/operation/value typed failure;
- no generic query/callback/code surface;
- exact synchronization of changed schemas/examples/tests/docs.

---

## 7. Questions Step 2 must answer

1. Which of the 29 dormant selectors are required by concrete supported-profile mechanics?
2. Which old schema/test examples are actual supported cases and which are illustrative or stale?
3. Are the five active selectors already complete against every required metadata field, or only structurally present?
4. What exact distinction exists between contribution type, operation value type and resolved result type?
5. Which operations are polymorphic, and where is their selector-specific value contract owned?
6. Does any registered operation lack a supported selector consumer and therefore remain dormant or become stale?
7. Which selectors require a subject, target, owner-effect binding or other typed binding restriction?
8. Which calculations may consume direct authority, derived mechanical state or invocation-adjudicated facts?
9. Which permissions must propagate transitively through selector/accessor/derived dependencies?
10. Which static edges are architecture-fixed and which arise only from a validated definition instance?
11. What minimum metadata proves cycle safety without introducing a second query/evaluation engine?
12. Who owns combination for flat modifiers, dice, advantage/disadvantage, min/max, override, multiplication, damage components, resistances and other supported operation families?
13. How are noncommutative or competing operations ordered without JSON/list-order authority?
14. How are provenance, stacking keys, predicates and reasons retained without making them combination owners?
15. Which failure distinctions belong to catalog compilation, definition validation, invocation preparation and runtime resolution?
16. Do current Rule Element and mechanical-surface schemas express the full accepted contract?
17. Which S6D-04 accessor/fact obligations are exposed, and can they be routed without solving them here?
18. Which S6D-05 value shapes are required, and what minimum reference is needed without stealing that domain?
19. Does any candidate selector duplicate Effect arbitration, Resource recovery, Activity execution, domain query or LLM adjudication authority?
20. Can Step 8 prove zero selectable selector without complete metadata and zero dormant selector accepted by executable content?

---

## 8. Alternatives to compare

### A. Evidence-activated selector surface with exact per-selector metadata — recommended investigation baseline

Start from the five active selectors, activate dormant selectors only when a concrete supported mechanic proves need, and remove/quarantine unsupported vocabulary. This minimizes false support while preserving deliberate future reservations.

### B. Activate the full registered selector vocabulary and complete all metadata

This maximizes apparent coverage but risks inventing contracts, supporting unused capabilities and stealing S6D-07–09 evidence work. It is acceptable only if current supported-profile evidence proves every selector.

### C. Keep only the current five active selectors and defer all other activation to seed domains

This is conservative but may leave S6D-03 incomplete if already accepted domain mechanics necessarily require additional calculations. It also risks transferring metadata design piecemeal into content domains.

### D. Family-based metadata templates with per-selector exceptions

This may reduce duplication for coherent operation/result families, but templates are acceptable only if expanded machine contracts remain exact and item-level differences in type, subject, inputs, ordering and resolver ownership cannot be hidden.

The Decision Brief may recommend a composition. Compare proof burden, false-activation risk, false-deletion risk, metadata complexity, deterministic validation, downstream coupling and supported-mechanics coverage.

---

## 9. Human/agent decision boundary

The agent owns source discovery, item-level extraction, supported-consumer tracing, reconciliation, metadata completeness analysis, alternative comparison, recommendation and coordinated consistency repair.

Continue automatically when current accepted owners and supported-profile evidence determine the result.

Stop for the human architect only if evidence establishes a genuine unresolved choice about:

- materially expanding or shrinking the supported product/rules surface;
- selecting among incompatible but valid combination semantics;
- superseding an accepted owner or authority boundary;
- accepting a material compatibility, correctness or performance risk;
- choosing a user-visible house-rule/rules interpretation not fixed by current product semantics.

Do not escalate bookkeeping, stale examples, schema synchronization, technically forced quarantine, type derivation from an accepted owner, or documentation volume.

---

## 10. Eight-step loop and review gates

1. Architecture Task Brief — this artifact plus independent whole-project brief critic.
2. Research & Architecture Draft — complete evidence products and alternatives.
3. Decision Brief — established deltas and exact human questions, if any.
4. Collaborative Architecture Review.
5. Candidate Specification.
6. Independent whole-project adversarial review.
7. Resolution Gate.
8. Canonicalization and verified publication.

Both critics must reconstruct the relevant direct and indirect dependency subgraph through `PROJECT_MAP.md`, locate actual current owners, inspect existing rules before proposing new ones, and determine whether a conflict belongs in S6D-03 or requires explicit supersession.

---

## 11. Step-1 exit criteria

Step 1 is complete only when:

1. scope and downstream boundaries are explicit;
2. the Source Manifest covers every source class capable of changing the framing;
3. registration/selectability/metadata completion remain distinct;
4. supported-profile evidence, not example presence, governs activation;
5. selector, accessor, query, Activity, Effect and LLM authority boundaries are preserved;
6. evidence products force separate item-level ledgers with exact registry equality for all 34 selectors and all 26 operations, including operations with no claimed pair;
7. whole-project brief critic has no unresolved BLOCKING or SIGNIFICANT finding;
8. brief and critic are published and verified on the authoritative branch;
9. roadmap records S6D-03 Step 1 complete / Step 2 next;
10. no Step-2 selector decision or machine-contract change has begun.

## 12. Full-loop exit criteria

S6D-03 closes only when:

1. the selector ledger equals all 34 registered selectors and the separate operation ledger equals all 26 registered operations; every ID has an evidence-backed active, dormant or stale outcome consistent with S6D-02;
2. every selectable selector has complete contribution/result/value/dependency/input/subject/resolver metadata;
3. selectable selector IDs equal machine selector metadata IDs;
4. every legal selector/operation pair has an exact S6D-03 compatibility contract and deterministic combination owner; it names the existing portable value owner or precise S6D-05 realization obligation and does not certify an unresolved serialized shape;
5. no executable definition uses a dormant/unregistered selector or operation;
6. unsupported vocabulary and stale active references are removed or nonselectable;
7. dependency/input permissions are explicit and transitively safe;
8. cycles and hidden evaluation-order/fixed-point behavior are rejected;
9. selector metadata does not duplicate accessor/query/Activity/Effect/LLM authority;
10. focused verification and maintenance audit pass;
11. whole-project adversarial critic has no unresolved BLOCKING/SIGNIFICANT finding;
12. canonical owners, machine artifacts, tests, PROJECT_MAP and roadmap are synchronized;
13. S6D-04 Step 1 is named next but not started.

---

## 13. Stop boundary

After the brief critic:

- repair every BLOCKING and SIGNIFICANT framing/source/dependency issue;
- publish only this Task Brief, its critic record and the minimal roadmap/PROJECT_MAP routing needed to record Step 1;
- verify exact remote contents and branch HEAD through the GitHub Connector;
- stop before Step 2 research or any selector/catalog/schema/test change.
