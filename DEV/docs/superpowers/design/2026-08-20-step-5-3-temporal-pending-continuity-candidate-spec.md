# Step 5.3 — Temporal & Pending-Obligation Continuity — Candidate Specification

Status: **CANDIDATE SPECIFICATION — OWNER DECISION A-NARROW APPROVED — NOT YET CANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Inputs:

- `2026-08-20-step-5-3-temporal-pending-continuity-pre-research-charter.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-task-brief.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-research-draft.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-analytical-challenge.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-decision-brief.md`
- Step-5.2 canonical v2
- Step-3 canonical execution contract
- current Step-2 temporal/effect/resource/LifeState contracts

Owner decision:

> **A-NARROW / OWNER-CLAIM MATERIALIZATION is approved.**

This specification formalizes that decision. It does not implement or choose the physical Git/checkpoint/live-epoch protocol owned by later Step-5 slices.

---

# 1. Purpose

Step 5.3 defines the minimum logical continuity contract that prevents gameplay-significant temporal and pending obligations from being silently lost or semantically executed twice across suspension, retry, cold hydration, controlled handoff, or process/context failure.

The architecture SHALL preserve native semantic ownership. It SHALL NOT introduce a generic scheduler, generic pending-job ledger, durable Temporal Agenda, standalone firing authority, synthetic background RuntimeCommand, or universal future-RNG stream merely to make recovery convenient.

The central design distinction is:

```text
REBUILDABLE CANDIDATE
    owner-local obligation + timing/boundary state + chronology/context

IRREDUCIBLE ACCEPTED EXECUTION
    owner occurrence is no longer freely materializable
    + stable Step-3 execution identity exists
```

A crash before that boundary may re-derive the candidate. A crash after that boundary must resume or suppress retry against the same accepted execution identity.

---

# 2. Normative ownership laws

## LAW 5.3-1 — Native owner remains obligation authority

Before accepted execution materialization, the native owner owns whether an obligation exists, which occurrence is current, whether it is armed, and which `TemporalBinding` or boundary relation governs it.

Temporal Agenda, routing/index membership, checkpoint metadata, receipts and firing-key indexes are evidence/projections and SHALL NOT become the source of temporal obligation existence or due state.

## LAW 5.3-2 — Pending obligation is a correctness category, not a universal owner class

Effect expiration, Effect scheduled triggers, Resource recovery, LifeState recovery, Procedure boundary recovery, Step-3 mandatory descendants, pending Choice/Reaction and accepted RNG continuity may share no-lost/no-double requirements while retaining different semantic owners and lifecycle shapes.

No generic `pending[]`, `jobs[]`, scheduler singleton or first-class obligation record is introduced by Step 5.3.

## LAW 5.3-3 — Due evaluation is derived and three-valued

Temporal comparison SHALL conceptually admit:

```text
NOT_DUE
DUE
INDETERMINATE
```

`INDETERMINATE` means available chronology/context is insufficient to establish the required relation lawfully.

Git commit order, ref order, ID order, array order, Agenda order and host wall-clock time SHALL NOT convert `INDETERMINATE` into `DUE` or `NOT_DUE` unless a separate owning chronology contract explicitly makes such evidence semantically relevant.

A generic persisted `due=true` flag is not an authority and is not required.

## LAW 5.3-4 — Occurrence identity is distinct from timing value

Every independently materializable obligation occurrence SHALL have stable identity that distinguishes it from later rearming/repetition, even if two occurrences have equal `TemporalBinding` values.

Allowed sources include:

- existing `BoundaryOccurrence.occurrence_key` for boundary occurrences;
- accepted Step-3 Event/Signal occurrence identity for event/signal-triggered work;
- owner-local occurrence generation/arming key for metric obligations;
- a derived identity only where the owner contract proves timing-value uniqueness for the full relevant lifecycle.

`TemporalBinding` remains timing authority; occurrence identity does not replace it.

## LAW 5.3-5 — Owner-claim materialization

