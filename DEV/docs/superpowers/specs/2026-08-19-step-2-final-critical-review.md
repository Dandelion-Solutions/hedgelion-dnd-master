# Final Critical Review — Step 2 Mechanical State Architecture

Status: **FINAL REVIEW COMPLETE — NO UNRESOLVED STEP-2 BLOCKER**

Target branch: `feature/mechanical-runtime-hot-state`

Review scope: the integrated Step-2 architecture for Resources, HP/LifeState,
Effects, Conditions, Duration, Recovery, selector/query boundaries, and the
aligned machine schemas/catalogs/tests.

This review is authoritative for Step-2 closure where it records corrections to
earlier preliminary/candidate wording. Historical design documents remain
valuable reasoning records; superseded machine-shape examples are not alternate
contracts.

## 1. Review method

The pass attacked the integrated result rather than re-reviewing one local spec.
It checked:

- duplicate or missing authority;
- cross-spec/schema contradictions;
- HP/LifeState/Condition interactions;
- Effect application/reapplication/arbitration/support/Condition aggregation;
- Resource lifetime/storage/recovery;
- Duration/boundary/Temporal Agenda semantics;
- selector/accessor/domain-query boundaries and dependency cycles;
- LLM versus deterministic-core authority;
- committed/prospective revision consistency;
- recovery/checkpoint dependencies;
- performance/index implications and YAGNI;
- accidental freezing of Step-3/5 responsibilities.

The review also used focused RED→GREEN contract tests for every machine-level
mismatch found during this pass.

## 2. Final verdict

The integrated Step-2 architecture is internally coherent after the corrections
below.

No unresolved BLOCKING or SIGNIFICANT finding remains that belongs to Step 2.
The remaining open work has an explicit later-stage owner and does not require a
second Step-2 authority or an unspecified state model.

The central ownership invariants survive the integrated review:

```text
Actor HP state               -> HP authority
Actor LifeState state        -> lifecycle authority
ResourceState owner          -> Resource mutable authority
Effect application           -> application/lifecycle/provenance authority
Condition aggregation        -> derived named-Condition meaning
TemporalBinding              -> concrete temporal obligation authority
Temporal Agenda              -> rebuildable due-index only
MechanicalContext            -> one pinned read view
LLM                           -> no engine-owned mechanical authority
```

## 3. Findings discovered and resolved in this final pass

### B1 — source-relative Condition TriggerBinding had no machine binding

**Severity:** BLOCKING machine-contract mismatch.

`per_effective_application` intrinsic Condition rules may depend on the concrete
Condition source/target, but `TriggerBinding` originally allowed only owner and
Signal/Event roles.

**Resolution:** the closed TriggerBinding binding vocabulary now includes:

```text
condition.source
condition.target
```

No generic role/query path was introduced.

A focused test first failed on the missing binding and then passed after the
schema correction.

### B2 — Condition-owned automatic boundary response was missing

**Severity:** BLOCKING machine-contract mismatch.

Recovery B2 removed `RestPolicy.recovery_steps` and made each state owner own
its automatic response. Resource and Effect paths existed, but the Condition
schema had no path for an automatic response such as D&D Exhaustion losing one
eligible level after a successful Long Rest.

**Resolution:** `definition.condition` now supports closed
`automatic_boundary_responses`. The initial proven operation is:

```text
condition_response.remove_count
```

with a registered boundary and positive count. Exhaustion can therefore own:

```text
boundary.long_rest_complete
    -> remove_count(1)
```

This does not make RestPolicy a Condition mutator. Selection among provenance-
sensitive eligible units remains Step-3 Resolution/adjudication behavior when
not mechanically determined.

### B3 — Effect reapplication machine shape lost matching semantics

**Severity:** BLOCKING machine-contract mismatch.

The accepted Effect design defines reapplication as two independent questions:

```text
which existing application episode matches?
what lifecycle action occurs: refresh or replace?
```

The first alignment incorrectly reduced this to one
`reapplication_policy_id = refresh|replace`, losing the match contract.

**Resolution:** machine shape is now:

```text
reapplication:
    match_policy_id
    action_id
```

Initial proven match policies:

