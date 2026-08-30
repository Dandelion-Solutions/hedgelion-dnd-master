# Step 5.3 — Temporal & Pending-Obligation Continuity — Research Draft

Status: **RESEARCH / DRAFT — NOT CANONICAL**

Date: 2026-08-20

Basis:

- `2026-08-20-step-5-3-temporal-pending-continuity-pre-research-charter.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-task-brief.md`
- current Step-5.2 canonical v2
- Step-3 canonical execution spec/final review
- current Step-2 temporal/resource/effect machine contracts
- current runtime chronology/randomness contracts

## 1. Executive research result

The current architecture already contains the principal exactly-once execution primitive needed by Step 5.3: the Step-3 `ExecutionSegment` can commit authoritative owner/runtime changes, stable mandatory child descriptors, receipts and idempotency evidence on one semantic execution edge.

Therefore the research does **not** find evidence for a new generic scheduler, pending-obligation ledger, or first-class firing record.

The remaining design problem is narrower:

> When an owner-local temporal obligation becomes mechanically actionable, what owner/execution state transition makes that occurrence irreducible exactly once, while allowing cold recovery to distinguish (a) still merely armed/due, (b) already materialized into execution, and (c) completed/rearmed/unarmed/terminal work?

The strongest candidate is an **owner-local materialization transition into existing Step-3 execution identity**. The transition must atomically couple the owner-side occurrence consumption/claim with stable firing/pending-child identity. The precise owner-side representation may vary by obligation family and should not be forced into one universal record.

A second major result is that temporal comparison must admit an **indeterminate / chronology-required** result. `due/not_due` cannot be the only conceptual result because HDM explicitly permits partial chronology and incomparable independent scopes.

A third result is that the current mandatory `Continuation.future_rng_frontier` is broader than the continuity guarantee Step 5.2 actually requires. The architecture needs stable continuity only for random experiments whose identity/result has entered accepted execution semantics; it does not require one generic future RNG sequence frontier.

---

# 2. Evidence classification

## FACT F1 — Temporal authority is owner-local

Current machine state stores temporal obligations on native owners:

- `world.effect.temporal_binding` for intrinsic Effect lifetime;
- `world.effect.scheduled_trigger_state[local_key]` for owner-local scheduled trigger state;
- actor ResourceState `recovery_binding` for delayed resource recovery;
- stable LifeState progress `recovery_binding` for delayed recovery;
- Procedure-linked boundary semantics through Procedure identity and `BoundaryOccurrence`.

Temporal routing/Agenda are not these authorities.

## FACT F2 — Step 5.2 v2 requires armed independently-due temporal owner enrollment

An armed owner that can become mechanically due independently remains in typed bounded temporal-source routing for the full armed lifetime. This eliminates the need for recovery to rediscover such owners by scanning world state.

The routing stores owner identity/retrieval evidence only; it does not store due state, deadline, firing generation or ordering.

## FACT F3 — Step 3 already defines stable occurrence/firing semantics

For committed event/boundary-triggered work, Step 3 defines:

```text
stable occurrence/Event identity
+ binding/local key
+ owner/application identity
    -> stable firing key
```

Retry cannot refire the same binding on the same occurrence.

`BoundaryOccurrence` already has a stable `occurrence_key`.

## FACT F4 — Step 3 already closes the Event -> lost-child crash window

If a committed segment creates mandatory post-commit work, the same segment must materialize sufficient stable child/firing identity atomically with the causal committed edge.

`ExecutionSegment` supports embedded `pending_child_invocations`; RuntimeCommand remains open while mandatory descendants remain unresolved.

## FACT F5 — Step 3 already defines an advancement barrier

When advancement reaches a mechanically relevant coordinate/boundary:

```text
freeze at coordinate
capture complete immediate due set
resolve or durably suspend mandatory same-coordinate work
only then advance beyond coordinate
```

Thus a durable state that is already beyond a known due coordinate but has no materialized required consequence is an integrity/publication defect, not a normal recovery state.

## FACT F6 — Chronology is intentionally partial

Independent scenes/events may remain unordered. Git order does not supply fictional order. Chronology may be `UNDEFINED`/insufficient until a material dependency requires reconciliation.

Therefore a temporal comparison can be semantically unresolved.

## FACT F7 — Scheduled Effect trigger state is only the next owner-local TemporalBinding

The current world Effect schema does not store an explicit firing generation or in-flight firing reference. Periodic declaration lives in the Effect definition; the owner state stores the current next due binding.

## FACT F8 — Resource/LifeState delayed recovery differs structurally from scheduled Effect Activity execution

