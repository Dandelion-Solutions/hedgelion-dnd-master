# Registered Activity Primitive Contracts

Status: **CANONICAL S6D-06 OWNER**

## 1. Scope and authority

This document owns the exact compile-time and execution contract of every registered `op.*` Activity primitive. The machine companion is `DEV/CATALOG/activity-primitive-contracts.json`; its schema and primitive-local value shapes are in `DEV/SCHEMAS/activity-primitive-contracts.schema.json` and `DEV/SCHEMAS/activity-primitive-values.schema.json`.

At S6D-06 closure the registry contained exactly 31 quarantine dispositions and granted no execution authority. S6D-07 replaces eleven of those dispositions after exact MVP seed consumers, owner-local semantics, failure closure, dependency admission and recovery boundaries are proven: `op.select_targets`, `op.roll`, `op.resolve_check`, `op.resolve_attack`, `op.resolve_save`, `op.apply_damage`, `op.apply_healing`, `op.consume_resource`, exact `op.create_effect`, exact action-entitlement `op.emit_fact`, and bounded compiler form `op.for_each_target`. Their catalog rows are now `COMPLETE / ACTIVE_ADMITTED`; the remaining 20 rows retain their S6D-06 quarantine.

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

S6D-06 originally closed the registered vocabulary by explicit quarantine. `QUARANTINED` still means the registered name has no execution authority and must be rejected. A later domain may replace that row only with an exact seed consumer, owner-local subject/storage/failure semantics, active dependency closure, recovery fixtures, catalog admission evidence and whole-project review. S6D-07 is the first such replacement and is limited to the eleven `COMPLETE / ACTIVE_ADMITTED` rows named above; registration or a separate overlay cannot activate any other row.

The `op.emit_fact` replacement is not a generic event/fact escape hatch. Its sole accepted variant emits one typed Action Surge entitlement into the current turn's procedure-state owner. The grant is atomic with the named resource decrement, is usable by the next eligible non-`activity.magic` activation exactly once, expires at that turn boundary, and is replay-safe by the enclosing Resolution idempotency key. The committed event is evidence; it does not become persistent Actor state or grant arbitrary turn-boundary authority.

The `op.create_effect` replacement is equally narrow. It accepts only `effect.innate_sorcery` for the bound actor/source pair and its definition-owned one-minute `DurationSpec`. Effect state owns the stable `(target, source, definition)` instance key; reapplication atomically replaces that same instance; the causing commit pins the start and concrete temporal binding; the Temporal Agenda emits an idempotent expiry transition; recovery reconstructs from committed Effect evidence plus that binding. S6D-08 retains all generic Effect/Duration/recovery design authority.

## 7. Verification

Focused tests prove registry equality, closed row shape, exact value routing, read allowlists, RNG exclusivity, suspension forms, compiler bounds, core transition/event/failure membership, execution ownership and rejection of dormant/unknown/ill-shaped steps. Whole-project review must additionally check Activity, Resolution, execution, persistence, chronology, catalog-admission and portable-value owners.

## 8. S6D-09 exact-consumer amendment

S6D-09 adds two identity-bound `definition.activity` consumers in the selected package: `activity.check.generic` and `activity.save.generic`. They add no primitive and change no primitive authority. The exact consumer amendments are limited to:

```text
op.roll          <- activity.check.generic, activity.save.generic
op.resolve_check <- activity.check.generic
op.resolve_save  <- activity.save.generic
```

Both definitions compile through the same closed argument/result contracts already admitted above. Ability/proficiency basis is selected from the finite package declaration; the threshold is one bounded `INVOCATION_ADJUDICATED` integer whose accepted binding/provenance/currentness is frozen by the Activity invocation owner; `op.roll` remains the sole RNG owner; resolution exports only `check_outcome` or `save_outcome`. Neither primitive receives consequence selection, arbitrary transition, mutation, Asset, spatial, query or product-policy authority. Any downstream world consequence is a separately admitted exact owner transition. A successful or failed check/save may therefore be Mechanical-Null.

The amended exact-consumer lists are content-identity-bound through `GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/gameplay-spine-seed.json` and its entry in `character-capabilities.json`. Removing that file, changing its digest, or failing package compilation makes both consumers nonselectable; it does not fall back to a descriptive overlay.
