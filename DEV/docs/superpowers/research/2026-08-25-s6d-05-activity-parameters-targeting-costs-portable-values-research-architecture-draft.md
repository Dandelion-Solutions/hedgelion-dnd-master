# S6D-05 — Research & Architecture Draft

Status: **STEP 2 COMPLETE — EVIDENCE SYNTHESIZED**

Base: `v1/engine-rearchitecture@a3e1705a8c1afe4969c25b3eb4d4d6f29ac073c2`.

## Result

The exact S6D-05 census contains 19 `protocol_value_kinds`. Every one is currently `EMBEDDED_NONOWNER / DOWNSTREAM_S6D_05`: runtime command, action request, transition request, intent clause, target spec, area spec, duration spec, cost spec, signal, state delta, roll request/result, choice request, reaction offer, resolution receipt, execution segment, pending child invocation, invocation fact and boundary occurrence.

Component vocabularies (8 target kinds, 6 area shapes, 8 range modes, 4 duration modes, 4 units, 20 signals, 7 boundaries, 10 Resolution states and 42 Events) are separate admitted ID sets. Their admission does not prove a complete portable envelope.

## Owner reconciliation

- Target/Area/Cost are Activity-owned embedded definitions with current schema roots.
- Duration’s ledger pointer is historical; current authority is the DurationSpec/TemporalBinding boundary plus Step-3/5 retention.
- Activity declarations and bindings are jointly constrained by Activity, House Rules, S6D-04 input authority and Step-3 accepted-work freezing.
- Rolls are Activity requests but Step-3/RANDOMNESS owns one-time generation and retained authoritative results.
- Choice/Reaction ledger pointers are historical. Current authority must be Resolution/Continuation/pending-child identity. Reaction remains distinct because responder/timing/currentness differs.
- Signal/StateDelta pointers are historical. Current authority is the Step-3 event/segment/receipt chain. Neither creates an event bus, mutation DSL or state store.
- ExecutionSegment, PendingChild, Receipt, InvocationFact and BoundaryOccurrence already have schema roots but require registry/embedding/recovery equality.

## Item-family decisions

1. All 19 remain embedded nonowners; no record kind is created.
2. A value is COMPLETE only with one canonical schema root or explicitly named canonical inline branch plus all embedding equality tests.
3. ReactionOffer exists but needs current owner alignment. Signal/StateDelta roots may be minimal closed shapes, but neither may own lifecycle/disposition; unsupported delta variants remain dormant.
4. Target selection and affected-set derivation remain distinct: TargetSpec declares binding constraints, runtime/primitive logic derives affected entities.
5. AreaSpec is geometry data, never a world query.
6. CostSpec declares payer/resource/amount/commit point; reservation/commit/refund behavior stays Step-3/S6D-06.
7. DurationSpec declares semantic duration; TemporalBinding is concrete scheduled identity.
8. Parameter declarations own type/cardinality/default/source. Bindings cannot widen them or supply engine state.
9. RollRequest is transient; RollResult is fixed causal evidence, not a record.
10. Choice and Reaction have distinct discriminators and generation-bound responder authority.
11. Signal is transient context and StateDelta a prospective parent-relative instruction. Their outcome is derived from validation, ExecutionSegment, MechanicalEvent and receipt; neither has a lifecycle field.
12. Retry/recovery retains only live accepted values and compatible catalog identity.

## Required machine products

- 19-row realization ledger and registry/schema-root equality test;
- canonical `reaction-offer`, `signal`, and `state-delta` schemas where no accepted root exists;
- strengthened declaration/binding, Target/Area, Cost/Duration and Roll schemas;
- Resolution/Continuation/receipt references to canonical roots rather than weaker copies;
- tests for illegal discriminators/combinations, missing/zero/empty, authority, generation/currentness, one-roll reuse, and recovery roundtrip;
- no-record/no-query/no-generic-payload assertions.

## Alternatives

A. Canonical embedded-value family with shared refs — selected.
B. Protocol-local copies — rejected for drift.
C. Universal tagged arbitrary payload — rejected as dynamic language.
D. Promote values to records — rejected by parent boundary.

## Human gate

None. The candidate does not choose seed ranges/costs/durations, primitive atomicity, valued Conditions or new gameplay semantics. Any unsupported branch is dormant with its downstream trigger.
