# Steps 1–2 Retrospective Assurance — Slice E Adversarial Review

Status: **CRITICAL REVIEW COMPLETE — BOUNDED AMENDMENTS MECHANICALLY DETERMINABLE**

Target branch: `feature/mechanical-runtime-hot-state`

Reviewed:

- Slice-E solution-blind Task Charter;
- Slice-E coverage/research synthesis;
- catalog class-admission, resolution/evolution, reference, and version-placement contracts;
- Step-2 Resource/Effect/Condition/Temporal/evaluation ownership;
- assurance slices 0A–D;
- runtime-record inventory and identifier policies;
- saved Step-3 research only to test later-owner compatibility.

## 1. Verdict

The integrated Steps 1–2 architecture survives the assurance pass. No local subsystem needs reopening.

Two cross-system requirements must become explicit before assurance closes:

1. procedure-local ResourceState requires one independently addressable runtime ProcedureScope owner because every existing alternative violates an already-accepted lifetime/classification rule;
2. live Effect provenance must retain compact immutable mechanical-order evidence when current arbitration can depend on recency, so bounded event/trace compaction cannot erase a live mechanical input.

The catalog-context, scheduled-trigger migration, checkpoint, promotion, LLM-fact, chronology, and derived-rebuild boundaries otherwise compose coherently.

The critic concludes that **neither amendment requires a new human product decision**. They are direct consequences of already-approved invariants. The exact Step-3 execution schema still remains a human decision at its existing Decision Gate.

## 2. C1 — attack on admitting `runtime.procedure`

### Strongest alternative: use `world.encounter`

This avoids a new runtime class and gives combat budgets an obvious owner.

### Rejection

Step 2 deliberately selected lifetime owner `procedure`, not `encounter`. More importantly, the accepted requirements say procedure-local state:

- spans several Activity/Resolution invocations;
- is shared with reaction children;
- survives suspension/resume;
- may exist in future parallel procedures;
- is operational/HOT/checkpoint state rather than necessarily campaign-world canon.

Making `world.encounter` universal would either:

1. narrow the already-approved generic procedure semantics to combat encounters; or
2. create fake world Encounters for non-encounter operational procedures.

Both are semantic regressions.

A real `world.encounter` may still be referenced by the runtime ProcedureScope and may supply world-facing encounter state such as participant roster/round/initiative when those facts are canonical/material. That does not make it the generic owner of runtime execution budgets.

## 3. C2 — attack on using `runtime.resolution`

A Resolution already has identity, suspension state, and execution lifetime. Could it own the budgets?

No. This is directly contradicted by Step 2. One Action/Reaction/Movement recovery epoch can be observed and consumed by several Resolutions. A reaction child cannot own a separate copy of the same Reaction budget merely because it is another Activity invocation.

Using Resolution would create exactly the duplicate authority Slice A forbids.

## 4. C3 — attack on an anonymous session map

A session map such as:

```text
runtime.session.procedures[procedure_id].participants[actor].resources
```

could physically hold the state without a new table/class.

The critic rejects this **as an architecture classification**, not necessarily as a future physical storage optimization.

`CATALOG_CONTRACTS.md` says an independently addressable operational owner needed across execution, retry, suspension, recovery, or audit is a `runtime.*` record. ProcedureScope meets every listed criterion and can have several parallel identities.

Therefore its **logical class** is a runtime record even if a physical SQLite implementation later stores small procedure rows/documents inside one table or aggregate.

The class-admission decision is already made. Applying it here is mechanical formalization, not a new product choice.

## 5. C4 — minimum `runtime.procedure` responsibility

The critic recommends admitting one runtime class with deliberately narrow semantics:

```text
runtime.procedure
    identity/lifetime of one active rules-bearing operational procedure
    participant-scoped procedure ResourceState
    procedure-local boundary/order state proven by Step 3
    status/lifetime epoch
    optional world referents (encounter/scene/etc.)
```

