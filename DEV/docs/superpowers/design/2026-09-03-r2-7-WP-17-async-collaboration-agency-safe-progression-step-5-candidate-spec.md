# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Step-5 Candidate Specification

Status: **STEP 5 CANDIDATE — READY FOR INDEPENDENT WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-03

Selected direction:

> **SCOPED CAMPAIGN-OWNED COLLABORATION OBLIGATION / INTERACTION-CLAUSE HUMAN INPUT IDENTITY / CONTENT-SUFFICIENT SEMANTIC REFERENCES / NATIVE-OWNER-FIRST PROGRESSION**

This is a candidate, not the final WP-17 canonical owner. Step 6 must independently reconstruct the relevant whole-project graph and may invalidate or repair this wording before Step 8.

---

# 1. Scope and central invariant

WP-17 realizes asynchronous human collaboration without creating a second gameplay/execution/chronology/information authority.

Central invariant:

> **HDM waits only for a positive bounded still-material human dependency, only at the first dependent consequence, and only under the smallest owner that actually owns unresolved collection. All independent consequences continue under their native owners.**

Collaboration owns only:

```text
bounded collection
waiting state for that collection
current collaboration generation
accepted human-input references
collection closure/discharge/obsolescence
```

It never owns the gameplay consequence of the collected input.

---

# 2. Coordination-family admission

## CANDIDATE LAW WP17-1 — Classify coordination before choosing representation

Every material multi-human dependency is classified first as exactly one current coordination family for the responsibility being decided:

```text
INDEPENDENT_IMMEDIATE
AGENCY_DEPENDENT_COLLECTIVE
RULE_OWNED_ORDERED
```

Representation follows the family; storage presence never chooses the family.

## WP17-2 — Independent input does not create a wait owner

`INDEPENDENT_IMMEDIATE` applies when no still-open human contribution can materially change the dependent consequence under current owner/rules/currentness evidence.

The engine progresses immediately under native owners. Absence of another player is irrelevant by itself.

## WP17-3 — Native ordered owner wins

`RULE_OWNED_ORDERED` applies when `Procedure`, `Continuation`, pending `Choice`, pending `Reaction` or another accepted native owner already controls responder/order/resume semantics.

No collaboration obligation mirrors that responder set, order, continuation state or pending response.

## WP17-4 — Durable collaboration owner is admitted narrowly

`runtime.collaboration_obligation` is admitted only when all are true:

1. the dependency is `AGENCY_DEPENDENT_COLLECTIVE`;
2. a positive bounded human dependency remains material;
3. no native ordered owner owns collection;
4. the decision opportunity exists under current owner/currentness/chronology evidence;
5. unresolved collection must survive participant/chat/session gaps or independent recovery/reference.

Otherwise no durable collaboration record is created.

---

# 3. Natural owner, route and identity

## WP17-5 — `runtime.collaboration_obligation` is the sole durable collection owner

The family owns only its collection lifecycle and accepted-input associations. It does not absorb another semantic owner merely because that owner is referenced by the collaboration scope.

## WP17-6 — Baseline obligation is campaign-owned

The current physical family route is WP-11 campaign-native:

```text
runtime.collaboration_obligation
    -> STATE/RUNTIME/COLLABORATION
```

No baseline LIVE-owned collaboration record is introduced.

A collaboration dependency may reference current LIVE/native decision-opportunity evidence while its collection lifecycle remains campaign-owned.

## WP17-7 — Stable obligation identity and generation are separate

Current identifier policy supplies stable campaign obligation identity.

One semantic generation is:

```text
CollaborationGenerationIdentity := (obligation_id, generation)
```

`generation` is owner-local. It is not fictional time, campaign revision, message sequence or global collaboration frontier.

ID/generation numeric or lexical order has no fictional chronology/priority meaning.

---

# 4. Generation-defining semantics

## WP17-8 — Identity-defining collection semantics are immutable within one generation

At minimum, these are generation-defining where applicable:

- purpose;
- bounded collaboration scope/dependency identity;
- decision-opportunity identity/basis class;
- required contributor requirements;
- voluntary-PC agency binding required by those requirements;
- admitted semantic input class expectations;
- material safe-frontier association.

A material change does not rewrite old reply meaning. It obsoletes/supersedes the current generation and, where the dependency remains valid, creates a successor generation.

