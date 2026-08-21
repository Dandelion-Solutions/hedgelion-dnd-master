# Adversarial Review — Step 2 Health/Effect Selectors and Query Boundaries

Status: **REVIEW COMPLETE — RESOLUTION PENDING**

Reviewed candidate: `DEV/docs/superpowers/specs/2026-08-19-step-2-health-effect-selector-query-boundary-design.md`

Related architecture:

- `DEV/docs/superpowers/specs/2026-08-18-step-2-mechanical-state-ownership-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-effect-application-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-lifestate-policy-transition-design.md`
- `DEV/docs/superpowers/specs/2026-08-19-step-2-recovery-boundary-b2-design.md`
- `DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md`
- `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`
- current Step 2 catalog/schema baseline

Review stance: assume the candidate contains hidden coupling, duplicate authority, ambiguous timing, performance traps, LLM/runtime authority leaks, or an unnecessary abstraction. Look for concrete failure modes rather than stylistic objections.

## Verdict

The three-surface split is sound and no finding justifies replacing it with a universal query DSL.

Two blocking corrections are required before preliminary acceptance. One is a material architecture choice: how dependency-cycle freedom is enforced across calculations and active mechanics. The other is a missing enforceable state-view invariant. Several significant wording/contract corrections should be applied mechanically once the dependency decision is resolved.

## BLOCKING B1 — dependency graph excludes derived Effect/Condition participation machinery

### Failure mode

The candidate requires selector/accessor dependency-cycle rejection, but the actual mechanical graph also contains nodes that are neither ordinary selector outputs nor simple accessors:

```text
Effect availability/suppression
Effect arbitration participation
Condition aggregation/effective value
```

A cycle can therefore bypass the stated graph.

Example:

```text
Effect A availability
    depends on condition.present(X)

condition.present(X)
    depends on participating application X

application X participation/availability
    depends on a value contributed by Effect A
```

Another example:

```text
health.maximum
    depends on Effect A contribution
Effect A availability
    depends on condition.present(X)
Condition X effectiveness
    depends on health.bloodied
health.bloodied
    depends on health.maximum
```

If only selectors and accessors are graph nodes, the runtime can still recurse, oscillate, or depend on cache/evaluation order.

### Required correction

The dependency model must cover every derived mechanical stage that can participate in a read/calculation chain, including:

- calculation selector resolution;
- context accessor derivation;
- Effect availability/suppression derivation;
- Effect arbitration participation;
- Condition aggregation/effective-value derivation;
- any future registered derived stage permitted inside predicates/calculations.

No hidden fixed-point semantics are allowed.

### Architecture choice

Two viable approaches remain:

**A. Strict global strata**

Assign every derived stage to a fixed rank and permit reads only from lower ranks.

Advantages: simple validation, cheap runtime, cycles structurally impossible.

Costs: can reject legitimate future mechanics solely because their dependency direction was not anticipated; changing strata later becomes a broad compatibility concern.

**B. Hybrid registered dependency contract + concrete DAG validation (RECOMMENDED)**

The registry defines allowed dependency classes/edges. Compilation validates each definition. Hydration/prospective application builds or incrementally extends the concrete scoped dependency DAG for the relevant active mechanics and rejects any would-be cycle before commit.

Advantages: preserves explicit bounded dependencies without over-freezing one universal evaluation order; handles cycles created only by combinations of independently valid Effects/Resources.

Costs: more compiler/runtime bookkeeping; active dependency graphs must be cached/incrementally invalidated and application can fail if a newly combined mechanic creates a cycle.

### Severity

**BLOCKING**. Without one of these contracts, deterministic evaluation is not guaranteed.

## BLOCKING B2 — logical MechanicalContext immutability is not operationally pinned

### Failure mode

The candidate permits lazy accessor evaluation against HOT/SQLite indexes and says all reads observe one immutable state view. However, if the underlying records/indexes mutate between two lazy reads, different accessors can observe different revisions even though the context object itself did not change.

Example:

```text
context reads health.current at revision 20
another operation mutates Effect state to revision 21
same context later derives health.maximum from revision 21
```

The resulting `health.bloodied` can combine facts from two worlds.

### Required correction

A MechanicalContext must be bound to an explicit state-view/revision identity. Implementations may choose transactions, immutable hydrated snapshots, revision vectors/tokens, or equivalent mechanisms, but every lazy read must either:

- resolve against the same pinned view; or
- detect invalidation and reject/rebuild the context before continuing.

Silent cross-revision reads are forbidden.

Step 3 may choose the exact representation. Step 2 must make the invariant normative.

### Severity

**BLOCKING**, but no product decision is required; this is a correctness correction.

## SIGNIFICANT S1 — dynamic cycle validation must occur before a new mechanic is committed

A definition can be acyclic in isolation and create a cycle only when combined with already active mechanics on a concrete target/procedure.

Therefore catalog compilation alone is insufficient. Under the recommended hybrid model, Effect/Feature/Resource activation or other prospective changes that extend the mechanical dependency graph must validate the resulting scoped graph before commit.

Failure must reject the prospective mechanic with a typed validation/integrity result. Runtime must never commit the state and discover the cycle only on the next calculation.

## SIGNIFICANT S2 — `condition.present` is semantically ambiguous

The candidate says it derives from nonterminal/eligible applications plus Condition aggregation, but `present` could mean either:

1. at least one application record exists; or
2. the named Condition is mechanically effective in the current state view.

Declarative D&D rules need the second meaning.

Recommended correction:

```text
condition.present(...)
    = mechanically effective named Condition in this state view
```