```text
effect_reapplication_match.target_family
effect_reapplication_match.target_family_source
```

Initial actions:

```text
effect_reapplication.refresh
effect_reapplication.replace
```

The old single-field form is rejected. Absence of `reapplication` retains the
accepted default: create a new application.

### B4 — Resource lifetime and storage model were independently selectable

**Severity:** BLOCKING authority mismatch.

The first schema allowed invalid combinations such as:

```text
actor + spent
asset + spent
procedure + current
```

although the architecture already fixes persistent Actor/Asset state as
`current` and procedure-local state as `spent`.

**Resolution:** Resource definition schema now permits only:

```text
actor     + current
asset     + current
procedure + spent
```

Recovery operations are also storage-model compatible:

```text
current -> restore_to_capacity | restore_amount
spent   -> reset_spent
```

### B5 — Resource recovery had two encodings for boundary timing

**Severity:** SIGNIFICANT duplicate-representation risk.

The first schema accepted both:

```text
boundary_id = boundary.long_rest_complete
```

and:

```text
after = DurationSpec(kind = duration.boundary, ...)
```

for the same semantic recovery edge, and even allowed nonsensical permanent
`after` specifications.

**Resolution:** direct `boundary_id` is the only boundary-based Resource recovery
form. `after` is restricted to a positive metric delay and materializes a
concrete recovery TemporalBinding. This preserves one boundary vocabulary and
one timing meaning.

### S1 — `condition.applicability` was broader than proven rules

**Severity:** SIGNIFICANT YAGNI/semantic overreach.

The initial metadata allowed `rule.immunity` plus generic `rule.override`.
Only immunity was proven by the current seed.

**Resolution:** initial selector contract is narrowed to:

```text
condition.applicability
    allowed operation = rule.immunity
    fixed contribution value = true
```

Future applicability transformations require a proven rule case rather than a
pre-authorized generic override language.

### S2 — field inventory and narrative architecture drifted behind schemas

**Severity:** SIGNIFICANT documentation/authority ambiguity.

Machine alignment removed old authorities while `ENTITY_STRUCTURES.md` and
related architecture text still contained provisional `target_ids`, stacks,
old Condition indirection, or outdated reapplication wording.

**Resolution:** current normative architecture docs and machine inventory now
use the aligned Step-2 contracts. Historical candidate/review documents remain
history, not alternate authority.

## 4. Conditions and Exhaustion after integrated review

The accepted two-axis model remains necessary and non-duplicative:

```text
ConditionAggregationPolicy
    presence
    cumulative_units

IntrinsicRuleScope
    aggregate_once
    per_effective_application
```

Aggregation decides effective named-Condition state/value/member applications.
Intrinsic scope decides evaluation cardinality/binding of one already-defined
intrinsic rule.

D&D seed cases remain representable:

```text
Poisoned
    presence + aggregate_once

Frightened / Charmed relational mechanics
    presence + per_effective_application(source)

Grappled
    one Condition mixing aggregate_once and per_effective_application rules

Exhaustion
    cumulative_units
    one effective application = one level
    per-unit fixed penalties via per_effective_application
    lethal threshold as aggregate crossing semantics
    Long Rest remove-one via Condition-owned boundary response
```

The committed Exhaustion value remains bounded to 0..6. A prospective plan must
normalize/reject excess gain before commit; exact same-segment ordering is Step
3.

## 5. Effect model after integrated review

The following concepts remain separate:

```text
application identity/lifecycle/provenance
reapplication matching + refresh/replace action
availability/suppression
Effect arbitration participation
Condition aggregation participation
Rule Element contribution combination
maintained support relation
```

No generic mutable Effect stack or universal uniqueness subsystem reappears.

One independent target-local application remains one `world.effect` with one
`target_id`. Maintained/concentration support remains the immutable parent
relation and is not a Duration mode.

## 6. Temporal and recovery model after integrated review

One semantic boundary has one registered identity. Producers establish the
occurrence; state owners respond through closed domain contracts.

```text
RestPolicy
    -> successful-rest boundary producer only

Resource definition/state
    -> Resource automatic recovery

Condition definition/applications
    -> Condition automatic boundary response

Effect TemporalBinding
    -> Effect expiry

HP/LifeState ruleset contract
    -> health/lifecycle response
```

