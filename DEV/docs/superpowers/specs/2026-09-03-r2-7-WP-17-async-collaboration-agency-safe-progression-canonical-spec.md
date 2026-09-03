# R2.7 WP-17 — Async Collaboration / Agency-Safe Progression — Canonical Specification

Status: **CANONICAL WP-17 RESULT — STEPS 1-8 COMPLETE / MANDATORY FINAL SENIOR AUDIT PENDING**

Date: 2026-09-03

Canonical direction:

> **SCOPED CAMPAIGN-OWNED COLLABORATION OBLIGATION / IMMUTABLE INTERACTION-CLAUSE HUMAN INPUT / COMPLETENESS-PROTECTED PLAYER ROUTING / EXPLICIT COLLECTION-TO-STEP-3 HANDOFF / NATIVE-OWNER-FIRST PROGRESSION**

Canonicalization basis:

- repaired WP-17 Step-1 Task Brief / open-world Source Manifest / whole-project critic;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-17-step-1-senior-recovery-SR17-01.md`;
- Step-2 evidence extraction + open-world Source Manifest expansion;
- Step-3 Decision Brief selecting Alternative C;
- Step-4 collaborative review;
- Step-5 candidate specification;
- Step-6 independent Source Manifest expansion;
- Step-6 whole-project adversarial review (`F17-01..F17-06`);
- Step-7 resolution/propagation gate.

This file is the single final implementation-facing WP-17 architecture owner, subject to mandatory final Senior audit. Earlier Step-2/3/4/5 artifacts remain evidence/design provenance. Where they differ from the Step-7 repairs incorporated here, this canonical specification governs.

This specification does not implement runtime/schema/template/catalog/test changes, does not start WP-18 and does not authorize implementation planning.

---

# 1. Central invariant and authority split

## LAW WP17-1 — Collaboration preserves unresolved human agency; it is not a second gameplay authority

Collaboration owns only:

```text
bounded human-input collection
scope-local waiting for that collection
one current collaboration generation
accepted human-input associations
collection close / handoff / obsolescence
```

It does **not** own:

- world truth or state consequence;
- player/PC authority;
- Procedure/Continuation/Choice/Reaction execution;
- mechanics or RNG;
- fictional chronology;
- `world.knowledge`;
- `runtime.message` communication evidence;
- `runtime.disclosure` recipient exposure;
- Story/Dramaturg planning;
- a generic job queue, scheduler, liveness service or global frontier.

## LAW WP17-2 — Existing native owner always wins its responsibility

Where an admitted existing owner already owns response order, execution, current state, chronology, information, authorization or persistence, collaboration references/coordinates with that owner and never copies or overrides its responsibility.

---

# 2. Coordination-family admission before representation

## LAW WP17-3 — Every relevant dependency is classified before any collaboration representation is chosen

Current coordination family for the responsibility being decided is exactly one of:

```text
INDEPENDENT_IMMEDIATE
AGENCY_DEPENDENT_COLLECTIVE
RULE_OWNED_ORDERED
```

Physical presence of `runtime.collaboration_obligation`, a message, a session, a PLAYER field or a LIVE record never chooses the family.

## LAW WP17-4 — `INDEPENDENT_IMMEDIATE` progresses now

Use `INDEPENDENT_IMMEDIATE` when no still-open human input can materially change the dependent consequence under the current owner/rules/currentness basis.

The native owner progresses immediately. Another player being absent, offline, slow or potentially interested creates no collaboration obligation.

## LAW WP17-5 — `RULE_OWNED_ORDERED` uses the native ordered owner

If `runtime.procedure`, `runtime.continuation`, pending Choice, pending Reaction or another admitted native owner already defines responder/order/resume semantics, that owner remains authoritative.

Generic collaboration does not mirror its responder set, queue, pending response, order, generation or continuation state.

## LAW WP17-6 — Durable collaboration exists only for independently durable `AGENCY_DEPENDENT_COLLECTIVE`

`runtime.collaboration_obligation` is admitted only when all are true:

1. a positive bounded material human dependency exists;
2. missing human input can still change the dependent result;
3. the decision opportunity exists under current owner/currentness/chronology evidence;
4. no native ordered owner already owns collection;
5. unresolved collection must survive participant/chat/session gaps or independent recovery/reference.

If condition 5 is false, ephemeral/local coordination is sufficient and no durable collaboration record is created.

---

# 3. Natural durable owner and physical route

## LAW WP17-7 — `runtime.collaboration_obligation` is the sole durable collection owner

For an admitted durable collective dependency, the semantic owner is:

```text
runtime.collaboration_obligation
```

Its current implementation-facing responsibility is limited to the collection lifecycle defined by this specification.

## LAW WP17-8 — Baseline collaboration obligation is campaign-owned

Closed WP-11 supplies the physical route:

```text
runtime.collaboration_obligation
    -> STATE/RUNTIME/COLLABORATION
    -> direct known-ID route
    -> no baseline collaboration index
