# Step 2 Health/Effect Selector and Query Review Resolution

Status: **PRELIMINARILY ACCEPTED — REVIEW FINDINGS RESOLVED**

Target branch: `feature/mechanical-runtime-hot-state`

Candidate design: `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`

Adversarial review: `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-adversarial-review.md`

Parent design: `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`

This resolution records the human-architect decision on the one material blocker from the adversarial review and mechanically resolves the remaining findings. Where this document conflicts with the candidate design, this document is authoritative for the remainder of Step 2.

No runtime implementation or final machine-schema migration is authorized by this checkpoint.

## 1. Human architecture decision — dependency-cycle model

The human architect approved **Hybrid registered dependency contracts plus a scoped concrete DAG**.

HDM does not impose one universal fixed evaluation stratum over all current and future mechanics. Instead:

1. each registered derived mechanical stage declares its typed dependency contract;
2. catalog/definition compilation validates that each mechanic uses only allowed dependency kinds;
3. hydration/prospective activation builds or incrementally extends the concrete dependency DAG for the relevant hydrated mechanical scope;
4. any prospective change that would create a mechanically relevant dependency cycle is rejected before commit;
5. runtime never relies on recursion order, cache order, SQL order, repeated-until-stable evaluation, or an implicit fixed point.

The graph must stay scoped to mechanically relevant hydrated state. A campaign-global graph rebuild for every calculation is explicitly rejected.

## 2. Dependency-node model

Cycle analysis covers every registered derived stage that can participate in a mechanical read/calculation chain, not only selectors and accessors.

Initial node kinds include at least:

```text
selector:<id>
accessor:<id>
effect_availability:<typed contract>
effect_arbitration:<typed contract>
condition_aggregation:<typed contract>
```

Future derived stages may participate only by becoming registered typed node kinds with declared dependency rules.

Node kind is part of identity. A semantic stem such as `health.maximum` may appear in more than one typed surface only when its surrounding registry/field makes the surface unambiguous. Internal graphs, diagnostics, schemas, traces, and cache keys must not collapse `selector:health.maximum` and `accessor:health.maximum` into one bare-string node.

## 3. Static and concrete validation

Two validation layers are required.

### 3.1 Static registry/definition validation

Compilation validates:

- selector/accessor/derived-stage IDs exist;
- argument and subject kinds are legal;
- a consumer may read only dependency classes explicitly allowed by its registry contract;
- a definition is internally acyclic where that can be proven without runtime bindings;
- no arbitrary path/filter/query expression can introduce undeclared dependencies.

### 3.2 Scoped prospective DAG validation

Independently valid definitions can form a cycle only when combined on one concrete Actor/target/procedure. Therefore a mechanically relevant prospective activation must validate the resulting scoped graph before the state mutation commits.

Examples include applying/activating an Effect, enabling a Feature, materializing a Resource relationship, or another typed change that introduces dependency edges.

If the proposed graph is cyclic, the prospective change fails with a typed validation/integrity result. Runtime must never commit the state and discover the cycle during a later roll.

The exact incremental graph representation and invalidation algorithm are implementation-planning concerns, but the pre-commit acyclicity requirement is normative.

## 4. MechanicalContext revision pinning

The review blocker concerning logical immutability is accepted as a correctness correction.

Every `MechanicalContext` is bound to an explicit state-view identity sufficient to prevent silent cross-revision reads.

Conceptually:

```text
MechanicalContext
    state_view_kind = committed | prospective
    state_view_identity
    bound roles
    typed accessors/results
```

Implementations may realize `state_view_identity` through an immutable hydrated snapshot, revision token/vector, transaction-compatible snapshot, prospective overlay identity, or another Step-3-compatible mechanism.

Every lazy read must either:

1. resolve against the pinned state view; or
2. detect that its underlying view was invalidated and reject/rebuild the context before continuing.

It is forbidden to combine, for example, `health.current` from revision 20 with `health.maximum` derived from revision 21 inside one logical context.

Memoized accessor/cache keys therefore include the state-view identity plus bound arguments. A cache result from committed state may not leak into a prospective view merely because the same Actor/accessor IDs are used.

Step 3 owns the exact representation, prospective overlay construction, atomic commit, receipts, and ordering.