Resource/LifeState recovery state is embedded directly in actor-owned state and often resolves as a deterministic owner mutation. It does not inherently require an Activity child or RuntimeCommand descendant.

Procedure boundary recovery similarly may be a deterministic Procedure owner response.

This weakens the case for one universal pending-child state machine.

## FACT F9 — Continuation currently requires `future_rng_frontier`

Current machine schema requires a nonempty string `future_rng_frontier`, while also preserving `fixed_rng_results`.

Step 5.2 v2 explicitly says only future RNG identity/state that is already semantically committed/reserved must survive; no global future stream is required.

## FACT F10 — runtime randomness prose is weaker than Step-3/5.2 continuity semantics

`GAME/CORE/RANDOMNESS.md` currently emphasizes current resolution trace retention. Canonical architecture requires unfinished execution to retain fixed generated RNG in native Resolution/Continuation continuity owners rather than relying solely on trace retention.

This is later implementation/prose alignment debt.

---

# 3. Constraints

## C1 — no second temporal owner

A due/firing representation may identify execution of an owner obligation; it may not become a copy of the temporal deadline/lifecycle authority.

## C2 — no generic scheduler/job subsystem by convenience

Different owner families may share occurrence/idempotency laws without sharing one record/lifecycle owner.

## C3 — normal cold recovery is bounded

Recovery must use Step-5.2 temporal routing + owner/native execution roots, not campaign/world/history scans.

## C4 — exactly-once is semantic, not delivery/transport exactly-once

The system may retry reads/writes/execution attempts. Stable identity/idempotency must make the semantic effect occur once.

## C5 — no implicit cross-domain temporal comparison

Two obligations in independent live/scene chronology domains need not be ordered simply because both are due in their own scopes.

## C6 — later slices own physical publication guarantees

Step 5.3 can require a semantic durability closure such as “owner transition + firing identity must become durable together” but does not define Git transaction mechanics.

---

# 4. Obligation family matrix

| Family | Native owner | Armed state | Due evidence | Materialized execution | Completion |
|---|---|---|---|---|---|
| Effect intrinsic expiration | `world.effect` | active + `temporal_binding` | binding vs chronology/boundary context | may be direct deterministic owner transition; child only if rule requires | owner terminal / binding replaced |
| Effect scheduled trigger | `world.effect` | `scheduled_trigger_state[key]` | next binding vs chronology | stable firing key + child Resolution/pending descriptor | child response atomically REARM / UNARM / OWNER TERMINAL |
| Actor/asset Resource delayed recovery | actor/asset ResourceState | `recovery_binding` | binding vs chronology | usually direct deterministic owner transition; Activity only if mechanic demands | value changed + binding cleared/replaced |
| Stable LifeState recovery | `world.actor` LifeState progress | `recovery_binding` | binding vs chronology | deterministic/registered LifeState transition or Activity if required | LifeState/progress updated |
| Procedure resource boundary recovery | `runtime.procedure` | resource policy + active Procedure | stable `BoundaryOccurrence` | deterministic Procedure owner transition | spent state reset/changed |
| Event/signal trigger mandatory followup | source binding + causal execution | binding applicable to occurrence | committed Event/Signal timing view | existing Step-3 firing/pending child | child settled or chain durably suspended |
| Pending Choice/Reaction | `runtime.continuation` | fixed pending response | not “due”; response awaited | continuation generation + offer identity | single consume / next generation/result |
| Fixed RNG | Resolution/Continuation | generated accepted value | not temporal | already part of execution continuity | consumed by deterministic recompute/commit |
| Reserved future RNG experiment | execution owner, if admitted | explicit accepted reservation | not temporal | stable experiment identity | generated once then fixed result |

Inference: “pending obligation” is a cross-cutting correctness category, **not one semantic owner class**.

---

# 5. Due-evaluation model

The minimum conceptual result space is:

```text
NOT_DUE
DUE
INDETERMINATE
```

`INDETERMINATE` means the owner binding is valid/armed but available chronology/context is insufficient to establish the required relation without inventing order/precision.

It is not automatically an integrity error.

Behavioral consequence:

- unrelated independent gameplay may continue if it does not need that relation;
- advancement/action that requires crossing or resolving the obligation’s temporal relation must obtain the minimum chronology evidence/reconciliation required or return a typed chronology/adjudication-required outcome;
- storage order, ID order, Agenda order and wall-clock runtime time may not convert INDETERMINATE into DUE/NOT_DUE.

Persisting a generic `due=true` marker is unnecessary and risky because due is a derived comparison over owner state + chronology context.

---

# 6. Candidate-to-materialized boundary

## 6.1 Rebuildable candidate