```

An obligation remains campaign-owned even when its decision opportunity references selected LIVE/current native state.

LIVE physical packing does not become collaboration ownership.

## LAW WP17-9 — No generic collaboration registry/index/scheduler is baseline architecture

Ordinary correctness does not require:

- enumerating the collaboration directory;
- a campaign-global obligation registry;
- a queue broker;
- a background scheduler;
- a presence/heartbeat service;
- a total collaboration frontier.

Exact bounded routing is defined below through completeness-protected PLAYER companions plus direct known-ID obligation reads.

---

# 4. Stable obligation identity and generation lineage

## LAW WP17-10 — Stable obligation ID owns one bounded dependency lineage

One `obligation_id` represents one stable bounded collaboration dependency lineage anchored to one admitted dependency/purpose family and original blocked decision lineage.

A semantically unrelated/new decision opportunity receives a new obligation ID even when participants, wording or scene are similar.

A terminal obligation ID is never repurposed for another decision.

## LAW WP17-11 — One semantic generation is owner-local

```text
CollaborationGenerationIdentity := (obligation_id, generation)
```

`generation` is local lineage metadata. Numeric/lexical order is not fictional chronology, campaign-global currentness or player priority.

## LAW WP17-12 — Identity-defining generation semantics are immutable

At minimum, these are generation-defining where applicable:

- collaboration purpose;
- bounded dependency/scope identity;
- decision-opportunity identity/basis class;
- required contributor requirements;
- voluntary-PC agency binding required by those requirements;
- admitted semantic input class expectations;
- material safe-frontier association;
- explicit single-command execution anchor when the dependency contract requires one.

A material change to the same dependency lineage produces a successor generation. A semantically new dependency produces a new obligation ID.

Old generation meaning is never rewritten to make a stale reply appear current.

---

# 5. Currentness composition

## LAW WP17-13 — Collaboration generation currentness is distinct from every other currentness domain

Material use composes, as applicable:

```text
current obligation record + exact generation
current campaign source/revision
current selected LIVE/native decision opportunity
current Procedure/Continuation relation
current principal/PLAYER/control/authorization
current accepted input evidence
```

No single value replaces these dimensions.

An unrelated campaign commit may require publication refresh/rebase while the same collaboration generation remains semantically current.

## LAW WP17-14 — Technical source movement does not establish fictional order

Campaign ref movement, LIVE ref/CAS movement, message arrival, collaboration publication or generation allocation may change technical currentness/provenance. They do not establish fictional chronology unless the WP-15/native chronology owner independently admits that relation.

---

# 6. Existing mechanical `value.contribution` is a separate domain

## LAW WP17-15 — `value.contribution` remains exclusively Rule-Element mechanical contribution vocabulary

Mandatory semantic separation:

```text
existing value.contribution
    = Rule-Element mechanical calculation contribution
    != human async collaboration input
    != runtime.collaboration_obligation lifecycle
```

`DEV/ARCHITECTURE/RULE_ELEMENT_MODEL.md` remains the semantic owner for that existing kind. WP-17 does not rename, reinterpret or reuse it.

No new human collaboration `value.*` kind is admitted by WP-17.

---

# 7. Accepted human collaboration input owner and identity

## LAW WP17-16 — Human collaboration input reuses the existing accepted Interaction/IntentPlan owner graph

The accepted semantic input owner remains:

```text
runtime.interaction
    -> runtime.intent_plan
        -> embedded IntentClause