It does **not** own:

- one Activity invocation (`runtime.resolution` owns that);
- player-message orchestration (`runtime.intent_plan`);
- canonical encounter fiction (`world.encounter`);
- suspension payload (`runtime.continuation`);
- Temporal Agenda;
- arbitrary workflow nodes;
- reusable procedure rules (`definition.activity`, Resource definitions, and registered procedures/policies remain reusable semantics).

The exact fields remain Step 3. Slice E should admit the logical runtime-record class and identifier policy only, because those are needed to make the already-accepted lifetime owner representable.

## 6. C5 — should every procedure become durable campaign canon?

No.

`runtime.procedure` is an operational record. Its durability follows continuity needs:

- ordinary completed procedure state may be disposable after its relevant recovery/history boundary;
- an active/suspended procedure may be checkpoint-critical;
- a world Encounter may separately be canonical when the campaign needs that world record.

Checkpoint publication serializes/restores the operational owner at a frontier; it does not turn every procedure into a permanent world entity.

## 7. C6 — Effect recency: event reference alone is insufficient under compaction

Could a live Effect simply store `created_by_event_id` and always look up the event when arbitration needs recency?

That works only if the event/order evidence is retained for the entire lifetime of every potentially compared Effect. The architecture explicitly permits bounded trace/history compaction and does not use event replay as current-state authority.

The critic therefore requires **compact live mechanical-order evidence**.

Exact representation is Step 3, but semantics are:

```text
application_order_key
    immutable for one Effect lifecycle episode
    created at the committed Effect-creation/replacement segment
    comparable when policy requires mechanical recency
    retry-stable
    independent of wall clock / SQL row order
    retained while the Effect is nonterminal
```

A creation-event reference may coexist for causal audit, but event-body retention is not the mechanical dependency.

## 8. C7 — could Effect ID itself be the recency key?

Not safely.

Current IDs are allocator identities, not a normative commit-order contract. Local IDs may be rekeyed on promotion, concurrent allocation can be retried/rekeyed, and identifier text is explicitly not chronology.

Using lexical/numeric Effect ID order would silently couple allocation to gameplay semantics and contradict existing chronology/arbitration rules.

Rejected.

## 9. C8 — could session-wide `state_revision` be the recency key?

It is closer, but the current runtime proposal treats `state_revision` as a coarse cache invalidation counter, not a durable world provenance contract. One committed segment can create several Effects, requiring an intra-segment order/ordinal if recency distinguishes them. Cross-environment durability/migration also needs a stable representation independent of one physical SQLite instance.

Step 3 may derive the final key from committed ExecutionSegment identity/order plus intra-segment ordinal or another equivalent mechanical ordering token. Slice E should not prematurely freeze the encoding.

## 10. C9 — active catalog migration versus per-instance version pinning

The critic re-runs the strongest counterargument to the coherent-context model:

> letting an old long-lived Effect finish under its old definition could reduce migration complexity.

Rejected because HDM stores plain `definition_id`, explicitly forbids mixed per-record content versions, and requires one ResolvedCatalogContext for loaders/binders/MechanicalContext/Resolution. Per-instance old-definition pinning would require loading multiple semantic definitions for the same ID simultaneously or adding per-instance version fields, both of which overturn accepted Step-1 architecture.

Therefore incompatible adoption migrates affected active state/continuations or blocks. This is already decided.

## 11. C10 — in-flight Continuation across catalog adoption

The critic confirms a necessary later-stage barrier:

```text
Continuation pins ResolvedCatalogContext identity/frontier
```

An incompatible runtime/catalog adoption cannot simply resume it under a new context.

Migration may eventually support Continuation transformation, but absence of such tooling means adoption must wait/abort safely. This is a maintenance/migration constraint, not permission to keep mixed contexts live.

## 12. C11 — checkpoint duplicate-authority attack

A checkpoint may contain serialized procedure/effect/execution state. Does that duplicate the live owner?

