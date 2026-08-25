# S6D-04 — Mechanical Accessors, Invocation Facts and Dependency Graph — Architecture Task Brief

Status: **STEP 1 COMPLETE — WHOLE-PROJECT BRIEF CRITIC PASS — STEP 2 NOT STARTED**

Date: 2026-08-25

Authoritative preparation ref: `v1/engine-rearchitecture@5ff8614a382619b29483592194c869a5e2372e4b`

Program inputs:

- S6D owner decision, parent Task Brief and plan;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- S6D-01 through S6D-03 canonical owners and review chains.

Predecessor: S6D-03 is closed by `DEV/ARCHITECTURE/CALCULATION_SELECTOR_METADATA.md`.

Whole-project critic: `DEV/docs/superpowers/specs/2026-08-25-s6d-04-mechanical-accessors-invocation-facts-dependency-graph-brief-critic.md`.

This artifact frames only Step 1. It does not decide item metadata, alter catalogs/schemas/runtime/tests, begin S6D-05, or resume R2.7.

---

## 1. Problem

The current mechanical-surface artifact contains four coupled surfaces:

- ten registered MechanicalContext accessors;
- two invocation-adjudicated boolean facts;
- four derived nodes;
- selector/accessor/derived dependency references and input-class declarations.

The accessor registry already states source class, value type, subject kinds and some static dependencies. Separate accessor-reference schemas define concrete arguments. This is not complete enough to prove deterministic safe use:

- metadata does not enumerate argument/binding contracts or permitted consumers;
- source classes (`DIRECT_AUTHORITY|DERIVED_MECHANICAL`) and input provenance classes (`ENGINE_STATE|INVOCATION_ADJUDICATED`) are different axes but are not fully reconciled;
- missing/unavailable/null/false/zero semantics are not item-complete;
- invocation facts have no exact consumer/binding/acceptance/provenance/occurrence contract;
- an input-class allowlist is not an exact fact-ID allowlist;
- derived-node metadata remains only partially specified;
- static ID edges do not by themselves prove acyclicity after definition-instance bindings;
- current selectors deliberately have empty fact allowlists, while `condition_intrinsic` still admits `INVOCATION_ADJUDICATED` as an unresolved S6D-04 obligation;
- cache/currentness and pinned state-view requirements are prose-owned but not machine-complete;
- runtime domain queries must remain infrastructure-only and must not leak into declarative content.

S6D-04 must close the exact supported surface without inventing accessors/facts from generic D&D familiarity or laundering runtime queries into content.

---

## 2. Goal

Produce a decision-ready architecture that:

1. accounts item by item for all 10 accessors, 2 facts and 4 derived nodes;
2. proves which remain supported/active and which must become dormant or stale;
3. gives every supported accessor exact arguments, bindings, subject restrictions, result type, source/provenance, missing semantics, consumers and dependencies;
4. gives every supported invocation fact exact type, producer/acceptance authority, occurrence scope, bindings, provenance, missing behavior and permitted consumers;
5. gives every supported derived node exact result role, allowed inputs, consumers, dependencies and evaluation ownership;
6. defines one scoped dependency graph across selectors/accessors/derived nodes and fact inputs;
7. proves transitive input-class/fact permissions and bound-instance cycle safety;
8. preserves one pinned committed/prospective state view and safe cache/currentness semantics;
9. keeps runtime domain queries infrastructure-only and nonserializable;
10. routes portable value members to S6D-05, primitives to S6D-06, seed evidence to S6D-07–09 and packaging/verification to S6D-11;
11. leaves zero unresolved machine/prose/schema/test/runtime contradiction.

---

## 3. Scope

### In scope

- all ten `core-catalog.mechanical_accessors` IDs;
- both `mechanical-surfaces.context_facts` IDs and the question of their exact registration/admission owner;
- all four current `derived_nodes`;
- `mechanical-accessor-ref.schema.json`, mechanical predicate/fact shapes and relevant definition schemas;
- direct-authority versus derived-mechanical source semantics;
- ENGINE_STATE versus INVOCATION_ADJUDICATED provenance;
- exact argument/binding/result/missing contracts;
- permitted selector/derived/predicate/Activity consumers;
- pinned state-view identity and prospective-view legality;
- exact static edges, definition-bound edges and cycle detection obligations;
- graph evaluation ownership, invalidation/cache keys and retry consistency;
- catalog-aware validation and focused tests;
- conflicts with existing Rule Element examples, execution/adjudication and domain owners.