Application existence/count/source IDs remain domain-query concerns. A suppressed/shadowed/non-effective application must not make `condition.present` true unless the Condition aggregation contract explicitly says the Condition remains effective.

## SIGNIFICANT S3 — `condition.application` sounds like mutation ownership

The proposed selector is pure, but its name can be read as the operation that creates the Condition application. That weakens the separation between calculation and mutation.

Recommended rename:

```text
condition.applicability
```

It calculates the target's typed allow/block/applicability disposition for a named Condition. Ordinary Effect creation remains the mutation path.

The existing `rule.immunity` operation can be legal for this selector if schema/seed validation confirms the operation value contract.

## SIGNIFICANT S4 — LLM engine-owned fact behavior must be reject, not `reject/ignore`

The candidate currently allows wording equivalent to “reject/ignore as authoritative input.” Ignoring is unsafe because a malformed ActionRequest could appear successful while the caller believes its supplied fact was used.

Recommended correction:

- an invocation that tries to supply an engine-owned fact/accessor as adjudicated authority fails typed validation;
- runtime then derives engine-owned values only in a valid request;
- caller may provide ordinary natural-language context separately, but it cannot smuggle mechanical truth through `context_facts`.

## SIGNIFICANT S5 — runtime domain queries need closed match contracts

`applications matching a removal/dispel contract` is too open-ended unless the contract itself is closed.

Otherwise it can become the universal query DSL under another name.

Recommended correction: domain query families accept only registered typed keys appropriate to that operation, for example explicit target, concrete application ID, named Condition identity, validated application family, source identity when the rule permits it, or a registered removal policy. No arbitrary predicate tree/filter callback is accepted by the domain query layer.

## SIGNIFICANT S6 — accessor subject-kind constraints must be explicit

`health.current(target)` is invalid if `target` is a Zone/Asset/Location. The registry therefore needs allowed subject/entity kinds in addition to argument names and value types.

Examples:

```text
health.*       -> Actor only
life.state     -> Actor only
condition.*    -> mechanically condition-capable target kinds defined by ruleset contract
resource.*     -> owner kinds accepted by the Resource resolver
```

Invalid binding kinds fail before evaluation.

## SIGNIFICANT S7 — `resource.available` must not absorb Activity eligibility

The accessor should mean the numeric amount currently available under Resource semantics, independent of whether a particular Activity is allowed to spend that Resource.

Otherwise action eligibility, targeting, resource-gate policy and Resource state collapse into one value.

Recommended correction:

```text
resource.available
    -> resource-domain spendable quantity under the current state view

activity/resource eligibility for this activation
    -> Activity/Step-3 gate semantics
```

Restricted extra action-economy budgets remain separate Resource definitions as already accepted.

## SIGNIFICANT S8 — registry node identity must preserve surface kind

The design currently uses strings such as `health.maximum` as both a calculation selector and a resolved context accessor.

That can be valid, but internal dependency graphs, diagnostics and schemas must distinguish:

```text
selector:health.maximum
accessor:health.maximum
```

or equivalent typed node identity.

Do not infer node kind from a bare string after parsing. Serialized user-facing IDs may reuse the semantic stem only when the surrounding typed field/registry makes the surface unambiguous.

## MINOR M1 — source traceability should be added

The candidate should record the existing project design bases used to justify the new surface: selected D&D/SRD rules for Bloodied, Condition Immunity and valued Conditions/Exhaustion, plus the existing Rule Element/Activity architecture. This is documentation/evidence traceability, not a design change.

## MINOR M2 — naming alignment remains pending

Existing documents use variants such as `actor.hp.maximum` while the candidate uses `health.maximum`. Schema/catalog alignment should choose one canonical machine spelling and update normative references deliberately rather than retain synonyms.

## MINOR M3 — context caching requires state-view-aware keys

Memoized accessor results must include the state-view identity and bound arguments. A cache keyed only by Actor/resource/accessor can leak a committed result into a prospective view.

## MINOR M4 — Duration/Recovery introspection is correctly deferred

No evidence currently requires generic declarative `duration.remaining` or `recovery.next_due` accessors. Runtime/read-model introspection should remain domain-owned unless full-seed validation proves a mechanical predicate dependency.

## Cross-system review

### Step 3

The candidate is compatible with Step 3 if Step 3 owns prospective state-view construction, state-view identity, atomic commit, idempotency and typed failure/receipt behavior. Dependency validation of a prospective new mechanic must run before its mutation segment commits.

### Step 4 / LLM context assembly

The engine-owned/adjudicated source-class separation is useful groundwork. Step 4 must not equate “LLM can be shown a read value” with “LLM may assert that value back as authority.” Read visibility and write/adjudication authority are separate permissions.

### Step 5

Cross-scene/multiplayer projections must preserve state-view/revision semantics. Disposable indexes may be rebuilt, but the same MechanicalContext cannot silently span conflicting revisions.

### Performance

The recommended hybrid dependency DAG is feasible only if scoped to hydrated/relevant mechanics and incrementally cached. A campaign-global graph rebuild for every roll would be an architecture regression.

## Resolution recommendation

1. Human architect decides B1: strict strata vs hybrid registered dependencies + scoped concrete DAG. Recommend **hybrid**.
2. Apply B2 and S1-S8 as specification corrections; none requires a product-semantic decision once B1 is chosen.
3. Add source traceability/naming notes from M1-M3.
4. Keep M4 as the current YAGNI position.
5. Re-run a short critical consistency pass after amendment.
6. Then mark the selector/query sub-block preliminarily accepted and proceed to the valued-Condition/Exhaustion nested design before machine schema/catalog alignment.
