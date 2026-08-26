# Registered Activity Primitive Contracts

Status: **CANONICAL S6D-06 OWNER**

## 1. Scope and authority

This document owns the exact compile-time and execution contract of every registered `op.*` Activity primitive. The machine companion is `DEV/CATALOG/activity-primitive-contracts.json`; its schema and primitive-local value shapes are in `DEV/SCHEMAS/activity-primitive-contracts.schema.json` and `DEV/SCHEMAS/activity-primitive-values.schema.json`.

The registry contains exactly 31 closed quarantine dispositions. Current seed and admission evidence establish no executable consumer, so S6D-06 grants no primitive execution authority. The detailed rows are non-authoritative activation drafts until a later seed domain proves the exact consumer, owner-local semantics, failure closure, dependency admission and recovery contract.

## 2. Core laws

1. An Activity step selects one registered primitive and is validated against that primitive's exact arguments, results, reads, RNG, mutation, atomicity, suspension, failure, bound and evidence contract. Unknown primitive IDs, fields, arguments, results and dependencies fail compilation.
2. Arguments are a closed typed map, never an extension bag, payload, query, script, path, patch or executable expression.
3. `op.branch` and `op.for_each_target` are bounded compiler forms. They do not create a query engine, loop runtime or mutation authority.
4. Only `op.roll` consumes RNG. A request/generation has one authoritative fixed result, reused across retry and recovery.
5. Ordinary steps are sequential. A mutation primitive participates in the enclosing planned ExecutionSegment and creates a primitive-local typed prospective output; it does not force a separately committed segment. Failure commits none of the enclosing atomic segment.
6. MechanicalEvent owns the committed fact and receipt owns outcome/evidence. Primitive-local candidates have no independent lifecycle, identity or disposition.
7. No generic Signal or StateDelta variant is activated. Continuation retains accepted causal inputs, fixed rolls, exports, revisions and pending work, never a trusted prospective delta.
8. Choice and reaction primitives suspend the same Resolution using generation-bound portable values. Resume validates generation, offer and responder, and is idempotent.
9. Scheduled follow-up publication is atomic with its causing committed Event. Time advancement emits bounded boundary occurrences through the chronology owner.
10. Reads are closed per primitive and routed to exact calculation selectors, mechanical accessors, named domain owners or bounded geometry infrastructure. A contract cannot dynamically discover another read.

## 3. Contract interpretation

`execution_kind` distinguishes calculation, mutation, compiler form, suspension, follow-up and temporal work. `arguments` and `results` name exact value contracts and cardinalities. `reads` is an allowlist, not an entitlement to access arbitrary state. `prospective_outputs` names only primitive-local typed candidates. `atomicity`, `suspension`, `failures`, `bounds` and `evidence` are mandatory even when their value is `NONE`.

The compiler resolves value shapes through the catalog's closed `value_contracts`. JSON primitives use JSON types; portable S6D-05 values use their canonical schema roots; primitive-local closed variants use `activity-primitive-values.schema.json`; catalog references and compiler symbols are separately identified.

## 4. Execution ownership

A calculation produces typed results and no mutation candidate. A mutation validates all declared reads and arguments, builds its typed candidate, then asks the owning ExecutionSegment to commit atomically. Validation or conflict failure discards the candidate and produces no MechanicalEvent. Successful commit produces the declared MechanicalEvent evidence and receipt linkage.

This does not give `StateDelta` a lifecycle. Candidate presence means proposed; segment disposition proves commit; MechanicalEvent proves durable fact; receipt proves outcome. Re-evaluation replaces the prospective plan rather than superseding a delta object.

## 5. Suspension and recovery

`op.request_choice` and `op.open_reaction_window` create exactly one bounded pending child described by the accepted S6D-05 value contract. Continuation records the current step, accepted bindings/facts, fixed rolls, prior exports, catalog and state revisions, generation and pending response identity. It does not checkpoint Signal or prospective mutation values.

`op.schedule_followup` accepts a registered Activity reference, exact bindings and TemporalBinding. The pending child and the causing committed Event are one atomic publication boundary. Recovery reuses their stable identities and never silently duplicates either.

## 6. Activation and admission

S6D-06 closes the registered vocabulary by explicit quarantine; it activates no seed mechanics and certifies no executable contract as complete. `QUARANTINED` means the registered name has no execution authority and must be rejected. Later activation requires an exact S6D-07–09 seed consumer, owner-local subject/storage/failure semantics, active dependency closure, recovery fixtures and catalog admission evidence. The admission ledger's dormant disposition therefore remains authoritative.

## 7. Verification

Focused tests prove registry equality, closed row shape, exact value routing, read allowlists, RNG exclusivity, suspension forms, compiler bounds, core transition/event/failure membership, execution ownership and rejection of dormant/unknown/ill-shaped steps. Whole-project review must additionally check Activity, Resolution, execution, persistence, chronology, catalog-admission and portable-value owners.

