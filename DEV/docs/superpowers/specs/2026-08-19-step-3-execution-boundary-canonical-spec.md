# Step 3 Canonical Specification — Deterministic Execution Boundary

Status: **CANONICAL ARCHITECTURE — IMPLEMENTATION PLANNING REQUIRED**

Target branch: `feature/mechanical-runtime-hot-state`

Owner decision: **Alternative C approved**.

Canonicalization basis:

- `2026-08-19-step-3-execution-boundary-task-brief.md`
- `2026-08-19-step-3-execution-boundary-research-draft.md`
- `2026-08-19-step-3-execution-boundary-decision-brief.md`
- `2026-08-19-step-3-execution-boundary-candidate-spec.md`
- `2026-08-19-step-3-execution-boundary-adversarial-review.md`
- `2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

This file is the consolidated normative Step-3 architecture after the owner-approved decision and adversarial-review resolution. Conflicting provisional wording in the earlier Step-3 draft/candidate is superseded by this specification.

This specification does not itself implement runtime schemas/code. After canonicalization, implementation planning MUST use the required Superpowers planning/TDD workflow.

## 1. Architecture invariant

HDM SHALL preserve distinct semantic/lifetime owners above one shared deterministic local commit kernel:

```text
Interaction
    -> IntentPlan
        -> executable IntentClause
            -> RuntimeCommand
                -> ActionRequest
                    -> Resolution(Activity)
                OR
                -> TransitionRequest
                    -> direct deterministic execution

RuntimeCommand = root execution-chain closure owner

Resolution / direct Transition execution
    -> ExecutionSegment(s)
        -> authoritative state/runtime commit
        -> MechanicalEvents
        -> receipts/idempotency evidence
        -> mandatory child invocation descriptors where required

runtime.procedure
    -> procedure-local operational state

Continuation
    -> one suspended Resolution generation
