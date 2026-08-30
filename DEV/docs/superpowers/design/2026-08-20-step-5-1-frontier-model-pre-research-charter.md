# Step 5.1 — Frontier Model — Pre-Research Charter

Status: **FIXED PRE-RESEARCH CHARTER — RESEARCH NOT YET EXECUTED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **Architectural**

This charter is intentionally fixed before the substantive Step-5.1 repository research pass. Its purpose is to constrain the investigation without pre-selecting the answer.

---

## 1. Primary research question

Investigate the **minimum coherent model** required to describe progress, durability, recoverability, concurrency and projection coverage across HDM.

Do **not** assume that the existing terms `frontier`, `cursor`, `checkpoint`, `HEAD`, `revision`, `last_event_id`, `dirty`, `SOFT`, `HARD`, `recovery cut`, or any other early-project term represent the correct abstraction boundary.

Reclassify each relevant concept from first principles using current repository contracts and accepted Steps 1–4 ownership semantics.

The investigation must answer:

> Which independently meaningful progress/durability boundaries actually exist in HDM, which relationships among them are required for correctness, and what is the smallest vocabulary/model that can express those relationships without creating new semantic authority?

A valid result may conclude that some currently named concept is unnecessary, derivable, a cache, a pointer rather than a frontier, or belongs to a later slice.

---

## 2. Research posture

The research SHALL be **solution-blind**.

Do not begin by designing a unified frontier algebra and then fitting repository concepts into it.

Do not begin by assuming that recovery is represented by one scalar, one Git SHA, one event ID, one checkpoint, a vector cut, or any other specific shape.

Do not assume that every notion of "progress" deserves durable identity.

Do not assume that every durable pointer is an authority.

Do not assume that every monotonically increasing value is a frontier.

Do not assume that event-ID order is fictional chronology.

Do not assume that Git ancestry is fictional chronology.

Do not assume that `CURRENT.last_event_id` should survive Step 5.1.

Do not assume that `CURRENT.world_time.frontier` has the right final representation merely because its current semantics are legitimate.

Do not assume that a checkpoint is itself the recovery state.

Do not assume that Story projection coverage can be represented by the same kind of marker as campaign durability.

Prefer deletion, derivation, or later deferral over adding a general abstraction whose current consumer cannot be demonstrated.

---

## 3. Fixed inherited constraints

The investigation may challenge terminology and representation, but it MUST preserve these already accepted architectural constraints unless a genuine contradiction is discovered and explicitly escalated:

1. Current semantic state remains owned by its world/runtime domain owner; persistence metadata does not become a second current-state authority.
2. One long-lived durable `campaign/*` branch is the durable campaign branch.
3. Temporary `live/*` branches exist only for active shared-scene concurrency.
4. A mutable entity cannot simultaneously have two writable authorities.
5. Git commit/ref order is storage order, not fictional chronology.
6. Fictional chronology is primarily a partial order with adaptive precision.
7. Checkpoints are sparse recovery descriptors/frontiers, not snapshots that own current world state.
8. Temporal Agenda is a rebuildable derived index, not temporal obligation authority.
9. Procedure, Continuation, RuntimeCommand pending-child descriptors, owner-local TemporalBindings and other accepted runtime owners retain their Step-2/3 semantic ownership.
10. Story is durable but non-canonical and may lag authoritative gameplay/history.
11. Player disclosure remains distinct from fictional knowledge and objective truth.
12. Raw chat/model/process memory is not durable campaign authority.
13. Step 5.1 must not pre-design the serialization contract of Step 5.2, the checkpoint protocol of Step 5.7, the live mutation protocol of Step 5.8, or the chronology representation/algorithm of Step 5.9.
14. Step 5.0 retired misleading early abstractions; they must not be silently reintroduced merely because an old document used them.

If any fixed inherited constraint appears incompatible with correctness, stop treating that point as mechanical work and prepare a decision-ready contradiction for the human architect.

---

## 4. Mandatory concept reclassification

For every relevant existing or proposed concept, determine which of the following it actually is:

```text
SEMANTIC AUTHORITY
CURRENT STATE / WORKING VIEW
DURABLE STATE
UNPUBLISHED DELTA
DURABILITY REQUIREMENT
FRONTIER / COVERAGE BOUNDARY
CURSOR
POINTER
REVISION / GENERATION
RECOVERY EVIDENCE
PROJECTION
DERIVED INDEX / CACHE
TRANSPORT METADATA
RETENTION / GC SAFETY BOUNDARY
EPHEMERAL PROCESS STATE
OTHER — justify explicitly
```