When a temporal occurrence is accepted as mandatory execution and that execution must outlive the materializing semantic edge, the same materialization closure SHALL:

1. make that exact owner-local occurrence unavailable for a distinct fresh materialization; and
2. create or reference the stable existing Step-3 firing/pending-child/Resolution identity that owns accepted execution.

The owner-side claim is minimal. It records only the relation that the specific occurrence has crossed into the specific accepted execution identity. It SHALL NOT copy child payload/status, deadline, due result, chronology state, Procedure payload, RNG values or receipt bodies.

## LAW 5.3-6 — No claim phase for one-edge completion

When an obligation can be fully resolved as a deterministic owner transition in the same semantic execution edge, the architecture SHALL allow direct transition:

```text
ARMED occurrence -> final owner state
```

without a visible long-lived `CLAIMED` phase.

The same edge must still carry stable occurrence/idempotency evidence sufficient to suppress semantic duplicate application on retry.

## LAW 5.3-7 — Accepted execution owner remains Step 3

Once materialized, the mandatory child/Resolution/Continuation remains owned by the existing Step-3 execution model.

The source-owner claim does not own execution progress. Step-3 execution state does not own whether the source occurrence was initially armed or which temporal binding created it.

## LAW 5.3-8 — Claim/execution closure is an integrity invariant

A durable state in which the owner marks occurrence `G` as claimed by firing/execution `F` but `F` is not resolvable from the compatible active execution closure is invalid.

A durable state in which accepted execution `F` exists but the source owner still permits a distinct fresh materialization of the same occurrence `G` is likewise invalid.

Recovery SHALL NOT guess which side is correct.

Physical atomicity/publication mechanics that prevent such split visibility are owned by Step 5.6 and related later slices.

## LAW 5.3-9 — No implicit global order among due obligations

Multiple obligations may be due concurrently without requiring a total order.

Use existing Step-3 precedence: registered mechanical ordering, controller/player choice where rules grant it, proven commutative batching, or typed adjudication/reconciliation when order is mechanically material.

Storage/ID ordering is observational only.

## LAW 5.3-10 — No autonomous gameplay advancement is invented

Under the current host/runtime model, cold hydration and elapsed real host time do not themselves create fictional advancement or Procedure boundary occurrences.

A material boundary/firing arises from accepted causal execution. That execution supplies the existing Step-3 root command/causal identity.

If a future architecture explicitly admits autonomous/background gameplay execution, the Step-3 root ownership contract must be reopened deliberately; Step 5.3 does not manufacture a synthetic internal RuntimeCommand.

## LAW 5.3-11 — Accepted RNG continuity is experiment-scoped

Randomness that has not yet entered accepted gameplay execution semantics need not be replayed identically after restart.

Once a random experiment is mechanically required and a result is generated/accepted, the raw result required by unfinished deterministic execution SHALL remain fixed in its native Resolution/Continuation continuity state.

The architecture does not require one generic future PRNG stream/frontier.

If a concrete future mechanic proves that experiment identity must be accepted before value generation, that reservation SHALL be a typed experiment-specific continuity concept rather than an untyped universal stream cursor.

---

# 3. Obligation-family disposition

| Family | Native owner | Before materialization | Accepted execution | Settlement |
|---|---|---|---|---|
| Effect intrinsic expiration | `world.effect` | active + `temporal_binding` | usually direct owner transition; child only if rule requires | terminal/remove/replace binding |
| Effect scheduled trigger | `world.effect` | `scheduled_trigger_state[local_key]` + occurrence identity | owner claim + Step-3 firing/child when long-lived | REARM / UNARM / OWNER TERMINAL |
| Resource delayed recovery | actor/asset ResourceState | `recovery_binding` + occurrence identity as required | normally deterministic owner transition | value/binding update |
| Stable LifeState recovery | `world.actor` LifeState progress | `recovery_binding` + occurrence identity as required | deterministic/registered transition or Activity if mechanic requires | LifeState/progress update |
| Procedure boundary recovery | `runtime.procedure` | policy + active Procedure + stable boundary occurrence | deterministic Procedure transition or Step-3 child | Procedure-owned state update |
| Event/signal mandatory followup | source binding + causal execution | applicable binding at accepted occurrence | existing Step-3 firing/pending child | descendant settled/suspended |
| Pending Choice/Reaction | `runtime.continuation` | already accepted response obligation | same continuation generation + stable offer identity | one consume then next state/generation |
| Generated RNG | Resolution/Continuation | n/a | fixed accepted value | deterministic continuation/commit |
| Reserved future experiment, if ever justified | execution owner | accepted typed reservation | stable experiment identity | generate once then preserve fixed result |