Not if the checkpoint contract is immutable frontier semantics:

```text
live runtime owner
    = current mutable authority

checkpoint at frontier F
    = immutable recovery representation of owner state at F
```

While the live environment advances beyond F, the checkpoint is history/recovery material, not a writable branch merged field-by-field into live state. On restoration, a selected compatible checkpoint becomes reconstruction input and authority is re-instantiated in the new live runtime.

This must be explicit in Step 5; it does not require removing state from checkpoints.

## 13. C12 — promotion closure attack

Could promoting every source/provenance dependency cause unnecessary canon expansion?

The generic rule should remain **mechanical-reference sensitive**:

- if a durable live record contains a required forward reference whose target must remain resolvable for mechanics/integrity, the dependency must be durable/promoted or publication fails;
- narrative provenance that is not a live typed reference need not promote an incidental entity merely for historical flavor;
- immutable receipt/event provenance may retain runtime identifiers under its own durability contract without turning those objects into current world references.

No campaign-global provenance closure is justified.

## 14. C13 — derived reconstruction attack

Could a checkpoint simply preserve DAG/Agenda/winner caches to avoid recompute cost?

It may cache them, but correctness cannot depend on them. On restore:

- ResolvedCatalogContext is reconstructed/validated;
- live owners are restored;
- support/Condition/arbitration/Resource indexes are rebuilt;
- DAG is rebuilt from registered metadata + concrete bindings;
- Agenda is rebuilt from authoritative TemporalBindings.

If a cache is present it must be validated against the same frontier/context or discarded.

## 15. C14 — old runtime proposal drift

The older `MECHANICAL_RUNTIME_PROPOSAL.md` contains pre-Step-2 assumptions (generic stacks and engine-owned pseudo-facts). It is clearly marked as a proposal and later normative documents supersede those areas.

The critic recommends a concise supersession warning rather than rewriting the full historical proposal during assurance. Implementation planning must not use its stale local examples where current normative contracts exist.

## 16. Human decision analysis

### Does `runtime.procedure` require a human class-boundary decision?

Normally adding a new record class is architectural. In this case, however, the controlling architecture decision already exists:

```text
independently addressable operational owner
needed across execution/retry/suspension/recovery/audit
and not world canon
    -> runtime.* record
```

Step 2 additionally already decided that procedure ResourceState has exactly those lifetime properties and is not Resolution-owned.

The viable alternatives either contradict Step 2 or violate the class-admission rule. There is no material product tradeoff left to choose; only the class name/shape and later execution details remain.

**Disposition: mechanically forced amendment; no separate human gate.**

### Does the Effect order token require a human decision?

No. Mechanical recency is already accepted, wall/ID/SQL ordering is already rejected, and bounded trace compaction is already accepted. Some compact live order evidence is therefore mandatory. Exact encoding is Step-3 engineering/design formalization.

**Disposition: mechanically forced Step-3 constraint.**

## 17. Recommended bounded changes before assurance closure

1. admit `runtime.procedure` in the runtime class inventory/machine catalog and identifier policy;
2. document its narrow ownership and its non-overlap with Encounter/Resolution/Continuation;
3. add a focused machine contract test proving the class exists and Resolution/Continuation remain distinct;
4. carry `application_order_key`-equivalent live Effect provenance as a mandatory Step-3 design constraint without guessing the field encoding now;
5. record Continuation/ResolvedCatalogContext migration barrier;
6. record checkpoint immutable-frontier semantics and promotion-closure traversal constraints;
7. add a supersession note to the old runtime proposal;
8. run full repository validation.

## 18. Final critic recommendation

**AMEND / KEEP STEPS 1–2 CLOSED.**

No unresolved Slice-E architecture blocker remains after the bounded changes above.

Human decision required for Slice E: **NO**.

Confidence: **HIGH**.

The next genuine human gate remains the already-saved Step-3 execution ownership Decision Brief.
