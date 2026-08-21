# Step 2 Retrospective Assurance — Slice D Resolution

Status: **ASSURED / AMENDED / STEP 2 REMAINS CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-2-assurance-slice-d-mechanical-evaluation-task-charter.md`

Coverage/research: `2026-08-19-step-2-assurance-slice-d-mechanical-evaluation-coverage-research.md`

Adversarial review: `2026-08-19-step-2-assurance-slice-d-mechanical-evaluation-adversarial-review.md`

This resolution records the retrospective assurance corrections to Step-2 mechanical evaluation and read boundaries. No new human architecture decision was required: the amendments enforce already-approved authority/reconstructability constraints and choose the narrowest viable machine representation.

## 1. Verdict

The core Step-2 evaluation architecture survives:

```text
Calculation Selector
MechanicalContext accessor / registered invocation fact
runtime-only Domain Query
```

as do:

- one pinned committed/prospective state view;
- engine-owned mechanical authority in deterministic state/accessors;
- no arbitrary JSON-path/query/eval surface;
- hybrid registered dependency contracts plus a scoped concrete DAG;
- no fixed-point/evaluation-order semantics;
- scoped hydration/indexing rather than campaign-global scans.

The assurance found machine-enforcement gaps around invocation input provenance and one Slice-B Condition dependency. These are amended below.

## 2. Registered invocation facts are a closed input channel

Bare predicate facts are no longer an implied open namespace.

`CATALOG/mechanical-surfaces.json` now contains structured `context_facts` metadata. Initial facts are deliberately boolean and have one source class:

```text
INVOCATION_ADJUDICATED
```

The initial seed includes fiction-dependent examples:

```text
fiction.target_visible
fiction.target_reachable
```

Definition compilation must reject every `{ "fact": id }` that does not resolve to registered context-fact metadata.

Engine-owned state is forbidden from this channel. HP, LifeState, Condition state, Resource state, equipment state, and other engine-resolvable mechanics use typed accessors/calculations instead.

The earlier examples `source.equipped` and `actor.can_act` as LLM facts are superseded/removed.

## 3. Invocation fact truth semantics

Registered boolean invocation facts distinguish:

```text
explicit true
explicit false
missing / unavailable
```

Missing is not false.

If compiled mechanics reference an invocation fact not accepted for the invocation, runtime must return a typed missing-input/adjudication outcome rather than make `fact` false or make `not fact` true by absence.

Exact RuntimeCommand/ActionRequest field layout and provenance representation remain Step 3. Step 3 must preserve accepted fact values/provenance as fixed causal execution input across suspension/retry when required.

Accepted invocation facts do not automatically become canonical lore/world facts. Step 4 owns promotion of durable truth.

## 4. Input capability metadata replaces a broader calculation taxonomy

The coverage draft considered `STATE_DERIVED | INVOCATION_DERIVED` calculation classes.

The adversarial review rejected that taxonomy as unnecessary abstraction. The machine contract needs only the narrower question:

> which input provenance classes may this reviewed selector/derived stage consume?

Structured selector/derived-node metadata therefore uses:

```text
allowed_input_classes
```

with the initial vocabulary:

```text
ENGINE_STATE
INVOCATION_ADJUDICATED
```

This is capability metadata, not an additional state owner or general calculation ontology.

## 5. State-sensitive Step-2 selectors are engine-state-only

The current reviewed Step-2 selectors allow only:

```text
ENGINE_STATE
```

for:

```text
health.maximum
resource.capacity
resource.recovery
condition.applicability
effect.duration
```

The `effect.duration` restriction is intentionally conservative: no current Step-2 seed proves a need for invocation-adjudicated duration input. A later concrete seed may explicitly widen a selector rather than pre-authorizing the capability.

The key correctness case is persistent Resource capacity. Slice A requires a real capacity decrease to normalize stored `current`. Therefore `resource.capacity` cannot depend on an ephemeral LLM adjudication that would disappear after the invocation and make the canonical clamp unreconstructable.

The same principle applies transitively. A consumer that forbids `INVOCATION_ADJUDICATED` may not reach that input indirectly through an accessor or derived stage.

The existing scoped dependency DAG is the enforcement graph; HDM does not add a second provenance graph.

## 6. Structured derived-node metadata

The old machine field:

```text
derived_node_kinds: [ ... ]
```

is replaced by one structured registry:

```text
derived_nodes[derived_kind]
    allowed_dependency_kinds
    allowed_input_classes
    fixed dependencies
```

The object keys are the registry. There is no parallel dependency table that could drift.

Concrete source/target/application edges still belong to the hydrated/prospective DAG. Static metadata only describes the allowed/fixed architecture contract.

Initial nodes remain:

```text
effect_availability
effect_arbitration
condition_aggregation
condition_intrinsic
```

`condition_intrinsic` may admit `INVOCATION_ADJUDICATED` because relational Condition mechanics can depend on genuinely fictional context such as source visibility. Whether the eventual target selector also permits that input remains independently validated.

## 7. Current Condition effectiveness explicitly consumes applicability

Slice B established that Condition immunity applies to current effectiveness, not only pre-create validation.

The derived pipeline is therefore:

```text
nonterminal Condition application
    -> basic Effect availability/suppression
    -> selector:condition.applicability(target, condition)
    -> eligible Condition member set
    -> Condition aggregation
    -> Condition intrinsic mechanics
