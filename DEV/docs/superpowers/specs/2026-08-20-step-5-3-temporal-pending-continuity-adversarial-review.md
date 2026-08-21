# Step 5.3 — Temporal & Pending-Obligation Continuity — Adversarial Review

Status: **ADVERSARIAL REVIEW — SIGNIFICANT REFINEMENTS RESOLVED — NO NEW OWNER DECISION REQUIRED**

Date: 2026-08-20

Reviewed candidate:

- `2026-08-20-step-5-3-temporal-pending-continuity-candidate-spec.md`

Approved owner decision under review:

- **A-NARROW / OWNER-CLAIM MATERIALIZATION**

Review objective: attempt to break the candidate through ownership ambiguity, crash windows, bounded-recovery gaps, unnecessary state, concurrency/order leakage, stale interpretation context and RNG replay ambiguity before canonicalization.

---

# 1. Executive result

A-NARROW survives adversarial review.

No finding reopens the owner choice between A-NARROW and B-IDEMPOTENT-LOOKUP. No generic firing/job owner is justified.

The review found four significant mechanical refinements and two clarification findings:

1. `CLAIMED` must be required only while **source-owner settlement itself remains contingent** on long-lived execution; a finalized source transition may materialize descendants without retaining a claim.
2. materialization needs an explicit **bounded-recoverability handoff invariant** between armed temporal routing and accepted execution-root routing;
3. immediate rearm while the prior firing is still in flight is legal only when **overlap/order safety** is proven, not merely when the next binding is outcome-independent;
4. fixed accepted RNG must be **stably associated with its accepted experiment/invocation identity**; a bare positional scalar list is not an architecture-level guarantee;
5. accepted firing execution must continue under pinned accepted interpretation context rather than silently reinterpret through a changed current catalog;
6. direct-transition idempotency must survive stale retries even when no `CLAIMED` state remains.

All six are derivable engineering refinements of the approved decision. Human architect escalation is not required.

---

# 2. S1 — Candidate overstates when a long-lived claim is required

Severity: **SIGNIFICANT — RESOLVED BY NARROWING**

## Attack

The candidate can be read as:

> if any mandatory execution created by a temporal occurrence outlives the materializing edge, the source owner must remain `CLAIMED` until that descendant settles.

That is unnecessarily strong.

Counterexample:

```text
Effect expiration occurrence G
    -> same committed edge:
       Effect becomes terminal
       mandatory support-loss child F is materialized

F continues later
```

The source temporal occurrence is already fully and irreversibly settled: the Effect is terminal and `G` cannot be selected again. The descendant may still be mandatory, but its outcome no longer decides the source owner's lifecycle.

Retaining `CLAIMED(G,F)` on the terminal Effect would duplicate information and complicate terminal-state schemas/GC without improving correctness.

## Resolution

Refine the rule:

> A long-lived owner-local claim is required only when the source occurrence has been accepted but the source owner's own final settlement remains contingent on the long-lived accepted execution.

Three legal forms become explicit:

```text
A. DIRECT FINALIZATION
   ARMED(G) -> final owner state
   + any mandatory descendants materialized atomically
   source owner needs no long-lived claim

B. IMMEDIATE REARM
   ARMED(G) -> ARMED(G+1)
   + child F(G)
   allowed only under the stronger overlap-safety rule in S3

C. CONTINGENT SETTLEMENT
   ARMED(G) -> CLAIMED(G,F)
   child F settles
   -> REARM | UNARM | TERMINAL
```

The shared A-NARROW invariant is not “always store CLAIMED.” It is:

> once `G` is accepted, native owner state must stop presenting `G` as a fresh independently materializable occurrence at the same semantic closure that accepted execution identity is established.

Disposition: **ACCEPTED refinement**.

---

# 3. S2 — Missing bounded-recoverability handoff at materialization

Severity: **SIGNIFICANT — RESOLVED**

## Attack

Step 5.2 guarantees that every armed independently-due native temporal source remains enrolled in bounded typed temporal-source routing for its armed lifetime.

A-NARROW creates a lifecycle edge where that owner may stop being armed and become claimed/finalized while execution `F` becomes the recovery-critical active root.

A logically coherent owner+execution pair is still insufficient if cold recovery cannot enumerate either side without a broad scan.

Bad durable window:

```text
owner G is no longer armed
therefore temporal routing no longer enumerates it
F exists
but F/root membership is not yet enrolled in bounded active-execution recovery routing
```