```

Current world records remain current-state authority. Events/receipts/history provide committed fact, causality, audit and reconstruction evidence; they do not replace state as a second current-state authority.

## 2. Authority/lifetime model

| Concept | Representation | Normative responsibility |
|---|---|---|
| Interaction | `runtime.interaction` | one accepted external exchange/invocation identity and raw message linkage |
| IntentPlan | `runtime.intent_plan` | finite ordered material clauses from one Interaction; not a transaction |
| IntentClause | embedded typed value | one interpreted material clause and optional bounded forward guard |
| RuntimeCommand | `runtime.command` | accepted idempotent root execution request and mandatory descendant closure owner |
| ActionRequest | protocol value | typed request for one Activity invocation |
| TransitionRequest | protocol value | typed already-adjudicated deterministic transition |
| Procedure | `runtime.procedure` | independently addressable procedure-local operational state owner |
| Resolution | `runtime.resolution` | exactly one Activity invocation |
| ExecutionSegment | embedded stable execution edge | smallest local atomic execution/persistence boundary |
| Signal | protocol value | transient pre-commit timing/calculation context |
| BoundaryOccurrence | protocol value | transient reached-boundary context |
| Continuation | `runtime.continuation` | portable suspended-Resolution generation authority |
| MechanicalEvent | `runtime.mechanical_event` | immutable committed mechanical fact |
| ResolutionTrace | `runtime.resolution_trace` | bounded diagnostic/calculation evidence |
| Receipt | protocol value | immutable observable/idempotent execution outcome |

## 3. Interaction and IntentPlan

### 3.1 Interaction

`runtime.interaction` SHALL own/reference:

- stable host invocation identity;
- raw input message reference;
- authenticated player/session/campaign context;
- resulting IntentPlan;
- response linkage when retained.

It SHALL NOT own world mutation, Procedure ResourceState, RNG progression, or a transaction.

Same prose in a later intentional turn is a new Interaction. Transport retry of the same invocation reuses Interaction identity.

### 3.2 IntentPlan

IntentPlan SHALL contain every material interpreted clause in finite order.

Default execution:

```text
clause N validates and executes against state committed by clauses < N
```

Earlier committed clauses are not compensated/rolled back because a later clause fails, becomes invalid, suspends, or needs clarification.

Narrative-only/clarification/unsupported material clauses remain represented by typed clause disposition even when they produce no RuntimeCommand.

### 3.3 Initial forward-guard contract

A clause MAY initially have at most one guard referring to one earlier clause.

The guard may inspect only:

- earlier clause execution status; or
- one registered typed scalar/boolean/enum receipt export.

Allowed initial comparison is equality or membership against literal registered values.

No loops, backward edges, arbitrary expressions, world queries, dynamic clause creation or user-authored scripts are permitted.

Revisit trigger: if focused compound-intent tests demonstrate frequent ordinary language that requires multiple prior-result conditions without a meaning-preserving clause split, reopen only this bounded guard vocabulary.

## 4. RuntimeCommand — root request and closure owner

### 4.1 Root command responsibility

One executable player IntentClause SHALL produce at most one accepted root RuntimeCommand.

RuntimeCommand SHALL own/reference:

```text
command_id
interaction_id
intent_plan_id
clause_id
command_kind = action | transition
normalized typed payload
accepted ResolvedCatalogContext identity
accepted invocation fact set + stable provenance
input_fingerprint
root execution-chain disposition
root action Resolution or direct-transition segment linkage
mandatory child/pending invocation linkage
final/suspended/blocked receipt references
```

It SHALL NOT copy Resolution cursor/procedure state as a second authority.

### 4.2 Root chain identity

`root_command_id` is the root execution-chain identity for all mechanically mandatory descendant work caused by that command.

Root action Resolution and mandatory child Resolutions SHALL retain/reference this root command.

No `runtime.resolution_chain` class is introduced.

### 4.3 Command disposition

RuntimeCommand owns only root invocation/closure disposition, not detailed Resolution state.

Initial conceptual states:

```text
ACCEPTED
SETTLED
```

`ACCEPTED` includes running, suspended, follow-up-required or typed-blocked root chains whose detailed execution state belongs to linked Resolution/Continuation/pending child state.

RuntimeCommand becomes `SETTLED` only when:

- the root direct transition or root Activity result is committed/terminal as applicable; and
- every mechanically mandatory descendant/pending obligation required for the command's completion is closed, durably suspended, or resolved through an authorized typed terminal/blocking policy.

An IntentClause SHALL NOT be marked mechanically executed merely because its first segment committed while mandatory descendants remain unresolved.

Optional/nonmechanical presentation work does not hold command closure open.

## 5. RuntimeCommand idempotency

### 5.1 Accepted input fingerprint

`input_fingerprint` SHALL use canonical serialization of mechanically relevant accepted command input including:

- command kind;
- typed request payload;
- resolved entity/definition/Activity identities;
- accepted ResolvedCatalogContext identity;
- accepted invocation fact IDs and explicit values;
- stable provenance class/reference where provenance changes mechanical identity/adjudication.

Exclude narration/explanation text, wall-clock time, SQL/list order and presentation-only data.

### 5.2 Retry lookup order

Idempotency processing SHALL look up existing command/resume identity BEFORE rebinding under the current ambient catalog/state.

```text
identity exists
    -> compare retry against stored accepted input/context/fingerprint
    -> exact retry returns stored result/current suspension
    -> different input => IDEMPOTENCY_CONFLICT

identity absent
    -> bind as new request under current accepted context
```

A hydration retry with the same accepted input does not change command fingerprint because more records were loaded.

This prevents a compatible ambient catalog refresh from turning an exact old-command retry into a false conflict.

## 6. LLM -> deterministic binder

### 6.1 LLM scope

The LLM MAY interpret:

- mention spans;
- intent/outcome/approach;
- semantic choice among bounded host-supplied candidates;
- explicitly registered fiction-dependent boolean facts.

It SHALL NOT establish:

- existence of an unchecked executable/entity ID;
- deterministic target eligibility when engine-checkable;
- HP/LifeState/Condition/Resource/Effect or other engine-owned state;
- executable primitives absent from the loaded catalog.

### 6.2 Bounded discovery/hydration

Discovery returns candidates, not authority.

The deterministic binder SHALL revalidate selected IDs, kinds, visibility/permission, Activity contracts and state constraints against the same accepted ResolvedCatalogContext and appropriate pinned state before RuntimeCommand acceptance.

### 6.3 Invocation-adjudicated facts

Accepted invocation facts conceptually contain:

```text
fact_id
value: true | false
provenance_class
stable provenance reference(s) where applicable
```

Missing is distinct from false.

Only registered facts admitted by the consuming selector/operation are valid. Engine-owned state through this channel is a typed validation failure.

An invocation fact remains causal execution input. It does not automatically become lore/current world truth/player knowledge because an execution commits.

## 7. Procedure owner

### 7.1 Runtime Procedure

`runtime.procedure` is the independently addressable owner for operational rules-procedure state that must survive multiple Resolutions, reactions, suspensions, retries and recovery.

It owns procedure-local ResourceState keyed semantically by:

```text
procedure_id
participant_id
resource_definition_id
    -> accepted spent-model ResourceState