Story projection and host-delivery work may reuse crash-consistency patterns later, but their semantic state machines remain owned by Steps 5.10 and 5.12.

---

# 4. Materialization lifecycle

## 4.1 Rebuildable armed occurrence

An armed independently-due occurrence is identified by at least:

```text
native owner identity
+ owner-local obligation key
+ stable occurrence identity/generation
+ current TemporalBinding or boundary relation
+ required chronology/procedure context
```

Step-5.2 temporal-source routing keeps bounded recovery possible while the source is armed. Temporal Agenda may be rebuilt from these native sources.

## 4.2 Long-lived outcome-dependent execution

Canonical logical lifecycle:

```text
ARMED(G, B)
    -> comparison
       NOT_DUE | DUE | INDETERMINATE

DUE accepted
    -> CLAIMED(G, F)
       + Step-3 execution F materialized

F settles
    -> REARM(G+1, B2)
       OR UNARM
       OR OWNER TERMINAL
```

Properties:

1. `G` cannot yield two different accepted firing identities.
2. `G+1` is a distinct occurrence even if `B2 == B` by value.
3. definition/catalog changes after `F` is accepted cannot erase the accepted child identity or fixed accepted inputs required to finish it.
4. when child outcome determines owner state, child settlement and `REARM|UNARM|TERMINAL` form one semantic completion closure.

## 4.3 Outcome-independent immediate rearm

If the next scheduled occurrence exists independently of the child result, materialization MAY atomically advance owner state to `G+1/B2` while materializing child `F(G)`.

This optimization is legal only when the child cannot terminate, unarm, alter or otherwise invalidate that next occurrence according to the governing mechanic.

## 4.4 Direct deterministic response

For one-shot expiration/recovery or another deterministic owner-local response that completes immediately:

```text
ARMED(G, B)
    -> one semantic edge
       final owner mutation
       + stable occurrence/receipt/idempotency evidence
```

No long-lived claim relation is required.

---

# 5. Choice, Reaction and suspended execution

Pending Choice/Reaction is not a temporal `DUE` candidate. It is already accepted execution continuity owned by `runtime.continuation`.

A temporal firing whose child suspends for Choice/Reaction SHALL leave the source occurrence in the A-NARROW committed/claimed relation until the child resolves sufficiently to settle owner state.

Retry/hydration resumes the same continuation/offer identity. The source owner SHALL NOT reopen that occurrence merely because the child is waiting for human/controller input.

---

# 6. Crash/retry matrix

| Loss/retry point | Required disposition |
|---|---|
| armed, not due | hydrate owner; rebuild candidate; execute nothing |
| chronology insufficient | keep owner armed; result remains `INDETERMINATE`; reconcile only when relation becomes mechanically material |
| due discovered but not yet accepted/materialized | candidate remains derivable; retry comparison/selection |
| crash during materialization before semantic commit | no partial accepted state visible; retry from prior armed occurrence |
| owner claim durable but execution identity missing | integrity/publication defect; do not invent child or reopen occurrence |
| execution identity durable but owner permits second claim of same occurrence | integrity defect; do not treat as valid fresh candidate |
| claim + execution durable, child not started | resume same child `F` |
| child partially executed | resume Step-3 Resolution/Continuation using fixed accepted inputs/receipts |
| child suspended on Choice/Reaction | preserve claim and resume same offer/continuation |
| child outcome known but owner settlement not coherently durable | invalid completion closure; later publication/recovery protocol must prevent or classify this split |
| direct one-edge owner transition already committed | old occurrence is consumed; retry suppressed by stable occurrence/idempotency evidence |
| periodic trigger settled and rearmed | next occurrence is new `G+1`, regardless of equal timing values |
| stale duplicate attempts to materialize `G` | same occurrence identity/firing key suppresses duplicate semantic execution |
| owner terminal but stale routing entry remains | routing is stale derivative; owner terminality wins; routing repair is required |
| owner armed but required temporal routing membership missing | Step-5.2 root-membership coherence defect; bounded recovery cannot silently scan world state to compensate |

