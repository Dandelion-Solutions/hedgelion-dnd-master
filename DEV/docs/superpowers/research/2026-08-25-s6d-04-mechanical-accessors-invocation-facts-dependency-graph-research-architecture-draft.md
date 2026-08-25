# S6D-04 — Research & Architecture Draft

Status: **STEP 2 COMPLETE — EVIDENCE SYNTHESIZED**

Base: `v1/engine-rearchitecture@3d3f45e77614a7fac5cf074571802d48f54ac232`.

## 1. Source Manifest and authority roles

Primary current owners inspected:

- process/sequencing: `AGENTS.md`, both design-process owners, `PROJECT_MAP.md`, roadmap, S6D owner/parent brief/plan and S6D-01–03 closure chains;
- semantics: `RULE_ELEMENT_MODEL.md`, `ACTIVITY_MODEL.md`, `ACTOR_MODEL.md`, `CALCULATION_SELECTOR_METADATA.md`, `CAMPAIGN_HOUSE_RULES.md`, Step-2 selector/query design and Slice-D assurance;
- execution/recovery: Step-3 canonical execution, Step-5.2 resumable v2, Step-5.7 checkpoint recovery, Step-5.13 GC canonical+resolution and S6D-01 reconstruction;
- machine: core catalog, admission ledger, mechanical surfaces, accessor/predicate/fact/Resolution/Continuation/receipt/occurrence schemas and focused Step-2/3/S6D/House-Rules tests;
- consumers: GAME CORE mechanics/adjudication/combat/magic/exploration/readiness/runtime/randomness and GAME RULES routing.

GAME RULES currently provides routing, not a definition seed. Structural examples were not counted as executable consumers.

## 2. Census and dispositions

| Item | Evidence result | Disposition |
|---|---|---|
| `health.current` | Actor `hp.current` direct authority; required bounded read | active |
| `health.temporary` | Actor temporary HP direct authority | active |
| `health.maximum` | active S6D-03 selector, integer >=1 | active |
| `health.bloodied` | exact same-view derivation accepted | active |
| `life.state` | Actor LifeState direct authority | active |
| `condition.present` | accepted effective Condition aggregate read | active |
| `condition.value` | identity accepted; aggregation deliberately unresolved | dormant to S6D-08 |
| `resource.capacity` | active selector; integer >=0 | active |
| `resource.available` | accepted storage-independent bounded read | active |
| `owner_effect.parameter` | accepted only through implicit current owner Effect binding | active |
| two fiction facts | bounded boolean capability accepted; no exact admitted compiled consumer | dormant to S6D-07–09 |
| four derived nodes | accepted internal stages; required by active Effect/Condition surface | active internal |

No item was removed. Dormancy prevents syntactic registration from becoming unsupported executable authority.

## 3. Accessor ledger synthesis

All ten IDs are equal across core registry, surface metadata and accessor-ref branches.

Shared contract:

- input class: ENGINE_STATE;
- explicit arguments resolve through a bound role/definition table;
- committed or prospective pinned view;
- cache key: catalog context + view + bindings + relevant revisions;
- permitted ceilings: closed predicate/accessor/derived surfaces;
- concrete definition occurrences become exact consumer nodes.

Item deltas:

- direct Actor fields missing when mechanics requires them produce typed hydration/materialization, not zero;
- `condition.present` returns false only after a valid named definition is resolved and aggregation proves no effective application;
- dormant `condition.value` would distinguish absent from missing, but cannot compile before S6D-08;
- Resource results align to integer supported selector semantics;
- `owner_effect.parameter` has an implicit `owner_effect_application` binding and cannot cross Effect authority.

## 4. Invocation-fact ledger synthesis

Both IDs have the same semantic contract:

| Field | Contract |
|---|---|
| type/source | boolean / INVOCATION_ADJUDICATED |
| producer | host LLM boundary |
| acceptor | Activity invocation validator |
| occurrence | one Activity/Resolution invocation generation |
| binding | exact roles of the admitted compiled consumer; optional boundary reference only for boundary-originated invocation |
| provenance | stable reference + fingerprint |
| missing | typed missing input; distinct from false |
| retention | fixed causal input while accepted work remains live |
| portable realization | current invocation-fact schema, completed by S6D-05 |
| current consumers | none admitted exactly |
| disposition | dormant reserved |