### Out of scope

- adding seed-derived accessors/facts without evidence;
- portable serialized Activity/invocation-fact/envelope member design (S6D-05);
- Activity primitive behavior (S6D-06);
- authoring rules/character/spell/monster/equipment seed content (S6D-07–09);
- runtime query/read-model API design;
- general-purpose expression/query languages;
- implementation of evaluator/compiler/cache;
- global repository scans, file/network access or LLM-owned state;
- timers/schedulers;
- reopening S6D-01–03 absent concrete contradiction.

---

## 4. Inherited invariants

1. Calculation Selectors, MechanicalContext accessors/facts and runtime domain queries are separate surfaces.
2. Accessors expose exact typed reads, never arbitrary JSON paths or expressions.
3. Runtime queries are infrastructure-only, nonserializable and unavailable to Rule Elements/content.
4. Every evaluation uses one logically immutable pinned committed or prospective state view.
5. Engine-owned state cannot be supplied as LLM adjudication.
6. Invocation-adjudicated inputs are explicitly accepted facts, never ambient prose or model memory.
7. Missing invocation fact is not false.
8. Missing engine record/value is not silently zero, false, empty or null unless the exact accessor contract says so.
9. A provenance class is not an exact fact-ID permission.
10. Permissions are transitive: a consumer cannot reach a forbidden input through an accessor/derived node.
11. Dependency kinds are only `selector|accessor|derived`; exact identities use prefixed references.
12. Graphs that can affect a calculation are acyclic. No stable loop, hidden fixed point or author order resolves a cycle.
13. Definition-instance bindings may create edges not visible in the registry-name graph and must be included or conservatively rejected.
14. Derived indexes/caches are disposable and never authority.
15. Cache keys include the pinned view plus bindings and other contract-relevant inputs.
16. Facts/reads used by accepted work preserve provenance required for retry, resume and Resolution trace.
17. LLM/House Rules cannot invent accessor/fact IDs, values, authority or mutation.
18. S6D-03 active selectors admit ENGINE_STATE only with empty fact allowlists; S6D-04 may not silently broaden them.
19. `condition_intrinsic` invocation input remains unresolved until item evidence closes it.
20. Conflicts are resolved at actual current owners; human escalation is reserved for material semantics/authority choices.
21. S6D-04 owns invocation-fact semantics: ID, nominal type, producer/acceptance authority, occurrence and binding rules, provenance, missing behavior, exact consumers and retention requirements. S6D-05 owns portable serialized invocation-fact/envelope members that realize those semantics.
22. An active fact cannot be certified complete until it names an existing portable envelope/schema owner or a precise S6D-05 realization obligation. S6D-04 must not define those portable members.

---

## 5. Current census baseline

### Accessors — exact 10

- `health.current`
- `health.temporary`
- `health.maximum`
- `health.bloodied`
- `life.state`
- `condition.present`
- `condition.value`
- `resource.capacity`
- `resource.available`
- `owner_effect.parameter`

### Invocation facts — exact current 2

- `fiction.target_visible`
- `fiction.target_reachable`

### Derived nodes — exact current 4

- `effect_availability`
- `effect_arbitration`
- `condition_aggregation`
- `condition_intrinsic`

Step 2 must not assume all remain active merely because they are present.

---

## 6. Mandatory Source Manifest

Step 2 starts from the current remote ref and assigns every source an authority role.

### Process/sequencing

- AGENTS and both design-process owners;
- PROJECT_MAP and current roadmap;
- S6D owner/brief/plan;
- S6D-01–03 canonical owners, evidence and critics.

### Mechanical ownership

- Rule Element, Calculation Selector, Activity, Actor, Asset, Resource, Effect, Condition, Duration/Recovery and LifeState owners;
- accepted Step-2 selector/query design and final assurance chain;
- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md` — Resolution/Continuation, boundary-occurrence, invocation and receipt identity;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md` — retry/idempotency and accepted-work resume semantics (the unsuffixed predecessor is historical);
- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md` — checkpoint reachability and recovery-currentness;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` plus its `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-resolution-gate.md` — GC liveness/orphan disposition;
- S6D-01 reconstruction/recovery obligations — pinned package/catalog identity during reconstruction;
- House Rules/adjudication and AI boundary owners.