Do not allow one field/concept to occupy two incompatible categories without an explicit reason and lifecycle.

For each classified concept record:

```text
Concept:
Repository representation(s):
Semantic owner:
Classification:
Meaning:
Identity, if any:
Domain of comparison:
Ordering/comparison relation, if any:
Monotonicity, if any:
Durable or volatile:
Recovery relevance:
Consumers:
Can it lag another domain?:
Can it be derived/rebuilt?:
Failure if stale/missing:
Duplicate-authority risk:
Current evidence:
Confidence:
Later-slice owner, if deferred:
```

---

## 5. Mandatory domains to investigate

Investigate at least these domains, while remaining open to discovering that two should merge or one should split:

- campaign durable publication;
- HOT/current working state relative to durable publication;
- unpublished/dirty accepted state;
- durability requirements currently described as SOFT/HARD;
- semantic event LOG traversal/coverage;
- checkpoint/recovery description;
- active live-epoch state;
- local scene chronology;
- globally reconciled chronology evidence;
- active operational runtime continuity;
- Story EVENTS projection coverage;
- Story MECHANICS projection coverage;
- Story NARRATIVE projection/coverage;
- Transcript/history retention;
- GC/compaction safety.

If a listed item is not actually a frontier domain, say so and classify it correctly rather than preserving the agenda wording.

---

## 6. Required distinctions to prove or reject

The research must explicitly determine whether HDM needs to distinguish each pair below and why:

```text
current truth
vs
durably published truth

branch ref
vs
observed/cached branch ref

Git commit object
vs
commit reachable from authoritative ref

working state
vs
unpublished delta

SOFT/HARD classification
vs
actual frontier

semantic LOG storage/traversal order
vs
fictional chronology

checkpoint pointer
vs
checkpoint descriptor
vs
recovery boundary

live branch HEAD
vs
live logical revision
vs
campaign durable frontier

source-history coverage
vs
Story projection coverage

projection coverage
vs
literary revision/version

retention eligibility
vs
causal/chronology age
```

A distinction that has no correctness consequence should not become architecture merely for conceptual neatness.

---

## 7. Hypotheses to attempt to falsify

The following are **working hypotheses only**. The research must actively try to disprove them.

### H1 — Git commit reachable from the campaign ref is the natural campaign durability boundary

Potential disconfirming evidence:
- accepted current state whose durability cannot be represented by one campaign ref;
- active authoritative live state that makes "campaign durable point" semantically insufficient without qualification;
- recovery obligations requiring an independent durable dimension.

### H2 — SOFT/HARD are requirement/classification concepts, not frontiers

Potential disconfirming evidence:
- a real ordered boundary with independent identity/coverage semantics that downstream recovery needs to reference.

### H3 — `CURRENT.last_event_id` may be useful only as a semantic-LOG cursor/coverage marker, not as chronology authority

Potential disconfirming evidence:
- no consumer actually requires the cursor;
- event IDs do not define a stable storage/coverage domain;
- another admitted index/frontier fully derives the same information;
- recovery requires a non-scalar event set rather than a single cursor.

### H4 — recovery may require a composite consistent description in multiplayer/runtime cases

Potential disconfirming evidence:
- a single durable campaign ref plus deterministic discovery is always sufficient and bounded;
- active live/runtime state can be reconstructed without any additional recovery frontier information;
- composite description adds no correctness or bounded-recovery value.

This hypothesis MUST NOT be treated as proof that a first-class `RecoveryCut` entity or schema is needed.

### H5 — Story projection frontiers are coverage/projection metadata, not campaign-state durability frontiers

Potential disconfirming evidence:
- any accepted gameplay semantics require Story publication to succeed atomically with canonical campaign publication.

### H6 — one universal frontier representation is likely unnecessary

Potential disconfirming evidence:
- several domains demonstrably share the same semantic ordering/coverage contract and consumers benefit materially from a common value type without losing domain meaning.

---

## 8. Repository evidence order

After this charter is fixed, inspect evidence in this order unless a concrete dependency requires a deviation:

