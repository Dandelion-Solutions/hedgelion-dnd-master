# Step 3 Candidate Specification — Deterministic Execution Boundary

Status: **CANDIDATE SPECIFICATION — OWNER-APPROVED CORE OWNERSHIP / ADVERSARIAL REVIEW REQUIRED**

Target branch: `feature/mechanical-runtime-hot-state`

Authority chain:

- `2026-08-19-step-3-execution-boundary-task-brief.md`
- `2026-08-19-step-3-execution-boundary-research-draft.md`
- `2026-08-19-step-3-execution-boundary-decision-brief.md`
- `2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`

Owner decision: **Alternative C approved**.

This candidate specification formalizes the approved ownership model. It does not reopen Steps 1–2 and does not authorize runtime implementation until adversarial review, resolution, canonicalization, and the implementation-planning gate complete.

## 1. Normative objective

HDM SHALL execute natural-language interactions through distinct upper semantic owners and one shared deterministic lower commit kernel.

The architecture SHALL preserve these separations:

```text
Interaction
    -> IntentPlan
        -> executable IntentClause
            -> RuntimeCommand
                -> ActionRequest -> Resolution(Activity)
                OR
                -> TransitionRequest -> direct deterministic execution

Resolution/Transition execution
    -> ExecutionSegment(s)
        -> committed state/runtime changes
        -> MechanicalEvents
        -> receipts/idempotency evidence

runtime.procedure
    -> owns procedure-local participant ResourceState

Continuation
    -> owns one suspended Resolution episode
    -> references Procedure when applicable
```

Current world state remains authoritative current-state truth. MechanicalEvents are immutable committed execution facts, not an event-sourced replacement for state.

## 2. Authority and lifetime table

| Concept | Class | Authority | Lifetime / identity |
|---|---|---|---|
| Interaction | `runtime.interaction` | host/player exchange identity and raw input linkage | one accepted external interaction |
| IntentPlan | `runtime.intent_plan` | finite ordered material clauses extracted from one Interaction | one Interaction |
| IntentClause | embedded typed value | one material interpreted clause and optional forward guard | owned by IntentPlan |
| RuntimeCommand | `runtime.command` | idempotent accepted executable clause envelope | one executable IntentClause |
| ActionRequest | protocol value | typed request for one Activity invocation | owned by RuntimeCommand |
| TransitionRequest | protocol value | typed already-adjudicated deterministic transition | owned by RuntimeCommand |
| Procedure | `runtime.procedure` | procedure-local operational state, especially participant ResourceState | one rules-bearing procedure lifetime |
| Resolution | `runtime.resolution` | one Activity invocation with execution cursor/fixed inputs | one Activity invocation |
| ExecutionSegment | embedded execution protocol with stable identity | smallest local atomic execution-persistence edge | owned by Resolution or direct transition command |
| Signal | protocol value | transient pre-commit timing/calculation context | one evaluation edge |
| BoundaryOccurrence | protocol value | transient typed reached-boundary context | one boundary occurrence |
| Continuation | `runtime.continuation` | portable suspended-Resolution authority | one suspension generation/episode |
| MechanicalEvent | `runtime.mechanical_event` | immutable committed mechanical fact | permanent while retained by execution/audit policy |
| ResolutionTrace | `runtime.resolution_trace` | diagnostic/audit calculation evidence | bounded retention unless material subset promoted |
| Segment/command receipt | protocol value | immutable idempotent observable outcome | tied to execution identity |

### 2.1 ExecutionSegment is not a new catalog class

The initial contract SHALL NOT add `runtime.execution_segment`.

A segment requires stable identity and auditability but has no independent domain lifecycle beyond its owning execution. It SHALL be represented as an embedded committed execution record/receipt under the owning Resolution or direct transition command, with enough identity for Events and retries to reference it.

If future requirements need independently addressed segment lifecycle outside the owning execution, class admission MUST be reopened explicitly.

## 3. Interaction and IntentPlan

### 3.1 Interaction

`runtime.interaction` SHALL own or reference:

- stable host invocation identity;
- raw player/user message reference;
- authenticated player/session/campaign context;
- resulting IntentPlan;
- final response linkage when retained.

It SHALL NOT own world mutation, procedure-local ResourceState, RNG progression, or a transaction.

A later intentional repetition of identical prose SHALL be a new Interaction. A transport retry of the same host invocation SHALL reuse the same Interaction identity.

### 3.2 IntentPlan

An IntentPlan SHALL be a finite ordered sequence of all material clauses from one Interaction. No material clause may disappear silently.

Clause execution SHALL be sequential by default:

```text
clause N validates/executes against state committed by clauses < N
```

Committed earlier clauses SHALL NOT be rolled back because a later clause fails, suspends, becomes invalid, or requires clarification.

IntentPlan SHALL NOT be a generic workflow language.

### 3.3 Initial conditional-clause surface

A clause MAY have at most one forward guard referring to one earlier clause.

The guard SHALL inspect only:

- an earlier clause execution status; or
- one registered typed scalar/boolean/enum receipt export.

Initial comparison SHALL be equality/membership against literal registered values. No backward edge, loop, dynamic clause creation, arbitrary expression, world query, or user-authored script is permitted.

A more complex reusable conditional procedure belongs in an Activity. A later proven player-language case MAY extend the guard surface through a reviewed catalog/schema change.

## 4. RuntimeCommand and binding

### 4.1 RuntimeCommand responsibility

One executable IntentClause SHALL produce at most one accepted RuntimeCommand identity.

RuntimeCommand SHALL own:

```text
command_id
interaction_id
intent_plan_id
clause_id
command_kind = action | transition
normalized typed payload
ResolvedCatalogContext identity
accepted invocation fact set + stable provenance
input_fingerprint
idempotency disposition
execution/result references
```

RuntimeCommand SHALL NOT duplicate detailed Resolution procedure state.

For an action command it SHALL link the created Resolution. For a deterministic transition command it SHALL own the direct segment/result linkage.

### 4.2 Command idempotency disposition

RuntimeCommand SHALL distinguish only invocation/idempotency state from detailed mechanical procedure state.

Conceptually:

```text
ACCEPTED
SETTLED
```

An action Resolution owns its own detailed running/suspended/terminal state. RuntimeCommand MUST NOT mirror that state as a second authority.

### 4.3 Input fingerprint

`input_fingerprint` SHALL be deterministic over canonical serialization of mechanically relevant accepted command input, including:

- command kind;
- typed request payload;
- resolved entity/definition/Activity identities;
- ResolvedCatalogContext identity;
- accepted invocation fact IDs and explicit values;
- stable fact provenance class/reference required to distinguish materially different adjudications.

It SHALL exclude volatile narration, explanation prose, wall-clock receipt time, SQL row order, and other mechanically irrelevant presentation data.

Same command identity + same fingerprint SHALL return the existing result/current suspension. Same command identity + different fingerprint SHALL fail `IDEMPOTENCY_CONFLICT` without executing a second consequence.

## 5. LLM -> deterministic binder boundary

### 5.1 LLM role

The LLM MAY produce semantic interpretation such as:

- mention spans;
- intended outcome/approach;
- candidate selection among bounded host-supplied references;
- fiction-dependent registered boolean facts when explicitly permitted.

The LLM SHALL NOT establish executable identity existence, mechanical eligibility, HP/LifeState/Condition/Resource/Effect state, or other engine-owned facts.

### 5.2 Bounded discovery

The execution host MAY perform bounded catalog/entity discovery and hydration and present a candidate set to the LLM.

Discovery results are candidates, never authority. The deterministic binder SHALL revalidate selected IDs against the same ResolvedCatalogContext and pinned state/frontier before accepting RuntimeCommand input.

### 5.3 Invocation-adjudicated facts

Accepted invocation facts SHALL have the conceptual shape:

```text
fact_id
value: true | false
provenance_class
stable provenance reference(s) where applicable
```

Absence means missing; missing SHALL NOT be coerced to false.

Only registered facts allowed by the consuming selector/operation MAY be accepted. Engine-owned facts supplied through this channel SHALL fail typed validation.

