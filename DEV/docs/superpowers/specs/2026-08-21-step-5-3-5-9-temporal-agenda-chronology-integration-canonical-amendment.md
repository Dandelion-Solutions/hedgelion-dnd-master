# Steps 5.3 / 5.9 — Temporal Agenda ↔ Chronology Integration — Canonical Amendment

Status: **CANONICAL AMENDMENT — SUPPLEMENTS STEPS 5.3 AND 5.9**

Date: 2026-08-21

Target branch: `feature/mechanical-runtime-hot-state`

Normative parents:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`

This amendment closes the integration contract between the rebuildable Temporal Agenda from Step 5.3 and the sparse chronology evidence/provider model from Step 5.9.

It does not reopen either architecture slice, create a scheduler, create a chronology service, create a new semantic owner, or authorize background fictional-time advancement.

Where older wording is merely less explicit about this interface, this amendment is the normative clarification.

---

# 1. Integration invariant

The four responsibilities remain distinct:

```text
NATIVE TEMPORAL OWNER
    owns obligation existence, lifecycle, occurrence identity and TemporalBinding

TEMPORAL AGENDA
    rebuildable derived index of armed temporal owners/candidates and their typed recheck dependencies

CHRONOLOGY
    supplies accepted causal/order/metric/boundary evidence needed to evaluate a temporal predicate

STEP-3 EXECUTION
    owns accepted execution/materialized consequences after a due occurrence crosses the acceptance edge
```

Canonical summary:

```text
owner says WHAT EXISTS
Agenda says WHAT MAY NEED RECHECK
chronology says WHAT TEMPORAL EVIDENCE IS LAWFULLY AVAILABLE
Step 3 says WHAT ACCEPTED CONSEQUENCE EXECUTES
```

Neither Temporal Agenda nor chronology may absorb another responsibility.

---

# 2. Temporal Agenda entry semantics

A Temporal Agenda entry is **not a scheduled job** and does not own a due time.

Conceptually it is derived from one current native temporal owner occurrence and includes enough typed dependency information to decide when that owner may need reevaluation.

Conceptual shape only:

```text
TemporalAgendaEntry
    temporal_owner_ref
    owner_occurrence_identity
    binding_ref / binding discriminator
    dependency_keys[]
```

This does not mandate a new durable record/schema. The Agenda may be an in-memory/indexed projection reconstructed from native owners and typed routing.

## LAW TA-C-1 — OWNER REMAINS AUTHORITY

An Agenda entry is valid only while its native owner still exposes the corresponding armed occurrence.

Stale Agenda state cannot keep an occurrence alive, reopen a settled occurrence, invent a deadline or override current owner lifecycle.

## LAW TA-C-2 — AGENDA ORDER IS NOT FICTIONAL ORDER

Agenda list position, priority-queue order, iteration order or registration order has no fictional chronology meaning and cannot break ties among due obligations.

Step-5.3/Step-3 ordering and adjudication rules remain authoritative.

---

# 3. Typed temporal dependency enrollment

Each independently due armed owner/binding family must provide or deterministically derive a bounded set of **typed recheck dependency keys**.

A dependency key identifies a chronology/boundary fact whose accepted change may alter the result of that owner's temporal predicate.

Baseline dependency families include, as applicable:

```text
METRIC_POSITION
    provider scope / provider route + metric context

BOUNDARY_OCCURRENCE
    typed boundary source/family + admitted occurrence identity/domain

EVENT_OR_SIGNAL
    admitted event/signal dependency identity or source binding

RELATION_EVIDENCE
    stable chronology anchor/relation dependency, including material bridge evidence

OWNER_LOCAL_TEMPORAL_STATE
    owner-local schedule generation/arming state when changing it can alter the current predicate