Nothing in semantic authority is duplicated, but bounded recovery has lost reachability.

The reverse ordering can also produce misleading duplicate roots if routing semantics are not explicit, although duplicate retrieval evidence is safer than omission.

## Resolution

Add a normative **RECOVERY-REACHABILITY HANDOFF LAW**:

> A materialization/settlement edge that changes bounded recovery-root membership SHALL preserve continuous bounded discoverability of every still-gameplay-significant owner/execution obligation. An armed temporal source may cease requiring armed-temporal routing only when the replacement accepted execution/final owner state is recoverable through its owning typed root path in the same acknowledged durability closure.

Important:

- root/routing membership remains derivative retrieval evidence, not semantic authority;
- temporary duplicate routing/reference visibility is acceptable if owning contracts allow it;
- an omission interval is not acceptable at an acknowledged durable recovery frontier;
- exact checkpoint/live/campaign representation and transaction order remain 5.6–5.8 concerns.

This follows Step-5.2 root-membership coherence and does not introduce a new owner.

Disposition: **ACCEPTED refinement**.

---

# 4. S3 — Immediate rearm condition is too weak

Severity: **SIGNIFICANT — RESOLVED**

## Attack

Candidate 4.3 allows immediate transition to `G+1/B2` when the next schedule is independent of child outcome.

Outcome-independence alone does not prove correctness.

Counterexample:

```text
G fires child F(G)
owner immediately rearms G+1
G+1 becomes due before F(G) settles
```

Even if F(G) cannot change the next deadline, the mechanic may require serial resolution or F(G) may mutate state used by F(G+1). Immediate rearm could then create overlapping firings whose ordering is mechanically significant.

Using ID order to settle that overlap would violate Step-3/5.1 ordering rules.

## Resolution

Immediate rearm while `F(G)` is unresolved is legal only if the governing mechanic proves both:

1. **schedule independence** — settlement of `F(G)` cannot unarm, terminate, reschedule or invalidate `G+1`; and
2. **overlap/order safety** — if `G+1` becomes actionable before `F(G)` settles, concurrent/pipelined existence is explicitly legal, or a registered mechanical ordering/serialization rule prevents semantic ambiguity.

Otherwise retain contingent settlement:

```text
CLAIMED(G,F)
    -> settle F
    -> decide/rearm G+1
```

This is the safer default.

Disposition: **ACCEPTED refinement**.

---

# 5. S4 — Fixed RNG continuity needs stable experiment association

Severity: **SIGNIFICANT — RESOLVED AS ARCHITECTURE REQUIREMENT / MACHINE DEBT**

## Attack

The candidate correctly rejects a universal future RNG frontier and requires already generated/accepted values to remain fixed.

Current `runtime-continuation-state.schema.json`, however, represents `fixed_rng_results` as a positional array of scalar values. A positional list by itself does not prove which accepted random experiment a value belongs to if execution is refactored, multiple draws exist, safe recomputation changes phase, or a retry re-enters through a different traversal path.

Merely preserving values is weaker than preserving **accepted experiment identity -> fixed result** semantics.

## Resolution

Strengthen the architecture requirement:

> Every generated random result whose value is required by unfinished accepted execution SHALL be recoverably associated with the stable accepted experiment/invocation identity and the fixed inputs needed to interpret that result. Recovery may not regenerate or remap the result by incidental list/traversal order.

This does not require a new generic RNG service or new schema during Step 5.3 architecture.

Machine realization must determine whether existing invocation facts/receipt structures can supply the stable association or whether `fixed_rng_results` needs a typed keyed representation.

`future_rng_frontier` remains targeted for retirement/narrowing unless a concrete reservation-before-generation use case appears.

Disposition: **ACCEPTED refinement**.

---

# 6. C1 — Accepted execution must not reinterpret through changed catalog state

Severity: **MODERATE CLARIFICATION — RESOLVED**

## Attack

An owner may be claimed by firing `F`, then content/catalog definitions can evolve before recovery. Re-evaluating `F` against current definitions could change activity, cadence, targets or RNG semantics while preserving the same firing identity.

## Existing protection

Step 5.2 requires resolvable compatible runtime/catalog interpretation context for open execution; Step 3 Continuation/Resolution state pins accepted inputs/context required for deterministic continuation.

## Resolution

Canonical Step 5.3 must state explicitly:

> materialized execution resumes using its accepted pinned execution/interpretation context; current owner definition may govern only later fresh occurrences after lawful settlement/rearm/migration.

If compatible interpretation context for `F` cannot be resolved, recovery blocks/suspects compatibility rather than silently replaying `F` under current rules.

Disposition: **CLARIFIED**.

---

# 7. C2 — Direct-finalization stale retry suppression must not depend on retained CLAIMED state

Severity: **MODERATE CLARIFICATION — RESOLVED**

## Attack

S1 deliberately allows owner `G` to finalize immediately and retain no claim. A stale retry may still carry old occurrence identity `G`.

If duplicate suppression depended only on owner `CLAIMED`, direct finalization would be vulnerable.

## Resolution

Direct finalization already requires:

- owner occurrence identity/generation to advance/disappear;
- causal execution/transition idempotency/receipt evidence on the same committed edge;
- revision/expected-state checks supplied by the execution/publication model.

Canonical wording must require stale attempts referring to old `G` to fail eligibility against current owner state and/or resolve to the already committed execution receipt rather than reapply the transition.

The retention lifetime/physical index for such evidence remains later publication/GC work.

Disposition: **CLARIFIED**.

---

# 8. Re-run of principal hostile scenarios

## H1 — Crash before due acceptance

Owner remains armed and enrolled. Candidate rebuilt. **PASS**.

## H2 — Crash after claim but before child root is discoverable

S2 forbids acknowledging such a durability closure. **PASS after refinement**.

## H3 — Terminal owner with long-lived mandatory descendant

S1 permits owner terminalization + child materialization without pointless claim. **PASS after refinement**.

## H4 — Periodic child waits on human Reaction while next interval arrives

Default contingent claim prevents accidental overlapping occurrence unless mechanic explicitly proves S3 safety. **PASS after refinement**.

## H5 — Same timing tuple repeats after rearm

Stable occurrence identity distinguishes generations. **PASS**.

## H6 — Two independent live scopes each have due work

No global order introduced; each source materializes in its owning scope. Cross-scope interaction remains 5.8. **PASS**.

## H7 — Current catalog changed after firing accepted

C1 pins accepted execution interpretation; no silent reinterpretation. **PASS after clarification**.

## H8 — Continuation has two fixed rolls and retry traversal order changes

S4 requires stable experiment association, not positional coincidence. **PASS after refinement**.

## H9 — Stale retry of directly finalized expiration

C2 rejects old generation / resolves committed idempotency evidence. **PASS after clarification**.

## H10 — Due relation remains chronologically incomparable

`INDETERMINATE`; unrelated work may continue; material crossing requires reconciliation. **PASS**.

## H11 — Procedure persists between Commands but no fictional advancement occurs

No synthetic background root invented. **PASS**.

## H12 — Owner claim exists but F was GC'd

Invalid recovery closure; 5.13 must protect necessary evidence until source claim/duplicate-suppression dependency ends. **PASS as later-slice requirement**.

---

# 9. Authority/abstraction contamination sweep

New concepts retained by Step 5.3:

```text
occurrence identity/generation
    -> owner-local identity property, not timing authority

CLAIMED relation
    -> conditional native-owner lifecycle relation
       only while source settlement depends on accepted execution

DUE comparison tri-state
    -> derived evaluation result, not durable authority

recovery reachability handoff
    -> derivative routing integrity rule, not semantic owner
```

Rejected concepts remain rejected:

```text
generic scheduler
generic pending job/obligation record
standalone firing authority
durable due flag
authoritative Temporal Agenda
synthetic internal RuntimeCommand for elapsed host time
universal future RNG stream/frontier
implicit total order by storage/ID
```

No reviewed concept introduces duplicate canonical authority.

---

# 10. Final adversarial disposition

**A-NARROW remains recommended and owner-approved.**

Required canonicalization refinements:

1. define claim as conditional on unresolved source-owner settlement, not arbitrary descendant lifetime;
2. add continuous bounded-recovery reachability handoff across ARMED -> accepted execution/final owner transition;
3. strengthen immediate-rearm legality with overlap/order safety;
4. require stable experiment association for fixed accepted RNG;
5. explicitly pin materialized firing interpretation context;
6. explicitly cover stale-retry suppression after direct finalization.

Human decision required: **NO**.

Confidence after review: **HIGH**.

Next gate: produce a resolution record confirming all findings are incorporated, then canonicalize Step 5.3. Do not start Step 5.4 during this closure sequence.