```

WP-17 creates no independent `runtime.collaboration_input` record.

## LAW WP17-17 — Exact human collaboration input identity is `(interaction_id, clause_id)`

```text
HumanCollaborationInputIdentity := (interaction_id, clause_id)
```

The corresponding IntentPlan is validated through the Interaction; `intent_plan_id` may be carried as integrity/routing metadata but does not create a second semantic identity.

A transport retry preserves the same Interaction/input identity. Identical prose in a later intentional Interaction is a new input identity.

## LAW WP17-18 — One collaboration-relevant clause is one immutable material semantic unit

For every collaboration-relevant accepted IntentClause, the accepted interpretation payload is immutable while referenced:

```text
interaction_id
clause_id
collaboration_semantic_class
normalized_semantics
material exact_text_ref(s), if any
```

The closed R2.5 semantic class is exactly one of:

```text
OOC_COORDINATION
DIEGETIC_COMMUNICATION
ACTIONABLE_INTENT
CONTROL_SIGNAL
```

If one host message contains several material semantic units/classes, Interpreter creates distinct IntentClauses under the same Interaction.

Correction/reinterpretation creates a new accepted input/current interpretation path. It does not rewrite the accepted meaning behind an existing identity.

## LAW WP17-19 — Collaboration-relevant IntentClause must be content-sufficient

A live collaboration consumer cannot depend on a bare input/message ID whose meaning disappears after lawful message compaction.

The existing accepted IntentClause/input owner must retain bounded normalized semantic content sufficient for its consumer.

Exact source wording is separately protected through Step-5.11 exact-text evidence only when exact form remains materially required.

Current machine schemas do not yet expose the final exact fields; that is downstream realization debt, not permission to copy transcript prose into collaboration state.

## LAW WP17-20 — `runtime.message` remains communication/exact-text evidence, not collaboration input identity

A message may contain multiple semantic inputs, may later compact and may be visible to recipients under independent disclosure rules.

Message presence/order does not establish collaboration meaning, truth, fictional knowledge, contribution currentness or fictional chronology.

---

# 8. Obligation stores references, not transcript or duplicated input bodies

## LAW WP17-21 — Accepted input associations are reference-only

Conceptually the obligation owns associations equivalent to:

```text
AcceptedInputUse {
    obligation_id
    generation
    requirement/purpose/scope association
    interaction_id
    clause_id
}
```

It does not copy:

- source transcript prose;
- complete message body;
- full IntentPlan;
- command/procedure payload;
- context bundle;
- another player's private context.

The referenced accepted input owner/evidence remains a required durable dependency while a live consumer needs it.

## LAW WP17-22 — Input identity and use are separate

One accepted input identity may satisfy more than one collaboration use only if each use independently proves deterministic semantic compatibility/currentness/admission.

Same wording, same source message or same participant never implies compatible reuse.

---

# 9. Required and optional contributors

## LAW WP17-23 — Required contributors need positive bounded material dependency

A participant becomes required only when current evidence proves their still-open input can materially change the dependent result.

Party/campaign membership, repository access, scene presence, availability or hypothetical interest is insufficient.

## LAW WP17-24 — Required set is minimal

Each required requirement binds, as applicable:

```text
player_id
pc_id?                        # voluntary PC agency dependency
purpose
scope/dependency
generation
allowed semantic class(es)
```

Only the minimum contributor set that can change the dependent result blocks progression.

## LAW WP17-25 — Optional contributors never block through silence

Optional eligible contributors may supply input while the generation is OPEN, but their silence alone cannot prevent collection close.

## LAW WP17-26 — Explicit non-action is not absence

A typed `PASS`, `READY`, `NO_FURTHER_INPUT` or equivalent may satisfy a requirement only where the owning semantics admit that non-action.

Absence/silence never synthesizes it.

## LAW WP17-27 — Required voluntary agency follows current control

If PLAYER membership, PC control or authorization changes materially while waiting:

1. re-evaluate whether the decision opportunity still exists;
2. do not rewrite the old generation's authority requirement in place;
3. obsolete/supersede the generation when requirement identity changes;
4. create a successor from current authority only when the same dependency lineage remains valid;
5. never infer a voluntary fictional action from controller transfer itself.

---

# 10. Completeness-protected PLAYER routing companion

## LAW WP17-28 — Nonterminal obligations have bounded positive PLAYER routing companions

Because WP-11 defines no baseline collaboration index and WP-14 forbids broad ordinary recovery scans, every nonterminal generation maintains completeness-protected routing references on the bounded current PLAYER records that must be able to recover the barrier.

Conceptually:

```text
RequiredCollaborationRouteRef {
    obligation_id
    generation
}

