# Step 2 Retrospective Assurance — Slice D Coverage and Research: Mechanical Evaluation and Read Boundaries

Status: **COVERAGE / RESEARCH COMPLETE — FINDINGS REQUIRE ADVERSARIAL REVIEW**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-2-assurance-slice-d-mechanical-evaluation-task-charter.md`.

This document audits the accepted Step-2 mechanical evaluation/read architecture against the independently frozen Slice-D problem framing. It distinguishes verified coverage from gaps rather than treating existing implementation shape as evidence of correctness.

## 1. Evidence inspected

Primary project evidence:

- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`;
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`;
- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/mechanical-surfaces.json`;
- `DEV/SCHEMAS/mechanical-surfaces.schema.json`;
- `DEV/SCHEMAS/mechanical-predicate.schema.json`;
- `DEV/SCHEMAS/mechanical-accessor-ref.schema.json`;
- `DEV/SCHEMAS/rule-element.schema.json`;
- `DEV/SCHEMAS/activity-definition-data.schema.json`;
- accepted selector/query design, adversarial review, and resolution;
- final integrated Step-2 review;
- Slice-A Resource amendment;
- Slice-B Condition/Effect amendment;
- Slice-C owner-local scheduled-trigger amendment;
- saved Step-3 Task Brief and research draft only after the Slice-D charter/baseline coverage was established.

No external research was required to establish the findings below. They arise from contradictions between accepted HDM authority rules and current project contracts rather than uncertainty about a third-party system.

## 2. Baseline that survives review

The following accepted design remains strong and should be retained unless the critic finds a concrete counterexample.

### COV-D1 — three mechanical surfaces are genuinely different

**Coverage: SATISFIED.**

The architecture correctly separates:

```text
Calculation Selector
    named calculation/contribution surface

MechanicalContext accessor
    typed engine-owned read in one pinned view

runtime Domain Query
    infrastructure lookup of relevant owners/index rows
```

Rule Elements cannot contain domain-query syntax, and accessors do not expose arbitrary JSON paths. This is a useful capability/security boundary, not merely naming.

### COV-D2 — direct versus derived engine facts are separated

**Coverage: SATISFIED.**

`mechanical-surfaces.json` distinguishes `DIRECT_AUTHORITY` from `DERIVED_MECHANICAL` accessors. HP/LifeState direct reads are not confused with derived maximum HP, Bloodied, Condition meaning, or Resource availability.

Derived accessor values remain cacheable/rebuildable rather than writable world aliases.

### COV-D3 — typed accessor shapes close arbitrary path reads

**Coverage: SATISFIED.**

`mechanical-accessor-ref.schema.json` provides exact argument shapes for the initial accessor set. The old arbitrary `{ref: "some.path"}` operand is rejected by the current predicate schema/tests.

### COV-D4 — pinned committed/prospective state-view invariant is correct

**Coverage: SATISFIED ARCHITECTURALLY / REPRESENTATION DEFERRED CORRECTLY.**

The selector/query resolution requires one explicit logical state-view identity and forbids cache leakage across committed/prospective views. Step 3 correctly owns concrete overlay/segment representation.

The saved Step-3 research reinforces rather than changes the invariant: after an expected reaction child, rebuild/re-pin and recompute from a safe phase while preserving fixed historical inputs rather than trusting stale prospective deltas.

### COV-D5 — hybrid static contracts + scoped concrete DAG remains justified

**Coverage: SATISFIED AS ARCHITECTURE / MACHINE CONTRACT PARTIAL.**

The human-approved model avoids both premature fixed strata and implicit fixed-point semantics. Concrete dependency cycles introduced only by a particular target/source combination are rejected before commit.

The graph is explicitly scoped to mechanically relevant hydrated state; campaign-global graph rebuilds are rejected.

A machine-contract gap remains below because the structured metadata does not yet encode all the dependency contracts the prose says exist.

### COV-D6 — runtime queries are correctly non-declarative

**Coverage: SATISFIED ARCHITECTURALLY / IMPLEMENTATION VERIFICATION LATER.**

The accepted resolution restricts runtime query inputs to operation/domain-specific typed keys and explicitly forbids callback/filter/SQL/JSON-path/general-`where` syntax.

There is not yet a runtime implementation to audit for an accidental generic filter API. That is an implementation verification item, not evidence for adding a serializable query language now.

### COV-D7 — scheduled triggers do not create a new query surface

**Coverage: SATISFIED.**

Slice C's new `scheduled_triggers` declaration contains only a local key, positive metric delay, and bounded `activity_id`. It has no predicate/query/callback field.

When due, the owning Effect provides owner/source/target/application identity and Step 3 creates normal bounded Activity execution. The child execution should use the ordinary MechanicalContext/accessor and deterministic binder rules rather than receive a privileged temporal query context.

