# Steps 1–2 Retrospective Assurance — Slice E Coverage and Research

Status: **INTEGRATION COVERAGE COMPLETE — ADVERSARIAL REVIEW REQUIRED**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-1-2-assurance-slice-e-integration-task-charter.md`.

## 1. Evidence inspected

Integration evidence included:

- `ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `ARCHITECTURE/CATALOG_RESOLUTION.md`;
- `ARCHITECTURE/CATALOG_INVENTORY.md`;
- `ARCHITECTURE/ENTITY_STRUCTURES.md`;
- `ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` as earlier non-normative runtime prior art;
- `ARCHITECTURE/RULE_ELEMENT_MODEL.md` and `ACTIVITY_MODEL.md`;
- Step-2 Resource/Effect/Condition/Duration/selector designs and final review;
- assurance resolutions 0A, 0B, A, B, C, and D;
- current machine catalogs/schemas;
- `GAME/CORE/CHRONOLOGY.md` and `PERSISTENCE.md` for later-stage compatibility constraints;
- saved Step-3 Task Brief/Research Draft after the solution-blind integration charter was frozen.

The saved Step-3 draft is used only to determine whether later execution work has an appropriate owner for a requirement already exposed by Steps 1–2. It is not treated as accepted architecture.

## 2. Integrated authority matrix

| Semantic concern | Reusable/static authority | Live mutable authority | Derived/projection | Execution/receipt role | Continuity/migration requirement |
|---|---|---|---|---|---|
| Definition meaning | ResolvedCatalogContext + one resolved definition | none | compiled definition/cache | command/Resolution pins context identity | incompatible adoption migrates/rejects coherent state; no mixed per-instance versions |
| Actor HP | actor schema/definition mechanics | `world.actor.state.hp` | max/bloodied calculations | segment plans/mutates | checkpoint/canon restores Actor state |
| LifeState | policy + registered life states | `world.actor.life_state_id` + state-local progress | resolver projections | prospective transition + event | restore current state/progress, not replay guesses |
| Persistent Resource | `definition.resource` | Actor/Asset ResourceState | capacity/available/recovery index | spend/recover segment | state migrated with owner; definitions coherent |
| Procedure Resource | `definition.resource` | **procedure-scope participant ResourceState** | capacity/available | several Resolutions may mutate same owner | owner must survive suspension/restart; Continuation/checkpoint cannot be parallel mutable copies |
| Effect/Condition application | Effect/Condition definition | `world.effect` application | arbitration, Condition aggregation, support reverse index | create/update/terminal + event | active instance must remain interpretable under catalog migration |
| Effect recency/provenance | arbitration/rules-origin policy | live Effect immutable causal provenance/order evidence | family/winner index | creation event/segment supplies evidence | recency cannot depend on disposable trace/event history |
| Intrinsic Effect duration | reusable DurationSpec | `world.effect.temporal_binding` | Temporal Agenda | due occurrence/terminal segment | owner binding restored; Agenda rebuilt |
| Scheduled Effect trigger | definition local trigger declaration | `world.effect.scheduled_trigger_state[key]` | Temporal Agenda | Step-3 due child Resolution/re-arm | incompatible key changes require explicit migration |
| Persistent Resource delayed recovery | Resource definition recovery policy | ResourceState recovery binding | Temporal Agenda | deterministic owner response | binding restored; Agenda rebuilt |
| Stable recovery | lifecycle policy | Stable LifeState recovery binding | Temporal Agenda | LifeState transition | binding restored; Agenda rebuilt |
| Invocation fact | registered fact capability | accepted command/Resolution input only | invocation-sensitive context/cache | fixed causal execution input | Continuation may preserve; never becomes world truth automatically |
| MechanicalContext | static selector/accessor/dependency contracts | none | pinned evaluation object/DAG/cache | one segment/phase view | rebuild after invalidation/restart |
| MechanicalEvent | event schema/capability | immutable committed receipt fact | semantic projections/compaction | causal/idempotency evidence | current world state never depends on unbounded retained trace by accident |
| Checkpoint | checkpoint format/frontier | immutable recovery snapshot/descriptor at one frontier | optional caches | serialization of runtime owner state | cannot be concurrently writable alternate authority |

