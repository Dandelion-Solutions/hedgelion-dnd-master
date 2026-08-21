# Step 5.1 — Frontier Model — Architecture Task Brief

Status: **RESEARCH ASSIGNMENT — NOT A DESIGN DECISION**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Pre-research charter:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-pre-research-charter.md`

This Task Brief operationalizes that charter. The charter is controlling where this brief is less specific.

---

## 1. Classification

**Architectural / deep-work.**

Step 5.1 establishes terminology and relationships that constrain durability, recovery, multiplayer/live ownership, chronology, Story projection, retention and later implementation. A wrong abstraction can create duplicate authority or false ordering across several later slices.

---

## 2. Problem statement

HDM currently uses several concepts that describe some form of progress, state position, durability, recovery, ordering or projection coverage: campaign branch HEAD, cached/working HEAD, dirty accepted state, SOFT/HARD durability classifications, checkpoint pointers/descriptors, semantic event cursors, live-epoch branch/revision state, chronology frontiers and future Story/retention coverage.

These concepts were introduced at different times and for different purposes. Some may not actually be frontiers; some may be pointers, cursors, revisions, requirements, projections or caches. Treating them as one generic concept without evidence risks false comparability and new authority. Treating every domain as unrelated risks duplicated semantics and inconsistent recovery.

Step 5.1 must discover the minimum coherent semantic vocabulary and relation model that later Step-5 slices can rely on without deciding their representations prematurely.

---

## 3. Goals

1. Reclassify all relevant progress/durability/recovery concepts from current authoritative repository evidence.
2. Identify the actual independent domains in which progress/coverage/order boundaries matter.
3. Define only the cross-domain vocabulary and relations required for correctness.
4. Explicitly identify which values/domains are comparable and which are intentionally incomparable.
5. Separate current semantic authority from evidence/pointers/cursors/projections about that authority.
6. Determine whether `CURRENT.last_event_id` has a justified surviving semantic role, should be replaced, or should be removed.
7. Establish the semantic relation among campaign publication, active live state, checkpoint/recovery description, chronology evidence and lagging Story projections without specifying later-slice schemas/protocols.
8. Produce exact constraints and open questions for Steps 5.2–5.13.
9. Prefer the simplest viable model; remove or defer abstractions without a demonstrated current consumer/correctness requirement.

---

## 4. Non-goals

Step 5.1 SHALL NOT finalize:

- Resumable Runtime Closure serialization or repository placement (5.2);
- pending/temporal execution recovery lifecycle (5.3);
- session/context handoff protocol (5.4);
- SOFT/HARD/SAVE trigger rules (5.5);
- Git tree/commit/ref publication transaction details (5.6);
- checkpoint schema/hydration/validation protocol (5.7);
- live CAS/lease/compaction state machine (5.8);
- final chronology data structure/algorithm or global ordering policy (5.9);
- Story catch-up/publication algorithm (5.10);
- transcript retention policy (5.11);
- disclosure host acknowledgement protocol (5.12);
- GC/compaction algorithm (5.13);
- implementation planning.

Later slices may be inspected only to identify constraints that Step 5.1 must support.

---

## 5. Fixed inherited constraints

Preserve unless current evidence establishes a genuine contradiction requiring owner decision:

- current semantic state belongs to its Step-1–4 world/runtime owner;
- persistence/recovery metadata does not create parallel current-state authority;
- one long-lived campaign branch is durable campaign storage;
- live branches are temporary shared-scene operational surfaces;
- one mutable entity cannot have two concurrent writable authorities;
- Git ordering is not fictional chronology;
- fictional chronology is primarily partial-order with adaptive precision;
- checkpoint is sparse recovery metadata, not a world snapshot authority;
- Temporal Agenda is rebuildable derived state;
- accepted Step-2/3 owners retain their responsibilities;
- Story is durable but noncanonical and may lag;
- raw chat/model/process memory is not campaign authority;
- retired Step-5.0 abstractions remain retired unless a later slice independently proves a replacement need.

---

## 6. Quality attributes that distinguish solutions

Priority order for this slice:

1. correctness / no duplicate authority;
2. recoverability semantics;
3. concurrency correctness;
4. avoidance of false total ordering or false comparability;
5. bounded inspectability/debuggability;
6. simplicity/YAGNI;
7. compatibility with later persistence and chronology design;
8. deterministic testability;
9. migration/reversibility.

No numerical performance target is invented in this slice.

---

## 7. Required repository evidence

Inspect, in order:

1. Step-5 roadmap/expanded agenda and Step-5.0 closure;
2. canonical Step-2/3/4 ownership and recovery constraints;
3. active `GAME/CORE` storage/persistence/durability/session/chronology/live/multiplayer contracts;
4. active MANIFEST, CURRENT, checkpoint, semantic-event, live-scene, scene/session/message schemas;
5. Step-3 operational machine contracts for command/resolution/procedure/continuation/pending-child/idempotency state;
6. current tests/regression cases that constrain observable behavior;
7. historical derivation only where needed to explain stale fields or terminology;
8. external primary evidence only if an unresolved architecture question remains after repository research.

Do not let historical proposal text override current canonical contracts.

---

## 8. Mandatory concept ledger

For each relevant concept record:

```text
Concept
Repository representation(s)
Semantic owner
Classification
Meaning
Identity
Domain of comparison
Ordering/comparison relation
Monotonicity/generation semantics
Durability
Recovery relevance
Consumers
Lag relation
Derivability/rebuildability
Failure if stale/missing
Duplicate-authority risk
Evidence/confidence
Later-slice owner if deferred
```

Permitted classifications include semantic authority, current/working view, durable state, unpublished delta, durability requirement, frontier/coverage boundary, cursor, pointer, revision/generation, recovery evidence, projection, derived cache/index, transport metadata, retention/GC safety boundary and ephemeral state.

---

## 9. Questions research must answer

At minimum:

1. What does “frontier” need to mean in HDM, if the term is retained at all?
2. Which existing “frontier-like” concepts are not frontiers?
3. What are the real independent progress/coverage domains?
4. Which relations are required: equality, ancestry/dominance, based-on, covers-through, projection-through, stale/lagging, incomparable, generation replacement, or something simpler?
5. What does campaign durable progress mean semantically, separately from a transport implementation?
6. How should accepted HOT state ahead of durable publication be described without creating another persistent owner?
7. Does `CURRENT.last_event_id` have a justified role as a log cursor/coverage marker, or can it be derived/removed?
8. What is the relation between a checkpoint pointer, checkpoint descriptor and the recoverable state boundary it describes?
9. How must active live state relate to the campaign durable base without pre-designing the live protocol?
10. What minimal notion of a consistent recovery description is forced by campaign + live + operational state, if any?
11. What role does chronology progress play without conflating it with publication or LOG storage order?
12. How should Story projection coverage be related to canonical source coverage while remaining non-authoritative?
13. What notion of retention/GC boundary is safe to name now without pre-designing GC?
14. Which concepts can be eliminated, derived or deliberately deferred?

---

## 10. Required falsification scenarios

Use all scenarios from the pre-research charter, including HOT-ahead-of-durable, failed ref advancement, stale session HEAD, multiple live epochs, closed-not-absorbed live epoch, checkpoint behind campaign HEAD, suspended operational state, missing Temporal Agenda, sequential event IDs with incomparable fictional chronology, Story layer lag/revision, cold runtime without model memory, retention dependency conflicts and generic abstractions without real consumers.

For every scenario identify semantic authority, current state, durable evidence, staleness/lag, comparability/incomparability and required recovery evidence.

---

## 11. Research deliverable

Create:

`DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-research-draft.md`

It must include:

- repository evidence map;
- fact/constraint/assumption/inference separation;
- normalized vocabulary;
- concept ledger;
- actual domain map;
- required relation model;
- `CURRENT.last_event_id` verdict candidates;
- campaign/live/checkpoint/chronology/Story relationship findings;
- counterexamples/failure analysis;
- simplest viable design;
- credible alternatives if more than one survives;
- current recommendation;
- strongest counterargument;
- assumption/evidence ledger;
- what evidence would change the recommendation;
- exact deferred constraints for later Step-5 slices.

---

## 12. Analytical challenge gate

Before Decision Brief:

- state the strongest case against the preferred model;
- compare against the simplest domain-local alternative;
- attack every assumption that introduces cross-domain vocabulary;
- attempt to show that any proposed generic frontier/cut type has no concrete consumer;
- test whether complexity was merely displaced into later slices;
- assess reversibility;
- state recommendation confidence and disconfirming evidence.

No recommendation proceeds to Decision Brief without this pass.

---

## 13. Escalation gate

Escalate to the human architect only if research establishes a material decision such as:

- need for a new durable semantic authority;
- contradiction with accepted Steps 1–4 ownership;
- materially different branch topology;
- checkpoint becoming state authority;
- forced global total chronology;
- Story joining the canonical gameplay transaction barrier;
- or a genuinely balanced cross-cutting trade-off that cannot be derived mechanically.

Do not escalate naming, mechanically derivable relation semantics, or deletion of demonstrably unused abstractions.

---

## 14. Exit criteria for Step-5.1 research

Research is complete only when, for every gameplay-significant fact/obligation class examined, the draft can say:

- where current semantic authority lives;
- what proves or describes durability/recoverability;
- which progress markers are comparable and under what relation;
- which are intentionally incomparable;
- what may lag;
- what may be rebuilt;
- and what minimum vocabulary later Step-5 slices may safely depend on.

Research completion does not itself canonicalize a design.