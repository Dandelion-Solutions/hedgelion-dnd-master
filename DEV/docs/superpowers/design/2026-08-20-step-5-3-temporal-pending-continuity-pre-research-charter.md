# Step 5.3 — Temporal & Pending-Obligation Continuity — Pre-Research Charter

Status: **PRE-RESEARCH FRAMING — ARCHITECTURAL**

Date: 2026-08-20

## 1. Research mandate

Investigate the minimum coherent architecture required to preserve gameplay-significant temporal and pending obligations across interruption, crash, cold hydration and retry without creating a second scheduler, generic job system, replay authority or hidden total order.

Do not assume that existing words such as `due`, `pending`, `scheduled`, `trigger`, `child`, `future_rng_frontier`, `Agenda`, `firing`, `boundary`, or `recovery` already identify the correct abstraction boundaries.

Reclassify each relevant concept from current native ownership contracts and ask what exact state transition must become durable, what may remain derived, and which identity/evidence prevents both loss and duplicate execution.

## 2. Fixed inherited constraints

The investigation must preserve unless a new owner-level contradiction forces escalation:

- Step 5.1 B-NARROW domain typing and no implicit cross-domain order;
- Step 5.2 v2 native-owner preservation, pinned hydration and bounded typed recovery routing;
- Step 5.2 v2 LAW 5.2-13: every armed independently-due native temporal source remains enrolled throughout its armed lifetime;
- Temporal Agenda is rebuildable projection, never temporal authority;
- temporal deadlines, due state, ordering, selected firing and lifecycle remain native owner / chronology / execution semantics, not routing metadata;
- Step 3 stable pending-child/firing identity after mandatory work crosses the execution-materialization boundary;
- Continuation owns one suspended Resolution generation and fixed Choice/Reaction semantics but does not copy Procedure state or derived caches;
- Procedure owns procedure-local ResourceState and may remain active across gaps between Commands;
- already generated/accepted RNG needed by unfinished execution must survive; future RNG not yet semantically reserved need not belong to one global stream;
- Git/ref/commit order must not become fictional chronology;
- no generic `pending[]`, `jobs[]`, scheduler singleton or new universal obligation owner without a genuine architecture decision;
- no broad campaign/world/history scan is allowed on normal cold recovery.

## 3. Framing challenges

Before accepting any candidate design, actively test these possible framing errors.

### 3.1 Do not assume one obligation state machine fits everything

Effect scheduled triggers, metric expiration, delayed Resource/LifeState recovery, Procedure boundaries, pending reaction/choice, mandatory post-commit child work and future Story/disclosure work may share crash-consistency patterns without sharing one semantic lifecycle.

A reusable transition vocabulary must be justified by real common semantics rather than convenience.

### 3.2 Do not assume `due` is always a boolean

Chronology evidence can be insufficient or incomparable. The design must permit at least the possibility that a candidate is not yet decidably `due` or `not_due` without fabricating chronology.

### 3.3 Do not assume due selection itself must be persisted

Determine exactly where persistence becomes irreducible. A due candidate may remain derivable until the architecture accepts a specific firing/child identity, but there must be no crash window that loses a mandatory occurrence or permits double materialization.

### 3.4 Do not assume owner mutation and child materialization are separate writes

The correct atomic semantic boundary may require one transition that simultaneously records owner-side firing consumption/rearm state and stable mandatory execution identity. Test this rather than presupposing a two-phase scheduler protocol.

### 3.5 Do not assume every armed owner must generate work immediately when due

Rules may require Procedure boundaries, chronology reconciliation, target/context validation, choice/reaction handling or another deterministic prerequisite before executable child work exists. Separate candidate detection from accepted execution semantics.

### 3.6 Do not let recovery dictate live runtime semantics

The same native transition should be correct during uninterrupted execution and after hydration. Avoid a special crash-only replay subsystem whose semantics diverge from the normal execution kernel.

### 3.7 Do not treat idempotency as semantic authority

Stable keys/receipts may reject duplicate materialization or execution; they do not decide whether an obligation exists, is due, or is satisfied.

### 3.8 Do not let current machine fields predetermine the answer

In particular, `Continuation.future_rng_frontier` is evidence of an earlier representation choice, not proof that one global or per-Continuation RNG frontier is required. Retain, narrow, replace or retire it based on accepted execution semantics.

## 4. Required owner-by-owner analysis

For every admitted obligation source or pending execution form, establish:

```text
semantic owner
native lifecycle
arming condition
independent-due capability
required chronology/context evidence
due evaluation result space
stable occurrence/firing identity, if any
materialization boundary
owner mutation at materialization
pending child / Resolution relationship
idempotency evidence
completion / rearm / terminal semantics
crash windows before and after each boundary
cold-recovery behavior
scope/domain of persistence
```

Minimum source families to inspect:

- Effect intrinsic duration/expiration;
- Effect owner-local scheduled trigger state;
- Resource delayed recovery;
- LifeState temporal recovery;
- Procedure/turn/round/rest/dawn boundary obligations;
- mandatory post-commit pending child descriptors;
- suspended Resolution/Continuation;
- pending Choice/Reaction;
- accepted/reserved RNG state;
- any existing global/semantic consequence mechanism that still has an active owner;
- live-owned variants of the above where ownership scope matters.