The major unresolved integration seam is the concrete independent owner for procedure-local ResourceState. The remaining rows have compatible ownership once the constraints below are made explicit.

## 3. E1 — catalog-context evolution is already semantically decided

### Coverage: SATISFIED / integration clarification needed

`CATALOG_RESOLUTION.md` and `CATALOG_CONTRACTS.md` already establish:

```text
one ResolvedCatalogContext per typed runtime operation
plain definition_id interpreted within that context
no duplicate same-ID shadowing
no mixed per-record schema/content versions
incompatible semantic updates require explicit campaign/package migration
```

Therefore the architecture **does not support** this behavior:

```text
new catalog adopted
    but old live Effect A continues using old definition semantics
    while new Effect B with same definition_id uses new semantics
```

That would create two meanings for one plain ID inside one runtime and contradict the coherent-snapshot contract.

The required integration rule is instead:

```text
compatible additive adoption
    -> live state remains valid under the new context

incompatible adoption
    -> migration transforms every affected live/durable/checkpointed state owner
       OR adoption fails/blocks
```

This includes active scheduled-trigger keys, parameter schemas, Resource recovery policies, Effect arbitration policies, and any state whose validity depends on the definition contract.

### In-flight execution

A RuntimeCommand/Resolution/Continuation also must pin the ResolvedCatalogContext identity used to validate its Activity/definitions.

An incompatible catalog/runtime adoption cannot silently resume an existing Continuation against new semantics. Maintenance must either:

- finish/close the old execution safely before adoption;
- migrate the in-flight execution/checkpoint under an explicit migration contract; or
- block/abort the incompatible adoption with a typed maintenance result.

The exact maintenance transaction is later-stage work; the no-silent-reinterpretation invariant is required now.

## 4. E2 — active scheduled-trigger definition evolution

### Coverage: SATISFIED after Slice C + catalog integration

A live application stores:

```text
scheduled_trigger_state[key] -> concrete TemporalBinding
```

while the definition owns:

```text
scheduled_triggers[key] -> reusable declaration
```

Because the key is local to one definition, a new catalog context that removes/renames/changes the declaration incompatibly cannot merely leave the old state entry.

The package/campaign migration must explicitly choose a valid transformation such as:

```text
preserve under compatible declaration
re-anchor/reset under new compatible semantics
rename/migrate key explicitly
unarm/cancel when migration semantics say so
terminate/replace owner if required
```

or reject adoption.

There is no per-instance hidden old declaration and no generic scheduler fallback.

## 5. E3 — Effect mechanical recency must be live provenance, not history retention

### Coverage: PARTIAL / Step-3 constraint required

Effect arbitration may use `potency_then_recency`. Step 2 correctly states that recency is committed causal/mechanical order rather than wall time and leaves the exact representation to Step 3.

However, current trace/history policy allows bounded trace compaction. Therefore a live Effect cannot require an arbitrarily old ResolutionTrace or full MechanicalEvent body merely to know whether it is newer than another still-live Effect.

Required integration invariant:

> Every nonterminal Effect whose current mechanics may depend on application recency must retain immutable compact causal-order evidence as part of its live provenance until that application terminates.

This evidence may be represented by a committed application-order token or another Step-3 causal reference/order key derived at Effect creation/replace commit. Exact field shape belongs to Step 3.

It must satisfy:

- comparable according to mechanical commit order where the arbitration policy requires recency;
- stable across retry;
- independent of SQL/list/wall-clock order;
- retained even if the creating trace/Event payload is compacted;
- not overwritten by refresh of the same lifecycle episode;
- newly allocated for replacement/new application.

A live Effect may additionally reference its creating MechanicalEvent for audit, but arbitration correctness cannot require the event body to remain forever.

## 6. E4 — procedure-local ResourceState exposes a missing concrete owner container

### Coverage: SEMANTIC OWNER FIXED / CONCRETE CLASS NOT YET ADMITTED

Step 2 already fixes:

```text
procedure identity + participant + Resource definition -> spent
```

and explicitly says:

- procedure state is not Actor canon;
- it is not owned by an individual Resolution;
- it must survive separate Activities and reaction children;
- it must survive suspension/resumption and process loss when checkpointed;
- future parallel procedures must be distinguishable by specific procedure identity.

This means the logical owner is an independently addressable **ProcedureScope**.

The current class inventory has:

- `world.encounter`, which represents a particular campaign encounter and may be one procedure domain;
- `runtime.resolution`, which is explicitly the wrong lifetime owner;
- no generic `runtime.procedure`/procedure-scope record.

### Why `world.encounter` alone is insufficient

It would force every procedure-local Resource lifetime into a world encounter even though the accepted Resource contract intentionally says `procedure`, not `encounter`, and future rules-bearing procedures may span several Activities without being an encounter-world entity.

It also couples an operational budget owner to canonical world-record admission even when the procedure is purely HOT/checkpoint state.

### Why Resolution/Continuation are insufficient

They fail the already accepted requirement that one action/reaction/movement budget be shared across several Activity invocations and child reactions. Continuation is only one suspended Resolution episode and cannot become the shared owner.

### Why session-level untyped map is insufficient

A map keyed by procedure ID under `runtime.session` could store the bytes, but the class-admission rule says an independently addressable operational owner needed across execution, retry, suspension, recovery, and audit belongs to a `runtime.*` record rather than remaining an anonymous embedded value.

### Preliminary implication

The accepted class-admission rule appears to force admission of a generic runtime ProcedureScope record in Step 3, conceptually:

```text
runtime.procedure
    procedure_id
    procedure kind/context
    status/lifetime epoch
    participant-local ResourceState
    current procedure ordering/boundary state as required
    optional world encounter/scene referent
```

It would not duplicate `world.encounter`: an Encounter may be the world-facing referent/context, while `runtime.procedure` owns operational execution budgets/lifetime state.

The exact class/name/schema is deliberately not canonicalized in Slice E because the currently active Step-3 Decision Gate owns execution/runtime-record boundaries. The adversarial pass must determine whether this is mechanically forced enough to become a Step-3 constraint or a genuine human class-boundary decision.

## 7. E5 — Continuation/checkpoint are serialization boundaries, not second procedure owners

### Coverage: REQUIRED INTEGRATION CONSTRAINT

Regardless of the concrete ProcedureScope record shape:

```text
ProcedureScope ResourceState
    = one mutable live authority

Resolution / Continuation
    = references procedure identity + expected frontier/revisions

checkpoint
    = immutable recovery serialization/descriptor for that owner at one frontier
```

A Continuation may carry a compact snapshot/hash/revision necessary to detect conflict, but it may not carry an independently mutable `spent` copy that is later merged heuristically.

A checkpoint may serialize local runtime-owner state because that is precisely how it survives environment loss. While the live environment exists, that checkpoint is an immutable historical recovery frontier, not another writable owner. Restoration transfers authority into the newly reconstructed runtime owner at that frontier.

This distinction also applies to local noncanonical Effects/resources: checkpoint serialization does not create a second concurrently mutable Effect/Resource authority.

## 8. E6 — expected reaction children share procedure authority but not parent prospective state

### Coverage: COMPOSES WITH SAVED STEP-3 DRAFT

Scenario:

```text
parent spends/observes procedure budget
reaction child executes and spends reaction budget
parent resumes
```

Required behavior:

1. both child and parent resolve the same ProcedureScope by identity;
2. the child commits its ResourceState mutation in its own ExecutionSegment;
3. parent Continuation does not contain an authoritative stale copy;
4. after child commit, parent advances/re-pins the relevant frontier and recomputes from its safe phase;
5. already committed spends are not repeated;
6. checkpointing preserves ProcedureScope state plus parent/child execution identities.

This matches the saved Step-3 recompute-after-expected-child model and does not require shared SQLite transactions across dialogue turns.

## 9. E7 — promotion/reference closure remains coherent

### Coverage: SATISFIED / mechanically required traversal clarification

Existing universal rules already prohibit durable canon from depending on an unpublished ephemeral entity and require support-parent promotion closure.

