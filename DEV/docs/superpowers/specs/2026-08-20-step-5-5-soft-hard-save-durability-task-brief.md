# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Task Brief

Status: **RESEARCH ASSIGNMENT — ARCHITECTURAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

## 1. Problem statement

Define one architecture-level contract for when gameplay-significant state may remain volatile, when durability becomes mandatory, what dependency-complete state must join a forced durability closure, and what an explicit player request such as `save`, `save game`, or `сохрани игру` promises.

Step 5.5 must reconcile the existing runtime SOFT/HARD/EPHEMERAL and `SAVE_ALL_DIRTY` vocabulary with the canonical recovery and host-lifecycle architecture from Steps 5.1–5.4.

The design must preserve sparse ordinary singleplayer publication while preventing a required durability boundary from publishing a logically incomplete subset whose omitted volatile dependencies would make cold recovery incorrect.

This slice defines semantic durability obligations. It must not choose the physical Git tree/commit/ref crash-consistency protocol owned by Step 5.6, checkpoint wire format owned by 5.7, or live-epoch ownership protocol owned by 5.8.

## 2. Classification

**Architectural / deep-work.**

Persistence semantics, recovery guarantees, publication completeness, explicit player-visible save promises, failure blocking, and downstream 5.6–5.8 interfaces are materially affected.

## 3. Fixed inherited constraints

Preserve unless a contradiction requires an explicit superseding owner decision:

- Step 5.1 B-NARROW domain typing and no implicit cross-domain order;
- Step 5.2 native owners remain authority; durable recovery is a compatible composition of domain-native sources plus bounded typed recovery routing, not a universal snapshot/frontier record;
- Step 5.2 lost unpublished HOT/SOFT state is never invented after total context loss;
- Step 5.2 open accepted execution requires recoverable compatible runtime/catalog interpretation context;
- Step 5.3 A-NARROW source/execution continuity and continuous bounded recovery reachability;
- Step 5.4 BARRIER-NATIVE controlled handoff: safe acknowledgement requires an actually durable compatible Resumable Runtime Closure; local handoff quiescence prevents closure drift;
- Step 5.4 no heartbeat/no-op handoff write when the required closure is already durable;
- Step 5.4 no trustworthy remaining host message/token/context capacity is assumed; advisory capacity heuristics are not correctness evidence;
- current world/runtime owners remain current-state authority; durability bookkeeping, commits, checkpoints and routing do not become duplicate state owners;
- no raw LLM/chat/process memory as campaign authority;
- no background daemon/timer is assumed when the host does not provide an execution opportunity;
- physical Git transport and ambiguous ref-update/crash outcomes remain Step 5.6;
- exact checkpoint/source-selection representation remains Step 5.7;
- multiplayer/live authority and visibility may impose stronger boundaries, but exact protocol remains Step 5.8.

## 4. Owner directions carried into this slice

### 4.1 Explicit save wording

The player-facing phrase `сохрани игру` / `save game` is a first-class durability intent and must receive a precise semantic promise. It must not degrade into a prose reminder or summary file.

### 4.2 Periodic SOFT safety flush

Owner direction from the preceding 5.4 work:

1. gameplay-significant unpublished SOFT should not remain exposed without bound when ordinary forced boundaries accumulate slowly;
2. the previously discussed `one hour` value is an example only, **not** an approved threshold or heuristic;
3. the semantic risk metric should concern age/exposure of relevant unpublished gameplay state, not merely elapsed time since any Git commit;
4. clean state must not create heartbeat/no-op publications;
5. if the host provides no background execution opportunity, the engine cannot promise a write at the exact instant a threshold is crossed;
6. capacity-risk signals/heuristics may exist, but their durability-policy effect is a 5.5 question and correctness cannot depend on them.

Existing runtime modules hard-code `one hour`; treat that number as provisional/stale pre-5.5 policy to be validated, replaced, parameterized, or rejected here rather than inherited as architecture.

## 5. Existing runtime hypotheses to test, not assume

Current `GAME/CORE/DURABILITY_GUARD.md` and `SAVE_CONTRACT.md` contain useful provisional behavior:

- durable facts become true in the hot working set immediately;
- ordinary gameplay changes are usually SOFT;
- a forced boundary flushes accumulated causally valid SOFT;
- explicit save creates `SAVE_ALL_DIRTY` and materializes established cross-session state;
- summary notes are not substitutes for normal authoritative records;
- clean state does not create heartbeat commits;
- publication failure must not be reported as saved.

Research must test whether these formulations remain correct after Steps 3, 5.1–5.4, especially:

- whether SOFT/HARD/EPHEMERAL classify state, obligations, boundaries, or combinations thereof;
- whether `all dirty` is too broad, too narrow, or exactly right once runtime operational owners and dependency closure are included;
- whether “causal” is the correct completeness relation, or whether recovery/reference/interpretation/routing dependencies must also participate;
- whether explicit SAVE has stronger semantics than an ordinary forced HARD boundary;
- whether narration/next-intent acceptance must block at all HARD boundaries or only specific externally observable ones;
- whether the current wall-clock anchor `durable_frontier_time` measures the actual exposure of dirty state correctly.

## 6. Goals

### G1 — Durability vocabulary

Define minimal precise semantics for:

- `EPHEMERAL`;
- `SOFT`;
- `HARD`;
- explicit `SAVE` / `SAVE_ALL_DIRTY` or a replacement concept if current naming is misleading.

Determine what each term classifies and what state transitions are legal.

### G2 — Required durability closure

Define a domain-typed dependency-complete closure for any state that must become durable.

At minimum investigate dependencies through:

- native authoritative current-state records;
- newly allocated/referenced identities and indexes;
- current routing required for bounded recovery;
- Step-3 command/resolution/procedure/continuation owners;
- Step-5.3 temporal owner/execution relations;
- accepted-message evidence when still irreducible under 5.4;
- compatible runtime/catalog interpretation context;
- integrity constraints and required provenance;
- active live/shared owner where relevant only to expose 5.8 requirements.

The closure must be complete for correct recovery without becoming “write every loaded record”.

### G3 — Forced boundary versus accumulated SOFT

Determine whether a forced durability requirement escalates:

- only the triggering HARD state;
- all dirty gameplay-significant state in the same writable scope;
- only a transitive dependency closure from the triggering requirement;
- or a hybrid rule.

Test atomic/coherence consequences of leaving unrelated SOFT volatile while publishing a HARD subset.

### G4 — Controlled handoff closure

Translate Step-5.4 BARRIER-NATIVE into an exact 5.5 durability obligation:

- what established SOFT/operational state must join a recovery-safe handoff;
- whether handoff is equivalent to explicit SAVE or a distinct closure;
- whether independent scopes may remain dirty without violating handoff semantics;
- what “all promised gameplay-significant state” means mechanically.

### G5 — Explicit save semantics

Define the exact contract of `save` / `сохрани игру`:

- what the player is entitled to expect after success;
- whether every established gameplay-significant dirty fact in the selected campaign scope must become recoverable;
- whether unresolved accepted execution/Choice/Reaction/Procedure/temporal obligations are included;
- whether explicit save creates a checkpoint or merely a durable closure;
- whether save changes campaign/session lifecycle (current expectation: no, unless separately requested);
- whether a save can succeed while a known dirty established fact remains intentionally volatile.

### G6 — Blocking / acknowledgement boundary

Define what actions are prohibited while a required durability obligation remains unsatisfied.

Investigate separately:

- acceptance of new gameplay-semantic input;
- further authoritative mechanics/state mutation;
- player-facing narration of an outcome whose durability is required before reveal;
- OOC/control communication;
- independent scopes.

Do not steal exact host-delivery acknowledgement from 5.12.

### G7 — Publication failure semantics

At the architecture level define outcomes when required durability cannot be established:

- remain HOT but blocked;
- retry;
- abandon a controlled boundary when semantically legal;
- terminate/degrade with honest recovery promise;
- user-action-required / integrity-blocked cases.

Do not specify Git tree/commit/ref mechanics.

### G8 — Bounded SOFT exposure policy

Define the semantic concept of maximum intended unpublished exposure without selecting an arbitrary number prematurely.

Investigate:

- what event starts exposure age;
- whether the metric is oldest dirty established state, oldest dirty closure, durable-frontier age, or another domain-typed concept;
- whether a successful partial publication can reset exposure for only the included state;
- first available runtime opportunity after threshold crossing;
- no-background-execution limitation;
- interaction with stronger immediate boundaries;
- no-heartbeat behavior;
- whether policy is configurable and at what scope (without choosing UI/config schema unless necessary).

### G9 — Advisory host-capacity risk

Determine whether an advisory capacity-risk signal should:

- only warn/offer handoff as already defined in 5.4;
- additionally request an opportunistic durability closure;
- or influence only the future configured exposure policy.

Any such behavior must remain safe under false positives and false negatives and must not promote the heuristic into authority.

### G10 — Later-slice interface requirements

Emit precise logical requirements for:

- 5.6 campaign publication/crash consistency;
- 5.7 checkpoint/recovery source selection;
- 5.8 multiplayer/live overrides;
- 5.10–5.12 only where canonical/noncanonical projection or host-delivery lag affects the meaning of save/durability.

## 7. Non-goals

Step 5.5 SHALL NOT choose or implement:

- the Git tree/commit/ref algorithm;
- exact transport retry/crash-window mechanics;
- prepared commit/object handling;
- checkpoint schema/wire format or universal recovery-cut record;
- live-epoch branch/CAS/lease/fencing/compaction protocol;
- fictional chronology persistence representation;
- Story projection publication machinery;
- transcript retention policy;
- exact host emission/read acknowledgement protocol;
- a raw model/chat snapshot;
- a campaign-global host lease;
- a universal scalar durability frontier;
- a background scheduler that the host cannot provide;
- an arbitrary numeric SOFT exposure threshold without owner approval.

Architecture closure does not itself require immediate GAME/schema implementation; machine-realization debt will be recorded for the later integrated implementation program.

## 8. Required repository evidence

Inspect at least:

- `AGENTS.md`;
- `DEV/DESIGN_PROCESS.md`;
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`;
- `DEV/PROJECT_MAP.md`;
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`;
- Step-5 expanded agenda;
- Step-5.2 canonical v2;
- Step-5.3 canonical spec;
- Step-5.4 canonical spec;
- Step-3 execution canonical spec where operational owners matter;
- `GAME/CORE/DURABILITY_GUARD.md`;
- `GAME/CORE/SAVE_CONTRACT.md`;
- `GAME/CORE/PERSISTENCE.md`;
- `GAME/CORE/STORAGE.md`;
- `GAME/CORE/RUNTIME.md`;
- `GAME/CORE/SESSION.md`;
- `GAME/CORE/INTEGRITY.md`;
- `GAME/CORE/RANDOMNESS.md` where fixed accepted RNG durability matters;
- `GAME/CORE/MULTIPLAYER.md` and `LIVE_SCENE.md` only to expose stronger-boundary interactions;
- `GAME/SCHEMA/current_state.schema.yaml`, `session.schema.yaml`, `checkpoint.schema.yaml`, campaign manifest/config schemas as relevant;
- current DEV runtime schemas for command/resolution/procedure/continuation/pending-child/temporal state;
- DEV tests/case catalogs that mention SOFT, HARD, save, dirty, durability boundary, one-hour, session boundary, handoff or publication completeness.

After structural inspection, search concrete symbols/phrases for consumers and stale duplicate policy.

## 9. Framing challenges

Research must remain able to conclude that current terminology is wrong. Explicitly test these possible mistakes:

1. **SOFT/HARD may be properties of durability obligations, not intrinsic permanent classes of facts.** The same fact may be SOFT now and required by a later boundary.
2. **A HARD trigger does not necessarily justify a global SAVE_ALL_DIRTY.** Scope/dependency boundaries may allow safe selective closure.
3. **Conversely, publishing only the triggering record may be incoherent.** Required recovery/reference/interpretation dependencies may extend beyond direct causality.
4. **Explicit save may be intentionally stronger than ordinary forced durability.** Do not assume equality merely because both publish state.
5. **`durable_frontier_time` may be the wrong exposure anchor.** A new dirty fact created long after the last commit should not inherit an artificially old age; unrelated publications should not reset unrelated dirty exposure.
6. **A numeric timer is policy, not architecture.** Establish semantics before choosing a value.
7. **No background callback means no exact wall-clock guarantee.** Do not promise impossible flush timing.
8. **Do not let a save note/checkpoint become a snapshot authority.** Native owners remain truth.
9. **Do not make narration universally wait on durability without proving a correctness need.** Latency/product experience matters.
10. **Do not let transport failure semantics leak upward into invented gameplay rollback.** State may remain established HOT even when durable publication failed, subject to blocking/recovery honesty.
11. **Do not conflate durable current-state closure with Story/transcript projection freshness.** Noncanonical projections may be allowed to lag unless the save promise explicitly includes them.
12. **Do not make advisory host-capacity heuristics correctness-critical.** False negatives must still fall back to normal durable recovery.
13. **Do not decide 5.8 by accident.** Shared visibility may require earlier publication, but live ownership mechanics remain later.

## 10. Quality attributes / fitness criteria

A candidate architecture must provide:

- honest, user-understandable save semantics;
- deterministic cold recovery from every successful required durability boundary;
- no duplicate state authority;
- dependency-complete publication obligations;
- sparse ordinary singleplayer Git traffic;
- bounded intended exposure of unpublished gameplay-significant SOFT;
- no required heartbeat writes;
- no impossible background-timer guarantee;
- bounded/local completeness rather than campaign-wide scans;
- explicit failure/blocking behavior;
- compatibility with Step-5.4 handoff quiescence;
- compatibility with future multiplayer/live stronger publication rules;
- testable edge cases and crash/failure dispositions;
- minimal new abstractions and YAGNI discipline.

## 11. Required analytical challenge

Before recommendation, explicitly challenge at least:

- intrinsic state labels vs dynamic durability obligations;
- `SAVE_ALL_DIRTY` vs dependency-scoped forced closure vs scope-wide dirty closure;
- whether explicit save must preserve all established dirty state or may intentionally leave some dirty scope volatile;
- whether explicit save and controlled handoff should have identical completeness semantics;
- whether a HARD boundary must block narration, next intent, both, or only continuation through a specific semantic edge;
- whether established HOT state may remain usable after publication failure while the host survives;
- whether a failed explicit save can be abandoned and play continue, and under what truthful warning/blocking semantics;
- whether SOFT exposure should be measured from first-dirty time rather than durable frontier time;
- whether independent dirty domains need independent exposure clocks/frontiers;
- whether advisory capacity risk should trigger opportunistic flush;
- strongest simpler alternative that removes HARD as an explicit category entirely and models only `MAY_DEFER` vs `MUST_DURABLE_BEFORE(edge)` obligations.

## 12. Minimum scenario matrix

Research must cover at least:

1. ordinary singleplayer action creates one SOFT world mutation;
2. many unrelated SOFT mutations accumulate;
3. a HARD-triggering transition depends on earlier SOFT state;
4. a HARD-triggering transition is independent of unrelated dirty SOFT in another scope;
5. forced handoff with dirty world + open RuntimeCommand/Continuation;
6. forced handoff where everything relevant is already durable;
7. player says `сохрани игру` with ordinary dirty world state;
8. player says `save` while Choice/Reaction/Procedure is suspended;
9. player says `save` during incomplete onboarding/provisional PC;
10. `save and stop` versus plain `save`;
11. explicit save with integrity-defective dirty material;
12. explicit save publication fails while host remains alive;
13. forced HARD publication fails while gameplay outcome already exists HOT;
14. crash after failed publication destroys HOT state;
15. dirty state created shortly after an old durable commit;
16. dirty state created long after an old durable commit;
17. unrelated successful publication while another dirty scope remains volatile;
18. threshold crosses while user is absent and no background callback exists;
19. next user interaction occurs after threshold crossing;
20. clean state remains idle far beyond threshold;
21. advisory near-capacity warning with dirty SOFT;
22. false-positive advisory warning;
23. hard host cutoff without warning before opportunistic flush;
24. multiplayer/shared rule requires earlier visibility than singleplayer policy;
25. explicit save when Story/transcript projections lag but canonical gameplay closure is complete;
26. new ID/index/routing dependency exists only in HOT state at forced boundary;
27. accepted RNG/Continuation dependency must survive a save/handoff closure;
28. partial selective closure would leave a durable reference to an unpublished owner;
29. two independent dirty scopes with different exposure ages;
30. no-op save when no gameplay-significant state is dirty.

## 13. Expected outputs

Produce:

A. precise durability vocabulary and authority model;
B. required durability-closure algorithm/relationship, conceptually not transport implementation;
C. forced-boundary vs accumulated-SOFT rule;
D. explicit save contract;
E. blocking/acknowledgement/failure matrix;
F. SOFT exposure policy model with no premature numeric constant;
G. advisory host-capacity disposition;
H. alternatives, strongest counterarguments and recommendation;
I. decision brief only for remaining material owner choices;
J. carry-forward requirements/debt for 5.6–5.8 and later projection/delivery slices;
K. adversarial review before canonicalization.

## 14. Exit criteria

Step 5.5 is decision-ready only when the architecture can answer unambiguously:

1. what EPHEMERAL/SOFT/HARD mean and what they classify;
2. when established gameplay state is permitted to remain volatile;
3. which complete native dependency closure must become durable when a requirement fires;
4. whether/how unrelated accumulated SOFT joins a forced boundary;
5. exactly what `save` / `сохрани игру` promises;
6. how save differs from handoff and ordinary forced durability, if it does;
7. what execution/narration/input is blocked while required durability is unresolved;
8. what a confirmed publication failure means semantically;
9. how unpublished-SOFT exposure is bounded without relying on `time since any commit`;
10. what happens when no background execution opportunity exists;
11. how advisory host-capacity risk may affect policy without becoming authority;
12. why clean state causes no heartbeat write;
13. what later slices must implement without Step 5.5 preempting them.

The step may close only after owner decisions, candidate specification, adversarial review, resolution, canonical specification, roadmap update and fresh remote verification.

## 15. Task-brief self-review

Self-review result: **PASS FOR RESEARCH**.

The brief does not assume that current `SOFT/HARD/SAVE_ALL_DIRTY`, current `one hour`, global dirty flushing, narration blocking, or current wall-clock anchoring are correct. It explicitly permits simplification/removal of existing vocabulary and selective or broader closure if evidence supports it.