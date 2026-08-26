# Portable Activity and Execution Values

Status: **CANONICAL S6D-05 OWNER**

## 1. Scope and authority

This document owns reusable embedded value contracts for Activity parameters/bindings, TargetSpec, AreaSpec, CostSpec, DurationSpec, RollRequest/Result, ChoiceRequest, ReactionOffer, Signal and StateDelta, plus their equality across ActionRequest, Resolution, Continuation, ExecutionSegment and receipt.

All are embedded nonowners. None is a world/runtime record or independent mutable authority.

## 2. Core laws

1. One semantic value has one canonical schema root; embedding sites use exact references or prove identical canonical branches.
2. Definitions declare constraints; invocation values bind them. Bindings cannot widen type, cardinality, source class or authority.
3. Engine-owned state is never accepted as adjudicated parameter input.
4. Target/Area values declare bounded selection geometry, never world searches or copied target state.
5. CostSpec declares cost and commit point; Step 3/S6D-06 owns reservation, mutation, refund and atomicity.
6. DurationSpec is definition intent; TemporalBinding is concrete scheduled identity.
7. RollRequest is transient. RollResult is fixed causal evidence generated once by accepted RNG authority and reused on retry.
8. Choice and Reaction are distinct generation-bound offers; responder/option/candidate eligibility is validated by the owning Resolution.
9. Signal is transient pre-commit timing/calculation context with no lifecycle/disposition.
10. StateDelta is parent-relative prospective instruction/evidence with no lifecycle/disposition and no trusted continuation retention.
11. Committed change belongs to MechanicalEvent; commit state belongs to ExecutionSegment; outcome belongs to receipt.
12. No generic payload/query/expression/path/mutation/event-bus language is admitted.

## 3. Signal necessity result

When an exact consumer contract activates a Signal variant, that variant contains a registered `kind_id` plus only the parent evaluation context and exact bindings required by that kind. S6D-05 activates no such consumer: the canonical root therefore rejects every instance and is `DORMANT_NONSELECTABLE`. No generic Signal envelope is admitted. An eventual exact variant has no `pending/accepted/ignored/rejected` field.

- pending reaction work is Continuation/PendingChild state;
- invalidity is validation/Resolution failure;
- absence of an applicable handler is absence of child work, optionally trace evidence;
- durable fact is a MechanicalEvent.

Signal is not checkpointed or garbage-collected independently.

## 4. StateDelta necessity result

When S6D-06 activates an exact mutation variant, StateDelta is a typed candidate owned by one prospective Resolution/segment plan. S6D-05 activates none: the canonical root rejects every instance and is `DORMANT_NONSELECTABLE`. No generic delta envelope is admitted. An eventual exact variant has no `proposed/applied/rejected/ignored/superseded` field.

- existence in the prospective plan means proposed;
- validation failure discards it;
- successful commit is proven by ExecutionSegment + MechanicalEvent;
- recomputation replaces the entire prospective plan;
- Continuation must not retain trusted prospective deltas.

Exact transition payloads and allowed mutations are owned by S6D-06 primitive contracts. Until such a contract exists, a delta variant is dormant/nonselectable.

## 5. Activity declarations and bindings

Every declaration is addressed by its stable parameter-map key and has a closed scalar value type, cardinality, source class, requiredness and bounded default where legal. Invocation bindings use the same key and carry one compatible scalar or collection according to cardinality. Adjudicated bindings additionally carry provenance, eligibility basis, rules-context fingerprint and policy refs and are frozen with accepted work.

Unknown, undeclared, wrong-type/cardinality/source or engine-state substitution fails before execution.

## 6. Target and area

TargetSpec owns target kind, min/max cardinality, range and optional AreaSpec. It distinguishes explicit selection from a runtime-derived affected set. It contains no target IDs.

AreaSpec owns registered shape, spatial unit and shape-specific dimensions. The S6D-05 portable contract admits `unit.foot`; expansion requires catalog admission rather than an arbitrary patterned ID. Origin/direction roles are bound by the Activity/operation contract. Geometry evaluation and line-of-effect queries are runtime infrastructure.

Empty selection is legal only when minimum is zero. Target collections are unordered unless an owning primitive explicitly requires order.

## 7. Cost and duration

CostSpec owns resource definition reference, payer role, nonnegative amount and registered commitment point. Zero is an explicit free cost; absence means no declared cost.

DurationSpec owns instant/metric/boundary/permanent intent. TemporalBinding owns a concrete deadline/boundary identity. DurationSpec never contains scheduler/current-state identity.

## 8. Rolls

RollRequest owns parent-relative roll ID, closed purpose, declarative dice expression and bound roller/subject/target roles. The expression is data, not script.

RollResult must link to its request, retain expression/raw values and authoritative source/provenance. Derived total/outcome never replaces raw evidence. Same request/generation cannot produce a second authoritative result on retry.

## 9. Choice and reaction

Both carry parent Resolution, continuation generation, stable offer identity and responder. Choice exposes option IDs; Reaction exposes candidate Activity IDs. They are not interchangeable.

Pending/accepted/declined/expired state belongs to the owning Continuation/Resolution response processing, not an embedded offer lifecycle. A consumed response is idempotency evidence keyed by generation+offer, not mutation of the offer object.

## 10. Embedding and recovery

ActionRequest carries definition identity, bound entities and parameter bindings. Accepted Resolution/Continuation freezes accepted bindings, facts, rolls and pending offer identity required for deterministic resume. It does not preserve Signal or trusted StateDelta.

ExecutionSegment contains committed Event/pending-child/receipt evidence. Receipt reports segment/Event/outcome identity without copying current state.

All references resolve through the accepted ResolvedCatalogContext.

## 11. Dispositions and downstream routing

The 19 relevant protocol values remain `EMBEDDED_NONOWNER`. Missing schema realization is S6D-05 machine debt, not permission to create records.

- Signal kind vocabulary is existing `signal_kinds`; no disposition registry is added.
- StateDelta variant/payload activation waits for S6D-06 exact primitive/transition contracts.
- Seed target/cost/duration/offer activation waits for S6D-07–09.
- valued Condition semantics remain S6D-08.

## 12. Verification

Tests must prove canonical-root/reference equality, declaration-binding compatibility, Target/Area/Cost/Duration illegal combinations, roll linkage/retry reuse, Choice/Reaction distinction/currentness, no Signal/Delta lifecycle fields, no prospective delta in Continuation, and no embedded value in record-kind registries.