```

No Resolution, Continuation, Encounter or checkpoint may become an alternate writable owner of this state.

### 7.2 Procedure versus world Encounter

`world.encounter` MAY provide a world-facing combat/procedure context but is not the generic procedure owner and is not required for every Procedure.

Procedure may reference a relevant Encounter/Scene/world context while retaining independent operational identity.

### 7.3 Participation

Resolution may omit `procedure_id` when no procedure-local semantics apply.

Parent and child/reaction Resolutions share the Procedure when they participate in the same rules procedure.

Procedure reset/termination occurs through explicit registered procedure/boundary semantics; no global `current_encounter` singleton is permitted.

## 8. Resolution

Resolution continues to mean exactly one Activity invocation with concrete bindings.

It owns/references as applicable:

```text
resolution_id
root_command_id
optional direct initiating clause/command relation
activity identity under accepted ResolvedCatalogContext
actor/source/target bindings
optional procedure_id
accepted invocation facts + provenance/fingerprint
status
execution cursor / safe recompute phase
fixed raw RNG values already generated
typed prior-step exports
parent/child Resolution refs
next segment sequence
current Continuation
trace reference
causal invocation/firing key
```

Internal Trigger/Reaction/Scheduled child Resolution does not need a separate player RuntimeCommand. It inherits/references the root command and uses a stable causal invocation key derived from the occurrence/offer/binding that created it.

## 9. ExecutionSegment

### 9.1 No new runtime class

The initial architecture SHALL NOT add `runtime.execution_segment`.

Segment identity is addressable through its independent execution owner plus segment sequence. Segment has no lifecycle/permissions/state independent of that owner.

Introduce a standalone class only if future requirements need independent segment lifecycle/reference semantics.

### 9.2 Identity

Conceptually:

```text
action-backed segment_id     = resolution_id + segment_sequence
direct-transition segment_id = command_id + segment_sequence
```

The exact wire encoding is implementation detail.

### 9.3 Atomicity

One segment transaction MAY atomically advance as applicable:

- authoritative world state;
- Procedure state;
- RuntimeCommand/Resolution execution state;
- RNG frontier + newly fixed raw random values;
- Continuation create/consume state;
- MechanicalEvent batch;
- selected mandatory post-commit firing descriptors/child identities;
- trace/segment receipt;
- idempotency markers;
- dirty/publication bookkeeping.

No SQLite transaction spans an external choice/reaction/host dialogue boundary.

### 9.4 Prospective flow

```text
pinned committed view
    -> prospective overlay
    -> calculations / Signals / state-owner plans
    -> scoped dependency DAG extension/validation
    -> authority/constraint validation
    -> event/follow-up identity planning
    -> atomic segment commit