S6D-04 must preserve those owners' state-view identity, fact retention, retry/idempotency, checkpoint reachability, GC liveness and failure-disposition contracts. It does not redesign resume, checkpoint, GC or recovery.

### Machine/schema/test surfaces

- all current catalog files;
- mechanical surfaces schema;
- accessor-ref and mechanical-predicate schemas;
- definition/effect/condition/resource/activity schemas that embed predicates or Rule Elements;
- `runtime-resolution-state.schema.json`, `runtime-continuation-state.schema.json`, `resolution-receipt.schema.json`, `execution-segment.schema.json`, `invocation-fact.schema.json`, `boundary-occurrence.schema.json` and `pending-child-invocation.schema.json`;
- Step-2 evaluation-input, applicability, machine-contract and example tests;
- `test_step3_execution_owner_contract.py`, `test_step3_resume_ordering_contract.py`, `test_step3_execution_value_schemas.py`, `test_step3_execution_examples.py`, `test_step3_event_followup_contract.py` and `test_step3_execution_catalog_contract.py`;
- S6D-02/03 focused verification;
- maintenance/release validation.

### Runtime/domain/seed consumers

- GAME/CORE mechanics integrity, combat, magic, exploration, dialogue, readiness, advancement and adjudication;
- GAME/RULES routing/current package content;
- exact execution/retry/recovery consumers;
- any consumer discovered through actual graph references.

### Historical evidence

Use runtime proposals and superseded designs only for derivation. A historical fact/accessor/query name is not current admission evidence.

### Search obligations

For every accessor/fact/derived node:

- search schemas, definitions, tests, runtime branches and owner prose;
- classify every hit as canonical, accepted supported requirement, machine realization, structural example, derivative, historical or stale;
- trace indirect consumers through selectors, predicates, derived nodes, Activities, effects and accepted-work recovery;
- record negative evidence only after the relevant owner route and repository boundary were checked.

---

## 7. Required Step-2 evidence products

### 7.1 Accessor evidence ledger — exact 10

For each accessor:

```text
Accessor ID:
Current disposition/realization:
Canonical state/value owner:
Machine metadata:
Reference-schema branch:
Argument names/types:
Binding roles and resolution:
Subject kinds:
Result type and constraints:
Source class:
Input provenance class:
Missing/unavailable/null semantics:
Permitted consumer classes and exact consumers:
Static dependencies:
Definition-bound dependency possibilities:
Pinned/prospective view legality:
Cache/currentness key requirements:
Trace/provenance requirements:
Supported-profile consumer evidence:
Decision and machine destination:
Conflicts/stale references:
```

The accessor-ledger ID set must equal `core-catalog.mechanical_accessors`.

### 7.2 Invocation-fact evidence ledger — exact current set

For each fact:

```text
Fact ID:
Registration/admission owner:
Type:
Producer:
Acceptance authority:
Occurrence/invocation identity:
Bindings/subjects/targets:
Provenance/evidence:
Missing semantics:
Permitted consumer IDs:
Transitive permission rule:
Retry/idempotency retention:
Supported-profile consumer:
Active/dormant/stale decision:
Machine/schema destination:
Existing portable envelope/schema owner or exact S6D-05 realization obligation:
```

Also decide whether exact fact IDs require core-catalog registration or whether the mechanical-surface registry is the bounded canonical ID owner. Do not create duplicate authority.
This ledger defines semantic requirements only. It must not design portable serialized members, and it must not call an active fact complete while its portable realization is unowned.

### 7.3 Derived-node evidence ledger — exact 4

For each node:

```text
Node ID:
Semantic owner:
Result role/type:
Permitted consumers:
Allowed dependency kinds:
Allowed input classes:
Exact static dependencies:
Definition-bound edges:
Evaluation/state-view owner:
Missing/failure semantics:
Cache/invalidation:
Supported consumer:
Decision:
```

### 7.4 Consumer-permission matrix

Rows: selectors, predicates, derived nodes, Activities/runtime resolvers.
Columns: each accessor/fact/node.
Cells: forbidden, permitted with exact binding, or downstream obligation.

Class-level permission alone is insufficient where exact ID permission is required.

