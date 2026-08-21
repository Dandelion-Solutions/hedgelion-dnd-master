# Step 5.3 — Temporal & Pending-Obligation Continuity — Canonical Specification

Status: **CANONICAL — STEP 5.3 ARCHITECTURE CLOSED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Owner decision:

> **A-NARROW / OWNER-CLAIM MATERIALIZATION**

Canonicalization basis:

- `2026-08-20-step-5-3-temporal-pending-continuity-pre-research-charter.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-task-brief.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-research-draft.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-analytical-challenge.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-decision-brief.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-candidate-spec.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-adversarial-review.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-resolution-gate.md`

This document is the current Step-5.3 authority and supersedes candidate/research wording where they differ.

---

# 1. Scope and central invariant

Step 5.3 defines logical continuity for gameplay-significant temporal and already accepted pending obligations across retry, suspension, cold hydration, handoff and process/context loss.

The architecture SHALL preserve native semantic ownership and SHALL reuse the Step-3 execution kernel for accepted mandatory execution.

Central invariant:

> A temporal occurrence is rebuildable while it remains only native-owner state plus timing/chronology context. Once the occurrence crosses into accepted mandatory execution, native owner state SHALL stop presenting that same occurrence as a distinct fresh materialization candidate, accepted execution SHALL have stable identity, and every still-significant consequence SHALL remain boundedly recoverable.

Exactly-once means one semantic consequence. Transport and execution attempts may retry.

---

# 2. Canonical ownership laws

## LAW 5.3-1 — Native temporal owner is source authority

Before accepted materialization, the native owner owns:

- whether the obligation exists;
- the current owner-local occurrence;
- armed/unarmed/terminal lifecycle;
- the governing `TemporalBinding` or boundary relation.

Temporal Agenda, temporal-source routing, checkpoint metadata, indexes, receipts and firing-key lookups are projections/evidence and SHALL NOT become temporal obligation authority.

## LAW 5.3-2 — Pending obligation is not a universal entity class

Effect expiration, Effect scheduled triggers, Resource recovery, LifeState recovery, Procedure boundary recovery, Step-3 mandatory descendants, pending Choice/Reaction and RNG continuity may share crash-consistency requirements without sharing one semantic owner or one lifecycle record.

Step 5.3 introduces no generic scheduler, job queue, `pending[]` ledger or standalone firing authority.

## LAW 5.3-3 — Temporal comparison is derived and three-valued

The conceptual result space is:

```text
NOT_DUE
DUE
INDETERMINATE
```

`INDETERMINATE` means available chronology/context cannot lawfully establish the required temporal relation.

Git/ref/commit order, record/ID order, Agenda/list order and host wall-clock time SHALL NOT resolve temporal ambiguity unless an owning chronology contract explicitly grants such evidence semantic meaning.

No generic durable `due=true` state is authorized.

## LAW 5.3-4 — Occurrence identity is distinct from timing value

Every independently materializable occurrence SHALL have stable identity that remains distinct from later rearming/repetition even when timing values are equal.

Canonical sources include:

- `BoundaryOccurrence.occurrence_key` for boundary occurrences;
- accepted Step-3 Event/Signal identity for event/signal occurrences;
- owner-local generation/arming identity for metric obligations;
- a derived key only when the owner contract proves timing-value uniqueness for the full relevant lifecycle.

`TemporalBinding` remains timing authority.

## LAW 5.3-5 — Accepted occurrence must become unavailable for fresh materialization

At the semantic edge where occurrence `G` is accepted, the native owner SHALL cease exposing `G` as a distinct fresh materialization candidate.

The owner may do this through one of three canonical lifecycle shapes defined in Section 4:

- direct finalization;
- safe immediate rearm;
- contingent owner claim.

## LAW 5.3-6 — Contingent owner claim is narrow

A long-lived owner-local `CLAIMED(G,F)` relation is required only when source-owner settlement remains contingent on accepted execution `F`.

The claim records only:

```text
source occurrence G
is committed to accepted execution F
```

