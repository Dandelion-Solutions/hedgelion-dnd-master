# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Resolution Gate

Status: **RESOLVED — READY FOR CANONICALIZATION**

Date: 2026-08-20

Owner-approved direction:

> **EDGE-OBLIGATION / SCOPE-POLICY RECOVERY-CLOSURE DURABILITY**

Reviews and resolves findings from:

- `2026-08-20-step-5-5-soft-hard-save-durability-adversarial-review.md`

No finding requires a new owner-level decision. The following consistency refinements are accepted for canonicalization.

## R1 — Owner-relative establishment

**Accepted.**

`ESTABLISHED` means accepted/committed current semantic state under the owning domain contract.

A prospective or in-flight mutation is not established merely because it has been computed in memory.

Therefore:

- ordinary singleplayer execution may establish HOT truth before campaign durability;
- same-scene live policy may make successful live CAS part of the shared-state acceptance/reveal edge;
- failed prospective writes do not create shared truth merely from local candidate state.

## R2 — Multi-domain save is composed native durability

**Accepted.**

Successful explicit save is a property over a compatible composed set of required domain-native durable sources.

It does not imply:

- one repository commit;
- one scalar cross-domain frontier;
- one distributed transaction;
- one globally writable save owner.

Each native domain follows its own publication authority/atomicity contract. The resulting source composition must satisfy Step-5.2 Resumable Runtime Closure for the promised save point.

## R3 — Partial native publication remains real

**Accepted.**

If a multi-source save attempt publishes one required native source but fails another:

- overall explicit save is not confirmed/successful;
- the successful native publication remains real durable authority;
- the runtime SHALL NOT pretend the prior source revision is still current merely to simplify retry;
- before dependent continuation, the host must adopt/revalidate a coherent current source composition under normal native ownership rules;
- if a required source remains unresolved/suspect, only the dependent scope is gated under existing correctness/integrity rules.

Exact physical ambiguous-write detection remains 5.6/5.8.

## R4 — Clean already-durable save needs no heartbeat

**Accepted.**

If the explicit-save postcondition already holds and there are no required dirty writes:

```text
known compatible durable source closure already satisfies SAVE
    -> save may succeed
    -> acknowledge saved
    -> zero gameplay publication required
```

No new commit/checkpoint/heartbeat is required solely to prove that the user asked for save.

## R5 — Durable source closure != pending write set

**Accepted.**

Canonical terminology will distinguish:

```text
REQUIRED DURABLE SOURCE CLOSURE
    all native owners/dependencies/revisions needed to satisfy the promise

PENDING WRITE SET
    only currently non-durable/changed native material that must be published
```

Already durable compatible dependencies participate in the closure proof but need not be rewritten.

## R6 — No false accumulation overaggregation

**Accepted.**

A durability policy may aggregate a practical scope/partition only when that aggregation is compatible with actual writable/authority/visibility ownership.

It SHALL NOT cross independently writable scopes merely for implementation convenience when doing so would create false synchronization or a hidden global authority.

A conservative singleplayer campaign-local partition remains legal where there is one effective local writer and no independent authority split.

## R7 — Safe points for opportunistic/risk-control flush

**Accepted.**

Advisory capacity or exposure-risk policy may request publication only at a point where selected roots are established and a coherent closure can be frozen/revalidated.

It SHALL NOT persist partial model reasoning or cut through an unresolved owning atomic/semantic edge.

Reliable destructive lifecycle handling remains Step 5.4.

## R8 — Friendly failed-save continuation is subordinate to independent HARD edges

**Accepted.**

A failed explicit save does not hard-lock otherwise coherent local/private play.

However that permission SHALL NOT bypass any independently active correctness-critical:

```text
MUST_BE_DURABLE_BEFORE(edge)
```

Only the relevant dependent edge/scope remains gated.

## R9 — Exposure tracks oldest still-relevant unpublished state

**Accepted.**

Exposure policy concerns the oldest still-relevant established/recovery state that remains unpublished in the policy partition.

Lawfully superseded dirty intermediate values that are no longer required by current truth, execution continuity, recovery, provenance or audit do not keep exposure alive merely because they once existed.

Implementation need not retain per-delta historical clocks when a correct aggregate representation exists.

## R10 — Degraded-risk warning/retry cadence is not per-turn spam

**Accepted.**

Step 5.5 requires truthful degraded durability state and later retry opportunities; it does not require repeating the same warning or publication attempt on every gameplay turn.

Retry/backoff/notification cadence is later runtime/product policy, provided it cannot falsely claim the exposure target has been satisfied.

---

# Resolution result

All adversarial findings are resolved mechanically without changing the owner-approved architecture direction.

Canonical specification SHALL incorporate R1–R10.

No Step-5.5 architecture blocker remains at this gate.