Optional non-authoritative diagnostics/presentation metadata need not force a new generation.

## WP17-9 — Collaboration currentness is domain-separated

Material use requires compatible current evidence for all applicable dimensions:

```text
current obligation record + generation
current campaign/LIVE/native decision opportunity
current native Procedure/Continuation relation
current principal/PLAYER/control/authorization
current accepted input evidence
```

No campaign HEAD, message sequence, session cursor or wall-clock scalar substitutes for this composition.

Unrelated campaign ref movement may require publication refresh/rebase without changing semantic generation.

---

# 5. Exact human async collaboration input

## WP17-10 — Existing mechanical `value.contribution` is reserved to Rule Element mechanics

Mandatory separation:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != collaboration-obligation lifecycle
```

WP-17 does not reuse or rename the existing kind.

## WP17-11 — Human collaboration input identity uses the existing accepted input owner

One accepted human semantic input unit is identified by:

```text
HumanCollaborationInputIdentity := (interaction_id, clause_id)
```

The clause belongs to the one `runtime.intent_plan` referenced by the `runtime.interaction`. `intent_plan_id` may be retained/revalidated as integrity metadata but does not create a second semantic identity.

A transport retry preserves the same Interaction identity. Same prose in a later intentional Interaction is new input.

## WP17-12 — Collaboration-relevant IntentClause is content-sufficient

For every clause referenced by a live collaboration consumer, the existing accepted input owner must retain bounded normalized semantic content sufficient to interpret the input after lawful raw-message compaction.

Conceptually:

```text
CollaborationRelevantIntentClause {
    clause_id
    collaboration_semantic_class
    normalized_semantics
    exact_text_ref?  # only when exact accepted wording remains material
}
```

`collaboration_semantic_class` uses the R2.5 closed set:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

The exact later schema spelling is implementation work. The semantic owner remains the existing IntentClause/InputPlan hierarchy; no `runtime.collaboration_input` record or new human-input `value.*` kind is admitted.

## WP17-13 — Message evidence remains separate

`runtime.message` remains accepted communication/exact-text evidence.

It is not the collaboration semantic input identity and does not become collection currentness merely because it contains the source prose.

If exact wording remains correctness-critical, Step-5.11 exact-text protection/slice semantics apply. Otherwise normalized IntentClause semantics are the durable semantic content.

## WP17-14 — Obligation stores accepted input references, never transcript prose

Conceptually:

```text
accepted_input_refs[]
    -> (interaction_id, clause_id)
    -> use association metadata owned by the obligation generation