An invocation fact that influenced execution SHALL remain causal execution input; it SHALL NOT automatically become lore, world truth, or player knowledge.

## 6. Procedure owner

### 6.1 `runtime.procedure`

`runtime.procedure` SHALL be the independently addressable operational owner for rules-procedure state that must survive multiple Resolutions, reactions, suspension, retries, and recovery.

It SHALL own procedure-local ResourceState keyed semantically by:

```text
procedure_id
participant_id
resource_definition_id
    -> spent / storage required by the accepted Resource contract
```

The exact physical record schema is implementation planning after this architecture canonicalizes.

### 6.2 Procedure versus Encounter

`world.encounter` MAY be the world-facing context/referent for a combat-like procedure, but SHALL NOT be required for every procedure and SHALL NOT become the universal owner of runtime procedure state.

A Procedure MAY reference a relevant world context such as an Encounter/Scene when needed; the world record and Procedure retain distinct responsibilities.

### 6.3 Procedure participation

A Resolution MAY have no Procedure when no procedure-local state/timing applies.

Parent and reaction/trigger child Resolutions SHALL share the same Procedure identity when they participate in the same rules procedure. They SHALL NOT copy Procedure ResourceState into Resolution or Continuation.

Procedure termination/reset SHALL occur only through explicit registered procedure/boundary semantics; no global `current_encounter` singleton is permitted.

## 7. Resolution

A Resolution SHALL continue to mean exactly one invocation of one Activity with concrete bindings.

It SHALL own or reference as applicable:

```text
resolution_id
optional initiating command_id
activity identity under pinned ResolvedCatalogContext
actor/source/target bindings
optional procedure_id
accepted invocation facts + provenance/fingerprint
status
execution cursor / safe phase
fixed RNG results already generated
typed prior-step exports
child Resolution links
next segment sequence
current Continuation reference
trace reference
causal invocation key for non-command child Resolution
```

A child Resolution created by a Trigger/Reaction/Scheduled occurrence MAY have no player RuntimeCommand. Its causal invocation key SHALL instead derive from the stable triggering occurrence + binding/offer identity so retry cannot create a duplicate child.

## 8. ExecutionSegment

### 8.1 Identity

Each execution owner SHALL allocate monotonically increasing segment sequence within that owner.

Conceptually:

```text
action-backed segment_id     = resolution_id + segment_sequence
direct-transition segment_id = command_id + segment_sequence
```

The encoded string is implementation detail; the identity relation is normative.

### 8.2 Atomicity

One committed ExecutionSegment SHALL atomically advance the coherent subset required by that edge, including as applicable:

- world authoritative records;
- `runtime.procedure` state;
- RuntimeCommand/Resolution state;
- RNG frontier and newly fixed raw random values;
- Continuation create/consume state;
- MechanicalEvent batch;
- trace/segment receipt;
- idempotency markers;
- dirty/publication bookkeeping.

No SQLite transaction SHALL span an external player/LLM/host choice or reaction boundary.

### 8.3 Prospective execution

A mutating segment SHALL follow:

```text
pinned committed view
    -> prospective overlay
    -> registered calculations / Signals / owner plans
    -> scoped dependency DAG extension/validation
    -> authority/constraint validation
    -> atomic commit
```

An invalid candidate segment SHALL commit none of its candidate authoritative mutations and SHALL emit no committed MechanicalEvent for those candidate mutations.

### 8.4 Suspension-only segment

A segment MAY commit only execution continuity facts, for example fixed RNG + Continuation + Resolution cursor, without mutating world state.

Such a segment is still a legitimate committed execution edge and SHALL be idempotent.

## 9. MechanicalEvent and receipts

### 9.1 Event identity

A committed MechanicalEvent SHALL be uniquely identified by:

```text
segment_id + stable event_ordinal
```

Retry of an already committed segment SHALL return the same Event identities.

Payload equality SHALL NOT define Event identity.

### 9.2 Event authority

MechanicalEvent SHALL record a compact mechanically relevant committed fact/change and causal provenance.