```

Invalid candidate segment commits no candidate authoritative mutation and emits no committed MechanicalEvent for that failed candidate.

### 9.5 Continuity-only segment

A segment may commit fixed RNG/Continuation/cursor/idempotency state while committing no world mutation.

Such a segment is still a real idempotent execution edge.

## 10. MechanicalEvent and receipts

### 10.1 Event identity

MechanicalEvent identity SHALL be:

```text
segment_id + stable event_ordinal
```

Retry of a committed segment returns the same Event identities. Payload equality is not identity.

### 10.2 Event authority

MechanicalEvent records a compact mechanically relevant committed fact/change plus causal provenance.

Current world records remain current-state authority.

Trace/Event body retention may be compacted only after live mechanics retain any compact causal/order evidence they still require.

### 10.3 Segment receipt

Every committed segment returns/stores an immutable receipt sufficient to identify:

- segment/execution owner;
- commit disposition;
- resulting execution state;
- Event IDs;
- typed exports needed later;
- affected state/revision references as required for validation;
- child/pending obligation refs.

Receipt is evidence/result, not copied state authority.

## 11. Mandatory post-commit trigger durability

### 11.1 No Event -> lost-child crash window

If a committed Event requires mandatory post-commit child work, the triggering segment SHALL atomically materialize enough obligation identity in the same transaction as the Event.

For each selected mandatory firing, persist/reference as applicable:

```text
MechanicalEvent identity
registered binding identity/local key
stable firing key
root_command_id
procedure_id when applicable
intended Activity identity
child Resolution ID if allocatable now
OR pending child invocation descriptor
```

Child execution may occur later; obligation identity may not be lost after the Event commits.

### 11.2 Timing view

Registered Signal/Event timing semantics determine which binding/source state participates.

Later mutable current-state SQL discovery SHALL NOT decide retroactively whether a historical firing existed.

### 11.3 Root closure

RuntimeCommand remains non-SETTLED while mandatory child/pending firing work remains unresolved under the command's execution chain.

## 12. Trigger/reaction firing identity and ordering

### 12.1 Firing key

Each firing uses a stable key derived from:

```text
binding identity/local key
+ triggering occurrence/Event identity
+ relevant owner/application identity
```

Same binding cannot refire on the same occurrence because of retry.

### 12.2 Ordering precedence

Mechanical ordering SHALL use:

1. explicit registered timing phase/priority semantics;
2. rules-defined controller/player order via typed ChoiceRequest;
3. proven order-independent batch semantics, where stable trace order is observational only;
4. otherwise typed `ORDER_ADJUDICATION_REQUIRED`/equivalent.

SQL/list/ID sorting may not select a mechanically different outcome merely because it is deterministic.

### 12.3 Chain safety bounds

Execution chains SHALL have configured safety bounds such as maximum depth/total generated child executions or firings.

Hitting a bound SHALL NOT silently discard mandatory work.

The root execution SHALL retain an embedded pending child invocation descriptor containing at least:

```text
firing key
trigger occurrence/Event
binding identity
intended Activity
root command/procedure linkage
reason = execution limit
```

The root command remains non-SETTLED and returns a typed blocked/maintenance/adjudication-required outcome.

Already committed ancestor facts remain committed.

No generic job/obligation runtime class is introduced at this stage.

## 13. External choices and reactions

### 13.1 Solicited response routing

When a ChoiceRequest/ReactionWindow is pending, the host SHALL interpret the relevant external player response first as a response to that pending continuation generation/offer, not as an unrelated fresh normal IntentPlan.

Stable resume identity is tied to:

```text
continuation generation
+ choice/reaction offer identity
+ responder identity
+ selected bounded option/Activity
```

A reaction Activity may create a child Resolution under the same root command and Procedure when applicable.

Unrelated extra intent in the same message may be planned only after the pending response is resolved; it SHALL NOT be silently folded into the reaction child.

### 13.2 Continuation payload

Continuation is portable authority for one suspended Resolution generation and preserves fixed historical inputs/safe recompute boundary.

As applicable it stores:

```text
continuation_id + generation
root command / resolution identity
ResolvedCatalogContext identity
procedure_id
activity identity
execution cursor + next safe recompute phase
actor/source/target bindings
accepted invocation facts + stable provenance/fingerprint
fixed raw RNG values
choices already made
typed prior-step exports
committed segment/Event receipt refs
dependency/revision frontier
pending ChoiceRequest/ReactionWindow
expected child Resolution IDs
future RNG frontier/state
idempotency/single-consume state
unconsumed requested advancement remainder when suspended at a due boundary
```

It SHALL NOT own Procedure ResourceState copies, cached MechanicalContext, Temporal Agenda, Condition/arbitration indexes, DAG cache, or trusted prospective StateDeltas.

### 13.3 Single consume

Continuation generation is single-consume.

Exact resume retry returns stored result/current next suspension. Stale superseded generation fails typed validation without re-execution.

## 14. Reaction recomputation

### 14.1 External choice

Unexpected relevant dependency change before resume triggers typed revalidation/conflict rather than stale prospective reuse.

### 14.2 Expected reaction child

Expected reaction child may intentionally change relevant state.

Parent SHALL:

```text
consume expected child receipt
re-pin resulting committed frontier
re-read Procedure state
rebuild MechanicalContext
recompute from declared safe phase
preserve fixed historical RNG/choices
continue
```

Parent SHALL NOT fail merely because the expected child changed a relevant revision and SHALL NOT restore a pre-child world/Procedure snapshot.

Unexpected additional relevant changes may still trigger typed conflict/revalidation.

## 15. RNG continuity

Raw random values become fixed execution history once committed with the owning execution continuity edge.

Retry/resume SHALL NOT reroll fixed values.

Reaction may change modifier/outcome interpretation while keeping original raw roll where the rules require the same roll basis.

Future RNG frontier/state required for deterministic continuation is checkpointable and changes atomically with the segment that consumes/generates values.

Exact PRNG algorithm is implementation detail/planning work.

## 16. Effect application recency evidence

### 16.1 Scope

Recency arbitration compares simultaneously nonterminal candidate applications within:

```text
target + derived application family
```

It does not require a campaign-global chronology token.

### 16.2 Immutable episode ordinal

Each new Effect lifecycle episode that may participate in recency arbitration SHALL receive immutable `application_order_key` equivalent to:

```text
1 + max(existing application_order_key)
```

over the complete currently nonterminal candidate set for the same `(target, application family)` in the pinned/prospective view.

If no candidate exists, the ordinal may restart from the initial value because no terminal episode remains mechanically comparable.

Requirements:

- candidate-set completeness is a hydration/query precondition;
- suppressed but nonterminal candidates remain in the comparison set;
- refresh preserves the episode ordinal;
- replace computes a new ordinal while the replaced application still participates in the prospective candidate set, then atomically terminates old + creates new;
- terminal applications need not remain comparable after leaving the nonterminal set;
- mechanically order-sensitive multiple same-segment creations for the same target/family require registered ordering/adjudication rather than arbitrary list order.

This key is stored with the live Effect episode as compact immutable causal evidence and does not depend on wall time, Effect ID order, SQL order or indefinite trace/Event body retention.

## 17. BoundaryOccurrence and same-coordinate closure

### 17.1 BoundaryOccurrence

BoundaryOccurrence is transient typed reached-boundary context containing at least:

```text
boundary_id
producer identity
scope/subject
causal execution position
stable occurrence key
```

Producer establishes occurrence; each state owner owns its response.

If committed boundary progress creates mandatory later work that cannot finish in the same segment, pending obligation identity is materialized atomically with the committed boundary progress.

### 17.2 Advancement barrier

When metric/procedure/semantic advancement reaches a mechanically due coordinate/boundary:

```text
freeze at reached coordinate
capture complete immediately-due set from the defined pinned timing view
resolve or durably suspend mandatory same-coordinate consequences
only after closure may advancement move beyond the coordinate
```

Any unconsumed requested advancement remains explicit continuation input; it is not silently lost or auto-applied across an unresolved choice/reaction/adjudication.

## 18. Owner-local scheduled trigger execution

Temporal Agenda remains rebuildable due-index state.

Due flow:

```text
Agenda discovers Effect owner + declaration key
    -> stable due occurrence
    -> ordinary bounded child Resolution(Activity)
    -> normal binder/read/reaction/segment rules
    -> atomic owner response
         REARM(new binding)
         OR UNARM
         OR OWNER TERMINAL