Before materialization, an obligation consists of:

```text
native owner identity
+ owner-local obligation identity/key
+ current armed TemporalBinding/boundary relation
+ required chronology/procedure context
```

Agenda may project that candidate. Losing Agenda is harmless.

## 6.2 Materialization

Once the engine accepts that a particular obligation occurrence must execute, the occurrence becomes irreducible execution continuity.

Required semantic closure:

```text
owner-side occurrence claim/consumption state
+ stable occurrence/firing identity
+ intended deterministic transition or pending child/Resolution identity
+ root/Procedure/causal linkage when applicable
+ idempotency evidence
```

must be committed as one semantic execution edge strongly enough that recovery cannot observe a promised durable state where:

- the old obligation is consumed but mandatory execution identity is absent; or
- mandatory execution is materialized while the owner still permits a distinct second materialization of the same occurrence.

Physical Git/transaction mechanics remain 5.6.

---

# 7. Competing materialization models

## Alternative A — owner-local claimed/in-flight occurrence + existing Step-3 execution identity

At materialization, atomically update the native owner so the occurrence is no longer a fresh selectable armed occurrence and create/reference the stable Step-3 execution identity.

Depending on the owner family:

```text
one-shot deterministic response
    -> consume binding + perform owner transition in same segment

scheduled Activity with deterministic next binding known immediately
    -> advance/rearm owner binding + materialize child

scheduled Activity whose child outcome determines rearm/unarm/terminal
    -> owner records minimal claimed/in-flight occurrence reference
       + materialize child
       -> child completion resolves owner to REARM/UNARM/TERMINAL
```

The “claimed/in-flight” representation is owner-local lifecycle state/reference, not a new firing record authority.

### Strengths

- owner state itself cannot be mistaken for a fresh occurrence;
- clean crash matrix;
- Step-3 pending child stays execution owner;
- avoids a global job table;
- bounded recovery loads owner + existing execution root;
- supports outcome-dependent periodic rearm.

### Costs

- temporal-owner schemas need a representable claimed/in-flight phase/reference where outcome-dependent execution exists;
- different owner families may express this differently;
- publication must preserve owner/materialization closure.

## Alternative B — leave owner unchanged while firing is in flight; suppress duplicate through firing-key lookup

At materialization, create pending child/Resolution with stable firing key but leave owner’s current binding unchanged until child completion.

Recovery sees the same DUE binding, derives the same firing key, checks whether execution already exists, and resumes/suppresses duplicate.

### Strengths

- smallest owner schema change;
- maximum reuse of Step-3 idempotency;
- no owner-side in-flight state.

### Costs / risk

- owner continues to semantically appear armed/due while work is already in flight;
- due evaluation must consult execution identity before deciding materialization eligibility;
- this creates a cross-owner negative lookup dependency for ordinary timing correctness;
- rules that inspect whether an owner remains armed while its scheduled response is unresolved become ambiguous;
- GC/retention of firing-key evidence becomes correctness-critical for preventing re-materialization;
- a periodic child that suspends for a Choice/Reaction can leave the old due binding visible for a long time.

Alternative B is feasible but less locally intelligible and makes idempotency evidence carry more semantic burden than intended.

## Alternative C — standalone firing/obligation record

Create a first-class durable occurrence/firing owner between temporal owner and child execution.

### Strengths

- explicit lifecycle and lookup;
- easy monitoring/debugging;
- one place for pending occurrence state.

### Costs / risk

- new semantic-ish owner boundary;
- risks duplicating owner timing/lifecycle and Step-3 pending child state;
- resembles the generic scheduler/job subsystem deliberately avoided in Steps 2/3/5.2;
- increases routing, retention, publication and migration complexity;
- no current use case requires independent permissions/lifetime beyond owner + execution chain.

Research assessment: **not justified**.

---

# 8. Preliminary recommendation: A-NARROW

Recommend Alternative A in a deliberately narrow form:

> A temporal occurrence crosses into irreversible execution through one native-owner + Step-3 execution materialization edge. The native owner must stop presenting that exact occurrence as a fresh selectable armed occurrence at the same semantic boundary that stable execution identity is accepted. No universal firing record is introduced.

This does **not** require one universal owner field named `in_flight`. The logical rule is shared; physical owner representation follows each native lifecycle.

For deterministic one-step recovery/expiration, the owner transition may complete immediately with no child.

For scheduled Activity whose outcome controls rearm/unarm/terminal state, the owner needs minimal local evidence that the current occurrence is claimed by a particular stable firing/child identity until that child settles.

This appears to preserve the strongest ownership/locality model while avoiding Alternative B’s permanent dependency on a negative global execution lookup.