The integrated closure must include every **mechanically required forward reference** of a durable live state owner, including as applicable:

- `definition_id` and required session-local reusable definitions;
- support parent chain;
- concrete `source_id` when live mechanics/removal/provenance depend on it;
- reusable `rules_origin_id`/definition dependency where it is separately referenced;
- other referenced world records required by typed state.

A session-local definition promoted to campaign scope preserves its semantic ID when legal; a local world record uses allocator/rekey promotion.

Invocation-adjudicated facts are not promotion dependencies merely because they influenced one committed execution. They remain receipt/Continuation causal input unless Step 4 separately promotes a proposition to durable lore.

Likewise, derived indexes, Temporal Agenda entries, and DAG nodes never enter promotion closure as authorities.

## 10. E8 — quantitative chronology evidence versus active temporal obligations

### Coverage: SATISFIED WITH DISTINCT OWNERS

Slice C separates:

```text
owner-local active binding
    -> concrete future obligation/lifetime

chronology evidence
    -> what quantitative elapsed passage has actually been established
```

These are not duplicate clocks.

An Effect deadline answers when that Effect is due. Retained chronology evidence answers what can later be proven about elapsed time even if no current obligation was armed.

Temporal Agenda derives only from current obligations; it does not need every chronology fact.

Step 5 may compact chronology evidence as long as future materially possible queries retain enough exact/bounded information to return TRUE/FALSE/INDETERMINATE correctly. It may not compact away evidence required by a still-live active binding.

## 11. E9 — LLM invocation facts compose without becoming lore

### Coverage: SATISFIED after Slice D

Scenario:

```text
attack execution accepts fiction.target_visible=true
attack commits
later target visibility differs
```

The old fact is retained only as fixed causal input/receipt evidence where needed for audit/resume. It is not a current-state visibility authority.

State-sensitive Step-2 selectors cannot consume `INVOCATION_ADJUDICATED`, so ephemeral adjudication cannot secretly define Resource capacity, current Condition applicability, HP maximum, recovery, or current Effect duration.

If Step 4 later establishes a durable lore/world proposition corresponding to an earlier adjudication, that is a new explicit truth-promotion operation. It does not retroactively change what input the old Resolution used.

## 12. E10 — derived-state reconstruction closes if source identities are preserved

### Coverage: SATISFIED WITH CARRY-FORWARDS

After SQLite/cache loss runtime can reconstruct:

- Condition presence/value from nonterminal Effects + applicability + aggregation definitions;
- Effect arbitration from target/family + live application parameters/provenance/order evidence;
- support reverse indexes from forward `support_effect_id`;
- Resource capacity/availability from owner ResourceState + definitions + engine-state mechanics;
- scoped DAG from loaded definitions/applications/registered metadata;
- Temporal Agenda from owner-local TemporalBindings;
- scheduled-trigger entries from live Effect state + resolved definition declarations;
- catalog semantics from a compatible ResolvedCatalogContext identity/frontier;
- suspended execution from Continuation/ProcedureScope/checkpoint authority once Step 3 defines the portable container.

No derived cache needs to survive as independent truth.

The two required later-stage source contracts are therefore:

1. live Effect causal-order evidence;
2. concrete independent ProcedureScope owner.

## 13. Multi-system scenario results

### E1 — periodic disease across immunity, catalog update, restart

**PASS WITH CONSTRAINTS.**

- live Effect owns lifecycle/intrinsic/scheduled due state;
- current Condition aggregation applies current immunity;
- catalog adoption uses one coherent context and explicit migration;
- trigger key migration cannot be silent;
- checkpoint restores Effect owner state; Agenda rebuilds;
- due Activity uses ordinary execution/input contracts.

### E2 — action/reaction procedure budgets with suspension

**PARTIAL / ProcedureScope owner required.**

All execution semantics compose if one independent procedure owner exists. Current inventory has not yet admitted the generic runtime record.

### E3 — recency arbitration after history compaction

**PARTIAL / live causal-order evidence required.**

The current architecture has the right provenance concept but Step 3 must make a compact immutable order token/reference part of live application provenance before traces can compact independently.