```

The due child receives no privileged callback/world-query surface.

### 18.1 Same-owner expiry coincidence

The engine SHALL NOT invent one universal order between scheduled firing and intrinsic Effect expiry for all rulesets.

If same-coordinate coincidence is mechanically order-sensitive, content must use a registered representable ordering relation. The initial contract SHALL reject ambiguous outcome-sensitive coincidence that lacks such semantics.

Step 6 seed review may justify a narrower dedicated tie policy if a real rules case requires it.

## 19. Direct deterministic TransitionRequest

TransitionRequest is valid only after every required mechanical choice/adjudication is resolved and no internal roll/reaction/external choice is required.

It uses the same prospective validation, ExecutionSegment, Event, receipt, idempotency and dirty-state kernel as Activity execution.

If preflight shows a genuine rules procedure is required, runtime returns typed misclassification/unsupported-for-direct-transition outcome rather than synthesizing a fake Activity.

A direct transition itself does not suspend mechanically. Committed Event consequences may create ordinary mandatory child Resolutions under the same root command.

## 20. Catalog-context barrier

RuntimeCommand, Resolution and Continuation bind one accepted compatible ResolvedCatalogContext identity.

Incompatible engine/catalog adoption SHALL NOT silently resume in-flight work under changed mechanics.

Authorized adoption paths are limited to:

- finish compatible in-flight work before adoption;
- explicitly migrate in-flight execution;
- block/reject adoption;
- explicitly abort through an authorized typed maintenance result when policy permits.

No mixed old/new definition semantics in one active execution.

## 21. Checkpoint continuity

Step 3 defines portable in-flight payload semantics; Step 5 owns Git publication/restoration/cleanup policy.

Recovery roots preserve as applicable:

- active Procedure identity/state roots;
- current suspended Resolution/Continuation;
- fixed RNG/choice inputs;
- committed segment/Event frontier;
- mandatory pending reaction/trigger/scheduled invocation descriptors;
- accepted invocation facts/provenance;
- local metric anchors/evidence when mechanically material;
- idempotency state;
- accepted ResolvedCatalogContext identity.

Derived Agenda/DAG/index/cache state is rebuilt, not restored as an alternate authority.

Checkpoint is immutable recovery-frontier representation, not a concurrently mutable second live state owner.

## 22. Mechanical completion versus narration

The execution API SHALL distinguish mechanically settled command closure from suspended/blocked/follow-up-required state.

Final outcome narration for one executable clause SHOULD normally consume a mechanically complete/settled receipt closure.

Interim prompts for choices/reactions are presentation of suspension state, not final outcome narration.

A host may narrate a committed intermediate fact intentionally, but SHALL NOT present unresolved mandatory descendants as if the clause were fully settled.

Narrative text SHALL never be read back as mechanical state authority.

## 23. Semantic/history projection boundary

Step 3 supplies stable identities/causality for later history projection but does not own the full lore/spectator design.

Intended layering:

```text
runtime.message / transcript
    raw player/Master/tool dialogue when retained

