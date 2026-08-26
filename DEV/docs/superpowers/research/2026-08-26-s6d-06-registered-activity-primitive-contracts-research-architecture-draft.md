# S6D-06 Step 2 — Research & Architecture Draft

## Source Manifest

Current branch/ref, both design-process owners, PROJECT_MAP, NEAR_TERM_ROADMAP, S6D owner decision/task brief/plan, ACTIVITY_MODEL, PORTABLE_ACTIVITY_VALUES, CALCULATION_SELECTOR_METADATA, MECHANICAL_CONTEXT_ACCESSORS, execution/Resolution/persistence/chronology owners, catalog admission owner/ledger, core catalog, Activity schema and focused tests were inspected. Repository-wide searches covered every `op.*`, Signal, StateDelta, ExecutionSegment, MechanicalEvent, Continuation, transition, event and failure identifier.

## Evidence synthesis

- Core catalog registers 31 primitives; the admission ledger currently has 31 dormant and zero admitted primitives, routed to S6D-06.
- ACTIVITY_MODEL already settles finite composition, closed arguments, bounded branch/iteration, sequential execution, optional atomic mutation segments, suspension in the same Resolution and fixed causal evidence on recovery.
- S6D-05 settles that Signal is transient and StateDelta prospective, both without lifecycle/disposition; segment/Event/receipt own commit/fact/outcome.
- Current seed contains no exact compiled consumer, so contract closure and selection activation must remain separate.
- Existing selector/accessor catalogs are dormant; naming an exact dependency cannot activate it.

## Draft architecture

Create one exact row per registered primitive, a closed value-contract table, schema validation and compiler conformance tests. Keep all rows nonselectable until S6D-07–09 supplies a consumer and active dependencies. Mutation rows produce only primitive-local candidates; structural rows compile to bounded plans; suspension rows preserve accepted causal inputs, not prospective deltas.

## Alternatives rejected

- Generic `args`/payload contract: unverifiable and reintroduces a rules DSL.
- Family-level contracts only: loses item-level reads, failures and mutation boundaries.
- Activate all rows when contracts exist: confuses coverage with admission.
- Add Signal/StateDelta dispositions: duplicates the accepted execution lifecycle.

No human product-semantic choice remains: the result is entailed by accepted owners and S6D sequencing.