It SHALL NOT copy execution payload/status, deadline, due result, chronology state, Procedure payload, RNG values or receipt bodies.

The source owner owns occurrence availability/lifecycle. Step-3 state owns execution progress.

## LAW 5.3-7 — Step 3 remains accepted execution authority

Mandatory child invocation, Resolution, Continuation, receipts and execution idempotency remain governed by the accepted Step-3 execution contract.

Step 5.3 does not introduce a parallel firing execution state machine.

## LAW 5.3-8 — Source/execution closure is an integrity invariant

Invalid durable states include:

- `CLAIMED(G,F)` with no compatible resolvable accepted execution `F`;
- accepted execution `F` while current source state still permits a distinct second materialization of the same `G`;
- two distinct accepted firing identities for one occurrence generation.

Recovery SHALL NOT guess which side is authoritative or invent missing execution.

Physical publication mechanics preventing split durable visibility belong to later Step-5 slices.

## LAW 5.3-9 — Bounded recovery reachability is continuous

A transition that changes recovery-root membership SHALL preserve continuous bounded discoverability of every still-gameplay-significant obligation at every acknowledged durable recovery closure.

An armed independently-due temporal owner may cease requiring armed-temporal routing only when its replacement final owner state and/or accepted execution root is recoverable through the applicable typed owning path.

Routing membership remains derivative retrieval evidence. Temporary duplicate retrieval references may be legal; an omission gap at an acknowledged recovery frontier is not.

## LAW 5.3-10 — Multiple due obligations do not imply total order

When several obligations are actionable at the same relevant coordinate/scope, use Step-3 ordering semantics:

- registered mechanical ordering;
- player/controller choice where granted by rules;
- proven commutative batching;
- typed adjudication/reconciliation when order is materially required.

Storage/ID ordering SHALL NOT create fictional precedence.

## LAW 5.3-11 — No background fictional advancement is invented

Cold hydration, process restart and elapsed real host time do not themselves advance fictional time or manufacture Procedure boundary occurrences.

A material boundary/firing arises from accepted causal gameplay execution and therefore uses the existing Step-3 causal/root execution identity.

If a future subsystem explicitly admits autonomous/background gameplay advancement, Step-3 root ownership must be reopened by a new architecture decision. Step 5.3 does not add a synthetic RuntimeCommand.

## LAW 5.3-12 — Accepted RNG continuity is experiment-scoped

Unrequested future randomness has no continuity obligation.

For every generated random result required by unfinished accepted execution:

- the value SHALL remain fixed across retry/recovery;
- the value SHALL be recoverably associated with the stable accepted experiment/invocation identity and interpretation inputs needed to use it;
- recovery SHALL NOT regenerate or remap the result by incidental traversal/list order.

A universal future PRNG frontier/stream is not required.

If a concrete future mechanic requires accepting experiment identity before generation, that reservation must be a typed experiment-specific continuity concept.

## LAW 5.3-13 — Accepted execution interpretation is pinned

Once firing/execution `F` is accepted, recovery SHALL resume `F` under its compatible accepted execution/catalog interpretation context.

A later current definition/catalog version may govern only later fresh occurrences after lawful settlement/rearm/migration. It SHALL NOT silently reinterpret an already accepted firing.

---

# 3. Obligation-family ownership disposition

