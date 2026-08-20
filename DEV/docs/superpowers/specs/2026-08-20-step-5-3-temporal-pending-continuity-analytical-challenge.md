# Step 5.3 — Temporal & Pending-Obligation Continuity — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NOT CANONICAL**

Date: 2026-08-20

Challenges:

- `2026-08-20-step-5-3-temporal-pending-continuity-research-draft.md`
- preliminary recommendation **A-NARROW**

## 1. Candidate under challenge

The research draft recommends:

```text
native temporal owner
    -> derived temporal comparison
       NOT_DUE | DUE | INDETERMINATE

DUE accepted for execution
    -> one semantic materialization edge
       owner-local occurrence claim/consumption
       + stable occurrence/firing identity
       + existing Step-3 transition / pending child / Resolution
       + idempotency/receipt evidence

outcome-dependent scheduled child
    -> owner retains only minimal claim to that firing
    -> child settles
       -> REARM | UNARM | OWNER TERMINAL
```

No generic firing record, scheduler, durable due marker or universal future RNG frontier.

---

# 2. Strongest counterargument: owner-local claim is unnecessary duplication

Alternative B argues that Step 3 already has a stable firing key and active root execution closure. Therefore the native owner can remain unchanged at the old due binding while the child is in flight:

```text
owner remains ARMED/DUE
pending child exists under firing key F
recovery derives F again
lookup F -> existing child
resume child, do not rematerialize
child completion atomically rearms/unarms/terminates owner
```

This avoids a new owner lifecycle phase/field and appears more YAGNI.

### Why this is a serious objection

A claim marker that merely repeats `firing_key F` can look like duplicate execution evidence already stored by RuntimeCommand/ExecutionSegment/Resolution.

If the engine is already required to perform idempotency lookup before execution, adding another owner-side reference may seem redundant.

### Response

Alternative B can be made correct, but only by adding a new **negative eligibility dependency** to every due-materialization attempt:

> an owner that still appears DUE is not actually eligible for materialization until the engine proves that no active/retained execution identity already owns the derived firing key.

That proof is no longer owner-local.

Consequences:

1. Due projection cannot distinguish a fresh due occurrence from one already executing by reading owner + chronology.
2. Every retry/rebuild needs bounded cross-root firing-key lookup before selection.
3. The retention lifetime of completed/materialized firing evidence becomes coupled to how long the owner can still expose the old binding.
4. A long suspended Choice/Reaction leaves the owner indefinitely presenting the same due obligation as if unclaimed.
5. Same-owner timing rules may need to know whether an occurrence is still freely armed or already committed to execution; Alternative B can answer only by joining execution state.

The claim is therefore not a duplicate of child payload. Its semantic role is narrower:

> **the native owner records that this exact owner-local occurrence is no longer available for fresh materialization.**

The execution root separately owns what accepted work must execute.

This is analogous to a local state-machine transition, not a second scheduler record.

Challenge result: **A-NARROW survives**, but the claim must be minimal and must not copy child payload, deadline, due result or execution status.

---

# 3. Counterargument: claim creates a second authority over whether work exists

If owner says `claimed F` and RuntimeCommand does not contain F, which wins? Could this create split authority?

### Resolution

The pair is a cross-owner integrity invariant, not two authorities for the same state:

- source owner owns **availability/lifecycle of the temporal occurrence**;
- Step-3 execution owner owns **accepted execution closure**.

A durable claim without corresponding execution identity is invalid materialization closure and blocks/suspects recovery.

An execution firing identity whose source owner still allows a distinct second claim of the same generation is likewise invalid.

Neither side may silently repair by guessing.

This is the same pattern already accepted for Event + mandatory child closure in Step 3.

Challenge result: **acceptable if ownership wording is explicit**.

---

# 4. Counterargument: one-step owner responses do not need CLAIMED

Resource delayed recovery and Effect expiration can often be applied directly in one deterministic owner transition. Adding a universal ARMED/CLAIMED wrapper would over-generalize.

### Resolution

Agree. A-NARROW must not require a visible CLAIMED phase when materialization and completion are the same segment.

Logical rule:

```text
if occurrence can complete atomically now
    ARMED -> final owner state
    with stable occurrence/idempotency evidence on same execution edge

if accepted mandatory work must outlive the materializing segment
    ARMED -> minimal CLAIMED/IN_FLIGHT reference
    + pending execution identity
```

Thus the claim phase is conditional, not universal.

Challenge result: **candidate narrowed**.

---

# 5. Counterargument: periodic rearm should happen immediately at materialization

For simple fixed-period triggers, when firing G is materialized the next binding G+1 can be computed immediately. Why retain a claim until child completion?

### Analysis