No new accessor is currently proven necessary.

## 3. Finding D-F1 — invocation context facts are promised as registered but have no registry

**Severity: BLOCKING machine/authority gap.**

The accepted selector/query resolution says:

> the LLM/host may provide only fact families explicitly registered as `INVOCATION_ADJUDICATED` or another approved non-engine-owned class.

`RULE_ELEMENT_MODEL.md` likewise says predicates may read registered context facts.

However, the current machine contracts contain no context-fact registry at all:

- `core-catalog.json` registers selectors and accessors but no mechanical/context fact IDs;
- `mechanical-surfaces.json` contains accessors/selectors/derived-node kinds only;
- `mechanical-predicate.schema.json` accepts `{ "fact": <any machineId> }`;
- no metadata states fact source class, value type, permitted consumers, or binding semantics.

Therefore the compiler cannot mechanically perform the registration check that the normative prose requires.

### Concrete failure

A catalog author can write:

```json
{
  "predicate": {"fact": "target.has_secret_super_bonus"}
}
```

and structural schema validation accepts the ID shape even though no registered fact contract exists.

This does not by itself execute arbitrary code, but it creates an unbounded authority namespace whose values would necessarily be invented/resolved somewhere outside the registered engine contract.

### Required correction direction

Add a machine-readable context-fact registry. Initial fact entries should be explicitly non-engine-owned and typed, for example a small proven fiction-dependent boolean family such as visibility/reachability where the deterministic runtime cannot establish the fiction itself.

Engine-owned conditions such as HP, equipment state, action availability, Resource state, and similar deterministic facts must remain accessors/calculations rather than context facts.

## 4. Finding D-F2 — current examples incorrectly model engine-owned mechanics as LLM facts

**Severity: SIGNIFICANT authority/documentation contradiction.**

Current examples include:

```text
source.equipped
actor.can_act
```

as bare predicate facts.

But equipment state and mechanically derived ability to act are engine-resolvable state/eligibility, exactly the class that the accepted LLM boundary forbids the host from asserting as adjudicated truth.

`ACTIVITY_MODEL.md` also says runtime rejects engine-checkable contradictions, which makes those examples misleading at best and an authority leak if implemented literally.

### Required correction

Remove engine-owned examples from the context-fact surface. Where the engine needs such mechanics, use registered accessors/selectors/Activity eligibility contracts. Context-fact examples must represent facts that are genuinely admitted as invocation adjudication.

## 5. Finding D-F3 — boolean fact absence is currently semantically ambiguous

**Severity: SIGNIFICANT correctness gap; exact request encoding belongs to Step 3.**

`mechanical-predicate.schema.json` supports:

```json
{"fact": "..."}
{"not": {"fact": "..."}}
```

while `ACTIVITY_MODEL.md` illustrates `context_facts` as a list of positive fact IDs.

A list cannot distinguish:

```text
fact explicitly adjudicated false
fact not supplied / not adjudicated
```

Treating missing as false would turn lack of evidence into mechanical evidence, especially under `not fact`.

### Required semantic correction

For invocation-adjudicated facts:

```text
explicit true  -> usable as true
explicit false -> usable as false
missing        -> UNAVAILABLE / typed missing-input failure when referenced
```

Missing must never silently coerce to false.

The exact normalized `RuntimeCommand`/ActionRequest encoding for fact values and provenance belongs to Step 3. Slice D only needs to fix the read semantics and fact registry so Step 3 cannot choose an unsafe representation.

## 6. Finding D-F4 — persistent/state-derived calculations can currently depend on invocation-only facts

**Severity: BLOCKING authority/reconstruction gap.**

This is the Slice-A carry-forward and the strongest current finding.

Any Rule Element may structurally contain a bare context-fact predicate. `resource.capacity` is an ordinary Rule Element selector. Therefore today nothing in the machine metadata prevents:

```text
Resource capacity modifier
    predicate = LLM-adjudicated visibility/reachability fact
```

Slice A now requires a true persistent capacity decrease to normalize canonical `ResourceState.current` in the same prospective transition.

That creates this failure:

```text
LLM adjudicates temporary invocation fact F
    -> F makes resource.capacity smaller
    -> runtime clamps canonical current
    -> invocation ends
    -> F is absent on recovery
```

The canonical state mutation depended on a fact that is not part of the reconstructable mechanical state. Worse, querying Resource capacity later could return a different invariant from the one used to normalize it.

The same structural issue applies to other continuously derived state semantics such as `health.maximum` and current `condition.applicability`.

### Required architecture distinction

Selectors need an explicit evaluation/reconstruction class.

Minimum semantics:

```text
STATE_DERIVED
    result must be reconstructable from pinned engine-owned state/context;
    no INVOCATION_ADJUDICATED dependency is legal, directly or transitively.

INVOCATION_DERIVED
    result may depend on explicitly registered invocation-adjudicated facts;
    those facts are fixed inputs/provenance for that invocation/Resolution.
```

For the current Step-2 surfaces, at minimum:

```text
health.maximum          STATE_DERIVED
resource.capacity       STATE_DERIVED
resource.recovery       STATE_DERIVED
condition.applicability STATE_DERIVED
```

`effect.duration` may remain subject to critic review: a concrete duration is materialized and persisted at application/refresh time, so invocation-dependent input may be safe if Step 3 preserves accepted fact provenance. No proven Step-2 case currently requires such dependence, so the simplest safe initial contract may still classify it `STATE_DERIVED` until seed evidence says otherwise.

The restriction must be **transitive**. A state-derived selector cannot evade the rule by depending on an accessor/derived stage whose own result depends on an invocation fact.

## 7. Finding D-F5 — structured metadata does not encode derived-stage dependency contracts

**Severity: SIGNIFICANT machine-contract gap.**

The accepted hybrid DAG decision says every registered derived mechanical stage declares its typed dependency contract.

Current `mechanical-surfaces.json` contains only:

```json
"derived_node_kinds": [
  "effect_availability",
  "effect_arbitration",
  "condition_aggregation",
  "condition_intrinsic"
]
```

This registers names but no dependency metadata.

Consequences:

- compilation cannot validate which dependency kinds a derived stage is allowed to consume;
- there is no structured edge showing that current Condition aggregation/effectiveness depends on `condition.applicability` after Slice B;
- the machine contract cannot prove a newly added derived stage obeys the human-approved DAG model.

### Required correction direction

Replace/narrow the bare list with structured `derived_nodes` metadata containing at least:

```text
allowed dependency kinds/classes
required fixed stage dependencies where architecture defines one
evaluation/reconstruction class where relevant
```

Concrete bound edges from Rule Element predicates/source roles still belong to the scoped runtime DAG; structured metadata is the static contract, not the whole graph.

## 8. Finding D-F6 — current Condition pipeline omits the Slice-B applicability gate in structured dependency semantics

**Severity: BLOCKING integration gap if left unresolved.**

Slice B established:

> `condition.applicability` gates current mechanical effectiveness, not merely whether a new application record may be created.

The current high-level pipeline still reads conceptually:

```text
Condition-bearing application
    -> lifecycle/basic availability
    -> Condition aggregation
```

and `condition.present/value` depend only on `condition_aggregation` metadata.

To represent immunity gained after application without terminating the application, the derived pipeline must be:

```text
nonterminal Condition application
    -> basic Effect availability/suppression
    -> condition.applicability for this target/Condition in this pinned view
    -> eligible effective member set
    -> Condition aggregation
    -> Condition intrinsic mechanics
```

`condition.applicability` is a selector node, not a second lifecycle field. A later immunity disappearing re-evaluates eligibility and may restore participation without mutation/resurrection.

The dependency graph must therefore contain the appropriate aggregation/effectiveness dependency on `selector:condition.applicability`.

## 9. Finding D-F7 — fact source class and cache identity must be part of invocation evaluation

**Severity: SIGNIFICANT cache/idempotency requirement; exact storage Step 3.**

The current cache rule correctly includes state-view identity and bound accessor arguments, but invocation-adjudicated facts are not part of the current structured contract.

If an invocation-derived calculation is allowed to use facts, cache identity must also distinguish the accepted fact-input set/fingerprint. Otherwise:

```text
same committed state view
+ same actor/target
+ different adjudicated visibility fact
```

could incorrectly reuse one derived result.

State-derived calculations avoid this problem by forbidding invocation facts. Invocation-derived calculations need their accepted fact inputs fixed/provenanced by Step 3 and included in calculation/context identity.

## 10. Finding D-F8 — scheduled-trigger read boundary remains narrow after attack

**Severity: NONE / KEEP.**

The critic target from Slice C does not require a new selector/accessor/query concept.

A due scheduled trigger needs:

- owning Effect identity;
- its definition/local trigger key;
- bound target/source/rules-origin/declared parameters;
- due occurrence/temporal context;
- ordinary hydrated state for the resulting Activity.

All can be supplied through existing owner bindings plus Step-3 execution context. If the child Activity requires an LLM-adjudicated fiction fact, it must obtain it through the same registered fact path as any other Activity and may suspend/ask rather than querying fiction itself.

No privileged `scheduled_trigger.query` or general temporal accessor is justified.

## 11. Finding D-F9 — domain-query determinism needs one explicit result-order rule

**Severity: MODERATE / likely mechanical clarification.**