1. current roadmap/status and Step-5.0 final resolution;
2. current canonical Steps 2–4 specs where frontier/recovery ownership was explicitly established;
3. active GAME runtime contracts: storage, persistence, durability guard, session, chronology, live scene, multiplayer;
4. active campaign schemas/templates: MANIFEST, CURRENT, checkpoint, scene/live, session/message/event and relevant indexes;
5. Step-3 runtime operational schemas/catalog entries for command/resolution/procedure/continuation/pending work;
6. tests/regression cases that establish observable semantics;
7. historical derivation documents only to explain provenance or detect stale assumptions, never as current authority;
8. external/primary comparable-system research only if repository evidence leaves a material design question where outside architecture practice can genuinely distinguish alternatives.

Do not browse generic "best practices" merely to decorate the design.

---

## 9. Mandatory evidence discipline

Every material research conclusion must be labelled as one of:

```text
FACT
CONSTRAINT
ASSUMPTION
INFERENCE
RECOMMENDATION
DECISION NEEDED
DEFERRED
```

For every assumption capable of changing the model record:

```text
Assumption:
Confidence:
Evidence:
Impact if false:
How to verify:
Revisit trigger:
```

Do not promote an old schema field, prose example or historical name into an accepted requirement merely because it exists.

When repository artifacts conflict, determine current authority and provenance before proposing reconciliation.

---

## 10. Mandatory counterexamples / break scenarios

At minimum, test the emerging model against all of the following before recommending anything:

1. Current HOT state contains accepted SOFT changes ahead of the durable campaign ref.
2. A HARD durability requirement arises while older SOFT changes also exist.
3. A Git commit object was created but ref advancement failed.
4. The local session cached campaign HEAD `C50`, while authoritative remote HEAD is `C53`.
5. Campaign durable state is `C50`, while one active live epoch was based on an earlier campaign state and has since advanced.
6. Two independent live epochs are active simultaneously.
7. One live epoch closes but has not yet been durably absorbed.
8. A checkpoint describes an older recoverable state while normal campaign publication has advanced beyond it.
9. A suspended Continuation or procedure-local obligation exists at a recovery boundary.
10. A scheduled temporal obligation is still live while the Temporal Agenda cache is absent.
11. Semantic events have sequential IDs/storage order while two fictional events remain temporally incomparable.
12. Fictional chronology later gains a cross-scene causal relation that was previously unnecessary.
13. Story EVENTS is caught up farther than NARRATIVE.
14. NARRATIVE is editorially revised without changing the authoritative event/history coverage it represents.
15. A restarted Chronicler must determine what source material is already projected without duplicating records.
16. A fresh chat/runtime starts with no prior model memory while active live/runtime state still matters.
17. Retention wants to delete old material that an active continuation, temporal obligation, checkpoint, chronology relation or Story provenance still needs.
18. A pointer references a missing/stale object.
19. Two frontiers from different domains use superficially comparable integers/IDs but have no semantic order relation.
20. A proposed general frontier abstraction has no consumer other than making the model look uniform.

For each scenario answer:

```text
What is semantic authority?
What is current?
What is durably established?
What is stale?
What is merely lagging?
What is comparable?
What is incomparable?
What evidence permits recovery?
What, if anything, must be persisted specifically to describe the boundary?
```

---

## 11. Alternatives that must remain available during research

Do not manufacture alternatives prematurely, but the final research must at least test these architecture shapes if evidence supports them:

### A — Domain-local semantics only

Each subsystem owns its own progress terminology and representation. No shared frontier vocabulary beyond basic prose conventions.

### B — Small shared semantic vocabulary, domain-specific representations

A few common relations/categories are defined (`authority`, `frontier`, `cursor`, `pointer`, `coverage`, `based_on`, `incomparable`), while each domain keeps the representation that matches its semantics.

### C — Unified first-class frontier model/value system

Most/all domains implement one generalized frontier/value abstraction with shared comparison/composition rules.

### D — Even simpler result

Research may conclude that several currently planned frontier concepts are unnecessary and that existing authorities plus a small number of explicit pointers/cursors suffice.

Do not select among these before repository evidence and counterexamples are complete.

---

## 12. Strongest anti-overengineering requirement

The research must explicitly answer:

> What is the simplest viable model that satisfies all currently demonstrated correctness/recovery/concurrency needs?

For every proposed new abstraction require at least one concrete current consumer and at least one failure/correctness problem it solves.

Reject an abstraction when its only benefit is:

- terminological symmetry;
- future hypothetical extensibility;
- making unrelated IDs comparable;
- hiding domain-specific semantics behind a generic wrapper;
- copying a distributed-systems pattern whose assumptions do not apply here.

---

## 13. Scope boundary with later Step-5 slices

Step 5.1 MAY establish semantic constraints that later slices must obey.

Step 5.1 MUST NOT finalize:

- durable serialization fields for Resumable Runtime Closure — Step 5.2;
- pending-work/Temporal Agenda recovery lifecycle — Step 5.3;
- host/session handoff protocol — Step 5.4;
- exact SOFT/HARD/SAVE trigger semantics — Step 5.5;
- Git publication transaction/failure protocol — Step 5.6;
- checkpoint storage/hydration/validation schema — Step 5.7;
- live epoch CAS/lease/compaction protocol — Step 5.8;
- final chronology representation/reconciliation algorithm — Step 5.9;
- Story catch-up/publication algorithm — Step 5.10;
- transcript retention policy — Step 5.11;
- host disclosure delivery acknowledgement — Step 5.12;
- GC deletion algorithm — Step 5.13.

If answering a Step-5.1 question requires one of these later details, record the minimum constraint and defer the representation/algorithm to its owner slice.

---

## 14. Required research output

The Step-5.1 Research & Architecture Draft must include:

1. repository evidence map;
2. normalized terminology table;
3. concept reclassification ledger;
4. actual frontier/progress domains discovered;
5. comparison/order relations that are genuinely required;
6. explicit non-relations/incomparability rules;
7. monotonicity/generation findings per domain;
8. analysis of `CURRENT.last_event_id` retain/replace/remove;
9. analysis of checkpoint pointer/descriptor/recovery-boundary distinction;
10. analysis of campaign vs active-live durability semantics;
11. analysis of projection lag/coverage without making Story authoritative;
12. recovery-composition findings without pre-selecting a schema;
13. counterexample results;
14. simplest viable alternative;
15. 2–3 credible architecture alternatives only if evidence leaves real alternatives;
16. current recommendation;
17. strongest counterargument;
18. assumptions/evidence ledger;
19. recommendation confidence and evidence that would change it;
20. exact later-slice constraints/deferred questions.

The output must not merely rename existing fields. It must explain why each retained concept exists and what would break without it.

---

## 15. Research stop / escalation conditions

Stop ordinary autonomous analysis and prepare a decision-ready human gate if research discovers any of the following:

- correct recovery requires a new durable semantic authority rather than metadata/projection over existing owners;
- one of the accepted Steps 1–4 ownership decisions must be reversed;
- multiplayer correctness requires a materially different durable branch topology;
- checkpoint must become a current-state snapshot authority;
- fictional chronology must become globally total rather than partial;
- Story must become part of the canonical gameplay commit barrier;
- a material quality trade-off remains genuinely balanced after analysis and constrains multiple later slices.

Do **not** escalate purely mechanical terminology, derivable relation definitions, or removal of an abstraction proven unnecessary.

---

## 16. Exit condition for the research phase

Research is complete only when the agent can answer, with evidence:

> For every gameplay-significant fact or obligation, where does current semantic authority live; what, if anything, proves its durability/recoverability; which progress markers are comparable; which are intentionally incomparable; and what is the minimum cross-domain vocabulary needed so later Step-5 slices cannot accidentally create duplicate authority or false ordering?

The research phase does not itself canonicalize the answer. It feeds the analytical challenge and Decision Brief phases of the Step-5.1 design cycle.

---

## 17. Pre-research charter self-review

Before fixation, this charter was challenged against the following failure modes:

```text
Does it smuggle in a unified frontier algebra as the expected answer?      NO
Does it assume a vector/composite recovery cut is required?                NO
Does it assume CURRENT.last_event_id must survive?                          NO
Does it treat Git representation as semantic design?                       NO
Does it assume monotonic scalar ordering across domains?                   NO
Does it permit negative/deletion/derivation outcomes?                      YES
Does it force current consumers for every new abstraction?                 YES
Does it preserve Steps 1–4 ownership boundaries?                           YES
Does it prevent Step 5.1 from pre-designing later Step-5 protocols?         YES
Does it require multiplayer/context-loss/projection-lag counterexamples?    YES
Does it distinguish repository facts from assumptions/recommendations?      YES
Does it contain a human escalation condition for true authority changes?    YES
```

No substantive repository research for Step 5.1 is considered executed by this charter itself.