---

# 9. Occurrence identity

## 9.1 Boundary occurrences

Use existing stable `BoundaryOccurrence.occurrence_key`.

A response firing key can derive from:

```text
owner/application identity
+ local response/binding key
+ BoundaryOccurrence.occurrence_key
```

## 9.2 Event/signal occurrences

Use the accepted Step-3 Event/Signal occurrence identity available at the selection boundary.

## 9.3 Metric deadline occurrences

The current TemporalBinding tuple alone is not proven sufficient as a permanent occurrence identity because an owner can potentially refresh/rearm to an equivalent coordinate/context tuple later.

Minimum robust architecture requirement:

> Every independently materializable owner-local metric obligation occurrence must have a stable owner-local occurrence generation/identity that remains distinguishable from later rearming, even when the resulting TemporalBinding values happen to be equal.

This identity may be represented as a compact owner-local generation/key; it is not a standalone record.

A firing key can then derive from:

```text
owner_id
+ obligation_local_key
+ obligation_generation
```

with current TemporalBinding remaining the timing authority.

If later machine review proves that a specific owner type’s binding tuple is structurally unique for its full active lifecycle, that owner may derive the key instead of storing an explicit generation. The architecture should not assume that globally.

---

# 10. Rearm / unarm / terminal semantics

For a scheduled periodic Activity:

```text
ARMED(generation G, binding B)
    -> DUE/accepted
    -> CLAIMED(G, firing_key F) + child materialized
    -> child settles
        -> REARM(generation G+1, new binding B2)
        OR UNARM
        OR OWNER TERMINAL
```

Important invariants:

1. `G` cannot produce two distinct firing identities.
2. `G+1` is a new occurrence even if B2 equals B numerically.
3. routing remains enrolled throughout any still-armed independently-due lifetime required by Step 5.2; whether claimed state remains in the temporal-source routing partition is a physical representation question for 5.7/5.8, but recovery must remain bounded through either temporal routing or linked active execution root.
4. owner terminality invalidates future rearm.
5. current definition changes after materialization do not erase historical accepted child identity/context.

For one-shot deterministic delayed recovery/expiration, CLAIMED may be unobservable because materialization and owner response can complete in one segment.

---

# 11. Crash-window matrix

| Crash point | Required recovery behavior |
|---|---|
| armed, not due | load owner from temporal routing; rebuild candidate; no work executes |
| chronology insufficient | preserve armed owner; remain INDETERMINATE; reconcile only when material |
| due derived, no materialization accepted | owner still ARMED; recovery may derive DUE again; safe because no irreversible selection occurred |
| materialization accepted | owner occurrence is claimed/consumed and stable execution identity exists in same semantic closure |
| child identity exists, child not started | resume/materialize same child identity once |
| child started before first commit | Resolution retry uses same causal/firing identity; no new firing |
| child suspended on Choice/Reaction | Continuation generation/offer survives; owner remains tied to same firing |
| child commits intermediate segment | receipts/Resolution state define resume; owner does not reselect occurrence |
| child settles and rearms | new owner generation/binding is authoritative; old firing cannot recur |
| child settles and unarms | no temporal source remains for that local obligation |
| owner terminal | stale routing repaired; no firing replay |
| stale duplicate materialization request | same occurrence generation/firing identity returns existing pending/completed result or typed idempotent conflict |
| owner consumed but firing missing | integrity/publication defect; do not invent whether work occurred |
| firing exists but owner allows a different fresh firing for same generation | integrity defect / machine invariant violation |

---

# 12. Same-coordinate multiple obligations

Two DUE obligations do not automatically require a total order.

Apply Step-3 ordering precedence:

1. registered timing/priority;
2. typed controller/player ordering choice;
3. proven commutative/order-independent batch;
4. otherwise `ORDER_ADJUDICATION_REQUIRED`.

Stable trace order or deterministic iteration may exist for observability only when it cannot change mechanics.

Independent obligations in separate chronology/live domains may each progress locally without a synthetic campaign-global ordering.

---

# 13. Procedure boundary continuity

Procedure boundaries already have stable `BoundaryOccurrence` identity and Procedure is independently recoverable across Command gaps.

Therefore Procedure-bound recovery/turn/round obligations do not require an open player RuntimeCommand to **exist** semantically.

However execution produced by a boundary still needs causal execution-root semantics when it materializes into a Resolution/segment.

Preliminary interpretation:

- if the boundary occurs as part of an advancing root execution, descendants inherit that root command;
- if a durable Procedure transition itself produces mandatory autonomous work between player Commands, the runtime needs an accepted internal root execution identity rather than fabricating a player command.