The accepted query contract forbids arbitrary filters, but it does not explicitly say what a multi-result query returns when mechanical semantics do not impose an order.

A query that returns several Effect application IDs for removal/arbitration/support must not let SQL/index iteration order become a mechanical tie-breaker.

Required rule:

- query API returns an **unordered semantic set** unless its specific registered contract defines a mechanical order;
- any deterministic serialization/trace sort is representational only;
- an operation needing non-commutative selection must use a registered comparator/choice/adjudication contract rather than `first()`.

This is consistent with existing arbitration/trigger principles and does not require a human tradeoff.

## 12. Coverage against Task Charter

| Charter area | Coverage | Notes |
|---|---|---|
| calculation vs read vs runtime lookup | SATISFIED | three-surface split survives |
| direct vs derived engine authority | SATISFIED | accessor metadata present |
| arbitrary path/eval rejection | SATISFIED | typed accessor refs; no generic query syntax |
| invocation-adjudicated fact registry | MISSING | D-F1 |
| engine-owned facts cannot be LLM supplied | PARTIAL | prose correct; examples contradict D-F2 |
| explicit false vs missing fact | MISSING | D-F3 |
| state-stable/reconstructable calculations | MISSING | D-F4 |
| pinned committed/prospective view | SATISFIED | exact representation Step 3 |
| scoped concrete DAG | SATISFIED conceptually | machine metadata partial D-F5 |
| current Condition applicability | PARTIAL | Slice-B prose accepted; pipeline metadata missing D-F6 |
| source-relative Condition mechanics | SATISFIED | per-effective-application bound context |
| scheduled-trigger read boundary | SATISFIED | no privileged query/read surface |
| domain-query closure | SATISFIED conceptually | implementation audit later |
| domain-query result-order semantics | IMPLICIT | D-F9 clarification |
| cache isolation across state views | SATISFIED | accepted invariant |
| cache isolation across invocation facts | MISSING | D-F7 |
| common-path bounded performance | SATISFIED architecturally | scoped hydration/DAG/indexes |
| restart reconstruction | PARTIAL | state-derived distinction missing D-F4 |

## 13. Recommended correction package before adversarial acceptance

The lightest coherent package appears to be:

1. add structured registered context-fact metadata;
2. restrict facts to non-engine-owned invocation-adjudicated inputs;
3. define explicit true/false/missing semantics, with exact command encoding deferred to Step 3;
4. add selector evaluation class and prohibit invocation facts transitively from `STATE_DERIVED` selectors;
5. replace the bare derived-node-kind list with structured static dependency metadata;
6. encode current Condition aggregation/effectiveness dependency on `condition.applicability`;
7. include accepted invocation-fact fingerprint in invocation-derived context/cache identity;
8. specify domain-query multi-result outputs as unordered semantic sets unless a typed query contract defines order;
9. remove/repair engine-owned `fact` examples.

This does **not** require:

- a generic expression language;
- a generic query registry exposed to content;
- a new canonical fact entity;
- storing every LLM adjudication in world state;
- a global evaluation order;
- a global dependency graph;
- a new scheduled-trigger context subsystem.

## 14. Alternatives considered

### A. Ban invocation-adjudicated facts from all mechanics

Simplest deterministic core, but HDM explicitly needs bounded fiction-dependent adjudication when exact tactical/world geometry is not engine-owned. It would force narrative judgments into fake canonical state or make ordinary improvised play impossible.

Rejected.

### B. Allow facts everywhere but persist every accepted fact

This could reconstruct results but turns invocation judgments into a broad durable fact/event subsystem and risks conflating fiction adjudication with world truth. Step 4 owns durable lore/knowledge, and most one-roll situational facts do not need world identity.

Rejected.

### C. Separate state-derived from invocation-derived calculations

Recommended. This preserves bounded LLM adjudication where needed while keeping continuously derived invariants reconstructable from engine-owned state.

### D. Use fixed global evaluation strata instead of structured dependency metadata + DAG

Already rejected by the human-approved selector/query architecture. The new findings do not undermine the scoped-DAG decision; they show that its machine metadata is incomplete.

## 15. Preliminary recommendation

**AMEND, not reopen.**

The core architecture is still sound: the missing pieces are machine-enforced input provenance/stability contracts and one Condition integration edge. No evidence currently requires changing the three-surface model, pinned views, hybrid DAG, or LLM/deterministic separation.

The strongest potential architecture question for the critic is whether the proposed `STATE_DERIVED` versus `INVOCATION_DERIVED` distinction is the minimum sufficient abstraction or whether a narrower per-selector `allows_invocation_facts` capability would express the same requirement with less taxonomy.

No human decision is requested yet. The adversarial pass must first determine whether that distinction changes product semantics or is mechanically forced by reconstructability.
