# Step 5.2 — Resumable Runtime Closure — Pre-Research Charter

Status: **FIXED PRE-RESEARCH CHARTER — RESEARCH NOT YET EXECUTED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Classification: **Architectural**

This charter is fixed before substantive Step-5.2 repository research. Its purpose is to constrain the investigation without pre-selecting a storage record, manifest, checkpoint shape, recovery protocol, durability policy, or lifecycle algorithm.

---

## 1. Primary research question

Investigate the **minimum gameplay-significant operational closure** that must be reconstructible after loss of process/chat/model memory at an already-established durable recovery boundary.

Do **not** assume that `Resumable Runtime Closure` must be a first-class record, one file, one checkpoint section, one manifest, one composite object, or one new semantic owner.

The investigation must answer:

> Which state and evidence must remain available so that a fresh HDM runtime can reconstruct the exact last durable gameplay point, enumerate every still-active authoritative operational owner and mandatory unresolved execution dependency, and resume without inventing canon, duplicating authority, replaying committed work, or silently dropping required work?

A valid result may conclude that the closure is primarily a **property of a compatible set of existing owners and references**, with little or no new persistent abstraction.

---

## 2. Research posture

The research SHALL be solution-blind and minimum-first.

Do not begin by designing a `runtime.recovery_closure`, `RuntimeClosure`, recovery manifest, checkpoint payload, snapshot, journal, or generic pending-work registry.

Do not assume that every in-memory runtime object must survive restart.

Do not assume that every gameplay-significant concept must be copied into a recovery projection.

Do not assume that a value is ephemeral merely because it is currently stored only in chat/process memory; determine whether that is an accepted RPO consequence or an architecture defect at a durability boundary.

Do not assume that durable campaign publication alone is sufficient for every active operational scope.

Do not assume the opposite: active runtime state may already be durably discoverable through native owners and require only bounded references rather than a new closure record.

Do not assume that the Temporal Agenda, MechanicalContext, dependency DAG, loaded-record cache, Context Assembler bundles, condition/effect aggregates, or prospective deltas should be serialized. Their existing status as derived/working material must be challenged only by demonstrated non-reconstructibility.

Do not design the temporal due-work lifecycle of Step 5.3, controlled handoff policy of 5.4, SOFT/HARD boundary rules of 5.5, publication crash protocol of 5.6, checkpoint schema/hydration protocol of 5.7, live CAS/absorption protocol of 5.8, or chronology representation of 5.9.

Prefer references to existing owners, deterministic reconstruction, and explicit ephemeral loss over duplicated snapshots or generic registries.

---

## 3. Fixed inherited constraints

The investigation MUST preserve these accepted constraints unless a genuine contradiction is found and escalated:

1. Step 5.1 domain typing and no-implicit-cross-domain-order laws.
2. Current world/domain/runtime state remains owned by its native semantic owner; recovery metadata never becomes a duplicate writable authority.
3. HOT current truth may be ahead of campaign publication; state destroyed before an applicable durability boundary cannot be truthfully reconstructed.
4. The authoritative campaign ref and reachable commit provide campaign-durable publication evidence, not fictional chronology.
5. Active live epochs may own mutable truth for routed scopes independently of campaign absorption.
6. `runtime.procedure` solely owns procedure-local ResourceState.
7. `runtime.resolution` owns one Activity execution state/cursor.
8. `runtime.continuation` owns one portable suspended Resolution generation and does not copy Procedure state, MechanicalContext, Temporal Agenda, DAG caches, or trusted prospective deltas.
9. RuntimeCommand / ExecutionSegment / pending-child contracts retain their accepted Step-3 causal and idempotency semantics.
10. Owner-local TemporalBindings and active Effect/Resource/LifeState owners retain temporal obligation authority; Temporal Agenda is a rebuildable derived index.
11. Fixed RNG/choice inputs that are already mechanically committed must not be regenerated after recovery.
12. Checkpoints are immutable recovery descriptors/evidence, not current-state snapshots or owners.
13. Story is durable but noncanonical and does not become a blocker for canonical operational recovery merely because it may lag.
14. Raw chat/model/process memory, hidden prompts and chain-of-thought are not campaign authority or required recovery payload.
15. No generic pending-global-consequence or generic job authority may be silently reintroduced after Step 5.0.
16. A fresh runtime must not require a campaign-wide guess/search when a bounded durable reference/owner set is required for correctness.

