# Implementation Planning — Catalog-Context Reconstruction Addendum

Status: **MANDATORY OVERLAY — AUTHOR FINDING 23 REPAIR / INDEPENDENTLY UNCONFIRMED**

Scope: planning only. This addendum does not authorize production implementation.

This overlay has higher precedence than the base RD-05, RD-06, RD-07 and RD-15 wording where those plans leave accepted `ResolvedCatalogContext` reconstruction implicit, fingerprint-only, or dependent on ambient/current catalog state.

## Finding 23 — SIGNIFICANT

The current package correctly introduces deterministic catalog binding in RD-15 and requires catalog-backed RD-05 acceptance to consume the RD-15 `SUPPORTED` result. It still fails to carry a reconstructive accepted catalog-context basis through durable accepted execution and recovery.

The gap is structural:

- the canonical Step-3 owner requires RuntimeCommand, Resolution and Continuation to bind one accepted compatible `ResolvedCatalogContext` identity;
- the catalog-resolution owner defines that context as engine capability identity + exact ruleset set + campaign-definition frontier + optional session-overlay frontier;
- the ruleset/package owner explicitly states that the catalog fingerprint is comparison/retry evidence and is **not** reconstruction authority;
- campaign/session definitions remain in their natural resolved catalog sources rather than becoming a new campaign-native record family;
- owner-local dependency references must retain definitions needed by retry/resume;
- active/unsettled accepted execution must retain accepted interpretation/dependency evidence;
- durable publication may not leave a durable reference to an unpublished session-only definition.

Current machine/planning surfaces do not close that chain consistently:

- `runtime-command-state.schema.json` stores only `catalog_context_fingerprint` for catalog basis;
- `runtime-resolution-state.schema.json` stores ruleset-set digest + catalog fingerprint, but not the owner-local definition dependency frontier needed to reconstruct the accepted context;
- `runtime-continuation-state.schema.json` has ruleset-set/fingerprint fields plus generic `dependency_frontier_refs`, but no typed catalog-context reconstruction contract and no package law making those generic strings the catalog basis;
- RD-15 plans a full logical `BoundCatalogContext`, but its durable `runtime.catalog_gap_report` minimum shape loses campaign/session dependency-frontier identity;
- RD-05 acceptance/resume APIs do not explicitly persist and compare one reconstructive catalog-context basis;
- RD-07 says accepted catalog/rules/dependency interpretation is preserved, but does not define the exact bounded reconstruction path;
- RD-06 does not explicitly prove that accepted execution cannot be published as recoverable while its required catalog dependency basis is not durably retained/protected.

A fingerprint-only retry/recovery path could therefore rebind accepted work against current/latest campaign/session definitions after those definitions change, move, disappear or remain unpublished. That would violate accepted execution identity even when a fingerprint mismatch is detected only after the original reconstructive source has already been lost.

## Owner-preserving realization

Do **not** create a global catalog-frontier owner, definition snapshot registry, universal reference graph, second ruleset loader, or new campaign native record family.

Realize one typed embedded value contract representing the reconstructive identity of the already accepted logical `ResolvedCatalogContext`:

```text
CatalogContextBasis {
    ruleset_set_digest_generation
    ruleset_set_sha256
    catalog_context_fingerprint_generation
    catalog_context_fingerprint
    catalog_definition_dependency_refs[]
}

CatalogDefinitionDependencyRef {
    owner_domain: CAMPAIGN | SESSION
    owner_scope_id
    definition_id
    source_route
    source_revision
}
```

Normative interpretation:

- `source_route` is the bounded natural-owner route for that definition in the selected campaign/session catalog source;
- `source_revision` is the exact immutable/pinned natural-owner revision/fence accepted for that dependency;
- neither field creates a second definition authority; the loaded definition must still validate its own identity/kind/capability under the accepted context;
- `source_route`/`source_revision` are opaque owner-qualified machine strings at this layer; do not encode Git-specific or host-specific authority into the value schema;
- ruleset-package reconstruction continues to use the existing exact ruleset-set identity/loader and is not duplicated into `catalog_definition_dependency_refs`;
- engine capability identity is validated by the existing engine/catalog compatibility contract and need not be copied as a new durable world/runtime owner;
- the dependency-ref array contains only campaign/session definitions actually required to reconstruct or retry the accepted material execution/gap evidence. It is not a copy of the whole resolved catalog and not a universal dependency registry;
- order is non-semantic; canonical serialization sorts the refs by `(owner_domain, owner_scope_id, definition_id, source_route, source_revision)` before computing any dependent fingerprint/input identity.

