# Step 2 Retrospective Assurance — Slice A Task Charter: Actor Mechanical State

Status: **SOLUTION-BLIND TASK CHARTER — DO NOT TREAT AS SOLUTION**

Target branch: `feature/mechanical-runtime-hot-state`

Parent assurance plan: `2026-08-19-step-2-retrospective-architecture-assurance-plan.md`.

## 1. Purpose

Independently reconstruct the requirements for HDM actor mechanical state before judging the accepted Step-2 HP/LifeState/Resource design.

This charter deliberately asks what the subsystem must accomplish without assuming the current Step-2 representation is correct. Detailed Step-2 HP/LifeState/Resource specs are evidence only during the later coverage phase.

## 2. System context

HDM combines:

- natural-language/fictional adjudication by an LLM;
- deterministic mechanical authority in Python/runtime structures;
- structured world records and local HOT/SQLite operational state;
- repository-backed durable campaign state and later continuity recovery;
- D&D 2024/SRD-style mechanics plus future registered/custom mechanics;
- dialogue-driven execution rather than a continuous simulation loop.

Actor mechanical state must remain deterministic even when the surrounding fiction is informal, partially loaded, or interpreted by an LLM.

## 3. Problem statement

Define the minimum coherent authority/lifetime model for actor-local mechanical state required to represent health, lifecycle, expendable/recoverable capacities, and procedure-local budgets without duplicate truth or ruleset-specific hard-coding.

The design must answer not just where values are stored, but:

- what owns each mutable fact;
- what is derived versus authoritative;
- when ownership/lifetime begins and ends;
- how state participates in prospective calculations and atomic execution;
- how recovery, transformation, suspension, restart, and later multiplayer affect authority;
- how rules/content can observe or modify the state without bypassing deterministic validation.

## 4. Goals

The architecture must support, at minimum:

1. damage, healing, temporary protection, and maximum-health modification;
2. lifecycle states where current health and alive/dead/dying/stable semantics are not forced to be the same variable;
3. state-local lifecycle progress such as death-save-like counters or automatic recovery obligations;
4. reusable finite Resources owned by actors or assets;
5. procedure-local Resources such as action/reaction/movement-style budgets whose lifetime is an encounter/turn/procedure rather than the Actor record;
6. capacity derivation from definitions, features, effects, ruleset state, or context without copying the same derived value into multiple authorities;
7. deterministic spending/recovery and exact prevention of double-spend/double-recovery on retry;
8. interaction with Effects/Conditions and rules that modify health, capacity, availability, recovery, or lifecycle transitions;
9. prospective evaluation before atomic commit;
10. recoverability after interruption without inventing or losing committed state;
11. efficient bounded reads for ordinary resolution without campaign-wide scans;
12. extension to new registered resources/lifecycle policies without new arbitrary executable code.

## 5. Non-goals

This slice does not need to finalize:

- exact Step-3 command/transaction/event ordering beyond the minimum state contract it requires;
- full repository publication/checkpoint transport policy owned by Step 5;
- exhaustive SRD seed data owned by Step 6;
- lore/knowledge/disclosure semantics;
- tactical positioning or encounter initiative design except where procedure-local Resource lifetime depends on them;
- migration implementation details, though migration constraints must be identified.

## 6. Architectural invariants inherited from the project

These are constraints, not conclusions about the local representation:

- mechanical mutation must be deterministic and validated;
- LLM output cannot itself be authoritative for engine-resolvable mechanical facts;
- one semantic fact should have one mutable authority;
- derived/cache/index state must be reconstructable and cannot silently become second canon;
- runtime-only state may still be continuity-critical and therefore recoverable;
- arbitrary Python/SQL/query capabilities are not content-level mechanics;
- rules/content must use registered typed capabilities;
- state reads used in one calculation must not mix incompatible revisions;
- later persistence/multiplayer design must be able to detect stale/conflicting writes rather than rely on last-writer-wins guessing;
- the architecture should avoid hard-coding one D&D policy where a small registered policy/data boundary is sufficient;
- YAGNI applies: do not build a generic state-machine/resource framework beyond proven needs.