If correct recovery requires reversing any of these ownership constraints, stop ordinary analysis and prepare a decision-ready contradiction for the human architect.

---

## 4. Critical scope distinction: closure versus durability policy

Step 5.2 defines **what must be reconstructible at a recovery boundary**, not **when that boundary must be forced**.

The investigation SHALL distinguish:

```text
volatile current working state
    may exist before a durability boundary

last durable recovery basis
    the latest basis the system truthfully promises to reconstruct after total context/process loss

resumable closure at that basis
    all authoritative operational owners + irreducible recovery evidence needed to resume exactly from that durable basis
```

Step 5.4/5.5 may later decide when controlled context destruction or HARD semantics require producing a newer durable basis.

Therefore Step 5.2 must not accidentally turn every current runtime mutation into an immediate publication requirement.

---

## 5. Mandatory state classification

For every gameplay/runtime concept relevant to resume, classify it from evidence as one of:

```text
AUTHORITATIVE STATE
    native current semantic owner; if active at the durable basis, its relevant state must remain recoverable

IRREDUCIBLE RECOVERY EVIDENCE / POINTER
    not authority, but must survive because exact/bounded recovery cannot derive it safely from authorities alone

REBUILDABLE DERIVED STATE
    can be reconstructed deterministically/boundedly from surviving owners/evidence

TRULY EPHEMERAL STATE
    may disappear without changing the promised durable gameplay point or future deterministic behavior

VOLATILE CURRENT STATE AHEAD OF DURABLE BASIS
    gameplay-significant now, but intentionally outside the cold-recovery guarantee until a later durability rule forces publication

DEFECT / UNOWNED STATE
    gameplay-significant at a promised durable basis yet not reconstructible from admitted durable owners/evidence
```

Do not force the existing agenda labels if the evidence requires a sharper classification.

For each concept record:

```text
Concept:
Semantic owner:
Current representation(s):
Classification:
When mechanically material:
Must survive cold recovery?:
Why / why not:
Can be rebuilt from:
Bounded discovery path:
Identity/generation needed?:
Idempotency/replay relevance:
RNG/choice relevance:
Temporal-obligation relevance:
Live-scope relevance:
Failure if missing/stale:
Duplicate-authority risk:
Later-slice protocol owner:
Evidence/confidence:
```

---

## 6. Mandatory candidate inventory to validate

Investigate at least:

### World / persistent domain state
- current actor/asset/location/scene/effect/resource/life-state state needed by active execution;
- canonical definition/catalog context identity required to interpret that state.

### Step-3 operational execution
- RuntimeCommand disposition and mandatory descendant closure;
- Resolution state/cursor;
- Procedure identity/state roots and procedure-local ResourceState;
- Continuation generation and dependency references;
- committed ExecutionSegment/Event frontier and receipts/idempotency evidence;
- pending mandatory child descriptors and stable causal identities;
- pending Choice/Reaction state that is semantically part of suspended execution.

### Randomness / fixed decisions
- already-fixed RNG outcomes;
- future RNG stream/frontier state when required to preserve deterministic continuation;
- fixed choice/offer inputs that cannot be recomputed after a suspension without semantic change.

### Temporal owners
- active owner-local TemporalBindings;
- armed scheduled Effect trigger state;
- delayed Resource/LifeState recovery state;
- enough owner/evidence to rebuild Temporal Agenda without serializing it.

### Identity allocation
- campaign allocator state/reservations whose loss could alter identities already referenced by recoverable operational state;
- distinction between unpublished local IDs and campaign-scoped durable IDs.

### Routing / concurrency
- selected campaign identity/basis;
- active live-epoch identities/scopes/revisions when their mutable authority matters;
- scene/session routing references required for bounded recovery.

### Semantic resume point
- unresolved player decision/declaration/question when not already represented by an admitted Resolution/Continuation/Choice/Reaction owner;
- maintenance continuation frame and current session evidence only insofar as gameplay semantics would otherwise be lost.

### Dirty/publication bookkeeping
- determine whether any dirty-set/publication preparation evidence is required for **controlled** restart recovery, versus purely volatile transport state whose crash semantics belong to 5.4–5.6.