It SHALL NOT become the current-state owner for world records.

MechanicalEvent/trace retention MAY be compacted later only after every live mechanic that requires durable causal/order evidence has its required compact evidence retained with the live owner or durable projection.

### 9.3 Segment receipt

Every committed segment SHALL produce an immutable receipt sufficient to identify:

- segment identity;
- execution owner;
- committed/not-committed disposition;
- resulting execution state;
- Event identities;
- typed exports needed by later execution;
- affected authoritative record references/revisions as needed for validation;
- child/pending obligation references when applicable.

Receipts are evidence/results, not duplicate world state.

## 10. Effect application order evidence

Effect create/replace that participates in recency-sensitive arbitration SHALL receive compact immutable mechanical order evidence at committed creation.

The initial logical contract is:

```text
application_order_key
    derived from committed execution order
    stable for one Effect lifecycle episode
    retry-stable
    mechanically comparable within the relevant chronology/procedure domain
    not wall-clock time
    not Effect ID order
    not SQL/list order
```

Refresh SHALL preserve the existing application order key because it continues the same lifecycle episode. Replace SHALL terminate the old episode and allocate new order evidence.

Exact field encoding and cross-scene comparison rules remain Step 5 implementation/integration work; Step 3 requires only that local committed execution produce sufficient compact order evidence and never depend on indefinite old trace-body retention.

## 11. Signal and BoundaryOccurrence

### 11.1 Signal

Signal SHALL be transient pre-commit timing/calculation context.

It MAY collect passive mechanics, determine candidate contributions, expose a reaction opportunity, or identify pending typed work. It SHALL NOT be durable world truth.

If execution suspends, Continuation SHALL store the normalized pending choice/reaction contract and occurrence/offer identity needed for deterministic resume rather than serializing an arbitrary Signal object as a new authority.

### 11.2 BoundaryOccurrence

BoundaryOccurrence SHALL be a transient typed reached-boundary context containing at least:

```text
boundary_id
producer identity
scope/subject
causal execution position
stable occurrence key
```

Boundary producers establish occurrence; state owners own their automatic responses.

If a committed boundary creates mandatory later work that cannot complete in the same segment, the pending obligation identity SHALL be checkpointed atomically with the committed boundary progress.

## 12. Reactions, choices, and Continuation

### 12.1 Continuation ownership

Continuation SHALL be the portable authority for one suspended Resolution generation.

It SHALL preserve fixed historical inputs and safe recomputation boundaries, not trusted prospective derived state.

Minimum payload, as applicable:

```text
continuation_id + generation
command_id / resolution_id
ResolvedCatalogContext identity
procedure_id
activity identity
execution cursor + next safe recompute phase
actor/source/target bindings
accepted invocation facts + stable provenance/fingerprint
fixed raw RNG results
choices already made
typed prior-step exports
committed segment/event receipt refs
dependency/revision frontier
pending ChoiceRequest or ReactionWindow
expected child Resolution identities
future RNG frontier/state
idempotency / consume state
```

It SHALL NOT own copies of Procedure ResourceState, MechanicalContext cache, Temporal Agenda, Condition index, arbitration winners, dependency DAG cache, or trusted prospective StateDeltas.

### 12.2 Single-consume generations

A continuation generation SHALL be single-consume.

An exact retry of the same resume identity/fingerprint SHALL return the stored result/current next suspension. A stale response to an already superseded generation SHALL fail typed validation and SHALL NOT execute again.

### 12.3 Resume after external choice

A choice response SHALL be validated against the expected dependency frontier.

Unexpected mechanically relevant changes SHALL trigger typed revalidation/conflict rather than reuse stale prospective state.

### 12.4 Resume after expected reaction child

Expected reaction children are allowed to change relevant state.

The parent SHALL:

```text
consume expected child receipt
re-pin to the resulting committed frontier
rebuild MechanicalContext
recompute from the declared safe phase
preserve fixed historical RNG/choice inputs
continue
```

It SHALL NOT reject merely because the expected child changed a relevant revision, and SHALL NOT restore a pre-child Procedure/world snapshot.