### 7.5 Dependency graph product

Represent separately:

- node kind and ID;
- exact static edges;
- parameter/binding schema;
- definition-instance edges;
- allowed input classes;
- exact fact permissions;
- state-view/prospective-view requirement;
- consumer edge.

The product must define graph scope and prove how bound-instance cycles are rejected without a global fixed-point engine.

### 7.6 Missing/failure matrix

For each read/fact distinguish:

- false/zero/empty as a legitimate value;
- value absent by domain semantics;
- required binding absent;
- referenced record/definition missing;
- invocation fact not supplied;
- fact supplied but unauthorized;
- stale/mismatched state view;
- dependency cycle;
- unsupported/dormant ID.

Map each to existing typed failure/disposition owners. Do not proliferate top-level codes without evidence.

### 7.7 Runtime-query exclusion ledger

Identify nearby infrastructure queries needed by runtime and prove why each is not a declarative accessor/fact. Record location/order/multi-result semantics and nonserialization boundary.

### 7.8 Verification matrix

Require executable checks for:

- exact accessor/fact/derived-node set accounting;
- metadata/reference-schema equality;
- argument/binding/subject legality;
- value/result/source/input-class compatibility;
- exact fact-ID permission;
- missing != false;
- state-view pinning and prospective-view legality;
- dependency-kind/reference separation across all sections;
- static and bound-instance cycle rejection;
- transitive forbidden-input rejection;
- cache-key completeness/currentness;
- dormant IDs inaccessible;
- runtime queries absent from serializable schemas;
- current structural examples classified correctly;
- changed owner/schema/catalog/test synchronization.
- every active invocation fact names an existing portable owner or an exact S6D-05 obligation, without S6D-04 defining portable members;
- Step-3/5.2/5.7/5.13 and S6D-01 recovery invariants remain preserved.

---

## 8. Questions Step 2 must answer

1. Which of the ten accessors have concrete supported consumers?
2. Are all current accessors truly independent IDs, or are any derived convenience aliases without a valid calculation consumer?
3. Does every accessor metadata entry exactly match one reference-schema branch and vice versa?
4. What is the semantic difference among DIRECT_AUTHORITY, DERIVED_MECHANICAL, ENGINE_STATE and INVOCATION_ADJUDICATED?
5. What arguments and binding roles does each accessor require?
6. How are subject role names resolved without arbitrary lookup authority?
7. When does an absent condition/resource/effect parameter mean false/zero versus typed missing?
8. Can `condition.value` exist when `condition.present` is false, and what result is returned?
9. What exact owner supplies `owner_effect.parameter`, and how is its parameter declaration/type validated?
10. Which accessors are legal against prospective state and which require committed state?
11. Are `fiction.target_visible` and `fiction.target_reachable` required by any current selectable consumer?
12. Who accepts an invocation fact, with what occurrence identity and retained provenance?
13. Must facts be registered in core catalog, or is the bounded mechanical-surface fact map the exact owner?
14. Does `condition_intrinsic` genuinely require invocation-adjudicated input, and which exact fact/binding permits it?
15. Are any additional nonboolean fact shapes proven by supported cases?
16. What is the exact difference between a fact input and an Activity parameter/adjudicated Choice?
17. Do derived-node dependencies and allowed kinds agree item by item?
18. Which exact nodes may consume each accessor/fact?
19. How are transitive input permissions computed?
20. How are definition-bound cross-resource/effect/subject cycles detected?
21. What graph scope is compiled together, and what happens when scope cannot prove acyclicity?
22. What cache key prevents cross-revision/cross-binding reuse?
23. Which reads require Resolution-trace retention or accepted-work recovery?
24. Which nearby runtime queries must remain nonserializable?
25. Are current tests proving semantic legality or only JSON shape?
26. Can closure prove zero hidden query/fixed-point/order/LLM authority?
27. Which findings are technical consequences and which require human product semantics?

---

## 9. Alternatives

### A. Item-complete bounded graph over current evidence — recommended baseline

Keep only evidence-supported accessors/facts/nodes, fully type metadata and permissions, and reject unsupported/dormant edges.

### B. Preserve all current entries and fill missing fields by family defaults

Lower churn, but risks placeholder laundering and hides item-specific missing/consumer semantics.

### C. Seed-first expansion