```

Implementations may use more specific owner-family keys. A universal generic dependency-object class is not required.

## LAW TA-C-3 — DEPENDENCY ENROLLMENT IS DERIVATIVE, NOT SEMANTIC AUTHORITY

Dependency enrollment/routing exists to make reevaluation bounded.

It does not own:

- the temporal obligation;
- chronology relations;
- the metric position;
- occurrence identity;
- accepted execution;
- fictional time.

## LAW TA-C-4 — ENROLLMENT MUST BE COMPLETE FOR THE OWNER CONTRACT

If an accepted change to chronology/boundary evidence can lawfully change an armed owner's temporal result, the owner/binding family must be enrolled on a dependency key through which that change can reach the owner boundedly.

An acknowledged state in which a live armed owner depends on chronology evidence but cannot be reached by its declared reevaluation path is a derivative routing/coherence defect, analogous to the bounded-recovery routing rules of Steps 5.2/5.3/5.7.

## LAW TA-C-5 — ENROLLMENT MUST BE BOUNDED

Ordinary reevaluation discovery may not depend on scanning all armed temporal owners, all scenes, all chronology relations or campaign history.

If a dependency fanout becomes operationally unbounded, the implementation must introduce a typed bounded partition/summary/index justified by that concrete owner/provider domain rather than falling back to a campaign-wide scan.

---

# 4. Chronology change → bounded candidate invalidation

An accepted chronology/boundary transition does not execute temporal obligations directly.

Instead it invalidates/reawakens only Agenda entries whose typed dependency keys may have changed meaning.

Canonical flow:

```text
accepted gameplay transition
    -> accepted chronology/boundary/provider evidence changes
    -> derive changed dependency keys
    -> lookup enrolled armed owners for those keys
    -> mark only those owners as temporal reevaluation candidates
    -> reread current owner occurrence + binding + current chronology basis
    -> NOT_DUE | DUE | INDETERMINATE
```

## LAW TA-C-6 — CHRONOLOGY NEVER ENQUEUES EXECUTION

Chronology may establish evidence that makes a predicate `DUE`, but it does not create Step-3 work by itself.

The native owner occurrence must still be current and must cross the Step-5.3 materialization/acceptance edge lawfully.

## LAW TA-C-7 — AGENDA NEVER ADVANCES CHRONOLOGY

Agenda processing cannot increment time, create a fictional boundary, establish a chronology relation or advance a metric provider merely because an armed obligation exists or has waited in host time.

Fictional chronology changes only through admitted accepted causal/world/mechanical transitions.

## LAW TA-C-8 — REEVALUATION USES FRESH CURRENT OWNER STATE

A changed dependency key only identifies candidates.

Before materialization, runtime re-resolves the current native owner occurrence, current binding/provider routing and required chronology evidence. A stale Agenda entry cannot cause execution after the owner has settled/rearmed/moved.

---

# 5. Metric dependency behavior

For metric temporal bindings, dependency enrollment targets the position provider/context actually selected by the owner-specific Step-5.9 routing contract.

Example:

```text
Effect E
    binding.context = world_elapsed_minutes
    current provider = Scene A

Agenda dependency:
    METRIC_POSITION(Scene A, world_elapsed_minutes)
```

If accepted play advances Scene A's metric position, E becomes a candidate.

An unrelated advance in Scene B does not make E a candidate unless E also has an explicit admitted dependency on B/bridge evidence.

## LAW TA-C-9 — PROVIDER MOVEMENT REWRITES DERIVATIVE ENROLLMENT COHERENTLY

When Step 5.9 applies `FOLLOW CURRENT SCOPE`, `PRESERVE SOURCE PROVIDER` or `SAFE REBASE`, the Agenda dependency projection must be recomputed from the resulting owner/binding/provider semantics.

Old provider enrollment may remain transiently duplicated during one coherent transition if needed for safe routing, but no acknowledged state may leave the armed owner reachable only from an obsolete provider.

---

# 6. Boundary / event dependency behavior

Not all temporal obligations are metric.

A binding such as:

```text
at start of next turn
at end of Procedure stage
when accepted EVENT_X occurs
on admitted signal/boundary occurrence
```

is reevaluated from the corresponding typed boundary/event dependency rather than from a numeric clock.

Accepted creation of the relevant stable boundary/event occurrence invalidates the dependent Agenda entries.

Host time, Git commit occurrence and polling do not synthesize such a boundary.

---

# 7. Late chronology bridge / relation evidence

A temporal owner may remain armed with result `INDETERMINATE` because required cross-scope chronology evidence is absent or insufficient.

If a later accepted reconciliation/material bridge supplies evidence that can change that predicate, the owner must be discoverable through its typed relation dependency.

Example:

```text
owner O
    predicate requires comparison across C1/C2
    current result = INDETERMINATE