If execution-time owner evidence proves an already accepted reusable value contract expresses these exact semantics without ambiguity, reuse it rather than creating duplicate schemas. Otherwise create the two named schemas below.

## Required machine surfaces

### Shared embedded contracts

Create, unless an exact semantically equivalent accepted contract is proven at execution time:

- `DEV/SCHEMAS/catalog-definition-dependency-ref.schema.json`
- `DEV/SCHEMAS/catalog-context-basis.schema.json`

Both use Draft 2020-12 and `additionalProperties: false`.

`catalog-definition-dependency-ref.schema.json` requires all five fields above and rejects:

- an unknown owner domain;
- blank owner/scope/definition/route/revision values;
- an ambient branch/tag/latest marker used as `source_revision` when the natural owner cannot prove it immutable/pinned;
- a dependency whose loaded body does not validate the requested `definition_id` and accepted kind/capability contract.

The last two laws require deterministic code/tests in addition to structural JSON Schema validation.

`catalog-context-basis.schema.json` requires the exact ruleset-set identity, exact catalog fingerprint identity and a unique set of typed definition dependency refs. It is an embedded value, not a registered runtime kind.

### RuntimeCommand

Modify `DEV/SCHEMAS/runtime-command-state.schema.json` and RD-05 acceptance planning so an accepted catalog-backed RuntimeCommand persists one `catalog_context_basis` conforming to the shared schema.

The legacy fingerprint-only field may be removed or retained only as the exact fingerprint member of `catalog_context_basis`; it may not remain a second independently writable value.

`input_fingerprint` must be computed from the accepted normalized command input **including the canonicalized `catalog_context_basis`**, consistent with Step-3 idempotency law.

### Resolution

Modify `DEV/SCHEMAS/runtime-resolution-state.schema.json` so catalog-backed Resolution stores/references the exact same `catalog_context_basis` as its root accepted command.

Do not allow independently supplied ruleset/fingerprint fields to diverge from the root basis. If retained for projection/compatibility reasons, they are derived projections validated equal to the basis and have one writer.

### Continuation

Modify `DEV/SCHEMAS/runtime-continuation-state.schema.json` so one suspended generation persists the exact same accepted `catalog_context_basis`.

`dependency_frontier_refs` remains available for non-catalog execution dependencies. It is **not** the sole or implicit catalog-context reconstruction carrier and must not be overloaded to hide campaign/session catalog dependencies.

Resume uses the stored accepted basis before consulting ambient/current catalog state.

### Catalog gap report

Modify the RD-15 planned `runtime-catalog-gap-report-state.schema.json` so a durable unsupported-capability report stores the same `catalog_context_basis` (or an exact lossless projection of it if the report is proven not to need a subset of dependencies).

The preferred v1 form is reuse of `catalog-context-basis.schema.json` to prevent a second near-equivalent contract.

This preserves the exact context in which deterministic validation proved the capability unsupported.

## RD-15 binding law

`BoundCatalogContext` and `ExecutableCatalogBinding` must expose the typed `CatalogContextBasis` used for deterministic validation.

`bind_executable_catalog(...)` may return `SUPPORTED` only after:

1. the exact ruleset-set basis is validated through the existing S6D package loader/lock contract;
2. every campaign/session definition selected as mechanically material has an exact natural-owner dependency ref;
3. every dependency ref exact-loads the requested `definition_id` and validates its kind/capability under the same accepted context;
4. the canonical fingerprint recomputed from that exact basis equals the accepted catalog-context fingerprint;
5. no dependency requires an unpublished session-only definition to be referenced by durable accepted execution.

For item 5, RD-15 must not silently promote, copy or rename the definition. If a material command would durably depend on a session-only definition without an owner-approved durable publication/promotion basis, return a typed non-supported/blocking outcome before RD-05 acceptance. A later owner-approved promotion may preserve `definition_id` under the existing catalog owner contract and then permit a new binding attempt.