Activate everything plausibly needed by D&D before seed evidence. Rejected as a default because S6D-07–09 own content proof and registration alone is insufficient.

### D. Replace accessors with a generic query/expression layer

Rejected by accepted architecture. Runtime query needs do not justify declarative query authority.

### E. Split static ID graph and bound-instance graph with conservative rejection

Potential component of A: use a compact registry graph plus definition-instance expansion. It is acceptable only if both remain one authoritative validation model rather than two competing evaluators.

Compare proof burden, false activation/deletion, retry safety, cycle completeness, hot-path cost, schema complexity and downstream coupling.

---

## 10. Human/agent boundary

The agent owns discovery, item extraction, owner/consumer tracing, missing/failure analysis, graph synthesis, alternatives, recommendation and coordinated consistency work.

Continue automatically when accepted owners determine the answer.

Stop for human decision only if evidence exposes:

- a material supported-product expansion/removal;
- incompatible valid semantics for missing/value/binding behavior;
- a material LLM-versus-engine authority choice;
- supersession of accepted state/query boundaries;
- explicit acceptance of critical correctness/retry/performance risk.

Do not escalate large ledgers, stale examples, schema synchronization, obvious dormant classification or mechanically forced graph constraints.

---

## 11. Eight-step loop

1. Task Brief plus whole-project brief critic.
2. Research & Architecture Draft with all evidence products.
3. Decision Brief.
4. Collaborative Review.
5. Candidate Specification.
6. Independent whole-project adversarial review.
7. Resolution Gate.
8. Canonicalization and verified publication.

Both critics reconstruct the direct/indirect dependency subgraph through PROJECT_MAP, locate actual owners, inspect pre-existing rules and challenge scope theft or local-only reasoning.

---

## 12. Step-1 exit criteria

Step 1 is complete only when:

1. scope covers exact 10 accessors, 2 current facts and 4 derived nodes;
2. the Source Manifest includes every source class capable of changing framing;
3. accessors, facts, derived nodes and runtime queries remain distinct;
4. source classes, input classes and exact fact permissions are not conflated;
5. missing semantics, bindings, state-view identity and bound-instance cycles are mandatory evidence;
6. S6D-04/S6D-05 boundaries are explicit;
7. whole-project critic has zero unresolved BLOCKING/SIGNIFICANT;
8. brief/critic are published and verified;
9. roadmap records Step 1 complete / Step 2 next;
10. no Step-2 item decision or machine edit has begun.

## 13. Full-loop exit criteria

S6D-04 closes only when:

1. exact accessor ledger equals all ten registered accessor IDs;
2. exact current fact and derived-node sets are accounted with one owner;
3. every active item has a supported consumer and complete metadata;
4. every dormant/stale item is nonselectable/inaccessible with trigger or coordinated removal;
5. accessor metadata and reference schemas are bidirectionally equal;
6. facts have exact producer/authority/occurrence/binding/provenance/missing/consumer contracts;
7. every active fact names an existing portable envelope/schema owner or a precise S6D-05 realization obligation, and no portable member is designed here;
8. every consumer has exact accessor/fact permissions;
9. engine state cannot enter through adjudication;
10. missing fact/value/binding behavior is exact and false/zero-safe;
11. one pinned committed/prospective view governs a calculation;
12. dependency kinds and exact refs are separated;
13. static and bound-instance graphs are cycle-safe without fixed points;
14. transitive input permissions are enforced;
15. cache/invalidation keys prevent stale/cross-binding reuse;
16. runtime queries remain infrastructure-only/nonserializable;
17. existing Step-3/5.2/5.7/5.13 and S6D-01 view/retention/retry/checkpoint/GC/recovery contracts are preserved;
18. no arbitrary code/query/file/network/LLM mutation authority appears;
19. focused verification and maintenance audit pass;
20. adversarial critic has no unresolved BLOCKING/SIGNIFICANT;
21. canonical owners, machine artifacts, tests, PROJECT_MAP and roadmap are synchronized;
22. S6D-05 Step 1 is next but not started.

---

## 14. Stop boundary

After brief criticism:

- repair all BLOCKING/SIGNIFICANT framing issues;
- publish only Task Brief, critic and minimal roadmap/PROJECT_MAP routing;
- verify exact remote HEAD/content;
- stop before Step 2.