later accepted bridge R establishes compatible relation evidence

R change
    -> RELATION_EVIDENCE dependency invalidation
    -> reevaluate O
```

## LAW TA-C-10 — INDETERMINATE OWNERS REMAIN ENROLLED WHEN FUTURE EVIDENCE CAN DECIDE THEM

`INDETERMINATE` is not terminal and does not remove an armed owner from Agenda/dependency routing merely because current evidence cannot decide the predicate.

Removal occurs only when native owner lifecycle/binding semantics make the occurrence no longer independently due/relevant or recovery ownership lawfully transfers to another accepted execution/root.

## LAW TA-C-11 — MATERIAL DEMAND MAY FORCE TARGETED RECONCILIATION

If current gameplay requires an `INDETERMINATE` predicate to be decided before proceeding, the runtime may invoke the bounded Step-5.9 reconciliation path for that exact dependency component.

This is distinct from routine Agenda invalidation and does not authorize broad chronology reconstruction.

---

# 8. Due result and materialization

Reevaluation result handling is canonical:

```text
NOT_DUE
    owner remains armed/enrolled according to current binding

INDETERMINATE
    owner remains armed/enrolled;
    no occurrence materialization;
    reconcile only when materially required or when new dependency evidence arrives

DUE
    current owner occurrence becomes eligible for Step-5.3 materialization;
    Step-5.3 direct-finalize / immediate-rearm / CLAIMED(G,F) rules apply;
    accepted descendants execute under Step 3
```

## LAW TA-C-12 — DUE IS EPHEMERAL DERIVED EVALUATION

Agenda and chronology do not persist a generic durable `due=true` bit.

If process loss occurs before the due occurrence is accepted/materialized, recovery simply reevaluates the current native owner against current lawful chronology evidence.

Once materialized, the accepted occurrence/execution identity — not a remembered due result — carries continuity.

---

# 9. Recovery and rebuild

Cold recovery follows Steps 5.2/5.3/5.7/5.9:

```text
recover current native temporal owners
    -> recover TemporalBindings / occurrence lifecycle
    -> re-resolve owner-specific chronology providers/dependencies
    -> rebuild Temporal Agenda + dependency routing/indexes
    -> evaluate candidates only as required by recovery/current gameplay
```

## LAW TA-C-13 — TEMPORAL AGENDA IS REBUILDABLE

Agenda contents and reverse dependency indexes may be lost with process memory without semantic loss if current native owners and required bounded chronology evidence/routing remain durable.

## LAW TA-C-14 — REBUILD CANNOT ADVANCE FICTION OR MATERIALIZE MERELY DUE TO HYDRATION

Cold hydration may discover that an owner is `DUE` under already accepted chronology evidence, but hydration itself is not a fictional event.

Any consequence still crosses the ordinary Step-5.3/Step-3 acceptance boundary with the same occurrence/idempotency rules.

## LAW TA-C-15 — RECOVERY MUST REPRODUCE DEPENDENCY ROUTING SUFFICIENTLY FOR FUTURE INVALIDATION

A recovered armed owner is not fully operationally restored if its current temporal predicate can later change but no bounded dependency path can notify/reselect it.

The dependency projection may be rebuilt, but its reconstruction source/coverage must be deterministic from current owner/binding/provider contracts.

---

# 10. Live ownership / transfer integration

When a temporal owner is live-owned, its ordinary mutable lifecycle and any owner-local temporal state follow Step-5.8 authority.

Agenda/dependency routing follows the current lawful owner/provider basis.

Technical transitions:

```text
ACTIVE -> CLOSED
campaign absorption
successor opening
```

do not themselves create temporal dependency changes unless the accepted semantic owner/provider evidence actually changes.

If live-to-campaign transfer or cross-scene movement changes the temporal provider/binding semantics, the resulting coherent transition must update/rebuild the derivative Agenda enrollment without creating a window in which the armed owner is semantically current but unreachable by required reevaluation/recovery routing.

---

# 11. Performance contract

The intended ordinary cost is dependency-local:

```text
chronology/provider change touching K dependency keys
    -> O(K + enrolled consumers of K)
