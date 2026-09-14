# Implementation Planning — PLAYER Authority / Collaboration Reconciliation Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 38 — SIGNIFICANT**

## Finding

WP-17 Law 27 requires pending voluntary-agency obligations to be re-evaluated when PLAYER membership, controlled-PC relation or applicable authorization changes materially while waiting. Requirement identity must not be rewritten in place: the old generation becomes obsolete/superseded and a successor is created from current authority only when the same dependency lineage remains valid.

The current package does not provide the reverse executable trigger from an access-control transition to the affected current collaboration obligations.

Current RD-12 does provide:

- completeness-protected per-PLAYER `collaboration_route_refs`;
- `reconcile_player_route_companions(...)` for obligation lifecycle changes;
- `associate_input(...)`, whose validation notices a controller/authorization mismatch when new input arrives.

But those mechanisms run from the collaboration/input side. A PLAYER deactivation, reactivation, control transfer or relevant authorization change can occur while no new collaboration input arrives. The proof ledger nevertheless maps WP-17 verification theme 16 to `InputAssociationTests + RD-09 authorization/currentness`, which does not establish the required reverse transition.

Therefore an acknowledged campaign authority change can otherwise leave an old OPEN/CLOSED obligation generation carrying stale required-controller semantics until a later input happens to touch it. That violates WP-17 Law 27 and creates a proof-without-mechanism defect.

No new global index is required: F35-preserved `world.player.collaboration_route_refs` is already the bounded reverse route from affected PLAYER to current obligations.

---

# 1. Required RD-12 reverse reconciliation producer

RD-12 must add an explicit bounded producer conceptually equivalent to:

```text
reconcile_collaboration_for_player_access_transition(
    player_before,
    player_after,
    current_collaboration_route_refs,
    load_current_obligation_exact,
    current_dependency_opportunity_basis,
) -> CollaborationAuthorityReconciliation | BLOCKED_INTEGRITY
```

The producer is invoked by F37 whenever a frozen PLAYER access transition can materially change voluntary-agency requirements.

`current_collaboration_route_refs` is a bounded routing companion, not authority. Every nominated obligation generation must be direct-loaded and revalidated from its exact current native owner before any reconciliation decision is made.

Conceptual output:

```text
CollaborationAuthorityReconciliation {
    player_id
    pinned_campaign_revision
    inspected_route_refs[]
    obligation_transitions[]: {
        obligation_id
        before_generation
        disposition:
            UNCHANGED
          | OBSOLETE_NO_SUCCESSOR
          | OBSOLETE_AND_SUCCESSOR
        successor_generation? 
        resulting_required_route_holders[]
    }
    affected_player_route_ref_deltas[]
}
```

The output is ephemeral mutation planning. It is not a durable reconciliation journal or second collaboration authority.

---

# 2. Exact transition law

For every exact current `(obligation_id, generation)` nominated by an affected PLAYER route ref:

1. load the exact current obligation generation;
2. validate that the PLAYER ref and obligation's required/accepted-input route-holder semantics agree;
3. re-evaluate whether the underlying decision opportunity still exists under current dependency state;
4. re-evaluate the current required contributor/controller/authorization basis;
5. apply exactly one disposition:

```text
same opportunity + same requirement identity
  -> UNCHANGED

opportunity no longer exists
  -> current generation OBSOLETE
  -> no successor

same dependency lineage still exists
+ material requirement identity changed
  -> current generation OBSOLETE
  -> successor generation from current authority

semantically new dependency
  -> not a successor; owning admission path creates a new obligation_id if required
```

Controller transfer itself never synthesizes a voluntary fictional action, consent, refusal, pass or readiness.

The old generation is never rewritten in place to make a stale reply or stale controller requirement appear current.

---

# 3. Old-input / successor isolation

WP-17 stale-generation law remains mandatory:

- an input addressed to the old terminal/obsolete/superseded generation does not append to its successor;
- it does not reopen the old generation;
- it does not silently carry accepted fictional intent across a changed requirement identity;
- at most it may be used as a discovery hint for an explicit current reinterpretation/reconfirmation path already permitted by the owner.

The reconciliation producer therefore never copies old-generation input association into a successor merely because text or contributor identity looks similar.

---

# 4. Bounded reverse routing / corruption behavior

Ordinary access transition reconciliation must not scan all `runtime.collaboration_obligation` records.

The bounded path is:

```text
exact current PLAYER
-> collaboration_route_refs
-> exact current obligation generations
-> owner revalidation
-> reconciliation
```

Integrity rules:

- a missing route ref that should exist under a proven current obligation is companion corruption;
- a ref to an absent/wrong generation is corruption/staleness;
- duplicate inconsistent refs are corruption;
- an obligation that names the PLAYER as a required/accepted-input holder but is absent from a completeness-proven PLAYER companion is corruption;
- corruption blocks the authority transition or routes to explicit repair/rebuild handling; it is not treated as proof that no obligation is affected.