| Family | Native source owner | Armed/current evidence | Accepted consequence | Source settlement |
|---|---|---|---|---|
| Effect intrinsic expiration | `world.effect` | active + `temporal_binding` + occurrence identity as required | direct transition and/or Step-3 descendants | terminal/updated Effect |
| Effect scheduled trigger | `world.effect` | `scheduled_trigger_state[key]` + occurrence identity | Step-3 firing/child when long-lived | immediate rearm or claim -> REARM/UNARM/TERMINAL |
| Resource delayed recovery | actor/asset ResourceState | `recovery_binding` + occurrence identity as required | normally direct deterministic transition | value/binding update |
| Stable LifeState recovery | `world.actor` LifeState progress | `recovery_binding` + occurrence identity as required | registered deterministic transition or Activity | LifeState/progress update |
| Procedure resource/boundary recovery | `runtime.procedure` | active Procedure + policy + stable boundary occurrence | deterministic Procedure transition or Step-3 child | Procedure-owned state update |
| Event/signal mandatory followup | source binding + causal execution | applicable binding at accepted occurrence | existing Step-3 firing/pending child | descendant settled/suspended |
| Pending Choice/Reaction | `runtime.continuation` | stable offer/response state | existing continuation generation | exactly one consume/advance |
| Generated accepted RNG | Resolution/Continuation execution state | stable experiment/invocation association | fixed value | deterministic continuation/commit |
| Reserved future experiment, if later justified | execution owner | explicit typed accepted reservation | stable experiment identity | generate once -> fixed result |

Story projection and host-delivery work remain owned by Steps 5.10 and 5.12 even if they later reuse similar idempotent patterns.

---

# 4. Canonical materialization shapes

All legal forms satisfy LAW 5.3-5.

## 4.1 Direct finalization

Use when source-owner settlement can be decided completely at the materializing edge.

```text
ARMED(G, B)
    -> final owner state
       + stable causal/occurrence/idempotency evidence
       + mandatory descendants materialized in same edge if required
```

A long-lived descendant does not itself force the source owner to remain `CLAIMED` when that descendant no longer controls source-owner settlement.

Examples include one-shot expiration/recovery or terminalization that atomically creates downstream mandatory consequences.

A stale retry carrying `G` must fail against the current owner occurrence/revision and/or resolve to already committed idempotency/receipt evidence rather than reapply the transition.

## 4.2 Safe immediate rearm

Use only when both conditions are proven by the mechanic:

1. **schedule independence** — the unresolved execution for `G` cannot unarm, terminate, reschedule or invalidate the existence/timing of `G+1`;
2. **overlap/order safety** — if `G+1` becomes actionable before execution `F(G)` settles, concurrent/pipelined existence is explicitly legal or registered mechanics provide an unambiguous serialization/ordering rule.

Then:

```text
ARMED(G, B)
    -> ARMED(G+1, B2)
       + accepted execution F(G)
```

`G+1` is a new occurrence even when `B2` equals `B` by value.

If either safety condition is unproven, use contingent owner claim.

## 4.3 Contingent owner claim

Default for long-lived outcome-dependent source settlement:

```text
ARMED(G, B)
    -> CLAIMED(G, F)
       + accepted Step-3 execution F

F settles
    -> REARM(G+1, B2)
       OR UNARM
       OR OWNER TERMINAL
```

When `F` outcome determines owner state, execution settlement and source `REARM|UNARM|TERMINAL` form one semantic completion closure.

The claim remains only until source-owner settlement is resolved.

---

# 5. Due evaluation and chronology insufficiency

An armed owner plus chronology/context may evaluate to `NOT_DUE`, `DUE` or `INDETERMINATE`.

`INDETERMINATE` rules:

1. it is not automatically integrity corruption;
2. unrelated gameplay may continue when correctness does not depend on the unresolved relation;
3. an operation that must cross/use the relation triggers bounded chronology reconciliation;
4. if lawful evidence still cannot establish the relation, execution returns typed chronology/order/adjudication-required outcome;
5. Step 5.9 owns final chronology persistence/reconciliation representation.

Temporal Agenda remains disposable and may be rebuilt from native armed sources.

---

# 6. Choice/Reaction and suspended descendant continuity

Pending Choice/Reaction is already accepted execution, not a temporal due candidate.

If source settlement depends on a child that suspends for Choice/Reaction:

```text
source = CLAIMED(G,F)
F/Continuation = pending stable offer
```

Cold recovery resumes the same execution/offer identity. Waiting for input does not reopen source occurrence `G`.

If the source was already safely finalized/rearmed under Section 4.1 or 4.2, no artificial claim is recreated merely because a descendant later suspends.

---

# 7. Crash/retry dispositions