Immediate rearm is safe only when the next obligation exists independently of the child outcome and rules do not allow the child to terminate/unarm/alter the schedule.

For a periodic disease save or similar mechanic, child result may determine whether the effect ends, changes cadence, or schedules another save. Pre-rearming would create a future obligation before the deciding rule outcome exists.

Therefore:

- deterministic outcome-independent schedule: materialization MAY atomically advance to G+1 and create child G;
- outcome-dependent schedule: must retain G as claimed until child settlement chooses REARM/UNARM/TERMINAL.

The architecture should permit both without inventing one universal timing policy.

Challenge result: **A-NARROW retained with two legal rearm forms**.

---

# 6. Counterargument: TemporalBinding tuple can serve as occurrence identity

Adding owner-local generation may be unnecessary because `(context, anchor, deadline, unit)` already identifies a metric deadline.

### Failure case

An owner may legitimately return to the same coordinate tuple after refresh, reapplication, rollback-compatible migration, repeated semantic cycle, or content-specific cadence reset. Identity-by-value would then treat a later occurrence as a retry of an earlier occurrence.

Payload equality is already rejected as event identity in Step 3. The same principle applies here.

### Resolution

Architecture requires stable **occurrence identity distinct from timing value**.

Representation does not have to be a universal integer field. It may be:

- explicit owner-local generation;
- stable arming/occurrence key assigned by the owner transition;
- an existing stable BoundaryOccurrence key for boundary-based obligations.

A derived binding fingerprint is sufficient only when the owner contract proves value uniqueness for the relevant lifecycle.

Challenge result: **explicit identity requirement survives**.

---

# 7. Counterargument: `INDETERMINATE` harms liveness

A three-way due comparison can leave work stuck forever if chronology remains unresolved.

### Response

Forcing DUE/NOT_DUE would be worse: it invents fictional order/precision.

Liveness rule must be scoped:

- unrelated operations continue while the relation is immaterial;
- an operation that must cross/use the temporal relation triggers bounded chronology reconciliation;
- if reconciliation cannot establish a lawful relation, execution returns typed chronology/order adjudication required rather than silently choosing;
- 5.9 owns persistence/algorithm for chronology evidence, not 5.3.

`INDETERMINATE` therefore delays only work whose correctness actually depends on missing chronology.

Challenge result: **three-way model survives**.

---

# 8. Counterargument: all simultaneous due work should receive deterministic ID order

A deterministic ID sort would make retry simple.

### Rejection

Determinism is not permission to create game semantics from storage/identity ordering.

Step 3 already defines correct precedence: registered order, player/controller choice, proven commutative batch, else adjudication required.

Two independent due obligations may remain unordered and execute independently when mechanics commute.

Challenge result: **ID/list/Git order remains observational only**.

---

# 9. Critical challenge: Procedure boundary with no open RuntimeCommand

The research draft flagged a possible Step-3 boundary gap: `pending-child-invocation` requires `root_command_id`, while Procedure may remain active between player Commands.

Could a turn/round/rest boundary autonomously occur during that gap and need mandatory work with no root command?

## Evidence

- runtime does not execute/advance world time in the background merely because the user is absent;
- Step 3 defines BoundaryOccurrence as produced by causal advancement;
- advancement freezes at a reached due coordinate and must resolve/durably suspend same-coordinate consequences before moving beyond it;
- Procedure persists between Commands, but persistence of Procedure state does not itself generate a boundary occurrence.

## Inference

A material Procedure boundary is created by some accepted causal execution that advances/changes the Procedure or chronology. In ordinary current architecture that execution has a root RuntimeCommand.

If another player/session causes the boundary, that other accepted execution supplies the causal root.

Cold hydration does not create fictional advancement merely because time passed outside the runtime.

Therefore a normal durable state containing:

```text
boundary already passed
mandatory consequence required
no accepted root/pending child identity
```

is an advancement/materialization defect, not a legitimate “scheduler needs synthetic command” case.

## Revisit trigger

If a later architecture slice explicitly admits autonomous/background system execution that advances gameplay without an accepted Interaction/RuntimeCommand, Step 3 root execution ownership must be reopened deliberately.

Current Step 5.3 should not speculate that subsystem into existence.

Challenge result: **no internal/synthetic root command admitted**.

---

# 10. Critical challenge: future RNG reservation

Current Continuation schema requires `future_rng_frontier`. Step 3 prose says future RNG frontier/state needed for deterministic continuation is checkpointable.

Could retiring it break deterministic resume?

## Strongest case for keeping it

A deterministic PRNG cursor can guarantee that after restart the next draw is identical even when the result has not yet been generated. This is operationally convenient and compact.

## Counter-analysis