Exactly-once here means **one semantic effect**, not exactly-once transport. Reads, writes and attempts may retry.

---

# 7. Bounded cold recovery requirements

Cold recovery SHALL use compatible Step-5.2 roots and native owners rather than broad world/history scans.

For temporal/pending continuity, bounded recovery must be able to distinguish:

```text
A. owner occurrence still ARMED
   -> derive temporal candidate

B. owner occurrence CLAIMED by F
   -> resolve compatible execution root F and resume

C. occurrence already settled
   -> owner shows rearmed/unarmed/terminal final state
```

Routing membership itself is not due/firing authority.

The exact physical location of claimed owners and linked active execution roots across checkpoint/live/campaign structures remains owned by Steps 5.7 and 5.8.

---

# 8. Cross-domain/live ownership

A-NARROW is scoped by the current writable owner domain.

When a temporal source is live-owned, its occurrence mutation/claim is made in that current live ownership scope. The campaign representation cannot concurrently mutate the same authority.

Step 5.3 requires semantic closure between source occurrence availability and accepted execution identity but does not require an impossible hidden distributed transaction across independent writable domains.

Cross-scope consequences and any rare operation that truly spans separately writable authorities remain Step-5.8 design problems. A global firing ledger SHALL NOT be introduced as a shortcut.

---

# 9. Chronology insufficiency and liveness

`INDETERMINATE` is not automatically corruption and SHALL NOT globally freeze unrelated gameplay.

Rules:

1. unrelated operations whose correctness does not depend on the unresolved temporal relation may proceed;
2. an operation that must cross/use the relation triggers the minimum bounded chronology reconciliation required;
3. if lawful evidence still cannot establish the relation, execution returns a typed chronology/order/adjudication-required result rather than inventing order;
4. Step 5.9 owns persistence and reconciliation representation for chronology evidence.

---

# 10. RNG continuity disposition

Classify random state as follows:

```text
UNREQUESTED FUTURE RANDOMNESS
    no accepted gameplay commitment
    -> no continuity requirement

GENERATED / ACCEPTED RESULT
    experiment required and raw result exists
    -> preserve fixed result in native execution continuity

RESERVED-BUT-NOT-GENERATED EXPERIMENT
    only if a concrete mechanic truly establishes this state
    -> preserve stable typed experiment identity/inputs
```

Default policy is to generate randomness only when execution has established that the experiment is required, then commit the raw value before any suspension/retry can depend on it.

The current mandatory generic `Continuation.future_rng_frontier` is therefore **machine-realization debt** and SHOULD be retired when Step-5 implementation/schema alignment occurs, unless a concrete reservation-before-generation mechanic is demonstrated.

No replacement generic RNG-frontier class is authorized by this specification.

---

# 11. Integrity outcomes

Step 5.3 does not choose the final recovery-status vocabulary, but later recovery protocols SHALL distinguish normal resumable states from contradictory closure states.

At minimum, the following are not normal candidates for silent repair:

- claimed occurrence with no resolvable accepted execution identity;
- accepted execution whose source owner permits a different fresh materialization of the same occurrence;
- durable chronology advanced beyond a mechanically mandatory boundary with neither completed consequence nor resumable accepted execution;
- duplicate accepted firing identities for one occurrence generation;
- accepted generated RNG required by unfinished execution but missing from all native execution continuity sources.