| Point of loss/retry | Canonical recovery behavior |
|---|---|
| armed, not due | hydrate owner from bounded routing; rebuild candidate; execute nothing |
| chronology insufficient | keep armed; remain `INDETERMINATE`; reconcile only when material |
| due discovered but not accepted | retry comparison/selection from native owner state |
| crash before materialization semantic commit | no accepted partial state is visible; retry prior owner occurrence |
| claim visible, F missing | integrity/publication defect; do not invent/reopen |
| F visible, source permits second fresh `G` | integrity defect; do not rematerialize as normal work |
| claim + F visible, F not started | resume same `F` |
| F partially executed | resume Step-3 Resolution/Continuation with pinned accepted inputs/context |
| F suspended on Choice/Reaction | resume same continuation/offer; source claim remains if still settlement-contingent |
| F outcome exists but contingent source settlement is not coherently durable | invalid completion closure; later durability/publication protocol must prevent/classify |
| direct finalization committed | old `G` is no longer current; stale retry suppressed by owner generation/revision + idempotency evidence |
| immediate rearm committed | current owner occurrence is `G+1`; `F(G)` continues independently under proven safety constraints |
| periodic claim settles and rearms | new occurrence identity `G+1`; equal timing value does not collapse identity |
| terminal owner but stale temporal routing remains | owner terminality wins; routing is stale derivative and must be repaired |
| armed independently-due owner missing required temporal routing | Step-5.2 root-membership coherence defect; no world/history scan fallback |
| source leaves temporal routing before replacement execution root is recoverable | invalid acknowledged durability closure under LAW 5.3-9 |
| fixed accepted RNG required by unfinished execution is missing/unbound | integrity/continuity defect; do not regenerate silently |

---

# 8. Bounded cold recovery handoff

Cold recovery SHALL distinguish the current source/execution form without campaign-wide scans:

```text
A. ARMED owner occurrence
   -> enumerate through temporal-source routing
   -> rebuild due candidate

B. CLAIMED source occurrence
   -> boundedly resolve linked accepted execution F
   -> resume F

C. FINALIZED / REARMED source
   -> owner shows settled state
   -> any still-active descendants are recoverable through their Step-3 execution roots
```

Root/routing membership changes are correctness-critical derivatives of lifecycle transitions but are not semantic authority.

Exact physical root manifests, checkpoint placement and live/campaign routing are owned by Steps 5.6–5.8.

---

# 9. Cross-domain/live ownership

A-NARROW applies inside the source's current writable ownership domain.

A live-owned source is mutated/claimed/finalized in the live owning scope. Campaign base cannot concurrently mutate the same authority.

Step 5.3 requires semantic and recovery closure, not one hidden distributed transaction across independently writable domains.

Cross-scope consequences, transfers and rare multi-scope slow paths remain Step-5.8 responsibilities. No global firing ledger is authorized as a shortcut.

---

# 10. RNG continuity

Canonical classification:

```text
UNREQUESTED FUTURE RANDOMNESS
    no accepted experiment
    -> no replay guarantee

GENERATED / ACCEPTED RESULT
    unfinished accepted execution depends on it
    -> preserve experiment identity + fixed value + interpretation inputs

RESERVED-BUT-NOT-GENERATED EXPERIMENT
    only if a concrete mechanic establishes such accepted state
    -> preserve typed stable experiment reservation
```

Default architecture policy:

> Generate the random result when execution has actually established that the experiment is required, then make the raw result part of accepted continuity before suspension/retry can depend on it.

The current mandatory generic `runtime.continuation.future_rng_frontier` is not justified by this architecture and is recorded for retirement/narrowing during later machine realization unless a concrete reservation-before-generation mechanic appears.

No replacement universal RNG-frontier class is approved.

---

# 11. Compatibility and interpretation context

A firing accepted under one compatible runtime/catalog interpretation context SHALL finish under that accepted context even if current definitions later change.

Owner/catalog updates may affect later fresh occurrence generation after lawful settlement/rearm or explicit migration.