```

subject to bounded owner/domain-specific indexes.

Baseline ordinary play must not require:

```text
scan every Agenda entry after every action
scan every temporal owner after every chronology change
scan all scenes/processes for deadlines
rebuild full chronology to discover due work
poll host/wall clock to advance timers
```

A coarse invalidation of one explicitly bounded local partition is allowed when it is cheaper/simpler than maintaining finer reverse edges and the partition remains bounded by contract.

---

# 12. Integrity/coherence cases

The following are derivative integration defects, not alternate chronology semantics:

- armed independently-due owner has no reconstructible Agenda/dependency enrollment path;
- owner depends on current provider P but is enrolled only on obsolete provider Q after acknowledged transfer;
- accepted bridge/relation evidence changes a protected temporal predicate but no bounded invalidation path can reach the owner;
- stale Agenda entry materializes an occurrence no longer exposed by current native owner state;
- Agenda order is used to invent fictional order among multiple due obligations;
- host elapsed time is used to advance a metric provider without an admitted fictional transition.

On detection, refresh current owner/routing evidence and repair derivative indexes where possible. Do not invent or replay fictional time.

---

# 13. Machine-realization obligations

Later implementation planning must include:

1. deterministic extraction of temporal dependency keys from each admitted armed owner/binding family;
2. bounded reverse enrollment/indexing from dependency key -> armed temporal owner occurrence;
3. incremental invalidation from accepted metric-provider changes;
4. incremental invalidation from typed boundary/event occurrences;
5. incremental invalidation from newly accepted material-bridge/relation evidence;
6. coherent enrollment rewrite on owner/provider move, rebase, rearm, unarm, claim and terminalization;
7. Agenda/reverse-index rebuild from current native temporal roots after cold recovery;
8. stale-entry validation against current owner occurrence identity before materialization;
9. no-campaign-scan performance assertions;
10. observability sufficient to explain why an owner was or was not selected for reevaluation without making the index authority.

This is implementation debt/contract realization, not authorization to create a durable scheduler subsystem.

---

# 14. Required regression cases

Later tests should include at least:

```text
metric advance in Scene A reevaluates only Scene-A-dependent owners
unrelated Scene B advance does not reevaluate Scene-A-only owner
bounded metric range changes NOT_DUE -> INDETERMINATE -> DUE deterministically
boundary occurrence reevaluates matching boundary-bound owners without numeric time
late material bridge turns INDETERMINATE owner into decidable candidate
INDETERMINATE owner remains enrolled until owner lifecycle changes
owner transfer FOLLOW_CURRENT_SCOPE moves dependency enrollment to destination provider
PRESERVE_SOURCE_PROVIDER retains old provider dependency lawfully
SAFE_REBASE rewrites dependency enrollment without invented precision
rearm replaces old occurrence enrollment with new occurrence identity
CLAIMED occurrence no longer appears as fresh Agenda materialization candidate
terminal owner removes ordinary temporal enrollment
stale Agenda entry cannot fire settled owner
cold recovery rebuilds Agenda and dependency index from native owners
cold recovery discovers DUE without fictional-time advancement
multiple due owners are not ordered by Agenda/index traversal
live close/absorption alone triggers no fictional timer advance
no ordinary chronology change performs all-Agenda/campaign-wide scan
```

---

# 15. Closure statement

This amendment makes explicit the already intended interface:

> **Temporal Agenda is a rebuildable dependency-indexed candidate selector over native temporal owners. Chronology is the accepted evidence/provider substrate used to reevaluate those candidates. Accepted chronology changes invalidate only boundedly enrolled dependent owners; neither subsystem advances or executes the other.**

Steps 5.3 and 5.9 remain CLOSED. No new human architecture decision is introduced by this amendment.