The Activity/Rule Element examples prove intended shape, not activation. Mechanical-surface fact map remains the one bounded registry; duplicating IDs into core catalog was rejected. Exact producer/consumer allowlists are machine metadata; an AST reference cannot authorize itself.

## 5. Derived-node ledger synthesis

| Node | Result | Inputs | Fixed edges | Exact fact IDs |
|---|---|---|---|---|
| availability | Effect member set | engine | none | none |
| arbitration | Effect member set | engine | availability | none |
| aggregation | Condition aggregate | engine | availability + applicability selector | none |
| intrinsic | Rule Element set | engine | aggregation | none |

The old intrinsic class allowance for adjudicated input had no exact fact/consumer and could not reach any S6D-03 selectable selector, all of which are engine-only. Removing it is gap closure, not product-semantic narrowing.

## 6. Missing/failure matrix

- legitimate false: accepted fact false; no effective valid named Condition for `condition.present`;
- legitimate zero: valid integer Resource capacity/availability result;
- legitimate absent: future valid valued-Condition aggregate with no value;
- missing fact: typed adjudication requirement;
- missing authority: typed hydration/materialization;
- invalid binding/definition/owner parameter: compile or invocation validation;
- dormant/unknown ID: compile validation;
- stale view/occurrence/catalog: currentness/compatibility failure;
- incomplete/cyclic graph: definition/prospective compilation failure.

No new parallel top-level failure vocabulary is required.

## 7. Graph and permission synthesis

The accepted hybrid model becomes one explicit product:

1. registry graph: exact static edges, allowed kinds/classes/facts;
2. bound-instance expansion: definitions, predicates, source/target/owner/resource/condition and prospective edges;
3. transitive proof: reachable input classes/fact IDs are subsets of every upstream consumer permission;
4. cycle proof: reject if full affected closure cannot be proven acyclic.

Canonical negative cases are maximum→bloodied→maximum and capacity(R)→available(R)→capacity(R), including cross-effect/resource bindings.

## 8. State view, cache and recovery

One context identity includes compatible ResolvedCatalogContext, pinned committed/prospective view, bindings, native revisions and any permitted accepted-fact fingerprint.

Step 3 owns re-pin after expected child work. Step-5.2/5.7 rebuild from native authority; no MechanicalContext/DAG/index/prospective cache is restored. Step-5.13 retains causal fact/receipt/fingerprint records only while live accepted work references them. This preserves, rather than redesigns, those owners.

## 9. Runtime-query exclusion

Nearby host needs include Effect membership lookup, Resource owner/storage lookup, temporal due reads, occurrence/receipt lookup and bounded context hydration. They remain nonserializable host capabilities, unordered unless their owner specifies order, and cannot appear in predicate/accessor schemas.

## 10. Alternatives

A. Activate every registered item. Rejected: examples would become support claims and unresolved valued-Condition semantics would leak.

B. Remove unsupported IDs. Rejected: accepted bounded capability and downstream triggers exist.

C. Retain exact registry, activate proven semantic surfaces, quarantine unresolved/unconsumed items. Selected.

D. Introduce one generic typed query/evaluation language. Rejected by accepted authority and performance boundaries.

E. Validate only the registry-name DAG. Rejected because definition bindings create cycles.

## 11. Synthesis-completeness gate

Every 10/2/4 item has a disposition, exact owner route, missing behavior, consumer rule, graph role and downstream trigger. Negative evidence and structural examples are classified. Execution/recovery/query boundaries are mapped. No unresolved technical contradiction remains.

Potential product choices were avoided:

- no valued-Condition aggregation chosen;
- no fiction fact declared current public support;
- no cross-Effect parameter access granted.

Therefore Step 3 can present a no-human-choice recommendation.