Unexpected additional relevant mutations MAY still produce a typed conflict/revalidation result.

## 13. RNG continuity

Raw random values become fixed execution history when generated and committed into the owning execution continuity segment/trace.

Runtime SHALL NOT reroll a previously fixed random value during retry/resume.

A later reaction MAY change modifiers or interpretation while retaining the original raw roll when the rules say the same roll remains the basis.

Future RNG frontier/state needed for deterministic continuation SHALL be checkpointable. Exact PRNG algorithm is implementation planning, but its state transition MUST be atomic with the segment that consumes/generates values.

## 14. Trigger and child-Resolution execution

### 14.1 Candidate collection

Trigger candidates SHALL be collected from one pinned state view and one stable triggering occurrence.

Each firing SHALL have a stable firing key derived from:

```text
trigger binding identity/local key
+ triggering occurrence identity
+ relevant owner/application identity
```

The same binding SHALL NOT fire twice on the same occurrence because of retry.

### 14.2 Ordering

Mechanical ordering SHALL use, in this precedence:

1. explicit registered timing phase/priority semantics;
2. rules-defined controller/player ordering through a typed ChoiceRequest;
3. proven order-independent batch semantics, with any stable trace order used only for observability;
4. otherwise a typed `ORDER_ADJUDICATION_REQUIRED`/equivalent outcome.

Stable ID/list/SQL order SHALL NOT decide a mechanically non-commutative result merely because it is reproducible.

### 14.3 Chain bounds

Parent/child Resolution chains SHALL have configured safety bounds for depth and total generated child executions/trigger firings.

Reaching a bound SHALL NOT silently drop mandatory work. The runtime SHALL preserve the blocked/pending obligation and return a typed execution-limit result requiring an explicit safe continuation/maintenance/adjudication path.

Already committed ancestor facts remain committed.

## 15. Scheduled owner-local trigger due execution

Temporal Agenda remains a rebuildable due index.

When an owner-local Effect scheduled trigger becomes due:

```text
Agenda discovers owner + declaration key
    -> stable due occurrence
    -> ordinary bounded child Activity/Resolution
    -> normal pinned reads/input/reaction rules
    -> atomic owner state response
         REARM(new binding)
         OR UNARM
         OR OWNER TERMINAL
```

The due Activity receives no privileged world-query or callback surface.

### 15.1 Same-coordinate due work

When one advancement reaches a coordinate/boundary with several due obligations, runtime SHALL discover the complete immediately-due set from the pre-mutation view before applying any one member solely because of storage iteration order.

If two due obligations are mechanically order-sensitive, their relation MUST be determined by registered timing/order semantics or typed adjudication. The engine SHALL NOT invent a universal `scheduled trigger before/after intrinsic expiry` rule for all rulesets.

The initial content contract SHALL reject a definition whose same-owner scheduled-trigger/expiry coincidence is outcome-sensitive but lacks a registered representable ordering relation. Step 6 seed review may justify a narrower dedicated tie policy if an actual rules case requires one.

## 16. Deterministic direct transitions

A TransitionRequest is valid only when all mechanical choices needed for the transition are already resolved and no roll/reaction/external choice is required inside the transition itself.

A direct transition SHALL use the same prospective validation, ExecutionSegment, Event, receipt, idempotency, and dirty-state kernel as an Activity-backed action.

If preflight discovers that the requested operation actually requires a rules procedure, it SHALL reject/misclassification-return rather than synthesize a fake Activity silently.

A direct TransitionRequest SHALL not suspend mechanically; post-commit child work MAY still be spawned by committed Events through ordinary trigger semantics.

## 17. Catalog-context barrier

RuntimeCommand, Resolution, and Continuation SHALL bind one compatible ResolvedCatalogContext identity.

An incompatible engine/catalog adoption SHALL NOT resume an in-flight execution under silently changed semantics.

Adoption/maintenance MUST choose an authorized path:

- finish compatible in-flight work before adoption;
- explicitly migrate the in-flight execution contract;
- block/reject adoption; or
- explicitly abort affected work through a typed maintenance result when product policy permits.