## 7. Required authority questions

The later assurance must answer explicitly:

### Health

- What facts are authoritative: current health, temporary health, base/max-health components, wounds/injury if any?
- Is maximum health stored, derived, or hybrid, and how are modifiers composed without circularity?
- Can health exceed normal maximum temporarily, and if so is that the same semantic as temporary HP or a max-health change?
- Which rules can change current health versus maximum health?
- What happens when maximum health changes below current health?
- What is the state after max-health restoration following a death/lifecycle change?

### Lifecycle

- Is lifecycle derived from health, independently authoritative, policy-driven, or some combination?
- Which transitions are automatic versus explicit rule procedures?
- What state-local progress exists only while in a lifecycle state?
- How are repeated entry/exit episodes distinguished?
- What prevents resurrection/revival from being accidentally represented as ordinary healing?
- How does lifecycle interact with Conditions such as unconscious/incapacitated without aliasing them?

### Resources

- What makes something a Resource rather than an ordinary actor field or lifecycle counter?
- What owns persistent ResourceState?
- What owns procedure-local ResourceState?
- Is mutable state represented as remaining/current, spent/consumed, or another model, and can two representations coexist safely?
- How is capacity derived and when is it re-evaluated?
- How are restricted/non-interchangeable budgets modeled?
- How does Resource identity distinguish definition, owner, instance/key/subtype, and procedure scope?
- What semantics are required for consume, restore amount, reset, recharge, and boundary-based recovery?
- What happens if capacity shrinks below current availability or below already-spent amount?

## 8. Lifecycle and episode questions

Test whether the design can represent cleanly:

- actor takes damage, enters an intermediate lifecycle state, progresses, stabilizes, recovers, and later repeats the episode;
- monster-like actor that bypasses an intermediate player-character death procedure;
- important NPC using a different lifecycle policy without changing fundamental entity kind;
- feature/effect preventing or replacing a prospective lifecycle transition;
- effect reducing maximum health while actor is damaged;
- effect expiration restoring maximum health without resurrecting a dead actor accidentally;
- persistent Resource whose capacity changes while partially spent;
- procedure-local budget surviving a suspended resolution or process restart;
- two Resources with similar presentation but non-interchangeable spending semantics;
- item/asset-owned charges used by an actor without moving ownership into the Actor.

## 9. Cross-subsystem dependencies to inspect

### Effects / Conditions

- health/capacity/lifecycle changes caused by Effects;
- Conditions derived from Effect applications versus lifecycle state;
- circular dependencies between health state and effect applicability;
- transformation replacing or layering actor statistics/resources;
- source/provenance-sensitive recovery or prevention.

### Temporal / Recovery

- timed recovery;
- rest/boundary recovery;
- state-local recovery obligations;
- expiry of effects that change capacity or health;
- pending recovery after suspension/environment loss.

### Execution / Step 3

- prospective health/lifecycle/resource plans;
- atomicity when one action changes several of them together;
- reaction before commit;
- idempotent retry;
- partial completion and committed costs;
- receipt/event representation sufficient to recover causal state.

### Durability / Step 5

- minimum revision/frontier information needed for conflict detection;
- continuity-critical procedure-local state;
- reconstruction without serialized derived caches;
- effect/resource/lifecycle references that must survive environment loss.

### Full seed / Step 6

- concrete D&D rules must fit without special actor fields for every class/feature;
- unusual rules may extend registered definitions/policies rather than rewrite core ownership.

## 10. Quality attributes / fitness criteria

### Correctness

- no semantic fact has two writable authorities;
- no retry duplicates spend, recovery, healing, damage, or lifecycle progress;
- a lifecycle transition observes one coherent prospective state;
- no ordinary health operation silently becomes resurrection/revival.

### Determinism

- the same pinned state + same validated command + same fixed RNG inputs yields the same state plan/result;
- LLM interpretation cannot bypass mechanical authority.