runtime.mechanical_event
    detailed committed mechanics facts

runtime.semantic_event
    compact durable campaign-history transitions

world.chapter
    authored human-readable narrative/history projection
```

SemanticEvents/Chapters are not alternate mechanical truth. Their factual claims must anchor to authoritative world/lore/event sources.

Full transcript retention/publication, spoiler-safe filtering, spectator projections, chapter authoring/regeneration and history compaction belong to Steps 4/5.

A public/spectator Git view MUST NOT expose hidden campaign facts merely because the private canonical campaign storage contains them.

## 24. Typed failure/outcome requirements

Implementation SHALL define typed outcomes covering at least:

- `IDEMPOTENCY_CONFLICT`;
- `HYDRATION_REQUIRED`;
- missing/invalid typed reference after bounded retrieval attempt;
- incompatible catalog-context resume/adoption;
- stale/unexpected continuation dependency conflict;
- stale/superseded continuation generation;
- prospective dependency-cycle/authority failure;
- direct-transition misclassification;
- `ORDER_ADJUDICATION_REQUIRED` or equivalent;
- execution/trigger safety limit reached with pending work preserved;
- missing required invocation-adjudicated fact;
- unauthorized LLM-supplied engine fact.

A typed failure cannot silently undo earlier committed segments or create unrecorded partial mutation.

## 25. Normative cases

### A — ordinary attack

```text
Interaction -> IntentPlan -> RuntimeCommand(action)
    -> Resolution
    -> one segment
        roll/calculation/state plans
        commit
        Events/receipt
    -> root command SETTLED
```

### B — pre-commit reaction

```text
parent Resolution
    -> fixed input/roll
    -> Signal opens ReactionWindow
    -> continuity segment commits fixed history + Continuation

solicited responder message
    -> binds pending offer generation first
    -> child Resolution under same root command/Procedure
    -> child commits reaction state/cost