Story projection and host-delivery work may be examined only to identify generic crash-pattern constraints; their semantic state machines remain owned by Steps 5.10/5.12.

## 5. Core research questions

1. What exact transition separates a rebuildable due candidate from irreducible accepted mandatory execution?
2. Can one owner-local atomic transition both consume/select an obligation occurrence and create its stable pending execution identity, avoiding an event-to-lost-child window?
3. What stable identity is minimally required for metric deadlines, semantic/procedure boundaries and rearming periodic triggers?
4. How are `due`, `not_due`, and temporally `indeterminate` represented or handled without letting Git order decide fiction?
5. When an obligation is discovered due after cold hydration, what evidence proves whether it was already materialized before the crash?
6. Which pending children belong to RuntimeCommand/ExecutionSegment continuity versus remain purely owner-local armed state?
7. How do Procedure boundary occurrences interact with child identity and Procedure lifetime across command gaps?
8. What exact RNG state must persist when randomness has been generated, accepted, or reserved but dependent execution has not completed?
9. Does `Continuation.future_rng_frontier` express a necessary concept, or is narrower accepted/reserved experiment identity sufficient?
10. Which apparent pending mechanisms are actually projections/caches and should be removed from the continuity model?
11. Which no-lost/no-double guarantees can be derived from existing Step-3 ExecutionSegment/idempotency semantics without adding new classes?
12. What obligations can safely be handled later by 5.4–5.9 without under-specifying 5.3?

## 6. Required counterexamples / crash matrix

The research must explain at least these cases:

1. crash while an armed timer is not yet due;
2. crash after it becomes due but before any firing identity is accepted;
3. crash after firing identity is accepted but before child Resolution starts;
4. crash after child starts but before first commit;
5. crash after child commits but before owner rearm/unarm is durably visible;
6. periodic trigger that must rearm;
7. one-shot expiration/removal;
8. two armed independent owners become due together with no required fictional order;
9. chronology evidence cannot yet compare a deadline with current local scene progress;
10. Procedure boundary occurs while no RuntimeCommand is open;
11. reaction/choice remains pending across restart;
12. RNG result already generated before suspension;
13. future RNG experiment reserved but result not yet generated;
14. stale duplicate retry attempts to materialize the same firing;
15. owner is terminal/removed but stale temporal routing still lists it;
16. owner is armed but routing enrollment is missing;
17. active live epoch owns the temporal source while campaign base contains older state;
18. mandatory child exists while current trigger definition has since changed;
19. scheduled source and pending child are both discoverable after restart;
20. independent due work exists in two live scopes without a common chronology order.

## 7. Quality attributes / fitness criteria

A candidate architecture is acceptable only if it provides:

- deterministic owner semantics;
- no silent loss of promised mandatory work;
- no duplicate semantic execution after retry/restart;
- no new temporal authority outside native owners/chronology;
- bounded cold reconstruction;
- local/partitionable write scope compatible with future multiplayer design;
- crash reasoning at every materialization boundary;
- idempotent recovery from already-materialized work;
- explicit handling of chronology insufficiency rather than invented order;
- exact preservation of already accepted RNG where required;
- YAGNI: no generic scheduler/job framework unless unavoidable;
- testability through owner lifecycle and crash-window cases.

## 8. Scope boundaries

Step 5.3 may define logical continuity semantics needed by later persistence slices, but it must not pre-design:

- when SOFT/HARD forces publication (5.5);
- exact Git transaction/write protocol (5.6);
- checkpoint/root physical wire format or hydration algorithm (5.7);
- live epoch open/close/compaction/CAS protocol (5.8);
- final chronology persistence representation or reconciliation algorithm (5.9);
- Story projection job semantics (5.10);
- host delivery acknowledgement state machine (5.12);
- retention/GC policy (5.13).

It may state requirements those later slices must satisfy.

## 9. Negative outcomes are valid

Research is allowed to conclude, for example:

- no common pending-obligation state machine is needed;
- no persisted `due` marker is needed;
- no new firing record class is needed because Step-3 pending-child identity is sufficient;
- an existing field is redundant and should be retired;
- some obligation family is not independently due and needs no temporal routing;
- exact future RNG sequence continuity is unnecessary beyond accepted/reserved experiments;
- a proposed atomic boundary is impossible without a later publication constraint and must be expressed only as a semantic closure requirement.

## 10. Prompt self-review

Before substantive research, verify that this charter does not:

- smuggle in a scheduler or job table;
- assume due is scalar/boolean/total-orderable;
- equate storage order with chronology;
- make Temporal Agenda authoritative;
- make routing authoritative;
- duplicate owner payload in recovery evidence;
- assume pending-child materialization representation before inspecting Step 3;
- force all obligation families into one lifecycle;
- silently decide 5.5–5.9 physical protocols;
- preserve `future_rng_frontier` merely because it exists;
- ignore live-scope ownership;
- ignore Procedure lifetime between Commands;
- ignore crash after selection but before execution;
- ignore double materialization after retry.

Self-review result: **PASS FOR RESEARCH**. The charter intentionally treats the central materialization boundary and RNG representation as hypotheses to derive, not predetermined solutions.