PLAYER.collaboration_route_refs[]
```

Exact later field spelling is machine-realization work.

## LAW WP17-29 — Route holders are bounded and derived from collaboration ownership relationships

At minimum, route holders include:

- every required contributor PLAYER;
- every PLAYER owning a collaboration-held accepted input whose dependent semantic unit remains behind the obligation;
- another PLAYER only when the generation's explicit bounded recovery/recipient contract requires them to recover that same barrier.

Optional merely eligible contributors are not route holders solely because they could contribute.

## LAW WP17-30 — Obligation and PLAYER routing companion share one campaign durability closure

Because both are campaign-owned, create/successor/terminal changes that affect route holders publish coherently with all affected PLAYER route refs.

For `OPEN`/`CLOSED`, current route holders carry the exact `(obligation_id,generation)` ref. Terminal `RESOLVED`/`OBSOLETE` removes it in the same campaign native-domain closure.

A required routing ref never points durably to an unpublished obligation generation.

## LAW WP17-31 — PLAYER routing companion is not collaboration authority

The companion only nominates exact obligation identity.

It cannot:

- satisfy/close/obsolete the obligation;
- grant input authority;
- prove current underlying opportunity without dereference/revalidation;
- transfer PC agency;
- make `PLAYER_INDEX.yaml` a collaboration index;
- make stale session/cache state authoritative.

An exact current PLAYER record whose companion passed its completeness invariant can terminate ordinary routing when no matching ref exists. That is a complete routing/protection contract, not semantic ownership of collaboration state.

Mismatch/corruption is an integrity/repair condition, not authorization to scan all runtime records on the ordinary path.

---

# 11. Accepting one human collaboration input

## LAW WP17-32 — Agency-bearing input requires current WP-16 authorization chain

Before association:

```text
trusted current authenticated principal
-> stable external user identity
-> exactly one current active PLAYER
-> current controlled PC where applicable
-> purpose-specific authorization
-> current obligation + exact generation
-> current underlying campaign/LIVE/native opportunity
-> accepted Interaction/IntentClause identity
-> allowed semantic class
-> deterministic purpose/scope/generation compatibility
```

Repository permission, stale session state, old message identity, cached participant list or possession of an obligation ID is insufficient.

## LAW WP17-33 — Duplicate association is idempotent

Repeated association of the same `(interaction_id, clause_id)` to the same obligation generation/use is a no-op/acknowledgement.

It cannot count, spend, execute or narrate twice.

## LAW WP17-34 — Same prose in a later Interaction is new input

A later intentional Interaction with identical words receives a new input identity and passes current interpretation/admission normally.

---

# 12. Stale, late and successor-generation input

## LAW WP17-35 — Old-generation input never mutates successor automatically

An input addressed to a terminal/obsolete/superseded generation:

- does not append to successor;
- does not reopen old generation;
- does not rewrite accepted fiction;
- may be acknowledged/rejected stale;
- may serve only as a discovery hint for an explicit current reinterpretation/reconfirmation path.

Any compatible reuse creates/currently admits a new use association under the current generation.

## LAW WP17-36 — Late input never replays accepted mechanics

Late/stale/duplicate collaboration input cannot rerun or replace:

- settled RuntimeCommand;
- committed ExecutionSegment;
- accepted firing/event identity;
- fixed RNG;
- consumed Continuation generation;
- already accepted native world/process consequence.

---

# 13. Collaboration-held `ACTIONABLE_INTENT` boundary

## LAW WP17-37 — A collaboration-held dependent actionable clause stays pre-command

For the dependent semantic unit while collaboration owns waiting:

```text
IntentClause.execution_state = intent.pending
IntentClause.command_id = absent
```

A RuntimeCommand MUST NOT be allocated/accepted for that dependent unit before collaboration handoff.

## LAW WP17-38 — Independent executable prefix is split before command acceptance

If one host message contains an independent executable semantic unit plus another unit that depends on collective input, Interpreter represents them as distinct IntentClauses.

The independent clause may enter normal Step-3 execution immediately. The dependent clause remains held.

Already accepted independent execution is never moved backward behind the collaboration barrier.

## LAW WP17-39 — Collaboration never synthesizes a RuntimeCommand

Collaboration creates no:

- collaboration command;
- synthetic system Interaction;
- multi-Interaction command ID;
- command anchor chosen from technical arrival/order.

Every released actionable unit remains owned by its original accepted IntentClause and enters the ordinary Step-3 command path after handoff.

## LAW WP17-40 — A single-command collective result needs an explicit semantic anchor

If one native command legitimately depends on several collected inputs, one semantically authorized execution-anchor IntentClause must be explicit in the generation/dependency contract.

The anchor clause owns the command through normal Step 3. Other closed accepted input refs become fixed dependencies in the accepted interpretation/input fingerprint.

The anchor is never inferred from first response, commit/CAS winner, message order or actor ID order.

If no admitted anchor/native mapping exists, collaboration does not fabricate one; the engine requires a current explicit input/clarification or remains blocked under the owning contract.

---

# 14. Collection lifecycle and explicit close

## LAW WP17-41 — One generation has monotonic collection lifecycle

Baseline states:

```text
OPEN
CLOSED
RESOLVED
OBSOLETE
```

Meaning:

- `OPEN` — accepts current compatible input;
- `CLOSED` — exact accepted input set is frozen and handoff is pending;
- `RESOLVED` — collection responsibility has been handed off/consumed by the accepted input/native owner boundary; collaboration no longer owns waiting;
- `OBSOLETE` — the opportunity/generation became invalid before successful handoff.

Baseline transitions:

```text
OPEN -> CLOSED -> RESOLVED
OPEN -> OBSOLETE
CLOSED -> OBSOLETE   # only before successful handoff
```

No same-generation reopen.

## LAW WP17-42 — Close is explicit and currentness-validated

`OPEN -> CLOSED` occurs only after current validation proves:

1. all required requirements are lawfully satisfied/discharged;
2. underlying decision opportunity remains compatible/current;
3. no native ordered owner has taken over the collection responsibility;
4. material chronology ambiguity necessary for the dependent consequence is resolved or collection remains blocked;
5. exact accepted input-use set is frozen.

Arrival/ref/CAS order never closes collection.

## LAW WP17-43 — Closed input set has order-independent identity

At close derive an immutable order-independent fingerprint:

```text
ClosedCollectionBasis :=
    (obligation_id, generation, closed_input_set_fingerprint)