Current Step-3 machine `pending-child-invocation` requires `root_command_id`, so this is a potential cross-step gap. It may be resolved by proving all material Procedure boundary occurrences are always produced inside some existing RuntimeCommand advancement, or by admitting a typed internal command/root invocation path.

This question is material and requires analytical challenge before recommendation because it can affect the fundamental RuntimeCommand ownership boundary.

---

# 14. RNG continuity analysis

## 14.1 Classes

```text
UNREQUESTED FUTURE RANDOMNESS
    no continuity state

ACCEPTED/RESERVED RANDOM EXPERIMENT
    stable experiment identity + fixed distribution/rule inputs as required

GENERATED RESULT
    stable experiment identity + raw generated result

CONSUMED/COMMITTED RESULT
    result retained as long as retry/recompute semantics require it
```

## 14.2 No universal future sequence requirement

A fresh runtime does not need to reproduce all random numbers it hypothetically would have generated in the old process.

It must only preserve random experiments that have crossed an accepted semantic boundary.

## 14.3 `future_rng_frontier` assessment

Current mandatory string field is too abstract to prove what it owns:

- it does not identify experiment semantics;
- it suggests sequence/cursor authority that Step 5.2 does not require;
- no current architecture requires replaying one global PRNG stream;
- already generated values are separately stored in `fixed_rng_results`.

Preliminary recommendation:

> Retire generic mandatory `Continuation.future_rng_frontier` during later machine realization. Replace it only with explicit accepted/reserved experiment identity/state if a real execution case requires reservation before generation.

Simplest viable policy is stronger YAGNI:

> Do not reserve a future random result unless execution has actually reached the point where that experiment is mechanically required; then generate and commit the result on the continuity edge before any suspension that depends on it.

Under that policy most execution needs only fixed generated results, not future RNG reservation state.

Revisit only if a real mechanic requires accepting a future experiment identity before the actual draw can occur.

---

# 15. Strongest evidence against a generic firing/job record

A standalone firing record would be justified if any of these were required:

- independent lifetime after both source owner and execution root disappear;
- independent ACL/ownership;
- cross-owner payload not naturally owned by either source or child execution;
- queue semantics independent of gameplay execution;
- long-lived scheduling state whose source owner no longer exists but obligation remains semantically valid.

Current architecture provides no such case.

When source owner terminality should not cancel already-materialized work, the existing stable pending child/Resolution owns that accepted work. The source need not remain temporal authority for it.

Thus separate firing owner is currently YAGNI.

---

# 16. Open material questions

## Q1 — autonomous Procedure boundary root ownership

Can every material Procedure boundary occurrence that creates mandatory child work be proven to occur inside an existing RuntimeCommand execution chain?

If **yes**, current `root_command_id` model remains sufficient.

If **no**, the architecture needs an internal/non-player root execution identity path. That would be a fundamental Step-3 boundary extension and likely needs owner decision.

## Q2 — owner claimed/in-flight representation

Is it acceptable to require a native owner-local claimed occurrence reference for outcome-dependent scheduled work, or should HDM deliberately choose Alternative B and make firing-key lookup part of due-materialization eligibility?

Recommendation currently favors owner-local claim (A-NARROW), but this changes owner lifecycle representation and deserves challenge.

## Q3 — metric occurrence generation

Should explicit owner-local generation identity be universal for independently-due metric obligations, or only required where tuple reuse is possible?

Recommendation: architecture requires unique occurrence identity; physical explicit generation may be conditional if uniqueness is otherwise proven.

## Q4 — RNG reservation

Is any real project/rules case known that requires reserving future RNG identity/state before generation?

No current evidence found. Recommendation is no generic frontier and no reservation by default.

---

# 17. Research recommendation

Proceed to analytical challenge with **A-NARROW** as the lead candidate:

```text
owner-local temporal authority
    -> derived due candidate
    -> DUE / NOT_DUE / INDETERMINATE

when execution is accepted:
    one semantic materialization edge
        owner occurrence claim/consume
        + stable occurrence/firing identity
        + existing Step-3 direct transition or pending child/Resolution
        + idempotency/receipt evidence

then:
    direct one-shot completion
    OR child settles -> owner REARM / UNARM / TERMINAL
```

No generic firing record, no durable `due` marker, no authoritative Agenda, no global future RNG frontier.

The two issues most likely to survive challenge into a human decision gate are:

1. whether outcome-dependent scheduled work requires explicit owner-local claimed/in-flight state rather than pure firing-key lookup;
2. whether autonomous Procedure-boundary work can exist outside a player RuntimeCommand root and therefore requires a Step-3 root-identity extension.
