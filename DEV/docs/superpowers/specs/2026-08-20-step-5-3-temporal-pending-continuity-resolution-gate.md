# Step 5.3 — Temporal & Pending-Obligation Continuity — Resolution Gate

Status: **RESOLUTION ACCEPTED — READY FOR CANONICALIZATION**

Date: 2026-08-20

Inputs:

- `2026-08-20-step-5-3-temporal-pending-continuity-candidate-spec.md`
- `2026-08-20-step-5-3-temporal-pending-continuity-adversarial-review.md`

Owner decision retained:

> **A-NARROW / OWNER-CLAIM MATERIALIZATION**

No new human architect decision is required.

---

# 1. Accepted refinements

The canonical specification SHALL incorporate all adversarial findings:

1. **Conditional claim scope** — a long-lived owner claim exists only while source-owner settlement remains contingent on accepted execution. Finalized/terminalized/rearmed source state may coexist with mandatory descendants without retaining a pointless claim when those descendants no longer control source settlement.
2. **Continuous bounded recoverability** — materialization/settlement transitions that change temporal/execution root membership must preserve bounded discoverability at every acknowledged durable recovery closure. Routing remains derivative evidence, not authority.
3. **Immediate-rearm safety** — advancing to the next occurrence while the prior firing remains unresolved requires both schedule independence and overlap/order safety; contingent claim is the default otherwise.
4. **RNG experiment association** — fixed accepted random results required by unfinished execution must be recoverably associated with stable accepted experiment/invocation identity and interpretation inputs, not merely preserved by incidental positional order.
5. **Pinned interpretation** — accepted firing execution resumes under the compatible pinned execution/catalog context established when it was accepted; current definitions govern only later fresh occurrences unless an explicit migration says otherwise.
6. **Direct-finalization retry safety** — source occurrence generation/final state plus execution receipt/idempotency/revision evidence must reject stale attempts to reapply an already finalized occurrence even when no claim remains.

---

# 2. Ownership disposition

Canonical ownership remains:

```text
native temporal owner
    owns existence, armed/current occurrence, timing binding, source lifecycle

chronology owner
    owns temporal/causal relation evidence

Step-3 execution owner
    owns accepted child/Resolution/Continuation execution progress

owner-local CLAIMED relation
    only records that current source occurrence settlement is committed to F
    does not own F progress or temporal due state

routing/checkpoint/index metadata
    bounded retrieval/recovery evidence only
```

No new universal firing/job/scheduler authority is admitted.

---

# 3. Canonical lifecycle forms

The final spec SHALL expose three legal materialization shapes:

```text
A. DIRECT FINALIZATION
   ARMED(G)
      -> final owner state
      + stable causal/idempotency evidence
      + mandatory descendants if required

B. SAFE IMMEDIATE REARM
   ARMED(G)
      -> ARMED(G+1)
      + accepted execution F(G)
   only when schedule independence + overlap/order safety are proven

C. CONTINGENT OWNER CLAIM
   ARMED(G)
      -> CLAIMED(G,F)
      -> F settles
      -> REARM(G+1) | UNARM | TERMINAL
```

All three satisfy the same governing invariant:

> Once occurrence `G` has crossed into accepted execution, native owner state no longer presents `G` as a distinct fresh materialization candidate, and recovery can reach every still-significant accepted consequence through bounded typed roots.

---

# 4. Rejected alternatives remain rejected

- B-IDEMPOTENT-LOOKUP is not selected; firing-key lookup remains duplicate suppression/recovery evidence rather than temporal eligibility authority.
- standalone firing/obligation record remains unjustified.
- generic scheduler/job ledger remains forbidden without a future explicit architecture decision.
- durable `due` state remains derived/non-authoritative.
- universal `future_rng_frontier` remains targeted for retirement/narrowing during machine realization.

---

# 5. Later-slice boundary

Canonical Step 5.3 may require later slices to physically enforce its closure invariants, but SHALL NOT choose:

- SOFT/HARD/SAVE cadence or blocking policy (5.5);
- Git publication transaction mechanics (5.6);
- checkpoint/root wire representation (5.7);
- live-epoch ownership/CAS/compaction protocol (5.8);
- chronology persistence/reconciliation representation (5.9);
- Story or host-delivery job state machines (5.10/5.12);
- GC/retention mechanics (5.13).

---

# 6. Resolution gate

All material candidate/adversarial findings are resolved without an unowned blocker.

Human architect decision required: **NO**.

Canonicalization authorized by the approved A-NARROW decision and this resolved review.

Do not begin Step 5.4 as part of this canonicalization/closure operation.