parent
    -> consumes expected child receipt
    -> re-pins/re-reads/recomputes
    -> commits final segment
    -> root command settles after mandatory closure
```

### C — post-damage mandatory follow-up

Damage Event and mandatory firing descriptor/child identity are committed atomically. Crash after Event commit cannot lose the child. Child may add later Events but cannot rewrite damage Event.

### D — compound player message partial completion

Clauses 1–2 commit; clause 3 becomes invalid. Earlier clauses remain committed. IntentPlan does not become all-or-nothing.

### E — deterministic transfer

Exact already-adjudicated transfer uses direct transition segment, no fake Activity.

### F — ambiguous natural-language target

Bounded candidate mapping remains materially ambiguous. No RuntimeCommand executes; clarification is returned instead of invented ID.

### G — retry after commit

Same command/resume identity + fingerprint returns same segment/Event/receipt result; no duplicate damage/spend/Effect/firing.

### H — crash while suspended

Restore compatible catalog context + Procedure roots + Continuation fixed history/frontier, rebuild derived indexes, resume without reroll or trusted stale prospective delta.

### I — multiple boundary responders

Complete due responder set captured at reached boundary. Registered order/commutativity/choice semantics determine execution; SQL order never decides a mechanically different outcome. Advancement remains frozen until closure/suspension.

### J — owner-local scheduled trigger

Stable due occurrence -> child Resolution -> atomic rearm/unarm/terminal owner response. Same occurrence cannot fire twice on retry.

### K — reaction spends procedure resource

Child reaction mutates sole Procedure ResourceState. Parent resume re-reads it and cannot restore Continuation copy because no such authoritative copy exists.

### L — incompatible catalog adoption during suspension

Resume under incompatible context is blocked until authorized finish/migrate/block/abort policy resolves it.

### M — trigger-chain limit after committed ancestor

Ancestor Events remain committed; pending mandatory child descriptor remains under root execution closure; command does not falsely settle and no mandatory firing disappears silently.

### N — Effect recency after trace compaction

Two nonterminal same-family applications keep immutable family-local episode ordinals on the live Effects. Old detailed traces may compact without changing `potency_then_recency` arbitration.

## 26. Deferred owners

### Step 4

- durable lore/knowledge/secrets/disclosure authority;
- knowledge-safe LLM context/candidate exposure;
- promotion of invocation facts into durable truth when justified;
- transcript -> semantic event -> chapter transformation semantics;
- spectator spoiler/visibility policy.

### Step 5

- Git publication/restoration of runtime continuity payloads;
- multiplayer/shared Procedure conflicts;
- cross-scene chronology/reconciliation where one target/state becomes shared;
- private canonical storage versus public/spectator Git projection transport;
- transcript/history retention/compaction policy;
- checkpoint cleanup/expiry.

### Step 6

- full D&D seed validation of trigger/simultaneous-order cases;
- specialized same-time scheduled-trigger tie policy only if proven necessary;
- final catalog/migration/gap closure;
- concrete mode/ruleset safety-limit defaults where needed.

## 27. Implementation-planning requirements

The implementation plan SHALL cover at least:

1. machine contract for RuntimeCommand root closure and root-command linkage;
2. Procedure record/state schema and storage contract;
3. Resolution/Continuation/root-child identity fields;
4. embedded ExecutionSegment/receipt identity and atomic storage transaction;
5. MechanicalEvent segment+ordinal identity;
6. mandatory post-commit child descriptor atomicity;
7. choice/reaction resume identity;
8. invocation fact typed/provenance/fingerprint schema;
9. Effect family-local immutable recency ordinal;
10. same-coordinate advancement barrier/pending remainder;
11. typed failure vocabulary;
12. focused TDD cases A–N;
13. schema/catalog/test/maintenance-audit alignment;
14. final Step-3 adversarial/critical verification before roadmap closure.

## 28. Canonical verdict

Alternative C is canonical for Step 3.

No unresolved Step-3 architecture blocker remains at the ownership/specification level.

Step 3 remains **IN PROGRESS** until implementation planning, machine/schema/catalog alignment, focused tests and final critical verification close its roadmap exit gate.

Human decision required now: **NO**.

Recommendation confidence: **HIGH**.