Mixed old/new definition meaning inside one active execution is invalid.

## 18. Checkpoint continuity

Step 3 defines portable in-flight payload semantics; Step 5 owns repository publication/restoration policy.

A continuity checkpoint SHALL preserve enough authoritative information to reconstruct active execution without replay guessing, including as applicable:

- active Procedure identity/state roots;
- suspended Resolution/Continuation;
- fixed RNG/choice inputs;
- committed segment/Event frontier;
- pending reaction/trigger/scheduled obligations;
- accepted invocation facts/provenance;
- mechanically material local metric anchors/evidence;
- idempotency information required to distinguish retry from new execution;
- ResolvedCatalogContext identity.

Derived Agenda/DAG/index/cache state SHALL be rebuilt, not restored as authority.

A checkpoint is an immutable recovery-frontier representation, not a second concurrently writable copy of live state.

## 19. Semantic/narrative projection boundary

Step 3 SHALL produce stable execution and causal references sufficient for later history/narrative projection but SHALL NOT make narration a mechanical authority.

The intended later layering is:

```text
runtime.message / transcript
    raw player/Master/tool dialogue for transcript/audit when retained

runtime.mechanical_event
    detailed committed mechanics fact

runtime.semantic_event
    compact durable campaign-history transition

world.chapter
    human-readable authored/history projection
```

`runtime.semantic_event` and `world.chapter` MUST derive/anchor claims from authoritative world/lore/event sources rather than becoming alternate mechanical truth.

Full transcript retention/publication, spectator-facing public projections, secret filtering, chapter generation/editing, and history compaction are Step 4/5 concerns. A viewer-facing Git projection MUST NOT expose hidden campaign facts merely because the underlying private campaign branch stores them.

## 20. Failure taxonomy requirements

Step 3 implementation SHALL have typed outcomes covering at least:

- `IDEMPOTENCY_CONFLICT`;
- invalid/missing typed reference after bounded hydration attempt;
- `HYDRATION_REQUIRED`;
- catalog-context incompatibility;
- stale/unexpected continuation dependency conflict;
- stale/superseded continuation generation;
- dependency cycle/prospective validation failure;
- transition misclassified as deterministic when a procedure is required;
- `ORDER_ADJUDICATION_REQUIRED` or equivalent;
- trigger/execution chain limit reached with preserved pending work;
- missing/invalid required invocation-adjudicated fact;
- unauthorized LLM-supplied engine fact.

Typed failures SHALL not cause silent partial mutation outside already committed prior segments.

## 21. Focused normative cases

### Case A — ordinary attack, no reaction

```text
Interaction -> IntentPlan clause -> RuntimeCommand(action)
    -> Resolution(attack Activity)
    -> one ExecutionSegment
        fixed roll + prospective result + damage/state owners
        commit
        MechanicalEvents
    -> completed receipt
```

No external pause and no Git operation is required by the execution architecture itself.

### Case B — Counterspell/Shield-like pre-commit reaction

```text
parent Resolution
    -> fixed initial roll/cast facts
    -> Signal opens ReactionWindow
    -> suspension segment commits fixed inputs + Continuation

reaction response
    -> child Resolution under same Procedure when applicable
    -> child segment commits reaction result/cost

parent resumes
    -> consume expected child receipt
    -> re-pin/recompute from safe phase
    -> commit resulting parent segment
```

No reroll and no stale prospective delta reuse.

### Case C — post-damage follow-up

Damage Event commits first. A post-commit TriggerBinding creates a stable child Resolution invocation from the Event occurrence. The child may add later Events but cannot rewrite the committed damage Event/segment.

### Case D — multiple intents with partial completion

```text
1 take sword      -> commits
2 enter hall      -> commits
3 attack guard    -> now invalid
```

Clauses 1–2 remain committed. Clause 3 returns typed failure/clarification. IntentPlan is not rolled back.

### Case E — deterministic transfer

An exact already-adjudicated asset/currency/location transition uses RuntimeCommand(transition) -> direct ExecutionSegment, with no fake Activity.

### Case F — ambiguous natural-language target