Search miss, model memory, current filesystem contents, mutable tags, latest-looking files and ranking order are never reconstruction evidence.

## RD-05 accepted execution join

Supersede the loose catalog-backed intake with an explicit accepted binding:

```text
accept_command(
    interaction,
    intent_plan,
    command_request,
    executable_catalog_binding,
    acceptance_basis,
) -> RuntimeCommand
```

For catalog-backed mechanics, `executable_catalog_binding.disposition` must be `SUPPORTED` and the command copies the exact canonical `catalog_context_basis` from that binding.

Resolution creation, child Resolution creation, Continuation creation/resume and accepted firing execution must preserve equality of the accepted basis. They may add owner-local state/revision dependencies, but may not rebind catalog definitions against ambient/current catalog state.

A mismatch between command, Resolution or Continuation catalog basis is an integrity/compatibility failure, not an invitation to choose the newest context.

## RD-06 durability/publication join

Accepted catalog dependency evidence is a correctness-required durability/recovery dependency, not an optional diagnostic.

Extend RD-06 focused integration proof so a SAVE/publication result cannot claim an accepted catalog-backed command/resolution/continuation is durably recoverable unless:

- its exact `catalog_context_basis` is included in the frozen correctness-required closure;
- every owner-local definition dependency required by that basis has a durable retained natural-owner source or an already accepted survivor/promotion basis;
- no durable accepted execution references an unpublished session-only definition;
- publication of owner-local definition changes/removals cannot strand an unsettled accepted execution whose retained basis still requires the prior definition source.

Do not solve this with a universal reference count, campaign-wide catalog snapshot, all-history scan or global GC graph. The accepted execution itself is the typed consumer/protection source; use bounded owner-qualified dependency refs and the existing Step-5.13 retention/protection laws.

## RD-07 recovery join

Extend `AcceptedExecutionRecoveryTests` and recovery planning with:

```text
reconstruct_accepted_catalog_context(catalog_context_basis)
    -> ExactResolvedCatalogContext | BLOCKED
```

Required behavior:

1. resolve the exact ruleset set from the stored ruleset-set identity using the existing package loader/retained package snapshots;
2. exact-load every campaign/session definition dependency via its owner-qualified route and pinned revision;
3. validate requested `definition_id`, kind/capability compatibility and owner/source identity;
4. reconstruct the accepted logical context from those exact inputs;
5. recompute/validate the accepted catalog-context fingerprint;
6. only then resume/retry the accepted command/resolution/continuation.

Missing retained source, incompatible definition, moved/unpinned route, mismatched fingerprint or non-resolvable required dependency returns typed `BLOCKED` / compatibility/integrity failure. Recovery must never substitute current/latest definitions, search for an approximate replacement, rewrite the definition ID, or silently execute under a different context.

## Step-5.13 retention/protection join

While accepted execution remains unsettled or otherwise retry/resume-capable, its required `CatalogDefinitionDependencyRef` targets are protected interpretation/dependency evidence.

The implementation plan must prove:

- the consumer registers/maintains the bounded protection relationship before/with accepted durable dependence;
- source replacement/promotion establishes an accepted survivor before old required representation becomes retirement-eligible;
- cleanup cannot infer safety from stale/missing protection routing;
- terminal execution may later release the protection only under the accepted idempotency/audit/causal-retention contracts; terminality alone does not imply immediate deletion.

No new global cleanup authority is introduced.

## Exact TDD obligations

Use the existing RD test modules; create new classes at the task that owns each RED→GREEN cycle, never pre-materialize future-task failing groups.

### RD-15 — `CatalogContextBasisContractTests`

Prove:

- shared basis/dependency-ref schemas accept exact owner-qualified refs and reject incomplete/ambient refs;
- same selected definitions but different owner revision/frontier are distinct reconstructive bases even if a buggy caller supplies the same fingerprint string;
- deterministic binder returns one canonical basis and fingerprint;
- a session-only material dependency with no durable promotion/publication basis cannot yield durable `SUPPORTED` binding;
- a promoted/published definition may be rebound only through the normal exact owner path, not by implicit promotion inside the binder.

### RD-05 — `AcceptedExecutionCatalogBasisTests`

Prove:

- catalog-backed command acceptance requires RD-15 `SUPPORTED` binding;
- RuntimeCommand persists the binding basis;
- root/child Resolution and Continuation carry an exactly equal basis;
- retry compares accepted basis before ambient rebinding;
- different basis with otherwise identical command input is not an exact retry;
- generic `dependency_frontier_refs` cannot substitute for the catalog basis.

### RD-06 — `CatalogDependencyDurabilityTests`

Prove:

- publication freezes the accepted catalog basis with the command/execution closure;
- an unsettled accepted execution protects required owner-local definition evidence;
- deletion/replacement that would strand the accepted basis is rejected/retained;
- unpublished session-only dependency prevents a durable-success claim;
- no campaign-global refcount/catalog snapshot/all-history scan is introduced.

### RD-07 — `CatalogBasisRecoveryTests`

Prove:

- recovery reconstructs exact accepted ruleset + owner-local definition dependencies;
- same fingerprint with changed/missing dependency ref cannot resume;
- current/latest fallback is forbidden;
- incompatible/missing retained source blocks rather than rebinds;
- recovered command/resolution/continuation keep the original basis and fixed accepted execution identity/RNG.

### RD-15 gap report — `CatalogGapContextEvidenceTests`

Prove unsupported evidence records the exact basis in which deterministic validation failed and cannot be reinterpreted using a newer/current catalog context.

## Checkpoint choreography

This repair does not create a new RD.

Owner-local work remains:

```text
RD-15
  catalog-context basis schemas + binder output + gap-report basis
  -> LOCAL_CATALOG_BASIS_READY

RD-05
  command/resolution/continuation accepted-basis propagation
  consumes RD-15 LOCAL_CATALOG_BASIS_READY for catalog-backed acceptance
  -> LOCAL_ACCEPTED_CATALOG_EXECUTION_READY

RD-06
  durability/protection join
  consumes accepted-basis carrier semantics
  -> LOCAL_CATALOG_BASIS_DURABILITY_READY

RD-07
  exact reconstruction/recovery join
  consumes RD-15 basis contract + RD-05 accepted execution + RD-06 retained source evidence
  -> LOCAL_CATALOG_BASIS_RECOVERY_READY
```

Hard semantic edge for catalog-backed execution remains:

```text
RD-10 typed interpretation
  -> RD-15 deterministic catalog binding
  -> RD-05 catalog-backed RuntimeCommand acceptance
```

Durability and recovery joins do not prevent RD-05 owner-local deterministic mechanics core from being implemented earlier where no catalog-backed acceptance claim is made.

Every checkpoint obeys the package-wide checkpoint-coherence law: all committed tests in the affected RD modules, focused tests, maintenance audit and full DEV discovery are GREEN before publication.

## Version and clean-slate rule

This is v1.0 clean-slate realization. Legacy pre-v1 fingerprint-only execution shapes are not preservation constraints.

The execution worker must run the Version Impact Gate for the affected local schema families. Do not add compatibility fields or migrations solely to preserve unreleased v0.8/pre-v1 runtime records.

## Proof / bidirectional closure requirements

Register this repair as post-WP27 **Finding 23** rather than inventing a historical readiness ID.

Coverage must prove both directions:

```text
F23
  -> RD-15 basis producer
  -> RD-05 durable accepted-execution carriers
  -> RD-06 retention/publication join
  -> RD-07 exact reconstruction
  -> exact named tests above

and

all new/modified basis schemas, APIs and tests
  -> F23
  -> Step-3 accepted-context identity + Catalog Resolution + Ruleset Package Identity + Step-5.13 retention laws
```

The current proof ledger must add one exact post-WP27 proof row with the named witness classes above. The witness matrix must name the primary proof channel; generic prose/static-search proof alone is insufficient.

## Closure condition

Finding 23 is repaired at planning level only when all of the following are present in the package:

1. one typed reconstructive `CatalogContextBasis` contract;
2. exact RD-15 producer and session-only durability guard;
3. RuntimeCommand/Resolution/Continuation/gap-report carrier obligations;
4. RD-06 retention/publication join;
5. RD-07 exact reconstruction/no-ambient-fallback join;
6. exact TDD witness classes;
7. coverage/proof/witness/execution-router updates;
8. package/currentness routing includes this overlay at highest precedence.

Until those package updates are routed and self-reviewed, author adversarial closure remains open and independent Senior plan review is not authorized.