The architectural correctness question is not “would the same process-level PRNG produce the same next value?” It is “has a future random experiment already entered accepted gameplay semantics?”

If no experiment has been accepted, producing a different future random number after restart changes no established gameplay fact.

If an experiment has been accepted strongly enough that its identity/distribution must survive, the engine should persist that accepted experiment identity/inputs (or generate/fix its value before suspension). A generic cursor does not itself state what experiment was accepted.

A global/per-Continuation PRNG frontier also creates accidental coupling among otherwise independent random experiments and scopes.

## Simplest viable rule

Default:

> Generate randomness only when the mechanic has actually established that the draw is required. Commit the raw generated value with the continuity edge before any suspension/retry can depend on it.

Optional later extension:

> If a concrete mechanic truly requires reservation-before-generation, represent a stable typed random-experiment reservation rather than a generic future stream frontier.

Challenge result: **recommend retirement of mandatory generic `future_rng_frontier` in later machine realization; no replacement class now**.

---

# 11. Crash-window challenge against A-NARROW

## W1 — crash before DUE selection

Owner remains ARMED. Recovery derives comparison again. Safe.

## W2 — crash during materialization before semantic commit

No promised partial transition is visible. Retry from ARMED.

## W3 — crash after claim but before child identity durable

Forbidden state. Materialization closure must prevent it; if observed, integrity defect.

## W4 — crash after child identity durable but before child starts

Owner points/commits to same occurrence claim; execution root resumes same child.

## W5 — crash during child

Resolution/Continuation semantics resume same causal firing and fixed inputs.

## W6 — crash after child outcome but before owner resolution

Child outcome and owner REARM/UNARM/TERMINAL must join the same semantic completion edge when that outcome determines owner state. Split durable visibility is forbidden.

## W7 — crash after immediate deterministic response

Final owner state and execution/idempotency evidence already committed; old occurrence is gone.

No unresolved crash window requires a standalone firing owner.

---

# 12. Cross-domain challenge

Could A-NARROW require impossible atomic mutation across campaign and live domains?

Step 5.3 must not require one physical distributed transaction.

The logical rule is scoped by **current owning domain**:

- temporal owner mutation and its execution materialization belong to the same current writable scope whenever that owner is live-owned;
- a campaign representation cannot simultaneously mutate the same live-owned truth;
- cross-domain consequences must route through later 5.8 synchronization/ownership protocol rather than one hidden transaction.

If one materialization genuinely requires atomic mutation of two independently writable domains, that is a later Step-5.8 slow-path design question and cannot be “solved” by a global firing ledger here.

Challenge result: **A-NARROW remains compatible with partitionable ownership**.

---

# 13. Revised recommendation

After challenge, recommend **A-NARROW / OWNER-CLAIM MATERIALIZATION**:

1. `due` is derived and three-valued: NOT_DUE / DUE / INDETERMINATE.
2. Every independently materializable temporal occurrence has stable identity distinct from timing value.
3. Before materialization, owner state is the sole obligation authority; Agenda is disposable.
4. If the occurrence completes in the same execution edge, update owner directly; no claimed phase is required.
5. If mandatory execution outlives the edge, atomically make the exact owner occurrence unavailable for fresh materialization **and** create/reference existing Step-3 firing/pending execution identity.
6. Minimal owner claim stores only enough to identify the claimed occurrence/execution relation; it does not copy child payload/status or timing authority.
7. Child settlement atomically resolves owner to REARM / UNARM / TERMINAL when its outcome controls owner state.
8. No standalone firing/job record.
9. No synthetic/internal RuntimeCommand for hypothetical background time; revisit only if autonomous gameplay execution is later admitted.
10. No universal future RNG frontier; preserve fixed generated values and introduce typed reservation only if a concrete future mechanic proves reservation-before-generation necessary.

---

# 14. Human-decision assessment

One material architecture choice remains genuinely reasonable:

```text
A-NARROW
    owner explicitly claims an in-flight occurrence
    before/with long-lived child execution

B-IDEMPOTENT-LOOKUP
    owner remains visibly armed/due
    while bounded firing-key lookup suppresses rematerialization
```

Both can be made correct.

The choice affects:

- native owner lifecycle semantics;
- coupling between temporal owner evaluation and execution-root lookup;
- schema complexity versus runtime lookup complexity;
- how locally inspectable/debuggable pending temporal state is;
- retention/idempotency dependency shape.

Recommendation: **A-NARROW** with HIGH confidence, because it preserves local semantic clarity and keeps idempotency evidence from becoming an implicit second eligibility authority.

This is a fundamental owner-state/lifecycle choice and should be presented to the human architect in a Decision Brief before candidate canonicalization.