## 5. Condition semantics corrections

### 5.1 `condition.present`

`condition.present(subject, condition_id)` means:

> the named Condition is mechanically effective for the subject in this state view.

It does **not** mean merely that an application record exists.

Application existence/count/source/application IDs remain Effect-domain queries. Suppressed, shadowed, terminal, or otherwise non-effective applications do not make `condition.present` true unless the registered Condition aggregation contract explicitly defines the Condition as still mechanically effective.

### 5.2 `condition.value`

`condition.value` remains the narrow accessor for a mechanically effective typed value/level of a named Condition. Its exact cumulative/valued semantics remain owned by the bounded Exhaustion/valued-Condition nested design before Step-2 schema alignment.

### 5.3 Application calculation naming

The candidate name `condition.application` is superseded by:

```text
condition.applicability
```

This is a pure calculation selector answering whether/how a named Condition may apply to a target. It does not create an application or own mutation.

The ordinary Effect create/update/remove path remains the only Condition-application mutation path.

Exact legal Rule Element operations for `condition.applicability` are finalized during seed/schema alignment; `rule.immunity` is the initial proven candidate.

## 6. LLM-supplied mechanical facts

The candidate's ambiguous `reject/ignore` wording is corrected.

If an invocation attempts to supply an engine-owned `DIRECT_AUTHORITY` or `DERIVED_MECHANICAL` fact as adjudicated authority, the invocation fails typed validation.

Runtime does not silently ignore the supplied value and continue as though the request were well-formed.

After a valid request is established, engine-owned facts are resolved only from the pinned MechanicalContext/state view.

The LLM/host may provide only fact families explicitly registered as `INVOCATION_ADJUDICATED` or other approved non-engine-owned input classes.

This is an early local contract for the later LLM/deterministic-core integration design.

## 7. Closed runtime domain-query contracts

Runtime-only domain queries remain typed capabilities rather than executable catalog data, but their arguments must also stay closed.

Allowed query keys are operation/domain-specific typed keys such as:

```text
explicit target identity
concrete Effect application ID
named Condition identity
validated application family
source identity when the rule permits source filtering
registered removal/dispel policy
registered support relation lookup
registered boundary + scope/context
```

Domain queries may not accept arbitrary predicate trees, callbacks, SQL fragments, JSON paths, generic `where` objects, joins, or user-authored filters.

This prevents the internal query layer from becoming the rejected universal query DSL under another name.

## 8. Accessor subject-kind contracts

Each registered accessor declares legal subject/entity kinds in addition to argument/value types.

Initial examples:

```text
health.*
    -> Actor only

life.state
    -> Actor only

condition.*
    -> target kinds explicitly supported by the ruleset/Condition contract

resource.*
    -> lifetime-owner/binding kinds supported by Resource resolution
```

Invalid subject binding fails validation before evaluation.

A Zone/Asset/Location must not accidentally be accepted by an Actor-health accessor merely because all records share a generic world-record envelope.

## 9. `resource.available` boundary

`resource.available(subject, resource_id)` means the numeric Resource-domain quantity currently available in the pinned state view.

It does not answer whether a particular Activity is legally allowed to spend that Resource for a particular activation.

Activity eligibility, targeting, alternate eligible budgets, commitment point, and gate semantics remain Activity/Step-3 responsibilities.

This preserves the already accepted distinction between Resource state and Activity activation policy.

## 10. Naming and namespace maintenance rule

Machine names in current architectural drafts are not sacred when schema/catalog alignment has not yet canonicalized them.

If a name collision or misleading reuse is discovered and one entity clearly owns the better semantic name, the agent may perform the mechanically necessary rename across affected development artifacts without a separate human decision, provided that:

- product semantics do not change;
- ownership/boundary semantics do not change;
- no published external compatibility contract is being broken;
- references are updated consistently;
- the rename is recorded in the normal change history.

A rename that changes meaning, public compatibility, or architecture remains a human decision.

This rule applies to the current selector/accessor alignment as well as earlier provisional architecture names.

## 11. Duration/Recovery introspection remains YAGNI

No evidence currently requires a generic declarative `duration.remaining` or `recovery.next_due` accessor.