### Support / diagnostics
- `HDM_EXPORT_CURRENT_LOG`, `HDM_EXPORT_CHECKPOINT_LOG`, and `HDM_RESET_LAST_CHECKPOINT` must be able to describe/validate the admitted closure without becoming authority themselves.

---

## 7. Mandatory rebuildable candidates to attempt to keep out of durable authority

Actively try to prove these can remain rebuildable/ephemeral:

- Temporal Agenda;
- MechanicalContext;
- rule/effect dependency DAG caches;
- loaded-record/entity caches;
- condition/effect aggregation indexes;
- derived mechanical values whose inputs survive;
- Context Assembler request/bundle/cache state;
- narrative-generation scratch state;
- prospective/uncommitted state deltas inside an uncommitted ExecutionSegment;
- repository directory listings/search caches;
- cached project/runtime instruction context that can be reloaded from the selected runtime package;
- Story rendering/editorial working buffers.

Promote any of these into required recovery evidence only if deterministic bounded reconstruction is demonstrably impossible or would change gameplay semantics.

---

## 8. Core hypotheses to attempt to falsify

### H1 — Resumable closure is a property, not necessarily a record

Hypothesis:

> At a durable recovery basis, exact resumability can be expressed as closure over existing semantic owners plus a small set of native-domain recovery references/evidence.

Potential disconfirming evidence:
- recovery cannot enumerate the required owners without a durable manifest;
- active owners can exist but are not discoverable from any bounded root;
- compatibility among campaign/live/operational roots cannot be proven without explicitly persisted composition evidence.

### H2 — Most current caches remain rebuildable

Potential disconfirming evidence:
- a cache contains irreducible accepted choice/RNG/adjudication evidence not stored by its semantic owner;
- recomputation after restart can produce a different mechanically valid result than the pre-crash accepted result.

### H3 — Step-3 portable execution owners already carry most irreducible in-flight semantics

Potential disconfirming evidence:
- an admitted suspended execution depends on hidden process-local state not represented by Resolution/Procedure/Continuation/receipts/pending-child/choice/reaction/RNG contracts;
- exact resume requires replaying prose or LLM hidden state.

### H4 — Temporal Agenda need not survive

Potential disconfirming evidence:
- owner-local bindings cannot be enumerated boundedly from admitted recovery roots;
- due/not-due correctness requires agenda-local evidence unavailable from temporal owners/chronology.

Do not solve the due-work lifecycle here; only determine whether agenda state itself is irreducible.

### H5 — Cold recovery may require several domain-native roots but not one merged authority

Potential disconfirming evidence:
- campaign durable state always absorbs/allows deterministic discovery of every operational scope before a recovery boundary;
- or, conversely, correctness requires a new authoritative composite snapshot rather than references to native owners.

### H6 — Semantic resume state should be mechanical when mechanics are open, lightweight when no mechanical execution exists

Potential disconfirming evidence:
- every unresolved player-facing point can be represented uniformly by an existing Interaction/Command/Continuation owner;
- or some narrative/social decision has durable semantic consequences that require a richer explicit owner.

---

## 9. Required repository evidence order

After this charter is fixed, inspect evidence in this order unless a concrete dependency requires deviation:

1. Step 5.1 canonical spec and Step 5.0 final carry-forward;
2. Step 3 canonical execution spec plus its machine schemas/tests for Command, Resolution, Procedure, Continuation, ExecutionSegment, pending children, receipts, choices/reactions and RNG/fixed inputs;
3. accepted Step-2 temporal/recovery ownership contracts and schemas;
4. active GAME runtime contracts from the Project Map persistence/recovery hot path: `RUNTIME`, `STORAGE`, `SESSION`, `DURABILITY_GUARD`, `SAVE_CONTRACT`, `PERSISTENCE`, `INTEGRITY`, `RANDOMNESS`;
5. multiplayer/live/chronology owners only to expose cold-recovery constraints, without designing 5.8/5.9;
6. active persistent schemas/templates: manifest, current state, session, checkpoint, scene/live, event/index and any runtime-like persistent records that actually exist;
7. support/maintenance contract;
8. regression tests/case catalogs;
9. historical derivation only to explain provenance or detect stale assumptions;
10. external research only if current project evidence leaves a material architectural choice where comparable systems can distinguish alternatives.

The Project Map is discovery guidance, not evidence of semantics. Owning artifacts win.

---

## 10. Mandatory failure / recovery scenarios

The emerging classification must survive at least:

1. Clean turn boundary, no in-flight mechanics, fresh runtime loses all chat memory.
2. Current HOT/SOFT state exists ahead of durable publication and the process crashes unexpectedly.
3. Controlled handoff happens while HOT/SOFT state exists, but exact forcing semantics are not yet defined.
4. Resolution suspended awaiting player choice.
5. Resolution suspended awaiting reaction.
6. Procedure exists with procedure-local spent ResourceState.
7. A segment committed and emitted MechanicalEvents, and mandatory child work was materialized but not yet executed.
8. A mandatory child is required by committed semantics but its descriptor was not durably materialized.
9. Fixed RNG was drawn before suspension.
10. Future RNG stream position matters after restart.
11. Active Effect owns a scheduled trigger; Temporal Agenda is absent after restart.
12. Delayed Resource/LifeState recovery remains armed.
13. Two independent active live epochs exist at recovery time.
14. A live epoch contains operational durable state not yet absorbed into campaign branch.
15. A stale session still points to an older campaign/live revision.
16. Campaign allocator has generated identities referenced by active recoverable runtime state.
17. An unpublished/local identity reservation was lost before durability.
18. Player made a meaningful declaration but no mechanical Resolution was opened yet.
19. Master asked the player for a clarification/choice that has no current mechanical owner.
20. Maintenance restart occurs during an unresolved gameplay point.
21. Checkpoint pointer exists but checkpoint is older than current durable campaign state.
22. Required recovery reference is missing/corrupt.
23. Story projection/transcript state is missing while gameplay operational owners are intact.
24. An apparently convenient serialized cache disagrees with its native owner after restart.
25. Cold recovery can reconstruct semantics only by scanning all campaign files/history.

For each scenario answer:

```text
What state is currently authoritative?
What durable basis is actually promised?
Which owners must be recoverable?
Which irreducible pointers/evidence are required?
Which state is rebuilt?
Which state may truthfully be lost?
What would constitute an integrity defect?
What later slice owns the protocol details?
```

---

## 11. Alternatives that must remain available

The final research should admit only real alternatives supported by evidence, but must remain capable of concluding among shapes such as:

### A — Native-owner closure only

No new persistent closure abstraction. Recovery roots are derived from existing campaign/live/runtime owners and existing pointers/indexes; any extra references are fields of their natural owners.

### B — Lightweight recovery-root descriptor

A small non-authoritative descriptor enumerates/anchors only the active native owners needed for bounded cold recovery. It stores references/evidence, never copied current state.

### C — Checkpoint-carried closure manifest

The sparse checkpoint descriptor is extended in 5.7 to carry the active-owner/reference closure needed for cold recovery, while authority remains in native owners.

This is only a future representation possibility; 5.2 must not design the checkpoint schema.

### D — First-class resumable closure record

A dedicated runtime recovery descriptor exists independently of checkpoints/campaign state because evidence proves its lifecycle is independently required.

This is the highest-complexity option and must be rejected unless a concrete correctness/lifecycle consumer proves it necessary.

The investigation may produce a hybrid or a simpler result.

---

## 12. Anti-overengineering / anti-underengineering gate

The research must answer both:

> What is the smallest durable information set that makes cold recovery exact and bounded?

and

> What gameplay-significant state would be silently lost if we persisted only ordinary campaign world state plus a checkpoint pointer?

For every proposed durable recovery datum require:

- one concrete semantic owner or consumer;
- a concrete failure if the datum is absent;
- proof it cannot be deterministically and boundedly derived from existing surviving owners;
- a clear statement that it does not duplicate writable authority.

For every proposed ephemeral/rebuildable datum require proof that its loss cannot change the promised durable gameplay state or future deterministic execution.

---

## 13. Scope boundary with later slices

Step 5.2 MAY establish:

- classification of state/evidence;
- minimum cold-recovery closure requirements;
- bounded-discoverability requirements;
- owner/reference invariants;
- constraints on what later serialization/protocols must preserve;
- defects in current ownership where accepted durable semantics cannot yet be reconstructed.

Step 5.2 MUST NOT finalize:

- timer/due-work state machine — 5.3;
- when controlled chat/context loss forces publication — 5.4;
- exact SOFT/HARD/SAVE publication triggers — 5.5;
- Git transaction crash windows/retry — 5.6;
- checkpoint schema and hydration ordering — 5.7;
- live lease/CAS/compaction/absorption protocol — 5.8;
- chronology storage/reconciliation — 5.9;
- Story projection durability/catch-up — 5.10;
- transcript retention — 5.11;
- delivery acknowledgement — 5.12;
- GC algorithm — 5.13.

If a 5.2 classification depends on one of these later protocols, record the minimum constraint and defer the algorithm/representation to its owning slice.

---

## 14. Required research output

The Research & Architecture Draft must include:

1. repository evidence map;
2. complete operational-state classification ledger;
3. admitted durable recovery roots by semantic domain;
4. exact list of irreducible recovery evidence/pointers, if any;
5. rebuildable-state proof for major caches/indexes;
6. truly-ephemeral and volatile-ahead-of-durable classifications;
7. Step-3 in-flight execution closure analysis;
8. RNG/choice/reaction preservation analysis;
9. temporal-owner versus Agenda analysis without 5.3 lifecycle design;
10. identity allocator/reservation recovery analysis;
11. live-scope cold-recovery constraints without 5.8 protocol design;
12. semantic resume-point analysis outside active mechanics;
13. bounded-discovery analysis;
14. failure-scenario results;
15. simplest viable architecture;
16. 2–3 credible alternatives only if real trade-offs remain;
17. current recommendation and strongest counterargument;
18. assumptions/evidence ledger;
19. exact defects/gaps in current repository contracts;
20. later-slice constraints and deferrals;
21. explicit statement whether 5.2 requires a new architecture decision from the owner.

---

## 15. Prompt self-review / bias check

Before substantive research, challenge this charter itself:

- Does `Resumable Runtime Closure` wording imply a record/object? **No: explicitly treated as a property/set unless evidence proves otherwise.**
- Does the charter assume all current runtime state deserves durability? **No: it distinguishes rebuildable, ephemeral, and volatile-ahead-of-durable state.**
- Does it assume campaign HEAD is insufficient? **No: H5 is falsifiable in both directions.**
- Does it assume checkpoint must carry the closure? **No: checkpoint representation is deferred and only one alternative.**
- Does it pre-design Temporal Agenda persistence? **No: it actively attempts to keep Agenda rebuildable.**
- Does it collapse current truth with durable recoverability? **No: Section 4 separates them.**
- Does it let later Step-5 slices leak backward into 5.2? **Only minimum constraints may be exposed; algorithms/representations remain deferred.**
- Could a correct investigation conclude “no new record required”? **Yes.**
- Could it conclude an existing concept is an unowned defect? **Yes.**
- Could it reveal a genuine owner-level contradiction requiring human decision? **Yes; stop conditions below require escalation.**

No material expected answer is intentionally embedded beyond already accepted Steps 1–5.1 constraints and the central cold-recovery correctness requirement.

---

## 16. Research stop / escalation conditions

Stop autonomous architecture work and prepare a decision-ready human gate if evidence shows any of the following:

- exact recovery requires a new durable semantic **authority**, not merely evidence/references to existing owners;
- an accepted Step-2/3/4/5.1 state owner must be changed;
- a dedicated first-class closure descriptor with an independent lifecycle is materially required and alternatives remain genuinely viable;
- current product semantics must choose between materially different RPO/recovery guarantees rather than merely documenting existing accepted behavior;
- preserving exact unresolved player-facing semantic state requires a new fundamental interaction/decision owner;
- multiplayer cold recovery requires a branch/ownership topology change rather than later 5.8 protocol detail;
- a material trade-off between recovery exactness, publication frequency, storage/complexity, or gameplay latency remains balanced after analysis;
- a later slice must be pulled forward because 5.2 cannot be made coherent without deciding its fundamental architecture now.

Do not escalate derivable classifications, obvious missing references, terminology, regression tests, or later-slice constraints that follow mechanically from accepted ownership.

---

## 17. Research exit condition

Research is complete only when a fresh runtime with no prior chat/process/model memory can be reasoned about from a named durable basis and, for every gameplay-significant active state/obligation at that basis, the design can identify:

```text
semantic owner
-> durable/recoverable representation or irreducible reference
-> bounded discovery path
-> deterministic rebuild path for derived state
-> integrity failure when required evidence is absent/incompatible
```

without inventing canon, treating caches as owners, relying on hidden LLM memory, or silently advancing into later Step-5 protocol design.