```

The fingerprint covers the exact frozen semantic use associations according to a deterministic canonical encoding. Physical list/order does not affect meaning.

---

# 15. Explicit collection-to-Step-3 handoff

## LAW WP17-44 — Handoff maps frozen inputs to existing owners only

A deterministic ephemeral handoff classifies each closed accepted semantic unit into one legal next responsibility:

```text
RELEASE_TO_ORIGINAL_CLAUSE_COMMAND_PATH
CONSUME_AS_NONEXECUTABLE_SEMANTIC_INPUT
HAND_TO_EXISTING_NATIVE_OWNER
CLARIFICATION_OR_UNSUPPORTED
```

This handoff is not a new durable execution owner.

## LAW WP17-45 — Actionable handoff releases the original IntentClause

For a held actionable clause, successful handoff transitions the original accepted clause from `intent.pending` to `intent.ready` or another valid noncommand disposition selected by deterministic interpretation.

Only after that handoff may ordinary Step 3 allocate/accept its RuntimeCommand.

## LAW WP17-46 — Collaboration `RESOLVED` means collection handoff, not gameplay completion

`RESOLVED` is established when the collaboration collection responsibility has been successfully transferred/consumed by the existing accepted input/native owner boundary.

It does not wait for a later command, Procedure, Choice, Reaction or Continuation to finish.

After `RESOLVED`, those native owners operate independently. Collaboration never reopens to mirror them.

## LAW WP17-47 — Baseline handoff is campaign-domain, not distributed

Current WP-11 routes place obligation and IntentPlan records in campaign-native runtime roots.

When handoff mutates campaign-owned IntentPlans and obligation/routing companions, publish the correctness-required handoff closure as one campaign native-domain transaction:

```text
closed collection basis
+ affected IntentPlan clause readiness/disposition
+ obligation RESOLVED
+ affected PLAYER routing-ref removals
```

If the complete handoff cannot be established, obligation remains `CLOSED` and no dependent RuntimeCommand is accepted.

No campaign+LIVE distributed transaction is introduced.

## LAW WP17-48 — Native execution preserves collaboration source basis where material

After handoff, any RuntimeCommand/native consumer whose accepted interpretation depends materially on the closed collection preserves causal/idempotency evidence equivalent to:

```text
obligation_id
generation
closed_input_set_fingerprint
relevant accepted input refs
```

This basis is execution input/provenance evidence only; it does not make collaboration an execution owner.

If accepted native execution exists, recovery never re-releases/rerolls/replays it because collaboration metadata is stale. Repair proceeds forward from accepted evidence.

---

# 16. Concurrent updates and campaign publication

## LAW WP17-49 — Accepted input associations are semantically unordered unless an owner says otherwise

Within a generation, accepted input-use associations form an identity-keyed semantic set.

Physical array order, commit order and CAS winner order have no semantic priority by themselves.

## LAW WP17-50 — Campaign CAS serializes publication only

Concurrent compatible obligation mutations use WP-13 current-ref/non-force semantics.

After a ref conflict:

1. refresh current obligation + underlying basis;
2. if same generation remains OPEN and associations are independently valid/order-independent, deterministic set union/reapply is allowed;
3. if generation/lifecycle/purpose/required set/current opportunity changed, stale input does not carry into successor automatically;
4. if relative fictional order matters, use native rules/WP-15 rather than commit order.

A CLOSED generation does not accept new input association.

---

# 17. Maximal safe frontier and visible consequence

## LAW WP17-51 — Progress every independent consequence before waiting

For a collective dependency:

```text
accepted current input
-> identify exact positive dependency
-> resolve every consequence independent of missing human input
-> establish/persist safe prefix under native owners
-> expose only that same safe prefix
-> stop before first dependent consequence
-> collect/revalidate missing input if still required
```

## LAW WP17-52 — Visible consequence shares the same frontier

Narration/disclosure cannot present a dependent unresolved result as established because a draft, message, participant reply, commit or prediction exists.

Recipient-safe OOC waiting/status output is allowed.

## LAW WP17-53 — Safe frontier remains owner-native evidence

The obligation may reference the smallest owner-native state/event/occurrence/chronology evidence needed to recover the barrier.

It owns no global safe-frontier scalar, total timeline or campaign-wide wait clock.

Independent scenes/processes/consequences continue.

---

# 18. Absence, silence and automatic consequences

## LAW WP17-54 — Absence never supplies voluntary agency

Absence/silence/offline/disconnect/delay never supplies:

- consent;
- pass;
- PC speech/action;
- belief/emotion;
- controller transfer;
- approval of another participant's proposal.

Another player's report of an absent player's intended action remains a discovery hint, not authority.

## LAW WP17-55 — Absence is not automatic immunity

If current rules/world/process owners prove that no applicable voluntary decision/reaction remains open and a consequence is automatic, absence alone does not block it.

## LAW WP17-56 — Timeout/presence/heartbeat/message age have no correctness authority

None can close, resolve, obsolete or satisfy a correctness-critical collaboration generation by itself.

No autonomous background worker is required for correctness.

---

# 19. Chronology separation

## LAW WP17-57 — Technical order never chooses fictional order

None of these establishes fictional chronology or winner by itself:

- host/message arrival;
- Interaction/clause ID/order across independent players;
- accepted-input serialization order;
- campaign commit/ref order;
- LIVE ref/CAS order;
- wall-clock receipt;
- session/catch-up traversal;
- obligation ID/generation numeric order.

WP-15/native owners establish only the minimum material relation needed.

If relative order remains materially unresolved, dependent consequence remains behind the maximal safe frontier.

---

# 20. Join/rejoin and recipient-safe catch-up

## LAW WP17-58 — Current authority/routing precedes catch-up and mutable input

Join/rejoin path:

```text
trusted current principal
-> current PLAYER/membership
-> current controlled PC
-> current campaign/LIVE/native route/currentness
-> exact PLAYER collaboration route refs
-> direct load/revalidate current relevant obligations
-> current Procedure/Continuation/native requirements
-> recipient-eligible bounded R2.3 assembly
-> catch-up
-> accept new mutable input
```

## LAW WP17-59 — Catch-up is an ephemeral recipient projection

Catch-up may include only the bounded information needed for current participation, derived from current eligible owners/evidence.

It is not durable truth, a second transcript, a second collaboration owner or a read receipt.

## LAW WP17-60 — Current obligation presence grants no access to another participant's input content

A recipient-safe obligation projection may expose, where independently eligible:

- obligation identity/generation/status summary;
- current purpose/situation summary;
- the recipient's own requirement/opportunity;
- neutral waiting/received status metadata;
- independently eligible facts/messages/knowledge/disclosures.

An input appearing in the same obligation does **not** itself authorize disclosure of its normalized semantics or exact text.

Another participant's private/OOC input remains hidden unless an existing message/knowledge/disclosure/context owner independently grants access.

## LAW WP17-61 — No transcript/context/planning dump

Catch-up does not automatically include:

- full chat/transcript/history;
- all role context;
- another player's private context;
- DM-only truth;
- secrets not eligible to recipient;
- Dramaturg/planning-only material;
- raw ContextTrace;
- session/cache/index contents as authority.

## LAW WP17-62 — Cursor does not prove human consumption

Session/collaboration cursor hints may reduce retrieval work but do not prove what the human read, do not satisfy an obligation and do not establish collaboration currentness.

---

# 21. Truth / knowledge / message / disclosure boundaries

## LAW WP17-63 — Existing information owners remain distinct

```text
objective/current truth       -> natural world/runtime owner
fictional subject knowledge   -> world.knowledge
accepted communication        -> runtime.message
human recipient exposure      -> runtime.disclosure
role/task context              -> R2.3 projection
collaboration collection       -> runtime.collaboration_obligation when admitted
```

Repeated storage/presentation of one fact across these surfaces never merges their authority.

## LAW WP17-64 — Collaboration input proposition is not truth by presence

A player may state a claim, intention or interpretation. Its accepted message/input evidence does not make the proposition objectively true, make every PC know/believe it or grant every human recipient disclosure.

Those changes follow their existing owners.

---

# 22. Durability and publication

## LAW WP17-65 — Admitted nonterminal collaboration state is durable because survival is its admission premise

A mutation another participant/recovery/dependent edge may rely upon becomes durable through normal campaign publication before that reliance is acknowledged.

This applies where material to:

- obligation creation;
- generation/successor transition;
- accepted input association;
- explicit close;
- handoff/RESOLVED;
- OBSOLETE transition;
- completeness-protected PLAYER routing companions.

This is not a generic per-message save rule. `INDEPENDENT_IMMEDIATE` and `RULE_OWNED_ORDERED` follow their own owners.

## LAW WP17-66 — Durable reference closure includes required accepted input semantics

A durable collaboration association cannot point to an unpublished required Interaction/IntentPlan/IntentClause semantic owner.

If exact wording remains required, the required Step-5.11 exact-text evidence/protection relation also survives.

## LAW WP17-67 — Normal WP-13 campaign publication applies

Use one immutable current campaign transaction snapshot, current authorization, exact dirty path set, non-force ref transition and rebase/re-evaluation on conflict.

No collaboration-specific transaction journal, distributed rollback or commit-order semantics are introduced.

---

# 23. LIVE/native dependency composition

## LAW WP17-68 — Collaboration remains campaign-owned when dependency touches LIVE

The obligation references/revalidates the selected native opportunity. It does not become LIVE-owned.

## LAW WP17-69 — No campaign+LIVE distributed transaction

Before obligation input association/close/handoff, validate the smallest underlying current LIVE/native basis needed by the dependency.

Later source movement may obsolete or change a still-open/closed pre-handoff generation according to owner law, but cannot rollback accepted independent native success or create fictional order from technical movement.

After collaboration handoff RESOLVES, later gameplay currentness/conflict belongs to Step-3/WP-16/native owners and never resurrects the collaboration generation.

---

# 24. Recovery

## LAW WP17-70 — Recovery starts from current PLAYER routing plus current native authority

For participant-facing recovery/rejoin:

1. resolve current campaign and trusted principal;
2. load current PLAYER by stable binding;
3. inspect completeness-protected collaboration route refs;
4. direct-route each nominated obligation and validate exact generation/nonterminal relationship;
5. hydrate referenced accepted input semantics;
6. resolve current underlying campaign/LIVE/native opportunity;
7. revalidate current PLAYER/control authorization before mutable input;
8. build recipient-safe catch-up;
9. resume OPEN collection, CLOSED handoff or bounded repair/obsolescence as current evidence requires.

## LAW WP17-71 — Accepted execution is never reconstructed from collaboration

After successful handoff, accepted Command/Procedure/Continuation/RNG/segment evidence remains with its native owner.

Recovery resumes that evidence and never rematerializes it from an old collaboration record.

## LAW WP17-72 — Session/checkpoint/cache/index never become collaboration authority

They may nominate positive recovery evidence only where their owners allow it. They cannot close/satisfy/obsolete obligations, authorize input or override direct current obligation/native owners.

---

# 25. Failure / ambiguity behavior

## LAW WP17-73 — Ambiguity blocks only the dependent scope

Typed bounded refresh/block/repair applies when material uncertainty remains, including:

- zero/multiple/malformed current obligation generations;
- PLAYER routing companion mismatch;
- stale/terminal route ref;
- required contributor no longer authorized;
- current opportunity moved/vanished;
- collaboration close races an input;
- material chronology ambiguity;
- content-insufficient accepted input after message compaction;
- missing required exact-text evidence;
- no legal native command anchor/handoff mapping;
- catch-up eligibility ambiguity;
- partial campaign publication conflict.

Do not guess, replay, reroll, globally freeze, synthesize agency or scan the whole repository as the ordinary fallback.

---

# 26. Performance / scaling discipline

## LAW WP17-74 — Ordinary cost scales with active bounded dependency

Known obligation reads use direct WP-11 routing. Join/rejoin begins from current PLAYER route refs. Input association checks only the current generation, bounded participant/control/native basis and referenced input semantic unit.

No work scales with campaign age by default.

## LAW WP17-75 — Derived optimization remains dormant until measured need

Do not introduce a partitioned collaboration index, retention compactor, fanout service, background expiration worker, queue broker or global routing service until a concrete consumer/measurement proves it necessary and the final authority boundaries remain intact.

WP-24 owns measured performance activation questions.

---

# 27. Current machine-realization debt

The current accepted architecture requires later coordinated realization of at least:

1. exact `runtime.collaboration_obligation` schema;
2. exact collaboration lineage/generation/lifecycle/current-basis/reference fields;
3. collaboration-relevant immutable IntentClause semantic class + normalized content;
4. held `ACTIONABLE_INTENT` pre-command validation and handoff transitions;
5. closed input-set deterministic fingerprint;
6. completeness-protected PLAYER collaboration routing companion;
7. route-ref publication/recovery integrity checks;
8. recipient-safe obligation catch-up projection;
9. execution input/provenance linkage to closed collection basis where material;
10. dedicated regression/adversarial coverage;
11. shipped CORE/session prose alignment.

These are implementation/test obligations only. They do not authorize modification in WP-17 architecture Steps 1–8.

Mechanical `value.contribution` remains unchanged.

---

# 28. Required downstream verification themes

Later executable coverage must include at least:

- all three coordination families;
- no obligation for independent input;
- native Procedure/Continuation/Choice/Reaction exclusion;
- obligation admission and stable lineage/generation;
- required vs optional contributors;
- PLAYER routing companion completeness/nonauthority;
- multi-player rejoin recovery without global scan;
- immutable one-unit-per-clause input semantics;
- `value.contribution` collision negative test;
- held actionable clause with no premature RuntimeCommand;
- explicit handoff to original Step-3 clause;
- no synthetic multi-Interaction command/arrival anchor;
- duplicate same input identity;
- same prose new Interaction;
- stale old generation;
- controller change / successor generation;
- close/input races and compatible set union;
- maximal safe and visible frontier;
- absence not consent and not immunity;
- no timeout/presence correctness;
- no technical-order chronology;
- recipient-safe catch-up/private input containment;
- message compaction content sufficiency;
- campaign/LIVE currentness movement without distributed transaction;
- recovery after OPEN/CLOSED/RESOLVED boundaries;
- no replay/reroll accepted mechanics.

---

# 29. Downstream work boundaries

- **WP-18** — Story / continuity / Dramaturg planning remains downstream. It receives no collaboration authority and is not started by this specification.
- **WP-19 / WP-20** — later bootstrap/schema/template/migration materialization where approved.
- **WP-22** — executable validation/regression realization.
- **WP-24** — measurement before collaboration routing/index/performance optimization.
- **WP-26** — reconcile stale shipped CORE/schema/catalog/test wording after accepted architecture.
- **WP-27** — implementation-planning readiness only when the R2.7 sequence reaches it.

No planning-only material is player catch-up evidence merely because it exists.

---

# 30. Canonical disposition

```text
SELECTED_ALTERNATIVE:         C / REPAIRED
STEP_6_BLOCKING:              2
STEP_6_SIGNIFICANT:           4
STEP_6_MINOR:                 0
UNRESOLVED_BLOCKING:          0
UNRESOLVED_SIGNIFICANT:       0
HUMAN_DECISION_REQUIRED:      NO
UPSTREAM_REOPEN_REQUIRED:     NO
SOURCE_MANIFEST_CLOSED_WORLD: NO
WP18_STARTED:                 NO
IMPLEMENTATION_PLANNING:      NO
NEXT_GATE:                    MANDATORY FINAL SENIOR AUDIT AFTER STEP 8
```