Recovery SHALL report/suspect integrity rather than inventing which event occurred.

---

# 12. Later-slice requirements

## Step 5.4 — Host lifecycle & handoff

Must define when controlled destruction of runtime context forces a durability attempt for active claimed executions and what unexpected-loss RPO is promised. It must not pretend unpublished volatile claims survived.

## Step 5.5 — SOFT/HARD/SAVE semantics

Must classify owner claim + accepted mandatory execution closure so that a durability boundary cannot knowingly publish one side without the other.

## Step 5.6 — Campaign publication/crash consistency

Must provide a physical publication protocol in which required source-owner materialization state and accepted execution identity become durably coherent, or failures are detected before the system claims a completed durability frontier.

## Step 5.7 — Checkpoint/recovery protocol

Must support bounded discovery/hydration of armed sources and claimed-to-execution links without making checkpoint metadata temporal/execution authority.

## Step 5.8 — Multiplayer/live ownership

Must preserve A-NARROW inside the source's current writable scope, prevent duplicate writable authority, and define cross-scope slow paths without a global firing ledger.

## Step 5.9 — Chronology persistence

Must retain enough chronology evidence to lawfully resolve every still-live temporal relation and must preserve `INDETERMINATE` where evidence is insufficient.

## Steps 5.10 / 5.12

Story projection and host-delivery work may adopt analogous idempotent materialization patterns, but SHALL define their own semantic owners and SHALL NOT reuse Step-5.3 temporal claims as a generic job mechanism.

## Step 5.13

GC/retention must not delete the only execution/receipt/identity evidence needed while an owner occurrence remains claimed or while duplicate suppression still depends on that accepted execution identity.

---

# 13. Machine-realization obligations

Architecture closure does not imply immediate schema/runtime implementation.

The integrated implementation program must later align at least:

1. temporal owner machine state that currently stores binding values but no explicit occurrence generation/claim relation where required;
2. Effect scheduled trigger state for outcome-dependent long-lived firings;
3. Resource/LifeState representations where repeated equal timing values can occur and stable occurrence identity is needed;
4. Step-3 firing-key derivation to consume stable owner occurrence identity for metric obligations;
5. continuation RNG schema/prose, including removal or narrowing of mandatory `future_rng_frontier`;
6. integrity/recovery tests for owner-claim/execution split states;
7. cold-recovery routing tests proving no world/history scan is needed.

The exact JSON field names and common-vs-family-specific schema factoring are implementation/specification mechanics to derive from this canonical semantic contract after the remaining architecture sequence closes.

---

# 14. Explicit non-goals

Step 5.3 does not define:

- publication cadence or SOFT/HARD policy;
- Git tree/commit/ref transaction mechanics;
- checkpoint wire format;
- live-epoch CAS/compaction protocol;
- final chronology storage/reconciliation algorithm;
- Story projector job state;
- host-delivery acknowledgement state machine;
- retention/GC policy;
- physical model-call orchestration;
- broad machine schema migration in this architecture slice.

---

# 15. Candidate exit checklist

The candidate is ready for adversarial review only if all are true:

- [x] each admitted obligation family retains one semantic owner;
- [x] due comparison permits chronology insufficiency;
- [x] occurrence identity is separated from timing value;
- [x] A-NARROW owner decision is expressed without a generic firing record;
- [x] direct one-edge transitions avoid unnecessary claimed state;
- [x] long-lived child execution has owner claim + Step-3 execution closure;
- [x] every major crash window has a no-lost/no-double disposition;
- [x] pending Choice/Reaction remains Step-3 continuation state;
- [x] RNG continuity is narrowed to accepted experiments/results;
- [x] cross-domain ownership is not replaced by a hidden transaction/global ledger;
- [x] physical durability/publication/checkpoint/live/chronology decisions remain with later slices;
- [x] current machine gaps are recorded as later realization obligations rather than silently implemented.

Next gate: **independent adversarial review of this candidate before canonicalization.**
