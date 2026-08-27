# S6D-10 — Campaign Rulings / House-Rule Mechanical Boundary — Candidate Specification

Status: **STEP 6 REPAIRED CANDIDATE / RE-REVIEW PENDING**

Date: 2026-08-27

## 1. Scope and authority

This specification integrates the accepted Campaign House-Rules policy/adjudication boundary with the active S6D deterministic consumers.

It owns only:

- exact causal reference shape from accepted adjudicated inputs to applied durable policy revisions;
- bidirectional equality between current active adjudicated consumers and the S6D-10 integration ledger;
- fail-closed conformance proof for `realization_refs`;
- separation of current supported realization edges from nonselectable fixtures.

It does not own policy meaning/adoption, information eligibility, catalog admission, Activity execution, RNG, native state, publication, recovery or product support.

## 2. Exact policy-basis reference

Canonical serialized form:

```text
<policy_id>@<exact campaign revision>
```

Normative grammar:

```regex
^[A-Za-z][A-Za-z0-9_.:-]*@[a-f0-9]{40}(?:[a-f0-9]{24})?$
```

The 40/64-hex suffix names the exact campaign commit selecting both normative Markdown and the sidecar. The schema proves only the immutable locator shape. Before acceptance, the existing campaign publication/history resolver must prove that this exact revision exists, contains the named policy in the sidecar, resolves its normative source anchor, and carries accepted authority/applicability evidence. Recovery dereferences the historical revision, never current HEAD. Mutable branch names, labels such as `rev-3`, timestamps, source anchors alone and policy IDs without a revision are invalid.

The ref is causal linkage only. It does not copy normative text, prove adoption authority, admit a catalog definition or invoke a capability.

## 3. Typed adjudicated inputs

### 3.1 Richer Activity bindings

Every `INVOCATION_ADJUDICATED` binding retains required `policy_basis_refs`:

- `[]` — lawful one-off/contextual ruling with no durable policy materially applied;
- one or more exact refs — every durable current policy that materially contributed to the accepted value.

The binding remains validated against the exact Activity parameter declaration. Policy refs cannot widen type, cardinality, bounds, candidate set, consumer or authority.

### 3.2 Boolean invocation facts

Every accepted invocation fact retains the same required array. The fact value remains boolean and exact-consumer/binding/rules-context-scoped. Adding causal refs does not create persistent world/spatial truth, a policy lifecycle or a new input class.

Resolution/Continuation preserve these embedded values as accepted causal evidence. Later policy publication is forward-looking.

## 4. Finite active boundary

Current derived equality is:

```text
2 active richer parameter edges
+ 7 active boolean fact consumer edges
= 9 active adjudicated consumer edges
```

The verification-only ledger must equal the union derived from:

- identity-bound built-in package candidate members and their admitted architectural `INVOCATION_ADJUDICATED` parameter contracts; runtime selection remains blocked until S6D-11;
- active `mechanical-surfaces.context_facts[*].permitted_consumer_ids` edges.

The comparison uses complete normalized rows, not `edge_key` alone: source/value/cardinality/required/bounds for parameter edges and source/value/disposition for fact edges must agree. The identity-bound candidate tuple must match `character-capabilities.json`, and every declared content member byte digest is recomputed before deriving rows. The three route profiles preserve the full policy/authority/eligibility/consumer/provenance/freeze/catalog/native/RNG/mutation/execution/failure/retry/publication/proof/trigger obligations. Duplicates, field drift, digest drift, missing edges and orphan rows fail validation. The ledger grants no activation.

## 5. Durable policy realization

The built-in campaign template contains no adopted policies, therefore:

```text
current_supported_policy_realizations = []
```

Conformance fixtures remain in a separate collection and are always `CONFORMANCE_ONLY_NONSELECTABLE`.

For each realization ref:

1. the policy ref must be exact;
2. adoption/currentness/applicability is validated by existing policy owners;
3. the target must resolve through identity-verified package bytes and its owning admission/selection contract;
4. it must name an admitted definition/capability allowed by the exact consumer;
5. mention does not invoke it;
6. Activity binding, choice, target, cost, resource, RNG and mutation validations still run;
7. missing, stale, incompatible, dormant or quarantined target yields `failure.policy_realization_gap`/the owning finite mismatch;
8. semantic equivalence is not inferred from ID resolution alone.