### E4 — capacity/lifecycle/effect changes in one prospective segment

**PASS.**

Pinned prospective view + one scoped DAG + state-owner normalization prevents intermediate mutation order from defining mechanics. Exact segment ordering is Step 3.

### E5 — durable dependent Effect with local dependencies

**PASS.**

Publication closure promotes/rejects mechanically required support/source/definition dependencies; indexes are not closure members.

### E6 — invocation fact affects one attack only

**PASS.**

Fact remains execution input/receipt evidence; state-sensitive selectors exclude it; no automatic lore promotion.

### E7 — catalog removes active scheduled-trigger declaration

**PASS WITH MIGRATION GATE.**

Coherent catalog migration must transform/cancel/rekey active state explicitly or reject adoption.

## 14. Drift discovered in older runtime proposal

`MECHANICAL_RUNTIME_PROPOSAL.md` still contains pre-Step-2 examples such as generic Effect stacks and engine-owned pseudo-facts (`source.equipped`) that later normative documents explicitly supersede.

Because that file is marked `PROPOSAL / Phase C` and points to later normative Activity/Rule Element contracts, this is documentation debt rather than live architecture authority.

It should receive a clear supersession/drift note or focused cleanup before implementation planning so engineers do not accidentally re-import retired concepts. It is not a reason to reopen Step 2.

## 15. Preliminary findings

```text
E-F1  mixed per-instance catalog semantics        RESOLVED by existing coherent-context contract
E-F2  active scheduled-trigger definition change  RESOLVED by explicit migration requirement
E-F3  Effect recency vs history compaction         STEP-3 REQUIRED CONSTRAINT
E-F4  generic procedure-local owner container      POTENTIAL ARCHITECTURE CLASS GAP
E-F5  Continuation/checkpoint duplicate state      RESOLVED by one-owner + immutable serialization rule
E-F6  reaction child procedure sharing             RESOLVED if ProcedureScope exists
E-F7  promotion closure breadth                    MECHANICAL CLARIFICATION
E-F8  chronology vs temporal obligation            RESOLVED / distinct owners
E-F9  invocation fact vs lore                      RESOLVED
E-F10 derived reconstruction                       RESOLVED with E-F3/E-F4 sources
E-F11 old runtime proposal drift                    DOCUMENTATION DEBT
```

## 16. Alternatives for the ProcedureScope gap

### A. Make `world.encounter` the universal procedure owner

Simple for combat, but semantically narrows the accepted generic `procedure` lifetime, forces operational state into a world class, and does not naturally cover future non-encounter rules procedures spanning multiple Activities.

**Not recommended.**

### B. Make `runtime.resolution` own procedure Resources

Reuses an existing runtime class but directly contradicts Step 2: reaction/movement/action budgets must survive and be shared across separate Resolutions.

**Rejected.**

### C. Store an anonymous procedure map under `runtime.session`

Physically possible, but the owner is independently addressed by procedure ID, referenced across Resolutions, required for suspension/recovery, and may have parallel instances. Under the accepted class-admission rule that is a runtime record, not an anonymous embedded bag.

**Rejected by current class-admission rule.**

### D. Admit one generic runtime ProcedureScope owner

Conceptually:

```text
runtime.procedure
    independently addressable operational procedure lifetime
    participant procedure-local ResourceState
    procedure/boundary/order state justified by Step 3
    optional referent to world.encounter/scene when applicable
```

It remains distinct from `world.encounter`, `runtime.resolution`, and `runtime.continuation`.

**Recommended if the adversarial review confirms no simpler existing owner satisfies the accepted invariants.**

## 17. Preliminary recommendation

**AMEND / KEEP Steps 1–2 closed.**

Most integration seams are already constrained correctly. Add two explicit Step-3 requirements:

1. nonterminal Effect provenance retains compact immutable mechanical-order evidence sufficient for recency independent of trace/event-body retention;
2. procedure-local Resources have one independently addressable ProcedureScope owner, never Resolution/Continuation/checkpoint copies.

The adversarial review must decide whether item 2 is a mechanically forced application of the already-approved class-admission rule or a new class-boundary choice requiring the human architect.