### Recovery

- every committed actor/resource/lifecycle fact survives according to its durability/continuity class;
- procedure-local state that matters to future mechanics can resume without guessing;
- derived capacities/indexes can be recomputed.

### Extensibility

- adding a new named Resource normally requires data/registered semantics, not a new actor field;
- adding a small new lifecycle policy does not require a new Actor entity kind;
- extensions cannot invent arbitrary mutation semantics.

### Performance

- ordinary resolution should hydrate/query only the actor/source/targets/procedure state and relevant Effects/Resources;
- no design should require campaign-wide Resource/Effect scans for actor-local calculations.

### Testability / observability

- authority and derived values can be inspected independently;
- prospective calculations and transition reasons are traceable;
- invalid lifetime/storage combinations are mechanically rejectable;
- recovery/retry cases can be reproduced with deterministic fixtures.

## 11. Failure scenarios the accepted design must survive

1. Maximum health changes in the same prospective segment that damage/healing occurs.
2. A reaction prevents a transition after a raw roll or cost has already been fixed.
3. Actor reaches zero health while a death-prevention Effect and an incapacitating Condition both participate.
4. A max-health reducing Effect expires while the actor is dead.
5. A Resource capacity modifier appears/disappears while some amount is already spent/available.
6. Procedure-local action/reaction state is checkpointed mid-procedure and restored elsewhere.
7. The same request is retried after local commit but before host acknowledgement.
8. Persistent item charges and actor resources are modified in one action.
9. A transformation changes definition-dependent capacities or lifecycle policy.
10. Two overlapping mechanics each believe they own automatic recovery at the same boundary.
11. A derived health threshold enables/disables the Effect that modifies the threshold's own source value.
12. A stale external write attempts to apply health/resource change against a newer revision.
13. A ruleset introduces a creature whose zero-health behavior differs from standard character behavior.
14. A recovery rule changes one resource but must not reset unrelated procedure-local budgets.
15. An LLM supplies a plausible but false current HP/resource/lifecycle fact in invocation context.

## 12. Known unknowns requiring investigation

- Whether the existing Step-2 model defines a complete rule for capacity shrink/growth relative to stored ResourceState.
- Whether definition-dependent transformation/migration of health/resources is sufficiently bounded now or safely deferred.
- Whether persistent Asset resources and Actor resources require identical mutable state shape in all proven cases.
- Whether state-local lifecycle progress needs explicit episode identity beyond lifecycle transition history.
- Whether any SRD 5.2.1 mechanics require source-specific health/lifecycle authority not represented by the generic model.
- Whether later multiplayer conflict detection requires finer-grained revisions than the current minimum Step-2 contract exposes.

These are questions to investigate, not findings.

## 13. Evidence to inspect after this charter is frozen

Project evidence:

- accepted Step-2 ownership, LifeState, Resource, Recovery, selector/query specs;
- Actor model and entity inventory;
- aligned schemas/catalogs/tests;
- final Step-2 critical review;
- Step-3 Task Brief/Research Draft only to expose downstream requirements, not to retroactively redefine Step 2.

External/domain evidence where a gap or assumption warrants it:

- official SRD/D&D rules for damage/healing/temp HP/death/unconscious/rest/resource-like mechanics;
- official or primary comparable-engine contracts for resource/lifecycle/effect handling where they illuminate a concrete question;
- database/transaction/recovery documentation only when required for a state-lifetime conclusion.

## 14. Exit criteria for Slice A

Slice A is assured only when:

1. every requirement/question above has a coverage status against the accepted Step-2 baseline;
2. every `PARTIAL`, `MISSING`, `DEFERRED_RISK`, and material `IMPLICIT` item has targeted investigation;
3. concrete multi-mechanic counterexamples have been attempted;
4. an independent adversarial review attacks both this charter and the resulting coverage analysis;
5. every finding is resolved, safely deferred, or escalated;
6. the result states `KEEP`, `AMEND`, or `REOPEN` with confidence and explicit reasons.