The positive fixture proves only nonselectable identity-bound link shape (`CONFORMANCE_VALID_LINK_ONLY`); it proves neither admission nor exact-consumer realization, current package selectability or semantic equivalence. Those checks remain with S6D-11/current-context runtime and the exact eventual consumer. Primitive fixtures additionally inspect `selection_state` and `realization_state`, so a quarantined primitive cannot pass merely because its ID exists. No generic realization-status registry is persisted.

## 6. Failure semantics

| Failure | Result |
|---|---|
| missing required adjudicated input | `failure.adjudication_input_missing` or exact fact missing failure |
| wrong type/bounds/source/consumer | `failure.adjudication_input_invalid` / unauthorized |
| stale eligibility/rules/policy basis | `failure.adjudication_context_stale` |
| conflicting current policy | `failure.policy_conflict` |
| missing/stale/incompatible/dormant/quarantined realization | `failure.policy_realization_gap` or owning compatible mismatch |
| exact catalog context unavailable | `failure.catalog_context_incompatible` |

The six already accepted House-Rules failure IDs are synchronized into the core failure registry and the admission ledger; this candidate does not mint additional failure vocabulary. Every failure occurs before unauthorized RNG/mutation and introduces no fallback to prose or stale baseline mechanics.

## 7. Ownership and recovery

- House-Rules owner: policy semantics and exact revision meaning.
- Access control: adoption authority.
- Context Runtime/Step 4: information eligibility.
- Activity invocation validator: input acceptance and exact consumer binding.
- Resolution/Continuation: accepted causal input retention and retry identity.
- catalog context: definition/currentness resolution.
- primitives/native owners: calculation/RNG/mutation.
- ExecutionSegment/MechanicalEvent/receipt: commit fact/outcome evidence according to exact route.

No owner is duplicated by the integration ledger.

## 8. Machine artifacts

- `DEV/SCHEMAS/policy-basis-ref.schema.json`;
- amended `activity-parameter-binding.schema.json`;
- amended `invocation-fact.schema.json`;
- `DEV/CATALOG/house-rules-mechanical-boundary.json`;
- `DEV/SCHEMAS/house-rules-mechanical-boundary.schema.json`;
- `DEV/TOOLS/validate_house_rules_mechanical_boundary.py`;
- `DEV/TESTS/test_s6d_10_house_rules_boundary_contract.py`;
- exact `core-catalog.json` / `catalog-admission-ledger.json` six-ID synchronization described by `failure-registry-admission-amendment.json`;
- focused amendments to existing House-Rules/S6D-09/Step-3 fixtures.

## 9. RED→GREEN evidence

RED 1: validator absent; valid exact boundary test failed.

GREEN 1: minimal validator produced exact `9 / 0 / 3` summary.

RED 2: mutable revision labels, active-edge drift and missing/quarantined ref claiming valid linkage were accepted.

GREEN 2: exact-ref, bidirectional equality and realization expectation validation reject all three.

RED 3: shared policy-ref schema and invocation-fact retention were absent.

GREEN 3: one strict reusable reference schema now governs parameter and fact arrays.

RED 4: production ledger/schema absent.

GREEN 4: strict ledger/schema validate against exact source-derived edges with current realization set empty.

Step-6 critics found successive conformance defects. Repairs add strict unknown/member/enum/path checks, complete-row equality, candidate content-byte identity checks without false S6D-11 selection, primitive selection/quarantine checks, exact-revision resolver evidence, canonical lexicographic policy-ref ordering, a finite three-profile atomic route matrix, registered failure admission, actual-repository invocation, and retry/cold-recovery tests for two real exact consumers.

Focused local result after repair: **8 tests / 0 failures**. The canonical repository test additionally executes the strict Draft-2020-12 schema graph and actual repository validator, validates enriched values transitively through canonical Resolution and Continuation schemas, round-trips a Continuation checkpoint, and uses a conformance-only canonical hash to prove that a changed policy basis is distinguishable. Production RuntimeCommand/idempotency fingerprint ownership remains with Step 3.

## 10. Negative space

This design introduces no prose execution, policy DSL, generic homebrew authoring/package distribution, policy frontier, notification queue, scheduler, world query, arbitrary payload/path/patch, Signal/StateDelta lifecycle, dormant primitive activation or broad rules-content promise.

## 11. Candidate gate

Material human decision open: **0**

Candidate ready for renewed independent whole-project Step-6 adversarial review.