Maintenance/recovery may rebuild PLAYER collaboration companions from current obligation owners under the existing derivative-companion rules. Broad scan remains repair-only, never the ordinary access-transition path.

---

# 5. Campaign publication closure

For a PLAYER authority transition requiring collaboration reconciliation, F37 and RD-12 compose into one campaign-domain resulting-tree closure after any prerequisite LIVE terminalization:

```text
F37 exact PLAYER access transition delta
+ F9 principal-routing delta when applicable
+ each affected obligation old-generation terminalization
+ each required successor generation
+ all affected PLAYER collaboration_route_refs deltas
+ other already-required campaign companions
  MUTATES_WITH
one RD-06 campaign publication closure
```

No acknowledged campaign state may expose:

- new PLAYER membership/control authority with an old collaboration generation still requiring the previous controller;
- an obsolete collaboration generation whose PLAYER route refs still nominate it as current;
- a successor generation that is not routed to every current required route holder;
- a route ref to an obligation generation absent from the same resulting campaign authority state.

This does not create a distributed transaction. If LIVE sources must be closed first, those exact-source CAS edges remain separate native durability edges and the campaign transition proceeds only forward from their truthful terminal result.

---

# 6. Recovery / retry

Cold recovery and stale-head retry use the same bounded reverse route and exact current owners.

A stale-head publication rejection must:

1. reload current PLAYER;
2. reload current `collaboration_route_refs`;
3. reload every nominated current obligation generation;
4. recompute the reconciliation from the new current campaign basis;
5. never replay a stale obsolete/successor plan over newer collaboration generations.

An indeterminate prior publication is reconciled from current resulting campaign state. There is no durable pending-reconciliation queue.

---

# 7. Required tests / proof repair

Extend RD-12 with a focused group conceptually:

```text
PlayerAuthorityCollaborationReconciliationTests
```

Required cases:

1. required controller deactivation while obligation OPEN obsoletes the old generation even when no new input arrives;
2. controlled-PC transfer while waiting obsoletes the old generation and creates a successor only if the same dependency lineage/opportunity remains valid;
3. activation/reactivation that does not affect any current requirement leaves unrelated generations unchanged;
4. authorization withdrawal that removes a still-required voluntary agency path yields obsolete/no-successor or successor according to current opportunity semantics;
5. controller transfer never synthesizes a PASS/READY/choice/action;
6. old-generation late input cannot append to successor;
7. successor route refs are derived from current required holders, not copied blindly from predecessor;
8. old generation terminalization + successor + all PLAYER route-ref changes publish in one campaign closure;
9. stale/missing/wrong-generation PLAYER route ref blocks or repairs; ordinary path never broad-scans obligations;
10. stale campaign HEAD forces complete re-read/reconciliation; no stale successor plan is replayed;
11. F37 access transition cannot publish when `collaboration_reconciliation_required` is true but this reconciliation output is absent;
12. an obligation-side input association still revalidates current authority independently; the reverse trigger does not weaken input-time checks.

Amend WP-17 proof theme 16:

```text
Wp17CollaborationProofTests.test_16_controller_change_requires_successor_or_obsolete
```

must require the reverse access-transition reconciliation witness above. `InputAssociationTests + RD-09 authorization/currentness` is supporting evidence only and cannot by itself close the theme.

---

# 8. Execution graph amendment

Add checkpoints:

```text
RD12_PLAYER_AUTHORITY_RECONCILIATION_LOCAL_READY
RD09_RD12_PLAYER_AUTHORITY_COLLABORATION_JOIN
```

Required edges:

```text
RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY
  HARD_PRECEDES
RD12_PLAYER_AUTHORITY_RECONCILIATION_LOCAL_READY

RD09_PLAYER_ACCESS_TRANSITION_LOCAL_READY
+ RD12_PLAYER_AUTHORITY_RECONCILIATION_LOCAL_READY
  JOIN_BEFORE_INTEGRATION
RD09_RD12_PLAYER_AUTHORITY_COLLABORATION_JOIN
```

For any F37 transition marked `collaboration_reconciliation_required`, RD-06 final campaign publication waits for `RD09_RD12_PLAYER_AUTHORITY_COLLABORATION_JOIN` plus any required LIVE-terminal/principal-route joins.

This is a checkpoint-level dependency and does not serialize unrelated RD-09 LIVE work with unrelated RD-12 collaboration work.

---

# 9. Non-goals

This repair does not add:

- a global collaboration reverse index;
- obligation scanning on ordinary access transitions;
- automatic actions for absent/transferred players;
- a persistent reconciliation worker/queue;
- in-place obligation authority rewrites;
- automatic old-input carry-forward;
- a second PLAYER or collaboration semantic owner;
- distributed campaign/LIVE transactions.

---

## Disposition

```text
AUTHOR_GRAPH_FINDING_38: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