```

The obligation does not copy the source message, full context, command payload or transcript.

The referenced accepted input owner/evidence participates in durable dependency closure while still required.

---

# 6. Input class and execution boundary

## WP17-15 — Human semantic input does not automatically execute a dependent consequence

An accepted IntentClause may be semantically valid collaboration input before the dependent collective result is executable.

For an `ACTIONABLE_INTENT` whose dependent consequence is blocked by collective agency:

- the IntentClause may remain an accepted pending semantic input;
- no dependent root RuntimeCommand/Resolution is executed merely because the input arrived;
- after collection closes, the applicable native execution owner performs the dependent interpretation/execution exactly once.

If a safe independent portion exists, Interpreter/native execution must split/address it so already-independent accepted consequences may establish before the collaborative barrier without later replay.

## WP17-16 — Already accepted independent semantics stay real

A collaboration input may reference a communication/action whose independent native consequence already became established before waiting at a later dependency.

Later collection closure/obsolescence never rewinds that established prefix.

---

# 7. Obligation lifecycle

## WP17-17 — One generation has monotonic collection lifecycle

Baseline states are equivalent to:

```text
OPEN
CLOSED
RESOLVED
OBSOLETE
```

Meaning:

- `OPEN` — current generation may accept currently authorized compatible inputs;
- `CLOSED` — accepted input set is frozen and no new input enters this generation; dependent native resolution may proceed;
- `RESOLVED` — collection obligation is discharged by accepted native outcome/evidence;
- `OBSOLETE` — underlying opportunity/scope became invalid/superseded before lawful resolution.

Baseline transitions:

```text
OPEN -> CLOSED -> RESOLVED
OPEN -> OBSOLETE
CLOSED -> OBSOLETE
```

No same-generation reopen. A new material need uses a successor generation.

## WP17-18 — Close is explicit, never arrival-order inferred

`OPEN -> CLOSED` occurs only after current validation proves:

1. all required contribution requirements are lawfully satisfied/discharged;
2. current underlying decision opportunity remains compatible;
3. no native ordered owner now supersedes generic collection;
4. material chronology ambiguity needed for the dependent consequence is resolved or the scope remains blocked;
5. the exact accepted input set for this generation is frozen.

Message/ref/CAS arrival order cannot close an obligation.

## WP17-19 — `CLOSED` is not execution state

`CLOSED` owns only collection closure. Dependent consequence returns to its natural Step-3/world/process owner.

If that execution suspends on Choice/Reaction/Continuation, the native owner controls resume. Collaboration does not mirror or reopen it.

## WP17-20 — `RESOLVED` stores discharge reference only

Where recovery/audit requires it, a resolved obligation may reference the accepted native consequence/execution/event that discharged it. It does not copy Procedure/Resolution/command/RNG state.

## WP17-21 — Obsolescence never manufactures an outcome

`OBSOLETE` neither invents missing input nor forces the result previously anticipated. It records that this generation no longer owns a valid collection opportunity.

---

# 8. Required and optional contributors

## WP17-22 — Positive bounded dependency is required

A contributor becomes required only when current evidence proves their still-open human input can materially change the dependent result.

Membership, scene presence, repository access, availability, friendship/party membership or hypothetical interest is insufficient.

## WP17-23 — Required set is minimal

Each required requirement binds as applicable:

```text
player_id
pc_id?                       # when voluntary PC agency is the dependency
purpose
scope/dependency
allowed semantic class(es)
generation
```

Only the minimum set capable of changing the dependent result is blocking.

## WP17-24 — Optional contributors never block through silence

Optional eligible input may be accepted while OPEN but its absence cannot prevent close solely because it was possible.

## WP17-25 — Explicit non-action differs from absence

A typed `PASS`, `READY`, `NO_FURTHER_INPUT` or equivalent may satisfy a requirement only where the owning semantics admit that non-action.

Silence/absence never synthesizes it.

## WP17-26 — Control/membership change re-evaluates generation

When voluntary PC agency is material and PLAYER/control/authorization changes:

- re-evaluate whether the decision opportunity still exists;
- old generation does not rewrite the required participant automatically;
- if requirement identity changes, obsolete/supersede old generation;
- create successor only from current authority if the dependency remains valid;
- no controller transfer creates a voluntary fictional action by itself.

---

# 9. Accepting input and use association

## WP17-27 — Agency-bearing input requires current authorization

Before association:

```text
trusted current principal
-> stable external user identity
-> exactly one current active PLAYER
-> current controlled PC where applicable
-> purpose-specific authorization
-> current obligation/generation
-> current underlying opportunity/native basis
-> accepted Interaction/IntentClause identity
-> allowed semantic class
-> deterministic purpose/scope/generation compatibility
```

Old session state, message identity, cached participant list, repository permission or stale obligation ref is insufficient.

## WP17-28 — Input identity and use association are distinct

One accepted input identity may be referenced by more than one obligation/purpose only when each use independently proves semantic compatibility and current admission.

No shared wording/message/participant implies reuse.

Use association conceptually includes:

```text
obligation_id
generation
requirement/purpose/scope association
accepted input identity
```

The association does not copy the input payload.

---

# 10. Duplicate, stale, late and reuse semantics

## WP17-29 — Same input identity is idempotent within one generation

Repeated association of the same `(interaction_id, clause_id)` to the same use association is an idempotent no-op/acknowledgement.

It never counts twice, spends twice or executes twice.

## WP17-30 — Later identical prose is new input

A later intentional Interaction with identical text is a distinct input identity and passes current interpretation/admission normally.

## WP17-31 — Stale generation cannot mutate successor

An input addressed to a terminal/obsolete/superseded generation:

- never appends to a successor automatically;
- never reopens the old generation;
- never rewrites accepted fiction;
- may be rejected/acknowledged stale;
- may be used as a discovery hint for an explicit current reinterpretation/reconfirmation path.

Compatible reuse requires current deterministic interpretation/admission; it is not inferred from wording similarity.

## WP17-32 — Accepted mechanics/RNG/idempotency never replay because input was late

Late/stale/duplicate input cannot rerun or replace:

- settled RuntimeCommand;
- committed ExecutionSegment;
- accepted firing/event identity;
- fixed RNG;
- consumed Continuation generation;
- already accepted native world/process consequence.

---

# 11. Concurrent obligation updates

## WP17-33 — Accepted input collection is semantically unordered unless an owner says otherwise

Within a generation, accepted input references are a semantic set keyed by their accepted identity/use association.

Physical array order, Git order and CAS winner order have no meaning unless the relevant rules/chronology owner explicitly defines an order relation.

## WP17-34 — Campaign CAS serializes publication, not fictional precedence

Concurrent compatible campaign updates use WP-13 non-force ref/currentness rules.

On ref conflict:

1. refresh current obligation/native basis;
2. if the same generation remains `OPEN` and both input associations remain independently valid and order-independent, deterministic set union/reapply is allowed;
3. if generation/lifecycle/purpose/required set/current opportunity changed, the stale attempt does not carry into successor automatically;
4. if relative semantic/fictional order is material, use the native rules/WP-15 owner rather than commit order.

A `CLOSED` generation rejects newly arriving input association unless a separate current owner creates a successor/reinterpretation path.

---

# 12. Maximal safe frontier

## WP17-35 — Progress every independent consequence before waiting

For an admitted collective dependency:

```text
accepted current input
-> identify exact positive dependency
-> resolve every consequence independent of missing human input
-> establish/persist the safe prefix under native owners
-> expose only that same established safe prefix
-> stop before first dependent consequence
-> collect/revalidate missing input if still required
```

## WP17-36 — Visible consequence shares the semantic frontier

Narration/disclosure cannot present a dependent unresolved result as established merely because a draft, prediction, message, commit or one participant's input exists.

Recipient-safe OOC waiting/status explanation is allowed.

## WP17-37 — Safe frontier is owner-native evidence, not a new scalar

The obligation may reference the smallest owner-native state/event/occurrence/chronology evidence needed to recover the barrier. It does not own a global `safe_frontier`, total timeline or campaign-wide wait clock.

Independent scenes/processes remain free to progress.

---

# 13. Absence, silence and automatic consequences

## WP17-38 — Absence never supplies voluntary agency

Absence/silence/offline/disconnect/delay never supplies:

- consent;
- pass;
- PC speech/action;
- belief/emotion/interpretation;
- controller transfer;
- acceptance of another player's proposal.

## WP17-39 — Absence is not automatic immunity

If current rules/world/process owners prove that no applicable voluntary decision/reaction remains open and a consequence is automatic, absence alone does not block it.

## WP17-40 — No timeout/presence correctness authority

Wall-clock timeout, message age, typing indicator, heartbeat, online status, reconnect state and host activity never close/resolve/obsolete a correctness-critical collaboration generation by themselves.

No background worker is required for correctness.

---

# 14. Chronology and technical order

## WP17-41 — Transport/technical order is not fictional chronology

None of these is fictional order by itself:

- message arrival;
- Interaction/clause order across independent participants;
- collaboration input-set serialization order;
- campaign commit/ref order;
- LIVE ref/CAS order;
- wall-clock receipt;
- session/catch-up order;
- ID/generation lexical/numeric order.

WP-15/native rules establish only the minimum material relation required.

If order remains materially unresolved, the dependent consequence remains behind the maximal safe frontier.

---

# 15. Join/rejoin and catch-up

## WP17-42 — Current authority precedes catch-up and mutable input

Before new mutable gameplay/collaboration input after join/rejoin:

```text
resolve trusted current principal
-> current PLAYER/membership
-> current controlled PC
-> current campaign/LIVE/native route
-> current Procedure/Continuation/collaboration obligations
-> recipient-eligible bounded Context Runtime assembly
-> catch-up
-> accept new input
```

## WP17-43 — Catch-up is bounded recipient projection

Catch-up derives from current owners and eligible evidence only. It may include:

- current situation necessary for action;
- PC/player-eligible knowledge/disclosure/history;
- current own unresolved native/collaboration requirements;
- bounded semantic recap needed to understand them.

It is not a second truth/history/currentness owner.

## WP17-44 — No transcript/context/planning dump

Catch-up does not automatically include:

- full chat/transcript/history;
- all role context;
- another player's private context;
- DM-only truth;
- secrets not eligible to recipient;
- Dramaturg/Story planning-only material;
- raw ContextTrace;
- session/cache/index contents as authority.

## WP17-45 — Cursor does not prove human consumption

Session/collaboration cursors/hints may reduce retrieval work but do not prove what the human read, do not satisfy obligations and do not establish collaboration currentness.

---

# 16. Truth / knowledge / message / disclosure boundaries

## WP17-46 — Existing information owners remain separate

```text
objective/current truth       -> natural world/runtime owner
fictional subject knowledge   -> world.knowledge
accepted communication        -> runtime.message
human recipient exposure      -> runtime.disclosure
role/task context              -> R2.3 Context Runtime projection
collaboration collection       -> runtime.collaboration_obligation when admitted
```

No one row/message/context bundle substitutes for another responsibility.

## WP17-47 — Message proposition is not truth or knowledge by presence

A human collaboration input may communicate a claim or action intent, but message/obligation presence does not make the proposition objectively true or every PC know/believe it.

Existing Step-4 semantic transitions decide those effects.

---

# 17. Durability and publication

## WP17-48 — Admitted obligation mutations have owner-defined shared durability

Because the record is admitted specifically to survive participant/chat gaps, a state mutation that another participant/recovery/dependent edge is allowed to rely on must become durable through normal campaign publication before that reliance is acknowledged.

This applies as relevant to:

- obligation creation/opening;
- generation/successor transition;
- accepted input association;
- explicit collection close;
- resolved/obsolete terminal transition.

This is not a generic per-message persistence rule. Inputs with no admitted durable obligation follow their native owners.

## WP17-49 — Accepted input dependency closes with the obligation reference

A durable obligation association cannot point to an unpublished required Interaction/IntentPlan/IntentClause semantic owner.

The campaign durability closure includes sufficient accepted input/evidence dependencies and exact-text protection routing where still required.

## WP17-50 — Normal WP-13 campaign publication applies

No collaboration-specific transaction/journal/commit protocol is introduced.

Use current authorization, exact path, coherent campaign delta and non-force current-ref semantics.

---

# 18. LIVE/native dependency composition

## WP17-51 — Collaboration record remains campaign-owned across LIVE dependency

A LIVE-owned decision opportunity is referenced/revalidated; LIVE does not become the collaboration collection owner.

## WP17-52 — No campaign+LIVE distributed transaction

Before obligation mutation/close/use, validate the smallest current underlying LIVE/native basis needed by the dependency.

After campaign publication, later LIVE/native movement may require refresh/obsolescence/reinterpretation, but does not roll back the accepted campaign record publication or accepted native gameplay edges.

Before dependent execution uses a closed collection, revalidate current native opportunity again.

## WP17-53 — Source movement can obsolete, not reorder fiction automatically

LIVE close/absorption/ref movement/CAS outcome may make a collaboration generation no longer applicable. That result follows owner/currentness semantics, not technical order as fictional chronology.

---

# 19. Recovery and routing

## WP17-54 — Current-authority-first recovery applies

A current open collaboration obligation is an admitted independent runtime root when current routing/lifecycle evidence identifies it for the requested recovery/participant scope.

Recovery loads:

1. current campaign route/basis;
2. current obligation record/generation;
3. referenced accepted Interaction/IntentPlan/IntentClause semantic dependencies;
4. current underlying native opportunity/currentness;
5. current participant/control authorization before new mutable input;
6. eligible catch-up projections.

Accepted mechanics/RNG/Continuation are resumed from their native owners, never replayed from collaboration.

## WP17-55 — Session/checkpoint/cache/index are not collaboration authority

They may provide bounded positive routing hints where their owner permits it. They cannot close/satisfy/obsolete an obligation or prove absence/currentness.

## WP17-56 — Ordinary collaboration recovery must remain bounded

The baseline introduces no campaign-global scan of all world/runtime/history and no generic collaboration registry.

Current participant/native lifecycle routing must expose sufficient bounded positive references to locate relevant current obligations. A later derived helper may be introduced only if a concrete machine consumer proves it necessary; such helper remains rebuildable/non-authoritative and cannot change obligation semantics.

Exact physical helper realization is deferred to later machine implementation evidence.

---

# 20. Performance and scaling

## WP17-57 — Ordinary cost scales with active dependency, not campaign age

For a known current obligation:

- direct WP-11 route;
- bounded current owner/authorization checks;
- bounded referenced accepted inputs;
- bounded required/optional contributor set.

No full collaboration history or all-player scan is required.

## WP17-58 — No speculative optimization authority

Do not add:

- partitioned collaboration indexes;
- retention compaction policy;
- background expiration worker;
- global fanout broker;
- cross-campaign service;
- presence service;
- queue scheduler

without measured WP-24/real consumer evidence and preserved authority boundaries.

---

# 21. Machine-contract alignment obligations

The current semantic result requires later coherent realization of:

1. `runtime.collaboration_obligation` exact schema;
2. collaboration-relevant IntentClause semantic class + normalized semantic content;
3. accepted input reference/use-association shape;
4. generation/lifecycle/current-basis/reference fields;
5. required/optional contributor requirement shape;
6. bounded current-obligation routing/recovery path;
7. schema/catalog/admission/identity consistency without changing mechanical `value.contribution`;
8. executable regression coverage;
9. shipped CORE/session cleanup against final accepted owners.

Current absence of these machine fields is implementation debt, not permission to weaken the semantic contract.

---

# 22. Failure / ambiguity classes

The final architecture must produce bounded typed handling for at least:

- no material dependency;
- native ordered owner already active;
- zero/multiple current obligation generation candidates;
- stale/terminal obligation reference;
- missing/malformed obligation record;
- required contributor no longer authorized/controlling PC;
- optional contributor silent;
- duplicate same input identity;
- same prose in new Interaction;
- old-generation input;
- current opportunity moved/vanished while waiting;
- collaboration close racing with another input;
- two compatible concurrent input publications;
- material chronology ambiguity;
- missing content-sufficient accepted input after message compaction;
- required exact-text evidence unavailable;
- recovery cannot locate current relevant obligation boundedly;
- catch-up candidate contains ineligible secret/private/planning material;
- stale session/cache/index nominates wrong obligation;
- attempted timeout/presence closure;
- attempted voluntary agency takeover for absent PC;
- partial campaign/LIVE durability/currentness movement;
- accepted execution already exists before a late response arrives.

Ambiguity blocks/retries only the dependent scope. It never justifies guessing, replay, reroll, global freeze or silent agency transfer.

---

# 23. Downstream boundaries

WP-17 candidate does not start:

- WP-18 Story/continuity/Dramaturg design;
- WP-19/WP-20 schema/template/bootstrap/migration implementation;
- WP-22 executable implementation/tests;
- WP-24 performance optimization;
- WP-26 stale consumer cleanup;
- WP-27 implementation planning.

Planning-only material remains ineligible for player catch-up unless independently established through an allowed source owner.

---

# 24. Candidate gate

```text
COORDINATION_ADMISSION_COMPLETE:             YES
DURABLE_OWNER_COMPLETE:                      YES
HUMAN_INPUT_IDENTITY_COMPLETE:               YES
CONTENT_SUFFICIENCY_COMPLETE:                YES
VALUE_CONTRIBUTION_SEPARATED:                YES
GENERATION_CURRENTNESS_COMPLETE:             YES
LIFECYCLE_COMPLETE:                          YES
REQUIRED_OPTIONAL_COMPLETE:                  YES
CONCURRENCY_IDEMPOTENCY_COMPLETE:            YES
MAXIMAL_SAFE_FRONTIER_COMPLETE:              YES
ABSENCE_AGENCY_COMPLETE:                     YES
CHRONOLOGY_SEPARATION_COMPLETE:              YES
CATCHUP_INFORMATION_COMPLETE:                YES
DURABILITY_RECOVERY_COMPLETE:                YES
GENERIC_QUEUE_SCHEDULER_FRONTIER:            NONE
HUMAN_DECISION_REQUIRED:                     NO
UPSTREAM_REOPEN_REQUIRED:                    NO
STEP_6_READY:                                YES
WP18_STARTED:                                NO
IMPLEMENTATION_PLANNING_STARTED:             NO
```