Duration/Recovery introspection remains a runtime/read-model concern unless a concrete seed mechanic proves another mechanical calculation must depend on such a value.

## 12. Updated authority/surface summary

```text
CALCULATION SELECTORS
    what calculation accepts Contributions?

    health.maximum
    condition.applicability
    resource.capacity
    resource.recovery
    effect.duration
    ...existing non-Step-2 selectors

MECHANICAL CONTEXT ACCESSORS
    what typed fact/value is visible in one pinned state view?

    health.current
    health.temporary
    health.maximum
    health.bloodied
    life.state
    condition.present
    condition.value
    resource.capacity
    resource.available
    owner_effect.parameter

RUNTIME DOMAIN QUERIES
    how does runtime locate the authoritative/derived objects required by a domain operation?

    Effect target/Condition/family/support lookups
    Resource lifetime-owner/state/recovery lookups
    Temporal/Boundary due/responder lookups
```

The surfaces remain non-interchangeable and none authorizes arbitrary world querying from declarative content.

## 13. Repeat adversarial pass after corrections

A second critical pass was performed against the corrected design.

### Attack: hybrid DAG is more complex than fixed strata

True. The hybrid model adds incremental dependency bookkeeping and pre-commit validation. However, strict fixed strata would encode a global evaluation direction before the complete mechanical seed and later architecture stages are known. The scoped-DAG cost is bounded to hydrated relevant mechanics and is preferable to either premature global ordering or implicit fixed-point semantics.

Disposition: **accepted trade-off; no blocker**.

### Attack: a campaign-global dependency graph could become a performance regression

Correct. The architecture therefore explicitly forbids rebuilding a campaign-global graph per calculation. Dependency validation/caching must be scoped to the relevant hydrated Actor/target/procedure and affected graph component.

Disposition: **constraint added; implementation benchmark/verification remains future work**.

### Attack: pinned contexts could be expensive if implemented as full deep copies

Correct, but the architecture requires logical state-view pinning, not eager deep copying. Revision tokens, immutable hydrated objects, overlays, or database snapshot techniques remain available to Step 3.

Disposition: **no blocker**.

### Attack: Condition effectiveness could itself depend on rules that read the same Condition

Covered by the expanded registered dependency-node model. Any such dependency participates in the scoped DAG and is rejected if cyclic. There is no implicit self-stabilizing Condition semantics.

Disposition: **resolved**.

### Attack: runtime-only domain queries could quietly regain arbitrary expressiveness

Closed operation/domain-specific typed keys are now normative; generic filters/callbacks are forbidden.

Disposition: **resolved**.

### Repeat-pass verdict

No unresolved blocker remains in the health/effect selector/query boundary after the approved hybrid-DAG decision and the corrections above.

The primary implementation risks are bounded DAG invalidation/cache correctness and state-view pinning efficiency. Both are explicit and testable; neither changes the accepted architecture.

## 14. Preliminary acceptance

The Step-2 health/effect selector/query sub-block is **PRELIMINARILY ACCEPTED** for current sequencing with these decisions:

- calculation selectors, Mechanical Context accessors, and runtime domain queries remain separate surfaces;
- engine-owned mechanical facts cannot be asserted by the LLM;
- MechanicalContext reads are pinned to one state-view identity;
- direct and derived values remain separate and derived values are not stored as canonical aliases;
- dependency freedom uses registered contracts plus a scoped concrete DAG with prospective pre-commit validation;
- Effect availability, Effect arbitration, and Condition aggregation participate in dependency analysis;
- `condition.present` means effective named Condition state;
- `condition.applicability` is the pure Condition-application calculation selector;
- domain queries accept only closed typed contracts;
- subject/entity kinds are validated;
- `resource.available` remains Resource-domain quantity rather than Activity eligibility;
- generic Effect stacks remain removed absent real seed evidence;
- generic Duration/Recovery declarative introspection remains deferred under YAGNI.

## 15. Next continuation

The exact next Step-2 design item is the bounded **valued/cumulative Condition semantics** analysis, with D&D Exhaustion as the required seed case.

After that nested item, Step 2 proceeds to schema/catalog alignment, focused validation cases, and the final independent Step-2 critical pass.