Reusable `DurationSpec` and concrete `TemporalBinding` remain distinct.
Concrete temporal bases remain:

```text
metric deadline
procedure boundary
semantic boundary
```

The Temporal Agenda remains a rebuildable index over authoritative bindings and
checkpointed runtime state, not a scheduler authority.

## 7. Selectors, accessors, and dependency evaluation

The three-surface separation survives final review:

```text
Calculation Selector
MechanicalContext accessor/fact
runtime-only Domain Query API
```

Engine-owned reads use registered typed accessors. Arbitrary predicate `ref`
paths remain rejected. Runtime domain queries remain closed implementation
capabilities, not serializable content.

Dependency-cycle freedom remains:

```text
registered static dependency contracts
    +
scoped concrete DAG validation before prospective commit
```

The graph includes selector/accessor derivation, Effect availability,
arbitration, Condition aggregation, and Condition intrinsic evaluation. No
fixed-point/evaluation-order semantics are introduced.

## 8. Revision and LLM authority

Every `MechanicalContext` is pinned to one explicit committed/prospective
state-view identity. Lazy reads either use that view or detect invalidation;
they cannot mix revisions.

The deterministic core remains sole authority for engine-resolvable HP,
LifeState, Condition, Resource, Effect, and other registered mechanical facts.
An LLM/host attempt to supply such a fact as adjudicated authority fails typed
validation.

This is sufficient Step-2 groundwork; the full natural-language/typed-intent
integration remains a mandatory Step-3/4 cross-cutting design.

## 9. Deliberately deferred work with explicit owners

### Step 3 — execution boundary

Owns:

- exact IntentPlan/Resolution phase ordering;
- prospective overlay representation;
- atomic mutation segments;
- occurrence/event/receipt identity and idempotency;
- reaction/choice suspension/resume;
- exact trigger execution and chain bounds;
- source/provenance-sensitive remove-one selection/adjudication;
- prospective dependency-DAG validation invocation/typed failure behavior;
- checkpointable in-flight execution state and idempotent resume;
- typed LLM intent/reference binding boundary at the execution edge.

These are not missing Step-2 state authorities.

### Step 4 — context/lore boundary

Owns LLM context selection, durable truth/disclosure, and refinement of which
fiction-only facts may be adjudicated by the LLM without becoming engine-owned
mechanical truth.

### Step 5 — durability/multiplayer/time

Owns repository-backed runtime continuity checkpoint publication/restoration,
SOFT/HARD publication, cross-scene/multiplayer reconciliation, checkpoint
cleanup/expiry, and preservation of pinned revision semantics across shared
state.

### Step 6 — full rules seed and closure

Owns exhaustive D&D seed coverage/migration/catalog-gap closure. In particular,
the accepted HP/LifeState responder ownership must be seeded/verified for
concrete rules such as successful Long Rest restoring HP without moving that
responsibility into RestPolicy or ResourceState.

## 10. Verification evidence

The final pass used executable contract tests for:

- selector/accessor registry alignment;
- removal of old Step-2 authorities;
- Poisoned/Frightened/Grappled/Exhaustion schemas;
- LifeState state-local progress;
- one-target Effect state;
- typed predicate accessors and rejection of old arbitrary `ref`;
- Condition source/target TriggerBinding;
- Condition-owned Long Rest remove-one response;
- `condition.applicability` operation narrowing;
- Effect reapplication match/action separation;
- Resource lifetime/storage compatibility;
- Resource recovery operation compatibility;
- metric-only delayed Resource recovery versus direct boundary recovery.

After the last machine correction, the repository's full `Validate engine
source` workflow completed successfully, including the maintenance audit and all
DEV unit tests.

## 11. Closure recommendation

**Recommendation: close Step 2 and make Step 3 the single active roadmap stage.**

Confidence: **HIGH** for Step-2 ownership/boundary architecture.

What would reopen Step 2 later: a real rules seed or Step-3 integration case
showing that one of the settled state authorities cannot represent required
mechanics without duplicate authority, cyclic evaluation, arbitrary query
capability, or a hidden second scheduler/state store.