```

The structured `condition_aggregation` node now has fixed dependencies on:

```text
derived:effect_availability
selector:condition.applicability
```

No `applicable` boolean is stored in `world.effect`.

If a target gains Poisoned immunity after Poisoned was already applied, the application may remain live/timed while it no longer participates in effective Poisoned state. If immunity disappears before application termination, the same application can participate again without lifecycle resurrection.

A self-referential immunity/Condition combination that forms a concrete dependency cycle is rejected prospectively; runtime does not choose an evaluation order or fixed point.

## 8. MechanicalContext identity includes accepted invocation inputs when allowed

For state-only evaluation, context/cache identity contains at least:

```text
pinned state-view identity
bound roles/arguments
```

For a reviewed invocation-sensitive calculation, identity additionally contains the accepted invocation-input fingerprint necessary for that calculation.

Therefore two calculations over the same committed state but different accepted fiction facts cannot share one invocation-sensitive cache result.

The fingerprint is execution identity, not world authority.

## 9. Runtime Domain Query result ordering

Runtime Domain Query APIs remain closed infrastructure capabilities with typed domain-specific arguments.

If a query returns multiple results and its contract does not define a rules-significant order, the semantic result is an **unordered set**.

An implementation may sort IDs for deterministic serialization/tests, but that order cannot choose a winner or target.

Any non-commutative selection uses an explicit registered comparator, rules-owned controller choice, or typed adjudication requirement. SQL/index/list order is never gameplay semantics.

## 10. Scheduled-trigger integration

Slice-C owner-local scheduled triggers do not require another read/query surface.

A due trigger supplies the owning Effect/definition/local key plus normal bound target/source/application context. Step 3 creates ordinary Activity/Resolution execution and applies the same MechanicalContext/fact/accessor restrictions as any other Activity.

Temporal Agenda does not grant query capabilities. A due Activity that needs an unavailable invocation-adjudicated fiction fact must take the normal typed adjudication/suspension path rather than fabricate it or skip the mechanic.

## 11. Machine alignment and TDD evidence

Focused contract test:

- `DEV/TESTS/test_step2_evaluation_input_contract.py`

The RED pass was run against the pre-amendment machine contracts.

Expected failures were observed because:

- `context_facts` did not exist;
- selectors did not declare `allowed_input_classes`;
- `derived_nodes` did not exist;
- Condition aggregation had no structured current-applicability dependency.

The maintenance audit and all pre-existing tests remained green in the RED run, isolating the failure to the intended new contract.

The minimum GREEN alignment changed:

- `DEV/SCHEMAS/mechanical-surfaces.schema.json`;
- `DEV/CATALOG/mechanical-surfaces.json`.

The full `Validate engine source` workflow then passed with the new tests plus all existing DEV tests.

Current schema/examples and normative prose were subsequently aligned to remove engine-owned pseudo-facts and document the input semantics.

## 12. Carry-forward to Step 3

Step 3 must own the exact typed execution representation for:

- explicit invocation-fact boolean values;
- fact provenance/source;
- missing-input/adjudication failures;
- deterministic binder verification that engine-owned facts cannot be supplied through the fact channel;
- invocation-input fingerprinting inside command/Resolution/Continuation identity;
- preservation of accepted facts across suspension/retry;
- safe recomputation after reactions while retaining fixed accepted inputs;
- scheduled-trigger child Activity binding through the same fact/accessor contract.

The saved Step-3 research already includes accepted adjudicated facts + provenance in Resolution/Continuation state and therefore composes with this amendment.

## 13. Carry-forward to Step 4

Step 4 owns:

- which fiction/context facts may be exposed/adjudicated under knowledge/disclosure rules;
- promotion of a situational adjudication into durable lore/world truth when actually required;
- preventing secret information from entering invocation facts through context leakage.

The Step-2 fact registry is a mechanical input capability registry, not a lore truth store.

## 14. Carry-forward to Step 6

`core-catalog.json` contains more rule selectors than the current structured `mechanical-surfaces.json` metadata covers.

Full structured selector/input/dependency seed closure remains Step 6.

Until then:

- every bare context fact still must be registered;
- every selector that has structured metadata must enforce its input capabilities;
- an unstructured selector must not be assumed state-safe merely because detailed metadata is absent.

Future numeric/enum invocation facts require a proven rule case and review; the initial fact channel remains boolean under YAGNI.

## 15. Final disposition

Recommendation: **KEEP Step 2 closed with Slice-D amendments.**

Human decision required: **NO**.

Confidence: **HIGH**.

The assurance found missing machine enforcement, not a failed ownership model. The accepted three-surface split, pinned-view discipline, scoped hybrid DAG, and LLM/deterministic boundary remain the recommended architecture.