LLM receives bounded candidates but cannot uniquely select with sufficient confidence/permission. No command executes. Host returns clarification rather than inventing an entity ID.

### Case G — retry after committed segment

Same command/resume identity + same fingerprint returns existing receipt/Event IDs. No duplicate Resource spending, damage, Effect create, or child firing occurs.

### Case H — crash while suspended

Checkpoint restore recreates Procedure + Resolution/Continuation fixed inputs/frontiers under compatible catalog context, rebuilds derived indexes, and resumes without reroll or trusted old prospective delta.

### Case I — boundary with several state-owner responders

BoundaryOccurrence is established once. The complete immediately relevant responder set is identified from pinned state. Responses execute under registered ordering/commutativity semantics; mechanically non-commutative unresolved order requires typed adjudication, never SQL ordering.

### Case J — owner-local scheduled trigger

Due occurrence creates ordinary child Resolution with stable firing key. Result atomically re-arms/unarms/terminates owner as declared. Retry cannot fire the same due occurrence twice.

### Case K — expected reaction consumes procedure resource

Reaction child spends a procedure-local Resource under the shared Procedure. Parent resume re-reads Procedure state and cannot restore the pre-reaction spent value from Continuation.

### Case L — incompatible catalog adoption while suspended

Resume under different incompatible ResolvedCatalogContext fails/blocks until an authorized adoption/migration/abort path resolves the in-flight execution. No mixed semantic interpretation is allowed.

## 22. Traceability to accepted decisions

| Requirement / inherited constraint | Candidate decision |
|---|---|
| one message may contain multiple intents | finite ordered IntentPlan, non-atomic |
| Resolution means one Activity invocation | preserved exactly |
| deterministic transitions are distinct | direct transition upper path |
| one lower atomic correctness path | ExecutionSegment |
| procedure Resource owner cannot be Resolution/Continuation | `runtime.procedure` |
| pinned MechanicalContext + prospective DAG | mandatory segment pre-commit path |
| LLM cannot own engine facts | bounded discovery + deterministic binder + registered invocation facts |
| retry must not duplicate committed mechanics | command/resume fingerprint + stable segment/Event/firing identities |
| suspended work must recover | Continuation fixed inputs + checkpoint roots |
| Temporal Agenda is projection | due occurrence -> ordinary Resolution; owner state remains authority |
| recency cannot depend on retained trace bodies | compact application order evidence |
| no background scheduler | all execution begins from typed interaction/procedure/boundary/due processing |
| narration is not mechanical authority | transcript/semantic/chapter remain projections/records with separate roles |

## 23. Deferred work with explicit owners

### Step 4

- lore/knowledge/secrets/disclosure authority;
- knowledge-safe context selection for LLM binding;
- promotion of invocation-adjudicated facts into durable truth when justified;
- transcript/event/chapter narrative transformation semantics;
- spectator-visible projection contents and spoiler policy.

### Step 5

- repository publication/restoration of runtime continuity payloads;
- multiplayer/shared procedure conflict semantics;
- cross-scene order-key comparison and chronology reconciliation;
- private campaign versus public/spectator Git projection transport;
- transcript/history retention and compaction policy;
- checkpoint cleanup/expiry.

### Step 6

- full D&D seed verification of simultaneous trigger ordering;
- any proven specialized scheduled-trigger/expiry tie policy;
- final package/migration/catalog-gap coverage;
- concrete chain-limit defaults if they are ruleset/mode-specific.

## 24. Candidate exit criteria

Before canonicalization:

1. adversarial review SHALL attack duplicate authority, retries, reaction recomputation, Procedure ownership, child invocation identity, same-time due ordering, catalog migration, compaction, LLM bypass, and narrative/mechanical leakage;
2. every critical/major finding SHALL be resolved or explicitly escalated;
3. focused machine/schema/tests MAY be specified but implementation SHALL wait for canonical architecture + writing-plans gate;
4. roadmap/status SHALL identify the exact next Step-3 continuation.

Human decision required at this candidate stage: **NO, unless adversarial review exposes a new material product/architecture trade-off.**