If the accepted interpretation context required to resume `F` is unavailable/incompatible, recovery SHALL surface a compatibility/integrity condition rather than silently execute `F` under current definitions.

---

# 12. Later Step-5 obligations

## 5.4 — Host lifecycle & session handoff

Define controlled handoff versus unexpected-loss RPO and when active source/execution continuity forces a publication attempt. Do not promise reconstruction of unpublished volatile state.

## 5.5 — SOFT/HARD/SAVE durability

Classify source/execution closure so a required durability boundary cannot knowingly acknowledge one side while losing the other.

## 5.6 — Campaign publication & crash consistency

Provide physical write/publication semantics that enforce source materialization/finalization + accepted execution + required root-membership closure before acknowledging a durable frontier.

## 5.7 — Checkpoint/recovery protocol

Provide bounded hydration of armed sources, claimed links and active execution roots without making checkpoint metadata authority.

## 5.8 — Multiplayer/live ownership

Preserve current writable authority and LAW 5.3-9 reachability across live scopes, compaction and ownership transfer; define explicit slow paths for true cross-scope consequences.

## 5.9 — Chronology persistence/reconciliation

Retain enough evidence for every still-live temporal relation and preserve lawful `INDETERMINATE` states where order/precision remains insufficient.

## 5.10 / 5.12

Story projection and host delivery may reuse idempotent transition patterns but must define their own owners/lifecycles and must not turn Step-5.3 claims into a generic job mechanism.

## 5.13

GC/retention SHALL preserve the only execution/receipt/experiment evidence needed while source claims, active descendants or duplicate-suppression dependencies remain live.

---

# 13. Machine-realization debt

Step 5.3 architecture closure does not imply immediate machine-schema implementation.

Later integrated implementation must align at least:

1. native temporal owner state that currently stores timing bindings but lacks occurrence generation/arming identity where required;
2. owner-local claim representation for outcome-dependent long-lived scheduled work;
3. Effect `scheduled_trigger_state` machine shape;
4. repeated Resource/LifeState recovery occurrence identity where equal binding values can recur;
5. Step-3 firing-key derivation for metric owner occurrences;
6. bounded root/routing handoff validation tests;
7. split-closure integrity tests;
8. RNG representation so fixed accepted results are stably associated with experiment/invocation identity;
9. retirement/narrowing of mandatory `Continuation.future_rng_frontier` and corresponding runtime prose/schema/tests;
10. pinned accepted interpretation-context recovery tests.

Concrete JSON field names and common-vs-family-specific schema factoring remain implementation/specification mechanics to derive after the architecture sequence closes.

---

# 14. Explicit non-goals

Step 5.3 does not choose:

- SOFT/HARD/SAVE cadence;
- Git tree/commit/ref publication protocol;
- checkpoint wire format;
- live-epoch CAS/compaction/transfer protocol;
- final chronology storage representation;
- Story projection job state;
- host-delivery acknowledgement state machine;
- retention/GC algorithm;
- physical LLM orchestration;
- broad machine migration in this architecture slice.

---

# 15. Step-5.3 closure result

Step 5.3 establishes:

```text
native armed occurrence
    -> derived NOT_DUE | DUE | INDETERMINATE

accepted occurrence G
    -> G no longer freshly materializable
    -> DIRECT FINALIZATION
       OR SAFE IMMEDIATE REARM
       OR CONTINGENT CLAIMED(G,F)
    -> existing Step-3 accepted execution identity/receipt/idempotency
    -> continuous bounded recovery reachability

unfinished accepted RNG
    -> stable experiment association + fixed generated result
```

No generic firing record, scheduler, durable due marker, authoritative Agenda, synthetic background RuntimeCommand, implicit total order or universal future RNG frontier is introduced.

Adversarial review: **PASSED WITH RESOLVED REFINEMENTS**.

Unresolved Step-5.3 architecture blockers: **NONE**.

Next architecture slice after roadmap/status update:

> **Step 5.4 — Host Lifecycle & Session Handoff — NOT STARTED**

Do not begin Step 5.4 as part of Step-5.3 closure verification.
